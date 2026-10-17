"""Road ends (owner, 17 Oct 2026: "the road quite literally just ends abruptly").

The generator drew streets that stop in the middle of nowhere: 2,725 ends touched no other road, no turning space and no
gate. A road in Lagos ends in one of a few ways, and the bake now gives every end one of them, after the frozen districts are
laid in (so it sees the final roads) and before the compound walls, fronts and trees (so they see the new ones):

- "water": it runs down to the lagoon, a creek or the sea (a landing, a jetty, the shore). Left as it is.
- "join": it was heading for another road and stopped short. It is carried on to that road, straight ahead if the other
  road is ahead within reach, else turning onto the nearest one, as long as the new stretch hits no house, no water, no
  railway and crosses no other road. A main road or arterial heading out of town with nothing in the way runs on through
  the bush to the edge of the map.
- "trim": the stretch past the last junction serves nobody (no house within SERVE m of it). It is cut back to the junction.
- "access": it stops at a house or a compound: someone's gate. Left as it is.
- "close": a close. It gets a turning space, a circle of tar at the end (HEAD_R, smaller where the houses are tight).
- "loose": none of those fit. The board flags it for a hand fix.

Roads are lengthened or shortened in place, never removed or reordered: the gutters and surfaces name roads by their place
in the lists. A trimmed road's gutters are cut back with it; furniture left beside a trimmed stretch, or standing where a
new stretch or turning space now runs, is taken out.

out["road_ends"] = [{"x", "y", "t": type, "road": id, "k": kind, "r": turning radius (closes only)}], every end that
touches no other road. Hand edits ("set road end") apply after this.
"""
import math

from shapely.geometry import LineString, Point, Polygon
from shapely.ops import substring, unary_union
from shapely.strtree import STRtree

import cross_sections as XS

JOIN = {'lane': 30.0, 'street': 45.0, 'main': 90.0, 'art': 160.0, 'exp': 160.0}   # how far it may be carried on to reach a road
AHEAD = 1.6       # straight ahead it may go this much further than when it turns
TURN_MAX = 70.0   # degrees: a join may bend no more than this from the road's own heading
SERVE = 45.0      # a stretch with no building within this many metres serves nobody (the checks: every building within 45 m of a way)
TOUCH = 3.0       # an end within this of another road meets it
HEAD_R = {'lane': 4.5, 'street': 7.0, 'main': 9.0}   # turning circle radius; shrunk to fit, never below half the road + 1 m
OUT_MAX = 6000.0  # how far a big road may run on, through the bush, to leave the map
EDGE = 30.0       # within this of the map's edge a road runs on out of Gidi


def _roads(out):
    """Every road as [kind, id, getter, setter], in a fixed order."""
    R = []
    for src, kind in (('streets', 'street'), ('lanes', 'lane')):
        for d in sorted(out.get(src) or {}):
            L = out[src][d]
            for i in range(len(L)):
                R.append([kind, f'{d}/{kind}/{i}', (lambda L=L, i=i: L[i]), (lambda v, L=L, i=i: L.__setitem__(i, v))])
    per, groups = {}, {}
    for m in out.get('mains', []):   # an edge road both its districts list is one road: named once, as scripts/isms.py names it
        sig = tuple(tuple(round(c, 1) for c in p) for p in m['pts'])
        g = groups.get(sig) or groups.get(sig[::-1])
        if g is not None:
            g.append(m); continue
        g = groups[sig] = [m]
        k = per.get(m.get('d'), 0); per[m.get('d')] = k + 1
        R.append(['main', f"{m.get('d')}/main/{k}", (lambda m=m: m['pts']), (lambda v, g=g: [x.__setitem__('pts', v) for x in g])])
    for a in out.get('arterials', []):
        R.append([a['cls'] if a['cls'] in JOIN or a['cls'] == 'bridge' else 'art', 'art/' + a['name'], (lambda a=a: a['pts']), (lambda v, a=a: a.__setitem__('pts', v))])
    return R


def _r(pts):
    return [[round(x, 1), round(y, 1)] for x, y in pts]


def road_ends(out):
    W, H = out['size']
    R = _roads(out)
    wet = unary_union([Polygon(w).buffer(0) for w in (out.get('water') or []) + (out.get('ocean') or [])])
    B = [Polygon(b[1:]).buffer(0) for L in out['buildings'].values() for b in L if len(b) > 3]
    BT = STRtree(B)
    decks = [LineString(s['pts']) for s in out.get('structures', []) if len(s.get('pts', [])) > 1]
    rails = [LineString(out['rail']['pts'])] if out.get('rail') else []
    dist_polys = [Polygon(d['poly'][0]).buffer(0) for d in out['districts']]
    dist_by_id = {d['id']: p for d, p in zip(out['districts'], dist_polys)}

    def hits_house(g, pad=-0.2):
        return any(B[j].buffer(pad).intersects(g) for j in BT.query(g))

    def house_near(g, d):
        return any(B[j].distance(g) < d for j in BT.query(g.buffer(d)))

    ends, cut_away, new_ground = [], [], []
    rep = {'joined': 0, 'trimmed': 0}
    for _pass in range(2):   # a trim can leave another road's end loose: look again
        geoms = [LineString(get()) if len(get()) > 1 else None for _, _, get, _ in R]
        idx = [i for i, g in enumerate(geoms) if g is not None]
        T = STRtree([geoms[i] for i in idx])
        others = lambda q, i, rad: [idx[j] for j in T.query(q.buffer(rad)) if idx[j] != i]
        touch_any = lambda q, i: (any(geoms[j].distance(q) < TOUCH for j in others(q, i, TOUCH))
                                  or any(g.distance(q) < TOUCH for g in decks))
        ends = []
        for i in idx:
            kind, rid, get, put = R[i]
            if kind == 'bridge':   # a bridge lands on its roads: it only counts as something to meet
                continue
            for head in (False, True):   # the start, then the end
                pts = get()
                if len(pts) < 2:
                    break
                g = LineString(pts)
                e, prev = (Point(pts[-1]), Point(pts[-2])) if head else (Point(pts[0]), Point(pts[1]))
                if touch_any(e, i):
                    continue
                rec = {'x': round(e.x, 1), 'y': round(e.y, 1), 'road': rid, 'k': kind}
                if e.x < EDGE or e.y < EDGE or e.x > W - EDGE or e.y > H - EDGE:
                    continue   # it runs on out of Gidi
                if wet.distance(e) < 8:
                    ends.append(dict(rec, t='water')); continue
                L = math.dist((prev.x, prev.y), (e.x, e.y)) or 1.0
                ux, uy = (e.x - prev.x) / L, (e.y - prev.y) / L
                hw = XS.half(kind) if kind in XS.SECTIONS else 3.0
                bl = XS.building_line(kind) + 0.2 if kind in XS.SECTIONS else hw   # no house nearer the new stretch than the building line
                home = dist_by_id.get(rid.split('/')[0]) if kind in ('street', 'lane') else None   # a side street stays in its district
                reach = JOIN.get(kind, 45.0)

                def clear(seg, target):   # no house, no water, no railway, and no other road crossed on the way
                    if hits_house(seg.buffer(bl), pad=0.0) or wet.intersects(seg) or any(r.crosses(seg) for r in rails):
                        return False
                    if home is not None and not home.buffer(2).contains(seg):
                        return False
                    return not any(j != target and geoms[j].intersects(seg) and geoms[j].distance(e) > TOUCH for j in others(seg.centroid, i, seg.length / 2 + 1))

                joined = None
                # straight ahead: the first road the line meets
                ray = LineString([(e.x, e.y), (e.x + ux * reach * AHEAD, e.y + uy * reach * AHEAD)])
                best = None
                for j in others(ray.centroid, i, reach * AHEAD):
                    x = geoms[j].intersection(ray)
                    if x.is_empty:
                        continue
                    for q in getattr(x, 'geoms', [x]):
                        q = q if q.geom_type == 'Point' else Point(q.coords[0])
                        dq = e.distance(q)
                        if dq > 0.5 and (best is None or dq < best[0]):
                            best = (dq, q, j)
                if best and clear(LineString([(e.x, e.y), (best[1].x, best[1].y)]), best[2]):
                    joined = best[1]
                else:   # turning onto the nearest road
                    c = []
                    for j in others(e, i, reach):
                        q = geoms[j].interpolate(geoms[j].project(e))
                        dq = e.distance(q)
                        if 0.5 < dq < reach:
                            turn = math.degrees(math.acos(max(-1, min(1, ((q.x - e.x) * ux + (q.y - e.y) * uy) / dq))))
                            if turn <= TURN_MAX:
                                c.append((dq, q, j))
                    for dq, q, j in sorted(c, key=lambda t: t[0]):
                        if clear(LineString([(e.x, e.y), (q.x, q.y)]), j):
                            joined = q; break
                if joined is None and kind in ('main', 'art', 'exp'):   # a big road heading out of town runs on to the edge of the map
                    tx = min([t for t in ((W - e.x) / ux if ux > 1e-6 else None, -e.x / ux if ux < -1e-6 else None,
                                          (H - e.y) / uy if uy > 1e-6 else None, -e.y / uy if uy < -1e-6 else None) if t is not None] or [1e9])
                    if tx <= OUT_MAX:
                        q = Point(e.x + ux * tx, e.y + uy * tx)
                        seg = LineString([(e.x, e.y), (q.x, q.y)])
                        if clear(seg, -1) and not any(dp.intersects(seg) for dp in dist_polys):
                            joined = q
                if joined is not None:
                    new = pts + [[joined.x, joined.y]] if head else [[joined.x, joined.y]] + pts
                    put(_r(new))
                    new_ground.append((LineString([(e.x, e.y), (joined.x, joined.y)]), kind))
                    rep['joined'] += 1; continue
                # the stretch past the last junction: does it serve anybody?
                ts = []   # where other roads (and decks) meet this one
                band = g.buffer(TOUCH)
                for o in [geoms[j] for j in others(g.centroid, i, g.length / 2 + TOUCH)] + decks:
                    x = o.intersection(band)
                    for piece in getattr(x, 'geoms', [x]):
                        if not piece.is_empty:
                            ts += [g.project(Point(c)) for c in piece.coords]
                if ts:
                    t0 = max(ts) if head else min(ts)
                    stub = substring(g, t0, g.length) if head else substring(g, 0, t0)
                    keep = substring(g, 0, t0) if head else substring(g, t0, g.length)
                    if stub.length > 1 and keep.length >= 10 and not house_near(stub, SERVE):
                        put(_r(keep.coords))
                        cut_away.append((stub, rid, kind))
                        rep['trimmed'] += 1; continue
                if house_near(e, 6.0):
                    ends.append(dict(rec, t='access')); continue
                if kind in HEAD_R:
                    r = HEAD_R[kind]
                    while r >= hw + 1.0 and (hits_house(e.buffer(r)) or wet.intersects(e.buffer(r))):
                        r -= 0.5
                    if r >= hw + 1.0:
                        new_ground.append((e.buffer(r), kind))
                        ends.append(dict(rec, t='close', r=round(r, 1))); continue
                ends.append(dict(rec, t='loose'))
    for x in ends:
        rep[x['t']] = rep.get(x['t'], 0) + 1
    rep['trimmed m'] = round(sum(s.length for s, _, _ in cut_away))
    _follow(out, cut_away, new_ground, rep)
    out['road_ends'] = sorted(ends, key=lambda x: (x['road'], x['x'], x['y']))
    return rep


def _follow(out, cut_away, new_ground, rep):
    """The gutters and furniture follow the roads: cut back with a trimmed road, out of the way of a new stretch."""
    if cut_away:
        by_road = {}
        for stub, rid, kind in cut_away:
            by_road.setdefault(rid, []).append(stub.buffer(XS.walkway_band(kind)[1] + 1.0 if kind in XS.SECTIONS else 4.0, cap_style=2))
        gone, shifted = set(), {}
        for gt in out.get('gutters', []):
            if gt['road'] not in by_road or len(gt['pts']) < 2:
                continue
            g = LineString(gt['pts']).difference(unary_union(by_road[gt['road']]))
            parts = [p for p in getattr(g, 'geoms', [g]) if not p.is_empty and p.length > 2]
            if not parts:
                gone.add(gt['id']); continue
            p = max(parts, key=lambda p: p.length)
            old = LineString(gt['pts'])
            off = old.project(Point(p.coords[0]))   # how far along the old run the kept piece starts
            if old.project(Point(p.coords[-1])) < off:
                p = LineString(list(p.coords)[::-1]); off = old.project(Point(p.coords[0]))
            gt['pts'] = _r(p.coords); gt['len'] = round(p.length, 1)
            if gt.get('blocked'):   # blocked stretches are measured along the run: they move with its start
                gt['blocked'] = [dict(b, **{'from': round(max(0.0, b['from'] - off), 1), 'to': round(min(p.length, b['to'] - off), 1)})
                                 for b in gt['blocked'] if b['to'] - off > 0 and b['from'] - off < p.length and min(p.length, b['to'] - off) > max(0.0, b['from'] - off)]
            shifted[gt['id']] = (off, p.length)
        if gone:
            out['gutters'] = [gt for gt in out['gutters'] if gt['id'] not in gone]
        cr = []
        for c in out.get('gutter_crossings', []):   # a crossing on a cut run moves with its start, or goes with the cut piece
            if c['gutter'] in gone:
                continue
            if c['gutter'] in shifted:
                off, L = shifted[c['gutter']]
                if not (0 <= c['at'] - off <= L):
                    continue
                c = dict(c, at=round(c['at'] - off, 1))
            cr.append(c)
        out['gutter_crossings'] = cr
        rep['gutters cut'] = len(gone)
    zones = [unary_union(v) for v in by_road.values()] if cut_away else []
    ground = [g.buffer(XS.walkway_band(k)[0] + 0.25) if g.geom_type == 'LineString' else g.buffer(0.5) for g, k in new_ground]
    keep, dropped = [], 0
    if zones or ground:
        ZT, GT = STRtree(zones) if zones else None, STRtree(ground) if ground else None
        for f in out.get('furniture', []):
            q = Point(f['x'], f['y'])
            if (ZT is not None and any(zones[j].contains(q) for j in ZT.query(q))) or (GT is not None and any(ground[j].contains(q) for j in GT.query(q))):
                dropped += 1; continue
            keep.append(f)
        out['furniture'] = keep
    rep['furniture moved off'] = dropped
