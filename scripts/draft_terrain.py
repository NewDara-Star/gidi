"""The land's own height for the city layer, first draft (owner, 28 Oct: "include things like terrain... the topography
of the land... how high some places are to ground level and how low"; DECISIONS "The land's own height too").

  ~/.venvs/gidi/bin/python -I scripts/draft_terrain.py map [--dry]

Reads GEDTM30 v1.2, a bare-earth model (buildings and trees taken off; 1 arc-second, about 30 m; OpenGeoHub, CC BY 4.0,
credited in the game; ~/gidi-data/research/data/gedtm30/README.md), and writes it into map/d00 as `relief` grids: one
per 1 km Gidi tile, CELL m between points, so a grid's point is one of the model's own 30 m cells at 1:3. Heights stay
real metres above sea level (lengths 1:3, heights real: DECISIONS), written in whole millimetres rounded to ROUND mm,
as the model's own uncertainty (median 0.58 m) makes finer figures noise. Neighbouring grids share their edge points
with the same values, as an Unreal Landscape's components share their edge vertices.

Each point is the model's height at that place, read bilinearly from the four cells round it; where some of those are
open water with no reading (the middle of the lagoons) the readings that exist are averaged, and a point with none
takes 0, the water's level: the bed under it comes from the water records' depth (owed). Each grid's note counts its
points with no reading.

A draft never overwrites: if map/d00 already holds relief records, nothing is written (re-drafted only when the owner
asks; the hand edits then are made on the board).
"""
import hashlib
import json
import os
import sys

import numpy as np
import rasterio
from pyproj import Transformer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from check_map import canonical   # noqa: E402

DEM = os.path.expanduser('~/gidi-data/research/data/gedtm30/lagos_gedtm30_rf_m_v1.2.tif')
W, H = 27000, 10500     # the frame, Gidi m
TILE = 1000             # Gidi m a grid
CELL = 10.0             # Gidi m between points: the model's 30 m at 1:3
ROUND = 100             # mm
SRC = ('GEDTM30 v1.2 bare-earth heights (OpenGeoHub, CC BY 4.0), read bilinearly at each point; first draft, '
       'scripts/draft_terrain.py, 28 Oct')


def heights(xs, ys):
    """The model's height in m at Gidi points (arrays); NaN where no cell round the point has a reading."""
    T = Transformer.from_crs(32631, 4326, always_xy=True)
    lon, lat = T.transform(3 * xs + 500525, 707825 + 3 * (H - ys))
    with rasterio.open(DEM) as f:
        z = f.read(1).astype('float64')
        nod = f.nodata
        inv = ~f.transform
    z[(z == nod) | (z > 1e30) | ~np.isfinite(z)] = np.nan
    c, r = inv * (lon, lat)
    c, r = c - 0.5, r - 0.5       # to cell centres
    c0, r0 = np.floor(c).astype(int), np.floor(r).astype(int)
    fc, fr = c - c0, r - r0
    acc, wsum = np.zeros(xs.shape), np.zeros(xs.shape)
    for dr, dc, w in ((0, 0, (1 - fr) * (1 - fc)), (0, 1, (1 - fr) * fc), (1, 0, fr * (1 - fc)), (1, 1, fr * fc)):
        v = z[np.clip(r0 + dr, 0, z.shape[0] - 1), np.clip(c0 + dc, 0, z.shape[1] - 1)]
        ok = np.isfinite(v)
        acc += np.where(ok, v * w, 0)
        wsum += np.where(ok, w, 0)
    return np.where(wsum > 0, acc / np.where(wsum > 0, wsum, 1), np.nan)


def main():
    top = sys.argv[1]
    dry = '--dry' in sys.argv
    dd = os.path.join(top, 'd00', 'dress')
    if os.path.isdir(dd) and any(r.get('type') == 'relief' for f in os.listdir(dd)
                                 for r in json.load(open(os.path.join(dd, f)))['records']):
        sys.exit('map/d00 already holds relief records: a draft never overwrites the hand-edited land')
    files, none_total, n_total, lo, hi = {}, 0, 0, 1e9, -1e9
    for ty in range(0, H, TILE):
        for tx in range(0, W, TILE):
            cols = int(min(TILE, W - tx) / CELL) + 1
            rows = int(min(TILE, H - ty) / CELL) + 1
            gx, gy = np.meshgrid(tx + CELL * np.arange(cols), ty + CELL * np.arange(rows))
            z = heights(gx.ravel(), gy.ravel())
            none = int(np.isnan(z).sum())
            mm = [int(v) for v in (np.round(np.nan_to_num(z, nan=0.0) * 1000 / ROUND) * ROUND)]
            none_total += none
            n_total += len(mm)
            lo, hi = min(lo, min(mm)), max(hi, max(mm))
            rid = 'rl-' + hashlib.sha1(f'd00 land {tx} {ty}'.encode()).hexdigest()[:8]
            note = SRC + (f'; {none} of {len(mm)} points with no reading (open water) set to 0' if none else '')
            rec = {'id': rid, 'type': 'relief', 'origin': [tx, ty], 'cell': CELL, 'cols': cols, 'rows': rows,
                   'z_mm': mm, 'note': note}
            name = f'{tx // 100}_{ty // 100}.json'
            files[name] = {'format': 'gidi-map/0.1', 'district': 'd00', 'layer': 'dress', 'tile': [tx // 100, ty // 100],
                           'records': [rec]}
    print(f'{len(files)} grids, {n_total} points, {none_total} with no reading ({none_total / n_total:.1%}); '
          f'heights {lo / 1000:.1f} to {hi / 1000:.1f} m')
    if dry:
        return
    os.makedirs(dd, exist_ok=True)
    size = 0
    for name, doc in files.items():
        s = canonical(doc)
        size += len(s)
        open(os.path.join(dd, name), 'w').write(s)
    print(f'written {len(files)} files into {dd}, {size / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
