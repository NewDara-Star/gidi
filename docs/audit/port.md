# 3D audit: The Port

`.venv/bin/python scripts/audit3d.py port` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 2**
  - street port/street/8 runs 49 m along street port/street/9 at (3583, 5557)
  - street port/street/38 runs 23 m along street port/street/45 at (3768, 5600)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 3**
  - art art/1 runs 5.1 m past lane port/lane/13 at (3680, 5120)
  - street port/street/49 runs 2.0 m past street port/street/40 at (3294, 6335)
  - street port/street/51 runs 2.0 m past street port/street/34 at (3667, 6336)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 11**
  - main Nwosu Road has 1178 m on water with no bridge, from (4006, 5565)
  - main Durojaiye Road has 541 m on water with no bridge, from (4030, 4388)
  - main Ogundipe Road has 374 m on water with no bridge, from (2560, 6367)
  - main Musa Road has 333 m on water with no bridge, from (3790, 6376)
  - street port/street/19 has 15 m on water with no bridge, from (4001, 5341)
  - street port/street/26 has 14 m on water with no bridge, from (4000, 4929)
  - street port/street/44 has 9 m on water with no bridge, from (3884, 6360)
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
  - street port/street/24 has 6 m on water with no bridge, from (4006, 5565)
  - street port/street/25 has 5 m on water with no bridge, from (4005, 4784)
  - lane port/lane/23 has 4 m on water with no bridge, from (4003, 5968)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 727, stalls 504, back 229, stack 224, trailer 120, kiosk 111, shed 43, tank 20, crane 18, villa 16, cellblock 10, checkpoint 4, warehouse 2, tower 2, school 2
