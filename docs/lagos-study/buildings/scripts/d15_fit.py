"""Mùṣá (d15): where our drawn houses sit over or under Google, and whether their kinds, storeys and sizes fit each real
block (building study, 27 Oct; the building-study agent). Reads d17_blocks.py's JSON and re-cuts the same blocks.

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d17_blocks.py d15 --json x.json
  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d15_fit.py x.json [--md]

What it adds to d17_blocks.py / d17_fabric.py (which give the block table and the furthest-below list):
1. Each block's border street: the Overture named street with the most length within 12 m of the block (real m), so the
   hand pass can find it by name. Study only: real names stay in docs/, never in map records.
2. Our houses' footprints per block (median m2, share under 40 m2, share of 500 m2 and up) beside Google's.
3. The roof gap per block in Gidi m2 ((Google cover - our cover) x the block's Gidi area), both ways: furthest below
   and furthest above; and our cover over the block's land left free of our carriageways ("ours net"), beside Google's.
4. A 100 m Gidi grid (300 m real): Google's cover (90% threshold, union clipped to the cell and the outline) against
   ours (our roofs' union clipped the same), cell by cell. Cells under 30% inside the outline are left out.
5. Fit flags for blocks with 10+ Google buildings and 5+ of ours: storeys (mean storeys, share at 3+), size (median
   footprint ratio), shacks (our shack share against Google's share under 40 m2), sheds (ours against Google's share of
   500 m2 and up), shops (our lock-up and kiosk share against Overture places per hectare).
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B  # noqa: E402

import numpy as np  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
import shapely  # noqa: E402
from shapely.geometry import LineString, Polygon, box  # noqa: E402
from shapely.ops import unary_union  # noqa: E402
from shapely.strtree import STRtree  # noqa: E402

D = 'd15'
CELL = 100   # Gidi m


def named_streets(w, s, e, n):
    t = pq.read_table(B.OV + 'lagos_overture_segment.parquet', columns=['subtype', 'class', 'names', 'geometry', 'bbox'])
    out = []
    for r in t.to_pylist():
        b = r['bbox']
        if b['xmax'] < w or b['xmin'] > e or b['ymax'] < s or b['ymin'] > n or r['subtype'] != 'road':
            continue
        nm = (r['names'] or {}).get('primary')
        if nm:
            out.append((nm, B.to_utm(shapely.from_wkb(r['geometry']))))
    return out


def main():
    R = json.load(open(sys.argv[1]))[D]
    rows = R['blocks']
    Dr, recs, ring_g, ring_u = B.load(D)
    w, s, e, n = B.lonlat_box(ring_u)
    blocks, _, _, _, _ = B.blocks_of(ring_u, w, s, e, n)
    assert len(blocks) == len(rows), (len(blocks), len(rows))
    for bk, r in zip(blocks, rows):
        assert abs(round(bk.area) - r['area_real_m2']) <= 1, r['block']
    t90 = R['summary']['t90']
    G = [g for c, g in B.google(w, s, e, n) if c >= t90 and ring_u.intersects(g)]
    gtree = STRtree([g.centroid for g in G])
    houses = [r for r in recs if r['type'] == 'building']
    HP = [Polygon(h['footprint']) for h in houses]
    htree = STRtree([p.centroid for p in HP])
    roads = [r for r in recs if r['type'] == 'road']
    CW = unary_union([LineString([q[:2] for q in r['centreline']]).buffer(r['width'] / 2, cap_style=2) for r in roads])
    ST = named_streets(w, s, e, n)
    stree = STRtree([g for _, g in ST])

    out = []
    for bk, r in zip(blocks, rows):
        bg = B.utm_to_gidi(bk)
        ih = [i for i in htree.query(bg) if bg.contains(HP[i].centroid)]
        oa = sorted(HP[i].area for i in ih)
        ig = [i for i in gtree.query(bk) if bk.contains(G[i].centroid)]
        ga = sorted(G[i].area for i in ig)
        near = collections.Counter()
        zone = bk.boundary.buffer(12)
        for j in stree.query(zone):
            near[ST[j][0]] += ST[j][1].intersection(zone).length
        free = bg.area - CW.intersection(bg).area
        roof = unary_union([HP[i] for i in ih]).intersection(bg).area if ih else 0.0
        kinds = r['ours_kinds']
        on = max(1, r['ours_n'])
        ost = {int(k): v for k, v in r['ours_storeys'].items()}
        gst = {int(k): v for k, v in r['storeys'].items()}
        mean = lambda d: sum(k * v for k, v in d.items()) / max(1, sum(d.values()))
        three = lambda d: sum(v for k, v in d.items() if k >= 3) / max(1, sum(d.values()))
        out.append(dict(
            block=r['block'], xy=r['centroid_gidi'], street=[k for k, _ in near.most_common(2)],
            g_cover=r['cover90'], o_cover=r['ours_cover'], o_net=round(roof / free, 3) if free > 1 else None,
            o_cw=r['ours_carriageway_share'], gap_m2=round((r['cover90'] - r['ours_cover']) * r['area_gidi_m2']),
            g_n=r['n90'], o_n=r['ours_n'], g_n_at_scale=round(r['n90'] / 9, 1),
            g_med=r['median_m2'], o_med=round(float(np.median(oa)), 1) if oa else None,
            g_small=round(sum(a < 40 for a in ga) / len(ga), 2) if ga else 0,
            o_small=round(sum(a < 40 for a in oa) / len(oa), 2) if oa else 0,
            g_big=round(sum(a >= 500 for a in ga) / len(ga), 2) if ga else 0,
            o_big=round(sum(a >= 500 for a in oa) / len(oa), 2) if oa else 0,
            g_storey_mean=round(mean(gst), 2), o_storey_mean=round(mean(ost), 2),
            g_three=round(three(gst), 2), o_three=round(three(ost), 2),
            o_shack=round(kinds.get('shack', 0) / on, 2), o_shed=round(kinds.get('shed', 0) / on, 2),
            o_shop=round((kinds.get('shop_under_flats', 0) + kinds.get('kiosk_row', 0)) / on, 2),
            o_walkup=round(kinds.get('walkup', 0) / on, 2),
            places_ha=round(r['places'] / (r['area_real_m2'] / 1e4), 1),
            area_gidi=r['area_gidi_m2']))

    # grid
    OU = unary_union(HP)
    GU = unary_union(G)
    x0, y0, x1, y1 = ring_g.bounds
    cells = []
    for cx in np.arange(np.floor(x0 / CELL) * CELL, x1, CELL):
        for cy in np.arange(np.floor(y0 / CELL) * CELL, y1, CELL):
            c = box(cx, cy, cx + CELL, cy + CELL).intersection(ring_g)
            if c.area < 0.3 * CELL * CELL:
                continue
            cu = shapely.transform(c, lambda a: np.column_stack(B.g2u(a[:, 0], a[:, 1])))
            gcv = GU.intersection(cu).area / cu.area
            ocv = OU.intersection(c).area / c.area
            cw = CW.intersection(c).area / c.area
            cells.append(dict(cell=f'{int(cx)},{int(cy)}', g=round(gcv, 3), o=round(ocv, 3), cw=round(cw, 3),
                              gap_m2=round((gcv - ocv) * c.area), area=round(c.area)))

    res = dict(blocks=out, cells=cells,
               whole=dict(o_med=round(float(np.median([p.area for p in HP])), 1),
                          o_small=round(sum(p.area < 40 for p in HP) / len(HP), 3),
                          o_big=sum(p.area >= 500 for p in HP),
                          g_med=round(float(np.median([g.area for g in G])), 1), g_n=len(G),
                          o_roof=round(OU.intersection(ring_g).area), g_roof=round(GU.intersection(ring_u).area),
                          ring_g=round(ring_g.area), ring_u=round(ring_u.area),
                          o_cw=round(CW.intersection(ring_g).area / ring_g.area, 3)))
    json.dump(res, open(sys.argv[1].replace('.json', '_fit.json'), 'w'), ensure_ascii=False, indent=1)
    report(res)


def report(res):
    W = res['whole']
    print('whole:', json.dumps(W))
    print('ours/Google cover whole:', round(W['o_roof'] / W['ring_g'], 4), round(W['g_roof'] / W['ring_u'], 4))
    bl = res['blocks']
    print('\nfurthest BELOW (gap m2 Gidi):')
    for b in sorted(bl, key=lambda b: -b['gap_m2'])[:20]:
        print(f"  {b['block']} {b['xy']} {b['street']} G {b['g_cover']:.0%} ours {b['o_cover']:.0%} net {b['o_net']} "
              f"cw {b['o_cw']:.0%} gap {b['gap_m2']} n {b['g_n_at_scale']}/{b['o_n']}")
    print('\nfurthest ABOVE:')
    for b in sorted(bl, key=lambda b: b['gap_m2'])[:20]:
        print(f"  {b['block']} {b['xy']} {b['street']} G {b['g_cover']:.0%} ours {b['o_cover']:.0%} net {b['o_net']} "
              f"cw {b['o_cw']:.0%} gap {b['gap_m2']} n {b['g_n_at_scale']}/{b['o_n']}")
    tot_below = sum(b['gap_m2'] for b in bl if b['gap_m2'] > 0)
    tot_above = -sum(b['gap_m2'] for b in bl if b['gap_m2'] < 0)
    print('\nsum below', tot_below, 'sum above', tot_above, 'blocks below', sum(b['gap_m2'] > 0 for b in bl))
    within = [b for b in bl if abs(b['g_cover'] - b['o_cover']) <= 0.05]
    print('blocks within 5 points', len(within), 'of', len(bl))
    print('blocks ours >= google', sum(b['o_cover'] >= b['g_cover'] for b in bl))
    nets = [b for b in bl if b['o_net'] is not None and b['o_cw'] < 0.9]
    print('median g_cover', np.median([b['g_cover'] for b in bl]), 'median ours', np.median([b['o_cover'] for b in bl]),
          'median ours net', np.median([b['o_net'] for b in nets]))
    print('\ncells (100 m Gidi):', len(res['cells']))
    cs = res['cells']
    for lab, key in (('BELOW', lambda c: -c['gap_m2']), ('ABOVE', lambda c: c['gap_m2'])):
        print(' cells', lab)
        for c in sorted(cs, key=key)[:10]:
            print(f"  {c['cell']} G {c['g']:.0%} ours {c['o']:.0%} cw {c['cw']:.0%} gap {c['gap_m2']} area {c['area']}")
    print(' cells within 5 points:', sum(abs(c['g'] - c['o']) <= 0.05 for c in cs),
          'ours over by 5+:', sum(c['o'] - c['g'] > 0.05 for c in cs), 'under by 5+:', sum(c['g'] - c['o'] > 0.05 for c in cs))
    # fit
    F = [b for b in bl if b['g_n'] >= 10 and b['o_n'] >= 5]
    print('\nfit blocks', len(F))
    flags = collections.defaultdict(list)
    for b in F:
        if b['o_storey_mean'] - b['g_storey_mean'] >= 0.5:
            flags['storeys high'].append(b)
        if b['g_storey_mean'] - b['o_storey_mean'] >= 0.5:
            flags['storeys low'].append(b)
        if b['o_med'] and b['g_med'] and b['o_med'] / b['g_med'] < 0.6:
            flags['houses small'].append(b)
        if b['o_med'] and b['g_med'] and b['o_med'] / b['g_med'] > 1.6:
            flags['houses big'].append(b)
        if b['o_shack'] - b['g_small'] >= 0.2:
            flags['shacks over'].append(b)
        if b['g_big'] >= 0.15 and b['o_shed'] + b['o_big'] < 0.05:
            flags['sheds missing'].append(b)
        if b['places_ha'] >= 8 and b['o_shop'] < 0.1:
            flags['shops missing'].append(b)
        if b['places_ha'] < 2 and b['o_shop'] >= 0.5:
            flags['shops heavy on quiet block'].append(b)
    for k, v in flags.items():
        print(f' {k}: {len(v)}')
        for b in sorted(v, key=lambda b: -b['area_gidi'])[:8]:
            print(f"   {b['block']} {b['xy']} {b['street']} storeys G {b['g_storey_mean']} o {b['o_storey_mean']} "
                  f"3+ G {b['g_three']} o {b['o_three']} med G {b['g_med']} o {b['o_med']} small G {b['g_small']} "
                  f"shack {b['o_shack']} big G {b['g_big']} shed {b['o_shed']} shop {b['o_shop']} pl/ha {b['places_ha']}")
    sm = lambda key: round(float(np.median([b[key] for b in F if b[key] is not None])), 2)
    print(' medians over fit blocks:', {k: sm(k) for k in ('g_storey_mean', 'o_storey_mean', 'g_three', 'o_three',
                                                          'g_med', 'o_med', 'g_small', 'o_small', 'o_shack', 'o_shop')})


if __name__ == '__main__':
    main()
