"""Contact sheets for the second batch: --part vehicles (service vehicles, the molue, port
machines, boats) or --part places (cathedral, heritage, civic tower, market block, refinery,
the commemorative square, Freedom Ground, the airport, statues, beach arch, mural wall, billboard).
blender -b --factory-startup -P legacy/blender/new_kit_sheet2.py -- --part vehicles [--out ...]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene  # noqa: E402
from mathutils import Matrix  # noqa: E402
from gidi_kit import boats, landmarks, monuments, parcels, vehicles  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng, hex_rgb  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(zip(args[::2], args[1::2]))
part = opt.get('--part', 'vehicles')
out = opt.get('--out', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', f'new_kit_{part}.jpg'))
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.3, 0.3, 0.3))
col = sc.collection
mb = MeshBuilder()
R = lambda x, y, a=0: Matrix.Translation((x, y, 0)) @ Matrix.Rotation(math.radians(a), 4, 'Z')
if part == 'vehicles':
    x = 0
    for k, cond in (('fire', 'worn'), ('ambulance', 'worn'), ('refuse', 'worn'), ('mixer', 'battered'), ('water', 'worn'), ('molue', 'worn'), ('molue', 'wreck'), ('stacker', 'worn'), ('forklift', 'worn')):
        ln = vehicles.LENGTH[k]
        vehicles.BUILDERS[k](mb, R(x + ln / 2, 0, -30), Rng('s', k, cond), cond)
        x += ln + 3
    water = MeshBuilder()
    water.face([(-10, -50, 0.02), (110, -50, 0.02), (110, -14, 0.02), (-10, -14, 0.02)], 'water', hex_rgb('#2f4a50'), 0)
    water.to_object('water', col, master)
    boats.ferry(mb, R(10, -30, -20), Rng('s', 'ferry'))
    boats.water_bus(mb, R(40, -28, -20), Rng('s', 'wb'))
    boats.outboard_canoe(mb, R(58, -26, -20), Rng('s', 'canoe'))
    boats.dredger(mb, R(80, -32, -20), Rng('s', 'dredger'))
    cam = (45, -110, 45, 45, -10, 2)
else:
    landmarks.cathedral(dict(poly=[(0, 0), (60, 0), (60, 30), (0, 30)], facing=0, name='cat'), Rng('s', 'cat'), col)
    landmarks.heritage_strip(dict(poly=[(75, 0), (115, 0), (115, 22), (75, 22)], facing=0, name='h1'), Rng('s', 'h1'), col)
    landmarks.heritage_strip(dict(poly=[(125, 0), (140, 0), (140, 12), (125, 12)], facing=0, name='h2'), Rng('s', 'h2'), col)
    landmarks.civic_tower(dict(poly=[(150, 0), (180, 0), (180, 24), (150, 24)], facing=0, name='tower'), Rng('s', 'tower'), col)
    landmarks.market_block(dict(poly=[(195, 0), (235, 0), (235, 30), (195, 30)], facing=0, name='mkt'), Rng('s', 'mkt'), col)
    landmarks.refinery(dict(poly=[(250, -20), (360, -20), (360, 60), (250, 60)], facing=0, name='ref'), Rng('s', 'ref'), col)
    pm = MeshBuilder()
    parcels.square(pm, [(0, -110), (90, -110), (90, -50), (0, -50)], Rng('s', 'sq'), 'old_island')
    landmarks.freedom_ground(pm, [(110, -120), (200, -120), (200, -40), (110, -40)], Rng('s', 'fg'), 'dense')
    pm.to_object('parcels', col, master)
    S = MeshBuilder()
    monuments.statue(S, R(220, -60), Rng('s', 'hr'), 'horse_rider')
    monuments.statue(S, R(235, -60), Rng('s', 'hu'), 'hunter')
    monuments.beach_arch(S, R(255, -60, 90), Rng('s', 'ba'))
    monuments.mural_wall(S, R(290, -60), Rng('s', 'mw'))
    monuments.billboard(S, R(330, -60), Rng('s', 'bb'))
    S.to_object('monuments', col, master)
    cam = (180, -260, 120, 180, -10, 10)
mb.to_object('kit', col, master)
cam = [float(v) for v in opt['--cam'].split(',')] if '--cam' in opt else cam
scene.camera(sc, tuple(cam[:3]), tuple(cam[3:]), lens=float(opt.get('--lens', 30)))
scene.render(sc, out, res=(2400, 1300))
print('WROTE', out)
