# 3D audit: The Heights

`.venv/bin/python scripts/audit3d.py heights` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 7**
  - street heights/street/33 runs 57 m along art Waterfront Drive at (5635, 5349)
  - street heights/street/25 runs 49 m along main Mbanefo Road at (6395, 5741)
  - street heights/street/61 runs 40 m along art Waterfront Drive at (6206, 5327)
  - art art/6 runs 35 m along street oldisland/street/185 at (4616, 5360)
  - main main/92 runs 34 m along street heights/street/22 at (5944, 5844)
  - street heights/street/14 runs 33 m along street heights/street/15 at (5812, 5516)
  - street heights/street/50 runs 29 m along street heights/street/51 at (5915, 4887)
- **R2 Near misses (ends short of a road): 3**
  - street heights/street/58 stops 8.2 m short of lane heights/lane/20 at (6083, 5240)
  - street heights/street/73 stops 1.7 m short of lane heights/lane/26 at (6313, 5090)
  - lane heights/lane/7 stops 0.9 m short of street heights/street/10 at (5798, 5598)
- **R3 Overshoots (ends past a road): 1**
  - street heights/street/79 runs 2.0 m past street heights/street/66 at (6227, 4630)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 6**
  - main Kunle Road has 804 m on water with no bridge, from (7466, 4487)
  - main Tokunbo Road has 647 m on water with no bridge, from (5004, 4710)
  - main Uche Close has 522 m on water with no bridge, from (5598, 4810)
  - main Hassan Road has 13 m on water with no bridge, from (5805, 4737)
  - lane heights/lane/19 has 9 m on water with no bridge, from (5689, 4787)
  - lane heights/lane/18 has 3 m on water with no bridge, from (5524, 4840)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 2**
  - main Mbanefo Road is listed twice (main/89, main/98)
  - main Yemi Road is listed twice (main/81, main/91)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 2** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (2): Community Football Pitch (on a front house, (6198, 5293)), Community Football Pitch (on a front house, (6217, 5117))

## Building kinds here
front 334, generator 184, water tank 76, office block 58, back 57, shed 31, beach shack 22, beach bar 20, gatehouse 11, kiosk 8, horse shelter 6, mansion 5, nightclub 2, school 2, toll booth 2, apartment tower 2, clubhouse 1
