"""A district's first draft of each house's look, by its house type: storey heights, roof, walls, windows, outside stair, wear.

  ~/.venvs/gidi/bin/python scripts/draft_looks.py map/d15 [--dry]

Step 4 of "Finish the map's first layer first" (DECISIONS, 24 Oct): the house types are written as rules that draft each
house's fields into its records; once drafted the records are the truth and are hand-edited. The industry's way: City
Sample's buildings come from building types and PCG rules, and footprint tools (Esri CityEngine's CGA) build each
footprint from its attributes by its type's rule.

The types and their shares come from the dense old town Street View study (~/gidi-data/research/google/kits/old-town/
KIT.md: 199 shots, about 32 in Mushin; sections 1 "House types" and 11 "Colour palette"):
- face-me bungalow: a low hip roof of rusty zinc with deep eaves (1-2 m), some long-span sheet in grey, green or pale
  orange, a few dark tiles; render in faded colours, often a darker band about 1 m high at the bottom; timber louvre or
  plank shutters, sometimes barred;
- walk-up and shop-under-flats: at 2-3 storeys a hip roof of zinc or long-span with deep eaves, at 3-6 a flat roof with a
  parapet; render in strong or faded colours, some brick- or stone-look tiles; louvre windows in plain frames, mostly
  barred; an outside stair on the front in about 7% of shots;
- compound house: 1-3 storeys behind a wall (the wall is a frontage record, not drawn here);
- shacks, kiosks and sheds: zinc or long-span sheet, plank shutters.
Colours are named in KIT.md; the hex values below are faded tones of those names, matched to the example records
(docs/map-format-example). Each house draws from its type's shares with its own id as the seed, so a re-run gives the
same draft.

Written only on houses that have a kind and storeys and none of storey_h, roof, finish, windows, outside_stair and wear
("Rules draft, records rule": a house with any of them set is a hand-edited house and is left alone).
"""
import hashlib
import json
import random
import sys

WALLS = [('#d8ccb0', 14), ('#e2ddd0', 11), ('#a3a29b', 14), ('#8e4a3e', 7), ('#6e3438', 5), ('#d49a86', 4),
         ('#d8a3a6', 4), ('#dcb08f', 4), ('#a9bfc9', 9), ('#9cb57e', 5), ('#a9b096', 4), ('#d9c27a', 4),
         ('#c4a24a', 4), ('#cf7f45', 6), ('#7f6046', 5)]                  # KIT.md 11, most to least common
RUST = ['#7c5c4b', '#6f5446', '#80553d', '#6a4a3b']
LONGSPAN = ['#7d8288', '#5f7a5a', '#4f6b8a', '#c98a5a', '#b9a888']         # grey, green, blue, pale orange, beige (B1)
SILVER, TILE, SLAB = '#a7a9a6', '#4a3a34', '#8f8c86'


def pick(rnd, opts):
    return rnd.choices([o for o, _ in opts], [w for _, w in opts])[0]


def darker(hexc, f=0.78):
    return '#' + ''.join(f'{int(int(hexc[i:i + 2], 16) * f):02x}' for i in (1, 3, 5))


def roof(rnd, kind, storeys):
    if kind in ('shack', 'kiosk_row'):
        return {'form': 'mono', 'material': 'zinc', 'state': 'rusty', 'colour': rnd.choice(RUST),
                'pitch': rnd.randint(8, 12), 'eave': round(rnd.uniform(0.2, 0.5), 1)}
    if kind == 'shed':
        m = pick(rnd, [('longspan', 70), ('zinc', 30)])
        return {'form': 'gable', 'material': m, 'state': 'silver' if m == 'longspan' else 'rusty',
                'colour': SILVER if m == 'longspan' else rnd.choice(RUST), 'pitch': rnd.randint(8, 12), 'eave': 0.5}
    if storeys >= 3 and rnd.random() < (0.45 if storeys == 3 else 0.8):
        return {'form': 'flat', 'material': 'slab', 'state': 'painted', 'colour': SLAB, 'pitch': 0, 'eave': 0,
                'parapet_h': round(rnd.uniform(0.6, 1.0), 1)}
    if kind == 'face_me_bungalow':
        s = pick(rnd, [('zinc_rusty', 80), ('zinc_silver', 5), ('longspan', 12), ('tile', 3)])
        eave = round(rnd.uniform(1.0, 2.0), 1)
    else:
        s = pick(rnd, [('zinc_rusty', 50), ('zinc_silver', 10), ('longspan', 35), ('gable_zinc', 5)])
        eave = round(rnd.uniform(0.6, 1.2), 1)
    r = {'form': 'gable' if s == 'gable_zinc' else 'hip', 'pitch': rnd.randint(12, 18), 'eave': eave}
    if s in ('zinc_rusty', 'gable_zinc'):
        r.update(material='zinc', state='rusty', colour=rnd.choice(RUST))
    elif s == 'zinc_silver':
        r.update(material='zinc', state='silver', colour=SILVER)
    elif s == 'longspan':
        r.update(material='longspan', state='painted', colour=rnd.choice(LONGSPAN), pitch=rnd.randint(10, 15))
    else:
        r.update(material='tile', state='new', colour=TILE)
    return r


def finish(rnd, kind):
    if kind in ('shack', 'kiosk_row', 'shed'):
        k = pick(rnd, [('bare_block', 50), ('render', 50)])
        return {'kind': k, 'colour': '#9a958c' if k == 'bare_block' else pick(rnd, WALLS)}
    k = pick(rnd, [('render', 85), ('bare_block', 8), ('tile_brick', 4), ('tile_stone', 3)])
    c = '#9a958c' if k == 'bare_block' else '#9b5a45' if k == 'tile_brick' else '#b8ad9a' if k == 'tile_stone' else pick(rnd, WALLS)
    f = {'kind': k, 'colour': c}
    if k == 'render' and rnd.random() < (0.6 if kind == 'face_me_bungalow' else 0.35):
        f['base_band'] = {'colour': darker(c), 'h': round(rnd.uniform(0.8, 1.1), 1)}
    if k == 'render' and kind in ('walkup', 'shop_under_flats') and rnd.random() < 0.3:
        f['storey_bands'] = '#e6e6e2'
    return f


def windows(rnd, kind):
    if kind in ('shack', 'kiosk_row', 'shed'):
        return {'kind': 'plank_shutter', 'shutter_colour': pick(rnd, [('#5a4a3e', 3), ('#3f5a43', 1), ('#5b3a32', 1)]),
                'bars': 'none'}
    if kind == 'face_me_bungalow':
        k = pick(rnd, [('louvre_timber', 40), ('plank_shutter', 30), ('louvre_glass', 20), ('casement', 10)])
        bars = pick(rnd, [('none', 55), ('vertical', 35), ('grid', 10)])
    else:
        k = pick(rnd, [('louvre_glass', 60), ('casement', 20), ('louvre_timber', 20)])
        bars = pick(rnd, [('vertical', 50), ('none', 20), ('grid', 15), ('scroll', 10), ('sunray', 5)])
    w = {'kind': k, 'bars': bars}
    if k == 'plank_shutter':
        w['shutter_colour'] = pick(rnd, [('#5a4a3e', 3), ('#3f5a43', 1), ('#5b3a32', 1)])
    if bars != 'none':
        w['bar_colour'] = '#e8e6e0' if bars in ('scroll', 'sunray') and rnd.random() < 0.5 else '#262626'
    return w


def storey_h(rnd, kind, storeys):
    if kind in ('shack', 'kiosk_row'):
        return [round(rnd.uniform(2.3, 2.7), 1)] * storeys
    if kind == 'shed':
        return [round(rnd.uniform(4.5, 6.0), 1)] + [3.0] * (storeys - 1)
    g = rnd.uniform(3.4, 3.8) if kind == 'shop_under_flats' else rnd.uniform(3.2, 3.6) if kind == 'face_me_bungalow' else rnd.uniform(3.0, 3.3)
    return [round(g, 1)] + [round(rnd.uniform(2.8, 3.1), 1) for _ in range(storeys - 1)]


def stair(rnd, kind, storeys):
    if storeys < 2 or kind in ('shack', 'kiosk_row', 'shed'):
        return 'none'
    return pick(rnd, [('none', 93), ('front_concrete', 5), ('front_steel', 2)])


LOOK = ('storey_h', 'roof', 'finish', 'windows', 'outside_stair', 'wear')


def main():
    pf = sys.argv[1].rstrip('/') + '/plan.json'
    plan = json.load(open(pf))
    n, skip, roofs = {}, 0, {}
    for r in plan['records']:
        if r['type'] != 'building':
            continue
        if 'kind' not in r or 'storeys' not in r or any(k in r for k in LOOK):
            skip += 1
            continue
        rnd = random.Random(int(hashlib.sha1(r['id'].encode()).hexdigest()[:12], 16))
        k, s = r['kind'], r['storeys']
        r['storey_h'] = storey_h(rnd, k, s)
        r['roof'] = roof(rnd, k, s)
        r['finish'] = finish(rnd, k)
        r['windows'] = windows(rnd, k)
        r['outside_stair'] = stair(rnd, k, s)
        r['wear'] = round(rnd.uniform(0.4, 0.9), 2)
        n[k] = n.get(k, 0) + 1
        rk = f"{r['roof']['form']} {r['roof']['material']} {r['roof']['state']}"
        roofs[rk] = roofs.get(rk, 0) + 1
    print('houses by type:', dict(sorted(n.items(), key=lambda t: -t[1])))
    print('roofs:', dict(sorted(roofs.items(), key=lambda t: -t[1])))
    print(f'{sum(n.values())} drafted; {skip} left (no kind or storeys, or a look field already set)')
    if '--dry' not in sys.argv:
        json.dump(plan, open(pf, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
