# How a place is built, not just how much: the structure measures of the Google rebuild (docs/REBUILD-PLAN.md).
# measure(buildings, streets, area) works the same on real Lagos (Google Open Buildings outlines + OSM streets, metres)
# and on Gidi (a district's buildings and ways), so a district can be scored against its inspiration like for like.
#
#   block fill      share of each street block's land that is built (blocks: land cut by the streets)
#   edge / back     ground built within 20 m of a street, and deeper than 20 m (the back of the block)
#   line            angle between a building's long side and its nearest street (0 = square to the street, 45 = skewed)
#   front           share of street length with a building within 12 m of the kerb on that side; slot widths between them
#   touching        share of buildings with another within 1 m (shared or nearly shared walls)
#   size            footprint percentiles; share under 40 m2 (kiosks, shacks, extensions, back rooms); long side
#   setback         distance from a front building to its street's centre line
import math
import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union, polygonize
from shapely.strtree import STRtree

FRONT_M = 12.0     # a building this near the kerb is on the street front
EDGE_M = 20.0      # the street edge band of a block


def _axis(p):
    """Angle (radians, 0..pi) and length of a footprint's long side, from its minimum rotated rectangle."""
    r = p.minimum_rotated_rectangle
    c = list(r.exterior.coords) if r.geom_type == 'Polygon' else [(0, 0), (1, 0)]
    best = (0, 0.0)
    for a, b in zip(c, c[1:]):
        L = math.dist(a, b)
        if L > best[1]:
            best = (math.atan2(b[1] - a[1], b[0] - a[0]) % math.pi, L)
    return best


def measure(buildings, streets, area, widths=None):
    """buildings: shapely Polygons; streets: LineStrings (centre lines); area: Polygon to measure inside.
    widths: optional list of carriageway widths per street (default 7 m)."""
    B = [b for b in buildings if b.is_valid and b.area > 4 and area.contains(b.centroid)]
    S = [s for s in streets if s.length > 1 and s.intersects(area)]
    W = widths or [7.0] * len(S)
    st = STRtree(S)
    bt = STRtree(B)
    out = {'buildings': len(B), 'area_km2': round(area.area / 1e6, 3)}
    if not B or not S:
        return out
    fp = np.array([b.area for b in B])
    out['per_km2'] = round(len(B) / (area.area / 1e6))
    out['cover'] = round(float(fp.sum() / area.area), 3)
    out['size_m2'] = {q: round(float(np.percentile(fp, p)), 1) for q, p in (('p10', 10), ('p25', 25), ('median', 50), ('p75', 75), ('p90', 90))}
    out['under_40m2'] = round(float((fp < 40).mean()), 3)
    ax = [_axis(b) for b in B]
    out['long_side_m'] = {'median': round(float(np.median([a[1] for a in ax])), 1), 'p90': round(float(np.percentile([a[1] for a in ax], 90)), 1)}
    # line and setback: each building against its nearest street
    ang, setb, dist = [], [], []
    for b, (a, L) in zip(B, ax):
        c = b.centroid
        j = min(st.query(c.buffer(80)), key=lambda j: S[j].distance(c), default=None)
        if j is None:
            dist.append(99.0)
            continue
        s = S[j]
        d = s.distance(c)
        dist.append(b.distance(s))
        t = s.project(c)
        p1, p2 = s.interpolate(max(0, t - 3)), s.interpolate(min(s.length, t + 3))
        sa = math.atan2(p2.y - p1.y, p2.x - p1.x) % math.pi
        diff = abs((a - sa + math.pi / 2) % math.pi - math.pi / 2)   # 0 parallel ... pi/2 perpendicular
        ang.append(math.degrees(min(diff, math.pi / 2 - diff)))       # 0 = square to the street either way, 45 = skewed
        if b.distance(s) <= FRONT_M + W[j] / 2:
            setb.append(d)
    dist = np.array(dist)
    out['line_deg'] = {'median': round(float(np.median(ang)), 1), 'p75': round(float(np.percentile(ang, 75)), 1), 'share_within_10deg': round(float((np.array(ang) <= 10).mean()), 3)} if ang else None
    out['setback_m'] = {'median': round(float(np.median(setb)), 1), 'p25': round(float(np.percentile(setb, 25)), 1), 'p75': round(float(np.percentile(setb, 75)), 1)} if setb else None
    out['front_share_of_buildings'] = round(float((dist <= FRONT_M).mean()), 3)
    # edge and back of the block
    sb = unary_union([s.buffer(w / 2 + EDGE_M) for s, w in zip(S, W)]).intersection(area)
    road = unary_union([s.buffer(w / 2) for s, w in zip(S, W)]).intersection(area)
    built = unary_union(B)
    edge_land = sb.difference(road)
    back_land = area.difference(sb)
    out['edge_cover'] = round(float(built.intersection(edge_land).area / max(1, edge_land.area)), 3)
    out['back_cover'] = round(float(built.intersection(back_land).area / max(1, back_land.area)), 3)
    # block fill
    blocks = [p for p in polygonize(unary_union(S + [area.exterior])) if p.area > 400 and area.contains(p.representative_point())]
    fills = []
    for p in blocks:
        land = p.difference(road)
        if land.area < 400:
            continue
        fills.append(built.intersection(land).area / land.area)
    if fills:
        out['block_fill'] = {'median': round(float(np.median(fills)), 3), 'p75': round(float(np.percentile(fills, 75)), 3), 'blocks': len(fills)}
    # the street front: walk each street side every 2 m, is there a building within FRONT_M of the kerb?
    occ, slots = [], []
    for s, w in zip(S, W):
        seg = s.intersection(area)
        for g in getattr(seg, 'geoms', [seg]):
            if g.geom_type != 'LineString' or g.length < 20:
                continue
            for side in (w / 2 + FRONT_M / 2, -(w / 2 + FRONT_M / 2)):
                try:
                    off = g.offset_curve(side)
                except Exception:
                    continue
                if off.is_empty or off.geom_type != 'LineString':
                    continue
                n = max(2, int(off.length / 2))
                hit = []
                for k in range(n):
                    q = off.interpolate(off.length * k / (n - 1))
                    hit.append(any(B[j].distance(q) <= FRONT_M / 2 for j in bt.query(q.buffer(FRONT_M / 2))))
                occ.append((sum(hit), len(hit)))
                run = 0
                for h in hit + [True]:
                    if not h:
                        run += 1
                    elif run:
                        slots.append(run * off.length / (n - 1))
                        run = 0
    if occ:
        out['front_occupied'] = round(sum(a for a, b in occ) / sum(b for a, b in occ), 3)
    if slots:
        sl = np.array(slots)
        out['front_gap_m'] = {'median': round(float(np.median(sl)), 1), 'p75': round(float(np.percentile(sl, 75)), 1), 'share_under_3m': round(float((sl < 3).mean()), 3)}
    # touching
    tch = 0
    for i, b in enumerate(B):
        if any(j != i and B[j].distance(b) < 1.0 for j in bt.query(b.buffer(1.0))):
            tch += 1
    out['touching'] = round(tch / len(B), 3)
    return out
