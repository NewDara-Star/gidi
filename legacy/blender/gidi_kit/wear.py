"""Age on the houses, in the vertex colours and in thin overlays on the walls.

Unreal shows the kit's vertex colour alone (no procedural wear), so everything the weather does to a Lagos wall has to be
painted into the colours or laid on the wall as geometry: red earth splashed up the foot, paint faded unevenly, black
rain-run streaks under the sills and the parapet, rust run down from the burglar bars, cement patches, render broken
away to the sandcrete block, the AC unit's drip. Looked at against the Mushin and Shomolu study and the street refs
(~/gidi-data/research): numbers and colours only.

Every overlay stands a hair off the wall (OFF) and fades into the wall's own colour at its soft edges: the wall's colour
at any point is a smooth function (Weather.wall), so an overlay can match it exactly where it fades out.
"""
import math

from mathutils import Matrix, Vector

from . import detail
from .core import at, hex_rgb

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

    def __init__(self, paint, wear, H, key, ph=None):
        """ph: the paint blotch's six phases (the house's wall_finish.blotch record); the old city's generators give
        none, and they are drafted from the house's key."""
        self.paint, self.wear, self.H = paint, wear, H
        self.top, self.top_k = H, 0.15   # the wall's very top (a parapet's coping) and how much grime runs down from it
        if ph is None:
            from . import draft
            ph = draft.blotch(key)
        self.ph = list(ph)
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
        col_w = col_w or (6.0 if detail.web() else 2.0)
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


DARK = {'grime': GRIME, 'rust': RUST}


def streak(mb, F, wx, u, z_top, length, w, dark, k, y=OFF, taper=0.9):
    """A run of grime (or rust) from z_top down: strongest at the top, gone at the foot, soft at the sides. A wide run
    comes as the few narrower runs its record splits it into (draft.streak_leaves); this draws one of them."""
    z_bot = z_top - length
    wb = w * taper
    wc = lambda q: wx.seen(*(F @ Vector((q[0], 0, q[1]))))
    top_c = lambda uu: mix(wc((uu, z_top)), dark, k)
    if w < 0.08:
        q = [(u - wb / 2, z_bot), (u + wb / 2, z_bot), (u + w / 2, z_top), (u - w / 2, z_top)]
        cols = [wc(q[0]), wc(q[1]), top_c(q[2][0]), top_c(q[3][0])]
        mb.face([_pt(F, a, b, y) for a, b in q], 'paint', cols, wx.wear)
        return
    if detail.web():   # two quads: soft at both sides, darkest down its middle
        q = [(u - wb / 2, z_bot), (u, z_bot), (u, z_top), (u - w / 2, z_top)]
        mb.face([_pt(F, a, b, y) for a, b in q], 'paint', [wc(q[0]), wc(q[1]), top_c(u), wc(q[3])], wx.wear)
        q = [(u, z_bot), (u + wb / 2, z_bot), (u + w / 2, z_top), (u, z_top)]
        mb.face([_pt(F, a, b, y) for a, b in q], 'paint', [wc(q[0]), wc(q[1]), wc(q[2]), top_c(u)], wx.wear)
        return
    tops = [u - w / 2, u - w / 4, u + w / 4, u + w / 2]
    bots = [u - wb / 2, u - wb / 4, u + wb / 4, u + wb / 2]
    for j in range(3):
        q = [(bots[j], z_bot), (bots[j + 1], z_bot), (tops[j + 1], z_top), (tops[j], z_top)]
        cols = [wc(q[0]), wc(q[1]), wc(q[2]) if j == 2 else top_c(q[2][0]), wc(q[3]) if j == 0 else top_c(q[3][0])]
        # the middle of the streak runs further down than its edges: lift the soft sides' feet
        mb.face([_pt(F, a, b, y) for a, b in q], 'paint', cols, wx.wear)


def patch(mb, F, wx, p):
    """A patch of plaster that was redone and never painted: a slightly ragged outline. p: its record (u, z, w, h, col,
    y; r, each of its 11 points' reach, and mix, how far each fades into the wall)."""
    u, z, w, h, col = p['u'], p['z'], p['w'], p['h'], tuple(p['col'])
    n = len(p['r'])
    pts = []
    for i, rr in enumerate(p['r']):
        a = i / n * math.tau
        pts.append((u + math.cos(a) * w / 2 * rr, z + math.sin(a) * h / 2 * rr))
    cols = [mix(col, wx.seen(*(F @ Vector((q[0], 0, q[1])))), m) for q, m in zip(pts, p['mix'])]
    mb.face([_pt(F, a, b, p['y']) for a, b in pts], 'paint', cols, wx.wear)


def bare_block(mb, F, wx, blk):
    """Render broken away down to the block: a ragged hole whose edges follow the blocks (450 x 225 mm, laid half-bond),
    the dark mortar showing in the joints, each block its own shade, a dark rim where the old render stands proud.
    blk: its record (z0, y, and per course from the foot, its ends ul, uh and each block's shade; null: none in it)."""
    ch, bl = 0.225, 0.45
    z0, y = blk['z0'], blk['y']
    for r, co in enumerate(blk['courses']):
        zl, zh = z0 + r * ch, z0 + (r + 1) * ch
        if co is None:
            continue
        ul, uh = co['ul'], co['uh']
        mb.face([_pt(F, ul, zl, y), _pt(F, uh, zl, y), _pt(F, uh, zh, y), _pt(F, ul, zh, y)], 'block', MORTAR, wx.wear)
        x = ul
        for f in co['shades']:
            c = tuple(v * f for v in BLOCK)
            c = mix(c, DIRT, wx.wear * 0.6 * (1 - smooth(0.0, 0.8, zl)))
            a, b = x + 0.008, x + bl - 0.008
            mb.face([_pt(F, a, zl + 0.008, y + 0.006), _pt(F, b, zl + 0.008, y + 0.006), _pt(F, b, zh - 0.008, y + 0.006), _pt(F, a, zh - 0.008, y + 0.006)], 'block', c, wx.wear)
            x += bl
        for e, s_ in ((ul, -1), (uh, 1)):   # the broken render's edge
            mb.face([_pt(F, e, zl, y + 0.008), _pt(F, e + s_ * 0.06, zl, y + 0.008), _pt(F, e + s_ * 0.06, zh, y + 0.008), _pt(F, e, zh, y + 0.008)],
                    'paint', mix(wx.seen(*(F @ Vector((e, 0, zl)))), GRIME, 0.35), wx.wear)


def ac_unit(mb, F, u, z, wear, rng=None):
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
def marks(mb, F, wx, ms):
    """Draw one wall face's weathering from its records: streak (u, z_top, length, w, 'grime' or 'rust', k, y, taper),
    patch, block (render broken to the block) and ac (an AC unit at u, z)."""
    for m in ms:
        if 'streak' in m:
            u, z_top, length, w, dark, k, y, taper = m['streak']
            streak(mb, F, wx, u, z_top, length, w, DARK[dark], k, y, taper)
        elif 'patch' in m:
            patch(mb, F, wx, m['patch'])
        elif 'block' in m:
            bare_block(mb, F, wx, m['block'])
        elif 'ac' in m:
            ac_unit(mb, F, m['ac'][0], m['ac'][1], wx.wear)


def age_face(mb, F, L, z_top, wx, openings, bands, rng, flat_top=False, foot=True, ac=0, few=False):
    """For the old city's generators: weather one wall face from its own dice (draft.age_face drafts the marks: openings
    [(kind, u, z, w, h, barred)], bands [z of the storey bands], z_top the wall's top), then draw them."""
    from . import draft
    marks(mb, F, wx, draft.age_face(L, z_top, wx.wear, wx.paint, openings, bands, rng, flat_top, foot, ac, few))


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
    if rng.chance(0.4) and not detail.web():   # a loose loop of spare cable hung on the hook
        for k in range(8):
            a0, a1 = k / 8 * math.tau, (k + 1) / 8 * math.tau
            bar(mb, 'rubber', top + out * 0.08 + Vector((0, 0, -0.2)) + e * math.cos(a0) * 0.12 + Vector((0, 0, math.sin(a0) * 0.07)),
                top + out * 0.08 + Vector((0, 0, -0.2)) + e * math.cos(a1) * 0.12 + Vector((0, 0, math.sin(a1) * 0.07)), 0.012, black)
