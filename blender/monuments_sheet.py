"""Every monument in the kit side by side.
blender -b --factory-startup -P blender/monuments_sheet.py -- [--out blender/out/monuments.jpg]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from mathutils import Matrix  # noqa: E402
from gidi_kit import monuments  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(zip(args[::2], args[1::2]))
out = opt.get('--out', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'monuments.jpg'))
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.3, 0.3, 0.3))
mb = MeshBuilder()
R = Matrix.Rotation(math.radians(-60), 4, 'Z')
for i, k in enumerate(['founder', 'masquerade', 'drummer']):
    monuments.statue(mb, Matrix.Translation((i * 7, 0, 0)) @ R, Rng('m', k), k)
monuments.sculpture(mb, Matrix.Translation((22, 0, 0)), Rng('m', 'sc'))
monuments.clock_tower(mb, Matrix.Translation((31, 2, 0)) @ R, Rng('m', 'ct'))
monuments.led_board(mb, Matrix.Translation((44, 4, 0)) @ Matrix.Rotation(math.radians(-80), 4, 'Z'), Rng('m', 'led'))
monuments.lighthouse(mb, Matrix.Translation((62, 10, 0)), Rng('m', 'lh'))
monuments.arch(mb, Matrix.Translation((84, 8, 0)) @ Matrix.Rotation(math.radians(70), 4, 'Z'), Rng('m', 'arch'), 16, 'Railside', 'sprawl')
mb.to_object('monuments', sc.collection, master)
scene.camera(sc, (44, -95, 30), (44, 4, 10), lens=30)
scene.render(sc, out, res=(2400, 1100))
print('WROTE', out)
