"""Building study, block by block, for a drawn Gidi district (written for d17 Saba and d19 Makoro, 27 Oct; the
building-study agent, .claude/agents/building-study.md).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d17_blocks.py d17 [--json out.json]

What it does (all real measures in real metres, UTM 31N, EPSG:32631; centroids also in Gidi metres):
1. The district outline (map/dNN/district.json) taken back to real metres: u = 500525 + 3x, v = 707825 + 3(10500 - y)
   (the inverse of scripts/working_bar.py's gidi()).
2. Real street blocks: the outline less Overture's street segments (classes in DIVIDE) and rail lines, each buffered to
   an ASSUMED full width per class (WIDTH below; Overture rarely carries a width here). Pieces of at least MIN_BLOCK m2
   are blocks; smaller pieces are counted together as slivers.
3. Google Open Buildings v3 inside each block at the confidence threshold for 90% precision of the S2 level-4 tile
   holding the district (thresholds/score_thresholds_s2_level_4.csv, the same reading as working_bar.py); also the
   count at the 80% threshold and at every confidence in the file. Count = buildings whose centroid is in the block;
   cover = the union of their footprints clipped to the block, over the block's area.
4. Storeys: each building's median 2.5D 2023 height (pixels with presence >= 0.5 and height > 0 inside its footprint,
   as scripts/draft_storeys.py), banded as draft_storeys.storeys(): max(1, (h + 1.5) // 3).
5. Land or water: ESA WorldCover 2021 (10 m, ~/gidi-data/research/data/worldcover) classes inside each block, and how
   many Google buildings have their centroid on a WorldCover permanent-water (80) pixel.
6. Overture places (count, categories, names) and land use (class and name) inside each block.
7. Our map: the block taken to Gidi metres (it is 1:3 there), our houses (map/dNN/plan.json) whose centroid is in it,
   their roof cover clipped to the block, their kinds and storeys, and the share of the block under our carriageways
   (each road's centreline buffered by width/2, flat ends, as working_bar.py).
"""
import collections
import csv
import gzip
import json
import os
import sys

import numpy as np
import pyarrow.parquet as pq
import rasterio
import shapely
from pyproj import Transformer
from rasterio.features import rasterize
from rasterio.windows import from_bounds
from shapely.geometry import LineString, MultiPolygon, Point, Polygon, box
from shapely.ops import unary_union
from shapely.strtree import STRtree

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
DATA = os.path.expanduser('~/gidi-data/research/data/')
GOOGLE = DATA + 'open-buildings-v3/lagos_open_buildings_v3.csv.gz'
THRESHOLDS = DATA + 'open-buildings-v3/thresholds/score_thresholds_s2_level_4.csv'
OB25 = DATA + 'open-buildings-2023/'
WORLDCOVER = DATA + 'worldcover/N06E003.tif'
OV = DATA + 'overture-lagos/'
RAIL = DATA + 'lagos_overture_ferry_and_rail_segments.parquet'

# assumed full carriageway widths, real metres, to cut the outline into blocks (not measured; a divider only)
WIDTH = {'motorway': 30, 'trunk': 24, 'primary': 18, 'secondary': 14, 'tertiary': 10, 'residential': 7,
         'unclassified': 7, 'living_street': 6}
DIVIDE = set(WIDTH)
RAIL_W = 10
MIN_BLOCK = 2000          # real m2
WC = {10: 'tree', 20: 'shrub', 30: 'grass', 40: 'crop', 50: 'built', 60: 'bare', 70: 'snow', 80: 'water',
      90: 'wetland', 95: 'mangrove', 100: 'moss'}

TU = Transformer.from_crs(4326, 32631, always_xy=True)
TL = Transformer.from_crs(32631, 4326, always_xy=True)


def g2u(x, y):
    return 500525 + 3 * x, 707825 + 3 * (10500 - y)


def u2g(u, v):
    return (u - 500525) / 3, 10500 - (v - 707825) / 3


def to_utm(geom):
    return shapely.transform(geom, lambda a: np.column_stack(TU.transform(a[:, 0], a[:, 1])))


def utm_to_gidi(geom):
    return shapely.transform(geom, lambda a: np.column_stack(u2g(a[:, 0], a[:, 1])))


def load(d):
    top = os.path.join(ROOT, 'map', d)
    recs = []
    for f in sorted(os.listdir(top)):
        if f.endswith('.json'):
            recs += json.load(open(os.path.join(top, f)))['records']
    D = next(r for r in recs if r['type'] == 'district')
    ring_g = MultiPolygon([Polygon(o) for o in D['outline']]).buffer(0)
    ring_u = shapely.transform(ring_g, lambda a: np.column_stack(g2u(a[:, 0], a[:, 1])))
    return D, recs, ring_g, ring_u


def lonlat_box(ring_u, pad=50):
    minx, miny, maxx, maxy = ring_u.buffer(pad).bounds
    w, s = TL.transform(minx, miny)
    e, n = TL.transform(maxx, maxy)
    return w, s, e, n


def segments(path, w, s, e, n, keep):
    t = pq.read_table(path, columns=['subtype', 'class', 'names', 'geometry', 'bbox'])
    out = []
    for r in t.to_pylist():
        b = r['bbox']
        if b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n:
            continue
        if keep(r):
            out.append((r, to_utm(shapely.from_wkb(r['geometry']))))
    return out


def blocks_of(ring_u, w, s, e, n):
    roads = segments(OV + 'lagos_overture_segment.parquet', w, s, e, n,
                     lambda r: r['subtype'] == 'road' and r['class'] in DIVIDE)
    rails = segments(RAIL, w, s, e, n, lambda r: r['subtype'] == 'rail')
    cut = unary_union([g.buffer(WIDTH[r['class']] / 2, cap_style=2) for r, g in roads] +
                      [g.buffer(RAIL_W / 2, cap_style=2) for r, g in rails])
    rest = ring_u.difference(cut)
    parts = list(getattr(rest, 'geoms', [rest]))
    big = [p for p in parts if p.area >= MIN_BLOCK]
    small = [p for p in parts if p.area < MIN_BLOCK]
    big.sort(key=lambda p: (-round(p.centroid.y / 150), p.centroid.x))      # north to south in 150 m bands, then west to east
    return big, small, roads, rails, cut


def threshold(lon, lat):
    for r in csv.DictReader(open(THRESHOLDS)):
        if shapely.from_wkt(r['geometry']).contains(Point(lon, lat)):
            return float(r['confidence_threshold_90%_precision']), float(r['confidence_threshold_80%_precision']), r['s2_token']
    raise SystemExit('no threshold tile holds the district')


def google(w, s, e, n):
    out = []
    with gzip.open(GOOGLE, 'rt') as f:
        for r in csv.DictReader(f):
            la, lo = float(r['latitude']), float(r['longitude'])
            if not (w <= lo <= e and s <= la <= n):
                continue
            g = to_utm(shapely.from_wkt(r['geometry']))
            out.append((float(r['confidence']), g))
    return out


def heights(polys):
    """Median 2.5D height per polygon index (None where no built pixels), read once over the polygons' extent."""
    out = [None] * len(polys)
    if not polys:
        return out
    ext = box(*unary_union([p.envelope for p in polys]).bounds)
    for t in sorted(f for f in os.listdir(OB25) if f.endswith('.tif')):
        r = rasterio.open(OB25 + t)
        if str(r.crs) != 'EPSG:32631' or not box(*r.bounds).intersects(ext):
            continue
        cl = box(*r.bounds).intersection(ext)
        win = from_bounds(*cl.bounds, r.transform).round_offsets().round_lengths()
        if win.width < 1 or win.height < 1:
            continue
        _, H, P = r.read(window=win, boundless=True, fill_value=0)
        idx = [i for i, p in enumerate(polys) if out[i] is None and box(*r.bounds).contains(p.centroid)]
        lab = rasterize([(polys[i], i + 1) for i in idx], out_shape=H.shape, transform=r.window_transform(win),
                        dtype='int32', all_touched=True)
        ok = (lab > 0) & (P >= 0.5) & (H > 0)
        L, V = lab[ok], H[ok]
        order = np.argsort(L, kind='stable')
        L, V = L[order], V[order]
        uniq, start = np.unique(L, return_index=True)
        ends = list(start[1:]) + [len(L)]
        for u, a, b in zip(uniq, start, ends):
            out[u - 1] = float(np.median(V[a:b]))
    return out


def storeys(h):
    return max(1, int((h + 1.5) // 3))


def worldcover(geoms_u):
    """For each real-metre polygon, a Counter of WorldCover class pixels; plus a sampler for points."""
    r = rasterio.open(WORLDCOVER)
    ext = unary_union([g.envelope for g in geoms_u]).bounds
    w, s = TL.transform(ext[0], ext[1])
    e, n = TL.transform(ext[2], ext[3])
    win = from_bounds(w, s, e, n, r.transform).round_offsets().round_lengths()
    A = r.read(1, window=win, boundless=True, fill_value=0)
    tr = r.window_transform(win)
    to_ll = lambda g: shapely.transform(g, lambda a: np.column_stack(TL.transform(a[:, 0], a[:, 1])))
    res = []
    for g in geoms_u:
        m = rasterize([(to_ll(g), 1)], out_shape=A.shape, transform=tr, dtype='uint8')
        v, c = np.unique(A[m.astype(bool)], return_counts=True)
        res.append(collections.Counter({WC.get(int(k), str(k)): int(n) for k, n in zip(v, c)}))

    def at(pts_u):
        lo, la = TL.transform(np.array([p.x for p in pts_u]), np.array([p.y for p in pts_u]))
        rows, cols = rasterio.transform.rowcol(tr, lo, la)
        rows, cols = np.clip(rows, 0, A.shape[0] - 1), np.clip(cols, 0, A.shape[1] - 1)
        return A[rows, cols]
    return res, at


def places(w, s, e, n):
    t = pq.read_table(OV + 'lagos_overture_place.parquet', columns=['taxonomy', 'names', 'geometry', 'bbox', 'confidence'])
    out = []
    for r in t.to_pylist():
        b = r['bbox']
        if b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n:
            continue
        g = to_utm(shapely.from_wkb(r['geometry']))
        out.append(((r['taxonomy'] or {}).get('primary'), (r['names'] or {}).get('primary'), r['confidence'], g))
    return out


def landuse(w, s, e, n):
    out = []
    for f in ('lagos_overture_land_use.parquet', 'lagos_overture_land.parquet'):
        t = pq.read_table(OV + f, columns=['subtype', 'class', 'names', 'geometry', 'bbox'])
        for r in t.to_pylist():
            b = r['bbox']
            if b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n:
                continue
            g = to_utm(shapely.from_wkb(r['geometry']))
            if g.geom_type in ('Polygon', 'MultiPolygon'):
                out.append((f.split('_')[2].split('.')[0], r['subtype'], r['class'], (r['names'] or {}).get('primary'), g.buffer(0)))
    return out


def study(d):
    D, recs, ring_g, ring_u = load(d)
    w, s, e, n = lonlat_box(ring_u)
    c_lon, c_lat = TL.transform(ring_u.centroid.x, ring_u.centroid.y)
    t90, t80, tok = threshold(c_lon, c_lat)
    blocks, slivers, roads, rails, cut = blocks_of(ring_u, w, s, e, n)
    G = google(w, s, e, n)
    G = [(c, g) for c, g in G if ring_u.intersects(g)]
    g90 = [g for c, g in G if c >= t90]
    hs = heights(g90)
    wc_cls, wc_at = worldcover(blocks + [ring_u])
    wc_pt = wc_at([g.centroid for g in g90]) if g90 else np.array([])
    allc = [c for c, g in G]
    gc = [g.centroid for c, g in G]
    tree_all = STRtree(gc)
    tree90 = STRtree([g.centroid for g in g90])
    P = [p for p in places(w, s, e, n) if ring_u.contains(p[3])]
    LU = [l for l in landuse(w, s, e, n) if l[4].intersects(ring_u)]
    houses = [r for r in recs if r['type'] == 'building']
    HP = [Polygon(h['footprint']) for h in houses]
    htree = STRtree([p.centroid for p in HP])
    OU = unary_union(HP)
    roads_g = [r for r in recs if r['type'] == 'road']
    CW = unary_union([LineString([q[:2] for q in r['centreline']]).buffer(r['width'] / 2, cap_style=2) for r in roads_g])

    def measure(bk, wc):
        i90 = [i for i in tree90.query(bk) if bk.contains(g90[i].centroid)]
        ia = [i for i in tree_all.query(bk) if bk.contains(gc[i])]
        polys = [g90[i] for i in i90]
        areas = sorted(p.area for p in polys)
        cover = unary_union(polys).intersection(bk).area / bk.area if polys else 0.0
        hh = [hs[i] for i in i90 if hs[i] is not None]
        st = collections.Counter(storeys(h) for h in hh)
        on_water = int(sum(1 for i in i90 if wc_pt[i] == 80))
        pl = [p for p in P if bk.contains(p[3])]
        lu = []
        for src, sub, cl, nm, g in LU:
            a = g.intersection(bk).area
            if a > 0.2 * bk.area or (g.area > 0 and a > 0.5 * g.area and a > 300):
                lu.append((src, sub, cl, nm, round(a / bk.area, 2)))
        bg = utm_to_gidi(bk)
        ih = [i for i in htree.query(bg) if bg.contains(HP[i].centroid)]
        ours_cover = OU.intersection(bg).area / bg.area
        return {
            'centroid_gidi': [round(v) for v in u2g(bk.centroid.x, bk.centroid.y)],
            'centroid_lonlat': [round(v, 5) for v in TL.transform(bk.centroid.x, bk.centroid.y)],
            'area_real_m2': round(bk.area), 'area_gidi_m2': round(bg.area),
            'n90': len(i90), 'n80': sum(1 for i in ia if allc[i] >= t80), 'n_all': len(ia),
            'per_ha': round(len(i90) / (bk.area / 1e4), 1),
            'cover90': round(cover, 3),
            'median_m2': round(float(np.median(areas)), 1) if areas else None,
            'p90_m2': round(float(np.percentile(areas, 90)), 1) if areas else None,
            'max_m2': round(areas[-1]) if areas else None,
            'n_under_40m2': sum(1 for a in areas if a < 40), 'n_over_500m2': sum(1 for a in areas if a >= 500),
            'heights_read': len(hh), 'median_h': round(float(np.median(hh)), 1) if hh else None,
            'storeys': dict(sorted(st.items())),
            'on_water_pixel': on_water,
            'worldcover': {k: round(v / max(1, sum(wc.values())), 2) for k, v in wc.most_common()},
            'places': len(pl),
            'place_cats': collections.Counter(p[0] for p in pl).most_common(6),
            'place_names': [(p[0], p[1]) for p in pl if p[1]],
            'landuse': lu,
            'ours_n': len(ih), 'ours_cover': round(ours_cover, 3),
            'ours_kinds': dict(collections.Counter(houses[i]['kind'] for i in ih).most_common()),
            'ours_storeys': dict(sorted(collections.Counter(houses[i]['storeys'] for i in ih).items())),
            'ours_carriageway_share': round(CW.intersection(bg).area / bg.area, 3),
        }

    rows = [dict(block=f'{d.upper()}-{k + 1:02d}', **measure(bk, wc)) for k, (bk, wc) in enumerate(zip(blocks, wc_cls))]
    whole = measure(ring_u, wc_cls[-1])
    sl = unary_union(slivers) if slivers else Polygon()
    real_cut = ring_u.intersection(cut).area / ring_u.area
    summary = {
        'district': d, 'name': D.get('name'), 'threshold_tile': tok, 't90': t90, 't80': t80,
        'outline_real_m2': round(ring_u.area), 'outline_gidi_m2': round(ring_g.area),
        'bbox_lonlat': [round(v, 5) for v in (w, s, e, n)],
        'blocks': len(blocks), 'slivers': len(slivers), 'sliver_real_m2': round(sl.area),
        'real_street_share_assumed_widths': round(real_cut, 3),
        'overture_divider_segments': len(roads), 'rail_segments': len(rails),
        'google_in_outline_any_conf': len(G), 'google_90': len(g90),
        'google_conf_hist': np.histogram(allc, bins=[0.65, 0.70, t90, 0.80, 0.90, 1.0])[0].tolist(),
        'heights_read_90': sum(1 for h in hs if h is not None),
        'whole': whole,
    }
    return summary, rows


def main():
    ds = [a for a in sys.argv[1:] if a.startswith('d') and a[1:].isdigit()]
    out = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
    res = {}
    for d in ds:
        summary, rows = study(d)
        res[d] = {'summary': summary, 'blocks': rows}
        print(json.dumps(summary, ensure_ascii=False, default=str))
        for r in rows:
            print(json.dumps(r, ensure_ascii=False, default=str))
    if out:
        json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1, default=str)


if __name__ == '__main__':
    main()
