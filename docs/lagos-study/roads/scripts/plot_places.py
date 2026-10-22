# Pictures of the places: coloured pieces, border lines, names. Optional argument: a group label per place (districts).
import json, sys, pickle, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from common import *
Pz = np.load(WORK + 'places.npz'); place = Pz['place']; wide = Pz['wide']; land = Pz['land']
PL = json.load(open(WORK + 'places.json'))['places']; N = json.load(open(WORK + 'network.json'))
OB = np.load(WORK + 'ob50.npz'); roof = OB['a'] / C ** 2
S = pickle.load(open(WORK + 'skel.pkl', 'rb'))['segs']

def draw(path, box, group=None, title='', labels=None, fs=6, gnames=None):
    """box = (x0, x1, y0, y1) in real km. group: dict place id -> group id (colour by group, border lines between groups only)."""
    lab = place.copy()
    if group is not None:
        g = np.zeros(place.max() + 1, np.int32)
        for p, k in group.items(): g[p] = k + 1
        lab = np.where(place > 0, g[place], 0)
    j0, j1 = int((box[0] * 1000 - X0) // C), int((box[1] * 1000 - X0) // C); i0, i1 = int((box[2] * 1000 - Y0) // C), int((box[3] * 1000 - Y0) // C)
    j0, i0 = max(j0, 0), max(i0, 0); j1, i1 = min(j1, NX), min(i1, NY)
    L = lab[i0:i1, j0:j1]
    rng = np.random.default_rng(3); pal = rng.uniform(0.55, 0.95, (L.max() + 2, 3))
    img = pal[L]; img[L == 0] = (0.72, 0.84, 0.95) if True else 1
    img[~land[i0:i1, j0:j1] & ~wide[i0:i1, j0:j1]] = (0.97, 0.96, 0.93)
    b = np.clip(roof[i0:i1, j0:j1] * 2.5, 0, 1)[..., None]; img = img * (1 - 0.35 * b)
    ext = [(X0 + j0 * C) / 1000, (X0 + j1 * C) / 1000, (Y0 + i0 * C) / 1000, (Y0 + i1 * C) / 1000]
    w = (box[1] - box[0]); h = (box[3] - box[2]); fig, ax = plt.subplots(figsize=(min(24, 0.9 * w + 2) if w < 30 else 24, (min(24, 0.9 * w + 2) if w < 30 else 24) * h / w), dpi=110)
    ax.imshow(img, origin='lower', extent=ext, interpolation='nearest')
    segs = []
    for a, b2, ax_ in ((L[:, 1:], L[:, :-1], 1), (L[1:, :], L[:-1, :], 0)):
        ii, jj = np.nonzero((a != b2) & ((a > 0) | (b2 > 0)))
        for i, j in zip(ii, jj):
            if ax_ == 1:
                x = ext[0] + (j + 1) * C / 1000; segs.append([(x, ext[2] + i * C / 1000), (x, ext[2] + (i + 1) * C / 1000)])
            else:
                y = ext[2] + (i + 1) * C / 1000; segs.append([(ext[0] + j * C / 1000, y), (ext[0] + (j + 1) * C / 1000, y)])
    ax.add_collection(LineCollection(segs, colors='k', linewidths=0.5))
    for s in S:
        if s['cls'] in ('motorway', 'trunk', 'primary', 'rail') and not s['link']:
            ax.plot(s['xy'][:, 0] / 1000, s['xy'][:, 1] / 1000, color={'rail': '#6c3483'}.get(s['cls'], '#c0392b'), lw=0.5, alpha=0.6)
    if labels is not None:
        for x, y, t in labels:
            if box[0] < x < box[1] and box[2] < y < box[3]: ax.text(x, y, t, fontsize=fs, ha='center', va='center', zorder=6)
    ax.set_xlim(box[0], box[1]); ax.set_ylim(box[2], box[3]); ax.set_aspect('equal'); ax.set_title(title)
    fig.tight_layout(); fig.savefig(path); plt.close(fig)

def frame_box():
    fu, fv = N['fu'], N['fv']; return (fu / 1000, (fu + 81000) / 1000, fv / 1000, (fv + 31500) / 1000)
INNER = (527.0, 556.0, 708.0, 736.0)   # the inner metro: Island, Surulere, Yaba, Mushin, Oshodi, Ikeja, Gbagada, Ketu (UTM km)

if __name__ == '__main__':
    labs = [(q['x'] / 1000, q['y'] / 1000, q['name']) for q in PL if q['roof_km2'] >= 0.05]
    draw(OUT + 'places_inner.png', INNER, title='Places of the inner metro, cut by their real borders (real km). Lines: place borders; red: big roads; purple: rail', labels=labs, fs=5.5)
    big = [(q['x'] / 1000, q['y'] / 1000, q['name']) for q in PL if q['roof_km2'] >= 0.6]
    draw(OUT + 'places_frame.png', frame_box(), title='All places inside the Gidi frame (real km); names on places with over 0.6 km2 of roof', labels=big, fs=4.5)
