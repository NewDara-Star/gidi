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
  density   our roof cover inside the outline lies between Google Open Buildings v3's cover there at Google's own
            90%- and 80%-precision confidence thresholds for the district's tile (CLAUDE.md "Working means it
            matches", owner 27 Oct); the street blocks furthest below Google are listed. Street km per km² is printed
            against Overture's streets, not gated until read from Google Maps.

  ~/.venvs/gidi/bin/python scripts/working_bar.py d15 [d09 ...]

Not held here, by eye in the running order: whether the widths were read (BUILDINGS.md and STREETS.md say where), and
which landmarks a district has (a landmark not drawn as a plot is not seen).
"""
import csv
import gzip
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
CITY_GAP = 8.0                        # m: half the widest divider the city layer leaves in one road (Ikorodu Road
                                      # at Onipanu east, 15.1 m with its bus bay, Google satellite 28 Oct)
GROUNDS = ('market', 'school', 'motor_park')   # places drawn whole: a real place inside one is in it
GOOGLE = os.path.expanduser('~/gidi-data/research/data/open-buildings-v3/lagos_open_buildings_v3.csv.gz')
THRESHOLDS = os.path.expanduser('~/gidi-data/research/data/open-buildings-v3/thresholds/score_thresholds_s2_level_4.csv')
STREET_CLASSES = {'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential', 'living_street', 'unclassified'}
BLOCKS_LISTED = 8                     # street blocks furthest below Google's cover, listed for the hand pass
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


def across(p, corridor, clines):
    """How far from p to the far edge of the city layer's road it stands in, across that road: a cut square to the
    nearest centreline, the piece of it inside the road that holds p, its far end."""
    from shapely.geometry import LineString, Point
    L = min(clines, key=lambda c: c.distance(p))
    s = L.project(p)
    a, b = L.interpolate(max(s - 1, 0)), L.interpolate(min(s + 1, L.length))
    dx, dy = b.x - a.x, b.y - a.y
    n = math.hypot(dx, dy) or 1
    nx, ny = -dy / n * 200, dx / n * 200
    cut = LineString([(p.x - nx, p.y - ny), (p.x + nx, p.y + ny)]).intersection(corridor)
    piece = next((g for g in getattr(cut, 'geoms', [cut]) if g.distance(p) < 1e-6), None)
    if piece is None or piece.is_empty:
        return 0.0
    c = list(piece.coords)
    return max(p.distance(Point(c[0])), p.distance(Point(c[-1])))


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
    seg = pq.read_table(os.path.join(OVERTURE, 'lagos_overture_segment.parquet'), columns=['subtype', 'class', 'geometry', 'bbox'])
    real, streets_real = [], []
    for r in seg.to_pylist():
        b = r['bbox']
        if r['subtype'] != 'road' or b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n:
            continue
        g = shapely.from_wkb(r['geometry'])
        real.append(LineString([gidi(x, y, T) for x, y in g.coords]))
        if r['class'] in STREET_CLASSES:
            streets_real.append(real[-1])
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
    # the city layer's roads through the district count as carriageway too (Ikorodu Road moved there, 28 Oct)
    city = os.path.join(ROOT, 'map', 'd00', 'plan.json')
    cr = [r for r in json.load(open(city))['records'] if r['type'] == 'road'] if d != 'd00' and os.path.exists(city) else []
    cr = [r for r in cr if ring.intersects(LineString([q[:2] for q in r['centreline']]))]
    cws = [LineString([q[:2] for q in r['centreline']]).buffer(r['width'] / 2, cap_style=2) for r in roads + cr]
    cwh = [r['width'] / 2 for r in roads + cr]
    # the city layer draws one road as strips (express, dividers, service roads): a point anywhere across it is measured
    # from the whole road's outer edge, as the old single record was; dividers up to 2*CITY_GAP wide are closed over
    corridor = unary_union(cws[len(roads):]).buffer(CITY_GAP).buffer(-CITY_GAP) if cr else Polygon()
    clines = [LineString([q[:2] for q in r['centreline']]) for r in cr]
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
        if t is not None and corridor.contains(p):
            # across the city layer's road: a place of its kind on either side, standing within PLACE_NEAR of its edge
            reach = max(slack, across(p, corridor, clines))
            if any(have[k][i].distance(p) <= PLACE_NEAR + reach and have[k][i].distance(corridor) <= PLACE_NEAR
                   for i in t.query(p.buffer(PLACE_NEAR + reach))):
                continue
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
    # density (CLAUDE.md "Working means it matches", owner 27 Oct): our roof cover inside the outline against Google
    # Open Buildings' inside the same outline, between Google's own 90%- and 80%-precision confidence thresholds for the
    # tile holding the district (their per-tile file); a per-area figure, so the 1:3 scale does not change it
    lon0, lat0 = inv.transform(500525 + 3 * ring.centroid.x, 707825 + 3 * (10500 - ring.centroid.y))
    t80 = t90 = None
    for r in csv.DictReader(open(THRESHOLDS)):
        if shapely.from_wkt(r['geometry']).contains(Point(lon0, lat0)):
            t80, t90 = float(r['confidence_threshold_80%_precision']), float(r['confidence_threshold_90%_precision'])
    if t80 is None:
        fails.append('density: no Google threshold tile holds the district')
    else:
        g80, g90 = [], []
        with gzip.open(GOOGLE, 'rt') as f:
            for r in csv.DictReader(f):
                c, la, lo = float(r['confidence']), float(r['latitude']), float(r['longitude'])
                if c < t80 or not (w <= lo <= e and s <= la <= n):
                    continue
                g = shapely.transform(shapely.from_wkt(r['geometry']), lambda a: [gidi(x, y, T) for x, y in a])
                g80.append(g)
                if c >= t90:
                    g90.append(g)
        ours = unary_union([Polygon(b['footprint']) for b in B]).intersection(ring).area / ring.area
        lo_, hi_ = (unary_union(gg).intersection(ring).area / ring.area for gg in (g90, g80))
        R['cover'] = f'{ours:.2%} (Google {lo_:.2%}-{hi_:.2%} at confidence {t90}-{t80})'
        if not lo_ <= ours <= hi_:
            fails.append(f'density: our cover {ours:.2%} is outside Google\'s {lo_:.2%}-{hi_:.2%}')
        # the street blocks (the outline less this district's carriageways) furthest below Google at its 90% figure
        G90 = unary_union(g90)
        OU = unary_union([Polygon(b['footprint']) for b in B])
        blocks = ring.difference(unary_union(cws))
        blocks = list(getattr(blocks, 'geoms', [blocks]))
        short = sorted(((bk.intersection(G90).area - bk.intersection(OU).area, bk) for bk in blocks), key=lambda t: -t[0])
        for sh, bk in short[:BLOCKS_LISTED]:
            if sh > 0:
                lines.append(('block', f'({bk.centroid.x:.0f},{bk.centroid.y:.0f})', round(bk.area),
                              round(bk.intersection(OU).area / bk.area, 2), f'Google {bk.intersection(G90).area / bk.area:.0%}, {sh:.0f} m2 short'))
    # street length per km2 against Overture's real roads, printed, not gated: Overture is OpenStreetMap's network, thin
    # in Lagos, and the real figure is to be read from Google Maps first (NOW 16)
    km2 = ring.area / 1e6
    ours_km = sum(LineString([q[:2] for q in r['centreline']]).intersection(ring).length for r in roads) / 1000
    real_km = sum(g.intersection(ring).length for g in streets_real) / 1000 / 3      # real length (x3) per real area (x9)
    R['street km per km2'] = f'{ours_km / km2:.1f} (Overture {real_km / km2:.1f}, not gated)'
    R['district'] = d
    return dict(R, fails=fails), lines


def main():
    ds = [a for a in sys.argv[1:] if re.fullmatch(r'd\d\d', a)] or sorted(x for x in os.listdir(os.path.join(ROOT, 'map')) if re.fullmatch(r'd\d\d', x) and x != 'd00')
    bad = 0
    for d in ds:
        R, lines = bar(d)
        print(f'{d}: ' + ', '.join(f'{k} {v}' for k, v in R.items() if k not in ('fails', 'district')))
        for l in lines:
            if l[0] == 'block':
                print(f'  block at {l[1]}, {l[2]} m2: ours {l[3]:.0%}, {l[4]}')
                continue
            print(f'  under {LINE_SHARE:.0%} on a real street: {l[0]} {l[1]} {l[2]} m, {l[3]:.0%}, {l[4]}')
        for f in R['fails']:
            print(f'  FAIL {f}')
        print(f'{"PASS" if not R["fails"] else "FAIL"}  {d} at the working bar' + (f': {len(R["fails"])} fails' if R['fails'] else ''))
        bad += bool(R['fails'])
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
