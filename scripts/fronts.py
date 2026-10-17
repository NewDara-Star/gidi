"""House fronts in the map data: which side faces the street, shop fronts, their canopies and the balconies (owner, 16 Oct
2026: if it's in the 3D, it's in the 2D).

The kit used to roll these itself: a balcony 1.1 m deep on any side of a house longer than 4 m, upstairs, even where a
neighbour stood half a metre away, and a shop canopy 1.2-1.8 m deep over the street with no check on the road. Now the
bake decides them here, where every one can be checked, and the kit draws what the data says.

For each front or back house:
- its front is the side nearest a street or main road (as the kit chose it);
- a front house within 9 m of the street is a shop at the kit's share for its character (never a walled one: a walled
  compound has a gate);
- half the shops have a canopy, 1.2-1.8 m deep, shortened so it stops 0.3 m short of the carriageway and clear of other
  buildings (dropped below 0.8 m);
- a house of two storeys or more has a balcony on each side longer than 4 m at the kit's share, but only where its
  1.1 m slab is clear of other buildings and of every carriageway.
Picks use a stable hash of the house's position, so the bake stays byte-identical.

out["fronts"][d][str(i)] = {"e": side (index into the building's points, side e runs from point e to e + 1), "shop": 0 or 1,
"aw": canopy depth (0 for none), "bal": [sides with a balcony]}. Hand edits ("set front") apply after this.
"""
import hashlib
import math

from shapely.geometry import LineString, Polygon
from shapely.strtree import STRtree

CHARACTER = {'maze': 'dense', 'hub': 'dense', 'jungle': 'dense', 'foodgate': 'dense', 'bazaar': 'dense',
             'railside': 'sprawl', 'frontier': 'sprawl', 'border': 'sprawl', 'oldisland': 'old_island', 'oldshore': 'old_island',
             'estate': 'elite', 'heights': 'elite', 'capital': 'civic', 'watertown': 'waterfront', 'port': 'port'}   # blender/gidi_kit/rules.py
SHOP_P = {'dense': 0.7, 'sprawl': 0.6, 'old_island': 0.8, 'elite': 0.1, 'civic': 0.5, 'waterfront': 0.4, 'port': 0.7}         # the kit's shop_p
BALCONY_P = {'dense': 0.35, 'sprawl': 0.3, 'old_island': 0.5, 'elite': 0.6, 'civic': 0.3, 'waterfront': 0.1, 'port': 0.35}    # the kit's balcony_p
HOUSES = ('front', 'back')
BAL_D, BAL_MAX = 1.1, 4.5   # parts.balcony: 1.1 m deep, up to 4.5 m wide


def _h(*parts):   # a stable draw in [0, 1); blake2b, not crc32: crc32 is linear, so two draws on one house were tied together
    return int.from_bytes(hashlib.blake2b('|'.join(str(p) for p in parts).encode(), digest_size=8).digest(), 'big') / 2 ** 64


def _ccw(pts):
    a = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return a > 0


def _slab(p, q, inward_ccw, depth, width):
    """The footprint of something standing out from side p-q: `width` wide, centred, `depth` deep, on the outside."""
    L = math.dist(p, q)
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    nx, ny = (uy, -ux) if inward_ccw else (-uy, ux)   # the outward normal (y runs south: a ccw ring in these numbers turns right)
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    w = width / 2
    return Polygon([(mx - ux * w, my - uy * w), (mx + ux * w, my + uy * w),
                    (mx + ux * w + nx * depth, my + uy * w + ny * depth), (mx - ux * w + nx * depth, my - uy * w + ny * depth)])


def fronts(out):
    XS = out.get('cross_sections') or {}
    cw = lambda k, dflt: XS[k]['carriageway'] / 2 if k in XS else dflt
    face_roads, cores = [], []   # streets and mains to face; every carriageway to keep clear
    for src, k in (('streets', 'street'), ('lanes', 'lane')):
        for L in (out.get(src) or {}).values():
            for p in L:
                if len(p) > 1:
                    g = LineString(p)
                    cores.append(g.buffer(cw(k, 2.5)))
                    if k == 'street':
                        face_roads.append((g, cw('street', 2.5)))
    for m in out.get('mains', []):
        if len(m['pts']) > 1:
            g = LineString(m['pts'])
            cores.append(g.buffer(cw('main', 3.75)))
            face_roads.append((g, cw('main', 3.75)))
    for a in out.get('arterials', []):
        if a['cls'] in ('art', 'exp'):
            cores.append(LineString(a['pts']).buffer(cw(a['cls'], 7.0)))
    FT = STRtree([g for g, _ in face_roads])
    CT = STRtree(cores)
    res = {}
    for d in sorted(out['buildings']):
        ch = CHARACTER.get(d, 'dense')
        B = out['buildings'][d]
        st = (out.get('storeys') or {}).get(d, [])
        walled = set((out.get('walled') or {}).get(d, []))
        polys = []
        for b in B:
            try:
                polys.append(Polygon(b[1:]).buffer(0) if len(b) > 3 else None)
            except Exception:
                polys.append(None)
        ok = [i for i, p in enumerate(polys) if p is not None and not p.is_empty]
        PT = STRtree([polys[i] for i in ok])
        R = {}
        for i, b in enumerate(B):
            if b[0] not in HOUSES or polys[i] is None or polys[i].is_empty:
                continue
            pts = b[1:]
            n = len(pts)
            c = polys[i].centroid
            key = (d, round(c.x, 1), round(c.y, 1))
            # the front: the side whose middle is nearest a street or main (less its half width), as the kit chose
            near = [face_roads[k] for k in FT.query(c.buffer(60))]
            best, e = 1e9, 0
            for j in range(n):
                p, q = pts[j], pts[(j + 1) % n]
                mid = LineString([p, q]).interpolate(0.5, normalized=True)
                dd = min((g.distance(mid) - hw for g, hw in near), default=99)
                if dd < best:
                    best, e = dd, j
            others = lambda g: any(polys[ok[k]].intersects(g) for k in PT.query(g) if ok[k] != i)
            on_road = lambda g: any(cores[k].intersects(g) for k in CT.query(g))
            inward = _ccw(pts)
            shop = int(b[0] == 'front' and best < 9 and i not in walled and _h('shop', *key) < SHOP_P[ch])
            aw = 0.0
            if shop and _h('awning', *key) < 0.5:
                p, q = pts[e], pts[(e + 1) % n]
                depth = 1.2 + 0.6 * _h('awdepth', *key)
                width = min(math.dist(p, q), 5.0)
                while depth >= 0.8 and (on_road(_slab(p, q, inward, depth + 0.3, width)) or others(_slab(p, q, inward, depth, width).buffer(-0.05))):
                    depth -= 0.1
                aw = round(depth, 1) if depth >= 0.8 else 0.0
            bal = []
            s = st[i] if i < len(st) else 1
            if s > 1:
                for j in range(n):
                    p, q = pts[j], pts[(j + 1) % n]
                    L = math.dist(p, q)
                    if L <= 4 or _h('balcony', j, *key) >= BALCONY_P[ch]:
                        continue
                    sl = _slab(p, q, inward, BAL_D, min(L - 1.0, BAL_MAX))
                    if not others(sl.buffer(0.15)) and not on_road(sl):
                        bal.append(j)
            R[str(i)] = {'e': e, 'shop': shop, 'aw': aw, 'bal': bal}
        res[d] = R
    out['fronts'] = res
    return {d: (sum(v['shop'] for v in R.values()), sum(1 for v in R.values() if v['aw']), sum(len(v['bal']) for v in R.values())) for d, R in res.items()}
