"""The ground of a street piece as real geometry: a Lagos street is "just ground", up here, down there, all over the place.

A subdivided sheet over the street and its edges, its height made from the map's street fields:
- `crown_m`: the middle stands higher and falls off to the sandy edges.
- `relief`: humps and dips (`amp_m` over `scale_m`); `off_road` scales them on the earth beyond the road's edge.
- `potholes`: bowls, each where the map puts it.
- `ruts`: wheel tracks along the street; `packed` makes one a dark, smooth beaten track rather than a muddy groove.
- `edge_rut`: a channel worn along the road's edge where the tar breaks into earth (`side`, `depth_m`, `w_m`).
- `tar_fray`: how far the tar's edge wanders (1 = as drafted, 0 = a clean edge, as at a kerb).
- `tar_lip_m`: the tar patches stand this proud of the earth and dust around them, so their broken edges show.
- `puddles`: water lies flat in every spot lower than `level_m`, and the ground is dark and wet up to `wet_m`.

The surface is packed earth and sand over the tar. Tar shows in patches covering `tar_cover` of the road. Dust lies in the
low spots and drifts at the edges, mud sits in the ruts and potholes, and laterite earth shows off the road. Each of these
is a per-corner attribute (Tar, Dust, Mud, Edge, Track, Wet, Water) for the material to blend by, and a flat colour (Col) for the untextured
look. The layers' colours and their photo surfaces come from the map (`ground_colours`, `surfaces`); textured.py reads
them off the material. The ground's own shape (humps and dips, the tar's fray and patches, the edge rut's wander) is the
street's ground grids, a record stored beside the map (`ground_grid`); the kit rolls nothing.
"""
import json
import os

import bpy
import numpy as np

from .core import hex_rgb, need

COLOURS = {'earth': '#7a5a44', 'dust': '#6e5a4a', 'tar': '#4a3c35', 'mud': '#3e3128'}
SURFACES = {'earth': 'red_laterite_soil_stones', 'dust': 'dirt_floor', 'tar': 'worn_asphalt', 'mud': 'muddy_tracks'}


def _smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def grids(sp, base_dir):
    """A street's ground grids, from the file its record names (`ground_grid`, beside the map)."""
    name = need(sp, 'ground_grid', 'street ' + sp['id'])
    with np.load(os.path.join(base_dir, name)) as f:
        return {k: f[k] for k in f.files}


class Ground:
    """One street piece's ground: its height and its layers at any point (numpy arrays or floats). The ground's own
    shape (its humps and dips, where the tar's edge frays, where the tar lies, the edge rut's wander) comes from the
    street's ground grids (KIT.md section 12), read between their corners; everything else from the street's fields."""

    def __init__(self, sp, grids):
        self.sp = sp
        self.g = grids
        (self.x0, self.cy), (self.x1, _) = sp['centreline'][0], sp['centreline'][-1]
        self.half = sp['width_m'] / 2
        rel = sp.get('relief') or {}
        self.amp = rel.get('amp_m', 0.0)
        self.off_road = rel.get('off_road', 1.0)
        self.crown = sp.get('crown_m', 0.0)
        self.lip = sp.get('tar_lip_m', 0.0)
        pu = sp.get('puddles') or {}
        self.level, self.wet = pu.get('level_m'), pu.get('wet_m')
        self.pins = []   # bands held level: a covered gutter's line (y, half width)
        g = sp.get('gutter_left') or {}
        if g.get('type', 'none') != 'none':
            self.pins.append((self.cy + g['offset_m'], g['width'] / 2 + 0.35))

    def _grid(self, key, x, y):
        """A grid's value at (x, y): bilinear between its corners (exact on them), held at its edges beyond."""
        xs, ys, v = self.g['xs'], self.g['ys'], self.g[key]
        x, y = np.asarray(x, float), np.asarray(y, float)
        i = np.clip(np.searchsorted(xs, x, side='right') - 1, 0, len(xs) - 2)
        j = np.clip(np.searchsorted(ys, y, side='right') - 1, 0, len(ys) - 2)
        tx = np.clip((x - xs[i]) / (xs[i + 1] - xs[i]), 0, 1)
        ty = np.clip((y - ys[j]) / (ys[j + 1] - ys[j]), 0, 1)
        return (v[i, j] * (1 - tx) + v[i + 1, j] * tx) * (1 - ty) + (v[i, j + 1] * (1 - tx) + v[i + 1, j + 1] * tx) * ty

    def _along(self, key, x):
        return np.interp(np.asarray(x, float), self.g['xs'], self.g[key])

    def _relief(self, x, y):
        return self._grid('relief', x, y)

    def _inside(self, x, y):
        return _smooth(-0.1, 0.5, self.half - np.abs(y - self.cy) + self._grid('fray', x, y) * self.sp.get('tar_fray', 1.0))

    def _tar(self, x, y, soft=0.08):
        rel = self._relief(x, y) if self.amp else np.zeros_like(x)
        tar = _smooth(-soft, soft, self._grid('tar', x, y)) * self._inside(x, y)
        return tar * (1 - _smooth(0.0, -0.06, rel) * self.sp.get('dust_in_low', 0.7))

    def _ruts(self, x, y, key):
        out = np.zeros_like(x)
        for r in self.sp.get('ruts', []):
            win = _smooth(r['from_x'] - 2, r['from_x'], x) * (1 - _smooth(r['to_x'], r['to_x'] + 2, x))
            out = np.maximum(out, win * np.exp(-((y - r['y']) / (r['w'] / 2)) ** 2 * 2) * r.get(key, 0.0))
        return out

    def _edge_rut(self, x, y):
        er = self.sp.get('edge_rut') or {}
        if not er:
            return np.zeros_like(x)
        wob = self._along('rut_wob', x)
        out = np.zeros_like(x)
        for s in ((-1,) if er.get('side') == 'right' else (1,) if er.get('side') == 'left' else (-1, 1)):
            yc = self.cy + s * (self.half - er.get('w_m', 0.8) * 0.3) + wob
            out = np.maximum(out, np.exp(-((y - yc) / (er.get('w_m', 0.8) / 2)) ** 2 * 2) * self._along('rut_k', x))
        return out * er.get('depth_m', 0.15)

    def height(self, x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        d = (y - self.cy) / self.half
        h = self.crown * (1 - np.minimum(d * d, 1.6))
        inside = self._inside(x, y)
        h = h + self._relief(x, y) * (self.off_road + (1 - self.off_road) * inside)
        if self.lip:   # the tar sheet's own thickness: a sharp step at its broken edges
            h = h + self.lip * self._tar(x, y, soft=0.02)
        h = h - self._edge_rut(x, y)
        for p in self.sp.get('potholes', []):
            q = np.hypot(x - p['x'], (y - p['y']) / p.get('stretch', 1.0)) / p['r']
            h = h - p['depth'] * np.where(q < 1, (1 - q * q) ** 2, 0) + 0.012 * np.where((q > 0.9) & (q < 1.3), 1 - np.abs(q - 1.1) / 0.2, 0)
        h = h - self._ruts(x, y, 'depth')
        for yp, hw in self.pins:   # level by the gutter, so its slabs sit on the ground
            k = _smooth(hw + 0.6, hw, np.abs(y - yp))
            h = h * (1 - k)
        if self.level is not None:   # standing water: flat at its level
            h = np.maximum(h, self.level)
        return h

    def bare(self, x, y):
        """The height without standing water (where the water's floor is)."""
        lv, self.level = self.level, None
        try:
            return self.height(x, y)
        finally:
            self.level = lv

    def layers(self, x, y, h):
        """Tar, Dust, Mud, Edge, Track, Wet, Water in 0..1 at each point."""
        sp = self.sp
        inside = self._inside(x, y)
        edge = 1 - inside
        tar = self._tar(x, y)
        rel = self._relief(x, y) if self.amp else np.zeros_like(x)
        low = _smooth(0.0, -0.06, rel) * sp.get('dust_in_low', 0.7)
        far = _smooth(25, 80, x) * sp.get('far_dust', 0.0)   # the far end of the street reads lighter, dustier
        dust = np.clip(1 - tar + low * 0.5 + far, 0, 1) * inside
        mud = self._ruts(x, y, 'mud')
        for p in sp.get('potholes', []):
            q = np.hypot(x - p['x'], (y - p['y']) / p.get('stretch', 1.0)) / p['r']
            mud = np.maximum(mud, _smooth(1.0, 0.5, q) * p.get('mud', 0.8))
        er = sp.get('edge_rut') or {}
        if er:
            mud = np.maximum(mud, np.clip(self._edge_rut(x, y) / max(er.get('depth_m', 0.15), 1e-3), 0, 1) * er.get('mud', 0.6))
        track = self._ruts(x, y, 'packed') * (1 - far * 0.5)
        water = np.zeros_like(x)
        wet = np.zeros_like(x)
        if self.level is not None:
            b = self.bare(x, y)
            water = _smooth(self.level + 0.004, self.level - 0.01, b)
            wet = _smooth(self.wet if self.wet is not None else self.level + 0.05, self.level, b) * (1 - water)
        return dict(Tar=tar, Dust=dust, Mud=mud, Edge=edge, Track=track, Wet=wet, Water=water)


def build(sp, grids, collection=None, materials=None):
    """The street's ground sheet as one object (material slot 'roadbed'), its corners where the ground grids have
    theirs; returns (object, Ground). The band it covers across the street is the grids' (`band`: 8.6 m past the right
    edge and 2.9 m past the left in a first draft, the frontages' ground)."""
    G = Ground(sp, grids)
    G.ys = tuple(float(v) for v in grids['band'])
    xs, yv = grids['xs'], grids['ys']
    X, Y = np.meshgrid(xs, yv, indexing='ij')
    X, Y = X.ravel(), Y.ravel()
    Hh = G.height(X, Y)
    lay = G.layers(X, Y, Hh)
    tar, mud, edge = lay['Tar'], lay['Mud'], lay['Edge']
    nx, ny = len(xs), len(yv)
    me = bpy.data.meshes.new(sp['id'] + '_ground')
    verts = np.stack([X, Y, Hh], 1)
    ii, jj = np.meshgrid(np.arange(nx - 1), np.arange(ny - 1), indexing='ij')
    a = (ii * ny + jj).ravel()
    quads = np.stack([a, a + ny, a + ny + 1, a + 1], 1)
    me.vertices.add(len(verts))
    me.vertices.foreach_set('co', verts.astype(np.float32).ravel())
    me.loops.add(quads.size)
    me.loops.foreach_set('vertex_index', quads.astype(np.int32).ravel())
    me.polygons.add(len(quads))
    me.polygons.foreach_set('loop_start', np.arange(0, quads.size, 4, dtype=np.int32))
    me.update(calc_edges=True)
    cols = {k: np.array(hex_rgb(v)) for k, v in {**COLOURS, **(sp.get('ground_colours') or {})}.items()}
    c = cols['earth'][None] * edge[:, None] + cols['dust'][None] * (1 - edge[:, None])
    c = c * (1 - tar[:, None]) + cols['tar'][None] * tar[:, None]
    c = c * (1 - mud[:, None]) + cols['mud'][None] * mud[:, None]
    c = c * (1 - 0.3 * lay['Track'][:, None]) * (1 - 0.4 * lay['Wet'][:, None]) * (1 - 0.6 * lay['Water'][:, None])
    lv = quads.ravel()
    col = me.color_attributes.new('Col', 'FLOAT_COLOR', 'CORNER')
    col.data.foreach_set('color', np.concatenate([c[lv], np.full((len(lv), 1), 0.3)], 1).astype(np.float32).ravel())
    for name, arr in (('Wear', np.full(len(X), 0.3)), *lay.items()):
        at = me.attributes.new(name, 'FLOAT', 'CORNER')
        at.data.foreach_set('value', arr[lv].astype(np.float32))
    uv = me.uv_layers.new(name='UVMap')
    uv.data.foreach_set('uv', np.stack([X[lv], Y[lv]], 1).astype(np.float32).ravel())
    for p in me.polygons:
        p.use_smooth = True
    me.validate()
    ob = bpy.data.objects.new(me.name, me)
    mat = materials('roadbed') if materials else None
    if mat is not None:
        mat['gidi_layers'] = json.dumps({'colours': {k: list(v) for k, v in cols.items()}, 'surfaces': {**SURFACES, **(sp.get('surfaces') or {})}})
    me.materials.append(mat)
    (collection or bpy.context.scene.collection).objects.link(ob)
    return ob, G
