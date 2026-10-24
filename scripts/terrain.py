# Gidi's ground: a height grid for the whole map (web/terrain.json), from the land under each district's real inspiration.
# Each district takes the relief of its study area (the 30 m Copernicus surface model, ground estimated as the lowest pixel of
# each ~90 m cell, so roofs and trees mostly drop out), laid onto the district by relative position with north up. The unbuilt
# land between districts is filled smoothly, everything is smoothed so borders don't step, and the land slopes down to the shore.
# Water is 0. Then the hand edits in web/terrain-edits.json are applied on top (Gidi is our city: the data is only a start).
#
# Hand edits: a list of {"name", "type": "ridge" | "valley" | "basin" | "raise", "pts": [[x, y], ...] (metres, Gidi map, y south),
# "width_m", "dz_m"}. ridge/raise add dz_m (positive), valley/basin cut it (give dz_m as a positive depth); along a line for two or
# more points, round a point for one. The brush falls off smoothly (a Gaussian, width_m across).
#
# Usage: python3 scripts/terrain.py  (run from the repo root; needs the study pickles, see STUDY_DIRS, and the DEM tile)
import json, os, pickle, math, sys
import numpy as np, rasterio
from rasterio.windows import from_bounds
from scipy import ndimage
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import transform
from shapely import contains_xy
from pyproj import Transformer

DEM = os.environ.get("GIDI_DEM", os.path.expanduser("~/gidi-data/research/data/dem/Copernicus_DSM_COG_10_N06_00_E003_00_DEM.tif"))
STUDY_DIRS = [".", os.environ.get("GIDI_STUDIES", "")]   # the study pickles are not in the repo (*.pkl is ignored)
CELL = 40
exec(open("scripts/bake_web.py").read().split("# Storeys for any district")[0])   # water, ocean (map polygons)
G = json.loads(open("web/gidi-data.js").read()[len("window.GIDI="):-1])
W_, H_ = G["size"]; nx_, ny_ = int(math.ceil(W_ / CELL)), int(math.ceil(H_ / CELL))
xs = (np.arange(nx_) + 0.5) * CELL; ys = (np.arange(ny_) + 0.5) * CELL; XX, YY = np.meshgrid(xs, ys)
sea = contains_xy(water.union(ocean), XX, YY)
to_ll = Transformer.from_crs(32631, 4326, always_xy=True).transform
dem = rasterio.open(DEM)

def _pkl(did):
    for d in STUDY_DIRS:
        f = os.path.join(d, f"study-{did}.pkl") if d else None
        if f and os.path.exists(f): return pickle.load(open(f, "rb"))["area"]

_FIT = None
def study_area(did):
    """The district's study area (UTM 31N). A district with no study yet (the Airport, Saba) takes the real ground under its own
    outline: the layout placed every district at its inspiration's real position / 4, so a least-squares fit of the anchors to the study
    centroids maps the outline back onto Lagos."""
    a = _pkl(did)
    if a is not None: return a
    global _FIT
    if _FIT is None:
        rows = [(LAYOUT["anchors"][k], _pkl(k).centroid) for k in LAYOUT["anchors"] if _pkl(k) is not None]
        A = np.array([[x, y, 1] for (x, y), c in rows]); _FIT = np.linalg.lstsq(A, np.array([[c.x, c.y] for _, c in rows]), rcond=None)[0]
    from shapely.affinity import affine_transform
    (a_, d_), (b_, e_), (xo, yo) = _FIT
    return affine_transform(Polygon(LAYOUT["districts"][did]), [a_, b_, d_, e_, xo, yo])

def ground(area):
    """The study area's ground on a ~90 m grid (north up), NaN over water and nodata."""
    w, s, e, n = transform(to_ll, area).bounds
    Z = dem.read(1, window=from_bounds(w, s, e, n, dem.transform)).astype(float)
    Z = Z[: Z.shape[0] // 3 * 3, : Z.shape[1] // 3 * 3].reshape(Z.shape[0] // 3, 3, Z.shape[1] // 3, 3).min(axis=(1, 3))   # lowest of 3x3
    Z[Z < 0.3] = np.nan   # the lagoon and the sea read about 0
    return Z

Z = np.full((ny_, nx_), np.nan); real = {}
for dd in G["districts"]:
    P = Polygon(dd["poly"][0]); did = dd["id"]
    g = ground(study_area(did)); real[did] = g[~np.isnan(g)]
    x0, y0, x1, y1 = P.bounds; m = contains_xy(P.buffer(CELL), XX, YY) & ~sea
    u = (XX[m] - x0) / (x1 - x0); v = (YY[m] - y0) / (y1 - y0)   # 0..1 across the district; v down = south, as rows of the DEM
    r = np.clip((v * (g.shape[0] - 1)).round().astype(int), 0, g.shape[0] - 1); c = np.clip((u * (g.shape[1] - 1)).round().astype(int), 0, g.shape[1] - 1)
    Z[m] = g[r, c]
# land the study left blank (its water cells, the unbuilt land between districts): filled from its neighbours, water held at 0
known = ~np.isnan(Z) | sea; Z[sea] = 0.0
dfill, idx = ndimage.distance_transform_edt(~known, return_distances=True, return_indices=True)
near = Z[tuple(idx)]
# away from a district the land settles to a gentle plain that rises inland (north), as Lagos's does from the lagoon: a district's
# hills fade out over a few hundred metres instead of being copied across the empty land
bg = 4.0 + 10.0 * np.clip((4600 - YY) / 4600, 0, 1)
fade = np.exp(-dfill * CELL / 350.0)
Z = np.where(known, Z, bg + (near - bg) * fade)
for _ in range(5):   # smooth so district borders blend and leftover roofs and trees in the surface model wash out (~300 m), water flat
    Z = ndimage.gaussian_filter(Z, sigma=250 / CELL / 2); Z[sea] = 0.0
# down to the shore: land within ~200 m of water eases to about 0.6 m at the water's edge
dist = ndimage.distance_transform_edt(~sea) * CELL
t = np.clip(dist / 200.0, 0, 1); Z = np.where(sea, 0.0, 0.6 * (1 - t) + Z * t)
# hand edits
EDITS = json.load(open("web/terrain-edits.json")) if os.path.exists("web/terrain-edits.json") else []
EDITS = [e for e in EDITS if e.get("layout", "v1") == "v2"]   # edits drawn in the v1 frame wait until their district is rebuilt in v2
for ed in EDITS:
    pts = ed["pts"]; geom = LineString(pts) if len(pts) > 1 else Point(pts[0]); sig = ed["width_m"] / 2
    d = np.vectorize(lambda x, y: geom.distance(Point(x, y)))(XX, YY) if geom.length < 1e9 else 0
    sign = 1 if ed["type"] in ("ridge", "raise") else -1
    Z = Z + sign * ed["dz_m"] * np.exp(-(d / sig) ** 2 / 2)
Z = np.where(sea, 0.0, np.maximum(Z, 0.2))
out = {"source": "Copernicus GLO-30 surface model (ground = lowest pixel per ~90 m cell), each district from its study area, smoothed; plus web/terrain-edits.json",
       "cell_m": CELL, "origin": [0, 0], "w": nx_, "h": ny_, "unit": "decimetres", "z": [int(round(v * 10)) for v in Z.ravel()]}
json.dump(out, open("web/terrain.json", "w"), separators=(",", ":"))
np.save(os.environ.get("GIDI_TERRAIN_NPY", "/tmp/gidi-terrain.npy"), Z)
# per-district comparison with the real study areas
rows = []
for dd in G["districts"]:
    P = Polygon(dd["poly"][0]); m = contains_xy(P, XX, YY) & ~sea; z = Z[m]; r = real[dd["id"]]
    rows.append((dd["id"], dd["name"], np.median(z), np.percentile(z, 10), np.percentile(z, 90), (z < 3).mean() * 100,
                 np.median(r), np.percentile(r, 10), np.percentile(r, 90), (r < 3).mean() * 100))
json.dump([dict(zip(("id", "name", "med", "p10", "p90", "below3", "real_med", "real_p10", "real_p90", "real_below3"), [x if isinstance(x, str) else round(float(x), 1) for x in r])) for r in rows],
          open(os.environ.get("GIDI_TERRAIN_TABLE", "/tmp/gidi-terrain-table.json"), "w"), indent=1)
steps = np.maximum(np.abs(np.diff(np.where(sea, np.nan, Z), axis=0))[~np.isnan(np.diff(np.where(sea, np.nan, Z), axis=0))].max(), 0)
print(f"terrain {nx_}x{ny_} cells of {CELL} m; land {Z[~sea].min():.1f}-{Z[~sea].max():.1f} m; largest step between neighbours {steps:.2f} m; {len(EDITS)} hand edits")
for r in rows: print(f"{r[1]:14} Gidi median {r[2]:5.1f} m (p10-p90 {r[3]:.1f}-{r[4]:.1f}), below 3 m {r[5]:4.0f}%   real median {r[6]:5.1f} (p10-p90 {r[7]:.1f}-{r[8]:.1f}), below 3 m {r[9]:4.0f}%")
