# Ìtìrí: the buildings draft and its hand pass

## Hand pass 2 (26 Oct): houses, storeys and kinds

**687 houses**, each with a kind and storeys; they cover 18.8% of the district. The real buildings under it (Microsoft
footprints at real size) cover 37.5%, about the same as under Mùṣá (37.6%), so Ìtìrí's houses are about half as dense as
the real ones. This is the working bar (every house a kind and storeys); filling up is owed to the look pass (NOW).

How, in Mùṣá's order (its draft ran on 62 skeleton streets, its lanes came after):

1. **Every street first, tried and thrown away.** `draft_buildings.py` on all 367 roads wrote 297 houses (13.5% of the
   land between the roads). With every real street at full width on a 1:3 frame, most blocks are 13-20 m deep, less
   than many real houses, so the draft drops them.
2. **Skeleton drafts**, on scratch copies of map/d14 (no change to the builder): all roads but the unnamed lanes (188
   roads) gave 415 houses, 390 after the cut below (17.4% of the land); the 37 main roads, local mains, service roads
   and the motorway gave 649, **566 after the cut (23.9% of the land)**. The 37-road draft was kept.
3. **The cut** (the road comes first): each house minus every Ìtìrí carriageway + 0.05 m; 391 were cut (the note gives
   the m² before and after), 83 left under 12 m² or a third of themselves were not written.
4. **Frontage** (`draft_buildings.py --frontage`), which fills only blocks still empty: 122 houses in 35 blocks, each
   real house turned to face its street.
5. Two houses stood in Mùṣá's carriageways (the expressway rd-cjk9hvop and rd-sdso0qxv): b-7b503fbd was cut (64.8 to
   45.1 m²); b-5d86e840 (5.4 m² left) went.
6. **Storeys**: `draft_storeys.py` read 458 from the real source's Open Buildings 2.5D height (sources found for 479;
   one reading 5+, b-7aa9e512, was left for a check and then took its neighbours' 2 from `draft_storeys_nearby.py`: a
   Street View check is owed); `draft_storeys_nearby.py` 190; the 39 with no neighbour within 30 m were set by hand to
   Ìtìrí's commonest, 2 (1 under 30 m²), noted on each. Storeys: 1: 126, 2: 496, 3: 54, 4: 11.
7. **Kinds** (`draft_kinds.py`): compound_house 465, face_me_bungalow 110, walkup 60, shop_under_flats 22, shack 20,
   shed 6, kiosk_row 4.

## The 37-road skeleton draft: real houses on a road

| block | houses | covered | on a road at (Gidi x, y) |
|---|---|---|---|
| 0 | 508 | 29% | 12139, 6364; 12500, 6535; 11961, 6884 |
| 1 | 55 | 22% |  |
| 2 | 69 | 47% |  |
| 3 | 37 | 30% |  |
| 4 | 27 | 33% |  |
| 5 | 4 | 21% | 11809, 6628 |
| 6 | 0 | 0% |  |
| 7 | 0 | 0% |  |
| 8 | 0 | 0% |  |

## The frontage pass: blocks it filled

| block | houses | covered | on a road at (Gidi x, y) |
|---|---|---|---|
| 42 | 7 | 34% |  |
| 45 | 13 | 66% |  |
| 75 | 5 | 72% |  |
| 89 | 4 | 32% |  |
| 95 | 7 | 51% |  |
| 97 | 6 | 57% |  |
| 102 | 5 | 71% |  |
| 111 | 4 | 51% |  |
| 118 | 5 | 72% |  |
| 120 | 3 | 52% |  |
| 125 | 5 | 38% |  |
| 126 | 3 | 67% |  |
| 128 | 3 | 33% |  |
| 130 | 4 | 66% |  |
| 131 | 6 | 63% |  |
| 133 | 4 | 19% |  |
| 134 | 3 | 50% |  |
| 137 | 2 | 35% |  |
| 139 | 3 | 82% |  |
| 147 | 3 | 24% |  |
| 152 | 3 | 42% |  |
| 153 | 1 | 5% |  |
| 154 | 1 | 59% |  |
| 160 | 4 | 52% |  |
| 161 | 2 | 44% |  |
| 165 | 4 | 54% |  |
| 169 | 2 | 60% |  |
| 170 | 1 | 32% |  |
| 171 | 3 | 43% |  |
| 172 | 4 | 75% |  |
| 174 | 0 | 0% |  |
| 175 | 3 | 59% |  |
| 178 | 2 | 36% |  |
| 179 | 2 | 35% |  |
| 180 | 2 | 52% |  |
