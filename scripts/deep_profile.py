# From a district's deep study (docs/data/deep/<id>.json) to its generator settings, and its fabric-type zones (docs/DEEP-STUDY.md).
#
# rules(did): the district-wide Lagos-fabric settings. The conversions are calibrated on the Food Gate pilot, the one district tuned by
#   hand against real Lagos (docs/pilot-foodgate.md): fed real Food Gate's numbers they give back the pilot's settings (touch 0.70, block
#   fill 0.43, small share 0.18, wobble 9 deg, back row 0.69).
# zones(did, land, roads_main, water, seed): the district cut into its fabric types (the study's 250 m cells, clustered), laid out the
#   way the study's gradients run: the busiest, densest types along the main roads, the open ones toward the water and the city's edge,
#   with a slow wobble so the patches read as neighbourhoods, not rings. Each zone carries rules relative to the district's own.
import json, math, os
import numpy as np
from shapely.geometry import box, Point
from shapely.ops import unary_union

STOREY_BANDS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 6), (7, 13), (14, 20)]
clamp = lambda v, lo, hi: max(lo, min(hi, v))


def study(did):
    f = f'docs/data/deep/{did}.json'
    return json.load(open(f)) if os.path.exists(f) else None


def h_bands(J):
    """The study's storeys by built area (1..8, 8 meaning 8+) as the generator's height bands (shares per STOREY_BANDS)."""
    s = {int(k): v for k, v in (J['heights'].get('storeys_share_by_area') or J['heights']['storeys_share']).items()}
    b = [s.get(1, 0), s.get(2, 0), s.get(3, 0), s.get(4, 0), s.get(5, 0) + s.get(6, 0), s.get(7, 0) + s.get(8, 0), 0.0]
    t = sum(b) or 1
    return [round(x / t, 4) for x in b]   # shares of built area, as district_profiles.height_bands gives


def rules(did):
    J = study(did)
    if not J or not J.get('structure_built_squares'):
        return {}
    Q = J['structure_built_squares']; B = J['buildings']
    med = lambda k: (Q.get(k) or {}).get('median') if isinstance(Q.get(k), dict) else Q.get(k)
    cover, touching = med('cover'), med('touching')
    back = clamp(med('back_cover') / max(med('edge_cover'), 1e-6) * 0.75, 0.2, 0.9)
    touch = clamp(touching - 0.05, 0.15, 0.9)
    return {
        'fabric': 'lagos', 'deep': True,
        'touch': round(touch, 3), 'gap_m': [0.6, round(max(1.5, B['nearest_gap_m']['p90']), 1)],
        'vacant': round(clamp(0.04 + (0.38 - cover) * 0.6, 0.02, 0.5), 3),
        'back_row': round(back, 3), 'courtyard_m': [0.8, 2.5],
        'wobble_deg': round(clamp(Q.get('line_deg.median', 5) * 1.9, 3, 18), 1),
        'infill': {'block_fill': round(clamp(Q.get('block_fill.median', 0.3) * 0.95, 0.05, 0.8), 3), 'touch': round(min(0.95, touch + 0.15), 3),
                   'small_share': round(clamp(med('under_40m2') * 0.8, 0.02, 0.6), 3), 'small_m2': [8, 38],
                   'room_m2': [50, round(clamp(B['size_m2']['p75'] * 0.8, 90, 400))]},
        'h_bands': h_bands(J),
    }


def _noise(xs, ys, seed, L=260.0):
    """A slow, smooth wobble (about L metres across), the same every run."""
    r = np.random.RandomState(seed); ph = r.uniform(0, 6.283, 4)
    return (np.sin(xs / L + ph[0]) * np.cos(ys / (1.3 * L) + ph[1]) + 0.5 * np.sin((xs + ys) / (0.6 * L) + ph[2])
            + 0.5 * np.cos((xs - ys) / (0.8 * L) + ph[3])) / 2.0


def zones(did, land, roads_main, water, seed=11, cell=40.0, base=None):
    """[(polygon, type dict, rules dict)] covering the land; [] if the study found fewer than two types."""
    J = study(did)
    if not J or len(J.get('fabric_types') or []) < 2:
        return []
    T = J['fabric_types']; C = J['built_cells_250m']
    base = base or rules(did)   # the district's settings in force (tuned), else the study's
    cmed = C['cover']['p50'] or 0.3; smed = C['size_m2_median']['p50'] or 100; stmed = C['storeys_mean']['p50'] or 1.5
    # busy rank: cover, density and places together (the study's own clusters, ordered)
    busy = sorted(T, key=lambda t: -(t['cover'] / cmed + t['buildings_per_km2'] / max(C['buildings_per_km2']['p50'], 1) + 0.3 * math.log1p(t['places_per_km2'])))
    x0, y0, x1, y1 = land.bounds
    xs = np.arange(x0 + cell / 2, x1, cell); ys = np.arange(y0 + cell / 2, y1, cell)
    X, Y = np.meshgrid(xs, ys)
    from shapely import contains_xy, distance
    from shapely.geometry import Point as _P
    inside = contains_xy(land, X, Y)
    pts = [(x, y) for x, y in zip(X[inside], Y[inside])]
    if not pts:
        return []
    import shapely
    geo = shapely.points(np.array(pts))
    dm = shapely.distance(geo, roads_main) if roads_main is not None and not roads_main.is_empty else np.full(len(pts), 500.0)
    edge = land.boundary
    de = shapely.distance(geo, edge)
    dw = shapely.distance(geo, water) if water is not None and not water.is_empty else np.full(len(pts), 2000.0)
    # high score = busy: near a main road, away from the water and the outer edge
    score = np.exp(-dm / 220.0) + 0.6 * np.clip(dw / 600.0, 0, 1) + 0.3 * np.clip(de / 300.0, 0, 1) + 0.55 * _noise(geo_x := np.array([p[0] for p in pts]), np.array([p[1] for p in pts]), seed)
    order = np.argsort(-score, kind='stable')
    shares = np.array([t['share_of_built_cells'] for t in busy]); shares = shares / shares.sum()
    cut = np.round(np.cumsum(shares) * len(order)).astype(int)
    lab = np.empty(len(order), int)
    start = 0
    for k, c in enumerate(cut):
        lab[order[start:c]] = k; start = c
    lab[order[start:]] = len(busy) - 1
    out = []
    for k, t in enumerate(busy):
        cells = [box(p[0] - cell / 2, p[1] - cell / 2, p[0] + cell / 2, p[1] + cell / 2) for p, l in zip(pts, lab) if l == k]
        if not cells:
            continue
        z = unary_union(cells).buffer(cell * 0.6).buffer(-cell * 0.6).intersection(land)   # smooth the cell edges
        rc = t['cover'] / cmed
        # a zone's built share follows its real cover: plots left empty in proportion (the open types really are open)
        r = {'vacant': round(clamp(1 - (1 - base.get('vacant', 0.07)) * min(rc, 1.0) ** 1.2, 0.01, 0.8), 3),
             'touch': round(clamp(t['touching'] - 0.05, 0.1, 0.95), 3),
             'back_row': round(clamp(base.get('back_row', 0.6) * rc, 0.1, 0.95), 3),
             'block_fill': round(clamp(base.get('infill', {}).get('block_fill', 0.3) * rc, 0.05, 0.85), 3),
             'size_scale': round(clamp(t['size_m2_median'] / smed, 0.5, 2.5), 2),
             'storeys_scale': round(clamp(t['storeys_mean'] / stmed, 0.6, 2.5), 2)}
        out.append((z, t, r))
    # each cell belongs to exactly one zone: the smoothing can overlap neighbours, so later zones give way
    done = None
    clean = []
    for z, t, r in out:
        if done is not None:
            z = z.difference(done)
        done = z if done is None else done.union(z)
        if not z.is_empty:
            clean.append((z, t, r))
    return clean
