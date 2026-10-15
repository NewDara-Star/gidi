# The Lagos-isms, placed by rule into the baked city data (docs/ISMS-BUILD.md, docs/LAGOS-ISMS.md).
# Runs inside scripts/bake_web.py after the road clean-up (roadclean.py) and the road heights (roadz.py), once the safe ground is listed.
# One function per ism, each reads the city (`out`) and writes its own lists back into it. Same seed, same isms.
# Hand edits (web/isms-edits.json) are applied last and always win.
# Units: metres, y down, like the rest of the data.
#
# Group 1 (built): open gutters (ism 15), with plank and slab crossings at entrances and side streets.
#   out["gutters"]           runs of gutter beside a road, open or slab-covered, with blocked stretches
#   out["gutter_crossings"]  planks and slabs over an open run
#   out["gutter_rates"]      the rates used per district
# Later groups add a function to ISMS below and a section to docs/ISMS-BUILD.md.
import json, math, os, random, zlib
import numpy as np
import shapely
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import nearest_points, unary_union
from shapely.strtree import STRtree

SEED = 2026
HERE = os.path.dirname(os.path.abspath(__file__))
EDITS_FILE = os.path.join(HERE, "..", "web", "isms-edits.json")

# ---- the roads: widths as the 3D kit draws them (blender/city.py WIDTH, ART_W)
WIDTH = {"lane": 3.5, "street": 7.0, "main": 14.0, "art": 18.0, "exp": 30.0}
RANK = {"lane": 0, "street": 1, "main": 2, "art": 3, "exp": 4}
STEP = 2.0   # sampling step along a gutter, metres

# ---- gutter rates per district (docs/LAGOS-ISMS.md ism 15, the owner's description; OSM does not map gutters)
# has:     chance that a side of a street has a gutter at all (nearly every Lagos side street has one)
# cover:   share of a street's gutter length under slabs
# blocked: share of the OPEN length that is blocked (rubbish or green water)
# w, depth: the channel in metres (40-100 cm wide, up to a metre deep)
# Starting point is the kit's character table (blender/gidi_kit/rules.py STREET): dense mainland mostly open and blocked, elite estates covered.
RATES = {
    "maze":      dict(has=0.97, cover=0.20, blocked=0.50, w=(0.5, 0.9), depth=(0.5, 0.9)),
    "hub":       dict(has=0.95, cover=0.30, blocked=0.40, w=(0.5, 0.9), depth=(0.5, 0.9)),
    "jungle":    dict(has=0.95, cover=0.15, blocked=0.60, w=(0.5, 0.9), depth=(0.5, 0.9)),
    "foodgate":  dict(has=0.93, cover=0.25, blocked=0.50, w=(0.5, 1.0), depth=(0.5, 1.0)),
    "bazaar":    dict(has=0.93, cover=0.30, blocked=0.40, w=(0.5, 0.9), depth=(0.5, 0.9)),
    "watertown": dict(has=0.90, cover=0.08, blocked=0.65, w=(0.4, 0.8), depth=(0.4, 0.7)),
    "railside":  dict(has=0.90, cover=0.25, blocked=0.40, w=(0.5, 0.9), depth=(0.5, 0.9)),
    "frontier":  dict(has=0.75, cover=0.35, blocked=0.15, w=(0.5, 0.9), depth=(0.5, 0.9)),
    "border":    dict(has=0.75, cover=0.25, blocked=0.35, w=(0.4, 0.8), depth=(0.4, 0.7)),
    "oldisland": dict(has=0.98, cover=0.40, blocked=0.55, w=(0.4, 0.7), depth=(0.5, 1.0)),
    "oldshore":  dict(has=0.93, cover=0.35, blocked=0.45, w=(0.4, 0.8), depth=(0.5, 0.9)),
    "port":      dict(has=0.90, cover=0.40, blocked=0.40, w=(0.8, 1.2), depth=(0.7, 1.1)),
    "capital":   dict(has=0.95, cover=0.60, blocked=0.25, w=(0.5, 0.9), depth=(0.5, 0.8)),
    "estate":    dict(has=0.98, cover=0.92, blocked=0.05, w=(0.45, 0.7), depth=(0.45, 0.7)),
    "heights":   dict(has=0.98, cover=0.95, blocked=0.03, w=(0.45, 0.7), depth=(0.45, 0.7)),
}
DEFAULT_RATES = RATES["hub"]
# Wealth of the entrance (chance a plain house gets a slab, not a plank) and share of fronts that are shops: from the kit's character table.
ENTRANCE = {
    "maze": (0.30, 0.35), "hub": (0.35, 0.35), "jungle": (0.20, 0.30), "foodgate": (0.30, 0.35), "bazaar": (0.40, 0.40),
    "watertown": (0.10, 0.20), "railside": (0.30, 0.30), "frontier": (0.50, 0.15), "border": (0.25, 0.25), "oldisland": (0.35, 0.40),
    "oldshore": (0.30, 0.35), "port": (0.35, 0.30), "capital": (0.80, 0.25), "estate": (1.00, 0.05), "heights": (1.00, 0.05),
}
# What a road class changes: mains and arterials are mostly covered (slabs under the walkway) and rarely blocked; lanes carry one gutter.
CLASS = {
    "lane":   dict(has=0.8, cover=0.0, blocked=1.0, w=0.8, sides=1),
    "street": dict(has=1.0, cover=0.0, blocked=1.0, w=1.0, sides=2),
    "main":   dict(has=1.0, cover=0.5, blocked=0.5, w=1.2, sides=2),   # cover: share of the rest that is also covered
    "art":    dict(has=1.0, cover=0.88, blocked=0.3, w=1.2, sides=2),
    "exp":    dict(has=0.9, cover=0.8, blocked=0.2, w=1.5, sides=2),
}
CHUNK = (30.0, 90.0)       # a stretch keeps one state (open or covered) for this long
BLOCK_CELL = 20.0          # blocked stretches come in cells of this length
SAFE_CLEAR = 12.0          # gutters within this of safe ground are covered, never open
BLOCK_CLEAR = 30.0         # nothing is blocked within this of safe ground (a resident standing at the gate sees 25 m)
ENTRANCE_REACH = 9.0       # a building this close to an open run is on it
NOT_ENTRANCE = {"back", "water tank", "generator", "stack", "pen", "trailer", "crane", "column", "flare stack", "mound", "drums", "checkpoint",
                "toll booth", "toll canopy", "border booth", "border canopy", "stilt", "stilt bar", "raft", "barge", "smoke rack", "tank",
                "transformer", "scrap", "canopy", "stage", "stands", "bust", "container", "sawdust", "saw shed", "horse shelter", "fishing hut"}
SHOPS = {"phone mall", "bakery", "print", "cafe", "strip", "nightclub", "hotel", "office block", "warehouse", "plaza", "shed", "beach bar", "beach shack"}


def seeded(*parts):
    return random.Random(zlib.crc32("|".join(str(p) for p in (SEED,) + parts).encode()))


def ring(r):
    return Polygon(r[0] if isinstance(r[0][0], (list, tuple)) else r).buffer(0)


class Ctx:
    """The city, indexed once for every ism."""
    def __init__(self, out):
        self.out = out
        self.districts = [(d["id"], ring(d["poly"])) for d in out["districts"]]
        self.built = {d["id"] for d in out["districts"] if d.get("fabric") == "lagos"}   # built to the agreed cross-sections
        self.roads = []                                  # {id, k, w, d, pts, geom, key}
        for d, lines in out["streets"].items():
            for i, ln in enumerate(lines):
                self.add_road(f"{d}/street/{i}", "street", d, ln)
        for d, lines in out.get("lanes", {}).items():
            for i, ln in enumerate(lines):
                self.add_road(f"{d}/lane/{i}", "lane", d, ln)
        seen = set()
        for i, m in enumerate(out["mains"]):
            sig = tuple(tuple(round(c, 1) for c in p) for p in m["pts"])
            if sig in seen or sig[::-1] in seen:
                continue   # an edge road both its districts list: once
            seen.add(sig)
            self.add_road(f"main/{i}", "main", m.get("d"), m["pts"])
        for a in out["arterials"]:
            if a["cls"] in ("art", "exp"):
                self.add_road("art/" + a["name"], a["cls"], None, a["pts"])
        self.road_tree = STRtree([r["zone"] for r in self.roads])
        # buildings of the whole city
        self.blds = []                                   # (district, index, kind, polygon)
        for d, lst in out["buildings"].items():
            for i, b in enumerate(lst):
                try:
                    p = Polygon(b[1:]).buffer(0)
                except Exception:
                    continue
                if not p.is_empty:
                    self.blds.append((d, i, b[0], p))
        self.bld_tree = STRtree([b[3] for b in self.blds])
        # ground a gutter never runs on: water, rail, canals, ramps and approaches
        nogo = [Polygon(r).buffer(1.0) for r in out["water"] + out["ocean"]]   # a metre of margin: the check reads the unrounded line
        nogo.append(LineString(out["rail"]["pts"]).buffer(4.0))
        for c in out.get("canals", []):
            nogo.append(LineString(c["pts"]).buffer(c.get("width", 4.0) / 2 + 0.8))
        for s in out.get("structures", []):
            if s["kind"] in ("approach", "ramp"):
                nogo.append(LineString(s["pts"]).buffer((s.get("width") or 8) / 2 + 0.5))
        self.nogo = unary_union(nogo)
        shapely.prepare(self.nogo)
        # safe ground (README): churches, mosques, schools, hospitals, clinics, the palaces, the Heritage Strip
        safe = [Polygon(s["pts"]).buffer(SAFE_CLEAR + 2.0) for s in out.get("safe_ground", []) if len(s["pts"]) >= 3]
        self.safe = unary_union(safe) if safe else Polygon()
        shapely.prepare(self.safe)
        self.safe_wide = unary_union([Polygon(s["pts"]).buffer(BLOCK_CLEAR) for s in out.get("safe_ground", []) if len(s["pts"]) >= 3]) if safe else Polygon()
        shapely.prepare(self.safe_wide)
        # compound walls: a gate in a wall is a slab over the gutter
        walls = [LineString(w) for lines in out.get("walls", {}).values() for w in lines if len(w) >= 2]
        self.wall_tree = STRtree(walls) if walls else None

    def add_road(self, rid, k, d, pts):
        if len(pts) < 2:
            return
        g = LineString(pts)
        if g.length < 4:
            return
        XS = self.out.get("cross_sections") or {}
        built = d in self.built or (d is None and k in ("art", "exp") and self.built)
        w = XS[k]["carriageway"] if built and k in XS else WIDTH[k]   # districts built to the agreed cross-sections: their widths
        self.roads.append(dict(id=rid, k=k, w=w, d=d, pts=pts, geom=g, key=(RANK[k], g.length), zone=g.buffer(w / 2 + 0.3), xs=XS.get(k) if built else None))

    def district_at(self, x, y):
        p = Point(x, y)
        for d, poly in self.districts:
            if poly.contains(p):
                return d
        return None


def curves(road, side, off):
    """The gutter's centre line on one side of a road ('R' is the right-hand side when walking along the road on the map, y down)."""
    try:
        c = road["geom"].offset_curve(off if side == "R" else -off, join_style=2, mitre_limit=2.0)
    except Exception:
        return []
    parts = [c] if c.geom_type == "LineString" else [g for g in getattr(c, "geoms", []) if g.geom_type == "LineString"]
    res = []
    for p in parts:
        if p.length < 6:
            continue
        if road["geom"].project(Point(p.coords[0])) > road["geom"].project(Point(p.coords[-1])):
            p = LineString(list(p.coords)[::-1])
        res.append(p)
    return res


def gutters(ctx):
    out = ctx.out
    runs, crossings = [], []
    entrance_best = {}   # building -> (distance, run index, point)
    stats = {}
    for road in ctx.roads:
        k = road["k"]
        cls = CLASS[k]
        # pick which sides; a lane carries one gutter
        rr = seeded("gutter", road["id"])
        sides = ["L", "R"]
        if cls["sides"] == 1:
            sides = [rr.choice(sides)]
        for side in sides:
            rs = seeded("gutter", road["id"], side)
            d0 = road["d"] or ctx.district_at(*road["geom"].interpolate(0.5, normalized=True).coords[0])
            rate0 = RATES.get(d0, DEFAULT_RATES)
            if rs.random() > rate0["has"] * cls["has"]:
                continue
            gw = rs.uniform(*rate0["w"]) * cls["w"]
            depth = rs.uniform(*rate0["depth"])
            off = road["w"] / 2 + 0.3 + gw / 2
            if road.get("xs") and road["xs"]["gutter"] > 0:   # the agreed cross-section: the gutter right beside the carriageway
                gw = road["xs"]["gutter"]; off = road["w"] / 2 + gw / 2
            n = 0
            for curve in curves(road, side, off):
                n = trace(ctx, road, side, curve, gw, depth, rs, runs, crossings, n)
    # entrances: each building onto the nearest open run
    for ri, run in enumerate(runs):
        if run["state"] != "open":
            continue
        run["_geom"] = LineString(run["pts"])
    open_idx = [ri for ri, r in enumerate(runs) if r["state"] == "open"]
    if open_idx:
        run_tree = STRtree([runs[ri]["_geom"] for ri in open_idx])
        bld_pairs = ctx.bld_tree.query([runs[ri]["_geom"] for ri in open_idx], predicate="dwithin", distance=ENTRANCE_REACH)
        best = {}
        for qi, bi in zip(*bld_pairs):
            d, i, kind, poly = ctx.blds[bi]
            if kind in NOT_ENTRANCE:
                continue
            ri = open_idx[qi]
            g = runs[ri]["_geom"]
            dist = poly.distance(g)
            if bi not in best or dist < best[bi][0]:
                best[bi] = (dist, ri)
        for bi, (dist, ri) in sorted(best.items()):
            d, i, kind, poly = ctx.blds[bi]
            run = runs[ri]
            g = run["_geom"]
            pt = nearest_points(poly, g)[1]
            at = g.project(pt)
            if at < 1.0 or at > g.length - 1.0:
                continue
            re_ = seeded("entrance", d, i)
            wealth, shop = ENTRANCE.get(d, (0.4, 0.3))
            if kind == "stalls":
                ck, w, mat = "slab", re_.uniform(5.0, 10.0), "concrete"      # in front of a busy stall row the gutter disappears under a run of slabs
            elif kind == "kiosk":
                ck, w, mat = "slab", re_.uniform(2.0, 3.0), "concrete"
            elif kind in SHOPS or (kind == "front" and re_.random() < shop * 0.5):
                ck, w, mat = "slab", re_.uniform(2.5, 4.5), "concrete"
            elif re_.random() < wealth:
                ck, w, mat = "slab", re_.uniform(1.6, 2.6) if wealth < 0.9 else re_.uniform(3.0, 4.0), "concrete"
            else:
                ck, w = "plank", re_.uniform(0.9, 1.4)
                mat = re_.choices(["plank", "old door", "metal sheet"], [0.6, 0.25, 0.15])[0]
            crossings.append(dict(gutter=run["id"], at=at, w=w, kind=ck, mat=mat, of="entrance", bld=[d, i], _g=g))
    return finish(ctx, runs, crossings)


def trace(ctx, road, side, curve, gw, depth, rs, runs, crossings, n):
    """Walk one gutter curve: classify each sample, cut it into open and covered runs, mark blocked stretches and side-street crossings."""
    L = curve.length
    ts = np.arange(0.0, L + 1e-6, STEP)
    if ts[-1] < L - 0.5:
        ts = np.append(ts, L)
    pts = shapely.line_interpolate_point(curve, ts)
    xy = shapely.get_coordinates(pts)
    nsamp = len(ts)
    hard = shapely.contains_xy(ctx.nogo, xy[:, 0], xy[:, 1])          # water, rail, canals, ramps
    # other roads: a lesser road meeting this one is a side-street mouth (a crossing); a bigger one cuts the gutter short
    mouth = {}
    for pi, rj in zip(*ctx.road_tree.query(pts, predicate="intersects")):
        other = ctx.roads[rj]
        if other is road:
            continue
        if road["key"] > other["key"]:
            mouth.setdefault(pi, rj)
        else:
            hard[pi] = True
    # chunk plan, same seed whatever the geometry: each chunk is open or covered
    d_mid = road["d"] or ctx.district_at(*xy[nsamp // 2])
    rates = RATES.get(d_mid, DEFAULT_RATES)
    cls = CLASS[road["k"]]
    p_cover = rates["cover"] + (1 - rates["cover"]) * cls["cover"] if road["k"] != "street" else rates["cover"]
    if road["k"] == "lane":
        p_cover = rates["cover"] * 0.6
    chunks, t = [], 0.0
    while t < L + CHUNK[1]:
        step = rs.uniform(*CHUNK)
        chunks.append((t + step, rs.random() < p_cover))
        t += step
    covered = np.zeros(nsamp, bool)
    ci = 0
    for i, tt in enumerate(ts):
        while chunks[ci][0] < tt:
            ci += 1
        covered[i] = chunks[ci][1]
    # under a building front or a wall gate the gutter is slabbed; near safe ground it is covered and never blocked
    near_bld = np.zeros(nsamp, bool)
    for pi in set(ctx.bld_tree.query(pts, predicate="intersects")[0]):
        near_bld[pi] = True
    if ctx.wall_tree is not None:
        for pi in set(ctx.wall_tree.query(pts, predicate="dwithin", distance=0.5)[0]):
            near_bld[pi] = True
    near_safe = shapely.contains_xy(ctx.safe, xy[:, 0], xy[:, 1])
    covered |= near_bld | near_safe
    # runs: unbroken stretches of the same state
    i = 0
    stretches = []
    while i < nsamp:
        if hard[i]:
            i += 1
            continue
        j = i
        while j + 1 < nsamp and not hard[j + 1] and covered[j + 1] == covered[i]:
            j += 1
        stretches.append((i, j))
        i = j + 1
    # fill gaps of under 6 m between covered stretches with cover, drop slivers
    made = []
    for (a, b) in stretches:
        length = ts[b] - ts[a]
        if length < 4.0:
            continue
        line = LineString(xy[a:b + 1]).simplify(0.25)
        if line.length < 4.0:
            continue
        pieces = [("covered" if covered[a] else "open", line)]
        if not covered[a]:   # an open run never goes through a house: the clipped part is slabbed
            hit = [ctx.blds[q][3] for q in ctx.bld_tree.query(line, predicate="dwithin", distance=0.4)]
            if hit:
                cut = unary_union(hit).buffer(0.4)
                pieces = []
                for state, geom in (("open", line.difference(cut)), ("covered", line.intersection(cut))):
                    for g in getattr(geom, "geoms", [geom]):
                        if g.geom_type == "LineString" and g.length >= 3.0:
                            pieces.append((state, g))
                pieces.sort(key=lambda sp: line.project(Point(sp[1].coords[0])))
        for state, g in pieces:
            rid = f"{road['id']}:{side}:{n}"
            n += 1
            run = dict(id=rid, road=road["id"], d=road["d"] or ctx.district_at(*xy[(a + b) // 2]), kind=road["k"], side=side,
                       state=state, w=round(gw, 2), depth=round(depth, 2),
                       pts=[[round(x, 1), round(y, 1)] for x, y in g.coords], len=round(g.length, 1), _t=(ts[a], ts[b], a, b))
            if state == "open":
                blk = blocked_stretches(ctx, run, g, near_safe[a:b + 1], rs)
                if blk:
                    run["blocked"] = blk
            runs.append(run)
            made.append(run)
    # side-street mouths on this curve: a slab over an open run
    if mouth:
        idx = sorted(mouth)
        groups, cur = [], [idx[0]]
        for q in idx[1:]:
            if q == cur[-1] + 1 and mouth[q] == mouth[cur[0]]:
                cur.append(q)
            else:
                groups.append(cur); cur = [q]
        groups.append(cur)
        for gp in groups:
            other = ctx.roads[mouth[gp[0]]]
            span = ts[gp[-1]] - ts[gp[0]] + STEP
            mid = (ts[gp[0]] + ts[gp[-1]]) / 2
            if span > other["w"] + 6 or mid < 3 or mid > L - 3:
                continue   # a long overlap, not a mouth; or too near the end of the road
            here = curve.interpolate(mid)
            cand = [r for r in made if r["_t"][2] <= gp[0] and gp[-1] <= r["_t"][3] and r["state"] == "open"]
            run = min(cand, key=lambda r: LineString(r["pts"]).distance(here), default=None)
            if run is None or LineString(run["pts"]).distance(here) > 1.5:
                continue
            g = LineString(run["pts"])
            at = g.project(here)
            w = min(max(span, other["w"] * 0.8), other["w"] + 2.0)
            crossings.append(dict(gutter=run["id"], at=at, w=w, kind="slab", mat="concrete", of="street", road=other["id"], _g=g))
    return n


def blocked_stretches(ctx, run, line, safe_flags, rs):
    """Rubbish or green water, in cells of ~20 m; more near market stalls."""
    rates = RATES.get(run["d"], DEFAULT_RATES)
    cls = CLASS[run["kind"]]
    share = min(0.95, rates["blocked"] * cls["blocked"])
    if share <= 0:
        return []
    L = line.length
    ncell = max(1, int(round(L / BLOCK_CELL)))
    cells = []
    for c in range(ncell):
        a, b = L * c / ncell, L * (c + 1) / ncell
        mid = line.interpolate((a + b) / 2)
        p = share
        # stalls beside the gutter: the traders' rubbish goes in
        near = ctx.bld_tree.query(mid.buffer(14.0), predicate="intersects")
        if any(ctx.blds[q][2] == "stalls" for q in near):
            p = min(0.95, p + 0.35)
        blk = rs.random() < p
        rub = rs.random() < 0.55
        if ctx.safe_wide.contains(mid):
            blk = False
        cells.append((a, b, blk, rub))
    res = []
    for a, b, blk, rub in cells:
        if not blk:
            continue
        fill = "rubbish" if rub else "green_water"
        if res and abs(res[-1]["to"] - a) < 0.5 and res[-1]["fill"] == fill:
            res[-1]["to"] = round(b, 1)
        else:
            res.append(dict(**{"from": round(a, 1), "to": round(b, 1), "fill": fill}))
    return res


def finish(ctx, runs, crossings):
    """Drop crossings that overlap, number the rest, strip the working fields."""
    by_run = {}
    for c in crossings:
        by_run.setdefault(c["gutter"], []).append(c)
    final = []
    for rid, cs in by_run.items():
        cs.sort(key=lambda c: c["at"])
        kept = []
        for c in cs:
            if kept and c["at"] - kept[-1]["at"] < (c["w"] + kept[-1]["w"]) / 2 + 0.4:
                p = kept[-1]   # overlapping: one longer slab (street mouths first, then the wider)
                if c["of"] == "street" and p["of"] != "street":
                    kept[-1] = c
                elif c["w"] > p["w"] and p["of"] == c["of"]:
                    p["w"] = c["w"]
                continue
            kept.append(c)
        final.extend(kept)
    res = []
    counter = {}
    for c in sorted(final, key=lambda c: (c["gutter"], c["at"])):
        g = c["_g"]
        n = counter.get(c["gutter"], 0)
        counter[c["gutter"]] = n + 1
        pt = g.interpolate(c["at"])
        a = g.interpolate(max(0, c["at"] - 1.0)); b = g.interpolate(min(g.length, c["at"] + 1.0))
        ang = math.degrees(math.atan2(b.y - a.y, b.x - a.x))
        rec = dict(id=f"{c['gutter']}:c{n}", gutter=c["gutter"], at=round(c["at"], 1), pt=[round(pt.x, 1), round(pt.y, 1)], ang=round(ang),
                   kind=c["kind"], mat=c["mat"], w=round(c["w"], 1), of=c["of"])
        if c["of"] == "entrance":
            rec["bld"] = c["bld"]
        else:
            rec["road"] = c["road"]
        res.append(rec)
    for r in runs:
        r.pop("_t", None); r.pop("_geom", None)
    ctx.out["gutters"] = runs
    ctx.out["gutter_crossings"] = res
    ctx.out["gutter_rates"] = {"seed": SEED, "per_district": {d: {k: v for k, v in r.items()} for d, r in RATES.items()},
                               "per_class": CLASS, "sides": "L = left, R = right when walking along the road's points on the map (y down)"}
    return summary(ctx)


def summary(ctx):
    out = ctx.out
    per = {}
    for r in out["gutters"]:
        s = per.setdefault(r["d"] or "(arterials)", dict(runs=0, open_m=0.0, covered_m=0.0, blocked_m=0.0, crossings=0))
        s["runs"] += 1
        s["open_m" if r["state"] == "open" else "covered_m"] += r["len"]
        s["blocked_m"] += sum(b["to"] - b["from"] for b in r.get("blocked", []))
    runs = {r["id"]: r for r in out["gutters"]}
    for c in out["gutter_crossings"]:
        r = runs.get(c["gutter"])
        if r:
            per[r["d"] or "(arterials)"]["crossings"] += 1
    return per


# ---- hand edits: web/isms-edits.json
# {"gutters": {"add": [run, ...], "delete": [id, ...], "edit": {id: {field: value, ...}}},
#  "gutter_crossings": {"add": [...], "delete": [...], "edit": {...}}}
# Add, move (edit "pts" or "pt") or delete any one item by id. Applied after the rules, so a hand edit always wins.
def apply_edits(out, path=EDITS_FILE):
    warnings = []
    if not os.path.exists(path):
        return warnings
    ed = json.load(open(path))
    for coll, ops in ed.items():
        if coll.startswith("_") or not isinstance(ops, dict):
            continue
        items = out.setdefault(coll, [])
        byid = {it["id"]: it for it in items}
        for iid in ops.get("delete", []):
            if iid in byid:
                items.remove(byid.pop(iid))
            else:
                warnings.append(f"{coll}: delete {iid}: no such item")
        for iid, fields in ops.get("edit", {}).items():
            if iid in byid:
                byid[iid].update(fields)
                byid[iid]["hand"] = True
            else:
                warnings.append(f"{coll}: edit {iid}: no such item")
        for it in ops.get("add", []):
            if it.get("id") in byid:
                warnings.append(f"{coll}: add {it.get('id')}: id already used")
                continue
            it = dict(it, hand=True)
            items.append(it)
            byid[it["id"]] = it
    if "gutters" in ed:   # a deleted run takes its crossings with it, unless they were added by hand
        ids = {r["id"] for r in out["gutters"]}
        out["gutter_crossings"] = [c for c in out["gutter_crossings"] if c["gutter"] in ids or c.get("hand")]
    return warnings


# ---- the isms, in order. Each takes the indexed city and writes its lists into it.
ISMS = [("gutters", gutters)]


def run(out, edits=EDITS_FILE):
    """Place every ism into `out` (the city data before it is written), then apply the hand edits. Returns {ism: summary} and warnings."""
    ctx = Ctx(out)
    report = {name: fn(ctx) for name, fn in ISMS}
    return report, apply_edits(out, edits)


if __name__ == "__main__":   # standalone: python3 scripts/isms.py  (reads web/gidi-data.js, prints the summary, writes nothing)
    src = open(os.path.join(HERE, "..", "web", "gidi-data.js")).read()
    city = json.loads(src[len("window.GIDI="):-1])
    city.pop("gutters", None); city.pop("gutter_crossings", None)
    rep, warn = run(city)
    for name, per in rep.items():
        print(name)
        for d, s in sorted(per.items()):
            tot = s["open_m"] + s["covered_m"]
            print(f"  {d:10s} {tot/1000:6.1f} km  open {s['open_m']/max(tot,1):4.0%}  blocked {s['blocked_m']/max(s['open_m'],1):4.0%} of open  crossings {s['crossings']}")
    for w in warn:
        print("WARNING", w)
