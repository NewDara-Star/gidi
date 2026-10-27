# Lagoon University (district 18): the buildings and their hand passes

## Hand pass 4 (27 Oct): the landmarks, walled with a gate each

Saba's hand pass 4 recipe on Overture's land use in Gidi metres, with two kinds added by hand for this district: a
university ground (a school ground, with its school place) and a clinic compound. **2 plots**:

- **The campus** (Overture's university ground, 95% of it inside the district): one school ground of 211,528 m², 71% of
  the district. It is kept whole with its 139 inside roads, as Gbàgede kept the Deeper Life ground whole (a campus is
  one walled ground its own roads run through), less the carriageways of the roads that only pass along it. Its wall
  0.2 m inside the edge: 15 pieces, 2,904 m of the 3,086 m edge (open where 16 houses stand on the edge), and a gate
  across each of the 14 roads that enter. The board's test then found 4 wall pieces across a road (where a road ends
  at the wall or meets it slanting, its round end reached past the gate): by hand, those 4 gates were widened to the
  road's whole carriageway along the wall + 0.6 m (by 2.1 to 11.8 m). The board's test then named 3 more (it names one
  road per wall), so every wall was tested the board's way (0.25 m pieces, 0.2 m thick, against every carriageway of
  Lagoon University and Saba, half width - 0.05 m, flat ends) and every stretch on a carriageway outside a gate got
  one, + 0.6 m: 3 walls, 4 stretches, 49.5 m (two of 35 m and 14 m where a campus road runs along the wall's line);
  the same test then finds none. Where a road runs along the wall rather than through it the gate covers its whole
  run, so 5 of the campus's gates are 38 m or longer, the longest 156.5 m: open stretches of wall, the look
  pass's to close with railings or a wall set back off the road (NOW). 89 houses wholly inside are linked to it; the school place is its outline.
- **The campus clinic** (Overture's clinic ground, wholly inside): a compound of 2,008 m² inside the campus, its wall
  271 m of 278 m with one 4 m gate where it comes nearest a road (none enters it).
- Left out: the college of education's ground (none of it inside the district), and the pitches,
  the track, the cricket oval and the grass (no plot kind for them yet; the look pass's).

The map picture (27 Oct, looked at): no land between districts left unclaimed (0.000 km²). Lagoon University reads
open next to Saba (houses cover 7.3%): the campus's halls and faculties are to come as buildings in the look pass. The
near view still frames off-centre with its labels outside the drawing (the tool's fix is owed, NOW).

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
