# Draw a generated district (and optionally the real comparison square) at the same scale.
import json, sys, os, pickle, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, box
DID = sys.argv[1]; out = sys.argv[2]; withreal = len(sys.argv) > 3
F = json.load(open(os.environ.get("GEN_FILE", f"web/gen-{DID}.json"))); s = open("web/gidi-data.js").read(); G = json.loads(s[len("window.GIDI="):-1])
poly = Polygon(next(d for d in G["districts"] if d["id"] == DID)["poly"][0])
def panel(ax, title):
    ax.set_title(title, fontsize=11, loc="left"); ax.set_aspect("equal"); ax.axis("off")
n = 2 if withreal else 1
fig, axs = plt.subplots(1, n, figsize=(9 * n, 9)); axs = [axs] if n == 1 else axs
ax = axs[0]
ax.fill(*poly.exterior.xy, fc="#f1eee8", ec="#999", lw=.8)
COL = {"front": "#b9a48a", "back": "#a8977f", "shed": "#8f8577", "kiosk": "#6e8fb0", "warehouse": "#7a7f86", "stalls": "#d08a3a", "school": "#c9a227",
       "terminal": "#5d7fa3", "station": "#8a5d9e", "stands": "#9a8f80", "hotel": "#b0473a",
       "print": "#7d5ba6", "transformer": "#e0b000", "flats": "#c27c5a", "studio": "#7d5ba6", "cafe": "#2b6cb0",
       "stage": "#b0473a", "checkpoint": "#d93025", "stilt": "#8a6a4f", "stilt bar": "#b0473a", "raft": "#a0784a",
       "saw shed": "#7a7f86", "canopy": "#8430ce", "phone mall": "#5d7fa3", "strip": "#b0473a", "hall": "#7d5ba6", "office": "#8c96a3", "barracks": "#7c8a5a", "bust": "#333333", "plaza": "#9a8f80", "unfinished": "#b5b5b5", "pen": "#8f8577", "scrap": "#6b4f3a", "container": "#3b78b8", "crane": "#d9822b", "stack": "#4f8fc0", "tank": "#c8ccd2", "villa": "#c9b99a", "cellblock": "#7a7f86", "tower": "#555555", "trailer": "#9aa0a6", "works": "#b05a3c", "mound": "#9c8a6a", "bakery": "#d9a85b", "sawdust": "#d9c39a",
       "gatehouse": "#d93025", "generator": "#55595e", "water tank": "#2b6cb0", "mansion": "#a0784a", "clubhouse": "#7d5ba6", "palace": "#c9a227", "bank tower": "#5f8fb8", "brazilian house": "#c4704a",
       "apartment tower": "#4f7fa8", "nightclub": "#b0457a", "toll booth": "#d93025",
       "office block": "#8a9bb0", "beach shack": "#c9a46a", "beach bar": "#e07b39", "horse shelter": "#8a6a4f",
       "column": "#6b7a8a", "flare stack": "#d93025", "unfinished house": "#9a9a9a", "toll canopy": "#c8645a"}
PC = {"market": "#f6d7b0", "industrial": "#dcdcdc", "school": "#f3e7a8", "pitch": "#bfe3b4", "motor park": "#d6dbe8",
      "bus terminal": "#d6dbe8", "station": "#e6d8ef", "stadium": "#e3e8d6", "under bridge": "#f6d7b0", "estate": "#e4ecd9",
      "lorry park": "#d6dbe8", "park": "#cfe8c4", "sawmill": "#e8dcc8", "government": "#e6e1d3", "garden": "#cfe8c4", "barracks": "#dfe3d0", "airfield": "#d9e8c8", "plazas": "#dcdcdc", "livestock": "#ead9c0", "container yard": "#dcdcdc", "tank farm": "#e4e4e4", "villas": "#dfe8d0", "prison": "#d6d6d6", "truck park": "#d6dbe8", "waterworks": "#dcdcdc", "landfill": "#e6d6bd", "pipeline": "#e3ead8",
      "compound": "#e4ecd9", "club": "#e4ecd9", "pool": "#8fd0ea", "court": "#c9884f", "palace": "#efe3b8", "forecourt": "#e2d6a8", "square": "#d9ead0", "fountain": "#8fd0ea", "enclave": "#efe3c2", "golf course": "#9fd18b", "green": "#c3ebb0", "bunker": "#efe0b0", "pond": "#8fd0ea", "refinery": "#d9d4c7"}
for p in F["parcels"]: ax.fill(*zip(*p["pts"]), fc=PC[p["kind"]], ec="none")
for b in F["buildings"]: ax.fill(*zip(*b[1:]), fc=COL[b[0]], ec="none", lw=0)
for l in F["streets"]: ax.plot(*zip(*l), c="#ffffff", lw=2.2, solid_capstyle="round"); ax.plot(*zip(*l), c="#9aa0a6", lw=.4)
for l in F.get("walls", []): ax.plot(*zip(*l), c="#6b5a48", lw=0.45, zorder=3)   # compound walls
for q in F.get("gates", []): ax.plot(*zip(*q["pts"]), c="#d93025", lw=2.4 if q["main"] else 1.6, zorder=7)   # estate gates
for p in F.get("paths", []): ax.plot(*zip(*p["pts"]), c="#a88a63", lw=0.9, ls=(0, (2, 1)), zorder=4)
for l in F.get("lanes", []): ax.plot(*zip(*l), c="#ffffff", lw=1.2); ax.plot(*zip(*l), c="#b0b4b8", lw=.3, ls=(0,(2,1)))
for m in F["mains"]: ax.plot(*zip(*m["pts"]), c="#f5c542", lw=3.6, solid_capstyle="round")
for a in G["arterials"]:
    g = LineString(a["pts"]).intersection(poly.buffer(200))
    for p in getattr(g, "geoms", [g]):
        if p.geom_type == "LineString": ax.plot(*p.xy, c="#e8710a", lw=6)
r = LineString(G["rail"]["pts"]).intersection(poly.buffer(200))
for p in getattr(r, "geoms", [r]): ax.plot(*p.xy, c="#555", lw=1.6, ls=(0, (4, 2)))
if F.get("canal"): ax.plot(*zip(*F["canal"]), c="#4aa3c7", lw=2.5)
for st in F.get("structures", []):   # flyovers and bridges on top, slip roads, skywalks
    if st["kind"] == "ramp": ax.plot(*zip(*st["pts"]), c="#f5c542", lw=3.0, solid_capstyle="round")
    elif st["kind"] in ("skywalk", "footbridge", "jetty"): ax.plot(*zip(*st["pts"]), c="#2b6cb0", lw=2.4, zorder=6)
    else:
        ax.plot(*zip(*st["pts"]), c="#333", lw=9 + 2 * st["layer"], solid_capstyle="butt", zorder=5)
        ax.plot(*zip(*st["pts"]), c="#bdbdbd" if st["layer"] == 1 else "#e0e0e0", lw=7 + 2 * st["layer"], solid_capstyle="butt", zorder=5)
x0, y0, x1, y1 = [float(v) for v in os.environ["ZOOM"].split(",")] if os.environ.get("ZOOM") else poly.bounds   # ZOOM=x0,y0,x1,y1 for a close-up
ax.set_xlim(x0 - 60, x1 + 60); ax.set_ylim(y1 + 60, y0 - 60)
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
    insp = next(d for d in G["districts"] if d["id"] == DID).get("inspired", "the inspiration area")
    panel(ax, f"Real reference: a dense 1 km square of {insp} (OSM) — for checking only, not used as geometry")
plt.tight_layout(); plt.savefig(out, dpi=110, facecolor="white")
