# Gidi

The city for Tunde's story: an invented city with the feeling of Lagos, built for an Unreal open-world game.
This repo is the **city master plan**: 15 districts, roads, buildings and places, generated from patterns measured in real Lagos.
That master plan is what gets carried into Unreal.

**Rule zero:** we study real Lagos and build our own city. No real street layout, building outline or name is copied into Gidi.

## What's here
| Path | What |
|---|---|
| `scripts/map02.py` | District layout v0.3: polygons, lagoon, arterials (map units 0.8 km). |
| `scripts/study_extract.py` → `study_analyse.py` → `study_connect.py` → `study_core.py` | Pattern study of a district's real inspiration areas (OSM). Statistics only. |
| `scripts/study_landmarks.py` | Sizes of a district's big structures (flyovers, interchanges, footbridges, terminals, stadiums, stations, hotels). Statistics only. |
| `scripts/fabric_metrics.py` | One measuring stick for real and generated fabric. |
| `scripts/gen_fabric.py` | The original street + building generator. Calibrated to a study, it writes `web/gen-<id>.json` and updates `web/network.json`. |
| `scripts/district_profiles.py` | Per-district settings for the generator (landmarks, calibration knobs, height bands), each with its source. The Maze and the Hub both have one. Settings such as `keep_gateways`, `rail_frontage` and `fence_parcels` switch on newer behaviour per district. |
| `scripts/landmarks.py` | Big pieces laid out before the street fabric: the interchange knot (flyovers, slip roads, skywalks), terminals, stations, stadiums. |
| `scripts/check_district.py` | Checks a generated district: no house on a road, no overlaps, edges match `network.json`, neighbours' gateways continued, storeys valid. |
| `scripts/draw_gen.py` | Side-by-side check picture: generated district vs a real 1 km square. |
| `scripts/bake_web.py` | Bakes everything into `web/gidi-data.js` for the 2D map (`web/shell.html` + `web/app.js`). |
| `web/network.json` | **Shared state between districts:** edge roads and gateways. Always pull before working. |
| `data/results/lga_table.json` | Per local government area: building heights (storey bands), people per km², tree/built-up cover, surface height. |
| `data/tools/` | Download scripts for the raw datasets. The raw files stay on the owner's Mac, about 17 GB. |
| `lagos.osm.pbf`, `adm6.geojson` | OpenStreetMap extract of Lagos and admin boundaries (ODbL, © OpenStreetMap contributors). |
| `docs/` | Districts v0.3, the Lagos LGA research, the data plan, the pattern studies (Maze, Hub, Jungle City, Food Gate, Water Town, the Capital, the Bazaar, the Port) and the city living tests. |

## Status
- **Done:** the Maze (Mushin + Shomolu). See `docs/maze-pattern-study.md`. v2 is in review: it was rebuilt with the current generator, and its edge roads and gateways are unchanged.
- **Done:** the Hub (Oshodi/Isolo + Surulere), see `docs/hub-pattern-study.md`; Jungle City (Ajegunle + Festac), see `docs/jungle-pattern-study.md`.
- **Done:** Food Gate (the Ojota–Ketu–Mile 12 corridor of Kosofe), see `docs/foodgate-pattern-study.md`.
- **Done:** Water Town (the Makoko–Iwaya and Bariga waterfront; v2 runs its streets down to the shore as fingers), see `docs/watertown-pattern-study.md`.
- **Done:** the Capital (central Ikeja; its buildings are estimated, because OSM maps few of them; okadas banned), see `docs/capital-pattern-study.md`.
- **Done:** the Bazaar (Ojo round the electronics market), see `docs/bazaar-pattern-study.md`.
- **Done:** the Port (Apapa; okadas banned), see `docs/port-pattern-study.md`.
- **City living test:** `docs/CITY-LIVING-TEST.md`; latest run `docs/living-test-2026-10-14c.md`.
- **Next:** one district per session. See `docs/DISTRICT-BRIEF.md`.
- **Live map, 2D and 3D** (private artifact): https://claude.ai/artifact/GnebG5XRaJRdTC8edK3yqP

## Data credits
- OpenStreetMap contributors (ODbL)
- Google Open Buildings 2.5D Temporal (CC-BY 4.0)
- ESA WorldCover 2021 (CC-BY 4.0)
- WorldPop 2020 (CC-BY 4.0)
- Copernicus DEM GLO-30 (© DLR/Airbus, provided under COPERNICUS by the European Union and ESA)
