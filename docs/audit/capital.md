# 3D audit: The Capital

`.venv/bin/python scripts/audit3d.py capital` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 2**
  - street capital/street/26 runs 54 m along street capital/street/27 at (1987, 3237)
  - street capital/street/22 runs 50 m along art Ayinde Avenue at (1938, 3005)
- **R2 Near misses (ends short of a road): 1**
  - street capital/street/65 stops 2.0 m short of street capital/street/52 at (2170, 3698)
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
front 707, back 323, kiosk 94, shed 78, phone mall 36, barracks 26, strip 10, office 2, school 2, hall 1, bust 1
