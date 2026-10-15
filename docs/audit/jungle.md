# 3D audit: Jungle City

`.venv/bin/python scripts/audit3d.py jungle` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 9**
  - street jungle/street/56 runs 327 m along street jungle/street/59 at (2704, 6305)
  - main main/11 runs 65 m along street maze/street/18 at (2660, 4895)
  - main main/18 runs 65 m along street maze/street/18 at (2660, 4895)
  - street jungle/street/65 runs 65 m along main Adeleke Road at (2753, 5519)
  - street jungle/street/34 runs 37 m along main Ogundipe Road at (2595, 6358)
  - main main/11 runs 36 m along street maze/street/67 at (2876, 4899)
  - main main/18 runs 36 m along street maze/street/67 at (2876, 4899)
  - street jungle/street/15 runs 31 m along street jungle/street/17 at (2433, 5920)
  - street jungle/street/82 runs 18 m along street jungle/street/83 at (3037, 5687)
- **R2 Near misses (ends short of a road): 5**
  - lane jungle/lane/1 stops 20.0 m short of exp Coastal Expressway at (2412, 5336)
  - street jungle/street/38 stops 6.0 m short of lane jungle/lane/6 at (2564, 6239)
  - lane jungle/lane/6 stops 4.3 m short of street jungle/street/12 at (2516, 6227)
  - lane jungle/lane/23 stops 1.0 m short of street jungle/street/102 at (2916, 5844)
  - lane jungle/lane/9 stops 1.0 m short of street jungle/street/20 at (2544, 5752)
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 15**
  - main Danjuma Road has 467 m on water with no bridge, from (1848, 5924)
  - path jungle/path/1 has 414 m on water with no bridge, from (3022, 6202)
  - path jungle/path/0 has 412 m on water with no bridge, from (3017, 6198)
  - main Ogundipe Road has 374 m on water with no bridge, from (2560, 6367)
  - main Musa Road has 333 m on water with no bridge, from (3790, 6376)
  - main Okonkwo Road has 229 m on water with no bridge, from (2321, 6216)
  - street jungle/street/34 has 26 m on water with no bridge, from (2605, 6360)
  - lane jungle/lane/18 has 14 m on water with no bridge, from (2975, 6261)
  - lane jungle/lane/22 has 14 m on water with no bridge, from (3111, 6080)
  - street jungle/street/103 has 12 m on water with no bridge, from (2920, 6308)
  - street jungle/street/58 has 11 m on water with no bridge, from (2908, 6322)
  - street jungle/street/12 has 10 m on water with no bridge, from (2330, 6196)
  - and 3 more
- **R6 Decks with no road: 0**
- **D Roads listed twice: 7**
  - main Alaba Road is listed twice (main/10, main/17)
  - main Oyelaran Road is listed twice (main/4, main/24)
  - main Ireti Road is listed twice (main/3, main/12)
  - main Idowu Street is listed twice (main/21, main/25)
  - main Okafor Road is listed twice (main/19, main/67)
  - main Afolabi Avenue is listed twice (main/11, main/18)
  - main Adeyemi Road is listed twice (main/16, main/62)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 1758, back 1066, stalls 165, shed 125, kiosk 87, flats 16, school 2, studio 1, cafe 1, hotel 1
