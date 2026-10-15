# 3D audit: The Capital

`.venv/bin/python scripts/audit3d.py capital` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 14**
  - street capital/street/2 runs 105 m along main Olatunji Street at (1940, 3705)
  - art art/2 runs 83 m along street hub/street/38 at (1859, 4097)
  - art art/2 runs 59 m along main Interchange slip road at (1853, 4559)
  - street capital/street/28 runs 49 m along street capital/street/29 at (1987, 3237)
  - street capital/street/33 runs 48 m along main Agboola Street at (2049, 3821)
  - street capital/street/47 runs 48 m along main Ajasa Street at (2543, 2809)
  - art art/2 runs 46 m along street hub/street/42 at (1868, 3947)
  - main main/41 runs 43 m along main main/61 at (2400, 3880)
  - main main/59 runs 43 m along main main/61 at (2400, 3880)
  - main main/23 runs 43 m along main Ajasa Street at (2395, 3838)
  - main main/28 runs 43 m along main Ajasa Street at (2395, 3838)
  - street capital/street/3 runs 42 m along art Ayinde Avenue at (1933, 2963)
  - and 2 more
- **R2 Near misses (ends short of a road): 8**
  - street capital/street/16 stops 8.0 m short of lane capital/lane/9 at (1742, 3530)
  - lane capital/lane/9 stops 8.0 m short of street capital/street/16 at (1750, 3528)
  - street capital/street/66 stops 2.0 m short of street capital/street/53 at (2170, 3698)
  - lane capital/lane/19 stops 1.0 m short of main Oladipo Road at (2173, 3336)
  - lane capital/lane/14 stops 1.0 m short of main Oladipo Road at (2400, 3397)
  - lane capital/lane/20 stops 1.0 m short of main Oladipo Road Roundabout at (2042, 3280)
  - lane railside/lane/52 stops 1.0 m short of main Eze Street at (1448, 3189)
  - lane capital/lane/32 stops 1.0 m short of main Oladipo Road at (1870, 3241)
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 0**
- **R6 Decks with no road: 0**
- **D Roads listed twice: 12**
  - main Ajasa Street is listed twice (main/41, main/59)
  - main Kehinde Street is listed twice (main/27, main/32)
  - main Salami Road is listed twice (main/42, main/48)
  - main Akande Road is listed twice (main/20, main/53)
  - main Agboola Street is listed twice (main/26, main/40)
  - main Idowu Street is listed twice (main/21, main/25)
  - main Eze Street is listed twice (main/33, main/43)
  - main main/23 is listed twice (main/23, main/28)
  - main main/23 is listed twice (main/23, main/61)
  - main main/28 is listed twice (main/28, main/61)
  - street foodgate/street/0 is listed twice (foodgate/street/0, foodgate/street/1)
  - street estate/street/49 is listed twice (estate/street/49, estate/street/50)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (2339, 3290))

## Building kinds here
front 707, back 323, kiosk 94, shed 78, phone mall 36, barracks 26, strip 10, office 2, school 2, hall 1, bust 1
