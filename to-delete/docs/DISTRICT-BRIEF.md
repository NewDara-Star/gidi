# Brief: build one Gidi district

One session = one district. Read this brief, `README.md` and `docs/maze-pattern-study.md` (the worked example), then do the steps.

## Owner's rules (non-negotiable)
- **No copying real Lagos.** Study real Lagos, then generate original streets and buildings from the measured rules. Never trace or transplant real street layouts or building outlines.
- **Invented names only.** No real brands, companies or people.
- **Safe ground.** Churches, mosques, schools, hospitals and clinics are never crime locations. Nor is any place the district model flags `"safe": true` in `web/districts_info.json` (the Palace); the bake marks them all, with their plots, in `safe_ground`. Sacred traditions (Eyo, Oro, Egungun, etc.) are never criminal.
- **Never push to `main`.** Work on a branch `district/<id>` and open a pull request. Only the owner merges.
- **Never fetch** Pinterest, Nominatim or Overpass. Never use Google Maps, Street View or 3D Tiles as data. If a site is blocked, say so; don't work around it.
- **Look at what you make before showing it.** Check the picture, and check that no house sits on a road.
- **Write for a designer, not a coder:** plain words, honest critique, one recommendation.

## Order
Districts share edge roads through `web/network.json`. **Never work on two neighbouring districts at the same time.**
- **Done:** maze, hub, jungle, foodgate, watertown, capital, bazaar, port, railside, estate, oldisland, heights, frontier, border, oldshore
- **Then:** none: all fifteen districts are built
- **Safe in parallel** (they don't touch each other): border + oldshore, or frontier + bazaar. Check `scripts/map02.py` polygons when unsure.

## District → inspiration (OSM `name` of the LGA, as in `adm6.geojson`)
| id | Gidi name | Study these LGAs | Notes |
|---|---|---|---|
| hub | The Hub | Oshodi/Isolo, Surulere | Motor parks, interchange, flyovers |
| jungle | Jungle City | Ajeromi/Ifelodun (+ Amuwo Odofin for Festac) | Ajegunle is the densest place in Lagos (~44k people/km²). Study Ajegunle on its own first. |
| foodgate | Food Gate | Kosofe | Mile 12 market, Ojota park |
| watertown | Water Town | Lagos Mainland (Makoko), Shomolu (Bariga) | Needs a neighbourhood-level study (waterfront strip), not whole LGAs |
| capital | The Capital | Ikeja | Computer village, government |
| bazaar | The Bazaar | Ojo | Trade Fair |
| port | The Port | Apapa | Containers, tank farms |
| railside | Railside | Agege, Ifako/Ijaye, Alimosho | Bread, cattle market, sprawl |
| estate | The Estate | Ikeja, Kosofe | **Neighbourhood-level only:** Ikeja GRA, Magodo, Omole. Whole LGAs would be wrong. |
| oldisland | Old Island | Lagos Island | Old dense core, markets, palace |
| heights | The Heights | Eti Osa | **Neighbourhood-level:** Ikoyi, VI, Banana Island |
| frontier | The Frontier | Ibeju Lekki (+ Lekki part of Eti Osa) | New estates, land war, refinery |
| oldshore | Old Shore | Ìkòròdú, Epe | Royal town, ferries, fish |
| border | The Border | Badagry | Smuggling, beach |

Use `data/results/lga_table.json` for storeys, people, trees and terrain for each area.

## Steps
1. **Pull and branch:** `git pull`, then `git checkout -b district/<id>`.
2. **Study:**
   - `python3 scripts/study_extract.py "<LGA1>,<LGA2>" <id>`
   - then `study_analyse.py <id>`, `study_connect.py <id>` and `study_core.py <id>`
   - For neighbourhood-level districts, pass a box: `study_extract.py "<LGA>" <id> west,south,east,north` (degrees). Food Gate is the worked example; several boxes are separated by `;` (Water Town). For a waterfront, `scripts/study_village.py <id>` splits the stilt village off the land, and `study_core.py <id> --land` measures the land only.
   - Where OSM maps the streets but few of the buildings (central Ikeja), `scripts/study_undermapped.py` estimates the building cover from WorldCover and the well-mapped districts. The Capital is the worked example.
   - Where OSM maps the buildings of only some neighbourhoods in the study area (the Estate: Ikeja GRA traced, Magodo and Omole not), `scripts/study_wellmapped.py <id> <box>` measures them on the traced 250 m cells of one box instead. Run it after `study_core.py`. Old Island used it too, on the old core: OSM's Lagos Island outline is mostly lagoon, so its study is also boxed to the island.
   - For a neighbourhood-level study, measure the height bands on the boxes too: `scripts/study_boxheights.py "<LGA>" "<boxes>"`, and put them in the profile as `h_bands`. An LGA can mix very different places (Eti Osa: Ikoyi's towers and Lekki's bungalows).
   - **Log the Lagos-isms (every district from now on):** run `scripts/study_isms.py <id>` and add the district's column and anything new to `docs/LAGOS-ISMS.md`: the eccentricities in the real data (streets ending at canals or rail, buildings in road reserves or on drain banks, markets on the carriageway, roads doing too many jobs, missing links, unfinished buildings, odd junctions, flood-prone low spots, pedestrians forced onto expressways). For each: what it is, where (LGA and coordinates), how often per km², and which Gidi district it would suit. **Don't build any of it into Gidi yet:** that's the owner's "make it feel like Lagos" pass, after the whole map is done.
   - Write `docs/<id>-pattern-study.md` in the same shape as the Maze study. It covers roads, buildings, land, water, rail, connections and the limits of the data, plus the height, people, tree and terrain numbers from `lga_table.json`.
3. **Generate:**
   - Add the district to `scripts/district_profiles.py`. The Hub's and the Maze's profiles are the worked examples.
   - To rebuild a district whose neighbours are already built, set `keep_gateways`. Its edge roads and crossings in `web/network.json` are then reused exactly, as the Maze v2 does.
   - `rail_frontage` builds houses up to the rail's clear strip. `fence_parcels` stops dead ends at a parcel's edge. Both are worth turning on for new districts.
   - `gen_fabric.py` was written for the Maze. Generalise what it needs:
     - parcels and landmarks for this district (its market, park, port, etc.)
     - storeys per building from the district's height bands
     - its own style
   - Keep the network rules: shared edge roads, gateways, arterials crossed at real angles, and no block bigger than the real 90th percentile.
   - **Compare blocks the fair way:** use `blocks_per_km2_closed` from `study_core.py`, which counts the real square's blocks with its border closed, as a Gidi district's edge roads close it. The old open count shows about half. `sector_split_ha` (collector streets) is the main lever; `spurs` adds dead-end side streets without new blocks.
   - **When a neighbour of a finished district is built,** give the finished one `keep_gateways` and rebuild it, so it keeps regenerating byte-identical (the Hub, Jungle City, Food Gate, Water Town, the Capital, the Bazaar, Old Island, the Heights and Railside have it).
   - Calibrate with the spacing scale and seeds until the metrics sit between the real "typical" and "dense" squares. The Maze v2 used seed 57, scale 1.8, the Hub seed 23, scale 2.4, Jungle City seed 71, scale 2.2, Food Gate seed 3, scale 1.4, Water Town seed 21, scale 2.1 (fingers to the shore), the Capital seed 3, scale 3.8, the Bazaar seed 9, scale 3.4, the Port seed 11, scale 4.5, Railside seed 7, scale 1.5, the Estate seed 3, scale 4.8, Old Island seed 11, scale 1.6, the Heights seed 13, scale 2.5, the Frontier seed 5, scale 3.8, the Border seed 1, scale 6.0, and Old Shore seed 6, scale 4.4. Sweep with `GIDI_TUNE='{"back_row": 0.45}'` and similar settings.
4. **Check:**
   - Run `scripts/draw_gen.py <id> out.png real` and look at it.
   - Run `python3 scripts/check_district.py <id>`. All checks must pass: 0 houses on roads, 0 overlaps, 0 neighbour streets inside, edge roads match `network.json`, the neighbours' gateways are continued, every lane, path and footbridge is joined to the network, and every building is within 45 m of a way.
   - Turn on `walk` in the profile (the Maze's is the example): it adds footpaths along the rail, along canal banks and across the rail, makes lanes start on streets, and keeps buildings within reach of a way.
   - Look at the knot or any landmark close up: `ZOOM=x0,y0,x1,y1 python3 scripts/draw_gen.py <id> out.png`.
   - **Everyday places are placed by coverage.** `bake_web.py` puts schools, places of worship and chemists/clinics on real plots so that every house has each within 10 min walk (15 at most). Check 13 fails otherwise; run it after baking.
   - **Locked places** (`web/locked.json`):
     - **the opening:** the Maze's parts market and its aisles, The steal's stall, Tunde's room, the boss's post (a canopy at the market's west mouth), and the Hub's boss's motor park
     - **Water Town:** the Okobaba Sawmill's plot
     - Regenerating keeps them exactly, and check 12 fails if any of them moves.
     - To re-record them on purpose, run the generator with `GIDI_LOCK=write`. Locks that already exist are kept.
5. **Bake and look:** `python3 scripts/bake_web.py` then `python3 scripts/build_viewer.py`. This writes `web/gidi-maps.html`, the one-page map with the 2D/3D toggle. Open it, check your district in 2D and 3D, and look before publishing.
6. **3D pass:** the 3D view is the test of the 2D map. A new district gets its 3D automatically: the Blender kit styles every building, plot, road and place from the data by rule (`docs/LAGOS-LOOK.md`). Nothing is modelled by hand per district. The district's character (`CHARACTER` in `legacy/blender/gidi_kit/rules.py`: dense, sprawl, old_island, elite, civic, waterfront or port) picks its styles. All 15 districts have one already.
   - Build its tiles: `python3 legacy/blender/city_run.py --detail web --only "<tx,ty;...>"` for the district's tiles, or the whole city. Add `--detail full` for the close-up build.
   - Run the 3D audit: `.venv/bin/python scripts/audit3d.py <id>` (it needs shapely: `.venv/bin/pip install shapely numpy networkx`). It writes `docs/audit/<id>.md` and adds the district's row to `docs/audit/README.md`.
   - **Map problems (R1 to R6, D) are fixed in the 2D map, in the generator, never patched in 3D:**
     - roads running along each other
     - ends that stop short of a road or run past it
     - knife-edge crossings
     - roads over water with no bridge
     - decks with no road
     - roads listed twice
     If it looks wrong in 3D, the map is wrong in that spot.
   - **Model gaps (M1 to M4) are kit work.** The 3D audit lists them:
     - a building or parcel kind the kit has no builder for (M1, M2)
     - a named landmark with no model of its own (M3: give it an entry in `legacy/blender/gidi_kit/landmarks.py`)
     - a place on the map with nothing of its kind under it (M4: usually a map fix, such as a pitch drawn on a house)
     Research the real thing (`docs/look/`), add the kit piece, render its contact sheet and check it, rebuild, and re-audit until M1 to M3 are 0.
   - Open `web/gidi-maps.html` in 3D (serve the repo root), zoom into the district, and look at its markets, junctions, bridges and landmarks. It should read as Lagos.
7. **City living test:** every district ends with this test.
   - Run the test in `docs/CITY-LIVING-TEST.md` on the whole built city, including the new district. Use `scripts/explore_city.py` and Haiku sub-agents, one persona for each district and one more for the new district.
   - Verify every problem the agents report, fix the real ones, and write `docs/living-test-<date>.md` with the standard-trips table.
8. **Report and PR:**
   - Commit, push the branch and open a PR. Show the owner the side-by-side picture and the match table: what matched, what didn't, and why.
   - After the owner merges, republish `web/gidi-maps.html` to the live map (https://claude.ai/artifact/GnebG5XRaJRdTC8edK3yqP; read it first, then publish to that URL), so the city map grows district by district.

## Paste this to start a session
> Clone https://github.com/NewDara-Star/gidi. Read README.md and docs/DISTRICT-BRIEF.md, then build the **<district id>** district following the brief. Work on a branch and open a PR; don't push to main.
