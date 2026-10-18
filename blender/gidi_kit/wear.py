"""Age on the houses, in the vertex colours and in thin overlays on the walls.

Unreal shows the kit's vertex colour alone (no procedural wear), so everything the weather does to a Lagos wall has to be
painted into the colours or laid on the wall as geometry: red earth splashed up the foot, paint faded unevenly, black
rain-run streaks under the sills and the parapet, rust run down from the burglar bars, cement patches, render broken
away to the sandcrete block, the AC unit's drip. Looked at against the Mushin and Shomolu study and the street refs
(~/Real-world/research): numbers and colours only.

Every overlay stands a hair off the wall (OFF) and fades into the wall's own colour at its soft edges: the wall's colour
at any point is a smooth function (Weather.wall), so an overlay can match it exactly where it fades out.
"""
import math

from mathutils import Matrix, Vector

from . import detail
from .core import Rng, at, hex_rgb

DIRT = hex_rgb('#7a5236')     # red earth splashed up from the yard and the gutter
GRIME = hex_rgb('#3b3a33')    # rain-run grime and mould
RUST = hex_rgb('#7e3b17')     # rust run down from steel
CEMENT = hex_rgb('#8c887f')   # a cement patch, never painted
BLOCK = hex_rgb('#6c685f')    # sandcrete block, damp
MORTAR = hex_rgb('#3f3c36')
OFF = 0.006


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def smooth(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


class Weather:
    """A house's weathering: the colour of its wall at any point, and the dice for its overlays."""

    def __init__(self, paint, wear, H, key):
        self.paint, self.wear, self.H = paint, wear, H
        self.top, self.top_k = H, 0.15   # the wall's very top (a parapet's coping) and how much grime runs down from it
        self.rng = Rng('wear', *key)
        r = self.rng.child('blotch')
        self.ph = [r.between(0, math.tau) for _ in range(6)]
        self.cells = []   # every wall strip drawn (a, b, columns, rows), so overlays can match the wall's colour exactly

    def wall(self, x, y, z):
        """The paint at a point: darker toward the foot (as before), faded in broad blotches, red earth splashed up the foot."""
        p, w = self.paint, self.wear
        c = mix(tuple(v * 0.82 for v in p), p, z / self.H if self.H else 1)
        ph = self.ph
        n = math.sin(x * 0.55 + y * 0.31 + ph[0]) * math.sin(z * 0.8 + ph[1]) + 0.6 * math.sin(x * 0.8 - y * 0.7 + z * 0.4 + ph[2])
        c = tuple(v * (1 + 0.15 * w * n) for v in c)
        c = mix(c, (0.40, 0.38, 0.34), 0.3 * w * smooth(-0.4, 1.4, n))   # faded and dirty in broad patches
        c = mix(c, GRIME, self.top_k * w * smooth(self.top - 1.8, self.top - 0.1, z))   # grime run down from the top
        return mix(c, DIRT, w * 0.85 * (1 - smooth(0.35, 1.6, z)))

    def prism(self, mb, mat, poly, z0, z1, rows=None, col_w=None):
        """Walls around a counter-clockwise polygon, cut into columns and bands so the colour can change along and up them."""
        col_w = col_w or (4.0 if detail.web() else 2.0)
        zs = sorted({z0, z1, *[z for z in (rows or ()) if z0 < z < z1]})
        n = len(poly)
        for i in range(n):
            a, b = poly[i], poly[(i + 1) % n]
            L = math.dist(a, b)
            k = max(1, round(L / col_w))
            self.cells.append((a, b, k, zs))
            for j in range(k):
                p0 = (a[0] + (b[0] - a[0]) * j / k, a[1] + (b[1] - a[1]) * j / k)
                p1 = (a[0] + (b[0] - a[0]) * (j + 1) / k, a[1] + (b[1] - a[1]) * (j + 1) / k)
                for zl, zh in zip(zs, zs[1:]):
                    pts = [(p0[0], p0[1], zl), (p1[0], p1[1], zl), (p1[0], p1[1], zh), (p0[0], p0[1], zh)]
                    mb.face(pts, mat, [self.wall(*q) for q in pts], self.wear)

    def seen(self, x, y, z):
        """The wall's colour at a point as the mesh shows it: the corner colours of the strip it falls in, blended the way
        the faces blend them. An overlay that fades into this has no edge."""
        best = None
        for a, b, k, zs in self.cells:
            if not zs[0] - 1e-6 <= z <= zs[-1] + 1e-6:
                continue
            dx, dy = b[0] - a[0], b[1] - a[1]
            l2 = dx * dx + dy * dy or 1
            t = max(0.0, min(1.0, ((x - a[0]) * dx + (y - a[1]) * dy) / l2))
            d = math.hypot(x - a[0] - t * dx, y - a[1] - t * dy)
            if best is None or d < best[0]:
                best = (d, a, b, k, zs, t)
        if best is None:
            return self.wall(x, y, z)
        _, a, b, k, zs, t = best
        j = min(k - 1, int(t * k))
        r = max(i for i in range(len(zs) - 1) if zs[i] <= z + 1e-9) if z > zs[0] else 0
        r = min(r, len(zs) - 2)
        z0, z1 = zs[r], zs[r + 1]
        p0 = (a[0] + (b[0] - a[0]) * j / k, a[1] + (b[1] - a[1]) * j / k)
        p1 = (a[0] + (b[0] - a[0]) * (j + 1) / k, a[1] + (b[1] - a[1]) * (j + 1) / k)
        fu, fz = t * k - j, (z - z0) / (z1 - z0) if z1 > z0 else 0.0
        lo = mix(self.wall(p0[0], p0[1], z0), self.wall(p1[0], p1[1], z0), fu)
        hi = mix(self.wall(p0[0], p0[1], z1), self.wall(p1[0], p1[1], z1), fu)
        return mix(lo, hi, fz)

    def foot(self, col, z):
        """A plinth's colour at height z: the same red splash."""
        return mix(col, DIRT, self.wear * 0.9 * (1 - smooth(0.0, 0.7, z)))


# ---------------------------------------------------------------- overlays on one wall face (F: x along, y out, z up)
def _pt(F, u, z, y=OFF):
    return F @ Vector((u, y, z))


def streak(mb, F, wx, u, z_top, length, w, dark, k, y=OFF, taper=0.9):
    """A run of grime (or rust) from z_top down: strongest at the top, gone at the foot, soft at the sides."""
    if w > 0.35 and length > 0.4:   # a wide run is never even: a few narrower runs, each its own length and strength
        r = Rng('streak', round(u, 2), round(z_top, 2), round(length, 2))
        n = 2 + int(w / 0.6)
        for j in range(n):
            ww = w / n * r.between(0.6, 1.7)
            uu = u - w / 2 + (j + 0.5) * w / n + r.between(-0.3, 0.3) * w / n
            streak(mb, F, wx, uu, z_top, length * r.between(0.45, 1.05), ww, dark, k * r.between(0.65, 1.0), y + j * 0.0005, taper)
        return
    z_bot = z_top - length
    wb = w * taper
    wc = lambda q: wx.seen(*(F @ Vector((q[0], 0, q[1]))))
    top_c = lambda uu: mix(wc((uu, z_top)), dark, k)
    if w < 0.08:
        q = [(u - wb / 2, z_bot), (u + wb / 2, z_bot), (u + w / 2, z_top), (u - w / 2, z_top)]
        cols = [wc(q[0]), wc(q[1]), top_c(q[2][0]), top_c(q[3][0])]
        mb.face([_pt(F, a, b, y) for a, b in q], 'paint', cols, wx.wear)
        return
    tops = [u - w / 2, u - w / 4, u + w / 4, u + w / 2]
    bots = [u - wb / 2, u - wb / 4, u + wb / 4, u + wb / 2]
    for j in range(3):
        q = [(bots[j], z_bot), (bots[j + 1], z_bot), (tops[j + 1], z_top), (tops[j], z_top)]
        cols = [wc(q[0]), wc(q[1]), wc(q[2]) if j == 2 else top_c(q[2][0]), wc(q[3]) if j == 0 else top_c(q[3][0])]
        # the middle of the streak runs further down than its edges: lift the soft sides' feet
        mb.face([_pt(F, a, b, y) for a, b in q], 'paint', cols, wx.wear)


def patch(mb, F, wx, u, z, w, h, col, rng, y=OFF):
    """A patch of plaster that was redone and never painted: a slightly ragged outline."""
    n = 11
    pts = []
    for i in range(n):
        a = i / n * math.tau
        rr = rng.between(0.7, 1.0)
        pts.append((u + math.cos(a) * w / 2 * rr, z + math.sin(a) * h / 2 * rr))
    cols = [mix(col, wx.seen(*(F @ Vector((p[0], 0, p[1])))), rng.between(0.0, 0.3)) for p in pts]
    mb.face([_pt(F, a, b, y) for a, b in pts], 'paint', cols, wx.wear)


def bare_block(mb, F, wx, u, z0, w, courses, rng, y=0.05):
    """Render broken away down to the block: a ragged hole whose edges follow the blocks (450 x 225 mm, laid half-bond),
    the dark mortar showing in the joints, each block its own shade, a dark rim where the old render stands proud."""
    ch, bl = 0.225, 0.45
    for r in range(courses):
        zl, zh = z0 + r * ch, z0 + (r + 1) * ch
        t = (r + 0.5) / courses * 2 - 1   # a ragged blob, widest across its middle
        hw = w / 2 * math.sqrt(max(0.0, 1 - t * t)) ** 0.6
        sh = bl / 2 if r % 2 else 0.0      # half-bond: every other course shifted half a block
        ul = math.floor((u - hw * rng.between(0.7, 1.05) - sh) / bl) * bl + sh
        uh = math.ceil((u + hw * rng.between(0.7, 1.05) - sh) / bl) * bl + sh
        if uh - ul < bl - 1e-6:
            continue
        mb.face([_pt(F, ul, zl, y), _pt(F, uh, zl, y), _pt(F, uh, zh, y), _pt(F, ul, zh, y)], 'block', MORTAR, wx.wear)
        x = ul
        while x < uh - 1e-6:
            f = rng.between(0.85, 1.12)
            c = tuple(v * f for v in BLOCK)
            c = mix(c, DIRT, wx.wear * 0.6 * (1 - smooth(0.0, 0.8, zl)))
            a, b = x + 0.008, x + bl - 0.008
            mb.face([_pt(F, a, zl + 0.008, y + 0.006), _pt(F, b, zl + 0.008, y + 0.006), _pt(F, b, zh - 0.008, y + 0.006), _pt(F, a, zh - 0.008, y + 0.006)], 'block', c, wx.wear)
            x += bl
        for e, s_ in ((ul, -1), (uh, 1)):   # the broken render's edge
            mb.face([_pt(F, e, zl, y + 0.008), _pt(F, e + s_ * 0.06, zl, y + 0.008), _pt(F, e + s_ * 0.06, zh, y + 0.008), _pt(F, e, zh, y + 0.008)],
                    'paint', mix(wx.seen(*(F @ Vector((e, 0, zl)))), GRIME, 0.35), wx.wear)


def ac_unit(mb, F, u, z, wear, rng):
    """A split AC's outdoor unit on two brackets, its pipes into the wall: off-white gone yellow-grey, the fan behind a dark grille."""
    from .parts import bar, cyl
    body = mix((0.80, 0.79, 0.74), (0.55, 0.50, 0.40), wear * 0.5)
    w, d, h = 0.82, 0.3, 0.56
    y0 = 0.08
    mb.box('plastic', at(F, u, y0 + d / 2, z + h / 2), body, wear, size=(w, d, h))
    mb.face([_pt(F, u - w / 2 + 0.06, z + 0.06, y0 + d + 0.003), _pt(F, u + 0.1, z + 0.06, y0 + d + 0.003),
             _pt(F, u + 0.1, z + h - 0.06, y0 + d + 0.003), _pt(F, u - w / 2 + 0.06, z + h - 0.06, y0 + d + 0.003)], 'plastic', (0.05, 0.05, 0.05), 0)
    for s in (-1, 1):   # the brackets
        bar(mb, 'steel', _pt(F, u + s * 0.3, z - 0.02, 0.0), _pt(F, u + s * 0.3, z - 0.02, y0 + d), 0.035, (0.25, 0.22, 0.2), wear)
        bar(mb, 'steel', _pt(F, u + s * 0.3, z - 0.3, 0.0), _pt(F, u + s * 0.3, z - 0.02, y0 + d - 0.05), 0.03, (0.25, 0.22, 0.2), wear)
    if not detail.web():   # the insulated pipes, out of the side and into the wall
        bar(mb, 'plastic', _pt(F, u + w / 2 + 0.03, z + 0.15, 0.2), _pt(F, u + w / 2 + 0.12, z + 0.15, 0.03), 0.04, (0.85, 0.85, 0.82), wear)
        bar(mb, 'plastic', _pt(F, u + w / 2 + 0.12, z + 0.15, 0.03), _pt(F, u + w / 2 + 0.12, z + h + 0.2, 0.03), 0.04, (0.85, 0.85, 0.82), wear)


def lnb_arm(mb, x, y, z, rz):
    """The dish's arm and LNB (the dish itself is parts.satellite_dish): what makes it read as a dish from the street."""
    from .parts import bar
    m = Matrix.Translation((x, y, z)) @ Matrix.Rotation(rz, 4, 'Z')
    a = m @ Vector((0, -0.09, 0.4))     # from the dish's lower rim (the dish faces local -y, tipped up)
    b = m @ Vector((0, -0.46, 0.95))    # out to its focus
    bar(mb, 'steel', a, b, 0.025, (0.6, 0.6, 0.6))
    mb.box('plastic', at(m, 0, -0.46, 0.95), (0.2, 0.2, 0.22), 0, size=(0.07, 0.12, 0.07))


# ---------------------------------------------------------------- one house's walls
def age_face(mb, F, L, z_top, wx, openings, bands, rng, flat_top=False, foot=True, ac=0):
    """Weather one wall face: openings [(kind, u, z, w, h, barred)], bands [z of the storey bands], z_top the wall's top
    (the parapet's top on a flat roof). Strength follows the house's wear."""
    w_ = wx.wear
    half = L / 2 - 0.25
    if half < 0.4:
        return
    below = lambda z: max([b + 0.1 for b in bands if b + 0.1 < z - 0.05] + [0.47])   # a streak stops at the band under it
    taken = [(o[1] - o[3] / 2 - 0.15, o[1] + o[3] / 2 + 0.15, o[2] - o[4] / 2 - 0.2, o[2] + o[4] / 2 + 0.25) for o in openings]
    free = lambda u0, u1, z0, z1: u0 >= -half - 1e-6 and u1 <= half + 1e-6 and not any(u0 < b and u1 > a and z0 < d and z1 > c for a, b, c, d in taken)

    for kind, u, z, w, h, barred in openings:
        if kind != 'window':
            continue
        sill = z - h / 2 - 0.16
        if rng.chance(0.35 + 0.6 * w_):   # grime from the sill: across it, or from its two ends
            ln = min(sill - below(sill), rng.between(0.7, 2.0) * (0.6 + w_))
            if ln > 0.2:
                if rng.chance(0.5):
                    streak(mb, F, wx, u, sill, ln, w + 0.35, GRIME, min(0.9, rng.between(0.55, 0.85) * (0.5 + w_)), taper=0.8)
                else:
                    for s in (-1, 1):
                        streak(mb, F, wx, u + s * (w / 2 + 0.1), sill, ln, rng.between(0.2, 0.4), GRIME, min(0.9, rng.between(0.6, 0.9) * (0.5 + w_)))
        if barred and rng.chance(0.25 + 0.7 * w_):   # rust run down from the bars' feet
            for k in range(rng.randrange(2, 5)):
                uu = u + rng.between(-w / 2, w / 2)
                ln = min(sill - below(sill), rng.between(0.25, 0.9))
                if ln > 0.1:
                    streak(mb, F, wx, uu, sill - 0.01, ln, rng.between(0.03, 0.07), RUST, rng.between(0.45, 0.8), y=OFF + 0.002, taper=0.5)
        if not detail.web() and rng.chance(0.3 * w_):   # rain run off the lintel's ends
            for s in (-1, 1):
                streak(mb, F, wx, u + s * (w / 2 + 0.05), z + h / 2 + 0.12, rng.between(0.3, 0.7), 0.12, GRIME, 0.3 * (0.5 + w_))

    # off the ledges: under a balcony's slab, and from the storey bands
    for kind, u, z, w, h, barred in openings:
        if kind == 'balcony' and rng.chance(0.4 + 0.6 * w_):
            zb = z - h / 2 - 0.13
            for k in range(rng.randrange(2, 5)):
                uu = u + rng.between(-w / 2, w / 2)
                streak(mb, F, wx, uu, zb, min(zb - below(zb), rng.between(0.6, 2.0)), rng.between(0.2, 0.7), GRIME, min(0.9, rng.between(0.5, 0.85) * (0.5 + w_)), taper=0.8)
    for b in bands:
        for k in range(int(rng.between(0, 3) * w_ * L / 8)):
            uu, zb = rng.between(-half, half), b - 0.11
            if free(uu - 0.2, uu + 0.2, zb - 0.5, zb):
                streak(mb, F, wx, uu, zb, min(zb - below(zb), rng.between(0.4, 1.6)), rng.between(0.15, 0.5), GRIME, min(0.85, rng.between(0.4, 0.75) * (0.5 + w_)), taper=0.8)

    # down from the top: a band of mould under a flat roof's coping, and streaks from it (fewer under a roof's overhang)
    if flat_top and rng.chance(0.3 + 0.7 * w_):
        streak(mb, F, wx, 0, z_top - 0.13, rng.between(0.3, 0.8), 2 * half + 0.4, GRIME, min(0.8, rng.between(0.4, 0.65) * (0.4 + w_)), y=OFF - 0.003, taper=1.0)
    n_top = int(L / 2.5 * (0.4 + w_) * (1.6 if flat_top else 0.6) * rng.between(0.6, 1.3))
    for k in range(n_top):
        uu = rng.between(-half, half)
        ln = rng.between(0.6, 2.8 if flat_top else 1.4) * (0.5 + w_)
        streak(mb, F, wx, uu, z_top - 0.13, ln, rng.between(0.2, 0.9), GRIME, min(0.95, rng.between(0.5, 0.9) * (0.4 + w_)), taper=rng.between(0.6, 1.0))

    # patches of new cement, and render broken off to the block
    for k in range(int(rng.between(0, 2.5) * w_ * L / 6 + 0.5)):
        pw, ph = rng.between(0.35, 1.4), rng.between(0.3, 1.0)
        uu, zz = rng.between(-half + pw / 2, half - pw / 2), rng.between(0.7, z_top - 0.6)
        if free(uu - pw / 2, uu + pw / 2, zz - ph / 2, zz + ph / 2):
            pc = CEMENT if rng.chance(0.6) else mix(tuple(v * rng.between(1.03, 1.1) for v in wx.paint), CEMENT, 0.25)   # bare cement, or a touch-up in new paint
            patch(mb, F, wx, uu, zz, pw, ph, pc, rng, y=OFF - 0.004)
    if foot and rng.chance(0.1 + 0.6 * w_):   # at the foot, where the splash and the damp eat it first
        bw, z0, nc = rng.between(0.9, 2.2), rng.between(0.0, 0.3), rng.randrange(2, 6)
        uu = rng.pick([-half + bw / 2, half - bw / 2, rng.between(-half + bw / 2, half - bw / 2)]) if half > bw / 2 else 0
        if half > bw / 2 and free(uu - bw / 2 - 0.25, uu + bw / 2 + 0.25, z0, z0 + nc * 0.225):
            bare_block(mb, F, wx, uu, z0, bw, nc, rng.child('block'))
    if rng.chance(0.25 * w_):   # and now and then higher up, where a pipe or a sign came off
        bw, nc = rng.between(0.9, 1.6), rng.randrange(2, 5)
        uu, zz = rng.between(-half + bw / 2, half - bw / 2), rng.between(1.2, max(1.3, z_top - 1.4))
        if half > bw / 2 and free(uu - bw / 2 - 0.25, uu + bw / 2 + 0.25, zz, zz + nc * 0.225):
            bare_block(mb, F, wx, uu, zz, bw, nc, rng.child('block2'), y=OFF + 0.002)

    # AC units on the upper floors (and the shop's), each with its drip stain
    for k in range(ac):
        for _ in range(6):
            uu = rng.between(-half + 0.5, half - 0.5)
            zz = rng.pick([b for b in bands] or [0.0]) + rng.between(1.0, 1.6)
            if free(uu - 0.5, uu + 0.5, zz - 0.35, zz + 0.6):
                ac_unit(mb, F, uu, zz, w_, rng)
                streak(mb, F, wx, uu - 0.2, zz - 0.02, min(zz - below(zz), rng.between(0.8, 2.2)), 0.18, GRIME, 0.55, taper=0.4)
                taken.append((uu - 0.55, uu + 0.55, zz - 0.4, zz + 0.65))
                break


def meter_drop(mb, corner, nxt, centre, z, rng):
    """Where a service drop from the data's pole lands on a house: an insulator hook at the corner, the cable run down the wall
    to the prepaid meter box by the door height, a second cable off it into the wall (and now and then a loose loop)."""
    from .parts import bar
    c, n_, m = Vector((corner[0], corner[1], 0)), Vector((nxt[0], nxt[1], 0)), Vector((centre[0], centre[1], 0))
    e = (n_ - c).normalized()                       # along the wall
    out = Vector((e.y, -e.x, 0))
    if out.dot(c - m) < 0:
        out = -out
    p = c + (m - c).normalized() * 0.12 + out * 0.03   # just inside the chamfered corner
    black = (0.02, 0.02, 0.02)
    top, low = Vector((p.x, p.y, z)), Vector((p.x, p.y, 1.95))
    mb.box('steel', at(Matrix.Translation(tuple(top)), 0, 0, 0), (0.3, 0.3, 0.3), 0.5, size=(0.06, 0.06, 0.12))   # the hook
    bar(mb, 'rubber', top, low, 0.014, black)
    box = c + e * rng.between(0.5, 0.9) + out * 0.1
    bar(mb, 'rubber', low, Vector((box.x, box.y, 1.95)), 0.014, black)
    rz = math.atan2(e.y, e.x)
    mb.box('plastic', Matrix.Translation((box.x, box.y, 1.65)) @ Matrix.Rotation(rz, 4, 'Z'), mix((0.78, 0.77, 0.72), DIRT, rng.between(0.1, 0.4)), 0.5, size=(0.26, 0.12, 0.36))
    mb.box('glass', Matrix.Translation((box.x + out.x * 0.062, box.y + out.y * 0.062, 1.7)) @ Matrix.Rotation(rz, 4, 'Z'), (0.15, 0.2, 0.18), 0, size=(0.1, 0.01, 0.06))
    q = box + e * rng.between(0.3, 1.2)                # on into the house
    bar(mb, 'rubber', Vector((box.x, box.y, 1.47)), Vector((box.x, box.y, 1.3)), 0.012, black)
    bar(mb, 'rubber', Vector((box.x, box.y, 1.3)), Vector((q.x - out.x * 0.07, q.y - out.y * 0.07, 1.3)), 0.012, black)
    if rng.chance(0.4):   # a loose loop of spare cable hung on the hook
        for k in range(8):
            a0, a1 = k / 8 * math.tau, (k + 1) / 8 * math.tau
            bar(mb, 'rubber', top + out * 0.08 + Vector((0, 0, -0.2)) + e * math.cos(a0) * 0.12 + Vector((0, 0, math.sin(a0) * 0.07)),
                top + out * 0.08 + Vector((0, 0, -0.2)) + e * math.cos(a1) * 0.12 + Vector((0, 0, math.sin(a1) * 0.07)), 0.012, black)
