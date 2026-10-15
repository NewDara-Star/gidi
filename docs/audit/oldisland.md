# 3D audit: Old Island

`.venv/bin/python scripts/audit3d.py oldisland` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 6**
  - street oldisland/street/100 runs 50 m along street oldisland/street/109 at (4884, 4984)
  - street oldisland/street/99 runs 39 m along main Remi Road at (4828, 5392)
  - street oldisland/street/111 runs 39 m along street oldisland/street/135 at (5022, 4990)
  - street oldisland/street/64 runs 32 m along street oldisland/street/78 at (4788, 4774)
  - street oldisland/street/75 runs 29 m along main Remi Road at (4782, 5612)
  - street oldisland/street/79 runs 28 m along street oldisland/street/83 at (4807, 5742)
- **R2 Near misses (ends short of a road): 1**
  - street oldisland/street/188 stops 9.1 m short of street oldisland/street/73 at (4782, 4762)
- **R3 Overshoots (ends past a road): 2**
  - street oldisland/street/186 runs 2.0 m past street oldisland/street/114 at (5054, 5081)
  - street oldisland/street/187 runs 2.0 m past street oldisland/street/141 at (5186, 5438)
- **R4 Knife-edge crossings (under 25 degrees): 1**
  - street oldisland/street/111 crosses street oldisland/street/135 at 1 degrees at (5053, 4985)
- **R5 Roads on water with no bridge: 13**
  - main Tokunbo Road has 647 m on water with no bridge, from (5172, 4781)
  - main Uche Close has 522 m on water with no bridge, from (5689, 4777)
  - main Tijani Road has 480 m on water with no bridge, from (4394, 5074)
  - main Nwachukwu Road has 212 m on water with no bridge, from (4518, 4743)
  - street oldisland/street/112 has 11 m on water with no bridge, from (4962, 4704)
  - street oldisland/street/1 has 11 m on water with no bridge, from (4400, 4996)
  - main Remi Road has 10 m on water with no bridge, from (5012, 4725)
  - street oldisland/street/34 has 9 m on water with no bridge, from (4522, 4751)
  - street oldisland/street/180 has 8 m on water with no bridge, from (5169, 4788)
  - street oldisland/street/2 has 6 m on water with no bridge, from (4394, 5074)
  - path oldisland/path/2 has 6 m on water with no bridge, from (5242, 4817)
  - street oldisland/street/5 has 5 m on water with no bridge, from (4462, 4775)
  - and 1 more
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 1255, back 425, stalls 180, shed 131, kiosk 96, brazilian house 53, bank tower 4, school 2, palace 1
