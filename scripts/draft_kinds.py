"""A district's first draft of each house's kind and ground floor, from its size, its storeys and the street it faces.

  ~/.venvs/gidi/bin/python scripts/draft_kinds.py map/d15 [--dry]

Industry: rule-based city fillers choose each plot's building by its footprint, its size and which of its sides face a
street (Scharl, "A Constraint Based System to Populate Procedurally Modeled Cities", CESCG 2010); street-class tagging
then puts shops on the busy roads and homes on the side streets. Here the street is read from the map's roads and the
kinds from Mùṣá's Street View sample (~/gidi-data/research/google/b1/STUDY.md, 24 Oct): long 2-storey rows with lock-up
shops below on the busier streets; 2-storey blocks behind a compound wall and gate, bungalows, and 3-storey blocks of
flats with balconies on the lanes.

The street a house faces: the nearest road whose edge is within FRONT m of the footprint (a motorway is not faced: its
houses face a service road or nothing). Busy: market_street, main_road, trunk, local_main, service_road; quiet:
home_street, lane, path; none: interior (behind other houses).

  footprint over SHED m2, 1-2 storeys         shed             workshop
  footprint under KIOSK m2, busy street       kiosk_row        lock_ups
  footprint under KIOSK m2, otherwise         shack            home
  1 storey, busy                              face_me_bungalow lock_ups
  1 storey, otherwise                         face_me_bungalow home
  2+ storeys, busy                            shop_under_flats lock_ups
  2 storeys, otherwise                        compound_house   home
  3+ storeys, otherwise                       walkup           flats

Written only where a house has storeys and no kind or ground floor yet ("Rules draft, records rule"): a house without
storeys is left for the hand pass, and a field already set is never changed. Schools, churches, mosques and markets are
not guessed: they are set by hand from the shots.
"""
import json
import sys
import os

from shapely.geometry import LineString, Polygon
from shapely.strtree import STRtree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draft_buildings import WIDTH

FRONT, SHED, KIOSK = 3.0, 600, 25
BUSY = {'market_street', 'main_road', 'trunk', 'local_main', 'service_road'}


def faces(h, roads, lines, tree):
    best = None
    for j in tree.query(h.buffer(FRONT + 15)):
        r = roads[j]
        if r['kind'] == 'motorway':
            continue
        d = lines[j].distance(h) - (r.get('width') or WIDTH[r['kind']]) / 2
        if d <= FRONT and (best is None or d < best[0]):
            best = (d, r['kind'])
    return 'none' if best is None else 'busy' if best[1] in BUSY else 'quiet'


def kind(area, storeys, street):
    if area > SHED and storeys <= 2:
        return 'shed', 'workshop'
    if area < KIOSK:
        return ('kiosk_row', 'lock_ups') if street == 'busy' else ('shack', 'home')
    if storeys == 1:
        return 'face_me_bungalow', 'lock_ups' if street == 'busy' else 'home'
    if street == 'busy':
        return 'shop_under_flats', 'lock_ups'
    return ('compound_house', 'home') if storeys == 2 else ('walkup', 'flats')


def main():
    d = sys.argv[1].rstrip('/')
    pf = f'{d}/plan.json'
    plan = json.load(open(pf))
    roads = [r for r in plan['records'] if r['type'] == 'road']
    lines = [LineString(r['centreline']) for r in roads]
    tree = STRtree(lines)
    n, skip = {}, 0
    for r in plan['records']:
        if r['type'] != 'building':
            continue
        if 'storeys' not in r or 'kind' in r or 'ground_floor' in r:
            skip += 1
            continue
        h = Polygon(r['footprint'])
        street = faces(h, roads, lines, tree)
        r['kind'], r['ground_floor'] = kind(h.area, r['storeys'], street)
        k = (r['kind'], r['ground_floor'], street)
        n[k] = n.get(k, 0) + 1
    for k, v in sorted(n.items(), key=lambda t: -t[1]):
        print(f'{v:5d}  {k[0]:17s} {k[1]:9s} ({k[2]} street)')
    print(f'{sum(n.values())} written; {skip} left (no storeys, or kind or ground floor already set)')
    if '--dry' not in sys.argv:
        json.dump(plan, open(pf, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
