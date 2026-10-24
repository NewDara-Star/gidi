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

from shapely import wkt
from shapely.geometry import LineString, Point, Polygon
from shapely.strtree import STRtree

D = sys.argv[1] if len(sys.argv) > 1 else 'hub'
BAND = {'buildings': (0.80, 1.10), 'built_m2': (0.70, 1.10), 'street_m': (0.85, 1.15)}   # what the building lines and the clean-up may take
NEAR = 100.0
PICS = os.path.expanduser('~/gidi-data/research/google/ibudo/twins')
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
            'main': [LineString(m['pts']) for m in G['mains'] if m.get('d') == D and len(m['pts']) > 1],
            'path': [LineString(p) for p in (G.get('paths') or {}).get(D, []) if len(p) > 1]}
    # Gidi's arterials and expressways are the layout's lines: the real trunk roads and expressways are left out of the real figures, so they
    # do not count in R2's main length; but a real main road can be Gidi's own arterial by design, so they do count as its twin (R3)
    allways = [g for v in WAYS.values() for g in v] + [LineString(x['pts']) for x in G['arterials'] if len(x['pts']) > 1]
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
        if 'area_wkt' not in T or 'real_counts' not in T:
            res.append((a, 'R0 real figures', False, 'the twin record has no real figures: build the area again (scripts/rebuild_areas.py)'))
            continue
        AREA = wkt.loads(T['area_wkt']); RC = T['real_counts']   # the area's own part: what no later area builds again
        inb = [B[int(i)] for i in bt.query(AREA, predicate='intersects') if AREA.contains(B[int(i)][1].representative_point())]
        res.append((a,) + ratio_line('R1 buildings (count)', len(inb), RC['buildings'], BAND['buildings']))
        res.append((a,) + ratio_line('R1 buildings (built-up m2)', sum(p.area for _, p in inb), RC['built_m2'], BAND['built_m2']))
        for k in ('main', 'street', 'lane'):
            have = sum(g.intersection(AREA).length for g in WAYS[k] if g.intersects(AREA))
            if RC['street_m'].get(k):
                res.append((a,) + ratio_line('R2 %s length' % k, have, RC['street_m'][k], BAND['street_m']))
        miss = []
        for s in T['streets']:
            if s.get('replaced'):
                continue
            g = LineString(s['gidi'])
            m = g.interpolate(0.5, normalized=True)
            tol = 10 if s['kind'] == 'main' else 3   # a real dual carriageway (one line each way, ~8 m apart) is one Gidi main on its middle
            near = [allways[int(i)] for i in wt.query(m.buffer(tol))]
            if not any(w.distance(m) < tol for w in near):
                miss.append('%s (%s) at (%.0f,%.0f)' % (s.get('real_name') or s['kind'], s['kind'], m.x, m.y))
        res.append((a, 'R3 twin streets on the map', not miss, '%d of %d gone. %s' % (len(miss), len(T['streets']), '; '.join(miss[:3]))))
        tw = [LineString(x['gidi']) for x in T['streets'] if len(x['gidi']) > 1 and not x.get('replaced')]
        twt = STRtree(tw) if tw else None
        orphan = []
        for k in ('main', 'street', 'lane'):
            for g in WAYS[k]:
                if g.length < 10 or g.intersection(AREA).length < 0.7 * g.length:
                    continue
                m = g.interpolate(0.5, normalized=True)
                tol = 10 if k == 'main' else 3
                if twt is None or not any(tw[int(i)].distance(m) < tol for i in twt.query(m.buffer(tol))):
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
    # N1: real names (the list is docs/hand/realnames.txt, made by scripts/realnames.py)
    import realnames
    core, cores = realnames.core, realnames.cores()
    names = [m.get('name', '') for m in G['mains']] + [p.get('name', '') for p in G['pois'] if p.get('d') == D]
    names += [l.get('t', '') if isinstance(l, dict) else '' for l in (G.get('labels') or [])]
    hit = sorted({n for n in names if n and core(n) in cores})
    res.append(('all', 'N1 no real names on the map', not hit, '%d found. %s' % (len(hit), '; '.join(sorted({re.sub(r' \d+$', '', h) for h in hit})))))
    return res


if __name__ == '__main__':
    res = run(load_map())
    for a, name, ok, detail in res:
        print('%-5s %-12s %-44s %s' % ('SKIP' if ok is None else ('PASS' if ok else 'FAIL'), a, name, detail[:260]))
    sys.exit(1 if any(ok is False for _, _, ok, _ in res) else 0)
