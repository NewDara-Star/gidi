#!/usr/bin/env python3
"""Explore the generated Gidi districts on foot or by okada. Data: web/gidi-data.js (the baked city; run scripts/bake_web.py first).
Run from the repo root: python3 scripts/explore_city.py COMMAND ...
Usage:
  explore_city.py overview                      what's here: size, counts, landmarks, parcels
  explore_city.py home [n] [district]           pick the n-th resident house (default random), optionally in one district, and describe it
  explore_city.py look X Y [radius]             what you see standing at X,Y (metres)
  explore_city.py walk FROM TO                  walk on foot (5 km/h). FROM/TO = landmark name (part ok) or X,Y
  explore_city.py ride FROM TO [--through]      okada ride (25 km/h, no lanes, arterials allowed); goes round okada ban zones unless --through
  explore_city.py places                        list landmarks and civic places with coordinates
  explore_city.py problems                      houses far from any street, dead-end counts, tiny blocks
Explores every district that has generated buildings; set DISTRICTS=maze,hub to limit it.
Distances run along road centre lines; no traffic or crowds. Landmark pins in the middle of big plots
(markets, yards) show some metres "off-network": that is the plot, not a missing street."""
import json, sys, os, math, random
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import networkx as nx, numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.strtree import STRtree
from fabric_metrics import noded, lines
DIDS = None
s = open(os.path.join(ROOT, "web", "gidi-data.js")).read(); G = json.loads(s[len("window.GIDI="):-1])
from shapely.ops import unary_union
DIDS = os.environ.get("DISTRICTS", "").split(",") if os.environ.get("DISTRICTS") else sorted(G.get("buildings", {}).keys())
DS = {d["id"]: d for d in G["districts"] if d["id"] in DIDS}; DP = {k: Polygon(v["poly"][0]) for k, v in DS.items()}
POLY = unary_union(list(DP.values())).buffer(1); AREA = POLY.buffer(120)
# a district's stilt village, stilt bar and rafts stand over the lagoon, outside its land outline, but they are still that district
WATER = {k: unary_union([Polygon(b[1:]) for b in G["buildings"][k] if b[0] in ("stilt", "stilt bar", "raft")]).buffer(25) for k in DP}
def where(pt):
    for k, p in DP.items():
        if p.buffer(2).contains(pt) or WATER[k].contains(pt): return DS[k]["name"]
    for k, p in DP.items():   # edge roads are gently bent, up to 16 m off the outline: still that district's road
        if p.buffer(20).contains(pt): return DS[k]["name"]
    return "outside the built districts"
B = [(b[0], Polygon(b[1:]), st) for DID in DIDS for b, st in zip(G["buildings"][DID], G["storeys"][DID])]
BD = [DID for DID in DIDS for b in G["buildings"][DID]]   # each building's district
BS = [st for DID in DIDS for st in (G.get("styles", {}).get(DID) or [None] * len(G["buildings"][DID]))]   # each house's style (the Heights)
BT = STRtree([p for k, p, st in B])
import walknet
ways = walknet.ways_of(G, DIDS, AREA)   # (kind, name, LineString)
RAIL = LineString(G["rail"]["pts"]); CANALS = [LineString(c["pts"]) for c in G.get("canals", []) if c["d"] in DIDS]
POIS = [p for p in G["pois"] if p["d"] in DIDS]
PARCELS = [(p["kind"], Polygon(p["pts"])) for DID in DIDS for p in G.get("parcels", {}).get(DID, [])]
FLY = [(st["name"], LineString(st["pts"])) for st in G.get("structures", []) if st.get("d") in DIDS and st["kind"] == "flyover"]
WT = STRtree([g for k, n, g in ways])

BAN = walknet.ban_zone(G)   # okada ban zones (the Capital): rides go round them unless --through
def graph(mode, through=False): return walknet.graph(ways, mode, BAN, through)
def nearest_way(pt):
    i = int(np.atleast_1d(WT.query_nearest(pt))[0]); k, n, g = ways[i]; return k, n, g, g.distance(pt)
def label(k, n): return f"{n} ({k})" if n else f"unnamed {k}"
def resolve(arg, near=None):
    """X,Y or part of a place name. Many names repeat across districts (a Fresh Life Pharmacy in the Maze and in the Hub):
    of several matches, the one nearest `near` (the other end of the trip) is taken."""
    if "," in arg and arg.replace(",", "").replace(".", "").replace("-", "").isdigit():
        x, y = map(float, arg.split(",")); return Point(x, y), f"{x:.0f},{y:.0f}"
    hits = [p for p in POIS if arg.lower() in p["name"].lower()]
    if not hits: sys.exit(f"no place matching '{arg}'. Try: places")
    if near is None: hits = [p for p in hits if p["name"].lower() == arg.lower()] or hits   # alone: an exact name first
    p = min(hits, key=lambda p: near.distance(Point(p["x"], p["y"]))) if near is not None else hits[0]
    return Point(p["x"], p["y"]), p["name"] + (f" ({p['x']},{p['y']})" if len(hits) > 1 else "")
def bkind(k, st): return {"front": "house on the street", "back": "back house in a compound", "shed": "shed", "kiosk": "kiosk", "stalls": "market stall", "canopy": "levy canopy", "phone mall": "phone mall", "strip": "bar or small hotel on the strip", "hall": "music hall", "office": "government office block", "barracks": "barrack block", "bust": "the bust on the roundabout", "plaza": "wholesale plaza", "unfinished": "half-built plaza", "pen": "livestock pen", "scrap": "scrap pile", "container": "shipping container", "crane": "gantry crane", "stack": "container stack", "tank": "fuel tank", "villa": "colonial bungalow", "cellblock": "prison cell block", "tower": "watchtower", "trailer": "parked trailer", "works": "waterworks building", "mound": "landfill mound", "bakery": "bakery", "warehouse": "warehouse", "school": "school block", "gatehouse": "gatehouse", "generator": "generator house", "water tank": "water tank on a stand", "mansion": "big house", "clubhouse": "clubhouse", "palace": "the palace", "bank tower": "bank tower (glass)", "apartment tower": "apartment tower (glass)", "nightclub": "club or lounge", "toll booth": "toll booth", "office block": "office or hotel block", "beach shack": "beach shack", "beach bar": "beach bar", "horse shelter": "horse shelter (beach rides)", "column": "refinery column", "flare stack": "flare stack", "unfinished house": "half-built house (no roof, nobody living)", "toll canopy": "toll plaza canopy", "brazilian house": "Brazilian house (brick, arches, shutters)"}.get(k, k) + (f", {st} storey" + ("s" if st > 1 else "") if k in ("front", "back", "school", "warehouse", "bank tower", "brazilian house") else "")

def overview():
    from collections import Counter
    for k, d in DS.items(): print(f"{d['name']} (inspired by {d['inspired']}): {DP[k].area/1e6:.2f} km²")
    print(f"buildings: {len(B)}  by kind: {dict(Counter(k for k,_,_ in B))}")
    print(f"storeys: {dict(sorted(Counter(st for *_,st in B).items()))}")
    print(f"ways: " + ", ".join(f"{k} {sum(g.length for kk,_,g in ways if kk==k)/1000:.1f} km" for k in sorted(set(k for k,_,_ in ways))))
    print("named main roads/arterials: " + ", ".join(sorted({n for k,n,_ in ways if n})))
    print("parcels: " + ", ".join(f"{k} {p.area/1e4:.2f} ha" for k, p in PARCELS))
    print(f"landmarks/civic places: {len(POIS)} (run: places)")
    print(f"rail inside: {RAIL.intersection(POLY).length:.0f} m; canal: {sum(c.length for c in CANALS):.0f} m")
def places():
    for p in sorted(POIS, key=lambda p: (bool(p.get('civic')), p['type'])):
        print(f"{DS[p['d']]['name']} | {'civic' if p.get('civic') else 'LANDMARK'} | {p['type']} | {p['name']} | {p['x']},{p['y']} | {p.get('note','')[:90]}")
def look(x, y, r=60):
    pt = Point(x, y); k, n, g, d = nearest_way(pt)
    print(f"Standing at {x:.0f},{y:.0f} in {where(pt)}")
    print(f"nearest way: {label(k,n)}, {d:.1f} m away")
    near = [B[i] for i in BT.query(pt.buffer(r))]
    from collections import Counter
    print(f"within {r} m: {len(near)} buildings; " + ", ".join(f"{c}× {bkind(kk, st)}" for (kk, st), c in Counter((kk, st) for kk, _, st in near).most_common(8)))
    sty = Counter(BS[i] for i in BT.query(pt.buffer(r)) if BS[i])
    if sty: print("house styles: " + ", ".join(f"{c}× {s_}" for s_, c in sty.most_common()))
    if near:
        tall = max(near, key=lambda b: b[2]); print(f"tallest nearby: {bkind(tall[0], tall[2])}, {tall[1].area:.0f} m² footprint")
    inside = [b for b in near if b[1].contains(pt)]
    if inside: print(f"you are INSIDE a building ({bkind(inside[0][0], inside[0][2])})")
    for kk, p in PARCELS:
        if p.distance(pt) < 80: print(f"parcel: {kk} {p.distance(pt):.0f} m away")
    for p in POIS:
        dd = pt.distance(Point(p['x'], p['y']))
        if dd < 150: print(f"{'civic' if p.get('civic') else 'landmark'} {dd:.0f} m: {p['name']} ({p['type']}{', safe ground' if p.get('safe') else ''})")
    for sg in G.get("safe_ground", []):
        if sg["d"] in DIDS and Polygon(sg["pts"]).contains(pt): print(f"you are on SAFE GROUND: {sg['name']} (never a crime site or a chase route)")
    print(f"rail: {RAIL.distance(pt):.0f} m away" + (f"; canal: {min(c.distance(pt) for c in CANALS):.0f} m" if CANALS else ""))
def route(a, b, mode, through=False):
    Gx = graph(mode, through); pa, na = resolve(a); pb, nb = resolve(b, pa); pa, na = resolve(a, pb)   # repeated names: the nearest pair
    EL = list(Gx.edges(data=True))
    if mode == "ride" and BAN is not None and not through:   # round the ban: join a real piece of the network, not a sketch-road scrap at a border
        comps = sorted(nx.connected_components(Gx), key=len, reverse=True); keep_ = comps[0]
        for c in comps[1:]:   # the bans can cut a district off (the Frontier, behind the Heights): a ride with both ends there stays there
            if len(c) < 200: break
            ELc = [e for e in EL if e[0] in c]; Tc = STRtree([e[2]["geom"] for e in ELc]); ELm = [e for e in EL if e[0] in comps[0]]; Tm = STRtree([e[2]["geom"] for e in ELm])
            near_c = lambda p: ELc[int(np.atleast_1d(Tc.query_nearest(p))[0])][2]["geom"].distance(p)
            near_m = lambda p: ELm[int(np.atleast_1d(Tm.query_nearest(p))[0])][2]["geom"].distance(p)
            if near_c(pa) < near_m(pa) and near_c(pb) < near_m(pb): keep_ = c; break
        EL = [e for e in EL if e[0] in keep_]
    ET = STRtree([e[2]["geom"] for e in EL])
    def attach(p, tag):   # step onto the nearest point of the nearest way (not the nearest junction), splitting that way there
        u, v, e = EL[int(np.atleast_1d(ET.query_nearest(p))[0])]; g = e["geom"]; t = g.project(p); q = g.interpolate(t)
        n = ("start" if tag == "a" else "end", round(q.x, 2), round(q.y, 2))
        du, dv = (u, v) if Point(u).distance(Point(g.coords[0])) <= Point(v).distance(Point(g.coords[0])) else (v, u)
        ib = e.get("inban", 0.0); f = t / g.length if g.length else 0
        Gx.add_edge(du, n, w=t, kind=e["kind"], name=e["name"], geom=g, inban=ib * f)
        Gx.add_edge(n, dv, w=g.length - t, kind=e["kind"], name=e["name"], geom=g, inban=ib * (1 - f))
        return n, p.distance(q)
    sa, da = attach(pa, "a"); sb, db = attach(pb, "b")
    try: path = nx.shortest_path(Gx, sa, sb, weight="w")
    except nx.NetworkXNoPath:
        if mode == "ride" and BAN is not None and not through:
            print(f"NO LEGAL OKADA ROUTE from {na} to {nb}: the okada ban zones cut one end off from the other (try --through, or walk)")
        else: print(f"NO ROUTE from {na} to {nb} by {mode} — the network is split")
        return
    legs = []; total = 0
    for u, v in zip(path, path[1:]):
        e = Gx[u][v]; total += e["w"]; lab = label(e["kind"], e["name"])
        if legs and legs[-1][0] == lab: legs[-1][1] += e["w"]
        else: legs.append([lab, e["w"]])
    speed = 5 if mode == "walk" else 25
    dist = total + da + db; straight = pa.distance(pb)
    mins = dist / 1000 / speed * 60
    if mode == "ride": mins = total / 1000 / speed * 60 + (da + db) / 1000 / 5 * 60   # the bits off the bike's network are on foot
    print(f"{mode}: {na} -> {nb}: {dist:.0f} m ({mins:.1f} min" + (f", {da + db:.0f} m of it on foot" if mode == "ride" and da + db > 30 else f" at {speed} km/h") + f"); straight line {straight:.0f} m; detour ×{dist/max(1,straight):.2f}")
    print(f"off-network bits: {da:.0f} m at start, {db:.0f} m at end")
    if mode == "ride" and BAN is not None and not through and BAN.contains(pa) and BAN.contains(pb):
        print("okada ban: both ends are inside the ban zone; on foot it is the walk between them (try: walk)")
    if mode == "ride" and BAN is not None:
        if through: print(f"okada ban: {sum(Gx[u][v].get('inban', 0) for u, v in zip(path, path[1:])):.0f} m ridden inside the ban zone (--through)")
        for p_, d_, w_ in ((pa, da, "starts"), (pb, db, "ends")):
            if BAN.contains(p_) and not through: print(f"okada ban: the trip {w_} inside the ban zone; {d_:.0f} m on foot to the nearest road a bike may use")
            elif d_ > 150 and not through: print(f"okada ban: no legal road reaches where the trip {w_} (the ban zones cut it off); {d_:.0f} m on foot from the nearest road a bike may use")
    for lab, L in legs: print(f"  {L:5.0f} m  {lab}")
    P_ = lambda c: Point(c[1:] if isinstance(c[0], str) else c)   # route points: junctions, or the split points where a trip joins a way
    geo = LineString([P_(c) for c in path]) if len(path) > 1 else None
    if geo is not None:
        seen = [p['name'] for p in POIS if geo.distance(Point(p['x'], p['y'])) < 35]
        if seen: print("you pass: " + "; ".join(seen[:15]))
        for u, v in zip(path, path[1:]):
            e = Gx[u][v]
            if e["geom"].crosses(RAIL) or e["geom"].intersects(RAIL):
                over = [n for n, f in FLY if f.distance(e["geom"].intersection(RAIL)) < 15] if not e["geom"].intersection(RAIL).is_empty else []
                up = e["kind"] in ("skywalk", "footbridge")
                how = " (up on the deck)" if up else (f" (bridge: {over[0]})" if over else (" (worn path over the tracks)" if e["kind"] == "path" else " (at ground level)"))
                print(f"you cross the rail on {label(e['kind'], e['name'])}{how}")
        print("districts on the way: " + " -> ".join(dict.fromkeys(where(P_(c)) for c in path[::max(1, len(path)//12)] + [path[-1]])))
def home(n=None, dist=None):   # dist: a district id or part of its name ("hub", "Water"), to pick a house there
    want = None if dist is None else next((k for k in DS if dist.lower() in (k + " " + DS[k]["name"]).lower()), None)
    if dist is not None and want is None: print(f"no built district matching '{dist}'"); return
    res = [i for i, (k, p, st) in enumerate(B) if k in ("front", "back", "stilt") and (want is None or BD[i] == want)]
    i = res[n % len(res)] if n is not None else random.choice(res)   # n picks the n-th house; the printed id is its building index
    k, p, st = B[i]; c = p.centroid
    print(f"house #{i}: {bkind(k, st)}, footprint {p.area:.0f} m², at {c.x:.0f},{c.y:.0f}")
    look(c.x, c.y, 40)
def problems():
    far = [(i, k) for i, (k, p, st) in enumerate(B) if k in ("front", "back", "stilt") and nearest_way(p.centroid)[3] > 45]
    print(f"houses more than 45 m from any street, lane or path: {len(far)} of {sum(1 for k,_,_ in B if k in ('front','back'))}")
    for i, k in far[:8]: c = B[i][1].centroid; print(f"  #{i} {k} at {c.x:.0f},{c.y:.0f} ({nearest_way(c)[3]:.0f} m)")
    Gx = graph("walk"); comps = sorted(nx.connected_components(Gx), key=len, reverse=True)
    print(f"walking network pieces: {len(comps)} (sizes {[len(c) for c in comps[:6]]})")
    for c in comps[1:6]:
        q = next(iter(c)); print(f"  island near {q[0]:.0f},{q[1]:.0f}")
    dead = [n for n, d in Gx.degree() if d == 1 and POLY.buffer(-20).contains(Point(n))]
    print(f"dead ends inside: {len(dead)}")
if __name__ == "__main__":
    a = sys.argv[1:] or ["overview"]
    if a[0] == "overview": overview()
    elif a[0] == "places": places()
    elif a[0] == "look": look(float(a[1]), float(a[2]), float(a[3]) if len(a) > 3 else 60)
    elif a[0] in ("walk", "ride"): route(a[1], a[2], a[0], "--through" in a[3:])
    elif a[0] == "home": home(int(a[1]) if len(a) > 1 else None, a[2] if len(a) > 2 else None)
    elif a[0] == "problems": problems()
    else: print(__doc__)
