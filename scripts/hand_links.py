# Hand placing helper: streets cut off from the city's road network (a cluster that only met a shore road, now a footpath in the v2
# frame) each get one link street to the nearest road, written into the district's hand file as an exact placement with a note.
# The link is the shortest straight line from the cluster to a road of the main network, clear of water, at most 120 m; it may run
# through up to 4 houses (they are taken down, recorded as delete edits) when no clear link is nearly as short.
# Usage: python3 scripts/hand_links.py [ids...]      (reads web/gidi-data.js; rerun the bake afterwards)
import json, os, sys
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union, nearest_points
from shapely.strtree import STRtree

G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
ids = sys.argv[1:] or [d['id'] for d in G['districts']]
wet = unary_union([Polygon(w).buffer(0) for w in G['water'] + G['ocean']])
B = [Polygon(b[1:]).buffer(0) for L in G['buildings'].values() for b in L if len(b) > 3]
bt = STRtree(B)
# the drivable network: streets, mains, arterials (not lanes or paths), pieces joined where their ends meet (within 1 m)
ways = [('street', d, LineString(p)) for d, L in G['streets'].items() for p in L if len(p) > 1] + \
       [('main', m.get('d'), LineString(m['pts'])) for m in G['mains'] if len(m['pts']) > 1] + \
       [('art', None, LineString(a['pts'])) for a in G['arterials']]
wt = STRtree([g for k, d, g in ways])
par = list(range(len(ways)))
def find(i):
    while par[i] != i:
        par[i] = par[par[i]]; i = par[i]
    return i
for i, (k, d, g) in enumerate(ways):
    for j in wt.query(g.buffer(1.0)):
        if j != i and g.distance(ways[j][2]) < 1.0:
            par[find(i)] = find(j)
comps = {}
for i in range(len(ways)):
    comps.setdefault(find(i), []).append(i)
main = max(comps.values(), key=lambda c: sum(ways[i][2].length for i in c))
mainU = unary_union([ways[i][2] for i in main])
added = {}
for c in comps.values():
    if c is main:
        continue
    ds = {ways[i][1] for i in c if ways[i][1]}
    d = next(iter(ds)) if len(ds) == 1 else (ways[c[0]][1] or None)
    if d not in ids:
        continue
    U = unary_union([ways[i][2] for i in c])
    best = None
    for g in getattr(U, 'geoms', [U]):
        for t in [x / 20 for x in range(21)]:
            p = g.interpolate(t, normalized=True)
            q = nearest_points(mainU, p)[0]
            ln = LineString([p, q])
            if ln.length < 1 or ln.length > 120 or ln.intersects(wet):
                continue
            hit = [j for j in bt.query(ln.buffer(3.0)) if B[j].distance(ln) < 3.0]   # what a street (and its walkways) would run through
            if len(hit) > 4:
                continue
            cost = ln.length + 60 * len(hit)   # a link through houses only if there is no clear one nearly as short
            if best is None or cost < best[0]:
                best = (cost, ln, hit)
    if best is None:
        print(f'{d}: a cluster of {len(c)} streets near ({U.centroid.x:.0f}, {U.centroid.y:.0f}) has no link: place it by hand')
        continue
    cost, best, hit = best
    for j in hit:   # the houses the link runs through come down (a planner's call, recorded)
        q = B[j].representative_point()
        added.setdefault(d, []).append({'op': 'delete building', 'at': [round(q.x, 1), round(q.y, 1)],
                                        'note': 'cleared for a link street', 'early': True, 'by': 'Claude, 16 Oct 2026 (scripts/hand_links.py)'})
    added.setdefault(d, []).append({'op': 'add street', 'kind': 'street', 'pts': [[round(x, 1), round(y, 1)] for x, y in best.coords],
                                    'note': f'links {len(c)} cut-off streets to the city ({best.length:.0f} m' + (f', through {len(hit)} houses taken down)' if hit else ')'),
                                    'by': 'Claude, 16 Oct 2026 (scripts/hand_links.py)'})
for d, E in added.items():
    f = f'web/hand/{d}.json'
    H = json.load(open(f)) if os.path.exists(f) else {'district': d, 'layout': 'v2', 'edits': [], 'log': []}
    if H.get('layout', 'v1') != 'v2':   # the v1 file is kept as a record; v2 edits go in their own file
        f = f'web/hand/{d}-v2.json'
        H = json.load(open(f)) if os.path.exists(f) else {'district': d, 'layout': 'v2', 'edits': [], 'log': []}
    have = {json.dumps(e.get('pts') or e.get('at')) for e in H['edits']}
    new = [e for e in E if json.dumps(e.get('pts') or e.get('at')) not in have]
    H['edits'] += new
    if new:
        H['log'].append(f'16 Oct 2026: {len(new)} link streets added by scripts/hand_links.py')
    json.dump(H, open(f, 'w'), indent=1)
    print(f'{d}: {len(new)} link streets -> {f}')
