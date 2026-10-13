"""Independent checker for a generated district.  Usage: python3 scripts/check_district.py <id>
Prints a PASS/FAIL line per check; exits 1 if any fails.  Import and call run(did) for raw results."""
import glob, json, math, os, sys
import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import polygonize, unary_union
from shapely.strtree import STRtree

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web")
HALF = {"street": 2.75, "lane": 1.1, "main": 5.0, "art": 11.0, "exp": 13.0, "canal": 2.0, "rail": 3.0}


def load(name):
    with open(os.path.join(ROOT, name)) as f:
        return json.load(f)


def load_city():
    s = open(os.path.join(ROOT, "gidi-data.js")).read()
    return json.loads(s[len("window.GIDI="):-1])


def line(pts):
    return LineString(pts) if pts and len(pts) >= 2 else None


def poly(ring):
    p = Polygon(ring)
    return p if p.is_valid else p.buffer(0)


def xy(g):  # short coordinate text
    c = g.representative_point()
    return "(%.0f,%.0f)" % (c.x, c.y)


def worst(items, n=3):  # items: (size, text); biggest first
    return "; ".join(t for _, t in sorted(items, key=lambda i: -i[0])[:n])


def ring_of(G, did):
    d = next(d for d in G["districts"] if d["id"] == did)
    r = d["poly"]
    return poly(r[0] if isinstance(r[0][0], (list, tuple)) else r)


def lagoon(G):
    w = G["water"][0]
    return poly(w if isinstance(w[0], (list, tuple)) else w["pts"])


def edge_mains(gen):
    return [m for m in gen["mains"] if "edge_with" in m]


def check_roads(gen, bgeoms, G):
    """1: no house on a carriageway, ramp, or under a deck (except stalls/kiosks)."""
    shapes = []  # (carriageway polygon, label, building kinds allowed there)
    def add(pts, half, label, ok=None):
        ln = line(pts)
        if ln is not None:
            shapes.append((ln.buffer(half), label, ok))
    for p in gen.get("streets", []):
        add(p, HALF["street"], "street")
    for p in gen.get("lanes", []):
        add(p, HALF["lane"], "lane")
    for m in gen["mains"]:
        add(m["pts"], HALF["main"], "main " + m.get("name", ""))
    for a in G["arterials"]:
        if a["cls"] in ("art", "exp"):
            add(a["pts"], HALF[a["cls"]], "arterial " + a["name"])
    add(G["rail"]["pts"], HALF["rail"], "rail")
    if gen.get("canal"):
        add(gen["canal"], HALF["canal"], "canal")
    for s in gen.get("structures", []):
        w = s.get("width")
        if s["kind"] == "ramp":
            add(s["pts"], (w or 8) / 2, "ramp " + s.get("name", ""))
        elif s["kind"] in ("flyover", "skywalk", "footbridge") and s.get("layer", 0) >= 1:
            add(s["pts"], (w / 2) if w else (6 if s["kind"] == "flyover" else 2),
                s["kind"] + " " + s.get("name", ""), {"stalls", "kiosk"})
    tree = STRtree([g for g, _, _ in shapes])
    bad = []
    for i, b in enumerate(bgeoms):
        for j in tree.query(b, predicate="intersects"):
            g, lab, ok = shapes[j]
            if ok and gen["buildings"][i][0] in ok:
                continue
            a = b.intersection(g).area
            if a > 0:
                bad.append((a, "%s %s on %s (%.1f m2)" % (gen["buildings"][i][0], xy(b), lab, a)))
    return len(bad), worst(bad)


def check_overlaps(bgeoms):
    """2: pairs of buildings overlapping by more than 0.05 m2."""
    tree = STRtree(bgeoms)
    a, b = tree.query(bgeoms, predicate="intersects")
    bad = []
    for i, j in zip(a, b):
        if i < j:
            ar = bgeoms[i].intersection(bgeoms[j]).area
            if ar > 0.05:
                bad.append((ar, "%s %.1f m2" % (xy(bgeoms[i]), ar)))
    return len(bad), worst(bad)


def land_of(gen, G):
    edges = unary_union([line(m["pts"]) for m in edge_mains(gen)])
    polys = list(polygonize(edges))
    if not polys:
        return None
    return max(polys, key=lambda p: p.area).buffer(1).difference(lagoon(G))


WATER_KINDS = ("stilt", "stilt bar", "raft")   # built over the lagoon on purpose (Water Town)


def check_land(bgeoms, land, kinds=None, G=None):
    """3: every building inside the land (edge-road polygon + 1 m, minus lagoon); stilt houses, the stilt bar and log rafts
    must instead stand over the lagoon, within 400 m of the district's land."""
    if land is None:
        return None, "edge roads do not form a closed polygon"
    bad = []
    lag = lagoon(G) if G is not None else None
    for i, b in enumerate(bgeoms):
        if kinds and kinds[i] in WATER_KINDS:
            if lag is None or not lag.buffer(0.5).contains(b) or b.distance(land) > 400:
                bad.append((b.area, "%s %s not over the lagoon next to the district" % (kinds[i], xy(b))))
            continue
        out = b.difference(land).area
        if out > 0.01:
            bad.append((out, "%s %.1f m2 outside" % (xy(b), out)))
    return len(bad), worst(bad)


def same(p, q, tol=0.05):
    return len(p) == len(q) and all(abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol for a, b in zip(p, q))


def check_edges(did, gen, net):
    """4: edge roads equal network.json edges, both ways."""
    mine = {k: e for k, e in net["edges"].items() if did in e["between"]}
    probs = []
    for m in edge_mains(gen):
        nb = m["edge_with"]
        cands = [e for e in mine.values() if nb is None or nb in e["between"]]
        if not any(same(m["pts"], e["pts"]) or same(m["pts"], e["pts"][::-1]) for e in cands):
            probs.append("gen road '%s' (%s) has no identical network edge" % (m.get("name"), nb))
    for k, e in mine.items():
        if not any(same(m["pts"], e["pts"]) or same(m["pts"], e["pts"][::-1]) for m in edge_mains(gen)):
            probs.append("network edge %s missing from gen mains" % k)
    return len(probs), "; ".join(probs)


def check_neighbours(did, gen, G):
    """5: (a) own streets stay in own ring (+2 m); (b) other districts' streets stay out (-2 m).
    The ring is the loop of the district's own edge roads (its real outline: the edge roads bend up to ~16 m off the drawn polygon)."""
    loops = list(polygonize(unary_union([line(m["pts"]) for m in edge_mains(gen)])))
    ring = max(loops, key=lambda p: p.area) if loops else ring_of(G, did)
    own = [line(p) for k in ("streets", "lanes") for p in gen.get(k, [])]
    out_a = [(l.difference(ring.buffer(2)).length, xy(l.difference(ring.buffer(2))))
             for l in own if l is not None and l.difference(ring.buffer(2)).length > 0]
    inner = ring.buffer(-2)
    out_b = []
    for f in glob.glob(os.path.join(ROOT, "gen-*.json")):
        oid = os.path.basename(f)[4:-5]
        if oid == did:
            continue
        o = json.load(open(f))
        for k in ("streets", "lanes"):
            for p in o.get(k, []):
                l = line(p)
                if l is not None and l.intersection(inner).length > 0:
                    out_b.append((l.intersection(inner).length, "%s %s" % (oid, xy(l.intersection(inner)))))
    n = len(out_a) + len(out_b)
    d = "own leaving ring: %d pieces, %.0f m (%s); other districts inside: %d pieces, %.0f m (%s)" % (
        len(out_a), sum(a for a, _ in out_a), worst(out_a, 2), len(out_b), sum(a for a, _ in out_b), worst(out_b, 2))
    return n, d


def check_incoming(did, gen, net, G):
    """6: every gateway coming into this district is continued by a street/main (or arterial/rail passes by)."""
    ends = []
    for l in list(gen["streets"]) + [m["pts"] for m in gen["mains"]]:
        ends += [Point(p) for p in l]
    ends = STRtree(ends)
    through = [line(a["pts"]) for a in G["arterials"] if a["cls"] != "bridge"] + [line(G["rail"]["pts"])]
    miss, tot = [], 0
    for g in net["gateways"]:
        if g["to"] != did:
            continue
        tot += 1
        p = Point(g["pt"])
        if g["kind"] in ("street", "main"):
            ok = len(ends.query(p.buffer(1.5), predicate="intersects")) > 0
        else:
            ok = any(l is not None and l.distance(p) <= 5 for l in through)
        if not ok:
            miss.append("%s '%s' from %s at (%.0f,%.0f)" % (g["kind"], g["road"], g["from"], *g["pt"]))
    return len(miss), "%d incoming gateways; missing: %s" % (tot, "; ".join(miss) or "none")


def check_outgoing(did, gen, net):
    """7: gateways leaving this district sit on an edge road toward the right neighbour."""
    em = [(line(m["pts"]), m["edge_with"]) for m in edge_mains(gen)]
    bad, tot = [], 0
    for g in net["gateways"]:
        if g["from"] != did:
            continue
        tot += 1
        p = Point(g["pt"])
        near = [nb for l, nb in em if l.distance(p) <= 1.5]
        if not near or (g["to"] not in near and None not in near):
            bad.append("%s '%s'->%s at (%.0f,%.0f)%s" % (g["kind"], g["road"], g["to"], *g["pt"],
                       "" if near else " not on an edge road"))
    return len(bad), "%d outgoing gateways; bad: %s" % (tot, "; ".join(bad) or "none")


def check_storeys(gen, bgeoms):
    """8: storeys list is valid; print band shares."""
    st = gen.get("storeys")
    if st is None:
        return None, "no storeys in file (skipped)"
    if len(st) != len(bgeoms) or any(not isinstance(s, int) or isinstance(s, bool) or s < 1 for s in st):
        return 1, "length %d vs %d buildings, or non-int / <1 values" % (len(st), len(bgeoms))
    bands = [("1", 1, 1), ("2", 2, 2), ("3", 3, 3), ("4", 4, 4), ("5-6", 5, 6), ("7-13", 7, 13), ("14+", 14, 999)]
    area = np.array([b.area for b in bgeoms]); s = np.array(st)
    txt = []
    for n, lo, hi in bands:
        m = (s >= lo) & (s <= hi)
        txt.append("%s: %.0f%% n / %.0f%% area" % (n, 100 * m.mean(), 100 * area[m].sum() / area.sum()))
    return 0, " | ".join(txt)


def ways_of(gen, G):
    """Every way a person can walk or drive on: (kind, line). Paths and footbridges included."""
    w = [("street", line(p)) for p in gen.get("streets", [])] + [("lane", line(p)) for p in gen.get("lanes", [])] \
        + [("path", line(p["pts"] if isinstance(p, dict) else p)) for p in gen.get("paths", [])] \
        + [("main", line(m["pts"])) for m in gen["mains"]] \
        + [(s["kind"], line(s["pts"])) for s in gen.get("structures", []) if s["kind"] in ("footbridge", "skywalk")] \
        + [("arterial", line(a["pts"])) for a in G["arterials"] if a["cls"] in ("art", "exp")]
    return [(k, l) for k, l in w if l is not None]


def check_connected(gen, G, tol=1.0):
    """9: every lane, path and footbridge joins the road network (lines within 1 m count as joined);
    a footbridge must land on a way at both ends."""
    W = ways_of(gen, G)
    geoms = [l for _, l in W]
    tree = STRtree(geoms)
    parent = list(range(len(W)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i, g in enumerate(geoms):
        for j in tree.query(g.buffer(tol)):
            if j != i and g.distance(geoms[j]) <= tol:
                parent[find(i)] = find(int(j))
    roots = {find(i) for i, (k, _) in enumerate(W) if k in ("main", "arterial")}
    bad = []
    for i, (k, g) in enumerate(W):
        if k in ("lane", "path", "footbridge", "street") and find(i) not in roots:
            bad.append((g.length, "%s %s floats (%.0f m)" % (k, xy(g), g.length)))
        if k == "footbridge":
            for e in (Point(g.coords[0]), Point(g.coords[-1])):
                if not any(j != i and geoms[j].distance(e) <= tol for j in tree.query(e.buffer(tol))):
                    bad.append((g.length, "footbridge end (%.0f,%.0f) lands on nothing" % (e.x, e.y)))
    return len(bad), worst(bad, 5)


def check_reach(gen, G, bgeoms, limit=45.0):
    """10: every building is within 45 m of a street, lane, path or road (someone has to walk to its door).
    Buildings inside a parcel (yard, market, school) count from the parcel, which must be within 10 m of a way."""
    W = [l for _, l in ways_of(gen, G)]
    tree = STRtree(W)
    parcels = [poly(p["pts"]) for p in gen.get("parcels", [])]
    bad = []
    for i, b in enumerate(bgeoms):
        home = next((p for p in parcels if p.buffer(0.5).contains(b)), None)
        if home is not None:   # a yard, market or school ground is open: measure from its fence, which must touch a way
            if min(l.distance(home) for l in W) > 10:
                bad.append((99, "%s %s: its parcel touches no way" % (gen["buildings"][i][0], xy(b))))
            continue
        j = tree.query_nearest(b, max_distance=limit)
        if len(np.atleast_1d(j)) == 0:
            d = min(W[int(k)].distance(b) for k in np.atleast_1d(tree.query_nearest(b)))
            bad.append((d, "%s %s %.0f m" % (gen["buildings"][i][0], xy(b), d)))
    return len(bad), worst(bad, 5)


def check_locked(did, gen, tol=0.15):
    """12: the locked opening (web/locked.json) is exactly where it was recorded: market, aisles, The steal, Tunde's room, the boss's park."""
    p = os.path.join(ROOT, "locked.json")
    L = json.load(open(p)).get(did) if os.path.exists(p) else None
    if not L:
        return None, "nothing locked in this district"
    def same_ring(a, b):   # same points, allowing the 0.1 m rounding of the generated file
        return len(a) == len(b) and all(abs(x[0] - y[0]) <= tol and abs(x[1] - y[1]) <= tol for x, y in zip(a, b))
    bad, ok = [], []
    for name, e in L.get("reserve", {}).items():
        hit = any(same_ring(q["pts"], e["rect"]) for q in gen["parcels"])
        (ok if hit else bad).append("%s plot" % name)
    for name, lines_ in L.get("aisles", {}).items():
        have = [q["pts"] for q in gen.get("paths", []) if q["kind"] == "market aisle"]
        for ln in lines_:
            hit = any(same_ring(h, ln) for h in have)
            (ok if hit else bad).append("%s aisle" % name)
    for name, e in L.get("buildings", {}).items():
        hit = any(b[0] == e["kind"] and same_ring(b[1:], e["poly"][:-1]) for b in gen["buildings"])
        pos = gen["poi_pos"].get(name)
        hit = hit and pos is not None and math.dist(pos, e["pt"]) <= 1
        (ok if hit else bad).append(name)
    for name, e in L.get("parcels", {}).items():
        hit = any(same_ring(q["pts"], e["poly"]) for q in gen["parcels"])
        pos = gen["poi_pos"].get(name)
        hit = hit and pos is not None and math.dist(pos, e["pt"]) <= 1
        (ok if hit else bad).append(name)
    return len(bad), "moved: %s; in place: %s" % (", ".join(bad) or "none", ", ".join(ok))


def check_everyday(did, G, limit=833, hard=1250):
    """13: every house has a school, a place of worship and a chemist or clinic within 10 min walk (15 at most), on the
    baked city (run bake_web.py first), on the same walking network as the living test."""
    import sys as _s; _s.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import walknet
    built = sorted(G.get("buildings", {}))
    if did not in built: return None, "not baked yet"
    R = walknet.Reach(walknet.graph(walknet.ways_of(G, built), "walk"))
    houses = [Polygon(b[1:]).centroid for b in G["buildings"][did] if b[0] in ("front", "back", "stilt")]
    bad, txt = 0, []
    for cat, types in (("school", {"school"}), ("worship", {"church", "mosque"}), ("chemist", {"chemist", "clinic", "hospital"})):
        d = R.from_points([Point(p["x"], p["y"]) for p in G["pois"] if p["type"] in types], hard + 1)
        t = [R.to_point(d, h) for h in houses]
        over10 = sum(1 for x in t if x > limit); over15 = sum(1 for x in t if x > hard); bad += over15
        txt.append("%s: %d over 10 min, %d over 15, worst %.1f min" % (cat, over10, over15, max(t) / 83.33))
    return bad, "; ".join(txt)


def run(did):
    gen, net, G = load("gen-%s.json" % did), load("network.json"), load_city()
    bg = [poly([p for p in b[1:]]) for b in gen["buildings"]]
    land = land_of(gen, G)
    res = []
    def add(name, r):
        n, d = r
        res.append((name, None if n is None else n == 0, "%s%s" % ("" if n is None else "%d found. " % n, d)))
    add("1 houses on roads/ramps/decks", check_roads(gen, bg, G))
    add("2 building overlaps", check_overlaps(bg))
    add("3 buildings on land", check_land(bg, land, [b[0] for b in gen["buildings"]], G))
    add("4 edge roads match network", check_edges(did, gen, net))
    add("5 neighbour streets", check_neighbours(did, gen, G))
    add("6 incoming gateways continued", check_incoming(did, gen, net, G))
    add("7 outgoing gateways on edges", check_outgoing(did, gen, net))
    add("8 storeys", check_storeys(gen, bg))
    add("9 lanes, paths, footbridges joined", check_connected(gen, G))
    add("10 buildings within 45 m of a way", check_reach(gen, G, bg))
    add("12 opening locked", check_locked(did, gen))
    add("13 everyday places in reach", check_everyday(did, G))
    kinds = {}
    for p in gen.get("parcels", []):
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    res.append(("11 parcels (report only)", True, ", ".join("%s: %d" % kv for kv in sorted(kinds.items())) or "none"))
    return res


if __name__ == "__main__":
    did = sys.argv[1]
    results = run(did)
    for name, ok, detail in results:
        print("%-5s %-34s %s" % ("SKIP" if ok is None else ("PASS" if ok else "FAIL"), name, detail))
    sys.exit(1 if any(ok is False for _, ok, _ in results) else 0)
