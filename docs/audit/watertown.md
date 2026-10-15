# 3D audit: Water Town

`.venv/bin/python scripts/audit3d.py watertown` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 3**
  - street watertown/street/74 runs 35 m along street watertown/street/76 at (3964, 4724)
  - street watertown/street/74 runs 35 m along street watertown/street/75 at (3964, 4724)
  - street watertown/street/75 runs 35 m along street watertown/street/76 at (3964, 4724)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 9**
  - main Nwosu Road has 1178 m on water with no bridge, from (4006, 5565)
  - main Durojaiye Road has 541 m on water with no bridge, from (4030, 4388)
  - main Adebayo Road has 537 m on water with no bridge, from (4003, 3950)
  - main Folake Street has 432 m on water with no bridge, from (3998, 2869)
  - path watertown/path/4 has 185 m on water with no bridge, from (4138, 3688)
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
  - lane watertown/lane/16 has 7 m on water with no bridge, from (3926, 3529)
  - street watertown/street/73 has 6 m on water with no bridge, from (4024, 4387)
  - lane watertown/lane/20 has 3 m on water with no bridge, from (4037, 4254)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
back 1978, front 1308, stilt 720, shed 45, kiosk 32, raft 8, sawdust 6, saw shed 3, school 2, stilt bar 1
