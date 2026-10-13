# Pattern study, step 3: gateways to neighbours (deduplicated) and the spread of fabric density over 1 km squares.
import sys, pickle, json, numpy as np, warnings; warnings.filterwarnings("ignore")
from collections import Counter, defaultdict
from shapely.geometry import box, Point
from shapely.ops import unary_union
DID = sys.argv[1]; D = pickle.load(open(f"study-{DID}.pkl", "rb")); R = json.load(open(f"study-{DID}.json"))
AREA = D["area"]; bd = AREA.boundary; NB = D["neighbours"]
MAJOR = {"motorway","trunk","primary","secondary"}; MID = {"tertiary"}; MINOR = {"residential","unclassified","living_street"}
pts = []
for t, g in D["halo_roads"]:
    c = t.get("highway","").replace("_link","")
    if c not in MAJOR | MID | MINOR: continue
    x = g.intersection(bd)
    for q in getattr(x, "geoms", [x]):
        if q.geom_type == "Point": pts.append((q, "main" if c in MAJOR | MID else "minor", t.get("name") or "", c))
# cluster crossings within 120 m (dual carriageways, roads running along the edge)
gw = []
for q, k, n, c in sorted(pts, key=lambda p: p[1] != "main"):
    hit = next((g for g in gw if g["pt"].distance(q) < 120 and (g["kind"] == k or k == "minor")), None)
    if hit: hit["names"].add(n); continue
    gw.append({"pt": q, "kind": k, "names": {n}, "cls": c, "nb": min(NB, key=lambda m: m[1].distance(q))[0]})
per = bd.length / 1000
main = [g for g in gw if g["kind"] == "main"]; minor = [g for g in gw if g["kind"] == "minor"]
ss = sorted(bd.project(g["pt"]) for g in main)
gaps = np.diff(ss + [ss[0] + bd.length])
C = {"perimeter_km": round(per, 1), "main_gateways": len(main), "minor_gateways": len(minor),
     "main_gateways_per_km_edge": round(len(main) / per, 2), "minor_gateways_per_km_edge": round(len(minor) / per, 2),
     "gap_between_main_gateways_m": {f"p{p}": round(float(np.percentile(gaps, p))) for p in (25, 50, 75)},
     "main_gateways_by_neighbour": dict(Counter(g["nb"] for g in main)), "minor_by_neighbour": dict(Counter(g["nb"] for g in minor)),
     "main_gateway_roads": sorted({n for g in main for n in g["names"] if n})[:30],
     "edge_share_on_hard_line": R["connections"]["edge_share_on_hard_line"]}
# fabric density over 1 km squares fully inside
roads = [(t.get("highway"), g.intersection(AREA)) for t, g in D["roads"]]
B = [g for t, g in D["buildings"]]
from shapely.strtree import STRtree
bt = STRtree(B); rt = STRtree([g for h, g in roads])
minx, miny, maxx, maxy = AREA.bounds; sq = []
for x in np.arange(minx, maxx, 250):
    for y in np.arange(miny, maxy, 250):
        b = box(x, y, x + 1000, y + 1000)
        if not AREA.contains(b): continue
        L = sum(roads[k][1].intersection(b).length for k in rt.query(b) if roads[k][0] in MAJOR | MID | MINOR) / 1000
        cov = sum(B[k].intersection(b).area for k in bt.query(b)) / 1e6
        n = sum(1 for k in bt.query(b) if b.contains(B[k].centroid))
        sq.append((L, cov, n))
sq = np.array(sq)
C["one_km_squares"] = {"n": len(sq), **{f"drive_km_p{p}": round(float(np.percentile(sq[:, 0], p)), 1) for p in (25, 50, 75, 90)},
                       **{f"coverage_p{p}": round(float(np.percentile(sq[:, 1], p)), 2) for p in (25, 50, 75, 90)},
                       **{f"buildings_p{p}": int(np.percentile(sq[:, 2], p)) for p in (25, 50, 75, 90)}}
R["connections_dedup"] = C; json.dump(R, open(f"study-{DID}.json", "w"), indent=1)
pickle.dump(gw, open(f"study-{DID}-gateways.pkl", "wb"))
print(json.dumps(C, indent=1))
