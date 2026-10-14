"""Named landmarks: a place on the map that needs a model of its own, by its name.

When a district brings a named landmark, give it a builder here:
- a civic plot of type 'landmark'
- a named place on the map that should take over a plot
- anything else scripts/audit3d.py flags

Until then it is built as a plain civic hall, never as something else's model, and the audit lists
it under M3. Invented designs from patterns only (README rule zero, docs/look/research-landmarks.md).

A place on the map (a POI) named here takes over the nearest civic plot of its own type within
300 m (or the nearest plain building plot), so its model stands on a real plot of the 2D map.
"""
import math

from mathutils import Matrix, Vector

from . import parts, places
from .blocks import block, dome, minaret, perimeter, faces
from .core import MeshBuilder, centroid, hex_rgb, offset, shade
from .kinds import T, footprint


def crown_hall(a, rng, collection=None):
    """The Crown Hall: a national cultural hall shaped like a ceremonial cap. A round drum stands
    on a podium. A brim of folded concrete leans out all round at mid height, and a raised crown
    drum with fins sits on top. Grey-white concrete, a band of dark glass. Research-landmarks 3
    (a cap-shaped national hall), invented."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    R = min(L, W) * 0.42
    wear = rng.between(0.35, 0.6)
    conc, dark = hex_rgb('#d8d4cc'), hex_rgb('#24343e')
    seg = 32
    C = Matrix.Translation((c[0], c[1], 0))
    parts.cyl(mb, 'concrete', C, R * 1.15, 1.2, shade(conc, 0.9), wear, seg=seg)  # podium
    for k in range(3):  # steps up to it
        parts.cyl(mb, 'concrete', C, R * 1.15 + 1.6 - k * 0.5, 0.4 * (k + 1), shade(conc, 0.85), wear, seg=seg)
    parts.cyl(mb, 'concrete', C @ Matrix.Translation((0, 0, 1.2)), R * 0.82, 7.0, conc, wear, seg=seg)  # lower drum
    parts.cyl(mb, 'glass', C @ Matrix.Translation((0, 0, 8.2)), R * 0.8, 2.2, dark, 0.1, seg=seg)  # glass band
    # the brim: one pleated concrete skirt leaning out all round, its outer edge folding up and down
    n = 36
    z0 = 10.4
    ring_in = [Vector((c[0] + math.cos(i / n * math.tau) * R * 0.8, c[1] + math.sin(i / n * math.tau) * R * 0.8, z0)) for i in range(n)]
    ring_out = [Vector((c[0] + math.cos(i / n * math.tau) * R * 1.32, c[1] + math.sin(i / n * math.tau) * R * 1.32, z0 + (1.3 if i % 2 else -0.2))) for i in range(n)]
    for i in range(n):
        j = (i + 1) % n
        mb.face([ring_in[i], ring_in[j], ring_out[j], ring_out[i]], 'concrete', conc, wear)
        under = [ring_out[i] - Vector((0, 0, 0.45)), ring_out[j] - Vector((0, 0, 0.45)), ring_in[j] - Vector((0, 0, 0.45)), ring_in[i] - Vector((0, 0, 0.45))]
        mb.face(under, 'concrete', shade(conc, 0.7), wear)
        mb.face([ring_out[i], ring_out[j], under[1], under[0]], 'concrete', shade(conc, 0.85), wear)  # the brim's edge
    parts.cyl(mb, 'concrete', C @ Matrix.Translation((0, 0, z0)), R * 0.8, 4.5, conc, wear, seg=seg, r2=R * 0.62)  # the cap rising
    parts.cyl(mb, 'concrete', C @ Matrix.Translation((0, 0, z0 + 4.5)), R * 0.42, 5.0, conc, wear, seg=seg)  # crown drum
    for i in range(16):  # its fins
        q = i / 16 * math.tau
        mb.box('concrete', Matrix.Translation((c[0] + math.cos(q) * R * 0.44, c[1] + math.sin(q) * R * 0.44, z0 + 7.0)) @ Matrix.Rotation(q, 4, 'Z'), shade(conc, 0.95), wear, size=(1.2, 0.35, 5.0))
    parts.cyl(mb, 'concrete', C @ Matrix.Translation((0, 0, z0 + 9.5)), R * 0.5, 0.5, shade(conc, 0.9), wear, seg=seg)
    # the forecourt: flagpoles along the approach on the facing side
    i, Lf, F = faces(poly)[a.get('facing', 0)]
    for k in range(5):
        p = F @ Vector((-Lf * 0.3 + k * Lf * 0.15, 3.0, 0))
        parts.bar(mb, 'steel', (p.x, p.y, 0), (p.x, p.y, 12), 0.08, hex_rgb('#c9ced2'), 0.3)
        mb.box('cloth', Matrix.Translation((p.x, p.y, 11.0)), hex_rgb(rng.pick(['#1e8e3e', '#ffffff', '#c62828', '#e0b020'])), 0, size=(0.05, 1.6, 1.0))
    return places._done(mb, a, collection)


def central_mosque(a, rng, collection=None):
    """A central mosque: a big gold dome on a drum, four smaller gold domes, four slender minarets
    with gold tips at the corners, an arcade in front, white walls with green trim, and a wall round
    the court. Research-religious 1 and research-landmarks 32 (the central mosque's gold dome), invented."""
    poly = places._poly(a)
    mb = MeshBuilder()
    wear = rng.between(0.15, 0.35)
    wall, green, gold = hex_rgb('#f4f2ea'), hex_rgb('#1f7a3a'), hex_rgb('#c9a13b')
    inner = offset(poly, -2.0)
    H = block(mb, inner, 2, dict(style='govt', wall=wall, band=green, trim=green, wear=wear, floor_h=4.5, window='casement', win_h=2.4,
                                 fins=False, roof='parapet', entrance=True, door=green, facing=a.get('facing', 0)), rng)
    c = centroid(inner)
    side = min(math.dist(inner[0], inner[1]), math.dist(inner[1], inner[2]))
    r = side * 0.3
    parts.cyl(mb, 'paint', Matrix.Translation((c[0], c[1], H)), r * 1.05, r * 0.6, wall, wear, seg=24)
    for k in range(20):  # arched windows round the drum
        q = k / 20 * math.tau
        mb.box('glass', Matrix.Translation((c[0] + math.cos(q) * r * 1.06, c[1] + math.sin(q) * r * 1.06, H + r * 0.3)) @ Matrix.Rotation(q, 4, 'Z'), hex_rgb('#24343e'), 0, size=(0.03, r * 0.12, r * 0.3))
    dome(mb, c[0], c[1], H + r * 0.6, r, gold, 0.05, seg=28, rings=10)
    for p in inner:  # small gold domes over the corners
        q = (c[0] + (p[0] - c[0]) * 0.62, c[1] + (p[1] - c[1]) * 0.62)
        parts.cyl(mb, 'paint', Matrix.Translation((q[0], q[1], H)), r * 0.3, r * 0.25, wall, wear, seg=16)
        dome(mb, q[0], q[1], H + r * 0.25, r * 0.28, gold, 0.05, seg=16, rings=6)
    hmin = max(26.0, H + r * 2.6)
    for p in poly:  # four minarets at the corners of the court, gold tips
        q = (c[0] + (p[0] - c[0]) * 0.9, c[1] + (p[1] - c[1]) * 0.9)
        minaret(mb, q[0], q[1], hmin, wall, green, gold, wear, rng)
    i, Lf, F = faces(inner)[a.get('facing', 0)]
    n = max(3, int(Lf / 3.2))
    for k in range(n):  # the arcade: columns and arches along the front
        u = -Lf / 2 + (k + 0.5) * Lf / n
        mb.box('paint', F @ Matrix.Translation((u, 1.6, 2.2)), wall, wear, size=(0.5, 0.5, 4.4))
    mb.box('paint', F @ Matrix.Translation((0, 1.6, 4.7)), green, wear, size=(Lf, 0.6, 0.6))
    mb.box('paint', F @ Matrix.Translation((0, 1.6, 5.1)), wall, wear, size=(Lf + 0.2, 3.4, 0.2))
    perimeter(mb, poly, dict(paint=wall, coping=green, gate=green, h=2.0, wear=wear), rng, a.get('facing', 0))
    return places._done(mb, a, collection)


# name -> builder(a, rng, collection), the same shape as the civic plot builders
BY_NAME = {
    'The Palace': places.palace,
    'The Crown Hall': crown_hall,          # waits for its plot in the 2D map (the Hub / Food Gate edge)
    'Railside Jumat Mosque': central_mosque,
    'Old Island Central Mosque': central_mosque,  # waits for its place in the 2D map
}


def build(a, rng, collection=None):
    return BY_NAME.get(a.get('label'), places.hall)(a, rng, collection)
