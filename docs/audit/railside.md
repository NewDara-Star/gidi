# 3D audit: Railside

`.venv/bin/python scripts/audit3d.py railside` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 7**
  - street railside/street/6 runs 39 m along street railside/street/30 at (426, 4022)
  - street railside/street/48 runs 32 m along main Market Roundabout at (459, 3676)
  - main main/38 runs 29 m along main Fadipe Road at (219, 3262)
  - street railside/street/49 runs 29 m along main Lawal Road at (630, 3613)
  - street railside/street/180 runs 21 m along street railside/street/196 at (1428, 3455)
  - street railside/street/96 runs 20 m along street railside/street/104 at (787, 3114)
  - street railside/street/121 runs 19 m along street railside/street/122 at (835, 3585)
- **R2 Near misses (ends short of a road): 23**
  - lane railside/lane/0 stops 14.6 m short of main Lawal Road at (252, 3850)
  - street railside/street/38 stops 10.5 m short of street railside/street/184 at (417, 3108)
  - lane railside/lane/44 stops 9.4 m short of street railside/street/115 at (832, 2775)
  - street railside/street/141 stops 8.8 m short of street railside/street/203 at (1098, 4522)
  - lane railside/lane/51 stops 6.5 m short of art Ring Road at (1002, 3486)
  - lane railside/lane/35 stops 6.0 m short of street railside/street/126 at (917, 4554)
  - street railside/street/22 stops 5.4 m short of lane railside/lane/7 at (294, 3586)
  - lane railside/lane/23 stops 5.4 m short of lane railside/lane/29 at (863, 3235)
  - lane railside/lane/49 stops 5.1 m short of main Kalejaiye Street at (1159, 2707)
  - street railside/street/21 stops 2.8 m short of street railside/street/186 at (403, 2682)
  - street railside/street/215 stops 2.0 m short of street railside/street/198 at (207, 4460)
  - lane railside/lane/31 stops 1.7 m short of street railside/street/142 at (1141, 4459)
  - and 11 more
- **R3 Overshoots (ends past a road): 4**
  - street railside/street/127 runs 3.7 m past street railside/street/194 at (929, 3038)
  - street railside/street/119 runs 2.1 m past street railside/street/193 at (915, 3638)
  - street railside/street/216 runs 2.0 m past street railside/street/14 at (206, 4372)
  - street railside/street/214 runs 1.9 m past street railside/street/18 at (365, 2942)
- **R4 Knife-edge crossings (under 25 degrees): 2**
  - street railside/street/48 crosses main Market Roundabout at 0 degrees at (458, 3697)
  - street railside/street/48 crosses main Market Roundabout at 1 degrees at (458, 3697)
- **R5 Roads on water with no bridge: 1**
  - art Ring Road has 8 m on water with no bridge, from (3001, 4515)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 9**
  - main Taiwo Road is listed twice (main/1, main/9)
  - main Kehinde Street is listed twice (main/30, main/35)
  - main Oyelaran Road is listed twice (main/7, main/27)
  - main Salami Road is listed twice (main/45, main/51)
  - main Balogun Street is listed twice (main/2, main/33)
  - main Agboola Street is listed twice (main/29, main/43)
  - main Eze Street is listed twice (main/36, main/46)
  - main Bello Street is listed twice (main/8, main/34)
  - street border/street/23 is listed twice (border/street/23, border/street/24)

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a back house, (770, 4012))

## Building kinds here
front 2370, back 1014, stalls 330, shed 267, kiosk 143, pen 127, bakery 15, mound 14, tank 2, school 2, works 1, bust 1
