"""The dense old town kit, driven by the map (decisions: "The map tells the kit what goes where").

Everything here reads one spot's map record (the fields of the old town kit list, KIT.md section 12, plus the ones the
first eye test found missing, now in KIT.md section 12 too) and puts exactly that there: a building's footprint, storeys,
roof, wall, balcony and shop fronts; each frontage edge's platform, wall and gate; the street piece; the props at their
spots. It never decides where a thing goes; where the map is silent the kit leaves the thing out, except windows on a
face the map gives no window spots for (spaced in bays, a gap noted in the test's NOTES.md).

Built on the shared parts (parts.walls, window, roof_pitched, roof_flat; zinc sheets; gutters; street poles and wires;
vehicles.car; parcels.tree; props; people). New here: the lean-to on timber posts, plank shutters, the plank stall, the
display cabinet and drinks fridge, the breeze-block screen, the steel balcony rail with loops, the plain rendered wall
with piers and the ribbed sheet-steel gate, the raised front platform, the street piece and a lattice mast.
"""
import math

import bpy
from mathutils import Matrix, Vector

from . import goods, gutters, parts, people, props, roadbed, street, vehicles, wear as W
from .core import MeshBuilder, Rng, at, ccw, edge_out, frame, hex_rgb, offset, prism, shade
from .materials import master
from .parcels import tree

DARK = (0.025, 0.022, 0.02)          # an open doorway or a shop's dark inside
TIMBER = hex_rgb('#5e4630')           # sawn timber posts and rafters, weathered
CONCRETE = hex_rgb('#a39f95')
STATE_WEAR = {'rusty': 0.85, 'silver': 0.25, 'painted': 0.35}


def _hex(c, default='#888888'):
    return hex_rgb(c or default)


def mat(name):
    """The kit's master material for a slot; 'slot:surface' is that slot with a photo surface the map picked for one part
    (textured.py), a copy of the slot's master until the textures go on."""
    if ':' not in name:
        return master(name)
    m = bpy.data.materials.get(name)
    if m is None:
        m = master(name.partition(':')[0]).copy()
        m.name = name
    return m


def surfaced(mb, picks):
    """Give the slots the map picked a surface for their own material ('zinc' -> 'zinc:rusty_corrugated_iron')."""
    mb.slots = [f'{s}:{picks[s]}' if picks.get(s) else s for s in mb.slots]
    return mb


# ---------------------------------------------------------------- footprints
def rects(poly):
    """A rectilinear footprint cut into rectangles along x (each a counter-clockwise quad), for pitched roofs."""
    xs = sorted({round(p[0], 3) for p in poly})
    out = []
    for x0, x1 in zip(xs, xs[1:]):
        xm = (x0 + x1) / 2
        ys = []
        n = len(poly)
        for i in range(n):
            a, b = poly[i], poly[(i + 1) % n]
            if (a[0] - xm) * (b[0] - xm) < 0:
                ys.append(a[1] + (b[1] - a[1]) * (xm - a[0]) / (b[0] - a[0]))
        if len(ys) >= 2:
            y0, y1 = min(ys), max(ys)
            if out and abs(out[-1][2] - y0) < 1e-3 and abs(out[-1][3] - y1) < 1e-3 and abs(out[-1][1] - x0) < 1e-3:
                out[-1][1] = x1
            else:
                out.append([x0, x1, y0, y1])
    return [[(r[0], r[2]), (r[1], r[2]), (r[1], r[3]), (r[0], r[3])] for r in out]


def faces(poly):
    """Each wall face: (A, B, length, outward normal, frame with x along, y out, z up at its middle)."""
    out = []
    for i in range(len(poly)):
        A, B = poly[i], poly[(i + 1) % len(poly)]
        n = edge_out(poly, i)
        F = frame(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0), (B[0] - A[0], B[1] - A[1]), n)
        out.append((A, B, math.dist(A, B), n, F))
    return out


def _on_face(fs, x, y, tol=0.6):
    """The face a map point lies on (within tol), and how far along it from its middle."""
    best = None
    for k, (A, B, L, n, F) in enumerate(fs):
        dx, dy = (B[0] - A[0]) / L, (B[1] - A[1]) / L
        t = (x - A[0]) * dx + (y - A[1]) * dy
        d = abs((x - A[0]) * n[0] + (y - A[1]) * n[1])
        if -0.3 <= t <= L + 0.3 and d < tol and (best is None or d < best[2]):
            best = (k, t - L / 2, d)
    return best


# ---------------------------------------------------------------- new parts
def plank_shutter(mb, F, u, w, h, col, wear, rng):
    """Timber plank doors across a lock-up: vertical boards, each its own shade, two ledges, a padlock hasp."""
    mb.face([F @ Vector((u - w / 2, 0.01, 0.05)), F @ Vector((u + w / 2, 0.01, 0.05)), F @ Vector((u + w / 2, 0.01, h)), F @ Vector((u - w / 2, 0.01, h))], 'paint', DARK, 0)
    n = max(2, round(w / 0.16))
    for i in range(n):
        x = u - w / 2 + (i + 0.5) * w / n
        mb.box('wood', at(F, x, 0.04, h / 2 + 0.02), shade(col, rng.between(0.82, 1.12)), min(1, wear + rng.between(-0.15, 0.2)), size=(w / n - 0.012, 0.03, h - 0.04))
    for z in (0.5, h - 0.45):
        mb.box('wood', at(F, u, 0.065, z), shade(col, 0.8), wear, size=(w - 0.1, 0.025, 0.12))
    mb.box('steel', at(F, u, 0.09, h * 0.5), (0.12, 0.12, 0.12), 0.5, size=(0.12, 0.03, 0.06))
    mb.box('wood', at(F, u, 0.05, h + 0.06), shade(col, 0.7), wear, size=(w + 0.16, 0.08, 0.12))   # the head


def dark_opening(mb, F, u, w, h, trim, wear):
    """An open shop door: the dark inside, a frame round it."""
    mb.face([F @ Vector((u - w / 2, 0.012, 0.0)), F @ Vector((u + w / 2, 0.012, 0.0)), F @ Vector((u + w / 2, 0.012, h)), F @ Vector((u - w / 2, 0.012, h))], 'paint', DARK, 0)
    for s in (-1, 1):
        mb.box('wood', at(F, u + s * (w / 2 + 0.04), 0.03, h / 2), trim, wear, size=(0.08, 0.05, h))
    mb.box('wood', at(F, u, 0.03, h + 0.04), trim, wear, size=(w + 0.16, 0.05, 0.08))


def plank_window(mb, F, u, z, w, h, col, wear):
    """A window shut with timber plank shutters (the face-me bungalow's)."""
    mb.box('paint', at(F, u, 0.01, z), shade(col, 0.6), wear, size=(w + 0.14, 0.04, h + 0.14), skip=('-y',))
    for s in (-1, 1):
        mb.box('wood', at(F, u + s * w / 4, 0.04, z), shade(col, 1.0 + 0.06 * s), wear, size=(w / 2 - 0.02, 0.03, h))


def leanto(mb, sp, side, rng):
    """A zinc lean-to on timber posts: its high edge on the wall, the low edge out toward the road on a timber plate,
    posts every 2-3 m. sp: x0, x1, wall_y, depth, z_wall, z_front, sheet_colour, roof_state, edge_colour."""
    s = 1 if side == 'left' else -1
    y_w, y_f = sp['wall_y'] + s * 0.05, sp['wall_y'] - s * sp['depth']
    x0, x1 = sp['x0'], sp['x1']
    wr = STATE_WEAR.get(sp.get('roof_state'), 0.6)
    col = _hex(sp.get('sheet_colour'), '#9a9c98')
    over = 0.15
    A, B = (x0, y_f - s * over, sp['z_front'] - 0.05), (x1, y_f - s * over, sp['z_front'] - 0.05)
    C, D = (x1, y_w, sp['z_wall']), (x0, y_w, sp['z_wall'])
    spec = dict(profile='sine', pitch=0.076, depth=0.018, col=col, col2=shade(col, 0.9), mixed=wr > 0.5, wear=wr,
                sag=0.05 * wr)
    parts.corrugated(mb, A, B, C, D, spec, lambda i: max(0.0, min(1.0, wr + rng.child('sheet', i).between(-0.25, 0.25))))
    # the front plate and the posts under it
    zf = sp['z_front'] - 0.12
    parts.bar(mb, 'wood', (x0, y_f, zf), (x1, y_f, zf), 0.1, TIMBER, 0.7)
    if sp.get('edge_colour'):   # a painted edge board (the red trim on a white sheet)
        parts.bar(mb, 'paint', (x0, y_f - s * (over + 0.02), sp['z_front'] - 0.1), (x1, y_f - s * (over + 0.02), sp['z_front'] - 0.1), 0.08, _hex(sp['edge_colour']), 0.5)
    n = max(1, math.ceil((x1 - x0) / 2.8))
    for k in range(n + 1 if sp.get('posts', 'timber') != 'none' else 0):
        x = x0 + 0.1 + (x1 - x0 - 0.2) * k / n
        lean = rng.between(-0.04, 0.04)
        parts.bar(mb, 'wood', (x, y_f, sp.get('z_foot', 0.0)), (x + lean, y_f, zf), 0.09, shade(TIMBER, rng.between(0.85, 1.15)), 0.7)
        parts.bar(mb, 'wood', (x, y_f, zf), (x, y_w, sp['z_wall'] - 0.08), 0.07, TIMBER, 0.7)   # a rafter back to the wall


def plank_stall(mb, sp, rng, gmb=None):
    """A plank stall against the road edge: a timber frame boarded on three sides, a plank shelf at table height, and a
    heap of sacks and bundles piled on its top."""
    x0, x1, y0, y1, h = sp['x0'], sp['x1'], sp['y0'], sp['y1'], sp['h']
    col = _hex(sp.get('colour'), '#5a3328')
    for x in (x0, x1):
        for y in (y0, y1):
            parts.bar(mb, 'wood', (x, y, 0.35), (x, y, h), 0.08, TIMBER, 0.8)
    # boards: the back and the two ends, a low front with the shelf over it
    for (ax, ay), (bx, by), top in (((x0, y1), (x1, y1), h), ((x0, y0), (x0, y1), h), ((x1, y0), (x1, y1), h), ((x0, y0), (x1, y0), 1.05)):
        L = math.hypot(bx - ax, by - ay)
        n = max(1, round((top - 0.35) / 0.22))
        for k in range(n):
            z = 0.35 + (k + 0.5) * (top - 0.35) / n
            m = Matrix.Translation(((ax + bx) / 2, (ay + by) / 2, z)) @ Matrix.Rotation(math.atan2(by - ay, bx - ax), 4, 'Z')
            mb.box('wood', m, shade(col, rng.between(0.75, 1.15)), 0.8, size=(L + 0.04, 0.03, (top - 0.35) / n - 0.015))
    mb.box('wood', Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, 1.08)), shade(col, 1.1), 0.8, size=(x1 - x0 + 0.1, y1 - y0 + 0.2, 0.05))
    mb.box('wood', Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, h)), shade(col, 0.9), 0.8, size=(x1 - x0 + 0.2, y1 - y0 + 0.2, 0.05))
    gmb = gmb or mb   # the soft goods (sacks, tarp) can go to their own smooth-shaded object
    if sp.get('goods') == 'sacks_on_top':   # sacks, foam and bundles in white, grey and cream, sagging over the edges
        nx_, ny_ = max(1, int((x1 - x0) / 0.85)), max(1, int((y1 - y0) / 0.55))
        for i in range(nx_):   # filled sacks lying in bricked layers, the top layer patchy
            for j in range(ny_):
                z = h + 0.03
                for k in range(rng.randrange(1, 3)):
                    off = 0.2 if k % 2 else 0.0
                    M_ = Matrix.Translation((x0 + (i + 0.5) * (x1 - x0) / nx_ + off * rng.between(-1, 1), y0 + (j + 0.5) * (y1 - y0) / ny_, z)) @ Matrix.Rotation(rng.between(-0.15, 0.15), 4, 'Z')
                    z += goods.sack_lying(gmb, M_, rng.child('sk', i, j, k), 1.0) * 0.9
        mb.box('cloth', Matrix.Translation((x1 + 0.05, (y0 + y1) / 2, h - 0.2)) @ Matrix.Rotation(-0.25, 4, 'Y'), hex_rgb('#d8d2c4'), 0.4, size=(0.9, y1 - y0 + 0.3, 0.05))
    if sp.get('tarp_colour'):   # a tarp thrown over the top, hanging down its road side
        goods.tarp(gmb, x0 - 0.15, x1 + 0.1, y0 - 0.12, y1, h + sp.get('tarp_z_m', 0.5), sp.get('tarp_drop_m', 1.0), _hex(sp['tarp_colour']), rng.child('tarp'), side=-1 if sp['y0'] > 0 else 1)


SNACKS = ['#c62828', '#f9a825', '#1f6fb8', '#2e9a46', '#e8e4dc', '#e07b20', '#6a1b9a', '#d81b60']


def display_cabinet(mb, M, w=0.9, d=0.45, h=0.6, rng=None):
    """A glass display case on a table: an aluminium frame, clear glass, and on its floor and one shelf rows of packets
    (biscuits, sweets, sachets), bottles and tins, packed tight."""
    rng = rng or Rng('cabinet', round(M.translation.x, 2))
    al = hex_rgb('#c8ccce')
    for sx in (-1, 1):
        for sy in (-1, 1):
            mb.box('steel', at(M, sx * w / 2, sy * d / 2, h / 2), al, 0.3, size=(0.025, 0.025, h))
    for z in (0.012, h):
        mb.box('steel', at(M, 0, 0, z), al, 0.3, size=(w + 0.02, d + 0.02, 0.025))
    mb.box('plastic', at(M, 0, 0, h * 0.5), hex_rgb('#e8e8e4'), 0.2, size=(w - 0.03, d - 0.03, 0.012))   # the shelf
    for z0 in (0.025, h * 0.5 + 0.006):
        x = -w / 2 + 0.04
        while x < w / 2 - 0.08:
            c = hex_rgb(rng.pick(SNACKS))
            kind = rng.between(0, 1)
            if kind < 0.5:   # a packet stood up
                pw, ph = rng.between(0.06, 0.11), rng.between(0.12, 0.2)
                for row in (-1, 1):
                    mb.box('plastic', at(M, x + pw / 2, row * d * 0.2, z0 + ph / 2, rz=rng.between(-0.1, 0.1)), c, 0.1, size=(pw, 0.035, ph))
                x += pw + 0.01
            elif kind < 0.8:   # a bottle
                for row in (-1, 1):
                    parts.cyl(mb, 'plastic', at(M, x + 0.03, row * d * 0.2, z0), 0.028, 0.17, c, 0.1, seg=8)
                    parts.cyl(mb, 'plastic', at(M, x + 0.03, row * d * 0.2, z0 + 0.17), 0.012, 0.03, hex_rgb('#e8e4dc'), 0, seg=6)
                x += 0.07
            else:   # a stack of tins
                for k in range(3):
                    parts.cyl(mb, 'steel', at(M, x + 0.04, 0, z0 + k * 0.06), 0.035, 0.058, c, 0.2, seg=10)
                x += 0.09
    for q in (((-1, -1), (1, -1)), ((-1, 1), (1, 1)), ((-1, -1), (-1, 1)), ((1, -1), (1, 1))):   # the glass: sides and top
        (ax, ay), (bx, by) = q
        mb.face([at(M, ax * w / 2, ay * d / 2, 0.02).translation, at(M, bx * w / 2, by * d / 2, 0.02).translation,
                 at(M, bx * w / 2, by * d / 2, h - 0.01).translation, at(M, ax * w / 2, ay * d / 2, h - 0.01).translation], 'glass_clear', hex_rgb('#cfdcdc'), 0)
    mb.face([at(M, -w / 2, -d / 2, h + 0.013).translation, at(M, w / 2, -d / 2, h + 0.013).translation, at(M, w / 2, d / 2, h + 0.013).translation, at(M, -w / 2, d / 2, h + 0.013).translation], 'glass_clear', hex_rgb('#cfdcdc'), 0)


def drinks_fridge(mb, M, h=1.3, col=None, rng=None):
    """A drinks fridge with a glass door: the maker's colour on its body and a brand header, a poster on its side, and
    rows of bottles and cans on wire shelves, seen through the door."""
    rng = rng or Rng('fridge', round(M.translation.x, 2))
    col = col or hex_rgb('#cfd3d6')
    W, D = 0.7, 0.65
    mb.box('plastic', at(M, 0, 0, h / 2), col, 0.4, size=(W, D, h))
    mb.box('plastic', at(M, 0, -D / 2 + 0.02, h / 2 + 0.06), hex_rgb('#dfe3e4'), 0.1, size=(W - 0.12, 0.03, h - 0.36))   # the lit inside
    for r in range(4):
        z = 0.24 + r * (h - 0.42) / 4
        mb.box('steel', at(M, 0, -D / 2 + 0.06, z), hex_rgb('#9aa0a2'), 0.1, size=(W - 0.14, 0.12, 0.01))
        x = -W / 2 + 0.1
        while x < W / 2 - 0.1:
            c = hex_rgb(rng.pick(['#c62828', '#2e9a46', '#f9a825', '#3b2414', '#1f6fb8', '#e07b20', '#bfc9b8']))
            if rng.chance(0.7):   # a bottle
                parts.cyl(mb, 'plastic', at(M, x, -D / 2 + 0.07, z + 0.005), 0.028, 0.15, c, 0, seg=8)
                parts.cyl(mb, 'plastic', at(M, x, -D / 2 + 0.07, z + 0.155), 0.012, 0.04, c, 0, seg=6)
            else:   # a can
                parts.cyl(mb, 'steel', at(M, x, -D / 2 + 0.07, z + 0.005), 0.03, 0.11, c, 0.1, seg=8)
            x += 0.075
    mb.face([at(M, -W / 2 + 0.05, -D / 2 - 0.005, 0.16).translation, at(M, W / 2 - 0.05, -D / 2 - 0.005, 0.16).translation,
             at(M, W / 2 - 0.05, -D / 2 - 0.005, h - 0.2).translation, at(M, -W / 2 + 0.05, -D / 2 - 0.005, h - 0.2).translation], 'glass_clear', hex_rgb('#cfdcdc'), 0)
    mb.box('plastic', at(M, 0, -D / 2 - 0.01, h - 0.1), hex_rgb('#c62828'), 0, size=(W, 0.02, 0.16))   # the brand header
    mb.box('plastic', at(M, 0, -D / 2 - 0.022, h - 0.1), hex_rgb('#f4f1ea'), 0, size=(W * 0.45, 0.004, 0.06))
    for sx in (-1, 1):   # posters stuck on its sides
        mb.box('paint', at(M, sx * (W / 2 + 0.003), 0, h * 0.55), hex_rgb(rng.pick(['#1f6fb8', '#2e9a46', '#e07b20'])), 0.3, size=(0.004, D * 0.6, h * 0.4))
        mb.box('paint', at(M, sx * (W / 2 + 0.006), 0, h * 0.6), hex_rgb('#f4f1ea'), 0.3, size=(0.004, D * 0.4, h * 0.12))


def breeze_screen(mb, a, b, z0, z1, col, rng, cell=0.4):
    """A breeze-block screen from a to b: a grid of hollow blocks, each with a round hole showing the dark behind."""
    L = math.dist(a, b)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    nx, nz = max(1, round(L / cell)), max(1, round((z1 - z0) / cell))
    cw, ch = L / nx, (z1 - z0) / nz
    base = Matrix.Translation((a[0], a[1], z0)) @ Matrix.Rotation(ang, 4, 'Z')
    for i in range(nx):
        for j in range(nz):
            c = shade(col, rng.between(0.9, 1.05))
            m = base @ Matrix.Translation(((i + 0.5) * cw, 0, (j + 0.5) * ch))
            mb.face([m @ Vector((-cw / 2, 0.0, -ch / 2)), m @ Vector((cw / 2, 0.0, -ch / 2)), m @ Vector((cw / 2, 0.0, ch / 2)), m @ Vector((-cw / 2, 0.0, ch / 2))], 'paint', shade(col, 0.25), 0.3)
            # the block's face: a square frame with a ring cut in it (eight segments round the hole)
            r = min(cw, ch) * 0.36
            seg = 8
            for k in range(seg):
                a0, a1 = k / seg * math.tau, (k + 1) / seg * math.tau
                p0 = Vector((math.cos(a0) * r, -0.04, math.sin(a0) * r))
                p1 = Vector((math.cos(a1) * r, -0.04, math.sin(a1) * r))
                q1 = Vector((math.copysign(min(abs(math.cos(a1) * cw / 2 / max(abs(math.cos(a1)), abs(math.sin(a1)))), cw / 2), math.cos(a1)), -0.04, math.copysign(min(abs(math.sin(a1) * ch / 2 / max(abs(math.cos(a1)), abs(math.sin(a1)))), ch / 2), math.sin(a1))))
                q0 = Vector((math.copysign(min(abs(math.cos(a0) * cw / 2 / max(abs(math.cos(a0)), abs(math.sin(a0)))), cw / 2), math.cos(a0)), -0.04, math.copysign(min(abs(math.sin(a0) * ch / 2 / max(abs(math.cos(a0)), abs(math.sin(a0)))), ch / 2), math.sin(a0))))
                mb.face([m @ p0, m @ p1, m @ q1, m @ q0][::-1], 'paint', c, 0.45)
                # the hole's inner wall
                mb.face([m @ p0, m @ Vector((p0.x, 0.0, p0.z)), m @ Vector((p1.x, 0.0, p1.z)), m @ p1][::-1], 'paint', shade(c, 0.6), 0.45)


def loop_rail(mb, a, b, z, h, col, wear, solid_h=0.3, pitch=0.32, pattern='loops'):
    """A steel balcony rail along a to b on the slab edge at z: a solid upstand, then a top and bottom flat bar with a row
    of upright loops (ovals) between, the Lagos rail painted white or cream. pattern 'pickets': plain upright bars."""
    L = math.dist(a, b)
    dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    P = lambda u, zz: Vector((a[0] + dx * u, a[1] + dy * u, zz))
    ang = math.atan2(dy, dx)
    if solid_h > 0:
        mb.box('paint', Matrix.Translation(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, z + solid_h / 2)) @ Matrix.Rotation(ang, 4, 'Z'), col, wear, size=(L, 0.12, solid_h))
    zb, zt = z + solid_h, z + h
    parts.bar(mb, 'steel', P(0, zt), P(L, zt), 0.05, col, wear)
    parts.bar(mb, 'steel', P(0, zb + 0.03), P(L, zb + 0.03), 0.035, col, wear)
    n = max(1, int(L / pitch))
    rx, rz = pitch * 0.38, (zt - zb) * 0.42
    zc = (zt + zb) / 2
    if pattern == 'pickets':
        n = max(1, int(L / 0.13))
        for k in range(n):
            uc = (k + 0.5) * L / n
            parts.bar(mb, 'steel', P(uc, zb + 0.03), P(uc, zt), 0.018, col, wear)
        n = 0
    for k in range(n):
        uc = (k + 0.5) * L / n
        seg = 10
        prev = None
        for j in range(seg + 1):
            t = j / seg * math.tau
            p = P(uc + math.cos(t) * rx, zc + math.sin(t) * rz)
            if prev is not None:
                parts.bar(mb, 'steel', prev, p, 0.022, col, wear)
            prev = p
        parts.bar(mb, 'steel', P(uc, zc + rz), P(uc, zt), 0.022, col, wear)
        parts.bar(mb, 'steel', P(uc, zb + 0.03), P(uc, zc - rz), 0.022, col, wear)
    for u in (0, L):
        parts.bar(mb, 'steel', P(u, zb), P(u, zt), 0.05, col, wear)


def plain_wall(mb, line, h, col, wear, rng, piers=(), mould=True, skip=None, broken=0.0, blotch=0.3, streaks=0.0, foot_stain=0.0):
    """A rendered block wall along a polyline, unpainted grey: mould dark at the top and in patches, red earth up its foot,
    a cement patch or two. piers: points where a square pier stands. skip(x0, x1) -> True leaves a stretch out (a gate).
    broken: the share of 1.2 m bays where the render has come away to the block; blotch: how uneven the grey is.
    streaks: 0..1, black mould runs hanging from the coping; foot_stain: m, how high the damp darkens the wall's foot."""
    for i in range(len(line) - 1):
        a, b = line[i], line[i + 1]
        L = math.dist(a, b)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        n = max(1, round(L / 1.2))
        for k in range(n):
            u0, u1 = L * k / n, L * (k + 1) / n
            pa = (a[0] + (b[0] - a[0]) * u0 / L, a[1] + (b[1] - a[1]) * u0 / L)
            pb = (a[0] + (b[0] - a[0]) * u1 / L, a[1] + (b[1] - a[1]) * u1 / L)
            if skip and skip(pa, pb):
                continue
            m = Matrix.Translation(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2, 0)) @ Matrix.Rotation(ang, 4, 'Z')
            w = u1 - u0
            blot = rng.between(0, 1)
            zs = [0.0, 0.35, 0.9, h - 0.7, h]
            cs = []
            for z in zs:
                c = shade(col, 1.0 + blotch * (blot - 0.5) * (0.6 + 0.4 * math.sin(z * 2.1 + blot * 6)))
                c = W.mix(c, W.DIRT, wear * 0.3 * (1 - W.smooth(0.0, 0.5, z)))
                if mould:
                    c = W.mix(c, W.GRIME, wear * (0.35 + 0.5 * blot) * W.smooth(h - 2.0, h, z))
                    c = W.mix(c, shade(W.GRIME, 1.3), wear * 0.3 * blot * W.smooth(0.5, 1.2, z) * (1 - W.smooth(1.4, 2.0, z)))
                cs.append(c)
            for side in (-1, 1):
                parts._band_face(mb, m, side, -w / 2 - 0.001, w / 2 + 0.001, zs, cs, 'paint', 0.15, y=0.1)
            mb.box('paint', m @ Matrix.Translation((0, 0, h + 0.04)), W.mix(col, W.GRIME, wear * 0.6), wear, size=(w + 0.01, 0.24, 0.08), skip=('-z',))
            if rng.chance(0.25 * wear):   # a cement patch, never painted
                x = rng.between(-w / 2 + 0.2, w / 2 - 0.4)
                z = rng.between(0.4, h - 0.6)
                for side in (-1, 1):
                    q = [m @ Vector((x, side * 0.104, z)), m @ Vector((x + 0.4, side * 0.104, z)), m @ Vector((x + 0.4, side * 0.104, z + 0.35)), m @ Vector((x, side * 0.104, z + 0.35))]
                    mb.face(q[::-1] if side > 0 else q, 'paint', W.CEMENT, wear)
            for _ in range(int(streaks * rng.between(4, 10))):   # black mould run down from the coping, tapering, fading out
                x, sw = rng.between(-w / 2 + 0.05, w / 2 - 0.05), rng.between(0.06, 0.3)
                zb = h - rng.between(0.3, h * 0.85)
                dark = shade(W.GRIME, rng.between(0.25, 0.5))
                for side in (-1, 1):
                    y = side * (0.1035 + rng.between(0, 0.0015))
                    q = [m @ Vector((x - sw * 0.25, y, zb)), m @ Vector((x + sw * 0.25, y, zb)), m @ Vector((x + sw / 2, y, h)), m @ Vector((x - sw / 2, y, h))]
                    cq = [col, col, dark, dark]
                    mb.face(q[::-1] if side > 0 else q, 'paint', cq[::-1] if side > 0 else cq, wear)
            if foot_stain > 0:   # the damp at the foot: a dark band, its top ragged, fading up
                n_ = 4
                for j in range(n_):
                    xa, xb = -w / 2 + w * j / n_, -w / 2 + w * (j + 1) / n_
                    za, zb_ = foot_stain * rng.between(0.5, 1.2), foot_stain * rng.between(0.5, 1.2)
                    wet = shade(W.GRIME, 0.8)
                    for side in (-1, 1):
                        y = side * 0.1032
                        q = [m @ Vector((xa, y, 0.0)), m @ Vector((xb, y, 0.0)), m @ Vector((xb, y, zb_)), m @ Vector((xa, y, za))]
                        cq = [wet, wet, W.mix(col, wet, 0.25), W.mix(col, wet, 0.25)]
                        mb.face(q[::-1] if side > 0 else q, 'paint', cq[::-1] if side > 0 else cq, wear)
            if rng.chance(broken):   # render come away: the sandcrete block and its mortar showing, ragged at the edge
                bw, bh = rng.between(0.4, w - 0.1), rng.between(0.35, 1.2)
                x = rng.between(-w / 2 + bw / 2, w / 2 - bw / 2)
                z = rng.pick([rng.between(0.05, 0.4), rng.between(0.4, h - bh - 0.1)])
                for side in (-1, 1):
                    y = side * 0.105
                    q = [m @ Vector((x - bw / 2, y, z)), m @ Vector((x + bw / 2, y, z)), m @ Vector((x + bw / 2, y, z + bh)), m @ Vector((x - bw / 2, y, z + bh))]
                    bc = shade(W.BLOCK, rng.between(0.45, 0.6))
                    mb.face(q[::-1] if side > 0 else q, 'paint', bc, wear)
                    for _ in range(3):   # its ragged edge: bites of render gone further, here and there
                        ex, ez = rng.between(-bw / 2, bw / 2), rng.pick([z, z + bh])
                        ew, eh = rng.between(0.08, 0.25), rng.between(0.05, 0.15)
                        q2 = [m @ Vector((ex - ew / 2, y * 1.002, ez - eh / 2)), m @ Vector((ex + ew / 2, y * 1.002, ez - eh / 2)), m @ Vector((ex + ew / 2, y * 1.002, ez + eh / 2)), m @ Vector((ex - ew / 2, y * 1.002, ez + eh / 2))]
                        mb.face(q2[::-1] if side > 0 else q2, 'paint', bc, wear)
                    zz = z + 0.225
                    while zz < z + bh - 0.05:   # the bed joints
                        q = [m @ Vector((x - bw / 2, y * 1.01, zz - 0.012)), m @ Vector((x + bw / 2, y * 1.01, zz - 0.012)), m @ Vector((x + bw / 2, y * 1.01, zz + 0.012)), m @ Vector((x - bw / 2, y * 1.01, zz + 0.012))]
                        mb.face(q[::-1] if side > 0 else q, 'paint', W.MORTAR, wear)
                        zz += 0.225
                    # the render's broken lip round it, a shade lighter
                    for z_ in (z - 0.02, z + bh + 0.02):
                        q = [m @ Vector((x - bw / 2 - 0.03, y * 1.005, z_ - 0.02)), m @ Vector((x + bw / 2 + 0.03, y * 1.005, z_ - 0.02)), m @ Vector((x + bw / 2 + 0.03, y * 1.005, z_ + 0.02)), m @ Vector((x - bw / 2 - 0.03, y * 1.005, z_ + 0.02))]
                        mb.face(q[::-1] if side > 0 else q, 'paint', shade(col, 1.15), wear)
    for p in piers:
        mb.box('paint', Matrix.Translation((p[0], p[1], (h + 0.35) / 2)), W.mix(col, W.GRIME, wear * 0.4), wear, size=(0.4, 0.4, h + 0.35), skip=('-z',))


POSTER = ['#c62828', '#1f6fb8', '#2e9a46', '#f9a825', '#6a1b9a', '#e07b20', '#111111']


def wall_marks(mb, y_at, wall, rng, road_y=0.0):
    """What people put on a street wall, on its street face: pasted posters (a church crusade, a party, a funeral), some
    torn, and painted daubs (a phone number, POST NO BILL, a house's warning). The map gives each one's place along the
    wall: wall.posters [{x, z, w, h}], wall.daubs [{x, z, text, colour, size}]."""
    def F(x, z=0.0, off=0.0):
        y = y_at(x)
        out = 1 if road_y > y else -1
        f = frame((x, y + out * (0.104 + off), z), (1, 0) if out > 0 else (-1, 0), (0, out))
        if f.to_3x3().determinant() > 0:
            f = f @ Matrix.Scale(-1, 4, (1, 0, 0))
        return f
    for k, p in enumerate(wall.get('posters', [])):
        r = rng.child('poster', k)
        w, h = p.get('w', 0.6), p.get('h', 0.85)
        bands = [(0.0, 0.18), (0.18, 0.62), (0.62, 0.8), (0.8, 1.0)]
        cs = [hex_rgb(r.pick(POSTER)), hex_rgb('#efe9d8'), hex_rgb(r.pick(POSTER)), hex_rgb(r.pick(POSTER))]
        torn = r.chance(0.5)
        for (a_, b_), c in zip(bands, cs):
            if torn and a_ < 0.1:
                continue   # its foot torn off
            mb.box('cloth', at(F(p['x']), 0, 0.002, p['z'] + h * (a_ + b_) / 2), shade(c, r.between(0.75, 0.95)), 0.5, size=(w, 0.003, h * (b_ - a_)))
        mb.box('skin', at(F(p['x']), -w * 0.18, 0.004, p['z'] + h * 0.4), hex_rgb('#4a2e1f'), 0.3, size=(w * 0.35, 0.003, h * 0.38))   # the face on it
    for k, d in enumerate(wall.get('daubs', [])):
        parts.text(mb, 'paint', at(F(d['x']), 0, 0.004, d['z']), d['text'], d.get('size', 0.16), _hex(d.get('colour'), '#1a1a1a'), max_w=d.get('w'), wobble=0.05)


def sheet_gate(mb, a, b, h, col, wear, rng, leaves=2, wicket=True, number=None):
    """A sheet-steel gate from a to b: a box-section frame, leaves of ribbed sheet (upright ribs), rust rising from the
    foot, a wicket door cut in one leaf, the house number painted on it."""
    L = math.dist(a, b)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    base = Matrix.Translation((a[0], a[1], 0)) @ Matrix.Rotation(ang, 4, 'Z')
    lw = L / leaves
    rust = W.RUST
    for k in range(leaves):
        m = base @ Matrix.Translation((lw * (k + 0.5), 0, 0))
        for zz in (0.05, h - 0.03):
            mb.box('steel', m @ Matrix.Translation((0, 0, zz)), shade(col, 0.8), wear, size=(lw - 0.02, 0.06, 0.06))
        for xx in (-lw / 2 + 0.03, lw / 2 - 0.03):
            mb.box('steel', m @ Matrix.Translation((xx, 0, h / 2)), shade(col, 0.8), wear, size=(0.06, 0.06, h))
        nr = int(lw / 0.11)
        for r in range(nr):   # the ribs: a raised strip every 11 cm, both sides
            x = -lw / 2 + 0.06 + (r + 0.5) * (lw - 0.12) / nr
            zs = [0.08, 0.35, 0.9, h - 0.06]
            cs = [W.mix(col, rust, wear * 1.0), W.mix(col, rust, wear * 0.45), W.mix(col, rust, wear * 0.1), shade(col, 1.04)]
            for side in (-1, 1):
                parts._band_face(mb, m, side, x - 0.045, x + 0.045, zs, [shade(c, 1.0 if r % 2 else 0.92) for c in cs], 'steel', wear, y=0.018 + 0.008 * (r % 2))
        if wicket and k == leaves - 1:   # the wicket door's outline and its handle
            for (x0, z0), (x1, z1) in (((-0.45, 0.15), (0.45, 0.15)), ((0.45, 0.15), (0.45, 1.75)), ((0.45, 1.75), (-0.45, 1.75)), ((-0.45, 1.75), (-0.45, 0.15))):
                mb.box('steel', m @ Matrix.Translation(((x0 + x1) / 2, -0.035, (z0 + z1) / 2)), shade(col, 0.6), wear, size=(abs(x1 - x0) + 0.03, 0.01, abs(z1 - z0) + 0.03))
            mb.box('steel', m @ Matrix.Translation((0.3, -0.05, 1.0)), (0.1, 0.1, 0.1), 0.4, size=(0.12, 0.03, 0.05))
        if number and k == leaves - 1:
            parts.text(mb, 'paint', m @ Matrix.Translation((0, -0.04, h * 0.72)) @ Matrix.Rotation(math.pi, 4, 'Z') @ Matrix.Scale(-1, 4, (1, 0, 0)), number, 0.32, shade(col, 1.35))
    # the bolt bar across the middle
    mb.box('steel', base @ Matrix.Translation((L / 2, -0.045, 1.0)), (0.12, 0.12, 0.12), 0.5, size=(0.5, 0.03, 0.05))


def lattice_mast(mb, x, y, h, col=None):
    """A telecom mast: three legs tapering, braced, a few panels near the top."""
    col = col or hex_rgb('#9a9c9e')
    legs = [(math.cos(a), math.sin(a)) for a in (0, math.tau / 3, 2 * math.tau / 3)]
    r0, r1 = 1.6, 0.5
    rr = lambda z: r0 + (r1 - r0) * z / h
    for lx, ly in legs:
        parts.bar(mb, 'steel', (x + lx * r0, y + ly * r0, 0), (x + lx * r1, y + ly * r1, h), 0.12, col, 0.3)
    for k in range(int(h / 3)):
        z0, z1 = k * 3, k * 3 + 3
        for i in range(3):
            (ax, ay), (bx, by) = legs[i], legs[(i + 1) % 3]
            parts.bar(mb, 'steel', (x + ax * rr(z0), y + ay * rr(z0), z0), (x + bx * rr(z1), y + by * rr(z1), z1), 0.05, col, 0.3)
    for k in range(3):
        a = k * math.tau / 3 + 0.5
        mb.box('steel', Matrix.Translation((x + math.cos(a) * 0.8, y + math.sin(a) * 0.8, h - 2)) @ Matrix.Rotation(a, 4, 'Z'), hex_rgb('#d9d9d6'), 0.2, size=(0.1, 0.5, 1.6))


# ---------------------------------------------------------------- a building from its map record
def building(b, collection=None):
    rng = Rng('oldtown', b['id'])
    poly = ccw([tuple(p) for p in b['footprint']])
    wf = b.get('wall_finish', {})
    paint = _hex(wf.get('wall_colour'), '#d8cfbf')
    roof = b.get('roof', {})
    rtype = roof.get('type', 'hip_zinc')
    flat = rtype == 'flat_parapet'
    storeys = b.get('storeys', 1)
    if b.get('storey_h_m'):
        sh = list(b['storey_h_m'])
    else:
        H0 = b.get('wall_h_m', storeys * parts.STOREY)
        sh = [H0 / storeys] * storeys
    H = sum(sh)
    levels = [sum(sh[:k]) for k in range(storeys)]
    wear = b.get('wear', 0.65)
    trim = _hex(wf.get('trim_colour'), '#e8e4dc')
    spec = dict(paint=paint, wear=wear, storeys=1, trim=trim, chamfer=0.06, lift=0.0,
                plinth=_hex(wf.get('base_band_colour')) if wf.get('base_band') else shade(paint, 0.7),
                plinth_h=wf.get('base_band_h', 1.0) if wf.get('base_band') else 0.3,
                bare=wf.get('finish') == 'bare_block',
                roof=dict(form='flat' if flat else 'hip'),
                parapet=dict(parapet_h=roof.get('parapet_h_m', 0.7), paint=paint, trim=trim, slab=hex_rgb('#8f8a80'), wear=wear))
    mb = MeshBuilder()
    parts.walls(mb, poly, H, spec)
    wx = spec['_wx']
    if wf.get('storey_bands'):
        for z in levels[1:]:
            prism(mb, 'paint', offset(poly, 0.06), z - 0.12, z + 0.12, _hex(wf['storey_bands']), _hex(wf['storey_bands']), wear)
    fs = faces(poly)
    street_side = -1 if b.get('side') == 'left' else 1   # the street lies toward -y from a left-hand building
    on_street = lambda n: n[1] * street_side > 0.7
    if wf.get('side_colour'):   # a face toward the street painted another colour
        for A, B, L, n, F in fs:
            if on_street(n):
                c = _hex(wf['side_colour'])
                mb.face([F @ Vector((-L / 2, 0.012, 0.3)), F @ Vector((L / 2, 0.012, 0.3)), F @ Vector((L / 2, 0.012, H)), F @ Vector((-L / 2, 0.012, H))], 'paint', c, wear)

    # shop fronts the map lists (x from..to along the street face)
    taken = {i: [] for i in range(len(fs))}
    openings = {i: [] for i in range(len(fs))}   # (kind, u, z, w, h, barred) per face, for the weathering
    for s in b.get('shopfronts', []):
        hit = None
        for k, (A, B, L, n, F) in enumerate(fs):
            if on_street(n):
                hit = (k, F, A, B, L)
        if not hit:
            continue
        k, F, A, B, L = hit
        xm = (s['from_x'] + s['to_x']) / 2
        dx = (B[0] - A[0]) / L
        u = (xm - (A[0] + B[0]) / 2) * dx
        w = s['to_x'] - s['from_x']
        r = rng.child('shop', s['from_x'])
        if s['door'] == 'plank_shutter':
            plank_shutter(mb, F, u, w, min(2.45, H - 0.5), _hex(s.get('colour'), '#6b3b2e'), 0.7, r)
        elif s['door'] == 'roll_up':
            parts.roller_shutter(mb, F, u, w, dict(col=_hex(s.get('colour'), '#9aa3a8'), open=s.get('open', 0.7), wear=0.6))
        else:
            dark_opening(mb, F, u, w, min(2.3, H - 0.5), shade(_hex(s.get('frame_colour'), '#5a3a2a'), 1.0), 0.6)
        taken[k].append((u - w / 2 - 0.3, u + w / 2 + 0.3))
        openings[k].append(('door', u, 1.2, w, 2.4, False))

    # windows: where the map puts them; on a face with no spots from the map, in bays (the gap noted in NOTES.md)
    wtype = b.get('windows', 'louvre_glass')
    spots = b.get('window_spots')
    win = dict(type='louvre' if wtype.startswith('louvre') else ('casement' if wtype == 'casement' else 'sliding'), w=1.0, h=1.15,
               frame=trim, glass=hex_rgb('#26323a'), mullion=hex_rgb('#b8bcc0'), bars=b.get('window_bars', 'none'), bar_col=_hex(b.get('bar_colour'), '#262626'), wear=wear, hood=False)
    shut = _hex(b['window_shutters']) if b.get('window_shutters') else None

    ac = b.get('ac_units', 0.0)

    def put_window(F, u, z, k):
        openings[k].append(('window', u, z, 1.0, 1.15, False))
        r_ = rng.child('ac', k, round(u, 1), round(z, 1))
        if r_.chance(ac):   # a split unit's outdoor box beside the window, on two brackets, its pipe run down the wall
            s_ = r_.pick((-1, 1))
            c_ = shade(hex_rgb('#dcdcd6'), r_.between(0.8, 1.0))
            mb.box('paint', at(F, u + s_ * 1.05, 0.18, z - 0.55), c_, 0.6, size=(0.8, 0.3, 0.55))
            mb.box('paint', at(F, u + s_ * 1.05, 0.33, z - 0.55), shade(c_, 0.45), 0.6, size=(0.42, 0.01, 0.42))   # the fan grille
            parts.bar(mb, 'steel', F @ Vector((u + s_ * 0.7, 0.04, z - 0.6)), F @ Vector((u + s_ * 0.7, 0.04, max(0.3, z - 2.6))), 0.025, hex_rgb('#e6e4dc'), 0.4)
        if wtype in ('plank_shutter', 'louvre_timber'):
            plank_window(mb, F, u, z, 0.9, 1.1, _hex(b.get('shutter_colour'), '#6b4a33'), wear)
        else:
            parts.window(mb, F, u, z, win)
            if shut:   # side shutters standing open
                for s_ in (-1, 1):
                    mb.box('wood', at(F, u + s_ * (win['w'] / 2 + 0.28), 0.05, z), shut, wear, size=(0.5, 0.03, win['h']))

    bal_runs = b.get('balcony', {}).get('runs', [])
    gf_runs = (b.get('ground_floor_front') or {}).get('runs', [])
    if spots is not None:
        for sp in spots:
            hit = _on_face(fs, sp['x'], sp['y'])
            if hit:
                k, u, _ = hit
                put_window(fs[k][4], u, levels[sp.get('storey', 0)] + 1.5, k)
    else:
        for k, (A, B, L, n, F) in enumerate(fs):
            use = L - 1.6
            nb = int(use / 3.0) if use > 1.0 else 0
            nb = max(nb, 1) if use > 1.0 else 0
            for st in range(storeys):
                if st == 0 and (on_street(n) and (gf_runs or b.get('shopfronts'))):
                    continue
                for j in range(nb):
                    u = (j - (nb - 1) / 2) * use / max(1, nb)
                    if any(a <= u <= c for a, c in taken[k]):
                        continue
                    put_window(F, u, levels[st] + min(1.55, sh[st] * 0.55), k)

    # ground floor front: a breeze-block screen (the closed verandah)
    for run in gf_runs:
        (ax, ay), (bx, by) = run['a'], run['b']
        off = run.get('out', 0.05)
        n = (0, 1) if b.get('side') == 'right' else (0, -1)   # out toward the street
        a2, b2 = (ax + n[0] * off, ay + n[1] * off), (bx + n[0] * off, by + n[1] * off)
        if run.get('screen') == 'breeze_block':
            # wound so the block faces look toward the street
            if b.get('side') == 'right':
                a2, b2 = b2, a2
            breeze_screen(mb, a2, b2, 0.0, run.get('h', sh[0] - 0.05), _hex(run.get('colour'), '#b9bcbc'), rng.child('breeze'))

    # balconies on the map's runs: a slab out from the wall, a loop rail or a solid parapet on its edge
    bal = b.get('balcony', {})
    for run in bal_runs:
        (ax, ay), (bx, by) = run['a'], run['b']
        st = run.get('storey', 1)
        z = levels[st] - 0.05
        d = run.get('depth', bal.get('depth_m', 1.2))
        L = math.dist((ax, ay), (bx, by))
        dxu, dyu = (bx - ax) / L, (by - ay) / L
        out = run['out']
        ex = (ax + out[0] * d, ay + out[1] * d), (bx + out[0] * d, by + out[1] * d)
        slab_c = hex_rgb('#c9c3b6')
        cx, cy = (ax + bx) / 2 + out[0] * d / 2, (ay + by) / 2 + out[1] * d / 2
        mb.box('concrete', Matrix.Translation((cx, cy, z)) @ Matrix.Rotation(math.atan2(dyu, dxu), 4, 'Z'), slab_c, wear, size=(L + 0.1, d, 0.16))
        rc = _hex(run.get('rail_colour') or bal.get('rail_colour'), '#ece8de')
        kind = run.get('balcony_rail', bal.get('balcony_rail', 'steel'))
        if kind == 'solid':
            loop_rail(mb, ex[0], ex[1], z + 0.08, 1.0, rc, wear, solid_h=1.0)
        else:
            loop_rail(mb, ex[0], ex[1], z + 0.08, 1.0, rc, wear, solid_h=run.get('solid_h', 0.25), pattern=run.get('rail_pattern', bal.get('rail_pattern', 'loops')))
        if run.get('posts'):
            for p in run['posts']:
                parts.bar(mb, 'paint', (p[0], p[1], z), (p[0], p[1], H), 0.22, paint, wear)

    # dishes fixed to the wall, and a scaffold up the street face (tubes, ledgers, braces, a few planks)
    street_faces = [(k, f) for k, f in enumerate(fs) if on_street(f[3])]
    for d_ in b.get('wall_dishes', []):
        for k, (A, B, L, n, F) in street_faces:
            u = (d_['x'] - (A[0] + B[0]) / 2) * (B[0] - A[0]) / L
            if abs(u) < L / 2:
                Fd = F @ Matrix.Translation((u, 0.45, d_.get('z', 6.0))) @ Matrix.Rotation(-1.2, 4, 'X') @ Matrix.Rotation(0.4, 4, 'Y')
                parts.cyl(mb, 'paint', Fd, d_.get('r', 0.4), 0.05, _hex(d_.get('colour'), '#3f7ad0'), 0.3, seg=16, r2=d_.get('r', 0.4) * 0.85)
                parts.bar(mb, 'steel', F @ Vector((u, 0.02, d_.get('z', 6.0) - 0.3)), F @ Vector((u, 0.4, d_.get('z', 6.0))), 0.03, hex_rgb('#5a5a5a'), 0.5)
    sc = b.get('scaffold')
    if sc:
        tube = _hex(sc.get('colour'), '#8a5a3a')
        out_ = sc.get('out_m', 0.9)
        top = sc.get('h_m', H + 1.0)
        for k, (A, B, L, n, F) in street_faces:
            dx = (B[0] - A[0]) / L
            ua, ub = sorted(((sc.get('from_x', -1e9) - (A[0] + B[0]) / 2) * dx, (sc.get('to_x', 1e9) - (A[0] + B[0]) / 2) * dx))
            ua, ub = max(ua, -L / 2), min(ub, L / 2)
            if ub - ua < 1.0:
                continue
            nb = max(1, round((ub - ua) / 2.0))
            us = [ua + (ub - ua) * j / nb for j in range(nb + 1)]
            lifts = [z for z in (2.0 * i for i in range(1, int(top / 2.0) + 1))]
            r_ = rng.child('scaffold', k)
            for u in us:   # standards, inner and outer
                for o in (0.25, out_):
                    parts.bar(mb, 'steel', F @ Vector((u, o, 0.0)), F @ Vector((u + r_.between(-0.04, 0.04), o, top)), 0.05, shade(tube, r_.between(0.8, 1.1)), 0.7)
            for z in lifts:   # ledgers along, transoms back to the wall, planks on some lifts
                for o in (0.25, out_):
                    parts.bar(mb, 'steel', F @ Vector((ua, o, z)), F @ Vector((ub, o, z)), 0.045, tube, 0.7)
                for u in us:
                    parts.bar(mb, 'steel', F @ Vector((u, 0.02, z + 0.05)), F @ Vector((u, out_ + 0.1, z + 0.05)), 0.04, tube, 0.7)
                if r_.chance(sc.get('planks', 0.4)):
                    mb.box('wood', F @ Matrix.Translation(((ua + ub) / 2, (0.25 + out_) / 2, z + 0.1)), shade(TIMBER, r_.between(0.8, 1.1)), 0.8, size=(ub - ua, out_ - 0.15, 0.04))
            for j in range(nb):   # a brace across every other bay, the zigzag up the face
                if j % 2 == 0:
                    parts.bar(mb, 'steel', F @ Vector((us[j], out_ + 0.06, 0.2)), F @ Vector((us[j + 1], out_ + 0.06, min(top, 2.0 * 2))), 0.04, tube, 0.7)
                    if top > 6:
                        parts.bar(mb, 'steel', F @ Vector((us[j + 1], out_ + 0.06, 4.0)), F @ Vector((us[j], out_ + 0.06, min(top, 8.0))), 0.04, tube, 0.7)

    # stains: rain run down from the eaves and the sills, cement patches, render broken off at the foot (wear.age_face)
    stains = wf.get('stains', 'none')
    if stains != 'none':
        for k, (A, B, L, n, F) in enumerate(fs):
            for rep_ in range(2 if stains == 'heavy' else 1):
                W.age_face(mb, F, L, H, wx, openings[k], levels[1:], rng.child('stains', k, rep_), flat_top=flat)

    # roof
    if flat:
        parts.roof_flat(mb, poly, H, spec['parapet'])
    elif roof.get('form') == 'mono':
        xs_, ys_ = [p[0] for p in poly], [p[1] for p in poly]
        left = b.get('side') == 'left'
        back, front = (max(ys_), min(ys_)) if left else (min(ys_), max(ys_))
        eave = roof.get('eave_depth_m', 1.0)
        tn = math.tan(math.radians(roof.get('pitch_deg', 8)))
        D = abs(back - front)
        state = roof.get('roof_state', 'rusty')
        sp_ = dict(x0=min(xs_) - 0.1, x1=max(xs_) + 0.1, wall_y=back, depth=D + eave, z_wall=H + tn * D, z_front=H - tn * eave,
                   sheet_colour=roof.get('colour', '#6e4f40'), roof_state=state, posts=roof.get('posts', 'timber'), z_foot=roof.get('post_foot_m', 0.0))
        rmb = MeshBuilder()   # its own object so the zinc slot can carry the roof's surface
        leanto(rmb, sp_, 'left' if left else 'right', rng.child('mono'))
        surfaced(rmb, {'zinc': roof.get('surface')}).to_object(b['id'] + '_roof', collection, mat)
        for x in (min(xs_), max(xs_)):   # the gable ends filled up to the sheet
            mb.face([(x, front, H), (x, back, H), (x, back, H + tn * D)][::1 if (x == min(xs_)) == left else -1], 'paint', paint, wear)
    else:
        longspan = rtype == 'longspan'
        state = roof.get('roof_state', 'rusty')
        col = _hex(roof.get('colour'), '#6e4f40')
        rw = STATE_WEAR.get(state, 0.7)
        for q in rects(poly):
            rs = dict(form=roof.get('form', 'hip'), pitch_deg=roof.get('pitch_deg', 15), overhang=roof.get('eave_depth_m', 0.6),
                      profile='trapezoid' if longspan else 'sine', pitch=0.2 if longspan else 0.076, depth=0.032 if longspan else 0.018,
                      col=col, col2=shade(col, 0.88), mixed=state == 'rusty', wear=rw, wall_wear=wear, gable_col=paint,
                      fascia=_hex(roof.get('fascia_colour'), '#5a3a2a'), fascia_wood=roof.get('fascia') == 'timber')
            r = parts.roof_pitched(mb, ccw(q), H, rs, rng.child('roof', q[0]))
            fh = roof.get('fascia_h_m')
            if fh:   # a deep fascia board round the eave
                for e0, e1 in ((r['A'], r['B']), (r['B'], r['C']), (r['C'], r['D']), (r['D'], r['A'])):
                    m = Matrix.Translation(((e0[0] + e1[0]) / 2, (e0[1] + e1[1]) / 2, r['y0'] - fh / 2 + 0.02)) @ Matrix.Rotation(math.atan2(e1[1] - e0[1], e1[0] - e0[0]), 4, 'Z')
                    mb.box('wood' if roof.get('fascia') == 'timber' else 'paint', m, rs['fascia'], wear, size=(math.dist(e0, e1) + 0.05, 0.05, fh))
                    if roof.get('edge_colour'):   # the sheet's turned-down edge flashing above it
                        mb.box('zinc', m @ Matrix.Translation((0, 0, fh / 2 + roof.get('edge_h_m', 0.15) / 2)), _hex(roof['edge_colour']), 0.3, size=(math.dist(e0, e1) + 0.08, 0.04, roof.get('edge_h_m', 0.15)))
    surfaced(mb, {'zinc': roof.get('surface'), 'paint': wf.get('surface')})
    return mb.to_object(b['id'], collection, mat)


# ---------------------------------------------------------------- frontage edges
def frontage(e, collection=None):
    rng = Rng('oldtown', e['id'])
    mb = MeshBuilder()
    kind = e['frontage_edge']
    s = 1 if e.get('side') == 'left' else -1
    if kind in ('platform_house', 'leanto_to_road', 'shop_line_step'):
        h = e.get('platform_height_m', 0.3)
        y_line, y_front = e['line_y'], e['platform_front_y']
        x0, x1 = e['from_x'], e['to_x']
        poly = ccw([(x0, y_front), (x1, y_front), (x1, y_line + s * 0.05), (x0, y_line + s * 0.05)])
        pc = _hex(e.get('platform_colour'), '#a39f95')
        prism(mb, 'concrete', poly, 0, h, shade(pc, 0.6), shade(pc, 0.85), 0.1, cap=True, cap_col=shade(pc, 0.95))
        # the broken front edge: a few chips out of the face
        for k in range(int((x1 - x0) / 3)):
            x = rng.between(x0 + 0.5, x1 - 0.5)
            mb.box('concrete', Matrix.Translation((x, y_front - s * 0.01, h - 0.06)), shade(pc, 0.55), 0.9, size=(rng.between(0.2, 0.6), 0.03, 0.1))
    elif kind == 'wall_gate':
        wall = e['wall']
        g = e.get('gate') or {}
        line = [tuple(p) for p in e['line']]
        gx0, gx1 = g.get('from_x', 1e9), g.get('to_x', -1e9)
        skip = lambda pa, pb: (pa[0] + pb[0]) / 2 > gx0 - 0.05 and (pa[0] + pb[0]) / 2 < gx1 + 0.05
        # the gate's two piers
        def y_at(x):
            for a, b in zip(line, line[1:]):
                if min(a[0], b[0]) - 1e-6 <= x <= max(a[0], b[0]) + 1e-6 and abs(b[0] - a[0]) > 1e-6:
                    return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
            return line[0][1]
        piers = [(gx0 - 0.2, y_at(gx0)), (gx1 + 0.2, y_at(gx1))] if g else []
        plain_wall(mb, line, wall.get('h', 2.2), _hex(wall.get('wall_colour'), '#8e8d87'), 0.85 if wall.get('state') == 'mouldy' else 0.5, rng.child('wall'), piers=piers, skip=skip,
                   broken=wall.get('render_broken', 0.0), blotch=wall.get('blotch', 0.3), streaks=wall.get('mould_streaks', 0.0), foot_stain=wall.get('foot_stain_m', 0.0))
        wall_marks(mb, y_at, wall, rng.child('marks'))
        if g:
            a, b = (gx0, y_at(gx0)), (gx1, y_at(gx1))
            if s < 0:   # the gate's face toward the street
                a, b = b, a
            sheet_gate(mb, a, b, g.get('h', 2.0), _hex(g.get('colour'), '#6f757a'), g.get('wear', 0.6), rng.child('gate'), leaves=g.get('leaves', 2), wicket=g.get('wicket', False), number=g.get('house_number'))
        surfaced(mb, {'steel': g.get('surface'), 'paint': wall.get('surface')})
    return mb.to_object(e['id'], collection, mat)


# ---------------------------------------------------------------- the street piece
GROUNDS = []   # the street pieces' ground built so far, so props stand on it rather than at zero


def ground_z(x, y):
    """The ground's height at (x, y): the roadbed's where a street piece has one, else zero."""
    for G in GROUNDS:
        if G.x0 - 5 <= x <= G.x1 and G.ys[0] <= y <= G.ys[1]:
            return float(G.height(x, y))
    return 0.0


def street_piece(sp, collection=None, extent=(-40, 220, -60, 60)):
    rng = Rng('oldtown', sp['id'])
    mb = MeshBuilder()
    (x0, cy), (x1, _) = sp['centreline'][0], sp['centreline'][-1]
    w = sp['width_m']
    yl, yr = cy + w / 2, cy - w / 2
    X0, X1, Y0, Y1 = extent
    G = None
    if sp.get('relief') or 'tar_cover' in sp:   # the ground as real geometry, humps, dips, potholes and patches (roadbed.py)
        zb = -0.08 - 2 * (sp.get('relief') or {}).get('amp_m', 0.0)   # under the sheet's deepest dips
        mb.face([(X0, Y0, zb), (X1, Y0, zb), (X1, Y1, zb), (X0, Y1, zb)], 'mud', hex_rgb('#7a5a44'), 0.1)
        _, G = roadbed.build(sp, collection, materials=master)
        GROUNDS.append(G)
    else:   # the ground everywhere (earth), then the tar laid on it in strips so its edge can fray into the earth
        tar = hex_rgb('#665e57')
        mb.face([(X0, Y0, -0.02), (X1, Y0, -0.02), (X1, Y1, -0.02), (X0, Y1, -0.02)], 'mud', hex_rgb('#8a8174'), 0.1)
        step = 2.0
        n = int((x1 - x0) / step)
        for k in range(n):
            xa, xb = x0 + k * step, x0 + (k + 1) * step
            fa, fb = rng.between(-0.25, 0.1), rng.between(-0.25, 0.1)   # the frayed edges
            ga, gb = rng.between(-0.1, 0.25), rng.between(-0.1, 0.25)
            mb.face([(xa, yr + ga, 0.0), (xb, yr + gb, 0.0), (xb, yl + fb, 0.0), (xa, yl + fa, 0.0)], 'asphalt', shade(tar, rng.between(0.95, 1.05)), 0.5)
        if sp.get('sand_cover') == 'edges':   # dust and sand blown onto the tar edges, fading out onto the tar
            sand, dust = hex_rgb('#8a8276'), shade(tar, 1.05)
            for k in range(n):
                xa, xb = x0 + k * step, x0 + (k + 1) * step
                for y_e, s in ((yl, -1), (yr, 1)):
                    wd = rng.between(0.3, 0.8)
                    mb.face([(xa, y_e, 0.004), (xb, y_e, 0.004), (xb, y_e + s * wd, 0.004), (xa, y_e + s * wd, 0.004)][::s], 'mud', [sand, sand, dust, dust][::s], 0.1)
    gz = (lambda x, y: float(G.height(x, y))) if G else (lambda x, y: 0.0)
    lt = sp.get('litter') or {}
    if lt and G is not None:   # litter spread thin, gathered at the walls and in the ruts (and the low spots, where water left it)
        lr = rng.child('litter')
        xa, xb = max(x0, lt.get('from_x', x0)), min(x1, lt.get('to_x', 60.0))
        ya, yb = cy - w / 2 - 1.2, cy + w / 2 + 0.2
        n = int(lt.get('per_m2', 0.05) * (xb - xa) * (yb - ya) * 4)
        for _ in range(n):
            x, y = lr.between(xa, xb), lr.between(ya, yb)
            edge = max(0.0, 1 - (w / 2 - abs(y - cy)) / 1.2)
            rut = float(G._ruts(x, y, 'depth')) / 0.05 + float(G._edge_rut(x, y)) / 0.1
            if lr.chance((1 + lt.get('walls', 3.0) * edge + lt.get('ruts', 2.0) * min(1.0, rut)) / (1 + lt.get('walls', 3.0) + lt.get('ruts', 2.0))):
                street.litter_piece(mb, x, y, gz(x, y) + 0.004, lr)
    vr = sp.get('verge_right') or {}
    if vr.get('surface') == 'concrete_apron':
        xa, xb = x0, vr.get('upto_x', x1)
        y0_, y1_ = yr - vr['width'] - 0.4, yr + 0.05
        n_ = max(1, int((xb - xa) / 0.5))   # in short pieces laid on the ground, cracked at the joints
        for k in range(n_):
            a_, b_ = xa + (xb - xa) * k / n_, xa + (xb - xa) * (k + 1) / n_ - 0.015
            z = [gz(a_, y0_) + 0.035, gz(b_, y0_) + 0.035, gz(b_, y1_) + 0.035, gz(a_, y1_) + 0.035]
            mb.face([(a_, y0_, z[0]), (b_, y0_, z[1]), (b_, y1_, z[2]), (a_, y1_, z[3])], 'concrete', shade(hex_rgb('#8f8b83'), rng.between(0.85, 1.05)), 0.4)
    g = sp.get('gutter_left') or {}
    if g.get('type', 'none') != 'none':
        y = cy + g['offset_m']
        gutters.gutter(mb, [(x0, y), (x1, y)], dict(id=sp['id'] + 'L', w=g['width'], depth=0.5, state='covered' if g['type'] == 'slab_covered' else 'open',
                                                    blocked=[{'from': 0, 'to': 999, 'fill': 'rubbish'}] if g.get('state') == 'half_blocked' else [],
                                                    **{k: g[k] for k in ('slab_colour', 'dust', 'open_share', 'broken', 'rock', 'litter') if k in g}),
                       lambda p: True, wear=g.get('wear', 0.2))
        for c in sp.get('crossings', []):
            if c.get('side') == 'left':
                mb.box('concrete', Matrix.Translation((c['x'], y, 0.27)) @ Matrix.Rotation(rng.between(-0.03, 0.03), 4, 'Z'), shade(_hex(g.get('slab_colour'), '#a39f95'), rng.between(0.85, 1.0)), 0.7, size=(c['w'], g['width'] + 0.7, 0.1))
    return mb.to_object(sp['id'], collection, master)


# ---------------------------------------------------------------- props at their spots
def spot_props(P, collection=None):
    mb = MeshBuilder()
    gmb = MeshBuilder()   # goods and clutter, shaded smooth
    hmb = MeshBuilder()   # hard goods (crates, basins, cartons), flat shaded with crisp edges
    rng = Rng('oldtown', 'props')
    tops = []
    for k, p in enumerate(P.get('poles', [])):
        pts, top = street.pole(mb, p['x'], p['y'], rng.child('pole', k), h=p.get('h', 9.5), wood=p.get('type') == 'timber')
        tops.append(pts)
    for wspec in P.get('wires', []):
        a = tops[wspec['from_pole']]
        bs = tops[wspec['to_pole']] if 'to_pole' in wspec else [Vector(wspec['to_xyz']) + Vector((0, 0.4 * (i - 1), 0)) for i in range(3)]
        for i in range(wspec.get('n', 2)):
            street.wire(mb, a[i % 3], bs[i % 3], wspec.get('sag', 0.5))
    for m in P.get('masts', []):
        lattice_mast(mb, m['x'], m['y'], m['h'])
    for t in P.get('trees', []):
        tree(mb, t['x'], t['y'], rng.child('tree', t['x']), kind=t.get('kind', 'palm'), h=t.get('h'))
    for k, s in enumerate(P.get('trade_spots', [])):
        r = rng.child('trade', k)
        side = 'left' if s.get('y', s.get('wall_y', s.get('y0', 0))) > 0 else 'right'
        if s['type'] == 'lean-to row':
            if s.get('surface'):   # a sheet the map gave its own photo surface: its own object, so its zinc can differ
                lmb = MeshBuilder()
                leanto(lmb, s, side, r)
                surfaced(lmb, {'zinc': s['surface']}).to_object(f'leanto_{k}', collection, mat)
            else:
                leanto(mb, s, side, r)
            sgn = 1 if side == 'left' else -1
            g0, h0 = len(gmb.cols), len(hmb.cols)
            goods.band(gmb, s['x0'] + 0.15, s['x1'] - 0.15, s['wall_y'], s.get('goods_depth_m', 0.9), s.get('stand_z_m', 0.0),
                       s.get('goods_kinds', []), s.get('goods_fill', 0.0), r.child('goods'), side=sgn, tarp_over=s.get('goods_tarp', False), hard=hmb, cols=s.get('goods_colours'))
            goods.hanging(gmb, s['x0'], s['x1'], s['wall_y'] - sgn * (s['depth'] - 0.08), s['z_front'] - 0.15,
                          s.get('hanging_kinds', []), s.get('hanging_fill', 0.0), r.child('hang'))
            goods.weather(gmb, g0, s.get('goods_tone', 1.0), s.get('goods_dust', 0.0))
            goods.weather(hmb, h0, s.get('goods_tone', 1.0), s.get('goods_dust', 0.0))
        elif s['type'] == 'umbrella':   # a market umbrella over a seller's spot
            z = ground_z(s['x'], s['y'])
            props.umbrella(mb, Matrix.Translation((s['x'], s['y'], z)) @ Matrix.Rotation(r.between(0, 1), 4, 'Z'), s.get('r', 1.1), s.get('h', 2.2), s.get('colours'))
            if s.get('goods_kinds'):
                goods.heap(gmb, s['x'], s['y'], 0.5, z, s['goods_kinds'], r.child('goods'), hard=hmb, cols=s.get('goods_colours'))
        elif s['type'] == 'kiosk' and s.get('kiosk_kind') == 'plank_stall':
            plank_stall(mb, s, r, gmb)
        elif s['type'] == 'kiosk' and s.get('kiosk_kind') == 'drinks_fridge':
            drinks_fridge(mb, Matrix.Translation((s['x'], s['y'], 0.3)) @ Matrix.Rotation(math.radians(s.get('facing_deg', 0)), 4, 'Z'), s.get('h', 1.3), _hex(s.get('colour'), '#cfd3d6'), r)
        elif s['type'] == 'table':
            M = Matrix.Translation((s['x'], s['y'], 0.3))
            items = s.get('items', [])
            if any(i.startswith('crate') for i in items):   # a stack of crates on the platform
                for j, it in enumerate(items):
                    props.crate(mb, M @ Matrix.Translation((0, 0, j * 0.3)) @ Matrix.Rotation(r.between(-0.1, 0.1), 4, 'Z'), _hex(it.split(':')[1]), 0.4)
                continue
            props.table(mb, M, s['w'], s['d'])
            for j, it in enumerate(items):
                u = (j - (len(items) - 1) / 2) * s['w'] / max(1, len(items))
                if it == 'display_cabinet':
                    display_cabinet(mb, M @ Matrix.Translation((u, 0, 0.8)), w=min(1.1, s['w'] / len(items) - 0.1), rng=r.child('cab', j))
                elif it.startswith('basin'):
                    props.basin(mb, M @ Matrix.Translation((u, 0, 0.8)), _hex(it.split(':')[1]))
    for s in P.get('signs', []):
        F = frame(((s['x0'] + s['x1']) / 2, s['wall_y'] - (0.04 if s['side'] == 'left' else -0.04), 0), (1, 0) if s['side'] == 'right' else (-1, 0), (0, -1) if s['side'] == 'left' else (0, 1))
        props.board(mb, F, s['text'], s['x1'] - s['x0'], s['z1'] - s['z0'], _hex(s['bg']), _hex(s['fg']), 0.5, hand=True, z=(s['z0'] + s['z1']) / 2)
    for k, v in enumerate(P.get('parked_vehicles', [])):
        a = math.radians(v.get('heading_deg', 0))   # on the ground: its height and pitch from where its wheels stand
        zf, zr = (max(ground_z(v['x'] + s_ * 1.35 * math.cos(a) - q * math.sin(a), v['y'] + s_ * 1.35 * math.sin(a) + q * math.cos(a)) for q in (-0.8, 0.8)) for s_ in (1, -1))
        M = Matrix.Translation((v['x'], v['y'], (zf + zr) / 2)) @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Rotation(-math.atan2(zf - zr, 2.7), 4, 'Y')
        if v['kind'] == 'car':
            vehicles.car(mb, M, rng.child('car', k), cond='worn', kind=v.get('car_kind', 'saloon'), colour=v.get('colour'))
    for k, v in enumerate(P.get('parked_vehicles', [])):
        if v['kind'] == 'container':   # a 40 ft box on its trailer; the map's x, y is the box's middle
            a = math.radians(v.get('heading_deg', 0))
            M = Matrix.Translation((v['x'] + 2.5 * math.cos(a), v['y'] + 2.5 * math.sin(a), ground_z(v['x'], v['y']))) @ Matrix.Rotation(a, 4, 'Z')
            vehicles.container_truck(mb, M, rng.child('container', k), cond='worn', loaded=True, box_col=v.get('colour'), tractor=v.get('tractor', False))
    for k, v in enumerate(P.get('parked_vehicles', [])):
        if v['kind'] == 'okada':
            a = math.radians(v.get('heading_deg', 0))
            vehicles.okada(mb, Matrix.Translation((v['x'], v['y'], ground_z(v['x'], v['y']))) @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Rotation(math.radians(v.get('lean_deg', 8)), 4, 'X'), rng.child('okada', k))
    for k, b in enumerate(P.get('bins', [])):
        props.bin_drum(mb, Matrix.Translation((b['x'], b['y'], b.get('z_m', ground_z(b['x'], b['y'])))), rng.child('bin', k), _hex(b.get('colour'), '#1f5fa8'))
    for k, f in enumerate(P.get('furniture', [])):   # benches, plastic chairs, a generator: where the map puts them
        M = Matrix.Translation((f['x'], f['y'], f.get('z_m', ground_z(f['x'], f['y'])))) @ Matrix.Rotation(math.radians(f.get('facing_deg', 0)), 4, 'Z')
        if f['kind'] == 'bench':
            props.bench(mb, M, f.get('length_m', 1.8), col=_hex(f.get('colour'), '#6b4f36') if f.get('colour') else None)
        elif f['kind'] == 'chair':
            props.chair(mb, M, _hex(f.get('colour'), '#f4f1ea'), 0.5)
        elif f['kind'] == 'generator':
            props.generator(mb, M, _hex(f.get('colour'), '#c62828'))
    for k, a in enumerate(P.get('awnings', [])):
        props.awning(mb, a['x0'], a['x1'], a['y'], a['z'], a.get('depth', 0.9), _hex(a.get('colour'), '#1f6fb8'), side=1 if a.get('out', 'north') == 'north' else -1)
    for k, pp in enumerate(P.get('pole_posters', [])):   # posters pasted round a pole, at head height
        pole = P['poles'][pp['pole']]
        r = rng.child('pp', k)
        for j in range(pp.get('n', 2)):
            ang = math.radians(pp.get('facing_deg', 90)) + r.between(-0.5, 0.5)
            z = pp.get('z', 1.7) + j * 0.5 * r.between(0.8, 1.2)
            m = Matrix.Translation((pole['x'] + math.cos(ang) * 0.16, pole['y'] + math.sin(ang) * 0.16, z)) @ Matrix.Rotation(ang, 4, 'Z')
            for zz, c in ((-0.15, r.pick(POSTER)), (0.05, '#efe9d8'), (0.2, r.pick(POSTER))):
                mb.box('cloth', m @ Matrix.Translation((0, 0, zz)), hex_rgb(c), 0.5, size=(0.004, 0.32, 0.15 if zz != 0.05 else 0.25))
    for k, hp in enumerate(P.get('heaps', [])):
        if hp['kind'] == 'rubbish':
            street.refuse_heap(mb, hp['x'], hp['y'], hp['r'], rng.child('heap', k))
        elif hp['kind'] == 'goods':   # a tumble of goods at a stall
            goods.heap(gmb, hp['x'], hp['y'], hp['r'], hp.get('z_m', 0.0) + ground_z(hp['x'], hp['y']), hp.get('goods_kinds', ['sacks']), rng.child('heap', k), hp.get('tarp_colour'), hard=hmb, cols=hp.get('goods_colours'))
    for k, p in enumerate(P.get('people', [])):
        M = Matrix.Translation((p['x'], p['y'], p.get('z_m', ground_z(p['x'], p['y'])))) @ Matrix.Rotation(math.radians(p.get('facing_deg', 0)), 4, 'Z')
        people.person(mb, M, rng.child('person', k), kind=p.get('kind'), h=p.get('h'), pose=p.get('walking'))
    goods.soft(gmb.to_object('goods', collection, mat))
    if hmb.faces:
        hmb.to_object('goods_hard', collection, mat)
    return mb.to_object('props', collection, master)


def build(spot, collection=None):
    """Everything on one spot's map record."""
    obs = [street_piece(s, collection) for s in spot.get('streets', [])]
    obs += [building(b, collection) for b in spot.get('buildings', [])]
    obs += [frontage(e, collection) for e in spot.get('frontage_edges', [])]
    obs.append(spot_props(spot.get('props', {}), collection))
    return obs
