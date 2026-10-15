# 3D audit: The Maze

`.venv/bin/python scripts/audit3d.py maze` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 2**
  - street maze/street/107 runs 40 m along street maze/street/110 at (3301, 4282)
  - street maze/street/52 runs 22 m along lane maze/lane/7 at (2738, 3962)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 0**
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (2429, 4242))

## Building kinds here
front 1197, back 433, shed 154, stalls 84, kiosk 68, print 15, warehouse 2, school 2, transformer 1, canopy 1
