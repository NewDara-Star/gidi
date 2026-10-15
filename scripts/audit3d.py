"""3D audit: does a district's map make a proper city when the kit builds it?

    .venv/bin/python scripts/audit3d.py [<district id> ...]     (all built districts if none)

The 3D view is the test of the 2D map: anything that looks wrong in 3D is a map problem or a gap in
the kit. This finds both, per district, and writes docs/audit/<id>.md plus docs/audit/README.md
(a table of every district). It complements scripts/check_district.py, which checks buildings,
overlaps, gateways and reach; this checks how the roads meet, what crosses water, and whether every
thing in the data has a model.

Map problems (fix them in the generator, then rebuild):
  R1 roads running along each other   two roads overlapping lengthwise (not a junction)
  R2 near misses                      a road ending 0.5-8 m short of another road
  R3 overshoots                       a road running 1-10 m past the road it meets
  R4 knife-edge crossings             two roads crossing at under 25 degrees (they look broken)
  D  duplicated roads                 the same road listed twice (an edge road in both its districts);
                                      the kit builds it once, but the data should hold it once
  R5 roads on water                   a road over the lagoon, sea or a canal with no bridge or deck
  R6 decks with no road               a flyover or bridge that no road runs along

Model gaps (make kits for them; see docs/LAGOS-LOOK.md):
  M1 building kinds                   data kinds with no builder in the kit
  M2 parcel kinds                     parcels the kit can't dress
  M3 civic plots                      named plots and what the kit makes of them
  M4 places on the map                every point (market, station, landmark...) and what stands there
"""
import glob
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
WIDTH = {'main': 14.0, 'street': 7.0, 'lane': 3.5, 'path': 2.5, 'exp': 30.0, 'art': 18.0, 'bridge': 22.0}  # blender/city.py


def load_city():
    s = open(os.path.join(ROOT, 'web', 'gidi-data.js')).read()
    return json.loads(s[s.index('{'):s.rindex('}') + 1])


def poly(ring):
    p = Polygon(ring)
    return p if p.is_valid else p.buffer(0)


def kit_registry():
    """What the kit can build, read from its source (it needs Blender to import)."""
    reg = open(os.path.join(ROOT, 'blender', 'gidi_kit', 'registry.py')).read()
    def keys(name):
        m = re.search(name + r'\s*=\s*\{(.*?)\n\}', reg, re.S)
        return set(re.findall(r"'([^']+)'\s*:", m.group(1))) if m else set()
    parcels = open(os.path.join(ROOT, 'blender', 'gidi_kit', 'parcels.py')).read()
    m = re.search(r'BUILDERS\s*=\s*\{(.*?)\n\}', parcels, re.S)
    pk = set(re.findall(r"'([^']+)'\s*:", m.group(1))) if m else set()
    lm = os.path.join(ROOT, 'blender', 'gidi_kit', 'landmarks.py')
    named = set()
    if os.path.exists(lm):
        m = re.search(r'BY_NAME\s*=\s*\{(.*?)\n\}', open(lm).read(), re.S)
        named = set(re.findall(r"'([^']+)'\s*:", m.group(1))) if m else set()
    return dict(buildings=keys('BUILDINGS'), civic=keys('CIVIC_PLOTS'), pois=keys('POI_PLACES'), parcels=pk, named=named)


def roads_of(G):
    """Every road centreline as (kind, width, district, name, LineString, id)."""
    out = []
    for kind, key in (('street', 'streets'), ('lane', 'lanes'), ('path', 'paths')):
        for d, lst in (G.get(key) or {}).items():
            for i, pts in enumerate(lst):
                if len(pts) >= 2:
                    out.append(dict(k=kind, w=WIDTH[kind], d=d, name=None, g=LineString(pts), id=f'{d}/{kind}/{i}'))
    for i, m in enumerate(G.get('mains', [])):
        out.append(dict(k='main', w=WIDTH['main'], d=m.get('d'), name=m.get('name'), g=LineString(m['pts']), id=f'main/{i}'))
    for i, a in enumerate(G.get('arterials', [])):
        out.append(dict(k=a['cls'], w=WIDTH.get(a['cls'], 18.0), d=None, name=a['name'], g=LineString(a['pts']), id=f'art/{i}'))
    return out


def fmt(p):
    return f'({p.x:.0f}, {p.y:.0f})'


def audit(G, did, ring, roads, tree, decks, wet, reg, built_kinds):
    here = [r for r in roads if r['g'].intersects(ring)]
    issues = defaultdict(list)
    real = [r for r in here if r['k'] != 'path']  # paths may run anywhere
    # R1 running along each other
    seen = set()
    for r in real:
        for j in tree.query(r['g'].buffer(r['w'] / 2)):
            o = roads[j]
            if o is r or o['k'] == 'path' or (o['id'], r['id']) in seen or o['k'] == 'bridge' or r['k'] == 'bridge':
                continue
            seen.add((r['id'], o['id']))
            if r['g'].equals_exact(o['g'], 0.5) or r['g'].equals_exact(LineString(o['g'].coords[::-1]), 0.5):
                issues['D'].append((r['g'].length, f"{r['k']} {r['name'] or r['id']} is listed twice ({r['id']}, {o['id']})"))
                continue
            along = r['g'].intersection(o['g'].buffer((o['w'] + r['w']) / 2 * 0.7)).length
            if along > max(o['w'], r['w']) * 1.6 + 6 and ring.contains(r['g'].interpolate(0.5, normalized=True)):
                ov = r['g'].intersection(o['g'].buffer((o['w'] + r['w']) / 2 * 0.7))
                issues['R1'].append((along, f"{r['k']} {r['id']} runs {along:.0f} m along {o['k']} {o['name'] or o['id']} at {fmt(ov.representative_point())}"))
    # R2 near misses and R3 overshoots, at each free road end
    ends = defaultdict(int)
    for r in real:
        for p in (r['g'].coords[0], r['g'].coords[-1]):
            ends[(round(p[0], 1), round(p[1], 1))] += 1
    for r in real:
        cs = list(r['g'].coords)
        for p, q in ((cs[0], cs[1]), (cs[-1], cs[-2])):
            P = Point(p)
            if not ring.contains(P) or ends[(round(p[0], 1), round(p[1], 1))] > 1:
                continue
            touching = False
            for j in tree.query(P.buffer(12)):
                o = roads[j]
                if o is r or o['k'] == 'path':
                    continue
                d = o['g'].distance(P)
                if d < 0.5:
                    touching = True
                    break
            if touching:
                continue
            for j in tree.query(P.buffer(12)):
                o = roads[j]
                if o is r or o['k'] in ('path', 'bridge'):
                    continue
                d = o['g'].distance(P)
                tail = LineString([p, q])
                if tail.intersects(o['g']) and 1.0 < d < 10 + o['w'] / 2:
                    issues['R3'].append((d, f"{r['k']} {r['id']} runs {d:.1f} m past {o['k']} {o['name'] or o['id']} at {fmt(P)}"))
                    break
                if 0.5 < d < 8 + o['w'] / 2 and not tail.intersects(o['g']):
                    issues['R2'].append((d, f"{r['k']} {r['id']} stops {d:.1f} m short of {o['k']} {o['name'] or o['id']} at {fmt(P)}"))
                    break
    # R4 knife-edge crossings: two roads crossing at under 25 degrees
    seen = set()
    for r in real:
        for j in tree.query(r['g']):
            o = roads[j]
            if o is r or o['k'] == 'path' or (o['id'], r['id']) in seen:
                continue
            seen.add((r['id'], o['id']))
            if r['g'].equals_exact(o['g'], 0.5):
                continue
            x = r['g'].intersection(o['g'])
            pts = [x] if x.geom_type == 'Point' else [g for g in getattr(x, 'geoms', []) if g.geom_type == 'Point']
            for c in pts:
                if not ring.contains(c) or any(dk.distance(c) < 3 for dk in decks):
                    continue
                if any(Point(e).distance(c) < 1.0 for g in (r['g'], o['g']) for e in (g.coords[0], g.coords[-1])):
                    continue  # one road ends here: a junction or a continuation, not a crossing
                def heading(g):
                    s0 = g.project(c)
                    a, b = g.interpolate(max(0, s0 - 3)), g.interpolate(min(g.length, s0 + 3))
                    return math.atan2(b.y - a.y, b.x - a.x)
                ang = abs((heading(r['g']) - heading(o['g']) + math.pi / 2) % math.pi - math.pi / 2)
                if math.degrees(ang) < 25:
                    issues['R4'].append((25 - math.degrees(ang), f"{r['k']} {r['id']} crosses {o['k']} {o['name'] or o['id']} at {math.degrees(ang):.0f} degrees at {fmt(c)}"))
    # R5 roads on water
    for r in here:
        if r['k'] in ('bridge',):
            continue
        on = r['g'].intersection(wet)
        if on.is_empty:
            continue
        for dk in decks:
            on = on.difference(dk.buffer(r['w'] / 2 + 2))
        if on.length > 3:
            issues['R5'].append((on.length, f"{r['k']} {r['name'] or r['id']} has {on.length:.0f} m on water with no bridge, from {fmt(on.representative_point())}"))
    # R6 decks with no road along them
    for s in G.get('structures', []):
        if s['d'] != did or s['kind'] not in ('flyover', 'ramp'):
            continue
        g = LineString(s['pts'])
        carried = max((g.intersection(o['g'].buffer(3)).length for o in roads if o['g'].distance(g) < 3), default=0)
        if carried < g.length * 0.8:
            issues['R6'].append((g.length, f"{s['kind']} {s['name']} ({g.length:.0f} m): only {carried:.0f} m has a road along it"))

    # model coverage
    kinds = Counter(b[0] for b in (G['buildings'].get(did) or []))
    m1 = [(n, k) for k, n in kinds.items() if k not in reg['buildings']]
    pk = Counter(p['kind'] for p in (G['parcels'].get(did) or []))
    m2 = [(n, k) for k, n in pk.items() if k not in reg['parcels']]
    m3 = []
    for c in G.get('safe_ground', []):
        if c['d'] != did:
            continue
        if c['type'] not in reg['civic']:
            m3.append(f"{c['name']} ({c['type']}): no builder, the plot stays bare")
        elif c['type'] == 'landmark' and c['name'] not in reg['named']:
            m3.append(f"{c['name']} (landmark): built as a plain hall until blender/gidi_kit/landmarks.py gives it a model of its own")
    # M4: what stands at each place on the map. A place is modelled when its own kind of building is
    # there, or a parcel or deck holds it; a place on an ordinary house (or nothing) has nothing of its own.
    m4 = defaultdict(list)
    parcels_here = [(p['kind'], poly(p['pts'])) for p in (G['parcels'].get(did) or [])]
    blds = [(b[0], poly(b[1:])) for b in (G['buildings'].get(did) or []) if len(b) > 3]
    structs = [(st['kind'], LineString(st['pts'])) for st in G.get('structures', [])] + [('jetty', LineString(b)) for b in G.get('boardwalks', [])] + [('canal', LineString(c['pts'])) for c in G.get('canals', [])]
    civic = [(c['type'], poly(c['pts'][:-1])) for c in G.get('safe_ground', []) if c['d'] == did]
    PLAIN = ('front', 'back', 'shed')
    for p in G['pois']:
        if p['d'] != did:
            continue
        t, P = p['type'], Point(p['x'], p['y'])
        if p['name'] in reg['named'] or t in reg['pois'] or t == 'cemetery':
            continue  # its own model, or it takes over the nearest plot
        if any(g.distance(P) < 25 for _, g in parcels_here) or any(g.distance(P) < 25 for _, g in structs) or any(g.distance(P) < 60 for _, g in civic):
            continue
        near = sorted((g.distance(P), k) for k, g in blds)
        if near and near[0][0] < 15 and (near[0][1] not in PLAIN or t == 'story'):
            continue  # its own kind of building stands there (or, for a story place, the house it is)
        on = f"on a {near[0][1]} house" if near and near[0][0] < 2 else 'on bare ground'
        m4[t].append(f"{p['name']} ({on}, {fmt(P)})")
    return issues, dict(M1=m1, M2=m2, M3=m3, M4=m4), kinds


def main():
    G = load_city()
    reg = kit_registry()
    roads = roads_of(G)
    tree = STRtree([r['g'] for r in roads])
    decks = [LineString(s['pts']).buffer(s.get('width', 8) / 2) for s in G.get('structures', []) if s['kind'] in ('flyover', 'ramp', 'footbridge', 'skywalk', 'jetty', 'approach', 'culvert')]
    decks += [LineString(a['pts']).buffer(WIDTH['bridge'] / 2) for a in G.get('arterials', []) if a['cls'] == 'bridge']
    decks += [LineString(b).buffer(1.5) for b in G.get('boardwalks', [])]
    wet = unary_union([poly(w) for w in G['water'] + G['ocean']] + [LineString(c['pts']).buffer(c.get('width', 4.0) / 2) for c in G.get('canals', [])])
    built_kinds = set()
    for f in glob.glob(os.path.join(ROOT, 'web', 'city', 'web', 'tiles', '*.json')):
        built_kinds |= set(json.load(open(f)).get('built', {}))
    want = sys.argv[1:] or [d['id'] for d in G['districts'] if d['id'] in G['buildings']]
    out = os.path.join(ROOT, 'docs', 'audit')
    os.makedirs(out, exist_ok=True)
    rows = []
    for d in G['districts']:
        if d['id'] not in want:
            continue
        ring = poly(d['poly'][0])
        issues, gaps, kinds = audit(G, d['id'], ring, roads, tree, decks, wet, reg, built_kinds)
        R = {k: sorted({t[1]: t for t in v}.values(), key=lambda t: -t[0]) for k, v in issues.items()}
        nm4 = sum(len(v) for v in gaps['M4'].values())
        rows.append((d['name'], d['id'], *(len(R.get(k, [])) for k in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'D')), len(gaps['M1']), len(gaps['M2']), len(gaps['M3']), nm4))
        L = [f"# 3D audit: {d['name']}", '', f"`.venv/bin/python scripts/audit3d.py {d['id']}` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).", '']
        names = {'R1': 'Roads running along each other', 'R2': 'Near misses (ends short of a road)', 'R3': 'Overshoots (ends past a road)', 'R4': 'Knife-edge crossings (under 25 degrees)',
                 'R5': 'Roads on water with no bridge', 'R6': 'Decks with no road', 'D': 'Roads listed twice'}
        L.append('## Map problems')
        for k, t in names.items():
            v = R.get(k, [])
            L.append(f'- **{k} {t}: {len(v)}**')
            for _, s in v[:12]:
                L.append(f'  - {s}')
            if len(v) > 12:
                L.append(f'  - and {len(v) - 12} more')
        L += ['', '## Model gaps']
        L.append(f"- **M1 building kinds with no builder: {len(gaps['M1'])}**" + ''.join(f'\n  - {k} ({n})' for n, k in gaps['M1']))
        L.append(f"- **M2 parcel kinds with no builder: {len(gaps['M2'])}**" + ''.join(f'\n  - {k} ({n})' for n, k in gaps['M2']))
        L.append(f"- **M3 civic plots: {len(gaps['M3'])}**" + ''.join(f'\n  - {s}' for s in gaps['M3']))
        L.append(f"- **M4 places on the map with nothing of their own: {nm4}** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)")
        for t, v in sorted(gaps['M4'].items()):
            L.append(f'  - {t} ({len(v)}): ' + ', '.join(v[:10]) + (f' and {len(v) - 10} more' if len(v) > 10 else ''))
        L += ['', '## Building kinds here', ', '.join(f'{k} {n}' for k, n in kinds.most_common())]
        open(os.path.join(out, f"{d['id']}.md"), 'w').write('\n'.join(L) + '\n')
        print(f"{d['id']:10s} R1 {rows[-1][2]:3d}  R2 {rows[-1][3]:3d}  R3 {rows[-1][4]:3d}  R4 {rows[-1][5]:3d}  R5 {rows[-1][6]:3d}  R6 {rows[-1][7]:2d}  D {rows[-1][8]:2d} | M1 {rows[-1][9]} M2 {rows[-1][10]} M3 {rows[-1][11]} M4 {rows[-1][12]}", flush=True)
    if not sys.argv[1:]:
        T = ['# 3D audit, all districts', '', 'Each district has its own page here with the details. Rerun with `.venv/bin/python scripts/audit3d.py`.', '',
             'R1 along each other, R2 near misses, R3 overshoots, R4 knife-edge crossings, R5 roads on water, R6 decks with no road, D roads listed twice; M1 building kinds, M2 parcel kinds, M3 civic plots, M4 places with nothing of their own.', '',
             '| District | R1 | R2 | R3 | R4 | R5 | R6 | D | M1 | M2 | M3 | M4 |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
        for r in rows:
            T.append(f'| [{r[0]}]({r[1]}.md) | ' + ' | '.join(str(x) for x in r[2:]) + ' |')
        open(os.path.join(out, 'README.md'), 'w').write('\n'.join(T) + '\n')


if __name__ == '__main__':
    main()
