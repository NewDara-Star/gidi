# Road heights, run by bake_web.py after the road clean-up (scripts/roadclean.py). Pass 2 of the road work.
#
# Ground roads follow the ground: their height is web/terrain.json under them, so they carry no z of their own.
# Everything that leaves the ground gets a height profile in the data, the master copy the 3D kit and the
# Unreal importer read:
#   - every deck in out["structures"] (flyovers, rail bridges, skywalks, footbridges, jetties) and every
#     bridge in out["arterials"] gets "z": deck-top height in metres above the water (0), one per point of
#     its "pts" (which are resampled every STEP m), plus "clear": the least headroom under it and what it is over.
#   - a deck that must climb higher than its own length allows is lengthened along the road it carries, so
#     its ramps never pass MAX_GRADE: flyovers and rail bridges along their own main road (the road stays at
#     grade beside the ramp as the service road, as in Lagos), bridges by new "approach" decks on the roads
#     that lead onto them.
#   - waterfront roads that the lagoon outline cut through (the R5 roads the clean-up could not move) get a
#     sea wall: the water is pushed back off the road and its shoulder, and out["quays"] gives each wall's line
#     and top height. Land behind a wall is made up to QUAY_TOP.
#   - a road crossing a canal gets a "culvert" deck level with the road; a footpath out over the water in a
#     stilt village becomes one of out["boardwalks"]; houses standing where a bridge lands are cleared.
#   - canals carry their water width ("width", 4 m: gen_fabric keeps 2 m a side, bank paths at 3 m, houses at 4 m).
# Numbers are game choices on real Lagos lines: 5.5 m under a flyover (FMW's 5.3 m minimum, rounded up for
# trucks), 6 m over rail, canoes need 4 m under a lagoon bridge and the ferry channel 8 m (the Cable Bridge 12).
import json, math
import numpy as np
from shapely.geometry import LineString, Point, Polygon, MultiPolygon
from shapely.ops import unary_union, substring

STEP = 5.0
CLEAR = {'shore': 1.5, 'road': 5.5, 'rail': 6.0, 'water': 4.0, 'channel': 8.0, 'cable channel': 12.0, 'canal': 2.0}
DEPTH = {'flyover': 1.2, 'bridge': 1.8, 'skywalk': 0.6, 'footbridge': 0.3, 'jetty': 0.3}
MAX_GRADE = {'flyover': 0.065, 'bridge': 0.04}
SHORE_SPAN = 120.0   # water this near the shore is too shallow for boats: the deck may come down over it
QUAY_TOP = 1.5    # top of a sea wall above the water; the road behind it sits there
QUAY_PAD = 4.0    # land kept between the road's edge and the water
WIDTH = {'main': 14.0, 'exp': 30.0, 'art': 18.0, 'bridge': 22.0, 'street': 7.0}


class Ground:
    def __init__(self, T):
        self.Z = np.array(T['z'], float).reshape(T['h'], T['w']) / 10.0
        self.C = T['cell_m']

    def __call__(self, x, y):
        """Bilinear height of the ground (water 0) at x, y."""
        C, Z = self.C, self.Z
        fx, fy = x / C - 0.5, y / C - 0.5
        j0, i0 = int(math.floor(fx)), int(math.floor(fy))
        tx, ty = fx - j0, fy - i0
        def at(i, j):
            return Z[min(max(i, 0), Z.shape[0] - 1), min(max(j, 0), Z.shape[1] - 1)]
        return (at(i0, j0) * (1 - tx) * (1 - ty) + at(i0, j0 + 1) * tx * (1 - ty)
                + at(i0 + 1, j0) * (1 - tx) * ty + at(i0 + 1, j0 + 1) * tx * ty)


def resample(g, step=STEP):
    n = max(1, int(math.ceil(g.length / step)))
    return [g.interpolate(g.length * k / n) for k in range(n + 1)]


def pieces(g):
    return [g] if g.geom_type == 'Polygon' else [p for p in getattr(g, 'geoms', []) if p.geom_type == 'Polygon']


def no_holes(p):
    """A polygon with holes (water round an island) as plain pieces, cut through each hole's middle (as scripts/layout_v2.py does)."""
    from shapely.geometry import box as _box
    if p.geom_type != 'Polygon' or not p.interiors:
        return [p] if p.geom_type == 'Polygon' else [q for g in getattr(p, 'geoms', []) for q in no_holes(g)]
    c = Polygon(p.interiors[0]).centroid; x0, y0, x1, y1 = p.bounds
    out_ = []
    for half in (_box(x0 - 1, y0 - 1, c.x, y1 + 1), _box(c.x, y0 - 1, x1 + 1, y1 + 1)):
        out_ += no_holes(p.intersection(half))
    return [q for q in out_ if q.geom_type == 'Polygon' and q.area > 1]


def heights(out, water, ocean, T):
    ground = Ground(T)
    report = {'quays': 0, 'quay_m': 0, 'extended': [], 'low': [], 'decks': 0}

    # ---- 1. sea walls: push the water back off the waterfront roads still standing in it
    wet = water.union(ocean)
    walls = []
    for m in out['mains']:
        g = LineString(m['pts'])
        on = g.intersection(wet)
        if on.length <= 3:
            continue
        cut = g.buffer(WIDTH['main'] / 2 + QUAY_PAD, cap_style=2)
        walls.append(cut)
        report['quays'] += 1
        report['quay_m'] += on.length
    if walls:
        W = unary_union(walls)
        # the wall works round what floats or stands in the water (rafts, stilt houses, stilt bars): they stay moored in it
        afloat = [Polygon(b[1:]).buffer(1.5) for L in out.get('buildings', {}).values() for b in L if len(b) > 3 and b[0] in ('raft', 'stilt', 'stilt bar')]
        if afloat:
            W = W.difference(unary_union(afloat))
        new_w, new_o = water.difference(W), ocean.difference(W)
        def biggest(g):
            ps = sorted(pieces(g), key=lambda p: -p.area)
            return [p for p in ps if p.area > 2000] or ps[:1]
        ws, os_ = biggest(new_w), biggest(new_o)
        out['water'] = [[[round(x, 1), round(y, 1)] for x, y in q.exterior.coords] for p in ws for q in no_holes(p)]   # the map keeps plain
        out['ocean'] = [[[round(x, 1), round(y, 1)] for x, y in q.exterior.coords] for p in os_ for q in no_holes(p)]  # outlines: an island's water is cut, not holed
        water, ocean = unary_union(ws), unary_union(os_)
        wet_new = water.union(ocean)
        # the wall: where the new shore runs along a carved road
        quays = []
        for c in pieces(W):
            edge = c.boundary.intersection(wet.buffer(0.5)).intersection(wet_new.buffer(0.5))
            for ln in getattr(edge, 'geoms', [edge]):
                if ln.geom_type == 'LineString' and ln.length > 8:
                    quays.append({'pts': [[round(x, 1), round(y, 1)] for x, y in ln.simplify(0.5).coords], 'top': QUAY_TOP})
        out['quays'] = quays
    wet = water.union(ocean)
    shore = unary_union([w.boundary for w in pieces(wet)])   # every shore, an island's too (its hole's ring)
    canals = unary_union([LineString(c['pts']).buffer(c.get('width', 4.0) / 2) for c in out.get('canals', [])]) if out.get('canals') else None

    # ---- what a deck can pass over: roads at the ground, the rail, and other decks (filled in as they get heights)
    below = []
    for kind, key in (('street', 'streets'), ('lane', 'lanes')):
        for d, L in (out.get(key) or {}).items():
            for p in L:
                if len(p) > 1:
                    below.append(('road', LineString(p), 7.0 if kind == 'street' else 3.5, None))
    for m in out['mains']:
        below.append(('road', LineString(m['pts']), WIDTH['main'], None))
    for a in out['arterials']:
        if a['cls'] != 'bridge':
            below.append(('road', LineString(a['pts']), WIDTH[a['cls']], None))
    rails = [LineString(out['rail']['pts'])] if out.get('rail') else []
    for r in rails:
        below.append(('rail', r, 10.0, None))

    # a house standing in a bridge's own footprint on the land (where it lands) cannot stay: the bridge mouth is cleared
    ON_DECK = ('toll booth', 'toll canopy')
    report['cleared'] = []
    bands = [LineString(a['pts']).buffer(WIDTH['bridge'] / 2) for a in out['arterials'] if a['cls'] == 'bridge']
    if bands:
        BU = unary_union(bands)
        for d, L in out.get('buildings', {}).items():
            keep = [i for i, b in enumerate(L) if not (len(b) > 3 and b[0] != 'stilt' and b[0] not in ON_DECK
                                                       and not wet.contains(Polygon(b[1:]).centroid) and Polygon(b[1:]).buffer(0).intersects(BU))]
            if len(keep) < len(L):
                for i in set(range(len(L))) - set(keep):
                    c = Polygon(L[i][1:]).centroid
                    report['cleared'].append(f"{d} {L[i][0]} at ({c.x:.0f}, {c.y:.0f})")
                for key in ('buildings', 'storeys', 'styles'):
                    arr = (out.get(key) or {}).get(d)
                    if arr is not None and len(arr) == len(L):
                        out[key][d] = [arr[i] for i in keep]

    # buildings a deck may pass over: it clears their roofs (storeys of 3.2 m, a stilt house 4.5 m above the water)
    from shapely.strtree import STRtree
    BLD = []
    for d, L in out.get('buildings', {}).items():
        st = (out.get('storeys') or {}).get(d) or []
        for i, b in enumerate(L):
            if len(b) > 3 and b[0] not in ON_DECK:
                h = 4.5 if b[0] == 'stilt' else 3.2 * (st[i] if i < len(st) else 1) + 1.0
                BLD.append((Polygon(b[1:]).buffer(0), h, b[0]))
    BT = STRtree([p for p, h, k in BLD])

    def ground_at(p):
        return 0.0 if wet.contains(p) else ground(p.x, p.y)

    def profile(host, s0, s1, kind, own=None, channel=None, span=None):
        """Deck tops along host between s0 and s1 (metres along it). Returns (pts, z, needs) where needs is
        how much longer each end must be to meet the ground within MAX_GRADE (0 when it already does)."""
        g = substring(host, s0, s1)
        P = resample(g)
        S = [k * g.length / (len(P) - 1) for k in range(len(P))]
        G_ = [ground_at(p) for p in P]
        need = [-1e9] * len(P)   # the least deck top at each station
        over = []
        dep = DEPTH['bridge' if kind in ('bridge', 'approach') else kind]
        # water under it
        for i, p in enumerate(P):
            if kind in ('jetty', 'flyover'):
                break   # a jetty sits on the water; a flyover's ramps over a creek are causeway, not navigation
            if wet.contains(p) and p.distance(shore) <= SHORE_SPAN and not (channel and channel[0] <= S[i] <= channel[1]):
                need[i] = max(need[i], CLEAR['shore'] + dep)   # a low shore span: no boat under it, but never in the water
            elif wet.contains(p):
                c = CLEAR['water']
                if channel and channel[0] <= S[i] <= channel[1]:
                    c = channel[2]
                need[i] = max(need[i], c + dep)
            elif canals is not None and canals.contains(p):
                need[i] = max(need[i], G_[i] - 1.5 + CLEAR['canal'] + dep)
        if any(wet.contains(p) for p in P):
            over.append('water')
        # roads, rail and lower decks it crosses (a jetty sits on the water at the shore road's end: nothing passes under it)
        for what, ln, w, zfun in (below if kind != 'jetty' else []):
            if own is not None and ln.equals_exact(own, 0.5):
                continue
            if not ln.intersects(g) or ln.intersection(g).geom_type not in ('Point', 'MultiPoint'):
                continue
            x = ln.intersection(g)
            for q in getattr(x, 'geoms', [x]):
                sc = g.project(q)
                end_zone = 50 if kind == 'bridge' else 1   # a road this near a bridge's end is where it lands
                if sc < end_zone or sc > g.length - end_zone:
                    continue   # it meets the deck at its end: a junction, not something under it
                if span is not None and not (span[0] - s0 - 3 <= sc <= span[1] - s0 + 3):
                    continue   # a side road crossing under a ramp meets the service road at grade beside it
                zb = zfun(q) if zfun else ground_at(q)
                req = zb + CLEAR['rail' if what == 'rail' else 'road'] + dep
                # level across the road below and a few metres either side (the crossing angle widens it)
                a1 = math.atan2(*reversed(np.subtract(g.interpolate(min(g.length, sc + 2)).coords[0], g.interpolate(max(0, sc - 2)).coords[0])))
                p1, p2 = ln.interpolate(max(0, ln.project(q) - 2)), ln.interpolate(min(ln.length, ln.project(q) + 2))
                a2 = math.atan2(p2.y - p1.y, p2.x - p1.x)
                sn = max(0.35, abs(math.sin(a1 - a2)))
                half = (w / 2) / sn + 3
                for i in range(len(P)):
                    if abs(S[i] - sc) <= half:
                        need[i] = max(need[i], req)
                over.append(what if what != 'deck' else 'deck')
        if span is not None and kind == 'flyover' and not over:
            # a rail bridge over a district's own rail (not in the city data): the rail is under the middle of the span
            sc = (span[0] + span[1]) / 2 - s0
            q = g.interpolate(sc)
            for i in range(len(P)):
                if abs(S[i] - sc) <= 8:
                    need[i] = max(need[i], ground_at(q) + CLEAR['rail'] + dep)
            over.append('rail')
        if kind in ('bridge', 'approach', 'flyover'):
            band = g.buffer((WIDTH['bridge'] if kind != 'flyover' else 10.0) / 2)
            for j in BT.query(band):
                bp, h, bk = BLD[j]
                if not bp.intersects(band):
                    continue
                roof = (0.0 if bk == 'stilt' else ground_at(bp.representative_point())) + h + 1.0
                for i, p in enumerate(P):
                    if span is not None and not (span[0] - s0 - 3 <= S[i] <= span[1] - s0 + 3):
                        continue   # under a ramp it's a house on the road, for the checks to catch, not something to fly over
                    if bp.distance(p) < (WIDTH['bridge'] if kind != 'flyover' else 10.0) / 2:
                        need[i] = max(need[i], roof + dep)
                over.append('buildings')
        if kind in ('skywalk', 'footbridge', 'jetty'):
            top = max([n for n in need if n > -1e8] or [0])
            if kind == 'jetty':
                z = [max(ground_at(p), 0.0) + 1.0 for p in P]
            elif kind == 'footbridge':
                z = [max(top, G_[i] + 1.3) for i in range(len(P))]
            else:
                z = [max(top, G_[i] + CLEAR['road'] + dep) if top < 0 else top for i in range(len(P))]   # stairs at both ends
            return P, z, (0.0, 0.0), over, S, need
        gr = MAX_GRADE['bridge' if kind in ('bridge', 'approach') else 'flyover']
        # widen each level stretch by 15 m a side, so rounding the crests below never eats into the headroom
        wide = list(need)
        for i in range(len(P)):
            if need[i] > -1e8:
                for j in range(max(0, i - 3), min(len(P), i + 4)):
                    wide[j] = max(wide[j], need[i])
        z = []
        for i in range(len(P)):
            best = G_[i] + 0.05
            for j in range(len(P)):
                if wide[j] > -1e8:
                    best = max(best, wide[j] - gr * 0.9 * abs(S[i] - S[j]))
            z.append(best)
        # round the crests a little (a vertical curve), never below what is needed
        zs = list(z)
        for i in range(len(P)):
            lo, hi = max(0, i - 3), min(len(P), i + 4)
            zs[i] = max(sum(z[lo:hi]) / (hi - lo), need[i] if need[i] > -1e8 else -1e9, G_[i] + 0.05)
        z = zs
        needs = tuple(max(0.0, (z[e] - (G_[e] + 0.05)) / gr) for e in (0, -1))
        return P, z, needs, over, S, need

    def clear_report(P, z, S, need, over):
        lows = [round(z[i] - need[i], 2) for i in range(len(P)) if need[i] > -1e8]
        return min(lows) if lows else None

    def write(s, P, z, over, name):
        s['pts'] = [[round(p.x, 1), round(p.y, 1)] for p in P]
        s['z'] = [round(v, 2) for v in z]
        s['over'] = sorted(set(over))
        report['decks'] += 1

    def chain(end, away, length, skip, max_turn=95):
        """The roads leading on from a bridge end, straightest first, for `length` metres."""
        roads = [(a['name'], LineString(a['pts'])) for a in out['arterials'] if a['cls'] != 'bridge'] + [(m.get('name') or '', LineString(m['pts'])) for m in out['mains']] \
            + [('street', LineString(p)) for L in (out.get('streets') or {}).values() for p in L if len(p) > 1]
        pts = [end]
        P_ = Point(end)
        got = 0.0
        heading = away
        for _ in range(6):
            best = None
            for n, r in roads:
                if r.distance(P_) > 25 or r.equals_exact(skip, 0.5):
                    continue
                t = r.project(P_)
                for sgn in (1, -1):
                    t2 = t + sgn * 10
                    if t2 < 0 or t2 > r.length:
                        continue
                    q = r.interpolate(t2)
                    h = math.atan2(q.y - P_.y, q.x - P_.x)
                    turn = abs((h - heading + math.pi) % (2 * math.pi) - math.pi)
                    if turn < math.radians(max_turn) and (best is None or turn < best[0]):
                        best = (turn, r, t, sgn, n)
            if best is None:
                break
            _, r, t, sgn, n = best
            take = min(length - got, (r.length - t) if sgn > 0 else t)
            seg = substring(r, t, t + take) if sgn > 0 else substring(r, t, t - take)
            cs = list(seg.coords)
            pts += [c for c in cs[1:]]
            got += seg.length
            P_ = Point(cs[-1])
            if got >= length - 1 or take < 5:
                break
            a, b = cs[-2], cs[-1]
            heading = math.atan2(b[1] - a[1], b[0] - a[0])
            skip = r
        return LineString(pts) if len(pts) > 1 and LineString(pts).length > 1 else None

    # ---- 2. flyovers and rail bridges along their own main road: lengthen the ramps as needed
    mains = [(m.get('name') or '', LineString(m['pts'])) for m in out['mains']]
    hosts = mains + [(a['name'], LineString(a['pts'])) for a in out['arterials'] if a['cls'] != 'bridge']
    order = sorted([s for s in out.get('structures', []) if s['kind'] == 'flyover'], key=lambda s: s.get('layer', 1))
    for s in order:
        # its line as drawn (`base`), never last bake's ramps: a frozen district hands its decks back with their ramps on,
        # and measuring from those grew the ramps a little more every bake (Folake Road's 78 m rail bridge had reached 538 m)
        s.setdefault('base', s['pts'])
        g = LineString(s['base'])
        host = max(hosts, key=lambda m: m[1].intersection(g.buffer(3)).length)[1]
        if host.intersection(g.buffer(3)).length < g.length * 0.6:
            host = g   # not along a main (an interchange deck): it keeps its own line
        # carry the host on past its ends into the roads that lead on, so a ramp never runs out of road
        hc = list(host.coords)
        back = chain(hc[0], math.atan2(hc[0][1] - hc[1][1], hc[0][0] - hc[1][0]), 400, host)
        fwd = chain(hc[-1], math.atan2(hc[-1][1] - hc[-2][1], hc[-1][0] - hc[-2][0]), 400, host)
        host = LineString((list(back.coords)[::-1][:-1] if back else []) + hc + (list(fwd.coords)[1:] if fwd else []))
        s0, s1 = sorted((host.project(Point(g.coords[0])), host.project(Point(g.coords[-1]))))
        a0, a1 = s0, s1
        for _ in range(4):
            P, z, needs, over, S, need = profile(host, a0, a1, 'flyover', own=host, span=(s0, s1))
            if needs[0] < 1 and needs[1] < 1:
                break
            a0, a1 = max(0.0, a0 - needs[0] - 5), min(host.length, a1 + needs[1] + 5)
        grown = (s0 - a0) + (a1 - s1)
        if grown > 1:
            report['extended'].append(f"{s['name']} ({s['d']}): {g.length:.0f} m -> {(a1 - a0):.0f} m, so its ramps stay under {MAX_GRADE['flyover'] * 100:.1f}%")
        end_gap = max(z[0] - ground_at(P[0]), z[-1] - ground_at(P[-1]))
        if end_gap > 0.3:
            report['low'].append(f"{s['name']}: its road ends before the ramp can come down ({end_gap:.1f} m up at the end)")
        c = clear_report(P, z, S, need, over)
        write(s, P, z, over, s['name'])
        s['clear'] = c
        dz = dict(zip([(round(p.x, 1), round(p.y, 1)) for p in P], z))
        line = LineString([(p.x, p.y) for p in P])
        def zf(q, line=line, P=P, z=z):
            t = line.project(q) / line.length * (len(P) - 1)
            i = min(int(t), len(P) - 2)
            return z[i] + (z[i + 1] - z[i]) * (t - i)
        below.append(('deck', line, s.get('width', 10), zf))

    # ---- 3. bridges over the water: clear everywhere, a channel in the middle, ramps on the land
    approaches = []
    # a bridge that runs on past the shore road it lands on (into the blocks behind) ends at that road, in a T
    land_roads = [LineString(m['pts']) for m in out['mains']] + [LineString(a['pts']) for a in out['arterials'] if a['cls'] != 'bridge']
    for a in out['arterials']:
        if a['cls'] != 'bridge':
            continue
        g = LineString(a['pts'])
        for e in (0, -1):
            cut = None
            for r in land_roads:
                x = g.intersection(r)
                for q in getattr(x, 'geoms', [x]):
                    if q.geom_type == 'Point':
                        t = g.project(q)
                        d = t if e == 0 else g.length - t
                        if 5.0 < d <= 50 and (cut is None or d < cut[0]):   # nearer than 5 m it is the junction itself
                            cut = (d, t)
            if cut:
                old_end = Point(g.coords[0 if e == 0 else -1])
                g = substring(g, cut[1], g.length) if e == 0 else substring(g, 0, cut[1])
                # a short link that joined the old end to the shore road now leads nowhere: it goes
                new_end = Point(g.coords[0 if e == 0 else -1])
                out['mains'] = [m for m in out['mains'] if not (LineString(m['pts']).length < 30 and LineString(m['pts']).distance(old_end) < 1
                                                                and LineString(m['pts']).distance(new_end) > 1)]
                report['extended'].append(f"{a['name']}: ended at the shore road it crossed, {cut[0]:.0f} m short of where it stopped (it ran on into the blocks)")
        a['pts'] = [[round(x, 1), round(y, 1)] for x, y in g.coords]
    for a in out['arterials']:
        if a['cls'] != 'bridge':
            continue
        g = LineString(a['pts'])
        ow = [x for x in getattr(g.intersection(wet), 'geoms', [g.intersection(wet)]) if x.length > 0]
        cable = 'Cable' in a['name']
        if ow:
            s_w0 = min(g.project(Point(x.coords[0])) for x in ow); s_w1 = max(g.project(Point(x.coords[-1])) for x in ow)
            mid, span = (s_w0 + s_w1) / 2, max(60.0, (s_w1 - s_w0) * 0.25)
            channel = (mid - span / 2, mid + span / 2, CLEAR['cable channel' if cable else 'channel'])   # headroom; the deck's depth is added in profile()
        else:
            channel = None
        P, z, needs, over, S, need = profile(g, 0, g.length, 'bridge', own=g, channel=channel)
        # the deck holds its height to the ends; approaches on the land bring it down
        top_end = (z[0], z[-1])
        for e, (pt, nxt) in enumerate(((g.coords[0], g.coords[1]), (g.coords[-1], g.coords[-2]))):
            gz = ground_at(Point(pt))
            if top_end[e] - gz <= 0.3:
                continue
            L = (top_end[e] - gz) / MAX_GRADE['bridge'] + 10
            away = math.atan2(pt[1] - nxt[1], pt[0] - nxt[0])
            # landing part-way along a road (a T): that road rises from both sides to meet it; else the road that leads straight on
            P0 = Point(pt)
            aps = []
            at = [r for r in land_roads if r.distance(P0) < 8 and 10 < r.project(P0) < r.length - 10]
            if at:
                r = max(at, key=lambda r: r.length)
                t = r.project(P0)
                aps = [x for x in (substring(r, t, min(r.length, t + L)), substring(r, t, max(0, t - L))) if x.length > 5]
                for k, x in enumerate(aps):   # a side that runs out of road carries on into the next one
                    if x.length < L - 1:
                        cs = list(x.coords)
                        more = chain(cs[-1], math.atan2(cs[-1][1] - cs[-2][1], cs[-1][0] - cs[-2][0]), L - x.length, r, max_turn=60)
                        if more is not None:
                            aps[k] = LineString(cs + list(more.coords)[1:])
            if not aps:
                ap = chain(pt, away, L, g, max_turn=50)
                aps = [ap] if ap is not None and ap.length >= L * 0.6 else []
            if aps:
                ap = aps[0]
            if not aps:
                report['low'].append(f"{a['name']}: no road on the land to carry its {'west/north' if e == 0 else 'east/south'} approach ({L:.0f} m needed, {0 if ap is None else ap.length:.0f} m found); the ramp comes down over the water")
                if ap is None:
                    continue
            for ap in aps:
                Q = resample(ap)
                Sa = [k * ap.length / (len(Q) - 1) for k in range(len(Q))]
                za = [max(ground_at(q) + 0.05, top_end[e] - MAX_GRADE['bridge'] * s) for q, s in zip(Q, Sa)]
                approaches.append({'kind': 'approach', 'name': f"{a['name']} approach", 'd': None, 'layer': 1, 'width': WIDTH['main'],   # the road it climbs on
                                   'pts': [[round(q.x, 1), round(q.y, 1)] for q in Q], 'z': [round(v, 2) for v in za], 'over': [], 'clear': None})
                report['extended'].append(f"{a['name']}: a {ap.length:.0f} m approach on the land at its {'first' if e == 0 else 'last'} end" + (" (the shore road rises to meet it)" if len(aps) > 1 else ""))
        # if an approach was short, let the deck come down over the water near that shore instead
        for e in (0, 1):
            if not any(x['name'] == f"{a['name']} approach" and Point(x['pts'][0]).distance(Point(g.coords[0 if e == 0 else -1])) < 10 for x in approaches):
                gz = ground_at(Point(g.coords[0 if e == 0 else -1]))
                rng = range(len(P)) if e == 0 else range(len(P) - 1, -1, -1)
                for k, i in enumerate(rng):
                    z[i] = min(z[i], gz + 0.05 + MAX_GRADE['bridge'] * S[k] if e == 0 else gz + 0.05 + MAX_GRADE['bridge'] * (S[-1] - S[i]))
        c = clear_report(P, z, S, need, over)
        if c is not None and c < -0.05:
            i = min((i for i in range(len(P)) if need[i] > -1e8), key=lambda i: z[i] - need[i])
            report['low'].append(f"{a['name']}: lowest at ({P[i].x:.0f}, {P[i].y:.0f}), {S[i]:.0f} m along, deck {z[i]:.1f} m where {need[i]:.1f} m is needed")
        write(a, P, z, over, a['name'])
        a['clear'] = c
        if channel:
            a['channel'] = [round(channel[0], 1), round(channel[1], 1), channel[2]]   # from, to (m along), headroom
    out.setdefault('structures', []).extend(approaches)

    # ---- 4. skywalks, footbridges and jetties: level decks (stairs at the ends), or just above the water
    for s in out.get('structures', []):
        if s['kind'] in ('skywalk', 'footbridge', 'jetty'):
            g = LineString(s['pts'])
            P, z, needs, over, S, need = profile(g, 0, g.length, s['kind'], own=None)
            c = clear_report(P, z, S, need, over)
            write(s, P, z, over, s['name'])
            s['clear'] = c
    # ---- 6. a footpath out over the water in a stilt village is a plank boardwalk on stilts, like the village's others
    stilts = [Polygon(b[1:]) for L in out.get('buildings', {}).values() for b in L if b[0] == 'stilt' and len(b) > 3]
    if stilts:
        village = unary_union(stilts).buffer(40)
        have = {json.dumps(b) for b in out.get('boardwalks', [])}
        report['boardwalks'] = 0
        for d, L in (out.get('paths') or {}).items():
            for p in L:
                pts = p['pts'] if isinstance(p, dict) else p
                g = LineString(pts)
                if g.length > 0 and g.intersection(wet).length > 0.5 * g.length and g.intersection(village).length > 0.5 * g.length and json.dumps(pts) not in have:
                    out.setdefault('boardwalks', []).append(pts)
                    report['boardwalks'] += 1

    # ---- 5. culverts: a road crossing a canal does it on a slab over a culvert, level with the road (Lagos's way)
    culverts = []
    if out.get('canals'):
        cl = [LineString(c['pts']) for c in out['canals']]
        roads = [(k[:-1], d, LineString(p)) for k in ('streets', 'lanes') for d, L in (out.get(k) or {}).items() for p in L if len(p) > 1]
        roads += [('main', m.get('d'), LineString(m['pts'])) for m in out['mains']]
        roads += [(a['cls'], None, LineString(a['pts'])) for a in out['arterials'] if a['cls'] != 'bridge']
        for k, d, r in roads:
            for c in cl:
                x = r.intersection(c)
                for q in getattr(x, 'geoms', [x]):
                    if q.geom_type != 'Point':
                        continue
                    t = r.project(q)
                    p1, p2 = c.interpolate(max(0, c.project(q) - 2)), c.interpolate(min(c.length, c.project(q) + 2))
                    r1, r2 = r.interpolate(max(0, t - 2)), r.interpolate(min(r.length, t + 2))
                    sn = max(0.3, abs(math.sin(math.atan2(p2.y - p1.y, p2.x - p1.x) - math.atan2(r2.y - r1.y, r2.x - r1.x))))
                    h = min(15.0, 3.0 / sn + 1.5)   # the 4 m of water, its banks, and a little either side
                    g = substring(r, max(0, t - h), min(r.length, t + h))
                    if g.length < 2:
                        continue
                    P = resample(g, 2.0)
                    culverts.append({'kind': 'culvert', 'name': 'Canal culvert', 'd': d, 'layer': 0, 'width': WIDTH.get(k, 3.5 if k == 'lane' else 7.0),
                                     'pts': [[round(p.x, 1), round(p.y, 1)] for p in P], 'z': [round(ground(p.x, p.y), 2) for p in P], 'over': ['canal'], 'clear': None})
    out['structures'].extend(culverts)
    report['culverts'] = len(culverts)
    for s in out.get('structures', []) + [a for a in out['arterials'] if a['cls'] == 'bridge']:
        if s.get('clear') is not None and s['clear'] < -0.05:
            report['low'].append(f"{s['name']}: {-s['clear']:.1f} m short of its headroom")
    return water, ocean, report
