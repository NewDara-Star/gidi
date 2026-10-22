"""The draft desk: the old kit's seeded rules, run once on a spot to write what they choose into its map as full records
(decisions, 22 Oct: one ground truth; KIT.md section 12, "Records").

The kit (oldtown.py and the parts it draws with) reads only those records and throws no dice: a spot builds from its
map and nothing else. A first draft of a new spot comes from here (blender/kit_draft.py), and after that the records are
the map's, edited by hand like any other field. Each planner is the old kit code with the drawing taken out: the same
dice in the same order, so a drafted spot builds exactly as the seeded kit built it.

The old city's generators (city.py, generate.py, archetypes.py...) still hand the shared parts an Rng; those parts pass it
here and draw what comes back, so the old base builds as before.
"""
import math
import os
import zlib

import numpy as np
from mathutils import Matrix, Vector

from . import detail
from .core import Rng, ccw, chamfer, edge_out, frame, hex_rgb, offset, shade

R = lambda v: float(v)


def place(M):
    """A placement matrix (a translation and a turn about z) as the record [x, y, z, turn]."""
    return [M.translation.x, M.translation.y, M.translation.z, math.atan2(M[1][0], M[0][0])]


# ---------------------------------------------------------------- the ground's noise (was roadbed.Ground's)
def _hash(i, j, seed):
    h = (i.astype(np.int64) * 374761393 + j.astype(np.int64) * 668265263 + seed * 2654435761) & 0xffffffff
    h = ((h ^ (h >> 13)) * 1274126177) & 0xffffffff
    return ((h ^ (h >> 16)) & 0xffff) / 65535.0


def vnoise(x, y, seed):
    i, j = np.floor(x), np.floor(y)
    fx, fy = x - i, y - j
    sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = _hash(i, j, seed), _hash(i + 1, j, seed)
    c, d = _hash(i, j + 1, seed), _hash(i + 1, j + 1, seed)
    return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy


def fbm(x, y, seed, octaves=3):
    v, amp, tot = 0.0, 1.0, 0.0
    for o in range(octaves):
        v = v + amp * vnoise(x * 2 ** o, y * 2 ** o, seed + 97 * o)
        tot += amp
        amp *= 0.5
    return v / tot


class Noise:
    """The noise the old roadbed seeded from the street's id: humps and dips, the frayed tar edge, the tar patches, the
    edge rut's wander. Sampled once into the street's ground grids."""

    def __init__(self, sp):
        self.sp = sp
        self.seed = zlib.crc32(sp['id'].encode()) & 0xffff
        (self.x0, self.cy), (self.x1, _) = sp['centreline'][0], sp['centreline'][-1]
        self.half = sp['width_m'] / 2
        rel = sp.get('relief') or {}
        self.amp, self.scale = rel.get('amp_m', 0.0), rel.get('scale_m', 6.0)
        gx, gy = np.meshgrid(np.arange(self.x0, self.x1, 0.5), np.arange(self.cy - self.half, self.cy + self.half, 0.25))
        cover = sp.get('tar_cover', 0.5)
        self.thr = float(np.quantile(self.tar_noise(gx, gy), 1 - cover)) if 0 < cover < 1 else (1.0 if cover <= 0 else -1.0)

    def relief(self, x, y):
        s = self.scale
        return self.amp * 2 * (fbm(x / (s * 1.6), y / s, self.seed) - 0.5)

    def fray(self, x, y):
        return 0.5 * (vnoise(x / 0.9, y / 0.9, self.seed + 7) - 0.5) + 0.6 * (vnoise(x / 4, y / 4, self.seed + 8) - 0.5)

    def tar_noise(self, x, y):
        patch = self.sp.get('tar_patch_m', 3.0)
        return fbm(x / patch, y / (patch * 0.7), self.seed + 31) + 0.15 * (vnoise(x / 0.5, y / 0.5, self.seed + 3) - 0.5)

    def wob(self, x):
        return 0.35 * (vnoise(x / 3, 0.5, self.seed + 41) - 0.5)

    def rut_k(self, x):
        return 0.7 + 0.6 * vnoise(x / 2, 1.5, self.seed + 43)


def _xs(x0, x1, near, grow):
    """Where the ground sheet's columns go along the street: fine near the camera, coarser with distance."""
    xs, x = [], x0
    while x < x1:
        xs.append(x)
        x += near + max(0.0, x - 20) * grow
    xs.append(x1)
    return np.array(xs)


def ground_grids(sp, near=0.2, grow=0.012):
    """A street's ground grids, sampled where the ground sheet has its corners: relief (m), fray (m, how far the tar's
    edge wanders in or out), tar (the tar field: tar where > 0), and along x the edge rut's wander (m) and strength."""
    N = Noise(sp)
    br, bl = sp.get('ground_band_m', (8.6, 2.9))   # how far the sheet reaches past the right and left edges
    ys = (N.cy - N.half - br, N.cy + N.half + bl)
    xs = _xs(N.x0 - 5, N.x1, near, grow)
    yv = np.arange(ys[0], ys[1] + 1e-6, 0.15)
    X, Y = np.meshgrid(xs, yv, indexing='ij')
    return dict(xs=xs, ys=yv, band=np.array(ys), relief=N.relief(X, Y), fray=N.fray(X, Y), tar=N.tar_noise(X, Y) - N.thr,
                rut_wob=N.wob(xs), rut_k=N.rut_k(xs))


# ---------------------------------------------------------------- zinc
def zinc_slope(A, B, C, D, spec, wear_of=None):
    """One slope of zinc sheets (zinc.sheets): how many sheets up the slope, the colour blotch's phases, and each sheet's
    tone (main, second, new), shade, wear and how badly each nail line and its lapped edge have rusted."""
    from .zinc import COVER
    A, B, C, D = (Vector(p) for p in (A, B, C, D))
    L = (B - A).length
    if L < 1e-3:
        return None
    ab = (B - A) / L
    up = (D - A) - ab * (D - A).dot(ab)
    hgt = up.length
    if hgt < 1e-3:
        return None
    rng = Rng('zinc', round(A.x, 1), round(A.y, 1), round(A.z, 1), round(B.x, 1), round(B.y, 1))
    web = detail.web()
    w0 = spec['wear']
    ns = max(1, round(L / (COVER * 2 if web else COVER)))
    nr = max(1, math.ceil(hgt / rng.between(2.4, 3.4)))
    ph = [rng.between(0, math.tau) for _ in range(3)]
    sheets = []
    for j in range(ns):
        sw = wear_of(j) if wear_of else max(0.0, min(1.0, w0 + rng.between(-0.3, 0.3)))
        new = rng.chance(0.02 + 0.06 * w0)
        tone = 'new' if new else ('second' if spec.get('mixed') and j % 3 == 0 else 'main')
        sh = rng.between(0.85, 1.1)
        if new:
            sw *= 0.15
        nails, edges = [], []
        for r in range(nr):
            v0, v1 = r / nr, (r + 1) / nr
            v0e = max(0.0, v0 - (0.12 / hgt if r else 0.0))
            npur = 0 if web else max(1, round(hgt * (v1 - v0e) / 1.0))
            nails.append([rng.random() ** 2 for i in range(max(1, npur))])
            edges.append(rng.random() ** 2)
        sheets.append(dict(tone=tone, shade=sh, wear=sw, nails=nails, edge=edges))
    return dict(rows=nr, ph=ph, sheets=sheets)


def slab_blotch(poly):
    """A flat roof's ponding blotch (zinc.slab): three phases."""
    n = len(poly)
    cx, cy = sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n
    rng = Rng('slab', round(cx, 1), round(cy, 1))
    return [rng.between(0, math.tau) for _ in range(3)]


def blotch(key):
    """A house's paint blotch (wear.Weather): six phases."""
    r = Rng('wear', *key).child('blotch')
    return [r.between(0, math.tau) for _ in range(6)]


def roof_pitched(poly, H, spec, rng):
    """A pitched roof (parts.roof_pitched): its sag and every slope's sheets."""
    from .parts import roof_slopes
    e0, e1 = math.dist(poly[0], poly[1]), math.dist(poly[1], poly[2])
    short = min(e0, e1)
    sag = spec['sag'] if 'sag' in spec else max(0.0, spec['wear'] - 0.45) * rng.child('sag').between(0.05, 0.3) * min(1.0, short / 5)
    sheet_wear = lambda i: max(0.0, min(1.0, spec['wear'] + rng.child('sheet', i).between(-0.35, 0.35)))
    s = dict(spec, sag=sag)
    slopes = []
    for q in roof_slopes(poly, H, s)['slopes']:
        if spec['pitch'] < 0.3:
            slopes.append(zinc_slope(*q, s, sheet_wear))
        else:   # long sheets (not zinc): only each sheet's wear
            slopes.append(dict(wears=[sheet_wear(i) for i in range(int(math.dist(q[0], q[1]) / spec.get('sheet_w', 0.9)) + 1)]))
    return dict(sag=sag, slopes=slopes)


# ---------------------------------------------------------------- weathering on a wall face (wear.py)
def streak_leaves(u, z_top, length, w, dark, k, y, taper):
    """A run of grime as the strips it is drawn with: a wide run is never even, so it splits into a few narrower ones."""
    if w > 0.35 and length > 0.4 and taper < 1.0 and not detail.web():
        r = Rng('streak', round(u, 2), round(z_top, 2), round(length, 2))
        n = 2 + int(w / 0.6)
        out = []
        for j in range(n):
            ww = w / n * r.between(0.6, 1.7)
            uu = u - w / 2 + (j + 0.5) * w / n + r.between(-0.3, 0.3) * w / n
            lo, hi = max(u - w / 2, uu - ww / 2), min(u + w / 2, uu + ww / 2)
            uu, ww = (lo + hi) / 2, hi - lo
            out += streak_leaves(uu, z_top, length * r.between(0.45, 1.05), ww, dark, k * r.between(0.65, 1.0), y + j * 0.0005, taper)
        return out
    return [dict(streak=[u, z_top, length, w, dark, k, y, taper])]


def patch(u, z, w, h, col, rng, y):
    n = 11
    rr = [rng.between(0.7, 1.0) for i in range(n)]
    mix = [rng.between(0.0, 0.3) for i in range(n)]
    return dict(patch=dict(u=u, z=z, w=w, h=h, col=list(col), r=rr, mix=mix, y=y))


def bare_block(u, z0, w, courses, rng, y=0.05):
    ch, bl = 0.225, 0.45
    out = []
    for r in range(courses):
        t = (r + 0.5) / courses * 2 - 1
        hw = w / 2 * math.sqrt(max(0.0, 1 - t * t)) ** 0.6
        sh = bl / 2 if r % 2 else 0.0
        ul = math.floor((u - hw * rng.between(0.7, 1.05) - sh) / bl) * bl + sh
        uh = math.ceil((u + hw * rng.between(0.7, 1.05) - sh) / bl) * bl + sh
        if uh - ul < bl - 1e-6:
            out.append(None)
            continue
        shades = []
        x = ul
        while x < uh - 1e-6:
            shades.append(rng.between(0.85, 1.12))
            x += bl
        out.append(dict(ul=ul, uh=uh, shades=shades))
    return dict(block=dict(z0=z0, y=y, courses=out))


def age_face(L, z_top, wear, paint, openings, bands, rng, flat_top=False, foot=True, ac=0, few=False):
    """Weather one wall face (wear.age_face): its streaks, patches, broken render and AC units as marks."""
    from .wear import CEMENT, OFF, mix
    out = []
    S = lambda *a, **k: out.extend(streak_leaves(*a, **k))
    w_ = wear
    half = L / 2 - 0.25
    if half < 0.4:
        return out
    below = lambda z: max([b + 0.1 for b in bands if b + 0.1 < z - 0.05] + [0.47])
    taken = [(o[1] - o[3] / 2 - 0.15, o[1] + o[3] / 2 + 0.15, o[2] - o[4] / 2 - 0.2, o[2] + o[4] / 2 + 0.25) for o in openings]
    free = lambda u0, u1, z0, z1: u0 >= -half - 1e-6 and u1 <= half + 1e-6 and not any(u0 < b and u1 > a and z0 < d and z1 > c for a, b, c, d in taken)
    for kind, u, z, w, h, barred in openings:
        if kind != 'window':
            continue
        sill = z - h / 2 - 0.16
        if rng.chance((0.35 + 0.6 * w_) * (0.5 if few else 1.0)):
            ln = min(sill - below(sill), rng.between(0.7, 2.0) * (0.6 + w_))
            if ln > 0.2:
                if rng.chance(0.5):
                    S(u, sill, ln, w + 0.35, 'grime', min(0.9, rng.between(0.55, 0.85) * (0.5 + w_)), OFF, 0.8)
                else:
                    for s in (-1, 1):
                        S(u + s * (w / 2 + 0.1), sill, ln, rng.between(0.2, 0.4), 'grime', min(0.9, rng.between(0.6, 0.9) * (0.5 + w_)), OFF, 0.9)
        if barred and rng.chance(0.25 + 0.7 * w_):
            for k in range(rng.randrange(2, 5)):
                uu = u + rng.between(-w / 2, w / 2)
                ln = min(sill - below(sill), rng.between(0.25, 0.9))
                if ln > 0.1:
                    S(uu, sill - 0.01, ln, rng.between(0.03, 0.07), 'rust', rng.between(0.45, 0.8), OFF + 0.002, 0.5)
        if not detail.web() and rng.chance(0.3 * w_):
            for s in (-1, 1):
                S(u + s * (w / 2 + 0.05), z + h / 2 + 0.12, rng.between(0.3, 0.7), 0.12, 'grime', 0.3 * (0.5 + w_), OFF, 0.9)
    for kind, u, z, w, h, barred in openings:
        if kind == 'balcony' and rng.chance(0.4 + 0.6 * w_):
            zb = z - h / 2 - 0.13
            for k in range(rng.randrange(2, 5)):
                uu = u + rng.between(-w / 2, w / 2)
                ln = min(zb - below(zb), rng.between(0.6, 2.0))
                ww = rng.between(0.2, 0.7)
                S(uu, zb, ln, ww, 'grime', min(0.9, rng.between(0.5, 0.85) * (0.5 + w_)), OFF, 0.8)
    for b in bands:
        for k in range(int(rng.between(0, 3) * w_ * L / 8 * (0.5 if detail.web() else 1.0) * (0.5 if few else 1.0))):
            uu, zb = rng.between(-half, half), b - 0.11
            if free(uu - 0.2, uu + 0.2, zb - 0.5, zb):
                ln = min(zb - below(zb), rng.between(0.4, 1.6))
                ww = rng.between(0.15, 0.5)
                S(uu, zb, ln, ww, 'grime', min(0.85, rng.between(0.4, 0.75) * (0.5 + w_)), OFF, 0.8)
    if flat_top and rng.chance(0.3 + 0.7 * w_):
        ln = rng.between(0.3, 0.8)
        S(0, z_top - 0.13, ln, 2 * half + 0.4, 'grime', min(0.8, rng.between(0.4, 0.65) * (0.4 + w_)), OFF - 0.003, 1.0)
    n_top = int(L / 2.5 * (0.4 + w_) * (1.6 if flat_top else 0.6) * rng.between(0.6, 1.3) * (0.5 if detail.web() else 1.0) * (0.5 if few else 1.0))
    for k in range(n_top):
        uu = rng.between(-half, half)
        ln = rng.between(0.6, 2.8 if flat_top else 1.4) * (0.5 + w_)
        sw_ = rng.between(0.2, 0.9)
        uu = max(-half + sw_ / 2, min(half - sw_ / 2, uu))
        kk = min(0.95, rng.between(0.5, 0.9) * (0.4 + w_))
        S(uu, z_top - 0.13, ln, sw_, 'grime', kk, OFF, rng.between(0.6, 1.0))
    for k in range(int(rng.between(0, 2.5) * w_ * L / 6 + 0.5)):
        pw, ph = rng.between(0.35, 1.4), rng.between(0.3, 1.0)
        uu, zz = rng.between(-half + pw / 2, half - pw / 2), rng.between(0.7, z_top - 0.6)
        if free(uu - pw / 2, uu + pw / 2, zz - ph / 2, zz + ph / 2):
            pc = CEMENT if rng.chance(0.6) else mix(tuple(v * rng.between(1.03, 1.1) for v in paint), CEMENT, 0.25)
            out.append(patch(uu, zz, pw, ph, pc, rng, OFF - 0.004))
    if foot and not few and rng.chance(0.1 + 0.6 * w_):
        bw, z0, nc = rng.between(0.9, 2.2), rng.between(0.0, 0.3), rng.randrange(2, 6)
        uu = rng.pick([-half + bw / 2, half - bw / 2, rng.between(-half + bw / 2, half - bw / 2)]) if half > bw / 2 else 0
        if half > bw / 2 and free(uu - bw / 2 - 0.25, uu + bw / 2 + 0.25, z0, z0 + nc * 0.225):
            out.append(bare_block(uu, z0, bw, nc, rng.child('block')))
    if not few and rng.chance(0.25 * w_):
        bw, nc = rng.between(0.9, 1.6), rng.randrange(2, 5)
        uu, zz = rng.between(-half + bw / 2, half - bw / 2), rng.between(1.2, max(1.3, z_top - 1.4))
        if half > bw / 2 and free(uu - bw / 2 - 0.25, uu + bw / 2 + 0.25, zz, zz + nc * 0.225):
            out.append(bare_block(uu, zz, bw, nc, rng.child('block2'), y=OFF + 0.002))
    for k in range(ac):
        for _ in range(6):
            uu = rng.between(-half + 0.5, half - 0.5)
            zz = rng.pick([b for b in bands] or [0.0]) + rng.between(1.0, 1.6)
            if free(uu - 0.5, uu + 0.5, zz - 0.35, zz + 0.6):
                out.append(dict(ac=[uu, zz]))
                S(uu - 0.2, zz - 0.02, min(zz - below(zz), rng.between(0.8, 2.2)), 0.18, 'grime', 0.55, OFF, 0.4)
                taken.append((uu - 0.55, uu + 0.55, zz - 0.4, zz + 0.65))
                break
    return out


# ---------------------------------------------------------------- street things (street.py, props.py, parcels.py)
def litter_piece(rng):
    """One piece of litter: what it is (from the old mix: sachets, bags, bottles, packs, cans, husks), its colour, its turn
    and its own shape."""
    from .street import LITTER
    col, kind, _ = rng.pick({l: l[2] for l in LITTER})
    rec = dict(kind=kind, col=col, rz=rng.between(0, math.tau))
    if kind == 'sachet':
        rec['tilt'] = rng.between(-0.2, 0.2)
    elif kind == 'bag':
        rec['r'], rec['h'], rec['r2'] = rng.between(0.05, 0.1), rng.between(0.04, 0.08), rng.between(0.02, 0.05)
    return rec


def refuse_heap(r, rng):
    rings, seg = 5, 14
    h = r * rng.between(0.3, 0.5)
    jit, cols = [], []
    for k in range(rings + 1):
        ring = []
        for i in range(seg):
            ring.append([rng.between(0.85, 1.15), rng.between(0.85, 1.15)])
        jit.append(ring)
        if k:
            cols.append([rng.pick(['#3a3026', '#4a3e30', '#2a2622']) for i in range(seg)])
    lit = []
    for _ in range(int(r * r * 12)):
        a, d = rng.between(0, math.tau), rng.between(0, r)
        zz = h * max(0, 1 - (d / r) ** 1.6) * 0.9
        lit.append(dict(litter_piece(rng), at=[math.cos(a) * d, math.sin(a) * d, zz]))
    return dict(h=h, jitter=jit, cols=cols, litter=lit)


def pole(rng, h=None, wood=False):
    out = {}
    if not h:
        out['h'] = h = rng.between(9, 11)
    out['lean'] = [rng.between(-0.06, 0.06), rng.between(-0.06, 0.06)]
    if not wood:
        out['wear'] = rng.between(0.4, 0.8)
    out['arm'] = rng.between(0, math.pi)
    return out


def tree(rng, kind=None, h=None):
    """A tree's form: a palm's height, lean and fronds, or a broad tree's lobes."""
    out = dict(kind=kind or rng.pick({'broad': 3, 'palm': 2}))
    if out['kind'] == 'palm':
        out['h'] = h or rng.between(7, 13)
        out['lean'] = [rng.between(-0.6, 0.6), rng.between(-0.6, 0.6)]
        out['fronds'] = []
        for f in range(11):
            a = rng.between(-0.2, 0.2)
            out['fronds'].append(dict(turn=a, shades=[rng.between(0.8, 1.15) for s in range(4)]))
        return out
    out['h'] = h or rng.between(6, 11)
    out['lobes'] = []
    for k in range(rng.randrange(4, 7)):
        lobe = dict(a=rng.between(0, math.tau), r=rng.between(0, out['h'] * 0.25), z=rng.between(0.6, 0.85), size=rng.between(0.22, 0.32))
        lobe['col'] = rng.pick(['#3f7a2e', '#4f8a34', '#2f6a2a'])
        lobe['shade'] = rng.between(0.85, 1.1)
        out['lobes'].append(lobe)
    return out


def bin_litter(rng):
    out = []
    for k in range(9):
        a, d = rng.between(0, math.tau), rng.between(0, 0.25)
        dz = 0.7 + rng.between(0, 0.12)
        out.append(dict(litter_piece(rng), at=[math.cos(a) * d, math.sin(a) * d, dz]))
    for k in range(6):
        a, d = rng.between(0, math.tau), rng.between(0.32, 0.8)
        out.append(dict(litter_piece(rng), at=[math.cos(a) * d, math.sin(a) * d, 0.005]))
    return out


def person(rng, kind=None, ch='dense', pose=None, h=None, phase=None, man=None):
    """A person's make-up (people.person): dress, height, skin, colours, gait and what is on their head."""
    from .people import ANKARA, DRESS, PLAIN, SKIN
    kind = kind or rng.pick(DRESS.get(ch, DRESS['dense']))
    woman = kind in ('wrapper',) or (kind in ('ankara', 'tshirt', 'office', 'hawker', 'school') and rng.chance(0.5))
    if man is not None:
        woman = not man
    h = h or (rng.between(1.55, 1.72) if woman else rng.between(1.65, 1.85))
    if kind == 'school':
        h = rng.between(1.2, 1.55)
    skin = rng.pick(SKIN)
    print_col = rng.pick(ANKARA)
    top = {'ankara': print_col, 'wrapper': rng.pick(ANKARA), 'buba': rng.pick(['#f4f1ea', '#c9a27a', '#1f5fa8', '#2e294e', '#7a1f1f']),
           'tshirt': rng.pick(PLAIN + ANKARA[:5]), 'kaftan': rng.pick(['#f4f1ea', '#e8dcc0', '#9ab0c8', '#3f5a3a', '#1d1d1d']),
           'agbada': rng.pick(['#f4f1ea', '#1f3f8a', '#4a2a55', '#c9a13b', '#2e7d4f']), 'school': '#f4f1ea', 'office': rng.pick(['#f4f1ea', '#bcd9e6', '#e8dcc0']),
           'hawker': rng.pick(ANKARA)}[kind]
    top_mat = 'ankara' if kind in ('ankara', 'wrapper', 'hawker', 'agbada') and not (kind == 'agbada' and rng.chance(0.5)) else 'cloth'
    bottom = {'ankara': print_col, 'buba': top, 'tshirt': rng.pick(['#2f3d4c', '#1f3f8a', '#1d1d1d', '#6d5d44']), 'school': rng.pick(['#1f3f8a', '#6d5d44', '#2e7d4f']),
              'office': rng.pick(['#1d1d1d', '#2f3d4c']), 'kaftan': top, 'agbada': top, 'wrapper': rng.pick(ANKARA), 'hawker': rng.pick(ANKARA)}[kind]
    walk = pose if pose is not None else rng.chance(0.6)
    sw = (0.32 if phase is not None else rng.between(0.25, 0.4)) if walk else 0.03
    ph = phase if phase is not None else rng.pick([1, -1])
    long_dress = kind in ('wrapper', 'kaftan', 'agbada') or (woman and kind in ('ankara', 'hawker') and rng.chance(0.6))
    shoes = [rng.pick(['#1d1d1d', '#5a3a28', '#e8e2d6']) for s in (-1, 1)]
    if kind == 'wrapper' or (woman and rng.chance(0.45)):
        head = dict(gele=[rng.pick(ANKARA + ['#c9a13b']), rng.pick(ANKARA)])
    elif kind in ('buba', 'agbada') or (not woman and rng.chance(0.15)):
        head = dict(fila=rng.pick(['#7a1f1f', '#2e294e', '#c9a13b', '#1d1d1d', '#f4f1ea']))
    else:
        head = dict(hair='#141210')
    out = dict(kind=kind, h=h, skin=skin, top=top, top_mat=top_mat, bottom=bottom, swing=sw, phase=ph, long_dress=long_dress, shoes=shoes, head=head)
    if kind == 'hawker':
        out['tray'] = dict(col=rng.pick(['#c9ced2', '#2f6fae', '#c62828']), goods=[])
        for _ in range(rng.randrange(5, 12)):
            out['tray']['goods'].append([rng.between(-0.22, 0.22), rng.between(-0.22, 0.22), rng.pick(['#ff7043', '#fdd835', '#7cb342', '#ffffff', '#e8f0f4', '#c62828'])])
    if kind == 'school':
        out['satchel'] = rng.pick(['#c62828', '#1f5fa8', '#3a3a3a'])
    return out


# ---------------------------------------------------------------- goods (goods.py): every item as a leaf record
def _sack(rng, scale):
    from .goods import PRINT, SACK
    c = rng.between(0.1, 0.14) * scale
    col = rng.pick(SACK + ['#f1ede4', '#f1ede4'])
    band_c, block = rng.pick(PRINT), rng.pick(PRINT)
    two = rng.chance(0.5)
    return dict(k='sack', s=scale, c=c, col=col, band=band_c, block=block, two=two), c * 1.8


def _bale(rng, scale, col=None):
    from .goods import BALE
    a, b, c = rng.between(0.45, 0.6) * scale, rng.between(0.32, 0.42) * scale, rng.between(0.3, 0.42) * scale
    col = col or rng.pick(BALE)
    f = rng.between(0.85, 1.1)
    bands = [rng.between(-0.55, -0.35), rng.between(0.35, 0.55)]
    return dict(k='bale', a=a, b=b, c=c, col=col, shade=f, bands=bands), c * 1.7


def _sack_open(rng, scale):
    from .goods import PRODUCE, SACK
    w, d, h = rng.between(0.45, 0.6) * scale, rng.between(0.38, 0.5) * scale, rng.between(0.4, 0.6) * scale
    col = rng.pick(SACK + ['#f1ede4'])
    produce = PRODUCE[rng.pick(list(PRODUCE))]
    tin = rng.between(-0.08, 0.08) if rng.chance(0.6) else None
    return dict(k='sack_open', w=w, d=d, h=h, col=col, produce=produce, tin=tin), h + 0.05


def _bag(rng, col=None, s=1.0):
    from .goods import BAG
    col = col or rng.pick(BAG)
    w, d, hh = rng.between(0.2, 0.32) * s, rng.between(0.16, 0.24) * s, rng.between(0.2, 0.32) * s
    return dict(k='bag', col=col, w=w, d=d, h=hh, s=s), hh


def _crate(rng, col=None, bottles=True):
    from .goods import BOTTLE, CRATE
    col = col or rng.pick(CRATE)
    out = dict(k='crate', col=col, bottles=None)
    if bottles:
        bc = rng.pick(BOTTLE)
        cap = rng.pick(['#c62828', '#d9b44a', '#e8e4dc', '#1f6fb8'])
        out['bottles'] = dict(col=bc, cap=cap, mask=[rng.chance(0.85) for i in range(4) for j in range(3)])
    return out


def _carton(rng, s):
    from .goods import CARTON, PRINT, WHITE_CARTON
    white = rng.chance(0.4)
    col = rng.pick(WHITE_CARTON if white else CARTON)
    f = rng.between(0.85, 1.05)
    pc = rng.pick(PRINT)
    dx = [rng.between(-0.05, 0.05) for sy in (-1, 1)]
    return dict(k='carton', size=list(s), col=col, shade=f, print=pc, dx=dx, white=white)


def _at(leaf, M):
    leaf['at'] = place(M)
    return leaf


def _item(kind, M, rng, scale=1.0, cols=None):
    """One item standing at M (goods._item): its leaves and its height."""
    from .goods import CLOTH, CRATE, PLASTIC
    out = []
    if kind == 'bales':
        leaf, h = _bale(rng, scale, rng.pick(cols) if cols else None)
        out.append(_at(leaf, M))
        if rng.chance(0.35):
            M2 = M @ Matrix.Translation((rng.between(-0.1, 0.1), 0, h * 0.85)) @ Matrix.Rotation(rng.between(1.2, 1.9), 4, 'Z')
            c2 = rng.pick(cols) if cols else None
            leaf, h2 = _bale(rng.child('top'), scale * 0.85, c2)
            out.append(_at(leaf, M2))
            h += h2 * 0.85
        return out, h
    if kind == 'sacks':
        if rng.chance(0.55):
            h = 0
            for k in range(rng.randrange(1, 4)):
                Mk = M @ Matrix.Translation((rng.between(-0.06, 0.06), rng.between(-0.04, 0.04), h)) @ Matrix.Rotation(rng.between(-0.2, 0.2), 4, 'Z')
                leaf, hk = _sack(rng.child('s', k), scale)
                out.append(_at(leaf, Mk))
                h += hk * 0.92
            return out, h
        leaf, h = _sack_open(rng, scale)
        return [_at(leaf, M)], h
    if kind == 'nylon_bags':
        h = 0
        for k in range(rng.randrange(2, 5)):
            Mk = M @ Matrix.Translation((rng.between(-0.2, 0.2), rng.between(-0.12, 0.12), 0)) @ Matrix.Rotation(rng.between(-1, 1), 4, 'Z')
            c = rng.pick(cols) if cols else None
            leaf, hk = _bag(rng.child('b', k), c)
            out.append(_at(leaf, Mk))
            h = max(h, hk)
        return out, h
    if kind == 'crates':
        n = rng.randrange(1, 5)
        c = rng.pick(CRATE)
        for k in range(n):
            Mk = M @ Matrix.Translation((0, 0, k * 0.29)) @ Matrix.Rotation(rng.between(-0.08, 0.08), 4, 'Z')
            ck = c if rng.chance(0.7) else None
            bottles = (k == n - 1) or rng.chance(0.3)
            out.append(_at(_crate(rng.child('c', k), ck, bottles), Mk))
        return out, n * 0.29 + 0.07
    if kind == 'plastics':
        c = rng.pick(PLASTIC)
        pick = rng.between(0, 1)
        if pick < 0.35:
            n = rng.randrange(4, 10)
            cs = [c if rng.chance(0.7) else rng.pick(PLASTIC) for k in range(n)]
            return [_at(dict(k='basins', cols=cs), M)], n * 0.045 + 0.12
        if pick < 0.65:
            n = rng.randrange(3, 8)
            return [_at(dict(k='buckets', col=c, n=n), M)], (n - 1) * 0.07 + 0.3 + 0.12
        for k in range(rng.randrange(1, 4)):
            Mk = M @ Matrix.Translation((rng.between(-0.08, 0.08), k * 0.2 - 0.2, 0)) @ Matrix.Rotation(rng.between(-0.3, 0.3), 4, 'Z')
            out.append(_at(dict(k='jerrycan', col=rng.pick(['#e8b923', '#e8b923', '#e8b923', '#1f6fb8', '#e8e4dc'])), Mk))
        return out, 0.47
    if kind == 'cloth':
        n = rng.randrange(3, 10)
        for k in range(n):
            mat = 'ankara' if rng.chance(0.7) else 'cloth'
            Mk = M @ Matrix.Translation((rng.between(-0.03, 0.03), rng.between(-0.03, 0.03), k * 0.06 + 0.03)) @ Matrix.Rotation(rng.between(-0.15, 0.15), 4, 'Z')
            out.append(_at(dict(k='fold', mat=mat, col=rng.pick(CLOTH)), Mk))
        return out, n * 0.06
    if kind == 'cartons':
        h = 0
        for k in range(rng.randrange(1, 4)):
            s = (rng.between(0.35, 0.6), rng.between(0.3, 0.45), rng.between(0.25, 0.45))
            Mk = M @ Matrix.Translation((0, 0, h)) @ Matrix.Rotation(rng.between(-0.2, 0.2), 4, 'Z')
            out.append(_at(_carton(rng.child('k', k), s), Mk))
            h += s[2]
        return out, h
    return out, 0.0


def tarp(x0, x1, y0, y1, z, drop, col, rng, side=1):
    return dict(k='tarp', x0=x0, x1=x1, y0=y0, y1=y1, z=z, drop=drop, col=col, ph=[rng.between(0, math.tau) for _ in range(4)], side=side)


def band(x0, x1, y_wall, depth, z0, kinds, fill, rng, side=1, tarp_over=False, cols=None):
    """Goods along a wall (goods.band) as leaves."""
    from .goods import TARP
    out = []
    if not kinds or fill <= 0:
        return out
    rows = max(1, round(depth / 0.45))
    tops = []
    for r in range(rows):
        y = y_wall - side * (0.3 + r * depth / rows)
        x = x0 + rng.between(0.0, 0.3)
        while x < x1 - 0.3:
            step = rng.between(0.45, 0.8)
            if rng.chance(fill * (1.0 - 0.35 * r / rows)):
                kind = rng.pick(kinds)
                M = Matrix.Translation((x + step / 2, y + rng.between(-0.08, 0.08), z0)) @ Matrix.Rotation(rng.between(-0.35, 0.35), 4, 'Z')
                lv, h = _item(kind, M, rng.child('item', r, round(x, 2)), scale=1.0 if r == 0 else 0.85, cols=cols)
                out += lv
                if r == 0 and kind in ('sacks', 'cartons', 'crates', 'nylon_bags') and rng.chance(fill * 0.6):
                    M2 = M @ Matrix.Translation((rng.between(-0.08, 0.08), 0, h)) @ Matrix.Rotation(rng.between(-0.4, 0.4), 4, 'Z')
                    out += _item(kind, M2, rng.child('top', round(x, 2)), 0.9, cols=cols)[0]
                tops.append(h)
            x += step
    if tarp_over and tops:
        col = rng.pick(TARP)
        out.append(tarp(x0, x1, y_wall - side * depth, y_wall, z0 + max(tops) * 0.9, 0.5, col, rng.child('tarp'), side=-side))
    return out


def hanging(x0, x1, y, z, kinds, fill, rng):
    """Things hung from a lean-to's front plate (goods.hanging) as leaves."""
    from .goods import CLOTH
    out = []
    if not kinds or fill <= 0:
        return out
    x = x0 + 0.2
    while x < x1 - 0.2:
        if rng.chance(fill):
            kind = rng.pick(kinds)
            if kind == 'cloth':
                L = rng.between(0.6, 1.3)
                c = rng.pick(CLOTH)
                out.append(dict(k='cloth_hang', x=x, y=y, z=z, L=L, col=c, dy=rng.between(-0.03, 0.03)))
            else:
                for k in range(rng.randrange(2, 6)):
                    zz = z - 0.15 - k * rng.between(0.12, 0.2)
                    M = Matrix.Translation((x + rng.between(-0.1, 0.1), y + rng.between(-0.05, 0.05), zz - 0.3)) @ Matrix.Rotation(rng.between(-1, 1), 4, 'Z')
                    out.append(_at(_bag(rng.child('hb', k), None, 0.8)[0], M))
                out.append(dict(k='string', x=x, y=y, z=z))
        x += rng.between(0.35, 0.7)
    return out


def heap(x, y, r, z0, kinds, rng, tarp_col=None, cols=None):
    """A heap of goods (goods.heap) as leaves."""
    out = []
    n = max(3, int(r * r * (3 if kinds == ['bales'] else 12)))
    for k in range(n):
        a, q = rng.between(0, math.tau), r * math.sqrt(rng.between(0, 1))
        zz = z0 + (1 - q / r) * 0.35 * rng.between(0.3, 1.0)
        kind = rng.pick(kinds)
        M = Matrix.Translation((x + math.cos(a) * q, y + math.sin(a) * q, zz)) @ Matrix.Rotation(rng.between(-1, 1), 4, 'Z')
        out += _item(kind, M, rng.child('heap', k), 0.9, cols=cols)[0]
    if tarp_col:
        out.append(tarp(x - r * 0.8, x + r * 0.6, y - r * 0.5, y + r * 0.7, z0 + 0.7, 0.55, tarp_col, rng.child('tarp'), side=-1))
    return out


def relative(leaves, z0):
    """Goods leaves on the ground: their heights as offsets from the ground under the heap (the kit puts them back on it)."""
    for lf in leaves:
        if 'at' in lf:
            lf['at'][2] -= z0
        elif lf['k'] == 'tarp':
            lf['z'] -= z0
    return leaves


# ---------------------------------------------------------------- gutters (gutters.py)
def gutter(pts, g, keep, wear=0.6):
    """Every piece of a gutter: its walls' dirt, what is inside it, and each slab over it."""
    from .gutters import PIECE, RUBBISH, pieces
    w = g['w']
    rng = Rng('gutter', g['id'])
    proud = 0.12 + 0.1 * min(1.0, g.get('depth', 0.6))
    blocked = g.get('blocked') or []
    covered = g['state'] == 'covered'
    out = []
    for a, b, s in pieces(pts, keep, 4.0 if detail.web() else PIECE):
        L = math.dist(a, b)
        if L < 0.05:
            continue
        rec = dict(ww=wear * rng.between(0.7, 1.2))
        fill = next((bk['fill'] for bk in blocked if bk['from'] <= s + L / 2 < bk['to']), None)
        if not (covered and detail.web()):
            ins = {}
            if fill == 'rubbish':
                ins['rubbish'] = []
                for _ in range(int(L * 6)):
                    u, o = rng.between(0, L), rng.between(-w / 2, w / 2)
                    z = proud * rng.between(0.7, 1.15)
                    c = rng.pick(RUBBISH)
                    sz = [rng.between(0.06, 0.2), rng.between(0.04, 0.14), rng.between(0.01, 0.05)]
                    ins['rubbish'].append(dict(u=u, o=o, z=z, col=list(c), size=sz, rz=rng.between(0, 3.14), rx=rng.between(-0.6, 0.6)))
            else:
                green = fill == 'green_water'
                ins['zw'] = proud * (0.75 if green else rng.between(0.25, 0.45))
                ins['mix'] = [rng.between(0.2, 0.7) if green else rng.between(0.0, 0.5) for _ in range(4)]
                ins['caught'] = []
                if not covered and rng.chance(0.25 * wear):
                    for _ in range(rng.randrange(1, 4)):
                        u, o = rng.between(0.2, L - 0.2), rng.between(-w / 3, w / 3)
                        rz = rng.between(0, 3.14)
                        c = rng.pick(RUBBISH)
                        ins['caught'].append(dict(u=u, o=o, rz=rz, col=list(c), size=[rng.between(0.1, 0.25), rng.between(0.06, 0.15), 0.04]))
            rec['inside'] = ins
        if covered:
            rec['slabs'] = _slabs(L, w, rng, wear, g)
        out.append(rec)
    return out


def _slabs(L, w, rng, wear, g):
    from .gutters import RUBBISH
    n = max(1, round(L / (1.2 if detail.web() else 0.6)))
    rock = g.get('rock', 0.0)
    out = []
    for k in range(n):
        if rng.chance(g.get('open_share', 0.0)):
            out.append(dict(gone=True))
            continue
        tip = rng.between(-0.08, 0.08) if rng.chance(0.15 + 0.3 * wear + 0.5 * rock) else 0.0
        roll = rng.between(-0.06, 0.06) * rock
        sink = rng.between(0.02, 0.08) if rng.chance(0.1 + 0.2 * wear + 0.3 * rock) else 0.0
        dirt, dust, sh = rng.between(0.1, 0.5), rng.between(0.6, 1.0), rng.between(0.8, 1.05)
        gap = 0.03 + rng.between(0.0, 0.06) * rock
        s = dict(tip=tip, roll=roll, sink=sink, dirt=dirt, dust=dust, shade=sh, gap=gap, broken=None)
        broken = rng.pick(['split', 'corner']) if rng.chance(g.get('broken', 0.0)) else None
        if broken == 'split':
            s['broken'] = dict(split=[rng.between(0.35, 0.65), rng.between(-0.06, 0.06), rng.between(-0.06, 0.06)])
        elif broken == 'corner':
            s_ = rng.pick([-1, 1])
            s['broken'] = dict(corner=[s_, rng.between(0.15, 0.3), rng.between(-0.5, 0.5), rng.between(-0.5, 0.5)])
        if g.get('litter', 0.0) > 0:
            s['joint'] = []
            for _ in range(int(rng.between(0, 4) * g['litter'])):
                o = rng.between(-w / 2 - 0.12, w / 2 + 0.12)
                sz = [rng.between(0.05, 0.16), rng.between(0.04, 0.1), rng.between(0.008, 0.03)]
                du, rz, rx = rng.between(-0.05, 0.05), rng.between(0, 3.14), rng.between(-0.5, 0.5)
                s['joint'].append(dict(o=o, size=sz, du=du, rz=rz, rx=rx, col=list(rng.pick(RUBBISH))))
        out.append(s)
    return out


# ---------------------------------------------------------------- the old town kit's own parts (oldtown.py)
def leanto(sp, side, rng):
    """A lean-to's records: its sheet slope and its uprights (each post's x along, lean, shade)."""
    from .oldtown import STATE_WEAR, leanto_frame
    A, B, C, D, spec = leanto_frame(sp, side)
    wr = STATE_WEAR.get(sp.get('roof_state'), 0.6)
    slope = zinc_slope(A, B, C, D, spec, lambda i: max(0.0, min(1.0, wr + rng.child('sheet', i).between(-0.25, 0.25))))
    x0, x1 = sp['x0'], sp['x1']
    n = max(1, math.ceil((x1 - x0) / 2.8))
    posts = []
    for k in range(n + 1 if sp.get('posts', 'timber') != 'none' else 0):
        posts.append(dict(x=x0 + 0.1 + (x1 - x0 - 0.2) * k / n, lean=rng.between(-0.04, 0.04), shade=rng.between(0.85, 1.15)))
    return dict(sheets=[slope], uprights=posts)


def plank_stall(sp, rng):
    x0, x1, y0, y1, h = sp['x0'], sp['x1'], sp['y0'], sp['y1'], sp['h']
    out = dict(boards=[])
    for (ax, ay), (bx, by), top in (((x0, y1), (x1, y1), h), ((x0, y0), (x0, y1), h), ((x1, y0), (x1, y1), h), ((x0, y0), (x1, y0), 1.05)):
        n = max(1, round((top - 0.35) / 0.22))
        out['boards'].append([rng.between(0.75, 1.15) for k in range(n)])
    if sp.get('goods') == 'sacks_on_top':
        out['sacks'] = []
        nx_, ny_ = max(1, int((x1 - x0) / 0.85)), max(1, int((y1 - y0) / 0.55))
        for i in range(nx_):
            for j in range(ny_):
                z = h + 0.03
                for k in range(rng.randrange(1, 3)):
                    off = 0.2 if k % 2 else 0.0
                    M_ = Matrix.Translation((x0 + (i + 0.5) * (x1 - x0) / nx_ + off * rng.between(-1, 1), y0 + (j + 0.5) * (y1 - y0) / ny_, z)) @ Matrix.Rotation(rng.between(-0.15, 0.15), 4, 'Z')
                    leaf, hk = _sack(rng.child('sk', i, j, k), 1.0)
                    out['sacks'].append(_at(leaf, M_))
                    z += hk * 0.9
    if sp.get('tarp_colour'):
        r = rng.child('tarp')   # goods.tarp's four fold phases
        out['tarp_ph'] = [r.between(0, math.tau) for _ in range(4)]
    return out


def display_cabinet(w, h, rng):
    from .oldtown import SNACKS
    shelves = []
    for z0 in (0.025, h * 0.5 + 0.006):
        items = []
        x = -w / 2 + 0.04
        while x < w / 2 - 0.08:
            c = rng.pick(SNACKS)
            kind = rng.between(0, 1)
            if kind < 0.5:
                pw, ph = rng.between(0.06, 0.11), rng.between(0.12, 0.2)
                items.append(dict(k='packet', col=c, w=pw, h=ph, rz=[rng.between(-0.1, 0.1) for row in (-1, 1)]))
                x += pw + 0.01
            elif kind < 0.8:
                items.append(dict(k='bottle', col=c))
                x += 0.07
            else:
                items.append(dict(k='tins', col=c))
                x += 0.09
        shelves.append(items)
    return shelves


def cage_stall(sp, rng):
    """A cage stall's records (oldtown.cage_stall): its bars on each side, its top's boards, its goods on the counter and shelves."""
    x0, x1, y0, y1, h = sp['x0'], sp['x1'], sp['y0'], sp['y1'], sp['h']
    left = y0 > 0
    yf, yb = (y0, y1) if left else (y1, y0)
    bars = {}
    for name, L in (('front', x1 - x0), ('start', abs(y1 - y0)), ('end', abs(y1 - y0))):
        us, u = [], 0.12
        while u < L - 0.08:
            us.append(round(u, 3))
            u += sp.get('bar_pitch_m', 0.12) * rng.between(0.9, 1.1)
        bars[name] = us
    top = [rng.between(0.78, 1.05) for k in range(max(2, round((x1 - x0) / 0.3)))]
    kinds, fill = sp.get('goods_kinds', ['cartons', 'plastics']), sp.get('goods_fill', 0.7)
    gd = []
    sgn = 1 if left else -1
    for k, z in enumerate([0.78] + list(sp.get('shelves', []))):
        gd += band(x0 + 0.1, x1 - 0.1, yb, abs(y1 - y0) * (0.55 if k else 0.8), z, kinds, fill, rng.child('shelf', k), side=sgn, cols=sp.get('goods_colours'))
    return dict(bars=bars, top_shades=top, goods=gd)   # heights over the ground under the stall


def glass_cabinet(w, h, n, rng):
    """A glass cabinet's shelves (oldtown.glass_cabinet): each shelf's row of packets, bottles and tins from the left."""
    from .oldtown import SNACKS
    shelves = []
    for r in range(n):
        items, x = [], -w / 2 + 0.06
        while x < w / 2 - 0.1:
            c, kind = rng.pick(SNACKS), rng.between(0, 1)
            if kind < 0.5:
                pw, ph = rng.between(0.06, 0.11), min(h / n - 0.05, rng.between(0.12, 0.2))
                items.append(dict(k='packet', col=c, w=pw, h=ph, rz=[rng.between(-0.1, 0.1)]))
                x += pw + 0.01
            elif kind < 0.8:
                items.append(dict(k='bottle', col=c))
                x += 0.07
            else:
                items.append(dict(k='tins', col=c))
                x += 0.09
        shelves.append(items)
    return shelves


def drinks_fridge(h, rng):
    W = 0.7
    shelves = []
    for r in range(4):
        row = []
        x = -W / 2 + 0.1
        while x < W / 2 - 0.1:
            c = rng.pick(['#c62828', '#2e9a46', '#f9a825', '#3b2414', '#1f6fb8', '#e07b20', '#bfc9b8'])
            row.append(dict(col=c, k='bottle' if rng.chance(0.7) else 'can'))
            x += 0.075
        shelves.append(row)
    return dict(contents=shelves, side_posters=[rng.pick(['#1f6fb8', '#2e9a46', '#e07b20']) for sx in (-1, 1)])


def breeze_cells(a, b, z0, z1, rng, cell=0.4):
    L = math.dist(a, b)
    nx, nz = max(1, round(L / cell)), max(1, round((z1 - z0) / cell))
    return [[rng.between(0.9, 1.05) for j in range(nz)] for i in range(nx)]


def plain_wall_bays(line, h, wear, rng, skip=None, broken=0.0, streaks=0.0, foot_stain=0.0):
    """A plain wall's 1.2 m bays (oldtown.plain_wall): each bay's blotch, cement patch, mould runs, damp foot and broken render."""
    out = []
    for i in range(len(line) - 1):
        a, b = line[i], line[i + 1]
        L = math.dist(a, b)
        n = max(1, round(L / 1.2))
        for k in range(n):
            u0, u1 = L * k / n, L * (k + 1) / n
            pa = (a[0] + (b[0] - a[0]) * u0 / L, a[1] + (b[1] - a[1]) * u0 / L)
            pb = (a[0] + (b[0] - a[0]) * u1 / L, a[1] + (b[1] - a[1]) * u1 / L)
            if skip and skip(pa, pb):
                continue
            w = u1 - u0
            bay = dict(blot=rng.between(0, 1), patch=None, streaks=[], foot=[], broken=None)
            if rng.chance(0.25 * wear):
                bay['patch'] = [rng.between(-w / 2 + 0.2, w / 2 - 0.4), rng.between(0.4, h - 0.6)]
            for _ in range(int(streaks * rng.between(4, 10))):
                x, sw = rng.between(-w / 2 + 0.05, w / 2 - 0.05), rng.between(0.06, 0.3)
                zb = h - rng.between(0.3, h * 0.85)
                dark = rng.between(0.25, 0.5)
                ys = [rng.between(0, 0.0015) for side in (-1, 1)]
                bay['streaks'].append(dict(x=x, w=sw, zb=zb, dark=dark, y=ys))
            if foot_stain > 0:
                for j in range(4):
                    bay['foot'].append([foot_stain * rng.between(0.5, 1.2), foot_stain * rng.between(0.5, 1.2)])
            if rng.chance(broken):
                bw, bh = rng.between(0.4, w - 0.1), rng.between(0.35, 1.2)
                x = rng.between(-w / 2 + bw / 2, w / 2 - bw / 2)
                z = rng.pick([rng.between(0.05, 0.4), rng.between(0.4, h - bh - 0.1)])
                sides = []
                for side in (-1, 1):
                    sd = dict(shade=rng.between(0.45, 0.6), bites=[])
                    for _ in range(3):
                        ex, ez = rng.between(-bw / 2, bw / 2), rng.pick([z, z + bh])
                        ew, eh = rng.between(0.08, 0.25), rng.between(0.05, 0.15)
                        sd['bites'].append([ex, ez, ew, eh])
                    sides.append(sd)
                bay['broken'] = dict(w=bw, h=bh, x=x, z=z, sides=sides)
            out.append(bay)
    return out


def posters(wall, rng):
    from .oldtown import POSTER
    for k, p in enumerate(wall.get('posters', [])):
        r = rng.child('poster', k)
        p['colours'] = [r.pick(POSTER), r.pick(POSTER), r.pick(POSTER)]
        p['torn'] = r.chance(0.5)
        bands = [(0.0, 0.18), (0.18, 0.62), (0.62, 0.8), (0.8, 1.0)]
        p['shades'] = [None if p['torn'] and a_ < 0.1 else r.between(0.75, 0.95) for a_, b_ in bands]


# ---------------------------------------------------------------- one spot
def building(b):
    """Draft a building's records: the paint blotch, shopfront planks, a window spot on every face (with its height and
    any AC box beside it), the breeze screen's blocks, the scaffold's members, the stains on every face, the roof's sheets."""
    from . import parts
    from .oldtown import STATE_WEAR, _on_face, faces, rects
    rng = Rng('oldtown', b['id'])
    poly = ccw([tuple(p) for p in b['footprint']])
    wf = b.setdefault('wall_finish', {})
    roof = b.get('roof', {})
    flat = roof.get('type', 'hip_zinc') == 'flat_parapet'
    storeys = b.get('storeys', 1)
    if b.get('storey_h_m'):
        sh = list(b['storey_h_m'])
    else:
        H0 = b.get('wall_h_m', storeys * parts.STOREY)
        sh = [H0 / storeys] * storeys
    H = sum(sh)
    levels = [sum(sh[:k]) for k in range(storeys)]
    wear = b.get('wear', 0.65)
    paint = hex_rgb(wf.get('wall_colour') or '#d8cfbf')
    wf['blotch'] = blotch((round(poly[0][0], 1), round(poly[0][1], 1)))
    fs = faces(poly)
    street_side = -1 if b.get('side') == 'left' else 1
    on_street = lambda n: n[1] * street_side > 0.7
    taken = {i: [] for i in range(len(fs))}
    openings = {i: [] for i in range(len(fs))}
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
        u = (xm - (A[0] + B[0]) / 2) / dx
        w = (s['to_x'] - s['from_x']) / abs(dx)
        if s['door'] == 'plank_shutter':
            r = rng.child('shop', s['from_x'])
            n = max(2, round(w / 0.16))
            s['planks'] = [[r.between(0.82, 1.12), r.between(-0.15, 0.2)] for i in range(n)]
        taken[k].append((u - w / 2 - 0.3, u + w / 2 + 0.3))
        openings[k].append(('door', u, 1.2, w, 2.4, False))
    ac = b.get('ac_units', 0.0)
    ac = ac if isinstance(ac, (int, float)) else 0.0
    spots, acs = [], []

    def window(F, u, z, k, storey):
        openings[k].append(('window', u, z, 1.0, 1.15, False))
        p = F @ Vector((u, 0, 0))
        spots.append(dict(x=p.x, y=p.y, storey=storey, z=z))
        r_ = rng.child('ac', k, round(u, 1), round(z, 1))
        if r_.chance(ac):
            s_ = r_.pick((-1, 1))
            q = F @ Vector((u + s_ * 1.05, 0, 0))
            acs.append(dict(x=q.x, y=q.y, z=z - 0.55, face=k, shade=r_.between(0.8, 1.0), pipe=[u + s_ * 0.7 - (u + s_ * 1.05), z - 0.6, max(0.3, z - 2.6)]))

    gf_runs = (b.get('ground_floor_front') or {}).get('runs', [])
    if b.get('window_spots') is not None:
        for sp in b['window_spots']:
            hit = _on_face(fs, sp['x'], sp['y'])
            if hit:
                k, u, _ = hit
                window(fs[k][4], u, levels[sp.get('storey', 0)] + 1.5, k, sp.get('storey', 0))
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
                    window(F, u, levels[st] + min(1.55, sh[st] * 0.55), k, st)
    b['window_spots'] = spots
    b['ac_units'] = acs
    for run in gf_runs:
        (ax, ay), (bx, by) = run['a'], run['b']
        off = run.get('out', 0.05)
        n = (0, 1) if b.get('side') == 'right' else (0, -1)
        a2, b2 = (ax + n[0] * off, ay + n[1] * off), (bx + n[0] * off, by + n[1] * off)
        if run.get('screen') == 'breeze_block':
            if b.get('side') == 'right':
                a2, b2 = b2, a2
            run['cells'] = breeze_cells(a2, b2, 0.0, run.get('h', sh[0] - 0.05), rng.child('breeze'))
    sc = b.get('scaffold')
    if sc:
        out_ = sc.get('out_m', 0.9)
        top = sc.get('h_m', H + 1.0)
        sc['tubes'], sc['boards'] = [], []
        tube = lambda a, b_, r, f=1.0: sc['tubes'].append([a.x, a.y, a.z, b_.x, b_.y, b_.z, r, f])
        for k, (A, B, L, n, F) in enumerate(fs):
            if not on_street(n):
                continue
            dx = (B[0] - A[0]) / L
            ua, ub = sorted(((sc.get('from_x', -1e9) - (A[0] + B[0]) / 2) * dx, (sc.get('to_x', 1e9) - (A[0] + B[0]) / 2) * dx))
            ua, ub = max(ua, -L / 2), min(ub, L / 2)
            if ub - ua < 1.0:
                continue
            nb = max(1, round((ub - ua) / 2.0))
            us = [ua + (ub - ua) * j / nb for j in range(nb + 1)]
            lifts = [z for z in (2.0 * i for i in range(1, int(top / 2.0) + 1))]
            r_ = rng.child('scaffold', k)
            for u in us:
                for o in (0.25, out_):
                    a_ = F @ Vector((u, o, 0.0))
                    b_ = F @ Vector((u + r_.between(-0.04, 0.04), o, top))
                    tube(a_, b_, 0.05, r_.between(0.8, 1.1))
            for z in lifts:
                for o in (0.25, out_):
                    tube(F @ Vector((ua, o, z)), F @ Vector((ub, o, z)), 0.045)
                for u in us:
                    tube(F @ Vector((u, 0.02, z + 0.05)), F @ Vector((u, out_ + 0.1, z + 0.05)), 0.04)
                if r_.chance(sc.get('planks', 0.4)):
                    sc['boards'].append(dict(face=k, u=(ua + ub) / 2, o=(0.25 + out_) / 2, z=z + 0.1, len=ub - ua, depth=out_ - 0.15, shade=r_.between(0.8, 1.1)))
            for j in range(nb):
                if j % 2 == 0:
                    tube(F @ Vector((us[j], out_ + 0.06, 0.2)), F @ Vector((us[j + 1], out_ + 0.06, min(top, 2.0 * 2))), 0.04)
                    if top > 6:
                        tube(F @ Vector((us[j + 1], out_ + 0.06, 4.0)), F @ Vector((us[j], out_ + 0.06, min(top, 8.0))), 0.04)
    stains = wf.get('stains', 'none')
    b['stains'] = []
    if stains != 'none':
        for k, (A, B, L, n, F) in enumerate(fs):
            for rep_ in range(2 if stains == 'heavy' else 1):
                for m in age_face(L, H, wear, paint, openings[k], levels[1:], rng.child('stains', k, rep_), flat_top=flat):
                    b['stains'].append(dict(m, face=k))
    if flat:
        oct_ = chamfer(poly, 0.18)
        roof['slab_blotch'] = slab_blotch(offset(oct_, -0.18))
    elif roof.get('form') == 'mono':
        from .oldtown import mono_frame
        sp_, side = mono_frame(b, poly, H)
        roof.update(leanto(sp_, side, rng.child('mono')))
    else:
        longspan = roof.get('type', 'hip_zinc') == 'longspan'
        state = roof.get('roof_state', 'rusty')
        rw = STATE_WEAR.get(state, 0.7)
        roof['sheets'] = []
        for q in rects(poly):
            rs = dict(form=roof.get('form', 'hip'), pitch_deg=roof.get('pitch_deg', 15), overhang=roof.get('eave_depth_m', 0.6),
                      profile='trapezoid' if longspan else 'sine', pitch=0.2 if longspan else 0.076, depth=0.032 if longspan else 0.018,
                      mixed=state == 'rusty', wear=rw)
            roof['sheets'].append(roof_pitched(ccw(q), H, rs, rng.child('roof', q[0])))


def frontage(e):
    rng = Rng('oldtown', e['id'])
    kind = e['frontage_edge']
    if kind in ('platform_house', 'leanto_to_road', 'shop_line_step'):
        x0, x1 = e['from_x'], e['to_x']
        e['chips'] = []
        for k in range(int((x1 - x0) / 3)):
            x = rng.between(x0 + 0.5, x1 - 0.5)
            e['chips'].append([x, rng.between(0.2, 0.6)])
    elif kind == 'wall_gate':
        wall = e['wall']
        g = e.get('gate') or {}
        line = [tuple(p) for p in e['line']]
        gx0, gx1 = g.get('from_x', 1e9), g.get('to_x', -1e9)
        skip = lambda pa, pb: (pa[0] + pb[0]) / 2 > gx0 - 0.05 and (pa[0] + pb[0]) / 2 < gx1 + 0.05
        wear = 0.85 if wall.get('state') == 'mouldy' else 0.5
        wall['bays'] = plain_wall_bays(line, wall.get('h', 2.2), wear, rng.child('wall'), skip=skip, broken=wall.get('render_broken', 0.0),
                                       streaks=wall.get('mould_streaks', 0.0), foot_stain=wall.get('foot_stain_m', 0.0))
        posters(wall, rng.child('marks'))


def street(sp, base_dir):
    """Draft a street piece's records: the ground grids (a file beside the map), the litter, the apron's pieces, the
    gutter's pieces and the crossing slabs; on a street without a ground sheet, the tar strips' frayed edges."""
    rng = Rng('oldtown', sp['id'])
    (x0, cy), (x1, _) = sp['centreline'][0], sp['centreline'][-1]
    w = sp['width_m']
    yl, yr = cy + w / 2, cy - w / 2
    N = None
    if sp.get('relief') or 'tar_cover' in sp:
        grids = ground_grids(sp)
        name = f"ground_{sp['id']}.npz"
        np.savez_compressed(os.path.join(base_dir, name), **{k: np.asarray(v, np.float64) for k, v in grids.items()})
        sp['ground_grid'] = name
        N = Noise(sp)
    else:
        step = 2.0
        n = int((x1 - x0) / step)
        sp['tar_strips'] = [[rng.between(-0.25, 0.1), rng.between(-0.25, 0.1), rng.between(-0.1, 0.25), rng.between(-0.1, 0.25), rng.between(0.95, 1.05)] for k in range(n)]
        if sp.get('sand_cover') == 'edges':
            sp['sand_edges'] = [[rng.between(0.3, 0.8), rng.between(0.3, 0.8)] for k in range(n)]
    lt = sp.get('litter') or {}
    if lt and N is not None:
        lr = rng.child('litter')
        xa, xb = max(x0, lt.get('from_x', x0)), min(x1, lt.get('to_x', 60.0))
        ya, yb = cy - w / 2 - 1.2, cy + w / 2 + 0.2
        n = int(lt.get('per_m2', 0.05) * (xb - xa) * (yb - ya) * 4)
        lt['pieces'] = []
        for _ in range(n):
            x, y = lr.between(xa, xb), lr.between(ya, yb)
            edge = max(0.0, 1 - (w / 2 - abs(y - cy)) / 1.2)
            rut = float(_ruts(sp, x, y, 'depth')) / 0.05 + float(_edge_rut(sp, N, x, y)) / 0.1
            if lr.chance((1 + lt.get('walls', 3.0) * edge + lt.get('ruts', 2.0) * min(1.0, rut)) / (1 + lt.get('walls', 3.0) + lt.get('ruts', 2.0))):
                lt['pieces'].append(dict(litter_piece(lr), x=x, y=y))
    for vk in ('verge_right', 'verge_left'):
        vr = sp.get(vk) or {}
        if vr.get('surface') == 'concrete_apron':
            xa, xb = vr.get('from_x', x0), vr.get('upto_x', x1)
            n_ = max(1, int((xb - xa) / 0.5))
            vr['shades'] = [rng.between(0.85, 1.05) for k in range(n_)]
        elif vr.get('surface') == 'grass':   # the grass strip's pieces: each one's length, shade, and how far its two edges wander in
            xa, xb = vr.get('from_x', x0), vr.get('upto_x', x1)
            gr, vr['patches'], x = rng.child('grass' + vk), [], xa
            while x < xb:
                ln = gr.between(0.6, 1.6)
                vr['patches'].append([round(min(ln, xb - x), 2), gr.between(0.8, 1.15), gr.between(0.0, 0.35), gr.between(0.0, 0.6)])
                x += ln
    for side in ('left', 'right'):   # a kerb's precast blocks: each one's length, shade and a chip off its top edge
        kb = sp.get('kerb_' + side)
        if kb:
            xa, xb = kb.get('from_x', x0), kb.get('upto_x', x1)
            kr, kb['blocks'], x = rng.child('kerb' + side), [], xa
            while x < xb:
                ln = kb.get('block_m', 1.0) * kr.between(0.95, 1.05)
                kb['blocks'].append([round(min(ln, xb - x), 3), kr.between(0.85, 1.08), kr.between(0.0, 1.0) if kr.chance(kb.get('chipped', 0.2)) else 0.0])
                x += ln
    g = sp.get('gutter_left') or {}
    if g.get('type', 'none') != 'none':
        y = cy + g['offset_m']
        gg = dict(id=sp['id'] + 'L', w=g['width'], depth=g.get('depth', 0.5), state='covered' if g['type'] == 'slab_covered' else 'open',
                  blocked=[{'from': 0, 'to': 999, 'fill': 'rubbish'}] if g.get('state') == 'half_blocked' else [],
                  **{k: g[k] for k in ('slab_colour', 'dust', 'open_share', 'broken', 'rock', 'litter', 'proud_m') if k in g})
        g['pieces'] = gutter([(x0, y), (x1, y)], gg, lambda p: True, wear=g.get('wear', 0.2))
        for c in sp.get('crossings', []):
            if c.get('side') == 'left':
                c['rz'], c['shade'] = rng.between(-0.03, 0.03), rng.between(0.85, 1.0)


def _ruts(sp, x, y, key):
    from .roadbed import _smooth
    out = 0.0
    for r in sp.get('ruts', []):
        win = _smooth(r['from_x'] - 2, r['from_x'], x) * (1 - _smooth(r['to_x'], r['to_x'] + 2, x))
        out = max(out, win * math.exp(-((y - r['y']) / (r['w'] / 2)) ** 2 * 2) * r.get(key, 0.0))
    return out


def _edge_rut(sp, N, x, y):
    er = sp.get('edge_rut') or {}
    if not er:
        return 0.0
    x_ = np.asarray(x, float)
    wob = N.wob(x_)
    out = 0.0
    for s in ((-1,) if er.get('side') == 'right' else (1,) if er.get('side') == 'left' else (-1, 1)):
        yc = N.cy + s * (N.half - er.get('w_m', 0.8) * 0.3) + wob
        out = np.maximum(out, np.exp(-((y - yc) / (er.get('w_m', 0.8) / 2)) ** 2 * 2) * N.rut_k(x_))
    return out * er.get('depth_m', 0.15)


def props(P):
    """Draft the props' records: poles, trees, every trade spot's sheets, posts, goods and contents, the vehicles'
    colours, the bins' and heaps' litter, the pole posters and each person's make-up."""
    rng = Rng('oldtown', 'props')
    for k, p in enumerate(P.get('poles', [])):
        p.update(pole(rng.child('pole', k), h=p.get('h', 9.5), wood=p.get('type') == 'timber'))
        if 'lean_toward_deg' in p:   # a pole the map says leans hard one way: its lean from the map, not drafted
            t, a = math.tan(math.radians(p.get('lean_deg', 0))), math.radians(p['lean_toward_deg'])
            p['lean'] = [round(t * math.cos(a), 3), round(t * math.sin(a), 3)]
    for t in P.get('trees', []):
        t['form'] = tree(rng.child('tree', t['x']), kind=t.get('kind', 'palm'), h=t.get('h'))
    for k, s in enumerate(P.get('trade_spots', [])):
        r = rng.child('trade', k)
        side = 'left' if s.get('y', s.get('wall_y', s.get('y0', 0))) > 0 else 'right'
        if s['type'] == 'lean-to row':
            rec = leanto(s, side, r)
            sgn = 1 if side == 'left' else -1
            s['goods'] = band(s['x0'] + 0.15, s['x1'] - 0.15, s['wall_y'], s.get('goods_depth_m', 0.9), s.get('stand_z_m', 0.0),
                              s.get('goods_kinds', []), s.get('goods_fill', 0.0), r.child('goods'), side=sgn, tarp_over=s.get('goods_tarp', False), cols=s.get('goods_colours'))
            s['hung'] = hanging(s['x0'], s['x1'], s['wall_y'] - sgn * (s['depth'] - 0.08), s['z_front'] - 0.15,
                                s.get('hanging_kinds', []), s.get('hanging_fill', 0.0), r.child('hang'))
            s.update(rec)
        elif s['type'] == 'umbrella':
            s['rz'] = r.between(0, 1)
            if s.get('goods_kinds'):
                s['goods'] = heap(s['x'], s['y'], 0.5, 0.0, s['goods_kinds'], r.child('goods'), cols=s.get('goods_colours'))
        elif s['type'] == 'kiosk' and s.get('kiosk_kind') == 'plank_stall':
            s.update(plank_stall(s, r))
        elif s['type'] == 'kiosk' and s.get('kiosk_kind') == 'drinks_fridge':
            s.update(drinks_fridge(s.get('h', 1.3), r))
        elif s['type'] == 'kiosk' and s.get('kiosk_kind') == 'glass_cabinet':
            s['contents'] = glass_cabinet(s['w'], s['h'], s.get('shelf_n', 3), r)
        elif s['type'] == 'cage stall':
            s.update(cage_stall(s, r))
        elif s['type'] == 'table':
            items = s.get('items', [])
            if any(i.startswith('crate') for i in items):
                s['crate_rz'] = [r.between(-0.1, 0.1) for it in items]
                continue
            s['contents'] = [display_cabinet(min(1.1, s['w'] / len(items) - 0.1), 0.6, r.child('cab', j)) if it == 'display_cabinet' else None for j, it in enumerate(items)]
    for k, v in enumerate(P.get('parked_vehicles', [])):
        if v['kind'] == 'car':
            r = rng.child('car', k)
            ck = v.get('car_kind', 'saloon')
            if not v.get('colour'):
                v['colour'] = car_colour(r, ck)
            if ck == 'pickup' and 'load' not in v:   # vehicles.car: the load in the bed, rolled last
                v['load'] = r.pick(['#c8a96e', '#2f5fa8', '#3a3a3a']) if r.chance(0.6) else None
        if v['kind'] == 'container':
            r = rng.child('container', k)
            if v.get('tractor', False):
                v['cab_colour'] = r.pick(['#e8e6df', '#c62828', '#1f5fa8', '#e0b020', '#2e7d4f', '#d8d4cc'])
            if not v.get('colour'):
                from .vehicles import CONTAINER_COLS
                v['colour'] = r.pick(CONTAINER_COLS)
        if v['kind'] == 'okada':
            v['colour'] = okada_colour(rng.child('okada', k))
    for k, b in enumerate(P.get('bins', [])):
        b['litter'] = bin_litter(rng.child('bin', k))
    for k, pp in enumerate(P.get('pole_posters', [])):
        r = rng.child('pp', k)
        pp['sheets'] = []
        for j in range(pp.get('n', 2)):
            turn = r.between(-0.5, 0.5)
            zf = r.between(0.8, 1.2)
            pp['sheets'].append(dict(turn=turn, z=zf, colours=[r.pick(POSTER_COLS()), r.pick(POSTER_COLS())]))
    for k, hp in enumerate(P.get('heaps', [])):
        if hp['kind'] == 'rubbish':
            hp['heap'] = refuse_heap(hp['r'], rng.child('heap', k))
        elif hp['kind'] == 'blocks':   # a stack of hollow blocks: each block's nudge, turn and shade, and the gaps where one is gone
            r = rng.child('blocks', k)
            hp['blocks'] = [[round(r.between(-0.02, 0.02), 3), round(r.between(-0.02, 0.02), 3), round(r.between(-0.04, 0.04), 3), r.between(0.85, 1.1),
                             r.chance(hp.get('gone', 0.1)) if j >= hp['cols'] * hp.get('rows', 1) else False]
                            for j in range(hp['cols'] * hp.get('rows', 1) * hp['layers'])]
        elif hp['kind'] == 'goods':
            hp['goods'] = heap(hp['x'], hp['y'], hp['r'], hp.get('z_m', 0.0), hp.get('goods_kinds', ['sacks']), rng.child('heap', k), hp.get('tarp_colour'), cols=hp.get('goods_colours'))
    for k, p in enumerate(P.get('people', [])):
        p['body'] = person(rng.child('person', k), kind=p.get('kind'), h=p.get('h'), pose=p.get('walking'))
        p['kind'] = p['body']['kind']


def POSTER_COLS():
    from .oldtown import POSTER
    return POSTER


def car_colour(rng, kind='saloon'):
    if kind == 'saloon':   # vehicles.saloon's mix; the other kinds' is vehicles.car's
        return rng.pick({'#c9ced2': 4, '#1d1d1d': 3, '#f2f2ee': 3, '#2f3d4c': 2, '#7a1f1f': 2, '#6d5d44': 1})
    return rng.pick({'#c9ced2': 4, '#1d1d1d': 3, '#f2f2ee': 3, '#2f3d4c': 2, '#7a1f1f': 2, '#6d5d44': 1, '#3f5a3a': 1, '#1f4fa0': 1})


def okada_colour(rng):
    return rng.pick({'#b71c1c': 3, '#111111': 3, '#1565c0': 2, '#e8e2d6': 1})


def spot(sp, base_dir):
    """Draft every record of one spot's map, in place."""
    detail.LEVEL = 'full'
    for s in sp.get('streets', []):
        street(s, base_dir)
    for b in sp.get('buildings', []):
        building(b)
    for e in sp.get('frontage_edges', []):
        frontage(e)
    props(sp.get('props', {}))
    return sp
