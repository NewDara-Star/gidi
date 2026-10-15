# 3D audit: The Port

`.venv/bin/python scripts/audit3d.py port` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 6**
  - street port/street/8 runs 44 m along street port/street/9 at (3539, 5550)
  - street port/street/26 runs 39 m along main Nwosu Road at (4005, 4890)
  - street port/street/27 runs 38 m along street port/street/47 at (3935, 5451)
  - street port/street/29 runs 37 m along street port/street/49 at (3715, 5192)
  - street port/street/0 runs 20 m along street port/street/49 at (3695, 5189)
  - street port/street/40 runs 19 m along street port/street/47 at (3763, 5600)
- **R2 Near misses (ends short of a road): 10**
  - lane port/lane/2 stops 10.5 m short of street port/street/5 at (3563, 5333)
  - lane port/lane/19 stops 9.7 m short of street port/street/0 at (3485, 5168)
  - lane port/lane/20 stops 8.1 m short of street port/street/6 at (3528, 6118)
  - lane port/lane/17 stops 7.5 m short of street port/street/0 at (3279, 5119)
  - lane jungle/lane/34 stops 4.2 m short of main Alaba Road at (3184, 5772)
  - lane port/lane/6 stops 2.9 m short of main Alaba Road at (3189, 5716)
  - street port/street/51 stops 2.0 m short of street port/street/9 at (3763, 5583)
  - lane port/lane/9 stops 1.1 m short of street port/street/44 at (3658, 5756)
  - lane port/lane/22 stops 1.0 m short of street port/street/47 at (3767, 5484)
  - street port/street/22 stops 0.6 m short of street port/street/23 at (3962, 4782)
- **R3 Overshoots (ends past a road): 3**
  - art art/1 runs 5.1 m past lane port/lane/13 at (3680, 5120)
  - street port/street/50 runs 2.0 m past street port/street/42 at (3294, 6335)
  - street port/street/52 runs 2.0 m past street port/street/36 at (3667, 6336)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 9**
  - main Nwosu Road has 1178 m on water with no bridge, from (4007, 5540)
  - main Durojaiye Road has 541 m on water with no bridge, from (4033, 4347)
  - main Ogundipe Road has 374 m on water with no bridge, from (2560, 6367)
  - main Musa Road has 333 m on water with no bridge, from (3790, 6376)
  - street port/street/26 has 59 m on water with no bridge, from (4000, 4870)
  - street port/street/46 has 9 m on water with no bridge, from (3883, 6360)
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
  - street port/street/24 has 6 m on water with no bridge, from (4006, 5564)
  - street port/street/25 has 5 m on water with no bridge, from (4005, 4784)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 4**
  - main Alaba Road is listed twice (main/13, main/20)
  - main Okafor Road is listed twice (main/22, main/70)
  - main Afolabi Avenue is listed twice (main/14, main/21)
  - main Adeyemi Road is listed twice (main/19, main/65)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 727, stalls 504, back 229, stack 224, trailer 120, kiosk 111, shed 43, tank 20, crane 18, villa 16, cellblock 10, checkpoint 4, warehouse 2, tower 2, school 2
