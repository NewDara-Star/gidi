"""Generate the whole city as tiles, in parallel Blender processes, and write the manifest.

python3 blender/city_run.py [--jobs 8] [--size 400] [--detail full,web] [--only 6,10;7,10]

Outputs web/city/<detail>/tiles/<tx>_<ty>.glb (+ .json with what was built and the signs), and
web/city/manifest.json: tile size, which tiles exist at which detail, and every gap found (data
kinds with no builder, builder errors) so the kit can be extended. web/city/ is not committed.
"""
import json
import math
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
opt = {}
for i, a in enumerate(args):
    if a.startswith('--'):
        opt[a] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('--') else True
JOBS = int(opt.get('--jobs', 8))
SIZE = float(opt.get('--size', 400))
DETAILS = str(opt.get('--detail', 'full,web')).split(',')
OUT = os.path.join(ROOT, 'web', 'city')

gd = open(os.path.join(ROOT, 'web', 'gidi-data.js')).read()
gd = json.loads(gd[gd.index('{'):gd.rindex('}') + 1])


def tiles_needed():
    """Every tile that holds a building, a road, a parcel or a structure."""
    t = set()
    add = lambda x, y: t.add((int(x // SIZE), int(y // SIZE)))
    for lst in gd['buildings'].values():
        for b in lst:
            add(sum(p[0] for p in b[1:]) / 4, sum(p[1] for p in b[1:]) / 4)
    lines = [ln for v in (gd.get('streets', {}), gd.get('lanes', {}), gd.get('paths', {})) for lst in v.values() for ln in lst]
    lines += [m['pts'] for m in gd.get('mains', [])] + [a['pts'] for a in gd.get('arterials', [])] + [s['pts'] for s in gd.get('structures', [])] + [gd['rail']['pts']]
    for ln in lines:
        for i in range(len(ln) - 1):
            a, b = ln[i], ln[i + 1]
            n = max(1, int(math.dist(a, b) / (SIZE / 4)))
            for k in range(n + 1):
                add(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
    for lst in gd['parcels'].values():
        for p in lst:
            add(sum(q[0] for q in p['pts']) / len(p['pts']), sum(q[1] for q in p['pts']) / len(p['pts']))
    W, H = gd['size'][0], 6720.0
    return sorted(k for k in t if 0 <= k[0] <= W // SIZE and 0 <= k[1] <= H // SIZE)  # only the map: stray points in the data are not tiles


if __name__ == '__main__':
    if opt.get('--only'):
        todo = [tuple(int(v) for v in s.split(',')) for s in opt['--only'].split(';')]
    else:
        todo = tiles_needed()
    print(len(todo), 'tiles', DETAILS, flush=True)
    t0 = time.time()
    for det in DETAILS:
        out = os.path.join(OUT, det)
        os.makedirs(os.path.join(out, 'tiles'), exist_ok=True)
        # the POI overrides are computed once, before the workers start
        subprocess.run(['blender', '-b', '--factory-startup', '-P', os.path.join(ROOT, 'blender', 'city.py'), '--', '--tiles', '', '--out', out, '--detail', det, '--size', str(SIZE)], capture_output=True)
        left = [t for t in todo if not os.path.exists(os.path.join(out, 'tiles', f'{t[0]}_{t[1]}.json'))]  # resumable
        chunks = [left[i::JOBS] for i in range(JOBS)]
        procs = []
        for c in chunks:
            if not c:
                continue
            log = open(os.path.join(out, f'log_{len(procs)}.txt'), 'w')
            procs.append(subprocess.Popen(['blender', '-b', '--factory-startup', '-P', os.path.join(ROOT, 'blender', 'city.py'), '--',
                                           '--tiles', ';'.join(f'{a},{b}' for a, b in c), '--out', out, '--detail', det, '--size', str(SIZE)], stdout=log, stderr=subprocess.STDOUT))
        while any(p.poll() is None for p in procs):
            done = len([f for f in os.listdir(os.path.join(out, 'tiles')) if f.endswith('.json')])
            print(f'{det}: {done}/{len(todo)} tiles, {int(time.time() - t0)} s', flush=True)
            time.sleep(30)
    # manifest
    present = [d for d in ('full', 'web') if os.path.isdir(os.path.join(OUT, d, 'tiles'))]
    man = dict(size=SIZE, details=present, tiles={}, gaps={}, errors=[])
    for det in present:
        for f in os.listdir(os.path.join(OUT, det, 'tiles')):
            if not f.endswith('.json'):
                continue
            info = json.load(open(os.path.join(OUT, det, 'tiles', f)))
            key = f"{info['tx']}_{info['ty']}"
            man['tiles'].setdefault(key, {})[det] = dict(faces=info['faces'], bytes=info['bytes'], signs=info.get('signs', 0))
            for k, v in info['built'].items():
                if k.startswith('unknown:') or k.endswith(':missing'):
                    man['gaps'][k] = man['gaps'].get(k, 0) + v
                if k.startswith('error:'):
                    man['errors'].append(dict(tile=key, detail=det, kind=k, n=v))
    json.dump(man, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
    print('DONE', len(man['tiles']), 'tiles; gaps', man['gaps'], 'errors', len(man['errors']), int(time.time() - t0), 's')
