# Deep study, step 1 (docs/DEEP-STUDY.md): one pass over the big building files, cut per district, so the 17 district studies can run
# side by side. Reads Google Open Buildings v3 (outlines, confidence) and Microsoft's building outlines for Lagos once, and keeps the
# buildings whose centre lies inside each district's study area (study-<id>.pkl), in metres (UTM 31N).
# Numbers only are taken from these files into Gidi; no outline is ever copied into the map.
# Usage: python3 scripts/deep_prep.py [ids...]      -> $GIDI_DEEP_CACHE/bld-<id>.pkl  (default: ~/gidi-data/research/data/deep-cache)
import csv, gzip, json, os, pickle, sys
import numpy as np
from shapely import wkt
from shapely.geometry import Polygon, shape
from shapely.ops import transform
from shapely.prepared import prep
from pyproj import Transformer

csv.field_size_limit(10 ** 8)
DATA = os.path.expanduser('~/gidi-data/research/data')
CACHE = os.environ.get('GIDI_DEEP_CACHE', os.path.join(DATA, 'deep-cache'))
DIRS = ['.', os.environ.get('GIDI_STUDIES', '')]
IDS = sys.argv[1:] or ['border', 'bazaar', 'jungle', 'port', 'maze', 'hub', 'railside', 'capital', 'estate', 'foodgate', 'watertown',
                       'oldshore', 'oldisland', 'heights', 'frontier', 'airport', 'yaba']
tr = Transformer.from_crs(4326, 32631, always_xy=True).transform
back = Transformer.from_crs(32631, 4326, always_xy=True).transform
os.makedirs(CACHE, exist_ok=True)


def area_of(did):
    for d in DIRS:
        f = os.path.join(d, f'study-{did}.pkl') if d else None
        if f and os.path.exists(f):
            return pickle.load(open(f, 'rb'))['area']
    sys.exit(f'no study-{did}.pkl')


AREAS = {k: area_of(k) for k in IDS}
LL = {k: transform(back, a) for k, a in AREAS.items()}
BB = {k: a.bounds for k, a in LL.items()}
PA = {k: prep(a) for k, a in LL.items()}
W = min(b[0] for b in BB.values()); S = min(b[1] for b in BB.values()); E = max(b[2] for b in BB.values()); N = max(b[3] for b in BB.values())
from shapely.geometry import Point


def owners(lon, lat):
    p = None
    for k, (w, s, e, n) in BB.items():
        if w <= lon <= e and s <= lat <= n:
            p = p or Point(lon, lat)
            if PA[k].contains(p):
                yield k


OUT = {k: {'google': [], 'ms': []} for k in IDS}
n = 0
with gzip.open(os.path.join(DATA, 'open-buildings-v3/lagos_open_buildings_v3.csv.gz'), 'rt') as f:
    for r in csv.DictReader(f):
        n += 1
        lat, lon = float(r['latitude']), float(r['longitude'])
        if not (W <= lon <= E and S <= lat <= N):
            continue
        ks = list(owners(lon, lat))
        if ks:
            g = transform(tr, wkt.loads(r['geometry']))
            for k in ks:
                OUT[k]['google'].append((g, float(r['confidence'])))
print('google rows read', n, {k: len(v['google']) for k, v in OUT.items()}, flush=True)
for fn in sorted(os.listdir(os.path.join(DATA, 'ms-buildings'))):
    with gzip.open(os.path.join(DATA, 'ms-buildings', fn), 'rt') as f:
        for line in f:
            o = json.loads(line)
            c = o['geometry']['coordinates'][0]
            lon, lat = sum(x for x, y in c) / len(c), sum(y for x, y in c) / len(c)
            if not (W <= lon <= E and S <= lat <= N):
                continue
            ks = list(owners(lon, lat))
            if ks:
                g = transform(tr, Polygon(c))
                for k in ks:
                    OUT[k]['ms'].append((g, o['properties'].get('height', -1)))
print('microsoft', {k: len(v['ms']) for k, v in OUT.items()}, flush=True)
for k, v in OUT.items():
    pickle.dump(v, open(os.path.join(CACHE, f'bld-{k}.pkl'), 'wb'))
