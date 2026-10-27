# Saba (district 17): the buildings and their hand passes

## Hand pass 2 (27 Oct): houses, storeys and kinds

**831 houses**, each with a kind and storeys; they cover 14.4% of the district (101,824 m²; Ṣọmọlá 16.7%, Gbàgede
13.0%). The real cover was not measured here; filling up is owed to the look pass (NOW), as the other districts'.

How, in Gbàgede's order (no change to any builder; drafts on scratch copies of map/d17):

1. **Skeleton draft** on Saba's 23 main roads and the 8 main roads and expressways of its neighbours within 60 m
   (Mùṣá's expressway among them): 616 houses.
2. **The cut** (the road comes first): each house minus every carriageway of Saba and its drawn neighbours Ṣọmọlá,
   Mùṣá and Sọ̀rọ̀lérè + 0.05 m, and minus their houses; 380 were cut, 118 left under 12 m² or a third of themselves
   were not written: **498 kept**.
3. **Frontage** (`draft_buildings.py --frontage`, blocks still empty only): 334 drafted in 74 blocks (the table
   below), cut the same way: 11 cut, none dropped, **334 kept**.
4. **Slivers and road ends**, before the board's test this time: houses on a carriageway (half width - 0.05 m, round
   ends, as the board draws a lane that stops at a wall) cut to the carriageway + 0.1 m, and to a party wall 0.05 m
   off a larger neighbour: 105 houses, 1,654 m² in all (most of it where a lane ends at a house's wall, about 21 m²
   each; the most 150 m², where the cut left the house in two and the larger piece was kept); one (b-2efeaddd) left
   with too little and dropped. A second run cut nothing.
5. **The board's own test** (web/mapedit.js boardProblems, headless, Saba with the seven districts at the bar): **0**.
6. **Storeys**: `draft_storeys.py` **read 489** (1: 100, 2: 321, 3: 60, 4: 8) and 2 read 5 or more and were left;
   `draft_storeys_nearby.py` gave 289 more their neighbours' median (the 2 tall readings among them, now 2 storeys);
   the last 53 had no house with storeys within 30 m and were set by hand to their 5 nearest houses' median (Saba's
   and its neighbours'), noted on each. Of the 2 tall readings, b-1b827014 is 40 m², too small to be 5 storeys;
   b-e9b783b2 (143 m²) is owed a look on Street View (NOW). Storeys: 1: 187, 2: 562, 3: 74, 4: 8.
7. **Kinds** (`draft_kinds.py`): compound_house 433, face_me_bungalow 154, shop_under_flats 123, walkup 64, shack 44,
   kiosk_row 7, shed 6.

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
| 8 | already drawn: skipped | | |
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
| 19 | already drawn: skipped | | |
| 20 | already drawn: skipped | | |
| 21 | already drawn: skipped | | |
| 22 | already drawn: skipped | | |
| 23 | already drawn: skipped | | |
| 24 | already drawn: skipped | | |
| 25 | already drawn: skipped | | |
| 26 | already drawn: skipped | | |
| 27 | already drawn: skipped | | |
| 28 | 19 | 57% |  |
| 29 | already drawn: skipped | | |
| 30 | already drawn: skipped | | |
| 31 | already drawn: skipped | | |
| 32 | already drawn: skipped | | |
| 33 | already drawn: skipped | | |
| 34 | already drawn: skipped | | |
| 35 | already drawn: skipped | | |
| 36 | already drawn: skipped | | |
| 37 | already drawn: skipped | | |
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
| 50 | 15 | 56% |  |
| 51 | already drawn: skipped | | |
| 52 | already drawn: skipped | | |
| 53 | already drawn: skipped | | |
| 54 | 4 | 38% |  |
| 55 | already drawn: skipped | | |
| 56 | 2 | 12% |  |
| 57 | already drawn: skipped | | |
| 58 | 8 | 50% |  |
| 59 | already drawn: skipped | | |
| 60 | already drawn: skipped | | |
| 61 | 6 | 43% |  |
| 62 | already drawn: skipped | | |
| 63 | already drawn: skipped | | |
| 64 | already drawn: skipped | | |
| 65 | already drawn: skipped | | |
| 66 | 11 | 45% |  |
| 67 | already drawn: skipped | | |
| 68 | already drawn: skipped | | |
| 69 | already drawn: skipped | | |
| 70 | 10 | 60% |  |
| 71 | already drawn: skipped | | |
| 72 | already drawn: skipped | | |
| 73 | already drawn: skipped | | |
| 74 | already drawn: skipped | | |
| 75 | already drawn: skipped | | |
| 76 | already drawn: skipped | | |
| 77 | already drawn: skipped | | |
| 78 | already drawn: skipped | | |
| 79 | 8 | 69% |  |
| 80 | 9 | 67% |  |
| 81 | already drawn: skipped | | |
| 82 | already drawn: skipped | | |
| 83 | already drawn: skipped | | |
| 84 | 10 | 52% |  |
| 85 | already drawn: skipped | | |
| 86 | already drawn: skipped | | |
| 87 | already drawn: skipped | | |
| 88 | already drawn: skipped | | |
| 89 | 5 | 46% |  |
| 90 | already drawn: skipped | | |
| 91 | already drawn: skipped | | |
| 92 | already drawn: skipped | | |
| 93 | already drawn: skipped | | |
| 94 | already drawn: skipped | | |
| 95 | 7 | 51% |  |
| 96 | already drawn: skipped | | |
| 97 | already drawn: skipped | | |
| 98 | already drawn: skipped | | |
| 99 | already drawn: skipped | | |
| 100 | 10 | 69% |  |
| 101 | already drawn: skipped | | |
| 102 | already drawn: skipped | | |
| 103 | already drawn: skipped | | |
| 104 | already drawn: skipped | | |
| 105 | 7 | 47% |  |
| 106 | already drawn: skipped | | |
| 107 | already drawn: skipped | | |
| 108 | 10 | 60% |  |
| 109 | already drawn: skipped | | |
| 110 | already drawn: skipped | | |
| 111 | already drawn: skipped | | |
| 112 | already drawn: skipped | | |
| 113 | 6 | 48% |  |
| 114 | already drawn: skipped | | |
| 115 | 4 | 67% |  |
| 116 | already drawn: skipped | | |
| 117 | already drawn: skipped | | |
| 118 | already drawn: skipped | | |
| 119 | already drawn: skipped | | |
| 120 | 3 | 42% |  |
| 121 | already drawn: skipped | | |
| 122 | 9 | 62% |  |
| 123 | 3 | 25% |  |
| 124 | already drawn: skipped | | |
| 125 | already drawn: skipped | | |
| 126 | already drawn: skipped | | |
| 127 | already drawn: skipped | | |
| 128 | already drawn: skipped | | |
| 129 | 9 | 58% |  |
| 130 | 3 | 21% |  |
| 131 | 4 | 50% |  |
| 132 | already drawn: skipped | | |
| 133 | 4 | 73% |  |
| 134 | already drawn: skipped | | |
| 135 | 4 | 59% |  |
| 136 | already drawn: skipped | | |
| 137 | already drawn: skipped | | |
| 138 | 7 | 62% |  |
| 139 | already drawn: skipped | | |
| 140 | already drawn: skipped | | |
| 141 | already drawn: skipped | | |
| 142 | 4 | 52% |  |
| 143 | already drawn: skipped | | |
| 144 | already drawn: skipped | | |
| 145 | 9 | 70% |  |
| 146 | 3 | 63% |  |
| 147 | already drawn: skipped | | |
| 148 | already drawn: skipped | | |
| 149 | 3 | 61% |  |
| 150 | already drawn: skipped | | |
| 151 | 8 | 63% |  |
| 152 | 4 | 65% |  |
| 153 | 3 | 64% |  |
| 154 | 3 | 24% |  |
| 155 | already drawn: skipped | | |
| 156 | already drawn: skipped | | |
| 157 | 3 | 60% |  |
| 158 | already drawn: skipped | | |
| 159 | already drawn: skipped | | |
| 160 | already drawn: skipped | | |
| 161 | already drawn: skipped | | |
| 162 | already drawn: skipped | | |
| 163 | already drawn: skipped | | |
| 164 | already drawn: skipped | | |
| 165 | already drawn: skipped | | |
| 166 | 6 | 48% |  |
| 167 | already drawn: skipped | | |
| 168 | already drawn: skipped | | |
| 169 | 3 | 55% |  |
| 170 | already drawn: skipped | | |
| 171 | already drawn: skipped | | |
| 172 | 2 | 60% |  |
| 173 | already drawn: skipped | | |
| 174 | 5 | 57% |  |
| 175 | already drawn: skipped | | |
| 176 | 3 | 72% |  |
| 177 | 2 | 64% |  |
| 178 | 1 | 23% |  |
| 179 | already drawn: skipped | | |
| 180 | 4 | 48% |  |
| 181 | already drawn: skipped | | |
| 182 | 2 | 37% |  |
| 183 | already drawn: skipped | | |
| 184 | 2 | 60% |  |
| 185 | already drawn: skipped | | |
| 186 | 2 | 70% |  |
| 187 | already drawn: skipped | | |
| 188 | already drawn: skipped | | |
| 189 | already drawn: skipped | | |
| 190 | 3 | 58% |  |
| 191 | 3 | 55% |  |
| 192 | already drawn: skipped | | |
| 193 | 5 | 29% |  |
| 194 | 4 | 48% |  |
| 195 | 4 | 45% |  |
| 196 | 4 | 66% |  |
| 197 | 3 | 48% |  |
| 198 | 4 | 55% |  |
| 199 | 2 | 46% |  |
| 200 | 2 | 34% |  |
| 201 | already drawn: skipped | | |
| 202 | 4 | 57% |  |
| 203 | already drawn: skipped | | |
| 204 | 4 | 64% |  |
| 205 | 2 | 51% |  |
| 206 | already drawn: skipped | | |
| 207 | 3 | 73% |  |
| 208 | 3 | 51% |  |
| 209 | 2 | 41% |  |
| 210 | already drawn: skipped | | |
| 211 | already drawn: skipped | | |
| 212 | already drawn: skipped | | |
| 213 | already drawn: skipped | | |
| 214 | already drawn: skipped | | |
| 215 | already drawn: skipped | | |
| 216 | already drawn: skipped | | |
| 217 | 4 | 70% |  |
| 218 | already drawn: skipped | | |
| 219 | 3 | 49% |  |
| 220 | 3 | 64% |  |
| 221 | 3 | 42% |  |
| 222 | 2 | 35% |  |
| 223 | 4 | 47% |  |
| 224 | 2 | 33% |  |
| 225 | 3 | 50% |  |
| 226 | 3 | 51% |  |
| 227 | 3 | 30% |  |
| 228 | 1 | 15% |  |
| 229 | already drawn: skipped | | |
