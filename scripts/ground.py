"""Ground use: what every square metre of Gidi is for, and who may be on it (owner, 17 Oct 2026: "it's important to have the
entire system understand where people can walk... human beings don't walk on the main road, where cars can go, where boats
can go... the fact that we don't understand where things can be on means we're having cars in weird places, people in weird
places").

One answer for everything: the bake places things by it (scripts/things.py), the checks test every thing against it
(scripts/check_district.py), the board colours it (web/board.js, the same rules in JavaScript), and the Unreal importer
makes its navigation areas from it (people walk where people may walk, traffic drives where vehicles may drive).

The ground is worked out from what the map already holds, in this order (the first that applies wins):

  water        the lagoon, creeks and sea, except on a boardwalk or jetty           boats
  boardwalk    a boardwalk or jetty over the water                                   people
  rail         the tracks and 2.4 m either side                                      trains (people only at crossings)
  rail market  the rail market's zone off the tracks                                 stalls, people
  market road  a market street's traders' strip: the walkway and the carriageway    stalls, people, parked vehicles
               outside the running lane kept clear (cross_sections.MARKET_CLEAR)
  carriageway  the road surface                                                      moving vehicles (people cross)
  parking      the outer PARK_W m of a street's or main road's carriageway, away    parked vehicles, moving vehicles
               from junctions: where cars, kekes and okadas stop
  lane         a lane: shared, no walkway                                            people, okadas, kekes, carts, parked
  gutter       the open drain                                                        nobody (planks and slabs cross it)
  walkway      beside the gutter                                                     people, furniture, parked okadas
  building     inside a building                                                     (indoors)
  park         a motor park, lorry park, truck park, bus terminal                    vehicles, people
  market       a market plot                                                         stalls, people, lorries
  yard         a container yard, barge yard, sawmill, industrial plot                vehicles, machines, people
  plot         any other plot (school, pitch, green, palace, ...)                    people
  ground       the rest of a district: compounds, alleys, open land                 people, parked vehicles
  bush         outside the districts                                                 people

out["ground_use"] = {"classes": {name: [who, ...]}, "order": [...], "park_w": PARK_W, "junction_m": JUNCTION_M}.
"""
import math

from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely.prepared import prep
from shapely.strtree import STRtree

import cross_sections as XS

PARK_W = 2.4        # the parking strip: the outer 2.4 m of a street's or main road's carriageway
JUNCTION_M = 12.0   # no parking within this of another road's carriageway (the mouth of a junction)
WHO = {
    'water': ['boat'],
    'boardwalk': ['person'],
    'rail': ['train'],
    'rail market': ['stall', 'person'],
    'market road': ['stall', 'person', 'parked vehicle', 'moving vehicle'],
    'carriageway': ['moving vehicle'],
    'parking': ['parked vehicle', 'moving vehicle'],
    'lane': ['person', 'parked vehicle', 'moving vehicle', 'stall'],
    'gutter': [],
    'walkway': ['person', 'furniture', 'parked okada', 'stall', 'equipment'],
    'building': [],
    'park': ['parked vehicle', 'moving vehicle', 'person', 'stall', 'equipment'],
    'market': ['stall', 'person', 'parked vehicle', 'equipment'],
    'yard': ['parked vehicle', 'machine', 'person', 'equipment'],
    'plot': ['person', 'equipment'],
    'ground': ['person', 'parked vehicle', 'stall', 'equipment'],
    'bush': ['person'],
}
ORDER = list(WHO)
PARK_KINDS = {'motor park', 'lorry park', 'truck park', 'bus terminal'}
YARD_KINDS = {'container yard', 'barge yard', 'sawmill', 'industrial', 'tank farm', 'refinery', 'landfill', 'waterworks'}
VEHICLES = {'danfo', 'korope', 'brt', 'keke', 'okada', 'car', 'police', 'tipper', 'tanker', 'cart', 'wheelbarrow', 'container', 'lorry911',
            'fire', 'ambulance', 'refuse', 'mixer', 'water', 'molue'}


def role(kind):
    """What a thing in out["things"] is, for the rules above."""
    if kind == 'person':
        return 'person'
    if kind in ('ferry', 'water_bus', 'dredger', 'canoe'):
        return 'boat'
    if kind.startswith('train'):
        return 'train'
    if kind == 'rail stall':
        return 'stall'
    if kind in ('stacker', 'forklift'):
        return 'machine'
    if kind == 'generator':
        return 'equipment'
    return 'parked vehicle'


def allowed(cls, kind):
    r = role(kind)
    who = WHO.get(cls, [])
    return r in who or (r == 'parked vehicle' and kind == 'okada' and 'parked okada' in who) or (r == 'machine' and 'parked vehicle' in who)


class Ground:
    """ground(x, y) on the map's axes (y south): the class of the ground there."""

    def __init__(self, out):
        self.roads = []   # (kind, line, road id)
        for src, kind in (('streets', 'street'), ('lanes', 'lane')):
            for d in sorted(out.get(src) or {}):
                for i, p in enumerate(out[src][d]):
                    if len(p) > 1:
                        self.roads.append((kind, LineString(p), f'{d}/{kind}/{i}'))
        for i, m in enumerate(out.get('mains', [])):
            if len(m['pts']) > 1:
                self.roads.append(('main', LineString(m['pts']), f"main/{i}"))
        for a in out.get('arterials', []):
            if a['cls'] != 'bridge':
                self.roads.append((a['cls'] if a['cls'] in XS.SECTIONS else 'art', LineString(a['pts']), 'art/' + a['name']))
        self.rt = STRtree([g for _, g, _ in self.roads])
        self.water = prep(unary_union([Polygon(w).buffer(0) for w in (out.get('water') or []) + (out.get('ocean') or [])]))
        walks = [LineString(b).buffer(1.5) for b in out.get('boardwalks', []) if len(b) > 1]
        walks += [LineString(s['pts']).buffer(s.get('width', 3) / 2) for s in out.get('structures', []) if s['kind'] == 'jetty' and len(s['pts']) > 1]
        self.walks = prep(unary_union(walks)) if walks else None
        self.rail = prep(LineString(out['rail']['pts']).buffer(2.4)) if out.get('rail') else None
        zones = [(z['kind'], Polygon(z['pts']).buffer(0)) for z in out.get('encroach', [])]
        self.rail_market = prep(unary_union([g for k, g in zones if k == 'rail market'] or [Point(-1e6, -1e6).buffer(1)]))
        self.market_streets = [g for k, g in zones if k == 'market street']
        self.mt = STRtree(self.market_streets) if self.market_streets else None
        B = [Polygon(b[1:]).buffer(0) for L in out['buildings'].values() for b in L if len(b) > 3]
        self.B, self.bt = B, STRtree(B)
        self.plots = []
        for d, L in (out.get('parcels') or {}).items():
            for p in L:
                k = p['kind']
                c = 'park' if k in PARK_KINDS else 'market' if k == 'market' else 'yard' if k in YARD_KINDS else 'plot'
                self.plots.append((c, Polygon(p['pts']).buffer(0)))
        self.pt = STRtree([g for _, g in self.plots])
        self.districts = prep(unary_union([Polygon(d['poly'][0]).buffer(0) for d in out['districts']]))

    def road_here(self, q):
        """(class, road) for a point on a road's cross-section, or None: the most specific band wins."""
        best = None
        for j in self.rt.query(q.buffer(20)):
            kind, g, rid = self.roads[j]
            dd = g.distance(q)
            s = XS.SECTIONS[kind]
            half = s['carriageway'] / 2
            if dd <= half:
                rank = 0
            elif dd <= half + s['gutter']:
                rank = 1
            elif dd <= half + s['gutter'] + s['walkway']:
                rank = 2
            else:
                continue
            if best is None or rank < best[0] or (rank == best[0] and dd - half < best[2]):
                best = (rank, j, dd - half)
        return best

    def __call__(self, x, y):
        q = Point(x, y)
        if self.water.contains(q):
            return 'boardwalk' if self.walks is not None and self.walks.contains(q) else 'water'
        if self.rail is not None and self.rail.contains(q):
            return 'rail'
        if self.rail_market.contains(q):
            return 'rail market'
        hit = self.road_here(q)
        if hit is not None:
            rank, j, edge = hit
            kind, g, rid = self.roads[j]
            if self.mt is not None and any(self.market_streets[k].contains(q) for k in self.mt.query(q)):
                clear = XS.MARKET_CLEAR.get(kind)
                if clear is None or g.distance(q) > clear / 2:
                    return 'market road'
            if rank == 0:
                if kind == 'lane':
                    return 'lane'
                if kind in ('street', 'main') and edge > -PARK_W and not self.near_other(q, j):
                    return 'parking'
                return 'carriageway'
            return 'gutter' if rank == 1 else 'walkway'
        if any(self.B[j].contains(q) for j in self.bt.query(q)):
            return 'building'
        for j in self.pt.query(q):
            c, g = self.plots[j]
            if g.contains(q):
                return c
        return 'ground' if self.districts.contains(q) else 'bush'

    def near_other(self, q, j):
        """The mouth of a junction: another road's carriageway within JUNCTION_M, crossing or branching off at an angle (a street
        that merely carries straight on as another piece is not a junction)."""
        own = self.roads[j][1]
        ends = [own.coords[0], own.coords[-1]]
        for k in self.rt.query(q.buffer(JUNCTION_M + 20)):   # an expressway's carriageway is 15 m from its centre line
            if k == j:
                continue
            kind, g, _ = self.roads[k]
            if g.distance(q) >= XS.SECTIONS[kind]['carriageway'] / 2 + JUNCTION_M:
                continue
            if _carries_on(own, ends, g) or g.equals(own):   # an edge road both its districts list is one road
                continue
            return True
        return False


def _carries_on(own, ends, g):
    """g is the same street carrying straight on as its next piece: they meet end to end (within 1 m) and run on within
    30 degrees of each other there. Anything else within reach is a junction (a shallow merge too)."""
    for e in ends:
        for f, f2 in ((g.coords[0], g.coords[1]), (g.coords[-1], g.coords[-2])):
            if math.dist(e, f) < 1.0:
                e2 = own.coords[1] if e == own.coords[0] else own.coords[-2]
                u = (e[0] - e2[0], e[1] - e2[1]); v = (f2[0] - f[0], f2[1] - f[1])
                lu, lv = math.hypot(*u) or 1, math.hypot(*v) or 1
                if (u[0] * v[0] + u[1] * v[1]) / (lu * lv) > 0.87:
                    return True
    return False


def rules():
    return {'classes': WHO, 'order': ORDER, 'park_w': PARK_W, 'junction_m': JUNCTION_M,
            'plots': {'park': sorted(PARK_KINDS), 'yard': sorted(YARD_KINDS), 'market': ['market']}}
