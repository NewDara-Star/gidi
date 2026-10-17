"""Street kit: road surfaces in every condition (from fresh asphalt to rutted mud), potholes that hold
rainwater, markings, painted kerbs, speed bumps, open drains with broken slabs, concrete poles with
sagging wire tangles, transformers, litter and refuse heaps.

Sources: docs/look/research-street.md (sections 1, 2, 6.7) and docs/look/research-roads.md.
Roads are real geometry grids, so potholes, ruts and puddles are actual dips; a flat water face at
the right level shows only where the road dips under it.
"""
import math

from mathutils import Matrix, Vector

from . import detail, parts
from .core import hex_rgb, shade

# ---------------------------------------------------------------- conditions
# Each condition: base colour(s), grid step, potholes per 100 m (range), pothole radius, ruts, patches.
COND = {
    'new':          dict(col='#3a3a38', step=1.0, holes=(0, 0), patch=0.0, mark=0.95, wear=0.1),
    'worn':         dict(col='#5e5c57', step=0.7, holes=(0, 2), r=(0.3, 0.9), patch=0.15, mark=0.5, wear=0.45),
    'potholed':     dict(col='#5a5853', step=0.5, holes=(4, 12), r=(0.4, 1.6), patch=0.3, mark=0.25, wear=0.7),
    'failed':       dict(col='#55524c', step=0.5, holes=(14, 30), r=(0.8, 3.0), patch=0.2, mark=0.0, wear=0.9, islands=True),
    'laterite_dry': dict(col='#c4703d', step=0.5, holes=(3, 8), r=(0.5, 1.8), ruts=0.07, mark=0.0, wear=0.5, soil=True),
    'laterite_wet': dict(col='#9a4a28', step=0.5, holes=(10, 22), r=(0.8, 3.5), ruts=0.14, mark=0.0, wear=0.9, soil=True, wet=True),
    'sand':         dict(col='#d8c9a3', step=0.6, holes=(1, 4), r=(0.6, 2.0), ruts=0.05, mark=0.0, wear=0.5, soil=True),
    'pavers':       dict(col='#8e8b84', step=0.7, holes=(0, 3), r=(0.3, 0.9), patch=0.0, mark=0.0, wear=0.4, pavers=True),
}
BASE_Z = {'main': 0.06, 'street': 0.05, 'lane': 0.04, 'path': 0.035}


def road_condition(r, ch, wealth, flood, rng):
    """Pick a road's condition from its class, the district's character, wealth and flood risk.
    Shares from research-street.md 1.1 and 1.6 (paved shares per class and character)."""
    k = r['k']
    if k == 'main':
        w = {'new': 1 + 4 * wealth, 'worn': 4, 'potholed': 3 * (1 - wealth) + (2 if ch == 'port' else 0), 'failed': 1.5 if ch == 'port' else 0.2}
    elif k == 'street':
        paved = {'elite': 0.95, 'civic': 0.9, 'dense': 0.7, 'old_island': 0.85, 'sprawl': 0.4, 'waterfront': 0.3, 'port': 0.6}.get(ch, 0.7)
        w = {'new': paved * wealth * 2, 'worn': paved * 2, 'potholed': paved * 3 * (1 - wealth), 'failed': paved * (1 - wealth),
             'pavers': (1.5 if ch == 'elite' else 0.2), 'laterite_dry': (1 - paved) * 3 * (1 - flood), 'laterite_wet': (1 - paved) * 3 * flood + 0.2,
             'sand': (1 - paved) * (2 if ch in ('old_island', 'waterfront') else 0.2)}
    else:  # lanes and paths: mostly earth outside the rich areas
        w = {'pavers': 2 if ch == 'elite' else 0.1, 'worn': 0.5, 'laterite_dry': 3 * (1 - flood), 'laterite_wet': 3 * flood + 0.4,
             'sand': 2 if ch in ('old_island', 'waterfront') else 0.2, 'potholed': 0.5}
    return rng.pick({c: v for c, v in w.items() if v > 0})


def _lerp(c0, c1, t):
    return tuple(a + (b - a) * t for a, b in zip(c0, c1))


# ---------------------------------------------------------------- road surface
def turning_head(mb, x, y, rad, kind, cond, rng):
    """The turning space at the end of a close (scripts/roadends.py): a round of the road's own surface, a hair under the
    road so the two meet without flicker, its rim crumbling to the shoulder like the road's edges."""
    C = COND[cond]
    z = BASE_Z.get(kind, 0.05) - 0.003
    col = hex_rgb(C['col'])
    rim = _lerp(col, hex_rgb('#c9926a'), 0.5) if not C.get('pavers') else col
    mat = 'mud' if C.get('soil') else ('pavers' if C.get('pavers') else 'asphalt')
    n = 20
    ring = [(x + math.cos(t) * rad * rng.between(0.97, 1.03), y + math.sin(t) * rad * rng.between(0.97, 1.03)) for t in (k / n * math.tau for k in range(n))]
    for k in range(n):
        a, b = ring[k], ring[(k + 1) % n]
        mb.face([Vector((x, y, z)), Vector((a[0], a[1], z)), Vector((b[0], b[1], z))], mat, [col, rim, rim], C['wear'])


def road(mb, r, cond, rng, wet_season=True, clip=None):
    """A road as a displaced grid. r: {k, pts, w}. Returns the potholes it made (for water faces)."""
    C = COND[cond]
    base = BASE_Z[r['k']] + rng.between(0, 0.002)
    col0 = hex_rgb(C['col'])
    soil = hex_rgb('#b5562e' if C.get('wet') else '#c4703d') if not C.get('soil') else col0
    asphalt_dark = hex_rgb('#2b2b29')
    w = r['w'] + (0.6 if r['k'] == 'street' else 0)
    pts = r['pts']
    holes, out_water = [], []
    total = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    n_holes = int(rng.between(*C['holes']) * total / 100) if C['holes'][1] else 0
    for _ in range(n_holes):
        s = rng.between(0, total)
        acc = 0
        for i in range(len(pts) - 1):
            L = math.dist(pts[i], pts[i + 1])
            if acc + L >= s:
                t = (s - acc) / L
                a, b = pts[i], pts[i + 1]
                dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                off = rng.between(-0.45, 0.45) * w
                cx, cy = a[0] + dx * L * t - dy * off, a[1] + dy * L * t + dx * off
                rad = rng.between(*C['r'])
                holes.append((cx, cy, rad, rng.between(0.06, 0.22) * (1.4 if C.get('soil') else 1), [rng.between(0.75, 1.25) for _ in range(7)]))
                break
            acc += L
    patches = []
    if C.get('patch'):
        for _ in range(int(C['patch'] * total / 6)):
            patches.append((rng.between(0, total), rng.between(-0.4, 0.4) * w, rng.between(1, 4), rng.between(0.8, 2.5)))
    seed = rng.between(0, 100)

    def noise(x, y, f):
        return (math.sin(x * f + seed) * math.cos(y * f * 1.3 - seed) + math.sin((x + y) * f * 0.7 + seed * 2)) * 0.5

    def hole_depth(x, y):
        d = 0.0
        for (hx, hy, hr, hd, rag) in holes:
            dx, dy = x - hx, y - hy
            dist = math.hypot(dx, dy)
            if dist > hr * 1.3:
                continue
            ang = math.atan2(dy, dx)
            k = rag[int((ang + math.pi) / math.tau * 7) % 7]
            q = dist / (hr * k)
            if q < 1:
                d = max(d, hd * (1 - q * q))
        return d

    step = C['step'] * (2.2 if detail.web() else 1.0)
    s_acc = 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.dist(a, b)
        if L < 0.01:
            continue
        dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        if clip and min(math.hypot(*a), math.hypot(*b)) > clip and _seg_dist0(a, b) > clip:
            s_acc += L
            continue
        ext = w / 2
        nu = max(1, int((L + 2 * ext) / step))
        nv = max(2, int(w / (min(step, 0.6) * (2.0 if detail.web() else 1.0))))

        def P(iu, iv):
            u = -ext + (L + 2 * ext) * iu / nu
            v = -w / 2 + w * iv / nv
            x, y = a[0] + dx * u - dy * v, a[1] + dy * u + dx * v
            z = base
            edge = abs(v) / (w / 2)
            c = col0
            # surface variation
            n1 = noise(x, y, 0.35)
            c = shade(c, 1 + 0.06 * n1)
            if C.get('ruts'):  # tyre ruts 0.9 m either side of the centre, with ridges of mud between
                for rv in (-0.9, 0.9):
                    t = abs(v - rv)
                    if t < 0.35:
                        z -= C['ruts'] * (1 - (t / 0.35) ** 2) * (0.7 + 0.3 * noise(x, y, 0.9))
                z += 0.03 * noise(x, y, 1.7)
            if C.get('islands') and noise(x, y, 0.25) < -0.1:  # failed road: asphalt gone, earth showing
                z -= 0.05
                c = _lerp(c, soil, 0.8)
            # crumbling edges give way to the shoulder
            if edge > 0.82 and not C.get('pavers'):
                k_ = (edge - 0.82) / 0.18 * (0.6 + 0.4 * noise(x, y, 2.0))
                c = _lerp(c, hex_rgb('#c9926a'), max(0, min(1, k_)))
                z -= 0.02 * k_
            hd = hole_depth(x, y)
            if hd > 0:
                z -= hd
                c = _lerp(c, hex_rgb('#5e4a38') if not C.get('soil') else shade(soil, 0.7), min(1, hd / 0.08))
            # patches of fresher asphalt
            su = s_acc + u
            for (ps, pv, pl, pw) in patches:
                if abs(su - ps) < pl / 2 and abs(v - pv) < pw / 2:
                    c = asphalt_dark
                    z += 0.004
            return Vector((x, y, z)), c

        grid = [[P(iu, iv) for iv in range(nv + 1)] for iu in range(nu + 1)]
        mat = 'mud' if C.get('soil') else ('pavers' if C.get('pavers') else 'asphalt')
        for iu in range(nu):
            for iv in range(nv):
                q = [grid[iu][iv], grid[iu + 1][iv], grid[iu + 1][iv + 1], grid[iu][iv + 1]]
                mb.face([p for p, _ in q], mat, [c for _, c in q], C['wear'])
        s_acc += L
    # rainwater in the dips
    if wet_season:
        for (hx, hy, hr, hd, rag) in holes:
            if C.get('wet') or rng.chance(0.6):
                lvl = base - hd * rng.between(0.25, 0.6)
                ring = [(hx + math.cos(t) * hr * 1.3, hy + math.sin(t) * hr * 1.3, lvl) for t in (k / 12 * math.tau for k in range(12))]
                mb.face(ring, 'water', hex_rgb('#4a3622' if C.get('soil') else '#3b3428'), 0.0)
    return holes


def _seg_dist0(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy or 1
    t = max(0, min(1, (-a[0] * dx - a[1] * dy) / l2))
    return math.hypot(a[0] + t * dx, a[1] + t * dy)


# ---------------------------------------------------------------- markings, kerbs, bumps
def markings(mb, r, cond, rng):
    """White dashed lane lines (3 m dash, 7 m gap) and yellow edge lines, faded by condition."""
    fresh = COND[cond]['mark']
    if fresh <= 0 or r['k'] not in ('main', 'street'):
        return
    z = BASE_Z[r['k']] + 0.006
    road_c = hex_rgb(COND[cond]['col'])
    white, yellow = _lerp(road_c, hex_rgb('#edebe4'), fresh), _lerp(road_c, hex_rgb('#e8c21a'), fresh)
    pts, w = r['pts'], r['w']
    lanes = [0.0] if r['k'] == 'street' else [-w / 4, w / 4]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.dist(a, b)
        if L < 1e-6:
            continue
        dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        rot = Matrix.Rotation(math.atan2(dy, dx), 4, 'Z')
        for off in lanes:
            s = rng.between(0, 5)
            while s < L - 3:
                if rng.chance(0.85 * fresh + 0.1):
                    x, y = a[0] + dx * (s + 1.5) - dy * off, a[1] + dy * (s + 1.5) + dx * off
                    mb.box('paint', Matrix.Translation((x, y, z)) @ rot, white, 0.3, size=(3.0, 0.12, 0.004), skip=('-z',))
                s += 10
        if r['k'] == 'main':
            for side in (-1, 1):
                off = side * (w / 2 - 0.3)
                x, y = (a[0] + b[0]) / 2 - dy * off, (a[1] + b[1]) / 2 + dx * off
                mb.box('paint', Matrix.Translation((x, y, z)) @ rot, yellow, 0.3, size=(L, 0.12, 0.004), skip=('-z',))


def kerbs(mb, r, scheme, rng, skip=None, clip=None):
    """Precast kerb blocks ~1 m, painted in alternating bands; some missing, some faded."""
    cols = {'yellow': ('#e8c21a', '#1c1c1c'), 'white': ('#edebe4', '#1c1c1c'), 'grey': ('#9a978f', '#8f8c84')}[scheme]
    pts, w = r['pts'], r['w']
    for side in (-1, 1):
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            L = math.dist(a, b)
            if L < 1e-6:
                continue
            dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            rot = Matrix.Rotation(math.atan2(dy, dx), 4, 'Z')
            for k in range(int(L)):
                x, y = a[0] + dx * (k + 0.5) - dy * side * (w / 2 + 0.07), a[1] + dy * (k + 0.5) + dx * side * (w / 2 + 0.07)
                if (clip and math.hypot(x, y) > clip) or (skip and skip((x, y))) or rng.chance(0.04):
                    continue
                c = hex_rgb(cols[k % 2])
                mb.box('concrete', Matrix.Translation((x, y, 0.13)) @ rot, shade(c, rng.between(0.75, 1.0)), rng.between(0.3, 0.8), size=(0.97, 0.14, 0.26))


def speed_bump(mb, r, s, rng, painted=False):
    pts = r['pts']
    a, b = pts[0], pts[-1]
    L = math.dist(a, b)
    dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    x, y = a[0] + dx * s, a[1] + dy * s
    h, l = rng.between(0.08, 0.18), rng.between(0.6, 1.4)
    m = Matrix.Translation((x, y, BASE_Z[r['k']])) @ Matrix.Rotation(math.atan2(dy, dx), 4, 'Z')
    n = 6
    for k in range(n):  # a hump: a strip of faces following a half-sine across the road
        t0, t1 = k / n, (k + 1) / n
        z0, z1 = h * math.sin(t0 * math.pi), h * math.sin(t1 * math.pi)
        x0, x1 = -l / 2 + l * t0, -l / 2 + l * t1
        c = hex_rgb('#e8c21a' if painted and k % 2 else '#3a3a38')
        mb.face([m @ Vector((x0, -r['w'] / 2, z0)), m @ Vector((x1, -r['w'] / 2, z1)), m @ Vector((x1, r['w'] / 2, z1)), m @ Vector((x0, r['w'] / 2, z0))], 'asphalt', c, 0.6)


# ---------------------------------------------------------------- drains
def drain(mb, run, spec, rng):
    """An open U-drain along a run of points (beside a road): block walls standing proud of the
    ground, silt and green water inside, some slabs over it, some broken or missing, rubbish in it."""
    w, h = spec['w'], spec['h']
    wall_c, wear = hex_rgb('#8a857a'), spec['wear']
    for i in range(len(run) - 1):
        a, b = run[i], run[i + 1]
        L = math.dist(a, b)
        if L < 0.05:
            continue
        dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        rot = Matrix.Rotation(math.atan2(dy, dx), 4, 'Z')
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        for side in (-1, 1):
            o = side * (w / 2 + 0.08)
            mb.box('concrete', Matrix.Translation((mid[0] - dy * o, mid[1] + dx * o, h / 2)) @ rot, wall_c, wear, size=(L + 0.02, 0.16, h))
        mb.box('mud', Matrix.Translation((mid[0], mid[1], 0.02)) @ rot, hex_rgb('#2b2a24'), 0.6, size=(L, w, 0.02), skip=('-z',))  # silt
        mb.box('water', Matrix.Translation((mid[0], mid[1], h * rng.between(0.2, 0.45))) @ rot, hex_rgb(spec['water']), 0, size=(L, w, 0.005), skip=('-z',))
        if rng.chance(spec['cover']):  # a slab over it (sometimes cracked and sunk)
            broken = rng.chance(0.2)
            mb.box('concrete', Matrix.Translation((mid[0], mid[1], h + 0.05 - (0.12 if broken else 0))) @ rot @ Matrix.Rotation(rng.between(-0.15, 0.15) if broken else 0, 4, 'X'),
                   hex_rgb('#9c978c'), wear + 0.2, size=(L - 0.04, w + 0.36, 0.1))
        elif rng.chance(spec['rubbish']):
            for _ in range(rng.randrange(2, 6)):
                litter_piece(mb, mid[0] + dx * rng.between(-L / 2, L / 2), mid[1] + dy * rng.between(-L / 2, L / 2), h * 0.4, rng)


# ---------------------------------------------------------------- poles, wires, transformers
def pole(mb, x, y, rng, h=None, wood=False):
    """A concrete (or old timber) pole with a crossarm and insulators. Returns its three wire points."""
    h = h or rng.between(9, 11)
    lean = (rng.between(-0.06, 0.06), rng.between(-0.06, 0.06))
    top = (x + lean[0] * h, y + lean[1] * h, h)
    if wood:
        parts.cyl(mb, 'wood', Matrix.Translation((x, y, 0)) @ Matrix.Rotation(lean[1], 4, 'X') @ Matrix.Rotation(-lean[0], 4, 'Y'), 0.13, h, hex_rgb('#5a4632'), 0.6, seg=8, r2=0.1)
    else:  # square-tapered concrete
        parts.cyl(mb, 'concrete', Matrix.Translation((x, y, 0)) @ Matrix.Rotation(lean[1], 4, 'X') @ Matrix.Rotation(-lean[0], 4, 'Y') @ Matrix.Rotation(math.pi / 4, 4, 'Z'), 0.18, h, hex_rgb('#9c978c'), rng.between(0.4, 0.8), seg=4, r2=0.1)
    ang = rng.between(0, math.pi)
    ax, ay = math.cos(ang), math.sin(ang)
    arm = 1.0
    parts.bar(mb, 'steel', (top[0] - ax * arm, top[1] - ay * arm, h - 0.3), (top[0] + ax * arm, top[1] + ay * arm, h - 0.3), 0.08, hex_rgb('#6b6b66'), 0.5)
    pts = []
    for k in (-1, 0, 1):
        px, py = top[0] + ax * arm * 0.9 * k, top[1] + ay * arm * 0.9 * k
        parts.cyl(mb, 'plastic', Matrix.Translation((px, py, h - 0.25)), 0.05, 0.14, hex_rgb('#e8e4dc'), 0, seg=6)
        pts.append((px, py, h - 0.1))
    return pts, top


def wire(mb, a, b, sag, col=(0.02, 0.02, 0.02), t=0.016, n=10):
    a, b = Vector(a), Vector(b)
    prev = a
    for k in range(1, n + 1):
        s = k / n
        p = a.lerp(b, s) - Vector((0, 0, sag * 4 * s * (1 - s)))
        parts.bar(mb, 'rubber', prev, p, t, col)
        prev = p


def transformer(mb, x, y, rng):
    """Pole-mounted H-frame with a grey finned tank, or a ground one in a block cage."""
    if rng.chance(0.6):
        for s in (-1, 1):
            parts.cyl(mb, 'concrete', Matrix.Translation((x + s * 0.9, y, 0)) @ Matrix.Rotation(math.pi / 4, 4, 'Z'), 0.17, 9.0, hex_rgb('#9c978c'), 0.6, seg=4, r2=0.11)
        mb.box('steel', Matrix.Translation((x, y, 3.6)), hex_rgb('#5a5a5a'), 0.6, size=(2.2, 1.0, 0.1))
        z = 3.65
    else:
        for (ax, ay), (bx, by) in ((((-1.4, -1.2), (1.4, -1.2))), (((1.4, -1.2), (1.4, 1.2))), (((1.4, 1.2), (-1.4, 1.2))), (((-1.4, 1.2), (-1.4, -1.2)))):
            mb.box('paint', Matrix.Translation((x + (ax + bx) / 2, y + (ay + by) / 2, 1.0)) @ Matrix.Rotation(math.atan2(by - ay, bx - ax), 4, 'Z'), hex_rgb('#d8ccb4'), 0.6, size=(math.hypot(bx - ax, by - ay), 0.2, 2.0))
        mb.box('concrete', Matrix.Translation((x, y, 0.15)), hex_rgb('#8f8a80'), 0.6, size=(1.8, 1.4, 0.3))
        z = 0.3
    mb.box('steel', Matrix.Translation((x, y, z + 0.75)), hex_rgb('#8c8f8a'), 0.5, size=(1.2, 0.8, 1.5))
    for k in range(7):  # radiator fins
        mb.box('steel', Matrix.Translation((x - 0.45 + k * 0.15, y + 0.5, z + 0.7)), hex_rgb('#7d807b'), 0.5, size=(0.03, 0.2, 1.1))
    for k in (-1, 0, 1):
        parts.cyl(mb, 'plastic', Matrix.Translation((x + k * 0.35, y, z + 1.5)), 0.05, 0.3, hex_rgb('#7a4a2a'), 0, seg=6)
    return (x, y, z + 1.8)


# ---------------------------------------------------------------- litter and refuse
LITTER = [('#e8f0f4', 'sachet', 5), ('#9ccbe8', 'sachet', 2), ('#1c1c1c', 'bag', 3), ('#1e6fd0', 'bag', 1), ('#d32f2f', 'bag', 1),
          ('#cfe3d6', 'bottle', 2), ('#ffffff', 'pack', 1.5), ('#c0c0c0', 'can', 1), ('#d9b85a', 'husk', 1)]


def litter_piece(mb, x, y, z, rng):
    col, kind, _ = rng.pick({l: l[2] for l in LITTER})
    c = hex_rgb(col)
    rz = rng.between(0, math.tau)
    m = Matrix.Translation((x, y, z)) @ Matrix.Rotation(rz, 4, 'Z')
    if kind == 'sachet':  # a torn pure-water pouch lying flat
        mb.box('plastic', m @ Matrix.Rotation(rng.between(-0.2, 0.2), 4, 'X'), c, 0, size=(0.18, 0.12, 0.006))
    elif kind == 'bag':  # a crumpled nylon bag
        parts.cyl(mb, 'plastic', m, rng.between(0.05, 0.1), rng.between(0.04, 0.08), c, 0, seg=6, r2=rng.between(0.02, 0.05))
    elif kind == 'bottle':
        parts.cyl(mb, 'glass', m @ Matrix.Translation((0, 0, 0.04)) @ Matrix.Rotation(math.pi / 2, 4, 'X'), 0.04, 0.24, c, 0, seg=6)
    elif kind == 'pack':
        mb.box('plastic', m @ Matrix.Translation((0, 0, 0.03)), c, 0, size=(0.2, 0.15, 0.06))
    elif kind == 'can':
        parts.cyl(mb, 'steel', m @ Matrix.Translation((0, 0, 0.035)) @ Matrix.Rotation(math.pi / 2, 4, 'X'), 0.033, 0.12, c, 0.3, seg=6)
    else:
        mb.box('cloth', m, c, 0, size=(0.2, 0.05, 0.03))


def refuse_heap(mb, x, y, r, rng):
    """A heap of bags, ash and food waste, 1–5 m across, often smouldering."""
    rings, seg = 5, 14
    h = r * rng.between(0.3, 0.5)
    prev = None
    for k in range(rings + 1):
        t = k / rings
        rr = r * (1 - t ** 1.6)
        z = h * math.sin(t * math.pi / 2)
        ring = [Vector((x + math.cos(a) * rr * rng.between(0.85, 1.15), y + math.sin(a) * rr * rng.between(0.85, 1.15), z)) for a in (i / seg * math.tau for i in range(seg))]
        if prev:
            for i in range(seg):
                j = (i + 1) % seg
                mb.face([prev[i], prev[j], ring[j], ring[i]], 'mud', hex_rgb(rng.pick(['#3a3026', '#4a3e30', '#2a2622'])), 0.9)
        prev = ring
    for _ in range(int(r * r * 12)):
        a, d = rng.between(0, math.tau), rng.between(0, r)
        zz = h * max(0, 1 - (d / r) ** 1.6) * 0.9
        litter_piece(mb, x + math.cos(a) * d, y + math.sin(a) * d, zz, rng)


# ---------------------------------------------------------------- people placed by hand (docs/KIT-GAPS.md, "New in the v2 layout")
# Each takes M at the spot, facing the road (+x), and the spot's Rng. Arms are poses for people.person (1.75 m frame;
# -1 is the right arm, 1 the left).
AGBERO_POSES = {
    'collect': {-1: ((0.25, -0.26, 1.16), (0.5, -0.2, 1.22)), 1: ((0.06, 0.25, 1.1), (0.2, 0.2, 0.93))},   # notes held out to the driver
    'count': {-1: ((0.16, -0.24, 1.08), (0.32, -0.07, 1.12)), 1: ((0.16, 0.24, 1.08), (0.32, 0.07, 1.1))},     # counting the float at the chest
    'wave': {-1: ((0.1, -0.36, 1.5), (0.16, -0.34, 1.86))},                                                 # waving the bus in with the notes
}


def agbero(mb, M, rng, pose=None):
    """An agbero at the park gate: a ticket book in one hand, a fan of notes folded lengthways in the other."""
    from . import people, props
    pose = pose or rng.pick(list(AGBERO_POSES))
    who = people.person(mb, M, rng, kind=rng.pick({'tshirt': 3, 'buba': 1}), pose=False, arms=AGBERO_POSES[pose], man=True)
    R, Lh = who['hands'][-1], who['hands'][1]
    yaw = Matrix.Rotation(math.atan2(M[1][0], M[0][0]), 4, 'Z')
    props.notes_fan(mb, Matrix.Translation(R) @ yaw, rng.child('notes'))
    props.ticket_book(mb, Matrix.Translation(Lh) @ yaw @ Matrix.Rotation(0.4, 4, 'Y'))
    if rng.chance(0.4):   # a cap
        parts.cyl(mb, 'cloth', who['head'] @ Matrix.Translation((0, 0, 0.08)), 0.105, 0.07, hex_rgb(rng.pick(['#1d1d1d', '#c62828', '#1f3f8a'])), 0.4, seg=10)
    return pose


def wheelbarrow_vendor(mb, M, rng):
    """Phone cases and chargers on a board across a wheelbarrow under an umbrella; the man behind it in an earpiece."""
    from . import people, props
    from .core import at
    tray = props.wheelbarrow(mb, M, hex_rgb(rng.pick(['#3f6b8a', '#6b6b66', '#8a3a2a'])))
    mb.box('wood', at(tray, 0, 0, 0.28), hex_rgb('#8a6a48'), 0.7, size=(1.05, 0.8, 0.03))
    for i in range(6):   # rows of cases lying on the board
        for j in range(4):
            mb.box('plastic', at(tray, -0.42 + i * 0.17, -0.27 + j * 0.18, 0.31, rz=rng.between(-0.08, 0.08)),
                   hex_rgb(rng.pick(['#1d1d1d', '#c62828', '#1f5fa8', '#f4f1ea', '#e91e63', '#f9a825', '#2e7d32', '#9e9e9e'])), 0.2, size=(0.15, 0.08, 0.012))
    parts.bar(mb, 'steel', at(tray, -0.5, 0, 0.3).translation, at(tray, -0.5, 0, 1.15).translation, 0.025, hex_rgb('#8a8d8c'), 0.6)   # the charger rail
    parts.bar(mb, 'steel', at(tray, -0.5, -0.4, 1.1).translation, at(tray, -0.5, 0.4, 1.1).translation, 0.02, hex_rgb('#8a8d8c'), 0.6)
    for k in range(7):
        y = -0.36 + k * 0.12
        parts.bar(mb, 'plastic', at(tray, -0.5, y, 1.1).translation, at(tray, -0.5, y, 0.75).translation, 0.008, hex_rgb('#f4f1ea'), 0.2)
        mb.box('plastic', at(tray, -0.5, y, 0.72), hex_rgb(rng.pick(['#f4f1ea', '#1d1d1d'])), 0.2, size=(0.04, 0.05, 0.06))
    props.umbrella(mb, at(M, -0.6, 0.3, 0), r=1.0, h=2.0, cols=rng.pick(props.UMBRELLA_COLS))
    who = people.person(mb, at(M, -1.3, -0.1, 0), rng, kind='tshirt', pose=False, man=True)
    parts.cyl(mb, 'plastic', who['head'] @ Matrix.Translation((0, -0.095 * who['k'], 0)) @ Matrix.Rotation(math.pi / 2, 4, 'X'), 0.018, 0.02, hex_rgb('#1d1d1d'), 0, seg=8)   # the earpiece


def fruit_seller(mb, M, rng):
    """Oranges, pineapples and bananas on a round tray on a folding table; the seller beside it."""
    from . import people, props
    from .core import at
    props.table(mb, M, 0.8, 0.8, 0.72, hex_rgb('#b0a08a'), 0.7, steel=True)
    T0 = at(M, 0, 0, 0.74)
    parts.cyl(mb, 'steel', T0, 0.42, 0.05, hex_rgb(rng.pick(['#c9ced2', '#2f6fae', '#c62828'])), 0.5, seg=16, r2=0.45)
    from .people import sphere
    for k in range(rng.randrange(14, 24)):   # oranges in a heap (greenish-orange, as they come)
        t, r = rng.between(0, math.tau), rng.between(0, 0.28)
        sphere(mb, 'plastic', at(T0, math.cos(t) * r - 0.05, math.sin(t) * r, 0.1 + (0.28 - r) * 0.4), 0.045, 0.045, 0.045, hex_rgb(rng.pick(['#f08a24', '#e8a33a', '#b8b23a'])), seg=6, rings=4)
    for k in range(2):   # pineapples
        P0 = at(T0, 0.22, -0.18 + k * 0.32, 0.05)
        parts.cyl(mb, 'plastic', P0, 0.07, 0.2, hex_rgb('#b8892e'), 0.5, seg=8, r2=0.06)
        parts.cyl(mb, 'plastic', at(P0, 0, 0, 0.2), 0.06, 0.14, hex_rgb('#3f6b2a'), 0.4, seg=6, r2=0.005)
    for k in range(3):   # bananas, a bunch of curved bars
        for j in range(4):
            a = at(T0, -0.3 + j * 0.03, 0.15 + k * 0.06, 0.07)
            parts.bar(mb, 'plastic', a.translation, at(a, 0.08, 0.14, 0.04).translation, 0.035, hex_rgb('#e8c430'), 0.3)
    people.person(mb, at(M, -0.7, 0.4, 0, rz=-0.4), rng, kind=rng.pick({'wrapper': 2, 'ankara': 1}), pose=False)
    if rng.chance(0.5):
        props.umbrella(mb, at(M, -0.3, -0.4, 0), r=1.0, h=2.0, cols=rng.pick(props.UMBRELLA_COLS))


def parking_boy(mb, M, rng):
    """A parking boy: his plastic chair with the ticket book on the seat, him beside it in a reflective vest."""
    from . import people, props
    from .core import at
    props.chair(mb, at(M, -0.4, 0.4, 0, rz=rng.between(-0.3, 0.3)), hex_rgb(rng.pick(props.CHAIR_COLS)), 0.6)
    props.ticket_book(mb, at(M, -0.4, 0.4, 0.47, rz=0.5))
    who = people.person(mb, M, rng, kind='tshirt', pose=False, arms={-1: ((0.2, -0.3, 1.25), (0.38, -0.3, 1.45))}, man=True)   # "Oga, park here"
    k, T0 = who['k'], who['torso']
    orange, silver = hex_rgb('#f26b1d'), hex_rgb('#d8dde0')
    parts.cyl(mb, 'cloth', T0 @ Matrix.Translation((0, 0, 0.04 * k)), 0.178 * k, 0.44 * k, orange, 0.5, seg=12, caps=(False, False), r2=0.205 * k)
    for z in (0.14, 0.3):
        parts.cyl(mb, 'cloth', T0 @ Matrix.Translation((0, 0, z * k)), 0.186 * k + z * 0.05, 0.035 * k, silver, 0.3, seg=12, caps=(False, False))


def bread_hawker(mb, M, rng, kind=None):
    """A bread hawker: loaves in nylon on a head tray, or a wheelbarrow of them pushed along (both versions)."""
    from . import people, props
    from .core import at
    kind = kind or rng.pick({'barrow': 1, 'tray': 1})
    if kind == 'barrow':
        tray = props.wheelbarrow(mb, M, hex_rgb(rng.pick(['#3f6b8a', '#6b6b66', '#2e6b45'])))
        props.loaves(mb, tray, rng.randrange(14, 24), rng.child('loaves'), rows=3)
        arms = {s: ((0.25, s * 0.26, 1.0), (0.5, s * 0.28, 0.8)) for s in (-1, 1)}   # on the handles
        people.person(mb, at(M, -1.45, 0, 0), rng, kind='tshirt', pose=False, arms=arms)
    else:
        who = people.person(mb, M, rng, kind=rng.pick({'ankara': 1, 'wrapper': 1}), pose=False, arms={1: ((0.05, 0.3, 1.55), (0.02, 0.25, 1.88))}, man=False)
        T0 = who['head'] @ Matrix.Translation((0, 0, 0.24 * who['k']))
        parts.cyl(mb, 'steel', T0, 0.36, 0.05, hex_rgb(rng.pick(['#c9ced2', '#2f6fae'])), 0.4, seg=16, r2=0.4)
        props.loaves(mb, at(T0, 0, 0, 0.0), rng.randrange(8, 13), rng.child('loaves'), rows=2)
    return kind


def rail_market(mb, M, rng):
    """One trader's pitch on the ballast beside the rails (the Hub's rail market): a low table or a mat of goods,
    basins, sometimes an umbrella. M: on the ballast, x along the track."""
    from . import props
    from .core import at
    from .people import sphere
    goods = rng.pick({'tomato': 3, 'pepper': 2, 'onion': 2, 'clothes': 2, 'plastic': 1, 'yam': 1})
    col = {'tomato': '#c62828', 'pepper': '#d84315', 'onion': '#b07a5a', 'clothes': None, 'plastic': None, 'yam': '#8a6a48'}[goods]
    if rng.chance(0.55):
        props.table(mb, M, rng.between(0.9, 1.4), 0.6, 0.45, shade(hex_rgb('#8a6a48'), rng.between(0.8, 1.1)), 0.8)
        top = at(M, 0, 0, 0.47)
    else:
        mb.box('cloth', at(M, 0, 0, 0.01), hex_rgb(rng.pick(['#1f5fa8', '#c62828', '#3a3a3a', '#7a6a4a'])), 0.7, size=(rng.between(1.0, 1.5), 0.9, 0.01))
        top = at(M, 0, 0, 0.02)
    for k in range(rng.randrange(2, 5)):
        B = at(top, -0.45 + k * 0.3, rng.between(-0.12, 0.12), 0)
        if goods in ('clothes', 'plastic'):
            for j in range(rng.randrange(2, 5)):
                mb.box('cloth' if goods == 'clothes' else 'plastic', at(B, 0, 0, 0.03 + j * 0.04, rz=rng.between(-0.3, 0.3)),
                       hex_rgb(rng.pick(['#d7263d', '#1b998b', '#f46036', '#2e294e', '#f2c14e', '#f4f1ea'])), 0.3, size=(0.3, 0.25, 0.04))
            continue
        props.basin(mb, B, hex_rgb(rng.pick(['#c9ced2', '#2f6fae', '#c62828', '#e8e2d6'])), r=0.17, h=0.1)
        for j in range(rng.randrange(4, 8)):
            sphere(mb, 'plastic', at(B, rng.between(-0.08, 0.08), rng.between(-0.08, 0.08), 0.1 + rng.between(0, 0.05)), 0.045, 0.045, 0.04,
                   shade(hex_rgb(col), rng.between(0.8, 1.1)), seg=6, rings=4)
    if rng.chance(0.3):
        props.umbrella(mb, at(M, -0.5, 0.5, 0), r=1.1, h=2.0, cols=rng.pick(props.UMBRELLA_COLS))
    if rng.chance(0.5):
        props.chair(mb, at(M, 0, -0.75, 0, rz=math.pi / 2), hex_rgb(rng.pick(props.CHAIR_COLS)), 0.6) if rng.chance(0.5) else props.bench(mb, at(M, 0, -0.75, 0, rz=math.pi / 2), 0.9, h=0.3)
