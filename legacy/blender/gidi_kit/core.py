"""Core of the Gidi kit: seeded randomness and a mesh builder.

Every object gets its own random stream from a stable key (district, building index, salt),
so the same building always comes out the same, and changing one building never shifts another.
"""
import hashlib
import math
import random

import bpy
import bmesh
from mathutils import Matrix, Vector


# ---------------------------------------------------------------- randomness
class Rng(random.Random):
    """random.Random seeded from any key; adds weighted picks and child streams."""

    def __init__(self, *key):
        self.key = '/'.join(str(k) for k in key)
        super().__init__(int(hashlib.sha1(self.key.encode()).hexdigest()[:15], 16))

    def child(self, *salt):
        return Rng(self.key, *salt)

    def pick(self, items, weights=None):
        """items: list, or dict {item: weight}."""
        if isinstance(items, dict):
            items, weights = list(items.keys()), list(items.values())
        return self.choices(items, weights=weights, k=1)[0]

    def chance(self, p):
        return self.random() < p

    def between(self, lo, hi):
        return lo + (hi - lo) * self.random()


class MissingRecord(KeyError):
    """A record the kit needs is not on the map. The kit draws only what the map holds (KIT.md section 12, "Records"):
    draft the spot (legacy/blender/kit_draft.py) or add the record by hand."""


def need(d, key, what):
    """d[key], or MissingRecord naming what is missing (`what`: whose record it is)."""
    if key not in d:
        raise MissingRecord(f'{what}: no {key!r} record on the map')
    return d[key]


def hex_rgb(h):
    """'#rrggbb' or 0xrrggbb -> linear RGB tuple (Blender colour attributes are linear)."""
    if isinstance(h, str):
        h = int(h.lstrip('#'), 16)
    c = [((h >> s) & 255) / 255 for s in (16, 8, 0)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def shade(rgb, f):
    return tuple(min(1.0, c * f) for c in rgb)


# ---------------------------------------------------------------- mesh builder
class MeshBuilder:
    """Collects faces with a material, a colour and a wear value per face corner.

    Colour goes to the 'Col' attribute, wear (0 clean .. 1 worn) to 'Wear'. The master
    materials read both, so one material serves every paint colour and every age.
    """

    def __init__(self):
        self.verts, self.faces, self.mats, self.cols, self.wears, self.uvs = [], [], [], [], [], []
        self.slots = []

    def slot(self, name):
        if name not in self.slots:
            self.slots.append(name)
        return self.slots.index(name)

    def face(self, pts, mat, col=(1, 1, 1), wear=0.0, uvs=None):
        base = len(self.verts)
        self.verts.extend(Vector(p) for p in pts)
        self.faces.append(tuple(range(base, base + len(pts))))
        self.mats.append(self.slot(mat))
        cols = col if isinstance(col, list) else [col] * len(pts)
        self.cols.append(cols)
        self.wears.append(wear)
        self.uvs.append(uvs)

    def box(self, mat, m, col, wear=0.0, size=(1, 1, 1), skip=()):
        """A box of `size` centred at the origin, transformed by matrix m.
        skip: faces to leave out ('-z' bottom etc.) when they would never be seen."""
        sx, sy, sz = (s / 2 for s in size)
        c = [m @ Vector((x * sx, y * sy, z * sz)) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
        # corner index = xi*4 + yi*2 + zi
        quads = {'-x': (0, 1, 3, 2), '+x': (4, 6, 7, 5), '-y': (0, 4, 5, 1), '+y': (2, 3, 7, 6), '-z': (0, 2, 6, 4), '+z': (1, 5, 7, 3)}
        mirrored = m.to_3x3().determinant() < 0   # a wall frame (frame()) is a mirror: keep the faces facing out
        for k, q in quads.items():
            if k in skip:
                continue
            self.face([c[i] for i in (q[::-1] if mirrored else q)], mat, col, wear)

    def merge_mesh(self, mesh_data, m, mat, col, wear=0.0):
        """Add faces from a bpy mesh (e.g. a text or a primitive) transformed by m."""
        mirrored = m.to_3x3().determinant() < 0
        for p in mesh_data.polygons:
            vs = [m @ mesh_data.vertices[i].co for i in p.vertices]
            self.face(vs[::-1] if mirrored else vs, mat, col, wear)

    def to_object(self, name, collection=None, materials=None, smooth_angle=None):
        me = bpy.data.meshes.new(name)
        me.from_pydata([tuple(v) for v in self.verts], [], self.faces)
        me.polygons.foreach_set('material_index', self.mats)
        col = me.color_attributes.new('Col', 'FLOAT_COLOR', 'CORNER')
        wear = me.attributes.new('Wear', 'FLOAT', 'CORNER')
        uv = me.uv_layers.new(name='UVMap')
        li = 0
        for fi, poly in enumerate(me.polygons):
            for k, loop in enumerate(poly.loop_indices):
                c = self.cols[fi][k]
                col.data[loop].color = (c[0], c[1], c[2], self.wears[fi])  # alpha carries wear for the web
                wear.data[loop].value = self.wears[fi]
                if self.uvs[fi]:
                    uv.data[loop].uv = self.uvs[fi][k]
                else:  # world-ish box projection so tiling textures line up
                    v = me.vertices[poly.vertices[k]].co
                    n = poly.normal
                    if abs(n.z) > 0.7:
                        uv.data[loop].uv = (v.x, v.y)
                    elif abs(n.x) > abs(n.y):
                        uv.data[loop].uv = (v.y, v.z)
                    else:
                        uv.data[loop].uv = (v.x, v.z)
        me.validate()
        me.update()
        ob = bpy.data.objects.new(name, me)
        for s in self.slots:
            ob.data.materials.append(materials(s) if materials else None)
        (collection or bpy.context.scene.collection).objects.link(ob)
        if smooth_angle is not None:
            for p in me.polygons:
                p.use_smooth = False
        return ob


# ---------------------------------------------------------------- frames and polygons
def frame(origin, along, out):
    """Matrix for a local frame on a wall: x along the wall, y out of the wall, z up. On a counter-clockwise ring this is a
    mirror (left-handed): MeshBuilder.box, parts.cyl and merge_mesh turn their faces round under it, and a face laid by
    hand in it reads x then z to face out of the wall."""
    a = Vector((along[0], along[1], 0)).normalized()
    o = Vector((out[0], out[1], 0)).normalized()
    m = Matrix((
        (a.x, o.x, 0, origin[0]),
        (a.y, o.y, 0, origin[1]),
        (0, 0, 1, origin[2] if len(origin) > 2 else 0),
        (0, 0, 0, 1)))
    return m


def at(m, x, y, z, rz=0.0, rx=0.0, ry=0.0):
    """m followed by a local translation and rotation."""
    return m @ Matrix.Translation((x, y, z)) @ Matrix.Rotation(rz, 4, 'Z') @ Matrix.Rotation(rx, 4, 'X') @ Matrix.Rotation(ry, 4, 'Y')


def centroid(poly):
    return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))


def signed_area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2


def ccw(poly):
    return poly if signed_area(poly) > 0 else list(reversed(poly))


def edge_out(poly, i):
    """Outward unit normal of edge i of a counter-clockwise polygon."""
    a, b = poly[i], poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    l = math.hypot(dx, dy) or 1
    return (dy / l, -dx / l)


def offset(poly, d):
    """Offset a convex counter-clockwise polygon outward by d (mitred)."""
    n = len(poly)
    out = []
    for i in range(n):
        a = edge_out(poly, (i - 1) % n)
        b = edge_out(poly, i)
        k = 1 + a[0] * b[0] + a[1] * b[1]
        if k < 1e-6:   # the outline doubles back here (a spike in the data): move straight out along one edge
            out.append((poly[i][0] + b[0] * d, poly[i][1] + b[1] * d))
            continue
        out.append((poly[i][0] + (a[0] + b[0]) / k * d, poly[i][1] + (a[1] + b[1]) / k * d))
    return out


def chamfer(poly, c):
    """Cut each corner by c (a quad becomes an octagon)."""
    out, n = [], len(poly)
    for i, p in enumerate(poly):
        a, b = poly[i - 1], poly[(i + 1) % n]
        la, lb = math.dist(a, p), math.dist(b, p)
        ca, cb = min(c, la * 0.3), min(c, lb * 0.3)
        out.append((p[0] + (a[0] - p[0]) / la * ca, p[1] + (a[1] - p[1]) / la * ca))
        out.append((p[0] + (b[0] - p[0]) / lb * cb, p[1] + (b[1] - p[1]) / lb * cb))
    return out


def prism(mb, mat, poly, z0, z1, col_bot, col_top=None, wear=0.0, cap=False, cap_mat=None, cap_col=None, inward=False):
    """Vertical walls around a counter-clockwise polygon (outward faces unless inward)."""
    col_top = col_top or col_bot
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        pts = [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)]
        cols = [col_bot, col_bot, col_top, col_top]
        if inward:
            pts.reverse()
            cols.reverse()
        mb.face(pts, mat, cols, wear)
    if cap:
        mb.face([(p[0], p[1], z1) for p in poly], cap_mat or mat, cap_col or col_top, wear)
