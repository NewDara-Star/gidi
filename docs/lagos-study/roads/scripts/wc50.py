# ESA WorldCover (10 m) onto the 50 m grid: share of water (80), wetland (90), mangrove (95), built (50), trees (10).
# Read in strips at ~16 m so memory stays small.
import glob, numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from common import *
KEEP = {'water': 80, 'wet': 90, 'mang': 95, 'built': 50, 'trees': 10, 'grass': 30, 'bare': 60, 'crop': 40}
cnt = {k: np.zeros((NY, NX), np.float32) for k in KEEP}; tot = np.zeros((NY, NX), np.float32)
RES = 0.00015
for p in sorted(glob.glob(DATA + 'worldcover/*.tif')):
    with rasterio.open(p) as src:
        b = src.bounds
        lo0, lo1 = max(b.left, 2.65), min(b.right, 4.40)
        if lo1 <= lo0: continue
        for la1 in np.arange(6.78, 6.33, -0.03):
            la0 = la1 - 0.03
            w = from_bounds(lo0, la0, lo1, la1, transform=src.transform).round_offsets().round_lengths()
            bw = src.window_bounds(w)
            H = max(int((bw[3] - bw[1]) / RES), 1); W = max(int((bw[2] - bw[0]) / RES), 1)
            a = src.read(1, window=w, out_shape=(H, W), resampling=Resampling.nearest)
            lon = bw[0] + (np.arange(W) + .5) * (bw[2] - bw[0]) / W; lat = bw[3] - (np.arange(H) + .5) * (bw[3] - bw[1]) / H
            LO, LA = np.meshgrid(lon, lat); x, y = T.transform(LO.ravel(), LA.ravel())
            i, j = ij(x, y); ok = (i >= 0) & (i < NY) & (j >= 0) & (j < NX) & (a.ravel() > 0)
            i, j, v = i[ok], j[ok], a.ravel()[ok]
            np.add.at(tot, (i, j), 1)
            for k, c in KEEP.items():
                m = v == c; np.add.at(cnt[k], (i[m], j[m]), 1)
        print(p, flush=True)
t = np.maximum(tot, 1)
np.savez_compressed(WORK + 'wc50.npz', seen=tot > 0, **{k: (cnt[k] / t).astype(np.float32) for k in KEEP})
print('done')
