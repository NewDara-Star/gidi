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
from .core import MissingRecord, hex_rgb, shade

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
    """One gutter: pts in the kit's frame, g its record (w, depth, state, blocked) with its pieces' records (pieces: per
    piece ww, how dirty its walls are; inside, what lies in it; slabs over it). The old city's generators give no pieces:
    they are drafted from the gutter's own dice (draft.gutter)."""
    w = g['w']
    recs = g.get('pieces')
    if recs is None:
        from . import draft
        recs = draft.gutter(pts, g, keep, wear)
    recs = iter(recs)
    proud = g['proud_m'] if 'proud_m' in g else 0.12 + 0.1 * min(1.0, g.get('depth', 0.6))   # deeper drains have taller walls;
    # the map can set the walls' top itself (proud_m, m above the ground: 0 or less sits the slabs flush with it)
    t = 0.12
    blocked = g.get('blocked') or []
    covered = g['state'] == 'covered'
    for a, b, s in pieces(pts, keep, 4.0 if detail.web() else PIECE):
        L = math.dist(a, b)
        if L < 0.05:
            continue
        rec = next(recs, None)
        if rec is None:
            raise MissingRecord('gutter %s: fewer piece records than pieces' % g.get('id'))
        dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nx, ny = -dy, dx
        P = lambda u, o, z: (a[0] + dx * u + nx * o, a[1] + dy * u + ny * o, z)
        ww = rec['ww']
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
            _inside(mb, P, L, w, proud, fill, rec['inside'])
        if covered:
            _slabs(mb, P, L, w, t, proud, dx, dy, wear, g, rec['slabs'])


def _inside(mb, P, L, w, proud, fill, ins):
    """Inside an open gutter: silt, then water (high and green where it's blocked), or rubbish heaped to the rim.
    ins: its record (rubbish: pieces at u along, o across, z, with col, size, rz, rx; or zw, the water's height, mix, how
    much silt or scum shows at each corner, and caught, what floats in it)."""
    if fill == 'rubbish' or not detail.web():   # under water the silt doesn't show in the web tiles
        mb.face([P(0, -w / 2, 0.02), P(L, -w / 2, 0.02), P(L, w / 2, 0.02), P(0, w / 2, 0.02)], 'mud', SILT, 0.7)
    if fill == 'rubbish':
        mb.face([P(0, -w / 2, proud * 0.7), P(L, -w / 2, proud * 0.85), P(L, w / 2, proud * 0.75), P(0, w / 2, proud * 0.8)], 'mud',
                [shade(SILT, 1.6), shade(SILT, 1.3), shade(SILT, 1.8), shade(SILT, 1.4)], 0.8)
        for r in ins['rubbish']:   # bottles, nylon, sachets, a slipper
            mb.box('plastic', Matrix.Translation(P(r['u'], r['o'], r['z'])) @ Matrix.Rotation(r['rz'], 4, 'Z') @ Matrix.Rotation(r['rx'], 4, 'X'), tuple(r['col']), 0.5, size=r['size'])
    else:
        green = fill == 'green_water'
        zw = ins['zw']
        q = [P(0, -w / 2, zw), P(L, -w / 2, zw), P(L, w / 2, zw), P(0, w / 2, zw)]
        if green:   # scum gathers along the walls
            cols = [_mix(GREEN, SCUM, m) for m in ins['mix']]
        else:
            cols = [_mix(WATER, SILT, m) for m in ins['mix']]
        mb.face(q, 'mud', cols, 0.2)   # not 'water': that slot is the lagoon's one colour in Unreal
        for c in ins['caught']:   # something caught in an open drain
            mb.box('plastic', Matrix.Translation(P(c['u'], c['o'], zw + 0.02)) @ Matrix.Rotation(c['rz'], 4, 'Z'), tuple(c['col']), 0.5, size=c['size'])


def _slab(mb, P, u, L_, w, t, z, ang, tip, roll, c, wear, broken):
    """One precast slab across the channel, centred u along it, L_ long: tipped (tip, about the gutter's line) and rocked
    (roll, across it). Broken: {split: [where, tip of each half]} in two pieces with a crack between, or {corner: [side,
    cut, the fallen lump's tilts]} a corner knocked off."""
    span = w + 2 * t + 0.04
    base = lambda du, dv, rx, ry: Matrix.Translation(P(u + du, dv, z)) @ Matrix.Rotation(ang, 4, 'Z') @ Matrix.Rotation(rx, 4, 'X') @ Matrix.Rotation(ry, 4, 'Y')
    if broken and 'split' in broken:   # cracked across the channel, the two halves at their own tilts
        f, t1, t2 = broken['split']
        a_, b_ = span * f, span * (1 - f)
        mb.box('concrete', base(0, -span / 2 + a_ / 2 - 0.01, tip + t1, roll), c, wear, size=(L_, a_ - 0.02, 0.1), skip=('-z',))
        mb.box('concrete', base(0, span / 2 - b_ / 2 + 0.01, tip + t2, roll - 0.02), shade(c, 0.93), wear, size=(L_, b_ - 0.02, 0.1), skip=('-z',))
    elif broken and 'corner' in broken:   # a corner gone: the slab short on one side, a lump of it fallen beside
        s_, cut, rx, ry = broken['corner']
        mb.box('concrete', base(0, -s_ * cut / 2, tip, roll), c, wear, size=(L_, span - cut, 0.1), skip=('-z',))
        mb.box('concrete', base(-L_ * 0.25, s_ * (span / 2 - cut / 2), tip, roll), c, wear, size=(L_ * 0.5, cut, 0.1), skip=('-z',))
        mb.box('concrete', base(L_ * 0.2, s_ * (span / 2 + 0.15), rx, ry) @ Matrix.Translation((0, 0, -0.07)), shade(c, 0.9), wear, size=(0.12, 0.09, 0.06))
    else:
        mb.box('concrete', base(0, 0, tip, roll), c, wear, size=(L_, span, 0.1), skip=('-z',))


def _slabs(mb, P, L, w, t, proud, dx, dy, wear, g, recs):
    """Precast slabs across a covered gutter, 0.6 m each (pairs in the web tiles), gaps between. From the map (`g`):
    `slab_colour`; `dust` 0..1 settled on them; `litter` > 0, dirt packed into the joints. recs: each slab's record
    ({gone} where the drain shows; or tip, roll, sink, its dirt, dust and shade, the gap after it, broken, and joint: the
    rubbish in the joint after it)."""
    n = len(recs)
    base_c = hex_rgb(g['slab_colour']) if g.get('slab_colour') else SLAB
    ang = math.atan2(dy, dx)
    for k, r in enumerate(recs):
        u = (k + 0.5) * L / n
        if r.get('gone'):   # this slab is gone: the drain shows
            continue
        c = shade(_mix(_mix(base_c, WALL_DIRTY, r['dirt'] * wear), DUST, g.get('dust', 0.0) * r['dust']), r['shade'])
        _slab(mb, P, u, L / n - r['gap'], w, t, proud + 0.05 - r['sink'], ang, r['tip'], r['roll'], c, wear, r['broken'])
        if g.get('litter', 0.0) > 0:   # the joint after this slab: dirt packed in, and what the wind left there
            uj = (k + 1) * L / n
            mb.face([P(uj - 0.04, -w / 2 - t, proud + 0.02), P(uj + 0.04, -w / 2 - t, proud + 0.02), P(uj + 0.04, w / 2 + t, proud + 0.03), P(uj - 0.04, w / 2 + t, proud + 0.03)], 'mud', DIRT, 0.8)
            for j in r['joint']:
                mb.box('plastic', Matrix.Translation(P(uj + j['du'], j['o'], proud + 0.1)) @ Matrix.Rotation(j['rz'], 4, 'Z') @ Matrix.Rotation(j['rx'], 4, 'X'), tuple(j['col']), 0.5, size=j['size'])
