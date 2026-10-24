# 3D audit: The Heights

`.venv/bin/python scripts/audit3d.py heights` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 5**
  - street heights/street/25 runs 56 m along main Mbanefo Road at (6403, 5741)
  - street heights/street/22 runs 41 m along main Hassan Road at (5941, 5811)
  - street heights/street/12 runs 38 m along street heights/street/15 at (5812, 5516)
  - art art/6 runs 35 m along street oldisland/street/185 at (4616, 5360)
  - street heights/street/50 runs 33 m along street heights/street/51 at (5919, 4888)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 1**
  - street heights/street/78 runs 2.0 m past street heights/street/65 at (6227, 4630)
- **R4 Knife-edge crossings (under 25 degrees): 0**
- **R5 Roads on water with no bridge: 0**
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (5816, 4977))

## Building kinds here
front 334, generator 184, water tank 76, office block 58, back 57, shed 31, beach shack 22, beach bar 20, gatehouse 11, kiosk 8, horse shelter 6, mansion 5, nightclub 2, school 2, toll booth 2, apartment tower 2, clubhouse 1
