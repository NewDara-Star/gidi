"""Named landmarks: a place on the map that needs a model of its own, by its name.

When a district brings a named landmark (a civic plot of type 'landmark', or a place the 3D audit
flags), give it a builder here. Until then it is built as a plain civic hall, never as something
else's model, and scripts/audit3d.py lists it under M3 until it has an entry.
"""
from . import places

# name -> builder(a, rng, collection), the same shape as the civic plot builders
BY_NAME = {
    'The Palace': places.palace,
}


def build(a, rng, collection=None):
    return BY_NAME.get(a.get('label'), places.hall)(a, rng, collection)
