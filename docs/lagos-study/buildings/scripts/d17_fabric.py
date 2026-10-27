"""The block table for a district's building study, from d17_blocks.py's JSON (building study, 27 Oct).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d17_blocks.py d17 --json /tmp/x.json
  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d17_fabric.py /tmp/x.json d17

The fabric column is a RULE DRAFT from the numbers (FABRIC below, first rule that holds wins), read against the
satellite by eye only where the study file says so. Kinds are the map's house kinds (docs/MAP-FORMAT.md, building
`kind` and `ground_floor`) the fabric would take.
"""
import json
import sys

NAMED_CATS = {'school', 'high_school', 'elementary_school', 'preschool', 'college_university', 'education', 'hospital',
              'christian_place_of_worship', 'muslim_place_of_worship', 'mosque', 'church_cathedral', 'market',
              'shopping_center', 'manufacturer', 'factory', 'commercial_industrial', 'government_office',
              'police_station', 'military', 'bus_station', 'train_station', 'stadium_arena', 'hotel', 'cemetery',
              'industrial_equipment_manufacturer', 'warehouse'}
SKIP_LU = ('Pacific Islands Heritage', )   # a mis-placed Overture polygon covering the whole box
INST = {'school': 'school ground', 'college': 'college campus', 'university': 'college campus',
        'hospital': 'hospital compound', 'military': 'barracks', 'grave_yard': 'cemetery', 'cemetery': 'cemetery',
        'railway': 'railway land', 'commercial': 'market and shops', 'retail': 'market and shops',
        'industrial': 'sheds and factories', 'wetland': 'open ground (wetland)'}


# by hand, where the satellite and Google Maps' labels (looked at 27 Oct, study only) show the rule draft wrong
OVERRIDE = {
    'D17-49': ('hospital compound: Military Hospital Yaba (Google Maps label; Overture place "Military Hospital"), '
               'with Mainland Hospital and the state infectious diseases isolation centre (Google Maps labels): '
               'separate low blocks in green ground, by eye', 'walkup (wards) *guess*, shed (halls) *guess*'),
    'D17-91': ('cemetery: Atan Cemetery Yaba (Google Maps label; Overture land use grave_yard, unnamed)',
               'none (open ground)'),
    'D17-103': ('barracks and compound houses: streets labelled "An Barrack" on Google Maps, long barrack blocks by '
                'eye east of Harvey Road; Overture places military_site and 2 courthouses',
                'walkup (barrack blocks), compound_house (home)'),
    'D17-81': ('yard and sheds: a large open lot packed with small white objects (cars or stalls, not told apart by eye '
               'at z17) beside long sheds, on Overture commercial land use (88%), unnamed; Lagos Presbyterian Church '
               'at its south edge (Google Maps label)', 'shed (workshop), kiosk_row; a yard plot *guess*'),
    'D19-31': ('split by grain, see "Land or water: the data": the stilt town over water in the south-east, land compounds '
               'in the north-west', 'shack (home) on the water; compound_house, face_me_bungalow on land'),
}


def landuse(b):
    return [l for l in b['landuse'] if l[2] != 'land' and not any(s in str(l[3]) for s in SKIP_LU)]


def fabric(b):
    """(fabric, kinds) from the block's numbers: the rule draft, or the hand override above."""
    if b['block'] in OVERRIDE:
        return OVERRIDE[b['block']]
    n, cov, med, mh = b['n90'], b['cover90'], b['median_m2'] or 0, b['median_h'] or 0
    big = b['n_over_500m2'] / n if n else 0
    small = b['n_under_40m2'] / n if n else 0
    ha = b['area_real_m2'] / 1e4
    for l in landuse(b):
        if l[4] >= 0.4 and l[2] in INST:
            f = INST[l[2]]
            k = {'school ground': 'school', 'college campus': 'school (halls), walkup (hostels)',
                 'hospital compound': 'walkup (wards) *guess*', 'barracks': 'walkup, compound_house',
                 'cemetery': 'none (open ground)', 'railway land': 'shed, station_hall',
                 'market and shops': 'market_block (open_stalls, cage_stalls), shop_under_flats (lock_ups)',
                 'sheds and factories': 'shed (workshop)', 'open ground (wetland)': 'shack (home) at the edge'}[f]
            return f + (f': {l[3]}' if l[3] else ''), k
    if cov < 0.12:
        return 'open ground, few houses', 'compound_house (home), shack'
    if b.get('stilts'):
        return 'shacks on stilts over water', 'shack (home)'
    if small >= 0.35 and med < 60:
        return 'shacks and rooms on land, very dense', 'shack (home), face_me_bungalow (home)'
    if med >= 300 or big >= 0.25:
        return 'big roofs: sheds, halls or institution blocks', 'shed (workshop), walkup (flats)'
    if mh >= 7.5:
        return 'walk-up flats (3 storeys and up)', 'walkup (flats), shop_under_flats (lock_ups) on the fronts'
    if b['places'] / ha >= 8:
        return 'compound houses, shops on the fronts', 'compound_house (home), shop_under_flats (lock_ups), kiosk_row'
    if cov < 0.3:
        return 'compound houses, loose (yards, open plots)', 'compound_house (home), face_me_bungalow (home)'
    if mh < 4.5:
        return 'bungalows: face-me-I-face-you and compounds, 1 storey', 'face_me_bungalow (home), compound_house (home)'
    return 'compound houses, 2 storeys, packed', 'compound_house (home), face_me_bungalow (home)'


def named(b):
    out = []
    for l in landuse(b):
        if l[3] and l[2] not in ('residential',) and l[3] not in out:
            out.append(l[3])
    for cat, nm in b['place_names']:
        if cat in NAMED_CATS and nm not in out:
            out.append(nm)
    return out


def st(b):
    s = b['storeys']
    four = sum(v for k, v in s.items() if int(k) >= 4)
    return f"{b['median_h'] or '-'} m; {s.get('1', 0)}/{s.get('2', 0)}/{s.get('3', 0)}/{four}"


def main():
    R = json.load(open(sys.argv[1]))[sys.argv[2]]
    print('| block | centroid (Gidi x, y) | real area m² | houses (90%) | per ha | cover | median m² (largest) | '
          'height; storeys 1/2/3/4+ | fabric (rule draft) | map kinds (ground floor) | named (Overture) | '
          'ours: houses, cover, under our roads |')
    print('|' + '---|' * 12)
    for b in R['blocks']:
        f, k = fabric(b)
        nm = named(b)
        nm = '; '.join(nm[:4]) + (f' (+{len(nm) - 4})' if len(nm) > 4 else '') if nm else ''
        print(f"| {b['block']} | {b['centroid_gidi'][0]}, {b['centroid_gidi'][1]} | {b['area_real_m2']:,} | {b['n90']} | "
              f"{b['per_ha']} | {b['cover90']:.0%} | {b['median_m2']} ({b['max_m2']}) | {st(b)} | {f} | {k} | {nm} | "
              f"{b['ours_n']}, {b['ours_cover']:.0%}, {b['ours_carriageway_share']:.0%} |")
    import collections
    print()
    print('Furthest below (Google 90% cover x block area in Gidi m2, less our roof area there):')
    short = sorted(R['blocks'], key=lambda b: -(b['cover90'] - b['ours_cover']) * b['area_gidi_m2'])
    for b in short[:12]:
        print(f"- {b['block']} at {b['centroid_gidi'][0]}, {b['centroid_gidi'][1]}: Google {b['cover90']:.0%}, ours "
              f"{b['ours_cover']:.0%} ({b['ours_n']} houses against Google's {b['n90']} real at 1:3, so about "
              f"{b['n90'] / 9:.0f} at Gidi's scale), {(b['cover90'] - b['ours_cover']) * b['area_gidi_m2']:,.0f} m² of roof short")
    print()
    c = collections.Counter(fabric(b)[0].split(':')[0] for b in R['blocks'])
    a = collections.Counter()
    for b in R['blocks']:
        a[fabric(b)[0].split(':')[0]] += b['area_real_m2']
    print()
    for f, v in c.most_common():
        print(f'- {f}: {v} blocks, {a[f] / 1e6:.2f} km² real')


if __name__ == '__main__':
    main()
