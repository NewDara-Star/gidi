# City living test, 14 Oct 2026 (fifth run): ten districts, with the new Estate

There are two states:
- **Before:** `main` at the start of this work (commit `22daecd`, nine districts).
- **After:** this branch.

Eleven Haiku agents ran:
- **New: Musa,** gateman and night-delivery rider in the Estate
- Ngozi (the Capital)
- Tunde (okada)
- Mama Ronke (the Hub)
- Kemi (Jungle City)
- Sule (Food Gate)
- Bola (Water Town)
- Emeka (the Bazaar)
- Chidi (the Port)
- Funmi (Railside)
- the chase

I re-ran every problem they reported that touched the Estate, and checked it by hand.

## How life feels (short version)
- **The Estate is quiet and close to the Capital on foot, far from it by okada.**
  - Musa's boys' quarters to the Estate Gate is a 2.7-minute walk. The gate to the Senator's House is 750 m (9 minutes); the Club is 4 minutes from his bed.
  - On his round he passes 3 gatehouses within 120 m of the main gate; the district has 21.
  - The Estate Gate to Gadget Village is a 10-minute walk (845 m, ×1.24).
  - **By okada, the Capital is in the way:** okadas are banned there, so a legal ride to the Hub's interchange goes round on the edge roads (Salami Road, then Eze Street): 3.3 km for 1.6 km (×2.12). Gadget Village to the Estate Gate by okada is 3.3 km against an 845 m walk. That is the ban doing its job.
- **The opening is intact:** stall → boss's post 1.6 minutes, stall → motor park 5.1. The chase still has 4 ways out of the market; the boss's end is not the only one.
- **Everyday places:** every home in all ten districts has a school, a place of worship and a chemist within 10 minutes.

## Verified problems
1. **Open (design): the Estate is cut off by okada.** Every okada trip from the Estate to the Hub or Food Gate goes round the Capital's ban. If the owner wants the Estate's big men easy to reach by bike, the Capital's ban zone could leave its north edge rideable, or the Estate could get a road of its own to Railside's north.
2. **Open: pins in the middle of walled plots**, now including the Estate Club (35 m from its street) and the Senator's House (28 m).
3. **Open, carried over:**
   - okada rides longer than walks wherever walkers use paths, skywalks or footbridges
   - pedestrians routed along the Coastal Expressway (Emeka: 1,184 m of it)
   - Bakery Row → the cattle market (×2.5)
   - Food Gate and the Estate meet only at a corner; a 212 m hop between them is ×2.08 through the Capital's edge.

Nothing new needed fixing in the city this run.

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| The 29 earlier trips | | | unchanged |
| **Estate Gate → The Senator's House (new)** | walk | — | **750 m / 9.0 min / ×1.24** |
| **Estate Club → Gidi Interchange (new)** | ride | — | **2,967 m / 7.8 min / ×1.59** (round the Capital's ban) |
| **Estate Gate → Gadget Village (new)** | walk | — | **845 m / 10.1 min / ×1.24** |

## City measures
| | Before | After |
|---|---|---|
| Districts built | 9 | 10 |
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| `check_district.py` | pass (9) | pass (10) |
| Every district regenerates byte-identical | yes | yes |
| The Capital's okada checkpoint sites | 40 | 45 (the Estate's streets meet its edge) |
| Lagos-isms logged | 11 isms × 11 areas | 12 isms × 12 areas (`docs/LAGOS-ISMS.md`) |

## Tool artefacts (not city problems)
- **The island at 673,4721:** sketch roads of the unbuilt Border.
- **`look` and `home` take numbers only;** district names aren't places, and a bare number in `walk` is read as part of a place name (Musa's `walk 1 estate` went from "Iju Waterworks").
- **`home 1 estate`** gives the main house; the boys' quarters is the next one.
- **`look 1500 2300`** says "outside the built districts" just past the Estate's west edge, where its edge road bends outward.
- **Civic names repeat** across districts (Daily Care Chemist, Good Health Chemist), so a name can match the wrong one.
- **The Food Gate and Water Town civic places were renamed** and 6 of Food Gate's moved to new plots: names are dealt in bake order, and the Estate comes before them. Coverage is still 100%.
