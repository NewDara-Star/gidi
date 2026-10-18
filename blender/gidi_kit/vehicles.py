"""Vehicles of Lagos roads, from docs/look/research-vehicles.md (sizes [src] where it had them).
Every builder adds faces to a MeshBuilder at matrix M (x forward, y left, z up, origin on the
ground under the middle). Condition ('new', 'worn', 'battered', 'wreck') drives wear, mismatched
panels, missing doors and wheels. Liveries, slogans and plates are invented (rule zero)."""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import hex_rgb, shade

YELLOW = {'new': '#f5c400', 'worn': '#ecb810', 'battered': '#dca81c', 'wreck': '#a87a22'}   # danfo yellow fades to mustard, never to beige
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


def car(mb, M, rng, cond='worn', kind='saloon', colour=None, taxi=False, bed_load=True):
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
    if kind == 'pickup' and bed_load and rng.chance(0.6):  # a load in the bed
        mb.box('cloth', L(M, -1.6, 0, 1.25), hex_rgb(rng.pick(['#c8a96e', '#2f5fa8', '#3a3a3a'])), 0.5, size=(1.6, 1.5, 0.5))


def police_pickup(mb, M, rng, cond='worn'):
    """A police pickup with bench seats in the bed (generic invented livery: dark blue, pale band)."""
    car(mb, M, rng, cond, kind='pickup', colour='#1f2e5a')
    mb.box('carpaint', L(M, 0.5, 0.92, 0.75), hex_rgb('#8db6d9'), 0, size=(3.5, 0.01, 0.15))
    mb.box('carpaint', L(M, 0.5, -0.92, 0.75), hex_rgb('#8db6d9'), 0, size=(3.5, 0.01, 0.15))
    for s in (-1, 1):
        mb.box('wood', L(M, -1.5, s * 0.6, 1.3), hex_rgb('#3a3a3a'), 0.5, size=(1.8, 0.3, 0.06))
    mb.box('emit', L(M, -0.2, 0, 1.75), hex_rgb('#2050ff'), 0, size=(0.2, 1.0, 0.1))


def task_force_truck(mb, M, rng):
    """The task force truck: a battered pickup in faded government green and white, seized okadas piled in the back,
    one standing up against the cab with its front wheel over the side."""
    car(mb, M, rng, 'battered', kind='pickup', colour='#5d7a4a', bed_load=False)
    for s in (-1, 1):
        mb.box('carpaint', L(M, 0.4, s * 0.915, 0.82), hex_rgb('#e8e6df'), 0.6, size=(4.4, 0.01, 0.16))
        mb.box('carpaint', L(M, -1.6, s * 0.92, 1.06), hex_rgb('#4a6a3a'), 0.8, size=(2.1, 0.03, 0.12))   # the bed's top rail
    from . import props
    for s in (-1, 1):   # the agency's name on the doors (invented, generic)
        F = M @ Matrix.Translation((0.35, s * 0.93, 0.62)) @ Matrix.Rotation(0 if s > 0 else math.pi, 4, 'Z')
        props.board(mb, F, 'TASK FORCE', 1.2, 0.2, hex_rgb('#e8e6df'), hex_rgb('#2e4a2a'), wear=0.6, hand=False)
    bed = 1.1
    okada(mb, L(M, -1.55, 0.05, bed + 0.37, rx=math.pi / 2), rng.child('seized', 0), 'battered')   # on its side
    okada(mb, L(M, -1.65, -0.1, bed + 0.95, rz=0.25, rx=-math.pi / 2 + 0.2), rng.child('seized', 1), 'wreck')   # thrown on top
    okada(mb, L(M, -1.0, 0.55, bed, rz=math.pi / 2 + 0.1, ry=-0.35), rng.child('seized', 2), 'battered')   # stood against the cab, wheel over the side


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


# ---------------------------------------------------------------- heavy goods
CONTAINER_COLS = ['#8e2f22', '#1f4f8a', '#2f6b3a', '#7a7d80', '#5a1f2a', '#c8a020', '#e8e6df', '#b0551f']


def container_box(mb, M, rng, length=12.2, col=None, wear=0.5):
    """A shipping container (corrugated sides, end doors with locking bars), base at M's origin,
    centred, x along. Plain: no line's name or mark (rule zero)."""
    col = hex_rgb(col or rng.pick(CONTAINER_COLS))
    H, W = 2.59, 2.44
    mb.box('steel', L(M, 0, 0, H / 2), col, wear, size=(length, W, H))
    k = -length / 2 + 0.3
    while k < length / 2 - 0.2:  # corrugation ribs on both sides
        for s_ in (-1, 1):
            mb.box('steel', L(M, k, s_ * (W / 2 + 0.02), H / 2), shade(col, 0.85), wear, size=(0.12, 0.04, H - 0.2))
        k += 0.3
    for y in (-0.6, -0.2, 0.2, 0.6):  # door locking bars at the back
        mb.box('steel', L(M, -length / 2 - 0.03, y, H / 2), hex_rgb('#3a3a3a'), wear, size=(0.04, 0.05, H - 0.3))
    mb.box('steel', L(M, 0, 0, H + 0.02), shade(col, 0.8), wear + 0.2, size=(length, W, 0.04))


def container_truck(mb, M, rng, cond='worn', loaded=None):
    """An articulated container truck, 16.5 m: a cab-over tractor and a skeletal trailer carrying a
    40 ft container (or empty), the Apapa queue's vehicle. Front at +x."""
    wear = WEAR[cond]
    cab = hex_rgb(rng.pick(['#e8e6df', '#c62828', '#1f5fa8', '#e0b020', '#2e7d4f', '#d8d4cc']))
    # tractor: cab-over, 2.5 m wide, roof at 3.4 m, fuel tanks and air tanks below
    mb.box('carpaint', L(M, 6.9, 0, 2.15), cab, wear, size=(2.2, 2.5, 2.5))
    mb.box('carpaint', L(M, 6.6, 0, 3.55), shade(cab, 0.9), wear, size=(1.6, 2.3, 0.4))  # roof fairing
    glass_panel(mb, M, [(8.01, -1.1, 2.3), (8.01, 1.1, 2.3), (8.01, 1.1, 3.25), (8.01, -1.1, 3.25)])
    mb.box('plastic', L(M, 8.0, 0, 1.2), hex_rgb('#1d1d1d'), 0.4, size=(0.08, 2.3, 0.6))  # bumper and grille
    mb.box('steel', L(M, 3.0, 0, 0.95), hex_rgb('#2a2a2a'), wear, size=(8.5, 1.0, 0.3))  # tractor chassis
    for s_ in (-1, 1):
        parts.cyl(mb, 'steel', L(M, 4.9, s_ * 1.0, 0.95, ry=math.pi / 2), 0.3, 1.4, hex_rgb('#b8bcbf'), wear, seg=10)
    mb.box('steel', L(M, 4.4, 0, 1.25), hex_rgb('#3a3a3a'), wear, size=(1.2, 2.0, 0.12))  # fifth wheel
    for x in (7.0, 3.6, 2.3):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 1.05, 0.52, 0.32, cond)
    for s_ in (-1, 1):
        lamp(mb, M, 8.02, s_ * 0.95, 1.2, 0.25, 0.15, 'head')
    # trailer: skeletal frame on three axles
    mb.box('steel', L(M, -2.5, 0, 1.25), hex_rgb('#2a2a2a'), wear, size=(12.4, 0.9, 0.25))
    for x in (-6.2, -7.5, -8.8):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 1.05, 0.5, 0.3, cond)
    for x in (2.0, -7.0):
        mb.box('steel', L(M, x, 0, 1.3), hex_rgb('#2a2a2a'), wear, size=(0.3, 2.4, 0.2))
    if loaded if loaded is not None else rng.chance(0.85):
        container_box(mb, L(M, -2.5, 0, 1.42), rng, 12.2, wear=wear)
    for s_ in (-1, 1):
        lamp(mb, M, -8.95, s_ * 1.0, 1.1, 0.2, 0.12, 'tail')


def lorry_911(mb, M, rng, cond='battered', load=None):
    """The old bonneted food lorry of the big markets, 8.8 m: a long nose, a wooden cab, tall plank
    sides painted in bands, loaded high with baskets of tomatoes or sacks of onions. Front at +x."""
    wear = WEAR[cond]
    cab = hex_rgb(rng.pick(['#e0b020', '#c62828', '#1f5fa8', '#2e7d4f', '#e8e6df']))
    mb.box('carpaint', L(M, 3.55, 0, 1.25), cab, wear, size=(1.7, 1.7, 1.0))  # bonnet
    mb.box('carpaint', L(M, 3.55, 0, 1.78), shade(cab, 0.85), wear, size=(1.6, 1.6, 0.06))
    mb.box('plastic', L(M, 4.43, 0, 1.2), hex_rgb('#c9ced2'), wear, size=(0.06, 1.2, 0.7))  # grille
    mb.box('wood', L(M, 2.0, 0, 1.95), shade(cab, 0.95), wear, size=(1.5, 2.3, 1.9))  # cab
    glass_panel(mb, M, [(2.76, -0.95, 2.05), (2.76, 0.95, 2.05), (2.76, 0.95, 2.7), (2.76, -0.95, 2.7)])
    mb.box('steel', L(M, -0.5, 0, 0.85), hex_rgb('#2a2a2a'), wear, size=(8.5, 1.0, 0.3))
    body_len, x0 = 5.8, -2.0
    mb.box('wood', L(M, x0, 0, 1.15), hex_rgb('#5a4030'), wear, size=(body_len, 2.4, 0.15))
    bands = [hex_rgb(c) for c in rng.pick([('#c62828', '#e0b020', '#1f5fa8'), ('#2e7d4f', '#e8e6df', '#c62828'), ('#1f5fa8', '#e0b020', '#e8e6df')])]
    for s_ in (-1, 1):  # tall plank sides, 2.2 m, in painted bands
        for j, c in enumerate(bands):
            mb.box('wood', L(M, x0, s_ * 1.2, 1.6 + j * 0.65), c, wear + 0.1, size=(body_len, 0.08, 0.6))
    for x in (x0 - body_len / 2, x0 + body_len / 2):
        for j, c in enumerate(bands):
            mb.box('wood', L(M, x, 0, 1.6 + j * 0.65), c, wear + 0.1, size=(0.08, 2.4, 0.6))
    load = load or rng.pick(['tomato', 'onion', 'yam'])
    col = {'tomato': '#c8321e', 'onion': '#c89a5a', 'yam': '#7a5a3a'}[load]
    for i in range(10):  # baskets or sacks heaped over the sides
        for j in range(4):
            x = x0 - body_len / 2 + 0.3 + i * (body_len - 0.6) / 9
            y = -0.95 + j * 0.63
            h = 3.25 + 0.25 * math.cos((i - 4.5) / 3)
            if load == 'tomato':
                parts.cyl(mb, 'cloth', L(M, x, y, h - 0.25), 0.3, 0.45, hex_rgb('#b08a4a'), 0.6, seg=8, r2=0.36)
                parts.cyl(mb, 'plastic', L(M, x, y, h + 0.2), 0.34, 0.12, hex_rgb(col), 0.2, seg=8, r2=0.2)
            else:
                mb.box('cloth', L(M, x, y, h), hex_rgb(col), 0.5, size=(0.55, 0.55, 0.5))
    for x in (3.5, -2.6, -3.9):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 1.0, 0.5, 0.3, cond)
    for s_ in (-1, 1):
        lamp(mb, M, 4.45, s_ * 0.7, 1.35, 0.2, 0.18, 'head')


# ---------------------------------------------------------------- trains (on the rail: base 0.5 m, standard gauge)
def bogie(mb, M, x, wear):
    mb.box('steel', L(M, x, 0, 0.75), hex_rgb('#2a2a2a'), wear, size=(2.6, 2.0, 0.4))
    for dx in (-0.9, 0.9):
        for s_ in (-1, 1):
            parts.cyl(mb, 'steel', L(M, x + dx, s_ * 0.72, 0.95, rx=math.pi / 2) @ Matrix.Translation((0, 0, -0.06)), 0.45, 0.12, hex_rgb('#3a3a3a'), wear, seg=12)


def commuter_car(mb, M, rng, cab=False, livery=None):
    """One car of an invented commuter train, 20 m: white with a coloured band, wide doors, a strip
    of windows; cab=True gives it a sloped driver's nose at +x."""
    wear = 0.25
    body, band = livery or (hex_rgb('#eceae4'), hex_rgb(rng.pick(['#1f5fa8', '#c62828', '#2e7d4f'])))
    Lc, Wc = 20.0, 3.0
    mb.box('carpaint', L(M, 0, 0, 2.5), body, wear, size=(Lc, Wc, 2.8))
    mb.box('carpaint', L(M, 0, 0, 1.25), band, wear, size=(Lc + 0.02, Wc + 0.02, 0.35))
    for s_ in (-1, 1):
        mb.box('glass', L(M, 0, s_ * (Wc / 2 + 0.01), 2.85), hex_rgb('#1c2830'), 0.1, size=(Lc - 2, 0.02, 0.9))
        for x in (-6.5, 0, 6.5):  # doors
            mb.box('steel', L(M, x, s_ * (Wc / 2 + 0.02), 2.3), shade(body, 0.8), wear, size=(1.6, 0.02, 2.2))
    mb.box('steel', L(M, 0, 0, 3.95), hex_rgb('#9a9a98'), wear, size=(Lc - 1, 2.4, 0.15))  # roof equipment
    if cab:
        mb.box('glass', L(M, Lc / 2 + 0.01, 0, 2.95), hex_rgb('#1c2830'), 0.1, size=(0.04, 2.4, 1.0))
        mb.box('carpaint', L(M, Lc / 2 + 0.02, 0, 1.25), band, wear, size=(0.04, 3.0, 0.35))
        for s_ in (-1, 1):
            lamp(mb, M, Lc / 2 + 0.03, s_ * 1.0, 1.7, 0.3, 0.15, 'head')
    for x in (-7, 7):
        bogie(mb, M, x, wear)


def diesel_loco(mb, M, rng, cond='battered'):
    """The old narrow-gauge diesel: a long hood with a cab at one end, green and yellow, rusted."""
    wear = WEAR[cond]
    col = hex_rgb(rng.pick(['#2f5a3a', '#7a2a1f', '#1f3f6a']))
    mb.box('carpaint', L(M, -1.0, 0, 2.3), col, wear, size=(10.0, 2.2, 2.2))  # hood
    mb.box('carpaint', L(M, 5.0, 0, 2.7), col, wear, size=(2.6, 2.8, 3.0))  # cab
    glass_panel(mb, M, [(6.31, -1.1, 3.0), (6.31, 1.1, 3.0), (6.31, 1.1, 3.8), (6.31, -1.1, 3.8)])
    for s_ in (-1, 1):
        mb.box('carpaint', L(M, -1.0, s_ * 1.11, 1.5), hex_rgb('#e0b020'), wear, size=(10.0, 0.02, 0.25))
    mb.box('steel', L(M, 0, 0, 1.1), hex_rgb('#2a2a2a'), wear, size=(13.5, 2.8, 0.4))
    parts.cyl(mb, 'steel', L(M, -3.0, 0, 3.4), 0.25, 0.6, hex_rgb('#2a2a2a'), wear, seg=8)  # exhaust
    lamp(mb, M, 6.33, 0, 3.95, 0.3, 0.2, 'head')
    for x in (-4.5, 3.5):
        bogie(mb, M, x, wear)


def old_coach(mb, M, rng, cond='battered'):
    """An old passenger coach, 18 m, cream over green, open windows, rust and fading."""
    wear = WEAR[cond]
    low, high = hex_rgb(rng.pick(['#2f5a3a', '#7a2a1f', '#1f3f6a'])), hex_rgb('#e8dcc0')
    mb.box('carpaint', L(M, 0, 0, 1.75), low, wear, size=(18.0, 2.9, 1.3))
    mb.box('carpaint', L(M, 0, 0, 3.0), high, wear, size=(18.0, 2.9, 1.2))
    for s_ in (-1, 1):
        for k in range(12):
            mb.box('glass', L(M, -8.0 + k * 1.45, s_ * 1.46, 3.0), hex_rgb('#14181c'), 0.2, size=(0.9, 0.02, 0.75))
    parts.cyl(mb, 'steel', L(M, -9.0, 0, 3.6, ry=math.pi / 2), 1.45, 18.0, hex_rgb('#6a6d6c'), wear, seg=12)  # curved roof
    for x in (-6.5, 6.5):
        bogie(mb, M, x, wear)


def wagon(mb, M, rng, cond='battered'):
    """An open freight wagon, 14 m, rusty, loaded or empty."""
    wear = WEAR[cond]
    col = hex_rgb(rng.pick(['#6b3a22', '#5a4636', '#4a4a48']))
    mb.box('steel', L(M, 0, 0, 1.3), hex_rgb('#2a2a2a'), wear, size=(14.0, 2.8, 0.3))
    for s_ in (-1, 1):
        mb.box('steel', L(M, 0, s_ * 1.4, 2.1), col, wear, size=(14.0, 0.08, 1.4))
    for x in (-7, 7):
        mb.box('steel', L(M, x, 0, 2.1), col, wear, size=(0.08, 2.8, 1.4))
    if rng.chance(0.6):
        mb.box('mud', L(M, 0, 0, 2.3), hex_rgb(rng.pick(['#d8c9a3', '#3a3a3a', '#8f8a80'])), 0.3, size=(13.6, 2.6, 1.0))
    for x in (-5, 5):
        bogie(mb, M, x, wear)


TRAIN = {'commuter': (commuter_car, 20.6), 'loco': (diesel_loco, 14.0), 'coach': (old_coach, 18.6), 'wagon': (wagon, 14.6)}


# ---------------------------------------------------------------- service vehicles, the molue, port machines
def truck_cab(mb, M, rng, x, col, cond, h=2.4):
    """A cab-over truck cab with its front at x, 2.4 m wide; returns the wear for the rest."""
    wear = WEAR[cond]
    mb.box('carpaint', L(M, x - 1.0, 0, 0.6 + h / 2), col, wear, size=(2.0, 2.4, h))
    glass_panel(mb, M, [(x + 0.01, -1.0, 1.7), (x + 0.01, 1.0, 1.7), (x + 0.01, 1.0, 0.6 + h - 0.25), (x + 0.01, -1.0, 0.6 + h - 0.25)])
    mb.box('plastic', L(M, x, 0, 0.75), hex_rgb('#1d1d1d'), 0.4, size=(0.08, 2.3, 0.5))
    for s_ in (-1, 1):
        lamp(mb, M, x + 0.02, s_ * 0.95, 0.95, 0.25, 0.15, 'head')
    return wear


def _beacons(mb, M, x, z, col):
    for s_ in (-0.5, 0.5):
        mb.box('emit', L(M, x, s_, z), hex_rgb(col), 0, size=(0.25, 0.3, 0.15))


def fire_engine(mb, M, rng, cond='worn'):
    """A red fire engine, 9 m: cab, lockers along the body, a ladder on the roof, blue beacons."""
    red, white = hex_rgb('#c62828'), hex_rgb('#f2efe6')
    wear = truck_cab(mb, M, rng, 4.4, red, cond, h=2.5)
    mb.box('carpaint', L(M, -0.8, 0, 1.75), red, wear, size=(6.4, 2.45, 2.5))
    for s_ in (-1, 1):
        mb.box('carpaint', L(M, -0.8, s_ * 1.23, 1.15), white, wear, size=(6.4, 0.02, 0.2))
        for k in range(4):  # locker doors
            mb.box('steel', L(M, -3.6 + k * 1.6, s_ * 1.235, 2.1), hex_rgb('#b8bcbf'), wear, size=(1.4, 0.02, 1.2))
    for s_ in (-0.55, 0.55):  # the ladder
        mb.box('steel', L(M, -0.8, s_, 3.15), hex_rgb('#c9ced2'), wear, size=(7.0, 0.08, 0.1))
    for k in range(18):
        mb.box('steel', L(M, -4.2 + k * 0.4, 0, 3.15), hex_rgb('#c9ced2'), wear, size=(0.05, 1.1, 0.05))
    _beacons(mb, M, 3.6, 3.15, '#2f6fff')
    for x in (3.4, -2.2, -3.4):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 1.05, 0.5, 0.3, cond)


def ambulance(mb, M, rng, cond='worn'):
    """A white ambulance van, 5.6 m, a high roof, a red-and-yellow band, blue beacons."""
    wear = WEAR[cond]
    white = hex_rgb('#f4f4f0')
    mb.box('carpaint', L(M, 1.9, 0, 1.15), white, wear, size=(1.2, 2.0, 1.1))  # bonnet
    mb.box('carpaint', L(M, -0.6, 0, 1.55), white, wear, size=(3.9, 2.05, 2.3))
    glass_panel(mb, M, [(1.31, -0.9, 1.75), (1.31, 0.9, 1.75), (1.31, 0.9, 2.4), (1.31, -0.9, 2.4)])
    for s_ in (-1, 1):
        for k, c in enumerate(('#c62828', '#e0b020')):
            mb.box('carpaint', L(M, 0.2, s_ * 1.03, 1.3 + k * 0.18), hex_rgb(c), wear, size=(5.0, 0.01, 0.15))
    _beacons(mb, M, 1.2, 2.75, '#2f6fff')
    for x in (1.9, -1.6):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 0.9, 0.36, 0.22, cond)
    for s_ in (-1, 1):
        lamp(mb, M, 2.51, s_ * 0.75, 0.9, 0.25, 0.15, 'head')


def refuse_compactor(mb, M, rng, cond='worn'):
    """A refuse compactor truck, 9 m: a boxy green-and-white body, the hopper at the back, bins on hooks."""
    green = hex_rgb(rng.pick(['#2e7d4f', '#1f5f3a']))
    wear = truck_cab(mb, M, rng, 4.4, hex_rgb('#f2efe6'), cond)
    mb.box('carpaint', L(M, -0.9, 0, 2.0), green, wear + 0.2, size=(5.6, 2.45, 2.6))
    mb.box('carpaint', L(M, -4.3, 0, 1.75), shade(green, 0.8), wear + 0.3, size=(1.4, 2.45, 2.2))  # hopper
    mb.box('steel', L(M, -5.05, 0, 1.0), hex_rgb('#3a3a3a'), wear + 0.3, size=(0.15, 2.2, 0.6))
    for s_ in (-1, 1):
        mb.box('carpaint', L(M, -0.9, s_ * 1.23, 2.0), hex_rgb('#f2efe6'), wear, size=(5.6, 0.02, 0.4))
    for x in (3.4, -2.0, -3.2):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 1.05, 0.5, 0.3, cond)


def cement_mixer(mb, M, rng, cond='battered'):
    """A cement mixer truck, 9 m: the striped drum tilted back on its frame."""
    wear = truck_cab(mb, M, rng, 4.4, hex_rgb(rng.pick(['#e8e6df', '#e0b020', '#c62828'])), cond)
    mb.box('steel', L(M, -0.6, 0, 1.0), hex_rgb('#2a2a2a'), wear, size=(8.0, 1.0, 0.3))
    drum = L(M, -1.2, 0, 2.3, ry=math.pi / 2 - 0.25)
    col = hex_rgb(rng.pick(['#e0b020', '#e8e6df', '#ff7a1a']))
    parts.cyl(mb, 'steel', drum @ Matrix.Translation((0, 0, -2.6)), 0.8, 1.2, col, wear, seg=16, r2=1.2)
    parts.cyl(mb, 'steel', drum @ Matrix.Translation((0, 0, -1.4)), 1.2, 2.2, col, wear, seg=16, r2=1.1)
    parts.cyl(mb, 'steel', drum @ Matrix.Translation((0, 0, 0.8)), 1.1, 1.4, col, wear, seg=16, r2=0.45)
    for k in range(3):  # stripes round the drum
        parts.cyl(mb, 'paint', drum @ Matrix.Translation((0, 0, -1.6 + k * 0.9)), 1.23, 0.2, hex_rgb('#c62828'), wear, seg=16)
    for x in (3.4, -1.8, -3.0):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 1.05, 0.5, 0.3, cond)


def water_tanker(mb, M, rng, cond='worn'):
    """A water tanker, 8.5 m: a blue round tank on a rigid truck, a tap and hose at the back."""
    wear = truck_cab(mb, M, rng, 4.2, hex_rgb(rng.pick(['#e8e6df', '#1f5fa8'])), cond)
    mb.box('steel', L(M, -0.6, 0, 1.0), hex_rgb('#2a2a2a'), wear, size=(7.8, 1.0, 0.3))
    tank = L(M, -4.3, 0, 2.15, ry=math.pi / 2)
    parts.cyl(mb, 'steel', tank, 1.05, 6.8, hex_rgb(rng.pick(['#1f5fa8', '#2f6fa6', '#e8e6df'])), wear, seg=18)
    parts.cyl(mb, 'steel', L(M, -4.5, 0, 1.3, ry=math.pi / 2), 0.08, 0.4, hex_rgb('#3a3a3a'), wear, seg=8)
    for x in (3.2, -2.2, -3.4):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 1.05, 0.5, 0.3, cond)


def molue(mb, M, rng, cond='wreck'):
    """The molue, the old big yellow bus of the city before the BRT: 10.5 m, a bonneted lorry-chassis
    body, two black bands, rows of open windows, the conductor's door always open. Retired; seen
    as a wreck at the roadside or as a church's bus."""
    wear = WEAR[cond]
    yel = hex_rgb('#e0a800' if cond != 'wreck' else '#b8901a')
    mb.box('carpaint', L(M, 4.6, 0, 1.15), yel, wear, size=(1.4, 1.9, 1.0))  # bonnet
    mb.box('carpaint', L(M, -0.9, 0, 1.95), yel, wear, size=(9.6, 2.5, 2.6))
    glass_panel(mb, M, [(3.91, -1.1, 2.1), (3.91, 1.1, 2.1), (3.91, 1.1, 3.0), (3.91, -1.1, 3.0)])
    for s_ in (-1, 1):
        for z in (1.2, 1.6):
            mb.box('carpaint', L(M, -0.9, s_ * 1.26, z), hex_rgb('#111111'), wear, size=(9.6, 0.01, 0.12))
        for k in range(9):
            mb.box('glass', L(M, -5.0 + k * 1.0, s_ * 1.26, 2.6), hex_rgb('#14181c'), 0.2, size=(0.75, 0.01, 0.7))
    if cond == 'wreck':
        for x in (4.4, -3.4):
            for s_ in (-1, 1):
                mb.box('concrete', L(M, x, s_ * 1.0, 0.3), hex_rgb('#8f8a80'), 0.8, size=(0.5, 0.4, 0.6))  # up on blocks
    else:
        for x in (4.4, -3.0, -4.2):
            for s_ in (-1, 1):
                wheel(mb, M, x, s_ * 1.05, 0.5, 0.3, cond)
        side_text(mb, M, -0.9, 1.27, 3.05, 'GOSPEL MISSION', 0.35, hex_rgb('#111111'))


def reach_stacker(mb, M, rng, cond='worn'):
    """A port reach stacker, 11 m: a yellow machine with a long telescopic boom and the container spreader."""
    wear = WEAR[cond]
    yel = hex_rgb('#e0b020')
    mb.box('carpaint', L(M, 0, 0, 1.4), yel, wear, size=(8.0, 3.6, 1.6))
    mb.box('carpaint', L(M, -1.2, 0, 2.9), yel, wear, size=(1.6, 1.4, 1.6))  # cab
    glass_panel(mb, M, [(-0.39, -0.6, 2.4), (-0.39, 0.6, 2.4), (-0.39, 0.6, 3.4), (-0.39, -0.6, 3.4)])
    a, b = L(M, -2.5, 0, 2.6).translation, L(M, 5.5, 0, 7.5).translation
    parts.bar(mb, 'steel', a, b, 0.7, yel, wear)  # the boom
    mb.box('steel', L(M, 6.0, 0, 7.0), hex_rgb('#2a2a2a'), wear, size=(1.0, 6.0, 0.4))  # spreader
    for x in (2.8, -2.8):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 1.6, 0.8, 0.6, cond)


def forklift(mb, M, rng, cond='worn'):
    """A big port forklift, 5 m: a counterweighted body, an open cab, the mast and forks."""
    wear = WEAR[cond]
    col = hex_rgb(rng.pick(['#e0b020', '#c62828', '#ff7a1a']))
    mb.box('carpaint', L(M, -0.4, 0, 1.0), col, wear, size=(3.2, 2.0, 1.2))
    for x, y in ((0.6, -0.8), (0.6, 0.8), (-1.6, -0.8), (-1.6, 0.8)):
        parts.bar(mb, 'steel', L(M, x, y, 1.6).translation, L(M, x, y, 3.2).translation, 0.08, hex_rgb('#2a2a2a'), wear)
    mb.box('steel', L(M, -0.5, 0, 3.25), hex_rgb('#2a2a2a'), wear, size=(2.4, 1.8, 0.1))
    for s_ in (-0.5, 0.5):
        mb.box('steel', L(M, 1.6, s_, 2.4), hex_rgb('#3a3a3a'), wear, size=(0.15, 0.15, 4.0))  # mast
        mb.box('steel', L(M, 2.3, s_, 0.5), hex_rgb('#3a3a3a'), wear, size=(1.4, 0.15, 0.08))  # forks
    for x in (0.8, -1.4):
        for s_ in (-1, 1):
            wheel(mb, M, x, s_ * 0.9, 0.45, 0.35, cond)


BUILDERS = {'danfo': danfo, 'korope': korope, 'brt': brt, 'keke': keke, 'okada': okada, 'car': car, 'police': police_pickup,
            'tipper': tipper, 'tanker': tanker, 'cart': pusher_cart, 'wheelbarrow': wheelbarrow, 'container': container_truck, 'lorry911': lorry_911,
            'fire': fire_engine, 'ambulance': ambulance, 'refuse': refuse_compactor, 'mixer': cement_mixer, 'water': water_tanker, 'molue': molue,
            'stacker': reach_stacker, 'forklift': forklift}
LENGTH = {'danfo': 4.8, 'korope': 3.6, 'brt': 12.2, 'keke': 2.8, 'okada': 2.1, 'car': 4.8, 'police': 5.3, 'tipper': 8.6, 'tanker': 11.5, 'cart': 3.6, 'wheelbarrow': 1.6, 'container': 17.2, 'lorry911': 8.9, 'fire': 9.0, 'ambulance': 5.6, 'refuse': 9.4, 'mixer': 9.0, 'water': 8.6, 'molue': 11.0, 'stacker': 11.0, 'forklift': 5.0}
# research-vehicles 8.6: shares of moving traffic by character and road class
MIX = {
    ('dense', 'main'): {'danfo': 26, 'korope': 4, 'keke': 5, 'okada': 5, 'car': 40, 'brt': 5, 'tipper': 6, 'tanker': 6, 'cart': 3, 'water': 1, 'refuse': 1, 'mixer': 1},
    ('dense', 'street'): {'danfo': 7, 'korope': 3, 'keke': 25, 'okada': 25, 'car': 30, 'tipper': 3, 'cart': 5, 'wheelbarrow': 2, 'water': 1.5, 'refuse': 0.5},
    ('old_island', 'main'): {'danfo': 20, 'car': 55, 'brt': 5, 'tanker': 5, 'tipper': 5, 'cart': 10},
    ('old_island', 'street'): {'keke': 5, 'okada': 5, 'car': 40, 'tipper': 5, 'cart': 40, 'wheelbarrow': 5},
    ('sprawl', 'main'): {'danfo': 20, 'korope': 5, 'keke': 15, 'okada': 15, 'car': 30, 'brt': 3, 'tipper': 7, 'tanker': 3, 'cart': 2},
    ('sprawl', 'street'): {'danfo': 2, 'korope': 3, 'keke': 30, 'okada': 30, 'car': 30, 'tipper': 3, 'cart': 2, 'mixer': 1.5, 'water': 2},
    ('elite', 'main'): {'danfo': 5, 'car': 80, 'brt': 5, 'tanker': 4, 'tipper': 4, 'okada': 2},
    ('elite', 'street'): {'car': 92, 'okada': 3, 'tipper': 5, 'mixer': 3, 'water': 3, 'refuse': 1},
    ('civic', 'main'): {'danfo': 15, 'car': 60, 'brt': 10, 'police': 2, 'tanker': 5, 'tipper': 5, 'cart': 3},
    ('civic', 'street'): {'danfo': 5, 'car': 70, 'police': 3, 'keke': 5, 'okada': 2, 'tipper': 5, 'cart': 3},
    ('port', 'main'): {'danfo': 10, 'car': 15, 'container': 35, 'tanker': 20, 'tipper': 15, 'brt': 3, 'okada': 2},
    ('port', 'street'): {'danfo': 10, 'car': 25, 'container': 15, 'tanker': 15, 'tipper': 20, 'okada': 5, 'keke': 5, 'cart': 5},
    ('waterfront', 'street'): {'danfo': 5, 'keke': 20, 'okada': 30, 'car': 20, 'tipper': 10, 'cart': 15},
}
COMMERCIAL = {'danfo', 'korope', 'keke', 'okada', 'tipper', 'tanker', 'brt', 'cart', 'container', 'lorry911', 'refuse', 'mixer', 'water', 'molue', 'stacker', 'forklift'}


def mix(ch, road):
    k = 'main' if road == 'main' else 'street'
    return MIX.get((ch, k)) or MIX.get(('dense', k))
