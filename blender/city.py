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
from gidi_kit import archetypes, parcels, places, registry, street, structures  # noqa: E402
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
for i, m in enumerate(GD.get('mains', [])):
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


def poi_overrides():
    """Point places take over the nearest plain building in their district (cached on disk)."""
    path = os.path.join(OUT, 'poi_overrides.json')
    if os.path.exists(path):
        return {tuple(k.split('|', 1)): v for k, v in json.load(open(path)).items()}
    res, used = {}, set()
    for poi in GD['pois']:
        t = poi['type']
        if t not in registry.POI_PLACES:
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
            fn = registry.POI_PLACES[ov['type']]
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
        if fn and len(c['poly']) == 4:
            a = attributes(dict(i=0, d=c['d'], kind=c['type'], poly=c['poly'], c=c['c'], storeys=2), roads_near, polys_near)
            a['label'] = c['name']
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

    # roads and street life
    sm = MeshBuilder()
    poles = []
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
                street.kerbs(sm, rc, ST['kerb'] if r['k'] == 'main' else 'white', rr, skip=lambda p: in_building(p, 0.1))
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

    # structures, expressways, bridges, rail, canals, boardwalks, walls, gates
    tm = MeshBuilder()
    for s in GD.get('structures', []):
        pts = [P(p) for p in s['pts']]
        if not inside(cent(pts)):
            continue
        rng = Rng('struct', s['name'], round(pts[0][0]))
        {'flyover': lambda: structures.flyover(tm, pts, s['width'], s.get('layer', 1), rng), 'skywalk': lambda: structures.skywalk(tm, pts, s['width'], rng),
         'footbridge': lambda: structures.footbridge(tm, pts, s['width'], rng), 'jetty': lambda: structures.jetty(tm, pts, s['width'], rng),
         'ramp': lambda: structures.flyover(tm, pts, s['width'], 1, rng)}.get(s['kind'], lambda: None)()
        built['structure:' + s['kind']] = built.get('structure:' + s['kind'], 0) + 1
    for a_ in GD.get('arterials', []):
        pts = [P(p) for p in a_['pts']]
        w = ART_W.get(a_['cls'], 18)
        rng = Rng('arterial', a_['name'])
        for piece in clip_line_rect(pts, x0, y0, x1, y1):
            if a_['cls'] == 'bridge':
                (structures.cable_bridge if 'Cable' in a_['name'] else structures.long_bridge)(tm, piece, w, rng)
            else:
                structures.expressway(tm, piece, w, rng, median=a_['cls'] == 'exp' or rng.chance(0.5))
    for piece in clip_line_rect([P(p) for p in GD['rail']['pts']], x0, y0, x1, y1):
        structures.rail(tm, piece, Rng('rail'))
    for c in GD.get('canals', []):
        for piece in clip_line_rect([P(p) for p in c['pts']], x0, y0, x1, y1):
            structures.canal(tm, piece, 8.0, Rng('canal', c['d']))
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

    for mb_, name in ((g, 'ground'), (pm, 'parcels'), (sm, 'street'), (tm, 'structures')):
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
        col, built, origin = build_tile(tx, ty, ov)
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
        json.dump(dict(info, origin=[origin[0], origin[1]], signs=signs), open(os.path.join(OUT, 'tiles', f'{tx}_{ty}.json'), 'w'), separators=(',', ':'))
        print('TILE', json.dumps(info))
