# 3D audit: The Frontier

`.venv/bin/python scripts/audit3d.py frontier` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 14**
  - main main/92 runs 175 m along exp Peninsula Expressway at (6691, 5323)
  - street frontier/street/81 runs 73 m along exp Peninsula Expressway at (6740, 5312)
  - street frontier/street/114 runs 58 m along street frontier/street/115 at (7746, 5777)
  - street frontier/street/182 runs 49 m along lane frontier/lane/83 at (8225, 5013)
  - street frontier/street/81 runs 42 m along main Wahab Road at (6740, 5312)
  - street frontier/street/3 runs 42 m along street frontier/street/6 at (6465, 4664)
  - street frontier/street/100 runs 40 m along main Akinola Drive at (7228, 5831)
  - street frontier/street/23 runs 40 m along street frontier/street/24 at (6856, 5219)
  - street frontier/street/120 runs 37 m along street frontier/street/121 at (7764, 5350)
  - street frontier/street/140 runs 26 m along street frontier/street/141 at (8129, 5440)
  - street frontier/street/176 runs 26 m along street frontier/street/189 at (7977, 4499)
  - street frontier/street/43 runs 25 m along street frontier/street/44 at (7443, 4966)
  - and 2 more
- **R2 Near misses (ends short of a road): 27**
  - lane frontier/lane/84 stops 13.6 m short of main Raji Street at (8303, 5167)
  - street frontier/street/114 stops 11.4 m short of street frontier/street/124 at (7764, 5774)
  - lane frontier/lane/16 stops 11.4 m short of street frontier/street/25 at (7038, 5081)
  - lane frontier/lane/72 stops 10.9 m short of street frontier/street/135 at (7889, 5434)
  - street frontier/street/106 stops 10.6 m short of street frontier/street/163 at (7396, 5564)
  - lane frontier/lane/61 stops 10.0 m short of street frontier/street/109 at (7478, 5570)
  - lane frontier/lane/85 stops 9.5 m short of main Wahab Road at (7633, 5118)
  - lane frontier/lane/40 stops 8.1 m short of street frontier/street/77 at (6474, 5683)
  - street frontier/street/98 stops 6.2 m short of street frontier/street/153 at (7146, 5606)
  - street frontier/street/127 stops 6.2 m short of street frontier/street/129 at (7818, 5829)
  - street frontier/street/29 stops 6.0 m short of street frontier/street/58 at (7155, 4909)
  - lane frontier/lane/60 stops 5.3 m short of street frontier/street/102 at (7347, 5392)
  - and 15 more
- **R3 Overshoots (ends past a road): 4**
  - lane frontier/lane/46 runs 10.8 m past street frontier/street/80 at (6646, 5566)
  - lane frontier/lane/43 runs 9.6 m past street frontier/street/89 at (7023, 5463)
  - street frontier/street/191 runs 7.8 m past main Kunle Road at (7263, 4518)
  - lane frontier/lane/36 runs 3.8 m past street frontier/street/173 at (7776, 4536)
- **R4 Knife-edge crossings (under 25 degrees): 2**
  - main main/92 crosses exp Peninsula Expressway at 10 degrees at (6776, 5304)
  - street frontier/street/81 crosses main Wahab Road at 20 degrees at (6740, 5312)
- **R5 Roads on water with no bridge: 4**
  - main Kunle Road has 804 m on water with no bridge, from (7466, 4487)
  - main Uche Close has 522 m on water with no bridge, from (5598, 4810)
  - street frontier/street/17 has 12 m on water with no bridge, from (6786, 4524)
  - street frontier/street/42 has 4 m on water with no bridge, from (7418, 4496)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 1**
  - main Mbanefo Road is listed twice (main/82, main/91)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 3** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - danger (1): Disputed Plots (on bare ground, (7172, 4949))
  - landmark (1): New Estates (on bare ground, (6977, 5506))
  - sport (1): Community Football Pitch (on a front house, (7887, 4982))

## Building kinds here
front 813, back 167, generator 124, shed 100, kiosk 97, column 84, water tank 70, unfinished house 48, beach shack 30, tank 20, toll booth 7, school 2, flare stack 1, toll canopy 1
