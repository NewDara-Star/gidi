"""Parcels: the plots and grounds in the data (web/gidi-data.js 'parcels'), each with its surface
and the furniture that makes it read: pitches with goalposts, a golf course with fairways and
greens, the decaying stadium bowl, an airfield runway, prison walls with towers, a tank farm's
bund walls, pools, a fountain square, the waterworks, the landfill. Research: research-leisure,
research-civic, research-commerce, research-transport, research-landmarks."""
import math

from mathutils import Matrix, Vector

from . import parts
from .blocks import block, dome, flagpole, perimeter
from .core import ccw, centroid, hex_rgb, offset, shade
from .kinds import _mound, cow, container, T


def _flat(mb, pts, z, mat, col, wear=0.4):
    mb.face([(p[0], p[1], z) for p in pts], mat, col, wear)


def _area(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2


def _bbox_frame(pts):
    """Long-axis frame of a polygon from its two longest-spaced points: centre, angle, length, width."""
    c = centroid(pts)
    best = (0, 0)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = math.dist(pts[i], pts[j])
            if d > best[0]:
                best = (d, math.atan2(pts[j][1] - pts[i][1], pts[j][0] - pts[i][0]))
    ang = best[1]
    ca, sa = math.cos(-ang), math.sin(-ang)
    xs = [(p[0] - c[0]) * ca - (p[1] - c[1]) * sa for p in pts]
    ys = [(p[0] - c[0]) * sa + (p[1] - c[1]) * ca for p in pts]
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    c2 = (c[0] + cx * math.cos(ang) - cy * math.sin(ang), c[1] + cx * math.sin(ang) + cy * math.cos(ang))
    m = Matrix.Translation((c2[0], c2[1], 0)) @ Matrix.Rotation(ang, 4, 'Z')
    return m, max(xs) - min(xs), max(ys) - min(ys)


def _scatter(pts, n, rng, pad=0.0):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    from .core import offset as _off
    inner = _off(pts, -pad) if pad else pts
    out, tries = [], 0
    while len(out) < n and tries < n * 30:
        tries += 1
        p = (rng.between(min(xs), max(xs)), rng.between(min(ys), max(ys)))
        if _inside(p, inner):
            out.append(p)
    return out


def _inside(p, poly):
    ins, j = False, len(poly) - 1
    for i in range(len(poly)):
        xi, yi, xj, yj = poly[i][0], poly[i][1], poly[j][0], poly[j][1]
        if (yi > p[1]) != (yj > p[1]) and p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi:
            ins = not ins
        j = i
    return ins


def tree(mb, x, y, rng, kind=None, h=None):
    """Street and compound trees: a broad almond/neem-like canopy, or a coconut/oil palm."""
    kind = kind or rng.pick({'broad': 3, 'palm': 2})
    if kind == 'palm':
        h = h or rng.between(7, 13)
        lean = Vector((rng.between(-0.6, 0.6), rng.between(-0.6, 0.6), 0))
        prev = Vector((x, y, 0))
        for k in range(1, 9):  # a curved, ringed trunk
            t = k / 8
            p = Vector((x, y, h * t)) + lean * t * t * 2
            parts.bar(mb, 'wood', prev, p, 0.32 - 0.1 * t, shade(hex_rgb('#7a6248'), 0.9 if k % 2 else 1.05), 0.6)
            prev = p
        for f in range(11):  # fronds: arching, drooping blades
            a = f / 11 * math.tau + rng.between(-0.2, 0.2)
            d = Vector((math.cos(a), math.sin(a), 0))
            pts = [prev]
            for s in range(1, 5):
                t = s / 4
                pts.append(prev + d * (3.2 * t) + Vector((0, 0, 1.0 * t - 2.2 * t * t)))
            side = Vector((-d.y, d.x, 0))
            for s in range(4):
                w0, w1 = 0.5 * (1 - s / 4) + 0.05, 0.5 * (1 - (s + 1) / 4) + 0.05
                col = shade(hex_rgb('#4f7a2e'), rng.between(0.8, 1.15))
                mb.face([pts[s] - side * w0, pts[s + 1] - side * w1, pts[s + 1] + side * w1, pts[s] + side * w0], 'leaf', col, 0.2)
                mb.face([pts[s] + side * w0, pts[s + 1] + side * w1, pts[s + 1] - side * w1, pts[s] - side * w0], 'leaf', col, 0.2)
        for k in range(3):
            parts.cyl(mb, 'plastic', Matrix.Translation(prev + Vector((math.cos(k * 2.1) * 0.25, math.sin(k * 2.1) * 0.25, -0.35))), 0.13, 0.22, hex_rgb('#6b5a2a'), 0, seg=6)
        return
    h = h or rng.between(6, 11)
    parts.cyl(mb, 'wood', Matrix.Translation((x, y, 0)), 0.25, h * 0.55, hex_rgb('#5e4a38'), 0.6, seg=8, r2=0.17)
    for k in range(rng.randrange(4, 7)):  # canopy of leafy lobes
        a, r = rng.between(0, math.tau), rng.between(0, h * 0.25)
        cx, cy, cz = x + math.cos(a) * r, y + math.sin(a) * r, h * rng.between(0.6, 0.85)
        rr = h * rng.between(0.22, 0.32)
        _lobe(mb, cx, cy, cz, rr, rr * 0.7, shade(hex_rgb(rng.pick(['#3f7a2e', '#4f8a34', '#2f6a2a'])), rng.between(0.85, 1.1)))


def _lobe(mb, x, y, z, r, rz, col, seg=10, rings=6):
    prev = None
    for k in range(rings + 1):
        t = -math.pi / 2 + math.pi * k / rings
        ring = [Vector((x + math.cos(a) * math.cos(t) * r, y + math.sin(a) * math.cos(t) * r, z + math.sin(t) * rz)) for a in (i / seg * math.tau for i in range(seg))]
        if prev:
            for i in range(seg):
                j = (i + 1) % seg
                mb.face([prev[i], prev[j], ring[j], ring[i]], 'leaf', col, 0.2)
        prev = ring


# ---------------------------------------------------------------- sport
def pitch(mb, pts, rng, ch):
    """A football pitch: sand or patchy grass, white lines, goalposts with no nets (most), a wall."""
    m, L, W = _bbox_frame(pts)
    grass = ch in ('elite', 'civic') or rng.chance(0.3)
    _flat(mb, pts, 0.04, 'ground', hex_rgb('#6e8f3a' if grass else '#d8c49a'), 0.6)
    lw = hex_rgb('#e8e4d8')
    pl, pw = L * 0.9, W * 0.85
    for (x0, y0, x1, y1) in ((-pl / 2, -pw / 2, pl / 2, -pw / 2), (-pl / 2, pw / 2, pl / 2, pw / 2), (-pl / 2, -pw / 2, -pl / 2, pw / 2), (pl / 2, -pw / 2, pl / 2, pw / 2), (0, -pw / 2, 0, pw / 2)):
        parts.bar(mb, 'paint', T(m, x0, y0, 0.05).translation, T(m, x1, y1, 0.05).translation, 0.1, lw, 0.3)
    for s in (-1, 1):  # goalposts
        x = s * pl / 2
        for y in (-3.66, 3.66):
            parts.bar(mb, 'steel', T(m, x, y, 0).translation, T(m, x, y, 2.44).translation, 0.1, hex_rgb('#f2f2f2'), 0.4)
        parts.bar(mb, 'steel', T(m, x, -3.66, 2.44).translation, T(m, x, 3.66, 2.44).translation, 0.1, hex_rgb('#f2f2f2'), 0.4)


def court(mb, pts, rng, ch):
    """Tennis or basketball court: green acrylic with white lines, a high mesh fence."""
    m, L, W = _bbox_frame(pts)
    _flat(mb, pts, 0.05, 'paint', hex_rgb('#2e7d5a'), 0.2)
    _flat(mb, offset(ccw(pts), -2.0), 0.055, 'paint', hex_rgb('#2f5f9f'), 0.2)
    parts.bar(mb, 'paint', T(m, 0, -W / 2 + 2, 0.06).translation, T(m, 0, W / 2 - 2, 0.06).translation, 0.08, hex_rgb('#f2f2f2'), 0.1)
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        n = max(1, int(math.dist(a, b) / 3))
        for k in range(n + 1):
            t = k / n
            p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            parts.bar(mb, 'steel', (p[0], p[1], 0), (p[0], p[1], 3.5), 0.05, hex_rgb('#2a4a3a'), 0.3)
        parts.bar(mb, 'steel', (a[0], a[1], 3.5), (b[0], b[1], 3.5), 0.04, hex_rgb('#2a4a3a'), 0.3)


def pool(mb, pts, rng, ch):
    """A pool: blue water in a white tiled surround, loungers."""
    p = ccw(pts)
    _flat(mb, offset(p, 1.2), 0.06, 'paint', hex_rgb('#f2efe6'), 0.1)
    _flat(mb, p, 0.07, 'water', hex_rgb('#2a9ad0'), 0)
    m, L, W = _bbox_frame(p)
    for k in range(3):
        mb.box('plastic', T(m, -L / 2 + 1 + k * 1.2, W / 2 + 0.8, 0.25), hex_rgb('#ffffff'), 0, size=(0.7, 1.9, 0.12))


def golf_course(mb, pts, rng, ch):
    """The golf club's course: rough, mown fairways, greens with flags, sand bunkers, palms and
    broad trees, a high wall round it (research-leisure golf club)."""
    p = ccw(pts)
    _flat(mb, p, 0.03, 'ground', hex_rgb('#5f8a35'), 0.3)
    m, L, W = _bbox_frame(p)
    holes = max(3, int(L * W / 3500))
    for h in range(holes):  # fairway strips of lighter mown grass, each ending in a green
        x = -L / 2 + (h + 0.5) * L / holes
        y0, y1 = rng.between(-W / 2.6, -W / 6), rng.between(W / 6, W / 2.6)
        wdt = rng.between(18, 30)
        quad = [T(m, x - wdt / 2, y0, 0.04).translation, T(m, x + wdt / 2, y0, 0.04).translation, T(m, x + wdt / 2 + rng.between(-6, 6), y1, 0.04).translation, T(m, x - wdt / 2 + rng.between(-6, 6), y1, 0.04).translation]
        mb.face(quad, 'ground', hex_rgb('#7aa845'), 0.1)
        g = T(m, x, y1 + 6, 0.05)
        mb.face([g @ Vector((math.cos(a) * 9, math.sin(a) * 7, 0)) for a in (k / 14 * math.tau for k in range(14))], 'ground', hex_rgb('#8cc152'), 0.05)
        parts.bar(mb, 'steel', g.translation, (g.translation.x, g.translation.y, 2.2), 0.03, hex_rgb('#f2f2f2'))
        mb.box('cloth', Matrix.Translation((g.translation.x + 0.25, g.translation.y, 2.0)), hex_rgb('#d32f2f'), 0, size=(0.5, 0.02, 0.32))
        b = T(m, x + rng.pick([-1, 1]) * 12, y1 - 4, 0.05)
        mb.face([b @ Vector((math.cos(a) * 5 * rng.between(0.8, 1.2), math.sin(a) * 3, 0)) for a in (k / 12 * math.tau for k in range(12))], 'ground', hex_rgb('#e8dcb0'), 0.2)  # bunker
    for q in _scatter(p, int(L * W / 900), rng, pad=4):
        tree(mb, q[0], q[1], rng, kind=rng.pick({'palm': 2, 'broad': 3}))
    perimeter(mb, p, dict(paint=hex_rgb('#f2efe6'), coping=hex_rgb('#2e5d3a'), gate=hex_rgb('#2e5d3a'), h=3.0, top='plain', wear=0.2), rng)


def stadium(mb, pts, rng, ch):
    """National Bowl (research-landmarks 1; invented design): a round 1970s concrete bowl of raker
    terraces with green-and-white raker tips, three lattice floodlight masts standing and one fallen,
    a detached dead scoreboard tower, a cracked track and a brown pitch, squatters' tents."""
    m, L, W = _bbox_frame(pts)
    R = min(L, W) / 2 * 0.95
    ri = R * 0.55
    _flat(mb, pts, 0.03, 'concrete', hex_rgb('#8f8a80'), 0.8)
    # pitch and running track
    track = [T(m, math.cos(a) * ri * 0.98, math.sin(a) * ri * 0.75, 0.05).translation for a in (k / 40 * math.tau for k in range(40))]
    mb.face(track, 'mud', hex_rgb('#9a4a32'), 0.8)
    pitch_ = [T(m, math.cos(a) * ri * 0.78, math.sin(a) * ri * 0.55, 0.06).translation for a in (k / 40 * math.tau for k in range(40))]
    mb.face(pitch_, 'ground', hex_rgb('#7a7a42'), 0.7)
    # raker terraces round the bowl: stepped rings, broken in places
    rows = 22
    seg = 72
    for k in range(rows):
        r0 = ri + k * (R - ri) / rows
        r1 = ri + (k + 1) * (R - ri) / rows
        z = 0.6 + k * 0.85
        for i in range(seg):
            a0, a1 = i / seg * math.tau, (i + 1) / seg * math.tau
            sq = lambda r, a: (math.cos(a) * r, math.sin(a) * r * (0.75 + 0.25 * (r - ri) / (R - ri)))
            p00, p01, p10, p11 = sq(r0, a0), sq(r0, a1), sq(r1, a0), sq(r1, a1)
            c = shade(hex_rgb('#a8a49a'), 0.95 + 0.1 * math.sin(i * 1.7 + k))
            if rng.chance(0.03 * (1 + k / rows)):
                continue  # a collapsed bay
            mb.face([T(m, *p00, z).translation, T(m, *p01, z).translation, T(m, *p11, z).translation, T(m, *p10, z).translation], 'concrete', c, 0.85)
            mb.face([T(m, *p10, z).translation, T(m, *p11, z).translation, T(m, *p11, z + 0.85).translation, T(m, *p10, z + 0.85).translation], 'concrete', shade(c, 0.85), 0.85)
            if k == rows - 1 and i % 4 == 0:  # raker fins with green and white tips above the rim
                tip = hex_rgb('#2e7d4f' if (i // 4) % 2 else '#f2f2f2')
                mb.box('concrete', T(m, *sq(r1 + 0.6, a0), z + 2.5, rz=a0), tip, 0.7, size=(1.4, 0.6, 3.5))
    # outer wall of the bowl
    rim = [T(m, math.cos(a) * R, math.sin(a) * R, 0).translation for a in (k / seg * math.tau for k in range(seg))]
    for i in range(seg):
        a, b = rim[i], rim[(i + 1) % seg]
        mb.face([a, b, b + Vector((0, 0, rows * 0.85 + 0.6)), a + Vector((0, 0, rows * 0.85 + 0.6))], 'concrete', hex_rgb('#9a958a'), 0.9)
    # floodlight masts: lattice towers, one lying fallen
    for i, a in enumerate((0.6, 2.5, 3.8, 5.6)):
        base = T(m, math.cos(a) * (R + 6), math.sin(a) * (R + 6), 0)
        hgt = 55
        if i == 3:  # fallen across the car park
            base = base @ Matrix.Rotation(1.45, 4, 'X')
        for (x, y) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            parts.bar(mb, 'steel', base @ Vector((x * 1.2, y * 1.2, 0)), base @ Vector((x * 0.6, y * 0.6, hgt)), 0.18, hex_rgb('#7a7d80'), 0.8)
        for k in range(0, hgt, 5):
            parts.bar(mb, 'steel', base @ Vector((-1.1, -1.1, k)), base @ Vector((1.1, 1.1, k + 5)), 0.08, hex_rgb('#7a7d80'), 0.8)
        mb.box('steel', base @ Matrix.Translation((0, 0, hgt + 2)), hex_rgb('#5a5a5a'), 0.8, size=(8, 1.2, 4))
    sb = T(m, 0, -R - 20, 0)  # the detached scoreboard tower, long dead
    mb.box('concrete', sb @ Matrix.Translation((0, 0, 9)), hex_rgb('#9a958a'), 0.9, size=(3, 3, 18))
    mb.box('steel', sb @ Matrix.Translation((0, 0, 20)), hex_rgb('#1d1d1d'), 0.9, size=(14, 1.2, 6))
    for q in _scatter(pts, 25, rng):  # squatters' tents and shacks round the outside
        if math.dist(q, (m.translation.x, m.translation.y)) > R + 4:
            mb.box('cloth', Matrix.Translation((q[0], q[1], 0.8)) @ Matrix.Rotation(rng.between(0, 3), 4, 'Z'), hex_rgb(rng.pick(['#2e6fb7', '#e8771e', '#d0d0d0', '#3a3a3a'])), 0.6, size=(rng.between(2, 4), rng.between(2, 3), 1.6))


# ---------------------------------------------------------------- transport and industry
def airfield(mb, pts, rng, ch):
    """Airport edge: runway with threshold bars and centreline, taxiway, approach lights, a high fence."""
    m, L, W = _bbox_frame(pts)
    _flat(mb, pts, 0.03, 'ground', hex_rgb('#8a9a4a'), 0.5)
    rw = min(45, W * 0.5)
    mb.face([T(m, -L / 2 + 10, -rw / 2, 0.05).translation, T(m, L / 2 - 10, -rw / 2, 0.05).translation, T(m, L / 2 - 10, rw / 2, 0.05).translation, T(m, -L / 2 + 10, rw / 2, 0.05).translation], 'asphalt', hex_rgb('#4a4c50'), 0.3)
    for x in range(int(-L / 2 + 40), int(L / 2 - 40), 50):
        mb.box('paint', T(m, x, 0, 0.06), hex_rgb('#f2f2ee'), 0.2, size=(30, 0.9, 0.01))
    for s in (-1, 1):
        for k in range(8):
            mb.box('paint', T(m, s * (L / 2 - 25), -rw / 2 + 4 + k * (rw - 8) / 7, 0.06), hex_rgb('#f2f2ee'), 0.2, size=(30, 1.8, 0.01))
        for k in range(10):  # approach lights
            mb.box('emit', T(m, s * (L / 2 - 8 + k * 0.0), -rw / 2 + k * rw / 9, 0.3), hex_rgb('#fff1c8'), 0, size=(0.3, 0.3, 0.3))
    p = ccw(pts)
    for i in range(len(p)):  # the airport fence
        a, b = p[i], p[(i + 1) % len(p)]
        n = max(1, int(math.dist(a, b) / 4))
        for k in range(n):
            t = k / n
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            parts.bar(mb, 'steel', (q[0], q[1], 0), (q[0], q[1], 3.2), 0.06, hex_rgb('#8a8f92'), 0.4)
        parts.bar(mb, 'steel', (a[0], a[1], 3.0), (b[0], b[1], 3.0), 0.03, hex_rgb('#8a8f92'), 0.4)
    # the terminal and the control tower beside the runway (research-landmarks 29, invented): a long
    # low concrete terminal with a glass front and a deep canopy, jet bridges, and the tower
    ty = rw / 2 + min(60, (W / 2 - rw / 2) * 0.6)
    if W / 2 - rw / 2 > 40:
        tl = min(L * 0.45, 260)
        tm = T(m, -L * 0.1, ty, 0)
        mb.box('concrete', tm @ Matrix.Translation((0, 12, 6)), hex_rgb('#d8d4cc'), 0.4, size=(tl, 30, 12))
        mb.box('glass', tm @ Matrix.Translation((0, -3.02, 6)), hex_rgb('#24343e'), 0.1, size=(tl - 4, 0.04, 9))
        mb.box('concrete', tm @ Matrix.Translation((0, -1, 12.3)), hex_rgb('#c9c4ba'), 0.4, size=(tl + 6, 8, 0.6))  # canopy
        for k in range(4):  # jet bridges reaching to the apron
            x = -tl / 2 + (k + 0.5) * tl / 4
            mb.box('steel', tm @ Matrix.Translation((x, -12, 5)), hex_rgb('#b8bcbf'), 0.3, size=(3, 18, 3))
        tw = tm @ Matrix.Translation((tl / 2 + 25, 5, 0))
        parts.cyl(mb, 'concrete', tw, 3.0, 38, hex_rgb('#d8d4cc'), 0.4, seg=14, r2=2.4)
        parts.cyl(mb, 'glass', tw @ Matrix.Translation((0, 0, 38)), 5.5, 4.0, hex_rgb('#24343e'), 0.1, seg=14, r2=6.0)
        parts.cyl(mb, 'concrete', tw @ Matrix.Translation((0, 0, 42)), 6.2, 1.2, hex_rgb('#c9c4ba'), 0.4, seg=14, r2=3.0)
        parts.bar(mb, 'steel', (tw @ Vector((0, 0, 43))), (tw @ Vector((0, 0, 50))), 0.15, hex_rgb('#c62828'), 0.3)


def tank_farm(mb, pts, rng, ch):
    """Rows of storage tanks in bund walls, pipe racks between, a gantry for tankers."""
    p = ccw(pts)
    _flat(mb, p, 0.03, 'concrete', hex_rgb('#8f8a80'), 0.6)
    m, L, W = _bbox_frame(p)
    nx, ny = max(1, int(L / 40)), max(1, int(W / 40))
    for i in range(nx):
        for j in range(ny):
            x, y = -L / 2 + (i + 0.5) * L / nx, -W / 2 + (j + 0.5) * W / ny
            r = min(L / nx, W / ny) * 0.32
            c = T(m, x, y, 0).translation
            parts.cyl(mb, 'steel', Matrix.Translation((c.x, c.y, 0)), r, r * 0.8, hex_rgb(rng.pick(['#e8e6df', '#d8dcdf'])), 0.4, seg=28)
            parts.cyl(mb, 'steel', Matrix.Translation((c.x, c.y, r * 0.8)), r, r * 0.1, hex_rgb('#cfd3d6'), 0.4, seg=28, r2=r * 0.2)
            for k in range(4):  # bund walls
                a = k * math.pi / 2
                mb.box('concrete', Matrix.Translation((c.x + math.cos(a) * r * 1.45, c.y + math.sin(a) * r * 1.45, 0.6)) @ Matrix.Rotation(a, 4, 'Z'), hex_rgb('#9c978c'), 0.6, size=(0.3, r * 2.9, 1.2))
    for y in (-W / 2 + 4, W / 2 - 4):  # pipe racks
        for k in range(3):
            parts.bar(mb, 'steel', T(m, -L / 2 + 5, y + k * 0.5, 2.5).translation, T(m, L / 2 - 5, y + k * 0.5, 2.5).translation, 0.25, hex_rgb('#b0a070'), 0.6)
    perimeter(mb, p, dict(paint=hex_rgb('#e8e2d2'), coping=hex_rgb('#c62828'), gate=hex_rgb('#c62828'), h=2.6, top='razor', wear=0.5), rng)


def landfill(mb, pts, rng, ch):
    """Refuse mounds with smoke columns, scavengers' paths, a tipper unloading."""
    p = ccw(pts)
    _flat(mb, p, 0.03, 'mud', hex_rgb('#4a3e30'), 0.9)
    m, L, W = _bbox_frame(p)
    for k in range(max(2, int(L * W / 2500))):
        q = _scatter(p, 1, rng, pad=10)
        if q:
            _mound(mb, q[0], rng.between(10, 22), rng.between(8, 18), rng.between(3, 9), hex_rgb('#3a3026'), 'mud', rng, 0.95)
    from .street import litter_piece
    for q in _scatter(p, int(L * W / 15), rng):
        litter_piece(mb, q[0], q[1], rng.between(0.05, 3.0), rng)
    for q in _scatter(p, 5, rng, pad=15):  # smoke from smouldering fires: grey columns
        for k in range(6):
            parts.cyl(mb, 'cloth', Matrix.Translation((q[0] + k * 0.6, q[1], k * 2.5)), 1.0 + k * 0.6, 2.5, hex_rgb('#8a8a86'), 0, seg=10, caps=(False, False), r2=1.3 + k * 0.6)


def waterworks(mb, pts, rng, ch):
    """Iju Waterworks (1915), invented design: a red-brick pump house with arched windows and a
    tall chimney, round settling tanks, open reservoirs, iron fence (research-landmarks 33)."""
    p = ccw(pts)
    _flat(mb, p, 0.03, 'ground', hex_rgb('#7a8f45'), 0.4)
    m, L, W = _bbox_frame(p)
    ph = [T(m, x, y, 0).translation for (x, y) in ((-L / 4 - 15, -8), (-L / 4 + 15, -8), (-L / 4 + 15, 8), (-L / 4 - 15, 8))]
    block(mb, ccw([(q.x, q.y) for q in ph]), 2, dict(style='govt', wall=hex_rgb('#9a4e34'), band=hex_rgb('#e8dcc0'), trim=hex_rgb('#e8dcc0'), wear=0.7, floor_h=4.5, window='casement', win_h=2.4, fins=False, roof='hip', pitch=25, roof_col=hex_rgb('#5a5a5a'),
                                                     sign='GIDI WATER WORKS • 1915', sign_bg=hex_rgb('#e8dcc0'), sign_fg=hex_rgb('#5a2a1a')), rng)
    ch_ = T(m, -L / 4 + 18, 10, 0)
    parts.cyl(mb, 'block', ch_, 1.8, 32, hex_rgb('#8a4430'), 0.8, seg=12, r2=1.2)
    for k in range(3):
        c = T(m, L / 6 + k * 22 - 10, -W / 5, 0).translation
        parts.cyl(mb, 'concrete', Matrix.Translation((c.x, c.y, 0)), 9, 3.0, hex_rgb('#a8a49a'), 0.7, seg=28)
        mb.face([Vector((c.x + math.cos(a) * 8.6, c.y + math.sin(a) * 8.6, 2.6)) for a in (j / 28 * math.tau for j in range(28))], 'water', hex_rgb('#3a5a50'), 0)
    rv = [T(m, x, y, 0.08).translation for (x, y) in ((L / 8, W / 8), (L / 2.4, W / 8), (L / 2.4, W / 2.4), (L / 8, W / 2.4))]
    mb.face(rv, 'water', hex_rgb('#3a5a50'), 0)
    perimeter(mb, p, dict(paint=hex_rgb('#e8dcc0'), coping=hex_rgb('#2e4d3a'), gate=hex_rgb('#2e4d3a'), h=2.2, wear=0.6), rng)


def prison(mb, pts, rng, ch):
    """A 6-7 m wall with watchtowers at the corners and one gate (research-civic 16)."""
    p = ccw(pts)
    _flat(mb, p, 0.03, 'ground', hex_rgb('#b59a78'), 0.6)
    for i in range(len(p)):
        a, b = p[i], p[(i + 1) % len(p)]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        L = math.dist(a, b)
        mb.box('paint', Matrix.Translation(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 3.25)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#e2d5b0'), 0.7, size=(L, 0.5, 6.5))
        mb.box('paint', Matrix.Translation(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0.6)) @ Matrix.Rotation(ang, 4, 'Z'), hex_rgb('#2e4d3a'), 0.7, size=(L + 0.02, 0.52, 1.2))
        for k in range(int(L / 0.3)):
            parts.bar(mb, 'steel', (a[0] + (b[0] - a[0]) * k * 0.3 / L, a[1] + (b[1] - a[1]) * k * 0.3 / L, 6.6), (a[0] + (b[0] - a[0]) * (k * 0.3 + 0.3) / L, a[1] + (b[1] - a[1]) * (k * 0.3 + 0.3) / L, 6.9 + 0.15 * (k % 2)), 0.015, hex_rgb('#9a9a9a'), 0.3)
        mb.box('paint', Matrix.Translation((a[0], a[1], 5.0)), hex_rgb('#e2d5b0'), 0.6, size=(3, 3, 10))  # watchtower
        mb.box('glass', Matrix.Translation((a[0], a[1], 9.0)), hex_rgb('#24343e'), 0, size=(3.1, 3.1, 1.2))
        mb.box('concrete', Matrix.Translation((a[0], a[1], 10.2)), hex_rgb('#ffffff'), 0.4, size=(3.8, 3.8, 0.3))


def barracks_ground(mb, pts, rng, ch):
    """A cantonment: long perimeter wall, painted kerbs, a parade ground, a ceremonial gate."""
    p = ccw(pts)
    _flat(mb, p, 0.03, 'ground', hex_rgb('#c9a57a'), 0.6)
    m, L, W = _bbox_frame(p)
    mb.face([T(m, x, y, 0.05).translation for (x, y) in ((-L / 6, -W / 6), (L / 6, -W / 6), (L / 6, W / 6), (-L / 6, W / 6))], 'asphalt', hex_rgb('#5e5c57'), 0.5)
    flagpole(mb, m.translation.x, m.translation.y, 12, ['#2f4a2a', '#ffffff', '#2f4a2a'])
    perimeter(mb, p, dict(paint=hex_rgb('#e6d6a8'), coping=hex_rgb('#2f4a2a'), gate=hex_rgb('#2f4a2a'), h=3.0, top='razor', wear=0.6), rng)


def market_ground(mb, pts, rng, ch):
    _flat(mb, pts, 0.04, 'concrete', hex_rgb('#a39b8e'), 0.7)


def yard(mb, pts, rng, ch, col='#b08e6a', mat='mud'):
    _flat(mb, pts, 0.04, mat, hex_rgb(col), 0.7)


def motor_park(mb, pts, rng, ch):
    """A motor park: laterite floor, a union office shack with a levy table and an umbrella."""
    _flat(mb, pts, 0.045, 'mud', hex_rgb('#b0784a'), 0.8)
    m, L, W = _bbox_frame(pts)
    sh = T(m, -L / 2 + 3, W / 2 - 3, 0)
    mb.box('wood', sh @ Matrix.Translation((0, 0, 1.2)), hex_rgb('#2f6fae'), 0.8, size=(3.0, 2.5, 2.4))
    parts.corrugated(mb, sh @ Vector((-1.8, -1.6, 2.4)), sh @ Vector((1.8, -1.6, 2.4)), sh @ Vector((1.8, 1.5, 2.6)), sh @ Vector((-1.8, 1.5, 2.6)), dict(profile='sine', pitch=0.076, depth=0.018, col=hex_rgb('#7a4524'), wear=0.9))
    parts.signboard(mb, sh @ Matrix.Translation((0, -1.27, 0)), 0, 2.0, 2.6, 0.5, dict(text='UNION OFFICE', bg=hex_rgb('#f2c21b'), fg=hex_rgb('#1a1a1a'), hand=True, wear=0.7, wobble=0.02))
    mb.box('wood', sh @ Matrix.Translation((0, -2.6, 0.75)), hex_rgb('#6b4f36'), 0.7, size=(1.4, 0.7, 0.05))


def paved(mb, pts, rng, ch, col='#c9c1b0'):
    _flat(mb, pts, 0.045, 'pavers', hex_rgb(col), 0.4)


def green(mb, pts, rng, ch, trees=True):
    """Lawns, gardens and parks: grass, paths, palms and broad trees, benches."""
    p = ccw(pts)
    _flat(mb, p, 0.04, 'ground', hex_rgb('#6e9a3e'), 0.3)
    if trees:
        for q in _scatter(p, max(1, int(_area(p) / 400)), rng, pad=2):
            tree(mb, q[0], q[1], rng)


def square(mb, pts, rng, ch):
    """The commemorative square, invented design: paving, a long arcade down one side, and the
    gate: two white pylons, each crowned with a white horse, an arch between them carrying a
    red eagle-like crest; palms. Research-landmarks 7 (a commemorative square with a gate, an
    arcade and horse statues), Gidi version."""
    from .monuments import horse
    p = ccw(pts)
    _flat(mb, p, 0.05, 'pavers', hex_rgb('#d8cfba'), 0.4)
    m, L, W = _bbox_frame(p)
    white, red = hex_rgb('#f2efe6'), hex_rgb('#b0302a')
    for s in (-1, 1):  # the gate pylons with a white horse on each
        g = T(m, s * 7, -W / 2 + 2, 0)
        mb.box('paint', g @ Matrix.Translation((0, 0, 4.5)), white, 0.4, size=(2.6, 2.6, 9))
        horse(mb, g @ Matrix.Translation((0, 0, 9.0)) @ Matrix.Rotation(math.pi / 2, 4, 'Z'), white, 1.6, mat='paint', rearing=True)
    mb.box('paint', T(m, 0, -W / 2 + 2, 7.8), white, 0.4, size=(16.6, 1.6, 1.6))  # the arch's lintel
    parts.cyl(mb, 'paint', T(m, 0, -W / 2 + 1.15, 7.8) @ Matrix.Rotation(math.pi / 2, 4, 'X'), 1.1, 0.1, red, 0.3, seg=6)  # the crest
    n = max(6, int(L * 0.8 / 4))  # the long arcade along the far side
    ay = W / 2 - 4
    for k in range(n + 1):
        x = -L * 0.4 + k * L * 0.8 / n
        mb.box('paint', T(m, x, ay, 2.4), white, 0.4, size=(0.7, 0.7, 4.8))
    mb.box('paint', T(m, 0, ay, 5.1), white, 0.4, size=(L * 0.8 + 1, 4.0, 0.6))
    mb.box('paint', T(m, 0, ay + 2.0, 2.6), shade(white, 0.92), 0.4, size=(L * 0.8 + 1, 0.3, 5.2))  # its back wall
    if ch == 'old_island':  # The Reach, the owner's sculpture, stands in the middle of the square
        from .monuments import the_reach
        the_reach(mb, m @ Matrix.Translation((0, -W * 0.05, 0)), rng)
    for q in _scatter(p, int(_area(p) / 300), rng, pad=6):
        c0 = (m.inverted() @ Vector((q[0], q[1], 0))).to_2d()
        if ch == 'old_island' and abs(c0.x) < 22 and abs(c0.y) < 14:
            continue  # keep palms off the sculpture
        tree(mb, q[0], q[1], rng, kind='palm')


def fountain(mb, pts, rng, ch):
    c = centroid(pts)
    r = max(1.5, math.sqrt(_area(pts) / math.pi))
    parts.cyl(mb, 'concrete', Matrix.Translation((c[0], c[1], 0)), r, 0.6, hex_rgb('#e8e2d2'), 0.4, seg=24)
    mb.face([Vector((c[0] + math.cos(a) * (r - 0.25), c[1] + math.sin(a) * (r - 0.25), 0.55)) for a in (k / 24 * math.tau for k in range(24))], 'water', hex_rgb('#3a7aa0'), 0)
    parts.cyl(mb, 'concrete', Matrix.Translation((c[0], c[1], 0.5)), 0.4, 1.6, hex_rgb('#e8e2d2'), 0.4, seg=12, r2=0.25)
    parts.cyl(mb, 'water', Matrix.Translation((c[0], c[1], 2.1)), 0.1, 1.2, hex_rgb('#cfe8f5'), 0, seg=8, r2=0.4)


def pipeline(mb, pts, rng, ch):
    """The pipeline corridor: a cleared strip with the pipe on concrete saddles, tapped in places."""
    p = ccw(pts)
    _flat(mb, p, 0.03, 'mud', hex_rgb('#a8643a'), 0.8)
    m, L, W = _bbox_frame(p)
    parts.cyl(mb, 'steel', T(m, -L / 2, 0, 0.7) @ Matrix.Rotation(math.pi / 2, 4, 'Y'), 0.45, L, hex_rgb('#6a6a5a'), 0.8, seg=14)
    for k in range(int(L / 12)):
        mb.box('concrete', T(m, -L / 2 + 6 + k * 12, 0, 0.3), hex_rgb('#9c978c'), 0.7, size=(0.8, 1.4, 0.6))
    for _ in range(rng.randrange(0, 3)):  # a tap: hoses and jerrycans
        x = rng.between(-L / 2.5, L / 2.5)
        for k in range(5):
            mb.box('plastic', T(m, x + k * 0.35, 1.2, 0.2), hex_rgb('#e0b020'), 0.4, size=(0.3, 0.22, 0.4))


def livestock(mb, pts, rng, ch):
    p = ccw(pts)
    _flat(mb, p, 0.03, 'mud', hex_rgb('#6a4a30'), 0.9)
    from .kinds import cow
    for q in _scatter(p, max(3, int(_area(p) / 300)), rng, pad=2):
        cow(mb, Matrix.Translation((q[0], q[1], 0)) @ Matrix.Rotation(rng.between(0, math.tau), 4, 'Z'), rng)


def sawmill(mb, pts, rng, ch):
    p = ccw(pts)
    _flat(mb, p, 0.03, 'mud', hex_rgb('#b8925a'), 0.8)
    for q in _scatter(p, max(3, int(_area(p) / 600)), rng, pad=3):  # stacked planks
        for k in range(4):
            mb.box('wood', Matrix.Translation((q[0], q[1], 0.15 + k * 0.12)) @ Matrix.Rotation(rng.between(0, 0.3), 4, 'Z'), shade(hex_rgb('#a07a52'), rng.between(0.8, 1.1)), 0.6, size=(5, 1.4, 0.1))


def pond(mb, pts, rng, ch):
    _flat(mb, pts, 0.05, 'water', hex_rgb('#3a5a40'), 0)


def bunker(mb, pts, rng, ch):
    _flat(mb, pts, 0.05, 'ground', hex_rgb('#e8dcb0'), 0.2)


def under_bridge(mb, pts, rng, ch):
    _flat(mb, pts, 0.04, 'asphalt', hex_rgb('#4f4d48'), 0.85)


BUILDERS = {
    'pitch': pitch, 'court': court, 'pool': pool, 'golf course': golf_course, 'stadium': stadium, 'airfield': airfield,
    'tank farm': tank_farm, 'landfill': landfill, 'waterworks': waterworks, 'prison': prison, 'barracks': barracks_ground,
    'market': market_ground, 'plazas': lambda mb, p, r, c: paved(mb, p, r, c, '#bdb5a8'), 'motor park': motor_park,
    'bus terminal': lambda mb, p, r, c: yard(mb, p, r, c, '#4f4d48', 'asphalt'), 'lorry park': lambda mb, p, r, c: yard(mb, p, r, c, '#9c6a48'),
    'truck park': lambda mb, p, r, c: yard(mb, p, r, c, '#9c6a48'), 'container yard': lambda mb, p, r, c: yard(mb, p, r, c, '#8f8a80', 'concrete'),
    'industrial': lambda mb, p, r, c: yard(mb, p, r, c, '#8f8a80', 'concrete'), 'station': lambda mb, p, r, c: paved(mb, p, r, c),
    'under bridge': under_bridge, 'school': lambda mb, p, r, c: yard(mb, p, r, c, '#d8c9a3', 'ground'), 'forecourt': lambda mb, p, r, c: paved(mb, p, r, c, '#d8cfba'),
    'square': square, 'fountain': fountain, 'garden': green, 'park': green, 'green': lambda mb, p, r, c: green(mb, p, r, c, trees=False),
    'government': green, 'club': green, 'compound': lambda mb, p, r, c: paved(mb, p, r, c, '#bdb5a8'), 'enclave': green,
    'estate': lambda mb, p, r, c: green(mb, p, r, c), 'villas': green, 'palace': lambda mb, p, r, c: paved(mb, p, r, c, '#d8c49a'),
    'pipeline': pipeline, 'livestock': livestock, 'sawmill': sawmill, 'pond': pond, 'bunker': bunker,
}


def build(mb, kind, pts, rng, ch):
    fn = BUILDERS.get(kind)
    if fn:
        fn(mb, [tuple(p) for p in pts], rng, ch)
        return True
    return False
