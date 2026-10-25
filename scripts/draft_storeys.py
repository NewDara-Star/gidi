"""A district's first draft of storeys, from each house's real source in Google's Open Buildings 2.5D heights.

  ~/.venvs/gidi/bin/python scripts/draft_storeys.py map/d15 [--dry]

draft_buildings.py copies real houses (Microsoft footprints) into Gidi blocks, moved and sometimes turned, never scaled,
and does not record where each came from. This finds each house's source again by its shape, then reads that source's
height:

1. exact: a real footprint of the same area and edge lengths within 120 m of the house's real twin spot (3x its Gidi
   position);
2. trimmed (houses cut to a shared party wall): moved by the offset of the nearest exactly matched house (within 40 m),
   the real footprint it overlaps by more than 80% of its own area;
3. nudged (houses pushed off a road as well): a corner of the moved house put on each corner of a real footprint within
   25 m of no less than its area and at most 2.5 times it; the best fit, if it covers 90% of the house.

Height: the median of the source footprint's 2.5D 2023 pixels with presence >= 0.5 (0.5 m pixels, an effective 4 m;
the same reading as scripts/study_boxheights.py). Storeys from the same bands as the height studies (about 3 m a
storey): under 4.5 m 1, 4.5-7.5 2, 7.5-10.5 3, 10.5-13.5 4, and on by 3 m.

Industry: footprint-based city tools (Esri CityEngine, ArcGIS Pro procedural rules) keep height, floor count and roof
type as attributes on each footprint, read from GIS data or a surface model, and the building rules read them
(doc.arcgis.com/en/cityengine; Penn State GEOG 497, CityEngine lessons).

Written: `storeys` on houses that have none, up to TALL - 1; a reading of TALL storeys or more is left unset for a
Street View check by hand (Mùṣá, 25 Oct: of five houses checked in Street View, the 1, 2 and 3 storey readings were right,
and the one reading 20 m, 7 storeys, on Ikorodu Road, stands among 3-storey blocks: 2.5D's 4 m blur over-reads some); a house already given storeys is never changed ("Rules draft, records
rule"). Houses with no source found, or whose source has no built pixels in 2.5D, are left without storeys and counted.
Heights: Google Open Buildings 2.5D Temporal (CC BY 4.0), ~/gidi-data/research/data/open-buildings-2023/.
"""
import json
import math
import os
import sys

import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.windows import from_bounds
from pyproj import Transformer
from shapely import transform as reproject
from shapely.affinity import translate
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union
from shapely.strtree import STRtree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draft_buildings import FU, FV, RH, footprints

OB = os.path.expanduser('~/gidi-data/research/data/open-buildings-2023/')
EXACT_R, TRIM_R, NUDGE_R = 120, 40, 25
TALL = 5


def sig(p):
    c = list(p.exterior.coords)[:-1]
    return sorted(round(math.dist(c[i], c[i - 1]), 1) for i in range(len(c)))


def sources(houses, real):
    """{house id: (real footprint, how found)} in real metres on Gidi axes."""
    tree = STRtree(real)
    src = {}
    for i, h in houses.items():
        twin = Point(3 * h.centroid.x, 3 * h.centroid.y)
        s = sig(h)
        ex = [real[j] for j in tree.query(twin.buffer(EXACT_R)) if abs(real[j].area - h.area) < 0.05 and sig(real[j]) == s]
        if ex:
            src[i] = (min(ex, key=lambda f: f.centroid.distance(twin)), 'exact')
    ids = list(src)
    off = {i: (src[i][0].centroid.x - houses[i].centroid.x, src[i][0].centroid.y - houses[i].centroid.y) for i in ids}
    etree = STRtree([houses[i].centroid for i in ids])
    for i, h in houses.items():
        if i in src:
            continue
        best = (0, None)
        for k in etree.query(h.centroid.buffer(TRIM_R)):
            t = translate(h, *off[ids[k]])
            for j in tree.query(t):
                o = real[j].intersection(t).area / h.area
                if o > best[0]:
                    best = (o, real[j])
        if best[0] > 0.8:
            src[i] = (best[1], 'trimmed')
            continue
        ks = list(etree.query(h.centroid.buffer(60)))
        if not ks:
            continue
        k = min(ks, key=lambda k: etree.geometries[k].distance(h.centroid))
        t = translate(h, *off[ids[k]])
        best = (0, None)
        for j in tree.query(t.centroid.buffer(NUDGE_R)):
            f = real[j]
            if not h.area * 0.98 <= f.area <= h.area * 2.5:
                continue
            for fv in list(f.exterior.coords)[:-1]:
                for v in list(t.exterior.coords)[:-1]:
                    o = f.intersection(translate(t, fv[0] - v[0], fv[1] - v[1])).area / h.area
                    if o > best[0]:
                        best = (o, f)
        if best[0] > 0.9:
            src[i] = (best[1], 'nudged')
    return src


def heights(src):
    """{house id: median 2.5D height of its source, m} for sources with built pixels."""
    utm = {i: Polygon([(FU + x, FV + RH - y) for x, y in f.exterior.coords]) for i, (f, _) in src.items()}
    ext = unary_union(list(utm.values())).envelope
    out = {}
    for t in sorted(f for f in os.listdir(OB) if f.endswith('.tif')):
        r = rasterio.open(OB + t)
        tr = Transformer.from_crs(32631, r.crs, always_xy=True)
        to = lambda g: reproject(g, lambda c: np.column_stack(tr.transform(c[:, 0], c[:, 1])))
        if not box(*r.bounds).intersects(to(ext)):
            continue
        for i, g in utm.items():
            if i in out:
                continue
            a = to(g)
            if not box(*r.bounds).contains(a):
                continue
            w = from_bounds(*a.bounds, r.transform).round_offsets().round_lengths()
            if w.width < 1 or w.height < 1:
                continue
            _, H, P = r.read(window=w, boundless=True, fill_value=0)
            m = rasterize([(a, 1)], out_shape=H.shape, transform=r.window_transform(w), dtype='uint8', all_touched=True)
            b = m.astype(bool) & (P >= 0.5) & (H > 0)
            out[i] = float(np.median(H[b])) if b.any() else None
    return {i: h for i, h in out.items() if h is not None}


def storeys(h):
    return max(1, int((h + 1.5) // 3))


def main():
    d = sys.argv[1].rstrip('/')
    pf = f'{d}/plan.json'
    plan = json.load(open(pf))
    todo = {r['id']: Polygon(r['footprint']) for r in plan['records'] if r['type'] == 'building' and 'storeys' not in r}
    xs = [c[0] for h in todo.values() for c in h.exterior.coords]
    ys = [c[1] for h in todo.values() for c in h.exterior.coords]
    real = footprints((min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60))
    src = sources(todo, real)
    hs = heights(src)
    n, tall = {}, []
    for r in plan['records']:
        if r['id'] in hs:
            s = storeys(hs[r['id']])
            n[s] = n.get(s, 0) + 1
            if s < TALL:
                r['storeys'] = s
            else:
                tall.append(r['id'])
    how = {}
    for f, k in src.values():
        how[k] = how.get(k, 0) + 1
    print(f'{len(todo)} houses without storeys; sources found {len(src)} ({how}); with 2.5D heights {len(hs)}')
    print('storeys read:', dict(sorted(n.items())), f'; written {len(hs) - len(tall)}; {TALL}+ left for a hand check:',
          len(tall), '; no source or no 2.5D pixels:', len(todo) - len(hs))
    print('tall:', ' '.join(tall))
    if '--dry' not in sys.argv:
        json.dump(plan, open(pf, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
