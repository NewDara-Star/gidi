"""The real main road network inside the Gidi frame: what the city layer map/d00 is drawn from (owner, 28 Oct: "make
the bigger things that connect the city. Then go down"; "real roads and interconnections as well as its waters are the
only things we are taking from Lagos one to one").

Reads Overture's road and rail segments (OpenStreetMap's lines; ~/gidi-data/research/data/overture-lagos/) of class motorway,
trunk, primary and secondary and their links, put into the Gidi frame (working_bar.gidi, 1:3). Prints the km per
class, the bridges, tunnels, raised levels and under-construction pieces Overture flags, the named roads by length,
and the junctions: Overture's connectors where three or more main segments meet, or two of a different class or
name (a connector on two segments of one road is that road continuing, not a junction). Draws the
network over the 51 districts of the frame study with the drawn districts' own roads, so what we have drawn can be
seen against the real lines. A line here is a reading to draw from by hand, read again on Google piece by piece: OSM
can hold roads still only planned, and Overture carries no widths for Lagos.

  ~/.venvs/gidi/bin/python -I scripts/city_network.py OUT_DIR        prints the inventory, writes OUT_DIR/city_network.png
"""
import json
import os
import sys
from collections import Counter, defaultdict

import pyarrow.parquet as pq
import shapely
from pyproj import Transformer
from shapely.geometry import LineString, box

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from map_picture import polys   # noqa: E402
from working_bar import gidi   # noqa: E402

SEG = os.path.expanduser('~/gidi-data/research/data/overture-lagos/lagos_overture_segment.parquet')
MAIN = ('motorway', 'trunk', 'primary', 'secondary')
FRAME = box(0, 0, 27000, 10500)
LOOK = {'motorway': ('#b0281e', 1.6), 'trunk': ('#d9661f', 1.3), 'primary': ('#d9a21f', 0.9),
        'secondary': ('#7f7f7f', 0.5)}


def flagged(r, flag):
    return any(flag in f['values'] for f in r['road_flags'] or [] if f.get('values'))


def main():
    out = sys.argv[1]
    T = Transformer.from_crs(4326, 32631, always_xy=True)
    t = pq.read_table(SEG, columns=['names', 'subtype', 'class', 'connectors', 'road_flags', 'level_rules',
                                    'geometry']).to_pylist()
    segs = []
    for r in t:
        if r['subtype'] != 'road' or r['class'] not in MAIN:
            continue
        g = shapely.from_wkb(r['geometry'])
        L = LineString([gidi(x, y, T) for x, y in g.coords])
        if L.intersects(FRAME):
            segs.append((r, L.intersection(FRAME)))
    km, link, flags, levels, names, joins = Counter(), Counter(), Counter(), Counter(), defaultdict(float), defaultdict(list)
    for r, L in segs:
        c = r['class']
        km[c] += L.length / 1000
        if flagged(r, 'is_link'):
            link[c] += L.length / 1000
        for f in ('is_bridge', 'is_tunnel', 'is_under_construction'):
            if flagged(r, f):
                flags[(c, f)] += L.length / 1000
        for lv in r['level_rules'] or []:
            levels[lv['value']] += 1
        names[(c, (r['names'] or {}).get('primary') or '(no name)')] += L.length / 1000
        for cc in r['connectors'] or []:
            joins[cc['connector_id']].append((c, (r['names'] or {}).get('primary')))
    print('km Gidi (1:3) inside the frame, by class (of which ramps and links):')
    for c in MAIN:
        print(f'   {c:10s} {km[c]:6.1f} km  (links {link[c]:.1f})')
    print('flagged, km Gidi:', ', '.join(f'{c} {f[3:]} {v:.1f}' for (c, f), v in sorted(flags.items())))
    print('segments with a level (above or below the ground):', dict(sorted(levels.items())))
    junctions = [v for v in joins.values() if len(v) >= 3 or (len(v) == 2 and v[0] != v[1])]
    print(f'junctions: {len(junctions)} ({sum(1 for v in junctions if len(v) >= 3)} of three or more segments); '
          f'{sum(1 for v in joins.values() if len(v) == 2 and v[0] == v[1])} more connectors are one road continuing')
    print('named roads, longest first (km Gidi):')
    for (c, nm), v in sorted(names.items(), key=lambda x: -x[1])[:40]:
        print(f'   {c:10s} {v:6.2f}  {nm}')

    rails = []
    for r in pq.read_table(SEG, columns=['subtype', 'class', 'geometry']).to_pylist():
        if r['subtype'] == 'rail':
            g = shapely.from_wkb(r['geometry'])
            L = LineString([gidi(x, y, T) for x, y in g.coords])
            if L.intersects(FRAME):
                rails.append(L.intersection(FRAME))
    print(f'rail inside the frame: {sum(L.length for L in rails) / 1000:.1f} km Gidi in {len(rails)} segments')
    picture(segs, rails, os.path.join(out, 'city_network.png'))


def lines(g):
    return [p for p in getattr(g, 'geoms', [g]) if p.geom_type == 'LineString' and not p.is_empty]


def picture(segs, rails, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    s = open(os.path.join(ROOT, 'web', 'frame-study.js')).read()
    F = json.loads(s[s.index('{'):s.rindex('}') + 1])
    fig, ax = plt.subplots(figsize=(18, 7.6), dpi=170)
    for x in F['districts']:
        g = polys(x['rings'])
        for p in getattr(g, 'geoms', [g]):
            if p.geom_type == 'Polygon':
                ax.fill(*p.exterior.xy, fc='#f4efe6', ec='#c9bda6', lw=0.5)
    for d in sorted(os.listdir(os.path.join(ROOT, 'map'))):
        plan = os.path.join(ROOT, 'map', d, 'plan.json')
        if d == 'd00' or not os.path.exists(plan):
            continue
        for r in json.load(open(plan))['records']:
            if r.get('type') == 'road':
                xs, ys = zip(*[q[:2] for q in r['centreline']])
                ax.plot(xs, ys, c='#3a78c2', lw=0.25)
    for L in rails:
        for p in lines(L):
            ax.plot(*p.xy, c='#000000', lw=0.9, ls=(0, (3, 1.5)))
    for c in reversed(MAIN):
        for r, L in segs:
            if r['class'] == c:
                col, lw = LOOK[c]
                planned = flagged(r, 'is_under_construction')
                for p in lines(L):
                    ax.plot(*p.xy, c=col, lw=lw, solid_capstyle='butt', ls=(0, (1, 1.5)) if planned else '-',
                            alpha=0.55 if planned else 1)
    for r, L in segs:
        if flagged(r, 'is_bridge') and not flagged(r, 'is_under_construction'):
            for p in lines(L):
                ax.plot(*p.xy, c='#1fa0a8', lw=LOOK[r['class']][1] + 0.8, alpha=0.9)
    ax.set_xlim(0, 27000)
    ax.set_ylim(10500, 0)    # Gidi y runs south: north at the top
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('The real main road network in the Gidi frame (Overture/OSM lines at 1:3): motorway red, trunk orange, '
                 'primary gold, secondary grey; bridges teal; dotted: flagged under construction; rail dashed black;\n'
                 'our drawn districts\' roads blue. North at the top; 27 x 10.5 km Gidi (81 x 31.5 km real)',
                 fontsize=9)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
