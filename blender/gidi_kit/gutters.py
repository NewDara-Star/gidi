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
            top = _mix(WALL, WALL_DIRTY, ww * 0.6)
            foot = _mix(WALL, WALL_DIRTY, ww * 0.8)
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
            _slabs(mb, P, L, w, t, proud, dx, dy, rng, wear)


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


def _slabs(mb, P, L, w, t, proud, dx, dy, rng, wear):
    """Precast slabs across a covered gutter, 0.6 m each (pairs in the web tiles), gaps between; some cracked and tipped, some sunk."""
    n = max(1, round(L / (1.2 if detail.web() else 0.6)))   # the web tiles: slabs in pairs
    for k in range(n):
        u = (k + 0.5) * L / n
        tip = rng.between(-0.08, 0.08) if rng.chance(0.15 + 0.3 * wear) else 0.0
        sink = rng.between(0.02, 0.08) if rng.chance(0.1 + 0.2 * wear) else 0.0
        c = shade(_mix(SLAB, WALL_DIRTY, rng.between(0.1, 0.5) * wear), rng.between(0.85, 1.08))
        m = Matrix.Translation(P(u, 0, proud + 0.05 - sink)) @ Matrix.Rotation(math.atan2(dy, dx), 4, 'Z') @ Matrix.Rotation(tip, 4, 'X')
        mb.box('concrete', m, c, wear, size=(L / n - 0.03, w + 2 * t + 0.04, 0.1), skip=('-z',))
