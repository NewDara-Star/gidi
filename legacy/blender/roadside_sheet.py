"""The roadside kit side by side: lamps, a direction sign, a gantry, speed and no-parking discs, a
dressed bridge deck. blender -b --factory-startup -P legacy/blender/roadside_sheet.py -- [--out legacy/blender/out/roadside.jpg]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from gidi_kit import roadside, structures  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(zip(args[::2], args[1::2]))
out = opt.get('--out', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'roadside.jpg'))
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.3, 0.3, 0.3))
mb = MeshBuilder()
r = Rng('sheet')
# readers stand at -y looking +y: faces point to -y (angle -90 deg)
face = -math.pi / 2
roadside.street_light(mb, 0, 0, 0, r, arms=1)
roadside.street_light(mb, 4, 0, 0, r, arms=2, solar=True)
roadside.direction_sign(mb, 10, 0, face, [('up', 'Food Gate'), ('left', 'The Estate'), ('right', 'Salami Road')], r)
roadside.disc_sign(mb, 15, 0, face, 'speed', r, 50)
roadside.disc_sign(mb, 17, 0, face, 'noparking', r)
roadside.gantry(mb, 26, 6, math.pi / 2, 14, [[('up', 'Old Island')], [('up', 'Coastal Expressway')]], r)  # traffic drives +y, reads facing -y
structures.deck_line(mb, [(36, -30), (36, 60)], 22, structures.profile([(36, -30), (36, 60)], None, 3.0, 20), r)
mb.to_object('roadside', sc.collection, master)
scene.camera(sc, (20, -26, 6), (20, 4, 3), lens=30)
scene.render(sc, out, res=(2400, 1100))
print('WROTE', out)
