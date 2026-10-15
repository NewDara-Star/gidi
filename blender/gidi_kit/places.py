"""Kinds built on the parametric block: civic, religious, commercial, housing types, leisure and
transport buildings. Each picks a style and colours from research-*.md and adds its signature parts.
All names on signs are invented (rule zero)."""
import math

from mathutils import Matrix, Vector

from . import parts
from .blocks import block, dome, faces, flagpole, minaret, perimeter
from .core import MeshBuilder, ccw, centroid, hex_rgb, offset, shade
from .kinds import _chair, container, footprint, T
from .materials import master
from .rules import C, CHARACTER


def _ch(a):
    return C[CHARACTER.get(a['district'], 'dense')]


def _poly(a):
    return ccw([tuple(p) for p in a['poly']])


def _done(mb, a, collection, spec=None):
    return mb.to_object(a.get('name', 'obj'), collection, master), spec or {}


def _wear(a, rng, bias=0.0):
    lo, hi = _ch(a)['wear']
    return max(0.0, min(1.0, rng.between(lo, hi) + bias))


# ---------------------------------------------------------------- worship
def mosque(a, rng, collection=None):
    """Green dome on a drum, one or two minarets, arched windows, white or cream walls, a fence.
    Size from the plot: neighbourhood (< 150 m2), Jumat, central (> 600 m2). research-religious 1-4."""
    poly = _poly(a)
    area = abs(sum(poly[i][0] * poly[(i + 1) % 4][1] - poly[(i + 1) % 4][0] * poly[i][1] for i in range(4))) / 2
    big = area > 600
    mb = MeshBuilder()
    wear = _wear(a, rng, -0.1)
    wall = hex_rgb(rng.pick({'#f4f2ea': 3, '#ede3c8': 2}))
    green = hex_rgb(rng.pick({'#1f7a3a': 5, '#4caf50': 2, '#6e9c6a': 2, '#2f6fa6': 1}))
    dome_col = hex_rgb(rng.pick({'#1f7a3a': 4, '#c9a13b': 2 if big else 0.5, '#b8bec4': 2, '#2f6fa6': 1}))
    inner = offset(poly, -1.5 if area > 120 else -0.6)
    H = block(mb, inner, 2 if big else 1, dict(style='govt', wall=wall, band=green, trim=green, wear=wear, floor_h=4.0, window='casement', win_h=2.0, fins=False, roof='parapet', entrance=True, door=green, facing=a.get('facing', 0)), rng)
    c = centroid(inner)
    r = min(math.dist(inner[0], inner[1]), math.dist(inner[1], inner[2])) * (0.32 if big else 0.3)
    parts.cyl(mb, 'paint', Matrix.Translation((c[0], c[1], H)), r * 1.02, r * 0.5, wall, wear, seg=20)
    for k in range(16):  # windows round the drum
        q = k / 16 * math.tau
        mb.box('glass', Matrix.Translation((c[0] + math.cos(q) * r * 1.03, c[1] + math.sin(q) * r * 1.03, H + r * 0.25)) @ Matrix.Rotation(q, 4, 'Z'), hex_rgb('#24343e'), 0, size=(0.03, r * 0.15, r * 0.25))
    dome(mb, c[0], c[1], H + r * 0.5, r, dome_col, wear * 0.5)
    n_min = 2 if big else rng.pick({0: 1, 1: 3, 2: 1})
    for k in range(n_min):
        p = inner[k * 2 % 4] if n_min == 2 else inner[0]
        minaret(mb, p[0], p[1], (30 if big else 14) * rng.between(0.85, 1.15), wall, green, dome_col, wear, rng)
    perimeter(mb, poly, dict(paint=wall, coping=green, gate=green, h=1.6, wear=wear), rng, a.get('facing', 0))
    if a.get('label'):
        i, L, F = faces(inner)[a.get('facing', 0)]
        parts.signboard(mb, F, 0, H - 0.6, min(L - 1, 7), 0.8, dict(text=a['label'].upper(), bg=green, fg=hex_rgb('#ffffff'), hand=False, wear=wear * 0.5))
    # ablution taps and kettles by the gate
    i, L, F = faces(poly)[a.get('facing', 0)]
    for k in range(5):
        parts.cyl(mb, 'plastic', parts.at(F, -L / 3 + k * 0.4, -1.0, 0), 0.08, 0.2, hex_rgb(rng.pick(['#2f6fae', '#2e7d4f', '#d9b23a'])), 0, seg=8, r2=0.05)
    return _done(mb, a, collection)


def church(a, rng, collection=None):
    """Picks the church type from the plot and district: warehouse church (portal shed, banner),
    parish hall with a belfry, white-garment church (white and blue), or an estate church with a
    glazed gable. research-religious 9-16."""
    poly = _poly(a)
    ch = CHARACTER.get(a['district'], 'dense')
    kind = rng.pick({'warehouse': 4 if ch in ('dense', 'sprawl', 'port') else 1, 'parish': 3 if ch in ('old_island', 'dense') else 1,
                     'white': 3 if ch in ('waterfront', 'dense', 'sprawl') else 0.3, 'estate': 4 if ch == 'elite' else 0.2})
    mb = MeshBuilder()
    wear = _wear(a, rng)
    name = (a.get('label') or rng.pick(['FIRE OF GRACE ASSEMBLY', 'LIVING WATERS CHAPEL', 'MOUNTAIN OF REFUGE', 'GLORY TABERNACLE'])).upper()
    inner = offset(poly, -1.0)
    fc = a.get('facing', 0)
    if kind == 'warehouse':
        H = block(mb, inner, 1, dict(style='shed', wall=hex_rgb('#c9c3b6'), band=hex_rgb('#8a857a'), wear=wear, floor_h=6.5, roof='gable', pitch=8, overhang=0.4, roof_col=hex_rgb(rng.pick(['#c3c7ca', '#2b5c9e', '#8a4b2a'])), facing=fc), rng)
        i, L, F = faces(inner)[fc]
        parts.signboard(mb, F, 0, 4.6, min(L - 0.6, 10), 1.6, dict(text=name, bg=hex_rgb(rng.pick(['#1f3f8a', '#8a1f2f', '#ffffff'])), fg=hex_rgb('#f2c21b'), hand=False, wear=wear * 0.3))
        mb.box('steel', parts.at(F, 0, 0.05, 1.6), hex_rgb('#2b4a66'), wear, size=(3.0, 0.06, 3.2))
    elif kind == 'parish':
        H = block(mb, inner, 1, dict(style='govt', wall=hex_rgb('#efe6d2'), band=hex_rgb('#8e3b2a'), trim=hex_rgb('#ffffff'), wear=wear, floor_h=6.0, window='casement', win_h=2.6, fins=False, roof='gable', pitch=30, roof_col=hex_rgb('#8e3b2a'), facing=fc), rng)
        i, L, F = faces(inner)[fc]
        bt = parts.at(F, 0, 1.0, 0)
        mb.box('paint', bt @ Matrix.Translation((0, 0, 6.5)), hex_rgb('#efe6d2'), wear, size=(2.6, 2.6, 13))
        parts.cyl(mb, 'zinc', bt @ Matrix.Translation((0, 0, 13)) @ Matrix.Rotation(math.pi / 4, 4, 'Z'), 1.9, 5.0, hex_rgb('#8e3b2a'), wear, seg=4, r2=0.05)
        mb.box('paint', bt @ Matrix.Translation((0, 0, 18.6)), hex_rgb('#ffffff'), 0, size=(0.12, 0.12, 1.2))
        mb.box('paint', bt @ Matrix.Translation((0, 0, 18.8)), hex_rgb('#ffffff'), 0, size=(0.7, 0.12, 0.12))
        parts.signboard(mb, F, 3.5, 2.6, 3.2, 0.8, dict(text=name, bg=hex_rgb('#ffffff'), fg=hex_rgb('#1f3f8a'), hand=False, wear=wear))
    elif kind == 'white':  # Aladura: white walls, blue trim, sand compound, a white cross
        mb.face([(p[0], p[1], 0.03) for p in poly], 'ground', hex_rgb('#e6dcc0'), 0.3)
        H = block(mb, inner, 1, dict(style='govt', wall=hex_rgb('#fafaf7'), band=hex_rgb('#2e64b8'), trim=hex_rgb('#2e64b8'), wear=wear * 0.7, floor_h=4.2, window='louvre', fins=False, roof='gable', pitch=16, roof_col=hex_rgb('#c3c7ca'), facing=fc), rng)
        i, L, F = faces(inner)[fc]
        parts.signboard(mb, F, 0, 3.8, min(L - 0.6, 6), 0.8, dict(text=name, bg=hex_rgb('#fafaf7'), fg=hex_rgb('#2e64b8'), hand=True, wear=wear, wobble=0.02))
        for k, (x, y) in enumerate([(-2, -2), (2, -2)]):
            mb.box('paint', parts.at(F, x, -2.0, 1.4), hex_rgb('#fafaf7'), 0.2, size=(0.15, 0.15, 2.8))
    else:  # estate church: modern hall, glazed gable, a slim steel cross
        H = block(mb, inner, 1, dict(style='govt', wall=hex_rgb('#f5f5f2'), band=hex_rgb('#3a3c3e'), trim=hex_rgb('#3a3c3e'), wear=0.1, floor_h=7.0, window='sliding', win_w=2.0, win_h=3.5, fins=False, roof='gable', pitch=25, roof_col=hex_rgb('#3a3c3e'), facing=fc), rng)
        i, L, F = faces(inner)[fc]
        mb.box('steel', parts.at(F, 0, 0.3, 11.0), hex_rgb('#c9ced2'), 0, size=(0.25, 0.25, 6.0))
        mb.box('steel', parts.at(F, 0, 0.3, 12.5), hex_rgb('#c9ced2'), 0, size=(2.2, 0.25, 0.25))
    # a banner across the gate and parked plastic chairs for the overflow
    i, L, F = faces(poly)[fc]
    if kind != 'estate':
        parts.bar(mb, 'steel', F @ Vector((-L / 2 + 0.3, -0.5, 0)), F @ Vector((-L / 2 + 0.3, -0.5, 3.4)), 0.06, hex_rgb('#8a8a8a'))
        parts.bar(mb, 'steel', F @ Vector((L / 2 - 0.3, -0.5, 0)), F @ Vector((L / 2 - 0.3, -0.5, 3.4)), 0.06, hex_rgb('#8a8a8a'))
        parts.signboard(mb, F, 0, 3.0, L - 1.0, 0.7, dict(text=rng.pick(['3 NIGHTS OF FIRE • CRUSADE', 'HOLY GHOST NIGHT • FRIDAY 10PM', 'THANKSGIVING SUNDAY • ALL WELCOME']), bg=hex_rgb(rng.pick(['#c8322b', '#1f3f8a', '#6a1b9a'])), fg=hex_rgb('#ffffff'), hand=False, wear=0.2))
    return _done(mb, a, collection)


# ---------------------------------------------------------------- schools and health
def school(a, rng, collection=None):
    """Public school: long verandah classroom blocks with a painted dado band and a name board,
    a sandy yard, a flagpole. Private/international in elite districts. research-leisure schools."""
    poly = _poly(a)
    ch = CHARACTER.get(a['district'], 'dense')
    mb = MeshBuilder()
    wear = _wear(a, rng, 0.05)
    elite = ch == 'elite'
    wall = hex_rgb('#f5f5f2' if elite else rng.pick(['#efe6c8', '#f2e2b0', '#e8eef0']))
    band = hex_rgb(rng.pick(['#2f6fae', '#2e7d4f', '#8a2f2f', '#c8a020']))
    fc = a.get('facing', 0)
    s = max(1, min(3, a.get('storeys', 2)))
    H = block(mb, poly, s, dict(style='govt', wall=wall, band=band, trim=band, wear=wear, floor_h=3.4, window='louvre' if not elite else 'sliding', fins=False, roof='hip' if not elite else 'parapet', roof_col=hex_rgb('#9aa3a8'), pitch=15, facing=fc, bars='grid'), rng)
    # the verandah: posts and a walkway along the street face, dado band painted
    i, L, F = faces(poly)[fc]
    for k in range(int(L / 3) + 1):
        u = -L / 2 + 0.2 + k * (L - 0.4) / max(1, int(L / 3))
        mb.box('paint', parts.at(F, u, 1.6, 1.6), band, wear, size=(0.25, 0.25, 3.2))
    mb.box('concrete', parts.at(F, 0, 0.9, 0.15), hex_rgb('#9c978c'), wear, size=(L, 1.8, 0.3))
    mb.box('concrete', parts.at(F, 0, 0.9, 3.25), hex_rgb('#c9c3b6'), wear, size=(L, 1.9, 0.12))
    name = (a.get('label') or rng.pick(['COMMUNITY PRIMARY SCHOOL', 'MODEL COLLEGE', 'GRACE NURSERY & PRIMARY'])).upper()
    parts.signboard(mb, F, 0, H - 0.5 if s > 1 else 2.7, min(L - 1, 9), 0.9, dict(text=name, bg=hex_rgb('#ffffff'), fg=band, hand=not elite, wear=wear, wobble=0.015 if not elite else None))
    c = centroid(poly)
    fp = F @ Vector((L / 2 + 2, -4, 0))
    flagpole(mb, fp.x, fp.y, 7.0, ['#2e7d4f', '#ffffff', '#2e7d4f'])
    mb.face([(p[0], p[1], 0.02) for p in offset(poly, 6)], 'ground', hex_rgb('#d8c9a3'), 0.4)  # sandy yard
    return _done(mb, a, collection)


def clinic(a, rng, collection=None):
    """A clinic or maternity home: two-storey block, white with sea-green or blue band, a red
    cross on the sign, a waiting shed, a ramp. research-civic 3, 5."""
    poly = _poly(a)
    mb = MeshBuilder()
    wear = _wear(a, rng, -0.05)
    band = hex_rgb(rng.pick(['#3e8e6e', '#3c78b4']))
    fc = a.get('facing', 0)
    H = block(mb, poly, max(1, min(4, a.get('storeys', 2))), dict(style='govt', wall=hex_rgb('#f3f1ea'), band=band, trim=band, wear=wear, window='sliding', fins=True, roof='parapet', tanks=2, facing=fc), rng)
    i, L, F = faces(poly)[fc]
    name = (a.get('label') or 'LIFE CARE CLINIC').upper()
    parts.signboard(mb, F, 0, 3.6, min(L - 1, 8), 1.0, dict(text=name, bg=hex_rgb('#ffffff'), fg=band, hand=False, wear=wear * 0.5))
    for (w, h) in ((0.9, 0.25), (0.25, 0.9)):  # red cross
        mb.box('paint', parts.at(F, -min(L - 1, 8) / 2 - 0.7, 0.15, 3.6), hex_rgb('#d2232a'), 0, size=(w, 0.05, h))
    # waiting shed with benches
    sh = parts.at(F, L / 4, -3.0, 0)
    for x in (-2, 2):
        for y in (-1, 1):
            parts.bar(mb, 'steel', sh @ Vector((x, y, 0)), sh @ Vector((x, y, 2.6)), 0.08, hex_rgb('#3a3a3a'))
    parts.corrugated(mb, sh @ Vector((-2.3, -1.4, 2.6)), sh @ Vector((2.3, -1.4, 2.6)), sh @ Vector((2.3, 1.4, 2.8)), sh @ Vector((-2.3, 1.4, 2.8)), dict(profile='trapezoid', pitch=0.2, depth=0.03, col=hex_rgb('#c3c7ca'), wear=0.4))
    for y in (-0.6, 0.6):
        mb.box('wood', sh @ Matrix.Translation((0, y, 0.45)), hex_rgb('#6b4f36'), 0.6, size=(3.6, 0.35, 0.06))
    return _done(mb, a, collection)


# ---------------------------------------------------------------- commerce
def phone_mall(a, rng, collection=None):
    """A house stacked into 3-4 storeys of phone shops: shop bays on every floor facing the street,
    a forest of signs and banners. research-housing conversions, research-commerce."""
    poly = _poly(a)
    mb = MeshBuilder()
    s = max(3, min(5, a.get('storeys', 3)))
    wear = _wear(a, rng)
    fc = a.get('facing', 0)
    H = block(mb, poly, s, dict(style='shops', wall=hex_rgb(rng.pick(['#efe2c4', '#f4f1ea', '#bcd9e6'])), band=hex_rgb('#3a3a3a'), wear=wear, floor_h=3.2, ground_h=3.6, window='sliding', roof='parapet', tanks=1, facing=fc), rng)
    i, L, F = faces(poly)[fc]
    for st in range(1, s):  # banners across the upper floors
        bg = rng.pick(['#1f5fa8', '#c8322b', '#2d7d46', '#f2c21b'])
        parts.signboard(mb, F, rng.between(-L / 6, L / 6), 3.6 + 3.2 * (st - 1) + 1.6, L * rng.between(0.5, 0.9), 0.8, dict(text=rng.pick(['PHONES • LAPTOPS • ACCESSORIES', 'UK USED PHONES', 'SCREEN REPAIR 30 MINS', 'GADGET PLAZA']), bg=hex_rgb(bg), fg=hex_rgb('#ffffff' if bg != '#f2c21b' else '#1a1a1a'), hand=False, wear=0.3))
    return _done(mb, a, collection)


def plaza(a, rng, collection=None, unfinished=False):
    """A multi-storey wholesale plaza: shop bays all round the ground floor, galleries above,
    a stair core; sometimes left as a frame. research-commerce plazas."""
    poly = _poly(a)
    mb = MeshBuilder()
    wear = _wear(a, rng)
    s = max(2, a.get('storeys', 3))
    if unfinished or rng.chance(0.33):
        from .parts import unfinished_storey
        for st in range(s):
            unfinished_storey(mb, poly, st * 3.4, dict(), rng.child('f', st))
            mb.face([(p[0], p[1], (st + 1) * 3.4) for p in poly], 'concrete', hex_rgb('#9c9890'), 0.6)
        return _done(mb, a, collection)
    block(mb, poly, s, dict(style='shops', wall=hex_rgb(rng.pick(['#e8e2d2', '#d8e6ec'])), band=hex_rgb('#2f6fae'), wear=wear, floor_h=3.4, ground_h=3.8, roof='parapet', tanks=3, facing=a.get('facing', 0),
                            shop_names=['WHOLESALE & RETAIL', 'IMPORTERS & DISTRIBUTORS', 'FABRICS', 'BAGS & SHOES', 'PROVISIONS WHOLESALE']), rng)
    return _done(mb, a, collection)


def strip(a, rng, collection=None):
    """The all-night strip: a hotel or lounge block with a neon sign and shop bays below."""
    poly = _poly(a)
    mb = MeshBuilder()
    s = max(2, a.get('storeys', 3))
    H = block(mb, poly, s, dict(style='shops', wall=hex_rgb(rng.pick(['#3a3c3e', '#6a1b9a', '#1f3f8a', '#f4f1ea'])), band=hex_rgb('#c9a13b'), wear=_wear(a, rng, -0.1), floor_h=3.3, ground_h=4.0, roof='parapet', facing=a.get('facing', 0),
                                shop_names=['SUYA SPOT', 'NOODLES • TEA', 'SHAWARMA & GRILLS', 'LOUNGE & BAR', 'POINT & KILL']), rng)
    i, L, F = faces(poly)[a.get('facing', 0)]
    parts.signboard(mb, F, 0, H + 1.2, min(L - 1, 10), 1.6, dict(text=rng.pick(['MOONLIGHT HOTEL', 'GOLDEN PALM SUITES', 'STARLIGHT LOUNGE']), bg=hex_rgb('#111111'), fg=hex_rgb('#ff4fd8'), hand=False, wear=0.2))
    return _done(mb, a, collection)


def bakery(a, rng, collection=None):
    """A bread bakery: a block shed with a big wood oven chimney, stacked firewood, bread trays
    and a sign. research-commerce bakeries."""
    poly = _poly(a)
    mb = MeshBuilder()
    wear = _wear(a, rng, 0.1)
    H = block(mb, poly, 1, dict(style='govt', wall=hex_rgb('#efe2c4'), band=hex_rgb('#8a4b2a'), wear=wear, floor_h=4.2, window='louvre', fins=False, roof='gable', pitch=14, roof_col=hex_rgb('#8a4b2a'), facing=a.get('facing', 0),
                                     sign=rng.pick(['AYO BREAD • SINCE 1998', 'TASTY BITE BAKERY', 'SWEET LOAF BREAD']), sign_bg=hex_rgb('#f2c21b'), sign_fg=hex_rgb('#8a1f2f')), rng)
    c = centroid(poly)
    p = poly[2]
    mb.box('block', Matrix.Translation((p[0] * 0.8 + c[0] * 0.2, p[1] * 0.8 + c[1] * 0.2, (H + 4) / 2)), hex_rgb('#5a4a3a'), 0.9, size=(1.2, 1.2, H + 4))  # soot-black oven chimney
    i, L, F = faces(poly)[(a.get('facing', 0) + 2) % 4]
    for k in range(int(L / 0.5)):  # firewood stack
        mb.box('wood', parts.at(F, -L / 2 + 0.4 + k * 0.5, 1.0, 0.6), shade(hex_rgb('#6b4f36'), rng.between(0.7, 1.1)), 0.8, size=(0.45, 1.2, 1.2))
    return _done(mb, a, collection)


def print_shop(a, rng, collection=None):
    """A house-front print shop: the ground floor opened up, paper bales, ink drums, a laminating
    table, signs for printing and binding. research-commerce print shops."""
    poly = _poly(a)
    mb = MeshBuilder()
    wear = _wear(a, rng)
    fc = a.get('facing', 0)
    block(mb, poly, max(1, a.get('storeys', 2)), dict(style='govt', wall=hex_rgb(rng.pick(['#efe2c4', '#bcd9e6', '#f4f1ea'])), band=hex_rgb('#3a3a3a'), wear=wear, window='louvre', fins=False, roof='parapet', shopfront=True, facing=fc,
                                                  sign=rng.pick(['PEDRO PRINTS • FLEX & BANNERS', 'CALENDARS • ID CARDS • LAMINATION', 'FAST PRINT & BINDING'])), rng)
    i, L, F = faces(poly)[fc]
    for k in range(rng.randrange(3, 7)):
        mb.box('cloth', parts.at(F, rng.between(-L / 2.5, L / 2.5), -0.8, 0.3), hex_rgb('#f2f2ee'), 0.2, size=(0.8, 0.6, 0.6))  # paper bales
    for k in range(3):
        parts.cyl(mb, 'steel', parts.at(F, -L / 2 + 0.6 + k * 0.7, -1.6, 0), 0.29, 0.88, hex_rgb(rng.pick(['#1f5fa8', '#111111', '#c62828'])), 0.7, seg=10)
    return _done(mb, a, collection)


def warehouse(a, rng, collection=None):
    """A portal-frame warehouse or works shed: block skirt, long-span cladding, roller doors."""
    poly = _poly(a)
    mb = MeshBuilder()
    wear = _wear(a, rng)
    fc = a.get('facing', 0)
    block(mb, poly, 1, dict(style='shed', wall=hex_rgb('#c9c3b6'), band=hex_rgb('#8a857a'), wear=wear, floor_h=8.0, roof='gable', pitch=8, overhang=0.4, roof_col=hex_rgb(rng.pick(['#c3c7ca', '#2b5c9e', '#8a4b2a'])), facing=fc), rng)
    for i, L, F in faces(poly):  # cladding above the block skirt
        n = int(L / 0.2)
        for k in range(0, n, 2):
            mb.box('zinc', parts.at(F, -L / 2 + (k + 0.5) * L / n, 0.03, 5.0), hex_rgb('#c3c7ca'), wear, size=(L / n, 0.03, 5.6))
        if i == fc:
            for u in (-L / 4, L / 4):
                parts.roller_shutter(mb, F, u, 4.0, dict(col=hex_rgb('#9aa3a8'), open=rng.between(0.0, 0.8), wear=wear))
    return _done(mb, a, collection)


def tank(a, rng, collection=None):
    """A fuel storage tank (tank farm) or a raised water tank: a big cylinder, stair, pipes."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    r = max(L, W) / 2 * (8 if max(L, W) < 2 else 1)  # data gives tiny markers for tank-farm tanks
    h = r * rng.between(0.6, 0.9)
    parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], 0)), r, h, hex_rgb(rng.pick(['#e8e6df', '#c9ced2'])), _wear(a, rng, -0.2), seg=32)
    parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], h)), r, r * 0.12, hex_rgb('#d8d8d8'), 0.3, seg=32, r2=r * 0.2)
    for k in range(int(h / 0.4)):  # spiral stair
        q = k * 0.18
        mb.box('steel', Matrix.Translation((c[0] + math.cos(q) * (r + 0.4), c[1] + math.sin(q) * (r + 0.4), k * 0.4)) @ Matrix.Rotation(q, 4, 'Z'), hex_rgb('#5a5a5a'), 0.4, size=(0.8, 0.9, 0.05))
    mb.face([(c[0] + math.cos(q) * (r + 3), c[1] + math.sin(q) * (r + 3), 0.03) for q in (k / 24 * math.tau for k in range(24))], 'concrete', hex_rgb('#8f8a80'), 0.5)
    return _done(mb, a, collection)


def crane(a, rng, collection=None):
    """A port crane: a rubber-tyred gantry over the stacks or a mobile harbour crane (research-transport)."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    col = hex_rgb(rng.pick(['#e8c21a', '#e07b1a', '#1f5fa8']))
    h = max(18, a.get('storeys', 10) * 2.2)
    for x in (-L / 2, L / 2):
        for y in (-W / 2, W / 2):
            mb.box('steel', T(m, x, y, h / 2), col, 0.4, size=(0.8, 0.8, h))
            parts.cyl(mb, 'rubber', T(m, x, y, 0.6) @ Matrix.Rotation(math.pi / 2, 4, 'X'), 0.6, 0.5, hex_rgb('#1b1b1b'), 0, seg=12)
        mb.box('steel', T(m, x, 0, 1.4), col, 0.4, size=(1.0, W, 1.0))
    for y in (-W / 2, W / 2):
        mb.box('steel', T(m, 0, y, h), col, 0.4, size=(L + 0.8, 1.2, 1.6))
    mb.box('steel', T(m, 0, 0, h - 1.2), hex_rgb('#e8e6df'), 0.3, size=(3.0, W, 2.0))  # trolley and cab
    for k in range(4):
        parts.bar(mb, 'steel', T(m, (k - 1.5) * 0.5, 0, h - 2.2).translation, T(m, (k - 1.5) * 0.5, 0, 4.0).translation, 0.03, hex_rgb('#222222'))
    container(mb, T(m, 0, 0, 1.4), 12.19, hex_rgb('#b03a2e'), 0.6, rng)
    return _done(mb, a, collection)


# ---------------------------------------------------------------- housing types
def flats(a, rng, collection=None):
    """1970s-80s government estate walk-ups: 3-4 storeys, balconies, stair cores, shops built into
    the gardens, laundry, tanks. research-housing estate flats."""
    poly = _poly(a)
    mb = MeshBuilder()
    wear = _wear(a, rng, 0.1)
    fc = a.get('facing', 0)
    block(mb, poly, max(2, a.get('storeys', 4)), dict(style='flats', wall=hex_rgb(rng.pick(['#efe2c4', '#e8d8b0', '#d8e6ec', '#f0d0b0'])), band=hex_rgb('#8a857a'), trim=hex_rgb('#f2efe6'), wear=wear, floor_h=3.0, window='louvre', roof='parapet', tanks=4, facing=fc, bars='vertical'), rng)
    i, L, F = faces(poly)[fc]
    for k in range(rng.randrange(1, 4)):  # a shop shack built into the garden
        u = rng.between(-L / 3, L / 3)
        m = parts.at(F, u, -3.0, 0)
        mb.box('wood', m @ Matrix.Translation((0, 0, 1.2)), hex_rgb(rng.pick(['#1f5fa8', '#c62828', '#f2c21b'])), 0.7, size=(2.4, 2.0, 2.4))
        parts.corrugated(mb, m @ Vector((-1.5, -1.3, 2.4)), m @ Vector((1.5, -1.3, 2.4)), m @ Vector((1.5, 1.2, 2.6)), m @ Vector((-1.5, 1.2, 2.6)), dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb('#7a4524'), wear=0.9))
    return _done(mb, a, collection)


def mansion(a, rng, collection=None):
    """Elite house in the style the data names (styles: mansion, modern villa, mediterranean villa,
    duplex, colonial bungalow). research-buildings 9.1, research-housing."""
    poly = _poly(a)
    style = a.get('style') or rng.pick({'mansion': 3, 'modern villa': 3, 'duplex': 2, 'mediterranean villa': 1, 'colonial bungalow': 1})
    mb = MeshBuilder()
    fc = a.get('facing', 0)
    s = max(1, min(3, a.get('storeys', 2)))
    if style in ('modern villa', 'duplex'):
        wall = hex_rgb(rng.pick(['#f5f5f2', '#e9e4d8', '#b5b1a8']))
        H = block(mb, poly, s, dict(style='govt', wall=wall, band=hex_rgb('#3a3c3e'), trim=hex_rgb('#3a3c3e'), wear=0.1, floor_h=3.8, window='sliding', win_w=2.4, win_h=2.2, fins=False, roof='parapet', facing=fc), rng)
        i, L, F = faces(poly)[fc]
        mb.box('wood', parts.at(F, L / 4, 0.12, H / 2), hex_rgb('#8a6a4a'), 0.1, size=(L / 4, 0.1, H))  # timber-look cladding strip
        mb.box('concrete', parts.at(F, -L / 6, 1.4, 3.9), hex_rgb('#f5f5f2'), 0.1, size=(L / 2, 2.8, 0.25))  # cantilevered slab
    elif style == 'colonial bungalow':
        H = block(mb, poly, 1, dict(style='govt', wall=hex_rgb('#f2ead8'), band=hex_rgb('#2f5e3a'), trim=hex_rgb('#ffffff'), wear=0.3, floor_h=4.0, window='casement', win_h=1.8, fins=False, roof='hip', pitch=24, overhang=1.6, roof_col=hex_rgb('#8e3b2a'), facing=fc), rng)
    else:  # classic mansion / mediterranean: columned portico, balusters, hipped stone-coated roof
        wall = hex_rgb(rng.pick(['#ede3c8', '#f2c9a8', '#f6f4ef']))
        H = block(mb, poly, s, dict(style='govt', wall=wall, band=hex_rgb('#c9a13b'), trim=hex_rgb('#ffffff'), wear=0.15, floor_h=3.8, window='casement', win_h=2.0, fins=False, roof='hip', pitch=28, overhang=0.7,
                                    roof_col=hex_rgb('#8e3b2a' if style == 'mediterranean villa' else rng.pick(['#3d4448', '#8e3b2a'])), facing=fc), rng)
        i, L, F = faces(poly)[fc]
        for u in (-2.4, -0.8, 0.8, 2.4):  # double-height portico columns
            parts.cyl(mb, 'paint', parts.at(F, u, 2.6, 0), 0.32, H - 0.4, hex_rgb('#ffffff'), 0.1, seg=14, r2=0.27)
            mb.box('paint', parts.at(F, u, 2.6, H - 0.3), hex_rgb('#ffffff'), 0.1, size=(0.8, 0.8, 0.3))
        mb.box('concrete', parts.at(F, 0, 2.0, H), hex_rgb('#ffffff'), 0.1, size=(6.2, 4.2, 0.4))
        mb.face([F @ Vector((-3.1, 4.1, H + 0.2)), F @ Vector((3.1, 4.1, H + 0.2)), F @ Vector((0, 4.1, H + 1.8))], 'paint', hex_rgb('#ffffff'), 0.1)
        if s > 1:
            parts.balcony(mb, F, 0, H - 0.2 - 3.8 * (s - 1) + 3.8, 5.6, dict(slab=hex_rgb('#ffffff'), rail='balusters', rail_col=hex_rgb('#ffffff'), wear=0.1)) if False else None
    if a.get('wall_poly'):
        parts.compound_wall(mb, a['wall_poly'], dict(h=3.0, paint=hex_rgb('#f2efe6'), coping=hex_rgb('#3a3c3e'), top='razor', gate=hex_rgb('#2a2a2a'), wear=0.1, gate_edge=fc), rng, a.get('wall_skip'))
    return _done(mb, a, collection, dict(style=style))


def villa(a, rng, collection=None):
    """Colonial bungalow on a leafy reserve (Apapa, old Ikoyi)."""
    return mansion(dict(a, style='colonial bungalow'), rng, collection)


def tower(a, rng, collection=None, crown=None, force_new=False):
    """Apartment, bank or office tower: glass curtain wall with a crown (new) or a 1970s concrete
    grid (old). research-buildings 9.3, 10.1; research-landmarks skylines."""
    poly = _poly(a)
    mb = MeshBuilder()
    s = max(5, a.get('storeys', 18))
    new = force_new or rng.chance(0.65)
    if new:
        block(mb, poly, s, dict(style='glass', wall=hex_rgb('#e9ecef'), band=hex_rgb('#3a3c3e'), trim=hex_rgb('#d0d4d8'), glass=hex_rgb(rng.pick(['#2a4a66', '#33504a', '#3a3f52'])), wear=0.05, floor_h=3.4, ground_h=5.0,
                                roof='parapet', crown=crown or rng.between(4, 10), facing=a.get('facing', 0)), rng)
    else:
        block(mb, poly, s, dict(style='govt', wall=hex_rgb('#d9d2c2'), band=hex_rgb('#3a3c3e'), wear=0.6, floor_h=3.3, ground_h=4.5, window='louvre', fins=True, roof='parapet', tanks=4, facing=a.get('facing', 0)), rng)
    return _done(mb, a, collection)


def bank_tower(a, rng, collection=None):
    """Bank Row: glass towers, each with its own crown (research-landmarks)."""
    return tower(a, rng, collection, crown=rng.between(8, 16), force_new=True)


def office(a, rng, collection=None):
    """A government or office slab: the 1970s-80s civic block with an agency band and a crest sign."""
    poly = _poly(a)
    mb = MeshBuilder()
    block(mb, poly, max(2, a.get('storeys', 5)), dict(style='govt', wall=hex_rgb('#ede3c8'), band=hex_rgb('#1d6f78'), wear=_wear(a, rng), floor_h=3.4, window='louvre', fins=True, roof='parapet', tanks=3, facing=a.get('facing', 0),
                                                  sign=(a.get('label') or 'STATE SECRETARIAT • BLOCK ' + str(rng.randrange(1, 12))).upper(), sign_bg=hex_rgb('#1d6f78'), sign_fg=hex_rgb('#ffffff')), rng)
    return _done(mb, a, collection)


def barracks(a, rng, collection=None, prison=False):
    """Army barracks or prison cellblock: long low rows of doors under a verandah, cream with a
    dark band; laundry; a watchtower for prisons. research-civic 11, 16, 17."""
    poly = _poly(a)
    mb = MeshBuilder()
    wear = _wear(a, rng, 0.2)
    band = hex_rgb('#2e4d3a' if prison else rng.pick(['#2f4a2a', '#8a3b2a']))
    fc = a.get('facing', 0)
    block(mb, poly, max(1, a.get('storeys', 1)), dict(style='govt', wall=hex_rgb('#e2d5b0' if prison else '#e6d6a8'), band=band, trim=band, wear=wear, floor_h=3.2, window='louvre', win_w=0.8, win_h=0.9, fins=False, bay=2.6,
                                                  roof='gable', pitch=12, roof_col=hex_rgb('#8a4b2a'), facing=fc, bars='grid' if prison else 'none'), rng)
    i, L, F = faces(poly)[fc]
    for k in range(int(L / 4)):  # laundry on lines between verandah posts
        u = -L / 2 + 2 + k * 4
        parts.bar(mb, 'steel', F @ Vector((u, -1.6, 2.0)), F @ Vector((u + 3, -1.6, 2.0)), 0.01, hex_rgb('#333333'))
        for j in range(4):
            mb.box('cloth', parts.at(F, u + 0.4 + j * 0.7, -1.6, 1.7), hex_rgb(rng.pick(['#d7263d', '#1b998b', '#f2c14e', '#ffffff', '#5bc0eb', '#2e294e'])), 0, size=(0.5, 0.02, 0.6))
    if prison:
        p = poly[0]
        mb.box('paint', Matrix.Translation((p[0], p[1], 4.5)), hex_rgb('#e2d5b0'), 0.5, size=(2.5, 2.5, 9))
        mb.box('glass', Matrix.Translation((p[0], p[1], 8.0)), hex_rgb('#24343e'), 0, size=(2.6, 2.6, 1.0))
        mb.box('concrete', Matrix.Translation((p[0], p[1], 9.1)), hex_rgb('#ffffff'), 0.4, size=(3.2, 3.2, 0.25))
    return _done(mb, a, collection)


def cellblock(a, rng, collection=None):
    return barracks(a, rng, collection, prison=True)


# ---------------------------------------------------------------- leisure and transport
def hotel(a, rng, collection=None):
    poly = _poly(a)
    mb = MeshBuilder()
    s = max(2, a.get('storeys', 3))
    H = block(mb, poly, s, dict(style='govt', wall=hex_rgb(rng.pick(['#f2e2b0', '#e6a7a8', '#bcd9e6'])), band=hex_rgb('#8a1f2f'), wear=_wear(a, rng), floor_h=3.2, ground_h=4.0, window='sliding', fins=s < 6, roof='parapet', tanks=2, facing=a.get('facing', 0)), rng)
    i, L, F = faces(poly)[a.get('facing', 0)]
    parts.signboard(mb, F, 0, H + 1.0, min(L - 1, 9), 1.4, dict(text=(a.get('label') or rng.pick(['HIGHLIFE HOTEL', 'IRETI HOTEL & SUITES', 'PEACEFUL INN'])).upper(), bg=hex_rgb('#111111'), fg=hex_rgb('#ff4f6a'), hand=False, wear=0.3))
    mb.box('concrete', parts.at(F, 0, 2.0, 4.0), hex_rgb('#f2efe6'), 0.3, size=(6, 4, 0.3))  # porch canopy
    return _done(mb, a, collection)


def nightclub(a, rng, collection=None):
    poly = _poly(a)
    mb = MeshBuilder()
    H = block(mb, poly, max(1, a.get('storeys', 2)), dict(style='govt', wall=hex_rgb('#1d1d22'), band=hex_rgb('#c9a13b'), trim=hex_rgb('#c9a13b'), wear=0.1, floor_h=4.5, window='sliding', fins=False, roof='parapet', facing=a.get('facing', 0)), rng)
    i, L, F = faces(poly)[a.get('facing', 0)]
    parts.signboard(mb, F, 0, H - 1.2, min(L - 1, 8), 1.2, dict(text=rng.pick(['CLUB VELVET', 'SKYBAR 21', 'OPULENCE']), bg=hex_rgb('#111111'), fg=hex_rgb('#4fd8ff'), hand=False, wear=0))
    for k in range(6):  # rope line posts
        parts.cyl(mb, 'steel', parts.at(F, -2.5 + k, -1.2, 0), 0.04, 1.0, hex_rgb('#c9a13b'), 0, seg=8)
    return _done(mb, a, collection)


def stands(a, rng, collection=None):
    """A raker stand of the decaying 1970s stadium: stepped concrete terraces on raking beams,
    a cantilever roof, a floodlight mast. research-landmarks / research-leisure National Bowl."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    rows = int(W / 0.8)
    for k in range(rows):
        mb.box('concrete', T(m, 0, -W / 2 + (k + 0.5) * 0.8, 0.5 + k * 0.45), shade(hex_rgb('#a8a49a'), 1 - 0.01 * k), 0.8, size=(L, 0.8, 0.45 + (0.0 if k else 0.5)))
        for x in range(int(L / 0.6)):  # faded seats in the club colours
            if rng.chance(0.55):
                mb.box('plastic', T(m, -L / 2 + 0.3 + x * 0.6, -W / 2 + (k + 0.5) * 0.8, 0.95 + k * 0.45), hex_rgb(rng.pick(['#2e7d4f', '#ffffff', '#8aa88a'])), 0.5, size=(0.4, 0.35, 0.3))
    for x in (-L / 2, 0, L / 2):  # raking beams
        parts.bar(mb, 'concrete', T(m, x, -W / 2, 0).translation, T(m, x, W / 2 + 1, rows * 0.45 + 1).translation, 0.6, hex_rgb('#8f8a80'), 0.8)
    mb.box('steel', T(m, 0, 0, rows * 0.45 + 5), hex_rgb('#9aa3a8'), 0.9, size=(L + 2, W + 3, 0.2))
    mast = T(m, L / 2 + 2, W / 2, 0)
    parts.cyl(mb, 'concrete', mast, 0.8, 30, hex_rgb('#a8a49a'), 0.8, seg=8, r2=0.5)
    mb.box('steel', mast @ Matrix.Translation((0, 0, 31)), hex_rgb('#3a3a3a'), 0.8, size=(5, 1, 2.5))
    return _done(mb, a, collection)


def terminal(a, rng, collection=None):
    """A bus terminal: a long multi-storey block over bus bays with a vast canopy, skywalk stubs."""
    poly = _poly(a)
    mb = MeshBuilder()
    s = max(1, a.get('storeys', 3))
    H = block(mb, offset(poly, -6), s, dict(style='glass', wall=hex_rgb('#e9ecef'), band=hex_rgb('#1f5fa8'), trim=hex_rgb('#d0d4d8'), wear=0.3, floor_h=4.5, ground_h=6.0, roof='parapet', facing=a.get('facing', 0)), rng)
    mb.face([(p[0], p[1], 6.5) for p in poly], 'steel', hex_rgb('#c3c7ca'), 0.4)
    mb.face([(p[0], p[1], 6.4) for p in reversed(poly)], 'steel', hex_rgb('#8a8f92'), 0.4)
    for p in poly:
        parts.cyl(mb, 'steel', Matrix.Translation((p[0], p[1], 0)), 0.3, 6.5, hex_rgb('#d8d8d8'), 0.3, seg=10)
    return _done(mb, a, collection)


def station(a, rng, collection=None):
    """A rail station: a long platform canopy on columns, a ticket hall block, fences."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    mb.box('concrete', T(m, 0, 0, 0.5), hex_rgb('#b8b2a6'), 0.5, size=(L, W * 0.5, 1.0))
    for k in range(int(L / 8) + 1):
        parts.cyl(mb, 'steel', T(m, -L / 2 + k * 8, 0, 1.0), 0.2, 4.5, hex_rgb('#2f6fae'), 0.3, seg=8)
    parts.corrugated(mb, T(m, -L / 2, -W / 4 - 1, 5.2).translation, T(m, L / 2, -W / 4 - 1, 5.2).translation, T(m, L / 2, W / 4 + 1, 5.8).translation, T(m, -L / 2, W / 4 + 1, 5.8).translation,
                     dict(profile='trapezoid', pitch=0.2, depth=0.03, col=hex_rgb('#c3c7ca'), wear=0.4))
    hall = [(T(m, x, y, 0).translation.x, T(m, x, y, 0).translation.y) for (x, y) in ((-8, W / 4 + 1), (8, W / 4 + 1), (8, W / 2), (-8, W / 2))]
    block(mb, ccw(hall), 1, dict(style='govt', wall=hex_rgb('#ede3c8'), band=hex_rgb('#2f6fae'), wear=0.4, floor_h=4.5, window='sliding', fins=False, roof='parapet', sign='HUB RAIL STATION'), rng)
    return _done(mb, a, collection)


def toll_booth(a, rng, collection=None):
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    mb.box('concrete', T(m, 0, 0, 0.15), hex_rgb('#e8c21a'), 0.3, size=(L, W, 0.3))
    mb.box('glass', T(m, 0, 0, 1.6), hex_rgb('#24343e'), 0, size=(L * 0.6, W * 0.6, 2.4))
    mb.box('steel', T(m, 0, 0, 2.9), hex_rgb('#f2f2f2'), 0.2, size=(L * 0.7, W * 0.7, 0.2))
    mb.box('steel', T(m, 0, 0, 6.8), hex_rgb('#1f5fa8'), 0.2, size=(L + 8, W + 4, 0.6))  # the plaza canopy
    for x in (-L / 2 - 3.5, L / 2 + 3.5):
        parts.cyl(mb, 'steel', T(m, x, 0, 0), 0.25, 6.6, hex_rgb('#d8d8d8'), 0.2, seg=10)
    for k in range(8):
        mb.box('steel', T(m, L / 2 + 0.3 + k * 0.45, -W / 2 - 0.3, 1.0), hex_rgb('#c62828' if k % 2 else '#f2f2f2'), 0.2, size=(0.45, 0.08, 0.1))
    return _done(mb, a, collection)


def toll_canopy(a, rng, collection=None):
    """The toll plaza's canopy: a wide flat roof on steel columns over the lanes, the booths under
    it as islands with yellow-and-black ends, lights under the eaves. research-landmarks 35."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    mb.box('steel', T(m, 0, 0, 7.2), hex_rgb('#1f5fa8'), 0.25, size=(L + 2, W + 2, 0.8))
    mb.box('steel', T(m, 0, 0, 6.75), hex_rgb('#f2f2f2'), 0.2, size=(L, W, 0.1))
    n = max(2, int(W / 4.5))
    for k in range(n):  # rows of columns, the booth islands between the lanes
        y = -W / 2 + (k + 0.5) * W / n
        for x in (-L / 3, L / 3):
            parts.cyl(mb, 'steel', T(m, x, y, 0), 0.25, 6.7, hex_rgb('#d8d8d8'), 0.2, seg=10)
        mb.box('concrete', T(m, 0, y, 0.15), hex_rgb('#e8c21a'), 0.3, size=(L * 0.8, 1.2, 0.3))
        mb.box('glass', T(m, 0, y, 1.5), hex_rgb('#24343e'), 0, size=(2.4, 1.0, 2.2))
        for e in (-1, 1):
            mb.box('paint', T(m, e * L * 0.4, y, 0.5), hex_rgb('#1d1d1d'), 0.3, size=(0.3, 1.2, 0.7))
        for x in range(int(-L / 2) + 2, int(L / 2), 4):
            mb.box('emit', T(m, x, y, 6.65), hex_rgb('#fff1d0'), 0, size=(1.2, 0.3, 0.05))
    return _done(mb, a, collection)


def cctv_tower(a, rng, collection=None):
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    h = max(12, a.get('storeys', 4) * 4)
    parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], 0)), 0.5, h, hex_rgb('#c9ced2'), 0.3, seg=10, r2=0.25)
    for k in range(4):
        q = k / 4 * math.tau
        mb.box('steel', Matrix.Translation((c[0] + math.cos(q) * 0.5, c[1] + math.sin(q) * 0.5, h - 0.5)) @ Matrix.Rotation(q, 4, 'Z'), hex_rgb('#f2f2f2'), 0.1, size=(0.5, 0.25, 0.25))
    return _done(mb, a, collection)


def transformer_kind(a, rng, collection=None):
    from .street import transformer
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    transformer(mb, c[0], c[1], rng)
    return _done(mb, a, collection)


def stage(a, rng, collection=None):
    """A protest park stage: a raised slab, a steel truss roof, speaker stacks."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    mb.box('concrete', T(m, 0, 0, 0.6), hex_rgb('#a8a49a'), 0.6, size=(L, W, 1.2))
    for x in (-L / 2 + 0.3, L / 2 - 0.3):
        for y in (-W / 2 + 0.3, W / 2 - 0.3):
            mb.box('steel', T(m, x, y, 4.2), hex_rgb('#3a3a3a'), 0.4, size=(0.4, 0.4, 6.0))
    mb.box('steel', T(m, 0, 0, 7.3), hex_rgb('#3a3a3a'), 0.4, size=(L, W, 0.5))
    for x in (-L / 2 + 0.8, L / 2 - 0.8):
        mb.box('plastic', T(m, x, -W / 2 + 0.8, 2.4), hex_rgb('#1a1a1a'), 0, size=(0.9, 0.8, 2.2))
    return _done(mb, a, collection)


def canopy(a, rng, collection=None):
    """An owambe / event canopy: white and coloured tent on poles, rows of chairs."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    col = hex_rgb(rng.pick(['#ffffff', '#1f5fa8', '#c62828']))
    for x in (-L / 2, L / 2):
        for y in (-W / 2, W / 2):
            parts.cyl(mb, 'steel', T(m, x, y, 0), 0.04, 2.8, hex_rgb('#d8d8d8'), 0.2, seg=6)
    mb.face([T(m, -L / 2, -W / 2, 2.8).translation, T(m, L / 2, -W / 2, 2.8).translation, T(m, 0, 0, 3.8).translation], 'cloth', col, 0)
    mb.face([T(m, L / 2, -W / 2, 2.8).translation, T(m, L / 2, W / 2, 2.8).translation, T(m, 0, 0, 3.8).translation], 'cloth', col, 0)
    mb.face([T(m, L / 2, W / 2, 2.8).translation, T(m, -L / 2, W / 2, 2.8).translation, T(m, 0, 0, 3.8).translation], 'cloth', col, 0)
    mb.face([T(m, -L / 2, W / 2, 2.8).translation, T(m, -L / 2, -W / 2, 2.8).translation, T(m, 0, 0, 3.8).translation], 'cloth', col, 0)
    for x in range(int(L / 0.6)):
        for y in range(int(W / 1.0)):
            _chair(mb, T(m, -L / 2 + 0.3 + x * 0.6, -W / 2 + 0.5 + y, 0, rz=math.pi), hex_rgb('#eeeeee'))
    return _done(mb, a, collection)


def bust(a, rng, collection=None):
    """A bust on a roundabout plinth (an invented founder), on a stepped base with a plaque."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    for k, (s, h) in enumerate(((3.0, 0.4), (2.2, 0.4), (1.2, 2.0))):
        mb.box('concrete', T(m, 0, 0, sum(x[1] for x in ((3.0, 0.4), (2.2, 0.4), (1.2, 2.0))[:k]) + h / 2), hex_rgb('#e8e2d2' if k < 2 else '#d9d2c2'), 0.4, size=(s, s, h))
    bronze = hex_rgb('#5a4a2a')
    parts.cyl(mb, 'steel', T(m, 0, 0, 2.8), 0.55, 0.7, bronze, 0.5, seg=14, r2=0.3)  # shoulders
    parts.cyl(mb, 'steel', T(m, 0, 0, 3.5), 0.12, 0.2, bronze, 0.5, seg=10)
    from .core import Vector as _V  # noqa: F401
    head = T(m, 0, 0, 3.85)
    parts.cyl(mb, 'steel', head @ Matrix.Translation((0, 0, -0.15)), 0.22, 0.4, bronze, 0.5, seg=12, r2=0.18)
    mb.box('steel', T(m, 0, -0.62, 1.8), hex_rgb('#c9a13b'), 0.3, size=(0.8, 0.02, 0.5))
    return _done(mb, a, collection)


def palace(a, rng, collection=None):
    """A traditional ruler's palace: a high wall with a gate arch, a long two-storey palace in
    white and royal colours with a verandah, courtyard. Shown with respect (safe ground)."""
    poly = _poly(a)
    mb = MeshBuilder()
    inner = offset(poly, -6)
    H = block(mb, inner, 2, dict(style='govt', wall=hex_rgb('#f4f1ea'), band=hex_rgb('#6a1b9a'), trim=hex_rgb('#c9a13b'), wear=0.25, floor_h=4.0, window='casement', win_h=2.0, fins=False, roof='hip', pitch=22, overhang=1.2,
                                       roof_col=hex_rgb('#8e3b2a'), facing=a.get('facing', 0)), rng)
    perimeter(mb, poly, dict(paint=hex_rgb('#e8dcc0'), coping=hex_rgb('#6a1b9a'), gate=hex_rgb('#6a1b9a'), h=3.2, wear=0.3), rng, a.get('facing', 0))
    i, L, F = faces(poly)[a.get('facing', 0)]
    for s in (-1, 1):  # gate pylons with an arch
        mb.box('paint', parts.at(F, s * 3.2, 0, 3.0), hex_rgb('#f4f1ea'), 0.3, size=(1.4, 1.4, 6.0))
    mb.box('paint', parts.at(F, 0, 0, 6.3), hex_rgb('#c9a13b'), 0.3, size=(7.8, 1.4, 0.9))
    return _done(mb, a, collection)


def stilt_bar(a, rng, collection=None):
    """The stilt bar: a two-level timber bar on posts over the water, coloured lights, a ladder."""
    from .kinds import stilt
    ob, _ = stilt(dict(a, storeys=1), rng, collection)
    return ob, {}


def saw_shed(a, rng, collection=None):
    """A sawmill shed: an open-sided long-span roof on steel posts, a saw bench, logs and planks."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    for x in [-L / 2 + k * L / 6 for k in range(7)]:
        for y in (-W / 2, W / 2):
            parts.bar(mb, 'steel', T(m, x, y, 0).translation, T(m, x, y, 5.0).translation, 0.2, hex_rgb('#5a5a5a'), 0.8)
    parts.corrugated(mb, T(m, -L / 2 - 0.5, -W / 2 - 0.5, 5.0).translation, T(m, L / 2 + 0.5, -W / 2 - 0.5, 5.0).translation, T(m, L / 2 + 0.5, W / 2 + 0.5, 5.8).translation, T(m, -L / 2 - 0.5, W / 2 + 0.5, 5.8).translation,
                     dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb('#7a4524'), wear=0.95))
    mb.box('steel', T(m, 0, 0, 0.5), hex_rgb('#3a3a3a'), 0.8, size=(8.0, 1.2, 1.0))  # saw bench
    for k in range(10):
        parts.cyl(mb, 'wood', T(m, rng.between(-L / 2.5, L / 2.5), rng.between(-W / 3, W / 3), 0.3) @ Matrix.Rotation(math.pi / 2, 4, 'Y') @ Matrix.Rotation(rng.between(0, 3), 4, 'X'), 0.3, rng.between(4, 8), hex_rgb('#7a5a3a'), 0.6, seg=8)
    return _done(mb, a, collection)


def hall(a, rng, collection=None):
    """A live-music hall / event hall: a big shed with a painted front, a canopy and a name."""
    poly = _poly(a)
    mb = MeshBuilder()
    block(mb, poly, 1, dict(style='shed', wall=hex_rgb(rng.pick(['#2f2f6a', '#6a1b9a', '#c8a020'])), band=hex_rgb('#1a1a1a'), wear=_wear(a, rng), floor_h=9, roof='gable', pitch=10, roof_col=hex_rgb('#c3c7ca'), facing=a.get('facing', 0),
                            sign=(a.get('label') or rng.pick(['THE GROOVE HALL', 'AFRO HALL', 'EVENT CENTRE'])).upper(), sign_bg=hex_rgb('#1a1a1a'), sign_fg=hex_rgb('#f2c21b')), rng)
    return _done(mb, a, collection)


def clubhouse(a, rng, collection=None):
    """An estate or golf clubhouse: low, wide hipped roof, deep verandah, white with dark trim."""
    return mansion(dict(a, style='colonial bungalow'), rng, collection)


def studio(a, rng, collection=None):
    return phone_mall(dict(a, storeys=2), rng, collection)


def cafe(a, rng, collection=None):
    poly = _poly(a)
    mb = MeshBuilder()
    block(mb, poly, 1, dict(style='shops', wall=hex_rgb('#1f3f8a'), band=hex_rgb('#f2c21b'), wear=_wear(a, rng), floor_h=3.4, roof='parapet', facing=a.get('facing', 0),
                            shop_names=['NETWORK CAFE • BROWSING', 'PRINTING • SCANNING', 'GAMES • 24 HRS']), rng)
    return _done(mb, a, collection)


def works(a, rng, collection=None):
    return warehouse(a, rng, collection)


def unfinished_plaza(a, rng, collection=None):
    return plaza(a, rng, collection, unfinished=True)


# ---------------------------------------------------------------- point places (web/gidi-data.js 'pois')
def police_station(a, rng, collection=None):
    """Divisional police station (research-civic 7): an invented two-tone block (pale blue, navy
    band), a charge-room counter, a yard of rusting seized cars and an okada heap behind."""
    poly = _poly(a)
    mb = MeshBuilder()
    fc = a.get('facing', 0)
    block(mb, poly, max(1, min(2, a.get('storeys', 2))), dict(style='govt', wall=hex_rgb('#8db6d9'), band=hex_rgb('#1f2e5a'), trim=hex_rgb('#f2f2ee'), wear=_wear(a, rng), window='louvre', fins=False, roof='parapet', facing=fc, bars='grid',
                                                           sign=(a.get('label') or 'GIDI POLICE • DIVISIONAL HQ').upper(), sign_bg=hex_rgb('#1f2e5a'), sign_fg=hex_rgb('#ffffff')), rng)
    i, L, F = faces(poly)[(fc + 2) % 4]
    from .vehicles import car, okada
    for k in range(rng.randrange(3, 7)):  # the pound
        car(mb, parts.at(F, rng.between(-L / 2.5, L / 2.5), rng.between(3, 9), 0, rz=rng.between(0, 6)), rng, 'wreck', kind=rng.pick(['saloon', 'suv', 'pickup']))
    for k in range(rng.randrange(4, 10)):
        okada(mb, parts.at(F, rng.between(-L / 3, L / 3), rng.between(1.5, 3), 0.1 * k % 0.6, rz=rng.between(0, 6), rx=rng.between(-1.4, 1.4)), rng, 'battered')
    return _done(mb, a, collection)


def fire_station(a, rng, collection=None):
    """Fire station (research-civic 12): white with a signal-red band, red appliance bay doors,
    a drill/hose tower."""
    poly = _poly(a)
    mb = MeshBuilder()
    fc = a.get('facing', 0)
    block(mb, poly, 2, dict(style='govt', wall=hex_rgb('#f2f0ea'), band=hex_rgb('#c8202a'), trim=hex_rgb('#c8202a'), wear=_wear(a, rng), window='sliding', fins=False, roof='parapet', facing=fc, entrance=False,
                            sign=(a.get('label') or 'GIDI FIRE SERVICE').upper(), sign_bg=hex_rgb('#c8202a'), sign_fg=hex_rgb('#ffffff')), rng)
    i, L, F = faces(poly)[fc]
    for u in (-L / 4, L / 4):
        parts.roller_shutter(mb, F, u, min(3.6, L / 2 - 0.6), dict(col=hex_rgb('#c8202a'), open=rng.between(0.0, 0.9), wear=0.3))
    p = poly[(fc + 2) % 4]
    mb.box('paint', Matrix.Translation((p[0], p[1], 7.5)), hex_rgb('#f2f0ea'), 0.4, size=(3, 3, 15))
    mb.box('paint', Matrix.Translation((p[0], p[1], 14)), hex_rgb('#c8202a'), 0.4, size=(3.05, 3.05, 1.0))
    return _done(mb, a, collection)


def fuel_station(a, rng, collection=None):
    """A fuel station (research-commerce; no real brands): a canopy on columns over 2-4 pump
    islands, a small shop, a price board, an invented livery. Pumps at least 15 m from the road."""
    poly = _poly(a)
    mb = MeshBuilder()
    lv = rng.pick([('#1f6f3a', '#f2c21b'), ('#c8202a', '#f2f2ee'), ('#1f4fa0', '#f2c21b'), ('#e07b1a', '#1f3f8a')])
    c1, c2 = hex_rgb(lv[0]), hex_rgb(lv[1])
    i, L, F = faces(poly)[a.get('facing', 0)]
    mb.face([(p[0], p[1], 0.05) for p in offset(poly, 3)], 'concrete', hex_rgb('#a8a49a'), 0.5)
    can = parts.at(F, 0, -4.0, 0)
    for x in (-5, 5):
        for y in (-3, 3):
            mb.box('paint', can @ Matrix.Translation((x, y, 2.6)), hex_rgb('#f2f2ee'), 0.2, size=(0.5, 0.5, 5.2))
    mb.box('paint', can @ Matrix.Translation((0, 0, 5.5)), c2, 0.2, size=(14, 9, 0.6))
    mb.box('paint', can @ Matrix.Translation((0, 0, 5.85)), c1, 0.2, size=(14.2, 9.2, 0.25))
    for x in (-5, 0, 5):
        mb.box('concrete', can @ Matrix.Translation((x, 0, 0.12)), hex_rgb('#d8d2c6'), 0.4, size=(1.2, 3.5, 0.24))
        for y in (-1, 1):
            mb.box('steel', can @ Matrix.Translation((x, y * 0.9, 1.0)), c1, 0.3, size=(0.6, 0.45, 1.6))
    block(mb, poly, 1, dict(style='govt', wall=hex_rgb('#f2f2ee'), band=c1, trim=c1, wear=0.3, window='sliding', fins=False, roof='parapet', facing=a.get('facing', 0), sign='MART • LUBRICANTS', sign_bg=c1, sign_fg=c2), rng)
    pb = parts.at(F, L / 2 + 2, -6, 0)
    mb.box('steel', pb @ Matrix.Translation((0, 0, 3)), hex_rgb('#3a3a3a'), 0.3, size=(0.3, 0.3, 6))
    parts.signboard(mb, pb, 0, 5.0, 2.0, 2.0, dict(text='PMS 980\nAGO 1450', bg=c1, fg=c2, hand=False, wear=0.2))
    return _done(mb, a, collection)


def bank_branch(a, rng, collection=None):
    """A bank branch: a clean 2-3 storey block, tinted glass, an aluminium-clad entrance, a
    security post and an ATM gallery, an invented livery."""
    poly = _poly(a)
    mb = MeshBuilder()
    lv = rng.pick([('#7a1f2f', '#f2f2ee'), ('#1f3f8a', '#f2c21b'), ('#e07b1a', '#f2f2ee'), ('#2e7d4f', '#f2f2ee'), ('#5a2a7a', '#f2c21b')])
    block(mb, poly, max(2, min(3, a.get('storeys', 2))), dict(style='glass', wall=hex_rgb('#e9ecef'), band=hex_rgb(lv[0]), trim=hex_rgb('#c9ced2'), glass=hex_rgb('#2a3a4a'), wear=0.1, floor_h=3.6, ground_h=4.2, roof='parapet', facing=a.get('facing', 0),
                                                           sign=rng.pick(['STEADY TRUST BANK', 'HARBOUR BANK', 'UNITY CAPITAL BANK', 'GREENLEAF BANK']), sign_bg=hex_rgb(lv[0]), sign_fg=hex_rgb(lv[1])), rng)
    i, L, F = faces(poly)[a.get('facing', 0)]
    for k in range(3):
        mb.box('steel', parts.at(F, -L / 3 + k * 0.9, 0.3, 1.0), hex_rgb('#c9ced2'), 0.1, size=(0.7, 0.4, 2.0))
        mb.box('emit', parts.at(F, -L / 3 + k * 0.9, 0.52, 1.3), hex_rgb('#4fd8ff'), 0, size=(0.4, 0.02, 0.3))
    return _done(mb, a, collection)


def chemist(a, rng, collection=None):
    """A chemist / patent medicine store: a shop house with a green-cross sign."""
    from .archetypes import house
    ob, spec = house(dict(a, kind='front', frontage=0.0), rng, collection)
    return ob, spec


def cemetery(mb, c, r, rng):
    """A public cemetery round a point: a wall, an iron gate, crowded tombs, weeds."""
    pts = [(c[0] + math.cos(t) * r, c[1] + math.sin(t) * r) for t in (k / 8 * math.tau + 0.39 for k in range(8))]
    mb.face([(p[0], p[1], 0.04) for p in pts], 'ground', hex_rgb('#8a8a4a'), 0.6)
    perimeter(mb, ccw(pts), dict(paint=hex_rgb('#e8e2d2'), coping=hex_rgb('#3a3a3a'), gate=hex_rgb('#1d1d1d'), h=2.0, wear=0.8), rng)
    for x in range(int(-r * 0.6), int(r * 0.6), 3):
        for y in range(int(-r * 0.6), int(r * 0.6), 2):
            if rng.chance(0.75):
                m = Matrix.Translation((c[0] + x + rng.between(-0.3, 0.3), c[1] + y, 0)) @ Matrix.Rotation(rng.between(-0.08, 0.08), 4, 'Z')
                col = hex_rgb(rng.pick(['#e8e2d2', '#d8d2c6', '#c9c3b6', '#f2efe6']))
                mb.box('concrete', m @ Matrix.Translation((0, 0, 0.25)), col, 0.8, size=(2.0, 0.9, 0.5))
                mb.box('concrete', m @ Matrix.Translation((-0.9, 0, 0.75)), col, 0.8, size=(0.12, 0.7, 0.9))


def bus_shelter(mb, m, rng):
    """A bus stop: a steel shelter with a bench and a route board, or just a pole (research-street 2.5)."""
    for x in (-1.8, 1.8):
        mb.box('steel', m @ Matrix.Translation((x, 0.6, 1.3)), hex_rgb('#3a3a3a'), 0.4, size=(0.1, 0.1, 2.6))
    mb.box('steel', m @ Matrix.Translation((0, 0.4, 2.65)), hex_rgb('#1f4fa0'), 0.4, size=(4.0, 1.6, 0.1))
    mb.box('wood', m @ Matrix.Translation((0, 0.8, 0.45)), hex_rgb('#6b4f36'), 0.6, size=(3.2, 0.35, 0.06))
    parts.signboard(mb, m @ Matrix.Translation((0, 1.3, 0)), 0, 2.2, 1.6, 0.5, dict(text='BUS STOP', bg=hex_rgb('#f2c21b'), fg=hex_rgb('#1a1a1a'), hand=False, wear=0.4))


# ---------------------------------------------------------------- the Heights' beach and office grid
def office_block(a, rng, collection=None):
    """Victoria-Island-style office and hotel grid: glass curtain walls or a clean concrete frame,
    a podium, a generator, a security post."""
    poly = _poly(a)
    mb = MeshBuilder()
    s = max(2, a.get('storeys', 3)) * rng.pick([1, 2, 2, 3])
    if rng.chance(0.6):
        block(mb, poly, s, dict(style='glass', wall=hex_rgb('#e9ecef'), band=hex_rgb('#3a3c3e'), trim=hex_rgb('#d0d4d8'), glass=hex_rgb(rng.pick(['#2a4a66', '#33504a', '#3a3f52', '#4a5a6a'])), wear=0.08, floor_h=3.6, ground_h=4.5, roof='parapet', crown=rng.between(1, 4), facing=a.get('facing', 0)), rng)
    else:
        block(mb, poly, s, dict(style='govt', wall=hex_rgb(rng.pick(['#f2f0ea', '#e8e2d2', '#d9d6cf'])), band=hex_rgb('#3a3c3e'), trim=hex_rgb('#f2f0ea'), wear=0.2, floor_h=3.5, window='sliding', fins=rng.chance(0.5), roof='parapet', tanks=2, facing=a.get('facing', 0)), rng)
    return _done(mb, a, collection)


def _thatch(mb, cx, cy, z, rx, ry, h, rng):
    """A palm-thatch roof: a low pyramid of straw with a ragged fringe."""
    corners = [(cx - rx, cy - ry), (cx + rx, cy - ry), (cx + rx, cy + ry), (cx - rx, cy + ry)]
    straw = hex_rgb(rng.pick(['#c9a46a', '#b8925a', '#d8b878']))
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        mb.face([(a[0], a[1], z), (b[0], b[1], z), (cx, cy, z + h)], 'cloth', straw, 0.5)
        mb.face([(b[0], b[1], z), (a[0], a[1], z), (cx, cy, z + h)], 'cloth', shade(straw, 0.6), 0.5)
        n = int(math.dist(a, b) / 0.3)
        for k in range(n):  # fringe
            t = (k + 0.5) / n
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            mb.box('cloth', Matrix.Translation((x, y, z - 0.18)), shade(straw, rng.between(0.8, 1.1)), 0.5, size=(0.3, 0.3, rng.between(0.2, 0.45)))


def beach_bar(a, rng, collection=None):
    """A Sunday-beach bar: a timber deck, a palm-thatch roof on poles, a bar counter with stools,
    a cooler, plastic chairs and umbrellas on the sand."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    mb.box('wood', T(m, 0, 0, 0.25), hex_rgb('#8a6a4a'), 0.5, size=(L, W, 0.15))
    for x in (-L / 2 + 0.3, 0, L / 2 - 0.3):
        for y in (-W / 2 + 0.3, W / 2 - 0.3):
            parts.cyl(mb, 'wood', T(m, x, y, 0.3), 0.1, 2.8, hex_rgb('#6b4f36'), 0.6, seg=8)
    _thatch(mb, c[0], c[1], 3.1, L / 2 + 0.6, W / 2 + 0.6, 1.8, rng)
    mb.box('wood', T(m, 0, -W / 4, 0.85), hex_rgb(rng.pick(['#2f6fae', '#c62828', '#2e7d4f'])), 0.5, size=(L * 0.6, 0.6, 1.1))
    for k in range(5):
        parts.cyl(mb, 'steel', T(m, -L * 0.25 + k * L * 0.12, -W / 4 - 0.7, 0.3), 0.18, 0.75, hex_rgb('#c9ced2'), 0.2, seg=10)
    for k in range(rng.randrange(4, 9)):
        _chair(mb, T(m, rng.between(-L, L), rng.between(W / 2 + 1, W / 2 + 6), 0, rz=rng.between(0, math.tau)), hex_rgb(rng.pick(['#d32f2f', '#eeeeee', '#1e88e5'])))
    for k in range(rng.randrange(1, 3)):
        p = T(m, rng.between(-L / 2, L / 2), W / 2 + rng.between(2, 5), 0)
        parts.cyl(mb, 'steel', p, 0.03, 2.3, hex_rgb('#dddddd'), 0, seg=6)
        parts.cyl(mb, 'cloth', p @ Matrix.Translation((0, 0, 2.0)), 1.4, 0.4, hex_rgb(rng.pick(['#e53935', '#1e88e5', '#fdd835'])), 0, seg=12, r2=0.02)
    return _done(mb, a, collection)


def beach_shack(a, rng, collection=None):
    """A beach shack: painted plank walls, a zinc lean-to roof, a serving hatch, a cooler."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    col = hex_rgb(rng.pick(['#2f6fae', '#2e7d4f', '#d9b23a', '#c62828', '#e8e2d6']))
    for (x, y, w, d) in ((0, -W / 2, L, 0.05), (0, W / 2, L, 0.05), (-L / 2, 0, 0.05, W), (L / 2, 0, 0.05, W)):
        mb.box('wood', T(m, x, y, 1.15), col, rng.between(0.4, 0.9), size=(w, d, 2.3))
    mb.box('paint', T(m, 0, -W / 2 - 0.02, 1.4), (0.03, 0.03, 0.03), 0, size=(L * 0.6, 0.02, 0.8))
    parts.corrugated(mb, T(m, -L / 2 - 0.3, -W / 2 - 0.8, 2.3).translation, T(m, L / 2 + 0.3, -W / 2 - 0.8, 2.3).translation, T(m, L / 2 + 0.3, W / 2 + 0.2, 2.6).translation, T(m, -L / 2 - 0.3, W / 2 + 0.2, 2.6).translation,
                     dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb('#7a4524'), wear=0.9))
    mb.box('plastic', T(m, L / 3, -W / 2 - 0.6, 0.3), hex_rgb('#1565c0'), 0.3, size=(0.6, 0.4, 0.45))
    return _done(mb, a, collection)


def horse(mb, m, rng):
    """A beach horse for hire: slim body, long neck, a saddle cloth."""
    col = hex_rgb(rng.pick(['#5a3a24', '#e8e2d6', '#2a2018', '#8a5a34']))
    parts.cyl(mb, 'skin', m @ Matrix.Translation((-0.65, 0, 1.25)) @ Matrix.Rotation(math.pi / 2, 4, 'Y'), 0.3, 1.35, col, 0, seg=10, r2=0.28)
    for x in (-0.5, 0.5):
        for y in (-0.14, 0.14):
            parts.cyl(mb, 'skin', m @ Matrix.Translation((x, y, 0)), 0.05, 1.1, col, 0, seg=6, r2=0.06)
    neck = m @ Matrix.Translation((0.6, 0, 1.3)) @ Matrix.Rotation(-0.6, 4, 'Y')
    parts.cyl(mb, 'skin', neck, 0.15, 0.8, col, 0, seg=8, r2=0.1)
    mb.box('skin', m @ Matrix.Translation((1.0, 0, 1.95)) @ Matrix.Rotation(0.9, 4, 'Y'), col, 0, size=(0.55, 0.2, 0.22))
    mb.box('cloth', m @ Matrix.Translation((-0.1, 0, 1.55)), hex_rgb(rng.pick(['#c62828', '#1f5fa8', '#c9a13b'])), 0, size=(0.6, 0.64, 0.05))


def horse_shelter(a, rng, collection=None):
    """Where the beach horses stand: thatch on posts, a rail, hay, two or three horses."""
    poly, c, ang, L, W, m = footprint(a)
    mb = MeshBuilder()
    for x in (-L / 2, 0, L / 2):
        for y in (-W / 2, W / 2):
            parts.cyl(mb, 'wood', T(m, x, y, 0), 0.1, 2.6, hex_rgb('#6b4f36'), 0.6, seg=8)
    _thatch(mb, c[0], c[1], 2.6, L / 2 + 0.4, W / 2 + 0.4, 1.2, rng)
    parts.bar(mb, 'wood', T(m, -L / 2, -W / 2, 1.1).translation, T(m, L / 2, -W / 2, 1.1).translation, 0.08, hex_rgb('#6b4f36'), 0.6)
    for k in range(rng.randrange(2, 4)):
        horse(mb, T(m, -L / 2 + 2 + k * 3, 0, 0, rz=math.pi / 2 + rng.between(-0.2, 0.2)), rng)
    return _done(mb, a, collection)
