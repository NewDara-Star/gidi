"""Roadside furniture that makes a road read and lets you find your way: street lights (single and
double arm, solar ones with their panel; a share dead, as in Lagos), green direction signs and
overhead gantries with Gidi's own place names, speed limits and no-parking discs.
Research: research-street 2.3-2.6, research-roads 4 (Lagos signage: green boards with white
lettering, white border, arrows; galvanised poles; the chequered black-and-white kerb and median).

Frames: M is a ground frame. For boards, y points out of the face towards whoever reads it and x
runs along the text (parts.text's convention)."""
import math

from mathutils import Matrix, Vector

from . import parts
from .core import hex_rgb, shade
from .kinds import T

GALV = hex_rgb('#8a8f92')
GREEN = hex_rgb('#0f6b3a')
WHITE = hex_rgb('#f4f4f0')
LAMP = hex_rgb('#fff1d0')     # warm-white LED / high-pressure sodium is oranger
SODIUM = hex_rgb('#ffb060')


def street_light(mb, x, y, ang, rng, arms=1, h=None, working=True, solar=False, z0=0.0, banners=False):
    """A galvanised tapered pole with one arm (reaching over the road along ang) or two (a median
    pole, arms both ways). Returns the lamp heads' positions [(x, y, z), ...] for the 3D view's night lights."""
    h = h or rng.between(8.5, 10.5)
    M = Matrix.Translation((x, y, z0)) @ Matrix.Rotation(ang, 4, 'Z')
    parts.cyl(mb, 'steel', M, 0.11, h, GALV, rng.between(0.3, 0.7), seg=8, r2=0.06)
    mb.box('concrete', T(M, 0, 0, 0.15), hex_rgb('#a8a59c'), 0.6, size=(0.5, 0.5, 0.3))
    heads = []
    col = LAMP if rng.chance(0.7) else SODIUM
    for s in ((1,) if arms == 1 else (1, -1)):
        reach = 1.8
        a = T(M, 0, 0, h - 0.4).translation
        b = T(M, s * reach * 0.6, 0, h + 0.15).translation
        c = T(M, s * reach, 0, h + 0.2).translation
        parts.bar(mb, 'steel', a, b, 0.07, GALV, 0.5)
        parts.bar(mb, 'steel', b, c, 0.06, GALV, 0.5)
        hm = T(M, s * (reach + 0.35), 0, h + 0.12)
        mb.box('steel', hm, hex_rgb('#5a5e60'), 0.5, size=(0.75, 0.32, 0.14))
        mb.box('lamp' if working else 'plastic', hm @ Matrix.Translation((0, 0, -0.075)), col if working else hex_rgb('#9a9a92'), 0, size=(0.62, 0.24, 0.02))
        if working:
            heads.append(tuple(hm.translation))
    if banners:  # a pair of street-light ads hanging off the pole, one each way (research-street 2.6)
        for s_ in ((1, -1) if arms == 2 else (1,)):
            lamp_banner(mb, M, s_, h * 0.55, rng)
    if solar:  # the panel on top and a battery box halfway up
        mb.box('glass', T(M, 0, 0, h + 0.5) @ Matrix.Rotation(0.35, 4, 'X'), hex_rgb('#1e2a44'), 0.2, size=(1.0, 0.7, 0.04))
        mb.box('steel', T(M, 0.12, 0, h * 0.45), hex_rgb('#d8d8d2'), 0.4, size=(0.18, 0.3, 0.45))
    return heads


def _arrow(mb, Fv, u, z, size, direction, col=WHITE):
    """A white arrow on a board. Fv is the board's viewer frame (x to the reader's right, y into
    the board); direction 'left', 'right' or 'up' (ahead)."""
    rot = {'right': 0.0, 'up': math.pi / 2, 'left': math.pi}[direction]
    A = Fv @ Matrix.Translation((u, -0.05, z)) @ Matrix.Rotation(math.pi / 2, 4, 'X') @ Matrix.Rotation(rot, 4, 'Z')
    s = size
    shaft = [(-0.5 * s, -0.09 * s), (0.1 * s, -0.09 * s), (0.1 * s, 0.09 * s), (-0.5 * s, 0.09 * s)]
    head = [(0.1 * s, -0.3 * s), (0.5 * s, 0.0), (0.1 * s, 0.3 * s)]
    for poly in (shaft, head):
        mb.face([A @ Vector((p[0], p[1], 0)) for p in poly], 'paint', col, 0.1)


def board(mb, F, w, h, lines, rng, col=GREEN):
    """A sign board centred on F (y out of the face, towards the reader) with a white border and
    lines of (arrow, text) from the top, printed on the front; the back is bare galvanised steel."""
    mb.box('steel', F, hex_rgb('#5a5e60'), 0.4, size=(w, 0.05, h))
    mb.box('paint', F @ Matrix.Translation((0, 0.03, 0)), WHITE, 0.15, size=(w - 0.04, 0.01, h - 0.04))
    mb.box('paint', F @ Matrix.Translation((0, 0.035, 0)), col, rng.between(0.1, 0.4), size=(w - 0.2, 0.01, h - 0.2))
    Fv = F @ Matrix.Rotation(math.pi, 4, 'Z')  # the reader's frame: x to their right
    n = max(1, len(lines))
    step = (h - 0.4) / n
    for i, (arrow, txt) in enumerate(lines):
        z = h / 2 - 0.2 - step * (i + 0.5)
        size = min(0.42, step * 0.62)
        if arrow == 'right':  # arrow at the right edge, text left of it
            _arrow(mb, Fv, w / 2 - 0.25 - size / 2, z, size, 'right')
            parts.text(mb, 'paint', Fv @ Matrix.Translation((-size * 0.6, -0.045, z)), txt, size, WHITE, depth=0.01, max_w=w - size - 0.7)
        elif arrow in ('left', 'up'):
            _arrow(mb, Fv, -w / 2 + 0.25 + size / 2, z, size, arrow)
            parts.text(mb, 'paint', Fv @ Matrix.Translation((size * 0.6, -0.045, z)), txt, size, WHITE, depth=0.01, max_w=w - size - 0.7)
        else:
            parts.text(mb, 'paint', Fv @ Matrix.Translation((0, -0.045, z)), txt, size, WHITE, depth=0.01, max_w=w - 0.5)


def direction_sign(mb, x, y, face, lines, rng):
    """A roadside direction sign on two galvanised posts, its face turned to face (radians, the
    direction its readers come from)."""
    w = max(2.4, min(4.2, 0.9 + 0.26 * max(len(t) for _, t in lines)))
    h = 0.55 + 0.55 * len(lines)
    F0 = Matrix.Translation((x, y, 0)) @ Matrix.Rotation(face - math.pi / 2, 4, 'Z')
    for s in (-1, 1):
        parts.cyl(mb, 'steel', F0 @ Matrix.Translation((s * w * 0.32, -0.06, 0)), 0.05, 2.2 + h, GALV, 0.5, seg=8)
    board(mb, F0 @ Matrix.Translation((0, 0, 2.2 + h / 2)), w, h, lines, rng)


def gantry(mb, x, y, ang, span, panels, rng, z0=0.0):
    """An overhead sign gantry across a carriageway: two posts, a box truss, a panel per lane group,
    readable by traffic travelling along ang (the direction they drive)."""
    M = Matrix.Translation((x, y, z0)) @ Matrix.Rotation(ang, 4, 'Z')  # x along the road (z0: on a bridge deck)
    clear = 6.0
    for s in (-1, 1):
        parts.cyl(mb, 'steel', M @ Matrix.Translation((0, s * span / 2, 0)), 0.22, clear + 1.6, GALV, 0.5, seg=10)
        mb.box('concrete', M @ Matrix.Translation((0, s * span / 2, 0.3)), hex_rgb('#a8a59c'), 0.6, size=(0.9, 0.9, 0.6))
    for dz in (0.0, 1.2):  # the truss chords and a zigzag
        for dx in (-0.3, 0.3):
            parts.bar(mb, 'steel', T(M, dx, -span / 2, clear + dz).translation, T(M, dx, span / 2, clear + dz).translation, 0.07, GALV, 0.5)
    k = 0
    while k < span:
        y0 = -span / 2 + k
        parts.bar(mb, 'steel', T(M, 0.3, y0, clear).translation, T(M, 0.3, min(span / 2, y0 + 1.2), clear + 1.2).translation, 0.04, GALV, 0.5)
        k += 1.2
    n = len(panels)
    pw = min(5.5, span / max(1, n) - 0.4)
    for i, lines in enumerate(panels):
        yc = -span / 2 + span * (i + 0.5) / n
        # the face looks back down the road (towards -x) at the drivers coming
        F = M @ Matrix.Translation((-0.4, yc, clear + 0.6)) @ Matrix.Rotation(math.pi / 2, 4, 'Z')
        board(mb, F, pw, 0.5 + 0.6 * len(lines), lines, rng)


def disc_sign(mb, x, y, face, kind, rng, value=None):
    """A round regulatory sign on a post: 'speed' (red ring, the limit in black) or 'noparking'
    (blue disc, red ring and slash)."""
    F = Matrix.Translation((x, y, 0)) @ Matrix.Rotation(face - math.pi / 2, 4, 'Z')
    parts.cyl(mb, 'steel', F, 0.04, 2.5, GALV, 0.5, seg=8)
    D = F @ Matrix.Translation((0, 0.05, 2.6)) @ Matrix.Rotation(-math.pi / 2, 4, 'X')  # disc facing +y
    red = hex_rgb('#c62828')
    parts.cyl(mb, 'paint', D, 0.4, 0.02, red, 0.2, seg=20)
    inner = WHITE if kind == 'speed' else hex_rgb('#1e4fa0')
    parts.cyl(mb, 'paint', D @ Matrix.Translation((0, 0, 0.02)), 0.31, 0.01, inner, 0.2, seg=20)
    if kind == 'speed':
        parts.text(mb, 'paint', F @ Matrix.Rotation(math.pi, 4, 'Z') @ Matrix.Translation((0, -0.085, 2.6)), str(value), 0.3, hex_rgb('#111111'), depth=0.01, max_w=0.5)
    else:
        mb.box('paint', D @ Matrix.Translation((0, 0, 0.035)) @ Matrix.Rotation(math.pi / 4, 4, 'Z'), red, 0.2, size=(0.62, 0.08, 0.01))


BANNER_POSTERS = [
    # (background, accent, text colour, the message): invented, no party, face or brand of the real city
    ('#c62828', '#f2c230', '#ffffff', 'VOTE FOR PROGRESS'), ('#1f5fa8', '#ffffff', '#ffffff', 'GIDI CARNIVAL'),
    ('#2e7d4f', '#f2c230', '#ffffff', 'ONE GOOD TERM'), ('#6a1b9a', '#ff7a1a', '#ffffff', 'CONCERT FRIDAY'),
    ('#f2c230', '#1d1d1d', '#1d1d1d', 'BIG SALE NOW'), ('#ffffff', '#c62828', '#1d1d1d', 'NEW CHURCH CRUSADE'),
    ('#1d1d1d', '#f2c230', '#ffffff', 'GIDI FM 101.1'), ('#00897b', '#ffffff', '#ffffff', 'CLEAN GIDI'),
]


def lamp_banner(mb, M, side, z, rng):
    """A vertical banner on two short arms off a lamp post, 1 x 2.6 m: a poster of colour fields,
    a portrait shape and a line of type. M: the pole's base frame, side: which way it hangs."""
    bg, acc, fg, msg = rng.pick(BANNER_POSTERS)
    bg, acc, fg = hex_rgb(bg), hex_rgb(acc), hex_rgb(fg)
    for dz in (1.3, -1.3):  # the two arms, reaching out across the road from the pole
        parts.bar(mb, 'steel', T(M, 0, 0, z + dz).translation, T(M, side * 1.15, 0, z + dz).translation, 0.035, GALV, 0.4)
    F = T(M, side * 0.7, 0, z)  # the banner, facing the traffic both ways along the road (local y)
    mb.box('cloth', F, bg, 0.3, size=(1.0, 0.03, 2.6))
    for fy in (1, -1):
        mb.box('cloth', F @ Matrix.Translation((0, fy * 0.02, -0.75)), acc, 0.3, size=(0.9, 0.01, 0.6))
        parts.cyl(mb, 'cloth', F @ Matrix.Translation((0, fy * 0.022, 0.45)) @ Matrix.Rotation(-fy * math.pi / 2, 4, 'X'), 0.28, 0.01, shade(acc, 0.8), 0.3, seg=12)  # a portrait shape
        Fv = F @ Matrix.Rotation(0 if fy < 0 else math.pi, 4, 'Z')  # the reader's frame on each face
        parts.text(mb, 'paint', Fv @ Matrix.Translation((0, -0.03, -0.1)), msg.replace(' ', '\n', 1), 0.16, fg, depth=0.005, max_w=0.85)


def traffic_light(mb, x, y, face, rng, arm=0.0, z0=0.0):
    """A Lagos traffic light: a grey pole, a black three-lamp head with visors, the red-digit
    countdown box beside it, often a small solar panel on top. arm > 0 hangs the head out over the
    road on a mast arm that long. face: the direction the lights face (towards the traffic coming)."""
    F = Matrix.Translation((x, y, z0)) @ Matrix.Rotation(face - math.pi / 2, 4, 'Z')  # y towards the traffic
    h = 4.2 if not arm else 6.2
    parts.cyl(mb, 'steel', F, 0.1, h, hex_rgb('#8a8f92'), 0.5, seg=10)
    mb.box('concrete', F @ Matrix.Translation((0, 0, 0.15)), hex_rgb('#a8a59c'), 0.6, size=(0.5, 0.5, 0.3))
    H = F @ Matrix.Translation((0, 0, h - 0.6))
    if arm:
        parts.bar(mb, 'steel', (F @ Vector((0, 0, h - 0.3))), (F @ Vector((-arm, 0, h - 0.3))), 0.09, hex_rgb('#8a8f92'), 0.5)
        H = F @ Matrix.Translation((-arm, 0, h - 1.0))
    mb.box('steel', H, hex_rgb('#151515'), 0.4, size=(0.36, 0.3, 1.05))
    lit = rng.randrange(3)  # one lamp on, the others dark
    for k, col in enumerate(('#d02020', '#e0a010', '#20b050')):  # the lamps with visors
        z = 0.33 - k * 0.33
        mb.box('emit' if k == lit else 'plastic', H @ Matrix.Translation((0, 0.16, z)), hex_rgb(col) if k == lit else shade(hex_rgb(col), 0.25), 0, size=(0.22, 0.02, 0.22))
        mb.box('steel', H @ Matrix.Translation((0, 0.24, z + 0.13)), hex_rgb('#151515'), 0.4, size=(0.28, 0.16, 0.03))
    C = H @ Matrix.Translation((0.42, 0, 0.0))  # the countdown timer
    mb.box('steel', C, hex_rgb('#151515'), 0.4, size=(0.46, 0.25, 0.4))
    mb.box('emit', C @ Matrix.Translation((0, 0.13, 0)), hex_rgb('#e02020'), 0, size=(0.34, 0.01, 0.24))
    if rng.chance(0.6):  # the solar panel
        mb.box('glass', F @ Matrix.Translation((0, 0, h + 0.25)) @ Matrix.Rotation(0.4, 4, 'X'), hex_rgb('#1e2a44'), 0.2, size=(0.8, 0.6, 0.04))
