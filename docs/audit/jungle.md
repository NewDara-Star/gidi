# 3D audit: Jungle City

`.venv/bin/python scripts/audit3d.py jungle` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 4**
  - main main/13 runs 36 m along street maze/street/67 at (2876, 4899)
  - street jungle/street/15 runs 35 m along street jungle/street/17 at (2404, 5914)
  - street jungle/street/80 runs 22 m along street jungle/street/82 at (3020, 5683)
  - lane jungle/lane/18 runs 12 m along lane jungle/lane/19 at (2978, 6258)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 17**
  - main Danjuma Road has 467 m on water with no bridge, from (1848, 5924)
  - path jungle/path/1 has 414 m on water with no bridge, from (3022, 6202)
  - path jungle/path/0 has 412 m on water with no bridge, from (3017, 6198)
  - main Ogundipe Road has 374 m on water with no bridge, from (2560, 6367)
  - main Musa Road has 333 m on water with no bridge, from (3790, 6376)
  - main Okonkwo Road has 229 m on water with no bridge, from (2321, 6216)
  - lane jungle/lane/23 has 14 m on water with no bridge, from (3111, 6080)
  - street jungle/street/57 has 11 m on water with no bridge, from (2908, 6322)
  - street jungle/street/102 has 10 m on water with no bridge, from (2915, 6312)
  - lane jungle/lane/18 has 9 m on water with no bridge, from (2975, 6249)
  - lane jungle/lane/19 has 9 m on water with no bridge, from (2975, 6249)
  - street jungle/street/12 has 9 m on water with no bridge, from (2320, 6192)
  - and 5 more
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
