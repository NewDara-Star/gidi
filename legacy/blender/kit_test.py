"""A kit eye test: build one Street View spot from its map record with the old town kit and shoot it from the Street View's
own camera (decisions: "A kit is proven by rebuilding real streets from it", "The owner's eye passes a kit").
blender -b --factory-startup -P legacy/blender/kit_test.py -- --map <spot>/map.json --out <spot>/rebuild.jpg [--samples 16] [--blend <file>]
    [--textures <dir> | --no-textures]   (textures default to $GIDI_TEXTURES or ~/gidi-data/textures/polyhaven)
    [--cam x,y,z --at x,y,z [--hfov deg] [--size w,h]]   a close-up of one part, from its own camera, in the same light
The map's 'shot' block gives the camera (position, heading, pitch, horizontal field of view, frame) and the light (a sun
angle and cloud cover, or the old overcast); the kit
reads the rest. Light by default: EEVEE, low samples, the shot's own frame size."""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
import scene  # noqa: E402
from gidi_kit import detail, oldtown, textured  # noqa: E402

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = {}
for i, a in enumerate(args):
    if a.startswith('--'):
        opt[a] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('--') else True
detail.LEVEL = 'full'
spot = json.load(open(opt['--map']))
spot['_dir'] = os.path.dirname(os.path.abspath(opt['--map']))   # the ground grids lie beside the map
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


def sky_sun(sc, sun, clouds=0.55, strength=0.35, sun_w=4.0, seen_gain=1.0, seen_sky=None):
    """A clear physical sky (Blender's multiple-scattering sky) with bright broken cumulus over it, and a hard sun at
    the Street View's sun angle. sun: {azimuth_deg from north, clockwise; elevation_deg}; the map's frame has x east,
    y north. clouds: how much of the sky they cover. The camera sees the clouds; the light is the sky dimmed toward grey by
    them, so shade under eaves stays dark. seen_gain lifts only what the camera sees of the sky (against a lowered exposure).
    seen_sky: the map's sky colours as the photo shows them ({horizon, zenith} hex): the camera sees that blue, graded up
    from the horizon, under the clouds, in place of the physical sky's own (which the light still comes from)."""
    az, el = math.radians(sun['azimuth_deg']), math.radians(sun['elevation_deg'])
    d = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    w = bpy.data.worlds.new('sky')
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    out = N.new('ShaderNodeOutputWorld')
    bg = N.new('ShaderNodeBackground')
    sk = N.new('ShaderNodeTexSky')
    sk.sky_type = 'MULTIPLE_SCATTERING'
    sk.sun_disc = False
    sk.sun_elevation = el
    sk.sun_rotation = math.atan2(d.y, d.x) - math.pi / 2
    sk.air_density, sk.aerosol_density = 1.0, 2.5   # tropical haze
    # a cloud layer: the view ray hits a flat sheet overhead (x/z, y/z), broken noise on it, thinning toward the horizon
    geo = N.new('ShaderNodeNewGeometry')
    sep = N.new('ShaderNodeSeparateXYZ')
    L.new(geo.outputs['Incoming'], sep.inputs[0])
    nz = N.new('ShaderNodeMath'); nz.operation = 'MULTIPLY'; nz.inputs[1].default_value = -1.0
    L.new(sep.outputs['Z'], nz.inputs[0])
    cz = N.new('ShaderNodeMath'); cz.operation = 'MAXIMUM'; cz.inputs[1].default_value = 0.04
    L.new(nz.outputs[0], cz.inputs[0])
    inv = N.new('ShaderNodeVectorMath'); inv.operation = 'DIVIDE'
    L.new(geo.outputs['Incoming'], inv.inputs[0])
    cmb = N.new('ShaderNodeCombineXYZ')
    L.new(cz.outputs[0], cmb.inputs[0]); L.new(cz.outputs[0], cmb.inputs[1]); L.new(cz.outputs[0], cmb.inputs[2])
    L.new(cmb.outputs[0], inv.inputs[1])
    noise = N.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 0.6
    noise.inputs['Detail'].default_value = 8.0
    noise.inputs['Roughness'].default_value = 0.6
    L.new(inv.outputs[0], noise.inputs['Vector'])
    cr = N.new('ShaderNodeValToRGB')   # cloud density: none below the threshold, white puffs above it
    L.new(noise.outputs['Fac'], cr.inputs['Fac'])
    e = cr.color_ramp.elements
    e[0].position, e[0].color = 0.6 - clouds * 0.25, (0, 0, 0, 1)
    e[1].position, e[1].color = 0.78 - clouds * 0.25, (1, 1, 1, 1)
    shadeR = N.new('ShaderNodeValToRGB')   # cloud colour: bright tops, grey bellies
    L.new(noise.outputs['Fac'], shadeR.inputs['Fac'])
    f = shadeR.color_ramp.elements
    g_ = 0.62 + 0.3 * max(0.0, clouds - 0.6)   # a full cover is white cloud, its bellies only a little grey
    f[0].position, f[0].color = 0.55, (g_, g_ + 0.01, g_ + 0.03, 1)
    f[1].position, f[1].color = 0.85, (1.0, 1.0, 1.0, 1)
    cloud_bright = N.new('ShaderNodeVectorMath'); cloud_bright.operation = 'SCALE'
    cloud_bright.inputs['Scale'].default_value = 1.0 / strength * 0.9
    L.new(shadeR.outputs['Color'], cloud_bright.inputs[0])
    seen = N.new('ShaderNodeMix'); seen.data_type = 'RGBA'
    L.new(cr.outputs['Color'], seen.inputs['Factor'])
    if seen_sky:   # the photo's own blue, horizon to zenith
        from gidi_kit.core import hex_rgb
        up = N.new('ShaderNodeMath'); up.operation = 'POWER'; up.use_clamp = True
        L.new(nz.outputs[0], up.inputs[0])   # how far up the view looks (the world's incoming points back at the camera)
        up.inputs[1].default_value = 0.6
        grad = N.new('ShaderNodeMix'); grad.data_type = 'RGBA'
        L.new(up.outputs[0], grad.inputs['Factor'])
        grad.inputs[6].default_value = tuple(v / strength for v in hex_rgb(seen_sky['horizon'])) + (1,)
        grad.inputs[7].default_value = tuple(v / strength for v in hex_rgb(seen_sky['zenith'])) + (1,)
        L.new(grad.outputs[2], seen.inputs[6])
    else:
        L.new(sk.outputs['Color'], seen.inputs[6])
    L.new(cloud_bright.outputs[0], seen.inputs[7])
    lit = N.new('ShaderNodeMix'); lit.data_type = 'RGBA'   # what lights the scene: the sky, greyed by the cloud cover
    lit.inputs['Factor'].default_value = clouds * 0.8
    L.new(sk.outputs['Color'], lit.inputs[6])
    lit.inputs[7].default_value = (0.8 / strength * 0.3, 0.75 / strength * 0.3, 0.68 / strength * 0.3, 1)
    lp = N.new('ShaderNodeLightPath')
    ms = N.new('ShaderNodeMix'); ms.data_type = 'RGBA'
    L.new(lp.outputs['Is Camera Ray'], ms.inputs['Factor'])
    L.new(lit.outputs[2], ms.inputs[6])
    L.new(seen.outputs[2], ms.inputs[7])
    gain = N.new('ShaderNodeMix'); gain.data_type = 'RGBA'; gain.blend_type = 'MULTIPLY'
    L.new(lp.outputs['Is Camera Ray'], gain.inputs['Factor'])
    L.new(ms.outputs[2], gain.inputs[6])
    gain.inputs[7].default_value = (seen_gain, seen_gain, seen_gain, 1)
    L.new(gain.outputs[2], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = strength
    L.new(bg.outputs['Background'], out.inputs['Surface'])
    lamp = bpy.data.lights.new('sun', 'SUN')
    lamp.energy = sun_w
    lamp.color = (1.0, 0.92, 0.82)
    lamp.angle = math.radians(sun.get('angle_deg', 1.0))
    ob = bpy.data.objects.new('sun', lamp)
    ob.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    sc.collection.objects.link(ob)


if shot.get('sun'):
    sky_sun(sc, shot['sun'], shot.get('cloud_cover', 0.55), shot.get('sky_strength', 0.35), shot.get('sun_w', 4.0), 2 ** -float(shot.get('exposure', 0.0)), shot.get('sky_seen'))
else:
    overcast(sc)
oldtown.build(spot, sc.collection)
if not opt.get('--no-textures'):   # the photo textures, outside the repo (gidi_kit/textured.py)
    print('textured:', textured.apply(opt.get('--textures')))
cx, cy, cz = shot['camera_xyz']
hd, pt = math.radians(shot.get('heading_deg', 0)), math.radians(shot.get('pitch_deg', 0))
if opt.get('--cam'):
    vec = lambda s_: tuple(float(v) for v in s_.split(','))
    cam = scene.camera(sc, vec(opt['--cam']), vec(opt['--at']))
else:
    cam = scene.camera(sc, (cx, cy, cz), (cx + math.cos(hd) * math.cos(pt) * 100, cy + math.sin(hd) * math.cos(pt) * 100, cz + math.sin(pt) * 100))
cam.data.sensor_fit = 'HORIZONTAL'
cam.data.sensor_width = 36.0
cam.data.lens = 18.0 / math.tan(math.radians(float(opt.get('--hfov', shot.get('hfov_deg', 90)))) / 2)
if opt.get('--blend'):
    bpy.ops.wm.save_as_mainfile(filepath=opt['--blend'])
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x, sc.render.resolution_y = [int(v) for v in opt['--size'].split(',')] if opt.get('--size') else shot.get('frame_px', (1200, 670))
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'JPEG'
sc.render.image_settings.quality = 90
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
sc.view_settings.exposure = float(shot.get('exposure', 0.0))
sc.eevee.taa_render_samples = int(opt.get('--samples', 16))
sc.eevee.use_shadows = True
sc.eevee.use_fast_gi = True
sc.eevee.use_raytracing = True
sc.eevee.fast_gi_distance = float(shot.get('gi_distance_m', 3.0))
sc.render.filepath = opt['--out']
bpy.ops.render.render(write_still=True)
print('WROTE', opt['--out'])
