"""The dense old town kit, driven by the map (decisions: "The map tells the kit what goes where").

Everything here reads one spot's map record (the fields of the old town kit list, KIT.md section 12, plus the ones the
first eye test found missing, now in KIT.md section 12 too) and puts exactly that there: a building's footprint, storeys,
roof, wall, balcony and shop fronts; each frontage edge's platform, wall and gate; the street piece; the props at their
spots. One ground truth (decisions, 22 Oct): every window, sheet, stain, sack and bump is a stored record of the map, and
the kit throws no dice. A record the kit needs and the map lacks is an error (core.MissingRecord), never a guess; a first
draft of a new spot's records comes from the draft desk (draft.py, legacy/blender/kit_draft.py).

Built on the shared parts (parts.walls, window, roof_pitched, roof_flat; zinc sheets; gutters; street poles and wires;
vehicles.car; parcels.tree; props; people). New here: the lean-to on timber posts, plank shutters, the plank stall, the
display cabinet and drinks fridge, the breeze-block screen, the steel balcony rail with loops, the plain rendered wall
with piers and the ribbed sheet-steel gate, the raised front platform, the street piece and a lattice mast.
"""
import math

import bpy
from mathutils import Matrix, Vector

from . import facade, goods, gutters, parts, people, props, roadbed, street, vehicles, wear as W, zinc
from .core import MeshBuilder, MissingRecord, at, ccw, edge_out, frame, hex_rgb, need, offset, prism, shade
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
    """A rectilinear footprint cut into rectangles along x (each a counter-clockwise quad), for pitched roofs. A plot
    turned to the street (a four-cornered footprint whose sides are not along x and y) keeps its quad whole."""
    if len(poly) == 4 and any(abs(poly[i][0] - poly[(i + 1) % 4][0]) > 1e-3 and abs(poly[i][1] - poly[(i + 1) % 4][1]) > 1e-3 for i in range(4)):
        return [[tuple(p) for p in poly]]
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
def plank_shutter(mb, F, u, w, h, col, wear, planks):
    """Timber plank doors across a lock-up: vertical boards, each its own shade, two ledges, a padlock hasp. planks: the
    shopfront's record, each board's [shade, wear offset]."""
    mb.face([F @ Vector((u - w / 2, 0.01, 0.05)), F @ Vector((u + w / 2, 0.01, 0.05)), F @ Vector((u + w / 2, 0.01, h)), F @ Vector((u - w / 2, 0.01, h))], 'paint', DARK, 0)
    n = len(planks)
    for i, (f, dw) in enumerate(planks):
        x = u - w / 2 + (i + 0.5) * w / n
        mb.box('wood', at(F, x, 0.04, h / 2 + 0.02), shade(col, f), min(1, wear + dw), size=(w / n - 0.012, 0.03, h - 0.04))
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


def leanto_frame(sp, side):
    """A lean-to's sheet: its corners (eave A-B out over the road, top C-D on the wall) and the zinc spec."""
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
    return A, B, C, D, spec


def leanto(mb, sp, side):
    """A zinc lean-to on timber posts: its high edge on the wall, the low edge out toward the road on a timber plate,
    posts every 2-3 m. sp: x0, x1, wall_y, depth, z_wall, z_front, sheet_colour, roof_state, edge_colour; and its records:
    sheets (the slope's sheets, zinc.slope), uprights (each post's x, lean and shade)."""
    s = 1 if side == 'left' else -1
    y_w, y_f = sp['wall_y'] + s * 0.05, sp['wall_y'] - s * sp['depth']
    x0, x1 = sp['x0'], sp['x1']
    over = 0.15
    A, B, C, D, spec = leanto_frame(sp, side)
    zinc.slope(mb, A, B, C, D, spec, need(sp, 'sheets', 'lean-to')[0])
    # the front plate and the posts under it
    zf = sp['z_front'] - 0.12
    parts.bar(mb, 'wood', (x0, y_f, zf), (x1, y_f, zf), 0.1, TIMBER, 0.7)
    if sp.get('edge_colour'):   # a painted edge board (the red trim on a white sheet)
        parts.bar(mb, 'paint', (x0, y_f - s * (over + 0.02), sp['z_front'] - 0.1), (x1, y_f - s * (over + 0.02), sp['z_front'] - 0.1), 0.08, _hex(sp['edge_colour']), 0.5)
    for p in need(sp, 'uprights', 'lean-to'):
        x = p['x']
        parts.bar(mb, 'wood', (x, y_f, sp.get('z_foot', 0.0)), (x + p['lean'], y_f, zf), 0.09, shade(TIMBER, p['shade']), 0.7)
        parts.bar(mb, 'wood', (x, y_f, zf), (x, y_w, sp['z_wall'] - 0.08), 0.07, TIMBER, 0.7)   # a rafter back to the wall


def plank_stall(mb, sp, gmb=None):
    """A plank stall against the road edge: a timber frame boarded on three sides, a plank shelf at table height, and a
    heap of sacks and bundles piled on its top. Its records: boards (each board's shade, per side), sacks (goods leaves),
    tarp_ph (the tarp's fold phases)."""
    x0, x1, y0, y1, h = sp['x0'], sp['x1'], sp['y0'], sp['y1'], sp['h']
    col = _hex(sp.get('colour'), '#5a3328')
    for x in (x0, x1):
        for y in (y0, y1):
            parts.bar(mb, 'wood', (x, y, 0.35), (x, y, h), 0.08, TIMBER, 0.8)
    # boards: the back and the two ends, a low front with the shelf over it
    boards = need(sp, 'boards', 'plank stall')
    for ((ax, ay), (bx, by), top), shades in zip((((x0, y1), (x1, y1), h), ((x0, y0), (x0, y1), h), ((x1, y0), (x1, y1), h), ((x0, y0), (x1, y0), 1.05)), boards):
        L = math.hypot(bx - ax, by - ay)
        n = len(shades)
        for k, f in enumerate(shades):
            z = 0.35 + (k + 0.5) * (top - 0.35) / n
            m = Matrix.Translation(((ax + bx) / 2, (ay + by) / 2, z)) @ Matrix.Rotation(math.atan2(by - ay, bx - ax), 4, 'Z')
            mb.box('wood', m, shade(col, f), 0.8, size=(L + 0.04, 0.03, (top - 0.35) / n - 0.015))
    mb.box('wood', Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, 1.08)), shade(col, 1.1), 0.8, size=(x1 - x0 + 0.1, y1 - y0 + 0.2, 0.05))
    mb.box('wood', Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, h)), shade(col, 0.9), 0.8, size=(x1 - x0 + 0.2, y1 - y0 + 0.2, 0.05))
    gmb = gmb or mb   # the soft goods (sacks, tarp) can go to their own smooth-shaded object
    if sp.get('goods') == 'sacks_on_top':   # sacks, foam and bundles in white, grey and cream, sagging over the edges
        goods.draw(gmb, need(sp, 'sacks', 'plank stall'))
        mb.box('cloth', Matrix.Translation((x1 + 0.05, (y0 + y1) / 2, h - 0.2)) @ Matrix.Rotation(-0.25, 4, 'Y'), hex_rgb('#d8d2c4'), 0.4, size=(0.9, y1 - y0 + 0.3, 0.05))
    if sp.get('tarp_colour'):   # a tarp thrown over the top, hanging down its road side
        goods.tarp(gmb, x0 - 0.15, x1 + 0.1, y0 - 0.12, y1, h + sp.get('tarp_z_m', 0.5), sp.get('tarp_drop_m', 1.0), _hex(sp['tarp_colour']), need(sp, 'tarp_ph', 'plank stall'), side=-1 if sp['y0'] > 0 else 1)


def cage_stall(mb, sp, gmb, hmb):
    """A cage stall: a timber frame on four posts, steel bars across its front and ends (the trader locks it at night),
    shelves inside with goods on them, a plank or zinc top. Its records: bars (each side's bar positions along it, from
    its start), goods (leaves on the floor and each shelf), top_shades (the top's boards)."""
    x0, x1, y0, y1, h = sp['x0'], sp['x1'], sp['y0'], sp['y1'], sp['h']
    left = sp.get('y0', 0) > 0
    yf, yb = (y0, y1) if left else (y1, y0)   # its front faces the street
    z0 = ground_z((x0 + x1) / 2, yf)
    wood = _hex(sp.get('colour'), '#5e4630')
    bar_c = _hex(sp.get('bar_colour'), '#2a2624')
    for x in (x0, x1):
        for y in (y0, y1):
            parts.bar(mb, 'wood', (x, y, z0), (x, y, z0 + h), 0.07, wood, 0.8)
    for z in (0.12, 0.75, h - 0.05):   # rails round the frame: foot, counter and head
        for (ax, ay), (bx, by) in (((x0, yf), (x1, yf)), ((x0, y0), (x0, y1)), ((x1, y0), (x1, y1)), ((x0, yb), (x1, yb))):
            parts.bar(mb, 'wood', (ax, ay, z0 + z), (bx, by, z0 + z), 0.05, shade(wood, 0.9), 0.8)
    mb.box('wood', Matrix.Translation(((x0 + x1) / 2, yb, z0 + h / 2)), shade(wood, 0.7), 0.8, size=(x1 - x0, 0.03, h))   # the back boards
    sides = {'front': ((x0, yf), (x1, yf)), 'start': ((x0, y0), (x0, y1)), 'end': ((x1, y0), (x1, y1))}
    for name, us in need(sp, 'bars', 'cage stall').items():
        (ax, ay), (bx, by) = sides[name]
        L = math.dist((ax, ay), (bx, by))
        for u in us:
            px, py = ax + (bx - ax) * u / L, ay + (by - ay) * u / L
            parts.bar(mb, 'steel', (px, py, z0 + 0.75), (px, py, z0 + h - 0.05), 0.018, bar_c, 0.9)
    for z in sp.get('shelves', []):   # plank shelves across the inside
        mb.box('wood', Matrix.Translation(((x0 + x1) / 2, (yb + (yf + yb) / 2) / 2, z0 + z)), shade(wood, 1.05), 0.8, size=(x1 - x0 - 0.1, abs(y1 - y0) * 0.5, 0.025))
    mb.box('wood', Matrix.Translation(((x0 + x1) / 2, (y0 + y1) / 2, z0 + 0.75)), shade(wood, 1.1), 0.8, size=(x1 - x0, abs(y1 - y0), 0.03))   # the counter
    for k, f in enumerate(need(sp, 'top_shades', 'cage stall')):   # the top: boards or sheets laid across, overhanging the front
        n = len(sp['top_shades'])
        xa = x0 - 0.1 + (x1 - x0 + 0.2) * (k + 0.5) / n
        mb.box('zinc' if sp.get('top') == 'zinc' else 'wood', Matrix.Translation((xa, (y0 + y1) / 2 + (-0.15 if left else 0.15), z0 + h + 0.03)),
               shade(_hex(sp.get('top_colour'), '#6a5040'), f), 0.85, size=((x1 - x0 + 0.2) / n - 0.01, abs(y1 - y0) + 0.35, 0.025))
    goods.draw(gmb, need(sp, 'goods', 'cage stall'), hard=hmb, dz=z0)


def glass_cabinet(mb, sp, hmb):
    """A trader's timber glass cabinet on legs by the road: a timber frame, glass on its front and ends, a boarded back,
    shelves of packets, bottles and tins seen through the glass, a top board. Its records: contents (each shelf's row)."""
    x, y, w, d, h, lh = sp['x'], sp['y'], sp['w'], sp['d'], sp['h'], sp.get('legs_h', 0.75)
    M = Matrix.Translation((x, y, ground_z(x, y))) @ Matrix.Rotation(math.radians(sp.get('facing_deg', 0)), 4, 'Z')   # its front looks along -y
    wood = _hex(sp.get('colour'), '#6a4a32')
    for sx in (-1, 1):
        for sy in (-1, 1):
            mb.box('wood', at(M, sx * (w / 2 - 0.03), sy * (d / 2 - 0.03), (lh + h) / 2), shade(wood, 0.9), 0.8, size=(0.05, 0.05, lh + h))
    for z in (lh, lh + h):
        mb.box('wood', at(M, 0, 0, z), wood, 0.8, size=(w + (0.08 if z > lh else 0.0), d + (0.08 if z > lh else 0.0), 0.04))
    mb.box('wood', at(M, 0, 0, lh * 0.3), shade(wood, 0.85), 0.8, size=(w - 0.06, 0.03, 0.04))   # a stretcher between the legs
    mb.box('wood', at(M, 0, d / 2 - 0.015, lh + h / 2), shade(wood, 0.6), 0.8, size=(w - 0.06, 0.02, h))   # the back
    mb.box('wood', at(M, 0, -d / 2 + 0.01, lh + h / 2), shade(wood, 0.85), 0.8, size=(0.035, 0.03, h))   # the doors' meeting stile
    contents = need(sp, 'contents', 'glass cabinet')
    n = len(contents)
    for r, items in enumerate(contents):
        zs = lh + 0.03 + r * h / n
        if r:
            mb.box('wood', at(M, 0, 0, zs - 0.015), shade(wood, 1.1), 0.8, size=(w - 0.06, d - 0.06, 0.02))
        u = -w / 2 + 0.06
        for it in items:
            c = hex_rgb(it['col'])
            if it['k'] == 'packet':
                hmb.box('plastic', at(M, u + it['w'] / 2, 0.0, zs + it['h'] / 2, rz=it['rz'][0]), c, 0.1, size=(it['w'], 0.04, it['h']))
                u += it['w'] + 0.01
            elif it['k'] == 'bottle':
                parts.cyl(hmb, 'plastic', at(M, u + 0.03, -0.02, zs), 0.028, min(0.18, h / n - 0.05), c, 0.1, seg=8)
                u += 0.07
            else:
                for k in range(2):
                    parts.cyl(hmb, 'steel', at(M, u + 0.04, 0.0, zs + k * 0.06), 0.035, 0.058, c, 0.2, seg=10)
                u += 0.09
    g = hex_rgb('#c9d6d6')
    for (ax, ay), (bx, by) in (((-w / 2, -d / 2), (w / 2, -d / 2)), ((-w / 2, -d / 2), (-w / 2, d / 2)), ((w / 2, d / 2), (w / 2, -d / 2))):
        mb.face([at(M, ax, ay, lh + 0.02).translation, at(M, bx, by, lh + 0.02).translation, at(M, bx, by, lh + h - 0.02).translation, at(M, ax, ay, lh + h - 0.02).translation], 'glass_clear', g, 0)


SNACKS = ['#c62828', '#f9a825', '#1f6fb8', '#2e9a46', '#e8e4dc', '#e07b20', '#6a1b9a', '#d81b60']


def display_cabinet(mb, M, shelves, w=0.9, d=0.45, h=0.6):
    """A glass display case on a table: an aluminium frame, clear glass, and on its floor and one shelf rows of packets
    (biscuits, sweets, sachets), bottles and tins, packed tight. shelves: its record, each shelf's items in a row from the
    left (k packet, with its w, h and each row's turn rz; bottle; tins), each with its col."""
    al = hex_rgb('#c8ccce')
    for sx in (-1, 1):
        for sy in (-1, 1):
            mb.box('steel', at(M, sx * w / 2, sy * d / 2, h / 2), al, 0.3, size=(0.025, 0.025, h))
    for z in (0.012, h):
        mb.box('steel', at(M, 0, 0, z), al, 0.3, size=(w + 0.02, d + 0.02, 0.025))
    mb.box('plastic', at(M, 0, 0, h * 0.5), hex_rgb('#e8e8e4'), 0.2, size=(w - 0.03, d - 0.03, 0.012))   # the shelf
    for z0, items in zip((0.025, h * 0.5 + 0.006), shelves):
        x = -w / 2 + 0.04
        for it in items:
            c = hex_rgb(it['col'])
            if it['k'] == 'packet':   # a packet stood up
                pw, ph = it['w'], it['h']
                for row, rz in zip((-1, 1), it['rz']):
                    mb.box('plastic', at(M, x + pw / 2, row * d * 0.2, z0 + ph / 2, rz=rz), c, 0.1, size=(pw, 0.035, ph))
                x += pw + 0.01
            elif it['k'] == 'bottle':   # a bottle
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


def drinks_fridge(mb, M, rec, h=1.3, col=None):
    """A drinks fridge with a glass door: the maker's colour on its body and a brand header, a poster on its side, and
    rows of bottles and cans on wire shelves, seen through the door. rec: its records (contents, each shelf's row of
    bottles and cans from the left with their col; side_posters, the two posters' colours)."""
    col = col or hex_rgb('#cfd3d6')
    W, D = 0.7, 0.65
    mb.box('plastic', at(M, 0, 0, h / 2), col, 0.4, size=(W, D, h))
    mb.box('plastic', at(M, 0, -D / 2 + 0.02, h / 2 + 0.06), hex_rgb('#dfe3e4'), 0.1, size=(W - 0.12, 0.03, h - 0.36))   # the lit inside
    for r, row in enumerate(need(rec, 'contents', 'drinks fridge')):
        z = 0.24 + r * (h - 0.42) / 4
        mb.box('steel', at(M, 0, -D / 2 + 0.06, z), hex_rgb('#9aa0a2'), 0.1, size=(W - 0.14, 0.12, 0.01))
        x = -W / 2 + 0.1
        for it in row:
            c = hex_rgb(it['col'])
            if it['k'] == 'bottle':   # a bottle
                parts.cyl(mb, 'plastic', at(M, x, -D / 2 + 0.07, z + 0.005), 0.028, 0.15, c, 0, seg=8)
                parts.cyl(mb, 'plastic', at(M, x, -D / 2 + 0.07, z + 0.155), 0.012, 0.04, c, 0, seg=6)
            else:   # a can
                parts.cyl(mb, 'steel', at(M, x, -D / 2 + 0.07, z + 0.005), 0.03, 0.11, c, 0.1, seg=8)
            x += 0.075
    mb.face([at(M, -W / 2 + 0.05, -D / 2 - 0.005, 0.16).translation, at(M, W / 2 - 0.05, -D / 2 - 0.005, 0.16).translation,
             at(M, W / 2 - 0.05, -D / 2 - 0.005, h - 0.2).translation, at(M, -W / 2 + 0.05, -D / 2 - 0.005, h - 0.2).translation], 'glass_clear', hex_rgb('#cfdcdc'), 0)
    mb.box('plastic', at(M, 0, -D / 2 - 0.01, h - 0.1), hex_rgb('#c62828'), 0, size=(W, 0.02, 0.16))   # the brand header
    mb.box('plastic', at(M, 0, -D / 2 - 0.022, h - 0.1), hex_rgb('#f4f1ea'), 0, size=(W * 0.45, 0.004, 0.06))
    for sx, pc in zip((-1, 1), need(rec, 'side_posters', 'drinks fridge')):   # posters stuck on its sides
        mb.box('paint', at(M, sx * (W / 2 + 0.003), 0, h * 0.55), hex_rgb(pc), 0.3, size=(0.004, D * 0.6, h * 0.4))
        mb.box('paint', at(M, sx * (W / 2 + 0.006), 0, h * 0.6), hex_rgb('#f4f1ea'), 0.3, size=(0.004, D * 0.4, h * 0.12))


def breeze_screen(mb, a, b, z0, z1, col, cells):
    """A breeze-block screen from a to b: a grid of hollow blocks, each with a round hole showing the dark behind.
    cells: its record, each block's shade, by column then row."""
    L = math.dist(a, b)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    nx, nz = len(cells), len(cells[0])
    cw, ch = L / nx, (z1 - z0) / nz
    base = Matrix.Translation((a[0], a[1], z0)) @ Matrix.Rotation(ang, 4, 'Z')
    for i in range(nx):
        for j in range(nz):
            c = shade(col, cells[i][j])
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


def plain_wall(mb, line, h, col, wear, bays, piers=(), mould=True, skip=None, blotch=0.3):
    """A rendered block wall along a polyline, unpainted grey: mould dark at the top and in patches, red earth up its foot,
    a cement patch or two. piers: points where a square pier stands. skip(x0, x1) -> True leaves a stretch out (a gate).
    blotch: how uneven the grey is. bays: its record, each 1.2 m bay's (in order, the skipped ones left out): blot, how
    its grey goes; patch [x, z] a cement patch or none; streaks, the black mould runs hanging from the coping (x, w, zb,
    dark, y per side); foot, the damp at its foot (four pieces' [left, right] heights); broken, where the render has come
    away to the block (w, h, x, z and per side its shade and the bites out of its edge)."""
    bays = iter(bays)
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
            bay = next(bays, None)
            if bay is None:
                raise MissingRecord('plain wall: fewer bay records than bays')
            blot = bay['blot']
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
            if bay['patch']:   # a cement patch, never painted
                x, z = bay['patch']
                for side in (-1, 1):
                    q = [m @ Vector((x, side * 0.104, z)), m @ Vector((x + 0.4, side * 0.104, z)), m @ Vector((x + 0.4, side * 0.104, z + 0.35)), m @ Vector((x, side * 0.104, z + 0.35))]
                    mb.face(q[::-1] if side > 0 else q, 'paint', W.CEMENT, wear)
            for st in bay['streaks']:   # black mould run down from the coping, tapering, fading out
                x, sw, zb = st['x'], st['w'], st['zb']
                dark = shade(W.GRIME, st['dark'])
                for side, dy in zip((-1, 1), st['y']):
                    y = side * (0.1035 + dy)
                    q = [m @ Vector((x - sw * 0.25, y, zb)), m @ Vector((x + sw * 0.25, y, zb)), m @ Vector((x + sw / 2, y, h)), m @ Vector((x - sw / 2, y, h))]
                    cq = [col, col, dark, dark]
                    mb.face(q[::-1] if side > 0 else q, 'paint', cq[::-1] if side > 0 else cq, wear)
            if bay['foot']:   # the damp at the foot: a dark band, its top ragged, fading up
                n_ = len(bay['foot'])
                for j, (za, zb_) in enumerate(bay['foot']):
                    xa, xb = -w / 2 + w * j / n_, -w / 2 + w * (j + 1) / n_
                    wet = shade(W.GRIME, 0.8)
                    for side in (-1, 1):
                        y = side * 0.1032
                        q = [m @ Vector((xa, y, 0.0)), m @ Vector((xb, y, 0.0)), m @ Vector((xb, y, zb_)), m @ Vector((xa, y, za))]
                        cq = [wet, wet, W.mix(col, wet, 0.25), W.mix(col, wet, 0.25)]
                        mb.face(q[::-1] if side > 0 else q, 'paint', cq[::-1] if side > 0 else cq, wear)
            br = bay['broken']
            if br:   # render come away: the sandcrete block and its mortar showing, ragged at the edge
                bw, bh, x, z = br['w'], br['h'], br['x'], br['z']
                for side, sd in zip((-1, 1), br['sides']):
                    y = side * 0.105
                    q = [m @ Vector((x - bw / 2, y, z)), m @ Vector((x + bw / 2, y, z)), m @ Vector((x + bw / 2, y, z + bh)), m @ Vector((x - bw / 2, y, z + bh))]
                    bc = shade(W.BLOCK, sd['shade'])
                    mb.face(q[::-1] if side > 0 else q, 'paint', bc, wear)
                    for ex, ez, ew, eh in sd['bites']:   # its ragged edge: bites of render gone further, here and there
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


def wall_marks(mb, y_at, wall, road_y=0.0):
    """What people put on a street wall, on its street face: pasted posters (a church crusade, a party, a funeral), some
    torn, and painted daubs (a phone number, POST NO BILL, a house's warning). The map gives each one's place along the
    wall and its look: wall.posters [{x, z, w, h, colours: its three printed bands, torn: its foot torn off, shades: each
    band's}], wall.daubs [{x, z, text, colour, size}]."""
    def F(x, z=0.0, off=0.0):
        y = y_at(x)
        out = 1 if road_y > y else -1
        f = frame((x, y + out * (0.104 + off), z), (1, 0) if out > 0 else (-1, 0), (0, out))
        if f.to_3x3().determinant() > 0:
            f = f @ Matrix.Scale(-1, 4, (1, 0, 0))
        return f
    for k, p in enumerate(wall.get('posters', [])):
        w, h = p.get('w', 0.6), p.get('h', 0.85)
        bands = [(0.0, 0.18), (0.18, 0.62), (0.62, 0.8), (0.8, 1.0)]
        c0, c2, c3 = need(p, 'colours', 'wall poster')
        cs = [hex_rgb(c0), hex_rgb('#efe9d8'), hex_rgb(c2), hex_rgb(c3)]
        torn = need(p, 'torn', 'wall poster')
        for (a_, b_), c, f in zip(bands, cs, need(p, 'shades', 'wall poster')):
            if torn and a_ < 0.1:
                continue   # its foot torn off
            mb.box('cloth', at(F(p['x']), 0, 0.002, p['z'] + h * (a_ + b_) / 2), shade(c, f), 0.5, size=(w, 0.003, h * (b_ - a_)))
        mb.box('skin', at(F(p['x']), -w * 0.18, 0.004, p['z'] + h * 0.4), hex_rgb('#4a2e1f'), 0.3, size=(w * 0.35, 0.003, h * 0.38))   # the face on it
    for k, d in enumerate(wall.get('daubs', [])):
        parts.text(mb, 'paint', at(F(d['x']), 0, 0.004, d['z']), d['text'], d.get('size', 0.16), _hex(d.get('colour'), '#1a1a1a'), max_w=d.get('w'), wobble=0.05)


def sheet_gate(mb, a, b, h, col, wear, leaves=2, wicket=True, number=None):
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
def mono_frame(b, poly, H):
    """A mono-pitch roof as a lean-to over the whole building (its sheet and posts drawn by leanto): the lean-to's fields
    and its side."""
    roof = b.get('roof', {})
    xs_, ys_ = [p[0] for p in poly], [p[1] for p in poly]
    left = b.get('side') == 'left'
    back, front = (max(ys_), min(ys_)) if left else (min(ys_), max(ys_))
    eave = roof.get('eave_depth_m', 1.0)
    tn = math.tan(math.radians(roof.get('pitch_deg', 8)))
    D = abs(back - front)
    sp_ = dict(x0=min(xs_) - 0.1, x1=max(xs_) + 0.1, wall_y=back, depth=D + eave, z_wall=H + tn * D, z_front=H - tn * eave,
               sheet_colour=roof.get('colour', '#6e4f40'), roof_state=roof.get('roof_state', 'rusty'), posts=roof.get('posts', 'timber'),
               z_foot=roof.get('post_foot_m', 0.0))
    return sp_, 'left' if left else 'right'


def building(b, collection=None):
    """One building from its record. Its look is the map's: the paint's blotch (wall_finish.blotch), each window spot
    (window_spots, with its height z), each AC box (ac_units), the shopfront planks, the breeze screen's blocks, the
    scaffold's members, every stain on every face (stains), the roof's sheets (roof.sheets, or a flat roof's slab_blotch)."""
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
    spec['blotch'] = need(wf, 'blotch', 'building ' + b['id'] + ' wall_finish')
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
        u = (xm - (A[0] + B[0]) / 2) / dx   # x along the street to the way along the face (the same on a face along x)
        w = (s['to_x'] - s['from_x']) / abs(dx)
        if s['door'] == 'plank_shutter':
            plank_shutter(mb, F, u, w, min(2.45, H - 0.5), _hex(s.get('colour'), '#6b3b2e'), 0.7, need(s, 'planks', 'plank shutter'))
        elif s['door'] == 'roll_up':
            parts.roller_shutter(mb, F, u, w, dict(col=_hex(s.get('colour'), '#9aa3a8'), open=s.get('open', 0.7), wear=0.6))
        else:
            dark_opening(mb, F, u, w, min(2.3, H - 0.5), shade(_hex(s.get('frame_colour'), '#5a3a2a'), 1.0), 0.6)

    # windows: where the map puts them, each spot on a face at its height
    wtype = b.get('windows', 'louvre_glass')
    spots = need(b, 'window_spots', 'building ' + b['id'])
    win = dict(type='louvre' if wtype.startswith('louvre') else ('casement' if wtype == 'casement' else 'sliding'), w=1.0, h=1.15,
               frame=trim, glass=hex_rgb('#26323a'), mullion=hex_rgb('#b8bcc0'), bars=b.get('window_bars', 'none'), bar_col=_hex(b.get('bar_colour'), '#262626'), wear=wear, hood=False)
    shut = _hex(b['window_shutters']) if b.get('window_shutters') else None

    def put_window(F, u, z, sp=None):
        if sp and sp.get('kind'):   # this window's own record (the facade pass): its kind, size, bars, cloth
            facade.window(mb, F, u, z, sp, win, wear)
            if shut and sp['kind'] not in ('boarded', 'dark'):
                for s_ in (-1, 1):
                    mb.box('wood', at(F, u + s_ * (sp.get('w', win['w']) / 2 + 0.28), 0.05, z), shut, wear, size=(0.5, 0.03, sp.get('h', win['h'])))
        elif wtype in ('plank_shutter', 'louvre_timber'):
            plank_window(mb, F, u, z, 0.9, 1.1, _hex(b.get('shutter_colour'), '#6b4a33'), wear)
        else:
            parts.window(mb, F, u, z, win)
            if shut:   # side shutters standing open
                for s_ in (-1, 1):
                    mb.box('wood', at(F, u + s_ * (win['w'] / 2 + 0.28), 0.05, z), shut, wear, size=(0.5, 0.03, win['h']))

    bal_runs = b.get('balcony', {}).get('runs', [])
    gf_runs = (b.get('ground_floor_front') or {}).get('runs', [])
    for sp in spots:
        hit = _on_face(fs, sp['x'], sp['y'])
        if hit:
            k, u, _ = hit
            put_window(fs[k][4], u + sp.get('du', 0.0), need(sp, 'z', 'window spot'), sp)
    acs = need(b, 'ac_units', 'building ' + b['id'])
    if not isinstance(acs, list):
        raise MissingRecord('building %s: ac_units must be a list of AC boxes (x, y, z, shade, pipe)' % b['id'])
    for a_ in acs:   # a split unit's outdoor box on the wall, on two brackets, its pipe run down the wall
        A, B, L, n, F = fs[need(a_, 'face', 'AC box')]   # the face it is fixed to, and how far along it from its middle
        u = (a_['x'] - A[0]) * (B[0] - A[0]) / L + (a_['y'] - A[1]) * (B[1] - A[1]) / L - L / 2
        z = a_['z']
        c_ = shade(hex_rgb('#dcdcd6'), a_['shade'])
        mb.box('paint', at(F, u, 0.18, z), c_, 0.6, size=(0.8, 0.3, 0.55))
        mb.box('paint', at(F, u, 0.33, z), shade(c_, 0.45), 0.6, size=(0.42, 0.01, 0.42))   # the fan grille
        du, zt, zf = a_['pipe']
        parts.bar(mb, 'steel', F @ Vector((u + du, 0.04, zt)), F @ Vector((u + du, 0.04, zf)), 0.025, hex_rgb('#e6e4dc'), 0.4)

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
            breeze_screen(mb, a2, b2, 0.0, run.get('h', sh[0] - 0.05), _hex(run.get('colour'), '#b9bcbc'), need(run, 'cells', 'breeze screen'))

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
    if sc:   # its members as the map has them: tubes (a, b, radius, shade) and boards (planks on the lifts)
        tube = _hex(sc.get('colour'), '#8a5a3a')
        for ax, ay, az, bx, by, bz, r, f in need(sc, 'tubes', 'scaffold'):
            parts.bar(mb, 'steel', Vector((ax, ay, az)), Vector((bx, by, bz)), r, shade(tube, f) if f != 1.0 else tube, 0.7)
        for pk in need(sc, 'boards', 'scaffold'):
            mb.box('wood', fs[pk['face']][4] @ Matrix.Translation((pk['u'], pk['o'], pk['z'])), shade(TIMBER, pk['shade']), 0.8, size=(pk['len'], pk['depth'], 0.04))

    # stains: rain run down from the eaves and the sills, cement patches, render broken off at the foot (wear.age_face)
    for m in (need(b, 'stains', 'building ' + b['id']) if wf.get('stains', 'none') != 'none' else []):
        W.marks(mb, fs[m['face']][4], wx, [m])

    if b.get('facade'):   # the walk-up's close-up layer: slab edges, add-on rooms, closed balconies, pipes, wires, signs, laundry, tanks, tarps
        facade.draw(mb, fs, wx, b['facade'], wear)

    # roof
    if flat:
        spec['parapet']['slab_blotch'] = need(roof, 'slab_blotch', 'flat roof of ' + b['id'])
        parts.roof_flat(mb, poly, H, spec['parapet'])
    elif roof.get('form') == 'mono':
        xs_, ys_ = [p[0] for p in poly], [p[1] for p in poly]
        left = b.get('side') == 'left'
        back, front = (max(ys_), min(ys_)) if left else (min(ys_), max(ys_))
        tn = math.tan(math.radians(roof.get('pitch_deg', 8)))
        D = abs(back - front)
        sp_, side = mono_frame(b, poly, H)
        sp_['sheets'], sp_['uprights'] = need(roof, 'sheets', 'mono roof of ' + b['id']), need(roof, 'uprights', 'mono roof of ' + b['id'])
        rmb = MeshBuilder()   # its own object so the zinc slot can carry the roof's surface
        leanto(rmb, sp_, side)
        surfaced(rmb, {'zinc': roof.get('surface')}).to_object(b['id'] + '_roof', collection, mat)
        for x in (min(xs_), max(xs_)):   # the gable ends filled up to the sheet
            mb.face([(x, front, H), (x, back, H), (x, back, H + tn * D)][::1 if (x == min(xs_)) == left else -1], 'paint', paint, wear)
    else:
        longspan = rtype == 'longspan'
        state = roof.get('roof_state', 'rusty')
        col = _hex(roof.get('colour'), '#6e4f40')
        rw = STATE_WEAR.get(state, 0.7)
        sheets = need(roof, 'sheets', 'roof of ' + b['id'])
        qs = rects(poly)
        if len(sheets) != len(qs):
            raise MissingRecord('roof of %s: %d sheet records for %d roof parts' % (b['id'], len(sheets), len(qs)))
        for q, rec in zip(qs, sheets):
            rs = dict(form=roof.get('form', 'hip'), pitch_deg=roof.get('pitch_deg', 15), overhang=roof.get('eave_depth_m', 0.6),
                      profile='trapezoid' if longspan else 'sine', pitch=0.2 if longspan else 0.076, depth=0.032 if longspan else 0.018,
                      col=col, col2=shade(col, 0.88), mixed=state == 'rusty', wear=rw, wall_wear=wear, gable_col=paint,
                      fascia=_hex(roof.get('fascia_colour'), '#5a3a2a'), fascia_wood=roof.get('fascia') == 'timber')
            r = parts.roof_pitched(mb, ccw(q), H, rs, rec=rec)
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
    """One frontage edge from its record: a platform with the chips out of its front edge (chips: x, width), or a plain
    wall with its bays' records, its posters and its gate."""
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
        for x, cw in need(e, 'chips', 'frontage ' + e['id']):
            mb.box('concrete', Matrix.Translation((x, y_front - s * 0.01, h - 0.06)), shade(pc, 0.55), 0.9, size=(cw, 0.03, 0.1))
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
        plain_wall(mb, line, wall.get('h', 2.2), _hex(wall.get('wall_colour'), '#8e8d87'), 0.85 if wall.get('state') == 'mouldy' else 0.5, need(wall, 'bays', 'wall of ' + e['id']),
                   piers=piers, skip=skip, blotch=wall.get('blotch', 0.3))
        wall_marks(mb, y_at, wall)
        if g:
            a, b = (gx0, y_at(gx0)), (gx1, y_at(gx1))
            if s < 0:   # the gate's face toward the street
                a, b = b, a
            sheet_gate(mb, a, b, g.get('h', 2.0), _hex(g.get('colour'), '#6f757a'), g.get('wear', 0.6), leaves=g.get('leaves', 2), wicket=g.get('wicket', False), number=g.get('house_number'))
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


def street_piece(sp, collection=None, extent=(-40, 220, -60, 60), base_dir='.'):
    """A street piece from its record: the ground sheet from its ground grids (or tar strips with their frayed edges,
    tar_strips and sand_edges), its litter pieces, the apron's slabs (verge_right.shades), the gutter's pieces and the
    crossing slabs (rz, shade). base_dir: where the map is (its ground grid files lie beside it)."""
    mb = MeshBuilder()
    (x0, cy), (x1, _) = sp['centreline'][0], sp['centreline'][-1]
    w = sp['width_m']
    yl, yr = cy + w / 2, cy - w / 2
    X0, X1, Y0, Y1 = extent
    G = None
    if sp.get('relief') or 'tar_cover' in sp:   # the ground as real geometry, humps, dips, potholes and patches (roadbed.py)
        zb = -0.08 - 2 * (sp.get('relief') or {}).get('amp_m', 0.0)   # under the sheet's deepest dips
        beyond = _hex((sp.get('ground_colours') or {}).get('beyond'), '#7a5a44')   # the ground past the sheet's band
        mb.face([(X0, Y0, zb), (X1, Y0, zb), (X1, Y1, zb), (X0, Y1, zb)], 'mud', beyond, 0.1)
        own = (lambda n: master(n)) if not GROUNDS else (lambda n: master(n).copy())   # each further street its own layers
        _, G = roadbed.build(sp, roadbed.grids(sp, base_dir), collection, materials=own)
        GROUNDS.append(G)
    else:   # the ground everywhere (earth), then the tar laid on it in strips so its edge can fray into the earth
        tar = hex_rgb('#665e57')
        mb.face([(X0, Y0, -0.02), (X1, Y0, -0.02), (X1, Y1, -0.02), (X0, Y1, -0.02)], 'mud', hex_rgb('#8a8174'), 0.1)
        step = 2.0
        strips = need(sp, 'tar_strips', 'street ' + sp['id'])
        for k, (fa, fb, ga, gb, f) in enumerate(strips):   # the frayed edges: left [a, b], right [a, b], and its shade
            xa, xb = x0 + k * step, x0 + (k + 1) * step
            mb.face([(xa, yr + ga, 0.0), (xb, yr + gb, 0.0), (xb, yl + fb, 0.0), (xa, yl + fa, 0.0)], 'asphalt', shade(tar, f), 0.5)
        if sp.get('sand_cover') == 'edges':   # dust and sand blown onto the tar edges, fading out onto the tar
            sand, dust = hex_rgb('#8a8276'), shade(tar, 1.05)
            for k, wds in enumerate(need(sp, 'sand_edges', 'street ' + sp['id'])):
                xa, xb = x0 + k * step, x0 + (k + 1) * step
                for (y_e, s), wd in zip(((yl, -1), (yr, 1)), wds):
                    mb.face([(xa, y_e, 0.004), (xb, y_e, 0.004), (xb, y_e + s * wd, 0.004), (xa, y_e + s * wd, 0.004)][::s], 'mud', [sand, sand, dust, dust][::s], 0.1)
    gz = (lambda x, y: float(G.height(x, y))) if G else (lambda x, y: 0.0)
    lt = sp.get('litter') or {}
    if lt and G is not None:   # litter spread thin, gathered at the walls and in the ruts: each piece where the map has it
        dust = (sp.get('ground_colours') or {}).get('dust') or roadbed.COLOURS['dust']
        srgb = lambda h: [int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
        for lp in need(lt, 'pieces', 'litter of ' + sp['id']):
            if lp.get('dust'):   # street dust settled on it: its colour drawn toward the ground's
                c, d = srgb(lp['col']), lp['dust']
                lp = dict(lp, col='#%02x%02x%02x' % tuple(round(a * (1 - d) + b * d) for a, b in zip(c, srgb(dust))))
            street.litter_piece(mb, lp['x'], lp['y'], gz(lp['x'], lp['y']) + 0.004 - 0.02 * lp.get('buried', 0.0), lp)
    for vk, s_ in (('verge_right', -1), ('verge_left', 1)):   # a concrete apron along the road's edge, either side
        vr = sp.get(vk) or {}
        if vr.get('surface') != 'concrete_apron':
            continue
        xa, xb = vr.get('from_x', x0), vr.get('upto_x', x1)
        y0_, y1_ = (yr - vr['width'] - 0.4, yr + 0.05) if s_ < 0 else (yl - 0.05, yl + vr['width'] + 0.4)
        shades = need(vr, 'shades', 'apron of ' + sp['id'])
        n_ = len(shades)   # in short pieces laid on the ground, cracked at the joints
        for k, f in enumerate(shades):
            a_, b_ = xa + (xb - xa) * k / n_, xa + (xb - xa) * (k + 1) / n_ - 0.015
            z = [gz(a_, y0_) + 0.035, gz(b_, y0_) + 0.035, gz(b_, y1_) + 0.035, gz(a_, y1_) + 0.035]
            mb.face([(a_, y0_, z[0]), (b_, y0_, z[1]), (b_, y1_, z[2]), (a_, y1_, z[3])], 'concrete', shade(_hex(vr.get('colour'), '#8f8b83'), f), 0.4)
    for vk, s_ in (('verge_right', -1), ('verge_left', 1)):   # a grass strip behind the road's edge (or its kerb), in pieces
        vr = sp.get(vk) or {}
        if vr.get('surface') != 'grass':
            continue
        xa = vr.get('from_x', x0)
        kb = sp.get('kerb_right' if s_ < 0 else 'kerb_left') or {}
        y_in = (yr if s_ < 0 else yl) + s_ * (kb.get('w_m', 0.0) + vr.get('gap_m', 0.0))
        col = _hex(need(vr, 'colour', 'grass verge of ' + sp['id']))
        for ln, f, a_in, a_out in need(vr, 'patches', 'grass verge of ' + sp['id']):
            ya, yb = y_in + s_ * a_in, y_in + s_ * (vr['width'] - a_out)
            q = [(xa, ya), (xa + ln, ya), (xa + ln, yb), (xa, yb)]
            mb.face([(px, py, gz(px, py) + 0.03) for px, py in (q if s_ > 0 else q[::-1])], 'ground', shade(col, f), 0.2)
            xa += ln
    for side, s_ in (('right', -1), ('left', 1)):   # a raised kerb along the road's edge: precast blocks, their face toward the road
        kb = sp.get('kerb_' + side)
        if not kb:
            if (sp.get('kerb') or {}).get(side, 'none') != 'none':
                raise MissingRecord(f"street {sp['id']}: kerb {side} is {sp['kerb'][side]} but has no kerb_{side} record")
            continue
        y_e = (yr if s_ < 0 else yl) + s_ * kb.get('w_m', 0.15) / 2
        top, face = _hex(need(kb, 'colour', 'kerb')), _hex(kb['face_colour']) if kb.get('face_colour') else None
        xa = kb.get('from_x', x0)
        for ln, f, chip in need(kb, 'blocks', 'kerb ' + side + ' of ' + sp['id']):
            z = gz(xa + ln / 2, y_e)
            M = Matrix.Translation((xa + ln / 2, y_e, z + kb.get('h_m', 0.2) / 2 - 0.05))
            mb.box('concrete', M, shade(top, f), 0.5, size=(ln - 0.012, kb.get('w_m', 0.15), kb.get('h_m', 0.2) + 0.1))
            if face:   # the road face darker (tyre and splash): a thin skin on it
                mb.face([(xa, y_e - s_ * (kb.get('w_m', 0.15) / 2 + 0.003), z - 0.05), (xa + ln - 0.012, y_e - s_ * (kb.get('w_m', 0.15) / 2 + 0.003), z - 0.05),
                         (xa + ln - 0.012, y_e - s_ * (kb.get('w_m', 0.15) / 2 + 0.003), z + kb.get('h_m', 0.2) * 0.85),
                         (xa, y_e - s_ * (kb.get('w_m', 0.15) / 2 + 0.003), z + kb.get('h_m', 0.2) * 0.85)][::s_], 'concrete', shade(face, f), 0.6)
            if chip:   # a chip off the road-side top edge
                mb.box('concrete', Matrix.Translation((xa + ln * chip, y_e - s_ * kb.get('w_m', 0.15) * 0.35, z + kb.get('h_m', 0.2) - 0.03)), shade(top, 0.6), 0.8, size=(0.12, kb.get('w_m', 0.15) * 0.32, 0.07))
            xa += ln
    md = sp.get('median_wall')
    if md:
        median_wall(mb, md, gz, sp['id'])
    elif sp.get('median', 'none') != 'none':
        raise MissingRecord(f"street {sp['id']}: median is {sp['median']} but has no median_wall record")
    g = sp.get('gutter_left') or {}
    if g.get('type', 'none') != 'none':
        y = cy + g['offset_m']
        gutters.gutter(mb, [(x0, y), (x1, y)], dict(id=sp['id'] + 'L', w=g['width'], depth=g.get('depth', 0.5), state='covered' if g['type'] == 'slab_covered' else 'open',
                                                    blocked=[{'from': 0, 'to': 999, 'fill': 'rubbish'}] if g.get('state') == 'half_blocked' else [],
                                                    pieces=need(g, 'pieces', 'gutter of ' + sp['id']),
                                                    **{k: g[k] for k in ('slab_colour', 'dust', 'open_share', 'broken', 'rock', 'litter', 'proud_m') if k in g}),
                       lambda p: True, wear=g.get('wear', 0.2))
        for c in sp.get('crossings', []):
            if c.get('side') == 'left':
                mb.box('concrete', Matrix.Translation((c['x'], y, 0.27)) @ Matrix.Rotation(need(c, 'rz', 'crossing'), 4, 'Z'), shade(_hex(g.get('slab_colour'), '#a39f95'), need(c, 'shade', 'crossing')), 0.7, size=(c['w'], g['width'] + 0.7, 0.1))
    return mb.to_object(sp['id'], collection, master)


def median_wall(mb, md, gz, sid):
    """A low cast-concrete median along the street, from its record: y_m (its middle line), w_m, h_m, chamfer_m (the top
    edges cut off), colour (the faces), top_colour (the grimed top), foot_colour and foot_h_m (the dirt splashed up its
    feet), from_x, upto_x; drafted blocks [[length, shade, chip, crack]]: each cast length, its shade, a chip off its near
    top edge (0 = none, else where along it) and a dark crack at its joint (0..1)."""
    w, h, c = need(md, 'w_m', 'median'), need(md, 'h_m', 'median'), md.get('chamfer_m', 0.0)
    y0, y1 = md['y_m'] - w / 2, md['y_m'] + w / 2
    prof = [(y0, 0.0), (y0, h - c), (y0 + c, h), (y1 - c, h), (y1, h - c), (y1, 0.0)]
    face, top = _hex(need(md, 'colour', 'median')), _hex(md.get('top_colour') or md['colour'])
    foot, fh = _hex(md.get('foot_colour') or md['colour']), md.get('foot_h_m', 0.0)
    xa = md['from_x']
    for ln, f, chip, crack in need(md, 'blocks', 'median of ' + sid):
        xb = xa + ln - 0.01
        z = gz(xa + ln / 2, md['y_m']) - 0.06   # sunk a little into the ground, so no gap shows under it on a hump
        P = lambda x, p: (x, p[0], z + p[1] + (0.06 if p[1] > 0 else 0.0))
        for k in range(len(prof) - 1):   # the faces round its profile, near foot to far foot
            p, q = prof[k], prof[k + 1]
            col = top if p[1] >= h - c - 1e-6 and q[1] >= h - c - 1e-6 else face
            mb.face([P(xa, p), P(xb, p), P(xb, q), P(xa, q)], 'concrete', shade(col, f), 0.55)
        mb.face([P(xa, p) for p in prof], 'concrete', shade(face, f * 0.9), 0.55)
        mb.face([P(xb, p) for p in prof[::-1]], 'concrete', shade(face, f * 0.9), 0.55)
        for yy, s_ in ((y0, -1), (y1, 1)):   # the dirt thrown up its feet: a thin skin on each long face
            if fh > 0:
                mb.face([(xa, yy + s_ * 0.004, z), (xb, yy + s_ * 0.004, z), (xb, yy + s_ * 0.004, z + 0.06 + fh), (xa, yy + s_ * 0.004, z + 0.06 + fh)][::-s_],
                        'concrete', shade(foot, f), 0.7)
        if chip:   # a bite off the near top edge
            mb.box('concrete', Matrix.Translation((xa + ln * chip, y0 + 0.04, z + 0.06 + h - 0.05)), shade(face, f * 0.7), 0.8, size=(0.25, 0.1, 0.12))
        if crack:   # the joint at its end, a dark gap down its near face
            mb.face([(xb + 0.004, y0 - 0.005, z), (xb + 0.004 + 0.03 * crack, y0 - 0.005, z), (xb + 0.004 + 0.03 * crack, y0 - 0.005, z + 0.06 + h),
                     (xb + 0.004, y0 - 0.005, z + 0.06 + h)], 'concrete', shade(face, 0.35), 0.8)
        xa += ln
    for x, sw, sh, dk in md.get('streaks', []):   # grime run down the near face from its top: x, width, how far down, how dark
        z = gz(x, md['y_m']) - 0.06
        zt = z + 0.06 + h - c
        mb.face([(x - sw / 2, y0 - 0.006, zt - sh), (x + sw / 2, y0 - 0.006, zt - sh * 0.7), (x + sw / 2, y0 - 0.006, zt), (x - sw / 2, y0 - 0.006, zt)],
                'concrete', [shade(face, 1 - dk * 0.5), shade(face, 1 - dk * 0.5), shade(face, 1 - dk), shade(face, 1 - dk)], 0.7)
    dr = md.get('drift')
    if dr:   # sand and dust banked against its near foot: per point along it, how high (h_m share) and how far out (w_m share)
        col = _hex(need(dr, 'colour', 'median drift'))
        pts = need(dr, 'points', 'median drift')
        for (xa_, ha, wa), (xb_, hb, wb) in zip(pts, pts[1:]):
            za, zb = gz(xa_, y0 - 0.1), gz(xb_, y0 - 0.1)
            mb.face([(xa_, y0 - 0.002, za + dr['h_m'] * ha), (xa_, y0 - dr['w_m'] * wa, za - 0.02), (xb_, y0 - dr['w_m'] * wb, zb - 0.02), (xb_, y0 - 0.002, zb + dr['h_m'] * hb)],
                    'mud', [shade(col, 1.06), shade(col, 0.95), shade(col, 0.95), shade(col, 1.06)], 0.3)


def street_lamp(mb, lp):
    """A steel street lamp from its record: x, y, h (m), arm_m (how far the arm reaches), facing_deg (the arm's way), colour."""
    if need(lp, 'type', 'lamp') != 'steel_arm':
        raise MissingRecord(f"lamp type {lp['type']} has no part")
    x, y, h = lp['x'], lp['y'], need(lp, 'h', 'lamp')
    col, a = _hex(lp.get('colour'), '#8a8c8c'), math.radians(need(lp, 'facing_deg', 'lamp'))
    z0 = ground_z(x, y)
    parts.cyl(mb, 'steel', Matrix.Translation((x, y, z0)), 0.09, h, col, 0.4, seg=10, r2=0.06)
    d = Vector((math.cos(a), math.sin(a), 0))
    top, end = Vector((x, y, z0 + h)), Vector((x, y, z0 + h)) + d * need(lp, 'arm_m', 'lamp') + Vector((0, 0, 0.35))
    parts.bar(mb, 'steel', top - Vector((0, 0, 0.6)), end, 0.05, col, 0.4)
    mb.box('steel', Matrix.Translation(end + d * 0.25 - Vector((0, 0, 0.05))) @ Matrix.Rotation(a, 4, 'Z'), shade(col, 0.8), 0.4, size=(0.6, 0.25, 0.12))


def sand_heap(mb, x, y, r, h, col):
    """A sand heap: a smooth mound r across its foot and h high, sitting on the ground at x, y, its foot a shade darker."""
    z0 = ground_z(x, y)
    rings, seg = 5, 18
    pts = []
    for i in range(rings + 1):
        t = i / rings
        rr = r * (1 - t ** 1.6)
        zz = z0 - 0.03 + h * (1 - (1 - t) ** 2) if i < rings else z0 + h
        pts.append([(x + rr * math.cos(a * math.tau / seg), y + rr * math.sin(a * math.tau / seg), zz) for a in range(seg)])
    for i in range(rings):
        c = shade(col, 0.86 + 0.14 * i / rings)
        for a in range(seg):
            b = (a + 1) % seg
            mb.face([pts[i][a], pts[i][b], pts[i + 1][b], pts[i + 1][a]], 'mud', c, 0.3)


# ---------------------------------------------------------------- props at their spots
def spot_props(P, collection=None):
    """The props at their spots, each from its record: a pole's lean and arm, a tree's form, a trade spot's sheets, posts,
    goods and contents, a vehicle's colours, a bin's litter, a heap's own shape or goods, a pole poster's sheets, each
    person's body (KIT.md section 12)."""
    mb = MeshBuilder()
    gmb = MeshBuilder()   # goods and clutter, shaded smooth
    hmb = MeshBuilder()   # hard goods (crates, basins, cartons), flat shaded with crisp edges
    tops = []
    for k, p in enumerate(P.get('poles', [])):
        pts, top = street.pole(mb, p['x'], p['y'], p, h=p.get('h', 9.5), wood=p.get('type') == 'timber')
        tops.append(pts)
    for wspec in P.get('wires', []):
        a = tops[wspec['from_pole']]
        bs = tops[wspec['to_pole']] if 'to_pole' in wspec else [Vector(wspec['to_xyz']) + Vector((0, 0.4 * (i - 1), 0)) for i in range(3)]
        for i in range(wspec.get('n', 2)):
            street.wire(mb, a[i % 3], bs[i % 3], wspec.get('sag', 0.5))
    for m in P.get('masts', []):
        lattice_mast(mb, m['x'], m['y'], m['h'])
    for t in P.get('trees', []):
        tree(mb, t['x'], t['y'], need(t, 'form', 'tree'))
    for lp in P.get('lamps', []):   # a street lamp: a steel pole, an arm out over the road, a flat head
        street_lamp(mb, lp)
    for k, s in enumerate(P.get('trade_spots', [])):
        side = 'left' if s.get('y', s.get('wall_y', s.get('y0', 0))) > 0 else 'right'
        if s['type'] == 'lean-to row':
            if s.get('surface'):   # a sheet the map gave its own photo surface: its own object, so its zinc can differ
                lmb = MeshBuilder()
                leanto(lmb, s, side)
                surfaced(lmb, {'zinc': s['surface']}).to_object(f'leanto_{k}', collection, mat)
            else:
                leanto(mb, s, side)
            g0, h0 = len(gmb.cols), len(hmb.cols)
            goods.draw(gmb, need(s, 'goods', 'lean-to'), hard=hmb)   # along its wall
            goods.draw(gmb, need(s, 'hung', 'lean-to'))   # hung from its front plate
            goods.weather(gmb, g0, s.get('goods_tone', 1.0), s.get('goods_dust', 0.0))
            goods.weather(hmb, h0, s.get('goods_tone', 1.0), s.get('goods_dust', 0.0))
        elif s['type'] == 'umbrella':   # a market umbrella over a seller's spot
            z = ground_z(s['x'], s['y'])
            props.umbrella(mb, Matrix.Translation((s['x'], s['y'], z)) @ Matrix.Rotation(need(s, 'rz', 'umbrella'), 4, 'Z'), s.get('r', 1.1), s.get('h', 2.2), s.get('colours'))
            if s.get('goods_kinds'):   # its goods heaped at its foot, on the ground
                goods.draw(gmb, need(s, 'goods', 'umbrella'), hard=hmb, dz=z)
        elif s['type'] == 'kiosk' and s.get('kiosk_kind') == 'plank_stall':
            plank_stall(mb, s, gmb)
        elif s['type'] == 'kiosk' and s.get('kiosk_kind') == 'glass_cabinet':
            glass_cabinet(mb, s, hmb)
        elif s['type'] == 'cage stall':
            cage_stall(mb, s, gmb, hmb)
        elif s['type'] == 'kiosk' and s.get('kiosk_kind') == 'drinks_fridge':
            drinks_fridge(mb, Matrix.Translation((s['x'], s['y'], 0.3)) @ Matrix.Rotation(math.radians(s.get('facing_deg', 0)), 4, 'Z'), s, s.get('h', 1.3), _hex(s.get('colour'), '#cfd3d6'))
        elif s['type'] == 'table':
            M = Matrix.Translation((s['x'], s['y'], s.get('z_m', 0.3)))   # on the platform, unless the map gives its foot
            items = s.get('items', [])
            if any(i.startswith('crate') for i in items):   # a stack of crates on the platform, each at its own turn
                for j, (it, rz) in enumerate(zip(items, need(s, 'crate_rz', 'crate stack'))):
                    props.crate(mb, M @ Matrix.Translation((0, 0, j * 0.3)) @ Matrix.Rotation(rz, 4, 'Z'), _hex(it.split(':')[1]), 0.4)
                continue
            props.table(mb, M, s['w'], s['d'])
            for j, it in enumerate(items):
                u = (j - (len(items) - 1) / 2) * s['w'] / max(1, len(items))
                if it == 'display_cabinet':
                    display_cabinet(mb, M @ Matrix.Translation((u, 0, 0.8)), need(s, 'contents', 'table')[j], w=min(1.1, s['w'] / len(items) - 0.1))
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
            ck = v.get('car_kind', 'saloon')
            vehicles.car(mb, M, None, cond='worn', kind=ck, colour=need(v, 'colour', 'car'), bed_load=need(v, 'load', 'pickup') or False if ck == 'pickup' else True)
    for k, v in enumerate(P.get('parked_vehicles', [])):
        if v['kind'] == 'container':   # a 40 ft box on its trailer; the map's x, y is the box's middle
            a = math.radians(v.get('heading_deg', 0))
            M = Matrix.Translation((v['x'] + 2.5 * math.cos(a), v['y'] + 2.5 * math.sin(a), ground_z(v['x'], v['y']))) @ Matrix.Rotation(a, 4, 'Z')
            tractor = v.get('tractor', False)
            bonneted = v.get('tractor_kind', 'cab_over') == 'bonneted'
            vehicles.container_truck(mb, M, None, cond=v.get('condition', 'worn'), loaded=True, box_col=need(v, 'colour', 'container'), tractor=tractor,
                                     cab_col=need(v, 'cab_colour', 'container truck') if tractor else None, tractor_kind=v.get('tractor_kind', 'cab_over'),
                                     bonnet_col=need(v, 'bonnet_colour', 'bonneted tractor') if tractor and bonneted else None, glass=v.get('glass', 'whole'),
                                     trailer=v.get('trailer', 'skeletal'), trailer_col=v.get('trailer_colour'), stripes=v.get('stripes', True),
                                     box_marks=v.get('box_marks'), box_wear=v.get('box_wear'), rec=v)
    for k, v in enumerate(P.get('parked_vehicles', [])):
        if v['kind'] == 'okada':
            a = math.radians(v.get('heading_deg', 0))
            vehicles.okada(mb, Matrix.Translation((v['x'], v['y'], ground_z(v['x'], v['y']))) @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Rotation(math.radians(v.get('lean_deg', 8)), 4, 'X'), None, colour=need(v, 'colour', 'okada'))
    for k, b in enumerate(P.get('bins', [])):
        props.bin_drum(mb, Matrix.Translation((b['x'], b['y'], b.get('z_m', ground_z(b['x'], b['y'])))), need(b, 'litter', 'bin'), _hex(b.get('colour'), '#1f5fa8'))
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
        for j, sh_ in enumerate(need(pp, 'sheets', 'pole poster')):   # each sheet's turn round the pole, height and two colours
            ang = math.radians(pp.get('facing_deg', 90)) + sh_['turn']
            z = pp.get('z', 1.7) + j * 0.5 * sh_['z']
            m = Matrix.Translation((pole['x'] + math.cos(ang) * 0.16, pole['y'] + math.sin(ang) * 0.16, z)) @ Matrix.Rotation(ang, 4, 'Z')
            for zz, c in ((-0.15, sh_['colours'][0]), (0.05, '#efe9d8'), (0.2, sh_['colours'][1])):
                mb.box('cloth', m @ Matrix.Translation((0, 0, zz)), hex_rgb(c), 0.5, size=(0.004, 0.32, 0.15 if zz != 0.05 else 0.25))
    for k, hp in enumerate(P.get('heaps', [])):
        if hp['kind'] == 'rubbish':
            street.refuse_heap(mb, hp['x'], hp['y'], hp['r'], need(hp, 'heap', 'rubbish heap'))
        elif hp['kind'] == 'sand':   # a heap of sand tipped by the road: a low mound, its height and colour from the map
            sand_heap(mb, hp['x'], hp['y'], hp['r'], need(hp, 'h', 'sand heap'), _hex(need(hp, 'colour', 'sand heap')))
        elif hp['kind'] == 'blocks':   # a stack of hollow sandcrete blocks: cols along, rows deep, layers high
            a = math.radians(hp.get('facing_deg', 0))
            z0, col, j = ground_z(hp['x'], hp['y']), _hex(need(hp, 'colour', 'block stack')), 0
            for ly in range(hp['layers']):
                for rw in range(hp.get('rows', 1)):
                    for c in range(hp['cols']):
                        dx, dy, rz, f, gone = need(hp, 'blocks', 'block stack')[j]
                        j += 1
                        if gone:
                            continue
                        u, v = (c - (hp['cols'] - 1) / 2) * 0.46 + dx, (rw - (hp.get('rows', 1) - 1) / 2) * 0.23 + dy
                        M = Matrix.Translation((hp['x'] + u * math.cos(a) - v * math.sin(a), hp['y'] + u * math.sin(a) + v * math.cos(a), z0 + 0.1125 + ly * 0.225)) @ Matrix.Rotation(a + rz, 4, 'Z')
                        mb.box('block', M, shade(col, f), 0.6, size=(0.45, 0.225, 0.225))
        elif hp['kind'] == 'goods':   # a tumble of goods at a stall, on the ground
            goods.draw(gmb, need(hp, 'goods', 'goods heap'), hard=hmb, dz=ground_z(hp['x'], hp['y']))
    for k, p in enumerate(P.get('people', [])):
        M = Matrix.Translation((p['x'], p['y'], p.get('z_m', ground_z(p['x'], p['y'])))) @ Matrix.Rotation(math.radians(p.get('facing_deg', 0)), 4, 'Z')
        people.person(mb, M, need(p, 'body', 'person'))
    goods.soft(gmb.to_object('goods', collection, mat))
    if hmb.faces:
        hmb.to_object('goods_hard', collection, mat)
    return mb.to_object('props', collection, master)


def build(spot, collection=None):
    """Everything on one spot's map record. spot['_dir']: the folder the map is in (its ground grid files lie there)."""
    obs = [street_piece(s, collection, base_dir=spot.get('_dir', '.')) for s in spot.get('streets', [])]
    obs += [building(b, collection) for b in spot.get('buildings', [])]
    obs += [frontage(e, collection) for e in spot.get('frontage_edges', [])]
    obs.append(spot_props(spot.get('props', {}), collection))
    return obs
