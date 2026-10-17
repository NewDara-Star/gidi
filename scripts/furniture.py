# Street furniture as data, run by bake_web.py after the junctions and heights (the ground plan of the Google rebuild).
# Every pole, street light, traffic light, transformer and bus stop gets its spot in out["furniture"] ({kind, x, y, ang, road}:
# ang in degrees on the map's axes, y south: toward the road, or for a traffic light out along its arm to the traffic), on a walkway
# (scripts/cross_sections.py), never on any road's carriageway or gutter, never in a building, never under a deck.
# The 3D kit draws them where the data says. Only for districts built to the cross-sections ("fabric": "lagos"); the
# others keep the kit's own placing until they are rebuilt.
#
# Spacing (Lagos lines; Overture maps too few to count from: about one bus stop per 2 km2 in Food Gate):
#   main roads and arterials: a street light every LIGHT_M, both sides on arterials, one side on mains
#   streets: an electricity pole every POLE_M on one side, a transformer every TRANSFORMER_M of street
#   traffic lights: at every "signals" junction, one per arm, on the corner to the right of the approach (Nigeria drives right)
#   bus stops: on mains and arterials, about every BUS_M, near a junction, alternating sides
#   LASMA posts: a traffic wardens' booth at every signalled junction, on a corner clear of the traffic lights
import math
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree
import cross_sections as XS

LIGHT_M, POLE_M, TRANSFORMER_M, BUS_M = 38.0, 36.0, 260.0, 450.0
SPACE = 1.5   # nothing within this of another piece of furniture


def furniture(out, districts, bush=False):
    """districts: ids built to the cross-sections. Returns a report. bush=True: the roads outside every district instead
    (owner, 17 Oct 2026: if it's in the 3D, it's in the 2D; the kit used to put up its own poles and lamps out there, and
    one stood in the middle of a road). Those are added to what is already placed, with d "bush"."""
    if bush:
        from shapely.geometry import box
        W, H = out['size']
        polys = {'bush': box(0, 0, W, H).difference(unary_union([Polygon(d['poly'][0]).buffer(0) for d in out['districts']]))}
    else:
        polys = {d['id']: Polygon(d['poly'][0]) for d in out['districts'] if d['id'] in districts}
    if not polys:
        return {}
    area = unary_union(list(polys.values()))
    # every road as (kind, line), and the strip no furniture may stand on: carriageway and gutter of all of them
    roads = []
    for kind, key in (('street', 'streets'), ('lane', 'lanes')):
        for d, L in (out.get(key) or {}).items():
            roads += [(kind, LineString(p)) for p in L if len(p) > 1]
    roads += [('main', LineString(m['pts'])) for m in out['mains']]
    roads += [(a['cls'] if a['cls'] in XS.SECTIONS else 'art', LineString(a['pts'])) for a in out['arterials']]
    roads = [(k, g) for k, g in roads if g.distance(area) < 60]
    keep_off = unary_union([g.buffer(XS.walkway_band(k)[0] + 0.25) for k, g in roads])
    decks = unary_union([LineString(s['pts']).buffer(s.get('width', 8) / 2 + 1) for s in out.get('structures', [])
                         if s['kind'] in ('flyover', 'skywalk', 'approach', 'ramp')] or [Point(-1e6, -1e6).buffer(1)])
    near_area = area.buffer(60)
    B = [p for L in out['buildings'].values() for b in L if len(b) > 3 for p in [Polygon(b[1:]).buffer(0)] if near_area.intersects(p)]   # neighbours' too
    bt = STRtree(B)
    wet = unary_union([Polygon(w) for w in out['water'] + out['ocean']])
    placed = list(out.get('furniture', [])) if bush else []
    grid = {}
    for f in placed:   # nothing too close to what the districts already have
        grid.setdefault((int(f['x'] // 10), int(f['y'] // 10)), []).append((f['x'], f['y']))
    rep = {}

    edge = area.buffer(40)   # a junction on the district's edge gets all its lights, on both sides of the line

    def ok(p, within=None):
        if not (within or area).contains(p) or keep_off.contains(p) or decks.contains(p) or wet.contains(p):
            return False
        if any(B[j].distance(p) < 0.3 for j in bt.query(p.buffer(0.3))):
            return False
        gx, gy = int(p.x // 10), int(p.y // 10)
        return not any(math.dist((p.x, p.y), q) < SPACE for i in (-1, 0, 1) for j in (-1, 0, 1) for q in grid.get((gx + i, gy + j), []))

    def owner(p):   # the district it belongs to: the one it stands in, or the nearest (a light just over the line)
        return min(polys, key=lambda k: polys[k].distance(p))

    def put(kind, p, ang, road):
        placed.append({'kind': kind, 'x': round(p.x, 1), 'y': round(p.y, 1), 'ang': round(math.degrees(ang) % 360, 1), 'road': road, 'd': owner(p)})
        grid.setdefault((int(p.x // 10), int(p.y // 10)), []).append((p.x, p.y))
        rep[kind] = rep.get(kind, 0) + 1

    def along(g, kind, every, sides, what, start=0.0, name=''):
        a, b = XS.walkway_band(kind)
        off = (a + b) / 2
        t = start
        while t < g.length:
            q = g.interpolate(t)
            q2 = g.interpolate(min(g.length, t + 1.0)) if t + 1.0 <= g.length else g.interpolate(t - 1.0)
            ang = math.atan2(q2.y - q.y, q2.x - q.x) if t + 1.0 <= g.length else math.atan2(q.y - q2.y, q.x - q2.x)
            nx, ny = -math.sin(ang), math.cos(ang)
            for sd in sides:
                p = Point(q.x + nx * off * sd, q.y + ny * off * sd)
                if ok(p):
                    put(what, p, ang - (math.pi / 2 if sd > 0 else -math.pi / 2), name)   # ang: toward the road (lamp arms reach over it)
            t += every

    for k, g in roads:
        if k == 'main':
            along(g, 'main', LIGHT_M, (1,), 'street light', 10.0)
        elif k in ('art', 'exp'):
            along(g, k, LIGHT_M, (1, -1), 'street light', 10.0)
        elif k == 'street':
            along(g, 'street', POLE_M, (1,), 'pole', 6.0)
            along(g, 'street', TRANSFORMER_M, (-1,), 'transformer', 90.0)
    # bus stops: near junctions on the mains and arterials
    for k, g in roads:
        if k not in ('main', 'art', 'exp') or g.length < 120:
            continue
        side = 1
        for t in [x * BUS_M + 60 for x in range(int(g.length // BUS_M) + 1)]:
            if t >= g.length - 20:
                break
            for dt in range(0, 80, 4):
                q = g.interpolate(t + dt)
                q2 = g.interpolate(min(g.length, t + dt + 1))
                ang = math.atan2(q2.y - q.y, q2.x - q.x)
                a, b = XS.walkway_band(k)
                p = Point(q.x - math.sin(ang) * (a + b) / 2 * side, q.y + math.cos(ang) * (a + b) / 2 * side)
                if ok(p):
                    put('bus stop', p, ang - (math.pi / 2 if side > 0 else -math.pi / 2), '')   # its open side to the road
                    side = -side
                    break
    # traffic lights at signalled junctions: one per arm, on the corner to the right of the approaching traffic
    for j in out.get('junctions', []):
        if j['kind'] != 'signals' or not area.buffer(5).contains(Point(j['x'], j['y'])):
            continue
        C = Point(j['x'], j['y'])
        near = [(k, g) for k, g in roads if g.distance(C) < 3]
        if not near:
            continue
        reach = max(XS.walkway_band(k)[1] for k, g in near) + 2.0   # back from the middle, clear of the crossing road
        for bdeg in j.get('arms', []):
            b = math.radians(bdeg)
            ux, uy = math.cos(b), math.sin(b)   # out along the arm; traffic approaches heading -u
            arm_k = min(near, key=lambda kg: kg[1].distance(Point(C.x + ux * 20, C.y + uy * 20)))[0]
            a_, b_ = XS.walkway_band(arm_k)
            # the right of a driver heading h = -u: with y running south, right of (hx, hy) is (-hy, hx) = (uy, -ux)
            rx, ry = uy, -ux
            for back in (reach, reach + 3, reach + 6):
                p = Point(C.x + ux * back + rx * (a_ + b_) / 2, C.y + uy * back + ry * (a_ + b_) / 2)
                if ok(p, edge):
                    put('traffic light', p, b, '')   # it faces out along the arm, toward the approaching traffic
                    break
    # LASMA posts: the traffic wardens' booth (or umbrella and stand) at every signalled junction, on a corner clear of the lights
    for j in out.get('junctions', []):
        if j['kind'] != 'signals' or not area.buffer(5).contains(Point(j['x'], j['y'])):
            continue
        C = Point(j['x'], j['y'])
        near = [(k, g) for k, g in roads if g.distance(C) < 3]
        if not near:
            continue
        reach = max(XS.walkway_band(k)[1] for k, g in near) + 6.0
        done = False
        for bdeg in j.get('arms', []):
            b = math.radians(bdeg); ux, uy = math.cos(b), math.sin(b)
            arm_k = min(near, key=lambda kg: kg[1].distance(Point(C.x + ux * 20, C.y + uy * 20)))[0]
            a_, b_ = XS.walkway_band(arm_k)
            for side in (-1, 1):   # the left corner first: the lights stand on the right
                rx, ry = uy * side, -ux * side
                p = Point(C.x + ux * reach + rx * (a_ + b_) / 2, C.y + uy * reach + ry * (a_ + b_) / 2)
                if ok(p, edge):
                    put('lasma post', p, b + math.pi, ''); done = True; break
            if done:
                break
    out['furniture'] = placed
    return rep
