"""The clean-up after a real-area build, by hand at each spot (owner: "clean up everything by hand"): reads the baked map and writes
hand edits into web/hand/<district>.json for every building the checks would flag, each fixed where it stands:
- past a road's building line, on a deck, over an open gutter or around a pole or light: the footprint is cut back (reshape), or the
  building goes if too little is left;
- two footprints overlapping: the smaller is cut back from the bigger;
- reached by no way within 45 m: it goes; a street piece of a few metres leading nowhere goes.
Usage: python3 scripts/hand_fix_checks.py hub "<who>"
"""
import json
import sys

from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

sys.path.insert(0, 'scripts')
import cross_sections as XS
from check_district import HALF

D = sys.argv[1]
WHO = sys.argv[2] if len(sys.argv) > 2 else 'Claude: clean-up after the checks'
G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
R = lambda xy: [round(xy[0], 1), round(xy[1], 1)]
DP = Polygon(next(d for d in G['districts'] if d['id'] == D)['poly'][0])
NEAR = DP.buffer(40)
L = lambda p: LineString(p) if len(p) > 1 else None
bad = []   # (shape, why)
for k, bl in (('streets', 'street'), ('lanes', 'lane')):
    for dd, ps in G[k].items():
        for p in ps:
            g = L(p)
            if g is not None and g.distance(DP) < 40:
                bad.append(g.buffer(XS.building_line(bl) - 0.05))
for m in G['mains']:
    g = L(m['pts'])
    if g is not None and g.distance(DP) < 40:
        bad.append(g.buffer(XS.building_line('main') - 0.05))
for a in G['arterials']:
    if a['cls'] in ('art', 'exp') and L(a['pts']).distance(DP) < 40:
        bad.append(L(a['pts']).buffer(XS.building_line(a['cls']) - 0.05))
bad.append(L(G['rail']['pts']).buffer(HALF['rail'] - 0.05))
for s in G.get('structures', []):
    if s['kind'] in ('flyover', 'skywalk', 'footbridge') and s.get('layer', 0) >= 1 and L(s['pts']).distance(DP) < 40:
        w = s.get('width'); bad.append(L(s['pts']).buffer(((w / 2) if w else (6 if s['kind'] == 'flyover' else 2)) - 0.05))
FURN = [Point(f['x'], f['y']) for f in G.get('furniture', []) if NEAR.contains(Point(f['x'], f['y']))]
for q in FURN:
    bad.append(q.buffer(0.4))
for b_ in G['buildings'][D]:   # a pole or light standing inside a footprint: a notch from it to the nearest wall, so the wall steps round it
    if len(b_) > 3:
        P_ = Polygon(b_[1:])
        for q in FURN:
            if P_.contains(q):
                e_ = P_.exterior.interpolate(P_.exterior.project(q)); dx, dy = e_.x - q.x, e_.y - q.y; n_ = (dx * dx + dy * dy) ** 0.5 or 1
                bad.append(LineString([(q.x - dx / n_ * 0.6, q.y - dy / n_ * 0.6), (e_.x + dx / n_ * 1.0, e_.y + dy / n_ * 1.0)]).buffer(0.6))
for r in G.get('gutters', []):
    if r.get('d') == D and r['state'] == 'open' and len(r['pts']) > 1:
        bad.append(L(r['pts']).buffer(0.1))
BAD = unary_union(bad)
SOFT = {'stalls', 'kiosk'}   # tables and kiosks may stand in the market spill (the checks allow them in declared zones)
B = G['buildings'][D]
E = []
polys = [Polygon(b[1:]) if len(b) > 3 else None for b in B]
cut = 0; gone = 0
for i, b in enumerate(B):
    P = polys[i]
    if P is None or b[0] in SOFT or not P.intersects(BAD):
        continue
    Q = P.difference(BAD)
    Q = max(getattr(Q, 'geoms', [Q]), key=lambda x: x.area) if not Q.is_empty else Q
    at = R(P.representative_point().coords[0])
    if Q.is_empty or Q.geom_type != 'Polygon' or Q.area < 6:
        E.append({'op': 'delete building', 'at': at, 'kind': b[0], 'note': 'past a building line, over a gutter or round a pole: too little left', 'by_who': WHO}); polys[i] = None; gone += 1
    else:
        E.append({'op': 'reshape building', 'at': at, 'kind': b[0], 'pts': [R(c) for c in list(Q.exterior.coords)[:-1]], 'note': 'cut back to the building line', 'by_who': WHO}); polys[i] = Q; cut += 1
# overlaps: the smaller gives way
idx = [i for i, P in enumerate(polys) if P is not None]
tree = STRtree([polys[i] for i in idx])
for a_, i in enumerate(idx):
    P = polys[i]
    if P is None:
        continue
    for b_ in tree.query(P):
        j = idx[int(b_)]
        if j <= i or polys[j] is None or polys[i] is None:
            continue
        if polys[i].intersection(polys[j]).area > 0.05:
            s_, l_ = (i, j) if polys[i].area < polys[j].area else (j, i)
            Q = polys[s_].difference(polys[l_].buffer(0.15))
            Q = max(getattr(Q, 'geoms', [Q]), key=lambda x: x.area) if not Q.is_empty else Q
            at = R(Polygon(B[s_][1:]).representative_point().coords[0])
            E = [e for e in E if not (e['op'] == 'reshape building' and e['at'] == at)]
            if Q.is_empty or Q.geom_type != 'Polygon' or Q.area < 6:
                E.append({'op': 'delete building', 'at': at, 'kind': B[s_][0], 'note': 'overlapped a bigger one', 'by_who': WHO}); polys[s_] = None; gone += 1
            else:
                E.append({'op': 'reshape building', 'at': at, 'kind': B[s_][0], 'pts': [R(c) for c in list(Q.exterior.coords)[:-1]], 'note': 'cut back from its neighbour', 'by_who': WHO}); polys[s_] = Q; cut += 1
# reach: no way within 45 m
W = [L(p) for k in ('streets', 'lanes', 'paths') for ps in (G.get(k) or {}).values() for p in ps] + [L(m['pts']) for m in G['mains']] + [L(a['pts']) for a in G['arterials']]
W = [w for w in W if w is not None and w.distance(DP) < 100]
wt = STRtree(W)
for i, P in enumerate(polys):
    if P is None or B[i][0] in SOFT:
        continue
    if len(wt.query(P.buffer(45))) == 0 or min(W[int(k)].distance(P) for k in wt.query(P.buffer(45))) > 44:
        E.append({'op': 'delete building', 'at': R(Polygon(B[i][1:]).representative_point().coords[0]), 'kind': B[i][0], 'note': 'reached by no way', 'by_who': WHO}); polys[i] = None; gone += 1
for p in G['streets'].get(D, []):
    g = L(p)
    if g is not None and g.length < 3:
        E.append({'op': 'delete street', 'at': R(g.interpolate(0.5, normalized=True).coords[0]), 'note': 'a scrap of street leading nowhere', 'by_who': WHO})
path = f'web/hand/{D}.json'
H = json.load(open(path))
H['edits'] = H.get('edits', []) + E
json.dump(H, open(path, 'w'), separators=(',', ':'), ensure_ascii=False)
print(D, len(E), 'edits:', cut, 'cut back,', gone, 'gone')
