# Junctions, run by bake_web.py after the road clean-up and before the heights (pass 3 of the road work).
#
# Every place where main roads and arterials meet gets a kind, in out["junctions"]:
#   - "roundabout": a ring road where main roads cross (four or more arms, no arterial or expressway among them) and there
#     is room for a ring of R_MIN m or more clear of buildings, walls and plots. The ring is a main road named after the
#     junction, the roads meeting it are cut at the ring, and streets, lanes and paths inside stop at it, the way the
#     generator builds its roundabouts (Hunter, Market, Oladipo Road). Roundabouts stay SPACING m apart.
#   - "signals": traffic lights, where a main road meets an arterial or an expressway (Lagos's expressways have them),
#     and at a main-road crossing with no room for a ring.
#   - "give way": a main road ending at another main road in a T.
# A roundabout entry carries the ring's centreline radius "r" and its island's "island_r" for the 3D kit; every entry
# carries its position, the roads that meet and the bearings of its arms (degrees, map axes, y south).
import math
from collections import Counter
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union, nearest_points
from shapely.strtree import STRtree

R_MIN, R_MAX = 12.0, 22.0
R_WANT = 16.0               # a proper Lagos roundabout: an island of 11.5 m
CLEARABLE = ('front', 'back', 'kiosk', 'shed', 'stalls', 'strip', 'generator', 'unfinished house')
MAX_CLEAR = 4               # ordinary corner houses or kiosks that may make way for one   # ring centreline radius (a 7 m ring round an island of 8.5 m and more)
CLEAR_B = 9.0               # building/wall edge to the ring's centreline: half a main road and a pavement
SPACING = 150.0
CLUSTER = 15.0


def lines_of(g):
    if g.is_empty:
        return []
    if g.geom_type == 'LineString':
        return [g]
    return [s for p in getattr(g, 'geoms', []) for s in lines_of(p)]


def rp(c):
    return [round(c[0], 1), round(c[1], 1)]


def junctions(out):
    report = Counter()
    # a main road that stops at an arterial's edge (its end within half the arterial's width of the centre line, touching
    # nothing else) is run on to the centre line, so the network joins them as the carriageways do
    W = {'exp': 30.0, 'art': 18.0}
    arts = [(LineString(a['pts']), W.get(a['cls'], 18.0)) for a in out['arterials'] if a['cls'] in W]
    allm = [LineString(m['pts']) for m in out['mains']]
    for k, m in enumerate(out['mains']):
        for e in (0, -1):
            E_ = Point(m['pts'][e])
            if any(g.distance(E_) < 0.5 for i, g in enumerate(allm) if i != k):
                continue
            for a, w in arts:
                d = a.distance(E_)
                if 0.5 < d <= w / 2 + 2:
                    q = nearest_points(E_, a)[1]
                    q = [round(q.x, 1), round(q.y, 1)]
                    m['pts'] = [q] + m['pts'] if e == 0 else m['pts'] + [q]
                    report['ran on to an arterial'] += 1
                    break
    R = [('main', m.get('name') or '', LineString(m['pts'])) for m in out['mains']]
    R += [(a['cls'], a['name'], LineString(a['pts'])) for a in out['arterials'] if a['cls'] != 'bridge']
    tree = STRtree([g for k, n, g in R])
    decks = unary_union([LineString(s['pts']).buffer(s.get('width', 8) / 2 + 4) for s in out.get('structures', [])
                         if s['kind'] in ('flyover', 'ramp', 'skywalk')]
                        + [LineString(a['pts']).buffer(15) for a in out['arterials'] if a['cls'] == 'bridge'])

    # where they meet: crossings and ends on another road, clustered
    pts = []
    for i, (k, n, g) in enumerate(R):
        for j in tree.query(g.buffer(0.5)):
            if j <= i or R[j][2].distance(g) > 0.5:
                continue
            x = g.intersection(R[j][2])
            if x.is_empty:   # touching, not crossing: where they come closest
                x = nearest_points(g, R[j][2])[0]
            pts += [p for p in getattr(x, 'geoms', [x]) if p.geom_type == 'Point']
    cl = []
    for p in pts:
        for c in cl:
            if c[0].distance(p) < CLUSTER:
                c[1].append(p)
                break
        else:
            cl.append([p, [p]])

    # what stands round each: buildings, walls, plots
    BL = [(d, i, b[0], Polygon(b[1:]).buffer(0)) for d, L in out.get('buildings', {}).items() for i, b in enumerate(L) if len(b) > 3]
    btree = STRtree([x[3] for x in BL])
    obst = []
    obst += [LineString(w) for L in (out.get('walls') or {}).values() for w in L if len(w) > 1] if isinstance(out.get('walls'), dict) else []
    obst += [Polygon(p['pts']).exterior for L in (out.get('parcels') or {}).values() for p in L if len(p.get('pts', [])) > 3] if isinstance(out.get('parcels'), dict) else []
    otree = STRtree(obst)

    def room(c):
        near = otree.query(c.buffer(60)) if obst else []
        hard = [obst[j].distance(c) for j in near] + [BL[j][3].distance(c) for j in btree.query(c.buffer(60)) if BL[j][2] not in CLEARABLE]
        return min(hard or [60.0])

    def plan(c):
        """The ring that fits: the largest radius up to R_WANT clearing at most MAX_CLEAR ordinary buildings; (r, to clear) or None."""
        hard = room(c)
        for r in (R_WANT, 15.0, 14.0, 13.0, R_MIN):
            if hard - CLEAR_B < r:
                continue
            gone = [j for j in btree.query(c.buffer(r + CLEAR_B)) if BL[j][2] in CLEARABLE and BL[j][3].distance(c) < r + CLEAR_B]
            if len(gone) <= MAX_CLEAR:
                return r, gone
        return None

    rings_done = []   # existing roundabouts (the generator's), then the new ones
    J = []
    for m in out['mains']:
        if (m.get('name') or '').endswith('Roundabout'):
            g = LineString(m['pts'])
            c = g.centroid
            r = sum(Point(p).distance(c) for p in m['pts']) / len(m['pts'])
            rings_done.append(c)
            J.append({'kind': 'roundabout', 'name': m['name'], 'x': round(c.x, 1), 'y': round(c.y, 1), 'r': round(r, 1), 'island_r': round(r - 4.5, 1), 'new': False})

    cands = []
    for c, ps in cl:
        if decks.contains(c) or any(c.distance(q) < 40 for q in rings_done):
            continue
        arms = []
        for j in tree.query(c.buffer(3)):
            k, n, g = R[j]
            if g.distance(c) > 3:
                continue
            t = g.project(c)
            for sgn in (1, -1):
                t2 = t + sgn * 25
                if 0 <= t2 <= g.length:
                    q = g.interpolate(t2)
                    arms.append((k, n, round(math.degrees(math.atan2(q.y - c.y, q.x - c.x))) % 360))
        names = sorted(set(a[1] for a in arms if a[1]))
        if len(arms) <= 2 or (len(names) <= 1 and len(arms) <= 2):
            continue   # one road going on under another name: not a junction
        kinds = Counter(a[0] for a in arms)
        cands.append((c, arms, names, kinds))

    # roundabouts first, the roomiest first
    def spread(arms):
        """The smallest angle between two arms: a ring only works when the roads come in from clearly different sides."""
        b = sorted(a[2] for a in arms)
        return min(((b[(i + 1) % len(b)] - b[i]) % 360) for i in range(len(b))) if len(b) > 1 else 0

    # nor on a flyover's ramps: those need their road straight and level for ~100 m each side (scripts/roadz.py)
    fly = unary_union([LineString(s['pts']) for s in out.get('structures', []) if s['kind'] == 'flyover'])
    plans = {id(c): plan(c) for c, arms, names, kinds in cands
             if len(arms) >= 4 and set(kinds) == {'main'} and (fly.is_empty or fly.distance(c) > 180) and spread(arms) >= 35}
    order = sorted(cands, key=lambda x: (len((plans.get(id(x[0])) or (0, [0] * 9))[1]), -(plans.get(id(x[0])) or (0,))[0]))
    made = set()
    clear = set()
    for c, arms, names, kinds in order:
        if plans.get(id(c)):
            r, gone = plans[id(c)]
            if all(c.distance(q) >= SPACING for q in rings_done):
                clear |= set(gone)
                report['cleared'] += len(gone)
                made.add(id(c))
                rings_done.append(c)
                longest = max(names, key=lambda n: sum(g.length for k, nn, g in R if nn == n)) if names else 'Junction'
                base = longest.split(' ')[0]
                nm = f"{base} Roundabout"
                if any(j.get('name') == nm for j in J):
                    nm = f"{names[-1].split(' ')[0]} Roundabout" if names else nm
                J.append({'kind': 'roundabout', 'name': nm, 'x': round(c.x, 1), 'y': round(c.y, 1), 'r': round(r, 1), 'island_r': round(r - 4.5, 1),
                          'roads': names, 'arms': sorted(a[2] for a in arms), 'new': True})
    for c, arms, names, kinds in cands:
        if id(c) in made:
            continue
        big = kinds.get('art', 0) + kinds.get('exp', 0)
        if big and kinds.get('main', 0):
            kind = 'signals'
        elif big:
            continue   # arterials meeting each other: their own interchanges (the Hub's) or continuations
        elif len(arms) >= 4:
            kind = 'signals'
        else:
            kind = 'give way'
        J.append({'kind': kind, 'x': round(c.x, 1), 'y': round(c.y, 1), 'roads': names, 'arms': sorted(a[2] for a in arms)})

    # the corner houses that make way for the rings
    if clear:
        drop = {}
        for j in clear:
            drop.setdefault(BL[j][0], set()).add(BL[j][1])
        for d, idx in drop.items():
            n = len(out['buildings'][d])
            keep = [i for i in range(n) if i not in idx]
            for key in ('buildings', 'storeys', 'styles'):
                arr = (out.get(key) or {}).get(d)
                if arr is not None and len(arr) == n:
                    out[key][d] = [arr[i] for i in keep]

    # build the new rings: cut every way at the ring, the ring a main road
    for j in [j for j in J if j.get('new')]:
        C = Point(j['x'], j['y'])
        r = j['r']
        disc = C.buffer(r, quad_segs=16)
        ends = []

        def cut(pts):
            g = LineString(pts)
            if g.distance(C) >= r:
                return [pts]
            res = []
            for s in lines_of(g.difference(disc)):
                if s.length < 4:
                    continue
                cs = [tuple(x) for x in s.coords]
                for e in (0, -1):   # an end on the ring: put it exactly on the circle, and note it for the ring
                    if abs(Point(cs[e]).distance(C) - r) < 0.5:
                        a = math.atan2(cs[e][1] - C.y, cs[e][0] - C.x)
                        cs[e] = (round(C.x + r * math.cos(a), 1), round(C.y + r * math.sin(a), 1))
                        ends.append(cs[e])
                res.append([list(x) for x in cs])
            report['cut'] += 1
            return res

        new_m = []
        for m in out['mains']:
            for p in cut(m['pts']):
                new_m.append(dict(m, pts=p))
        for key in ('streets', 'lanes'):
            for d, L in (out.get(key) or {}).items():
                out[key][d] = [p for q in L for p in cut(q)]
        for d, L in (out.get('paths') or {}).items():
            nl = []
            for q in L:
                pts = q['pts'] if isinstance(q, dict) else q
                for p in cut(pts):
                    nl.append(dict(q, pts=p) if isinstance(q, dict) else p)
            out['paths'][d] = nl
        # the ring: 64 points round, plus every arm's end, in order
        ring = [(round(C.x + r * math.cos(2 * math.pi * k / 64), 1), round(C.y + r * math.sin(2 * math.pi * k / 64), 1)) for k in range(64)]
        ring = sorted(set(ring + ends), key=lambda p: math.atan2(p[1] - C.y, p[0] - C.x))
        ring = ring + [ring[0]]
        d = None
        for m in out['mains']:
            if LineString(m['pts']).distance(C) < r + 1:
                d = m.get('d')
                break
        new_m.append({'name': j['name'], 'pts': [list(p) for p in ring], 'd': d})
        out['mains'] = new_m
        j['arms_n'] = len(ends)
        report['roundabouts'] += 1
    for j in J:
        j.pop('new', None)
        report[j['kind']] += 1
    out['junctions'] = J
    return report
