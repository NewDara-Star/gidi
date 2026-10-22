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
    """The texture's average colour (linear, as the shader sees it), so it can be divided out and leave only its variation."""
    if im.name not in _MEAN:
        import numpy as np
        w, h = im.size
        px = np.empty(w * h * 4, dtype=np.float32)
        im.pixels.foreach_get(px)
        c = px.reshape(-1, 4)[::97, :3]
        if im.colorspace_settings.name == 'sRGB':   # pixels come back as stored (sRGB); the shader sees them linear
            c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
        _MEAN[im.name] = tuple(float(v) for v in c.mean(axis=0))
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
    slot = mat.name.partition(':')[0]
    if slot in ('zinc', 'steel'):
        bs.inputs['Metallic'].default_value = 0.35 if slot == 'zinc' else 0.2


def _const(N, v):
    n = N.new('ShaderNodeValue')
    n.outputs[0].default_value = v
    return n.outputs[0]


def _roadbed(mat, base):
    """The street's ground (roadbed.py): earth, dust, tar and mud layers, each its map colour times its photo surface's
    variation, blended by the sheet's Edge, Dust, Tar and Mud attributes and by each surface's own height map, so tar
    shows on its high grains first and dust settles into the low ones."""
    import json
    spec = json.loads(mat.get('gidi_layers', '{}') or '{}')
    cols, surfs = spec.get('colours', {}), spec.get('surfaces', {})
    nt = mat.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    out = N.new('ShaderNodeOutputMaterial')
    bs = N.new('ShaderNodeBsdfPrincipled')
    L.new(bs.outputs[0], out.inputs['Surface'])
    uv = N.new('ShaderNodeUVMap')
    uv.uv_map = 'UVMap'

    def attr(name):
        a = N.new('ShaderNodeAttribute')
        a.attribute_name = name
        return a.outputs['Fac']

    def math(op, a, b):
        m = N.new('ShaderNodeMath')
        m.operation = op
        for i, v in enumerate((a, b)):
            if isinstance(v, (int, float)):
                m.inputs[i].default_value = v
            else:
                L.new(v, m.inputs[i])
        return m.outputs[0]

    def mixc(fac, a, b, kind='RGBA'):
        m = N.new('ShaderNodeMix')
        m.data_type = kind
        L.new(fac, m.inputs['Factor'])
        ia, ib = (6, 7) if kind == 'RGBA' else (2, 3)
        for i, v in ((ia, a), (ib, b)):
            if isinstance(v, (int, float, tuple)):
                m.inputs[i].default_value = v
            else:
                L.new(v, m.inputs[i])
        return m.outputs[2 if kind == 'RGBA' else 0]

    GRAIN = {'earth': 0.5, 'dust': 0.45, 'tar': 0.7, 'mud': 0.8}
    NORMAL_STRENGTH = 0.35   # the ground's grain stays fine; its shape is the geometry
    TILE = {'earth': 3.0, 'dust': 3.0, 'tar': 4.0, 'mud': 2.5}
    ROUGH = {'earth': 0.95, 'dust': 0.97, 'tar': 0.85, 'mud': 0.75}
    lay = {}
    for k in ('earth', 'dust', 'tar', 'mud'):
        surf = surfs.get(k)
        sc = N.new('ShaderNodeVectorMath')
        sc.operation = 'SCALE'
        sc.inputs['Scale'].default_value = 1.0 / TILE[k]
        L.new(uv.outputs['UV'], sc.inputs[0])

        def tex(kind, colour=False):
            im = _img(base, surf, kind, colour) if surf else None
            if im is None:
                return None, None
            t = N.new('ShaderNodeTexImage')
            t.image = im
            L.new(sc.outputs[0], t.inputs['Vector'])
            return t, im
        t, im = tex('diffuse', True)
        tint = N.new('ShaderNodeRGB')
        tint.outputs[0].default_value = (*cols.get(k, (0.3, 0.25, 0.2)), 1)
        if t:
            d = N.new('ShaderNodeVectorMath')
            d.operation = 'DIVIDE'
            L.new(t.outputs['Color'], d.inputs[0])
            d.inputs[1].default_value = tuple(max(1e-3, v) for v in _mean(im))
            g = N.new('ShaderNodeMix')   # only part of the photo's grain: packed street dust is smoother than the photo's
            g.data_type = 'RGBA'
            g.inputs['Factor'].default_value = GRAIN.get(k, 1.0)
            g.inputs[6].default_value = (1, 1, 1, 1)
            L.new(d.outputs[0], g.inputs[7])
            m = N.new('ShaderNodeVectorMath')
            m.operation = 'MULTIPLY'
            L.new(tint.outputs[0], m.inputs[0])
            L.new(g.outputs[2], m.inputs[1])
            colour = m.outputs[0]
        else:
            colour = tint.outputs[0]
        # a Metal shader takes 16 samplers, EEVEE uses some: height maps only where they blend, normals for dust and tar
        dt, _ = tex('displacement') if k != 'earth' else (None, None)
        nt_, _ = tex('nor_gl') if k in ('dust', 'tar') else (None, None)
        lay[k] = dict(col=colour, disp=dt.outputs['Color'] if dt else 0.5, nor=nt_.outputs['Color'] if nt_ else None, rough=ROUGH[k])

    def hb(mask, disp, soft=0.12):
        """Height blend: where the mask is half, the layer's own high grains win."""
        v = math('ADD', mask, math('MULTIPLY', math('SUBTRACT', disp, 0.5), 0.6) if not isinstance(disp, float) else 0.0)
        r = N.new('ShaderNodeMapRange')
        L.new(v, r.inputs['Value'])
        r.inputs['From Min'].default_value, r.inputs['From Max'].default_value = 0.5 - soft, 0.5 + soft
        return r.outputs['Result']

    f_dust = hb(math('SUBTRACT', 1.0, attr('Edge')), lay['dust']['disp'], 0.2)
    f_tar = hb(attr('Tar'), lay['tar']['disp'])
    f_mud = hb(attr('Mud'), lay['mud']['disp'], 0.2)
    c, r, n = lay['earth']['col'], lay['earth']['rough'], lay['dust']['nor']
    for f, k in ((f_dust, 'dust'), (f_tar, 'tar'), (f_mud, 'mud')):
        c = mixc(f, c, lay[k]['col'])
        r = mixc(f, r, lay[k]['rough'], 'FLOAT')
        if k == 'tar' and n is not None and lay[k]['nor'] is not None:
            n = mixc(f, n, lay[k]['nor'])
    # beaten wheel tracks: darker, smoother; wet ground: darker, a little glossy; standing water: dark, mirror-flat
    track, wet, water = attr('Track'), attr('Wet'), attr('Water')
    for f, k, rough in ((track, 0.72, 0.8), (wet, 0.55, 0.4), (water, 0.35, 0.04)):
        dark = N.new('ShaderNodeVectorMath')
        dark.operation = 'SCALE'
        dark.inputs['Scale'].default_value = k
        L.new(c, dark.inputs[0])
        c = mixc(f, c, dark.outputs[0])
        r = mixc(f, r, rough, 'FLOAT')
    L.new(c, bs.inputs['Base Color'])
    L.new(r, bs.inputs['Roughness'])
    if n is not None:
        flat = math('MAXIMUM', water, math('MULTIPLY', track, 0.6))
        n = mixc(flat, n, (0.5, 0.5, 1.0, 1.0))
        nm = N.new('ShaderNodeNormalMap')
        nm.inputs['Strength'].default_value = NORMAL_STRENGTH
        L.new(n, nm.inputs['Color'])
        L.new(nm.outputs['Normal'], bs.inputs['Normal'])


def apply(base=None):
    """Swap the kit's master materials for textured ones, by slot name. A material named 'slot:surface' is that slot with
    another surface picked by the map (a rusty roof's rusty_corrugated_iron). 'roadbed' is the street's ground. Returns the
    materials done."""
    base = base or root()
    done = []
    if not os.path.isdir(base):
        print('textures: no folder at', base, '- kit materials kept')
        return done
    has = lambda s: s and os.path.isdir(os.path.join(base, s))
    for mat in list(bpy.data.materials):
        name = mat.name
        if name == 'roadbed':
            _roadbed(mat, base)
            done.append(name)
            continue
        slot, _, pick = name.partition(':')
        if slot not in SLOTS or not mat.use_nodes:
            continue
        surf, tile, aged, show, span = SLOTS[slot]
        surf = pick if has(pick) else surf
        if not has(surf):
            continue
        _slot(mat, base, surf, tile, aged if has(aged) else None, show, span)
        done.append(name)
    return done
