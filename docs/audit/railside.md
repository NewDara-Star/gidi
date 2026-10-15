# 3D audit: Railside

`.venv/bin/python scripts/audit3d.py railside` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 9**
  - street railside/street/81 runs 49 m along main Lawal Road at (655, 3599)
  - main main/8 runs 38 m along main Kehinde Street at (1245, 4772)
  - street railside/street/47 runs 35 m along main Market Roundabout at (465, 3681)
  - street railside/street/32 runs 34 m along main Market Roundabout at (457, 3708)
  - street railside/street/32 runs 33 m along street railside/street/47 at (457, 3708)
  - main main/28 runs 29 m along main Fadipe Road at (219, 3262)
  - street railside/street/179 runs 26 m along street railside/street/195 at (1408, 3450)
  - street railside/street/95 runs 24 m along street railside/street/103 at (788, 3114)
  - street railside/street/115 runs 23 m along street railside/street/120 at (835, 3585)
- **R2 Near misses (ends short of a road): 0**
- **R3 Overshoots (ends past a road): 2**
  - street railside/street/215 runs 2.0 m past street railside/street/14 at (206, 4372)
  - street railside/street/213 runs 1.9 m past street railside/street/18 at (365, 2942)
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
front 2370, back 1014, stalls 330, shed 267, kiosk 143, pen 127, bakery 15, mound 14, tank 2, school 2, works 1, bust 1
