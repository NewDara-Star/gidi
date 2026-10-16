# One calibration pass (docs/DEEP-STUDY.md): each district's own miss against its study (docs/data/deep-check/<id>.json, written by
# scripts/deep_check.py) scales its own settings, and the result goes to web/deep-tune.json, which district_profiles applies last.
# Run it after a build and its checks, rebuild, check again. Not a search: one proportional step per run, so it can't wander.
#   buildings per km2 too high  -> more plots left empty        ground built over too high -> less infill
#   touching too low            -> more houses wall to wall     too many streets           -> streets further apart
#   too square to the street    -> more wobble                  too many small buildings   -> fewer small rooms and shacks
#   houses too big or too small -> plots narrower or wider
# A district with fewer than 5 built squares has too small a sample: only its streets are tuned.
# Usage: python3 scripts/deep_tune.py [ids...]
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from district_profiles import profile

clamp = lambda v, lo, hi: max(lo, min(hi, v))
step = lambda old, new: old * clamp(new / old, 0.67, 1.5) if old else new   # no setting moves more than half again in one pass
T = json.load(open('web/deep-tune.json')) if os.path.exists('web/deep-tune.json') else {}
ids = sys.argv[1:] or sorted(f[:-5] for f in os.listdir('docs/data/deep-check') if f.endswith('.json'))
for did in ids:
    C = json.load(open(f'docs/data/deep-check/{did}.json'))
    M = C['measures']
    ratio = lambda k: (M[k]['gidi'] / M[k]['real']) if M.get(k) and M[k]['gidi'] and M[k]['real'] else None
    P = profile(did, json.load(open(f'study-{did}.json')))   # the settings in force now, tune included
    t = dict(T.get(did, {}))
    if C['squares'] >= 5:
        r = ratio('buildings per km2 (built squares)')
        if r:
            t['vacant'] = round(clamp(step(P.get('vacant', 0.07), 1 - (1 - P.get('vacant', 0.07)) / r ** 0.8), 0.01, 0.75), 3)
        r = ratio('ground built over')
        if r:
            t['block_fill'] = round(clamp(step(P['infill']['block_fill'], P['infill']['block_fill'] / r), 0.05, 0.85), 3)
        g, real = (M.get('touching') or {}).get('gidi'), (M.get('touching') or {}).get('real')
        if g is not None and real:
            t['touch'] = round(clamp(P['touch'] + clamp(0.8 * (real - g), -0.15, 0.15), 0.1, 0.95), 3)
        r = ratio('under 40 m2')
        if r:
            t['small_share'] = round(clamp(step(P['infill']['small_share'], P['infill']['small_share'] / r), 0.02, 0.7), 3)
        r = ratio('line to the street, deg')
        if r:
            t['wobble_deg'] = round(clamp(step(P['wobble_deg'], P['wobble_deg'] / max(r, 0.25)), 2, 15), 1)
        r = ratio('footprint median m2')
        if r:   # house size apart from density: plots narrower or wider (a footprint scales with the plot's width, roughly squared)
            t['size_scale'] = round(clamp(step(P.get('size_scale', 1.0), P.get('size_scale', 1.0) / r), 0.4, 2.5), 3)
    r = ratio('drivable km per km2 (whole land)')
    if r and abs(r - 1) > 0.1:   # parallel streets further apart (cross-street spacing barely moves it: pass 1, 16 Oct)
        t['rib_scale'] = round(clamp(step(P.get('rib_scale', 1.0), P.get('rib_scale', 1.0) * r), 0.5, 3.0), 3)
    T[did] = t
    print(did, t)
json.dump(T, open('web/deep-tune.json', 'w'), indent=1, sort_keys=True)
