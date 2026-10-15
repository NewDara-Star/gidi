# 3D audit: The Maze

`.venv/bin/python scripts/audit3d.py maze` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 2**
  - street maze/street/107 runs 40 m along street maze/street/110 at (3301, 4282)
  - street maze/street/52 runs 22 m along lane maze/lane/7 at (2738, 3962)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 16**
  - path maze/path/2 has 663 m on water with no bridge, from (2980, 4446)
  - path maze/path/3 has 661 m on water with no bridge, from (2986, 4446)
  - street maze/street/86 has 17 m on water with no bridge, from (2943, 4214)
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
  - lane maze/lane/12 has 8 m on water with no bridge, from (3013, 4594)
  - lane maze/lane/11 has 8 m on water with no bridge, from (3021, 4594)
  - street maze/street/83 has 8 m on water with no bridge, from (2961, 4316)
  - street maze/street/84 has 8 m on water with no bridge, from (2961, 4316)
  - lane maze/lane/17 has 8 m on water with no bridge, from (2987, 4437)
  - street maze/street/57 has 8 m on water with no bridge, from (3031, 4688)
  - lane maze/lane/18 has 8 m on water with no bridge, from (2979, 4436)
  - street maze/street/58 has 8 m on water with no bridge, from (3023, 4688)
  - and 4 more
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (2429, 4242))

## Building kinds here
front 1199, back 433, shed 154, stalls 84, kiosk 68, print 15, warehouse 2, school 2, transformer 1, canopy 1
