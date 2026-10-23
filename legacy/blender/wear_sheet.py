"""A street of Maze houses on their own, to judge wear and age close up (no tile build).
blender -b --factory-startup -P legacy/blender/wear_sheet.py -- [--detail web|full] [--vc] [--district maze] [--view street|high|roofs] [--out ...]
--vc renders the vertex colours alone, the way Unreal's master material shows them (the Blender shader's wear is not there)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import scene  # noqa: E402
from gidi_kit import archetypes, detail, wear  # noqa: E402
from gidi_kit.core import MeshBuilder  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
wires = MeshBuilder()
from gidi_kit.core import Rng  # noqa: E402
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = {}
for i, a in enumerate(args):
    if a.startswith('--'):
        opt[a] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('--') else True
detail.LEVEL = opt.get('--detail', 'web')
D = opt.get('--district', 'maze')
view = opt.get('--view', 'street')
out = opt.get('--out', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', f'wear_{D}_{detail.LEVEL}_{view}{"_vc" if opt.get("--vc") else ""}.jpg'))
sc = scene.reset(); scene.sky_and_sun(sc); scene.ground(sc, col=(0.32, 0.27, 0.22))
col = sc.collection

# (width, depth, storeys, flat roof, shop, tank, dish, tyres): one row facing the street (+y is the street side)
ROW = [(9, 10, 1, False, False, False, False, 3), (7, 9, 2, True, True, True, True, 0), (11, 10, 1, False, False, False, True, 0),
       (8, 10, 3, True, False, True, False, 0), (10, 9, 2, False, True, False, False, 2), (9, 10, 2, True, False, False, True, 0)]
x = 0.0
for side in (0, 1):
    x = 0.0
    for k, (w, d, s, flat, shop, tank, dish, tyres) in enumerate(ROW if side == 0 else ROW[::-1]):
        y0 = 0.0 if side == 0 else 24.0
        poly = [(x, y0 - d), (x + w, y0 - d), (x + w, y0), (x, y0)] if side == 0 else [(x + w, y0 + d), (x, y0 + d), (x, y0), (x + w, y0)]
        cx, cy = x + w / 2, y0 - d / 2 if side == 0 else y0 + d / 2
        a = dict(kind='front', storeys=s, district=D, poly=poly, facing=2, frontage=3, near_main=80, name=f'h{side}{k}',
                 house=dict(flat=flat, tank=[cx - 2, -(cy - 2)] if tank else None, dish=[cx + 2, -(cy + 1)] if dish else None, tyres=tyres, unf=False, ac=k % 3 == 1 and s),
                 front=dict(shop=shop, aw=1.4 if shop else 0, bal={2} if s > 1 and not shop else set()))
        archetypes.house(a, Rng(D, 'sheet', side, k), col)
        if k % 2 == 0:   # a service drop on every other house, as the tile's drop loop would land it
            wear.meter_drop(wires, poly[3], poly[2], (cx, cy), min(s * 3.1, 6.5) - 0.3, Rng('meter', side, k))
        x += w + 0.0
from gidi_kit import gutters  # noqa: E402
for gy, recs in ((1.0, [('covered', None), ('open', None), ('open', 'rubbish'), ('open', 'green_water'), ('covered', None)]),
                 (23.0, [('open', None), ('covered', None), ('open', 'green_water')])):
    x = 0.0
    for k, (state, fill) in enumerate(recs):
        g = dict(id=f'sheet{gy}{k}', w=0.6, depth=0.7, state=state, blocked=[dict({'from': 0, 'to': 99, 'fill': fill})] if fill else [])
        gutters.gutter(wires, [(x, gy), (x + 10, gy)], g, lambda p: True, wear=0.7)
        x += 10
from gidi_kit import parts, roadside  # noqa: E402
from mathutils import Matrix  # noqa: E402
for k, x in enumerate((4.0, 20.0, 34.0, 46.0)):   # generators in front of the far row, as the data stands them by a wall
    F = Matrix.Translation((x, 24.0, 0)) @ Matrix.Rotation(math.pi, 4, 'Z')
    parts.generator(wires, F, 0, dict(col=[(0.5, 0.05, 0.04), (0.05, 0.3, 0.06), (0.8, 0.55, 0.03), (0.2, 0.25, 0.28)][k], wear=0.6), Rng('gen', k))
roadside.warden_post(wires, Matrix.Translation((10, 12, 0)) @ Matrix.Rotation(-math.pi / 2, 4, 'Z'), Rng('wp', 1))
roadside.warden_post(wires, Matrix.Translation((40, 12, 0)) @ Matrix.Rotation(-math.pi / 2, 4, 'Z'), Rng('wp', 4))
from gidi_kit import rules  # noqa: E402
for k, (ch, y) in enumerate((('dense', 2.0), ('dense', 10.0), ('elite', 18.0))):   # compound walls as the data draws them: open lines, gates at points
    wr_ = Rng('sheetwall', k)
    sp = rules.compound_spec(ch, wr_)
    if k < 2:
        sp.update(top='bottles', wear=0.8)
    parts.compound_wall(wires, [(62, y), (92, y), (92, y + 6)], sp, wr_, closed=False, gates=[(77.0 + k * 3, y)])
wires.to_object('wires', col, master)
if opt.get('--vc'):   # Unreal's view: the vertex colour alone, rough, no procedural wear
    m = bpy.data.materials.new('vc'); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    at_ = nt.nodes.new('ShaderNodeVertexColor'); at_.layer_name = 'Col'; nt.links.new(at_.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.85
    m.use_backface_culling = True   # as Unreal's master materials do: a face wound the wrong way vanishes here too
    for ob in col.objects:
        if ob.type == 'MESH' and ob.name != 'ground':
            for s_ in ob.material_slots:
                if s_.material and 'glass' not in s_.material.name:
                    s_.material = m
cams = {'street': ((22, 12, 1.7), (14, -2, 3.0), 24), 'close': ((30, 8, 1.7), (30, -1, 2.6), 22), 'lit': ((24, 13, 1.7), (24, 25, 3.0), 22), 'high': ((-14, 40, 22), (24, 6, 2), 26), 'roofs': ((26, 34, 30), (26, 6, 4), 30), 'walls': ((70, -8, 2.2), (78, 6, 1.2), 26)}
loc, tgt, lens = cams[view] if '--cam' not in opt else (tuple(float(v) for v in opt['--cam'].split(',')[:3]), tuple(float(v) for v in opt['--cam'].split(',')[3:6]), 24)
scene.camera(sc, loc, tgt, lens=lens)
scene.render(sc, out, res=(1800, 1100))
print('WROTE', out)
