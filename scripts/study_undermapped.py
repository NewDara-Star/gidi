# Pattern study, for an area where OSM has mapped the streets but only a fraction of the buildings (central Ikeja: OSM footprints
# cover 10-14% of land that ESA WorldCover counts as 83% built up). The street figures in study-<id>-core.json stay as measured.
# The building density is estimated instead, from districts whose buildings OSM maps well:
#   their core-square cover / their LGA's WorldCover built-up share  ->  a ratio, applied to this LGA's built-up share.
# Building sizes come from the buildings OSM did map, in the study named last (the whole LGA: in the small box, mappers traced
# the big offices and malls first, so its few buildings run large). The measured figures are kept under "osm".
# Usage: python3 scripts/study_undermapped.py capital Ikeja maze:Mushin,hub:Oshodi/Isolo,jungle:Ajeromi/Ifelodun ikeja
import json, sys, pickle
import numpy as np
DID, LGA, REFS = sys.argv[1], sys.argv[2], [r.split(":") for r in sys.argv[3].split(",")]
SIZES = sys.argv[4] if len(sys.argv) > 4 else DID
T = json.load(open("data/results/lga_table.json"))
ratio = {k: [] for k in ("median", "dense")}
for d, lga in REFS:
    c = json.load(open(f"study-{d}-core.json")); b = T[lga]["cover_pct_of_land"]["built"] / 100
    for k in ratio: ratio[k].append(c[k]["coverage"] / b)
built = T[LGA]["cover_pct_of_land"]["built"] / 100
D = pickle.load(open(f"study-{SIZES}.pkl", "rb")); fp = np.array([g.area for t, g in D["buildings"] if g.area > 8])
mean_fp = float(np.mean(fp[fp < np.percentile(fp, 99)]))   # the few huge sheds and malls would swamp the mean
C = json.load(open(f"study-{DID}-core.json"))
out = {"note": f"Buildings under-mapped in OSM: cover and buildings per km2 estimated as (cover / WorldCover built-up share) of "
               f"{', '.join(d for d, l in REFS)} x {LGA}'s built-up share ({built:.0%}); building sizes from the {len(fp)} mapped buildings of study-{SIZES}. "
               "Street figures as measured. The measured building figures are under 'osm'.",
       "ratio_cover_to_builtup": {k: [round(v, 3) for v in ratio[k]] for k in ratio}, "mean_footprint_m2": round(mean_fp, 1)}
for k in ("median", "dense"):
    m = dict(C[k]); m["osm"] = {x: C[k][x] for x in ("buildings_per_km2", "coverage", "footprint_m2", "gap_m", "front_row_share", "share_under_60m2", "share_over_400m2")}
    cov = float(np.mean(ratio[k])) * built
    m["coverage"] = round(cov, 3); m["buildings_per_km2"] = int(round(cov * 1e6 / mean_fp))
    pc = lambda q: round(float(np.percentile(fp, q)), 1)
    m["footprint_m2"] = {"p10": pc(10), "p25": pc(25), "p50": pc(50), "p75": pc(75), "p90": pc(90)}
    m["share_under_60m2"] = round(float((fp < 60).mean()), 2); m["share_over_400m2"] = round(float((fp > 400).mean()), 2)
    m["gap_m"] = C["dense"]["gap_m"]; m["front_row_share"] = C["dense"]["front_row_share"]   # the dense square is the best-mapped one
    out[k] = m
json.dump(out, open(f"study-{DID}-core.json", "w"), indent=1)
print(json.dumps({k: {x: out[k][x] for x in ("coverage", "buildings_per_km2", "footprint_m2", "gap_m")} for k in ("median", "dense")}, indent=1), out["ratio_cover_to_builtup"], out["mean_footprint_m2"])
