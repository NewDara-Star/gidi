"""The clean-up after a real-area build, written as hand edits (owner: "clean up everything by hand"): reads the baked map and writes
hand edits into web/hand/<district>.json for every building the checks would flag (scripts/autoclean.py says how each is fixed).
Districts built again from their real places (web/hand/gen/) are cleaned up in the bake itself; this is for the others.
Usage: python3 scripts/hand_fix_checks.py hub "<who>"
"""
import json
import sys

from shapely.geometry import LineString

sys.path.insert(0, 'scripts')
import autoclean

D = sys.argv[1]
WHO = sys.argv[2] if len(sys.argv) > 2 else 'Claude: clean-up after the checks'
G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
B = G['buildings'][D]
acts, scraps = autoclean.plan(G, D)
E = []
for i, Q, why in acts:
    P = autoclean._valid(B[i]); at = autoclean.R(P.representative_point().coords[0])
    if Q is None:
        E.append({'op': 'delete building', 'at': at, 'kind': B[i][0], 'note': why, 'by_who': WHO})
    else:
        E.append({'op': 'reshape building', 'at': at, 'kind': B[i][0], 'pts': autoclean.ring_pts(Q), 'note': why, 'by_who': WHO})
for i in scraps:
    E.append({'op': 'delete street', 'at': autoclean.R(LineString(G['streets'][D][i]).interpolate(0.5, normalized=True).coords[0]), 'note': 'a scrap of street leading nowhere', 'by_who': WHO})
path = f'web/hand/{D}.json'
H = json.load(open(path))
H['edits'] = H.get('edits', []) + E
json.dump(H, open(path, 'w'), separators=(',', ':'), ensure_ascii=False)
print(D, len(E), 'edits:', sum(1 for _, q, _ in acts if q is not None), 'cut back,', sum(1 for _, q, _ in acts if q is None), 'gone')
