# The deep study: every district's inspiration, from all the data

> **History (the old map, 13-21 Oct).** The scripts that made this study (`study_deep.py`, `deep_prep.py`) and the old districts it compares against were deleted on 25 Oct (git tag `before-cleanup-25oct`); the real-Lagos numbers stand (`docs/RESEARCH.md`).

The owner asked for this on 15 Oct 2026: "the research should look at everything in the data and take them into consideration". Every Gidi district is rebuilt by one shared generator. Each district gets its own profile, and the profile is set from this study.

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
1. `python3 scripts/deep_prep.py`: one pass over the big building files, cut per district, into `~/gidi-data/research/data/deep-cache/`.
2. `python3 scripts/study_deep.py <id>` for each district. They run side by side; about 20 s each, a few minutes for Railside.
3. `python3 scripts/deep_report.py` writes the pages.

## Output
- `docs/data/deep/<id>.json`: the numbers.
- `docs/studies/<id>.md`: the page, ending in the generator's targets.
- `docs/img/study-<id>.png`: buildings by storeys, main roads, and the fabric types.

## Known limits
- **Places and street things** are what people have mapped. They cluster on main roads, and lamps, signals and bus stops are badly under-mapped, so they're floors, not counts.
- **Heights** are 2023 estimates at about 3 m a storey. A zinc roof on a high plinth can read as two storeys.
- **Study areas** are the boxes and LGAs each district was first studied on. The two new ones:
  - **Saba:** Yaba, Sabo, Akoka and the university (Lagos Mainland and Shomolu, 3.368–3.405 E, 6.497–6.528 N)
  - **The Airport:** the airport, its cargo side and hotel strip (Ikeja and Oshodi/Isolo, 3.295–3.345 E, 6.555–6.592 N)

## From the study to the generator (`scripts/deep_profile.py`)
- **District-wide settings.** Every district with a study gets the Lagos fabric. Its touching, gaps, empty plots, back rows, block fill, small buildings, wobble and height bands come from the study (`district_profiles._deep`). The district keeps its own landmarks, parcels and models. The conversions are calibrated on the Food Gate pilot: fed real Food Gate's numbers, they give back the pilot's hand-tuned settings.
- **Fabric types.** The district is cut into its types in the study's shares (`deep_profile.zones`).
  - **Where each type goes:**
    - the busiest, most built-over types along the main roads
    - the open ones toward the water and the city's edge
    - a slow wobble, so the zones read as neighbourhoods
  - **Each zone's own settings:** its empty plots follow its real cover, plus its touching, back rows, block fill, house size and a lean on height. Taller types take more of the tall buildings, and the district's bands stay as measured.
- **The check.** `scripts/deep_check.py <id> [gen.json] [picture.png]` measures a generated district the way the study measured real Lagos, and flags anything more than 20% off.
- **Names.** `scripts/rename_mains.py` runs after a side-by-side build: no two roads share a first name, and none uses the name of a famous real person or street.
