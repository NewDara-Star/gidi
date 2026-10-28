import json, sys, math
import pyarrow.parquet as pq, shapely, shapely.ops
from shapely.geometry import Polygon, MultiPolygon, Point, LineString
from pyproj import Transformer
sys.path.insert(0, '/Users/Star/gidi/scripts')
from working_bar import gidi
T = Transformer.from_crs(4326, 32631, always_xy=True)
OV = '/Users/Star/gidi-data/research/data/overture-lagos/'
s = open('/Users/Star/gidi/web/frame-study.js').read(); s = s[s.index('{'):].rstrip().rstrip(';'); F = json.loads(s)
D = {x['n']: x for x in F['districts']}
def fpoly(n): return MultiPolygon([Polygon(p[0], p[1:]) for p in D[n]['rings']]).buffer(0)
def fpts(n): return [tuple(q) for p in D[n]['rings'] for r in p for q in r]
frame30 = fpoly(30)
d15rec = json.load(open('/Users/Star/gidi/map/d15/district.json'))['records'][0]
o15 = MultiPolygon([Polygon(p) for p in d15rec['outline']]).buffer(0)
rest = frame30.difference(o15)
def G(lat, lon): return gidi(lon, lat, T)
def geo_to_game(g):
    return shapely.ops.transform(lambda x, y, z=None: gidi(x, y, T), g)
