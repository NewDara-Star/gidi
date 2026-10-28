"""A picture of the Gidi map, made each time a district reaches the working bar (owner, 26 Oct: "generate a photo of the
map everytime you get a district to working"; the first one showed the land no district held).

  ~/.venvs/gidi/bin/python scripts/map_picture.py OUT_DIR [--near=d13]

Writes OUT_DIR/gidi_city.png (all 51 districts from the frame study, the drawn ones white with their roads and houses)
and OUT_DIR/gidi_near.png (a close view round the named district and its drawn neighbours: roads at their real width,
houses). Land the frame study gave a drawn district that no drawn district holds is shaded red: a gap to give to a
district by hand (or land a border decision gave to a district not drawn yet). Look at both before sending them.
"""
import json
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.ops import unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def polys(rings):
    out = []

    def walk(x):
        if isinstance(x[0][0], (int, float)):
            out.append(Polygon(x).buffer(0))
        else:
            for y in x:
                walk(y)
    walk(rings)
    return unary_union(out)


def fill(ax, g, **kw):
    for p in getattr(g, 'geoms', [g]):
        if p.geom_type == 'Polygon' and not p.is_empty:
            xs, ys = p.exterior.xy
            ax.fill(xs, ys, **kw)


def main():
    out = sys.argv[1]
    near = next((a.split('=')[1] for a in sys.argv[2:] if a.startswith('--near=')), None)
    s = open(os.path.join(ROOT, 'web', 'frame-study.js')).read()
    F = json.loads(s[s.index('{'):s.rindex('}') + 1])
    drawn, city = {}, []
    for d in sorted(os.listdir(os.path.join(ROOT, 'map'))):
        f = os.path.join(ROOT, 'map', d, 'district.json')
        if d == 'd00':                 # the city layer: its roads drawn over every district, no outline of its own
            plan = os.path.join(ROOT, 'map', d, 'plan.json')
            city = json.load(open(plan))['records'] if os.path.exists(plan) else []
        elif d.startswith('d') and os.path.exists(f):
            D = next(r for r in json.load(open(f))['records'] if r['type'] == 'district')
            plan = os.path.join(ROOT, 'map', d, 'plan.json')
            drawn[D['n']] = (d, D, MultiPolygon([Polygon(o) for o in D['outline']]).buffer(0),
                             json.load(open(plan))['records'] if os.path.exists(plan) else [])
    held = unary_union([v[2] for v in drawn.values()])
    mine = unary_union([polys(x['rings']) for x in F['districts'] if x['n'] in drawn])
    gap = mine.difference(held)
    gap = unary_union([g for g in getattr(gap, 'geoms', [gap]) if g.area > 500])

    def draw(ax, detail):
        for x in F['districts']:
            g = polys(x['rings'])
            fill(ax, g, fc='#ffffff' if x['n'] in drawn else '#f1ece2', ec='#b9ad97', lw=0.6)
        fill(ax, gap, fc='#e05a4a', ec='none', alpha=0.45)
        for r in city:
            if r['type'] == 'road':
                fill(ax, LineString([q[:2] for q in r['centreline']]).buffer(r['width'] / 2, cap_style=2),
                     fc='#6f6f6f' if r['kind'] in ('motorway', 'trunk') else '#9a9a9a', ec='none')
        for n, (d, D, ring, recs) in drawn.items():
            fill(ax, ring, fc='none', ec='#a0301e', lw=0.8)
            for r in recs:
                if r['type'] == 'building':
                    xs, ys = zip(*[q[:2] for q in r['footprint']])
                    ax.fill(xs, ys, fc='#c98b5a', ec='none')
                elif r['type'] == 'road' and detail:
                    fill(ax, LineString([q[:2] for q in r['centreline']]).buffer(r['width'] / 2, cap_style=2),
                         fc='#6f6f6f' if r['kind'] in ('motorway', 'trunk') else '#9a9a9a', ec='none')
                elif r['type'] == 'road':
                    xs, ys = zip(*[q[:2] for q in r['centreline']])
                    ax.plot(xs, ys, c='#777', lw=0.15)
            cx, cy = ring.representative_point().coords[0]
            ax.text(cx, cy, D.get('name') or d, fontsize=11 if detail else 7, ha='center', va='center',
                    color='#a0301e', weight='bold')
        for x in F['districts']:
            if x['n'] not in drawn and not detail:
                cx, cy = polys(x['rings']).representative_point().coords[0]
                ax.text(cx, cy, str(x['n']), fontsize=6, ha='center', va='center', color='#5a4e3c')
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')

    names = ', '.join(v[1].get('name') or v[0] for v in drawn.values())
    fig, ax = plt.subplots(figsize=(14, 8), dpi=170)
    draw(ax, False)
    ax.set_title(f'Gidi: the 51 districts (frame study); drawn: {names}; red: land no drawn district holds '
                 f'({gap.area / 1e6:.3f} km2)', fontsize=9)
    fig.savefig(os.path.join(out, 'gidi_city.png'), bbox_inches='tight')
    plt.close(fig)
    if near:
        z = next(v[2] for v in drawn.values() if v[0] == near)
        around = unary_union([v[2] for v in drawn.values() if v[2].distance(z) < 50])
        x0, y0, x1, y1 = around.buffer(150).bounds
        fig, ax = plt.subplots(figsize=(12, 10), dpi=200)
        draw(ax, True)
        ax.set_xlim(x0, x1)
        ax.set_ylim(y1, y0)
        ax.set_title(f'{drawn[next(n for n, v in drawn.items() if v[0] == near)][1].get("name")} and its drawn '
                     'neighbours: roads at real width, houses', fontsize=10)
        fig.savefig(os.path.join(out, 'gidi_near.png'), bbox_inches='tight')
        plt.close(fig)
    print('gap km2', round(gap.area / 1e6, 4), [[round(v) for v in g.bounds] for g in getattr(gap, 'geoms', [gap]) if not g.is_empty])


if __name__ == '__main__':
    main()
