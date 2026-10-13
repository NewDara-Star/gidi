# Waterfront studies: split the buildings on the water (stilt villages: more than 60 m from any mapped road) from the land ones.
# Writes study-<id>-village.json (the village rules) and keeps only land buildings in study-<id>.pkl (the original is kept as
# study-<id>-all.pkl), so study_analyse / study_core --land measure the land fabric.  Usage: python3 scripts/study_village.py <id>
import sys, os, pickle, json, numpy as np, warnings; warnings.filterwarnings("ignore")
from shapely.ops import unary_union
from shapely.strtree import STRtree
DID = sys.argv[1]; src = f"study-{DID}-all.pkl" if os.path.exists(f"study-{DID}-all.pkl") else f"study-{DID}.pkl"
D = pickle.load(open(src, "rb")); pickle.dump(D, open(f"study-{DID}-all.pkl", "wb"))
R = unary_union([g for t, g in D["roads"] if t.get("highway")])
land = [(t, g) for t, g in D["buildings"] if g.distance(R) <= 60]; far = [g for t, g in D["buildings"] if g.distance(R) > 60 and g.area > 4]
A = np.array([b.area for b in far]); vil = unary_union([b.buffer(8) for b in far]).buffer(-8)
tr = STRtree(far); gaps = [min(far[j].distance(b) for j in tr.query(b.buffer(10)) if far[j] is not b) for b in far if len(tr.query(b.buffer(10))) > 1]
ch = [g for t, g in D["water"] if t.get("waterway") in ("canal", "river", "stream")]; chv = sum(g.intersection(vil.buffer(20)).length for g in ch)
fb = [g.length for t, g in D["roads"] if t.get("bridge") and t.get("highway") in ("footway", "path")]
def sides(b):
    c = list(b.minimum_rotated_rectangle.exterior.coords); return sorted([np.hypot(c[0][0] - c[1][0], c[0][1] - c[1][1]), np.hypot(c[1][0] - c[2][0], c[1][1] - c[2][1])])
S_ = np.array([sides(b) for b in far]); pc = lambda a, ps: {f"p{p}": round(float(np.percentile(a, p)), 1) for p in ps}
V = {"method": "buildings more than 60 m from any mapped road: the stilt village", "count": len(far), "area_ha": round(vil.area / 1e4, 1),
     "per_km2_of_village": round(len(far) / vil.area * 1e6), "coverage": round(float(A.sum() / vil.area), 2), "footprint_m2": pc(A, (10, 25, 50, 75, 90)),
     "short_side_m": pc(S_[:, 0], (25, 50, 75)), "long_side_m": pc(S_[:, 1], (25, 50, 75)), "gap_m": pc(gaps, (25, 50, 75)),
     "canoe_channels_km_per_km2_of_village": round(chv / 1000 / (vil.area / 1e6), 1), "plank_bridges_m": pc(fb, (25, 50, 75)) if fb else {}}
json.dump(V, open(f"study-{DID}-village.json", "w"), indent=1); print(V)
D["buildings"] = land; pickle.dump(D, open(f"study-{DID}.pkl", "wb")); print("land buildings kept:", len(land))
