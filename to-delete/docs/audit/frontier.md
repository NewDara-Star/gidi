# 3D audit: The Frontier

`.venv/bin/python scripts/audit3d.py frontier` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 6**
  - street frontier/street/3 runs 46 m along street frontier/street/6 at (6469, 4623)
  - street frontier/street/23 runs 45 m along street frontier/street/24 at (6859, 5258)
  - street frontier/street/137 runs 30 m along street frontier/street/138 at (8134, 5465)
  - street frontier/street/43 runs 30 m along street frontier/street/44 at (7445, 4990)
  - street frontier/street/176 runs 20 m along lane frontier/lane/82 at (8057, 5055)
  - street frontier/street/118 runs 19 m along street frontier/street/120 at (7769, 5399)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 1**
  - street frontier/street/188 runs 7.9 m past main Kunle Road at (7263, 4518)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 0**
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 2** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - danger (1): Disputed Plots (on bare ground, (7172, 4949))
  - landmark (1): New Estates (on bare ground, (6977, 5506))

## Building kinds here
front 813, back 167, generator 124, shed 100, kiosk 97, column 84, water tank 70, unfinished house 48, beach shack 30, tank 20, toll booth 7, school 2, flare stack 1, toll canopy 1
