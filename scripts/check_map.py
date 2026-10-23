"""The new map's checker (docs/MAP-FORMAT.md; owner, 22 Oct 2026: "one ground truth"). Nothing in the map is guessed: a
record with an unknown field, a missing field, a wrong type, a broken link or a real name fails here, before the board,
the kit or the Unreal import ever reads it.

  python3 scripts/check_map.py <map dir>                      check every district under it (map/ by default)
  python3 scripts/check_map.py <map dir> --kit schema/kit_reads.json   also check what each kit part reads
  python3 scripts/check_map.py <map dir> --sizes              bytes and counts per record type
  python3 scripts/check_map.py <map dir> --fix                rewrite each file in the canonical layout (one record a line)

A map dir holds one folder per district: district.json, plan.json and dress/<tx>_<ty>.json (100 m tiles). The schema is
schema/map_schema.json. Exits 1 on any failure.
"""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(open(os.path.join(ROOT, 'schema', 'map_schema.json')))
TILE = 100.0                 # dress tiles, m
JOIN = (0.01, 1.0)           # two road ends closer than 1 m but not on the same point: a slip, not a junction
HEADER = {'format', 'district', 'layer', 'tile', 'records'}
ID_RE = re.compile(r'^[a-z]{1,2}-[a-z0-9]{8}$')

errors = []


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


def check(top, fix=False, only=None):
    """Check the map under top (only: a list of district folders to check, as the board does on each save)."""
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

    ends = [(rid, p) for rid, r in recs.items() if r.get('type') == 'road' and isinstance(r.get('centreline'), list)
            for p in (r['centreline'][0], r['centreline'][-1]) if is_pt(p)]
    pts = [(rid, p) for rid, r in recs.items() if r.get('type') == 'road' and isinstance(r.get('centreline'), list)
           for p in r['centreline'] if is_pt(p)]
    for rid, e in ends:             # a road end that almost lands on another road: join it or pull it back
        for oid, q in pts:
            if oid != rid and JOIN[0] < math.hypot(e[0] - q[0], e[1] - q[1]) < JOIN[1]:
                err(f'{recs[rid]["_file"]} {rid}', f'its end {e} almost meets {oid} at {q}: join them on one point or pull it back')
    return files, recs


# ------------------------------------------------------------------ what each kit part reads
def resolve(rt, path):
    """True if a dotted path (faces[].windows, roof.form) is a field of record type rt."""
    fields = dict(SCHEMA['common'], **SCHEMA['records'][rt]['fields'])
    for seg in path.split('.'):
        key = seg.rstrip('[]')
        if fields is None or key not in fields:
            return False
        kind, _, _ = parse(fields[key])
        base, _, arg = kind.partition(':')
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
    for e in errors:
        print('FAIL ', e)
    print('%s  %d records in %d files, %d problems' % ('PASS' if not errors else 'FAIL', len(recs), len(files), len(errors)))
    sys.exit(1 if errors else 0)
