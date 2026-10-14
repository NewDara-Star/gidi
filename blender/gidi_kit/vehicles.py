"""Vehicles of Lagos roads, from docs/look/research-vehicles.md (sizes [src] where it had them).
Every builder adds faces to a MeshBuilder at matrix M (x forward, y left, z up, origin on the
ground under the middle). Condition ('new', 'worn', 'battered', 'wreck') drives wear, mismatched
panels, missing doors and wheels. Liveries, slogans and plates are invented (rule zero)."""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import hex_rgb, shade

YELLOW = {'new': '#f2c200', 'worn': '#e0b43a', 'battered': '#d6b867', 'wreck': '#9c7a3a'}
WEAR = {'new': 0.05, 'worn': 0.4, 'battered': 0.75, 'wreck': 1.0}
SLOGANS = ['STILL STANDING BY GRACE', 'PATIENCE PAYS THE FARE', 'NO SHAKING, NA STEADY WHEEL', "MAMA'S PRAYER NA MY AIRBAG", 'WHO KNOWS TOMORROW?',
           'SLOW ROAD, SURE ARRIVAL', 'ENVY ME IN SILENCE', 'GIDI NO DEY SLEEP', 'IRON SHARPENS IRON', 'SMALL SMALL, BIG BIG', 'DESTINY HAS NO HOLIDAY',
           'THANK YOU LORD, NEXT STOP', 'HUSTLE IS NOT A CRIME', 'PEACE BE UPON THIS BUS']


def condition(wealth, rng, commercial=False, parked=False):
    """research-vehicles 8.7: condition = 0.25 + 0.6 wealth +- 0.2; commercial -0.2."""
    c = 0.25 + 0.6 * wealth + rng.between(-0.2, 0.2) - (0.2 if commercial else 0)
    if c > 0.8:
        return 'new'
    if c > 0.5:
        return 'worn'
    if c > 0.2 or not parked:
        return 'battered'
    return 'wreck'


def L(M, x, y, z, rz=0.0, rx=0.0, ry=0.0):
    return M @ Matrix.Translation((x, y, z)) @ Matrix.Rotation(rz, 4, 'Z') @ Matrix.Rotation(rx, 4, 'X') @ Matrix.Rotation(ry, 4, 'Y')


def _rounded_profile(pts, r):
    """A closed polygon in (x, z) with each corner cut into a small round."""
    out = []
    n = len(pts)
    for i in range(n):
        p, a, b = Vector(pts[i]), Vector(pts[i - 1]), Vector(pts[(i + 1) % n])
        da, db = (a - p), (b - p)
        ra, rb = min(r, da.length * 0.45), min(r, db.length * 0.45)
        pa, pb = p + da.normalized() * ra, p + db.normalized() * rb
        for k in range(4):
            t = k / 3
            out.append(((1 - t) ** 2 * pa + 2 * (1 - t) * t * p + t * t * pb))
    return out


def body(mb, M, profile, width, mat, col, wear, r=0.12):
    """Extrude a side profile [(x, z)...] across the width, with rounded corners and edges."""
    prof = _rounded_profile(profile, r)
    hw = width / 2
    inset = min(0.06, r * 0.5)
    cx = sum(p.x for p in prof) / len(prof)
    cz = sum(p.y for p in prof) / len(prof)
    shrink = lambda p: Vector((cx + (p.x - cx) * (1 - inset / 2.0), 0, cz + (p.y - cz) * (1 - inset / 1.2)))
    # the full profile sits just inside the sides; the flat sides (shrunk profile) are at +-hw,
    # with a chamfer band between, so decals at hw + a few mm always show
    left = [M @ Vector((p.x, hw - inset, p.y)) for p in prof]
    right = [M @ Vector((p.x, -hw + inset, p.y)) for p in prof]
    li = [M @ Vector((shrink(p).x, hw, shrink(p).z)) for p in prof]
    ri = [M @ Vector((shrink(p).x, -hw, shrink(p).z)) for p in prof]
    n = len(prof)
    for i in range(n):
        j = (i + 1) % n
        mb.face([right[i], right[j], left[j], left[i]], mat, col, wear)
        mb.face([left[i], left[j], li[j], li[i]], mat, col, wear)
        mb.face([right[j], right[i], ri[i], ri[j]], mat, col, wear)
    mb.face(li, mat, col, wear)
    mb.face(list(reversed(ri)), mat, col, wear)


def wheel(mb, M, x, y, r, w, cond, rim='steel'):
    s = 1 if y > 0 else -1
    if cond == 'wreck':  # on blocks
        mb.box('concrete', L(M, x, y, 0.15), hex_rgb('#8a857a'), 0.8, size=(0.4, 0.2, 0.3))
        return
    tyre = hex_rgb('#1c1c1c' if cond in ('new', 'worn') else '#2e2d2b')
    parts.cyl(mb, 'rubber', L(M, x, y - s * w / 2, r, rx=-math.pi / 2), r, w, tyre, 0, seg=18)
    rim_c = hex_rgb({'steel': '#2a2a2a', 'alloy': '#c9ced2', 'chrome': '#e8ecef'}[rim])
    if cond == 'battered':
        rim_c = hex_rgb('#6b3a22')
    parts.cyl(mb, 'steel', L(M, x, y + s * 0.005, r, rx=-math.pi / 2 if s > 0 else math.pi / 2), r * 0.6, 0.02, rim_c, 0.3, seg=14)
    for k in range(5 if rim == 'alloy' else 0):
        a = k / 5 * math.tau
        mb.box('steel', L(M, x + math.cos(a) * r * 0.3, y + s * 0.03, r + math.sin(a) * r * 0.3, ry=-a), rim_c, 0.2, size=(r * 0.5, 0.02, 0.05))


def lamp(mb, M, x, y, z, w, h, kind='head'):
    col = {'head': '#fff4d6', 'tail': '#d02020', 'amber': '#ff9a1e'}[kind]
    mb.box('emit' if kind == 'head' else 'emit', L(M, x, y, z), hex_rgb(col), 0, size=(0.03, w, h))


def plate(mb, M, x, z, rng, back=False):
    mb.box('plastic', L(M, x, 0, z), hex_rgb('#f2f2ee'), 0.2, size=(0.02, 0.36, 0.11))
    mb.box('plastic', L(M, x + (-0.012 if back else 0.012), 0, z + 0.035), hex_rgb('#2a6a3a'), 0, size=(0.005, 0.3, 0.02))


def glass_panel(mb, M, pts, col=hex_rgb('#1c2830')):
    mb.face([M @ Vector(p) for p in pts], 'glass', col, 0)


def side_text(mb, M, x, y, z, s, size, col, facing=1):
    m = L(M, x, y, z, rz=0 if facing > 0 else math.pi)
    parts.text(mb, 'paint', m, s, size, col, max_w=None)


# ---------------------------------------------------------------- danfo, korope, buses
def danfo(mb, M, rng, cond='worn', variant=None, load=True):
    """The yellow 14-18 seat minibus: a boxy rear-engined van (4.57 x 1.84 x 1.95 m, wheelbase 2.46),
    two black stripes, the kerb-side sliding door open or missing, a roof rack, slogans."""
    Lh, W, H = 2.285, 1.84, 1.95
    wear = WEAR[cond]
    col = hex_rgb(YELLOW[cond])
    prof = [(-Lh, 0.32), (Lh - 0.05, 0.32), (Lh, 0.42), (Lh, 0.98), (Lh - 0.16, 1.05), (Lh - 0.42, H - 0.04), (Lh - 0.6, H), (-Lh + 0.05, H), (-Lh, H - 0.12)]
    body(mb, M, prof, W, 'carpaint', col, wear, r=0.14)
    # mismatched panel on battered buses
    if cond in ('battered', 'wreck') and rng.chance(0.5):
        x0 = rng.between(-1.6, 0.6)
        mb.box('carpaint', L(M, x0, W / 2 + 0.006, 0.75), hex_rgb(rng.pick(['#8a8d8c', '#c9c1ae', '#3e6b3a', '#f5b800'])), wear, size=(0.9, 0.01, 0.75))
    # glazing: windscreen, the side band of three panes each side, rear window
    glass = hex_rgb('#1c2830' if cond != 'wreck' else '#050505')
    glass_panel(mb, M, [(Lh - 0.2, -W / 2 + 0.12, 1.08), (Lh - 0.2, W / 2 - 0.12, 1.08), (Lh - 0.52, W / 2 - 0.12, 1.84), (Lh - 0.52, -W / 2 + 0.12, 1.84)], glass)
    for s in (-1, 1):
        y = s * (W / 2 + 0.008)
        for k, (x0, x1) in enumerate(((1.45, 1.9), (0.35, 1.3), (-0.75, 0.2), (-1.95, -0.9))):
            pts = [(x0, y, 1.08), (x1, y, 1.08), (x1, y, 1.68), (x0, y, 1.68)]
            glass_panel(mb, M, pts if s > 0 else list(reversed(pts)), glass)
        for z, h in ((0.95, 0.1), (0.45, 0.08)):  # the two black stripes
            mb.box('carpaint', L(M, -0.05, s * (W / 2 + 0.004), z), hex_rgb('#141414'), wear, size=(4.3, 0.01, h))
        mb.box('carpaint', L(M, -0.1, s * (W / 2 + 0.005), 1.38), hex_rgb('#141414'), wear, size=(4.1, 0.008, 0.66))  # black window band
    glass_panel(mb, M, [(-Lh - 0.008, W / 2 - 0.15, 1.1), (-Lh - 0.008, -W / 2 + 0.15, 1.1), (-Lh - 0.008, -W / 2 + 0.15, 1.75), (-Lh - 0.008, W / 2 - 0.15, 1.75)], glass)
    # the kerb-side sliding door (right side, -y): open/missing shows the dark inside and benches
    state = rng.pick({'missing': 4, 'open': 3, 'closed': 2}) if cond != 'new' else rng.pick({'open': 1, 'closed': 1})
    if state != 'closed':
        mb.face([M @ Vector((0.0, -W / 2 - 0.01, 0.4)), M @ Vector((0.0, -W / 2 - 0.01, 1.75)), M @ Vector((1.0, -W / 2 - 0.01, 1.75)), M @ Vector((1.0, -W / 2 - 0.01, 0.4))], 'paint', (0.02, 0.02, 0.02), 0)
        for k in range(3):
            mb.box('wood', L(M, -0.5 - k * 0.55, 0, 0.75), hex_rgb('#5a4632'), 0.6, size=(0.35, W - 0.3, 0.06))
    if state == 'open':
        mb.box('carpaint', L(M, -0.55, -W / 2 - 0.05, 1.05), col, wear, size=(1.0, 0.03, 1.3))
    # front: black strip with grille slot, rectangular lamps, bumper, plate
    mb.box('plastic', L(M, Lh + 0.005, 0, 0.88), hex_rgb('#141414'), wear, size=(0.02, W - 0.1, 0.16))
    for s in (-1, 1):
        lamp(mb, M, Lh + 0.01, s * 0.62, 0.7, 0.2, 0.13, 'head')
        lamp(mb, M, Lh + 0.01, s * 0.82, 0.58, 0.1, 0.06, 'amber')
        lamp(mb, M, -Lh - 0.01, s * 0.8, 0.62, 0.12, 0.28, 'tail')
        mb.box('plastic', L(M, Lh - 0.3, s * (W / 2 + 0.12), 1.2), hex_rgb('#141414'), 0.4, size=(0.05, 0.12, 0.18))  # mirrors
    for x in (Lh + 0.06, -Lh - 0.06):
        if cond == 'battered' and rng.chance(0.3):
            continue  # a bumper lost
        mb.box('plastic', L(M, x, 0, 0.38), hex_rgb('#141414'), wear, size=(0.14, W + 0.04, 0.18))
    plate(mb, M, Lh + 0.14, 0.38, rng)
    plate(mb, M, -Lh - 0.14, 0.62, rng, back=True)
    # wheels (wheelbase 2.46, 0.65 m tyres)
    for x in (1.23, -1.23):
        for s in (-1, 1):
            wheel(mb, M, x, s * (W / 2 - 0.12), 0.325, 0.19, cond)
    # roof rack and load
    if rng.chance(0.55):
        rack = hex_rgb('#1a1a1a' if rng.chance(0.6) else '#6b3a22')
        for s in (-1, 1):
            parts.bar(mb, 'steel', M @ Vector((-1.4, s * 0.72, H + 0.15)), M @ Vector((1.0, s * 0.72, H + 0.15)), 0.035, rack, 0.6)
        for x in (-1.4, -0.6, 0.2, 1.0):
            parts.bar(mb, 'steel', M @ Vector((x, -0.72, H + 0.15)), M @ Vector((x, 0.72, H + 0.15)), 0.03, rack, 0.6)
            for s in (-1, 1):
                parts.bar(mb, 'steel', M @ Vector((x, s * 0.72, H)), M @ Vector((x, s * 0.72, H + 0.15)), 0.03, rack, 0.6)
        if load and rng.chance(0.6):
            for k in range(rng.randrange(1, 4)):
                mb.box('cloth', L(M, rng.between(-1.2, 0.8), rng.between(-0.4, 0.4), H + 0.35, rz=rng.between(-0.3, 0.3)), hex_rgb(rng.pick(['#c8a96e', '#1f5fa8', '#d32f2f', '#e8e2d0', '#2e7d4f'])), 0.5, size=(rng.between(0.5, 1.0), rng.between(0.4, 0.7), rng.between(0.25, 0.45)))
    # slogan on the rear window strip and the windscreen strip
    slogan = rng.pick(SLOGANS)
    mb.box('plastic', L(M, -Lh - 0.012, 0, 1.79), hex_rgb('#141414'), 0, size=(0.005, W - 0.3, 0.13))
    parts.text(mb, 'paint', L(M, -Lh - 0.02, 0, 1.79, rz=-math.pi / 2), slogan, 0.07, hex_rgb('#d4a62a'), max_w=W - 0.4)
    mb.box('plastic', L(M, Lh - 0.5, 0, 1.79, ry=-0.65), hex_rgb('#141414'), 0, size=(0.005, W - 0.3, 0.11))
    if cond == 'wreck':
        mb.box('mud', L(M, 0, 0, H + 0.01), hex_rgb('#6b3a22'), 1.0, size=(3.0, 1.4, 0.01))


def korope(mb, M, rng, cond='battered'):
    """The smaller yellow minibus (the owner's 'Tambulu'): a tall narrow microvan, 3.40 x 1.48 x 1.90,
    short sloped nose, same livery with a single stripe, 12-inch wheels."""
    Lh, W, H = 1.7, 1.48, 1.9
    wear = WEAR[cond]
    col = hex_rgb(YELLOW[cond])
    body(mb, M, [(-Lh, 0.28), (Lh - 0.05, 0.28), (Lh, 0.36), (Lh, 0.95), (Lh - 0.25, 1.15), (Lh - 0.45, H - 0.03), (Lh - 0.55, H), (-Lh + 0.05, H), (-Lh, H - 0.1)], W, 'carpaint', col, wear, r=0.12)
    glass = hex_rgb('#1c2830')
    glass_panel(mb, M, [(Lh - 0.27, -W / 2 + 0.1, 1.18), (Lh - 0.27, W / 2 - 0.1, 1.18), (Lh - 0.47, W / 2 - 0.1, 1.82), (Lh - 0.47, -W / 2 + 0.1, 1.82)], glass)
    for s in (-1, 1):
        y = s * (W / 2 + 0.008)
        for (x0, x1) in ((0.7, 1.15), (-0.4, 0.55), (-1.55, -0.55)):
            pts = [(x0, y, 1.1), (x1, y, 1.1), (x1, y, 1.65), (x0, y, 1.65)]
            glass_panel(mb, M, pts if s > 0 else list(reversed(pts)), glass)
        mb.box('carpaint', L(M, 0, s * (W / 2 + 0.004), 0.92), hex_rgb('#141414'), wear, size=(3.2, 0.01, 0.1))
    mb.face([M @ Vector((-0.4, -W / 2 - 0.01, 0.35)), M @ Vector((-0.4, -W / 2 - 0.01, 1.7)), M @ Vector((0.5, -W / 2 - 0.01, 1.7)), M @ Vector((0.5, -W / 2 - 0.01, 0.35))], 'paint', (0.02, 0.02, 0.02), 0)
    for s in (-1, 1):
        lamp(mb, M, Lh + 0.01, s * 0.5, 0.72, 0.18, 0.12, 'head')
        lamp(mb, M, -Lh - 0.01, s * 0.62, 0.6, 0.1, 0.25, 'tail')
    mb.box('plastic', L(M, Lh + 0.05, 0, 0.34), hex_rgb('#141414'), wear, size=(0.1, W, 0.14))
    mb.box('plastic', L(M, -Lh - 0.05, 0, 0.34), hex_rgb('#141414'), wear, size=(0.1, W, 0.14))
    for x in (1.15, -1.15):
        for s in (-1, 1):
            wheel(mb, M, x, s * (W / 2 - 0.1), 0.275, 0.15, cond)
    parts.text(mb, 'paint', L(M, -Lh - 0.02, 0, 1.55, rz=-math.pi / 2), rng.pick(SLOGANS), 0.06, hex_rgb('#141414'), max_w=W - 0.3)


def brt(mb, M, rng, cond='worn'):
    """A 12 m high-floor city bus in an invented blue-and-white scheme, full-length glazing."""
    Lh, W, H = 6.0, 2.55, 3.2
    wear = WEAR[cond]
    body(mb, M, [(-Lh, 0.35), (Lh, 0.35), (Lh, 2.9), (Lh - 0.15, H), (-Lh + 0.1, H), (-Lh, 3.05)], W, 'carpaint', hex_rgb('#f2f2ee'), wear, r=0.2)
    for s in (-1, 1):
        mb.box('carpaint', L(M, 0, s * (W / 2 + 0.004), 0.75), hex_rgb('#1f4fa0'), wear, size=(2 * Lh - 0.2, 0.01, 0.8))
        y = s * (W / 2 + 0.008)
        pts = [(-Lh + 0.4, y, 1.3), (Lh - 0.3, y, 1.3), (Lh - 0.3, y, 2.6), (-Lh + 0.4, y, 2.6)]
        glass_panel(mb, M, pts if s > 0 else list(reversed(pts)))
    glass_panel(mb, M, [(Lh + 0.01, -W / 2 + 0.1, 1.0), (Lh + 0.01, W / 2 - 0.1, 1.0), (Lh + 0.01, W / 2 - 0.1, 2.85), (Lh + 0.01, -W / 2 + 0.1, 2.85)])
    for x in (Lh - 2.4, -Lh + 2.8):
        for s in (-1, 1):
            wheel(mb, M, x, s * (W / 2 - 0.15), 0.5, 0.3, cond, rim='alloy')
    for s in (-1, 1):
        lamp(mb, M, Lh + 0.02, s * 0.95, 0.75, 0.3, 0.15, 'head')
        lamp(mb, M, -Lh - 0.02, s * 1.05, 1.0, 0.15, 0.4, 'tail')
    mb.box('emit', L(M, Lh + 0.02, 0, 2.95), hex_rgb('#ffb000'), 0, size=(0.02, 1.6, 0.25))  # route display


# ---------------------------------------------------------------- keke and okada
def keke(mb, M, rng, cond='worn', cargo=False):
    """Tricycle taxi, 2.66 x 1.30 x 1.70 m, wheelbase 2.00 [src]: yellow tub, black canvas canopy
    on a frame, side curtains rolled or down, one front wheel, two rear."""
    wear = WEAR[cond]
    col = hex_rgb(YELLOW[cond] if not cargo else rng.pick(['#2e7d4f', '#1f5fa8', '#c62828']))
    body(mb, M, [(-1.25, 0.3), (0.7, 0.3), (1.25, 0.45), (1.32, 0.95), (1.1, 1.1), (0.65, 1.1), (0.45, 0.72), (-1.25, 0.72)], 1.25, 'carpaint', col, wear, r=0.1)
    canvas = hex_rgb('#151515' if cond in ('new', 'worn') else '#3a3a3a')
    mb.box('cloth', L(M, -0.15, 0, 1.68), canvas, wear, size=(2.3, 1.32, 0.06))
    mb.box('cloth', L(M, -1.22, 0, 1.2), canvas, wear, size=(0.04, 1.3, 0.95))
    for x, s in ((1.0, -1), (1.0, 1), (-1.2, -1), (-1.2, 1)):
        parts.bar(mb, 'steel', M @ Vector((x, s * 0.6, 0.72 if x < 0 else 1.1)), M @ Vector((x - 0.05, s * 0.62, 1.66)), 0.035, hex_rgb('#1a1a1a'), 0.4)
    glass_panel(mb, M, [(1.12, -0.55, 1.12), (1.12, 0.55, 1.12), (1.02, 0.52, 1.62), (1.02, -0.52, 1.62)])
    if rng.chance(0.5):  # side curtains rolled down on one side
        mb.box('cloth', L(M, -0.3, 0.64, 1.3), canvas, wear, size=(1.6, 0.02, 0.7))
    mb.box('plastic', L(M, -0.4, 0, 0.82), hex_rgb('#2a2a2a'), 0.4, size=(1.1, 1.0, 0.1))  # bench
    mb.box('plastic', L(M, -0.95, 0, 1.1), hex_rgb('#2a2a2a'), 0.4, size=(0.12, 1.0, 0.5))
    lamp(mb, M, 1.33, 0, 0.9, 0.12, 0.1, 'head')
    for s in (-1, 1):
        lamp(mb, M, -1.27, s * 0.5, 0.55, 0.08, 0.12, 'tail')
    wheel(mb, M, 1.1, 0.0, 0.25, 0.12, cond)
    for s in (-1, 1):
        wheel(mb, M, -0.9, s * 0.58, 0.25, 0.12, cond)
    if cargo:  # flatbed with sacks
        mb.box('steel', L(M, -1.4, 0, 0.75), hex_rgb('#3a3a3a'), wear, size=(1.2, 1.3, 0.05))
        for k in range(rng.randrange(2, 6)):
            mb.box('cloth', L(M, -1.4 + rng.between(-0.4, 0.4), rng.between(-0.4, 0.4), 0.95 + k * 0.1), hex_rgb('#e8dcc0'), 0.5, size=(0.6, 0.4, 0.25))
    parts.text(mb, 'paint', L(M, -1.27, 0, 1.4, rz=-math.pi / 2), rng.pick(SLOGANS), 0.06, hex_rgb('#d4a62a'), max_w=1.1)


def okada(mb, M, rng, cond='worn', rider=None, passenger=None, load=None):
    """Motorcycle taxi, 2.02 x 0.74 x 1.06 m, wheelbase 1.285, 17-inch wheels [src]."""
    wear = WEAR[cond]
    col = hex_rgb(rng.pick({'#b71c1c': 3, '#111111': 3, '#1565c0': 2, '#e8e2d6': 1}))
    for x in (0.64, -0.64):  # 17-inch wheels with spokes
        parts.cyl(mb, 'rubber', L(M, x, -0.04, 0.31, rx=-math.pi / 2), 0.31, 0.08, hex_rgb('#1c1c1c'), 0, seg=18)
        parts.cyl(mb, 'steel', L(M, x, -0.045, 0.31, rx=-math.pi / 2), 0.24, 0.09, hex_rgb('#b0b4b8'), 0.3, seg=18)
        parts.cyl(mb, 'steel', L(M, x, -0.05, 0.31, rx=-math.pi / 2), 0.07, 0.1, hex_rgb('#8a8a8a'), 0.3, seg=10)
    body(mb, M, [(-0.1, 0.72), (0.5, 0.72), (0.62, 0.86), (0.5, 0.98), (0.0, 0.95)], 0.3, 'carpaint', col, wear, r=0.08)  # tank
    body(mb, M, [(-0.85, 0.82), (-0.05, 0.82), (-0.05, 0.92), (-0.8, 0.95)], 0.28, 'rubber', hex_rgb('#1a1a1a'), 0.4, r=0.05)  # seat
    mb.box('steel', L(M, 0.05, 0, 0.48), hex_rgb('#6a6a6a'), wear, size=(0.45, 0.25, 0.32))  # engine
    parts.bar(mb, 'steel', M @ Vector((0.64, 0, 0.31)), M @ Vector((0.5, 0, 1.0)), 0.05, hex_rgb('#9a9a9a'), 0.3)  # fork
    parts.bar(mb, 'steel', M @ Vector((0.48, -0.36, 1.05)), M @ Vector((0.48, 0.36, 1.05)), 0.03, hex_rgb('#2a2a2a'), 0.3)
    for s in (-1, 1):
        parts.bar(mb, 'steel', M @ Vector((0.48, s * 0.25, 1.05)), M @ Vector((0.46, s * 0.3, 1.3)), 0.015, hex_rgb('#2a2a2a'), 0.3)
        mb.box('steel', L(M, 0.46, s * 0.3, 1.32), hex_rgb('#d8d8d8'), 0.1, size=(0.02, 0.1, 0.07))
    body(mb, M, [(0.5, 0.88), (0.68, 0.88), (0.7, 1.05), (0.52, 1.08)], 0.22, 'carpaint', col, wear, r=0.03)  # headlamp cowl
    lamp(mb, M, 0.71, 0, 0.97, 0.1, 0.08, 'head')
    mb.box('steel', L(M, -0.95, 0, 0.82), hex_rgb('#2a2a2a'), 0.4, size=(0.35, 0.28, 0.04))  # rack
    lamp(mb, M, -1.0, 0, 0.75, 0.08, 0.05, 'tail')
    parts.bar(mb, 'steel', M @ Vector((-0.1, -0.15, 0.4)), M @ Vector((-0.8, -0.17, 0.55)), 0.06, hex_rgb('#c8c8c8'), 0.4)  # exhaust
    if load:
        mb.box('cloth', L(M, -0.95, 0, 1.15), hex_rgb(load), 0.5, size=(0.6, 0.6, 0.6))


def _car_profile(kind):
    if kind == 'suv':
        return [(-2.25, 0.4), (2.25, 0.4), (2.35, 0.55), (2.35, 0.95), (1.95, 1.08), (1.2, 1.12), (0.65, 1.72), (-2.0, 1.75), (-2.3, 1.6), (-2.35, 0.7)], 1.88, 0.38, 1.4, 'alloy'
    if kind == 'pickup':
        return [(-2.6, 0.42), (2.5, 0.42), (2.6, 0.6), (2.6, 0.98), (2.1, 1.05), (1.35, 1.08), (0.85, 1.65), (-0.45, 1.68), (-0.55, 1.1), (-2.6, 1.1)], 1.82, 0.38, 1.6, 'steel'
    return [(-2.25, 0.3), (2.2, 0.3), (2.3, 0.5), (2.3, 0.72), (1.6, 0.9), (1.0, 0.93), (0.35, 1.4), (-0.95, 1.42), (-1.65, 0.98), (-2.3, 0.92), (-2.3, 0.5)], 1.75, 0.32, 1.35, 'steel'


def car(mb, M, rng, cond='worn', kind='saloon', colour=None, taxi=False):
    """Private cars: saloon, SUV, pickup (research-vehicles 10). Taxi: yellow with a roof sign."""
    prof, W, r, wb, rim = _car_profile(kind)
    wear = WEAR[cond]
    col = hex_rgb(colour or ('#f2c200' if taxi else rng.pick({'#c9ced2': 4, '#1d1d1d': 3, '#f2f2ee': 3, '#2f3d4c': 2, '#7a1f1f': 2, '#6d5d44': 1, '#3f5a3a': 1, '#1f4fa0': 1})))
    body(mb, M, prof, W, 'carpaint', col, wear, r=0.16)
    # greenhouse: side windows on both sides, screen and rear glass
    xs = sorted(p[0] for p in prof if p[1] > 1.0)
    x0, x1 = (xs[0] + 0.12, xs[-1] - 0.12) if xs else (-0.8, 0.8)
    zt = max(p[1] for p in prof) - 0.12
    zb = zt - (0.38 if kind == 'saloon' else 0.5)
    for s in (-1, 1):
        y = s * (W / 2 - 0.03 + 0.012)
        pts = [(x0, y, zb), (x1, y, zb), (x1 - 0.1, y, zt), (x0 + 0.1, y, zt)]
        glass_panel(mb, M, pts if s > 0 else list(reversed(pts)))
        mb.box('plastic', L(M, x1 + 0.15, s * (W / 2 + 0.1), zb + 0.05), col, wear, size=(0.08, 0.12, 0.12))  # mirrors
        for x in (0.2, -0.9):  # door seams and handles
            mb.box('paint', L(M, x, s * (W / 2 + 0.003), 0.7), hex_rgb('#202020'), 0, size=(0.01, 0.005, 0.6))
            mb.box('steel', L(M, x - 0.15, s * (W / 2 + 0.008), 0.82), hex_rgb('#c9ced2'), 0, size=(0.14, 0.01, 0.03))
    front = max(p[0] for p in prof)
    back = min(p[0] for p in prof)
    for s in (-1, 1):
        lamp(mb, M, front + 0.005, s * (W / 2 - 0.25), 0.68 if kind != 'saloon' else 0.6, 0.3, 0.1, 'head')
        lamp(mb, M, back - 0.005, s * (W / 2 - 0.2), 0.78 if kind != 'saloon' else 0.72, 0.25, 0.12, 'tail')
    mb.box('plastic', L(M, front + 0.005, 0, 0.55), hex_rgb('#1d1d1d'), 0.3, size=(0.02, W * 0.45, 0.16))  # grille
    for x in (front + 0.04, back - 0.04):
        mb.box('plastic', L(M, x, 0, 0.42), hex_rgb('#2a2a2a'), wear, size=(0.12, W + 0.02, 0.16))
    plate(mb, M, front + 0.11, 0.42, rng)
    plate(mb, M, back - 0.11, 0.55, rng, back=True)
    for x in (wb, -wb):
        for s in (-1, 1):
            wheel(mb, M, x, s * (W / 2 - 0.1), r, 0.22, cond, rim=rim)
    if taxi:
        mb.box('plastic', L(M, -0.3, 0, max(p[1] for p in prof) + 0.08), hex_rgb('#ffffff'), 0, size=(0.4, 0.15, 0.15))
        for s in (-1, 1):
            mb.box('carpaint', L(M, -0.2, s * (W / 2 + 0.005), 0.65), hex_rgb('#141414'), 0, size=(3.4, 0.01, 0.06))
    if kind == 'pickup' and rng.chance(0.6):  # a load in the bed
        mb.box('cloth', L(M, -1.6, 0, 1.25), hex_rgb(rng.pick(['#c8a96e', '#2f5fa8', '#3a3a3a'])), 0.5, size=(1.6, 1.5, 0.5))


def police_pickup(mb, M, rng, cond='worn'):
    """A police pickup with bench seats in the bed (generic invented livery: dark blue, pale band)."""
    car(mb, M, rng, cond, kind='pickup', colour='#1f2e5a')
    mb.box('carpaint', L(M, 0.5, 0.92, 0.75), hex_rgb('#8db6d9'), 0, size=(3.5, 0.01, 0.15))
    mb.box('carpaint', L(M, 0.5, -0.92, 0.75), hex_rgb('#8db6d9'), 0, size=(3.5, 0.01, 0.15))
    for s in (-1, 1):
        mb.box('wood', L(M, -1.5, s * 0.6, 1.3), hex_rgb('#3a3a3a'), 0.5, size=(1.8, 0.3, 0.06))
    mb.box('emit', L(M, -0.2, 0, 1.75), hex_rgb('#2050ff'), 0, size=(0.2, 1.0, 0.1))


# ---------------------------------------------------------------- trucks
def tipper(mb, M, rng, cond='battered'):
    """Sand/laterite tipper, 8.5 x 2.5 x 3.4: bonneted or cab-over, steel tipping body with a heaped load."""
    wear = WEAR[cond]
    cab = hex_rgb(rng.pick(['#e8e6df', '#c62828', '#1f5fa8', '#2e7d4f', '#c8a020']))
    mb.box('carpaint', L(M, 3.1, 0, 1.75), cab, wear, size=(2.0, 2.4, 2.3))
    glass_panel(mb, M, [(4.11, -1.0, 2.0), (4.11, 1.0, 2.0), (4.11, 1.0, 2.75), (4.11, -1.0, 2.75)])
    mb.box('plastic', L(M, 4.1, 0, 1.0), hex_rgb('#1d1d1d'), 0.4, size=(0.05, 1.6, 0.5))
    mb.box('steel', L(M, -0.9, 0, 1.0), hex_rgb('#2a2a2a'), wear, size=(8.0, 1.0, 0.3))
    bc = hex_rgb(rng.pick(['#c8a020', '#8a8d8c', '#c62828', '#6b3a22']))
    for s in (-1, 1):
        mb.box('steel', L(M, -1.0, s * 1.2, 2.05), bc, wear + 0.2, size=(5.4, 0.08, 1.4))
    mb.box('steel', L(M, -1.0, 0, 1.4), bc, wear + 0.2, size=(5.4, 2.4, 0.12))
    mb.box('steel', L(M, 1.7, 0, 2.2), bc, wear + 0.2, size=(0.1, 2.4, 1.7))
    load = hex_rgb(rng.pick(['#d8c9a3', '#c4703d', '#8f8a80']))
    for k in range(5):  # a heaped load of sand, laterite or stone
        mb.box('mud', L(M, -1.0 + (k - 2) * 1.0, 0, 2.55 + 0.25 * math.cos((k - 2) / 2.2)), load, 0.2, size=(1.05, 2.3, 0.6))
    for x in (3.2, -1.6, -2.8):
        for s in (-1, 1):
            wheel(mb, M, x, s * 1.05, 0.52, 0.32, cond)
    for s in (-1, 1):
        lamp(mb, M, 4.12, s * 0.95, 0.95, 0.25, 0.15, 'head')


def tanker(mb, M, rng, cond='worn'):
    """Fuel tanker: cab plus a long elliptical silver tank with a top walkway and hatches."""
    wear = WEAR[cond]
    mb.box('carpaint', L(M, 4.2, 0, 1.75), hex_rgb(rng.pick(['#e8e6df', '#c62828', '#1f5fa8'])), wear, size=(2.0, 2.4, 2.3))
    glass_panel(mb, M, [(5.21, -1.0, 2.0), (5.21, 1.0, 2.0), (5.21, 1.0, 2.75), (5.21, -1.0, 2.75)])
    mb.box('steel', L(M, -0.5, 0, 1.0), hex_rgb('#2a2a2a'), wear, size=(10.5, 1.0, 0.3))
    tm = L(M, -1.2, 0, 2.15, ry=math.pi / 2)
    parts.cyl(mb, 'steel', tm @ Matrix.Translation((0, 0, -4.5)) @ Matrix.Scale(1.0, 4, (0, 0, 1)), 1.15, 9.0, hex_rgb('#c9ced2'), wear, seg=20)
    for k in range(4):
        parts.cyl(mb, 'steel', L(M, -4.5 + k * 2.2, 0, 3.25), 0.3, 0.12, hex_rgb('#9ea3a6'), wear, seg=10)
    mb.box('steel', L(M, -1.2, 0, 3.32), hex_rgb('#5a5a5a'), wear, size=(8.5, 0.5, 0.04))
    for x in (4.3, -3.5, -4.8, -6.0):
        for s in (-1, 1):
            wheel(mb, M, x, s * 1.05, 0.52, 0.32, cond)
    mb.box('plastic', L(M, -1.2, 1.16, 2.1), hex_rgb('#c62828'), 0, size=(2.0, 0.01, 0.4))  # an invented hazard band
    mb.box('plastic', L(M, -1.2, -1.16, 2.1), hex_rgb('#c62828'), 0, size=(2.0, 0.01, 0.4))


# ---------------------------------------------------------------- carts
def pusher_cart(mb, M, rng, loaded=True):
    """The truck-pusher's cart: a plank bed on two car wheels, long handles, piled high."""
    mb.box('wood', L(M, 0, 0, 0.8), hex_rgb('#7a5a3a'), 0.7, size=(2.6, 1.1, 0.08))
    for s in (-1, 1):
        parts.bar(mb, 'wood', M @ Vector((-1.3, s * 0.5, 0.8)), M @ Vector((-2.3, s * 0.45, 0.9)), 0.07, hex_rgb('#6b4f36'), 0.7)
        wheel(mb, M, 0.3, s * 0.65, 0.3, 0.18, 'battered')
    if loaded:
        for k in range(rng.randrange(3, 8)):
            mb.box('cloth', L(M, rng.between(-1.0, 1.0), rng.between(-0.35, 0.35), 1.0 + k * 0.2), hex_rgb(rng.pick(['#e8dcc0', '#2f5fa8', '#c62828', '#d9b85a', '#3a3a3a'])), 0.5, size=(rng.between(0.4, 0.9), rng.between(0.4, 0.8), 0.25))


def wheelbarrow(mb, M, rng):
    mb.box('steel', L(M, 0, 0, 0.55, ry=0.1), hex_rgb(rng.pick(['#2f6fae', '#c62828', '#3a3a3a'])), 0.8, size=(0.9, 0.6, 0.3))
    parts.cyl(mb, 'rubber', L(M, 0.55, -0.05, 0.2, rx=-math.pi / 2), 0.2, 0.1, hex_rgb('#1c1c1c'), 0, seg=12)
    for s in (-1, 1):
        parts.bar(mb, 'steel', M @ Vector((0.55, s * 0.05, 0.2)), M @ Vector((-0.9, s * 0.3, 0.75)), 0.035, hex_rgb('#2a2a2a'), 0.6)


BUILDERS = {'danfo': danfo, 'korope': korope, 'brt': brt, 'keke': keke, 'okada': okada, 'car': car, 'police': police_pickup,
            'tipper': tipper, 'tanker': tanker, 'cart': pusher_cart, 'wheelbarrow': wheelbarrow}
LENGTH = {'danfo': 4.8, 'korope': 3.6, 'brt': 12.2, 'keke': 2.8, 'okada': 2.1, 'car': 4.8, 'police': 5.3, 'tipper': 8.6, 'tanker': 11.5, 'cart': 3.6, 'wheelbarrow': 1.6}
# research-vehicles 8.6: shares of moving traffic by character and road class
MIX = {
    ('dense', 'main'): {'danfo': 26, 'korope': 4, 'keke': 5, 'okada': 5, 'car': 40, 'brt': 5, 'tipper': 6, 'tanker': 6, 'cart': 3},
    ('dense', 'street'): {'danfo': 7, 'korope': 3, 'keke': 25, 'okada': 25, 'car': 30, 'tipper': 3, 'cart': 5, 'wheelbarrow': 2},
    ('old_island', 'main'): {'danfo': 20, 'car': 55, 'brt': 5, 'tanker': 5, 'tipper': 5, 'cart': 10},
    ('old_island', 'street'): {'keke': 5, 'okada': 5, 'car': 40, 'tipper': 5, 'cart': 40, 'wheelbarrow': 5},
    ('sprawl', 'main'): {'danfo': 20, 'korope': 5, 'keke': 15, 'okada': 15, 'car': 30, 'brt': 3, 'tipper': 7, 'tanker': 3, 'cart': 2},
    ('sprawl', 'street'): {'danfo': 2, 'korope': 3, 'keke': 30, 'okada': 30, 'car': 30, 'tipper': 3, 'cart': 2},
    ('elite', 'main'): {'danfo': 5, 'car': 80, 'brt': 5, 'tanker': 4, 'tipper': 4, 'okada': 2},
    ('elite', 'street'): {'car': 92, 'okada': 3, 'tipper': 5},
    ('civic', 'main'): {'danfo': 15, 'car': 60, 'brt': 10, 'police': 2, 'tanker': 5, 'tipper': 5, 'cart': 3},
    ('civic', 'street'): {'danfo': 5, 'car': 70, 'police': 3, 'keke': 5, 'okada': 2, 'tipper': 5, 'cart': 3},
    ('port', 'main'): {'danfo': 10, 'car': 20, 'tanker': 35, 'tipper': 30, 'brt': 3, 'okada': 2},
    ('port', 'street'): {'danfo': 10, 'car': 25, 'tanker': 25, 'tipper': 25, 'okada': 5, 'keke': 5, 'cart': 5},
    ('waterfront', 'street'): {'danfo': 5, 'keke': 20, 'okada': 30, 'car': 20, 'tipper': 10, 'cart': 15},
}
COMMERCIAL = {'danfo', 'korope', 'keke', 'okada', 'tipper', 'tanker', 'brt', 'cart'}


def mix(ch, road):
    k = 'main' if road == 'main' else 'street'
    return MIX.get((ch, k)) or MIX.get(('dense', k))
