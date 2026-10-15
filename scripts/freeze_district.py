# Freeze a district: write what the bake generated for it (market-street tables and zones, street furniture) into its hand
# file web/hand/<id>.json, so from now on only hand edits change them (scripts/hand.py). Run after a bake.
# Usage: python3 scripts/freeze_district.py foodgate
import json, os, sys
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
d = sys.argv[1]
G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
P = Polygon([x for x in G['districts'] if x['id'] == d][0]['poly'][0])
zones = [z for z in G.get('encroach', []) if z.get('d') == d and z['kind'] == 'market street']
Z = unary_union([Polygon(z['pts']).buffer(0) for z in zones]).buffer(0.1) if zones else None
tables = [b[1:] for b in G['buildings'][d] if b[0] == 'stalls' and Z is not None and Z.contains(Polygon(b[1:]).buffer(0))]
furn = [f for f in G.get('furniture', []) if P.buffer(40).contains(Point(f['x'], f['y']))]
path = f'web/hand/{d}.json'
H = json.load(open(path)) if os.path.exists(path) else {'district': d, 'edits': []}
H['frozen'] = {'tables': tables, 'encroach': [{'kind': z['kind'], 'pts': z['pts']} for z in zones], 'furniture': furn}
H['note'] = 'Frozen from the bake; change by hand edits only (scripts/hand.py).'
json.dump(H, open(path, 'w'), separators=(',', ':'))
print(path, len(tables), 'tables,', len(zones), 'zones,', len(furn), 'pieces of furniture')
