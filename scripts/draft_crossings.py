"""A district's first draft of each road's crossings: the bridges over its open gutters into the houses that face it.

  ~/.venvs/gidi/bin/python scripts/draft_crossings.py map/d15 [--dry]

In the Mushin Street View reading (road_reads.tsv) the open drains are crossed wherever a house is entered from the road:
a slab or a plank at each gate or door, and a slab the width of the shop front before a row of lock-ups. So each house
whose front stands within FRONT m of a road's open gutter (open_concrete or open_earth; a slab-covered drain needs no
bridge) gets one crossing on that side, at the point of the road nearest the house's middle:
- lock-ups: a slab_bridge the length of the house's side along the road (up to SHOP_MAX m);
- a workshop or shed: a gate_ramp GATE m wide (a vehicle gate);
- any other house: a slab_bridge over a concrete drain, a plank_bridge over an earth one, DOOR m wide.
A road with no open gutter gets no crossings (an empty list: drawn, none there).

Industry: game cities place street props by rule where the rule is sure and by hand where it is not, the rule's points
handed to the engine as instances (Astragon, "Brighton Was Not Built in a Day", on their Houdini road tools). Here the
rule is the frontage seen in Street View; the hand pass corrects it street by street.

Written only where a road has no crossings yet ("Rules draft, records rule").
"""
import json
import sys
from collections import Counter

from shapely.geometry import LineString, Point, Polygon
from shapely.strtree import STRtree

FRONT, DOOR, GATE, SHOP_MAX = 2.5, 1.2, 3.0, 12.0
OPEN = ('open_concrete', 'open_earth')


def side_of(L, s, p):
    # the board's y axis points down, so a point on the walker's left gives a negative cross product
    a, b = L.interpolate(max(s - 0.5, 0)), L.interpolate(min(s + 0.5, L.length))
    return 'left' if (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x) < 0 else 'right'


def main():
    pf = sys.argv[1].rstrip('/') + '/plan.json'
    plan = json.load(open(pf))
    bs = [r for r in plan['records'] if r['type'] == 'building']
    polys = [Polygon(r['footprint']) for r in bs]
    tree = STRtree(polys)
    n, kinds = 0, Counter()
    for road in plan['records']:
        if road['type'] != 'road' or 'crossings' in road:
            continue
        L = LineString([p[:2] for p in road['centreline']])
        gut = [g for g in road.get('gutters', []) if g['kind'] in OPEN]
        out = []
        for g in gut:
            reach = g['offset'] + g['width'] / 2 + FRONT
            for j in tree.query(L.buffer(reach)):
                h = polys[j]
                c = h.centroid
                s = L.project(c)
                if not g['s0'] <= s < g['s1'] or h.distance(L) > reach:
                    continue
                if side_of(L, s, Point(c.x, c.y)) != g['side']:
                    continue
                gf = bs[j].get('ground_floor')
                if gf == 'lock_ups':
                    a, b = L.project(Point(min(h.exterior.coords, key=lambda q: L.project(Point(q))))), \
                        L.project(Point(max(h.exterior.coords, key=lambda q: L.project(Point(q)))))
                    w, kind = min(max(b - a, DOOR), SHOP_MAX), 'slab_bridge'
                elif gf == 'workshop' or bs[j].get('kind') == 'shed':
                    w, kind = GATE, 'gate_ramp'
                else:
                    w, kind = DOOR, 'slab_bridge' if g['kind'] == 'open_concrete' else 'plank_bridge'
                out.append({'side': g['side'], 's': round(s, 1), 'w': round(w, 1), 'kind': kind})
        # one crossing per house: two gutter stretches meeting at a house's middle could both take it
        seen, uniq = set(), []
        for c in sorted(out, key=lambda c: (c['side'], c['s'])):
            if (c['side'], c['s']) not in seen:
                seen.add((c['side'], c['s']))
                uniq.append(c)
        road['crossings'] = uniq
        kinds.update(c['kind'] for c in uniq)
        n += 1
    print(f'{n} roads given crossings;', dict(kinds), f'; {sum(kinds.values())} in all')
    if '--dry' not in sys.argv:
        json.dump(plan, open(pf, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
