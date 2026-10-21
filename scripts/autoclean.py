"""The clean-up after the real areas, in every bake (owner, 21 Oct 2026: a fix made once must reach everything already built). Run after
the hand edits, the road ends and the bush furniture, on each district built from real places (web/hand/gen/<id>.json). Each building
the checks would flag is fixed where it stands:
- past a road's building line, on a deck, over an open gutter or round a pole or light: its footprint is cut back, or it goes if too
  little is left;
- two footprints overlapping: the smaller is cut back from the bigger;
- reached by no way within 45 m: it goes; a scrap of street under 3 m goes.
It used to write these as hand edits after each bake (scripts/hand_fix_checks.py), three bakes a pass; now the bake does it once."""
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

import cross_sections as XS

HALF_RAIL = 3.0   # scripts/check_district.py HALF['rail']
SOFT = {'stalls', 'kiosk'}   # tables and kiosks may stand in the market spill (the checks allow them in declared zones)
R = lambda xy: [round(xy[0], 1), round(xy[1], 1)]
L = lambda p: LineString(p) if len(p) > 1 else None


def ring_pts(g):   # a footprint's corners, rounded to 0.1 m, with no corner repeated (the bake's fronts need real edges)
    out = []
    for c in list(g.exterior.coords)[:-1]:
        q = R(c)
        if not out or q != out[-1]:
            out.append(q)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out


def _valid(b):   # a footprint whose outline crosses itself is mended (its largest piece), so the cuts don't fail
    if len(b) < 4:
        return None
    P = Polygon([R(c) for c in b[1:]])   # as the bake will store it: rounding can turn a 0.04 m2 touch into a 0.2 m2 overlap
    if not P.is_valid:
        P = P.buffer(0)
        P = max(getattr(P, 'geoms', [P]), key=lambda x: x.area) if not P.is_empty else None
    return P


def _biggest(Q):   # the largest piece, with its corners rounded as they will be stored (rounding must not bring an overlap back)
    Q = max(getattr(Q, 'geoms', [Q]), key=lambda x: x.area) if not Q.is_empty else Q
    if Q.is_empty or Q.geom_type != 'Polygon' or len(ring_pts(Q)) < 3:
        return Q
    R_ = Polygon(ring_pts(Q))
    return R_ if R_.is_valid else Q


def plan(G, D):
    """What to do in district D of the map G: ([(building index, new outline or None to remove it, why)], [street index to remove])."""
    from shapely.geometry import Point
    DP = Polygon(next(d for d in G['districts'] if d['id'] == D)['poly'][0])
    NEAR = DP.buffer(40)
    bad = []
    for k, bl in (('streets', 'street'), ('lanes', 'lane')):
        for ps in (G.get(k) or {}).values():
            for p in ps:
                g = L(p)
                if g is not None and g.distance(DP) < 40:
                    bad.append(g.buffer(XS.building_line(bl) - 0.05))
    for m in G['mains']:
        g = L(m['pts'])
        if g is not None and g.distance(DP) < 40:
            bad.append(g.buffer(XS.building_line('main') - 0.05))
    for a in G['arterials']:
        if a['cls'] in ('art', 'exp') and L(a['pts']).distance(DP) < 40:
            bad.append(L(a['pts']).buffer(XS.building_line(a['cls']) - 0.05))
    bad.append(L(G['rail']['pts']).buffer(HALF_RAIL - 0.05))
    for s in G.get('structures', []):
        if s['kind'] in ('flyover', 'skywalk', 'footbridge') and s.get('layer', 0) >= 1 and L(s['pts']).distance(DP) < 40:
            w = s.get('width'); bad.append(L(s['pts']).buffer(((w / 2) if w else (6 if s['kind'] == 'flyover' else 2)) - 0.05))
    FURN = [Point(f['x'], f['y']) for f in G.get('furniture', []) if NEAR.contains(Point(f['x'], f['y']))]
    for q in FURN:
        bad.append(q.buffer(0.4))
    B = G['buildings'][D]
    polys = [_valid(b) for b in B]
    ft = STRtree(FURN) if FURN else None
    for P_ in polys:   # a pole or light standing inside a footprint: a notch from it to the nearest wall, so the wall steps round it
        if P_ is None or ft is None:
            continue
        for k in ft.query(P_, predicate='contains'):
            q = FURN[int(k)]
            e_ = P_.exterior.interpolate(P_.exterior.project(q)); dx, dy = e_.x - q.x, e_.y - q.y; n_ = (dx * dx + dy * dy) ** 0.5 or 1
            bad.append(LineString([(q.x - dx / n_ * 0.6, q.y - dy / n_ * 0.6), (e_.x + dx / n_ * 1.0, e_.y + dy / n_ * 1.0)]).buffer(0.6))
    for r in G.get('gutters', []):
        if r.get('d') == D and r['state'] == 'open' and len(r['pts']) > 1:
            bad.append(L(r['pts']).buffer(0.1))
    bt = STRtree([g.buffer(0) if not g.is_valid else g for g in bad])
    act = {}
    for i, b in enumerate(B):
        P = polys[i]
        if P is None or b[0] in SOFT:
            continue
        near = [bt.geometries[int(k)] for k in bt.query(P, predicate='intersects')]
        if not near:
            continue
        Q = _biggest(P.difference(unary_union(near).buffer(0.15)))   # 15 cm more: rounding corners to 0.1 m must not bring the touch back
        if Q.is_empty or Q.geom_type != 'Polygon' or Q.area < 6:
            act[i] = (None, 'past a building line, over a gutter or round a pole: too little left'); polys[i] = None
        elif P.symmetric_difference(Q).area > 0.01:   # a touch the cut does not change is not a cut (it would only add corners, every bake)
            act[i] = (Q, 'cut back to the building line'); polys[i] = Q
    # overlaps: the smaller gives way
    idx = [i for i, P in enumerate(polys) if P is not None]
    tree = STRtree([polys[i] for i in idx])
    for i in idx:
        if polys[i] is None:
            continue
        for b_ in tree.query(polys[i]):
            j = idx[int(b_)]
            if j <= i or polys[j] is None or polys[i] is None:
                continue
            if polys[i].intersection(polys[j]).area > 0.05:
                s_, l_ = (i, j) if polys[i].area < polys[j].area else (j, i)
                Q = _biggest(polys[s_].difference(polys[l_].buffer(0.35)))   # 35 cm: rounding corners to 0.1 m must not bring the overlap back
                if Q.is_empty or Q.geom_type != 'Polygon' or Q.area < 6:
                    act[s_] = (None, 'overlapped a bigger one'); polys[s_] = None
                else:
                    act[s_] = (Q, 'cut back from its neighbour'); polys[s_] = Q
    # reach: no way within 45 m
    W = [L(p) for k in ('streets', 'lanes', 'paths') for ps in (G.get(k) or {}).values() for p in ps] + [L(m['pts']) for m in G['mains']] + [L(a['pts']) for a in G['arterials']]
    W = [w for w in W if w is not None and w.distance(DP) < 100]
    wt = STRtree(W)
    for i, P in enumerate(polys):
        if P is None or B[i][0] in SOFT:
            continue
        q = wt.query(P.buffer(45))
        if len(q) == 0 or min(W[int(k)].distance(P) for k in q) > 44:
            act[i] = (None, 'reached by no way'); polys[i] = None
    scraps = [i for i, p in enumerate(G['streets'].get(D, [])) if L(p) is not None and L(p).length < 3]
    return [(i, q, why) for i, (q, why) in sorted(act.items())], scraps


def clean(out, D):
    """The plan carried out on the bake's own data. Returns (cut back, gone, scraps)."""
    import hand
    cut = gone = n_scraps = 0
    for _ in range(4):   # again until nothing is left to do: a cut can leave a sliver against a third building
        acts, scraps = plan(out, D)
        if not acts and not scraps:
            break
        for i, Q, why in sorted(acts, key=lambda a: -a[0]):   # from the end, so removing one does not move the others
            if Q is None:
                hand._drop_building(out, D, i); gone += 1
            else:
                out['buildings'][D][i] = [out['buildings'][D][i][0]] + ring_pts(Q); cut += 1
        for i in sorted(scraps, reverse=True):
            out['streets'][D].pop(i)
        n_scraps += len(scraps)
    return cut, gone, n_scraps


def join(out, D, link=250.0):   # 250 m: real lanes that met a real road Gidi draws elsewhere
    """Every street, lane and path group must reach one of the district's main roads or an arterial (check 9, same rules). One that
    does not is joined to the nearest way that does by the shortest link, nearest first, on the bake's own roads. Returns the links."""
    from shapely.ops import nearest_points
    W = [(k, L(p['pts'] if isinstance(p, dict) else p)) for k in ('streets', 'lanes', 'paths') for p in (out.get(k) or {}).get(D, [])]
    W += [('main', L(m['pts'])) for m in out['mains'] if m.get('d') == D]
    W += [('main', L(a['pts'])) for a in out['arterials'] if a['cls'] in ('art', 'exp')]
    W += [('deck', L(s['pts'])) for s in out.get('structures', []) if s.get('d') == D and s.get('kind') in ('footbridge', 'skywalk')]
    W = [(k, g) for k, g in W if g is not None]
    links = []
    while True:
        geoms = [g for _, g in W]; tree = STRtree(geoms); parent = list(range(len(W)))
        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]; i = parent[i]
            return i
        for i, g in enumerate(geoms):
            for j in tree.query(g.buffer(1.0)):
                if j != i and g.distance(geoms[j]) <= 1.0:
                    parent[find(i)] = find(int(j))
        rooted = {find(i) for i, (k, _) in enumerate(W) if k == 'main'}
        loose = [i for i in range(len(W)) if W[i][0] != 'deck' and find(i) not in rooted]
        if not loose:
            return links
        ok_ = [i for i in range(len(W)) if find(i) in rooted]
        ot = STRtree([geoms[i] for i in ok_])
        best = None
        for i in loose:
            for j in ot.query(geoms[i].buffer(link)):
                dd = geoms[i].distance(geoms[ok_[int(j)]])
                if dd < link and (best is None or dd < best[0]):
                    best = (dd, i, ok_[int(j)])
        if best is None:
            return links   # too far from any way: left for check 9 to show
        dd, i, j = best
        p_, q_ = nearest_points(geoms[i], geoms[j])
        pts = [R(p_.coords[0]), R(q_.coords[0])]
        if pts[0] == pts[1]:   # within a hair: a half-metre stub makes the touch count
            pts = [pts[0], [round(pts[0][0] + 0.5, 1), pts[0][1]]]
        k = 'lanes'   # a lane, always: the clean-up takes street pieces under 3 m as scraps, and most links are a metre or two
        out[k].setdefault(D, []).append(pts); W.append((k, L(pts))); links.append((k, pts))
