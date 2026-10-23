"""A district's first draft of buildings, from its real blocks' own houses (owner, 23 Oct: "real footprints, then hand").

  ~/.venvs/gidi/bin/python scripts/draft_buildings.py map/d15 [--blocks=3,7] [--frontage] [--dry]

--frontage lines the named blocks' street edges with the twin place's own houses turned to face the street (for
blocks cut by hand-drawn lanes; see frontage()); --sizes=a,b takes only real buildings of a to b m2 (a warehouse
strip: its sheds; default 12,600, houses).

A Gidi block (the land between the district's roads) is its real block at 1:3: the streets lie on the real lines. Houses
stay house-size, so a block takes its real block's own houses, moved, never scaled or turned. Anchors are set round the
block's edge (corners and every STEP m); each Gidi point belongs to its nearest anchor c and takes the real fabric at the
same place relative to the real anchor 3c (a house moves by -2c). Near each anchor the real street runs through 3c the way
the Gidi street runs through c, so frontages keep their real setbacks and angles; the real block's dropped streets come
through as gaps, where lanes are drawn by hand. The real street is where the real houses are not, so each anchor's
fabric is nudged (up to SHIFT m) to where the Gidi roads near it are clearest, and a house still caught by a road is
moved straight away from it (up to NUDGE m): the road lines carry their own small errors, tripled at real size. A house
still caught is set back on clear land beside where it fell (up to SETBACK m), and houses that overlap are trimmed to a
shared party wall: the road stays on its real line (hand passes 1 and 2, 23 Oct).

Written: one `building` record per kept house, its footprint only, with a `note`. Everything else (kind, storeys, roof,
finish, ground floor) is left missing, so the board shows it amber until the hand pass sets it from the shots. A house
that would land on a road, the rail or the station, or on a house already kept, is not written; the first kind is
listed in <district>/BUILDINGS.md for the hand pass (the rule: a real house on a Gidi road means the road moves). Blocks
that already hold a building are skipped: a draft never moves anything already in the map ("Rules draft, records rule").

Footprints: Microsoft's Global ML Building Footprints (ODbL, © Microsoft; numbers only), streamed from
~/Real-world/research/data/ms-buildings/ for the district's real box. Never Google's geometry.
"""
import gzip
import hashlib
import json
import math
import os
import sys

from pyproj import Transformer
from shapely.geometry import LineString, Point, Polygon, shape
from shapely.affinity import rotate, translate
from shapely.ops import unary_union
from shapely.strtree import STRtree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.expanduser('~/Real-world/research/data/ms-buildings/')
FU, FV = 500525.0, 707825.0            # the frame's south-west corner, UTM 31N (web/frame-study.js `real_sw_utm31`)
SCALE, RH = 3, 10500 * 3
STEP, SHIFT, NUDGE, SETBACK = 30.0, 7, 6.0, 15.0
FRONT, HOUSE = 0.7, [12, 600]        # frontage: front this far in from the street edge; a house's footprint, m2
WIDTH = {'motorway': 25, 'trunk': 21.5, 'main_road': 12, 'local_main': 8, 'service_road': 7, 'market_street': 8,
         'home_street': 6, 'lane': 4, 'path': 2, 'ramp': 6}          # where a road's width is still missing
RAIL_CORRIDOR = 18.0                                               # where a rail's corridor is still missing
TI = Transformer.from_crs(32631, 4326, always_xy=True)
T = Transformer.from_crs(4326, 32631, always_xy=True)


def footprints(box):
    """Real footprints inside a Gidi box, as polygons in real metres on Gidi axes (x east, y south; Gidi x 3)."""
    x0, y0, x1, y1 = box
    ux0, ux1 = FU + SCALE * x0, FU + SCALE * x1
    uy0, uy1 = FV + RH - SCALE * y1, FV + RH - SCALE * y0
    lo0, la0 = TI.transform(ux0, uy0)
    lo1, la1 = TI.transform(ux1, uy1)
    out = []
    for name in sorted(os.listdir(DATA)):
        with gzip.open(DATA + name, 'rt') as f:
            for line in f:
                i = line.find('[[[')
                a = line[i + 3:line.find(']', i)].split(',')
                lo, la = float(a[0]), float(a[1])
                if lo0 <= lo <= lo1 and la0 <= la <= la1:
                    ring = json.loads(line)['geometry']['coordinates'][0]
                    xs, ys = T.transform([p[0] for p in ring], [p[1] for p in ring])
                    out.append(Polygon([(x - FU, FV + RH - y) for x, y in zip(xs, ys)]))
    return out


def anchors(g):
    ring = g.exterior
    n = max(int(ring.length // STEP), 4)
    pts = [ring.interpolate(i * ring.length / n) for i in range(n)]
    cs = list(ring.coords)[:-1]
    for i, c in enumerate(cs):                       # corners: where the edge turns by more than 30 degrees
        a, b = cs[i - 1], cs[(i + 1) % len(cs)]
        t1 = math.atan2(c[1] - a[1], c[0] - a[0])
        t2 = math.atan2(b[1] - c[1], b[0] - c[0])
        if abs((t2 - t1 + math.pi) % (2 * math.pi) - math.pi) > math.radians(30):
            pts.append(Point(c))
    return pts


def fill(g, real, tree, blocked, outline):
    """One block's houses: (kept, on a road). A house must stand wholly inside the district."""
    A = anchors(g)
    near = lambda p: min(range(len(A)), key=lambda k: A[k].distance(p))
    cands = []
    for k, c in enumerate(A):
        local = [real[i] for i in tree.query(Point(SCALE * c.x, SCALE * c.y).buffer(SCALE * 40 + 120))]
        zone = blocked.intersection(c.buffer(40))
        moved = [f for f in (translate(f, -2 * c.x, -2 * c.y) for f in local) if f.distance(c) < 45]
        best = min((sum(f.intersection(translate(zone, -dx, -dy)).area for f in moved), dx * dx + dy * dy, dx, dy)
                   for dx in range(-SHIFT, SHIFT + 1) for dy in range(-SHIFT, SHIFT + 1) if dx * dx + dy * dy <= SHIFT ** 2)
        dx, dy = best[2], best[3]
        for f in local:
            h = translate(f, -2 * c.x + dx, -2 * c.y + dy)
            p = h.centroid
            if g.contains(p) and near(p) == k:
                cands.append((p.distance(c), h))
    cands.sort(key=lambda t: t[0])
    keep, clash = [], []
    free = lambda h: not any(h.intersection(o).area > 0.1 * min(h.area, o.area) for o in keep)
    for _, h in cands:
        if not outline.contains(h):
            continue
        if h.intersection(blocked).area > 0.5:
            h2 = nudge(h, blocked)
            if h2 is None or not (free(h2) and outline.contains(h2)):
                h2 = set_back(h, g, blocked, outline, keep)
            if h2 is None:
                clash.append(h)
            else:
                keep.append(h2)
        elif free(h):
            keep.append(h)
    return keep, clash


def axis(f):
    """A real house's street-facing side: the short side of its smallest box (angle in degrees, width, depth)."""
    c = list(f.minimum_rotated_rectangle.exterior.coords)
    e = [(c[i + 1][0] - c[i][0], c[i + 1][1] - c[i][1]) for i in range(2)]
    L = [math.hypot(*v) for v in e]
    k = 0 if L[0] <= L[1] else 1
    return math.degrees(math.atan2(e[k][1], e[k][0])), L[k], L[1 - k]


def frontage(g, real, tree, outline):
    """A block cut by hand-drawn lanes (owner, 23 Oct: "lanes on dropped streets"): its edges are lined with the twin
    place's own real houses, nearest the twin point first, each turned to face its street, its front FRONT m in from the
    street edge, wall to wall. Copied fabric cannot follow lanes drawn by hand (the real streets near the twin point are
    not where the lanes are), so here the houses follow the lanes and keep only their real shapes and sizes."""
    keep, used, ring, t = [], set(), g.exterior, 0.0
    inside = g.buffer(0.01)
    while t < ring.length - 4:
        p, q = ring.interpolate(t), ring.interpolate(min(t + 2, ring.length))
        ang = math.degrees(math.atan2(q.y - p.y, q.x - p.x))
        ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        twin = Point(SCALE * p.x, SCALE * p.y)
        cand = sorted((i for i in tree.query(twin.buffer(80)) if i not in used and HOUSE[0] < real[i].area < HOUSE[1]),
                      key=lambda i: real[i].centroid.distance(twin))
        placed = False
        for i in cand[:12]:
            a, wid, dep = axis(real[i])
            h = rotate(real[i], ang - a, origin='centroid')
            c = h.centroid
            for sgn in (1, -1):
                tx = p.x + ux * wid / 2 - sgn * uy * (dep / 2 + FRONT)
                ty = p.y + uy * wid / 2 + sgn * ux * (dep / 2 + FRONT)
                h2 = translate(h, tx - c.x, ty - c.y)
                if inside.contains(h2) and outline.contains(h2) and not any(h2.intersection(o).area > 0.5 for o in keep):
                    keep.append(h2)
                    used.add(i)
                    t += wid + 0.3
                    placed = True
                    break
            if placed:
                break
        if not placed:
            t += 1.0
    return keep, []


def set_back(h, g, blocked, outline, keep):
    """A house the road lines catch, set back on clear land beside where it fell: the nearest spot within SETBACK m
    (rings of 0.5 m, not turned) that is half a metre clear of every road, inside the district, on its own block and
    clear of the houses kept; else None (hand pass 1, 23 Oct: the road stays on its real line)."""
    gap = blocked.buffer(0.5)
    for r in range(1, int(SETBACK * 2) + 1):
        for a in range(0, 360, 10):
            h2 = translate(h, r / 2 * math.cos(math.radians(a)), r / 2 * math.sin(math.radians(a)))
            if (g.contains(h2.centroid) and outline.contains(h2) and not h2.intersects(gap)
                    and not any(h2.intersection(o).area > 0.05 * min(h2.area, o.area) for o in keep)):
                return h2
    return None


def party_walls(new, have):
    """Neighbours share a wall, never pass through each other (hand pass 2, 23 Oct): each new house that overlaps a
    bigger one, or any house already in the map, is trimmed back to that house's wall."""
    from shapely.strtree import STRtree as T
    allh = have + new
    tree = T(allh)
    for k in sorted(range(len(new)), key=lambda k: new[k].area):
        h = new[k]
        for j in tree.query(h):
            o = allh[j]
            if o is h or (j >= len(have) and o.area < h.area):
                continue
            if h.intersection(o).area > 0.05:
                d = h.difference(o).buffer(-0.05).buffer(0.05)
                if d.is_empty:
                    h = d
                    break
                h = max(getattr(d, 'geoms', [d]), key=lambda q: q.area).simplify(0.1)
        new[k] = h
    return [h for h in new if not h.is_empty and h.area >= 12]      # a house swallowed by its neighbour is gone


def nudge(h, blocked):
    """A house the road lines catch, moved straight away from the road (up to NUDGE m) until it is clear; else None.
    The Gidi road lines carry small errors of their own (tripled at real size), so a house a few metres onto a road is
    where its real street really runs."""
    from shapely.ops import nearest_points
    c = h.centroid
    p = nearest_points(blocked.boundary, c)[0]
    dx, dy = c.x - p.x, c.y - p.y
    n = math.hypot(dx, dy)
    if n < 1e-6:
        return None
    dx, dy = dx / n, dy / n
    for k in range(1, int(NUDGE * 2) + 1):
        h2 = translate(h, dx * k / 2, dy * k / 2)
        if h2.intersection(blocked).area <= 0.5:
            return h2
    return None


def ring(h):
    pts = [[round(x, 2), round(y, 2)] for x, y in h.exterior.coords][:-1]
    return [p for i, p in enumerate(pts) if p != pts[i - 1]]


def bid(h):
    c = h.centroid
    return 'b-' + hashlib.sha1(f'{c.x:.2f},{c.y:.2f}'.encode()).hexdigest()[:8]


def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    opt = dict(x[2:].split('=', 1) if '=' in x else (x[2:], True) for x in sys.argv[1:] if x.startswith('--'))
    D = a[0]
    dist = json.load(open(os.path.join(D, 'district.json')))['records'][0]
    pf = os.path.join(D, 'plan.json')
    plan = json.load(open(pf))
    recs = plan['records']
    roads = [r for r in recs if r['type'] == 'road']
    width = lambda r: r.get('width') or WIDTH[r['kind']]
    blocked = unary_union(
        [LineString(r['centreline']).buffer(width(r) / 2, cap_style=2) for r in roads] +
        [LineString(r['centreline']).buffer((r.get('corridor') or RAIL_CORRIDOR) / 2) for r in recs if r['type'] == 'rail'] +
        [Polygon(ring_[0]) for r in recs if r['type'] == 'station' for ring_ in [r['area']]])
    outline = unary_union([Polygon(o) for o in dist['outline']]).buffer(0)
    land = outline.difference(blocked)
    blocks = sorted([b for b in getattr(land, 'geoms', [land]) if b.area > 200], key=lambda b: (-b.area, b.bounds))
    print('reading footprints ...', flush=True)
    real = footprints(outline.buffer(60).bounds)
    tree = STRtree(real)
    have = [Polygon(r['footprint']) for r in recs if r['type'] == 'building']
    only = {int(v) for v in opt['blocks'].split(',')} if 'blocks' in opt else None
    new, report = [], []
    for i, g in enumerate(blocks):
        if only is not None and i not in only:
            continue
        if any(g.intersects(h) for h in have):
            report.append((i, g, None, None))
            continue
        if 'sizes' in opt:                                   # e.g. --sizes=600,20000: a warehouse strip's sheds only
            HOUSE[:] = [float(v) for v in opt['sizes'].split(',')]
        keep, clash = (frontage(g, real, tree, outline) if opt.get('frontage') else fill(g, real, tree, blocked, outline))
        new += keep
        report.append((i, g, keep, clash))
        print(f'block {i}: {len(keep)} houses, {round(sum(h.area for h in keep) / g.area * 100)}% covered, {len(clash)} on a road',
              flush=True)
    new = party_walls(new, have)
    seen = {r['id'] for r in recs}
    for h in new:
        i = bid(h)
        if i in seen:
            continue
        seen.add(i)
        recs.append({'id': i, 'type': 'building', 'footprint': ring(h),
                     'note': "draft: the real block's own house, moved (scripts/draft_buildings.py); kind, storeys and looks by hand"})
    lines = ['# ' + dist.get('name', D) + ': the buildings draft and its hand pass', '',
             f"Drafted by `scripts/draft_buildings.py` (owner, 23 Oct: real footprints, then hand). {len(new)} houses in "
             f"{sum(1 for r in report if r[2] is not None)} blocks. Each block's number is its place in size order.", '',
             '## Real houses that land on a road (hand pass: move the road, or the house if the road is right)', '',
             '| block | houses | covered | on a road at (Gidi x, y) |', '|---|---|---|---|']
    for i, g, keep, clash in report:
        if keep is None:
            lines.append(f'| {i} | already drawn: skipped | | |')
            continue
        at = '; '.join(f'{h.centroid.x:.0f}, {h.centroid.y:.0f}' for h in clash)
        lines.append(f'| {i} | {len(keep)} | {round(sum(h.area for h in keep) / g.area * 100)}% | {at} |')
    if opt.get('dry'):
        print('\n'.join(lines[-len(report):]))
        return
    plan['records'] = recs
    json.dump(plan, open(pf, 'w'), ensure_ascii=False)
    open(os.path.join(D, 'BUILDINGS.md'), 'w').write('\n'.join(lines) + '\n')
    print(f'{len(new)} houses written to {pf}; run check_map.py --fix for the layout')


if __name__ == '__main__':
    main()
