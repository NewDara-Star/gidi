"""Generate the whole city as tiles, in parallel Blender processes, and write the manifest.

python3 blender/city_run.py [--jobs 8] [--size 400] [--detail web] [--only 6,10;7,10] [--fresh] [--terrain]

--detail: "web" (the light build, the default) or "full,web". The browser view is a quick preview and loads only the light
tiles (owner, 16 Oct: "the full scene can be viewed in Unreal"); full tiles are for close test renders.

--terrain stands every tile on the ground heights (web/terrain.json), as the slice renders do.

--fresh rebuilds every tile, overwriting the old ones (otherwise a tile already built is skipped).

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
DETAILS = str(opt.get('--detail', 'web')).split(',')
OUT = os.path.join(ROOT, 'web', 'city')

gd = open(os.path.join(ROOT, 'web', 'gidi-data.js')).read()
gd = json.loads(gd[gd.index('{'):gd.rindex('}') + 1])


def tiles_needed():
    """Every tile that holds a building, a road, a parcel, a structure or a ferry route."""
    t = set()
    add = lambda x, y: t.add((int(x // SIZE), int(y // SIZE)))
    for lst in gd['buildings'].values():
        for b in lst:
            add(sum(p[0] for p in b[1:]) / 4, sum(p[1] for p in b[1:]) / 4)
    lines = [ln for v in (gd.get('streets', {}), gd.get('lanes', {}), gd.get('paths', {})) for lst in v.values() for ln in lst]
    lines += [m['pts'] for m in gd.get('mains', [])] + [a['pts'] for a in gd.get('arterials', [])] + [s['pts'] for s in gd.get('structures', [])] + [gd['rail']['pts']] + [f['pts'] for f in gd.get('ferries', [])]  # the ferry routes, so the boats on them have tiles
    for ln in lines:
        for i in range(len(ln) - 1):
            a, b = ln[i], ln[i + 1]
            n = max(1, int(math.dist(a, b) / (SIZE / 4)))
            for k in range(n + 1):
                add(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
    for lst in gd['parcels'].values():
        for p in lst:
            add(sum(q[0] for q in p['pts']) / len(p['pts']), sum(q[1] for q in p['pts']) / len(p['pts']))
    W, H = gd['size']   # the whole map (v1 hard-coded 6720 m here, which cut v2's Atlantic coast off)
    return sorted(k for k in t if 0 <= k[0] <= W // SIZE and 0 <= k[1] <= H // SIZE)  # only the map: stray points in the data are not tiles


if __name__ == '__main__':
    if opt.get('--only'):
        todo = [tuple(int(v) for v in s.split(',')) for s in opt['--only'].split(';')]
    else:
        todo = tiles_needed()
    print(len(todo), 'tiles', DETAILS, flush=True)
    t0 = time.time()
    FRESH = bool(opt.get('--fresh'))
    built = lambda out, t: (lambda f: os.path.exists(f) and (not FRESH or os.path.getmtime(f) >= t0))(os.path.join(out, 'tiles', f'{t[0]}_{t[1]}.json'))
    MISSING = {}
    for det in DETAILS:
        out = os.path.join(OUT, det)
        os.makedirs(os.path.join(out, 'tiles'), exist_ok=True)
        # the POI overrides are computed once, before the workers start
        subprocess.run(['blender', '-b', '--factory-startup', '-P', os.path.join(ROOT, 'blender', 'city.py'), '--', '--tiles', '', '--out', out, '--detail', det, '--size', str(SIZE)] + (['--terrain'] if opt.get('--terrain') else []), capture_output=True)
        # a pool of short-lived workers: each Blender process builds a small batch and exits, so its
        # memory is freed (a full tile peaks at ~3.5 GB and Blender keeps growing across tiles; two
        # long-lived full workers got killed on a 16 GB machine). A batch that dies loses only itself;
        # its tiles are retried once, and anything still missing is reported.
        batch = 3 if det == 'full' else 12
        for attempt in (1, 2):
            left = [t for t in todo if not built(out, t)]  # resumable
            if not left:
                break
            queue = [left[i:i + batch] for i in range(0, len(left), batch)]
            procs, n = [], 0
            last = 0
            while queue or any(p.poll() is None for p in procs):
                procs = [p for p in procs if p.poll() is None]
                while queue and len(procs) < JOBS:
                    c = queue.pop(0)
                    log = open(os.path.join(out, f'log_{n % 50}.txt'), 'w')
                    n += 1
                    procs.append(subprocess.Popen(['blender', '-b', '--factory-startup', '-P', os.path.join(ROOT, 'blender', 'city.py'), '--',
                                                   '--tiles', ';'.join(f'{a},{b}' for a, b in c), '--out', out, '--detail', det, '--size', str(SIZE)], stdout=log, stderr=subprocess.STDOUT))
                if time.time() - last > 30:
                    last = time.time()
                    done = len([t for t in todo if built(out, t)])
                    print(f'{det}: {done}/{len(todo)} tiles, {int(time.time() - t0)} s', flush=True)
                time.sleep(2)
        missing = [t for t in todo if not built(out, t)]
        MISSING[det] = len(missing)
        if missing:
            print(f'{det}: MISSING {len(missing)} tiles after a retry: ' + ';'.join(f'{a},{b}' for a, b in missing), flush=True)
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
    print('DONE' if not any(MISSING.values()) else 'INCOMPLETE', len(man['tiles']), 'tiles; missing', MISSING, 'gaps', man['gaps'], 'errors', len(man['errors']), int(time.time() - t0), 's')
