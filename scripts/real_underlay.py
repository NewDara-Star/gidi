"""The real place under each Ìbùdó area, for the drawing board's "Real place" layer: the real footprints (Google Open Buildings v3) and
roads (Overture) each area is the child of, placed by that area's own anchor (docs/hand/ibudo/twins/<area>.json) and kept to the area.
A study aid to move Gidi's buildings onto their real spots by hand; never map data, never committed (web/real-underlay.js is ignored).

  python3 scripts/real_underlay.py      writes web/real-underlay.js (needs ~/Real-world)
"""
import csv
import glob
import gzip
import json
import os

import pyarrow.parquet as pq
from shapely import wkb, wkt
from shapely.geometry import LineString, Polygon
from shapely.prepared import prep

DATA = os.path.expanduser('~/Real-world/research/data')
M_LAT, M_LON = 110600.0, 109900.0
KIND = {'motorway': 'exp', 'trunk': 'art', 'primary': 'main', 'secondary': 'main', 'tertiary': 'street', 'residential': 'street', 'unclassified': 'street',
        'living_street': 'street', 'service': 'lane', 'track': 'lane', 'unknown': 'lane', 'footway': 'path', 'path': 'path', 'pedestrian': 'path', 'steps': 'path'}
R1 = lambda c: [round(c[0], 1), round(c[1], 1)]

AREAS = []
for tf in sorted(glob.glob('docs/hand/ibudo/twins/*.json')):
    T_ = json.load(open(tf))
    if 'area_wkt' not in T_:
        continue
    A = wkt.loads(T_['area_wkt']); (LA0, LO0), (GX0, GY0) = T_['anchor_real'], T_['anchor_gidi']
    x0, y0, x1, y1 = A.bounds
    box = (LA0 - (y1 - GY0) / M_LAT, LA0 - (y0 - GY0) / M_LAT, LO0 + (x0 - GX0) / M_LON, LO0 + (x1 - GX0) / M_LON)   # south, north, west, east
    T = (lambda LA0, LO0, GX0, GY0: lambda lo, la: (GX0 + (lo - LO0) * M_LON, GY0 - (la - LA0) * M_LAT))(LA0, LO0, GX0, GY0)
    AREAS.append((T_['area'], A, prep(A), box, T))

out = {'b': [], 'r': []}
with gzip.open(f'{DATA}/open-buildings-v3/lagos_open_buildings_v3.csv.gz', 'rt') as f:
    for r in csv.DictReader(f):
        if float(r['confidence']) < 0.65:
            continue
        la, lo = float(r['latitude']), float(r['longitude'])
        for name, A, PA, (s_, n_, w_, e_), T in AREAS:
            if s_ <= la <= n_ and w_ <= lo <= e_:
                g = wkt.loads(r['geometry'])
                for pg in getattr(g, 'geoms', [g]):
                    P = Polygon([T(*c) for c in pg.exterior.coords])
                    if PA.contains(P.centroid):
                        out['b'].append([R1(c) for c in P.exterior.coords[:-1]])
t = pq.read_table(f'{DATA}/overture-lagos/lagos_overture_segment.parquet', columns=['subtype', 'class', 'geometry', 'bbox'])
for sub, cl, g, b in zip(*(t.column(c).to_pylist() for c in ('subtype', 'class', 'geometry', 'bbox'))):
    if sub != 'road' or cl not in KIND:
        continue
    for name, A, PA, (s_, n_, w_, e_), T in AREAS:
        if b['xmax'] >= w_ and b['xmin'] <= e_ and b['ymax'] >= s_ and b['ymin'] <= n_:
            L = LineString([T(*c) for c in wkb.loads(g).coords]).intersection(A)
            for part in getattr(L, 'geoms', [L]):
                if part.geom_type == 'LineString' and part.length > 1:
                    out['r'].append({'k': KIND[cl], 'pts': [R1(c) for c in part.coords]})
open('web/real-underlay.js', 'w').write('window.REAL=' + json.dumps(out, separators=(',', ':')) + ';')
print(len(out['b']), 'real footprints,', len(out['r']), 'real road pieces, for', len(AREAS), 'areas -> web/real-underlay.js')
