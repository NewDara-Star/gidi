# 3D audit: Food Gate

`.venv/bin/python scripts/audit3d.py foodgate` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).

## Map problems
- **R1 Roads running along each other: 11**
  - street foodgate/street/33 runs 218 m along street foodgate/street/35 at (2833, 3524)
  - street foodgate/street/203 runs 166 m along street foodgate/street/218 at (3901, 2782)
  - street foodgate/street/2 runs 145 m along street foodgate/street/103 at (3116, 3693)
  - street foodgate/street/52 runs 53 m along lane foodgate/lane/10 at (2703, 3499)
  - street foodgate/street/27 runs 49 m along street foodgate/street/64 at (2797, 2831)
  - street foodgate/street/35 runs 46 m along street foodgate/street/51 at (2783, 3522)
  - street foodgate/street/33 runs 32 m along street foodgate/street/51 at (2833, 3524)
  - street foodgate/street/154 runs 23 m along street foodgate/street/155 at (3436, 3022)
  - street foodgate/street/106 runs 20 m along lane foodgate/lane/22 at (3123, 2760)
  - street foodgate/street/27 runs 19 m along street foodgate/street/32 at (2736, 2829)
  - street foodgate/street/145 runs 19 m along lane foodgate/lane/40 at (3370, 2844)
- **R2 Near misses (ends short of a road): 34**
  - street foodgate/street/193 stops 10.7 m short of street foodgate/street/197 at (3732, 2882)
  - lane foodgate/lane/6 stops 9.5 m short of street foodgate/street/210 at (2722, 2782)
  - street foodgate/street/115 stops 8.9 m short of lane foodgate/lane/31 at (3190, 2639)
  - street foodgate/street/18 stops 8.8 m short of lane foodgate/lane/3 at (2533, 3363)
  - lane foodgate/lane/25 stops 8.6 m short of street foodgate/street/99 at (3098, 2626)
  - lane foodgate/lane/26 stops 8.4 m short of street foodgate/street/100 at (3112, 2519)
  - lane foodgate/lane/47 stops 6.6 m short of art Northern Road at (3636, 2874)
  - street foodgate/street/62 stops 6.2 m short of lane foodgate/lane/8 at (2746, 3599)
  - lane foodgate/lane/28 stops 6.1 m short of street foodgate/street/118 at (3213, 3123)
  - street foodgate/street/153 stops 5.5 m short of lane foodgate/lane/44 at (3455, 2529)
  - street foodgate/street/46 stops 5.3 m short of lane foodgate/lane/6 at (2676, 2728)
  - lane foodgate/lane/44 stops 4.5 m short of street foodgate/street/153 at (3434, 2595)
  - and 22 more
- **R3 Overshoots (ends past a road): 4**
  - lane foodgate/lane/14 runs 11.0 m past street foodgate/street/58 at (2819, 3221)
  - lane foodgate/lane/10 runs 9.9 m past street foodgate/street/52 at (2706, 3402)
  - street foodgate/street/224 runs 1.9 m past street foodgate/street/75 at (3070, 3229)
  - lane foodgate/lane/8 runs 1.7 m past street foodgate/street/71 at (2852, 3593)
- **R4 Knife-edge crossings (under 25 degrees): 3**
  - street foodgate/street/203 crosses street foodgate/street/218 at 3 degrees at (3895, 2778)
  - street foodgate/street/52 crosses lane foodgate/lane/10 at 8 degrees at (2707, 3473)
  - street foodgate/street/145 crosses lane foodgate/lane/40 at 13 degrees at (3372, 2845)
- **R5 Roads on water with no bridge: 7**
  - main Adebayo Road has 537 m on water with no bridge, from (4003, 3950)
  - main Folake Street has 431 m on water with no bridge, from (3998, 2869)
  - street foodgate/street/203 has 10 m on water with no bridge, from (4003, 2842)
  - street foodgate/street/218 has 7 m on water with no bridge, from (3999, 2844)
  - street foodgate/street/205 has 7 m on water with no bridge, from (3967, 2952)
  - lane foodgate/lane/62 has 6 m on water with no bridge, from (4019, 2752)
  - street foodgate/street/201 has 3 m on water with no bridge, from (3951, 3019)
- **R6 Decks with no road: 0**
- **D Roads listed twice: 13**
  - main Ajasa Street is listed twice (main/41, main/59)
  - main Salami Road is listed twice (main/42, main/48)
  - main Akande Road is listed twice (main/20, main/53)
  - main Agboola Street is listed twice (main/26, main/40)
  - main Idowu Street is listed twice (main/21, main/25)
  - main Okafor Road is listed twice (main/19, main/67)
  - main Ibrahim Road is listed twice (main/55, main/65)
  - main Ogunleye Road is listed twice (main/54, main/66)
  - main main/23 is listed twice (main/23, main/28)
  - main main/23 is listed twice (main/23, main/61)
  - main main/28 is listed twice (main/28, main/61)
  - street foodgate/street/0 is listed twice (foodgate/street/0, foodgate/street/1)
  - and 1 more

## Model gaps
- **M1 building kinds with no builder: 0**
- **M2 parcel kinds with no builder: 0**
- **M3 civic plots: 0**
- **M4 places on the map with nothing of their own: 1** (a pitch, market or landmark with no plot or building of its kind under it: give it one in the map)
  - sport (1): Community Football Pitch (on a front house, (3097, 3704))

## Building kinds here
front 1012, stalls 540, back 348, kiosk 183, shed 113, school 2, checkpoint 1, terminal 1, stage 1
