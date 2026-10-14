# Heights pattern study: Ikoyi, Victoria Island and Banana Island → the Heights (v1)

Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**

Data:
- OpenStreetMap (ODbL), Lagos extract
- heights from Google Open Buildings 2.5D, measured on the study boxes themselves (`scripts/study_boxheights.py`, new)
- people, tree cover and terrain from `data/results/lga_table.json` (Eti Osa)
- the Lagos-isms of these neighbourhoods are in `docs/LAGOS-ISMS.md`

![The Heights (left) beside a dense real square of Ikoyi (right)](img/heights-vs-real.png)

## Areas studied
- **Neighbourhood level only, as the brief says:** three boxes inside Eti Osa (19.1 km² of land in all).
  - **Ikoyi:** 3.418–3.450 E, 6.440–6.462 N
  - **Victoria Island:** 3.405–3.440 E, 6.420–6.438 N (stops short of the reclaimed city to the south)
  - **Banana Island:** 3.444–3.462 E, 6.455–6.470 N
- The boxes were found from OSM's own place points, then checked on a drawing of the streets.
- **Lekki is left out on purpose.** It is the Frontier's inspiration, and its low estates make up most of Eti Osa.

## 1. How it transfers to the scale of our world
- The Heights is 1.18 km², all land. The study area is 19.1 km² (1:16).
- **Fabric stays 1:1.**
- **Landmarks are chosen, not scaled.**
- **Its neighbours:**
  - the lagoon along the north
  - the ocean beach 80 m off the south edge
  - Old Island to the west
  - the unbuilt Frontier to the east
- **Waterfront Drive** (an arterial) crosses it west to east and becomes the Peninsula Expressway at the Frontier.

## 2. Road connections to other districts
- **Old Island:** its two crossings (Waterfront Drive and one street), recorded when Old Island was built, are reused exactly.
- **The Frontier, for when it's built:** three crossings are recorded in `web/network.json`: the arterial, a main road and a street.
- **New: the Cable Bridge.** A 1.1 km tolled bridge leaves the Heights' north shore, swings out over the lagoon and lands on the Frontier's north shore, like the real link bridge from Ikoyi to Lekki. It is a new bridge in the city's road list (`bake_web.py`). On the Heights side it lands on the edge road (`bridge_links`), with two toll booths on its deck 30 m out.
- **Old Island had to be rebuilt once.** The Heights now records its own crossings at Old Island's two crossing points. As the brief says, Old Island gets `keep_gateways` and is rebuilt:
  - 2,147 buildings instead of 2,187, and the same street figures
  - every measure still within the real range
  - it passes `check_district.py`, and regenerates byte-identical from now on
- **The other ten districts regenerate byte-identical.**
- **Okada ban:** the district model bans okadas, so the bake marks the Heights a ban zone with checkpoint sites, as it does for Old Island.

## 3. What the data says
### Mapping
OSM traces the buildings well in all three boxes: 121 of Ikoyi's 135 250 m cells, 96 of Victoria Island's 112 and 33 of Banana Island's 48 have buildings covering at least 3%. So every figure is measured on the study itself, with no well-mapped-cells step.

### Roads
- **Street density:** 11.0 km of drivable street per km² in the typical square, 12.0 in the dense one.
- **Private service roads:** 3.7 km per km² on top of that, the driveways and compound roads of big plots.
- **Junctions:** 46–51 per km², 91–92% of them T.
- **Dead ends:** 0.33–0.41 per junction, the closes.
- **Blocks:** 20–25 per km² counted closed. The median block is 3.3–5.9 ha, among the biggest of any district.
- **Parallel streets:** a median 109 m apart. Blocks are 2.7× longer than wide.
- **Main roads:** 4.3–5.3 km per km², among the most of any district.
- **One way:** 40% of the street length, the same as Lagos Island.
- **Surface:** paving stones (44 tagged) more often than asphalt (34). It's the only area studied where that's so.
- **Street names:** Street (146), Close (131), Road (115), then Avenue, Crescent, Drive.

### Buildings
- **Density:** 378 per km² in the typical square, 503 in the dense one, covering 12–15% of the ground. That's the emptiest of any district; the Estate has 528–800.
- **Size:** typical 218–238 m². 26–28% are over 400 m² (the most of any district), and 11–12% are under 60 m² (boys' quarters, gatehouses).
- **Set back:** the edge of a building is a median 22 m from the street's centreline, the deepest of any district.
- **Gaps:** 3.4–3.5 m.
- **Big buildings:** 99 over 1,500 m² (5.2 per km²), a median 27 m from a main road. The hotels run up to 88 m tall.
- **Heights:** measured on the boxes from Google Open Buildings 2.5D. Eti Osa as a whole is mostly Lekki's low estates (14+ storeys: 0%) and would hide the towers.

| Storeys | 1 | 2 | 3 | 4 | 5–6 | 7–13 | 14+ |
|---|---|---|---|---|---|---|---|
| Eti Osa (whole LGA) | 31% | 50% | 13% | 3% | 2% | 1% | 0% |
| Ikoyi, VI, Banana Island (the boxes) | 19% | 45% | 18% | 6% | 5% | 4% | 3% |
| The Heights (by area) | 18% | 45% | 19% | 6% | 5% | 5% | 3% |

- The method was checked on Old Island's box, which gives back Lagos Island's LGA bands (11/51/21/7/6/3/1 against 9/49/24/8/6/4/1).
- The study boxes average 9.0 m, the tallest of any area. Lagos Island averages 8.8 m.
- **People:** Eti Osa averages 2,338 per km² of land (WorldPop), but that's the whole LGA.
- **Land:** Eti Osa has 11% tree cover, and 54% of its land is below 3 m.

### Land use and landmarks (sizes only)
- Two golf courses (77 ha), 56 ha of military land, 18 ha of schools (median compound 0.7 ha), 39 building sites.
- **No market is mapped in the boxes.** There are 45 small shops and retail plots, a median 0.2 ha, all on a main road.
- **No bus station.** Four interchanges and 10 flyovers.

## 4. The generator: what is new for the Heights
`scripts/gen_fabric.py heights 9 2.5`, with its settings in `scripts/district_profiles.py` (`heights`). It starts from the Estate's rules: big walled plots, front yards, closes, generators and water tanks.

**Landmarks** (from the district model's pins):
1. **Pearl Towers:** three 20-storey glass apartment towers (1,100 m² each) on Waterfront Drive, set back on the line of the houses. They make up the boxes' 14+ storey band (3% of the built area).
2. **The Gold Island:** a 3.5 ha walled enclave with one gate, five mansions with pools, and a gatehouse, on sand-coloured ground (reclaimed sand).
3. **The Club Strip:** the five houses round the pin are clubs and lounges, one to three storeys.
4. **The Cable Bridge:** the tolled bridge to the Frontier, with its toll booths.
5. **Sunday Beach** is the 80 m of sand between the south edge road and the ocean. Its pin is on the edge road. There are no beach shacks or horses yet.
6. **A private school** and **a pitch.**
7. The everyday places (churches, mosques, the school, chemists, a clinic) are placed by the civic layer, as in every district.

**New in the generator** (all switched on per district, so the other eleven don't change):
- **`h_bands`:** a neighbourhood's own height bands in place of its LGA's.
- **Gated cul-de-sacs** (`estate_gates.closes_only`): every close gets a barrier and a gatehouse 13 m in from its mouth. The through streets and main roads stay open. 20 gates.
- **The `enclave` parcel,** with the compound code's buildings and grounds.
- **`toll`:** booths on a bridge near its landing, with the pin between them.
- **Towers set back with the houses** (`halls.front_m`, `within_m`): the towers stand behind a front yard, within 250 m of their pin.
- **The map:** apartment towers, clubs, toll booths and the enclave's sand have their own colours in 2D and 3D. `explore_city.py` names them.
- **`check_district.py`:**
  - toll booths may stand over the water, like stilt houses
  - the "building on land" check allows 0.05 m² (was 0.01), as the overlap check does. Coordinates are written to 0.1 m, and one of Old Island's rebuilt shore houses crossed the shore line by 0.0104 m².

**Calibration:**
- **Values:**
  - seed 9; street spacing × 2.5; cross streets × 2.0
  - a close every ~150 m of street
  - houses from the lower two-thirds of the size range; a boys' quarters behind 40%; 40% of plots empty (walled, never built)
- **How we chose them:** six sweeps, about 100 runs.

## 5. Result vs real (same measuring stick for both)

| | Real, typical km² | Real, dense km² | **Heights** |
|---|---|---|---|
| Streets, km/km² (edge roads half) | 11.0 | 12.0 | **12.4** |
| Main roads, km/km² (edge roads half) | 5.3 | 4.3 | **4.0** |
| Junctions/km² | 46 | 51 | **49** |
| T-junctions | 91% | 92% | **90%** |
| Dead ends per junction | 0.41 | 0.33 | **0.37** |
| Blocks/km² (counted closed) | 20 | 25 | **25** |
| Buildings/km² | 378 | 503 | **485** |
| Ground built on | 12% | 15% | **13%** |
| Typical house | 218 m² | 239 m² | **252 m²** |
| Over 400 m² | 28% | 26% | **24%** |
| Gap between houses | 3.4 m | 3.5 m | **4.2 m** |
| Front row | 21% | 19% | **16%** |
| Gates across streets, per km² | 6.1 (mapped) | | **17** |

**Checks:** `check_district.py heights` passes all its checks.

**What doesn't match yet (honest):**
- **It looks like the Estate.** The numbers match, but the picture is a tidy grid of walled plots. Real Ikoyi has curving roads, a golf course, big empty grounds, and big plots next to clusters of small ones. Ours has the same plot everywhere.
- **Only one kind of place.** The real study area is three: Ikoyi's leafy compounds, Victoria Island's office and hotel blocks, and Banana Island's enclave. Ours is Ikoyi everywhere, with Victoria Island reduced to three towers and the club strip.
- **The beach is bare.** It has no shacks and no horses.
- **Houses** are a little big (252 m² against 218–239) and a little far apart (4.2 m against 3.5).
- **Gates:** we gate every cul-de-sac (17 per km²); OSM maps 6.1. Mapped gates are a floor, and the model asks for gated cul-de-sacs, so this is a design choice.
- **The one-way streets** (40%) are logged, not built.

## 6. Questions for Daramola
1. **The Cable Bridge** goes to the Frontier, like the real link bridge to Lekki. Is that the crossing you meant, or should it reach somewhere else (the Gold Island, Old Island)?
2. **Victoria Island:** should part of the Heights become an office-and-hotel quarter (big blocks, towers on the main roads), rather than leafy compounds everywhere?
3. **Sunday Beach:** a strip of shacks, bars and horse rides on the sand?

## Files
- **Study:** `scripts/study_extract.py "Eti Osa" heights "3.418,6.440,3.450,6.462;3.405,6.420,3.440,6.438;3.444,6.455,3.462,6.470"`, then `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_landmarks.py` and `study_isms.py`, all with `heights`. Then `scripts/study_boxheights.py "Eti Osa" "<the same boxes>"` for the height bands.
- **Generator:** `scripts/gen_fabric.py heights 9 2.5` → `web/gen-heights.json`. `web/network.json` gains the Heights' edges and crossings.
- **Picture:** `docs/img/heights-vs-real.png`
