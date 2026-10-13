# Pattern study, step 1: pull everything OSM knows about an inspiration area (OSM, ODbL). Data stays local; only statistics are used.
import json, sys, pickle, osmium, shapely.wkb as wl
from shapely.geometry import shape, Point
from shapely.ops import unary_union, transform
from shapely.prepared import prep
from pyproj import Transformer
LGAS = sys.argv[1].split(","); DID = sys.argv[2]   # optional 3rd arg: west,south,east,north box in degrees
tr = Transformer.from_crs(4326, 32631, always_xy=True).transform
adm = json.load(open("adm6.geojson"))
lag = [f for f in adm["features"] if f["properties"].get("admin_level") == "6" and 2.6 < shape(f["geometry"]).representative_point().x < 4.4 and 6.3 < shape(f["geometry"]).representative_point().y < 6.75]
area = unary_union([shape(f["geometry"]) for f in lag if f["properties"]["name"] in LGAS])
if len(sys.argv) > 3:   # neighbourhood-level study: only the part of the LGAs inside lon/lat boxes (west,south,east,north;...)
    from shapely.geometry import box as _box
    area = area.intersection(unary_union([_box(*map(float, b.split(","))) for b in sys.argv[3].split(";")]))
ring = area.buffer(0.02)  # ~2 km halo for connections to neighbours
pa, pr = prep(area), prep(ring)
F = osmium.geom.WKBFactory()
D = {"buildings": [], "roads": [], "water": [], "rail": [], "power": [], "landuse": [], "points": [], "halo_roads": []}
KEEP = ("highway","name","width","lanes","surface","oneway","bridge","layer","building","building:levels","height","roof:shape","waterway","railway","power","landuse","leisure","natural","amenity","shop","religion","barrier","craft","office","tourism","man_made")
def tg(o): return {k: o.tags.get(k) for k in KEEP if o.tags.get(k)}
class H(osmium.SimpleHandler):
    def way(s, w):
        t = w.tags
        if not any(k in t for k in ("highway","waterway","railway","power","barrier")): return
        try: g = wl.loads(F.create_linestring(w), hex=True)
        except Exception: return
        if not pr.intersects(g): return
        rec = (tg(w), transform(tr, g))
        if "highway" in t:
            if pa.intersects(g): D["roads"].append(rec)
            D["halo_roads"].append(rec)
        elif "waterway" in t and pa.intersects(g): D["water"].append(rec)
        elif "railway" in t: D["rail"].append(rec)
        elif "power" in t and pa.intersects(g): D["power"].append(rec)
    def area(s, a):
        t = a.tags
        if not any(k in t for k in ("building","landuse","leisure","natural","amenity","waterway","water")): return
        try: g = wl.loads(F.create_multipolygon(a), hex=True)
        except Exception: return
        if not pa.intersects(g.representative_point()): return
        rec = (tg(a), transform(tr, g))
        (D["buildings"] if "building" in t else D["landuse"]).append(rec)
    def node(s, n):
        t = n.tags
        if not any(k in t for k in ("amenity","shop","leisure","power","natural","craft","office","highway","railway","man_made","tourism")): return
        p = Point(n.location.lon, n.location.lat)
        if pa.contains(p): D["points"].append((tg(n), transform(tr, p)))
H().apply_file("lagos.osm.pbf", locations=True)
D["area"] = transform(tr, area)
D["neighbours"] = [(f["properties"]["name"], transform(tr, shape(f["geometry"]))) for f in lag if f["properties"]["name"] not in LGAS and shape(f["geometry"]).distance(area) < 0.01]
pickle.dump(D, open(f"study-{DID}.pkl", "wb"))
print({k: len(v) for k, v in D.items() if isinstance(v, list)}, round(D["area"].area / 1e6, 1), "km2")
