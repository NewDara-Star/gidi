"""Structures and city-scale lines: flyovers and rail bridges, skywalks, canal footbridges, jetties,
expressways with Jersey barriers, the Long Bridge on piers, the Cable Bridge with its leaning
paddle-blade pylon (research-landmarks 14-17, invented), the rail line, canals and boardwalks.
All take points already in Blender space (x east, y north)."""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import hex_rgb, shade

CONCRETE = '#a8a49a'


def _seg(a, b):
    a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0))
    d = b - a
    L = max(d.length, 1e-6)
    return a, d / L, L


def deck(mb, a, b, w, z0, z1, rng, col=CONCRETE, barrier=True, piers=25.0, wear=0.6, ramp=True, depth=1.2, solid=False):
    """A bridge deck from a to b, rising from z0 at the ends to z1 (ramps over the first and last
    quarter when ramp), on pier pairs every `piers` metres, with parapets. depth: the deck's
    thickness; solid: an embankment, its retaining walls running down to the ground."""
    A, d, L = _seg(a, b)
    n = max(2, int(L / 6))
    side = Vector((-d.y, d.x, 0))
    hz = lambda t: (z0 + (z1 - z0) * t) if ramp == 'linear' else z0 + (z1 - z0) * (min(1.0, min(t, 1 - t) / 0.25) if ramp else 1.0)
    for k in range(n):
        t0, t1 = k / n, (k + 1) / n
        p0, p1 = A + d * L * t0, A + d * L * t1
        z_0, z_1 = hz(t0), hz(t1)
        q = lambda p, s, z: p + side * s * w / 2 + Vector((0, 0, z))
        mb.face([q(p0, -1, z_0), q(p1, -1, z_1), q(p1, 1, z_1), q(p0, 1, z_0)], 'asphalt', hex_rgb('#4f5156'), wear)
        b0, b1 = (-0.2, -0.2) if solid else (z_0 - depth, z_1 - depth)
        if not solid:
            mb.face([q(p0, 1, b0), q(p1, 1, b1), q(p1, -1, b1), q(p0, -1, b0)], 'concrete', shade(hex_rgb(col), 0.75), wear)
        for s in (-1, 1):
            mb.face([q(p0, s, b0), q(p1, s, b1), q(p1, s, z_1), q(p0, s, z_0)] if s > 0 else [q(p1, s, b1), q(p0, s, b0), q(p0, s, z_0), q(p1, s, z_1)], 'concrete', hex_rgb(col), wear)
            if barrier:  # parapet, following the slope (no steps on the ramps)
                o_in, o_out = w / 2 - 0.3, w / 2
                P = lambda p, o, z: p + side * s * o + Vector((0, 0, z))
                top0, top1 = z_0 + 1.0, z_1 + 1.0
                for o in (o_in, o_out):  # inner and outer faces
                    quad = [P(p0, o, z_0), P(p1, o, z_1), P(p1, o, top1), P(p0, o, top0)]
                    mb.face(quad if (s > 0) == (o == o_out) else quad[::-1], 'concrete', hex_rgb(col), wear)
                mb.face([P(p0, o_in, top0), P(p1, o_in, top1), P(p1, o_out, top1), P(p0, o_out, top0)][::(1 if s > 0 else -1)], 'concrete', shade(hex_rgb(col), 1.05), wear)
    k = piers
    while k < L - piers * 0.5:
        t = k / L
        z = hz(t) - 1.2
        if z > 1.0:
            p = A + d * k
            for s in ((-1, 1) if w > 8 else (0,)):
                c = p + side * s * w * 0.28
                parts.cyl(mb, 'concrete', Matrix.Translation((c.x, c.y, 0)), 0.6 if w > 8 else 0.4, z, hex_rgb(col), wear, seg=12)
            mb.box('concrete', Matrix.Translation((p.x, p.y, z - 0.5)) @ Matrix.Rotation(math.atan2(d.y, d.x), 4, 'Z'), shade(hex_rgb(col), 0.85), wear, size=(1.4, w * 0.9, 1.0))
        k += piers


def deck_height(s, S, H, R):
    """Deck height at s metres along a structure S long: up from the road at each end over R metres
    (a smoothstep, a proper vertical curve), H in the middle."""
    R = min(R, S * 0.45)
    u = max(0.0, min(1.0, min(s, S - s) / R)) if R > 0 else 1.0
    return 0.05 + (H - 0.05) * u * u * (3 - 2 * u)


RAMP = {'flyover': 60.0, 'bridge': 80.0}
DEPTH = {'flyover': 1.2, 'bridge': 1.8, 'skywalk': 0.6}  # deck thickness, as the map's road pass sets it


def profile(pts, zs=None, H=6.5, R=60.0):
    """The deck top as a function of metres along pts. zs: the map's heights, one per point (above
    the ground under the deck); without them, deck_height's smooth hump of height H."""
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    S = acc[-1]
    if not zs:
        return lambda s: deck_height(s, S, H, R)

    def zf(s):
        if s <= 0:
            return zs[0]
        for i in range(len(acc) - 1):
            if s <= acc[i + 1]:
                t = (s - acc[i]) / ((acc[i + 1] - acc[i]) or 1)
                return zs[i] + (zs[i + 1] - zs[i]) * t
        return zs[-1]
    return zf


def deck_line(mb, pts, w, zs, rng, keep=lambda p: True, col=CONCRETE, piers=25.0, wear=0.6, lamps=None, dead=0.1, murals=False, depth=1.2, solid=False):
    """A whole deck along a polyline at its map heights (zs, one per point; a callable s -> z also
    works), in 3 m slabs; only the slabs and
    piers whose middle passes keep(p) (the tile being built) are made, so a bridge crossing many
    tiles comes out seamless. Dressed as Lagos decks are: yellow edge lines, white dashed lanes, on
    wide decks (w >= 18) a chequered black-and-white median barrier with double-arm lamps on it,
    otherwise lamps on alternate sides. Lamp heads are appended to `lamps` (saved with the tile)."""
    from . import roadside
    zf = zs if callable(zs) else profile(pts, zs)
    median = w >= 18
    half = w / 2 - 0.3  # inside the parapets
    lanes = max(1, int(((half - (0.4 if median else 0)) - 1.0) / 3.5))  # per side (or in all, without a median)
    if not median:
        lanes = max(1, int((w - 0.6 - 1.0) / 3.5))
    YEL, WHT = hex_rgb('#e8c21a'), hex_rgb('#e8e4d8')
    s0 = 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.dist(a, b)
        if L < 1e-6:
            continue
        A, d, _ = _seg(a, b)
        side = Vector((-d.y, d.x, 0))
        n = max(1, int(math.ceil(L / 3)))
        for k in range(n):
            t0, t1 = k / n, (k + 1) / n
            pa = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            pb = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if not keep(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)):
                continue
            za, zb = zf(s0 + L * t0), zf(s0 + L * t1)
            deck(mb, pa, pb, w, za, zb, rng, col=col, piers=1e9, wear=wear, ramp='linear', depth=depth, solid=solid and min(za, zb) < 4.0)
            Pa, Pb = Vector((pa[0], pa[1], 0)), Vector((pb[0], pb[1], 0))

            def strip(o0, o1, c, lift=0.012):
                mb.face([Pa + side * o0 + Vector((0, 0, za + lift)), Pb + side * o0 + Vector((0, 0, zb + lift)),
                         Pb + side * o1 + Vector((0, 0, zb + lift)), Pa + side * o1 + Vector((0, 0, za + lift))], 'paint', c, 0.35)
            for sg in (-1, 1):  # yellow edge lines by the parapets
                o = sg * (half - 0.5)
                strip(o - 0.08, o + 0.08, YEL)
            sm = s0 + L * (t0 + t1) / 2
            dash = int(sm // 3) % 3 == 0
            if median:
                for sg in (-1, 1):
                    strip(sg * 0.45 - 0.06, sg * 0.45 + 0.06, YEL)  # yellow by the median too
                    for ln in range(1, lanes):
                        o = sg * (0.6 + ln * 3.5)
                        if dash:
                            strip(o - 0.07, o + 0.07, WHT)
                # the barrier: 1.5 m blocks, black and white in turn
                for j in range(2):
                    u0, u1 = t0 + (t1 - t0) * j / 2, t0 + (t1 - t0) * (j + 1) / 2
                    q = A + d * L * (u0 + u1) / 2
                    zq = zf(s0 + L * (u0 + u1) / 2)
                    blk = (int((s0 + L * u0) // 1.5) % 2) == 0
                    mb.box('concrete', Matrix.Translation((q.x, q.y, zq + 0.4)) @ Matrix.Rotation(math.atan2(d.y, d.x), 4, 'Z'),
                           hex_rgb('#1a1a1a') if blk else hex_rgb('#f2f2ee'), 0.5, size=(L * (u1 - u0) + 0.01, 0.5, 0.8))
            else:
                for ln in range(1, lanes):
                    o = -(w / 2 - 0.3 - 0.5) + ln * ((w - 1.6) / lanes)
                    if dash:
                        strip(o - 0.07, o + 0.07, WHT)
        s0 += L
    # piers, and lamps every 40 m, along the whole line
    s0, nxt, nl = 0.0, piers, 20.0
    li = 0
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        while nxt < s0 + L:
            p = A + d * (nxt - s0)
            z = zf(nxt) - depth
            if z > (4.0 - depth if solid else 1.0) and keep((p.x, p.y)):
                for sg in ((-1, 1) if w > 8 else (0,)):
                    c = p + side * sg * w * 0.28
                    pr = 0.6 if w > 8 else 0.4
                    parts.cyl(mb, 'concrete', Matrix.Translation((c.x, c.y, -1.5)), pr, z + 1.5, hex_rgb(col), wear, seg=12)
                    if murals and z > 3 and rng.chance(0.75):
                        mural_pier(mb, c, pr, z, rng.child('mural', round(c.x), round(c.y)))
                mb.box('concrete', Matrix.Translation((p.x, p.y, z - 0.5)) @ Matrix.Rotation(math.atan2(d.y, d.x), 4, 'Z'), shade(hex_rgb(col), 0.85), wear, size=(1.4, w * 0.9, 1.0))
            nxt += piers
        while nl < s0 + L:
            p = A + d * (nl - s0)
            if keep((p.x, p.y)):
                lr = rng.child('lamp', round(p.x), round(p.y))
                zd = zf(nl)
                ang = math.atan2(side.y, side.x)  # arms reach across the road
                if median:
                    heads = roadside.street_light(mb, p.x, p.y, ang, lr, arms=2, h=10, working=not lr.chance(dead), z0=zd + 0.8)
                else:
                    sg = 1 if li % 2 else -1
                    q = p + side * sg * (w / 2 - 0.35)
                    heads = roadside.street_light(mb, q.x, q.y, ang + (math.pi if sg > 0 else 0), lr, arms=1, h=9, working=not lr.chance(dead), z0=zd + 1.0)
                if lamps is not None:
                    lamps.extend(heads)
            li += 1
            nl += 40.0
        s0 += L


MURAL_PALETTES = [('#f2c230', '#1f5fa8', '#c62828', '#f4f1ea', '#1d1d1d'), ('#2e7d4f', '#f2c230', '#ff7a1a', '#3a2a6a', '#f4f1ea'),
                  ('#e8467c', '#29a3c9', '#f2c230', '#1d1d1d', '#ffffff'), ('#6a1b9a', '#ffb000', '#00897b', '#f4f1ea', '#c62828')]


def mural_pier(mb, c, r, h, rng):
    """Paint a bridge pier the way Lagos under-bridges are painted: bold bands and shapes in a
    few strong colours round all four faces, up to about two thirds of its height (research-
    landmarks 25). c: the pier's base centre, r: its radius, h: its height."""
    pal = [hex_rgb(x) for x in rng.pick(MURAL_PALETTES)]
    top = h * rng.between(0.5, 0.75)
    for q in range(4):  # four faces round the pier
        a = q * math.pi / 2 + math.pi / 4
        F = Matrix.Translation((c.x + math.cos(a) * (r + 0.02), c.y + math.sin(a) * (r + 0.02), 0)) @ Matrix.Rotation(a + math.pi / 2, 4, 'Z')
        z = 0.3
        while z < top:  # stacked bands of colour
            bh = rng.between(0.5, 1.6)
            mb.box('paint', F @ Matrix.Translation((0, 0, z + bh / 2)), rng.pick(pal), 0.3, size=(r * 1.45, 0.02, bh))
            z += bh
        for _ in range(rng.randrange(1, 4)):  # discs and diamonds over the bands
            zz = rng.between(1.0, top)
            sz = rng.between(0.3, r * 0.6)
            D = F @ Matrix.Translation((rng.between(-r * 0.4, r * 0.4), -0.02, zz)) @ Matrix.Rotation(math.pi / 2, 4, 'X')
            if rng.chance(0.5):
                parts.cyl(mb, 'paint', D, sz, 0.01, rng.pick(pal), 0.2, seg=12)
            else:
                mb.box('paint', D @ Matrix.Rotation(math.pi / 4, 4, 'Z'), rng.pick(pal), 0.2, size=(sz * 1.4, sz * 1.4, 0.01))


def flyover(mb, pts, w, zs, rng, lamps=None, keep=lambda p: True):
    """A flyover or rail bridge at its map heights (zs: list, or a callable s -> z)."""
    deck_line(mb, pts, w, zs, rng, keep, lamps=lamps, dead=0.3, murals=True, depth=DEPTH['flyover'])


def approach(mb, pts, w, zs, rng, lamps=None, keep=lambda p: True):
    """The ramp onto a bridge: an embankment between retaining walls where it is low (under 4 m),
    a short viaduct on piers above that."""
    deck_line(mb, pts, w, zs, rng, keep, lamps=lamps, dead=0.2, depth=DEPTH['bridge'], solid=True)


def skywalk(mb, pts, w, rng, z=6.8):
    """An enclosed footbridge over the expressway: a steel-framed tube with a roof, stair towers at
    both ends. z: the deck top above the ground (from the map)."""
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        if L < 1e-6:
            continue
        side = Vector((-d.y, d.x, 0))
        ang = math.atan2(d.y, d.x)
        mid = A + d * L / 2
        mb.box('concrete', Matrix.Translation((mid.x, mid.y, z)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#9c978c'), 0.5, size=(L + 0.05, w, DEPTH['skywalk']))
        for s in (-1, 1):
            for k in range(int(L / 2) + 1):
                p = A + d * min(L, k * 2) + side * s * w / 2
                parts.bar(mb, 'steel', (p.x, p.y, z), (p.x, p.y, z + 2.6), 0.08, hex_rgb('#2f6fae'), 0.4)
            pa, pb = A + side * s * w / 2, A + d * L + side * s * w / 2
            parts.bar(mb, 'steel', (pa.x, pa.y, z + 1.1), (pb.x, pb.y, z + 1.1), 0.06, hex_rgb('#2f6fae'), 0.4)
        mb.box('zinc', Matrix.Translation((mid.x, mid.y, z + 2.7)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#c3c7ca'), 0.4, size=(L + 0.4, w + 0.6, 0.08))
    S = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    k = 10.0
    while k < S - 5:  # columns every 10 m
        acc = 0.0
        for a, b in zip(pts, pts[1:]):
            L = math.dist(a, b)
            if acc + L >= k and L > 0:
                t = (k - acc) / L
                parts.cyl(mb, 'steel', Matrix.Translation((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, 0)), 0.3, z, hex_rgb('#8a8f92'), 0.4, seg=8)
                break
            acc += L
        k += 10
    for (A, d, L), e, t in ((_seg(pts[0], pts[1]), 0, -1), (_seg(pts[-2], pts[-1]), 1, 1)):  # stair towers
        ang = math.atan2(d.y, d.x)
        c = (A + d * L * e) + d * t * 3
        mb.box('steel', Matrix.Translation((c.x, c.y, z / 2)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#2f6fae'), 0.5, size=(5, w + 1, z))
        n = max(12, int(z / 0.18))
        for k in range(n):
            mb.box('concrete', Matrix.Translation((c.x + d.x * t * (k * 3.0 / n - 1.5), c.y + d.y * t * (k * 3.0 / n - 1.5), z * k / n)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#9c978c'), 0.5, size=(0.3, w, 0.15))


def snap_footbridge(pts, canals, gap=10.0, width=None):
    """A footbridge in the data is drawn from somewhere near the canal; centre it on the canal's
    line and make it span the channel and both banks (the canal's width + 4 m), square across the flow.
    Returns the new two-point line, or the original if no canal is near."""
    m = ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
    best = None
    for c in canals:
        for a, b in zip(c, c[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy or 1
            t = max(0.0, min(1.0, ((m[0] - a[0]) * dx + (m[1] - a[1]) * dy) / L2))
            q = (a[0] + dx * t, a[1] + dy * t)
            d = math.dist(q, m)
            if d < gap and (best is None or d < best[0]):
                L = math.sqrt(L2)
                best = (d, q, (-dy / L, dx / L))
    if not best:
        return pts
    _, q, n = best
    half = max(math.dist(pts[0], pts[-1]), (width or CANAL_W) + 4) / 2
    return [(q[0] - n[0] * half, q[1] - n[1] * half), (q[0] + n[0] * half, q[1] + n[1] * half)]


CANAL_W = 4.0  # the default; each canal carries its own width in the map
FOOTBRIDGE_H = 1.3


def footbridge(mb, pts, w, rng, z=FOOTBRIDGE_H):
    """A canal footbridge: a steel deck with handrails on block abutments, steps up at each end.
    z: the deck above the ground (from the map)."""
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        ang = math.atan2(d.y, d.x)
        steps = 2.0  # metres of stair at each end
        for k in range(int((L - 2 * steps) / 0.4)):
            p = A + d * (steps + k * 0.4 + 0.2)
            mb.box('steel', Matrix.Translation((p.x, p.y, z)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#6a6a6a'), 0.8, size=(0.38, w, 0.05))
        for e in (0, 1):  # stairs and the block abutment under them
            for k in range(5):
                u = (k + 0.5) / 5 * steps
                p = A + d * (u if e == 0 else L - u)
                mb.box('concrete', Matrix.Translation((p.x, p.y, z * (k + 1) / 5 / 2)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#8a857a'), 0.7, size=(steps / 5 + 0.02, w, z * (k + 1) / 5))
        for s in (-1, 1):
            pa, pb = A + d * steps + side * s * w / 2, A + d * (L - steps) + side * s * w / 2
            parts.bar(mb, 'steel', (pa.x, pa.y, z + 1.0), (pb.x, pb.y, z + 1.0), 0.05, hex_rgb('#3a3a3a'), 0.7)
            for k in range(int((L - 2 * steps) / 1.5) + 1):
                p = pa + d * min(L - 2 * steps, k * 1.5)
                parts.bar(mb, 'steel', (p.x, p.y, z), (p.x, p.y, z + 1.0), 0.04, hex_rgb('#3a3a3a'), 0.7)


def jetty(mb, pts, w, rng, z=0.9):
    """A timber jetty on piles at z over the water, canoes tied along it."""
    from .kinds import canoe
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        ang = math.atan2(d.y, d.x)
        for k in range(int(L / 0.25)):
            p = A + d * (k * 0.25 + 0.12)
            mb.box('wood', Matrix.Translation((p.x, p.y, z)) @ Matrix.Rotation(ang, 4, 'Z'), shade(hex_rgb('#6e6152'), rng.between(0.8, 1.1)), 0.8, size=(0.22, w, 0.06))
        for k in range(int(L / 2) + 1):
            for s in (-1, 1):
                p = A + d * min(L, k * 2) + side * s * w / 2
                parts.bar(mb, 'wood', (p.x, p.y, -0.5), (p.x, p.y, z + 0.3), 0.16, hex_rgb('#4a4036'), 0.8)
        for k in range(rng.randrange(0, 3) if len(pts) > 2 else rng.randrange(2, 6)):
            p = A + d * rng.between(2, L) + side * rng.pick([-1, 1]) * (w / 2 + 0.8)
            canoe(mb, Matrix.Translation((p.x, p.y, 0.08)) @ Matrix.Rotation(ang + rng.between(-0.2, 0.2), 4, 'Z'), rng)


def expressway(mb, pts, w, rng, median=True, lamps=None, keep=lambda p: True):
    """A dual carriageway: asphalt, lane dashes, yellow edge lines, a Jersey barrier median painted
    in black and white blocks, double-arm lamps on the median every 40 m (a share dead)."""
    from . import roadside
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        ang = math.atan2(d.y, d.x)
        ext = w / 2
        p0, p1 = A - d * ext, A + d * (L + ext)
        mb.face([p0 - side * w / 2 + Vector((0, 0, 0.07)), p1 - side * w / 2 + Vector((0, 0, 0.07)), p1 + side * w / 2 + Vector((0, 0, 0.07)), p0 + side * w / 2 + Vector((0, 0, 0.07))], 'asphalt', hex_rgb('#4a4c50'), 0.45)
        for s in (-1, 1):
            for off in (w / 4, w / 2 - 0.5):
                q0, q1 = A + side * s * off, A + d * L + side * s * off
                if off > w / 3:
                    mb.box('paint', Matrix.Translation(((q0.x + q1.x) / 2, (q0.y + q1.y) / 2, 0.075)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#e8c21a'), 0.4, size=(L, 0.15, 0.01))
                else:
                    k = 0.0
                    while k < L - 3:
                        q = A + d * (k + 1.5) + side * s * off
                        mb.box('paint', Matrix.Translation((q.x, q.y, 0.075)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#e8e4d8'), 0.4, size=(3, 0.12, 0.01))
                        k += 10
        if median:
            k = 0.0
            while k < L:
                q = A + d * (k + 2)
                mb.box('concrete', Matrix.Translation((q.x, q.y, 0.47)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#1a1a1a') if int(k // 4) % 2 else hex_rgb('#f2f2ee'), 0.6, size=(3.96, 0.5, 0.8))
                k += 4
            k = 20.0
            while k < L:
                q = A + d * k
                if keep((q.x, q.y)):
                    lr = rng.child('lamp', round(q.x), round(q.y))
                    heads = roadside.street_light(mb, q.x, q.y, ang + math.pi / 2, lr, arms=2, h=10, working=not lr.chance(0.25), z0=0.87, banners=lr.chance(0.5))
                    if lamps is not None:
                        lamps.extend(heads)
                k += 40


BRIDGE_H = {'long': 7.0, 'cable': 9.0}


def long_bridge(mb, pts, w, rng, keep=lambda p: True, lamps=None, zs=None):
    """The Long Bridge: an endless low concrete ribbon on pier pairs across the lagoon, high over
    the boat channel. zs: the map's deck heights (else a hump of BRIDGE_H)."""
    deck_line(mb, pts, w, zs or profile(pts, None, BRIDGE_H['long'], RAMP['bridge']), rng, keep, piers=30, wear=0.7, lamps=lamps, dead=0.2, depth=DEPTH['bridge'])


def cable_bridge(mb, pts, w, rng, keep=lambda p: True, lamps=None, zs=None):
    """The Cable Bridge (invented): a single leaning paddle-blade pylon, a fan of stays, a white
    deck; the pylon is lit at night (research-landmarks 15, Gidi design)."""
    zf = profile(pts, zs) if zs else profile(pts, None, BRIDGE_H['cable'], RAMP['bridge'])
    deck_line(mb, pts, w, zf, rng, keep, col='#e8e6df', piers=40, wear=0.15, lamps=lamps, dead=0.0, depth=DEPTH['bridge'])
    A, d, L = _seg(pts[0], pts[-1])
    S = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    mid = A + d * L * 0.5
    if not keep((mid.x, mid.y)):
        return
    side = Vector((-d.y, d.x, 0))
    top = mid + Vector((0, 0, zf(S / 2) + 76)) - d * 8
    for s in (-1, 1):  # the blade: two legs leaning together, joined into a paddle
        base = mid + side * s * (w / 2 + 1.5)
        parts.bar(mb, 'concrete', (base.x, base.y, 0), (top.x + side.x * s * 1.2, top.y + side.y * s * 1.2, top.z), 2.2, hex_rgb('#f2efe6'), 0.1)
    for k in range(14):  # stays fanning to both spans
        for e in (-1, 1):
            t = (k + 1) / 15
            p = mid + d * e * (L * 0.48) * t
            zq = zf(S / 2 + e * (S * 0.48) * t) + 0.5
            for s in (-1, 1):
                q = p + side * s * (w / 2 - 0.3)
                parts.bar(mb, 'steel', (top.x, top.y, top.z - k * 2.5), (q.x, q.y, zq), 0.08, hex_rgb('#d8dcdf'), 0.1)
    mb.box('emit', Matrix.Translation((top.x, top.y, top.z + 1)), hex_rgb('#ffffff'), 0, size=(2, 2, 2))


def rail(mb, pts, rng):
    """The rail line: ballast bed, sleepers, two rails, a fence along parts, shanties close by."""
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        ang = math.atan2(d.y, d.x)
        mid = A + d * L / 2
        mb.box('concrete', Matrix.Translation((mid.x, mid.y, 0.12)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#8a8378'), 0.8, size=(L + 2, 4.2, 0.24))
        for k in range(int(L / 0.8)):
            p = A + d * (k * 0.8)
            mb.box('wood', Matrix.Translation((p.x, p.y, 0.3)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#4a4038'), 0.8, size=(0.22, 2.4, 0.12))
        for s in (-1, 1):
            q = mid + side * s * 0.72
            mb.box('steel', Matrix.Translation((q.x, q.y, 0.42)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#7a6a5a'), 0.7, size=(L, 0.08, 0.15))


def canal(mb, pts, w, rng):
    """A drainage canal: concrete banks, dark green water, refuse and water hyacinth."""
    from .street import litter_piece
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        ang = math.atan2(d.y, d.x)
        mid = A + d * L / 2
        wz = Vector((0, 0, 0.1))  # clear of the ground, so it never flickers through it
        mb.face([A - side * w / 2 + wz, A + d * L - side * w / 2 + wz, A + d * L + side * w / 2 + wz, A + side * w / 2 + wz], 'water', hex_rgb('#2a3a22'), 0)
        for s in (-1, 1):
            q = mid + side * s * (w / 2 + 0.2)
            mb.box('concrete', Matrix.Translation((q.x, q.y, 0.3)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#8a857a'), 0.8, size=(L + 0.4, 0.4, 0.6))
            qi = mid + side * s * (w / 2 - 0.01)  # stained inner face, the waterline's green-black tide mark
            mb.box('concrete', Matrix.Translation((qi.x, qi.y, 0.35)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#3a3a2a'), 0.95, size=(L + 0.4, 0.02, 0.5))
        for k in range(int(L * w / 8)):
            p = A + d * rng.between(0, L) + side * rng.between(-w / 2.2, w / 2.2)
            if rng.chance(0.4):
                mb.box('leaf', Matrix.Translation((p.x, p.y, 0.05)) @ Matrix.Rotation(rng.between(0, 3), 4, 'Z'), hex_rgb('#4f8a34'), 0, size=(rng.between(0.6, 1.6), rng.between(0.5, 1.2), 0.05))
            else:
                litter_piece(mb, p.x, p.y, 0.04, rng)


def culvert(mb, pts, w, rng, z=0.12, cross=None):
    """A road over a canal on a concrete slab flush with the road. cross: where the road crosses the
    water, (x, y, canal direction (dx, dy), canal width); low parapets stand along the road edges
    there, as long as the water is wide. Without it (the road runs along the canal) just the slab."""
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        if L < 1e-6:
            continue
        ang = math.atan2(d.y, d.x)
        mid = A + d * L / 2
        mb.box('concrete', Matrix.Translation((mid.x, mid.y, (z - 0.6) / 2)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#8f8a80'), 0.7, size=(L + 0.05, w + 0.6, z + 0.6))
    if not cross:
        return
    x, y, (cx, cy), cw = cross
    c = Vector((x, y, 0))
    u = Vector((cx, cy, 0)).normalized()  # along the canal = across the road
    n = Vector((-u.y, u.x, 0))  # across the canal = along the road
    ang = math.atan2(n.y, n.x)
    for s in (-1, 1):
        q = c + u * s * (w / 2 + 0.25)
        mb.box('concrete', Matrix.Translation((q.x, q.y, z + 0.3)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#a8a49a'), 0.7, size=(cw + 1.2, 0.35, 0.6))


def quay(mb, pts, top, rng):
    """A sea wall: a concrete face down into the water, a coping along the top and a railing, with
    the odd bollard. top: the coping above the ground behind it."""
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        if L < 1e-6:
            continue
        ang = math.atan2(d.y, d.x)
        mid = A + d * L / 2
        M = Matrix.Translation((mid.x, mid.y, 0)) @ Matrix.Rotation(ang, 4, 'Z')
        mb.box('concrete', M @ Matrix.Translation((0, 0, (top - 1.5) / 2)), hex_rgb('#8f8a80'), 0.75, size=(L + 0.05, 0.8, top + 1.5))
        mb.box('concrete', M @ Matrix.Translation((0, 0, top + 0.06)), hex_rgb('#b8b3a8'), 0.5, size=(L + 0.05, 1.0, 0.12))
        for k in range(int(L / 2.5) + 1):
            p = A + d * min(L, k * 2.5)
            parts.bar(mb, 'steel', (p.x, p.y, top), (p.x, p.y, top + 1.0), 0.04, hex_rgb('#3a5a6a'), 0.6)
            if rng.chance(0.08):
                parts.cyl(mb, 'steel', Matrix.Translation((p.x, p.y, top)), 0.18, 0.5, hex_rgb('#2a2a2a'), 0.6, seg=8)
        a, b = A + Vector((0, 0, top + 1.0)), A + d * L + Vector((0, 0, top + 1.0))
        parts.bar(mb, 'steel', tuple(a), tuple(b), 0.04, hex_rgb('#3a5a6a'), 0.6)


def boardwalk(mb, pts, rng):
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        ang = math.atan2(d.y, d.x)
        for k in range(int(L / 0.25)):
            p = A + d * (k * 0.25)
            mb.box('wood', Matrix.Translation((p.x, p.y, 1.2)) @ Matrix.Rotation(ang, 4, 'Z'), shade(hex_rgb('#6e6152'), rng.between(0.8, 1.1)), 0.9, size=(0.22, 0.6, 0.05))
        for k in range(int(L / 2) + 1):
            p = A + d * min(L, k * 2)
            parts.bar(mb, 'wood', (p.x, p.y, -0.4), (p.x, p.y, 1.2), 0.1, hex_rgb('#4a4036'), 0.9)


def estate_wall(mb, pts, rng):
    """A long estate wall segment: block, coping, razor wire."""
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.dist(a, b)
        if L < 0.1:
            continue
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        m = Matrix.Translation(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0)) @ Matrix.Rotation(ang, 4, 'Z')
        mb.box('paint', m @ Matrix.Translation((0, 0, 1.4)), hex_rgb('#f2efe6'), 0.3, size=(L, 0.22, 2.8))
        mb.box('paint', m @ Matrix.Translation((0, 0, 2.85)), hex_rgb('#3a3c3e'), 0.3, size=(L + 0.02, 0.3, 0.1))


def estate_gate(mb, pts, main, rng):
    a, b = pts[0], pts[-1]
    L = max(3.0, math.dist(a, b))
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    m = Matrix.Translation(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0)) @ Matrix.Rotation(ang, 4, 'Z')
    for s in (-1, 1):
        mb.box('paint', m @ Matrix.Translation((s * (L / 2 + 0.5), 0, 1.8)), hex_rgb('#f2efe6'), 0.3, size=(1.0, 1.0, 3.6))
    mb.box('steel', m @ Matrix.Translation((0, 0, 1.2)), hex_rgb('#2a2a2a'), 0.3, size=(L, 0.08, 2.4))
    if main:
        mb.box('paint', m @ Matrix.Translation((0, 0, 4.0)), hex_rgb('#f2efe6'), 0.3, size=(L + 2, 1.0, 0.8))
