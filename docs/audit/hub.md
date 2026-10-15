# 3D audit: The Hub

`.venv/bin/python scripts/audit3d.py hub` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 2**
  - art art/1 runs 42 m along street railside/street/114 at (831, 2776)
  - art art/1 runs 35 m along street maze/street/137 at (2662, 4474)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 1**
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (2167, 4785))

## Building kinds here
front 1057, back 884, shed 76, kiosk 66, stalls 48, stands 4, warehouse 2, school 2, terminal 1, station 1, hotel 1
