# The terrain review map: colour relief with hillshade, land 0-3 m (flood-prone) marked, contours every 2 m, district outlines.
# Usage: python3 scripts/draw_terrain.py [out.png]  (after scripts/terrain.py)
import json, sys
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, ListedColormap
T = json.load(open("web/terrain.json")); Z = np.array(T["z"], float).reshape(T["h"], T["w"]) / 10; C = T["cell_m"]
G = json.loads(open("web/gidi-data.js").read()[len("window.GIDI="):-1])
sea = Z <= 0.0
fig, ax = plt.subplots(figsize=(16, 12.5)); ext = (0, T["w"] * C, T["h"] * C, 0)
ls = LightSource(azdeg=315, altdeg=40)
land = np.ma.masked_where(sea, Z)
cmap = plt.get_cmap("terrain"); cmap = ListedColormap(cmap(np.linspace(0.25, 1.0, 256)))
rgb = ls.shade(np.where(sea, 0, Z), cmap=cmap, vmin=0, vmax=max(40, float(Z.max())), vert_exag=8, blend_mode="soft")
rgb[sea] = (0.62, 0.79, 0.93, 1)
ax.imshow(rgb, extent=ext)
low = np.ma.masked_where(sea | (Z >= 3), np.ones_like(Z)); ax.imshow(low, extent=ext, cmap=ListedColormap([(0.85, 0.2, 0.6)]), alpha=0.35)
cs = ax.contour(np.arange(T["w"]) * C + C / 2, np.arange(T["h"]) * C + C / 2, np.where(sea, np.nan, Z), levels=np.arange(2, 70, 2), colors="k", linewidths=0.3, alpha=0.5)
ax.clabel(cs, cs.levels[::5], fontsize=7, fmt="%d m")
for d in G["districts"]:
    p = np.array(d["poly"][0]); ax.plot(p[:, 0], p[:, 1], "-", color="#222", lw=1.2)
    ax.text(p[:, 0].mean(), p[:, 1].mean(), d["name"], ha="center", va="center", fontsize=10, weight="bold", color="#111",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, max(40, float(Z.max())))); cb = fig.colorbar(sm, ax=ax, shrink=0.6); cb.set_label("ground height, m")
ax.set_title("Gidi terrain (pink wash: land below 3 m, flood-prone; contours every 2 m)"); ax.set_xlim(0, T["w"] * C); ax.set_ylim(T["h"] * C, 0); ax.set_aspect("equal")
plt.savefig(sys.argv[1] if len(sys.argv) > 1 else "docs/img/terrain.png", dpi=80, bbox_inches="tight")
