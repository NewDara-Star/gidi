# Maze pattern study: Mushin + Shomolu → The Maze (v1)

Status: done for the Maze (13 Oct 2026). Method: **Option 2.** We measure the real place, turn the numbers into rules, and generate original streets and houses from the rules. **No real street or building geometry is copied into Gidi.** Data: OpenStreetMap (ODbL), Lagos extract. Area studied: Mushin + Shomolu LGAs, 33.7 km².

## 1. How it transfers to the scale of our world

- Gidi has about 21 km² of land; the Lagos it draws on is about 50× bigger. The Maze is 0.95 km²; Mushin + Shomolu are 33.7 km² (1:35).
- **Fabric stays 1:1.** Street widths, block sizes, house sizes and gaps keep their real size, because the player walks and drives at real scale. If we shrank them, the place would feel like a toy.
- **Counts shrink.** The Maze is one dense square kilometre of Mushin, not all of it. We matched it to a typical (median) and a dense (75th percentile) real 1 km square.
- **Landmarks are chosen, not scaled.** Real Mushin has dozens of markets. The Maze gets one parts market and one print row, chosen for the story.
- **The road hierarchy compresses.** In the real place, main roads are about 1 km apart. The Maze gets the Ring Road, one through-road and its four edge roads.

## 2. Road connections to other districts

- In the real place, 83% of the district edge runs along a hard line: a major road, the rail or water. So **every Gidi district edge is a road shared with the neighbour** (or the rail, or water). The edge road is generated once and stored in `web/network.json`. The neighbour builds against the same road, so houses never sit on it.
- **Gateways** are where roads cross into the neighbour. They are recorded in `web/network.json` so the neighbour continues those roads instead of starting new ones.
  - Real: 1.87 main-road gateways per km of edge (median 277 m apart), plus 0.86 street gateways per km.
  - Maze: 8 road gateways on 3.9 km of edge (about 2 per km, a bit sparser than real), plus 2 rail crossings:
    - **Jungle City:** Adeleke Road (main), one street.
    - **Food Gate:** Adeleke Road (main), one street.
    - **The Hub:** Ring Road, rail, one street.
    - **Water Town:** Ring Road, rail, one street.
    - The north-west corner links to the Northern Road.
- Other residential streets meet the edge road at a T, as in the real place.
- **Next districts must load `web/network.json` first.**

## 3. What the data says

### Roads
- **Street density:** 14.4 km of drivable street per km² over the whole area. Real 1 km squares range from 13.9 to 19.2 km (25th–90th percentile).
- **Service lanes and drives:** another 3.0 km/km².
- **No city-wide grid,** but every small patch is a grid:
  - Grid order of the whole area: 0.071 (0 is random, 1 is a perfect grid).
  - Inside each 400 m patch: median 0.7.
  - Neighbouring patches turn by a median of 35.0°.
  - This patchwork of small grids is what makes it a maze.
- **Streets are straight:** almost no curving between junctions.
- **Junctions are mostly T's:** 84% T, 16% X. There are 0.2 dead ends per junction.
- **Parallel streets** are a median 73.1 m apart (25th–75th percentile: 66.8–99.8 m).
- **Street length between junctions:** median 76.9 m.
- **Blocks:**
  - Median 11759 m², about 80.7 m wide.
  - Long side about 2.0× the short side.
  - 90% are under 32171 m².
- **Main roads:** 3.53 km/km². Side streets hit a main road every ~68.8 m, almost always at a T.
- **Surface:** of the streets that are tagged, about 3 in 4 are unpaved.
- **One-way:** 20% of street length is one-way, mostly main roads and dual carriageways.
- **Street names:** "Street" dominates (486 of the named streets), then Road (107), then Avenue, Close, Way, Crescent and Lane. The generator uses the same mix.

### Buildings (55,519 footprints)
- **Density:** 1,649 per km². They cover 30% of the land, or 26–41% inside residential squares.
- **Size:**
  - Median footprint 134.4 m², about 15.9 × 8.5 m.
  - 27% are under 60 m²: sheds, kiosks, toilets, shops.
  - Only 0.5% are over 1,500 m².
- **Orientation:** 86% sit square to the nearest street. In the front row, 69% have the **gable end to the street**: deep, narrow houses on deep plots.
- **Front and back rows:** 52% stand within 12 m of a street centreline. The rest are back rows and compounds (face-me-I-face-you).
- **Gaps:** the median gap to the next building is 1.1 m, and 20% are touching.
- **Big buildings (>1,500 m²):** 8.7 per km². They sit nearer main roads: median 91.2 m, against 129.7 m for all buildings. These are warehouses, factories and church halls.
- **Heights: not in the data.** Only a few hundred buildings are tagged, and badly. We need photos, or Daramola's memory, for storeys.

### Land, water, rail, power
- **Mapped land use (ha):** residential 1430.8, industrial 128.3 (≈4%), commercial 62.8, schools 57.5 in 24 sites, hospital 54.5, military 53.4, wetland 46.9, retail 28.7, cemetery 15.2, pitches 8.3 in 29 pitches (~0.3 ha each), parking 5.1.
- **Markets:** median 1.4 ha, and always touching a main road.
- **Places of worship:** median 26 m from a main road. **Schools:** median 65 m back from one.
- **Water:** 8.55 km of drains, 6.13 km of streams and 4.38 km of canal, about 0.6 km per km².
- **Rail:** 16.55 km of track, but only 12 road crossings (about one per 1.4 km) and 15 level crossings. 658 buildings stand within 30 m of the track, 247 of them within 15 m. **Houses hug the line.**
- **Power:** 23 pylons, 8 lines and 3 substations are mapped.
- **Trees:** 114 trees are mapped in 33.7 km². Daramola was right.

### Limits of the data
- **Civic places** (churches, mosques, clinics) are badly under-mapped in OSM here. We use them for placement rules only, never for counts.
- **Elevation and land cover:** we could not get these. The servers are blocked from this workspace, and we did not route around the block.
- **Mapping date:** the building footprints look complete but their date is unknown.

## 4. The generator (`scripts/gen_fabric.py`)
1. **Network first.**
   - Shared edge roads come from `network.json`, or are created there.
   - The Ring Road and the rail pass through.
   - One through-road is placed: it crosses arterials at more than 55° and the rail at more than 40° (a level crossing).
   - A short link joins the district corner to any nearby arterial.
2. **Sectors.**
   - The mains and the rail cut the district into sectors. Sectors over 14 ha are split by a collector street, which gives the "patches that turn" look.
   - Each sector lines its streets up with its longest road frontage. Streets next to the rail run parallel to it.
3. **Streets.**
   - Ribs run perpendicular to the frontage, spaced by the real spacing distribution × 1.35. This is the one calibration knob: the raw measure undercounts because short stubs count as "parallel streets".
   - 12% of ribs stop short, as dead ends.
   - Cross streets come every ~150 m. Half of them line up with the cross street across the rib (X junctions); the rest are staggered (T junctions).
   - Streets stop 9 m short of the rail.
   - Clean-up: slivers are pruned and near-misses snapped.
   - No block may be bigger than the real 90th percentile: bigger ones get a street through the middle.
   - Deep blocks get dead-end service lanes.
4. **Parcels.** Market (1.4 ha, fronting a main road), industrial yard (~3 ha), school (~0.8 ha, set back from the main road), pitch (0.3 ha), motor park.
5. **Plots and houses.**
   - Every frontage is cut into plots one house wide, running back toward the middle of the block.
   - Inside each plot: a front house (gable to the street 69% of the time), a 1.5–4 m courtyard, then back houses. Sometimes a shed. 7% of plots stay vacant.
   - Sizes and gaps are drawn from the real distributions.
   - Houses keep clear of street centrelines: 3.4 m on streets, 6.5 m on mains, 12.5 m on arterials, 6 m from the rail, 4 m from the canal. **No house on a road** (checked: 0 overlaps).
6. **Civic places** take over real plots, near main roads when they need passing trade. **Landmarks** sit on their parcels or on a street.

## 5. Result vs real (same measuring stick for both)

| | Real, typical km² | Real, dense km² | Maze |
|---|---|---|---|
| Streets, km/km² | 16.7 | 18.4 | 18.3 |
| Junctions/km² | 78 | 98 | 101 |
| T-junctions | 87% | 81% | 84% |
| Dead ends per junction | 0.31 | 0.12 | 0.12 |
| Typical block | 1.5 ha | 1.0 ha | 1.3 ha |
| Buildings/km² | 1,541 | 2,855 | 2,654 |
| Ground built on | 31% | 39% | 33% |
| Typical house | 190 m² | 112 m² | 100 m² |
| Gap between houses | 1.7 m | 1.0 m | 1.4 m |

**What doesn't match yet (honest):**
- **Main roads:** about 4 km/km², against 1–3 in the real place. A small district with four edge roads has more main road per km². This is accepted.
- **Small blocks:** more of them (about 60 per km² against 24–39). Slivers form along the rail and the edges.
- **Front row:** fewer houses (about 48%, against 61–63%). Deep plots get more back houses.
- **Regularity:** streets are straighter and more regular than the real place, and blocks are tidier. It reads like a slightly more planned Mushin. More bend and more irregular plot widths would help.
- **Civic schools:** the civic-layer school pins are not tied to the school parcel yet.

## 6. Public spaces the data says the Maze needs (check with Daramola)
- A market on a main road (~1.4 ha). **Done:** Ladi Lane Parts Market.
- An industrial/warehouse yard by the rail. **Done:** Daleko Grain Yard.
- A school compound set back from the main road, and a sand pitch nearby. **Done.**
- A motor park or garage on a main road. **Done** (small).
- An open drainage canal through the houses. **Done:** Gang Canal.
- Houses right up against the rail, with one level crossing. **Done.**
- Pylons or a transformer feeding a whole block. **Done:** Transformer 44.
- **Not added:**
  - a cemetery (real: 0.45% of land, too small to matter at 1 km²)
  - a barracks (real: 53 ha of military land in the area; this could be a story place, Daramola's call)
  - a hospital compound (real: 1.6% of land; the civic layer has clinics only)
- **Questions for Daramola's memory:** How many storeys are typical? Are the street fronts all shops? Where do people actually gather: a junction, a buka, a viewing centre?

## Files
- **Study pipeline:**
  - `scripts/study_extract.py`: pulls everything OSM has for the area.
  - `scripts/study_analyse.py`: patterns → `study-maze.json`.
  - `scripts/study_connect.py`: gateways and 1 km squares.
  - `scripts/study_core.py`: the reference squares.
  - `scripts/fabric_metrics.py`: one measuring stick for real and Gidi.
- **Generator:** `scripts/gen_fabric.py maze 71 1.35`, which writes `web/gen-maze.json` and `web/network.json`. `scripts/draw_gen.py` draws the comparison.
- **Lifting retired:** the old lifted fabric is quarantined in `_lifted_do_not_publish/` and never baked. `bake_web.py` no longer has the transplant code.
- **Map:** Gidi Maps artifact, Version 4. Buildings, plots, lanes and the canal show when you zoom in. The Maze panel has a "Town plan check" table and "Roads to neighbours".
