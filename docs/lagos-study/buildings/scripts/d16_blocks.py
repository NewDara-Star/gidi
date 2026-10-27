"""d16 Ìbùdó Mẹ́ta: the real street blocks and their buildings (building-study agent, 27 Oct 2026). Study only.

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d16_blocks.py [--md]

1. The outline: map/d16/district.json (Gidi metres; real positions moved in with scripts/working_bar.py's gidi()).
2. Real street blocks: the outline less Overture's real streets (road classes motorway..unclassified, the same set as
   working_bar.py's STREET_CLASSES, and the rail lines), each line cut 0.5 m either side (1.5 m real); the parts of a
   segment Overture flags `is_bridge` are left out (a bridge deck does not split the land under it). Blocks under
   MIN_BLOCK m2 (Gidi) are dropped and counted.
3. Per block, Google Open Buildings v3 at the tile's 90%-precision threshold (and the 80% one for the cover range,
   thresholds/score_thresholds_s2_level_4.csv): count (centroid in block), cover (footprints cut to the block), median
   and largest footprint (Google's area_in_meters, real m2). Storeys from Open Buildings 2.5D Temporal 2023: each
   footprint's median height over its pixels with presence >= 0.5 (bands read as scripts/draft_storeys.py reads them:
   _, height, presence), storeys = max(1, (h + 1.5) // 3) (the same bands as draft_storeys.py).
4. Overture places (point in block) and land use (polygon share in block).
5. Our map: buildings of map/d16 with centroid in the block, their cover (cut to the block), kinds and storeys.

Gidi's map is 1:3 in position but houses are real size, so a Gidi block holds about a ninth of its real twin's houses
at the same cover: 'real n /9' is printed beside our count.
"""
import collections
import csv
import gzip
import json
import os
import re
import statistics
import sys

import numpy as np
import pyarrow.parquet as pq
import rasterio
import shapely
from pyproj import Transformer
from rasterio.features import rasterize
from rasterio.windows import from_bounds
from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import substring, unary_union
from shapely.strtree import STRtree

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from working_bar import GOOGLE, OVERTURE, STREET_CLASSES, THRESHOLDS, gidi  # noqa: E402

D = 'd16'
WC = {10: 'trees', 20: 'shrub', 30: 'grass', 40: 'crops', 50: 'built', 60: 'bare', 80: 'water', 90: 'wetland', 95: 'mangrove'}
WORLDCOVER = os.path.expanduser('~/gidi-data/research/data/worldcover/N06E003.tif')
TILE = os.path.expanduser('~/gidi-data/research/data/open-buildings-2023/tile_qNSfrvnK9X8.tif')  # wholly covers d16
CUT = 0.5          # m (Gidi) either side of a real street line
MIN_BLOCK = 300.0  # m2 (Gidi): smaller pieces are slivers between close lines
BIG = 8000.0       # m2 (Gidi): a block this big is cut again (minor ways, then a grid)
GRID = 80.0        # m (Gidi), the grid's square (240 m real)


def bridge_free(line, flags):
    """The parts of a segment not flagged is_bridge (Overture road_flags, ranges as fractions of its length)."""
    rng = sorted(tuple(f['between']) for f in (flags or []) if 'is_bridge' in (f.get('values') or []) and f.get('between'))
    if any(not f.get('between') and 'is_bridge' in (f.get('values') or []) for f in (flags or [])):
        return []
    out, t = [], 0.0
    for a, b in rng:
        if a > t:
            out.append(substring(line, t, a, normalized=True))
        t = max(t, b)
    if t < 1:
        out.append(substring(line, t, 1, normalized=True))
    return [g for g in out if g.length > 0]


def main():
    T = Transformer.from_crs(4326, 32631, always_xy=True)
    inv = Transformer.from_crs(32631, 4326, always_xy=True)
    recs = []
    top = os.path.join(ROOT, 'map', D)
    for f in sorted(os.listdir(top)):
        if f.endswith('.json'):
            recs += json.load(open(os.path.join(top, f)))['records']
    dist = next(r for r in recs if r['type'] == 'district')
    ring = MultiPolygon([Polygon(o) for o in dist['outline']]).buffer(0)
    minx, miny, maxx, maxy = ring.buffer(100).bounds
    (w, n), (e, s) = inv.transform(500525 + 3 * minx, 707825 + 3 * (10500 - miny)), inv.transform(500525 + 3 * maxx, 707825 + 3 * (10500 - maxy))
    inside = lambda b: not (b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n)

    # real streets and rail, bridges left out; minor ways (service, path, footway, track) kept to split the big blocks
    seg = pq.read_table(os.path.join(OVERTURE, 'lagos_overture_segment.parquet'),
                        columns=['subtype', 'class', 'road_flags', 'names', 'geometry', 'bbox']).to_pylist()
    cuts, minor, named = [], [], []
    for r in seg:
        if not inside(r['bbox']) or r['subtype'] not in ('road', 'rail'):
            continue
        street = r['subtype'] == 'rail' or r['class'] in STREET_CLASSES
        g = shapely.from_wkb(r['geometry'])
        L = LineString([gidi(x, y, T) for x, y in g.coords])
        for p in bridge_free(L, r['road_flags']):
            (cuts if street else minor).append(p.buffer(CUT, cap_style=2))
            if street:
                named.append((p, (r['names'] or {}).get('primary'), r['class']))
    parts = ring.difference(unary_union(cuts))
    parts = [(p, 'street') for p in getattr(parts, 'geoms', [parts])]
    # a block over BIG is cut again by the minor ways, then what is still over BIG by a GRID m square grid (cells,
    # not real blocks: the real streets there are missing from Overture)
    mu = unary_union(minor)
    out = []
    big = sorted([p for p, _ in parts if p.area > BIG], key=lambda p: -p.area)
    BIGS = []      # (label, area, polygon) of the blocks too big to read whole
    for p, how in parts:
        if p.area > BIG:
            BIGS.append((f'M{big.index(p) + 1}', p.area, p))
            how = f'M{big.index(p) + 1}'
        if p.area <= BIG:
            out.append((p, how))
            continue
        q = p.difference(mu)
        for a in getattr(q, 'geoms', [q]):
            if a.area <= BIG:
                out.append((a, f'{how} minor way'))
                continue
            x0, y0, x1, y1 = a.bounds
            cells = []
            for i in range(int((x1 - x0) // GRID) + 1):
                for j in range(int((y1 - y0) // GRID) + 1):
                    c = a.intersection(shapely.box(x0 + i * GRID, y0 + j * GRID, x0 + (i + 1) * GRID, y0 + (j + 1) * GRID))
                    cells += [cc for cc in getattr(c, 'geoms', [c]) if cc.geom_type == 'Polygon' and not cc.is_empty]
            # a cell under MIN_BLOCK joins the neighbour it shares the longest edge with
            cells.sort(key=lambda c: c.area)
            while cells and cells[0].area < MIN_BLOCK:
                c = cells.pop(0)
                nb = max(range(len(cells)), key=lambda k: c.buffer(0.01).intersection(cells[k]).area, default=None)
                if nb is None or c.buffer(0.01).intersection(cells[nb]).area == 0:
                    out.append((c, f'{how} grid'))
                    continue
                cells[nb] = unary_union([cells[nb], c]).buffer(0)
                cells.sort(key=lambda c: c.area)
            out += [(c, f'{how} grid') for c in cells]
    blocks = sorted([(p, h) for p, h in out if p.area >= MIN_BLOCK],
                    key=lambda t: (t[1] != 'street', t[1].split()[0], round(t[0].centroid.y / 150), t[0].centroid.x))
    slivers = [p for p, h in out if p.area < MIN_BLOCK]
    hows = [h for _, h in blocks]
    blocks = [p for p, _ in blocks]

    # Google v3
    t80 = t90 = None
    lon0, lat0 = inv.transform(500525 + 3 * ring.centroid.x, 707825 + 3 * (10500 - ring.centroid.y))
    for r in csv.DictReader(open(THRESHOLDS)):
        if shapely.from_wkt(r['geometry']).contains(Point(lon0, lat0)):
            t80, t90 = float(r['confidence_threshold_80%_precision']), float(r['confidence_threshold_90%_precision'])
    G = []   # (gidi polygon, utm polygon, area m2, conf)
    with gzip.open(GOOGLE, 'rt') as f:
        for r in csv.DictReader(f):
            c, la, lo = float(r['confidence']), float(r['latitude']), float(r['longitude'])
            if c < t80 or not (w <= lo <= e and s <= la <= n):
                continue
            g = shapely.from_wkt(r['geometry'])
            G.append((shapely.transform(g, lambda a: np.array([gidi(x, y, T) for x, y in a])),
                      shapely.transform(g, lambda a: np.column_stack(T.transform(a[:, 0], a[:, 1]))),
                      float(r['area_in_meters']), c))
    G = [x for x in G if ring.intersects(x[0])]

    # 2.5D heights per Google footprint (90% set)
    hi = [i for i, x in enumerate(G) if x[3] >= t90]
    H = {}
    with rasterio.open(TILE) as rr:
        ub = unary_union([G[i][1] for i in hi]).bounds
        win = from_bounds(*ub, rr.transform).round_offsets().round_lengths()
        Hb = rr.read(2, window=win, boundless=True, fill_value=0)
        Pb = rr.read(3, window=win, boundless=True, fill_value=0)
        lab = rasterize([(G[i][1], k + 1) for k, i in enumerate(hi)], out_shape=Hb.shape,
                        transform=rr.window_transform(win), dtype='int32', all_touched=True)
    m = (lab > 0) & (Pb >= 0.5) & (Hb > 0)
    L_, H_ = lab[m], Hb[m]
    o = np.argsort(L_, kind='stable')
    L_, H_ = L_[o], H_[o]
    ids, starts = np.unique(L_, return_index=True)
    for k, a, b in zip(ids, starts, list(starts[1:]) + [len(L_)]):
        H[hi[k - 1]] = float(np.median(H_[a:b]))
    st = lambda h: max(1, int((h + 1.5) // 3))
    print(f'# 2.5D band check: presence max {float(Pb.max()):.2f}, height max {float(Hb.max()):.1f} m, '
          f'footprints with a height {len(H)} of {len(hi)}', file=sys.stderr)

    # Overture places and land use
    pl = pq.read_table(os.path.join(OVERTURE, 'lagos_overture_place.parquet'),
                       columns=['taxonomy', 'names', 'geometry', 'bbox']).to_pylist()
    P = []
    for r in pl:
        if not inside(r['bbox']):
            continue
        g = shapely.from_wkb(r['geometry'])
        p = Point(gidi(g.x, g.y, T))
        if ring.contains(p):
            P.append((p, (r['taxonomy'] or {}).get('primary'), (r['names'] or {}).get('primary')))
    lu = pq.read_table(os.path.join(OVERTURE, 'lagos_overture_land_use.parquet'),
                       columns=['subtype', 'class', 'names', 'geometry', 'bbox']).to_pylist()
    LU = []
    for r in lu:
        if not inside(r['bbox']):
            continue
        g = shapely.from_wkb(r['geometry'])
        if g.geom_type not in ('Polygon', 'MultiPolygon'):
            continue
        b = r['bbox']
        if b['xmax'] - b['xmin'] > 0.2 or b['ymax'] - b['ymin'] > 0.2:
            continue     # a world-sized polygon (Overture has a marine monument whose box wraps the globe)
        gg = shapely.transform(g, lambda a: np.array([gidi(x, y, T) for x, y in a])).buffer(0)
        if gg.intersects(ring):
            LU.append((gg, r['class'], (r['names'] or {}).get('primary')))

    # ESA WorldCover 2021 (10 m): each pixel's centre moved into Gidi metres, the share of each class per block
    with rasterio.open(WORLDCOVER) as wc:
        win = from_bounds(w, s, e, n, wc.transform).round_offsets().round_lengths()
        A = wc.read(1, window=win)
        tf = wc.window_transform(win)
    jj, ii = np.meshgrid(np.arange(A.shape[1]), np.arange(A.shape[0]))
    lon_, lat_ = rasterio.transform.xy(tf, ii.ravel(), jj.ravel())
    U, V = T.transform(np.asarray(lon_), np.asarray(lat_))
    WX, WY, WA = (U - 500525) / 3, 10500 - (V - 707825) / 3, A.ravel()

    # our map
    OB = [r for r in recs if r['type'] == 'building']
    OP = [Polygon(b['footprint']) for b in OB]

    gt = STRtree([x[0] for x in G])
    rows = []
    for bi, bk in enumerate(blocks, 1):
        cand = [G[i] + (i,) for i in gt.query(bk)]
        g90 = [x for x in cand if x[3] >= t90]
        cnt = [x for x in g90 if bk.contains(x[0].centroid)]
        cov90 = unary_union([x[0] for x in g90]).intersection(bk).area / bk.area if g90 else 0
        cov80 = unary_union([x[0] for x in cand]).intersection(bk).area / bk.area if cand else 0
        areas = [x[2] for x in cnt]
        hs = [H[x[4]] for x in cnt if x[4] in H]
        sts = [st(h) for h in hs]
        sc = collections.Counter(min(s_, 4) for s_ in sts)
        pin = [(c, nm) for p, c, nm in P if bk.contains(p)]
        lus = []
        for gg, c, nm in LU:
            a = gg.intersection(bk).area
            if a > 0.1 * bk.area or (gg.area and a > 0.5 * gg.area):
                lus.append((c, nm, a / bk.area))
        ours = [(b, p) for b, p in zip(OB, OP) if bk.contains(p.centroid)]
        ocov = unary_union([p for p in OP if p.intersects(bk)]).intersection(bk).area / bk.area if OP else 0
        inb = shapely.contains_xy(bk, WX, WY)
        wcc = collections.Counter(WA[inb].tolist())
        wct = sum(wcc.values()) or 1
        wcs = {WC[k]: v / wct for k, v in wcc.items() if k in WC}
        touches = sorted({c for L, nm, c in named if L.distance(bk) < CUT + 0.6})
        rows.append(dict(
            id=f'B{bi:03d}' if hows[bi - 1] == 'street' else f"{hows[bi - 1].split()[0]}-{sum(1 for h in hows[:bi] if h.split()[0] == hows[bi - 1].split()[0]):02d}",
            how=hows[bi - 1], x=round(bk.centroid.x), y=round(bk.centroid.y), area=round(bk.area),
            n=len(cnt), cov90=cov90, cov80=cov80,
            med=round(statistics.median(areas)) if areas else 0, max=round(max(areas)) if areas else 0,
            nh=len(hs), hmed=round(statistics.median(hs), 1) if hs else None,
            smed=st(statistics.median(hs)) if hs else None,
            s1=sc[1], s2=sc[2], s3=sc[3], s4=sc[4],
            places=pin, lu=lus, wc=wcs, touches=touches,
            ours_n=len(ours), ours_cov=ocov,
            ours_kinds=collections.Counter(b['kind'] for b, _ in ours),
            ours_st=statistics.median([b['storeys'] for b, _ in ours]) if ours else None,
            ours_med=round(statistics.median([p.area for _, p in ours])) if ours else 0))

    # district totals
    g90all = [x for x in G if x[3] >= t90]
    tot = dict(
        outline=ring.area, blocks=len(blocks), block_area=sum(b.area for b in blocks), slivers=len(slivers),
        sliver_area=sum(p.area for p in slivers),
        n90=sum(1 for x in g90all if ring.contains(x[0].centroid)),
        cov90=unary_union([x[0] for x in g90all]).intersection(ring).area / ring.area,
        cov80=unary_union([x[0] for x in G]).intersection(ring).area / ring.area,
        med=statistics.median([x[2] for x in g90all if ring.contains(x[0].centroid)]),
        storeys=collections.Counter(min(st(H[i]), 4) for i in H if ring.contains(G[i][0].centroid)),
        ours_cov=unary_union(OP).intersection(ring).area / ring.area, ours_n=len(OB),
        ours_med=statistics.median([p.area for p in OP]), places=len(P), t80=t80, t90=t90,
        bigs=[(l, a, round(p.centroid.x), round(p.centroid.y)) for l, a, p in BIGS])
    return rows, tot


def fmt(rows, tot):
    print(f"outline {tot['outline']:.0f} m2 (Gidi); {tot['blocks']} blocks over {tot['block_area']:.0f} m2; "
          f"{tot['slivers']} slivers under {MIN_BLOCK:.0f} m2 dropped ({tot['sliver_area']:.0f} m2); thresholds {tot['t90']}/{tot['t80']}")
    print('too big to read whole (cut by minor ways, then a grid): ' + '; '.join(f'{l} {a:,.0f} m2 at ({x},{y})' for l, a, x, y in tot['bigs']))
    print(f"Google: {tot['n90']} buildings (centroid inside, at 90%), cover {tot['cov90']:.2%} (90%) - {tot['cov80']:.2%} (80%), "
          f"median {tot['med']:.0f} m2; storeys (1,2,3,4+) {dict(sorted(tot['storeys'].items()))}")
    print(f"ours: {tot['ours_n']} houses, cover {tot['ours_cov']:.2%}, median footprint {tot['ours_med']:.0f} m2; Overture places {tot['places']}")
    for r in rows:
        cats = collections.Counter(c for c, _ in r['places'])
        print(f"{r['id']} {r['how']} ({r['x']},{r['y']}) {r['area']} m2 | wc { {k: round(v, 2) for k, v in r['wc'].items() if v >= 0.05} } | n {r['n']} (/9 {r['n'] / 9:.0f}) | cover {r['cov90']:.0%}-{r['cov80']:.0%} "
              f"| med {r['med']} max {r['max']} | h med {r['hmed']} m, st {r['smed']} [1:{r['s1']} 2:{r['s2']} 3:{r['s3']} 4+:{r['s4']}] "
              f"| roads {','.join(r['touches'])} | LU {[(c, nm, round(a, 2)) for c, nm, a in r['lu']]} "
              f"| places {len(r['places'])} {dict(cats.most_common(4))} "
              f"| ours n {r['ours_n']} cover {r['ours_cov']:.0%} med {r['ours_med']} st {r['ours_st']} {dict(r['ours_kinds'])}")
        nm = [f'{c}: {x}' for c, x in r['places'] if x and re.search(
            r'church|mosque|school|college|market|hospital|medical|clinic|hotel|terminal|station|factory|company|limited|ltd|'
            r'house|estate|plaza|complex|mission|cathedral|park|nrc|railway|bank|police|hall|centre|center', f'{c} {x}', re.I)]
        if nm:
            print('   named: ' + '; '.join(nm[:14]))


INST = (r'church|cathedral|chapel|mosque|masjid|school|college|academy|market|hospital|medical cent|clinic|hotel|'
        r'terminal|terminus|station|estate|factory|industr|manufactur|mission|hall|nrc|railway|police|museum|house\b|plaza|complex|bank\b')
INST_CATS = {'christian_place_of_worship', 'muslim_place_of_worship', 'religious_organization', 'school', 'elementary_school',
             'high_school', 'college_university', 'hospital', 'train_station', 'bus_station', 'hotel', 'police_station',
             'industrial_company', 'manufacturer', 'museum', 'historic_site', 'shopping_mall', 'government_office',
             'public_and_government_association', 'warehouse', 'market'}
ELSEWHERE = (r'ladipo|ikeja|alausa|isolo|shomolu|oniru|ogba|akoka|badagry|oworonshoki|treasure city|ijero|abaranje|'
             r'marina|npa')   # names of places outside d16 seen on d16 points
SHOPS = r'store|shop|restaurant|eatery|salon|pharmacy|bank|bar\b|food|boutique|retail|fashion|clothing|market|supermarket|mobile_phone|auto_parts'


def fabric(r):
    """A reading of the block's fabric from its numbers (rules stated in the study file, not measured facts)."""
    lu = collections.Counter()
    for c, _, a in r['lu']:
        lu[c] += a
    nm = ' '.join(f'{c} {x or ""}' for c, x in r['places'])
    shops = sum(1 for c, _ in r['places'] if c and re.search(SHOPS, c))
    main = bool({'trunk', 'primary', 'secondary'} & set(r['touches']))
    nh = r['nh'] or 1
    tall = (r['s3'] + r['s4']) / nh
    dens = r['n'] / r['area'] * 1000          # Google buildings per 1,000 m2 of Gidi block (9,000 m2 real)
    station = any(c == 'train_station' or re.search(r'terminus', x or '', re.I) for c, x in r['places'])
    market = lu.get('retail', 0) >= 0.3 or any(re.search(r'\bmarket\b', x or '', re.I) and not re.search(ELSEWHERE, x or '', re.I)
                                               for c, x in r['places'])
    if r['wc'].get('water', 0) + r['wc'].get('wetland', 0) >= 0.5 and r['n'] < 5:
        f, k, g = 'water (lagoon edge)', [], []
    elif station:
        f, k, g = 'railway station', ['station_hall', 'shed'], ['workshop']
    elif lu.get('railway', 0) >= 0.3:
        f, k, g = 'railway land', ['shed', 'station_hall'], ['workshop']
    elif lu.get('cemetery', 0) >= 0.3:
        f, k, g = 'cemetery (open ground)', [], []
    elif lu.get('school', 0) >= 0.3:
        f, k, g = 'school ground', ['school'], ['home']
    elif r['n'] < 5 and r['cov90'] < 0.10:
        f, k, g = 'open ground', [], []
    elif r['n'] >= 10 and r['med'] < 60:
        f, k, g = 'shacks and small sheds (low, under 60 m2)', ['shack', 'face_me_bungalow'], ['home', 'workshop']
    elif (lu.get('industrial', 0) >= 0.3 or lu.get('brownfield', 0) >= 0.3) and dens < 15:
        f, k, g = 'sheds and yards', ['shed', 'kiosk_row'], ['workshop', 'lock_ups']
    elif market and r['cov90'] >= 0.25:
        f, k, g = 'market', ['market_block', 'kiosk_row', 'shop_under_flats'], ['open_stalls', 'lock_ups']
    elif r['cov90'] < 0.10:
        f, k, g = 'open ground with a few houses', ['face_me_bungalow', 'shack'], ['home']
    elif r['med'] < 75 and r['cov90'] >= 0.35:
        f, k, g = 'packed small houses (face-me-I-face-you, shacks)', ['face_me_bungalow', 'shack'], ['home']
    elif r['smed'] and (r['smed'] >= 3 or tall >= 0.4):
        f, k, g = 'walk-up flats', ['walkup', 'shop_under_flats'], ['flats', 'lock_ups']
    elif r['med'] >= 200:
        f, k, g = 'big old houses and compounds', ['compound_house', 'colonial_house', 'walkup'], ['home', 'flats']
    else:
        f, k, g = 'compound houses, face-me-I-face-you', ['compound_house', 'face_me_bungalow'], ['home']
    for c in ('industrial', 'brownfield'):
        if lu.get(c, 0) >= 0.3 and not f.startswith('sheds'):
            f += f' (Overture land use: {c})'
    if (main or shops >= 4) and not re.match(r'water|open ground|cemetery|school|railway', f):
        f += ', shops on the front'
        k = k + [x for x in ['shop_under_flats'] if x not in k]
        g = g + [x for x in ['lock_ups'] if x not in g]
    if re.search(r'church|cathedral|chapel', nm, re.I) and 'church' not in k:
        k = k + ['church']
    if re.search(r'mosque|masjid', nm, re.I):
        k = k + ['mosque']
    return f, k, g


def named(r):
    out = []
    for c, x in r['places']:
        if x and (c in INST_CATS or re.search(INST, x, re.I)) and x not in out:
            out.append(x + (' [names elsewhere]' if re.search(ELSEWHERE, x, re.I) else ''))
    out += [f'{x} (land use {c})' for c, x, _ in r['lu'] if x]
    return out


def md(rows, tot):
    print('| block | cut by | centroid (Gidi m) | area m2 Gidi | land cover (WorldCover) | Google n (/9) | cover 90-80% | median / largest m2 | storeys median [1/2/3/4+] '
          '| fabric (reading) | map kinds; ground floors | named (Overture) | ours: n, cover, kinds |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r in rows:
        f, k, g = fabric(r)
        nm = named(r)
        ok = ', '.join(f'{a} {b}' for a, b in r['ours_kinds'].most_common())
        st_ = f"{r['smed']} ({r['hmed']} m) [{r['s1']}/{r['s2']}/{r['s3']}/{r['s4']}]" if r['smed'] else 'none read'
        lc = ', '.join(f'{k_} {v:.0%}' for k_, v in sorted(r['wc'].items(), key=lambda t: -t[1]) if v >= 0.1) or '-'
        print(f"| {r['id']} | {r['how']} | {r['x']}, {r['y']} | {r['area']:,} | {lc} | {r['n']} ({r['n'] / 9:.0f}) | {r['cov90']:.0%}-{r['cov80']:.0%} "
              f"| {r['med']} / {r['max']:,} | {st_} | {f} | {', '.join(k) or '-'}; {', '.join(g) or '-'} "
              f"| {'; '.join(nm[:4]) + (f' (+{len(nm) - 4})' if len(nm) > 4 else '') if nm else '-'} "
              f"| {r['ours_n']}, {r['ours_cov']:.0%}{', ' + ok if ok else ''} |")
    fc = collections.Counter()
    fa = collections.Counter()
    for r in rows:
        f = re.split(r', shops| \(Overture', fabric(r)[0])[0]
        fc[f] += 1
        fa[f] += r['area']
    print()
    for f, c in fc.most_common():
        print(f'- {f}: {c} blocks, {fa[f]:,} m2 ({fa[f] / tot["block_area"]:.0%})')
    # roof area, Google's (90%) against ours, by fabric and by the big blocks
    print()
    print('| group | area m2 | Google cover (roof m2) | our cover (roof m2) | short m2 | Google n (/9) | our n |')
    print('|---|---|---|---|---|---|---|')
    g = collections.defaultdict(lambda: [0.0] * 5)
    for r in rows:
        f = re.split(r', shops| \(Overture', fabric(r)[0])[0]
        for key in (f, 'street blocks (B)' if r['how'] == 'street' else r['how'].split()[0]):
            a = g[key]
            a[0] += r['area']; a[1] += r['cov90'] * r['area']; a[2] += r['ours_cov'] * r['area']; a[3] += r['n']; a[4] += r['ours_n']
    for k, (A, G_, O, n_, on) in sorted(g.items(), key=lambda t: -(t[1][1] - t[1][2])):
        print(f'| {k} | {A:,.0f} | {G_ / A:.0%} ({G_:,.0f}) | {O / A:.0%} ({O:,.0f}) | {G_ - O:,.0f} | {n_:.0f} ({n_ / 9:.0f}) | {on:.0f} |')


if __name__ == '__main__':
    rows, tot = main()
    fmt(rows, tot)
    if '--md' in sys.argv:
        print()
        md(rows, tot)
