"""Trees in the map data (owner, 16 Oct 2026: if it's in the 3D, it's in the 2D).

The kit used to scatter trees in each 400 m tile at random, checking only buildings, roads and the lagoon. It missed the
ocean, compound walls and street furniture. Now the bake plants them here, so the drawing board shows every tree, the
checks see them, and they can be moved, added and taken out.

At the kit's densities per 400 m tile: estates 60, civic 30, sprawl 25, dense 8, old island 6, waterfront 10, port 6, and
the bush outside the districts 80. A tree needs 2 m clear of buildings, the road and its walkway plus 2 m, 1 m of a
compound wall, 1.5 m of street furniture, and dry land. Palms are twice as likely on Old Island, the estates and the
waterfront. The draw is seeded by district, so the bake stays byte-identical.

out["trees"][d] = [[x, y, "palm" | "broad"], ...] (d "bush" for the land outside the districts). Hand edits ("add tree",
"move tree", "delete tree") apply after this.
"""
import random

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union
from shapely.prepared import prep
from shapely.strtree import STRtree

CHARACTER = {'maze': 'dense', 'hub': 'dense', 'jungle': 'dense', 'foodgate': 'dense', 'bazaar': 'dense',
             'railside': 'sprawl', 'frontier': 'sprawl', 'border': 'sprawl', 'oldisland': 'old_island', 'oldshore': 'old_island',
             'estate': 'elite', 'heights': 'elite', 'capital': 'civic', 'watertown': 'waterfront', 'port': 'port'}
PER_TILE = {'elite': 60, 'civic': 30, 'sprawl': 25, 'dense': 8, 'old_island': 6, 'waterfront': 10, 'port': 6, 'bush': 80}   # legacy/blender/city.py
TILE_M2 = 400.0 * 400.0
PALMY = {'old_island', 'elite', 'waterfront'}


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


def trees(out):
    XS = out.get('cross_sections') or {}
    reach = lambda k, dflt: (XS[k]['carriageway'] / 2 + XS[k].get('gutter', 0) + XS[k].get('walkway', 0) + 2.0) if k in XS else dflt
    keep_out = []
    for src, k in (('streets', 'street'), ('lanes', 'lane'), ('paths', None)):
        for L in (out.get(src) or {}).values():
            keep_out += [LineString(p).buffer(reach(k, 3.0) if k else 2.5) for p in L if len(p) > 1]
    keep_out += [LineString(m['pts']).buffer(reach('main', 8.0)) for m in out.get('mains', []) if len(m['pts']) > 1]
    keep_out += [LineString(a['pts']).buffer(reach(a['cls'], 14.0) if a['cls'] in XS else 14.0) for a in out.get('arterials', [])]
    if out.get('rail'):
        keep_out.append(LineString(out['rail']['pts']).buffer(5.0))
    for L in (out.get('buildings') or {}).values():
        keep_out += [Polygon(b[1:]).buffer(2.0) for b in L if len(b) > 3]
    for L in (out.get('compound_walls') or {}).values():
        keep_out += [LineString(w).buffer(1.0) for w in L if len(w) > 1]
    keep_out += [Point(f['x'], f['y']).buffer(1.5) for f in out.get('furniture', [])]
    for s in out.get('structures', []):
        if len(s.get('pts', [])) > 1:
            keep_out.append(LineString(s['pts']).buffer((s.get('width') or 8) / 2 + 1.0))
    KT = STRtree(keep_out)
    wet_g = unary_union(_rings(out.get('water')) + _rings(out.get('ocean')))
    wet = prep(wet_g)
    dist_polys = [(d['id'], Polygon(d['poly'][0]).buffer(0)) for d in out['districts']]
    W, H = out['size']
    areas = [(d, CHARACTER.get(d, 'dense'), p) for d, p in dist_polys]
    areas.append(('bush', 'bush', box(0, 0, W, H).difference(unary_union([p for _, p in dist_polys])).difference(wet_g)))   # dry land only: the count follows the land
    res = {}
    for d, ch, area in areas:
        if area.is_empty:
            continue
        rng = random.Random('trees|' + d)
        n = int(round(area.area / TILE_M2 * PER_TILE[ch]))
        x0, y0, x1, y1 = area.bounds
        A = prep(area)
        got, tries = [], 0
        while len(got) < n and tries < n * 40:
            tries += 1
            x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
            q = Point(x, y)
            if not A.contains(q) or wet.contains(q) or any(keep_out[k].contains(q) for k in KT.query(q)):
                continue
            kind = 'palm' if rng.random() < (2 / 4 if ch in PALMY else 1 / 3) else 'broad'
            got.append([round(x, 1), round(y, 1), kind])
        res[d] = sorted(got)
    out['trees'] = res
    return {d: len(v) for d, v in res.items()}
