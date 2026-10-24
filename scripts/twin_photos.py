"""Street twins' pictures for one built area of a child district (docs/hand/<dir>/twins/<area>.json).
  plan:   python3 scripts/twin_photos.py plan ibudo <area>    -> ~/gidi-data/research/google/<dir>/twins/<area>/PLAN.json (Street View points every 40 m, both ways)
  attach: python3 scripts/twin_photos.py attach ibudo <area>  -> reads that folder's INDEX.tsv, lists each street's pictures in the twins file (amber)
Pictures stay outside the repo (study only)."""
import csv
import json
import math
import os
import sys

from shapely.geometry import LineString

CMD, D, AREA = sys.argv[1:4]
TW = f'docs/hand/{D}/twins/{AREA}.json'
OUT = os.path.expanduser(f'~/gidi-data/research/google/{D}/twins/{AREA}')
T = json.load(open(TW))
(LA0, LO0), (GX0, GY0) = T['anchor_real'], T['anchor_gidi']
inv = lambda x, y: (LA0 - (y - GY0) / 110600, LO0 + (x - GX0) / 109900)
if CMD == 'plan':
    os.makedirs(OUT, exist_ok=True)
    plan = []
    for i, s in enumerate(T['streets']):
        if s['kind'] == 'path':
            continue
        g = LineString(s['gidi']); n = max(1, int(g.length // 40)); shots = []
        for k in range(n + 1):
            d = k * g.length / n
            a, b = g.interpolate(max(0, d - 1)), g.interpolate(min(g.length, d + 1))
            hdg = math.degrees(math.atan2(b.x - a.x, -(b.y - a.y))) % 360   # the map's y runs south: north-up heading
            la, lo = inv(*g.interpolate(d).coords[0])
            shots.append({'lat': round(la, 6), 'lon': round(lo, 6), 'heading': [round(hdg), round((hdg + 180) % 360)]})
        plan.append({'n': i, 'real_name': s['real_name'], 'kind': s['kind'], 'length_m': s['length_m'], 'shots': shots})
    json.dump(plan, open(f'{OUT}/PLAN.json', 'w'), indent=0)
    print(len(plan), 'streets,', sum(len(p['shots']) * 2 for p in plan), 'pictures ->', OUT)
else:
    rows = list(csv.DictReader(open(f'{OUT}/INDEX.tsv'), delimiter='\t'))
    by = {}
    for r in rows:
        f = r.get('file', '-')
        if f and f != '-':
            by.setdefault(int(r['n']), []).append(os.path.relpath(os.path.join(OUT, os.path.basename(f)), os.path.expanduser('~/gidi-data/research')))
    for i, s in enumerate(T['streets']):
        s['pics'] = sorted(set(by.get(i, [])))
        if s['pics'] and s['status'] == 'red':
            s['status'] = 'amber'
    json.dump(T, open(TW, 'w'), ensure_ascii=False, indent=0)
    print(sum(1 for s in T['streets'] if s['pics']), 'of', len(T['streets']), 'streets have pictures')
