# One-off correction for a frozen district: its gutters were placed at the 3D kit's old road widths (a 7 m street, a 14 m main
# road) by scripts/isms.py; the agreed cross-sections (scripts/cross_sections.py) put the gutter right beside a narrower
# carriageway. Each run (and each crossing) slides in toward its road by the difference, and takes the agreed gutter width;
# its state, depth and crossings stay. Logged in the hand file.  Usage: python3 scripts/fix_gutters_to_sections.py foodgate
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import LineString, Point
from shapely.strtree import STRtree
import cross_sections as XS
OLD = {"lane": 3.5, "street": 7.0, "main": 14.0, "art": 18.0, "exp": 30.0}
d = sys.argv[1]
SRC = sys.argv[2] if len(sys.argv) > 2 else 'web/gidi-data.js'   # the built map the gutters were traced on (its road names match theirs)
path = f'web/hand/{d}.json'; H = json.load(open(path)); S = H['snapshot']
G = json.loads(open(SRC).read()[len('window.GIDI='):-1])
ROAD = {}
for dd, L in G['streets'].items():
    for i, p in enumerate(L): ROAD[f'{dd}/street/{i}'] = LineString(p)
for dd, L in G.get('lanes', {}).items():
    for i, p in enumerate(L): ROAD[f'{dd}/lane/{i}'] = LineString(p)
for i, m in enumerate(G['mains']): ROAD[f'main/{i}'] = LineString(m['pts'])
for a_ in G['arterials']: ROAD['art/' + a_['name']] = LineString(a_['pts'])
ORIG = {g['id']: g for g in G.get('gutters', []) if g.get('d') == d}
ORIGC = {c['id']: c for c in G.get('gutter_crossings', []) if c.get('gutter') in ORIG}


def new_w(k, w):
    return XS.SECTIONS[k]['gutter'] if XS.SECTIONS[k]['gutter'] > 0 else w


def shift(pt, road, k, w_new):
    """Put a gutter point at the agreed distance from its own road's centre line, on the side it was on."""
    P = Point(pt)
    q = road.interpolate(road.project(P))
    dd = q.distance(P)
    if dd < 1e-6:
        return pt
    target = XS.half(k) + w_new / 2
    return [round(q.x + (P.x - q.x) / dd * target, 1), round(q.y + (P.y - q.y) / dd * target, 1)]


kind_of = {}
n = 0
for g in S.get('gutters', []):
    o = ORIG.get(g['id'], g); road = ROAD.get(g['road'])
    k = g['kind'] if g['kind'] in XS.SECTIONS else 'street'
    w0 = o['w']; w1 = new_w(k, w0)
    if road is None:
        continue
    g['pts'] = [shift(p, road, k, w1) for p in o['pts']]
    g['w'] = w1
    old_len = LineString(o['pts']).length if len(o['pts']) > 1 else 0
    g['len'] = round(LineString(g['pts']).length, 1) if len(g['pts']) > 1 else g.get('len', 0)
    if o.get('blocked') and old_len > 0:   # blocked stretches scale with the run (it shortens a little as it moves in)
        f_ = g['len'] / old_len
        g['blocked'] = [dict(b, **{'from': round(b['from'] * f_, 1), 'to': round(min(b['to'] * f_, g['len']), 1)}) for b in o['blocked']]
    kind_of[g['id']] = (k, w0, w1)
    n += 1
m = 0
for c in S.get('gutter_crossings', []):
    if c['gutter'] in kind_of:
        k, w0, w1 = kind_of[c['gutter']]
        road = ROAD.get(next(g['road'] for g in S['gutters'] if g['id'] == c['gutter']))
        oc = ORIGC.get(c['id'], c)
        c['pt'] = shift(oc['pt'], road, k, w1) if road is not None else c['pt']
        og = ORIG.get(c['gutter']); ng = next(g for g in S['gutters'] if g['id'] == c['gutter'])
        if og and len(og['pts']) > 1 and 'at' in oc:   # its distance along the run scales the same way
            c['at'] = round(oc['at'] * ng['len'] / max(LineString(og['pts']).length, 1e-6), 1)
        m += 1
H['log'] = [l for l in H.get('log', []) if not l.startswith('gutters moved')]
H.setdefault('log', []).append(f"gutters moved to the agreed cross-sections (scripts/fix_gutters_to_sections.py): {n} runs, {m} crossings; states kept")
json.dump(H, open(path, 'w'), separators=(',', ':'))
print(path, n, 'runs and', m, 'crossings moved')
