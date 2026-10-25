"""A district's first draft of each road's surface, width, kerbs, drains and verges, from Street View readings by hand.

  ~/.venvs/gidi/bin/python scripts/draft_roads.py map/d15 [--dry]

The readings are <district>/road_reads.tsv: one row per point along a road (one point per 100 m of centreline, at the
middle of each 100 m), each read by eye from the Street View pano nearest that point, looking along the road from its
first point to its last (so left and right are the record's). Columns: i, id, sv (the pano's address and capture date,
or "none"), width (m, kerb to kerb, by eye against parked cars), surface, sand (sand_cover), kerbL, kerbR, gutL, gutR
(a gutters kind or -), vergeL, vergeR (surface:width or -), edge (what lines the road, in words, for the frontage pass;
a median seen is written in it as MEDIAN=low_concrete or MEDIAN=jersey).

Industry: road surface type is surveyed from street-level images matched to the nearest road segment, the readings of a
segment's images put together for the segment, and human reading is the reference the classifiers are checked against
(StreetSurfaceVis, Kapp et al. 2024, arXiv 2407.21454; SurfaceAI, arXiv 2409.18922: per-image readings aggregated to
the OSM segment). Here every image is read by hand and the readings of one road put together:
- width: the median of its readings; surface, sand_cover, kerbs, median: the most common reading (ties to the first; a
  reading with no MEDIAN= in its edge counts as none);
- gutters and verges: each reading holds for its own 100 m stretch (s0 to s1 along the centreline), offset from the
  centreline by half the width plus half the gutter; gutters 0.5 m wide, 0.45 deep, half blocked (the state seen most);
- gutters and verges none seen: an empty list (drawn, none there);
- crown: half the width times the normal cross slope, 2% for a sealed surface (tar, concrete, interlock: AASHTO's 1.5-2%
  for high-type pavements) and 4% for a loose one (sand, earth, laterite: FHWA's Gravel Roads guide), 0 for plank;
- a road with no reading of its own (no Street View) takes the fields of the nearest road of the same kind that has
  one, whole length; it is listed for the hand pass.

Written only where a field is missing ("Rules draft, records rule"): a field already set by hand is never changed.
"""
import csv
import json
import re
import statistics
import sys
from collections import Counter

from shapely.geometry import LineString

GUT_W, GUT_D = 0.5, 0.45
SLOPE = {'tar_new': 0.02, 'tar_worn': 0.02, 'concrete': 0.02, 'interlock': 0.02, 'sand': 0.04, 'earth': 0.04,
         'laterite': 0.04, 'plank': 0.0}


def common(vals):
    vals = [v for v in vals if v not in ('-', '')]
    return Counter(vals).most_common(1)[0][0] if vals else None


def fields(road, rows, L):
    n = len(rows)
    widths = [float(r['width']) for r in rows if r['width'] not in ('-', '')]
    f = {}
    if widths:
        f['width'] = round(statistics.median(widths), 1)
    for k, col in (('surface', 'surface'), ('sand_cover', 'sand'), ('kerb_left', 'kerbL'), ('kerb_right', 'kerbR')):
        v = common(r[col] for r in rows)
        if v:
            f[k] = v
    f['median'] = common((re.search(r'MEDIAN=(\w+)', r['edge']) or [None, 'none'])[1] for r in rows)
    w = f.get('width') or road.get('width') or 6.0
    gut, ver = [], []
    for j, r in enumerate(rows):
        s0, s1 = round(L * j / n, 1), round(L * (j + 1) / n, 1)
        for side, gc, vc in (('left', 'gutL', 'vergeL'), ('right', 'gutR', 'vergeR')):
            if r[gc] not in ('-', ''):
                gut.append({'side': side, 's0': s0, 's1': s1, 'kind': r[gc], 'width': GUT_W, 'depth': GUT_D,
                            'offset': round(w / 2 + GUT_W / 2, 2), 'state': 'half_blocked'})
            if r[vc] not in ('-', ''):
                sf, vw = r[vc].split(':')
                ver.append({'side': side, 's0': s0, 's1': s1, 'surface': sf, 'width': float(vw)})
    f['gutters'], f['verges'] = gut, ver
    return f


def crown(road):
    slope = SLOPE.get(road.get('surface'))
    return round(slope * road['width'] / 2, 2) if slope is not None and road.get('width') else None


def main():
    d = sys.argv[1].rstrip('/')
    pf = f'{d}/plan.json'
    plan = json.load(open(pf))
    reads = {}
    for r in csv.DictReader((l for l in open(f'{d}/road_reads.tsv') if not l.startswith('#!')), delimiter='\t'):
        reads.setdefault(r['id'], []).append(r)
    roads = [r for r in plan['records'] if r['type'] == 'road']
    lines = {r['id']: LineString([p[:2] for p in r['centreline']]) for r in roads}
    seen = {i: [r for r in rows if r['sv'] != 'none'] for i, rows in reads.items()}
    own, borrowed, written = 0, [], Counter()
    for road in roads:
        L = lines[road['id']].length
        rows = seen.get(road['id'])
        if rows:
            # a reading missing at some points still covers the road: its rows stand for their stretches only
            all_rows = reads[road['id']]
            f = fields(road, rows, L)
            f.pop('gutters', None), f.pop('verges', None)
            g = fields(road, [r if r['sv'] != 'none' else dict(r, gutL='-', gutR='-', vergeL='-', vergeR='-')
                              for r in all_rows], L)
            for k in ('gutters', 'verges'):
                if k in g:
                    f[k] = g[k]
            own += 1
        else:
            same = [r for r in roads if r['kind'] == road['kind'] and seen.get(r['id'])]
            if not same:
                continue
            near = min(same, key=lambda r: lines[r['id']].distance(lines[road['id']]))
            nrows = seen[near['id']]
            f = fields(road, [dict(nrows[0], **{k: common(r[k] for r in nrows) or '-' for k in
                                                ('gutL', 'gutR', 'vergeL', 'vergeR')})], L)
            borrowed.append((road['id'], near['id']))
        for k, v in f.items():
            if k not in road:
                road[k] = v
                written[k] += 1
        if 'crown' not in road and crown(road) is not None:
            road['crown'] = crown(road)
            written['crown'] += 1
    print(f'{own} roads from their own readings; {len(borrowed)} from the nearest read road of their kind')
    print('fields written:', dict(written))
    for a, b in borrowed:
        print('  borrowed', a, 'from', b)
    if '--dry' not in sys.argv:
        json.dump(plan, open(pf, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
