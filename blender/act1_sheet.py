"""The Act 1 kit pieces side by side (docs/KIT-GAPS.md, "New in the v2 layout"): the face-me-I-face-you block, the motor
park office (and a shot inside it), the buka, Ladi Lane's open lock-ups, the rail market, the people placed by hand,
the police kiosk, the task force truck and an overhead sign.
blender -b --factory-startup -P blender/act1_sheet.py -- [--out blender/out/act1] [--shots all,people,office,ladi]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from mathutils import Matrix  # noqa: E402
from gidi_kit import archetypes, roadside, street, structures, vehicles  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(zip(args[::2], args[1::2]))
out = opt.get('--out', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'act1'))
shots = opt.get('--shots', 'all,people,office,ladi').split(',')
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.45, 0.3, 0.2))
col = sc.collection
R = lambda x, y, a=0: Matrix.Translation((x, y, 0)) @ Matrix.Rotation(math.radians(a), 4, 'Z')
box = lambda x, y, w, d: [(x - w / 2, y - d / 2), (x + w / 2, y - d / 2), (x + w / 2, y + d / 2), (x - w / 2, y + d / 2)]
A = lambda kind, poly, facing, name, **kw: dict(kind=kind, poly=poly, facing=facing, name=name, district=kw.get('d', 'maze'), storeys=1, near_main=99, frontage=2, **kw)

# buildings: the street runs along y = -12 in front of them (facing edge 0 is the south side of each box)
archetypes.face_me(A('face-me', box(0, 0, 21.9, 9.5), 0, 'face-me'), Rng('s', 'faceme'), col)
archetypes.park_office(A('office', box(26, -2, 7.0, 4.6), 0, 'office', d='hub'), Rng('s', 'office'), col)
archetypes.buka(A('buka', box(-22, -1, 6.0, 4.0), 0, 'buka', label='Flyover Buka'), Rng('s', 'buka'), col)
# Ladi Lane: two rows of lock-ups facing a 3 m aisle along x
for i in range(8):
    for s, fe in ((1, 0), (-1, 2)):
        archetypes.lockup_open(A('stalls', box(-30 + i * 3.1, -40 + s * 3.5, 3.0, 4.0), fe, f'lockup{i}{s}'), Rng('s', 'lock', i, s), col)
mb = MeshBuilder()
# the rail market: a track and pitches on the ballast either side
structures.rail(mb, [(0, -62), (60, -62)], Rng('s', 'rail'))
for i in range(12):
    for s in (1, -1):
        street.rail_market(mb, R(4 + i * 2.0, -62 + s * 3.2), Rng('s', 'rm', i, s))
# people placed by hand, the police kiosk, the truck and a gantry over a road at y = -20
P0 = 18
for k, (fn, pose) in enumerate(((street.agbero, 'collect'), (street.agbero, 'count'), (street.agbero, 'wave'))):
    fn(mb, R(P0 + k * 1.3, -14, -90), Rng('s', 'agb', k), pose=pose)
street.wheelbarrow_vendor(mb, R(P0 + 5, -14, -90), Rng('s', 'wv'))
street.fruit_seller(mb, R(P0 + 8, -14, -90), Rng('s', 'fs'))
street.parking_boy(mb, R(P0 + 10.5, -14, -90), Rng('s', 'pb'))
street.bread_hawker(mb, R(P0 + 13, -14, -90), Rng('s', 'bh1'), kind='barrow')
street.bread_hawker(mb, R(P0 + 15.5, -14, -90), Rng('s', 'bh2'), kind='tray')
roadside.police_kiosk(mb, R(P0 + 19, -14.5, -90), Rng('s', 'pk'))
vehicles.task_force_truck(mb, R(P0 + 4, -18.5, 0), Rng('s', 'tf'))
roadside.gantry(mb, P0 + 30, -22, 0, 16, [[('up', 'Old Island')], [('up', 'Ring Road')]], Rng('s', 'gantry'))
mb.face([(-40, -26, 0.01), (70, -26, 0.01), (70, -18, 0.01), (-40, -18, 0.01)], 'asphalt', (0.18, 0.18, 0.18), 0.6)
mb.to_object('pieces', col, master)

os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
CAMS = {   # name: (location, target, lens)
    'all': ((5, -95, 60), (5, -20, 0), 24),
    'people': ((P0 + 8, -26, 3.2), (P0 + 8, -14, 1.0), 30),
    'office': ((24.3, -3.8, 1.6), (26.6, -0.8, 1.0), 14),   # inside, from the door corner toward the desk
    'office_out': ((26 - 3, -2 - 8, 2.4), (26, -2, 1.4), 30),
    'ladi': ((-34, -40, 1.7), (-10, -40, 1.4), 22),
    'faceme': ((-6, 18, 9), (0, 0, 1), 26),
    'truck': ((P0 + 9, -24, 4.5), (P0 + 3, -18.5, 1.2), 30),
    'buka': ((-22 + 4, -1 - 10, 2.4), (-22, -1, 1.2), 26),
    'kiosk': ((P0 + 17, -22, 2.2), (P0 + 17, -14, 1.2), 30),
    'rail': ((2, -68, 3.0), (16, -62, 0.4), 28),
    'gantry': ((P0 + 18, -21, 2.5), (P0 + 30, -22, 5.5), 26),
}
for name in shots:
    for n in (CAMS if name == 'all-shots' else [name]):
        loc, tgt, lens = CAMS[n]
        scene.camera(sc, loc, tgt, lens=lens)
        scene.render(sc, f'{out}_{n}.jpg', res=(1800, 1000))
        print('WROTE', f'{out}_{n}.jpg')
