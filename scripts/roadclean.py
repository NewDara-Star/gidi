# Rule-based clean-up of the baked road network, run by bake_web.py before the civic layer.
# Fixes what scripts/audit3d.py finds (D, R5, R1, R4, R2, R3), using the same tests as the audit.
# Buildings never move; a road is never extended through one (0.5 m clearance). Deterministic.
import math
from collections import Counter
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union, substring, nearest_points
from shapely import segmentize
from shapely.strtree import STRtree

WIDTH = {'main': 14.0, 'street': 7.0, 'lane': 3.5, 'path': 2.5, 'exp': 30.0, 'art': 18.0, 'bridge': 22.0}  # blender/city.py
RANK = {'path': 0, 'lane': 1, 'street': 2, 'main': 3, 'exp': 4, 'art': 4, 'bridge': 5}
KEYS = (('street', 'streets'), ('lane', 'lanes'), ('path', 'paths'))
MIN_PIECE = 18.0    # shortest piece worth keeping after a cut
MAX_EXTEND = 15.0   # longest extension to close a near miss
CLEAR = 0.5         # clearance from a building footprint
ON = {'D', 'R5', 'R1', 'R4', 'R2'}  # which rules run (for testing)
SHIFT = 40.0         # furthest a vertex is slid ashore
ISLAND = 150.0       # pieces of cut roads under this length, joined to nothing, are dropped
STILT_REACH = 30.0  # water this near a stilt house counts as boardwalk
DEBUG = False
CANALS = True       # canals count as water for rule 2


def lines_of(g):
    """The LineString pieces of any geometry, in order."""
    if g.is_empty:
        return []
    if g.geom_type == 'LineString':
        return [g]
    return [s for p in getattr(g, 'geoms', []) for s in lines_of(p)]


def rpts(g):
    return [[round(x, 1), round(y, 1)] for x, y in g.coords]


def clean(out, water_poly):
    skipped = []
    stats = Counter()
    joins = []   # new road ends that should sit exactly on another road

    # ---- gather every road as a record
    R = []
    def rec(k, d, name, pts, src=None):
        return dict(k=k, w=WIDTH[k], d=d, name=name, pts=pts, g=LineString(pts), src=src, mod=False)
    for kind, key in KEYS:
        for d, lst in (out.get(key) or {}).items():
            for pts in lst:
                if len(pts) >= 2:
                    R.append(rec(kind, d, None, pts))
    for mm in out['mains']:
        R.append(rec('main', mm.get('d'), mm.get('name'), mm['pts'], mm))
    for a in out['arterials']:
        R.append(rec(a['cls'], None, a['name'], a['pts'], a))
    for n, r in enumerate(R):
        r['uid'] = n   # lineage: every piece cut from a road keeps its uid

    # where roads meet now: (uid, uid, point). The rules must not leave any of these apart (see the end).
    meet = []
    real0 = [r for r in R if r['k'] != 'path']
    t0 = STRtree([r['g'] for r in real0])
    for r in real0:
        for j in t0.query(r['g'].buffer(0.3)):
            o = real0[j]
            if o['uid'] > r['uid'] and o['g'].distance(r['g']) < 0.3:
                x = o['g'].intersection(r['g'])
                p = x.representative_point() if not x.is_empty else nearest_points(r['g'], o['g'])[0]
                meet.append((r['uid'], o['uid'], (p.x, p.y)))
    alias = {}

    def lesser(r, o):
        """Is r the one to give way to o? Equal rank: the shorter road gives way."""
        if RANK[r['k']] != RANK[o['k']]:
            return RANK[r['k']] < RANK[o['k']]
        return (r['g'].length, r['d'] or '') < (o['g'].length, o['d'] or '')

    def movable(r):
        return r['k'] in ('street', 'lane', 'main')

    def piece(r, geom, **kw):
        """New records from a clipped geometry of r (same kind, district, name)."""
        res = []
        for s in lines_of(geom):
            if s.length < 0.5:
                continue
            n = dict(r, pts=rpts(s), g=LineString(rpts(s)), mod=True, **kw)
            if r['src'] is not None and r['k'] == 'main':
                n['src'] = dict(r['src'], pts=n['pts'])
            res.append(n)
        return res

    # ---- buildings, water and decks (the audit's definitions)
    bpolys, stilts = [], []
    for lst in out.get('buildings', {}).values():
        for b in lst:
            if len(b) > 3:
                p = Polygon(b[1:])
                bpolys.append(p if p.is_valid else p.buffer(0))
                if b[0] == 'stilt':
                    stilts.append(bpolys[-1])
    btree = STRtree(bpolys)

    def hits_building(line):
        return any(bpolys[j].distance(line) < CLEAR for j in btree.query(line.buffer(CLEAR + 1)))

    deck_base = [(LineString(s['pts']), s.get('width', 8) / 2) for s in out.get('structures', [])
                 if s['kind'] in ('flyover', 'ramp', 'footbridge', 'skywalk', 'jetty')]
    deck_base += [(LineString(a['pts']), WIDTH['bridge'] / 2) for a in out['arterials'] if a['cls'] == 'bridge']
    deck_base += [(LineString(b), 1.5) for b in out.get('boardwalks', [])]
    decks = [g.buffer(w) for g, w in deck_base]
    wet = [water_poly]
    if CANALS:
        wet += [LineString(c['pts']).buffer(c.get('width', 4.0) / 2) for c in out.get('canals', [])]
    wet = unary_union(wet)
    if stilts:  # the stilt village stands on the water: its roads are its boardwalks, not roads to clip
        wet = wet.difference(unary_union(stilts).buffer(STILT_REACH))
    wet_eff = {}
    for w in (WIDTH['main'], WIDTH['street'], WIDTH['lane']):
        wet_eff[w] = wet.difference(unary_union([d.buffer(w / 2 + 2) for d in decks])) if decks else wet

    def tree_of(rs):
        return STRtree([r['g'] for r in rs])

    # ---- 1. D: the same road listed twice
    real = [r for r in R if r['k'] != 'path' and r['k'] != 'bridge']
    t = tree_of(real)
    drop = set()
    for i, r in enumerate(real if 'D' in ON else []):
        if i in drop or not movable(r):
            continue
        rev = LineString(r['g'].coords[::-1])
        for j in sorted(t.query(r['g'].buffer(r['w'] / 2))):
            o = real[j]
            if j <= i or j in drop or o['k'] != r['k'] or not movable(o):
                continue
            if o['g'].equals_exact(r['g'], 0.5) or o['g'].equals_exact(rev, 0.5):
                drop.add(j)  # keep the first, record the other district
                alias[o['uid']] = r['uid']
                if r['k'] == 'main' and o['d'] and o['d'] != r['d']:
                    also = r['src'].setdefault('also', [])
                    if o['d'] not in also:
                        also.append(o['d'])
                stats['D'] += 1
    dead = {id(real[j]) for j in drop}
    R = [r for r in R if id(r) not in dead]

    # ---- 2. R5: a road over water that is not on a deck. First slide a shore-hugging road back onto
    # the land (vertices moved at most SHIFT m; the shore here is crude, the road was meant to be dry),
    # then clip what is still over water and drop the leftovers.
    new = []
    for r in R:
        if not (movable(r) and 'R5' in ON):
            new.append(r)
            continue
        we = wet_eff[r['w']]
        on = r['g'].intersection(we)
        if on.length <= 3:
            new.append(r)
            continue
        stats['R5'] += 1
        g = r['g']
        zone = we.buffer(r['w'] / 2 + 1.5)
        shifted = segmentize(g, 10.0)
        moved = False
        cs = []
        last = len(shifted.coords) - 1
        for n, (x, y) in enumerate(shifted.coords):
            P = Point(x, y)
            if (zone if 0 < n < last else we).contains(P):   # a road end stays put unless it is in the water itself
                q = nearest_points(P, zone.boundary)[1]
                if q.distance(P) <= SHIFT:
                    cs.append((q.x, q.y))
                    moved = True
                    continue
            cs.append((x, y))
        if moved:
            cand = LineString(cs).simplify(0.5)
            if hits_building(cand) and not hits_building(g):
                skipped.append(f"R5 {r['k']} {r['name'] or r['d']} near ({on.representative_point().x:.0f}, {on.representative_point().y:.0f}): {on.length:.0f} m on water, sliding it ashore would cross a building")
                new.append(r)
                continue
            stats['R5_shift'] += 1
            g = cand
        left = g.intersection(we)
        stats['R5_m'] += round(left.length) if left.length > 3 else 0
        if left.length > 3:
            new += [p for p in piece(r, g.difference(we)) if p['g'].length >= MIN_PIECE]
        else:
            new += piece(r, g)
    R = new

    # ---- 3. R1: a lesser road runs along a bigger one: remove the overlapping stretch
    for _ in range(2 if 'R1' in ON else 0):
        real = [r for r in R if r['k'] not in ('path', 'bridge')]
        t = tree_of(real)
        new = []
        for r in R:
            if not movable(r):
                new.append(r)
                continue
            zone = None
            for j in sorted(t.query(r['g'].buffer(r['w'] / 2 + 20))):
                o = real[j]
                if o is r or not lesser(r, o):
                    continue
                if r['g'].equals_exact(o['g'], 0.5):
                    continue
                zo = o['g'].buffer((o['w'] + r['w']) / 2 * 0.7)
                if r['g'].intersection(zo).length > max(o['w'], r['w']) * 1.6 + 6:
                    zone = zo if zone is None else zone.union(zo)
            if zone is None:
                new.append(r)
                continue
            stats['R1'] += 1
            new += [p for p in piece(r, r['g'].difference(zone)) if p['g'].length >= MIN_PIECE]
        R = new

    # ---- 4. R4: knife-edge crossing: cut the lesser road at the crossing so it ends there
    def heading(g, c):
        s0 = g.project(c)
        a, b = g.interpolate(max(0, s0 - 3)), g.interpolate(min(g.length, s0 + 3))
        return math.atan2(b.y - a.y, b.x - a.x)

    for _ in range(3 if 'R4' in ON else 0):
        real = [r for r in R if r['k'] not in ('path', 'bridge')]
        t = tree_of(real)
        cuts = {}
        for i, r in enumerate(real):
            for j in sorted(t.query(r['g'])):
                o = real[j]
                if o is r or not movable(r) or not lesser(r, o) or id(r) in cuts:
                    continue
                if r['g'].equals_exact(o['g'], 0.5):
                    continue
                x = r['g'].intersection(o['g'])
                pts = [x] if x.geom_type == 'Point' else [g for g in getattr(x, 'geoms', []) if g.geom_type == 'Point']
                for c in pts:
                    if any(dk.distance(c) < 3 for dk in decks):
                        continue
                    if any(Point(e).distance(c) < 1.0 for g in (r['g'], o['g']) for e in (g.coords[0], g.coords[-1])):
                        continue
                    ang = abs((heading(r['g'], c) - heading(o['g'], c) + math.pi / 2) % math.pi - math.pi / 2)
                    if math.degrees(ang) < 25:
                        cuts[id(r)] = c
                        break
        if not cuts:
            break
        new = []
        for r in R:
            c = cuts.get(id(r))
            if c is None:
                new.append(r)
                continue
            joins.append((round(c.x, 1), round(c.y, 1)))
            s0 = r['g'].project(c)
            keep = substring(r['g'], 0, s0) if s0 >= r['g'].length - s0 else substring(r['g'], s0, r['g'].length)
            stats['R4'] += 1
            new += piece(r, keep)
        R = new

    # ---- 5/6. R2 and R3 at the free ends: extend a near miss, trim an overshoot
    def fix_ends(R):
        real = [r for r in R if r['k'] != 'path']
        t = tree_of(real)
        ends = Counter()
        for r in real:
            for p in (r['g'].coords[0], r['g'].coords[-1]):
                ends[(round(p[0], 1), round(p[1], 1))] += 1
        new = []
        for r in R:
            if not movable(r):
                new.append(r)
                continue
            cs = [tuple(c) for c in r['g'].coords]
            changed = False
            for first in (True, False):
                p, q = (cs[0], cs[1]) if first else (cs[-1], cs[-2])
                if ends[(round(p[0], 1), round(p[1], 1))] > 1:
                    continue
                P = Point(p)
                near = [real[j] for j in sorted(t.query(P.buffer(12))) if real[j] is not r]
                if any(o['g'].distance(P) < 0.5 for o in near):
                    continue
                tail = LineString([p, q])
                best = None
                for o in near:
                    if o['k'] in ('bridge',):
                        continue
                    d = o['g'].distance(P)
                    if tail.intersects(o['g']) and 1.0 < d < 10 + o['w'] / 2:
                        kind = 'R3'
                    elif 0.5 < d < o['w'] / 2 + min(MAX_EXTEND, 8) and not tail.intersects(o['g']):   # the gap past the other road's edge
                        kind = 'R2'
                    else:
                        continue
                    if best is None or d < best[0]:
                        best = (d, kind, o)
                if best is None:
                    continue
                d, kind, o = best
                if kind == 'R3':
                    x = tail.intersection(o['g'])
                    xs = [g for g in (x.geoms if hasattr(x, 'geoms') else [x]) if g.geom_type == 'Point']
                    if not xs:
                        continue
                    c = min(xs, key=lambda g: g.distance(P))
                    c = Point(round(c.x, 1), round(c.y, 1))
                    joins.append((c.x, c.y))
                    if first:
                        cs[0] = (c.x, c.y)
                    else:
                        cs[-1] = (c.x, c.y)
                    changed = True
                    stats['R3'] += 1
                else:
                    c = nearest_points(P, o['g'])[1]
                    c = Point(round(c.x, 1), round(c.y, 1))
                    ext = LineString([p, (c.x, c.y)])
                    we = wet_eff[r['w']]
                    # water in the way only if both ends are dry (a road already on the water may be joined there)
                    swim = ext.intersection(we).length > 1.0 and we.distance(Point(p)) > 0.5 and we.distance(c) > 0.5
                    if hits_building(ext) or swim:
                        skipped.append(f"R2 {r['k']} {r['name'] or r['d']} end ({p[0]:.0f}, {p[1]:.0f}) left {d:.1f} m short of {o['name'] or o['k']}: " + ('a building' if hits_building(ext) else 'water') + ' in the way')
                        continue
                    joins.append((c.x, c.y))
                    if first:
                        cs.insert(0, (c.x, c.y))
                    else:
                        cs.append((c.x, c.y))
                    changed = True
                    stats['R2'] += 1
            if changed and len(cs) >= 2 and LineString(cs).length > 0.5:
                new += piece(r, LineString(cs))
            else:
                new.append(r)
        return new

    if 'R2' in ON:
        R = fix_ends(R)
        R = fix_ends(R)

    # ---- weld: the road a new end lands on gets a vertex there, so rounding to 0.1 m cannot leave a gap
    allr = [r for r in R if r['k'] != 'path']
    t = tree_of(allr)
    for (x, y) in joins:
        P = Point(x, y)
        for j in sorted(t.query(P.buffer(0.5))):
            o = allr[j]
            if o['g'].distance(P) >= 0.3 or any(abs(cx - x) < 0.05 and abs(cy - y) < 0.05 for cx, cy in o['g'].coords):
                continue
            cs = list(o['g'].coords)
            at = min(range(len(cs) - 1), key=lambda i: LineString(cs[i:i + 2]).distance(P))
            cs.insert(at + 1, (x, y))
            o['g'] = LineString(cs)
            o['pts'] = [list(c) if isinstance(c, tuple) else c for c in cs]
            if o['src'] is not None:
                o['src']['pts'] = o['pts']
            stats['weld'] += 1

    # ---- islands: a few cut-off pieces left by the rules, joined to nothing, are dropped
    everything = R
    t = tree_of(everything)
    par = list(range(len(everything)))
    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for i, r in enumerate(everything):
        for j in t.query(r['g'].buffer(0.3)):
            if j != i and everything[j]['g'].distance(r['g']) < 0.3:
                par[find(i)] = find(j)
    comp = {}
    for i, r in enumerate(everything):
        comp.setdefault(find(i), []).append(i)
    gone = set()
    for ids in comp.values():
        if all(everything[i]['mod'] and everything[i]['k'] in ('street', 'lane', 'main') for i in ids) and sum(everything[i]['g'].length for i in ids) < ISLAND:
            gone |= set(ids)
            stats['island'] += 1
            if DEBUG:
                print('island', [(everything[i]['k'], everything[i]['d'], round(everything[i]['g'].length), [round(c) for c in everything[i]['g'].coords[0]]) for i in ids])
    R = [r for i, r in enumerate(R) if i not in gone]

    # ---- junctions the rules broke: two roads that met before and no longer do are joined again, the nearer
    # end of the cut road run straight back to the other road (never through a building). Owner's complaint was
    # places that don't connect; the clean-up must not make new ones.
    pieces = {}
    for r in R:
        if r['k'] != 'path':
            pieces.setdefault(r['uid'], []).append(r)
    for a, b, J in meet:
        a, b = alias.get(a, a), alias.get(b, b)
        if a == b or a not in pieces or b not in pieces:
            continue
        if any(p['g'].distance(q['g']) < 0.5 for p in pieces[a] for q in pieces[b]):
            continue
        P = Point(J)
        # the movable side gives the end; if both can move, the lesser road
        sides = [(a, b), (b, a)]
        sides = [(x, y) for x, y in sides if movable(pieces[x][0])]
        if len(sides) == 2 and not lesser(pieces[sides[0][0]][0], pieces[sides[1][0]][0]):
            sides.reverse()
        done = False
        for x, y in sides:
            # ends of x within 200 m of where they met, nearest the other road first; the first that reaches it
            # (60 m at most) without crossing a building is run straight onto it
            cands = []
            for r in pieces[x]:
                for i in (0, -1):
                    E_ = Point(r['g'].coords[i])
                    if E_.distance(P) > 200:
                        continue
                    for o in pieces[y]:
                        cands.append((o['g'].distance(E_), E_.distance(P), r, i, nearest_points(E_, o['g'])[1]))
            pick = None
            for dq, _, r, i, q in sorted(cands, key=lambda c: (c[0], c[1])):
                if dq > 60:
                    break
                q = (round(q.x, 1), round(q.y, 1))
                ext = LineString([r['g'].coords[i], q])
                if not hits_building(ext) and (ext.intersection(wet_eff[r['w']]).length <= 1.0 or wet_eff[r['w']].contains(Point(q))):
                    # a junction out on the water was never real, unless the road it meets was kept there (see R5 skips)
                    pick = (r, i, q)
                    break
            if pick is None:
                continue
            r, i, q = pick
            cs = [tuple(c) for c in r['g'].coords]
            cs = [q] + cs if i == 0 else cs + [q]
            r['g'] = LineString(cs); r['pts'] = rpts(r['g'])
            if r['src'] is not None and r['k'] == 'main':
                r['src'] = dict(r['src'], pts=r['pts'])
            stats['rejoin'] += 1
            done = True
            break
        if not done:
            skipped.append(f"junction {pieces[a][0]['name'] or pieces[a][0]['k']} / {pieces[b][0]['name'] or pieces[b][0]['k']} near ({J[0]:.0f}, {J[1]:.0f}) is broken and could not be rejoined")

    # ---- kinks: a cut end that doubles back on itself (a hook of a few metres) is straightened. Only bends sharper
    # than 135 degrees on a leg under 20 m go; the ends of a road never move, so its junctions hold.
    for r in R:
        if not r['mod'] or r['k'] == 'path':
            continue
        cs = [tuple(c) for c in r['g'].coords]
        gone_any = False
        changed = True
        while changed and len(cs) > 2:
            changed = False
            for i in range(1, len(cs) - 1):
                (ax, ay), (bx, by), (cx, cy) = cs[i - 1], cs[i], cs[i + 1]
                l1, l2 = math.hypot(bx - ax, by - ay), math.hypot(cx - bx, cy - by)
                if l1 < 0.05 or l2 < 0.05:
                    del cs[i]; changed = gone_any = True; break
                turn = abs((math.atan2(cy - by, cx - bx) - math.atan2(by - ay, bx - ax) + math.pi) % (2 * math.pi) - math.pi)
                if math.degrees(turn) > 135 and min(l1, l2) < 20:
                    del cs[i]; changed = gone_any = True; break
        if gone_any:
            r['g'] = LineString(cs); r['pts'] = rpts(r['g'])
            if r['src'] is not None and r['k'] == 'main':
                r['src'] = dict(r['src'], pts=r['pts'])
            stats['kink'] += 1

    # ---- write back, keeping the order and the original point lists of roads we did not touch
    for kind, key in KEYS:
        for d in (out.get(key) or {}):
            out[key][d] = []
    out['mains'] = []
    for r in R:
        if r['k'] in ('street', 'lane', 'path'):
            out[dict(KEYS)[r['k']]].setdefault(r['d'], []).append(r['pts'])
        elif r['k'] == 'main':
            out['mains'].append(r['src'])
    return stats, skipped
