"""Real roofs under the new frame, for the drawing board's zoomed-in "Real roofs" layer (web/board.html).

Google Open Buildings v3 footprints (confidence 0.65 or more) moved into the 1:3 frame the same way as scripts/frame_study.py,
cut into 1 km tiles (Gidi metres): web/frame-tiles/<i>_<j>.txt, one roof per line, "x,y,x,y,..." in decimetres from the
tile's corner. The board loads a tile only when zoomed in over it. A study aid, never map data: real footprints are
never committed (web/frame-tiles/ is ignored).

At 1:3 a real roof is drawn a third of its size: it shows where the fabric is and how it runs, not house sizes
(houses stay house-size in Gidi: the 22 Oct decision).

  ~/.venvs/gidi/bin/python scripts/frame_footprints.py      (a few minutes; streams the file, small memory)
"""
import csv
import gzip
import json
import os
import re
import shutil
import sys

import numpy as np
from pyproj import Transformer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'docs', 'lagos-study', 'roads', 'scripts'))
from common import DATA, WORK, SCALE, FRAME   # noqa: E402

NW = json.load(open(WORK + 'network.json'))
FU, FV = NW['fu'], NW['fv']
RH = FRAME[1] * SCALE
TILE = 1000
OUT = os.path.join(ROOT, 'web', 'frame-tiles')
T = Transformer.from_crs(4326, 32631, always_xy=True)
NUM = re.compile(r'-?\d+\.\d+')

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
buf = {}
count = {}


def flush(k, force=False):
    s = buf.get(k)
    if s and (force or len(s) > 400):
        with open(os.path.join(OUT, '%d_%d.txt' % k), 'a') as fh:
            fh.write('\n'.join(s) + '\n')
        buf[k] = []


def take(rows):
    lens = [len(r) // 2 for r in rows]
    flat = np.concatenate([np.asarray(r, float) for r in rows]).reshape(-1, 2)
    x, y = T.transform(flat[:, 0], flat[:, 1])
    gx, gy = (x - FU) / SCALE, (FV + RH - y) / SCALE
    o = 0
    for n in lens:
        px, py = gx[o:o + n], gy[o:o + n]
        o += n
        cx, cy = px.mean(), py.mean()
        if not (0 <= cx < FRAME[0] and 0 <= cy < FRAME[1]):
            continue
        k = (int(cx // TILE), int(cy // TILE))
        ox, oy = k[0] * TILE, k[1] * TILE
        q = np.round(np.column_stack([px[:-1] - ox, py[:-1] - oy]) * 10).astype(int).ravel()   # the ring, not closed
        buf.setdefault(k, []).append(','.join(map(str, q)))
        count[k] = count.get(k, 0) + 1
        flush(k)


rows = []
n = 0
with gzip.open(DATA + 'open-buildings-v3/lagos_open_buildings_v3.csv.gz', 'rt') as f:
    for r in csv.DictReader(f):
        if float(r['confidence']) < 0.65:
            continue
        g = r['geometry']
        if not g.startswith('POLYGON'):
            continue
        ring = g[g.index('((') + 2:g.index(')')]
        rows.append([float(v) for v in NUM.findall(ring)])
        if len(rows) >= 50000:
            take(rows)
            n += len(rows)
            rows = []
            print(n, 'read', sum(count.values()), 'in the frame', flush=True)
if rows:
    take(rows)
for k in list(buf):
    flush(k, True)
json.dump({'tile': TILE, 'count': {'%d_%d' % k: c for k, c in count.items()}}, open(os.path.join(OUT, 'index.json'), 'w'))
print('done:', sum(count.values()), 'roofs in', len(count), 'tiles ->', OUT)
