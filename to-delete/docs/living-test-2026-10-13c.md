# City living test, 13 Oct 2026 (third run): all five districts

This is the third run of `docs/CITY-LIVING-TEST.md` today. It is the first run with all five built districts: the Maze, the Hub, Jungle City, Food Gate and the new Water Town.

There are two states:
- **Before:** `main` at the start of this work (commit `f044853`).
- **After:** this branch.

Both were measured with the same `explore_city.py`.

Six Haiku agents ran on the after state:
- Tunde, okada rider
- Mama Ronke, food seller on foot (the Hub)
- Kemi, a student in Jungle City
- Sule, a night porter in Food Gate
- **New:** Bola, a canoe paddler who lives in Water Town's stilt village
- **The chase:** the opening, run through the parts market

I re-ran every problem they reported and checked it by hand before it went into this file.

## How life feels (short version)
- **The opening is now fixed in place.** Tunde's room, the stall, the market aisles and the boss's motor park are locked. Regenerating the Maze or the Hub keeps them where they are, and `check_district.py` fails if any of them move.
- **Everyday life is within reach everywhere.**
  - In all five districts, every home (stilt huts included) has a school, a place of worship and a chemist or clinic within 10 minutes' walk.
  - This now survives regeneration, because the places are placed by coverage, not at random.
- **Jungle City's expressway is easier on foot.**
  - A second footbridge stands west of the market.
  - The reported walk from 3017,5225 to 3029,5181 went from 480 m to 147 m.
- **Water Town works as a place.**
  - From the stilt village, the Canoe Jetty is 12 minutes' walk and Mile Market 14.
  - An okada reaches the Interchange in 5 minutes.
  - The Stilt Bar is a few steps from the huts.
- **What still grates:**
  - Water Town is far from everything else on foot: 26–33 minutes to Ladi Lane, the Interchange and the station. Bola rides.
  - Some walks to a place right behind a house are long, because back houses sit in deep compounds. Mama Ronke's clinic is 72 m away in a straight line but a 438 m walk.
  - Okadas still go the long way round where walkers use skywalks and footbridges.

## The days (shortened)
- **Tunde (okada):**
  - Room to the stall: 1.9 minutes on foot. Stall to the boss's park: 5.1 minutes.
  - Interchange to station: ×3.47 by bike against ×1.04 on foot over the skywalk. That's by design: bikes don't use the skywalk.
- **Mama Ronke (on foot, the Hub):**
  - Home (a back house, 1945,4625) to Under the Bridge: 5.6 minutes.
  - School 5.6, church 6.4, the bank 7.9–9.2, the station 3.0 minutes.
  - Mile Market: 25.6 minutes on foot, or 5.9 by okada.
- **Kemi (Jungle City):**
  - From the north: school 6.1, chemist 6.8, Boundary Plank Market 8.8 minutes.
  - From the south: chapel 1.6, mosque 7.9, secondary school 8.6 minutes.
  - The Maze: 12–16 minutes on foot, or 2.5–3.5 by okada.
- **Sule (porter, Food Gate):**
  - Home to Mile Market: 7.2 minutes. Market to the bus park over the footbridge: 6 minutes.
  - Water Town: the Stilt Bar is 13.9 minutes on foot, and the checkpoint to the Stilt Bar is 4.4.
  - Schools are 2.9–9.1 minutes from six homes he tried.
- **Bola (paddler, Water Town):**
  - Stilt house (4005,3585) to the Stilt Bar: 34 m. Canoe Jetty: 11.6 minutes. Sawmill: 14.3 minutes, or 3.7 by okada.
  - School on Stilts: 5.4 minutes. Chemist: 8.3 minutes.
  - The Maze and the Hub: 6–7 minutes by okada.
- **The chase:**
  - Stall to the market's west end: 2.4 minutes. Stall to the boss's park: 429 m, 5.1 minutes, ×1.29.
  - Every direction is reachable, through four distinct exits: east, north, south (Ring Road) and west along the aisle.

## Standard trips
| Trip | Mode | Before: m / min / detour | After: m / min / detour |
|---|---|---|---|
| Tunde's room → The steal | walk | 161 / 1.9 / ×1.50 | 161 / 1.9 / ×1.50 |
| The steal → boss's motor park, through the market | walk | 429 / 5.1 / ×1.29 | 429 / 5.1 / ×1.29 |
| The steal → Gang Canal | walk | 496 / 6.0 / ×1.49 | 496 / 6.0 / ×1.49 |
| Maze house by the rail → Ladi Lane Parts Market | walk | 828 / 9.9 / ×1.37 | 828 / 9.9 / ×1.37 |
| Gidi Interchange → Hub Rail Station | walk | 220 / 2.6 / ×1.04 | 220 / 2.6 / ×1.04 |
| Boss's motor park → Ladi Lane Parts Market | ride | 477 / 1.1 / ×1.73 | 477 / 1.1 / ×1.73 |
| Under the Bridge → Daleko Grain Yard | walk | 1,222 / 14.7 / ×1.28 | 1,222 / 14.7 / ×1.28 |
| Jungle City centre → Gidi Interchange | ride | 2,201 / 5.3 / ×1.43 | 2,201 / 5.3 / ×1.43 |
| Food Gate house (3100,3884) → Mile Market | walk | 639 / 7.7 / ×1.18 | 639 / 7.7 / ×1.18 |
| Mile Market → Ladi Lane Parts Market | ride | 1,569 / 3.8 / ×1.33 | 1,569 / 3.8 / ×1.33 |
| **Jungle City 3017,5225 → 3029,5181** | walk | 480 / 5.8 / ×10.52 | **147 / 1.8 / ×3.23** |
| **Jungle City 2520,5280 → 2520,5400, across the expressway** | walk | 257 / 3.1 / ×2.14 (at grade) | **131 / 1.6 / ×1.09** (footbridge) |
| **Water Town centre (3650,4050) → Gidi Interchange (new)** | ride | no route (not built) | **2,083 / 5.0 / ×1.21** |
| Stilt Village → Canoe Jetty (new) | walk | — | 963 / 11.6 / ×1.11 |
| Stilt Village → Mile Market (new) | walk | — | 1,123 / 13.5 / ×1.21 |

**Notes:**
- **3017,5225 → 3029,5181:** both points are north of the expressway. The long walk came from the market's own road, which never joined the street grid. It now does (`clear_access` in Jungle City). What's left (×3.23) is a 46 m gap across a block.
- **Across the expressway:** before, the tool let walkers cross the expressway at grade. They now use the new footbridge.

## City measures
| | Before | After | Target |
|---|---|---|---|
| School within 10 min: Maze / Hub / Jungle City / Food Gate / Water Town | 100 / 100 / 100 / 90 / — | 100 / 100 / 100 / 100 / 100% | 100%; up to 15 min accepted |
| Worship within 10 min | 100 / 100 / 98 / 99 / — | 100 / 100 / 100 / 100 / 100% | 100% |
| Chemist or clinic within 10 min | 100 / 100 / 100 / 98 / — | 100 / 100 / 100 / 100 / 100% | 100% |
| Worst walk to an everyday place (any district) | 12.4 min (Food Gate school) | 9.7 min (Food Gate school) | ≤ 10 min |
| Coverage after regenerating the Maze (seed 3) or the Hub (seed 42) | could drop (Hub 99 → 89%) | **100%** | 100% |
| Opening moved by a regeneration | not checked | **check 12 fails** | never |
| Longest walk between pedestrian rail crossings: Maze / Hub / Water Town | 200 / 254 m / — | 200 / 254 / 118 m | 150–250 m |
| Walking islands inside the built districts | 0 | 0 (one in Water Town was found and fixed, below) | 0 |
| Walking islands at the study border | 9 | 6 | tiny pieces only |
| Houses > 45 m from a way (tool, by house centre) | 34 of 7,917 | 51 of 10,777 | 0 by wall (`check_district.py` passes) |
| `check_district.py`, all five districts | pass (four built) | **pass** | all pass |

## Verified problems (real), with coordinates
1. **Fixed: a street lying on top of another in Water Town** (3819,4500 to 3875,4474, by the sawmill). Two clean-up steps had each cut the same line, so a 62 m copy sat 0.3 m from the real street without joining it. Bola's `walk 3875,4474 4047,4455` gave NO ROUTE. The generator now drops a street that lies on top of a longer one (short ties stay). This also removed three doubled streets in Food Gate (99, 164 and 54 m). The Maze, the Hub and Jungle City regenerate byte-identical.
2. **Fixed (tool): the stilt village showed as "outside the built districts"** (`look 4005 3585`). It stands on the lagoon, outside Water Town's land outline. The tool now counts a district's stilt huts, stilt bar and rafts as that district.
3. **Open: the boss's motor park is about 200 m from the market's west edge, across Ring Road.** Its note in `web/districts_info.json` says "just across Idowu Street from the far end", and the persona says the same. The walk from the market's west edge (2520,4407) to the park is 301 m, 3.6 minutes. Both are locked, so I did not move them. **For the owner:** is 200 m close enough for the boss to see the chase? If yes, I'll correct the note to "across Ring Road". If no, a later session moves the park and re-locks it.
4. **Open: Water Town is far from the city on foot.** From the stilt village, walks to Ladi Lane (26 min), the Interchange (32) and the Hub station (33) all pass 20 minutes. By okada they are 6–7 minutes. That fits a waterfront village at the city's edge, and in the game canoes will carry much of it.
5. **Open: long walks to a place behind a back house.**
   - Mama Ronke: 1945,4625 → Divine Health Hospital (1891,4673) is 438 m for 72 m, ×6.06. Her house is the back of a deep compound with one lane out, and the hospital faces Ayinde Avenue.
   - Kemi: 2657,5439 → Cure Pharmacy (2738,5540) is 420 m for 129 m, ×3.25.
   - Real compounds are like this, but a few more rear footpaths through deep blocks would help. **Next session:** a footpath through blocks deeper than 90 m.
6. **Still open from the last test:**
   - **Okada rides between neighbouring landmarks:** the Interchange to the station is ×3.47. Walkers use skywalks and footbridges, which bikes can't.
   - **The Hub's rail gap along the industrial yard:** 254 m (target 250).
   - **The tool lets pedestrians walk along arterials** (for example 119 m along the Coastal Expressway on `walk 2900,5200 2900,5450`). In the game this would be the verge.

## Tool artefacts (not city problems)
- **Islands at 2289,5243, 1737,4959, 3304,5540, 1375,3602, 2413,3300 and 1980,3747:** all outside the built districts. They are the unbuilt neighbours' sketch roads, cut at the study border.
- **"Footbridge 0.0 km"** in `overview`: road footbridges are counted as skywalks, and the canal footbridges are 6–7 m long.
- **`home N` is not house number N:** it picks a house from a shuffled list.
- **Name lookup picks the first match:** "Fresh Life Pharmacy" exists in the Maze and the Hub. Use X,Y.
- **Pins off the network:** Mile Market (102 m by okada; bikes don't use the aisles), Okobaba Sawmill (61 m, the middle of a 1.4 ha yard), Little Angels School (43 m, inside the compound).
- **Long walks to one chosen place are not coverage gaps:**
  - Sule: 15 minutes to Oko Medicine Store from 3799,3040.
  - Bola: 17.5 minutes to Al-Ikhlas Mosque.
  - Each house has a closer chemist or place of worship, and `check_district.py` check 13 measures every house to its nearest one.
- **Houses "45–46 m from a way" (51 houses):** the tool measures to the house's centre. `check_district.py` measures to the nearest wall, and every district passes.
- **No bus or train command:** the tool can't time a bus or train leg.

## What was fixed in this session
- **The opening is locked** (`web/locked.json`, check 12).
- **Everyday places are placed by coverage** (`scripts/walknet.py`, check 13).
- **Jungle City:** a second expressway footbridge, and the market's road joins the grid.
- **Water Town built,** with Okafor Road's rail crossing decided from data: it's a bridge.
- **From this test:**
  - the doubled streets (generator)
  - the stilt village counts as Water Town (tool)
