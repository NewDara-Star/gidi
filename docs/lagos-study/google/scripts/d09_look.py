"""Every scripted number in docs/lagos-study/google/d09.md (the Google look for d09 Ayégúnlẹ̀).

Run: ~/.venvs/gidi/bin/python -I docs/lagos-study/google/scripts/d09_look.py

Reads map/d09/district.json, map/d09/plan.json and map/d09/STREETS.md only (nothing is written). Prints:
- each looked-at spot (satellite S*, Street View V*): its lat,lon turned into Gidi x,y with the frame of
  scripts/working_bar.gidi() (UTM 31N, x = (east - 500525)/3, y = 10500 - (north - 707825)/3), whether it is inside
  the d09 outline (and how far outside), and "ours" in a 30 m Gidi circle round it: houses whose footprint centroid
  is in the circle, the roof cover of the circle (footprints clipped to it), the median footprint, kinds, storeys,
  places (any part in the circle), plots, and the nearest road with its real name from STREETS.md;
- district-wide counts the note quotes: record types, house kinds and storeys, places, plots, roads by kind;
- the Google street names read on Maps, each searched in STREETS.md by a core pattern of the name (NAMES below), case ignored.
Real names are in this file and the note only, never in map records.
"""
import collections
import json
import os
import re
import statistics

from pyproj import Transformer
from shapely.geometry import MultiPolygon, Point, Polygon, LineString
from shapely.ops import unary_union

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
D = os.path.join(ROOT, 'map', 'd09')
R30 = 30.0

# (code, lat, lon). S*: the centre of each satellite view, as typed in its URL. F*: a feature inside a view, its
# position read by eye off the screen (pixels from the view's centre at 1.18 m/px for z17 and 0.51 m/px for z18), so
# good to about 20-40 m. V*: Street View; the pano's own position where the URL gave it, otherwise the requested point
# (Google opens the nearest pano to it). N*: requested points with no Street View imagery.
SPOTS = [
    ('S1', 6.47400, 3.34500),   # Amukoko north, z18
    ('S2', 6.47200, 3.34600),   # Amukoko canal
    ('S3', 6.46850, 3.33700),   # Cemetery Rd / Labaka grid
    ('S4', 6.46400, 3.34300),   # Yusuf Esan / Fagbemi, the Main Canal
    ('S5', 6.46250, 3.35300),   # Layinka / La-gold, the east canal
    ('S6', 6.46200, 3.36000),   # tank farm (outside)
    ('S7', 6.46450, 3.35650),   # east lobe: broad canal, Ladipo marketplace ground
    ('S8', 6.45800, 3.32400),   # Signals Barracks, the canal's west end
    ('S9', 6.45650, 3.33100),   # Canal Rd, Ajeromi General Hospital
    ('S10', 6.45600, 3.34100),  # Ajegunle core: Cemetery Market, LG council
    ('S11', 6.45650, 3.35100),  # Boundary: Malu Rd, Navy quarters
    ('S12', 6.45050, 3.32200),  # Berger side: James Igbe canal, St Margaret
    ('S13', 6.45250, 3.33400),  # Okito / God in Action canal, Nathaniel Idowu field
    ('S14', 6.45100, 3.34600),  # Tolu Rd, canal into the Waterside creek
    ('S15', 6.44300, 3.34100),  # Olodi-Apapa, the north-south channel
    ('S16', 6.44600, 3.33000),  # Idewu / Oba Olu-Iwa west, Sifax
    ('S17', 6.43950, 3.33700),  # Maracana, the creek edge
    ('S18', 6.46100, 3.33300),  # Ojo Rd west, the Main Canal
    ('S19', 6.46500, 3.32550),  # Suru Alaba: expressway, rail, market
    ('S20', 6.44800, 3.35200),  # Waterside creek, Apapa side (east)
    ('S21', 6.46950, 3.35000),  # Amukoko east: Iganmu Rd, Alakoto
    ('S22', 6.45780, 3.33200),  # the canal at z18
    ('S23', 6.45450, 3.35000),  # Boundary Market at z18
    ('F1', 6.45410, 3.35150),   # Boundary Market sheds
    ('F2', 6.45340, 3.34880),   # Goriola Primary School (salmon block, sandy yard)
    ('F3', 6.45300, 3.35060),   # dark canal south of Goriola, "Water Side Market"
    ('F4', 6.45700, 3.33260),   # the canal (green strip) at z18
    ('F5', 6.47140, 3.34680),   # Amukoko canal (dark water)
    ('F6', 6.46250, 3.33300),   # Main Canal (green strip) north of Ojo Rd
    ('F7', 6.46410, 3.35560),   # east lobe broad canal
    ('F8', 6.46390, 3.35870),   # Ladipo marketplace bare ground
    ('F9', 6.45760, 3.35360),   # Navy married quarters field
    ('F10', 6.45410, 3.35490),  # Nigerian Bottling Company blue roofs
    ('F11', 6.44840, 3.35070),  # Waterside creek
    ('F12', 6.45870, 3.32220),  # Signals Barracks salmon-roofed rows
    ('F13', 6.45660, 3.32220),  # green open ground, the canal's west end
    ('F14', 6.44280, 3.32660),  # Sifax off-dock container lot
    ('F15', 6.43950, 3.34010),  # Maracana pitch
    ('F16', 6.44370, 3.34120),  # Olodi-Apapa north-south channel
    ('F17', 6.45360, 3.33260),  # Nathaniel Idowu Football Field
    ('F18', 6.45390, 3.33430),  # St Mary's Catholic Church and its yard
    ('F19', 6.45800, 3.34390),  # Cemetery Market (orange long-span rows)
    ('F20', 6.46440, 3.32660),  # Suru Alaba Market sheds
    ('F21', 6.46340, 3.32610),  # St Kizito church pond and green
    ('F22', 6.46940, 3.34970),  # Alakoto / Alayaki St market rows
    ('F23', 6.45180, 3.31970),  # Berger yard, bare lot
    ('F24', 6.45080, 3.32340),  # James Igbe St canal
    ('F25', 6.45540, 3.33250),  # Ajeromi General Hospital
    ('F26', 6.45230, 3.35090),  # Waterside creek north, where the canal joins
    ('F27', 6.46300, 3.34300),  # Main Canal (dark water) by Yusuf Esan St
    ('V1', 6.4553785, 3.349517),
    ('V2', 6.45450, 3.33700),
    ('V3', 6.44750, 3.33400),
    ('V4', 6.4683154, 3.339922),
    ('V5', 6.46150, 3.33300),
    ('V6', 6.44850, 3.34200),
    ('V7', 6.46730, 3.33300),
    ('V8', 6.45580, 3.35300),
    ('V9', 6.45550, 3.34200),
    ('V10', 6.44250, 3.34300),
    ('V11', 6.4699428, 3.348226),
    ('V12', 6.44630, 3.33600),
    ('N1', 6.45650, 3.32600),
    ('N2', 6.45720, 3.33000),
    ('N3', 6.45150, 3.35150),
]

# big roads Google names that STREETS.md lacks: a point on each, read by eye off the satellite views as the F* points
ROADS = [
    ('Sanwo-olo Rd (V9)', 6.45550, 3.34200),
    ('Oba Olu-Iwa Rd', 6.44830, 3.33140),
    ('Okito St', 6.45330, 3.33420),
    ('Cardoso St', 6.45440, 3.32900),
    ('Canal Rd', 6.45620, 3.32650),
    ('Oba Abdulfatai Aremu Aromire St', 6.45050, 3.34620),
    ('Ago-Hausa St', 6.45570, 3.33240),
    ('Kalejaiye Adeboye', 6.45350, 3.34140),
]

# (name as Google shows it, a regular expression searched in each real name of STREETS.md's road table, case
# ignored; anchored where a bare word would hit a longer name, e.g. Epe in Aiyepe)
NAMES = [
    ('Ojo Rd', 'Ojo Road'), ('Cementry Rd', 'Cemetery Road'), ('Mosafejo Rd', 'Mosafejo'),
    ('Sanwo-olo Rd', 'Sanwo'), ('Oba Abdulfatai Aremu Aromire St', 'Aromire'), ('Malu Rd', 'Malu Road'),
    ('Orodu St', 'Orodu'), ('Goriola St', 'Goriola'), ('Okito St', 'Okito'), ('Kalejaiye Adeboye', 'Kalejaiye'),
    ('Cardoso St', 'Cardoso'), ('Canal Rd', 'Canal'), ('Ago-Hausa St', 'Hausa'), ('Oba Olu-Iwa Rd', 'Olu-Iwa'),
    ('Idewu St', 'Idewu'), ('Wilmer Cres', 'Wilmer'), ('Ohuntan St', 'Ohuntan'), ('Tolu Rd', 'Tolu'),
    ('Boundary Rd', 'Boundary'), ('Baale Alayabiagba St', 'Alayabiagba'), ('Ojora St', 'Ojora'),
    ('Iyalode St', 'Iyalode'), ('Nosamu St', 'Nosamu'), ('Layinka St', r'^Layinka'), ('Gaskiya Rd', r'^Gaskiya Road'),
    ('Iganmu Rd', 'Iganmu'), ('Ludun St', r'^Ludun\b'), ('Olojowon St', 'Olojowon'), ('Labaka St', 'Labaka'),
    ('Ateboh Cl', 'Ateboh'), ('Muyibi St', 'Muyibi'), ('Ladega St', 'Ladega'), ('Ashogbon St', 'Ashogbon'),
    ('Mokoya St', 'Mokoya'), ('Temidire St', 'Temidire'), ('Ojoku St', 'Ojoku'), ('Yusuf Esan St', 'Yusuf Esan'),
    ('Fagbemi St', 'Fagbemi'), ('Agbamu St', 'Agbamu'), ('Market St', 'Market Street'), ('Turner St', 'Turner'),
    ('Olatunji St', 'Olatunji'), ('Muri Ojora St', 'Muri Ojara'), ('James Igbe St', 'Igbe'),
    ('Chief Titus Ufondu St', 'Ufondu'), ('God In Action Ave', 'God In Action'), ('Peter St', 'Peter'),
    ('Erelu Mojisola St', 'Mojisola'), ('Adekeye St', 'Adekeye'), ('Oyedeji St', 'Oyedeji'),
    ('Alh. Owoyemi St', 'Owoyemi'), ('Charles Ave', 'Charles'), ('Barracks Ln', 'Barracks'),
    ('Salimonu Bakare St', 'Salimonu'), ('Itire St', r'^Itire Street'), ('Turner Eradiri St', 'Eradiri'),
    ('Layode St', 'Layode'), ('Sufianu St', 'Sufianu'), ('Akogun St', 'Akogun'), ('Salawu St', 'Salawu'),
    ('Otunba Gbadamosi St', 'Gbadamosi'), ('Industrial Rd', 'Industrial'), ('Mission St', 'Mission'),
    ('Rorobi St', 'Rorobi'), ('Taiwo St', 'Taiwo'), ('Oluwa St', 'Oluwa Street'), ('Idi St', r'^Idi\b'),
    ('Molade St', 'Molade'), ('Oremeji St', 'Oremeji'), ('Oshodi St', 'Oshodi'), ('Ebenezer St', 'Ebenezer'),
    ('Okunowa St', 'Okunowa'), ('Ojumola St', 'Ojumola'), ('Oyebo St', 'Oyebo'), ('Apasa St', 'Apasa'),
    ('Aiyepe St', 'Aiyepe'), ('Edidi St', 'Edidi'), ('Imam St', 'Imam'), ('Sanni Aro St', r'^Sanni Aro'),
    ('Adejiyan St', 'Adejiyan'), ('Otua St', 'Otua'), ('Ayinde St', 'Ayinde'), ('Salami St', r'^Salami\b'),
    ('Wowo St', 'Wowo'), ('Ashafa St', 'Ashafa'), ('Mensah St', 'Mensah'), ('Akinbo St', 'Akinbo'),
    ('Musibau Oluwa', 'Musibau'), ('Makaila Kolawole', 'Kolawole'), ('John Okorie St', 'Okorie'),
    ('Yaya Cres', 'Yaya'), ('Fasasi St', 'Fasasi'), ('Abayomi St', 'Abayomi'), ('Emmanuel Ave', 'Emmanuel'),
    ('Redemption Ave', 'Redemption'), ('Freedom St', 'Freedom'), ('Ajibola Odunsi St', 'Odunsi'),
    ('Police Ln', 'Police'), ('Kehinde St', 'Kehinde'), ('Rabiu Oluwa', 'Rabiu'), ('Ikogwe St', 'Ikogwe'),
    ('Alayaki St', 'Alayaki'), ('Epe St', r'^Epe\b'), ('Adekunle Deen St', 'Deen'), ('Osime St', 'Osime'),
    ('Raimi St', 'Raimi'), ('Moshalashi St', 'Moshalashi'), ('Asemota St', 'Asemota'), ('Palace Rd', 'Palace'),
    ('Prince Fadina St', 'Fadina'), ('Babatunde St', 'Babatunde'), ('Ogunkoya Shina', 'Ogunkoya'),
    ('Abiola Oluwa St', 'Abiola'), ('Chief Dele Fayemi Rd', 'Fayemi'), ('Igharemu St', 'Igharemu'),
    ('Prince Tajudeen St', 'Tajudeen'), ('Aribo St', 'Aribo'), ('Afolayan St', 'Afolayan'),
    ('Odusanya St', 'Odusanya'), ('Ebunoti St', r'^Ebunot+i'), ('Alaka St', 'Alaka'),
]


def main():
    T = Transformer.from_crs(4326, 32631, always_xy=True)

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
        r['_g'] = LineString(r['centreline'])

    names = {}
    streets = open(os.path.join(D, 'STREETS.md')).read()
    for m in re.finditer(r'^\| (rd-[0-9a-f]+) \| ([^|]+) \| ([a-z_]+) \|', streets, re.M):
        names[m.group(1)] = m.group(2).strip()

    minx, miny, maxx, maxy = ring.bounds
    print('outline: x %.0f-%.0f, y %.0f-%.0f, %.0f m2 (Gidi)' % (minx, maxx, miny, maxy, ring.area))
    print()
    print('SPOTS (r=%.0f Gidi m)' % R30)
    for code, lat, lon in SPOTS:
        x, y = gidi(lat, lon)
        pt = Point(x, y)
        c = pt.buffer(R30, 64)
        ins = ring.contains(pt)
        where = 'inside' if ins else 'OUTSIDE by %.0f Gidi m' % ring.distance(pt)
        hs = [b for b in B if c.contains(b['_g'].centroid)]
        cover = unary_union([b['_g'] for b in B]).intersection(c).area / c.area if B else 0
        med = statistics.median([b['_g'].area for b in hs]) if hs else 0
        kinds = collections.Counter(b['kind'] for b in hs)
        st = collections.Counter(b['storeys'] for b in hs)
        pl = collections.Counter(p['kind'] for p in P if p['_g'].intersects(c))
        pt_plots = collections.Counter(l['kind'] for l in L if l['_g'].intersects(c))
        near = min(RD, key=lambda r: r['_g'].distance(pt))
        nm = names.get(near['id'], '?')
        print('%s %.5f,%.5f -> %.0f,%.0f %s | houses %d cover %.0f%% median %.0f m2 | kinds %s | storeys %s | places %s | plots %s | nearest road %s %s (%s, %.1f m wide) %.0f m off'
              % (code, lat, lon, x, y, where, len(hs), 100 * cover, med, dict(kinds), dict(sorted(st.items())),
                 dict(pl), dict(pt_plots), near['id'], nm, near['kind'], near['width'], near['_g'].distance(pt)))

    print()
    print('DISTRICT')
    print('record types', dict(collections.Counter(r['type'] for r in recs)))
    print('houses', len(B), 'kinds', dict(collections.Counter(b['kind'] for b in B).most_common()))
    print('storeys', dict(sorted(collections.Counter(b['storeys'] for b in B).items())))
    print('house record fields', sorted(set(k for b in B for k in b if not k.startswith('_'))))
    print('median footprint %.1f m2' % statistics.median(b['_g'].area for b in B))
    covers = [unary_union([b['_g'] for b in B]).intersection(Point(*gidi(lat, lon)).buffer(R30, 64)).area
              / (3.14159265 * R30 * R30) for c, lat, lon in SPOTS if c[0] in 'SF' and ring.contains(Point(*gidi(lat, lon)))]
    print('S and F spots inside: %d, median cover in r30 %.0f%%, max %.0f%%' % (len(covers), 100 * statistics.median(covers), 100 * max(covers)))
    print('cover of outline %.2f%%' % (100 * unary_union([b['_g'] for b in B]).intersection(ring).area / ring.area))
    print('places', dict(collections.Counter(p['kind'] for p in P).most_common()))
    print('plots', dict(collections.Counter(l['kind'] for l in L)))
    print('roads by kind', dict(collections.Counter(r['kind'] for r in RD).most_common()))
    print('roads by kind with real width', dict(collections.Counter((r['kind'], r['width']) for r in RD).most_common()))

    print()
    print('STREET NAMES (Google) grepped in STREETS.md road table')
    road_names = sorted(set(names.values()))
    hit, miss = [], []
    for g, core in NAMES:
        found = [n for n in road_names if re.search(core, n, re.I)]
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
        print('  %-34s %.0f,%.0f %s | %s' % (g, x, y, 'inside' if ring.contains(pt) else 'OUTSIDE',
              '; '.join('%s %s %s %.2f m, %.0f m off' % (r['id'], names.get(r['id'], '?'), r['kind'], r['width'],
                                                         r['_g'].distance(pt)) for r in near)))


if __name__ == '__main__':
    main()
