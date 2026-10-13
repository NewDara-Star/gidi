# Big pieces a district is known for, laid out before (or after) the ordinary street fabric.
# Used by gen_fabric.py when a district profile asks for them (the Hub: flyovers, slip roads, skywalks, terminal, station, stadium, hotel).
# Every size comes from the profile (which comes from the pattern study); this file only decides where things go.
import math
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union, substring
from shapely.affinity import rotate, translate

def rect(cx, cy, w, d, a):  # w along the front, d back from it, turned by angle a (radians)
    return translate(rotate(box(-w / 2, -d / 2, w / 2, d / 2), a, use_radians=True), cx, cy)

def direction_at(line, t):
    p, q = line.interpolate(max(0, t - 5)), line.interpolate(min(line.length, t + 5))
    L = p.distance(q) or 1; return (q.x - p.x) / L, (q.y - p.y) / L

def pts(g): return [[round(x, 1), round(y, 1)] for x, y in g.coords]

# ---------- the knot: where two arterials cross, with the rail close by ----------
def find_knot(arts, poly):
    """The crossing of two arterials that both run through it (a road that *ends* there is a branch, not a crossing)."""
    for i in range(len(arts)):
        for j in range(i + 1, len(arts)):
            a, b = arts[i][2], arts[j][2]; x = a.intersection(b)
            for p in getattr(x, "geoms", [x]):
                if p.geom_type != "Point" or not poly.buffer(-20).contains(p): continue
                if min(Point(g.coords[k]).distance(p) for g in (a, b) for k in (0, -1)) > 5: return i, j, p
    return None

def branches_near(k, arts, knot, r=200):
    """How many other arterials start or end on arterial k close to the knot (traffic must turn there, so k stays at ground level)."""
    a = arts[k][2]
    return sum(1 for n, c, b in arts if b is not a for e in (Point(b.coords[0]), Point(b.coords[-1])) if a.distance(e) < 3 and e.distance(knot) < r)

def build_interchange(arts, rail, poly, land, IC, blockers):
    """Flyover over the knot, bridges where arterials cross the rail, slip roads in the corners that are free.
    Returns structures (for the map and Unreal), slip roads (drivable lines), gores (land between slip road and arterials) and the knot."""
    hit = find_knot(arts, poly)
    if not hit: return [], [], [], None
    i, j, knot = hit
    fly_k = i if branches_near(i, arts, knot) <= branches_near(j, arts, knot) else j   # the road with no junction at the knot flies over it
    S = []
    a = arts[fly_k][2]; t = a.project(knot); L = IC["flyover_m"]
    fly = substring(a, max(0, t - L / 2), min(a.length, t + L / 2))
    # every other arterial crossing the rail inside the district gets a rail bridge (real: 92% of major-road rail crossings are bridged)
    for n, c, b in arts:
        x = b.intersection(rail)
        for p in getattr(x, "geoms", [x]):
            if p.geom_type != "Point" or not poly.contains(p) or fly.distance(p) < 1: continue
            tb = b.project(p); g = substring(b, max(0, tb - IC["rail_bridge_m"] / 2), min(b.length, tb + IC["rail_bridge_m"] / 2))
            S.append({"kind": "flyover", "name": f"{n} Rail Bridge", "geom": g, "layer": 1, "width": 22})
    S.append({"kind": "flyover", "name": f"{arts[fly_k][0]} Flyover", "geom": fly, "layer": 2 if any(fly.intersects(s["geom"]) for s in S) else 1, "width": 22})
    # slip roads: one per free corner of the crossing, joining the two arterials without the junction
    arms = []
    for k in (i, j):
        g = arts[k][2]; tk = g.project(knot)
        for sgn in (1, -1):
            room = (g.length - tk) if sgn > 0 else tk
            if room > 60: arms.append((k, sgn, g, tk))
    def arm_angle(arm):
        dx, dy = direction_at(arm[2], arm[3] + arm[1] * 40); return math.atan2(dy * arm[1], dx * arm[1])
    arms.sort(key=arm_angle)
    corners = [(arms[q], arms[(q + 1) % len(arms)]) for q in range(len(arms)) if arms[q][0] != arms[(q + 1) % len(arms)][0]]
    ramps, gores = [], []
    keep_out = unary_union(blockers + [rail.buffer(12)] + [b.buffer(14) for n, c, b in arts if b is not arts[i][2] and b is not arts[j][2]])
    for A, B in corners[:IC["slip_roads"]]:
        best = None
        clear_arms = unary_union([arts[i][2].buffer(12.5), arts[j][2].buffer(12.5)])
        for da in range(50, 260, 10):
            for db in range(50, 260, 10):
                if A[0] == fly_k and da < L / 2 + 10: continue   # leave the flying road before its flyover ramp starts
                if B[0] == fly_k and db < L / 2 + 10: continue
                pa = A[2].interpolate(A[3] + A[1] * da); pb = B[2].interpolate(B[3] + B[1] * db)
                for wk in (0.3, 0.5, 0.7):   # how hard the slip road bows toward the knot
                    ctl = (knot.x * wk + (pa.x + pb.x) / 2 * (1 - wk), knot.y * wk + (pa.y + pb.y) / 2 * (1 - wk))
                    cv = LineString([((1 - u) ** 2 * pa.x + 2 * (1 - u) * u * ctl[0] + u * u * pb.x, (1 - u) ** 2 * pa.y + 2 * (1 - u) * u * ctl[1] + u * u * pb.y) for u in [k / 16 for k in range(17)]])
                    if not 0.75 * IC["slip_road_m"] <= cv.length <= 1.4 * IC["slip_road_m"]: continue   # real slip roads: p25-p75 around the median
                    mid = substring(cv, 15, cv.length - 15)
                    if not land.buffer(-12).contains(mid) or mid.intersects(keep_out): continue
                    if cv.intersects(rail.buffer(6)) or any(s["geom"].buffer(12).contains(q) for s in S for q in (pa, pb) if s["geom"] is not fly): continue   # never across the rail, never off a bridge
                    gore = Polygon(list(cv.coords) + [knot.coords[0]]).buffer(0).difference(clear_arms).difference(cv.buffer(6.5))
                    sc = -gore.area + abs(cv.length - IC["slip_road_m"]) * 5   # keep usable land between slip road and arterials
                    if best is None or sc < best[0]: best = (sc, cv, pa, pb)
        if best:
            sc, cv, pa, pb = best; ramps.append(cv)
            g = Polygon(list(cv.coords) + [knot.coords[0]]).buffer(0)
            gores.append(g)
    if len(ramps) < IC["slip_roads"]:
        import sys; print(f"interchange: {len(ramps)} of {IC['slip_roads']} slip roads fit (rail, bridges or branches block the other corners)", file=sys.stderr)
    return S, ramps, gores, knot

def skywalks(front_line, at_pt, n, length, avoid, spacing=120):
    """Footbridges straight across a big road, `spacing` apart, centred on the terminal's front so they land on it."""
    out = []; t0 = front_line.project(at_pt)
    for k in range(n):
        for t in (t0 + (k - (n - 1) / 2) * spacing + d for d in (0, 10, -10)):
            if not 0 < t < front_line.length: continue
            p = front_line.interpolate(t); ux, uy = direction_at(front_line, t)
            g = LineString([(p.x + uy * length / 2, p.y - ux * length / 2), (p.x - uy * length / 2, p.y + ux * length / 2)])
            if not g.intersects(avoid): out.append(g); break
    return out

# ---------- big places carved out of the land before streets are drawn ----------
def place_reserved(spec, hint, front_lines, clear_off, land, avoid, gap):
    """Find a rectangle of the right size as close to `hint` as possible.
    front_lines: lines it must face (arterial / rail), or [] to sit anywhere oriented to the nearest road.
    gap: room left around it for its own access road. Returns (rect, front line, offset) or None."""
    m2, asp = spec["m2"], spec["aspect"]; w = math.sqrt(m2 * asp); d = m2 / w; best = None
    if front_lines:
        for fl in front_lines:
            t0 = fl.project(hint)
            for dt in range(-450, 451, 10):
                t = t0 + dt
                if not 30 < t < fl.length - 30: continue
                p = fl.interpolate(t); ux, uy = direction_at(fl, t); a = math.atan2(uy, ux)
                for side in (1, -1):
                    nx, ny = -uy * side, ux * side; off = clear_off + 1
                    r = rect(p.x + nx * (off + d / 2), p.y + ny * (off + d / 2), w, d, a)
                    if not land.buffer(-4).contains(r) or r.buffer(gap).intersects(avoid): continue
                    if any(r.distance(f) < clear_off for f in front_lines): continue   # sits on its own road
                    if not land.buffer(-4).contains(r.buffer(gap).difference(fl.buffer(clear_off + gap + 2))): continue
                    sc = r.centroid.distance(hint)
                    if best is None or sc < best[0]: best = (sc, r, (fl, t, side, off, w, d, a))
    else:
        for dx in range(-450, 451, 15):
            for dy in range(-450, 451, 15):
                c = Point(hint.x + dx, hint.y + dy)
                if not land.contains(c): continue
                for a in (0, math.pi / 4, math.pi / 2, 3 * math.pi / 4):
                    r = rect(c.x, c.y, w, d, a)
                    if not land.buffer(-4).contains(r.buffer(gap)) or r.buffer(gap).intersects(avoid): continue
                    sc = c.distance(hint)
                    if best is None or sc < best[0]: best = (sc, r, (None, 0, 1, 0, w, d, a))
    return best[1:] if best else None

def u_road(info, gap):
    """Access road around the back and sides of a parcel that faces a big road: its two legs come back to that road."""
    fl, t, side, off, w, d, a = info
    p = fl.interpolate(t); ux, uy = direction_at(fl, t); nx, ny = -uy * side, ux * side
    def P(u, v): return (p.x + ux * u + nx * v, p.y + uy * u + ny * v)
    hw = w / 2 + gap; back = off + d + gap
    return LineString([P(-hw, 0), P(-hw, back), P(hw, back), P(hw, 0)])

def back_road(info, gap, extra=40):
    """A street along the back of a parcel that faces the rail (people reach the station from the town side)."""
    fl, t, side, off, w, d, a = info
    p = fl.interpolate(t); ux, uy = direction_at(fl, t); nx, ny = -uy * side, ux * side
    def P(u, v): return (p.x + ux * u + nx * v, p.y + uy * u + ny * v)
    return LineString([P(-w / 2 - extra, off + d + gap), P(w / 2 + extra, off + d + gap)])

def ring_road(r, gap, hard_union, n_access=1, avoid=None):
    """A loop around a parcel with no frontage (the stadium) and straight access roads to the nearest road:
    the first from the nearest point, any more from other sides of the loop (never across `avoid`, e.g. the rail)."""
    ring = r.buffer(gap, join_style=2).exterior
    from shapely.ops import nearest_points
    a, b = nearest_points(ring, hard_union)
    out = [LineString(ring.coords), LineString([a, b])]
    if n_access > 1:
        cc = list(ring.coords); sides = [LineString([p, q]) for p, q in zip(cc, cc[1:]) if math.dist(p, q) > 10]
        used = [min(range(len(sides)), key=lambda i: sides[i].distance(a))]
        for _ in range(n_access - 1):
            best = None
            for i, sd in enumerate(sides):
                if i in used: continue
                for f in (0.3, 0.5, 0.7):
                    p0 = sd.interpolate(f, normalized=True); q0 = nearest_points(hard_union, p0)[0]; seg = LineString([p0, q0])
                    if seg.length < 1 or seg.crosses(ring) or seg.intersects(r) or (avoid is not None and seg.intersects(avoid)): continue
                    if best is None or seg.length < best[0]: best = (seg.length, seg, i)
            if best: out.append(best[1]); used.append(best[2])
    return out

# ---------- buildings inside the big places ----------
def stands(parcel, bowl_m2, inset=6, n=4):
    """A 1970s bowl: an oval ring of stands around the pitch, in n pieces (gaps are the entrances). Returns (stands, pitch)."""
    mr = parcel.minimum_rotated_rectangle; cc = list(mr.exterior.coords)
    l1, l2 = math.dist(cc[0], cc[1]), math.dist(cc[1], cc[2])
    a = math.atan2(cc[1][1] - cc[0][1], cc[1][0] - cc[0][0]) if l1 >= l2 else math.atan2(cc[2][1] - cc[1][1], cc[2][0] - cc[1][0])
    A, B = max(l1, l2) / 2 - inset, min(l1, l2) / 2 - inset
    k = math.sqrt(max(0.05, 1 - bowl_m2 / (math.pi * A * B)))   # inner oval scaled so the stands cover bowl_m2
    c = parcel.centroid; ca, sa = math.cos(a), math.sin(a)
    def P(r, th): x, y = r * A * math.cos(th), r * B * math.sin(th); return (c.x + x * ca - y * sa, c.y + x * sa + y * ca)
    out = []; gapr = 0.06
    for q in range(n):
        t0, t1 = 2 * math.pi * q / n + gapr, 2 * math.pi * (q + 1) / n - gapr
        ths = [t0 + (t1 - t0) * s / 12 for s in range(13)]
        out.append(Polygon([P(1, th) for th in ths] + [P(k, th) for th in reversed(ths)]))
    pitch = Polygon([P(k * 0.92, 2 * math.pi * s / 48) for s in range(48)])
    return out, pitch

def stall_rows(area, angle, w=3.5, d=3.0, aisle=2.0):
    """Rows of market stalls filling `area` (the under-bridge trade)."""
    out = []; c = area.centroid; R = math.sqrt(area.area) * 2 + 40
    ca, sa = math.cos(angle), math.sin(angle); inner = area.buffer(-1.0)
    y = -R
    while y < R:
        for yy in (y, y + d):   # back-to-back pair of stall rows, then an aisle
            x = -R
            while x < R:
                cx, cy = c.x + x * ca - yy * sa, c.y + x * sa + yy * ca
                r = rect(cx, cy, w, d, angle)
                if inner.contains(r): out.append(r)
                x += w + 0.3
        y += d * 2 + aisle
    return out
