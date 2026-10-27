"""The block table for Lagoon University's (d18) building study, from d18_campus.py's JSON (27 Oct).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d18_campus.py --json x.json
  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d18_table.py x.json

Zone tags are d18_campus.zone()'s rule draft, or OVERRIDE below (by eye on Google Maps satellite with labels, 27 Oct,
study only). The primary zone (first of PRIORITY among a block's tags) picks the kinds column. Town blocks take
d17_fabric.fabric()'s rule draft for their fabric.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_fabric as F

OVERRIDE = {
    'D18c-09': ['campus'], 'D18c-10': ['campus'], 'D18c-17': ['campus'],
    # outside Overture's university polygon but inside the campus by Google Maps' labels round them (FBA Walkway,
    # Zenith Bank Drive, Faculty of Law, by eye)
    'D18c-126': ['town', 'wetland edge'],
    # by eye: Iwaya's side of the creek, small roofs and cleared ground; the creek between it and D18c-127
    'D18c-127': ['staff housing'],
    # by eye: "University Of Lagos High Rise Block B / Block C" labels on Abdul Karimu Street, blocks in green ground
}
FABRIC = {'D18c-126': ('shacks and rooms on cleared ground by the creek, by eye (median 32 m², 1 storey)',
                     'shack (home), face_me_bungalow (home)')}
PRIORITY = ['town', 'hostel', 'staff housing', 'academic', 'campus', 'wetland edge', 'open ground']
KINDS = {
    'hostel': 'walkup (flats) as hall blocks *guess* (no hall kind)',
    'staff housing': 'colonial_house or compound_house (home), detached in yards *guess*; walkup (flats) for the high-rise blocks',
    'academic': 'school (faculty blocks), shed (halls) *guess*',
    'campus': 'school, open ground',
    'wetland edge': 'none (mangrove, grass, water)',
    'open ground': 'none',
}


CAMPUS_CATS = {'campus_building', 'hostel', 'lodging', 'auditorium', 'library', 'palace', 'gas_station',
               'bank_or_credit_union', 'shopping_mall', 'stadium_arena', 'fire_station', 'radio_station', 'hotel',
               'college_university', 'religious_organization'}


def named(b):
    """Overture names worth naming: d17_fabric's categories, the campus's, and any hall / staff / faculty name."""
    import d18_campus as C
    out = [l[3] for l in b['landuse'] if l[3] and l[2] not in ('land', 'university', 'residential')
           and 'Pacific' not in str(l[3])]
    for cat, nm in b['place_names']:
        if nm in out:
            continue
        if cat in F.NAMED_CATS or cat in CAMPUS_CATS or C.HOSTEL.search(nm) or C.STAFF.search(nm) or C.ACAD.search(nm):
            out.append(nm)
    return out


def tags(b):
    return OVERRIDE.get(b['block'], b['zone'])


def primary(b):
    t = tags(b)
    return next(p for p in PRIORITY if p in t)


def kinds(b):
    p = primary(b)
    if b['block'] in FABRIC:
        return FABRIC[b['block']]
    if p == 'town':
        f, k = F.fabric(b)
        return f, k
    return '', KINDS[p]


def main():
    R = json.load(open(sys.argv[1]))['d18']
    B = R['blocks']
    print('| block | centroid (Gidi x, y) | lon, lat | real area m² | houses (90%) | per ha | cover | median m² (largest) | '
          'height; storeys 1/2/3/4+ | zone (rule; *hand*) | fabric (town: rule draft) and map kinds | named (Overture) | '
          'streets (Overture) | ours: houses, cover, under our roads |')
    print('|' + '---|' * 14)
    for b in B:
        f, k = kinds(b)
        nm = named(b)
        nm = '; '.join(nm[:6]) + (f' (+{len(nm) - 6})' if len(nm) > 6 else '') if nm else ''
        z = '/'.join(tags(b)) + (' *hand*' if b['block'] in OVERRIDE else '')
        st = ', '.join(b['streets'][:4])
        print(f"| {b['block']} | {b['centroid_gidi'][0]}, {b['centroid_gidi'][1]} | {b['centroid_lonlat'][0]}, "
              f"{b['centroid_lonlat'][1]} | {b['area_real_m2']:,} | {b['n90']} | {b['per_ha']} | {b['cover90']:.0%} | "
              f"{b['median_m2'] or '-'} ({b['max_m2'] or '-'}) | {F.st(b)} | {z} | {(f + ': ') if f else ''}{k} | {nm} | "
              f"{st} | {b['ours_n']}, {b['ours_cover']:.0%}, {b['ours_carriageway_share']:.0%} |")
    print()
    print('| zone (primary) | blocks | real km² | Google buildings (90%) | Google cover | median m² (block medians) | '
          'ours: houses | ours: cover |')
    print('|---|---|---|---|---|---|---|---|')
    for p in PRIORITY:
        bs = [b for b in B if primary(b) == p]
        if not bs:
            continue
        a = sum(b['area_real_m2'] for b in bs)
        ag = sum(b['area_gidi_m2'] for b in bs)
        cov = sum(b['cover90'] * b['area_real_m2'] for b in bs) / a
        ours = sum(b['ours_cover'] * b['area_gidi_m2'] for b in bs) / ag
        meds = sorted(b['median_m2'] for b in bs if b['median_m2'])
        med = meds[len(meds) // 2] if meds else '-'
        print(f"| {p} | {len(bs)} | {a / 1e6:.2f} | {sum(b['n90'] for b in bs)} | {cov:.1%} | {med} | "
              f"{sum(b['ours_n'] for b in bs)} | {ours:.1%} |")
    print()
    for p in PRIORITY:
        k = collections.Counter()
        st = collections.Counter()
        for b in B:
            if primary(b) == p:
                k.update(b['ours_kinds'])
                st.update({x: v for x, v in b['storeys'].items()})
        print(f'- {p}: ours {dict(k.most_common())}; Google storeys {dict(sorted(st.items(), key=lambda t: int(t[0])))}')
    print()
    print('Furthest below (Google 90% cover x block area in Gidi m², less our roof area there):')
    short = sorted(B, key=lambda b: -(b['cover90'] - b['ours_cover']) * b['area_gidi_m2'])
    for b in short[:12]:
        print(f"- {b['block']} ({primary(b)}) at {b['centroid_gidi'][0]}, {b['centroid_gidi'][1]}: Google "
              f"{b['cover90']:.0%}, ours {b['ours_cover']:.0%} ({b['ours_n']} houses against {b['n90']} real, about "
              f"{b['n90'] / 9:.0f} at 1:3), {(b['cover90'] - b['ours_cover']) * b['area_gidi_m2']:,.0f} m² of roof short")
    print()
    print('Town fabric (rule draft):', collections.Counter(kinds(b)[0].split(':')[0].split(',')[0] for b in B if primary(b) == 'town'))


if __name__ == '__main__':
    main()
