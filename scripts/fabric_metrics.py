# Same yardstick for real and generated fabric: streets [(cls, LineString)], buildings [Polygon], area Polygon (metres).
import math, numpy as np, networkx as nx
from collections import Counter
from shapely.geometry import Point
from shapely.ops import unary_union, polygonize
from shapely.strtree import STRtree
MAINC = {"motorway","trunk","primary","secondary","tertiary","main","art","exp","bridge"}
def pct(a, ps=(25, 50, 75)):
    a = np.asarray(a, float); return {f"p{p}": round(float(np.percentile(a, p)), 1) for p in ps} if len(a) else {}
def lines(g): return [p for p in getattr(g, "geoms", [g]) if p.geom_type == "LineString" and p.length > 0.5]
def extend(g, d=0.4):  # overshoot both ends slightly so T-junctions node even with floating-point gaps
    if g.length < 0.5: return g
    c = list(g.coords)
    def ext(p, q):  # q is a point ~2 m back along the line, so micro-segments don't skew the direction
        L = math.dist(p, q) or 1; return (p[0] + (p[0] - q[0]) / L * d, p[1] + (p[1] - q[1]) / L * d)
    b = min(2.0, g.length / 2)
    q0 = g.interpolate(b).coords[0]; q1 = g.interpolate(g.length - b).coords[0]
    return type(g)([ext(c[0], q0)] + c + [ext(c[-1], q1)])
def noded(gs, d=0.4):  # robust noding: overshoot ends, snap to a 5 cm grid, union
    import shapely
    return shapely.unary_union(shapely.set_precision(shapely.GeometryCollection([extend(g, d) for g in gs]), 0.05))
def measure(streets, buildings, area, edge_tol=30):
    A = area.area / 1e6
    st = [(c, p) for c, g in streets for p in lines(g.intersection(area.buffer(1)))]
    import shapely; noded = shapely.unary_union(shapely.set_precision(shapely.GeometryCollection([extend(g) for c, g in st]), 0.05)); segs = lines(noded)
    G = nx.MultiGraph(); k = lambda c: (round(c[0], 2), round(c[1], 2))
    for s in segs: G.add_edge(k(s.coords[0]), k(s.coords[-1]), L=s.length)
    for _ in range(2):  # drop the tiny overshoot stubs
        G.remove_edges_from([(u, v, kk) for u, v, kk, d in G.edges(keys=True, data=True) if d["L"] < 1.0 and (G.degree(u) == 1 or G.degree(v) == 1)])
        G.remove_nodes_from([n for n, d in G.degree() if d == 0])
    inner = area.buffer(-edge_tol); dg = Counter(d for n, d in G.degree() if inner.contains(Point(n)))
    J = sum(v for kk, v in dg.items() if kk >= 3)
    polys = [p for p in polygonize(noded) if p.area > 150 and inner.contains(p.representative_point())]
    r = {"drive_km_per_km2": round(sum(g.length for c, g in st) / 1000 / A, 1),
         "main_km_per_km2": round(sum(g.length for c, g in st if c in MAINC) / 1000 / A, 2),
         "junctions_per_km2": round(J / A), "T_share": round(dg[3] / max(1, J), 2), "dead_end_ratio": round(dg[1] / max(1, J), 2),
         "block_m2": pct([p.area for p in polys]), "blocks_per_km2": round(len(polys) / A)}
    if buildings:
        bA = np.array([b.area for b in buildings])
        r.update({"buildings_per_km2": round(len(buildings) / A), "coverage": round(sum(b.intersection(area).area for b in buildings) / area.area, 3),
                  "footprint_m2": pct(bA, (10, 25, 50, 75, 90)), "share_under_60m2": round(float(np.mean(bA < 60)), 2), "share_over_400m2": round(float(np.mean(bA >= 400)), 2)})
        tr = STRtree([g for c, g in st]); gl = [g for c, g in st]
        sb = [b.distance(gl[int(np.atleast_1d(tr.query_nearest(b.centroid))[0])]) for b in buildings]
        r["edge_to_street_m"] = pct(sb, (10, 25, 50, 75, 90)); r["front_row_share"] = round(float(np.mean(np.array(sb) < 12)), 2)
        bt = STRtree(buildings); gaps = []
        for b in buildings[::5]:
            nb = [buildings[i] for i in bt.query(b.buffer(15)) if buildings[i] is not b]
            if nb: gaps.append(min(b.distance(o) for o in nb))
        r["gap_m"] = pct(gaps); r["overlaps_with_streets"] = int(sum(1 for d in sb if d < 0.5))
    return r
