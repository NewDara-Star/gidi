"""Kit pieces. Each adds faces to a MeshBuilder, in world space, from a spec dict that the
rules fill in (so the look of every piece is chosen from data, never hard-wired here)."""
import math
import os

import bpy
from mathutils import Matrix, Vector

from . import detail
from . import wear as wear_
from . import zinc
from .core import at, chamfer, edge_out, frame, offset, prism, shade

STOREY = 3.1


# ---------------------------------------------------------------- primitives
def cyl(mb, mat, m, r, h, col, wear=0.0, seg=12, caps=(True, True), r2=None):
    """Cylinder along local z from 0 to h (r2: top radius)."""
    r2 = r if r2 is None else r2
    seg = detail.segs(seg)
    ring = lambda rad, z: [m @ Vector((math.cos(a) * rad, math.sin(a) * rad, z)) for a in (i / seg * math.tau for i in range(seg))]
    lo, hi = ring(r, 0), ring(r2, h)
    fix = (lambda q: q[::-1]) if m.to_3x3().determinant() < 0 else (lambda q: q)   # under a mirror (a wall frame) keep them facing out
    for i in range(seg):
        j = (i + 1) % seg
        mb.face(fix([lo[i], lo[j], hi[j], hi[i]]), mat, col, wear)
    if caps[0]:
        mb.face(fix(list(reversed(lo))), mat, col, wear)
    if caps[1]:
        mb.face(fix(hi), mat, col, wear)


def bar(mb, mat, a, b, t, col, wear=0.0):
    """A square bar of thickness t from point a to point b (world)."""
    a, b = Vector(a), Vector(b)
    d = (b - a)
    l = d.length
    if l < 1e-6:
        return
    z = d / l
    x = z.cross(Vector((0, 0, 1)) if abs(z.z) < 0.9 else Vector((1, 0, 0))).normalized()
    y = z.cross(x)
    m = Matrix((
        (x.x, y.x, z.x, (a.x + b.x) / 2),
        (x.y, y.y, z.y, (a.y + b.y) / 2),
        (x.z, y.z, z.z, (a.z + b.z) / 2),
        (0, 0, 0, 1)))
    mb.box(mat, m, col, wear, size=(t, t, l))


_FONT = None


def font():
    """A heavy sans font if the machine has one (signs are hand-lettered in that spirit), else Blender's own."""
    global _FONT
    try:
        if _FONT:
            _FONT.name  # still alive after a scene reset?
    except ReferenceError:
        _FONT = None
    if _FONT is None:
        for p in ('/System/Library/Fonts/Supplemental/Impact.ttf', '/System/Library/Fonts/Supplemental/Arial Black.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
            if os.path.exists(p):
                _FONT = bpy.data.fonts.load(p)
                break
        else:
            _FONT = False
    return _FONT or None


def text(mb, mat, m, s, size, col, depth=0.004, max_w=None, wobble=None):
    """3D lettering merged into the builder. m: frame whose x runs along the text, y out of the board."""
    if detail.web():
        detail.record_text(m, s, size, col, w=max_w)
        return
    cu = bpy.data.curves.new('t', 'FONT')
    cu.body = s
    cu.size = size
    cu.extrude = 0 if detail.web() else depth
    cu.resolution_u = 1 if detail.web() else 12
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    cu.space_line = 0.9
    f = font()
    if f:
        cu.font = f
    ob = bpy.data.objects.new('t', cu)
    bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    xs = [v.co.x for v in me.vertices] or [0]
    w = max(xs) - min(xs)
    sx = min(1.0, max_w / w) if max_w and w > 0 else 1.0
    # text lies in its x-y plane facing +z: stand it up on the board (x along, z up, facing +y)
    stand = Matrix(((sx, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))
    if wobble:  # hand lettering: a slight tilt
        stand = Matrix.Rotation(wobble, 4, 'Y') @ stand
    mb.merge_mesh(me, m @ stand, mat, col)
    ev.to_mesh_clear()
    bpy.data.objects.remove(ob)
    bpy.data.curves.remove(cu)


# ---------------------------------------------------------------- walls
def walls(mb, poly, H, spec):
    """Rendered walls with chamfered corners, a plinth, floor bands. Darker at the foot (baked occlusion)."""
    col, wear = spec['paint'], spec['wear']
    oct_ = chamfer(poly, spec.get('chamfer', 0.18))
    lift = spec.get('lift', 0.0)
    bands = [k * STOREY + lift for k in range(1, spec['storeys'])]
    # the paint, weathered (gidi_kit/wear.py): cut into columns and bands so it can fade, blotch and take the red splash at the foot
    wx = spec.get('_wx') or wear_.Weather(col, wear, H, (round(poly[0][0], 1), round(poly[0][1], 1)))
    spec['_wx'] = wx
    if spec.get('roof', {}).get('form') == 'flat':   # rain off a parapet's coping streaks the wall under it most
        wx.top, wx.top_k = H + spec['parapet']['parapet_h'] + 0.12, 0.4
    wx.prism(mb, 'block' if spec.get('bare') else 'paint', oct_, 0, H, rows=[0.45, 0.8, 1.15, wx.top - 1.8, wx.top - 0.9] + [z + d for z in bands for d in (-0.6, 0.6)])
    ph = spec.get('plinth_h', 0.45)
    prism(mb, 'paint', offset(oct_, 0.04), 0, ph, wx.foot(spec['plinth'], 0), wx.foot(spec['plinth'], ph), wear + 0.1)
    for k in range(1, spec['storeys']):
        prism(mb, 'paint', offset(oct_, 0.07), k * STOREY + lift - 0.1, k * STOREY + lift + 0.08, spec['trim'], spec['trim'], wear)
    return oct_


# ---------------------------------------------------------------- windows and bars
def burglar_bars(mb, F, u, z, w, h, pattern, col, wear):
    """Burglar-proof bars in front of a window. F: wall frame (x along, y out, z up)."""
    y, t = 0.17, 0.03
    p = lambda x, zz: F @ Vector((u + x, y, z + zz))
    hw, hh = w / 2 + 0.04, h / 2 + 0.04
    # the outer frame of flat bar
    for a, b in (((-hw, -hh), (hw, -hh)), ((hw, -hh), (hw, hh)), ((hw, hh), (-hw, hh)), ((-hw, hh), (-hw, -hh))):
        bar(mb, 'steel', p(*a), p(*b), 0.04, col, wear)
    if detail.web():
        for x in (-hw / 2, 0, hw / 2):
            bar(mb, 'steel', p(x, -hh), p(x, hh), t, col, wear)
        return
    if pattern in ('vertical', 'diamond', 'grid', 'sunray', 'scroll'):
        n = max(3, round(w / 0.13))
        for i in range(1, n):
            x = -hw + i * 2 * hw / n
            bar(mb, 'steel', p(x, -hh), p(x, hh), t, col, wear)
    if pattern in ('grid', 'diamond'):
        for zz in (-hh / 3, hh / 3):
            bar(mb, 'steel', p(-hw, zz), p(hw, zz), t, col, wear)
    if pattern == 'diamond':
        r = min(hw, hh) * 0.45
        for a, b in (((-r, 0), (0, r)), ((0, r), (r, 0)), ((r, 0), (0, -r)), ((0, -r), (-r, 0))):
            bar(mb, 'steel', p(*a), p(*b), t, col, wear)
    if pattern == 'sunray':  # rays fanning from the bottom middle
        for k in range(7):
            a = math.pi * (k + 1) / 8
            bar(mb, 'steel', p(0, -hh), p(math.cos(a) * hw * 0.95, -hh + math.sin(a) * hh * 1.9), t, col, wear)
    if pattern == 'scroll':  # S-scrolls between the verticals, top and bottom
        for zz in (-hh * 0.6, hh * 0.6):
            for k in range(8):
                a0, a1 = k / 8 * math.tau, (k + 1) / 8 * math.tau
                for cx in (-hw / 2, hw / 2):
                    rr = min(hw, hh) * 0.22
                    bar(mb, 'steel', p(cx + math.cos(a0) * rr, zz + math.sin(a0) * rr), p(cx + math.cos(a1) * rr, zz + math.sin(a1) * rr), 0.025, col, wear)


def window(mb, F, u, z, spec):
    """A window on a wall frame F at (u along, z centre height). spec from rules.window_spec."""
    w, h, wear = spec['w'], spec['h'], spec['wear']
    trim, glass = spec['frame'], spec['glass']
    # reveal: a dark recess, then the frame, then the glass inset
    mb.box('paint', at(F, u, 0.01, z), trim, wear, size=(w + 0.16, 0.06, h + 0.16), skip=('-y',))
    mb.face([F @ Vector((u - w / 2, 0.045, z - h / 2)), F @ Vector((u + w / 2, 0.045, z - h / 2)), F @ Vector((u + w / 2, 0.045, z + h / 2)), F @ Vector((u - w / 2, 0.045, z + h / 2))], spec.get('glass_mat', 'glass'), glass, 0)
    kind = spec['type']
    if kind == 'louvre' and detail.web():
        kind = 'sliding'
    if kind == 'louvre':  # naco: glass blades in an aluminium frame, tilted open
        n = max(5, round(h / 0.11))
        for i in range(n):
            zz = z - h / 2 + (i + 0.5) * h / n
            for cx in (-w / 4, w / 4):  # two columns of blades either side of the mullion
                mb.box('glass', at(F, u + cx, 0.07, zz, rx=-0.55), glass, 0, size=(w * 0.47, 0.004, h / n * 1.05))
        mb.box('steel', at(F, u, 0.07, z), spec['mullion'], wear, size=(0.04, 0.05, h))  # the centre mullion
    elif kind == 'casement':
        mb.box('paint', at(F, u, 0.06, z), trim, wear, size=(0.05, 0.05, h))
        mb.box('paint', at(F, u, 0.06, z + h * 0.22), trim, wear, size=(w, 0.05, 0.05))
    elif kind == 'sliding':
        mb.box('steel', at(F, u, 0.065, z), spec['mullion'], wear, size=(0.05, 0.03, h))
    # sill and hood
    mb.box('paint', at(F, u, 0.12, z - h / 2 - 0.12), trim, wear, size=(w + 0.36, 0.24, 0.07))
    if spec.get('hood'):
        mb.box('paint', at(F, u, 0.2, z + h / 2 + 0.16, rx=0.18), trim, wear, size=(w + 0.4, 0.4, 0.06))
    if spec['bars'] != 'none':
        burglar_bars(mb, F, u, z, w, h, spec['bars'], spec['bar_col'], wear)


def door(mb, F, u, spec):
    w, wear = 1.0, spec['wear']
    mb.box('paint', at(F, u, 0.01, 1.12), spec['frame'], wear, size=(w + 0.16, 0.06, 2.3), skip=('-y',))
    mb.box('steel', at(F, u, 0.04, 1.06), spec['door'], wear, size=(w - 0.04, 0.05, 2.1))
    for zz in (0.55, 1.15, 1.75):  # pressed panels
        mb.box('steel', at(F, u, 0.07, zz), shade(spec['door'], 0.85), wear, size=(w * 0.7, 0.02, 0.42))
    mb.box('steel', at(F, u + 0.38, 0.09, 1.05), (0.7, 0.6, 0.3), 0, size=(0.04, 0.06, 0.14))
    if spec.get('step', True):
        mb.box('concrete', at(F, u, 0.35, 0.08), (0.55, 0.55, 0.53), wear + 0.2, size=(w + 0.6, 0.7, 0.16))


def roller_shutter(mb, F, u, w, spec):
    """A shop opening with a roller shutter part-raised; the shutter has real horizontal ribs."""
    wear, open_ = spec['wear'], spec['open']
    h = 2.5
    # the opening: a dark back face set in from a reveal (so it never fights the wall)
    dark = (0.03, 0.025, 0.02)
    mb.face([F @ Vector((u - w / 2, 0.02, 0.05)), F @ Vector((u + w / 2, 0.02, 0.05)), F @ Vector((u + w / 2, 0.02, h)), F @ Vector((u - w / 2, 0.02, h))], 'paint', dark, 0)
    for s_ in (-1, 1):
        mb.box('concrete', at(F, u + s_ * (w / 2 + 0.01), 0.04, h / 2), (0.5, 0.5, 0.48), wear, size=(0.04, 0.06, h))
    mb.box('concrete', at(F, u, 0.04, h + 0.02), (0.5, 0.5, 0.48), wear, size=(w + 0.06, 0.06, 0.06))
    mb.box('concrete', at(F, u, 0.3, 0.06), (0.55, 0.55, 0.53), wear + 0.2, size=(w + 0.3, 0.6, 0.12))  # the step people sit on
    for s in (-1, 1):
        mb.box('steel', at(F, u + s * (w / 2 + 0.04), 0.06, h / 2), spec['col'], wear, size=(0.08, 0.1, h))
    sh = h * (1 - open_)
    n = max(1, int(sh / 0.075))
    for i in range(n):  # ribs
        z = h - (i + 0.5) * sh / n
        mb.box('zinc', at(F, u, 0.07 + (i % 2) * 0.01, z), spec['col'], wear, size=(w, 0.02, sh / n * 1.02))
    mb.box('steel', at(F, u, 0.12, h + 0.15), shade(spec['col'], 0.85), wear, size=(w + 0.2, 0.28, 0.3))  # the drum box


# ---------------------------------------------------------------- balconies
def balcony(mb, F, u, z, w, spec):
    """A slab on the wall with a balustrade: precast balusters or a steel rail."""
    wear, d = spec['wear'], 1.1
    mb.box('concrete', at(F, u, d / 2, z), spec['slab'], wear, size=(w, d, 0.15))
    rail_h = 1.0
    if spec['rail'] == 'balusters' and detail.web():
        mb.box('paint', at(F, u, d - 0.06, z + rail_h / 2), spec['rail_col'], wear, size=(w, 0.14, rail_h))
        for x in (-w / 2, w / 2):
            mb.box('paint', at(F, u + x, d / 2, z + rail_h / 2), spec['rail_col'], wear, size=(0.14, d, rail_h))
    elif spec['rail'] == 'balusters':
        n = int(w / 0.22)
        for side, (x0, y0, x1, y1) in enumerate(((-w / 2, d, w / 2, d), (-w / 2, 0.05, -w / 2, d), (w / 2, 0.05, w / 2, d))):
            L = math.hypot(x1 - x0, y1 - y0)
            k = max(1, int(L / 0.22))
            for i in range(k + 1):
                t = i / k
                x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
                # a turned baluster: wide-narrow-wide
                cyl(mb, 'paint', at(F, u + x - 0.0, y - 0.06, z + 0.08), 0.06, 0.18, spec['rail_col'], wear, seg=8, caps=(False, False), r2=0.035)
                cyl(mb, 'paint', at(F, u + x, y - 0.06, z + 0.26), 0.035, 0.45, spec['rail_col'], wear, seg=8, caps=(False, False), r2=0.065)
                cyl(mb, 'paint', at(F, u + x, y - 0.06, z + 0.71), 0.065, 0.14, spec['rail_col'], wear, seg=8, caps=(False, True), r2=0.04)
            mid = ((x0 + x1) / 2, (y0 + y1) / 2 - 0.06)
            ang = math.atan2(y1 - y0, x1 - x0)
            mb.box('paint', at(F, u + mid[0], mid[1], z + rail_h - 0.1, rz=ang), spec['rail_col'], wear, size=(L + 0.12, 0.16, 0.12))
    else:  # steel rail with vertical pickets
        for (x0, y0, x1, y1) in ((-w / 2, d - 0.05, w / 2, d - 0.05), (-w / 2, 0.05, -w / 2, d - 0.05), (w / 2, 0.05, w / 2, d - 0.05)):
            a, b = F @ Vector((u + x0, y0, z + rail_h - 0.05)), F @ Vector((u + x1, y1, z + rail_h - 0.05))
            bar(mb, 'steel', a, b, 0.045, spec['rail_col'], wear)
            L = math.hypot(x1 - x0, y1 - y0)
            for i in range(int(L / 0.12) + 1):
                t = i / max(1, int(L / 0.12))
                x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
                bar(mb, 'steel', F @ Vector((u + x, y, z + 0.08)), F @ Vector((u + x, y, z + rail_h - 0.05)), 0.022, spec['rail_col'], wear)


# ---------------------------------------------------------------- roofs
def corrugated(mb, A, B, C, D, spec, wear_of=None):
    """A corrugated sheet surface: eave edge A->B, top edge D->C (C == D for a hip end).
    Ribs run up the slope; the profile varies along A->B. Sheets are ~0.9 m wide and each
    gets its own wear, so old roofs read as a patchwork of replaced sheets."""
    if spec['pitch'] < 0.3:   # zinc: sheet by sheet, rusted, lapped, sagging (gidi_kit/zinc.py)
        return zinc.sheets(mb, A, B, C, D, spec, wear_of)
    A, B, C, D = (Vector(p) for p in (A, B, C, D))
    L = (B - A).length
    if detail.web():  # tarpaulin: one face (and its underside)
        w = spec['wear']
        mb.face([A, B, C, D] if C != D else [A, B, C], 'zinc', spec['col'], w)
        mb.face([D, C, B, A] if C != D else [C, B, A], 'zinc', shade(spec['col'], 0.6), w)
        return
    pitch, depth, prof = spec['pitch'], spec['depth'], spec['profile']
    n = max(2, int(L / pitch * (4 if prof == 'sine' else 5)))
    nrm = (B - A).cross(D - A).normalized()
    if nrm.z < 0:
        nrm = -nrm

    def h(s):  # profile height at distance s along the eave
        t = (s / pitch) % 1.0
        if prof == 'sine':
            return depth * 0.5 * (1 - math.cos(t * math.tau))
        # trapezoidal long-span: narrow raised rib, wide pan
        return depth if 0.08 < t < 0.24 else (depth * (t / 0.08) if t <= 0.08 else (depth * (1 - (t - 0.24) / 0.08) if t < 0.32 else 0.0))

    # ribs run straight up the slope, square to the eave, and stop at the ridge or at a hip line
    ab = (B - A) / L
    up = (D - A) - ab * (D - A).dot(ab)
    hgt = up.length
    up = up / hgt
    sD, sC = (D - A).dot(ab), (C - A).dot(ab)

    def top(s):
        k = 1.0
        if sD > 1e-3 and s < sD:
            k = s / sD
        elif sC < L - 1e-3 and s > sC:
            k = (L - s) / (L - sC)
        return A + ab * s + up * hgt * max(0.0, min(1.0, k))

    sheet_w = spec.get('sheet_w', 0.9)
    for i in range(n):
        s0, s1 = L * i / n, L * (i + 1) / n
        t0, t1 = s0 / L, s1 / L
        sheet = int(s0 / sheet_w)
        wear = wear_of(sheet) if wear_of else spec['wear']
        col = spec['col'] if not spec.get('mixed') or sheet % 3 else spec['col2']
        p0 = A.lerp(B, t0) + nrm * h(s0)
        p1 = A.lerp(B, t1) + nrm * h(s1)
        q1 = top(s1) + nrm * h(s1)
        q0 = top(s0) + nrm * h(s0)
        mb.face([p0, p1, q1, q0], 'zinc', col, wear)
        mb.face([q0, q1, p1, p0], 'zinc', shade(col, 0.6), wear)  # underside


def roof_pitched(mb, poly, H, spec, rng):
    """Gable or hip roof over a quad footprint with an overhang, fascia and ridge cap."""
    e0, e1 = math.dist(poly[0], poly[1]), math.dist(poly[1], poly[2])
    gp = offset(poly, spec['overhang'])
    A, B, C, D = gp if e0 >= e1 else [gp[1], gp[2], gp[3], gp[0]]
    o = poly if e0 >= e1 else [poly[1], poly[2], poly[3], poly[0]]
    short = min(e0, e1)
    rise = min(2.4, short * 0.5 * math.tan(math.radians(spec['pitch_deg'])))
    y0 = H - 0.1
    m1 = ((A[0] + D[0]) / 2, (A[1] + D[1]) / 2)
    m2 = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
    if spec['form'] == 'hip':
        dx, dy = m2[0] - m1[0], m2[1] - m1[1]
        l = math.hypot(dx, dy) or 1
        k = min(0.45, (short / 2 + spec['overhang']) / l)
        m1, m2 = (m1[0] + dx * k, m1[1] + dy * k), (m2[0] - dx * k, m2[1] - dy * k)
    P = lambda p, z: (p[0], p[1], z)
    zr = H + rise
    if 'sag' not in spec:   # old roofs sink between the eave and the ridge
        spec['sag'] = max(0.0, spec['wear'] - 0.45) * rng.child('sag').between(0.05, 0.3) * min(1.0, short / 5)
    sheet_wear = lambda i: max(0.0, min(1.0, spec['wear'] + rng.child('sheet', i).between(-0.35, 0.35)))
    corrugated(mb, P(A, y0), P(B, y0), P(m2, zr), P(m1, zr), spec, sheet_wear)
    corrugated(mb, P(C, y0), P(D, y0), P(m1, zr), P(m2, zr), spec, sheet_wear)
    if spec['form'] == 'hip':
        corrugated(mb, P(D, y0), P(A, y0), P(m1, zr), P(m1, zr), spec, sheet_wear)
        corrugated(mb, P(B, y0), P(C, y0), P(m2, zr), P(m2, zr), spec, sheet_wear)
    else:  # gable walls in the wall paint, on the wall line
        for a, b in ((o[1], o[2]), (o[3], o[0])):
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            tri = [(a[0], a[1], H), (b[0], b[1], H), (mid[0], mid[1], zr - 0.15)]
            mb.face(tri, 'paint', spec['gable_col'], spec['wall_wear'])
            mb.face(list(reversed(tri)), 'paint', spec['gable_col'], spec['wall_wear'])
    # ridge cap and fascia boards
    rc = zinc._mix(shade(spec['col'], 0.8), zinc.RUST, spec['wear'] * 0.8)   # the ridge cap rusts first: water and nails
    bar(mb, 'zinc', (m1[0], m1[1], zr + 0.05), (m2[0], m2[1], zr + 0.05), 0.16, rc, spec['wear'])
    for a, b in ((A, B), (C, D)) + (((B, C), (D, A)) if spec['form'] == 'hip' else ()):
        bar(mb, 'wood' if spec['fascia_wood'] else 'paint', (a[0], a[1], y0 - 0.08), (b[0], b[1], y0 - 0.08), 0.16, spec['fascia'], spec['wall_wear'])
    return dict(A=A, B=B, C=C, D=D, m1=m1, m2=m2, y0=y0, zr=zr)


def roof_flat(mb, poly, H, spec):
    """Flat slab, parapet with coping, and the slab's spout."""
    oct_ = chamfer(poly, spec.get('chamfer', 0.18))
    ph = spec['parapet_h']
    inner = offset(oct_, -0.18)
    if spec.get('_wx'):   # the house's weathering runs on up the parapet
        spec['_wx'].prism(mb, 'paint', oct_, H, H + ph)
    else:
        prism(mb, 'paint', oct_, H, H + ph, spec['paint'], spec['paint'], spec['wear'])
    prism(mb, 'concrete', inner, H, H + ph, spec['slab'], spec['slab'], spec['wear'], inward=True)
    outer = offset(oct_, 0.06)
    prism(mb, 'paint', outer, H + ph, H + ph + 0.12, spec['trim'], spec['trim'], spec['wear'])
    z = H + ph + 0.12
    for i in range(len(outer)):  # the coping's top: a ring from the outer edge to the inner face only
        j = (i + 1) % len(outer)
        mb.face([(outer[i][0], outer[i][1], z), (outer[j][0], outer[j][1], z), (inner[j][0], inner[j][1], z), (inner[i][0], inner[i][1], z)], 'paint', spec['trim'], spec['wear'])
    zinc.slab(mb, inner, H + 0.02, spec['slab'], spec['wear'])
    return inner


# ---------------------------------------------------------------- roof and yard furniture
def water_tank(mb, x, y, z, spec):
    """A ribbed plastic tank on a steel stand."""
    r, h = spec['r'], spec['h']
    stand = spec['stand']
    for sx in (-1, 1):
        for sy in (-1, 1):
            bar(mb, 'steel', (x + sx * r * 0.85, y + sy * r * 0.85, z), (x + sx * r * 0.85, y + sy * r * 0.85, z + stand), 0.06, (0.18, 0.18, 0.18), spec['wear'])
    for k in range(2):
        zz = z + stand * (0.4 + 0.6 * k)
        for (ax, ay), (bx, by) in ((((-1, -1), (1, -1))), (((1, -1), (1, 1))), (((1, 1), (-1, 1))), (((-1, 1), (-1, -1)))):
            bar(mb, 'steel', (x + ax * r * 0.85, y + ay * r * 0.85, zz), (x + bx * r * 0.85, y + by * r * 0.85, zz), 0.05, (0.18, 0.18, 0.18), spec['wear'])
    m = Matrix.Translation((x, y, z + stand))
    ribs = 1 if detail.web() else 6
    for k in range(ribs):  # the tank's horizontal ribs
        cyl(mb, 'plastic', m @ Matrix.Translation((0, 0, h * k / ribs)), r * (1.0 if k % 2 else 0.97), h / ribs, spec['col'], 0, seg=20, caps=(k == 0, False), r2=r * (0.97 if k % 2 else 1.0))
    cyl(mb, 'plastic', m @ Matrix.Translation((0, 0, h)), r, 0.25, spec['col'], 0, seg=20, caps=(False, True), r2=r * 0.55)
    cyl(mb, 'plastic', m @ Matrix.Translation((0, 0, h + 0.25)), 0.22, 0.12, spec['col'], 0, seg=12)


def satellite_dish(mb, x, y, z, rz, col):
    m = Matrix.Translation((x, y, z)) @ Matrix.Rotation(rz, 4, 'Z')
    bar(mb, 'steel', m @ Vector((0, 0, 0)), m @ Vector((0, 0, 0.6)), 0.04, (0.6, 0.6, 0.6))
    dm = m @ Matrix.Translation((0, 0.05, 0.75)) @ Matrix.Rotation(1.2, 4, 'X')
    seg, rings, R = 16, 3, 0.4
    pts = [[dm @ Vector((math.cos(a) * R * k / rings, math.sin(a) * R * k / rings, 0.12 * (k / rings) ** 2)) for a in (i / seg * math.tau for i in range(seg))] for k in range(rings + 1)]
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg
            mb.face([pts[k][i], pts[k][j], pts[k + 1][j], pts[k + 1][i]], 'plastic', col)
            mb.face([pts[k + 1][i], pts[k + 1][j], pts[k][j], pts[k][i]], 'plastic', col)


def tyre(mb, x, y, z, r=0.32, w=0.2):
    seg, tube = 14, 6
    pts = []
    for i in range(seg):
        a = i / seg * math.tau
        ring = []
        for k in range(tube):
            b = k / tube * math.tau
            rr = r + math.cos(b) * w / 2
            ring.append(Vector((x + math.cos(a) * rr, y + math.sin(a) * rr, z + math.sin(b) * w / 2)))
        pts.append(ring)
    for i in range(seg):
        for k in range(tube):
            a, b = pts[i][k], pts[(i + 1) % seg][k]
            c, d = pts[(i + 1) % seg][(k + 1) % tube], pts[i][(k + 1) % tube]
            mb.face([a, b, c, d], 'rubber', (0.02, 0.02, 0.02))


def generator(mb, F, u, spec):
    """A petrol generator in a welded cage, beside the wall."""
    col, wear = spec['col'], spec['wear']
    mb.box('steel', at(F, u, 0.9, 0.35), col, wear, size=(0.75, 0.55, 0.5))
    mb.box('steel', at(F, u + 0.2, 0.9, 0.68), shade(col, 0.8), wear, size=(0.3, 0.4, 0.16))
    cyl(mb, 'steel', at(F, u - 0.3, 0.9, 0.55, rx=math.pi / 2), 0.05, 0.25, (0.25, 0.25, 0.25), wear + 0.3, seg=8)
    cage = (0.2, 0.2, 0.2)
    for k in range(9):
        x = -0.55 + k * 1.1 / 8
        for yy in (0.5, 1.3):
            bar(mb, 'steel', F @ Vector((u + x, yy, 0)), F @ Vector((u + x, yy, 1.05)), 0.025, cage, wear)
    for zz in (0.02, 1.05):
        for (a, b) in (((-0.55, 0.5), (0.55, 0.5)), ((0.55, 0.5), (0.55, 1.3)), ((0.55, 1.3), (-0.55, 1.3)), ((-0.55, 1.3), (-0.55, 0.5))):
            bar(mb, 'steel', F @ Vector((u + a[0], a[1], zz)), F @ Vector((u + b[0], b[1], zz)), 0.035, cage, wear)


# ---------------------------------------------------------------- unfinished work and walls
def unfinished_storey(mb, poly, z, spec, rng):
    """Columns, a ring beam on some sides, part-built block walls and rods waiting for the next floor."""
    oct_ = poly
    for i, p in enumerate(oct_):
        c = (sum(q[0] for q in oct_) / len(oct_), sum(q[1] for q in oct_) / len(oct_))
        px, py = p[0] * 0.95 + c[0] * 0.05, p[1] * 0.95 + c[1] * 0.05
        mb.box('concrete', Matrix.Translation((px, py, z + STOREY / 2)), (0.55, 0.54, 0.51), 0.6, size=(0.3, 0.3, STOREY))
        for r in range(4):
            dx, dy = (0.08 if r % 2 else -0.08), (0.08 if r > 1 else -0.08)
            top = z + STOREY + rng.between(0.6, 1.4)
            bar(mb, 'steel', (px + dx, py + dy, z + STOREY), (px + dx + rng.between(-0.08, 0.08), py + dy + rng.between(-0.08, 0.08), top), 0.02, (0.33, 0.14, 0.06), 0.9)
    for i in range(len(oct_)):
        a, b = oct_[i], oct_[(i + 1) % len(oct_)]
        L = math.dist(a, b)
        n = max(1, int(L / 0.45))
        if rng.chance(0.3):
            continue
        for k in range(n):  # block courses stepped where the money ran out
            t = (k + 0.5) / n
            hgt = round(rng.between(0.2, 2.4) / 0.225) * 0.225 if rng.chance(0.75) else 0.225
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            mb.box('block', Matrix.Translation((x, y, z + hgt / 2)) @ Matrix.Rotation(math.atan2(b[1] - a[1], b[0] - a[0]), 4, 'Z'), (1, 1, 1), 0.5, size=(L / n - 0.01, 0.2, hgt))


def compound_wall(mb, poly, spec, rng, skip_seg=None, closed=True, gates=None):
    """A block wall round a compound: pillars, coping, broken bottles or razor wire, a steel gate."""
    h, col, wear = spec['h'], spec['paint'], spec['wear']
    gate_i = spec.get('gate_edge', 0) if gates is None else -1   # gates=[points]: a gate wherever one stands on the line
    for i in range(len(poly) if closed else len(poly) - 1):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        L = math.dist(a, b)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        n = max(1, int(L / 3.0))
        for k in range(n):
            t0, t1 = k / n, (k + 1) / n
            mid = (a[0] + (b[0] - a[0]) * (t0 + t1) / 2, a[1] + (b[1] - a[1]) * (t0 + t1) / 2)
            seg_len = L / n
            if skip_seg and skip_seg(mid):
                continue
            if (i == gate_i and k == n // 2) or (gates and any(math.dist(mid, g) < seg_len / 2 + 0.3 for g in gates)):  # the gate
                m = Matrix.Translation((mid[0], mid[1], 0)) @ Matrix.Rotation(ang, 4, 'Z')
                for s in (-0.5, 0.5):
                    mb.box('steel', m @ Matrix.Translation((s * seg_len / 2, 0, h * 0.95 / 2)), spec['gate'], wear, size=(seg_len / 2 - 0.04, 0.06, h * 0.95))
                    for z in (0.5, 1.2):
                        mb.box('steel', m @ Matrix.Translation((s * seg_len / 2, 0.04, z)), shade(spec['gate'], 0.8), wear, size=(seg_len / 2 - 0.3, 0.02, 0.5))
                continue
            m = Matrix.Translation((mid[0], mid[1], 0)) @ Matrix.Rotation(ang, 4, 'Z')
            mb.box('paint', m @ Matrix.Translation((0, 0, h / 2)), col, wear, size=(seg_len, 0.2, h))
            mb.box('paint', m @ Matrix.Translation((0, 0, h + 0.05)), spec['coping'], wear, size=(seg_len + 0.02, 0.28, 0.1))
            mb.box('paint', m @ Matrix.Translation((seg_len / 2, 0, (h + 0.25) / 2)), spec['coping'], wear, size=(0.3, 0.3, h + 0.25))
            if detail.web() and spec['top'] in ('bottles', 'razor'):  # one strip stands for shards or wire
                mb.box('glass' if spec['top'] == 'bottles' else 'steel', m @ Matrix.Translation((0, 0, h + 0.15)), (0.15, 0.28, 0.12) if spec['top'] == 'bottles' else (0.6, 0.6, 0.6), 0.2, size=(seg_len, 0.06, 0.12))
            elif spec['top'] == 'bottles':
                for j in range(int(seg_len / 0.12)):
                    x = -seg_len / 2 + (j + 0.5) * 0.12
                    mb.box('glass', m @ Matrix.Translation((x, rng.between(-0.06, 0.06), h + 0.14)) @ Matrix.Rotation(rng.between(-0.6, 0.6), 4, 'Y'), rng.pick([(0.1, 0.25, 0.08), (0.3, 0.2, 0.05), (0.4, 0.5, 0.45)]), 0, size=(0.03, 0.02, 0.12))
            elif spec['top'] == 'razor':
                for j in range(int(seg_len / 0.1)):
                    a0 = j * 1.3
                    x0 = -seg_len / 2 + j * 0.1
                    bar(mb, 'steel', m @ Vector((x0, math.cos(a0) * 0.15, h + 0.3 + math.sin(a0) * 0.15)), m @ Vector((x0 + 0.1, math.cos(a0 + 1.3) * 0.15, h + 0.3 + math.sin(a0 + 1.3) * 0.15)), 0.012, (0.65, 0.65, 0.65), 0.2)


# ---------------------------------------------------------------- signs and awnings
def signboard(mb, F, u, z, w, h, spec):
    """A shop sign: a painted board on the wall with 3D lettering (and a phone number)."""
    mb.box('wood' if spec['hand'] else 'steel', at(F, u, 0.08, z), spec['bg'], spec['wear'], size=(w, 0.06, h))
    mb.box('steel', at(F, u, 0.08, z), (0.08, 0.08, 0.08), spec['wear'], size=(w + 0.08, 0.05, h + 0.08))
    if detail.web():  # the browser paints the whole board: text, phone, colours
        detail.record_text(at(F, u, 0.115, z), spec['text'] + ('\n' + spec['phone'] if spec.get('phone') else ''), h, spec['fg'], bg=spec['bg'], w=w, h=h, hand=spec.get('hand', False))
        return
    lines = spec['text'].split('\n')
    fs = h * (0.38 if len(lines) > 1 else 0.55)
    text(mb, 'paint', at(F, u, 0.115, z + (0.06 if spec.get('phone') else 0)), spec['text'], fs, spec['fg'], max_w=w * 0.92, wobble=spec.get('wobble'))
    if spec.get('phone'):
        text(mb, 'paint', at(F, u, 0.115, z - h * 0.38), spec['phone'], h * 0.13, spec['fg'], max_w=w * 0.6)


def awning(mb, F, u, w, spec):
    """A sloping zinc awning on two posts in front of a shop."""
    d, z = spec['depth'], 2.75
    A, B = F @ Vector((u - w / 2, 0.05, z)), F @ Vector((u + w / 2, 0.05, z))
    C, D = F @ Vector((u + w / 2, d, z - 0.45)), F @ Vector((u - w / 2, d, z - 0.45))
    corrugated(mb, D, C, B, A, dict(spec, profile='sine', pitch=0.076, depth=0.018))
    for s in (-1, 1):
        bar(mb, 'wood', F @ Vector((u + s * (w / 2 - 0.1), d - 0.1, 0)), F @ Vector((u + s * (w / 2 - 0.1), d - 0.1, z - 0.45)), 0.08, (0.35, 0.25, 0.16), spec['wear'])
