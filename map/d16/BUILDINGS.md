# Ìbùdó Mẹ́ta (district 16): the buildings and their hand passes

## Hand pass 2 (27 Oct): houses, storeys and kinds

**402 houses**, each with a kind and storeys; they cover 11.4% of the district (54,279 m² of 475,276 m²; Makoro
13.1%, Saba 14.4%). The real cover was not measured; filling up is owed to the look pass (NOW), as the other
districts'. The cleared sawmill ground (NOW, the owner's call) is drawn with the landmarks.

How, in Makoro's order (no change to any builder; drafts on scratch copies of map/d16):

1. **Skeleton draft** on Ìbùdó Mẹ́ta's 32 main roads and 13 of Saba's and Makoro's main roads within 60 m: 294 houses.
2. **The cut** (the road comes first): each house minus every carriageway of Ìbùdó Mẹ́ta, Saba and Makoro + 0.05 m,
   and minus their houses; 155 were cut, 55 left under 12 m² or a third of themselves were not written: **239 kept**.
3. **Frontage** (`draft_buildings.py --frontage`, blocks still empty only): the draft's log counts 176 in 45 blocks
   (the table below) but wrote 164 (the drafter's party-wall step trims each new house back to an overlapping house
   and drops what is left under 12 m²); those 164 were cut the same way: 3 cut, none dropped, **164 kept**.
4. **Slivers and road ends** (houses on a carriageway, half width - 0.05 m with round ends, cut to the carriageway +
   0.1 m, and to a party wall 0.05 m off a larger neighbour): 53 houses, 681.2 m² in all (the most 186.2 m²; read
   back from the houses' notes), and one house left with too little was dropped (403 -> 402). A second, third and
   fourth run cut nothing.
5. **By hand**: b-1718d74a stands wholly inside the district but its first corner was on the border line, which the
   map check counts as outside; its points now start at the next corner (the same shape).
6. **The board's own test** (web/mapedit.js boardProblems, headless, all eleven drawn districts): first run: one pair, b-40794727 and b-b44c323c, touching along a wall (shared area 0.0000002 m²); b-b44c323c pulled 5 cm off by hand (43.40 → 43.24 m²); second run: **0 problems**.
7. **Storeys**: `draft_storeys.py` **read 243** (1: 42, 2: 151, 3: 46, 4: 4) and one read 5 or more (b-c0559b50)
   and was left; `draft_storeys_nearby.py` gave 138 more their neighbours' median (1: 30, 2: 88, 3: 18, 4: 2; the
   tall reading among them, now 2); the last 21 had no house with storeys within 30 m and were set by hand to their 5
   nearest houses' median (Ìbùdó Mẹ́ta's, Saba's and Makoro's), noted on each (1: 3, 2: 16, 3: 1, 4: 1). The tall
   reading is owed a look on Street View (NOW). Storeys: 1: 75, 2: 255, 3: 65, 4: 7.
8. **Kinds** (`draft_kinds.py`): compound_house 204, face_me_bungalow 63, walkup 56, shop_under_flats 55, shack 21,
   kiosk_row 2, shed 1.

## The frontage draft: real houses on a road

| block | houses (the draft's log; 176, of which 164 written) | covered | on a road |
|---|---|---|---|
| 14 | 11 | 60% | 0 |
| 16 | 10 | 56% | 0 |
| 18 | 10 | 42% | 0 |
| 22 | 5 | 53% | 0 |
| 23 | 5 | 57% | 0 |
| 26 | 5 | 78% | 0 |
| 30 | 6 | 26% | 0 |
| 37 | 6 | 54% | 0 |
| 38 | 4 | 67% | 0 |
| 39 | 6 | 75% | 0 |
| 41 | 5 | 66% | 0 |
| 46 | 3 | 62% | 0 |
| 49 | 4 | 52% | 0 |
| 51 | 3 | 67% | 0 |
| 58 | 7 | 72% | 0 |
| 59 | 2 | 75% | 0 |
| 60 | 7 | 66% | 0 |
| 61 | 4 | 64% | 0 |
| 70 | 5 | 64% | 0 |
| 71 | 3 | 74% | 0 |
| 76 | 3 | 60% | 0 |
| 77 | 7 | 65% | 0 |
| 82 | 3 | 56% | 0 |
| 89 | 3 | 64% | 0 |
| 94 | 4 | 57% | 0 |
| 96 | 4 | 28% | 0 |
| 97 | 5 | 53% | 0 |
| 98 | 4 | 63% | 0 |
| 101 | 3 | 47% | 0 |
| 102 | 4 | 37% | 0 |
| 103 | 2 | 47% | 0 |
| 104 | 2 | 18% | 0 |
| 106 | 2 | 42% | 0 |
| 108 | 1 | 11% | 0 |
| 110 | 2 | 65% | 0 |
| 111 | 1 | 66% | 0 |
| 112 | 1 | 9% | 0 |
| 113 | 1 | 19% | 0 |
| 119 | 2 | 37% | 0 |
| 120 | 2 | 27% | 0 |
| 121 | 3 | 51% | 0 |
| 124 | 1 | 43% | 0 |
| 126 | 3 | 49% | 0 |
| 128 | 1 | 20% | 0 |
| 129 | 1 | 27% | 0 |

The other blocks were already drawn by the skeleton or have no real house in them.
