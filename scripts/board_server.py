"""The drawing board's server (owner, 16 Oct 2026: "we should hand draw... know where something meets something").

python3 scripts/board_server.py [--port 8777]   then open http://127.0.0.1:8777/web/board.html

Serves the repo's files. The board draws the new map (docs/MAP-FORMAT.md): /api/map/* load and save whole records
by id in map/<district>/district.json, plan.json and dress/<tx>_<ty>.json (each dress record in its parent's 100 m
tile), in the canonical layout, and run scripts/check_map.py on the district
after every save so the board can show each record's problems. A record may be saved before every field has a value (the
board shows what is missing in red); the checker, not the board, says when it is complete.

Local only: it listens on 127.0.0.1, accepts only records of the map schema, and writes only map/.
"""
import http.server
import json
import os
import re
import sys
import threading
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = threading.Lock()   # one edit at a time: two quick saves must not overwrite each other

# ------------------------------------------------------------------ the new map (docs/MAP-FORMAT.md)
MAP = os.path.join(ROOT, 'map')
STUDY = os.path.join(ROOT, 'web', 'frame-study.js')
DISTRICT_RE = re.compile(r'^d\d\d$')
ID_RE = re.compile(r'^[a-z]{1,2}-[a-z0-9]{8}$')
TILE_RE = re.compile(r'^-?\d+_-?\d+\.json$')
MAP_UNDO = []        # [(district, [(id, before, after), ...])], newest last; kept while the server runs
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
_checker = None


def checker():
    global _checker
    if _checker is None:
        import check_map
        _checker = check_map
    return _checker


def layer_of(t):
    return checker().SCHEMA['records'][t]['layer']


def map_files(d):
    return os.path.join(MAP, d, 'district.json'), os.path.join(MAP, d, 'plan.json')


def map_started(top=MAP):
    return sorted(d for d in os.listdir(top) if DISTRICT_RE.match(d) and os.path.exists(os.path.join(top, d, 'district.json'))) if os.path.isdir(top) else []


def read_doc(path):
    return json.load(open(path))


def write_doc(path, doc):
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh:
        fh.write(checker().canonical(doc))
    os.replace(tmp, path)


def doc_names(top, d):
    """district.json, plan.json and every dress tile of district d, as paths inside its folder."""
    dd = os.path.join(top, d, 'dress')
    tiles = sorted('dress/' + f for f in os.listdir(dd) if TILE_RE.match(f)) if os.path.isdir(dd) else []
    return [n for n in ('district.json', 'plan.json') if os.path.exists(os.path.join(top, d, n))] + tiles


_STATE = {}          # district -> {'sig', 'recs': {id: record}, 'loc': {id: file inside the district folder}}


def load_state(d, top=MAP):
    """Every record of district d and the file each one is in, read again only when a file has changed on disk."""
    names = doc_names(top, d)
    sig = tuple((n, os.stat(os.path.join(top, d, n)).st_mtime_ns, os.path.getsize(os.path.join(top, d, n))) for n in names)
    key = (top, d)
    S = _STATE.get(key)
    if S and S['sig'] == sig:
        return S
    recs, loc = {}, {}
    for n in names:
        for r in read_doc(os.path.join(top, d, n)).get('records', []):
            recs[r['id']], loc[r['id']] = r, n
    S = _STATE[key] = {'sig': sig, 'recs': recs, 'loc': loc}
    return S


def map_state(d):
    """{id: record} for district d (a copy: change it, then map_write the ids that changed)."""
    return dict(load_state(d)['recs'])


def home_of(r, recs):
    """The file a record belongs in: district.json, plan.json, or the dress tile of its parent's first point (its own
    first point when it has no parent; a lean-to's, the point of what it leans on), as check_map.py wants it. None when a dress record has neither."""
    if r['type'] == 'district':
        return 'district.json'
    if layer_of(r['type']) == 'plan':
        return 'plan.json'
    C = checker()
    a, par, seen = None, recs.get(r.get('of')), set()
    while par and a is None and par['id'] not in seen:     # a lean-to has no point of its own: go to what it leans on
        seen.add(par['id'])
        a = C.anchor(par)
        par = recs.get(par.get('of') or par.get('against'))
    a = a or C.anchor(r)
    if a is None:
        return None
    tx, ty = C.tile_of(a)
    return f'dress/{tx}_{ty}.json'


def map_write(d, recs, changed):
    """Write the files that the changed (or removed) ids touch, and their dress children's, which follow the parent's tile."""
    S = load_state(d)
    loc = dict(S['loc'])
    ids, grow = set(changed), True
    while grow:                          # and what hangs on them, which may have to follow them into another tile
        more = {i for i, r in recs.items() if i not in ids and (r.get('of') in ids or r.get('against') in ids)}
        ids |= more
        grow = bool(more)
    files = {loc[i] for i in ids if i in loc}
    for i in ids:
        if i in recs:
            loc[i] = home_of(recs[i], recs)
            files.add(loc[i])
        else:
            loc.pop(i, None)
    head = {'format': checker().SCHEMA['format'], 'district': d}
    for n in sorted(files):
        p = os.path.join(MAP, d, n)
        recs_n = [recs[i] for i, f in loc.items() if f == n]
        if n.startswith('dress/'):
            if not recs_n:
                if os.path.exists(p):
                    os.remove(p)
                continue
            os.makedirs(os.path.dirname(p), exist_ok=True)
            write_doc(p, dict(head, layer='dress', tile=[int(x) for x in re.findall(r'-?\d+', n)], records=recs_n))
        else:
            write_doc(p, dict(head, layer='plan', records=recs_n))
    _STATE.pop((MAP, d), None)
    S = load_state(d)
    return S


def stamp_sources():
    """Folders in the map format a stamp can copy from: the map itself, the worked example, and each folder under map-stamps/
    (a test spot converted into Gidi metres goes there)."""
    out = {'map': MAP, 'example': os.path.join(ROOT, 'docs', 'map-format-example')}
    extra = os.path.join(ROOT, 'map-stamps')
    if os.path.isdir(extra):
        for n in sorted(os.listdir(extra)):
            if os.path.isdir(os.path.join(extra, n)) and re.fullmatch(r'[a-z0-9_-]+', n):
                out[n] = os.path.join(extra, n)
    return out


def map_problems(d):
    """check_map.py on one district: [{id, field, msg}], id None for a file-level problem."""
    C = checker()
    del C.errors[:]
    C.check(MAP, only=[d])
    out = []
    for e in C.errors:
        where, _, msg = e.partition(': ')
        rest = where.split(' ', 1)[1] if ' ' in where else ''
        m = re.match(r'([a-z]{1,2}-[a-z0-9]{8}|d\d\d)', rest)
        rid = m.group(1) if m else None
        out.append({'id': rid, 'field': rest[len(rid):].lstrip('.') if rid else '', 'msg': msg, 'where': where})
    del C.errors[:]
    return out


def links_to(recs, rid):
    """Ids of the records that point at rid (a plot, road, place, building or pole they hang on)."""
    def has(v):
        return v == rid if isinstance(v, str) else any(has(x) for x in v) if isinstance(v, list) else any(has(x) for x in v.values()) if isinstance(v, dict) else False
    return [r['id'] for r in recs.values() if r['id'] != rid and any(has(v) for k, v in r.items() if k not in ('id', 'note'))]


def record_error(d, r):
    """Why a record can't be saved at all, or None. Missing fields are allowed (the board shows them); strays are not."""
    S = checker().SCHEMA
    if not isinstance(r, dict):
        return 'not a record'
    t = r.get('type')
    if t not in S['records']:
        return f'{t!r} is not a record type'
    if t == 'district':
        if r.get('id') != d or r.get('n') != int(d[1:]):
            return 'the district record is the one for this district'
    elif not ID_RE.match(str(r.get('id'))) or str(r['id']).split('-')[0] != S['records'][t]['prefix']:
        return f'id {r.get("id")!r} should look like {S["records"][t]["prefix"]}-k3v8q2xa'
    fields = dict(S['common'], **S['records'][t]['fields'])
    stray = [k for k in r if k not in fields]
    if stray:
        return f'unknown field{"s" if len(stray) > 1 else ""} {", ".join(stray)}'
    if not numbers_ok(r):
        return 'a number is not finite'
    return None


def district_from_study(d):
    """A new district record: its number and its outline from the frame study (scripts/frame_study.py). No name: names
    are given by hand (a working name per district, decisions 22 Oct)."""
    if d == 'd00':                     # the city layer: the whole frame (owner, 28 Oct: the roads for the entire map first)
        return {'id': d, 'type': 'district', 'n': 0, 'name': 'Gidi', 'outline': [[[0, 0], [27000, 0], [27000, 10500], [0, 10500]]],
                'note': 'the city layer: the main roads, bridges, rail and water of the whole map, not cut at district lines'}
    s = open(STUDY).read()
    F = json.loads(s[s.index('{'):s.rindex('}') + 1])
    n = int(d[1:])
    D = next((x for x in F['districts'] if x['n'] == n), None)
    if D is None:
        return None
    outline = []
    for poly in D['rings']:            # the outer ring of each piece; the first point is not repeated at the end
        ring = [[round(x, 2), round(y, 2)] for x, y in poly[0]]
        if len(ring) > 1 and ring[0] == ring[-1]:
            ring.pop()
        if len(ring) >= 3:
            outline.append(ring)
    return {'id': d, 'type': 'district', 'n': n, 'outline': outline,
            'note': 'outline from the frame study (scripts/frame_study.py); redraw by hand where the border is decided'}


def numbers_ok(v):
    """Every number in an edit is finite (no NaN or infinity from a slip of the mouse)."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v == v and abs(v) < 1e7
    if isinstance(v, list):
        return all(numbers_ok(x) for x in v)
    if isinstance(v, dict):
        return all(numbers_ok(x) for x in v.values())
    return True


class Board(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, fmt, *args):
        if self.command != 'GET':
            sys.stderr.write('%s %s\n' % (self.command, fmt % args))

    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        if self.path.endswith('.js') or self.path.endswith('.html'):
            self.send_header('Cache-Control', 'no-store')   # always the latest bake and board code
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/api/map/'):
            with LOCK:
                return self.map_get()
        return super().do_GET()

    def map_get(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == '/api/map/list':
            return self.send_json({'districts': map_started(), 'study': os.path.exists(STUDY)})
        if u.path == '/api/map/load':          # the district record and the plan; dress tiles come one by one (tiles)
            d = (q.get('d') or [''])[0]
            if not DISTRICT_RE.match(d):
                return self.send_json({'error': f'no district {d!r}'}, 400)
            if d not in map_started():
                return self.send_json({'d': d, 'exists': False})
            S = load_state(d)
            return self.send_json({'d': d, 'exists': True, 'records': [r for i, r in S['recs'].items() if not S['loc'][i].startswith('dress/')],
                                   'tiles': sorted({f[6:-5] for f in S['loc'].values() if f.startswith('dress/')}), 'problems': map_problems(d)})
        if u.path == '/api/map/tiles':         # the dress records of some tiles: t=128_60,128_61
            d = (q.get('d') or [''])[0]
            if d not in map_started():
                return self.send_json({'error': f'{d!r} is not started'}, 400)
            want = {'dress/' + t + '.json' for t in (q.get('t') or [''])[0].split(',') if re.fullmatch(r'-?\d+_-?\d+', t)}
            S = load_state(d)
            return self.send_json({'d': d, 'records': [r for i, r in S['recs'].items() if S['loc'][i] in want]})
        if u.path == '/api/map/sources':
            return self.send_json({'sources': [{'src': k, 'districts': map_started(v)} for k, v in stamp_sources().items()]})
        if u.path == '/api/map/source':        # every record of one district of a stamp source, plan and dress
            src, d = (q.get('src') or [''])[0], (q.get('d') or [''])[0]
            top = stamp_sources().get(src)
            if not top or d not in map_started(top):
                return self.send_json({'error': f'no district {d!r} in {src!r}'}, 400)
            return self.send_json({'src': src, 'd': d, 'records': list(load_state(d, top)['recs'].values())})
        return self.send_json({'error': 'unknown'}, 404)

    def do_POST(self):
        with LOCK:
            return self.post()

    def post(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
        except ValueError:
            return self.send_json({'error': 'not JSON'}, 400)
        if self.path.startswith('/api/map/'):
            return self.map_post(body)
        return self.send_json({'error': 'unknown'}, 404)

    def map_post(self, body):
        if self.path == '/api/map/undo':       # the last save or delete on the map, if nothing has changed it since
            if not MAP_UNDO:
                return self.send_json({'error': 'nothing to undo'}, 400)
            d, steps = MAP_UNDO[-1]
            recs = map_state(d)
            for rid, before, after in steps:
                if recs.get(rid) != after:
                    return self.send_json({'error': f'{rid} has changed since; change it back by hand'}, 409)
            MAP_UNDO.pop()
            for rid, before, after in steps:
                if before is None:
                    recs.pop(rid, None)
                else:
                    recs[rid] = before
            map_write(d, recs, [rid for rid, _, _ in steps])
            return self.send_json({'ok': True, 'd': d, 'changed': [recs[rid] for rid, _, _ in steps if rid in recs],
                                   'removed': [rid for rid, _, _ in steps if rid not in recs], 'problems': map_problems(d)})
        d = body.get('d')
        if not isinstance(d, str) or not DISTRICT_RE.match(d) or not 0 <= int(d[1:]) <= 99:
            return self.send_json({'error': f'no district {d!r}'}, 400)
        if self.path == '/api/map/start':      # the first drawing in a district: its record and an empty plan
            if d in map_started():
                return self.send_json({'error': f'{d} is already started'}, 409)
            if not os.path.exists(STUDY):
                return self.send_json({'error': 'no frame study: run scripts/frame_study.py'}, 400)
            rec = district_from_study(d)
            if rec is None:
                return self.send_json({'error': f'the frame study has no district {int(d[1:])}'}, 400)
            os.makedirs(os.path.join(MAP, d), exist_ok=True)
            write_doc(map_files(d)[1], {'format': checker().SCHEMA['format'], 'district': d, 'layer': 'plan', 'records': []})
            map_write(d, {d: rec}, [d])
            return self.send_json({'ok': True, 'records': [rec], 'problems': map_problems(d)})
        if d not in map_started():
            return self.send_json({'error': f'{d} is not started yet'}, 400)
        recs = map_state(d)
        if self.path == '/api/map/save':       # whole records by id: new ones added, existing ones replaced
            new, drop = body.get('records', []), body.get('remove', [])   # remove: ids to take away in the same undo step (a brush stroke)
            if not isinstance(new, list) or not isinstance(drop, list) or not (new or drop):
                return self.send_json({'error': 'no records'}, 400)
            for rid in drop:
                if rid not in recs or recs[rid]['type'] == 'district' or rid in {r.get('id') for r in new if isinstance(r, dict)}:
                    return self.send_json({'error': f'{rid!r} can not be removed here'}, 400)
            others = {r for o in map_started() if o != d for r in map_state(o)}
            for r in new:
                why = record_error(d, r)
                if why:
                    return self.send_json({'error': f'{r.get("id") if isinstance(r, dict) else r}: {why}'}, 400)
                if r['id'] in others:
                    return self.send_json({'error': f'{r["id"]} is already used in another district'}, 400)
            for r in new:
                recs[r['id']] = r
            for r in new:
                if home_of(r, recs) is None:
                    return self.send_json({'error': f'{r["id"]}: a dress record needs its parent (of) or a point of its own, to find its tile'}, 400)
            for rid in drop:
                recs.pop(rid, None)
            by = sorted({b for rid in drop for b in links_to(recs, rid)})
            if by:
                return self.send_json({'error': f'{", ".join(by)} still point{"s" if len(by) == 1 else ""} at {", ".join(drop)}'}, 409)
            recs = map_state(d)
            if len({r['id'] for r in new}) != len(new):
                return self.send_json({'error': 'the same id twice'}, 400)
            MAP_UNDO.append((d, [(r['id'], recs.get(r['id']), r) for r in new] + [(rid, recs[rid], None) for rid in drop]))
            for r in new:
                recs[r['id']] = r
            for rid in drop:
                recs.pop(rid)
            map_write(d, recs, [r['id'] for r in new] + drop)
            return self.send_json({'ok': True, 'removed': drop, 'problems': map_problems(d)})
        if self.path == '/api/map/delete':
            rid = body.get('id')
            if rid not in recs:
                return self.send_json({'error': f'{rid!r} is not in {d}'}, 400)
            if recs[rid]['type'] == 'district':
                return self.send_json({'error': 'the district record stays'}, 400)
            gone = [rid]                        # children: true also takes the dress records that dress it (faces, goods...)
            if body.get('children'):            # and the person spots that belong to it (parent)
                for i in gone:
                    gone += [c for c, r in recs.items() if (r.get('of') == i or r.get('parent') == i) and c not in gone]
            by = [b for b in links_to(recs, rid) if b not in gone]
            for c in gone[1:]:
                by += [b for b in links_to(recs, c) if b not in gone and b not in by]
            if by:
                return self.send_json({'error': f'{", ".join(by)} still point{"s" if len(by) == 1 else ""} at it: delete or relink them first'}, 409)
            MAP_UNDO.append((d, [(i, recs.pop(i), None) for i in gone]))
            map_write(d, recs, gone)
            return self.send_json({'ok': True, 'removed': gone, 'problems': map_problems(d)})
        if self.path == '/api/map/check':
            return self.send_json({'ok': True, 'problems': map_problems(d)})
        return self.send_json({'error': 'unknown'}, 404)


if __name__ == '__main__':
    port = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 8777
    print(f'Drawing board: http://127.0.0.1:{port}/web/board.html')
    http.server.ThreadingHTTPServer(('127.0.0.1', port), Board).serve_forever()
