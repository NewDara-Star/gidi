"""Ìtìrí (d14) building study, 28 Oct: the big roofs, the named places by kind, and the blocks' land use.

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d14_landmarks.py d14 x.json

x.json is d17_blocks.py's output for the district (d17_blocks.py d14 --json x.json); it gives the block ids.
Reuses d17_blocks.py (same folder) for the outline, Google Open Buildings v3 at the tile's 90%-precision threshold,
the 2.5D heights, Overture places and land use. Prints:
1. every Google building (90%) of 1,000 m2 or more whose centroid is in the outline: footprint, height, storeys, its
   block, lon/lat, Gidi metres, and the Overture places within 60 m of its footprint (category | name);
2. the Overture places in the outline for the kinds that name a ground (schools, churches, mosques, hospitals,
   manufacturers, markets, hotels, government, police, parking), counted, with the named ones and their block;
1b. for each block holding a roof of 1,000 m2 or more, the share of its roof area in such roofs;
3. Overture land use (not residential, not the bogus 'Pacific Islands Heritage' polygon) inside the outline.
Our houses are at real size in map/dNN/plan.json; nothing here scales them.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B  # noqa: E402

from shapely.geometry import Polygon  # noqa: E402

KINDS = {
    'school': ('school', 'high_school', 'elementary_school', 'preschool', 'education', 'college_university',
               'educational_service', 'private_school', 'day_care_preschool'),
    'church': ('christian_place_of_worship', 'church_cathedral', 'religious_organization', 'pentecostal_church',
               'anglican_church', 'catholic_church', 'baptist_church', 'methodist_church'),
    'mosque': ('muslim_place_of_worship', 'mosque'),
    'health': ('hospital', 'health_care', 'doctors_office', 'medical_center', 'pharmacy', 'clinic', 'maternity_centers'),
    'industry': ('manufacturer', 'factory', 'industrial_equipment_manufacturer', 'warehouse', 'commercial_industrial',
                 'printing_service', 'freight_and_cargo_service'),
    'market': ('market', 'shopping_center', 'farmers_market', 'grocery_store'),
    'hotel': ('hotel', 'motel', 'guest_house'),
    'government': ('government_office', 'police_station', 'post_office', 'town_hall', 'courthouse'),
    'parking': ('parking', 'bus_station', 'motor_park', 'taxi_stand'),
}


def main(d, js):
    rows = json.load(open(js))[d]['blocks']
    D, recs, ring_g, ring_u = B.load(d)
    w, s, e, n = B.lonlat_box(ring_u)
    blocks, slivers, *_ = B.blocks_of(ring_u, w, s, e, n)
    assert len(blocks) == len(rows), 'block split differs from the JSON'
    ids = [r['block'] for r in rows]

    def block_of(pt):
        for k, bk in enumerate(blocks):
            if bk.contains(pt):
                return ids[k]
        return 'street/sliver'

    c_lon, c_lat = B.TL.transform(ring_u.centroid.x, ring_u.centroid.y)
    t90, t80, tok = B.threshold(c_lon, c_lat)
    G = [g for c, g in B.google(w, s, e, n) if c >= t90 and ring_u.contains(g.centroid)]
    big = [g for g in G if g.area >= 1000]
    HS = B.heights(big)
    P = [p for p in B.places(w, s, e, n) if ring_u.buffer(60).contains(p[3])]
    print(f'tile {tok}: 90% {t90}; Google at 90% with centroid in the outline: {len(G)}; of 1,000 m2 and more: {len(big)}')
    print('\n== big roofs (area m2 | height m | storeys | block | lat, lon | Gidi x, y | places within 60 m)')
    for g, h in sorted(zip(big, HS), key=lambda t: -t[0].area):
        lon, lat = B.TL.transform(g.centroid.x, g.centroid.y)
        gx, gy = B.u2g(g.centroid.x, g.centroid.y)
        near = sorted(((round(g.distance(q)), c, nm) for c, nm, cf, q in P if g.distance(q) <= 60 and nm),
                      key=lambda t: t[0])
        print(f'{g.area:7.0f} | {h if h is None else round(h, 1)} | {None if h is None else B.storeys(h)} | '
              f'{block_of(g.centroid)} | {lat:.5f}, {lon:.5f} | {gx:.0f}, {gy:.0f} | '
              + '; '.join(f'{dd} m {c} | {nm}' for dd, c, nm in near[:5]))

    print('\n== blocks holding a roof of 1,000 m2 or more: roofs of 1,000 m2+ against all roofs (centroid in the block)')
    for k, bk in enumerate(blocks):
        allr = [g.area for g in G if bk.contains(g.centroid)]
        bigr = [a for a in allr if a >= 1000]
        if bigr:
            print(f'{ids[k]}: {len(bigr)} big of {len(allr)} roofs; big roof {sum(bigr):,.0f} m2 of {sum(allr):,.0f} m2 '
                  f'({sum(bigr) / sum(allr):.0%}); block {bk.area:,.0f} m2')

    print('\n== named places by kind (in the outline)')
    Pin = [p for p in P if ring_u.contains(p[3])]
    print('places in the outline:', len(Pin))
    for kind, cats in KINDS.items():
        hit = [p for p in Pin if p[0] in cats]
        print(f'\n{kind}: {len(hit)}')
        for c, nm, cf, q in sorted(hit, key=lambda p: block_of(p[3])):
            lon, lat = B.TL.transform(q.x, q.y)
            print(f'  {block_of(q)} | {c} | {nm} | conf {cf:.2f} | {lat:.5f}, {lon:.5f}')

    print('\n== land use, not residential, inside the outline')
    for src, sub, cls, nm, g in B.landuse(w, s, e, n):
        if cls in ('residential', 'land') or 'Pacific Islands Heritage' in str(nm):
            continue
        a = g.intersection(ring_u)
        if a.area < 50:
            continue
        lon, lat = B.TL.transform(a.centroid.x, a.centroid.y)
        cnt = sum(1 for q in G if a.contains(q.centroid))
        print(f'{sub} | {cls} | {nm} | {a.area:,.0f} m2 real | {block_of(a.representative_point())} | '
              f'{lat:.5f}, {lon:.5f} | Google buildings in it {cnt}')
    houses = [r for r in recs if r['type'] == 'building']
    print('\nour houses:', len(houses), dict(collections.Counter(h['kind'] for h in houses)))
    print('our roof area, Gidi m2 (real-size footprints):', round(sum(Polygon(h['footprint']).area for h in houses)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
