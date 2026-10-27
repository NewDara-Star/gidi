"""Lagoon University (d18): the campus cut finer (building study, 27 Oct).

  ~/.venvs/gidi/bin/python -I docs/lagos-study/buildings/scripts/d18_campus.py --json out.json

d17_blocks.py d18 leaves the campus as four blocks of 0.29-0.99 km2: Overture's campus roads (residential and
service) end in the grounds and close few loops (adding service roads and tracks as dividers was tried, 27 Oct: 28
blocks instead of 23, the four big ones barely smaller). So this runs the same study (d17_blocks.study, unchanged)
with each block of SPLIT m2 or more cut into CELL x CELL real-metre squares on the UTM grid (pieces under
d17_blocks.MIN_BLOCK join the slivers, counted in the summary), so halls, faculties, staff housing and Iwaya's town
come apart. Everything else is d17_blocks.py's.
Then a zone draft per block (ZONE below, first rule that holds wins), from Overture land use and place names only:
  town          Overture land use residential named Iwaya over 40% of the block, or no university land use at all
  wetland edge  WorldCover mangrove + water + wetland over 30%
  hostel        a place named "... Hall" (not a lecture hall) / hostel / quadrangle, or land use "UNILAG New Hall"
  staff housing a place named "Quarters" / "Staff" / "Guest House", or Overture land use residential inside campus
  academic      faculty / department / library / senate / auditorium / college / school names
  campus        university land use over 40% with none of the above
Halls of residence are told from lecture halls by name only (a list below, from Overture's names); *not checked*
against the university's own list.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d17_blocks as B

from shapely.geometry import box

SPLIT = 100_000      # real m2
CELL = 200           # real m (67 m in Gidi)
_blocks_of = B.blocks_of


def blocks_of(ring_u, w, s, e, n):
    big, small, roads, rails, cut = _blocks_of(ring_u, w, s, e, n)
    out = []
    for p in big:
        if p.area < SPLIT:
            out.append(p)
            continue
        x0, y0, x1, y1 = p.bounds
        for i in range(int(x0 // CELL), int(x1 // CELL) + 1):
            for j in range(int(y0 // CELL), int(y1 // CELL) + 1):
                q = p.intersection(box(i * CELL, j * CELL, (i + 1) * CELL, (j + 1) * CELL))
                for g in getattr(q, 'geoms', [q]):
                    if g.geom_type != 'Polygon' or g.is_empty:
                        continue
                    (out if g.area >= B.MIN_BLOCK else small).append(g)
    out.sort(key=lambda p: (-round(p.centroid.y / 150), p.centroid.x))
    BLOCKS[:] = out
    SEGS[:] = [(r, g) for r, g in B.segments(B.OV + 'lagos_overture_segment.parquet', w, s, e, n,
                                             lambda r: r['subtype'] == 'road')]
    return out, small, roads, rails, cut


BLOCKS, SEGS = [], []


B.blocks_of = blocks_of

# streets whose houses are staff housing: detached houses and blocks of flats in green yards, by eye on Google Maps
# satellite with its street labels, 27 Oct (Kosoko Drive's cul-de-sacs; Ozolua Road with "Ozolua BQs"; Abdul Atta Road,
# Alvan Ikoku, College of Medicine Road; Ransome Kuti Road by the "Vice Chancellors Lodge" label; Abdul Karimu Street
# with "University Of Lagos High Rise Block B/C" labels). Not checked on Street View.
STAFF_STREETS = re.compile(r'(Kosoko|Ozolua|Abdul Atta|Alvan Ikoku|College of Medicine|Ransome|Abdul Karimu)', re.I)
HOSTEL = re.compile(r'(Jaja|Moremi|Amina|Fagunwa|Eni-Njoku|Mariere|Biobaku|Kofo|Tinubu|New Hall|Henry Carr|Akingbola|'
                    r'Makama|Sodeinde|El-Kanemi|Honours|hostel|quadrangle)', re.I)
STAFF = re.compile(r'(quarters|staff|guest house|guest houses)', re.I)
ACAD = re.compile(r'(faculty|department|library|senate|auditorium|college|school of|institute|centre|research|lecture)', re.I)


def streets_in(bk):
    """Named Overture streets running 20 m or more within 10 m of the block (the block itself excludes the street)."""
    out = []
    for r, g in SEGS:
        nm = (r['names'] or {}).get('primary')
        if nm and nm not in out and g.intersection(bk.buffer(10)).length >= 20:
            out.append(nm)
    return out


def zone(b):
    lu = [l for l in b['landuse'] if 'Pacific' not in str(l[3]) and l[2] != 'land']
    uni = sum(l[4] for l in lu if l[2] == 'university')
    iwaya = sum(l[4] for l in lu if l[2] == 'residential' and l[3] == 'Iwaya')
    wc = b['worldcover']
    wet = wc.get('mangrove', 0) + wc.get('water', 0) + wc.get('wetland', 0)
    names = [n for c, n in b['place_names']] + [str(l[3]) for l in lu]
    tags = []
    if b['n90'] == 0:
        tags.append('open ground')
    elif iwaya >= 0.4 or (uni < 0.4 and wet < 0.3):
        tags.append('town')
    if wet >= 0.3:
        tags.append('wetland edge')
    if any(HOSTEL.search(n) for n in names) or any(c == 'hostel' for c, n in b['place_names']):
        tags.append('hostel')
    if any(STAFF.search(n) for n in names) or any(l[2] == 'residential' and l[3] != 'Iwaya' and l[3] != 'UNILAG New Hall'
                                                for l in lu) or any(STAFF_STREETS.search(n) for n in b.get('streets', [])):
        tags.append('staff housing')
    if uni >= 0.4 and any(ACAD.search(n) for n in names):
        tags.append('academic')
    if not tags:
        tags.append('campus')
    return tags, round(uni, 2), round(iwaya, 2), round(wet, 2)


def main():
    out = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
    summary, rows = B.study('d18')
    for r, bk in zip(rows, BLOCKS):
        r['streets'] = streets_in(bk)
        r['block'] = r['block'].replace('D18-', 'D18c-')  # c: cut finer than d17_blocks.py's D18-nn
        t, u, i, w = zone(r)
        r['zone'] = t
        r['zone_shares'] = {'university_landuse': u, 'iwaya_landuse': i, 'wet': w}
        print(r['block'], r['centroid_gidi'], r['centroid_lonlat'], r['area_real_m2'], r['n90'], r['cover90'],
              r['median_m2'], r['median_h'], '/'.join(t), [n for c, n in r['place_names']][:8], r['streets'][:6])
    print(json.dumps({k: v for k, v in summary.items() if k != 'whole'}, default=str))
    if out:
        json.dump({'d18': {'summary': summary, 'blocks': rows}}, open(out, 'w'), ensure_ascii=False, indent=1, default=str)


if __name__ == '__main__':
    main()
