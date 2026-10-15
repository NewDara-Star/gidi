# 3D audit: Jungle City

`.venv/bin/python scripts/audit3d.py jungle` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 3**
  - main main/13 runs 36 m along street maze/street/67 at (2876, 4899)
  - street jungle/street/15 runs 35 m along street jungle/street/17 at (2404, 5914)
  - street jungle/street/81 runs 22 m along street jungle/street/83 at (3020, 5683)
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
  - sport (1): Community Football Pitch (on a back house, (3022, 6288))

## Building kinds here
front 1758, back 1066, stalls 165, shed 125, kiosk 87, flats 16, school 2, studio 1, cafe 1, hotel 1
