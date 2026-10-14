"""Build part of Gidi in Blender from the generated map data, every object styled by rules.

blender -b --factory-startup -P blender/generate.py -- --district maze --at 2620,4392 --r 110 --out blender/out/ladi-lane
  [--render overview,street,main] [--glb] [--blend]

Reads web/gen-<district>.json (x east, y south, metres). Each building's look comes from its own
attributes (kind, storeys, district, facing street, distance to a main road), through
gidi_kit.rules, with a seed from its district and index: rebuilds are identical.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import scene  # noqa: E402
from gidi_kit import archetypes, parts, registry  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng, ccw, edge_out, hex_rgb, offset  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
from gidi_kit.rules import UNFINISHED_SHARE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = {}
for i, a in enumerate(args):
    if a.startswith('--'):
        opt[a] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('--') else True
district = opt.get('--district', 'maze')
cx, cy = (float(v) for v in opt.get('--at', '2620,4392').split(','))
R = float(opt.get('--r', 110))
out = opt.get('--out', os.path.join(ROOT, 'blender', 'out', district))
os.makedirs(out, exist_ok=True)

D = json.load(open(os.path.join(ROOT, 'web', f'gen-{district}.json')))
P = lambda p: (p[0] - cx, -(p[1] - cy))  # data -> Blender (y north)
WIDTH = {'main': 14.0, 'street': 7.0, 'lane': 3.5, 'path': 2.5}


def dist_seg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy or 1
    t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2))
    return math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy))


def dist_line(p, pts):
    return min(dist_seg(p, pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def in_poly(p, poly):
    ins, j = False, len(poly) - 1
    for i in range(len(poly)):
        xi, yi, xj, yj = poly[i][0], poly[i][1], poly[j][0], poly[j][1]
        if (yi > p[1]) != (yj > p[1]) and p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi:
            ins = not ins
        j = i
    return ins


# ---------------------------------------------------------------- roads
roads = []
for m in D.get('mains', []):
    roads.append(dict(k='main', pts=[P(p) for p in m['pts']], name=m.get('name')))
for s in D.get('streets', []):
    roads.append(dict(k='street', pts=[P(p) for p in s]))
for s in D.get('lanes', []):
    roads.append(dict(k='lane', pts=[P(p) for p in s]))
for s in D.get('paths', []):
    roads.append(dict(k='path', pts=[P(p) for p in s['pts']]))
for r in roads:
    r['w'] = WIDTH[r['k']]
roads = [r for r in roads if any(math.hypot(*p) < R + 120 for p in r['pts']) or dist_line((0, 0), r['pts']) < R + 60]


def near_road(p, pad=0.0, kinds=('main', 'street', 'lane', 'path')):
    return any(r['k'] in kinds and dist_line(p, r['pts']) < r['w'] / 2 + pad for r in roads)


# ---------------------------------------------------------------- buildings and their attributes
blds = []
for i, b in enumerate(D['buildings']):
    poly = ccw([P(p) for p in b[1:]])
    c = (sum(p[0] for p in poly) / 4, sum(p[1] for p in poly) / 4)
    if math.hypot(*c) > R:
        continue
    blds.append(dict(i=i, kind=b[0], poly=poly, c=c, storeys=D['storeys'][i]))
print('buildings', len(blds))
polys = [b['poly'] for b in blds]


def attributes(b):
    poly = b['poly']
    best, facing = 1e9, 0
    for e in range(4):
        a, q = poly[e], poly[(e + 1) % 4]
        mid = ((a[0] + q[0]) / 2, (a[1] + q[1]) / 2)
        d = min((dist_line(mid, r['pts']) - r['w'] / 2 for r in roads if r['k'] in ('main', 'street')), default=99)
        if d < best:
            best, facing = d, e
    mains = [r for r in roads if r['k'] == 'main']
    near_main = min((dist_line(b['c'], r['pts']) - 7 for r in mains), default=999)
    rng = Rng(district, 'unfinished', b['i'])
    a = dict(kind=b['kind'], storeys=b['storeys'], district=district, poly=poly, facing=facing, frontage=best, near_main=near_main,
             name=f"{district}_{b['kind']}_{b['i']}", unfinished=b['storeys'] >= 2 and rng.chance(UNFINISHED_SHARE.get(district, 0.01)))
    others = [p for p in polys if p is not poly]
    a['wall_poly'] = offset(poly, 2.0)
    a['wall_skip'] = lambda m, others=others: near_road(m, 0.8) or any(in_poly(m, o) for o in others)
    return a


sc = scene.reset()
col = bpy.data.collections.new(district)
sc.collection.children.link(col)
counts = {}
shops = []
for b in blds:
    a = attributes(b)
    rng = Rng(district, b['i'])
    k = b['kind']
    fn = registry.builder(k)
    if fn is None:  # kinds without an archetype yet: a plain house so the area is complete
        fn, a = archetypes.house, dict(a, kind='back')
    ob, spec = fn(a, rng, col)
    if fn is archetypes.house:
        b['H'] = spec['storeys'] * 3.1 + spec.get('lift', 0)
        if spec['shop']:
            e = a['facing']
            pa, pb = a['poly'][e], a['poly'][(e + 1) % 4]
            shops.append(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2))
    counts[k] = counts.get(k, 0) + 1
print('built', counts)

# ---------------------------------------------------------------- ground, roads and street life
from gidi_kit import street  # noqa: E402
from gidi_kit.rules import CHARACTER, FLOOD, STREET  # noqa: E402
ch = CHARACTER.get(district, 'dense')
ST, flood = STREET[ch], FLOOD.get(district, 0.2)
wealth = {'elite': 0.85, 'civic': 0.55, 'dense': 0.3, 'sprawl': 0.35, 'old_island': 0.3, 'waterfront': 0.1, 'port': 0.3}[ch]
clip = R + 40
soil = hex_rgb('#d8c9a3' if ch in ('old_island', 'waterfront', 'elite') else '#b5714a')  # pale sand on the island and coast, red earth inland

mb = MeshBuilder()
G = R + 160
mb.face([(-G, -G, 0), (G, -G, 0), (G, G, 0), (-G, G, 0)], 'ground', soil, 0.5)


def ribbon(pts, w, z, colr, wear, mat='ground'):
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy) or 1
        nx, ny = -dy / l * w / 2, dx / l * w / 2
        ex, ey = dx / l * w / 2, dy / l * w / 2
        mb.face([(a[0] - ex + nx, a[1] - ey + ny, z), (a[0] - ex - nx, a[1] - ey - ny, z), (b[0] + ex - nx, b[1] + ey - ny, z), (b[0] + ex + nx, b[1] + ey + ny, z)], mat, colr, wear)


def clip_line(pts, rad, piece=8.0):
    """Cut a polyline to the parts within rad of the centre."""
    out, cur = [], []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.dist(a, b)
        n = max(1, int(L / piece))
        for k in range(n):
            p0 = (a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
            p1 = (a[0] + (b[0] - a[0]) * (k + 1) / n, a[1] + (b[1] - a[1]) * (k + 1) / n)
            if math.hypot((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2) < rad:
                if not cur:
                    cur = [p0]
                cur.append(p1)
            elif cur:
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    return out


in_building = lambda p, pad=0.3: any(in_poly(p, offset(q, pad)) for q in polys)
sm = MeshBuilder()
poles = []
for ri, r in enumerate(roads):
    rr = Rng(district, 'road', ri)
    cond = street.road_condition(r, ch, wealth, flood, rr)
    for piece in clip_line(r['pts'], clip):
        rc = dict(r, pts=piece)
        if r['k'] in ('main', 'street'):
            ribbon(piece, r['w'] + 3.0, 0.025, hex_rgb('#c9926a') if soil[0] > soil[2] * 1.5 else hex_rgb('#cbbd98'), 0.6)  # dusty shoulder
        street.road(sm, rc, cond, rr, clip=None)
        street.markings(sm, rc, cond, rr)
        if r['k'] == 'main' or (ch in ('elite', 'civic') and r['k'] == 'street'):
            street.kerbs(sm, rc, ST['kerb'] if r['k'] == 'main' else 'white', rr, skip=lambda p: in_building(p, 0.1))
        if r['k'] == 'street' and rr.chance(ST['bumps']) and len(piece) > 1:
            L = sum(math.dist(piece[i], piece[i + 1]) for i in range(len(piece) - 1))
            if L > 30:
                street.speed_bump(sm, dict(rc, pts=[piece[0], piece[-1]]), rr.between(10, L - 10), rr, painted=ch in ('elite', 'civic'))
        if r['k'] not in ('main', 'street'):
            continue
        # open drains along both edges, broken where they meet another road or a building
        dw, dh = ST['drain']
        for side in (-1, 1):
            off = side * (r['w'] / 2 + 0.3 + dw / 2)
            run = []
            for i in range(len(piece) - 1):
                a, b = piece[i], piece[i + 1]
                L = math.dist(a, b)
                if L < 1e-6:
                    continue
                dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                k = 0.0
                while k <= L:
                    p = (a[0] + dx * k - dy * off, a[1] + dy * k + dx * off)
                    bad = in_building(p, 0.2) or any(o is not r and dist_line(p, o['pts']) < o['w'] / 2 + 0.6 for o in roads)
                    if bad:
                        if len(run) > 2:
                            street.drain(sm, run, dict(w=dw, h=dh, wear=0.6, cover=ST['cover'], rubbish=ST['rubbish'], water='#4f5a3c' if rr.chance(0.6) else '#2b2a24'), rr)
                        run = []
                    else:
                        run.append(p)
                    k += 1.5
            if len(run) > 2:
                street.drain(sm, run, dict(w=dw, h=dh, wear=0.6, cover=ST['cover'], rubbish=ST['rubbish'], water='#4f5a3c'), rr)
        # poles on one side, every ~35 m, wired to each other
        if ch == 'elite' and r['k'] != 'main':
            continue
        off = (1 if ri % 2 else -1) * (r['w'] / 2 + 0.6 + dw + 0.5)
        prev = None
        for i in range(len(piece) - 1):
            a, b = piece[i], piece[i + 1]
            L = math.dist(a, b)
            if L < 1e-6:
                continue
            dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            k = rr.between(3, 20)
            while k < L:
                p = (a[0] + dx * k - dy * off, a[1] + dy * k + dx * off)
                if in_building(p, 0.3) or any(dist_line(p, o['pts']) < o['w'] / 2 + 0.3 for o in roads):
                    prev = None
                else:
                    pts3, top = street.pole(sm, p[0], p[1], rr, wood=rr.chance(ST['wood_pole']))
                    if prev:
                        for w0, w1 in zip(prev, pts3):
                            street.wire(sm, w0, w1, rr.between(0.5, 1.3))
                    prev = pts3
                    poles.append((p, top))
                k += rr.between(30, 42)
# service drops: every house near a pole gets its own wire or three (the spaghetti)
for b in blds:
    if 'H' not in b or not poles:
        continue
    p, top = min(poles, key=lambda q: math.dist(q[0], b['c']))
    if math.dist(p, b['c']) > 32:
        continue
    rr = Rng(district, 'drop', b['i'])
    for _ in range(rr.randrange(ST['drops'][0], ST['drops'][1] + 1)):
        cnr = b['poly'][rr.randrange(4)]
        street.wire(sm, (top[0], top[1], top[2] - 0.6), (cnr[0], cnr[1], min(b['H'], 6.5) - 0.3), rr.between(0.4, 1.5), t=0.012, n=8)
# a transformer about every 150 m of street, tied to its nearest poles
rr = Rng(district, 'transformers')
street_len = sum(math.dist(p[i], p[i + 1]) for r in roads if r['k'] == 'street' for p in clip_line(r['pts'], clip) for i in range(len(p) - 1))
for _ in range(max(1, int(street_len / 150))):
    if not poles:
        break
    p, top = poles[rr.randrange(len(poles))]
    q = (p[0] + rr.between(-3, 3), p[1] + rr.between(-3, 3))
    if in_building(q, 1.5):
        continue
    t = street.transformer(sm, q[0], q[1], rr)
    for pp, tp in sorted(poles, key=lambda z: math.dist(z[0], q))[:3]:
        street.wire(sm, t, (tp[0], tp[1], tp[2] - 0.3), rr.between(0.6, 1.4), t=0.02)
# litter along road edges, thicker in markets; refuse heaps on spare ground
rr = Rng(district, 'litter')
for r in roads:
    for piece in clip_line(r['pts'], clip):
        for i in range(len(piece) - 1):
            a, b = piece[i], piece[i + 1]
            L = math.dist(a, b)
            if L < 1e-6:
                continue
            dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            for _ in range(int(L * ST['litter'] * (0.6 if r['k'] == 'main' else 1.5))):
                k, side = rr.between(0, L), rr.pick([-1, 1])
                o = side * (r['w'] / 2 + rr.between(-0.8, 2.5))
                p = (a[0] + dx * k - dy * o, a[1] + dy * k + dx * o)
                if not in_building(p, 0.0):
                    street.litter_piece(sm, p[0], p[1], 0.07, rr)
for pc in D.get('parcels', []):
    pts = [P(p) for p in pc['pts'][:-1]]
    if pc['kind'] == 'market' and any(math.hypot(*p) < R + 60 for p in pts):
        mb.face([(p[0], p[1], 0.04) for p in ccw(pts)], 'concrete', hex_rgb('#a39b8e'), 0.6)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        for _ in range(int(ST['litter'] * 1500)):
            p = (rr.between(min(xs), max(xs)), rr.between(min(ys), max(ys)))
            if in_poly(p, pts) and not in_building(p, 0.0):
                street.litter_piece(sm, p[0], p[1], 0.06, rr)
for _ in range(int(ST['heaps'] * (R / 60) ** 2 * 2)):
    for _try in range(30):
        p = (rr.between(-R, R), rr.between(-R, R))
        near = min((dist_line(p, r['pts']) - r['w'] / 2 for r in roads), default=99)
        if 1.5 < near < 8 and not in_building(p, 1.0):
            street.refuse_heap(sm, p[0], p[1], rr.between(1.0, 2.6), rr)
            break
mb.to_object('ground', col, master)
sm.to_object('street', col, master)

# ---------------------------------------------------------------- render and export
scene.sky_and_sun(sc)
renders = str(opt.get('--render', 'overview,street')).split(',')
if 'overview' in renders:
    scene.camera(sc, (-R * 0.9, -R * 1.25, R * 0.75), (0, 0, 0), lens=30)
    scene.render(sc, os.path.join(out, 'overview.jpg'))
if 'street' in renders:
    # eye level on the street segment with the most shop fronts, from one end looking along it
    best = None
    for r in roads:
        if r['k'] not in ('street', 'main'):
            continue
        for i in range(len(r['pts']) - 1):
            a_, b_ = r['pts'][i], r['pts'][i + 1]
            n = sum(1 for sp in shops if dist_seg(sp, a_, b_) < r['w'] / 2 + 6)
            if best is None or n > best[0]:
                best = (n, a_, b_, r['w'])
    _, a_, b_, w = best
    L = math.dist(a_, b_)
    dx, dy = (b_[0] - a_[0]) / L, (b_[1] - a_[1]) / L
    on = [sp for sp in shops if dist_seg(sp, a_, b_) < w / 2 + 6]
    ts = sorted(((sp[0] - a_[0]) * dx + (sp[1] - a_[1]) * dy) for sp in on) or [L / 2]
    t0 = max(0.0, ts[0] - 12)
    side = 1
    ex, ey = a_[0] + dx * t0 - dy * side * (w / 4), a_[1] + dy * t0 + dx * side * (w / 4)
    scene.camera(sc, (ex, ey, 1.7), (ex + dx * 25, ey + dy * 25, 2.4), lens=22)
    scene.render(sc, os.path.join(out, 'street.jpg'))
if opt.get('--glb'):
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, f'{district}.glb'), export_format='GLB', use_selection=False)
if opt.get('--blend'):
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, f'{district}.blend'))
print('DONE', out)
