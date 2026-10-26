# Ṣọmọlá (district 27): the buildings and their hand passes

## Hand pass 2 (26 Oct): houses, storeys and kinds

**1,988 houses**, each with a kind and storeys; they cover 16.7% of the district (221,935 m²; Agunda 15.2%,
Ayégúnlẹ̀ 16.0%, Sọ̀rọ̀lérè 15.0%, Ìtìrí 18.8%). The real cover was not measured here; filling up is owed to the look
pass (NOW), as the other districts'.

How, in Agunda's order (no change to any builder; drafts on scratch copies of map/d27):

1. **Skeleton draft** on the 18 main roads, service roads and expressways (12 main roads, 4 expressway pieces, 2
   ramps): 1,496 houses.
2. **The cut** (the road comes first): each house minus every carriageway of Ṣọmọlá and its drawn neighbour Mùṣá
   + 0.05 m, and minus Mùṣá's houses; 947 were cut (the note gives the m² before and after), 310 left under 12 m² or
   a third of themselves were not written: **1,186 kept** (12.1% of the district). Footprints the draft left crossing
   themselves were mended before the cut. One house whose first point lay on the border (b-11fb83a4) was started at
   a point inside it, as the check asks.
3. **Frontage** (`draft_buildings.py --frontage`, blocks still empty only): 804 drafted in 148 blocks (the table
   below), cut the same way: 7 cut, 2 not written, **802 kept**.
4. **The board's own test** (web/mapedit.js boardProblems, headless, Ṣọmọlá with the five drawn districts): 194
   flagged (64 on a road, 130 overlaps), then 50, 2, 0: houses grazing a carriageway or a neighbour cut
   again to the carriageway + 0.1 m and a party wall 0.05 m off the larger neighbour or a Mùṣá house (158 houses,
   79.1 m² in all, the most 2.2 m²); the 48 where a lane ends at or bends by their wall cut to that road's
   round-ended carriageway + 0.1 m (50 cuts, two of them cut twice, none dropped); two houses that only touched (b-d93274f8 and
   b-8b24b6ce) given a party wall 0.05 m apart; one footprint the cuts left crossing itself (b-4440c655) mended
   (119.1 m²).
5. **Storeys**: `draft_storeys.py` found sources for 1,454 and **read 1,358** (1: 268, 2: 952, 3: 123, 4: 15); 5 read
   5 or more and were left; `draft_storeys_nearby.py` gave 557 more their neighbours' median (the 5 tall readings
   among them, now 2 storeys); the last 73 had no house with storeys within 30 m and were set by hand to their 5
   nearest houses' median (Ṣọmọlá's and Mùṣá's), noted on each. Of the 5 tall readings, three are 29-39 m², too small
   to be 5 storeys; the two larger (b-5097e7c0, 166 m², and b-7c249835, 169 m²) are owed a look on Street View (NOW).
   Storeys: 1: 385, 2: 1,442, 3: 143, 4: 18.
6. **Kinds** (`draft_kinds.py`): compound_house 1,286, face_me_bungalow 311, shack 146, walkup 130,
   shop_under_flats 102, kiosk_row 10, shed 3.

## The frontage draft: real houses on a road

| block | houses | covered | on a road at (Gidi x, y) |
|---|---|---|---|
| 0 | already drawn: skipped | | |
| 1 | already drawn: skipped | | |
| 2 | already drawn: skipped | | |
| 3 | already drawn: skipped | | |
| 4 | already drawn: skipped | | |
| 5 | 28 | 27% |  |
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
| 30 | 20 | 53% |  |
| 31 | already drawn: skipped | | |
| 32 | already drawn: skipped | | |
| 33 | already drawn: skipped | | |
| 34 | already drawn: skipped | | |
| 35 | already drawn: skipped | | |
| 36 | 22 | 59% |  |
| 37 | already drawn: skipped | | |
| 38 | already drawn: skipped | | |
| 39 | already drawn: skipped | | |
| 40 | already drawn: skipped | | |
| 41 | already drawn: skipped | | |
| 42 | already drawn: skipped | | |
| 43 | 13 | 63% |  |
| 44 | already drawn: skipped | | |
| 45 | already drawn: skipped | | |
| 46 | already drawn: skipped | | |
| 47 | already drawn: skipped | | |
| 48 | 13 | 48% |  |
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
| 97 | 15 | 47% |  |
| 98 | already drawn: skipped | | |
| 99 | already drawn: skipped | | |
| 100 | already drawn: skipped | | |
| 101 | 17 | 63% |  |
| 102 | 18 | 68% |  |
| 103 | already drawn: skipped | | |
| 104 | already drawn: skipped | | |
| 105 | already drawn: skipped | | |
| 106 | already drawn: skipped | | |
| 107 | already drawn: skipped | | |
| 108 | already drawn: skipped | | |
| 109 | 12 | 62% |  |
| 110 | already drawn: skipped | | |
| 111 | already drawn: skipped | | |
| 112 | already drawn: skipped | | |
| 113 | already drawn: skipped | | |
| 114 | 12 | 69% |  |
| 115 | 16 | 62% |  |
| 116 | already drawn: skipped | | |
| 117 | 10 | 59% |  |
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
| 128 | already drawn: skipped | | |
| 129 | already drawn: skipped | | |
| 130 | already drawn: skipped | | |
| 131 | already drawn: skipped | | |
| 132 | already drawn: skipped | | |
| 133 | already drawn: skipped | | |
| 134 | already drawn: skipped | | |
| 135 | already drawn: skipped | | |
| 136 | already drawn: skipped | | |
| 137 | 12 | 65% |  |
| 138 | already drawn: skipped | | |
| 139 | already drawn: skipped | | |
| 140 | already drawn: skipped | | |
| 141 | 13 | 63% |  |
| 142 | 16 | 53% |  |
| 143 | already drawn: skipped | | |
| 144 | already drawn: skipped | | |
| 145 | 14 | 62% |  |
| 146 | already drawn: skipped | | |
| 147 | already drawn: skipped | | |
| 148 | already drawn: skipped | | |
| 149 | already drawn: skipped | | |
| 150 | 9 | 61% |  |
| 151 | already drawn: skipped | | |
| 152 | already drawn: skipped | | |
| 153 | already drawn: skipped | | |
| 154 | already drawn: skipped | | |
| 155 | already drawn: skipped | | |
| 156 | already drawn: skipped | | |
| 157 | 8 | 63% |  |
| 158 | 11 | 57% |  |
| 159 | already drawn: skipped | | |
| 160 | already drawn: skipped | | |
| 161 | 11 | 55% |  |
| 162 | already drawn: skipped | | |
| 163 | already drawn: skipped | | |
| 164 | already drawn: skipped | | |
| 165 | already drawn: skipped | | |
| 166 | already drawn: skipped | | |
| 167 | already drawn: skipped | | |
| 168 | already drawn: skipped | | |
| 169 | already drawn: skipped | | |
| 170 | already drawn: skipped | | |
| 171 | 12 | 67% |  |
| 172 | already drawn: skipped | | |
| 173 | already drawn: skipped | | |
| 174 | already drawn: skipped | | |
| 175 | 6 | 59% |  |
| 176 | already drawn: skipped | | |
| 177 | already drawn: skipped | | |
| 178 | already drawn: skipped | | |
| 179 | 9 | 47% |  |
| 180 | already drawn: skipped | | |
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
| 194 | 6 | 40% |  |
| 195 | already drawn: skipped | | |
| 196 | already drawn: skipped | | |
| 197 | already drawn: skipped | | |
| 198 | already drawn: skipped | | |
| 199 | already drawn: skipped | | |
| 200 | already drawn: skipped | | |
| 201 | already drawn: skipped | | |
| 202 | already drawn: skipped | | |
| 203 | already drawn: skipped | | |
| 204 | already drawn: skipped | | |
| 205 | already drawn: skipped | | |
| 206 | 13 | 65% |  |
| 207 | already drawn: skipped | | |
| 208 | already drawn: skipped | | |
| 209 | already drawn: skipped | | |
| 210 | already drawn: skipped | | |
| 211 | 6 | 54% |  |
| 212 | already drawn: skipped | | |
| 213 | already drawn: skipped | | |
| 214 | already drawn: skipped | | |
| 215 | already drawn: skipped | | |
| 216 | already drawn: skipped | | |
| 217 | already drawn: skipped | | |
| 218 | 7 | 58% |  |
| 219 | already drawn: skipped | | |
| 220 | already drawn: skipped | | |
| 221 | already drawn: skipped | | |
| 222 | already drawn: skipped | | |
| 223 | already drawn: skipped | | |
| 224 | already drawn: skipped | | |
| 225 | 7 | 54% |  |
| 226 | 8 | 57% |  |
| 227 | already drawn: skipped | | |
| 228 | already drawn: skipped | | |
| 229 | already drawn: skipped | | |
| 230 | already drawn: skipped | | |
| 231 | already drawn: skipped | | |
| 232 | 10 | 64% |  |
| 233 | already drawn: skipped | | |
| 234 | already drawn: skipped | | |
| 235 | already drawn: skipped | | |
| 236 | already drawn: skipped | | |
| 237 | already drawn: skipped | | |
| 238 | 7 | 58% |  |
| 239 | already drawn: skipped | | |
| 240 | 10 | 60% |  |
| 241 | already drawn: skipped | | |
| 242 | already drawn: skipped | | |
| 243 | already drawn: skipped | | |
| 244 | 6 | 61% |  |
| 245 | already drawn: skipped | | |
| 246 | already drawn: skipped | | |
| 247 | already drawn: skipped | | |
| 248 | already drawn: skipped | | |
| 249 | already drawn: skipped | | |
| 250 | already drawn: skipped | | |
| 251 | 7 | 54% |  |
| 252 | already drawn: skipped | | |
| 253 | 6 | 57% |  |
| 254 | already drawn: skipped | | |
| 255 | already drawn: skipped | | |
| 256 | already drawn: skipped | | |
| 257 | 6 | 61% |  |
| 258 | already drawn: skipped | | |
| 259 | already drawn: skipped | | |
| 260 | already drawn: skipped | | |
| 261 | 7 | 60% |  |
| 262 | 8 | 54% |  |
| 263 | 8 | 56% |  |
| 264 | already drawn: skipped | | |
| 265 | already drawn: skipped | | |
| 266 | already drawn: skipped | | |
| 267 | already drawn: skipped | | |
| 268 | already drawn: skipped | | |
| 269 | already drawn: skipped | | |
| 270 | already drawn: skipped | | |
| 271 | 5 | 56% |  |
| 272 | already drawn: skipped | | |
| 273 | already drawn: skipped | | |
| 274 | already drawn: skipped | | |
| 275 | already drawn: skipped | | |
| 276 | already drawn: skipped | | |
| 277 | already drawn: skipped | | |
| 278 | 7 | 64% |  |
| 279 | already drawn: skipped | | |
| 280 | 7 | 57% |  |
| 281 | already drawn: skipped | | |
| 282 | already drawn: skipped | | |
| 283 | already drawn: skipped | | |
| 284 | 5 | 53% |  |
| 285 | already drawn: skipped | | |
| 286 | already drawn: skipped | | |
| 287 | already drawn: skipped | | |
| 288 | already drawn: skipped | | |
| 289 | already drawn: skipped | | |
| 290 | already drawn: skipped | | |
| 291 | 7 | 73% |  |
| 292 | already drawn: skipped | | |
| 293 | 11 | 57% |  |
| 294 | already drawn: skipped | | |
| 295 | already drawn: skipped | | |
| 296 | 4 | 52% |  |
| 297 | already drawn: skipped | | |
| 298 | already drawn: skipped | | |
| 299 | 7 | 61% |  |
| 300 | 2 | 62% |  |
| 301 | already drawn: skipped | | |
| 302 | already drawn: skipped | | |
| 303 | already drawn: skipped | | |
| 304 | already drawn: skipped | | |
| 305 | already drawn: skipped | | |
| 306 | already drawn: skipped | | |
| 307 | 6 | 54% |  |
| 308 | already drawn: skipped | | |
| 309 | already drawn: skipped | | |
| 310 | already drawn: skipped | | |
| 311 | already drawn: skipped | | |
| 312 | already drawn: skipped | | |
| 313 | 4 | 56% |  |
| 314 | already drawn: skipped | | |
| 315 | already drawn: skipped | | |
| 316 | already drawn: skipped | | |
| 317 | already drawn: skipped | | |
| 318 | already drawn: skipped | | |
| 319 | already drawn: skipped | | |
| 320 | 8 | 66% |  |
| 321 | 4 | 77% |  |
| 322 | already drawn: skipped | | |
| 323 | 7 | 47% |  |
| 324 | already drawn: skipped | | |
| 325 | already drawn: skipped | | |
| 326 | 5 | 56% |  |
| 327 | already drawn: skipped | | |
| 328 | already drawn: skipped | | |
| 329 | already drawn: skipped | | |
| 330 | 6 | 53% |  |
| 331 | already drawn: skipped | | |
| 332 | already drawn: skipped | | |
| 333 | already drawn: skipped | | |
| 334 | 5 | 49% |  |
| 335 | 4 | 61% |  |
| 336 | already drawn: skipped | | |
| 337 | already drawn: skipped | | |
| 338 | already drawn: skipped | | |
| 339 | already drawn: skipped | | |
| 340 | 6 | 64% |  |
| 341 | already drawn: skipped | | |
| 342 | 6 | 67% |  |
| 343 | 4 | 52% |  |
| 344 | already drawn: skipped | | |
| 345 | 4 | 18% |  |
| 346 | already drawn: skipped | | |
| 347 | 3 | 46% |  |
| 348 | already drawn: skipped | | |
| 349 | already drawn: skipped | | |
| 350 | 7 | 60% |  |
| 351 | already drawn: skipped | | |
| 352 | 7 | 63% |  |
| 353 | 6 | 50% |  |
| 354 | already drawn: skipped | | |
| 355 | already drawn: skipped | | |
| 356 | already drawn: skipped | | |
| 357 | 5 | 41% |  |
| 358 | 4 | 53% |  |
| 359 | 5 | 66% |  |
| 360 | already drawn: skipped | | |
| 361 | 6 | 62% |  |
| 362 | already drawn: skipped | | |
| 363 | 5 | 53% |  |
| 364 | 5 | 59% |  |
| 365 | already drawn: skipped | | |
| 366 | already drawn: skipped | | |
| 367 | already drawn: skipped | | |
| 368 | 4 | 43% |  |
| 369 | already drawn: skipped | | |
| 370 | 4 | 36% |  |
| 371 | already drawn: skipped | | |
| 372 | 4 | 78% |  |
| 373 | 3 | 54% |  |
| 374 | already drawn: skipped | | |
| 375 | 6 | 54% |  |
| 376 | already drawn: skipped | | |
| 377 | already drawn: skipped | | |
| 378 | already drawn: skipped | | |
| 379 | already drawn: skipped | | |
| 380 | 0 | 0% |  |
| 381 | already drawn: skipped | | |
| 382 | 6 | 57% |  |
| 383 | 7 | 62% |  |
| 384 | 5 | 36% |  |
| 385 | already drawn: skipped | | |
| 386 | 5 | 52% |  |
| 387 | already drawn: skipped | | |
| 388 | 4 | 40% |  |
| 389 | already drawn: skipped | | |
| 390 | 2 | 58% |  |
| 391 | already drawn: skipped | | |
| 392 | already drawn: skipped | | |
| 393 | 3 | 60% |  |
| 394 | 5 | 68% |  |
| 395 | already drawn: skipped | | |
| 396 | already drawn: skipped | | |
| 397 | already drawn: skipped | | |
| 398 | already drawn: skipped | | |
| 399 | 6 | 44% |  |
| 400 | 5 | 61% |  |
| 401 | already drawn: skipped | | |
| 402 | already drawn: skipped | | |
| 403 | already drawn: skipped | | |
| 404 | 3 | 66% |  |
| 405 | 5 | 49% |  |
| 406 | already drawn: skipped | | |
| 407 | already drawn: skipped | | |
| 408 | 6 | 53% |  |
| 409 | already drawn: skipped | | |
| 410 | 4 | 46% |  |
| 411 | already drawn: skipped | | |
| 412 | 3 | 67% |  |
| 413 | already drawn: skipped | | |
| 414 | already drawn: skipped | | |
| 415 | 4 | 50% |  |
| 416 | 5 | 60% |  |
| 417 | already drawn: skipped | | |
| 418 | already drawn: skipped | | |
| 419 | already drawn: skipped | | |
| 420 | already drawn: skipped | | |
| 421 | already drawn: skipped | | |
| 422 | 6 | 71% |  |
| 423 | already drawn: skipped | | |
| 424 | 4 | 66% |  |
| 425 | 3 | 28% |  |
| 426 | 4 | 67% |  |
| 427 | already drawn: skipped | | |
| 428 | already drawn: skipped | | |
| 429 | 4 | 49% |  |
| 430 | already drawn: skipped | | |
| 431 | 4 | 58% |  |
| 432 | 4 | 47% |  |
| 433 | already drawn: skipped | | |
| 434 | already drawn: skipped | | |
| 435 | 4 | 51% |  |
| 436 | already drawn: skipped | | |
| 437 | already drawn: skipped | | |
| 438 | already drawn: skipped | | |
| 439 | 3 | 67% |  |
| 440 | already drawn: skipped | | |
| 441 | 3 | 49% |  |
| 442 | 4 | 58% |  |
| 443 | 4 | 50% |  |
| 444 | 5 | 47% |  |
| 445 | 3 | 47% |  |
| 446 | already drawn: skipped | | |
| 447 | 3 | 62% |  |
| 448 | 2 | 37% |  |
| 449 | already drawn: skipped | | |
| 450 | 4 | 52% |  |
| 451 | 2 | 11% |  |
| 452 | 3 | 56% |  |
| 453 | 2 | 57% |  |
| 454 | 1 | 40% |  |
| 455 | already drawn: skipped | | |
| 456 | already drawn: skipped | | |
| 457 | already drawn: skipped | | |
| 458 | 2 | 71% |  |
| 459 | 3 | 54% |  |
| 460 | 2 | 48% |  |
| 461 | already drawn: skipped | | |
| 462 | 3 | 67% |  |
| 463 | 3 | 60% |  |
| 464 | already drawn: skipped | | |
| 465 | already drawn: skipped | | |
| 466 | 3 | 37% |  |
| 467 | 1 | 56% |  |
| 468 | 3 | 45% |  |
| 469 | 2 | 42% |  |
| 470 | 3 | 36% |  |
| 471 | already drawn: skipped | | |
| 472 | 3 | 47% |  |
| 473 | 4 | 74% |  |
| 474 | 1 | 58% |  |
| 475 | already drawn: skipped | | |
| 476 | 2 | 40% |  |
| 477 | 1 | 36% |  |
| 478 | already drawn: skipped | | |
| 479 | 3 | 50% |  |
| 480 | 3 | 49% |  |
| 481 | 2 | 31% |  |
| 482 | 5 | 50% |  |
| 483 | 5 | 60% |  |
| 484 | 1 | 70% |  |
| 485 | 3 | 73% |  |
| 486 | 1 | 55% |  |
| 487 | 2 | 21% |  |
| 488 | already drawn: skipped | | |
| 489 | 1 | 56% |  |
| 490 | already drawn: skipped | | |
| 491 | 3 | 36% |  |
| 492 | 3 | 45% |  |
| 493 | 2 | 44% |  |
| 494 | already drawn: skipped | | |
| 495 | 1 | 69% |  |
| 496 | already drawn: skipped | | |
| 497 | already drawn: skipped | | |
| 498 | 1 | 57% |  |
| 499 | 2 | 37% |  |
| 500 | 1 | 22% |  |
| 501 | 1 | 12% |  |
| 502 | already drawn: skipped | | |
