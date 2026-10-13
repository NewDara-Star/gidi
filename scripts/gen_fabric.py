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
from district_profiles import profile, height_bands, STOREY_BANDS

DID = sys.argv[1]; SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 7
SCALE = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0   # one calibration knob: stretches street spacing until the network matches the study
OUT = sys.argv[4] if len(sys.argv) > 4 else f"web/gen-{DID}.json"
rnd = random.Random(SEED)
ST = json.load(open(f"study-{DID}.json")); CORE = json.load(open(f"study-{DID}-core.json"))
s = open("web/gidi-data.js").read(); G = json.loads(s[len("window.GIDI="):-1])
DIST = {d["id"]: d for d in G["districts"]}; POLY = {k: Polygon(v["poly"][0]) for k, v in DIST.items()}
poly = POLY[DID]; water = Polygon(G["water"][0]); land = poly.difference(water)
PROF = profile(DID, ST)   # empty for the Maze: it keeps the original v1 behaviour
if PROF and os.environ.get("GIDI_TUNE"): PROF.update(json.loads(os.environ["GIDI_TUNE"]))   # calibration sweeps only
nrnd = random.Random(SEED * 7919 + 1) if PROF else rnd   # edge roads get their own dice, so re-running a district gives the same result

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
if PROF:
    ce = PROF["cross_every"]; RULE["cross_every"] = sampler({k: ce[k] for k in ("p25", "p50", "p75")}, ce["lo"], ce["hi"])
    RULE["x_junction"] = PROF["x_junction"]; RULE["dead_end"] = PROF.get("dead_end", RULE["dead_end"])
    RULE["back_row"] = PROF.get("back_row", RULE["back_row"]); RULE["big_front"] = PROF.get("big_front", 0.0); RULE["cross_scale"] = PROF.get("cross_scale", SCALE); RULE["size_lo_u"] = PROF.get("size_lo_u", 0.25)
CLEAR = {"lane": 2.2, "street": 3.4, "main": 6.5, "art": 12.5, "exp": 15, "rail": 6.0, "canal": 4.0}   # building edge to centreline, minimum
WIDTH = {"street": 5.5, "main": 10, "art": 22}
FIRST = ["Adeyemi","Okafor","Bello","Ayinde","Ogundipe","Balogun","Lawal","Adebayo","Eze","Musa","Akande","Oladipo","Afolabi","Ibrahim","Adeleke","Oyelaran","Kalejaiye","Bankole","Odusanya","Ajasa","Fadipe","Oshinowo","Salami","Olatunji","Abeni","Taiwo","Kehinde","Idowu","Alaba","Ireti","Folake","Agboola","Shonibare","Ilori","Durojaiye","Ogunleye","Aremu","Okonkwo","Nwosu","Danjuma"]
ENDS = [("Street", 60), ("Road", 13), ("Avenue", 4), ("Close", 4), ("Way", 4), ("Crescent", 2), ("Lane", 2)]   # from street_name_endings
used = set()
ART_FIRST = {a["name"].split()[0] for a in G["arterials"]}
if PROF:
    ENDS = list(PROF["name_endings"].items())
    import glob
    for f in glob.glob("web/gen-*.json"):   # never reuse a name another district already has
        if f != f"web/gen-{DID}.json": used |= {m["name"] for m in json.load(open(f))["mains"] if m["name"]}
def street_name(kind="street", r=None):
    r = r or rnd; n = None
    for _ in range(200):
        e = "Road" if kind == "main" and r.random() < .6 else r.choices([e for e, w in ENDS], [w for e, w in ENDS])[0]
        f = r.choice(FIRST)
        if PROF and (f in ART_FIRST or f in {u.split()[0] for u in used}): continue   # never "Ayinde Road" next to Ayinde Avenue, nor two Idowus
        n = f"{f} {e}"
        if n not in used: used.add(n); return n
    return n

# ---------- 1. the network shared with the rest of Gidi ----------
NET_F = "web/network.json"
NET = json.load(open(NET_F)) if os.path.exists(NET_F) else {"edges": {}, "gateways": []}
if PROF: used |= {e["name"] for e in NET["edges"].values()}
# a district rebuilt after its neighbours keeps the crossings it already agreed with them (web/network.json), road for road
KEEP = bool(PROF.get("keep_gateways")) and any(g["from"] == DID for g in NET["gateways"])
arts = [(a["name"], a["cls"], LineString(a["pts"])) for a in G["arterials"] if a["cls"] != "bridge" and LineString(a["pts"]).distance(poly) < 160]
rail = LineString(G["rail"]["pts"]); rail_in = rail.intersection(poly.buffer(30))
coords = list(poly.exterior.coords)[:-1]
edge_roads = []
for i in range(len(coords)):
    a, b = coords[i], coords[(i + 1) % len(coords)]; e = LineString([a, b])
    nb = max((k for k in POLY if k != DID), key=lambda k: POLY[k].buffer(25).intersection(e).length)
    if POLY[nb].buffer(25).intersection(e).length < 0.5 * e.length: nb = None
    key = "|".join(sorted([DID, nb])) if nb else f"{DID}|outer{i}"
    if nb:   # two districts can share more than one edge: each stored edge is matched by its end points ("a|b", "a|b#2", ...)
        def ends_match(k):
            p = NET["edges"][k]["pts"]; return min(math.dist(p[0], a) + math.dist(p[-1], b), math.dist(p[0], b) + math.dist(p[-1], a)) < 60
        same = [k for k in NET["edges"] if k == key or k.startswith(key + "#")]
        hit = next((k for k in same if ends_match(k)), None)
        if hit: key = hit
        elif same: key = f"{key}#{len(same) + 1}"
    if key not in NET["edges"]:  # gently bent so it doesn't read as a ruler line (sinuosity ~1.0 with small kinks)
        L = e.length; n = max(3, int(L // 200)); pts = [a]
        for j in range(1, n):
            p = e.interpolate(j / n, normalized=True); nx_, ny_ = -(b[1] - a[1]) / L, (b[0] - a[0]) / L; o = nrnd.uniform(-16, 16)
            pts.append((p.x + nx_ * o, p.y + ny_ * o))
        pts.append(b)
        NET["edges"][key] = {"between": [DID, nb], "name": street_name("main", nrnd), "pts": [[round(x, 1), round(y, 1)] for x, y in pts]}
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

import landmarks as LMK
INTERNAL_MAINS = PROF.get("internal_mains", 2) if PROF else 2
# internal mains: one through-route crossing the district (gateways on both sides), one half-route that T's into it.
# Main density target ~3 km/km2 (dense core square 3.1); edge roads count half because neighbours share them.
def through_main(e1, e2, t1, t2, bend, ends=None):
    p, q = ends or (e1.interpolate(t1, normalized=True), e2.interpolate(t2, normalized=True))
    m = LineString([p, q]).interpolate(rnd.uniform(.4, .6), normalized=True)
    L = p.distance(q); nx_, ny_ = -(q.y - p.y) / L, (q.x - p.x) / L
    k = (m.x + nx_ * bend, m.y + ny_ * bend)
    return LineString([p.coords[0], k, q.coords[0]])
# pick the two longest opposite edges for the through route, avoiding arterial corridors
E = [(i, e) for i, (n, e, nb) in enumerate(edge_roads)]
pairs = [(i, j) for i in range(len(E)) for j in range(len(E)) if i < j and E[i][1].distance(E[j][1]) > 300]
best = None
PIN = {}   # kept main-road gateways: the through-route must start and end exactly on them
for g in (NET["gateways"] if KEEP else []):
    if g["from"] == DID and g["kind"] == "main": PIN.setdefault(g["road"], []).append(Point(g["pt"]))
PIN = [(n, v) for n, v in PIN.items() if len(v) == 2]
if PIN: pairs = [(None, None)]
# a finished neighbour's main road that ends on our edge carries on as our through-route (it has no bearing: we pick the far end)
PIN1 = None
if not PIN and PROF.get("continue_mains"):
    done = {k for k in POLY if k != DID and os.path.exists(f"web/gen-{k}.json")}
    g1 = next((g for g in NET["gateways"] if g["to"] == DID and g["from"] in done and g["kind"] == "main"), None)
    if g1:
        PIN1 = (g1["road"], Point(g1["pt"])); pairs = [(None, j) for j in range(len(E)) if E[j][1].distance(PIN1[1]) > 300]
for i, j in (pairs if INTERNAL_MAINS else []):
    for t in range(40):
        t1, t2 = rnd.uniform(.35, .65), rnd.uniform(.35, .65)
        if PIN: ln = through_main(None, None, 0, 0, rnd.uniform(-35, 35), PIN[0][1])
        elif PIN1: ln = through_main(None, None, 0, 0, rnd.uniform(-35, 35), (PIN1[1], E[j][1].interpolate(t2, normalized=True)))
        else: ln = through_main(E[i][1], E[j][1], t1, t2, rnd.uniform(-35, 35))
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
mains = [(PIN[0][0] if PIN else PIN1[0] if PIN1 else street_name("main"), best[1])] if best else []
if PIN or PIN1: used.add((PIN[0] if PIN else PIN1)[0])
# half-route from another edge into the through-route, on the biggest leftover piece
pieces = [] if not best else list(polygonize(unary_union([e for n, e, nb in edge_roads] + [a for n, k, a in arts] + [best[1], rail])))
pieces = [p.intersection(land) for p in pieces if poly.buffer(-5).intersects(p.representative_point())]
big = max(pieces, key=lambda p: p.area) if pieces else None
cand = None
for n, e, nb in (edge_roads if INTERNAL_MAINS > 1 and big is not None else []):
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
NET_GW0 = list(NET["gateways"])   # to keep the file's order when nothing about this district's crossings changed
if not KEEP: NET["gateways"] = [g for g in NET["gateways"] if g["from"] != DID]
def add_gate(pt, nb, road, kind, bearing=None):
    if KEEP: return   # already recorded; the neighbours built against these
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
# ---------- 1b. landmarks carved out first (Hub: the knot of flyovers and slip roads, terminal, station, stadium) ----------
STRUCT, ramps, access, RES = [], [], [], []   # RES: reserved parcels {"kind","geom","poi"} that ordinary streets and houses keep out of
POIS = {p["name"]: Point(p["x"], p["y"]) for p in G["pois"] if p["d"] == DID}
if PROF:  # the designed pins (districts_info.json), placed the way bake_web.py first places them - not the baked ones, which move onto what we generate
    _land0 = poly.difference(water).difference(Polygon(G["ocean"][0])); _core = _land0.buffer(-40) if not _land0.buffer(-40).is_empty else _land0
    _b = _land0.bounds
    for q in json.load(open("web/districts_info.json"))[DID]["pois"]:
        pt = Point(_b[0] + (_b[2] - _b[0]) * q["u"], _b[1] + (_b[3] - _b[1]) * (1 - q["v"]))
        POIS[q["name"]] = pt if _core.contains(pt) else nearest_points(_core, pt)[0]
# canal (real: ~0.76 km of canal/drain/stream per km2) - one open canal following the land, with culverts under streets
canal = None
gc = next((p for p in G["pois"] if p["d"] == DID and "Canal" in p["name"]), None)
if gc:
    c0 = POIS[gc["name"]]; ang = rnd.uniform(0, math.pi); pts = []   # with a profile, the designed pin (the baked one moves onto the canal we draw)
    for t in np.linspace(-1, 1, 9):
        pts.append((c0.x + math.cos(ang) * 340 * t + rnd.uniform(-12, 12), c0.y + math.sin(ang) * 340 * t + rnd.uniform(-12, 12)))
    canal = LineString(pts).intersection(land.buffer(-12))
    canal = max(lines(canal), key=lambda l: l.length) if not canal.is_empty else None
    if canal is not None and PROF: canal = max(lines(canal.difference(rail.buffer(CLEAR["rail"] + 4))), key=lambda l: l.length)   # it stops at the rail and goes under in a culvert

knot = None; poi_pos = {}
for n, ln in (mains if PROF.get("exp_bridge_m") else []):   # an internal main crosses an expressway on a flyover, never at grade
    for an, ak, a in arts:
        if ak != "exp": continue
        x = ln.intersection(a)
        for p in getattr(x, "geoms", [x]):
            if p.geom_type != "Point" or not poly.contains(p): continue
            tb = ln.project(p); h = PROF["exp_bridge_m"] / 2
            STRUCT.append({"kind": "flyover", "name": f"{n} Flyover", "geom": substring(ln, max(0, tb - h), min(ln.length, tb + h)), "layer": 1, "width": WIDTH["main"]})
if PROF.get("rail_bridge_m"):   # an internal main road crosses the rail on a bridge (real: most major roads do)
    for n, ln in mains:
        x = ln.intersection(rail)
        for p in getattr(x, "geoms", [x]):
            if p.geom_type != "Point" or not poly.contains(p): continue
            tb = ln.project(p); h = PROF["rail_bridge_m"] / 2
            STRUCT.append({"kind": "flyover", "name": f"{n} Rail Bridge", "geom": substring(ln, max(0, tb - h), min(ln.length, tb + h)), "layer": 1, "width": WIDTH["main"]})
if PROF.get("interchange"):
    IC = PROF["interchange"]
    art_in = [(n, k, a) for n, k, a in arts if a.intersection(poly).length > 100]
    STRUCT, ramps, gores, knot = LMK.build_interchange(art_in, rail, poly, land, IC, [e.buffer(10) for n, e, nb in edge_roads])
    for g in gores:  # the land between a slip road and the two arterials: the under-bridge trade
        g2 = g.difference(unary_union([a.buffer(CLEAR["art"]) for n, k, a in arts] + [r.buffer(CLEAR["main"]) for r in ramps] + [rail.buffer(CLEAR["rail"])]))
        g2 = max(getattr(g2, "geoms", [g2]), key=lambda x: x.area, default=None)
        if g2 is not None and g2.area > 600: RES.append({"kind": "under bridge", "geom": g2, "poi": None})
    ub = [r for r in RES if r["kind"] == "under bridge"]
    if ub: max(ub, key=lambda r: r["geom"].area)["poi"] = "Under the Bridge"
GAP = 8.0   # room between a reserved parcel and its access road
for spec in PROF.get("reserve", []):
    hint = knot if spec.get("near_knot") and knot else POIS.get(spec["poi"], poly.centroid)
    fronts = [a for n, k, a in arts if a.intersection(poly).length > 100] if spec["front"] == "art" else ([rail] if spec["front"] == "rail" else [])
    off = CLEAR["art"] if spec["front"] == "art" else CLEAR["rail"]
    if spec["front"] and not fronts: print("skipped", spec["kind"], "- nothing to face", file=sys.stderr); continue
    others = [e.buffer(CLEAR["main"] + 2) for n, e, nb in edge_roads] + [a.buffer(CLEAR["art"] + 2) for n, k, a in arts if all(a is not f for f in fronts)] \
        + [r.buffer(CLEAR["main"] + 2) for r in ramps] + [r["geom"].buffer(GAP + 10) for r in RES] + ([] if spec["front"] == "rail" else [rail.buffer(CLEAR["rail"] + 2)]) \
        + [ln.buffer(CLEAR["main"] + 2) for n, ln in mains] + ([canal.buffer(CLEAR["canal"] + 10)] if canal is not None else [])
    if knot is not None: others.append(knot.buffer(60))
    # it faces its own road (its margin may reach it), but stays clear of everything else
    got = LMK.place_reserved(spec, hint, fronts, off, land, unary_union(others), GAP + (6 if spec["front"] != "rail" else 0))
    if not got: print("could not place", spec["kind"], file=sys.stderr); continue
    r, info = got
    RES.append({"kind": spec["kind"], "geom": r, "poi": spec.get("poi"), "spec": spec, "info": info})
    hard_u = unary_union([e for n, e, nb in edge_roads] + [a for n, k, a in arts] + access)
    if spec["front"] == "art": access.append(LMK.u_road(info, GAP))
    elif spec["front"] == "rail": access.append(LMK.back_road(info, GAP))
    else: access += LMK.ring_road(r, GAP, hard_u, spec.get("access_roads", 1), rail.buffer(CLEAR["rail"]).union(unary_union([x["geom"] for x in RES[:-1]])) if RES[:-1] else rail.buffer(CLEAR["rail"]))
RES_U = unary_union([r["geom"] for r in RES]) if RES else None

# ---------- 2. sectors and residential streets ----------
hard = [e for n, e, nb in edge_roads] + [a for n, k, a in arts] + [ln for n, ln in mains] + links + ramps + access
sector_lines = unary_union(hard + [rail])
LAND_S = land.difference(RES_U.buffer(1)) if RES_U is not None else land
sectors = [p.intersection(LAND_S) for p in polygonize(sector_lines) if poly.buffer(-3).contains(p.representative_point())]
sectors = [g for p in sectors for g in getattr(p, "geoms", [p]) if g.geom_type == "Polygon"]
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
            y += RULE.get("cross_scale", SCALE) * RULE["cross_every"]()
        prev = cur
    streets += [rotate(g, th, origin=c, use_radians=True) for g in ribs]
streets += [g for c in collectors for g in lines(c)]
# streets a finished neighbour started on the shared edge carry straight on into this district
GEN_DONE = {k for k in POLY if k != DID and os.path.exists(f"web/gen-{k}.json")}
incoming = [g for g in NET["gateways"] if g["to"] == DID and g["from"] in GEN_DONE and g["kind"] in ("street", "main") and "bearing_deg" in g] if PROF else []
if PROF and not PIN1 and any(g["to"] == DID and g["kind"] == "main" and "bearing_deg" not in g for g in NET["gateways"]):
    print("note: a neighbour's main road gateway has no bearing; continue it by hand", file=sys.stderr)
if KEEP:  # the district's own street crossings, already recorded: a street runs in from each one (bearing points out, so turn it round)
    incoming = incoming + [{**g, "bearing_deg": (g["bearing_deg"] + 180) % 360} for g in NET["gateways"] if g["from"] == DID and g["kind"] == "street" and "bearing_deg" in g
                           and all(Point(g["pt"]).distance(Point(h["pt"])) > 1 for h in incoming)]
for g in incoming:
    b = math.radians(g.get("bearing_deg", 0)); p0 = Point(g["pt"]); dx, dy = math.sin(b), -math.cos(b)
    ray = LineString([p0, (p0.x + dx * 600, p0.y + dy * 600)])
    stop = unary_union([a for n, k, a in arts] + ramps + access + [rail.buffer(9).exterior] + ([RES_U.exterior if RES_U.geom_type == "Polygon" else RES_U.boundary] if RES_U is not None else []) + [e for n, e, nb in edge_roads if e.distance(p0) > 1])
    if KEEP: stop = stop.union(unary_union(streets))   # a rebuilt district ties its kept crossings into the first street they meet
    x = ray.intersection(stop); hits = [] if x.is_empty else [q for q in getattr(x, "geoms", [x]) if q.geom_type == "Point"]
    cut = min([ray.project(q) for q in hits if ray.project(q) > (25 if KEEP else 5)] or [ray.length])
    streets.append(substring(ray, 0, cut))
if RES_U is not None:   # with "clear_access", streets also stop short of a big place's own road and snap onto it (no double road beside it)
    streets = [x for s0 in streets for x in lines(s0.difference(RES_U.buffer((GAP if PROF.get("clear_access") else 0) + CLEAR["street"] + 1))) if x.length > 18]
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
# level crossings (real Mushin + Shomolu: 15 mapped): a street that stops at the rail carries straight over it to the first street beyond
LX = []
if PROF.get("level_crossings"):
    away = unary_union([x["geom"] for x in STRUCT]).buffer(150) if STRUCT else None
    cand = []
    for g in streets:
        c = list(g.coords)
        for i0, i1 in ((0, 1), (-1, -2)):
            p, q = Point(c[i0]), Point(c[i1])
            if p.distance(rail_zone.exterior) > 1.5: continue
            L = p.distance(q) or 1; ux, uy = (p.x - q.x) / L, (p.y - q.y) / L
            ray = LineString([p, (p.x + ux * 200, p.y + uy * 200)]); x = ray.intersection(rail)
            if x.geom_type != "Point" or not land.buffer(-40).contains(x) or (away is not None and away.contains(x)): continue
            vx, vy = LMK.direction_at(rail, rail.project(x)); ang = math.degrees(math.acos(min(1, abs(ux * vx + uy * vy))))
            if ang < 40: continue   # the same rule as the through-road: cross the line at a real angle
            beyond = ray.intersection(unary_union([o for o in streets + hard if o is not g]))
            hits = [h for h in getattr(beyond, "geoms", [beyond]) if h.geom_type == "Point" and ray.project(h) > ray.project(x) + 9]
            if not hits: continue
            h = min(hits, key=ray.project)
            cand.append((-ang + x.distance(land.centroid) / 20, LineString([p, h])))
    LX = [ln for sc, ln in sorted(cand, key=lambda c: c[0])[:PROF["level_crossings"]]]
    streets += LX
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
    big = [b for b in polygonize(noded(streets + hard + [rail] + ([rail_zone.exterior] if PROF.get("rail_frontage") else []))) if land.buffer(1).contains(b.representative_point()) and b.area > ST["blocks"]["area_m2"]["p90"]]
    if not big: break
    for b in big:
        mr = b.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
        e1, e2 = ((cc[0], cc[1]), (cc[3], cc[2])) if math.dist(cc[0], cc[1]) >= math.dist(cc[1], cc[2]) else ((cc[1], cc[2]), (cc[0], cc[3]))
        f = rnd.uniform(.4, .6); p1 = LineString(e1).interpolate(f, normalized=True); p2 = LineString(e2).interpolate(f, normalized=True)
        ln = LineString([(p1.x + (p1.x - p2.x), p1.y + (p1.y - p2.y)), (p2.x + (p2.x - p1.x), p2.y + (p2.y - p1.y))]).intersection(b)
        streets += [g for g in lines(ln.difference(rail_zone) if PROF.get("rail_frontage") else ln) if g.length > 20]   # stop short of the rail like every other street

# a few residential streets carry straight on into the neighbour (real: ~0.9 per km of edge); the rest T into the edge road
for g in incoming: add_gate(Point(g["pt"]), g["from"], g["road"], g["kind"], (g.get("bearing_deg", 0) + 180) % 360)
for en, e, nb in edge_roads:
    if not nb or KEEP or (PROF and nb in GEN_DONE): continue   # a finished neighbour already chose where streets cross this edge
    ends = []
    for g in streets:
        for i0, i1 in ((0, 1), (-1, -2)):
            p = Point(g.coords[i0])
            if p.distance(e) < 1.0:
                q = Point(g.coords[i1]); ends.append((p, math.degrees(math.atan2(p.x - q.x, -(p.y - q.y))) % 360))
    rnd.shuffle(ends); n_keep = max(1, round(0.9 * e.length / 1000))
    for p, brg in ends[:n_keep]: add_gate(p, nb, "", "street", brg)
# ---------- 3. parcels for the places a neighbourhood needs ----------
NET_LINES = lambda: [("street", g) for g in streets] + [("main", e) for n, e, nb in edge_roads] + [("main", ln) for n, ln in mains] + [("main", l) for l in links] + [(k, a) for n, k, a in arts] \
    + [("main", r) for r in ramps] + [("street", g) for g in access]
net_lines = NET_LINES()
blocks = [b for b in polygonize(noded([g for k, g in net_lines] + [rail])) if land.buffer(1).contains(b.representative_point()) and b.area > 120]
mainU = unary_union([g for k, g in net_lines if k != "street"])
parcels = [{"kind": r["kind"], "geom": r["geom"]} for r in RES]
for r in RES:
    if r.get("poi"): poi_pos[r["poi"]] = r["geom"].representative_point()
def short_side(b):
    cc = list(b.minimum_rotated_rectangle.exterior.coords); return min(math.dist(cc[0], cc[1]), math.dist(cc[1], cc[2]))
def take(kind, near_pt, want_ha, near_main=True, max_dist=None, min_w=0):
    cands = [b for b in blocks if not any(b.intersects(p["geom"]) for p in parcels) and (not min_w or short_side(b) >= min_w)]
    if near_main: cands = [b for b in cands if b.distance(mainU) < 3]
    elif PROF: cands = [b for b in cands if b.distance(unary_union([a for n, k, a in arts] + ramps)) > 20] or cands   # off the arterials
    else: cands = [b for b in cands if 0.6 * want_ha * 1e4 < b.area < 1.8 * want_ha * 1e4 and 30 < b.centroid.distance(mainU) < 200] or cands
    if max_dist: cands = [b for b in cands if b.distance(near_pt) < max_dist] or cands
    if PROF and not cands: cands = [b for b in blocks if not any(b.intersects(p["geom"]) for p in parcels)] or blocks
    if PROF:  # nearest block to the pin; a big block gives up only the piece around the pin (no long strips)
        b = min(cands, key=lambda b: b.distance(near_pt) + (0 if b.area > 0.8 * want_ha * 1e4 else 400))
        g = b
        if b.area > want_ha * 1e4 * 1.1:
            fr = mainU.buffer(60) if near_main else b
            q = nearest_points(b.intersection(fr), near_pt)[0]
            mr = b.minimum_rotated_rectangle; cc = list(mr.exterior.coords); ang = math.atan2(cc[1][1] - cc[0][1], cc[1][0] - cc[0][0])
            for rr in range(20, 400, 4):   # a square around the pin, turned with the block, so parcels come out rectangular
                sq = rotate(box(q.x - rr, q.y - rr, q.x + rr, q.y + rr), ang, origin=q, use_radians=True)
                g = b.intersection(sq).intersection(fr.buffer(rr) if near_main else b)
                if g.area >= want_ha * 1e4: break
        g = g.buffer(-2)
        if g.geom_type != "Polygon": g = max(getattr(g, "geoms", [g]), key=lambda x: x.area)
        parcels.append({"kind": kind, "geom": g}); return g
    b = min(cands, key=lambda b: b.distance(near_pt) + abs(b.area - want_ha * 1e4) / 40)
    g = b
    if b.area > want_ha * 1e4 * 1.4 and near_main:  # only the part of the block that faces the main road
        for r in range(20, 200, 5):
            g = b.intersection(mainU.buffer(r))
            if g.area >= want_ha * 1e4: break
    g = g.buffer(-2)
    if g.geom_type != "Polygon": g = max(getattr(g, "geoms", [g]), key=lambda x: x.area)
    parcels.append({"kind": kind, "geom": g}); return g
c0 = poly.centroid
mk = next((n for n in POIS if "Market" in n), None) if not PROF else None
if mk: g = take("market", POIS[mk], 1.4); poi_pos[mk] = g.representative_point()        # markets front main roads, median 1.4 ha
yard = next((n for n in POIS if "Yard" in n), None)
ind_ha = max(1.5, ST["landuse_polygons_ha"].get("industrial", [0, 0])[1] / ST["area_km2"] / 100 * land.area / 1e4)  # ~3.8% of land
if yard and not PROF: g = take("industrial", POIS[yard], min(ind_ha, 3.0)); poi_pos[yard] = g.representative_point()
if not PROF:
    take("school", c0, 0.8, near_main=False)                                              # schools sit ~65 m back from mains
    take("pitch", c0, 0.3, near_main=False)
    take("motor park", Point(poly.bounds[0], poly.bounds[1]), 0.25)
GATES = []   # (parcel, "nearest" | "north" | ...): a short access road from the parcel's fence to a street
for spec in PROF.get("parcels", []):
    parcel_u0 = unary_union([p["geom"] for p in parcels])
    if spec.get("near") == "rail":   # on the line, as close to its pin as the rail allows
        pin = POIS.get(spec.get("poi"), c0); rin = rail.intersection(land.buffer(-30))
        hint = nearest_points(rin, pin)[0] if not rin.is_empty else pin
    elif str(spec.get("near", "")).startswith("res:"):   # next to a big place carved out earlier (the lorry park behind the market)
        rr = next((r for r in RES if r["kind"] == spec["near"][4:]), None); hint = rr["geom"].centroid if rr else c0
    elif spec.get("near") == "junction":   # where an internal main meets an arterial
        xs = [q for n, ln in mains for n2, k, a in arts for q in getattr(ln.intersection(a), "geoms", [ln.intersection(a)]) if q.geom_type == "Point"]
        hint = xs[0] if xs else c0
    elif spec.get("uv"):   # a spot given like a designed pin (fraction across and down the district)
        _b = land.bounds; hint = Point(_b[0] + (_b[2] - _b[0]) * spec["uv"][0], _b[1] + (_b[3] - _b[1]) * (1 - spec["uv"][1]))
    elif spec.get("poi"): hint = POIS.get(spec["poi"], c0)
    elif spec.get("near") == "rail_far_from_knot":   # industry lines the rail, away from the crowds at the interchange
        rin = rail.intersection(land.buffer(-30)); rls = lines(rin)
        if not rls: hint = c0
        else:
            rl = max(rls, key=lambda l: l.length)
            hint = max([rl.interpolate(f, normalized=True) for f in np.linspace(0, 1, 21)], key=lambda q: q.distance(knot) if knot else 0)
    else:  # schools and pitches: the quietest spot, far from arterials, rail and the interchange
        noise = unary_union([a for n, k, a in arts] + [rail] + ([knot.buffer(150)] if knot else []))
        cand = [Point(x, y) for x in np.arange(*land.bounds[0::2], 25) for y in np.arange(*land.bounds[1::2], 25)]
        cand = [q for q in cand if land.buffer(-60).contains(q) and not parcel_u0.buffer(30).contains(q)]
        hint = max(cand, key=lambda q: q.distance(noise)) if cand else c0
    ha = spec["ha"]
    if ha == "from_study": ha = min(spec["cap_ha"], ST["landuse_polygons_ha"].get("industrial", [0, 0])[1] / ST["area_km2"] / 100 * land.area / 1e4)
    g = take(spec["kind"], hint, ha, near_main=spec["near_main"], min_w=spec.get("min_w", 0))
    if spec.get("gate"): GATES.append((g, spec["gate"]))
    if spec.get("poi"): poi_pos[spec["poi"]] = g.representative_point()
parcel_u = unary_union([p["geom"] for p in parcels])
if PROF.get("fence_parcels"):   # dead-end streets that poked into a block taken for a parcel stop at its fence
    if any(g.intersects(parcel_u) for g in streets):
        streets = [x for g in streets for x in lines(g.difference(parcel_u)) if x.length > 18]; net_lines = NET_LINES()
DIRS = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}   # y runs south
for g, how in GATES:
    ways_u = unary_union([x for k, x in net_lines])
    if how == "nearest":
        a0, b0 = nearest_points(g.exterior, ways_u); gl = LineString([a0, b0])
    else:   # leave the parcel on that side, straight out to the first street
        dx, dy = DIRS[how]; c = g.centroid; far = Point(c.x + dx * 1000, c.y + dy * 1000)
        a0 = nearest_points(g.exterior, far)[0]; ray = LineString([a0, (a0.x + dx * 300, a0.y + dy * 300)])
        x = ray.intersection(ways_u); hits = [h for h in getattr(x, "geoms", [x]) if h.geom_type == "Point" and ray.project(h) > 0.5]
        gl = LineString([a0, min(hits, key=ray.project)]) if hits else None
    if gl is not None and gl.length > 0.5: access.append(gl)
if GATES: net_lines = NET_LINES()
def mostly_parcel(b): return b.intersection(parcel_u).area > 0.6 * b.area

# service lanes (real: ~3 km per km2 of service ways): deep blocks get a dead-end lane so their middle can be built on
lanes = []
WAYS_U = unary_union([g for k, g in net_lines])
for b in blocks:
    if b.area < 12000 or (mostly_parcel(b) if PROF else parcel_u.buffer(-1).intersects(b.representative_point())): continue
    mr = b.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
    s1, s2 = Point(cc[0]).distance(Point(cc[1])), Point(cc[1]).distance(Point(cc[2]))
    if min(s1, s2) < 105: continue
    ext = list(b.exterior.coords); sides = list(zip(ext, ext[1:]))
    if PROF.get("walk"):   # a lane starts on a street, never on the rail side of the block
        sides = [e for e in sides if Point((e[0][0] + e[1][0]) / 2, (e[0][1] + e[1][1]) / 2).distance(WAYS_U) < 1] or [None]
        if sides == [None]: continue
    p, q = max(sides, key=lambda e: math.dist(*e))
    L = math.dist(p, q); ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L; nx_, ny_ = -uy, ux
    k = max(1, int(L // 110))                                   # one lane per ~110 m of frontage
    for i in range(k):
        f = (i + 0.5) / k + rnd.uniform(-.08, .08)
        m0 = (p[0] + ux * L * f, p[1] + uy * L * f); nx2, ny2 = nx_, ny_
        if not b.contains(Point(m0[0] + nx2 * 3, m0[1] + ny2 * 3)): nx2, ny2 = -nx2, -ny2
        depth = min(s1, s2) - rnd.uniform(35, 50)
        ln = LineString([m0, (m0[0] + nx2 * depth, m0[1] + ny2 * depth)]).intersection(b.buffer(-1))
        for g in lines(ln):
            if g.length > 25:
                ln2 = LineString([m0] + [g.coords[-1]])
                if PROF and ln2.intersects(parcel_u.buffer(3)): continue   # lanes never run through a school or a park
                lanes.append(ln2)
# ---------- 3b. footpaths: the walking network the streets leave out ----------
# Along the rail (in its clear strip), along both canal banks, short links from street ends to the rail path,
# and worn crossings over the line every 150-200 m (people cross on foot far more often than OSM maps).
PATHS = []   # (kind, line)
BANK = CLEAR["canal"] - 1.0   # bank path: between the water (2 m) and the houses (4 m)
W = PROF.get("walk")
if W:
    def offset(g, d):
        o = g.offset_curve(d); return o if not o.is_empty else None
    rail_in = rail.intersection(land)
    rail_sides = []
    for d in (W["rail_path_m"], -W["rail_path_m"]):
        o = offset(rail, d)
        if o is None: continue
        o = o.intersection(land).difference(parcel_u.buffer(2))
        rail_sides.append([g for g in lines(o) if g.length > 20])
        PATHS += [("rail path", g) for g in rail_sides[-1]]
    if canal is not None:
        for d in (BANK, -BANK):
            o = offset(canal, d)
            if o is not None: PATHS += [("canal path", g) for g in lines(o.intersection(land)) if g.length > 20]
    # street ends that stop at the rail walk on to the rail path
    side_u = [unary_union(sd) if sd else None for sd in rail_sides]
    links_t = []
    for g in streets:
        for i0 in (0, -1):
            e = Point(g.coords[i0])
            if not 3 < e.distance(rail) < CLEAR["rail"] + 6: continue
            near = min((u for u in side_u if u is not None), key=lambda u: u.distance(e), default=None)
            if near is None or near.distance(e) > 8: continue
            q = nearest_points(near, e)[0]
            if q.distance(e) > 0.5: PATHS.append(("link", LineString([e, q])))
            links_t.append(rail.project(e))
    have = [rail.project(x) for g in streets for x in [g.intersection(rail)] if x.geom_type == "Point"] + \
           [rail.project(x["geom"].interpolate(0.5, normalized=True)) for x in STRUCT if x["kind"] == "flyover" and x["geom"].intersects(rail)]
    # cut-throughs: deep blocks beside the line get a footpath from the rail path straight out to the next street
    # (no long way round for the back rows), and a worn crossing over the tracks where it meets the line
    cut_pts = []
    if W.get("cut_every_m"):
        stop_u = unary_union(streets + [e for n, e, nb in edge_roads] + [ln for n, ln in mains] + [a for n, k, a in arts] + lanes + access)
        link_pts = [Point(g.coords[0]) for k, g in PATHS if k == "link"]
        for rl in [g for sd in rail_sides for g in sd]:
            for t in np.arange(W["cut_every_m"] / 2, rl.length, W["cut_every_m"]):
                p = rl.interpolate(t)
                if any(p.distance(q) < W["cut_every_m"] / 3 for q in link_pts + cut_pts): continue
                r0 = nearest_points(rail, p)[0]; L = p.distance(r0) or 1; ux, uy = (p.x - r0.x) / L, (p.y - r0.y) / L
                ray = LineString([p, (p.x + ux * W["cut_max_m"], p.y + uy * W["cut_max_m"])]); x = ray.intersection(stop_u)
                hits = [h for h in getattr(x, "geoms", [x]) if h.geom_type == "Point" and ray.project(h) > 5]
                if not hits: continue
                seg = LineString([p, min(hits, key=ray.project)])
                if seg.length < 25 or seg.intersects(parcel_u.buffer(1)) or (RES_U is not None and seg.intersects(RES_U.buffer(2))): continue
                PATHS.append(("cut-through", seg)); cut_pts.append(p); links_t.append(rail.project(p))
                h = W["rail_path_m"]; q = rail.interpolate(rail.project(p)); vx, vy = LMK.direction_at(rail, rail.project(p))
                cr = LineString([(q.x - vy * h, q.y + vx * h), (q.x + vy * h, q.y - vx * h)])
                near_cross = [u for u in have if abs(u - rail.project(p)) < 60]
                if not near_cross and land.buffer(-2).contains(cr) and not cr.intersects(parcel_u):
                    PATHS.append(("worn crossing", cr)); have.append(rail.project(p))
    # worn crossings: between the crossings the line already has (street, bridge, the edge roads at either end),
    # spread evenly, never more than 200 m apart; each moves onto a street end nearby if one is within 20 m
    lo, hi = W["cross_every_m"]
    for r0 in lines(rail_in):
        ta, tb = sorted([rail.project(Point(r0.coords[0])), rail.project(Point(r0.coords[-1]))])
        anchors = sorted([ta] + [t for t in have if ta < t < tb] + [tb])
        for a0, b0 in zip(anchors, anchors[1:]):
            n = max(0, math.ceil((b0 - a0 - 10) / hi) - 1)   # never more than `hi` apart; fixed crossings can make a gap a little under `lo`
            for k in range(1, n + 1):
                want = a0 + (b0 - a0) * k / (n + 1)
                near = [u for u in links_t if abs(u - want) < 20]
                tc = min(near, key=lambda u: abs(u - want)) if near else want
                room = min((b0 - a0) / (n + 1) * 0.45, 60)   # if a yard or the edge is in the way, slide along the line, keeping the spacing
                for sh in sorted(range(-int(room), int(room) + 1, 5), key=abs):
                    q = rail.interpolate(tc + sh); ux, uy = LMK.direction_at(rail, tc + sh); h = W["rail_path_m"]
                    cr = LineString([(q.x - uy * h, q.y + ux * h), (q.x + uy * h, q.y - ux * h)])
                    if land.buffer(-2).contains(cr) and not cr.intersects(parcel_u): PATHS.append(("worn crossing", cr)); break
paths_u = unary_union([g for k, g in PATHS]) if PATHS else None

# ---------- 4. buildings: plots along every street frontage, compounds behind ----------
clear_geoms = [g.buffer(2.2) for g in lanes] + [g.buffer(CLEAR.get(k, 3.4)) for k, g in net_lines] + [rail.buffer(CLEAR["rail"])] + [g.buffer(1.2) for k, g in PATHS]
if canal: clear_geoms.append(canal.buffer(CLEAR["canal"]))
# skywalks: footbridges over the arterial in front of the bus terminal (Daramola's model: "terminal with skywalks"; real: ~45 m long)
for r in RES:
    if r["kind"] == "bus terminal" and PROF.get("interchange"):
        fl = r["info"][0]; IC = PROF["interchange"]
        n_sw = max(2, round(IC["skywalks_per_km_art"] * sum(a.intersection(poly).length for n, k, a in arts) / 1000))
        avoid = unary_union([x["geom"].buffer(3) for x in STRUCT] + [rr.buffer(3) for rr in ramps])
        for g in LMK.skywalks(fl, r["geom"].centroid, n_sw, IC["skywalk_m"], avoid, spacing=r["info"][4] * 0.55):
            STRUCT.append({"kind": "skywalk", "name": "Interchange skywalk", "geom": g, "layer": 1, "width": 4})
        SS = PROF.get("station_skywalk")
        st_res = next((x for x in RES if x["kind"] == "station"), None)
        if SS and st_res:   # one deck from the terminal over the arterial and the rail to the station (as at the real interchange)
            g = LineString([r["geom"].centroid, st_res["geom"].centroid]).difference(st_res["geom"].buffer(0.5))
            g = max(lines(g), key=lambda l: l.length)   # it lands on the station's facade; the terminal end is trimmed at its facade below
            STRUCT.append({"kind": "skywalk", "name": SS["name"], "geom": g, "layer": 1, "width": SS["width"]})
# footbridges over the canal where streets cross it too far apart; they join the walkable banks (inside the canal's clear strip)
if canal is not None and PROF.get("canal_footbridges"):   # in the longest stretches between street crossings
    cuts = sorted(canal.project(q) for k, g in net_lines for x in [canal.intersection(g)] for q in getattr(x, "geoms", [x]) if q.geom_type == "Point")
    for a0, b0 in sorted(zip([0.0] + cuts, cuts + [canal.length]), key=lambda ab: ab[0] - ab[1])[:PROF["canal_footbridges"]]:
        t = (a0 + b0) / 2; q = canal.interpolate(t); ux, uy = LMK.direction_at(canal, t); h = BANK if W else CLEAR["canal"] - 0.3   # with bank paths, it lands on them
        STRUCT.append({"kind": "footbridge", "name": f"{gc['name']} footbridge", "geom": LineString([(q.x + uy * h, q.y - ux * h), (q.x - uy * h, q.y + ux * h)]), "layer": 1, "width": 2.5})
    poi_pos[gc["name"]] = canal.interpolate(0.5, normalized=True)
XF = PROF.get("exp_footbridges")
if XF:   # footbridges over the expressway (real: about one per 3 km of major road, median 82 m), by the market where people cross
    exps = [a for n, k, a in arts if k == "exp" and a.intersection(poly).length > 100]
    for xa in exps:
        n_x = max(1, round(XF["per_km"] * xa.intersection(poly).length / 1000))
        at = next((r["geom"].centroid for r in RES if r["kind"] == "market"), poly.centroid)
        avoid = unary_union([x["geom"].buffer(12) for x in STRUCT] + [ln.buffer(15) for n, ln in mains])
        walk_to = STRtree([g for k, g in net_lines if k not in ("art", "exp")] + lanes + [g for k, g in PATHS])
        for gfb in LMK.skywalks(xa, at, n_x, XF["m"], avoid, spacing=200):
            gfb = gfb.intersection(land)
            if gfb.geom_type != "LineString": continue
            STRUCT.append({"kind": "skywalk", "name": "Expressway footbridge", "geom": gfb, "layer": 1, "width": 3})
            for e in (Point(gfb.coords[0]), Point(gfb.coords[-1])):   # the stairs come down onto the nearest street
                o = walk_to.geometries[int(np.atleast_1d(walk_to.query_nearest(e))[0])]
                q = nearest_points(o, e)[0]
                if q.distance(e) > 0.5: lk = LineString([e, q]); PATHS.append(("link", lk)); clear_geoms.append(lk.buffer(1.2))
for RF in PROF.get("road_footbridges", []):   # a footbridge over an arterial in front of a busy place (market, bus park)
    at_r = next((r for r in RES if r["kind"] == RF["near"]), None)
    rds = [a for n, k, a in arts if k in RF["cls"] and a.intersection(poly).length > 100]
    if at_r is None or not rds: continue
    xa = min(rds, key=lambda a: a.distance(at_r["geom"]))
    avoid = unary_union([x["geom"].buffer(12) for x in STRUCT] + [ln.buffer(15) for n, ln in mains] + [r["geom"] for r in RES if r is not at_r])   # it may land in its own market
    walk_to = STRtree([g for k, g in net_lines if k not in ("art", "exp")] + lanes + [g for k, g in PATHS])
    for gfb in LMK.skywalks(xa, at_r["geom"].centroid, 1, RF["m"], avoid, spacing=200):
        gfb = gfb.intersection(land)
        if gfb.geom_type != "LineString": continue
        STRUCT.append({"kind": "skywalk", "name": RF["name"], "geom": gfb, "layer": 1, "width": 3})
        for e in (Point(gfb.coords[0]), Point(gfb.coords[-1])):   # the stairs come down onto the nearest street, or into the place itself
            if at_r["geom"].buffer(1).contains(e): continue
            o = walk_to.geometries[int(np.atleast_1d(walk_to.query_nearest(e))[0])]
            q = nearest_points(o, e)[0]
            if q.distance(e) > 0.5: lk = LineString([e, q]); PATHS.append(("link", lk)); clear_geoms.append(lk.buffer(1.2))
JT = PROF.get("jetty")
if JT and JT["poi"] in POIS:   # a canoe jetty: from the shore road straight out over the water, toward the creek villages
    pin = POIS[JT["poi"]]; shore = [e for n, e, nb in edge_roads if nb is None and e.distance(water) < 20]
    if shore:
        sh = min(shore, key=lambda e: e.distance(pin)); q = sh.interpolate(sh.project(pin)); w0 = nearest_points(water, q)[0]
        L = q.distance(w0) or 1; ux, uy = (w0.x - q.x) / L, (w0.y - q.y) / L
        STRUCT.append({"kind": "jetty", "name": JT["name"], "geom": LineString([q, (w0.x + ux * JT["m"], w0.y + uy * JT["m"])]), "layer": 0, "width": 2.5})
        poi_pos[JT["poi"]] = Point(w0.x + ux * JT["m"], w0.y + uy * JT["m"])
SKY_CLEAR = [x["geom"].buffer(x["width"] / 2 + 1) for x in STRUCT if x["kind"] == "skywalk"]
if PROF.get("station_skywalk") and RES_U is not None: SKY_CLEAR = [c.difference(RES_U) for c in SKY_CLEAR]   # the decks land inside the terminal and station plots
clear_geoms += SKY_CLEAR
blocked = unary_union(clear_geoms + [parcel_u.buffer(1.0)])
buildable = land.difference(blocked)
road_free = land.difference(unary_union(clear_geoms))   # parcel buildings may fill their parcel but never touch a road
road_free_ns = land.difference(unary_union([c for c in clear_geoms if not any(c is x for x in SKY_CLEAR)]))
bld = []; tree = None
def free(r, pad=0.0):
    if not buildable.contains(r): return False
    for o in near(r):
        if o.distance(r) < pad: return False
    return True
grid = {}
def near(r):
    if PROF:  # every building whose centre could reach r (big frontage buildings are up to ~40 m long)
        x0, y0, x1, y1 = r.bounds; out = []
        for i in range(int((x0 - 25) // 30), int((x1 + 25) // 30) + 1):
            for j in range(int((y0 - 25) // 30), int((y1 + 25) // 30) + 1): out += grid.get((i, j), [])
        return out
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
REACH = STRtree([g for k, g in net_lines] + lanes + [g for k, g in PATHS]) if W else None
def reachable(r):   # someone has to walk to its door: no building more than 44 m from a street, lane or path
    return REACH is None or len(np.atleast_1d(REACH.query_nearest(r, max_distance=44))) > 0
def place(plot, r):
    if not reachable(r): return False
    if plot.buffer(0.05).contains(r) and buildable.contains(r) and not any((o.distance(r) < 0.15) if PROF else (o.intersection(r).area > 0.05) for o in near(r)): add(r, kind_now[0]); return True   # 15 cm: survives rounding to 0.1 m
    return False
kind_now = ["front"]
plot_count = 0; vacant = 0
# frontage = every block edge, plus both sides of dead-end streets that poke into a block (they have houses too)
btree = STRtree(blocks); fronts = []
for bi, b in enumerate(blocks):
    if (mostly_parcel(b) if PROF else parcel_u.buffer(-1).intersects(b.representative_point())) or b.area < 250: continue
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
                if bb.contains(pt) and bb.exterior.distance(mid) > 0.5 and not (mostly_parcel(bb) if PROF else parcel_u.buffer(-1).intersects(bb.representative_point())):
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
        if PROF.get("rail_frontage") and rail.distance(Point((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)) < 1: cl = CLEAR["rail"]   # houses back onto the line
        a = math.atan2(uy, ux); t = 0.0
        big_ok = PROF and cl >= CLEAR["main"]   # big shops, plazas and warehouses face the main roads (real: 73 m from a main vs 183 m for all)
        while t < L - 4:
            big = big_ok and rnd.random() < RULE["big_front"]
            w = (rnd.uniform(18, 34) if big else RULE["short_side"](rnd.uniform(*PROF.get("plot_u", (.35, .97))))) + RULE["gap"]()
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
            if rnd.random() < PROF.get("vacant", 0.07): vacant += 1; continue          # vacant / abandoned plot
            gap = RULE["gap"](); hw = w - gap; base = (P0[0] + ux * w / 2, P0[1] + uy * w / 2)
            def at(off, d, ww):  # rectangle whose front edge sits `off` metres in from the street centreline
                return rect(base[0] + nx_ * (off + d / 2), base[1] + ny_ * (off + d / 2), ww, d, a)
            off = cl + abs(rnd.gauss(0, 2.2)); first = True
            while off < dmax - 3:
                sh, lo = size(RULE.get("size_lo_u", 0.25))
                if first and big: d = rnd.uniform(18, 40)          # 400-1,300 m2: the real 400-1,500 m2 band
                elif first: d = lo if rnd.random() < RULE["perp_front"] else sh
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
                off += rnd.uniform(*PROF.get("courtyard_m", (1.5, 4)))   # courtyard
            if rnd.random() < RULE["outbuilding"]:
                kind_now[0] = "shed"; ow, od = rnd.uniform(2.2, 4.5), rnd.uniform(2.2, 4.0)
                r = at(dmax - od - 0.3, od, ow)
                if not any(o.intersects(r) for o in near(r)): place(plot, r)   # fix: sheds used to land on top of back houses
# kiosks and sheds on leftover frontage (the many <60 m2 structures)
for k, g in net_lines:
    if k == "art": continue
    for i in range(int(g.length // 70)):
        p = g.interpolate(rnd.uniform(0, g.length)); q = g.interpolate(min(g.length, g.project(p) + 1))
        a = math.atan2(q.y - p.y, q.x - p.x); side = rnd.choice((1, -1)); off = CLEAR.get(k, 3.4) + 1.6
        r = rect(p.x - math.sin(a) * off * side, p.y + math.cos(a) * off * side, rnd.uniform(2.2, 4), rnd.uniform(2, 3.2), a)
        if free(r, 0.2): add(r, "kiosk")
# small named things on the street edge near their pins: a transformer, a food stall
for sp in PROF.get("spots", []):
    pin = POIS.get(sp["poi"])
    if pin is None: continue
    got = None
    for k, g in sorted(net_lines, key=lambda kg: kg[1].distance(pin)):
        if k == "art" or g.distance(pin) > 150: continue
        t0 = g.project(pin)
        for dt in sorted(range(-120, 121, 2), key=abs):
            if not 0 < t0 + dt < g.length: continue
            q = g.interpolate(t0 + dt); ux, uy = LMK.direction_at(g, t0 + dt); off = CLEAR.get(k, 3.4) + sp["d"] / 2 + 0.2
            for side in (1, -1):
                r = rect(q.x - uy * off * side, q.y + ux * off * side, sp["w"], sp["d"], math.atan2(uy, ux))
                if free(r, 0.3): got = r; break
            if got: break
        if got: break
    if got: add(got, sp["kind"]); poi_pos[sp["poi"]] = got.centroid
    else: print("no room for", sp["poi"], file=sys.stderr)
# a print row: the house fronts along one street near the pin are presses and copy shops
PR = PROF.get("print_row")
if PR and PR["poi"] in POIS:
    pin = POIS[PR["poi"]]; sg = min([g for g in streets if g.length > PR["length_m"] * 0.6], key=lambda g: g.distance(pin))
    t0 = min(max(sg.project(pin), PR["length_m"] / 2), sg.length - PR["length_m"] / 2)
    row = substring(sg, max(0, t0 - PR["length_m"] / 2), min(sg.length, t0 + PR["length_m"] / 2))
    bld = [(r, "print" if k == "front" and r.distance(row) < CLEAR["street"] + 2 and 0 < row.project(r.centroid) < row.length else k) for r, k in bld]
    poi_pos[PR["poi"]] = row.interpolate(0.5, normalized=True)
for sp in [x for x in PROF.get("named", []) if set(x["from"]) & {"front", "back"}]:   # a house near the pin becomes the studio, the cafe, Tunde's room
    pin = POIS.get(sp["poi"])
    if pin is None: continue
    cands = [i for i, (r, k) in enumerate(bld) if k in sp["from"]]
    if not cands: continue
    i = min(cands, key=lambda i: bld[i][0].distance(pin))
    if sp.get("kind"): bld[i] = (bld[i][0], sp["kind"])
    poi_pos[sp["poi"]] = bld[i][0].centroid
NAMED_LATE = [sp for sp in PROF.get("named", []) if not set(sp["from"]) & {"front", "back"}]
extra_parcels = []
# parcel buildings: market sheds, warehouses (the big >1500 m2 buildings sit near mains), school blocks
for p in parcels:
    g = p["geom"]; mr = g.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
    e = (cc[0], cc[1]) if math.dist(cc[0], cc[1]) >= math.dist(cc[1], cc[2]) else (cc[1], cc[2])
    a = math.atan2(e[1][1] - e[0][1], e[1][0] - e[0][0]); ctr = g.centroid; LL = max(math.dist(cc[0], cc[1]), math.dist(cc[1], cc[2]))
    if p["kind"] == "industrial":
        for dx in (-1, 1):
            r = rect(ctr.x + math.cos(a) * dx * 30, ctr.y + math.sin(a) * dx * 30, 46, 30, a)
            if g.contains(r): bld.append((r, "warehouse"))
    if p["kind"] == "market" and not PROF:
        for i in range(-3, 4):
            for j in range(-2, 3):
                r = rect(ctr.x + math.cos(a) * i * 13 - math.sin(a) * j * 11, ctr.y + math.sin(a) * i * 13 + math.cos(a) * j * 11, 10, 7, a)
                if g.buffer(-3).contains(r): bld.append((r, "stalls"))
    if p["kind"] == "school":
        for j in (-1, 1):
            r = rect(ctr.x - math.sin(a) * j * 14, ctr.y + math.cos(a) * j * 14, min(46, LL - 12), 8, a)
            if g.contains(r): bld.append((r, "school"))
    if not PROF: continue
    fit = lambda r: g.contains(r) and road_free.contains(r)
    bld[:] = [(r, k) for r, k in bld if not (k in ("warehouse", "stalls", "school") and r.intersects(g) and not road_free.contains(r))]   # v1 parcel buildings must clear roads too
    if p["kind"] == "market":   # a parts market: back-to-back rows of lock-up stalls with narrow aisles, cleared off its access road
        spine = None
        if W:   # a walk-through aisle across the rows, from the market's own road to the road in front
            c = g.centroid; ux, uy = -math.sin(a), math.cos(a); stop = unary_union(access + [x for n, k, x in arts] + [e for n, e, nb in edge_roads])
            ends = []
            for sg in (1, -1):
                ray = LineString([c, (c.x + ux * sg * 400, c.y + uy * sg * 400)]); x = ray.intersection(stop)
                hits = [h for h in getattr(x, "geoms", [x]) if h.geom_type == "Point"]
                ends.append(min(hits, key=ray.project) if hits else None)
            if all(ends): spine = LineString(ends); PATHS.append(("market aisle", spine))
        spines = [spine] if spine is not None else []
        if W and PROF.get("market_through_aisle"):   # and one along its length, end to end
            c = g.centroid; ends = []
            for sg in (1, -1):
                ray = LineString([c, (c.x + math.cos(a) * sg * 400, c.y + math.sin(a) * sg * 400)]); x = ray.intersection(stop)
                hits = [h for h in getattr(x, "geoms", [x]) if h.geom_type == "Point"]
                ends.append(min(hits, key=ray.project) if hits else None)
            if all(ends): spines.append(LineString(ends)); PATHS.append(("market aisle", spines[-1]))
        for r in LMK.stall_rows(g.buffer(-2), a, w=16, d=4, aisle=3.5):   # each piece is a row of four lock-ups under one roof
            if road_free.contains(r) and all(r.distance(sp) > 1.5 for sp in spines): bld.append((r, "stalls"))
    if p["kind"] == "estate":   # 1970s walk-up flats in rows, gardens between, shops built into the gardens
        ES = next(x for x in PROF["parcels"] if x["kind"] == "estate"); bl, bs, gap, garden = ES["block_m"][1], ES["block_m"][0], ES["gap_m"], ES["garden_m"]
        ca, sa = math.cos(a), math.sin(a); R = LL
        for v in np.arange(-R, R, bs + garden):
            for u in np.arange(-R, R, bl + gap):
                cx, cy = ctr.x + u * ca - v * sa, ctr.y + u * sa + v * ca
                r = rect(cx, cy, bl, bs, a)
                if not (g.buffer(-3).contains(r) and road_free.contains(r)): continue
                bld.append((r, "flats"))
                k = rect(cx - (bs / 2 + 5) * -sa, cy - (bs / 2 + 5) * ca, 3.5, 3.0, a)   # a lock-up shop in the front garden
                if rnd.random() < ES["shop_share"] and g.buffer(-1).contains(k) and road_free.contains(k): bld.append((k, "kiosk"))
    if p["kind"] == "under bridge":   # rows of stalls between the slip road and the flyover
        for r in LMK.stall_rows(g, a): 
            if road_free.contains(r): bld.append((r, "stalls"))
    if p["kind"] == "bus terminal":   # the terminal building faces the arterial; bus bays behind it
        R0 = next(x for x in RES if x["geom"] is g); fl, t, side, off, w, d, a2 = R0["info"]; sp = R0["spec"]["building"]
        pp = fl.interpolate(t); ux, uy = LMK.direction_at(fl, t); nx2, ny2 = -uy * side, ux * side
        bw = w * 0.9; bd = min(d - 6, w * d * sp["share"] / bw)
        r = rect(pp.x + nx2 * (off + 1 + 2 + bd / 2), pp.y + ny2 * (off + 1 + 2 + bd / 2), bw, bd, a2)
        if g.contains(r) and road_free_ns.contains(r):
            bld.append((r, "terminal"))
            for x in STRUCT:   # the skywalks come down inside the terminal
                if x["kind"] == "skywalk" and x["geom"].intersects(r):
                    x["geom"] = max(lines(x["geom"].difference(r.buffer(x["width"] / 2 + 0.3))), key=lambda l: l.length)   # the deck stops at the facade
    if p["kind"] == "station":
        R0 = next(x for x in RES if x["geom"] is g); fl, t, side, off, w, d, a2 = R0["info"]; m2 = R0["spec"]["building"]["m2"]
        pp = fl.interpolate(t); ux, uy = LMK.direction_at(fl, t); nx2, ny2 = -uy * side, ux * side
        bd = min(d - 4, 20.0); bw = m2 / bd
        r = rect(pp.x + nx2 * (off + 1 + d - 2 - bd / 2), pp.y + ny2 * (off + 1 + d - 2 - bd / 2), bw, bd, a2)
        if fit(r):
            bld.append((r, "station"))
            for x in STRUCT:   # the station skywalk comes down at the facade, as the terminal's does
                if x["name"] == PROF.get("station_skywalk", {}).get("name"):
                    x["geom"] = max(lines(LineString([x["geom"].coords[0], r.centroid.coords[0]]).difference(r.buffer(x["width"] / 2 + 0.3))), key=lambda l: l.length)
    if p["kind"] == "stadium":
        R0 = next(x for x in RES if x["geom"] is g)
        st_, pitch = LMK.stands(g, R0["spec"]["bowl_m2"])
        bld += [(r, "stands") for r in st_ if fit(r)]
        extra_parcels.append({"kind": "pitch", "geom": pitch})
    if p["kind"] == "park":   # a protest ground: open, with a raised stage at one end
        r = rect(ctr.x + math.cos(a) * (LL / 2 - 12), ctr.y + math.sin(a) * (LL / 2 - 12), 8, 14, a)
        if fit(r): bld.append((r, "stage"))
    if p["kind"] in ("motor park", "lorry park"):   # union office shack and the levy table shelter
        for k2, (w2, d2) in enumerate(((6, 4), (4, 3))):
            r = rect(ctr.x + math.cos(a) * (k2 * 9 - 4), ctr.y + math.sin(a) * (k2 * 9 - 4), w2, d2, a)
            if fit(r): bld.append((r, "shed"))
parcels += extra_parcels
for sp in NAMED_LATE:   # places inside a parcel, named after its buildings exist (The steal: the stall at the market's near end)
    pin = POIS.get(sp["poi"]); cands = [r for r, k in bld if k in sp["from"]]
    if pin is not None and cands: poi_pos[sp["poi"]] = min(cands, key=lambda r: r.distance(pin)).centroid
# the old highlife hotel: a tall block on a main-road frontage near its pin; the houses it replaces are cleared
H = PROF.get("hotel")
if H and H["poi"] in POIS:
    hp = POIS[H["poi"]]; hw_ = math.sqrt(H["m2"] / 1.15); hd_ = H["m2"] / hw_
    cands = sorted([(r, k) for r, k in bld if k == "front" and r.distance(mainU) < CLEAR["main"] + 4], key=lambda rk: rk[0].centroid.distance(hp))
    for r0, k0 in cands[:200]:
        mr = r0.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
        q = mainU.interpolate(mainU.project(r0.centroid)); dxy = (r0.centroid.x - q.x, r0.centroid.y - q.y); L0 = math.hypot(*dxy) or 1
        ux2, uy2 = dxy[0] / L0, dxy[1] / L0; a3 = math.atan2(ux2, -uy2)
        off3 = CLEAR["main"] + 2 + hd_ / 2
        hr = rect(q.x + ux2 * off3, q.y + uy2 * off3, hw_, hd_, a3)
        if road_free.contains(hr) and not hr.intersects(parcel_u):
            bld = [(r, k) for r, k in bld if not r.intersects(hr.buffer(1.5))]
            bld.append((hr, "hotel")); poi_pos[H["poi"]] = hr.centroid; break

# ---------- 5. civic slots: real plots the civic layer can sit on ----------
slots = []
for r, kind in bld:
    if kind in ("front", "back") and r.area > 90:
        d = r.distance(mainU); slots.append({"x": round(r.centroid.x), "y": round(r.centroid.y), "main": d < 40})
rnd.shuffle(slots)

# ---------- 6. measure against the real core squares ----------
B = [r for r, k in bld]
gen_streets = [("street", g) for g in streets + access] + [("main", e) for n, e, nb in edge_roads] + [("main", ln) for n, ln in mains + [("", r) for r in ramps]] + [("art", a) for n, k, a in arts]
M = measure(gen_streets, B, land.buffer(3))
# edge roads are shared with neighbours: count half of their length in the density figures
half = sum(e.intersection(land.buffer(1)).length for n, e, nb in edge_roads) / 2000 / (land.area / 1e6)
M["drive_km_per_km2_edges_half"] = round(M["drive_km_per_km2"] - half, 1); M["main_km_per_km2_edges_half"] = round(M["main_km_per_km2"] - half, 2)
_bt = STRtree(B)   # counted, not assumed (the Maze's v1 file said 0 but its sheds overlapped back houses)
if PROF.get("level_crossings"): M["level_crossings"] = len(LX)
M["building_overlaps"] = int(sum(1 for i, b in enumerate(B) for j in _bt.query(b) if j > i and b.intersection(B[j]).area > 0.05))

# ---------- 7. storeys: match the inspiration area's height bands (share of built area), tallest on big plots near main roads ----------
storeys = None
if PROF:
    srnd = random.Random(SEED * 31 + 5); bands = height_bands(PROF["lgas"])
    FIXED = {"kiosk": 1, "shed": 1, "stalls": 1, "stage": 1, "checkpoint": 1, "warehouse": 2, "school": 2, "stands": 4, "terminal": 3, "station": 2, "transformer": 1}
    FIXED.update({"flats": x["storeys"] for x in PROF.get("parcels", []) if x["kind"] == "estate"})
    FIXED.update({k: x["spec"]["building"]["storeys"] for x in RES if x.get("spec", {}).get("building") for k in [x["spec"]["building"]["kind"]]})
    if PROF.get("hotel"): FIXED["hotel"] = PROF["hotel"]["storeys"]
    storeys = [FIXED.get(k) for r, k in bld]
    def band_of(st): return next(i for i, (lo, hi) in enumerate(STOREY_BANDS) if lo <= st <= hi)
    tot = sum(r.area for r, k in bld); target = [b * tot for b in bands]
    for (r, k), st in zip(bld, storeys):   # the fixed buildings use up part of their band's share
        if st: target[band_of(st)] -= r.area
    free_i = [i for i, st in enumerate(storeys) if st is None]
    # tallness: bigger footprint, nearer a main road, plus noise (real: big buildings sit nearer mains, 73 m vs 183 m)
    score = {i: math.log(bld[i][0].area) - bld[i][0].distance(mainU) / 120 + srnd.gauss(0, .6) for i in free_i}
    order = sorted(free_i, key=lambda i: -score[i])   # tallest first, so the rare tall bands are filled exactly and rounding lands in the big 1-storey band
    b = 6; acc = 0.0
    for i in order:
        while b > 0 and acc >= max(0, target[b]): b -= 1; acc = 0.0
        lo, hi = STOREY_BANDS[b]; storeys[i] = lo if lo == hi else min(hi, lo + int(srnd.expovariate(1.2)))
        acc += bld[i][0].area
    if PROF.get("print_row"):   # the presses sit in 2-3 storey houses (district model); the band shares barely move
        lo, hi = PROF["print_row"]["storeys"]; storeys = [min(hi, max(lo, st)) if k == "print" else st for st, (r, k) in zip(storeys, bld)]
    M["storeys_share_by_area"] = [round(sum(bld[i][0].area for i in range(len(bld)) if band_of(storeys[i]) == q) / tot, 3) for q in range(7)]
    M["storeys_target_by_area"] = [round(x, 3) for x in bands]
print(json.dumps({"seed": SEED, "scale": SCALE, "gidi": M, "real_median": {k: CORE["median"][k] for k in M if k in CORE["median"]}, "real_dense": {k: CORE["dense"][k] for k in M if k in CORE["dense"]}}, indent=1))

R2 = lambda g: [[round(x, 1), round(y, 1)] for x, y in g.coords]
out = {"id": DID, "seed": SEED, "method": "original generator calibrated on OSM statistics of the inspiration area; no real geometry used",
       "streets": [R2(g) for g in streets + access],
       "lanes": [R2(g) for g in lanes],
       **({"paths": [{"kind": k, "pts": R2(g)} for k, g in PATHS]} if PATHS else {}),
       "mains": [{"name": n, "pts": R2(e), "edge_with": nb} for n, e, nb in edge_roads] + [{"name": n, "pts": R2(ln)} for n, ln in mains] + [{"name": "", "pts": R2(l)} for l in links] + [{"name": "Interchange slip road", "pts": R2(r)} for r in ramps],
       "canal": R2(canal) if canal else None,
       "buildings": [[k] + [[round(x, 1), round(y, 1)] for x, y in list(r.exterior.coords)[:-1]] for r, k in bld],
       "parcels": [{"kind": p["kind"], "pts": [[round(x, 1), round(y, 1)] for x, y in p["geom"].exterior.coords]} for p in parcels],
       "poi_pos": {k: [round(v.x), round(v.y)] for k, v in poi_pos.items()}, "slots": slots[:400], "metrics": M}
if PROF:
    out["storeys"] = storeys
    out["structures"] = [{"kind": x["kind"], "name": x["name"], "pts": R2(x["geom"]), "layer": x["layer"], "width": x["width"]} for x in STRUCT] \
        + [{"kind": "ramp", "name": "Interchange slip road", "pts": R2(r), "layer": 0, "width": 8} for r in ramps]
json.dump(out, open(OUT, "w"), separators=(",", ":"))
_k = lambda L: sorted(json.dumps(g, sort_keys=True) for g in L)
if _k(NET["gateways"]) == _k(NET_GW0): NET["gateways"] = NET_GW0
if OUT == f"web/gen-{DID}.json": json.dump(NET, open(NET_F, "w"), indent=1)
