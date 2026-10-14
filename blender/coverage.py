"""Writes docs/look/COVERAGE.md: every kind of thing in Gidi's data, how many, where, and whether
the kit can build it yet. Plain Python (no Blender): python3 blender/coverage.py"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
reg = open(os.path.join(ROOT, 'blender', 'gidi_kit', 'registry.py')).read()


def section(name):
    m = re.search(name + r' = \{(.*?)\n\}', reg, re.S)
    return set(re.findall(r"'([^']+)':\s*(?:archetypes|kinds|places)\.", m.group(1))) if m else set()


done = {k: section(k) for k in ('BUILDINGS', 'STRUCTURES', 'CIVIC_PLOTS')}
pb = open(os.path.join(ROOT, 'blender', 'gidi_kit', 'parcels.py')).read()
done['PARCELS'] = set(re.findall(r"'([^']+)':\s*(?:lambda|[a-z_]+[,\n])", pb[pb.index('BUILDERS = {'):]))
done['STRUCTURES'] = {'flyover', 'skywalk', 'footbridge', 'jetty', 'ramp'}
done['CIVIC'] = done.pop('CIVIC_PLOTS') | set(re.findall(r"'([^']+)':\s*places\.", reg[reg.index('POI_PLACES'):])) | {'cemetery', 'sport', 'market', 'transit'}
tables = {'BUILDINGS': {}, 'PARCELS': {}, 'STRUCTURES': {}, 'CIVIC': {}}
for f in sorted(glob.glob(os.path.join(ROOT, 'web', 'gen-*.json'))):
    d = json.load(open(f))
    dist = os.path.basename(f)[4:-5]
    for b in d['buildings']:
        tables['BUILDINGS'].setdefault(b[0], {}).setdefault(dist, 0)
        tables['BUILDINGS'][b[0]][dist] += 1
    for p in d.get('parcels', []):
        tables['PARCELS'].setdefault(p['kind'], {}).setdefault(dist, 0)
        tables['PARCELS'][p['kind']][dist] += 1
    for s in d.get('structures', []):
        tables['STRUCTURES'].setdefault(s['kind'], {}).setdefault(dist, 0)
        tables['STRUCTURES'][s['kind']][dist] += 1
civ = json.load(open(os.path.join(ROOT, 'web', 'civic.json')))
for dist, items in civ['key'].items():
    for it in items:
        tables['CIVIC'].setdefault(it['type'], {}).setdefault(dist, 0)
        tables['CIVIC'][it['type']][dist] += 1
for dist, counts in civ['counts'].items():
    for t, n in zip(civ['_counts_order'], counts):
        tables['CIVIC'].setdefault(t, {}).setdefault(dist, 0)
        tables['CIVIC'][t][dist] += n

out = ['# Kit coverage: everything in Gidi\'s data, and whether the kit builds it', '',
       'Made by `python3 blender/coverage.py` from `web/gen-*.json`, `web/civic.json` and `blender/gidi_kit/registry.py`. Do not edit by hand.', '']
total = built = 0
for name, title in (('BUILDINGS', 'Building kinds'), ('PARCELS', 'Parcels (plots and grounds)'), ('STRUCTURES', 'Structures'), ('CIVIC', 'Civic places')):
    out += [f'## {title}', '', '| Kind | Count | Districts | Built by the kit |', '|---|---|---|---|']
    for k, v in sorted(tables[name].items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(v.values())
        ok = k in done[name]
        total += 1
        built += ok
        out.append(f"| {k} | {n} | {', '.join(f'{d} {c}' for d, c in sorted(v.items(), key=lambda x: -x[1]))} | {'yes' if ok else '—'} |")
    out.append('')
out.insert(4, f'**{built} of {total} kinds built.**\n')
open(os.path.join(ROOT, 'docs', 'look', 'COVERAGE.md'), 'w').write('\n'.join(out))
print(built, 'of', total)
