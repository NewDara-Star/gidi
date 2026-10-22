# The skeleton: every motorway, trunk, primary and secondary road (with their links), rail, bridges.
# Overture segments -> skel.pkl (one record per segment, UTM 31N metres) + junction nodes.
import pickle, collections, numpy as np, pyarrow.parquet as pq, shapely
from shapely import wkb
from common import *
# Roads Overture carries that are planned or only partly built (not on the ground in 2026); left out of the skeleton.
PLANNED = ('Fourth Mainland Bridge', 'Fourth Mainland Road', '4MB Link Road', 'Lagoon Highway', '7th Axial Road', 'Third Axial Road',
           'Lagos-Calabar Coastal Highway', 'Omu Creek Road', 'Lekki Regional Road')
MAJOR = ('motorway', 'trunk', 'primary', 'secondary')
def spans(fl, name):
    return [tuple(f.get('between') or [0, 1]) for f in fl or [] if name in (f.get('values') or [])]
def flagspan(fl, name, L):
    """Length of the segment carrying a flag (between = fractions along it)."""
    s = 0.0
    for f in fl or []:
        if name in (f.get('values') or []):
            b = f.get('between') or [0, 1]; s += (b[1] - b[0]) * L
    return s
segs = []
pf = pq.ParquetFile(DATA + 'overture-lagos/lagos_overture_segment.parquet')
for b in pf.iter_batches(batch_size=20000, columns=['id', 'subtype', 'class', 'subclass', 'names', 'road_flags', 'connectors', 'geometry']):
    for r in b.to_pylist():
        st, cl = r['subtype'], r['class']
        if st == 'road' and cl not in MAJOR: continue
        if st not in ('road', 'rail'): continue
        g = shapely.transform(wkb.loads(r['geometry']), lambda a: np.column_stack(T.transform(a[:, 0], a[:, 1])))
        if g.geom_type != 'LineString' or g.length < 1: continue
        nm = (r['names'] or {}).get('primary') or ''
        fl = r['road_flags']; L = g.length
        uc = flagspan(fl, 'is_under_construction', L)
        if st == 'road' and (nm in PLANNED or uc > 0.5 * L): continue
        link = r['subclass'] == 'link' or flagspan(fl, 'is_link', L) > 0.5 * L
        segs.append(dict(id=r['id'], kind=st, cls=cl if st == 'road' else 'rail', link=bool(link), name=nm, L=L,
                         bridge=flagspan(fl, 'is_bridge', L), bspans=spans(fl, 'is_bridge'), tunnel=flagspan(fl, 'is_tunnel', L),
                         xy=np.asarray(g.coords, np.float32)[:, :2],
                         conn=[(c['connector_id'], c['at'] or 0.0) for c in (r['connectors'] or [])]))
# rail from the ferry-and-rail file too (the SGR and the Blue Line), where the segment file lacks it
have = {s['id'] for s in segs}
t = pq.read_table(DATA + 'lagos_overture_ferry_and_rail_segments.parquet', columns=['id', 'subtype', 'class', 'names', 'geometry']).to_pylist()
ferry = []
for r in t:
    g = shapely.transform(wkb.loads(r['geometry']), lambda a: np.column_stack(T.transform(a[:, 0], a[:, 1])))
    if g.geom_type != 'LineString': continue
    nm = (r['names'] or {}).get('primary') or ''
    if r['subtype'] == 'rail' and r['id'] not in have:
        segs.append(dict(id=r['id'], kind='rail', cls='rail', link=False, name=nm, L=g.length, bridge=0.0, bspans=[], tunnel=0.0,
                         xy=np.asarray(g.coords, np.float32)[:, :2], conn=[]))
    elif r['subtype'] == 'water':
        ferry.append(dict(name=nm, L=g.length, xy=np.asarray(g.coords, np.float32)[:, :2]))
# junction nodes on the major road network: a connector shared by 3 or more segment ends/through-points
inc = collections.defaultdict(list); pos = {}
for k, s in enumerate(segs):
    if s['kind'] != 'road': continue
    ln = shapely.LineString(s['xy'])
    for cid, at in s['conn']:
        inc[cid].append(k)
        if cid not in pos:
            p = ln.interpolate(at, normalized=True); pos[cid] = (p.x, p.y)
nodes = []
for cid, ks in inc.items():
    if len(ks) < 3: continue
    names = sorted({segs[k]['name'] for k in ks if segs[k]['name']})
    nodes.append(dict(id=cid, x=pos[cid][0], y=pos[cid][1], deg=len(ks), links=sum(segs[k]['link'] for k in ks),
                      classes=sorted({segs[k]['cls'] for k in ks}), names=names))
pickle.dump(dict(segs=segs, nodes=nodes, ferry=ferry), open(WORK + 'skel.pkl', 'wb'))
c = collections.Counter();
for s in segs: c[(s['cls'], s['link'])] += s['L'] / 1000
for k in sorted(c): print(k, round(c[k], 1), 'km')
print(len(segs), 'segments', len(nodes), 'junction nodes', len(ferry), 'ferry lines')
