"""Shared scene setup for previews: sky, sun, ground, camera, render settings."""
import math

import bpy
from mathutils import Vector


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    return sc


def sky_and_sun(sc, time='day'):
    """Nishita-free sky: a gradient world plus a sun lamp (works the same in EEVEE and Cycles)."""
    w = bpy.data.worlds.new('sky')
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    nt.links.new(tc.outputs['Generated'] if False else tc.outputs['Window'], sep.inputs[0]) if False else None
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    nt.links.new(geo.outputs['Incoming'], sep.inputs[0])
    neg = nt.nodes.new('ShaderNodeMath'); neg.operation = 'MULTIPLY'; neg.inputs[1].default_value = -1.0
    nt.links.new(sep.outputs['Z'], neg.inputs[0])
    nt.links.new(neg.outputs[0], ramp.inputs['Fac'])
    el = ramp.color_ramp.elements
    if time == 'day':
        el[0].position, el[0].color = 0.0, (0.62, 0.78, 0.92, 1)
        el[1].position, el[1].color = 0.55, (0.08, 0.27, 0.68, 1)
        strength, sun_col, sun_e, sun_rot = 1.0, (1.0, 0.95, 0.86), 4.5, (math.radians(45), 0, math.radians(35))
    else:
        el[0].position, el[0].color = 0.0, (0.95, 0.5, 0.25, 1)
        el[1].position, el[1].color = 0.5, (0.12, 0.12, 0.35, 1)
        strength, sun_col, sun_e, sun_rot = 0.6, (1.0, 0.55, 0.3), 2.5, (math.radians(80), 0, math.radians(60))
    nt.links.new(ramp.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = strength
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
    sun = bpy.data.lights.new('sun', 'SUN')
    sun.energy = sun_e
    sun.color = sun_col
    sun.angle = math.radians(2.5)
    ob = bpy.data.objects.new('sun', sun)
    ob.rotation_euler = sun_rot
    sc.collection.objects.link(ob)
    return ob


def ground(sc, size=600, col=(0.55, 0.32, 0.18)):
    from gidi_kit.core import MeshBuilder
    from gidi_kit.materials import master
    mb = MeshBuilder()
    h = size / 2
    mb.face([(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0)], 'ground', col, 0.4)
    return mb.to_object('ground', sc.collection, master)


def camera(sc, loc, target, lens=35):
    cam = bpy.data.cameras.new('cam')
    cam.lens = lens
    cam.clip_end = 3000
    ob = bpy.data.objects.new('cam', cam)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    sc.collection.objects.link(ob)
    sc.camera = ob
    return ob


def render(sc, path, res=(1600, 1000), samples=32, engine='BLENDER_EEVEE'):
    sc.render.engine = engine
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'JPEG'
    sc.render.image_settings.quality = 90
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Punchy'
    try:
        sc.eevee.taa_render_samples = samples
        sc.eevee.use_shadows = True
        sc.eevee.use_raytracing = True
        sc.eevee.ray_tracing_options.resolution_scale = '2'
        sc.eevee.use_fast_gi = True
    except AttributeError:
        pass
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
