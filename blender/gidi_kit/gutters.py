"""The gutters the data lays along the roads (scripts/isms.py, GD['gutters']): open or covered with slabs, and the stretches
it marks blocked, with green water or rubbish.

A Lagos gutter is a concrete U-channel beside the carriageway: block walls a hand or two proud of the ground, black silt
and green-black water in it, plastic and nylon caught in it; where it's covered, a row of precast slabs, some cracked,
some sunk or tipped. The kit's ground is one surface at the ground's height, so the channel stands on it rather than in
it: the walls proud, the silt and water low inside them. Cut into short pieces so it follows the terrain.
"""
import math

from mathutils import Matrix

from . import detail
from .core import Rng, hex_rgb, shade

WALL = hex_rgb('#8a857a')
WALL_DIRTY = hex_rgb('#4a4a40')
SILT = hex_rgb('#26251f')
WATER = hex_rgb('#24301f')       # the usual: black-green, barely moving
GREEN = hex_rgb('#2f3d1e')       # blocked: standing green water with scum
SCUM = hex_rgb('#58613a')
SLAB = hex_rgb('#9a958b')
DUST = hex_rgb('#5b4c3e')         # the street's dust, settled on slabs and walls
DIRT = hex_rgb('#3a2e24')         # packed into the joints
RUBBISH = [hex_rgb(c) for c in ('#d9d4c8', '#cfc9bb', '#e2ddd2', '#1c1c1c', '#262626', '#3d5f86', '#8a3a30', '#b8ad8c', '#6b5b45', '#5d7a8c')]   # sachets, black nylon, faded bottles
PIECE = 2.4


def _mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def pieces(pts, keep, piece=PIECE):
    """The gutter's line cut into pieces of about PIECE metres: (a, b, distance along the gutter at a) for those keep() wants."""
    d = 0.0
    for p, q in zip(pts, pts[1:]):
        L = math.dist(p, q)
        n = max(1, math.ceil(L / piece))
        for i in range(n):
            a = (p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n)
            b = (p[0] + (q[0] - p[0]) * (i + 1) / n, p[1] + (q[1] - p[1]) * (i + 1) / n)
            if keep(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)):
                yield a, b, d + L * i / n
        d += L


def gutter(mb, pts, g, keep, wear=0.6):
    """One gutter from the data: pts in the kit's frame, g its record (w, depth, state, blocked)."""
    w = g['w']
    rng = Rng('gutter', g['id'])
    proud = 0.12 + 0.1 * min(1.0, g.get('depth', 0.6))   # deeper drains have taller walls
    t = 0.12
    blocked = g.get('blocked') or []
    covered = g['state'] == 'covered'
    for a, b, s in pieces(pts, keep, 4.0 if detail.web() else PIECE):
        L = math.dist(a, b)
        if L < 0.05:
            continue
        dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nx, ny = -dy, dx
        P = lambda u, o, z: (a[0] + dx * u + nx * o, a[1] + dy * u + ny * o, z)
        ww = wear * rng.between(0.7, 1.2)
        # the two walls: outer face, top, inner face (dark with the wet below the top)
        for side in (-1, 1):
            o_in, o_out = side * w / 2, side * (w / 2 + t)
            top = _mix(_mix(WALL, WALL_DIRTY, ww * 0.6), DUST, g.get('dust', 0.0))
            foot = _mix(_mix(WALL, WALL_DIRTY, ww * 0.8), DUST, g.get('dust', 0.0))
            faces = ([P(0, o_out, 0), P(L, o_out, 0), P(L, o_out, proud), P(0, o_out, proud)], [foot, foot, top, top]), \
                    ([P(0, o_out, proud), P(L, o_out, proud), P(L, o_in, proud), P(0, o_in, proud)], [top] * 4), \
                    ([P(0, o_in, proud), P(L, o_in, proud), P(L, o_in, 0.0), P(0, o_in, 0.0)], [top, top, SILT, SILT])
            if covered and detail.web():   # under the slabs: only the outer faces show
                faces = faces[:1]
            for q, cs in faces:   # wound for the right-hand wall; the left-hand one turns them round to face out
                mb.face(q if side < 0 else q[::-1], 'concrete', cs if side < 0 else cs[::-1], ww)
        fill = next((bk['fill'] for bk in blocked if bk['from'] <= s + L / 2 < bk['to']), None)
        if not (covered and detail.web()):   # in the web tiles the slabs hide what's inside
            _inside(mb, P, L, w, proud, fill, covered, rng, wear)
        if covered:
            _slabs(mb, P, L, w, t, proud, dx, dy, rng, wear, g)


def _inside(mb, P, L, w, proud, fill, covered, rng, wear):
    """Inside an open gutter: silt, then water (high and green where it's blocked), or rubbish heaped to the rim."""
    if fill == 'rubbish' or not detail.web():   # under water the silt doesn't show in the web tiles
        mb.face([P(0, -w / 2, 0.02), P(L, -w / 2, 0.02), P(L, w / 2, 0.02), P(0, w / 2, 0.02)], 'mud', SILT, 0.7)
    if fill == 'rubbish':
        mb.face([P(0, -w / 2, proud * 0.7), P(L, -w / 2, proud * 0.85), P(L, w / 2, proud * 0.75), P(0, w / 2, proud * 0.8)], 'mud',
                [shade(SILT, 1.6), shade(SILT, 1.3), shade(SILT, 1.8), shade(SILT, 1.4)], 0.8)
        for _ in range(int(L * 6)):   # bottles, nylon, sachets, a slipper
            u, o = rng.between(0, L), rng.between(-w / 2, w / 2)
            z = proud * rng.between(0.7, 1.15)
            c = rng.pick(RUBBISH)
            sz = (rng.between(0.06, 0.2), rng.between(0.04, 0.14), rng.between(0.01, 0.05))   # flat: sachets, bags, crushed bottles
            mb.box('plastic', Matrix.Translation(P(u, o, z)) @ Matrix.Rotation(rng.between(0, 3.14), 4, 'Z') @ Matrix.Rotation(rng.between(-0.6, 0.6), 4, 'X'), c, 0.5, size=sz)
    else:
        green = fill == 'green_water'
        zw = proud * (0.75 if green else rng.between(0.25, 0.45))
        q = [P(0, -w / 2, zw), P(L, -w / 2, zw), P(L, w / 2, zw), P(0, w / 2, zw)]
        if green:   # scum gathers along the walls
            cols = [_mix(GREEN, SCUM, rng.between(0.2, 0.7)) for _ in range(4)]
        else:
            cols = [_mix(WATER, SILT, rng.between(0.0, 0.5)) for _ in range(4)]
        mb.face(q, 'mud', cols, 0.2)   # not 'water': that slot is the lagoon's one colour in Unreal
        if not covered and rng.chance(0.25 * wear):   # something caught in an open drain
            for _ in range(rng.randrange(1, 4)):
                u, o = rng.between(0.2, L - 0.2), rng.between(-w / 3, w / 3)
                mb.box('plastic', Matrix.Translation(P(u, o, zw + 0.02)) @ Matrix.Rotation(rng.between(0, 3.14), 4, 'Z'), rng.pick(RUBBISH), 0.5,
                       size=(rng.between(0.1, 0.25), rng.between(0.06, 0.15), 0.04))


def _slab(mb, P, u, L_, w, t, z, ang, tip, roll, c, wear, rng, broken):
    """One precast slab across the channel, centred u along it, L_ long: tipped (tip, about the gutter's line) and rocked
    (roll, across it). Broken: in two pieces with a crack between, or a corner knocked off."""
    span = w + 2 * t + 0.04
    base = lambda du, dv, rx, ry: Matrix.Translation(P(u + du, dv, z)) @ Matrix.Rotation(ang, 4, 'Z') @ Matrix.Rotation(rx, 4, 'X') @ Matrix.Rotation(ry, 4, 'Y')
    if broken == 'split':   # cracked across the channel, the two halves at their own tilts
        f = rng.between(0.35, 0.65)
        a_, b_ = span * f, span * (1 - f)
        mb.box('concrete', base(0, -span / 2 + a_ / 2 - 0.01, tip + rng.between(-0.06, 0.06), roll), c, wear, size=(L_, a_ - 0.02, 0.1), skip=('-z',))
        mb.box('concrete', base(0, span / 2 - b_ / 2 + 0.01, tip + rng.between(-0.06, 0.06), roll - 0.02), shade(c, 0.93), wear, size=(L_, b_ - 0.02, 0.1), skip=('-z',))
    elif broken == 'corner':   # a corner gone: the slab short on one side, a lump of it fallen beside
        s_ = rng.pick([-1, 1])
        cut = rng.between(0.15, 0.3)
        mb.box('concrete', base(0, -s_ * cut / 2, tip, roll), c, wear, size=(L_, span - cut, 0.1), skip=('-z',))
        mb.box('concrete', base(-L_ * 0.25, s_ * (span / 2 - cut / 2), tip, roll), c, wear, size=(L_ * 0.5, cut, 0.1), skip=('-z',))
        mb.box('concrete', base(L_ * 0.2, s_ * (span / 2 + 0.15), rng.between(-0.5, 0.5), rng.between(-0.5, 0.5)) @ Matrix.Translation((0, 0, -0.07)), shade(c, 0.9), wear, size=(0.12, 0.09, 0.06))
    else:
        mb.box('concrete', base(0, 0, tip, roll), c, wear, size=(L_, span, 0.1), skip=('-z',))


def _slabs(mb, P, L, w, t, proud, dx, dy, rng, wear, g=None):
    """Precast slabs across a covered gutter, 0.6 m each (pairs in the web tiles), gaps between; some cracked and tipped,
    some sunk. From the map (`g`): `slab_colour`; `dust` 0..1 settled on them; `open_share`, the share of slabs gone, the
    drain open between the ones left; `broken` 0..1, how many are cracked or chipped; `rock` 0..1, how much they tip and
    rock; `litter` 0..1, dirt and rubbish packed into the joints."""
    g = g or {}
    n = max(1, round(L / (1.2 if detail.web() else 0.6)))   # the web tiles: slabs in pairs
    base_c = hex_rgb(g['slab_colour']) if g.get('slab_colour') else SLAB
    rock = g.get('rock', 0.0)
    ang = math.atan2(dy, dx)
    for k in range(n):
        u = (k + 0.5) * L / n
        if rng.chance(g.get('open_share', 0.0)):   # this slab is gone: the drain shows
            continue
        tip = rng.between(-0.08, 0.08) if rng.chance(0.15 + 0.3 * wear + 0.5 * rock) else 0.0
        roll = rng.between(-0.06, 0.06) * rock
        sink = rng.between(0.02, 0.08) if rng.chance(0.1 + 0.2 * wear + 0.3 * rock) else 0.0
        c = shade(_mix(_mix(base_c, WALL_DIRTY, rng.between(0.1, 0.5) * wear), DUST, g.get('dust', 0.0) * rng.between(0.6, 1.0)), rng.between(0.8, 1.05))
        gap = 0.03 + rng.between(0.0, 0.06) * rock
        broken = rng.pick(['split', 'corner']) if rng.chance(g.get('broken', 0.0)) else None
        _slab(mb, P, u, L / n - gap, w, t, proud + 0.05 - sink, ang, tip, roll, c, wear, rng, broken)
        if g.get('litter', 0.0) > 0:   # the joint after this slab: dirt packed in, and what the wind left there
            uj = (k + 1) * L / n
            mb.face([P(uj - 0.04, -w / 2 - t, proud + 0.02), P(uj + 0.04, -w / 2 - t, proud + 0.02), P(uj + 0.04, w / 2 + t, proud + 0.03), P(uj - 0.04, w / 2 + t, proud + 0.03)], 'mud', DIRT, 0.8)
            for _ in range(int(rng.between(0, 4) * g['litter'])):
                o = rng.between(-w / 2 - t, w / 2 + t)
                sz = (rng.between(0.05, 0.16), rng.between(0.04, 0.1), rng.between(0.008, 0.03))
                mb.box('plastic', Matrix.Translation(P(uj + rng.between(-0.05, 0.05), o, proud + 0.1)) @ Matrix.Rotation(rng.between(0, 3.14), 4, 'Z') @ Matrix.Rotation(rng.between(-0.5, 0.5), 4, 'X'), rng.pick(RUBBISH), 0.5, size=sz)
