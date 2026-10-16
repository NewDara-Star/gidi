# Generate a 3D district model (Apple Maps style) from the Gidi map data.
# Output: local metres, centred on the district; x east, z south (three.js), y up.
import json, math, random, sys
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union
from shapely.affinity import rotate, translate
from shapely.strtree import STRtree

DID = sys.argv[1] if len(sys.argv) > 1 else "maze"
s = open("web/gidi-data.js").read(); G = json.loads(s[len("window.GIDI="):-1])
D = {d["id"]: d for d in G["districts"]}[DID]
poly = Polygon(D["poly"][0])
water = Polygon(G["water"][0])
cx, cy = poly.centroid.x, poly.centroid.y
rnd = random.Random(44)

# Per-district style. Storeys are probabilities for 1..5 floors.
STYLE = {
 "maze": dict(street_w=5.5, main_w=10, front=(7, 12), depth=(10, 17), gap=0.6, setback=1.8,
              storeys=[.22, .36, .28, .11, .03], unfinished=.1, tin=.6, trees=.03, max_trees=6,
              walls=["#c9bba0", "#c8a98e", "#a9b4b8", "#b9b29b", "#c4b39a", "#b5ab98", "#a8a49c", "#c7b48c", "#9fa79a"],
              roofs_tin=["#8a4f36", "#7d4a35", "#965a3b", "#6e5546", "#8f8a82", "#7b3f2c"], roof_flat="#a9a49b"),
}[DID]

def L(p):  # world -> local
    return [round(p[0] - cx, 1), round(p[1] - cy, 1)]

area = poly.buffer(260)  # include surroundings
# ---- roads ----
streets = []
for k, lines in G["streets"].items():
    for ln in lines:
        g = LineString(ln)
        if g.intersects(area):
            g = g.intersection(area)
            for part in getattr(g, "geoms", [g]):
                if part.length > 4:
                    streets.append({"pts": [L(c) for c in part.coords], "w": STYLE["street_w"], "kind": "lane", "inside": k == DID})
mains = []
for m in G["mains"]:
    g = LineString(m["pts"])
    if g.intersects(area):
        g = g.intersection(area)
        for part in getattr(g, "geoms", [g]):
            mains.append({"pts": [L(c) for c in part.coords], "w": STYLE["main_w"], "kind": "main", "name": m["name"], "inside": m["d"] == DID})
arts = []
for a in G["arterials"]:
    g = LineString(a["pts"])
    if g.intersects(area.buffer(400)):
        arts.append({"pts": [L(c) for c in g.coords], "w": 22 if a["cls"] != "exp" else 28, "kind": a["cls"], "name": a["name"]})
rail = LineString(G["rail"]["pts"])
rail_l = [L(c) for c in rail.intersection(area.buffer(400)).coords] if rail.intersects(area.buffer(400)) else []

# Ring Road becomes a flyover over this district (the 'buka under a flyover').
flyover = None
for a in arts:
    if a["name"] == "Ring Road":
        a["elev"] = 7.5; flyover = a

# ---- canal (Gang Canal) ----
pois = [p for p in G["pois"] if p["d"] == DID]
gc = next(p for p in pois if p["name"] == "Gang Canal")
ang = math.radians(62)
c0 = Point(gc["x"], gc["y"])
canal = LineString([(c0.x - 900 * math.cos(ang), c0.y - 900 * math.sin(ang)), (c0.x + 900 * math.cos(ang), c0.y + 900 * math.sin(ang))]).intersection(poly.buffer(-5))
canal_w = 9
canal = translate(canal, -cx, -cy)  # to local coordinates
canal_poly = canal.buffer(canal_w / 2, cap_style=2)

# ---- road footprint for collision ----
road_geoms = [LineString(st["pts"]).buffer(st["w"] / 2 + 1.0) for st in streets + mains] + \
             [LineString(a["pts"]).buffer(a["w"] / 2 + 2) for a in arts if "elev" not in a]
if rail_l: road_geoms.append(LineString(rail_l).buffer(7))
blocked = unary_union(road_geoms + [canal_poly.buffer(2)])
land_local = translate(poly, -cx, -cy).difference(translate(water, -cx, -cy))
free = land_local.difference(blocked).buffer(-0.3)

# reserved zones for landmarks (no ordinary houses)
P = {p["name"]: (p["x"] - cx, p["y"] - cy) for p in pois}
reserve = {
 "Ladi Lane Parts Market": Point(P["Ladi Lane Parts Market"]).buffer(55),
 "Gari Yard": Point(P["Gari Yard"]).buffer(35),
 "The steal": Point(P["The steal"]).buffer(22),
}
reserved = unary_union(list(reserve.values()))

def pick_storeys():
    r = rnd.random(); acc = 0
    for i, p in enumerate(STYLE["storeys"]):
        acc += p
        if r < acc: return i + 1
    return 2

lots = []; placed = []
tree_idx = None
def ok(rect):
    if not free.contains(rect): return False
    if rect.intersects(reserved): return False
    for o in placed[-400:]:
        if o.intersects(rect): return False
    return True

all_ways = [st for st in streets + mains if st["inside"]]
rnd.shuffle(all_ways)
for st in all_ways:
    ln = LineString([(p[0], p[1]) for p in st["pts"]])
    coords = list(ln.coords)
    for (x0, y0), (x1, y1) in zip(coords, coords[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        if seg < 6: continue
        ux, uy = (x1 - x0) / seg, (y1 - y0) / seg
        nx, ny = -uy, ux
        for side in (1, -1):
            t = rnd.uniform(0, 3)
            while t < seg - 4:
                fw = rnd.uniform(*STYLE["front"]); dp = rnd.uniform(*STYLE["depth"])
                off = st["w"] / 2 + STYLE["setback"] + dp / 2
                mx = x0 + ux * (t + fw / 2) + nx * off * side
                my = y0 + uy * (t + fw / 2) + ny * off * side
                a = math.atan2(uy, ux)
                rect = rotate(box(-fw / 2, -dp / 2, fw / 2, dp / 2), a, use_radians=True)
                rect = translate(rect, mx, my)
                if ok(rect):
                    placed.append(rect)
                    stor = pick_storeys()
                    unfinished = rnd.random() < STYLE["unfinished"]
                    tin = (stor <= 2 and rnd.random() < STYLE["tin"]) and not unfinished
                    lots.append({"x": round(mx, 1), "y": round(my, 1), "w": round(fw - STYLE["gap"], 1), "d": round(dp, 1), "a": round(a, 3),
                                 "h": round(stor * 3.1 + (0.4 if not tin else 0), 1), "s": stor,
                                 "roof": "tin" if tin else ("open" if unfinished else "flat"),
                                 "c": "#c8c5bf" if unfinished else rnd.choice(STYLE["walls"]),
                                 "rc": rnd.choice(STYLE["roofs_tin"]) if tin else STYLE["roof_flat"],
                                 "tank": (not tin and not unfinished and stor >= 2 and rnd.random() < .45)})
                t += fw + rnd.uniform(0, 1.2)

# second row: fill block interiors with back houses (face-me-I-face-you compounds)
minx, miny, maxx, maxy = free.bounds
for i in range(9000):
    x, y = rnd.uniform(minx, maxx), rnd.uniform(miny, maxy)
    fw, dp = rnd.uniform(8, 14), rnd.uniform(14, 24)
    a = rnd.uniform(0, math.pi)
    rect = translate(rotate(box(-fw / 2, -dp / 2, fw / 2, dp / 2), a, use_radians=True), x, y)
    if ok(rect):
        placed.append(rect)
        stor = 1 if rnd.random() < .7 else 2
        lots.append({"x": round(x, 1), "y": round(y, 1), "w": round(fw, 1), "d": round(dp, 1), "a": round(a, 3), "h": round(stor * 3.1, 1), "s": stor,
                     "roof": "tin", "c": rnd.choice(STYLE["walls"]), "rc": rnd.choice(STYLE["roofs_tin"]), "tank": False, "compound": True})

# trees in leftover space
trees = []
for i in range(4000):
    x, y = rnd.uniform(minx, maxx), rnd.uniform(miny, maxy)
    pt = Point(x, y)
    if free.contains(pt.buffer(3)) and not any(r.contains(pt) for r in placed[-60:]) and rnd.random() < 0.5:
        if all(not r.buffer(1.5).contains(pt) for r in placed if r.distance(pt) < 4):
            trees.append([round(x, 1), round(y, 1), round(rnd.uniform(3, 6.5), 1)])
    if len(trees) >= STYLE.get("max_trees", 140): break

# landmarks (procedural props placed at POIs)
def around(name, n, r, fn):
    px, py = P[name]; out = []
    for i in range(n):
        out.append(fn(px, py, i))
    return out
stalls = []
mx, my = P["Ladi Lane Parts Market"]
for row in range(-4, 5):
    for col in range(-5, 6):
        x = mx + col * 9 + (row % 2) * 2; y = my + row * 10
        if Point(x, y).distance(Point(mx, my)) < 52 and free.buffer(6).contains(Point(x, y)):
            if rnd.random() < 0.18: continue
            stalls.append({"x": round(x + rnd.uniform(-1.5, 1.5), 1), "y": round(y + rnd.uniform(-1.5, 1.5), 1), "a": round(rnd.uniform(-0.12, 0.12), 3), "w": round(rnd.uniform(5, 7.5), 1), "d": round(rnd.uniform(3.5, 5), 1), "c": rnd.choice(["#4f79a8", "#b5574a", "#c99a45", "#5b8a6a", "#8d8a84", "#8d8a84", "#a8a39a"])})
gx, gy = P["Gari Yard"]
landmarks = {
 "stalls": stalls,
 "warehouse": {"x": round(gx, 1), "y": round(gy, 1), "w": 46, "d": 26, "a": 0.2, "h": 9},
 "foodstall": {"x": round(P["The steal"][0], 1), "y": round(P["The steal"][1], 1)},
 "transformer": {"x": round(P["Transformer 44"][0], 1), "y": round(P["Transformer 44"][1], 1)},
}
canal_l = [[round(c[0], 1), round(c[1], 1)] for c in canal.coords] if not canal.is_empty else []
out = {"id": DID, "name": D["name"], "inspired": D["inspired"], "blurb": D["blurb"], "model": D["model"], "oja": D["oja"],
       "activities": D["activities"], "act": D["act"], "okada": D["okada"], "area": D["area"],
       "outline": [L(c) for c in poly.exterior.coords], "streets": streets, "mains": mains, "arts": arts, "rail": rail_l,
       "canal": {"pts": canal_l, "w": canal_w}, "lots": lots, "trees": trees, "landmarks": landmarks,
       "pois": [{**{k: v for k, v in p.items() if k not in ("x", "y", "d")}, "x": round(p["x"] - cx, 1), "y": round(p["y"] - cy, 1)} for p in pois],
       "water": [L(c) for c in water.exterior.coords]}
txt = json.dumps(out, separators=(",", ":"))
open(f"web/{DID}3d.js", "w").write(f"window.DISTRICT={txt};")
print(len(txt) // 1024, "KB", len(lots), "buildings", sum(1 for l in lots if l.get("compound")), "back-row", len(trees), "trees", len(stalls), "stalls")
