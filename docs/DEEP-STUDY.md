# The deep study: every district's inspiration, from all the data

The owner asked for this on 15 Oct 2026: "the research should look at everything in the data and take them into consideration". Every Gidi district is rebuilt in the v2 frame (`docs/LAYOUT-V2.md`) by one shared generator. Each district gets its own profile, and the profile is set from this study.

**The rule:** Gidi takes numbers from the study, never an outline, a name or an image.

## The sources

| Source | What it gives |
|---|---|
| Google Open Buildings v3 | Every building outline it traced (we keep confidence 70% and up): counts, sizes, shapes, gaps, touching |
| Google Open Buildings 2.5D (2023) | Building heights at 0.5 m (read at 2 m), so storeys per building |
| Microsoft building outlines | A cross-check on the counts |
| OpenStreetMap (`study-<id>.pkl`) | Streams, drains and canals, markets, power lines, rail, amenity points |
| Overture | Road segments (class, surface, bridges, junctions), places (churches, schools, shops...), street things (gates, poles, bus stops, lamps), land use, land |
| ESA WorldCover 2021 | Land cover at 10 m: built-up, trees, grass, wetland, mangrove, water |
| WorldPop 2020 | People, about 100 m cells |
| Copernicus GLO-30 | Ground height and slope |

## What is measured
- **Buildings:**
  - density and cover, over all the land and over the built 500 m squares
  - size bands, shape, grain
  - touching and gaps
  - the structure measures (`scripts/structure.py`): street front, line to the street, setback, block fill, edge and back cover
- **Heights:** storeys share, storeys by size, tall buildings, floor area.
- **Streets:**
  - km by class, surfaces
  - junctions, T share, dead ends
  - block sizes, grain
  - bridges and flyovers, rail, paths
- **Places:** by Gidi kind per km², and how many sit on a main road.
- **Street things, land use and land cover, people, ground, water.**
- **Gradients:** how the fabric changes away from main roads and away from open water.
- **Fabric types:** the district's 250 m cells clustered into 3–4 types. A district is never one fabric; the generator lays its types out in the same shares.
- **Landmarks:** the biggest buildings, and the place listed nearest each one.

## Run
1. `python3 scripts/deep_prep.py`: one pass over the big building files, cut per district, into `~/Real-world/research/data/deep-cache/`.
2. `python3 scripts/study_deep.py <id>` for each district. They run side by side; about 20 s each, a few minutes for Railside.
3. `python3 scripts/deep_report.py` writes the pages.

## Output
- `docs/data/deep/<id>.json`: the numbers.
- `docs/studies/<id>.md`: the page, ending in the generator's targets.
- `docs/img/study-<id>.png`: buildings by storeys, main roads, and the fabric types.

## Known limits
- **Places and street things** are what people have mapped. They cluster on main roads, and lamps, signals and bus stops are badly under-mapped, so they're floors, not counts.
- **Heights** are 2023 estimates at about 3 m a storey. A zinc roof on a high plinth can read as two storeys.
- **Study areas** are the boxes and LGAs each district was first studied on (`docs/DISTRICT-BRIEF.md`). The two new ones:
  - **The Campus:** Yaba, Sabo, Akoka and the university (Lagos Mainland and Shomolu, 3.368–3.405 E, 6.497–6.528 N)
  - **The Airport:** the airport, its cargo side and hotel strip (Ikeja and Oshodi/Isolo, 3.295–3.345 E, 6.555–6.592 N)
