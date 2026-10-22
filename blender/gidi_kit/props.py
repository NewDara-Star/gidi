"""Small props shared by the Act 1 pieces (docs/KIT-GAPS.md, "New in the v2 layout"): plastic chairs, benches,
water drums, jerrycans, umbrellas, tables, a wheelbarrow, crates, basins, washing lines, loaves in nylon and
hand-painted boards. Each adds faces to a MeshBuilder at a matrix M (x forward, y left, z up). Worn, never new."""
import math

from mathutils import Matrix, Vector

from . import detail, parts
from .core import at, hex_rgb, shade

CHAIR_COLS = {'#f4f1ea': 3, '#c62828': 2, '#1f5fa8': 2, '#2e7d32': 1, '#f9a825': 1}
UMBRELLA_COLS = [('#c62828', '#f4f1ea'), ('#1f5fa8', '#f9a825'), ('#2e7d32', '#f4f1ea'), ('#f9a825', '#c62828'), ('#6a1b9a', '#f9a825')]
WOOD = hex_rgb('#6b4f36')


def chair(mb, M, col, wear=0.3):
    """A monobloc plastic chair, faded and scuffed: seat, back and four legs (facing +x)."""
    mb.box('plastic', at(M, 0, 0, 0.44), col, wear, size=(0.46, 0.46, 0.04))
    mb.box('plastic', at(M, -0.22, 0, 0.7, ry=0.15), col, wear, size=(0.04, 0.46, 0.5))
    for x in (-0.19, 0.19):
        for y in (-0.19, 0.19):
            mb.box('plastic', at(M, x, y, 0.21), shade(col, 0.92), wear, size=(0.05, 0.05, 0.42))
    for y in (-0.21, 0.21):   # armrests
        mb.box('plastic', at(M, -0.02, y, 0.62), col, wear, size=(0.36, 0.04, 0.04))


def bench(mb, M, length, wear=0.6, h=0.45, col=None):
    """A plank bench on two trestles (length along y)."""
    col = col or WOOD
    mb.box('wood', at(M, 0, 0, h), col, wear, size=(0.32, length, 0.05))
    for y in (-length / 2 + 0.25, length / 2 - 0.25):
        for x in (-0.11, 0.11):
            mb.box('wood', at(M, x, y, h / 2), shade(col, 0.85), wear, size=(0.05, 0.05, h))
        mb.box('wood', at(M, 0, y, 0.12), shade(col, 0.85), wear, size=(0.3, 0.04, 0.04))


def table(mb, M, w, d, h=0.78, col=None, wear=0.6, steel=False):
    """A table: a top w (x) by d (y) on four legs; steel legs for a folding table."""
    col = col or shade(WOOD, 1.2)
    mb.box('wood', at(M, 0, 0, h), col, wear, size=(w, d, 0.04))
    for x in (-w / 2 + 0.06, w / 2 - 0.06):
        for y in (-d / 2 + 0.06, d / 2 - 0.06):
            mb.box('steel' if steel else 'wood', at(M, x, y, h / 2), hex_rgb('#5a5e60') if steel else shade(col, 0.8), wear, size=(0.04, 0.04, h))


def drum(mb, M, col=None, r=0.29, h=0.9, wear=0.4):
    """A blue plastic water drum with its lid and two ribs."""
    col = col or hex_rgb('#1f5fa8')
    parts.cyl(mb, 'plastic', M, r, h, col, wear, seg=14)
    for z in (h * 0.33, h * 0.66):
        parts.cyl(mb, 'plastic', at(M, 0, 0, z), r + 0.012, 0.03, shade(col, 0.85), wear, seg=14, caps=(False, False))
    parts.cyl(mb, 'plastic', at(M, 0, 0, h), r * 0.98, 0.04, shade(col, 0.8), wear, seg=14)


def jerrycan(mb, M, col=None, wear=0.5):
    """A 25-litre jerrycan, yellow by habit (the old cooking-oil cans)."""
    col = col or hex_rgb('#e8b923')
    mb.box('plastic', at(M, 0, 0, 0.2), col, wear, size=(0.28, 0.17, 0.4))
    mb.box('plastic', at(M, -0.04, 0, 0.44), col, wear, size=(0.14, 0.04, 0.06))   # the handle
    parts.cyl(mb, 'plastic', at(M, 0.09, 0, 0.4), 0.025, 0.06, shade(col, 0.6), wear, seg=8)


def crate(mb, M, col=None, wear=0.5, h=0.3):
    """A plastic bottle crate: a box with darker slots on the sides."""
    col = col or hex_rgb('#c62828')
    mb.box('plastic', at(M, 0, 0, h / 2), col, wear, size=(0.45, 0.32, h))
    for s in (-1, 1):
        for x in (-0.12, 0.0, 0.12):
            mb.box('plastic', at(M, x, s * 0.162, h * 0.6), shade(col, 0.45), 0, size=(0.07, 0.005, h * 0.4))


def basin(mb, M, col=None, r=0.3, h=0.14, wear=0.4):
    """An enamel or plastic basin (wider at the top)."""
    col = col or hex_rgb('#c9ced2')
    parts.cyl(mb, 'plastic', M, r * 0.75, h, col, wear, seg=14, caps=(True, False), r2=r)


def umbrella(mb, M, r=1.1, h=2.2, cols=None, wear=0.5):
    """A big market umbrella: a pole and a shallow cone of panels in two alternating colours."""
    a_, b_ = (hex_rgb(c) for c in (cols or UMBRELLA_COLS[0]))
    parts.cyl(mb, 'steel', M, 0.025, h + 0.2, hex_rgb('#8a8d8c'), wear, seg=6)
    n = 8
    top = M @ Vector((0, 0, h + 0.25))
    for i in range(n):
        t0, t1 = i / n * math.tau, (i + 1) / n * math.tau
        p0 = M @ Vector((math.cos(t0) * r, math.sin(t0) * r, h - 0.1))
        p1 = M @ Vector((math.cos(t1) * r, math.sin(t1) * r, h - 0.1))
        col = a_ if i % 2 == 0 else b_
        mb.face([p0, p1, top], 'cloth', col, wear)
        mb.face([top, p1, p0], 'cloth', shade(col, 0.7), wear)   # the underside, darker


def wheelbarrow(mb, M, col=None, wear=0.7):
    """A builder's wheelbarrow, the hawker's shop: a steel tray, a wheel at +x, two handles and legs at -x.
    Returns the matrix of the tray's floor, for the load."""
    col = col or hex_rgb('#3f6b8a')
    tray = at(M, 0.05, 0, 0.62)
    mb.box('steel', tray, col, wear, size=(0.9, 0.62, 0.04))
    for s in (-1, 1):   # the flared sides
        mb.box('steel', at(tray, 0, s * 0.33, 0.13, rx=s * 0.35), col, wear, size=(0.9, 0.03, 0.3))
    mb.box('steel', at(tray, 0.47, 0, 0.13, ry=-0.5), col, wear, size=(0.03, 0.62, 0.3))
    mb.box('steel', at(tray, -0.45, 0, 0.13), col, wear, size=(0.03, 0.62, 0.28))
    parts.cyl(mb, 'rubber', at(M, 0.62, 0.05, 0.2, rx=math.pi / 2), 0.2, 0.1, hex_rgb('#1c1c1c'), 0.4, seg=12)
    for s in (-1, 1):
        parts.bar(mb, 'steel', at(M, 0.62, s * 0.06, 0.2).translation, at(M, -0.9, s * 0.28, 0.62).translation, 0.035, hex_rgb('#4a4a4a'), wear)
        parts.bar(mb, 'steel', at(M, -0.35, s * 0.25, 0.55).translation, at(M, -0.4, s * 0.25, 0.0).translation, 0.03, hex_rgb('#4a4a4a'), wear)
    return at(tray, 0, 0, 0.03)


def loaves(mb, M, n, rng, rows=None):
    """Sliced loaves in clear nylon, stacked: golden crust, the bag's printed band and its knot at one end.
    M: the stack's floor (x along the loaves); n loaves in rows of `rows`."""
    rows = rows or 3   # loaves side by side across the stack, two deep, layered
    for i in range(n):
        lay, j = divmod(i, rows * 2)
        x, y, z = ((j % 2) - 0.5) * 0.3, (j // 2 - (rows - 1) / 2) * 0.13, 0.07 + lay * 0.125
        m = at(M, x, y, z, rz=rng.between(-0.06, 0.06))
        crust = shade(hex_rgb('#c8893e'), rng.between(0.85, 1.1))
        mb.box('cloth', at(m, 0, 0, -0.02), shade(crust, 1.15), 0.2, size=(0.28, 0.12, 0.08))
        parts.cyl(mb, 'cloth', at(m, -0.14, 0, 0.02, ry=math.pi / 2), 0.06, 0.28, crust, 0.2, seg=10)   # the domed top
        band = hex_rgb(rng.pick(['#c62828', '#1f5fa8', '#2e7d32', '#f9a825']))
        mb.box('plastic', at(m, 0.05, 0, 0.0), band, 0, size=(0.04, 0.125, 0.125))
        mb.box('plastic', at(m, -0.155, 0, 0.0), hex_rgb('#e8e6df'), 0, size=(0.04, 0.05, 0.05))   # the knot


def washing_line(mb, a, b, z, rng, sag=0.15):
    """A line between two posts with clothes pegged on it (a, b: ground points)."""
    a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0))
    for p in (a, b):
        parts.bar(mb, 'wood', p, p + Vector((0, 0, z + 0.1)), 0.06, WOOD, 0.7)
    L = (b - a).length
    n = 8
    pts = [a.lerp(b, k / n) + Vector((0, 0, z - sag * math.sin(math.pi * k / n))) for k in range(n + 1)]
    for p, q in zip(pts, pts[1:]):
        parts.bar(mb, 'steel', p, q, 0.012, (0.05, 0.05, 0.05), 0)
    d = (b - a).normalized()
    from .people import ANKARA, PLAIN
    t = 0.3
    while t < L - 0.4:
        w = rng.between(0.25, 0.6)
        h = rng.between(0.3, 0.75)
        p = a + d * (t + w / 2)
        zz = z - sag * math.sin(math.pi * (t + w / 2) / L)
        F = Matrix.Translation((p.x, p.y, zz - h / 2)) @ Matrix.Rotation(math.atan2(d.y, d.x), 4, 'Z')
        mb.box('ankara' if rng.chance(0.5) else 'cloth', F, hex_rgb(rng.pick(ANKARA + PLAIN)), 0.3, size=(w, 0.01, h))
        t += w + rng.between(0.15, 1.4)   # gaps: not every peg is full


def board(mb, F, text, w, h, bg, fg, wear=0.6, hand=True, z=0.0):
    """A hand-painted board on a wall frame F (x along, y out): a timber board with painted letters.
    On the web the browser paints the lettering (detail.SIGNS), as for shop signs. The kit's wall frames (core.frame) are
    left-handed; a right-handed one (a vehicle's or a booth's matrix) would mirror the letters, so it's flipped here."""
    if F.to_3x3().determinant() > 0:
        F = F @ Matrix.Scale(-1, 4, (1, 0, 0))
    mb.box('wood' if hand else 'steel', at(F, 0, 0.04, z), bg, wear, size=(w, 0.04, h))
    if detail.web():
        detail.record_text(at(F, 0, 0.065, z), text, h, fg, bg=bg, w=w, h=h, hand=hand)
        return
    lines = text.split('\n')
    parts.text(mb, 'paint', at(F, 0, 0.065, z), text, h * (0.36 if len(lines) > 1 else 0.55), fg, max_w=w * 0.9, wobble=0.04 if hand else None)


def soot(mb, F, w, h, z0=0.3):
    """Smoke-black on a wall above a cooking fire: three overlapping dark patches, darkest low down."""
    for k, (sw, sh, c) in enumerate(((w, h, 0.22), (w * 0.7, h * 0.75, 0.12), (w * 0.4, h * 0.45, 0.06))):
        mb.box('paint', at(F, 0, 0.012 + k * 0.004, z0 + sh / 2), (c, c * 0.95, c * 0.9), 0.9, size=(sw, 0.004, sh))


def coal_fire(mb, M, rng, pot_r=0.32):
    """Three stones and firewood under a big blackened pot (the buka's and the yard kitchen's fire)."""
    for k in range(3):
        t = k / 3 * math.tau
        mb.box('concrete', at(M, math.cos(t) * pot_r * 0.8, math.sin(t) * pot_r * 0.8, 0.1, rz=t), hex_rgb('#5e5a52'), 0.8, size=(0.22, 0.18, 0.2))
    for k in range(4):   # sticks pushed in from one side, charred at the inner end
        t = rng.between(-0.6, 0.6)
        a = M @ Vector((math.cos(t) * 0.9, math.sin(t) * 0.9, 0.04))
        b = M @ Vector((math.cos(t) * 0.1, math.sin(t) * 0.1, 0.08))
        parts.bar(mb, 'wood', a, b, 0.05, hex_rgb('#5b4027'), 0.8)
    mb.box('emit', at(M, 0, 0, 0.05), hex_rgb('#ff6a1a'), 0, size=(0.3, 0.3, 0.04))   # the embers
    parts.cyl(mb, 'steel', at(M, 0, 0, 0.2), pot_r * 0.85, pot_r * 1.1, hex_rgb('#1e1c1a'), 0.9, seg=14, caps=(True, False), r2=pot_r)
    parts.cyl(mb, 'steel', at(M, 0, 0, 0.2 + pot_r * 1.1), pot_r * 0.98, 0.03, hex_rgb('#3a3632'), 0.8, seg=14)   # the lid


def notes_fan(mb, M, rng, n=None):
    """Banknotes folded lengthways and fanned between the fingers (an agbero's or conductor's float).
    M: at the hand; the fan opens upward."""
    n = n or rng.randrange(5, 9)
    for i in range(n):
        a = (i - (n - 1) / 2) * 0.14
        col = hex_rgb(rng.pick(['#5d7a3a', '#7a4f8a', '#b06a3a', '#3f6f7a', '#8a3a3a']))   # Gidi's notes, not anyone's
        mb.box('cloth', at(M, 0, 0, 0.06, rx=a), shade(col, rng.between(0.85, 1.1)), 0.5, size=(0.01, 0.035, 0.15))


def ticket_book(mb, M, col=None):
    """A ticket book: a pad of coloured tickets with a dark card back."""
    mb.box('cloth', M, hex_rgb('#2a2622'), 0.4, size=(0.1, 0.07, 0.012))
    mb.box('cloth', at(M, 0, 0, 0.012), col or hex_rgb('#f2d7a0'), 0.3, size=(0.095, 0.065, 0.012))


def generator(mb, M, col=None, wear=0.6):
    """A small petrol generator ("I better pass my neighbour"): a tube frame round a dark engine, the fuel tank on top in
    the maker's red or yellow, the pull-start and the exhaust's silencer on one side."""
    col = col or hex_rgb('#c62828')
    tube = hex_rgb('#2a2a2a')
    L, W, H = 0.6, 0.45, 0.46
    for sx in (-1, 1):   # the frame: two hoops and the rails between
        for sy in (-1, 1):
            parts.bar(mb, 'steel', M @ Vector((sx * L / 2, sy * W / 2, 0.02)), M @ Vector((sx * L / 2, sy * W / 2, H)), 0.025, tube, wear)
        parts.bar(mb, 'steel', M @ Vector((sx * L / 2, -W / 2, H)), M @ Vector((sx * L / 2, W / 2, H)), 0.025, tube, wear)
        parts.bar(mb, 'steel', M @ Vector((sx * L / 2, -W / 2, 0.02)), M @ Vector((sx * L / 2, W / 2, 0.02)), 0.025, tube, wear)
    for sy in (-1, 1):
        parts.bar(mb, 'steel', M @ Vector((-L / 2, sy * W / 2, 0.02)), M @ Vector((L / 2, sy * W / 2, 0.02)), 0.025, tube, wear)
    mb.box('steel', at(M, -0.05, 0, 0.17), hex_rgb('#3a3a38'), wear, size=(0.32, 0.3, 0.26))   # engine
    mb.box('steel', at(M, 0.17, 0, 0.17), shade(col, 0.9), wear, size=(0.16, 0.34, 0.26))    # alternator housing
    mb.box('carpaint', at(M, 0, 0, H - 0.06), col, wear, size=(0.42, 0.34, 0.14))           # tank
    parts.cyl(mb, 'plastic', at(M, 0.08, 0.08, H + 0.01), 0.04, 0.03, hex_rgb('#1d1d1d'), 0, seg=8)
    parts.cyl(mb, 'steel', at(M, -0.08, -W / 2 + 0.06, 0.24, rx=math.pi / 2), 0.06, 0.2, hex_rgb('#5a5650'), wear, seg=10)   # silencer
    mb.box('plastic', at(M, -0.2, W / 2 - 0.02, 0.2), hex_rgb('#1d1d1d'), 0, size=(0.06, 0.03, 0.04))   # pull-start


def bin_drum(mb, M, litter, col=None):
    """A blue drum cut down for a bin, rubbish heaped over its rim and spilling at its foot. litter: its record, each
    piece (street.litter_piece's record) with at, where it lies from the drum's foot."""
    from . import street
    col = col or hex_rgb('#1f5fa8')
    parts.cyl(mb, 'plastic', M, 0.29, 0.72, col, 0.6, seg=14, caps=(True, False))
    parts.cyl(mb, 'plastic', M, 0.27, 0.72, shade(col, 0.5), 0.6, seg=14, caps=(False, False))
    for lp in litter:
        dx, dy, dz = lp['at']
        street.litter_piece(mb, M.translation.x + dx, M.translation.y + dy, M.translation.z + dz, lp)


def awning(mb, x0, x1, y, z, depth, col, side=1, wear=0.5):
    """A canvas or plastic awning over a door: sloping out from the wall at y (side +1: out toward +y), a valance hanging
    from its front edge, two steel stays."""
    yf = y + side * depth
    zf = z - depth * 0.35
    q = [Vector((x0, y, z)), Vector((x1, y, z)), Vector((x1, yf, zf)), Vector((x0, yf, zf))]
    mb.face(q if side < 0 else q[::-1], 'cloth', col, wear)
    mb.face(q[::-1] if side < 0 else q, 'cloth', shade(col, 0.7), wear)
    n = max(2, int((x1 - x0) / 0.3))
    for k in range(n):   # the scalloped valance
        a_, b_ = x0 + (x1 - x0) * k / n, x0 + (x1 - x0) * (k + 1) / n
        v = [Vector((a_, yf, zf)), Vector((b_, yf, zf)), Vector((b_, yf, zf - 0.18)), Vector(((a_ + b_) / 2, yf, zf - 0.24)), Vector((a_, yf, zf - 0.18))]
        mb.face(v if side > 0 else v[::-1], 'cloth', shade(col, 0.9), wear)
        mb.face(v[::-1] if side > 0 else v, 'cloth', shade(col, 0.6), wear)
    for x in (x0 + 0.1, x1 - 0.1):
        parts.bar(mb, 'steel', (x, y, z - depth * 0.7), (x, yf, zf), 0.015, hex_rgb('#3a3a3a'), wear)
