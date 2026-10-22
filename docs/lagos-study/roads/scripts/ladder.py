# Join places into districts: only places that really touch (built land meets across 200 m or more of their border)
# and are alike enough. The Google checks of 22 Oct are fixed: some pairs never join, two always do.
import json, csv, re, collections, numpy as np
from common import *
B = json.load(open(WORK + 'borders.json')); rows = B['rows']; borders = B['borders']
PL = json.load(open(WORK + 'places.json'))['places']; NW = json.load(open(WORK + 'network.json'))
Sim = np.load(WORK + 'sim.npy')
fu, fv = NW['fu'], NW['fv']
NP = len(PL); byid = {q['id']: q for q in PL}; R = {r['id']: r for r in rows}
OPEN_ROOF = 0.10          # km2 of roof: below this a place is open land (bush, swamp, sand), not a district
built = [q['id'] for q in PL if q['roof_km2'] >= OPEN_ROOF]
bset = set(built)
inframe = {q['id']: bool(0 <= q['x'] - fu <= 81000 and 0 <= q['y'] - fv <= 31500) for q in PL}
COMPASS = r'\s+(north|south|east|west|north-east|north-west|south-east|south-west)(\s+\d+)?$'
def tags(q):
    t = set(q['gaz'])
    base = re.sub(COMPASS, '', q['name'].split(',')[0]).strip(); t.add(base)
    return t
TAG = {q['id']: tags(q) for q in PL}
def has(p, names): return bool(TAG[p] & names)
NEVER = [({'Ikoyi', 'Old Ikoyi', 'Banana Island', 'Parkview', 'Dolphin Estate'}, {'Obalende', 'Onikan', 'Lafiaji'}),
         ({'Festac'}, {'Okota', 'Ago Palace'}),
         ({'Magodo', 'Shangisha'}, {'Ketu', 'Mile 12', 'Ikosi', 'Alapere'}),
         ({'Gbagada', 'Gbagada Phase 2', 'Ifako-Gbagada', 'Soluyi'}, {'Maryland', 'Mende', 'Onigbongbo'}),
         ({'Apapa GRA', 'Apapa Wharf'}, {'Trade Fair', 'Abule Ado', 'Satellite Town'}),
         ({'Alaba'}, {'Ijanikin', 'Morogbo', 'Agbara', 'Otto-Awori'}),
         ({'Ilupeju'}, {'Ladipo', 'Papa Ajao'}),
         ({'Ajao Estate'}, {'Airport (MMIA)'})]
ALWAYS = [({'Bariga', 'Ilaje (Bariga)'}, {'Shomolu'}), ({'Badore'}, {'Ajah', 'Ilaje Ajah'})]
touch = collections.defaultdict(set); bd = {}
for o in borders:
    bd[(o['a'], o['b'])] = o
    if o['touch'] and o['a'] in bset and o['b'] in bset: touch[o['a']].add(o['b']); touch[o['b']].add(o['a'])
w = {p: max(R[p]['roof_km2'], 1e-3) for p in built}
def gsim(A, B_):
    a = np.array(A) - 1; b = np.array(B_) - 1
    wa = np.array([w[p] for p in A]); wb = np.array([w[p] for p in B_])
    return float((Sim[np.ix_(a, b)] * np.outer(wa, wb)).sum() / (wa.sum() * wb.sum()))
def conflict(A, B_):
    for x, y in NEVER:
        if (any(has(p, x) for p in A) and any(has(p, y) for p in B_)) or (any(has(p, y) for p in A) and any(has(p, x) for p in B_)): return True
    return False

def run():
    cl = {p: [p] for p in built}; cn = {p: set(touch[p]) for p in built}; owner = {p: p for p in built}
    def merge(a, b, s, why):
        cl[a] += cl.pop(b); cn[a] = (cn[a] | cn.pop(b)) - {a, b}
        for c in cn[a]: cn[c] = (cn[c] - {a, b}) | {a}
        for p in cl[a]: owner[p] = a
        steps.append(dict(sim=round(s, 1), a=a, b=b, why=why, count_after=len(cl)))
    steps = []
    forced = []
    for x, y in ALWAYS:
        A = [p for p in built if has(p, x)]; Bs = [p for p in built if has(p, y)]
        if not A or not Bs: continue
        # join every named piece of each side, then the two sides
        for grp in (A, Bs):
            for p in grp[1:]:
                if owner[p] != owner[grp[0]]: merge(owner[grp[0]], owner[p], gsim(cl[owner[grp[0]]], cl[owner[p]]), 'Google check: always together')
        a, b = owner[A[0]], owner[Bs[0]]
        if a != b:
            t = b in cn[a]; forced.append((sorted(x)[0], sorted(y)[0], t)); merge(a, b, gsim(cl[a], cl[b]), 'Google check: always together')
    snaps = {}
    while True:
        best = None
        for a in cl:
            for b in cn[a]:
                if a < b and not conflict(cl[a], cl[b]):
                    s = gsim(cl[a], cl[b])
                    if best is None or s > best[0]: best = (s, a, b)
        if best is None: break
        snaps[len(cl)] = {k: list(v) for k, v in cl.items()}
        merge(best[1], best[2], best[0], 'ladder')
    snaps[len(cl)] = {k: list(v) for k, v in cl.items()}
    return steps, snaps, forced
steps, snaps, forced = run()
NB = len(built); nforced = sum(s['why'] != 'ladder' for s in steps)
start = NB - nforced
lad = [s for s in steps if s['why'] == 'ladder']
def groups_at(t):
    k = next((i for i, s in enumerate(lad) if s['sim'] < t), len(lad))
    return snaps[start - k]
def roof(g): return sum(R[p]['roof_km2'] for p in g)
def bkm(g): return sum(R[p]['built_km2'] for p in g)
def gin(g): return sum(R[p]['roof_km2'] for p in g if inframe[p]) > 0.5 * roof(g)
def gtouch(G):
    adj = collections.defaultdict(set); own = {p: k for k, g in G.items() for p in g}
    for p in built:
        for q in touch[p]:
            if own[p] != own[q]: adj[own[p]].add(own[q])
    return adj
TINY = 3.0          # km2 of built land (real): under 0.33 km2 at 1:3, too small for a district
SPECIAL = {'campus', 'port & tank farm', 'airport', 'barracks', 'waterfront', 'towers'}
anyb = collections.defaultdict(set)
for o in borders:
    if o['a'] in bset and o['b'] in bset: anyb[o['a']].add(o['b']); anyb[o['b']].add(o['a'])
def standout(g):
    """A small place kept as its own district: its main fabric is a special one (campus, port, airport, barracks, stilts, towers)."""
    fb = collections.Counter()
    for p in g: fb[R[p]['fabric']] += R[p]['roof_km2']
    return fb.most_common(1)[0][0] in SPECIAL and bkm(g) >= 1.0
def fold(G, keep_standouts=True):
    """Tiny groups fold into the most alike group they touch. A tiny group that touches nothing (an island, a hamlet in
    the bush) goes with the most alike group across any border, water included: a satellite, not a district."""
    G = {k: list(v) for k, v in G.items()}
    while True:
        adj = gtouch(G); own = {p: k for k, g in G.items() for p in g}
        cands = sorted([k for k, g in G.items() if bkm(g) < TINY and not (keep_standouts and standout(g))], key=lambda k: bkm(G[k]))
        done = False
        for k in cands:
            nb = adj[k] or {own[q] for p in G[k] for q in anyb[p] if own[q] != k}
            opts = [(gsim(G[k], G[o]), o) for o in nb if not conflict(G[k], G[o])]
            if not opts: continue
            s, o = max(opts)
            G[o] += G.pop(k); done = True; break
        if not done: return G
TH = [90, 85, 80, 75, 70, 65, 60, 55, 50]
table = []
for t in TH:
    G = groups_at(t); Gf = fold(G)
    table.append(dict(t=t, all=len(G), folded=len(Gf), frame=sum(gin(g) for g in G.values()), frame_folded=sum(gin(g) for g in Gf.values())))
    print(table[-1])
# district names: its three biggest places by roof
def dname(g):
    top = sorted(g, key=lambda p: -R[p]['roof_km2'])
    n = [re.sub(COMPASS, '', byid[p]['name'].split(',')[0]).strip() for p in top]
    out = []
    for x in n:
        if x not in out: out.append(x)
    return ' / '.join(out[:3]) + (' (+%d places)' % (len(g) - 3) if len(g) > 3 else '')
json.dump(dict(steps=steps, table=table, forced=forced, built=built, start=start,
               snaps={t: {str(k): v for k, v in groups_at(t).items()} for t in TH},
               folded={t: {str(k): v for k, v in fold(groups_at(t)).items()} for t in TH}), open(WORK + 'ladder.json', 'w'))
with open(OUT + 'ladder.csv', 'w', newline='') as f:
    wr = csv.writer(f); wr.writerow(['step', 'similarity_pct', 'why', 'group_a', 'group_b', 'groups_after'])
    cl = {p: [p] for p in built}
    for i, s in enumerate(steps):
        wr.writerow([i + 1, s['sim'], s['why'], dname(cl[s['a']]), dname(cl[s['b']]), s['count_after']]); cl[s['a']] += cl.pop(s['b'])
print('forced', forced, 'built places', NB, 'in frame', sum(inframe[p] for p in built))
