"""Ìbùdó's areas built again from their real places, every one, in the child plan's order (owner, 21 Oct 2026: "if you fix a bug in the
future", it must reach everything already built). The area builds are not kept as hand edits any more: this writes them all, fresh, to
web/hand/gen/hub.json, which the bake applies before the hand edits (scripts/hand.py). After any change to the builder
(scripts/hand_spots/ibudo_real_area.py), the child plan or the real data, run this and bake: every area gets the change.
Each area is built on the map as the areas before it left it (applied here in memory, with the clean-up the bake does), so no bake is
needed between areas: one bake with no areas (the base), this, then one bake.
Usage: python3 scripts/rebuild_areas.py <base gidi-data.js, baked with web/hand/gen/hub.json away>
"""
import json
import os
import subprocess
import sys
import tempfile

from shapely.geometry import Polygon
from shapely.ops import unary_union

sys.path.insert(0, 'scripts')
import autoclean
import hand

BASE = sys.argv[1]
CP = json.load(open('docs/hand/ibudo/child_plan.json'))
s = open(BASE).read()
G = json.loads(s[s.index('{'):s.rstrip().rstrip(';').rindex('}') + 1])
TMP = tempfile.mkdtemp(prefix='gidi_areas_')
ALL = []
for n, A in enumerate(CP['areas']):
    base_f, hub_f, out_f = (os.path.join(TMP, x) for x in ('base.js', 'hub.json', 'area.json'))
    open(base_f, 'w').write('window.GIDI=' + json.dumps(G, separators=(',', ':'), ensure_ascii=False) + ';')
    json.dump({'district': 'hub', 'edits': ALL}, open(hub_f, 'w'), separators=(',', ':'), ensure_ascii=False)
    env = dict(os.environ, GIDI_BASE=base_f, GIDI_HUB=hub_f, GIDI_OUT=out_f)
    later = [Polygon(B_['pts']) for B_ in CP['areas'][n + 1:]]
    if later:   # the part a later area builds again is not this one's: its twin record and real figures leave it out
        env['GIDI_LATER_WKT'] = unary_union(later).wkt
    if n == 0:
        env['GIDI_CORRIDORS'] = '1'   # the layout's corridors through the whole district are cleared with the first area
    r = subprocess.run([sys.executable, '-W', 'ignore', 'scripts/hand_spots/ibudo_real_area.py', A['id']], env=env, capture_output=True, text=True)
    print('\n'.join(l for l in r.stdout.strip().splitlines() if l.startswith(('street pieces', 'WARNING'))) + '\n' + (r.stdout.strip().splitlines() or [''])[-1], r.stderr[-2000:] if r.returncode else '')
    if r.returncode:
        sys.exit(f'area {A["id"]} failed')
    E = json.load(open(out_f))
    hand._files = lambda E=E: iter([('mem', {'district': 'hub', 'layout': 'v2', 'edits': E})])
    del hand.MISSES[:]; hand._D[0] = 'hub'
    hand.apply_road_edits(G); hand.apply_edits(G)
    if hand.MISSES:
        print(f'  {A["id"]}: {len(hand.MISSES)} edits found nothing, e.g.', hand.MISSES[0]['what'])
    print(f'  {A["id"]}: clean-up (cut back, gone, scraps)', autoclean.clean(G, 'hub'), '| buildings now', len(G['buildings']['hub']))
    ALL += E


def join_floating(G, d):
    """Cut-off street groups joined to the nearest way that reaches a main road (autoclean.join, which the bake runs again), as edits."""
    return [{'op': 'add street', 'kind': 'lane' if k == 'lanes' else 'street', 'pts': pts,
             'note': 'Gidi link: this group reached no main road once all the areas were in', 'by_who': 'Claude, 21 Oct 2026: Ìbùdó, joining up after the areas'}
            for k, pts in autoclean.join(G, d)]


def top_up_reach(G, d, cap=12):
    """Every house needs a school, a place of worship and a chemist within 10 minutes' walk, 15 at most (check 13). Real places come
    from Overture, which misses most small chemists and churches, so once all the areas are in, the house with most others out of
    reach around it becomes one, greedily, until everyone is within 10 minutes or `cap` are added per kind."""
    import walknet
    from shapely.geometry import Point
    R = walknet.Reach(walknet.graph(walknet.ways_of(G, sorted(G['buildings'])), 'walk'))
    homes = [b for b in G['buildings'][d] if b[0] in ('front', 'back', 'stilt')]
    H = [Polygon(b[1:]).centroid for b in homes]
    NAMES = {'chemist': ['Healthway Chemist', 'Sure Cure Chemist', 'Good Health Chemist', 'Life Spring Pharmacy', 'Alaafia Chemist', 'Mama Bisi Chemist'],
             'church': ['Living Waters Chapel', 'Grace Harvest Church', 'New Dawn Church', 'Mount Zion Assembly'],
             'mosque': ['Central Jumat Mosque', 'Nurudeen Mosque', 'Ansar Mosque'], 'school': ['Ayo Kids Academy', 'Morning Star School', 'Unity Nursery']}
    E_ = []
    for kind, types in (('chemist', {'chemist', 'clinic', 'hospital'}), ('church', {'church', 'mosque'}), ('school', {'school'})):
        for k in range(cap):
            d0 = R.from_points([Point(p['x'], p['y']) for p in G['pois'] if p['type'] in types], 1251)
            t = [R.to_point(d0, h) for h in H]
            out = [i for i, x in enumerate(t) if x > 833]
            if not out:
                break
            def gain(i):
                di = R.from_points([H[i]], 834)
                return sum(1 for j in out if H[j].distance(H[i]) < 834 and R.to_point(di, H[j]) <= 833)
            i = max(sorted(out, key=lambda i: -t[i])[::max(1, len(out) // 40)][:40], key=lambda i: (gain(i), -i))
            name = NAMES[kind][len(E_) % len(NAMES[kind])] + ' %d' % (len(E_) + 1)
            e = {'op': 'add place', 'name': name, 'type': kind, 'x': round(H[i].x), 'y': round(H[i].y),
                 'note': 'Gidi: a house turned %s, so every home has one in reach once all the areas were in' % kind, 'by_who': 'Claude, 21 Oct 2026: Ìbùdó, joining up after the areas'}
            G['pois'].append({'name': name, 'type': kind, 'note': e['note'], 'd': d, 'x': e['x'], 'y': e['y']}); E_.append(e)
    return E_


L_ = join_floating(G, 'hub')
print(len(L_), 'links so every street group reaches a main road')
ALL += L_
P_ = top_up_reach(G, 'hub')
print(len(P_), 'everyday places added so every home has one in reach:', [e['type'] for e in P_])
ALL += P_
os.makedirs('web/hand/gen', exist_ok=True)
json.dump({'district': 'hub', 'layout': 'v2',
           'note': 'GENERATED by scripts/rebuild_areas.py: the Ìbùdó areas built from their real places. Never edit by hand: fixes go in web/hand/hub.json.',
           'edits': ALL}, open('web/hand/gen/hub.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print(len(ALL), 'area edits written to web/hand/gen/hub.json')
