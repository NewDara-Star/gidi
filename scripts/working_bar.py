"""A district against the working bar (DECISIONS "Every district to working first", owner 26 Oct): the bar is roads at
real widths on their real lines, houses with a kind and storeys, the real places, bus stops and motor parks, landmarks
with walls and gates, and the check at 0. This reports each part in numbers and fails on the parts a program can hold:

  check     check_map.py on the district: 0 problems.
  houses    every building has a kind and storeys.
  lines     each road's share of its centreline within LINE_NEAR m of a real street (Overture segments, in Gidi
            metres): a road under LINE_SHARE is listed, and fails unless its note, or its row in the district's STREETS.md,
            says where it was read from (a Google study street missing from Overture, a service road or ramp split off a
            real one).
  places    each real place (Overture places) whose category says what the game uses it for (the same rules as Mùṣá's
            hand pass 55, place_kind below) has a place of that kind within PLACE_NEAR m, or lies inside a market,
            school or motor park drawn whole; a miss fails. A real point on a carriageway is measured from the road's
            edge (half its width more): Gidi places things at 1:3 but draws roads at their full width, so a real
            roadside place's point often falls on the road.
  parks     motor parks and bus stops are counted; none of either fails (every Lagos district has a stop).
  landmarks every plot (a school ground, market, factory: the walled landmarks) has a wall with a gate.

  ~/.venvs/gidi/bin/python scripts/working_bar.py d15 [d09 ...]

Not held here, by eye in the running order: whether the widths were read (BUILDINGS.md and STREETS.md say where), and
which landmarks a district has (a landmark not drawn as a plot is not seen).
"""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
OVERTURE = os.path.expanduser('~/gidi-data/research/data/overture-lagos')
LINE_NEAR, LINE_SHARE = 4.0, 0.5     # m, and the share of a road that must lie that near a real street
PLACE_NEAR = 10.0                     # m from a real place's point to a Gidi place of its kind
GROUNDS = ('market', 'school', 'motor_park')   # places drawn whole: a real place inside one is in it
WRITTEN = re.compile(r'study|google|satellite|split|service road|side road|ramp|bridge|deck|hand pass|z1[789]', re.I)

CHURCH = r'church|ministr|assembl|parish|chapel|rccg|c\.?c\.?c|c\.?a\.?c|cathedral|gospel|tabernacle|christ|evangel|apostolic|baptist|methodist|anglican|catholic|redeem|bethel|cherubim|seraphim|deeper life|winners'
MOSQUE = r'mosque|masjid|jama|islam|ansar|nawair|anwar|muslim'
SCHOOL = r'school|college|academy|nursery|primary|secondary|institute|montessori'
HEALTH = r'hospital|clinic|medical|health|maternity|specialist'


def place_kind(cat, name):
    """A real place's kind in the game from its Overture category and, for the vaguer ones, its name (hand pass 55)."""
    n = name or ''
    if cat == 'christian_place_of_worship': return 'church'
    if cat == 'muslim_place_of_worship': return 'mosque'
    if cat == 'religious_organization':
        if re.search(r'newspaper|times\b|chapter', n, re.I): return None
        return 'mosque' if re.search(MOSQUE, n, re.I) else 'church' if re.search(CHURCH, n, re.I) else None
    if cat in ('place_of_learning', 'high_school', 'elementary_school', 'middle_school', 'preschool'): return 'school'
    if cat in ('education', 'specialty_school', 'college_university') and re.search(SCHOOL, n, re.I): return 'school'
    if cat in ('hospital', 'outpatient_care_facility', 'dental_clinic', 'diagnostics_imaging_or_lab_service',
               'vision_or_eye_care_clinic', 'reproductive_perinatal_and_womens_care'): return 'clinic'
    if cat == 'health_care' and re.search(HEALTH, n, re.I): return 'clinic'
    if cat == 'pharmacy_and_drug_store': return 'chemist'
    if cat == 'bank_or_credit_union': return 'bank'
    if cat == 'gas_station': return 'fuel'
    if cat == 'police_station' or re.search(r'police station', n, re.I): return 'police'
    if cat == 'public_transit_facility_or_service' or re.search(r'bus stop', n, re.I): return 'bus_stop'
    if cat in ('bar', 'lounge'): return 'bar'
    if cat in ('restaurant', 'casual_eatery'): return 'buka'
    if cat == 'automotive_service': return 'garage'
    return None


def gidi(lon, lat, T):
    """Real WGS84 to Gidi metres (UTM 31N, 1:3 from the frame's south-west corner)."""
    u, v = T.transform(lon, lat)
    return (u - 500525) / 3, 10500 - (v - 707825) / 3


def bar(d):
    import pyarrow.parquet as pq
    import shapely
    from pyproj import Transformer
    from shapely.geometry import LineString, MultiPolygon, Point, Polygon
    from shapely.ops import unary_union
    from shapely.strtree import STRtree
    import check_map as C

    top = os.path.join(ROOT, 'map', d)
    if not os.path.isdir(top):
        return {'district': d, 'fails': ['not started (no map/%s)' % d]}, []
    recs = []
    for f in sorted(os.listdir(top)):
        if f.endswith('.json'):
            recs += json.load(open(os.path.join(top, f)))['records']
    D = next(r for r in recs if r['type'] == 'district')
    ring = MultiPolygon([Polygon(o) for o in D['outline']]).buffer(0)
    T = Transformer.from_crs(4326, 32631, always_xy=True)
    R, fails, lines = {}, [], []

    # the whole map is loaded, so a seam junction on a node shared with a neighbour's road reads as joined; only this
    # district's own problems count
    del C.errors[:]
    C.check(os.path.join(ROOT, 'map'))
    bad = [e for e in C.errors if e.startswith(d + '/') and not C.TODO.search(e)]
    R['check problems'] = len(bad)
    if bad:
        fails.append(f'check: {len(bad)} problems (check_map.py)')

    B = [r for r in recs if r['type'] == 'building']
    nok = [b['id'] for b in B if not b.get('kind') or not isinstance(b.get('storeys'), int) or b['storeys'] < 1]
    R['houses'], R['houses without kind or storeys'] = len(B), len(nok)
    if nok:
        fails.append(f'houses: {len(nok)} without a kind or storeys, e.g. {nok[:3]}')

    # real lines: Overture segments near the district, in Gidi metres
    minx, miny, maxx, maxy = ring.buffer(200).bounds
    inv = Transformer.from_crs(32631, 4326, always_xy=True)
    (w, n), (e, s) = inv.transform(500525 + 3 * minx, 707825 + 3 * (10500 - miny)), inv.transform(500525 + 3 * maxx, 707825 + 3 * (10500 - maxy))
    seg = pq.read_table(os.path.join(OVERTURE, 'lagos_overture_segment.parquet'), columns=['subtype', 'geometry', 'bbox'])
    real = []
    for r in seg.to_pylist():
        b = r['bbox']
        if r['subtype'] != 'road' or b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n:
            continue
        g = shapely.from_wkb(r['geometry'])
        real.append(LineString([gidi(x, y, T) for x, y in g.coords]))
    near = unary_union([g.buffer(LINE_NEAR) for g in real]) if real else Polygon()
    roads = [r for r in recs if r['type'] == 'road']
    sf = os.path.join(top, 'STREETS.md')                 # the district's street list: each row says what it was read from
    streets = open(sf).read() if os.path.exists(sf) else ''
    on = off = 0.0
    for r in roads:
        L = LineString([q[:2] for q in r['centreline']])
        k = L.intersection(near).length / L.length if L.length else 1
        on, off = on + L.length * k, off + L.length * (1 - k)
        if k < LINE_SHARE:
            ok = bool(WRITTEN.search(r.get('note') or '')) or r['id'] in streets
            lines.append((r['id'], r.get('kind'), round(L.length, 1), round(k, 2), 'note or STREETS.md says where' if ok else 'NOT WRITTEN'))
            if not ok:
                fails.append(f'lines: {r["id"]} ({r.get("kind")}, {L.length:.0f} m) has {k:.0%} on a real street and nothing saying where it was read (its note or STREETS.md)')
    R['roads'], R['road m on a real street'] = len(roads), f'{on / (on + off):.0%}' if on + off else '-'

    # real places
    pl = pq.read_table(os.path.join(OVERTURE, 'lagos_overture_place.parquet'), columns=['taxonomy', 'names', 'geometry', 'bbox'])
    have = {}
    for r in recs:
        if r['type'] == 'place' and r.get('area'):
            have.setdefault(r.get('kind'), []).append(Polygon(r['area'][0]))
    trees = {k: STRtree(v) for k, v in have.items()}
    cws = [LineString([q[:2] for q in r['centreline']]).buffer(r['width'] / 2, cap_style=2) for r in roads]
    cwh = [r['width'] / 2 for r in roads]
    cw = STRtree(cws)
    want = miss = 0
    for r in pl.to_pylist():
        b = r['bbox']
        if b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n:
            continue
        g = shapely.from_wkb(r['geometry'])
        x, y = gidi(g.x, g.y, T)
        p = Point(x, y)
        if not ring.contains(p):
            continue
        k = place_kind((r['taxonomy'] or {}).get('primary'), (r['names'] or {}).get('primary'))
        if not k:
            continue
        want += 1
        if any(a.contains(p) for kk in GROUNDS for a in have.get(kk, [])):
            continue                     # inside a market, school or park drawn whole (hand pass 55)
        t = trees.get(k)
        on = [c for c in cw.query(p) if cws[c].contains(p)]      # a point on a carriageway: measured from the road's edge
        slack = max((cwh[c] for c in on), default=0.0)
        if t is None or have[k][t.nearest(p)].distance(p) > PLACE_NEAR + slack:
            miss += 1
            if miss <= 9:
                fails.append(f'places: a real {k} at ({x:.1f},{y:.1f}) has no {k} place within {PLACE_NEAR:.0f} m')
    R['real places for the game'], R['real places missing'] = want, miss
    if miss > 9:
        fails.append(f'places: {miss - 9} more real places missing')
    R['places'] = sum(len(v) for v in have.values())

    R['motor parks'], R['bus stops'] = len(have.get('motor_park', [])), len(have.get('bus_stop', []))
    if not R['bus stops'] and not R['motor parks']:
        fails.append('parks: no bus stop or motor park')

    walls = [r for r in recs if r['type'] == 'wall']
    plots = [r for r in recs if r['type'] == 'plot']
    unwalled = [p['id'] for p in plots if not any(wl.get('plot') == p['id'] and (wl.get('wall') or {}).get('gates') for wl in walls)]
    R['landmark plots'], R['plots without a gated wall'] = len(plots), len(unwalled)
    if unwalled:
        fails.append(f'landmarks: {len(unwalled)} plots with no wall and gate, e.g. {unwalled[:3]}')
    R['district'] = d
    return dict(R, fails=fails), lines


def main():
    ds = [a for a in sys.argv[1:] if re.fullmatch(r'd\d\d', a)] or sorted(x for x in os.listdir(os.path.join(ROOT, 'map')) if re.fullmatch(r'd\d\d', x))
    bad = 0
    for d in ds:
        R, lines = bar(d)
        print(f'{d}: ' + ', '.join(f'{k} {v}' for k, v in R.items() if k not in ('fails', 'district')))
        for l in lines:
            print(f'  under {LINE_SHARE:.0%} on a real street: {l[0]} {l[1]} {l[2]} m, {l[3]:.0%}, {l[4]}')
        for f in R['fails']:
            print(f'  FAIL {f}')
        print(f'{"PASS" if not R["fails"] else "FAIL"}  {d} at the working bar' + (f': {len(R["fails"])} fails' if R['fails'] else ''))
        bad += bool(R['fails'])
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
