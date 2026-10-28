"""How well a drawn district's roads sit on the real main roads (owner, 28 Oct: "if the stuff I've done earlier is
correct... all our districts that we have done already, their roads should line up to the new roads now perfectly").

The real main roads are Overture's segments of class motorway, trunk, primary and secondary (OpenStreetMap's lines),
put into the Gidi frame (working_bar.gidi, 1:3). Each is sampled every STEP Gidi metres inside the district's outline,
and each sample is measured against our roads there:
  - on: the sample lies on one of our roads' paved width (its centreline buffered by half its width, plus TOL);
  - off: our nearest road centreline is further, the distance printed;
  - a run of off samples longer than GAP m is listed as a stretch where our map has no road on the real line.
A dual carriageway is two Overture lines a few metres apart; ours is often one road with a median, so both fall on
its width. Overture's lines are where OpenStreetMap's mappers put them, a few metres off the true centre in places:
the on share is a measure, not a verdict, and each listed stretch is read on Google before it is called a gap.

  ~/.venvs/gidi/bin/python -I scripts/main_road_fit.py d15            one district
  ~/.venvs/gidi/bin/python -I scripts/main_road_fit.py all            every drawn district, a line each
"""
import json
import os
import sys
from collections import defaultdict

import pyarrow.parquet as pq
import shapely
from pyproj import Transformer
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from working_bar import gidi   # noqa: E402

SEG = os.path.expanduser('~/gidi-data/research/data/overture-lagos/lagos_overture_segment.parquet')
MAIN = ('motorway', 'trunk', 'primary', 'secondary')
STEP = 3.0      # Gidi m between samples
TOL = 1.0       # Gidi m past our paved edge still counted on
GAP = 30.0      # Gidi m of off samples in a row listed as a stretch


def real_main(T):
    t = pq.read_table(SEG, columns=['subtype', 'class', 'geometry']).to_pylist()
    out = []
    for r in t:
        if r['subtype'] == 'road' and r['class'] in MAIN:
            g = shapely.from_wkb(r['geometry'])
            out.append((r['class'], LineString([gidi(x, y, T) for x, y in g.coords])))
    return out


def fit(d, real):
    ring = Polygon(json.load(open(os.path.join(ROOT, 'map', d, 'district.json')))['records'][0]['outline'][0])
    roads = [r for r in json.load(open(os.path.join(ROOT, 'map', d, 'plan.json')))['records'] if r.get('type') == 'road']
    lines = [LineString([q[:2] for q in r['centreline']]) for r in roads]
    paved = unary_union([L.buffer(float(r['width']) / 2 + TOL, cap_style=2) for L, r in zip(lines, roads)])
    allc = unary_union(lines)
    by = defaultdict(lambda: [0, 0])
    offd, stretches = [], []
    for cls, L in real:
        if not L.intersects(ring):
            continue
        I = L.intersection(ring)
        for part in getattr(I, 'geoms', [I]):
            if part.geom_type != 'LineString' or part.length < STEP:
                continue
            run = []
            n = int(part.length // STEP) + 1
            for k in range(n):
                p = part.interpolate(k * STEP)
                ok = paved.contains(p)
                by[cls][0 if ok else 1] += 1
                if ok:
                    if len(run) * STEP >= GAP:
                        stretches.append((cls, len(run) * STEP, run[0], run[-1]))
                    run = []
                else:
                    offd.append(allc.distance(p))
                    run.append((round(p.x), round(p.y)))
            if len(run) * STEP >= GAP:
                stretches.append((cls, len(run) * STEP, run[0], run[-1]))
    on = sum(v[0] for v in by.values())
    tot = on + sum(v[1] for v in by.values())
    return ring, by, on, tot, sorted(offd), sorted(stretches, key=lambda s: -s[1])


def main():
    arg = sys.argv[1]
    T = Transformer.from_crs(4326, 32631, always_xy=True)
    real = real_main(T)
    ds = sorted(x for x in os.listdir(os.path.join(ROOT, 'map')) if x.startswith('d') and x != 'd00') if arg == 'all' else [arg]
    for d in ds:
        ring, by, on, tot, offd, st = fit(d, real)
        if not tot:
            print(f'{d}: no real main road inside the outline')
            continue
        med = offd[len(offd) // 2] if offd else 0
        line = (f'{d}: real main roads {tot * STEP / 1000:.2f} km Gidi inside; on our paved roads {on / tot:.0%}; '
                f'off {tot - on} samples, median {med:.1f} m from our nearest centreline; '
                f'{len(st)} stretches of {GAP:.0f} m+ with no road on the real line ({sum(s[1] for s in st):.0f} m)')
        print(line)
        if arg != 'all':
            for cls, (a, b) in sorted(by.items()):
                print(f'   {cls}: {a / (a + b):.0%} on of {(a + b) * STEP:.0f} m')
            for cls, length, p0, p1 in st:
                print(f'   stretch {cls} {length:.0f} m from {p0} to {p1}')


if __name__ == '__main__':
    main()
