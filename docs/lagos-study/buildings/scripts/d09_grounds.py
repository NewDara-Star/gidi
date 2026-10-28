"""Ayégúnlẹ̀ (d09) building study, the parts d17_blocks.py does not cover (building-study agent, 28 Oct).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d17_blocks.py d09 --json X.json
  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d09_grounds.py X.json

1. Overture's named and special grounds in d09 (wetland, scrub, military, industrial, retail, cemetery, school, wood):
   per class, the real area inside the outline, Google Open Buildings at the tile's 90% threshold inside it (count with
   centroid in, cover = footprint union clipped over the ground's area), WorldCover classes, and our houses' cover of
   the same ground taken to Gidi metres.
2. The "empty band" BUILDINGS.md hand pass 4 names (Gidi x 11,500-12,450, y 8,440-8,570): Google cover and count in it,
   ours, WorldCover.
3. The fabric table again, through d17_fabric's rule, with one d09 change (FIX_WETLAND below): Overture's wetland
   land use is NOT taken as the block's fabric where the block is built (WorldCover built >= 0.85 and Google cover
   >= 0.30): there the wetland polygon lies over houses, so it is dropped and the rest of the rule decides. Then the
   d09 hand labels (OVERRIDE09; each says what it rests on, *guess* where it is one).
"""
import collections
import json
import os
import sys

import numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely.strtree import STRtree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B   # noqa: E402
import d17_fabric as F   # noqa: E402

BAND = (11500, 8440, 12450, 8570)   # Gidi metres, from map/d09/BUILDINGS.md hand pass 4
KEEP = {'wetland', 'scrub', 'military', 'industrial', 'retail', 'cemetery', 'school', 'wood', 'construction'}

# d09 hand labels: looked at on Google Maps satellite and labels (study only) where the note says so
OVERRIDE09 = {
    'D09-129': ('split: Signals Barracks (Google Maps label "Nigeria Army Signal Barracks", Overture military 33%) and '
                'green wet ground with trees west of where Canal Rd ends, a grey open lot beside it (by eye, z17, 28 Oct); '
                'packed compound houses east along the canal; Overture has few streets here, so it is one "block"',
                'none (open ground, barracks ground) in the west; walkup (barrack blocks) *guess*; compound_house, '
                'face_me_bungalow (home) in the east'),
    'D09-201': ('split: the Julius Berger yard by the Oworonshoki-Apapa Expressway (Google Maps label; Overture '
                'industrial 41%): bare dusty ground and long sheds, by eye; a canal with houses to its banks (James '
                'Igbe St); packed compound houses south of it (by eye, z17, 28 Oct)',
                'shed (workshop), yard plot in the north-west; compound_house, face_me_bungalow (home) elsewhere'),
    'D09-353': ('school grounds and playing fields: Maracana Stadium and playing field, Reservation Secondary, Olodi-'
                'Apapa Junior Secondary, Mokoya Senior High, Bola Ige Millennium Model School, Odion Ighalo Stadium '
                '(Google Maps labels): long blue-roofed classroom blocks on open ground by the creek (by eye, z17, '
                '28 Oct). Its 69 readings of 4+ storeys are blur (BUILDINGS.md hand pass 2 checked six here)',
                'school (halls), school_ground plots; open_ground (pitches)'),
    'D09-331': ('long rooming houses, packed: deep narrow plots with long rusty roofs end-on to the street, some 2-3 '
                'storey (Olodi-Apapa, by eye at z18, 28 Oct); "big roofs" by the rule only because the median '
                'footprint is 352 m2', 'face_me_bungalow (home), compound_house (home), walkup (flats) a few'),
    'D09-17': ('compound houses, 2 storeys, packed, along a canal: a dark channel runs east-west through it (Amukoko, '
               'by eye at z17, 28 Oct); Overture has no streets through it, so it is several real blocks',
               'compound_house (home), face_me_bungalow (home)'),
}


def grounds(js):
    D, recs, ring_g, ring_u = B.load('d09')
    w, s, e, n = B.lonlat_box(ring_u)
    t90 = js['summary']['t90']
    G = [g for c, g in B.google(w, s, e, n) if c >= t90 and ring_u.intersects(g)]
    gtree = STRtree([g.centroid for g in G])
    houses = [Polygon(r['footprint']) for r in recs if r['type'] == 'building']
    OU = unary_union(houses)
    LU = [l for l in B.landuse(w, s, e, n) if l[4].intersects(ring_u) and l[2] in KEEP
          and 'Pacific' not in str(l[3])]
    by = collections.defaultdict(list)
    for src, sub, cl, nm, g in LU:
        by[(cl, nm)].append(g.intersection(ring_u))
    items = [(k, unary_union(v)) for k, v in by.items()]
    band_g = box(*BAND)
    band_u = B.shapely.transform(band_g, lambda a: np.column_stack(B.g2u(a[:, 0], a[:, 1])))
    items.append((('BAND (BUILDINGS.md hand pass 4)', None), band_u.intersection(ring_u)))
    wc, _ = B.worldcover([g for k, g in items])
    print('| ground (Overture class, name) | real m² in d09 | Google 90%: count, cover, median m² | WorldCover | '
          'ours: houses, cover |')
    print('|---|---|---|---|---|')
    for (k, g), c in sorted(zip(items, wc), key=lambda t: -t[0][1].area):
        if g.area < 1500:
            continue
        idx = [i for i in gtree.query(g) if g.contains(G[i].centroid)]
        cov = unary_union([G[i] for i in idx]).intersection(g).area / g.area if idx else 0
        med = float(np.median([G[i].area for i in idx])) if idx else 0
        gg = B.utm_to_gidi(g)
        nh = sum(1 for p in houses if gg.contains(p.centroid))
        tot = sum(c.values()) or 1
        wcs = ', '.join(f'{a} {v / tot:.0%}' for a, v in c.most_common(3))
        print(f'| {k[0]}{", " + k[1] if k[1] else ""} | {g.area:,.0f} | {len(idx)}, {cov:.0%}, {med:.0f} | {wcs} | '
              f'{nh}, {OU.intersection(gg).area / gg.area:.0%} |')


def fix(b):
    built = b['worldcover'].get('built', 0)
    if built >= 0.85 and b['cover90'] >= 0.30:
        b = dict(b, landuse=[l for l in b['landuse'] if l[2] != 'wetland'])
    return b


def fabric(b):
    if b['block'] in OVERRIDE09:
        return OVERRIDE09[b['block']]
    return F.fabric(fix(b))


def table(js):
    print('| block | centroid (Gidi x, y) | real area m² | houses (90%) | per ha | cover | median m² (largest) | '
          'height; storeys 1/2/3/4+ | fabric (rule draft) | map kinds (ground floor) | named (Overture) | '
          'ours: houses, cover, under our roads |')
    print('|' + '---|' * 12)
    for b in js['blocks']:
        f, k = fabric(b)
        nm = F.named(b)
        nm = '; '.join(nm[:4]) + (f' (+{len(nm) - 4})' if len(nm) > 4 else '') if nm else ''
        print(f"| {b['block']} | {b['centroid_gidi'][0]}, {b['centroid_gidi'][1]} | {b['area_real_m2']:,} | {b['n90']} | "
              f"{b['per_ha']} | {b['cover90']:.0%} | {b['median_m2']} ({b['max_m2']}) | {F.st(b)} | {f} | {k} | {nm} | "
              f"{b['ours_n']}, {b['ours_cover']:.0%}, {b['ours_carriageway_share']:.0%} |")
    print()
    c, a, n = collections.Counter(), collections.Counter(), collections.Counter()
    for b in js['blocks']:
        f = fabric(b)[0].split(':')[0]
        c[f] += 1
        a[f] += b['area_real_m2']
        n[f] += b['n90']
    for f, v in c.most_common():
        print(f'- {f}: {v} blocks, {a[f] / 1e6:.2f} km² real, {n[f]:,} Google buildings')
    changed = [b['block'] for b in js['blocks'] if F.fabric(b) != fabric(b)]
    print(f'\nblocks whose label the wetland fix or a hand label changed: {len(changed)}: {", ".join(changed)}')


if __name__ == '__main__':
    js = json.load(open(sys.argv[1]))['d09']
    if '--table' in sys.argv:
        table(js)
    else:
        grounds(js)
