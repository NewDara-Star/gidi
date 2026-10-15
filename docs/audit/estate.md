# 3D audit: The Estate

`.venv/bin/python scripts/audit3d.py estate` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 2**
  - street estate/street/54 runs 59 m along main Salami Road at (2237, 2763)
  - street estate/street/54 runs 32 m along main Balogun Road at (2024, 2729)
- **R2 Near misses (ends short of a road): 14**
  - street estate/street/2 stops 14.9 m short of main Balogun Road at (1569, 2368)
  - street estate/street/30 stops 13.5 m short of main Oshinowo Road at (1903, 1818)
  - street estate/street/45 stops 9.4 m short of lane estate/lane/0 at (1676, 2662)
  - street estate/street/37 stops 6.4 m short of lane estate/lane/0 at (1543, 2637)
  - lane estate/lane/12 stops 6.3 m short of street estate/street/28 at (1934, 1894)
  - lane estate/lane/2 stops 3.9 m short of main Odusanya Street at (1573, 2098)
  - street estate/street/79 stops 2.0 m short of street estate/street/73 at (2174, 2192)
  - lane estate/lane/9 stops 1.7 m short of street estate/street/25 at (1893, 2490)
  - lane estate/lane/8 stops 1.1 m short of street estate/street/25 at (1905, 2637)
  - lane estate/lane/4 stops 1.1 m short of street estate/street/14 at (1836, 2274)
  - lane estate/lane/13 stops 1.0 m short of street estate/street/28 at (1918, 2009)
  - lane estate/lane/7 stops 1.0 m short of street estate/street/25 at (1890, 2494)
  - and 2 more
- **R3 Overshoots (ends past a road): 2**
  - street estate/street/81 runs 5.7 m past main Shonibare Road at (2653, 1952)
  - street estate/street/80 runs 2.0 m past street estate/street/35 at (1785, 2468)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 0**
- **R6 Decks with no road: 0**
- **D Roads listed twice: 7**
  - main Ajasa Street is listed twice (main/41, main/59)
  - main Salami Road is listed twice (main/42, main/48)
  - main Eze Street is listed twice (main/33, main/43)
  - street estate/street/49 is listed twice (estate/street/49, estate/street/50)
  - street estate/street/38 is listed twice (estate/street/38, estate/street/40)
  - street estate/street/38 is listed twice (estate/street/38, estate/street/39)
  - street estate/street/39 is listed twice (estate/street/39, estate/street/40)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 521, generator 346, back 216, water tank 187, shed 33, gatehouse 21, kiosk 8, school 2, mansion 1, clubhouse 1
