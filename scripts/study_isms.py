# Pattern study, the "Lagos-isms": eccentricities in the real data that a tidy generator would never make, counted the same way
# for every studied area so they can be compared (docs/LAGOS-ISMS.md). Nothing here is built into Gidi.
# Usage: python3 scripts/study_isms.py <study id>   ->   study-<id>-isms.json
# Every count is per km2 of the study area unless it says per km of road. Examples are lon,lat (WGS84) for looking up, never copied.
import sys, json, pickle, math, warnings, collections; warnings.filterwarnings("ignore")
import numpy as np
from shapely.geometry import Point, LineString
from shapely.ops import unary_union
from shapely.strtree import STRtree
from pyproj import Transformer
DID = sys.argv[1]; D = pickle.load(open(f"study-{DID}.pkl", "rb")); AREA = D["area"]; A = AREA.area / 1e6
inv = Transformer.from_crs(32631, 4326, always_xy=True).transform
LL = lambda p: [round(v, 5) for v in inv(p.x, p.y)]
DRIVE = {"motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "living_street", "service"}
MAIN = {"motorway", "trunk", "primary", "secondary"}
HALF_W = {"motorway": 12, "trunk": 9, "primary": 7, "secondary": 6, "tertiary": 5, "unclassified": 3.5, "residential": 3, "living_street": 2.5, "service": 2.5}
hw = lambda t: t.get("highway", "").replace("_link", "")
roads = [(t, g) for t, g in D["roads"] if hw(t) in DRIVE and g.length > 1 and AREA.intersects(g)]
RT = STRtree([g for t, g in roads])
water = [g for t, g in D["water"] if t.get("waterway") in ("canal", "drain", "stream", "ditch", "river")]
rail = [g for t, g in D["rail"] if t.get("railway") in ("rail", "disused", "light_rail")]
WU = unary_union(water) if water else None; RU = unary_union(rail) if rail else None
B = [(t, g) for t, g in D["buildings"] if g.area > 6]; BT = STRtree([g for t, g in B])
out = {"id": DID, "area_km2": round(A, 1), "note": "counts per km2 of the study area; examples are lon,lat"}
def ex(pts, n=3): return [LL(p) for p in pts[:n]]

# road ends: a way end that touches no other drivable way is a dead end
ends = []
for i, (t, g) in enumerate(roads):
    for p in (Point(g.coords[0]), Point(g.coords[-1])):
        if not AREA.contains(p): continue
        if any(j != i and roads[j][1].distance(p) < 1.0 for j in RT.query(p.buffer(1.0))): continue
        ends.append((p, i))
# 1. streets that dead-end at a canal, drain or the rail (they would cross, but there is no bridge or crossing)
at_water = [p for p, i in ends if WU is not None and p.distance(WU) < 15]
at_rail = [p for p, i in ends if RU is not None and p.distance(RU) < 15]
out["dead_end_at_water"] = {"n": len(at_water), "per_km2": round(len(at_water) / A, 2), "examples": ex(at_water)}
out["dead_end_at_rail"] = {"n": len(at_rail), "per_km2": round(len(at_rail) / A, 2), "examples": ex(at_rail)}
# 6. missing links: two dead ends of different streets within 25 m of each other, never joined
ET = STRtree([p for p, i in ends]); ml = []
for k, (p, i) in enumerate(ends):
    for j in ET.query(p.buffer(25)):
        if j > k and ends[j][1] != i and p.distance(ends[j][0]) < 25: ml.append(p); break
out["missing_links"] = {"n": len(ml), "per_km2": round(len(ml) / A, 2), "examples": ex(ml), "rule": "two dead ends of different streets < 25 m apart"}
# 2. buildings over a drainage channel or on its bank (within 3 m of the waterway's line)
bw = [g.centroid for t, g in B if WU is not None and g.distance(WU) < 3]
out["buildings_on_drainage_setback"] = {"n": len(bw), "per_km2": round(len(bw) / A, 2), "examples": ex(bw), "rule": "footprint within 3 m of a canal, drain or stream line"}
# 3. buildings in the road reserve: the footprint reaches into the carriageway (half-width by road class)
br = []
for t, g in B:
    for j in RT.query(g):
        tj, gj = roads[j]
        if g.distance(gj) < HALF_W.get(hw(tj), 3) - 0.5: br.append((g.centroid, hw(tj))); break
out["buildings_in_road_reserve"] = {"n": len(br), "per_km2": round(len(br) / A, 2), "by_road": dict(collections.Counter(c for p, c in br).most_common()),
                                    "examples": ex([p for p, c in br]), "rule": "footprint closer to the road's centreline than its half-width (OSM class)"}
# 4. markets spilling onto the carriageway: a mapped market that reaches a main road's carriageway
mk = [g for t, g in D["landuse"] if t.get("amenity") == "marketplace" or t.get("landuse") == "retail"] + [g.buffer(15) for t, g in D["points"] if t.get("amenity") == "marketplace"]
mains = [(t, g) for t, g in roads if hw(t) in MAIN]
spill = [m.centroid for m in mk if any(m.distance(g) < HALF_W[hw(t)] for t, g in mains)]
out["markets_on_carriageway"] = {"n": len(spill), "of_markets": len(mk), "share": round(len(spill) / max(1, len(mk)), 2), "examples": ex(spill)}
# 5. roads doing too many jobs: side streets joining a main road (per km), bus stops on it, and the km where side streets come every < 30 m
mainL = sum(g.length for t, g in mains) / 1000; side = []
MU = unary_union([g for t, g in mains]) if mains else None
for t, g in roads:
    if hw(t) in MAIN or MU is None: continue
    for p in (Point(g.coords[0]), Point(g.coords[-1])):
        if p.distance(MU) < 1.5: side.append(p)
stops = [g for t, g in D["points"] if t.get("highway") == "bus_stop" and MU is not None and g.distance(MU) < 20]
dense_km = 0.0
for t, g in mains:   # spacing of side junctions along each main road
    pos = sorted(g.project(p) for tt, gg in roads if hw(tt) not in MAIN for p in (Point(gg.coords[0]), Point(gg.coords[-1])) if p.distance(g) < 1.5) if g.length > 100 else []
    gaps = np.diff(pos) if len(pos) > 1 else []
    dense_km += sum(d for d in gaps if d < 30) / 1000
out["overloaded_main_roads"] = {"main_km": round(mainL, 1), "side_junctions_per_km": round(len(side) / max(0.1, mainL), 1), "bus_stops_per_km": round(len(stops) / max(0.1, mainL), 2),
                                "km_with_side_street_every_30m": round(dense_km, 2), "share_of_main_km": round(dense_km / max(0.1, mainL), 3)}
# 7. unfinished buildings (tagged as under construction)
uc = [g.centroid for t, g in B if t.get("building") == "construction"]
out["unfinished_buildings"] = {"n": len(uc), "per_km2": round(len(uc) / A, 2), "share": round(len(uc) / max(1, len(B)), 3), "examples": ex(uc)}
# 8. odd junctions: five or more road ends meeting, or two roads meeting at less than 25 degrees
node = collections.defaultdict(list)
for t, g in roads:
    c = list(g.coords)
    for a, b in ((c[0], c[1]), (c[-1], c[-2])):
        node[(round(a[0]), round(a[1]))].append(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])))
five, acute = [], []
for k, angs in node.items():
    p = Point(k)
    if not AREA.contains(p): continue
    if len(angs) >= 5: five.append(p)
    if len(angs) >= 2:
        diffs = [min(abs(x - y) % 360, 360 - abs(x - y) % 360) for i, x in enumerate(angs) for y in angs[i + 1:]]
        if diffs and min(diffs) < 25: acute.append(p)
out["odd_junctions"] = {"five_way_or_more": {"n": len(five), "per_km2": round(len(five) / A, 2), "examples": ex(five)},
                        "acute_under_25deg": {"n": len(acute), "per_km2": round(len(acute) / A, 2), "examples": ex(acute)}}
# 9. flood-prone low ground: wetland and basins inside or touching homes (OSM); the LGA's share of land below 3 m (Copernicus DEM, lga_table)
wet = [g for t, g in D["landuse"] if t.get("natural") == "wetland" or t.get("landuse") in ("basin", "reservoir") or t.get("flood_prone") == "yes"]
res = unary_union([g for t, g in D["landuse"] if t.get("landuse") == "residential"]) if any(t.get("landuse") == "residential" for t, g in D["landuse"]) else None
wet_in = [w for w in wet if res is not None and w.intersects(res)]
bwet = [g.centroid for t, g in B if any(g.intersects(w) for w in wet)] if wet and len(B) < 200000 else []
out["flood_prone"] = {"wetland_ha": round(sum(w.area for w in wet) / 1e4, 1), "wetland_touching_homes_ha": round(sum(w.area for w in wet_in) / 1e4, 1),
                      "buildings_in_wetland": len(bwet), "per_km2": round(len(bwet) / A, 2), "examples": ex(bwet),
                      "note": "the 30 m DEM is not on this machine; the LGA's share of land below 3 m comes from data/results/lga_table.json"}
# 10. pedestrians forced onto expressways: km of motorway and trunk, bus stops on them, and the longest stretch with no way across on foot
xp = [(t, g) for t, g in D["roads"] if hw(t) in ("motorway", "trunk") and AREA.intersects(g)]
xu = unary_union([g for t, g in xp]) if xp else None
crossings = [g for t, g in D["roads"] if (t.get("highway") in ("footway", "path", "steps", "pedestrian") or t.get("bridge") or t.get("tunnel")) and xu is not None and g.crosses(xu)] + \
            [g for t, g in D["points"] if t.get("highway") == "crossing" and xu is not None and g.distance(xu) < 10]
xstops = [g for t, g in D["points"] if t.get("highway") == "bus_stop" and xu is not None and g.distance(xu) < 20]
gaps = []
for t, g in xp:
    if g.length < 300: continue
    pos = sorted([0.0, g.length] + [g.project(c.centroid) for c in crossings if c.distance(g) < 15])
    gaps.append((max(np.diff(pos)), g.interpolate(pos[int(np.argmax(np.diff(pos)))] + max(np.diff(pos)) / 2)))
gaps.sort(key=lambda x: -x[0])
out["pedestrians_on_expressways"] = {"expressway_km": round(sum(g.length for t, g in xp) / 1000, 1), "bus_stops_on_them": len(xstops),
                                     "ways_across_on_foot": len(crossings), "longest_stretch_without_crossing_m": round(gaps[0][0]) if gaps else 0,
                                     "examples": ex([p for d, p in gaps])}
json.dump(out, open(f"study-{DID}-isms.json", "w"), indent=1)
print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "examples"}) for k, v in out.items()}, indent=1)[:3000])
