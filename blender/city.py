"""Build the whole city (everything in web/gidi-data.js) as streamable tiles.

blender -b --factory-startup -P blender/city.py -- --tiles 6,12;7,12 [--size 400] [--out web/city] [--detail web|full]

Each tile is a square of `size` metres. Everything whose centre falls in it is built there (lines
are cut at the edges): buildings by kind through the registry, named civic plots, point places
(the nearest plot turns into the police station, the fuel station...), parcels, roads in their
conditions with drains, kerbs, poles and wires, litter, structures, expressways and bridges, the
rail line, canals, boardwalks, estate walls and gates, water, ground, trees. Everything in a tile
is merged into one mesh and exported as tiles/<tx>_<ty>.glb (Draco), positioned relative to the
tile's corner. Colour is in COLOR_0 (alpha = wear); material names say which shader to use.
blender/city_run.py runs many tiles in parallel and writes the manifest.
"""
import json
import math
import os
import sys
import time
import zlib  # stable choices: Python's hash() changes every run, and the city must come out the same every time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

from gidi_kit import detail  # noqa: E402
from gidi_kit import parts as kit_parts  # noqa: E402   (compound walls from the data)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = {}
for i, a in enumerate(args):
    if a.startswith('--'):
        opt[a] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('--') else True
SIZE = float(opt.get('--size', 400))
OUT = opt.get('--out', os.path.join(ROOT, 'web', 'city'))
detail.LEVEL = opt.get('--detail', 'web')
TILES = [tuple(int(v) for v in t.split(',')) for t in str(opt.get('--tiles', '') if opt.get('--tiles') is not True else '').split(';') if t]
TERRAIN = bool(opt.get('--terrain'))   # stand the tile on web/terrain.json (the Google rebuild pilot); off: flat, as before

import scene  # noqa: E402
from gidi_kit import archetypes, rules, boats, landmarks, monuments, parcels, people, places, registry, roadside, street, structures, vehicles  # noqa: E402
from gidi_kit.core import MeshBuilder, Rng, ccw, edge_out, hex_rgb, offset  # noqa: E402
from gidi_kit.materials import master  # noqa: E402
from gidi_kit.rules import CHARACTER, FLOOD, STREET, UNFINISHED_SHARE  # noqa: E402

GD = open(os.path.join(ROOT, 'web', 'gidi-data.js')).read()
GD = json.loads(GD[GD.index('{'):GD.rindex('}') + 1])
P = lambda p: (p[0], -p[1])  # data (y south) -> Blender (y north)
WIDTH = {'main': 14.0, 'street': 7.0, 'lane': 3.5, 'path': 2.5}
ART_W = {'exp': 30.0, 'art': 18.0, 'bridge': 22.0}


# ---------------------------------------------------------------- geometry helpers
def dist_seg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy or 1
    t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2))
    return math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy))


def dist_line(p, pts):
    return min(dist_seg(p, pts[i], pts[i + 1]) for i in range(len(pts) - 1)) if len(pts) > 1 else 1e9


def in_poly(p, poly):
    ins, j = False, len(poly) - 1
    for i in range(len(poly)):
        xi, yi, xj, yj = poly[i][0], poly[i][1], poly[j][0], poly[j][1]
        if (yi > p[1]) != (yj > p[1]) and p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi:
            ins = not ins
        j = i
    return ins


def cent(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def clip_line_rect(pts, x0, y0, x1, y1, piece=6.0):
    """Cut a polyline to the parts inside a rectangle (by small pieces, so tiles meet)."""
    out, cur = [], []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        n = max(1, int(math.dist(a, b) / piece))
        for k in range(n):
            p0 = (a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
            p1 = (a[0] + (b[0] - a[0]) * (k + 1) / n, a[1] + (b[1] - a[1]) * (k + 1) / n)
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            if x0 <= mx < x1 and y0 <= my < y1:
                if not cur:
                    cur = [p0]
                cur.append(p1)
            elif cur:
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    return out


def clip_poly_rect(poly, x0, y0, x1, y1):
    """Sutherland-Hodgman clip of a polygon to a rectangle."""
    def clip(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            if inside(b):
                if not inside(a):
                    out.append(inter(a, b))
                out.append(b)
            elif inside(a):
                out.append(inter(a, b))
        return out
    pts = list(poly)
    for edge in ('x0', 'x1', 'y0', 'y1'):
        if not pts:
            break
        if edge == 'x0':
            pts = clip(pts, lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0])))
        elif edge == 'x1':
            pts = clip(pts, lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0])))
        elif edge == 'y0':
            pts = clip(pts, lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0))
        else:
            pts = clip(pts, lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1))
    return pts


def triangulate_fill(mb, poly, z, mat, col, wear):
    """Fill a possibly concave polygon (ear clipping)."""
    pts = ccw([tuple(p) for p in poly])
    idx = list(range(len(pts)))
    guard = 0
    while len(idx) > 3 and guard < 5000:
        guard += 1
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = pts[i0], pts[i1], pts[i2]
            if (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) <= 0:
                continue
            if any(in_poly(pts[j], [a, b, c]) for j in idx if j not in (i0, i1, i2)):
                continue
            mb.face([(a[0], a[1], z), (b[0], b[1], z), (c[0], c[1], z)], mat, col, wear)
            idx.pop(k)
            break
        else:
            break
    if len(idx) == 3:
        a, b, c = (pts[i] for i in idx)
        mb.face([(a[0], a[1], z), (b[0], b[1], z), (c[0], c[1], z)], mat, col, wear)


# ---------------------------------------------------------------- the city's layers in Blender space
DISTRICTS = {d['id']: [P(p) for p in d['poly'][0]] for d in GD['districts']}


def district_at(p):
    for k, poly in DISTRICTS.items():
        if in_poly(p, poly):
            return k
    return None


# Districts built to the agreed cross-sections (docs/REBUILD-PLAN.md): the data holds their street furniture and their road
# widths (GD["cross_sections"]); here the kit draws what the data says instead of placing its own poles and lamps.
XS = GD.get('cross_sections') or {}
if XS:   # the agreed arterial and expressway carriageways (bridges keep their deck width)
    ART_W.update({k: XS[k]['carriageway'] for k in ('art', 'exp') if k in XS})
LAGOS_D = {district_at(P((f['x'], f['y']))) for f in GD.get('furniture', [])} - {None}
def road_w(kind, d):
    return XS[kind]['carriageway'] if d in LAGOS_D and kind in XS else WIDTH[kind]


ROADS = []  # {k, pts, w, d, id}
for kind, src in (('street', 'streets'), ('lane', 'lanes'), ('path', 'paths')):
    for d, lines in GD.get(src, {}).items():
        for i, ln in enumerate(lines):
            ROADS.append(dict(k=kind, pts=[P(p) for p in ln], w=road_w(kind, d), d=d, id=f'{d}/{kind}/{i}'))
_seen_mains = set()
_main_n = {}
for i, m in enumerate(GD.get('mains', [])):
    sig = tuple(tuple(round(c, 1) for c in p) for p in m['pts'])
    if sig in _seen_mains or sig[::-1] in _seen_mains:
        continue  # an edge road both its districts list: build it once (else double kerbs, poles and lamps)
    _seen_mains.add(sig)
    _mk = _main_n.get(m.get('d'), 0); _main_n[m.get('d')] = _mk + 1   # named within its district, as scripts/isms.py names their gutters
    ROADS.append(dict(k='main', pts=[P(p) for p in m['pts']], w=road_w('main', m.get('d')), d=m.get('d'), id=f"{m.get('d')}/main/{_mk}", name=m.get('name')))
THINGS = {}   # (tile x, tile y): the things standing there (scripts/things.py), on the map's axes
for _t in GD.get('things', []):
    THINGS.setdefault((int(_t['x'] // SIZE), int(_t['y'] // SIZE)), []).append(_t)
HOUSE_D = GD.get('houses') or {}   # each house's roof, unfinished top, tank, dish, tyres (scripts/houses.py)
CLOSES = {}   # road id: [(x, y, radius)] the turning spaces at the ends of the closes (scripts/roadends.py)
for e_ in GD.get('road_ends', []):
    if e_['t'] == 'close':
        CLOSES.setdefault(e_['road'], []).append((e_['x'], e_['y'], e_['r']))
BUILDINGS = []
for d, lst in GD['buildings'].items():
    st = GD['storeys'].get(d, [])
    sty = (GD.get('styles') or {}).get(d) or []
    for i, b in enumerate(lst):
        poly = ccw([P(p) for p in b[1:]])
        BUILDINGS.append(dict(d=d, i=i, kind=b[0], poly=poly, c=cent(poly), storeys=st[i] if i < len(st) else 1, style=sty[i] if i < len(sty) else None))
WALLED = {d: set(v) for d, v in (GD.get('walled') or {}).items()}
FRONTS = GD.get('fronts') or {}   # house fronts from the data (scripts/fronts.py): the street side, shop, canopy, balconies   # houses with a compound wall in the data: no shop front
PARCELS = [dict(d=d, kind=p['kind'], pts=[P(q) for q in p['pts'][:-1]]) for d, lst in GD['parcels'].items() for p in lst]
CIVIC = [dict(type=s['type'], name=s['name'], d=s['d'], poly=ccw([P(p) for p in s['pts'][:-1]])) for s in GD.get('safe_ground', [])]
for c in CIVIC:
    c['c'] = cent(c['poly'])
# named places with a model of their own (landmarks.BY_NAME) stand on the nearest civic plot of
# their type within 300 m; the ones with no such plot take over a building plot (poi_overrides)
NAMED_PARCEL_POIS = [(p['name'], P((p['x'], p['y']))) for p in GD['pois'] if p['name'] in landmarks.PARCEL_BY_NAME]
NAMED_PLOTS = {}  # civic plot name -> landmark name
for _poi in GD['pois']:
    if _poi['name'] in landmarks.BY_NAME:
        _q = P((_poi['x'], _poi['y']))
        _best = min((c for c in CIVIC if c['type'] == _poi['type'] and c['name'] not in NAMED_PLOTS), key=lambda c: math.dist(c['c'], _q), default=None)
        if _best and math.dist(_best['c'], _q) < 300:
            NAMED_PLOTS[_best['name']] = _poi['name']


def poi_overrides():
    """Point places take over the nearest plain building in their district (cached on disk)."""
    path = os.path.join(OUT, 'poi_overrides.json')
    if os.path.exists(path):
        return {tuple(k.split('|', 1)): v for k, v in json.load(open(path)).items()}
    res, used = {}, set()
    for poi in GD['pois']:
        t = poi['type']
        if poi['name'] in landmarks.BY_NAME and poi['name'] not in NAMED_PLOTS.values():
            t = 'named'
        elif t not in registry.POI_PLACES:
            continue
        p = P((poi['x'], poi['y']))
        best = None
        for b in BUILDINGS:
            if b['d'] != poi['d'] or b['kind'] not in ('front', 'back') or (b['d'], str(b['i'])) in used:
                continue
            dd = math.dist(p, b['c'])
            if dd < 120 and (best is None or dd < best[0]):
                best = (dd, b)
        if best:
            key = (best[1]['d'], str(best[1]['i']))
            used.add(key)
            res[key] = dict(type=t, name=poi['name'])
    os.makedirs(OUT, exist_ok=True)
    json.dump({'|'.join(k): v for k, v in res.items()}, open(path, 'w'))
    return res


def _seg_cross(a, b, c, d):
    """Where segment ab crosses cd, or None."""
    r = (b[0] - a[0], b[1] - a[1])
    q = (d[0] - c[0], d[1] - c[1])
    den = r[0] * q[1] - r[1] * q[0]
    if abs(den) < 1e-9:
        return None
    t = ((c[0] - a[0]) * q[1] - (c[1] - a[1]) * q[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    return (a[0] + t * r[0], a[1] + t * r[1], r, q) if 0 <= t <= 1 and 0 <= u <= 1 else None


def _unit(v):
    L = math.hypot(*v) or 1
    return (v[0] / L, v[1] / L)


def _clear(p, pad=1.5):
    return not any(math.dist(b['c'], p) < 40 and in_poly(p, offset(b['poly'], pad)) for b in BUILDINGS)


CANALS = [[P(p) for p in c['pts']] for c in GD.get('canals', [])]
CANAL_WIDTH = [c.get('width', structures.CANAL_W) for c in GD.get('canals', [])]

# ---------------------------------------------------------------- deck heights
# The map holds every deck's height (docs/road-heights.md): z per point, metres above the water. The
# kit still builds on flat ground, so each deck is drawn at its height above the ground under it
# (web/terrain.json; water is 0). That keeps the headroom, and the ramps land on the road. When the
# kit takes the terrain, draw the map's z as it is.
_T = json.load(open(os.path.join(ROOT, 'web', 'terrain.json')))
_TZ, _TC, _TW, _TH = _T['z'], _T['cell_m'], _T['w'], _T['h']
_WET = [(min(q[0] for q in w), min(q[1] for q in w), max(q[0] for q in w), max(q[1] for q in w), w) for w in list(GD['water']) + list(GD['ocean'])]


def wet_at(x, y):
    """Map point x, y (y south) on water: the lagoon, creeks, harbour or the ocean."""
    return any(a <= x <= c and b <= y <= d and in_poly((x, y), w) for a, b, c, d, w in _WET)


def ground_at(x, y):
    """The ground's height at map point x, y (y south): bilinear on the terrain grid, 0 on water."""
    if wet_at(x, y):
        return 0.0
    fx, fy = x / _TC - 0.5, y / _TC - 0.5
    j0, i0 = math.floor(fx), math.floor(fy)
    tx, ty = fx - j0, fy - i0
    at = lambda i, j: _TZ[min(max(i, 0), _TH - 1) * _TW + min(max(j, 0), _TW - 1)] / 10.0
    return (at(i0, j0) * (1 - tx) * (1 - ty) + at(i0, j0 + 1) * tx * (1 - ty) + at(i0 + 1, j0) * (1 - tx) * ty + at(i0 + 1, j0 + 1) * tx * ty)


def rel_z(d):
    """A deck's heights above the ground under it, one per point (None when the map has none)."""
    if not d.get('z'):
        return None
    return [max(0.05, z - ground_at(p[0], p[1])) for p, z in zip(d['pts'], d['z'])]


CULVERTS_DONE = []  # crossings already given parapets (the map can hold overlapping culverts at a junction)
BRIDGE_Z = {a['name']: rel_z(a) for a in GD.get('arterials', []) if a['cls'] == 'bridge'}
BUILT = set(GD['buildings'])  # districts with buildings (the others aren't built yet)

# Act 1 (docs/KIT-GAPS.md, "New in the v2 layout"): Ladi Lane's lock-ups stand open along its aisle (the chase line);
# a buka takes the name of the food place on it; overhead signs find the road they span.
LADI = [((q[0], q[1] - 78), (q[0], q[1] + 78)) for q in (P((p_['x'], p_['y'])) for p_ in GD['pois'] if p_['name'] == 'Ladi Lane')]
FOOD_POIS = [(p_['name'], P((p_['x'], p_['y']))) for p_ in GD['pois'] if p_['type'] == 'food']
ARTS = [dict(k='art', cls=a_['cls'], pts=[P(p) for p in a_['pts']], w=ART_W.get(a_['cls'], 18.0), name=a_['name'], d=None) for a_ in GD.get('arterials', [])]


def ladi_lockup(b):
    """A small stall on Ladi Lane's aisle: the edge facing the aisle, or None."""
    if b['kind'] != 'stalls' or len(b['poly']) != 4:
        return None
    area = abs(sum(b['poly'][i][0] * b['poly'][(i + 1) % 4][1] - b['poly'][(i + 1) % 4][0] * b['poly'][i][1] for i in range(4))) / 2
    for a_, b_ in LADI:
        if area < 25 and dist_seg(b['c'], a_, b_) < 14:
            mids = [((b['poly'][i][0] + b['poly'][(i + 1) % 4][0]) / 2, (b['poly'][i][1] + b['poly'][(i + 1) % 4][1]) / 2) for i in range(4)]
            return min(range(4), key=lambda i: dist_seg(mids[i], a_, b_))
    return None


def span_road(q):
    """The road an overhead sign spans: (road, the nearest point on its middle, its direction there)."""
    best = None
    for r in list(ROADS) + ARTS:
        if r['k'] not in ('main', 'art'):
            continue
        for a_, b_ in zip(r['pts'], r['pts'][1:]):
            d = dist_seg(q, a_, b_)
            if best is None or d < best[0]:
                best = (d, r, a_, b_)
    if not best or best[0] > 40:
        return None
    _, r, a_, b_ = best
    u = _unit((b_[0] - a_[0], b_[1] - a_[1]))
    t = (q[0] - a_[0]) * u[0] + (q[1] - a_[1]) * u[1]
    return r, (a_[0] + u[0] * t, a_[1] + u[1] * t), u


def monument_sites():
    """Every monument from the data (scripts/things.py places the junction statues, welcome arches, point landmarks, murals
    and billboards by rule; the rest are placed by hand): the kit draws them where the data says. Also written to
    web/city/monuments.json."""
    sites = []
    for m_ in GD.get('monuments') or []:
        x_, y_ = P((m_['x'], m_['y']))
        k = m_['model']
        sites.append(dict(kind=k, x=x_, y=y_, ang=-math.radians(m_.get('ang', 0)), d=m_['d'],
                          r=3.4 if k == 'lighthouse' else 1.0 if k == 'led_board' else 0.6 if k == 'billboard' else 0 if k == 'mural_wall' else 2.5,
                          **({'span': m_.get('span', 16), 'name': m_.get('name') or next(dd['name'] for dd in GD['districts'] if dd['id'] == m_['d'])} if k == 'arch' else {})))
    path = os.path.join(ROOT, 'web', 'city', 'monuments.json')
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + f'.{os.getpid()}'
        json.dump([dict(s_, y=-s_['y']) for s_ in sites], open(tmp, 'w'))  # in the data's frame (y south)
        os.replace(tmp, path)
    except OSError:
        pass
    return sites


MONUMENTS = monument_sites()




DNAME = {d['id']: d['name'] for d in GD['districts']}
SPEED = {'main': 50, 'art': 60, 'exp': 80, 'bridge': 80}


def _ahead_name(road, end_pt, here):
    """What a road leads to from a junction: the district at that end of it, or its own name when
    that end is still in the district you're in."""
    d = district_at(end_pt)
    if d and d != here and d in BUILT:
        return DNAME[d]
    return road.get('name') or (DNAME.get(d) if d else None) or 'City Centre'


def roadside_sites():
    """The road signs from the data (scripts/things.py: direction signs before the big junctions, speed limits after them,
    no-parking discs by the markets, gantries over the expressways and bridges), in the kit's frame."""
    KIND = {'direction sign': 'dir', 'speed sign': 'speed', 'no parking sign': 'noparking', 'gantry': 'gantry'}
    by_name = {a_['name']: a_ for a_ in ARTS}
    out = []
    for f in GD.get('furniture', []):
        k = KIND.get(f['kind'])
        if not k:
            continue
        x, y = P((f['x'], f['y']))
        a = -math.radians(f['ang'])
        s_ = dict(kind=k, x=x, y=y, face=a)
        if k == 'dir':
            s_['lines'] = [tuple(ln) for ln in f['lines']]
        elif k == 'speed':
            s_['v'] = f['v']
        elif k == 'gantry':
            r = by_name.get(f['road'])
            s_.update(ang=a, span=f['span'], panels=[[tuple(ln) for ln in p_] for p_ in f['panels']],
                      z0=structures.profile(r['pts'], BRIDGE_Z.get(r['name']), structures.BRIDGE_H['cable' if 'Cable' in r['name'] else 'long'], structures.RAMP['bridge'])(f['s'])
                      if r and r['cls'] == 'bridge' else 0.0)
        out.append(s_)
    return out


ROADSIDE = roadside_sites()


def build_roadside(mb, s_):
    rng = Rng('roadside', s_['kind'], round(s_['x']), round(s_['y']))
    if s_['kind'] == 'dir':
        roadside.direction_sign(mb, s_['x'], s_['y'], s_['face'], s_['lines'], rng)
    elif s_['kind'] == 'speed':
        roadside.disc_sign(mb, s_['x'], s_['y'], s_['face'], 'speed', rng, s_['v'])
    elif s_['kind'] == 'noparking':
        roadside.disc_sign(mb, s_['x'], s_['y'], s_['face'], 'noparking', rng)
    elif s_['kind'] == 'gantry':
        roadside.gantry(mb, s_['x'], s_['y'], s_['ang'], s_['span'], s_['panels'], rng, z0=s_.get('z0', 0.0))


LAMPS = []  # this tile's working lamp heads (Blender frame), saved in the tile's JSON for the 3D view's night lights
DEAD_LAMPS = {'elite': 0.05, 'civic': 0.15, 'old_island': 0.3, 'dense': 0.45, 'sprawl': 0.4, 'port': 0.4, 'waterfront': 0.6}


def blocks_faces(poly):
    from gidi_kit.blocks import faces
    return faces(poly)


def build_monument(mb, s_):
    M = Matrix.Translation((s_['x'], s_['y'], 0)) @ Matrix.Rotation(s_['ang'], 4, 'Z')
    rng = Rng('monument', s_['kind'], round(s_['x']), round(s_['y']))
    k = s_['kind']
    if k.startswith('statue'):
        monuments.statue(mb, M, rng, k.split(':')[1] if ':' in k else None)
    elif k == 'arch':
        monuments.arch(mb, M, rng, s_['span'], s_['name'], CHARACTER.get(s_['d'], 'dense'))
    else:
        monuments.BUILDERS[k](mb, M, rng)


# ---------------------------------------------------------------- one tile
def build_tile(tx, ty, overrides):
    x0, y0 = tx * SIZE, -(ty + 1) * SIZE  # tile ty counts southward in the data, northward is -y here
    x1, y1 = x0 + SIZE, y0 + SIZE
    inside = lambda p: x0 <= p[0] < x1 and y0 <= p[1] < y1
    things_here = lambda kind=None: [t for i in (-1, 0, 1) for j in (-1, 0, 1) for t in THINGS.get((tx + i, ty + j), ())
                                     if inside(P((t['x'], t['y']))) and (t['k'] == kind if kind else t['k'] != 'rail stall')]
    near = lambda p, m: x0 - m <= p[0] < x1 + m and y0 - m <= p[1] < y1 + m
    sc = scene.reset()
    col = bpy.data.collections.new(f'tile_{tx}_{ty}')
    sc.collection.children.link(col)
    built = {}
    roads_near = [r for r in ROADS if any(near(p, 60) for p in r['pts']) or any(dist_seg(((x0 + x1) / 2, (y0 + y1) / 2), r['pts'][i], r['pts'][i + 1]) < SIZE for i in range(len(r['pts']) - 1))]
    blds_here = [b for b in BUILDINGS if inside(b['c'])]
    polys_near = [b['poly'] for b in BUILDINGS if near(b['c'], 40)]
    in_building = lambda p, pad=0.3: any(in_poly(p, offset(q, pad)) for q in polys_near if math.dist(cent(q), p) < 40)
    civic_here = [c for c in CIVIC if inside(c['c'])]
    SERVICE = []  # (vehicle kind, plot attributes): fire engines, ambulances, church buses to park out front

    # ground: district soil, bush outside districts; water and ocean on top
    g = MeshBuilder()
    dc = district_at(((x0 + x1) / 2, (y0 + y1) / 2))
    ch = CHARACTER.get(dc, 'sprawl') if dc else None
    soil = hex_rgb('#d8c9a3' if ch in ('old_island', 'waterfront', 'elite') else ('#b5714a' if ch else '#7a8a45'))
    if TERRAIN:   # a 10 m grid, so the ground can take the terrain's shape (drape() lifts every point)
        st_ = 10.0
        for gx in range(int((x1 - x0) // st_)):
            for gy in range(int((y1 - y0) // st_)):
                a_, b_ = x0 + gx * st_, y0 + gy * st_
                g.face([(a_, b_, 0), (a_ + st_, b_, 0), (a_ + st_, b_ + st_, 0), (a_, b_ + st_, 0)], 'ground', soil, 0.5)
    else:
        g.face([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], 'ground', soil, 0.5)
    for wpoly in list(GD['water']) + list(GD['ocean']):
        cp = clip_poly_rect([P(p) for p in wpoly], x0, y0, x1, y1)
        if len(cp) >= 3:
            triangulate_fill(g, cp, 0.02, 'water', hex_rgb('#2f4a50'), 0)

    # buildings
    for b in blds_here:
        if any(in_poly(b['c'], c['poly']) for c in civic_here):
            continue
        a = attributes(b, roads_near, polys_near)
        rng = Rng(b['d'], b['i'])
        ov = overrides.get((b['d'], str(b['i'])))
        fn = registry.builder(b['kind'])
        lf = ladi_lockup(b) if LADI else None
        if lf is not None:
            fn, a['facing'] = archetypes.lockup_open, lf
            built['lock-up'] = built.get('lock-up', 0) + 1
        if b['kind'] == 'buka':
            nm = min(FOOD_POIS, key=lambda np_: math.dist(np_[1], b['c']), default=None)
            if nm and math.dist(nm[1], b['c']) < 30:
                a['label'] = nm[0]
        if ov:
            fn = landmarks.BY_NAME[ov['name']] if ov['type'] == 'named' else registry.POI_PLACES[ov['type']]
            a['label'] = ov['name']
        elif b.get('style') and b['kind'] in ('front', 'back'):
            fn = places.mansion
        if fn is None:
            fn, a = archetypes.house, dict(a, kind='back')
            built['unknown:' + b['kind']] = built.get('unknown:' + b['kind'], 0) + 1
        n0 = len(col.objects)
        try:
            fn(a, rng, col)
            if TERRAIN:   # the whole building stands level on the ground under its middle (a plinth takes up the slope)
                gz = ground_at(b['c'][0], -b['c'][1])
                for o_ in col.objects[n0:]:
                    o_['lift'] = gz
            if ov and ov['type'] in ('fire', 'hospital', 'clinic'):
                pass   # its service vehicles are things in the data (scripts/houses.py)
        except Exception as e:  # a builder that breaks on odd data must not stop the city
            built['error:' + b['kind']] = built.get('error:' + b['kind'], 0) + 1
            print('ERROR', b['kind'], b['d'], b['i'], repr(e))
        built[b['kind']] = built.get(b['kind'], 0) + 1
    for c in civic_here:
        fn = registry.CIVIC_PLOTS.get(c['type'])
        if c['name'] in NAMED_PLOTS:  # a named landmark stands on this plot
            fn = landmarks.BY_NAME[NAMED_PLOTS[c['name']]]
        if fn and len(c['poly']) == 4:
            a = attributes(dict(i=0, d=c['d'], kind=c['type'], poly=c['poly'], c=c['c'], storeys=2), roads_near, polys_near)
            a['label'] = NAMED_PLOTS.get(c['name'], c['name'])
            if c['type'] in ('hospital', 'clinic'):
                pass   # its service vehicles are things in the data (scripts/houses.py)
            elif c['type'] == 'church' and Rng('molue', c['name']).chance(0.25):
                pass   # the church's own old bus: a thing in the data (scripts/houses.py)
            try:
                fn(a, Rng(c['d'], 'civic', c['name']), col)
            except Exception as e:
                print('ERROR civic', c['type'], c['name'], repr(e))
            built['civic:' + c['type']] = built.get('civic:' + c['type'], 0) + 1

    # parcels (built where their centre is)
    pm = MeshBuilder()
    for pc in PARCELS:
        if inside(cent(pc['pts'])):
            named = next((n for n, q in NAMED_PARCEL_POIS if in_poly(q, pc['pts']) or dist_line(q, pc['pts'] + pc['pts'][:1]) < 20), None)
            if named:
                landmarks.PARCEL_BY_NAME[named](pm, pc['pts'], Rng(pc['d'], 'parcel', named), CHARACTER.get(pc['d'], 'dense'))
                ok = True
            else:
                ok = parcels.build(pm, pc['kind'], pc['pts'], Rng(pc['d'], 'parcel', pc['kind'], round(cent(pc['pts'])[0])), CHARACTER.get(pc['d'], 'dense'))
            built['parcel:' + pc['kind'] + ('' if ok else ':missing')] = built.get('parcel:' + pc['kind'], 0) + 1
    # cemeteries at their points
    for poi in GD['pois']:
        if poi['type'] == 'cemetery' and inside(P((poi['x'], poi['y']))):
            places.cemetery(pm, P((poi['x'], poi['y'])), 30, Rng('cemetery', poi['name']))
            built['cemetery'] = built.get('cemetery', 0) + 1
        if poi['type'] == 'transit' and inside(P((poi['x'], poi['y']))):
            q = P((poi['x'], poi['y']))
            places.bus_shelter(pm, Matrix.Translation((q[0], q[1], 0)), Rng('stop', poi['name']))
    for s_ in ROADSIDE:
        if inside((s_['x'], s_['y'])):
            build_roadside(pm, s_)
            built['roadside:' + s_['kind']] = built.get('roadside:' + s_['kind'], 0) + 1
    for sg in GD.get('signals', []):  # traffic lights, where the 2D map marks a signalled approach: {x, y, ang (deg, the way they face), arm (m)}
        q = P((sg['x'], sg['y']))
        if inside(q):
            roadside.traffic_light(pm, q[0], q[1], -math.radians(sg.get('ang', 0)), Rng('signal', round(q[0]), round(q[1])), arm=sg.get('arm', 0.0))
            built['signal'] = built.get('signal', 0) + 1
    for s_ in MONUMENTS:
        if inside((s_['x'], s_['y'])):
            build_monument(pm, s_)
            built['monument:' + s_['kind']] = built.get('monument:' + s_['kind'], 0) + 1

    # roads and street life
    sm = MeshBuilder()
    poles = []
    # kerbs stop where they would cross another road's surface (side streets running into a main
    # road, the mouths of junctions): a 20 m grid of carriageway segments
    seg_grid = {}
    for r in roads_near:
        if r['k'] == 'path':
            continue
        for a, b in zip(r['pts'], r['pts'][1:]):
            for gx in range(int(min(a[0], b[0]) // 20) - 1, int(max(a[0], b[0]) // 20) + 2):
                for gy in range(int(min(a[1], b[1]) // 20) - 1, int(max(a[1], b[1]) // 20) + 2):
                    seg_grid.setdefault((gx, gy), []).append((a, b, r['w'] / 2 + 0.25, r['id']))
    for r in ARTS:   # the arterials too: a side road's kerb used to run straight across a four-lane road
        if r['cls'] == 'bridge' or not any(near(p, 60) for p in r['pts']) and not any(dist_seg(((x0 + x1) / 2, (y0 + y1) / 2), r['pts'][i], r['pts'][i + 1]) < SIZE for i in range(len(r['pts']) - 1)):
            continue
        for a, b in zip(r['pts'], r['pts'][1:]):
            for gx in range(int(min(a[0], b[0]) // 20) - 1, int(max(a[0], b[0]) // 20) + 2):
                for gy in range(int(min(a[1], b[1]) // 20) - 1, int(max(a[1], b[1]) // 20) + 2):
                    seg_grid.setdefault((gx, gy), []).append((a, b, r['w'] / 2 + 0.25, 'art/' + r['name']))

    def on_other_road(p, rid):
        return any(dist_seg(p, a, b) < hw for a, b, hw, oid in seg_grid.get((int(p[0] // 20), int(p[1] // 20)), ()) if oid != rid)

    for r in roads_near:
        d = r.get('d') or dc
        rch = CHARACTER.get(d, 'dense')
        ST, flood = STREET[rch], FLOOD.get(d, 0.2)
        wealth = {'elite': 0.85, 'civic': 0.55, 'dense': 0.3, 'sprawl': 0.35, 'old_island': 0.3, 'waterfront': 0.1, 'port': 0.3}[rch]
        rr = Rng('road', r['id'])
        cond = street.road_condition(r, rch, wealth, flood, rr)
        for ex, ey, er in CLOSES.get(r['id'], ()):   # a close's turning space (scripts/roadends.py)
            q = P((ex, ey))
            if inside(q):
                street.turning_head(sm, q[0], q[1], er, r['k'], cond, Rng('close', r['id'], round(ex), round(ey)))
        for piece in clip_line_rect(r['pts'], x0, y0, x1, y1):
            rc = dict(r, pts=piece)
            street.road(sm, rc, cond, Rng('road', r['id'], round(piece[0][0]), round(piece[0][1])))
            street.markings(sm, rc, cond, rr)
            if r['k'] == 'main' or (rch in ('elite', 'civic') and r['k'] == 'street'):
                street.kerbs(sm, rc, ST['kerb'] if r['k'] == 'main' else 'white', rr, skip=lambda p, rid=r['id']: on_other_road(p, rid) or in_building(p, 0.1)
                             or any(math.dist(p, P((ex, ey))) < er - 0.3 for ex, ey, er in CLOSES.get(rid, ())))
            # poles, wires and street lights: all in the data now (scripts/furniture.py, the bush too), drawn below
            for i in range(len(piece) - 1):  # litter at the edges
                a, b = piece[i], piece[i + 1]
                L = math.dist(a, b)
                if L < 1e-6:
                    continue
                dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                for _ in range(int(L * ST['litter'] * 0.5)):
                    k, side = rr.between(0, L), rr.pick([-1, 1])
                    o = side * (r['w'] / 2 + rr.between(-0.6, 2.0))
                    p = (a[0] + dx * k - dy * o, a[1] + dy * k + dx * o)
                    street.litter_piece(sm, p[0], p[1], 0.02, rr)
    # street furniture the data places (districts built to the cross-sections; scripts/furniture.py): drawn where it says.
    # f['ang'] is on the map's axes (y south): toward the road, or a traffic light's face out along its arm; Blender's y runs
    # north, so the angle flips sign here.
    for f_ in GD.get('furniture', []):
        q = P((f_['x'], f_['y']))
        if not inside(q):
            continue
        ang = -math.radians(f_['ang'])
        fr = Rng('furniture', f_['kind'], round(q[0]), round(q[1]))
        if f_['kind'] == 'pole':
            pts3, top = street.pole(sm, q[0], q[1], fr, wood=fr.chance(STREET[CHARACTER.get(district_at(q) or dc, 'dense')]['wood_pole']))
            poles.append((q, top))
        elif f_['kind'] == 'street light':
            ch_ = CHARACTER.get(district_at(q) or dc, 'dense')
            LAMPS.extend(roadside.street_light(sm, q[0], q[1], ang, fr, h=9, working=not fr.chance(DEAD_LAMPS.get(ch_, 0.3)), solar=ch_ in ('dense', 'sprawl', 'waterfront') and fr.chance(0.3)))
        elif f_['kind'] == 'transformer':
            street.transformer(sm, q[0], q[1], fr)
        elif f_['kind'] == 'traffic light':
            roadside.traffic_light(pm, q[0], q[1], ang, fr)
        elif f_['kind'] in ('agbero', 'wheelbarrow vendor', 'fruit seller', 'parking boy', 'bread hawker'):   # people placed by hand, facing the road
            getattr(street, f_['kind'].replace(' ', '_'))(pm, Matrix.Translation((q[0], q[1], 0)) @ Matrix.Rotation(ang, 4, 'Z'), fr)
        elif f_['kind'] == 'police kiosk':
            roadside.police_kiosk(pm, Matrix.Translation((q[0], q[1], 0)) @ Matrix.Rotation(ang, 4, 'Z'), fr)
        elif f_['kind'] == 'task force truck':   # parked along the road it's beside
            sr = span_road(q)
            ha = math.atan2(sr[2][1], sr[2][0]) if sr else ang
            vehicles.task_force_truck(pm, Matrix.Translation((q[0], q[1], 0)) @ Matrix.Rotation(ha, 4, 'Z'), fr)
        elif f_['kind'] == 'overhead sign':   # a gantry across the road, facing the traffic toward the road's far end
            sr = span_road(q)
            if sr:
                r_, c_, u_ = sr
                end = r_['pts'][-1]
                panels = [[('up', _ahead_name(r_, end, district_at(c_)))], [('up', r_.get('name') or 'City Centre')]]
                roadside.gantry(sm, c_[0], c_[1], math.atan2(u_[1], u_[0]), r_['w'] + 1.0, panels, fr)
        elif f_['kind'] == 'bus stop':   # the shelter's open side (its local -y) toward the road
            dx, dy = math.cos(ang), math.sin(ang)
            places.bus_shelter(pm, Matrix.Translation((q[0], q[1], 0)) @ Matrix.Rotation(math.atan2(dx, -dy), 4, 'Z'), fr)
        built['furniture:' + f_['kind']] = built.get('furniture:' + f_['kind'], 0) + 1
    rmb = MeshBuilder()   # the rail market's stalls, from the data (scripts/things.py)
    for t in things_here('rail stall'):
        q = P((t['x'], t['y']))
        street.rail_market(rmb, Matrix.Translation((q[0], q[1], 0)) @ Matrix.Rotation(-math.radians(t['a']), 4, 'Z'), Rng('rail market', round(q[0] * 2), round(q[1] * 2)))
        built['rail market'] = built.get('rail market', 0) + 1
    if rmb.faces:
        rmb.to_object('rail market', col, master)   # its own object: the pitches clear as one when a train comes
    for b in blds_here:  # service drops to houses from the nearest pole
        if not poles or b['kind'] not in ('front', 'back'):
            continue
        p, top = min(poles, key=lambda q: math.dist(q[0], b['c']))
        if math.dist(p, b['c']) < 30:
            cn = b['poly'][zlib.crc32(f"{b['d']}/{b['i']}".encode()) % 4]
            street.wire(sm, (top[0], top[1], top[2] - 0.6), (cn[0], cn[1], min(b['storeys'] * 3.1, 6.5) - 0.3), 1.0, t=0.012, n=5)

    # life: a still of the traffic (moving, frozen; parked at the edges), people along the frontages
    # and in the markets, danfos loading in the motor parks, container trucks queued for the port,
    # 911 lorries at the food markets, and the trains on the line. Half as thick in the web build.
    vm, hm = MeshBuilder(), MeshBuilder()
    thin = 0.5 if detail.web() else 1.0
    PARKED = {}   # the parked vehicles the data places in and around this tile (scripts/things.py), on a 10 m grid
    for t in [t for i in (-1, 0, 1) for j in (-1, 0, 1) for t in THINGS.get((tx + i, ty + j), ())]:
        if t['k'] in vehicles.BUILDERS:
            q = P((t['x'], t['y']))
            PARKED.setdefault((int(q[0] // 10), int(q[1] // 10)), []).append(q)
    parked_near = lambda p, m: any(math.dist(p, q) < m for i in (-1, 0, 1) for j in (-1, 0, 1) for q in PARKED.get((int(p[0] // 10) + i, int(p[1] // 10) + j), ()))
    LIFE = GD.get('life') or {}   # what moves, from the data (scripts/things.py): crowds, traffic mix, gaps, wealth; per-road overrides
    WEALTH, CROWD, GAPS = LIFE.get('wealth', {}), LIFE.get('crowd', {}), LIFE.get('gap', {'main': 14, 'street': 30, 'lane': 60})

    def put_vehicle(kind, x, y, ang, cond, rng, rch, wealth, style=None, taxi=None):
        M = Matrix.Translation((x, y, 0)) @ Matrix.Rotation(ang, 4, 'Z')
        fn = vehicles.BUILDERS[kind]
        if kind == 'car':
            fn(vm, M, rng, cond, kind=style or rng.pick({'saloon': 5, 'suv': 3 + 4 * wealth, 'pickup': 1}),
               taxi=bool(taxi) if taxi is not None else (rch == 'old_island' and rng.chance(0.15)))
        elif kind in ('cart', 'wheelbarrow'):
            fn(vm, M, rng)
            people.person(hm, M @ Matrix.Translation((-2.6 if kind == 'cart' else -1.3, 0, 0)), rng, kind='tshirt', ch=rch, pose=True)
        else:
            fn(vm, M, rng, cond)
        if kind == 'okada':
            people.seated_rider(vm, M @ Matrix.Translation((-0.25, 0, 0.92)), rng)

    for r in roads_near:
        if r['k'] not in ('main', 'street', 'lane'):
            continue
        d = r.get('d') or dc
        rch = CHARACTER.get(d, 'dense')
        rk = 'main' if r['k'] == 'main' else 'street'
        RO = LIFE.get('roads', {}).get(r['id'], {})   # this road's own, set on the board
        wealth = RO.get('wealth', WEALTH.get(rch, 0.3))
        mixk = dict(RO.get('mix') or LIFE.get('mix_d', {}).get(f'{d}|{rk}') or LIFE.get('mix', {}).get(f'{rch}|{rk}') or LIFE.get('mix', {}).get(f'dense|{rk}'))
        for piece in clip_line_rect(r['pts'], x0, y0, x1, y1):
            rr = Rng('life', r['id'], round(piece[0][0]), round(piece[0][1]))
            for i in range(len(piece) - 1):
                a, b = piece[i], piece[i + 1]
                Ls = math.dist(a, b)
                if Ls < 1e-6:
                    continue
                dx, dy = (b[0] - a[0]) / Ls, (b[1] - a[1]) / Ls
                ang = math.atan2(dy, dx)
                lanes = [(-r['w'] / 4, 1), (r['w'] / 4, -1)] if r['k'] != 'lane' else [(0, 1)]  # drive on the right
                gap = RO.get('gap', GAPS[r['k']]) / thin
                xs_ = XS.get(r['k'], {})   # people walk on the walkway (scripts/ground.py), never in the gutter or the road
                walk_band = (r['w'] / 2 + xs_.get('gutter', 0) + 0.15, r['w'] / 2 + xs_.get('gutter', 0) + xs_.get('walkway', 0) - 0.15)
                for off, dirn in lanes:
                    k = rr.between(0, gap)
                    while k < Ls:
                        kind = rr.pick(mixk)
                        x, y = a[0] + dx * k - dy * off, a[1] + dy * k + dx * off
                        if inside((x, y)) and not in_building((x, y), 0.5) and not parked_near((x, y), vehicles.LENGTH[kind] / 2 + 2.5):
                            put_vehicle(kind, x, y, ang if dirn > 0 else ang + math.pi, vehicles.condition(wealth, rr, commercial=kind in vehicles.COMMERCIAL), rr, rch, wealth)
                            built['vehicle:' + kind] = built.get('vehicle:' + kind, 0) + 1
                        k += vehicles.LENGTH[kind] + rr.between(gap * 0.4, gap * 1.6)
                # parked at the edge: in the data now (scripts/things.py), drawn with the other things below
                n = int(Ls / 100 * RO.get('crowd', CROWD.get(rch, 15)) * (1.6 if r['k'] == 'main' else 1.0) * thin)
                for _ in range(n):  # people along the frontage
                    k, side = rr.between(0, Ls), rr.pick([-1, 1])
                    o = side * (rr.between(*walk_band) if walk_band[1] > walk_band[0] else rr.between(0.3, r['w'] / 2 - 0.3))   # the walkway (a lane: the lane itself)
                    x, y = a[0] + dx * k - dy * o, a[1] + dy * k + dx * o
                    if inside((x, y)) and not in_building((x, y), 0.2):
                        walk = ang + (0 if rr.chance(0.5) else math.pi) + rr.between(-0.3, 0.3) if rr.chance(0.6) else rr.between(0, math.tau)
                        people.person(hm, Matrix.Translation((x, y, 0.03)) @ Matrix.Rotation(walk, 4, 'Z'), rr, ch=rch)
    # the things the data places (scripts/things.py): parked vehicles, buses and lorries in their parks, people standing in the
    # markets and parks, port machines, boats, canoes, the trains. The web build draws every other parked car and person.
    for t in things_here():
        k = t['k']
        q = P((t['x'], t['y']))
        ang = -math.radians(t['a'])
        tr = Rng('thing', k, round(q[0] * 10), round(q[1] * 10))
        if detail.web() and k in ('person', 'car', 'keke', 'okada') and tr.chance(0.5):
            continue
        rch = CHARACTER.get(t['d'], 'dense')
        if k == 'person':
            people.person(hm, Matrix.Translation((q[0], q[1], 0.05)) @ Matrix.Rotation(ang, 4, 'Z'), tr, ch=rch, kind=t.get('s'))
        elif k in vehicles.BUILDERS:
            if k in ('stacker', 'forklift'):
                vehicles.BUILDERS[k](vm, Matrix.Translation((q[0], q[1], 0)) @ Matrix.Rotation(ang, 4, 'Z'), tr, t.get('c', 'worn'))
            else:
                put_vehicle(k, q[0], q[1], ang, t.get('c', 'worn'), tr, rch, WEALTH.get(rch, 0.3), style=t.get('s'), taxi=t.get('taxi', 0))
            built['vehicle:' + k] = built.get('vehicle:' + k, 0) + 1
        elif k == 'generator':   # beside its house, caged, facing out (scripts/houses.py)
            F = Matrix.Translation((q[0] - math.cos(ang) * 0.9, q[1] - math.sin(ang) * 0.9, 0)) @ Matrix.Rotation(ang - math.pi / 2, 4, 'Z')
            kit_parts.generator(vm, F, 0, dict(col=hex_rgb(tr.pick({'#c62828': 2, '#2e7d32': 2, '#f9a825': 2, '#37474f': 1})), wear=tr.between(0.3, 0.8)))
            built['generator'] = built.get('generator', 0) + 1
        elif k == 'canoe':
            boats.outboard_canoe(vm, Matrix.Translation((q[0], q[1], 0.05)) @ Matrix.Rotation(ang, 4, 'Z'), tr, people=bool(t.get('p')))
            built['boat:canoe'] = built.get('boat:canoe', 0) + 1
        elif k in boats.BUILDERS:
            boats.BUILDERS[k](vm, Matrix.Translation((q[0], q[1], 0.05)) @ Matrix.Rotation(ang, 4, 'Z'), Rng('boat', k, round(q[0])))
            built['boat:' + k] = built.get('boat:' + k, 0) + 1
        elif k.startswith('train:'):
            fn, _ = vehicles.TRAIN[k[6:]]
            M = Matrix.Translation((q[0], q[1], 0)) @ Matrix.Rotation(ang, 4, 'Z')
            trng = Rng('train', t.get('train', ''), round(q[0]))
            fn(vm, M, trng, cab=bool(t.get('cab'))) if k == 'train:commuter' else fn(vm, M, trng)
            built[k] = built.get(k, 0) + 1
    # fire engines, ambulances, a church's molue and the police pound: things in the data now (scripts/houses.py)
    # structures, expressways, bridges, rail, canals, boardwalks, walls, gates
    tm = MeshBuilder()
    for s in GD.get('structures', []):
        pts = [P(p) for p in s['pts']]
        zs = rel_z(s)
        rng = Rng('struct', s['name'], round(pts[0][0]))
        if s['kind'] in ('flyover', 'ramp', 'approach'):  # the whole line, so the ramps sit at the real ends; this tile's slabs only
            if not any(inside(p) for p in pts):
                continue
            (structures.approach if s['kind'] == 'approach' else structures.flyover)(tm, pts, s['width'], zs or structures.profile(pts, None, 6.5 * s.get('layer', 1)), rng, lamps=LAMPS, keep=inside)
        else:
            if not inside(cent(pts)):
                continue
            zm = sum(zs) / len(zs) if zs else None
            k = s['kind']
            if k == 'skywalk':
                structures.skywalk(tm, pts, s['width'], rng, **({'z': zm} if zm else {}))
            elif k == 'footbridge':
                near_canal = min(range(len(CANALS)), key=lambda i: min(dist_seg(cent(pts), a, b) for a, b in zip(CANALS[i], CANALS[i][1:]))) if CANALS else None   # not "near": that's the tile's own test, used below
                structures.footbridge(tm, structures.snap_footbridge(pts, CANALS, width=CANAL_WIDTH[near_canal] if near_canal is not None else None), s['width'], rng, **({'z': zm} if zm else {}))
            elif k == 'jetty':
                structures.jetty(tm, pts, s['width'], rng, **({'z': zm} if zm else {}))
            elif k == 'culvert':
                cross = None
                for ci, cn in enumerate(CANALS):
                    for a, b in zip(pts, pts[1:]):
                        for c0, c1 in zip(cn, cn[1:]):
                            x = _seg_cross(a, b, c0, c1)
                            if x and not any(math.dist(x[:2], q) < 6 for q in CULVERTS_DONE):
                                cross = (x[0], x[1], x[3], CANAL_WIDTH[ci])
                                break
                        if cross:
                            break
                    if cross:
                        break
                if cross:
                    CULVERTS_DONE.append(cross[:2])
                structures.culvert(tm, pts, s['width'], rng, cross=cross)
            else:
                continue
        built['structure:' + s['kind']] = built.get('structure:' + s['kind'], 0) + 1
    for a_ in GD.get('arterials', []):
        pts = [P(p) for p in a_['pts']]
        w = ART_W.get(a_['cls'], 18)
        rng = Rng('arterial', a_['name'])
        if a_['cls'] == 'bridge':  # the whole line, so the ramps sit at the real ends; this tile's slabs only
            (structures.cable_bridge if 'Cable' in a_['name'] else structures.long_bridge)(tm, pts, w, rng, keep=inside, lamps=LAMPS, zs=BRIDGE_Z.get(a_['name']))
            continue
        for piece in clip_line_rect(pts, x0, y0, x1, y1):
            structures.expressway(tm, piece, w, rng, median=a_['cls'] == 'exp' or rng.chance(0.5), lamps=LAMPS, keep=inside,
                                  gap=lambda p, rid='art/' + a_['name']: on_other_road(p, rid))   # the median opens where a road crosses
    for qy in GD.get('quays', []):  # sea walls; the land behind is made up to their top, so here the top is the ground
        for piece in clip_line_rect([P(p) for p in qy['pts']], x0, y0, x1, y1):
            structures.quay(tm, piece, 0.3, Rng('quay', round(qy['pts'][0][0])))
    for piece in clip_line_rect([P(p) for p in GD['rail']['pts']], x0, y0, x1, y1):
        structures.rail(tm, piece, Rng('rail'))
    for c in GD.get('canals', []):
        for piece in clip_line_rect([P(p) for p in c['pts']], x0, y0, x1, y1):
            structures.canal(tm, piece, c.get('width', structures.CANAL_W), Rng('canal', c['d']))
    for bw in GD.get('boardwalks', []):
        for piece in clip_line_rect([P(p) for p in bw], x0, y0, x1, y1):
            structures.boardwalk(tm, piece, Rng('boardwalk', round(bw[0][0])))
    for d, segs in (GD.get('walls') or {}).items():
        for w in segs:
            pts = [P(p) for p in w]
            if inside(cent(pts)):
                structures.estate_wall(tm, pts, Rng('wall', d))
    for d, ws in (GD.get('compound_walls') or {}).items():   # compound walls from the data (scripts/compounds.py), dressed by character
        rch = CHARACTER.get(d, 'dense')
        gts = [P(q) for q in (GD.get('compound_gates') or {}).get(d, [])]
        for w in ws:
            pts = [P(p) for p in w]
            if not inside(cent(pts)):
                continue
            wr = Rng('compound', d, round(w[0][0]), round(w[0][1]))
            kit_parts.compound_wall(sm, pts, rules.compound_spec(rch, wr), wr, closed=False, gates=[g for g in gts if near(g, 4)])
            built['compound wall'] = built.get('compound wall', 0) + 1
    for gt in GD.get('gates', []):
        pts = [P(p) for p in gt['pts']]
        if inside(cent(pts)):
            structures.estate_gate(tm, pts, gt.get('main'), Rng('gate'))

    # trees from the data (scripts/trees.py): the board shows and moves them
    for d_, L_ in (GD.get('trees') or {}).items():
        for t_ in L_:
            p = P((t_[0], t_[1]))
            if x0 <= p[0] < x1 and y0 <= p[1] < y1:
                parcels.tree(pm, p[0], p[1], Rng('tree', round(t_[0]), round(t_[1])), kind=t_[2])

    for mb_, name in ((g, 'ground'), (pm, 'parcels'), (sm, 'street'), (tm, 'structures'), (vm, 'traffic'), (hm, 'people')):
        if mb_.faces:
            mb_.to_object(name, col, master)
    return col, built, (x0, y0)


def data_front(b, poly):
    """The data's front for a house (scripts/fronts.py), with its sides renumbered for the kit's ring (the kit turns rings
    counter-clockwise in Blender space, which can reverse them)."""
    f = (FRONTS.get(b['d']) or {}).get(str(b['i']))
    if not f:
        return {}
    pts = [P(p) for p in GD['buildings'][b['d']][b['i']][1:]]
    n = len(pts)
    key = lambda p, q: frozenset(((round(p[0], 2), round(p[1], 2)), (round(q[0], 2), round(q[1], 2))))
    kit = {key(poly[k], poly[(k + 1) % n]): k for k in range(n)}
    side = lambda j: kit.get(key(pts[j % n], pts[(j + 1) % n]))
    e = side(f['e'])
    out = dict(front=dict(shop=bool(f['shop']), aw=f['aw'], bal={side(j) for j in f['bal']} - {None}))
    if e is not None:
        out['facing'] = e
    return out


def attributes(b, roads, polys):
    poly = b['poly']
    best, facing = 1e9, 0
    near_roads = [r for r in roads if r['k'] in ('main', 'street') and dist_line(b['c'], r['pts']) < 60]
    for e in range(len(poly)):
        a, q = poly[e], poly[(e + 1) % len(poly)]
        mid = ((a[0] + q[0]) / 2, (a[1] + q[1]) / 2)
        dd = min((dist_line(mid, r['pts']) - r['w'] / 2 for r in near_roads), default=99)
        if dd < best:
            best, facing = dd, e
    near_main = min((dist_line(b['c'], r['pts']) - 7 for r in roads if r['k'] == 'main'), default=999)
    rng = Rng(b['d'], 'unfinished', b['i'])
    others = [p for p in polys if p is not poly and math.dist(cent(p), b['c']) < 30]
    return {**dict(kind=b['kind'], storeys=b['storeys'], district=b['d'], poly=poly, facing=facing, frontage=best, near_main=near_main,
                name=f"{b['d']}_{b['kind']}_{b['i']}", style=b.get('style'),
                unfinished=bool(HOUSE_D.get(b['d'], {}).get(str(b['i']), {}).get('unf')) if HOUSE_D and b['kind'] in ('front', 'back', 'shed') else b['storeys'] >= 2 and rng.chance(UNFINISHED_SHARE.get(b['d'], 0.01)),
                house=HOUSE_D.get(b['d'], {}).get(str(b['i'])) if b['kind'] in ('front', 'back', 'shed') else None,   # roof, tank, dish, tyres from the data (scripts/houses.py)
                walled=b['i'] in WALLED.get(b['d'], ())), **data_front(b, poly)}   # walls and fronts come from the data now (the data's facing wins)


def drape(obs):
    """--terrain: stand everything on the ground. A building's pieces (tagged 'lift') rise together, level; everything else
    (ground, roads, kerbs, furniture, decks drawn at their height above the ground) follows the ground point by point."""
    import numpy as np
    Z = np.array(_TZ, float).reshape(_TH, _TW) / 10.0
    for o in obs:
        if 'lift' in o.keys():
            o.data.transform(Matrix.Translation((0, 0, o['lift'])))
            continue
        n = len(o.data.vertices)
        if not n:
            continue
        co = np.empty(n * 3)
        o.data.vertices.foreach_get('co', co)
        co = co.reshape(n, 3)
        mw = np.array(o.matrix_world)
        wx = co[:, 0] * mw[0, 0] + co[:, 1] * mw[0, 1] + co[:, 2] * mw[0, 2] + mw[0, 3]
        wy = co[:, 0] * mw[1, 0] + co[:, 1] * mw[1, 1] + co[:, 2] * mw[1, 2] + mw[1, 3]
        fx, fy = wx / _TC - 0.5, -wy / _TC - 0.5   # map y runs south
        j0, i0 = np.floor(fx).astype(int), np.floor(fy).astype(int)
        tx, ty = fx - j0, fy - i0
        at = lambda i, j: Z[np.clip(i, 0, _TH - 1), np.clip(j, 0, _TW - 1)]
        g = at(i0, j0) * (1 - tx) * (1 - ty) + at(i0, j0 + 1) * tx * (1 - ty) + at(i0 + 1, j0) * (1 - tx) * ty + at(i0 + 1, j0 + 1) * tx * ty
        # on the water (and its edge) the ground stays at the water's level: the water is flat, so nothing pokes through it
        mx, my = wx, -wy
        for a_, b_, c_, d_, w in _WET:
            box_ = (mx >= a_ - 1) & (mx <= c_ + 1) & (my >= b_ - 1) & (my <= d_ + 1)
            if not box_.any():
                continue
            px, py = mx[box_], my[box_]
            inside = np.zeros(px.shape, bool)
            q = w if w[0] != w[-1] else w[:-1]
            for (x1_, y1_), (x2_, y2_) in zip(q, q[1:] + q[:1]):   # ray casting
                c = ((y1_ > py) != (y2_ > py)) & (px < (x2_ - x1_) * (py - y1_) / ((y2_ - y1_) or 1e-9) + x1_)
                inside ^= c
            gi = g[box_]
            gi[inside] = 0.0
            g[box_] = gi
        co[:, 2] += g   # local z: the tile's objects carry no rotation or scale
        o.data.vertices.foreach_set('co', co.ravel())
        o.data.update()


CHUNK_LOOPS = 6_000_000


def export(col, origin, path):
    """Join the tile into a few objects, move them to the tile's corner, export Draco GLB."""
    obs = [o for o in col.all_objects if o.type == 'MESH']
    if not obs:
        return 0
    if TERRAIN:
        drape(obs)
    if os.environ.get('GIDI_FACES'):  # where the faces go, by object kind
        tally = {}
        for o in obs:
            k = o.name.split('_')[1] if o.name.count('_') >= 2 else o.name
            tally[k] = tally.get(k, 0) + len(o.data.polygons)
        print('FACES', sorted(tally.items(), key=lambda kv: -kv[1])[:12])
    # join into parts of at most CHUNK_LOOPS corners each: the browser's Draco decoder aborts on a mesh
    # of more than ~8M vertices (one material of a full tile could reach 14M as a single mesh)
    parts, cur, n = [], [], 0
    for o in obs:
        k = len(o.data.loops)
        if cur and n + k > CHUNK_LOOPS:
            parts.append(cur)
            cur, n = [], 0
        cur.append(o)
        n += k
    parts.append(cur)
    nt, joined = 0, []
    for i, part in enumerate(parts):
        for o in list(bpy.context.view_layer.objects):
            if o is not None:  # the temporary lettering objects can leave dead entries behind
                o.select_set(False)
        for o in part:
            o.select_set(True)
        bpy.context.view_layer.objects.active = part[0]
        if len(part) > 1:
            bpy.ops.object.join()
        ob = bpy.context.view_layer.objects.active
        ob.data.transform(Matrix.Translation((-origin[0], -origin[1], 0)))
        ob.name = os.path.basename(path)[:-4] + (f'_{i}' if i else '')
        nt += len(ob.data.polygons)
        joined.append(ob)
    for o in joined:
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_vertex_color='ACTIVE', export_all_vertex_colors=False,
                              export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6, export_draco_position_quantization=16,
                              export_draco_normal_quantization=8, export_draco_color_quantization=8, export_draco_texcoord_quantization=10,
                              export_materials='EXPORT', export_image_format='NONE', export_yup=True)
    return nt


if __name__ == '__main__':
    os.makedirs(os.path.join(OUT, 'tiles'), exist_ok=True)
    ov = {(d, i): r for d, R in (GD.get('roles') or {}).items() for i, r in R.items()} if GD.get('roles') is not None else poi_overrides()   # which building each place takes over (scripts/houses.py)
    for tx, ty in TILES:
        t0 = time.time()
        detail.SIGNS.clear()
        LAMPS.clear()
        col, built, origin = build_tile(tx, ty, ov)
        lamps = [[round(x - origin[0], 2), round(z + (ground_at(x, -y) if TERRAIN else 0), 2), round(-(y - origin[1]), 2)] for x, y, z in LAMPS]  # GLB frame, like signs
        signs = []
        for sg in detail.SIGNS:  # tile-relative, in the GLB's y-up frame: (x, z, -y)
            m = sg['m']
            px, py, pz = m[0][3] - origin[0], m[1][3] - origin[1], m[2][3] + (ground_at(m[0][3], -m[1][3]) if TERRAIN else 0)
            along = (m[0][0], m[1][0])
            out = (m[0][1], m[1][1])
            signs.append(dict(p=[round(px, 3), round(pz, 3), round(-py, 3)], a=round(math.atan2(along[1], along[0]), 4), o=[round(out[0], 3), round(out[1], 3)],
                              t=sg['text'], s=round(sg['size'], 3), fg=[round(c, 3) for c in sg['col']], bg=[round(c, 3) for c in sg['bg']] if sg['bg'] else None,
                              w=round(sg['w'], 2) if sg['w'] else None, h=round(sg['h'], 2) if sg['h'] else None, hand=sg['hand']))
        path = os.path.join(OUT, 'tiles', f'{tx}_{ty}.glb')
        nt = export(col, origin, path)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        info = dict(tx=tx, ty=ty, faces=nt, bytes=size, seconds=round(time.time() - t0, 1), built=built, signs=len(signs))
        json.dump(dict(info, origin=[origin[0], origin[1]], signs=signs, lamps=lamps), open(os.path.join(OUT, 'tiles', f'{tx}_{ty}.json'), 'w'), separators=(',', ':'))
        print('TILE', json.dumps(info))
