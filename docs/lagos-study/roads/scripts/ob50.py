# Open Buildings v3 (confidence >= 0.65) onto the 50 m grid: count and roof area per cell.
# Streams the 430 MB csv.gz in chunks; keeps only two small grids in memory.
import gzip, numpy as np
from common import *
n = np.zeros((NY, NX), np.int32); a = np.zeros((NY, NX), np.float32); big = np.zeros((NY, NX), np.float32)
def flush(L):
    arr = np.array(L, dtype=np.float64); lat, lon, ar, cf = arr.T
    ok = cf >= 0.65
    x, y = T.transform(lon[ok], lat[ok]); ar = ar[ok]
    i, j = ij(x, y); k = (i >= 0) & (i < NY) & (j >= 0) & (j < NX)
    np.add.at(n, (i[k], j[k]), 1); np.add.at(a, (i[k], j[k]), ar[k])
    b = k & (ar >= 1000); np.add.at(big, (i[b], j[b]), ar[b])
L = []; tot = 0
with gzip.open(DATA + 'open-buildings-v3/lagos_open_buildings_v3.csv.gz', 'rt') as fh:
    fh.readline()
    for line in fh:
        p = line.split(',', 4)
        L.append((float(p[0]), float(p[1]), float(p[2]), float(p[3])))
        if len(L) >= 200000:
            flush(L); tot += len(L); L = []
            if tot % 1000000 == 0: print(tot, flush=True)
if L: flush(L); tot += len(L)
np.savez_compressed(WORK + 'ob50.npz', n=n, a=a, big=big)
print('done', tot, int(n.sum()))
