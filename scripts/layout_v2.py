# Gidi v2 layout (owner's choice, 15 Oct 2026): a fictional Lagos at ONE even scale, 1:4 (docs/LAYOUT-V2.md).
# District positions = their inspirations' real positions (study-area centroids) / SCALE, no turning, nothing squeezed.
# Coasts, the lagoon, the harbour, creeks, district borders and the arterials are drawn fresh here, never traced.
# Writes web/layout-v2.json (the map's frame: size, water, districts, arterials, rail) and a preview picture.
# Usage: python3 scripts/layout_v2.py [preview.png]
import math, sys
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, MultiPoint, LineString, box
from shapely.ops import unary_union, voronoi_diagram

SCALE = 4.0
REAL = {'border': (0, 4.4), 'bazaar': (14.9, 2.6), 'railside': (21.9, 16.1), 'airport': (27.9, 15.1), 'hub': (28.3, 8.4), 'jungle': (29.5, 1.4),
        'capital': (31.1, 18.2), 'port': (32.4, 0.0), 'maze': (32.8, 9.8), 'estate': (33.2, 18.8), 'yaba': (34.2, 8.6), 'watertown': (36.6, 7.4),
        'foodgate': (35.9, 17.5), 'oldisland': (36.4, 1.6), 'heights': (40.1, 0.2), 'oldshore': (47.8, 18.9), 'frontier': (63.4, 2.0)}
M = 1500   # margin, metres
W = int(63.4 / SCALE * 1000 + 2 * M + 800); H = int(18.9 / SCALE * 1000 + 2 * M + 1600)
X = lambda e: M + e / SCALE * 1000
Y = lambda n: H - M - 1200 - n / SCALE * 1000          # y runs south: the sea below, the bush above
anchor = {k: (X(e), Y(n)) for k, (e, n) in REAL.items()}


def chaikin(pts, n=4):
    p = np.array(pts, float)
    for _ in range(n):
        q = np.roll(p, -1, axis=0)
        new = np.empty((len(p) * 2, 2)); new[0::2] = 0.75 * p + 0.25 * q; new[1::2] = 0.25 * p + 0.75 * q
        p = new
    return [tuple(x) for x in p]


ax_, ay_ = lambda k: anchor[k][0], lambda k: anchor[k][1]
km = 1000 / SCALE   # one real km in Gidi metres
coast_y = Y(-0.9)   # the ocean beach runs just south of the Port, the Island and the Heights
OCEAN = chaikin([(-500, coast_y + 300), (X(10), coast_y + 150), (X(25), coast_y + 250), (X(32), coast_y + 80), (X(36), coast_y + 300), (X(45), coast_y + 120),
                 (X(64), coast_y), (W + 500, coast_y), (W + 500, H + 500), (-500, H + 500)])
# the lagoon: east of Yaba and Water Town, north of the Island strip, south of the north shore (Ikorodu)
LAGOON = chaikin([(X(37.5), Y(1.9)), (X(37.0), Y(4.5)), (X(37.6), Y(8.5)), (X(38.4), Y(12.5)), (X(41), Y(15.2)), (X(46), Y(15.6)), (X(55), Y(14.2)),
                  (X(66), Y(12.5)), (W + 500, Y(12)), (W + 500, Y(4.2)), (X(62), Y(4.3)), (X(50), Y(3.6)), (X(43), Y(3.0)), (X(40.5), Y(2.6))])
HARBOUR = chaikin([(X(33.4), Y(3.2)), (X(34.9), Y(3.4)), (X(35.1), Y(1.2)), (X(34.9), Y(-1.2)), (X(33.9), Y(-1.2)), (X(33.8), Y(0.6))])   # west of the Island
CREEK_E = chaikin([(X(38.8), Y(2.8)), (X(39.3), Y(2.8)), (X(39.2), Y(-1.0)), (X(38.7), Y(-1.0))])                                     # east of the Island
CREEK_W = chaikin([(-500, Y(1.6)), (X(6), Y(2.6)), (X(14), Y(1.4)), (X(18), Y(0.9)), (X(14), Y(0.6)), (X(6), Y(1.4)), (-500, Y(0.4))])  # Badagry creek
water = unary_union([Polygon(x).buffer(0) for x in (OCEAN, LAGOON, HARBOUR, CREEK_E, CREEK_W)])
land = box(0, 0, W, H).difference(water)
# where the built city ends (bush and farms beyond): a fresh outline round the districts
hull = MultiPoint([Point(*v) for v in anchor.values()]).convex_hull.buffer(2.6 * km, quad_segs=8)
city = hull.intersection(land)

ids = list(anchor)
vd = voronoi_diagram(MultiPoint([Point(*anchor[k]) for k in ids]), envelope=box(-W, -H, 2 * W, 2 * H))
cells = {min(ids, key=lambda k: p.distance(Point(*anchor[k]))): p for p in vd.geoms}


def bend(poly, amp, seed=7):
    rng = np.random.RandomState(seed); ph = rng.uniform(0, 6.28, 6); L = 900 / SCALE * 2.5
    f = lambda x, y: (amp * (math.sin(x / L + ph[0]) * math.cos(y / (1.2 * L) + ph[1]) + .5 * math.sin(x / (.45 * L) + y / (.55 * L) + ph[2])),
                      amp * (math.cos(x / (1.1 * L) + ph[3]) * math.sin(y / (.9 * L) + ph[4]) + .5 * math.cos(x / (.5 * L) - y / (.42 * L) + ph[5])))
    ring = LineString(poly.exterior.coords).segmentize(60)
    return Polygon([(x + f(x, y)[0], y + f(x, y)[1]) for x, y in ring.coords]).buffer(0)


D = {}
for k in ids:
    P = bend(cells[k], 0.18 * km).intersection(city)
    D[k] = max(getattr(P, 'geoms', [P]), key=lambda g: g.area)
names = {'border': 'The Border', 'bazaar': 'The Bazaar', 'railside': 'Railside', 'airport': 'THE AIRPORT (new)', 'hub': 'The Hub', 'jungle': 'Jungle City',
         'capital': 'The Capital', 'port': 'The Port', 'maze': 'The Maze', 'estate': 'The Estate', 'yaba': 'YABA/AKOKA (new)', 'watertown': 'Water Town',
         'foodgate': 'Food Gate', 'oldisland': 'Old Island', 'heights': 'The Heights', 'oldshore': 'Old Shore', 'frontier': 'The Frontier'}
# ---- the arterials and the rail, drawn by hand between the districts (each plays its real counterpart's part)
P_ = lambda k, dx=0, dy=0: (anchor[k][0] + dx, anchor[k][1] + dy)
ART = [
    ('Coastal Expressway', 'exp', [(0, Y(3.4)), (X(4), Y(3.3)), (X(9), Y(3.2)), (X(14.9), Y(3.0)), (X(20), Y(2.6)), (X(24), Y(2.2)), P_('jungle', -200, 250), (X(31.2), Y(0.6))]),   # inland of the creek
    ('Ring Road', 'exp', [(X(31.6), Y(0.4)), (X(30.6), Y(3.6)), P_('hub', 150, 300), (X(28.6), Y(11.5)), P_('airport', 300, 450)]),
    ('Ayinde Avenue', 'art', [P_('hub', 0, 0), (X(29.4), Y(11.8)), P_('airport', 900, -50), P_('capital', -100, 300), P_('estate', -200, -250)]),
    ('Northern Road', 'art', [P_('yaba', -120, 80), (X(34.6), Y(12.6)), P_('foodgate', -200, 300), (X(38.5), Y(19.2)), (X(43), Y(19.6)), P_('oldshore', 0, 250), (X(56), Y(18.6))]),
    ('Agege Road', 'art', [P_('capital', -300, 500), (X(26), Y(15.8)), P_('railside', 0, 0), (X(16), Y(13.8))]),
    ('The Long Bridge', 'bridge', [(X(36.3), Y(8.9)), (X(39.0), Y(8.6)), (X(40.4), Y(7.0)), (X(40.4), Y(4.6)), (X(39.0), Y(3.0)), (X(37.0), Y(2.3))]),   # out over the lagoon
    ('Wharf Bridge', 'bridge', [(X(33.0), Y(2.3)), (X(34.4), Y(2.4)), (X(35.9), Y(2.2))]),   # across the harbour
    ('Waterfront Drive', 'art', [(X(36.0), Y(1.6)), (X(38.4), Y(1.3))]),
    ('Creek Bridge', 'bridge', [(X(38.4), Y(1.3)), (X(39.6), Y(1.1))]),   # over the creek between the Island and the Heights
    ('Waterfront Drive East', 'art', [(X(39.6), Y(1.1)), P_('heights', 0, 0)]),
    ('Peninsula Expressway', 'exp', [P_('heights', 0, 0), (X(47), Y(1.3)), (X(55), Y(1.6)), P_('frontier', 0, 200), (W, Y(2.4))]),
]
RAIL = [P_('railside', -300, -500), (X(26.5), Y(14)), (X(28.0), Y(10.5)), P_('hub', 250, -200), P_('maze', 0, 250), (X(34.0), Y(7.2)), (X(34.5), Y(4.2)), (X(34.6), Y(2.6))]

if __name__ == '__main__':
    import json as _json
    out = {'scale': SCALE, 'size': [W, H], 'note': 'Gidi v2 frame (scripts/layout_v2.py): positions from real Lagos at 1:4; all shapes drawn fresh',
           'water': [[[round(x, 1), round(y, 1)] for x, y in g.exterior.coords] for g in getattr(water, 'geoms', [water])],
           'districts': {k: [[round(x, 1), round(y, 1)] for x, y in v.exterior.coords] for k, v in D.items()},
           'anchors': {k: [round(v[0]), round(v[1])] for k, v in anchor.items()},
           'arterials': [{'name': n, 'cls': c, 'pts': [[round(x, 1), round(y, 1)] for x, y in pts]} for n, c, pts in ART],
           'rail': {'name': 'Gidi Rail', 'pts': [[round(x, 1), round(y, 1)] for x, y in RAIL]}}
    _json.dump(out, open('web/layout-v2.json', 'w'), separators=(',', ':'))

fig, ax = plt.subplots(figsize=(18, 18 * H / W + 1))
ax.fill(*box(0, 0, W, H).exterior.xy, color='#cfdcb8')
for g in getattr(water, 'geoms', [water]):
    ax.fill(*g.exterior.xy, color='#a9cbe6')
cols = plt.cm.tab20(np.linspace(0, 1, len(ids)))
for (k, P), c in zip(D.items(), cols):
    ax.fill(*P.exterior.xy, color=c, alpha=.6 if k not in ('airport', 'yaba') else .9, ec='#333', lw=1)
    q = P.representative_point()
    ax.text(q.x, q.y, f"{names[k]}\n{P.area / 1e6:.1f} km²", ha='center', va='center', fontsize=7.5, fontweight='bold' if k in ('airport', 'yaba') else 'normal')
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.set_aspect('equal')
ax.set_title(f'Gidi v2 at 1:{SCALE:.0f}: {W / 1000:.1f} x {H / 1000:.1f} km. Districts where their inspirations sit in Lagos; coasts, borders and arterials drawn fresh', fontsize=10)
for n, c, pts in ART:
    xs, ys = zip(*pts); ax.plot(xs, ys, color={'exp': '#922b21', 'art': '#c0392b', 'bridge': '#1b2631'}[c], lw={'exp': 3.2, 'art': 2.2, 'bridge': 3.0}[c])
    m = pts[len(pts) // 2]; ax.text(m[0], m[1] - 120, n, fontsize=7, color='#641e16', ha='center', fontweight='bold')
xs, ys = zip(*RAIL); ax.plot(xs, ys, 'k--', lw=1.6); ax.text(RAIL[1][0] - 200, RAIL[1][1], 'Rail', fontsize=8)
plt.tight_layout(); plt.savefig(sys.argv[1] if len(sys.argv) > 1 else 'docs/img/layout-v2.png', dpi=60)
print(f'{W / 1000:.1f} x {H / 1000:.1f} km;', {k: round(v.area / 1e6, 1) for k, v in D.items()})
