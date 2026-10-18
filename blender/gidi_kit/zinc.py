"""Corrugated zinc the way Lagos roofs are: sheet by sheet.

Seen from above (the Mushin and Shomolu study) a roof is a patchwork: every sheet its own brown or grey, rust worst toward
the eave where the water sits, now and then one bright new sheet among the old, the laps showing as lines, and on old roofs
a sag between the eave and the ridge. From the street the ribs show along the eave. All of it is geometry and vertex colour,
so Unreal (which shows the vertex colour alone) sees it too. The web tiles get a coarser rib (two to a sheet) than the full
build's real 76 mm corrugation. The web tiles carry no ribs: Unreal lays its own corrugation on 'zinc' faces and the
browser's shader draws them, so the tiles spend their faces on colour instead: rust run down from each nail line and
along the sheet edges, where the water gets under.
"""
import math

from mathutils import Vector

from . import detail
from .core import Rng, hex_rgb, shade

RUST = hex_rgb('#6d4129')        # rust, a dull red-brown
RUST_DARK = hex_rgb('#3c2416')   # old rust, nearly black where it's wet longest
NEW = hex_rgb('#9da2a3')         # a new galvanised sheet, not yet rusted
COVER = 0.8                      # a sheet's width less its side lap


def _mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def sag_at(spec, t, v):
    """How far an old roof has sunk at t along the eave (0..1) and v up the slope (0..1): nothing at the edges."""
    return spec.get('sag', 0.0) * math.sin(math.pi * max(0.0, min(1.0, t))) * math.sin(math.pi * max(0.0, min(1.0, v)))


def sheets(mb, A, B, C, D, spec, wear_of=None):
    """A slope of zinc sheets: eave A->B, top D->C (C == D: a hip end). spec: col, col2, mixed, wear, pitch, depth, profile,
    and sag (metres, from the roof's age). wear_of(i): sheet i's own wear."""
    A, B, C, D = (Vector(p) for p in (A, B, C, D))
    L = (B - A).length
    if L < 1e-3:
        return
    ab = (B - A) / L
    up = (D - A) - ab * (D - A).dot(ab)
    hgt = up.length
    if hgt < 1e-3:
        return
    up = up / hgt
    sD, sC = (D - A).dot(ab), (C - A).dot(ab)
    nrm = (B - A).cross(D - A).normalized()
    flip = nrm.z < 0   # the slope was given the other way round: turn the faces so the tops face up (Unreal culls back faces)
    if flip:
        nrm = -nrm
    rng = Rng('zinc', round(A.x, 1), round(A.y, 1), round(A.z, 1), round(B.x, 1), round(B.y, 1))
    web = detail.web()
    w0 = spec['wear']
    sag = spec.get('sag', 0.0)
    pitch, depth, prof = spec['pitch'], spec['depth'], spec['profile']

    def reach(s):   # how far up the slope the roof goes at s (less on a hip's triangle)
        k = 1.0
        if sD > 1e-3 and s < sD:
            k = s / sD
        elif sC < L - 1e-3 and s > sC:
            k = (L - s) / (L - sC)
        return max(0.0, min(1.0, k))

    def rib(s, s0, s1):
        if web:   # flat: the ribs come from the material
            return 0.0
        t = (s / pitch) % 1.0
        if prof == 'sine':
            return depth * 0.5 * (1 - math.cos(t * math.tau))
        return depth if 0.08 < t < 0.24 else (depth * (t / 0.08) if t <= 0.08 else (depth * (1 - (t - 0.24) / 0.08) if t < 0.32 else 0.0))

    ns = max(1, round(L / COVER))
    nr = max(1, math.ceil(hgt / rng.between(2.4, 3.4)))   # sheets come 2.4-3.6 m long: a long slope has end laps
    ph = [rng.between(0, math.tau) for _ in range(3)]
    for j in range(ns):
        s0, s1 = L * j / ns, L * (j + 1) / ns
        sw = wear_of(j) if wear_of else max(0.0, min(1.0, w0 + rng.between(-0.3, 0.3)))
        new = rng.chance(0.02 + 0.06 * w0)
        base = NEW if new else (spec['col2'] if spec.get('mixed') and j % 3 == 0 else spec['col'])
        base = shade(base, rng.between(0.85, 1.1))
        if new:
            sw *= 0.15
        side = 0.006 * (j % 2)   # each sheet laps over the one before by a rib
        m = 2 if web else max(2, round((s1 - s0) / pitch * (4 if prof == 'sine' else 5)))
        ss = [s0 + (s1 - s0) * i / m for i in range(m + 1)]
        for r in range(nr):
            v0, v1 = r / nr, (r + 1) / nr
            lap = 0.012 * r                                   # an upper sheet lies on the one below...
            v0e = max(0.0, v0 - (0.12 / hgt if r else 0.0))   # ...and reaches 12 cm down over it
            # the purlins the sheet is nailed to, about a metre apart: a row at each nail line (rust starts there and runs
            # down the slope) and one just above it (clean), so the colour can break sharply at the nails
            npur = max(1, round(hgt * (v1 - v0e) / 1.0))
            nails = [v0e + (v1 - v0e) * (i + 0.5) / npur for i in range(npur)]
            nail_k = {i: rng.random() ** 2 for i in range(npur)}     # how badly each nail line has rusted: most a little
            edge_k = rng.random() ** 2                                  # and this sheet's lapped edge
            vs = sorted({v0e, v1, *nails, *[min(v1, v + 0.03 / hgt) for v in nails]})
            if sag > 0.005 and len(vs) < 3:
                vs = [v0e, (v0e + v1) / 2, v1]

            def P(s, v, under=0.0):
                base_pt = A + ab * s + up * hgt * reach(s) * v
                h = (rib(s, s0, s1) if not under else 0.0) + side + lap - under
                return base_pt + nrm * (h - sag_at(spec, s / L, v))

            def col(s, v):
                low = (1 - v) ** 1.5   # the water sits longest at the eave
                blot = 0.55 + 0.45 * math.sin(s * 1.7 + ph[0] + v * 2.3) * math.sin(s * 0.6 - v * 3.1 + ph[1])
                nail = next((nail_k[i] for i, n in enumerate(nails) if abs(v - n) < 1e-6), 0.0)   # just under a nail line
                edge = edge_k if abs(s - s0) < 1e-6 else 0.0                                  # the sheet's lapped edge
                k = sw * (0.15 + 0.6 * low + 0.5 * nail + 0.35 * edge) * (0.5 + blot)
                c = _mix(base, RUST, k * 0.9)
                return _mix(c, RUST_DARK, (k - 0.75) * 2.5)

            for a, b in zip(vs, vs[1:]):
                for s_a, s_b in zip(ss, ss[1:]):
                    q = [(s_a, a), (s_b, a), (s_b, b), (s_a, b)]
                    if reach(s_a) <= 1e-4 and reach(s_b) <= 1e-4:
                        continue
                    if flip:
                        q = q[::-1]
                    mb.face([P(*p) for p in q], 'zinc', [col(*p) for p in q], sw)
                # the underside, sheet by sheet: dark, a little under the ribs
                q = [(s1, a), (s0, a), (s0, b), (s1, b)]
                mb.face([P(*p, under=0.012) for p in (q[::-1] if flip else q)], 'zinc', shade(base, 0.45), sw)


GRIME = hex_rgb('#36342f')


def slab(mb, poly, z, col, wear):
    """A flat concrete roof: rings from the parapet in to the middle, so the colour can change across it. Darkest along
    the parapet where the water stands and the mould grows, ponding marks in blotches, sun-bleached in the open."""
    n = len(poly)
    cx, cy = sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n
    rng = Rng('slab', round(cx, 1), round(cy, 1))
    ph = [rng.between(0, math.tau) for _ in range(3)]
    fs = [1.0, 0.85, 0.5, 0.0]   # the rings, as a share of the way out from the middle

    def pt(p, f):
        return (cx + (p[0] - cx) * f, cy + (p[1] - cy) * f, z)

    def c(p, f):
        x, y = cx + (p[0] - cx) * f, cy + (p[1] - cy) * f
        blot = math.sin(x * 0.9 + ph[0]) * math.sin(y * 0.8 + ph[1]) + 0.5 * math.sin((x + y) * 1.7 + ph[2])
        k = wear * (0.25 + 0.6 * smooth_edge(f) + 0.45 * max(0.0, blot))
        return _mix(shade(col, 1.0 + 0.12 * (1 - f) - 0.05), GRIME, k)

    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for f0, f1 in zip(fs, fs[1:]):
            if f1 == 0.0:
                mb.face([pt(a, f0), pt(b, f0), (cx, cy, z)], 'concrete', [c(a, f0), c(b, f0), c(a, 0.0)], wear)
            else:
                mb.face([pt(a, f0), pt(b, f0), pt(b, f1), pt(a, f1)], 'concrete', [c(a, f0), c(b, f0), c(b, f1), c(a, f1)], wear)


def smooth_edge(f):
    """1 at the parapet, 0 a little way in."""
    t = max(0.0, min(1.0, (f - 0.8) / 0.2))
    return t * t * (3 - 2 * t)
