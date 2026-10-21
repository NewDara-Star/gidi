"""Ìbùdó, one area of the child plan built from its real place (owner, 19 Oct 2026: "you are taking streets from this place ... so you can
have real life images that we can now model from"). docs/hand/ibudo/child_plan.json says which real place an area is and where it sits
(true scale, north up). This writes hand edits into web/hand/hub.json:
- the area is cleared (houses, streets, lanes, paths, plots, slip roads, decks and places that were there);
- the new arterial and rail lines (scripts/layout_v2.py) get their corridors through the whole district;
- the real streets go in (Overture Maps transportation, ODbL, from OpenStreetMap: ~/Real-world/research/data/overture-lagos), the trunk
  road, the expressway and the rail being the layout's own lines;
- the real building footprints go in (Google Open Buildings v3, CC-BY 4.0 / ODbL), their storeys from Open Buildings 2.5D 2023 heights;
- every street's twin is written to docs/hand/ibudo/twins/<area>.json: the real street it is, its real name and a point to photograph.
Nothing is generated: the shapes are the real ones; Gidi's own changes come by hand after.
Usage: GIDI_BASE=<baked data before the area> python3 scripts/hand_spots/ibudo_real_area.py oshodi_core
scripts/rebuild_areas.py runs it for every area in turn (GIDI_HUB: the edits so far; GIDI_OUT: where this area's edits go).
The twin record keeps what the study already found (pictures, status, notes) for every street it had.
"""
import csv
import gzip
import json
import math
import os
import sys

import numpy as np
import pyarrow.parquet as pq
from shapely import STRtree, wkb, wkt
from shapely.geometry import LineString, MultiLineString, Point, Polygon, box
from shapely.ops import unary_union

AREA_ID = sys.argv[1]
DATA = os.path.expanduser('~/Real-world/research/data')
CP = json.load(open('docs/hand/ibudo/child_plan.json'))
A = next(a for a in CP['areas'] if a['id'] == AREA_ID)
S = open(os.environ.get('GIDI_BASE', 'web/gidi-data.js')).read()
G = json.loads(S[S.index('{'):S.rstrip().rstrip(';').rindex('}') + 1])
L = json.load(open('web/layout-v2.json'))
HUB = Polygon(L['districts']['hub'])
AREA = Polygon(A['pts']).intersection(HUB.buffer(-6))
for pr in CP.get('protect', []):   # story places no area build may touch (the boss's motor park)
    AREA = AREA.difference(Polygon(pr['pts']).buffer(4))
AREA = max(getattr(AREA, 'geoms', [AREA]), key=lambda g: g.area)
HUBF = os.environ.get('GIDI_HUB', 'web/hand/hub.json')
OWN = AREA.difference(wkt.loads(os.environ['GIDI_LATER_WKT'])) if os.environ.get('GIDI_LATER_WKT') else AREA   # what stays this area's own
WHO = f"Claude, 19 Oct 2026: Ìbùdó from real places ({A['name']})"
M_LAT, M_LON = 110600.0, 109900.0
(LA0, LO0), (GX0, GY0) = A['anchor_real'], A['anchor_gidi']
R = lambda xy: [round(xy[0], 1), round(xy[1], 1)]


def ring_pts(g):   # a footprint's corners, rounded to 0.1 m, with no corner repeated (the bake's fronts need real edges)
    out = []
    for c in list(g.exterior.coords)[:-1]:
        q = R(c)
        if not out or q != out[-1]:
            out.append(q)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out


def T(lo, la):   # real -> Gidi
    return (GX0 + (lo - LO0) * M_LON, GY0 - (la - LA0) * M_LAT)


def Tinv(x, y):   # Gidi -> real (lat, lon)
    return (LA0 - (y - GY0) / M_LAT, LO0 + (x - GX0) / M_LON)


x0, y0, x1, y1 = AREA.bounds
N, W = Tinv(x0 - 60, y0 - 60); S_, E_ = Tinv(x1 + 60, y1 + 60)
E = []

# ---- the layout's lines through the district: corridors (half-widths as the generator clears them, scripts/gen_fabric.py)
CLR = {'exp': 18.2, 'art': 12.5}   # past the building line (scripts/cross_sections.py: exp 18, art 10)
LINES = [(a['name'], LineString(a['pts']), CLR.get(a['cls'], 12.5)) for a in L['arterials'] if LineString(a['pts']).distance(HUB) < 30]
RAIL = LineString(L['rail']['pts'])
CORR = unary_union([g.buffer(w) for n, g, w in LINES] + [RAIL.buffer(7)]).intersection(HUB.buffer(5))

# ---- 1. what is there goes: in the area, and in the new corridors through the district
B = G['buildings']['hub']
CLEAR = AREA.union(CORR.intersection(HUB)) if os.environ.get('GIDI_CORRIDORS') else AREA   # the corridors were cleared once, with the first area (GIDI_CORRIDORS=1)
# one shape clears it (scripts/hand.py "clear area"): its streets cut back to the edge, its buildings, paths, plots, mains, decks and places
# gone, whether the base or an earlier area put them there. A delete per thing missed whatever had moved by bake time (21 Oct 2026).
sys.path.insert(0, 'scripts')
import hand
from shapely import set_precision
e = {'op': 'clear area', 'wkt': set_precision(CLEAR, 0.1).wkt, 'places_wkt': set_precision(AREA, 0.1).wkt,
     'note': f"cleared for {A['name']} (real) or a layout line", 'by_who': WHO}
E.append(e)
n_par = len(G['parcels'].get('hub', []))
hand._clear_area(G, 'hub', e, 'road'); hand._clear_area(G, 'hub', e, 'late')   # this area is built on the map as the bake will leave it
seen_par = n_par - len(G['parcels'].get('hub', []))
B = G['buildings']['hub']
LIVE = [[k, LineString(p)] for k in ('streets', 'lanes') for p in G[k].get('hub', []) if len(p) > 1]
FIXED = [LineString(m['pts']) for m in G['mains'] if len(m['pts']) > 1] + [g for n, g, w in LINES]

# ---- 2. the real streets
t = pq.read_table(f'{DATA}/overture-lagos/lagos_overture_segment.parquet', columns=['id', 'names', 'subtype', 'class', 'geometry', 'bbox'])
bb = t.column('bbox').to_pylist()
rows = t.take([i for i, b in enumerate(bb) if b['xmax'] >= W and b['xmin'] <= E_ and b['ymax'] >= S_ and b['ymin'] <= N]).to_pylist()
KIND = {'primary': 'main', 'secondary': 'main', 'tertiary': 'street', 'residential': 'street', 'unclassified': 'street', 'living_street': 'street',
        'service': 'lane', 'track': 'lane', 'unknown': 'lane', 'footway': 'path', 'steps': 'path', 'path': 'path', 'pedestrian': 'path', 'cycleway': 'path'}
TWINS, ADDED, TWINS_E = [], [], []
REAL = {'buildings': 0, 'built_m2': 0.0, 'street_m': {}, 'places': {}}   # the real place in the area, before Gidi's changes: what check_real.py holds the map to
KEEP_OUT = CORR.buffer(1)
for r in rows:
    if r['subtype'] != 'road' or r['class'] not in KIND:
        continue   # the trunk road, the expressway and the rail are the layout's lines
    g = LineString([T(*c) for c in wkb.loads(r['geometry']).coords]).intersection(AREA)
    REAL['street_m'][KIND[r['class']]] = REAL['street_m'].get(KIND[r['class']], 0) + round(g.intersection(OWN).length)
    g = g.difference(KEEP_OUT)
    name = (r['names'] or {}).get('primary') if r['names'] else None
    for part in getattr(g, 'geoms', [g]):
        if part.geom_type != 'LineString' or part.length < 8:
            continue
        kind = KIND[r['class']]
        pts = [R(c) for c in part.coords]
        if kind == 'path':
            E.append({'op': 'add path', 'pts': pts, 'note': f"real: {name or r['class']}", 'by_who': WHO})
        else:
            E.append({'op': 'add street', 'kind': kind, 'pts': pts, **({'name': ''} if kind == 'main' else {}), 'note': f"real: {name or r['class']}", 'by_who': WHO})
        TWINS_E.append(E[-1])
        ADDED.append((kind, part, E[-1]))
        mid = part.interpolate(0.5, normalized=True); la, lo = Tinv(mid.x, mid.y)
        TWINS.append({'gidi': pts, 'kind': kind, 'real_name': name, 'real_class': r['class'], 'overture_id': r['id'],
                      'photo_at': [round(la, 6), round(lo, 6)], 'length_m': round(part.length), 'status': 'red', 'pics': []})
# a street trimmed at a layout line's corridor runs on to the line, as the real one meets the real road
from shapely.ops import nearest_points
EDGE = KEEP_OUT.boundary
for i, (k, g, e) in enumerate(ADDED):
    cs = list(g.coords)
    for end in (0, -1):
        p_ = Point(cs[end])
        if p_.distance(EDGE) > 2.0:
            continue
        near = min(((ln.distance(p_), ln) for n, ln, w in LINES), key=lambda t_: t_[0])
        if near[0] < 25:
            q = nearest_points(near[1], p_)[0]
            cs = cs + [(q.x, q.y)] if end == -1 else [(q.x, q.y)] + cs
    for end in (0, -1):   # the seam: a street reaching the area's edge runs on to the nearest street, lane or main outside it
        p_ = Point(cs[end])
        if p_.distance(AREA.boundary) > 2.0 or g.length < 10:
            continue
        outside = [h for kk, h in LIVE if h.distance(p_) < 30] + [m_ for m_ in FIXED if m_.distance(p_) < 30]
        if not outside:
            continue
        h = min(outside, key=lambda h_: h_.distance(p_))
        if h.distance(p_) < 0.5:
            continue
        q = nearest_points(h, p_)[0]
        cs = cs + [(q.x, q.y)] if end == -1 else [(q.x, q.y)] + cs
    if len(cs) != len(g.coords):
        g = LineString(cs); e['pts'] = [R(c) for c in cs]; ADDED[i] = (k, g, e)
# pieces cut off by the clipping lead nowhere: only what joins the network (the layout's lines, mains, the streets kept) stays
roots = [g for n, g, w in LINES] + [LineString(m['pts']) for m in G['mains'] if len(m['pts']) > 1] + [h for k, h in LIVE]
items = [g for k, g, e in ADDED]
ok = set()


def spread(frontier):
    ok.update(frontier)
    while frontier:
        nxt = []
        for i in frontier:
            for j, h in enumerate(items):
                if j not in ok and items[i].distance(h) < 1.0:
                    ok.add(j); nxt.append(j)
        frontier = nxt


spread([i for i, g in enumerate(items) if any(g.distance(r_) < 1.0 for r_ in roots if r_.distance(g) < 2)])
# a group of real streets whose real way out is not on the map (a trunk road Gidi's arterial replaces, an old road the area cleared) is
# joined to the nearest way by the shortest link, nearest group first, not dropped: the link is Gidi's own and its twin record says so
LINK = 80.0
while True:
    out_ = [i for i in range(len(items)) if i not in ok]
    if not out_:
        break
    reach = roots + [items[i] for i in ok]
    best = None
    for i in out_:
        for r_ in reach:
            dd = items[i].distance(r_)
            if dd < LINK and (best is None or dd < best[0]):
                best = (dd, i, r_)
    if best is None:
        break
    dd, i, r_ = best
    p_, q_ = nearest_points(items[i], r_)
    if dd >= 0.5:
        kind = 'street' if ADDED[i][0] in ('street', 'main') else 'lane'
        pts = [R((p_.x, p_.y)), R((q_.x, q_.y))]
        e = {'op': 'add street', 'kind': kind, 'pts': pts, 'note': 'Gidi link: the real way out of these streets is not on the map', 'by_who': WHO}
        E.append(e); g = LineString(pts)
        ADDED.append((kind, g, e)); items.append(g); ok.add(len(items) - 1)
        TWINS.append({'gidi': pts, 'kind': kind, 'real_name': None, 'real_class': 'gidi link', 'overture_id': None, 'photo_at': None,
                      'length_m': round(dd), 'status': 'n/a', 'pics': [], 'link': True})
        TWINS_E.append(e)
    spread([i])
dropped = [e for i, (k, g, e) in enumerate(ADDED) if i not in ok]
E = [e for e in E if not any(e is d_ for d_ in dropped)]
TWINS = [t_ for t_, e in zip(TWINS, TWINS_E) if not any(e is d_ for d_ in dropped)]
ADDED = [(k, g) for i, (k, g, e) in enumerate(ADDED) if i in ok]
print('street pieces dropped (cut off):', len(dropped))
WAYS = unary_union([g for k, g in ADDED] + [g for n, g, w in LINES] + roots)

# ---- 3. the real buildings, their storeys from the 2023 heights
import rasterio
from rasterio.warp import transform as rtrans
HT = rasterio.open(f'{DATA}/open-buildings-2023/tile_shazo_x29JA.tif')
H2 = HT.read(2)


def height(poly):
    c = poly.representative_point(); la, lo = Tinv(c.x, c.y)
    xs, ys = rtrans('EPSG:4326', HT.crs, [lo], [la]); r_, c_ = HT.index(xs[0], ys[0])
    win = H2[max(r_ - 4, 0):r_ + 5, max(c_ - 4, 0):c_ + 5]
    v = win[win > 0.5]
    return float(np.median(v)) if v.size else 0.0


BL = {'main': 6.3, 'street': 4.1, 'lane': 1.7}   # the building lines (scripts/cross_sections.py) and 20 cm
STREET_BUF = unary_union([g.buffer(BL[k]) for k, g in ADDED if k != 'path'] + [CORR]
                         + [LineString(m['pts']).buffer(6.3) for m in G['mains'] if len(m['pts']) > 1 and LineString(m['pts']).distance(AREA) < 30]
                         + [h.buffer(BL['lane' if k == 'lanes' else 'street']) for k, h in LIVE if h.distance(AREA) < 30])
OLD = [Polygon(b[1:]) for b in B if len(b) > 3 and not Polygon(b[1:]).intersects(CLEAR) and Polygon(b[1:]).distance(AREA) < 20]
PLACED = []
LOST = {'building line': 0.0, 'on a kept building': 0.0, 'no way within 40 m': 0.0}   # real built-up m2 the area does not keep, and why
INNER = AREA.buffer(-1.0)
nb = 0
with gzip.open(f'{DATA}/open-buildings-v3/lagos_open_buildings_v3.csv.gz', 'rt') as f:
    for r in csv.DictReader(f):
        la, lo = float(r['latitude']), float(r['longitude'])
        if not (S_ <= la <= N and W <= lo <= E_) or float(r['confidence']) < 0.65:
            continue
        g0 = wkt.loads(r['geometry'])
        for pg in getattr(g0, 'geoms', [g0]):
            P = Polygon([T(*c) for c in pg.exterior.coords]).buffer(0)
            if P.is_empty or not AREA.contains(P.centroid):
                continue
            own = OWN.contains(P.centroid)
            if own:
                REAL['buildings'] += 1; REAL['built_m2'] += P.area
            a0 = P.area
            P = P.intersection(INNER).difference(STREET_BUF)   # inside the area, and cut back to the building line of every road near it
            P = max(getattr(P, 'geoms', [P]), key=lambda q: q.area) if not P.is_empty else P
            if own:
                LOST['building line'] += a0 - (P.area if not P.is_empty else 0)
            if P.is_empty or P.geom_type != 'Polygon' or P.area < 6:
                continue
            P = P.simplify(0.3)
            if P.distance(WAYS) > 40:
                if own:
                    LOST['no way within 40 m'] += P.area
                continue   # reached by no way
            hit = [q for q in OLD + PLACED if q.distance(P) < 0.5 and P.intersection(q).area > 0.5]
            if hit:   # real neighbours overlap a little in the data: cut back from them (35 cm, so rounding keeps them apart); a double goes
                a1 = P.area
                P = P.difference(unary_union(hit).buffer(0.35))
                P = max(getattr(P, 'geoms', [P]), key=lambda q: q.area) if not P.is_empty else P
                if P.is_empty or P.geom_type != 'Polygon' or P.area < 6 or P.area < 0.3 * a1:
                    if own:
                        LOST['on a kept building'] += a1
                    continue
                if own:
                    LOST['on a kept building'] += a1 - P.area
            PLACED.append(P)
            h = height(P)
            st = max(1, min(12, round(h / 3.2))) if h else 1
            kind = 'warehouse' if P.area > 2500 else ('front' if P.distance(WAYS) < 9 else 'back')
            E.append({'op': 'add building', 'kind': kind, 'pts': ring_pts(P), 'storeys': st, 'note': f"real footprint {r['full_plus_code']}, {h:.1f} m", 'by_who': WHO})
            nb += 1

# ---- 4. the real places: churches, mosques, schools, clinics, chemists, hotels, banks, offices (Overture places), each at its real spot
# with a Gidi name (invented, never a real one); the real name stays in the twin record
PNAMES = {'church': ['Living Waters Chapel', 'Grace Harvest Church', 'Oke Iye Chapel', 'Mount Zion Assembly', 'New Dawn Church', 'Cherubim Light Chapel',
                     'Rock of Ages Chapel', 'Peace Assembly', 'Overflow Chapel', 'Shiloh Gate Church', 'Ebenezer House of Prayer', 'Bethel Light Church',
                     'Oluwaseun Gospel Church', 'Light of Ìbùdó Assembly', 'Fountain of Mercy Chapel', 'Abundant Rain Church', 'Holy Ghost Fire Ministry',
                     'Calvary Hope Chapel', 'Emmanuel Covenant Church', 'Pillar of Truth Assembly', 'Morning Glory Chapel', 'Faith Harvest Ministry',
                     'Anchor of Life Church', 'Second Mile Chapel', 'Showers of Grace Church', 'Jesus Arena Chapel', 'Olorun Agbaye Church',
                     'Seed of Life Assembly', 'Divine Help Chapel', 'Prayer Mountain Church', 'Christ the Rock Chapel', 'Wells of Joy Church',
                     'Victory Torch Assembly', 'Gate of Heaven Chapel', 'Love Fountain Church', 'Mercy Seat Chapel', 'Glorious Dawn Assembly',
                     'Ayo Ni O Church', 'Testimony Chapel', 'Shield of Faith Church', 'House of Refuge', 'Living Bread Chapel'],
          'mosque': ['Nurul Islam Mosque', 'Ìbùdó Central Mosque', 'Ansar Jumat Mosque', 'Al-Furqan Mosque', 'Baitul Huda Mosque', 'Tawheed Mosque',
                     'Nasrul Lahi Mosque', 'Al-Hikmah Mosque', 'Darul Salam Mosque', 'Al-Ihsan Mosque', 'Jamiu Mosque', 'Al-Amin Mosque'],
          'school': ['Bright Star Nursery and Primary', 'Ayo Kids Academy', 'Grace Comprehensive College', 'Morning Star School', 'Unity Grammar School',
                     'Ìbùdó Model School', 'Royal Seeds Academy', 'Victory Nursery and Primary', 'Treasure Kids School', 'Excel High School',
                     'Golden Gate College', 'Little Angels School', 'Crown Heights Academy', 'Sunrise Nursery and Primary', 'Wisdom Gate College',
                     'Great Minds School', 'Pathfinder Academy', 'Rainbow Kids School', 'Ìlérí Grammar School', 'Owode Comprehensive College',
                     'Starlight Nursery and Primary', 'Beacon High School', 'Bright Future Academy', 'Kingdom Heritage School'],
          'clinic': ['Mercy Clinic', 'Good Hope Clinic', 'Life Line Medical Centre', 'St Luke Clinic', 'Ireti Clinic', 'Alafia Medical Centre', 'Care Point Clinic', 'Doyin Maternity', 'Healing Touch Clinic'], 'hospital': ['Ìbùdó General Hospital', 'Oasis Hospital'],
          'chemist': ['Healthway Chemist', 'Rapha Pharmacy', 'Mama Bisi Chemist', 'Sure Cure Chemist', 'Alaafia Pharmacy', 'Good Health Chemist', 'Iya Rasaq Chemist', 'Life Spring Pharmacy', 'Tunde Drugs'],
          'hotel': ['Gidi Rest Hotel', 'Palm Court Hotel', 'Royal Comfort Inn', 'Travellers Lodge', 'Jet Stop Hotel', 'Airways Suites', 'Cool Breeze Inn', 'Owambe Hotel', 'Sky Lane Suites',
                     'Landing Hotel', 'Golden Crest Hotel', 'Plaza Comfort Inn', 'Starboard Suites', 'Quiet Haven Hotel'], 'bank': ['Gidi Trust Bank', 'Mainland Bank', 'Union Ọjà Bank'],
          'government': ['Ìbùdó Council Office', 'Motor Licensing Office']}
used = {p_['name'] for p_ in G['pois']}


def pname(t_):
    for n_ in PNAMES[t_]:
        if n_ not in used:
            used.add(n_); return n_
    k_ = 2
    while f"{PNAMES[t_][0]} {k_}" in used:
        k_ += 1
    used.add(f"{PNAMES[t_][0]} {k_}"); return f"{PNAMES[t_][0]} {k_}"


def ptype(cat, name):
    n_ = (name or '').lower()
    if any(w in n_ for w in ('mosque', 'masjid', 'jumat', 'jamat', 'islam')): return 'mosque'
    if cat in ('christian_place_of_worship', 'religious_organization', 'church_cathedral') or any(w in n_ for w in ('church', 'chapel', 'assembly', 'tabernacle')): return 'church'
    if cat in ('place_of_learning', 'education', 'elementary_school', 'preschool', 'high_school', 'specialty_school', 'college_university', 'educational_service') or 'school' in n_ or 'college' in n_: return 'school'
    if cat in ('pharmacy', 'drugstore') or 'pharm' in n_ or 'chemist' in n_: return 'chemist'
    if cat in ('hospital',) or 'hospital' in n_: return 'hospital'
    if cat in ('health_care', 'medical_center', 'clinic') or 'clinic' in n_ or 'medical' in n_: return 'clinic'
    if cat in ('hotel', 'lodging'): return 'hotel'
    if cat in ('bank', 'financial_service') and 'bank' in n_: return 'bank'
    if cat == 'government_office': return 'government'
    return None


tp = pq.read_table(f'{DATA}/overture-lagos/lagos_overture_place.parquet', columns=['id', 'geometry', 'confidence', 'basic_category', 'names', 'bbox'])
bbp = tp.column('bbox').to_pylist()
PL = []
for r in tp.take([i for i, b in enumerate(bbp) if W <= b['xmin'] <= E_ and S_ <= b['ymin'] <= N]).to_pylist():
    nm = (r['names'] or {}).get('primary') if r['names'] else None
    t_ = ptype(r['basic_category'], nm)
    if not t_ or float(r['confidence'] or 0) < 0.4:
        continue
    pt = wkb.loads(r['geometry']); x, y = T(pt.x, pt.y)
    if OWN.contains(Point(x, y)):
        REAL['places'][t_] = REAL['places'].get(t_, 0) + 1
    if not AREA.contains(Point(x, y)) or any(Point(x, y).distance(Point(q_)) < 15 for q_ in PL):
        continue
    PL.append((x, y))
    E.append({'op': 'add place', 'name': pname(t_), 'type': t_, 'x': round(x), 'y': round(y), 'note': f"real: {nm} ({r['basic_category']})", 'by_who': WHO})
print('places:', len(PL))
if os.environ.get('GIDI_PLACES_ONLY'):
    E = [e for e in E if e['op'] == 'add place']
if os.environ.get('GIDI_OUT'):
    json.dump(E, open(os.environ['GIDI_OUT'], 'w'), separators=(',', ':'), ensure_ascii=False)
else:
    H = json.load(open(HUBF))
    H['edits'] = H.get('edits', []) + E
    json.dump(H, open(HUBF, 'w'), separators=(',', ':'), ensure_ascii=False)
os.makedirs('docs/hand/ibudo/twins', exist_ok=True)
TF = f'docs/hand/ibudo/twins/{AREA_ID}.json'
if not os.environ.get('GIDI_PLACES_ONLY'):
    OLD_T = json.load(open(TF)) if os.path.exists(TF) else {}
    was = {}
    for t_ in OLD_T.get('streets', []):   # a street the study photographed keeps its pictures, status and notes when the area is built again
        was.setdefault(t_.get('overture_id'), []).append(t_)
    for t_ in TWINS:
        if was.get(t_['overture_id']):
            o_ = was[t_['overture_id']].pop(0)
            t_.update({k: v for k, v in o_.items() if k not in ('gidi', 'length_m')})
    for t_ in TWINS:   # a street a later area builds again: its record stays (and its pictures), marked, and is not looked for on the map
        g_ = LineString(t_['gidi'])
        if OWN.buffer(1).intersection(g_).length < 0.5 * g_.length:
            t_['replaced'] = 'by a later area'
        else:
            t_.pop('replaced', None)
    lost = sum(1 for v in was.values() for t_ in v if t_.get('pics'))
    if lost:
        print('WARNING: photographed streets no longer in the area:', lost)
    json.dump({**{k: v for k, v in OLD_T.items() if k != 'streets'}, 'area': AREA_ID, 'real': A['real'], 'anchor_real': A['anchor_real'],
               'anchor_gidi': A['anchor_gidi'], 'area_wkt': set_precision(OWN, 0.1).wkt,
               'real_counts': {**REAL, 'built_m2': round(REAL['built_m2'])}, 'streets': TWINS}, open(TF, 'w'), ensure_ascii=False, indent=0)
from collections import Counter
print('real built-up m2 not kept:', {k: round(v) for k, v in LOST.items()}, 'of', round(REAL['built_m2']))
print(AREA_ID, len(E), 'edits', dict(Counter(e['op'] for e in E)), '| buildings', nb, '| twin streets', len(TWINS), '| plots cleared', seen_par)
