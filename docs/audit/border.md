# 3D audit: The Border

`.venv/bin/python scripts/audit3d.py border` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 0**
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 0**
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 6**
  - main Chukwuma Street has 677 m on water with no bridge, from (200, 5935)
  - main Danjuma Road has 467 m on water with no bridge, from (1848, 5924)
  - street border/street/30 has 10 m on water with no bridge, from (239, 5930)
  - street border/street/1 has 6 m on water with no bridge, from (81, 5920)
  - path border/path/27 has 3 m on water with no bridge, from (298, 5920)
  - street border/street/37 has 3 m on water with no bridge, from (890, 5920)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 2** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - danger (1): Bush Paths (on bare ground, (351, 4832))
  - sport (1): Community Football Pitch (on a back house, (409, 4921))

## Building kinds here
front 944, back 820, kiosk 137, shed 95, fishing hut 86, colonial house 25, drums 10, border booth 5, checkpoint 3, school 2, border canopy 1
