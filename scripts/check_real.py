"""How close the map is to the real places it is the child of (owner, 21 Oct 2026: "nobody checks how close it is to the real place").
For every area of a district built from real places (docs/hand/ibudo/twins/<area>.json):
  R1 buildings     the map's buildings in the area against the real footprints (count and built-up area)
  R2 streets       street, lane and main length against the real ones
  R3 twin streets  every street the twin record holds is still on the map
  R6 twins back  every street, lane and main inside the area has a twin record (a hand-added one too: twin it or it fails)
  R4 places        every kind of place the real area has (churches, schools, banks...) is on the map there
  R5 livable       each thing the twin photos show (okada, keke, danfo, kiosks, stalls, betting, POS, loading, fuel...) is on the map
                   within 100 m of where it was photographed (DECISIONS: a livable world before the story)
  N1 real names    no real Lagos street or place name anywhere on the map (Gidi's names are its own)
Prints a PASS/FAIL line per check per area, exits 1 if any fails. Usage: python3 scripts/check_real.py hub
"""
import csv
import glob
import json
import os
import re
import sys

from shapely.geometry import LineString, Point, Polygon
from shapely.strtree import STRtree

D = sys.argv[1] if len(sys.argv) > 1 else 'hub'
BAND = {'buildings': (0.80, 1.10), 'built_m2': (0.70, 1.10), 'street_m': (0.85, 1.15)}   # what the building lines and the clean-up may take
NEAR = 100.0
PICS = os.path.expanduser('~/Real-world/research/google/ibudo/twins')
M_LAT, M_LON = 110600.0, 109900.0
# what a photo note names -> what stands for it on the map: (pois types, things, building kinds, furniture kinds)
LIVABLE = {
    'okada':    (r'\bokadas?\b', ((), ('okada',), (), ())),
    'keke':     (r'\bkekes?\b', ((), ('keke',), (), ())),
    'danfo':    (r'\bdanfos?\b|\bbus (stop|park)\b', (('transit',), ('danfo', 'molue'), (), ('bus stop',))),
    'kiosk':    (r'\bkiosks?\b', ((), (), ('kiosk',), ())),
    'stalls':   (r'\b(market|umbrella|table) stalls?\b|\bstalls\b', (('market',), (), ('stalls', 'canopy'), ())),
    'betting':  (r'\bbet(ting|9ja|king|naija)?\b', (('betting',), (), (), ())),
    'POS':      (r'\bPOS\b', (('pos',), (), (), ())),
    'loading':  (r'\bloading\b|\bhead.?load', (('loading',), (), (), ())),
    'fuel':     (r'\bfuel|filling station|petrol', (('fuel',), (), (), ())),
    'bank':     (r'\bbank\b|\bATM\b', (('bank',), (), (), ())),
    'chemist':  (r'\bpharmac|\bchemist', (('chemist',), (), (), ())),
    'school':   (r'\bschool', (('school',), (), (), ())),
    'church':   (r'\bchurch', (('church',), (), (), ())),
    'mosque':   (r'\bmosque', (('mosque',), (), (), ())),
    'vulcaniser': (r'\bvulcani[sz]', (('vulcaniser',), (), (), ())),
}


def load_map():
    s = open('web/gidi-data.js').read()
    return json.loads(s[len('window.GIDI='):-1])


def ratio_line(name, have, real, band):
    if not real:
        return (name, None, 'no real figure')
    r = have / real
    return (name, band[0] <= r <= band[1], '%.0f%% of the real (%s of %s)' % (100 * r, round(have), round(real)))


def run(G):
    res = []
    B = [(b[0], Polygon(b[1:])) for b in G['buildings'].get(D, []) if len(b) > 3]
    bt = STRtree([p for _, p in B])
    WAYS = {'street': [LineString(p) for p in G['streets'].get(D, []) if len(p) > 1], 'lane': [LineString(p) for p in G['lanes'].get(D, []) if len(p) > 1],
            'main': [LineString(m['pts']) for m in G['mains'] if m.get('d') == D and len(m['pts']) > 1]
                    + [LineString(x['pts']) for x in G['arterials'] if len(x['pts']) > 1],   # a real main road can be Gidi's own arterial, by design
            'path': [LineString(p) for p in (G.get('paths') or {}).get(D, []) if len(p) > 1]}
    allways = [g for v in WAYS.values() for g in v]
    wt = STRtree(allways)
    # what stands for each livable thing, by kind
    PTS = {}
    for p in G['pois']:
        PTS.setdefault(('poi', p['type']), []).append(Point(p['x'], p['y']))
    for t in G.get('things', []):
        if t.get('d') == D:
            PTS.setdefault(('thing', t['k']), []).append(Point(t['x'], t['y']))
    for k, p in B:
        PTS.setdefault(('bld', k), []).append(p.representative_point())
    for f in G.get('furniture', []):
        PTS.setdefault(('furn', f['kind']), []).append(Point(f['x'], f['y']))
    for tf in sorted(glob.glob('docs/hand/ibudo/twins/*.json')):
        T = json.load(open(tf)); a = T['area']
        if 'area_pts' not in T or 'real_counts' not in T:
            res.append((a, 'R0 real figures', False, 'the twin record has no real figures: build the area again (scripts/rebuild_areas.py)'))
            continue
        AREA = Polygon(T['area_pts']); RC = T['real_counts']
        inb = [B[int(i)] for i in bt.query(AREA, predicate='intersects') if AREA.contains(B[int(i)][1].representative_point())]
        res.append((a,) + ratio_line('R1 buildings (count)', len(inb), RC['buildings'], BAND['buildings']))
        res.append((a,) + ratio_line('R1 buildings (built-up m2)', sum(p.area for _, p in inb), RC['built_m2'], BAND['built_m2']))
        for k in ('main', 'street', 'lane'):
            have = sum(g.intersection(AREA).length for g in WAYS[k] if g.intersects(AREA))
            if RC['street_m'].get(k):
                res.append((a,) + ratio_line('R2 %s length' % k, have, RC['street_m'][k], BAND['street_m']))
        miss = []
        for s in T['streets']:
            g = LineString(s['gidi'])
            m = g.interpolate(0.5, normalized=True)
            near = [allways[int(i)] for i in wt.query(m.buffer(3))]
            if not any(w.distance(m) < 3 for w in near):
                miss.append('%s (%s) at (%.0f,%.0f)' % (s.get('real_name') or s['kind'], s['kind'], m.x, m.y))
        res.append((a, 'R3 twin streets on the map', not miss, '%d of %d gone. %s' % (len(miss), len(T['streets']), '; '.join(miss[:3]))))
        tw = [LineString(x['gidi']) for x in T['streets'] if len(x['gidi']) > 1]
        twt = STRtree(tw) if tw else None
        orphan = []
        for k in ('main', 'street', 'lane'):
            for g in WAYS[k]:
                if g.length < 10 or g.intersection(AREA).length < 0.7 * g.length:
                    continue
                m = g.interpolate(0.5, normalized=True)
                if twt is None or not any(tw[int(i)].distance(m) < 3 for i in twt.query(m.buffer(3))):
                    orphan.append('%s at (%.0f,%.0f)' % (k, m.x, m.y))
        res.append((a, 'R6 every street has its twin', not orphan, '%d without. %s' % (len(orphan), '; '.join(orphan[:3]))))
        gone = []
        for t, n in sorted(RC.get('places', {}).items()):
            have = sum(1 for q in PTS.get(('poi', t), []) if AREA.contains(q))
            if have == 0:
                gone.append('%s (real %d)' % (t, n))
        res.append((a, 'R4 kinds of place', not gone, 'missing: ' + ', '.join(gone) if gone else 'every kind the real area has'))
        idx = os.path.join(PICS, a, 'INDEX.tsv')
        if not os.path.exists(idx):
            res.append((a, 'R5 livable', None, 'no twin photos yet'))
            continue
        (LA0, LO0), (GX0, GY0) = T['anchor_real'], T['anchor_gidi']
        seen, short = {}, {}
        for r in csv.DictReader(open(idx), delimiter='\t'):
            note = r.get('note') or ''
            if 'Livable:' not in note:
                continue
            liv = note.split('Livable:', 1)[1]
            q = Point(GX0 + (float(r['lon']) - LO0) * M_LON, GY0 - (float(r['lat']) - LA0) * M_LAT)
            for name, (rx, (pt, th, bk, fu)) in LIVABLE.items():
                if not re.search(rx, liv, re.I):
                    continue
                seen[name] = seen.get(name, 0) + 1
                keys = [('poi', x) for x in pt] + [('thing', x) for x in th] + [('bld', x) for x in bk] + [('furn', x) for x in fu]
                if not any(p.distance(q) < NEAR for k in keys for p in PTS.get(k, [])):
                    short[name] = short.get(name, 0) + 1
        bad = {k: v for k, v in short.items() if v > 0.2 * seen[k]}   # four photos in five must find theirs on the map
        res.append((a, 'R5 livable (photo spots with it on the map)', not bad,
                    ', '.join('%s %d/%d' % (k, seen[k] - short.get(k, 0), seen[k]) for k in sorted(seen, key=lambda k: -seen[k]))))
    # N1: real names
    real = set()
    for tf in glob.glob('docs/hand/ibudo/twins/*.json'):
        for s in json.load(open(tf))['streets']:
            if s.get('real_name'):
                real.add(s['real_name'])
    for idx in glob.glob(os.path.join(PICS, '*', 'INDEX.tsv')):
        for r in csv.DictReader(open(idx), delimiter='\t'):
            for k in ('real_name', 'panel_street'):
                v = re.sub(r'^[\d\-/ ]+', '', r.get(k) or '').strip()
                if v:
                    real.add(v)
    BOX = []   # the real places Gidi is a child of: every named road and place around them (Overture Maps, from OpenStreetMap)
    for tf in glob.glob('docs/hand/ibudo/twins/*.json'):
        la = [s['photo_at'][0] for s in json.load(open(tf))['streets']]; lo = [s['photo_at'][1] for s in json.load(open(tf))['streets']]
        if la:
            BOX.append((min(la) - 0.01, max(la) + 0.01, min(lo) - 0.01, max(lo) + 0.01))
    try:
        import pyarrow.parquet as pq
        for f in ('lagos_overture_segment.parquet', 'lagos_overture_place.parquet'):
            t = pq.read_table(os.path.expanduser('~/Real-world/research/data/overture-lagos/' + f), columns=['names', 'bbox'])
            for n, b in zip(t.column('names').to_pylist(), t.column('bbox').to_pylist()):
                if n and n.get('primary') and any(a0 <= b['ymin'] <= a1 and o0 <= b['xmin'] <= o1 for a0, a1, o0, o1 in BOX):
                    real.add(n['primary'])
    except OSError:
        pass
    GENERIC = {'road', 'street', 'close', 'avenue', 'crescent', 'way', 'lane', 'drive', 'st', 'rd', 'ave', 'the', 'old', 'new', 'market', 'church',
               'mosque', 'school', 'link', 'bridge', 'expressway', 'service', 'estate', 'park', 'garage', 'motor', 'bus', 'stop', 'junction', 'oshodi',
               'surulere', 'lagos', 'unnamed', 'none'}
    core = lambda n: ' '.join(w for w in re.findall(r"[a-zà-ÿ']+", n.lower()) if w not in GENERIC and len(w) > 1)
    cores = {core(n) for n in real} - {''}
    cores = {c for c in cores if len(c) >= 5}
    names = [m.get('name', '') for m in G['mains']] + [p.get('name', '') for p in G['pois'] if p.get('d') == D]
    names += [l.get('text', l.get('name', '')) if isinstance(l, dict) else '' for l in (G.get('labels') or [])]
    hit = sorted({n for n in names if n and core(n) in cores})
    res.append(('all', 'N1 no real names on the map', not hit, '%d found. %s' % (len(hit), '; '.join(sorted({re.sub(r' \d+$', '', h) for h in hit})))))
    return res


if __name__ == '__main__':
    res = run(load_map())
    for a, name, ok, detail in res:
        print('%-5s %-12s %-44s %s' % ('SKIP' if ok is None else ('PASS' if ok else 'FAIL'), a, name, detail[:260]))
    sys.exit(1 if any(ok is False for _, _, ok, _ in res) else 0)
