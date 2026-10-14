# 3D audit: The Heights

`.venv/bin/python scripts/audit3d.py heights` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 3**
  - street heights/street/8 runs 101 m along art Waterfront Drive at (5713, 5346)
  - art art/6 runs 35 m along street oldisland/street/185 at (4616, 5360)
  - street heights/street/18 runs 24 m along street heights/street/19 at (5866, 5411)
- **R2 Near misses (ends short of a road): 6**
  - street heights/street/59 stops 13.6 m short of main Uche Close at (6287, 4619)
  - street heights/street/58 stops 2.2 m short of street heights/street/22 at (6140, 4976)
  - lane heights/lane/35 stops 1.0 m short of main Uche Close at (6147, 4657)
  - lane heights/lane/5 stops 1.0 m short of street heights/street/49 at (5557, 5208)
  - lane heights/lane/13 stops 1.0 m short of street heights/street/56 at (5632, 5114)
  - lane heights/lane/18 stops 1.0 m short of street heights/street/12 at (5838, 5593)
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 5**
  - main Tokunbo Road has 647 m on water with no bridge, from (5004, 4710)
  - main Uche Close has 522 m on water with no bridge, from (5598, 4810)
  - main Hassan Road has 13 m on water with no bridge, from (5805, 4737)
  - lane heights/lane/12 has 9 m on water with no bridge, from (5681, 4790)
  - lane heights/lane/11 has 3 m on water with no bridge, from (5529, 4839)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 1**
  - main Yemi Road is listed twice (main/71, main/81)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 305, generator 164, water tank 75, office block 64, back 55, shed 38, beach shack 22, beach bar 20, kiosk 8, gatehouse 6, horse shelter 6, nightclub 5, mansion 5, apartment tower 3, school 2, toll booth 2, clubhouse 1
