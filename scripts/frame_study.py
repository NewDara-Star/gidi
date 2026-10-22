"""The new frame's study layers for the drawing board (owner, 22 Oct 2026: Gidi is real Lagos miniaturised at 1:3, in a
27 x 10.5 km frame; roads first, districts by their borders). Open them with web/board.html?frame=new.

A study underlay to draw the new map on by hand, never map data: real names and real lines stay on the board, never in
web/hand/ or any map file. The output (web/frame-study.js) is made from real data and is not committed (.gitignore).

Layers, all in Gidi metres (x east, y south, 0..27000 x 0..10500), from the roads study (docs/lagos-study/roads/):
  roads    the real skeleton: motorway, trunk, primary, secondary (+ their links), rail, bridges (Overture, via skel.pkl)
  water    the lagoon, creeks and ocean (ESA WorldCover water, 50 m grid)
  districts the 51 districts of EARTH-CHECK.md, each the union of its places (places.npz); the unsure lines and the lines
           still to trace are drawn dashed with their question
  places   the 819 places of places.csv, as labels

  ~/.venvs/gidi/bin/python scripts/frame_study.py
needs the roads study's working files (run docs/lagos-study/roads/scripts first; GIDI_SCRATCH points at them).
Footprints for the zoomed-in underlay: scripts/frame_footprints.py.
"""
import collections
import json
import os
import pickle
import re
import sys

import numpy as np
import shapely
from affine import Affine
from rasterio import features
from scipy import ndimage as nd
from shapely.geometry import box, shape
from shapely.ops import linemerge, unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'docs', 'lagos-study', 'roads', 'scripts'))
from common import WORK, X0, Y0, C, SCALE, FRAME   # noqa: E402

NW = json.load(open(WORK + 'network.json'))
FU, FV = NW['fu'], NW['fv']                       # the frame's south-west corner, UTM 31N metres (the frame is not turned)
RW, RH = FRAME[0] * SCALE, FRAME[1] * SCALE       # 81 x 31.5 km real
CLIP = box(FU, FV, FU + RW, FV + RH)
AFF = Affine(C, 0, X0, 0, C, Y0)                  # grid row i is y = Y0 + i*C (north up as i grows)


def gidi(xy):
    """Real UTM metres -> Gidi metres at 1:3 (x east, y south, as the board draws)."""
    xy = np.asarray(xy, float)
    return np.column_stack([(xy[:, 0] - FU) / SCALE, (FV + RH - xy[:, 1]) / SCALE])


R1 = lambda a: [[round(float(x), 1), round(float(y), 1)] for x, y in a]


def lines_of(g, tol=0):
    """A (multi)line clipped to the frame, simplified, as lists of Gidi points."""
    g = g.intersection(CLIP)
    if tol:
        g = g.simplify(tol)
    out = []
    for p in getattr(g, 'geoms', [g]):
        if p.geom_type == 'LineString' and p.length > 1:
            out.append(R1(gidi(p.coords)))
        elif p.geom_type in ('MultiLineString', 'GeometryCollection'):
            out += lines_of(p)
    return out


def rings_of(g):
    out = []
    for p in getattr(g, 'geoms', [g]):
        if p.geom_type == 'Polygon' and not p.is_empty:
            out.append([R1(gidi(p.exterior.coords))] + [R1(gidi(h.coords)) for h in p.interiors])
    return out


# ------------------------------------------------------------------ 1. the road skeleton
S = pickle.load(open(WORK + 'skel.pkl', 'rb'))
roads = []
for s in S['segs']:
    ln = shapely.LineString(s['xy'])
    if not ln.intersects(CLIP):
        continue
    k = 'rail' if s['cls'] == 'rail' else s['cls']
    for pts in lines_of(ln, 3):
        roads.append({'k': k, 'l': int(s['link']), 'n': s['name'], 'p': pts})
    for a, b in s.get('bspans') or []:          # the bridge spans, drawn over the road
        part = shapely.ops.substring(ln, a, b, normalized=True)
        if part.length >= 30:
            for pts in lines_of(part, 3):
                roads.append({'k': 'bridge', 'l': 0, 'n': s['name'], 'p': pts})
print(len(roads), 'road pieces')

# ------------------------------------------------------------------ 2. water
WC = np.load(WORK + 'wc50.npz')
water = WC['water'] >= 0.5
water = nd.binary_opening(water, iterations=1)
lab, n = nd.label(water)
sz = nd.sum(np.ones_like(lab), lab, range(1, n + 1))
water = np.isin(lab, 1 + np.nonzero(sz >= 40)[0])          # ponds under 0.1 km2 left out
wpolys = [shape(g) for g, v in features.shapes(water.astype(np.uint8), mask=water, transform=AFF) if v == 1]
wat = []
for g in wpolys:
    g = g.simplify(30).intersection(CLIP)
    wat += rings_of(g)
print(len(wat), 'water polygons')

# ------------------------------------------------------------------ 3. places and the 51 districts
PZ = np.load(WORK + 'places.npz')
place = PZ['place']
PL = {q['id']: q for q in json.load(open(WORK + 'places.json'))['places']}

# EARTH-CHECK.md, "District list after the checks": each district's members, by place name. A place goes to the district
# whose name prefix is the longest match ("Agbara" takes "Agbara west", "Agbara, east of ..."); FULL names win over prefixes.
D51 = [
    (1, 'Agbara-Morogbo', ['Agbara', 'Morogbo', 'Badagry', 'Ajara']),
    (2, 'Okokomaiko-Ijanikin-Otto', ['Okokomaiko', 'Ijanikin', 'Otto-Awori']),
    (3, 'Alaba-Ojo-Trade Fair', ['Alaba', 'Ojo (LASU)', 'Volks', 'Navy Town', 'Abule Ado', 'Trade Fair']),
    (4, 'Iba-Isheri-Olofin', ['Iba', 'Isheri-Olofin']),
    (5, 'Festac', ['Festac', 'Agboju', 'Alakija']),
    (6, 'Mile 2-Amuwo Odofin', ['Mile 2', 'Amuwo Odofin', '=Amukoko, north of Lagos-Badagry Expressway']),
    (7, 'Satellite Town', ['Satellite Town', 'Ijegun-Egba']),
    (8, 'Kirikiri-Tin Can', ['Kirikiri', 'Tin Can', '=Ijegun-Egba east', '=Boundary (Ajegunle), west of Apapa-Oworonshoki Expressway']),
    (9, 'Ajegunle', ['Ajegunle', 'Amukoko', 'Boundary (Ajegunle)', 'Olodi Apapa']),
    (10, 'Apapa', ['Apapa GRA', 'Apapa Wharf']),
    (11, 'Ijora-Iganmu-Costain', ['Ijora', 'Iganmu', 'Costain', 'Iponri']),
    (12, 'Aguda-Coker-Orile', ['Aguda', 'Coker', 'Orile Iganmu']),
    (13, 'Surulere', ['Surulere', 'Ojuelegba', 'Bode Thomas', 'Stadium (Surulere)', 'Adelabu', 'Ogunlana']),
    (14, 'Itire-Lawanson-Ijesha', ['Itire', 'Lawanson', 'Ijesha']),
    (15, 'Mushin', ['Mushin', 'Idi-Oro', 'Odi-Olowo', 'Ojuwoye-Mushin', 'Olorunsogo', 'Idi-Araba']),
    (16, 'Ebute Metta-Oyingbo-Otto', ['Ebute Metta', 'Oyingbo', 'Otto-Iddo']),
    (17, 'Yaba', ['Yaba', 'Sabo', 'Alagomeji', 'Jibowu', 'Onike-Abule Oja', 'Igbobi']),
    (18, 'UNILAG', ['UNILAG']),
    (19, 'Makoko', ['Makoko', 'Iwaya']),
    (20, 'Lagos Island (Eko)', ['Isale Eko', 'Idumota', 'Marina', 'Lafiaji', 'Onikan', 'Obalende']),
    (21, 'Ikoyi', ['Ikoyi', 'Old Ikoyi', 'Dolphin Estate', 'Parkview', 'Banana Island']),
    (22, 'Victoria Island', ['Victoria Island', '=Elegushi west', 'Eko Atlantic']),
    (23, 'Lekki Phase 1', ['Oniru', 'Lekki Phase 1', 'Ikate', 'Elegushi']),
    (24, 'Lekki-Agungi-Chevron', ['Agungi', 'Ilasan', 'Jakande (Lekki)', 'Osapa London', 'Ikota', 'VGC', 'Chevron']),
    (25, 'Ajah', ['Ajah', 'Ilaje Ajah', 'Abraham Adesanya', 'Addo', 'Langbasa', 'Badore', '=Chevron south-east']),
    (26, 'Sangotedo-Abijo-Lakowe', ['Sangotedo', 'Bogije', 'Abijo', 'Lakowe', 'Awoyaya', 'Ogombo', 'Eleko']),
    (27, 'Shomolu-Bariga', ['Shomolu', 'Bariga', 'Ilaje (Bariga)', 'Bajulaiye', 'Pedro', 'Akoka', 'Fadeyi', 'Palmgrove', 'Obanikoro-Onipanu', 'Oworonshoki']),
    (28, 'Gbagada-Ogudu', ['Gbagada', 'Gbagada Phase 2', 'Ifako-Gbagada', 'Soluyi', 'Ogudu', 'Anthony Village']),
    (29, 'Ilupeju', ['Ilupeju', '=Shogunle, east of Agege Motor Road']),
    (30, 'Isolo-Ladipo', ['Isolo', 'Cele', 'Ladipo', 'Papa Ajao', 'Ilasamaja', 'Ajao Estate']),
    (31, 'Okota', ['Okota', 'Ire-Akari', 'Oke-Afa', '=Ago Palace, east of Ago Palace Way']),
    (32, 'Oshodi-Mafoluku', ['Oshodi', 'Mafoluku', 'Shogunle', '=Airport (MMIA) south', '=Ago Palace east']),
    (33, 'Airport (MMIA)', ['Airport (MMIA)']),
    (34, 'Ikeja GRA-Cantonment', ['Ikeja GRA', 'Ikeja Cantonment', 'Onigbongbo', 'Ikeja Along']),
    (35, 'Computer Village-Allen-Maryland', ['Computer Village', 'Allen-Opebi', '=Oregun, south of Opebi Road', 'Maryland', 'Mende', 'Ojota']),
    (36, 'Alausa-Oregun-Ogba', ['Alausa', 'Oregun', 'Agidingbi', 'Ogba']),
    (37, 'Agege-Ifako-Ijaiye', ['Orile Agege', 'Agege', 'Pen Cinema', 'Oko-Oba', 'Ifako-Ijaiye', 'Fagba', 'Iju', '=Iyana Ipaja north-east']),
    (38, 'Ketu-Mile 12', ['Ketu', 'Mile 12', 'Kosofe', 'Alapere', 'Ikosi', 'Agboyi', 'Irawo', 'Owode Onirin']),
    (39, 'Magodo-Omole-Berger', ['Magodo', 'Shangisha', 'Omole', 'Ojodu', 'Berger', 'Olowora']),
    (40, 'Agbado-Oke Odo', ['Alagbado', 'Alakuko', 'Ijaiye', 'Ojokoro', 'Abule Egba', 'Meiran', 'Ekoro', 'Oke Odo']),
    (41, 'Ipaja-Ayobo', ['Ipaja', 'Ayobo', 'Abesan', 'Baruwa', 'Gowon Estate', 'Command', 'Iyana Ipaja', '=Alagbado south', '=Alagbado south-west']),
    (42, 'Egbeda-Idimu', ['Egbeda', 'Akowonjo', 'Shasha', 'Dopemu', 'Idimu']),
    (43, 'Ikotun-Igando', ['Ikotun', 'Igando', 'Egan', 'Akesan', 'Egbe']),
    (44, 'Ejigbo', ['Ejigbo', '=Jakande Estate (Isolo) north-west']),
    (45, 'Ago Palace-Abaranje-Ijegun', ['Ago Palace', 'Jakande Estate (Isolo)', 'Abaranje', 'Ijegun', 'Isheri-Osun']),
    (46, 'Agric-Isawo-Owutu', ['Isawo', 'Owutu', 'Majidun', 'Ajegunle (Ikorodu Rd)', 'Agric (Ikorodu)', 'Ogolonto']),
    (47, 'Ikorodu Town', ['Ikorodu town', 'Ebute (Ikorodu)', 'Ipakodo', 'Ibeshe', 'Itamaga']),
    (48, 'Odogunyan-Ogijo', ['Odogunyan', 'Ogijo']),
    (49, 'Igbogbo-Bayeku-Ita Elewa', ['Ita Elewa', 'Igbogbo', 'Bayeku', 'Ofin', 'Igbopa']),
    (50, 'Ijede-Gberigbe', ['Ijede', 'Gberigbe', 'Oke Agbo', 'Ipakan', 'Oyewaw', '=Ita Elewa, east of Ijede Road']),
    (51, 'Imota-Ewu-Elepe', ['Imota', 'Ewu-Elepe']),
]
FULL, PREF = {}, []
for d, _, mem in D51:
    for m in mem:
        if m.startswith('='):
            FULL[m[1:]] = d
        else:
            PREF.append((m, d))
PREF.sort(key=lambda t: -len(t[0]))


def district_of(name):
    if name in FULL:
        return FULL[name]
    for m, d in PREF:
        if name == m or re.match(re.escape(m) + r'[ ,]', name):
            return d
    return 0


NP = int(place.max())
own = np.zeros(NP + 1, np.int32)
for p, q in PL.items():
    own[p] = district_of(q['name'])
# a place no list names (open land, scraps) joins the district it shares the longest land border with, round after round
pairs = collections.Counter()
for a, b in ((place[:, 1:], place[:, :-1]), (place[1:, :], place[:-1, :])):
    m = (a != b) & (a > 0) & (b > 0)
    for p, q in zip(a[m], b[m]):
        pairs[(p, q)] += 1
        pairs[(q, p)] += 1
for _ in range(50):
    best = {}
    for (p, q), c in pairs.items():
        if own[p] == 0 and own[q] > 0 and c > best.get(p, (0, 0))[0]:
            best[p] = (c, own[q])
    if not best:
        break
    for p, (_, d) in best.items():
        own[p] = d
D = own[place]
D[place == 0] = 0

# check: every place EARTH-CHECK names is found
for d, nm, mem in D51:
    for m in mem:
        m = m.lstrip('=')
        if not any(q['name'] == m or q['name'].startswith(m + ' ') or q['name'].startswith(m + ',') for q in PL.values()):
            print('  (no place named %r for %d %s)' % (m, d, nm))

dpoly = {}
for g, v in features.shapes(D.astype(np.int32), mask=D > 0, transform=AFF):
    dpoly.setdefault(int(v), []).append(shape(g))
dpoly = {d: unary_union(L).intersection(CLIP) for d, L in dpoly.items()}
dpoly = {d: g for d, g in dpoly.items() if g.area > 0}
ids = sorted(dpoly)
simple = dict(zip(ids, shapely.coverage_simplify([dpoly[d] for d in ids], 60)))
NAME = {d: nm for d, nm, _ in D51}
dists = []
for d in ids:
    g = simple[d]
    big = max(getattr(dpoly[d], 'geoms', [dpoly[d]]), key=lambda p: p.area)
    lab = big.representative_point() if not big.centroid.within(big) else big.centroid
    dists.append({'n': d, 'name': NAME[d], 'rings': rings_of(g), 'at': R1(gidi([lab.coords[0]]))[0],
                  'km2': round(dpoly[d].area / 1e6 / SCALE ** 2, 2)})
print(len(dists), 'districts in the frame')


def group_poly(pred):
    m = np.isin(place, [p for p, q in PL.items() if pred(q)]) & (place > 0)
    return unary_union([shape(g) for g, v in features.shapes(m.astype(np.uint8), mask=m, transform=AFF) if v == 1])


def border(A, B):
    g = A.boundary.intersection(B.boundary)
    g = linemerge([p for p in getattr(g, 'geoms', [g]) if p.geom_type == 'LineString']) if not g.is_empty else g
    return lines_of(g, 60) if not g.is_empty else []


starts = lambda *names: (lambda q: any(q['name'] == n or q['name'].startswith(n + ' ') or q['name'].startswith(n + ',') for n in names))
inD = lambda d, pred: (lambda q: own[q['id']] == d and pred(q))
# EARTH-CHECK.md, "Still unsure" and the lines marked *to trace*. kind: unsure = a question to settle, trace = a named
# line to draw on the board against the fabric.
LINES = [
    ('unsure', 'Agbado-Oke Odo east edge: Lagos-Abeokuta Expressway or the old Agege-Ijoko railway?', dpoly.get(40), dpoly.get(37)),
    ('unsure', 'Command: Agbado-Oke Odo or Ipaja-Ayobo?', group_poly(starts('Command')), dpoly.get(40)),
    ('unsure', 'Ago Palace-Abaranje-Ijegun is large: cut here, Ago Palace Way estates / Abaranje-Ijegun?',
     group_poly(inD(45, starts('Ago Palace', 'Jakande Estate (Isolo)'))), group_poly(inD(45, lambda q: not starts('Ago Palace', 'Jakande Estate (Isolo)')(q)))),
    ('unsure', 'Surulere / Aguda: a street line, not a wall (Ogunlana, Adelabu): where?', dpoly.get(13), dpoly.get(12)),
    ('unsure', 'Itire / Mushin: Lawanson Road or Itire Road? (no wall on the ground)', dpoly.get(14), dpoly.get(15)),
    ('unsure', 'Mushin / Ilupeju: Agege Motor Road or Palm Avenue? (no wall on the ground)', dpoly.get(15), dpoly.get(29)),
    ('unsure', 'Oworonshoki: its own waterfront place (like Makoko) or part of Shomolu-Bariga?',
     group_poly(starts('Oworonshoki')), group_poly(inD(27, lambda q: not starts('Oworonshoki')(q)))),
    ('unsure', 'Ita Elewa: Ikorodu Town or Igbogbo-Bayeku? (check Street View along Ijede Road)', group_poly(starts('Ita Elewa')), dpoly.get(47)),
    ('unsure', 'Boundary west of the expressway: Kirikiri-Tin Can or Ajegunle? (houses, not port)',
     group_poly(starts('Boundary (Ajegunle), west of Apapa-Oworonshoki Expressway')), dpoly.get(9)),
    ('trace', 'To trace: Mushin west, the railway by Ladipo and Papa Ajao', dpoly.get(15), dpoly.get(30)),
    ('trace', 'To trace: Itire-Lawanson / Surulere, Lawanson Road / Itire Road', dpoly.get(14), dpoly.get(13)),
    ('trace', 'To trace: Ikotun-Igando south, the edge of Abaranje along Igando-LASU Road', dpoly.get(43), dpoly.get(45)),
    ('trace', 'To trace: Ejigbo south, Jakande Estate\'s north edge', dpoly.get(44), dpoly.get(45)),
    ('trace', 'To trace: Lekki Phase 1 / Agungi', dpoly.get(23), dpoly.get(24)),
    ('trace', 'To trace: Agric-Isawo-Owutu east, the stream and open band at about 3.48', dpoly.get(46), dpoly.get(47)),
    ('trace', 'To trace: Ikorodu Town north, Odogunyan\'s edge on Sagamu Road (about 6.645)', dpoly.get(47), dpoly.get(48)),
]
lines = []
for kind, q, A, B in LINES:
    L = border(A, B) if A is not None and B is not None else []
    if not L:
        print('  (no shared line for: %s)' % q)
    for pts in L:
        lines.append({'k': kind, 'q': q, 'p': pts})
# lines inside a district with no place border to follow: a note at the spot
notes = []
if 20 in dpoly:
    c = dpoly[20].representative_point()
    notes.append({'k': 'trace', 'q': 'To trace: Lagos Island quarters, Broad Street / Idumagbo Avenue (office strip / old town) and the Tafawa Balewa Square-Onikan edge',
                  'at': R1(gidi([c.coords[0]]))[0]})
print(len(lines), 'unsure or to-trace lines,', len(notes), 'notes')

# ------------------------------------------------------------------ 4. the 819 places, as labels
labels = []
for p, q in PL.items():
    x, y = q['x'], q['y']
    if not CLIP.contains(shapely.Point(x, y)):
        continue
    labels.append({'n': q['name'], 'at': R1(gidi([(x, y)]))[0], 'r': q['roof_km2'], 'd': int(own[p]), 'f': q['fabric']})
labels.sort(key=lambda o: -o['r'])
print(len(labels), 'place labels in the frame (of', len(PL), ')')

out = {'frame': {'w': FRAME[0], 'h': FRAME[1], 'scale': SCALE, 'real_sw_utm31': [FU, FV], 'corners_latlon': NW['frame']['corners_latlon']},
       'roads': roads, 'water': wat, 'districts': dists, 'lines': lines, 'notes': notes, 'places': labels}
path = os.path.join(ROOT, 'web', 'frame-study.js')
open(path, 'w').write('window.FRAME=' + json.dumps(out, separators=(',', ':'), ensure_ascii=False) + ';')
print('-> web/frame-study.js', round(os.path.getsize(path) / 1e6, 2), 'MB')
