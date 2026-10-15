# What is on the ground here? Everything the map holds at one spot, from the built data (web/gidi-data.js): the district and
# the ground's height, the surface (carriageway, gutter, walkway, market street, building, plot, yard, water), the building
# and its height, the plot, safe ground, any deck overhead, the furniture within reach, the nearest named place.
# Usage: python3 scripts/whats_here.py X Y          (map metres, y running south, as in the 2D map's coordinates)
#        python3 scripts/whats_here.py "Mile Market"   (a named place)
import json, math, sys
from shapely.geometry import LineString, Point, Polygon

G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
T = json.load(open('web/terrain.json'))
XS = G.get('cross_sections', {})
if len(sys.argv) == 2:
    p = next((q for q in G['pois'] if q['name'].lower() == sys.argv[1].lower()), None)
    if not p:
        sys.exit('no place called ' + sys.argv[1])
    X, Y = p['x'], p['y']
else:
    X, Y = float(sys.argv[1]), float(sys.argv[2])
P = Point(X, Y)
say = []


def ground(x, y):
    C, Z = T['cell_m'], T['z']
    fx, fy = x / C - 0.5, y / C - 0.5
    j0, i0 = int(math.floor(fx)), int(math.floor(fy))
    tx, ty = fx - j0, fy - i0
    at = lambda i, j: Z[min(max(i, 0), T['h'] - 1) * T['w'] + min(max(j, 0), T['w'] - 1)] / 10
    return at(i0, j0) * (1 - tx) * (1 - ty) + at(i0, j0 + 1) * tx * (1 - ty) + at(i0 + 1, j0) * (1 - tx) * ty + at(i0 + 1, j0 + 1) * tx * ty


dist = next((d for d in G['districts'] if Polygon(d['poly'][0]).contains(P)), None)
built = dist and dist.get('fabric') == 'lagos'
say.append(f"({X:.1f}, {Y:.1f}) in {dist['name'] if dist else 'no district'}" + (" (built to the cross-sections)" if built else " (not yet rebuilt to the cross-sections: widths are the agreed ones, the district may not respect them yet)" if dist else ''))
wet = any(Polygon(w).contains(P) for w in G['water'] + G['ocean'])
say.append(f"ground height {0.0 if wet else ground(X, Y):.1f} m above the water")

surface = None
if wet:
    surface = 'water (the lagoon or the sea)'
for c in G.get('canals', []):
    if LineString(c['pts']).distance(P) <= c.get('width', 4) / 2:
        surface = f"water: a canal ({c.get('width', 4)} m wide)"
# roads at their cross-sections
roads = [('street', LineString(p), f'{d} street') for d, L in G['streets'].items() for p in L if len(p) > 1]
roads += [('lane', LineString(p), f'{d} lane') for d, L in G['lanes'].items() for p in L if len(p) > 1]
roads += [('main', LineString(m['pts']), m.get('name') or 'a main road') for m in G['mains']]
roads += [(a['cls'] if a['cls'] in XS else 'art', LineString(a['pts']), a['name']) for a in G['arterials']]
near_roads = sorted(((g.distance(P), k, n, g) for k, g, n in roads if g.distance(P) < 25), key=lambda r: r[0])
for dd, k, n, g in near_roads[:1]:
    x = XS.get(k)
    if not x:
        break
    c = x['carriageway'] / 2
    if dd <= c:
        surface = surface or f"carriageway of {n} ({k}, {x['carriageway']} m wide, {dd:.1f} m from its centre line)"
    elif dd <= c + x['gutter']:
        gt = min((gg for gg in G.get('gutters', []) if len(gg.get('pts', [])) > 1 and LineString(gg['pts']).distance(P) < 3.0), key=lambda gg: LineString(gg['pts']).distance(P), default=None)
        surface = surface or f"the gutter (open drain) beside {n}" + (f": {gt['state']}" if gt else '')
    elif dd <= c + x['gutter'] + x['walkway']:
        surface = surface or f"the walkway beside {n} (where poles, lights, signs and bus stops stand)"
    say.append(f"nearest road: {n} ({k}), centre line {dd:.1f} m away")
zone = next((z for z in G.get('encroach', []) if Polygon(z['pts']).buffer(0).contains(P)), None)
if zone:
    say.append(f"inside a declared zone: {zone['kind']} (traders may stand here on purpose)")
# deck overhead
for s in G.get('structures', []) + [a for a in G['arterials'] if a['cls'] == 'bridge']:
    g = LineString(s['pts'])
    w = s.get('width', 22 if s.get('cls') == 'bridge' else 8)
    if g.distance(P) <= w / 2 and s.get('z'):
        t = g.project(P) / max(g.length, 1e-6) * (len(s['z']) - 1)
        i = min(int(t), len(s['z']) - 2) if len(s['z']) > 1 else 0
        z = s['z'][i] + (s['z'][i + 1] - s['z'][i]) * (t - i) if len(s['z']) > 1 else s['z'][0]
        say.append(f"overhead: {s.get('kind', s.get('cls'))} {s['name']}, deck top {z:.1f} m (above the ground here: {z - (0 if wet else ground(X, Y)):.1f} m)")
# building
for d, L in G['buildings'].items():
    st = (G.get('storeys') or {}).get(d, [])
    sty = (G.get('styles') or {}).get(d) or []
    for i, b in enumerate(L):
        if len(b) > 3 and Polygon(b[1:]).buffer(0).contains(P):
            n = st[i] if i < len(st) else 1
            say.append(f"building: {b[0]} #{i} of {d}, {n} storey{'s' if n > 1 else ''} (~{n * 3.1:.0f} m)" + (f", style {sty[i]}" if i < len(sty) and sty[i] else '')
                       + f", footprint {Polygon(b[1:]).area:.0f} m2")
            surface = surface or f"inside a building ({b[0]})"
# plot, safe ground
for d, L in (G.get('parcels') or {}).items():
    for p in L:
        if Polygon(p['pts']).buffer(0).contains(P):
            say.append(f"plot: {p['kind']} ({d})")
            surface = surface or f"open ground inside a {p['kind']} plot"
for s in G.get('safe_ground', []):
    if Polygon(s['pts']).buffer(0).contains(P):
        say.append(f"SAFE GROUND: {s['name']} ({s['type']}) - never a crime site")
# furniture, places, junctions
fu = sorted(((math.dist((f['x'], f['y']), (X, Y)), f) for f in G.get('furniture', [])), key=lambda t: t[0])
for dd, f in [t for t in fu if t[0] < 6][:5]:
    say.append(f"{f['kind']} {dd:.1f} m away at ({f['x']}, {f['y']})")
j = min(G.get('junctions', []), key=lambda j: math.dist((j['x'], j['y']), (X, Y)), default=None)
if j and math.dist((j['x'], j['y']), (X, Y)) < 40:
    say.append(f"junction {math.dist((j['x'], j['y']), (X, Y)):.0f} m away: {j['kind']}" + (f" ({j.get('name')})" if j.get('name') else '') + (f", {', '.join(j['roads'])}" if j.get('roads') else ''))
poi = min(G['pois'], key=lambda q: math.dist((q['x'], q['y']), (X, Y)))
say.append(f"nearest named place: {poi['name']} ({poi['type']}), {math.dist((poi['x'], poi['y']), (X, Y)):.0f} m")
say.insert(2, 'SURFACE: ' + (surface or 'open ground (a yard, a gap between buildings, or waste ground)'))
print('\n'.join(say))
