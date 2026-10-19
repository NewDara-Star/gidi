"""Ìbùdó spot 1 (docs/hand/ibudo/design_v1.png, the owner's approval 19 Oct 2026): Oshodi rebuilt one-for-one beside the Ring
Road flyover, written as hand edits into web/hand/hub.json. Run once, then bake with GIDI_THAW=hub, check, freeze.

The design's frame (metres, x east, y north, the flyover's centre over Market Road at (221, 145)) is laid on the map so that
point sits on the Ring Road Flyover at map (8676, 4120); the map's y runs south.
"""
import json
from shapely.geometry import LineString, Point, Polygon

FX, FY = 8676.0, 4120.0
ALLEYS = [[(103, 158), (103, 300)], [(10, 206.5), (196, 206.5)], [(10, 254), (196, 254)]]   # the market's alleys (design frame)


def M(x, y):   # design metres -> map
    return [round(FX + (x - 221), 1), round(FY - (y - 145), 1)]


def rect(x0, y0, x1, y1):
    return [M(x0, y0), M(x1, y0), M(x1, y1), M(x0, y1)]


import os
s = open(os.environ.get('GIDI_BASE', 'web/gidi-data.js')).read()   # the map before this spot (the bake's data, or a saved copy)
G = json.loads(s[s.index('{'):s.rstrip().rstrip(';').rindex('}') + 1])
clear = Polygon(rect(0, 114, 200, 302))   # the market, both shop rows and Market Road, west of the flyover
WHO = 'Claude, 19 Oct 2026: Ìbùdó spot 1 (Oshodi, one-for-one)'
E = []
new_rows = [Polygon(rect(0, 114, 200, 132)), Polygon(rect(0, 156, 200, 174)), Polygon(rect(8, 172, 198, 303)), Polygon(rect(196, 133, 320, 157))]   # (+ Market Road's way east, past the flyover)
for b in G['buildings']['hub']:
    if len(b) < 4:
        continue
    g = Polygon(b[1:]).buffer(0)
    if clear.contains(g.representative_point()) or any(g.intersects(r) for r in new_rows):   # inside, or under a new shop row
        p = g.representative_point()
        E.append({'op': 'delete building', 'at': [round(p.x, 1), round(p.y, 1)], 'early': True, 'note': 'cleared for the market and Market Road', 'by_who': WHO})
for k in ('streets', 'lanes'):   # streets into the cleared ground: cut back to what lies outside it (their far ends still serve houses)
    for st in (G.get(k) or {}).get('hub', []):
        g = LineString(st)
        if not g.intersects(clear.buffer(-1)):
            continue
        p = g.interpolate(0.5, normalized=True)
        E.append({'op': 'delete street', 'at': [round(p.x, 1), round(p.y, 1)], 'note': 'cleared for the market', 'by_who': WHO})
        rest = g.difference(clear.buffer(2))
        for part in getattr(rest, 'geoms', [rest]):
            if part.geom_type == 'LineString' and part.length > 8:
                E.append({'op': 'add street', 'kind': 'lane' if k == 'lanes' else 'street', 'pts': [[round(x, 1), round(y, 1)] for x, y in part.coords],
                          'note': 'the part outside the market, kept', 'by_who': WHO})
E.append({'op': 'add street', 'kind': 'street', 'pts': [M(0, 144), M(320, 144)],   # a plain street: the kit draws mains as tarred
          'note': 'Market Road, after Oshodi Road: mud, no kerb, under the flyover (named by its place pin)', 'by_who': WHO})   # highways
for line in ([M(*a), M(*b)] for a, b in ALLEYS):
    E.append({'op': 'add street', 'kind': 'lane', 'pts': line, 'note': 'the market\'s alleys: from the gate in, and across', 'by_who': WHO})
for f in G['furniture']:   # poles and posts that would stand inside the new shops and sheds
    if f.get('d') == 'hub' and clear.contains(Point(f['x'], f['y'])):
        E.append({'op': 'delete furniture', 'at': [f['x'], f['y']], 'kind': f['kind'], 'by_who': WHO})
E.append({'op': 'add structure', 'kind': 'footbridge', 'name': 'Ìbùdó Footbridge', 'pts': [M(190, 112), M(300, 112)], 'width': 3,
          'layer': 1, 'note': 'over the flyover foot to the terminal side (our truss)', 'by_who': WHO})
E.append({'op': 'add parcel', 'kind': 'market', 'pts': rect(10, 174, 196, 300) + [rect(10, 174, 196, 300)[0]],
          'name': 'Ìbùdó Market', 'note': 'after Oshodi Market', 'by_who': WHO})
alley_ground = [LineString([M(*a), M(*b)]).buffer(4.5) for a, b in ALLEYS]
for x0 in (14, 28.5, 43, 57.5, 72, 86.5, 107.5, 122, 136.5, 151, 165.5):   # the market's stall sheds: 13 x 12 m, 1.5 m gaps,
    for y0 in (176, 189.5, 211, 224.5, 238, 258.5, 272, 285.5):         # 8 m alleys left clear (ALLEYS)
        E.append({'op': 'add building', 'kind': 'shed', 'pts': rect(x0, y0, x0 + 13, y0 + 12), 'by_who': WHO})
for yy in (158, 116):   # two-storey shop rows both sides of Market Road (balconies with doors: the kit's fronts)
    for x in range(4, 190, 9):   # stopping short of the Ring Road's edge
        if yy == 158 and 92 <= x <= 110:
            continue   # the gate
        E.append({'op': 'add building', 'kind': 'front', 'pts': rect(x, yy, x + 8.4, yy + 14), 'storeys': 2, 'by_who': WHO})
gx, gy = M(101, 165)
E.append({'op': 'add monument', 'model': 'arch', 'x': gx, 'y': gy, 'ang': 0, 'span': 18, 'name': 'ÌBÙDÓ MARKET',
          'note': 'the market gate: a painted arch (red bars in the kit later)', 'by_who': WHO})
for side in (133.5, 154.5):   # traders on planks and tarps on the road edges
    E.append({'op': 'add zone', 'kind': 'market street', 'pts': rect(4, side - 3, 198, side + 3) + [rect(4, side - 3, 198, side + 3)[0]], 'by_who': WHO})
for x in range(10, 200, 25):
    E.append({'op': 'set surface', 'at': M(x, 144), 'surface': 'mud', 'by_who': WHO})
for p in G['pois']:   # places whose building the market cleared
    if p.get('d') == 'hub' and clear.contains(Point(p['x'], p['y'])):
        E.append({'op': 'delete place', 'name': p['name'], 'at': [p['x'], p['y']], 'note': 'its building cleared for the market', 'by_who': WHO})
mx, my = M(103, 238)
E.append({'op': 'add place', 'name': 'Ìbùdó Market', 'type': 'market', 'x': mx, 'y': my, 'note': 'Red-roof stall sheds behind the shop rows; the gate on Market Road.', 'by_who': WHO})
px, py = M(150, 145)
E.append({'op': 'add place', 'name': 'Market Road', 'type': 'story', 'x': px, 'y': py,
          'note': 'Spot 1 of the Lagos pass: video 1 plays out here, from the gate to under the flyover.', 'by_who': WHO})
for i in range(9):   # danfos jammed along Market Road
    x, y = M(112 + i * 9, 150.2)   # parked tight at the road edge, nose to tail
    E.append({'op': 'add thing', 'k': 'danfo', 'x': x, 'y': y, 'a': 0 if i % 2 else 180, 'c': 'battered', 'by_who': WHO})
H = json.load(open('web/hand/hub.json'))
H['edits'] = H.get('edits', []) + E
json.dump(H, open('web/hand/hub.json', 'w'), separators=(',', ':'))
print(len(E), 'edits:', sum(e['op'] == 'delete building' for e in E), 'buildings cleared,', sum(e['op'] == 'delete street' for e in E), 'streets cleared')
