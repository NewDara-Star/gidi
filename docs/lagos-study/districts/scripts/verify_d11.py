"""Re-check the data claims of docs/lagos-study/districts/d11.md (the d11 Costa scout note, 27 Oct).

Prints one line per claim: id | what the note states | what the data gives | verdict.
Verdicts: TRUE (within the stated rounding), FALSE (to correct), SEE (printed for a reading by eye).

  ~/.venvs/gidi/bin/python -I verify_d11.py

Reads only: ~/gidi/web/frame-study.js, ~/gidi/map/*/ records, ~/gidi/docs/lagos-study/... files, and the Overture
extract under ~/gidi-data/research/data/overture-lagos/. Writes nothing.
"""
import csv
import json
import os
import re

import pyarrow.parquet as pq
import shapely
from pyproj import Transformer
from shapely.geometry import LineString, MultiPolygon, Point, Polygon, shape
from shapely.ops import unary_union, transform as shp_transform

ROOT = os.path.expanduser('~/gidi')
OV = os.path.expanduser('~/gidi-data/research/data/overture-lagos')
T = Transformer.from_crs(4326, 32631, always_xy=True)
TI = Transformer.from_crs(32631, 4326, always_xy=True)


def gidi(lon, lat):
    """working_bar.py's gidi(): real WGS84 to Gidi metres (UTM 31N, 1:3 from the frame's south-west corner)."""
    u, v = T.transform(lon, lat)
    return (u - 500525) / 3, 10500 - (v - 707825) / 3


def real(x, y):
    return TI.transform(x * 3 + 500525, (10500 - y) * 3 + 707825)


def say(cid, stated, found, ok=None):
    v = 'SEE' if ok is None else ('TRUE' if ok else 'FALSE')
    print(f'{cid:8} | stated: {stated} | found: {found} | {v}')


def near(a, b, tol):
    return abs(a - b) <= tol


# ---------------------------------------------------------------- frame study
s = open(os.path.join(ROOT, 'web/frame-study.js')).read()
F = json.loads(s[s.index('{'):s.rstrip().rstrip(';').rindex('}') + 1])
FD = {d['n']: d for d in F['districts']}


def fring(n):
    return MultiPolygon([Polygon(r[0], r[1:]) for r in FD[n]['rings']]).buffer(0)


R = fring(11)
ring_pts = FD[11]['rings'][0][0]
print('== section 0/1: the frame ring')
say('S0.oyb', 'Oyingbo Red Line station (6.4834, 3.3815) -> 13886, 7556', '%.0f, %.0f' % gidi(3.3815, 6.4834),
    near(gidi(3.3815, 6.4834)[0], 13886, 1) and near(gidi(3.3815, 6.4834)[1], 7556, 1))
closed = ring_pts[0] == ring_pts[-1]
say('S1.pts', 'one polygon, 87 points', f'{len(FD[11]["rings"])} ring(s), {len(ring_pts)} points (closed={closed}, '
    f'{len(ring_pts) - closed} distinct)', len(FD[11]['rings']) == 1 and len(ring_pts) == 87)
say('S1.area', '0.665 km2 game, 5.98 km2 real', f'{R.area / 1e6:.3f} km2 game, {R.area * 9 / 1e6:.2f} km2 real',
    near(R.area / 1e6, 0.665, 0.0006) and near(R.area * 9 / 1e6, 5.98, 0.006))
b = R.bounds
say('S1.bbox', 'x 12725-13808, y 6675-8242', 'x %.0f-%.0f, y %.0f-%.0f' % (b[0], b[2], b[1], b[3]),
    near(b[0], 12725, 1) and near(b[2], 13808, 1) and near(b[1], 6675, 1) and near(b[3], 8242, 1))
say('S5.ring', 'ring perimeter 5,799 m', f'{R.length:.0f} m', near(R.length, 5799, 1))

# ---------------------------------------------------------------- docs
print('== docs read by the note')
liv = open(os.path.join(ROOT, 'docs/lagos-study/LIVING.md')).read()
row = re.search(r'^\| 11 \| Ijora-Iganmu-Costain \|.*$', liv, re.M).group(0)
say('L1.liv', '6.0 km2, ~100,600 people, 16,800/km2, 6,700 bldgs, mean 203 m2, 37.2% big roofs, 44 : 0', row, None)
for n, v in ((16, '8.4'), (13, '8.9'), (12, '2.4')):
    r = re.search(r'^\| %d \|.*$' % n, liv, re.M).group(0).split('|')
    say(f'L6.liv{n}', f'big roofs {v}%', r[8].strip(), r[8].strip() == v)
say('L1.cls', 'class D "poor and packed" for Ijora-Badia', 'yes' if re.search(r'D, poor and packed:.*Ijora-Badia \(11\)', liv)
    else 'no', bool(re.search(r'D, poor and packed:.*Ijora-Badia \(11\)', liv)))
say('L5.vil', '"the residents are never the villains" [LIV]', 'yes' if 'the residents are never the villains' in liv else 'no',
    'the residents are never the villains' in liv)
names = open(os.path.join(ROOT, 'docs/lagos-study/roads/NAMES.md')).read()
q = 'Cos-tain to Cos-ta (the old Gidi Costa Circle, after the Costain roundabout)'
say('N1.name', q, 'found in NAMES.md row 11' if q in names else 'not found', q in names)
ec = open(os.path.join(ROOT, 'docs/lagos-study/roads/EARTH-CHECK.md')).read().split('\n')
say('E1.ec221', 'members Ijora, Ijora Badia (both), Iganmu, Costain, Iponri; borders railway, Eko Bridge approach, Western Avenue',
    ec[220], 'Ijora, Ijora Badia (both), Iganmu, Costain, Iponri | Railway, Eko Bridge approach and Western Avenue' in ec[220])
r8 = [l for l in ec if l.startswith('| 8 | Apapa')][0]
say('E1.row8', 'EC row 8: "Ijora Badia north with Ijora"', re.search(r'Ijora Badia[^|]*', r8).group(0),
    'Ijora Badia north with Ijora' in r8)
st = open(os.path.join(ROOT, 'docs/lagos-study/STUDY.md')).read()
say('ST.knot', '"knot to the bridges" [ST]', 'yes' if 'knot to the bridges' in st else 'no', 'knot to the bridges' in st)
say('ST.iga', 'Iganmu-Ijora 2.4 km2 industrial piece; Ijora-Otto 1.2 km2 port',
    'Iganmu-Ijora**: 2.4 / Ijora-Otto 1.2' if ('**Iganmu-Ijora**: 2.4 km²' in st and 'Ijora-Otto 1.2 km²' in st) else 'no',
    '**Iganmu-Ijora**: 2.4 km²' in st and 'Ijora-Otto 1.2 km²' in st)
lga = open(os.path.join(ROOT, 'docs/lagos-lgas-research.md')).read()
for cid, pat in (('G.4lane', 'four-lane dual carriageway at Ijora'), ('G.tank', 'October 2023: a tanker rolled back'),
                 ('G.9veh', 'about nine vehicles'), ('G.ojora', 'carried out the 2015 Badia demolitions'),
                 ('G.zinc', 'replaced by zinc, tarpaulin and tent shelters'),
                 ('G.50s', '**[unverified]** The housing is mostly 1950s'), ('G.edge', 'Iganmu, Iponri, Coker:** the industrial edge'),
                 ('G.costain', 'Costain roundabout')):
    hay = lga if cid != 'G.costain' else liv
    say(cid, pat, 'found' if pat in hay else 'not found', pat in hay)
d13s = open(os.path.join(ROOT, 'map/d13/STREETS.md')).read()
say('M.d13w', 'd13 read the two carriageways ~14 m apart (real) and drew 25 m', 'yes' if 'about 14 m real' in d13s and
    '| rd-32d33ffa | Western Avenue | motorway | 25 |' in d13s else 'no',
    'about 14 m real' in d13s and '| rd-32d33ffa | Western Avenue | motorway | 25 |' in d13s)
d12s = open(os.path.join(ROOT, 'map/d12/STREETS.md')).read()
say('M.d12ap', 'five short Apapa Road pieces on its east border left to d11', 'yes' if '5 short Apapa Road pieces on the east border are left to'
    in d12s.replace('\n', ' ').replace('  ', ' ') else 'no',
    '5 short Apapa Road pieces on the east border are left to' in d12s.replace('\n', ' ').replace('  ', ' '))

# ---------------------------------------------------------------- map records
print('== drawn neighbours (map/)')
REC = {}
for d in sorted(os.listdir(os.path.join(ROOT, 'map'))):
    p = os.path.join(ROOT, 'map', d)
    if not os.path.isdir(p):
        continue
    recs = []
    for f in sorted(os.listdir(p)):
        if f.endswith('.json'):
            recs += json.load(open(os.path.join(p, f)))['records']
    REC[d] = recs
ROADS = {r['id']: (d, r) for d, rs in REC.items() for r in rs if r['type'] == 'road'}
NAME = {}   # road records carry no name; the districts' STREETS.md tables do
for d in REC:
    f = os.path.join(ROOT, 'map', d, 'STREETS.md')
    if os.path.exists(f):
        for m in re.finditer(r'^\| (rd-[0-9a-z]+) \| ([^|]+?) \|', open(f).read(), re.M):
            NAME[m.group(1)] = m.group(2)
for rid, (d, r) in ROADS.items():
    r['name'] = NAME.get(rid, '(not in STREETS.md)')
OUT = {d: MultiPolygon([Polygon(o) for o in next(r for r in rs if r['type'] == 'district')['outline']]).buffer(0)
       for d, rs in REC.items()}
ov = {d: R.intersection(o).area for d, o in OUT.items()}
say('S2.over', '0 m2 overlap with each of the 11 drawn districts', f'{len(OUT)} drawn; max overlap {max(ov.values()):.1f} m2',
    len(OUT) == 11 and max(ov.values()) < 1)

rset = {tuple(map(float, p)) for p in ring_pts}
bnd = R.boundary


def shared(n=None, outline=None):
    if n is not None:
        pts = {tuple(map(float, p)) for r in FD[n]['rings'] for ring in r for p in ring}
        poly = fring(n)
    else:
        pts = {tuple(map(float, p)) for o in outline for p in o}
        poly = MultiPolygon([Polygon(o) for o in outline]).buffer(0)
    k = len(rset & pts)
    L = bnd.intersection(poly.buffer(0.5)).length
    return k, L


for n, (pts_s, len_s), drawn in ((16, (21, 1417), 'd16'), (13, (14, 1608), 'd13'), (17, (18, 756), 'd17'),
                                  (12, (14, 1078), 'd12'), (10, (14, 605), None)):
    k, L = shared(n)
    say(f'S2.d{n}', f'{pts_s} shared points, {len_s} m (frame)', f'{k} points, {L:.0f} m', k == pts_s and near(L, len_s, 3))
    if drawn:
        o = next(r for r in REC[drawn] if r['type'] == 'district')['outline']
        k2, L2 = shared(outline=o)
        say(f'S2.m{n}', 'drawn outline gives the same counts', f'{k2} points, {L2:.0f} m', k2 == pts_s)
allfr = unary_union([fring(n) for n in FD if n != 11])
free = bnd.difference(allfr.buffer(0.5)).length
say('S2.free', 'about 336 m of the ring touches no district', f'{free:.0f} m', near(free, 336, 10))


def within2(d):
    return sum(1 for r in REC[d] if r['type'] == 'road' and LineString(r['centreline']).distance(bnd) <= 2)


for d, n in (('d16', 18), ('d13', 24), ('d17', 17), ('d12', 19)):
    say(f'S2.{d}w2', f'{n} {d} roads within 2 m of the line', within2(d), within2(d) == n)


def rinfo(rid):
    d, r = ROADS[rid]
    L = LineString(r['centreline'])
    a, z = r['centreline'][0], r['centreline'][-1]
    return d, r, L, a, z


for rid, st_ in (('rd-87778241', 'Ijora Causeway 170 m, ends on border x13725-13760 y8053-8074'),
                 ('rd-d6e90d7a', 'Ijora Causeway 42 m, ends on border'), ('rd-e1ee4c5e', 'unnamed, ends on border')):
    d, r, L, a, z = rinfo(rid)
    e = min((a, z), key=lambda p: Point(p).distance(bnd))
    say('S2.' + rid[3:], st_, f'{d} {r.get("name", "(unnamed)")} {L.length:.0f} m, nearer end ({e[0]:.0f}, {e[1]:.0f}) '
        f'{Point(e).distance(bnd):.1f} m from the ring', Point(e).distance(bnd) < 2 and 13720 <= e[0] <= 13765 and 8050 <= e[1] <= 8078)
d, r, L, a, z = rinfo('rd-32d33ffa')
say('S2.wave', 'rd-32d33ffa 25 m motorway, ends at (13241.36, 7384.58)', f'{r["kind"]} {r["width"]} m; ends {a}, {z}',
    r['kind'] == 'motorway' and r['width'] == 25 and [13241.36, 7384.58] in (a, z))
say('S2.wav69', '69 m of rd-32d33ffa over d11\'s side', f'{L.intersection(R).length:.0f} m', near(L.intersection(R).length, 69, 2))
d, r, L, a, z = rinfo('rd-1d8a6faf')
e = max((a, z), key=lambda p: R.contains(Point(p)))
say('S2.bode', 'Bode Thomas rd-1d8a6faf ends 3.8 m inside d11', f'{r.get("name")}; end {e} inside={R.contains(Point(e))}, '
    f'{Point(e).distance(bnd):.1f} m from the line', R.contains(Point(e)) and near(Point(e).distance(bnd), 3.8, 0.05))
d, r, L, a, z = rinfo('rd-9e64ec60')
say('S2.mmw', 'Saba MMW rd-9e64ec60 ends on d11\'s north tip at (13563, 6679)', f'{r.get("name")}; ends {a}, {z}',
    any(near(p[0], 13563, 1) and near(p[1], 6679, 1) for p in (a, z)))
for rid in ('rd-7ba7820e', 'rd-25f7e40e', 'rd-30285fb8', 'rd-0f64a3d8'):
    d, r, L, a, z = rinfo(rid)
    say('S2.' + rid[3:], 'Saba MMW piece on the border, 0 m inside d11', f'{d} {r.get("name")} {L.intersection(R).length:.1f} m '
        f'inside, max dist to line {max(Point(p).distance(bnd) for p in r["centreline"]):.1f} m', L.intersection(R).length < 1)
d, r, L, a, z = rinfo('rd-d8784e5c')
dd = min(Point(a).distance(bnd), Point(z).distance(bnd))
say('S2.eric', 'Eric Moore rd-d8784e5c local main 12.5 m, ends 1.9 m short', f'{r.get("name")} {r["kind"]} {r["width"]} m, '
    f'end {dd:.1f} m from line', r['kind'] == 'local_main' and r['width'] == 12.5 and near(dd, 1.9, 0.15))
for rid in ('rd-da8895b1', 'rd-63ff2dcb'):
    d, r, L, a, z = rinfo(rid)
    say('S2.' + rid[3:], 'unnamed main road touching the line', f'{d} {r.get("name", "(unnamed)")} {r["kind"]} '
        f'{L.distance(bnd):.2f} m', L.distance(bnd) < 0.5 and r['kind'] == 'main_road')
d, r, L, a, z = rinfo('rd-b2b8a5cc')
e = min((a, z), key=lambda p: Point(p).distance(R))
say('S2.lbx', 'rd-b2b8a5cc ends (12568.69, 7733.91), 157 m short of d11', f'{d} {r["kind"]} {r["width"]} end {e}, '
    f'{Point(e).distance(R):.0f} m', e == [12568.69, 7733.91] and near(Point(e).distance(R), 157, 1))
gap = LineString([e, R.exterior.interpolate(R.exterior.project(Point(e))).coords[0]]).buffer(40)
wide = [(rid, dd_, rr['width']) for rid, (dd_, rr) in ROADS.items() if rr['width'] >= 13 and LineString(rr['centreline']).intersects(gap)
        and dd_ != 'd09']
say('S2.lbx2', 'no 25 m record across Agunda\'s corner', f'records >=13 m crossing the gap (40 m band): {wide}', not wide)
for rid in ('rd-ae987305', 'rd-dee2c26e', 'rd-9eb41b43'):
    d, r, L, a, z = rinfo(rid)
    say('S2.' + rid[3:], 'Agunda 7 m record near the line', f'{d} {r["kind"]} {r["width"]} m, {L.distance(bnd):.0f} m from d11, '
        f'{L.distance(Point(e)):.0f} m from the expressway end', d == 'd12' and r['width'] == 7)

# ---------------------------------------------------------------- frame roads
print('== section 3: frame-study roads clipped to the ring')
agg = {}
tot = 0
for r in F['roads']:
    L = LineString(r['p'])
    if not L.intersects(R):
        continue
    l = L.intersection(R).length
    tot += l
    key = (r['n'] or '(unnamed)', r['k'], r['l'])
    agg[key] = agg.get(key, 0) + l
for k, v in sorted(agg.items(), key=lambda kv: -kv[1]):
    if v >= 20:
        print(f'          frame road {k}: {v:.0f} m')
say('S3.ftot', '16.6 km in all, counting bridge lines', f'{tot / 1000:.1f} km', near(tot / 1000, 16.6, 0.05))
say('S3.fram', 'rail 3,103 unnamed + 1,816 Lagos-Ibadan + 714 Blue Line; Apapa Rd 1,261 motorway (661 bridge); Eko Bridge '
    '1,219 motorway all bridge; unnamed primary 1,111 + 106; unnamed motorway 975; Western Ave 779 primary + 315 motorway, '
    '223 bridge; L-B Expwy 778 + 123 trunk, 159 bridge; Ijora Causeway 541 (104 bridge); unnamed trunk 384; MMW 228',
    'see the frame road lines above (k = kind, l = layer flag)',
    all(near(agg.get(k, 0), v, 1.5) for k, v in {('(unnamed)', 'rail', 0): 3103, ('Lagos–Ibadan SGR', 'rail', 0): 1816,
        ('LRMT Blue Line', 'rail', 0): 714, ('Apapa Road', 'motorway', 0): 1261, ('Apapa Road', 'bridge', 0): 661,
        ('Eko Bridge', 'motorway', 0): 1219, ('Eko Bridge', 'bridge', 0): 1219, ('(unnamed)', 'primary', 0): 1111,
        ('(unnamed)', 'primary', 1): 106, ('(unnamed)', 'motorway', 1): 975, ('Western Avenue', 'primary', 0): 779,
        ('Western Avenue', 'motorway', 0): 315, ('Western Avenue', 'bridge', 0): 223,
        ('Lagos-Badagry Expressway', 'trunk', 0): 778, ('Lagos Badagry Expressway', 'trunk', 0): 123,
        ('Ijora Causeway', 'primary', 0): 541, ('Ijora Causeway', 'bridge', 0): 104, ('(unnamed)', 'trunk', 1): 384,
        ('Murtula Muhammed Way', 'primary', 0): 228}.items())
    and near(agg[('Lagos Badagry Expressway', 'bridge', 0)] + agg[('Lagos-Badagry Expressway', 'bridge', 0)], 159, 2))
water = unary_union([Polygon(w[0], w[1:]) for w in F['water']]).buffer(0)
say('S5.water', 'only 1,180 game m2 of frame water inside the ring', f'{water.intersection(R).area:.0f} m2',
    near(water.intersection(R).area, 1180, 10))
fc = [p for p in F['places'] if p['n'] == 'Costain']
say('S1.fcost', 'frame "Costain" place point at (13474, 7194), inside the ring', [(p['at'], R.contains(Point(p['at']))) for p in fc],
    bool(fc) and near(fc[0]['at'][0], 13474, 1) and near(fc[0]['at'][1], 7194, 1))
say('S1.420', 'real Costain junction 420 m further south (13436, 7612)', f'{7612 - fc[0]["at"][1]:.0f} m in y', near(7612 - fc[0]['at'][1], 420, 5))

# ---------------------------------------------------------------- csv
print('== places.csv and borders.csv')
P = {r['name']: r for r in csv.DictReader(open(os.path.join(ROOT, 'docs/lagos-study/roads/places.csv')))}
for name, want in (('Iganmu', 'industry 1174 83 0.55 10.3'), ('Ijora', 'industry 1161 53'), ('Ijora Badia', 'port & tank farm 868 big 0.62'),
                   ('Iponri', 'bungalow suburb 2685 104 6.2'), ('Costain', 'bungalow suburb 1210 68 7.6')):
    r = P.get(name)
    say('S5.' + name.replace(' ', '')[:6], want, r and f"{r['fabric']} {r['bldg_per_km2']} {r['median_foot_m2']} big {r['big_share']} h {r['height_m']}", None)
ib = [r for n_, r in P.items() if n_.startswith('Ijora Badia')]
for r in ib:
    print(f"          places.csv {r['name']}: {r['fabric']} {r['bldg_per_km2']}/km2 median {r['median_foot_m2']} big {r['big_share']}")
B = list(csv.DictReader(open(os.path.join(ROOT, 'docs/lagos-study/roads/borders.csv'))))
for r in B:
    if 'Ijora' in r['place_a'] + r['place_b'] and ('creek' in r['border'] or 'water' in r['border'] or 'Apapa GRA' in r['place_a'] + r['place_b']):
        print(f"          borders.csv {r['place_a']} | {r['place_b']}: {r['border']} {r['length_km']} km, roads {r['roads']}")
say('S5.creek', 'creek Ijora|Ijora Badia 0.45 km; Ijora|Apapa GRA 0.65 km; Apapa GRA NE|Ijora Badia main road, Ijora Causeway and Apapa Road',
    'see borders.csv lines above', None)

# ---------------------------------------------------------------- Overture
print('== Overture, clipped to the ring')
lo0, la0 = real(b[0] - 50, b[3] + 50)
lo1, la1 = real(b[2] + 50, b[1] - 50)
lo0, lo1, la0, la1 = lo0 - 0.01, lo1 + 0.01, la0 - 0.01, la1 + 0.01   # a wider box so d10/d13/d16 points come in too


import numpy as np


def _tf(c):
    u, v = T.transform(c[:, 0], c[:, 1])
    return np.column_stack(((np.asarray(u) - 500525) / 3, 10500 - (np.asarray(v) - 707825) / 3))


def load(name, cols):
    t = pq.read_table(os.path.join(OV, f'lagos_overture_{name}.parquet'), columns=cols + ['geometry', 'bbox'])
    out = []
    for row in t.to_pylist():
        bb = row['bbox']
        if bb['xmax'] < lo0 or bb['xmin'] > lo1 or bb['ymax'] < la0 or bb['ymin'] > la1:
            continue
        g = shapely.from_wkb(row['geometry'])
        row['ll'] = g
        row['g'] = shapely.transform(g, _tf)
        out.append(row)
    return out


PL = load('place', ['names', 'basic_category', 'taxonomy', 'confidence'])
for p in PL:
    p['name'] = (p['names'] or {}).get('primary') or ''
    p['cat'] = (p['taxonomy'] or {}).get('primary') or ''
LU = load('land_use', ['names', 'subtype', 'class'])
INF = load('infrastructure', ['names', 'subtype', 'class'])
SEG = load('segment', ['names', 'subtype', 'class', 'road_surface', 'level_rules', 'road_flags', 'speed_limits', 'routes'])
for x in LU + INF + SEG:
    x['name'] = (x['names'] or {}).get('primary') or ''
inR = lambda p: R.contains(p['g'])
place_kind_church = lambda p: p['basic_category'] in ('christian_place_of_worship',) or bool(re.search(r'church|ministr|assembl|parish|chapel|rccg|cathedral|gospel', p['name'], re.I))


def find(name, exact=False):
    return [p for p in PL if (p['name'] == name if exact else name.lower() in p['name'].lower())]


def where(n):
    """Which frame district holds this game point."""
    for k in FD:
        if fring(k).contains(n):
            return k
    return None


# land use shares
lu = {}
for x in LU:
    if x['g'].geom_type in ('Polygon', 'MultiPolygon'):
        if x['subtype'] == 'protected':
            continue
        a = x['g'].buffer(0).intersection(R).area
        if a:
            lu[x['subtype'], x['class']] = lu.get((x['subtype'], x['class']), 0) + a
say('S1.lu', 'industrial 27%, residential 23%, railway 4%, grass 1.7%, retail 0.9%, brownfield+farmland+commercial 2%',
    ', '.join(f'{k[1]} {v / R.area * 100:.2f}%' for k, v in sorted(lu.items(), key=lambda kv: -kv[1])) +
    ' (Overture\'s "protected" polygon, a Pacific marine monument over the whole box, left out)',
    near(lu['developed', 'industrial'] / R.area * 100, 27, 0.5) and near(lu['residential', 'residential'] / R.area * 100, 23, 0.5)
    and near(lu['developed', 'retail'] / R.area * 100, 0.9, 0.05))
cls = {}
for x in LU:
    if x['g'].geom_type in ('Polygon', 'MultiPolygon'):
        a = x['g'].buffer(0).intersection(R).area
        if a > 500:
            cls[(x['subtype'], x['class'], x['name'])] = cls.get((x['subtype'], x['class'], x['name']), 0) + a
for k, v in sorted(cls.items(), key=lambda kv: -kv[1])[:14]:
    print(f'          land_use {k}: {v:.0f} m2')
rail = [x for x in LU if x['class'] == 'railway' and x['g'].buffer(0).intersection(R).area > 0]
say('S1.rlu', 'a "railway" land-use polygon of 29,288 game m2 (north tip)', [f"{x['g'].buffer(0).intersection(R).area:.0f} m2 "
    f"y {x['g'].bounds[1]:.0f}-{x['g'].bounds[3]:.0f}" for x in rail], any(near(x['g'].buffer(0).intersection(R).area, 29288, 30) for x in rail))
grass = [x for x in LU if x['class'] in ('grass',) and x['g'].buffer(0).intersection(R).area > 5000]
say('S4.grass', 'theatre grass grounds 11,398 game m2, x 13347-13501, y 7722-7891',
    [f"{x['g'].buffer(0).intersection(R).area:.0f} m2 bbox %.0f-%.0f, %.0f-%.0f" % (x['g'].bounds[0], x['g'].bounds[2], x['g'].bounds[1], x['g'].bounds[3]) for x in grass],
    any(near(x['g'].buffer(0).intersection(R).area, 11398, 15) for x in grass))
ret = [x for x in LU if x['subtype'] == 'commercial' and x['class'] == 'retail' and x['g'].buffer(0).intersection(R).area > 1000]
ret = ret or [x for x in LU if x['class'] in ('retail', 'marketplace') and x['g'].buffer(0).intersection(R).area > 1000]
say('S4.ret', 'Iponri Market retail polygon 5,536 m2, x 13211-13295, y 7456-7544',
    [f"{x['class']} {x['name']!r} {x['g'].buffer(0).intersection(R).area:.0f} m2 bbox %.0f-%.0f, %.0f-%.0f" % (x['g'].bounds[0], x['g'].bounds[2], x['g'].bounds[1], x['g'].bounds[3]) for x in ret],
    any(near(x['g'].buffer(0).intersection(R).area, 5536, 10) for x in ret))
ind = sorted([x for x in LU if x['class'] == 'industrial'], key=lambda x: -x['g'].buffer(0).intersection(R).area)[:1]
say('S4.ind', 'biggest industrial polygon 100,041 m2 in the ring, between Eric Moore Rd and the expressway',
    [f"{x['g'].buffer(0).intersection(R).area:.0f} m2 bbox %.0f-%.0f, %.0f-%.0f" % (x['g'].bounds[0], x['g'].bounds[2], x['g'].bounds[1], x['g'].bounds[3]) for x in ind],
    near(ind[0]['g'].buffer(0).intersection(R).area, 100041, 50))
res = [x for x in LU if x['subtype'] == 'residential' and x['g'].buffer(0).intersection(R).area > 1000 and x['g'].bounds[3] > 8050]
say('S1.pock', 'residential pocket by the Eko Bridge foot, about x 13506-13630, y 8094-8222',
    ["%s %.0f-%.0f, %.0f-%.0f" % (x['class'], *[x['g'].buffer(0).intersection(R).bounds[i] for i in (0, 2, 1, 3)]) for x in res], None)
pitch = [x for x in LU if x['class'] == 'pitch' and x['g'].buffer(0).intersection(R).area > 0]
say('S4.pitch', 'pitch polygon of 725 m2 by the Railway Institute', [f"{x['g'].area:.0f} m2 at %.0f, %.0f" % x['g'].centroid.coords[0] for x in pitch],
    any(near(x['g'].area, 725, 5) for x in pitch))
plat = [x for x in INF if x['class'] == 'platform' and R.intersects(x['g'])]
say('S4.plat', 'two platforms at Mobolaji Johnson, ~615 m2 each', [f"{x['g'].area:.0f} m2 at %.0f, %.0f" % x['g'].centroid.coords[0] for x in plat], None)
sup = [x for x in INF if x['class'] in ('bridge_support', 'pillar', 'pier') and R.contains(x['g'].centroid)]
say('S7.sup', '15 bridge supports in the ring, most at the Eko Bridge foot', f"{len(sup)}; y > 8000: {sum(1 for x in sup if x['g'].centroid.y > 8000)}; "
    f"classes {sorted({x['class'] for x in INF if R.contains(x['g'].centroid)})}", len(sup) == 15)
busst = [x for x in INF if x['class'] in ('bus_station', 'bus_stop') and R.contains(x['g'].centroid)]
say('S4.busst', 'Costain bus station 144 m2 in Overture', [f"{x['class']} {x['name']!r} {x['g'].area:.0f} m2 at %.0f, %.0f" % x['g'].centroid.coords[0] for x in busst], None)

# places
print('== Overture places (name, category, lat/lon, game, frame district)')
WANT = ['Aorta', 'Iponri', 'Costain', 'National Theatre', 'National Gallery', 'Little Theatre', 'National Studios',
        'Nigerian Breweries', 'Abebe', 'Railway Hospital', 'Railway Institute', 'Railway Museum', 'Lilypond', 'Sifax',
        'Total', 'Michelin', 'CFAO', 'Abdul Azeez', 'Dairat', 'Ijero Baptist', 'Ascension', 'St Paul', "St. Paul",
        'Marywood', 'Jibril Martin', 'Olaleye', 'Alaka', 'Anthony', 'Seven', '7up', '7-Up', 'Ijora Badia', 'Ijora Central',
        'Oloye', 'Ebute Metta', 'Mobolaji', 'Cummins', 'Building Material']
for p in PL:
    if any(w.lower() in p['name'].lower() for w in WANT):
        x, y = p['g'].coords[0]
        lon, lat = p['ll'].coords[0]
        print(f"          {p['name']!r} [{p['cat']}] conf {p['confidence']:.2f} {lat:.4f}, {lon:.4f} -> {x:.0f}, {y:.0f} d{where(p['g'])}")

PTS = [  # (id, label, lat, lon, stated game x, y, district the note puts it in)
    ('S1.ijsub', 'OSM Ijora suburb point', 6.4667, 3.3678, 13381, 8172, 10),
    ('S1.7up', 'Seven-Up plant', 6.4678, 3.3642, None, None, 10),
    ('S1.ipest', 'Iponri Housing Estate (Overture)', 6.4883, 3.3612, None, None, 13),
    ('S1.jaek', 'Jaekel House (Wikipedia)', 6.4890, 3.3783, None, None, 16),
    ('S1.mus', 'Legacy Nigerian Railway Museum (Overture)', 6.4946, 3.3762, 13690, 7143, 11),
    ('S3.aorta', 'Aorta Interchange', 6.4862, 3.3646, 13263, 7453, 11),
    ('S4.nt', 'National Theatre (OSM way centre)', 6.4765, 3.3695, 13444, 7811, 11),
    ('S4.ntbl', 'National Theatre Blue Line station', 6.4748, 3.3688, 13418, 7873, 11),
    ('S4.ntcp', 'car park by the station', 6.4756, 3.3677, None, None, 11),
    ('S4.cbs', 'Costain bus stop', 6.4819, 3.3693, 13436, 7612, 11),
    ('S4.cbs2', 'second "Costain Busstop"', 6.4772, 3.3657, 13303, 7785, 11),
    ('S4.cj', 'Costain junction', 6.4814, 3.3683, 13399, 7630, 11),
    ('S4.ipm', 'Iponri Market', 6.4849, 3.3643, 13252, 7501, 11),
    ('S4.ipbs', 'Iponri bus stop', 6.4871, 3.3647, 13266, 7420, 11),
    ('S4.nbh', 'Nigerian Breweries Hospital', 6.4819, 3.3629, 13200, 7612, 11),
    ('S4.abebe', 'Abebe Village Road', 6.4811, 3.3609, 13125, 7642, 11),
    ('S4.mj', 'Mobolaji Johnson station', 6.5018, 3.3737, 13598, 6878, 11),
    ('S4.rh', 'Nigerian Railway Hospital', 6.5021, 3.3731, 13576, 6867, 11),
    ('S4.ri', 'The Railway Institute', 6.4957, 3.3731, 13576, 7103, 11),
    ('S4.bus', 'unnamed bus station by the railway land', 6.4934, 3.3758, 13674, 7186, 11),
    ('S4.fuel', 'fuel station by the railway land', 6.4921, 3.3758, 13675, 7236, 11),
    ('S4.lily', 'Lilypond Container Terminal', 6.4696, 3.3638, 13234, 8065, 11),
    ('S4.sifax', 'Sifax Empty Container Terminal', 6.4712, 3.3627, 13193, 8006, 11),
    ('S4.trd1', 'causeway trade strip (west end)', 6.4694, 3.3694, 13441, 8073, 11),
    ('S4.trd2', 'causeway trade strip (east end)', 6.4697, 3.3701, 13465, 8060, 11),
    ('S4.aacm', 'Abdul Azeez Central Mosque', 6.4817, 3.3769, 13716, 7619, 11),
    ('S4.dairat', 'Dairat Jafariyah', 6.4664, 3.3767, 13708, 8183, 11),
    ('S4.ijero', 'Ijero Baptist Church', 6.4820, 3.3737, 13598, 7608, 11),
    ('S4.asc', 'Anglican Church of the Ascension', 6.4821, 3.3758, 13676, 7604, 11),
    ('S4.stp', "St Paul's (Overture)", 6.4807, 3.3733, 13584, 7656, 11),
    ('S4.stp16', "St Paul's (OSM, in [D16])", 6.4846, 3.3824, None, None, 16),
    ('S4.mary', 'Marywood Girls College', 6.4862, 3.3716, 13521, 7453, 11),
    ('S4.jm', 'Jibril Martin Memorial Grammar School', 6.4861, 3.3671, 13355, 7457, 11),
    ('S4.ipehs', 'Iponri Estate High School', 6.4855, 3.3663, 13326, 7481, 11),
    ('S4.olal', 'Olaleye Market', 6.4855, 3.3689, 13421, 7479, 11),
    ('S4.alaka', 'Alaka Estate', 6.4912, 3.3633, 13215, 7269, 11),
    ('S4.pol', 'Police station ("Anthony")', 6.4885, 3.3694, 13440, 7368, 11),
]
print('== stated positions: lat/lon -> game by gidi(), and the frame district that holds them')
for cid, lab, lat, lon, sx, sy, sd in PTS:
    x, y = gidi(lon, lat)
    d = where(Point(x, y))
    ok = (sx is None or (near(x, sx, 4) and near(y, sy, 4))) and d == sd
    say(cid, f'{lab} ({lat}, {lon}) -> {sx}, {sy} in d{sd}', f'{x:.0f}, {y:.0f} in d{d}', ok)

# Overture place counts in the ring
cnt = {}
for p in PL:
    if inR(p):
        cnt[p['basic_category']] = cnt.get(p['basic_category'], 0) + 1
top = sorted(cnt.items(), key=lambda kv: -kv[1])[:10]
say('S5.ovc', '24 churches, 22 religious orgs, 16 professional services, 15 clothing shops, 10 schools, 10 hotels',
    'basic_category: ' + ', '.join(f'{k} {v}' for k, v in top) + f"; total {sum(cnt.values())}",
    [cnt.get(k) for k in ('christian_place_of_worship', 'religious_organization', 'professional_service',
     'fashion_and_apparel_store', 'place_of_learning', 'hotel')] == [24, 22, 16, 15, 10, 10])
rel = [p['name'] for p in PL if inR(p) and p['cat'] == 'religious_organization']
mos = [n for n in rel if re.search(r'mosque|masjid|jama|islam|ansar|nawair|anwar|muslim', n, re.I)]
say('S1.mosq', 'Overture files some mosques under religious_organization', mos, bool(mos))
say('S4.cmosq', 'Abdul Azeez the only "central mosque" in the ring', [p['name'] for p in PL if inR(p) and 'central mosque' in p['name'].lower()], None)
mk = [p for p in PL if inR(p) and ('motor park' in p['name'].lower() or p['cat'] in ('bus_station', 'park_and_ride'))]
say('S8.park', 'no named motor park in Overture inside the ring', [(p['name'], p['cat']) for p in mk], None)
nb = [p for p in PL if inR(p) and 'brewer' in p['name'].lower()]
say('S4.nb', 'Overture has no named brewery (only the hospital)', [p['name'] for p in nb], None)

# segments
print('== Overture segments in the ring')
roadlen = sum(s_['g'].intersection(R).length for s_ in SEG if s_['subtype'] == 'road')
raillen = sum(s_['g'].intersection(R).length for s_ in SEG if s_['subtype'] == 'rail')
say('S3.ovt', '30.2 km of road and 5.6 km of rail in the ring', f'{roadlen / 1000:.1f} km road, {raillen / 1000:.1f} km rail',
    near(roadlen / 1000, 30.2, 0.05) and near(raillen / 1000, 5.6, 0.05))


def seg(name, cls_=None):
    out = [s_ for s_ in SEG if s_['name'] == name and (cls_ is None or s_['class'] == cls_)]
    L = sum(s_['g'].intersection(R).length for s_ in out)
    parts = [s_['g'].intersection(R) for s_ in out if s_['g'].intersection(R).length > 0]
    bb = unary_union(parts).bounds if parts else None
    return out, L, bb


for cid, nm, c, sl, sbb in (('S3.apapa', 'Apapa Road', 'motorway', 1259, (13199, 7452, 13331, 8108)),
                            ('S3.apt', 'Apapa Road', 'tertiary', 308, None),
                            ('S3.eric', 'Eric Moore Road', None, 866, (12917, 7442, 13229, 7806)),
                            ('S3.mmw', 'Murtula Muhammed Way', None, 228, (13563, 6679, 13685, 6978)),
                            ('S2.lbx3', 'Lagos-Badagry Expressway', None, 784, (12735, 7708, 13229, 7806))):
    out, L, bb = seg(nm, c)
    say(cid, f'{nm} ({c or "all"}) {sl} m in the ring' + (f', bbox {sbb}' if sbb else ''),
        f'{L:.0f} m, bbox ' + ('%.0f-%.0f, %.0f-%.0f' % (bb[0], bb[2], bb[1], bb[3]) if bb else '-') +
        f"; classes {sorted({s_['class'] for s_ in out if s_['g'].intersects(R)})}", near(L, sl, 3))
out, L, bb = seg('Apapa Road', 'tertiary')
say('S3.apty', 'tertiary Apapa Road at y about 7615-7639, from Costain east to the railway',
    'y %.0f-%.0f, x %.0f-%.0f' % (bb[1], bb[3], bb[0], bb[2]) if bb else '-', None)
apd16 = [r for r in REC['d16'] if r['type'] == 'road' and NAME.get(r['id']) == 'Apapa Road']
say('S3.ap16', 'd16 drew 186 m of Apapa Road', f"{sum(LineString(r['centreline']).length for r in apd16):.0f} m in {len(apd16)} records",
    near(sum(LineString(r['centreline']).length for r in apd16), 186, 2))
for cid, nm in (('S3.wav', 'Western Avenue'), ('S3.wavf', 'Funsho Williams Avenue'), ('S3.eko', 'Eko Bridge'),
                ('S3.ijc', 'Ijora Causeway'), ('S3.lbx', 'Lagos-Badagry Expressway'), ('S3.eric2', 'Eric Moore Road'),
                ('S3.apapa2', 'Apapa Road'), ('S3.mmw2', 'Murtula Muhammed Way'), ('S3.ofa', 'Oba Fatai Aromire Way')):
    out = [s_ for s_ in SEG if s_['name'] == nm and s_['g'].intersects(R.buffer(30))]
    lv = sorted({lr['value'] for s_ in out for lr in (s_['level_rules'] or [])})
    fl = sorted({v for s_ in out for f_ in (s_['road_flags'] or []) for v in f_['values']})
    sp = sorted({sl_['max_speed']['value'] for s_ in out for sl_ in (s_['speed_limits'] or []) if sl_.get('max_speed')})
    refs = sorted({rt['ref'] for s_ in out for rt in (s_['routes'] or []) if rt.get('ref')})
    surf = sorted({rs['value'] for s_ in out for rs in (s_['road_surface'] or [])})
    say(cid, nm + ' tags', f"{len(out)} pieces; classes {sorted({s_['class'] for s_ in out})}; levels {lv}; flags {fl}; "
        f"maxspeed {sp}; refs {refs}; surface {surf}", None)
inner = ['Abule-Nla Road', 'Park Road', 'Ibadan Street', 'Afric Road', 'Barracks Road', 'Franklin Road', 'Mosalashi Street',
         'Temple Street', 'Owukori Crescent', 'Olaleye Road', 'Jimoh Odutola Street', 'Imam Dauda Street', 'Oke-Ira Road',
         'Ahmadu Bello Road', 'Awolowo Road', 'Nnamdi Azikiwe Road', 'Abubakar Road', 'Akintola Road', 'Ikejiani Road']
segnames = {s_['name'] for s_ in SEG if s_['g'].intersects(R)}
for nm in inner:
    hit = nm in segnames
    alt = sorted(n for n in segnames if nm.split()[0].lower() in n.lower()) if not hit else []
    out = [s_ for s_ in SEG if s_['name'] == nm and s_['g'].intersects(R)]
    lv = sorted({lr['value'] for s_ in out for lr in (s_['level_rules'] or [])})
    fl = sorted({v for s_ in out for f_ in (s_['road_flags'] or []) for v in f_['values']})
    bb = unary_union([s_['g'].intersection(R) for s_ in out]).bounds if out else None
    say('S3.in', f'{nm} in the ring', ('yes' if hit else f'no (similar: {alt})') + (f'; levels {lv} flags {fl}; bbox x %.0f-%.0f y %.0f-%.0f' % (bb[0], bb[2], bb[1], bb[3]) if bb else ''), hit)
lead = [s_ for s_ in SEG if s_['g'].intersects(R) and re.search(r'Ahmadu Bello|Awolowo|Azikiwe|Abubakar|Akintola|Ikejiani', s_['name'])]
bb = unary_union([s_['g'].intersection(R) for s_ in lead]).bounds if lead else None
for nm in sorted({s_['name'] for s_ in lead}):
    q_ = unary_union([s_['g'].intersection(R) for s_ in lead if s_['name'] == nm]).bounds
    print(f'          {nm}: x %.0f-%.0f, y %.0f-%.0f' % (q_[0], q_[2], q_[1], q_[3]))
say('S3.lead', 'leaders grid at x 13517-13566, y 7113-7299', 'x %.0f-%.0f, y %.0f-%.0f' % (bb[0], bb[2], bb[1], bb[3]) if bb else '-',
    bb is not None and near(bb[0], 13517, 3) and near(bb[2], 13566, 3) and near(bb[1], 7113, 3) and near(bb[3], 7299, 3))
rs = [s_ for s_ in SEG if s_['subtype'] == 'road' and s_['g'].intersects(R)]
unp = [s_ for s_ in rs if any(x['value'] == 'unpaved' for x in (s_['road_surface'] or []))]
say('S3.unp', 'many roads tagged unpaved', f"{len(unp)} of {len(rs)} road pieces; {sum(s_['g'].intersection(R).length for s_ in unp):.0f} m of {roadlen:.0f} m", None)

ipe = [s_ for s_ in SEG if s_['name'] == 'Iponri Estate Road']
L13 = sum(s_['g'].intersection(fring(13)).length for s_ in ipe)
L11 = sum(s_['g'].intersection(R).length for s_ in ipe)
say('S1.iper', 'most of Iponri Estate Road falls in d13', f'{L13:.0f} m in d13, {L11:.0f} m in d11', L13 > L11)
fc_ = Point(fc[0]['at'])
ch = [p['name'] for p in PL if p['g'].distance(fc_) < 100 and place_kind_church(p)]
say('S1.okeira', 'the frame Costain point sits among the Oke-Ira churches', f'{len(ch)} church places within 100 m: {ch[:6]}', None)
okr = [s_ for s_ in SEG if s_['name'] == 'Oke-Ira Road']
say('S1.okeira2', '(Oke-Ira Road beside it)', f"Oke-Ira Road {min(s_['g'].distance(fc_) for s_ in okr):.0f} m from the point" if okr else 'no Oke-Ira Road', None)

print('== named Overture infrastructure (OSM-derived) for the OSM-cited points')
for cid, nm, cls_, lat, lon in (('S3.aortaI', 'Aorta Interchange', 'motorway_junction', 6.4862, 3.3646),
                                ('S4.ntblI', 'National Theatre', 'subway_station', 6.4748, 3.3688),
                                ('S4.mjI', 'Mobolaji Johnson Station', 'railway_station', 6.5018, 3.3737),
                                ('S4.cbsI', 'Costain Bus stop', 'bus_station', 6.4819, 3.3693)):
    hit = [x for x in INF if x['name'] == nm and x['class'] == cls_]
    got = [(round(x['ll'].centroid.y, 4), round(x['ll'].centroid.x, 4)) for x in hit]
    say(cid, f'{nm} ({cls_}) at {lat}, {lon}', got, any(near(a, lat, 0.00015) and near(o, lon, 0.00015) for a, o in got))
say('S1.ijsubI', 'Ijora/Badia places of section 1 in d10', [(p['name'], where(p['g'])) for p in PL if p['name'] in (
    'Ijora Badia Market', 'Ijora Central Mosque', 'Ijora Oloye Primary Health Center', 'Ijora Oloye Nursery and Primary School',
    'Seven-Up Bottling Company (PepsiCo International)')],
    all(where(p['g']) == 10 for p in PL if p['name'] in ('Ijora Badia Market', 'Ijora Central Mosque',
        'Ijora Oloye Primary Health Center', 'Ijora Oloye Nursery and Primary School', 'Seven-Up Bottling Company (PepsiCo International)')))
