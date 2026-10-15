# 3D audit: Old Island

`.venv/bin/python scripts/audit3d.py oldisland` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 9**
  - street oldisland/street/99 runs 65 m along main Remi Road at (4834, 5361)
  - street oldisland/street/100 runs 46 m along street oldisland/street/109 at (4929, 4988)
  - street oldisland/street/112 runs 36 m along main Tokunbo Road at (4962, 4704)
  - street oldisland/street/111 runs 34 m along street oldisland/street/122 at (5056, 4984)
  - street oldisland/street/115 runs 32 m along main Remi Road at (4893, 5145)
  - street oldisland/street/75 runs 31 m along main Remi Road at (4786, 5591)
  - street oldisland/street/64 runs 27 m along street oldisland/street/73 at (4796, 4799)
  - street oldisland/street/79 runs 24 m along street oldisland/street/83 at (4802, 5742)
  - street oldisland/street/175 runs 21 m along street oldisland/street/185 at (4813, 5220)
- **R2 Near misses (ends short of a road): 3**
  - street oldisland/street/189 stops 7.8 m short of street oldisland/street/112 at (4861, 4693)
  - street oldisland/street/113 stops 3.7 m short of main Tokunbo Road at (4871, 4669)
  - lane oldisland/lane/5 stops 1.0 m short of street oldisland/street/185 at (4628, 5219)
- **R3 Overshoots (ends past a road): 3**
  - street oldisland/street/187 runs 2.0 m past street oldisland/street/140 at (5186, 5438)
  - street oldisland/street/188 runs 2.0 m past street oldisland/street/64 at (4782, 4762)
  - street oldisland/street/186 runs 2.0 m past street oldisland/street/114 at (5054, 5081)
- **R4 Knife-edge crossings (under 25 degrees): 2**
  - street oldisland/street/99 crosses main Remi Road at 14 degrees at (4834, 5361)
  - street oldisland/street/75 crosses main Remi Road at 18 degrees at (4786, 5590)
- **R5 Roads on water with no bridge: 12**
  - main Tokunbo Road has 647 m on water with no bridge, from (5004, 4710)
  - main Uche Close has 522 m on water with no bridge, from (5598, 4810)
  - main Tijani Road has 480 m on water with no bridge, from (4388, 5008)
  - main Nwachukwu Road has 212 m on water with no bridge, from (4530, 4737)
  - street oldisland/street/112 has 40 m on water with no bridge, from (4998, 4708)
  - street oldisland/street/1 has 11 m on water with no bridge, from (4389, 4996)
  - main Remi Road has 10 m on water with no bridge, from (5013, 4725)
  - street oldisland/street/34 has 9 m on water with no bridge, from (4521, 4751)
  - street oldisland/street/180 has 8 m on water with no bridge, from (5170, 4788)
  - street oldisland/street/2 has 7 m on water with no bridge, from (4400, 5073)
  - path oldisland/path/2 has 6 m on water with no bridge, from (5242, 4817)
  - street oldisland/street/5 has 5 m on water with no bridge, from (4461, 4776)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 1**
  - main Yemi Road is listed twice (main/71, main/81)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (4565, 5383))

## Building kinds here
front 1255, back 425, stalls 180, shed 131, kiosk 96, brazilian house 53, bank tower 4, school 2, palace 1
