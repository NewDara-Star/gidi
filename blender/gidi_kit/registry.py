"""Which builder makes which thing in the data. generate.py and coverage.py both read this.

Keys are the data's own names: building kinds (web/gen-*.json 'buildings'), parcel kinds,
structure kinds and civic types (web/civic.json). A value of None means: not modelled yet.
"""
from . import archetypes, kinds

BUILDINGS = {
    'front': archetypes.house, 'back': archetypes.house, 'shed': archetypes.house,
    'stalls': archetypes.stall, 'kiosk': archetypes.kiosk,
    'stilt': kinds.stilt, 'raft': kinds.raft, 'sawdust': kinds.sawdust, 'brazilian house': kinds.brazilian,
    'gatehouse': kinds.gatehouse, 'generator': kinds.generator, 'water tank': kinds.water_tank,
    'stack': kinds.stack, 'trailer': kinds.trailer, 'container': kinds.container_shop,
    'pen': kinds.pen, 'scrap': kinds.scrap, 'checkpoint': kinds.checkpoint, 'mound': kinds.mound,
}
PARCELS = {}
STRUCTURES = {}
CIVIC = {}


def builder(kind):
    return BUILDINGS.get(kind)
