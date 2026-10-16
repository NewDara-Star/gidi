"""Archetypes: whole objects assembled from parts, driven by rules."""
import math

from mathutils import Matrix, Vector

from . import detail, parts
from .core import MeshBuilder, at, ccw, centroid, edge_out, frame, offset, shade
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
                if st > 0 and w['bars'] != 'none' and (detail.web() or not wr.chance(0.6)):
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


def extension(a, rng, collection=None):
    """A room built onto a house (the Google rebuild's infill, docs/KIT-GAPS.md): one storey against its neighbour, a door and
    a window to the yard, a lean-to zinc roof falling away from the high side, or now and then a flat concrete slab."""
    from .core import hex_rgb
    poly = ccw([tuple(p) for p in a['poly']])
    spec = house_spec(dict(a, storeys=1), rng)
    spec.update(storeys=1, shop=False, balcony_p=0.0, generator=None, compound=None, tank=None, dish=False, unfinished=False, lift=0.0)
    H = STOREY - 0.2
    mb = MeshBuilder()
    parts.walls(mb, poly, H, spec)
    facing = a.get('facing', 0) % len(poly)
    A, B = poly[facing], poly[(facing + 1) % len(poly)]
    L = math.dist(A, B)
    n = edge_out(poly, facing)
    F = frame(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0), (B[0] - A[0], B[1] - A[1]), n)
    if L > 1.6:
        parts.door(mb, F, -L / 4 if L > 3.5 else 0, spec['door'])
    if L > 3.5:
        parts.window(mb, F, L / 4, 1.6, dict(spec['window'], glass_mat='glass'))
    if rng.chance(0.3):   # a flat slab: the next storey will go on it one day
        parts.roof_flat(mb, poly, H, spec['parapet'])
    else:   # lean-to: low over the facing (yard) side, high at the back
        C_, D_ = poly[(facing + 2) % len(poly)], poly[(facing + 3) % len(poly)]
        ov = 0.35
        lo, hi = H + 0.05, H + 0.75
        roof = dict(profile='sine', pitch=0.076, depth=0.018, col=spec['roof'].get('col', hex_rgb('#7a5a40')), wear=min(1.0, spec['roof'].get('wear', 0.6) + 0.15))
        parts.corrugated(mb, (A[0] + n[0] * ov, A[1] + n[1] * ov, lo), (B[0] + n[0] * ov, B[1] + n[1] * ov, lo), (C_[0], C_[1], hi), (D_[0], D_[1], hi), roof)
    return mb.to_object(a.get('name', 'extension'), collection, master), spec


def market_shed(a, rng, collection=None):
    """A Lagos market shed (Mile 12, from Google's outlines): posts every 3-4 m, one zinc roof over the whole footprint (two
    slopes on the big ones), tarpaulins hung down some sides, goods heaped underneath. 40 to 400 m2."""
    from .core import hex_rgb, shade
    from .rules import C, CHARACTER
    ch = C[CHARACTER.get(a['district'], 'dense')]
    poly = ccw([tuple(p) for p in a['poly']])
    if len(poly) != 4:
        return stall(dict(a, _small=True), rng, collection)
    wear = rng.between(*ch['wear'])
    e0, e1 = math.dist(poly[0], poly[1]), math.dist(poly[1], poly[2])
    A, B, Cc, D = poly if e0 >= e1 else [poly[1], poly[2], poly[3], poly[0]]
    L, Wd = math.dist(A, B), math.dist(B, Cc)
    mb = MeshBuilder()
    wood = hex_rgb('#5e4630')
    eave = rng.between(2.8, 3.3)
    big = L * Wd > 150
    ridge = eave + (rng.between(0.9, 1.4) if big else 0.0)
    roof = dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb(rng.pick(ch['roof_cols'])), wear=min(1, wear + 0.2))
    Av, Bv, Cv, Dv = (Vector((*p, 0)) for p in (A, B, Cc, D))
    # posts along both long sides (and down the middle under a ridge)
    nposts = max(2, int(L // rng.between(3.0, 4.0)) + 1)
    for k in range(nposts):
        t = k / (nposts - 1)
        for side, h in ((Av.lerp(Bv, t), eave), (Dv.lerp(Cv, t), eave if big else eave - 0.5)):
            parts.bar(mb, 'wood', (side.x, side.y, 0), (side.x, side.y, h), 0.09, wood, wear)
        if big and 0 < k < nposts - 1:
            m = Av.lerp(Bv, t).lerp(Dv.lerp(Cv, t), 0.5)
            parts.bar(mb, 'wood', (m.x, m.y, 0), (m.x, m.y, ridge), 0.1, wood, wear)
    if big:   # two slopes meeting at a ridge along the length
        M1, M2 = Av.lerp(Dv, 0.5), Bv.lerp(Cv, 0.5)
        parts.corrugated(mb, (A[0], A[1], eave), (B[0], B[1], eave), (M2.x, M2.y, ridge), (M1.x, M1.y, ridge), roof)
        parts.corrugated(mb, (M1.x, M1.y, ridge), (M2.x, M2.y, ridge), (Cc[0], Cc[1], eave), (D[0], D[1], eave), dict(roof, col=shade(roof['col'], rng.between(0.85, 1.05))))
    else:   # one slope, high at the front
        parts.corrugated(mb, (D[0], D[1], eave - 0.5), (Cc[0], Cc[1], eave - 0.5), (B[0], B[1], eave), (A[0], A[1], eave), roof)
    # tarpaulins down some sides
    TARP = ['#1f5fa8', '#2b6cb0', '#e67e22', '#2e7d32', '#9e9e9e', '#c62828']
    for P0, P1 in ((Av, Bv), (Bv, Cv), (Cv, Dv), (Dv, Av)):
        if rng.chance(0.35):
            h = rng.between(1.2, eave - 0.4)
            parts.corrugated(mb, (P0.x, P0.y, eave - h), (P1.x, P1.y, eave - h), (P1.x, P1.y, eave - 0.05), (P0.x, P0.y, eave - 0.05),
                             dict(profile='sine', pitch=0.5, depth=0.04, col=hex_rgb(rng.pick(TARP)), wear=wear))
    # goods: heaps of sacks, baskets and crates under the roof
    for _ in range(int(L * Wd / rng.between(6, 12))):
        u, v = rng.between(0.1, 0.9), rng.between(0.15, 0.85)
        p = Av.lerp(Bv, u).lerp(Dv.lerp(Cv, u), v)
        mb.box('plastic' if rng.chance(0.4) else 'wood', Matrix.Translation((p.x, p.y, 0.35)) @ Matrix.Rotation(rng.between(0, 3.14), 4, 'Z'),
               shade(hex_rgb(rng.pick(['#c9b37e', '#8d6e4a', '#d84315', '#f9a825', '#6d8b3a', '#b0a08a', '#3d3d3d'])), rng.between(0.8, 1.1)), wear,
               size=(rng.between(0.5, 1.4), rng.between(0.5, 1.2), rng.between(0.3, 0.8)))
    return mb.to_object(a.get('name', 'market shed'), collection, master), None


def stall(a, rng, collection=None):
    """A market stall: timber posts, a lean-to zinc roof higher at the front, a counter, a back wall of old sheets."""
    from .core import hex_rgb, shade
    from .rules import C, CHARACTER
    ch = C[CHARACTER.get(a['district'], 'dense')]
    poly = ccw([tuple(p) for p in a['poly']])
    if not a.get('_small') and len(poly) == 4 and abs(sum(poly[i][0] * poly[(i + 1) % 4][1] - poly[(i + 1) % 4][0] * poly[i][1] for i in range(4))) / 2 > 40:
        return market_shed(a, rng, collection)   # a market shed, not a lock-up row
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


# ---------------------------------------------------------------- Act 1 (docs/KIT-GAPS.md, "New in the v2 layout")
RUST = ['#7a4a32', '#8a5a3a', '#6b4a3a', '#7d6a58', '#5e4a3e']
TARP = ['#1f5fa8', '#2b6cb0', '#e67e22', '#2e7d32', '#9e9e9e']


def _front(a):
    """A frame on the footprint's middle facing its street (x along the front, y out to the street, z up), with the
    front's length and the depth behind it."""
    poly = ccw([tuple(p) for p in a['poly']])
    i = a.get('facing', 0) % len(poly)
    A, B = poly[i], poly[(i + 1) % len(poly)]
    n = edge_out(poly, i)
    C = centroid(poly)
    depth = max(abs((p[0] - C[0]) * n[0] + (p[1] - C[1]) * n[1]) for p in poly) * 2
    return poly, frame((C[0], C[1], 0), (B[0] - A[0], B[1] - A[1]), n), math.dist(A, B), depth


def _side(F, x, y, out_deg):
    """A wall frame at (x, y) in F, facing out_deg (0 = F's +x, 90 = F's +y)."""
    return F @ Matrix.Translation((x, y, 0)) @ Matrix.Rotation(math.radians(out_deg - 90), 4, 'Z')


def _zinc(col, wear, pitch=0.076):
    return dict(profile='sine', pitch=pitch, depth=0.018 if pitch < 0.2 else 0.04, col=col, wear=wear)


def _open_door(mb, Fw, u, w, h, col, wear, swing=1.6, z0=0.0):
    """A doorway standing open: the dark gap and the leaf swung out on its hinge (u - w/2)."""
    mb.face([Fw @ Vector((u - w / 2, 0.03, z0)), Fw @ Vector((u + w / 2, 0.03, z0)), Fw @ Vector((u + w / 2, 0.03, z0 + h)), Fw @ Vector((u - w / 2, 0.03, z0 + h))], 'paint', (0.03, 0.025, 0.02), 0)
    hinge = Fw @ Matrix.Translation((u - w / 2, 0.06, z0)) @ Matrix.Rotation(swing, 4, 'Z')
    mb.box('steel', hinge @ Matrix.Translation((w / 2, 0, h / 2)), col, wear, size=(w - 0.04, 0.04, h - 0.04))
    return hinge


def face_me(a, rng, collection=None):
    """Face-me-I-face-you (Tunde's block in the Maze): one storey, a corridor down the middle with five rooms a side and a
    door at each end; small barred windows, a low rusted gable roof. Behind it the shared toilet and bathroom block, a
    kitchen corner with soot up the wall, washing lines across the yard; a bench and plastic chairs at the front door,
    a generator in its cage, jerrycans."""
    from . import props
    from .core import hex_rgb
    from .kinds import footprint
    poly, c, ang, L, W, m = footprint(a)
    spec = house_spec(dict(a, storeys=1, kind='back'), rng)
    wear = max(0.65, spec['wear'])
    spec.update(storeys=1, wear=wear, bare=rng.chance(0.25), lift=0.0)
    H = 2.95
    mb = MeshBuilder()
    parts.walls(mb, poly, H, spec)
    # which end is the front door, and which long side the yard is on: away from the street
    fi = a.get('facing', 0) % len(poly)
    fm = Vector(((poly[fi][0] + poly[(fi + 1) % 4][0]) / 2, (poly[fi][1] + poly[(fi + 1) % 4][1]) / 2, 0))
    loc = m.inverted() @ fm
    sx = 1 if loc.x >= 0 else -1
    ys = -1 if loc.y > 0.5 else 1 if loc.y < -0.5 else rng.pick([-1, 1])
    S = lambda x, y, out: m @ Matrix.Translation((x, y, 0)) @ Matrix.Rotation(math.radians(out - 90), 4, 'Z')
    door = dict(spec['door'], wear=wear)
    for e in (1, -1):   # the corridor's two doors; the front one stands open on the dark corridor
        Fe = S(e * L / 2, 0, 0 if e > 0 else 180)
        if e == sx:
            _open_door(mb, Fe, 0, 1.0, 2.1, door['door'], wear)
            mb.box('concrete', at(Fe, 0, 0.35, 0.08), (0.55, 0.55, 0.53), wear, size=(1.6, 0.7, 0.16))
        else:
            parts.door(mb, Fe, 0, door)
    win = dict(spec['window'], w=0.7, h=0.75, hood=False, wear=wear, bars=spec['window']['bars'] if spec['window']['bars'] != 'none' else 'vertical')
    for s in (1, -1):   # five rooms a side, a small window each
        Fs = S(0, s * W / 2, 90 if s > 0 else 270)
        for j in range(5):
            u = (j - 2) * (L - 1.6) / 5
            parts.window(mb, Fs, u, 1.75, dict(win, glass_mat='glass_lit' if rng.chance(0.15) else 'glass'))
    roof = spec['roof'] if spec['roof']['form'] != 'flat' else dict(profile='sine', pitch=0.076, depth=0.018, mixed=True, col2=hex_rgb(rng.pick(RUST)),
                                                                    gable_col=spec['paint'], fascia=spec['trim'], fascia_wood=True)
    roof.update(form='gable', pitch_deg=rng.between(12, 16), overhang=0.35, col=hex_rgb(rng.pick(RUST)), wear=min(1.0, wear + 0.25), wall_wear=wear,
                profile='sine', pitch=0.076, depth=0.018)
    parts.roof_pitched(mb, poly, H, roof, rng.child('roof'))
    # the yard behind
    Fb = S(0, ys * W / 2, 90 if ys > 0 else 270)   # the back wall, facing the yard (x along it)
    bx = lambda x, y: m @ Vector((x, ys * (W / 2 + y), 0))
    tx = -sx * (L / 2 - 1.8)   # toilet and bathroom block at the far end of the yard
    T0 = m @ Matrix.Translation((tx, ys * (W / 2 + 2.4), 0)) @ Matrix.Rotation(0 if ys > 0 else math.pi, 4, 'Z')
    grey = hex_rgb('#9a958a')
    mb.box('block', at(T0, 0, 0.8, 1.1), grey, 0.8, size=(2.8, 1.6, 2.2))
    for u in (-0.65, 0.65):   # two doors of old zinc sheet, toward the house
        Ft = T0 @ Matrix.Translation((0, 0, 0)) @ Matrix.Rotation(math.pi, 4, 'Z')
        mb.box('zinc', at(Ft, u, 0.02, 0.95), hex_rgb(rng.pick(RUST)), 0.9, size=(0.8, 0.03, 1.8))
    parts.corrugated(mb, at(T0, -1.6, -0.2, 2.1).translation, at(T0, 1.6, -0.2, 2.1).translation, at(T0, 1.6, 1.8, 2.45).translation, at(T0, -1.6, 1.8, 2.45).translation,
                     _zinc(hex_rgb(rng.pick(RUST)), 0.95))
    parts.cyl(mb, 'plastic', at(T0, 1.1, 1.5, 2.2), 0.05, 1.2, hex_rgb('#7a7a74'), 0.6, seg=8)   # the soak-away's vent pipe
    for k in range(rng.randrange(3, 6)):
        props.jerrycan(mb, at(T0, -1.8 - (k % 3) * 0.32, 0.3 + (k // 3) * 0.3, 0, rz=rng.between(-0.3, 0.3)), hex_rgb(rng.pick(['#e8b923', '#e8b923', '#2f6fae', '#c62828'])))
    # the kitchen corner: a low block wall, a coal pot, soot up the back wall
    kx = sx * (L / 2 - 2.6)
    soot_F = Fb @ Matrix.Translation((kx if ys > 0 else -kx, 0, 0))   # Fb runs along +x on one side, -x on the other
    props.soot(mb, soot_F, 1.8, 2.4)
    K = Matrix.Translation(tuple(bx(kx, 1.0))) @ Matrix.Rotation(ang, 4, 'Z')
    props.coal_fire(mb, K, rng.child('kitchen'), pot_r=0.26)
    mb.box('block', K @ Matrix.Translation((1.0, 0, 0.55)), grey, 0.8, size=(0.2, 1.8, 1.1))
    props.basin(mb, K @ Matrix.Translation((-0.7, 0.3, 0)), hex_rgb('#c9ced2'))
    # washing lines across the yard
    for k, y in enumerate((1.5, 2.9) if rng.chance(0.4) else (2.0,)):   # from the front end to just short of the toilet block
        props.washing_line(mb, bx(sx * (L / 2 - 0.8), y), bx(-sx * (L / 2 - 3.6), y), 1.85, rng.child('line', k))
    # the generator in its cage, by the back wall
    parts.generator(mb, Fb, (L / 2 - 1.2) * (-1 if rng.chance(0.5) else 1), dict(col=hex_rgb(rng.pick(['#c62828', '#2e7d32', '#f9a825'])), wear=0.8))
    # a bench and plastic chairs at the front door
    Fd = S(sx * L / 2, 0, 0 if sx > 0 else 180)
    props.bench(mb, at(Fd, 1.6, 1.2, 0, rz=0), 1.8)
    for k in range(rng.randrange(1, 3)):
        props.chair(mb, at(Fd, -1.4 - 0.6 * k, 1.1 + 0.2 * k, 0, rz=-math.pi / 2 + rng.between(-0.5, 0.5)), hex_rgb(rng.pick(props.CHAIR_COLS)), 0.5)
    return mb.to_object(a.get('name', 'face-me'), collection, master), spec


def park_office(a, rng, collection=None):
    """The motor park office (the boss's, the Hub; the first cutscene is shot inside). A zinc-walled shed on a block
    base: a hand-painted union sign over the door, a bench and a blue water drum outside, the door open on its padlock,
    a satellite dish. Inside: a desk with the ledger and the cash box, an office chair and two plastic chairs, a
    standing fan, a bare bulb, a peeling church calendar, a small TV on a stool."""
    from . import props
    from .core import hex_rgb
    poly, F, Lf, D = _front(a)
    Lf, D = max(Lf, 4.5), max(D, 3.2)
    mb = MeshBuilder()
    hx, hy = Lf / 2, D / 2
    base, top = 0.35, 2.7   # the block base, the zinc wall's top
    block, zinc = hex_rgb('#8f8a80'), hex_rgb(rng.pick(RUST))
    wear = rng.between(0.75, 0.95)
    dx = -hx + 1.3   # the door, toward one end of the front
    # block base and floor slab
    for (x, y, sx_, sy_) in ((0, hy - 0.1, Lf, 0.2), (0, -hy + 0.1, Lf, 0.2), (hx - 0.1, 0, 0.2, D), (-hx + 0.1, 0, 0.2, D)):
        mb.box('block', at(F, x, y, base / 2), block, 0.8, size=(sx_, sy_, base))
    mb.box('concrete', at(F, 0, 0, base - 0.03), hex_rgb('#7d786e'), 0.9, size=(Lf - 0.3, D - 0.3, 0.06))
    mb.box('concrete', at(F, dx, hy + 0.35, 0.09), hex_rgb('#8a857a'), 0.8, size=(1.3, 0.6, 0.18))   # the step
    # zinc walls: thin sheets (seen from inside too) with ribs outside; the front split round the door
    zh = top - base
    walls = [((-hx, -hy), (hx, -hy), 270), ((hx, -hy), (hx, hy), 0), ((-hx, hy), (-hx, -hy), 180),
             ((-hx, hy), (dx - 0.48, hy), 90), ((dx + 0.48, hy), (hx, hy), 90)]
    for (p0, p1, out) in walls:
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        l = math.dist(p0, p1)
        Fw = _side(F, mid[0], mid[1], out)
        mb.box('zinc', at(Fw, 0, -0.02, base + zh / 2), shade(zinc, 0.9), wear, size=(l, 0.03, zh))
        parts.corrugated(mb, at(Fw, -l / 2, 0.01, base).translation, at(Fw, l / 2, 0.01, base).translation, at(Fw, l / 2, 0.01, top).translation, at(Fw, -l / 2, 0.01, top).translation,
                         _zinc(zinc, wear))
    Ff = _side(F, 0, hy, 90)
    mb.box('zinc', at(Ff, dx, -0.02, (base + 2.35 + top) / 2), shade(zinc, 0.9), wear, size=(0.96, 0.03, top - base - 2.0))   # over the door
    leaf = _open_door(mb, Ff, dx, 0.9, 2.0, hex_rgb('#5e6a70'), wear, swing=1.9, z0=base)
    mb.box('steel', leaf @ Matrix.Translation((0.82, 0.04, 1.05)), hex_rgb('#2a2a2a'), 0.6, size=(0.12, 0.02, 0.04))   # the hasp
    mb.box('steel', leaf @ Matrix.Translation((0.86, 0.07, 0.98)), hex_rgb('#b08d3a'), 0.4, size=(0.05, 0.03, 0.06))   # the padlock, hanging open
    parts.bar(mb, 'steel', leaf @ Vector((0.84, 0.07, 1.01)), leaf @ Vector((0.84, 0.07, 1.06)), 0.008, hex_rgb('#9a9a9a'), 0.3)
    # a small barred window in the end wall
    Fe = _side(F, hx, 0, 0)
    mb.face([Fe @ Vector((-0.3, 0.03, 1.5)), Fe @ Vector((0.3, 0.03, 1.5)), Fe @ Vector((0.3, 0.03, 2.0)), Fe @ Vector((-0.3, 0.03, 2.0))], 'glass', hex_rgb('#24343e'), 0)
    parts.burglar_bars(mb, Fe, 0, 1.75, 0.6, 0.5, 'vertical', hex_rgb('#3a3a3a'), 0.8)
    # mono-pitch roof, higher at the front, with an underside for the inside shots
    o = 0.4
    lo, hi = top + 0.05, top + 0.4
    Pp = lambda x, y, z: (F @ Vector((x, y, z)))[:]
    parts.corrugated(mb, Pp(-hx - o, -hy - o, lo), Pp(hx + o, -hy - o, lo), Pp(hx + o, hy + o, hi), Pp(-hx - o, hy + o, hi), _zinc(hex_rgb(rng.pick(RUST)), min(1, wear + 0.1)))
    mb.face([Pp(-hx, hy, hi - 0.06), Pp(hx, hy, hi - 0.06), Pp(hx, -hy, lo - 0.06), Pp(-hx, -hy, lo - 0.06)], 'zinc', shade(zinc, 0.5), 0.9)
    parts.satellite_dish(mb, *Pp(hx - 0.8, -hy + 0.6, lo + 0.1)[:2], lo + 0.1, rng.between(0, 6), (0.85, 0.85, 0.82))
    # the union sign over the door, a bench and the water drum
    props.board(mb, Ff @ Matrix.Translation((0, 0.06, 0)), a.get('label') or 'PARK UNION OFFICE\nHUB UNIT', min(Lf - 0.6, 3.0), 0.55, hex_rgb('#f2efe6'), hex_rgb('#1f3f8a'), wear=0.8, z=top + 0.12)
    props.bench(mb, at(Ff, dx + 1.9, 0.55, 0, rz=math.pi / 2), 1.8)
    props.drum(mb, at(Ff, hx - 0.5, 0.55, 0), wear=0.6)
    # inside (floor at the base's top): desk, ledger, cash box, chairs, fan, bulb, calendar, TV
    z0 = base
    I = lambda x, y, rz=0.0: F @ Matrix.Translation((x, y, z0)) @ Matrix.Rotation(rz, 4, 'Z')
    wood = hex_rgb('#7a5a3a')
    Dk = I(0.7, -hy + 1.0)
    mb.box('wood', at(Dk, 0, 0, 0.76), wood, 0.7, size=(1.4, 0.7, 0.04))
    for x in (-0.66, 0.66):
        mb.box('wood', at(Dk, x, 0, 0.38), shade(wood, 0.8), 0.7, size=(0.04, 0.66, 0.76))
    mb.box('wood', at(Dk, 0, -0.3, 0.45), shade(wood, 0.75), 0.7, size=(1.3, 0.03, 0.55))
    led = at(Dk, -0.2, 0.05, 0.79, rz=0.15)   # the ledger, open
    for s in (-1, 1):
        mb.box('cloth', at(led, s * 0.16, 0, 0), hex_rgb('#6b1f1f'), 0.6, size=(0.32, 0.42, 0.012))
        mb.box('cloth', at(led, s * 0.155, 0, 0.012), hex_rgb('#e8e0c8'), 0.4, size=(0.3, 0.4, 0.01))
    mb.box('steel', at(Dk, 0.45, -0.05, 0.85), hex_rgb('#2e6b45'), 0.6, size=(0.32, 0.22, 0.14))   # the cash box
    mb.box('steel', at(Dk, 0.45, 0.06, 0.85), hex_rgb('#c9a13b'), 0.3, size=(0.05, 0.01, 0.04))
    mb.box('cloth', at(Dk, 0.15, -0.2, 0.79), hex_rgb('#f2d7a0'), 0.3, size=(0.1, 0.07, 0.03))   # ticket books
    C0 = I(0.7, -hy + 0.4, math.pi / 2)   # the office chair behind the desk, facing the door side
    parts.cyl(mb, 'steel', C0, 0.03, 0.42, hex_rgb('#3a3a3a'), 0.5, seg=8)
    for k in range(5):
        t = k / 5 * math.tau
        parts.bar(mb, 'steel', at(C0, 0, 0, 0.06).translation, at(C0, math.cos(t) * 0.3, math.sin(t) * 0.3, 0.04).translation, 0.03, hex_rgb('#2a2a2a'), 0.5)
    mb.box('cloth', at(C0, 0, 0, 0.47), hex_rgb('#1d1d1d'), 0.7, size=(0.5, 0.5, 0.08))
    mb.box('cloth', at(C0, -0.24, 0, 0.85, ry=0.12), hex_rgb('#1d1d1d'), 0.7, size=(0.07, 0.48, 0.65))
    mb.box('cloth', at(C0, -0.22, 0.12, 0.98, ry=0.12), hex_rgb('#5a4a3a'), 0.3, size=(0.08, 0.2, 0.16))   # a split in the vinyl
    for k, x in enumerate((0.3, 1.1)):   # two plastic chairs facing the desk
        props.chair(mb, I(x, -hy + 1.85, -math.pi / 2 + rng.between(-0.3, 0.3)), hex_rgb(rng.pick(['#f4f1ea', '#c62828', '#1f5fa8'])), 0.6)
    Fn = I(hx - 0.45, -hy + 0.45)   # the standing fan in the corner, turned to the desk
    parts.cyl(mb, 'plastic', Fn, 0.2, 0.04, hex_rgb('#e8e2d6'), 0.6, seg=12)
    parts.cyl(mb, 'steel', Fn, 0.02, 1.25, hex_rgb('#c9ced2'), 0.5, seg=6)
    hd = at(Fn, 0, 0, 1.3, rz=math.radians(200)) @ Matrix.Rotation(math.pi / 2, 4, 'Y')
    parts.cyl(mb, 'plastic', hd, 0.07, 0.16, hex_rgb('#e8e2d6'), 0.6, seg=10)
    parts.cyl(mb, 'steel', at(hd, 0, 0, -0.06), 0.24, 0.1, hex_rgb('#b0b4b8'), 0.6, seg=14, caps=(False, False))   # the cage
    for k in range(3):
        mb.box('plastic', at(hd, 0, 0, -0.01, rz=k * math.tau / 3) @ Matrix.Translation((0.11, 0, 0)), hex_rgb('#5aa0c8'), 0.4, size=(0.18, 0.08, 0.01))
    bz = (lo + hi) / 2 - 0.06   # the bare bulb on its flex from the roof
    parts.bar(mb, 'rubber', F @ Vector((0, 0, bz)), F @ Vector((0, 0, 2.3)), 0.01, (0.05, 0.05, 0.05), 0)
    from .people import sphere
    sphere(mb, 'lamp', F @ Matrix.Translation((0, 0, 2.25)), 0.04, 0.04, 0.055, hex_rgb('#fff1c0'), seg=8, rings=5)
    Fc = _side(F, -0.3, -hy + 0.06, 90)   # the church calendar, on the back wall inside, a corner peeling
    mb.box('cloth', at(Fc, 0, 0, 1.75), hex_rgb('#f2efe6'), 0.5, size=(0.42, 0.01, 0.62))
    mb.box('cloth', at(Fc, 0, 0.008, 1.88), hex_rgb('#3f6b9a'), 0.4, size=(0.36, 0.006, 0.28))
    mb.box('cloth', at(Fc, 0, 0.008, 2.0), hex_rgb('#c62828'), 0.4, size=(0.36, 0.006, 0.06))
    for r_ in range(3):
        mb.box('cloth', at(Fc, 0, 0.008, 1.66 - r_ * 0.08), hex_rgb('#8a8a8a'), 0.3, size=(0.34, 0.004, 0.01))
    mb.face([Fc @ Vector((0.21, 0.01, 1.44)), Fc @ Vector((0.21, 0.01, 1.56)), Fc @ Vector((0.11, 0.08, 1.46))], 'cloth', hex_rgb('#d8d0bc'), 0.6)
    T0 = I(-hx + 0.45, -0.3, 0)   # the TV on a stool against the end wall, facing the room
    for x in (-0.15, 0.15):
        for y in (-0.15, 0.15):
            mb.box('wood', at(T0, x, y, 0.25), shade(wood, 0.8), 0.7, size=(0.04, 0.04, 0.5))
    mb.box('wood', at(T0, 0, 0, 0.5), wood, 0.7, size=(0.38, 0.38, 0.03))
    mb.box('plastic', at(T0, 0, 0, 0.72), hex_rgb('#1d1d1d'), 0.5, size=(0.3, 0.5, 0.4))
    Ft = _side(F, -hx + 0.45 + 0.155, -0.3, 0)
    mb.face([Ft @ Vector((-0.2, 0, z0 + 0.58)), Ft @ Vector((0.2, 0, z0 + 0.58)), Ft @ Vector((0.2, 0, z0 + 0.88)), Ft @ Vector((-0.2, 0, z0 + 0.88))], 'glass', hex_rgb('#2a3a44'), 0)
    return mb.to_object(a.get('name', 'park office'), collection, master), None


def buka(a, rng, collection=None):
    """A buka (the Flyover Buka in the Maze): a lean-to kitchen against a wall. Big pots on coal and firewood, soot up
    the wall, a glass food display, long benches and a table under a tarpaulin, plastic plates, a hand-painted name board."""
    from . import props
    from .core import hex_rgb
    poly, F, Lf, D = _front(a)
    hx, hy = Lf / 2, D / 2
    mb = MeshBuilder()
    wear = rng.between(0.7, 0.95)
    grey = hex_rgb(rng.pick(['#a39d90', '#b8a88a', '#9a958a']))
    mb.box('block', at(F, 0, -hy + 0.1, 1.45), grey, 0.85, size=(Lf + 0.6, 0.2, 2.9))   # the wall it leans on
    mb.box('concrete', at(F, 0, 0, 0.04), hex_rgb('#7d786e'), 0.95, size=(Lf, D, 0.08))
    Fb = _side(F, 0, -hy + 0.2, 90)
    props.soot(mb, Fb @ Matrix.Translation((-hx * 0.35, 0, 0)), Lf * 0.55, 2.5)
    wood = hex_rgb('#5e4630')
    for x in (-hx + 0.1, hx - 0.1):   # front posts
        parts.bar(mb, 'wood', F @ Vector((x, hy - 0.1, 0)), F @ Vector((x, hy - 0.1, 2.3)), 0.1, wood, wear)
    Pp = lambda x, y, z: (F @ Vector((x, y, z)))[:]
    parts.corrugated(mb, Pp(-hx - 0.3, hy + 0.2, 2.3), Pp(hx + 0.3, hy + 0.2, 2.3), Pp(hx + 0.3, -hy + 0.2, 2.8), Pp(-hx - 0.3, -hy + 0.2, 2.8), _zinc(hex_rgb(rng.pick(RUST)), min(1, wear + 0.1)))
    tarp = hex_rgb(rng.pick(TARP))   # the tarpaulin out front over the table, on two poles
    ty = hy + 2.6
    for x in (-hx + 0.2, hx - 0.2):
        parts.bar(mb, 'wood', F @ Vector((x, ty, 0)), F @ Vector((x, ty, 2.1)), 0.06, wood, wear)
    parts.corrugated(mb, Pp(-hx, ty + 0.1, 2.1), Pp(hx, ty + 0.1, 2.1), Pp(hx, hy + 0.2, 2.28), Pp(-hx, hy + 0.2, 2.28), _zinc(tarp, 0.6, pitch=0.5))
    for k in range(3 if Lf > 4.5 else 2):   # the pots on their fires along the wall
        props.coal_fire(mb, F @ Matrix.Translation((-hx + 0.7 + k * 1.1, -hy + 0.75, 0.08)), rng.child('fire', k), pot_r=rng.between(0.3, 0.4))
    disp = F @ Matrix.Translation((hx - 1.0, -0.1, 0.08))   # the glass food display on its cabinet
    mb.box('wood', at(disp, 0, 0, 0.42), hex_rgb('#8a6a48'), 0.8, size=(1.3, 0.65, 0.84))
    for x, y, w, d in ((0, 0.32, 1.3, 0.01), (0, -0.32, 1.3, 0.01), (0.65, 0, 0.01, 0.65), (-0.65, 0, 0.01, 0.65)):   # the glass case
        mb.box('glass', at(disp, x, y, 1.1), hex_rgb('#9fb8c0'), 0, size=(w, d, 0.52))
    mb.box('glass', at(disp, 0, 0, 1.36), hex_rgb('#9fb8c0'), 0, size=(1.3, 0.65, 0.01))
    for k, col in enumerate(('#6b4a2e', '#3f6b2a', '#b03a1e', '#e8dcc0')):   # trays: amala, ewedu, stew, rice
        mb.box('steel', at(disp, -0.45 + k * 0.3, 0, 0.9), hex_rgb('#b0b4b8'), 0.4, size=(0.26, 0.5, 0.05))
        mb.box('plastic', at(disp, -0.45 + k * 0.3, 0, 0.93), hex_rgb(col), 0.3, size=(0.22, 0.44, 0.03))
    Tb = F @ Matrix.Translation((0, hy + 1.3, 0)) @ Matrix.Rotation(math.pi / 2, 4, 'Z')   # the long table and benches
    tl = min(Lf - 0.6, 3.2)
    props.table(mb, Tb, 0.7, tl, 0.76, hex_rgb('#9a7a52'), 0.8)
    for s in (-1, 1):
        props.bench(mb, at(Tb, s * 0.6, 0, 0), tl)
    for k in range(rng.randrange(3, 7)):   # plastic plates
        parts.cyl(mb, 'plastic', at(Tb, rng.between(-0.2, 0.2), rng.between(-tl / 2 + 0.2, tl / 2 - 0.2), 0.785), 0.11, 0.02,
                  hex_rgb(rng.pick(['#f4f1ea', '#c62828', '#2e7d32', '#1f5fa8'])), 0.3, seg=12)
    Fs = _side(F, -hx + 0.9, hy + 0.15, 90)   # the name board on two posts at the front
    for x in (-0.8, 0.8):
        parts.bar(mb, 'wood', Fs @ Vector((x, 0.1, 0)), Fs @ Vector((x, 0.1, 2.0)), 0.06, wood, wear)
    props.board(mb, Fs @ Matrix.Translation((0, 0.06, 0)), (a.get('label') or 'BUKA').upper() + '\nAMALA  EWEDU  RICE', 1.8, 0.6, hex_rgb('#f2c230'), hex_rgb('#7a1f1f'), wear=0.8, z=1.65)
    props.drum(mb, F @ Matrix.Translation((-hx - 0.1, -hy + 0.6, 0.0)), wear=0.7)
    return mb.to_object(a.get('name', 'buka'), collection, master), None


def lockup_open(a, rng, collection=None):
    """A market lock-up standing open (Ladi Lane, the chase line): block walls, the shutter rolled right up into its
    drum, goods stacked to the roof (engine parts, tyres, phone boxes, bolts of fabric), a tarpaulin awning out over the
    aisle, crates and a trolley in front."""
    from . import props
    from .core import hex_rgb
    poly, F, Lf, D = _front(a)
    hx, hy = Lf / 2, D / 2
    mb = MeshBuilder()
    wear = rng.between(0.6, 0.95)
    paint = hex_rgb(rng.pick(['#c9c3b6', '#d8cdb0', '#b8c4b0', '#c8b8a0', '#9a958a']))
    H = 2.9
    for (x, y, sx_, sy_) in ((0, -hy + 0.08, Lf, 0.16), (-hx + 0.08, 0, 0.16, D), (hx - 0.08, 0, 0.16, D)):
        mb.box('block' if rng.chance(0.4) else 'paint', at(F, x, y, H / 2), paint, wear, size=(sx_, sy_, H))
    mb.box('concrete', at(F, 0, 0, 0.05), hex_rgb('#7d786e'), 0.9, size=(Lf, D, 0.1))
    Pp = lambda x, y, z: (F @ Vector((x, y, z)))[:]
    parts.corrugated(mb, Pp(-hx - 0.1, hy + 0.2, H + 0.15), Pp(hx + 0.1, hy + 0.2, H + 0.15), Pp(hx + 0.1, -hy, H), Pp(-hx - 0.1, -hy, H), _zinc(hex_rgb(rng.pick(RUST)), min(1, wear + 0.1)))
    sh = hex_rgb(rng.pick(['#9aa3a8', '#2f6fae', '#2e7d4f', '#8a8f92']))
    mb.box('steel', at(F, 0, hy - 0.1, H - 0.2), shade(sh, 0.85), wear, size=(Lf - 0.1, 0.3, 0.32))   # the shutter, rolled up into its drum
    for s in (-1, 1):
        mb.box('steel', at(F, s * (hx - 0.2), hy - 0.05, (H - 0.35) / 2), sh, wear, size=(0.06, 0.08, H - 0.35))
    kind = rng.pick({'engine': 4, 'tyres': 3, 'phones': 1, 'fabric': 1})
    gr = rng.child('goods')
    y0, y1 = -hy + 0.3, hy - 0.7
    if kind == 'tyres':
        x = -hx + 0.55
        while x < hx - 0.4:
            y = y0 + 0.3
            while y < y1:
                for k in range(gr.randrange(4, 9)):
                    p = F @ Vector((x + gr.between(-0.03, 0.03), y, 0.12 + k * 0.21))
                    parts.tyre(mb, p.x, p.y, p.z, r=gr.between(0.3, 0.36), w=0.2)
                y += 0.75
            x += 0.75
    else:
        colsets = {'engine': ['#3a3a3a', '#5a5e60', '#6b4a2e', '#8a8f92', '#2a2a2a', '#7a3a2a'],
                   'phones': ['#f4f1ea', '#1d1d1d', '#c62828', '#1f5fa8', '#e8dcc0', '#f9a825'],
                   'fabric': ['#d7263d', '#1b998b', '#f46036', '#2e294e', '#f2c14e', '#5bc0eb', '#9bc53d']}[kind]
        x = -hx + 0.25
        while x < hx - 0.25:
            w = gr.between(0.35, 0.7) if kind != 'phones' else gr.between(0.25, 0.4)
            z = 0.1
            ztop = gr.between(1.8, H - 0.1)
            while z < ztop:
                h = gr.between(0.25, 0.55) if kind == 'engine' else gr.between(0.12, 0.3)
                col = shade(hex_rgb(gr.pick(colsets)), gr.between(0.8, 1.1))
                if kind == 'fabric':   # bolts lying across the shelves
                    parts.cyl(mb, 'ankara', F @ Matrix.Translation((x + w / 2, (y0 + y1) / 2, z + 0.1)) @ Matrix.Rotation(math.pi / 2, 4, 'X') @ Matrix.Translation((0, 0, -(y1 - y0) / 2)),
                              0.1, y1 - y0, col, 0.3, seg=8)
                    h = 0.21
                else:
                    mb.box('steel' if kind == 'engine' else 'cloth', at(F, x + w / 2, (y0 + y1) / 2 + gr.between(-0.1, 0.1), z + h / 2, rz=gr.between(-0.1, 0.1)), col, 0.6 if kind == 'engine' else 0.3,
                           size=(w * 0.95, (y1 - y0) * gr.between(0.6, 0.95), h))
                    if kind == 'engine' and gr.chance(0.3):   # a gearbox or alternator on top, round
                        parts.cyl(mb, 'steel', at(F, x + w / 2, y1 + 0.1, z + h, rx=math.pi / 2), 0.12, 0.25, hex_rgb('#5a5e60'), 0.7, seg=10)
                z += h + 0.01
            x += w + 0.04
    if rng.chance(0.65):   # the tarpaulin awning out over the aisle, on poles
        tc = hex_rgb(rng.pick(TARP))
        out = rng.between(1.3, 1.9)
        parts.corrugated(mb, Pp(-hx, hy + out, 2.25), Pp(hx, hy + out, 2.25), Pp(hx, hy + 0.15, 2.7), Pp(-hx, hy + 0.15, 2.7), _zinc(tc, 0.6, pitch=0.5))
        for x in (-hx + 0.1, hx - 0.1):
            parts.bar(mb, 'wood', F @ Vector((x, hy + out - 0.05, 0)), F @ Vector((x, hy + out - 0.05, 2.25)), 0.04, hex_rgb('#5e4630'), 0.8)
    for k in range(rng.randrange(0, 4)):   # crates in front, some stacked
        props.crate(mb, at(F, rng.between(-hx + 0.4, hx - 0.4), hy + rng.between(0.25, 0.6), 0.3 * (k % 2) if k else 0, rz=rng.between(-0.3, 0.3)),
                    hex_rgb(rng.pick(['#c62828', '#1f5fa8', '#f9a825', '#2e7d32'])), 0.6)
    if rng.chance(0.3):   # a hand trolley leaning by the door
        Tr = at(F, hx - 0.35, hy + 0.35, 0, rz=rng.between(-0.4, 0.4))
        for s in (-1, 1):
            parts.bar(mb, 'steel', at(Tr, s * 0.2, 0, 0.2).translation, at(Tr, s * 0.2, -0.25, 1.25).translation, 0.03, hex_rgb('#c62828'), 0.7)
            parts.cyl(mb, 'rubber', at(Tr, s * 0.26, 0.05, 0.12, ry=math.pi / 2), 0.12, 0.06, hex_rgb('#1c1c1c'), 0.4, seg=10)
        mb.box('steel', at(Tr, 0, 0.15, 0.03), hex_rgb('#5a5e60'), 0.7, size=(0.45, 0.3, 0.02))
    return mb.to_object(a.get('name', 'lock-up'), collection, master), None


def office(a, rng, collection=None):
    """'office' in the data: a one-storey hut under 60 m2 is a motor park's office (the boss's, the first cutscene);
    anything bigger is an office building (places.office)."""
    from .core import signed_area
    if a.get('storeys', 1) <= 1 and abs(signed_area([tuple(p) for p in a['poly']])) < 60:
        return park_office(a, rng, collection)
    from . import places
    return places.office(a, rng, collection)
