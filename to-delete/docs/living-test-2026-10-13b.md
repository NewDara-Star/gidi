# City living test, 13 Oct 2026 (second run): the Maze, the Hub, Jungle City, Food Gate

This is the second run of `docs/CITY-LIVING-TEST.md` today. It covers the whole built city after the owner's five fixes and the new district, Food Gate.

There are two states:
- **Before:** `main` at the start of this work (commit `8401854`).
- **After:** this branch.

Both are measured with the same, corrected `explore_city.py`. Trips now start and end on the nearest point of a way, not the nearest junction, so the "before" numbers differ a little from the first run's.

Five Haiku agents ran on the after state:
- Tunde, okada rider (new persona: his room is now by the parts market)
- Mama Ronke, food seller on foot
- Kemi, a student in Jungle City
- **New:** Sule, a market porter in Food Gate
- **The chase:** the opening, run through the parts market

Every problem they reported was re-run and checked by hand before it went into this file.

## How life feels (short version)
- **The opening works.**
  - Tunde's room is a 2-minute walk from the stall where he steals.
  - The chase runs the length of the parts market down its aisle, comes out at the west end, and reaches the boss's park in about 5 minutes.
  - There are eight ways out of the market zone, so the boss's end is one option, not the only one.
- **Food Gate feels like a market town.**
  - A porter's walk from home to the market is under 8 minutes.
  - The market to the bus park is 6 minutes over the footbridge.
  - The okada reaches the Maze in under 4 minutes and the Hub's interchange in 5.
- **The rail is easier to cross in the Hub.** The short walks near the knot that were ×2.5–3.5 are now ×1.6–1.9.
- **What still grates:**
  - The Coastal Expressway in Jungle City: a mosque 46 m away is a 480 m walk, because the one footbridge is by the market.
  - Okadas can't use the footbridges and skywalks. That's by design, but rides between neighbouring landmarks run ×2–3.5.
  - The stadium's okada runs stay at ×2.1–2.6: the rail sits between it and the south.

## The days (shortened)
- **Tunde (okada):**
  - Room to Ladi Lane market: 2.6 minutes on foot. Boss's park to the market: 1.1 minutes by bike, or a 4-minute walk.
  - Ladi Lane to Mile Market: 3.8 minutes. Mile Market to Ireti Hotel: 7 minutes.
  - Interchange to station: 732 m by bike, but 220 m on foot over the skywalk, so he walks.
- **Mama Ronke (on foot, Hub):**
  - Home to Under the Bridge: 2.4 minutes. School: 2.5 minutes. Bank: 5 minutes. Mosque: 7 minutes.
  - Hub Rail Station: 4.4 minutes.
  - Mile Market is a 5-minute okada ride before dawn, or a 24-minute walk along Northern Road.
- **Kemi (Jungle City):**
  - From the south: Boundary Plank Market 2.7 minutes, secondary school 9.3 minutes.
  - From the north: the new North Primary School is next door, and the chemist and mosque are 5–6 minutes away.
  - The Maze is 13–15 minutes on foot, or about 3 minutes by okada.
- **Sule (porter, Food Gate):**
  - Home to Mile Market: 7.7 minutes. Market to Northern Bus Park: 6 minutes over the footbridge.
  - Freedom Ground: 9 minutes. The canoe jetty: 16 minutes on foot, or 3.6 by okada.
  - The Maze: 3.8 minutes by okada. The Hub's interchange: 4.6.
- **The chase:**
  - Room → stall: 161 m, 1.9 minutes.
  - Stall → the market's west end: 174 m, ×1.15 (after the fix below).
  - Stall → boss's park: 429 m, 5.1 minutes, ×1.29.
  - Escape directions N, NE, NW, W, SW, S, SE and E are all reachable, from three different first branches out of the stall.

## Standard trips
| Trip | Mode | Before: m / min / detour | After: m / min / detour |
|---|---|---|---|
| **Tunde's room → The steal** | walk | 1,705 / 20.5 / ×1.11 (room in Jungle City) | **161 / 1.9 / ×1.50** |
| **The steal → boss's motor park, through the market** | walk | 1,461 / 17.5 / ×1.13 (park in west Hub) | **429 / 5.1 / ×1.29** |
| The steal → Gang Canal | walk | 362 / 4.3 / ×1.60 | 496 / 6.0 / ×1.49 (the stall moved to the market) |
| Maze house by the rail → Ladi Lane Parts Market | walk | 828 / 9.9 / ×1.37 | 828 / 9.9 / ×1.37 |
| Gidi Interchange → Hub Rail Station | walk | 220 / 2.6 / ×1.04 | 220 / 2.6 / ×1.04 |
| Boss's motor park → Ladi Lane Parts Market | ride | 1,285 / 3.1 / ×1.24 | 477 / 1.1 / ×1.73 (park moved next to the market) |
| Under the Bridge → Daleko Grain Yard | walk | 1,222 / 14.7 / ×1.28 | 1,222 / 14.7 / ×1.28 |
| Jungle City centre → Gidi Interchange | ride | 2,201 / 5.3 / ×1.43 | 2,201 / 5.3 / ×1.43 |
| **Food Gate centre → Gidi Interchange (new)** | ride | no route (not built) | **2,100 / 5.0 / ×1.24** |
| Food Gate house (3100,3884) → Mile Market (new) | walk | — | 639 / 7.7 / ×1.18 |
| Mile Market → Northern Bus Park (new) | walk | — | 499 / 6.0 / ×1.43 |
| Mile Market → Ladi Lane Parts Market (new) | ride | — | 1,569 / 3.8 / ×1.33 |

## The owner's five fixes, before and after
| Fix | Measure | Before | After |
|---|---|---|---|
| 1. The opening | room → stall; stall → park; market's far end → park fence | 20.5 min; 17.5 min; ~1 km | **1.9 min; 5.1 min; ~170 m** |
| 1. The opening | ways out of the market zone | 6 | **8, in all four directions** |
| 2. Hub rail-side blocks | walk 1697,4272 → 1578,4229 | 449 m, ×3.55 | **208 m, ×1.64** |
| 2. Hub rail-side blocks | walk 1697,4272 → 1825,4180 | 400 m, ×2.54 | **294 m, ×1.87** |
| 2. Hub rail crossings | longest gap; crossings | 247 m; 8 | 254 m (along the industrial yard); **10** |
| 3. Daleko Grain Yard | walk Ladi Lane → Daleko | 763 m, ×1.75 | 763 m, ×1.75 (see note) |
| 4. National Bowl | ride from 1556,4411; from the Interchange | ×2.58; ×2.10 | ×2.58; ×2.10 (see note) |
| 5. North Jungle City | houses with a school within 10 min | 96% (worst 12.4 min) | **100%** |

**Notes:**
- **Fix 3:** the first run's ×2.40 came from the old tool snapping to junctions. The yard already filled a block with a street on its north side; it now has a recorded north gate. What's left is the rail.
- **Fix 4:** six vehicle roads already left the stadium's ring, and a second dedicated access now comes from the north. The long okada runs are the rail and the arterials at the knot, not the stadium's access.

## City measures
| | Before | After | Target |
|---|---|---|---|
| Longest walk between pedestrian rail crossings, Maze / Hub | 200 / 247 m | 200 / 254 m | 150–250 m |
| Walking islands inside the built districts | 0 | 0 | 0 |
| School within 10 min: Maze / Hub / Jungle City / Food Gate | 100 / 100 / 96 / — | 100 / 100 / 100 / 92% | 100%; up to 15 min accepted |
| Worship within 10 min | 100 / 100 / 100 / — | 100 / 100 / 99 / 99% | 100% |
| Chemist or clinic within 10 min | 100 / 100 / 100 / — | 100 / 100 / 100 / 98% | 100% |
| Worst walk to a school, Food Gate | — | 12.5 min | ≤ 15 min |
| `check_district.py`: Maze / Hub / Jungle City / Food Gate | pass | pass / pass / pass / pass | all pass |

## Verified problems (real), with coordinates
1. **Fixed: a double road beside the parts market.** An ordinary street ran 4–5 m from the market's own access road along its west side, and the two never joined, so the chase went round by Ring Road. Streets now stop at a big place's own road and snap onto it (`clear_access`, on in the Maze and Food Gate). `walk "The steal" 2500,4407` went from 265 m (×1.76) to 174 m (×1.15).
2. **Fixed: Food Gate's everyday places.** Civic places landed in clusters. Three schools, a mosque and three chemists were added as late places (on the nearest free plot, so no other pin moves). Before the fix: schools 66%, chemists 93%; worst school walk 18.1 minutes, from 3823,2915.
3. **Open: the Coastal Expressway splits Jungle City on foot.** `walk 3017,5225 3029,5181` (Hidaya Mosque) is 480 m for 46 m, ×10.5. The real rate is 0.3 footbridges per km, so only one stands, by the market. **Next session:** a second footbridge or a pedestrian crossing west of the market.
4. **Open: the Hub's rail gap along the industrial yard** is 254 m (target 250). The yard fills the rail side there, so a worn crossing would come out inside the fenced yard. **Next session:** a gate in the yard fence, or move the yard back from the line.
5. **Open: okada rides between neighbouring landmarks:**
   - Interchange → station: ×3.47
   - Mile Market → bus park: ×2.27
   - Under the Bridge → Interchange: ×2.42
   - National Bowl → hotel: ×2.18

   Walkers use the footbridges and skywalks, which bikes can't. The access roads of big places come out onto arterials at single points. **Next session:** a drop-off lay-by on the arterial side of the terminal, station and market.
6. **Open: Okafor Road (the Maze–Water Town edge road) crosses the rail at ground level** (seen on `ride "Mile Market" "Ireti Hotel"`). Real major roads bridge the rail 4 times in 6. **When Water Town is built:** decide on a bridge or a level crossing.
7. **Open: civic coverage is fragile.** Every regeneration of a district re-deals its civic places at random, and coverage can fall (the Hub went 99% → 89% → 95% during this work). **Next session:** place schools, places of worship and chemists by coverage, not at random.

## Tool artefacts (not city problems)
- **Islands at 2289,5243, 3304,5540, 1737,4959, 1364,3604 and 2465,3300:** all outside the built districts (`look` shows each one). They are the unbuilt neighbours' sketch roads cut at the study border.
- **"Footbridge 0.0 km"** in `overview`: the canal footbridges are 6–7 m long and the total rounds to zero. The road footbridges are counted as skywalks.
- **Name lookup picks the first match:** the far Harbour Bank, a Little Angels School in Jungle City. Use X,Y.
- **"Agboyi Creek Villages" by road:** the pin is the jetty's end. The villages themselves are on the water, reached by canoe.
- **Okada rides that "start 102 m off the network" at Mile Market:** the pin is in the middle of a 6.3 ha market, and bikes don't use its aisles.
- **"Northern Road outside the built districts"** between the Hub and Food Gate: about 90 m across the Capital's corner. The Capital is not built yet.
- **Houses "46 m from a way" (37 houses):** the tool measures to the house centre. `check_district.py` measures to the nearest wall, and every district passes.

## What was fixed in this session
- **The five owner fixes** (one commit each).
- **Food Gate built,** with its landmarks approved by the owner.
- **From this test:** the double road beside markets (`clear_access`), and Food Gate's everyday places.
- **Tool:** trips start and end on the nearest point of a way.
- **Generator:**
  - districts that share more than one edge keep one record per edge
  - parcels get gates
  - the Hub skywalk code no longer assumes an interchange
  - late civic places are placed after all districts
