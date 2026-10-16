# Deep study, step 2 (docs/DEEP-STUDY.md): everything the data says about one district's real inspiration, for its generator profile.
# Sources (numbers only go into Gidi, never an outline, a name or an image):
#   Google Open Buildings v3 outlines (confidence >= 0.70)   Google Open Buildings 2.5D 2023 heights (0.5 m, read at 2 m)
#   Microsoft building outlines (a cross-check)              OpenStreetMap (study-<id>.pkl: waterways, markets, rail, power)
#   Overture: road segments, places, infrastructure, land use, land
#   ESA WorldCover 2021 (10 m land cover)   WorldPop 2020 (people, ~100 m)   Copernicus GLO-30 (ground height)
# What it measures, over the whole study area and over its built-up 500 m squares:
#   buildings (density, cover, sizes, shapes, orientation, touching, gaps, lines and fronts, block fill), heights and storeys,
#   streets (km by class, surface, junctions, dead ends, blocks, grain, bridges), places (by Gidi kind, on main roads or not),
#   street things (lamps, signals, bus stops, poles, gates, walls), land use and land cover, people, ground, water,
#   how it changes away from main roads and water, the fabric types inside the district (250 m cells, clustered), landmarks,
#   and how far the sources agree.
# Usage: python3 scripts/study_deep.py <id>   -> docs/data/deep/<id>.json, docs/studies/<id>.md, docs/img/study-<id>.png
import json, math, os, pickle, sys, collections
import numpy as np
import pyarrow.parquet as pq
import rasterio
from rasterio.enums import Resampling
from rasterio.features import rasterize
from rasterio.windows import from_bounds
from shapely import wkb, contains_xy
from shapely.geometry import box, Point, LineString, MultiLineString, Polygon
from shapely.ops import transform, unary_union, polygonize
from shapely.strtree import STRtree
from pyproj import Transformer
from scipy import ndimage
sys.path.insert(0, os.path.dirname(__file__))
from structure import measure

DID = sys.argv[1]
DATA = os.path.expanduser('~/Real-world/research/data')
CACHE = os.environ.get('GIDI_DEEP_CACHE', os.path.join(DATA, 'deep-cache'))
DIRS = ['.', os.environ.get('GIDI_STUDIES', '')]
tr = Transformer.from_crs(4326, 32631, always_xy=True).transform
back = Transformer.from_crs(32631, 4326, always_xy=True).transform
R = lambda v, n=3: round(float(v), n)
pct = lambda a, ps=(10, 25, 50, 75, 90): {f'p{p}': R(np.percentile(a, p), 1) for p in ps} if len(a) else None

D = next(pickle.load(open(os.path.join(d, f'study-{DID}.pkl'), 'rb')) for d in DIRS if d and os.path.exists(os.path.join(d, f'study-{DID}.pkl')))
A = D['area'].buffer(0)
ALL = transform(back, A)
W_, S_, E_, N_ = ALL.bounds
J = {'id': DID, 'area_km2': R(A.area / 1e6, 2), 'bounds_lonlat': [R(v, 4) for v in ALL.bounds]}
log = lambda *a: print(DID, *a, flush=True)

# ---------------------------------------------------------------- land cover (WorldCover) and water
WC = {10: 'trees', 20: 'shrub', 30: 'grass', 40: 'crops', 50: 'built-up', 60: 'bare', 80: 'water', 90: 'wetland', 95: 'mangrove'}
res = 10.0
gx0, gy0, gx1, gy1 = [math.floor(v / res) * res for v in A.bounds[:2]] + [math.ceil(v / res) * res for v in A.bounds[2:]]
nxw, nyw = int((gx1 - gx0) / res), int((gy1 - gy0) / res)
from rasterio.transform import from_origin
T10 = from_origin(gx0, gy1, res, res)
wc = np.zeros((nyw, nxw), np.uint8)
from rasterio.warp import reproject
for tile in ('N06E000.tif', 'N06E003.tif'):
    with rasterio.open(os.path.join(DATA, 'worldcover', tile)) as r:
        if not box(*r.bounds).intersects(ALL):
            continue
        tmp = np.zeros_like(wc)
        reproject(rasterio.band(r, 1), tmp, dst_transform=T10, dst_crs='EPSG:32631', resampling=Resampling.nearest)
        wc = np.where(tmp > 0, tmp, wc)
inA = rasterize([(A, 1)], out_shape=wc.shape, transform=T10, dtype='uint8').astype(bool)
cls, cnt = np.unique(wc[inA], return_counts=True)
J['land_cover'] = {WC.get(int(c), str(c)): R(n / inA.sum()) for c, n in zip(cls, cnt) if c in WC}
wet = (wc == 80) & inA
land_km2 = A.area / 1e6 * (1 - J['land_cover'].get('water', 0))
J['land_km2'] = R(land_km2, 2)
dist_water = ndimage.distance_transform_edt(~(wc == 80)) * res   # metres to open water (WorldCover), for the gradients


def at_raster(xs, ys, arr, T):
    c = ((np.asarray(xs) - T.c) / T.a).astype(int); r = ((np.asarray(ys) - T.f) / T.e).astype(int)
    c = np.clip(c, 0, arr.shape[1] - 1); r = np.clip(r, 0, arr.shape[0] - 1)
    return arr[r, c]


log('land cover', J['land_cover'])

# ---------------------------------------------------------------- buildings
BC = pickle.load(open(os.path.join(CACHE, f'bld-{DID}.pkl'), 'rb'))
G = [g.buffer(0) for g, c in BC['google'] if c >= 0.70]
G = [g for g in G if g.area >= 6 and g.geom_type == 'Polygon']
fp = np.array([g.area for g in G])
cx = np.array([g.centroid.x for g in G]); cy = np.array([g.centroid.y for g in G])
J['sources'] = {'google_all': len(BC['google']), 'google_conf70': len(G), 'microsoft': len(BC['ms']),
                'microsoft_with_height': sum(1 for g, h in BC['ms'] if h and h > 0), 'osm': len(D['buildings'])}
mr = [g.minimum_rotated_rectangle for g in G]


def rect_sides(r):
    c = list(r.exterior.coords) if r.geom_type == 'Polygon' else [(0, 0), (1, 0), (1, 1)]
    a, b = math.dist(c[0], c[1]), math.dist(c[1], c[2])
    ang = math.degrees(math.atan2(c[1][1] - c[0][1], c[1][0] - c[0][0])) % 90
    return max(a, b), max(min(a, b), 0.1), ang


sides = np.array([rect_sides(r) for r in mr])
rectness = np.array([g.area / max(r.area, 1e-6) for g, r in zip(G, mr)])
tree = STRtree(G)
touch = np.zeros(len(G), bool); gap = np.full(len(G), 99.0)
for i, g in enumerate(G):
    for j in tree.query(g.buffer(6)):
        if j != i:
            d = g.distance(G[j]); gap[i] = min(gap[i], d)
    touch[i] = gap[i] <= 1.0
SB = [0, 15, 40, 100, 200, 500, 2000, 1e9]
J['buildings'] = {
    'per_km2_land': R(len(G) / land_km2, 0), 'cover_land': R(fp.sum() / 1e6 / land_km2),
    'size_m2': pct(fp, (5, 10, 25, 50, 75, 90, 95, 99)),
    'size_bands_share': {f'{SB[i]}-{SB[i + 1] if SB[i + 1] < 1e9 else "+"}': R(((fp >= SB[i]) & (fp < SB[i + 1])).mean()) for i in range(len(SB) - 1)},
    'long_side_m': pct(sides[:, 0]), 'aspect': pct(sides[:, 0] / sides[:, 1]), 'rectangularity': pct(rectness),
    'touching_share': R(touch.mean()), 'nearest_gap_m': pct(gap[gap < 99]),
}
# grain: how lined up the buildings are (angle of the long side, folded to 0-90)
h, _ = np.histogram(sides[:, 2], bins=18, range=(0, 90), weights=fp)
hs = h / max(h.sum(), 1)
J['buildings']['orientation_peak_deg'] = int(np.argmax(hs) * 5 + 2)
J['buildings']['orientation_share_within_10deg_of_peak'] = R(sum(hs[(np.argmax(hs) + k) % 18] for k in (-2, -1, 0, 1)))
log('buildings', len(G))

# ---------------------------------------------------------------- heights (Google 2.5D, 2023)
HR = 2.0
hx0, hy0, hx1, hy1 = [math.floor(v / HR) * HR for v in A.bounds[:2]] + [math.ceil(v / HR) * HR for v in A.bounds[2:]]
nxh, nyh = int((hx1 - hx0) / HR), int((hy1 - hy0) / HR)
T2 = from_origin(hx0, hy1, HR, HR)
Hm = np.zeros((nyh, nxh), np.float32)
OBD = os.path.join(DATA, 'open-buildings-2023')
for t in sorted(f for f in os.listdir(OBD) if f.endswith('.tif')):
    with rasterio.open(os.path.join(OBD, t)) as r:
        if not box(*r.bounds).intersects(box(hx0, hy0, hx1, hy1)):
            continue
        w = from_bounds(hx0, hy0, hx1, hy1, r.transform)
        part = r.read(2, window=w, out_shape=(nyh, nxh), resampling=Resampling.max, boundless=True, fill_value=0)
        Hm = np.maximum(Hm, np.nan_to_num(part))
ids = rasterize([(g, i + 1) for i, g in enumerate(G)], out_shape=Hm.shape, transform=T2, dtype='int32')
hmax = np.zeros(len(G) + 1, np.float32)
m = ids > 0
np.maximum.at(hmax, ids[m], Hm[m])
hb = hmax[1:]
miss = hb <= 0
hb[miss] = at_raster(cx[miss], cy[miss], Hm, T2)   # small buildings with no 2 m pixel inside: the pixel at the centre


def storeys(hh):
    return np.where(hh < 4.5, 1, ((hh - 4.5) // 3 + 2)).astype(int)


st = storeys(hb)
J['heights'] = {'no_height_share': R((hb <= 0).mean()), 'height_m': pct(hb[hb > 0]),
                'storeys_share': {str(k): R((np.minimum(st, 8) == k).mean()) for k in range(1, 9)},
                'storeys_share_by_area': {str(k): R(fp[np.minimum(st, 8) == k].sum() / fp.sum()) for k in range(1, 9)},   # as the generator's height bands
                'storeys_by_size': {f'{SB[i]}-{SB[i + 1] if SB[i + 1] < 1e9 else "+"} m2': R(np.median(st[(fp >= SB[i]) & (fp < SB[i + 1])]), 1)
                                    for i in range(len(SB) - 1) if ((fp >= SB[i]) & (fp < SB[i + 1])).sum() >= 20},
                'tall_7plus_per_km2': R((st >= 7).sum() / land_km2, 1), 'floor_area_ratio_land': R((fp * st).sum() / 1e6 / land_km2)}
log('heights', J['heights']['storeys_share'])

# ---------------------------------------------------------------- streets (Overture segments)
O = os.path.join(DATA, 'overture-lagos')


def read_overture(name, cols):
    t = pq.read_table(os.path.join(O, name), columns=cols + ['geometry', 'bbox'])
    out = []
    for r in t.to_pylist():
        b = r['bbox']
        if b['xmax'] < W_ or b['xmin'] > E_ or b['ymax'] < S_ or b['ymin'] > N_:
            continue
        g = transform(tr, wkb.loads(r['geometry']))
        if g.intersects(A):
            r['g'] = g; out.append(r)
    return out


SEG = read_overture('lagos_overture_segment.parquet', ['id', 'subtype', 'class', 'subclass', 'road_surface', 'road_flags', 'connectors', 'names'])
MAINC = ('motorway', 'trunk', 'primary', 'secondary')
LOCALC = ('tertiary', 'unclassified', 'residential', 'living_street')
PATHC = ('path', 'footway', 'steps', 'track', 'pedestrian', 'cycleway')
WID = {'motorway': 30, 'trunk': 24, 'primary': 18, 'secondary': 14, 'tertiary': 10, 'unclassified': 7, 'residential': 7, 'living_street': 6, 'service': 4}
roads = [s for s in SEG if s['subtype'] == 'road']
km = collections.Counter()
surf = collections.Counter()
for s in roads:
    L = s['g'].intersection(A).length / 1000
    km[s['class']] += L
    v = (s['road_surface'] or [{'value': 'not recorded'}])[0]['value']
    surf[('main' if s['class'] in MAINC else 'local' if s['class'] in LOCALC else 'other', v)] += L
drive = [s for s in roads if s['class'] in MAINC + LOCALC + ('service', 'unknown')]
# junctions from Overture's connectors: a connector used by 3+ segment ends (a pass-through counts as 2)
deg = collections.Counter(); cpos = {}
for s in drive:
    for c in s['connectors'] or []:
        deg[c['connector_id']] += 1 if c['at'] in (0, 1) or abs(c['at']) < 1e-9 or abs(c['at'] - 1) < 1e-9 else 2
        p = s['g'].interpolate(c['at'], normalized=True); cpos[c['connector_id']] = (p.x, p.y)
inside = {k: v for k, v in deg.items() if A.contains(Point(cpos[k]))}
dv = np.array(list(inside.values()))
bridges = [s for s in roads if s['road_flags'] and any('is_bridge' in f['values'] for f in s['road_flags'])]
def bridge_len(s):   # only the flagged part of a segment is bridge ("between" is a share of its length)
    g = s['g'].intersection(A); L = 0.0
    for f in s['road_flags']:
        if 'is_bridge' in f['values']:
            a, b = f['between'] or (0, 1); L += g.length * (b - a)
    return L
main_lines = [s['g'] for s in roads if s['class'] in MAINC]
mainU = unary_union(main_lines) if main_lines else None
# blocks: the land cut by the drivable streets
blocks = [p for p in polygonize(unary_union([s['g'] for s in drive])) if A.contains(p.representative_point())]
blk = np.array([p.area / 1e4 for p in blocks if p.area < 50e4])
# grain of the streets: length-weighted bearing, folded to 0-180, and its entropy (0 = a perfect grid, 1 = every direction)
bh = np.zeros(18)
for s in drive:
    cs = list(s['g'].coords)
    for a, b in zip(cs, cs[1:]):
        bh[int(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 180 // 10)] += math.dist(a, b)
pb = bh / max(bh.sum(), 1)
ent = -sum(p * math.log(p) for p in pb if p > 0) / math.log(18)
seglen = np.array([s['g'].length for s in drive])
J['streets'] = {
    'km_per_km2_land': {k: R(v / land_km2, 2) for k, v in sorted(km.items(), key=lambda kv: -kv[1])},
    'drivable_km_per_km2': R(sum(km[c] for c in MAINC + LOCALC + ('service', 'unknown')) / land_km2, 2),
    'main_km_per_km2': R(sum(km[c] for c in MAINC) / land_km2, 2),
    'surface_km': {f'{a}: {b}': R(v, 1) for (a, b), v in sorted(surf.items(), key=lambda kv: -kv[1])},
    'junctions_per_km2': R((dv >= 3).sum() / land_km2, 1), 'T_share': R((dv == 3).mean() / max((dv >= 3).mean(), 1e-9)),
    'four_plus_share': R((dv >= 4).mean() / max((dv >= 3).mean(), 1e-9)), 'dead_ends_per_km2': R((dv == 1).sum() / land_km2, 1),
    'segment_m': pct(seglen), 'block_ha': pct(blk, (25, 50, 75, 90)), 'blocks': len(blk),
    'grain_entropy': R(ent), 'grain_peak_deg': int(np.argmax(pb) * 10 + 5),
    'bridge_segments': len(bridges), 'bridge_m': R(sum(bridge_len(b) for b in bridges), 0),
    'rail_km': R(sum(s['g'].intersection(A).length for s in SEG if s['subtype'] == 'rail') / 1000, 2),
    'paths_km_per_km2': R(sum(km[c] for c in PATHC) / land_km2, 2),
}
log('streets', J['streets']['drivable_km_per_km2'])

# ---------------------------------------------------------------- the structure measures (scripts/structure.py) on built 500 m squares
SQ = 500.0
stt = STRtree([s['g'] for s in drive])
sq_rows = []
x0, y0, x1, y1 = A.bounds
for x in np.arange(x0, x1 - SQ, SQ):
    for y in np.arange(y0, y1 - SQ, SQ):
        sq = box(x, y, x + SQ, y + SQ)
        if A.intersection(sq).area < 0.95 * SQ * SQ:
            continue
        bs = [G[i] for i in tree.query(sq)]
        ss = [drive[i] for i in stt.query(sq.buffer(30))]
        cov = sum(b.area for b in bs if sq.contains(b.centroid)) / (SQ * SQ)
        if cov < 0.10 or sum(s['g'].intersection(sq).length for s in ss) < 1200:
            continue
        sq_rows.append(measure(bs, [s['g'] for s in ss], sq, [WID.get(s['class'], 6) for s in ss]))


def summary(rs):
    if not rs:
        return None
    out = {'squares': len(rs)}
    for k in ('per_km2', 'cover', 'edge_cover', 'back_cover', 'front_occupied', 'front_share_of_buildings', 'touching', 'under_40m2'):
        v = [r[k] for r in rs if r.get(k) is not None]
        if v:
            out[k] = {'p25': R(np.percentile(v, 25)), 'median': R(np.median(v)), 'p75': R(np.percentile(v, 75))}
    for k, sub in (('block_fill', 'median'), ('line_deg', 'median'), ('line_deg', 'share_within_10deg'), ('setback_m', 'median'),
                   ('front_gap_m', 'median'), ('front_gap_m', 'share_under_3m'), ('size_m2', 'median'), ('long_side_m', 'median')):
        v = [r[k][sub] for r in rs if r.get(k)]
        if v:
            out[f'{k}.{sub}'] = R(np.median(v))
    return out


J['structure_built_squares'] = summary(sq_rows)
log('structure squares', len(sq_rows))

# ---------------------------------------------------------------- places (Overture)
KINDS = [('church', ('christian_place_of_worship', 'religious_organization', 'church')), ('mosque', ('muslim_place_of_worship', 'mosque')),
         ('school', ('place_of_learning', 'education', 'school', 'preschool', 'educational_service')), ('university', ('college_university',)),
         ('health', ('hospital', 'health_care', 'clinic', 'pharmacy', 'diagnostics', 'dental', 'medical')),
         ('market & shops', ('shopping', 'store', 'market', 'shopping_mall', 'retail')),
         ('food & drink', ('restaurant', 'eatery', 'bar', 'lounge', 'food_service', 'food_and_drink', 'dance_club', 'night_club', 'bakery')),
         ('hotel', ('hotel', 'lodging', 'accommodation')), ('money', ('financial_service', 'bank', 'atm')), ('fuel', ('gas_station', 'fuel')),
         ('motor trade', ('automotive', 'auto_dealer', 'vehicle', 'car_wash')), ('beauty', ('beauty', 'personal_care', 'salon', 'barber')),
         ('events & music', ('event', 'arts_and_entertainment', 'music', 'cinema', 'movie_theater')),
         ('transport', ('travel', 'transportation', 'parking', 'bus_station')), ('industry & trade', ('manufacturer', 'industrial', 'supplier', 'wholesale', 'b2b')),
         ('government & order', ('government', 'police', 'military', 'court', 'civic')),
         ('offices & services', ('professional_service', 'real_estate', 'corporate', 'office', 'attorney', 'legal', 'media', 'design', 'technical', 'service'))]


def kind_of(r):
    hier = ' '.join(((r.get('taxonomy') or {}).get('hierarchy') or []) + [r.get('basic_category') or ''])
    for k, keys in KINDS:
        if any(x in hier for x in keys):
            return k
    return 'other'


PL = [r for r in read_overture('lagos_overture_place.parquet', ['basic_category', 'taxonomy', 'confidence', 'names']) if (r['confidence'] or 0) >= 0.4]
PL = [r for r in PL if A.contains(r['g'])]
kc = collections.Counter(kind_of(r) for r in PL)
onmain = collections.Counter(kind_of(r) for r in PL if mainU is not None and r['g'].distance(mainU) <= 40)
raw = collections.Counter(((r.get('taxonomy') or {}).get('primary') or r['basic_category'] or 'none') for r in PL)
J['places'] = {'total_per_km2': R(len(PL) / land_km2, 1),
               'by_kind_per_km2': {k: R(v / land_km2, 2) for k, v in kc.most_common()},
               'share_within_40m_of_main_road': {k: R(onmain[k] / v) for k, v in kc.most_common() if v >= 5},
               'top_categories': [[k, v] for k, v in raw.most_common(30)]}
log('places', len(PL))

# ---------------------------------------------------------------- street things and structures (Overture infrastructure)
INF = [r for r in read_overture('lagos_overture_infrastructure.parquet', ['subtype', 'class']) if True]
ic = collections.Counter(); il = collections.Counter()
for r in INF:
    g = r['g'].intersection(A)
    if g.is_empty:
        continue
    k = f"{r['subtype']}: {r['class']}"
    if g.geom_type in ('LineString', 'MultiLineString'):
        il[k] += g.length / 1000
    elif g.geom_type in ('Polygon', 'MultiPolygon'):
        ic[k] += 1
    else:
        ic[k] += 1
J['street_things'] = {'count_per_km2': {k: R(v / land_km2, 2) for k, v in ic.most_common()}, 'km_per_km2': {k: R(v / land_km2, 2) for k, v in il.most_common()},
                      'note': 'Overture infrastructure is mostly OSM: street lamps, signals and bus stops are badly under-mapped in Lagos; read these as a floor'}

# ---------------------------------------------------------------- land use (Overture) and OSM extras
LU = read_overture('lagos_overture_land_use.parquet', ['subtype', 'class'])
lu = collections.Counter()
for r in LU:
    if r['g'].geom_type in ('Polygon', 'MultiPolygon') and r['g'].area < 3 * A.area:   # not the region-wide outlines
        lu[f"{r['subtype']}: {r['class']}"] += r['g'].buffer(0).intersection(A).area
J['land_use_mapped_share'] = {k: R(v / A.area, 4) for k, v in lu.most_common() if v > 0}
LN = read_overture('lagos_overture_land.parquet', ['subtype', 'class'])
ln = collections.Counter()
for r in LN:
    if r['g'].geom_type in ('Polygon', 'MultiPolygon') and r['g'].area < 3 * A.area:
        ln[f"{r['subtype']}: {r['class']}"] += r['g'].buffer(0).intersection(A).area
J['land_mapped_share'] = {k: R(v / A.area, 4) for k, v in ln.most_common() if v > 0}
ww = collections.Counter()
for t, g in D['water']:
    ww[t.get('waterway') or t.get('natural') or 'water'] += g.intersection(A).length / 1000
mk = [g for t, g in D['landuse'] if t.get('amenity') == 'marketplace' or t.get('landuse') == 'retail' and 'market' in (t.get('name') or '').lower()]
J['osm'] = {'waterways_km': {k: R(v, 2) for k, v in ww.most_common()}, 'markets': len(mk), 'market_ha': [R(g.area / 1e4, 1) for g in sorted(mk, key=lambda g: -g.area)[:12]],
            'power_km': R(sum(g.intersection(A).length for t, g in D['power']) / 1000, 2), 'rail_km': R(sum(g.intersection(A).length for t, g in D['rail']) / 1000, 2),
            'amenity_points': collections.Counter(t.get('amenity') or t.get('shop') or t.get('leisure') or 'other' for t, g in D['points']).most_common(20)}

# ---------------------------------------------------------------- people (WorldPop 2020) and ground (Copernicus)
with rasterio.open(os.path.join(DATA, 'worldpop/nga_ppp_2020_UNadj_constrained.tif')) as r:
    w = from_bounds(W_, S_, E_, N_, r.transform).round_offsets().round_lengths()
    P = r.read(1, window=w, boundless=True, fill_value=0).astype(float); P[P < 0] = 0
    mP = rasterize([(ALL, 1)], out_shape=P.shape, transform=r.window_transform(w), dtype='uint8').astype(bool)
    people = float(P[mP].sum())
J['people'] = {'total': int(people), 'per_km2_land': R(people / land_km2, 0), 'per_building': R(people / max(len(G), 1), 1),
               'per_100m2_floor': R(people / max((fp * st).sum() / 100, 1), 2)}
Z = None
for t in sorted(os.listdir(os.path.join(DATA, 'dem'))):   # the 1-degree Copernicus tiles (E002 for the Border)
    with rasterio.open(os.path.join(DATA, 'dem', t)) as r:
        ref = r if Z is None else ref
        if Z is None:
            w = from_bounds(W_, S_, E_, N_, r.transform).round_offsets().round_lengths(); TZ = r.window_transform(w)
            Z = np.full((int(w.height), int(w.width)), -99.0)
        w2 = from_bounds(*rasterio.transform.array_bounds(Z.shape[0], Z.shape[1], TZ), r.transform)
        part = r.read(1, window=w2, out_shape=Z.shape, boundless=True, fill_value=-99).astype(float)
        Z = np.where(part > -50, part, Z)
mZ = rasterize([(ALL, 1)], out_shape=Z.shape, transform=TZ, dtype='uint8').astype(bool)
if True:
    Z3 = ndimage.minimum_filter(Z, 3)   # roofs and trees drop out (as scripts/terrain.py)
    z = Z3[mZ & (Z3 > 0.3)]
    gy, gx = np.gradient(ndimage.gaussian_filter(Z3, 2), 30.0)
    slope = np.degrees(np.arctan(np.hypot(gx, gy)))[mZ & (Z3 > 0.3)]
J['ground'] = {'height_m': pct(z), 'below_3m_share': R((z < 3).mean()), 'slope_deg': pct(slope, (50, 90, 99))}

# ---------------------------------------------------------------- gradients: away from main roads, away from water
dmain = np.array([Point(a, b).distance(mainU) for a, b in zip(cx, cy)]) if mainU is not None else np.full(len(G), 9e9)
dwat = at_raster(cx, cy, dist_water, T10)


def band_table(dist, edges, name):
    rows = []
    for lo, hi in zip(edges, edges[1:]):
        sel = (dist >= lo) & (dist < hi)
        if mainU is not None and name == 'main':
            ring = (mainU.buffer(hi) if hi < 1e8 else A).difference(mainU.buffer(lo) if lo > 0 else Polygon()).intersection(A)
            akm2 = ring.area / 1e6 * (1 - J['land_cover'].get('water', 0))
        else:
            px = ((dist_water >= lo) & (dist_water < hi) & inA & ~wet).sum(); akm2 = px * res * res / 1e6
        if sel.sum() < 30 or akm2 <= 0.01:
            continue
        rows.append({'band_m': f'{lo}-{hi if hi < 1e8 else "+"}', 'buildings_per_km2': R(sel.sum() / akm2, 0), 'cover': R(fp[sel].sum() / 1e6 / akm2),
                     'size_m2_median': R(np.median(fp[sel]), 0), 'storeys_mean': R(st[sel].mean(), 2), 'touching': R(touch[sel].mean()),
                     'share_3plus_storeys': R((st[sel] >= 3).mean())})
    return rows


J['away_from_main_roads'] = band_table(dmain, [0, 30, 80, 150, 300, 600, 1e9], 'main')
J['away_from_water'] = band_table(dwat, [0, 50, 150, 400, 1000, 1e9], 'water')

# ---------------------------------------------------------------- fabric types: 250 m cells, clustered (k-means, fixed seed)
C = 250.0
cells = []
ptree = STRtree([r['g'] for r in PL]) if PL else None
for x in np.arange(x0, x1, C):
    for y in np.arange(y0, y1, C):
        c = box(x, y, x + C, y + C)
        if A.intersection(c).area < 0.9 * C * C:
            continue
        sel = (cx >= x) & (cx < x + C) & (cy >= y) & (cy < y + C)
        cov = fp[sel].sum() / (C * C)
        if cov < 0.04 or sel.sum() < 8:
            continue
        sl = sum(drive[i]['g'].intersection(c).length for i in stt.query(c)) / 1000 / (C * C / 1e6)
        npl = len(ptree.query(c, predicate='contains')) if ptree else 0
        cells.append([x + C / 2, y + C / 2, sel.sum() / (C * C / 1e6), cov, np.median(fp[sel]), touch[sel].mean(), st[sel].mean(), sl, npl / (C * C / 1e6)])
cells = np.array(cells)
FEAT = ['buildings_per_km2', 'cover', 'size_m2_median', 'touching', 'storeys_mean', 'street_km_per_km2', 'places_per_km2']
types = []
if len(cells) >= 8:
    X = cells[:, 2:].copy(); X[:, 0] = np.log1p(X[:, 0]); X[:, 2] = np.log1p(X[:, 2]); X[:, 6] = np.log1p(X[:, 6])
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-9)
    k = 4 if len(cells) >= 40 else 3
    rng = np.random.RandomState(7)
    best = None
    for rep in range(12):
        cen = Xs[rng.choice(len(Xs), k, replace=False)]
        for _ in range(60):
            lab = np.argmin(((Xs[:, None, :] - cen[None]) ** 2).sum(-1), 1)
            cen = np.array([Xs[lab == j].mean(0) if (lab == j).any() else cen[j] for j in range(k)])
        sse = ((Xs - cen[lab]) ** 2).sum()
        if best is None or sse < best[0]:
            best = (sse, lab)
    lab = best[1]
    order = np.argsort([-cells[lab == j, 2].mean() for j in range(k)])
    for rank, j in enumerate(order):
        cj = cells[lab == j]
        v = {f: R(np.median(cj[:, 2 + i]), 2) for i, f in enumerate(FEAT)}
        # a plain name: the two ways this type differs most from the district's average cell
        WORDS = [('denser', 'sparser'), ('more built over', 'more open'), ('bigger buildings', 'smaller buildings'), ('walls touching', 'spaced out'),
                 ('taller', 'lower'), ('more streets', 'fewer streets'), ('busier (shops, churches, services)', 'quieter')]
        zc = Xs[lab == j].mean(0)
        name = ', '.join(WORDS[i][0 if zc[i] > 0 else 1] for i in np.argsort(-np.abs(zc))[:2])
        ex = cj[np.argmin(((cj[:, 2:4] - np.median(cj[:, 2:4], 0)) ** 2).sum(1))]
        lon, lat = back(ex[0], ex[1])
        types.append({'type': rank + 1, 'name': name, 'share_of_built_cells': R(len(cj) / len(cells)), 'cells': int(len(cj)), **v,
                      'example_lonlat': [R(lon, 5), R(lat, 5)]})
    J['fabric_types'] = types
J['built_cells_250m'] = {'cells': int(len(cells)), **({f: pct(cells[:, 2 + i]) for i, f in enumerate(FEAT)} if len(cells) else {})}

# ---------------------------------------------------------------- landmarks: the biggest buildings, with the nearest named place
big = np.argsort(-fp)[:20]
L = []
for i in big:
    near = min(PL, key=lambda r: r['g'].distance(G[i]), default=None) if PL else None
    lon, lat = back(cx[i], cy[i])
    L.append({'m2': int(fp[i]), 'storeys': int(st[i]), 'lonlat': [R(lon, 5), R(lat, 5)],
              'nearest_place': None if near is None or near['g'].distance(G[i]) > 60 else
              [((near.get('names') or {}).get('primary') or ''), (near.get('taxonomy') or {}).get('primary') or near['basic_category']]})
J['landmarks_biggest'] = L
J['note'] = ('Study only: names and positions here are for understanding the real place. Gidi takes numbers from this file, never an '
             'outline, a name or an image (CLAUDE.md, the Google rule).')

os.makedirs('docs/data/deep', exist_ok=True)
json.dump(J, open(f'docs/data/deep/{DID}.json', 'w'), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- picture: buildings by storeys, main roads, places, fabric types
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(20, 10))
for a_ in ax:
    for g_ in getattr(A, 'geoms', [A]):   # a study area can be several boxes
        a_.fill(*g_.exterior.xy, color='#f3efe6', ec='#888')
    wpx = np.argwhere(wet[::3, ::3])
    a_.scatter(gx0 + wpx[:, 1] * res * 3, gy1 - wpx[:, 0] * res * 3, s=0.3, c='#a9cbe6', marker='s')
SC = {1: '#d9c9a8', 2: '#c49a6c', 3: '#a0522d', 4: '#7b2d26', 5: '#4a1c40'}
from matplotlib.collections import PolyCollection
polys = [np.array(g.exterior.coords) for g in G]
ax[0].add_collection(PolyCollection(polys, facecolors=[SC[min(int(s), 5)] for s in st], edgecolors='none'))
for s in roads:
    if s['class'] in MAINC:
        for g in getattr(s['g'], 'geoms', [s['g']]):
            ax[0].plot(*g.xy, color='#c0392b', lw=1.2)
    elif s['class'] in LOCALC:
        for g in getattr(s['g'], 'geoms', [s['g']]):
            ax[0].plot(*g.xy, color='#999', lw=0.25)
ax[0].set_title(f'{DID}: {len(G):,} buildings by storeys (1 pale to 5+ dark), main roads red')
if len(cells):
    TC = ['#e74c3c', '#f39c12', '#27ae60', '#2980b9', '#8e44ad']
    lab_rank = {j: r for r, j in enumerate(order)}
    for (x, y, *_), l in zip(cells, lab):
        ax[1].add_patch(plt.Rectangle((x - C / 2, y - C / 2), C, C, color=TC[lab_rank[l]], alpha=.65, lw=0))
    for t in types:
        ax[1].plot([], [], 's', color=TC[t['type'] - 1], label=f"{t['type']}. {t['name']} ({round(100 * t['share_of_built_cells'])}%)")
    ax[1].legend(loc='upper right', fontsize=9)
ax[1].set_title('fabric types (250 m cells)')
for a_ in ax:
    a_.set_aspect('equal'); a_.set_xlim(x0, x1); a_.set_ylim(y0, y1); a_.set_xticks([]); a_.set_yticks([])
plt.tight_layout(); os.makedirs('docs/img', exist_ok=True); plt.savefig(f'docs/img/study-{DID}.png', dpi=55)
log('done')
