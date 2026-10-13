# Compare a Gidi district's street fabric and public places with its real Lagos inspiration (OSM, ODbL).
import json, sys, math, osmium, shapely.wkb as wl
from shapely.geometry import shape, LineString, Point, Polygon
from shapely.ops import unary_union, transform
from pyproj import Transformer
LGAS = sys.argv[1].split(","); DID = sys.argv[2]
tr = Transformer.from_crs(4326, 32631, always_xy=True).transform  # UTM 31N, metres
adm = json.load(open("adm6.geojson"))
area = unary_union([shape(f["geometry"]) for f in adm["features"] if f["properties"].get("name") in LGAS and f["properties"].get("admin_level") == "6"
                    and 2.6 < shape(f["geometry"]).representative_point().x < 4.4])
area_m = transform(tr, area); A = area_m.area / 1e6
f = osmium.geom.WKBFactory(); roads = []; amen = []
DRIVE = {"motorway","trunk","primary","secondary","tertiary","unclassified","residential","living_street","service","motorway_link","trunk_link","primary_link","secondary_link","tertiary_link"}
class H(osmium.SimpleHandler):
    def way(s, w):
        h = w.tags.get("highway")
        if h in DRIVE or h in ("footway","path","track"):
            try: g = wl.loads(f.create_linestring(w), hex=True)
            except Exception: return
            if g.intersects(area): roads.append((h, transform(tr, g.intersection(area))))
    def node(s, n):
        t = n.tags; k = t.get("amenity") or t.get("shop") or t.get("leisure") or t.get("landuse")
        if k and area.contains(Point(n.location.lon, n.location.lat)): amen.append((k, t.get("religion",""), transform(tr, Point(n.location.lon, n.location.lat))))
    def area(s, a):
        t = a.tags; k = t.get("amenity") or t.get("leisure") or t.get("landuse")
        if not k: return
        try: g = wl.loads(f.create_multipolygon(a), hex=True)
        except Exception: return
        c = g.representative_point()
        if area.contains(c): amen.append((k, t.get("religion",""), transform(tr, c)))
H().apply_file("lagos.osm.pbf", locations=True)
def km(h): return sum(g.length for x, g in roads if x in h) / 1000
drive = [g for h, g in roads if h in DRIVE and h not in ("service",)]
L = sum(g.length for g in drive) / 1000
ends = {}
for g in drive:
    for part in getattr(g, "geoms", [g]):
        if part.geom_type != "LineString": continue
        for c in (part.coords[0], part.coords[-1]):
            k = (round(c[0]), round(c[1])); ends[k] = ends.get(k, 0) + 1
inter = sum(1 for v in ends.values() if v >= 3)
from collections import Counter
cats = Counter()
for k, rel, _ in amen:
    if k == "place_of_worship": cats["church" if rel == "christian" else "mosque" if rel == "muslim" else "worship (other)"] += 1
    elif k in ("school","college","university","kindergarten"): cats["school"] += 1
    elif k in ("hospital","clinic","doctors"): cats["hospital/clinic"] += 1
    elif k == "pharmacy" or k == "chemist": cats["chemist"] += 1
    elif k in ("police","fire_station","townhall","courthouse"): cats["police/fire/council"] += 1
    elif k == "fuel": cats["fuel"] += 1
    elif k in ("bank","atm"): cats["bank"] += 1
    elif k in ("marketplace",): cats["market"] += 1
    elif k in ("bus_station","taxi","parking"): cats["motor park/parking"] += 1
    elif k in ("pitch","stadium","sports_centre","park","playground","recreation_ground"): cats["park/pitch"] += 1
    elif k in ("restaurant","fast_food","bar","pub","cafe"): cats["food/drink"] += 1
    elif k in ("cemetery","grave_yard"): cats["cemetery"] += 1
out = {"lgas": LGAS, "area_km2": round(A, 2), "drive_km": round(L, 1), "drive_km_per_km2": round(L / A, 1),
       "intersections_per_km2": round(inter / A), "by_class_km": {h: round(km({h}), 1) for h in ["primary","secondary","tertiary","residential","unclassified","service","footway","path"]},
       "places": dict(cats), "places_per_km2": {k: round(v / A, 1) for k, v in cats.items()}}
# Gidi district for comparison
s = open("web/gidi-data.js").read(); G = json.loads(s[len("window.GIDI="):-1])
d = {x["id"]: x for x in G["districts"]}[DID]; poly = Polygon(d["poly"][0])
gl = sum(LineString(l).length for l in G["streets"][DID]) / 1000 + sum(LineString(m["pts"]).length for m in G["mains"] if m["d"] == DID) / 1000
gends = {}
for l in G["streets"][DID]:
    for c in (l[0], l[-1]): k = (round(c[0]/3), round(c[1]/3)); gends[k] = gends.get(k, 0) + 1
gc = Counter(p["type"] for p in G["pois"] if p["d"] == DID and p.get("civic"))
out["gidi"] = {"area_km2": round(poly.area / 1e6, 2), "drive_km_per_km2": round(gl / (poly.area / 1e6), 1), "civic": dict(gc)}
json.dump(out, open(f"compare-{DID}.json", "w"), indent=1)
print(json.dumps(out, indent=1))
# save real network sample for drawing
import pickle; pickle.dump({"area": area_m, "roads": roads, "amen": amen}, open(f"real-{DID}.pkl", "wb"))
