"""A walk-up's street face, close up (the facade pass, 22 Oct 2026): what Balogun and Isale Eko faces carry on top of the
wall, its windows and its balconies. Every piece is a record in the building's `facade` block (KIT.md section 12); this
draws them and decides nothing. Face-based records name the face (its index in the footprint, as `faces` lists them) and
u, how far along it from its middle; z is up from the ground.

- slab_edges: each floor's slab nosing standing out of the face, and the dark drip band it leaves under it.
- addons: rooms built out from the face on steel struts (zinc, plank, block or render), with their own window and roof.
- enclosed: a balcony's front closed in up to the slab above (louvres, zinc, block or glass) over its rail.
- pipes: down pipes and service pipes on the face. wires: cables (polylines in the spot's frame) run over and down it.
- signs: painted boards fixed to the face, with their colour bands. banners: cloth hung on the face, sagging.
- laundry: lines (two points) with each thing hung on them. tanks: water tanks on the roof. tarps: sheets over the roof.
- bars: steel members (a rooftop frame, a rail). roof_rooms: rooms built on the roof.
"""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import at, hex_rgb, shade

STRUT = hex_rgb('#3a2c24')
MORTAR = hex_rgb('#5b564d')


def _c(v, default='#888888'):
    return hex_rgb(v or default) if isinstance(v, str) or v is None else tuple(v)


def _q(mb, F, u0, u1, z0, z1, y, mat, col, wear=0.6):
    """A flat panel on frame F from u0..u1, z0..z1, y out. col: one colour, or four (bottom left, bottom right, top
    right, top left)."""
    mb.face([F @ Vector((u0, y, z0)), F @ Vector((u1, y, z0)), F @ Vector((u1, y, z1)), F @ Vector((u0, y, z1))], mat, col, wear)


def slab_edge(mb, F, wx, r):
    """A floor slab's nosing: a concrete lip out of the face, its soffit in shade, and a dark band under it where the
    rain drips off its edge and runs back down the wall."""
    u0, u1, z, out, h = r['u0'], r['u1'], r['z'], r.get('out', 0.2), r.get('h', 0.2)
    col = _c(r.get('col'), '#8d877b')
    mb.box('concrete', at(F, (u0 + u1) / 2, out / 2, z), col, 0.8, size=(u1 - u0, out, h))
    d = r.get('drip', 0.45)
    if d > 0:
        k = r.get('dark', 0.55)
        seen = lambda u, zz: wx.seen(*(F @ Vector((u, 0, zz))))
        n = max(1, round((u1 - u0) / 1.5))
        for i in range(n):
            a, b = u0 + (u1 - u0) * i / n, u0 + (u1 - u0) * (i + 1) / n
            top = [shade(seen(a, z - h / 2), k), shade(seen(b, z - h / 2), k)]
            _q(mb, F, a, b, z - h / 2 - d, z - h / 2, 0.012, 'paint', [seen(a, z - h / 2 - d), seen(b, z - h / 2 - d), top[1], top[0]], r.get('wear', 0.25))   # low wear: the paint's chalky fade would lift the dark


def window(mb, F, u, z, r, base, wear):
    """One window from its record: kind louvre, casement or sliding (glass in a frame), bars (with burglar bars over),
    boarded (planks over the hole), cloth (a curtain pulled across the glass), dark (an open hole); w, h; bars, cloth
    colours; bar style. base: the building's own window spec."""
    kind = r.get('kind')
    spec = dict(base, w=r.get('w', base['w']), h=r.get('h', base['h']))
    w, h = spec['w'], spec['h']
    if kind in ('louvre', 'casement', 'sliding', 'bars', 'cloth'):
        spec['type'] = 'louvre' if kind in ('bars', 'cloth') and base['type'] == 'louvre' else (kind if kind in ('louvre', 'casement', 'sliding') else base['type'])
    if r.get('frame'):
        spec['frame'] = _c(r['frame'])
    if kind == 'bars' or r.get('bars'):
        spec['bars'] = r.get('bar_style', 'grid')
        spec['bar_col'] = _c(r.get('bar_col'), '#3b2a22')
    if kind == 'dark':
        mb.box('paint', at(F, u, 0.01, z), spec['frame'], wear, size=(w + 0.12, 0.05, h + 0.12), skip=('-y',))
        _q(mb, F, u - w / 2, u + w / 2, z - h / 2, z + h / 2, 0.04, 'paint', (0.02, 0.018, 0.016), 0)
        return
    if kind == 'boarded':
        _q(mb, F, u - w / 2, u + w / 2, z - h / 2, z + h / 2, 0.02, 'paint', (0.03, 0.026, 0.022), 0)
        for i, (f, dz) in enumerate(r.get('boards', [[0.9, 0.0]] * 4)):
            n = len(r.get('boards', [0] * 4))
            uu = u - w / 2 + (i + 0.5) * w / n
            mb.box('wood', at(F, uu, 0.05, z + dz, ry=r.get('tilt', 0.0) * (1 if i % 2 else -1)), shade(_c(r.get('col'), '#6a5040'), f), 0.8, size=(w / n * 0.96, 0.025, h + 0.08))
        mb.box('wood', at(F, u, 0.075, z + h * 0.25), shade(_c(r.get('col'), '#6a5040'), 0.8), 0.8, size=(w + 0.1, 0.025, 0.1))
        return
    parts.window(mb, F, u, z, spec)
    if kind == 'cloth':   # a curtain behind the glass, pulled across most of it
        c = _c(r.get('cloth'), '#7a2e3a')
        cov = r.get('cover', 0.8)
        _q(mb, F, u - w / 2, u - w / 2 + w * cov, z - h / 2 + 0.02, z + h / 2 - 0.02, 0.03, 'cloth', c, 0.3)
    if r.get('sheet'):   # a sheet of cardboard or zinc pushed up behind the louvres
        s = r['sheet']
        _q(mb, F, u - w / 2 + s[0] * w, u - w / 2 + s[1] * w, z - h / 2 + s[2] * h, z - h / 2 + s[3] * h, 0.035, 'paint', _c(s[4] if len(s) > 4 else None, '#9a8a70'), 0.6)


def addon(mb, F, r, wear):
    """A room built out from the face: a box from z0 up h, out from the wall, on two or three steel struts back to the
    wall below it; its wall in zinc sheets, planks, block or render; a window or a dark opening in its front; a flat
    sheet roof, falling outward."""
    u, w, z0, h, out = r['u'], r['w'], r['z0'], r['h'], r['out']
    wall = r.get('wall', 'zinc')
    col = _c(r.get('col'), '#6b5a4a')
    mat = {'zinc': 'zinc', 'plank': 'wood', 'block': 'block', 'render': 'paint'}[wall]
    mb.box('concrete', at(F, u, out / 2, z0 + 0.05), shade(col, 0.6) if wall != 'block' else MORTAR, wear, size=(w + 0.1, out + 0.05, 0.1))   # its floor
    if wall in ('zinc', 'plank'):   # sheets or planks, each its own shade, standing side by side
        pw = 0.8 if wall == 'zinc' else 0.22
        n = max(1, round(w / pw))
        shades = r.get('shades') or [1.0] * n
        for i in range(n):
            f = shades[i % len(shades)]
            uu = u - w / 2 + (i + 0.5) * w / n
            mb.box(mat, at(F, uu, out, z0 + h / 2), shade(col, f), wear, size=(w / n * 1.01, 0.03 + 0.008 * (i % 2), h))
        for s_ in (-1, 1):
            n2 = max(1, round(out / pw))
            for i in range(n2):
                yy = (i + 0.5) * out / n2
                mb.box(mat, at(F, u + s_ * w / 2, yy, z0 + h / 2), shade(col, shades[(i + 1) % len(shades)] * 0.9), wear, size=(0.03, out / n2 * 1.01, h))
    else:
        mb.box(mat, at(F, u, out / 2, z0 + h / 2), col, wear, size=(w, out, h), skip=('-y',))
    win = r.get('win')
    if win:
        ww, wh, wz = win.get('w', 0.9), win.get('h', 0.9), z0 + win.get('z', h * 0.55)
        wu = u + win.get('du', 0.0)
        if win.get('kind') == 'louvre':
            parts.window(mb, F @ Matrix.Translation((0, out + 0.02, 0)), wu, wz,
                         dict(type='louvre', w=ww, h=wh, frame=_c(win.get('frame'), '#4a4038'), glass=hex_rgb('#26323a'), mullion=hex_rgb('#8a8c8e'), bars='none', bar_col=(0, 0, 0), wear=wear))
        else:
            _q(mb, F, wu - ww / 2, wu + ww / 2, wz - wh / 2, wz + wh / 2, out + 0.04, 'paint', (0.02, 0.018, 0.016), 0)
            if win.get('cloth'):
                _q(mb, F, wu - ww / 2, wu + ww * 0.15, wz - wh / 2, wz + wh / 2, out + 0.045, 'cloth', _c(win['cloth']), 0.3)
    rc = _c(r.get('roof_col'), '#6a4a38')
    tilt = math.atan2(0.15, out + 0.3)
    mb.box('zinc', at(F, u, (out + 0.3) / 2, z0 + h + 0.1, rx=-tilt), rc, 0.85, size=(w + 0.3, out + 0.35, 0.02))
    for k in range(r.get('struts', 2)):   # struts from the floor's outer edge back down to the wall
        uu = u - w / 2 + 0.1 + (w - 0.2) * (k / max(1, r.get('struts', 2) - 1))
        parts.bar(mb, 'steel', F @ Vector((uu, out - 0.05, z0)), F @ Vector((uu, 0.02, z0 - min(1.2, out * 1.1))), 0.06, STRUT, 0.8)
        parts.bar(mb, 'steel', F @ Vector((uu, 0.02, z0)), F @ Vector((uu, out - 0.05, z0)), 0.06, STRUT, 0.8)


def enclosed(mb, F, r, wear):
    """A balcony's front closed in above its rail up to the slab over it: louvre blades, zinc sheets, a slack plastic
    sheet, a block wall with a window in it, or glass in frames."""
    u, w, z0, h, out = r['u'], r['w'], r['z0'], r['h'], r['out']
    kind = r.get('kind', 'louvre')
    col = _c(r.get('col'), '#4a4038')
    if r.get('floor'):   # no balcony under it on the map: its own slab, the solid upstand over the slab edge, and the slab over it
        mb.box('concrete', at(F, u, out / 2, z0 - 0.1), hex_rgb('#8d877b'), wear, size=(w + 0.1, out + 0.05, 0.2))
        mb.box('paint', at(F, u, out, z0 + 0.35), _c(r['floor']), wear, size=(w + 0.1, 0.1, 0.9))
        mb.box('concrete', at(F, u, out / 2, z0 + h + 0.1), hex_rgb('#8d877b'), wear, size=(w + 0.1, out + 0.05, 0.2))
        z0, h = z0 + 0.8, h - 0.8
    if kind == 'block':
        mb.box('paint', at(F, u, out, z0 + h / 2), col, wear, size=(w, 0.12, h))
        for wu in r.get('windows', []):
            parts.window(mb, F @ Matrix.Translation((0, out + 0.06, 0)), u + wu, z0 + h * 0.55,
                         dict(type='louvre', w=0.9, h=min(1.0, h * 0.6), frame=shade(col, 0.8), glass=hex_rgb('#26323a'), mullion=hex_rgb('#8a8c8e'), bars='none', bar_col=(0, 0, 0), wear=wear))
        return
    n = max(1, round(w / r.get('bay', 1.0)))
    shades = r.get('shades') or [1.0]
    for i in range(n):
        uu = u - w / 2 + (i + 0.5) * w / n
        bw = w / n
        f = shades[i % len(shades)]
        mb.box('steel', at(F, uu - bw / 2, out, z0 + h / 2), shade(col, 0.7), wear, size=(0.05, 0.06, h))   # a mullion
        if kind == 'louvre':
            nb = max(4, round(h / 0.12))
            for j in range(nb):
                zz = z0 + (j + 0.5) * h / nb
                mb.box('glass', at(F, uu, out, zz, rx=-0.5), shade(hex_rgb('#2a343a'), f), 0, size=(bw * 0.92, 0.004, h / nb * 1.05))
            mb.box('steel', at(F, uu, out - 0.01, z0 + h / 2), shade(col, 0.6), wear, size=(bw, 0.02, 0.04))
        elif kind == 'sheet':   # a plastic sheet or tarpaulin tied across the opening, hanging slack
            mb.face([F @ Vector((uu - bw / 2, out - 0.04, z0)), F @ Vector((uu + bw / 2, out - 0.04, z0)), F @ Vector((uu + bw / 2, out - 0.02, z0 + h)), F @ Vector((uu - bw / 2, out - 0.02, z0 + h))],
                    'cloth', shade(col, f), 0.2)
        elif kind == 'zinc':
            mb.box('zinc', at(F, uu, out, z0 + h / 2), shade(col, f), 0.9, size=(bw * 1.01, 0.02, h))
        else:   # glass in frames
            _q(mb, F, uu - bw / 2, uu + bw / 2, z0, z0 + h, out, 'glass', shade(hex_rgb('#26323a'), f), 0)
    mb.box('steel', at(F, u, out, z0 + h), shade(col, 0.7), wear, size=(w, 0.07, 0.06))


def pipe(mb, F, r):
    """A pipe down the face (and its bend into the wall at the top)."""
    u, z0, z1 = r['u'], r['z0'], r['z1']
    rad, y = r.get('r', 0.04), r.get('out', 0.06)
    col = _c(r.get('col'), '#2c2c2c')
    parts.bar(mb, 'plastic' if r.get('pvc', True) else 'steel', F @ Vector((u, y, z0)), F @ Vector((u, y, z1)), rad * 2, col, 0.7)
    if r.get('bend', True):
        parts.bar(mb, 'plastic', F @ Vector((u, y, z1)), F @ Vector((u, 0.0, z1 + 0.15)), rad * 2, col, 0.7)


def wire(mb, r):
    """A cable through its points, sagging between them by sag (m, at each span's middle)."""
    pts = [Vector(p) for p in r['pts']]
    t, col, sag = r.get('r', 0.012) * 2, _c(r.get('col'), '#151515'), r.get('sag', 0.0)
    for a, b in zip(pts, pts[1:]):
        if sag > 0:
            n = 6
            pp = [a + (b - a) * (i / n) - Vector((0, 0, sag * 4 * (i / n) * (1 - i / n))) for i in range(n + 1)]
            for p, q in zip(pp, pp[1:]):
                parts.bar(mb, 'rubber', p, q, t, col, 0.3)
        else:
            parts.bar(mb, 'rubber', a, b, t, col, 0.3)


def sign(mb, F, r, wear):
    """A painted board on the face: its ground colour, colour bands across it (each [colour, from, to] up the board, or
    a block [colour, u0, u1, z0, z1] in board fractions), on a thin frame, out from the wall."""
    u, z, w, h, y = r['u'], r['z'], r['w'], r['h'], r.get('out', 0.08)
    col = _c(r.get('col'), '#e8e2d0')
    if r.get('sag') or r.get('torn') or r.get('peel') or r.get('paper') or 't' in r:
        return _sheet(mb, F, r, wear, u, z, w, h, y, col)
    mb.box('wood', at(F, u, y, z), shade(col, 0.6), wear, size=(w + 0.06, 0.04, h + 0.06))
    _q(mb, F, u - w / 2, u + w / 2, z - h / 2, z + h / 2, y + 0.021, 'paint', col, r.get('wear', wear))
    for bd in r.get('bands', []):
        if len(bd) == 3:
            c, f0, f1 = bd
            _q(mb, F, u - w / 2 + 0.03, u + w / 2 - 0.03, z - h / 2 + h * f0, z - h / 2 + h * f1, y + 0.024, 'paint', _c(c), r.get('wear', wear))
        else:
            c, a, b, f0, f1 = bd
            _q(mb, F, u - w / 2 + w * a, u - w / 2 + w * b, z - h / 2 + h * f0, z - h / 2 + h * f1, y + 0.026, 'paint', _c(c), r.get('wear', wear))
    for s_ in r.get('legs', []):   # brackets back to the wall
        parts.bar(mb, 'steel', F @ Vector((u + s_ * w / 2 * 0.8, y, z - h / 2)), F @ Vector((u + s_ * w / 2 * 0.8, 0.0, z - h / 2 - 0.3)), 0.03, STRUT, 0.8)


def _sheet(mb, F, r, wear, u, z, w, h, y, col):
    """A board or a pasted poster with a body: a board t thick on its frame (or paper, flat on the wall), bulging out by
    sag in its middle, its printed blocks (bands) following the bulge, torn away up from its foot where the map says
    (torn: [from, to, how far up] in fractions of its width and height, ragged), and a corner peeled off and folded out
    (peel: [corner tl, tr, bl or br, size m])."""
    t, sag, paper = r.get('t', 0.004 if r.get('paper') else 0.04), r.get('sag', 0.0), r.get('paper', False)
    nu, nv = 10, 5
    ww = r.get('wear', wear)

    def cut(fu):   # how far up the foot is torn at fu across
        for a, b, dep in r.get('torn', []):
            if a <= fu <= b:
                k = int(fu * nu * 2) % 3
                return dep * (1.0, 0.65, 0.85)[k]
        return 0.0

    def P(fu, fv, dy):
        bulge = sag * math.sin(math.pi * fu) * math.sin(math.pi * fv)
        return F @ Vector((u - w / 2 + w * fu, y + dy + bulge, z - h / 2 + h * fv))

    def patch(a, b, f0, f1, dy, c, mat='paint'):
        for i in range(nu):
            u0, u1 = a + (b - a) * i / nu, a + (b - a) * (i + 1) / nu
            fm = (u0 + u1) / 2
            v0 = max(f0, cut(fm))
            if v0 >= f1:
                continue
            mb.face([P(u0, v0, dy), P(u1, v0, dy), P(u1, f1, dy), P(u0, f1, dy)], mat, c, ww)
    if not paper:   # the board: its edge and back, then its face
        mb.box('wood', at(F, u, y - t / 2, z), shade(col, 0.6), wear, size=(w + 0.06, t, h + 0.06))
    patch(0.0, 1.0, 0.0, 1.0, 0.002 + (0 if paper else 0.001), col)
    for k, bd in enumerate(r.get('bands', [])):
        c, a, b, f0, f1 = (bd[0], 0.03, 0.97, bd[1], bd[2]) if len(bd) == 3 else bd
        patch(a, b, f0, f1, 0.004 + 0.001 * k, _c(c))
    if r.get('peel'):   # a corner come away, folded out from the wall
        cn, sz = r['peel']
        fu, fv = {'tl': (0, 1), 'tr': (1, 1), 'bl': (0, 0), 'br': (1, 0)}[cn]
        su, sv = (1 if fu == 0 else -1) * sz / w, (1 if fv == 0 else -1) * sz / h
        a_, b_, c_ = P(fu, fv, 0.009), P(fu + su, fv, 0.009), P(fu, fv + sv, 0.009)
        tip = F @ Vector((u - w / 2 + w * (fu + su * 0.4), y + sz * 0.7, z - h / 2 + h * (fv + sv * 0.4)))
        mb.face([b_, c_, tip], 'paint', hex_rgb('#e4dfd2'), ww)
        mb.face([tip, c_, b_], 'paint', hex_rgb('#d6d0c2'), ww)
        mb.face([a_, b_, c_], 'paint', shade(hex_rgb('#8a8174'), 0.8), 0.8)   # the wall showing under it


def banner(mb, F, r):
    """Cloth hung on the face from its top corners: sagging in the middle, a band of colour across it."""
    u, z, w, h, y = r['u'], r['z'], r['w'], r['h'], r.get('out', 0.1)
    col, sag = _c(r.get('col'), '#c62828'), r.get('sag', 0.08)
    n = 6
    for i in range(n):
        a, b = u - w / 2 + w * i / n, u - w / 2 + w * (i + 1) / n
        sa = sag * math.sin(math.pi * i / n)
        sb = sag * math.sin(math.pi * (i + 1) / n)
        yy = y + 0.02 * (i % 2)
        mb.face([F @ Vector((a, yy, z - h - sa)), F @ Vector((b, yy, z - h - sb)), F @ Vector((b, yy, z - sb * 0.4)), F @ Vector((a, yy, z - sa * 0.4))], 'cloth', col, 0.3)
        if r.get('band'):
            c, f0, f1 = r['band']
            mb.face([F @ Vector((a, yy + 0.004, z - h * f1 - sa * 0.8)), F @ Vector((b, yy + 0.004, z - h * f1 - sb * 0.8)),
                     F @ Vector((b, yy + 0.004, z - h * f0 - sb * 0.6)), F @ Vector((a, yy + 0.004, z - h * f0 - sa * 0.6))], 'cloth', _c(c), 0.3)


def laundry(mb, r):
    """A line from a to b (the spot's frame), sagging, with each thing hung on it: at t along, w wide, h long, colour."""
    a, b = Vector(r['a']), Vector(r['b'])
    sag = r.get('sag', 0.12)
    pt = lambda t: a + (b - a) * t - Vector((0, 0, sag * 4 * t * (1 - t)))
    n = 8
    for i in range(n):
        parts.bar(mb, 'rubber', pt(i / n), pt((i + 1) / n), 0.012, hex_rgb('#d8d4c8'), 0.2)
    d = (b - a)
    d.z = 0
    d.normalize()
    side = Vector((-d.y, d.x, 0)) * 0.01
    for it in r['items']:
        t, w, h = it['t'], it['w'], it['h']
        p = pt(t)
        c = _c(it['col'])
        q = [p - d * w / 2, p + d * w / 2, p + d * w / 2 - Vector((0, 0, h)), p - d * w / 2 - Vector((0, 0, h * it.get('drop', 1.0)))]
        mb.face([q[3] + side, q[2] + side, q[1] + side, q[0] + side], 'cloth', c, 0.3)
        mb.face([q[0] - side, q[1] - side, q[2] - side, q[3] - side], 'cloth', shade(c, 0.85), 0.3)


def tank(mb, r):
    """A water tank on the roof: a ribbed plastic drum (black, blue or the old cream ones) on a block plinth or steel
    stand, its lid on top."""
    x, y, z, rad, h = r['x'], r['y'], r['z'], r['r'], r['h']
    col = _c(r.get('col'), '#1d1d1f')
    st = r.get('stand', 0.4)
    if st > 0:
        if r.get('steel'):
            for sx in (-1, 1):
                for sy in (-1, 1):
                    parts.bar(mb, 'steel', (x + sx * rad * 0.7, y + sy * rad * 0.7, z), (x + sx * rad * 0.7, y + sy * rad * 0.7, z + st), 0.06, STRUT, 0.8)
            mb.box('steel', at(Matrix(), x, y, z + st), STRUT, 0.8, size=(rad * 1.6, rad * 1.6, 0.06))
        else:
            mb.box('block', at(Matrix(), x, y, z + st / 2), hex_rgb('#7b766a'), 0.8, size=(rad * 1.9, rad * 1.9, st))
    M = at(Matrix(), x, y, z + st)
    for k in range(4):   # the ribs: a ring every quarter
        parts.cyl(mb, 'plastic', at(M, 0, 0, h * k / 4), rad * (1.0 if k % 2 == 0 else 0.97), h / 4, shade(col, 1.0 if k % 2 == 0 else 0.92), 0.4, seg=20, caps=(k == 0, False))
    parts.cyl(mb, 'plastic', at(M, 0, 0, h), rad * 0.97, 0.06, shade(col, 0.95), 0.4, seg=20, r2=rad * 0.35)
    parts.cyl(mb, 'plastic', at(M, 0, 0, h + 0.06), rad * 0.3, 0.06, shade(col, 0.8), 0.4, seg=12)


def tarp(mb, r):
    """A sheet over a roof: its four corners (the spot's frame), sagging in its middle by sag, with a fold across it."""
    p = [Vector(q) for q in r['pts']]
    col, sag = _c(r.get('col'), '#2f5fa8'), r.get('sag', 0.15)
    n = 4
    grid = [[p[0] + (p[1] - p[0]) * (i / n) + ((p[3] + (p[2] - p[3]) * (i / n)) - (p[0] + (p[1] - p[0]) * (i / n))) * (j / n)
             - Vector((0, 0, sag * 16 * (i / n) * (1 - i / n) * (j / n) * (1 - j / n))) for j in range(n + 1)] for i in range(n + 1)]
    for i in range(n):
        for j in range(n):
            f = 1.0 - 0.08 * ((i + j) % 2)
            mb.face([grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]], 'woven', shade(col, f), 0.5)
    for a, b in r.get('ropes', []):   # weights or ropes holding it down: a tyre or block at each corner named
        q = p[a]
        mb.box('rubber' if b == 'tyre' else 'block', at(Matrix(), q.x, q.y, q.z + 0.08), (0.08, 0.08, 0.08) if b == 'tyre' else hex_rgb('#7b766a'), 0.5, size=(0.4, 0.4, 0.16))


def bars(mb, r):
    """Steel members as the map has them (a rooftop frame, a rail, a stand): each [x0, y0, z0, x1, y1, z1] in the spot's
    frame, all of one size t and colour."""
    t, col = r.get('t', 0.05), _c(r.get('col'), '#6a3a26')
    for m in r['members']:
        parts.bar(mb, 'steel', m[:3], m[3:6], t, col, r.get('wear', 0.8))


def roof_room(mb, r, wear):
    """A room built on the roof (the spot's frame, x0..x1, y0..y1, from z up h): block or zinc walls, a dark door or
    window on the face named, a sheet roof."""
    x0, y0, x1, y1, z, h = r['x0'], r['y0'], r['x1'], r['y1'], r['z'], r['h']
    col = _c(r.get('col'), '#a89c84')
    mat = {'zinc': 'zinc', 'plank': 'wood', 'block': 'block', 'render': 'paint'}[r.get('wall', 'render')]
    mb.box(mat, at(Matrix(), (x0 + x1) / 2, (y0 + y1) / 2, z + h / 2), col, wear, size=(x1 - x0, y1 - y0, h))
    for o in r.get('openings', []):   # [x, y, w, h, side: +1 faces +y, -1 faces -y]
        x, y, w_, h_, sd = o
        mb.face([(x - w_ / 2, y + sd * 0.01, z), (x + w_ / 2, y + sd * 0.01, z), (x + w_ / 2, y + sd * 0.01, z + h_), (x - w_ / 2, y + sd * 0.01, z + h_)][::-sd],
                'paint', (0.02, 0.018, 0.016), 0)
    mb.box('zinc', at(Matrix(), (x0 + x1) / 2, (y0 + y1) / 2, z + h + 0.05), _c(r.get('roof_col'), '#6a4a38'), 0.85, size=(x1 - x0 + 0.4, y1 - y0 + 0.4, 0.03))


def panel(mb, F, r):
    """A corrugated zinc sheet nailed over the face (a shack's or a fence's walls): u0..u1 along, z0..z1 up, out from
    the wall; its colour, a rust colour bled up from its foot over the share rust_h of its height, and its corrugation
    (ribs every 0.076 m: the sheet's own profile, like the roof's)."""
    u0, u1, z0, z1, y = r['u0'], r['u1'], r['z0'], r['z1'], r.get('out', 0.03)
    col = _c(r['col'])
    rust = _c(r.get('rust'), '#6b3a22')
    zr = z0 + (z1 - z0) * r.get('rust_h', 0.0)
    n = max(2, int((u1 - u0) / 0.038))
    for i in range(n):
        a, b = u0 + (u1 - u0) * i / n, u0 + (u1 - u0) * (i + 1) / n
        f = 1.0 if i % 2 == 0 else 0.8
        yy = y + (0.012 if i % 2 == 0 else 0.0)
        if zr > z0 + 0.01:
            _q(mb, F, a, b, z0, zr, yy, 'zinc', shade(rust, f), 0.9)
        _q(mb, F, a, b, zr, z1, yy, 'zinc', shade(col, f), r.get('wear', 0.7))


def draw(mb, fs, wx, fc, wear):
    """Everything in one building's facade block."""
    for r in fc.get('slab_edges', []):
        slab_edge(mb, fs[r['face']][4], wx, r)
    for r in fc.get('addons', []):
        addon(mb, fs[r['face']][4], r, wear)
    for r in fc.get('enclosed', []):
        enclosed(mb, fs[r['face']][4], r, wear)
    for r in fc.get('pipes', []):
        pipe(mb, fs[r['face']][4], r)
    for r in fc.get('wires', []):
        wire(mb, r)
    for r in fc.get('signs', []):
        sign(mb, fs[r['face']][4], r, wear)
    for r in fc.get('banners', []):
        banner(mb, fs[r['face']][4], r)
    for r in fc.get('laundry', []):
        laundry(mb, r)
    for r in fc.get('tanks', []):
        tank(mb, r)
    for r in fc.get('tarps', []):
        tarp(mb, r)
    for r in fc.get('bars', []):
        bars(mb, r)
    for r in fc.get('panels', []):
        panel(mb, fs[r['face']][4], r)
    for r in fc.get('roof_rooms', []):
        roof_room(mb, r, wear)
