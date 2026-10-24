# City living test, 13 Oct 2026: the Maze, the Hub, Jungle City

This is the first run of `docs/CITY-LIVING-TEST.md`, done on the whole built city.

There are two states:
- **Before:** commit `963a578`. The Maze fixes and Jungle City are in; the Hub fixes are not.
- **After:** `main` after PR #6. The Hub has rail paths, worn crossings and the station skywalk.

Six Haiku agents ran: three personas on each state.
- Tunde, okada rider
- Mama Ronke, food seller on foot
- **New:** Kemi, a student in Jungle City

Every problem they reported was re-run and checked by hand before it went into this file.

## How life feels (short version)
- **On a bike the city works.** Most cross-district rides take 1–4 minutes, and the longest standard ride is 5.1 minutes (Jungle City to the interchange).
- **On foot most trips are fine:** detours of ×1.1–1.6. The rail is still the thing you feel.
- **Hub fixes:**
  - Interchange to station: before, a ×3.35 detour (8.5 minutes); now a 2.5-minute walk over the skywalk.
  - Mama Ronke's supply run is shorter.
  - Far more Hub houses have a school within 10 minutes.
- **What still grates:**
  - Short trips near the Hub knot, where the rail, Ayinde Avenue and deep rail-side blocks force ×2.6–3.5 detours over 130–160 m.
  - The grain yard only opens to the south.
  - The stadium has one access road.

## The three days (shortened, from the after run)
- **Tunde (okada):**
  - Motor park to interchange: 552 m, 1.3 minutes.
  - Interchange to Ladi Lane Parts Market: 808 m, 1.9 minutes. To the Highlife Hotel: 767 m, 1.8 minutes.
  - Boundary Plank Market to Ireti Hotel: 1,067 m, ×2.02. The okada can't use the expressway footbridge, so it rides 249 m further than a walker.
  - The station run is 657 m (×3.11) because bikes can't use the skywalk.
- **Mama Ronke (on foot):**
  - 246 m to her stall Under the Bridge, 3 minutes. Interchange to station over the skywalk: 211 m.
  - Supplies: Ladi Lane 960 m (×1.24), Daleko Grain Yard 1,215 m (×1.27), Boundary Plank Market 1,868 m (×1.38).
  - Her local errands are the worst part: the mosque, the church and the chemist are 130–160 m away in a straight line but 410–520 m to walk (×2.6–3.5).
- **Kemi (Jungle City, the new district):**
  - School: 820–1,036 m, 9.8–12.4 minutes, depending on the house.
  - Mosque and chemist: 3–5 minutes.
  - Boundary Plank Market: 6–7 minutes.
  - Across the rail via Adeleke Road's bridge into the Maze: easy.
  - The interchange and station are 15–20 minutes on foot and 3–4 minutes by okada.

## Standard trips
| Trip | Mode | Before: m / min / detour | After: m / min / detour |
|---|---|---|---|
| Tunde's room → The steal (added after this run) | walk | 1,740 / 20.9 / ×1.14 | 1,740 / 20.9 / ×1.14 |
| The steal → Gang Canal | walk | 353 / 4.2 / ×1.56 | 353 / 4.2 / ×1.56 |
| Maze house by the rail (3040,4815) → Ladi Lane Parts Market | walk | 931 / 11.2 / ×1.54 | 931 / 11.2 / ×1.54 |
| **Gidi Interchange → Hub Rail Station** | walk | **708 / 8.5 / ×3.35** | **211 / 2.5 / ×1.00** |
| Boss's motor park → Ladi Lane Parts Market | ride | 1,155 / 2.8 / ×1.11 | 1,155 / 2.8 / ×1.11 |
| **Under the Bridge → Daleko Grain Yard** | walk | **1,325 / 15.9 / ×1.38** | **1,215 / 14.6 / ×1.27** |
| Jungle City centre (2740,5620) → Gidi Interchange | ride | 2,142 / 5.1 / ×1.39 | 2,142 / 5.1 / ×1.39 |
| Tunde's room → Boundary Plank Market (new, Jungle City) | walk | 1,136 / 13.6 / ×1.21 | 1,136 / 13.6 / ×1.21 |
| Hub Rail Station → Under the Bridge (from the agents) | walk | 489 / 5.9 / ×2.40 | 250 / 3.0 / ×1.23 |

There is no earlier test to compare with, so the baseline is the Before column.

## City measures
| | Before | After | Target |
|---|---|---|---|
| Longest walk between pedestrian rail crossings, Hub | 311 m | 247 m | 150–250 m |
| Longest walk between pedestrian rail crossings, Maze | 200 m | 200 m | 150–250 m |
| Walking islands inside the built districts | 3 (Hub lanes) | 0 | 0 |
| Houses with a school within 10 minutes: Hub / Maze / Jungle City | 81% / 100% / 96% | 99% / 100% / 96% | 100% |
| Houses with a place of worship within 10 minutes | 98–100% | 99–100% | 100% |
| Houses with a chemist or clinic within 10 minutes | 98–100% | 99–100% | 100% |
| Houses over 45 m from a way, measured to the house centre (tool) | 37 (worst 50 m) | 30 (all 45–46 m) | 0 |
| Dead ends inside | 121 | 111 | — |

- `check_district.py` measures to the nearest wall, and every district passes. The 30 "after" houses are back houses whose centre is 45–46 m away while the wall facing the lane is within 45 m.
- The remaining walking islands are all outside the built districts (see the artefacts below).

## Verified problems (real), with coordinates
1. **Short walks near the Hub knot.** The rail-side blocks west of Ayinde Avenue (about 1600–1780 E, 4200–4330 S) are deep, with few streets. Houses reach the network through the rail path.
   - `walk 1697,4272 1578,4229` (Taqwa Mosque): 446 m for 127 m, ×3.53.
   - `walk 1697,4272 "Latter Rain Assembly"`: ×3.26.
   - `walk 1697,4272 1825,4180` (chemist): ×2.61.
   - **Next session:** worn shortcuts or lanes through these blocks.
2. **Daleko Grain Yard opens only to the south.** `walk "Ladi Lane" "Daleko"` is 1,047 m for 436 m, ×2.40. The route goes over the Adeleke Road bridge and round the yard, which sits one block back from the rail. **Next session:** a gate on the rail side, or a path to the nearest worn crossing.
3. **The National Bowl has a single access road.** `ride 1556,4411 1618,3980` (motor park to stadium) is 1,043 m for 435 m, ×2.40. **Next session:** a second access road from the south.
4. **School reach in north Jungle City.** 4% of Jungle City houses have no school within 10 minutes; the worst seen is 12.4 minutes, from 3028,4995. The school compound is in the south. **Next session:** a second school site north of the expressway, or move the compound.
5. **The okada can't follow walkers over footbridges and skywalks** (×3.11 interchange to station, ×2.02 market to hotel). This is by design: the station's vehicle access is its back road. Accepted.

## Tool artefacts (not city problems)
- **Islands at the study border:** main roads of the unbuilt neighbours (Idowu Way, Balogun Street, Alaba Street and others), cut off at the border of the area the tool covers.
- **Walking "islands" at 2234,4162, 2571,3926 and 2893,4204** in the agents' early runs. The tool's road-joining step dropped sub-metre slivers between streets running end to end. Fixed in the tool; there are none now.
- **"Off-network" metres** (for example 57 m at Tunde's room). The tool counts from the nearest junction, not the nearest road; `look` shows the room is 23 m from a street. The route totals are slightly high because of this.
- **Name lookup picks the first match.** Civic names repeat across districts (two Harbour Banks, two Viewing Centres, four Iya Bisi chemists), so the agents sometimes got a far one.
- **Footbridges and roads aren't places,** and the overview shows the 7 m canal footbridges as "0.0 km".
- **"Outside the built districts" on routes.** These run along an edge road shared with an unbuilt neighbour (Alaba Road with the Port), or through the unbuilt Bazaar.
- **"The coast at 2000,5400" and "the west point 2100,5300"** are in the unbuilt Bazaar, not Jungle City.
- **Tunde's room is in Jungle City,** while the test doc's persona said Tunde lives in the Maze. The owner confirmed the pin is right, so the persona in `CITY-LIVING-TEST.md` is fixed. His walk from his room to The steal is now a standard trip: 1,740 m, 20.9 minutes, ×1.14, up Adeleke Road and over its rail bridge.

## What was fixed in this session
- **Hub (PR #6):**
  - footpaths on both sides of the rail, with links from street ends
  - 3 worn crossings
  - the Station skywalk from Gidi Interchange over Northern Road, Ring Road and the rail
  - lanes start on streets (the Hub's 3 floating lanes are gone)
  - nothing built more than 44 m from a way
- **Tool (`scripts/explore_city.py`):**
  - reads footpaths (`paths`); okadas don't use them
  - joins junctions within 25 cm and loose ends within 1 m, the same tolerance as `check_district.py`
  - labels rail crossings on a deck or a worn path correctly
  - points at `web/gidi-data.js` instead of a temp folder
