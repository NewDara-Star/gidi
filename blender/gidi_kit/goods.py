"""Goods and clutter: what fills a Lagos lean-to, stall or shop door. Sacks, tarps, nylon bags, crates, stacked plastics,
cloth and cartons, piled against the wall, hung from the lean-to's front plate, or heaped at a stall.

The map gives the place (a trade spot's band along its wall, or a heap's spot and radius), the kinds and how full it is
(`goods_kinds`, `goods_fill` 0..1, `hanging_kinds`, `hanging_fill`). The kit only arranges the items inside that place,
deterministically from the spot's own dice. Looked at against ot175 and the markets refs (Mile 12, Oshodi): sacks are
woven polypropylene in white, cream and grey, tarps blue or grey and slack, bags black, blue and pink.
"""
import math

import bmesh
from mathutils import Matrix, Vector

from . import parts, props
from .core import hex_rgb, shade

SACK = ['#e6e3dc', '#d2cec4', '#bdb7aa', '#e9e0c9', '#c9c3b4', '#a89f8e']
TARP = ['#2f5f9e', '#3f6fa8', '#6b7378', '#4f6b45', '#8a8f93']
BAG = ['#141414', '#1f1f22', '#2a4f9a', '#d0438a', '#e8e6e0', '#1f1f22', '#7a1f1f']
CLOTH = ['#c62828', '#f9a825', '#1f6fb8', '#2e9a46', '#7a1f6e', '#e8dcc0', '#3b2a1a', '#e07b20']
PLASTIC = ['#c62828', '#1f6fb8', '#2e9a46', '#f9a825', '#e8e4dc', '#7a1f1f']
CARTON = ['#a8835a', '#9a7a55', '#b8946a', '#8c6d4c']


def lump(mb, mat, M, w, d, h, col, wear=0.4, seg=8, top=0.45, sag=0.0):
    """A soft filled thing (a sack, a bag, a bundle): an oval prism bulging at its middle, rounded and gathered at the top."""
    rings = [(0.0, 0.82), (0.12, 1.0), (0.55, 1.04), (0.85, 0.86), (1.0, top)]
    pts = []
    for z, k in rings:
        ring = []
        for i in range(seg):
            a = i / seg * math.tau
            ring.append(M @ Vector((math.cos(a) * w / 2 * k, math.sin(a) * d / 2 * k, z * h - sag * abs(math.cos(a)) * z)))
        pts.append(ring)
    fix = (lambda q: q[::-1]) if M.to_3x3().determinant() < 0 else (lambda q: q)
    for r in range(len(pts) - 1):
        for i in range(seg):
            j = (i + 1) % seg
            c = shade(col, 0.82 + 0.18 * r / (len(pts) - 1))
            mb.face(fix([pts[r][i], pts[r][j], pts[r + 1][j], pts[r + 1][i]]), mat, c, wear)
    mb.face(fix(list(pts[-1])), mat, col, wear)


def soft(ob):
    """Weld an object's faces where they meet and shade it smooth (sacks and tarps are soft, never faceted)."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.002)
    bm.to_mesh(ob.data)
    bm.free()
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def tarp(mb, x0, x1, y0, y1, z, drop, col, rng, side=1):
    """A slack sheet thrown over a pile: across the top at z in soft folds, its front hanging down by `drop`, the hem
    wavy. side: which way the front is (+1 toward +y, -1 toward -y)."""
    nx = max(4, int((x1 - x0) / 0.12))
    yf, yb = (y1, y0) if side > 0 else (y0, y1)
    ph = [rng.between(0, math.tau) for _ in range(4)]
    fold = lambda x, k: 0.035 * math.sin(x * 6.0 + ph[0]) + 0.02 * math.sin(x * 13.0 + ph[1] + k)
    rows = [(yb, z, 0.4), ((yb + yf) / 2, z + 0.05, 1.0), (yf, z, 0.6)]
    for k in range(1, 5):
        rows.append((yf + side * 0.02 * k, z - drop * k / 4, 1.0 + k * 0.6))
    grid = []
    for k, (y, zz, amp) in enumerate(rows):
        row = []
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx
            hem = (0.18 * (0.5 + 0.5 * math.sin(x * 2.3 + ph[2])) + 0.08 * math.sin(x * 5.1 + ph[3])) * (k - 2) / 4 if k > 2 else 0.0
            if k <= 2:
                row.append(Vector((x, y, zz + fold(x, k) * amp)))
            else:
                row.append(Vector((x, y + side * fold(x, k) * amp, zz + hem)))
        grid.append(row)
    for k in range(len(grid) - 1):
        for i in range(nx):
            q = [grid[k][i], grid[k][i + 1], grid[k + 1][i + 1], grid[k + 1][i]]
            mb.face(q if side > 0 else q[::-1], 'cloth', col, 0.5)


def _item(mb, kind, M, rng, scale=1.0):
    """One item standing at M; returns its height."""
    if kind == 'sacks':
        w, d, h = rng.between(0.5, 0.75) * scale, rng.between(0.35, 0.5) * scale, rng.between(0.45, 0.8) * scale
        lump(mb, 'cloth', M, w, d, h, hex_rgb(rng.pick(SACK)), 0.5, top=rng.between(0.3, 0.6))
        return h * 0.9
    if kind == 'nylon_bags':
        h = 0
        for k in range(rng.randrange(2, 5)):
            hh = rng.between(0.2, 0.38)
            lump(mb, 'plastic', M @ Matrix.Translation((rng.between(-0.2, 0.2), rng.between(-0.12, 0.12), 0)), rng.between(0.22, 0.36), rng.between(0.18, 0.3), hh, hex_rgb(rng.pick(BAG)), 0.2, seg=7, top=0.25)
            h = max(h, hh)
        return h
    if kind == 'crates':
        n = rng.randrange(1, 5)
        for k in range(n):
            props.crate(mb, M @ Matrix.Translation((0, 0, k * 0.3)) @ Matrix.Rotation(rng.between(-0.12, 0.12), 4, 'Z'), hex_rgb(rng.pick(PLASTIC)), 0.5)
        return n * 0.3
    if kind == 'plastics':
        c = hex_rgb(rng.pick(PLASTIC))
        if rng.chance(0.5):   # a stack of basins, rims out
            n = rng.randrange(3, 9)
            for k in range(n):
                props.basin(mb, M @ Matrix.Translation((0, 0, k * 0.05)), c if rng.chance(0.7) else hex_rgb(rng.pick(PLASTIC)), r=0.28)
            return n * 0.05 + 0.1
        if rng.chance(0.5):   # buckets nested in a tower
            n = rng.randrange(2, 7)
            for k in range(n):
                parts.cyl(mb, 'plastic', M @ Matrix.Translation((0, 0, k * 0.08)), 0.13, 0.3, c, 0.3, seg=10, caps=(True, False), r2=0.16)
            return n * 0.08 + 0.22
        for k in range(rng.randrange(1, 4)):
            props.jerrycan(mb, M @ Matrix.Translation((rng.between(-0.15, 0.15), k * 0.2 - 0.2, 0)) @ Matrix.Rotation(rng.between(-0.3, 0.3), 4, 'Z'), hex_rgb(rng.pick(['#e8b923', '#e8b923', '#1f6fb8', '#e8e4dc'])))
        return 0.45
    if kind == 'cloth':   # folded cloth piled up, each fold its own print
        n = rng.randrange(3, 10)
        for k in range(n):
            mb.box('ankara' if rng.chance(0.6) else 'cloth', M @ Matrix.Translation((rng.between(-0.03, 0.03), rng.between(-0.03, 0.03), k * 0.06 + 0.03)) @ Matrix.Rotation(rng.between(-0.15, 0.15), 4, 'Z'),
                   hex_rgb(rng.pick(CLOTH)), 0.3, size=(0.55, 0.4, 0.055))
        return n * 0.06
    if kind == 'cartons':
        h = 0
        for k in range(rng.randrange(1, 4)):
            s = (rng.between(0.35, 0.6), rng.between(0.3, 0.45), rng.between(0.25, 0.45))
            mb.box('cloth', M @ Matrix.Translation((0, 0, h + s[2] / 2)) @ Matrix.Rotation(rng.between(-0.2, 0.2), 4, 'Z'), shade(hex_rgb(rng.pick(CARTON)), rng.between(0.8, 1.05)), 0.6, size=s)
            h += s[2]
        return h
    return 0.0


def band(mb, x0, x1, y_wall, depth, z0, kinds, fill, rng, side=1, tarp_over=False):
    """Goods along a wall: rows from the wall outward (`depth` deep), on a floor at z0. side +1: the wall is at +y and the
    goods come out toward -y (a left-hand shop); -1 the other way. fill 0..1 is how much of the band is taken."""
    if not kinds or fill <= 0:
        return
    rows = max(1, round(depth / 0.45))
    tops = []
    for r in range(rows):
        y = y_wall - side * (0.3 + r * depth / rows)
        x = x0 + rng.between(0.0, 0.3)
        while x < x1 - 0.3:
            step = rng.between(0.45, 0.8)
            if rng.chance(fill * (1.0 - 0.35 * r / rows)):
                kind = rng.pick(kinds)
                M = Matrix.Translation((x + step / 2, y + rng.between(-0.08, 0.08), z0)) @ Matrix.Rotation(rng.between(-0.35, 0.35), 4, 'Z')
                h = _item(mb, kind, M, rng.child('item', r, round(x, 2)), scale=1.0 if r == 0 else 0.85)
                if r == 0 and kind in ('sacks', 'cartons') and rng.chance(fill * 0.6):   # a second layer on the back row
                    _item(mb, kind, M @ Matrix.Translation((rng.between(-0.08, 0.08), 0, h)) @ Matrix.Rotation(rng.between(-0.4, 0.4), 4, 'Z'), rng.child('top', round(x, 2)), 0.9)
                tops.append(h)
            x += step
    if tarp_over and tops:
        tarp(mb, x0, x1, y_wall - side * depth, y_wall, z0 + max(tops) * 0.9, 0.5, hex_rgb(rng.pick(TARP)), rng.child('tarp'), side=-side)


def hanging(mb, x0, x1, y, z, kinds, fill, rng):
    """Things hung from a lean-to's front plate at height z: bunches of nylon bags, cloth lengths, bags of goods."""
    if not kinds or fill <= 0:
        return
    x = x0 + 0.2
    while x < x1 - 0.2:
        if rng.chance(fill):
            kind = rng.pick(kinds)
            if kind == 'cloth':   # a length of cloth hung over the plate
                L = rng.between(0.6, 1.3)
                c = hex_rgb(rng.pick(CLOTH))
                q = [Vector((x - 0.25, y, z)), Vector((x + 0.25, y, z)), Vector((x + 0.25, y + rng.between(-0.03, 0.03), z - L)), Vector((x - 0.25, y, z - L))]
                mb.face(q, 'ankara', c, 0.3)
                mb.face(q[::-1], 'ankara', shade(c, 0.7), 0.3)
            else:   # a bunch of bags on a string
                for k in range(rng.randrange(2, 6)):
                    zz = z - 0.15 - k * rng.between(0.12, 0.2)
                    lump(mb, 'plastic', Matrix.Translation((x + rng.between(-0.1, 0.1), y + rng.between(-0.05, 0.05), zz - 0.25)), rng.between(0.15, 0.28), rng.between(0.12, 0.2), 0.25, hex_rgb(rng.pick(BAG)), 0.2, seg=6, top=0.2)
                parts.bar(mb, 'cloth', (x, y, z), (x, y, z - 0.2), 0.008, (0.05, 0.05, 0.05), 0)
        x += rng.between(0.35, 0.7)


def heap(mb, x, y, r, z0, kinds, rng, tarp_col=None):
    """A heap of goods (a tumble at a stall's foot): items piled in a mound of radius r, a tarp half over it."""
    n = max(3, int(r * r * 12))
    for k in range(n):
        a, q = rng.between(0, math.tau), r * math.sqrt(rng.between(0, 1))
        zz = z0 + (1 - q / r) * 0.35 * rng.between(0.3, 1.0)
        _item(mb, rng.pick(kinds), Matrix.Translation((x + math.cos(a) * q, y + math.sin(a) * q, zz)) @ Matrix.Rotation(rng.between(-1, 1), 4, 'Z'), rng.child('heap', k), 0.9)
    if tarp_col:
        tarp(mb, x - r * 0.8, x + r * 0.6, y - r * 0.5, y + r * 0.7, z0 + 0.7, 0.55, hex_rgb(tarp_col), rng.child('tarp'), side=-1)
