# Freeze a district: write everything it owns in the baked map (scripts/hand.py: snapshot) into web/hand/<id>.json, so from
# now on the bake loads it as it is and only hand edits change it. Run after a bake.
# Usage: python3 scripts/freeze_district.py foodgate
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import hand
d = sys.argv[1]
G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
path = f'web/hand/{d}.json'
H = json.load(open(path)) if os.path.exists(path) else {'district': d, 'layout': hand.LAYOUT, 'edits': []}
if H.get('layout', 'v1') != hand.LAYOUT:   # a file from the old frame stays as a record; the district's current file is <id>-v2.json
    path = f'web/hand/{d}-{hand.LAYOUT}.json'
    H = json.load(open(path)) if os.path.exists(path) else {'district': d, 'layout': hand.LAYOUT, 'edits': []}
H['layout'] = hand.LAYOUT
H.pop('frozen', None)
H['snapshot'] = hand.snapshot(G, d)
# the edits made so far are in the snapshot now: filed as applied, so the next bake doesn't make them a second time
H['applied'] = H.get('applied', []) + H.get('edits', [])
H['edits'] = []
H.setdefault('log', []).append('frozen from the bake (scripts/freeze_district.py); edits so far filed under "applied"')
H['note'] = 'The whole district, frozen from the bake; change it only with hand edits (scripts/hand.py).'
json.dump(H, open(path, 'w'), separators=(',', ':'))
print(path, {k: len(v) for k, v in H['snapshot'].items() if isinstance(v, list)})
