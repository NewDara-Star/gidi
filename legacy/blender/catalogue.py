"""Contact sheet of the kit: the same footprint built for each district character and several seeds.

blender -b --factory-startup -P legacy/blender/catalogue.py -- --out legacy/blender/out/catalogue.jpg [--storeys 1,2,3] [--seeds 4]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from gidi_kit import archetypes  # noqa: E402
from gidi_kit.core import Rng  # noqa: E402
from gidi_kit.rules import CHARACTER  # noqa: E402

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(zip(args[::2], args[1::2]))
out = opt.get('--out', os.path.join(os.path.dirname(__file__), 'out', 'catalogue.jpg'))
storeys = [int(x) for x in opt.get('--storeys', '1,2,3').split(',')]
seeds = int(opt.get('--seeds', 3))
districts = opt.get('--districts', 'maze,railside,oldisland,estate').split(',')

sc = scene.reset()
scene.sky_and_sun(sc)
scene.ground(sc)
W, D = 9.0, 12.0
col_gap, row_gap = 16.0, 30.0
x0 = 0
for di, dist in enumerate(districts):
    for si, s in enumerate(storeys):
        for k in range(seeds):
            x = (si * seeds + k) * col_gap
            y = -di * row_gap
            poly = [(x - W / 2, y - D / 2), (x + W / 2, y - D / 2), (x + W / 2, y + D / 2), (x - W / 2, y + D / 2)]
            wall = [(x - W / 2 - 2, y - D / 2 - 2.5), (x + W / 2 + 2, y - D / 2 - 2.5), (x + W / 2 + 2, y + D / 2 + 2), (x - W / 2 - 2, y + D / 2 + 2)]
            a = dict(kind='front', storeys=s, district=dist, poly=poly, facing=0, frontage=3, near_main=60,
                     wall_poly=wall, name=f'{dist}_{s}_{k}', unfinished=(dist == 'railside' and k == seeds - 1 and s > 1))
            archetypes.house(a, Rng('catalogue', dist, s, k))
n = len(storeys) * seeds
cx = (n - 1) * col_gap / 2
cy = -(len(districts) - 1) * row_gap / 2
if opt.get('--cam') == 'close':  # eye level in front of the first dense house
    scene.camera(sc, (5.5, -16.0, 1.7), (0.5, -6, 3.2), lens=22)
else:
    scene.camera(sc, (cx - 10, cy - 95, 60), (cx, cy + 4, 2), lens=28)
os.makedirs(os.path.dirname(out), exist_ok=True)
scene.render(sc, out, res=(2400, 1350))
print('WROTE', out)
