# Draw a generated district (and optionally the real comparison square) at the same scale.
import json, sys, pickle, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, box
DID = sys.argv[1]; out = sys.argv[2]; withreal = len(sys.argv) > 3
F = json.load(open(f"web/gen-{DID}.json")); s = open("web/gidi-data.js").read(); G = json.loads(s[len("window.GIDI="):-1])
poly = Polygon(next(d for d in G["districts"] if d["id"] == DID)["poly"][0])
def panel(ax, title):
    ax.set_title(title, fontsize=11, loc="left"); ax.set_aspect("equal"); ax.axis("off")
n = 2 if withreal else 1
fig, axs = plt.subplots(1, n, figsize=(9 * n, 9)); axs = [axs] if n == 1 else axs
ax = axs[0]
ax.fill(*poly.exterior.xy, fc="#f1eee8", ec="#999", lw=.8)
COL = {"front": "#b9a48a", "back": "#a8977f", "shed": "#8f8577", "kiosk": "#6e8fb0", "warehouse": "#7a7f86", "stalls": "#d08a3a", "school": "#c9a227"}
PC = {"market": "#f6d7b0", "industrial": "#dcdcdc", "school": "#f3e7a8", "pitch": "#bfe3b4", "motor park": "#d6dbe8"}
for p in F["parcels"]: ax.fill(*zip(*p["pts"]), fc=PC[p["kind"]], ec="none")
for b in F["buildings"]: ax.fill(*zip(*b[1:]), fc=COL[b[0]], ec="none", lw=0)
for l in F["streets"]: ax.plot(*zip(*l), c="#ffffff", lw=2.2, solid_capstyle="round"); ax.plot(*zip(*l), c="#9aa0a6", lw=.4)
for l in F.get("lanes", []): ax.plot(*zip(*l), c="#ffffff", lw=1.2); ax.plot(*zip(*l), c="#b0b4b8", lw=.3, ls=(0,(2,1)))
for m in F["mains"]: ax.plot(*zip(*m["pts"]), c="#f5c542", lw=3.6, solid_capstyle="round")
for a in G["arterials"]:
    g = LineString(a["pts"]).intersection(poly.buffer(200))
    for p in getattr(g, "geoms", [g]):
        if p.geom_type == "LineString": ax.plot(*p.xy, c="#e8710a", lw=6)
r = LineString(G["rail"]["pts"]).intersection(poly.buffer(200))
for p in getattr(r, "geoms", [r]): ax.plot(*p.xy, c="#555", lw=1.6, ls=(0, (4, 2)))
if F.get("canal"): ax.plot(*zip(*F["canal"]), c="#4aa3c7", lw=2.5)
x0, y0, x1, y1 = poly.bounds; ax.set_xlim(x0 - 60, x1 + 60); ax.set_ylim(y1 + 60, y0 - 60)
ax.plot([x0, x0 + 200], [y1 + 40, y1 + 40], c="k", lw=2); ax.text(x0, y1 + 55, "200 m", fontsize=9)
panel(ax, f"Gidi · {DID} (generated)")
if withreal:
    D = pickle.load(open(f"study-{DID}.pkl", "rb")); C = json.load(open(f"study-{DID}-core.json"))["dense"]["bounds"]
    b = box(*C); ax = axs[1]
    for t, g in D["buildings"]:
        if g.intersects(b):
            gg = g.intersection(b)
            for q in getattr(gg, "geoms", [gg]):
                if q.geom_type == "Polygon": ax.fill(*q.exterior.xy, fc="#b9a48a", ec="none")
    for t, g in D["roads"]:
        h = t.get("highway", "").replace("_link", "")
        if g.intersects(b):
            gg = g.intersection(b)
            for q in getattr(gg, "geoms", [gg]):
                if q.geom_type != "LineString": continue
                if h in ("motorway", "trunk", "primary", "secondary", "tertiary"): ax.plot(*q.xy, c="#f5c542", lw=3.6)
                elif h in ("residential", "unclassified", "living_street"): ax.plot(*q.xy, c="#fff", lw=2.2); ax.plot(*q.xy, c="#9aa0a6", lw=.4)
    ax.set_xlim(C[0] - 60, C[2] + 60); ax.set_ylim(C[1] - 60, C[3] + 60)
    ax.plot([C[0], C[0] + 200], [C[1] - 40, C[1] - 40], c="k", lw=2)
    panel(ax, "Real reference: a dense 1 km square of Mushin/Shomolu (OSM) — for checking only, not used as geometry")
plt.tight_layout(); plt.savefig(out, dpi=110, facecolor="white")
