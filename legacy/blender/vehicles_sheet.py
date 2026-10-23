"""Line-up of every vehicle in its conditions, and a crowd of every dress type.
blender -b --factory-startup -P legacy/blender/vehicles_sheet.py -- [--out legacy/blender/out/vehicles.jpg]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from mathutils import Matrix  # noqa: E402
from gidi_kit import people, vehicles  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(zip(args[::2], args[1::2]))
out = opt.get('--out', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'vehicles.jpg'))
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.3, 0.3, 0.3))
mb = MeshBuilder()
x = 0.0
row = [('danfo', 'new'), ('danfo', 'worn'), ('danfo', 'battered'), ('korope', 'worn'), ('keke', 'worn'), ('keke', 'battered'), ('okada', 'worn'), ('car', 'new'), ('car', 'battered'), ('brt', 'worn'), ('tipper', 'battered'), ('tanker', 'worn'), ('police', 'worn'), ('cart', 'battered'), ('wheelbarrow', 'worn')]
for i, (k, cond) in enumerate(row):
    rng = Rng('vsheet', k, i)
    Lk = vehicles.LENGTH[k]
    M = Matrix.Translation((x + Lk / 2, 0, 0)) @ Matrix.Rotation(math.radians(-35), 4, 'Z')
    fn = vehicles.BUILDERS[k]
    if k == 'car':
        fn(mb, M, rng, cond, kind=['saloon', 'suv', 'pickup'][i % 3])
    elif k in ('cart', 'wheelbarrow'):
        fn(mb, M, rng)
    else:
        fn(mb, M, rng, cond)
    if k == 'okada':
        people.seated_rider(mb, M @ Matrix.Translation((-0.25, 0, 0.92)), rng)
    x += Lk * 0.85 + 1.2
# a crowd of every dress type
for i, kind in enumerate(['ankara', 'wrapper', 'buba', 'tshirt', 'kaftan', 'agbada', 'school', 'office', 'hawker'] * 2):
    people.person(mb, Matrix.Translation((2 + (i % 9) * 1.1, -6 - (i // 9) * 1.3, 0)) @ Matrix.Rotation(math.radians(-90 + (i * 37) % 60), 4, 'Z'), Rng('crowd', i), kind=kind)
mb.to_object('lineup', sc.collection, master)
zx = float(opt.get('--zx', x * 0.42)); zd = float(opt.get('--zd', x * 0.62))
scene.camera(sc, (zx, -zd, zd * 0.32), (zx, -2, 0.8), lens=30)
scene.render(sc, out, res=(2400, 1200))
print('WROTE', out)
