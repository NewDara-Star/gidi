# Gidi's road cross-sections: one table, read by the generator, the bake (written into the data as "cross_sections"),
# the space checker and the 3D kit. Agreed with the owner on 15 Oct 2026 from real Food Gate (Google outlines against OSM
# centre lines: on residential streets a quarter of front buildings stand within 5 m of the centre line).
#
# Each side of the centre line, from the middle out: half the carriageway, then the gutter (the open drain), then the
# walkway, which is the only place poles, street lights, traffic lights, signs and bus stops stand. Then the building line:
# no building closer to the centre line than that, except inside a declared encroachment zone (market spill).
SECTIONS = {
    'lane':   {'carriageway': 3.0,  'gutter': 0.0, 'walkway': 0.0, 'building_line': 1.5},   # poles on the plot edge
    'street': {'carriageway': 5.0,  'gutter': 0.6, 'walkway': 0.8, 'building_line': 3.9},
    'main':   {'carriageway': 7.5,  'gutter': 0.8, 'walkway': 1.5, 'building_line': 6.1},
    'art':    {'carriageway': 14.0, 'gutter': 1.0, 'walkway': 2.0, 'building_line': 10.0},
    'exp':    {'carriageway': 30.0, 'gutter': 1.0, 'walkway': 2.0, 'building_line': 18.0},
}
SECTIONS['bridge'] = dict(SECTIONS['art'])

# Market streets (owner, 15 Oct 2026, from Mile 12, Oshodi, Idumota): traders take the walkways and part of the carriageway
# too, under umbrellas and on tables; the traffic squeezes through what is left. MARKET_CLEAR is the running lane kept clear
# down the middle: one lane on a street or a main road, one each way on an arterial. Expressways are never market streets.
MARKET_CLEAR = {'street': 3.0, 'main': 3.5, 'art': 7.0}


def half(kind):
    """Half the carriageway: the road surface each side of the centre line."""
    return SECTIONS[kind]['carriageway'] / 2


def walkway_band(kind):
    """(inner, outer) distance from the centre line of the walkway strip, where street furniture stands."""
    s = SECTIONS[kind]
    a = s['carriageway'] / 2 + s['gutter']
    return a, a + s['walkway']


def building_line(kind):
    return SECTIONS[kind]['building_line']
