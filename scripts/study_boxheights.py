# Height bands for a neighbourhood-level study: data/results/heights.py measures whole LGAs; this measures the part of an LGA inside
# lon/lat boxes, the same way (Google Open Buildings 2.5D, 2023: built pixels with presence >= 0.5, banded by height).
# Where an LGA mixes very different places (Eti Osa: Ikoyi and VI's towers with Lekki's low estates) its bands mislead.
# Usage: python3 scripts/study_boxheights.py "Eti Osa" "w,s,e,n;w,s,e,n"   (needs rasterio and the data folder below)
import json, os, sys
import numpy as np, rasterio
from rasterio.features import rasterize
from rasterio.windows import from_bounds
from shapely.geometry import shape, box
from shapely.ops import unary_union, transform
from pyproj import Transformer
D = os.environ.get("GIDI_DATA", os.path.expanduser("~/Real-world/research/data/"))   # where data/tools/pull-data.sh puts it
lga = sys.argv[1]; boxes = [tuple(map(float, b.split(","))) for b in sys.argv[2].split(";")]
L = json.load(open(D + "lagos_lgas_utm31.geojson"))["features"]
g = next(shape(f["geometry"]) for f in L if f["properties"]["name"] == lga)
area = g.intersection(unary_union([transform(Transformer.from_crs(4326, 32631, always_xy=True).transform, box(*b)) for b in boxes]))
BINS = [0, 4.5, 7.5, 10.5, 13.5, 20, 40, 200]   # storeys 1, 2, 3, 4, 5-6, 7-13, 14+ (about 3 m a storey), as in heights.py
hist = np.zeros(7); hsum = 0.0; nb = 0
OB = D + "open-buildings-2023/"
for t in sorted(f for f in os.listdir(OB) if f.endswith(".tif")):
    r = rasterio.open(OB + t)
    a = transform(Transformer.from_crs(32631, r.crs, always_xy=True).transform, area)
    if not box(*r.bounds).intersects(a): continue
    w = from_bounds(*a.bounds, r.transform).round_offsets().round_lengths()
    cnt, H, P = r.read(window=w, boundless=True, fill_value=0)
    m = rasterize([(a, 1)], out_shape=H.shape, transform=r.window_transform(w), dtype="uint8").astype(bool)
    b = m & (P >= 0.5) & (H > 0); h = H[b]
    hist += np.histogram(h, BINS)[0]; hsum += float(h.sum()); nb += int(b.sum())
print(json.dumps({"lga": lga, "boxes": boxes, "land_km2": round(area.area / 1e6, 2), "mean_h": round(hsum / max(nb, 1), 1),
                  "h_bands": [round(float(100 * x / max(nb, 1)), 2) for x in hist]}))
