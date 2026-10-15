# 3D audit: Railside

`.venv/bin/python scripts/audit3d.py railside` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 6**
  - street railside/street/6 runs 39 m along street railside/street/30 at (426, 4022)
  - street railside/street/48 runs 32 m along main Market Roundabout at (459, 3676)
  - main main/35 runs 29 m along main Fadipe Road at (219, 3262)
  - street railside/street/49 runs 29 m along main Lawal Road at (630, 3613)
  - street railside/street/96 runs 20 m along street railside/street/106 at (787, 3114)
  - street railside/street/125 runs 19 m along street railside/street/126 at (835, 3585)
- **R2 Near misses (ends short of a road): 22**
  - lane railside/lane/49 stops 12.2 m short of art Ring Road at (1013, 3510)
  - street railside/street/38 stops 10.5 m short of street railside/street/194 at (417, 3108)
  - lane railside/lane/56 stops 10.0 m short of street railside/street/219 at (1249, 3450)
  - street railside/street/132 stops 9.7 m short of lane railside/lane/33 at (927, 4480)
  - lane railside/lane/36 stops 9.5 m short of street railside/street/111 at (799, 3983)
  - lane railside/lane/0 stops 8.8 m short of main Lawal Road at (242, 3849)
  - lane railside/lane/42 stops 8.1 m short of street railside/street/117 at (834, 2781)
  - street railside/street/174 stops 6.3 m short of lane railside/lane/56 at (1254, 3454)
  - street railside/street/122 stops 6.0 m short of lane railside/lane/27 at (827, 4450)
  - lane railside/lane/33 stops 5.8 m short of street railside/street/132 at (921, 4488)
  - street railside/street/21 stops 2.8 m short of street railside/street/196 at (403, 2682)
  - lane railside/lane/19 stops 2.5 m short of street railside/street/198 at (581, 2896)
  - and 10 more
- **R3 Overshoots (ends past a road): 5**
  - street railside/street/133 runs 3.7 m past street railside/street/204 at (929, 3038)
  - street railside/street/123 runs 2.1 m past street railside/street/203 at (915, 3638)
  - street railside/street/223 runs 2.0 m past street railside/street/14 at (206, 4372)
  - street railside/street/222 runs 1.9 m past street railside/street/208 at (207, 4460)
  - street railside/street/221 runs 1.9 m past street railside/street/18 at (365, 2942)
- **R4 Knife-edge crossings (under 25 degrees): 2**
  - street railside/street/48 crosses main Market Roundabout at 0 degrees at (458, 3697)
  - street railside/street/48 crosses main Market Roundabout at 1 degrees at (458, 3697)
- **R5 Roads on water with no bridge: 1**
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 6**
  - main Kehinde Street is listed twice (main/27, main/32)
  - main Oyelaran Road is listed twice (main/4, main/24)
  - main Salami Road is listed twice (main/42, main/48)
  - main Agboola Street is listed twice (main/26, main/40)
  - main Eze Street is listed twice (main/33, main/43)
  - main Bello Street is listed twice (main/5, main/31)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 0** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)

## Building kinds here
front 2398, back 1054, stalls 336, shed 247, kiosk 170, pen 127, bakery 20, mound 12, tank 2, school 2, works 1, bust 1
