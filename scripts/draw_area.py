"""One Ìbùdó area side by side with its real place, at the same scale and frame: the map as baked (left) and the real footprints and
roads it was built from (right: Google Open Buildings v3, Overture Maps; drawn here to compare, never put in the map). For the match
check (scripts/check_real.py) and the checker agent's eyes. Usage: python3 scripts/draw_area.py <area> <out.png>"""
import csv
import gzip
import json
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pyarrow.parquet as pq
from shapely import wkb, wkt
from shapely.geometry import LineString, Point, Polygon

A, OUT = sys.argv[1], sys.argv[2]
DATA = os.path.expanduser('~/Real-world/research/data')
T_ = json.load(open(f'docs/hand/ibudo/twins/{A}.json'))
AREA = Polygon(T_['area_pts'])
(LA0, LO0), (GX0, GY0) = T_['anchor_real'], T_['anchor_gidi']
M_LAT, M_LON = 110600.0, 109900.0
T = lambda lo, la: (GX0 + (lo - LO0) * M_LON, GY0 - (la - LA0) * M_LAT)
x0, y0, x1, y1 = AREA.buffer(30).bounds
s = open('web/gidi-data.js').read(); G = json.loads(s[len('window.GIDI='):-1])
WCOL = {'main': ('#d9822b', 3.0), 'street': ('#555', 1.6), 'lane': ('#888', 0.9), 'path': ('#5a9', 0.6), 'art': ('#c33', 4), 'exp': ('#c33', 5)}
fig, axs = plt.subplots(1, 2, figsize=(18, 9 * (y1 - y0) / (x1 - x0) + 1))
for ax, title in zip(axs, (f'Gidi: {A} (as baked)', f'The real place it is the child of')):
    ax.set_title(title, loc='left'); ax.set_aspect('equal'); ax.set_xlim(x0, x1); ax.set_ylim(y1, y0); ax.axis('off')
    ax.plot(*AREA.exterior.xy, color='#36c', lw=1, ls='--')
ax = axs[0]
for b in G['buildings']['hub']:
    if len(b) > 3:
        P = Polygon(b[1:])
        if P.intersects(AREA.buffer(30)):
            ax.fill(*P.exterior.xy, fc='#b9a48a' if b[0] != 'kiosk' else '#6e8fb0', ec='#6b5a45', lw=0.3)
for k, kk in (('streets', 'street'), ('lanes', 'lane'), ('paths', 'path')):
    for p in (G.get(k) or {}).get('hub', []):
        if len(p) > 1 and LineString(p).intersects(AREA.buffer(30)):
            ax.plot(*zip(*p), color=WCOL[kk][0], lw=WCOL[kk][1])
for m in G['mains'] + G['arterials']:
    if len(m['pts']) > 1 and LineString(m['pts']).intersects(AREA.buffer(30)):
        c, w = WCOL.get(m.get('cls', 'main'), WCOL['main']); ax.plot(*zip(*m['pts']), color=c, lw=w)
for p in G['pois']:
    if AREA.contains(Point(p['x'], p['y'])):
        ax.plot(p['x'], p['y'], 'o', ms=4, color='#c22'); ax.text(p['x'] + 4, p['y'], p['type'], fontsize=6, color='#c22')
ax = axs[1]
from_ll = lambda c: T(*c)
N_, S_ = LA0 - (y0 - GY0) / M_LAT, LA0 - (y1 - GY0) / M_LAT
W_, E_ = LO0 + (x0 - GX0) / M_LON, LO0 + (x1 - GX0) / M_LON
with gzip.open(f'{DATA}/open-buildings-v3/lagos_open_buildings_v3.csv.gz', 'rt') as f:
    for r in csv.DictReader(f):
        la, lo = float(r['latitude']), float(r['longitude'])
        if S_ <= la <= N_ and W_ <= lo <= E_ and float(r['confidence']) >= 0.65:
            g = wkt.loads(r['geometry'])
            for pg in getattr(g, 'geoms', [g]):
                ax.fill(*zip(*[from_ll(c) for c in pg.exterior.coords]), fc='#c9c2b5', ec='#7a7266', lw=0.3)
t = pq.read_table(f'{DATA}/overture-lagos/lagos_overture_segment.parquet', columns=['subtype', 'class', 'geometry', 'bbox'])
KIND = {'motorway': 'exp', 'trunk': 'art', 'primary': 'main', 'secondary': 'main', 'tertiary': 'street', 'residential': 'street', 'unclassified': 'street',
        'living_street': 'street', 'service': 'lane', 'track': 'lane', 'unknown': 'lane', 'footway': 'path', 'path': 'path', 'pedestrian': 'path', 'steps': 'path'}
for sub, cl, g, b in zip(*(t.column(c).to_pylist() for c in ('subtype', 'class', 'geometry', 'bbox'))):
    if sub == 'road' and cl in KIND and b['xmax'] >= W_ and b['xmin'] <= E_ and b['ymax'] >= S_ and b['ymin'] <= N_:
        c, w = WCOL[KIND[cl]]; ax.plot(*zip(*[from_ll(q) for q in wkb.loads(g).coords]), color=c, lw=w)
plt.tight_layout(); plt.savefig(OUT, dpi=110)
print(OUT)
