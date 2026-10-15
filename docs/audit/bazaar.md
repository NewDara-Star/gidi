# 3D audit: The Bazaar

`.venv/bin/python scripts/audit3d.py bazaar` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 12**
  - street border/street/49 runs 153 m along main Taiwo Road at (1203, 4882)
  - street bazaar/street/25 runs 107 m along exp Coastal Expressway at (1985, 5356)
  - main main/1 runs 77 m along main Bello Street at (1200, 4640)
  - main main/9 runs 77 m along main Bello Street at (1200, 4640)
  - main main/8 runs 77 m along main Taiwo Road at (1205, 4695)
  - exp art/0 runs 58 m along street border/street/55 at (1006, 5320)
  - main main/1 runs 46 m along street border/street/48 at (1187, 5067)
  - main main/9 runs 46 m along street border/street/48 at (1187, 5067)
  - street bazaar/street/41 runs 44 m along main Oyelaran Road at (2199, 4878)
  - main main/8 runs 31 m along main Kehinde Street at (1235, 4770)
  - main main/34 runs 31 m along main Kehinde Street at (1235, 4770)
  - street bazaar/street/35 runs 28 m along street bazaar/street/60 at (2098, 5202)
- **R2 Near misses (ends short of a road): 13**
  - street bazaar/street/9 stops 11.3 m short of street bazaar/street/1 at (1477, 4978)
  - street bazaar/street/0 stops 7.1 m short of lane bazaar/lane/10 at (1807, 5750)
  - lane bazaar/lane/7 stops 5.4 m short of main Oyelaran Road at (1691, 4850)
  - street bazaar/street/29 stops 4.8 m short of lane bazaar/lane/28 at (2007, 5853)
  - lane bazaar/lane/28 stops 4.8 m short of street bazaar/street/29 at (2006, 5858)
  - street bazaar/street/35 stops 4.4 m short of street bazaar/street/60 at (2097, 5202)
  - lane bazaar/lane/12 stops 2.1 m short of lane bazaar/lane/11 at (1800, 5246)
  - art art/2 stops 1.7 m short of street bazaar/street/25 at (1920, 5360)
  - lane bazaar/lane/19 stops 1.0 m short of street bazaar/street/63 at (1513, 5099)
  - street bazaar/street/8 stops 1.0 m short of street bazaar/street/59 at (1362, 5359)
  - lane bazaar/lane/0 stops 1.0 m short of street bazaar/street/4 at (1240, 5162)
  - lane bazaar/lane/3 stops 1.0 m short of street bazaar/street/63 at (1373, 5114)
  - and 1 more
- **R3 Overshoots (ends past a road): 4**
  - lane bazaar/lane/24 runs 11.4 m past street bazaar/street/32 at (2061, 4899)
  - street bazaar/street/66 runs 2.0 m past street bazaar/street/9 at (1459, 4978)
  - street bazaar/street/64 runs 2.0 m past main Aremu Road at (1714, 5884)
  - street bazaar/street/65 runs 2.0 m past street bazaar/street/55 at (1962, 5647)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 4**
  - main Chukwuma Street has 677 m on water with no bridge, from (200, 5935)
  - main Danjuma Road has 467 m on water with no bridge, from (1848, 5924)
  - main Okonkwo Road has 229 m on water with no bridge, from (2321, 6216)
  - main Aremu Road has 4 m on water with no bridge, from (1714, 5920)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 8**
  - main Taiwo Road is listed twice (main/1, main/9)
  - main Kehinde Street is listed twice (main/30, main/35)
  - main Oyelaran Road is listed twice (main/7, main/27)
  - main Balogun Street is listed twice (main/2, main/33)
  - main Ireti Road is listed twice (main/6, main/15)
  - main Idowu Street is listed twice (main/24, main/28)
  - main Afolabi Avenue is listed twice (main/14, main/21)
  - main Bello Street is listed twice (main/8, main/34)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 1010, stalls 641, back 502, shed 97, pen 82, kiosk 76, barracks 29, scrap 8, plaza 6, unfinished 2, school 2, container 1, checkpoint 1
