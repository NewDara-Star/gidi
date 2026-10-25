"""A district's first draft of what stands along each road: poles and their wires, parked vehicles, stalls, trees,
drums, tyre stacks, heaps and masts, from the Street View reading's edge notes.

  ~/.venvs/gidi/bin/python scripts/draft_edge.py map/d15 [--dry]

Each row of <district>/road_reads.tsv covers its own 100 m of road (draft_roads.py); its `edge` column says in words what
lines the road there, a clause starting "L " or "R " for one side ("sides unsure" or no letter: either side). This
places what the words name, on that stretch and side, in the numbers below (a plural word gives the plural count):
- poles: one every POLE_SPAN m along the stretch, on the named side (or the side with more houses), concrete (JICA:
  Nigeria's medium- and low-voltage poles are "basically concrete"), joined by a 4-wire line (415/240 V, three phase
  four wire); a lamp on each where streetlights are named (`solar` where solar ones are); one with a transformer where
  a transformer is named;
- parked vehicles at the kerb, nose along the traffic (Nigeria drives on the right), clear of the crossings;
- stalls, kiosks and umbrellas, trees and palms, drums, tyre stacks, water tanks and heaps beside the road, outside its
  carriageway and gutter when there is room before the houses, else on the road's edge (stalls only: "umbrella market
  stalls on the carriageway edge"); a mast behind the frontage.
A stretch with no pano takes the nearest seen stretch of the same road, and a road with none the reading draft_roads.py
borrowed for it (the nearest seen road of its kind). Nothing is placed on a house, a carriageway (but parked vehicles and
edge stalls), a crossing or another placed thing. Walls and gates wait for plots (MAP-FORMAT: a frontage belongs to one).

Industry: game cities dress their streets by rule where a prop follows the street and comes in numbers, and by hand
where it does not (Astragon, "Brighton Was Not Built in a Day": Houdini places such props as instancing points; Unreal
PCG road tools hang streetlights and props off splines along each road edge at set spacings). Here the rule's numbers
come from each 100 m's own Street View note; the hand pass follows street by street.

Seeded by road id, so a re-run gives the same draft. Run once: a road that already has edge records (a note
"edge rd-...") is left as it is ("Rules draft, records rule").
"""
import csv
import json
import math
import random
import re
import string
import sys

from shapely.geometry import LineString, Point, Polygon, box
from shapely.affinity import rotate, translate
from shapely.ops import unary_union
from shapely.strtree import STRtree

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from draft_roads import common  # noqa: E402

POLE_SPAN, POLE_H = 40.0, 9.0
# what a word names: (record type, kind, count when singular, count when plural)
WORDS = [
    (r'\bcars?\b|\bsaloons?\b|\bjeeps?\b|\bvans?\b', 'vehicle', 'saloon', 1, 3),
    (r'\bsuvs?\b', 'vehicle', 'suv', 1, 2),
    (r'\bkekes?\b', 'vehicle', 'keke', 1, 2),
    (r'\bdanfos?\b', 'vehicle', 'danfo', 1, 2),
    (r'\bokadas?\b', 'vehicle', 'okada', 1, 3),
    (r'\bbus(es)?\b', 'vehicle', 'bus', 1, 1),
    (r'\blorr(y|ies)\b|\btrucks?\b', 'vehicle', 'lorry', 1, 1),
    (r'\bpickups?\b', 'vehicle', 'pickup', 1, 2),
    (r'\bkiosks?\b', 'stall', 'kiosk', 1, 2),
    (r'\bu(m|r)brellas?\b|\burellas?\b', 'stall', 'umbrella', 1, 2),
    (r'\bstalls?\b|\btraders\b|\btables?\b', 'stall', 'plank_stall', 1, 3),
    (r'\bcontainer shops?\b', 'stall', 'container_shop', 1, 1),
    (r'\bpalms?\b', 'tree', 'palm', 1, 2),
    (r'\btrees?\b', 'tree', 'shade', 1, 2),
    (r'\bdrums?\b', 'furniture', 'drum', 1, 2),
    (r'\btyres?\b|\btires?\b', 'furniture', 'tyre_stack', 1, 1),
    (r'\bwater tanks?\b|\bwater tower\b', 'furniture', 'water_tank', 1, 1),
    (r'\bgenerators?\b', 'furniture', 'generator', 1, 1),
    (r'\bbenche?s?\b|\bchairs\b', 'furniture', 'bench', 1, 1),
    (r'\brubbish\b|\brubble\b|\bwaste\b|\bdump\b', 'heap', 'rubbish', 1, 1),
    (r'\bsand heaps?\b|\bsand piles?\b', 'heap', 'sand', 1, 1),
    (r'\bmasts?\b', 'mast', 'lattice', 1, 1),
]
# half widths and half lengths of what stands (m)
SIZE = {'saloon': (0.9, 2.3), 'suv': (1.0, 2.4), 'keke': (0.7, 1.4), 'danfo': (1.0, 2.6), 'okada': (0.4, 1.0),
        'bus': (1.25, 5.0), 'lorry': (1.25, 5.5), 'pickup': (0.95, 2.6), 'kiosk': (0.9, 0.9), 'umbrella': (1.1, 1.1),
        'plank_stall': (0.5, 1.0), 'container_shop': (1.2, 3.0), 'palm': (0.6, 0.6), 'shade': (1.5, 1.5),
        'drum': (0.35, 0.35), 'tyre_stack': (0.45, 0.45), 'water_tank': (0.8, 0.8), 'generator': (0.5, 0.8),
        'bench': (0.3, 1.0), 'rubbish': (1.2, 1.2), 'sand': (1.4, 1.4), 'pole': (0.2, 0.2), 'lattice': (2.0, 2.0)}
CAR = ['#c0c0c0', '#1b1b1b', '#f2f2f2', '#2b3a55', '#7a1f1f', '#5b5b5b', '#8a8f93', '#3c4a3a']
UMBRELLA = [['#f6c800', '#1f5fbf'], ['#d62828', '#f2f2f2'], ['#2e8b3a', '#f2f2f2'], ['#f6c800', '#1b1b1b'],
            ['#1f5fbf', '#f2f2f2']]


def new_id(prefix, rng, taken):
    while True:
        i = prefix + '-' + ''.join(rng.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        if i not in taken:
            taken.add(i)
            return i


def clauses(note):
    """(side, text) pieces of an edge note: side 'left', 'right' or None (either)."""
    out = []
    for cl in note.split(';'):
        side = None
        for part in re.split(r',\s*', cl.strip()):
            m = re.match(r'^(L|R)\s+(.*)', part)
            if m:
                side, part = ('left' if m.group(1) == 'L' else 'right'), m.group(2)
            if re.search(r'\bboth sides\b', part):
                out.append(('both', part))
            else:
                out.append((side, part))
    return out


def things(note):
    """what the note names: list of (side, record type, kind, count), plus pole and lamp flags."""
    out, poles, lamp, transformer = [], None, 'none', False
    for side, part in clauses(note):
        p = part.lower()
        if re.search(r'\bpoles?\b|\bwires\b|\bstreetlights?\b|\blamp posts?\b', p):
            poles = poles or side or 'any'
        if re.search(r'streetlight|lamp post', p):
            lamp = 'solar' if 'solar' in p else 'steel_arm'
        if 'transformer' in p:
            transformer = True
        for rx, rt, kind, one, many in WORDS:
            m = re.search(rx, p)
            if m:
                plural = m.group(0).endswith('s') or 'many' in p or 'row' in p
                out.append((side, rt, kind, many if plural else one))
                if rt == 'stall':      # 'umbrella stall' is one umbrella, not an umbrella and a stall
                    break
    return out, poles, lamp, transformer


def main():
    d = sys.argv[1].rstrip('/')
    pf = f'{d}/plan.json'
    plan = json.load(open(pf))
    recs = plan['records']
    taken = {r['id'] for r in recs}
    done = {r['note'].split()[1] for r in recs if str(r.get('note', '')).startswith('edge rd-')}
    reads = {}
    for r in csv.DictReader((l for l in open(f'{d}/road_reads.tsv') if not l.startswith('#!')), delimiter='\t'):
        reads.setdefault(r['id'], []).append(r)
    roads = [r for r in recs if r['type'] == 'road']
    lines = {r['id']: LineString([p[:2] for p in r['centreline']]) for r in roads}
    seen = {i: [r for r in rows if r['sv'] != 'none'] for i, rows in reads.items()}
    houses = [Polygon(r['footprint']) for r in recs if r['type'] == 'building']
    htree = STRtree(houses)
    carriage = [lines[r['id']].buffer(r['width'] / 2, cap_style=2) for r in roads]
    ctree = STRtree(carriage)
    dj = json.load(open(f'{d}/district.json'))
    D = [r for r in (dj['records'] if 'records' in dj else [dj]) if r['type'] == 'district'][0]
    inside_d = unary_union([Polygon(g) for g in D['outline']]).buffer(-0.5)
    placed = []         # footprints of what this run placed
    new, counts, skipped = [], {}, {}

    def free(shape, own=None):
        """clear of houses, of what was placed, and of every carriageway but `own` (the road it may stand on)"""
        if not inside_d.contains(shape):
            return False
        if any(houses[j].intersects(shape) for j in htree.query(shape)):
            return False
        if any(j != own and carriage[j].intersection(shape).area > 0.05 for j in ctree.query(shape)):
            return False
        return not any(p.intersects(shape) for p in placed)

    def foot(x, y, kind, turn):
        hw, hl = SIZE[kind]
        return rotate(box(x - hl, y - hw, x + hl, y + hw), turn, origin=(x, y))

    for ri, road in enumerate(roads):
        rid = road['id']
        if rid in done:
            continue
        rng = random.Random(rid)
        L = lines[rid]
        n = len(reads.get(rid, [])) or max(1, round(L.length / 100))
        own = seen.get(rid) or []
        if not own:
            same = [r for r in roads if r['kind'] == road['kind'] and seen.get(r['id'])]
            own = seen[min(same, key=lambda r: lines[r['id']].distance(L))['id']][:1] if same else []
        if not own:
            continue
        w = road['width']
        crossings = road.get('crossings', [])
        guts = road.get('gutters', [])
        verge = {s: max([v['width'] for v in road.get('verges', []) if v['side'] == s] or [0]) for s in ('left', 'right')}
        prev_pole = None
        for j in range(n):
            s0, s1 = L.length * j / n, L.length * (j + 1) / n
            rows = reads.get(rid, [])
            row = rows[j] if j < len(rows) and rows[j]['sv'] != 'none' else \
                min(own, key=lambda r: abs(int(r['#i']) - (int(rows[j]['#i']) if j < len(rows) else 0)))
            items, poles, lamp, transformer = things(row['edge'])

            def frame(s):
                a, b = L.interpolate(max(s - 0.5, 0)), L.interpolate(min(s + 0.5, L.length))
                dx, dy = b.x - a.x, b.y - a.y
                k = math.hypot(dx, dy) or 1
                return L.interpolate(s), dx / k, dy / k

            def at(s, side, off):
                c, tx, ty = frame(s)
                nx, ny = (ty, -tx) if side == 'left' else (-ty, tx)    # board y down: left of travel is (ty, -tx)
                return c.x + nx * off, c.y + ny * off, math.degrees(math.atan2(ty, tx))

            def gut(side, s):
                return sum(g['width'] for g in guts if g['side'] == side and g['s0'] <= s < g['s1'])

            def busier():
                c = lambda side: sum(1 for k in htree.query(L.buffer(w / 2 + 6)) if houses[k].distance(L) < w / 2 + 6
                                     and (Point(at(L.project(houses[k].centroid), side, w / 2 + 3)[:2])
                                          .distance(houses[k]) < 4))
                return 'left' if c('left') >= c('right') else 'right'

            def put(rt, kind, side, s, fields, on_road_ok=False, inside=False):
                hw, hl = SIZE[kind]
                # a tree, a drum or a heap may stand a few metres back (in a forecourt, a gap between houses); a mast
                # well back, in a compound; anything may slide a few metres along the road to find room
                backs = (0,) if inside or rt in ('pole', 'stall') else (-12, -6, 6, 14, 22) if rt == 'mast' \
                    else (0, 1.5, 3, 5)
                ok = False
                for ds in (0, 2, -2, 4, -4, 6, -6):
                    s2 = min(max(s + ds, hl), L.length - hl)
                    if inside and any(abs(c['s'] - s2) < c['w'] / 2 + hl + 0.3 and c['side'] == side for c in crossings):
                        continue      # never parked across a gate's bridge
                    if inside:        # parked at the kerb
                        offs = [w / 2 - hw - 0.3]
                    elif rt == 'mast':
                        offs = [w / 2 + gut(side, s2) + 18 + k for k in backs]
                    else:
                        offs = [w / 2 + gut(side, s2) + hw + 0.3 + k for k in backs]
                    if on_road_ok:    # no room before the houses: on the road's own edge
                        offs.append(w / 2 - hw - 0.1)
                    for off in offs:
                        x, y, t = at(s2, side, off)
                        turn = t if (inside and side == 'right') or not inside else (t + 180) % 360
                        if rt in ('stall', 'furniture'):
                            turn = (t + (90 if side == 'left' else -90)) % 360      # faces the road
                        shape = foot(x, y, kind, turn if rt != 'pole' else 0)
                        on_own = inside or off < w / 2
                        ok = free(shape, own=ri if on_own else None) and \
                            (not inside or carriage[ri].buffer(0.1).contains(shape))
                        if ok:
                            break
                    if ok:
                        break
                if not ok:
                    skipped[kind] = skipped.get(kind, 0) + 1
                    return None
                placed.append(shape)
                r = {'id': new_id({'vehicle': 'vh', 'stall': 'st', 'tree': 'tr', 'furniture': 'fu', 'heap': 'hp',
                                   'mast': 'ms', 'pole': 'po'}[rt], rng, taken),
                     'type': rt, 'note': f'edge {rid}', 'kind': kind, 'at': [round(x, 2), round(y, 2)]}
                r.update(fields(turn))
                new.append(r)
                counts[kind] = counts.get(kind, 0) + 1
                return r

            # poles first: the line runs the stretch on one side
            if poles:
                side = poles if poles in ('left', 'right') else busier()
                k0 = math.ceil(s0 / POLE_SPAN)
                for k in range(k0, int(s1 // POLE_SPAN) + 1):
                    s = min(max(k * POLE_SPAN + rng.uniform(-3, 3), 0.5), L.length - 0.5)
                    p = put('pole', 'pole', side, s, lambda t: {
                        'kind': 'concrete', 'h': POLE_H, 'lean': [round(rng.uniform(-2, 2), 1), round(rng.uniform(-2, 2), 1)],
                        'transformer': transformer and k == k0, 'lamp': lamp, 'arm': True,
                        'wear': round(rng.uniform(0.5, 0.8), 2), 'turn': round((t + 90) % 360, 1)}, on_road_ok=True)
                    if p:
                        if prev_pole and math.dist(prev_pole['at'], p['at']) < 60:
                            new.append({'id': new_id('wi', rng, taken), 'type': 'wire', 'note': f'edge {rid}',
                                        'from_pole': prev_pole['id'], 'to_pole': p['id'], 'n': 4, 'sag': 0.4,
                                        'kind': 'line'})
                            counts['wire'] = counts.get('wire', 0) + 1
                        prev_pole = p
            else:
                prev_pole = None
            for side0, rt, kind, count in items:
                sides = ['left', 'right'] if side0 == 'both' else [side0]
                for side in sides:
                    for _ in range(count):
                        sd = side or rng.choice(['left', 'right'])
                        s = rng.uniform(s0 + 2, max(s1 - 2, s0 + 2.1))
                        if rt == 'vehicle':
                            if w < 4.5:
                                skipped[kind] = skipped.get(kind, 0) + 1
                                continue
                            col = {'danfo': '#f2b705', 'keke': '#e8b818', 'bus': '#f2b705', 'okada': rng.choice(['#1b1b1b', '#7a1f1f'])}.get(kind, rng.choice(CAR))
                            put(rt, kind, sd, s, lambda t, col=col: {'turn': round(t, 1), 'colour': col,
                                                                    'wear': round(rng.uniform(0.3, 0.8), 2)}, inside=True)
                        elif rt == 'stall':
                            def f(t, kind=kind):
                                o = {'turn': round(t, 1), 'w': round(SIZE[kind][1] * 2, 1), 'd': round(SIZE[kind][0] * 2, 1),
                                     'h': {'kiosk': 2.2, 'umbrella': 0.8, 'container_shop': 2.6}.get(kind, 0.9),
                                     'colour': rng.choice(['#6b4a2f', '#2d5d8a', '#8a8f93', '#5a3328', '#3f6e4a']),
                                     'wear': round(rng.uniform(0.4, 0.9), 2)}
                                if kind == 'umbrella':
                                    o['umbrella'] = {'diameter': 2.2, 'colours': rng.choice(UMBRELLA)}
                                return o
                            put(rt, kind, sd, s, f, on_road_ok=True)
                        elif rt == 'tree':
                            def f(t, kind=kind):
                                if kind == 'palm':
                                    h = round(rng.uniform(7, 12), 1)
                                    form = {'fronds': {'cols': ['turn', 'droop', 'len'], 'rows': [
                                        [i * 30 + rng.randint(-8, 8), rng.randint(25, 65), round(rng.uniform(3, 4.2), 1)]
                                        for i in range(12)]}}
                                else:
                                    h = round(rng.uniform(6, 10), 1)
                                    form = {'lobes': {'cols': ['x', 'y', 'z', 'r'], 'rows': [
                                        [round(rng.uniform(-1.5, 1.5), 1), round(rng.uniform(-1.5, 1.5), 1),
                                         round(h - rng.uniform(1, 3), 1), round(rng.uniform(1.5, 2.6), 1)] for _ in range(4)]}}
                                return {'h': h, 'lean': [round(rng.uniform(-4, 4), 1), round(rng.uniform(-4, 4), 1)], 'form': form}
                            put(rt, kind, sd, s, f)
                        elif rt == 'furniture':
                            put(rt, kind, sd, s, lambda t, kind=kind: {
                                'z': 0, 'turn': round(t, 1), 'wear': round(rng.uniform(0.4, 0.9), 2),
                                'colour': {'drum': rng.choice(['#1f5fbf', '#2b2b2b', '#b23a2a']), 'water_tank': '#1b1b1b',
                                           'tyre_stack': '#1b1b1b', 'generator': '#c43b2b'}.get(kind, '#6b4a2f'),
                                **({'length': rng.randint(3, 7)} if kind == 'tyre_stack' else {})})
                        elif rt == 'heap':
                            put(rt, kind, sd, s, lambda t: {'r': SIZE[kind][0], 'h': 0.7 if kind == 'rubbish' else 1.0})
                        elif rt == 'mast':
                            put(rt, kind, sd, s, lambda t: {'h': 30, 'colour': '#b9bcbf'})
    recs.extend(new)
    print(f'{len(new)} records:', dict(sorted(counts.items())))
    print('not placed (no free room):', dict(sorted(skipped.items())))
    if '--dry' not in sys.argv:
        json.dump(plan, open(pf, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
