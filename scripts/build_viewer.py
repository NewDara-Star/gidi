# Assemble the one-file Gidi Maps page (2D + 3D) from the baked data: web/gidi-maps.html.
# Run after scripts/bake_web.py. Then publish web/gidi-maps.html to the live artifact (see docs/DISTRICT-BRIEF.md).
import os
W = os.path.join(os.path.dirname(__file__), "..", "web")
rd = lambda f: open(os.path.join(W, f), encoding="utf-8").read()
page = rd("shell.html") + "\n<script>" + rd("gidi-data.js") + "</script>\n<script>" + rd("view3d.js") + "</script>\n<script>" + rd("app.js") + "</script>\n"
for bad in ("fabric-", "rail_from_real", "real_centre"):
    assert bad not in page, "lifted real data must never be published: " + bad
open(os.path.join(W, "gidi-maps.html"), "w", encoding="utf-8").write(page)
print("web/gidi-maps.html", len(page) // 1024, "KB")
