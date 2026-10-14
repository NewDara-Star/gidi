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


def deck(mb, a, b, w, z0, z1, rng, col=CONCRETE, barrier=True, piers=25.0, wear=0.6, ramp=True):
    """A bridge deck from a to b, rising from z0 at the ends to z1 (ramps over the first and last
    quarter when ramp), on pier pairs every `piers` metres, with parapets."""
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
        mb.face([q(p0, 1, z_0 - 1.2), q(p1, 1, z_1 - 1.2), q(p1, -1, z_1 - 1.2), q(p0, -1, z_0 - 1.2)], 'concrete', shade(hex_rgb(col), 0.75), wear)
        for s in (-1, 1):
            mb.face([q(p0, s, z_0 - 1.2), q(p1, s, z_1 - 1.2), q(p1, s, z_1), q(p0, s, z_0)] if s > 0 else [q(p1, s, z_1 - 1.2), q(p0, s, z_0 - 1.2), q(p0, s, z_0), q(p1, s, z_1)], 'concrete', hex_rgb(col), wear)
            if barrier:  # parapet
                mid = (p0 + p1) / 2 + side * s * (w / 2 - 0.15)
                mb.box('concrete', Matrix.Translation((mid.x, mid.y, (z_0 + z_1) / 2 + 0.5)) @ Matrix.Rotation(math.atan2(d.y, d.x), 4, 'Z'), hex_rgb(col), wear, size=(L / n + 0.02, 0.3, 1.0))
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
    (a smoothstep, so the car feels a vertical curve), H in the middle. The Mock uses the same
    profile (mock/src/world.ts deckHeight) to put cars and walkers on the deck."""
    R = min(R, S * 0.45)
    u = max(0.0, min(1.0, min(s, S - s) / R)) if R > 0 else 1.0
    return 0.05 + (H - 0.05) * u * u * (3 - 2 * u)


RAMP = {'flyover': 60.0, 'bridge': 80.0}


def deck_line(mb, pts, w, H, R, rng, keep=lambda p: True, col=CONCRETE, piers=25.0, wear=0.6):
    """A whole deck along a polyline with deck_height's profile, in ~6 m slabs; only the slabs and
    piers whose middle passes keep(p) (the tile being built) are made, so a bridge crossing many
    tiles comes out seamless."""
    S = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    s0 = 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.dist(a, b)
        if L < 1e-6:
            continue
        n = max(1, int(math.ceil(L / 6)))
        for k in range(n):
            t0, t1 = k / n, (k + 1) / n
            pa = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            pb = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if keep(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)):
                deck(mb, pa, pb, w, deck_height(s0 + L * t0, S, H, R), deck_height(s0 + L * t1, S, H, R), rng, col=col, piers=1e9, wear=wear, ramp='linear')
        s0 += L
    # piers, every `piers` metres along the whole line
    s0, nxt = 0.0, piers
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        while nxt < s0 + L:
            p = A + d * (nxt - s0)
            z = deck_height(nxt, S, H, R) - 1.2
            if z > 1.0 and keep((p.x, p.y)):
                side = Vector((-d.y, d.x, 0))
                for sg in ((-1, 1) if w > 8 else (0,)):
                    c = p + side * sg * w * 0.28
                    parts.cyl(mb, 'concrete', Matrix.Translation((c.x, c.y, -1.5)), 0.6 if w > 8 else 0.4, z + 1.5, hex_rgb(col), wear, seg=12)
                mb.box('concrete', Matrix.Translation((p.x, p.y, z - 0.5)) @ Matrix.Rotation(math.atan2(d.y, d.x), 4, 'Z'), shade(hex_rgb(col), 0.85), wear, size=(1.4, w * 0.9, 1.0))
            nxt += piers
        s0 += L


def flyover(mb, pts, w, layer, rng):
    deck_line(mb, pts, w, 6.5 * layer, RAMP['flyover'], rng)


def skywalk(mb, pts, w, rng):
    """An enclosed footbridge over the expressway: a steel-framed tube with a roof, stair towers."""
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        z = 6.8
        ang = math.atan2(d.y, d.x)
        mid = A + d * L / 2
        mb.box('concrete', Matrix.Translation((mid.x, mid.y, z)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#9c978c'), 0.5, size=(L, w, 0.3))
        for s in (-1, 1):
            for k in range(int(L / 2) + 1):
                p = A + d * min(L, k * 2) + side * s * w / 2
                parts.bar(mb, 'steel', (p.x, p.y, z), (p.x, p.y, z + 2.6), 0.08, hex_rgb('#2f6fae'), 0.4)
            pa, pb = A + side * s * w / 2, A + d * L + side * s * w / 2
            parts.bar(mb, 'steel', (pa.x, pa.y, z + 1.1), (pb.x, pb.y, z + 1.1), 0.06, hex_rgb('#2f6fae'), 0.4)
        mb.box('zinc', Matrix.Translation((mid.x, mid.y, z + 2.7)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#c3c7ca'), 0.4, size=(L + 0.4, w + 0.6, 0.08))
        for e, t in ((A, -1), (A + d * L, 1)):  # stair towers
            c = e + d * t * 3
            mb.box('steel', Matrix.Translation((c.x, c.y, z / 2)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#2f6fae'), 0.5, size=(5, w + 1, z))
            for k in range(12):
                mb.box('concrete', Matrix.Translation((c.x + d.x * t * (k * 0.25 - 1.5), c.y + d.y * t * (k * 0.25 - 1.5), z * k / 12)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#9c978c'), 0.5, size=(0.3, w, 0.15))
        for k in range(int(L / 10) + 1):
            p = A + d * min(L, k * 10)
            parts.cyl(mb, 'steel', Matrix.Translation((p.x, p.y, 0)), 0.3, z, hex_rgb('#8a8f92'), 0.4, seg=8)


def footbridge(mb, pts, w, rng):
    """A canal footbridge: a steel truss on block abutments, a little above the water."""
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        z = 1.6
        for k in range(int(L / 0.4)):
            p = A + d * (k * 0.4 + 0.2)
            mb.box('steel', Matrix.Translation((p.x, p.y, z)) @ Matrix.Rotation(math.atan2(d.y, d.x), 4, 'Z'), hex_rgb('#6a6a6a'), 0.8, size=(0.38, w, 0.05))
        for s in (-1, 1):
            pa, pb = A + side * s * w / 2, A + d * L + side * s * w / 2
            parts.bar(mb, 'steel', (pa.x, pa.y, z + 1.1), (pb.x, pb.y, z + 1.1), 0.05, hex_rgb('#3a3a3a'), 0.7)
            for k in range(int(L / 1.5) + 1):
                p = A + d * min(L, k * 1.5) + side * s * w / 2
                parts.bar(mb, 'steel', (p.x, p.y, z), (p.x, p.y, z + 1.1), 0.04, hex_rgb('#3a3a3a'), 0.7)


def jetty(mb, pts, w, rng):
    """A timber jetty on piles, canoes tied along it."""
    from .kinds import canoe
    for i in range(len(pts) - 1):
        A, d, L = _seg(pts[i], pts[i + 1])
        side = Vector((-d.y, d.x, 0))
        ang = math.atan2(d.y, d.x)
        for k in range(int(L / 0.25)):
            p = A + d * (k * 0.25 + 0.12)
            mb.box('wood', Matrix.Translation((p.x, p.y, 0.9)) @ Matrix.Rotation(ang, 4, 'Z'), shade(hex_rgb('#6e6152'), rng.between(0.8, 1.1)), 0.8, size=(0.22, w, 0.06))
        for k in range(int(L / 2) + 1):
            for s in (-1, 1):
                p = A + d * min(L, k * 2) + side * s * w / 2
                parts.bar(mb, 'wood', (p.x, p.y, -0.5), (p.x, p.y, 1.2), 0.16, hex_rgb('#4a4036'), 0.8)
        for k in range(rng.randrange(2, 6)):
            p = A + d * rng.between(2, L) + side * rng.pick([-1, 1]) * (w / 2 + 0.8)
            canoe(mb, Matrix.Translation((p.x, p.y, 0.08)) @ Matrix.Rotation(ang + rng.between(-0.2, 0.2), 4, 'Z'), rng)


def expressway(mb, pts, w, rng, median=True):
    """A dual carriageway: asphalt, lane dashes, yellow edge lines, a Jersey barrier median."""
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
                mb.box('concrete', Matrix.Translation((q.x, q.y, 0.47)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#a8a59c'), 0.6, size=(3.96, 0.5, 0.8))
                k += 4


BRIDGE_H = {'long': 7.0, 'cable': 9.0}


def long_bridge(mb, pts, w, rng, keep=lambda p: True):
    """The Long Bridge: an endless low concrete ribbon on pier pairs across the lagoon, ramping
    down to the shore at both ends."""
    deck_line(mb, pts, w, BRIDGE_H['long'], RAMP['bridge'], rng, keep, piers=30, wear=0.7)


def cable_bridge(mb, pts, w, rng, keep=lambda p: True):
    """The Cable Bridge (invented): a single leaning paddle-blade pylon, a fan of stays, a white
    deck; the pylon is lit at night (research-landmarks 15, Gidi design)."""
    deck_line(mb, pts, w, BRIDGE_H['cable'], RAMP['bridge'], rng, keep, col='#e8e6df', piers=40, wear=0.15)
    A, d, L = _seg(pts[0], pts[-1])
    mid = A + d * L * 0.5
    if not keep((mid.x, mid.y)):
        return
    side = Vector((-d.y, d.x, 0))
    top = mid + Vector((0, 0, 85)) - d * 8
    for s in (-1, 1):  # the blade: two legs leaning together, joined into a paddle
        base = mid + side * s * (w / 2 + 1.5)
        parts.bar(mb, 'concrete', (base.x, base.y, 0), (top.x + side.x * s * 1.2, top.y + side.y * s * 1.2, top.z), 2.2, hex_rgb('#f2efe6'), 0.1)
    for k in range(14):  # stays fanning to both spans
        for e in (-1, 1):
            t = (k + 1) / 15
            p = mid + d * e * (L * 0.48) * t
            for s in (-1, 1):
                q = p + side * s * (w / 2 - 0.3)
                parts.bar(mb, 'steel', (top.x, top.y, top.z - k * 2.5), (q.x, q.y, 9.5), 0.08, hex_rgb('#d8dcdf'), 0.1)
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
        mb.face([A - side * w / 2 + Vector((0, 0, 0.02)), A + d * L - side * w / 2 + Vector((0, 0, 0.02)), A + d * L + side * w / 2 + Vector((0, 0, 0.02)), A + side * w / 2 + Vector((0, 0, 0.02))], 'water', hex_rgb('#3a4a30'), 0)
        for s in (-1, 1):
            q = mid + side * s * (w / 2 + 0.2)
            mb.box('concrete', Matrix.Translation((q.x, q.y, 0.3)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#8a857a'), 0.8, size=(L, 0.4, 0.6))
        for k in range(int(L * w / 8)):
            p = A + d * rng.between(0, L) + side * rng.between(-w / 2.2, w / 2.2)
            if rng.chance(0.4):
                mb.box('leaf', Matrix.Translation((p.x, p.y, 0.05)) @ Matrix.Rotation(rng.between(0, 3), 4, 'Z'), hex_rgb('#4f8a34'), 0, size=(rng.between(0.6, 1.6), rng.between(0.5, 1.2), 0.05))
            else:
                litter_piece(mb, p.x, p.y, 0.04, rng)


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
