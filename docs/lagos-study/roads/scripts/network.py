# Measure the skeleton, choose the real extent that fits Gidi's 27 x 10.5 km frame at 1:3, draw it.
import pickle, json, collections, numpy as np, shapely, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.spatial import cKDTree
from common import *
import gaz
S = pickle.load(open(WORK + 'skel.pkl', 'rb')); segs, nodes = S['segs'], S['nodes']
OB = np.load(WORK + 'ob50.npz'); WC = np.load(WORK + 'wc50.npz')
roof = OB['a'].astype(float)
from scipy import ndimage as nd
_l = np.load(LAGOS + 'feat.npz')['lga'] >= 0
STATE = up(nd.binary_fill_holes(nd.binary_closing(_l, iterations=3)) | _l)      # Lagos State land and lagoon (LGA polygons, gaps filled)

# ---------- 1. the frame: the 81 x 31.5 km real window (27 x 10.5 km at 1:3) holding the most roof area
W, H = FRAME[0] * SCALE, FRAME[1] * SCALE
yy, xx = np.nonzero((roof > 0) & STATE)   # only Lagos State's roofs choose the frame (Ogun's edge towns do not)
px = X0 + (xx + .5) * C; py = Y0 + (yy + .5) * C; pw = roof[yy, xx]
best = None
for ang in range(-20, 21, 1):
    t = np.radians(ang); c, s = np.cos(t), np.sin(t)
    u = px * c + py * s; v = -px * s + py * c                      # frame axes
    G = 500; u0, v0 = u.min(), v.min()
    iu = ((u - u0) // G).astype(int); iv = ((v - v0) // G).astype(int)
    A = np.zeros((iv.max() + 1, iu.max() + 1)); np.add.at(A, (iv, iu), pw)
    I = np.pad(A.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    w, h = int(W // G), int(H // G)
    if A.shape[0] < h or A.shape[1] < w: continue
    Sm = I[h:, w:] - I[:-h, w:] - I[h:, :-w] + I[:-h, :-w]
    k = np.unravel_index(np.argmax(Sm), Sm.shape)
    if best is None or Sm[k] > best[0]:
        best = (Sm[k], ang, u0 + k[1] * G, v0 + k[0] * G)
tot, ang, fu, fv = best
t = np.radians(ang); c, s = np.cos(t), np.sin(t)
def to_frame(x, y):            # real metres -> frame metres (0..W, 0..H)
    x = np.asarray(x); y = np.asarray(y)
    return x * c + y * s - fu, -x * s + y * c - fv
def from_frame(u, v):
    u = np.asarray(u) + fu; v = np.asarray(v) + fv
    return u * c - v * s, u * s + v * c
corners = [from_frame(a, b) for a, b in ((0, 0), (W, 0), (W, H), (0, H))]
corners_ll = [tuple(round(q, 4) for q in TI.transform(*p)[::-1]) for p in corners]
def inside(x, y):
    u, v = to_frame(x, y); return (u >= 0) & (u <= W) & (v >= 0) & (v <= H)
inroof = pw[inside(px, py)].sum()
G = gaz.load(); gx, gy = T.transform([g[2] for g in G], [g[1] for g in G])
outside = [G[k][0] for k in range(len(G)) if not inside(gx[k], gy[k])]
frame = dict(angle_deg=ang, corners_latlon=corners_ll, real_km=(W / 1000, H / 1000), roof_share_in_frame=round(inroof / pw.sum(), 3),
             roof_km2_in=round(inroof / 1e6, 1), roof_km2_all=round(pw.sum() / 1e6, 1), outside=outside)
print('frame', frame)

# ---------- 2. network lengths: carriageway km and centre-line km (a dual carriageway counted once)
lines = [shapely.LineString(s['xy']) for s in segs]
tree = shapely.STRtree(lines)
def centre_share(k):
    """Share of segment k that is NOT the second side of a dual carriageway (same name or class, parallel, within 40 m)."""
    s = segs[k]; ln = lines[k]
    if s['L'] < 20: return 1.0
    ds = np.arange(10, s['L'], 20.0); P = shapely.points(np.array([ln.interpolate(d).coords[0] for d in ds]))
    hit = tree.query(P, predicate='dwithin', distance=40)
    paired = np.zeros(len(ds), bool)
    for pi, q in zip(*hit):
        if q == k: continue
        o = segs[q]
        if o['kind'] != s['kind'] or o['cls'] != s['cls'] or (s['name'] and o['name'] != s['name']): continue
        # parallel test: the other line's direction near the point
        d0 = lines[q].project(P[pi]); a = lines[q].interpolate(max(d0 - 10, 0)); b = lines[q].interpolate(min(d0 + 10, lines[q].length))
        d1 = ln.interpolate(max(ds[pi] - 10, 0)); d2 = ln.interpolate(min(ds[pi] + 10, s['L']))
        v1 = np.array([b.x - a.x, b.y - a.y]); v2 = np.array([d2.x - d1.x, d2.y - d1.y])
        if np.linalg.norm(v1) < 1 or np.linalg.norm(v2) < 1: continue
        if abs(v1 @ v2) / np.linalg.norm(v1) / np.linalg.norm(v2) > 0.9 and ln.distance(lines[q]) > 4:   # parallel, not the continuation
            paired[pi] = True
    return 1 - 0.5 * paired.mean()
cs = np.array([centre_share(k) for k in range(len(segs))])
inF = np.array([inside(*s['xy'].mean(0)) for s in segs])
rows = collections.OrderedDict()
for key in ('motorway', 'trunk', 'primary', 'secondary', 'rail'):
    for link in (False, True):
        m = [k for k, s in enumerate(segs) if s['cls'] == key and s['link'] == link]
        if not m: continue
        L = np.array([segs[k]['L'] for k in m]) / 1000; f = inF[m]
        rows[key + (' links' if link else '')] = dict(carriageway_km=round(L.sum(), 1), centre_km=round((L * cs[m]).sum(), 1),
            centre_km_in_frame=round((L * cs[m])[f].sum(), 1), centre_km_at_1to3=round((L * cs[m])[f].sum() / 3, 1))
for k, v in rows.items(): print('%-16s' % k, v)

# ---------- 3. bridges: bridge-flagged spans, grouped by name and place (pieces within 300 m)
import shapely.ops
bp = [(n, c_, L, shapely.ops.substring(lines[k], a, b, normalized=True)) for k, s in enumerate(segs) for a, b in s['bspans']
      for n, c_, L in [((s['name'] or '(unnamed %s)' % s['cls']), s['cls'], (b - a) * s['L'] * cs[k])] if L >= 15]
groups = []
for n, c_, L, g in sorted(bp, key=lambda r: -r[2]):
    for gr in groups:
        if gr['name'] == n and gr['geom'].distance(g) < 300:
            gr['km'] += L / 1000; gr['geom'] = gr['geom'].union(g); break
    else:
        groups.append(dict(name=n, cls=c_, km=L / 1000, geom=g))
bridges = sorted(groups, key=lambda g: -g['km'])
for g in bridges:
    p = g['geom'].centroid; g['latlon'] = [round(q, 4) for q in TI.transform(p.x, p.y)[::-1]]; g['in_frame'] = bool(inside(p.x, p.y))
print('bridges >= 100 m:', sum(g['km'] >= 0.1 for g in bridges), 'total bridge km (centre)', round(sum(g['km'] for g in bridges), 1))
for g in bridges[:25]: print('  %-40s %-9s %.2f km %s' % (g['name'], g['cls'], g['km'], g['latlon']))

# ---------- 4. junctions: major-road connector nodes clustered within 150 m; interchanges carry links
nx_ = np.array([[n['x'], n['y']] for n in nodes])
tr = cKDTree(nx_); par = list(range(len(nodes)))
def find(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for a, b in tr.query_pairs(150): par[find(a)] = find(b)
cl = collections.defaultdict(list)
for k in range(len(nodes)): cl[find(k)].append(k)
junc = []
for mem in cl.values():
    x, y = nx_[mem].mean(0)
    names = sorted({nm for k in mem for nm in nodes[k]['names']}); classes = sorted({q for k in mem for q in nodes[k]['classes']})
    links = sum(nodes[k]['links'] for k in mem)
    junc.append(dict(x=x, y=y, n=len(mem), names=names, classes=classes, links=links, interchange=links >= 4, in_frame=bool(inside(x, y))))
print('junctions', len(junc), 'interchanges', sum(j['interchange'] for j in junc), 'in frame', sum(j['in_frame'] for j in junc))

# ---------- 5. key crossings [K] points, measured within 700 m
KEY = [('Oshodi', 6.5530, 3.3440), ('Ojota', 6.5870, 3.3810), ('Maryland', 6.5715, 3.3665), ('Ikeja Along', 6.6050, 3.3260),
       ('Ojuelegba', 6.5085, 3.3655), ('Ijora (Apapa road)', 6.4690, 3.3680), ('Mile 2', 6.4650, 3.3140),
       ('Kara/Berger', 6.6390, 3.3730), ('Ketu-Mile 12', 6.6030, 3.3950), ('Lekki toll gate', 6.4345, 3.4700), ('Ajah', 6.4675, 3.5720),
       ('Obalende/CMS', 6.4500, 3.4020), ('Iyana Ipaja', 6.6120, 3.2960), ('Ikorodu garage', 6.6170, 3.5050), ('Abule Egba', 6.6440, 3.3030),
       ('Third Mainland, Oworonshoki end', 6.5545, 3.3985), ('Third Mainland, Adeniji end', 6.4600, 3.3950)]
# where two named roads meet: the point where they come closest, nearest the [K] hint
PAIR = {'Oshodi': ('Agege Motor Road', 'Apapa-Oworonshoki Expressway'), 'Ojota': ('Ikorodu Road', 'Lagos-Ibadan Expressway'),
        'Maryland': ('Ikorodu Road', 'Mobolaji Bank-Anthony Way'), 'Ikeja Along': ('Agege Motor Road', 'Lagos-Abeokuta Expressway'),
        'Ojuelegba': ('Ojuelegba Road', 'Western Avenue'),
        'Mile 2': ('Apapa-Oworonshoki Expressway', 'Lagos-Badagry Expressway'),
        'Kara/Berger': ('Lagos-Ibadan Expressway', 'Isheri Road'), 
        'Third Mainland, Adeniji end': ('Third Mainland Bridge', 'Ring Road')}
def meet(a, b, hx, hy):
    A = [lines[k] for k, s in enumerate(segs) if s['name'] == a]; B = [lines[k] for k, s in enumerate(segs) if s['name'] == b]
    if not A or not B: return None
    best = None
    for la in A:
        for lb in B:
            d = la.distance(lb)
            if d > 60: continue
            p, q = shapely.ops.nearest_points(la, lb); x, y = (p.x + q.x) / 2, (p.y + q.y) / 2
            h = np.hypot(x - hx, y - hy)
            if best is None or h < best[0]: best = (h, x, y)
    return best if best and best[0] < 2500 else None
key = []
for k_, (nm, la, lo) in enumerate(KEY):
    x, y = T.transform(lo, la)
    if nm in PAIR:
        m = meet(*PAIR[nm], x, y)
        if m: x, y = m[1], m[2]
        else: print('no meeting found for', nm)
    KEY[k_] = (nm,) + tuple(TI.transform(x, y)[::-1])
    P = shapely.Point(x, y)
    near = tree.query(P, predicate='dwithin', distance=700)
    rn = sorted({segs[k]['name'] for k in near if segs[k]['kind'] == 'road' and segs[k]['name'] and not segs[k]['link']})
    lk = sum(lines[k].intersection(P.buffer(700)).length for k in near if segs[k]['link']) / 1000
    br = sum(1 for g in bridges if g['geom'].distance(P) < 700 and g['km'] >= 0.05)
    jn = [j for j in junc if np.hypot(j['x'] - x, j['y'] - y) < 700]
    key.append(dict(name=nm, roads=rn, n_roads=len(rn), link_km=round(lk, 2), junction_nodes=sum(j['n'] for j in jn), bridges=br, in_frame=bool(inside(x, y))))
    print('%-32s roads %2d links %.1f km nodes %3d bridges %d  %s' % (nm, len(rn), lk, key[-1]['junction_nodes'], br, ', '.join(rn[:8])))
json.dump(dict(frame=frame, rows=rows, bridges=[{k: v for k, v in g.items() if k != 'geom'} for g in bridges if g['km'] >= 0.05],
               junctions=dict(all=len(junc), interchanges=sum(j['interchange'] for j in junc), in_frame=sum(j['in_frame'] for j in junc),
                              interchanges_in_frame=sum(j['interchange'] and j['in_frame'] for j in junc)), key=key,
               fu=fu, fv=fv), open(WORK + 'network.json', 'w'), indent=1)

# ---------- 6. pictures
STY = {'motorway': ('#c0392b', 2.2), 'trunk': ('#e67e22', 1.7), 'primary': ('#d4ac0d', 1.2), 'secondary': ('#1f6f8b', 0.7), 'rail': ('#6c3483', 1.0)}
def base(ax, xf=None, scale=1.0, alpha=1):
    wat = WC['water'] >= 0.5; wet = (WC['wet'] + WC['mang']) >= 0.4; cov = roof / C ** 2
    img = np.ones((NY, NX, 3)); img[wet] = (0.80, 0.90, 0.84); img[wat] = (0.70, 0.83, 0.95)
    b = np.clip(cov * 2.5, 0, 1); img = img * (1 - 0.32 * b[..., None])
    img[~STATE] = img[~STATE] * 0.93 + 0.07 * np.array([1.0, 0.95, 0.85])
    if xf is None:
        ax.imshow(img, origin='lower', extent=[X0 / 1000, (X0 + NX * C) / 1000, Y0 / 1000, (Y0 + NY * C) / 1000], interpolation='nearest')
    return img
def draw_lines(ax, f, lwmul=1.0):
    for cls_ in ('secondary', 'primary', 'trunk', 'motorway', 'rail'):
        col, lw = STY[cls_]
        L = [f(s['xy']) for s in segs if s['cls'] == cls_]
        ax.add_collection(LineCollection(L, colors=col, linewidths=lw * lwmul * (0.6 if cls_ != 'rail' else 1), zorder=3 if cls_ != 'secondary' else 2,
                                         linestyles='-' if cls_ != 'rail' else (0, (2, 1))))
    for g in bridges:
        if g['km'] < 0.1: continue
        gs = g['geom'].geoms if hasattr(g['geom'], 'geoms') else [g['geom']]
        ax.add_collection(LineCollection([f(np.asarray(q.coords)) for q in gs], colors='k', linewidths=2.2 * lwmul, zorder=4))
def legend(ax):
    from matplotlib.lines import Line2D
    h = [Line2D([], [], color=STY[k][0], lw=2.5, label=k) for k in STY] + [Line2D([], [], color='k', lw=3, label='bridge (>100 m)')]
    ax.legend(handles=h, loc='lower right', fontsize=8, framealpha=0.9)
km = lambda a: a / 1000
# a) whole state, real scale
fig, ax = plt.subplots(figsize=(22, 5.6), dpi=110)
base(ax); draw_lines(ax, lambda xy: xy / 1000, 0.8)
P = np.array(corners + [corners[0]]) / 1000; ax.plot(P[:, 0], P[:, 1], 'b-', lw=1.5)
ax.set_title('Lagos State: the road skeleton at real scale (km, UTM 31N). Blue box: the 81 x 31.5 km that becomes Gidi at 1:3'); legend(ax)
ax.set_aspect('equal'); ax.set_xlim(X0 / 1000, (X0 + NX * C) / 1000); ax.set_ylim(Y0 / 1000, (Y0 + NY * C) / 1000)
fig.tight_layout(); fig.savefig(OUT + 'skeleton_state.png'); plt.close(fig)
# b) the frame region, real scale, with key crossings labelled
fig, ax = plt.subplots(figsize=(20, 8.6), dpi=110)
base(ax); draw_lines(ax, lambda xy: xy / 1000, 1.0); ax.plot(P[:, 0], P[:, 1], 'b-', lw=1.5)
for kk in key:
    x, y = T.transform(*[q for q in [k for k in KEY if k[0] == kk['name']][0][2:0:-1]])
    ax.plot(x / 1000, y / 1000, 'o', mfc='none', mec='b', ms=9); ax.text(x / 1000 + .3, y / 1000 + .3, kk['name'], fontsize=7, color='navy', zorder=6)
bx = P[:, 0]; by = P[:, 1]; ax.set_xlim(bx.min() - 2, bx.max() + 2); ax.set_ylim(by.min() - 2, by.max() + 2); ax.set_aspect('equal')
ax.set_title('The metro at real scale (km). Blue box = Gidi frame; circles = key crossings'); legend(ax)
fig.tight_layout(); fig.savefig(OUT + 'skeleton_metro.png'); plt.close(fig)
# c) Gidi frame at 1:3: 27 x 10.5 km
fig, ax = plt.subplots(figsize=(20, 8.4), dpi=110)
img = base(ax, xf=True)
# resample the base picture into the frame: each frame pixel (90 m real = 30 m Gidi) looks up the real cell
uu, vv = np.meshgrid(np.arange(0, W, 90) + 45, np.arange(0, H, 90) + 45)
rx, ry = from_frame(uu, vv); ii, jj = ij(rx, ry); ok = (ii >= 0) & (ii < NY) & (jj >= 0) & (jj < NX)
fimg = np.ones(uu.shape + (3,)); fimg[ok] = img[ii[ok], jj[ok]]
ax.imshow(fimg, origin='lower', extent=[0, W / SCALE / 1000, 0, H / SCALE / 1000], interpolation='nearest')
def tf(xy):
    u, v = to_frame(xy[:, 0], xy[:, 1]); return np.column_stack([u, v]) / SCALE / 1000
draw_lines(ax, tf, 1.1)
for kk in key:
    x, y = T.transform(*[q for q in [k for k in KEY if k[0] == kk['name']][0][2:0:-1]]); u, v = tf(np.array([[x, y]]))[0]
    if 0 <= u <= 27 and 0 <= v <= 10.5: ax.text(u + .1, v + .1, kk['name'], fontsize=7, color='navy', zorder=6)
ax.set_xlim(0, 27); ax.set_ylim(0, 10.5); ax.set_aspect('equal')
ax.set_title('Gidi at 1:3: the real skeleton shrunk into the 27 x 10.5 km frame (axes in Gidi km; frame turned %d deg)' % ang); legend(ax)
fig.tight_layout(); fig.savefig(OUT + 'skeleton_gidi_1to3.png'); plt.close(fig)
print('pictures done')
