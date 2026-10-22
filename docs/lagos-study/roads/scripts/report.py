# District maps for the chosen thresholds, the old unit pairs that are not real neighbours, and the close calls for Google.
import json, csv, sys, collections, re, numpy as np
from common import *
import plot_places as PP
B = json.load(open(WORK + 'borders.json')); borders = B['borders']; R = {r['id']: r for r in B['rows']}
PL = json.load(open(WORK + 'places.json'))['places']; byid = {q['id']: q for q in PL}
LD = json.load(open(WORK + 'ladder.json'))
CHOSEN = [int(t) for t in (sys.argv[1:] or ['65', '60', '55'])]
COMPASS = r'\s+(north|south|east|west|north-east|north-west|south-east|south-west)(\s+\d+)?$'
base = lambda p: re.sub(COMPASS, '', byid[p]['name'].split(',')[0]).strip()
def dname(g):
    out = []
    for p in sorted(g, key=lambda p: -R[p]['roof_km2']):
        if base(p) not in out: out.append(base(p))
    return ' / '.join(out[:3])
nbr = collections.defaultdict(collections.Counter)
for o in borders:
    w = o['length_km'] if o['border'] != 'open water' else 0.05
    nbr[o['a']][o['b']] += w; nbr[o['b']][o['a']] += w
NW = json.load(open(WORK + 'network.json')); fu, fv = NW['fu'], NW['fv']
inframe = lambda p: 0 <= byid[p]['x'] - fu <= 81000 and 0 <= byid[p]['y'] - fv <= 31500
summary = {}
for t in CHOSEN:
    G = {int(k): v for k, v in LD['folded'][str(t)].items()}
    own = {p: k for k, g in G.items() for p in g}
    # open land and places too small to count go with the group they share the most border with (repeat to reach inland pieces)
    for it in range(30):
        ch = 0
        for q in PL:
            p = q['id']
            if p in own: continue
            c = collections.Counter()
            for o, wgt in nbr[p].items():
                if o in own: c[own[o]] += wgt
            if c: own[p] = c.most_common(1)[0][0]; ch += 1
        if not ch: break
    gi = {k: i for i, k in enumerate(sorted(G, key=lambda k: -sum(R[p]['roof_km2'] for p in G[k])))}
    group = {p: gi[k] for p, k in own.items()}
    dist = []
    for k in sorted(G, key=lambda k: gi[k]):
        g = G[k]; roof = sum(R[p]['roof_km2'] for p in g); bk = sum(R[p]['built_km2'] for p in g)
        inf = sum(R[p]['roof_km2'] for p in g if inframe(p)) > 0.5 * roof
        dist.append(dict(n=gi[k] + 1, name=dname(g), places=[byid[p]['name'] for p in sorted(g, key=lambda p: -R[p]['roof_km2'])],
                         roof_km2=round(roof, 2), built_km2=round(bk, 1), built_km2_1to3=round(bk / 9, 2), in_frame=inf))
    summary[t] = dist
    labs = []
    for d in dist:
        g = G[[k for k in G if gi[k] == d['n'] - 1][0]]
        top = max(g, key=lambda p: R[p]['roof_km2'])
        labs.append((byid[top]['x'] / 1000, byid[top]['y'] / 1000, '%d %s' % (d['n'], d['name'].split(' / ')[0])))
    nfr = sum(d['in_frame'] for d in dist)
    PP.draw(OUT + 'districts_%d.png' % t, PP.frame_box(), group=group, labels=labs, fs=6,
            title='Districts at %d%% similarity, tiny places folded: %d with most of their roofs in the Gidi frame (real km). Open land coloured with its neighbour' % (t, nfr))
    PP.draw(OUT + 'districts_%d_inner.png' % t, PP.INNER, group=group, labels=labs + [(byid[p]['x'] / 1000, byid[p]['y'] / 1000, '') for p in []], fs=7,
            title='Districts at %d%%, inner metro (real km)' % t)
# ---------- old units: which of the first study's neighbour pairs really touch now
U = np.load(SCR + 'similar/units.npz')['unit']; UN = json.load(open(SCR + 'similar/unit_names.json'))
Pz = np.load(WORK + 'places.npz'); place = Pz['place']
u50 = up(U)
I, J = np.nonzero(place > 0); pu = collections.defaultdict(collections.Counter)
for p, u in zip(place[I, J], u50[I, J]):
    if u >= 0: pu[p][u] += 1
home = {p: c.most_common(1)[0][0] for p, c in pu.items() if c.most_common(1)[0][1] >= 0.5 * sum(c.values())}
# each old unit's core: the new places carrying its names (old names are made of neighbourhood names joined by '-');
# a unit with no namesake place falls back to the places lying mostly inside it
TAGS = {q['id']: set(q['gaz']) | {base(q['id'])} for q in PL}
def toks(n): return {t.strip() for t in re.split(r'[-/()]', n.replace('Lagos Island East', '')) if len(t.strip()) > 2}
core = {}
for u, n in enumerate(UN):
    tk = toks(n)
    c = {p for p, tg in TAGS.items() if any(any(t == x or x.startswith(t + ' ') or t.startswith(x + ' ') for x in tg) for t in tk)}
    c = {p for p in c if pu[p].get(u, 0) > 0} or {p for p, h in home.items() if h == u}
    core[u] = c
tb = {}
for o in borders:
    k = (min(o['a'], o['b']), max(o['a'], o['b'])); tb[k] = o
def link(A, B_):
    """built land meets between the two cores, km; and the land border length."""
    m = l = 0.0
    if A & B_: return 9.9, 9.9
    for p in A:
        for q in B_:
            o = tb.get((min(p, q), max(p, q)))
            if o and o['border'] != 'open water': m += o['built_meets_km']; l += o['length_km']
    return m, l
idx = {n: i for i, n in enumerate(UN)}
notreal = []
for r in csv.DictReader(open(os.path.expanduser('~/gidi/docs/lagos-study/similar/pairs.csv'))):
    a, b = idx[r['unit_a']], idx[r['unit_b']]; m, l = link(core[a], core[b])
    if m < 0.2:
        between = set()
        for p in core[a]:
            for o_, w_ in nbr[p].items():
                if o_ in core[b]: continue
                if any(o2 in core[b] for o2 in nbr[o_]) and R[o_]['roof_km2'] >= 0.05: between.add(byid[o_]['name'])
        notreal.append(dict(a=r['unit_a'], b=r['unit_b'], old_link=r['link'], old_edge_km=r['shared_edge_km'], old_sim=r['similarity_pct'],
                            core_a='; '.join(byid[p]['name'] for p in core[a]), core_b='; '.join(byid[p]['name'] for p in core[b]),
                            new_land_border_km=round(l, 2), new_built_meets_km=round(m, 2), places_between='; '.join(sorted(between)[:6])))
# ---------- close calls
close = []
for t in CHOSEN:
    for s in LD['steps']:
        if s['why'] == 'ladder' and abs(s['sim'] - t) <= 2.5: close.append((t, s['sim']))
weak = [o for o in borders if 0.1 <= o['built_meets_km'] < 0.35 and R[o['a']]['roof_km2'] >= 0.3 and R[o['b']]['roof_km2'] >= 0.3]
split = [o for o in borders if o['border'] == 'street (named split)' and R[o['a']]['roof_km2'] >= 0.3 and R[o['b']]['roof_km2'] >= 0.3]
json.dump(dict(summary=summary, notreal=notreal, weak=[(o['place_a'], o['place_b'], o['built_meets_km'], o['length_km'], o['border']) for o in weak],
               split=[(o['place_a'], o['place_b'], o['length_km'], o['similarity']) for o in split]), open(WORK + 'report.json', 'w'), indent=1)
with open(OUT + 'districts.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['threshold', 'district', 'name', 'in_frame', 'roof_km2', 'built_km2', 'built_km2_at_1to3', 'places'])
    for t, ds in summary.items():
        for d in ds: w.writerow([t, d['n'], d['name'], d['in_frame'], d['roof_km2'], d['built_km2'], d['built_km2_1to3'], '; '.join(d['places'])])
with open(OUT + 'not_neighbours.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(list(notreal[0].keys()))
    for r in notreal: w.writerow(list(r.values()))
print('old pairs', 185, 'not real neighbours now', len(notreal), 'weak touches', len(weak), 'named splits', len(split))
