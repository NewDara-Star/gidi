"""Archetypes for the rest of the data's building kinds. Each builder takes the object's
attributes `a` (poly, storeys, district, ...) and its Rng, and returns (object, spec).
Specs come from docs/look/research-*.md; numbers there marked [est] are tuned by eye.
"""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import MeshBuilder, ccw, centroid, chamfer, edge_out, frame, hex_rgb, offset, prism, shade
from .materials import master
from .rules import C, CHARACTER

STOREY = parts.STOREY


def footprint(a):
    """Long-axis frame of a quad footprint: centre, angle, length, width, and a matrix."""
    poly = ccw([tuple(p) for p in a['poly']])
    e0, e1 = math.dist(poly[0], poly[1]), math.dist(poly[1], poly[2])
    A, B = (poly[0], poly[1]) if e0 >= e1 else (poly[1], poly[2])
    c = centroid(poly)
    ang = math.atan2(B[1] - A[1], B[0] - A[0])
    m = Matrix.Translation((c[0], c[1], 0)) @ Matrix.Rotation(ang, 4, 'Z')
    return poly, c, ang, max(e0, e1), min(e0, e1), m


def T(m, x, y, z, rz=0.0):
    return m @ Matrix.Translation((x, y, z)) @ Matrix.Rotation(rz, 4, 'Z')


def _done(mb, a, collection, spec=None):
    return mb.to_object(a.get('name', 'obj'), collection, master), spec or {}


# ---------------------------------------------------------------- waterfront
def stilt(a, rng, collection=None):
    """Makoko-like house on hardwood posts: plank walls, rusty zinc with tarp patches, a front
    platform where canoes tie up. research-buildings 8."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    floor = rng.between(1.0, 2.0)
    wear = rng.between(0.6, 1.0)
    wood = lambda: shade(hex_rgb(rng.pick({'#6e6152': 4, '#4a4036': 3, '#7a6a55': 2})), rng.between(0.85, 1.1))
    # the lagoon round it
    mb.face([(p[0], p[1], 0.06) for p in offset(poly, 4.0)], 'water', hex_rgb('#2a2620'), 0)
    # posts on a grid, leaning a little
    for x in [(-L / 2 + 0.2) + k * (L - 0.4) / max(1, round(L / 2)) for k in range(round(L / 2) + 1)]:
        for y in (-W / 2 + 0.2, W / 2 - 0.2, W / 2 + 1.4):
            lean = (rng.between(-0.08, 0.08), rng.between(-0.08, 0.08))
            parts.bar(mb, 'wood', T(m, x + lean[0], y + lean[1], -0.3).translation, T(m, x, y, floor).translation, rng.between(0.1, 0.18), wood(), wear)
    # floor deck and the front platform
    mb.box('wood', T(m, 0, 0, floor), wood(), wear, size=(L, W, 0.1))
    mb.box('wood', T(m, 0, W / 2 + 0.8, floor - 0.1), wood(), wear, size=(L * rng.between(0.5, 0.9), 1.6, 0.08))
    # walls of vertical planks, each its own shade; a door and a shuttered window
    h = rng.between(2.2, 2.5)
    for side, (x0, y0, x1, y1) in enumerate(((-L / 2, -W / 2, L / 2, -W / 2), (L / 2, -W / 2, L / 2, W / 2), (L / 2, W / 2, -L / 2, W / 2), (-L / 2, W / 2, -L / 2, -W / 2))):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 0.22))
        for k in range(n):
            t = (k + 0.5) / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            if side == 2 and abs(x) < 0.45:  # the door gap
                continue
            if side in (0, 2) and 0.9 < abs(x - (L * 0.25 if side == 2 else -L * 0.2)) < 1.6 and False:
                continue
            ph = h + rng.between(-0.05, 0.05)
            mb.box('wood', T(m, x, y, floor + ph / 2, rz=math.atan2(y1 - y0, x1 - x0)), wood(), wear, size=(math.hypot(x1 - x0, y1 - y0) / n + 0.01, 0.03, ph))
    mb.box('wood', T(m, 0, W / 2 + 0.02, floor + 1.05), shade(wood(), 0.6), wear, size=(0.85, 0.03, 2.0))  # door
    if rng.chance(0.3):  # a painted board
        mb.box('wood', T(m, -L / 4, W / 2 + 0.03, floor + 1.4), hex_rgb(rng.pick(['#2f6fae', '#2e7d4f', '#d9b23a'])), wear, size=(1.2, 0.02, 0.9))
    mb.box('paint', T(m, L / 4, W / 2 + 0.02, floor + 1.5), (0.03, 0.03, 0.03), 0, size=(0.6, 0.02, 0.5))  # window hole
    # mono-pitch or low gable zinc roof, with tarp patches
    rust = dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb('#7a4524'), wear=min(1, wear + 0.2))
    zf, zb = floor + h + 0.35, floor + h
    A, B = T(m, -L / 2 - 0.3, -W / 2 - 0.4, zb).translation, T(m, L / 2 + 0.3, -W / 2 - 0.4, zb).translation
    Cc, D = T(m, L / 2 + 0.3, W / 2 + 0.6, zf).translation, T(m, -L / 2 - 0.3, W / 2 + 0.6, zf).translation
    parts.corrugated(mb, A, B, Cc, D, rust)
    for _ in range(rng.randrange(0, 3)):
        x, y, s = rng.between(-L / 3, L / 3), rng.between(-W / 3, W / 3), rng.between(1.0, 2.2)
        z = zb + (y + W / 2 + 0.4) / (W + 1.0) * (zf - zb) + 0.05
        mb.box('cloth', T(m, x, y, z, rz=rng.between(-0.3, 0.3)) @ Matrix.Rotation(math.atan2(zf - zb, W + 1.0), 4, 'X'), hex_rgb(rng.pick(['#2e6fb7', '#e8771e', '#2e6fb7', '#d0d0d0'])), 0.3, size=(s, s * 0.8, 0.01))
    if rng.chance(0.6):  # a dugout canoe tied at the platform
        canoe(mb, T(m, rng.between(-L / 3, L / 3), W / 2 + 2.6, 0.06, rz=rng.between(-0.2, 0.2)), rng)
    return _done(mb, a, collection)


def canoe(mb, m, rng, length=None):
    """A dugout canoe: a pointed hull from stacked rings."""
    L = length or rng.between(4.5, 7.0)
    n, w, d = 10, rng.between(0.6, 0.8), 0.35
    col = shade(hex_rgb('#5a4632'), rng.between(0.7, 1.1))
    prev = None
    for k in range(n + 1):
        t = k / n
        x = -L / 2 + L * t
        hw = w / 2 * math.sin(math.pi * t) ** 0.6
        ring = [m @ Vector((x, -hw, d)), m @ Vector((x, -hw * 0.7, d * 0.2)), m @ Vector((x, 0, 0)), m @ Vector((x, hw * 0.7, d * 0.2)), m @ Vector((x, hw, d))]
        if prev:
            for i in range(4):
                mb.face([prev[i], ring[i], ring[i + 1], prev[i + 1]], 'wood', col, 0.7)
                mb.face([prev[i + 1], ring[i + 1], ring[i], prev[i]], 'wood', shade(col, 0.7), 0.7)
        prev = ring


def raft(a, rng, collection=None):
    """A timber raft from the sawmill: logs lashed side by side, floating."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    mb.face([(p[0], p[1], 0.05) for p in offset(poly, 3.0)], 'water', hex_rgb('#2a2620'), 0)
    n = max(3, int(W / 0.55))
    for k in range(n):
        y = -W / 2 + (k + 0.5) * W / n
        r = rng.between(0.22, 0.3)
        parts.cyl(mb, 'wood', T(m, -L / 2 + rng.between(-0.5, 0.5), y, 0.12) @ Matrix.Rotation(math.pi / 2, 4, 'Y'), r, L + rng.between(-1, 1), shade(hex_rgb('#7a5a3a'), rng.between(0.7, 1.1)), 0.6, seg=8)
    return _done(mb, a, collection)


def sawdust(a, rng, collection=None):
    """A sawdust mound, pale and smoking a little."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    _mound(mb, c, L / 2, W / 2, rng.between(1.5, 3.0), hex_rgb('#c9a46a'), 'mud', rng, 0.2)
    return _done(mb, a, collection)


def _mound(mb, c, rx, ry, h, col, mat, rng, wear):
    rings, seg = 6, 18
    prev = None
    for k in range(rings + 1):
        t = k / rings
        rr = (1 - t ** 1.5)
        z = h * math.sin(t * math.pi / 2)
        ring = [Vector((c[0] + math.cos(q) * rx * rr * rng.between(0.9, 1.1), c[1] + math.sin(q) * ry * rr * rng.between(0.9, 1.1), z)) for q in (i / seg * math.tau for i in range(seg))]
        if prev:
            for i in range(seg):
                j = (i + 1) % seg
                mb.face([prev[i], prev[j], ring[j], ring[i]], mat, shade(col, rng.between(0.85, 1.05)), wear)
        prev = ring


# ---------------------------------------------------------------- old island
def brazilian(a, rng, collection=None):
    """Afro-Brazilian returnee house: tall arched windows with timber shutters, stucco string
    courses and pilasters, a parapet with a pediment and a date panel, decay showing brick.
    research-buildings 7."""
    poly = ccw([tuple(p) for p in a['poly']])
    s = max(1, min(3, a.get('storeys', 2)))
    gf, uf = 3.8, 3.5
    H = gf + uf * (s - 1)
    wear = rng.between(0.55, 0.95)
    wall = hex_rgb(rng.pick({'#ede3c8': 3, '#e0b04a': 2, '#9cc7e0': 2, '#e6a7a8': 2, '#b5d3a0': 2}))
    trim = hex_rgb('#f2efe6')
    shut = hex_rgb(rng.pick({'#2f5e3a': 3, '#6b1f22': 2, '#5a3a28': 2}))
    mb = MeshBuilder()
    prism(mb, 'paint', poly, 0, H, shade(wall, 0.8), wall, wear)
    prism(mb, 'paint', offset(poly, 0.06), 0, 0.6, shade(wall, 0.6), shade(wall, 0.65), wear + 0.1)
    for k in range(s):  # string courses
        z = gf + uf * (k - 1) if k else None
        if z:
            prism(mb, 'paint', offset(poly, 0.09), z - 0.08, z + 0.14, trim, trim, wear)
    # ornamental parapet hiding the roof, with a pediment and date panel on the street face
    prism(mb, 'paint', poly, H, H + 0.9, wall, wall, wear)
    prism(mb, 'paint', offset(poly, 0.08), H + 0.9, H + 1.05, trim, trim, wear, cap=False)
    prism(mb, 'paint', offset(poly, 0.06), H - 0.25, H, trim, trim, wear)
    mb.face([(p[0], p[1], H + 0.4) for p in offset(poly, -0.2)], 'zinc', hex_rgb('#7a4524'), min(1, wear + 0.2))
    facing = a.get('facing', 0)
    for i in range(len(poly)):
        A, B = poly[i], poly[(i + 1) % len(poly)]
        Lf = math.dist(A, B)
        n = edge_out(poly, i)
        F = frame(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0), (B[0] - A[0], B[1] - A[1]), n)
        k = max(1, int((Lf - 1.0) / 2.3))
        us = [(j - (k - 1) / 2) * (Lf - 1.0) / k for j in range(k)]
        for u in [(-Lf / 2 + 0.3), (Lf / 2 - 0.3)] + [(us[j] + us[j + 1]) / 2 for j in range(len(us) - 1)]:  # pilasters
            mb.box('paint', parts.at(F, u, 0.08, H / 2), trim, wear, size=(0.32, 0.16, H))
        for st in range(s):
            z0 = 0.5 if st == 0 else gf + uf * (st - 1) + 0.45
            for j, u in enumerate(us):
                shop = st == 0 and i == facing and rng.child('shop', j).chance(0.5)
                if shop:  # an old arch punched out for a roller shutter
                    parts.roller_shutter(mb, F, u, 1.8, dict(col=hex_rgb('#9aa3a8'), open=rng.between(0.4, 0.9), wear=wear))
                    continue
                arched_window(mb, F, u, z0 if st else 0.9, 1.0, 2.1 if st else 2.2, trim, shut, wear, rng.child('w', i, st, j), door=(st == 0 and i == facing and j == (k - 1) // 2))
        if i == facing:
            # pediment with a date panel
            peak = H + 2.0
            mb.face([F @ Vector((-2.2, 0.03, H + 1.05)), F @ Vector((2.2, 0.03, H + 1.05)), F @ Vector((0, 0.03, peak))], 'paint', wall, wear)
            mb.box('paint', parts.at(F, 0, 0.06, H + 1.35), trim, wear, size=(1.6, 0.06, 0.45))
            parts.text(mb, 'paint', parts.at(F, 0, 0.1, H + 1.35), str(rng.randrange(1890, 1935)), 0.28, shade(shut, 0.8))
            if s > 1:  # wrought-iron balcony on brackets
                parts.balcony(mb, F, 0, gf + 0.05, min(Lf - 1.2, 6.0), dict(slab=trim, rail='steel', rail_col=hex_rgb('#1f1f1f'), wear=wear))
    # decay: stucco lost in patches, showing brick
    for _ in range(int(wear * 10)):
        i = rng.randrange(len(poly))
        A, B = poly[i], poly[(i + 1) % len(poly)]
        n = edge_out(poly, i)
        F = frame(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0), (B[0] - A[0], B[1] - A[1]), n)
        mb.box('block', parts.at(F, rng.between(-math.dist(A, B) / 2.4, math.dist(A, B) / 2.4), 0.012, rng.between(0.3, H)), hex_rgb('#9a4e34'), 0.8, size=(rng.between(0.3, 1.2), 0.01, rng.between(0.2, 0.8)))
    if rng.chance(wear):  # a weed on the parapet
        p = poly[rng.randrange(len(poly))]
        parts.cyl(mb, 'cloth', Matrix.Translation((p[0], p[1], H + 1.0)), 0.3, 0.5, hex_rgb('#4f7a34'), 0, seg=6, r2=0.05)
    return _done(mb, a, collection)


def arched_window(mb, F, u, z0, w, h, trim, shut, wear, rng, door=False):
    """A tall window (or door) with a round arch head, stucco surround and timber shutters."""
    seg = 8
    r = w / 2
    zs = z0 + h - r  # springing line
    # surround: jambs, sill and the arch made of segments
    for s_ in (-1, 1):
        mb.box('paint', parts.at(F, u + s_ * (r + 0.07), 0.05, (z0 + zs) / 2), trim, wear, size=(0.14, 0.1, zs - z0))
    for k in range(seg):
        a0, a1 = math.pi * k / seg, math.pi * (k + 1) / seg
        p0 = F @ Vector((u + math.cos(a0) * (r + 0.07), 0.05, zs + math.sin(a0) * (r + 0.07)))
        p1 = F @ Vector((u + math.cos(a1) * (r + 0.07), 0.05, zs + math.sin(a1) * (r + 0.07)))
        parts.bar(mb, 'paint', p0, p1, 0.14, trim, wear)
    mb.box('paint', parts.at(F, u, 0.08, zs + r + 0.12), trim, wear, size=(0.22, 0.12, 0.24))  # keystone
    if not door:
        mb.box('paint', parts.at(F, u, 0.1, z0 - 0.06), trim, wear, size=(w + 0.35, 0.2, 0.08))
    # the opening, then shutters: two leaves of horizontal slats, sometimes one missing or ajar
    pts = [F @ Vector((u - r, 0.02, z0)), F @ Vector((u + r, 0.02, z0)), F @ Vector((u + r, 0.02, zs))]
    pts += [F @ Vector((u + math.cos(math.pi * k / seg) * r, 0.02, zs + math.sin(math.pi * k / seg) * r)) for k in range(1, seg)]
    pts += [F @ Vector((u - r, 0.02, zs))]
    mb.face(pts, 'paint', (0.03, 0.025, 0.02), 0)
    for s_ in (-1, 1):
        if rng.chance(0.12 * (1 + wear)):
            continue  # a lost leaf
        ajar = rng.chance(0.3)
        hinge = u + s_ * r
        for k in range(int((zs - z0) / 0.09)):
            z = z0 + 0.05 + k * 0.09
            if ajar:
                c0 = F @ Vector((hinge, 0.04, z))
                c1 = F @ Vector((hinge + s_ * r * 0.7, 0.04 + r * 0.7, z))
                parts.bar(mb, 'wood', c0, c1, 0.035, shut, wear)
            else:
                mb.box('wood', parts.at(F, u + s_ * r / 2, 0.05, z, rx=-0.4), shut, wear, size=(r - 0.02, 0.012, 0.075))


# ---------------------------------------------------------------- estates
def gatehouse(a, rng, collection=None):
    """A gateman's hut: block walls, slab roof with overhang, a window, a door, a boom barrier,
    a plastic chair outside. research-buildings 10.15."""
    poly, c, ang, L, W, m = footprint(a)
    ch = CHARACTER.get(a['district'], 'elite')
    wear = rng.between(*C[ch]['wear'])
    col = hex_rgb(rng.pick(C[ch]['paints']))
    mb = MeshBuilder()
    h = rng.between(2.5, 2.8)
    mb.box('paint', T(m, 0, 0, h / 2), col, wear, size=(L * 0.8, W * 0.8, h))
    mb.box('concrete', T(m, 0, 0, h + 0.08), hex_rgb('#d9d6cf'), wear, size=(L * 0.8 + 0.6, W * 0.8 + 0.6, 0.16))
    F = T(m, 0, -W * 0.4, 0)
    mb.box('glass', T(m, 0.3, -W * 0.4 - 0.01, 1.5), hex_rgb('#24343e'), 0, size=(1.0, 0.03, 0.8))
    mb.box('steel', T(m, -L * 0.25, -W * 0.4 - 0.02, 1.0), hex_rgb('#2b4a66'), wear, size=(0.8, 0.03, 2.0))
    # boom barrier: post, arm striped red and white
    px = L * 0.4 + 0.6
    mb.box('steel', T(m, px, -W * 0.4 - 1.2, 0.5), hex_rgb('#d9d9d9'), wear, size=(0.3, 0.3, 1.0))
    for k in range(8):
        mb.box('steel', T(m, px + 0.25 + k * 0.5, -W * 0.4 - 1.2, 0.95), hex_rgb('#c62828' if k % 2 else '#f2f2f2'), wear, size=(0.5, 0.08, 0.1))
    _chair(mb, T(m, -L * 0.1, -W * 0.4 - 1.2, 0, rz=rng.between(-0.5, 0.5)), hex_rgb(rng.pick(['#d32f2f', '#eeeeee', '#1e88e5'])))
    return _done(mb, a, collection)


def _chair(mb, m, col):
    """A monobloc plastic chair."""
    mb.box('plastic', m @ Matrix.Translation((0, 0, 0.44)), col, 0, size=(0.46, 0.46, 0.04))
    mb.box('plastic', m @ Matrix.Translation((0, -0.22, 0.7)) @ Matrix.Rotation(-0.15, 4, 'X'), col, 0, size=(0.46, 0.04, 0.5))
    for x in (-0.19, 0.19):
        for y in (-0.19, 0.19):
            mb.box('plastic', m @ Matrix.Translation((x, y, 0.21)), col, 0, size=(0.05, 0.05, 0.42))


def generator(a, rng, collection=None):
    """A big standby generator in a soundproof canopy on a pad (estate houses), sometimes in a
    block generator house with a zinc roof."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    mb.box('concrete', T(m, 0, 0, 0.1), hex_rgb('#8f8a80'), 0.4, size=(L, W, 0.2))
    col = hex_rgb(rng.pick({'#3a5f8a': 2, '#2e6b45': 2, '#c8a020': 1, '#8a8f92': 2, '#c62828': 1}))
    gl, gw, gh = L * 0.85, W * 0.8, rng.between(1.4, 1.8)
    mb.box('steel', T(m, 0, 0, 0.2 + gh / 2), col, rng.between(0.1, 0.5), size=(gl, gw, gh))
    for k in range(6):  # louvres on the side
        mb.box('steel', T(m, -gl / 2 + 0.3 + k * 0.1, -gw / 2 - 0.01, 0.2 + gh * 0.55, ), shade(col, 0.7), 0.3, size=(0.06, 0.02, gh * 0.6))
    parts.cyl(mb, 'steel', T(m, gl / 3, 0, 0.2 + gh), 0.08, 0.5, hex_rgb('#3a3a3a'), 0.6, seg=8)
    if rng.chance(0.4):  # a generator house round it
        for (x0, y0, x1, y1) in ((-L / 2, -W / 2, L / 2, -W / 2), (L / 2, -W / 2, L / 2, W / 2), (-L / 2, W / 2, -L / 2, -W / 2)):
            mb.box('block', T(m, (x0 + x1) / 2, (y0 + y1) / 2, 1.3, rz=math.atan2(y1 - y0, x1 - x0)), hex_rgb('#c9c3b6'), 0.4, size=(math.hypot(x1 - x0, y1 - y0) + 0.2, 0.2, 2.6))
        parts.corrugated(mb, T(m, -L / 2 - 0.3, -W / 2 - 0.3, 2.6).translation, T(m, L / 2 + 0.3, -W / 2 - 0.3, 2.6).translation, T(m, L / 2 + 0.3, W / 2 + 0.3, 2.9).translation, T(m, -L / 2 - 0.3, W / 2 + 0.3, 2.9).translation,
                         dict(profile='trapezoid', pitch=0.2, depth=0.03, col=hex_rgb('#9aa3a8'), wear=0.4))
    return _done(mb, a, collection)


def water_tank(a, rng, collection=None):
    """A stand-alone tank tower: a steel or block stand with one to three plastic tanks."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    stand = rng.between(3.0, 5.5)
    n = rng.pick({1: 2, 2: 2, 3: 1})
    col = hex_rgb(rng.pick({'#1d1d1d': 4, '#2f5f9f': 2, '#e8e2d0': 1}))
    r = min(L, W) / (2 if n == 1 else 2.6)
    for k in range(n):
        off = (k - (n - 1) / 2) * r * 2.05
        x, y = (T(m, off, 0, 0).translation.x, T(m, off, 0, 0).translation.y)
        parts.water_tank(mb, x, y, 0, dict(r=r * 0.95, h=r * 2.0, stand=stand, col=col, wear=0.4))
    return _done(mb, a, collection)


# ---------------------------------------------------------------- port
CONTAINER_COLS = {'#b03a2e': 3, '#1f5fa8': 3, '#2e7d4f': 2, '#e07b1a': 2, '#8a8f92': 2, '#e8e6df': 1, '#6b2f2a': 2, '#c8a020': 1}


def container(mb, m, length, col, wear, rng, doors_open=False):
    """An ISO container (2.44 x 2.59 m; 6.06 or 12.19 m long) with ribbed sides and corner castings."""
    w, h = 2.44, 2.59
    mb.box('steel', m @ Matrix.Translation((0, 0, h / 2)), col, wear, size=(length, w, h))
    n = int(length / 0.28)
    for k in range(n):  # the corrugation of the side walls
        x = -length / 2 + (k + 0.5) * length / n
        for s in (-1, 1):
            mb.box('steel', m @ Matrix.Translation((x, s * (w / 2 + 0.015), h / 2)), shade(col, 0.88), wear, size=(length / n * 0.45, 0.03, h - 0.3))
    for x in (-length / 2 + 0.09, length / 2 - 0.09):
        for y in (-w / 2 + 0.09, w / 2 - 0.09):
            for z in (0.09, h - 0.09):
                mb.box('steel', m @ Matrix.Translation((x, y, z)), hex_rgb('#2a2a2a'), wear, size=(0.19, 0.19, 0.19))
    for y in (-w / 4, w / 4):  # door locking bars
        for k in (-1, 1):
            parts.bar(mb, 'steel', m @ Vector((length / 2 + 0.03, y + k * 0.3, 0.2)), m @ Vector((length / 2 + 0.03, y + k * 0.3, h - 0.2)), 0.04, shade(col, 0.7), wear)


def stack(a, rng, collection=None):
    """A row of containers stacked two to five high in a yard."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    high = max(2, a.get('storeys', 2) + rng.randrange(0, 3))
    x = -L / 2
    while x < L / 2 - 6:
        length = 12.19 if rng.chance(0.65) and x + 12.19 <= L / 2 else 6.06
        hh = high - rng.randrange(0, 2)
        for z in range(hh):
            container(mb, T(m, x + length / 2, 0, z * 2.6), length, hex_rgb(rng.pick(CONTAINER_COLS)), rng.between(0.3, 0.9), rng)
        x += length + 0.15
    return _done(mb, a, collection)


def trailer(a, rng, collection=None):
    """An articulated truck: a boxy cab, a flatbed trailer, often with a container on it (queues of
    them wall off the port's roads)."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    cab = hex_rgb(rng.pick({'#e8e6df': 3, '#c62828': 2, '#1f5fa8': 2, '#2e7d4f': 1, '#c8a020': 1}))
    wear = rng.between(0.4, 0.95)
    x0 = L / 2 - 1.3
    mb.box('steel', T(m, x0, 0, 1.9), cab, wear, size=(2.2, 2.45, 2.4))  # cab
    mb.box('glass', T(m, x0 + 1.11, 0, 2.4), hex_rgb('#1c2830'), 0, size=(0.03, 2.1, 0.9))
    mb.box('steel', T(m, x0 + 1.12, 0, 1.2), hex_rgb('#2a2a2a'), wear, size=(0.05, 1.6, 0.6))  # grille
    mb.box('steel', T(m, x0 - 0.2, 0, 3.25), shade(cab, 0.9), wear, size=(1.6, 2.3, 0.3))  # sleeper roof
    for s in (-1, 1):
        parts.cyl(mb, 'steel', T(m, x0 - 1.0, s * 1.0, 1.5), 0.08, 2.0, hex_rgb('#b0b0b0'), wear, seg=8)  # exhaust stacks
    # chassis, wheels, trailer bed
    mb.box('steel', T(m, 0, 0, 1.15), hex_rgb('#2a2a2a'), wear, size=(L - 0.4, 2.4, 0.25))
    for x in [x0 + 0.3, x0 - 2.3, x0 - 3.6] + [-L / 2 + 1.3 + k * 1.3 for k in range(3)]:
        for s in (-1, 1):
            parts.cyl(mb, 'rubber', T(m, x, s * 1.05, 0.52) @ Matrix.Rotation(math.pi / 2, 4, 'X'), 0.52, 0.32, hex_rgb('#1b1b1b'), 0, seg=14)
    if rng.chance(0.75):
        container(mb, T(m, -1.8, 0, 1.3), 12.19, hex_rgb(rng.pick(CONTAINER_COLS)), rng.between(0.3, 0.9), rng)
    return _done(mb, a, collection)


# ---------------------------------------------------------------- markets and yards
def pen(a, rng, collection=None):
    """A livestock pen: timber post-and-rail fence, a zinc shade on poles, a trough, cattle."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    wood = hex_rgb('#6b4f36')
    corners = [(-L / 2, -W / 2), (L / 2, -W / 2), (L / 2, W / 2), (-L / 2, W / 2)]
    for i in range(4):
        (x0, y0), (x1, y1) = corners[i], corners[(i + 1) % 4]
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 2.0))
        for k in range(n + 1):
            x, y = x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n
            parts.bar(mb, 'wood', T(m, x, y, 0).translation, T(m, x + rng.between(-0.05, 0.05), y, 1.4).translation, 0.12, wood, 0.7)
        for z in (0.5, 1.0, 1.35):
            parts.bar(mb, 'wood', T(m, x0, y0, z).translation, T(m, x1, y1, z + rng.between(-0.05, 0.05)).translation, 0.07, wood, 0.7)
    for x in (-L / 4, L / 4):  # shade
        for y in (-W / 4, W / 4):
            parts.bar(mb, 'wood', T(m, x, y, 0).translation, T(m, x, y, 2.6).translation, 0.1, wood, 0.7)
    parts.corrugated(mb, T(m, -L / 3, -W / 3, 2.5).translation, T(m, L / 3, -W / 3, 2.5).translation, T(m, L / 3, W / 3, 2.7).translation, T(m, -L / 3, W / 3, 2.7).translation,
                     dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb('#8a8f92'), wear=0.8))
    mb.box('concrete', T(m, 0, W / 2 - 0.5, 0.25), hex_rgb('#8f8a80'), 0.8, size=(L * 0.5, 0.5, 0.5))
    _mound(mb, (c[0], c[1]), L / 2 - 0.2, W / 2 - 0.2, 0.08, hex_rgb('#5a4430'), 'mud', rng, 0.9)  # trampled dung and mud
    for _ in range(rng.randrange(2, 7)):
        cow(mb, T(m, rng.between(-L / 2.6, L / 2.6), rng.between(-W / 2.8, W / 2.8), 0, rz=rng.between(0, math.tau)), rng)
    return _done(mb, a, collection)


def cow(mb, m, rng):
    """A long-horned humped zebu, the kind walked south to the cattle markets."""
    col = hex_rgb(rng.pick({'#e8e2d6': 4, '#8a4a2a': 2, '#c9a27a': 2, '#3a2a20': 1}))
    parts.cyl(mb, 'skin', m @ Matrix.Translation((-0.7, 0, 1.05)) @ Matrix.Rotation(math.pi / 2, 4, 'Y'), 0.36, 1.45, col, 0, seg=10, r2=0.33)  # body
    parts.cyl(mb, 'skin', m @ Matrix.Translation((0.35, 0, 1.38)), 0.17, 0.25, col, 0, seg=8, r2=0.05)  # hump
    for x in (-0.55, 0.5):
        for y in (-0.18, 0.18):
            parts.cyl(mb, 'skin', m @ Matrix.Translation((x, y, 0)), 0.06, 0.8, col, 0, seg=6, r2=0.07)
    hm = m @ Matrix.Translation((0.95, 0, 1.25)) @ Matrix.Rotation(-0.5, 4, 'Y')
    mb.box('skin', hm, col, 0, size=(0.45, 0.24, 0.24))
    for s in (-1, 1):  # the lyre horns
        parts.bar(mb, 'plastic', hm @ Vector((0.0, s * 0.1, 0.12)), hm @ Vector((0.05, s * 0.45, 0.55)), 0.06, hex_rgb('#e8dcc0'))


def scrap(a, rng, collection=None):
    """A scrap pile: car carcasses, drums, wheels and sheet metal."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    for _ in range(rng.randrange(8, 18)):
        x, y = rng.between(-L / 2.4, L / 2.4), rng.between(-W / 2.4, W / 2.4)
        k = rng.random()
        mm = T(m, x, y, 0, rz=rng.between(0, math.tau))
        if k < 0.35:
            parts.cyl(mb, 'steel', mm, 0.29, 0.88, hex_rgb(rng.pick(['#1f5fa8', '#c62828', '#2e7d4f', '#3a3a3a'])), 0.9, seg=10)  # drum
        elif k < 0.6:
            parts.tyre(mb, mm.translation.x, mm.translation.y, 0.1 + rng.between(0, 0.6))
        else:
            mb.box('steel', mm @ Matrix.Translation((0, 0, rng.between(0.05, 0.8))) @ Matrix.Rotation(rng.between(-0.6, 0.6), 4, 'X'), hex_rgb(rng.pick(['#7a4524', '#8a8f92', '#5a3a28'])), 1.0, size=(rng.between(0.6, 2.0), rng.between(0.4, 1.2), 0.03))
    return _done(mb, a, collection)


def checkpoint(a, rng, collection=None):
    """A road checkpoint: painted drums, old tyres, a plank with nails, a bench and an umbrella."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    for k in range(5):
        x = -L / 2 + k * L / 4
        parts.cyl(mb, 'steel', T(m, x, rng.between(-0.3, 0.3), 0), 0.29, 0.88, hex_rgb(rng.pick(['#c62828', '#f2f2f2', '#1f5fa8'])), 0.8, seg=10)
        parts.tyre(mb, T(m, x + 0.5, 0.6, 0).translation.x, T(m, x + 0.5, 0.6, 0).translation.y, 0.1)
    mb.box('wood', T(m, 0, -0.8, 0.04), hex_rgb('#6b4f36'), 0.8, size=(3.5, 0.25, 0.05))
    for k in range(12):
        mb.box('steel', T(m, -1.6 + k * 0.29, -0.8, 0.1), hex_rgb('#8a8a8a'), 0.5, size=(0.01, 0.01, 0.08))
    mb.box('wood', T(m, 0, W / 2 + 0.6, 0.45), hex_rgb('#6b4f36'), 0.7, size=(2.0, 0.35, 0.06))
    parts.cyl(mb, 'steel', T(m, 1.5, W / 2 + 0.6, 0), 0.025, 2.3, hex_rgb('#cccccc'), 0.3, seg=6)
    parts.cyl(mb, 'cloth', T(m, 1.5, W / 2 + 0.6, 2.0), 1.3, 0.45, hex_rgb(rng.pick(['#1e88e5', '#e53935', '#43a047'])), 0.3, seg=12, r2=0.02)
    return _done(mb, a, collection)


def container_shop(a, rng, collection=None):
    """A 20 or 40 ft container turned into a shop: one side cut open with a roller shutter, a sign."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    col = hex_rgb(rng.pick(CONTAINER_COLS))
    container(mb, T(m, 0, 0, 0.15), min(L, 12.19), col, rng.between(0.4, 0.9), rng)
    for x in (-L / 3, L / 3):
        mb.box('concrete', T(m, x, 0, 0.07), hex_rgb('#8a857a'), 0.5, size=(0.4, 2.5, 0.15))
    F = T(m, 0, -1.25, 0.15)
    parts.roller_shutter(mb, F, 0, min(L - 1.0, 3.2), dict(col=hex_rgb('#9aa3a8'), open=rng.between(0.5, 0.95), wear=0.5))
    return _done(mb, a, collection)


def mound(a, rng, collection=None):
    """A landfill or spoil mound: refuse and earth, with scavengers' paths."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    _mound(mb, c, L / 2, W / 2, rng.between(3, 6), hex_rgb('#4a3e30'), 'mud', rng, 0.9)
    from .street import litter_piece
    for _ in range(int(L * W * 0.8)):
        q, d = rng.between(0, math.tau), rng.between(0, 1)
        x, y = c[0] + math.cos(q) * d * L / 2, c[1] + math.sin(q) * d * W / 2
        litter_piece(mb, x, y, (1 - d ** 1.5) * 4.0, rng)
    return _done(mb, a, collection)


# ---------------------------------------------------------------- the Frontier: half-built land, the refinery
def unfinished_house(a, rng, collection=None):
    """A half-built house on the peninsula: bare grey block walls stopped at different heights,
    concrete columns with rods waiting for the next floor, sometimes the first-floor slab and its
    columns, a sand heap and stacked blocks, and the owner's warning painted on the wall.
    research-housing (unfinished buildings), LAGOS-ISMS #8."""
    poly = ccw([tuple(p) for p in a['poly']])
    mb = MeshBuilder()
    block = hex_rgb('#9c978c')
    stage = rng.pick({'walls': 4, 'slab': 3, 'footing': 1})
    if stage == 'footing':
        for i in range(len(poly)):  # just the footing and the first courses
            A, B = poly[i], poly[(i + 1) % len(poly)]
            mb.box('block', Matrix.Translation(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0.3)) @ Matrix.Rotation(math.atan2(B[1] - A[1], B[0] - A[0]), 4, 'Z'), block, 0.7, size=(math.dist(A, B), 0.25, 0.6))
    else:
        for i in range(len(poly)):  # walls stopped at different heights, gaps for doors and windows
            A, B = poly[i], poly[(i + 1) % len(poly)]
            L = math.dist(A, B)
            h = rng.between(1.2, 3.0)
            n = max(1, int(L / 1.8))
            for k in range(n):
                if rng.chance(0.2):
                    continue  # an opening
                t = (k + 0.5) / n
                mb.box('block', Matrix.Translation((A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t, h / 2)) @ Matrix.Rotation(math.atan2(B[1] - A[1], B[0] - A[0]), 4, 'Z'), block, 0.75, size=(L / n + 0.02, 0.22, h))
        parts.unfinished_storey(mb, poly, 0.0, {}, rng)
        if stage == 'slab':
            pts = [(p[0], p[1], 3.2) for p in poly]
            mb.face(pts, 'concrete', hex_rgb('#8f8a80'), 0.7)
            mb.face([(p[0], p[1], 3.0) for p in poly][::-1], 'concrete', hex_rgb('#7a756c'), 0.7)
            parts.unfinished_storey(mb, poly, 3.2, {}, rng)
    c = centroid(poly)
    if rng.chance(0.7):  # a sand heap and a stack of blocks by the wall
        parts.cyl(mb, 'mud', Matrix.Translation((c[0] + 2.5, c[1] + 2.5, 0)), 1.6, 1.1, hex_rgb('#c9b07a'), 0.3, seg=10, r2=0.1)
        mb.box('block', Matrix.Translation((c[0] - 2.0, c[1] + 2.0, 0.5)), block, 0.6, size=(1.6, 1.2, 1.0))
    if rng.chance(0.5):  # the warning, painted on the first wall
        A, B = poly[0], poly[1]
        F = Matrix.Translation(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0.9)) @ Matrix.Rotation(math.atan2(B[1] - A[1], B[0] - A[0]) + math.pi, 4, 'Z') @ Matrix.Translation((0, -0.12, 0))
        parts.text(mb, 'paint', F, rng.pick(['THIS LAND IS NOT FOR SALE', 'NOT FOR SALE', 'BEWARE OF 419']), 0.35, hex_rgb('#b0302a'), depth=0.01, max_w=math.dist(A, B) * 0.8)
    return _done(mb, a, collection)


def refinery_column(a, rng, collection=None):
    """A refinery column: a tall steel cylinder sized to its footprint, platforms with railings
    every 8 m, a caged ladder and pipes running down its side."""
    poly = ccw([tuple(p) for p in a['poly']])
    mb = MeshBuilder()
    c = centroid(poly)
    r = max(1.0, min(math.dist(poly[0], poly[1]), math.dist(poly[1], poly[2])) * 0.45)
    h = rng.between(30, 48)
    steel = hex_rgb(rng.pick(['#c9ced2', '#b8bcbf', '#e8e6df']))
    parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], 0)), r, h, steel, 0.35, seg=16)
    parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], h)), r, r * 0.5, steel, 0.35, seg=16, r2=0.3)
    for z in range(8, int(h), 8):  # platforms and their railings
        parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], z)), r + 0.9, 0.12, hex_rgb('#5a5a5a'), 0.5, seg=16)
        parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], z + 1.0)), r + 0.9, 0.05, hex_rgb('#e0b020'), 0.4, seg=16, caps=(False, False))
    parts.bar(mb, 'steel', (c[0] + r + 0.3, c[1], 0), (c[0] + r + 0.3, c[1], h), 0.12, hex_rgb('#5a5a5a'), 0.5)  # the ladder
    for k in range(2):  # pipes down the side
        q = (k + 1) * 2.0
        parts.bar(mb, 'steel', (c[0] + math.cos(q) * (r + 0.4), c[1] + math.sin(q) * (r + 0.4), 0), (c[0] + math.cos(q) * (r + 0.4), c[1] + math.sin(q) * (r + 0.4), h * 0.85), 0.25, hex_rgb('#8a8f92'), 0.5)
    return _done(mb, a, collection)


def flare_stack(a, rng, collection=None):
    """The refinery's flare: a red-and-white banded stack of 64 m with guy cables, and the flame on top."""
    poly = ccw([tuple(p) for p in a['poly']])
    mb = MeshBuilder()
    c = centroid(poly)
    h = 64.0
    for k in range(8):  # red and white bands
        parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], k * h / 8)), 1.2 - k * 0.06, h / 8, hex_rgb('#c62828' if k % 2 else '#f4f4f0'), 0.4, seg=12, r2=1.2 - (k + 1) * 0.06)
    for k in range(3):  # guy cables
        q = k / 3 * math.tau
        parts.bar(mb, 'steel', (c[0], c[1], h * 0.7), (c[0] + math.cos(q) * 30, c[1] + math.sin(q) * 30, 0), 0.04, hex_rgb('#3a3a3a'), 0.4)
    parts.cyl(mb, 'emit', Matrix.Translation((c[0], c[1], h)), 1.4, 7.0, hex_rgb('#ff8a1a'), 0, seg=8, r2=0.15)  # the flame
    parts.cyl(mb, 'emit', Matrix.Translation((c[0], c[1], h + 1.0)), 0.8, 4.5, hex_rgb('#ffe08a'), 0, seg=8, r2=0.1)
    return _done(mb, a, collection)


# ---------------------------------------------------------------- the Border: the old town, the beach, the post
def colonial_house(a, rng, collection=None):
    """An old colonial-era house of the border town: two storeys of lime-washed walls, a hipped
    roof of rusted zinc or red tiles, a timber veranda on posts along the front, louvred shutters.
    research-buildings (Badagry's colonial and returnee houses), invented."""
    from .landmarks import first_storey_house
    poly = ccw([tuple(p) for p in a['poly']])
    mb = MeshBuilder()
    wear = rng.between(0.5, 0.85)
    first_storey_house(mb, poly, rng, wear)
    return _done(mb, a, collection)


def fishing_hut(a, rng, collection=None):
    """A beach fishing hut: a pole frame with walls of palm-frond mats, a low thatched roof, nets
    hung out to dry on poles, a canoe pulled up on the sand beside it."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    frond, thatch, pole = hex_rgb('#b59a5e'), hex_rgb('#8a6a3a'), hex_rgb('#5a4632')
    h = rng.between(1.9, 2.4)
    for x in (-L / 2 + 0.2, L / 2 - 0.2):
        for y in (-W / 2 + 0.2, W / 2 - 0.2):
            parts.bar(mb, 'wood', T(m, x, y, 0).translation, T(m, x, y, h + 0.3).translation, 0.1, pole, 0.7)
    for s in (-1, 1):  # frond-mat walls, one side left open
        mb.box('wood', T(m, 0, s * (W / 2 - 0.2), h / 2), frond, 0.7, size=(L - 0.4, 0.06, h))
    mb.box('wood', T(m, -L / 2 + 0.2, 0, h / 2), frond, 0.7, size=(0.06, W - 0.4, h))
    for s in (-1, 1):  # a low thatched gable roof
        mb.face([T(m, -L / 2 - 0.4, s * (W / 2 + 0.4), h).translation, T(m, L / 2 + 0.4, s * (W / 2 + 0.4), h).translation,
                 T(m, L / 2 + 0.4, 0, h + W * 0.45).translation, T(m, -L / 2 - 0.4, 0, h + W * 0.45).translation][::s], 'wood', thatch, 0.8)
    for x in (L / 2 + 1.5, L / 2 + 4.0):  # nets drying on poles
        parts.bar(mb, 'wood', T(m, x, 0, 0).translation, T(m, x, 0, 2.2).translation, 0.06, pole, 0.7)
    mb.box('cloth', T(m, L / 2 + 2.75, 0, 1.4), hex_rgb(rng.pick(['#2f6fa6', '#2e7d4f', '#c8a020'])), 0.5, size=(2.5, 0.03, 1.6))
    if rng.chance(0.6):
        canoe(mb, T(m, 0, W / 2 + 2.0, 0.0, rng.between(-0.3, 0.3)), rng)
    return _done(mb, a, collection)


def border_booth(a, rng, collection=None):
    """A booth at the border post: a small rendered cabin painted in two bands, a window with a
    counter, a striped barrier pole across the lane beside it."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    wear = rng.between(0.4, 0.7)
    band = hex_rgb(rng.pick(['#2e7d4f', '#1f5fa8', '#c8a020']))
    mb.box('paint', T(m, 0, 0, 1.25), hex_rgb('#efe8d8'), wear, size=(L, W, 2.5))
    mb.box('paint', T(m, 0, 0, 0.5), band, wear, size=(L + 0.02, W + 0.02, 1.0))
    mb.box('zinc', T(m, 0, 0, 2.6), hex_rgb('#8a8d8c'), wear + 0.2, size=(L + 0.8, W + 0.8, 0.12))
    mb.box('glass', T(m, L / 2 + 0.01, 0, 1.6), hex_rgb('#24343e'), 0.1, size=(0.02, W * 0.6, 0.9))
    mb.box('wood', T(m, L / 2 + 0.25, 0, 1.05), hex_rgb('#6b4a30'), wear, size=(0.5, W * 0.6, 0.06))  # counter
    parts.bar(mb, 'steel', T(m, L / 2 + 0.6, W / 2, 1.0).translation, T(m, L / 2 + 0.6, W / 2 + 6.0, 1.0).translation, 0.08, hex_rgb('#c62828'), 0.3)
    for k in range(6):
        mb.box('paint', T(m, L / 2 + 0.6, W / 2 + 0.5 + k, 1.0), hex_rgb('#f2f2ee'), 0.3, size=(0.1, 0.45, 0.1))
    return _done(mb, a, collection)


def border_canopy(a, rng, collection=None):
    """The border post's big canopy over the lanes, like a toll plaza's, with an invented crest
    and the words BORDER POST on its fascia."""
    from .places import toll_canopy
    poly, c, ang, L, W, m = footprint(a)
    ob, spec = toll_canopy(a, rng, collection)
    mb = MeshBuilder()
    for s in (-1, 1):  # the fascia sign on both faces
        F = T(m, s * (L / 2 + 1.05), 0, 7.2, -s * math.pi / 2 + math.pi)
        mb.box('paint', F, hex_rgb('#2e7d4f'), 0.3, size=(W * 0.6, 0.05, 0.7))
        parts.text(mb, 'paint', F @ Matrix.Translation((0, -0.05, 0)), 'BORDER POST', 0.5, hex_rgb('#f4f4f0'), depth=0.02, max_w=W * 0.5)
    _done(mb, a, collection)
    return ob, spec


def drums(a, rng, collection=None):
    """Drums and jerrycans of fuel stacked by the road, the border's smuggled fuel: blue and
    rusty steel drums in rows, yellow jerrycans on top, a funnel and a hose."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    nx, ny = max(1, int(L / 0.7)), max(1, int(W / 0.7))
    for i in range(nx):
        for j in range(ny):
            if rng.chance(0.15):
                continue
            x, y = -L / 2 + (i + 0.5) * L / nx, -W / 2 + (j + 0.5) * W / ny
            parts.cyl(mb, 'steel', T(m, x, y, 0), 0.29, 0.88, hex_rgb(rng.pick(['#1f5fa8', '#2f6fa6', '#6b3a22', '#3a3a3a'])), 0.8, seg=10)
            if rng.chance(0.4):
                mb.box('plastic', T(m, x, y, 1.05), hex_rgb('#e0b020'), 0.5, size=(0.36, 0.2, 0.34))
    parts.cyl(mb, 'plastic', T(m, L / 2 + 0.4, 0, 0), 0.15, 0.3, hex_rgb('#c62828'), 0.5, seg=8, r2=0.03)  # a funnel
    return _done(mb, a, collection)
