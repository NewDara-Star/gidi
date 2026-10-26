# Gbàgede (district 28): the buildings and their hand passes

## Hand pass 2 (26 Oct): houses, storeys and kinds

**1,702 houses**, each with a kind and storeys; they cover 13.0% of the district (218,564 m²; Ṣọmọlá 16.7%,
Agunda 15.2%). The real cover was not measured here; filling up is owed to the look pass (NOW), as the other
districts'.

How, in Ṣọmọlá's order (no change to any builder; drafts on scratch copies of map/d28):

1. **Skeleton draft** on the 39 main roads, service roads and expressways (22 main roads, 3 expressway pieces, 14
   ramps and service roads): 1,661 houses.
2. **The cut** (the road comes first): each house minus every carriageway of Gbàgede and its drawn neighbour Ṣọmọlá
   + 0.05 m, and minus Ṣọmọlá's houses; 1,002 were cut, 269 left under 12 m² or a third of themselves were not
   written: **1,392 kept** (11.6% of the district).
3. **Frontage** (`draft_buildings.py --frontage`, blocks still empty only): 321 drafted in 65 blocks (the table
   below), cut the same way: 6 cut, 10 not written, **311 kept**. Two houses whose first point lay on the border
   (b-c6f2fd51, b-ffc412ec) were started at a corner inside it, as the check asks; their footprints did not change.
4. **The board's own test** (web/mapedit.js boardProblems, headless, Gbàgede with the six drawn districts): 160
   flagged (110 on a road, 50 overlaps), then 79 (all on a road), 5, 0: houses grazing a carriageway or a neighbour
   cut again to the carriageway + 0.1 m and a party wall 0.05 m off the larger neighbour (166 houses, 128.2 m² in
   all, the most 5.7 m²); the 83 where a lane ends at or bends by their wall cut to that road's round-ended
   carriageway + 0.1 m (78, then 5), one of them (b-291c45c7) left with too little and dropped.
5. **Storeys**: `draft_storeys.py` **read 903** (1: 183, 2: 591, 3: 113, 4: 11) and 5 read 5 or more and were left
   (898 written); `draft_storeys_nearby.py` gave 541 more their neighbours' median (the 5 tall readings among them,
   now 1-2 storeys); the last 263 had no house with storeys within 30 m and were set by hand to their 5 nearest
   houses' median (Gbàgede's and Ṣọmọlá's), noted on each. Of the 5 tall readings, three are 18-36 m², too small to
   be 5 storeys; the two larger (b-e058528f, 284 m², and b-ae17f158, 124 m², 57 m apart) are owed a look on Street
   View (NOW). Storeys: 1: 410, 2: 1,122, 3: 156, 4: 14.
6. **Kinds** (`draft_kinds.py`): compound_house 1,055, face_me_bungalow 317, shack 122, walkup 161,
   shop_under_flats 36, shed 6, kiosk_row 5.

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
| 28 | already drawn: skipped | | |
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
| 66 | 10 | 42% |  |
| 67 | already drawn: skipped | | |
| 68 | already drawn: skipped | | |
| 69 | already drawn: skipped | | |
| 70 | already drawn: skipped | | |
| 71 | already drawn: skipped | | |
| 72 | already drawn: skipped | | |
| 73 | already drawn: skipped | | |
| 74 | already drawn: skipped | | |
| 75 | already drawn: skipped | | |
| 76 | already drawn: skipped | | |
| 77 | already drawn: skipped | | |
| 78 | already drawn: skipped | | |
| 79 | already drawn: skipped | | |
| 80 | already drawn: skipped | | |
| 81 | already drawn: skipped | | |
| 82 | already drawn: skipped | | |
| 83 | already drawn: skipped | | |
| 84 | already drawn: skipped | | |
| 85 | already drawn: skipped | | |
| 86 | already drawn: skipped | | |
| 87 | already drawn: skipped | | |
| 88 | already drawn: skipped | | |
| 89 | already drawn: skipped | | |
| 90 | already drawn: skipped | | |
| 91 | already drawn: skipped | | |
| 92 | already drawn: skipped | | |
| 93 | already drawn: skipped | | |
| 94 | already drawn: skipped | | |
| 95 | already drawn: skipped | | |
| 96 | already drawn: skipped | | |
| 97 | 9 | 72% |  |
| 98 | already drawn: skipped | | |
| 99 | already drawn: skipped | | |
| 100 | 10 | 47% |  |
| 101 | already drawn: skipped | | |
| 102 | 12 | 57% |  |
| 103 | already drawn: skipped | | |
| 104 | 11 | 52% |  |
| 105 | already drawn: skipped | | |
| 106 | already drawn: skipped | | |
| 107 | already drawn: skipped | | |
| 108 | already drawn: skipped | | |
| 109 | already drawn: skipped | | |
| 110 | already drawn: skipped | | |
| 111 | 10 | 63% |  |
| 112 | already drawn: skipped | | |
| 113 | already drawn: skipped | | |
| 114 | already drawn: skipped | | |
| 115 | already drawn: skipped | | |
| 116 | already drawn: skipped | | |
| 117 | already drawn: skipped | | |
| 118 | 9 | 67% |  |
| 119 | already drawn: skipped | | |
| 120 | already drawn: skipped | | |
| 121 | already drawn: skipped | | |
| 122 | already drawn: skipped | | |
| 123 | already drawn: skipped | | |
| 124 | already drawn: skipped | | |
| 125 | already drawn: skipped | | |
| 126 | already drawn: skipped | | |
| 127 | already drawn: skipped | | |
| 128 | already drawn: skipped | | |
| 129 | already drawn: skipped | | |
| 130 | already drawn: skipped | | |
| 131 | already drawn: skipped | | |
| 132 | already drawn: skipped | | |
| 133 | 11 | 53% |  |
| 134 | already drawn: skipped | | |
| 135 | already drawn: skipped | | |
| 136 | already drawn: skipped | | |
| 137 | already drawn: skipped | | |
| 138 | already drawn: skipped | | |
| 139 | already drawn: skipped | | |
| 140 | already drawn: skipped | | |
| 141 | 7 | 67% |  |
| 142 | already drawn: skipped | | |
| 143 | already drawn: skipped | | |
| 144 | 6 | 75% |  |
| 145 | already drawn: skipped | | |
| 146 | 8 | 57% |  |
| 147 | already drawn: skipped | | |
| 148 | 8 | 67% |  |
| 149 | 6 | 65% |  |
| 150 | already drawn: skipped | | |
| 151 | already drawn: skipped | | |
| 152 | already drawn: skipped | | |
| 153 | already drawn: skipped | | |
| 154 | already drawn: skipped | | |
| 155 | already drawn: skipped | | |
| 156 | 7 | 67% |  |
| 157 | already drawn: skipped | | |
| 158 | 6 | 59% |  |
| 159 | already drawn: skipped | | |
| 160 | already drawn: skipped | | |
| 161 | already drawn: skipped | | |
| 162 | 6 | 65% |  |
| 163 | already drawn: skipped | | |
| 164 | already drawn: skipped | | |
| 165 | already drawn: skipped | | |
| 166 | 4 | 49% |  |
| 167 | already drawn: skipped | | |
| 168 | 8 | 51% |  |
| 169 | 6 | 63% |  |
| 170 | already drawn: skipped | | |
| 171 | 4 | 21% |  |
| 172 | 6 | 55% |  |
| 173 | already drawn: skipped | | |
| 174 | already drawn: skipped | | |
| 175 | 8 | 33% |  |
| 176 | 5 | 66% |  |
| 177 | 8 | 49% |  |
| 178 | 6 | 64% |  |
| 179 | 6 | 50% |  |
| 180 | already drawn: skipped | | |
| 181 | already drawn: skipped | | |
| 182 | already drawn: skipped | | |
| 183 | 5 | 54% |  |
| 184 | already drawn: skipped | | |
| 185 | already drawn: skipped | | |
| 186 | 8 | 57% |  |
| 187 | already drawn: skipped | | |
| 188 | already drawn: skipped | | |
| 189 | already drawn: skipped | | |
| 190 | 5 | 60% |  |
| 191 | already drawn: skipped | | |
| 192 | 6 | 35% |  |
| 193 | already drawn: skipped | | |
| 194 | already drawn: skipped | | |
| 195 | 6 | 65% |  |
| 196 | already drawn: skipped | | |
| 197 | already drawn: skipped | | |
| 198 | already drawn: skipped | | |
| 199 | 6 | 65% |  |
| 200 | already drawn: skipped | | |
| 201 | already drawn: skipped | | |
| 202 | already drawn: skipped | | |
| 203 | 6 | 57% |  |
| 204 | already drawn: skipped | | |
| 205 | already drawn: skipped | | |
| 206 | 5 | 52% |  |
| 207 | already drawn: skipped | | |
| 208 | already drawn: skipped | | |
| 209 | already drawn: skipped | | |
| 210 | already drawn: skipped | | |
| 211 | already drawn: skipped | | |
| 212 | 5 | 60% |  |
| 213 | 6 | 57% |  |
| 214 | already drawn: skipped | | |
| 215 | 4 | 46% |  |
| 216 | already drawn: skipped | | |
| 217 | 4 | 54% |  |
| 218 | 6 | 64% |  |
| 219 | already drawn: skipped | | |
| 220 | 4 | 60% |  |
| 221 | already drawn: skipped | | |
| 222 | already drawn: skipped | | |
| 223 | already drawn: skipped | | |
| 224 | 5 | 78% |  |
| 225 | already drawn: skipped | | |
| 226 | 3 | 23% |  |
| 227 | 4 | 56% |  |
| 228 | 5 | 56% |  |
| 229 | already drawn: skipped | | |
| 230 | already drawn: skipped | | |
| 231 | already drawn: skipped | | |
| 232 | 5 | 40% |  |
| 233 | already drawn: skipped | | |
| 234 | 3 | 68% |  |
| 235 | 5 | 52% |  |
| 236 | already drawn: skipped | | |
| 237 | already drawn: skipped | | |
| 238 | 2 | 68% |  |
| 239 | already drawn: skipped | | |
| 240 | already drawn: skipped | | |
| 241 | already drawn: skipped | | |
| 242 | 4 | 45% |  |
| 243 | 5 | 44% |  |
| 244 | 5 | 53% |  |
| 245 | 2 | 36% |  |
| 246 | 2 | 54% |  |
| 247 | 4 | 56% |  |
| 248 | 1 | 23% |  |
| 249 | already drawn: skipped | | |
| 250 | already drawn: skipped | | |
| 251 | 4 | 48% |  |
| 252 | already drawn: skipped | | |
| 253 | already drawn: skipped | | |
| 254 | 3 | 66% |  |
| 255 | 1 | 8% |  |
| 256 | 0 | 0% |  |
| 257 | 2 | 21% |  |
| 258 | 3 | 33% |  |
| 259 | 1 | 27% |  |
| 260 | 2 | 18% |  |
| 261 | already drawn: skipped | | |
| 262 | 1 | 24% |  |
| 263 | already drawn: skipped | | |
| 264 | 3 | 46% |  |
