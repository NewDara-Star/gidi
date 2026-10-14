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
from gidi_kit import archetypes, parts  # noqa: E402
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
    if k in ('front', 'back', 'shed'):
        ob, spec = archetypes.house(a, rng, col)
        if spec['shop']:
            e = a['facing']
            pa, pb = a['poly'][e], a['poly'][(e + 1) % 4]
            shops.append(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2))
    elif k == 'stalls':
        archetypes.stall(a, rng, col)
    elif k == 'kiosk':
        archetypes.kiosk(a, rng, col)
    else:  # kinds without an archetype yet: a plain house so the area is complete
        archetypes.house(dict(a, kind='back'), rng, col)
    counts[k] = counts.get(k, 0) + 1
print('built', counts)

# ---------------------------------------------------------------- ground, roads, market floor
mb = MeshBuilder()
G = R + 160
mb.face([(-G, -G, 0), (G, -G, 0), (G, G, 0), (-G, G, 0)], 'ground', hex_rgb('#b5714a'), 0.5)
ROAD = {'main': ('#4a4d52', 0.06, 0.35), 'street': ('#5a5c60', 0.05, 0.5), 'lane': ('#a8714c', 0.04, 0.6), 'path': ('#9c6a48', 0.035, 0.6)}


def ribbon(pts, w, z, colr, wear, mat='ground'):
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy) or 1
        nx, ny = -dy / l * w / 2, dx / l * w / 2
        ex, ey = dx / l * w / 2, dy / l * w / 2  # extend ends so joints close
        mb.face([(a[0] - ex + nx, a[1] - ey + ny, z), (a[0] - ex - nx, a[1] - ey - ny, z), (b[0] + ex - nx, b[1] + ey - ny, z), (b[0] + ex + nx, b[1] + ey + ny, z)], mat, colr, wear)


for r in roads:
    c, z, wear = ROAD[r['k']]
    if r['k'] in ('main', 'street'):
        ribbon(r['pts'], r['w'] + 3.0, 0.025, hex_rgb('#b98a62'), 0.6)  # sandy shoulder
    ribbon(r['pts'], r['w'], z, hex_rgb(c), wear)
    if r['k'] == 'main':  # yellow-and-black kerbs on the main road, 1 m blocks
        for side in (-1, 1):
            for i in range(len(r['pts']) - 1):
                a, b = r['pts'][i], r['pts'][i + 1]
                L = math.dist(a, b)
                dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                for k in range(int(L)):
                    x, y = a[0] + dx * (k + 0.5) - dy * side * (r['w'] / 2 + 0.1), a[1] + dy * (k + 0.5) + dx * side * (r['w'] / 2 + 0.1)
                    if math.hypot(x, y) > R + 60:
                        continue
                    from mathutils import Matrix
                    mb.box('concrete', Matrix.Translation((x, y, 0.12)) @ Matrix.Rotation(math.atan2(dy, dx), 4, 'Z'), hex_rgb('#f2c21b' if k % 2 else '#1a1a1a'), 0.4, size=(0.98, 0.2, 0.25))
for pc in D.get('parcels', []):
    pts = [P(p) for p in pc['pts'][:-1]]
    if pc['kind'] == 'market' and any(math.hypot(*p) < R + 60 for p in pts):
        mb.face([(p[0], p[1], 0.04) for p in ccw(pts)], 'concrete', hex_rgb('#a39b8e'), 0.6)
mb.to_object('ground', col, master)

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
