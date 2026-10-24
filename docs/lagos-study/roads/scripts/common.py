# Shared paths and the 50 m grid. The 50 m grid nests 5 x 5 inside the earlier study's 250 m grid.
import os, json, numpy as np
from pyproj import Transformer
DATA = '/Users/Star/gidi-data/research/data/'
SCR = os.environ.get('GIDI_SCRATCH', '/private/tmp/claude-501/-Users-Star-gidi/bd25866f-2f1b-4b56-a662-5ab97de6e073/scratchpad/')
LAGOS = SCR + 'lagos/'          # the earlier study's 250 m grids (feat.npz, class.npz, bgrid65.npz, hgrid.npz, rgrid.npz)
WORK = SCR + 'roads/'           # this study's working files
OUT = os.environ.get('ROADS_OUT', os.path.expanduser('~/gidi-worktrees/roads/docs/lagos-study/roads/'))
T = Transformer.from_crs(4326, 32631, always_xy=True)
TI = Transformer.from_crs(32631, 4326, always_xy=True)
X0, Y0 = 466250.0, 702750.0      # same origin as the 250 m grid
C = 50; NX, NY = 3700, 785        # 185 km x 39.25 km
C250 = 250
SCALE = 3                         # Gidi is 1:3
FRAME = (27000, 10500)            # Gidi's frame in metres

def ij(x, y):
    return ((np.asarray(y) - Y0) // C).astype(int), ((np.asarray(x) - X0) // C).astype(int)

def up(a250):
    """250 m grid -> 50 m grid (repeat each cell 5 x 5)."""
    return np.repeat(np.repeat(a250, 5, axis=0), 5, axis=1)

def lga_shapes():
    from shapely.geometry import shape
    g = json.load(open(DATA + 'lagos_lgas_utm31.geojson'))
    return [(f['properties']['name'], shape(f['geometry'])) for f in g['features']]
