"""The newest kit pieces side by side: the container truck, the 911 food lorry, the trains, the
Crown Hall, the central mosque and a flyover with painted piers.
blender -b --factory-startup -P blender/new_kit_sheet.py -- [--out blender/out/new_kit.jpg]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from mathutils import Matrix  # noqa: E402
from gidi_kit import landmarks, structures, vehicles  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(zip(args[::2], args[1::2]))
out = opt.get('--out', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'new_kit.jpg'))
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.3, 0.3, 0.3))
col = sc.collection
mb = MeshBuilder()
R = lambda x, y, a=0: Matrix.Translation((x, y, 0)) @ Matrix.Rotation(math.radians(a), 4, 'Z')
vehicles.container_truck(mb, R(0, 0, -20), Rng('s', 'ct1'))
vehicles.container_truck(mb, R(2, 6, -20), Rng('s', 'ct2'))
vehicles.lorry_911(mb, R(22, 2, -20), Rng('s', 'l911'), load='tomato')
vehicles.lorry_911(mb, R(24, 8, -20), Rng('s', 'l911b'), load='onion')
structures.rail(mb, [(-20, -24), (80, -24)], Rng('s', 'rail'))
x = 70
for i, k in enumerate(['commuter', 'commuter', 'loco', 'coach', 'wagon']):
    fn, ln = vehicles.TRAIN[k]
    x -= ln / 2
    M = R(x, -24)
    fn(mb, M, Rng('s', k, i), cab=True) if k == 'commuter' else fn(mb, M, Rng('s', k, i))
    x -= ln / 2
mb.to_object('vehicles', col, master)
landmarks.crown_hall(dict(poly=[(40, 10), (110, 10), (110, 80), (40, 80)], facing=0, name='crown'), Rng('s', 'crown'), col)
landmarks.central_mosque(dict(poly=[(-60, 10), (-20, 10), (-20, 50), (-60, 50)], facing=0, name='mosque', district='railside', kind='mosque'), Rng('s', 'mosque'), col)
fm = MeshBuilder()
structures.flyover(fm, [(-80, -60), (60, -60)], 12, structures.profile([(-80, -60), (60, -60)], None, 6.5), Rng('s', 'fly'))
fm.to_object('flyover', col, master)
cam = [float(v) for v in opt.get('--cam', '10,-150,70,15,5,8').split(',')]
scene.camera(sc, tuple(cam[:3]), tuple(cam[3:]), lens=float(opt.get('--lens', 30)))
scene.render(sc, out, res=(2400, 1300))
print('WROTE', out)
