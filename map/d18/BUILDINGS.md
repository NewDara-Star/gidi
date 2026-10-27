# Lagoon University (district 18): the buildings and their hand passes

## Hand pass 2 (27 Oct): houses, storeys and kinds

**144 houses**, each with a kind and storeys; they cover 7.3% of the district (21,587 m²; Saba 14.4%). Most of the
district is campus: halls, faculties and grounds, which come in as landmark plots (hand pass 4), not as houses. The
real cover was not measured; filling up is owed to the look pass (NOW), as the other districts'.

How, in Saba's order (no change to any builder; drafts on scratch copies of map/d18):

1. **Skeleton draft** on Lagoon University's 4 main roads and Saba's 6 main roads within 60 m: 104 houses.
2. **The cut** (the road comes first): each house minus every carriageway of Lagoon University and Saba + 0.05 m, and
   minus Saba's houses; 43 were cut, 17 left under 12 m² or a third of themselves were not written: **87 kept**.
3. **Frontage** (`draft_buildings.py --frontage`, blocks still empty only): the draft's log counts 62
   in 13 blocks (the table below) but wrote 58 (the drafter's party-wall step trims each new house back to an
   overlapping house already drawn or a bigger new one, and drops what is left under 12 m²: 4 went there); those 58 were cut the same way: 1 cut, none dropped, **58 kept**.
4. **Slivers and road ends** (houses on a carriageway, half width - 0.05 m with round ends, cut to the carriageway +
   0.1 m, and to a party wall 0.05 m off a larger neighbour): 20 houses, 147 m² in all (the most 40.2 m²; read back from
   the houses' notes), and one house left with too little was dropped (145 -> 144). A second and third run cut nothing.
5. **The board's own test** (web/mapedit.js boardProblems, headless, Lagoon University with the eight districts at the
   bar): **0**.
6. **Storeys**: `draft_storeys.py` **read 75** (1: 26, 2: 35, 3: 11, 4: 3) and 1 read 5 or more and was left;
   `draft_storeys_nearby.py` gave 39 more their neighbours' median (the tall reading among them, now 3 storeys); the
   last 30 had no house with storeys within 30 m and were set by hand to their 5 nearest houses' median (Lagoon
   University's and Saba's), noted on each. The tall reading, b-8bd534f5 (76 m²), is owed a look on Street View
   (NOW). Storeys: 1: 47, 2: 75, 3: 19, 4: 3.
7. **Kinds** (`draft_kinds.py`): compound_house 66, face_me_bungalow 39, walkup 20, shack 8, shop_under_flats 6, shed
   4, kiosk_row 1.

## The frontage draft: real houses on a road

| block | houses (the draft's log; 62, of which 58 written) | covered | on a road |
|---|---|---|---|
| 7 | 14 | 62% | 0 |
| 10 | 10 | 60% | 0 |
| 12 | 5 | 66% | 0 |
| 13 | 5 | 58% | 0 |
| 14 | 2 | 18% | 0 |
| 15 | 6 | 63% | 0 |
| 18 | 3 | 36% | 0 |
| 19 | 3 | 57% | 0 |
| 20 | 5 | 61% | 0 |
| 21 | 3 | 60% | 0 |
| 22 | 2 | 43% | 0 |
| 23 | 2 | 58% | 0 |
| 24 | 2 | 61% | 0 |

The other blocks were already drawn by the skeleton or have no real house in them.
