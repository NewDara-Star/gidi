# 3D audit: Food Gate

`.venv/bin/python scripts/audit3d.py foodgate` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 4**
  - street foodgate/street/69 runs 32 m along street foodgate/street/70 at (2962, 3116)
  - street foodgate/street/78 runs 26 m along street foodgate/street/114 at (3319, 2962)
  - street foodgate/street/79 runs 22 m along street foodgate/street/80 at (3096, 2728)
  - street foodgate/street/33 runs 22 m along street foodgate/street/35 at (2686, 3207)
- **R2 Near misses (ends short of a road): 1**
  - street foodgate/street/211 stops 2.0 m short of street foodgate/street/209 at (2951, 3366)
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 0**
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (3358, 3327))

## Building kinds here
extension 2049, stalls 1394, front 1343, back 790, shed 458, kiosk 140, school 2, checkpoint 1, terminal 1, stage 1
