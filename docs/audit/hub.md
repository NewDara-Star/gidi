# 3D audit: The Hub

`.venv/bin/python scripts/audit3d.py hub` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 15**
  - art art/1 runs 178 m along street maze/street/4 at (2366, 4445)
  - street hub/street/38 runs 74 m along art Ayinde Avenue at (1855, 4014)
  - main main/29 runs 55 m along street capital/street/33 at (2042, 3820)
  - main main/43 runs 55 m along street capital/street/33 at (2042, 3820)
  - main main/32 runs 48 m along art Ayinde Avenue at (1844, 4522)
  - street hub/street/70 runs 43 m along art Ring Road at (2270, 4444)
  - art art/1 runs 42 m along street railside/street/115 at (840, 2815)
  - main main/30 runs 41 m along art Ring Road at (1325, 4275)
  - main main/35 runs 41 m along art Ring Road at (1325, 4275)
  - street hub/street/2 runs 38 m along main Kehinde Street at (1298, 4464)
  - street hub/street/42 runs 38 m along art Ayinde Avenue at (1880, 3902)
  - street hub/street/0 runs 37 m along main Kehinde Street at (1265, 4701)
  - and 3 more
- **R2 Near misses (ends short of a road): 13**
  - street hub/street/94 stops 15.1 m short of art Ring Road at (2321, 4425)
  - lane hub/lane/13 stops 12.1 m short of main Agboola Street at (1743, 3795)
  - lane hub/lane/1 stops 11.9 m short of art Ring Road at (1438, 4343)
  - lane hub/lane/5 stops 7.8 m short of art Ring Road at (1506, 4333)
  - lane hub/lane/9 stops 7.2 m short of art Ayinde Avenue at (1843, 4522)
  - lane hub/lane/21 stops 1.1 m short of art Northern Road at (2091, 4178)
  - lane hub/lane/22 stops 1.0 m short of art Northern Road at (2030, 4260)
  - lane hub/lane/3 stops 1.0 m short of main Kehinde Street at (1354, 4043)
  - lane hub/lane/4 stops 1.0 m short of art Ring Road at (1682, 4365)
  - lane hub/lane/11 stops 1.0 m short of street hub/street/91 at (1751, 3980)
  - lane hub/lane/14 stops 1.0 m short of street hub/street/89 at (1917, 4271)
  - lane hub/lane/17 stops 1.0 m short of street hub/street/57 at (2082, 4682)
  - and 1 more
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 1**
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 14**
  - main Ajasa Street is listed twice (main/44, main/62)
  - main Kehinde Street is listed twice (main/30, main/35)
  - main Oyelaran Road is listed twice (main/7, main/27)
  - main Akande Road is listed twice (main/23, main/56)
  - main Ireti Road is listed twice (main/6, main/15)
  - main Agboola Street is listed twice (main/29, main/43)
  - main Idowu Street is listed twice (main/24, main/28)
  - main Eze Street is listed twice (main/36, main/46)
  - main Afolabi Avenue is listed twice (main/14, main/21)
  - main Bello Street is listed twice (main/8, main/34)
  - main main/26 is listed twice (main/26, main/31)
  - main main/26 is listed twice (main/26, main/64)
  - and 2 more

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 1057, back 884, shed 76, kiosk 66, stalls 48, stands 4, warehouse 2, school 2, terminal 1, station 1, hotel 1
