# Pattern study, step 5 (Hub and any transit district): sizes of the big structures a district is known for.
# Flyover spans, interchanges (clusters of slip roads), footbridges, bus terminals/parks, stadiums, rail stations, hotels.
# Statistics only: no real geometry or name goes into Gidi.  Usage: python3 scripts/study_landmarks.py <id>
import sys, pickle, json, numpy as np, warnings; warnings.filterwarnings("ignore")
from shapely.ops import unary_union, linemerge
from shapely.geometry import MultiLineString
DID = sys.argv[1]; D = pickle.load(open(f"study-{DID}.pkl", "rb")); AREA = D["area"]; A = AREA.area / 1e6
def pct(a, ps=(25, 50, 75)):
    a = np.asarray(a, float); return {f"p{p}": round(float(np.percentile(a, p)), 1) for p in ps} if len(a) else {}
def lines(g): return [p for p in getattr(g, "geoms", [g]) if p.geom_type == "LineString" and p.length > 0.5]
def hw(t): return t.get("highway", "")
MAJOR = {"motorway", "trunk", "primary", "secondary"}
R = {"area_km2": round(A, 1)}

# Flyovers: contiguous bridge pieces of major roads (each carriageway is mapped separately, so pieces come in pairs)
br = linemerge(unary_union([g for t, g in D["roads"] if t.get("bridge") and hw(t) in MAJOR | {"tertiary"}]))
spans = [l.length for l in lines(br) if l.length > 15]
R["flyover_spans_m"] = {"n": len(spans), **pct(spans, (25, 50, 75, 90)), "km_per_km2": round(sum(spans) / 1000 / A, 2)}

# Interchanges: slip roads (*_link) clustered within 250 m of each other
links = [g for t, g in D["roads"] if hw(t).endswith("_link")]
cl = list(getattr(unary_union([g.buffer(125) for g in links]), "geoms", [])) if links else []
per = []
for c in cl:
    mine = [g for g in links if c.contains(g.centroid)]
    per.append((len(mine), sum(g.length for g in mine), max((g.length for g in mine), default=0)))
big = [p for p in per if p[1] > 300]  # a real interchange has at least ~300 m of slip road
R["interchanges"] = {"n": len(big), "per_km2": round(len(big) / A, 2), "slip_roads_each": pct([p[0] for p in big]),
                     "slip_road_m_each": pct([p[1] for p in big]), "slip_road_length_m": pct([g.length for g in links], (25, 50, 75, 90))}

# Rail crossings by major roads that are grade-separated (bridge/layer) vs level crossings
rail = unary_union([g for t, g in D["rail"] if t.get("railway") == "rail"])
maj = [(t, g) for t, g in D["roads"] if hw(t).replace("_link", "") in MAJOR | {"tertiary"} and g.intersects(rail)]
R["major_road_rail_crossings"] = {"n": len(maj), "share_bridged": round(np.mean([bool(t.get("bridge") or t.get("layer")) for t, g in maj]), 2) if maj else None}

# Footbridges (pedestrian bridges over the big roads)
fb = [g for t, g in D["roads"] if t.get("bridge") and hw(t) in ("footway", "steps", "path", "pedestrian")]
fbm = lines(linemerge(unary_union(fb))) if fb else []
mkm = sum(g.intersection(AREA).length for t, g in D["roads"] if hw(t) in MAJOR) / 1000
R["footbridges"] = {"n": len(fbm), "length_m": pct([g.length for g in fbm], (25, 50, 75)), "per_km_of_major_road": round(len(fbm) / max(mkm, .1), 2)}

# Bus terminals and motor parks (amenity=bus_station, as land or as buildings)
bs = [(t, g) for t, g in D["landuse"] + D["buildings"] if t.get("amenity") == "bus_station"]
R["bus_stations"] = {"n": len(bs), "area_m2": pct([g.area for t, g in bs], (25, 50, 75, 90)), "max_m2": round(max((g.area for t, g in bs), default=0)),
                     "levels_tagged": [t.get("building:levels") for t, g in bs if t.get("building:levels")]}
pk = [g.area for t, g in D["landuse"] if t.get("amenity") == "parking"]
R["parking_lots_m2"] = pct(pk)

# Stadiums: the bowl (building) and its grounds (leisure=stadium / sports_centre)
R["stadium"] = {"bowl_building_m2": sorted(round(g.area) for t, g in D["buildings"] if t.get("building") == "stadium"),
                "stadium_ground_m2": sorted(round(g.area) for t, g in D["landuse"] if t.get("leisure") == "stadium"),
                "sports_centre_m2": sorted(round(g.area) for t, g in D["landuse"] if t.get("leisure") == "sports_centre")}
mainU = unary_union([g for t, g in D["roads"] if hw(t) in MAJOR])
R["stadium"]["ground_dist_to_main_m"] = [round(g.distance(mainU)) for t, g in D["landuse"] if t.get("leisure") == "stadium"]

# Rail stations (buildings) and hotels (height tag -> storeys at ~3 m)
R["rail_station_building_m2"] = sorted(round(g.area) for t, g in D["buildings"] if t.get("building") == "train_station")
R["rail_stops_per_km_of_track"] = round(sum(1 for t, p in D["points"] if t.get("railway") in ("station", "stop")) / max(.1, rail.intersection(AREA).length / 1000), 2)
R["hotels"] = [{"m2": round(g.area), "height_m": t.get("height")} for t, g in D["buildings"] if t.get("building") == "hotel"]
mk = [g for t, g in D["landuse"] if t.get("amenity") == "marketplace"]
R["markets_m2"] = sorted(round(g.area) for g in mk)
json.dump(R, open(f"study-{DID}-landmarks.json", "w"), indent=1); print(json.dumps(R, indent=1))
