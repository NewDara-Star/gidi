"""Traffic lights, street-light ads, the new statues. blender -b --factory-startup -P legacy/blender/lights_sheet.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from mathutils import Matrix  # noqa: E402
from gidi_kit import monuments, roadside  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.3, 0.3, 0.3))
mb = MeshBuilder()
face = -math.pi / 2
roadside.traffic_light(mb, 0, 0, face, Rng('t1'))
roadside.traffic_light(mb, 4, 0, face, Rng('t2'), arm=4.0)
for k in range(4):
    roadside.street_light(mb, 12 + k * 6, 2, 0, Rng('b', k), arms=2, h=10, banners=True)
monuments.statue(mb, Matrix.Translation((40, 0, 0)) @ Matrix.Rotation(face + math.pi / 2, 4, 'Z'), Rng('s1'), 'three_elders')
monuments.statue(mb, Matrix.Translation((50, 0, 0)) @ Matrix.Rotation(face + math.pi / 2, 4, 'Z'), Rng('s2'), 'saxophonist')
mb.to_object('sheet', sc.collection, master)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'lights.jpg')
scene.camera(sc, (24, -40, 8), (24, 0, 4), lens=28)
scene.render(sc, out, res=(2400, 1100))
print('WROTE', out)
