"""Sọ̀rọ̀lérè (d13) building study, 27 Oct: the real grounds (Overture land use that is not residential) measured on
their own, Randle General Hospital first, and our map inside the same grounds.

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d13_landmarks.py [d13]

Reuses d17_blocks.py (same folder) for the outline, Google Open Buildings v3 at the tile's 90%-precision threshold,
the 2.5D heights and storeys, Overture places and land use. For each land-use polygon of a non-residential class that
overlaps the outline by 2,000 m2 or more (real), or is named: its real area inside the outline, the Google buildings
whose centroid is in it (count, cover, median and largest footprint, storeys), the Overture places in it, and our
houses (map/d13) whose centroid falls inside the same ground taken to Gidi metres, with their kinds, storeys and
roof area; and our plot records whose outline overlaps it.

Also prints, for Randle General Hospital's ground, every Google building in it (footprint, height, storeys) and the
Overture places within 150 m, so the note can describe it building by building.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B  # noqa: E402

import shapely  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

SKIP_CLASS = {'residential', 'land', 'species_management_area'}
MIN_REAL = 2000


def main(d='d13'):
    D, recs, ring_g, ring_u = B.load(d)
    w, s, e, n = B.lonlat_box(ring_u)
    c_lon, c_lat = B.TL.transform(ring_u.centroid.x, ring_u.centroid.y)
    t90, t80, tok = B.threshold(c_lon, c_lat)
    G = [g for c, g in B.google(w, s, e, n) if c >= t90 and ring_u.intersects(g)]
    HS = B.heights(G)
    P = [p for p in B.places(w, s, e, n) if ring_u.buffer(150).contains(p[3])]
    LU = [l for l in B.landuse(w, s, e, n) if l[2] not in SKIP_CLASS and l[4].intersects(ring_u)]
    houses = [r for r in recs if r['type'] == 'building']
    HP = [Polygon(h['footprint']) for h in houses]
    plots = [r for r in recs if r['type'] == 'plot']
    print(f'threshold tile {tok}: 90% {t90}, 80% {t80}; Google buildings at 90% touching the outline: {len(G)}')
    rows = []
    for src, sub, cls, name, poly in LU:
        inside = poly.intersection(ring_u)
        if inside.area < MIN_REAL and not name:
            continue
        if inside.area < 50:
            continue
        idx = [i for i, g in enumerate(G) if inside.contains(g.centroid)]
        polys = [G[i] for i in idx]
        areas = sorted(p.area for p in polys)
        cover = unary_union(polys).intersection(inside).area / inside.area if polys else 0
        st = collections.Counter(B.storeys(HS[i]) for i in idx if HS[i] is not None)
        pl = [(c, nm) for c, nm, cf, g in P if inside.contains(g)]
        gid = B.utm_to_gidi(inside)
        mine = [k for k, hp in enumerate(HP) if gid.contains(hp.centroid)]
        ours_area = unary_union([HP[k] for k in mine]).intersection(gid).area if mine else 0
        kinds = collections.Counter(houses[k].get('kind') for k in mine)
        mst = collections.Counter(houses[k].get('storeys') for k in mine)
        pids = [p['id'] + ':' + p.get('kind', '') for p in plots
                if Polygon(p['outline']).buffer(0).intersection(gid).area > 0.3 * Polygon(p['outline']).buffer(0).area]
        cx, cy = B.u2g(inside.centroid.x, inside.centroid.y)
        rows.append((cls, name, round(inside.area), round(cx), round(cy), len(idx), cover,
                     areas[len(areas) // 2] if areas else 0, areas[-1] if areas else 0, dict(sorted(st.items())),
                     pl[:6], len(pl), len(mine), ours_area / gid.area if gid.area else 0, dict(kinds), dict(mst), pids,
                     round(gid.area)))
    rows.sort(key=lambda r: -r[2])
    for r in rows:
        (cls, name, a, cx, cy, nb, cov, med, mx, st, pl, npl, nm, oc, kinds, mst, pids, ga) = r
        print(f'\n{cls} | {name} | real {a:,} m2 (Gidi {ga:,}) at Gidi {cx},{cy} | Google {nb}, cover {cov:.0%}, '
              f'median {med:.0f} m2, largest {mx:.0f} m2, storeys {st} | places {npl}: {pl} | ours {nm} houses, '
              f'cover {oc:.0%}, kinds {kinds}, storeys {mst}, plots {pids}')

    # Randle, building by building
    rand = [l for l in LU if l[3] == 'Randle General Hospital']
    for src, sub, cls, name, poly in rand:
        inside = poly.intersection(ring_u)
        lon, lat = B.TL.transform(inside.centroid.x, inside.centroid.y)
        bx = inside.bounds
        print(f'\n== {name}: real {inside.area:,.0f} m2, centroid {lat:.5f} N {lon:.5f} E, '
              f'{bx[2] - bx[0]:.0f} m east-west by {bx[3] - bx[1]:.0f} m north-south (bounding box)')
        idx = [i for i, g in enumerate(G) if inside.contains(g.centroid)]
        for i in sorted(idx, key=lambda i: -G[i].area):
            g = G[i]
            mrr = g.minimum_rotated_rectangle
            xs = mrr.exterior.coords
            sides = sorted({round(shapely.geometry.Point(xs[k]).distance(shapely.geometry.Point(xs[k + 1]))) for k in range(2)})
            gx, gy = B.u2g(g.centroid.x, g.centroid.y)
            glon, glat = B.TL.transform(g.centroid.x, g.centroid.y)
            h = HS[i]
            print(f'  {g.area:7.0f} m2  about {sides} m  height {h if h is None else round(h, 1)} m '
                  f'storeys {None if h is None else B.storeys(h)}  at {glat:.5f} N {glon:.5f} E (Gidi {gx:.0f},{gy:.0f})')
        near = [(c, nm, round(inside.distance(g))) for c, nm, cf, g in P if inside.distance(g) <= 150]
        print('  places within 150 m (category, name, metres from the ground):')
        for c, nm, dd in sorted(near, key=lambda x: x[2]):
            print('   ', c, '|', nm, '|', dd)
        gid = B.utm_to_gidi(inside)
        for k, hp in enumerate(HP):
            if gid.intersects(hp):
                h = houses[k]
                print(f"  ours: {h['id']} {h.get('kind')} storeys {h.get('storeys')} {hp.area:.0f} Gidi m2 "
                      "(drawn at real size: never times 9)")


if __name__ == '__main__':
    main(*(sys.argv[1:2] or ['d13']))
