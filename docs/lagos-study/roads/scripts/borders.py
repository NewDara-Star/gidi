# Every border between two places: what it is, how long, whether built land meets across it; plus each place's fingerprint
# and the similarity of every pair (the fingerprint method of docs/lagos-study/similar/scripts/analyse.py).
import json, csv, re, pickle, collections, numpy as np, pyarrow.parquet as pq, shapely
from scipy import ndimage as nd
from common import *
Pz = np.load(WORK + 'places.npz'); place = Pz['place']; BT = Pz['BT']; BN = Pz['BN']; fab = Pz['fab']; land = Pz['land']; wide = Pz['wide']
D = json.load(open(WORK + 'places.json')); PL = D['places']; RNAMES = D['road_names']; FG = D['FG']
NP = len(PL); byid = {q['id']: q for q in PL}
OB = np.load(WORK + 'ob50.npz'); WC = np.load(WORK + 'wc50.npz')
cov = OB['a'] / C ** 2
built_s = nd.uniform_filter(cov, 5) >= 0.06                 # built land: >= 6% roof within 250 m
wet = (WC['wet'] + WC['mang']) >= 0.5
EST = FG.index('estate & villa')
KIND = {1: 'big road', 2: 'main road', 3: 'rail', 4: 'canal or creek', 5: 'secondary road'}

# ---------- land borders
rec = collections.defaultdict(lambda: dict(n=0, meet=0, kinds=collections.Counter(), roads=collections.Counter()))
for sl_a, sl_b in (((slice(None), slice(1, None)), (slice(None), slice(None, -1))), ((slice(1, None), slice(None)), (slice(None, -1), slice(None)))):
    a, b = place[sl_a], place[sl_b]; m = (a != b) & (a > 0) & (b > 0)
    ta, tb = BT[sl_a][m], BT[sl_b][m]; t = np.where((ta > 0) & ((tb == 0) | (ta < tb)), ta, tb)
    na_, nb_ = BN[sl_a][m], BN[sl_b][m]; rn = np.where(na_ >= 0, na_, nb_)
    fa, fb = fab[sl_a][m], fab[sl_b][m]; wa, wb = wet[sl_a][m], wet[sl_b][m]; ba, bb = built_s[sl_a][m], built_s[sl_b][m]
    for p, q, tt, r, f1, f2, w1, w2, b1, b2 in zip(a[m], b[m], t, rn, fa, fb, wa, wb, ba, bb):
        if tt: kind = KIND[int(tt)]
        elif w1 or w2: kind = 'swamp'
        elif f1 != f2 and (f1 == EST or f2 == EST): kind = 'estate edge'
        elif f1 != f2: kind = 'fabric change'
        else: kind = 'street (named split)'
        R = rec[(min(p, q), max(p, q))]; R['n'] += 1; R['kinds'][kind] += 1
        if b1 and b2: R['meet'] += 1
        if r >= 0 and tt: R['roads'][RNAMES[r]] += 1

# ---------- across wide water (750 m or less), and bridges
S = pickle.load(open(WORK + 'skel.pkl', 'rb'))['segs']
idx = nd.distance_transform_edt(place == 0, return_distances=False, return_indices=True)
def place_at(x, y):
    i, j = ij(x, y)
    if not (0 <= i < NY and 0 <= j < NX): return 0
    ii, jj = idx[0][i, j], idx[1][i, j]
    return int(place[ii, jj]) if np.hypot(ii - i, jj - j) <= 4 else 0
bridge = collections.defaultdict(set)
for s in S:
    for a0, b0 in s['bspans']:
        if (b0 - a0) * s['L'] < 100: continue
        ln = shapely.LineString(s['xy']); p0 = ln.interpolate(max(a0 - 0.02, 0), normalized=True); p1 = ln.interpolate(min(b0 + 0.02, 1), normalized=True)
        A, B = place_at(p0.x, p0.y), place_at(p1.x, p1.y)
        if A and B and A != B: bridge[(min(A, B), max(A, B))].add(s['name'] or '(unnamed bridge)')
water_pairs = set()
shore = nd.binary_dilation(wide) & (place > 0)
for p in np.unique(place[shore]):
    ii, jj = np.nonzero(place == p); i0, i1, j0, j1 = max(ii.min() - 16, 0), min(ii.max() + 17, NY), max(jj.min() - 16, 0), min(jj.max() + 17, NX)
    sub = place[i0:i1, j0:j1]; w = wide[i0:i1, j0:j1]
    g = nd.binary_dilation(sub == p, iterations=15, mask=(sub == p) | w)          # 15 cells = 750 m across water
    ring = nd.binary_dilation(g) & (sub > 0) & (sub != p)
    for q in np.unique(sub[ring]):
        k = (min(p, q), max(p, q))
        if k not in rec: water_pairs.add(k)
for k in bridge:
    if k not in rec: water_pairs.add(k)

# ---------- fingerprints: 250 m grids weighted by each place's share of every 250 m cell; 50 m grids directly
F = dict(np.load(LAGOS + 'feat.npz')); K = dict(np.load(LAGOS + 'class.npz')); B = dict(np.load(LAGOS + 'bgrid65.npz')); H = dict(np.load(LAGOS + 'hgrid.npz')); R = dict(np.load(LAGOS + 'rgrid.npz'))
n250 = F['n'].shape
I, J = np.nonzero(place > 0); pp = place[I, J]; c250 = (I // 5) * n250[1] + (J // 5)
key = pp.astype(np.int64) * (n250[0] * n250[1]) + c250
uk, wk = np.unique(key, return_counts=True); pk = (uk // (n250[0] * n250[1])).astype(int); ck = (uk % (n250[0] * n250[1])).astype(int); wk = wk / 25.0
def wsum(a250, mask=None):
    v = a250.ravel()[ck] * wk
    if mask is not None: v = v * mask.ravel()[ck]
    return np.bincount(pk, weights=v, minlength=NP + 1)
built250 = (F['cover'] >= 0.10).astype(float)
bk = np.maximum(wsum(np.ones(n250), built250) / 16, 1 / 400)
landk = np.bincount(pp, minlength=NP + 1) * C * C / 1e6
hist = np.stack([wsum(B['hist'][k], built250) for k in range(B['hist'].shape[0])], 1)
P = {k: np.zeros(NP + 1) for k in ('poi', 'market', 'transit', 'campus')}
for r in pq.read_table(DATA + 'overture-lagos/lagos_overture_place.parquet', columns=['geometry', 'confidence', 'basic_category', 'names']).to_pylist():
    if (r['confidence'] or 0) < 0.5: continue
    g = shapely.from_wkb(r['geometry']); x, y = T.transform(g.x, g.y); i, j = ij(x, y)
    if not (0 <= i < NY and 0 <= j < NX) or place[i, j] == 0: continue
    u = place[i, j]; c = r['basic_category'] or ''; nm = ((r['names'] or {}).get('primary') or '').lower(); P['poi'][u] += 1
    if c in ('market', 'farmers_market') or re.search(r'\bmarket\b', nm): P['market'][u] += 1
    if c in ('public_transit_facility_or_service', 'train_station') or re.search(r'motor park|bus terminal|bus station|\bbrt\b|jetty|ferry terminal', nm): P['transit'][u] += 1
    if c == 'college_university': P['campus'][u] += 1
cl = K['cl'].copy(); _i = nd.distance_transform_edt(cl < 0, return_distances=False, return_indices=True); cl = cl[_i[0], _i[1]]
mix = np.zeros((NP + 1, 17)); np.add.at(mix, (pp, up(cl)[I, J]), 1); mix /= np.maximum(mix.sum(1, keepdims=True), 1)
nb50 = np.bincount(pp, weights=OB['n'][I, J], minlength=NP + 1); ab50 = np.bincount(pp, weights=OB['a'][I, J], minlength=NP + 1)
big50 = np.bincount(pp, weights=OB['big'][I, J], minlength=NP + 1)
nbuilt = wsum(F['n'].astype(float), built250); abuilt = wsum(B['a'], built250)
bp = wsum(H['bp']); hs = wsum(H['hs']); h4 = wsum(H['h4'])
gw = wsum(K['grid'] * F['n'], built250); gn = wsum(F['n'].astype(float), built250)
popb = wsum(F['pop'], built250); Lb = wsum(R['L'], built250); Lall = wsum(R['L']); Lmaj = wsum(R['Lmaj'])
rows = []
for q in PL:
    u = q['id']; h = hist[u]; c = np.cumsum(h); k = int(np.argmax(c >= c[-1] / 2)) if c[-1] else 0
    prev = c[k - 1] if k else 0; medfoot = 2 ** (k + 3 + (c[-1] / 2 - prev) / max(h[k], 1e-9)) if c[-1] else 0
    rows.append(dict(id=u, name=q['name'], land_km2=round(landk[u], 2), built_km2=round(bk[u], 2), roof_km2=round(ab50[u] / 1e6, 3),
        built_share=round(min(bk[u] / max(landk[u], 1e-9), 1), 3), bldg=int(nb50[u]),
        bldg_per_km2=int(nbuilt[u] / bk[u]), roof_cover=round(abuilt[u] / (bk[u] * 1e6), 3), median_foot_m2=round(medfoot, 0),
        big_share=round(big50[u] / max(ab50[u], 1), 3), height_m=round(hs[u] / max(bp[u], 1), 2), share4=round(h4[u] / max(bp[u], 1), 3),
        grid=round(gw[u] / max(gn[u], 1), 3), pop=int(wsum(F['pop'])[u]) if False else 0, pop_per_built_km2=int(popb[u] / bk[u]),
        street_km_per_km2=round(Lb[u] / 1000 / bk[u], 1), major_share=round(Lmaj[u] / max(Lall[u], 1), 3), poi_per_km2=round(P['poi'][u] / bk[u], 1),
        ov_markets=int(P['market'][u]), ov_transit=int(P['transit'][u]), ov_campus=int(P['campus'][u]), fabric=q['fabric'],
        mix=mix[u].round(4).tolist()))
popall = wsum(F['pop'])
for r in rows: r['pop'] = int(popall[r['id']])
# similarity
MET = [('bldg_per_km2', 'log'), ('median_foot_m2', 'log'), ('big_share', 'lin'), ('height_m', 'lin'), ('share4', 'sqrt'), ('grid', 'lin'),
       ('pop_per_built_km2', 'log'), ('street_km_per_km2', 'lin'), ('major_share', 'lin'), ('built_share', 'lin'), ('roof_cover', 'lin'), ('poi_per_km2', 'log')]
tr = lambda v, t: np.log1p(v) if t == 'log' else (np.sqrt(v) if t == 'sqrt' else v)
M = np.array([[tr(float(r[k]), t) for k, t in MET] for r in rows])
ref = np.array([r['roof_km2'] >= 0.1 for r in rows])           # the scale is set by places with real built land, not by slivers of bush
Z = np.clip((M - M[ref].mean(0)) / M[ref].std(0), -3, 3)
Pc = np.array([r['mix'] for r in rows]); Sq = np.sqrt(Pc)
Hd = np.sqrt(((Sq[:, None, :] - Sq[None, :, :]) ** 2).sum(-1) / 2)
Md = np.sqrt(((Z[:, None, :] - Z[None, :, :]) ** 2).mean(-1))
rr = np.ix_(ref, ref); H95 = Hd[rr].max(); M95 = Md[rr].max()
Sim = 100 * (1 - (0.5 * np.minimum(Hd / H95, 1) + 0.5 * np.minimum(Md / M95, 1)))
np.save(WORK + 'sim.npy', Sim.astype(np.float32))
# ---------- table of borders
out = []
def nm(u): return byid[u]['name']
for (a, b), R_ in rec.items():
    L = R_['n'] * C / 1000; kinds = R_['kinds']; main = kinds.most_common(1)[0][0]
    out.append(dict(a=int(a), b=int(b), place_a=nm(a), place_b=nm(b), border=main,
                    border_mix='; '.join('%s %.2f km' % (k, v * C / 1000) for k, v in kinds.most_common()),
                    roads='; '.join(r for r, _ in R_['roads'].most_common(3)), length_km=round(L, 2), built_meets_km=round(R_['meet'] * C / 1000, 2),
                    built_meets_share=round(R_['meet'] / R_['n'], 2), similarity=round(float(Sim[a - 1, b - 1]), 1),
                    bridge='; '.join(sorted(bridge.get((a, b), []))), touch=False))
for (a, b) in water_pairs:
    out.append(dict(a=int(a), b=int(b), place_a=nm(a), place_b=nm(b), border='open water', border_mix='lagoon, harbour or wide creek',
                    roads='', length_km=0.0, built_meets_km=0.0, built_meets_share=0.0, similarity=round(float(Sim[a - 1, b - 1]), 1),
                    bridge='; '.join(sorted(bridge.get((a, b), []))), touch=False))
# really touching: built land meets across at least 200 m of the border
for o in out: o['touch'] = o['built_meets_km'] >= 0.2
json.dump(dict(rows=rows, borders=out, MET=MET, H95=float(H95), M95=float(M95)), open(WORK + 'borders.json', 'w'))
with open(OUT + 'borders.csv', 'w', newline='') as f:
    cols = ['place_a', 'place_b', 'border', 'border_mix', 'roads', 'length_km', 'built_meets_km', 'built_meets_share', 'touch', 'similarity', 'bridge']
    w = csv.writer(f); w.writerow(cols)
    for o in sorted(out, key=lambda o: (-o['touch'], -o['similarity'])): w.writerow([o[c] for c in cols])
with open(OUT + 'places.csv', 'w', newline='') as f:
    cols = ['id', 'name', 'fabric', 'land_km2', 'built_km2', 'roof_km2', 'bldg', 'bldg_per_km2', 'median_foot_m2', 'big_share', 'height_m', 'share4', 'grid',
            'pop', 'pop_per_built_km2', 'street_km_per_km2', 'major_share', 'poi_per_km2', 'ov_markets', 'ov_transit', 'ov_campus']
    w = csv.writer(f); w.writerow(cols + ['lat', 'lon', 'gazetteer names inside'])
    for r, q in zip(rows, PL): w.writerow([r[c] for c in cols] + q['latlon'] + ['; '.join(q['gaz'])])
print('land borders', len(rec), 'touching', sum(o['touch'] for o in out), 'water pairs', len(water_pairs), 'bridge pairs', len(bridge))
print('kinds', collections.Counter(o['border'] for o in out))
