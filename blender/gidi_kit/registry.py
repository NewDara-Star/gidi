"""Which builder makes which thing in the data. generate.py and coverage.py both read this.

Keys are the data's own names: building kinds (web/gen-*.json 'buildings'), parcel kinds,
structure kinds and civic types (web/civic.json). A value of None means: not modelled yet.
"""
from . import archetypes, kinds, places

BUILDINGS = {
    'front': archetypes.house, 'back': archetypes.house, 'shed': archetypes.house,
    'stalls': archetypes.stall, 'kiosk': archetypes.kiosk,
    'stilt': kinds.stilt, 'raft': kinds.raft, 'sawdust': kinds.sawdust, 'brazilian house': kinds.brazilian,
    'gatehouse': kinds.gatehouse, 'generator': kinds.generator, 'water tank': kinds.water_tank,
    'stack': kinds.stack, 'trailer': kinds.trailer, 'container': kinds.container_shop,
    'pen': kinds.pen, 'scrap': kinds.scrap, 'checkpoint': kinds.checkpoint, 'mound': kinds.mound,
    'barracks': places.barracks, 'cellblock': places.cellblock, 'phone mall': places.phone_mall, 'plaza': places.plaza,
    'unfinished': places.unfinished_plaza, 'strip': places.strip, 'bakery': places.bakery, 'print': places.print_shop,
    'warehouse': places.warehouse, 'works': places.works, 'tank': places.tank, 'crane': places.crane,
    'flats': places.flats, 'villa': places.villa, 'mansion': places.mansion, 'apartment tower': places.tower,
    'bank tower': places.bank_tower, 'office': places.office, 'school': places.school, 'hotel': places.hotel,
    'nightclub': places.nightclub, 'stands': places.stands, 'terminal': places.terminal, 'station': places.station,
    'toll booth': places.toll_booth, 'tower': places.cctv_tower, 'transformer': places.transformer_kind,
    'stage': places.stage, 'canopy': places.canopy, 'bust': places.bust, 'palace': places.palace,
    'stilt bar': places.stilt_bar, 'saw shed': places.saw_shed, 'hall': places.hall, 'clubhouse': places.clubhouse,
    'studio': places.studio, 'cafe': places.cafe,
}
# civic places in web/gidi-data.js 'safe_ground' (each with its own plot and name)
CIVIC_PLOTS = {
    'church': places.church, 'mosque': places.mosque, 'school': places.school, 'clinic': places.clinic,
    'hospital': places.clinic, 'landmark': places.palace,
}
PARCELS = {}
STRUCTURES = {}
CIVIC = {}


def builder(kind):
    return BUILDINGS.get(kind)
