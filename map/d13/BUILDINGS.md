# Sọ̀rọ̀lérè (district 13): the buildings and their hand passes

## Hand pass 4, places (26 Oct): the south lobe's real places

The lobe brought 83 more real places (234 in the district now). Hand pass 3's rules, run again over the whole district
(the older places come out the same; 3 had their area brought to their house's re-cut footprint): **76 new places**,
all in the lobe: church 31, clinic 18, school 10, buka 8, bar 7, mosque 1, garage 1.

- 44 on houses (36 lobe houses newly linked), 31 as 6 m squares in open ground.
- 1 buka by hand: its point at the border just past where Ìtìrí's Ogunlana Drive ends, its nearest house's buka 12.2 m
  off and no 6 m of open ground within 9 m, so its spot is the 65 m2 open strip by the street around its point.
- **219 places** in the district; 0 real places missing. No new bus stop or motor park in Overture here (still owed).

## Hand pass 4 (26 Oct): the south lobe's houses

The south lobe (STREETS.md hand pass 4) built as hand pass 2 built the rest, no builder changed: `draft_buildings.py`
on a scratch copy holding only the lobe and its 5 main-street records (Akerele Road and Randle Avenue among them), 151 houses, each then cut
back from every road's carriageway (+0.05 m) and off every house already drawn: **129 kept** (102 cut, 22 left out
under 12 m2 or a third of themselves). Then `--frontage` on a scratch copy of the whole district: 93 houses, all in the
lobe's still-empty blocks. **222 houses**, 24,079 m2, 17.2% of the lobe (the district now 15.0%).

- Two frontage houses stood on Mùṣá's side road rd-wavside1: cut back (26.2 -> 18.1 and 43.8 -> 41.6 m2).
- Storeys: 167 from 2.5D heights (no reading of 5+), 51 from neighbours within 30 m, 4 by hand (no source and no house
  within 30 m: 1 storey under 60 m2, else 2). 1: 64, 2: 142, 3: 14, 4: 2.
- Kinds (`draft_kinds.py`): compound_house 132, face_me_bungalow 55, shack 17, walkup 12, shop_under_flats 4, kiosk_row 2.
- The board's own test then flagged 24 (13 overlapping pairs, 11 on a road): slivers cut (28 houses, 20.1 m2, most
  4.0 m2), then the 11 cut to the round-ended carriageway + 0.1 m where a lane ends or bends at them; one older
  house, b-f4f4613f, lost 26.5 m2 where the lobe's rd-dc1b715f ends at it. Then 0.

## Hand pass 3 (26 Oct): the real places and the bus stop

151 real places (Overture) have a kind the game uses (`working_bar.place_kind`, Mùṣá's hand pass 55 rules). **143
places**: church 51, school 25, buka 21, clinic 19, bar 9, bank 5, mosque 5, garage 4, fuel 2, bus_stop 1, police 1.

- 89 on the house their point stands in or the nearest within 8 m, on 77 houses (11 hold two or more kinds; the
  house links the first). 8 real places shared a house and kind with another, so one place serves both.
- 1 with no open ground within 15 m of its point, on its nearest house (9.6 m off). 78 houses carry a place link.
- 53 as 6 m squares at their point (the bus stop, which stands on the street, and 52 in open ground with no house
  within 8 m), moved up to 14.5 m off roads and houses; their buildings are owed to the look pass, as Ìtìrí's.
- Only one bus stop is in Overture here, and no motor park: Ojuelegba's park and stops and Sọ̀rọ̀lérè's other stops
  (the stadium, Masha, Adeniran Ogunsanya) are owed to a study of the map (NOW).

## Hand pass 2 (26 Oct): houses, storeys and kinds

**518 houses**, each with a kind and storeys; they cover 14.4% of the district (76,366 m²; Ìtìrí 18.8%). The real
cover was not measured here; filling up is owed to the look pass (NOW), as Ìtìrí's.

How, in Ìtìrí's order (no change to any builder; drafts on scratch copies of map/d13):

1. **Three skeleton drafts tried**: 33 roads (motorway, main roads, local mains) gave 385 houses, 335 after the cut
   (11.2% of the district); 148 roads (adding the named home streets) 283, 259 after (9.2%); the 17 main roads and
   Western Avenue 401, **351 after the cut (12.1%)**. The 17-road draft was kept.
2. **The cut** (the road comes first): each house minus every Sọ̀rọ̀lérè, Ìtìrí and Mùṣá carriageway + 0.05 m and
   minus Ìtìrí's and Mùṣá's houses; 284 were cut (the note gives the m² before and after), 50 left under 12 m² or a
   third of themselves were not written. No simplifying; points rounded to 3 decimals, repeats dropped.
3. **Frontage** (`draft_buildings.py --frontage`, blocks still empty only): the table below counts 177 houses in 44 blocks before the draft's own party-wall trim (`party_walls`), which left 10
   swallowed by a neighbour or under 12 m², so **167 written** (replayed on a scratch copy: 177 before, 167 after).
4. **Storeys**: `draft_storeys.py` read 255 from Open Buildings 2.5D heights (sources found for 318); six read 5 or
   more (b-3cdd1cf8, b-4afb5a28, b-54e89275, b-5c40ea0c, b-bada8739, b-d12fcb8e) and took their neighbours' storeys
   from `draft_storeys_nearby.py` (185 in all); a Street View check of the six is owed (NOW). The 78 with no
   neighbour within 30 m were set by hand to 2 (1 under 30 m², 4 houses), noted on each. Storeys: 1: 121, 2: 330,
   3: 64, 4: 3.
5. **Kinds** (`draft_kinds.py`): compound_house 290, face_me_bungalow 102, walkup 55, shop_under_flats 35, shack 25,
   shed 8, kiosk_row 3.
6. **The board's own test** (web/mapedit.js boardProblems, headless): 48 flagged, then 25, 24 (houses grazing a
   carriageway or a neighbour: cut again to the carriageway + 0.1 m and a party wall 0.05 m off the larger neighbour,
   36.7 m² in all); the last 24 sat where a lane ends at or bends by their wall, cut to that road's round-ended
   carriageway + 0.1 m (496.7 m² in all, the most 153.4 m² off one compound); then 0.

## The frontage draft: real houses on a road

| block | houses | covered | on a road at (Gidi x, y) |
|---|---|---|---|
| 0 | already drawn: skipped | | |
| 1 | already drawn: skipped | | |
| 2 | already drawn: skipped | | |
| 3 | already drawn: skipped | | |
| 4 | already drawn: skipped | | |
| 5 | already drawn: skipped | | |
| 6 | already drawn: skipped | | |
| 7 | already drawn: skipped | | |
| 8 | 16 | 36% |  |
| 9 | already drawn: skipped | | |
| 10 | already drawn: skipped | | |
| 11 | already drawn: skipped | | |
| 12 | already drawn: skipped | | |
| 13 | already drawn: skipped | | |
| 14 | already drawn: skipped | | |
| 15 | already drawn: skipped | | |
| 16 | already drawn: skipped | | |
| 17 | already drawn: skipped | | |
| 18 | already drawn: skipped | | |
| 19 | 19 | 43% |  |
| 20 | already drawn: skipped | | |
| 21 | already drawn: skipped | | |
| 22 | already drawn: skipped | | |
| 23 | already drawn: skipped | | |
| 24 | already drawn: skipped | | |
| 25 | already drawn: skipped | | |
| 26 | already drawn: skipped | | |
| 27 | already drawn: skipped | | |
| 28 | already drawn: skipped | | |
| 29 | already drawn: skipped | | |
| 30 | already drawn: skipped | | |
| 31 | 10 | 48% |  |
| 32 | already drawn: skipped | | |
| 33 | already drawn: skipped | | |
| 34 | already drawn: skipped | | |
| 35 | already drawn: skipped | | |
| 36 | already drawn: skipped | | |
| 37 | 11 | 63% |  |
| 38 | already drawn: skipped | | |
| 39 | already drawn: skipped | | |
| 40 | already drawn: skipped | | |
| 41 | already drawn: skipped | | |
| 42 | already drawn: skipped | | |
| 43 | already drawn: skipped | | |
| 44 | already drawn: skipped | | |
| 45 | already drawn: skipped | | |
| 46 | already drawn: skipped | | |
| 47 | already drawn: skipped | | |
| 48 | already drawn: skipped | | |
| 49 | already drawn: skipped | | |
| 50 | already drawn: skipped | | |
| 51 | already drawn: skipped | | |
| 52 | already drawn: skipped | | |
| 53 | already drawn: skipped | | |
| 54 | already drawn: skipped | | |
| 55 | already drawn: skipped | | |
| 56 | already drawn: skipped | | |
| 57 | already drawn: skipped | | |
| 58 | already drawn: skipped | | |
| 59 | already drawn: skipped | | |
| 60 | already drawn: skipped | | |
| 61 | already drawn: skipped | | |
| 62 | already drawn: skipped | | |
| 63 | already drawn: skipped | | |
| 64 | already drawn: skipped | | |
| 65 | already drawn: skipped | | |
| 66 | already drawn: skipped | | |
| 67 | 4 | 45% |  |
| 68 | 8 | 63% |  |
| 69 | 8 | 47% |  |
| 70 | already drawn: skipped | | |
| 71 | already drawn: skipped | | |
| 72 | already drawn: skipped | | |
| 73 | already drawn: skipped | | |
| 74 | already drawn: skipped | | |
| 75 | 6 | 43% |  |
| 76 | 6 | 52% |  |
| 77 | already drawn: skipped | | |
| 78 | already drawn: skipped | | |
| 79 | already drawn: skipped | | |
| 80 | already drawn: skipped | | |
| 81 | 4 | 48% |  |
| 82 | already drawn: skipped | | |
| 83 | already drawn: skipped | | |
| 84 | 4 | 39% |  |
| 85 | 1 | 32% |  |
| 86 | already drawn: skipped | | |
| 87 | 5 | 60% |  |
| 88 | 3 | 24% |  |
| 89 | already drawn: skipped | | |
| 90 | 4 | 62% |  |
| 91 | 4 | 38% |  |
| 92 | 1 | 11% |  |
| 93 | 2 | 45% |  |
| 94 | 3 | 42% |  |
| 95 | 4 | 52% |  |
| 96 | 5 | 76% |  |
| 97 | already drawn: skipped | | |
| 98 | 3 | 45% |  |
| 99 | 0 | 0% |  |
| 100 | already drawn: skipped | | |
| 101 | already drawn: skipped | | |
| 102 | 4 | 55% |  |
| 103 | 2 | 23% |  |
| 104 | 2 | 16% |  |
| 105 | already drawn: skipped | | |
| 106 | already drawn: skipped | | |
| 107 | 2 | 60% |  |
| 108 | already drawn: skipped | | |
| 109 | 1 | 12% |  |
| 110 | 3 | 57% |  |
| 111 | 0 | 0% |  |
| 112 | 3 | 41% |  |
| 113 | 3 | 55% |  |
| 114 | 4 | 43% |  |
| 115 | 3 | 23% |  |
| 116 | 1 | 39% |  |
| 117 | 3 | 34% |  |
| 118 | already drawn: skipped | | |
| 119 | 3 | 45% |  |
| 120 | 2 | 21% |  |
| 121 | 5 | 52% |  |
| 122 | already drawn: skipped | | |
| 123 | 2 | 44% |  |
| 124 | 1 | 11% |  |
| 125 | 0 | 0% |  |
| 126 | 0 | 0% |  |
| 127 | 2 | 37% |  |
