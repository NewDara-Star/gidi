"""The draft desk: write a first draft of every record a spot's map needs (decisions, 22 Oct: one ground truth; KIT.md
section 12, "Records"). The old kit's seeded rules (gidi_kit/draft.py) run once on the map and what they choose goes
into it as full records; from then on the records are the map's, edited by hand, and the kit reads only them.
blender -b --factory-startup -P blender/kit_draft.py -- --map <spot>/map.json
The map is kept first as <spot>/map_seeded.json (unless that is there already); the ground grids go beside the map
(ground_<street id>.npz). Run it once per new spot, never on a map whose records were edited by hand: it overwrites them."""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gidi_kit import draft  # noqa: E402

args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = {}
for i, a in enumerate(args):
    if a.startswith('--'):
        opt[a] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('--') else True
path = opt['--map']
base = os.path.dirname(os.path.abspath(path))
keep = os.path.join(base, 'map_seeded.json')
if not os.path.exists(keep):
    shutil.copy(path, keep)
spot = json.load(open(path))
draft.spot(spot, base)
with open(path, 'w') as f:
    json.dump(spot, f, indent=1)
print('DRAFTED', path)
