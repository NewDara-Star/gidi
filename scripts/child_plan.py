"""A district's child plan (owner, 19 Oct 2026: a district is the child of its real inspirations): draws docs/hand/<dir>/child_plan.json
over the district's outline, the arterials and the rail, each area labelled with the real place it comes from, and writes the real
box each area covers, so every Gidi point has a real twin to photograph.
Usage: python3 scripts/child_plan.py ibudo [layout.json]   (writes docs/hand/<dir>/child_plan.png and child_plan.md)
"""
import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

D = sys.argv[1]
P = json.load(open(f'docs/hand/{D}/child_plan.json'))
L = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'web/layout-v2.json'))
OUT = Polygon(L['districts'][P['district']])
M_LAT, M_LON = 110600.0, 109900.0   # metres per degree near 6.5 N


def to_real(a, x, y):
    (la, lo), (gx, gy) = a['anchor_real'], a['anchor_gidi']
    return la - (y - gy) / M_LAT, lo + (x - gx) / M_LON


COL = ['#e8a26a', '#d9c36a', '#9fc3e8', '#c9a46b', '#e0c0a0', '#a8c99a', '#b6d9a0', '#b9c2d0', '#ef8f7a', '#e6dd9a', '#d8c8e8', '#c8e0d8']
f, ax = plt.subplots(figsize=(17, 13))
xs, ys = OUT.exterior.xy
ax.fill(xs, ys, color='#f3eee6', zorder=0); ax.plot(xs, ys, 'k-', lw=2, zorder=6)
rows = ['| Gidi area | Real place | Real box (lat, lon) | Real streets in it |', '|---|---|---|---|']
for i, a in enumerate(P['areas']):
    g = Polygon(a['pts']).intersection(OUT)
    for part in getattr(g, 'geoms', [g]):
        px, py = part.exterior.xy
        ax.fill(px, py, color=COL[i % len(COL)], alpha=.75, zorder=1); ax.plot(px, py, color='#555', lw=.8, zorder=2)
    c = g.representative_point()
    ax.text(c.x, c.y - 30, a['name'], ha='center', fontsize=11, weight='bold', zorder=9)
    ax.text(c.x, c.y + 5, '← ' + a['real'].split(':')[0], ha='center', va='top', fontsize=7.5, zorder=9, wrap=True)
    x0, y0, x1, y1 = g.bounds
    n, w = to_real(a, x0, y0); s, e = to_real(a, x1, y1)
    rows.append(f"| {a['name']} | {a['real']} | {s:.4f} to {n:.4f}, {w:.4f} to {e:.4f} | {', '.join(a['streets'])} |")
NAMES = {r['gidi'].split(' (')[0]: r['real'] for r in P['roads']}
for art in L['arterials']:
    pts = art['pts']; xs, ys = zip(*pts)
    ax.plot(xs, ys, color='#b02020', lw=5, alpha=.75, zorder=4)
xs, ys = zip(*L['rail']['pts']); ax.plot(xs, ys, color='k', lw=3, zorder=5); ax.plot(xs, ys, color='w', lw=1.2, ls=(0, (4, 4)), zorder=5)
LBL = [((8675, 3800), 'Ring Road = Agege Motor Rd (A5)', 80), ((8760, 3790), 'rail', 70), ((8700, 4300), 'Ayinde Ave = Apapa-Oworonshoki Expy', 72),
       ((7000, 4495), 'west road = Airport Rd', -3), ((7400, 5120), 'cross road = Itire Rd / Ojuelegba Rd', 0), ((8115, 4800), 'N-S road = Church St / Osolo Way', 86),
       ((8930, 5230), 'Ring Road = Ikorodu Rd', 63)]
for (x, y), t, rot in LBL:
    ax.text(x, y, t, fontsize=8, color='#700', rotation=rot, zorder=10, bbox=dict(fc='w', ec='none', alpha=.7, pad=1))
ax.add_patch(plt.Rectangle((8455, 3963), 320, 188, fill=False, ec='b', lw=2, zorder=8)); ax.text(8460, 3958, 'spot 1 (Oshodi Rd at the market gate)', color='b', fontsize=8, zorder=10)
b = OUT.bounds
ax.set_xlim(b[0] - 60, b[2] + 60); ax.set_ylim(b[3] + 60, b[1] - 60); ax.set_aspect('equal')
ax.set_title(f"Ìbùdó plan v3: the child of Oshodi and Ojuelegba (each area a real place at true scale; every street's twin is the real street under it)", fontsize=12)
plt.savefig(f'docs/hand/{D}/child_plan.png', dpi=75, bbox_inches='tight')
open(f'docs/hand/{D}/child_plan.md', 'w').write('# ' + P['note'] + '\n\n## Areas\n\n' + '\n'.join(rows) + '\n\n## Main roads\n\n| Gidi | Real twin |\n|---|---|\n' +
                                                  '\n'.join(f"| {r['gidi']} | {r['real']} |" for r in P['roads']) + '\n')
print('\n'.join(rows))
