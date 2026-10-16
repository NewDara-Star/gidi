# Hand fix: houses that reach over a street's building line in the finished map (web/gidi-data.js). The bake's road clean-up extends and
# straightens streets after the houses are placed, and roads placed by hand can pass close to houses. Each one is moved straight back
# from its street until it is 0.2 m clear of the line; if that would put it on another house, a water edge or another road's line, it
# comes down instead. Written into the district's hand file (scripts/hand.py: move / delete building) with a note on each.
# Declared encroachment zones (market streets) and the kinds that stand on a road on purpose are left alone.
# Usage: python3 scripts/hand_fix_lines.py [ids...]    (then bake; the checks read the finished map)
import json, os, sys
from shapely.geometry import LineString, Point, Polygon
from shapely.affinity import translate
from shapely.ops import unary_union, nearest_points
from shapely.strtree import STRtree
sys.path.insert(0, os.path.dirname(__file__))
import cross_sections as XS

G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
ids = sys.argv[1:] or [d['id'] for d in G['districts'] if d.get('fabric') == 'lagos']
ON_ROAD = {'toll booth', 'toll canopy', 'border booth', 'border canopy', 'drums', 'checkpoint', 'stalls', 'raft', 'stilt', 'stilt bar'}
wet = unary_union([Polygon(w).buffer(0) for w in G['water'] + G['ocean']])
roads = [('street', LineString(p)) for L in G['streets'].values() for p in L if len(p) > 1] + \
        [('lane', LineString(p)) for L in (G.get('lanes') or {}).values() for p in L if len(p) > 1] + \
        [('main', LineString(m['pts'])) for m in G['mains'] if len(m['pts']) > 1] + \
        [(a['cls'] if a['cls'] in XS.SECTIONS else 'art', LineString(a['pts'])) for a in G['arterials'] if a['cls'] != 'bridge']
lines = [(k, g, g.buffer(XS.building_line(k) - 0.1, cap_style=2)) for k, g in roads]
lt = STRtree([z for k, g, z in lines])
rt = STRtree([g for k, g in roads])
W = [g for k, g in roads] + [LineString(p) for k in ('paths',) for L in (G.get(k) or {}).values() for p in L if len(p) > 1]
wt = STRtree(W)
zones = unary_union([Polygon(z['pts']).buffer(0) for z in G.get('encroach', [])]) if G.get('encroach') else None
BY = 'Claude, 16 Oct 2026 (scripts/hand_fix_lines.py)'
tot = {}
for d in ids:
    L = G['buildings'].get(d, [])
    P = [Polygon(b[1:]).buffer(0) if len(b) > 3 else None for b in L]
    bt = STRtree([p for p in P if p is not None]); idx = [i for i, p in enumerate(P) if p is not None]
    edits = []
    for i, (b, p) in enumerate(zip(L, P)):
        if p is not None and b[0] == 'stalls' and not any(Polygon(q['pts']).buffer(0.5).contains(p) for q in (G.get('parcels') or {}).get(d, [])) \
                and all(g.distance(p) > 30 for k, g in [roads[j] for j in rt.query(p.buffer(30))]):   # a market table whose street has gone
            at = p.representative_point()
            edits.append({'op': 'delete building', 'at': [round(at.x, 1), round(at.y, 1)], 'kind': 'stalls',
                          'note': 'a market table stranded over 30 m from any road (its street was moved in the clean-up)', 'by_who': BY})
            continue
        if p is None:
            continue
        at = p.representative_point()
        if b[0] in ('shed', 'extension', 'back') and not any(Polygon(q['pts']).buffer(0.5).contains(p) for q in (G.get('parcels') or {}).get(d, [])) \
                and all(w.distance(p) > 45 for w in [W[j] for j in wt.query(p.buffer(45))]):   # nobody could walk to its door
            edits.append({'op': 'delete building', 'at': [round(at.x, 1), round(at.y, 1)], 'kind': b[0],
                          'note': 'a back-yard room over 45 m from any street, lane or path: comes down', 'by_who': BY}); continue
        ov = [idx[j] for j in bt.query(p) if idx[j] != i and P[idx[j]].intersection(p).area > 0.05]
        if ov and p.area <= min(P[j].area for j in ov):   # two houses overlap: the smaller comes down
            edits.append({'op': 'delete building', 'at': [round(at.x, 1), round(at.y, 1)], 'kind': b[0],
                          'note': 'overlapped a bigger neighbour: comes down', 'by_who': BY}); continue
        if b[0] in ON_ROAD or (zones is not None and zones.contains(p.centroid)):
            continue
        over = [j for j in lt.query(p) if lines[j][2].intersection(p).area > 0.05]
        if not over:
            continue
        k, g, z = lines[max(over, key=lambda j: lines[j][2].intersection(p).area)]
        q = nearest_points(g, p.centroid)[0]; c = p.centroid
        L_ = c.distance(q) or 1.0; ux, uy = (c.x - q.x) / L_, (c.y - q.y) / L_
        need = XS.building_line(k) - p.distance(g) + 0.2
        moved = translate(p, ux * need, uy * need)
        clash = any(lines[j][2].intersection(moved).area > 0.05 for j in lt.query(moved)) or moved.intersects(wet) or \
                any(P[idx[j]].intersection(moved).area > 0.05 for j in bt.query(moved) if idx[j] != i)
        at = p.representative_point()
        if clash or need > 6:
            edits.append({'op': 'delete building', 'at': [round(at.x, 1), round(at.y, 1)], 'kind': b[0],
                          'note': f'over the building line of a {k} by {need - 0.2:.1f} m and no room to move back: comes down', 'by_who': BY})
        else:
            edits.append({'op': 'move building', 'at': [round(at.x, 1), round(at.y, 1)], 'kind': b[0], 'by': [round(ux * need, 2), round(uy * need, 2)],
                          'note': f'over the building line of a {k}: moved back {need:.1f} m', 'by_who': BY})
    if not edits:
        continue
    f = f'web/hand/{d}.json'
    H = json.load(open(f)) if os.path.exists(f) else {'district': d, 'layout': 'v2', 'edits': [], 'log': []}
    if H.get('layout', 'v1') != 'v2':
        f = f'web/hand/{d}-v2.json'
        H = json.load(open(f)) if os.path.exists(f) else {'district': d, 'layout': 'v2', 'edits': [], 'log': []}
    have = {json.dumps(e.get('at')) for e in H['edits']}
    new = [e for e in edits if json.dumps(e['at']) not in have]
    H['edits'] += new; H['log'].append(f'16 Oct 2026: {len(new)} houses off the building lines (scripts/hand_fix_lines.py)')
    json.dump(H, open(f, 'w'), indent=1)
    tot[d] = (sum(1 for e in new if e['op'] == 'move building'), sum(1 for e in new if e['op'] == 'delete building'))
print('moved, taken down:', tot)
