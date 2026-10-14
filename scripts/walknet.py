"""The walking and riding network of the built districts, shared by explore_city.py (the living test) and bake_web.py
(placing schools, places of worship and chemists by coverage), so both measure walks the same way.
G is the baked city (web/gidi-data.js) or the dict bake_web.py is building."""
import math
import networkx as nx, numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree
from fabric_metrics import noded, lines


def ways_of(G, dids, area=None):
    """Every way in the built districts: (kind, name, LineString). Mains and arterials are cut to `area` (the districts + 120 m)."""
    if area is None:
        area = unary_union([Polygon(d["poly"][0]) for d in G["districts"] if d["id"] in dids]).buffer(1).buffer(120)
    ways = []
    for did in dids:
        for l in G["streets"].get(did, []): ways.append(("street", "", LineString(l)))
        for l in G.get("lanes", {}).get(did, []): ways.append(("lane", "", LineString(l)))
        for l in G.get("paths", {}).get(did, []): ways.append(("path", "", LineString(l)))   # footpaths: rail side, canal banks, worn crossings
    for m in G["mains"]:
        for p in lines(LineString(m["pts"]).intersection(area)): ways.append(("main", m["name"], p))
    for a in G["arterials"]:
        for p in lines(LineString(a["pts"]).intersection(area)): ways.append(("arterial", a["name"], p))
    for st in G.get("structures", []):
        if st.get("d") in dids and st["kind"] in ("footbridge", "skywalk"): ways.append((st["kind"], st.get("name", st["kind"]), LineString(st["pts"])))
    return ways


def ban_zone(G):
    """The okada ban zones of the built districts (bake_web.py records them), as one shape, or None."""
    z = [Polygon(e["poly"]) for e in G.get("okada_ban", []) if e.get("built")]
    return unary_union(z) if z else None


def graph(ways, mode, ban=None, through=False):
    """walk: everything; ride: no lanes, footpaths, footbridges or skywalks.
    ban (ride only): the okada ban zone. Each edge records the metres it runs inside it ("inban"); unless `through`,
    edges that run inside it are left out, so the ride goes round."""
    keep = [(k, n, g) for k, n, g in ways if not (mode == "ride" and k in ("lane", "path", "footbridge", "skywalk"))]
    U = noded([g for k, n, g in keep]); Gx = nx.Graph()
    snap = {}   # junctions closer than 25 cm are one node (rounding alone splits a junction that falls on a rounding boundary)
    def key(c):
        cell = (int(c[0] // 0.5), int(c[1] // 0.5))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for q in snap.get((cell[0] + dx, cell[1] + dy), []):
                    if (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2 < 0.0625: return q
        q = (round(c[0], 2), round(c[1], 2)); snap.setdefault(cell, []).append(q); return q
    tr = STRtree([g for k, n, g in keep])
    for seg in lines(U):
        ka, kb = key(seg.coords[0]), key(seg.coords[-1])
        if ka == kb: continue   # a sliver shorter than the snap: its two ends are one junction (never drop a short link)
        m = seg.interpolate(0.5, normalized=True); i = int(np.atleast_1d(tr.query_nearest(m))[0]); k, n, _ = keep[i]
        inban = seg.intersection(ban).length if ban is not None and mode == "ride" and seg.intersects(ban) else 0.0
        if inban > 0.5 and not through: continue
        Gx.add_edge(ka, kb, w=seg.length, kind=k, name=n, geom=seg, inban=inban)
    # noding collinear streets can drop a sub-metre sliver between two pieces; a loose end within 1 m of another node joins it
    # (the same 1 m tolerance check_district.py uses)
    nodes = list(Gx.nodes); NT = STRtree([Point(q) for q in nodes])
    for q in [q for q, d in Gx.degree() if d == 1]:
        for j in NT.query(Point(q).buffer(1.0)):
            o = nodes[int(j)]
            if o != q and not Gx.has_edge(q, o) and math.dist(q, o) <= 1.0:
                Gx.add_edge(q, o, w=math.dist(q, o), kind=Gx[q][next(iter(Gx[q]))]["kind"], name="", geom=LineString([q, o]))
    return Gx


class Reach:
    """Walking distances on the main walking network. A point joins the network at the nearest point of its nearest way
    (the way is split there), the same way explore_city.py starts and ends a trip."""
    def __init__(self, Gx):
        self.G = Gx.subgraph(max(nx.connected_components(Gx), key=len)).copy()
        self.E = list(self.G.edges(data=True)); self.T = STRtree([e[2]["geom"] for e in self.E])
    def attach(self, p):
        """(node_a, dist_a, node_b, dist_b, off): the two ends of the nearest way, how far along it each is, and the step onto it."""
        u, v, e = self.E[int(np.atleast_1d(self.T.query_nearest(p))[0])]; g = e["geom"]; t = g.project(p)
        if Point(u).distance(Point(g.coords[0])) > Point(v).distance(Point(g.coords[0])): u, v = v, u
        return u, t, v, g.length - t, g.interpolate(t).distance(p)
    def from_points(self, pts, limit):
        """Shortest walk from the nearest of `pts` to every node, up to `limit` metres."""
        src = {}
        for p in pts:
            u, du, v, dv, off = self.attach(p)
            for n, d in ((u, du + off), (v, dv + off)): src[n] = min(src.get(n, 1e18), d)
        if not src: return {}
        S = "_src_"; H = self.G.copy()
        for n, d in src.items(): H.add_edge(S, n, w=d)
        dist = nx.single_source_dijkstra_path_length(H, S, cutoff=limit, weight="w"); dist.pop(S, None); return dist
    def to_point(self, dist, p):
        u, du, v, dv, off = self.attach(p)
        return min(dist.get(u, 1e18) + du, dist.get(v, 1e18) + dv) + off
