"""The new map's checker (docs/MAP-FORMAT.md; owner, 22 Oct 2026: "one ground truth"). Nothing in the map is guessed: a
record with an unknown field, a wrong type, a broken link or a real name fails here, before the board, the kit or the
Unreal import ever reads it. A field not given yet is counted as still to fill (TODO), and fails too with --strict.

  python3 scripts/check_map.py <map dir>                      check every district under it (map/ by default)
  python3 scripts/check_map.py <map dir> --kit schema/kit_reads.json   also check what each kit part reads
  python3 scripts/check_map.py <map dir> --sizes              bytes and counts per record type
  python3 scripts/check_map.py <map dir> --fix                rewrite each file in the canonical layout (one record a line)

A map dir holds one folder per district: district.json, plan.json and dress/<tx>_<ty>.json (100 m tiles). The schema is
schema/map_schema.json. Exits 1 on any problem. A field not given yet is counted on a TODO line, not a problem (the
board shows it amber); with --strict it fails too.
"""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(open(os.path.join(ROOT, 'schema', 'map_schema.json')))
TILE = 100.0                 # dress tiles, m
ON_ROAD = 1.0                # m2 of a house inside a carriageway that fails (DECISIONS: the road comes first)
JOIN = (0.01, 1.0)           # two road ends closer than 1 m but not on the same point: a slip, not a junction
HEADER = {'format', 'district', 'layer', 'tile', 'records'}
ID_RE = re.compile(r'^[a-z]{1,2}-[a-z0-9]{8}$')

errors = []
corners = []                 # road lines the kit can't round without folding: hand edits still to do (amber, like TODO)
staggered = []               # road ends on a node within reach of another road's node: one junction the kit must still join
TODO = re.compile(r": missing (?:field|value) '([^']+)'")      # what the board shows amber


def err(where, msg):
    errors.append(f'{where}: {msg}')


# ------------------------------------------------------------------ real names (a Gidi name may not share a real name's core)
def name_cores():
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    try:
        import realnames
    except ImportError:
        return (lambda n: n.lower()), set()
    cores = set(realnames.cores())
    study = os.path.join(ROOT, 'web', 'frame-study.js')   # the new frame's 819 real places (gitignored; used when present)
    if os.path.exists(study):
        s = open(study).read()
        for p in json.loads(s[s.index('{'):s.rindex('}') + 1]).get('places', []):
            c = realnames.core(p.get('n', ''))
            if c:
                cores.add(c)
    return realnames.core, cores


CORE, CORES = name_cores()


# ------------------------------------------------------------------ one value against one field spec
def parse(spec):
    opt = spec.endswith('?')
    spec = spec.rstrip('?').strip()
    kind, _, rng = spec.partition(' ')
    return kind, rng.strip(), opt


def in_range(v, rng):
    if not rng:
        return True
    if rng.startswith('>='):
        return v >= float(rng[2:])
    if rng.startswith('>'):
        return v > float(rng[1:])
    a, b = rng.split('..')
    return float(a) <= v <= float(b)


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def is_pt(v, dims=(2, 3)):
    return isinstance(v, list) and len(v) in dims and all(is_num(x) for x in v)


def check_value(where, v, spec, refs):
    kind, rng, _ = parse(spec)
    base, _, arg = kind.partition(':')
    if base in ('num', 'int'):
        if not is_num(v) or (base == 'int' and not isinstance(v, int)):
            return err(where, f'should be a{"n integer" if base == "int" else " number"}, is {v!r}')
        if not in_range(v, rng):
            return err(where, f'{v} is outside {rng}')
    elif base in ('nums', 'ints'):
        if not isinstance(v, list) or not all(is_num(x) and (base == 'nums' or isinstance(x, int)) for x in v):
            err(where, f'should be a list of {"numbers" if base == "nums" else "integers"}')
    elif base == 'angles':
        if not (is_num(v) or isinstance(v, list) and v and all(is_num(x) for x in v)):
            err(where, 'should be a number or a list of numbers')
    elif base == 'numss':
        if not isinstance(v, list) or not all(isinstance(x, list) and all(is_num(y) for y in x) for x in v):
            err(where, 'should be a list of lists of numbers')
    elif base == 'bool':
        if not isinstance(v, bool):
            err(where, f'should be true or false, is {v!r}')
    elif base in ('str', 'surface', 'name', 'text'):
        if not isinstance(v, str) or not v:
            return err(where, f'should be some text, is {v!r}')
        if base == 'surface' and not re.fullmatch(r'[a-z0-9_]+', v):
            err(where, f'{v!r} is not a photo surface name (textures folder, lower_case)')
        if base in ('name', 'text') and CORE(v) and CORE(v) in CORES:
            err(where, f'{v!r} shares its core with a real name; Gidi names are its own')
    elif base == 'strs':
        if not isinstance(v, list) or not all(isinstance(x, str) and x for x in v):
            err(where, 'should be a list of text')
    elif base == 'hex':
        if not isinstance(v, str) or not re.fullmatch(r'#[0-9a-f]{6}', v):
            err(where, f'should be a colour like "#a1b2c3", is {v!r}')
    elif base == 'hexes':
        if not isinstance(v, list) or not v or not all(isinstance(x, str) and re.fullmatch(r'#[0-9a-f]{6}', x) for x in v):
            err(where, 'should be a list of colours like "#a1b2c3"')
    elif base == 'pt':
        if not is_pt(v, (2,)):
            err(where, f'should be a point [x, y], is {v!r}')
    elif base == 'pt3':
        if not is_pt(v, (3,)):
            err(where, f'should be a point [x, y, z], is {v!r}')
    elif base == 'line':
        if not isinstance(v, list) or len(v) < 2 or not all(is_pt(p) for p in v):
            err(where, 'should be a line of at least 2 points')
    elif base == 'ring':
        check_ring(where, v)
    elif base == 'rings':
        if not isinstance(v, list) or not v:
            return err(where, 'should be a list of rings')
        for i, r in enumerate(v):
            check_ring(f'{where}[{i}]', r)
    elif base == 'enum':
        if v not in SCHEMA['enums'][arg]:
            err(where, f'{v!r} is not one of {arg}: {", ".join(SCHEMA["enums"][arg])}')
    elif base == 'enums':
        if not isinstance(v, list) or any(x not in SCHEMA['enums'][arg] for x in v):
            err(where, f'should be a list from {arg}: {", ".join(SCHEMA["enums"][arg])}')
    elif base == 'dict':                       # keyed by the data's own names (a garment's colour by its name)
        if not isinstance(v, dict) or not all(isinstance(k, str) for k in v):
            err(where, 'should be an object keyed by names')
    elif base == 'obj':
        check_obj(where, v, SCHEMA['shapes'][arg], refs)
    elif base == 'objs':
        if not isinstance(v, list):
            return err(where, 'should be a list')
        for i, o in enumerate(v):
            check_obj(f'{where}[{i}]', o, SCHEMA['shapes'][arg], refs)
    elif base == 'table':
        check_table(where, v, arg, refs)
    elif base == 'id':
        if not isinstance(v, str):
            return err(where, f'should be a record id, is {v!r}')
        refs.append((where, v, arg.split(',')))
    else:
        err(where, f'schema has an unknown type {kind!r}')


def check_ring(where, r):
    if not isinstance(r, list) or len(r) < 3 or not all(is_pt(p, (2,)) for p in r):
        return err(where, 'should be a ring of at least 3 [x, y] points')
    if r[0] == r[-1]:
        err(where, 'a ring does not repeat its first point at the end')
    if abs(area(r)) < 0.01:
        err(where, 'the ring has no area')
    n = len(r)
    for i in range(n):          # no edge crosses another (a footprint that folds over itself is a drawing slip)
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if crosses(r[i], r[(i + 1) % n], r[j], r[(j + 1) % n]):
                return err(where, f'the ring crosses itself (edges {i} and {j})')


def area(r):
    return sum(r[i][0] * r[(i + 1) % len(r)][1] - r[(i + 1) % len(r)][0] * r[i][1] for i in range(len(r))) / 2


def crosses(a, b, c, d):
    o = lambda p, q, r: (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def check_obj(where, o, shape, refs, extra=()):
    if not isinstance(o, dict):
        return err(where, 'should be an object')
    for k in o:
        if k not in shape and k not in extra:
            err(where, f'unknown field {k!r}')
    for k, spec in shape.items():
        if k in o:
            check_value(f'{where}.{k}', o[k], spec, refs)
        elif not spec.endswith('?'):
            err(where, f'missing field {k!r}')


def check_table(where, t, name, refs):
    cols = SCHEMA['tables'][name]
    if not isinstance(t, dict) or set(t) != {'cols', 'rows'}:
        return err(where, 'a table is {"cols": [...], "rows": [[...], ...]}')
    if t['cols'] != [c for c, _ in cols]:
        return err(where, f'columns should be {[c for c, _ in cols]}, are {t["cols"]}')
    if not isinstance(t['rows'], list):
        return err(where, 'rows should be a list')
    for i, row in enumerate(t['rows']):
        if not isinstance(row, list) or len(row) != len(cols):
            err(f'{where}.rows[{i}]', f'should have {len(cols)} values')
            continue
        for (c, spec), v in zip(cols, row):
            if v is None and not spec.endswith('?'):      # a cell drawn but not given yet: still to set, like a missing field
                err(f'{where}.rows[{i}]', f'missing value {c!r}')
            elif v is not None:
                check_value(f'{where}.rows[{i}].{c}', v, spec, refs)


# ------------------------------------------------------------------ geometry helpers for the cross-checks
def anchor(r):
    """The point that decides which dress tile a record lives in."""
    for k in ('footprint', 'outline', 'centreline', 'line'):
        if isinstance(r.get(k), list) and r[k] and is_pt(r[k][0]):
            return r[k][0][:2]
    for k in ('at', 'origin'):
        if is_pt(r.get(k)):
            return r[k][:2]
    if isinstance(r.get('rings'), list) and r['rings'] and isinstance(r['rings'][0], list) and r['rings'][0] and is_pt(r['rings'][0][0]):
        return r['rings'][0][0]
    for k in ('pieces', 'spots'):
        t = r.get(k)
        if isinstance(t, dict) and t.get('rows') and 'x' in t.get('cols', []):
            row = t['rows'][0]
            return [row[t['cols'].index('x')], row[t['cols'].index('y')]]
    return None


def tile_of(p):
    return [int(math.floor(p[0] / TILE)), int(math.floor(p[1] / TILE))]


def in_poly(p, poly):
    c = False
    for i in range(len(poly)):
        a, b = poly[i], poly[i - 1]
        if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]:
            c = not c
    return c


def face_len(fp, i):
    a, b = fp[i], fp[(i + 1) % len(fp)]
    return math.hypot(b[0] - a[0], b[1] - a[1])


# ------------------------------------------------------------------ files
def canonical(doc):
    """One record a line, sorted by id: the board writes this, git diffs it record by record."""
    head = {k: doc[k] for k in ('format', 'district', 'layer', 'tile') if k in doc}
    recs = sorted(doc.get('records', []), key=lambda r: str(r.get('id')))
    lines = [json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in recs]
    h = json.dumps(head, ensure_ascii=False, separators=(',', ':'))[:-1]
    return h + ',"records":[\n' + ',\n'.join(lines) + '\n]}\n'


def load_map(top, fix, only=None):
    files = []
    for d in sorted(os.listdir(top)):
        dd = os.path.join(top, d)
        if not os.path.isdir(dd) or (only and d not in only):
            continue
        names = ['district.json', 'plan.json'] + ['dress/' + f for f in sorted(os.listdir(os.path.join(dd, 'dress')))
                                                   if f.endswith('.json')] if os.path.isdir(os.path.join(dd, 'dress')) else ['district.json', 'plan.json']
        for n in names:
            p = os.path.join(dd, n)
            if not os.path.exists(p):
                err(f'{d}/{n}', 'missing file')
                continue
            text = open(p).read()
            try:
                doc = json.loads(text)
            except ValueError as e:
                err(f'{d}/{n}', f'not JSON ({e})')
                continue
            files.append((d, n, p, doc))
            if text != canonical(doc):
                if fix:
                    open(p, 'w').write(canonical(doc))
                else:
                    err(f'{d}/{n}', 'not in the canonical layout (one record a line, sorted by id); run with --fix')
    return files


CITY = 'd00'                      # the city layer (owner, 28 Oct): the main roads, bridges, rail and water of the whole map,
CITY_TYPES = {'district', 'road', 'rail', 'water', 'relief'}   # not cut at district lines; districts' streets join them on
                                                    # shared points; its relief grids are the land's own height (owner, 28 Oct)
FRAME = (27000, 10500)            # the frame, Gidi m: the city layer's land covers it all
WATER_AREA = {'sea', 'lagoon', 'pond', 'marsh'}     # as Unreal's water bodies: a closed outline at one level (ocean, lake)
WATER_LINE = {'river', 'creek', 'canal'}            # or an open line with a width, one per point if they vary (river)
CITY_ROADS = {'motorway', 'trunk', 'main_road', 'local_main', 'ramp'}


def check(top, fix=False, only=None):
    """Check the map under top (only: a list of district folders to check, as the board does on each save)."""
    if only and CITY not in only and os.path.isdir(os.path.join(top, CITY)):
        only = list(only) + [CITY]    # the city roads cross every district: a district is checked with them in view
    files = load_map(top, fix, only)
    recs, where_of, refs = {}, {}, []
    for d, n, p, doc in files:
        w = f'{d}/{n}'
        for k in doc:
            if k not in HEADER:
                err(w, f'unknown header field {k!r}')
        if doc.get('format') != SCHEMA['format']:
            err(w, f'format should be {SCHEMA["format"]!r}')
        if doc.get('district') != d:
            err(w, f'district should be {d!r} (its folder)')
        layer = 'dress' if n.startswith('dress/') else 'plan'
        if doc.get('layer') != layer:
            err(w, f'layer should be {layer!r}')
        if layer == 'dress':
            want = [int(x) for x in re.findall(r'-?\d+', n)]
            if doc.get('tile') != want:
                err(w, f'tile should be {want} (its file name)')
        for r in doc.get('records', []):
            rid, rt = r.get('id'), r.get('type')
            rw = f'{w} {rid}'
            if rt not in SCHEMA['records']:
                err(rw, f'unknown record type {rt!r}')
                continue
            spec = SCHEMA['records'][rt]
            if (n == 'district.json') != (rt == 'district'):
                err(rw, 'district.json holds the district record and nothing else')
            elif spec['layer'] != layer:
                err(rw, f'a {rt} belongs in the {spec["layer"]} layer')
            ok = re.fullmatch(r'd\d\d', str(rid)) if rt == 'district' else (ID_RE.match(str(rid)) and str(rid).split('-')[0] == spec['prefix'])
            if not ok:
                err(rw, f'id should look like {"d07" if rt == "district" else spec["prefix"] + "-" + "k3v8q2xa"}')
            if rid in recs:
                err(rw, f'id already used in {where_of[rid]}')
            recs[rid], where_of[rid] = r, w
            fields = dict(SCHEMA['common'], **spec['fields'])
            check_obj(rw, r, fields, refs)
            for group in spec.get('one_of', []):
                if sum(k in r for k in group) != 1:
                    err(rw, f'needs exactly one of {group}')
            r['_file'], r['_district'], r['_tile'] = w, d, doc.get('tile')

    for w, rid, types in refs:      # every link lands on a record of the right type
        t = recs.get(rid)
        if t is None:
            err(w, f'points to {rid!r}, which is not on the map')
        elif t['type'] not in types:
            err(w, f'points to a {t["type"]}, should be a {" or ".join(types)}')

    dist = {r['_district']: r for r in recs.values() if r.get('type') == 'district'}
    for rid, r in recs.items():
        rt, w = r.get('type'), f'{r["_file"]} {rid}'
        if rt == 'building' and isinstance(r.get('storey_h'), list) and r.get('storeys') != len(r['storey_h']):
            err(w, f'storey_h has {len(r["storey_h"])} heights for {r.get("storeys")} storeys')
        if rt == 'building' and isinstance(r.get('footprint'), list) and len(r['footprint']) >= 3 and area(r['footprint']) > 0:
            err(w, 'footprint runs the wrong way: walking from point i to i+1 the building is on your left on the board')
        if rt == 'relief' and isinstance(r.get('z_mm'), list) and len(r['z_mm']) != r.get('cols', 0) * r.get('rows', 0):
            err(w, f'z_mm has {len(r["z_mm"])} values, cols x rows is {r.get("cols", 0) * r.get("rows", 0)}')
        if rt == 'person_spot' and isinstance(r.get('hours'), list):     # when someone is there: one or more from-to spans
            if not r['hours']:
                err(w, "missing value 'hours': at least one from-to span (0 to 24 is all day; 22 to 5 runs past midnight)")
            for i, h in enumerate(r['hours']):
                if isinstance(h, dict) and is_num(h.get('from')) and h.get('from') == h.get('to'):
                    err(f'{w}.hours[{i}]', 'from and to are the same hour: the span is empty (0 to 24 is all day)')
        if rt == 'leanto' and recs.get(r.get('against'), {}).get('type') == 'building':
            fp = recs[r['against']].get('footprint') or []
            if not isinstance(r.get('face'), int) or not 0 <= r['face'] < len(fp):
                err(w, 'a lean-to against a building needs the face it leans on')
            elif r.get('u1', 0) > face_len(fp, r['face']) + 0.05 or r.get('u0', 0) >= r.get('u1', 0):
                err(w, f'u0..u1 should run along face {r["face"]} (0..{face_len(fp, r["face"]):.2f} m)')
        if rt == 'faces' and recs.get(r.get('of'), {}).get('type') == 'building':
            b = recs[r['of']]
            fp, top = b.get('footprint') or [], sum(b.get('storey_h') or [0]) + 4
            for i, f in enumerate(r.get('faces') or []):
                fi = f.get('face')
                if not isinstance(fi, int) or not 0 <= fi < len(fp):
                    err(f'{w}.faces[{i}]', f'face {fi} is not an edge of the footprint (0..{len(fp) - 1})')
                    continue
                L = face_len(fp, fi)
                for key in ('windows', 'doors', 'stains', 'addons'):
                    t = f.get(key) or {}
                    for j, row in enumerate(t.get('rows') or []):
                        o = dict(zip(t.get('cols', []), row))
                        u, z = o.get('u'), o.get('z', 0)
                        if is_num(u) and not -0.05 <= u <= L + 0.05:
                            err(f'{w}.faces[{i}].{key}.rows[{j}]', f'u {u} is off the face (0..{L:.2f} m)')
                        if is_num(z) and not -0.5 <= z <= top:
                            err(f'{w}.faces[{i}].{key}.rows[{j}]', f'z {z} is off the building (0..{top:.1f} m)')
                for key in ('shopfronts', 'balconies', 'screens', 'signs'):
                    for j, o in enumerate(f.get(key) or []):
                        if is_num(o.get('u0')) and is_num(o.get('u1')) and not (0 <= o['u0'] < o['u1'] <= L + 0.05):
                            err(f'{w}.faces[{i}].{key}[{j}]', f'u0..u1 should run along the face (0..{L:.2f} m)')
        if 'of' in r and r['of'] in recs:        # a dress record lives with its parent: same district, the parent's tile
            par = recs[r['of']]
            if par['_district'] != r['_district']:
                err(w, f'its parent {r["of"]} is in district {par["_district"]}')
            a = anchor(par)
            if r.get('_tile') is not None and a is not None and tile_of(a) != r['_tile']:
                err(w, f'belongs in dress/{tile_of(a)[0]}_{tile_of(a)[1]}.json, beside its parent')
        elif SCHEMA['records'].get(rt, {}).get('layer') == 'dress' and r.get('_tile') is not None:
            a = anchor(r)
            if a is not None and tile_of(a) != r['_tile']:
                err(w, f'its first point is in tile {tile_of(a)}, not {r["_tile"]}')
        if SCHEMA['records'].get(rt, {}).get('layer') == 'plan' and rt != 'district':
            a, D = anchor(r), dist.get(r['_district'])
            if a and D and isinstance(D.get('outline'), list) and not any(in_poly(a, ring) for ring in D['outline']):
                err(w, f'stands outside its district {r["_district"]}')
        if r['_district'] == CITY and rt not in CITY_TYPES:
            err(w, f'the city layer {CITY} holds only main roads, rail, water and the land\'s height, not a {rt}')
        if rt == 'water' and r.get('kind') in WATER_AREA and ('rings' not in r or 'centreline' in r):
            err(w, f'a {r["kind"]} is an outline (rings) at one level, not a centreline')
        if rt == 'water' and r.get('kind') in WATER_LINE:
            c = r.get('centreline')
            if not isinstance(c, list) or 'rings' in r:
                err(w, f'a {r["kind"]} is a centreline with a width, not an outline')
            elif ('width' in r) == ('widths' in r):
                err(w, 'give the water one width, or widths (one per centreline point), not both or neither')
            elif 'widths' in r and len(r['widths']) != len(c):
                err(w, f'{len(r["widths"])} widths for {len(c)} centreline points')
        if r['_district'] == CITY and rt == 'road' and r.get('kind') not in CITY_ROADS:
            err(w, f'the city layer holds main roads ({", ".join(sorted(CITY_ROADS))}), not a {r.get("kind")!r}')

    ends = [(rid, p) for rid, r in recs.items() if r.get('type') == 'road' and isinstance(r.get('centreline'), list)
            for p in (r['centreline'][0], r['centreline'][-1]) if is_pt(p)]
    pts = [(rid, p) for rid, r in recs.items() if r.get('type') == 'road' and isinstance(r.get('centreline'), list)
           for p in r['centreline'] if is_pt(p)]
    for rid, e in ends:             # a road end that almost lands on another road: join it or pull it back
        for oid, q in pts:
            if oid != rid and JOIN[0] < math.hypot(e[0] - q[0], e[1] - q[1]) < JOIN[1]:
                err(f'{recs[rid]["_file"]} {rid}', f'its end {e} almost meets {oid} at {q}: join them on one point or pull it back')
    land(recs)
    on_road(recs)
    road_lines(recs)
    road_nodes(recs)
    return files, recs


def land(recs):
    """The city layer's relief grids are the land's height (DECISIONS "The land's own height too"): together they cover
    the whole frame at one spacing, and where two grids meet their shared points carry the same height, as an Unreal
    Landscape's components share their edge vertices. The city layer without its land fails too."""
    grids = [(rid, r) for rid, r in recs.items() if r['_district'] == CITY and r.get('type') == 'relief'
             and isinstance(r.get('z_mm'), list) and len(r['z_mm']) == r.get('cols', 0) * r.get('rows', 0)]
    if not grids:
        if any(r.get('type') == 'district' and r['_district'] == CITY for r in recs.values()):
            err(f'{CITY} relief', 'the city layer holds no land height: its relief grids are missing (scripts/draft_terrain.py drafted them once)')
        return
    cells = {r['cell'] for _, r in grids}
    if len(cells) != 1:
        return err(f'{CITY} relief', f'the land\'s grids should share one spacing, have {sorted(cells)}')
    c = cells.pop()
    import numpy as np
    nx, ny = round(FRAME[0] / c) + 1, round(FRAME[1] / c) + 1
    Z, who = np.full((ny, nx), np.nan), np.full((ny, nx), -1)
    clash, outside = [], 0
    for n, (rid, r) in enumerate(grids):
        i0, j0 = r['origin'][0] / c, r['origin'][1] / c
        if i0 != round(i0) or j0 != round(j0) or i0 < 0 or j0 < 0 or i0 + r['cols'] > nx or j0 + r['rows'] > ny:
            outside += 1
            continue
        i0, j0 = round(i0), round(j0)
        z = np.array(r['z_mm'], dtype=float).reshape(r['rows'], r['cols'])
        win, wwho = Z[j0:j0 + r['rows'], i0:i0 + r['cols']], who[j0:j0 + r['rows'], i0:i0 + r['cols']]
        bad = np.isfinite(win) & (win != z)
        if bad.any():
            j, i = np.argwhere(bad)[0]
            clash.append((rid, grids[wwho[j, i]][0], [float((i0 + i) * c), float((j0 + j) * c)], int(bad.sum())))
        new = ~np.isfinite(win)
        win[new], wwho[new] = z[new], n
    for rid, oid, pt, k in clash[:5]:
        err(f'{recs[rid]["_file"]} {rid}', f'{k} of its points differ from {oid}\'s, the first at {pt}: grids that meet share their edge heights')
    if len(clash) > 5:
        err(f'{CITY} relief', f'{len(clash) - 5} more grids differ from a neighbour on shared points')
    if outside:
        err(f'{CITY} relief', f'{outside} grids lie off the frame\'s {c} m spacing or outside it')
    missing = np.argwhere(~np.isfinite(Z))
    if len(missing):
        j, i = missing[0]
        err(f'{CITY} relief', f'the land leaves {len(missing)} points of the frame without a height, the first at {[float(i * c), float(j * c)]}')


def road_lines(recs):
    """Where the road kit (gidi-game tools/road_build.py, centre_at) can't lay a road along its line without folding its
    carriageway or drains: a point repeated, a line doubling back (a turn over 150 degrees), or a corner whose legs are too
    short to round it on a circle as wide as the road and its drains. The builder's own rule, read the same way: points
    turning under 2 degrees are dropped, each corner's tangent points held to 0.45 of each leg. A hand edit of the line."""
    for rid, r in recs.items():
        if r.get('type') != 'road' or not is_num(r.get('width')) or not isinstance(r.get('centreline'), list):
            continue
        w = f'{r["_file"]} {rid}'
        core = max([r['width'] / 2] + [g['offset'] + g.get('width', 0.5) / 2 + 0.15 for g in r.get('gutters') or []
                                       if is_num(g.get('offset'))])
        cl = [tuple(p[:2]) for p in r['centreline'] if is_pt(p)]
        L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(cl, cl[1:]))
        for k, f in (('gutters', 's0'), ('gutters', 's1'), ('verges', 's0'), ('verges', 's1'), ('crossings', 's')):
            for o in r.get(k) or []:   # a stretch placed past the road's end (its line cut shorter, its stretches not moved)
                if is_num(o.get(f)) and o[f] > L + 0.5:
                    err(w, f'a {k[:-1]} at {f} {o[f]} is past the road\'s end ({L:.1f} m along its line)')
        keep, s = [cl[0]], 0.0
        for a, b in zip(cl, cl[1:]):
            if math.hypot(b[0] - a[0], b[1] - a[1]) < 0.05:
                corners.append(f'{w}: a point repeated at {list(b)}')
        for a, b in zip(cl[1:], cl[2:]):
            q = keep[-1]
            if math.hypot(a[0] - q[0], a[1] - q[1]) < 0.05:
                continue
            h0, h1 = math.atan2(a[1] - q[1], a[0] - q[0]), math.atan2(b[1] - a[1], b[0] - a[0])
            if abs((h1 - h0 + math.pi) % (2 * math.pi) - math.pi) > math.radians(2):
                keep.append(a)
        keep.append(cl[-1])
        seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(keep, keep[1:])]
        for i in range(1, len(keep) - 1):
            s += seg[i - 1]
            a, b, c = keep[i - 1], keep[i], keep[i + 1]
            th = abs((math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi) % (2 * math.pi) - math.pi)
            if min(seg[i - 1], seg[i]) < 0.05 or th < 1e-3:
                continue
            if th > math.radians(150):
                corners.append(f'{w}: doubles back {math.degrees(th):.0f} degrees at {list(b)} (s {s:.1f})')
                continue
            R = min((core + 0.5) * math.tan(th / 2), 0.45 * seg[i - 1], 0.45 * seg[i]) / math.tan(th / 2)
            if R < core:
                corners.append(f'{w}: its {math.degrees(th):.0f} degree corner at {list(b)} (s {s:.1f}) has legs of '
                               f'{seg[i - 1]:.1f} and {seg[i]:.1f} m, too short to round {core:.1f} m out from the line')


def on_road(recs):
    """The road comes first (DECISIONS, 25 Oct): no house stands more than ON_ROAD m2 inside a road's real width."""
    try:
        from shapely.geometry import LineString, Polygon
        from shapely.strtree import STRtree
    except ImportError:
        return err('map', 'the on-road check needs shapely (run with ~/.venvs/gidi/bin/python)')
    hs = [(hid, Polygon(h['footprint'])) for hid, h in recs.items() if h.get('type') == 'building'
          and isinstance(h.get('footprint'), list) and len(h['footprint']) >= 3 and all(is_pt(p) for p in h['footprint'])]
    hs = [(hid, p) for hid, p in hs if p.is_valid]
    tree = STRtree([p for _, p in hs])
    for rid, r in recs.items():
        if r.get('type') != 'road' or not is_num(r.get('width')) or not isinstance(r.get('centreline'), list):
            continue
        cw = LineString([p[:2] for p in r['centreline'] if is_pt(p)]).buffer(r['width'] / 2, cap_style=2)
        for j in tree.query(cw):
            a = hs[j][1].intersection(cw).area
            if a > ON_ROAD:
                err(f'{recs[hs[j][0]]["_file"]} {hs[j][0]}', f'stands {a:.1f} m2 inside road {rid} ({r["width"]} m wide): '
                    'set the house back, cut its front or leave it out; never narrow the road')


RUN_NEAR, RUN_LONG = 1.0, 8.0   # m: two roads meeting at 15 degrees lie within 1 m of each other for about 8 m
DECK_OVER = 6.7   # m between road surfaces where one crosses over the other: 5.5 m clearance + a 1.2 m deck (OLD-MAP-LESSONS)
RAMP_MAX = 0.08   # a ramp's steepest grade: flyovers ramp at about 6.5% (OLD-MAP-LESSONS); 8% is a steep urban ramp


def road_z(cl, q):
    """A road's surface height at the point of its line nearest q: its points' z (MAP-FORMAT: an absolute height, for
    bridges and ramps) taken along the line, 0 where a point has none."""
    best = (float('inf'), 0.0)
    for a, b in zip(cl, cl[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t = max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / (dx * dx + dy * dy or 1)))
        d = math.hypot(a[0] + t * dx - q[0], a[1] + t * dy - q[1])
        za, zb = (a[2] if len(a) > 2 else 0.0), (b[2] if len(b) > 2 else 0.0)
        if d < best[0]:
            best = (d, za + t * (zb - za))
    return best[1]


def road_nodes(recs):
    """Where roads meet, they share a point (a node): the junction kit builds a junction at each shared point and nowhere
    else. Fails: two centrelines crossing without one, or a road end inside another road's carriageway with no node of
    that road near it (within its half width): a hand edit puts the point on both lines. An end on a node of its own a few
    metres from the other road's node (within its half width + 0.5 m) is a staggered junction, left as drawn and counted
    on a TODO line: the junction kit (not built yet) must join nodes that close into one junction (pulling them onto one
    point pushed 26 houses into the roads, 25 Oct). --strict fails on them. Also fails two roads drawn on top of each
    other: centrelines within RUN_NEAR of each other for more than RUN_LONG (a road record has no level, so in plan one
    road is the other drawn twice; the junction kit can't build it, 25 Oct). A hand edit cuts the copy back to where it
    joins. A road whose points carry z passes over another without a node (a bridge, as OpenStreetMap's layer and
    Overture's level_rules keep crossings on different levels unjoined) when their surfaces there are DECK_OVER apart;
    nearer than that and not joined, it fails as a deck too low to pass under. Also fails a ramp steeper than RAMP_MAX
    between two points."""
    try:
        from shapely.geometry import LineString, Point
        from shapely.strtree import STRtree
    except ImportError:
        return err('map', 'the road-node check needs shapely (run with ~/.venvs/gidi/bin/python)')
    rs = [(rid, r) for rid, r in recs.items() if r.get('type') == 'road' and is_num(r.get('width'))
          and isinstance(r.get('centreline'), list) and len([p for p in r['centreline'] if is_pt(p)]) >= 2]
    pts = {rid: [tuple(p[:2]) for p in r['centreline'] if is_pt(p)] for rid, r in rs}
    lines = [LineString(pts[rid]) for rid, _ in rs]
    pz = {rid: [tuple(p) for p in r['centreline'] if is_pt(p)] for rid, r in rs}
    over = lambda a, b, q: abs(road_z(pz[a], q) - road_z(pz[b], q)) >= DECK_OVER
    for rid, _ in rs:
        for a, b in zip(pz[rid], pz[rid][1:]):
            run, rise = math.hypot(b[0] - a[0], b[1] - a[1]), abs((b[2] if len(b) > 2 else 0) - (a[2] if len(a) > 2 else 0))
            if rise and rise > RAMP_MAX * run:
                err(f'{recs[rid]["_file"]} {rid}', f'climbs {rise:.2f} m in {run:.1f} m at {list(b)}, steeper than '
                    f'{RAMP_MAX:.0%}: lengthen the ramp')
    tree = STRtree(lines)
    node = {}
    for rid, _ in rs:
        for q in {(round(a[0], 1), round(a[1], 1)) for a in pts[rid]}:
            node[q] = node.get(q, 0) + 1
    near = lambda q, ps: any(math.hypot(q[0] - a[0], q[1] - a[1]) < 0.3 for a in ps)
    for k, (rid, r) in enumerate(rs):
        w = f'{r["_file"]} {rid}'
        for e in (pts[rid][0], pts[rid][-1]):
            for j in tree.query(Point(e).buffer(60)):
                oid, o = rs[j]
                if oid == rid or lines[j].distance(Point(e)) >= o['width'] / 2 or near(e, pts[oid]) or over(rid, oid, e):
                    continue
                if node.get((round(e[0], 1), round(e[1], 1)), 0) > 1 and \
                        min(math.hypot(e[0] - a[0], e[1] - a[1]) for a in pts[oid]) < o['width'] / 2 + 0.5:
                    staggered.append(f'{w}: its end at {list(e)} is a node {min(math.hypot(e[0] - a[0], e[1] - a[1]) for a in pts[oid]):.1f} m from '
                                     f'road {oid}\'s node, inside it: a staggered junction for the junction kit to join')
                    continue
                err(w, f'its end at {list(e)} is inside road {oid} with no node of it near (no junction)')
        for j in tree.query(lines[k].buffer(RUN_NEAR)):
            oid = rs[j][0]
            if oid <= rid:
                continue
            run = min(lines[k].intersection(lines[j].buffer(RUN_NEAR)).length, lines[j].intersection(lines[k].buffer(RUN_NEAR)).length)
            if run > RUN_LONG:
                err(w, f'runs on top of road {oid} for {run:.0f} m (centrelines within {RUN_NEAR} m): one is the other '
                       f'drawn twice; cut it back to where it joins')
            if not lines[k].crosses(lines[j]):
                continue
            x = lines[k].intersection(lines[j])
            for g in getattr(x, 'geoms', [x]):
                if g.geom_type == 'Point' and not (near((g.x, g.y), pts[rid]) and near((g.x, g.y), pts[oid])):
                    if over(rid, oid, (g.x, g.y)):
                        continue
                    dz = abs(road_z(pz[rid], (g.x, g.y)) - road_z(pz[oid], (g.x, g.y)))
                    err(w, f'crosses road {oid} at {[round(g.x, 2), round(g.y, 2)]} without a shared point (no node)'
                        + (f', {dz:.1f} m above it: a deck needs {DECK_OVER} m' if dz else ''))


# ------------------------------------------------------------------ what each kit part reads
def resolve(rt, path):
    """True if a dotted path (faces[].windows, roof.form) is a field of record type rt."""
    fields = dict(SCHEMA['common'], **SCHEMA['records'][rt]['fields'])
    for seg in path.split('.'):
        key = seg.rstrip('[]')
        if fields is None or key not in fields:
            return False
        spec = fields[key][0] if isinstance(fields[key], list) else fields[key]   # a table's column is [type]
        kind, _, _ = parse(spec)
        base, _, arg = kind.partition(':')
        if base == 'dict':                      # keyed by the data's own names: what lies under it is free
            return True
        if base == 'table':
            fields = dict({'cols': ['strs'], 'rows': ['list']}, **dict(SCHEMA['tables'][arg]))
        else:
            fields = SCHEMA['shapes'][arg] if base in ('obj', 'objs') else None
    return True


def check_kit(path):
    K = json.load(open(path))['parts']
    read = {}
    for part, p in K.items():
        rt = p.get('record')
        if rt not in SCHEMA['records']:
            err(f'kit {part}', f'reads record type {rt!r}, which the schema does not have')
            continue
        for f in p.get('reads', []):
            if not resolve(rt, f):
                err(f'kit {part}', f'reads {rt}.{f}, which the schema does not have: add the field to the map first')
            read.setdefault(rt, set()).add(f.split('.')[0].rstrip('[]'))
    for rt, spec in SCHEMA['records'].items():
        if not spec.get('kit'):
            continue
        if rt not in read:
            err(f'schema {rt}', 'drawn by the kit, but no part reads it')
            continue
        for f in spec['fields']:
            if f not in SCHEMA['not_drawn'] and f not in read[rt]:
                err(f'schema {rt}.{f}', 'no kit part reads it: a field the kit ignores is a gap in the interface')


def sizes(files):
    by = {}
    for d, n, p, doc in files:
        for r in doc.get('records', []):
            s = len(json.dumps({k: v for k, v in r.items() if not k.startswith('_')}, separators=(',', ':')))
            c = by.setdefault(r.get('type'), [0, 0])
            c[0] += 1
            c[1] += s
    print('%-14s %7s %10s %9s' % ('type', 'records', 'bytes', 'per rec'))
    for t, (c, s) in sorted(by.items(), key=lambda kv: -kv[1][1]):
        print('%-14s %7d %10d %9d' % (t, c, s, s // c))
    tot = sum(os.path.getsize(p) for _, _, p, _ in files)
    print('%-14s %7d %10d   (on disk, %d files)' % ('all', sum(c for c, _ in by.values()), tot, len(files)))


if __name__ == '__main__':
    args = sys.argv[1:]
    top = next((a for a in args if not a.startswith('--') and not a.endswith('.json')), os.path.join(ROOT, 'map'))
    if not os.path.isdir(top):
        sys.exit(f'No map at {top}')
    files, recs = check(top, fix='--fix' in args)
    if '--kit' in args:
        check_kit(args[args.index('--kit') + 1])
    if '--sizes' in args:
        sizes(files)
    # A field drawn but not given yet is still to fill (the board's amber), not a problem (its red): one count per
    # field, so the problems stay readable and PASS means none. --strict fails on them too (a district called finished).
    todo = [e for e in errors if TODO.search(e)]
    bad = errors if '--strict' in args else [e for e in errors if not TODO.search(e)]
    if '--strict' in args:
        bad = bad + corners + staggered
    for e in bad:
        print('FAIL ', e)
    if corners and '--strict' not in args:
        for e in corners:
            print('ROAD ', e)
        print('TODO  %d road corners to hand-edit (the road kit would fold them)' % len(corners))
    if staggered and '--strict' not in args:
        for e in staggered:
            print('NODE ', e)
        print('TODO  %d staggered junctions for the junction kit to join (nodes within reach of each other)' % len(staggered))
    if todo and '--strict' not in args:
        by = {}
        for e in todo:
            f = TODO.search(e).group(1)
            by[f] = by.get(f, 0) + 1
        print('TODO  %d fields still to fill: %s' % (len(todo), ', '.join('%s %d' % kv for kv in sorted(by.items(), key=lambda kv: -kv[1]))))
    print('%s  %d records in %d files, %d problems' % ('PASS' if not bad else 'FAIL', len(recs), len(files), len(bad)))
    sys.exit(1 if bad else 0)
