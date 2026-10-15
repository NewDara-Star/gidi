# The v2 frame's shared roads (docs/LAYOUT-V2.md): every district border becomes one named road, drawn once here, so districts can be
# generated side by side and still meet exactly. Reads web/layout-v2.json (districts already cut from one partition, so neighbours
# share their border vertex for vertex) and writes web/network.json:
#   edges: {key: {"between": [a, b or null], "kind": ..., "name": ..., "pts": [...]}}
#     kind "border"    a road between two districts (a main road, named)
#          "arterial"  the border already runs along an arterial: the arterial is the border, no second road (name = the arterial's)
#          "shore"     a district's edge on the water: a footpath and the waterline, not a road
#          "edge"      a district's edge on the bush, where the city ends: a track
#   gateways: [] (each district keeps its own crossings in its generated file; nothing here is written by the generator)
# Usage: python3 scripts/frame_network.py
import json, random
from shapely.geometry import Polygon, LineString, MultiLineString, Point
from shapely.ops import unary_union, linemerge

L = json.load(open('web/layout-v2.json'))
P = {k: Polygon(v) for k, v in L['districts'].items()}
water = unary_union([Polygon(w).buffer(0) for w in L['water']] + [Polygon(L['ocean']).buffer(0)])
ARTS = [(a['name'], LineString(a['pts'])) for a in L['arterials'] if a['cls'] != 'bridge']
rnd = random.Random(2610)
FIRST = ['Adewale', 'Babatunde', 'Chukwuma', 'Ekpo', 'Gbadamosi', 'Ige', 'Jimoh', 'Kolawole', 'Lateef', 'Mbanefo', 'Popoola', 'Raji', 'Sanni',
         'Tijani', 'Udoh', 'Wahab', 'Yusuf', 'Akinola', 'Bamidele', 'Egbe', 'Hassan', 'Ikenna', 'Kunle', 'Mojeed', 'Nwachukwu', 'Remi', 'Segun',
         'Tokunbo', 'Uche', 'Yemi', 'Aremu', 'Bolaji', 'Dosunmu', 'Fashola', 'Gbenga', 'Ilesanmi', 'Jaiyeola', 'Kasumu', 'Laniyan', 'Makinde',
         'Odunsi', 'Pedro', 'Quadri', 'Sowande', 'Taiwo', 'Usman', 'Vaughan', 'Williams', 'Animashaun', 'Coker']
ART_FIRST = {n.split()[0] for n, g in ARTS}
used = set()


def name():
    for _ in range(500):
        f = rnd.choice(FIRST)
        if f in ART_FIRST or f in used:
            continue
        used.add(f)
        return f"{f} {rnd.choices(['Road', 'Avenue', 'Street', 'Way'], [6, 2, 2, 1])[0]}"
    raise SystemExit('ran out of border road names')


def lines(g):
    g = linemerge(g) if g.geom_type in ('MultiLineString', 'GeometryCollection') and not g.is_empty else g
    return [x for x in getattr(g, 'geoms', [g]) if x.geom_type == 'LineString' and x.length > 1]


def along_arterial(ln):
    """The arterial this border runs along (most of its length within 45 m), if any."""
    for n, a in ARTS:
        if ln.length > 0 and a.buffer(45).intersection(ln).length > 0.7 * ln.length:
            return n
    return None


ks = sorted(P)


def runs_of(a):
    """Walk district a's outline segment by segment and label each: the neighbour it borders, or water / bush. Consecutive segments
    with one label make a run; a water/bush flicker shorter than 80 m takes its neighbours' label."""
    cs = list(P[a].exterior.coords)[:-1]
    segs = []
    for i in range(len(cs)):
        p, q = cs[i], cs[(i + 1) % len(cs)]
        m = Point((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        nb = next((b for b in ks if b != a and P[b].boundary.distance(m) < 0.05), None)
        segs.append([nb or ('~water' if water.distance(m) < 25 else '~bush'), p, q])
    def group(segs):
        out = []
        for lab, p, q in segs:
            if out and out[-1][0] == lab:
                out[-1][1].append(q)
            else:
                out.append([lab, [p, q]])
        return out
    # start the walk at a label change, so no run wraps round the start
    k0 = next((i for i in range(len(segs)) if segs[i][0] != segs[i - 1][0]), 0)
    segs = segs[k0:] + segs[:k0]
    R_ = group(segs)
    for _ in range(3):
        for i, (lab, pts) in enumerate(R_):
            if lab.startswith('~') and LineString(pts).length < 80 and len(R_) > 2:
                L_, N_ = R_[i - 1][0], R_[(i + 1) % len(R_)][0]
                if L_.startswith('~') and L_ == N_:
                    R_[i][0] = L_
        R_ = group([[lab, p, q] for lab, pts in R_ for p, q in zip(pts, pts[1:])])
    return R_


E = {}
done = {}
for a in ks:
    k = 0
    for lab, pts in runs_of(a):
        g = LineString(pts)
        if not lab.startswith('~'):
            pair = tuple(sorted([a, lab]))
            if a != pair[0]:
                continue   # drawn once, from the first district of the pair
            j = done.get(pair, 0); done[pair] = j + 1
            key = f'{pair[0]}|{pair[1]}' + (f'#{j + 1}' if j else '')
            art = along_arterial(g)
            wet = g.buffer(1).intersection(water).area / max(g.buffer(1).area, 1) > 0.5
            kind = 'arterial' if art else 'shore' if wet else 'border'
            E[key] = {'between': list(pair), 'kind': kind, 'name': art or (None if kind == 'shore' else name()),
                      'pts': [[round(x, 1), round(y, 1)] for x, y in g.simplify(1.0).coords]}
        else:
            art = along_arterial(g)
            kind = 'arterial' if art else 'shore' if lab == '~water' else 'edge'
            E[f'{a}|{kind}{k}'] = {'between': [a, None], 'kind': kind, 'name': art,
                                   'pts': [[round(x, 1), round(y, 1)] for x, y in g.simplify(1.0).coords]}
            k += 1
# ends that meet (within half a metre: the two outlines' vertices round differently) are snapped to one point, so every ring closes
nodes = []
for e in E.values():
    for i in (0, -1):
        p = e['pts'][i]
        hit = next((n for n in nodes if abs(n[0] - p[0]) < 0.5 and abs(n[1] - p[1]) < 0.5), None)
        if hit is None:
            nodes.append(p)
        else:
            e['pts'][i] = list(hit)
json.dump({'frame': 'v2', 'edges': E, 'gateways': []}, open('web/network.json', 'w'), indent=1)
from collections import Counter
c = Counter(e['kind'] for e in E.values())
print(len(E), 'edges:', dict(c), '| km:', {k: round(sum(LineString(e['pts']).length for e in E.values() if e['kind'] == k) / 1000, 1) for k in c})
# every district's edges must close into its own outline
from shapely.ops import polygonize
for a in ks:
    ring = unary_union([LineString(e['pts']) for e in E.values() if a in e['between']])
    poly = max(polygonize(ring), key=lambda p: p.area, default=None)   # the rounded points close to within centimetres
    ok = poly is not None and abs(poly.area - P[a].area) / P[a].area < 0.01
    if not ok:
        print('  NOT CLOSED:', a, round(poly.area / P[a].area, 3) if poly else None)
