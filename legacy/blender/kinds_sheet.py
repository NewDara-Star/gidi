"""Contact sheet of every registered kind (except houses), each built on footprints taken from
the real data, a few seeds side by side. blender -b --factory-startup -P legacy/blender/kinds_sheet.py -- [--kinds a,b] [--seeds 3] [--out ...]"""
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from gidi_kit import registry  # noqa: E402
from gidi_kit.core import Rng  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # legacy/blender/ -> the repo
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(zip(args[::2], args[1::2]))
seeds = int(opt.get('--seeds', 3))
out = opt.get('--out', os.path.join(ROOT, 'legacy', 'blender', 'out', 'kinds.jpg'))
want = opt['--kinds'].split(',') if '--kinds' in opt else [k for k in registry.BUILDINGS if k not in ('front', 'back', 'shed')]

samples = {}
gd = open(os.path.join(ROOT, 'web', 'gidi-data.js')).read()
gd = json.loads(gd[gd.index('{'):gd.rindex('}') + 1])
for sg in gd['safe_ground']:
    k = 'civic:' + sg['type']
    p = sg['pts'][:4]
    if k in want and len(samples.setdefault(k, [])) < seeds and len(sg['pts']) == 5:
        e0, e1 = math.dist(p[0], p[1]), math.dist(p[1], p[2])
        samples[k].append((max(e0, e1), min(e0, e1), 2, sg['d'], sg['name']))
for f in sorted(glob.glob(os.path.join(ROOT, 'web', 'gen-*.json'))):
    d = json.load(open(f))
    dist = os.path.basename(f)[4:-5]
    for b, s in zip(d['buildings'], d['storeys']):
        if b[0] in want and len(samples.setdefault(b[0], [])) < seeds:
            p = b[1:]
            e0, e1 = math.dist(p[0], p[1]), math.dist(p[1], p[2])
            samples[b[0]].append((max(e0, e1), min(e0, e1), s, dist))

# one framed render per kind, then a labelled montage (PIL, outside Blender)
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
tiles = []
for k in want:
    if k not in samples:
        continue
    sc = scene.reset()
    scene.sky_and_sun(sc)
    scene.ground(sc)
    y = 0.0
    obs = []
    for i, smp in enumerate(samples[k]):
        L, W, s, dist = smp[:4]
        poly = [(-L / 2, y - W / 2), (L / 2, y - W / 2), (L / 2, y + W / 2), (-L / 2, y + W / 2)]
        fn = registry.CIVIC_PLOTS[k[6:]] if k.startswith('civic:') else registry.BUILDINGS[k]
        ob, _ = fn(dict(kind=k, storeys=s, district=dist, poly=poly, facing=0, name=f'{k}_{i}', label=smp[4] if len(smp) > 4 else None), Rng('sheet', k, i), sc.collection)
        obs.append(ob)
        y += max(W, 4) + max(6, W * 0.6)
    pts = [ob.matrix_world @ Vector(c) for ob in obs for c in ob.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), 0))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    mid = (lo + hi) / 2
    size = max(hi.x - lo.x, hi.y - lo.y, hi.z * 1.5, 6)
    scene.camera(sc, (mid.x - size * 0.4, mid.y - size * 0.8, size * 0.42 + hi.z * 0.5), (mid.x, mid.y, hi.z * 0.3), lens=32)
    path = os.path.join(os.path.dirname(out), 'kinds', k.replace(' ', '_') + '.jpg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    scene.render(sc, path, res=(960, 600), samples=24)
    tiles.append((k, path))
json.dump(tiles, open(os.path.join(os.path.dirname(out), 'kinds', 'tiles.json'), 'w'))
print('WROTE', len(tiles), 'tiles')
