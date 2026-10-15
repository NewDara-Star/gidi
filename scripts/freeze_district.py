# Freeze a district: write everything it owns in the baked map (scripts/hand.py: snapshot) into web/hand/<id>.json, so from
# now on the bake loads it as it is and only hand edits change it. Run after a bake.
# Usage: python3 scripts/freeze_district.py foodgate
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import hand
d = sys.argv[1]
G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
path = f'web/hand/{d}.json'
H = json.load(open(path)) if os.path.exists(path) else {'district': d, 'edits': []}
H.pop('frozen', None)
H['snapshot'] = hand.snapshot(G, d)
H['note'] = 'The whole district, frozen from the bake; change it only with hand edits (scripts/hand.py).'
json.dump(H, open(path, 'w'), separators=(',', ':'))
print(path, {k: len(v) for k, v in H['snapshot'].items() if isinstance(v, list)})
