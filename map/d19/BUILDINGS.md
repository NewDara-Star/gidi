# Makoro (district 19): the buildings and their hand passes

## Hand pass 4 (27 Oct): the landmark, walled with a gate

Gbàgede's hand pass 4 recipe, as Saba's and Lagoon University's, on Overture's land use in Gidi metres, searched over
Makoro's own box (3.379-3.401 E, 6.486-6.513 N): each ground less the carriageways along it (Makoro's and its
neighbours') is a plot, a wall 0.2 m inside its edge, open where houses close it, a gate across each road that
enters or else one 4 m gate where it comes nearest a road. Overture has **one** landmark ground here: a hospital
compound, **pl-makf546e**, 146 m² of outline, 130 m² of plot once the carriageways are off. Its wall is 2 pieces,
26.2 m of the 44.6 m edge (the rest is closed by 3 houses standing on the edge, none cut), with one 4 m sheet-steel
gate (no road enters it). No school ground, market or church ground in Overture's land use in Makoro; its churches
and schools stand as places on their houses (hand pass 3).

The board's own test (web/mapedit.js boardProblems, headless, all ten drawn districts): **0**. check_map: 25157
records, 0 problems. working_bar d19: PASS (landmark plots 1).

The map picture (27 Oct, looked at): no land between districts left unclaimed (0.000 km²). Makoro's east half, to
the lagoon, is houses with no roads between them, by eye: the stilt town reached by water; its canoe landings and
water ways are owed (NOW). The near view still frames badly: the drawing sits in a box in its middle with blank
round it (the tool's fix is owed, NOW).

## Hand pass 3 (27 Oct): the real places

The real places (Overture) with a kind the game uses (`working_bar.place_kind`, Mùṣá's hand pass 55 rules), and by
hand, as Saba, the real churches whose Overture category names a denomination. Placed by Saba's hand pass 3 rules:
43 real points, **44 places**: church 34, school 6, bar 1, clinic 1, buka 1 and a bus stop by hand. Makoro reads as
it should: a town of many small churches (by count; not checked against a picture).

- On the house their point stands in or the nearest within 8 m: 29 places on 27 houses (b-9b421f39 and b-6e93ef95
  each carry a church and a school (both real points stand in the house; a church school, by guess); each house links one). The clinic's point has no open
  ground within 15 m, so it is on its nearest house, 8.2 m off. The other 14 as 6 m squares at their point, moved up
  to 14.0 m off roads and houses.
- By hand: pc-ac587e36 (a church) sat 10.5 m off its real point, past the bar's 10 m: its point is in a junction
  ringed by carriageways and no 6 m square fits nearer, so it is a 5 m square 9.2 m off.
- The first run used Lagoon University's search box (copied with its script) and found 23 of the 43 points; the
  working bar named the 20 missing; the box was set to Makoro's, those 23 places and 14 links taken out, and the
  places drawn again. Every real place now has a place of its kind within 10 m (working bar: PASS).
- **No bus stop or motor park is in Overture inside Makoro** (the nearest transport point, a taxi service, is 43 m
  outside). By hand, one stop on its spine street where it comes in at the border (rd-1ddbc022, local_main, 407 m),
  a 6 m square on the street's edge 56 m in, clear of carriageways, houses and places. The water side's canoe landings
  and stops are owed to a study of the map (NOW), with Saba's and Lagoon University's.

## Hand pass 2 (27 Oct): houses, storeys and kinds

**286 houses**, each with a kind and storeys; they cover 13.1% of the district (33,973 m²; Saba 14.4%, Lagoon
University 7.3%). The real cover was not measured; filling up is owed to the look pass (NOW), as the other districts'.

How, in Saba's order (no change to any builder; drafts on scratch copies of map/d19):

1. **Skeleton draft** on Makoro's 5 main roads and Saba's 1 main road within 60 m (rd-1c10b064; Lagoon
   University has none within 60 m): 278 houses.
2. **The cut** (the road comes first): each house minus every carriageway of Makoro, Saba and Lagoon University
   + 0.05 m, and minus their houses; 111 were cut, 32 left under 12 m² or a third of themselves were not written:
   **246 kept**.
3. **Frontage** (`draft_buildings.py --frontage`, blocks still empty only): the draft's log counts 44 in 8 blocks (the
   table below) but wrote 41 (the drafter's party-wall step trims each new house back to an overlapping house already
   drawn or a bigger new one, and drops what is left under 12 m²: 3 went there); those 41 were cut the same way: none
   cut, none dropped, **41 kept**.
4. **Slivers and road ends** (houses on a carriageway, half width - 0.05 m with round ends, cut to the carriageway +
   0.1 m, and to a party wall 0.05 m off a larger neighbour): 32 houses, 460 m² in all (the most 76.0 m²; read back
   from the houses' notes), and one house left with too little was dropped (287 -> 286). A second, third and fourth
   run cut nothing.
5. **By hand**: b-b90fb95d stands wholly inside the district but its first corner was on the border line, which the
   map check counts as outside; its points now start at the next corner (the same shape).
6. **The board's own test** (web/mapedit.js boardProblems, headless, Makoro with the nine districts at the bar):
   **0**.
7. **Storeys**: `draft_storeys.py` **read 160** (1: 50, 2: 93, 3: 14, 4: 3) and 8 read 5 or more and were left;
   `draft_storeys_nearby.py` gave 100 more their neighbours' median (1: 35, 2: 61, 4: 4); the last 26 had no house
   with storeys within 30 m and were set by hand to their 5 nearest houses' median (Makoro's, Saba's and Lagoon
   University's), noted on each (1: 1, 2: 17, 3: 1, 4: 7). The 8 tall readings (7 of them in the north-east corner
   around 14280-14350, 7040-7100, now 3 or 4 storeys; b-0dcdd67b now 2) are owed a look on Street View (NOW): a
   lagoon-edge town of 4-storey blocks is not what the study shows. Storeys: 1: 86, 2: 171, 3: 15, 4: 14.
8. **Kinds** (`draft_kinds.py`): compound_house 153, face_me_bungalow 66, walkup 26, shack 22, shop_under_flats 16,
   shed 2, kiosk_row 1.

## The frontage draft: real houses on a road

| block | houses (the draft's log; 44, of which 41 written) | covered | on a road |
|---|---|---|---|
| 5 | 17 | 51% | 0 |
| 16 | 9 | 54% | 0 |
| 26 | 4 | 42% | 0 |
| 27 | 3 | 39% | 0 |
| 29 | 2 | 21% | 0 |
| 31 | 4 | 51% | 0 |
| 32 | 3 | 18% | 0 |
| 33 | 2 | 77% | 0 |

The other blocks were already drawn by the skeleton or have no real house in them.
