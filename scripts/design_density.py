"""A density pass: fill a district the way its real counterpart is built (Claude's design pass, owner 17 Oct 2026: "build it
based off the Lagos you see"). Writes hand edits into web/hand/<district>.json, so every house it adds or lowers can be moved,
reshaped or deleted on the drawing board like any other.

    python3 scripts/design_density.py maze [--dry]

What it does, street by street, on the finished map (web/gidi-data.js):
- along each side of every street, lane and main road, terraced houses at the building line: FRONT_LEN m along the road,
  FRONT_DEPTH m deep, a GAP between them, wherever the ground is free (no road, house, plot, market zone, safe ground,
  water, rail or deck in the way); then a second row behind them where there's room;
- the storeys of what it adds follow the district's mix (STOREYS), a little taller near the main roads;
- the existing towers away from the main roads come down to two storeys (a few stay), with "set storeys".

PROFILES holds each district's numbers, from the Google Earth study (study yes, lift no: only measurements, no geometry):
the Maze, from Mushin and Shomolu (18 Oct; notes in ~/gidi-data/research/google/maze/NOTES.md): roofs cover 75-85% of the ground; long one- and two-storey houses (about 10 x 15-30 m)
in rows along the streets with 1-3 m alleys between; taller buildings only here and there, mostly on the main roads.
"""
import json
import math
import os
import random
import sys

from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely.prepared import prep
from shapely.strtree import STRtree

sys.path.insert(0, os.path.dirname(__file__))
import cross_sections as XS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILES = {
    'maze': dict(front_len=(13, 26), front_depth=(8.5, 12), gap=(1.0, 2.2), back_depth=(8, 11), back_gap=(2.0, 3.2),
                 storeys={1: 0.55, 2: 0.4, 3: 0.05}, near_main_storeys={2: 0.55, 3: 0.3, 4: 0.15},
                 tall_keep=0.12, interior=True, alley=1.2, sizes=[((13, 24), (8, 11), 'back'), ((9, 13), (7, 9.5), 'back'), ((6, 9), (5, 7), 'back'), ((4, 6), (3.5, 5), 'shed')], note='density pass from the Mushin and Shomolu study, 18 Oct'),
}


def _pick(rng, dist):
    r, acc = rng.random(), 0.0
    for k, p in dist.items():
        acc += p
        if r < acc:
            return k
    return list(dist)[-1]


def plan(G, did, prof):
    rng = random.Random('density|' + did)
    D = Polygon([d for d in G['districts'] if d['id'] == did][0]['poly'][0]).buffer(0)
    inside = prep(D.buffer(-2.0))
    roads = []   # (kind, line)
    for src, kind in (('streets', 'street'), ('lanes', 'lane')):
        for d_, L in (G.get(src) or {}).items():
            roads += [(kind, LineString(p)) for p in L if len(p) > 1]
    roads += [('main', LineString(m['pts'])) for m in G.get('mains', []) if len(m['pts']) > 1]
    roads += [(a['cls'] if a['cls'] in XS.SECTIONS else 'art', LineString(a['pts'])) for a in G.get('arterials', []) if a['cls'] != 'bridge']
    near = D.buffer(60)
    roads = [(k, g) for k, g in roads if g.intersects(near)]
    keep_off = [g.buffer(XS.building_line(k) + 0.2) for k, g in roads]   # the building line of every road
    keep_off += [Polygon(w).buffer(1.0) for w in (G.get('water') or []) + (G.get('ocean') or []) if Polygon(w).buffer(0).intersects(near)]
    keep_off += [Polygon(p['pts']).buffer(1.0) for p in (G.get('parcels') or {}).get(did, [])]
    keep_off += [Polygon(z['pts']).buffer(0.5) for z in G.get('encroach', []) if z.get('d') == did]
    keep_off += [Polygon(s['pts']).buffer(1.5) for s in G.get('safe_ground', []) if s.get('d') == did and len(s['pts']) > 2]
    keep_off += [LineString(s['pts']).buffer((s.get('width') or 8) / 2 + 2) for s in G.get('structures', []) if len(s.get('pts', [])) > 1]
    if G.get('rail'):
        keep_off.append(LineString(G['rail']['pts']).buffer(8))
    keep_off += [LineString(c['pts']).buffer((c.get('width') or 6) / 2 + 2) for c in G.get('canals', []) if len(c.get('pts', [])) > 1]
    keep_off += [LineString(g['pts']).buffer((g.get('w') or 0.8) / 2 + 0.4) for g in G.get('gutters', [])
                 if len(g['pts']) > 1 and LineString(g['pts']).intersects(near)]   # no house over a gutter
    KO = STRtree(keep_off)
    existing = [Polygon(b[1:]).buffer(0) for b in G['buildings'].get(did, []) if len(b) > 3]
    placed = list(existing)
    PT = [STRtree(placed)]

    def free(poly, pad=0.9):
        if not inside.contains(poly):
            return False
        if any(keep_off[j].intersects(poly) for j in KO.query(poly)):
            return False
        g = poly.buffer(pad)
        if any(placed[j].intersects(g) for j in PT[0].query(g)):
            return False
        if NT[0] is None and new_polys:
            NT[0] = (STRtree(new_polys), len(new_polys))
        hits = [new_polys[j] for j in NT[0][0].query(g)] if NT[0] else []
        return not any(q.intersects(g) for q in hits) and not any(q.intersects(g) for q in new_polys[NT[0][1] if NT[0] else 0:])

    new_polys, edits = [], []
    NT = [None]   # a tree of the new houses, rebuilt now and then
    mains = [g for k, g in roads if k in ('main', 'art', 'exp')]
    for kind, g in roads:
        if kind not in ('street', 'lane', 'main'):
            continue
        bl = XS.building_line(kind) + 0.3
        for side in (1, -1):
            t = rng.uniform(0, 6)
            while t < g.length - 6:
                L = rng.uniform(*prof['front_len'])
                if t + L > g.length:
                    break
                a, b = g.interpolate(t), g.interpolate(t + L)
                ux, uy = b.x - a.x, b.y - a.y
                n = math.hypot(ux, uy) or 1
                ux, uy = ux / n, uy / n
                if g.interpolate(t + L / 2).distance(LineString([a, b])) > 1.5:   # too curved here for a straight terrace
                    t += 4
                    continue
                nx, ny = -uy * side, ux * side
                rows = [('front', bl, rng.uniform(*prof['front_depth']))]
                rows.append(('back', bl + rows[0][2] + rng.uniform(*prof['back_gap']), rng.uniform(*prof['back_depth'])))
                put_front = False
                for rk, off, dep in rows:
                    if rk == 'back' and not put_front:
                        break
                    pts = [(a.x + nx * off, a.y + ny * off), (b.x + nx * off, b.y + ny * off),
                           (b.x + nx * (off + dep), b.y + ny * (off + dep)), (a.x + nx * (off + dep), a.y + ny * (off + dep))]
                    poly = Polygon(pts)
                    if free(poly):
                        c = poly.centroid
                        by_main = min((m.distance(c) for m in mains), default=99) < 30
                        st = _pick(rng, prof['near_main_storeys'] if by_main else prof['storeys'])
                        new_polys.append(poly)
                        edits.append({'op': 'add building', 'kind': rk, 'pts': [[round(x, 1), round(y, 1)] for x, y in pts], 'storeys': st, 'note': prof['note']})
                        put_front = put_front or rk == 'front'
                t += L + rng.uniform(*prof['gap']) if put_front else 3.0
    # the block interiors: rows of houses lined up with the nearest road, alleys between, every one within REACH of a road
    if prof.get('interior'):
        REACH = 42.0
        allroads = unary_union([g for k, g in roads])
        x0, y0, x1, y1 = D.bounds
        step = 3.0
        anchors = [(x0 + i * step + rng.uniform(-1, 1), y0 + j * step + rng.uniform(-1, 1))
                   for i in range(int((x1 - x0) / step)) for j in range(int((y1 - y0) / step))]
        rng.shuffle(anchors)
        rtree = STRtree([g for k, g in roads])
        for (lr, dr, kind_) in prof['sizes']:   # terraces everywhere first, then smaller houses in what's left, sheds last
            for (px, py) in anchors:
                q = Point(px, py)
                if not inside.contains(q):
                    continue
                near_r = [roads[j][1] for j in rtree.query(q.buffer(REACH))]
                if not near_r:
                    continue
                r = min(near_r, key=lambda g: g.distance(q))
                if r.distance(q) > REACH:
                    continue
                t = r.project(q)
                a, b = r.interpolate(max(0, t - 1)), r.interpolate(min(r.length, t + 1))
                angs = [math.atan2(b.y - a.y, b.x - a.x)]
                nb = [placed[j] for j in PT[0].query(q.buffer(12))]
                if nb:   # or lined up with the nearest house: infill grows off its neighbours
                    h = min(nb, key=lambda p_: p_.distance(q)).minimum_rotated_rectangle
                    c_ = list(h.exterior.coords)
                    e_ = max(range(4), key=lambda i: math.dist(c_[i], c_[i + 1]))
                    angs.append(math.atan2(c_[e_ + 1][1] - c_[e_][1], c_[e_ + 1][0] - c_[e_][0]))
                for ang in angs:
                    ux, uy, vx, vy = math.cos(ang), math.sin(ang), -math.sin(ang), math.cos(ang)
                    L, dep = rng.uniform(*lr), rng.uniform(*dr)
                    pts = [(px - ux * L / 2 - vx * dep / 2, py - uy * L / 2 - vy * dep / 2), (px + ux * L / 2 - vx * dep / 2, py + uy * L / 2 - vy * dep / 2),
                           (px + ux * L / 2 + vx * dep / 2, py + uy * L / 2 + vy * dep / 2), (px - ux * L / 2 + vx * dep / 2, py - uy * L / 2 + vy * dep / 2)]
                    poly = Polygon(pts)
                    if free(poly, pad=prof['alley'] / 2) and poly.distance(allroads) < REACH:
                        new_polys.append(poly)
                        if len(new_polys) % 200 == 0:
                            NT[0] = None
                        st_ = _pick(rng, prof['storeys']) if kind_ != 'shed' else 1
                        edits.append({'op': 'add building', 'kind': kind_, 'pts': [[round(x, 1), round(y, 1)] for x, y in pts], 'storeys': st_, 'note': prof['note']})
                        break
    # the towers away from the main roads come down (a few stay)
    st = (G.get('storeys') or {}).get(did, [])
    lowered = 0
    for i, b in enumerate(G['buildings'].get(did, [])):
        if i < len(st) and st[i] >= 3 and len(b) > 3 and b[0] in ('front', 'back'):
            p = Polygon(b[1:]).buffer(0)
            if min((m.distance(p) for m in mains), default=99) > 25 and rng.random() > prof['tall_keep']:
                q = p.representative_point()
                edits.append({'op': 'set storeys', 'at': [round(q.x, 1), round(q.y, 1)], 'kind': b[0], 'storeys': 2, 'note': prof['note']})
                lowered += 1
    cov0 = unary_union(existing).area / D.area
    cov1 = unary_union(existing + new_polys).area / D.area
    return edits, {'added': len(new_polys), 'lowered': lowered, 'coverage': f'{cov0:.0%} -> {cov1:.0%}'}


if __name__ == '__main__':
    did = sys.argv[1]
    s = open(os.path.join(ROOT, 'web', 'gidi-data.js')).read()
    G = json.loads(s[s.index('{'):s.rstrip().rstrip(';').rindex('}') + 1])
    edits, rep = plan(G, did, PROFILES[did])
    print(rep)
    if '--dry' not in sys.argv:
        p = os.path.join(ROOT, 'web', 'hand', did + '.json')
        H = json.load(open(p))
        H['edits'] = [e for e in H.get('edits', []) if e.get('note') != PROFILES[did]['note']] + edits   # run again: replaces its own
        json.dump(H, open(p, 'w'), separators=(',', ':'), ensure_ascii=False)
        print('wrote', len(edits), 'edits to', p)
