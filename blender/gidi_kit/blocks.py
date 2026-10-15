"""A parametric building block that most non-house kinds are made from, plus shared pieces
(signs with names, flagpoles, perimeter walls with gates, domes, minarets, towers).

Styles (research-civic 0.1, research-housing, research-commerce):
  govt     1970s-80s concrete frame: floor bands, sun fins, louvre windows, an agency band
  glass    curtain wall with a mullion grid, spandrels and a crown
  shops    ground floor of shop bays with shutters and signs, plain windows above (plazas, phone malls)
  flats    walk-up flats: balconies on every floor, an open stair, washing
  shed     portal-frame shed: block skirt, long-span cladding, a big door (warehouses, churches, works)
  row      one-storey row of doors and windows under a verandah (barracks, cellblocks, classrooms)
"""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import MeshBuilder, ccw, centroid, chamfer, edge_out, frame, hex_rgb, offset, prism, shade
from .materials import master

STOREY = parts.STOREY


def faces(poly):
    """(index, length, frame) for each wall of a counter-clockwise polygon."""
    out = []
    for i in range(len(poly)):
        A, B = poly[i], poly[(i + 1) % len(poly)]
        n = edge_out(poly, i)
        out.append((i, math.dist(A, B), frame(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0), (B[0] - A[0], B[1] - A[1]), n)))
    return out


def street_face(poly, a):
    return a.get('facing', 0) % len(poly)


def block(mb, poly, storeys, o, rng):
    """Build a block on `poly`. o: dict(style, wall, band, trim, wear, floor_h, ground_h, glass, roof, tanks, sign, facing)."""
    style, wear = o.get('style', 'govt'), o.get('wear', 0.4)
    fh, gh = o.get('floor_h', 3.4), o.get('ground_h', o.get('floor_h', 3.4))
    H = gh + fh * (storeys - 1)
    wall, band, trim = o['wall'], o.get('band', o['wall']), o.get('trim', hex_rgb('#f2efe6'))
    glass = o.get('glass', hex_rgb('#24343e'))
    fc = o.get('facing', 0)
    prism(mb, 'paint' if style != 'shed' else 'block', poly, 0, H, shade(wall, 0.82), wall, wear)
    prism(mb, 'paint', offset(poly, 0.05), 0, 0.5, shade(band, 0.7), shade(band, 0.75), wear + 0.1)
    for k in range(1, storeys):
        z = gh + fh * (k - 1)
        prism(mb, 'concrete', offset(poly, 0.08 if style != 'glass' else 0.04), z - 0.12, z + 0.12, trim if style != 'govt' else shade(wall, 0.9), trim, wear)
    if style == 'govt' and o.get('band'):  # the agency band under the roof
        prism(mb, 'paint', offset(poly, 0.03), H - 0.7, H - 0.2, band, band, wear)
    for i, L, F in faces(poly):
        bay = o.get('bay', 3.0 if style != 'glass' else 1.5)
        n = max(1, int((L - 1.0) / bay))
        us = [(j - (n - 1) / 2) * (L - 1.0) / n for j in range(n)]
        for st in range(storeys):
            z0 = 0 if st == 0 else gh + fh * (st - 1)
            zc = z0 + (gh if st == 0 else fh) * 0.52
            if style == 'glass':
                h = (gh if st == 0 else fh) - 0.7
                mb.face([F @ Vector((-L / 2 + 0.3, 0.06, z0 + 0.35)), F @ Vector((L / 2 - 0.3, 0.06, z0 + 0.35)), F @ Vector((L / 2 - 0.3, 0.06, z0 + 0.35 + h)), F @ Vector((-L / 2 + 0.3, 0.06, z0 + 0.35 + h))], 'glass', glass, 0)
                for u in us + [-L / 2 + 0.3, L / 2 - 0.3]:
                    mb.box('steel', parts.at(F, u - (L - 1.0) / n / 2 if u in us else u, 0.09, z0 + 0.35 + h / 2), hex_rgb('#c9ced2'), 0.1, size=(0.08, 0.08, h))
                continue
            if st == 0 and style == 'shops' or (st == 0 and i == fc and o.get('shopfront')):
                for u in us:
                    parts.roller_shutter(mb, F, u, min(2.6, (L - 1.0) / n - 0.4), dict(col=hex_rgb(rng.pick(['#9aa3a8', '#2f6fae', '#c0c4c6', '#2e7d4f'])), open=rng.between(0.3, 0.95), wear=wear))
                    if rng.chance(0.85):  # every bay its own sign
                        bg, fg = rng.pick([('#1f5fa8', '#ffffff'), ('#f2c21b', '#1a1a1a'), ('#c8322b', '#ffffff'), ('#ffffff', '#c8322b'), ('#2d7d46', '#ffffff')])
                        parts.signboard(mb, F, u, gh - 0.42, min(2.6, (L - 1.0) / n - 0.3), 0.55, dict(text=rng.pick(o.get('shop_names', ['PHONES & ACCESSORIES', 'LAPTOP REPAIRS', 'GSM WORLD', 'CHARGERS & CABLES', 'BLESSED GADGETS', 'POS • TRANSFER'])), bg=hex_rgb(bg), fg=hex_rgb(fg), hand=False, wear=wear * 0.5))
                continue
            if style == 'shed':
                continue
            for j, u in enumerate(us):
                if st == 0 and i == fc and j == (n - 1) // 2 and o.get('entrance', True):
                    parts.door(mb, F, u, dict(frame=trim, door=o.get('door', hex_rgb('#3a3a3a')), wear=wear))
                    continue
                parts.window(mb, F, u, zc, dict(type=o.get('window', 'louvre'), w=o.get('win_w', 1.4), h=o.get('win_h', 1.3), frame=trim, glass=glass, mullion=hex_rgb('#b8bcc0'),
                                                 bars=o.get('bars', 'none') if st == 0 else 'none', bar_col=hex_rgb('#262626'), wear=wear, hood=False,
                                                 glass_mat='glass_lit' if rng.chance(0.3) else 'glass'))
                if style == 'govt' and o.get('fins', True):  # sun fins over each window
                    mb.box('concrete', parts.at(F, u, 0.35, zc + o.get('win_h', 1.3) / 2 + 0.25), shade(wall, 0.92), wear, size=(min(bay - 0.2, 2.2), 0.7, 0.1))
                if style == 'flats' and st > 0 and j % 2 == 0 and i == fc:
                    parts.balcony(mb, F, u, z0 + 0.05, min(bay * 1.6, 3.4), dict(slab=hex_rgb('#c9c3b6'), rail=rng.pick(['steel', 'balusters']), rail_col=trim, wear=wear))
    # roof
    roof = o.get('roof', 'parapet')
    if roof == 'parapet':
        parts.roof_flat(mb, poly, H, dict(parapet_h=0.9, paint=wall, trim=trim, slab=hex_rgb('#8f8a80'), wear=wear, chamfer=0.05))
    elif roof in ('gable', 'hip'):
        parts.roof_pitched(mb, poly, H, dict(form=roof, pitch_deg=o.get('pitch', 18), overhang=o.get('overhang', 0.6), profile='trapezoid', pitch=0.2, depth=0.032,
                                             col=o.get('roof_col', hex_rgb('#9aa3a8')), col2=o.get('roof_col', hex_rgb('#9aa3a8')), mixed=False, wear=min(1, wear + 0.1), wall_wear=wear,
                                             gable_col=wall, fascia=trim, fascia_wood=False), rng)
    if o.get('tanks'):
        c = centroid(poly)
        for k in range(o['tanks']):
            p = poly[k % len(poly)]
            parts.water_tank(mb, p[0] * 0.7 + c[0] * 0.3, p[1] * 0.7 + c[1] * 0.3, H, dict(r=0.8, h=1.6, stand=1.2, col=hex_rgb('#1d1d1d'), wear=0.4))
    if o.get('crown'):  # a lit crown on a tower
        c = centroid(poly)
        inner = offset(poly, -1.5)
        prism(mb, 'steel', inner, H + 0.9, H + o['crown'], hex_rgb('#c9ced2'), hex_rgb('#e8ecef'), 0.1)
        parts.cyl(mb, 'steel', Matrix.Translation((c[0], c[1], H + o['crown'])), 0.15, 8.0, hex_rgb('#c9ced2'), 0.1, seg=8, r2=0.03)
    if o.get('sign'):
        i, L, F = faces(poly)[fc]
        parts.signboard(mb, F, 0, min(H - 0.6, gh + 0.6) if storeys > 1 else H - 0.5, min(L - 1.0, 8.0), 0.9, dict(text=o['sign'], bg=o.get('sign_bg', trim), fg=o.get('sign_fg', band), hand=False, wear=wear * 0.5))
    return H


# ---------------------------------------------------------------- shared civic pieces
def perimeter(mb, poly, o, rng, gate_edge=0):
    """Compound wall with pillars every 3 m, coping, a painted band and a steel gate on gate_edge."""
    parts.compound_wall(mb, poly, dict(h=o.get('h', 2.4), paint=o['paint'], coping=o.get('coping', hex_rgb('#f2efe6')), top=o.get('top', 'plain'),
                                       gate=o.get('gate', hex_rgb('#2b4a66')), wear=o.get('wear', 0.4), gate_edge=gate_edge), rng)


def flagpole(mb, x, y, h, flag_cols):
    parts.cyl(mb, 'steel', Matrix.Translation((x, y, 0)), 0.05, h, hex_rgb('#d8d8d8'), 0.2, seg=8, r2=0.03)
    for k, c in enumerate(flag_cols):  # a vertical tricolour-like flag of invented colours
        mb.box('cloth', Matrix.Translation((x + 0.3 + k * 0.4, y, h - 0.6)), hex_rgb(c), 0, size=(0.4, 0.02, 0.9))


def dome(mb, x, y, z, r, col, wear=0.2, seg=20, rings=8, finial=True):
    prev = None
    for k in range(rings + 1):
        t = k / rings * math.pi / 2
        rr, zz = r * math.cos(t), z + r * 1.1 * math.sin(t)
        ring = [Vector((x + math.cos(a) * rr, y + math.sin(a) * rr, zz)) for a in (i / seg * math.tau for i in range(seg))]
        if prev:
            for i in range(seg):
                j = (i + 1) % seg
                mb.face([prev[i], prev[j], ring[j], ring[i]], 'zinc', col, wear)
        prev = ring
    if finial:  # a crescent on a rod
        parts.cyl(mb, 'steel', Matrix.Translation((x, y, z + r * 1.1)), 0.06, r * 0.5, hex_rgb('#c9a13b'), 0, seg=8)
        for k in range(7):
            a0, a1 = math.pi * (0.15 + 0.7 * k / 7), math.pi * (0.15 + 0.7 * (k + 1) / 7)
            parts.bar(mb, 'steel', (x + math.cos(a0) * r * 0.18, y, z + r * 1.6 + math.sin(a0) * r * 0.18), (x + math.cos(a1) * r * 0.18, y, z + r * 1.6 + math.sin(a1) * r * 0.18), 0.05, hex_rgb('#c9a13b'))


def minaret(mb, x, y, h, wall, trim, dome_col, wear, rng):
    """A tapering minaret with a balcony ring near the top and a small dome."""
    seg = 12
    parts.cyl(mb, 'paint', Matrix.Translation((x, y, 0)), 1.2, h * 0.8, wall, wear, seg=seg, r2=0.9)
    for z in (h * 0.4, h * 0.8):
        parts.cyl(mb, 'paint', Matrix.Translation((x, y, z - 0.15)), 1.35, 0.3, trim, wear, seg=seg)
    parts.cyl(mb, 'paint', Matrix.Translation((x, y, h * 0.8)), 0.8, h * 0.15, wall, wear, seg=seg)
    dome(mb, x, y, h * 0.95, 0.9, dome_col, wear, seg=12, rings=5)
    for k in range(3):  # loudspeakers lashed to the top
        a = k / 3 * math.tau + rng.between(0, 1)
        mb.box('steel', Matrix.Translation((x + math.cos(a) * 1.0, y + math.sin(a) * 1.0, h * 0.83)) @ Matrix.Rotation(a, 4, 'Z'), hex_rgb('#d8d8d8'), 0.3, size=(0.3, 0.3, 0.4))
