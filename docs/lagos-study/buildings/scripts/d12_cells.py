"""Agunda (d12): the big blocks cut into 150 m real cells (building study, 27 Oct).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d12_cells.py [--min 150000] [--cell 150] [--json out.json]

d17_blocks.py d12 leaves two blocks far bigger than a street block (D12-226, 1.15 km2 real, in the east; D12-139,
0.82 km2, in the middle), because Overture's street network has no segments through them. This takes every block of
at least --min real m2 (the same blocks, the same numbering as d17_blocks.py: the functions are imported from it) and
cuts it into --cell x --cell real-metre cells on a grid anchored at the block's bounds; for each cell piece of at least
2,000 m2 it reads the same measures as d17_blocks.py (Google Open Buildings v3 at the tile's 90% threshold, 2.5D 2023
storeys, WorldCover, Overture places and land use, our houses and carriageways in Gidi metres).
Prints one JSON line per cell; with --json writes them all.
"""
import json
import os
import sys

import shapely
from shapely.geometry import box

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B   # noqa: E402


def main():
    a = sys.argv
    MIN = float(a[a.index('--min') + 1]) if '--min' in a else 150000
    CELL = float(a[a.index('--cell') + 1]) if '--cell' in a else 150
    out = a[a.index('--json') + 1] if '--json' in a else None
    d = 'd12'
    # run the block study once, but measure cells instead of blocks: re-use study()'s inner pieces by patching
    D, recs, ring_g, ring_u = B.load(d)
    w, s, e, n = B.lonlat_box(ring_u)
    blocks, slivers, roads, rails, cut = B.blocks_of(ring_u, w, s, e, n)
    big = [(f'{d.upper()}-{k + 1:02d}', bk) for k, bk in enumerate(blocks) if bk.area >= MIN]
    cells = []
    for name, bk in big:
        x0, y0, x1, y1 = bk.bounds
        j = 0
        y = y1
        while y > y0:
            x = x0
            while x < x1:
                piece = bk.intersection(box(x, y - CELL, x + CELL, y))
                for p in getattr(piece, 'geoms', [piece]):
                    if p.geom_type == 'Polygon' and p.area >= B.MIN_BLOCK:
                        j += 1
                        cells.append((f'{name}.{j:02d}', p))
                x += CELL
            y -= CELL
    # measure with study()'s own measure(): call study() on a patched blocks_of that returns the cells
    orig = B.blocks_of
    B.blocks_of = lambda *_: ([c for _, c in cells], slivers, roads, rails, cut)
    try:
        summary, rows = B.study(d)
    finally:
        B.blocks_of = orig
    res = []
    for (name, _), r in zip(cells, rows):
        r['block'] = name
        res.append(r)
        print(json.dumps(r, ensure_ascii=False, default=str))
    if out:
        json.dump({d: {'summary': {'cells_of': [nm for nm, _ in big], 'cell_m': CELL}, 'blocks': res}},
                  open(out, 'w'), ensure_ascii=False, indent=1, default=str)


if __name__ == '__main__':
    main()
