# 3D audit: Food Gate

`.venv/bin/python scripts/audit3d.py foodgate` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 3**
  - street foodgate/street/149 runs 28 m along street foodgate/street/150 at (3450, 3039)
  - street foodgate/street/101 runs 20 m along lane foodgate/lane/23 at (3123, 2777)
  - street foodgate/street/24 runs 19 m along street foodgate/street/29 at (2736, 2829)
- **R2 Near misses (ends short of a road): 1**
  - street foodgate/street/218 stops 2.0 m short of street foodgate/street/216 at (3070, 3229)
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 0**
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 1011, stalls 540, back 348, kiosk 182, shed 113, school 2, checkpoint 1, terminal 1, stage 1
