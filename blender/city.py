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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

from gidi_kit import detail  # noqa: E402

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

import scene  # noqa: E402
from gidi_kit import archetypes, landmarks, monuments, parcels, people, places, registry, roadside, street, structures, vehicles  # noqa: E402
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


ROADS = []  # {k, pts, w, d, id}
for kind, src in (('street', 'streets'), ('lane', 'lanes'), ('path', 'paths')):
    for d, lines in GD.get(src, {}).items():
        for i, ln in enumerate(lines):
            ROADS.append(dict(k=kind, pts=[P(p) for p in ln], w=WIDTH[kind], d=d, id=f'{d}/{kind}/{i}'))
_seen_mains = set()
for i, m in enumerate(GD.get('mains', [])):
    sig = tuple(tuple(round(c, 1) for c in p) for p in m['pts'])
    if sig in _seen_mains or sig[::-1] in _seen_mains:
        continue  # an edge road both its districts list: build it once (else double kerbs, poles and lamps)
    _seen_mains.add(sig)
    ROADS.append(dict(k='main', pts=[P(p) for p in m['pts']], w=WIDTH['main'], d=m.get('d'), id=f'main/{i}', name=m.get('name')))
BUILDINGS = []
for d, lst in GD['buildings'].items():
    st = GD['storeys'].get(d, [])
    sty = (GD.get('styles') or {}).get(d) or []
    for i, b in enumerate(lst):
        poly = ccw([P(p) for p in b[1:]])
        BUILDINGS.append(dict(d=d, i=i, kind=b[0], poly=poly, c=cent(poly), storeys=st[i] if i < len(st) else 1, style=sty[i] if i < len(sty) else None))
PARCELS = [dict(d=d, kind=p['kind'], pts=[P(q) for q in p['pts'][:-1]]) for d, lst in GD['parcels'].items() for p in lst]
CIVIC = [dict(type=s['type'], name=s['name'], d=s['d'], poly=ccw([P(p) for p in s['pts'][:-1]])) for s in GD.get('safe_ground', [])]
for c in CIVIC:
    c['c'] = cent(c['poly'])
# named places with a model of their own (landmarks.BY_NAME) stand on the nearest civic plot of
# their type within 300 m; the ones with no such plot take over a building plot (poi_overrides)
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
BUILT = set(GD['buildings'])  # districts with buildings (the others aren't built yet)


def monument_sites():
    """Where the monuments stand (blender/gidi_kit/monuments.py), the same for every tile and detail:
    a corner of the main-road junctions (a statue, clock tower, sculpture or LED screen by the
    district's character, up to four a district), a welcome arch on the main roads entering each
    built district, and the lighthouse on the port mole. Also written to web/city/monuments.json."""
    mains = [r for r in ROADS if r['k'] == 'main']
    sites, per = [], {}
    for i, r1 in enumerate(mains):
        for r2 in mains[i + 1:]:
            for a, b in zip(r1['pts'], r1['pts'][1:]):
                for c, d in zip(r2['pts'], r2['pts'][1:]):
                    x = _seg_cross(a, b, c, d)
                    if not x:
                        continue
                    j = (x[0], x[1])
                    dist = district_at(j)
                    if dist not in BUILT or any(math.dist(j, (s_['x'], s_['y'])) < 60 for s_ in sites):
                        continue
                    rng = Rng('monument', round(j[0]), round(j[1]))
                    u1, u2 = _unit(x[2]), _unit(x[3])
                    corners = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                    rng.shuffle(corners)
                    for sgn1, sgn2 in corners:
                        bis = _unit((u1[0] * sgn1 + u2[0] * sgn2, u1[1] * sgn1 + u2[1] * sgn2))
                        p = (j[0] + bis[0] * 16, j[1] + bis[1] * 16)
                        if _clear(p, 3.0) and per.get(dist, 0) < 4:
                            kinds = monuments.JUNCTION[CHARACTER.get(dist, 'dense')]
                            kind = kinds[per.get(dist, 0) % len(kinds)]
                            per[dist] = per.get(dist, 0) + 1
                            sites.append(dict(kind=kind, x=p[0], y=p[1], ang=math.atan2(-bis[1], -bis[0]), d=dist, r=2.5 if kind != 'led_board' else 1.0))
                            break
    # welcome arches: main roads crossing into a built district, one or two a district
    arches = {}
    for r in mains:
        for a, b in zip(r['pts'], r['pts'][1:]):
            for dname, poly in DISTRICTS.items():
                if dname not in BUILT or arches.get(dname, 0) >= 2:
                    continue
                for c, d in zip(poly, poly[1:] + poly[:1]):
                    x = _seg_cross(a, b, c, d)
                    if not x:
                        continue
                    u = _unit(x[2])
                    # step 30 m inside the district along the road
                    for sgn in (1, -1):
                        p = (x[0] + u[0] * 30 * sgn, x[1] + u[1] * 30 * sgn)
                        if in_poly(p, poly) and all(math.dist(p, (s_['x'], s_['y'])) > 50 for s_ in sites):
                            sites.append(dict(kind='arch', x=p[0], y=p[1], ang=math.atan2(u[1], u[0]), d=dname, span=r['w'] + 2, name=next(dd['name'] for dd in GD['districts'] if dd['id'] == dname)))
                            arches[dname] = arches.get(dname, 0) + 1
                            break
    sites.append(dict(kind='lighthouse', x=3975.0, y=-6330.0, ang=0.0, d='port', r=3.4))
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
    """Direction signs before every main-road and arterial junction (both ways along each road,
    naming where the crossing road goes left and right), overhead gantries on the expressways and
    bridges every 800 m, speed limits after each junction, no-parking discs by the markets."""
    big = [dict(r, cls='main') for r in ROADS if r['k'] == 'main']
    for a in GD.get('arterials', []):
        big.append(dict(k='art', cls=a['cls'], pts=[P(p) for p in a['pts']], w=ART_W.get(a['cls'], 18.0), name=a['name'], d=None))
    sites = []
    # junctions: every crossing of two big roads, and every big road ending on another (a T)
    junctions = []
    for i, r1 in enumerate(big):
        for r2 in big[i + 1:]:
            for a, b in zip(r1['pts'], r1['pts'][1:]):
                for c, d in zip(r2['pts'], r2['pts'][1:]):
                    x = _seg_cross(a, b, c, d)
                    if x:
                        junctions.append(((x[0], x[1]), r1, r2))
    for r in big:
        for e in (r['pts'][0], r['pts'][-1]):
            for o in big:
                if o is r:
                    continue
                best = None
                for a, b in zip(o['pts'], o['pts'][1:]):
                    dx, dy = b[0] - a[0], b[1] - a[1]
                    L2 = dx * dx + dy * dy or 1
                    t = max(0.0, min(1.0, ((e[0] - a[0]) * dx + (e[1] - a[1]) * dy) / L2))
                    q = (a[0] + dx * t, a[1] + dy * t)
                    if math.dist(q, e) < 14 and 0.02 < t < 0.98:
                        best = q
                if best:
                    junctions.append((best, r, o))
    seen = []
    for J, r1, r2 in junctions:
        if any(math.dist(J, q) < 20 for q in seen):
            continue
        seen.append(J)
        here = district_at(J)
        if here not in BUILT:
            continue
        for r, other in ((r1, r2), (r2, r1)):
            # the approach along r from each side: the point 30 m before J
            pts = r['pts']
            for sgn in (1, -1):
                # walk back along r from J by 30 m in direction -sgn
                k = min(range(len(pts) - 1), key=lambda i: dist_seg(J, pts[i], pts[i + 1]))
                a, b = pts[k], pts[k + 1]
                u = _unit((b[0] - a[0], b[1] - a[1]))
                u = (u[0] * sgn, u[1] * sgn)  # travel direction towards J
                p0 = (J[0] - u[0] * 30, J[1] - u[1] * 30)
                if min(dist_seg(p0, pts[i], pts[i + 1]) for i in range(len(pts) - 1)) > 2.0:
                    continue  # the road doesn't come from this side (J is its own end)
                right = (u[1], -u[0])
                off = r['w'] / 2 + 2.2
                sp = (p0[0] + right[0] * off, p0[1] + right[1] * off)
                if not _clear(sp, 1.0) or district_at(sp) not in BUILT:
                    continue
                lines = []
                for end in (other['pts'][0], other['pts'][-1]):
                    side = u[0] * (end[1] - J[1]) - u[1] * (end[0] - J[0])
                    if math.dist(end, J) < 25:
                        continue
                    lines.append(('left' if side > 0 else 'right', _ahead_name(other, end, here)))
                ahead = pts[-1] if sgn > 0 else pts[0]
                if math.dist(ahead, J) > 60:
                    lines.insert(0, ('up', _ahead_name(r, ahead, here)))
                uniq = []
                for ln in lines:
                    if ln[1] not in [x[1] for x in uniq]:
                        uniq.append(ln)
                if uniq:
                    sites.append(dict(kind='dir', x=sp[0], y=sp[1], face=math.atan2(-u[1], -u[0]), lines=uniq[:3]))
                # a speed limit 25 m after the junction, going away from it
                q = (J[0] + u[0] * 25 + right[0] * off, J[1] + u[1] * 25 + right[1] * off)
                if _clear(q, 1.0) and district_at(q) in BUILT:
                    sites.append(dict(kind='speed', x=q[0], y=q[1], face=math.atan2(-u[1], -u[0]), v=SPEED.get(r.get('cls', 'main'), 50)))
    # gantries on the expressways and bridges: every 800 m, one per direction
    for r in big:
        if r.get('cls') not in ('exp', 'bridge'):
            continue
        S = sum(math.dist(r['pts'][i], r['pts'][i + 1]) for i in range(len(r['pts']) - 1))
        s_ = 300.0
        while s_ < S - 200:
            acc = 0.0
            for a, b in zip(r['pts'], r['pts'][1:]):
                L = math.dist(a, b)
                if acc + L >= s_:
                    t = (s_ - acc) / L
                    p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                    u = _unit((b[0] - a[0], b[1] - a[1]))
                    for sgn, end in ((1, r['pts'][-1]), (-1, r['pts'][0])):
                        here = district_at(p)
                        q = (p[0] + u[0] * 30 * sgn, p[1] + u[1] * 30 * sgn)
                        panels = [[('up', _ahead_name(r, end, here))], [('up', r['name'])]]
                        sites.append(dict(kind='gantry', x=q[0], y=q[1], ang=math.atan2(u[1] * sgn, u[0] * sgn), span=r['w'] + 1.0, panels=panels,
                                          z0=structures.deck_height(s_ + 30 * sgn, S, structures.BRIDGE_H['cable' if 'Cable' in r['name'] else 'long'], structures.RAMP['bridge']) if r['cls'] == 'bridge' else 0.0))
                    break
                acc += L
            s_ += 800
    # no parking by the markets, on the nearest big road
    for poi in GD['pois']:
        if poi['type'] != 'market':
            continue
        p = P((poi['x'], poi['y']))
        best = None
        for r in big:
            for a, b in zip(r['pts'], r['pts'][1:]):
                d = dist_seg(p, a, b)
                if d < 120 and (best is None or d < best[0]):
                    best = (d, r, a, b)
        if best:
            _, r, a, b = best
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy or 1
            t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
            u = _unit((dx, dy))
            for sg in (1, -1):
                q = (a[0] + dx * t + u[1] * sg * (r['w'] / 2 + 1.8), a[1] + dy * t - u[0] * sg * (r['w'] / 2 + 1.8))
                if _clear(q, 0.8):
                    sites.append(dict(kind='noparking', x=q[0], y=q[1], face=math.atan2(-u[1] * sg, -u[0] * sg)))
    out = []
    for s_ in sites:  # one sign of a kind at a spot (a junction found from both of its roads)
        if not any(o['kind'] == s_['kind'] and math.dist((o['x'], o['y']), (s_['x'], s_['y'])) < 6 for o in out):
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

    # ground: district soil, bush outside districts; water and ocean on top
    g = MeshBuilder()
    dc = district_at(((x0 + x1) / 2, (y0 + y1) / 2))
    ch = CHARACTER.get(dc, 'sprawl') if dc else None
    soil = hex_rgb('#d8c9a3' if ch in ('old_island', 'waterfront', 'elite') else ('#b5714a' if ch else '#7a8a45'))
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
        if ov:
            fn = landmarks.BY_NAME[ov['name']] if ov['type'] == 'named' else registry.POI_PLACES[ov['type']]
            a['label'] = ov['name']
        elif b.get('style') and b['kind'] in ('front', 'back'):
            fn = places.mansion
        if fn is None:
            fn, a = archetypes.house, dict(a, kind='back')
            built['unknown:' + b['kind']] = built.get('unknown:' + b['kind'], 0) + 1
        try:
            fn(a, rng, col)
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
            try:
                fn(a, Rng(c['d'], 'civic', c['name']), col)
            except Exception as e:
                print('ERROR civic', c['type'], c['name'], repr(e))
            built['civic:' + c['type']] = built.get('civic:' + c['type'], 0) + 1

    # parcels (built where their centre is)
    pm = MeshBuilder()
    for pc in PARCELS:
        if inside(cent(pc['pts'])):
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

    def on_other_road(p, rid):
        return any(dist_seg(p, a, b) < hw for a, b, hw, oid in seg_grid.get((int(p[0] // 20), int(p[1] // 20)), ()) if oid != rid)

    for r in roads_near:
        d = r.get('d') or dc
        rch = CHARACTER.get(d, 'dense')
        ST, flood = STREET[rch], FLOOD.get(d, 0.2)
        wealth = {'elite': 0.85, 'civic': 0.55, 'dense': 0.3, 'sprawl': 0.35, 'old_island': 0.3, 'waterfront': 0.1, 'port': 0.3}[rch]
        rr = Rng('road', r['id'])
        cond = street.road_condition(r, rch, wealth, flood, rr)
        for piece in clip_line_rect(r['pts'], x0, y0, x1, y1):
            rc = dict(r, pts=piece)
            street.road(sm, rc, cond, Rng('road', r['id'], round(piece[0][0]), round(piece[0][1])))
            street.markings(sm, rc, cond, rr)
            if r['k'] == 'main' or (rch in ('elite', 'civic') and r['k'] == 'street'):
                street.kerbs(sm, rc, ST['kerb'] if r['k'] == 'main' else 'white', rr, skip=lambda p, rid=r['id']: on_other_road(p, rid) or in_building(p, 0.1))
            if r['k'] in ('main', 'street') and not (rch == 'elite' and r['k'] != 'main'):
                off = (1 if hash(r['id']) % 2 else -1) * (r['w'] / 2 + 1.6)
                prev = None
                for i in range(len(piece) - 1):
                    a, b = piece[i], piece[i + 1]
                    L = math.dist(a, b)
                    if L < 1e-6:
                        continue
                    dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                    s0 = (sum(math.dist(piece[j], piece[j + 1]) for j in range(i)))
                    k = (35 - s0 % 35) % 35
                    while k < L:
                        p = (a[0] + dx * k - dy * off, a[1] + dy * k + dx * off)
                        if not in_building(p, 0.3):
                            pts3, top = street.pole(sm, p[0], p[1], Rng('pole', round(p[0]), round(p[1])), wood=rr.chance(ST['wood_pole']))
                            if prev:
                                for w0, w1 in zip(prev, pts3):
                                    street.wire(sm, w0, w1, 0.9, n=6)
                            prev = pts3
                            poles.append((p, top))
                        else:
                            prev = None
                        k += 35
            # street lights: main roads everywhere, streets in the elite and civic districts; opposite
            # the electricity poles; a share dead, more in the poor districts, some solar
            if r['k'] == 'main' or (rch in ('elite', 'civic') and r['k'] == 'street'):
                pole_side = (1 if hash(r['id']) % 2 else -1)
                loff = -pole_side * (r['w'] / 2 + 1.0)
                for i in range(len(piece) - 1):
                    a, b = piece[i], piece[i + 1]
                    L = math.dist(a, b)
                    if L < 1e-6:
                        continue
                    dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                    s0 = (sum(math.dist(piece[j], piece[j + 1]) for j in range(i)))
                    k = (38 - (s0 + 19) % 38) % 38
                    while k < L:
                        p = (a[0] + dx * k - dy * loff, a[1] + dy * k + dx * loff)
                        if not in_building(p, 0.3):
                            lr = Rng('lamp', round(p[0]), round(p[1]))
                            # the arm reaches back over the road
                            ang = math.atan2(dx * (1 if loff < 0 else -1), -dy * (1 if loff < 0 else -1))
                            LAMPS.extend(roadside.street_light(sm, p[0], p[1], ang, lr, h=9 if r['k'] == 'main' else 7.5,
                                                               working=not lr.chance(DEAD_LAMPS.get(rch, 0.3)), solar=rch in ('dense', 'sprawl', 'waterfront') and lr.chance(0.3)))
                        k += 38
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
    for b in blds_here:  # service drops to houses from the nearest pole
        if not poles or b['kind'] not in ('front', 'back'):
            continue
        p, top = min(poles, key=lambda q: math.dist(q[0], b['c']))
        if math.dist(p, b['c']) < 30:
            cn = b['poly'][hash((b['d'], b['i'])) % 4]
            street.wire(sm, (top[0], top[1], top[2] - 0.6), (cn[0], cn[1], min(b['storeys'] * 3.1, 6.5) - 0.3), 1.0, t=0.012, n=5)

    # life: a still of the traffic (moving, frozen; parked at the edges), people along the frontages
    # and in the markets, danfos loading in the motor parks, container trucks queued for the port,
    # 911 lorries at the food markets, and the trains on the line. Half as thick in the web build.
    vm, hm = MeshBuilder(), MeshBuilder()
    thin = 0.5 if detail.web() else 1.0
    WEALTH = {'elite': 0.85, 'civic': 0.55, 'dense': 0.3, 'sprawl': 0.35, 'old_island': 0.3, 'waterfront': 0.1, 'port': 0.3}
    CROWD = {'dense': 30, 'old_island': 40, 'sprawl': 15, 'elite': 2, 'civic': 10, 'waterfront': 20, 'port': 10}  # per 100 m, research-street 4.3

    def put_vehicle(kind, x, y, ang, cond, rng, rch, wealth):
        M = Matrix.Translation((x, y, 0)) @ Matrix.Rotation(ang, 4, 'Z')
        fn = vehicles.BUILDERS[kind]
        if kind == 'car':
            fn(vm, M, rng, cond, kind=rng.pick({'saloon': 5, 'suv': 3 + 4 * wealth, 'pickup': 1}), taxi=rch == 'old_island' and rng.chance(0.15))
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
        wealth = WEALTH[rch]
        mixk = dict(vehicles.mix(rch, r['k']))
        if d == 'foodgate' and r['k'] == 'main':
            mixk['lorry911'] = 10  # the food lorries of the big market
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
                gap = {'main': 14, 'street': 30, 'lane': 60}[r['k']] / thin
                for off, dirn in lanes:
                    k = rr.between(0, gap)
                    while k < Ls:
                        kind = rr.pick(mixk)
                        x, y = a[0] + dx * k - dy * off, a[1] + dy * k + dx * off
                        if inside((x, y)) and not in_building((x, y), 0.5):
                            put_vehicle(kind, x, y, ang if dirn > 0 else ang + math.pi, vehicles.condition(wealth, rr, commercial=kind in vehicles.COMMERCIAL), rr, rch, wealth)
                            built['vehicle:' + kind] = built.get('vehicle:' + kind, 0) + 1
                        k += vehicles.LENGTH[kind] + rr.between(gap * 0.4, gap * 1.6)
                if r['k'] in ('street', 'main'):  # parked at the edge
                    for side in (-1, 1):
                        k = rr.between(0, 20)
                        while k < Ls:
                            kind = rr.pick({'car': 4, 'keke': 2, 'okada': 3, 'danfo': 1 if r['k'] == 'main' else 0.2})
                            o = side * (r['w'] / 2 - 1.0)
                            x, y = a[0] + dx * k - dy * o, a[1] + dy * k + dx * o
                            if inside((x, y)) and not in_building((x, y), 0.6) and rr.chance(0.55 * thin):
                                put_vehicle(kind, x, y, ang + (math.pi if rr.chance(0.5) else 0) + rr.between(-0.1, 0.1), vehicles.condition(wealth, rr, kind in vehicles.COMMERCIAL, parked=True), rr, rch, wealth)
                            k += vehicles.LENGTH[kind] + rr.between(2, 18)
                n = int(Ls / 100 * CROWD.get(rch, 15) * (1.6 if r['k'] == 'main' else 1.0) * thin)
                for _ in range(n):  # people along the frontage
                    k, side = rr.between(0, Ls), rr.pick([-1, 1])
                    o = side * (r['w'] / 2 + rr.between(0.3, 2.8))
                    x, y = a[0] + dx * k - dy * o, a[1] + dy * k + dx * o
                    if inside((x, y)) and not in_building((x, y), 0.2):
                        walk = ang + (0 if rr.chance(0.5) else math.pi) + rr.between(-0.3, 0.3) if rr.chance(0.6) else rr.between(0, math.tau)
                        people.person(hm, Matrix.Translation((x, y, 0.03)) @ Matrix.Rotation(walk, 4, 'Z'), rr, ch=rch)
    for pc in PARCELS:  # markets, motor parks, the port's truck park, the food lorries
        if not inside(cent(pc['pts'])):
            continue
        pts, kind = pc['pts'], pc['kind']
        rch = CHARACTER.get(pc['d'], 'dense')
        rr = Rng('life', pc['d'], kind, round(cent(pts)[0]))
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        if kind in ('market', 'motor park', 'under bridge', 'under-bridge'):
            n = 0
            for _ in range(4000):
                if n > (400 if kind == 'market' else 80) * thin:
                    break
                p = (rr.between(min(xs), max(xs)), rr.between(min(ys), max(ys)))
                if in_poly(p, pts) and not in_building(p, 0.3):
                    people.person(hm, Matrix.Translation((p[0], p[1], 0.05)) @ Matrix.Rotation(rr.between(0, math.tau), 4, 'Z'), rr, ch=rch, kind=rr.pick({None: 4, 'hawker': 1, 'wrapper': 1}) or None)
                    n += 1
        rows = {'motor park': ('danfo', 2.6, 7.0, 12), 'truck park': ('container', 3.4, 18.5, 24), 'lorry park': ('lorry911', 3.2, 10.0, 16)}
        if pc['d'] == 'foodgate' and kind == 'market':
            rows['market'] = ('lorry911', 3.2, 10.0, 6)
        if kind in rows:
            vk, sx, sy, count = rows[kind]
            c = cent(pts)
            per = max(1, int(count ** 0.5 * 1.5))
            for k in range(count):
                x, y = c[0] + (k % per - (per - 1) / 2) * sx, c[1] + (k // per - 0.5) * sy
                if in_poly((x, y), pts) and not in_building((x, y), 0.5):
                    put_vehicle(vk, x, y, math.pi / 2, vehicles.condition(0.3, rr, True, parked=True), rr, rch, 0.3)
                    built['vehicle:' + vk] = built.get('vehicle:' + vk, 0) + 1
    # trains on the line: a commuter set at the Hub station, the old narrow-gauge train in Railside,
    # a freight train at the port end
    for name, at, consist in (('commuter', 'station', ['commuter'] * 4), ('old', 0.22, ['loco'] + ['coach'] * 4), ('freight', 0.9, ['loco'] + ['wagon'] * 8)):
        line_pts = [P(p) for p in GD['rail']['pts']]
        segl = [math.dist(line_pts[i], line_pts[i + 1]) for i in range(len(line_pts) - 1)]
        S = sum(segl)
        if at == 'station':
            st = next((p for p in GD['pois'] if p['name'] == 'Hub Rail Station'), None)
            if not st:
                continue
            q = P((st['x'], st['y']))
            best, acc = (1e9, 0), 0.0
            for i in range(len(line_pts) - 1):
                A, B = line_pts[i], line_pts[i + 1]
                for t in (j / 50 for j in range(51)):
                    p = (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)
                    if math.dist(p, q) < best[0]:
                        best = (math.dist(p, q), acc + segl[i] * t)
                acc += segl[i]
            s0 = best[1]
        else:
            s0 = S * at
        trng = Rng('train', name)
        s = s0
        for idx, kname in enumerate(consist):
            fn, ln = vehicles.TRAIN[kname]
            mid = s - ln / 2
            acc = 0.0
            for i in range(len(line_pts) - 1):
                if acc + segl[i] >= mid:
                    A, B = line_pts[i], line_pts[i + 1]
                    t = (mid - acc) / segl[i]
                    p = (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)
                    if inside(p):
                        M = Matrix.Translation((p[0], p[1], 0)) @ Matrix.Rotation(math.atan2(B[1] - A[1], B[0] - A[0]), 4, 'Z')
                        if kname == 'commuter':
                            fn(vm, M, trng, cab=idx == 0)  # the leading car has the driver's cab
                        else:
                            fn(vm, M, trng)
                        built['train:' + kname] = built.get('train:' + kname, 0) + 1
                    break
                acc += segl[i]
            s -= ln

    # structures, expressways, bridges, rail, canals, boardwalks, walls, gates
    tm = MeshBuilder()
    for s in GD.get('structures', []):
        pts = [P(p) for p in s['pts']]
        if not inside(cent(pts)):
            continue
        rng = Rng('struct', s['name'], round(pts[0][0]))
        {'flyover': lambda: structures.flyover(tm, pts, s['width'], s.get('layer', 1), rng, lamps=LAMPS), 'skywalk': lambda: structures.skywalk(tm, pts, s['width'], rng),
         'footbridge': lambda: structures.footbridge(tm, structures.snap_footbridge(pts, CANALS), s['width'], rng), 'jetty': lambda: structures.jetty(tm, pts, s['width'], rng),
         'ramp': lambda: structures.flyover(tm, pts, s['width'], 1, rng, lamps=LAMPS)}.get(s['kind'], lambda: None)()
        built['structure:' + s['kind']] = built.get('structure:' + s['kind'], 0) + 1
    for a_ in GD.get('arterials', []):
        pts = [P(p) for p in a_['pts']]
        w = ART_W.get(a_['cls'], 18)
        rng = Rng('arterial', a_['name'])
        if a_['cls'] == 'bridge':  # the whole line, so the ramps sit at the real ends; this tile's slabs only
            (structures.cable_bridge if 'Cable' in a_['name'] else structures.long_bridge)(tm, pts, w, rng, keep=inside, lamps=LAMPS)
            continue
        for piece in clip_line_rect(pts, x0, y0, x1, y1):
            structures.expressway(tm, piece, w, rng, median=a_['cls'] == 'exp' or rng.chance(0.5), lamps=LAMPS, keep=inside)
    for piece in clip_line_rect([P(p) for p in GD['rail']['pts']], x0, y0, x1, y1):
        structures.rail(tm, piece, Rng('rail'))
    for c in GD.get('canals', []):
        for piece in clip_line_rect([P(p) for p in c['pts']], x0, y0, x1, y1):
            structures.canal(tm, piece, structures.CANAL_W, Rng('canal', c['d']))
    for bw in GD.get('boardwalks', []):
        for piece in clip_line_rect([P(p) for p in bw], x0, y0, x1, y1):
            structures.boardwalk(tm, piece, Rng('boardwalk', round(bw[0][0])))
    for d, segs in (GD.get('walls') or {}).items():
        for w in segs:
            pts = [P(p) for p in w]
            if inside(cent(pts)):
                structures.estate_wall(tm, pts, Rng('wall', d))
    for gt in GD.get('gates', []):
        pts = [P(p) for p in gt['pts']]
        if inside(cent(pts)):
            structures.estate_gate(tm, pts, gt.get('main'), Rng('gate'))

    # trees on open ground, by character
    tree_n = {'elite': 60, 'civic': 30, 'sprawl': 25, 'dense': 8, 'old_island': 6, 'waterfront': 10, 'port': 6, None: 80}.get(ch, 15)
    trng = Rng('trees', tx, ty)
    for _ in range(tree_n):
        p = (trng.between(x0, x1), trng.between(y0, y1))
        if in_building(p, 2.0) or any(dist_line(p, r['pts']) < r['w'] / 2 + 2 for r in roads_near) or any(in_poly(p, [P(q) for q in wp]) for wp in GD['water']):
            continue
        parcels.tree(pm, p[0], p[1], trng, kind=trng.pick({'palm': 2 if ch in ('old_island', 'elite', 'waterfront') else 1, 'broad': 2}))

    for mb_, name in ((g, 'ground'), (pm, 'parcels'), (sm, 'street'), (tm, 'structures'), (vm, 'traffic'), (hm, 'people')):
        if mb_.faces:
            mb_.to_object(name, col, master)
    return col, built, (x0, y0)


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
    return dict(kind=b['kind'], storeys=b['storeys'], district=b['d'], poly=poly, facing=facing, frontage=best, near_main=near_main,
                name=f"{b['d']}_{b['kind']}_{b['i']}", style=b.get('style'),
                unfinished=b['storeys'] >= 2 and rng.chance(UNFINISHED_SHARE.get(b['d'], 0.01)),
                wall_poly=offset(poly, 2.0), wall_skip=lambda m, others=others: any(in_poly(m, o) for o in others))


def export(col, origin, path):
    """Join the tile into one object, move it to the tile's corner, export Draco GLB."""
    obs = [o for o in col.all_objects if o.type == 'MESH']
    if not obs:
        return 0
    if os.environ.get('GIDI_FACES'):  # where the faces go, by object kind
        tally = {}
        for o in obs:
            k = o.name.split('_')[1] if o.name.count('_') >= 2 else o.name
            tally[k] = tally.get(k, 0) + len(o.data.polygons)
        print('FACES', sorted(tally.items(), key=lambda kv: -kv[1])[:12])
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in obs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    if len(obs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.data.transform(Matrix.Translation((-origin[0], -origin[1], 0)))
    ob.name = os.path.basename(path)[:-4]
    nt = len(ob.data.polygons)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_vertex_color='ACTIVE', export_all_vertex_colors=False,
                              export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6, export_draco_position_quantization=16,
                              export_draco_normal_quantization=8, export_draco_color_quantization=8, export_draco_texcoord_quantization=10,
                              export_materials='EXPORT', export_image_format='NONE', export_yup=True)
    return nt


if __name__ == '__main__':
    os.makedirs(os.path.join(OUT, 'tiles'), exist_ok=True)
    ov = poi_overrides()
    for tx, ty in TILES:
        t0 = time.time()
        detail.SIGNS.clear()
        LAMPS.clear()
        col, built, origin = build_tile(tx, ty, ov)
        lamps = [[round(x - origin[0], 2), round(z, 2), round(-(y - origin[1]), 2)] for x, y, z in LAMPS]  # GLB frame, like signs
        signs = []
        for sg in detail.SIGNS:  # tile-relative, in the GLB's y-up frame: (x, z, -y)
            m = sg['m']
            px, py, pz = m[0][3] - origin[0], m[1][3] - origin[1], m[2][3]
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
