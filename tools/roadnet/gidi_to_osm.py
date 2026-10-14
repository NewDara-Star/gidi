"""Turn Gidi's roads (web/gidi-data.js) into an OSM file that SUMO's netconvert understands, so
Gidi gets the same lane network as the owner's Real-world sim: lanes, right of way, signals,
footpaths, crossings, walking areas.

python3 tools/roadnet/gidi_to_osm.py web/city/net/gidi.osm web/city/net/gidi.world.json

- Geometry: Gidi metres (x east, y south) become lon/lat by a local linear map round the city's
  centre; bake_net.py maps them back to metres (x east, z south) centred on the same point.
- Classes: expressways -> trunk (3+3 lanes), arterials -> primary (2+2), bridges -> trunk bridges,
  district mains -> secondary (2+2, 14 m), streets -> residential, lanes -> living_street,
  paths -> footway, flyovers -> primary bridges on layer 1, skywalks and footbridges -> footway
  bridges. Gidi drives on the right.
- Junctions: roads only meet where they share a node, so every endpoint that lands on another
  road (a T) and every crossing of two roads on the same layer gets a shared node.
- Signals on main-road and expressway crossings; give-way where a street meets a main road.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_OSM, OUT_WORLD = sys.argv[1:3]
gd = open(os.path.join(ROOT, 'web', 'gidi-data.js')).read()
gd = json.loads(gd[gd.index('{'):gd.rindex('}') + 1])
W, H = gd['size'][0], gd['size'][1] if len(gd['size']) > 1 else 6720.0
CX, CY = W / 2, 3360.0
LON0, LAT0 = 3.40, 6.50  # any origin works: the map is linear and bake_net inverts it
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110574.0

lines = []  # (pts, tags, layer)
for m in gd.get('mains', []):
    lines.append((m['pts'], {'highway': 'secondary', 'lanes': '4', 'maxspeed': '50', 'name': m.get('name', '')}, 0))
for d, ls in gd.get('streets', {}).items():
    for ln in ls:
        lines.append((ln, {'highway': 'residential', 'lanes': '2', 'maxspeed': '30'}, 0))
for d, ls in gd.get('lanes', {}).items():
    for ln in ls:
        lines.append((ln, {'highway': 'living_street', 'maxspeed': '15'}, 0))
for d, ls in gd.get('paths', {}).items():
    for ln in ls:
        lines.append((ln, {'highway': 'footway'}, 0))
for a in gd.get('arterials', []):
    if a['cls'] == 'exp':
        tags = {'highway': 'trunk', 'lanes': '6', 'maxspeed': '80', 'name': a['name']}
    elif a['cls'] == 'bridge':
        tags = {'highway': 'trunk', 'lanes': '4', 'maxspeed': '80', 'bridge': 'yes', 'name': a['name']}
    else:
        tags = {'highway': 'primary', 'lanes': '4', 'maxspeed': '60', 'name': a['name']}
    lines.append((a['pts'], tags, 0))
for s in gd.get('structures', []):
    if s['kind'] in ('flyover', 'ramp'):
        lines.append((s['pts'], {'highway': 'primary', 'lanes': '2' if s['width'] < 14 else '4', 'bridge': 'yes', 'layer': str(s.get('layer', 1)), 'name': s['name']}, s.get('layer', 1)))
    elif s['kind'] in ('skywalk', 'footbridge'):
        lines.append((s['pts'], {'highway': 'footway', 'bridge': 'yes', 'layer': '1'}, 1))

MAJOR = {'secondary', 'primary', 'trunk'}

# ---- shared nodes: snap endpoints, split at T's and crossings on the same layer ----
nodes = {}  # key -> (id, x, y)
nid = [0]


def node(x, y):
    k = (round(x * 2), round(y * 2))  # 0.5 m snap
    if k not in nodes:
        nid[0] += 1
        nodes[k] = (nid[0], x, y)
    return nodes[k][0]


segs = []  # (line index, seg index, a, b)
for li, (pts, tags, layer) in enumerate(lines):
    for i in range(len(pts) - 1):
        segs.append((li, i, pts[i], pts[i + 1]))
grid = {}
CELL = 50.0
for s in segs:
    a, b = s[2], s[3]
    for gx in range(int(min(a[0], b[0]) // CELL), int(max(a[0], b[0]) // CELL) + 1):
        for gy in range(int(min(a[1], b[1]) // CELL), int(max(a[1], b[1]) // CELL) + 1):
            grid.setdefault((gx, gy), []).append(s)

cuts = {li: {} for li in range(len(lines))}  # li -> seg index -> [t, ...]


def proj(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy or 1
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2
    t = max(0.0, min(1.0, t))
    return t, math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy))


def inter(a, b, c, d):
    r = (b[0] - a[0], b[1] - a[1])
    s = (d[0] - c[0], d[1] - c[1])
    den = r[0] * s[1] - r[1] * s[0]
    if abs(den) < 1e-9:
        return None
    t = ((c[0] - a[0]) * s[1] - (c[1] - a[1]) * s[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    if 0.001 < t < 0.999 and 0.001 < u < 0.999:
        return t, u
    return None


seen = set()
for cell, ss in grid.items():
    for i in range(len(ss)):
        for j in range(i + 1, len(ss)):
            s1, s2 = ss[i], ss[j]
            if s1[0] == s2[0] or (id(s1), id(s2)) in seen:
                continue
            seen.add((id(s1), id(s2)))
            if lines[s1[0]][2] != lines[s2[0]][2]:
                continue  # different layers pass over each other
            r = inter(s1[2], s1[3], s2[2], s2[3])
            if r:
                cuts[s1[0]].setdefault(s1[1], []).append(r[0])
                cuts[s2[0]].setdefault(s2[1], []).append(r[1])
            for (sa, sb) in ((s1, s2), (s2, s1)):  # an endpoint landing on the other road
                for e in (sa[2], sa[3]):
                    ends = lines[sa[0]][0]
                    if e not in (ends[0], ends[-1]):
                        continue
                    t, dd = proj(e, sb[2], sb[3])
                    if dd < 1.5 and 0.001 < t < 0.999:
                        cuts[sb[0]].setdefault(sb[1], []).append(t)

ways = []
for li, (pts, tags, layer) in enumerate(lines):
    nds = []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        if not nds:
            nds.append(node(*a))
        for t in sorted(cuts[li].get(i, [])):
            nds.append(node(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        nds.append(node(*b))
    dedup = [n for k, n in enumerate(nds) if k == 0 or n != nds[k - 1]]
    if len(dedup) >= 2:
        ways.append((dedup, tags))

# ---- control: signals where major roads cross, give-way where a minor road meets a major ----
use = {}
for nds, tags in ways:
    for n in set(nds):
        use.setdefault(n, []).append(tags['highway'])
node_tags = {}
for n, hws in use.items():
    major = sum(1 for h in hws if h in MAJOR)
    if len(hws) >= 2 and major >= 2:
        node_tags[n] = {'highway': 'traffic_signals', 'crossing': 'traffic_signals'}
    elif len(hws) >= 2 and major >= 1 and any(h in ('residential', 'living_street') for h in hws):
        node_tags[n] = {'highway': 'give_way'}

os.makedirs(os.path.dirname(OUT_OSM), exist_ok=True)
with open(OUT_OSM, 'w') as f:
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n<osm version='0.6' generator='gidi_to_osm'>\n")
    f.write(f"<bounds minlat='{LAT0 - (H - CY) / KY:.7f}' minlon='{LON0 - CX / KX:.7f}' maxlat='{LAT0 + CY / KY:.7f}' maxlon='{LON0 + (W - CX) / KX:.7f}'/>\n")
    for (k, (i, x, y)) in nodes.items():
        lon, lat = LON0 + (x - CX) / KX, LAT0 - (y - CY) / KY
        t = node_tags.get(i)
        if t:
            f.write(f"<node id='{i}' version='1' lat='{lat:.8f}' lon='{lon:.8f}'>" + ''.join(f"<tag k='{a}' v='{b}'/>" for a, b in t.items()) + "</node>\n")
        else:
            f.write(f"<node id='{i}' version='1' lat='{lat:.8f}' lon='{lon:.8f}'/>\n")
    for wi, (nds, tags) in enumerate(ways):
        f.write(f"<way id='{wi + 1}' version='1'>" + ''.join(f"<nd ref='{n}'/>" for n in nds) + ''.join(f"<tag k='{a}' v='{str(b).replace(chr(39), '')}'/>" for a, b in tags.items() if b != '') + "</way>\n")
    f.write("</osm>\n")
json.dump({'origin': {'lon': LON0, 'lat': LAT0}, 'half': {'x': CX, 'z': max(CY, H - CY)}, 'centre': {'x': CX, 'y': CY}}, open(OUT_WORLD, 'w'))
print(len(nodes), 'nodes', len(ways), 'ways', sum(1 for t in node_tags.values() if t['highway'] == 'traffic_signals'), 'signals')
