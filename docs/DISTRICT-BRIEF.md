# Brief: build one Gidi district

One session = one district. Read this brief, `README.md` and `docs/maze-pattern-study.md` (the worked example), then do the steps.

## Owner's rules (non-negotiable)
- **No copying real Lagos.** Study real Lagos, then generate original streets and buildings from the measured rules. Never trace or transplant real street layouts or building outlines.
- **Invented names only.** No real brands, companies or people.
- **Safe ground.** Churches, mosques, schools, hospitals and clinics are never crime locations. Sacred traditions (Eyo, Oro, Egungun, etc.) are never criminal.
- **Never push to `main`.** Work on a branch `district/<id>` and open a pull request. Only the owner merges.
- **Never fetch** Pinterest, Nominatim or Overpass. Never use Google Maps, Street View or 3D Tiles as data. If a site is blocked, say so; don't work around it.
- **Never read or use the `gta5` folder** on the owner's Mac.
- **Look at what you make before showing it.** Check the picture, and check that no house sits on a road.
- **Write for a designer, not a coder:** plain words, honest critique, one recommendation.

## Order
Districts share edge roads through `web/network.json`. **Never work on two neighbouring districts at the same time.**
- **Done:** maze, hub (in review)
- **Ring around the Maze (one at a time):** jungle, foodgate, watertown
- **Then:** capital, bazaar, port, railside, estate, oldisland, heights, frontier, oldshore, border
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
   - For the neighbourhood-level districts, add a bounding-box or polygon option to `study_extract.py`.
   - Write `docs/<id>-pattern-study.md` in the same shape as the Maze study. It covers roads, buildings, land, water, rail, connections and the limits of the data, plus the height, people, tree and terrain numbers from `lga_table.json`.
3. **Generate:**
   - Add the district to `scripts/district_profiles.py` (the Hub's profile is the worked example). The Maze has no profile, so it keeps its original behaviour.
   - `gen_fabric.py` was written for the Maze. Generalise what it needs:
     - parcels and landmarks for this district (its market, park, port, etc.)
     - storeys per building from the district's height bands
     - its own style
   - Keep the network rules: shared edge roads, gateways, arterials crossed at real angles, and no block bigger than the real 90th percentile.
   - Calibrate with the spacing scale and seeds until the metrics sit between the real "typical" and "dense" squares. The Maze used seed 71, scale 1.35.
4. **Check:**
   - Run `scripts/draw_gen.py <id> out.png real` and look at it.
   - Run `python3 scripts/check_district.py <id>`. All checks must pass: 0 houses on roads, 0 overlaps, 0 neighbour streets inside, edge roads match `network.json`, the neighbours' gateways are continued.
   - Look at the knot or any landmark close up: `ZOOM=x0,y0,x1,y1 python3 scripts/draw_gen.py <id> out.png`.
5. **Bake and look:** `python3 scripts/bake_web.py` then `python3 scripts/build_viewer.py`. This writes `web/gidi-maps.html`, the one-page map with the 2D/3D toggle. Open it, check your district in 2D and 3D, and look before publishing.
6. **Report and PR:**
   - Commit, push the branch and open a PR. Show the owner the side-by-side picture and the match table: what matched, what didn't, and why.
   - After the owner merges, republish `web/gidi-maps.html` to the live map (https://claude.ai/artifact/GnebG5XRaJRdTC8edK3yqP; read it first, then publish to that URL), so the city map grows district by district.

## Paste this to start a session
> Clone https://github.com/NewDara-Star/gidi. Read README.md and docs/DISTRICT-BRIEF.md, then build the **<district id>** district following the brief. Work on a branch and open a PR; don't push to main.
