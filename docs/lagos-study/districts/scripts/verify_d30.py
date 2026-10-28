"""Re-check the data claims of docs/lagos-study/districts/d30.md (scout note, 27 Oct).

Run:  ~/.venvs/gidi/bin/python -I <this file>
Prints one line per claim: id | what the note states | what the data gives.
Reads: web/frame-study.js, map/d15/{district,plan}.json, map/d14/district.json,
docs/lagos-study/{roads/places.csv,roads/EARTH-CHECK.md,roads/NAMES.md,LIVING.md,STUDY.md},
docs/lagos-lgas-research.md, Overture parquet under ~/gidi-data, and the scout's saved
Overpass answers (osm.json, osm2.json, osmroads.json in ~/gidi-data/research/data/overpass-d30-27oct; not re-fetched).
"""
import collections, csv, json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OSM = os.path.expanduser('~/gidi-data/research/data/overpass-d30-27oct')  # the scout's Overpass answers of 27 Oct, not re-fetched
from verify_common import *  # noqa: F401,F403  (frame, d15 cut, gidi transform)
from shapely.geometry import box
from shapely.ops import unary_union, substring

REPO = '/Users/Star/gidi'
def out(cid, stated, found):
    print(f'{cid:5} | stated: {stated} | found: {found}')
def gm(la, lo):
    x, y = G(la, lo); return f'({x:.0f}, {y:.0f})'

# ---------- section 1: frame, cut, lobe ----------
pts30 = fpts(30)
print('== 1. frame, cut')
out('C1', '1.29 km2 game, 11.6 real, 85 points, bbox x 11325-12992 y 4858-6692',
    f'{frame30.area/1e6:.3f} km2, real {frame30.area*9/1e6:.2f}, {len(set(pts30))} points, bbox {[round(v) for v in frame30.bounds]}, frame name "{D[30]["name"]}"')
cut = frame30.intersection(o15)
out('C2', 'Mùṣá takes 0.168 km2, x 12142-12992 y 5236-6342',
    f'{cut.area/1e6:.3f} km2, bbox {[round(v) for v in cut.bounds]}')
pl = {p['n']: p for p in F['places'] if p['d'] == 30}
out('C3', 'frame place Papa Ajao inside drawn Mùṣá',
    f'Papa Ajao {pl["Papa Ajao"]["at"]} in drawn d15: {o15.contains(Point(pl["Papa Ajao"]["at"]))}')
P = pq.read_table(OV + 'lagos_overture_place.parquet', columns=['geometry', 'names', 'basic_category', 'taxonomy']).to_pylist()
cutc, restc, rest_places = collections.Counter(), collections.Counter(), []
for r in P:
    g = shapely.from_wkb(r['geometry'])
    if not (3.30 < g.x < 3.37 and 6.50 < g.y < 6.565): continue
    x, y = G(g.y, g.x); p = Point(x, y)
    cat = r['basic_category'] or (r['taxonomy'] or {}).get('primary')
    nm = (r['names'] or {}).get('primary') or ''
    if rest.contains(p): restc[cat] += 1; rest_places.append((cat, nm, g.y, g.x, x, y))
    elif cut.contains(p): cutc[cat] += 1
out('C4', 'parts 42/3, automotive_service 34/14, auto_dealer 27/10 (cut/left)',
    ', '.join(f'{k} {cutc[k]}/{restc[k]}' for k in ('vehicle_parts_store', 'automotive_service', 'auto_dealer')))
osm = {}
for f in ('osm.json', 'osm2.json'):
    for e in json.load(open(os.path.join(OSM, f)))['elements']:
        n = e.get('tags', {}).get('name')
        if n and n not in osm:
            c = e.get('center') or e
            osm[n] = (c['lat'], c['lon'], e.get('tags', {}))
la, lo, _ = osm['Ladipo Market']
out('C5', 'OSM Ladipo Market (6.5442, 3.3418) in Mùṣá', f'({la:.4f}, {lo:.4f}) in drawn d15: {o15.contains(Point(G(la, lo)))}')
out('C6', 'what is left 1.124 km2 game, ~10.1 real', f'{rest.area/1e6:.3f} km2, real {rest.area*9/1e6:.2f}')
out('C7', 'frame Ladipo / Ilasamaja points 6.5439,3.3500 / 6.5503,3.3457',
    f'Ladipo {pl["Ladipo"]["at"]} vs {gm(6.5439, 3.35)}; Ilasamaja {pl["Ilasamaja"]["at"]} vs {gm(6.5503, 3.3457)}')
mw = [LineString(r['p']) for r in F['roads'] if r['n'] == 'Apapa-Oworonshoki Expressway' and r['k'] == 'motorway']
pieces = shapely.ops.split(rest, unary_union(mw + [LineString([(12260, 5220), (12263, 5000)])]))
lobe = [g for g in pieces.geoms if g.bounds[0] > 12250 and g.bounds[3] <= 5530]
out('C8', 'north-east lobe about 0.23 km2 game', f'pieces east of the expressway motorway line, north of y 5530: {sum(g.area for g in lobe)/1e6:.3f} km2')
la2, lo2, _ = osm['Ilasamaja']
out('C9', 'other sources put Ilasamaja 3.5 km south, by Cele',
    f'OSM Ilasamaja node ({la2:.4f}, {lo2:.4f}) {gm(la2, lo2)}: {math.dist(G(6.5503, 3.3457), G(la2, lo2))*3:.0f} m real from the frame point')
def inwhich(x, y): return [n for n in D if fpoly(n).contains(Point(x, y))]
b32 = fpoly(32).boundary
for cid, nm in (('C10a', 'Oshodi Transport Interchange - Terminal 1'), ('C10b', 'Oshodi Transport Interchange - Terminal 2'),
                ('C10c', 'Oshodi Transport Interchange - Terminal 3'), ('C10d', 'Oshodi')):
    la, lo, tg = osm[nm] if nm != 'Oshodi' else [(e['lat'], e['lon'], e['tags']) for e in json.load(open(os.path.join(OSM, 'osm2.json')))['elements'] if e.get('tags', {}).get('railway') == 'station' and e['tags'].get('name') == 'Oshodi'][0]
    x, y = G(la, lo)
    out(cid, {'C10a': 'T1 6.5549,3.3512 (12768,4922) in d30, 30 m from d32', 'C10b': 'T2 6.5558,3.3508 (12754,4889) in d30, 5 m from d32',
              'C10c': 'T3 in d29', 'C10d': 'Oshodi station 6.5573,3.3514 in d29'}[cid],
        f'({la:.4f}, {lo:.4f}) ({x:.0f}, {y:.0f}) in frame {inwhich(x, y)}, {b32.distance(Point(x, y)):.1f} m from d32 line')
names_md = open(f'{REPO}/docs/lagos-study/roads/NAMES.md').read()
out('C11', 'NAMES: Ìṣọ́lẹ̀ "keeping watch over the land"', [l for l in names_md.splitlines() if l.startswith('| 30 ')])

# ---------- section 2: neighbours ----------
print('== 2. neighbours')
p30 = set(pts30)
stated = {32: (27, 2465), 15: (21, 2272), 31: (16, 1257), 29: (15, 667), 14: (6, 563)}
for n, (sp, sl) in stated.items():
    nb = o15 if n == 15 else fpoly(n)
    sh = p30 & set(fpts(n))
    seam = rest.boundary.intersection(nb.buffer(0.5)).length
    out(f'N{n}', f'{sp} shared points, seam {sl} m', f'{len(sh)} shared points, seam (rest vs {"drawn d15" if n==15 else "frame"}) {seam:.0f} m')
for n in (32, 31, 29, 14):
    out(f'N{n}x', f'd{n} not drawn' if n != 14 else 'd14 drawn', f'map/d{n:02d}/ exists: {os.path.isdir(f"{REPO}/map/d{n:02d}")}')
o15pts = [tuple(q) for q in d15rec['outline'][0]]
sh15 = p30 & set(fpts(15))
out('N15a', 'drawn Mùṣá 79 points, keeps 13 shared exactly (15 within 2 m)',
    f'{len(o15pts)} points; exact {sum(q in o15pts for q in sh15)}; within 2 m {sum(min(math.dist(q, r) for r in o15pts) <= 2 for q in sh15)}; '
    f'next nearest {sorted(round(o15.boundary.distance(Point(q)),1) for q in sh15)[13:16]} m')
plan15 = {r['id']: r for r in json.load(open(f'{REPO}/map/d15/plan.json'))['records'] if r.get('type') == 'road'}
for rid in ('rd-qc8rcv8v', 'rd-cjk9hvop', 'rd-isodeck1', 'rd-qqm8wpxb'):
    r = plan15[rid]; c = r['centreline']
    out('N15b', {'rd-qc8rcv8v': 'from y 6279 north to y 5220, 25 m', 'rd-cjk9hvop': 'south to y 6370, 25 m',
                 'rd-isodeck1': 'starts 12215.2, 5786.3, 6.7 m up', 'rd-qqm8wpxb': 'east service road 7 m'}[rid],
        f'{rid} kind {r["kind"]} width {r["width"]} first {c[0]} last {c[-1]}')
seams = {n: rest.boundary.intersection(fpoly(n).buffer(0.5)) for n in (29, 31, 32)}
def near(n, name, kinds=None):
    return sum(LineString(r['p']).intersection(seams[n].buffer(25)).length for r in F['roads']
               if r['n'] == name and (kinds is None or r['k'] in kinds))
out('N32r', 'Airport Road 1,450 m near the d32 seam', f'{near(32, "International Airport Road"):.0f} m within 25 m')
out('N31r', 'Okota Road 949 m within 25 m of the d31 seam', f'{near(31, "Okota Road"):.0f} m (primary only {near(31, "Okota Road", ("primary",)):.0f})')
out('N29r', 'Agege Motor Road and SGR ~1,250 m each within 25 m of d29 seam',
    f'Agege {near(29, "Agege Motor Road"):.0f}, SGR {near(29, "Lagos–Ibadan SGR"):.0f}')
d14o = [tuple(q) for r in json.load(open(f'{REPO}/map/d14/district.json'))['records'][0]['outline'] for q in r]
out('N14', 'd14 drawn outline matches the 6 shared points', f'{sum(q in d14o for q in p30 & set(fpts(14)))} of {len(p30 & set(fpts(14)))}')
W = [Polygon(w[0]) if isinstance(w[0][0], list) else Polygon(w) for w in F['water']]
out('NW', 'no frame water touches the outline', f'{sum(w.buffer(0).intersects(frame30.buffer(1)) for w in W)} water polygons touch')
canals = [e for e in json.load(open(os.path.join(OSM, 'osm2.json')))['elements'] if e.get('tags', {}).get('waterway')]
out('NC', 'OSM: only Ajegunle Canal, in d13', [(e['tags'].get('name'), inwhich(*G(e['center']['lat'], e['center']['lon']))) for e in canals])
for n in ('Airport (MMIA) south', 'Ago Palace east'):
    out('N32p', f'frame puts "{n}" in d32', [p['d'] for p in F['places'] if p['n'] == n])
ec = open(f'{REPO}/docs/lagos-study/roads/EARTH-CHECK.md').read().splitlines()
out('NEC', 'EC row 30: Isolo canal south; expressway; airport south fence; row 7 canal is Okota/Isolo line',
    [l[:160] for l in ec if l.startswith('| 30 |') or l.startswith('| 7 |')])

# ---------- section 3: roads ----------
print('== 3. roads')
L = collections.Counter(); tot = 0
for r in F['roads']:
    ln = LineString(r['p']).intersection(rest).length
    if ln: L[(r['n'] or '-', r['k'])] += ln; tot += ln
out('R1', 'expressway 2578 primary + 2279 motorway + 134 bridge; Mushin Rd 1214; Agege 1168; unnamed motorway 854; Osolo 802; '
    'unnamed primary 533; SGR 499 + rail 158; Airport Rd 454 + 355; Okota 333; Egbe 125; Isolo Rd 81 + 67; 12.1 km',
    f'{ {f"{k[0]}/{k[1]}": round(v) for k, v in L.most_common()} } total {tot/1000:.2f} km')
S = pq.read_table(OV + 'lagos_overture_segment.parquet', columns=['names', 'subtype', 'class', 'road_surface', 'road_flags', 'width_rules', 'speed_limits', 'geometry', 'bbox']).to_pylist()
cls = collections.Counter(); widths = 0; resid = collections.Counter()
seg = collections.defaultdict(lambda: dict(L=0, cls=collections.Counter(), surf=collections.Counter(), lat=[9, 0], lon=[9, 0], speed=set(), bridge=0))
want = ['Mushin Road', 'Isolo Road', 'Osolo Way', 'Okota Road', 'Egbe Road', 'Cowbell Way', 'Abimbola Way', 'Chivita Avenue', 'Aswani Road',
        'Aswani Mechanic Village', 'Akinbaiye Street', 'Baale Shekoni Street', 'Baale Street', 'Kogberegbe', 'Okeho', 'Church Street',
        'Lateef Salami Street', 'Asa Afariogun Street', 'Ire-Akari Estate Road', 'Godwin Omonua Street', 'International Airport Road']
for r in S:
    b = r['bbox']
    if not (b['xmax'] > 3.29 and b['xmin'] < 3.38 and b['ymax'] > 6.49 and b['ymin'] < 6.57): continue
    g = shapely.from_wkb(r['geometry']); gg = geo_to_game(g)
    lr = gg.intersection(rest).length
    if r['subtype'] == 'road' and lr:
        cls[r['class']] += lr
        widths += bool(r['width_rules'])
        if r['class'] == 'residential': resid[(r['road_surface'] or [{}])[0].get('value')] += lr
    nm = (r['names'] or {}).get('primary') or ''
    for k in want:
        if nm.lower().startswith(k.lower()):
            a = seg[k]; a['L'] += gg.length * 3; a['cls'][r['class']] += 1
            a['surf'][(r['road_surface'] or [{}])[0].get('value')] += gg.length * 3
            if k == 'International Airport Road' and not lr: continue
            a['lat'] = [min(a['lat'][0], b['ymin']), max(a['lat'][1], b['ymax'])]; a['lon'] = [min(a['lon'][0], b['xmin']), max(a['lon'][1], b['xmax'])]
            if r['speed_limits']: a['speed'].add(r['speed_limits'][0]['max_speed']['value'])
            for fl in r['road_flags'] or []:
                if 'is_bridge' in fl['values']:
                    bt = fl['between'] or [0, 1]; a['bridge'] += substring(gg, bt[0], bt[1], normalized=True).length * 3
out('R2', 'Overture 23.7 km residential, 15.7 km service inside the line (game km)',
    f'residential {cls["residential"]/1000:.1f}, service {cls["service"]/1000:.1f} game km (x3 real); widths tagged on {widths} pieces inside')
out('R3', 'most residential pieces unpaved', {k: f'{v/sum(resid.values()):.0%}' for k, v in resid.items()})
for k in want:
    a = seg[k]
    out('R-' + k.split()[0][:6], k, f'{a["L"]:.0f} m real; class {dict(a["cls"])}; surface m {{{", ".join(f"{s}: {v:.0f}" for s, v in a["surf"].items())}}}; '
        f'lat {a["lat"][0]:.4f}-{a["lat"][1]:.4f}, lon {a["lon"][0]:.4f}-{a["lon"][1]:.4f}; maxspeed {a["speed"] or "-"}; bridge {a["bridge"]:.0f} m')
osmr = collections.Counter()
for e in json.load(open(os.path.join(OSM, 'osmroads.json')))['elements']:
    t = e.get('tags', {})
    if t.get('name') in ('Apapa-Oworonshoki Expressway', 'International Airport Road', 'Agege Motor Road', 'Okota Road', 'Egbe Road',
                         'Mushin Road', 'Isolo Road', 'Osolo Way', 'Cowbell Way'):
        osmr[(t['name'], t.get('highway'), t.get('ref'), t.get('lanes'), t.get('oneway'), t.get('width'), t.get('maxspeed'))] += 1
out('R4', 'OSM: expressway motorway F265 oneway + primary frontage; Airport Rd motorway F269 2 lanes; Agege trunk A5 2 lanes oneway; '
    'Okota primary 2 lanes oneway; Egbe primary oneway; Mushin Rd primary oneway + secondary; Isolo Rd primary; Osolo secondary; Cowbell tertiary 2 lanes two-way; no widths',
    '; '.join(f'{k}x{v}' for k, v in sorted(osmr.items(), key=str)))
I = pq.read_table(OV + 'lagos_overture_infrastructure.parquet', columns=['geometry', 'names', 'class']).to_pylist()
infra = {}
for r in I:
    n = (r['names'] or {}).get('primary') or ''
    if n in ('Airport Interchange', 'Isolo Ejigbo/Mushin Road'):
        c = shapely.from_wkb(r['geometry']).centroid; infra.setdefault(n, []).append((round(c.y, 4), round(c.x, 4), gm(c.y, c.x), r['class']))
out('R5', 'Airport Interchange (12190, 5135); junction signals 6.5291,3.3180 (11543, 5875)', infra)
st15 = open(f'{REPO}/map/d15/STREETS.md').read()
out('R6', 'Mùṣá: 41 m at 6.52569,3.33561; Agege 21.5 m at 6.53379,3.35349; Isolo Rd 16 m',
    [l[:120] for l in st15.splitlines() if l.startswith(('| rd-kxa8hz1b', '| rd-qc8rcv8v', '| rd-cb2h4xa5'))])

# ---------- section 4: landmarks ----------
print('== 4. landmarks (Overture pins in what is left)')
def find(pat):
    return [(c, n, round(la, 4), round(lo, 4), round(x), round(y)) for c, n, la, lo, x, y in rest_places if re.search(pat, n, re.I)]
for cid, st, pat in [
    ('L1', 'palace 6.5314,3.3233 (11739,5788)', r'Palace of Oba Osolo'),
    ('L2', 'Isolo Central Mosque 6.5300,3.3233 (11739,5840)', r'^Isolo Central Mosque'),
    ('L3', 'Ishagatedo Central Mosque 6.5268,3.3251 (11807,5958)', r'Ishagatedo'),
    ('L4', 'Ilasa Central Mosque 6.5194,3.3333 (12107,6231)', r'Ilasa Central'),
    ('L6', 'NNPC bus stop 6.5270,3.3201 (11621,5949)', r'^NNPC Bus'),
    ('L7', 'Oke-Afa Memorial Arcade 6.5299,3.3160 (11469,5844)', r'Oke-Afa Memorial'),
    ('L8', 'Ansar-Ud-Deen 6.5331,3.3242 (11773,5725); 6.5307,3.3257 (11826,5816)', r'Ansar'),
    ('L9', "St Mary's 6.5242,3.3222 (11698,6056)", r"St\. Mary"),
    ('L10', "St Paul's Anglican 6.5273,3.3256 (11826,5939)", r"^St\. Paul's Anglican Church$"),
    ('L11', 'St Peter Claver 6.5387,3.3246 (11788,5520)', r'Peter Claver'),
    ('L12', 'CCC Apata Ayeraye 6.5437,3.3337 (12122,5336)', r'Apata Ayeraye'),
    ('L14', 'Iyana-Isolo stop 6.5281,3.3359 (12203,5912)', r'^Iyana Isolo$'),
    ('L15', 'Promasidor 6.5265,3.3325 (12079,5968)', r'Promasidor'),
    ('L16', 'Aswani place pin 6.5459,3.3328 (12090,5253); LCDA pin shares it', r'Aswani|ISOLO LCDA'),
    ('L18', 'Ibis 6.5509,3.3302 (11975,5067); D\'Palms 6.5427,3.3273 (11870,5381)', r"ibis Lagos Airport|D'Palms"),
    ('L19', 'FIIRO 6.5468,3.3510 (12760,5222)', r'Industrial Research'),
    ('L20', 'DBI pin, NIMET, Federal Ministry of Housing', r'Digital Bridge|NIMET|Ministry of Housing')]:
    out(cid, st, find(pat))
LU = pq.read_table(OV + 'lagos_overture_land_use.parquet', columns=['names', 'subtype', 'class', 'geometry']).to_pylist()
lu_by = collections.defaultdict(list)
for r in LU:
    gg = geo_to_game(shapely.from_wkb(r['geometry'])).buffer(0)
    if not gg.intersects(frame30): continue
    lu_by[(r['subtype'], r['class'])].append(gg)
    n = (r['names'] or {}).get('primary') or ''
    if re.search(r'Resettlement|Digital Bridge|Polytechnic|Isolo General|Aswani', n):
        c = shapely.from_wkb(r['geometry']).centroid
        out('LU', n, f'{r["class"]} centroid ({c.y:.4f}, {c.x:.4f}) {gm(c.y, c.x)}, {gg.area*9/1e4:.1f} ha real in all, {gg.intersection(rest).area*9/1e4:.1f} ha inside the line')
out('L5', 'Isolo General Hospital (OSM) 6.5272,3.3193 (11590,5944)', f'OSM {osm["Isolo General Hospital"][:2]} {gm(*osm["Isolo General Hospital"][:2])}')
for n in ('Federal Neuro Psychatric Hospital Oshodi', 'Federal Medical Centre', 'Ajao Estate main entrance', 'Junction bus stop'):
    out('L-osm', n, f'{osm[n][:2]} {gm(*osm[n][:2])} in frame {inwhich(*G(*osm[n][:2]))}')
mos = [e for e in json.load(open(os.path.join(OSM, 'osm2.json')))['elements'] if e.get('tags', {}).get('religion') == 'muslim']
out('L2b', 'OSM unnamed mosque 6.5329,3.3251 (11805,5735)', [(round(e['center']['lat'], 4), round(e['center']['lon'], 4), gm(e['center']['lat'], e['center']['lon'])) for e in mos if not e['tags'].get('name')])
d = lambda a, b: math.dist(a, b)
out('L-dist', 'mosque ~50 game m S of palace; junction ~85 game m from hospital (11590,5944)',
    f'{d((11739, 5788), G(6.5300, 3.3233)):.0f} m; {d(G(6.5291, 3.3180), G(6.5272, 3.3193)):.0f} m')
for lab, (la, lo) in (('note pos', (6.5299, 3.3160)), ('Overture pin', (6.5296, 3.3157))):
    x, y = G(la, lo)
    out('L7b', 'Oke-Afa 14 game m from d32 line, 19 from d31', f'{lab}: d32 {fpoly(32).boundary.distance(Point(x, y)):.0f} m, d31 {fpoly(31).boundary.distance(Point(x, y)):.0f} m')
hot = [(n, y) for c, n, la, lo, x, y in rest_places if c in ('hotel', 'lodging')]
out('L18b', '48 hotel/lodging pins, 27 north of y 5300', f'{len(hot)}, {sum(y < 5300 for n, y in hot)} north; the palace pin is filed as "hotel": {any("Palace of Oba" in n for n, y in hot)}')
out('L21', '3 mosques to 68 churches', f'{restc["muslim_place_of_worship"]} : {restc["christian_place_of_worship"]}')

# ---------- section 5 ----------
print('== 5. what it is like')
pc = {r['name']: r for r in csv.DictReader(open(f'{REPO}/docs/lagos-study/roads/places.csv'))}
for n in ('Isolo', 'Cele', 'Isolo north-east', 'Ajao Estate', 'Ladipo', 'Ilasamaja'):
    r = pc[n]
    out('F-' + n[:6], 'see note §5', f'{r["fabric"]}, {r["bldg_per_km2"]}/km2, median {r["median_foot_m2"]} m2, big {r["big_share"]}, h {r["height_m"]}, grid {r["grid"]}')
for k in (('residential', 'residential'), ('developed', 'industrial')):
    u = unary_union(lu_by[k])
    out('LU%', f'{k[1]} 52% / 21% of the outline', f'{100*u.intersection(rest).area/rest.area:.1f}% of what is left ({100*u.intersection(frame30).area/frame30.area:.1f}% of the frame)')
out('LUx', 'stray "Pacific Islands Heritage Marine National Monument" polygon', [k for k in lu_by if k[0] == 'protected'])
out('T', 'logistics/storage 37, fashion 63', f'{restc["b2b_transportation_and_storage_service"]}, {restc["fashion_and_apparel_store"]}')
study = open(f'{REPO}/docs/lagos-study/STUDY.md').read()
out('ST', 'Okota / Ago Palace / Isolo south grid 0.82', [l for l in study.splitlines() if 'Isolo south' in l][:1])
liv = open(f'{REPO}/docs/lagos-study/LIVING.md').read().splitlines()
out('LIV', '11.6 km2, 40k/km2, class C, shift 7 and 19 [K], mosques under-counted',
    [l for l in liv if l.startswith('| 30 |')] + [l[:110] for l in liv if l.startswith('#### 30.') or 'shift change at 7' in l or 'badly under-counts mosques' in l])
lga = open(f'{REPO}/docs/lagos-lgas-research.md').read().splitlines()
heads = [(i + 1, l) for i, l in enumerate(lga) if l.startswith('## ')]
out('LGA', 'Oshodi-Isolo brief lines 1161-1290; Mushin brief lines 885-1002',
    [(i, l[:30]) for i, l in heads if 'Oshodi-Isolo' in l or 'Mushin' in l or i in (1022, 1291)])
blob = '\n'.join(lga[1160:1290])
for k in ('older industrial zones quieter at night', 'Isolo LCDA from 1 September 2022', 'not desilted for about five years',
          'Idris Balogun Street was submerged on 10 July 2012', '10-lane', 'Mosafejo', 'It is now overgrown', 'the Oba and his palace',
          'raise their houses above ground', 'Ilasamaja:** low-lying'):
    out('LGAq', k, k in blob)
