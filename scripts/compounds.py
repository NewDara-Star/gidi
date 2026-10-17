"""Compound walls, in the map data (owner, 16 Oct 2026: if it's in the 3D, it's in the 2D).

The 3D kit used to put its own wall 2 m round a share of houses, checking nothing: a fifth of them crossed a road, and
neighbours' walls ran through each other. Now the bake works the walls out here, and the kit only dresses them, so the
drawing board shows and checks every wall, and what's fixed on the board is what the 3D draws.

For each district:
- a house is walled at the share the kit used for its character (dense a third, the estates nearly all; shops and sheds
  never: a shop opens onto the street), picked by a stable hash of its position, so the bake stays byte-identical;
- its compound is the ground within 2 m of it that is nearer to it than to any other building (a Voronoi cell), less
  every road out to its walkway, the water, the plots (markets, schools, parks have their own edges) and other buildings;
- neighbouring compounds merge, so one wall line runs round them (never two walls side by side), and the parts of that line
  that hug a house's own wall are dropped;
- each walled house gets a gate on its street side.

out["compound_walls"][d]: wall lines; out["compound_gates"][d]: [x, y]; out["walled"][d]: the walled buildings' indices
(the kit gives them no shop front). Hand edits ("cut wall", "add wall", "add gate", "delete gate") apply after this.
"""
import zlib

from shapely import voronoi_polygons
from shapely.geometry import LineString, MultiPoint, Point, Polygon
from shapely.ops import linemerge, nearest_points, unary_union
from shapely.strtree import STRtree

CHARACTER = {'maze': 'dense', 'hub': 'dense', 'jungle': 'dense', 'foodgate': 'dense', 'bazaar': 'dense',
             'railside': 'sprawl', 'frontier': 'sprawl', 'border': 'sprawl', 'oldisland': 'old_island', 'oldshore': 'old_island',
             'estate': 'elite', 'heights': 'elite', 'capital': 'civic', 'watertown': 'waterfront', 'port': 'port'}   # blender/gidi_kit/rules.py
WALLED_SHARE = {'dense': 0.3, 'sprawl': 0.55, 'old_island': 0.1, 'elite': 0.95, 'civic': 0.6, 'waterfront': 0.05, 'port': 0.4}   # the kit's compound_p
HOUSES = {'front', 'back', 'old house', 'brazilian house', 'colonial house', 'villa', 'mansion', 'flats', 'face-me', 'unfinished house'}
REACH = 2.0   # how far a compound reaches from its house


def _hash01(*parts):
    return zlib.crc32('|'.join(str(p) for p in parts).encode()) / 2 ** 32


def _rings(ws):
    out = []
    for r in ws or []:
        try:
            p = Polygon(r).buffer(0)
            if not p.is_empty:
                out.append(p)
        except Exception:
            pass
    return out


def compounds(out):
    XS = out.get('cross_sections') or {}
    reach = lambda k, dflt: (XS[k]['carriageway'] / 2 + XS[k].get('gutter', 0) + XS[k].get('walkway', 0)) if k in XS else dflt
    roads = []
    for src, k in (('streets', 'street'), ('lanes', 'lane'), ('paths', None)):
        for d, L in (out.get(src) or {}).items():
            for p in L:
                if len(p) > 1:
                    roads.append(LineString(p).buffer(reach(k, 1.2) if k else 1.2))
    for m in out.get('mains', []):
        if len(m['pts']) > 1:
            roads.append(LineString(m['pts']).buffer(reach('main', 5.0)))
    for a in out.get('arterials', []):
        if a['cls'] in ('art', 'exp'):
            roads.append(LineString(a['pts']).buffer(reach(a['cls'], 10.0)))
    if out.get('rail'):
        roads.append(LineString(out['rail']['pts']).buffer(4.0))
    # the carriageway and gutter alone (+15 cm): the last word, so no piece of wall ever stands on a road
    core = lambda k, dflt: (XS[k]['carriageway'] / 2 + XS[k].get('gutter', 0) + 0.15) if k in XS else dflt
    cores = [LineString(p).buffer(core(k, 1.0)) for src, k in (('streets', 'street'), ('lanes', 'lane')) for L in (out.get(src) or {}).values() for p in L if len(p) > 1]
    cores += [LineString(m['pts']).buffer(core('main', 4.5)) for m in out.get('mains', []) if len(m['pts']) > 1]
    cores += [LineString(a['pts']).buffer(core(a['cls'], 8.0)) for a in out.get('arterials', []) if a['cls'] in ('art', 'exp')]
    CT = STRtree(cores)
    blockers = roads + _rings(out.get('water')) + _rings(out.get('ocean'))
    for L in (out.get('parcels') or {}).values():
        blockers += [p.buffer(0.3) for p in _rings([q['pts'] for q in L])]
    BT = STRtree(blockers)
    walls, gates, walled = {}, {}, {}
    for d in sorted(out['buildings']):
        B = [b for b in out['buildings'][d]]
        polys = []
        for b in B:
            try:
                polys.append(Polygon(b[1:]).buffer(0) if len(b) > 3 else None)
            except Exception:
                polys.append(None)
        share = WALLED_SHARE[CHARACTER.get(d, 'dense')]
        pick = [i for i, (b, p) in enumerate(zip(B, polys)) if p is not None and not p.is_empty and b[0] in HOUSES
                and _hash01(d, round(p.centroid.x, 1), round(p.centroid.y, 1)) < share]
        walled[d] = pick
        if not pick:
            continue
        idx = [i for i, p in enumerate(polys) if p is not None and not p.is_empty]
        cents = [polys[i].centroid for i in idx]
        cells = voronoi_polygons(MultiPoint(cents), extend_to=MultiPoint(cents).envelope.buffer(50), ordered=True).geoms
        cell_of = {i: c for i, c in zip(idx, cells)}
        PT = STRtree([polys[i] for i in idx])
        areas = []
        for i in pick:
            p = polys[i]
            a = p.buffer(REACH, join_style=2).intersection(cell_of[i])
            near = [blockers[k] for k in BT.query(a)]
            others = [polys[idx[k]].buffer(0.25, join_style=2) for k in PT.query(a) if idx[k] != i]
            if near or others:
                a = a.difference(unary_union(near + others))
            a = a.buffer(0)
            if not a.is_empty:
                areas.append(a.union(p))
        if not areas:
            continue
        merged = unary_union(areas)
        hug = unary_union([p.buffer(0.35, join_style=2) for p in (polys[i] for i in idx)])
        lines = merged.boundary.difference(hug)
        lines = linemerge(lines) if lines.geom_type == 'MultiLineString' else lines
        ck = CT.query(lines)
        if len(ck):
            lines = lines.difference(unary_union([cores[k] for k in ck]))
        parts = [g for g in getattr(lines, 'geoms', [lines]) if g.geom_type == 'LineString' and g.length >= 1.0]
        walls[d] = sorted([[[round(x, 1), round(y, 1)] for x, y in g.coords] for g in parts])   # not simplified: a shortcut could clip a road's edge
        # a gate for each walled house: where its wall comes nearest the road in front of it
        WT = STRtree(parts)
        gd = []
        for i in pick:
            p = polys[i]
            c = p.centroid
            rk = BT.query(c.buffer(25))
            rd = [blockers[k] for k in rk if k < len(roads)]
            if not rd:
                continue
            road = min(rd, key=lambda r: r.distance(c))
            cand = [parts[k] for k in WT.query(p.buffer(REACH + 0.5))]
            if not cand:
                continue
            w = min(cand, key=lambda g: g.distance(road))
            q = nearest_points(w, road)[0]
            if q.distance(p) <= REACH + 0.6:
                gd.append([round(q.x, 1), round(q.y, 1)])
        gates[d] = sorted({tuple(g) for g in gd})
        gates[d] = [list(g) for g in gates[d]]
    out['compound_walls'], out['compound_gates'], out['walled'] = walls, gates, walled
    return {d: (len(walls.get(d, [])), round(sum(LineString(w).length for w in walls.get(d, [])) / 1000, 1), len(walled[d])) for d in walled}
