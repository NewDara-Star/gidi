# How much does OSM miss? Google Open Buildings v3 (machine-traced from satellite imagery, CC BY 4.0) against the OSM
# buildings of each district's study area, cell by cell. Only numbers are taken from Google's data: counts, ground covered,
# sizes. No geometry goes into Gidi.
# Cells: 250 m squares inside the study area with at least 300 m of streets (built-up land, not lagoon or bush).
# Google buildings with confidence >= CONF (Google's own advice for precision ~ 0.70+).
# Usage: python3 scripts/study_google.py [ids...]  (study-<id>.pkl in the working directory or GIDI_STUDIES;
#        GIDI_OPEN_BUILDINGS = the Lagos cut of the v3 CSV)   -> docs/data/google-vs-osm.json and a table on stdout
import csv, gzip, json, os, pickle, sys
import numpy as np
from shapely.geometry import box, Point
from shapely.strtree import STRtree
from shapely import contains_xy
from pyproj import Transformer

OB = os.environ.get("GIDI_OPEN_BUILDINGS", os.path.expanduser("~/Real-world/research/data/open-buildings-v3/lagos_open_buildings_v3.csv.gz"))
CONF = 0.70
CELL = 250.0
IDS = sys.argv[1:] or ["maze", "hub", "jungle", "foodgate", "watertown", "capital", "bazaar", "port", "railside", "estate",
                       "oldisland", "heights", "frontier", "border", "oldshore"]
DIRS = [".", os.environ.get("GIDI_STUDIES", "")]
tr = Transformer.from_crs(4326, 32631, always_xy=True).transform
back = Transformer.from_crs(32631, 4326, always_xy=True).transform


def study(did):
    for d in DIRS:
        f = os.path.join(d, f"study-{did}.pkl") if d else None
        if f and os.path.exists(f):
            return pickle.load(open(f, "rb"))
    sys.exit(f"no study-{did}.pkl")


S = {d: study(d) for d in IDS}
# one pass over Google's file: keep the buildings inside any study area's bounds
bounds = {}
for d, D in S.items():
    x0, y0, x1, y1 = D["area"].bounds
    (w, s), (e, n) = back(x0, y0), back(x1, y1)
    bounds[d] = (w, s, e, n)
G = {d: [] for d in IDS}
with gzip.open(OB, "rt") as fh:
    r = csv.reader(fh)
    next(r)
    for row in r:
        lat, lon, area, conf = float(row[0]), float(row[1]), float(row[2]), float(row[3])
        if conf < CONF:
            continue
        for d, (w, s, e, n) in bounds.items():
            if w <= lon <= e and s <= lat <= n:
                G[d].append((lon, lat, area))

out = {}
print(f"{'district':10} {'cells':>5} | {'OSM /km2':>8} {'Google /km2':>11} {'x':>5} | {'OSM cover':>9} {'Google cover':>12} | {'Google median m2':>16} {'under 40 m2':>11}")
for d, D in S.items():
    A = D["area"]
    if not G[d]:
        continue
    g = np.array(G[d])
    gx, gy = tr(g[:, 0], g[:, 1])
    gx, gy, ga = np.asarray(gx), np.asarray(gy), g[:, 2]
    inside = contains_xy(A, gx, gy)
    gx, gy, ga = gx[inside], gy[inside], ga[inside]
    OSM = [b for t, b in D["buildings"] if b.area > 8]
    ot = STRtree(OSM)
    ox = np.array([b.centroid.x for b in OSM]); oy = np.array([b.centroid.y for b in OSM]); oa = np.array([b.area for b in OSM])
    R = [l for t, l in D["roads"] if t.get("highway") in ("primary", "secondary", "tertiary", "unclassified", "residential", "living_street", "service")]
    rt = STRtree(R)
    x0, y0, x1, y1 = A.bounds
    cells = []
    for x in np.arange(x0, x1, CELL):
        for y in np.arange(y0, y1, CELL):
            b = box(x, y, x + CELL, y + CELL)
            if A.intersection(b).area < 0.9 * CELL * CELL or sum(R[i].intersection(b).length for i in rt.query(b)) < 300:
                continue
            mg = (gx >= x) & (gx < x + CELL) & (gy >= y) & (gy < y + CELL)
            mo = (ox >= x) & (ox < x + CELL) & (oy >= y) & (oy < y + CELL)
            k = CELL * CELL / 1e6
            cells.append((mo.sum() / k, mg.sum() / k, oa[mo].sum() / (CELL * CELL), ga[mg].sum() / (CELL * CELL)))
    c = np.array(cells)
    if not len(c):
        continue
    med = np.median(c, axis=0); p75 = np.percentile(c, 75, axis=0)
    # sizes and the small-structure share from Google's buildings in those built-up cells' area
    small = float((ga < 40).mean()) if len(ga) else 0.0
    out[d] = {"cells": len(c),
              "osm_per_km2": {"median": round(float(med[0])), "dense": round(float(p75[0]))},
              "google_per_km2": {"median": round(float(med[1])), "dense": round(float(p75[1]))},
              "osm_cover": {"median": round(float(med[2]), 3), "dense": round(float(p75[2]), 3)},
              "google_cover": {"median": round(float(med[3]), 3), "dense": round(float(p75[3]), 3)},
              "google_size_m2": {q: round(float(np.percentile(ga, p)), 1) for q, p in (("p10", 10), ("p25", 25), ("median", 50), ("p75", 75), ("p90", 90))},
              "google_under_40m2": round(small, 3),
              "osm_size_m2": {"median": round(float(np.median(oa)), 1) if len(oa) else None},
              "google_buildings": int(len(ga)), "osm_buildings": int(len(oa))}
    o = out[d]
    print(f"{d:10} {len(c):5d} | {o['osm_per_km2']['median']:8d} {o['google_per_km2']['median']:11d} {o['google_per_km2']['median'] / max(1, o['osm_per_km2']['median']):5.1f} | "
          f"{o['osm_cover']['median'] * 100:8.0f}% {o['google_cover']['median'] * 100:11.0f}% | {o['google_size_m2']['median']:16.0f} {small * 100:10.0f}%")
os.makedirs("docs/data", exist_ok=True)
json.dump({"source": "Google Open Buildings v3 (CC BY 4.0), confidence >= %.2f; OSM from the study extracts" % CONF, "cell_m": CELL, "districts": out},
          open("docs/data/google-vs-osm.json", "w"), indent=1)
