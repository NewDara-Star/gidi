# Ìtìrí: the buildings draft and its hand pass

## Hand pass 4 (26 Oct): the landmarks with walls and gates, and the board's own house test

**Landmarks** (a one-off scratch script, not kept), from Overture's land use in Gidi metres, as LUTH (Mùṣá hand pass 63): each ground
less the carriageways along it is a plot, a wall 0.2 m inside its edge, open where houses close it. No road enters any of
them, so each has one 4 m gate where its wall comes nearest a road. 4 plots, 6 wall records, 4 gates:

| plot | what | m² | wall m (of the edge) | houses inside, linked |
|---|---|---|---|---|
| pl-itr259e9 | school ground (its place pc-itr259e9), sheet steel gate | 2086 | 146.7 of 190.9 | 0 |
| pl-itrbb775 | school ground (its place pc-itrbb775), sheet steel gate | 998 | 72.2 of 129.0 | 1 |
| pl-itr58634 | factory compound, 2.8 m with razor wire, sheet steel gate | 5945 | 295.2 of 330.6 | 3 |
| pl-itr4b3a8 | church ground, bar gate | 501 | 80.9 of 122.9 | 1 |

Left out: a 210 m² pitch (not walled). The grounds' buildings (classrooms, sheds) are owed to the look pass.

**The board's own test** (web/mapedit.js boardProblems: a house on a carriageway with round bends and flat ends, or on
another house) flagged houses that check_map passes, by slivers: 4 house pairs overlapping by up to 0.7 m² (trimmed
to a party wall); then 43 Ìtìrí houses with slivers the earlier cuts' simplify left (re-cut unsimplified to the
carriageway + 0.1 m and 0.05 m off the larger neighbour, 30.8 m² in all, at most 2.5 m² a house); then 18 whose corner
sat at a lane's flat end or bend (notched, then cut 0.15 m past the end; at most 2.6 m² a house). Five Ìtìrí roads repeated a point (rd-4388eab9,
rd-7fd4aeca, rd-8078760d, rd-95e589a5, rd-c9abda39); the repeats went. The same test run headless (node, the board's
own functions on both districts' records): 0.

## Hand pass 3 (26 Oct): the real places, the bus stops and the Itire Road Motor Park

218 real places (Overture) have a kind the game uses (`working_bar.place_kind`, Mùṣá's hand pass 55 rules). **202
places**: church 104, school 33, clinic 21, buka 10, mosque 9, bar 8, bank 6, fuel 4, garage 3, bus_stop 2, police 1,
motor_park 1.

- 130 on the house their point stands in or the nearest within 8 m (one place per house and kind; 19 points shared a
  house and kind with another; 122 houses linked to their place).
- 4 with no open ground within 15 m of their point on their nearest house (8.8 to 10.1 m off; one, a bar 40.6 m off,
  was replaced as below).
- 65 as 6 m squares at their point (the 2 bus stops, which stand on the street, and 63 in open ground with no house
  within 8 m), moved up to 11.5 m off roads and houses; their buildings are owed to the look pass, as Mùṣá's six.
- A church and a bar whose shared point lies on the expressway 5 m from the border: two 6 m squares on open ground at
  the motorway's edge, 21.5 m from the point (the bar measures a point on a road from its edge).
- **Itire Road Motor Park** (owner, 26 Oct, "Remember this"; Google Maps, study only, 6.51381,3.33419): its point is
  1.0 m from Adeniyi Street's centreline. As Mùṣá's danfo park (hand pass 59), a 6 m strip on the street's edge, 30 m
  along it at the point, on the side with no houses (the other would take 62.5 m² of houses), cut back from the side
  streets crossing it: 13.5 m along the street left, 80.5 m², pc-itrpark1; hours 05-23, a guess.

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
