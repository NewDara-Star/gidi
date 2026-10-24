# City living test, 14 Oct 2026 (third run): eight districts, with the new Port

There are two states:
- **Before:** `main` at the start of this work (commit `1925734`, seven districts).
- **After:** this branch, with the Port.

Nine Haiku agents ran:
- **New: Chidi,** a clearing agent in the Port
- Ngozi (the Capital)
- Emeka (the Bazaar)
- Tunde (okada)
- Mama Ronke (the Hub)
- Kemi (Jungle City)
- Sule (Food Gate)
- Bola (Water Town)
- the chase

I re-ran every problem they reported and checked it by hand.

## How life feels (short version)
- **The Port is where the oja comes in, and getting it out is work.**
  - Okadas are banned there, so from the Container Yard you walk about 650 m out of the zone first.
  - The run to the boss's motor park is then 14.6 minutes door to door. Riding through the ban (`--through`) would be 9.3 minutes, with 1.5 km inside it.
  - For a game that's a good tension: the legal way is slow and the fast way is seen.
- **On foot, the Port joins its neighbours.**
  - The reserve to the yard is 17 minutes.
  - The reserve to the under-bridge market is 6 minutes.
  - Expressway footbridges link the two halves.
- **Nothing else moved.** Every standard trip from before is unchanged.
- **Everyday places:** every home in all eight districts has a school, a place of worship and a chemist within 10 minutes. The worst is 10.0 minutes, a chemist in Food Gate.

## Verified problems, and what was fixed
1. **Fixed: the Container Yard had no roads inside.** Its pin was 157 m from any way, and Bola's okada couldn't get near the tank farm. Yard lanes now run along and across it, out to the yard's access road. The yard pin is now on a lane.
2. **Fixed: the colonial reserve had no way in.** Its pin was 112 m from a road. It now has its avenue, a lane down its length joining the streets at both ends, with the bungalows either side.
3. **Fixed earlier in this run:** the reserve first landed on a sliver of a block (minimum width added). Container stacks, trailers and cranes are no longer counted as buildings.
4. **Open, by design: the okada ban makes some rides slower than walking.**
   - Ngozi: home → Capital Junior High is 12.3 minutes by okada against 10.3 on foot.
   - Tunde: the Cantonment → the motor park is 6.0 minutes against 4.2 minutes riding through.
   - The tool shows both. That's the ban working.
5. **Open: pins in the middle of big walled plots** (the barracks, the prison, the plazas, the Cantonment), 65–78 m from a way. The places have gates; the pins just sit in their middle.
6. **Open, carried over:**
   - pedestrians are routed along the expressway (Chidi: 181 m on it on one walk)
   - okada detours round skywalks
   - a few deep-compound walks of ×6–9 between neighbours (for example, Emeka's house to the school 22 m away is 207 m)

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| All 22 earlier standard trips | | | unchanged (Stilt Village → Mile Market 1,139 → 1,141 m) |
| **Old Reserve Avenue → Container Yard (new)** | walk | — | **1,443 m / 17.3 min / ×1.30** |
| **Container Yard → Gidi Interchange (new)** | ride | — | **4,084 m / 16.1 min (657 m on foot, round the ban)** |
| **Container Yard → boss's motor park (new)** | ride | — | **3,524 m / 14.6 min (642 m on foot)**; `--through` 9.3 min, 1,571 m inside the ban |

## City measures
| | Before | After |
|---|---|---|
| Districts built | 7 | 8 |
| Okada ban zones in the data (built) | 1 (Capital, 35 checkpoint sites) | 2 (+ the Port, 28) |
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| Walking pieces at the border | 4 | 3 |
| `check_district.py` | pass (7) | pass (8) |
| Every district regenerates byte-identical | yes | yes |

## Tool artefacts (not city problems)
- **District names aren't places** ("The Maze", "The Hub"): use a landmark or X,Y.
- **Edge roads count as the first district:** Alaba Road is shared by Jungle City and the Port, so a walk between two Port places along it reads "Jungle City".
- **"You pass" lists the start and end places too,** and repeats a few names.
- **`look` takes X Y only,** not a place name.
- **Islands at 1404,3596 and 2020,2619:** sketch roads of the unbuilt Railside and Estate at the Capital's edge.
