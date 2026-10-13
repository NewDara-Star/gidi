# Pattern study, step 2: turn the raw inspiration data into rules (statistics only; nothing is copied into Gidi).
import sys, pickle, json, math, warnings; warnings.filterwarnings("ignore")
import numpy as np, networkx as nx
from collections import Counter, defaultdict
from shapely.geometry import LineString, Point, MultiLineString, box
from shapely.ops import unary_union, polygonize, nearest_points
from shapely.strtree import STRtree
DID = sys.argv[1]; D = pickle.load(open(f"study-{DID}.pkl", "rb"))
AREA = D["area"]; A = AREA.area / 1e6; R = {}
def pct(a, ps=(10, 25, 50, 75, 90)): a = np.asarray(a, float); return {f"p{p}": round(float(np.percentile(a, p)), 1) for p in ps} if len(a) else {}
MAJOR = {"motorway","trunk","primary","secondary","motorway_link","trunk_link","primary_link","secondary_link"}
MID = {"tertiary","tertiary_link"}
MINOR = {"residential","unclassified","living_street"}
DRIVE = MAJOR | MID | MINOR
def lines(g): return [p for p in getattr(g, "geoms", [g]) if p.geom_type == "LineString" and p.length > 0.5]
roads = [(t, p) for t, g in D["roads"] for p in lines(g.intersection(AREA))]
cls = lambda t: t.get("highway")
# ---------- ROADS ----------
km = Counter()
for t, g in roads: km[cls(t)] += g.length / 1000
R["road_km_by_class"] = {k: round(v, 1) for k, v in km.most_common()}
R["road_km_per_km2"] = {"drive (no service)": round(sum(v for k, v in km.items() if k in DRIVE) / A, 1), "service": round(km["service"] / A, 1), "foot/path": round((km["footway"] + km["path"] + km["pedestrian"] + km["steps"]) / A, 1)}
tagc = lambda k: Counter(t.get(k) for t, g in roads if cls(t) in DRIVE and t.get(k))
R["surface_tags"] = dict(tagc("surface").most_common(6)); R["lanes_tags"] = dict(tagc("lanes").most_common(6))
R["oneway_share_by_km"] = round(sum(g.length for t, g in roads if cls(t) in DRIVE and t.get("oneway") == "yes") / max(1, sum(g.length for t, g in roads if cls(t) in DRIVE)), 3)
R["named_share_minor"] = round(sum(1 for t, g in roads if cls(t) in MINOR and t.get("name")) / max(1, sum(1 for t, g in roads if cls(t) in MINOR)), 2)
suf = Counter()
for t, g in roads:
    n = t.get("name")
    if n and cls(t) in DRIVE: suf[n.split()[-1].title()] += 1
R["street_name_endings"] = dict(suf.most_common(12))
# noded drive network
drv = [g for t, g in roads if cls(t) in DRIVE]
noded = unary_union(drv)
segs = lines(noded)
key = lambda c: (round(c[0], 1), round(c[1], 1))
Gr = nx.MultiGraph()
segcls = STRtree([g for g in drv]); drvcls = [cls(t) for t, g in roads if cls(t) in DRIVE]
for s in segs:
    m = s.interpolate(0.5, normalized=True)
    i = segcls.query_nearest(m); c = drvcls[int(np.atleast_1d(i)[0])]
    Gr.add_edge(key(s.coords[0]), key(s.coords[-1]), length=s.length, geom=s, cls=c)
deg = Counter(dict(Gr.degree()).values())
inner = AREA.buffer(-30)
degi = Counter(d for n, d in Gr.degree() if inner.contains(Point(n)))
R["junctions"] = {"per_km2": round(sum(v for k, v in degi.items() if k >= 3) / A), "dead_ends_per_km2": round(degi[1] / A),
                  "T_share": round(degi[3] / max(1, sum(v for k, v in degi.items() if k >= 3)), 2), "X_share": round(degi[4] / max(1, sum(v for k, v in degi.items() if k >= 3)), 2),
                  "dead_end_to_junction_ratio": round(degi[1] / max(1, sum(v for k, v in degi.items() if k >= 3)), 2)}
# street lengths between junctions (merge degree-2 chains)
def chains(G):
    out = []; seen = set()
    for u, v, k, d in G.edges(keys=True, data=True):
        if (u, v, k) in seen: continue
        L = d["length"]; seen.add((u, v, k)); seen.add((v, u, k))
        for a, b in ((u, v), (v, u)):
            prev, cur = a, b
            while G.degree(cur) == 2:
                nb = [(x, kk, dd) for x, kk, dd in ((x, kk, dd) for _, x, kk, dd in G.edges(cur, keys=True, data=True)) if (cur, x, kk) not in seen]
                if not nb: break
                x, kk, dd = nb[0]; seen.add((cur, x, kk)); seen.add((x, cur, kk)); L += dd["length"]; prev, cur = cur, x
        out.append((L, d["cls"]))
    return out
ch = chains(Gr)
R["street_length_between_junctions_m"] = {"minor": pct([l for l, c in ch if c in MINOR]), "major+tertiary": pct([l for l, c in ch if c not in MINOR])}
sin = [s.length / max(1, Point(s.coords[0]).distance(Point(s.coords[-1]))) for s in segs if s.length > 40]
R["sinuosity_segments_over_40m"] = pct(sin, (50, 75, 90, 97))
# orientation
def bearings(gs):
    h = np.zeros(36)
    for g in gs:
        c = list(g.coords)
        for (x0, y0), (x1, y1) in zip(c, c[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            if L < 1: continue
            b = math.degrees(math.atan2(x1 - x0, y1 - y0)) % 180; h[int(b // 5) % 36] += L
    return h
def entropy(h):
    p = h / h.sum(); p = p[p > 0]; Hm = math.log(36); H0 = math.log(4)  # Boeing 2019 order
    H = -(p * np.log(p)).sum(); return round(H, 3), round(1 - ((H - H0) / (Hm - H0)) ** 2, 3)
minor_g = [g for t, g in roads if cls(t) in MINOR]
h = bearings(minor_g); H, order = entropy(h)
R["orientation_whole_area"] = {"entropy": H, "grid_order_0to1": order, "top_bearings_deg": [int(i * 5) for i in np.argsort(-h)[:4]]}
# local: 400 m cells -> dominant bearing + order; neighbour turn
minx, miny, maxx, maxy = AREA.bounds; cells = {}; CS = 400
mtree = STRtree(minor_g)
for i in range(int((maxx - minx) // CS) + 1):
    for j in range(int((maxy - miny) // CS) + 1):
        b = box(minx + i * CS, miny + j * CS, minx + (i + 1) * CS, miny + (j + 1) * CS)
        if not AREA.contains(b.centroid): continue
        gs = [minor_g[k].intersection(b) for k in mtree.query(b)]
        gs = [p for g in gs for p in lines(g)]
        if sum(g.length for g in gs) < 1500: continue
        hh = bearings(gs); s2 = np.convolve(np.r_[hh, hh[:2]], [1, 1, 1], "valid")[:36]
        cells[(i, j)] = (int(np.argmax(s2)) * 5 + 5, entropy(hh)[1])
turns = []
for (i, j), (b, o) in cells.items():
    for di, dj in ((1, 0), (0, 1)):
        if (i + di, j + dj) in cells:
            d = abs(cells[(i + di, j + dj)][0] - b) % 180; turns.append(min(d, 180 - d))
R["local_400m_cells"] = {"n": len(cells), "grid_order": pct([o for b, o in cells.values()], (25, 50, 75)),
                        "turn_between_neighbour_cells_deg": pct(turns, (25, 50, 75, 90)), "share_neighbours_turned_over_20deg": round(np.mean(np.array(turns) > 20), 2)}
# parallel spacing of minor streets
mids = []
for g in minor_g:
    for p in lines(g):
        if p.length < 60: continue
        c = list(p.coords); m = p.interpolate(0.5, normalized=True)
        x0, y0 = p.interpolate(0.4, normalized=True).coords[0]; x1, y1 = p.interpolate(0.6, normalized=True).coords[0]
        mids.append((m, math.atan2(y1 - y0, x1 - x0)))
sp = []
for m, a in mids:
    nx_, ny_ = -math.sin(a), math.cos(a); best = None
    ray = LineString([(m.x - nx_ * 250, m.y - ny_ * 250), (m.x + nx_ * 250, m.y + ny_ * 250)])
    for k in mtree.query(ray):
        g = minor_g[k]; x = ray.intersection(g)
        for q in getattr(x, "geoms", [x]):
            if q.geom_type != "Point": continue
            d = m.distance(q)
            if d < 8: continue
            # roughly parallel?
            pr = g.project(q); qa = g.interpolate(max(0, pr - 5)); qb = g.interpolate(min(g.length, pr + 5))
            aa = math.atan2(qb.y - qa.y, qb.x - qa.x); dd = abs((aa - a + math.pi / 2) % math.pi - math.pi / 2)
            if dd < math.radians(20) and (best is None or d < best): best = d
    if best: sp.append(best)
R["parallel_street_spacing_m"] = pct(sp)
# blocks
polys = [p for p in polygonize(noded) if p.area > 150 and inner.contains(p.representative_point())]
ba = [p.area for p in polys]
def elong(p):
    r = p.minimum_rotated_rectangle; c = list(r.exterior.coords); a = Point(c[0]).distance(Point(c[1])); b = Point(c[1]).distance(Point(c[2]))
    return max(a, b) / max(1, min(a, b))
R["blocks"] = {"n": len(polys), "area_m2": pct(ba), "mean_m2": round(float(np.mean(ba))), "elongation_long_over_short": pct([elong(p) for p in polys], (25, 50, 75)),
               "compactness_area_over_rect": pct([p.area / p.minimum_rotated_rectangle.area for p in polys], (25, 50, 75)),
               "width_short_side_m": pct([min(Point(c0).distance(Point(c1)) for c0, c1 in [(list(p.minimum_rotated_rectangle.exterior.coords)[0], list(p.minimum_rotated_rectangle.exterior.coords)[1]), (list(p.minimum_rotated_rectangle.exterior.coords)[1], list(p.minimum_rotated_rectangle.exterior.coords)[2])]) for p in polys])}
# main-road mesh (tertiary and up)
mainnet = unary_union([g for t, g in roads if cls(t) in MAJOR | MID])
sup = [p for p in polygonize(mainnet) if p.area > 5000]
R["main_road_mesh"] = {"superblocks_fully_closed": len(sup), "superblock_area_m2": pct([p.area for p in sup], (25, 50, 75)),
                       "main_km_per_km2": round(sum(v for k, v in km.items() if k in MAJOR | MID) / A, 2)}
# side-street access spacing along mains, and T vs X on mains
mains = [g for t, g in roads if cls(t) in MAJOR | MID]
mainU = unary_union(mains)
acc = defaultdict(list); tx = Counter()
for n, d in Gr.degree():
    if d < 3: continue
    cs = [dd["cls"] for _, _, dd in Gr.edges(n, data=True)]
    if any(c in MAJOR | MID for c in cs) and any(c in MINOR for c in cs):
        tx["T" if d == 3 else "X+"] += 1
for g in mains:
    pts = sorted(g.project(Point(n)) for n, d in Gr.degree() if d >= 3 and Point(n).distance(g) < 1)
    acc["gap"] += [b - a for a, b in zip(pts, pts[1:]) if b - a > 2]
R["side_streets_on_mains"] = {"gap_between_side_junctions_m": pct(acc["gap"]), "T_vs_X": dict(tx)}
# ---------- BUILDINGS ----------
B = [(t, g) for t, g in D["buildings"] if g.area > 6]
bA = np.array([g.area for t, g in B])
R["buildings"] = {"count": len(B), "per_km2": round(len(B) / A), "coverage_share_of_land": round(bA.sum() / AREA.area, 3), "footprint_m2": pct(bA, (10, 25, 50, 75, 90, 99)),
                  "size_bands_share": {"<60": round(np.mean(bA < 60), 2), "60-150": round(np.mean((bA >= 60) & (bA < 150)), 2), "150-400": round(np.mean((bA >= 150) & (bA < 400)), 2), "400-1500": round(np.mean((bA >= 400) & (bA < 1500)), 2), "1500+": round(np.mean(bA >= 1500), 3)},
                  "type_tags": dict(Counter(t.get("building") for t, g in B).most_common(10)), "levels_tagged": dict(Counter(t.get("building:levels") for t, g in B if t.get("building:levels")).most_common(8)),
                  "roof_tags": dict(Counter(t.get("roof:shape") for t, g in B if t.get("roof:shape")).most_common(5))}
def rect(g):
    r = g.minimum_rotated_rectangle; c = list(r.exterior.coords)
    a = Point(c[0]).distance(Point(c[1])); b = Point(c[1]).distance(Point(c[2]))
    ang = math.atan2(c[1][1] - c[0][1], c[1][0] - c[0][0]) if a >= b else math.atan2(c[2][1] - c[1][1], c[2][0] - c[1][0])
    return max(a, b), min(a, b), ang, g.area / max(1, r.area)
RR = [rect(g) for t, g in B]
R["buildings"]["long_side_m"] = pct([r[0] for r in RR]); R["buildings"]["short_side_m"] = pct([r[1] for r in RR])
R["buildings"]["aspect"] = pct([r[0] / max(1, r[1]) for r in RR], (25, 50, 75)); R["buildings"]["rectangularity"] = pct([r[3] for r in RR], (10, 50))
# relation to streets
stree = STRtree(drv); setb = []; angd = []; front = []
for (t, g), r in zip(B, RR):
    c = g.centroid; k = int(np.atleast_1d(stree.query_nearest(c))[0]); s = drv[k]
    d_edge = g.distance(s); setb.append(d_edge)
    pr = s.project(c); qa = s.interpolate(max(0, pr - 5)); qb = s.interpolate(min(s.length, pr + 5))
    sa = math.atan2(qb.y - qa.y, qb.x - qa.x); dd = abs((r[2] - sa + math.pi / 2) % math.pi - math.pi / 2)
    angd.append(math.degrees(dd))
setb = np.array(setb); angd = np.array(angd)
R["buildings"]["edge_to_street_centreline_m"] = pct(setb)
R["buildings"]["share_within_12m_of_street(front row)"] = round(float(np.mean(setb < 12)), 2)
R["buildings"]["angle_to_nearest_street_deg"] = pct(angd, (25, 50, 75)); R["buildings"]["share_aligned_within_15deg_or_perp"] = round(float(np.mean((angd < 15) | (angd > 75))), 2)
R["buildings"]["front_row_long_side_parallel_share"] = round(float(np.mean(angd[setb < 12] < 15)), 2)
# gaps
btree = STRtree([g for t, g in B]); gaps = []
for i, (t, g) in enumerate(B[::7]):
    nb = [B[k][1] for k in btree.query(g.buffer(15)) if B[k][1] is not g]
    if nb: gaps.append(min(g.distance(o) for o in nb))
R["buildings"]["gap_to_nearest_neighbour_m"] = pct(gaps); R["buildings"]["share_touching(<0.5m)"] = round(float(np.mean(np.array(gaps) < 0.5)), 2)
# per block coverage
bc = []; bn = []
for p in polys:
    ks = btree.query(p); cov = sum(B[k][1].intersection(p).area for k in ks)
    bc.append(cov / p.area); bn.append(sum(1 for k in ks if p.contains(B[k][1].centroid)))
R["blocks"]["building_coverage_share"] = pct(bc, (25, 50, 75)); R["blocks"]["buildings_per_block"] = pct(bn, (25, 50, 75))
R["blocks"]["buildings_per_hectare_of_block"] = pct([n / (p.area / 1e4) for n, p in zip(bn, polys) if p.area > 2000], (25, 50, 75))
# big buildings: what and where
big = [(t, g) for t, g in B if g.area > 1500]
R["big_buildings_over_1500m2"] = {"count": len(big), "per_km2": round(len(big) / A, 1), "tags": dict(Counter(t.get("building") for t, g in big).most_common(6)),
                                  "dist_to_main_road_m": pct([g.distance(mainU) for t, g in big], (25, 50, 75)), "all_buildings_dist_to_main_m": pct([g.distance(mainU) for t, g in B[::5]], (25, 50, 75))}
# density variation over 250 m cells
cs = 250; dens = []
for i in range(int((maxx - minx) // cs) + 1):
    for j in range(int((maxy - miny) // cs) + 1):
        b = box(minx + i * cs, miny + j * cs, minx + (i + 1) * cs, miny + (j + 1) * cs)
        if AREA.contains(b): dens.append(sum(B[k][1].intersection(b).area for k in btree.query(b)) / b.area)
R["coverage_variation_250m_cells"] = pct(dens)
# ---------- LAND, WATER, RAIL, POWER, PLACES ----------
lu = defaultdict(float); lun = Counter()
for t, g in D["landuse"]:
    k = t.get("landuse") or t.get("leisure") or t.get("natural") or t.get("amenity"); lu[k] += g.intersection(AREA).area; lun[k] += 1
R["landuse_polygons_ha"] = {k: [lun[k], round(v / 1e4, 1)] for k, v in sorted(lu.items(), key=lambda x: -x[1])[:16]}
R["waterways_km"] = {k: round(sum(g.intersection(AREA).length for t, g in D["water"] if t.get("waterway") == k) / 1000, 2) for k in set(t.get("waterway") for t, g in D["water"])}
rl = [(t, g) for t, g in D["rail"] if t.get("railway") in ("rail", "light_rail", "narrow_gauge", "construction")]
R["rail"] = {"km_in_area": round(sum(g.intersection(AREA).length for t, g in rl) / 1000, 2), "types": dict(Counter(t.get("railway") for t, g in D["rail"]))}
railU = unary_union([g for t, g in rl]) if rl else None
if railU:
    cross = [g for t, g in roads if cls(t) in DRIVE and g.intersects(railU)]
    R["rail"]["drive_roads_crossing"] = len(cross); R["rail"]["of_which_bridge_or_layer"] = sum(1 for t, g in roads if cls(t) in DRIVE and g.intersects(railU) and (t.get("bridge") or t.get("layer")))
    R["rail"]["buildings_within_15m_of_track"] = int(sum(1 for t, g in B if g.distance(railU) < 15)); R["rail"]["buildings_within_30m"] = int(sum(1 for t, g in B if g.distance(railU) < 30))
R["power"] = dict(Counter(t.get("power") for t, g in D["power"]))
pts = Counter(); pnames = defaultdict(list)
for t, p in D["points"]:
    k = t.get("amenity") or t.get("shop") and "shop:" + t["shop"] or t.get("leisure") or t.get("power") and "power:" + t["power"] or t.get("highway") and "hw:" + t["highway"] or t.get("railway") and "rail:" + t["railway"] or t.get("craft") and "craft" or t.get("office") and "office" or t.get("natural") or t.get("man_made") or t.get("tourism")
    pts[k] += 1
R["point_tags"] = dict(pts.most_common(30))
R["trees_mapped"] = pts.get("tree", 0) + sum(1 for t, g in D["landuse"] if t.get("natural") in ("wood", "tree_row", "scrub"))
# markets: size and relation to main roads
mk = [g for t, g in D["landuse"] if t.get("amenity") == "marketplace" or t.get("landuse") == "retail"]
R["markets_and_retail"] = {"n": len(mk), "ha": pct([g.area / 1e4 for g in mk], (25, 50, 75)), "dist_to_main_m": pct([g.distance(mainU) for g in mk], (25, 50, 75))}
pw = [g for t, g in D["landuse"] if t.get("amenity") in ("place_of_worship",) or t.get("landuse") == "religious"] + [p for t, p in D["points"] if t.get("amenity") == "place_of_worship"]
sch = [g for t, g in D["landuse"] if t.get("amenity") in ("school",)] + [p for t, p in D["points"] if t.get("amenity") == "school"]
R["civic_mapped_note"] = {"places_of_worship": len(pw), "schools": len(sch), "warning": "OSM civic coverage here is far below reality; use for placement rules only, not counts"}
R["civic_dist_to_main_m"] = {"worship": pct([g.distance(mainU) for g in pw], (25, 50, 75)), "schools": pct([g.distance(mainU) for g in sch], (25, 50, 75))}
# ---------- CONNECTIONS TO NEIGHBOURS ----------
bd = AREA.boundary; per = bd.length / 1000
cr = defaultdict(list); NB = D["neighbours"]
for t, g in D["halo_roads"]:
    c = cls(t)
    if c not in DRIVE: continue
    x = g.intersection(bd)
    for q in getattr(x, "geoms", [x]):
        if q.geom_type != "Point": continue
        nb = min(NB, key=lambda n: n[1].distance(q))[0]
        cr["major" if c in MAJOR else "tertiary" if c in MID else "minor"].append((nb, bd.project(q)))
R["connections"] = {"perimeter_km": round(per, 1), "crossings": {k: len(v) for k, v in cr.items()}, "per_km_of_edge": {k: round(len(v) / per, 1) for k, v in cr.items()},
                    "major_crossings_by_neighbour": dict(Counter(n for n, s in cr["major"])), "all_crossings_by_neighbour": dict(Counter(n for k in cr for n, s in cr[k]))}
ms = sorted(s for k in ("major", "tertiary") for n, s in cr[k])
R["connections"]["gap_between_main_gateways_m"] = pct(np.diff(ms)) if len(ms) > 2 else {}
# how much of the edge runs along a hard line (major road / rail / water)
hard = unary_union([g for t, g in D["halo_roads"] if cls(t) in MAJOR] + ([railU] if railU else []) + [g for t, g in D["water"]]).buffer(40)
R["connections"]["edge_share_on_hard_line"] = round(bd.intersection(hard).length / bd.length, 2)
through = defaultdict(float)
for t, g in roads:
    if cls(t) in MAJOR and t.get("name"): through[t["name"]] += g.length / 1000
R["through_routes_km"] = {k: round(v, 2) for k, v in sorted(through.items(), key=lambda x: -x[1])[:10]}
R["area_km2"] = round(A, 1)
json.dump(R, open(f"study-{DID}.json", "w"), indent=1)
pickle.dump({"polys": polys, "cells": cells}, open(f"study-{DID}-derived.pkl", "wb"))
print(json.dumps(R, indent=1))
