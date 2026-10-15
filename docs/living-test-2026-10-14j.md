# City living test, 14 Oct 2026 (tenth run): thirteen districts, with the new Frontier

There are two states:
- **Before:** `main` at commit `10b9708` (twelve districts).
- **After:** this branch: the Frontier, and the Heights rebuilt once with `keep_gateways`.

The other eleven districts regenerate byte-identical, so three agents ran:
- **New: Femi,** site security on the Frontier
- **Kunle** (the Heights, rebuilt)
- **Tunde** (okada)

## How life feels (short version)
- **Inside the Frontier, life works by okada:**
  - Femi rides to the Toll Plaza in 4.2 minutes, the Refinery in 4.3, the Eroding Beach in 3.2.
  - Toll Plaza → Refinery is 2.1 km in 5.1 minutes.
- **On foot, everyday places are close:** from Femi's house a mosque is 5.1 minutes away, a secondary school 5.7 and a chemist 5.9. Every Frontier home has its everyday places within 10 minutes.
- **The Heights and the Frontier join on foot:**
  - the Toll Plaza is a 4.2-minute walk from a house at the Heights' east edge
  - New Estates is 10 minutes, and the streets carry straight on across the border
- **No okada can legally reach the Frontier.**
  - Its only roads in run through the Heights, and okadas are banned there.
  - From the boss's motor park, the legal ride ends 975 m short of the Toll Plaza.
  - Through the ban it is 12 minutes, 2.8 km of it inside the ban.
  - It is a design question for the story map (the study, section 6).
- **The opening is intact:** Tunde's room → The steal is 1.9 minutes.

## Verified problems, and what was fixed
1. **Fixed (tool): rides inside the Frontier were all on foot.**
   - **Why:** the bans cut the Frontier's road network off from the rest of the city's. The tool joined every ride to the biggest piece of network, so a 2 km ride inside the Frontier became a 3.2 km walk.
   - **The fix:** a ride whose two ends both lie on a cut-off piece now rides inside it. Every earlier standard trip is unchanged.
2. **Fixed (tool): a ride into the Frontier walked its last kilometre without saying why** (Tunde). It now says so: "no legal road reaches where the trip ends (the ban zones cut it off)".
3. **Open, design:** the Frontier is cut off for okadas (above).
4. **Open, small:** in the rebuilt Heights, the Gold Island's gate opens onto the border road it shares with the Frontier, so walks out of the enclave start on the Frontier side (Kunle).

## Not problems (checked)
- **"The Disputed Plots are full of houses"** (Femi): within 180 m of the pin there are 118 homes per km², against the district's 381, a third. Femi's count included generator houses and sheds, and `look` doesn't list walls or empty plots.
- **Walks ending hundreds of metres off the network** (Femi: 6900,6150; 8200,6200; 7600,4000): those points are in the sea or the lagoon.
- **Short walks with big detours** (Kunle, Femi): they go round walled plots and long blocks.
- **The island near 673,4721:** a sketch street of the unbuilt Border.

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| The 37 trips outside the Heights | | | unchanged |
| Pearl Towers → Club Strip | walk | 626 m / 7.5 min / ×1.33 | 648 m / 7.8 min / ×1.30 (the Heights rebuilt) |
| The Gold Island → Pearl Towers | walk | 1,060 m / 12.7 min / ×1.45 | 1,339 m / 16.1 min / ×1.37 (the enclave moved to the east edge) |
| Cable Bridge → Sunday Beach | walk | 1,605 m / 19.3 min / ×1.24 | 1,593 m / 19.1 min / ×1.23 |
| Pearl Towers → Cloth Market | walk | 937 m / 11.2 min / ×1.13 | 921 m / 11.1 min / ×1.15 |
| Club Strip → Gidi Interchange | ride | 5,826 m / 20.7 min / ×1.39 | unchanged |
| **New Estates → Disputed Plots (new)** | walk | — | **838 m / 10.1 min / ×1.42** |
| **Toll Plaza → Refinery (new)** | ride | — | **2,081 m / 5.1 min / ×1.26** |
| **Eroding Beach → Toll Plaza (new)** | walk | — | **1,189 m / 14.3 min / ×1.34** |
| **Toll Plaza → Pearl Towers (new)** | walk | — | **1,119 m / 13.4 min / ×1.04** |
| **Refinery → Gidi Interchange (new)** | ride | — | **7,385 m / 39.4 min / ×1.22** (2,258 m on foot: no legal okada road out of the Frontier) |

## City measures
| | Before | After |
|---|---|---|
| Districts built | 12 | 13 |
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| Houses over 45 m from a way (the tool's count) | 113 | 116 |
| `check_district.py` | pass (12) | pass (13) |
| Every district regenerates byte-identical | yes | yes (the Heights rebuilt once with `keep_gateways`) |
| Lagos-isms logged | 13 isms × 14 areas | 14 isms × 15 areas |
