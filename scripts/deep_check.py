# Does a generated district come out like its inspiration? Measures a gen file the way the deep study measured real Lagos (the same
# structure measures, scripts/structure.py, on built 500 m squares; storeys; street density) and prints it beside the study's targets.
# Usage: python3 scripts/deep_check.py <id> [gen.json] [picture.png]     (reads web/gidi-data.js for the outline and water)
import json, math, sys, os
import numpy as np
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
from shapely.strtree import STRtree
sys.path.insert(0, os.path.dirname(__file__))
from structure import measure

DID = sys.argv[1]
F = json.load(open(sys.argv[2] if len(sys.argv) > 2 else f'web/gen-{DID}.json'))
J = json.load(open(f'docs/data/deep/{DID}.json'))
G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
P = Polygon(next(d for d in G['districts'] if d['id'] == DID)['poly'][0])
water = unary_union([Polygon(w).buffer(0) for w in G['water'] + G['ocean']])
land = P.difference(water)
ST_ALL = F.get('storeys') or [1] * len(F['buildings'])
B, BST = [], []   # buildings (not market tables), and their storeys, in step
for b, s_ in zip(F['buildings'], ST_ALL):
    if len(b) > 3 and b[0] != 'stalls':
        g = Polygon(b[1:]).buffer(0)
        if g.area >= 6:
            B.append(g); BST.append(s_)
BST = np.array(BST)
W = {'street': 5.0, 'main': 7.5, 'art': 14}
ways = [(LineString(s), W['street']) for s in F['streets']] + [(LineString(m['pts']), W['main']) for m in F['mains']] + \
       [(LineString(a['pts']), W['art']) for a in G['arterials'] if a['cls'] != 'bridge']
tree = STRtree(B); wt = STRtree([g for g, w in ways])
SQ = 500.0; rows = []
x0, y0, x1, y1 = land.bounds
for x in np.arange(x0, x1 - SQ, SQ / 2):
    for y in np.arange(y0, y1 - SQ, SQ / 2):
        sq = box(x, y, x + SQ, y + SQ)
        if land.intersection(sq).area < 0.95 * SQ * SQ:
            continue
        bs = [B[i] for i in tree.query(sq)]
        ss = [ways[i] for i in wt.query(sq.buffer(30))]
        cov = sum(b.area for b in bs if sq.contains(b.centroid)) / (SQ * SQ)
        if cov < 0.10 or sum(g.intersection(sq).length for g, w in ss) < 1200:
            continue
        rows.append(measure(bs, [g for g, w in ss], sq, [w for g, w in ss]))
med = lambda k: float(np.median([r[k] for r in rows if r.get(k) is not None])) if rows else None
sub = lambda k, s: float(np.median([r[k][s] for r in rows if r.get(k)])) if rows else None
Q = J['structure_built_squares']; tq = lambda k: (Q.get(k) or {}).get('median') if isinstance(Q.get(k), dict) else Q.get(k)
st = F.get('storeys') or []
area_w = np.array([b.area for b in B])
sh = lambda k: float(area_w[BST == k].sum() / area_w.sum())   # by built area, as the generator's bands and the study's storeys_share_by_area
real_sh = J['heights'].get('storeys_share_by_area') or J['heights']['storeys_share']
drive_km = (sum(LineString(s).intersection(land).length for s in F['streets']) + sum(LineString(m['pts']).intersection(land).length for m in F['mains'])) / 1000
R = [('buildings per km2 (built squares)', med('per_km2'), tq('per_km2'), 0),
     ('ground built over', med('cover'), tq('cover'), 2), ('touching', med('touching'), tq('touching'), 2),
     ('under 40 m2', med('under_40m2'), tq('under_40m2'), 2), ('street front occupied', med('front_occupied'), tq('front_occupied'), 2),
     ('block fill', sub('block_fill', 'median'), Q.get('block_fill.median'), 2), ('line to the street, deg', sub('line_deg', 'median'), Q.get('line_deg.median'), 1),
     ('footprint median m2', float(np.median(area_w)), J['buildings']['size_m2']['p50'], 0),
     ('storeys 1 (by area)', sh(1), real_sh['1'], 2), ('storeys 2 (by area)', sh(2), real_sh['2'], 2),
     ('storeys 3+ (by area)', 1 - sh(1) - sh(2), 1 - real_sh['1'] - real_sh['2'], 2),
     ('drivable km per km2 (whole land)', drive_km / (land.area / 1e6), J['streets']['drivable_km_per_km2'], 1)]
print(f'{DID}: {len(B):,} buildings on {land.area / 1e6:.2f} km2; {len(rows)} built 500 m squares (overlapping)')
print(f"{'measure':34} {'Gidi':>9} {'real':>9}  off")
bad = 0
for n, g, r, d in R:
    if g is None or r is None:
        continue
    off = (g - r) / r if r else 0
    flag = '' if abs(off) <= 0.2 else ' <-- ' + ('high' if off > 0 else 'low')
    bad += bool(flag)
    print(f'{n:34} {g:9.{d}f} {r:9.{d}f} {off:+5.0%}{flag}')
print(f'{bad} measures more than 20% off')
os.makedirs('docs/data/deep-check', exist_ok=True)   # read by scripts/deep_tune.py
json.dump({'id': DID, 'squares': len(rows), 'buildings': len(B), 'land_km2': round(land.area / 1e6, 3),
           'storeys_by_area': {str(k): round(float(area_w[np.minimum(BST, 8) == k].sum() / area_w.sum()), 3) for k in range(1, 9)},
           'measures': {n: {'gidi': None if g is None else round(g, 4), 'real': None if r is None else round(r, 4)} for n, g, r, d in R}},
          open(f'docs/data/deep-check/{DID}.json', 'w'), indent=1)
if len(sys.argv) > 3:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    fig, ax = plt.subplots(figsize=(13, 13 * (y1 - y0) / (x1 - x0)))
    ax.set_facecolor('#f3efe6')
    for w in G['water'] + G['ocean']:
        ax.fill(*Polygon(w).exterior.xy, color='#a9cbe6')
    ZC = ['#e74c3c', '#f39c12', '#27ae60', '#2980b9', '#8e44ad']
    names = []
    for z in F.get('zones', []):
        if z['type'] not in names:
            names.append(z['type'])
        ax.fill(*zip(*z['pts']), color=ZC[names.index(z['type']) % 5], alpha=.13, lw=0)
    SC = {1: '#cdb895', 2: '#a07a52', 3: '#7a4a2a', 4: '#4a2418'}
    ax.add_collection(PolyCollection([b[1:] for b in F['buildings']], facecolors=[SC[min(s, 4)] for s in ST_ALL], edgecolors='none'))
    for s in F['streets']:
        ax.plot(*zip(*s), color='#bbb', lw=.5)
    for m in F['mains']:
        ax.plot(*zip(*m['pts']), color='#e0a040', lw=1.6)
    for a in G['arterials']:
        ax.plot(*zip(*a['pts']), color='#c0392b', lw=2.4)
    for i, n in enumerate(names):
        ax.plot([], [], 's', color=ZC[i % 5], alpha=.5, label=n)
    ax.legend(loc='upper left', fontsize=8)
    ax.set_xlim(x0 - 50, x1 + 50); ax.set_ylim(y1 + 50, y0 - 50); ax.set_aspect('equal')
    ax.set_title(f'{DID}: {len(B):,} buildings, by storeys (pale 1 to dark 4+); fabric types shaded')
    plt.tight_layout(); plt.savefig(sys.argv[3], dpi=60)
