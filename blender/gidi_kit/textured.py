"""Photo textures on the kit's material slots (the eye tests now; the same files go into Unreal later, so the look the owner
passes is the one that ships).

The textures live outside the repo (CC0 Poly Haven surfaces, ~/Real-world/textures/polyhaven/<surface>/<surface>_<map>_2k.jpg);
point GIDI_TEXTURES (or kit_test.py --textures) at that folder. Each slot keeps the kit's vertex colour as its colour: the
texture only adds its own variation (its colour divided by its average, so a green wall stays the green the map asked for),
and its normal and roughness maps. Wear (the vertex 'Wear', also in the colour's alpha) blends in the slot's aged surface:
rust on zinc and steel, worn plaster on paint, dark stains on concrete. UVs are the kit's metre-scale box projection
(core.MeshBuilder), so each surface tiles at its real size.
"""
import os

import bpy

# slot -> (detail surface, metres per tile, aged surface or None, how much of the aged surface's own colour shows when worn,
#          the wear at which ageing starts and is full)
SLOTS = {
    'paint': ('painted_plaster_wall', 2.5, 'worn_plaster_wall', 0.0, (0.6, 1.4)),
    'block': ('concrete_block_wall', 2.0, None, 0.0, (0.35, 1.0)),
    'concrete': ('concrete_floor_worn_001', 2.5, 'damaged_concrete_floor', 0.0, (0.4, 1.2)),
    'zinc': ('corrugated_iron', 2.0, 'rusty_metal_sheet', 0.85, (0.35, 1.0)),
    'steel': ('rusty_painted_metal', 1.5, 'rusty_metal_sheet', 0.6, (0.35, 1.0)),
    'asphalt': ('asphalt_02', 4.0, 'road_damaged', 0.0, (0.6, 1.4)),
    'mud': ('dirt_floor', 3.0, None, 0.0, (0.35, 1.0)),
    'ground': ('dirt_floor', 3.0, None, 0.0, (0.35, 1.0)),
    'wood': ('weathered_planks', 1.5, None, 0.0, (0.35, 1.0)),
}


def root():
    return os.environ.get('GIDI_TEXTURES', os.path.expanduser('~/Real-world/textures/polyhaven'))


def _img(base, surf, kind, colour=False):
    p = os.path.join(base, surf, f'{surf}_{kind}_2k.jpg')
    if not os.path.exists(p):
        return None
    im = bpy.data.images.load(p, check_existing=True)
    im.colorspace_settings.name = 'sRGB' if colour else 'Non-Color'
    return im


_MEAN = {}


def _mean(im):
    """The texture's average colour (linear), so it can be divided out and leave only its variation."""
    if im.name not in _MEAN:
        import numpy as np
        w, h = im.size
        px = np.empty(w * h * 4, dtype=np.float32)
        im.pixels.foreach_get(px)
        _MEAN[im.name] = tuple(float(v) for v in px.reshape(-1, 4)[::97, :3].mean(axis=0))
    return _MEAN[im.name]


def _slot(mat, base, surf, tile, aged, aged_show, span):
    nt = mat.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    out = N.new('ShaderNodeOutputMaterial')
    bs = N.new('ShaderNodeBsdfPrincipled')
    L.new(bs.outputs[0], out.inputs['Surface'])
    uv = N.new('ShaderNodeUVMap')
    uv.uv_map = 'UVMap'
    sc = N.new('ShaderNodeVectorMath')
    sc.operation = 'SCALE'
    sc.inputs['Scale'].default_value = 1.0 / tile
    L.new(uv.outputs['UV'], sc.inputs[0])
    col = N.new('ShaderNodeAttribute')
    col.attribute_name = 'Col'
    wear = N.new('ShaderNodeAttribute')
    wear.attribute_name = 'Wear'

    def tex(im):
        t = N.new('ShaderNodeTexImage')
        t.image = im
        L.new(sc.outputs[0], t.inputs['Vector'])
        return t

    def detail(im):   # texture / its mean: its variation only, around 1.0
        t = tex(im)
        m = _mean(im)
        d = N.new('ShaderNodeVectorMath')
        d.operation = 'DIVIDE'
        L.new(t.outputs['Color'], d.inputs[0])
        d.inputs[1].default_value = tuple(max(1e-3, v) for v in m)
        return d.outputs[0]

    def mul(a, b):
        m = N.new('ShaderNodeVectorMath')
        m.operation = 'MULTIPLY'
        L.new(a, m.inputs[0])
        L.new(b, m.inputs[1])
        return m.outputs[0]

    def mix(fac, a, b):
        m = N.new('ShaderNodeMix')
        m.data_type = 'RGBA'
        L.new(fac, m.inputs['Factor'])
        L.new(a, m.inputs[6])
        L.new(b, m.inputs[7])
        return m.outputs[2]

    def ramp(src, lo, hi):
        r = N.new('ShaderNodeMapRange')
        L.new(src, r.inputs['Value'])
        r.inputs['From Min'].default_value, r.inputs['From Max'].default_value = lo, hi
        return r.outputs['Result']

    dif = _img(base, surf, 'diffuse', True)
    colour = mul(col.outputs['Color'], detail(dif))
    fac = None
    if aged:
        adif = _img(base, aged, 'diffuse', True)
        aged_tint = mul(col.outputs['Color'], detail(adif))
        if aged_show:   # rust: the aged surface's own colour comes through
            at = tex(adif)
            aged_tint = mix(_const(N, aged_show), aged_tint, at.outputs['Color'])
        fac = ramp(wear.outputs['Fac'], *span)
        colour = mix(fac, colour, aged_tint)
    L.new(colour, bs.inputs['Base Color'])
    rough = _img(base, surf, 'rough')
    if rough:
        L.new(tex(rough).outputs['Color'], bs.inputs['Roughness'])
    nor = _img(base, surf, 'nor_gl')
    if nor:
        nm = N.new('ShaderNodeNormalMap')
        nm.inputs['Strength'].default_value = 0.8
        L.new(tex(nor).outputs['Color'], nm.inputs['Color'])
        L.new(nm.outputs['Normal'], bs.inputs['Normal'])
    if mat.name in ('zinc', 'steel'):
        bs.inputs['Metallic'].default_value = 0.35 if mat.name == 'zinc' else 0.2


def _const(N, v):
    n = N.new('ShaderNodeValue')
    n.outputs[0].default_value = v
    return n.outputs[0]


def apply(base=None):
    """Swap the kit's master materials for textured ones, by slot name. Returns the slots done."""
    base = base or root()
    done = []
    if not os.path.isdir(base):
        print('textures: no folder at', base, '- kit materials kept')
        return done
    for name, (surf, tile, aged, show, span) in SLOTS.items():
        mat = bpy.data.materials.get(name)
        if mat is None or not os.path.isdir(os.path.join(base, surf)):
            continue
        _slot(mat, base, surf, tile, aged if aged and os.path.isdir(os.path.join(base, aged)) else None, show, span)
        done.append(name)
    return done
