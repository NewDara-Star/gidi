"""Makoro (d19): land or water under its buildings, in 100 m real cells (building study, 27 Oct).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d19_water.py [--json out.json]

The block study (d17_blocks.py d19) leaves Makoro's east as one 1.3 km2 block, as Overture has no street there. This
cuts the district into 100 m x 100 m real cells (33 m in Gidi) and, for each, reads:
  - Google Open Buildings v3 at the tile's 90%-precision threshold (0.749) and at every confidence: count, cover,
    median footprint; 2.5D 2023 median heights (as d17_blocks.py);
  - ESA WorldCover 2021 (10 m): the share of water (class 80) and built (50) pixels;
  - Copernicus GLO-30 DSM (1 arc-second, ~30 m; ~/gidi-data/research/data/dem): the median surface height, and the
    share of pixels at exactly 0 m, which is where the DSM's water-body editing flattened water (the open lagoon);
    a surface under 3 m with buildings on it is read as low ground or water under stilts, not as solid made ground;
  - Google buildings whose centroid is on a DSM pixel under 3 m, and on an exactly-0 pixel.
(Overture's land polygon, land/land, was tried first and is no help: it is the land side of OpenStreetMap's sea
coastline and holds the whole Lagos Lagoon, e.g. 3.41 E 6.49 N, as land.)
  - our map's houses (count, cover) in the same cell taken to Gidi metres.
Prints one line per cell with buildings, then totals east and west of the coastline.
"""
import collections
import json
import os
import sys

import numpy as np
import pyarrow.parquet as pq
import shapely
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely.strtree import STRtree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B

CELL = 100


DSM = os.path.expanduser('~/gidi-data/research/data/dem/Copernicus_DSM_COG_10_N06_00_E003_00_DEM.tif')
LOW = 3.0


class Raster:
    """A lon/lat raster window over the district, sampled at real-metre points or summarised over real polygons."""
    def __init__(self, path, w, s, e, n):
        import rasterio
        from rasterio.windows import from_bounds
        r = rasterio.open(path)
        win = from_bounds(w, s, e, n, r.transform).round_offsets().round_lengths()
        self.A = r.read(1, window=win, boundless=True, fill_value=-999)
        self.tr = r.window_transform(win)

    def at(self, pts):
        import rasterio
        lo, la = B.TL.transform(np.array([p.x for p in pts]), np.array([p.y for p in pts]))
        rr, cc = rasterio.transform.rowcol(self.tr, lo, la)
        return self.A[np.clip(rr, 0, self.A.shape[0] - 1), np.clip(cc, 0, self.A.shape[1] - 1)]

    def over(self, g):
        from rasterio.features import rasterize
        ll = shapely.transform(g, lambda a: np.column_stack(B.TL.transform(a[:, 0], a[:, 1])))
        m = rasterize([(ll, 1)], out_shape=self.A.shape, transform=self.tr, dtype='uint8', all_touched=False).astype(bool)
        return self.A[m]


def main():
    D, recs, ring_g, ring_u = B.load('d19')
    w, s, e, n = B.lonlat_box(ring_u, pad=150)
    t90, t80, tok = B.threshold(*B.TL.transform(ring_u.centroid.x, ring_u.centroid.y))
    dsm, wc = Raster(DSM, w, s, e, n), Raster(B.WORLDCOVER, w, s, e, n)
    G = [(c, g) for c, g in B.google(w, s, e, n) if ring_u.intersects(g)]
    g90 = [g for c, g in G if c >= t90]
    hs = B.heights(g90)
    d90 = dsm.at([g.centroid for g in g90])
    houses = [r for r in recs if r['type'] == 'building']
    HP = [Polygon(h['footprint']) for h in houses]
    OU = unary_union(HP)
    minx, miny, maxx, maxy = ring_u.bounds
    t_all, t_90 = STRtree([g.centroid for c, g in G]), STRtree([g.centroid for g in g90])
    cells = []
    for x in np.arange(minx, maxx, CELL):
        for y in np.arange(miny, maxy, CELL):
            c = box(x, y, x + CELL, y + CELL).intersection(ring_u)
            if c.area < 2000:
                continue
            i90 = [i for i in t_90.query(c) if c.contains(g90[i].centroid)]
            ia = [i for i in t_all.query(c) if c.contains(G[i][1].centroid)]
            ps = [g90[i] for i in i90]
            hh = [hs[i] for i in i90 if hs[i] is not None]
            cg = B.utm_to_gidi(c)
            dv, wv = dsm.over(c), wc.over(c)
            zero = float(np.mean(dv == 0)) if dv.size else 0.0
            med = float(np.median(dv)) if dv.size else None
            zone = 'lagoon0' if zero >= 0.5 else 'low' if med is not None and med < LOW else 'ground'
            cells.append({
                'gidi': [round(v) for v in B.u2g(c.centroid.x, c.centroid.y)], 'ix': int((x - minx) // CELL),
                'iy': int((maxy - y) // CELL), 'area': round(c.area), 'zone': zone,
                'dsm_median': round(med, 1) if med is not None else None, 'dsm_zero': round(zero, 2),
                'wc_water': round(float(np.mean(wv == 80)), 2) if wv.size else None,
                'wc_built': round(float(np.mean(wv == 50)), 2) if wv.size else None,
                'n90': len(i90), 'n_all': len(ia),
                'cover90': round(unary_union(ps).intersection(c).area / c.area, 3) if ps else 0,
                'median_m2': round(float(np.median([p.area for p in ps])), 1) if ps else None,
                'median_h': round(float(np.median(hh)), 1) if hh else None,
                'ours_n': sum(1 for p in HP if cg.contains(p.centroid)),
                'ours_cover': round(OU.intersection(cg).area / cg.area, 3),
                '_c': c, '_i90': i90, '_ia': ia,
            })
    for k in cells:
        if k['n_all'] or k['ours_n']:
            print(json.dumps({a: b for a, b in k.items() if not a.startswith('_')}))
    # ASCII map: one character per cell, north up; the zone's letter, upper case where Google's cover >= 30%
    nx, ny = max(k['ix'] for k in cells) + 1, max(k['iy'] for k in cells) + 1
    grid = [[' '] * nx for _ in range(ny)]
    for k in cells:
        ch = {'lagoon0': 'w', 'low': 'l', 'ground': 'g'}[k['zone']]
        grid[k['iy']][k['ix']] = ch.upper() if k['cover90'] >= 0.3 else ch
    print('map (west to east, north to south; w lagoon at 0 m, l low under 3 m, g ground; capital = cover >= 30%):')
    for row in grid:
        print('  ' + ''.join(row))
    for k in cells:
        m = k['median_m2']
        k['grain'] = None if m is None else 'fine' if m < 50 else 'mid' if m < 90 else 'coarse'
    print('grain map (s fine < 50 m2, m mid, L coarse >= 90 m2, . no house):')
    grid = [[' '] * nx for _ in range(ny)]
    for k in cells:
        grid[k['iy']][k['ix']] = {'fine': 's', 'mid': 'm', 'coarse': 'L', None: '.'}[k['grain']]
    for row in grid:
        print('  ' + ''.join(row))
    tot = {'threshold': [tok, t90, t80], 'google90': len(g90), 'google_all': len(G),
           'google90_centroid_dsm_under3': int(np.sum(d90 < LOW)), 'google90_centroid_dsm_zero': int(np.sum(d90 == 0)),
           'zones': {}}
    for z in ('ground', 'low', 'lagoon0', 'fine', 'mid', 'coarse'):
        ks = [k for k in cells if z in (k['zone'], k['grain'])]
        if not ks:
            continue
        area = unary_union([k['_c'] for k in ks])
        idx = [i for k in ks for i in k['_i90']]
        ps = [g90[i] for i in idx]
        hh = [hs[i] for i in idx if hs[i] is not None]
        ag = B.utm_to_gidi(area)
        tot['zones'][z] = {
            'cells': len(ks), 'area_real_m2': round(area.area), 'gidi_x_range': [round(v) for v in ag.bounds[::2]],
            'n90': len(idx), 'n_all': sum(k['n_all'] for k in ks),
            'cover90': round(unary_union(ps).intersection(area).area / area.area, 3) if ps else 0,
            'cover_all': round(unary_union([G[i][1] for k in ks for i in k['_ia']]).intersection(area).area / area.area, 3),
            'median_m2': round(float(np.median([p.area for p in ps])), 1) if ps else None,
            'share_under_40m2': round(float(np.mean([p.area < 40 for p in ps])), 2) if ps else None,
            'median_h': round(float(np.median(hh)), 1) if hh else None,
            'storeys': dict(sorted(collections.Counter(B.storeys(h) for h in hh).items())),
            'wc_water': round(float(np.mean([k['wc_water'] for k in ks])), 3),
            'wc_built': round(float(np.mean([k['wc_built'] for k in ks])), 3),
            'zones_of_cells': dict(collections.Counter(k['zone'] for k in ks)),
            'ours_n': sum(k['ours_n'] for k in ks),
            'ours_kinds': dict(collections.Counter(houses[i]['kind'] for i, p in enumerate(HP) if ag.contains(p.centroid)).most_common()),
            'ours_cover': round(OU.intersection(ag).area / ag.area, 3),
        }
    # Overture power lines across the outline (the Dec 2025 - Jan 2026 clearances were measured from a high-tension line)
    t = pq.read_table(B.OV + 'lagos_overture_infrastructure.parquet', columns=['subtype', 'class', 'geometry', 'bbox'])
    tot['power_lines'] = []
    for r in t.to_pylist():
        b = r['bbox']
        if r['class'] != 'power_line' or b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n:
            continue
        g = B.to_utm(shapely.from_wkb(r['geometry'])).intersection(ring_u)
        if g.length:
            gg = B.utm_to_gidi(g)
            near = sum(1 for x in g90 if x.distance(g) <= 30)
            tot['power_lines'].append({'real_m_in_outline': round(g.length), 'gidi_bounds': [round(v) for v in gg.bounds],
                                       'google90_within_30m': near})
    print(json.dumps(tot))
    if '--json' in sys.argv:
        json.dump({'cells': [{a: b for a, b in k.items() if not a.startswith('_')} for k in cells], 'totals': tot},
                  open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)


if __name__ == '__main__':
    main()
