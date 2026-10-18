"""The ground itself, painted in the map data (owner, 17 Oct 2026: "even the grain of sand on the ground... everything in the
data"; batch 3 of what the kit used to invent, which drew one soil colour per 400 m tile).

Two kinds of record, because some ground is a place and some is a texture:

out["ground_paint"]["areas"] = [{"k": kind, "pts": ring, "d": district, "s": seed}]: patches with an outline, each one shown
on the drawing board and movable or deletable there:
  grass      unused land in a district, well away from the houses and the roads (lots nobody has built on yet), and the
             greens, gardens and parks; dry grass in the drier inland districts
  mud        wet ground by the open gutters, more of it in the districts that flood (the share of the real place below 3 m)
  dirt       footpaths worn into packed earth
  sand       the beach-side and creek-side land of the waterfront and old-island districts

out["ground_paint"]["rules"][character] = {"soil", "yard", "weeds", "dust", "litter", "puddles"}: what is too fine to outline,
by district character: the colour of the bare ground, a walled compound's yard (swept dirt, or concrete in the estates and
the civic district), weeds at the foot of walls (share of wall length), dust spilt from
the road edges (metres), litter (pieces per 100 m of road, the kit's rate), puddles (per hectare of open ground). The kit draws these
from the rules, seeded by place, so they are fixed and the same every time.

Everything is clipped to ground that is open: never on a road's carriageway, gutter or walkway, a building, water, rail,
or a plot that dresses itself (markets, parks, yards...). Seeded by district: the bake stays byte-identical.
Hand edits: "add paint", "delete paint" (scripts/hand.py).
"""
import math
import random

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union
from shapely.prepared import prep

import cross_sections as XS

CHARACTER = {'maze': 'dense', 'hub': 'dense', 'jungle': 'dense', 'foodgate': 'dense', 'bazaar': 'dense',
             'railside': 'sprawl', 'frontier': 'sprawl', 'border': 'sprawl', 'oldisland': 'old_island', 'oldshore': 'old_island',
             'estate': 'elite', 'heights': 'elite', 'capital': 'civic', 'watertown': 'waterfront', 'port': 'port'}
FLOOD = {'maze': 0.08, 'hub': 0.09, 'jungle': 0.45, 'foodgate': 0.57, 'watertown': 0.55, 'capital': 0.0, 'bazaar': 0.32,
         'port': 0.48, 'railside': 0.03, 'estate': 0.2, 'oldisland': 0.97, 'heights': 0.54, 'frontier': 0.5, 'border': 0.4, 'oldshore': 0.4}   # rules.FLOOD
RULES = {   # the colour of bare ground (sRGB), and what is too fine to outline
    'dense':      {'soil': '#b5714a', 'yard': 'dirt', 'weeds': 0.25, 'dust': 1.2, 'litter': 50.0, 'puddles': 4.0},
    'sprawl':     {'soil': '#b9764b', 'yard': 'dirt', 'weeds': 0.45, 'dust': 1.6, 'litter': 35.0, 'puddles': 3.0},
    'old_island': {'soil': '#c8b089', 'yard': 'dirt', 'weeds': 0.2, 'dust': 0.8, 'litter': 50.0, 'puddles': 5.0},
    'elite':      {'soil': '#a9875f', 'yard': 'concrete', 'weeds': 0.05, 'dust': 0.3, 'litter': 2.5, 'puddles': 0.5},
    'civic':      {'soil': '#b07a52', 'yard': 'concrete', 'weeds': 0.15, 'dust': 0.6, 'litter': 20.0, 'puddles': 1.5},
    'waterfront': {'soil': '#8f7a5c', 'yard': 'dirt', 'weeds': 0.3, 'dust': 0.5, 'litter': 65.0, 'puddles': 8.0},
    'port':       {'soil': '#8e8579', 'yard': 'concrete', 'weeds': 0.2, 'dust': 1.0, 'litter': 50.0, 'puddles': 3.0},
    'bush':       {'soil': '#8a8a4e', 'yard': 'dirt', 'weeds': 0.6, 'dust': 1.0, 'litter': 5.0, 'puddles': 1.0},
}
SOIL_D = {'maze': '#9a8572'}   # a district's own bare-ground colour, measured (the Maze: Mushin and Shomolu's dusty grey-brown)
GREEN_PLOTS = {'green', 'garden', 'park', 'golf course', 'club', 'enclave', 'villas', 'estate'}
SELF_DRESSED = {'market', 'motor park', 'lorry park', 'truck park', 'bus terminal', 'container yard', 'barge yard', 'tank farm',
                'refinery', 'landfill', 'sawmill', 'waterworks', 'stadium', 'airfield', 'pitch', 'court', 'pool', 'school',
                'prison', 'barracks', 'pipeline', 'under bridge', 'station', 'mall', 'campus', 'livestock'}
LOT_SETBACK = 8.0      # a grass lot keeps this far from houses and road edges
LOT_MIN = 250.0        # m2: smaller open ground is yard and alley, not a lot
MUD_SHARE = 0.18       # of the gutter length, at full flood share, has mud beside it


def _ring(g):
    return [[round(x, 1), round(y, 1)] for x, y in g.exterior.coords]


def _pieces(g):
    return [p for p in getattr(g, 'geoms', [g]) if p.geom_type == 'Polygon' and not p.is_empty]


def paint(out):
    roads = []
    for src, kind in (('streets', 'street'), ('lanes', 'lane')):
        for L in (out.get(src) or {}).values():
            roads += [LineString(p).buffer(XS.walkway_band(kind)[1]) for p in L if len(p) > 1]
    roads += [LineString(m['pts']).buffer(XS.walkway_band('main')[1]) for m in out.get('mains', []) if len(m['pts']) > 1]
    roads += [LineString(a['pts']).buffer(XS.walkway_band(a['cls'] if a['cls'] in XS.SECTIONS else 'art')[1]) for a in out.get('arterials', []) if a['cls'] != 'bridge']
    if out.get('rail'):
        roads.append(LineString(out['rail']['pts']).buffer(4.0))
    wet = unary_union([Polygon(w).buffer(0) for w in (out.get('water') or []) + (out.get('ocean') or [])])
    areas = []
    for d in out['districts']:
        did = d['id']
        ch = CHARACTER.get(did, 'dense')
        D = Polygon(d['poly'][0]).buffer(0)
        DP = prep(D.buffer(30))
        R = unary_union([r for r in roads if DP.intersects(r)])
        B = [Polygon(b[1:]).buffer(0) for b in out['buildings'].get(did, []) if len(b) > 3]
        Bu = unary_union(B)
        plots = (out.get('parcels') or {}).get(did, [])
        dressed = unary_union([Polygon(p['pts']).buffer(0) for p in plots if p['kind'] in SELF_DRESSED] or [Point(-1e6, -1e6).buffer(1)])
        greens = [Polygon(p['pts']).buffer(0) for p in plots if p['kind'] in GREEN_PLOTS]
        open_ground = D.difference(R).difference(Bu).difference(wet).difference(dressed)
        rng = random.Random('paint|' + did)
        # grass: the lots nobody has built on (well clear of houses and roads), and the greens
        lots = D.difference(R.buffer(LOT_SETBACK)).difference(Bu.buffer(LOT_SETBACK)).difference(wet).difference(dressed)
        dry = ch in ('sprawl', 'port') or did in ('railside', 'border', 'frontier')
        for p in _pieces(lots.simplify(1.0)):
            if p.area >= LOT_MIN:
                areas.append({'k': 'dry grass' if dry and rng.random() < 0.6 else 'grass', 'pts': _ring(p), 'd': did, 's': rng.randrange(1 << 20)})
        for g in greens:
            for p in _pieces(g.difference(Bu).difference(R)):
                if p.area > 20:
                    areas.append({'k': 'grass', 'pts': _ring(p.simplify(0.5)), 'd': did, 's': rng.randrange(1 << 20)})
        # mud by the open gutters, by how much the place floods
        share = MUD_SHARE * (0.3 + 1.4 * FLOOD.get(did, 0.2))
        for gt in out.get('gutters', []):
            if gt.get('state') != 'open' or len(gt['pts']) < 2 or not DP.contains(Point(gt['pts'][0])):
                continue
            g = LineString(gt['pts'])
            t = rng.uniform(0, 30)
            while t < g.length:
                if rng.random() < share:
                    q = g.interpolate(t)
                    blob = Point(q.x, q.y).buffer(rng.uniform(1.5, 4.0), 8)
                    blob = blob.intersection(open_ground)
                    for p in _pieces(blob):
                        if p.area > 1.5:
                            areas.append({'k': 'mud', 'pts': _ring(p.simplify(0.2)), 'd': did, 's': rng.randrange(1 << 20)})
                t += rng.uniform(15, 45)
        # footpaths worn to packed dirt
        for p_ in (out.get('paths') or {}).get(did, []):
            if len(p_) > 1:
                for p in _pieces(LineString(p_).buffer(1.4, cap_style=2).intersection(open_ground)):
                    if p.area > 3:
                        areas.append({'k': 'dirt', 'pts': _ring(p.simplify(0.3)), 'd': did, 's': rng.randrange(1 << 20)})
        # sand by the water in the waterfront and old-island districts
        if ch in ('waterfront', 'old_island'):
            shore = wet.buffer(12).difference(wet).intersection(open_ground)
            for p in _pieces(shore.simplify(1.0)):
                if p.area > 30:
                    areas.append({'k': 'sand', 'pts': _ring(p), 'd': did, 's': rng.randrange(1 << 20)})
    out['ground_paint'] = {'rules': RULES, 'soil_d': SOIL_D, 'areas': areas}
    rep = {}
    for a in areas:
        rep[a['k']] = rep.get(a['k'], 0) + 1
    return rep
