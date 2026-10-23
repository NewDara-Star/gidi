"""The Reach, close up. blender -b --factory-startup -P legacy/blender/reach_sheet.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from mathutils import Matrix  # noqa: E402
from gidi_kit import monuments  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.3, 0.3, 0.3))
mb = MeshBuilder()
monuments.the_reach(mb, Matrix.Identity(4), Rng('reach'))
mb.to_object('reach', sc.collection, master)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'the_reach.jpg')
scene.camera(sc, (1.5, -22, 6.5), (-0.5, 0, 5.0), lens=40)
scene.render(sc, out, res=(2000, 1200))
print('WROTE', out)
