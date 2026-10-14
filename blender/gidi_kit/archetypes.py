"""Archetypes: whole objects assembled from parts, driven by rules."""
import math

from mathutils import Vector

from . import parts
from .core import MeshBuilder, ccw, centroid, edge_out, frame, offset
from .materials import master
from .rules import house_spec

STOREY = parts.STOREY


def house(a, rng, collection=None):
    """A front or back house (or shed): walls, windows with bars, doors, shop front and sign,
    balconies, pitched or flat roof, tank, dish, generator, compound wall, unfinished storey."""
    poly = ccw([tuple(p) for p in a['poly']])
    spec = house_spec(a, rng)
    s = spec['storeys']
    lift = 0.7 if spec['shop'] else 0.0  # shops get a taller ground floor, with the sign above the shutter
    H = s * STOREY + lift
    spec['lift'] = lift
    mb = MeshBuilder()
    oct_ = parts.walls(mb, poly, H, spec)
    facing = a.get('facing', 0)

    # windows, doors, shop front, balconies: face by face
    for i in range(len(poly)):
        A, B = poly[i], poly[(i + 1) % len(poly)]
        L = math.dist(A, B)
        n = edge_out(poly, i)
        F = frame(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0), (B[0] - A[0], B[1] - A[1]), n)
        use = L - 1.3
        k = max(1 if use > 1.2 else 0, int(use / spec['bay']))
        us = [(j - (k - 1) / 2) * use / max(1, k) for j in range(k)]
        wr = rng.child('face', i)
        balcony_here = s > 1 and wr.chance(spec['balcony_p']) and L > 4
        for st in range(s):
            z = st * STOREY + 1.6 + (lift if st else 0)
            for j, u in enumerate(us):
                if st == 0 and i == facing:
                    if spec['shop'] and abs(u) < 2.2:
                        continue
                    if not spec['shop'] and j == (k - 1) // 2:
                        parts.door(mb, F, u, spec['door'])
                        continue
                if a['kind'] == 'shed' and wr.chance(0.5):
                    continue
                w = dict(spec['window'])
                w['glass_mat'] = 'glass_lit' if wr.chance(0.35) else 'glass'
                if st > 0 and w['bars'] != 'none' and not wr.chance(0.6):
                    w['bars'] = 'none'
                parts.window(mb, F, u, z, w)
            if balcony_here and st >= 1:
                parts.balcony(mb, F, 0, st * STOREY + lift + 0.05, min(L - 1.0, 4.5), spec['balcony'])
        if spec['shop'] and i == facing:
            w = min(L - 1.4, 3.4)
            parts.roller_shutter(mb, F, 0, w, spec['shutter'])
            if spec['sign']:
                parts.signboard(mb, F, 0, 3.12, min(L - 0.4, 4.2), 0.72, spec['sign'])
            if spec.get('awning'):
                parts.awning(mb, F, 0, min(L, 5.0), spec['awning'])
        if spec['generator'] and i == (facing + 2) % len(poly):
            parts.generator(mb, F, rng.between(-L / 4, L / 4), spec['generator'])

    # roof
    if spec['roof']['form'] == 'flat':
        inner = parts.roof_flat(mb, poly, H, spec['parapet'])
        c = centroid(poly)
        if spec['tank']:
            t = (poly[0][0] * 0.6 + c[0] * 0.4, poly[0][1] * 0.6 + c[1] * 0.4)
            parts.water_tank(mb, t[0], t[1], H, spec['tank'])
        if spec['dish']:
            parts.satellite_dish(mb, poly[2][0] * 0.8 + c[0] * 0.2, poly[2][1] * 0.8 + c[1] * 0.2, H + 0.05, rng.between(0, 6), (0.92, 0.92, 0.92))
        if spec['unfinished']:
            parts.unfinished_storey(mb, poly, H + 0.05, spec, rng.child('unfinished'))
    else:
        r = parts.roof_pitched(mb, poly, H, dict(spec['roof']), rng.child('roof'))
        if spec['roof_tyres']:
            for k in range(rng.randrange(2, 5)):
                t, u = rng.between(0.15, 0.85), rng.between(0.3, 0.7)
                e = Vector((*r['A'], r['y0'])).lerp(Vector((*r['B'], r['y0'])), t)
                top = Vector((*r['m1'], r['zr'])).lerp(Vector((*r['m2'], r['zr'])), t)
                p = e.lerp(top, u)
                parts.tyre(mb, p.x, p.y, p.z + 0.12)
        if spec['dish'] and rng.chance(0.5):
            c = centroid(poly)
            parts.satellite_dish(mb, c[0], c[1], r['zr'] - 0.4, rng.between(0, 6), (0.92, 0.92, 0.92))

    # compound wall around it, open where the street is
    if spec['compound'] and a.get('wall_poly'):
        parts.compound_wall(mb, a['wall_poly'], dict(spec['compound'], gate_edge=facing), rng.child('wall'), a.get('wall_skip'))

    return mb.to_object(a.get('name', 'house'), collection, master), spec


def stall(a, rng, collection=None):
    """A market stall: timber posts, a lean-to zinc roof higher at the front, a counter, a back wall of old sheets."""
    from .core import hex_rgb, shade
    from .rules import C, CHARACTER
    ch = C[CHARACTER.get(a['district'], 'dense')]
    poly = ccw([tuple(p) for p in a['poly']])
    wear = rng.between(*ch['wear'])
    e0, e1 = math.dist(poly[0], poly[1]), math.dist(poly[1], poly[2])
    A, B, Cc, D = poly if e0 >= e1 else [poly[1], poly[2], poly[3], poly[0]]
    mb = MeshBuilder()
    wood = hex_rgb('#6b4f36')
    for p, h in ((A, 2.9), (B, 2.9), (Cc, 2.4), (D, 2.4)):
        parts.bar(mb, 'wood', (p[0], p[1], 0), (p[0], p[1], h), 0.1, wood, wear)
    roof = dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb(rng.pick(ch['roof_cols'])), wear=min(1, wear + 0.15))
    ov = 0.5
    front = Vector(A).lerp(Vector(B), 0.5)
    # overhanging lean-to: front edge A-B at 2.95 m, back edge D-C at 2.45 m
    nAB = edge_out(poly if e0 >= e1 else [poly[1], poly[2], poly[3], poly[0]], 0)
    Af = (A[0] + nAB[0] * ov, A[1] + nAB[1] * ov, 2.95)
    Bf = (B[0] + nAB[0] * ov, B[1] + nAB[1] * ov, 2.95)
    parts.corrugated(mb, (D[0], D[1], 2.45), (Cc[0], Cc[1], 2.45), Bf, Af, dict(roof, profile='sine'))
    L = math.dist(A, B)
    F = frame(((D[0] + Cc[0]) / 2, (D[1] + Cc[1]) / 2, 0), (Cc[0] - D[0], Cc[1] - D[1]), (-nAB[0], -nAB[1]))
    parts.corrugated(mb, F @ Vector((-L / 2, 0, 0.05)), F @ Vector((L / 2, 0, 0.05)), F @ Vector((L / 2, 0, 2.4)), F @ Vector((-L / 2, 0, 2.4)), dict(roof, col=hex_rgb(rng.pick(ch['roof_cols']))))
    Ff = frame(((A[0] + B[0]) / 2 - nAB[0] * 0.5, (A[1] + B[1]) / 2 - nAB[1] * 0.5, 0), (B[0] - A[0], B[1] - A[1]), nAB)
    mb.box('wood', parts.at(Ff, 0, 0, 0.45), shade(hex_rgb('#a07a52'), rng.between(0.8, 1.1)), wear, size=(L * 0.9, 0.6, 0.9))
    for k in range(rng.randrange(3, 9)):  # goods on and in front of the counter
        x = rng.between(-L * 0.42, L * 0.42)
        mb.box('plastic', parts.at(Ff, x, rng.between(-0.1, 0.1), 0.9 + 0.12), hex_rgb(rng.pick(['#c62828', '#1565c0', '#f9a825', '#2e7d32', '#3d3d3d', '#d8cdb8'])), 0, size=(rng.between(0.15, 0.4), rng.between(0.15, 0.3), rng.between(0.12, 0.3)))
    return mb.to_object(a.get('name', 'stall'), collection, master), None


def kiosk(a, rng, collection=None):
    """A painted steel kiosk with a serving hatch and a small zinc roof."""
    from .core import hex_rgb, shade
    poly = ccw([tuple(p) for p in a['poly']])
    c = centroid(poly)
    ang = math.atan2(poly[1][1] - poly[0][1], poly[1][0] - poly[0][0])
    from mathutils import Matrix
    m = Matrix.Translation((c[0], c[1], 0)) @ Matrix.Rotation(ang, 4, 'Z')
    col = hex_rgb(rng.pick(['#fdd835', '#1e88e5', '#e53935', '#43a047', '#ffffff']))
    wear = rng.between(0.3, 0.8)
    mb = MeshBuilder()
    mb.box('steel', m @ Matrix.Translation((0, 0, 1.15)), col, wear, size=(2.2, 1.6, 2.3))
    mb.box('paint', m @ Matrix.Translation((0, -0.81, 1.3)), (0.03, 0.03, 0.03), 0, size=(1.4, 0.02, 0.7))
    mb.box('steel', m @ Matrix.Translation((0, -1.0, 0.95)), shade(col, 0.85), wear, size=(1.5, 0.4, 0.05))
    parts.corrugated(mb, m @ Vector((-1.35, -1.05, 2.35)), m @ Vector((1.35, -1.05, 2.35)), m @ Vector((1.35, 1.0, 2.5)), m @ Vector((-1.35, 1.0, 2.5)),
                     dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb('#a7b0b5'), wear=wear))
    return mb.to_object(a.get('name', 'kiosk'), collection, master), None
