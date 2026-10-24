# City living test, 14 Oct 2026 (second run): seven districts, with the new Bazaar

This run tests four changes on this branch:
- **The fair block count:** the generator fix that came with it gives Jungle City and the Capital fewer collector streets.
- **The okada ban zone** in the Capital.
- **The new district:** the Bazaar.
- **Lane passages:** short footpaths from dead-end lanes, added after the test showed a regression (see below).

There are two states:
- **Before:** `main` at the start of this work (commit `1c7a49d`).
- **After:** this branch.

Eight Haiku agents ran on the branch:
- **New: Emeka,** an electronics trader in the Bazaar
- Ngozi (the Capital)
- Tunde (okada)
- Mama Ronke (the Hub)
- Kemi (Jungle City)
- Sule (Food Gate)
- Bola (Water Town)
- the chase

I re-ran every problem they reported and checked it by hand before it went into this file.

## How life feels (short version)
- **The Bazaar works as a market town on the expressway.**
  - A trader's home to the electronics market is 6.4 minutes, over a footbridge.
  - The Container Court is 9.5 minutes and Rago Yard 10.6.
  - An okada reaches the Hub's interchange in 5 minutes and Jungle City's market in 4.8.
  - It's low and sandy-feeling: half the buildings are one storey, a quarter of the plots stand empty, and short dead-end streets run off the long ones.
- **The okada ban makes the Capital feel different.**
  - Rides now go round it, and the trip says how far you walk to the nearest road a bike may use: 394 m out of Gadget Village, 549 m from the strip.
  - Ride times now include those walks. The Capital's centre to the Interchange is 9.3 minutes door to door (1.8 km); it was 3.3 minutes before the ban was enforced.
  - `--through` shows what breaking the ban costs: 559 m inside the zone on Ladi Lane → Gadget Village.
- **The opening is intact:** stall → boss's post 1.6 minutes; four ways out of the market.
- **Everyday life:** every home in all seven districts has a school, a place of worship and a chemist within 10 minutes. The worst is exactly 10.0 minutes, a chemist in Food Gate.

## Verified problems, and what was fixed
1. **Fixed: a regression from the block fix.**
   - With fewer collector streets, a deep block in Jungle City cut the walk 3017,5225 → 3029,5181 (the one you asked to fix before) from 147 m back to 543 m. A dead-end service lane stopped 25 m short of the market's road.
   - **Fix, for all districts:** a dead-end lane that stops within 40 m of another way now carries on to it as a footpath, if no house is in the way. At most one shed or kiosk per district was cleared for one; no house moves.
   - The walk is now 97 m (×2.13), better than before.
   - Across the city, 114 passages were added, and dead ends inside the network fell from 364 to 276.
2. **Fixed (tool): rides to a place deep in the Capital gave "no route"** (`ride "Boss's motor park" "Allen Roundabout Strip"`). The trip snapped onto a sketch-road scrap at the border. It now joins the main network: 2,133 m, plus 549 m on foot.
3. **Fixed (tool): ride times ignored the walk to and from the bike.** They now include it, at walking speed.
4. **Fixed (tool): repeated names picked the first match,** often in another district (the agents' biggest complaint). A named place now resolves to the nearest one of that name, and the output shows its X,Y when the name repeats.
5. **Fixed: the wholesale plazas had no gate.** Their pin is 73 m inside a 2.5 ha plot; they now have a gate.
6. **Open: two walks are longer after the block fix:**
   - Jungle City's crossing at 2520,5280 → 2520,5400: 131 → 180 m (×1.50)
   - the Capital's Gadget Village → Allen strip: 295 → 373 m (×1.85)

   Fewer collector streets means fewer short cuts. Both are inside what the other districts have.
7. **Still open:**
   - okada detours round skywalks (Interchange → station, ×3.47)
   - pedestrians walk along the expressway (`walk 1810,5285 "Barracks"`: 269 m on it)
   - short walks round walled plots

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| Tunde's room → The steal | walk | 161 m / 1.9 min / ×1.50 | 161 / 1.9 / ×1.50 |
| The steal → boss's post | walk | 137 / 1.6 / ×1.07 | 137 / 1.6 / ×1.07 |
| The steal → boss's motor park | walk | 429 / 5.1 / ×1.29 | 429 / 5.1 / ×1.29 |
| Gidi Interchange → Hub Rail Station | walk | 220 / 2.6 / ×1.04 | 220 / 2.6 / ×1.04 |
| Boss's motor park → Ladi Lane | ride | 477 / 1.1 | 477 / 1.9 (incl. 78 m on foot) |
| Mile Market → Ladi Lane | ride | 1,569 / 3.8 | 1,569 / 5.3 (incl. 157 m on foot) |
| Jungle City 3017,5225 → 3029,5181 | walk | 147 / 1.8 / ×3.23 | **97 / 1.2 / ×2.13** |
| Jungle City 2520,5280 → 2520,5400 | walk | 131 / 1.6 / ×1.09 | 180 / 2.2 / ×1.50 |
| Jungle City 2400,5200 → 2400,5450 | walk | 446 / 5.3 / ×1.78 | **287 / 3.4 / ×1.15** |
| Stilt Village → Mile Market | walk | 1,196 / 14.4 / ×1.29 | 1,139 / 13.7 / ×1.23 |
| Gadget Village → Allen Roundabout Strip | walk | 295 / 3.5 / ×1.47 | 373 / 4.5 / ×1.85 |
| Gadget Village → Interchange | walk | 1,167 / 14.0 / ×1.33 | 1,142 / 13.7 / ×1.30 |
| Capital centre (1980,3300) → Interchange | ride | 1,358 / 3.3 (through the ban) | 1,763 / 9.3 (528 m on foot, round the ban) |
| Ladi Lane → Gadget Village | ride | 1,625 / 3.9 (through the ban) | 1,573 / 8.1 (449 m on foot); `--through` 1,615 m, 559 m inside |
| **Alade Electronics Market → Interchange (new)** | ride | no route (not built) | **1,465 / 5.0 / ×1.46** |
| **Bazaar house (1700,5600) → Alade Electronics Market (new)** | walk | — | **535 / 6.4 / ×1.29** |

All other standard trips are unchanged; ride times now include their short walks.

## City measures
| | Before | After |
|---|---|---|
| Districts built | 6 | 7 |
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| Dead ends inside the network | 299 (6 districts) | 276 (7 districts) |
| Houses > 45 m from a way (tool, by house centre) | 72 of 11,955 | 78 of 13,251 (0 by wall: `check_district.py` passes) |
| `check_district.py` | pass (6) | pass (7) |
| Every district regenerates byte-identical | yes | yes |

## Tool artefacts (not city problems)
- **Islands at 3304,5540, 1404,3596 and 2020,2619:** the unbuilt neighbours' sketch roads at the border.
- **Pins in the middle of big plots:** the plazas, the barracks, the Secretariat.
- **"Inside the bust":** standing on the Allen roundabout pin.
- **`home N water` rarely lands on a stilt house:** most of Water Town's homes are on land.
- **No time of day, bus, train or canoe** in the tool.
