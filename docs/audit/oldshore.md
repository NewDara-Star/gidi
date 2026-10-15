# 3D audit: Old Shore

`.venv/bin/python scripts/audit3d.py oldshore` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 9**
  - street oldshore/street/108 runs 76 m along art Shore Road at (5198, 1187)
  - street oldshore/street/68 runs 68 m along main Lateef Road at (6477, 1188)
  - street oldshore/street/68 runs 56 m along street oldshore/street/69 at (6363, 934)
  - street oldshore/street/54 runs 49 m along street oldshore/street/55 at (5925, 493)
  - street oldshore/street/16 runs 26 m along lane oldshore/lane/5 at (5450, 736)
  - street oldshore/street/81 runs 23 m along lane oldshore/lane/45 at (6611, 791)
  - street oldshore/street/90 runs 20 m along street oldshore/street/91 at (6891, 1071)
  - street oldshore/street/13 runs 19 m along street oldshore/street/20 at (5504, 1410)
  - street oldshore/street/29 runs 18 m along street oldshore/street/30 at (5525, 1464)
- **R2 Near misses (ends short of a road): 23**
  - lane oldshore/lane/50 stops 13.7 m short of main Jimoh Street at (6715, 411)
  - lane oldshore/lane/65 stops 12.4 m short of main Udoh Road at (5107, 1554)
  - lane oldshore/lane/42 stops 11.2 m short of street oldshore/street/77 at (6561, 588)
  - lane oldshore/lane/35 stops 10.5 m short of street oldshore/street/55 at (5951, 777)
  - street oldshore/street/108 stops 9.1 m short of street oldshore/street/14 at (5445, 1176)
  - street oldshore/street/71 stops 8.6 m short of street oldshore/street/91 at (6885, 1112)
  - street oldshore/street/87 stops 7.4 m short of street oldshore/street/91 at (6881, 1092)
  - street oldshore/street/105 stops 6.8 m short of street oldshore/street/122 at (7160, 913)
  - street oldshore/street/11 stops 4.2 m short of lane oldshore/lane/0 at (5366, 1017)
  - street oldshore/street/4 stops 4.0 m short of street oldshore/street/127 at (5233, 715)
  - lane oldshore/lane/45 stops 4.0 m short of street oldshore/street/81 at (6585, 795)
  - street oldshore/street/81 stops 2.0 m short of lane oldshore/lane/45 at (6612, 791)
  - and 11 more
- **R3 Overshoots (ends past a road): 4**
  - street oldshore/street/45 runs 11.2 m past street oldshore/street/46 at (5913, 858)
  - art art/8 runs 9.8 m past street oldshore/street/108 at (5120, 1200)
  - street oldshore/street/165 runs 2.0 m past street oldshore/street/0 at (5055, 425)
  - street oldshore/street/163 runs 1.9 m past street oldshore/street/159 at (7025, 1029)
- **R4 Knife-edge crossings (under 25 degrees): 2**
  - street oldshore/street/68 crosses main Lateef Road at 13 degrees at (6477, 1188)
  - street oldshore/street/108 crosses art Shore Road at 13 degrees at (5161, 1188)
- **R5 Roads on water with no bridge: 9**
  - main Popoola Street has 728 m on water with no bridge, from (6722, 1230)
  - main Kolawole Street has 340 m on water with no bridge, from (5318, 1716)
  - street oldshore/street/111 has 13 m on water with no bridge, from (5319, 1714)
  - street oldshore/street/118 has 10 m on water with no bridge, from (6653, 1231)
  - main Lateef Road has 9 m on water with no bridge, from (6524, 1251)
  - street oldshore/street/68 has 8 m on water with no bridge, from (6510, 1260)
  - street oldshore/street/158 has 7 m on water with no bridge, from (6762, 1221)
  - lane oldshore/lane/66 has 7 m on water with no bridge, from (5224, 1756)
  - street oldshore/street/122 has 6 m on water with no bridge, from (7213, 1149)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 0**

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a back house, (5647, 1370))

## Building kinds here
front 1806, back 434, shed 239, kiosk 179, old house 67, stalls 58, smoke rack 23, barge 3, school 2, palace 1, bust 1
