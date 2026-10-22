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
    fold = lambda x, k: 0.06 * math.sin(x * 5.0 + ph[0]) + 0.03 * math.sin(x * 11.0 + ph[1] + k) + 0.04 * max(0.0, math.sin(x * 2.1 + ph[2])) ** 6
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
            mb.face(q if side > 0 else q[::-1], 'woven', col, 0.5)
    for f in (0.22, 0.78):   # rope ties over the top and down the front, pulling the sheet in
        i = round(nx * f)
        pts = [grid[k][i] + Vector((0, 0, 0.012)) for k in range(len(grid) - 1)]
        for a_, b_ in zip(pts, pts[1:]):
            parts.bar(mb, 'cloth', a_, b_, 0.012, hex_rgb('#2a2520'), 0.3)


PRINT = ['#c62828', '#1f6fb8', '#2e9a46', '#e07b20', '#f9a825', '#6a1b9a', '#d81b60']
PRODUCE = {'garri': '#e9dfb8', 'beans': '#a8743f', 'pepper': '#b8321c', 'rice': '#f1ede2', 'corn': '#d9b44a', 'crayfish': '#c46a3a', 'egusi': '#e6d7a0'}
CRATE = ['#2e9a46', '#2e9a46', '#f9a825', '#1f6fb8', '#c62828', '#1f6b3a']
BOTTLE = ['#3b2414', '#2f5d2a', '#3b2414', '#bfc9b8']
WHITE_CARTON = ['#e8e4dc', '#efe9d8']


def _sq(t, e):
    return math.copysign(abs(t) ** e, t)


def pillow(mb, mat, M, a, b, c, col, colf=None, e1=0.45, e2=0.35, nu=24, nv=10, flat=0.8, wear=0.4):
    """A filled sack lying down (or any soft box): a superquadric with half sizes a (x), b (y), c (z), its underside
    pressed flat at -c*flat and stood on z=0. colf(local point) gives a face's colour (a printed band, a stitched end)."""
    grid = []
    for j in range(nv + 1):
        eta = -math.pi / 2 + 1e-3 + (math.pi - 2e-3) * j / nv
        row = []
        for i in range(nu):
            w = -math.pi + math.tau * i / nu
            x = a * _sq(math.cos(eta), e1) * _sq(math.cos(w), e2)
            y = b * _sq(math.cos(eta), e1) * _sq(math.sin(w), e2)
            z = max(c * _sq(math.sin(eta), e1), -c * flat)
            row.append(Vector((x, y, z + c * flat)))
        grid.append(row)
    fix = (lambda q: q[::-1]) if M.to_3x3().determinant() < 0 else (lambda q: q)
    for j in range(nv):
        for i in range(nu):
            k = (i + 1) % nu
            q = [grid[j][i], grid[j][k], grid[j + 1][k], grid[j + 1][i]]
            cc = colf((q[0] + q[1] + q[2] + q[3]) / 4) if colf else col
            mb.face(fix([M @ v for v in q]), mat, cc, wear)
    return c * (1 + flat)


def sack_lying(mb, M, rng, scale=1.0):
    """A woven polypropylene sack of rice, beans or flour lying flat: white or cream, a printed band and brand block
    across its middle, its two ends stitched shut (darker, pinched). Returns its height."""
    a, b, c = 0.42 * scale, 0.27 * scale, rng.between(0.1, 0.14) * scale
    col = hex_rgb(rng.pick(SACK + ['#f1ede4', '#f1ede4']))
    band_c, block = hex_rgb(rng.pick(PRINT)), hex_rgb(rng.pick(PRINT))
    two = rng.chance(0.5)

    def colf(p):
        u = abs(p.x) / a
        if u > 0.9:
            return shade(col, 0.72)   # the stitched end
        if u < 0.26 and p.z > c * 0.9 and abs(p.y) < b * 0.55:
            return block   # the brand block on top
        if 0.3 < u < 0.4 or (two and 0.5 < u < 0.56):
            return band_c   # printed stripes round it
        return col
    h = pillow(mb, 'woven', M, a, b, c, col, colf, e1=0.55, e2=0.5, nu=36, nv=12)
    for sx in (-1, 1):   # the stitched seam, a pinched lip along each end
        mb.box('woven', M @ Matrix.Translation((sx * (a + 0.01), 0, c * 0.8)), shade(col, 0.68), 0.5, size=(0.035, b * 1.7, 0.03))
    return h


def sack_open(mb, M, rng, scale=1.0):
    """A sack standing open on a stall, its top rolled down to show what it holds (garri, beans, pepper, rice...)."""
    w, d, h = rng.between(0.45, 0.6) * scale, rng.between(0.38, 0.5) * scale, rng.between(0.4, 0.6) * scale
    col = hex_rgb(rng.pick(SACK + ['#f1ede4']))
    lump(mb, 'woven', M, w, d, h, col, 0.5, seg=12, top=0.98)
    for k, z in enumerate((h * 0.84, h * 0.93)):   # the rolled rim
        parts.cyl(mb, 'woven', M @ Matrix.Translation((0, 0, z)) @ Matrix.Scale(d / w, 4, Vector((0, 1, 0))), w / 2 * (1.02 - 0.03 * k), 0.07, shade(col, 1.05 - 0.12 * k), 0.4, seg=12, caps=(False, False))
    produce = hex_rgb(PRODUCE[rng.pick(list(PRODUCE))])
    parts.cyl(mb, 'cloth', M @ Matrix.Translation((0, 0, h * 0.9)) @ Matrix.Scale(d / w, 4, Vector((0, 1, 0))), w / 2 * 0.95, 0.07, produce, 0.2, seg=12, r2=w / 2 * 0.35)
    if rng.chance(0.6):   # the measuring tin (a paint tin, a "mudu") on top
        parts.cyl(mb, 'steel', M @ Matrix.Translation((rng.between(-0.08, 0.08), 0, h * 0.9 + 0.05)), 0.07, 0.11, hex_rgb('#b9bcbd'), 0.5, seg=10, caps=(True, False))
    return h + 0.05


def nylon_bag(mb, M, rng, col=None, s=1.0):
    """A filled black, blue or pink nylon bag: a soft body knotted at the top, its two handles standing up."""
    col = col or hex_rgb(rng.pick(BAG))
    w, d, hh = rng.between(0.2, 0.32) * s, rng.between(0.16, 0.24) * s, rng.between(0.2, 0.32) * s
    lump(mb, 'plastic', M, w, d, hh, col, 0.15, seg=8, top=0.3, sag=0.04)
    for sx in (-1, 1):   # the two handles pulled up and knotted together over the bag's mouth
        parts.bar(mb, 'plastic', M @ Vector((sx * w * 0.22, 0, hh * 0.92)), M @ Vector((0, 0, hh + 0.05 * s)), 0.014 * s, shade(col, 0.85), 0)
    parts.cyl(mb, 'plastic', M @ Matrix.Translation((0, 0, hh + 0.04 * s)), 0.018 * s, 0.03 * s, shade(col, 0.8), 0, seg=6)
    return hh


def crate(mb, M, rng, col=None, bottles=True):
    """A plastic bottle crate: open sides of ribs and holes (you see the bottles through them), a hand hole at each end,
    and bottles standing in it with their caps. Returns its height."""
    col = col or hex_rgb(rng.pick(CRATE))
    L, W, H, t = 0.45, 0.31, 0.29, 0.016
    mb.box('plastic', M @ Matrix.Translation((0, 0, 0.012)), shade(col, 0.8), 0.3, size=(L, W, 0.024))
    for sx in (-1, 1):
        for sy in (-1, 1):
            mb.box('plastic', M @ Matrix.Translation((sx * (L / 2 - t / 2), sy * (W / 2 - t / 2), H / 2)), col, 0.3, size=(t * 1.6, t * 1.6, H))
    for z in (0.03, H * 0.55, H - 0.02):   # rails round the four sides
        for sy in (-1, 1):
            mb.box('plastic', M @ Matrix.Translation((0, sy * (W / 2 - t / 2), z)), col, 0.3, size=(L, t, 0.035 if z > 0.1 else 0.05))
        for sx in (-1, 1):
            mb.box('plastic', M @ Matrix.Translation((sx * (L / 2 - t / 2), 0, z)), col, 0.3, size=(t, W, 0.035 if z > 0.1 else 0.05))
    for k in range(1, 7):   # vertical ribs between the rails: the holes are the gaps
        x = -L / 2 + k * L / 7
        for sy in (-1, 1):
            mb.box('plastic', M @ Matrix.Translation((x, sy * (W / 2 - t / 2), H / 2)), col, 0.3, size=(0.014, t, H))
    for k in range(1, 4):
        y = -W / 2 + k * W / 4
        for sx in (-1, 1):
            mb.box('plastic', M @ Matrix.Translation((sx * (L / 2 - t / 2), y, H * 0.3)), col, 0.3, size=(t, 0.014, H * 0.5))
    if bottles:
        bc = hex_rgb(rng.pick(BOTTLE))
        cap = hex_rgb(rng.pick(['#c62828', '#d9b44a', '#e8e4dc', '#1f6fb8']))
        for i in range(4):
            for j in range(3):
                if rng.chance(0.85):
                    B = M @ Matrix.Translation((-L / 2 + (i + 0.5) * L / 4, -W / 2 + (j + 0.5) * W / 3, 0.024))
                    parts.cyl(mb, 'glass', B, 0.032, 0.2, bc, 0, seg=8, caps=(False, False))
                    parts.cyl(mb, 'glass', B @ Matrix.Translation((0, 0, 0.2)), 0.032, 0.07, bc, 0, seg=8, caps=(False, False), r2=0.013)
                    parts.cyl(mb, 'plastic', B @ Matrix.Translation((0, 0, 0.27)), 0.015, 0.012, cap, 0, seg=6)
    return H


def carton(mb, M, rng, s):
    """A cardboard carton: brown or white board, a printed brand block on its faces, packing tape over the top."""
    white = rng.chance(0.4)
    col = shade(hex_rgb(rng.pick(WHITE_CARTON if white else CARTON)), rng.between(0.85, 1.05))
    mb.box('cloth', M @ Matrix.Translation((0, 0, s[2] / 2)), col, 0.5, size=s)
    pc = hex_rgb(rng.pick(PRINT))
    for sy in (-1, 1):   # the print on the two long faces: a block and a stripe under it
        mb.box('plastic', M @ Matrix.Translation((rng.between(-0.05, 0.05), sy * (s[1] / 2 + 0.002), s[2] * 0.6)), pc, 0.3, size=(s[0] * 0.55, 0.003, s[2] * 0.35))
        mb.box('plastic', M @ Matrix.Translation((0, sy * (s[1] / 2 + 0.002), s[2] * 0.2)), shade(pc, 0.7), 0.3, size=(s[0] * 0.9, 0.003, 0.03))
    mb.box('plastic', M @ Matrix.Translation((0, 0, s[2] + 0.001)), hex_rgb('#c8a46a' if not white else '#d8cfb8'), 0.2, size=(s[0] + 0.004, 0.06, 0.003))
    return s[2]


def _item(mb, kind, M, rng, scale=1.0, hard=None):
    """One item standing at M; returns its height. Soft things go to mb (shaded smooth); hard ones (crates, basins,
    jerrycans, cartons) to `hard` when given, so their edges stay crisp."""
    hb = hard or mb
    if kind == 'sacks':
        if rng.chance(0.55):   # a stack of filled sacks lying flat, bricked
            h = 0
            for k in range(rng.randrange(1, 4)):
                h += sack_lying(mb, M @ Matrix.Translation((rng.between(-0.06, 0.06), rng.between(-0.04, 0.04), h)) @ Matrix.Rotation(rng.between(-0.2, 0.2), 4, 'Z'), rng.child('s', k), scale) * 0.92
            return h
        return sack_open(mb, M, rng, scale)
    if kind == 'nylon_bags':
        h = 0
        for k in range(rng.randrange(2, 5)):
            h = max(h, nylon_bag(mb, M @ Matrix.Translation((rng.between(-0.2, 0.2), rng.between(-0.12, 0.12), 0)) @ Matrix.Rotation(rng.between(-1, 1), 4, 'Z'), rng.child('b', k)))
        return h
    if kind == 'crates':
        n = rng.randrange(1, 5)
        c = hex_rgb(rng.pick(CRATE))
        for k in range(n):
            crate(hb, M @ Matrix.Translation((0, 0, k * 0.29)) @ Matrix.Rotation(rng.between(-0.08, 0.08), 4, 'Z'), rng.child('c', k), c if rng.chance(0.7) else None, bottles=(k == n - 1) or rng.chance(0.3))
        return n * 0.29 + 0.07
    if kind == 'plastics':
        c = hex_rgb(rng.pick(PLASTIC))
        pick = rng.between(0, 1)
        if pick < 0.35:   # a stack of basins, rims out
            n = rng.randrange(4, 10)
            for k in range(n):
                cc = c if rng.chance(0.7) else hex_rgb(rng.pick(PLASTIC))
                props.basin(hb, M @ Matrix.Translation((0, 0, k * 0.045)), cc, r=0.3)
                parts.cyl(hb, 'plastic', M @ Matrix.Translation((0, 0, k * 0.045 + 0.13)), 0.315, 0.014, shade(cc, 0.9), 0.3, seg=14, caps=(False, False))
            return n * 0.045 + 0.12
        if pick < 0.65:   # buckets nested in a tower, the top one's handle up
            n = rng.randrange(3, 8)
            for k in range(n):
                parts.cyl(hb, 'plastic', M @ Matrix.Translation((0, 0, k * 0.07)), 0.12, 0.3, c, 0.3, seg=12, caps=(True, False), r2=0.155)
                parts.cyl(hb, 'plastic', M @ Matrix.Translation((0, 0, k * 0.07 + 0.29)), 0.162, 0.02, shade(c, 0.85), 0.3, seg=12, caps=(False, False))
            z = (n - 1) * 0.07 + 0.3
            parts.bar(hb, 'steel', M @ Vector((-0.15, 0, z)), M @ Vector((0, 0, z + 0.12)), 0.008, hex_rgb('#9a9a9a'), 0.2)
            parts.bar(hb, 'steel', M @ Vector((0, 0, z + 0.12)), M @ Vector((0.15, 0, z)), 0.008, hex_rgb('#9a9a9a'), 0.2)
            return z + 0.12
        for k in range(rng.randrange(1, 4)):   # yellow jerrycans, the old cooking-oil cans
            props.jerrycan(hb, M @ Matrix.Translation((rng.between(-0.08, 0.08), k * 0.2 - 0.2, 0)) @ Matrix.Rotation(rng.between(-0.3, 0.3), 4, 'Z'), hex_rgb(rng.pick(['#e8b923', '#e8b923', '#e8b923', '#1f6fb8', '#e8e4dc'])))
        return 0.47
    if kind == 'cloth':   # folded cloth piled up, each fold its own print
        n = rng.randrange(3, 10)
        for k in range(n):
            hb.box('ankara' if rng.chance(0.7) else 'cloth', M @ Matrix.Translation((rng.between(-0.03, 0.03), rng.between(-0.03, 0.03), k * 0.06 + 0.03)) @ Matrix.Rotation(rng.between(-0.15, 0.15), 4, 'Z'),
                   hex_rgb(rng.pick(CLOTH)), 0.3, size=(0.55, 0.4, 0.055))
        return n * 0.06
    if kind == 'cartons':
        h = 0
        for k in range(rng.randrange(1, 4)):
            s = (rng.between(0.35, 0.6), rng.between(0.3, 0.45), rng.between(0.25, 0.45))
            h += carton(hb, M @ Matrix.Translation((0, 0, h)) @ Matrix.Rotation(rng.between(-0.2, 0.2), 4, 'Z'), rng.child('k', k), s)
        return h
    return 0.0


DUST = (0.105, 0.085, 0.065)   # the street's dust (#5b5148 linear-ish), settling on goods left out


def weather(mb, start, tone=1.0, dust=0.0):
    """Darken (tone) and dust (0..1, toward the street's dust colour) every face added to mb since face index `start`:
    goods that sit in the shade and the street's dust all day."""
    if tone == 1.0 and dust == 0.0:
        return
    f = lambda c: tuple((c[i] * (1 - dust) + DUST[i] * dust) * tone for i in range(3)) + tuple(c[3:])
    for k in range(start, len(mb.cols)):
        mb.cols[k] = [f(c) for c in mb.cols[k]]


def band(mb, x0, x1, y_wall, depth, z0, kinds, fill, rng, side=1, tarp_over=False, hard=None):
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
                h = _item(mb, kind, M, rng.child('item', r, round(x, 2)), scale=1.0 if r == 0 else 0.85, hard=hard)
                if r == 0 and kind in ('sacks', 'cartons', 'crates', 'nylon_bags') and rng.chance(fill * 0.6):   # a second layer on the back row
                    _item(mb, kind, M @ Matrix.Translation((rng.between(-0.08, 0.08), 0, h)) @ Matrix.Rotation(rng.between(-0.4, 0.4), 4, 'Z'), rng.child('top', round(x, 2)), 0.9, hard=hard)
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
                    nylon_bag(mb, Matrix.Translation((x + rng.between(-0.1, 0.1), y + rng.between(-0.05, 0.05), zz - 0.3)) @ Matrix.Rotation(rng.between(-1, 1), 4, 'Z'), rng.child('hb', k), s=0.8)
                parts.bar(mb, 'cloth', (x, y, z), (x, y, z - 0.2), 0.008, (0.05, 0.05, 0.05), 0)
        x += rng.between(0.35, 0.7)


def heap(mb, x, y, r, z0, kinds, rng, tarp_col=None, hard=None):
    """A heap of goods (a tumble at a stall's foot): items piled in a mound of radius r, a tarp half over it."""
    n = max(3, int(r * r * 12))
    for k in range(n):
        a, q = rng.between(0, math.tau), r * math.sqrt(rng.between(0, 1))
        zz = z0 + (1 - q / r) * 0.35 * rng.between(0.3, 1.0)
        _item(mb, rng.pick(kinds), Matrix.Translation((x + math.cos(a) * q, y + math.sin(a) * q, zz)) @ Matrix.Rotation(rng.between(-1, 1), 4, 'Z'), rng.child('heap', k), 0.9, hard=hard)
    if tarp_col:
        tarp(mb, x - r * 0.8, x + r * 0.6, y - r * 0.5, y + r * 0.7, z0 + 0.7, 0.55, hex_rgb(tarp_col), rng.child('tarp'), side=-1)
