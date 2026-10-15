# 3D audit: The Border

`.venv/bin/python scripts/audit3d.py border` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 2**
  - street border/street/46 runs 85 m along street border/street/50 at (972, 4881)
  - street border/street/48 runs 39 m along main Taiwo Road at (1184, 5107)
- **R2 Near misses (ends short of a road): 13**
  - lane border/lane/24 stops 12.5 m short of main Chukwuma Street at (444, 5901)
  - lane border/lane/1 stops 8.2 m short of street border/street/0 at (65, 5888)
  - street border/street/26 stops 7.7 m short of lane border/lane/23 at (381, 5569)
  - lane border/lane/38 stops 7.3 m short of main Mojeed Close at (627, 5391)
  - street border/street/5 stops 2.7 m short of lane border/lane/3 at (192, 5008)
  - street border/street/46 stops 2.5 m short of street border/street/49 at (1200, 4906)
  - lane border/lane/12 stops 1.1 m short of street border/street/16 at (480, 5072)
  - lane border/lane/13 stops 1.1 m short of street border/street/16 at (498, 4933)
  - lane border/lane/10 stops 1.1 m short of street border/street/16 at (516, 4792)
  - lane border/lane/41 stops 1.0 m short of street border/street/45 at (730, 4664)
  - lane border/lane/11 stops 1.0 m short of street border/street/16 at (535, 4637)
  - lane border/lane/42 stops 1.0 m short of street border/street/45 at (737, 4839)
  - and 1 more
- **R3 Overshoots (ends past a road): 1**
  - lane border/lane/23 runs 2.9 m past street border/street/26 at (385, 5561)
- **R4 Knife-edge crossings (under 25 degrees): 1**
  - street border/street/46 crosses street border/street/50 at 7 degrees at (1014, 4885)
- **R5 Roads on water with no bridge: 6**
  - main Chukwuma Street has 677 m on water with no bridge, from (200, 5935)
  - main Danjuma Road has 467 m on water with no bridge, from (1848, 5924)
  - street border/street/38 has 12 m on water with no bridge, from (890, 5923)
  - street border/street/31 has 10 m on water with no bridge, from (238, 5920)
  - street border/street/1 has 6 m on water with no bridge, from (81, 5926)
  - path border/path/27 has 3 m on water with no bridge, from (298, 5920)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 3**
  - main Taiwo Road is listed twice (main/1, main/9)
  - main Balogun Street is listed twice (main/2, main/33)
  - main Bello Street is listed twice (main/8, main/34)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - danger (1): Bush Paths (on bare ground, (351, 4832))

## Building kinds here
front 944, back 820, kiosk 137, shed 95, fishing hut 86, colonial house 25, drums 10, border booth 5, checkpoint 3, school 2, border canopy 1
