"""Export the kit's vehicles and people as GLB models for the Mock (mock/public/models/).

blender -b --factory-startup -P blender/export_fleet.py

Vehicles face +z in the glTF (Blender -y), one mesh per material, named for their role: CarPaint
(repainted per car by the traffic code; private cars only, in white), DanfoPaint (kept), Glass,
Brakelights, Lamps, Trim. People: one file per dress type, two stride poses (Step0, Step1)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Matrix  # noqa: E402
import scene  # noqa: E402
from gidi_kit import people, vehicles  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng  # noqa: E402
from gidi_kit.materials import master  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mock', 'public', 'models')
os.makedirs(OUT, exist_ok=True)
FACE_Z = Matrix.Rotation(math.radians(90), 4, 'Z')  # Blender +x forward -> -y... then glTF z = -y: forward +z
ROLE = {'carpaint': 'CarPaint', 'glass': 'Glass', 'emit': 'Lamps', 'emitRed': 'Brakelights', 'emitAmber': 'Lamps'}


def export(name, build, role_paint='CarPaint'):
    scene.reset()
    mb = MeshBuilder()
    build(mb)
    ob = mb.to_object(name, bpy.context.scene.collection, master)
    ob.data.transform(Matrix.Rotation(math.radians(-90), 4, 'Z'))  # +x forward becomes -y, which glTF calls +z
    # one object per material, named by role
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.separate(type='MATERIAL')
    bpy.ops.object.mode_set(mode='OBJECT')
    for o in bpy.context.scene.objects:
        if o.type != 'MESH' or not o.data.materials:
            continue
        m = o.data.materials[0].name.split('.')[0]
        o.name = ROLE.get(m, m.capitalize())
        if m == 'carpaint':
            o.name = role_paint
            o.data.materials[0].name = role_paint
    path = os.path.join(OUT, name + '.glb')
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', export_vertex_color='ACTIVE', export_yup=True, export_materials='EXPORT')
    print('WROTE', path, os.path.getsize(path))


V = vehicles
# private cars in white: the traffic code paints each car its own colour
export('gidi_car_saloon', lambda mb: V.car(mb, Matrix(), Rng('fleet', 'saloon'), 'worn', kind='saloon', colour='#f2f2f2'))
export('gidi_car_suv', lambda mb: V.car(mb, Matrix(), Rng('fleet', 'suv'), 'new', kind='suv', colour='#f2f2f2'))
export('gidi_car_pickup', lambda mb: V.car(mb, Matrix(), Rng('fleet', 'pickup'), 'battered', kind='pickup', colour='#f2f2f2'))
export('gidi_taxi', lambda mb: V.car(mb, Matrix(), Rng('fleet', 'taxi'), 'worn', kind='saloon', taxi=True), 'DanfoPaint')
for i, cond in enumerate(('worn', 'battered', 'new')):
    export(f'gidi_danfo_{i}', lambda mb, cond=cond, i=i: V.danfo(mb, Matrix(), Rng('fleet', 'danfo', i), cond), 'DanfoPaint')
export('gidi_korope', lambda mb: V.korope(mb, Matrix(), Rng('fleet', 'korope'), 'battered'), 'DanfoPaint')
for i in range(2):
    export(f'gidi_keke_{i}', lambda mb, i=i: V.keke(mb, Matrix(), Rng('fleet', 'keke', i), ('worn', 'battered')[i]), 'DanfoPaint')
for i in range(2):
    def ok(mb, i=i):
        r = Rng('fleet', 'okada', i)
        V.okada(mb, Matrix(), r, 'worn')
        people.seated_rider(mb, Matrix.Translation((-0.25, 0, 0.92)), r)
        if i:
            people.seated_rider(mb, Matrix.Translation((-0.75, 0, 0.98)), r, vest='#f4f1ea', helmet=False)
    export(f'gidi_okada_{i}', ok, 'DanfoPaint')
export('gidi_brt', lambda mb: V.brt(mb, Matrix(), Rng('fleet', 'brt'), 'worn'), 'DanfoPaint')
export('gidi_tipper', lambda mb: V.tipper(mb, Matrix(), Rng('fleet', 'tipper'), 'battered'), 'DanfoPaint')
export('gidi_tanker', lambda mb: V.tanker(mb, Matrix(), Rng('fleet', 'tanker'), 'worn'), 'DanfoPaint')
export('gidi_police', lambda mb: V.police_pickup(mb, Matrix(), Rng('fleet', 'police'), 'worn'), 'DanfoPaint')
# people: each dress type in two stride poses
for kind in ('ankara', 'wrapper', 'buba', 'tshirt', 'kaftan', 'agbada', 'office', 'hawker', 'school'):
    for step, ph in ((0, 1), (1, -1)):
        export(f'gidi_person_{kind}_{step}', lambda mb, kind=kind, ph=ph: people.person(mb, Matrix(), Rng('fleet', 'person', kind), kind=kind, pose=True, phase=ph), 'Cloth')
