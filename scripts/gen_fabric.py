# Original street + building generator for one Gidi district.
# Nothing here is copied from a real map: the inputs are only the statistics in study-<id>.json / study-<id>-core.json
# (spacing, block size, junction mix, house sizes, setbacks, gaps, land-use shares) and Gidi's own districts, arterials and rail.
# Usage: python3 scripts/gen_fabric.py maze [seed]
import json, math, random, sys, os
import numpy as np
from shapely.geometry import Polygon, LineString, Point, box, MultiLineString
from shapely.ops import unary_union, polygonize, nearest_points, substring, linemerge
from shapely.affinity import rotate, translate
from shapely.strtree import STRtree
sys.path.insert(0, "scripts"); from fabric_metrics import measure, lines, extend, noded

DID = sys.argv[1]; SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 7
SCALE = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0   # one calibration knob: stretches street spacing until the network matches the study
OUT = sys.argv[4] if len(sys.argv) > 4 else f"web/gen-{DID}.json"
rnd = random.Random(SEED)
ST = json.load(open(f"study-{DID}.json")); CORE = json.load(open(f"study-{DID}-core.json"))
s = open("web/gidi-data.js").read(); G = json.loads(s[len("window.GIDI="):-1])
DIST = {d["id"]: d for d in G["districts"]}; POLY = {k: Polygon(v["poly"][0]) for k, v in DIST.items()}
poly = POLY[DID]; water = Polygon(G["water"][0]); land = poly.difference(water)

# ---------- rules from the study (Mushin + Shomolu) ----------
def sampler(pc, lo, hi):
    qs = [0.0] + [int(k[1:]) / 100 for k in pc] + [1.0]; vs = [lo] + list(pc.values()) + [hi]
    return lambda u=None: float(np.interp(rnd.random() if u is None else u, qs, vs))
RULE = {
    "rib_spacing": sampler(ST["parallel_street_spacing_m"], 40, 190),          # distance between parallel streets
    "cross_every": sampler({"p25": 120, "p50": 150, "p75": 185}, 95, 240),     # block long side ~ 2 x short side (elongation p50 2.0)
    "short_side": sampler(ST["buildings"]["short_side_m"], 3.0, 18),
    "long_side": sampler(ST["buildings"]["long_side_m"], 4.5, 34),
    "gap": sampler(ST["buildings"]["gap_to_nearest_neighbour_m"], 0.0, 6),
    "dead_end": 0.12,          # share of ribs that stop short (dead-end : junction ~ 0.12-0.31 in the core squares)
    "x_junction": 0.5,         # share of cross streets that line up with the next one (X); the rest are staggered T's
    "perp_front": 0.69,        # front-row houses: long side runs back from the street (gable to street) 69%, parallel 31%
    "back_row": 0.85,          # chance a plot gets a second building behind (face-me-I-face-you compound)
    "outbuilding": 0.2,       # chance of a small shed / kiosk / toilet block in a plot
    "sector_split_ha": 14.0,    # sectors larger than this are split by a collector street (fan sections; neighbours turn ~35 deg)
}
CLEAR = {"lane": 2.2, "street": 3.4, "main": 6.5, "art": 12.5, "exp": 15, "rail": 6.0, "canal": 4.0}   # building edge to centreline, minimum
WIDTH = {"street": 5.5, "main": 10, "art": 22}
FIRST = ["Adeyemi","Okafor","Bello","Ayinde","Ogundipe","Balogun","Lawal","Adebayo","Eze","Musa","Akande","Oladipo","Afolabi","Ibrahim","Adeleke","Oyelaran","Kalejaiye","Bankole","Odusanya","Ajasa","Fadipe","Oshinowo","Salami","Olatunji","Abeni","Taiwo","Kehinde","Idowu","Alaba","Ireti","Folake","Agboola","Shonibare","Ilori","Durojaiye","Ogunleye","Aremu","Okonkwo","Nwosu","Danjuma"]
ENDS = [("Street", 60), ("Road", 13), ("Avenue", 4), ("Close", 4), ("Way", 4), ("Crescent", 2), ("Lane", 2)]   # from street_name_endings
used = set()
def street_name(kind="street"):
    for _ in range(200):
        e = "Road" if kind == "main" and rnd.random() < .6 else rnd.choices([e for e, w in ENDS], [w for e, w in ENDS])[0]
        n = f"{rnd.choice(FIRST)} {e}"
        if n not in used: used.add(n); return n
    return n

# ---------- 1. the network shared with the rest of Gidi ----------
NET_F = "web/network.json"
NET = json.load(open(NET_F)) if os.path.exists(NET_F) else {"edges": {}, "gateways": []}
arts = [(a["name"], a["cls"], LineString(a["pts"])) for a in G["arterials"] if a["cls"] != "bridge" and LineString(a["pts"]).distance(poly) < 160]
rail = LineString(G["rail"]["pts"]); rail_in = rail.intersection(poly.buffer(30))
coords = list(poly.exterior.coords)[:-1]
edge_roads = []
for i in range(len(coords)):
    a, b = coords[i], coords[(i + 1) % len(coords)]; e = LineString([a, b])
    nb = max((k for k in POLY if k != DID), key=lambda k: POLY[k].buffer(25).intersection(e).length)
    if POLY[nb].buffer(25).intersection(e).length < 0.5 * e.length: nb = None
    key = "|".join(sorted([DID, nb])) if nb else f"{DID}|outer{i}"
    if key not in NET["edges"]:  # gently bent so it doesn't read as a ruler line (sinuosity ~1.0 with small kinks)
        L = e.length; n = max(3, int(L // 200)); pts = [a]
        for j in range(1, n):
            p = e.interpolate(j / n, normalized=True); nx_, ny_ = -(b[1] - a[1]) / L, (b[0] - a[0]) / L; o = rnd.uniform(-16, 16)
            pts.append((p.x + nx_ * o, p.y + ny_ * o))
        pts.append(b)
        NET["edges"][key] = {"between": [DID, nb], "name": street_name("main"), "pts": [[round(x, 1), round(y, 1)] for x, y in pts]}
    edge_roads.append((NET["edges"][key]["name"], LineString(NET["edges"][key]["pts"]), nb))
# the district's working outline is the ring of its (gently bent) edge roads, so streets meet them exactly
ring_poly = max(polygonize(unary_union([e for n, e, nb in edge_roads])), key=lambda p: p.area)
land = ring_poly.difference(water)
# corners close to an arterial get a short link to it, so the edge roads join the city network
links = []
for c in coords:
    for n, k, a in arts:
        d = a.distance(Point(c))
        if 20 < d < 170 and not poly.buffer(-5).contains(nearest_points(a, Point(c))[0]):
            links.append(LineString([c, nearest_points(a, Point(c))[0].coords[0]]))

# internal mains: one through-route crossing the district (gateways on both sides), one half-route that T's into it.
# Main density target ~3 km/km2 (dense core square 3.1); edge roads count half because neighbours share them.
def through_main(e1, e2, t1, t2, bend):
    p, q = e1.interpolate(t1, normalized=True), e2.interpolate(t2, normalized=True)
    m = LineString([p, q]).interpolate(rnd.uniform(.4, .6), normalized=True)
    L = p.distance(q); nx_, ny_ = -(q.y - p.y) / L, (q.x - p.x) / L
    k = (m.x + nx_ * bend, m.y + ny_ * bend)
    return LineString([p.coords[0], k, q.coords[0]])
# pick the two longest opposite edges for the through route, avoiding arterial corridors
E = [(i, e) for i, (n, e, nb) in enumerate(edge_roads)]
pairs = [(i, j) for i in range(len(E)) for j in range(len(E)) if i < j and E[i][1].distance(E[j][1]) > 300]
best = None
for i, j in pairs:
    for t in range(40):
        t1, t2 = rnd.uniform(.35, .65), rnd.uniform(.35, .65)
        ln = through_main(E[i][1], E[j][1], t1, t2, rnd.uniform(-35, 35))
        # stay clear of arterials running parallel; crossing them is fine
        def cross_angle(a):
            x = ln.intersection(a)
            if x.is_empty: return 90 if ln.distance(a) > 120 else 0
            p = x if x.geom_type == "Point" else x.geoms[0]; d = a.project(p); q1, q2 = a.interpolate(max(0, d - 20)), a.interpolate(min(a.length, d + 20))
            d2 = ln.project(p); r1, r2 = ln.interpolate(max(0, d2 - 20)), ln.interpolate(min(ln.length, d2 + 20))
            t = abs(math.degrees(math.atan2(q2.y - q1.y, q2.x - q1.x) - math.atan2(r2.y - r1.y, r2.x - r1.x))) % 180
            return min(t, 180 - t)
        ang_ok = all(cross_angle(a) >= 55 for n, k, a in arts) and cross_angle(rail) >= 40
        score = (0 if ang_ok else 1e4) + ln.distance(poly.centroid) * 2 + abs(ln.length - 1000) * .2
        if best is None or score < best[0]: best = (score, ln, (i, j))
mains = [(street_name("main"), best[1])]
# half-route from another edge into the through-route, on the biggest leftover piece
pieces = list(polygonize(unary_union([e for n, e, nb in edge_roads] + [a for n, k, a in arts] + [best[1], rail])))
pieces = [p.intersection(land) for p in pieces if poly.buffer(-5).intersects(p.representative_point())]
big = max(pieces, key=lambda p: p.area)
cand = None
for n, e, nb in edge_roads:
    if e.distance(big) > 5: continue
    for t in range(30):
        p = e.interpolate(rnd.uniform(.25, .75), normalized=True)
        q = nearest_points(best[1], p)[1]
        ln = LineString([p, q])
        if not big.buffer(1).contains(ln.interpolate(.5, normalized=True)) or ln.length < 250: continue
        # meet the through-route at a near-right angle
        sc = abs(ln.length - 520)
        if cand is None or sc < cand[0]: cand = (sc, ln)
if cand: mains.append((street_name("main"), cand[1]))
NET["gateways"] = [g for g in NET["gateways"] if g["from"] != DID]
def add_gate(pt, nb, road, kind, bearing=None):
    NET["gateways"].append({"from": DID, "to": nb, "road": road, "kind": kind, "pt": [round(pt.x, 1), round(pt.y, 1)], **({"bearing_deg": round(bearing)} if bearing is not None else {})})
for n, ln in mains:  # gateways where internal mains reach the district edge: the neighbour continues the road from here
    for en, e, nb in edge_roads:
        for end in (Point(ln.coords[0]), Point(ln.coords[-1])):
            if nb and end.distance(e) < 2: add_gate(end, nb, n, "main")
for n, k, a in arts:  # arterials crossing the edge
    for en, e, nb in edge_roads:
        x = a.intersection(e)
        for p in getattr(x, "geoms", [x]):
            if p.geom_type == "Point" and nb: add_gate(p, nb, n, "arterial")
for en, e, nb in edge_roads:  # rail crossing the edge
    x = rail.intersection(e)
    for p in getattr(x, "geoms", [x]):
        if p.geom_type == "Point" and nb: add_gate(p, nb, "Gidi Rail", "rail")
# canal (real: ~0.76 km of canal/drain/stream per km2) - one open canal following the land, with culverts under streets
canal = None
gc = next((p for p in G["pois"] if p["d"] == DID and "Canal" in p["name"]), None)
if gc:
    c0 = Point(gc["x"], gc["y"]); ang = rnd.uniform(0, math.pi); pts = []
    for t in np.linspace(-1, 1, 9):
        pts.append((c0.x + math.cos(ang) * 340 * t + rnd.uniform(-12, 12), c0.y + math.sin(ang) * 340 * t + rnd.uniform(-12, 12)))
    canal = LineString(pts).intersection(land.buffer(-12))
    canal = max(lines(canal), key=lambda l: l.length) if not canal.is_empty else None

# ---------- 2. sectors and residential streets ----------
hard = [e for n, e, nb in edge_roads] + [a for n, k, a in arts] + [ln for n, ln in mains] + links
sector_lines = unary_union(hard + [rail])
sectors = [p.intersection(land) for p in polygonize(sector_lines) if poly.buffer(-3).contains(p.representative_point())]
sectors = [p for p in sectors if p.area > 2000]
rail_zone = rail.buffer(9)
def frontage_angle(P):  # bearing of the longest piece of road frontage around a sector
    best = (0, 0)
    for n, e in [("road", x) for x in hard] + [("rail", rail)]:
        sh = P.exterior.intersection(e.buffer(2))
        for seg in lines(sh) if not sh.is_empty else []:
            c = list(seg.coords); a = math.atan2(c[-1][1] - c[0][1], c[-1][0] - c[0][0])
            if seg.length > best[0]: best = (seg.length, a + (math.pi / 2 if n == "rail" else 0))  # along a rail, streets run parallel to it
    return best[1]
def split_big(P):
    out = []
    if P.area < RULE["sector_split_ha"] * 1e4: return [P]
    r = P.minimum_rotated_rectangle; c = list(r.exterior.coords)
    l1, l2 = Point(c[0]).distance(Point(c[1])), Point(c[1]).distance(Point(c[2]))
    a, b = ((c[0], c[1]), (c[3], c[2])) if l1 > l2 else ((c[1], c[2]), (c[0], c[3]))
    t = rnd.uniform(.4, .6); ca = LineString(a).interpolate(t, normalized=True); cb = LineString(b).interpolate(t + rnd.uniform(-.12, .12), normalized=True)
    # the collector runs across the long axis -> two sections with their own orientation
    cut = LineString([ca, cb]).buffer(0.01)
    parts = [g for g in getattr(P.difference(cut), "geoms", [P.difference(cut)]) if g.area > 1000]
    collectors.append(LineString([ca, cb]).intersection(P))
    for g in parts: out += split_big(g)
    return out
collectors = []
secs2 = []
for P in sectors: secs2 += split_big(P)
streets = []
for P in secs2:
    th = frontage_angle(P) + math.radians(rnd.uniform(-6, 6))
    c = P.centroid; Pr = rotate(P, -th, origin=c, use_radians=True)  # frontage now runs along x; ribs run along y
    minx, miny, maxx, maxy = Pr.bounds
    xs = []; x = minx + rnd.uniform(20, 55)
    while x < maxx - 25: xs.append(x); x += SCALE * RULE["rib_spacing"](rnd.uniform(0.2, 0.97))
    ribs = []
    for x in xs:
        tilt = math.radians(rnd.uniform(-3.5, 3.5)); H = maxy - miny + 80
        ln = LineString([(x - math.sin(tilt) * H / 2, (miny + maxy) / 2 - math.cos(tilt) * H / 2), (x + math.sin(tilt) * H / 2, (miny + maxy) / 2 + math.cos(tilt) * H / 2)])
        bow = rnd.uniform(-1, 1) * rnd.choice([0, 3, 6, 9])                 # most streets straight, some bow a little
        ln = LineString([ln.coords[0], (x + bow, (miny + maxy) / 2), ln.coords[1]])
        seg = [g for g in lines(ln.intersection(Pr)) if g.length > 30]
        for g in seg:
            if rnd.random() < RULE["dead_end"] and g.length > 110:  # stop short inside the block: a dead end
                keep = rnd.uniform(.45, .8); g = substring(g, 0, g.length * keep) if rnd.random() < .5 else substring(g, g.length * (1 - keep), g.length)
            ribs.append(g)
    # cross streets between neighbouring ribs, staggered so most junctions are T's
    ribs.sort(key=lambda g: g.centroid.x)
    walls = [Pr.exterior]  # the sector edge is a road: cross streets may run to it too
    cols = [None] + ribs + [None]
    prev = []
    for k in range(len(cols) - 1):
        L, R = cols[k], cols[k + 1]
        lx = L.centroid.x if L else minx; rx = R.centroid.x if R else maxx
        if rx - lx < 25: continue
        y = miny + rnd.uniform(40, 120); cur = []
        while y < maxy - 40:
            yy = y
            if prev and rnd.random() < RULE["x_junction"]: yy = min(prev, key=lambda v: abs(v - y))
            probe = LineString([(lx - 80, yy), (rx + 80, yy)])
            def hit(G2, from_left):
                if G2 is None:
                    x = probe.intersection(Pr.exterior); pts = [p for p in getattr(x, "geoms", [x]) if p.geom_type == "Point"]
                    pts = [p for p in pts if (p.x < (lx + rx) / 2) == from_left]
                    return max(pts, key=lambda p: p.x) if from_left and pts else (min(pts, key=lambda p: p.x) if pts else None)
                x = probe.intersection(G2); return x if x.geom_type == "Point" else None
            pa, pb = hit(L, True), hit(R, False)
            if pa is not None and pb is not None and pb.x - pa.x > 18:
                sg = LineString([pa, pb])
                if Pr.buffer(0.5).contains(sg): streets.append(rotate(sg, th, origin=c, use_radians=True)); cur.append(yy)
            y += SCALE * RULE["cross_every"]()
        prev = cur
    streets += [rotate(g, th, origin=c, use_radians=True) for g in ribs]
streets += [g for c in collectors for g in lines(c)]
# keep residential streets off the rail (they stop short: people cross on foot) and clip to land
streets = [g for s in streets for g in lines(s.difference(rail_zone)) if g.length > 18]
# snap: dangling ends within 12 m of another line get extended to it (no near-misses)
snap_tree = STRtree(streets + hard); snap_all = streets + hard
def snap(g):
    c = list(g.coords)
    for end in (0, -1):
        p = Point(c[end]); best = None
        for i in snap_tree.query(p.buffer(12)):
            o = snap_all[i]
            if o is g: continue
            d = p.distance(o)
            if best is None or d < best[0]: best = (d, o)
        if best and 0.3 < best[0] < 12: c[end] = nearest_points(best[1], p)[0].coords[0]
    return LineString(c)
streets = [snap(g) for g in streets]
# clean-up: node the network and prune spurs shorter than 15 m (slivers left by clipping), repeat until stable
import networkx as nx
def prune(streets):
    hardU = unary_union(hard)
    U = unary_union([extend(x, 1.0) for x in streets] + hard + [rail_zone.exterior])
    segs = [sg for sg in lines(U) if not hardU.buffer(0.05).contains(sg) and not rail_zone.exterior.buffer(0.05).contains(sg)]
    kk = lambda c: (round(c[0], 2), round(c[1], 2))
    hard_nodes = set()
    for h in lines(U):
        if hardU.buffer(0.05).contains(h) or rail_zone.exterior.buffer(0.05).contains(h): hard_nodes |= {kk(h.coords[0]), kk(h.coords[-1])}
    for _ in range(6):
        Gx = nx.MultiGraph()
        for sg in segs: Gx.add_edge(kk(sg.coords[0]), kk(sg.coords[-1]))
        for n in hard_nodes:
            if n in Gx: Gx.add_edge(n, ("hard",))  # a node on a main road / rail edge counts as connected
        dead = {n for n, d in Gx.degree() if d == 1}
        keep = [sg for sg in segs if not ((kk(sg.coords[0]) in dead or kk(sg.coords[-1]) in dead) and sg.length < 15)]
        if len(keep) == len(segs): break
        segs = keep
    m = linemerge(segs)
    return list(getattr(m, "geoms", [m]))
streets = prune(streets)
# no block bigger than the real 90th percentile (~3.2 ha): split oversize blocks with a street across their long axis
for _ in range(3):
    big = [b for b in polygonize(noded(streets + hard + [rail])) if land.buffer(1).contains(b.representative_point()) and b.area > ST["blocks"]["area_m2"]["p90"]]
    if not big: break
    for b in big:
        mr = b.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
        e1, e2 = ((cc[0], cc[1]), (cc[3], cc[2])) if math.dist(cc[0], cc[1]) >= math.dist(cc[1], cc[2]) else ((cc[1], cc[2]), (cc[0], cc[3]))
        f = rnd.uniform(.4, .6); p1 = LineString(e1).interpolate(f, normalized=True); p2 = LineString(e2).interpolate(f, normalized=True)
        ln = LineString([(p1.x + (p1.x - p2.x), p1.y + (p1.y - p2.y)), (p2.x + (p2.x - p1.x), p2.y + (p2.y - p1.y))]).intersection(b)
        streets += [g for g in lines(ln) if g.length > 20]

# a few residential streets carry straight on into the neighbour (real: ~0.9 per km of edge); the rest T into the edge road
for en, e, nb in edge_roads:
    if not nb: continue
    ends = []
    for g in streets:
        for i0, i1 in ((0, 1), (-1, -2)):
            p = Point(g.coords[i0])
            if p.distance(e) < 1.0:
                q = Point(g.coords[i1]); ends.append((p, math.degrees(math.atan2(p.x - q.x, -(p.y - q.y))) % 360))
    rnd.shuffle(ends); n_keep = max(1, round(0.9 * e.length / 1000))
    for p, brg in ends[:n_keep]: add_gate(p, nb, "", "street", brg)
# ---------- 3. parcels for the places a neighbourhood needs ----------
net_lines = [("street", g) for g in streets] + [("main", e) for n, e, nb in edge_roads] + [("main", ln) for n, ln in mains] + [("main", l) for l in links] + [(k, a) for n, k, a in arts]
blocks = [b for b in polygonize(noded([g for k, g in net_lines] + [rail])) if land.buffer(1).contains(b.representative_point()) and b.area > 120]
mainU = unary_union([g for k, g in net_lines if k != "street"])
parcels = []
def take(kind, near_pt, want_ha, near_main=True, max_dist=None):
    cands = [b for b in blocks if not any(b.intersects(p["geom"]) for p in parcels)]
    if near_main: cands = [b for b in cands if b.distance(mainU) < 3]
    else: cands = [b for b in cands if 0.6 * want_ha * 1e4 < b.area < 1.8 * want_ha * 1e4 and 30 < b.centroid.distance(mainU) < 200] or cands
    if max_dist: cands = [b for b in cands if b.distance(near_pt) < max_dist] or cands
    b = min(cands, key=lambda b: b.distance(near_pt) + abs(b.area - want_ha * 1e4) / 40)
    g = b
    if b.area > want_ha * 1e4 * 1.4 and near_main:  # only the part of the block that faces the main road
        for r in range(20, 200, 5):
            g = b.intersection(mainU.buffer(r))
            if g.area >= want_ha * 1e4: break
    g = g.buffer(-2)
    if g.geom_type != "Polygon": g = max(getattr(g, "geoms", [g]), key=lambda x: x.area)
    parcels.append({"kind": kind, "geom": g}); return g
P = {p["name"]: Point(p["x"], p["y"]) for p in G["pois"] if p["d"] == DID}
c0 = poly.centroid
mk = next((n for n in P if "Market" in n), None)
poi_pos = {}
if mk: g = take("market", P[mk], 1.4); poi_pos[mk] = g.representative_point()        # markets front main roads, median 1.4 ha
yard = next((n for n in P if "Yard" in n), None)
ind_ha = max(1.5, ST["landuse_polygons_ha"].get("industrial", [0, 0])[1] / ST["area_km2"] / 100 * land.area / 1e4)  # ~3.8% of land
if yard: g = take("industrial", P[yard], min(ind_ha, 3.0)); poi_pos[yard] = g.representative_point()
take("school", c0, 0.8, near_main=False)                                              # schools sit ~65 m back from mains
take("pitch", c0, 0.3, near_main=False)
take("motor park", Point(poly.bounds[0], poly.bounds[1]), 0.25)
parcel_u = unary_union([p["geom"] for p in parcels])

# service lanes (real: ~3 km per km2 of service ways): deep blocks get a dead-end lane so their middle can be built on
lanes = []
for b in blocks:
    if b.area < 12000 or parcel_u.buffer(-1).intersects(b.representative_point()): continue
    mr = b.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
    s1, s2 = Point(cc[0]).distance(Point(cc[1])), Point(cc[1]).distance(Point(cc[2]))
    if min(s1, s2) < 105: continue
    ext = list(b.exterior.coords); p, q = max(zip(ext, ext[1:]), key=lambda e: math.dist(*e))
    L = math.dist(p, q); ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L; nx_, ny_ = -uy, ux
    k = max(1, int(L // 110))                                   # one lane per ~110 m of frontage
    for i in range(k):
        f = (i + 0.5) / k + rnd.uniform(-.08, .08)
        m0 = (p[0] + ux * L * f, p[1] + uy * L * f); nx2, ny2 = nx_, ny_
        if not b.contains(Point(m0[0] + nx2 * 3, m0[1] + ny2 * 3)): nx2, ny2 = -nx2, -ny2
        depth = min(s1, s2) - rnd.uniform(35, 50)
        ln = LineString([m0, (m0[0] + nx2 * depth, m0[1] + ny2 * depth)]).intersection(b.buffer(-1))
        for g in lines(ln):
            if g.length > 25: lanes.append(LineString([m0] + [g.coords[-1]]))
# ---------- 4. buildings: plots along every street frontage, compounds behind ----------
clear_geoms = [g.buffer(2.2) for g in lanes] + [g.buffer(CLEAR.get(k, 3.4)) for k, g in net_lines] + [rail.buffer(CLEAR["rail"])]
if canal: clear_geoms.append(canal.buffer(CLEAR["canal"]))
blocked = unary_union(clear_geoms + [parcel_u.buffer(1.0)])
buildable = land.difference(blocked)
bld = []; tree = None
def free(r, pad=0.0):
    if not buildable.contains(r): return False
    for o in near(r):
        if o.distance(r) < pad: return False
    return True
grid = {}
def near(r):
    x, y = r.centroid.x, r.centroid.y; out = []
    for i in (-1, 0, 1):
        for j in (-1, 0, 1): out += grid.get((int(x // 30) + i, int(y // 30) + j), [])
    return out
def near_all(b):
    x0, y0, x1, y1 = b.bounds; out = []
    for i in range(int(x0 // 30), int(x1 // 30) + 1):
        for j in range(int(y0 // 30), int(y1 // 30) + 1): out += [r for r in grid.get((i, j), []) if b.contains(r.centroid)]
    return out
def add(r, kind):
    bld.append((r, kind)); x, y = r.centroid.x, r.centroid.y; grid.setdefault((int(x // 30), int(y // 30)), []).append(r)
def rect(cx, cy, w, d, a):  # w along the street, d back from it
    return translate(rotate(box(-w / 2, -d / 2, w / 2, d / 2), a, use_radians=True), cx, cy)
def size(lo_u=0.0):
    u = rnd.uniform(lo_u, 1); u2 = min(.99, max(.01, u + rnd.uniform(-.25, .25)))  # short and long side are correlated
    sh, lo = RULE["short_side"](u), RULE["long_side"](u2)
    return min(sh, lo), max(sh, lo)
# Plots: the neighbourhood is built plot by plot. Each block's frontage is cut into plots about one house wide (+ gap);
# each plot runs back towards the middle of the block. Inside a plot: front house (gable to the street 69% of the time),
# a courtyard, then back house(s) - the face-me-I-face-you compound. A few plots stay vacant or half-built.
netU_tree = STRtree([g for k, g in net_lines] + lanes); net_k = [k for k, g in net_lines] + ["lane"] * len(lanes)
def edge_class(p):
    i = int(np.atleast_1d(netU_tree.query_nearest(p))[0]); return net_k[i]
def place(plot, r):
    if plot.buffer(0.05).contains(r) and buildable.contains(r): add(r, kind_now[0]); return True
    return False
kind_now = ["front"]
plot_count = 0; vacant = 0
# frontage = every block edge, plus both sides of dead-end streets that poke into a block (they have houses too)
btree = STRtree(blocks); fronts = []
for bi, b in enumerate(blocks):
    if parcel_u.buffer(-1).intersects(b.representative_point()) or b.area < 250: continue
    ext = list(b.exterior.coords)
    fronts += [(math.dist(p, q), p, q, bi) for p, q in zip(ext, ext[1:])]
for g in streets + lanes:
    c = list(g.coords)
    for p, q in zip(c, c[1:]):
        L = math.dist(p, q)
        if L < 7: continue
        mid = Point((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        for side in (1, -1):
            ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L; pt = Point(mid.x - uy * 2 * side, mid.y + ux * 2 * side)
            for bi in btree.query(pt):
                bb = blocks[bi]
                if bb.contains(pt) and bb.exterior.distance(mid) > 0.5 and not parcel_u.buffer(-1).intersects(bb.representative_point()):
                    fronts.append((L - 1000, p, q, int(bi)) if side == 1 else (L - 1000, q, p, int(bi)))
fronts.sort(key=lambda f: -f[0])
taken = {}
def dmax_of(b):
    mr = b.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
    return min(48.0, min(Point(cc[0]).distance(Point(cc[1])), Point(cc[1]).distance(Point(cc[2]))) / 2 + 1.0)
DM = {}
for _, p, q, bi in fronts:
    b = blocks[bi]
    if bi not in DM: DM[bi] = dmax_of(b)
    dmax = DM[bi]
    if True:
        L = math.dist(p, q)
        if L < 7: continue
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L; nx_, ny_ = -uy, ux
        mid = Point((p[0] + q[0]) / 2 + nx_ * 2, (p[1] + q[1]) / 2 + ny_ * 2)
        if not b.contains(mid): nx_, ny_ = -nx_, -ny_
        cl = CLEAR.get(edge_class(Point((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)), 3.4)
        a = math.atan2(uy, ux); t = 0.0
        while t < L - 4:
            w = RULE["short_side"](rnd.uniform(.35, .97)) + RULE["gap"]()
            w = min(w, L - t)
            P0 = (p[0] + ux * t, p[1] + uy * t); P1 = (p[0] + ux * (t + w), p[1] + uy * (t + w))
            strip = Polygon([P0, P1, (P1[0] + nx_ * dmax, P1[1] + ny_ * dmax), (P0[0] + nx_ * dmax, P0[1] + ny_ * dmax)])
            try:
                plot = strip.intersection(b)
                if bi in taken: plot = plot.difference(taken[bi])
            except Exception:
                t += w; continue
            if plot.geom_type != "Polygon": plot = max(getattr(plot, "geoms", [plot]), key=lambda g: g.area, default=None) if not plot.is_empty else None
            t += w
            if plot is None or plot.area < 30: continue
            taken[bi] = plot if bi not in taken else taken[bi].union(plot).buffer(0); plot_count += 1
            if rnd.random() < 0.07: vacant += 1; continue          # vacant / abandoned plot
            gap = RULE["gap"](); hw = w - gap; base = (P0[0] + ux * w / 2, P0[1] + uy * w / 2)
            def at(off, d, ww):  # rectangle whose front edge sits `off` metres in from the street centreline
                return rect(base[0] + nx_ * (off + d / 2), base[1] + ny_ * (off + d / 2), ww, d, a)
            off = cl + abs(rnd.gauss(0, 2.2)); first = True
            while off < dmax - 3:
                sh, lo = size(0.25)
                if first: d = lo if rnd.random() < RULE["perp_front"] else sh
                else: d = rnd.choice([sh, lo])
                ww = hw if first else max(3, hw - rnd.uniform(0, 2.5))
                kind_now[0] = "front" if first else "back"
                ok = False
                for shrink in (1, .8, .62, .45):
                    dd = min(d * shrink, dmax - off)
                    if dd < 3: break
                    if place(plot, at(off, dd, ww)): ok = True; off += dd; break
                if not ok: break
                first = False
                if rnd.random() > RULE["back_row"]: break
                off += rnd.uniform(1.5, 4)                              # courtyard
            if rnd.random() < RULE["outbuilding"]:
                kind_now[0] = "shed"; ow, od = rnd.uniform(2.2, 4.5), rnd.uniform(2.2, 4.0)
                place(plot, at(dmax - od - 0.3, od, ow))
# kiosks and sheds on leftover frontage (the many <60 m2 structures)
for k, g in net_lines:
    if k == "art": continue
    for i in range(int(g.length // 70)):
        p = g.interpolate(rnd.uniform(0, g.length)); q = g.interpolate(min(g.length, g.project(p) + 1))
        a = math.atan2(q.y - p.y, q.x - p.x); side = rnd.choice((1, -1)); off = CLEAR.get(k, 3.4) + 1.6
        r = rect(p.x - math.sin(a) * off * side, p.y + math.cos(a) * off * side, rnd.uniform(2.2, 4), rnd.uniform(2, 3.2), a)
        if free(r, 0.2): add(r, "kiosk")
# parcel buildings: market sheds, warehouses (the big >1500 m2 buildings sit near mains), school blocks
for p in parcels:
    g = p["geom"]; mr = g.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
    e = (cc[0], cc[1]) if math.dist(cc[0], cc[1]) >= math.dist(cc[1], cc[2]) else (cc[1], cc[2])
    a = math.atan2(e[1][1] - e[0][1], e[1][0] - e[0][0]); ctr = g.centroid; LL = max(math.dist(cc[0], cc[1]), math.dist(cc[1], cc[2]))
    if p["kind"] == "industrial":
        for dx in (-1, 1):
            r = rect(ctr.x + math.cos(a) * dx * 30, ctr.y + math.sin(a) * dx * 30, 46, 30, a)
            if g.contains(r): bld.append((r, "warehouse"))
    if p["kind"] == "market":
        for i in range(-3, 4):
            for j in range(-2, 3):
                r = rect(ctr.x + math.cos(a) * i * 13 - math.sin(a) * j * 11, ctr.y + math.sin(a) * i * 13 + math.cos(a) * j * 11, 10, 7, a)
                if g.buffer(-3).contains(r): bld.append((r, "stalls"))
    if p["kind"] == "school":
        for j in (-1, 1):
            r = rect(ctr.x - math.sin(a) * j * 14, ctr.y + math.cos(a) * j * 14, min(46, LL - 12), 8, a)
            if g.contains(r): bld.append((r, "school"))

# ---------- 5. civic slots: real plots the civic layer can sit on ----------
slots = []
for r, kind in bld:
    if kind in ("front", "back") and r.area > 90:
        d = r.distance(mainU); slots.append({"x": round(r.centroid.x), "y": round(r.centroid.y), "main": d < 40})
rnd.shuffle(slots)

# ---------- 6. measure against the real core squares ----------
B = [r for r, k in bld]
gen_streets = [("street", g) for g in streets] + [("main", e) for n, e, nb in edge_roads] + [("main", ln) for n, ln in mains] + [("art", a) for n, k, a in arts]
M = measure(gen_streets, B, land.buffer(3))
# edge roads are shared with neighbours: count half of their length in the density figures
half = sum(e.intersection(land.buffer(1)).length for n, e, nb in edge_roads) / 2000 / (land.area / 1e6)
M["drive_km_per_km2_edges_half"] = round(M["drive_km_per_km2"] - half, 1); M["main_km_per_km2_edges_half"] = round(M["main_km_per_km2"] - half, 2)
M["building_overlaps"] = 0
print(json.dumps({"seed": SEED, "scale": SCALE, "gidi": M, "real_median": {k: CORE["median"][k] for k in M if k in CORE["median"]}, "real_dense": {k: CORE["dense"][k] for k in M if k in CORE["dense"]}}, indent=1))

R2 = lambda g: [[round(x, 1), round(y, 1)] for x, y in g.coords]
out = {"id": DID, "seed": SEED, "method": "original generator calibrated on OSM statistics of the inspiration area; no real geometry used",
       "streets": [R2(g) for g in streets],
       "lanes": [R2(g) for g in lanes],
       "mains": [{"name": n, "pts": R2(e), "edge_with": nb} for n, e, nb in edge_roads] + [{"name": n, "pts": R2(ln)} for n, ln in mains] + [{"name": "", "pts": R2(l)} for l in links],
       "canal": R2(canal) if canal else None,
       "buildings": [[k] + [[round(x, 1), round(y, 1)] for x, y in list(r.exterior.coords)[:-1]] for r, k in bld],
       "parcels": [{"kind": p["kind"], "pts": [[round(x, 1), round(y, 1)] for x, y in p["geom"].exterior.coords]} for p in parcels],
       "poi_pos": {k: [round(v.x), round(v.y)] for k, v in poi_pos.items()}, "slots": slots[:400], "metrics": M}
json.dump(out, open(OUT, "w"), separators=(",", ":"))
if OUT == f"web/gen-{DID}.json": json.dump(NET, open(NET_F, "w"), indent=1)
