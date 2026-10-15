# 3D audit: Water Town

`.venv/bin/python scripts/audit3d.py watertown` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 2**
  - street watertown/street/72 runs 35 m along street watertown/street/77 at (3956, 4695)
  - street watertown/street/54 runs 29 m along street watertown/street/56 at (3786, 4206)
- **R2 Near misses (ends short of a road): 10**
  - lane watertown/lane/11 stops 8.7 m short of street watertown/street/40 at (3664, 4225)
  - lane watertown/lane/4 stops 6.8 m short of street watertown/street/25 at (3508, 4481)
  - street watertown/street/5 stops 6.6 m short of street watertown/street/3 at (3270, 4882)
  - lane watertown/lane/1 stops 1.0 m short of street watertown/street/15 at (3361, 4640)
  - lane port/lane/14 stops 1.0 m short of main Adeyemi Road at (3256, 4905)
  - lane watertown/lane/2 stops 1.0 m short of street watertown/street/41 at (3747, 4440)
  - lane watertown/lane/14 stops 1.0 m short of street watertown/street/22 at (3526, 3759)
  - lane watertown/lane/10 stops 1.0 m short of street watertown/street/20 at (3537, 4247)
  - lane watertown/lane/17 stops 1.0 m short of main Adebayo Road at (3942, 3654)
  - lane watertown/lane/3 stops 1.0 m short of street watertown/street/41 at (3654, 4458)
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 9**
  - main Nwosu Road has 1178 m on water with no bridge, from (4007, 5540)
  - main Durojaiye Road has 541 m on water with no bridge, from (4033, 4347)
  - main Adebayo Road has 537 m on water with no bridge, from (4003, 3950)
  - main Folake Street has 431 m on water with no bridge, from (3998, 2869)
  - path watertown/path/4 has 185 m on water with no bridge, from (4138, 3688)
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
  - lane watertown/lane/16 has 6 m on water with no bridge, from (3920, 3530)
  - street watertown/street/74 has 6 m on water with no bridge, from (4030, 4388)
  - lane watertown/lane/20 has 3 m on water with no bridge, from (4037, 4254)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 7**
  - main Alaba Road is listed twice (main/13, main/20)
  - main Akande Road is listed twice (main/23, main/56)
  - main Okafor Road is listed twice (main/22, main/70)
  - main Afolabi Avenue is listed twice (main/14, main/21)
  - main Adeyemi Road is listed twice (main/19, main/65)
  - main Ibrahim Road is listed twice (main/58, main/68)
  - main Ogunleye Road is listed twice (main/57, main/69)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
back 1978, front 1308, stilt 720, shed 45, kiosk 32, raft 8, sawdust 6, saw shed 3, school 2, stilt bar 1
