# 3D audit: Old Shore

`.venv/bin/python scripts/audit3d.py oldshore` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 4**
  - street oldshore/street/67 runs 33 m along main Lateef Road at (6517, 1241)
  - street oldshore/street/90 runs 25 m along street oldshore/street/91 at (6891, 1070)
  - street oldshore/street/20 runs 24 m along street oldshore/street/28 at (5502, 1397)
  - street oldshore/street/28 runs 22 m along street oldshore/street/30 at (5516, 1449)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 5**
  - street oldshore/street/45 runs 11.2 m past street oldshore/street/46 at (5913, 858)
  - art art/8 runs 5.5 m past street oldshore/street/109 at (5120, 1200)
  - street oldshore/street/165 runs 2.0 m past street oldshore/street/144 at (6624, 1016)
  - street oldshore/street/166 runs 2.0 m past street oldshore/street/0 at (5055, 425)
  - street oldshore/street/164 runs 1.9 m past street oldshore/street/160 at (7025, 1029)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 0**
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (5129, 1637))

## Building kinds here
front 1806, back 434, shed 239, kiosk 179, old house 67, stalls 58, smoke rack 23, barge 3, school 2, palace 1, bust 1
