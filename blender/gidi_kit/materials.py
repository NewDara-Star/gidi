"""Master materials. Each reads the mesh's 'Col' (paint colour) and 'Wear' (0..1) attributes,
so a handful of materials cover every colour and age. The same pair of attributes can drive
material instances in Unreal (vertex colour + one float), which keeps the look portable.

Wear adds what Lagos weather does: red-earth splash at the foot of walls, rain streaks under
ledges, sun-chalked paint, rust on zinc and steel, stains on concrete.
"""
import bpy

_cache = {}


def _sock(node, ident, out=False):
    for s in (node.outputs if out else node.inputs):
        if s.identifier == ident or s.name == ident:
            return s
    raise KeyError(ident)


class _NT:
    """Tiny helper for building node trees by code."""

    def __init__(self, mat):
        mat.use_nodes = True
        self.t = mat.node_tree
        self.n = self.t.nodes
        self.n.clear()
        self.x = 0

    def add(self, kind, **props):
        nd = self.n.new(kind)
        nd.location = (self.x, 0)
        self.x += 200
        for k, v in props.items():
            setattr(nd, k, v)
        return nd

    def link(self, a, b):
        self.t.links.new(a, b)

    def attr(self, name):
        nd = self.add('ShaderNodeAttribute', attribute_name=name, attribute_type='GEOMETRY')
        return nd

    def noise(self, scale, detail=3, vec=None, w=None):
        nd = self.add('ShaderNodeTexNoise')
        nd.inputs['Scale'].default_value = scale
        nd.inputs['Detail'].default_value = detail
        if vec is not None:
            self.link(vec, nd.inputs['Vector'])
        return _sock(nd, 'Fac', out=True)

    def mix(self, fac, a, b, blend='MIX'):
        nd = self.add('ShaderNodeMix', data_type='RGBA', blend_type=blend)
        self._in(fac, _sock(nd, 'Factor_Float'))
        self._in(a, _sock(nd, 'A_Color'))
        self._in(b, _sock(nd, 'B_Color'))
        return _sock(nd, 'Result_Color', out=True)

    def math(self, op, a, b=None, clamp=False):
        nd = self.add('ShaderNodeMath', operation=op, use_clamp=clamp)
        self._in(a, nd.inputs[0])
        if b is not None:
            self._in(b, nd.inputs[1])
        return nd.outputs[0]

    def ramp(self, value, lo, hi):
        """smoothstep(lo, hi, value)"""
        nd = self.add('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP')
        self._in(value, nd.inputs['Value'])
        self._in(lo, nd.inputs['From Min'])
        self._in(hi, nd.inputs['From Max'])
        return nd.outputs['Result']

    def _in(self, v, sock):
        if isinstance(v, (int, float)):
            sock.default_value = v
        elif isinstance(v, tuple):
            sock.default_value = v if len(v) == 4 else (*v, 1.0)
        else:
            self.link(v, sock)

    def world_pos(self):
        nd = self.add('ShaderNodeNewGeometry')
        return nd.outputs['Position']

    def xyz(self, vec):
        nd = self.add('ShaderNodeSeparateXYZ')
        self.link(vec, nd.inputs[0])
        return nd.outputs

    def scaled(self, vec, s):
        nd = self.add('ShaderNodeMapping')
        self.link(vec, nd.inputs['Vector'])
        nd.inputs['Scale'].default_value = s
        return nd.outputs['Vector']

    def bsdf(self, base, rough=0.8, metal=0.0, emit=None, emit_strength=0.0, alpha=None):
        p = self.add('ShaderNodeBsdfPrincipled')
        self._in(base, p.inputs['Base Color'])
        self._in(rough, p.inputs['Roughness'])
        self._in(metal, p.inputs['Metallic'])
        if emit is not None:
            self._in(emit, p.inputs['Emission Color'])
            p.inputs['Emission Strength'].default_value = emit_strength
        out = self.add('ShaderNodeOutputMaterial')
        self.link(p.outputs['BSDF'], out.inputs['Surface'])
        return p


def _weathered(nt, base, dirt=(0.30, 0.20, 0.13), splash=(0.42, 0.19, 0.09), streak_dir=True, chalk=True):
    """base colour -> colour after weathering, scaled by the Wear attribute."""
    wear = nt.attr('Wear').outputs['Fac']
    pos = nt.world_pos()
    z = nt.xyz(pos)[2]
    big = nt.noise(0.35, 4, pos)
    fine = nt.noise(6.0, 2, pos)
    # uneven, sun-chalked paint
    if chalk:
        chalky = nt.ramp(nt.noise(0.9, 3, pos), 0.55, 0.8)
        base = nt.mix(nt.math('MULTIPLY', chalky, nt.math('MULTIPLY', wear, 0.6)), base, (0.86, 0.84, 0.8))
    # stains and rain streaks (noise stretched vertically)
    stain = nt.ramp(big, 0.45, 0.75)
    if streak_dir:
        st = nt.noise(3.0, 2, nt.scaled(pos, (3.0, 3.0, 0.12)))
        stain = nt.math('ADD', stain, nt.math('MULTIPLY', nt.ramp(st, 0.5, 0.8), 0.7))
    base = nt.mix(nt.math('MULTIPLY', nt.math('MULTIPLY', stain, wear), 0.75, clamp=True), base, nt.mix(0.5, base, dirt, 'MULTIPLY'))
    # red earth splashed up the foot of the wall
    foot = nt.math('SUBTRACT', 1.0, nt.ramp(z, 0.05, nt.math('ADD', 0.5, nt.math('MULTIPLY', big, 0.9))))
    base = nt.mix(nt.math('MULTIPLY', nt.math('MULTIPLY', foot, wear), 0.8, clamp=True), base, splash)
    # fine unevenness, always a little
    base = nt.mix(nt.math('MULTIPLY', fine, 0.12), base, (0.5, 0.5, 0.5), 'MULTIPLY')
    return base, wear, big, fine


def master(name):
    if name in _cache and _cache[name].name in bpy.data.materials:
        return _cache[name]
    mat = bpy.data.materials.new(name)
    nt = _NT(mat)
    col = nt.attr('Col').outputs['Color']
    if name in ('paint', 'concrete', 'block'):
        base = col
        if name == 'block':  # sandcrete blocks: 450 x 225 mm courses
            br = nt.add('ShaderNodeTexBrick')
            br.inputs['Scale'].default_value = 1.0
            br.inputs['Mortar Size'].default_value = 0.012
            br.inputs['Brick Width'].default_value = 0.45
            br.inputs['Row Height'].default_value = 0.225
            br.inputs['Color1'].default_value = (0.42, 0.41, 0.39, 1)
            br.inputs['Color2'].default_value = (0.36, 0.35, 0.33, 1)
            br.inputs['Mortar'].default_value = (0.5, 0.48, 0.44, 1)
            uvn = nt.add('ShaderNodeUVMap')
            nt.link(uvn.outputs['UV'], br.inputs['Vector'])
            base = nt.mix(1.0, col, br.outputs['Color'], 'MULTIPLY')
        base, wear, big, fine = _weathered(nt, base, chalk=(name == 'paint'))
        nt.bsdf(base, rough=0.88)
    elif name in ('zinc', 'steel'):
        # zinc ages as a whole (dull, browner) and rusts in streaks running down the ribs, heaviest at laps and edges
        wear = nt.attr('Wear').outputs['Fac']
        pos = nt.world_pos()
        patina = nt.mix(nt.math('MULTIPLY', wear, 0.55), col, (0.36, 0.27, 0.2))
        streak = nt.noise(2.5, 3, nt.scaled(pos, (6.0, 6.0, 0.6)))
        patch = nt.noise(0.5, 3, pos)
        r = nt.ramp(nt.math('ADD', nt.math('MULTIPLY', streak, 0.6), nt.math('MULTIPLY', patch, 0.4)), nt.math('SUBTRACT', 0.85, nt.math('MULTIPLY', wear, 0.3)), 0.95)
        rust_amt = nt.math('MULTIPLY', r, nt.math('MULTIPLY', wear, 1.2), clamp=True)
        rust = nt.mix(nt.noise(18, 2, pos), (0.22, 0.09, 0.03), (0.40, 0.17, 0.06))
        base = nt.mix(rust_amt, patina, rust)
        rough = nt.math('ADD', 0.4 if name == 'zinc' else 0.5, nt.math('MULTIPLY', nt.math('ADD', rust_amt, wear), 0.3))
        metal = nt.math('SUBTRACT', 0.55 if name == 'zinc' else 0.3, nt.math('MULTIPLY', nt.math('ADD', rust_amt, wear), 0.3))
        nt.bsdf(base, rough=rough, metal=metal)
    elif name == 'glass':
        nt.bsdf(col, rough=0.06, metal=0.4)
    elif name == 'glass_lit':
        nt.bsdf(col, rough=0.06, metal=0.2, emit=(1.0, 0.72, 0.38), emit_strength=0.0)
    elif name == 'wood':
        pos = nt.world_pos()
        w = nt.add('ShaderNodeTexWave')
        w.inputs['Scale'].default_value = 3.0
        w.inputs['Distortion'].default_value = 6.0
        nt.link(nt.scaled(pos, (1, 1, 8)), w.inputs['Vector'])
        base = nt.mix(nt.math('MULTIPLY', w.outputs['Fac'], 0.35), col, nt.mix(0.5, col, (0.2, 0.12, 0.06), 'MULTIPLY'))
        base, *_ = _weathered(nt, base, chalk=False)
        nt.bsdf(base, rough=0.8)
    elif name == 'plastic':
        nt.bsdf(col, rough=0.4)
    elif name == 'rubber':
        nt.bsdf(col, rough=0.9)
    elif name == 'cloth':
        nt.bsdf(col, rough=0.95)
    elif name == 'skin':
        nt.bsdf(col, rough=0.55)
    elif name == 'emit':
        nt.bsdf(col, rough=0.5, emit=col, emit_strength=2.0)
    elif name == 'asphalt':
        # grain, a web of fine cracks (voronoi edges) that opens up with wear, oil and dust
        pos = nt.world_pos()
        wear = nt.attr('Wear').outputs['Fac']
        base = nt.mix(nt.math('MULTIPLY', nt.noise(40, 2, pos), 0.25), col, (0.5, 0.5, 0.5), 'MULTIPLY')
        vor = nt.add('ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE')
        vor.inputs['Scale'].default_value = 1.6
        nt.link(pos, vor.inputs['Vector'])
        crack = nt.math('MULTIPLY', nt.math('SUBTRACT', 1.0, nt.ramp(vor.outputs['Distance'], 0.0, 0.025)), nt.math('MULTIPLY', wear, 0.9))
        base = nt.mix(crack, base, (0.03, 0.03, 0.03))
        oil = nt.ramp(nt.noise(0.6, 3, pos), 0.62, 0.8)
        base = nt.mix(nt.math('MULTIPLY', oil, 0.4), base, (0.05, 0.05, 0.05))
        nt.bsdf(base, rough=0.9)
    elif name == 'mud':
        # laterite and silt: Wear is wetness here; wet mud is darker and glossy
        pos = nt.world_pos()
        wet = nt.attr('Wear').outputs['Fac']
        base = nt.mix(nt.math('MULTIPLY', nt.noise(9, 3, pos), 0.3), col, (0.5, 0.45, 0.4), 'MULTIPLY')
        base = nt.mix(nt.math('MULTIPLY', wet, 0.35), base, (0.1, 0.06, 0.04), 'MULTIPLY')
        rough = nt.math('SUBTRACT', 0.95, nt.math('MULTIPLY', nt.math('MULTIPLY', wet, nt.ramp(nt.noise(1.5, 2, pos), 0.3, 0.7)), 0.7))
        nt.bsdf(base, rough=rough)
    elif name == 'pavers':
        br = nt.add('ShaderNodeTexBrick')
        br.inputs['Scale'].default_value = 1.0
        br.inputs['Mortar Size'].default_value = 0.006
        br.inputs['Brick Width'].default_value = 0.2
        br.inputs['Row Height'].default_value = 0.1
        br.inputs['Color1'].default_value = (0.5, 0.5, 0.5, 1)
        br.inputs['Color2'].default_value = (0.42, 0.42, 0.41, 1)
        br.inputs['Mortar'].default_value = (0.25, 0.24, 0.22, 1)
        nt.link(nt.world_pos(), br.inputs['Vector'])
        base = nt.mix(1.0, col, br.outputs['Color'], 'MULTIPLY')
        base = nt.mix(1.0, base, (2.0, 2.0, 2.0), 'MULTIPLY')
        base, *_ = _weathered(nt, base, chalk=False, streak_dir=False)
        nt.bsdf(base, rough=0.85)
    elif name == 'water':
        pos = nt.world_pos()
        p = nt.add('ShaderNodeBsdfPrincipled')
        nt._in(col, p.inputs['Base Color'])
        p.inputs['Roughness'].default_value = 0.12  # muddy water: soft reflections, mostly its own colour
        p.inputs['Specular IOR Level'].default_value = 0.35
        bump = nt.add('ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.08
        nt.link(nt.noise(3.0, 2, pos), bump.inputs['Height'])
        nt.link(bump.outputs['Normal'], p.inputs['Normal'])
        out = nt.add('ShaderNodeOutputMaterial')
        nt.link(p.outputs['BSDF'], out.inputs['Surface'])
    elif name == 'ground':
        base, *_ = _weathered(nt, col, chalk=False)
        nt.bsdf(base, rough=0.95)
    else:
        nt.bsdf(col)
    _cache[name] = mat
    return mat
