"""Monuments and street landmarks, all invented (README rule zero): roundabout and corner statues
(a founder in agbada, a masquerade, a talking-drummer), welded scrap-metal sculpture, clock towers,
'welcome' arches over the main roads into a district, the port lighthouse and the big LED screens at
the main junctions. Research: docs/look/research-landmarks.md 4-9, 23, 24.

Every builder is (mb, M, rng, ...) with M a ground frame facing +x; city.py picks the sites
(monument_sites) from the main-road junctions, district entrances and the coast."""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import hex_rgb, shade
from .kinds import T
from .people import limb, sphere

BRONZE = hex_rgb('#5a4a2a')
WHITE = hex_rgb('#ece6d6')


def plinth(mb, M, rng, h=2.4, w=2.0, paint=None):
    """Stepped base, a tiled or painted die and a brass plaque on the front."""
    paint = paint or rng.pick([WHITE, hex_rgb('#e2d9c2'), hex_rgb('#cfc7b4')])
    z = 0
    for s, hh in ((w + 1.6, 0.3), (w + 0.8, 0.3)):
        mb.box('concrete', T(M, 0, 0, z + hh / 2), shade(paint, 0.92), 0.5, size=(s, s, hh))
        z += hh
    mb.box('paint', T(M, 0, 0, z + h / 2), paint, 0.45, size=(w, w, h))
    mb.box('steel', T(M, w / 2 + 0.01, 0, z + h * 0.55), hex_rgb('#c9a13b'), 0.3, size=(0.02, w * 0.6, h * 0.3))
    mb.box('concrete', T(M, 0, 0, z + h + 0.1), shade(paint, 0.9), 0.4, size=(w + 0.2, w + 0.2, 0.2))
    # the little railing and flower bed councils put round them
    r = w / 2 + 1.6
    for k in range(16):
        a = k / 16 * math.tau
        parts.bar(mb, 'steel', T(M, math.cos(a) * r, math.sin(a) * r, 0).translation, T(M, math.cos(a) * r, math.sin(a) * r, 0.8).translation, 0.05, hex_rgb('#2f5f2f'), 0.6)
    return z + h + 0.2


def founder(mb, M, rng, col=BRONZE, scale=2.2):
    """A standing elder statesman in agbada and fila, one arm raised to the crowd."""
    s = scale
    m = lambda x, y, z: (M @ Vector((x * s, y * s, z * s)))
    # the agbada falls wide from the shoulders as one draped cone
    parts.cyl(mb, 'steel', M @ Matrix.Scale(s, 4), 0.62, 1.42, col, 0.5, seg=16, r2=0.42)
    parts.cyl(mb, 'steel', M @ Matrix.Translation((0, 0, 1.42 * s)) @ Matrix.Scale(s, 4), 0.42, 0.06, col, 0.5, seg=16, r2=0.3)
    limb(mb, 'steel', m(0, 0.3, 1.38), m(0.12, 0.58, 1.72), 0.08 * s, 0.06 * s, col)       # raised arm
    limb(mb, 'steel', m(0.12, 0.58, 1.72), m(0.15, 0.62, 2.02), 0.06 * s, 0.05 * s, col)
    sphere(mb, 'steel', Matrix.Translation(m(0.15, 0.62, 2.06)), 0.06 * s, 0.06 * s, 0.07 * s, col, seg=8, rings=4)
    limb(mb, 'steel', m(0, -0.3, 1.38), m(0.18, -0.38, 0.95), 0.08 * s, 0.06 * s, col)     # the other holds a staff
    parts.bar(mb, 'steel', m(0.24, -0.4, 0.0), m(0.24, -0.4, 1.7), 0.04 * s, col, 0.5)
    limb(mb, 'steel', m(0, 0, 1.46), m(0, 0, 1.58), 0.07 * s, 0.07 * s, col)               # neck
    sphere(mb, 'steel', Matrix.Translation(m(0.02, 0, 1.7)), 0.12 * s, 0.11 * s, 0.14 * s, col, seg=10, rings=6)
    sphere(mb, 'steel', Matrix.Translation(m(0, 0, 1.8)), 0.13 * s, 0.13 * s, 0.09 * s, col, seg=10, rings=4, top=0.5)  # fila


def masquerade(mb, M, rng, scale=1.9):
    """An Eyo-like white-robed masquerade, invented: a tall cone of cloth to the ground, a flat
    wide hat, a staff; painted, not bronze, with coloured trims."""
    s = scale
    robe = hex_rgb('#f3f0e8')
    hat = rng.pick([hex_rgb('#1f4fa0'), hex_rgb('#c0392b'), hex_rgb('#2e7d32'), hex_rgb('#6a1b9a')])
    parts.cyl(mb, 'cloth', M @ Matrix.Scale(s, 4), 0.75, 1.75, robe, 0.3, seg=18, r2=0.22)
    for z, r in ((0.35, 0.68), (0.9, 0.5)):  # coloured bands at the hem and the waist
        parts.cyl(mb, 'paint', M @ Matrix.Translation((0, 0, z * s)) @ Matrix.Scale(s, 4), r + 0.01, 0.06, hat, 0.3, seg=18, r2=r - 0.02)
    sphere(mb, 'cloth', Matrix.Translation(M @ Vector((0, 0, 1.85 * s))), 0.2 * s, 0.2 * s, 0.22 * s, robe, seg=10, rings=6)
    parts.cyl(mb, 'paint', M @ Matrix.Translation((0, 0, 2.0 * s)) @ Matrix.Scale(s, 4), 0.55, 0.04, hat, 0.3, seg=18)  # wide hat
    parts.cyl(mb, 'paint', M @ Matrix.Translation((0, 0, 2.04 * s)) @ Matrix.Scale(s, 4), 0.2, 0.22, hat, 0.3, seg=12, r2=0.14)
    parts.bar(mb, 'wood', M @ Vector((0.35 * s, -0.4 * s, 0)), M @ Vector((0.35 * s, -0.4 * s, 2.3 * s)), 0.05 * s, hex_rgb('#4a3020'), 0.5)
    limb(mb, 'cloth', M @ Vector((0.05 * s, -0.18 * s, 1.55 * s)), M @ Vector((0.33 * s, -0.38 * s, 1.35 * s)), 0.07 * s, 0.06 * s, robe)


def drummer(mb, M, rng, col=BRONZE, scale=2.4):
    """A seated talking-drummer on a stool, the drum under the arm."""
    s = scale
    m = lambda x, y, z: (M @ Vector((x * s, y * s, z * s)))
    parts.cyl(mb, 'steel', M @ Matrix.Scale(s, 4), 0.22, 0.45, col, 0.5, seg=12)  # stool
    for y in (-0.12, 0.12):
        limb(mb, 'steel', m(0, y, 0.48), m(0.42, y, 0.48), 0.09 * s, 0.08 * s, col)  # thighs
        limb(mb, 'steel', m(0.42, y, 0.48), m(0.45, y, 0.05), 0.08 * s, 0.06 * s, col)
    limb(mb, 'steel', m(0, 0, 0.5), m(0, 0, 1.08), 0.2 * s, 0.17 * s, col)  # body in a buba
    sphere(mb, 'steel', Matrix.Translation(m(0.03, 0, 1.28)), 0.11 * s, 0.1 * s, 0.13 * s, col, seg=10, rings=6)
    drum = M @ Matrix.Translation((0.12 * s, -0.24 * s, 0.85 * s)) @ Matrix.Rotation(math.pi / 2, 4, 'Y')
    parts.cyl(mb, 'steel', drum @ Matrix.Translation((0, 0, -0.22 * s)), 0.11 * s, 0.22 * s, col, 0.5, seg=12, r2=0.07 * s)
    parts.cyl(mb, 'steel', drum, 0.07 * s, 0.22 * s, col, 0.5, seg=12, r2=0.11 * s)
    limb(mb, 'steel', m(0, -0.2, 1.0), m(0.14, -0.3, 0.88), 0.06 * s, 0.05 * s, col)
    limb(mb, 'steel', m(0, 0.2, 1.0), m(0.32, 0.0, 0.95), 0.06 * s, 0.05 * s, col)
    parts.bar(mb, 'wood', m(0.32, 0.0, 0.95), m(0.4, -0.2, 0.9), 0.02 * s, hex_rgb('#3a2a1a'), 0.4)  # the stick


def statue(mb, M, rng, kind=None):
    kind = kind or rng.pick(['founder', 'masquerade', 'drummer'])
    top = plinth(mb, M, rng, h=rng.between(2.0, 3.0))
    S = M @ Matrix.Translation((0, 0, top))
    {'founder': founder, 'masquerade': masquerade, 'drummer': drummer, 'horse_rider': horse_rider, 'hunter': hunter,
     'three_elders': three_elders, 'saxophonist': saxophonist}[kind](mb, S, rng)
    return kind


def sculpture(mb, M, rng):
    """Welded scrap: crossed bent I-beams, rings, a cog and bolted plates on a low base, rusty."""
    mb.box('concrete', T(M, 0, 0, 0.25), hex_rgb('#9c978c'), 0.6, size=(4.0, 4.0, 0.5))
    rust = [hex_rgb('#6a3a20'), hex_rgb('#4a4a48'), hex_rgb('#8a5a30'), hex_rgb('#2f5f7f')]
    for k in range(rng.randrange(4, 7)):  # leaning beams meeting high up
        a = k / 6 * math.tau + rng.between(-0.3, 0.3)
        base = T(M, math.cos(a) * 1.5, math.sin(a) * 1.5, 0.5).translation
        top = T(M, rng.between(-0.5, 0.5), rng.between(-0.5, 0.5), rng.between(5.5, 8.0)).translation
        parts.bar(mb, 'steel', base, top, rng.between(0.14, 0.24), rng.pick(rust), 0.9)
    for k in range(2):  # rings
        R = M @ Matrix.Translation((0, 0, 3.5 + k * 1.8)) @ Matrix.Rotation(rng.between(0, 1.2), 4, 'X') @ Matrix.Rotation(rng.between(0, 3), 4, 'Z')
        n = 16
        for i in range(n):
            a0, a1 = i / n * math.tau, (i + 1) / n * math.tau
            r = 1.4 - k * 0.4
            parts.bar(mb, 'steel', R @ Vector((math.cos(a0) * r, math.sin(a0) * r, 0)), R @ Vector((math.cos(a1) * r, math.sin(a1) * r, 0)), 0.12, rust[k + 1], 0.8)
    cog = M @ Matrix.Translation((0.8, 0, 2.2)) @ Matrix.Rotation(math.pi / 2, 4, 'Y')
    parts.cyl(mb, 'steel', cog, 0.9, 0.15, rust[0], 0.9, seg=24)
    for i in range(12):
        a = i / 12 * math.tau
        mb.box('steel', cog @ Matrix.Translation((math.cos(a) * 0.98, math.sin(a) * 0.98, 0.075)) @ Matrix.Rotation(a, 4, 'Z'), rust[0], 0.9, size=(0.22, 0.14, 0.15))


def clock_tower(mb, M, rng, h=None):
    """A square concrete clock tower: a tall shaft with a band at each floor, four white faces with
    hands, a pyramid cap; flowers round the foot."""
    h = h or rng.between(13, 18)
    wall = rng.pick([WHITE, hex_rgb('#e8d9b0'), hex_rgb('#d8c8a8')])
    band = rng.pick([hex_rgb('#2f6f4f'), hex_rgb('#8e3b2a'), hex_rgb('#1f4fa0')])
    mb.box('concrete', T(M, 0, 0, 0.3), shade(wall, 0.9), 0.5, size=(4.6, 4.6, 0.6))
    mb.box('paint', T(M, 0, 0, 0.6 + h / 2), wall, 0.55, size=(2.8, 2.8, h))
    for z in range(3, int(h), 4):
        mb.box('paint', T(M, 0, 0, 0.6 + z), band, 0.4, size=(3.0, 3.0, 0.25))
    head = 0.6 + h
    mb.box('paint', T(M, 0, 0, head + 1.4), wall, 0.5, size=(3.4, 3.4, 2.8))
    hour, minute = rng.between(0, math.tau), rng.between(0, math.tau)  # stopped, as often as not
    for k in range(4):
        F = M @ Matrix.Rotation(k * math.pi / 2, 4, 'Z') @ Matrix.Translation((1.71, 0, head + 1.4)) @ Matrix.Rotation(math.pi / 2, 4, 'Y')
        parts.cyl(mb, 'paint', F, 1.05, 0.04, hex_rgb('#f6f4ee'), 0.3, seg=24)
        parts.cyl(mb, 'paint', F @ Matrix.Translation((0, 0, 0.04)), 1.1, 0.02, hex_rgb('#1a1a1a'), 0.3, seg=24, caps=(False, False), r2=1.0)
        for ang, ln, t in ((hour, 0.55, 0.07), (minute, 0.85, 0.05)):
            d = F @ Vector((math.cos(ang) * ln, math.sin(ang) * ln, 0.08))
            parts.bar(mb, 'steel', F @ Vector((0, 0, 0.08)), d, t, hex_rgb('#111111'), 0.3)
    apex = T(M, 0, 0, head + 5.0).translation
    eave = [T(M, x, y, head + 2.8).translation for x, y in ((-1.9, -1.9), (1.9, -1.9), (1.9, 1.9), (-1.9, 1.9))]
    for k in range(4):  # pyramid cap
        mb.face([eave[k], eave[(k + 1) % 4], apex], 'paint', band, 0.5)


def lighthouse(mb, M, rng):
    """The port lighthouse on the mole: a tapering round tower in red and white bands, a gallery
    with railings, the lantern room and a keeper's hut."""
    h = 26.0
    segs = 8
    for k in range(segs):
        z0 = k * h / segs
        r0 = 3.2 - 1.2 * k / segs
        r1 = 3.2 - 1.2 * (k + 1) / segs
        parts.cyl(mb, 'paint', M @ Matrix.Translation((0, 0, z0)), r0, h / segs, hex_rgb('#c0392b') if k % 2 else hex_rgb('#f2efe6'), 0.55, seg=20, r2=r1)
    parts.cyl(mb, 'concrete', M @ Matrix.Translation((0, 0, h)), 2.8, 0.3, hex_rgb('#3a3a3a'), 0.5, seg=20)
    for k in range(20):
        a = k / 20 * math.tau
        parts.bar(mb, 'steel', T(M, math.cos(a) * 2.7, math.sin(a) * 2.7, h + 0.3).translation, T(M, math.cos(a) * 2.7, math.sin(a) * 2.7, h + 1.3).translation, 0.05, hex_rgb('#222222'), 0.5)
    parts.cyl(mb, 'glass_lit', M @ Matrix.Translation((0, 0, h + 0.3)), 1.5, 2.2, hex_rgb('#fff2b0'), 0, seg=16)
    parts.cyl(mb, 'paint', M @ Matrix.Translation((0, 0, h + 2.5)), 1.7, 1.2, hex_rgb('#1a1a1a'), 0.4, seg=16, r2=0.2)
    mb.box('paint', T(M, 6, 0, 1.5), hex_rgb('#f2efe6'), 0.6, size=(5, 4, 3))  # keeper's hut
    mb.box('zinc', T(M, 6, 0, 3.1), hex_rgb('#9a9a9a'), 0.9, size=(5.6, 4.6, 0.15))
    for x in (-4, 4):  # rocks round the foot
        for y in (-4, 4):
            parts.cyl(mb, 'concrete', M @ Matrix.Translation((x + rng.between(-1, 1), y + rng.between(-1, 1), -0.5)), rng.between(1.0, 1.8), 1.2, hex_rgb('#6a6a62'), 0.9, seg=6, r2=0.6)


def arch(mb, M, rng, span, name, ch):
    """The 'welcome' arch over a main road into a district: two pylons, a deep beam with the
    district's (invented) name, a crest in the middle; clear height 6.5 m for lorries. M sits on
    the road's centreline with x along the road."""
    wall = rng.pick([WHITE, hex_rgb('#e8d9b0'), hex_rgb('#f0e0c0')])
    band = rng.pick([hex_rgb('#2f6f4f'), hex_rgb('#8e3b2a'), hex_rgb('#1f4fa0'), hex_rgb('#6a1b9a')])
    half = span / 2 + 1.2
    for s in (-1, 1):
        mb.box('paint', T(M, 0, s * half, 4.4), wall, 0.5, size=(2.0, 2.0, 8.8))
        mb.box('paint', T(M, 0, s * half, 0.4), band, 0.5, size=(2.4, 2.4, 0.8))
        mb.box('paint', T(M, 0, s * half, 9.2), band, 0.4, size=(2.4, 2.4, 0.8))
    mb.box('paint', T(M, 0, 0, 7.6), wall, 0.5, size=(1.4, half * 2, 2.2))
    mb.box('paint', T(M, 0, 0, 8.85), band, 0.4, size=(1.6, half * 2 + 0.6, 0.3))
    parts.cyl(mb, 'paint', T(M, 0, 0, 8.7), 1.6, 0.6, band, 0.4, seg=16, r2=1.2)  # crest
    parts.cyl(mb, 'steel', T(M, 0, 0, 9.3), 0.9, 0.3, hex_rgb('#c9a13b'), 0.3, seg=12)
    for side in (1, -1):  # the lettering on both faces, read by traffic coming each way
        F = M @ Matrix.Translation((side * 0.72, 0, 7.6)) @ Matrix.Rotation(-side * math.pi / 2 + math.pi, 4, 'Z')  # text reads from the side it faces
        parts.text(mb, 'paint', F, 'WELCOME TO ' + name.upper(), 0.9, hex_rgb('#1a1a1a'), depth=0.04, max_w=half * 1.7)


def led_board(mb, M, rng):
    """A big LED screen on a steel pylon at a junction: lit panels in blocks of colour (adverts
    without brands), a catwalk, a cabinet and the generator at its foot."""
    W, H = rng.pick([(10, 5), (12, 6), (8, 4)])
    z0 = rng.between(7, 10)
    parts.cyl(mb, 'steel', M, 0.5, z0, hex_rgb('#5a5a5a'), 0.6, seg=12)
    mb.box('steel', T(M, 0, 0, z0 + H / 2), hex_rgb('#1a1a1a'), 0.5, size=(0.6, W + 0.4, H + 0.4))
    cols = [hex_rgb(c) for c in ('#ff3b30', '#ffd60a', '#30d158', '#0a84ff', '#bf5af2', '#ff9f0a', '#ffffff')]
    for side in (1, -1):
        nx, ny = rng.randrange(2, 4), rng.randrange(1, 3)
        for i in range(nx):
            for j in range(ny):
                mb.box('emit', T(M, side * 0.31, -W / 2 + (i + 0.5) * W / nx, z0 + (j + 0.5) * H / ny), rng.pick(cols), 0, size=(0.02, W / nx - 0.08, H / ny - 0.08))
    mb.box('steel', T(M, 0.9, 0, z0 - 0.1), hex_rgb('#3a3a3a'), 0.7, size=(1.0, W, 0.08))  # catwalk
    mb.box('steel', T(M, 1.2, 0, 0.8), hex_rgb('#c8c8c0'), 0.6, size=(1.0, 0.8, 1.6))
    mb.box('steel', T(M, -1.8, 0.6, 0.45), hex_rgb('#c9a13b'), 0.7, size=(1.6, 0.9, 0.9))  # its generator


def horse(mb, M, col, scale=1.0, mat='steel', rearing=False):
    """A horse, standing (or rearing), facing +x; M at the ground under its middle."""
    s = scale
    v = lambda x, y, z: M @ Vector((x * s, y * s, z * s))
    lift = 0.35 if rearing else 0.0
    sphere(mb, mat, Matrix.Translation(v(0, 0, 1.45 + lift * 0.5)), 0.85 * s, 0.38 * s, 0.42 * s, col, seg=10, rings=6)  # barrel
    limb(mb, mat, v(0.6, 0, 1.6 + lift), v(1.05, 0, 2.25 + lift * 1.5), 0.22 * s, 0.15 * s, col)  # neck
    sphere(mb, mat, Matrix.Translation(v(1.25, 0, 2.2 + lift * 1.5)), 0.35 * s, 0.13 * s, 0.15 * s, col, seg=8, rings=5)  # head
    for x, front in ((0.55, True), (-0.55, False)):
        for y in (-0.18, 0.18):
            if rearing and front:
                limb(mb, mat, v(x, y, 1.3 + lift), v(x + 0.35, y, 1.0 + lift), 0.09 * s, 0.07 * s, col)
            else:
                limb(mb, mat, v(x, y, 1.25), v(x + (0.05 if front else -0.05), y, 0.05), 0.09 * s, 0.06 * s, col)
    limb(mb, mat, v(-0.85, 0, 1.55), v(-1.15, 0, 0.9), 0.07 * s, 0.03 * s, col)  # tail


def horse_rider(mb, M, rng, col=BRONZE, scale=1.7):
    """A rider on a horse, sword raised: the equestrian statue of the big squares and roundabouts."""
    horse(mb, M, col, scale, rearing=rng.chance(0.4))
    s = scale
    v = lambda x, y, z: M @ Vector((x * s, y * s, z * s))
    limb(mb, 'steel', v(0, 0, 1.85), v(0.05, 0, 2.55), 0.2 * s, 0.17 * s, col)  # body
    sphere(mb, 'steel', Matrix.Translation(v(0.08, 0, 2.75)), 0.11 * s, 0.1 * s, 0.13 * s, col, seg=8, rings=5)
    limb(mb, 'steel', v(0.05, 0.18, 2.45), v(0.2, 0.3, 2.95), 0.06 * s, 0.05 * s, col)  # sword arm
    parts.bar(mb, 'steel', v(0.2, 0.3, 2.95), v(0.3, 0.32, 3.7), 0.03 * s, col, 0.4)
    for y in (-0.22, 0.22):
        limb(mb, 'steel', v(0, y, 1.85), v(0.1, y * 1.3, 1.3), 0.08 * s, 0.07 * s, col)  # legs astride


def hunter(mb, M, rng, col=BRONZE, scale=2.0):
    """A hunter in a cap and smock with a long dane gun on his shoulder, his dog at his heel."""
    s = scale
    v = lambda x, y, z: M @ Vector((x * s, y * s, z * s))
    for y in (-0.1, 0.1):
        limb(mb, 'steel', v(0, y, 0.85), v(0.05 if y > 0 else -0.08, y, 0.0), 0.08 * s, 0.06 * s, col)
    parts.cyl(mb, 'steel', M @ Matrix.Translation((0, 0, 0.75 * s)) @ Matrix.Scale(s, 4), 0.28, 0.75, col, 0.5, seg=12, r2=0.2)  # smock
    sphere(mb, 'steel', Matrix.Translation(v(0.02, 0, 1.65)), 0.11 * s, 0.1 * s, 0.13 * s, col, seg=8, rings=5)
    parts.cyl(mb, 'steel', M @ Matrix.Translation((0.02 * s, 0, 1.74 * s)) @ Matrix.Scale(s, 4), 0.12, 0.12, col, 0.5, seg=10, r2=0.05)  # cap
    limb(mb, 'steel', v(0, 0.22, 1.45), v(0.15, 0.25, 1.62), 0.06 * s, 0.05 * s, col)
    parts.bar(mb, 'steel', v(-0.5, 0.22, 1.3), v(0.9, 0.22, 1.85), 0.03 * s, col, 0.4)  # the long gun on his shoulder
    dog = M @ Matrix.Translation((0.55 * s, -0.4 * s, 0))
    sphere(mb, 'steel', Matrix.Translation(dog @ Vector((0, 0, 0.45 * s))), 0.35 * s, 0.13 * s, 0.15 * s, col, seg=8, rings=5)
    sphere(mb, 'steel', Matrix.Translation(dog @ Vector((0.4 * s, 0, 0.62 * s))), 0.13 * s, 0.08 * s, 0.09 * s, col, seg=8, rings=5)
    for x in (0.22, -0.22):
        for y in (-0.08, 0.08):
            limb(mb, 'steel', dog @ Vector((x * s, y * s, 0.4 * s)), dog @ Vector((x * s, y * s, 0)), 0.04 * s, 0.03 * s, col)


def beach_arch(mb, M, rng):
    """A memorial arch on the beach, facing the sea: two concrete legs and a deep lintel, a
    plaque, and chains cast in relief on the legs. Research-landmarks 26, invented."""
    conc = hex_rgb('#d8d4cc')
    for s_ in (-1, 1):
        mb.box('concrete', T(M, 0, s_ * 4.5, 5.0), conc, 0.5, size=(2.0, 2.0, 10.0))
        for k in range(8):  # chain links in relief
            mb.box('steel', T(M, 1.02, s_ * 4.5, 1.5 + k * 1.0), hex_rgb('#4a4a48'), 0.6, size=(0.1, 0.6 if k % 2 else 0.25, 0.7))
    mb.box('concrete', T(M, 0, 0, 10.8), conc, 0.5, size=(2.4, 11.0, 1.6))
    mb.box('steel', T(M, 1.21, 0, 10.8), hex_rgb('#c9a13b'), 0.3, size=(0.02, 5.0, 0.8))  # plaque
    mb.box('concrete', T(M, 0, 0, 0.15), shade(conc, 0.9), 0.5, size=(4.0, 13.0, 0.3))


def mural_wall(mb, M, rng, length=None):
    """A free-standing painted wall, 20-30 m long, 4 m high: bold shapes, faces and bands in a
    few strong colours on both sides (research-landmarks 25)."""
    from .structures import MURAL_PALETTES
    L = length or rng.between(20, 30)
    pal = [hex_rgb(x) for x in rng.pick(MURAL_PALETTES)]
    mb.box('block', T(M, 0, 0, 2.0), hex_rgb('#d8d4cc'), 0.5, size=(L, 0.3, 4.0))
    for s_ in (-1, 1):
        x = -L / 2
        while x < L / 2:  # broad colour fields
            w = min(L / 2 - x, rng.between(2.0, 5.0))
            mb.box('paint', T(M, x + w / 2, s_ * 0.16, 2.0), rng.pick(pal), 0.3, size=(w, 0.01, 3.8))
            x += w
        for _ in range(int(L / 3)):  # shapes over them: discs, diamonds, a face in profile
            cx, cz, r = rng.between(-L / 2 + 1, L / 2 - 1), rng.between(1.0, 3.2), rng.between(0.4, 1.4)
            D = T(M, cx, s_ * 0.175, cz) @ Matrix.Rotation(-s_ * math.pi / 2, 4, 'X')
            if rng.chance(0.5):
                parts.cyl(mb, 'paint', D, r, 0.01, rng.pick(pal), 0.2, seg=14)
            else:
                mb.box('paint', D @ Matrix.Rotation(math.pi / 4, 4, 'Z'), rng.pick(pal), 0.2, size=(r * 1.4, r * 1.4, 0.01))
    mb.box('concrete', T(M, 0, 0, 4.05), hex_rgb('#b8b2a6'), 0.5, size=(L + 0.2, 0.4, 0.15))  # coping


def billboard(mb, M, rng):
    """A printed billboard on a unipole, 12 x 4 m, both faces: a poster of colour fields and a
    bold line of type; no brand (rule zero), invented messages."""
    z0 = rng.between(9, 13)
    parts.cyl(mb, 'steel', M, 0.55, z0, hex_rgb('#7a7d80'), 0.6, seg=12)
    mb.box('steel', T(M, 0, 0, z0 + 2.0), hex_rgb('#3a3a3a'), 0.5, size=(0.5, 12.4, 4.4))
    msgs = ['GIDI FM 101.1', 'SAVE SMALL SMALL', 'NEW ESTATE NOW SELLING', 'FRESH BREAD DAILY', 'WATER IS LIFE', 'MOVE GIDI FORWARD', 'BIG SALE THIS WEEK']
    pals = [('#f2c230', '#1d1d1d', '#c62828'), ('#1f5fa8', '#ffffff', '#f2c230'), ('#2e7d4f', '#ffffff', '#ff7a1a'), ('#c62828', '#ffffff', '#1d1d1d')]
    for s_ in (-1, 1):
        bg, fg, acc = (hex_rgb(c) for c in rng.pick(pals))
        F = T(M, s_ * 0.27, 0, z0 + 2.0) @ Matrix.Rotation(-s_ * math.pi / 2, 4, 'Z')  # a frame facing outwards
        mb.box('paint', F @ Matrix.Translation((0, 0.01, 0)), bg, 0.3, size=(12.0, 0.02, 4.0))
        mb.box('paint', F @ Matrix.Translation((-3.0, 0.025, -0.9)), acc, 0.3, size=(5.5, 0.01, 1.4))
        parts.cyl(mb, 'paint', F @ Matrix.Translation((4.0, 0.025, 0.3)) @ Matrix.Rotation(-math.pi / 2, 4, 'X'), 1.4, 0.01, acc, 0.2, seg=16)
        parts.text(mb, 'paint', F @ Matrix.Rotation(math.pi, 4, 'Z') @ Matrix.Translation((1.2, -0.035, 0.9)), rng.pick(msgs), 0.7, fg, depth=0.02, max_w=8.0)
    mb.box('steel', T(M, 0.9, 0, z0 - 0.1), hex_rgb('#3a3a3a'), 0.6, size=(1.0, 12.0, 0.08))  # catwalk


def the_reach(mb, M, rng, scale=2.4):
    """The Reach: a painted sculpture group after the owner's own artwork. A woman in a yellow
    wrapper and a green spotted blouse, beaded headgear, reclines on a dark rock and reaches out
    with a striped sleeve. A white-robed Eyo-style masquerade, invented, floats in to meet her: wide
    flat hat, black stripes on the robe, his robe streaming behind him. He holds a long staff, which
    plants on the plinth and holds him up. Their fingertips almost touch. About 14 m across; M at
    the plinth's middle, the woman at -x."""
    s = scale
    v = lambda x, y, z: M @ Vector((x * s, y * s, z * s))
    skin = hex_rgb('#6b3e26')
    yellow, green, white, ink = hex_rgb('#e8c43a'), hex_rgb('#2f7a3a'), hex_rgb('#f4f1e6'), hex_rgb('#1d1d1d')
    # the plinth and the rock she lies on
    mb.box('concrete', T(M, 0, 0, 0.3), hex_rgb('#d8d4cc'), 0.4, size=(7.2 * s, 3.0 * s, 0.6))
    mb.box('steel', T(M, 0, -1.5 * s - 0.01, 0.3), hex_rgb('#c9a13b'), 0.3, size=(2.0 * s, 0.02, 0.35))  # plaque
    rock = hex_rgb('#3a3346')
    for k, (x, y, r, h) in enumerate(((-2.3, 0, 1.3, 1.15), (-1.3, 0.15, 1.0, 0.9), (-3.1, -0.3, 0.85, 1.0), (-0.6, -0.1, 0.7, 0.6))):
        sphere(mb, 'concrete', Matrix.Translation(v(x, y, 0.0)), r * s, r * 0.75 * s, h * s, rock, seg=12, rings=6)  # sunk into the plinth
    # her: legs under the wrapper along the rock, the body leaning back, the head tilted
    limb(mb, 'paint', v(-2.2, 0, 1.25), v(-0.5, 0.05, 1.0), 0.42 * s, 0.22 * s, yellow)   # the wrapper over her legs
    sphere(mb, 'paint', Matrix.Translation(v(-1.4, 0.05, 1.05)), 1.0 * s, 0.55 * s, 0.32 * s, yellow, seg=10, rings=5)  # its fall over the rock
    limb(mb, 'paint', v(-2.25, 0, 1.25), v(-2.7, 0, 2.0), 0.3 * s, 0.24 * s, green)       # the blouse
    for k in range(6):  # its white spots
        q = v(-2.35 - k * 0.06, rng.between(-0.24, 0.24), 1.45 + k * 0.09)
        sphere(mb, 'paint', Matrix.Translation(q), 0.03 * s, 0.03 * s, 0.03 * s, white, seg=6, rings=3)
    sphere(mb, 'paint', Matrix.Translation(v(-2.82, 0, 2.3)), 0.13 * s, 0.12 * s, 0.16 * s, skin, seg=10, rings=6)  # her head
    for k, c in enumerate(('#c62828', '#f2c230', '#1f5fa8', '#2e7d4f', '#ff7a1a')):  # beaded headgear, rising
        sphere(mb, 'paint', Matrix.Translation(v(-2.88 - k * 0.025, 0, 2.45 + k * 0.07)), (0.12 - k * 0.015) * s, (0.12 - k * 0.015) * s, 0.05 * s, hex_rgb(c), seg=8, rings=3)
    # the reaching arm, the sleeve striped
    sh, el, wr = (-2.55, 0.22, 2.0), (-1.85, 0.3, 2.25), (-1.15, 0.32, 2.42)
    for (a0, a1), c in zip(((sh, el), (el, wr)), (('#2f7a3a', '#f2c230'), ('#1f5fa8', '#f2c230'))):
        for k in range(4):
            t0, t1 = k / 4, (k + 1) / 4
            pa = tuple(a0[i] + (a1[i] - a0[i]) * t0 for i in range(3))
            pb = tuple(a0[i] + (a1[i] - a0[i]) * t1 for i in range(3))
            limb(mb, 'paint', v(*pa), v(*pb), 0.075 * s, 0.07 * s, hex_rgb(c[k % 2]))
    limb(mb, 'paint', v(*wr), v(-0.98, 0.33, 2.47), 0.05 * s, 0.035 * s, skin)  # her hand, the finger out
    limb(mb, 'paint', v(-2.65, -0.24, 1.95), v(-2.85, -0.45, 1.35), 0.07 * s, 0.06 * s, green)  # the other arm, resting
    # him: the Eyo, floating in from the right, leaning down to her
    limb(mb, 'paint', v(1.0, 0, 3.25), v(2.6, 0.1, 2.35), 0.28 * s, 0.9 * s, white)  # the robe streaming back
    limb(mb, 'paint', v(1.6, 0.1, 2.9), v(3.2, -0.2, 2.6), 0.5 * s, 0.25 * s, white)  # a flying fold
    limb(mb, 'paint', v(1.5, -0.1, 2.7), v(2.9, 0.3, 1.9), 0.4 * s, 0.15 * s, white)
    for k in range(4):  # the black stripes across the robe
        t = 0.15 + k * 0.2
        c = v(1.0 + 1.6 * t, 0, 3.25 - 0.9 * t)
        sphere(mb, 'paint', Matrix.Translation(c), 0.06 * s, (0.3 + 0.6 * t) * s * 1.03, (0.3 + 0.6 * t) * s * 1.03, ink, seg=10, rings=4)
    sphere(mb, 'paint', Matrix.Translation(v(0.82, 0, 3.55)), 0.15 * s, 0.14 * s, 0.17 * s, white, seg=10, rings=6)  # the veiled head
    parts.cyl(mb, 'paint', M @ Matrix.Translation(v(0.8, 0, 3.66) - M.translation) @ Matrix.Scale(s, 4), 0.48, 0.03, white, 0.2, seg=18)  # the wide flat hat
    parts.cyl(mb, 'paint', M @ Matrix.Translation(v(0.8, 0, 3.69) - M.translation) @ Matrix.Scale(s, 4), 0.17, 0.2, white, 0.2, seg=12, r2=0.12)
    sphere(mb, 'paint', Matrix.Translation(v(0.8, -0.18, 3.8)), 0.05 * s, 0.01 * s, 0.05 * s, ink, seg=6, rings=3)  # the emblem on the crown
    # his reaching arm: the fingertip stops a hand's breadth short of hers
    limb(mb, 'paint', v(0.9, 0.25, 3.25), v(0.2, 0.32, 2.85), 0.09 * s, 0.07 * s, white)
    limb(mb, 'paint', v(0.2, 0.32, 2.85), v(-0.62, 0.34, 2.52), 0.07 * s, 0.05 * s, white)
    limb(mb, 'paint', v(-0.62, 0.34, 2.52), v(-0.8, 0.34, 2.49), 0.045 * s, 0.03 * s, skin)
    # the staff, held high in his other hand and planted on the plinth: it holds him up
    limb(mb, 'paint', v(1.1, -0.25, 3.2), v(1.75, -0.32, 3.45), 0.08 * s, 0.06 * s, white)
    parts.bar(mb, 'steel', v(2.35, -0.32, 4.35), v(0.35, -0.32, 0.05), 0.07 * s, hex_rgb('#c9c4ba'), 0.3)


def three_elders(mb, M, rng, col=BRONZE, scale=1.7):
    """Three elders in agbada and caps standing together on one plinth, the middle one a little
    forward with a staff: an invented group in the spirit of the city's statues of elders."""
    for k, (x, y, rz) in enumerate(((0.35, 0, 0), (-0.25, -1.05, 0.25), (-0.25, 1.05, -0.25))):
        S = M @ Matrix.Translation((x * scale, y * scale, 0)) @ Matrix.Rotation(rz, 4, 'Z')
        s = scale
        parts.cyl(mb, 'steel', S @ Matrix.Scale(s, 4), 0.42, 1.45, col, 0.5, seg=14, r2=0.26)  # the agbada
        parts.cyl(mb, 'steel', S @ Matrix.Translation((0, 0, 1.45 * s)) @ Matrix.Scale(s, 4), 0.26, 0.08, col, 0.5, seg=14, r2=0.07)  # shoulders to the neck
        sphere(mb, 'steel', Matrix.Translation(S @ Vector((0, 0, 1.62 * s))), 0.11 * s, 0.1 * s, 0.13 * s, col, seg=10, rings=6)
        parts.cyl(mb, 'steel', S @ Matrix.Translation((0, 0, 1.7 * s)) @ Matrix.Scale(s, 4), 0.12, 0.15, col, 0.5, seg=10, r2=0.09)  # cap
        if k == 0:
            parts.bar(mb, 'steel', S @ Vector((0.3 * s, -0.35 * s, 0)), S @ Vector((0.3 * s, -0.35 * s, 1.9 * s)), 0.035 * s, col, 0.5)


def saxophonist(mb, M, rng, col=BRONZE, scale=2.2):
    """A musician mid-solo, an invented bronze in the spirit of the city's music: open shirt, wide
    trousers, the saxophone raised, one knee bent into the note."""
    s = scale
    v = lambda x, y, z: M @ Vector((x * s, y * s, z * s))
    limb(mb, 'steel', v(0, -0.1, 0.9), v(0.05, -0.12, 0.0), 0.09 * s, 0.07 * s, col)
    limb(mb, 'steel', v(0, 0.1, 0.9), v(0.18, 0.14, 0.45), 0.09 * s, 0.08 * s, col)  # the bent knee
    limb(mb, 'steel', v(0.18, 0.14, 0.45), v(0.1, 0.16, 0.0), 0.08 * s, 0.06 * s, col)
    limb(mb, 'steel', v(0, 0, 0.95), v(-0.06, 0, 1.5), 0.17 * s, 0.15 * s, col)  # body, leaning back
    sphere(mb, 'steel', Matrix.Translation(v(-0.06, 0, 1.68)), 0.11 * s, 0.1 * s, 0.13 * s, col, seg=10, rings=6)
    limb(mb, 'steel', v(-0.05, 0.18, 1.45), v(0.15, 0.2, 1.3), 0.05 * s, 0.045 * s, col)
    limb(mb, 'steel', v(-0.05, -0.18, 1.45), v(0.18, -0.1, 1.15), 0.05 * s, 0.045 * s, col)
    parts.bar(mb, 'steel', v(0.02, 0.0, 1.62), v(0.2, 0.05, 1.0), 0.035 * s, hex_rgb('#c9a13b'), 0.3)  # the sax
    parts.cyl(mb, 'steel', M @ Matrix.Translation(v(0.2, 0.05, 1.0) - M.translation) @ Matrix.Scale(s, 4), 0.06, 0.18, hex_rgb('#c9a13b'), 0.3, seg=10, r2=0.1)


BUILDERS = {'statue': statue, 'sculpture': sculpture, 'clock_tower': clock_tower, 'lighthouse': lighthouse, 'led_board': led_board,
            'beach_arch': beach_arch, 'mural_wall': mural_wall, 'billboard': billboard, 'the_reach': the_reach}

# what each district character puts on its junction corners (research-landmarks 4-9, 24)
JUNCTION = {
    'old_island': ['statue:masquerade', 'statue:horse_rider', 'clock_tower', 'led_board'],
    'civic': ['statue:saxophonist', 'statue:horse_rider', 'clock_tower', 'led_board'],
    'elite': ['statue:three_elders', 'sculpture', 'led_board'],
    'dense': ['led_board', 'statue:founder', 'statue:drummer', 'led_board'],
    'sprawl': ['led_board', 'statue:founder', 'clock_tower'],
    'waterfront': ['statue:masquerade', 'statue:drummer'],
    'port': ['led_board', 'sculpture'],
}
