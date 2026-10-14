"""Boats on the lagoon: the ferries and water buses on the ferry routes, outboard canoes round Water
Town, and the sand-dredging barges. Research-transport (lagoon ferries, water buses), research-
housing (the stilt village's canoes), research-commerce (sand mining on the lagoon). All invented.
Every builder is (mb, M, rng) with M on the water line, the bow at +x."""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import hex_rgb, shade
from .kinds import T, canoe
from .people import person, seated_rider


def hull(mb, M, L, W, H, col, wear, bow=0.25):
    """A simple hull: straight sides, a raked bow over the last `bow` of the length."""
    xb = L / 2 - L * bow
    top = [(-L / 2, -W / 2), (xb, -W / 2), (L / 2, 0), (xb, W / 2), (-L / 2, W / 2)]
    bot = [(-L / 2 + 0.3, -W / 2 + 0.3), (xb, -W / 2 + 0.3), (L / 2 - 0.8, 0), (xb, W / 2 - 0.3), (-L / 2 + 0.3, W / 2 - 0.3)]
    tp = [M @ Vector((x, y, H)) for x, y in top]
    bp = [M @ Vector((x, y, -0.6)) for x, y in bot]
    mb.face(tp[::-1], 'paint', shade(col, 1.05), wear)  # deck
    for i in range(len(tp)):
        j = (i + 1) % len(tp)
        mb.face([bp[i], bp[j], tp[j], tp[i]], 'paint', col, wear)
    mb.face(bp, 'paint', shade(col, 0.6), wear)


def ferry(mb, M, rng):
    """A passenger ferry, 24 m: a white twin-deck cabin on a blue hull, windows all round, a wheelhouse."""
    wear = rng.between(0.2, 0.5)
    hull(mb, M, 24, 6.4, 1.2, hex_rgb(rng.pick(['#1f4f8a', '#2e7d4f', '#8e2f22'])), wear)
    for k, (Lc, z) in enumerate(((17, 1.2), (11, 3.6))):
        mb.box('paint', T(M, -1.5, 0, z + 1.2), hex_rgb('#f2efe6'), wear, size=(Lc, 5.6 - k * 0.6, 2.4))
        for s in (-1, 1):
            mb.box('glass', T(M, -1.5, s * (2.81 - k * 0.3), z + 1.4), hex_rgb('#1c2830'), 0.1, size=(Lc - 1.5, 0.02, 1.0))
    mb.box('paint', T(M, 2.5, 0, 6.6), hex_rgb('#f2efe6'), wear, size=(3, 3, 1.4))  # wheelhouse
    mb.box('glass', T(M, 4.01, 0, 6.7), hex_rgb('#1c2830'), 0.1, size=(0.02, 2.6, 0.8))
    parts.bar(mb, 'steel', T(M, 2.5, 0, 7.3).translation, T(M, 2.5, 0, 9.3).translation, 0.08, hex_rgb('#c9ced2'), 0.3)
    for s in (-1, 1):  # orange life rings
        parts.cyl(mb, 'plastic', T(M, -6, s * 2.82, 2.4) @ Matrix.Rotation(math.pi / 2, 4, 'X'), 0.35, 0.1, hex_rgb('#ff7a1a'), 0.2, seg=10)


def water_bus(mb, M, rng):
    """A small water bus, 13 m: an open-sided boat with a canopy roof on posts and rows of benches."""
    wear = rng.between(0.3, 0.6)
    col = hex_rgb(rng.pick(['#e0b020', '#2f6fa6', '#e8e6df', '#c62828']))
    hull(mb, M, 13, 3.4, 0.8, col, wear, bow=0.3)
    for x in (-5, -2.5, 0, 2.5):
        for s in (-1, 1):
            parts.bar(mb, 'steel', T(M, x, s * 1.5, 0.8).translation, T(M, x, s * 1.5, 2.8).translation, 0.06, hex_rgb('#c9ced2'), wear)
    mb.box('paint', T(M, -1.2, 0, 2.85), hex_rgb(rng.pick(['#1f5fa8', '#2e7d4f', '#f2efe6'])), wear, size=(9.0, 3.4, 0.12))
    for k in range(6):
        mb.box('wood', T(M, -5 + k * 1.4, 0, 1.2), hex_rgb('#5a4030'), wear, size=(0.4, 2.8, 0.1))
        for s in (-0.8, 0.8):
            if rng.chance(0.6):
                seated_rider(mb, T(M, -5 + k * 1.4, s, 0.75, math.pi / 2 * (1 if s > 0 else -1)), rng)
    parts.cyl(mb, 'steel', T(M, -6.8, 0, 0.3), 0.25, 1.0, hex_rgb('#2a2a2a'), wear, seg=8)  # the outboard


def outboard_canoe(mb, M, rng, people=True):
    """A long plank canoe with an outboard motor at the stern, a passenger or two and a load."""
    Lc = rng.between(6.5, 9.0)
    canoe(mb, M @ Matrix.Translation((0, 0, -0.15)), rng, length=Lc)
    parts.cyl(mb, 'steel', T(M, -Lc / 2 + 0.1, 0, -0.2), 0.12, 0.9, hex_rgb('#2a2a2a'), 0.5, seg=8)
    mb.box('plastic', T(M, -Lc / 2 + 0.1, 0, 0.75), hex_rgb(rng.pick(['#1d1d1d', '#c62828', '#1f5fa8'])), 0.4, size=(0.45, 0.35, 0.4))
    if people:
        seated_rider(mb, T(M, -Lc / 2 + 0.7, 0, 0.1), rng)
        for k in range(rng.randrange(0, 3)):
            seated_rider(mb, T(M, -Lc / 2 + 2.0 + k * 1.2, 0, 0.1), rng)
    if rng.chance(0.5):  # a load: sacks, jerrycans, fish baskets
        for k in range(rng.randrange(2, 6)):
            mb.box('cloth', T(M, Lc / 2 - 1.5 - k * 0.5, rng.between(-0.15, 0.15), 0.2), hex_rgb(rng.pick(['#d8c9a3', '#e0b020', '#2f6fa6', '#c8321e'])), 0.4, size=(0.45, 0.4, 0.35))


def dredger(mb, M, rng):
    """A sand-dredging barge, 22 m: a flat rusty barge with a pump house, a suction pipe down into
    the lagoon and a wet heap of sand, a smaller canoe tied alongside."""
    wear = rng.between(0.7, 0.95)
    hull(mb, M, 22, 7, 0.9, hex_rgb('#6b3a22'), wear, bow=0.08)
    mb.box('steel', T(M, -6.5, 0, 2.3), hex_rgb('#4a4a48'), wear, size=(4.0, 4.0, 2.8))  # pump house
    parts.cyl(mb, 'steel', T(M, -6.0, 1.0, 3.7), 0.25, 2.5, hex_rgb('#2a2a2a'), wear, seg=8)  # exhaust
    pipe0, pipe1 = T(M, 11.0, 0, 1.4).translation, T(M, 16.0, 0, -2.0).translation
    parts.bar(mb, 'steel', T(M, -4.5, 0, 1.4).translation, pipe0, 0.45, hex_rgb('#3a3a3a'), wear)
    parts.bar(mb, 'steel', pipe0, pipe1, 0.45, hex_rgb('#3a3a3a'), wear)
    for k in range(5):  # the heap of wet sand on deck
        mb.box('mud', T(M, 2.0 + (k - 2) * 2.0, 0, 1.4 + 0.6 * math.cos((k - 2) / 1.8)), hex_rgb('#c9b07a'), 0.3, size=(2.2, 5.4, 1.4))
    outboard_canoe(mb, T(M, 0, 4.4, 0), rng, people=False)


BUILDERS = {'ferry': ferry, 'water_bus': water_bus, 'canoe': outboard_canoe, 'dredger': dredger}
