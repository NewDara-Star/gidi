# Lagoon University (district 18): the buildings and their hand passes

## Hand pass 3 (27 Oct): the real places

The real places (Overture) with a kind the game uses (`working_bar.place_kind`, Mùṣá's hand pass 55 rules), and by
hand, as Saba, the real churches whose Overture category names a denomination (none here). Placed by Saba's hand pass
3 rules: 26 real points, **26 places**: church 12, school 5, buka 2, bank 2, clinic 1, fuel 1, mosque 1, bar 1 and a
bus stop by hand.

- On the house their point stands in or the nearest within 8 m: 9 places on 8 houses (b-9d4fe6f6 carries both the
  fuel station and a bank; its link is the fuel station's); a second real place of a kind at the same house shares
  its place once (26 real points, 25 places from Overture). The other 16 as 6 m squares at their point, moved up to
  12.5 m off roads and houses. 8 houses carry a place link. Every real place has a place of its kind within 10 m
  (working bar).
- **No bus stop or motor park is in Overture inside Lagoon University** (the nearest, a bus_station point, is 158 m
  outside it and outside Saba too). By hand, one stop: at the university's main gate on its main road in from Saba
  (rd-cbdf1d43), a 6 m square on the street's edge 40 m in from the border, clear of carriageways, houses and places.
  The campus shuttle's stops and the gate's motor park are owed to a study of the map (NOW), as Saba's.

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
