# Structure study of a district's inspiration from Google Open Buildings v3 (outlines) and OSM (streets), and the same
# measures on Gidi's district, square by square (scripts/structure.py). Also Overture's places and street furniture per km2.
# Usage: python3 scripts/study_structure.py foodgate 3.370,6.580,3.415,6.620  -> docs/data/structure-<id>.json, table
# Needs study-<id>.pkl (OSM streets, markets), the Lagos cut of Open Buildings v3, Overture's Lagos files, web/gidi-data.js.
import csv, gzip, json, os, pickle, sys
import numpy as np
from shapely import wkt
from shapely.geometry import box, Polygon, LineString, Point
from shapely.ops import transform
from pyproj import Transformer
sys.path.insert(0, os.path.dirname(__file__))
from structure import measure

DID = sys.argv[1]
W_, S_, E_, N_ = map(float, sys.argv[2].split(','))
DATA = os.path.expanduser('~/Real-world/research/data')
SQ = 500.0
tr = Transformer.from_crs(4326, 32631, always_xy=True).transform
WID = {'motorway': 30, 'trunk': 24, 'primary': 18, 'secondary': 14, 'tertiary': 10, 'unclassified': 7, 'residential': 7,
       'living_street': 6, 'service': 4, 'track': 4, 'pedestrian': 4}

D = pickle.load(open(f'study-{DID}.pkl', 'rb'))
A = D['area']
streets = [(g, WID[t.get('highway')]) for t, g in D['roads'] if t.get('highway') in WID]
markets = [g for t, g in D['landuse'] if t.get('amenity') == 'marketplace' and g.area > 5000]
print(f'{DID}: {len(streets)} OSM ways, {len(markets)} markets', flush=True)

G = []
with gzip.open(f'{DATA}/open-buildings-v3/lagos_open_buildings_v3.csv.gz', 'rt') as fh:
    r = csv.reader(fh)
    next(r)
    for row in r:
        lat, lon = float(row[0]), float(row[1])
        if W_ <= lon <= E_ and S_ <= lat <= N_ and float(row[3]) >= 0.70:
            G.append(transform(tr, wkt.loads(row[4])))
print(f'{len(G)} Google buildings in the box', flush=True)
from shapely.strtree import STRtree
gt = STRtree(G)
stt = STRtree([g for g, w in streets])


def square(x, y):
    sq = box(x, y, x + SQ, y + SQ)
    bs = [G[i] for i in gt.query(sq)]
    ss = [streets[i] for i in stt.query(sq.buffer(30))]
    return sq, bs, ss


x0, y0, x1, y1 = A.bounds
rows, mrows = [], []
for x in np.arange(x0, x1 - SQ, SQ):
    for y in np.arange(y0, y1 - SQ, SQ):
        sq, bs, ss = square(x, y)
        if A.intersection(sq).area < 0.95 * SQ * SQ:
            continue
        cov = sum(b.area for b in bs if sq.contains(b.centroid)) / (SQ * SQ)
        if cov < 0.15 or sum(g.intersection(sq).length for g, w in ss) < 1500:
            continue   # lagoon edge, bush or untraced: not the built city
        m = measure(bs, [g for g, w in ss], sq, [w for g, w in ss])
        (mrows if any(sq.contains(mk.centroid) for mk in markets) else rows).append(m)
# the markets themselves, centred
for mk in markets:
    c = mk.centroid
    sq, bs, ss = square(c.x - SQ / 2, c.y - SQ / 2)
    m = measure(bs, [g for g, w in ss], sq, [w for g, w in ss])
    m['market_ha'] = round(mk.area / 1e4, 1)
    mrows.append(m)
print(f'{len(rows)} built squares, {len(mrows)} market squares', flush=True)


def summary(rs):
    keys = ['per_km2', 'cover', 'edge_cover', 'back_cover', 'front_occupied', 'front_share_of_buildings', 'touching', 'under_40m2']
    out = {k: {'median': round(float(np.median([r[k] for r in rs if k in r])), 3), 'p75': round(float(np.percentile([r[k] for r in rs if k in r], 75)), 3)} for k in keys if any(k in r for r in rs)}
    for k, sub in (('block_fill', 'median'), ('line_deg', 'median'), ('line_deg', 'share_within_10deg'), ('setback_m', 'median'), ('front_gap_m', 'median'),
                   ('front_gap_m', 'share_under_3m'), ('size_m2', 'median'), ('size_m2', 'p90'), ('long_side_m', 'median')):
        v = [r[k][sub] for r in rs if r.get(k)]
        if v:
            out[f'{k}.{sub}'] = round(float(np.median(v)), 3)
    return out


# Gidi's district now, in 500 m squares (y runs south in Gidi; the measures don't care)
GD = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
dd = [d for d in GD['districts'] if d['id'] == DID][0]
P = Polygon(dd['poly'][0])
gb = [Polygon(b[1:]).buffer(0) for b in GD['buildings'][DID] if len(b) > 3]
gw = [(LineString(p), 7.0) for p in GD['streets'].get(DID, [])] + [(LineString(p), 3.5) for p in GD['lanes'].get(DID, [])] \
    + [(LineString(m['pts']), 14.0) for m in GD['mains']] + [(LineString(a['pts']), 18.0 if a['cls'] != 'exp' else 30.0) for a in GD['arterials']]
grow = []
px0, py0, px1, py1 = P.bounds
for x in np.arange(px0, px1 - SQ, SQ / 2):
    for y in np.arange(py0, py1 - SQ, SQ / 2):
        sq = box(x, y, x + SQ, y + SQ)
        if P.intersection(sq).area < 0.95 * SQ * SQ:
            continue
        ss = [(g, w) for g, w in gw if g.intersects(sq.buffer(30))]
        grow.append(measure([b for b in gb if sq.intersects(b)], [g for g, w in ss], sq, [w for g, w in ss]))
print(f'{len(grow)} Gidi squares', flush=True)

# Overture: places and street furniture per km2 of the built squares' land
import pyarrow.parquet as pq
from shapely import from_wkb
pl = pq.read_table(f'{DATA}/overture-lagos/lagos_overture_place.parquet', columns=['geometry', 'basic_category']).to_pydict()
inf = pq.read_table(f'{DATA}/overture-lagos/lagos_overture_infrastructure.parquet', columns=['geometry', 'subtype', 'class']).to_pydict()
from collections import Counter
def in_area(geoms):
    for g in geoms:
        p = from_wkb(g)
        c = p.centroid
        x, y = tr(c.x, c.y)
        yield A.contains(Point(x, y))
pc = Counter(c for c, ok in zip(pl['basic_category'], in_area(pl['geometry'])) if ok)
ic = Counter(f'{s}/{c}' for s, c, ok in zip(inf['subtype'], inf['class'], in_area(inf['geometry'])) if ok)
km2 = A.area / 1e6

res = {'id': DID, 'box': sys.argv[2], 'square_m': SQ,
       'source': 'Google Open Buildings v3 (CC BY 4.0, confidence >= 0.70) outlines; OSM streets (ODbL); Overture places and infrastructure; numbers only',
       'real': summary(rows), 'real_squares': len(rows), 'market': summary(mrows) if mrows else None, 'market_squares': len(mrows),
       'gidi_now': summary(grow), 'gidi_squares': len(grow),
       'places_per_km2': {k: round(v / km2, 1) for k, v in pc.most_common(40) if k}, 'study_km2': round(km2, 1),
       'infrastructure_per_km2': {k: round(v / km2, 2) for k, v in ic.most_common(30)}}
os.makedirs('docs/data', exist_ok=True)
json.dump(res, open(f'docs/data/structure-{DID}.json', 'w'), indent=1)
print(f"{'measure':34} {'real':>8} {'market':>8} {'Gidi now':>9}")
for k in res['real']:
    f = lambda d: (d[k]['median'] if isinstance(d.get(k), dict) else d.get(k)) if d else None
    a, b, c = f(res['real']), f(res['market']), f(res['gidi_now'])
    fmt = lambda v: f'{v:8.3f}' if isinstance(v, float) and v < 10 else (f'{v:8.0f}' if v is not None else '       -')
    print(f'{k:34} {fmt(a)} {fmt(b)} {fmt(c)} ')
