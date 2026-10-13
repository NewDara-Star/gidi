# Pick representative real 1 km squares (median and dense) and measure them with the same yardstick used on Gidi.
import sys, pickle, json, numpy as np, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "scripts"); from fabric_metrics import measure
from shapely.geometry import box
from shapely.strtree import STRtree
DID = sys.argv[1]; D = pickle.load(open(f"study-{DID}.pkl", "rb")); AREA = D["area"]
DR = {"motorway","trunk","primary","secondary","tertiary","unclassified","residential","living_street"}
M = {"motorway":"main","trunk":"main","primary":"main","secondary":"main","tertiary":"main"}
st = [(M.get(t["highway"].replace("_link",""), "street"), g) for t, g in D["roads"] if t.get("highway","").replace("_link","") in DR]
B = [g for t, g in D["buildings"] if g.area > 6]
rt = STRtree([g for c, g in st]); bt = STRtree(B)
minx, miny, maxx, maxy = AREA.bounds; sq = []
for x in np.arange(minx, maxx, 250):
    for y in np.arange(miny, maxy, 250):
        b = box(x, y, x + 1000, y + 1000)
        if AREA.contains(b):
            L = sum(st[k][1].intersection(b).length for k in rt.query(b)) / 1000
            cov = sum(B[k].intersection(b).area for k in bt.query(b)) / 1e6
            sq.append((L, cov, b))
Ls = np.array([s[0] for s in sq]); Cs = np.array([s[1] for s in sq]); out = {}
for name, q in (("median", 50), ("dense", 75)):
    tL, tC = np.percentile(Ls, q), np.percentile(Cs, q)
    s = min(sq, key=lambda s: ((s[0] - tL) / Ls.std()) ** 2 + ((s[1] - tC) / Cs.std()) ** 2)
    b = s[2]
    stb = [(c, st[k][1]) for k in rt.query(b) for c in [st[k][0]]]
    bb = [B[k] for k in bt.query(b) if b.contains(B[k].centroid)]
    out[name] = {"bounds": [round(v) for v in b.bounds], **measure(stb, bb, b)}
json.dump(out, open(f"study-{DID}-core.json", "w"), indent=1); print(json.dumps(out, indent=1))
