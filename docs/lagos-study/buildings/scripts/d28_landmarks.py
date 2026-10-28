"""Gbàgede (d28) building study, 28 Oct: the Deeper Life church's ground and Ajayi Aina Street, building by building,
and a search for Twinkle Star nursery (the owner's grandmother's house was on Ajayi Aina Street in front of the big
Deeper Life church; he went to Twinkle Star nursery there).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d28_landmarks.py

Reuses d17_blocks.py (same folder): the outline, Google Open Buildings v3 at the tile's 90%-precision threshold,
2.5D 2023 heights and storeys, Overture places and land use, the real blocks. Prints:
1. The Overture places whose name holds 'deeper' or 'twinkle', or whose address holds 'ajayi aina', inside the
   district's box, with their distance to the outline (0 = inside).
2. Overture's segments named Ajayi Aina Street: class, length, ends (lat, lon and Gidi metres).
3. The Overture 'religious' land-use ground holding the Deeper Life church's point: area, its Google buildings one by
   one (area, rotated-rectangle sides, height, storeys, position), our houses inside it (real size, as drawn).
4. The frontage of Ajayi Aina Street: Google buildings whose centroid is within 35 m of the street's centreline, on the
   church's side (north-west of the line) and on the far side (south-east, facing the church); count, median, storeys; and our houses along our
   own record of the street.
5. The real blocks (d17_blocks numbering) that hold the church's point and the street.
6. Every Overture school, preschool, kindergarten, child-care or education place within 1,000 m of the church point.
7. Bakare Dawodu Street (Twinkle Star's listed address): its segments, buildings along it, its blocks.
8. Twinkle Star's Google Maps pin (TWINKLE): its block, the Google buildings at it, our houses nearest it.
Our footprints in map/d28 are at REAL size: never multiplied by 9.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B  # noqa: E402

import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
import shapely  # noqa: E402
from shapely.geometry import LineString, Point, Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

CHURCH = (3.38790, 6.55633)   # Overture 'Deeper Life Bible Church', pentecostal_place_of_worship, 10 Oke Owo St
# Google Maps place 'Twinkle Star Nursery and Primary School', Elementary school, 'Plot 23 Bakare Dawodu St, Gbagada',
# plus code H94Q+7M; its pin read from the place URL (!3d6.5556825!4d3.3891698), looked at 28 Oct (study only)
TWINKLE = (3.3891698, 6.5556825)
SCHOOLISH = ('school', 'preschool', 'kindergarten', 'child_care', 'day_care', 'education', 'elementary_school',
             'montessori')


def ll(g):
    lo, la = B.TL.transform(g.x, g.y)
    return f'{la:.5f} N {lo:.5f} E'


def gd(g):
    x, y = B.u2g(g.x, g.y)
    return f'Gidi {x:.0f},{y:.0f}'


def sides(g):
    xs = g.minimum_rotated_rectangle.exterior.coords
    return sorted(round(Point(xs[k]).distance(Point(xs[k + 1]))) for k in range(2))


def main(d='d28'):
    D, recs, ring_g, ring_u = B.load(d)
    w, s, e, n = B.lonlat_box(ring_u)
    c_lon, c_lat = B.TL.transform(ring_u.centroid.x, ring_u.centroid.y)
    t90, t80, tok = B.threshold(c_lon, c_lat)
    church = Point(*B.TU.transform(*CHURCH))
    print(f'church point {CHURCH[1]} N {CHURCH[0]} E -> {gd(church)}; inside the outline: {ring_u.contains(church)}, '
          f'{ring_u.exterior.distance(church) if hasattr(ring_u, "exterior") else ring_u.boundary.distance(church):.0f} m from its edge')

    # 1. places by name or address
    t = pq.read_table(B.OV + 'lagos_overture_place.parquet',
                      columns=['taxonomy', 'names', 'geometry', 'bbox', 'confidence', 'addresses'])
    allp = []
    print('\n1. Overture places named deeper/twinkle or addressed on Ajayi Aina, in the district box:')
    for r in t.to_pylist():
        b = r['bbox']
        if b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n:
            continue
        g = B.to_utm(shapely.from_wkb(r['geometry']))
        nm = (r['names'] or {}).get('primary') or ''
        cat = (r['taxonomy'] or {}).get('primary')
        ad = '; '.join((a.get('freeform') or '') for a in (r['addresses'] or []))
        allp.append((cat, nm, r['confidence'], ad, g))
        if 'deeper' in nm.lower() or 'twinkle' in nm.lower() or 'ajayi aina' in ad.lower():
            print(f'   {cat} | {nm} | conf {r["confidence"]:.2f} | {ad} | {ll(g)} {gd(g)} | '
                  f'{church.distance(g):.0f} m from the church point | inside: {ring_u.contains(g)}')

    # 2. Ajayi Aina Street in Overture
    segs = B.segments(B.OV + 'lagos_overture_segment.parquet', w, s, e, n,
                      lambda r: r['subtype'] == 'road' and 'ajayi aina' in str((r['names'] or {}).get('primary')).lower())
    print(f'\n2. Overture segments named Ajayi Aina: {len(segs)}')
    for r, g in segs:
        a, z = Point(g.coords[0]), Point(g.coords[-1])
        print(f'   {r["class"]} {g.length:.0f} m from {ll(a)} ({gd(a)}) to {ll(z)} ({gd(z)}); '
              f'nearest to the church point {g.distance(church):.0f} m; inside the outline {ring_u.contains(g)}')
    street = unary_union([g for _, g in segs])
    print(f'   together {street.length:.0f} m')

    # 3. the religious ground holding the church
    G = [(c, g) for c, g in B.google(w, s, e, n) if ring_u.intersects(g)]
    G90 = [g for c, g in G if c >= t90]
    HS = B.heights(G90)
    LU = [l for l in B.landuse(w, s, e, n) if l[2] == 'religious' and l[4].distance(church) < 60]
    houses = [r for r in recs if r['type'] == 'building']
    HP = [Polygon(h['footprint']) for h in houses]
    for src, sub, cls, name, poly in LU:
        inside = poly.intersection(ring_u)
        bx = inside.bounds
        print(f'\n3. religious ground {name!r}: real {inside.area:,.0f} m2, centroid {ll(inside.centroid)} '
              f'({gd(inside.centroid)}), {bx[2] - bx[0]:.0f} m E-W by {bx[3] - bx[1]:.0f} m N-S (bounding box); '
              f'church point inside: {inside.contains(church)} ({inside.distance(church):.0f} m)')
        idx = [i for i, g in enumerate(G90) if inside.contains(g.centroid)]
        cov = unary_union([G90[i] for i in idx]).intersection(inside).area / inside.area if idx else 0
        print(f'   Google buildings at 90% (centroid in): {len(idx)}, cover {cov:.1%}')
        for i in sorted(idx, key=lambda i: -G90[i].area):
            g, h = G90[i], HS[i]
            print(f'   {g.area:7.0f} m2  about {sides(g)} m  height {None if h is None else round(h, 1)} m  storeys '
                  f'{None if h is None else B.storeys(h)}  at {ll(g.centroid)} ({gd(g.centroid)}), '
                  f'{g.distance(church):.0f} m from the church point')
        near = sorted(((p[0], p[1], round(inside.distance(p[4]))) for p in allp if inside.distance(p[4]) <= 100),
                      key=lambda x: x[2])
        print('   Overture places within 100 m of the ground (category | name | m):')
        for c, nm, dd in near:
            print('     ', c, '|', nm, '|', dd)
        gid = B.utm_to_gidi(inside)
        print(f'   in Gidi: {gid.area:,.0f} m2')
        for k, hp in enumerate(HP):
            if gid.intersects(hp):
                h = houses[k]
                print(f"   ours: {h['id']} {h.get('kind')} storeys {h.get('storeys')} {hp.area:.0f} m2 (real size, as "
                      f"drawn), {hp.intersection(gid).area / hp.area:.0%} of it inside the ground")

    # 4. Ajayi Aina frontage
    if not street.is_empty:
        line = street if street.geom_type == 'LineString' else shapely.ops.linemerge(street)
        band = street.buffer(35)
        idx = [i for i, g in enumerate(G90) if band.contains(g.centroid)]
        church_side = ring_u.intersection(LU[0][4]).centroid if LU else church
        sides_ = collections.defaultdict(list)
        for i in idx:
            g = G90[i].centroid
            # side: the sign of the cross product against the nearest segment of the street
            best = min((seg for _, seg in segs), key=lambda q: q.distance(g))
            # run every segment south-west to north-east (Overture's segments run both ways here), so that
            # left is the north-west side (the church's) and right the south-east side
            a_, z_ = best.coords[0], best.coords[-1]
            if a_[1] > z_[1]:
                best = LineString(list(best.coords)[::-1])
            pr = best.project(g)
            p0 = best.interpolate(max(0, pr - 1))
            p1 = best.interpolate(min(best.length, pr + 1))
            cr = (p1.x - p0.x) * (g.y - p0.y) - (p1.y - p0.y) * (g.x - p0.x)
            sides_['north-west side (the church\'s)' if cr > 0 else 'south-east side (facing the church)'].append(i)
        print(f'\n4. Google buildings at 90% with centroid within 35 m of Ajayi Aina Street: {len(idx)}')
        for k, v in sides_.items():
            ar = sorted(G90[i].area for i in v)
            st = collections.Counter(B.storeys(HS[i]) for i in v if HS[i] is not None)
            print(f'   {k}: {len(v)}, median {np.median(ar):.0f} m2, largest {ar[-1]:.0f} m2, storeys {dict(sorted(st.items()))}')
        side_of = {i: k for k, v in sides_.items() for i in v}
        if LU:
            gr = LU[0][4].intersection(ring_u)
            east = [i for i in sides_['south-east side (facing the church)'] if G90[i].distance(gr) <= 40]
            print(f'   facing the church ground (south-east side, within 40 m of the ground): {len(east)}: ' +
                  ', '.join(f'{G90[i].area:.0f} m2 {B.storeys(HS[i]) if HS[i] else "?"} st at {ll(G90[i].centroid)} '
                            f'({G90[i].distance(gr):.0f} m from the ground)' for i in sorted(east, key=lambda i: G90[i].centroid.y)))
        for i in sorted(idx, key=lambda i: street.project(G90[i].centroid) if street.geom_type == 'LineString' else G90[i].centroid.y):
            g, h = G90[i], HS[i]
            print(f'     {g.area:6.0f} m2 {sides(g)} m h {None if h is None else round(h, 1)} st '
                  f'{None if h is None else B.storeys(h)} at {ll(g.centroid)} ({gd(g.centroid)}), '
                  f'{street.distance(g):.0f} m off the street, {side_of[i].split(' (')[0]}')
        # ours: our road record nearest to the real street, and our houses within 35/3 m of it in Gidi
        roads = [r for r in recs if r['type'] == 'road']
        sg = B.utm_to_gidi(street)
        best = sorted(roads, key=lambda r: LineString([q[:2] for q in r['centreline']]).hausdorff_distance(sg))[:3]
        for r in best:
            L = LineString([q[:2] for q in r['centreline']])
            print(f"   our road {r['id']} {r.get('class')} width {r.get('width')} m, {L.length:.0f} m long, hausdorff "
                  f"{L.hausdorff_distance(sg):.0f} m from the real street taken to Gidi; name in record: {r.get('name')!r}")
        L = LineString([q[:2] for q in best[0]['centreline']])
        mine = [k for k, hp in enumerate(HP) if L.distance(hp.centroid) <= 35 / 3 + best[0]['width'] / 2]
        print(f"   our houses with centroid within {35 / 3 + best[0]['width'] / 2:.1f} Gidi m of {best[0]['id']}'s centreline: "
              f"{len(mine)}, kinds {dict(collections.Counter(houses[k]['kind'] for k in mine))}, storeys "
              f"{dict(collections.Counter(houses[k]['storeys'] for k in mine))}, median {np.median([HP[k].area for k in mine]) if mine else 0:.0f} m2 (real size)")

    # 5. blocks
    blocks, *_ = B.blocks_of(ring_u, w, s, e, n)
    for k, bk in enumerate(blocks):
        hit = []
        if bk.contains(church):
            hit.append('church point')
        if not street.is_empty and bk.distance(street) < 10:
            hit.append(f'within 10 m of Ajayi Aina ({bk.intersection(street.buffer(35)).area:,.0f} m2 of the 35 m band)')
        if hit:
            print(f'5. {d.upper()}-{k + 1:02d}: {", ".join(hit)}; block {bk.area:,.0f} m2 at {ll(bk.centroid)}')

    # 7. Bakare Dawodu Street (Twinkle Star Nursery and Primary School's address is 23 Bakare Dawodu Street, Gbagada:
    #    finelib.com listing 14632, read 28 Oct; not in Overture places by name)
    bd = B.segments(B.OV + 'lagos_overture_segment.parquet', w, s, e, n,
                    lambda r: r['subtype'] == 'road' and 'bakare dawodu' in str((r['names'] or {}).get('primary')).lower())
    bds = unary_union([g for _, g in bd])
    print(f'\n7. Overture segments named Bakare Dawodu: {len(bd)}, together {bds.length:.0f} m, all inside the outline: '
          f'{all(ring_u.contains(g) for _, g in bd)}; nearest to the church point {bds.distance(church):.0f} m, '
          f'farthest {max(church.distance(Point(c)) for _, g in bd for c in g.coords):.0f} m; nearest to Ajayi Aina '
          f'{bds.distance(street):.0f} m')
    for r, g in bd:
        print(f'   {r["class"]} {g.length:.0f} m from {ll(Point(g.coords[0]))} ({gd(Point(g.coords[0]))}) to '
              f'{ll(Point(g.coords[-1]))} ({gd(Point(g.coords[-1]))})')
    idx = [i for i, g in enumerate(G90) if bds.distance(g.centroid) <= 30]
    ar = sorted(G90[i].area for i in idx)
    st = collections.Counter(B.storeys(HS[i]) for i in idx if HS[i] is not None)
    print(f'   Google buildings at 90% with centroid within 30 m of it: {len(idx)}, median {np.median(ar):.0f} m2, '
          f'largest {ar[-1]:.0f} m2, under 100 m2 {sum(a < 100 for a in ar)}, storeys {dict(sorted(st.items()))}')
    for k, bk in enumerate(blocks):
        if bk.distance(bds) < 10:
            print(f'   block {d.upper()}-{k + 1:02d} ({bk.area:,.0f} m2) within 10 m of it')
    for cat, nm, cf, ad, g in allp:
        if 'bakare dawodu' in ad.lower():
            print(f'   place addressed on it: {nm} | {cat} | {ad} | {ll(g)}')

    # 8. Twinkle Star's Google Maps pin
    tw = Point(*B.TU.transform(*TWINKLE))
    print(f'\n8. Twinkle Star pin {TWINKLE[1]} N {TWINKLE[0]} E ({gd(tw)}): inside the outline {ring_u.contains(tw)}; '
          f'{tw.distance(church):.0f} m from the church point; {tw.distance(LU[0][4]) if LU else -1:.0f} m from the church '
          f'ground; {tw.distance(street):.0f} m from Ajayi Aina; {tw.distance(bds):.0f} m from Bakare Dawodu')
    for k, bk in enumerate(blocks):
        if bk.contains(tw) or bk.distance(tw) < 5:
            print(f'   block {d.upper()}-{k + 1:02d} ({bk.area:,.0f} m2), {bk.distance(tw):.1f} m')
    for i in sorted(range(len(G90)), key=lambda i: G90[i].distance(tw))[:4]:
        g, h = G90[i], HS[i]
        print(f'   Google building {g.area:.0f} m2 {sides(g)} m h {None if h is None else round(h, 1)} st '
              f'{None if h is None else B.storeys(h)} at {ll(g.centroid)}, {g.distance(tw):.1f} m from the pin '
              f'(contains it: {g.contains(tw)})')
    twg = Point(*B.u2g(tw.x, tw.y))
    for k in sorted(range(len(HP)), key=lambda k: HP[k].distance(twg))[:3]:
        h = houses[k]
        print(f"   ours: {h['id']} {h['kind']} storeys {h['storeys']} {HP[k].area:.0f} m2 (real size), "
              f"{HP[k].distance(twg):.1f} Gidi m from the pin taken to Gidi")

    # 6. schools near the church
    print('\n6. Overture schooling places within 1,000 m of the church point:')
    for cat, nm, cf, ad, g in sorted(allp, key=lambda p: p[4].distance(church)):
        if g.distance(church) > 1000:
            break
        if cat and any(k in cat for k in SCHOOLISH) or any(k in nm.lower() for k in ('nursery', 'montessori', 'school', 'academy', 'college')):
            print(f'   {g.distance(church):4.0f} m | {cat} | {nm} | {ad} | conf {cf:.2f}')


if __name__ == '__main__':
    main(*(sys.argv[1:2] or ['d28']))
