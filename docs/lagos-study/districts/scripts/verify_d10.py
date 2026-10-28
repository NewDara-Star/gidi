"""Re-check the data claims of docs/lagos-study/districts/d10.md (Apapa scout note, 27 Oct) against the repo's own data.

Each line: claim id | what the note states | what was found | verdict (TRUE / FALSE / CHECK = read the found value).
Web claims are not here (listed in the agent's report). OSM claims (Overpass, 27 Oct) have no local copy: only the
in-which-outline part of their positions is checked.

  ~/.venvs/gidi/bin/python -I <this file>
"""
import collections
import csv
import json
import os
import re

import pyarrow.parquet as pq
import shapely
from pyproj import Transformer
from shapely.geometry import LineString, MultiPolygon, Point, Polygon, box
from shapely.ops import unary_union

GIDI = os.path.expanduser('~/gidi')
OV = os.path.expanduser('~/gidi-data/research/data/overture-lagos')
T = Transformer.from_crs(4326, 32631, always_xy=True)
INV = Transformer.from_crs(32631, 4326, always_xy=True)


def gidi(lon, lat):  # as scripts/working_bar.py gidi()
    u, v = T.transform(lon, lat)
    return (u - 500525) / 3, 10500 - (v - 707825) / 3


def to_game(g):
    return shapely.transform(g, lambda a: __import__('numpy').array([gidi(x, y) for x, y in a]).reshape(-1, 2))


n_true = n_false = n_check = 0


def claim(cid, stated, found, ok=None):
    global n_true, n_false, n_check
    v = 'CHECK' if ok is None else ('TRUE' if ok else 'FALSE')
    n_true += v == 'TRUE'; n_false += v == 'FALSE'; n_check += v == 'CHECK'
    print(f'{cid:8s} | stated: {stated} | found: {found} | {v}')


def near(a, b, tol):
    return abs(a - b) <= tol


def pt_ok(p, q, tol=3):
    return abs(p[0] - q[0]) <= tol and abs(p[1] - q[1]) <= tol


# ---- the frame
s = open(os.path.join(GIDI, 'web/frame-study.js')).read()
F = json.loads(s[s.index('{'):s.rindex('}') + 1])
DIST = {d['n']: d for d in F['districts']}


def frame_ring(n):
    return MultiPolygon([Polygon(r[0], r[1:]) for r in DIST[n]['rings']]).buffer(0)


R = {n: frame_ring(n) for n in DIST}
D10 = R[10]


def where(p):
    P = Point(p)
    hits = [n for n, g in R.items() if g.contains(P)]
    return hits[0] if hits else None


def verts(n):
    out = set()
    for r in DIST[n]['rings']:
        for ring in r:
            for x, y in ring:
                out.add((round(x, 1), round(y, 1)))
    return out


V10 = verts(10)
print('== Section 1: what the district is')
pieces = [p for p in F['places'] if p['d'] == 10]
claim('1.pieces', 'six place pieces in the frame d10', f'{len(pieces)}: ' + '; '.join(p['n'] for p in pieces), len(pieces) == 6)
pp = {p['n']: p['at'] for p in pieces}
for name, st in [('Apapa GRA, south-west of Apapa-Oworonshoki Expressway', (12641, 9384)),
                 ('Apapa Wharf south-east', (13739, 9642)), ('Apapa GRA north-east', (13412, 8399))]:
    claim('1.piece', f'{name} at {st}', pp[name], pt_ok(pp[name], st, 2))

PC = {r['name']: r for r in csv.DictReader(open(os.path.join(GIDI, 'docs/lagos-study/roads/places.csv')))}
isl = PC['Apapa Wharf south-east']
claim('1.island', '4,597 buildings, median 42 m2, 4.2 m, grid 0.343', f"{isl['bldg']}, {isl['median_foot_m2']}, {isl['height_m']}, {isl['grid']}",
      (isl['bldg'], isl['median_foot_m2'], isl['height_m'], isl['grid']) == ('4597', '42.0', '4.2', '0.343'))
claim('1.ne.fab', 'GRA north-east: port & tank farm fabric', PC['Apapa GRA north-east']['fabric'], PC['Apapa GRA north-east']['fabric'] == 'port & tank farm')

polys = sorted(D10.geoms, key=lambda g: -g.area) if D10.geom_type == 'MultiPolygon' else [D10]
claim('1.size', '1.48 km2 in game, three polygons', f'{D10.area/1e6:.3f} km2, {len(polys)} polygons', near(D10.area / 1e6, 1.48, 0.005) and len(polys) == 3)
claim('1.real', '13.3 km2 real (x9)', f'{D10.area*9/1e6:.2f}', near(D10.area * 9 / 1e6, 13.3, 0.05))
names6 = ['Apapa GRA', 'Apapa GRA north-east', 'Apapa Wharf, east of Apapa-Oworonshoki Expressway',
          'Apapa GRA, south-west of Apapa-Oworonshoki Expressway', 'Apapa Wharf south-east', 'Apapa Wharf']
sm = sum(float(PC[n]['land_km2']) for n in names6)
claim('1.land6', "six pieces' land in places.csv sums to 13.3 km2", f'{sm:.2f}', near(sm, 13.3, 0.05))
for i, (st_a, st_b, st_n) in enumerate([(1.299, (12075, 8058, 14392, 9558), 125), (0.177, (13492, 9375, 13992, 9925), None),
                                         (139e-6, (12475, 9575, 12492, 9592), None)]):
    g = polys[i]
    b = tuple(round(v) for v in g.bounds)
    npts = max((len(r[0]) for r in DIST[10]['rings'] if abs(Polygon(r[0]).area - g.area) < 1), default=None)  # raw ring, closing point included
    claim(f'1.poly{i}', f'{st_a} km2 bbox {st_b}' + (f' {st_n} points' if st_n else ''), f'{g.area/1e6:.6f} km2 bbox {b} {npts} points',
          near(g.area / 1e6, st_a, 0.0015 if i < 2 else 2e-5) and all(abs(x - y) <= 1 for x, y in zip(b, st_b)) and (st_n is None or npts == st_n))

# positions said to lie in a given outline (OSM or Overture points)
for cid, p, want in [('1.tc-w', (12482, 9328), 8), ('1.tict', (12638, 9342), 10), ('1.berth9', (12403, 9540), 10),
                     ('1.ilado', (13816, 9438), 10), ('1.sagb', (13719, 9422), 10), ('1.ijora', (13382, 8172), 10),
                     ('1.lily', (13235, 8066), 11), ('1.badia', (13158, 7954), 12), ('2.ws-ap', (12744, 8931), 10),
                     ('2.ws-aj', (12720, 8933), 9), ('2.bmkt', (12806, 8643), 9)]:
    claim(cid, f'{p} is in d{want:02d}', f'in d{where(p)}', where(p) == want)

# ---- Overture places inside d10
pl = pq.read_table(os.path.join(OV, 'lagos_overture_place.parquet'), columns=['names', 'geometry', 'confidence', 'basic_category', 'taxonomy']).to_pylist()
P10 = []
for r in pl:
    g = shapely.from_wkb(r['geometry'])
    xy = gidi(g.x, g.y)
    if D10.contains(Point(xy)):
        P10.append(dict(name=(r['names'] or {}).get('primary') or '', xy=xy, lonlat=(g.x, g.y), conf=r['confidence'],
                        cat=r['basic_category'], prim=(r['taxonomy'] or {}).get('primary')))
claim('S.OV', '648 Overture places inside the frame outline', len(P10), len(P10) == 648)


def find(pat):
    return [p for p in P10 if re.search(pat, p['name'], re.I)]


def show(ps):
    return '; '.join(f"{p['name']} ({p['xy'][0]:.0f},{p['xy'][1]:.0f}) {p['lonlat'][1]:.4f},{p['lonlat'][0]:.4f} c{p['conf']:.2f} {p['cat']}" for p in ps[:4]) or 'none'


for pat in ['Western Naval|Naval Command', 'depot|AP/NOC|Oando', 'Ijora Oloye', 'Ijora Central Mosque',
            'Ashanti', 'Tamandu', 'Queen.*Barr', 'Tego', 'School of Finance', 'Signals', 'TICT|Tin.?Can.*Container',
            'Lilypond|Lily Pond', 'Neck', 'Oval', 'Kofo Abayomi']:
    claim('1.OV', f'Overture names /{pat}/ inside d10', show(find(pat)))
barr = [p for p in P10 if re.search(r'^(Ashanti|Tamandu|Queen|Tego) Barracks|School of Finance|School of Signals|Navy Base', p['name'], re.I)]
claim('1.mil-conf', 'the seven military places named: confidence 0.28-0.80', f"{len(barr)} places, {min(p['conf'] for p in barr):.2f}-{max(p['conf'] for p in barr):.2f}: " + ', '.join(f"{p['name']} {p['conf']:.2f}" for p in barr),
      len(barr) == 7 and near(min(p['conf'] for p in barr), 0.28, 0.006) and near(max(p['conf'] for p in barr), 0.80, 0.006))
lily = [r for r in pl if re.search('lilypond|lily pond', ((r['names'] or {}).get('primary') or ''), re.I)]
claim('1.lily-OV', 'Lilypond container terminal at (13235, 8066)', '; '.join(f"{(r['names'] or {}).get('primary')} {tuple(round(v) for v in gidi(*shapely.from_wkb(r['geometry']).coords[0]))}" for r in lily[:5]))

# ---- section 2: neighbours
print('== Section 2: neighbours')
B10 = D10.boundary
tot = B10.length
claim('2.perim', 'outline 10,326 m', f'{tot:.0f}', near(tot, 10326, 3))
shared_len = 0
for n, st_pts, st_len, st_bb in [(8, 36, 2409, (12092, 9107, 13992, 9925)), (9, 12, 1461, (12258, 8275, 13158, 9259)),
                                 (11, 14, 606, (13192, 8058, 13525, 8226)), (12, 7, 456, (13157, 8074, 13242, 8325))]:
    sh = V10 & verts(n)
    seam = B10.intersection(R[n].boundary)
    L = seam.length
    shared_len += L
    xs = [p[0] for p in sh]; ys = [p[1] for p in sh]
    bb = (round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys))) if sh else None
    sb = tuple(round(v) for v in seam.bounds)
    claim(f'2.d{n:02d}', f'{st_pts} shared points, {st_len} m, bbox {st_bb}', f'{len(sh)} points, {L:.0f} m (edge shared with d{n:02d}), seam bbox {sb}',
          len(sh) == st_pts and near(L, st_len, 1.5) and all(abs(a - b) <= 2 for a, b in zip(sb, st_bb)))
others = [n for n in R if n not in (8, 9, 10, 11, 12)]
extra = sum(B10.intersection(R[n].boundary).length for n in others)
claim('2.water', 'rest 5,394 m of 10,326 m is water', f'{tot-shared_len-extra:.0f} m (other districts touch {extra:.0f} m)', near(tot - shared_len - extra, 5394, 3))
for n, st in [(20, 209), (16, 217), (22, 302)]:
    claim(f'2.gap{n}', f'd{n} not touching, {st} m away', f'{D10.distance(R[n]):.0f} m, shared points {len(V10 & verts(n))}', near(D10.distance(R[n]), st, 2) and not (V10 & verts(n)))
touch = [n for n in R if n != 10 and (V10 & verts(n))]
claim('2.touch', 'neighbours with shared points: 8, 9, 11, 12', touch, sorted(touch) == [8, 9, 11, 12])

# expressway along the d08 seam
seam8 = B10.intersection(R[8].boundary)
aoe = unary_union([LineString(r['p']) for r in F['roads'] if 'Apapa-Oworonshoki' in r['n']])
AOE_FRAME = aoe.intersection(seam8.buffer(20)).length  # Overture's line is measured in section 3 (2.aoe962)

# drawn districts
def drawn(d):
    recs = json.load(open(os.path.join(GIDI, 'map', d, 'district.json')))['records']
    D = next(r for r in recs if r['type'] == 'district')
    return D['outline']


for d, n, st_pts, st_all in [('d09', 9, 12, 88), ('d12', 12, 7, None)]:
    o = drawn(d)
    pts = {(round(x, 1), round(y, 1)) for ring in o for x, y in ring}
    allp = sum(len(r) for r in o)
    g = MultiPolygon([Polygon(r) for r in o]).buffer(0)
    claim(f'2.{d}', f'drawn outline has the same {st_pts} points' + (f' ({st_all} in all)' if st_all else '') + ', 0 m2 overlap',
          f'{len(pts & V10 & verts(n))} of the frame seam points ({len(V10 & verts(n))}), {allp} points, overlap {g.intersection(D10).area:.1f} m2',
          len(pts & V10 & verts(n)) == st_pts and (st_all is None or allp == st_all) and g.intersection(D10).area < 1)
claim('2.d08', 'no map/d08', os.path.isdir(os.path.join(GIDI, 'map/d08')), not os.path.isdir(os.path.join(GIDI, 'map/d08')))


def records(d):
    out = []
    for f in os.listdir(os.path.join(GIDI, 'map', d)):
        if f.endswith('.json'):
            out += json.load(open(os.path.join(GIDI, 'map', d, f)))['records']
    return {r['id']: r for r in out if 'id' in r}


r09, r12 = records('d09'), records('d12')
seam9 = B10.intersection(R[9].boundary)
f = r09['rd-f1478f6a']
cl = LineString(f['centreline'])
claim('2.f147', 'rd-f1478f6a 25 m wide, runs 49 m by the seam, 25 m of it over d10 land',
      f"width {f['width']}; centreline within 13 m of the d09 seam {cl.intersection(seam9.buffer(13)).length:.1f} m, within 15 m {cl.intersection(seam9.buffer(15)).length:.1f} m; centreline inside d10 {cl.intersection(D10).length:.1f} m",
      f['width'] == 25.0 and near(cl.intersection(seam9.buffer(15)).length, 49, 1) and near(cl.intersection(D10).length, 25, 1))
STR9 = open(os.path.join(GIDI, 'map/d09/STREETS.md')).read()


def streets_md_name(txt, rid):
    m = re.search(r'\| ' + rid + r' \| ([^|]+)\|', txt)
    return m.group(1).strip() if m else None


for nm in ['Marine Road', 'Okunowa Street', 'Anthony Agbaje Street', 'Young Lane']:
    ids = re.findall(r'\| (rd-[0-9a-f]{8}) \| ' + re.escape(nm) + r' \|', STR9)
    ends = []
    for i in ids:
        c = r09[i]['centreline']
        dd = min(Point(c[0]).distance(seam9), Point(c[-1]).distance(seam9))
        ends.append(f'{i} end {dd:.1f} m from seam')
    claim('2.ends', f'{nm} ends at the d09 seam', '; '.join(ends) or 'not in STREETS.md')
STR12 = open(os.path.join(GIDI, 'map/d12/STREETS.md')).read()
seam12 = B10.intersection(R[12].boundary)
for rid, nm in [('rd-31de79b1', 'Gaskiya College Road'), ('rd-fe80ec1c', 'Gaskiya Road'), ('rd-0009669d', '(unnamed)')]:
    r = r12[rid]
    claim('2.d12rd', f'{rid} {nm} 10.75 m by the seam', f"{streets_md_name(STR12, rid)}, {r['width']} m, {r['kind']}, nearest {LineString(r['centreline']).distance(seam12):.1f} m from seam",
          streets_md_name(STR12, rid) == nm and r['width'] == 10.75)

NN = list(csv.DictReader(open(os.path.join(GIDI, 'docs/lagos-study/roads/not_neighbours.csv'))))
ap = [(r['a'] if r['b'] == 'Apapa-Tin Can' else r['b'], r['old_link']) for r in NN if 'Apapa-Tin Can' in (r['a'], r['b'])]
claim('2.notnb', 'not_neighbours: land Kirikiri-Navy Town, Amukoko-Layeni; water VI, Onikan-Lafiaji, Obalende, Isale Eko', ap)

# ---- Overture segments in d10
print('== Section 3: roads')
seg = pq.read_table(os.path.join(OV, 'lagos_overture_segment.parquet'), columns=['names', 'subtype', 'class', 'geometry', 'bbox', 'road_surface', 'road_flags', 'width_rules', 'subclass']).to_pylist()
(w, n_), (e, s_) = INV.transform(500525 + 3 * 12000, 707825 + 3 * (10500 - 8000)), INV.transform(500525 + 3 * 14500, 707825 + 3 * (10500 - 10000))
S10 = []
for r in seg:
    b = r['bbox']
    if b['xmax'] < w or b['xmin'] > e or b['ymax'] < s_ or b['ymin'] > n_:
        continue
    g = to_game(shapely.from_wkb(r['geometry']))
    if not g.intersects(D10):
        continue
    r['g'] = g; r['gin'] = g.intersection(D10); r['name'] = (r['names'] or {}).get('primary') or ''
    S10.append(r)
L = collections.Counter()
for r in S10:
    if r['subtype'] == 'road':
        L[r['class']] += r['gin'].length
aoe_ov = unary_union([r['g'] for r in S10 if r['subtype'] == 'road' and 'Apapa-Oworonshoki' in r['name']])
claim('2.aoe962', 'AOE: 962 m within 20 m of the d08 seam', f"Overture AOE segments (touching d10): {aoe_ov.intersection(seam8.buffer(20)).length:.0f} m; frame AOE: {AOE_FRAME:.0f} m",
      near(aoe_ov.intersection(seam8.buffer(20)).length, 962, 3))
claim('3.ovres', 'Overture 15.4 km residential, 23.0 km service inside d10', f"{L['residential']/1000:.1f} km residential, {L['service']/1000:.1f} km service", near(L['residential'] / 1000, 15.4, 0.06) and near(L['service'] / 1000, 23.0, 0.06))


def segs(pat):
    return [r for r in S10 if r['subtype'] == 'road' and re.search(pat, r['name'], re.I)]


def classes(pat):
    c = collections.Counter()
    for r in segs(pat):
        c[r['class']] += r['gin'].length
    return {k: round(v) for k, v in c.items()}


for nm, st in [('Wharf Road', 'primary'), ('Burma Road', 'unclassified'), ('Warehouse Road', 'secondary'), ('Liverpool Road', 'secondary'),
               ('Marine Road', 'tertiary'), ('Park Lane', 'tertiary'), ('Point Road', 'residential'), ('Malu Road', 'secondary 824 m'),
               ('Commercial Road', 'secondary 437 m'), ('Dockyard Road', 'unclassified'), ('Tin ?Can Island Port Road', 'tertiary 1,418 m'),
               ('Creek Road', 'no name in Overture'), ('Kofo Abayomi', 'no name in Overture'), ('Randle Road', 'no name in Overture'),
               ('Oduduwa', '(queue road)')]:
    claim('3.cls', f'{nm}: {st}', classes(nm) or 'no segment of that name in d10')
grastreets = ['Child Avenue', 'Ladipo Oluwole', 'Itapeju', 'North Avenue', 'Central Avenue', 'Hinderer', 'Barthurst|Bathurst', 'Forcados',
              'Oranyan', 'Dakar', 'Randle Avenue', 'Bombay', 'Calcutta', 'Crowther', 'Caulcrick', 'Azare', 'Ogedengbe', 'Bornu', 'Idunganran',
              'Lisabi', 'Obanta', 'Danfodio|Dan Fodio', 'Ashanti', 'Takoradi', 'Seaplane', 'Rhodes']
miss = [g for g in grastreets if not segs(g)]
claim('3.gra', f'{len(grastreets)} GRA street names in Overture inside d10', f"{len(grastreets)-len(miss)} found; missing {miss}", not miss)
surf = collections.Counter()
for g in grastreets:
    for r in segs(g):
        for rs in (r['road_surface'] or [{'value': None}]):
            surf[rs['value']] += 1
claim('3.unpaved', 'most GRA streets tagged unpaved', dict(surf))
bar_surf = collections.Counter()
for g in grastreets:
    vals = {rs['value'] for r in segs(g) for rs in (r['road_surface'] or [{'value': None}])}
    bar_surf['unpaved' if vals == {'unpaved'} else 'some unpaved' if 'unpaved' in vals else 'none unpaved'] += 1
claim('3.unpaved2', 'per street name: all unpaved / some / none', dict(bar_surf))
mb = [r for r in segs('Malu Road') if any('is_bridge' in (f['values'] or []) for f in (r['road_flags'] or []))]
mx = unary_union([r['g'] for r in segs('Malu Road')]).intersection(seam9)
claim('3.malu-seam', 'Malu Road runs along the d09 seam north end', f'Overture Malu Road crosses the d09 seam at {mx}; seam spans y 8275-9258')
claim('3.malu-br', 'Malu Road bridge piece at (12950, 8597)', '; '.join(f"({r['gin'].centroid.x:.0f},{r['gin'].centroid.y:.0f}) {r['gin'].length:.0f} m" for r in mb) or 'no bridge flag')
for pat, st in [('Snake Island.*Tunnel', '351 m, class unknown'), ('Apapa Tunnel Bypass', 'class unknown')]:
    claim('3.tunnel', f'{pat}: {st}', '; '.join(f"{r['name']} {r['class']} {r['gin'].length:.0f} m in d10 (whole {r['g'].length:.0f})" for r in segs(pat)) or 'none')
wr = [r for r in S10 if r['width_rules']]
claim('3.width', 'no Overture width rules inside d10', f'{len(wr)} segments with width_rules', not wr)
brs = [r for r in segs('^Apapa Road$') if any('is_bridge' in (f['values'] or []) for f in (r['road_flags'] or []))]
if brs:
    ys = [y for r in brs for x, y in (r['gin'].coords if r['gin'].geom_type == 'LineString' else [c for gg in r['gin'].geoms for c in gg.coords])]
    claim('3.br-span', 'Apapa Road bridge pieces from y 8130 to 8653', f'Overture Apapa Road bridge-flag pieces in d10: y {min(ys):.0f}-{max(ys):.0f}', near(min(ys), 8130, 5) and near(max(ys), 8653, 5))

# frame big roads clipped to d10
FL = collections.Counter()
for r in F['roads']:
    g = LineString(r['p']).intersection(D10)
    if g.length:
        FL[(r['n'] or '(unnamed)', r['k'])] += g.length
for k, v in sorted(FL.items(), key=lambda kv: -kv[1]):
    print(f'         frame road in d10: {k[0]} / {k[1]}: {v:.0f} m')
for (nm, k), st in [(('(unnamed)', 'rail'), 5490), (('Apapa-Oworonshoki Expressway', 'motorway'), 1874), (('Apapa-Oworonshoki Expressway', 'primary'), 1431),
                    (('Apapa-Oworonshoki Expressway', 'bridge'), 474), (('(unnamed)', 'motorway'), 1748), (('(unnamed)', 'bridge'), 1033),
                    (('Apapa Road', 'motorway'), 1149), (('Apapa Road', 'bridge'), 1150), (('Apapa Road', 'primary'), 336), (('Wharf Road', None), 900),
                    (('Malu Road', None), 824), (('Liverpool Road', None), 481), (('Commercial Road', None), 437), (('Warehouse Road', None), 405),
                    (('Ijora Causeway', None), 284), (('Ijora Causeway', 'bridge'), 181)]:
    if k is None:
        got = {kk: round(v) for (n2, kk), v in FL.items() if n2 == nm and kk != 'bridge'}
        val = sum(got.values())
    else:
        val = sum(v for (n2, kk), v in FL.items() if (n2 == nm or (nm == '(unnamed)' and k == 'rail' and kk == 'rail')) and kk == k)
        got = round(val)
    claim('3.frame', f'{nm} {k or ""} {st} m', got, near(val, st, 3))
claim('3.frame-all', 'about 19.5 km in all', f'{sum(FL.values())/1000:.2f} km', near(sum(FL.values()) / 1000, 19.5, 0.1))

# ---- infrastructure and land use
print('== Section 3-5: infrastructure, land use')
INF, LU = [], []
for fname, out in [('lagos_overture_infrastructure.parquet', INF), ('lagos_overture_land_use.parquet', LU)]:
    for r in pq.read_table(os.path.join(OV, fname), columns=['names', 'subtype', 'class', 'geometry', 'bbox']).to_pylist():
        b = r['bbox']
        if b['xmax'] < w or b['xmin'] > e or b['ymax'] < s_ or b['ymin'] > n_:
            continue
        g = to_game(shapely.from_wkb(r['geometry']))
        if not g.is_valid:
            g = g.buffer(0)
        if g.intersects(D10):
            r['g'] = g; r['gin'] = g.intersection(D10); r['name'] = (r['names'] or {}).get('primary') or ''
            out.append(r)
for pat in ['Neck', 'Oval', 'Tin ?Can Island', 'Liverpool', 'number 1 \\(apapa\\)', 'number 1 \\(ajegunle\\)', 'Number 1A', 'second badagry', 'Allens', 'flour mills', 'sagbokoji', 'Tinubu Station']:
    hits = [r for r in INF if re.search(pat, r['name'], re.I)]
    for r in hits:
        r['gin'] = r['g'] if r['gin'].is_empty else r['gin']
    claim('3.inf', f'Overture infrastructure /{pat}/', '; '.join(f"{r['name']} {r['class']} ({r['gin'].centroid.x:.0f},{r['gin'].centroid.y:.0f})" for r in hits[:6]) or 'none')
for r in pq.read_table(os.path.join(OV, 'lagos_overture_infrastructure.parquet'), columns=['names', 'geometry']).to_pylist():
    nm = (r['names'] or {}).get('primary') or ''
    if nm.startswith('number 1 (ajegunle)'):
        c = shapely.from_wkb(r['geometry']).centroid; xy = gidi(c.x, c.y)
        claim('2.ws-aj-OV', 'number 1 (ajegunle) waterside at (12720, 8933) in d09 (the note read OSM; Overture copy, 12 m allowed)', f'({xy[0]:.0f}, {xy[1]:.0f}) in d{where(xy)}', pt_ok(xy, (12720, 8933), 12) and where(xy) == 9)
luc = collections.Counter()
for r in LU:
    luc[r['subtype']] += r['gin'].area
claim('5.land', 'industrial 690,000, residential 488,000, garages 60,000, railway 14,000 m2 (subtype or class)',
      {k: round(v, -3) for k, v in luc.most_common(12)})
luc2 = collections.Counter()
for r in LU:
    luc2[r['class']] += r['gin'].area
claim('5.land-cls', '(by class)', {k: round(v, -3) for k, v in luc2.most_common(14)})
for pat, st in [('Amusement', '[W-AAP][OV] row'), ('Tincan|Tin Can', '186,000 m2 industrial'), ('Port of Apapa', '307,000 m2, centre (13725, 8881)'), ('Boundary', '2,160 m2 on d10 side at (12845, 8641)'),
                ('Liverpool', 'grass at (13077, 9145)'), ('Pacific Islands', 'over the whole district')]:
    hits = [r for r in LU if re.search(pat, r['name'], re.I)]
    claim('LU', f'{pat}: {st}', '; '.join(f"{r['name']} {r['subtype']}/{r['class']} {r['gin'].area:.0f} m2 in d10 ({r['gin'].centroid.x:.0f},{r['gin'].centroid.y:.0f})" for r in hits[:4]) or 'none')
gar = [r for r in LU if r['class'] in ('garages', 'parking', 'depot') or r['subtype'] == 'transportation']
claim('5.yards', 'truck yards at (12749, 9397) and (12375, 9467)', '; '.join(f"{r['name'] or '-'} {r['subtype']}/{r['class']} {r['gin'].area:.0f} m2 ({r['gin'].centroid.x:.0f},{r['gin'].centroid.y:.0f})" for r in sorted(gar, key=lambda r: -r['gin'].area)[:5]))

# ---- section 4 table: lat/lon to game, and Overture rows
print('== Section 4: landmarks')
rows = [('Lagos Port Complex', 6.4424, 3.3790, (13793, 9068)), ('APM Terminals', 6.4411, 3.3801, (13836, 9116)), ('TICT', 6.4349, 3.3476, (12638, 9342)),
        ('Tinubu station', 6.4520, 3.3689, (13421, 8713)), ('Amusement Park', 6.4439, 3.3664, (13330, 9012)), ('Apapa Club', 6.4478, 3.3619, (13163, 8868)),
        ('Apapa Mall', 6.4474, 3.3630, (13204, 8884)), ("Shippers'", 6.4470, 3.3650, (13278, 8899)), ('Flour Mills', 6.4465, 3.3743, (13621, 8917)),
        ('General Hospital', 6.4420, 3.3688, (13419, 9081)), ('LG secretariat', 6.4373, 3.3672, (13361, 9256)), ('Central Mosque', 6.4377, 3.3674, (13366, 9241)),
        ('Sacred Heart', 6.4384, 3.3623, (13179, 9214)), ('Methodist', 6.4395, 3.3666, (13337, 9175)), ("St Andrew's", 6.4406, 3.3551, (12914, 9135)),
        ('Liverpool Bridge', 6.4360, 3.3616, (13154, 9304)), ('Liverpool jetty', 6.4391, 3.3591, (13063, 9191)), ('Boat Club', 6.4378, 3.3617, (13157, 9238)),
        ('NPA Gate', 6.4346, 3.3600, (13095, 9354)), ('Marine Bridge bus stop', 6.4560, 3.3641, (13244, 8565)), ('Western Naval', 6.4620, 3.3714, (13515, 8347)),
        ('Navy base', 6.4565, 3.3673, (13364, 8549)), ('AP/NOC depot', 6.4630, 3.3659, (13311, 8307)), ('Oando depot', 6.4597, 3.3597, (13083, 8430)),
        ('Ijora Central Mosque', 6.4670, 3.3662, (13321, 8159)), ('Ijora Badia Market', 6.4668, 3.3634, (13217, 8170)), ('Ijora Oloye school', 6.4684, 3.3663, (13326, 8109)),
        ('waterside N', 6.4461, 3.3505, (12744, 8931)), ('waterside S', 6.4410, 3.3486, (12674, 9118)), ('Sagbokoji', 6.4328, 3.3769, (13719, 9422)),
        ('Ilado', 6.4323, 3.3796, (13816, 9438))]
for nm, lat, lon, st in rows:
    xy = gidi(lon, lat)
    claim('4.xy', f'{nm} {lat},{lon} -> {st}', f'({xy[0]:.0f}, {xy[1]:.0f}) in d{where(xy)}, {D10.distance(Point(xy)):.1f} m from d10', pt_ok(xy, st, 4) and D10.distance(Point(xy)) < 2)
for pat, conf in [('APM|Lagos Port Complex|Port of Apapa', None), ('TICT|Tin Can Island Container', None), ('Tinubu|Apapa (Railway )?Station', None),
                  ('Amusement', None), ('Apapa Club', None), ('Apapa Mall', 0.98), ('Shippers', None), ('Flour Mills', None), ('General Hospital', None),
                  ('Local Government|Secretariat', 0.95), ('Apapa Central Mosque', None), ('Sacred Heart', 0.99), ('Methodist', None), ("Andrew", None),
                  ('Boat Club', None), ('NPA Gate', 0.68), ('Marine Bridge', None), ('Navy|Naval', None), ('AP/NOC|Oando|depot', None),
                  ('Ijora Central Mosque', None), ('Ijora Badia', None), ('Ijora Oloye', None), ('Liverpool', None)]:
    hits = find(pat)
    ok = None
    if conf is not None and hits:
        ok = any(abs(p['conf'] - conf) < 0.006 for p in hits)
    claim('4.OV', f'/{pat}/' + (f' confidence {conf}' if conf else ''), show(hits), ok)
icm = find('Ijora Central Mosque')
claim('4.icm-cat', 'Ijora Central Mosque filed as a Christian place of worship', [(p['cat'], p['prim']) for p in icm])
bs = [p for p in P10 if p['cat'] == 'public_transit_facility_or_service' or p['prim'] in ('bus_station', 'bus_stop') or re.search('bus.?stop', p['name'], re.I)]
claim('4.busstop', 'the only named bus stop in Overture in d10 is Marine Bridge', show(bs) + f" (taxonomy {[p['prim'] for p in bs]})", len(bs) == 1)
claim('4.noise', '/Pacific Islands/ over the whole district', '; '.join(f"land use {r['name']} {r['gin'].area:.0f} m2 of {D10.area:.0f}" for r in LU if 'Pacific Islands' in r['name']),
      any('Pacific Islands' in r['name'] and r['gin'].area > 0.99 * D10.area for r in LU))
for pat in ['Badagry Divisional', 'Iju Ishaga', 'Zaranda', 'Jalingo', 'Ladipo Auto']:
    claim('4.noise', f'/{pat}/ inside d10', show(find(pat)), bool(find(pat)))
cats = collections.Counter(p['cat'] for p in P10)
claim('4.worship', '21 Christian, 17 religious organisations, 6 mosques', f"{cats['christian_place_of_worship']}, {cats['religious_organization']}, {cats['muslim_place_of_worship']}",
      (cats['christian_place_of_worship'], cats['religious_organization'], cats['muslim_place_of_worship']) == (21, 17, 6))
prims = collections.Counter(p['prim'] for p in P10)
claim('5.trades', '86 transport and storage firms, 14 shipping or delivery, 10 fuel stations (of 648)',
      f"cat: {[(k, v) for k, v in cats.most_common(8)]}; gas_station {cats['gas_station']}; taxonomy: {[(k, v) for k, v in prims.most_common(6)]}")

# ---- section 5/6 fabric from places.csv
print('== Section 5-6: fabric (places.csv)')
for nm, st in [('Apapa GRA', ('5.08', '1742', '72.0', '6.34', '0.083')), ('Apapa GRA north-east', ('1.46', '1340', '106.0', '8.55', None)),
               ('Apapa Wharf', ('1.3', '1208', '139.0', '7.43', None)), ('Apapa Wharf, east of Apapa-Oworonshoki Expressway', ('2.08', '740', '95.0', '13.68', '0.554')),
               ('Apapa GRA, south-west of Apapa-Oworonshoki Expressway', ('1.79', '944', '64.0', '12.1', '0.466')), ('Apapa Wharf south-east', ('1.6', '5603', '42.0', '4.2', '0.0'))]:
    r = PC[nm]
    got = (r['land_km2'], r['bldg_per_km2'], r['median_foot_m2'], r['height_m'], r['share4'] if st[4] else None)
    claim('5.fab', f'{nm}: land, bldg/km2, median, height, share4 = {st}', f"{got}, fabric {r['fabric']}, big {r['big_share']}, poi/km2 {r['poi_per_km2']}", got == st)
poi = {n: float(PC[n]['poi_per_km2']) for n in names6}
claim('5.poi', 'Apapa Wharf the highest places density of the six (110/km2)', poi, max(poi, key=poi.get) == 'Apapa Wharf')
aj = [r for r in PC.values() if r['name'].startswith('Ajegunle')]
claim('6.aj', 'Ajegunle 2,976 buildings/km2, 127 m2 median', [(r['name'], r['bldg_per_km2'], r['median_foot_m2']) for r in aj])

print('== Repo documents cited')
def has(path, pat, cid, stated, lines=None):
    t = open(os.path.join(GIDI, path)).read().split('\n')
    if lines:
        t = t[lines[0] - 1:lines[1]]
    hit = [x for x in t if re.search(pat, x, re.I)]
    claim(cid, f'{path}: {stated}', (hit[0][:160] + ('...' if len(hit[0]) > 160 else '')) if hit else 'not found', bool(hit))
EC, LIV, LGA, NM = 'docs/lagos-study/roads/EARTH-CHECK.md', 'docs/lagos-study/LIVING.md', 'docs/lagos-lgas-research.md', 'docs/lagos-study/roads/NAMES.md'
has(EC, r'^\| 10 \| Apapa \|.*West canal; harbour; Ijora to the north', 'EC.d10', 'members GRA + Wharf; west canal, harbour, Ijora north')
has(EC, r'^\| 8 \|.*Tin Can goes with Kirikiri as the western port. Ijora Badia goes north with Ijora', 'EC.8', 'row 8: Tin Can with Kirikiri; Ijora Badia north')
has(EC, r'^\| 13 \|.*Apapa west canal', 'EC.13', 'row 13: the Apapa west canal')
has(NM, r'\| 10 \| Apapa \| Àpapọ̀ .*everything gathered together', 'NAMES', 'Àpapọ̀ "everything gathered together"')
has(NM, r'\| 8 \| Kirikiri-Tin Can \| Kẹ́rẹ́kẹ́rẹ́-Tin Pan', 'NAMES8', 'd08 Kẹ́rẹ́kẹ́rẹ́-Tin Pan')
has(LIV, r'10\. Apapa .*B in the GRA, D in Badia and under the bridges', 'LIV.10', 'sheet 10 grade')
has(LIV, r'the GRA almost empty on foot', 'LIV.foot', 'GRA almost empty on foot')
has(LIV, r'50k/km² measured, the densest', 'LIV.aj', 'Ajegunle 50k/km2')
has(LIV, r'badly under-counts mosques', 'LIV.mosq', 'Overture under-counts mosques')
has(LIV, r'Kirikiri.*prison|the prison \[LGA\]', 'LIV.kk', 'Kirikiri: the prison')
has(LIV, r'Badia demolitions: the residents are never the villains', 'LIV.11', 'sheet 11 careful line')
has(LIV, r'banned in six councils from 1 June 2022.*Apapa', 'LIV.okada', 'okada ban 1 June 2022 incl. Apapa (second source for [S-OKB])')
has('docs/lagos-study/STUDY.md', r'Ladipo Auto Market" pin in Apapa', 'ST', 'ST noted the Ladipo pin')
LG = (1291, 1418)
has(LGA, r'^## Apapa LGA: research brief', 'LGA.head', 'brief starts line 1291 (note: lines 1291-1370)', (1291, 1291))
has(LGA, r'^## Ajeromi', 'LGA.end', 'next section starts (brief ends the line before)', (1419, 1419))
for cid, pat, st in [('LGA.1', r'built 1975.78', 'expressway built 1975-78'), ('LGA.2', r'Apapa Mall.*cinema', 'Apapa Mall has a cinema'),
                     ('LGA.3', r'Ijora Bridge, Marine Bridge, Liverpool Bridge, Coconut Bridge, the Apapa.Ijora.Costain bridge and Eko Bridge', 'six bridges named'),
                     ('LGA.4', r'choking smell of urine.*Creek Road', 'urine on Creek Road'), ('LGA.5', r'Tankers.*queue on Liverpool Road', 'tankers queue on Liverpool Road'),
                     ('LGA.6', r'maritime executives', 'maritime executives in the GRA'), ('LGA.7', r'APM Terminals\) ?since 2005|APM Terminals since 2005', 'APM Terminals since 2005'),
                     ('LGA.8', r'red zone', '2021 red zone under Liverpool Bridge'), ('LGA.9', r'2013 and 2015: forced evictions in Badia', 'Badia evictions 2013, 2015'),
                     ('LGA.10', r'ban on the Apapa axis around February 2020', 'okada ban ~Feb 2020'), ('LGA.11', r'Traffic robbers', 'robbers in the jams'),
                     ('LGA.12', r'touts, the "traffic managers"', 'touts, traffic managers'), ('LGA.13', r'drink, smoke', 'drinking under the bridge'),
                     ('LGA.14', r'Area B Police Command, the disused Apapa North railway station', 'Area B, Apapa North station, Military Hospital named'),
                     ('LGA.15', r'motor boy', 'motor boys (note cites [LGA][NM-MB])')]:
    has(LGA, pat, cid, st, LG)

print(f'\nTRUE {n_true}  FALSE {n_false}  CHECK (read the found value) {n_check}')
