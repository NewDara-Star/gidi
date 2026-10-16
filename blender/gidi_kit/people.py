"""People of Lagos streets, from docs/look/research-street.md section 4 (clothing, skin, density).
Real proportions (1.55-1.85 m, head about 1/7.5 of height), standing or walking, and dressed by
type: ankara two-piece, blouse and wrapper with gele, buba and sokoto with fila, agbada, kaftan,
T-shirt and jeans, school uniform, okada rider's vest, hawker with a head tray, conductor."""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import hex_rgb, shade

SKIN = ['#5a3622', '#6e4329', '#4a2b1b', '#7c5033', '#3d2416', '#8a5a3a']
ANKARA = ['#d7263d', '#1b998b', '#f46036', '#2e294e', '#f2c14e', '#5bc0eb', '#9bc53d', '#e55934', '#8e44ad', '#0b6e4f', '#fa7921', '#c2185b', '#1f5fa8']
PLAIN = ['#f4f1ea', '#1d1d1d', '#2f3d4c', '#7a1f1f', '#3f5a3a', '#c9a27a', '#5a6a7a', '#e8dcc0']
DRESS = {  # shares by character [est, research-street 4.2]
    'dense': {'ankara': 3, 'wrapper': 3, 'buba': 2, 'tshirt': 4, 'kaftan': 1, 'hawker': 1.5, 'school': 0.8, 'agbada': 0.3},
    'old_island': {'ankara': 3, 'wrapper': 4, 'buba': 2, 'tshirt': 3, 'kaftan': 1.5, 'hawker': 2, 'agbada': 0.6, 'school': 0.6},
    'sprawl': {'ankara': 2, 'wrapper': 3, 'buba': 2, 'tshirt': 4, 'kaftan': 2, 'hawker': 1, 'school': 1.2, 'agbada': 0.3},
    'elite': {'tshirt': 4, 'ankara': 2, 'office': 3, 'kaftan': 1, 'agbada': 0.5, 'wrapper': 0.5},
    'civic': {'office': 4, 'tshirt': 3, 'ankara': 2, 'buba': 1, 'kaftan': 1, 'wrapper': 1, 'hawker': 0.8},
    'waterfront': {'tshirt': 4, 'wrapper': 3, 'ankara': 1, 'buba': 1, 'hawker': 1, 'school': 0.6},
    'port': {'tshirt': 5, 'office': 1, 'buba': 2, 'kaftan': 2, 'hawker': 1},
}


def L(M, x, y, z, rz=0.0, rx=0.0, ry=0.0):
    return M @ Matrix.Translation((x, y, z)) @ Matrix.Rotation(rz, 4, 'Z') @ Matrix.Rotation(rx, 4, 'X') @ Matrix.Rotation(ry, 4, 'Y')


def sphere(mb, mat, m, rx, ry, rz, col, seg=10, rings=6, top=1.0):
    """An ellipsoid (top < 1 gives a cap, e.g. hair)."""
    prev = None
    for k in range(rings + 1):
        t = -math.pi / 2 + math.pi * k / rings
        if t > -math.pi / 2 + math.pi * top + 1e-6:
            break
        ring = [m @ Vector((math.cos(a) * math.cos(t) * rx, math.sin(a) * math.cos(t) * ry, math.sin(t) * rz)) for a in (i / seg * math.tau for i in range(seg))]
        if prev:
            for i in range(seg):
                j = (i + 1) % seg
                mb.face([prev[i], prev[j], ring[j], ring[i]], mat, col, 0)
        prev = ring


def limb(mb, mat, a, b, r0, r1, col, seg=7):
    """A tapered limb from point a to b with rounded ends."""
    a, b = Vector(a), Vector(b)
    d = b - a
    l = d.length
    z = d / l
    x = z.cross(Vector((0, 0, 1)) if abs(z.z) < 0.95 else Vector((1, 0, 0))).normalized()
    y = z.cross(x)
    m = Matrix(((x.x, y.x, z.x, a.x), (x.y, y.y, z.y, a.y), (x.z, y.z, z.z, a.z), (0, 0, 0, 1)))
    parts.cyl(mb, mat, m, r0, l, col, 0, seg=seg, caps=(False, False), r2=r1)
    sphere(mb, mat, Matrix.Translation(a), r0, r0, r0, col, seg=seg, rings=4)
    sphere(mb, mat, Matrix.Translation(b), r1, r1, r1, col, seg=seg, rings=4)


def person(mb, M, rng, kind=None, ch='dense', pose=None, h=None, phase=None, arms=None, man=None):
    """One person at M (facing +x). kind: a dress type from DRESS, or None to pick by character.
    arms: {side (-1 right, 1 left): (elbow, wrist)} in M's frame at 1.75 m tall (scaled to the height), for a pose
    other than hanging or swinging; man: True or False to fix it. Returns where the hands and head are, so props can go in them."""
    kind = kind or rng.pick(DRESS.get(ch, DRESS['dense']))
    woman = kind in ('wrapper',) or (kind in ('ankara', 'tshirt', 'office', 'hawker', 'school') and rng.chance(0.5))
    if man is not None:   # a part that has to be one or the other (an agbero, a parking boy)
        woman = not man
    h = h or (rng.between(1.55, 1.72) if woman else rng.between(1.65, 1.85))
    if kind == 'school':
        h = rng.between(1.2, 1.55)
    k = h / 1.75
    skin = hex_rgb(rng.pick(SKIN))
    print_col = hex_rgb(rng.pick(ANKARA))
    top = {'ankara': print_col, 'wrapper': hex_rgb(rng.pick(ANKARA)), 'buba': hex_rgb(rng.pick(['#f4f1ea', '#c9a27a', '#1f5fa8', '#2e294e', '#7a1f1f'])),
           'tshirt': hex_rgb(rng.pick(PLAIN + ANKARA[:5])), 'kaftan': hex_rgb(rng.pick(['#f4f1ea', '#e8dcc0', '#9ab0c8', '#3f5a3a', '#1d1d1d'])),
           'agbada': hex_rgb(rng.pick(['#f4f1ea', '#1f3f8a', '#4a2a55', '#c9a13b', '#2e7d4f'])), 'school': hex_rgb('#f4f1ea'), 'office': hex_rgb(rng.pick(['#f4f1ea', '#bcd9e6', '#e8dcc0'])),
           'hawker': hex_rgb(rng.pick(ANKARA))}[kind]
    top_mat = 'ankara' if kind in ('ankara', 'wrapper', 'hawker', 'agbada') and not (kind == 'agbada' and rng.chance(0.5)) else 'cloth'
    bottom = {'ankara': print_col, 'buba': top, 'tshirt': hex_rgb(rng.pick(['#2f3d4c', '#1f3f8a', '#1d1d1d', '#6d5d44'])), 'school': hex_rgb(rng.pick(['#1f3f8a', '#6d5d44', '#2e7d4f'])),
              'office': hex_rgb(rng.pick(['#1d1d1d', '#2f3d4c'])), 'kaftan': top, 'agbada': top, 'wrapper': hex_rgb(rng.pick(ANKARA)), 'hawker': hex_rgb(rng.pick(ANKARA))}[kind]
    walk = pose if pose is not None else rng.chance(0.6)
    sw = (0.32 if phase is not None else rng.between(0.25, 0.4)) if walk else 0.03
    ph = phase if phase is not None else rng.pick([1, -1])
    hip = 0.95 * k
    # legs (hidden by long dresses and robes, but feet show)
    long_dress = kind in ('wrapper', 'kaftan', 'agbada') or (woman and kind in ('ankara', 'hawker') and rng.chance(0.6))
    for s in (-1, 1):
        a = ph * s * sw
        foot = Vector((math.sin(a) * hip * 0.95, s * 0.09 * k, 0.07))
        limb(mb, 'cloth' if not long_dress else 'skin', M @ Vector((0, s * 0.09 * k, hip)), M @ foot, 0.075 * k, 0.05 * k, bottom if not long_dress else skin)
        sphere(mb, 'rubber', M @ Matrix.Translation((foot.x + 0.05, foot.y, 0.04)), 0.12 * k, 0.05 * k, 0.045, hex_rgb(rng.pick(['#1d1d1d', '#5a3a28', '#e8e2d6'])), seg=8, rings=4)
    if long_dress:  # wrapper/kaftan/agbada skirt: a flared tapered tube
        flare = 0.24 if kind == 'agbada' else 0.2
        parts.cyl(mb, top_mat if kind != 'wrapper' else 'ankara', M @ Matrix.Translation((0, 0, 0.1 * k)), flare * k, hip + 0.05 * k - 0.1 * k, bottom if kind == 'wrapper' else top, 0, seg=12, r2=0.17 * k)
    # torso
    torso_m = M @ Matrix.Translation((0, 0, hip))
    parts.cyl(mb, top_mat, torso_m, 0.165 * k, 0.5 * k, top, 0, seg=12, caps=(True, False), r2=0.195 * k)
    sphere(mb, top_mat, torso_m @ Matrix.Translation((0, 0, 0.5 * k)), 0.2 * k, 0.12 * k, 0.07 * k, top, seg=12, rings=4)
    if kind == 'agbada':  # the big flowing robe: wide panels from the shoulders
        for s in (-1, 1):
            mb.face([M @ Vector((0.05, s * 0.18 * k, 1.42 * k)), M @ Vector((0.05, s * 0.55 * k, 1.0 * k)), M @ Vector((0.05, s * 0.5 * k, 0.55 * k)), M @ Vector((0.05, s * 0.15 * k, 0.6 * k))], top_mat, top, 0)
            mb.face([M @ Vector((0.05, s * 0.15 * k, 0.6 * k)), M @ Vector((0.05, s * 0.5 * k, 0.55 * k)), M @ Vector((0.05, s * 0.55 * k, 1.0 * k)), M @ Vector((0.05, s * 0.18 * k, 1.42 * k))], top_mat, top, 0)
    # neck and head
    parts.cyl(mb, 'skin', M @ Matrix.Translation((0, 0, 1.45 * k)), 0.05 * k, 0.13 * k, skin, 0, seg=8)
    head = M @ Matrix.Translation((0.01, 0, 1.63 * k))
    sphere(mb, 'skin', head, 0.1 * k, 0.09 * k, 0.12 * k, skin, seg=12, rings=8)
    sphere(mb, 'skin', head @ Matrix.Translation((0.095 * k, 0, -0.01 * k)), 0.025 * k, 0.022 * k, 0.03 * k, shade(skin, 0.9), seg=6, rings=4)  # nose
    hair = hex_rgb('#141210')
    if kind == 'wrapper' or (woman and rng.chance(0.45)):  # gele head-tie
        g = head @ Matrix.Translation((-0.01 * k, 0, 0.1 * k))
        sphere(mb, 'ankara', g, 0.15 * k, 0.16 * k, 0.09 * k, hex_rgb(rng.pick(ANKARA + ['#c9a13b'])), seg=12, rings=6, top=0.75)
        sphere(mb, 'ankara', g @ Matrix.Translation((-0.06 * k, 0, 0.08 * k)) @ Matrix.Rotation(-0.5, 4, 'Y'), 0.05 * k, 0.17 * k, 0.1 * k, hex_rgb(rng.pick(ANKARA)), seg=10, rings=5)
    elif kind in ('buba', 'agbada') or (not woman and rng.chance(0.15)):  # fila cap, slouched
        parts.cyl(mb, 'cloth', head @ Matrix.Translation((0, 0, 0.06 * k)) @ Matrix.Rotation(0.25, 4, 'Y'), 0.105 * k, 0.11 * k, hex_rgb(rng.pick(['#7a1f1f', '#2e294e', '#c9a13b', '#1d1d1d', '#f4f1ea'])), 0, seg=10, r2=0.08 * k)
    else:
        sphere(mb, 'rubber', head @ Matrix.Translation((-0.005, 0, 0.012)), 0.104 * k, 0.094 * k, 0.122 * k, hair, seg=12, rings=8, top=0.62)
    # arms swing against the legs
    hands = {}
    for s in (-1, 1):
        a = -ph * s * sw * 0.9
        sh = M @ Vector((0, s * 0.2 * k, 1.38 * k))
        el = M @ Vector((math.sin(a) * 0.3 * k, s * 0.23 * k, 1.1 * k))
        wr = M @ Vector((math.sin(a) * 0.3 * k + math.sin(a + 0.25) * 0.26 * k, s * 0.22 * k, 0.86 * k))
        if arms and s in arms:
            el, wr = (M @ (Vector(v) * k) for v in arms[s])
        hands[s] = wr + (wr - el).normalized() * 0.06 * k
        sleeve_long = kind in ('kaftan', 'agbada', 'office', 'buba')
        limb(mb, top_mat, sh, el, 0.055 * k, 0.05 * k, top)
        limb(mb, top_mat if sleeve_long else 'skin', el, wr, 0.048 * k, 0.04 * k, top if sleeve_long else skin)
        sphere(mb, 'skin', Matrix.Translation(wr + Vector((0, 0, -0.06 * k))), 0.035 * k, 0.03 * k, 0.06 * k, skin, seg=6, rings=4)
    if kind == 'hawker':  # a tray or basin on the head, with goods
        t = head @ Matrix.Translation((0, 0, 0.16 * k))
        parts.cyl(mb, 'steel', t, 0.32, 0.08, hex_rgb(rng.pick(['#c9ced2', '#2f6fae', '#c62828'])), 0.3, seg=16, r2=0.36)
        for _ in range(rng.randrange(5, 12)):
            sphere(mb, 'plastic', t @ Matrix.Translation((rng.between(-0.22, 0.22), rng.between(-0.22, 0.22), 0.12)), 0.06, 0.06, 0.06, hex_rgb(rng.pick(['#ff7043', '#fdd835', '#7cb342', '#ffffff', '#e8f0f4', '#c62828'])), seg=6, rings=4)
    if kind == 'school':  # a satchel
        mb.box('cloth', torso_m @ Matrix.Translation((-0.2 * k, 0, 0.25 * k)), hex_rgb(rng.pick(['#c62828', '#1f5fa8', '#3a3a3a'])), 0, size=(0.12, 0.28 * k, 0.32 * k))
    return dict(hands=hands, head=head, k=k, torso=torso_m, top=top)


def seated_rider(mb, M, rng, vest=None, helmet=True):
    """A rider sitting astride an okada (M at the seat, facing +x)."""
    skin = hex_rgb(rng.pick(SKIN))
    top = hex_rgb(vest or rng.pick(['#fdd835', '#ff6f00', '#1565c0', '#2e7d32']))
    pants = hex_rgb(rng.pick(['#2f3d4c', '#1d1d1d', '#6d5d44']))
    parts.cyl(mb, 'cloth', L(M, -0.05, 0, 0.0, ry=0.25), 0.17, 0.52, top, 0, seg=10, r2=0.19)
    for s in (-1, 1):
        limb(mb, 'cloth', M @ Vector((0, s * 0.11, 0.02)), M @ Vector((0.42, s * 0.16, 0.05)), 0.075, 0.06, pants)
        limb(mb, 'cloth', M @ Vector((0.42, s * 0.16, 0.05)), M @ Vector((0.45, s * 0.2, -0.45)), 0.06, 0.05, pants)
        limb(mb, 'cloth', M @ Vector((0.08, s * 0.2, 0.45)), M @ Vector((0.5, s * 0.3, 0.25)), 0.05, 0.045, top)
    head = L(M, 0.15, 0, 0.7)
    sphere(mb, 'skin', head, 0.1, 0.09, 0.12, skin, seg=10, rings=7)
    if helmet:
        sphere(mb, 'plastic', head @ Matrix.Translation((-0.01, 0, 0.02)), 0.14, 0.13, 0.14, hex_rgb(rng.pick(['#1b1b1b', '#c62828', '#fdd835', '#f4f1ea'])), seg=12, rings=8, top=0.62)
