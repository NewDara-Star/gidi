"""Bake the walk map: what every square metre of Gidi is, for the Mock's movement.

python3 tools/walkmap/bake_walk.py            (run after blender/city_run.py; it reads web/city/monuments.json)

Writes web/city/walk/<tx>_<ty>.png, one 400 x 400 greyscale PNG per city tile (1 px = 1 m, the
same tiles as web/city/<detail>/tiles, rows running south as the data's y does). Each pixel is a class:

  0 BLOCK   buildings, estate walls, monuments, the unbuilt districts, off the map
  1 GROUND  open ground: walkable, drivable off-road
  2 FOOT    pavements and footpaths
  3 ROAD    streets, lanes, main roads and expressways: walkable (people do), drivable
  4 DECK    a road bridge over the water: walkable and drivable (height from World.deckHeight)
  5 FOOTDECK jetties, boardwalks, canal footbridges: walkable
  6 WATER   the lagoon, creeks, the sea and the canals: nobody walks or drives here

and web/city/walk/carwalls.json: the shore as low wall segments for the car's physics
([ax, ay, bx, by, ...] in data metres), with gaps wherever a road, a bridge or a jetty meets it.
Flyovers stay as ground here; the Mock lifts traffic onto them by heading (World.deckHeight).
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'blender'))
TILE = 400
BLOCK, GROUND, FOOT, ROAD, DECK, FOOTDECK, WATER = range(7)
WIDTH = {'main': 14.0, 'street': 7.0, 'lane': 3.5, 'path': 2.5}  # blender/city.py WIDTH
ART_W = {'exp': 30.0, 'art': 18.0, 'bridge': 22.0}  # blender/city.py ART_W
CANAL_W = 8.0  # blender/gidi_kit/structures.py

src = open(os.path.join(ROOT, 'web', 'gidi-data.js')).read()
GD = json.loads(src[src.index('{'):src.rindex('}') + 1])
W, H = int(GD['size'][0]), int(GD['size'][1])
img = Image.new('L', (W, H), GROUND)
dr = ImageDraw.Draw(img)


def poly(pts, v):
    if len(pts) >= 3:
        dr.polygon([tuple(p) for p in pts], fill=v)


def line(pts, w, v):
    if len(pts) >= 2:
        dr.line([tuple(p) for p in pts], fill=v, width=max(1, int(round(w))), joint='curve')
        r = w / 2
        for p in (pts[0], pts[-1]):  # round ends, so lines meet cleanly
            dr.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=v)


def snap_footbridge(pts):
    """As blender/gidi_kit/structures.py snap_footbridge: centred across the nearest canal."""
    m = ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
    best = None
    for c in GD.get('canals', []):
        for a, b in zip(c['pts'], c['pts'][1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy or 1
            t = max(0.0, min(1.0, ((m[0] - a[0]) * dx + (m[1] - a[1]) * dy) / L2))
            q = (a[0] + dx * t, a[1] + dy * t)
            d = math.dist(q, m)
            if d < 10 and (best is None or d < best[0]):
                best = (d, q, (-dy / math.sqrt(L2), dx / math.sqrt(L2)))
    if not best:
        return pts
    _, q, n = best
    half = max(math.dist(pts[0], pts[-1]), CANAL_W + 4) / 2
    return [(q[0] - n[0] * half, q[1] - n[1] * half), (q[0] + n[0] * half, q[1] + n[1] * half)]


built = set(GD['buildings'])
unbuilt = [d for d in GD['districts'] if d['id'] not in built]

# the land, then the water on it
for p in GD['water'] + GD['ocean']:
    poly(p, WATER)
for c in GD.get('canals', []):
    line(c['pts'], CANAL_W, WATER)

# pavements either side of the bigger roads, then the roads over them
roads = []
for m in GD.get('mains', []):
    roads.append((m['pts'], WIDTH['main'], True))
for kind, key in (('street', 'streets'), ('lane', 'lanes')):
    for lst in GD.get(key, {}).values():
        for ln in lst:
            roads.append((ln, WIDTH[kind], kind == 'street'))
for a in GD.get('arterials', []):
    if a['cls'] != 'bridge':
        roads.append((a['pts'], ART_W.get(a['cls'], 18.0), a['cls'] != 'exp'))
for pts, w, pave in roads:
    if pave:
        line(pts, w + 5.0, FOOT)
for pts, w, _ in roads:
    line(pts, w, ROAD)
for lst in GD.get('paths', {}).values():
    for ln in lst:
        line(ln, WIDTH['path'], FOOT)

# decks over the water
for b in GD.get('boardwalks', []):
    line(b, 2.0, FOOTDECK)
for s in GD.get('structures', []):
    if s['kind'] == 'jetty':
        line(s['pts'], max(2.0, s['width']), FOOTDECK)
    elif s['kind'] == 'footbridge':
        line(snap_footbridge(s['pts']), max(2.0, s['width']), FOOTDECK)
for a in GD.get('arterials', []):
    if a['cls'] == 'bridge':
        line(a['pts'], ART_W['bridge'], DECK)

# what nobody walks through
for d, lst in GD['buildings'].items():
    for b in lst:
        poly(b[1:], BLOCK)
for segs in (GD.get('walls') or {}).values():
    for w_ in segs:
        line(w_, 1.0, BLOCK)
for g in GD.get('gates', []):  # the gates in those walls
    line(g['pts'], 4.0, ROAD)
mon = os.path.join(ROOT, 'web', 'city', 'monuments.json')
for m in (json.load(open(mon)) if os.path.exists(mon) else []):
    if m['kind'] == 'arch':  # the two pylons beside the road
        h = m.get('span', 16) / 2 + 1.2
        nx, ny = -math.sin(m['ang']), -math.cos(m['ang'])  # ang is in Blender's frame (y north)
        for sg in (-1, 1):
            c = (m['x'] + nx * h * sg, m['y'] + ny * h * sg)
            dr.rectangle([c[0] - 1, c[1] - 1, c[0] + 1, c[1] + 1], fill=BLOCK)
    else:
        r = m.get('r', 2)
        dr.rectangle([m['x'] - r, m['y'] - r, m['x'] + r, m['y'] + r], fill=BLOCK)
for d in unbuilt:
    poly(d['poly'][0], BLOCK)

a = np.asarray(img)
out = os.path.join(ROOT, 'web', 'city', 'walk')
os.makedirs(out, exist_ok=True)
n = 0
for ty in range(math.ceil(H / TILE)):
    for tx in range(math.ceil(W / TILE)):
        t = np.zeros((TILE, TILE), np.uint8)  # off the map: blocked
        part = a[ty * TILE:(ty + 1) * TILE, tx * TILE:(tx + 1) * TILE]
        t[:part.shape[0], :part.shape[1]] = part
        Image.fromarray(t, 'L').save(os.path.join(out, f'{tx}_{ty}.png'), optimize=True)
        n += 1

# the shore for the car: water edges in 5 m pieces, open where anything you can drive or walk on
# meets it (look 4 m either side of each piece's middle)
walls = []
for p in GD['water'] + GD['ocean']:
    for i in range(len(p)):
        A, B = p[i], p[(i + 1) % len(p)]
        L = math.dist(A, B)
        k = max(1, int(L / 5))
        for j in range(k):
            a0 = (A[0] + (B[0] - A[0]) * j / k, A[1] + (B[1] - A[1]) * j / k)
            a1 = (A[0] + (B[0] - A[0]) * (j + 1) / k, A[1] + (B[1] - A[1]) * (j + 1) / k)
            mx, my = (a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2
            if not (0 <= mx < W and 0 <= my < H):
                continue
            x0, x1, y0, y1 = max(0, int(mx) - 4), min(W, int(mx) + 5), max(0, int(my) - 4), min(H, int(my) + 5)
            win = a[y0:y1, x0:x1]
            if np.isin(win, (ROAD, DECK, FOOTDECK)).any() or not (win == WATER).any():
                continue  # a road, bridge or jetty meets the water here, or the edge is inland
            walls += [round(a0[0], 2), round(a0[1], 2), round(a1[0], 2), round(a1[1], 2)]
json.dump(walls, open(os.path.join(out, 'carwalls.json'), 'w'))
counts = np.bincount(a.ravel(), minlength=7)
print(f'{n} tiles; {len(walls) // 4} shore wall pieces;', ', '.join(f'{k} {c / a.size:.1%}' for k, c in zip(('block', 'ground', 'foot', 'road', 'deck', 'footdeck', 'water'), counts)))
