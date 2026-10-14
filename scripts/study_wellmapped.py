# Pattern study, for an area where OSM maps the streets everywhere but the buildings only in some neighbourhoods (the Estate:
# Ikeja GRA is traced, most of Magodo and Omole are not). The street figures in study-<id>-core.json stay as measured.
# The building figures are measured instead on the 250 m cells of one well-mapped box whose buildings cover at least 3% of the
# cell (below that the cell is untraced, not empty): the median cell -> "median", the 75th percentile -> "dense".
# Building sizes come from every building in that box. The measured figures are kept under "osm".
# Usage: python3 scripts/study_wellmapped.py estate 3.341,6.569,3.368,6.592
import json, sys, pickle
import numpy as np
from shapely.geometry import box
from shapely.strtree import STRtree
from pyproj import Transformer
DID = sys.argv[1]; W, S_, E, N = map(float, sys.argv[2].split(","))
tr = Transformer.from_crs(4326, 32631, always_xy=True).transform
D = pickle.load(open(f"study-{DID}.pkl", "rb")); A = D["area"]
B = [g for t, g in D["buildings"] if g.area > 8]; BT = STRtree(B)
R = [g for t, g in D["roads"] if t.get("highway") in ("primary", "secondary", "tertiary", "unclassified", "residential", "living_street")]; RT = STRtree(R)
(x0, y0), (x1, y1) = tr(W, S_), tr(E, N); c = 250.0; cells = []
for x in np.arange(x0, x1, c):
    for y in np.arange(y0, y1, c):
        b = box(x, y, x + c, y + c)
        if A.intersection(b).area < 0.9 * c * c or sum(R[i].intersection(b).length for i in RT.query(b)) < 300: continue
        bs = [B[i] for i in BT.query(b) if B[i].centroid.within(b)]
        cells.append((len(bs) / (c * c) * 1e6, sum(g.area for g in bs) / (c * c)))
cells = np.array(cells); mapped = cells[cells[:, 1] >= 0.03]
gb = box(x0, y0, x1, y1); fp = np.array([g.area for g in B if g.centroid.within(gb)])
pc = lambda q: round(float(np.percentile(fp, q)), 1)
C = json.load(open(f"study-{DID}-core.json"))
out = {"note": f"Buildings under-mapped in most of the area: building figures measured on the {len(mapped)} traced 250 m cells (of {len(cells)}) "
               f"in the box {sys.argv[2]}, median cell -> median, 75th percentile -> dense; sizes from its {len(fp)} buildings. "
               "Street figures as measured. The measured building figures are under 'osm'.", "box": sys.argv[2]}
for k, q in (("median", 50), ("dense", 75)):
    m = dict(C[k]); m["osm"] = {x: C[k][x] for x in ("buildings_per_km2", "coverage", "footprint_m2", "share_under_60m2", "share_over_400m2")}
    m["buildings_per_km2"] = int(round(float(np.percentile(mapped[:, 0], q)))); m["coverage"] = round(float(np.percentile(mapped[:, 1], q)), 3)
    m["footprint_m2"] = {f"p{p}": pc(p) for p in (10, 25, 50, 75, 90)}
    m["share_under_60m2"] = round(float((fp < 60).mean()), 2); m["share_over_400m2"] = round(float((fp > 400).mean()), 2)
    out[k] = m
json.dump(out, open(f"study-{DID}-core.json", "w"), indent=1)
print(json.dumps({k: {x: out[k][x] for x in ("coverage", "buildings_per_km2", "footprint_m2", "gap_m", "drive_km_per_km2", "junctions_per_km2", "dead_end_ratio", "blocks_per_km2_closed")} for k in ("median", "dense")}, indent=1))
