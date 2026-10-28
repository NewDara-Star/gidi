"""The city layer's main roads, first draft (owner, 28 Oct: "make sure we get all the roads and interconnected travel
lines correct and right"; DECISIONS "The whole network first, to a drive in Unreal" and "1:3 sets where things are; a
road keeps its real shape").

  ~/.venvs/gidi/bin/python -I scripts/draft_network.py OUT_DIR          picture and report only, nothing written
  ~/.venvs/gidi/bin/python -I scripts/draft_network.py OUT_DIR --write  also adds the roads to map/d00/plan.json

Reads Overture's motorway, trunk and primary segments (OpenStreetMap's lines; ~/gidi-data/research/data/overture-lagos/)
inside the frame, in real metres (UTM 31N), and merges each dual carriageway into one centreline with neatnet
(Fleischmann et al. 2025, the method published for this: two one-way lines a median apart become the line between
them). Only then is it put into the Gidi frame at 1:3 (working_bar.gidi): where a road goes and where it meets the
others is 1:3; its width is real, one record from kerb to kerb with its median, as Ikorodu Road's.

Each merged line takes the class and the name of the Overture lines it was made from (by the length of them within
MATCH m). Widths are a default by kind, marked "not read" in the note, to be read on Google road by road, longest
first. Heights are not drafted: a road over another is listed as a flyover to draw (owed), and neatnet drops the
interchanges' slip roads, which are drawn by hand with their main road.

A junction is a point where three or more lines meet, or two of a different class or name. Each is written with an
id to the twin catalogue outside the repo (~/gidi-data/research/twins/junctions.tsv: the real road names that meet,
the nearest of the frame study's 819 real places and the district it lands in), because the map never holds real
names (docs/MAP-FORMAT.md "References to the real place"); the map's road keeps the ids of the junctions on it in its
note, so a district's streets know where they meet the network when the district is remade (owner, 28 Oct).

A draft never overwrites: the hand-drawn records already in map/d00 (Third Mainland, Ikorodu Road) stay, the draft is
cut back from them, and its cut ends are listed for joining by hand. If map/d00 already holds drafted roads, nothing is
written.
"""
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

import geopandas as gpd
import pyarrow.parquet as pq
import shapely
from shapely.geometry import LineString, MultiLineString, Point, box
from shapely.ops import linemerge, unary_union
from shapely.strtree import STRtree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from check_map import canonical   # noqa: E402
from map_picture import polys   # noqa: E402

SEG = os.path.expanduser('~/gidi-data/research/data/overture-lagos/lagos_overture_segment.parquet')
TWINS = os.path.expanduser('~/gidi-data/research/twins/junctions.tsv')
X0, Y0, W, H = 500525, 707825, 27000, 10500
CLASSES = ('motorway', 'trunk', 'primary')
KIND = {'motorway': 'motorway', 'trunk': 'trunk', 'primary': 'main_road'}
WIDTH = {'motorway': 24.0, 'trunk': 18.0, 'primary': 11.0}   # m, real: three, two and one lanes a way with a median; not read
MATCH = 25.0        # real m: an Overture line this near a merged line made it
KEEP_OFF = 10.0     # Gidi m past a hand record's kerb that the draft is cut back to
SHORT = 20.0        # Gidi m: a piece shorter than this after the cut is dropped
STUB = 50.0         # Gidi m: a piece with a loose end, shorter than this, is a slip road neatnet half took off
TOUCH = 0.05        # Gidi m: an end this near another line is on it
JOIN = 15.0         # Gidi m past a road's kerb: a loose end this near it is a junction the merge left open
EDGE = 0.5          # Gidi m: centrelines kept this far inside the frame (d00's own outline)
MARK = 'scripts/draft_network.py'


def gidi(x, y):
    return (round(min(max((x - X0) / 3, EDGE), W - EDGE), 2), round(min(max(H - (y - Y0) / 3, EDGE), H - EDGE), 2))


def read_overture():
    t = pq.read_table(SEG, columns=['id', 'subtype', 'class', 'names', 'road_flags', 'geometry']).to_pylist()
    F = box(X0, Y0, X0 + 3 * W, Y0 + 3 * H)
    rows = [{'id': r['id'], 'cls': r['class'], 'name': (r['names'] or {}).get('primary'),
             'unbuilt': any('is_under_construction' in (f.get('values') or []) for f in r['road_flags'] or []),
             'geometry': shapely.from_wkb(r['geometry'])}
            for r in t if r['subtype'] == 'road' and r['class'] in CLASSES]
    g = gpd.GeoDataFrame(rows, crs=4326).to_crs(32631)
    g = g[g.intersects(F)].copy()
    g['geometry'] = g.intersection(F)
    g = g.explode(index_parts=False)
    return g[g.geom_type == 'LineString'].reset_index(drop=True)


def attribute(out, src):
    """Each merged line's class and name: the most length of source lines within MATCH m (real) of it."""
    tree = STRtree(list(src.geometry))
    cls, name, unbuilt = [], [], []
    for L in out.geometry:
        c, n, u = Counter(), Counter(), Counter()
        near = L.buffer(MATCH)
        for j in tree.query(near):
            s = src.iloc[j]
            run = s.geometry.intersection(near).length
            c[s.cls] += run
            u[bool(s.unbuilt)] += run
            if isinstance(s['name'], str):
                n[s['name']] += run
        # the highest class with near its own length of lines; a short touch of a motorway at a junction is not it
        top = [k for k in CLASSES if c[k] > 0.4 * L.length]
        cls.append(top[0] if top else (c.most_common(1)[0][0] if c else 'primary'))
        name.append(n.most_common(1)[0][0] if n else None)
        unbuilt.append(u[True] > u[False])
    out = out.copy()
    out['cls'], out['name'], out['unbuilt'] = cls, name, unbuilt
    return out


def with_point(L, at):
    """L with the point at put in on the segment it lies on (a no-op if it is already one of L's points)."""
    cs = list(L.coords)
    if any(abs(a[0] - at[0]) < 0.01 and abs(a[1] - at[1]) < 0.01 for a in cs):
        return L
    d = L.project(Point(at))
    run = 0.0
    for i, (a, b) in enumerate(zip(cs, cs[1:])):
        seg = Point(a).distance(Point(b))
        if run + seg >= d:
            return LineString(cs[:i + 1] + [at] + cs[i + 1:])
        run += seg
    return L


def to_gidi(L):
    return LineString([gidi(x, y) for x, y in L.coords])


def hand_roads():
    plan = os.path.join(ROOT, 'map', 'd00', 'plan.json')
    recs = json.load(open(plan))['records']
    return plan, recs, [r for r in recs if r['type'] == 'road']


def main():
    out_dir = sys.argv[1]
    write = '--write' in sys.argv
    os.makedirs(out_dir, exist_ok=True)
    plan, recs, hand = hand_roads()
    if any(MARK in r.get('note', '') for r in hand):
        sys.exit('map/d00 already holds drafted roads: a draft never overwrites (re-drafted only when the owner asks)')
    import neatnet
    src = read_overture()
    merged = neatnet.neatify(src[['geometry']].copy())
    merged = merged[merged.geom_type == 'LineString'].reset_index(drop=True)
    merged = attribute(merged, src)
    print(f'Overture: {len(src)} lines, {src.length.sum() / 1000:.0f} km real; merged: {len(merged)} lines, '
          f'{merged.length.sum() / 1000:.0f} km real')

    # into the Gidi frame, cut back from the hand records
    hand_lines = [LineString([p[:2] for p in r['centreline']]) for r in hand]
    hand_zone = unary_union([L.buffer(r['width'] / 2 + KEEP_OFF) for L, r in zip(hand_lines, hand)])
    pieces, cut_ends = [], []
    for L, c, n in zip(merged.geometry, merged.cls, merged['name']):
        G = to_gidi(L)
        rest = G.difference(hand_zone)
        for p in getattr(rest, 'geoms', [rest]):
            if p.geom_type != 'LineString' or p.length < SHORT:
                continue
            for e in (p.coords[0], p.coords[-1]):
                if Point(e).distance(hand_zone.boundary) < 0.5:
                    cut_ends.append((e, c, n))
            pieces.append((p, c, n))

    # stubs: a short piece with an end on nothing is what is left of an interchange's slip road; taken off until none
    while True:
        tree = STRtree([p for p, _, _ in pieces])
        on = lambda e, k: [j for j in tree.query(Point(e).buffer(TOUCH)) if j != k
                           and pieces[j][0].distance(Point(e)) < TOUCH]
        loose = lambda e, k: not on(e, k) and Point(e).distance(hand_zone.boundary) >= 0.5
        drop = {k for k, (p, _, _) in enumerate(pieces)
                if p.length < STUB and (loose(p.coords[0], k) or loose(p.coords[-1], k))}
        if not drop:
            break
        pieces = [x for k, x in enumerate(pieces) if k not in drop]
    # a loose end within JOIN of another road's kerb is a junction the merge left open: it is taken on to the
    # nearest point of that road, which gets a point there, so the two share it
    for k in range(len(pieces)):
        for first in (True, False):
            p, c, n = pieces[k]
            e = Point(p.coords[0] if first else p.coords[-1])
            tree = STRtree([q for q, _, _ in pieces])
            if on(e.coords[0], k) or e.distance(hand_zone.boundary) < 0.5:
                continue
            best = None
            for j in tree.query(e.buffer(max(WIDTH.values()) / 2 + JOIN)):
                d = pieces[j][0].distance(e)
                if j != k and d < WIDTH[pieces[j][1]] / 2 + JOIN and (best is None or d < best[0]):
                    best = (d, j)
            if best is None:
                continue
            j = best[1]
            q = pieces[j][0]
            at = q.interpolate(q.project(e))
            at = (round(at.x, 2), round(at.y, 2))
            pieces[j] = (with_point(q, at), pieces[j][1], pieces[j][2])
            cs = list(p.coords)
            pieces[k] = (LineString([at] + cs if first else cs + [at]), c, n)
    tree = STRtree([p for p, _, _ in pieces])

    # junctions: where an end meets two or more other lines, or one of a different class or name
    junctions, dead = {}, []
    for k, (p, c, n) in enumerate(pieces):
        for e in (p.coords[0], p.coords[-1]):
            js = on(e, k)
            q = (round(e[0], 1), round(e[1], 1))
            if not js:
                if 1 < q[0] < W - 1 and 1 < q[1] < H - 1 and Point(e).distance(hand_zone.boundary) >= 0.5:
                    dead.append(q)
            elif len(js) >= 2 or (pieces[js[0]][1], pieces[js[0]][2]) != (c, n):
                junctions.setdefault(q, set()).update([k, *js])

    # merge runs of one road (same class and name) through points that are not junctions
    roads = []
    groups = defaultdict(list)
    for p, c, n in pieces:
        groups[(c, n)].append(p)
    jpts = set(junctions)
    for (c, n), ls in groups.items():
        m = linemerge(MultiLineString(ls)) if len(ls) > 1 else ls[0]
        for L in getattr(m, 'geoms', [m]):    # a junction linemerge ran through stays a vertex of the line
            roads.append((L, c, n))

    # flyovers to draw: two roads crossing with no shared point
    lines = [L for L, _, _ in roads]
    tree = STRtree(lines)
    crossings = []
    for i, L in enumerate(lines):
        for j in tree.query(L):
            if j <= i or not L.crosses(lines[j]):
                continue
            x = L.intersection(lines[j])
            for g in getattr(x, 'geoms', [x]):
                if g.geom_type == 'Point':
                    crossings.append((round(g.x, 1), round(g.y, 1)))

    # where each junction is: district and nearest real place (frame study)
    s = open(os.path.join(ROOT, 'web', 'frame-study.js')).read()
    FS = json.loads(s[s.index('{'):s.rindex('}') + 1])
    dist = [(d['n'], d['name'], polys(d['rings'])) for d in FS['districts']]
    places = FS['places']

    def where(q):
        d = next(((n, nm) for n, nm, g in dist if g.contains(Point(q))), (0, 'outside the districts'))
        pl = min(places, key=lambda p: (p['at'][0] - q[0]) ** 2 + (p['at'][1] - q[1]) ** 2)
        return d, pl['n'], ((pl['at'][0] - q[0]) ** 2 + (pl['at'][1] - q[1]) ** 2) ** 0.5

    jid = {q: 'jn-' + hashlib.sha1(f'd00 junction {q[0]} {q[1]}'.encode()).hexdigest()[:8] for q in junctions}
    tsv = ['id\tx\ty\tdistrict\tdistrict_name\tnearest_place\tplace_m\troads']
    for q, ks in sorted(junctions.items()):
        (dn, dname), pl, pm = where(q)
        names = sorted({f'{pieces[k][2] or "(no name)"} ({pieces[k][1]})' for k in ks})
        tsv.append(f'{jid[q]}\t{q[0]}\t{q[1]}\td{dn:02d}\t{dname}\t{pl}\t{pm:.0f}\t{"; ".join(names)}')

    km = Counter()
    for L, c, _ in roads:
        km[c] += L.length / 1000
    print(f'draft: {len(roads)} roads, ' + ', '.join(f'{c} {km[c]:.1f} km' for c in CLASSES)
          + f' (Gidi km); {len(junctions)} junctions; {len(dead)} dead ends inside the frame; '
          f'{len(cut_ends)} ends cut back from the hand records; {len(crossings)} crossings with no shared point '
          f'(flyovers to draw, or junctions neatnet missed)')
    open(os.path.join(out_dir, 'junctions.tsv'), 'w').write('\n'.join(tsv) + '\n')
    json.dump({'dead': dead, 'cut_ends': [e for e, _, _ in cut_ends], 'crossings': crossings},
              open(os.path.join(out_dir, 'draft_network_ends.json'), 'w'))
    picture(out_dir, roads, hand_lines, list(junctions), dead, cut_ends, crossings, FS)

    if not write:
        return
    unbuilt = unary_union([to_gidi(L).buffer(1.0) for L, u in zip(merged.geometry, merged.unbuilt) if u])
    new = []
    for L, c, n in roads:
        on = [jid[q] for q in junctions if Point(q).distance(L) < 0.05]
        rid = 'rd-' + hashlib.sha1(f'd00 network {L.wkt}'.encode()).hexdigest()[:8]
        new.append({'id': rid, 'type': 'road', 'kind': KIND[c], 'width': WIDTH[c], 'surface': 'tar_worn',
                    'sand_cover': 'none', 'kerb_left': 'raised_pavement', 'kerb_right': 'raised_pavement',
                    'median': 'low_concrete' if c != 'primary' else 'none', 'crown': 0.2, 'crossings': [],
                    'gutters': [], 'verges': [], 'ground_look': {},
                    'centreline': [list(p) for p in L.coords],
                    'note': f'City layer, first draft ({MARK}, 28 Oct): Overture {c} lines merged to one centreline '
                            f'by neatnet, at 1:3. Width {WIDTH[c]} m is the default for its kind, not read; heights '
                            f'not drafted. Junctions on it: {", ".join(on) or "none"} (twin catalogue '
                            f'junctions.tsv)' + ('. Overture marks it under construction: drawn as being built'
                                                 if L.intersection(unbuilt).length > 0.5 * L.length else '')})
    doc = json.load(open(plan))
    doc['records'] += new
    open(plan, 'w').write(canonical(doc))
    os.makedirs(os.path.dirname(TWINS), exist_ok=True)
    open(TWINS, 'w').write('\n'.join(tsv) + '\n')
    print(f'written {len(new)} roads into {plan}; {len(tsv) - 1} junctions into {TWINS}')


def picture(out_dir, roads, hand_lines, junctions, dead, cut_ends, crossings, FS):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    look = {'motorway': ('#b0281e', 1.4), 'trunk': ('#d9661f', 1.1), 'primary': ('#c9961a', 0.7)}
    fig, ax = plt.subplots(figsize=(20, 8.4), dpi=150)
    for d in FS['districts']:
        g = polys(d['rings'])
        for p in getattr(g, 'geoms', [g]):
            if p.geom_type == 'Polygon':
                ax.fill(*p.exterior.xy, fc='#f4efe6', ec='#d4c9b4', lw=0.4)
        ax.text(*d['at'], d['name'], fontsize=5, color='#9a8e78', ha='center')
    for L, c, _ in roads:
        ax.plot(*L.xy, color=look[c][0], lw=look[c][1], solid_capstyle='round')
    for L in hand_lines:
        ax.plot(*L.xy, color='#1f4fb0', lw=1.8)
    if junctions:
        ax.scatter(*zip(*junctions), s=4, c='#222', zorder=5, label=f'junctions ({len(junctions)})')
    if dead:
        ax.scatter(*zip(*dead), s=14, marker='x', c='#7a00a8', zorder=6, label=f'dead ends ({len(dead)})')
    if crossings:
        ax.scatter(*zip(*crossings), s=12, marker='o', facecolors='none', edgecolors='#0a8a3a', zorder=6,
                   label=f'crossings with no shared point ({len(crossings)})')
    if cut_ends:
        ax.scatter(*zip(*[e for e, _, _ in cut_ends]), s=18, marker='s', facecolors='none', edgecolors='#1f4fb0',
                   zorder=6, label=f'cut back from hand roads ({len(cut_ends)})')
    for c in CLASSES:
        ax.plot([], [], color=look[c][0], lw=2, label=c)
    ax.plot([], [], color='#1f4fb0', lw=2, label='drawn by hand (Third Mainland, Ikorodu Road)')
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.set_aspect('equal')
    ax.legend(loc='lower left', fontsize=8)
    ax.set_title('Gidi city layer: main roads, first draft (1:3 positions, real widths), not yet in the map')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, 'draft_network.png'))


if __name__ == '__main__':
    main()
