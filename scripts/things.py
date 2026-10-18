"""Things the 3D kit used to invent, now in the map data (owner, 17 Oct 2026: "everything should be in the data... even the
grain of sand... if everything is in the data, we'll be able to better place stuff").

The kit placed these by its own rules, tile by tile, where the board could not see them, the checks could not test them
and nobody could move them. The same rules now run here, once, on the finished map, and the kit only draws what they put:

- out["monuments"] gains the ones the kit placed by rule: a statue, clock tower, sculpture or LED screen at a corner of
  the main-road junctions (up to four a district, by its character), welcome arches where a main road enters a district,
  the point landmarks (Coconut Beach's arch, the Hunter at his roundabout), murals in the Hub, the Maze and the Heights,
  and billboards along the main roads (every ~350 m). A district with monuments placed by hand keeps only those (as the
  kit did); "rule": 1 marks the ones placed here.
- out["furniture"] gains the road signs: a direction sign 30 m before every main-road and arterial junction (where the
  crossing road goes, left and right), a speed limit 25 m after it, no-parking discs by the markets, and gantries over
  the expressways and bridges every 800 m.
- out["things"]: everything else that stands somewhere, one entry each: {"k": kind, "x", "y", "a": heading (degrees on
  the map's axes, y south), "d": district or "bush", and what the kit needs to draw it: "c" condition, "s" style, "p"
  people aboard, "cab"}. Parked vehicles at the road edges; buses packed in the motor parks, lorries and container trucks
  in their parks; people standing in the markets, motor parks and under the bridges; reach stackers and forklifts in the
  container yard; ferries, water buses and dredgers; canoes tied along Water Town's boardwalks; the three trains on the
  line; the rail market's stalls between the tracks.
- out["life"]: what moves. Traffic and people walking are not fixed things (in the game they move), so the data holds
  how much of each and what kind, by district character and road (the kit draws a still of them from this): people per
  100 m of frontage, the traffic mix, the gap between vehicles, how well off (vehicle condition). "roads": {road id:
  {...}} overrides any of it for one road.

The draws are seeded by place, as the kit's were (same Rng), so the bake stays byte-identical. Work is done in the kit's
frame (y north) with the kit's own geometry, then turned back to the map's frame, so nothing changes in the porting.
Hand edits: "add thing", "move thing", "delete thing" (scripts/hand.py apply_thing_edits); the furniture and monument
edits as before (applied once these exist: hand.apply_late_furniture).
"""
import hashlib
import math
import random

from shapely.geometry import Point, Polygon
from shapely.prepared import prep
from shapely.strtree import STRtree

from shapely.geometry import LineString
from shapely.ops import unary_union

import cross_sections as XS
import ground as GU

CHARACTER = {'maze': 'dense', 'hub': 'dense', 'jungle': 'dense', 'foodgate': 'dense', 'bazaar': 'dense',
             'railside': 'sprawl', 'frontier': 'sprawl', 'border': 'sprawl', 'oldisland': 'old_island', 'oldshore': 'old_island',
             'estate': 'elite', 'heights': 'elite', 'capital': 'civic', 'watertown': 'waterfront', 'port': 'port'}
ART_W = {'exp': 30.0, 'art': 18.0, 'bridge': 22.0}   # blender/city.py: the kit's arterial widths
SPEED = {'main': 50, 'art': 60, 'exp': 80, 'bridge': 80}
JUNCTION = {   # blender/gidi_kit/monuments.py: what stands at a main-road junction, by character
    'old_island': ['statue:masquerade', 'statue:horse_rider', 'clock_tower', 'led_board'],
    'civic': ['statue:saxophonist', 'statue:horse_rider', 'clock_tower', 'led_board'],
    'elite': ['statue:three_elders', 'sculpture', 'led_board'],
    'dense': ['led_board', 'statue:founder', 'statue:drummer', 'led_board'],
    'sprawl': ['led_board', 'statue:founder', 'clock_tower'],
    'waterfront': ['statue:masquerade', 'statue:drummer'],
    'port': ['led_board', 'sculpture'],
}
POINT_LANDMARKS = {'Coconut Beach': ('beach_arch', -math.pi / 2), 'Hunter Roundabout': ('statue:hunter', 0.0)}
WEALTH = {'elite': 0.85, 'civic': 0.55, 'dense': 0.3, 'sprawl': 0.35, 'old_island': 0.3, 'waterfront': 0.1, 'port': 0.3}
CROWD = {'dense': 30, 'old_island': 40, 'sprawl': 15, 'elite': 2, 'civic': 10, 'waterfront': 20, 'port': 10}   # per 100 m, research-street 4.3
GAP = {'main': 14, 'street': 30, 'lane': 60}   # metres between moving vehicles in a lane, about
MIX = {   # research-vehicles 8.6: shares of moving traffic by character and road class (blender/gidi_kit/vehicles.py)
    ('dense', 'main'): {'danfo': 26, 'korope': 4, 'keke': 5, 'okada': 5, 'car': 40, 'brt': 5, 'tipper': 6, 'tanker': 6, 'cart': 3, 'water': 1, 'refuse': 1, 'mixer': 1},
    ('dense', 'street'): {'danfo': 7, 'korope': 3, 'keke': 25, 'okada': 25, 'car': 30, 'tipper': 3, 'cart': 5, 'wheelbarrow': 2, 'water': 1.5, 'refuse': 0.5},
    ('old_island', 'main'): {'danfo': 20, 'car': 55, 'brt': 5, 'tanker': 5, 'tipper': 5, 'cart': 10},
    ('old_island', 'street'): {'keke': 5, 'okada': 5, 'car': 40, 'tipper': 5, 'cart': 40, 'wheelbarrow': 5},
    ('sprawl', 'main'): {'danfo': 20, 'korope': 5, 'keke': 15, 'okada': 15, 'car': 30, 'brt': 3, 'tipper': 7, 'tanker': 3, 'cart': 2},
    ('sprawl', 'street'): {'danfo': 2, 'korope': 3, 'keke': 30, 'okada': 30, 'car': 30, 'tipper': 3, 'cart': 2, 'mixer': 1.5, 'water': 2},
    ('elite', 'main'): {'danfo': 5, 'car': 80, 'brt': 5, 'tanker': 4, 'tipper': 4, 'okada': 2},
    ('elite', 'street'): {'car': 92, 'okada': 3, 'tipper': 5, 'mixer': 3, 'water': 3, 'refuse': 1},
    ('civic', 'main'): {'danfo': 15, 'car': 60, 'brt': 10, 'police': 2, 'tanker': 5, 'tipper': 5, 'cart': 3},
    ('civic', 'street'): {'danfo': 5, 'car': 70, 'police': 3, 'keke': 5, 'okada': 2, 'tipper': 5, 'cart': 3},
    ('port', 'main'): {'danfo': 10, 'car': 15, 'container': 35, 'tanker': 20, 'tipper': 15, 'brt': 3, 'okada': 2},
    ('port', 'street'): {'danfo': 10, 'car': 25, 'container': 15, 'tanker': 15, 'tipper': 20, 'okada': 5, 'keke': 5, 'cart': 5},
}
LENGTH = {'danfo': 4.8, 'korope': 3.6, 'brt': 12.2, 'keke': 2.8, 'okada': 2.1, 'car': 4.8, 'police': 5.3, 'tipper': 8.6, 'tanker': 11.5, 'cart': 3.6,
          'wheelbarrow': 1.6, 'container': 17.2, 'lorry911': 8.9, 'fire': 9.0, 'ambulance': 5.6, 'refuse': 9.4, 'mixer': 9.0, 'water': 8.6,
          'molue': 11.0, 'stacker': 11.0, 'forklift': 5.0}
WIDTH = {'danfo': 2.0, 'korope': 1.7, 'brt': 2.6, 'keke': 1.3, 'okada': 0.8, 'car': 1.8, 'police': 1.9, 'tipper': 2.5, 'tanker': 2.5, 'cart': 1.4,
         'wheelbarrow': 0.7, 'container': 2.5, 'lorry911': 2.4, 'fire': 2.5, 'ambulance': 2.0, 'refuse': 2.5, 'mixer': 2.5, 'water': 2.5,
         'molue': 2.5, 'stacker': 4.0, 'forklift': 1.4}
COMMERCIAL = {'danfo', 'korope', 'keke', 'okada', 'tipper', 'tanker', 'brt', 'cart', 'container', 'lorry911', 'refuse', 'mixer', 'water', 'molue', 'stacker', 'forklift'}
TRAIN_L = {'commuter': 20.6, 'loco': 14.0, 'coach': 18.6, 'wagon': 14.6}
DRESS = {   # blender/gidi_kit/people.py, shares by character [est, research-street 4.2]
    'dense': {'ankara': 3, 'wrapper': 3, 'buba': 2, 'tshirt': 4, 'kaftan': 1, 'hawker': 1.5, 'school': 0.8, 'agbada': 0.3},
    'old_island': {'ankara': 3, 'wrapper': 4, 'buba': 2, 'tshirt': 3, 'kaftan': 1.5, 'hawker': 2, 'agbada': 0.6, 'school': 0.6},
    'sprawl': {'ankara': 2, 'wrapper': 3, 'buba': 2, 'tshirt': 4, 'kaftan': 2, 'hawker': 1, 'school': 1.2, 'agbada': 0.3},
    'elite': {'tshirt': 4, 'ankara': 2, 'office': 3, 'kaftan': 1, 'agbada': 0.5, 'wrapper': 0.5},
    'civic': {'office': 4, 'tshirt': 3, 'ankara': 2, 'buba': 1, 'kaftan': 1, 'wrapper': 1, 'hawker': 0.8},
    'waterfront': {'tshirt': 4, 'wrapper': 3, 'ankara': 1, 'buba': 1, 'hawker': 1, 'school': 0.6},
    'port': {'tshirt': 5, 'office': 1, 'buba': 2, 'kaftan': 2, 'hawker': 1},
}


class Rng(random.Random):
    """blender/gidi_kit/core.py's Rng, exactly: random.Random seeded from any key, with weighted picks."""

    def __init__(self, *key):
        self.key = '/'.join(str(k) for k in key)
        super().__init__(int(hashlib.sha1(self.key.encode()).hexdigest()[:15], 16))

    def pick(self, items, weights=None):
        if isinstance(items, dict):
            items, weights = list(items.keys()), list(items.values())
        return self.choices(items, weights=weights, k=1)[0]

    def chance(self, p):
        return self.random() < p

    def between(self, lo, hi):
        return lo + (hi - lo) * self.random()


def condition(wealth, rng, commercial=False, parked=False):
    c = 0.25 + 0.6 * wealth + rng.between(-0.2, 0.2) - (0.2 if commercial else 0)
    return 'new' if c > 0.8 else 'worn' if c > 0.5 else 'battered' if c > 0.2 or not parked else 'wreck'


def P(p):   # the map's frame (y south) to the kit's (y north)
    return (p[0], -p[1])


def _unit(v):
    L = math.hypot(*v) or 1
    return (v[0] / L, v[1] / L)


def dist_seg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy or 1
    t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2))
    return math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy))


def _seg_cross(a, b, c, d):
    r = (b[0] - a[0], b[1] - a[1])
    q = (d[0] - c[0], d[1] - c[1])
    den = r[0] * q[1] - r[1] * q[0]
    if abs(den) < 1e-9:
        return None
    t = ((c[0] - a[0]) * q[1] - (c[1] - a[1]) * q[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    return (a[0] + t * r[0], a[1] + t * r[1], r, q) if 0 <= t <= 1 and 0 <= u <= 1 else None


def cent(poly):
    return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))


class World:
    """The finished map in the kit's frame, with the kit's tests (clear of buildings, which district, on a road)."""

    def __init__(self, out):
        self.out = out
        cw = lambda k: XS.SECTIONS[k]['carriageway']
        self.roads = []
        for kind, src in (('street', 'streets'), ('lane', 'lanes'), ('path', 'paths')):
            for d, lines in sorted((out.get(src) or {}).items()):
                for i, ln in enumerate(lines):
                    if len(ln) > 1:
                        self.roads.append(dict(k=kind, pts=[P(p) for p in ln], w=cw(kind) if kind in XS.SECTIONS else 2.5, d=d, id=f'{d}/{kind}/{i}'))
        seen, n = set(), {}
        for m in out.get('mains', []):
            sig = tuple(tuple(round(c, 1) for c in p) for p in m['pts'])
            if sig in seen or sig[::-1] in seen:
                continue
            seen.add(sig)
            k = n.get(m.get('d'), 0); n[m.get('d')] = k + 1
            self.roads.append(dict(k='main', pts=[P(p) for p in m['pts']], w=cw('main'), d=m.get('d'), id=f"{m.get('d')}/main/{k}", name=m.get('name')))
        self.arts = [dict(k='art', cls=a['cls'], pts=[P(p) for p in a['pts']], w=ART_W.get(a['cls'], 18.0), name=a['name'], d=None) for a in out.get('arterials', [])]
        self.bpolys = [Polygon([P(p) for p in b[1:]]).buffer(0) for L in out['buildings'].values() for b in L if len(b) > 3]
        self.bt = STRtree(self.bpolys)
        self.dpolys = [(d['id'], prep(Polygon([P(p) for p in d['poly'][0]]).buffer(0))) for d in out['districts']]
        self.dname = {d['id']: d['name'] for d in out['districts']}
        self.built = set(out['buildings'])
        # every carriageway and gutter, for "not on a road", and whose it is
        self.cores, self.core_id = [], []
        for r in self.roads:
            if r['k'] in XS.SECTIONS:
                self.cores.append(LineString(r['pts']).buffer(XS.walkway_band(r['k'])[0])); self.core_id.append(r['id'])
        for a in self.arts:
            k = a['cls'] if a['cls'] in XS.SECTIONS else 'art'
            self.cores.append(LineString(a['pts']).buffer(XS.walkway_band(k)[0])); self.core_id.append('art/' + a['name'])
        self.ct = STRtree(self.cores)
        self.ground = GU.Ground(out)   # what each square metre is for, and who may be on it (scripts/ground.py)
        self.wet = prep(unary_union([Polygon([P(p) for p in w]).buffer(0) for w in (out.get('water') or []) + (out.get('ocean') or [])]))

    def district_at(self, p):
        q = Point(p)
        for k, poly in self.dpolys:
            if poly.contains(q):
                return k
        return None

    def clear(self, p, pad=1.5):   # the kit's _clear / in_building: no building within pad
        q = Point(p)
        return not any(self.bpolys[j].distance(q) <= pad for j in self.bt.query(q.buffer(pad)))

    def on_road(self, p):
        q = Point(p)
        return any(self.cores[j].contains(q) for j in self.ct.query(q))

    def on_other_road(self, p, rid):   # on the carriageway of a road other than rid (a parked car in a junction's mouth)
        q = Point(p)
        return any(self.core_id[j] != rid and self.cores[j].contains(q) for j in self.ct.query(q))

    def fits(self, kind, p, ang=0.0):
        """The ground allows this kind here (kit frame): at its middle, and for a vehicle or boat at both ends too."""
        L = LENGTH.get(kind, 0) / 2
        pts = [p] if L < 1 else [p, (p[0] + math.cos(ang) * L, p[1] + math.sin(ang) * L), (p[0] - math.cos(ang) * L, p[1] - math.sin(ang) * L)]
        return all(GU.allowed(self.ground(q[0], -q[1]), kind) for q in pts)

    def on_water(self, p):
        return self.wet.contains(Point(p))


def _back(x, y, ang):
    """A point and heading in the kit's frame back on the map's axes: (x, y south, degrees)."""
    return round(x, 1), round(-y, 1), round(-math.degrees(ang) % 360, 1)


def _ahead_name(W, road, end_pt, here):
    d = W.district_at(end_pt)
    if d and d != here and d in W.built:
        return W.dname[d]
    return road.get('name') or (W.dname.get(d) if d else None) or 'City Centre'


# ------------------------------------------------------------------ monuments by rule (blender/city.py monument_sites)
def monuments(W):
    mains = [r for r in W.roads if r['k'] == 'main']
    sites, per = [], {}
    for i, r1 in enumerate(mains):
        for r2 in mains[i + 1:]:
            for a, b in zip(r1['pts'], r1['pts'][1:]):
                for c, d in zip(r2['pts'], r2['pts'][1:]):
                    x = _seg_cross(a, b, c, d)
                    if not x:
                        continue
                    j = (x[0], x[1])
                    dist = W.district_at(j)
                    if dist not in W.built or any(math.dist(j, (s_['x'], s_['y'])) < 60 for s_ in sites):
                        continue
                    rng = Rng('monument', round(j[0]), round(j[1]))
                    u1, u2 = _unit(x[2]), _unit(x[3])
                    corners = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                    rng.shuffle(corners)
                    for sgn1, sgn2 in corners:
                        bis = _unit((u1[0] * sgn1 + u2[0] * sgn2, u1[1] * sgn1 + u2[1] * sgn2))
                        p = (j[0] + bis[0] * 16, j[1] + bis[1] * 16)
                        if W.clear(p, 3.0) and not W.on_road(p) and per.get(dist, 0) < 4:
                            kinds = JUNCTION[CHARACTER.get(dist, 'dense')]
                            kind = kinds[per.get(dist, 0) % len(kinds)]
                            per[dist] = per.get(dist, 0) + 1
                            sites.append(dict(kind=kind, x=p[0], y=p[1], ang=math.atan2(-bis[1], -bis[0]), d=dist))
                            break
    arches = {}
    for r in mains:
        for a, b in zip(r['pts'], r['pts'][1:]):
            for dname, poly in W.dpolys:
                if dname not in W.built or arches.get(dname, 0) >= 2:
                    continue
                ring = list(poly.context.exterior.coords)[:-1]
                for c, d in zip(ring, ring[1:] + ring[:1]):
                    x = _seg_cross(a, b, c, d)
                    if not x:
                        continue
                    u = _unit(x[2])
                    for sgn in (1, -1):
                        p = (x[0] + u[0] * 30 * sgn, x[1] + u[1] * 30 * sgn)
                        if poly.contains(Point(p)) and all(math.dist(p, (s_['x'], s_['y'])) > 50 for s_ in sites):
                            sites.append(dict(kind='arch', x=p[0], y=p[1], ang=math.atan2(u[1], u[0]), d=dname, span=r['w'] + 2, name=W.dname[dname]))
                            arches[dname] = arches.get(dname, 0) + 1
                            break
    hand_d = {m['d'] for m in W.out.get('monuments', [])}
    sites = [s_ for s_ in sites if s_['d'] not in hand_d]   # a district with monuments placed by hand keeps only those
    for poi in W.out['pois']:
        if poi['name'] in POINT_LANDMARKS and poi['d'] in W.built:
            k, a = POINT_LANDMARKS[poi['name']]
            q = P((poi['x'], poi['y']))
            sites.append(dict(kind=k, x=q[0], y=q[1], ang=a, d=poi['d']))
    # murals and billboards (street_art_sites)
    rng = Rng('street art')
    per = {}
    roads = list(W.roads) + [dict(k='main', pts=a['pts'], w=a['w'], d=None, id='art/' + a['name']) for a in W.arts if a['cls'] != 'bridge']
    for r in roads:
        if r['k'] != 'main':
            continue
        d = r.get('d') or W.district_at(r['pts'][len(r['pts']) // 2])
        if d not in W.built:
            continue
        acc = 0.0
        for a, b in zip(r['pts'], r['pts'][1:]):
            L = math.dist(a, b)
            if L < 1e-6:
                continue
            u = _unit((b[0] - a[0], b[1] - a[1]))
            k = (350 - acc % 350) % 350 + 60
            while k < L:
                side = rng.pick([-1, 1])
                n = (-u[1] * side, u[0] * side)
                if d in ('hub', 'maze', 'heights') and per.get(d, 0) < 4 and rng.chance(0.5):
                    q = (a[0] + u[0] * k + n[0] * (r['w'] / 2 + 5), a[1] + u[1] * k + n[1] * (r['w'] / 2 + 5))
                    if W.clear(q, 14) and W.district_at(q) == d and not W.on_road(q):
                        sites.append(dict(kind='mural_wall', x=q[0], y=q[1], ang=math.atan2(u[1], u[0]), d=d))
                        per[d] = per.get(d, 0) + 1
                elif d != 'estate' and rng.chance(0.55):
                    q = (a[0] + u[0] * k + n[0] * (r['w'] / 2 + 7), a[1] + u[1] * k + n[1] * (r['w'] / 2 + 7))
                    if W.clear(q, 7) and W.district_at(q) == d and not W.on_road(q):
                        sites.append(dict(kind='billboard', x=q[0], y=q[1], ang=math.atan2(u[1], u[0]), d=d))
                k += 350
            acc += L
    res = []
    for s_ in sites:
        x, y, a = _back(s_['x'], s_['y'], s_['ang'])
        m = {'model': s_['kind'], 'x': x, 'y': y, 'ang': a, 'd': s_['d'], 'rule': 1}
        if s_['kind'] == 'arch':
            m.update(span=round(s_['span'], 1), name=s_['name'])
        res.append(m)
    return res


# ------------------------------------------------------------------ road signs (blender/city.py roadside_sites)
def signs(W, profile_s=None):
    big = [dict(r, cls='main') for r in W.roads if r['k'] == 'main'] + [dict(a) for a in W.arts]
    sites, junctions = [], []
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
        here = W.district_at(J)
        if here not in W.built:
            continue
        for r, other in ((r1, r2), (r2, r1)):
            pts = r['pts']
            for sgn in (1, -1):
                k = min(range(len(pts) - 1), key=lambda i: dist_seg(J, pts[i], pts[i + 1]))
                a, b = pts[k], pts[k + 1]
                u = _unit((b[0] - a[0], b[1] - a[1]))
                u = (u[0] * sgn, u[1] * sgn)
                p0 = (J[0] - u[0] * 30, J[1] - u[1] * 30)
                if min(dist_seg(p0, pts[i], pts[i + 1]) for i in range(len(pts) - 1)) > 2.0:
                    continue
                right = (u[1], -u[0])
                off = r['w'] / 2 + 2.2
                sp = (p0[0] + right[0] * off, p0[1] + right[1] * off)
                if not W.clear(sp, 1.0) or W.district_at(sp) not in W.built:
                    continue
                lines = []
                for end in (other['pts'][0], other['pts'][-1]):
                    side = u[0] * (end[1] - J[1]) - u[1] * (end[0] - J[0])
                    if math.dist(end, J) < 25:
                        continue
                    lines.append(('left' if side > 0 else 'right', _ahead_name(W, other, end, here)))
                ahead = pts[-1] if sgn > 0 else pts[0]
                if math.dist(ahead, J) > 60:
                    lines.insert(0, ('up', _ahead_name(W, r, ahead, here)))
                uniq = []
                for ln in lines:
                    if ln[1] not in [x[1] for x in uniq]:
                        uniq.append(ln)
                if uniq:
                    sites.append(dict(kind='dir', x=sp[0], y=sp[1], face=math.atan2(-u[1], -u[0]), lines=uniq[:3]))
                q = (J[0] + u[0] * 25 + right[0] * off, J[1] + u[1] * 25 + right[1] * off)
                if W.clear(q, 1.0) and W.district_at(q) in W.built:
                    sites.append(dict(kind='speed', x=q[0], y=q[1], face=math.atan2(-u[1], -u[0]), v=SPEED.get(r.get('cls', 'main'), 50)))
    for r in big:   # gantries on the expressways and bridges, every 800 m, one each way
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
                        here = W.district_at(p)
                        q = (p[0] + u[0] * 30 * sgn, p[1] + u[1] * 30 * sgn)
                        panels = [[('up', _ahead_name(W, r, end, here))], [('up', r['name'])]]
                        sites.append(dict(kind='gantry', x=q[0], y=q[1], ang=math.atan2(u[1] * sgn, u[0] * sgn), span=r['w'] + 1.0, panels=panels,
                                          road=r['name'], s=round(s_ + 30 * sgn, 1)))
                    break
                acc += L
            s_ += 800
    for poi in W.out['pois']:   # no parking by the markets, on the nearest big road
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
                if W.clear(q, 0.8):
                    sites.append(dict(kind='noparking', x=q[0], y=q[1], face=math.atan2(-u[1] * sg, -u[0] * sg)))
    out = []
    for s_ in sites:
        if not any(o['kind'] == s_['kind'] and math.dist((o['x'], o['y']), (s_['x'], s_['y'])) < 6 for o in out):
            out.append(s_)
    NAME = {'dir': 'direction sign', 'speed': 'speed sign', 'noparking': 'no parking sign', 'gantry': 'gantry'}
    res = []
    for s_ in out:
        if s_['kind'] != 'gantry' and W.on_road((s_['x'], s_['y'])):
            continue   # never on a carriageway (a gantry spans one by design)
        x, y, a = _back(s_['x'], s_['y'], s_['ang'] if s_['kind'] == 'gantry' else s_['face'])
        f = {'kind': NAME[s_['kind']], 'x': x, 'y': y, 'ang': a, 'road': s_.get('road', ''), 'd': W.district_at((s_['x'], s_['y'])) or 'bush'}
        if s_['kind'] == 'dir':
            f['lines'] = [list(ln) for ln in s_['lines']]
        elif s_['kind'] == 'speed':
            f['v'] = s_['v']
        elif s_['kind'] == 'gantry':
            f.update(span=round(s_['span'], 1), panels=[[list(ln) for ln in p] for p in s_['panels']], s=s_['s'])
        res.append(f)
    return res


# ------------------------------------------------------------------ things
REFUSED = {}   # what the ground did not allow, by kind (the report)


def things(W):
    T = []
    REFUSED.clear()

    def put(k, x, y, ang, **kw):   # only where the ground allows it (scripts/ground.py), tested where it will be written
        X, Y, A = _back(x, y, ang)
        if not W.fits(k, (X, -Y), ang):
            REFUSED[k] = REFUSED.get(k, 0) + 1
            return
        T.append(dict({'k': k, 'x': X, 'y': Y, 'a': A, 'd': W.district_at((x, y)) or 'bush'}, **kw))

    def vehicle(k, x, y, ang, cond, rng, rch):
        kw = {'c': cond}
        if k == 'car':
            kw['s'] = rng.pick({'saloon': 5, 'suv': 3 + 4 * WEALTH[rch], 'pickup': 1})
            if rch == 'old_island' and rng.chance(0.15):
                kw['taxi'] = 1
        put(k, x, y, ang, **kw)

    # parked at the road edges (streets and mains), both sides
    for r in W.roads:
        if r['k'] not in ('street', 'main'):
            continue
        d = r.get('d')
        rch = CHARACTER.get(d, 'dense')
        rr = Rng('parked', r['id'])
        for a, b in zip(r['pts'], r['pts'][1:]):
            Ls = math.dist(a, b)
            if Ls < 1e-6:
                continue
            dx, dy = (b[0] - a[0]) / Ls, (b[1] - a[1]) / Ls
            ang = math.atan2(dy, dx)
            for side in (-1, 1):
                k = rr.between(0, 20)
                while k < Ls:
                    kind = rr.pick({'car': 4, 'keke': 2, 'okada': 3, 'danfo': 1 if r['k'] == 'main' else 0.2, 'molue': 0.06 if rch in ('dense', 'sprawl') else 0})
                    o = side * (r['w'] / 2 - 1.0)
                    x, y = a[0] + dx * k - dy * o, a[1] + dy * k + dx * o
                    if W.clear((x, y), 0.6 + WIDTH[kind] / 2) and rr.chance(0.55) and not W.on_other_road((x, y), r['id']):
                        cond = 'wreck' if kind == 'molue' else condition(WEALTH[rch], rr, kind in COMMERCIAL, parked=True)
                        vehicle(kind, x, y, ang + (math.pi if rr.chance(0.5) else 0) + rr.between(-0.1, 0.1), cond, rr, rch)
                    k += LENGTH[kind] + rr.between(2, 18)
    # the parks: people in markets, motor parks and under the bridges; rows of buses and lorries
    rows = {'motor park': ('danfo', 2.6, 7.0, 12), 'truck park': ('container', 3.4, 18.5, 24), 'lorry park': ('lorry911', 3.2, 10.0, 16)}
    for d, lst in sorted(W.out['parcels'].items()):
        for pc_ in lst:
            pts, kind = [P(q) for q in pc_['pts'][:-1]], pc_['kind']
            if len(pts) < 3:
                continue
            poly = Polygon(pts).buffer(0)
            Pp = prep(poly)
            rch = CHARACTER.get(d, 'dense')
            c = cent(pts)
            rr = Rng('life', d, kind, round(c[0]))
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            if kind in ('market', 'motor park', 'under bridge', 'under-bridge'):
                n = 0
                for _ in range(4000):
                    if n > (400 if kind == 'market' else 80):
                        break
                    p = (rr.between(min(xs), max(xs)), rr.between(min(ys), max(ys)))
                    if Pp.contains(Point(p)) and W.clear(p, 0.3):
                        dress = rr.pick({None: 4, 'hawker': 1, 'wrapper': 1}) or rr.pick(DRESS.get(rch, DRESS['dense']))
                        put('person', p[0], p[1], rr.between(0, math.tau), s=dress, still=1)
                        n += 1
            my_rows = dict(rows)
            if d == 'foodgate' and kind == 'market':
                my_rows['market'] = ('lorry911', 3.2, 10.0, 6)
            if kind in my_rows and kind != 'market':   # packed yard to yard: rows nose to nose, a drive lane every two rows
                vk, sx, sy, _ = my_rows[kind]
                best = []
                for i in range(len(pts)):
                    a, b = pts[i], pts[(i + 1) % len(pts)]
                    ang = math.atan2(b[1] - a[1], b[0] - a[0])
                    ux, uy, vx, vy = math.cos(ang), math.sin(ang), -math.sin(ang), math.cos(ang)
                    us, vs = [p[0] * ux + p[1] * uy for p in pts], [p[0] * vx + p[1] * vy for p in pts]
                    got, v, row = [], min(vs) + sy / 2 + 1.0, 0
                    while v < max(vs) - sy / 2:
                        u = min(us) + sx / 2 + 1.0
                        while u < max(us) - sx / 2:
                            x, y = u * ux + v * vx, u * uy + v * vy
                            if all(Pp.contains(Point(q)) for q in ((x + dx_ * ux + dy_ * vx, y + dx_ * uy + dy_ * vy) for dx_ in (-sx / 2, sx / 2) for dy_ in (-sy / 2, sy / 2))) and W.clear((x, y), 1.0):
                                got.append((x, y, ang + math.pi / 2 + (math.pi if row % 2 else 0)))
                            u += sx
                        v += sy + (6.0 if row % 2 else 0)
                        row += 1
                    if len(got) > len(best):
                        best = got
                for x, y, h in best:
                    if rr.chance(0.1):   # a gap here and there: a bus out on the road
                        continue
                    put(vk, x, y, h, c=condition(0.3, rr, True, parked=True))
            elif kind in my_rows:
                vk, sx, sy, count = my_rows[kind]
                per = max(1, int(count ** 0.5 * 1.5))
                for k in range(count):
                    x, y = c[0] + (k % per - (per - 1) / 2) * sx, c[1] + (k // per - 0.5) * sy
                    if Pp.contains(Point(x, y)) and W.clear((x, y), 0.5):
                        put(vk, x, y, math.pi / 2, c=condition(0.3, rr, True, parked=True))
            if kind == 'container yard':   # reach stackers and forklifts among the containers
                rr2 = Rng('port machines', round(c[0]))
                n = 0
                for _ in range(400):
                    if n >= 16:
                        break
                    p = (rr2.between(min(xs), max(xs)), rr2.between(min(ys), max(ys)))
                    if Pp.contains(Point(p)) and W.clear(p, 4.0):
                        put(rr2.pick({'stacker': 1, 'forklift': 1}), p[0], p[1], rr2.between(0, math.tau), c='worn')
                        n += 1
    # boats: a ferry under way on each route and a water bus at each end; dredgers off the sand and sawmill shores
    for f in W.out.get('ferries', []):
        a, b = P(f['pts'][0]), P(f['pts'][-1])
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for t, kind, back in ((0.4, 'ferry', False), (0.06, 'water_bus', True), (0.94, 'water_bus', False)):
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            if W.on_water(q):
                put(kind, q[0], q[1], ang + (math.pi if back else 0))
    for name in ('Agboyi Creek Villages', 'Okobaba Sawmill', 'Canoe Jetty'):
        poi = next((p for p in W.out['pois'] if p['name'] == name), None)
        if not poi:
            continue
        q0 = P((poi['x'], poi['y']))
        for ang in [k * math.pi / 8 for k in range(16)]:
            q = (q0[0] + math.cos(ang) * 160, q0[1] + math.sin(ang) * 160)
            if W.on_water(q) and W.on_water((q0[0] + math.cos(ang) * 200, q0[1] + math.sin(ang) * 200)):
                put('dredger', q[0], q[1], ang + math.pi / 2)
                break
    for bw in W.out.get('boardwalks', []):   # canoes tied along Water Town's boardwalks
        pts = [P(p) for p in bw]
        rr = Rng('canoes', round(pts[0][0]), round(pts[0][1]))
        for a_, b_ in zip(pts, pts[1:]):
            Ls = math.dist(a_, b_)
            if Ls < 1e-6:
                continue
            dx, dy = (b_[0] - a_[0]) / Ls, (b_[1] - a_[1]) / Ls
            k = rr.between(4, 20)
            while k < Ls:
                o = rr.pick([-1, 1]) * rr.between(3.0, 8.0)
                q = (a_[0] + dx * k - dy * o, a_[1] + dy * k + dx * o)
                if W.clear(q, 1.0) and rr.chance(0.7):
                    ang = math.atan2(dy, dx) + rr.between(-0.4, 0.4)
                    put('canoe', q[0], q[1], ang, p=1 if rr.chance(0.6) else 0)
                k += rr.between(12, 30)
    # the trains: a commuter set at the Hub station, the old narrow-gauge train in Railside, a freight train at the port end
    if W.out.get('rail'):
        line_pts = [P(p) for p in W.out['rail']['pts']]
        segl = [math.dist(line_pts[i], line_pts[i + 1]) for i in range(len(line_pts) - 1)]
        S = sum(segl)
        for name, at, consist in (('commuter', 'station', ['commuter'] * 4), ('old', 0.22, ['loco'] + ['coach'] * 4), ('freight', 0.9, ['loco'] + ['wagon'] * 8)):
            if at == 'station':
                st = next((p for p in W.out['pois'] if p['name'] == 'Hub Rail Station'), None)
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
                s = best[1]
            else:
                s = S * at
            for idx, kname in enumerate(consist):
                ln = TRAIN_L[kname]
                mid = s - ln / 2
                acc = 0.0
                for i in range(len(line_pts) - 1):
                    if acc + segl[i] >= mid:
                        A, B = line_pts[i], line_pts[i + 1]
                        t = (mid - acc) / segl[i]
                        p = (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)
                        kw = {'train': name}
                        if kname == 'commuter' and idx == 0:
                            kw['cab'] = 1
                        put('train:' + kname, p[0], p[1], math.atan2(B[1] - A[1], B[0] - A[0]), **kw)
                        break
                    acc += segl[i]
                s -= ln
    # the rail market: stalls on a 1.9 m grid between the tracks' clearance and the zone's edge
    if W.out.get('rail'):
        rail_pts = [P(p) for p in W.out['rail']['pts']]
        rail = LineString(rail_pts)
        for e_ in W.out.get('encroach', []):
            if e_['kind'] != 'rail market':
                continue
            zone = [P(p) for p in e_['pts']]
            Z = prep(Polygon(zone).buffer(0))
            bx0, by0, bx1, by1 = min(p[0] for p in zone), min(p[1] for p in zone), max(p[0] for p in zone), max(p[1] for p in zone)
            gx = bx0 + 0.9
            while gx < bx1:
                gy = by0 + 0.9
                while gy < by1:
                    p = (gx, gy)
                    rr = Rng('rail market', round(gx * 2), round(gy * 2))
                    if Z.contains(Point(p)) and rail.distance(Point(p)) > 2.4 and not rr.chance(0.3):
                        k = min(range(len(rail_pts) - 1), key=lambda i: dist_seg(p, rail_pts[i], rail_pts[i + 1]))
                        ra = math.atan2(rail_pts[k + 1][1] - rail_pts[k][1], rail_pts[k + 1][0] - rail_pts[k][0])
                        put('rail stall', p[0], p[1], ra)
                    gy += 1.9
                gx += 1.9
    return T


def life(out):
    """What moves: the data for the traffic and the walkers (the kit draws a still of them; the game moves them)."""
    return {'crowd': CROWD, 'wealth': WEALTH, 'gap': GAP,
            'mix': {f'{ch}|{k}': m for (ch, k), m in sorted(MIX.items())},
            'mix_d': {'foodgate|main': dict(MIX[('dense', 'main')], lorry911=10)},   # the food lorries of the big market
            'roads': {}}


def place(out):
    W = World(out)
    mon = monuments(W)
    sg = signs(W)
    th = things(W)
    out.setdefault('monuments', []).extend(mon)
    out.setdefault('furniture', []).extend(sg)
    out['things'] = sorted(th, key=lambda t: (t['k'], t['x'], t['y']))
    out['life'] = life(out)
    out['ground_use'] = GU.rules()
    rep = {'monuments': len(mon), 'signs': len(sg), 'refused by the ground': dict(sorted(REFUSED.items()))}
    for t in th:
        k = 'vehicles' if t['k'] in LENGTH else 'people' if t['k'] == 'person' else 'trains' if t['k'].startswith('train') else t['k']
        rep[k] = rep.get(k, 0) + 1
    return rep
