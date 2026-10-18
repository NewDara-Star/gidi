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
    mb.box(mat, m, col, wear, size=(t, t, l), skip=('-z', '+z') if detail.web() else ())   # the web tiles: no end caps on a thin bar


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
    wx.prism(mb, 'block' if spec.get('bare') else 'paint', oct_, 0, H, rows=[0.45, 1.15, wx.top - 1.8] + ([] if detail.web() else [0.8, wx.top - 0.9] + [z + d for z in bands for d in (-0.6, 0.6)]))
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


def generator(mb, F, u, spec, rng=None):
    """A generator beside the wall (F: x along the wall, y out, z up; it stands 0.9 m out at u). Most are the small petrol
    sets every house runs: a tubular frame, the tank on top in its maker's colour, the engine and alternator, a rusty
    muffler and exhaust, all in a welded rebar cage with a padlocked door, an oil stain under it, often a jerrycan by it.
    Now and then a bigger soundproof diesel box instead."""
    from .core import Rng, hex_rgb
    col, wear = spec['col'], spec['wear']
    rng = rng or Rng('generator', round(F[0][3], 1), round(F[1][3], 1), u)
    P = lambda x, y, z: F @ Vector((u + x, 0.9 + y, z))
    dark, steel, rust = (0.06, 0.06, 0.06), (0.32, 0.33, 0.34), hex_rgb('#5a3a26')
    stain = [P(-0.7, -0.45, 0.012), P(0.75, -0.5, 0.012), P(0.8, 0.5, 0.012), P(-0.65, 0.55, 0.012)]   # oil and soot on the ground
    mb.face(stain, 'ground', (0.08, 0.07, 0.06), 0.8)
    if rng.chance(0.12):   # the soundproof box: louvres along the side, a door, the exhaust up the back
        body = hex_rgb(rng.pick(['#3f6b8a', '#2e7d32', '#c9c3b6', '#8a8d8c']))
        mb.box('steel', at(F, u, 0.9, 0.62), body, wear, size=(1.6, 0.8, 1.05))
        mb.box('steel', at(F, u, 0.9, 0.08), dark, wear, size=(1.65, 0.85, 0.16))
        for k in range(6):
            mb.box('steel', at(F, u - 0.4 + k * 0.16, 1.305, 0.75), shade(body, 0.6), wear, size=(0.1, 0.012, 0.45))
        cyl(mb, 'steel', at(F, u + 0.6, 0.65, 1.15), 0.05, 0.6, rust, min(1, wear + 0.3), seg=8)
        return
    # the cage: rebar welded in a box round it, rusty, a door on the front with its padlock
    cw, cd, ch = 1.1, 0.8, 1.05
    cage = shade(rust, rng.between(0.7, 1.1)) if rng.chance(0.6) else (0.16, 0.17, 0.16)
    for zz in (0.03, ch):
        for a, b in (((-cw / 2, -cd / 2), (cw / 2, -cd / 2)), ((cw / 2, -cd / 2), (cw / 2, cd / 2)), ((cw / 2, cd / 2), (-cw / 2, cd / 2)), ((-cw / 2, cd / 2), (-cw / 2, -cd / 2))):
            bar(mb, 'steel', P(a[0], a[1], zz), P(b[0], b[1], zz), 0.035, cage, wear)
    n = 8 if not detail.web() else 3
    for k in range(n + 1):
        x = -cw / 2 + k * cw / n
        for yy in (-cd / 2, cd / 2):
            bar(mb, 'steel', P(x, yy, 0.03), P(x, yy, ch), 0.022, cage, wear)
    for k in range(1, (5 if not detail.web() else 2)):
        y = -cd / 2 + k * cd / (5 if not detail.web() else 2)
        for xx in (-cw / 2, cw / 2):
            bar(mb, 'steel', P(xx, y, 0.03), P(xx, y, ch), 0.022, cage, wear)
        bar(mb, 'steel', P(-cw / 2, y, ch), P(cw / 2, y, ch), 0.022, cage, wear)   # the top
    mb.box('steel', at(F, u + 0.05, 0.9 + cd / 2 + 0.03, 0.55), (0.55, 0.5, 0.2), 0.3, size=(0.07, 0.04, 0.09))   # the padlock
    # the set: a tubular frame on the ground, the engine at one end, the alternator at the other, the tank over both
    fw, fd, fh = 0.62, 0.46, 0.5
    for sx in (-1, 1):
        for sy in (-1, 1):
            bar(mb, 'steel', P(sx * fw / 2, sy * fd / 2, 0.02), P(sx * fw / 2, sy * fd / 2, fh), 0.03, dark, wear)
        bar(mb, 'steel', P(sx * fw / 2, -fd / 2, 0.03), P(sx * fw / 2, fd / 2, 0.03), 0.03, dark, wear)
        bar(mb, 'steel', P(sx * fw / 2, -fd / 2, fh), P(sx * fw / 2, fd / 2, fh), 0.03, dark, wear)
    mb.box('steel', at(F, u - 0.12, 0.9, 0.24), steel, wear, size=(0.3, 0.3, 0.32))                       # the engine
    mb.box('steel', at(F, u - 0.12, 0.9 - 0.17, 0.3), shade(steel, 0.6), wear, size=(0.22, 0.04, 0.18))   # its recoil start
    cyl(mb, 'steel', at(F, u + 0.08, 0.9, 0.24, ry=math.pi / 2), 0.12, 0.2, col, wear, seg=12)            # the alternator
    mb.box('steel', at(F, u + 0.22, 0.9, 0.24), shade(col, 0.8), wear, size=(0.08, 0.24, 0.24))           # its panel: sockets, switch
    mb.face([P(0.265, -0.08, 0.16), P(0.265, 0.08, 0.16), P(0.265, 0.08, 0.32), P(0.265, -0.08, 0.32)], 'plastic', dark, 0)
    mb.box('plastic', at(F, u, 0.9, fh + 0.09), col, wear, size=(0.5, 0.36, 0.17))                       # the tank
    mb.box('plastic', at(F, u, 0.9, fh + 0.19), shade(col, 1.08), wear, size=(0.4, 0.28, 0.04))
    cyl(mb, 'plastic', at(F, u - 0.1, 0.9, fh + 0.21), 0.04, 0.04, dark, 0, seg=8)                         # the cap
    mb.box('steel', at(F, u - 0.12, 0.9 + 0.2, 0.42), rust, min(1, wear + 0.3), size=(0.24, 0.1, 0.14))   # the muffler
    cyl(mb, 'steel', at(F, u - 0.2, 0.9 + 0.25, 0.42, rx=-math.pi / 2), 0.025, 0.55, (0.05, 0.04, 0.035), 0.9, seg=6)   # the exhaust out through the cage
    if rng.chance(0.55):   # the fuel, in a jerrycan by the cage
        jc = hex_rgb(rng.pick(['#e8b923', '#2e7d32', '#c62828', '#d9d4c8']))
        mb.box('plastic', at(F, u + cw / 2 + 0.22, 0.75 + rng.between(-0.1, 0.2), 0.19, rz=rng.between(-0.4, 0.4)), jc, 0.6, size=(0.18, 0.3, 0.38))
        cyl(mb, 'plastic', at(F, u + cw / 2 + 0.22, 0.68, 0.38), 0.025, 0.05, shade(jc, 0.7), 0.6, seg=6)


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


def _band_face(mb, m, side, x0, x1, zs, cols, mat='paint', wear=0.0, y=0.1, cols_r=None):
    """One side of a thin wall in its frame m (x along, y across, z up): quads up the bands zs, coloured cols[k] at zs[k]
    (cols_r: the right-hand end's, if it differs). side +1 faces +y, -1 faces -y."""
    cr = cols_r or cols
    for k in range(len(zs) - 1):
        q = [m @ Vector((x0, side * y, zs[k])), m @ Vector((x1, side * y, zs[k])), m @ Vector((x1, side * y, zs[k + 1])), m @ Vector((x0, side * y, zs[k + 1]))]
        c = [cols[k], cr[k], cr[k + 1], cols[k + 1]]
        mb.face(q[::-1] if side > 0 else q, mat, c[::-1] if side > 0 else c, wear)


def compound_wall(mb, poly, spec, rng, skip_seg=None, closed=True, gates=None):
    """A block wall round a compound, weathered: red earth up its foot and grime run down from the coping, painted in
    3 m panels between pillars; on the dense and sprawl districts' walls (spec['rough']) a stretch now and then where the
    top has broken off down to the block, and broken bottles set in the coping; razor wire on the better-off ones. Gates:
    two painted steel leaves, rust rising from their foot. All colour and geometry, so Unreal sees it too."""
    from . import wear as W
    h, col, wear = spec['h'], spec['paint'], spec['wear']
    gate_i = spec.get('gate_edge', 0) if gates is None else -1   # gates=[points]: a gate wherever one stands on the line
    wr = rng.child('weather')
    mix = W.mix

    def tone(c, z, top, k=1.0):   # the wall's colour at z: splash at the foot, grime under the top
        c = mix(c, W.DIRT, min(1.0, wear * 1.15 * k) * (1 - W.smooth(0.0, 0.95, z)))
        return mix(c, W.GRIME, wear * 0.7 * k * W.smooth(top - 0.8, top, z))

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
            m = Matrix.Translation((mid[0], mid[1], 0)) @ Matrix.Rotation(ang, 4, 'Z')
            pillar = lambda x: mb.box('paint', m @ Matrix.Translation((x, 0, (h + 0.25) / 2)), tone(spec['coping'], 0.3, h, 0.8), wear, size=(0.3, 0.3, h + 0.25), skip=('-z',))
            if i == 0 and k == 0 and not closed:   # the line's own end
                pillar(-seg_len / 2)
            if (i == gate_i and k == n // 2) or (gates and any(math.dist(mid, g) < seg_len / 2 + 0.3 for g in gates)):  # the gate
                pillar(-seg_len / 2)   # the gate posts
                pillar(seg_len / 2)
                gc = spec['gate']
                rust = W.RUST
                lh = h * 0.95
                for s_ in (-0.5, 0.5):
                    lm = m @ Matrix.Translation((s_ * seg_len / 2, 0, 0))
                    lw = seg_len / 2 - 0.04
                    zs = [0.0, 0.3, 0.8, lh]
                    cs = [mix(gc, rust, wear * 1.1), mix(gc, rust, wear * 0.55), mix(gc, rust, wear * 0.15), shade(gc, 1.05)]
                    for side in (-1, 1):
                        _band_face(mb, lm, side, -lw / 2, lw / 2, zs, cs, 'steel', wear, y=0.03)
                    mb.box('steel', lm @ Matrix.Translation((0, 0, lh)), shade(gc, 0.8), wear, size=(lw, 0.08, 0.06))   # the top rail
                    for z in (0.5, 1.2):   # pressed panels
                        mb.box('steel', lm @ Matrix.Translation((0, 0.04, z)), mix(shade(gc, 0.8), rust, wear * (0.6 if z < 1 else 0.2)), wear, size=(lw - 0.3, 0.02, 0.5))
                    if wr.chance(0.3 + 0.6 * wear):   # rust run down from a hinge or a bolt
                        x = wr.between(-lw / 2 + 0.1, lw / 2 - 0.1)
                        z0 = wr.between(0.9, lh - 0.2)
                        q = [lm @ Vector((x - 0.03, 0.035, z0 - 0.7)), lm @ Vector((x + 0.03, 0.035, z0 - 0.7)), lm @ Vector((x + 0.04, 0.035, z0)), lm @ Vector((x - 0.04, 0.035, z0))]
                        mb.face(q[::-1], 'steel', [mix(gc, rust, 0.3)] * 2 + [rust] * 2, wear)
                continue
            # a broken stretch: the top gone down to the block over part of the panel
            broken = spec.get('rough') and wr.chance(0.12 * wear)
            bx0 = wr.between(-seg_len / 2, 0) if broken else 0.0
            bx1 = min(seg_len / 2, bx0 + wr.between(0.6, 1.6)) if broken else 0.0
            drop = wr.between(0.25, 0.7) if broken else 0.0
            pc = shade(col, wr.between(0.9, 1.06))   # each panel painted its own time
            dirty_r = wr.chance(0.5)
            parts_x = [(-seg_len / 2, bx0, h), (bx0, bx1, h - drop), (bx1, seg_len / 2, h)] if broken else [(-seg_len / 2, seg_len / 2, h)]
            if broken:   # the broken edges: block showing where the wall steps down
                for x, sgn in ((bx0, 1), (bx1, -1)):
                    q = [m @ Vector((x, -0.1, h - drop)), m @ Vector((x, 0.1, h - drop)), m @ Vector((x, 0.1, h)), m @ Vector((x, -0.1, h))]
                    mb.face(q if sgn > 0 else q[::-1], 'block', W.BLOCK, wear)
            for x0, x1, top in parts_x:
                if x1 - x0 < 0.02:
                    continue
                zs = sorted({0.0, 0.45, 0.95, max(1.0, top - 0.8), top})
                cs = [tone(pc, z, h) for z in zs]
                if top < h:   # the broken top shows the block for a course or two
                    zs = sorted({0.0, 0.45, 0.95, max(1.0, top - 0.25), top})
                    cs = [tone(pc, z, h) for z in zs[:-2]] + [W.BLOCK, shade(W.BLOCK, 0.9)]
                fade = lambda x: 1.0 - 0.35 * wear * max(0.0, min(1.0, (x - (-seg_len / 2)) / seg_len if dirty_r else (seg_len / 2 - x) / seg_len))
                csl = [mix(c, W.GRIME, 1 - fade(x0)) for c in cs]   # dirtier toward one end of the panel
                csr = [mix(c, W.GRIME, 1 - fade(x1)) for c in cs]
                for side in (-1, 1):
                    _band_face(mb, m, side, x0, x1, zs, csl, 'paint', wear, cols_r=csr)
                cs = None
                if top >= h:
                    bands = (zs, csl, csr, x0, x1)   # what the wall shows, so a streak can fade into it exactly
                mb.face([m @ Vector((x0, -0.1, top)), m @ Vector((x1, -0.1, top)), m @ Vector((x1, 0.1, top)), m @ Vector((x0, 0.1, top))],
                        'block' if top < h else 'paint', shade(W.BLOCK, 0.85) if top < h else spec['coping'], wear)
                if top < h:
                    continue
                cop = mix(spec['coping'], W.GRIME, wear * 0.5)
                mb.box('paint', m @ Matrix.Translation(((x0 + x1) / 2, 0, h + 0.05)), cop, wear, size=(x1 - x0 + 0.02, 0.28, 0.1), skip=('-z',))
                if spec['top'] == 'bottles':   # shards set in the coping: green, brown and clear, jagged
                    cnt = max(1, int((x1 - x0) / 0.28))
                    for j in range(cnt):
                        xa, xb = x0 + (x1 - x0) * j / cnt, x0 + (x1 - x0) * (j + 1) / cnt
                        c = wr.pick([(0.1, 0.25, 0.08), (0.3, 0.17, 0.05), (0.45, 0.52, 0.48), (0.08, 0.2, 0.12)])
                        yy = wr.between(-0.06, 0.06)
                        tip = h + 0.1 + wr.between(0.06, 0.16)
                        for sgn in (1, -1):   # a thin blade, seen from both sides
                            tri = [m @ Vector((xa, yy, h + 0.1)), m @ Vector((xb, yy, h + 0.1)), m @ Vector(((xa + xb) / 2 + wr.between(-0.03, 0.03), yy, tip))]
                            mb.face(tri if sgn > 0 else tri[::-1], 'glass', c, 0)
                elif spec['top'] == 'razor':
                    if detail.web():
                        mb.box('steel', m @ Matrix.Translation(((x0 + x1) / 2, 0, h + 0.3)), (0.6, 0.6, 0.6), 0.2, size=(x1 - x0, 0.06, 0.12))
                    else:
                        for j in range(int((x1 - x0) / 0.1)):
                            a0 = j * 1.3
                            xx = x0 + j * 0.1
                            bar(mb, 'steel', m @ Vector((xx, math.cos(a0) * 0.15, h + 0.3 + math.sin(a0) * 0.15)), m @ Vector((xx + 0.1, math.cos(a0 + 1.3) * 0.15, h + 0.3 + math.sin(a0 + 1.3) * 0.15)), 0.012, (0.65, 0.65, 0.65), 0.2)
            # the pillar at the panel's end, and a run of grime down from the coping now and then
            pillar(seg_len / 2)
            for _ in range(2 if wr.chance(0.7 * wear) else (1 if wr.chance(0.5) else 0)):
                side = wr.pick([-1, 1])
                x = wr.between(-seg_len / 2 + 0.3, seg_len / 2 - 0.5)
                w_ = wr.between(0.2, 0.6)
                l_ = wr.between(0.6, h - 0.5)
                if broken and x + w_ / 2 > bx0 and x - w_ / 2 < bx1:   # no top to run from here
                    continue
                def seen(z, xx):
                    zs_, cl, cr, bx_0, bx_1 = bands
                    t = max(0.0, min(1.0, (xx - bx_0) / (bx_1 - bx_0)))
                    j = next(j for j in range(len(zs_) - 1) if zs_[j] <= z <= zs_[j + 1])
                    f = (z - zs_[j]) / (zs_[j + 1] - zs_[j])
                    return mix(mix(cl[j], cr[j], t), mix(cl[j + 1], cr[j + 1], t), f)
                zt, zb = h - 0.02, h - l_
                rows = [zb] + [z for z in bands[0] if zb < z < zt] + [zt]   # cut where the wall is cut, so the sides match it
                dark = lambda z: mix(seen(z, x), W.GRIME, (0.5 * wear + 0.2) * (z - zb) / (zt - zb))   # strongest at the top
                for za, zc in zip(rows, rows[1:]):
                    for xa, xb, ca, cb in ((x - w_ / 2, x, lambda z: seen(z, x - w_ / 2), dark), (x, x + w_ / 2, dark, lambda z: seen(z, x + w_ / 2))):
                        q = [m @ Vector((xa, side * 0.103, za)), m @ Vector((xb, side * 0.103, za)), m @ Vector((xb, side * 0.103, zc)), m @ Vector((xa, side * 0.103, zc))]
                        c = [ca(za), cb(za), cb(zc), ca(zc)]
                        mb.face(q[::-1] if side > 0 else q, 'paint', c[::-1] if side > 0 else c, wear)


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
