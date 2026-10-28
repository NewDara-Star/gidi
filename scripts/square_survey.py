"""Cuts a district into squares for the square-by-square line survey (owner, 28 Oct: "since you're a machine, you need
to find out ways that you would not miss obvious things"). The method: never a wide view; one square at a time at
close zoom, the same questions for every square with "none" as an answer, and the squares counted by this script.

Each square is SQ Gidi metres a side (SQ x 3 real, one Google satellite view at zoom 19 with nothing shrunk away). For
every square at least half inside the outline it prints: its centre in Gidi metres and real lat/lon, a Google Maps
satellite link for that centre, our roof cover against Google Open Buildings' at its 90%-precision threshold (the
same file and tile as working_bar.py's density row; a per-area figure, so the 1:3 scale does not change it), and our
counts there of walls, plots, stalls, poles, places by kind and roads by kind.

At 1:3 a real square holds about nine times the houses of ours, so a square is compared by shares and kinds (how many
houses walled, whether shop rows line the road), never roof by roof.

  ~/.venvs/gidi/bin/python -I scripts/square_survey.py d15                      every square, a count
  ~/.venvs/gidi/bin/python -I scripts/square_survey.py d15 --pick=10 --out=DIR  ten squares across Google's cover,
                                                                                 a table and a picture of ours for each
"""
import csv
import gzip
import json
import os
import sys
from collections import Counter

import shapely
from pyproj import Transformer
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from working_bar import GOOGLE, THRESHOLDS, gidi   # noqa: E402

SQ = 70.0          # Gidi metres a side: 210 m real
INSIDE = 0.5       # share of a square that must lie inside the outline


def main():
    d = sys.argv[1]
    opts = dict(a[2:].split('=', 1) for a in sys.argv[2:] if a.startswith('--'))
    plan = json.load(open(os.path.join(ROOT, 'map', d, 'plan.json')))['records']
    ring = Polygon(json.load(open(os.path.join(ROOT, 'map', d, 'district.json')))['records'][0]['outline'][0])
    T = Transformer.from_crs(4326, 32631, always_xy=True)
    inv = Transformer.from_crs(32631, 4326, always_xy=True)

    x0, y0, x1, y1 = ring.bounds
    squares = []
    for i in range(int((x1 - x0) // SQ) + 1):
        for j in range(int((y1 - y0) // SQ) + 1):
            b = box(x0 + i * SQ, y0 + j * SQ, x0 + (i + 1) * SQ, y0 + (j + 1) * SQ)
            if b.intersection(ring).area >= INSIDE * b.area:
                squares.append((f'{d}-{i:02d}{j:02d}', b))
    print(f'{d}: {len(squares)} squares of {SQ:.0f} m (Gidi; {3 * SQ:.0f} m real), at least {INSIDE:.0%} inside')
    if 'pick' not in opts:
        return

    # Google's roofs at its 90%-precision threshold for the tile holding the district, into the Gidi frame
    lon0, lat0 = inv.transform(500525 + 3 * ring.centroid.x, 707825 + 3 * (10500 - ring.centroid.y))
    t90 = next(float(r['confidence_threshold_90%_precision']) for r in csv.DictReader(open(THRESHOLDS))
               if shapely.from_wkt(r['geometry']).contains(Point(lon0, lat0)))
    w, n = inv.transform(500525 + 3 * x0, 707825 + 3 * (10500 - y0))
    e, s = inv.transform(500525 + 3 * x1, 707825 + 3 * (10500 - y1))
    g = []
    with gzip.open(GOOGLE, 'rt') as f:
        for r in csv.DictReader(f):
            la, lo = float(r['latitude']), float(r['longitude'])
            if float(r['confidence']) >= t90 and w <= lo <= e and s <= la <= n:
                g.append(shapely.transform(shapely.from_wkt(r['geometry']), lambda a: [gidi(x, y, T) for x, y in a]))
    G = unary_union(g)
    B = [Polygon(r['footprint']) for r in plan if r.get('type') == 'building' and r.get('footprint')]
    O = unary_union([p.buffer(0) for p in B])

    rows = []
    for sid, b in squares:
        inner = b.intersection(ring)
        rows.append((sid, b, G.intersection(inner).area / inner.area, O.intersection(inner).area / inner.area))
    rows.sort(key=lambda t: t[2])
    k = int(opts['pick'])
    picked = [rows[round(q * (len(rows) - 1) / (k - 1))] for q in range(k)]   # evenly across Google's cover

    out = opts.get('out', '.')
    os.makedirs(out, exist_ok=True)
    print(f'Google threshold {t90} (90% precision); {len(g)} real roofs in the district\'s box')
    for sid, b, gc, oc in picked:
        cx, cy = b.centroid.x, b.centroid.y
        lon, lat = inv.transform(500525 + 3 * cx, 707825 + 3 * (10500 - cy))
        c = Counter()
        for r in plan:
            t = r.get('type')
            geo = (Point(r['at']) if 'at' in r else LineString(r['line']) if 'line' in r else
                   LineString([q[:2] for q in r['centreline']]) if 'centreline' in r else
                   Polygon(r['outline']) if 'outline' in r else
                   Polygon(r['area'][0]) if 'area' in r and r['area'] else None)
            if t == 'building' or geo is None or not geo.intersects(b):
                continue
            c[f"{t}:{r.get('kind')}" if t in ('place', 'road', 'plot') else t] += 1
        nb = sum(1 for p in B if b.contains(p.centroid))
        print(f'{sid} centre {cx:.0f},{cy:.0f} real {lat:.5f},{lon:.5f} Google {gc:.0%} ours {oc:.0%} houses {nb} '
              f'https://www.google.com/maps/@{lat:.5f},{lon:.5f},19z/data=!3m1!1e3')
        print('   ' + ', '.join(f'{a} {v}' for a, v in sorted(c.items())))
        picture(sid, b, plan, os.path.join(out, f'{sid}.png'), f'{sid}  ours {oc:.0%} / Google {gc:.0%}  houses {nb}')


def picture(sid, b, plan, path, title):
    """Our map in the square: roads at their width, houses, walls, plots, places, stalls and poles."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    view = b.buffer(5, join_style=2)
    fig, ax = plt.subplots(figsize=(7, 7), dpi=130)

    def fill(poly, **kw):
        for p in getattr(poly, 'geoms', [poly]):
            if not p.is_empty and p.geom_type == 'Polygon':
                ax.fill(*p.exterior.xy, **kw)

    for r in plan:
        t = r.get('type')
        if t == 'road':
            L = LineString([q[:2] for q in r['centreline']])
            if L.intersects(view):
                fill(L.buffer(float(r['width']) / 2, cap_style=2).intersection(view), color='#9a9a9a', lw=0)
    for r in plan:
        t = r.get('type')
        if t == 'plot' and Polygon(r['outline']).intersects(view):
            fill(Polygon(r['outline']).intersection(view), facecolor='#e8e0c0', edgecolor='#a08040', lw=1)
        elif t == 'place' and r.get('area') and Polygon(r['area'][0]).intersects(view):
            p = Polygon(r['area'][0]).buffer(0)
            fill(p.intersection(view), facecolor='none', edgecolor='#2060c0', lw=1, ls='--')
            ax.text(*p.centroid.coords[0], r.get('kind'), color='#2060c0', fontsize=7, ha='center')
        elif t == 'building' and Polygon(r['footprint']).intersects(view):
            fill(Polygon(r['footprint']).buffer(0), facecolor='#c86a4a', edgecolor='#5a2a1a', lw=0.4)
    for r in plan:
        t = r.get('type')
        if t == 'wall' and LineString(r['line']).intersects(view):
            ax.plot(*LineString(r['line']).xy, color='black', lw=1.5)
        elif t in ('stall', 'pole', 'furniture', 'tree', 'mast', 'heap') and view.contains(Point(r['at'])):
            m = {'stall': ('s', '#e0a020'), 'pole': ('x', '#303030'), 'furniture': ('.', '#606060'),
                 'tree': ('o', '#3a8a3a'), 'mast': ('^', '#000000'), 'heap': ('v', '#806040')}[t]
            ax.plot(*r['at'][:2], marker=m[0], color=m[1], ms=4, ls='none')
    ax.plot(*b.exterior.xy, color='#d02020', lw=1)
    ax.set_xlim(view.bounds[0], view.bounds[2])
    ax.set_ylim(view.bounds[3], view.bounds[1])    # Gidi y runs south: north at the top
    ax.set_aspect('equal')
    ax.set_title(title + f'\nred square {SQ:.0f} m Gidi = {3 * SQ:.0f} m real; north up', fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
