"""The drawing board's server (owner, 16 Oct 2026: "we should hand draw... know where something meets something").

python3 scripts/board_server.py [--port 8777]   then open http://127.0.0.1:8777/web/board.html

Serves the repo's files, and saves every edit made on the board into its district's hand file (web/hand/<d>.json, the
"edits" list, the same format scripts/hand.py applies), so the bake, the checks and the 3D all follow the drawing.

Edits made since the last bake are also kept in web/board-pending.json, so the board can draw them before the bake has
run: each carries the time it was made, and the board shows the ones newer than web/gidi-data.js.

The new frame (board.html?frame=new) draws the new map instead (docs/MAP-FORMAT.md): /api/map/* load and save whole records
by id in map/<district>/district.json and plan.json, in the canonical layout, and run scripts/check_map.py on the district
after every save so the board can show each record's problems. A record may be saved before every field has a value (the
board shows what is missing in red); the checker, not the board, says when it is complete.

Local only: it listens on 127.0.0.1, accepts only the hand-file operations below and plan records of the map schema, and
writes only web/hand/, that file and map/.
"""
import http.server
import json
import os
import re
import sys
import threading
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAND = os.path.join(ROOT, 'web', 'hand')
PENDING = os.path.join(ROOT, 'web', 'board-pending.json')
DATA = os.path.join(ROOT, 'web', 'gidi-data.js')
OPS = {'add building', 'delete building', 'move building', 'add furniture', 'delete furniture', 'move furniture',
       'add place', 'move place', 'delete place', 'add parcel', 'delete parcel', 'add monument', 'move monument',
       'delete monument', 'add zone', 'add street', 'delete street', 'cut street', 'name road', 'set surface', 'name',
       'reshape building', 'reshape parcel', 'reshape zone', 'reshape street',
       'cut wall', 'delete wall', 'add wall', 'add gate', 'delete gate',
       'set front', 'add tree', 'move tree', 'delete tree', 'add thing', 'move thing', 'delete thing', 'set house', 'add paint', 'delete paint', 'set storeys'}
LOCK = threading.Lock()   # one edit at a time: two quick saves must not overwrite each other
ROAD_OPS = {'add street', 'delete street', 'cut street', 'name road', 'reshape street'}   # a frozen district needs a thaw bake for these

# ------------------------------------------------------------------ the new map (docs/MAP-FORMAT.md)
MAP = os.path.join(ROOT, 'map')
STUDY = os.path.join(ROOT, 'web', 'frame-study.js')
DISTRICT_RE = re.compile(r'^d\d\d$')
ID_RE = re.compile(r'^[a-z]{1,2}-[a-z0-9]{8}$')
MAP_UNDO = []        # [(district, [(id, before, after), ...])], newest last; kept while the server runs
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
_checker = None


def checker():
    global _checker
    if _checker is None:
        import check_map
        _checker = check_map
    return _checker


def plan_types():
    S = checker().SCHEMA
    return {t for t, r in S['records'].items() if r['layer'] == 'plan'}


def map_files(d):
    return os.path.join(MAP, d, 'district.json'), os.path.join(MAP, d, 'plan.json')


def map_started():
    return sorted(d for d in os.listdir(MAP) if DISTRICT_RE.match(d) and os.path.exists(map_files(d)[0])) if os.path.isdir(MAP) else []


def read_doc(path):
    return json.load(open(path))


def write_doc(path, doc):
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh:
        fh.write(checker().canonical(doc))
    os.replace(tmp, path)


def map_state(d):
    """{id: record} for district d: the district record and every plan record."""
    fd, fp = map_files(d)
    recs = {r['id']: r for r in read_doc(fd).get('records', [])}
    if os.path.exists(fp):
        recs.update({r['id']: r for r in read_doc(fp).get('records', [])})
    return recs


def map_write(d, recs):
    fd, fp = map_files(d)
    S = checker().SCHEMA
    head = {'format': S['format'], 'district': d, 'layer': 'plan'}
    write_doc(fd, dict(head, records=[r for r in recs.values() if r['type'] == 'district']))
    write_doc(fp, dict(head, records=[r for r in recs.values() if r['type'] != 'district']))


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
    if t not in plan_types():
        return f'{t!r} is not a plan record type'
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


def districts():
    return {f[:-5] for f in os.listdir(HAND) if f.endswith('.json')}


def load_pending():
    try:
        return json.load(open(PENDING))
    except (OSError, ValueError):
        return []


def save_json(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh:
        json.dump(obj, fh, separators=(',', ':'))
    os.replace(tmp, path)


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
        if self.path.startswith('/api/pending'):
            return self.send_json({'data_time': os.path.getmtime(DATA), 'edits': load_pending()})
        if self.path.startswith('/api/map/'):
            with LOCK:
                return self.map_get()
        return super().do_GET()

    def map_get(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == '/api/map/list':
            return self.send_json({'districts': map_started(), 'study': os.path.exists(STUDY)})
        if u.path == '/api/map/load':
            d = (q.get('d') or [''])[0]
            if not DISTRICT_RE.match(d):
                return self.send_json({'error': f'no district {d!r}'}, 400)
            if d not in map_started():
                return self.send_json({'d': d, 'exists': False})
            return self.send_json({'d': d, 'exists': True, 'records': list(map_state(d).values()), 'problems': map_problems(d)})
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
        if self.path == '/api/edit':
            d, e = body.get('d'), body.get('edit')
            if d not in districts():
                return self.send_json({'error': f'no district {d!r}'}, 400)
            if not isinstance(e, dict) or e.get('op') not in OPS or not numbers_ok(e):
                return self.send_json({'error': 'not a hand-file edit'}, 400)
            e = dict(e, note=(str(e.get('note') or '') + ' (drawing board)').strip())
            path = os.path.join(HAND, d + '.json')
            H = json.load(open(path))
            H.setdefault('edits', []).append(e)
            save_json(path, H)
            P = load_pending()
            P.append({'t': time.time(), 'd': d, 'edit': e, 'thaw': e['op'] in ROAD_OPS})
            save_json(PENDING, P)
            return self.send_json({'ok': True, 'pending': len(P)})
        if self.path == '/api/undo':   # takes back the last edit made on the board, if it's still the last in its hand file
            P = load_pending()
            if not P:
                return self.send_json({'error': 'nothing to undo'}, 400)
            last = P[-1]
            path = os.path.join(HAND, last['d'] + '.json')
            H = json.load(open(path))
            if not H.get('edits') or H['edits'][-1] != last['edit']:
                return self.send_json({'error': 'that edit has been baked or changed since; undo it with a new edit'}, 409)
            H['edits'].pop()
            save_json(path, H)
            P.pop()
            save_json(PENDING, P)
            return self.send_json({'ok': True, 'pending': len(P)})
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
            map_write(d, recs)
            return self.send_json({'ok': True, 'd': d, 'records': list(recs.values()), 'problems': map_problems(d)})
        d = body.get('d')
        if not isinstance(d, str) or not DISTRICT_RE.match(d) or not 1 <= int(d[1:]) <= 99:
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
            map_write(d, {d: rec})
            return self.send_json({'ok': True, 'records': [rec], 'problems': map_problems(d)})
        if d not in map_started():
            return self.send_json({'error': f'{d} is not started yet'}, 400)
        recs = map_state(d)
        if self.path == '/api/map/save':       # whole records by id: new ones added, existing ones replaced
            new = body.get('records')
            if not isinstance(new, list) or not new:
                return self.send_json({'error': 'no records'}, 400)
            others = {r for o in map_started() if o != d for r in map_state(o)}
            for r in new:
                why = record_error(d, r)
                if why:
                    return self.send_json({'error': f'{r.get("id") if isinstance(r, dict) else r}: {why}'}, 400)
                if r['id'] in others:
                    return self.send_json({'error': f'{r["id"]} is already used in another district'}, 400)
            if len({r['id'] for r in new}) != len(new):
                return self.send_json({'error': 'the same id twice'}, 400)
            MAP_UNDO.append((d, [(r['id'], recs.get(r['id']), r) for r in new]))
            for r in new:
                recs[r['id']] = r
            map_write(d, recs)
            return self.send_json({'ok': True, 'problems': map_problems(d)})
        if self.path == '/api/map/delete':
            rid = body.get('id')
            if rid not in recs:
                return self.send_json({'error': f'{rid!r} is not in {d}'}, 400)
            if recs[rid]['type'] == 'district':
                return self.send_json({'error': 'the district record stays'}, 400)
            by = links_to(recs, rid)
            if by:
                return self.send_json({'error': f'{", ".join(by)} still point{"s" if len(by) == 1 else ""} at it: delete or relink them first'}, 409)
            MAP_UNDO.append((d, [(rid, recs.pop(rid), None)]))
            map_write(d, recs)
            return self.send_json({'ok': True, 'problems': map_problems(d)})
        if self.path == '/api/map/check':
            return self.send_json({'ok': True, 'problems': map_problems(d)})
        return self.send_json({'error': 'unknown'}, 404)


if __name__ == '__main__':
    port = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 8777
    print(f'Drawing board: http://127.0.0.1:{port}/web/board.html')
    http.server.ThreadingHTTPServer(('127.0.0.1', port), Board).serve_forever()
