"""Mùṣá (d15): Microsoft's footprints (the source scripts/draft_buildings.py copied our houses from) against Google's,
inside the same real outline, so a size gap can be told apart as the source's or the drawing's (building study, 27 Oct).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d15_sources.py

Prints, for each source: count with centroid in the outline, median and quartile footprints (m2), share under 40 m2,
count of 500 m2 and up, roof cover of the outline (union clipped). Google at the 90%-precision threshold (0.749).
Microsoft: ~/gidi-data/research/data/ms-buildings/*.csv.gz (ODbL), read the way draft_buildings.py reads it.
Ours: map/d15 houses, in Gidi metres (houses are at real size; the land is 1:3).
"""
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B  # noqa: E402

import numpy as np  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

MS = os.path.expanduser('~/gidi-data/research/data/ms-buildings/')


def stats(name, polys, ring, cents_in):
    a = np.array([p.area for p in polys])
    cov = unary_union(polys).intersection(ring).area / ring.area
    print(f'{name}: n {len(polys)}, median {np.median(a):.1f}, quartiles {np.percentile(a, 25):.1f}-{np.percentile(a, 75):.1f}, '
          f'under 40 {np.mean(a < 40):.3f}, 500+ {int(np.sum(a >= 500))}, cover {cov:.4f}')


def main():
    D, recs, ring_g, ring_u = B.load('d15')
    w, s, e, n = B.lonlat_box(ring_u)
    ms = []
    for f in sorted(os.listdir(MS)):
        with gzip.open(MS + f, 'rt') as fh:
            for line in fh:
                i = line.find('[[[')
                a = line[i + 3:line.find(']', i)].split(',')
                lo, la = float(a[0]), float(a[1])
                if w <= lo <= e and s <= la <= n:
                    ring = json.loads(line)['geometry']['coordinates'][0]
                    g = B.to_utm(Polygon(ring))
                    if ring_u.contains(g.centroid):
                        ms.append(g)
    G = [g for c, g in B.google(w, s, e, n) if c >= 0.749 and ring_u.contains(g.centroid)]
    H = [Polygon(r['footprint']) for r in recs if r['type'] == 'building']
    stats('google90', G, ring_u, True)
    stats('microsoft', ms, ring_u, True)
    stats('ours', H, ring_g, True)


if __name__ == "__main__" and "--plots" not in sys.argv:
    main()


def plots():
    """Google's cover (90%) against ours inside each of our plots (plot outline taken to real metres), and inside
    Overture's named land-use polygons that lie mostly in the outline (Ladipo Market, LUTH)."""
    import shapely
    import numpy as np
    D, recs, ring_g, ring_u = B.load('d15')
    w, s, e, n = B.lonlat_box(ring_u)
    G = unary_union([g for c, g in B.google(w, s, e, n) if c >= 0.749 and ring_u.intersects(g)])
    H = unary_union([Polygon(r['footprint']) for r in recs if r['type'] == 'building'])
    to_u = lambda p: shapely.transform(p, lambda a: np.column_stack(B.g2u(a[:, 0], a[:, 1])))
    for r in recs:
        if r['type'] == 'plot':
            pg = Polygon(r['outline']).buffer(0)
            pu = to_u(pg)
            print(f"plot {r['id']} {r['kind']}: Gidi {pg.area:.0f} m2, Google {G.intersection(pu).area / pu.area:.3f}, "
                  f"ours {H.intersection(pg).area / pg.area:.3f}")
    for src, sub, cl, nm, g in B.landuse(w, s, e, n):
        if nm and 'Pacific' not in nm and g.intersection(ring_u).area > 0.5 * g.area and g.area > 5000:
            gg = B.utm_to_gidi(g)
            print(f"landuse {cl} '{nm}': real {g.area:.0f} m2, Google {G.intersection(g).area / g.area:.3f}, "
                  f"ours {H.intersection(gg).area / gg.area:.3f}")


if __name__ == '__main__' and '--plots' in sys.argv:
    plots()
