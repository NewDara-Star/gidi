# Cut Lagos land into places bounded by real borders, on the 50 m grid.
# Borders: big roads (motorway, trunk, primary), rail, narrow water (canals, creeks), secondary roads, and changes in the built fabric.
# Wide water (lagoon, harbour, wide creeks) is not land: places only face each other across it.
import pickle, json, collections, numpy as np
from scipy import ndimage as nd
from common import *
import gaz
S = pickle.load(open(WORK + 'skel.pkl', 'rb')); segs = S['segs']
OB = np.load(WORK + 'ob50.npz'); WC = np.load(WORK + 'wc50.npz')
F = np.load(LAGOS + 'feat.npz'); K = np.load(LAGOS + 'class.npz')
_l = F['lga'] >= 0
STATE = up(nd.binary_fill_holes(nd.binary_closing(_l, iterations=3)) | _l)

# ---- water: wide water separates; narrow water (under ~300 m across) is a border line like a road
water = (WC['water'] >= 0.5) & STATE
disk = np.hypot(*np.mgrid[-3:4, -3:4]) <= 3
wide = nd.binary_opening(water, structure=disk)
wide = nd.binary_dilation(wide, iterations=1) & water          # keep the shore cells of wide water as water
lab, n = nd.label(wide); sz = nd.sum(np.ones_like(lab), lab, range(1, n + 1))
wide = np.isin(lab, 1 + np.nonzero(sz >= 200)[0])              # a pond under 0.5 km2 is a hole in the land, not a divide
narrow = water & ~wide
land = STATE & ~wide

# ---- barrier lines: 1 motorway/trunk, 2 primary, 3 rail, 4 narrow water, 5 secondary  (lower = stronger)
BT = np.zeros((NY, NX), np.int8); BN = np.full((NY, NX), -1, np.int32); names = []
nid = {}
RANK = {'motorway': 1, 'trunk': 1, 'primary': 2, 'rail': 3, 'secondary': 5}
for s in sorted(segs, key=lambda s: -RANK.get(s['cls'], 9)):      # stronger roads drawn last, so they win a shared cell
    if s['link'] or s['cls'] not in RANK: continue
    xy = s['xy'].astype(float); d = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
    if d[-1] < 1: continue
    t = np.arange(0, d[-1] + 5, 5.0); x = np.interp(t, d, xy[:, 0]); y = np.interp(t, d, xy[:, 1])
    i, j = ij(x, y); ok = (i >= 0) & (i < NY) & (j >= 0) & (j < NX); i, j = i[ok], j[ok]
    k = nid.setdefault(s['name'] or '(unnamed %s)' % s['cls'], len(nid))
    BT[i, j] = RANK[s['cls']]; BN[i, j] = k
names = [None] * len(nid)
for k, v in nid.items(): names[v] = k
BT[narrow & ((BT == 0) | (BT == 5))] = 4
BT[~land] = 0
hard = (BT >= 1) & (BT <= 4); soft = BT == 5

# ---- fabric: the earlier study's 17 character classes (250 m, smoothed into zones), grouped
FAB = {1: 'airport', 2: 'barracks', 3: 'campus', 4: 'port & tank farm', 5: 'industry', 6: 'open', 7: 'open', 8: 'thin new build',
       9: 'waterfront', 10: 'towers', 11: 'estate & villa', 12: 'planned grid', 13: 'dense core', 14: 'dense core',
       15: 'bungalow suburb', 16: 'dense sprawl'}
FG = sorted(set(FAB.values()))
z = K['z'].copy(); idx = nd.distance_transform_edt(z < 1, return_distances=False, return_indices=True); z = z[idx[0], idx[1]]
fab = up(np.vectorize(lambda c: FG.index(FAB.get(int(c), 'open')))(z)).astype(np.int8)

# ---- atoms: connected pieces of (land minus border lines) with one fabric; 4-connected
free = land & ~hard & ~soft
atom = np.zeros((NY, NX), np.int32); na = 0
for f in range(len(FG)):
    l, m = nd.label(free & (fab == f)); atom[l > 0] = l[l > 0] + na; na += m
# border-line cells (and anything left) join the nearest atom
idx = nd.distance_transform_edt(atom == 0, return_distances=False, return_indices=True)
atom = np.where(land, atom[idx[0], idx[1]], 0)
print('atoms', na)

# ---- atom graph: edges between 4-neighbour cells, typed by the strongest border line on either cell
def edges(lab):
    out = collections.Counter()
    for a, b, ta, tb in ((lab[:, 1:], lab[:, :-1], BT[:, 1:], BT[:, :-1]), (lab[1:, :], lab[:-1, :], BT[1:, :], BT[:-1, :])):
        m = (a != b) & (a > 0) & (b > 0)
        t = np.where((ta[m] > 0) & ((tb[m] == 0) | (ta[m] < tb[m])), ta[m], tb[m])
        A, B = np.minimum(a[m], b[m]), np.maximum(a[m], b[m])
        key = (A.astype(np.int64) * 10 + t) * 4000000 + B
        u, c = np.unique(key, return_counts=True)
        for k, cc in zip(u, c):
            out[(int(k // 4000000 // 10), int(k % 4000000), int(k // 4000000 % 10))] += int(cc)
    return out
cells = np.bincount(atom.ravel(), minlength=na + 1)
G = gaz.load(); gx, gy = T.transform([g[2] for g in G], [g[1] for g in G]); gi, gj = ij(gx, gy)
anchor = collections.defaultdict(list)
for k, (nm, la, lo) in enumerate(G):
    if 0 <= gi[k] < NY and 0 <= gj[k] < NX:
        a = atom[gi[k], gj[k]]
        if a == 0:   # a point on water: take the nearest land atom
            ii, jj = idx[0][gi[k], gj[k]], idx[1][gi[k], gj[k]]; a = atom[ii, jj]
        if a: anchor[a].append(nm)
fh = np.zeros((na + 1, len(FG))); np.add.at(fh, (atom[land], fab[land]), 1)     # fabric cells per atom
roof = OB['a'].astype(float)

par = np.arange(na + 1)
def find(a):
    r = a
    while par[r] != r: r = par[r]
    while par[a] != r: par[a], a = r, par[a]
    return r
size = cells.astype(float).copy(); names_in = {a: list(v) for a, v in anchor.items()}
def union(a, b):
    a, b = find(a), find(b)
    if a == b: return
    if size[a] < size[b]: a, b = b, a
    par[b] = a; size[a] += size[b]; fh[a] += fh[b]
    names_in[a] = names_in.get(a, []) + names_in.pop(b, [])
E = edges(atom)
def grouped():
    g = collections.Counter()
    for (a, b, t), c in E.items():
        A, B = find(a), find(b)
        if A != B: g[(min(A, B), max(A, B), t)] += c
    return g
# pass 1: slivers. A piece under 0.25 km2 with no name joins the neighbour it shares most border with,
# preferring soft borders (no line, secondary road) over hard ones. Named pieces stay if over 0.1 km2.
for it in range(8):
    g = grouped(); best = {}
    for (a, b, t), c in g.items():
        w = c * (4 if t in (0, 5) else 1)
        for p, q in ((a, b), (b, a)):
            best.setdefault(p, collections.Counter())[q] += w
    ch = 0
    for p in sorted(best, key=lambda p: size[p]):
        if find(p) != p: continue
        small = size[p] < 100 and not (names_in.get(p) and size[p] >= 40)
        if small:
            q = best[p].most_common(1)[0][0]; union(p, q); ch += 1
    print('sliver pass', it, ch)
    if not ch: break
# pass 2: same main fabric across a soft border (no line, or a secondary road), and not two named places: one place.
# Capped at 10 km2 so a big field of one fabric still splits at its secondary roads.
for it in range(8):
    g = grouped(); ch = 0; pairs = collections.Counter()
    for (a, b, t), c in g.items():
        if t in (0, 5): pairs[(a, b)] += c
    for (a, b), c in pairs.most_common():
        A, B = find(a), find(b)
        if A == B or c < 6: continue
        if fh[A].argmax() != fh[B].argmax(): continue
        if names_in.get(A) and names_in.get(B): continue
        if size[A] + size[B] > 4000: continue
        union(A, B); ch += 1
    print('fabric pass', it, ch)
    if not ch: break
# pass 3: an unnamed piece still under 1 km2 joins its most-bordered neighbour across a soft border, if it has one
for it in range(4):
    g = grouped(); best = {}; ch = 0
    for (a, b, t), c in g.items():
        if t not in (0, 5): continue
        for p, q in ((a, b), (b, a)): best.setdefault(p, collections.Counter())[q] += c
    for p in sorted(best, key=lambda p: size[p]):
        if find(p) != p or names_in.get(p) or size[p] >= 400: continue
        union(p, best[p].most_common(1)[0][0]); ch += 1
    print('small unnamed pass', it, ch)
    if not ch: break

# ---- final labels
root = np.array([find(a) for a in range(na + 1)]); root[0] = 0
u, place = np.unique(root[atom], return_inverse=True); place = place.reshape(atom.shape).astype(np.int32)
if u[0] != 0: place += 1
place[~land] = 0
NP = place.max()

# ---- a bordered piece that holds several named neighbourhoods, with no road or fabric line between them, is shared out
# between those names: each cell goes to the name it reaches most cheaply, where crossing a tertiary street costs 4 cells.
import heapq, pyarrow.parquet as pq, shapely
from shapely import wkb
TER = np.zeros((NY, NX), bool)
for b in pq.ParquetFile(DATA + 'overture-lagos/lagos_overture_segment.parquet').iter_batches(batch_size=20000, columns=['class', 'geometry']):
    for cl, g in zip(b.column('class').to_pylist(), b.column('geometry').to_pylist()):
        if cl != 'tertiary': continue
        xy = np.asarray(wkb.loads(g).coords)[:, :2]; x, y = T.transform(xy[:, 0], xy[:, 1]); xy = np.column_stack([x, y])
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]; t = np.arange(0, d[-1] + 5, 5.0)
        i, j = ij(np.interp(t, d, xy[:, 0]), np.interp(t, d, xy[:, 1])); ok = (i >= 0) & (i < NY) & (j >= 0) & (j < NX); TER[i[ok], j[ok]] = True
pts = collections.defaultdict(list)
for k in range(len(G)):
    if 0 <= gi[k] < NY and 0 <= gj[k] < NX and place[gi[k], gj[k]]: pts[place[gi[k], gj[k]]].append(k)
nxt = NP + 1; nsplit = 0
for p, ks in pts.items():
    if len(ks) < 2: continue
    ii, jj = np.nonzero(place == p)
    if len(ii) < 2 * 400: continue                               # under 2 km2: one place with a double name
    i0, j0 = ii.min(), jj.min(); sub = place[i0:ii.max() + 1, j0:jj.max() + 1] == p; ter = TER[i0:ii.max() + 1, j0:jj.max() + 1]
    dist = np.full(sub.shape, np.inf); lab = np.full(sub.shape, -1); h = []
    for q, k in enumerate(ks):
        a, b = gi[k] - i0, gj[k] - j0; dist[a, b] = 0; lab[a, b] = q; heapq.heappush(h, (0.0, a, b, q))
    while h:
        d, a, b, q = heapq.heappop(h)
        if d > dist[a, b]: continue
        for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = a + da, b + db
            if 0 <= x < sub.shape[0] and 0 <= y < sub.shape[1] and sub[x, y]:
                nd_ = d + (5.0 if ter[x, y] else 1.0)
                if nd_ < dist[x, y]: dist[x, y] = nd_; lab[x, y] = q; heapq.heappush(h, (nd_, x, y, q))
    view = place[i0:ii.max() + 1, j0:jj.max() + 1]
    for q in range(1, len(ks)):
        view[sub & (lab == q)] = nxt; nxt += 1
    nsplit += 1
print('split', nsplit, 'multi-name pieces into', nxt - NP - 1 + nsplit)
NP = place.max()
pc = np.bincount(place.ravel(), minlength=NP + 1)
proof = np.bincount(place.ravel(), weights=roof.ravel(), minlength=NP + 1)
pfab = np.zeros((NP + 1, len(FG))); np.add.at(pfab, (place[land], fab[land]), 1)
# ---- names: the [K] neighbourhood points inside; else the nearest point plus a compass word
ii, jj = np.nonzero(land); cnt = np.bincount(place[land], minlength=NP + 1)
cx = np.bincount(place[land], weights=jj, minlength=NP + 1) / np.maximum(cnt, 1); cy = np.bincount(place[land], weights=ii, minlength=NP + 1) / np.maximum(cnt, 1)
inside = collections.defaultdict(list)
for k, (nm, la, lo) in enumerate(G):
    if 0 <= gi[k] < NY and 0 <= gj[k] < NX:
        p = place[gi[k], gj[k]]
        if p == 0:
            d = nd.distance_transform_edt(place == 0, return_distances=False, return_indices=True) if 'D_' not in globals() else D_
            globals()['D_'] = d; p = place[d[0][gi[k], gj[k]], d[1][gi[k], gj[k]]]
        inside[p].append(k)
def compass(dx, dy):
    a = np.degrees(np.arctan2(dy, dx)) % 360
    return ['east', 'north-east', 'north', 'north-west', 'west', 'south-west', 'south', 'south-east'][int(((a + 22.5) % 360) // 45)]
P = []
for p in range(1, NP + 1):
    land_km2 = pc[p] * C * C / 1e6; built = proof[p] / 1e6
    ks = inside.get(p, [])
    if ks:
        # order the names by how near each point is to the place's centre
        ks = sorted(ks, key=lambda k: (gj[k] - cx[p]) ** 2 + (gi[k] - cy[p]) ** 2)
        nm = '-'.join(G[k][0] for k in ks[:3]) + (' (+%d)' % (len(ks) - 3) if len(ks) > 3 else ''); named = True
    else:
        k = int(np.argmin((gj - cx[p]) ** 2 + (gi - cy[p]) ** 2))
        nm = None; named = False; near = (G[k][0], compass(cx[p] - gj[k], cy[p] - gi[k]))
    x, y = X0 + (cx[p] + .5) * C, Y0 + (cy[p] + .5) * C
    P.append(dict(id=p, name=nm, near=None if named else near, gaz=[G[k][0] for k in ks], from_gazetteer=named, land_km2=round(land_km2, 2), roof_km2=round(built, 3),
                  fabric=FG[int(pfab[p].argmax())], fabric_mix={FG[f]: round(pfab[p][f] / pc[p], 2) for f in np.argsort(-pfab[p])[:3] if pfab[p][f] > 0},
                  x=x, y=y, latlon=[round(v, 4) for v in TI.transform(x, y)[::-1]]))
# an unnamed place is named from the named place it shares the longest border with, and the line between them:
# "Ikotun, north of Ikotun-Igando Road". With no named neighbour: the nearest named point and a compass word.
EP = collections.Counter(); RN = collections.defaultdict(collections.Counter)
for a, b, na_, nb_ in ((place[:, 1:], place[:, :-1], BN[:, 1:], BN[:, :-1]), (place[1:, :], place[:-1, :], BN[1:, :], BN[:-1, :])):
    m = (a != b) & (a > 0) & (b > 0)
    for p, q, r1, r2 in zip(a[m], b[m], na_[m], nb_[m]):
        EP[(p, q)] += 1; EP[(q, p)] += 1
        r = r1 if r1 >= 0 else r2
        if r >= 0: RN[(min(p, q), max(p, q))][names[r]] += 1
byid = {q['id']: q for q in P}
for q in P:
    if q['name']: continue
    nb = [(c, o) for (p, o), c in EP.items() if p == q['id'] and byid[o]['from_gazetteer']]
    if nb:
        c, o = max(nb); on = byid[o]; road = RN.get((min(q['id'], o), max(q['id'], o)))
        side = compass(q['x'] - on['x'], q['y'] - on['y'])
        base_ = on['gaz'][0]
        if road and road.most_common(1)[0][1] >= 0.3 * c and not road.most_common(1)[0][0].startswith('(unnamed'):
            q['name'] = '%s, %s of %s' % (base_, side, road.most_common(1)[0][0])
        else:
            q['name'] = '%s %s' % (base_, side)
    else:
        q['name'] = '%s %s' % q['near']
# make names unique
seen = collections.Counter(q['name'] for q in P); dup = collections.Counter()
for q in P:
    if seen[q['name']] > 1:
        dup[q['name']] += 1; q['name'] += ' %d' % dup[q['name']]
np.savez_compressed(WORK + 'places.npz', place=place, BT=BT, BN=BN, fab=fab, land=land, wide=wide, narrow=narrow, STATE=STATE)
json.dump(dict(places=P, road_names=names, FG=FG), open(WORK + 'places.json', 'w'), indent=0)
print('places', NP, 'named from gazetteer', sum(q['from_gazetteer'] for q in P))
for nm in ('Anthony Village', 'Ifako-Gbagada', 'Ijegun', 'Abule Ado', 'Gbagada', 'Maryland'):
    print(nm, '->', [q['name'] + ' %.1f km2' % q['land_km2'] for q in P if nm in q['gaz']])
