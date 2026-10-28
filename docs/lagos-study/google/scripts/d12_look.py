"""Every scripted number in docs/lagos-study/google/d12.md (the Google look for d12 Agunda).

Run: ~/.venvs/gidi/bin/python -I docs/lagos-study/google/scripts/d12_look.py

Reads map/d12/district.json, map/d12/plan.json and map/d12/STREETS.md, and Google Open Buildings v3 (the Lagos file
and the per-tile confidence thresholds that scripts/working_bar.py reads); nothing is written. Prints:
- each looked-at spot (satellite S*, feature F*, Street View V*, no imagery N*): its lat,lon turned into Gidi x,y with
  the frame of scripts/working_bar.gidi() (UTM 31N, x = (east - 500525)/3, y = 10500 - (north - 707825)/3), whether
  it is inside the d12 outline (and how far outside), and "ours" in a 30 m Gidi circle round it: houses whose
  footprint centroid is in the circle, our roof cover of the circle (footprints clipped to it), the median footprint,
  kinds, storeys, places and plots touching it, the nearest road with its real name from STREETS.md; and Google's roof
  cover of the same circle at its 90%- and 80%-precision confidence thresholds (a per-area figure, so the 1:3 scale
  does not change it);
- district-wide counts the note quotes: record types, house kinds and storeys, places, plots, roads by kind; our cover
  of the outline and Google's at both thresholds;
- the Google street names read on the satellite labels, each searched in STREETS.md by a core pattern (NAMES below);
- for the big roads, the three nearest road records to a point on each.
Real names are in this file and the note only, never in map records.
"""
import collections
import csv
import gzip
import json
import os
import re
import statistics

import shapely
from pyproj import Transformer
from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import unary_union

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
D = os.path.join(ROOT, 'map', 'd12')
GOOGLE = os.path.expanduser('~/gidi-data/research/data/open-buildings-v3/lagos_open_buildings_v3.csv.gz')
THRESHOLDS = os.path.expanduser('~/gidi-data/research/data/open-buildings-v3/thresholds/score_thresholds_s2_level_4.csv')
R30 = 30.0

# (code, lat, lon). S*: the centre of each satellite view, as typed in its URL ("600m" opens at z17, about 1.18 m/px
# by Google's scale bar; "300m" at z18, about 0.5 m/px). F*: a feature inside a view, its position read by eye off the
# screen (pixels from the view's centre at that scale), so good to about 20-40 m. V*: Street View, the pano's own
# position from the URL Google opened. N*: a requested point with no Street View imagery.
SPOTS = [
    ('S1', 6.49800, 3.34500),   # Aguda north, Adelabu St side, z17
    ('S2', 6.49300, 3.34700),   # TCN Akangba substation, Census Market creek, z18
    ('S3', 6.49800, 3.33150),   # Ijesha side: Mogaji St grid, the north canal
    ('S4', 6.49200, 3.32750),   # west edge: Erelu-Danisa St, the expressway
    ('S5', 6.48900, 3.33850),   # Coker-Aguda LG secretariat, Bolaji Banwo St
    ('S6', 6.48400, 3.33050),   # Sanya St, the west canal, the expressway
    ('S7', 6.48400, 3.34150),   # Orile Iganmu: Abata canal, St Thomas of Villanova
    ('S8', 6.47850, 3.33300),   # Coker Rd and the canal bridge
    ('S9', 6.47850, 3.34400),   # Orile: the Lagos-Badagry Expy, the bus stop, police
    ('S10', 6.47400, 3.35400),  # east lobe west: Amukoko creek, Saka Alao, the swamp
    ('S11', 6.46700, 3.35750),  # Ijora Badia: Gaskiya Rd, the dump ground
    ('S12', 6.47600, 3.36000),  # east lobe: the swamp, Ascon/Total depot, Ijora interchange
    ('S13', 6.47400, 3.33600),  # south edge: Coker, St Michael's, NNPC, the expressway
    ('S14', 6.48100, 3.35100),  # north-east edge: the industrial estate over the expressway
    ('S15', 6.47000, 3.35050),  # Iganmu Rd, Alakoto, the east-lobe canal
    ('S16', 6.49350, 3.33750),  # Aguda centre: Central Mosque, the school field
    ('S17', 6.49500, 3.34180),  # Aguda Ultra Modern Market, z18
    ('S18', 6.48450, 3.33950),  # the Abata canal, z18
    ('S19', 6.47900, 3.33280),  # the canal at Coker Rd, z18
    ('S20', 6.47400, 3.35550),  # Saka Alao and the swamp, z18
    ('F1', 6.49550, 3.34220),   # Aguda Ultra Modern Market (orange long-span rows)
    ('F2', 6.49450, 3.34690),   # TCN Akangba transmission substation (gravel yard, gantries)
    ('F3', 6.49350, 3.34730),   # green bush ground south of the substation
    ('F4', 6.49260, 3.34850),   # dark creek behind Census Market (marsh both banks)
    ('F5', 6.49800, 3.33680),   # north canal (dark, green banks), Ijesha side
    ('F6', 6.49160, 3.33310),   # the same canal by Erelu-Danisa St
    ('F7', 6.48360, 3.32970),   # the west canal, north-south by Sanya St
    ('F8', 6.48690, 3.34250),   # the Abata canal, broad green band
    ('F9', 6.48590, 3.34390),   # the Abata canal further east
    ('F10', 6.47880, 3.33330),  # the canal under the Coker Rd bridge
    ('F11', 6.48820, 3.33770),  # Coker-Aguda Local Government secretariat
    ('F12', 6.49120, 3.34010),  # school: sandy field and a blue U-shaped block
    ('F13', 6.49360, 3.34030),  # Aguda Central Mosque
    ('F14', 6.48480, 3.34580),  # St Thomas of Villanova Catholic Church, Abata
    ('F15', 6.49700, 3.33040),  # Ijesha Market
    ('F16', 6.48150, 3.32710),  # Apapa-Oworonshoki Expy on the west edge
    ('F17', 6.48430, 3.32780),  # Sanya Junior Grammar School (blue roofs)
    ('F18', 6.47780, 3.34310),  # Orile bus stop and the rail station over the expressway
    ('F19', 6.47780, 3.34540),  # Orile Police Station
    ('F20', 6.47850, 3.34940),  # cleared rubble lot by CIPM Ave
    ('F21', 6.47680, 3.33580),  # Ajegunle roundabout
    ('F22', 6.47490, 3.33730),  # St Michael's Anglican Church, Coker
    ('F23', 6.47550, 3.33630),  # bare lot by St Michael's
    ('F24', 6.47370, 3.33810),  # NNPC depot by the expressway
    ('F25', 6.47490, 3.35720),  # the swamp (water hyacinth, open-water pools)
    ('F26', 6.47370, 3.35630),  # Saka Alao: a fill heap into the swamp, shacks
    ('F27', 6.47270, 3.35650),  # Badia Nursery and Primary School (orange long roof)
    ('F28', 6.47320, 3.35240),  # Amukoko creek, west of the swamp
    ('F29', 6.47780, 3.35920),  # Ascon/Total depot, trucks and containers
    ('F30', 6.47070, 3.35380),  # the east-lobe canal
    ('F31', 6.46840, 3.35450),  # the east-lobe canal further south, by Barakat Hospital
    ('F32', 6.46630, 3.35990),  # Gaskiya Rd
    ('F33', 6.46390, 3.36210),  # Ijora Badia cleared dump ground with black ponds
    ('F34', 6.46570, 3.35510),  # dark north-south canal, Ijora side
    ('F35', 6.46910, 3.36260),  # Ijora 7up Market
    ('F36', 6.48490, 3.33960),  # the Abata canal at z18
    ('F37', 6.47970, 3.35400),  # big blue factory roof by the expressway
    ('F38', 6.47470, 3.36030),  # Ajeromi Primary School (orange rows on the swamp edge)
    ('V1', 6.49520, 3.34280),   # Adetayo Shode St, Dec 2016 (requested point)
    ('V2', 6.48820, 3.33770),   # Thomas Animashaun St, Nov 2019 (requested point)
    ('V3', 6.4789473, 3.3330108),   # Yisa Oroki St, Jul 2024
    ('V4', 6.4777591, 3.3431254),   # Lagos-Badagry Expy at Orile, Nov 2016
    ('V5', 6.4664200, 3.3599729),   # Gaskiya Rd, Jul 2024
    ('V6', 6.4696739, 3.3509072),   # Iganmu Rd, Dec 2016
    ('V7', 6.4937250, 3.3403002),   # Soloki St, Jul 2024
    ('V8', 6.4900854, 3.3299399),   # Ilamoye St, Nov 2019
    ('V9', 6.4846835, 3.3459768),   # Abata St, Apr 2024
    ('V10', 6.4972133, 3.3308846),  # Alh. Kewulere St, Nov 2019
    ('V11', 6.4750980, 3.3367600),  # Ecwa Church Rd, Jul 2024
    ('V12', 6.4925432, 3.3481749),  # Olatunde Onimole St, Jul 2024
    ('N1', 6.47300, 3.35400),
]

# big roads: a point on each, read by eye off the satellite views as the F* points
ROADS = [
    ('Lagos-Badagry Expy (S9)', 6.47840, 3.34400),
    ('Apapa-Oworonshoki Expy', 6.48150, 3.32710),
    ('Coker Rd', 6.47940, 3.33400),
    ('Babs Animashaun Rd', 6.48310, 3.34820),
    ('Iganmu Rd (V6)', 6.46967, 3.35091),
    ('Gaskiya Rd (V5)', 6.46642, 3.35997),
    ('Adelabu St', 6.49870, 3.34940),
    ('Olatunde Onimole St (V12)', 6.49254, 3.34817),
    ('Bolaji Banwo St', 6.48940, 3.33710),
    ('Brown Rd', 6.48940, 3.33870),
    ('Adetola St', 6.48440, 3.33410),
    ('Mogaji St', 6.49760, 3.33290),
    ('Erelu-Danisa St', 6.49240, 3.32760),
    ('Imam Dauda St', 6.48060, 3.35130),
    ('Jimoh Odutola St', 6.48010, 3.35240),
    ('Eric Moore Rd', 6.48330, 3.35750),
]

# (name as Google shows it, a regular expression searched in each real name of STREETS.md's road table, case ignored)
NAMES = [
    ('Agbonyin Ave', 'Agbo'), ('Nuru Oniwo St', 'Oniwo'), ('Ogundare St', 'Ogundare'), ('Kusimo St', 'Kusimo'),
    ('Adetayo Shode St', 'Shode'), ('Ilorin St', 'Ilorin'), ('Adelabu St', r'^Adelabu Street'),
    ('Alade Shonubi St', 'Shonubi'), ('Olaseni Diyaolu St', 'Diyaolu'), ('Eloseh St', 'Eloseh'), ('Nnobi St', 'Nnobi'),
    ('Odelola St', 'Odelola'), ('Oyelowo Cl', 'Oyelowo'), ('Akpoguma St', 'Akpoguma'),
    ('Olatunde Onimole St', 'Onimole'), ('Babs Animashaun Rd', 'Babs Animashaun'), ('Orunmila Wy', 'Orunmila'),
    ('Idowu Randle', 'Randle'), ('Williams Cl', r'^Williams Close'), ('Martins St', 'Martins'),
    ('Tade Aromolate', 'Tade A'), ('Adenuga St', 'Adenuga'), ('Taiwo Williams', 'Taiwo Williams'),
    ('Alh. Shittu St', 'Shittu Street'), ('Somosu St', 'Somosu'), ('Adebola Ojomu St', 'Ojomu'),
    ('Dimeji Longe Ave', 'Longe'), ('Ayo Elegbede St', 'elegbede'), ('Adefowope St', 'Adefowope'),
    ('Odunjo St', 'Odunjo'), ('Akanbi Arimi St', 'Arimi'), ('Soloki St', 'Soloki'), ('Aiyetoro St', 'Aiyetoro'),
    ('Ade-Omo Olubiyi St', 'Olubiyi'), ('Basiyi St', 'Basiyi'), ('Ramat Timson St', 'Timson'),
    ('Ademola Oki St', r'\bOki\b'), ('Adebowale Cl', 'Adebowale'), ('Alh. Asiri Akofa St', 'Akofa'),
    ('Bolaji Banwo St', 'Banwo'), ('Brown Rd', 'Brown'), ('Efutide St', 'Efutide'), ('Jadesola Oshodi St', 'Jadesola'),
    ('Alhaji Salami St', 'Salami'), ('Ketu St', 'Ketu'), ('Achala St', 'Achala'), ('Babatope St', 'ba+tope'),
    ('Adetola St', 'Adetola'), ('Onikoyi St', 'Onikoyi'), ('Ogunbadero St', 'Ogunbadero'), ('Trimnell St', 'Trimnel'),
    ('Chief Natufe St', 'Natufe'), ('Kernel St', 'Kernel'), ('Oyebode St', 'Oyebode'), ('Falohun St', 'Falohun'),
    ('Emmanuel Cl', 'Emmanuel'), ('Oniwinde St', 'Oniwinde'), ('Santos Estate', 'Santos'),
    ('Muyiwa Opaleye St', 'Opaleye'), ('Balogun Kuku St', 'Kuku'), ('Odogbolu St', 'Odogbolu'),
    ('Savannah St', 'Savannah'), ('Karimu St', 'Karimu'), ('Sanya St', 'Sanya'), ('Iya Rere St', 'Rere'),
    ('Ikare St', 'Ikare'), ('Ijiwere St', 'Ijiwere'), ('Idowu Odunmuga St', 'Odunmuga|Odenuga'),
    ('Alh. Kazeem Akewukewe St', 'Akewukewe'), ('Ayisat Onisemo St', 'Onisemo'), ('Unity Cl', 'Unity'),
    ('Imam Memudu St', 'Memudu'), ('Wosilat-Aina St', 'Wosilat'), ('Imalenfe-Alafia St', 'Alafia'),
    ('Orowunmi St', 'Orowunmi'), ('Alagba St', 'Alagba'), ('Opeloyeru St', 'Opeloyeru'), ('Asiata St', 'Asiata'),
    ('Disu Esan St', r'\bEsan\b'), ('Lasisi St', r'^Lasisi'), ('Nurudeen St', 'Nurudeen'), ('Odusanmi St', 'Odusanmi'),
    ('Orenaike St', 'Orenaike'), ('Igbehin Adun St', 'Igbehin'), ('Abata St', 'Abata'), ('Onyah St', 'Onyah'),
    ('Alh. Jimoh St', r'^Alhaji Jimoh'), ('Alhaji Ajala St', 'Ajala'), ('Alh. Bello Tapa St', 'Tapa'),
    ('Coker Rd', 'Coker'), ('Ecwa Church Rd', 'Ecwa|Church'), ('Yisa Oroki St', 'Oroki'), ('Baale St', r'^Baa?le\b'),
    ('Bello St', r'^Bello'), ('Aliu Olanipekun St', 'Olanipekun'), ('Towolawi Ave', 'Towolawi'),
    ('Austine Onwalu St', 'Onwalu'), ('Alice Tinubu St', 'Tinubu'), ('Arikewuyo St', 'Arikewuyo'), ('Awe St', r'^Awe\b'),
    ('Obanta St', 'Obanta'), ('Ojora Royal Compound', 'Ojora'), ('Alhaji Opere St', 'Opere'),
    ('Lasisi Akinwale St', 'Akinwale'), ('Igbo-Ukwu Dev Cres', 'Igbo.Ukwu'), ('Al Ameen St', 'Ameen'),
    ('Ogunsanya St', 'Ogunsanya'), ('Kadiri St', 'Kadiri'), ('Lagos-Badagry Expy', 'Badagry'),
    ('Isalu-Ijanikin-Animashaun Rd', 'Isalu|Ijanikin'), ('Apapa-Oworonshoki Expy', 'Oworonshoki'),
    ('Iganmu Rd', r'^Iganmu Road'), ('CIPM Ave', 'CIPM'), ('Imam Raji St', 'Raji'), ('Senabu St', 'Senabu'),
    ('Sadiku St', 'Sadiku'), ('Adisatu St', 'Adisatu'), ('Raimi St', 'Raimi'), ('Abbi Ave', 'Abbi'),
    ('Ojo Afeje St', 'Afeje'), ('Adekunle Deen St', 'Deen'), ('Emmanuel Kayode St', 'Kayode Str'),
    ('Fassy Adesina St', 'Adesina'), ('Onilewura St', 'Onilewura'), ('Amai St', 'Amai'), ('Muda St', r'^Muda'),
    ('Mogaji St', 'Mogaji'), ('Jinadu St', 'Jinadu'), ('Ijikoyejo St', 'Ijikoyejo'), ('Imam Suaibu St', 'Suaibu'),
    ('Agbebi St', 'Agbebi'), ('Raufu Baruwa St', 'Baruwa'), ('Wosilatu Dawodu St', 'Wosilatu'),
    ('Itelorun St', 'Itelorun'), ('Jubrila St', 'Jubrila'), ('Alh. Animashaun St', r'^Animashaun|Alhaji Animashaun'),
    ('Oyenuga St', 'Oyenuga'), ('Babs Oni St', 'Babs Oni'), ('Omilani St', 'Omilani'), ('Alh. Kewulere St', 'Kewulere'),
    ('Erelu-Danisa St', 'Danisa'), ('Association Ave', 'Association'), ('Aguntasolo St', 'Aguntasolo'),
    ('Ilamoye St', 'Ilamoye'), ('Airways St', 'Airways'), ('Duro Oyedoyin St', 'Oyedoyin'), ('Shonde St', 'Shonde'),
    ('Obalodu St', 'Obalodu'), ('Alubarika St', 'Alubarika'), ('Wale Shotunde Cl', 'Shotunde'),
    ('Obashola Ajijola Ave', 'Ajijola'), ('Alh. Sulaimon St', 'Sulaimon'), ('Solo Ogun St', 'Solo Ogun'),
    ('Joel Ogunlade St', 'Ogunlade'), ('Adeshina St', 'Adeshina'), ('Irepodun St', 'Irepodun'),
    ('Wole Cole St', 'Cole'), ('Agboola St', 'Agboola'), ('Adedoyin St', 'Adedoyin'), ('Alh. Olakunle St', 'Olakunle'),
    ('Olufemi Shokan St', 'Shokan'), ('Oladimeji St', 'Oladimeji'), ('Kehinde St', 'Kehinde'),
    ('Gaskiya Rd', r'^Gaskiya Road'), ('Akorede St', 'Akorede'), ('Fadani St', 'Fadani'), ('Matiminu St', 'Matiminu'),
    ('Amusu St', 'Amusu'), ('Adeboye St', 'Adeboye'), ('Adeyemi St', 'Adeyemi'), ('Afolabi Alasa St', 'Alasa'),
    ('Oliyide St', 'Oliyide'), ('Ojora St', r'^Ojora Street'), ('Sango St', 'Sango'), ('Ladejobi St', 'Ladejobi'),
    ('Giwa St', 'Giwa'), ('Obale St', 'Obale'), ('Sule Ln', r'^Sule'), ('Olojowon St', 'Olojowon'),
    ('Olodan St', 'Olodan'), ('Sari-Iganmu Rd', 'Sari'), ('Rafiu Banana St', 'Banana'), ('Ireti Owoseni St', 'Owoseni'),
    ('Adefisayo St', 'Adefisayo'), ('Orisha St', 'Orisha'), ('Afagbon St', 'Afagbon'), ('Adeolu St', 'Adeolu'),
    ('Moshalashi St', 'Moshalashi'), ('Imam Dauda St', 'Dauda'), ('Jimoh Odutola St', 'Odutola'),
    ('Eric Moore Rd', 'Eric Moore'),
]


def main():
    T = Transformer.from_crs(4326, 32631, always_xy=True)
    inv = Transformer.from_crs(32631, 4326, always_xy=True)

    def gidi(lat, lon):
        u, v = T.transform(lon, lat)
        return (u - 500525) / 3, 10500 - (v - 707825) / 3

    dist = json.load(open(os.path.join(D, 'district.json')))['records'][0]
    ring = MultiPolygon([Polygon(o) for o in dist['outline']]).buffer(0)
    recs = json.load(open(os.path.join(D, 'plan.json')))['records']
    B = [r for r in recs if r['type'] == 'building']
    P = [r for r in recs if r['type'] == 'place']
    L = [r for r in recs if r['type'] == 'plot']
    RD = [r for r in recs if r['type'] == 'road']
    for b in B:
        b['_g'] = Polygon(b['footprint']).buffer(0)
    for p in P:
        p['_g'] = unary_union([Polygon(a).buffer(0) for a in p['area']])
    for l in L:
        l['_g'] = Polygon(l['outline']).buffer(0)
    for r in RD:
        r['_g'] = LineString([q[:2] for q in r['centreline']])
    OURS = unary_union([b['_g'] for b in B])

    names = {}
    streets = open(os.path.join(D, 'STREETS.md')).read()
    for m in re.finditer(r'^\| (rd-[0-9a-f]+) \| ([^|]+) \| ([a-z_]+) \|', streets, re.M):
        names[m.group(1)] = m.group(2).strip()

    # Google Open Buildings in the outline's box (plus 100 Gidi m, so circles at the edge are whole), at the tile's
    # 80%- and 90%-precision thresholds, as scripts/working_bar.py reads them
    minx, miny, maxx, maxy = ring.bounds
    (w, n), (e, s) = (inv.transform(500525 + 3 * (minx - 100), 707825 + 3 * (10500 - (miny - 100))),
                      inv.transform(500525 + 3 * (maxx + 100), 707825 + 3 * (10500 - (maxy + 100))))
    lon0, lat0 = inv.transform(500525 + 3 * ring.centroid.x, 707825 + 3 * (10500 - ring.centroid.y))
    t80 = t90 = None
    for r in csv.DictReader(open(THRESHOLDS)):
        if shapely.from_wkt(r['geometry']).contains(Point(lon0, lat0)):
            t80, t90 = float(r['confidence_threshold_80%_precision']), float(r['confidence_threshold_90%_precision'])
    g80, g90 = [], []
    with gzip.open(GOOGLE, 'rt') as f:
        for r in csv.DictReader(f):
            c, la, lo = float(r['confidence']), float(r['latitude']), float(r['longitude'])
            if c < t80 or not (w <= lo <= e and s <= la <= n):
                continue
            g = shapely.transform(shapely.from_wkt(r['geometry']), lambda a: [gidi(y, x) for x, y in a])
            g80.append(g)
            if c >= t90:
                g90.append(g)
    G80, G90 = unary_union(g80), unary_union(g90)

    print('outline: x %.0f-%.0f, y %.0f-%.0f, %.0f m2 (Gidi)' % (minx, maxx, miny, maxy, ring.area))
    print('Google tile thresholds: 90%% precision %.3f, 80%% precision %.3f; buildings in the box %d (90%%) %d (80%%)'
          % (t90, t80, len(g90), len(g80)))
    print()
    print('SPOTS (r=%.0f Gidi m)' % R30)
    rows = []
    for code, lat, lon in SPOTS:
        x, y = gidi(lat, lon)
        pt = Point(x, y)
        c = pt.buffer(R30, 64)
        ins = ring.contains(pt)
        where = 'inside' if ins else 'OUTSIDE by %.0f Gidi m' % ring.distance(pt)
        hs = [b for b in B if c.contains(b['_g'].centroid)]
        cover = OURS.intersection(c).area / c.area
        gc90, gc80 = G90.intersection(c).area / c.area, G80.intersection(c).area / c.area
        med = statistics.median([b['_g'].area for b in hs]) if hs else 0
        kinds = collections.Counter(b['kind'] for b in hs)
        st = collections.Counter(b['storeys'] for b in hs)
        pl = collections.Counter(p['kind'] for p in P if p['_g'].intersects(c))
        pt_plots = collections.Counter(l['kind'] for l in L if l['_g'].intersects(c))
        near = min(RD, key=lambda r: r['_g'].distance(pt))
        nm = names.get(near['id'], '?')
        rows.append((code, ins, cover, gc90, gc80))
        print('%s %.5f,%.5f -> %.0f,%.0f %s | houses %d cover %.0f%% (Google %.0f-%.0f%%) median %.0f m2 | kinds %s | '
              'storeys %s | places %s | plots %s | nearest road %s %s (%s, %.1f m wide) %.0f m off'
              % (code, lat, lon, x, y, where, len(hs), 100 * cover, 100 * gc90, 100 * gc80, med, dict(kinds),
                 dict(sorted(st.items())), dict(pl), dict(pt_plots), near['id'], nm, near['kind'], near['width'],
                 near['_g'].distance(pt)))

    print()
    print('DISTRICT')
    print('record types', dict(collections.Counter(r['type'] for r in recs)))
    print('houses', len(B), 'kinds', dict(collections.Counter(b['kind'] for b in B).most_common()))
    print('storeys', dict(sorted(collections.Counter(b['storeys'] for b in B).items())))
    print('house record fields', sorted(set(k for b in B for k in b if not k.startswith('_'))))
    print('median footprint %.1f m2' % statistics.median(b['_g'].area for b in B))
    sf = [r for r in rows if r[0][0] in 'SF' and r[1]]
    print('S and F spots inside: %d, our cover in r30 median %.0f%% max %.0f%%; Google at 90%% median %.0f%% max %.0f%%'
          % (len(sf), 100 * statistics.median(r[2] for r in sf), 100 * max(r[2] for r in sf),
             100 * statistics.median(r[3] for r in sf), 100 * max(r[3] for r in sf)))
    print('S and F spots inside where Google at 90%% has more than twice our cover: %d'
          % sum(1 for r in sf if r[3] > 2 * r[2]))
    print('cover of outline: ours %.2f%%, Google %.2f%% (90%%) - %.2f%% (80%%)'
          % (100 * OURS.intersection(ring).area / ring.area, 100 * G90.intersection(ring).area / ring.area,
             100 * G80.intersection(ring).area / ring.area))
    print('places', dict(collections.Counter(p['kind'] for p in P).most_common()))
    print('plots', dict(collections.Counter(l['kind'] for l in L)))
    print('roads by kind', dict(collections.Counter(r['kind'] for r in RD).most_common()))
    print('roads by kind with real width', dict(collections.Counter((r['kind'], r['width']) for r in RD).most_common()))

    print()
    print('STREET NAMES (Google) grepped in STREETS.md road table')
    road_names = sorted(set(names.values()))
    hit, miss = [], []
    for g, core in NAMES:
        found = [nm for nm in road_names if re.search(core, nm, re.I)]
        (hit if found else miss).append((g, found))
    for g, found in hit:
        print('  hit  %-34s %s' % (g, '; '.join(found)))
    for g, found in miss:
        print('  MISS %s' % g)
    print('names %d: hit %d, miss %d' % (len(NAMES), len(hit), len(miss)))

    print()
    print('BIG ROADS Google names, our nearest road records (3 nearest)')
    for g, lat, lon in ROADS:
        x, y = gidi(lat, lon)
        pt = Point(x, y)
        near = sorted(RD, key=lambda r: r['_g'].distance(pt))[:3]
        print('  %-30s %.0f,%.0f %s | %s' % (g, x, y, 'inside' if ring.contains(pt) else
                                             'OUTSIDE by %.0f' % ring.distance(pt),
              '; '.join('%s %s %s %.2f m, %.0f m off' % (r['id'], names.get(r['id'], '?'), r['kind'], r['width'],
                                                         r['_g'].distance(pt)) for r in near)))


if __name__ == '__main__':
    main()
