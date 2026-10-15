# 3D audit: The Maze

`.venv/bin/python scripts/audit3d.py maze` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 8**
  - street maze/street/4 runs 169 m along art Ring Road at (2378, 4446)
  - street maze/street/64 runs 107 m along main Adeleke Road at (2861, 4106)
  - street maze/street/18 runs 58 m along main Afolabi Avenue at (2652, 4894)
  - street maze/street/21 runs 51 m along street maze/street/136 at (2511, 4352)
  - street maze/street/105 runs 45 m along street maze/street/108 at (3301, 4282)
  - street maze/street/108 runs 32 m along street maze/street/110 at (3346, 4285)
  - street maze/street/62 runs 29 m along main Adeleke Road at (2850, 4192)
  - street maze/street/124 runs 23 m along street maze/street/136 at (2682, 4360)
- **R2 Near misses (ends short of a road): 4**
  - lane maze/lane/7 stops 7.8 m short of street maze/street/52 at (2740, 4006)
  - street maze/street/90 stops 7.7 m short of street maze/street/129 at (3059, 4644)
  - street maze/street/52 stops 2.2 m short of lane maze/lane/7 at (2738, 3961)
  - street maze/street/137 stops 2.1 m short of street maze/street/26 at (2599, 4750)
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 1**
  - street maze/street/62 crosses main Adeleke Road at 5 degrees at (2849, 4192)
- **R5 Roads on water with no bridge: 12**
  - path maze/path/2 has 663 m on water with no bridge, from (2980, 4446)
  - path maze/path/3 has 661 m on water with no bridge, from (2986, 4446)
  - street maze/street/84 has 12 m on water with no bridge, from (2941, 4226)
  - street maze/street/87 has 9 m on water with no bridge, from (3040, 4771)
  - lane maze/lane/11 has 9 m on water with no bridge, from (3021, 4596)
  - street maze/street/82 has 9 m on water with no bridge, from (2961, 4314)
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
  - street maze/street/57 has 8 m on water with no bridge, from (3031, 4688)
  - lane maze/lane/16 has 8 m on water with no bridge, from (2987, 4437)
  - street maze/street/77 has 8 m on water with no bridge, from (2938, 4157)
  - street maze/street/73 has 5 m on water with no bridge, from (2943, 4214)
  - street maze/street/85 has 4 m on water with no bridge, from (2947, 4215)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 14**
  - main Alaba Road is listed twice (main/10, main/17)
  - main Ajasa Street is listed twice (main/41, main/59)
  - main Oyelaran Road is listed twice (main/4, main/24)
  - main Akande Road is listed twice (main/20, main/53)
  - main Ireti Road is listed twice (main/3, main/12)
  - main Agboola Street is listed twice (main/26, main/40)
  - main Idowu Street is listed twice (main/21, main/25)
  - main Okafor Road is listed twice (main/19, main/67)
  - main Afolabi Avenue is listed twice (main/11, main/18)
  - main Adeyemi Road is listed twice (main/16, main/62)
  - main Ogunleye Road is listed twice (main/54, main/66)
  - main main/23 is listed twice (main/23, main/28)
  - and 2 more

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a back house, (3276, 4469))

## Building kinds here
front 1199, back 433, shed 154, stalls 84, kiosk 68, print 15, warehouse 2, school 2, transformer 1, canopy 1
