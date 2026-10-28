"""Extra readings for the d27 Somolu-Bariga building study (28 Oct), from d17_blocks.py's JSON.

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d17_blocks.py d27 --json x.json
  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d27_extras.py x.json

Prints: whole-district storeys and footprint shares; the blocks over 100,000 m2 real (where Overture has too few
streets to cut real blocks); the Overture printing_service places per block (named ones only: d17_blocks keeps
place_names only where a name exists); our cover against Google's by fabric (the rule draft with overrides); and how
many blocks of each size band sit at or above Google's cover.
"""
import collections
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_fabric as F  # noqa: E402

R = json.load(open(sys.argv[1]))['d27']
S, B = R['summary'], R['blocks']
W = S['whole']

print('whole: n90', W['n90'], 'cover90', W['cover90'], 'median_m2', W['median_m2'], 'p90', W['p90_m2'],
      'under40', W['n_under_40m2'], f"({W['n_under_40m2'] / W['n90']:.1%})", 'over500', W['n_over_500m2'])
st = {int(k): v for k, v in W['storeys'].items()}
tot = sum(st.values())
print('storeys read', tot, {k: f'{v} ({v / tot:.1%})' for k, v in sorted(st.items())})
print('ours', W['ours_n'], W['ours_cover'], W['ours_storeys'], 'carriageway', W['ours_carriageway_share'])
print('blocks', len(B), 'median block cover google', statistics.median(b['cover90'] for b in B),
      'ours', statistics.median(b['ours_cover'] for b in B),
      'blocks ours >= google', sum(b['ours_cover'] >= b['cover90'] for b in B))

print('\nblocks over 100,000 m2 real:')
big = [b for b in B if b['area_real_m2'] >= 100000]
for b in sorted(big, key=lambda b: -b['area_real_m2']):
    print(' ', b['block'], b['centroid_gidi'], b['area_real_m2'], b['n90'])
print(f"  {len(big)} blocks, {sum(b['area_real_m2'] for b in big) / S['outline_real_m2']:.1%} of the outline, "
      f"{sum(b['n90'] for b in big)} of {W['n90']} buildings")

print('\nprinting_service places (named) per block:')
pr = collections.Counter()
for b in B:
    n = sum(1 for c, _ in b['place_names'] if c == 'printing_service')
    if n:
        pr[b['block']] = n
cen = {b['block']: b['centroid_gidi'] for b in B}
print('  named printing places in blocks', sum(pr.values()), 'in', len(pr), 'blocks; whole-district category count',
      dict(W['place_cats']).get('printing_service'))
xs = [cen[k][0] for k, v in pr.items() for _ in range(v)]
ys = [cen[k][1] for k, v in pr.items() for _ in range(v)]
print('  median Gidi x, y of them', statistics.median(xs), statistics.median(ys))
inbox = sum(v for k, v in pr.items() if 13350 <= cen[k][0] <= 13650 and 5400 <= cen[k][1] <= 5750)
print('  in the box x 13350-13650, y 5400-5750 (Gidi):', inbox)
for k, v in pr.most_common(10):
    print('  ', k, cen[k], v)

print('\nby fabric (rule draft + overrides): blocks, real km2, google cover, ours cover (area-weighted)')
agg = collections.defaultdict(lambda: [0, 0.0, 0.0, 0.0])
for b in B:
    f = F.fabric(b)[0].split(':')[0]
    a = agg[f]
    a[0] += 1
    a[1] += b['area_real_m2']
    a[2] += b['cover90'] * b['area_real_m2']
    a[3] += b['ours_cover'] * b['area_real_m2']
for f, (n, ar, g, o) in sorted(agg.items(), key=lambda kv: -kv[1][1]):
    print(f'  {f}: {n} blocks, {ar / 1e6:.2f} km2, google {g / ar:.0%}, ours {o / ar:.0%}')

print('\nsmall footprints (under 40 m2) share, blocks with 100+ buildings, top 8:')
sm = sorted((b for b in B if b['n90'] >= 100), key=lambda b: -b['n_under_40m2'] / b['n90'])
for b in sm[:8]:
    print(' ', b['block'], b['centroid_gidi'], b['n90'], f"{b['n_under_40m2'] / b['n90']:.0%}", b['median_m2'],
          'on water px', b['on_water_pixel'])
