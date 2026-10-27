# Ìbùdó Mẹ́ta (district 16): the buildings and their hand passes

## Hand pass 4 (27 Oct): the landmarks

**17 landmark plots**, each walled with a gate (working bar: PASS, 0 plots without a gated wall), and Oyingbo Market.

- **15 from Overture's land use** (in Gidi metres, less the carriageways along them; a wall 0.2 m inside the edge, open
  where houses close it, one 4 m gate where it comes nearest a road; Makoro's hand pass 4 rules): Iddo Market, the Otto
  side's market, St Jude's church ground and its primary school, Apena Cemetery, Ebute Metta Primary, St Saviour's School
  and two more school grounds (each school ground with its school place), and six yards (Overture `industrial`, not
  read further): five at the Iddo end by the Lagos Terminus, one by Otto.
- **Oyingbo Bus Terminal** from its real outline (Overture infrastructure, `bus_station`): a 1,207 m² compound with a
  motor park place on it.
- **Oyingbo Market** (b-oyingbom, `market_block`, 4 storeys, 565 m², and its market place): the real block read off
  Google satellite at 18z (study only). The picture was calibrated on two real points (Mainland Hotel and the Total
  station on Coates Street, Overture): 0.665 m a pixel both ways, the check point 0.4 m off. Both real market points
  fall on it (1.4 m and 0 m). The drafted houses gave way: b-59961128 and b-d9448d3c (wholly under it) and b-0d689aad
  and b-d3afa977 (under 20 m² left) removed, b-ed4bbfdb trimmed 0.2 m clear (119 to 64 m²). The buka on the removed
  house keeps its real point, now the market's food market.
- **The cleared sawmill ground at Oko-Baba** (owner: the real sawmill moved to Agbowa in May 2025, so clear it): pl-ibusawmi,
  8,825 m² of the waterfront block east of Oko-Baba Street, north of Ondo Street's line carried on to the lagoon (the
  real yards run on further south; that part stays the town's). Four drafted houses removed; the largest, b-e6189a77,
  kept as the sawmill's broken shed. A sheet hoarding along its road sides (552 m of 718 m), open to the lagoon, one 4 m
  gate. Its street-football pitch and canoe landing are owed to the look pass (NOW).
- **Not drawn yet:** the railway compound with Jaekel House, the Federal Medical Centre and the Oyingbo Red Line station
  share one block by the railway, which only Mùṣá has drawn; they come with the railway (NOW).

## Hand pass 3 (27 Oct): the real places

The real places (Overture) with a kind the game uses (`working_bar.place_kind`), and the real churches whose Overture
category names a denomination, placed by Saba's and Makoro's hand pass 3 rules: **98 places** (church 53, school 17,
buka 10, clinic 5, bar 3, fuel 3, bank 3, garage 2, mosque 1, police 1), 58 on the house their point stands in or the
nearest, 34 as squares at their point moved up to 14.5 m off roads and houses. Where two real points of one kind stand
in one house, one place serves both (14). Like Makoro, a town of many small churches (by count; not checked against a
picture).

- By hand: b-b56066ad (where a real bar, garage and church point stand together, 10.3 m off) grown 0.6 m toward the
  point (26.4 to 27.7 m²; 9.5 m off), and its three places' areas set to the new footprint.
- By hand, at the Saba seam: two real points sit on ground our neighbours' roads and houses fill. Each is a place on
  free ground inside Ìbùdó Mẹ́ta, 0.2 m clear of everything, no neighbour touched: a small roadside church (35.9 m²,
  2.5 m from its point) on the ground between the three main roads, and a fuel station's pumps (10.8 m², 7.4 m from its
  point) on the strip by the seam, the station running on into Saba.
- By hand, the **bus stop**: a 6 m square on the edge of rd-bc0c9c23 (main road), 9.3 m from the real Oyingbo Bus
  Terminal point; the terminal itself comes with the landmarks.
- Working bar: PASS (107 real places, 0 missing; 100 places; 1 bus stop).

## Hand pass 2 (27 Oct): houses, storeys and kinds

**402 houses**, each with a kind and storeys; they cover 11.4% of the district (54,279 m² of 475,276 m²; Makoro
13.1%, Saba 14.4%). The real cover, measured 27 Oct against Google Open Buildings v3 inside the same outline, is
26.4-30.5% (confidence 0.75-0.65): ours is a third to a half of it, so the district is not at the working bar under
the 27 Oct density rule; filling up comes in NOW item 16, by hand. The cleared sawmill ground (NOW, the owner's call) is drawn with the landmarks.

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
