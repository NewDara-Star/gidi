"""A kit eye test: build one Street View spot from its map record with the old town kit and shoot it from the Street View's
own camera (decisions: "A kit is proven by rebuilding real streets from it", "The owner's eye passes a kit").
blender -b --factory-startup -P blender/kit_test.py -- --map <spot>/map.json --out <spot>/rebuild.jpg [--samples 16] [--blend <file>]
    [--textures <dir> | --no-textures]   (textures default to $GIDI_TEXTURES or ~/Real-world/textures/polyhaven)
The map's 'shot' block gives the camera (position, heading, pitch, horizontal field of view, frame) and the sky; the kit
reads the rest. Light by default: EEVEE, low samples, the shot's own frame size."""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
import scene  # noqa: E402
from gidi_kit import detail, oldtown, textured  # noqa: E402

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = {}
for i, a in enumerate(args):
    if a.startswith('--'):
        opt[a] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('--') else True
detail.LEVEL = 'full'
spot = json.load(open(opt['--map']))
shot = spot['shot']
sc = scene.reset()


def overcast(sc):
    """A bright overcast sky: a soft white-grey dome with cloud banks, a weak sun through it (soft shadows)."""
    w = bpy.data.worlds.new('overcast')
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    neg = nt.nodes.new('ShaderNodeMath'); neg.operation = 'MULTIPLY'; neg.inputs[1].default_value = -1.0
    nt.links.new(geo.outputs['Incoming'], sep.inputs[0])
    nt.links.new(sep.outputs['Z'], neg.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    nt.links.new(neg.outputs[0], ramp.inputs['Fac'])
    el = ramp.color_ramp.elements
    el[0].position, el[0].color = 0.0, (0.92, 0.92, 0.92, 1)
    el[1].position, el[1].color = 0.6, (0.62, 0.66, 0.74, 1)
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 2.2
    noise.inputs['Detail'].default_value = 6.0
    vm = nt.nodes.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY'; vm.inputs[1].default_value = (1.0, 1.0, 3.0)
    nt.links.new(geo.outputs['Incoming'], vm.inputs[0])
    nt.links.new(vm.outputs[0], noise.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB')
    nt.links.new(noise.outputs['Fac'], cr.inputs['Fac'])
    cr.color_ramp.elements[0].position, cr.color_ramp.elements[0].color = 0.42, (0.36, 0.37, 0.40, 1)
    cr.color_ramp.elements[1].position, cr.color_ramp.elements[1].color = 0.62, (1.15, 1.15, 1.15, 1)
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
    mix.inputs['Factor'].default_value = 0.85
    nt.links.new(ramp.outputs['Color'], mix.inputs[6])
    nt.links.new(cr.outputs['Color'], mix.inputs[7])
    lp = nt.nodes.new('ShaderNodeLightPath')
    ms = nt.nodes.new('ShaderNodeMix'); ms.data_type = 'RGBA'
    nt.links.new(lp.outputs['Is Camera Ray'], ms.inputs['Factor'])
    ms.inputs[6].default_value = (0.78, 0.79, 0.80, 1)   # what lights the scene: an even bright grey
    nt.links.new(mix.outputs[2], ms.inputs[7])           # what the camera sees: the clouds
    nt.links.new(ms.outputs[2], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = 1.35
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    sun = bpy.data.lights.new('sun', 'SUN')
    sun.energy = 1.8
    sun.color = (1.0, 0.97, 0.92)
    sun.angle = math.radians(25)
    ob = bpy.data.objects.new('sun', sun)
    ob.rotation_euler = (math.radians(35), 0, math.radians(150))
    sc.collection.objects.link(ob)


overcast(sc)
oldtown.build(spot, sc.collection)
if not opt.get('--no-textures'):   # the photo textures, outside the repo (gidi_kit/textured.py)
    print('textured:', textured.apply(opt.get('--textures')))
cx, cy, cz = shot['camera_xyz']
hd, pt = math.radians(shot.get('heading_deg', 0)), math.radians(shot.get('pitch_deg', 0))
cam = scene.camera(sc, (cx, cy, cz), (cx + math.cos(hd) * math.cos(pt) * 100, cy + math.sin(hd) * math.cos(pt) * 100, cz + math.sin(pt) * 100))
cam.data.sensor_fit = 'HORIZONTAL'
cam.data.sensor_width = 36.0
cam.data.lens = 18.0 / math.tan(math.radians(shot.get('hfov_deg', 90)) / 2)
if opt.get('--blend'):
    bpy.ops.wm.save_as_mainfile(filepath=opt['--blend'])
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x, sc.render.resolution_y = shot.get('frame_px', (1200, 670))
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'JPEG'
sc.render.image_settings.quality = 90
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
sc.eevee.taa_render_samples = int(opt.get('--samples', 16))
sc.eevee.use_shadows = True
sc.eevee.use_fast_gi = True
sc.eevee.use_raytracing = True
sc.eevee.fast_gi_distance = 3.0
sc.render.filepath = opt['--out']
bpy.ops.render.render(write_still=True)
print('WROTE', opt['--out'])
