# Ayégúnlẹ̀ (district 9): the buildings and their hand passes

## Hand pass 3 (26 Oct): the real places

284 real places (Overture) have a kind the game uses (`working_bar.place_kind`, Mùṣá's hand pass 55 rules), by
Sọ̀rọ̀lérè's hand pass 3 rules. **262 places**: church 158, school 51, clinic 18, mosque 13, bar 10, buka 4, fuel 3,
garage 2, bus_stop 2, police 1.

- 156 on the house their point stands in or the nearest within 8 m; 18 real places shared a house and kind with
  another, so one place serves both. 147 houses carry a place link.
- 3 with no open ground within 15 m of their point, on their nearest house (9.0-21.1 m off).
- 103 as 6 m squares at their point (the 2 bus stops, which stand on the street, and the rest in open ground with no
  house within 8 m), moved up to 15 m off roads and houses; their buildings are owed to the look pass, as Ìtìrí's.
- Only two bus stops are in Overture here and no motor park: Ayégúnlẹ̀'s stops and parks (Boundary, Mosafejo, the
  expressway stops) are owed to a study of the map (NOW).

## Hand pass 2 (26 Oct): houses, storeys and kinds

**1,472 houses**, each with a kind and storeys; they cover 16.0% of the district (222,791 m²; Sọ̀rọ̀lérè 15.0%, Ìtìrí
18.8%). The real cover was not measured here; filling up is owed to the look pass (NOW), as the other districts'.

How, in Sọ̀rọ̀lérè's order (no change to any builder; drafts on scratch copies of map/d09):

1. **Skeleton draft** on the 39 main roads, service roads and the two expressways: 1,367 houses.
2. **The cut** (the road comes first): each house minus every Ayégúnlẹ̀ carriageway + 0.05 m; 939 were cut (the note
   gives the m² before and after), 206 left under 12 m² or a third of themselves were not written: **1,161 kept**
   (14.2% of the district). No neighbour is drawn, so no neighbour's houses to keep off.
3. **Frontage** (`draft_buildings.py --frontage`, blocks still empty only): **311 houses** in 81 blocks (the table
   below); 3 cut back off a carriageway or a house, none dropped.
4. **The board's own test** (web/mapedit.js boardProblems, headless): 131 flagged (67 overlaps, 64 on a road), then 50,
   2, 0: houses grazing a carriageway or a neighbour cut again to the carriageway + 0.1 m and a party wall 0.05 m off
   the larger neighbour (121 houses, 91.8 m² in all, the most 4.8 m²); the 52 where a lane ends at or bends by
   their wall cut to that road's round-ended carriageway + 0.1 m.
5. **Storeys**: `draft_storeys.py` found sources for 765 and read none: its first Open Buildings tile over Ayégúnlẹ̀
   (tile_HKIm1T8zqO4) has no built pixels here and the script then skips the overlapping tile that has them
   (tile_qNSfrvnK9X8). The same reading was run from a scratch copy that goes on to the next tile (one line; the
   draft script itself unchanged, its fix owed, NOW): **691 read** (1: 157, 2: 446, 3: 77, 4: 11), 10 read 5 or
   more and left; `draft_storeys_nearby.py` gave 537 more their neighbours' median (56 small ones 1 storey before
   the reading); the last 188 (3 of the tall readings among them) had no house with storeys within 30 m and were set
   by hand to their 5 nearest houses' median, noted on each. Of the 10 tall readings (5+ storeys, 15-34 m), 9 were checked by eye on the satellite and Street View (study only,
   26 Oct):
   the six by the Maracana ground and canal stand on tin shacks, long sheds and stands, so the reading was blur: set by
   hand to 1-2 storeys with a fitting kind (a shed, 2 shacks and a bungalow of 1, 2 compound houses of 2);
   the two on Iganmu Road are 2-storey shop rows (one 3-storey block nearby), so their 2 stays; the Amukoko one keeps 3
   (2-3 storey rows); the last keeps the common 2 without being looked at. Each changed house's note says so.
   Storeys after the check: 1: 468, 2: 890, 3: 101, 4: 13 (before it 464, 888, 106, 14).
6. **Kinds** (`draft_kinds.py`): compound_house 807, face_me_bungalow 403, walkup 104, shop_under_flats 85, shack 54,
   shed 15, kiosk_row 4 (after the height check: 6 walkups became the low kinds above).

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
| 48 | 17 | 48% |  |
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
| 67 | already drawn: skipped | | |
| 68 | already drawn: skipped | | |
| 69 | already drawn: skipped | | |
| 70 | already drawn: skipped | | |
| 71 | 18 | 50% |  |
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
| 97 | already drawn: skipped | | |
| 98 | already drawn: skipped | | |
| 99 | already drawn: skipped | | |
| 100 | already drawn: skipped | | |
| 101 | already drawn: skipped | | |
| 102 | already drawn: skipped | | |
| 103 | already drawn: skipped | | |
| 104 | already drawn: skipped | | |
| 105 | already drawn: skipped | | |
| 106 | already drawn: skipped | | |
| 107 | already drawn: skipped | | |
| 108 | already drawn: skipped | | |
| 109 | already drawn: skipped | | |
| 110 | already drawn: skipped | | |
| 111 | already drawn: skipped | | |
| 112 | already drawn: skipped | | |
| 113 | already drawn: skipped | | |
| 114 | already drawn: skipped | | |
| 115 | already drawn: skipped | | |
| 116 | already drawn: skipped | | |
| 117 | already drawn: skipped | | |
| 118 | already drawn: skipped | | |
| 119 | already drawn: skipped | | |
| 120 | already drawn: skipped | | |
| 121 | already drawn: skipped | | |
| 122 | already drawn: skipped | | |
| 123 | already drawn: skipped | | |
| 124 | already drawn: skipped | | |
| 125 | already drawn: skipped | | |
| 126 | already drawn: skipped | | |
| 127 | already drawn: skipped | | |
| 128 | 11 | 73% |  |
| 129 | already drawn: skipped | | |
| 130 | already drawn: skipped | | |
| 131 | already drawn: skipped | | |
| 132 | already drawn: skipped | | |
| 133 | already drawn: skipped | | |
| 134 | already drawn: skipped | | |
| 135 | 12 | 65% |  |
| 136 | already drawn: skipped | | |
| 137 | already drawn: skipped | | |
| 138 | already drawn: skipped | | |
| 139 | already drawn: skipped | | |
| 140 | already drawn: skipped | | |
| 141 | already drawn: skipped | | |
| 142 | already drawn: skipped | | |
| 143 | 10 | 42% |  |
| 144 | already drawn: skipped | | |
| 145 | already drawn: skipped | | |
| 146 | already drawn: skipped | | |
| 147 | already drawn: skipped | | |
| 148 | already drawn: skipped | | |
| 149 | already drawn: skipped | | |
| 150 | 3 | 9% |  |
| 151 | already drawn: skipped | | |
| 152 | already drawn: skipped | | |
| 153 | already drawn: skipped | | |
| 154 | already drawn: skipped | | |
| 155 | already drawn: skipped | | |
| 156 | already drawn: skipped | | |
| 157 | 6 | 25% |  |
| 158 | already drawn: skipped | | |
| 159 | already drawn: skipped | | |
| 160 | 6 | 51% |  |
| 161 | already drawn: skipped | | |
| 162 | already drawn: skipped | | |
| 163 | already drawn: skipped | | |
| 164 | already drawn: skipped | | |
| 165 | already drawn: skipped | | |
| 166 | already drawn: skipped | | |
| 167 | already drawn: skipped | | |
| 168 | already drawn: skipped | | |
| 169 | already drawn: skipped | | |
| 170 | 7 | 45% |  |
| 171 | 9 | 71% |  |
| 172 | already drawn: skipped | | |
| 173 | already drawn: skipped | | |
| 174 | already drawn: skipped | | |
| 175 | already drawn: skipped | | |
| 176 | already drawn: skipped | | |
| 177 | already drawn: skipped | | |
| 178 | already drawn: skipped | | |
| 179 | already drawn: skipped | | |
| 180 | 11 | 65% |  |
| 181 | already drawn: skipped | | |
| 182 | already drawn: skipped | | |
| 183 | already drawn: skipped | | |
| 184 | already drawn: skipped | | |
| 185 | already drawn: skipped | | |
| 186 | already drawn: skipped | | |
| 187 | already drawn: skipped | | |
| 188 | already drawn: skipped | | |
| 189 | already drawn: skipped | | |
| 190 | already drawn: skipped | | |
| 191 | already drawn: skipped | | |
| 192 | already drawn: skipped | | |
| 193 | already drawn: skipped | | |
| 194 | already drawn: skipped | | |
| 195 | 3 | 28% |  |
| 196 | 8 | 55% |  |
| 197 | already drawn: skipped | | |
| 198 | already drawn: skipped | | |
| 199 | already drawn: skipped | | |
| 200 | 6 | 69% |  |
| 201 | already drawn: skipped | | |
| 202 | already drawn: skipped | | |
| 203 | 6 | 63% |  |
| 204 | already drawn: skipped | | |
| 205 | already drawn: skipped | | |
| 206 | already drawn: skipped | | |
| 207 | 5 | 68% |  |
| 208 | already drawn: skipped | | |
| 209 | already drawn: skipped | | |
| 210 | already drawn: skipped | | |
| 211 | already drawn: skipped | | |
| 212 | already drawn: skipped | | |
| 213 | already drawn: skipped | | |
| 214 | 6 | 40% |  |
| 215 | already drawn: skipped | | |
| 216 | 4 | 36% |  |
| 217 | already drawn: skipped | | |
| 218 | 6 | 39% |  |
| 219 | already drawn: skipped | | |
| 220 | 2 | 44% |  |
| 221 | already drawn: skipped | | |
| 222 | 4 | 47% |  |
| 223 | already drawn: skipped | | |
| 224 | already drawn: skipped | | |
| 225 | already drawn: skipped | | |
| 226 | 5 | 65% |  |
| 227 | already drawn: skipped | | |
| 228 | 4 | 55% |  |
| 229 | already drawn: skipped | | |
| 230 | 6 | 59% |  |
| 231 | 2 | 55% |  |
| 232 | already drawn: skipped | | |
| 233 | 2 | 70% |  |
| 234 | already drawn: skipped | | |
| 235 | already drawn: skipped | | |
| 236 | already drawn: skipped | | |
| 237 | already drawn: skipped | | |
| 238 | already drawn: skipped | | |
| 239 | already drawn: skipped | | |
| 240 | already drawn: skipped | | |
| 241 | 4 | 62% |  |
| 242 | 3 | 67% |  |
| 243 | 3 | 39% |  |
| 244 | already drawn: skipped | | |
| 245 | 6 | 53% |  |
| 246 | already drawn: skipped | | |
| 247 | already drawn: skipped | | |
| 248 | already drawn: skipped | | |
| 249 | 4 | 51% |  |
| 250 | 6 | 71% |  |
| 251 | already drawn: skipped | | |
| 252 | already drawn: skipped | | |
| 253 | already drawn: skipped | | |
| 254 | already drawn: skipped | | |
| 255 | 5 | 50% |  |
| 256 | already drawn: skipped | | |
| 257 | already drawn: skipped | | |
| 258 | 5 | 58% |  |
| 259 | already drawn: skipped | | |
| 260 | already drawn: skipped | | |
| 261 | already drawn: skipped | | |
| 262 | 3 | 40% |  |
| 263 | already drawn: skipped | | |
| 264 | already drawn: skipped | | |
| 265 | 5 | 44% |  |
| 266 | 3 | 53% |  |
| 267 | already drawn: skipped | | |
| 268 | already drawn: skipped | | |
| 269 | 1 | 24% |  |
| 270 | already drawn: skipped | | |
| 271 | already drawn: skipped | | |
| 272 | already drawn: skipped | | |
| 273 | 4 | 58% |  |
| 274 | already drawn: skipped | | |
| 275 | already drawn: skipped | | |
| 276 | 7 | 53% |  |
| 277 | already drawn: skipped | | |
| 278 | already drawn: skipped | | |
| 279 | already drawn: skipped | | |
| 280 | 4 | 34% |  |
| 281 | 5 | 44% |  |
| 282 | 5 | 55% |  |
| 283 | 6 | 56% |  |
| 284 | already drawn: skipped | | |
| 285 | 3 | 47% |  |
| 286 | already drawn: skipped | | |
| 287 | 1 | 33% |  |
| 288 | 5 | 59% |  |
| 289 | already drawn: skipped | | |
| 290 | 4 | 51% |  |
| 291 | already drawn: skipped | | |
| 292 | already drawn: skipped | | |
| 293 | 2 | 36% |  |
| 294 | 0 | 0% |  |
| 295 | 4 | 40% |  |
| 296 | already drawn: skipped | | |
| 297 | 1 | 4% |  |
| 298 | 1 | 33% |  |
| 299 | 4 | 61% |  |
| 300 | 4 | 48% |  |
| 301 | 2 | 18% |  |
| 302 | 2 | 53% |  |
| 303 | 3 | 49% |  |
| 304 | 0 | 0% |  |
| 305 | already drawn: skipped | | |
| 306 | 3 | 25% |  |
| 307 | already drawn: skipped | | |
| 308 | already drawn: skipped | | |
| 309 | 3 | 45% |  |
| 310 | 3 | 64% |  |
| 311 | already drawn: skipped | | |
| 312 | 0 | 0% |  |
| 313 | already drawn: skipped | | |
| 314 | 2 | 47% |  |
| 315 | already drawn: skipped | | |
| 316 | 3 | 46% |  |
| 317 | already drawn: skipped | | |
| 318 | 1 | 55% |  |
| 319 | already drawn: skipped | | |
| 320 | already drawn: skipped | | |
| 321 | 2 | 26% |  |
| 322 | 1 | 7% |  |
| 323 | 3 | 42% |  |
| 324 | 3 | 27% |  |
| 325 | 2 | 56% |  |
| 326 | 3 | 50% |  |
| 327 | 2 | 23% |  |
| 328 | 1 | 14% |  |
| 329 | 1 | 15% |  |
| 330 | already drawn: skipped | | |
| 331 | 1 | 31% |  |
| 332 | 2 | 65% |  |
| 333 | 1 | 62% |  |
| 334 | 3 | 56% |  |
| 335 | 2 | 53% |  |
| 336 | already drawn: skipped | | |
| 337 | 1 | 59% |  |
