"""A district's first draft of storeys for the houses that draft_storeys.py could not read, from the houses around them.

  ~/.venvs/gidi/bin/python scripts/draft_storeys_nearby.py map/d15 [--dry]

draft_storeys.py reads each house's storeys from its real source's Open Buildings 2.5D height; houses whose source was not
found again, or whose source has no built pixels in 2.5D, are left without. This gives each of those the median storeys
of the houses within NEAR m of it that have storeys (rounded down on a tie), and a house under KIOSK m2 one storey (a
kiosk or shack: draft_kinds.py's size line).

Industry: missing building heights in OpenStreetMap are estimated from each building's surroundings (Bernard et al.,
"Estimation of missing building height in OpenStreetMap data: a French case study using GeoClimate", Geoscientific Model
Development 15, 7505, 2022: a random forest on 62 indicators of the building and its neighbours, half the buildings
within 4 m). This is the simplest form of it, the neighbours' median; the Street View check by hand follows.

Written only where a house has no storeys ("Rules draft, records rule"); a house with no house with storeys within NEAR m
is left for the hand pass.
"""
import json
import sys
import os

from shapely.geometry import Polygon
from shapely.strtree import STRtree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draft_kinds import KIOSK

NEAR = 30


def main():
    pf = sys.argv[1].rstrip('/') + '/plan.json'
    plan = json.load(open(pf))
    bs = [r for r in plan['records'] if r['type'] == 'building']
    known = [r for r in bs if 'storeys' in r]
    polys = [Polygon(r['footprint']) for r in known]
    tree = STRtree(polys)
    n, left = {}, 0
    for r in bs:
        if 'storeys' in r:
            continue
        h = Polygon(r['footprint'])
        if h.area < KIOSK:
            s = 1
        else:
            near = sorted(known[j]['storeys'] for j in tree.query(h.buffer(NEAR)) if polys[j].distance(h) <= NEAR)
            if not near:
                left += 1
                continue
            s = near[(len(near) - 1) // 2]
        r['storeys'] = s
        n[s] = n.get(s, 0) + 1
    print('storeys written:', dict(sorted(n.items())), f'; {sum(n.values())} written; {left} with no neighbour within {NEAR} m')
    if '--dry' not in sys.argv:
        json.dump(plan, open(pf, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
