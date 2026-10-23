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


def cathedral(a, rng, collection=None):
    """A Gothic-revival cathedral: a long nave under a steep roof, buttresses, tall pointed windows,
    and a square tower with a spire at the west front. Cream render or red-brown stone, slate-grey
    roof. Research-landmarks 31 (a cathedral spire over low roofs), invented."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    wear = rng.between(0.35, 0.6)
    wall = hex_rgb(rng.pick(['#e6d9bc', '#a8553a']))
    roof = hex_rgb('#4a5058')
    nl, nw, nh = L * 0.78, min(W * 0.6, 16), 13.0
    mb.box('paint', T(m, -L * 0.08, 0, nh / 2), wall, wear, size=(nl, nw, nh))
    rh = nw * 0.75  # steep pitched roof
    for s in (-1, 1):
        mb.face([T(m, -L * 0.08 - nl / 2, s * nw / 2, nh).translation, T(m, -L * 0.08 + nl / 2, s * nw / 2, nh).translation,
                 T(m, -L * 0.08 + nl / 2, 0, nh + rh).translation, T(m, -L * 0.08 - nl / 2, 0, nh + rh).translation][::s], 'zinc', roof, wear)
    for x in (-L * 0.08 - nl / 2, -L * 0.08 + nl / 2):  # gable ends
        mb.face([T(m, x, -nw / 2, nh).translation, T(m, x, nw / 2, nh).translation, T(m, x, 0, nh + rh).translation], 'paint', wall, wear)
    n = int(nl / 5)
    for k in range(n):  # buttresses and pointed windows down both sides
        x = -L * 0.08 - nl / 2 + (k + 0.5) * nl / n
        for s in (-1, 1):
            mb.box('paint', T(m, x - nl / n / 2, s * (nw / 2 + 0.5), nh * 0.4), shade(wall, 0.9), wear, size=(0.9, 1.0, nh * 0.8))
            mb.box('glass', T(m, x, s * (nw / 2 + 0.02), nh * 0.55), hex_rgb('#3a5a8a'), 0.1, size=(1.4, 0.02, nh * 0.55))
            mb.face([T(m, x - 0.7, s * (nw / 2 + 0.03), nh * 0.825).translation, T(m, x + 0.7, s * (nw / 2 + 0.03), nh * 0.825).translation,
                     T(m, x, s * (nw / 2 + 0.03), nh * 0.95).translation][::s], 'glass', hex_rgb('#3a5a8a'), 0.1)
    tx = -L * 0.08 + nl / 2 + 3.5  # the tower at the front
    th = 30.0
    mb.box('paint', T(m, tx, 0, th / 2), wall, wear, size=(7, 7, th))
    for z in (th * 0.35, th * 0.7):
        mb.box('paint', T(m, tx, 0, z), shade(wall, 0.85), wear, size=(7.4, 7.4, 0.5))
    for s in (-1, 1):
        mb.box('glass', T(m, tx, s * 3.51, th * 0.82), hex_rgb('#1c2830'), 0.1, size=(1.4, 0.02, 3.5))
        mb.box('glass', T(m, tx + s * 3.51, 0, th * 0.82), hex_rgb('#1c2830'), 0.1, size=(0.02, 1.4, 3.5))
    for k in range(4):  # pinnacles
        q = T(m, tx + (3.2 if k % 2 else -3.2), 3.2 if k // 2 else -3.2, th)
        parts.cyl(mb, 'paint', q, 0.45, 3.5, wall, wear, seg=6, r2=0.05)
    apex = T(m, tx, 0, th + 18).translation  # the spire
    base = [T(m, tx + x, y, th).translation for x, y in ((-3, -3), (3, -3), (3, 3), (-3, 3))]
    for i in range(4):
        mb.face([base[i], base[(i + 1) % 4], apex], 'zinc', roof, wear)
    parts.bar(mb, 'steel', apex, T(m, tx, 0, th + 21).translation, 0.12, hex_rgb('#c9a13b'), 0.2)
    mb.box('steel', T(m, tx, 0, th + 20.3), hex_rgb('#c9a13b'), 0.2, size=(0.12, 1.4, 0.12))  # the cross bar
    return places._done(mb, a, collection)


def colonial_civic(mb, poly, rng, wear):
    """An arcaded two-storey colonial civic building with twin towers and red hipped roofs."""
    wall, trim, red = hex_rgb(rng.pick(['#f2ead6', '#e8d9b0'])), hex_rgb('#f8f6f0'), hex_rgb('#a4473a')
    H = block(mb, poly, 2, dict(style='govt', wall=wall, band=trim, trim=trim, wear=wear, floor_h=4.6, window='casement', win_h=2.4, fins=False,
                                roof='hip', pitch=22, overhang=1.0, roof_col=red, facing=0), rng)
    i, Lf, F = faces(poly)[0]
    n = max(5, int(Lf / 3.0))
    for k in range(n + 1):  # the ground-floor arcade
        u = -Lf / 2 + k * Lf / n
        mb.box('paint', F @ Matrix.Translation((u, 1.8, 2.2)), trim, wear, size=(0.6, 0.6, 4.4))
    mb.box('paint', F @ Matrix.Translation((0, 1.8, 4.7)), trim, wear, size=(Lf + 0.6, 3.6, 0.5))
    for u in (-Lf / 2 + 2.5, Lf / 2 - 2.5):  # twin towers with pyramid caps
        tw = F @ Matrix.Translation((u, -1.5, 0))
        mb.box('paint', tw @ Matrix.Translation((0, 0, (H + 7) / 2)), wall, wear, size=(4.5, 4.5, H + 7))
        top = tw @ Vector((0, 0, H + 11))
        base = [tw @ Vector((x, y, H + 7)) for x, y in ((-2.5, -2.5), (2.5, -2.5), (2.5, 2.5), (-2.5, 2.5))]
        for j in range(4):
            mb.face([base[j], base[(j + 1) % 4], top], 'paint', red, wear)
        mb.box('glass', tw @ Matrix.Translation((0, 2.26, H + 4.5)), hex_rgb('#1c2830'), 0.1, size=(1.2, 0.02, 2.0))


def first_storey_house(mb, poly, rng, wear):
    """The oldest storey building: a small white two-storey house with a hipped zinc roof and a
    deep timber veranda on posts all round the upper floor."""
    white, wood, zinc = hex_rgb('#f4f2ea'), hex_rgb('#6b4a30'), hex_rgb('#8a8d8c')
    inner = offset(poly, -2.2)
    H = block(mb, inner, 2, dict(style='govt', wall=white, band=white, trim=wood, wear=wear, floor_h=3.4, window='casement', win_h=1.8, fins=False,
                                 roof='hip', pitch=24, overhang=2.4, roof_col=zinc, facing=0), rng)
    for p in poly:  # veranda posts at the corners and along each side
        parts.bar(mb, 'wood', (p[0], p[1], 0), (p[0], p[1], H), 0.18, wood, wear)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        for k in range(1, 4):
            q = (a[0] + (b[0] - a[0]) * k / 4, a[1] + (b[1] - a[1]) * k / 4)
            parts.bar(mb, 'wood', (q[0], q[1], 0), (q[0], q[1], H), 0.15, wood, wear)
        parts.bar(mb, 'wood', (a[0], a[1], 3.4 + 1.0), (b[0], b[1], 3.4 + 1.0), 0.08, wood, wear)  # the balustrade
    pts = [(p[0], p[1], 3.4) for p in poly]
    mb.face(pts, 'wood', shade(wood, 1.2), wear)  # the veranda floor


def heritage_strip(a, rng, collection=None):
    """The Heritage Strip: the colonial civic building, and on a smaller plot the oldest storey
    building. Research-landmarks 10 and 11, invented."""
    poly = places._poly(a)
    mb = MeshBuilder()
    wear = rng.between(0.4, 0.7)
    area = abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))) / 2
    (colonial_civic if area > 500 else first_storey_house)(mb, offset(poly, -1.0), rng, wear)
    return places._done(mb, a, collection)


def civic_tower(a, rng, collection=None):
    """A tall civic tower: a slim concrete shaft of 30 storeys with ribbon windows and fins, a plant
    crown and an antenna mast on top. Research-landmarks 20, invented."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    wear = rng.between(0.4, 0.65)
    conc = hex_rgb('#cfcac0')
    tw, td = min(L, 26) * 0.8, min(W, 20) * 0.8
    fh, n = 3.6, 30
    H = fh * n
    mb.box('concrete', T(m, 0, 0, 4.0), shade(conc, 0.9), wear, size=(tw + 6, td + 6, 8.0))  # podium
    mb.box('concrete', T(m, 0, 0, H / 2), conc, wear, size=(tw, td, H))
    for k in range(2, n):  # ribbon windows
        for s in (-1, 1):
            mb.box('glass', T(m, 0, s * (td / 2 + 0.02), k * fh + 1.6), hex_rgb('#24343e'), 0.1, size=(tw - 1.0, 0.02, 1.6))
            mb.box('glass', T(m, s * (tw / 2 + 0.02), 0, k * fh + 1.6), hex_rgb('#24343e'), 0.1, size=(0.02, td - 1.0, 1.6))
    for u in (-tw / 4, 0, tw / 4):  # vertical fins on the long faces
        for s in (-1, 1):
            mb.box('concrete', T(m, u, s * (td / 2 + 0.4), H / 2), shade(conc, 0.95), wear, size=(0.4, 0.8, H))
    mb.box('concrete', T(m, 0, 0, H + 3), shade(conc, 0.85), wear, size=(tw * 0.7, td * 0.7, 6))  # plant crown
    parts.bar(mb, 'steel', T(m, 0, 0, H + 6).translation, T(m, 0, 0, H + 32).translation, 0.5, hex_rgb('#c62828'), 0.4)  # the mast
    for z in (H + 14, H + 22, H + 30):
        mb.box('steel', T(m, 0, 0, z), hex_rgb('#f4f4f0'), 0.3, size=(1.4, 1.4, 1.2))
    mb.box('emit', T(m, 0, 0, H + 32.5), hex_rgb('#ff3030'), 0, size=(0.6, 0.6, 0.6))  # the aircraft light
    return places._done(mb, a, collection)


def market_block(a, rng, collection=None):
    """A multi-storey market: five floors of open galleries, each floor's band a different colour,
    railings, stair towers at the ends, signboards crowding the frontage. Research-landmarks 30, invented."""
    poly = places._poly(a)
    mb = MeshBuilder()
    wear = rng.between(0.5, 0.8)
    inner = offset(poly, -0.5)
    cols = [hex_rgb(c) for c in rng.pick([('#e0b020', '#1f5fa8', '#c62828', '#2e7d4f', '#ff7a1a'), ('#29a3c9', '#e8467c', '#f2c230', '#6a1b9a', '#2e7d4f')])]
    H = block(mb, inner, 5, dict(style='shops', wall=hex_rgb('#e8e2d2'), band=cols[0], wear=wear, floor_h=3.6, roof='parapet', tanks=3, facing=a.get('facing', 0)), rng)
    for fi, F_ in enumerate(faces(inner)):
        i, Lf, F = F_
        for k in range(5):  # a coloured gallery slab and railing on each floor
            z = k * 3.6 + 3.4
            mb.box('paint', F @ Matrix.Translation((0, 1.2, z)), cols[k % len(cols)], wear, size=(Lf, 2.4, 0.3))
            mb.box('steel', F @ Matrix.Translation((0, 2.35, z + 0.6)), hex_rgb('#3a3a3a'), wear, size=(Lf, 0.05, 0.9))
        if fi == a.get('facing', 0):
            for k in range(int(Lf / 3.0)):  # crowded signboards on the frontage
                u = -Lf / 2 + 1.5 + k * 3.0
                mb.box('paint', F @ Matrix.Translation((u, 2.4, rng.between(1, 5) * 3.6 + 1.6)), hex_rgb(rng.pick(['#f2c230', '#c62828', '#1f5fa8', '#ffffff', '#2e7d4f'])), 0.3, size=(2.6, 0.06, 1.2))
    for p in (inner[0], inner[2]):  # stair towers
        mb.box('paint', Matrix.Translation((p[0], p[1], (H + 3) / 2)), cols[1], wear, size=(4.0, 4.0, H + 3))
    return places._done(mb, a, collection)


def refinery(a, rng, collection=None):
    """A refinery on its plot: distillation columns, storage spheres and tanks, pipe racks, and the
    flare stack burning at the top. Research-landmarks 28, invented."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    wear = rng.between(0.3, 0.6)
    steel, white = hex_rgb('#b8bcbf'), hex_rgb('#e8e6df')
    for k in range(4):  # columns
        parts.cyl(mb, 'steel', T(m, -L * 0.3 + k * 6, -W * 0.15, 0), rng.between(1.6, 2.6), rng.between(30, 55), steel, wear, seg=14)
    for k in range(3):  # spheres on legs
        x, y = L * 0.05 + k * 14, W * 0.2
        for q in range(6):
            aq = q / 6 * math.tau
            parts.bar(mb, 'steel', T(m, x + math.cos(aq) * 5, y + math.sin(aq) * 5, 0).translation, T(m, x + math.cos(aq) * 5, y + math.sin(aq) * 5, 7).translation, 0.35, steel, wear)
        from .blocks import dome as _dome
        _dome(mb, *T(m, x, y, 6.5).translation.to_tuple(), 6.0, white, wear, finial=False)
    for k in range(3):  # tanks
        parts.cyl(mb, 'steel', T(m, -L * 0.3 + k * 18, W * 0.3, 0), 8.0, 12.0, white, wear, seg=24)
    for y in (-W * 0.02, W * 0.05):  # pipe racks
        parts.bar(mb, 'steel', T(m, -L * 0.4, y, 6).translation, T(m, L * 0.35, y, 6).translation, 0.8, hex_rgb('#7a7d80'), wear)
    fx, fy = L * 0.4, -W * 0.35  # the flare
    parts.cyl(mb, 'steel', T(m, fx, fy, 0), 1.0, 70, hex_rgb('#c62828'), wear, seg=10, r2=0.7)
    for z in (20, 40, 60):
        mb.box('steel', T(m, fx, fy, z), hex_rgb('#f4f4f0'), 0.3, size=(1.8, 1.8, 1.5))
    parts.cyl(mb, 'emit', T(m, fx, fy, 70), 1.4, 6.0, hex_rgb('#ff8a1a'), 0, seg=8, r2=0.2)
    return places._done(mb, a, collection)


# ---------------------------------------------------------------- landmark parcels
def freedom_ground(mb, pts, rng, ch):
    """Freedom Ground: the protest park on the old prison site. Paved open ground, a half-round
    amphitheatre of stepped seats facing a stage, fragments of the old prison wall left standing
    with their barred openings, trees. Research-landmarks 12, invented."""
    from .parcels import _bbox_frame, _flat, tree
    from .core import ccw
    p = ccw(pts)
    _flat(mb, p, 0.03, 'pavers', hex_rgb('#c9c1b0'), 0.4)
    m, L, W = _bbox_frame(p)
    r0 = min(L, W) * 0.32
    for k in range(7):  # stepped seats in a half ring
        r = r0 - k * 2.2
        for j in range(16):
            a0, a1 = math.pi * j / 16, math.pi * (j + 1) / 16
            q0, q1 = T(m, math.cos(a0) * r, math.sin(a0) * r, 0).translation, T(m, math.cos(a1) * r, math.sin(a1) * r, 0).translation
            mid = (q0 + q1) / 2
            mb.box('concrete', Matrix.Translation((mid.x, mid.y, (7 - k) * 0.25)) @ Matrix.Rotation(math.atan2(q1.y - q0.y, q1.x - q0.x), 4, 'Z'), hex_rgb('#b8b2a6'), 0.5, size=((q1 - q0).length + 0.05, 2.2, (7 - k) * 0.5))
    mb.box('concrete', T(m, 0, -2.0, 0.5), hex_rgb('#8f8a80'), 0.5, size=(10, 5, 1.0))  # the stage
    for k in range(5):  # old prison wall fragments, brick, with barred openings
        x = -L * 0.4 + k * L * 0.2
        y = W * 0.38 * (1 if k % 2 else -1)
        ln = rng.between(8, 18)
        wm = T(m, x, y, 0, rng.between(-0.2, 0.2))
        mb.box('block', wm @ Matrix.Translation((0, 0, 2.6)), hex_rgb('#8a4a32'), 0.85, size=(ln, 0.6, 5.2))
        for j in range(int(ln / 3)):
            u = -ln / 2 + 1.5 + j * 3
            for b in range(5):
                mb.box('steel', wm @ Matrix.Translation((u - 0.4 + b * 0.2, 0, 2.8)), hex_rgb('#2a2a2a'), 0.8, size=(0.04, 0.7, 1.6))
    from .parcels import _scatter
    for q in _scatter(p, int(L * W / 1800), rng, pad=4):  # a few shade trees, the seats left open
        if math.hypot(*(m.inverted() @ Vector((q[0], q[1], 0))).to_2d()) > r0 + 4:
            tree(mb, q[0], q[1], rng, kind='broad')


# name -> builder(a, rng, collection), the same shape as the civic plot builders
BY_NAME = {
    'The Palace': places.palace,
    'Shore Palace': places.palace,
    'The Crown Hall': crown_hall,          # waits for its plot in the 2D map (the Hub / Food Gate edge)
    'Railside Jumat Mosque': central_mosque,
    'Old Island Central Mosque': central_mosque,  # waits for its place in the 2D map
    'Cathedral of Christ': cathedral,
    'Heritage Strip': heritage_strip,      # The Border, when it is built
    'Secretariat': civic_tower,
    'Cloth Market': market_block,
    'Alade Electronics Market': market_block,
}

# a named place lying in a parcel dresses that parcel: name -> builder(mb, pts, rng, ch)
PARCEL_BY_NAME = {
    'Freedom Ground': freedom_ground,
}


def build(a, rng, collection=None):
    return BY_NAME.get(a.get('label'), places.hall)(a, rng, collection)
