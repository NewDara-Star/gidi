# 3D audit: The Bazaar

`.venv/bin/python scripts/audit3d.py bazaar` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 1**
  - exp art/0 runs 58 m along street border/street/55 at (1006, 5320)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 3**
  - art art/2 runs 14.3 m past exp Coastal Expressway at (1920, 5360)
  - street bazaar/street/65 runs 2.0 m past street bazaar/street/9 at (1459, 4978)
  - street bazaar/street/64 runs 2.0 m past street bazaar/street/54 at (1962, 5647)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 4**
  - main Chukwuma Street has 677 m on water with no bridge, from (200, 5935)
  - main Danjuma Road has 467 m on water with no bridge, from (1848, 5924)
  - main Okonkwo Road has 229 m on water with no bridge, from (2321, 6216)
  - main Aremu Road has 4 m on water with no bridge, from (1714, 5924)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 1010, stalls 641, back 502, shed 97, pen 82, kiosk 76, barracks 29, scrap 8, plaza 6, unfinished 2, school 2, container 1, checkpoint 1
