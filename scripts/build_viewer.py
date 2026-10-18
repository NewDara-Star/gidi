# Assemble the one-file Gidi Maps page (2D + 3D) from the baked data: web/gidi-maps.html.
# Run after scripts/bake_web.py. Then publish web/gidi-maps.html to the live artifact (see docs/DISTRICT-BRIEF.md).
import os
W = os.path.join(os.path.dirname(__file__), "..", "web")
rd = lambda f: open(os.path.join(W, f), encoding="utf-8").read()
def map_data():
    """The data for the map page: everything but the things and the life (scripts/things.py), which the board, the kit and
    Unreal read from gidi-data.js; the page has no use for 60,000 parked cars."""
    import json
    s = rd("gidi-data.js")
    G = json.loads(s[s.index("{"):s.rstrip().rstrip(";").rindex("}") + 1])
    for k in ("things", "life", "ground_paint"):
        G.pop(k, None)
    return "window.GIDI=" + json.dumps(G, separators=(",", ":"), ensure_ascii=False) + ";"


page = rd("shell.html") + "\n<script>" + map_data() + "</script>\n<script>" + rd("view3d.js") + "</script>\n<script>" + rd("app.js") + "</script>\n"
for bad in ("fabric-", "rail_from_real", "real_centre"):
    assert bad not in page, "lifted real data must never be published: " + bad
open(os.path.join(W, "gidi-maps.html"), "w", encoding="utf-8").write(page)
print("web/gidi-maps.html", len(page) // 1024, "KB")
