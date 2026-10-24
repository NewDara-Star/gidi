# The documents, as a vault

Made by `scripts/inventory.py` with `scripts/doc_vault.py`: every markdown document in gidi, gidi-game and gidi-data, what it is for (its title, first line and the words that mark it out), what it links to, what points to it, and the documents nearest it in words. The repo folders open as a vault in Obsidian as they are; `vault.json` holds the same graph.

162 documents: 19 orphans (nothing points to them), 16 near-orphans (only CODEBASE.md or OLD-MAP.md do).

## Orphans

### `gidi:docs/data/deep-check/SUMMARY.md`
**(no title)**. Each cell is Gidi against its real inspiration (0% = the same; ⚠ = more than 20% off). "Squares" = built 500 m squares measured (under 5: a small sample).
For: skew, squares, sample, inspiration, saba, cell, touching, small. Last changed 2026-10-16, 22 lines.
Links to 0: 
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/look/COVERAGE.md` (0.22); `gidi:docs/audit/README.md` (0.2); `gidi:docs/studies/airport.md` (0.19).

### `gidi:docs/living-test-2026-10-13.md`
**City living test, 13 Oct 2026: the Maze, the Hub, Jungle City**. City living test, 13 Oct 2026: the Maze, the Hub, Jungle City: This is the first run of `docs/CITY-LIVING-TEST.md`, done on the whole built city.
For: minutes, walk, skywalk, jungle, interchange, station, tool, session. Last changed 2026-10-13, 108 lines.
Links to 4: `gidi:docs/CITY-LIVING-TEST.md`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:web/gidi-data.js`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-13b.md` (0.68); `gidi:docs/living-test-2026-10-13c.md` (0.6); `gidi:docs/living-test-2026-10-14.md` (0.5).

### `gidi:docs/living-test-2026-10-13b.md`
**City living test, 13 Oct 2026 (second run): the Maze, the Hub, Jungle City, Food Gate**. City living test, 13 Oct 2026 (second run): the Maze, the Hub, Jungle City, Food Gate: This is the second run of `docs/CITY-LIVING-TEST.md` today. It covers the whole built city after the owner's five fixes and the new district, Food Gate.
For: minutes, walk, interchange, jungle, stadium's, mile, yard, maze. Last changed 2026-10-13, 135 lines.
Links to 3: `gidi:docs/CITY-LIVING-TEST.md`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-13c.md` (0.72); `gidi:docs/living-test-2026-10-13.md` (0.68); `gidi:docs/living-test-2026-10-14.md` (0.59).

### `gidi:docs/living-test-2026-10-13c.md`
**City living test, 13 Oct 2026 (third run): all five districts**. City living test, 13 Oct 2026 (third run): all five districts: This is the third run of `docs/CITY-LIVING-TEST.md` today. It is the first run with all five built districts: the Maze, the Hub, Jungle City, Food Gate and the new Water Town.
For: minutes, walk, stilt, tool, foot, jungle, town, footbridge. Last changed 2026-10-13, 135 lines.
Links to 6: `gidi:docs/CITY-LIVING-TEST.md`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/walknet.py`, `gidi:web/districts_info.json`, `gidi:web/locked.json`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-13b.md` (0.72); `gidi:docs/living-test-2026-10-14.md` (0.63); `gidi:docs/living-test-2026-10-13.md` (0.6).

### `gidi:docs/living-test-2026-10-14.md`
**City living test, 14 Oct 2026: six districts, with the new Capital**. City living test, 14 Oct 2026: six districts, with the new Capital: This is the test in `docs/CITY-LIVING-TEST.md`, run on the whole built city after the Capital was added. It also covers Water Town v2 (fingers to the shore) and the boss's post, which this branch carries.
For: minutes, capital, walk, gadget, secretariat, fingers, village, mile. Last changed 2026-10-14, 127 lines.
Links to 4: `gidi:docs/CITY-LIVING-TEST.md`, `gidi:docs/capital-pattern-study.md`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14b.md` (0.65); `gidi:docs/living-test-2026-10-13c.md` (0.63); `gidi:docs/living-test-2026-10-13b.md` (0.59).

### `gidi:docs/living-test-2026-10-14b.md`
**City living test, 14 Oct 2026 (second run): seven districts, with the new Bazaar**. City living test, 14 Oct 2026 (second run): seven districts, with the new Bazaar: This run tests four changes on this branch: - **The fair block count:** the generator fix that came with it gives Jungle City and the Capital fewer collector streets. - **The okada ban zone** in the Capital. - **The new district:** the Bazaar.
For: walk, gadget, ride, dead-end, tool, minutes, village, jungle. Last changed 2026-10-14, 97 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14.md` (0.65); `gidi:docs/living-test-2026-10-13c.md` (0.53); `gidi:docs/living-test-2026-10-14d.md` (0.53).

### `gidi:docs/living-test-2026-10-14c.md`
**City living test, 14 Oct 2026 (third run): eight districts, with the new Port**. City living test, 14 Oct 2026 (third run): eight districts, with the new Port: There are two states: - **Before:** `main` at the start of this work (commit `1925734`, seven districts). - **After:** this branch, with the Port.
For: reserve, minutes, yard, port, container, chidi, okada, ngozi. Last changed 2026-10-14, 71 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14f.md` (0.44); `gidi:docs/living-test-2026-10-14.md` (0.43); `gidi:docs/living-test-2026-10-13c.md` (0.42).

### `gidi:docs/living-test-2026-10-14d.md`
**City living test, 14 Oct 2026 (fourth run): nine districts, with the new Railside**. City living test, 14 Oct 2026 (fourth run): nine districts, with the new Railside: There are two states: - **Before:** `main` at the start of this work (commit `8a23e34`, eight districts). - **After:** this branch.
For: re-laid, railside, roundabout, interchange, walk, capital, minutes, nine. Last changed 2026-10-14, 67 lines.
Links to 2: `gidi:docs/LAGOS-ISMS.md`, `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14b.md` (0.53); `gidi:docs/living-test-2026-10-14.md` (0.52); `gidi:docs/living-test-2026-10-14e.md` (0.52).

### `gidi:docs/living-test-2026-10-14e.md`
**City living test, 14 Oct 2026 (fifth run): ten districts, with the new Estate**. City living test, 14 Oct 2026 (fifth run): ten districts, with the new Estate: There are two states: - **Before:** `main` at the start of this work (commit `22daecd`, nine districts). - **After:** this branch.
For: capital's, senator's, musa's, okada, gadget, estate's, walk, emeka. Last changed 2026-10-14, 68 lines.
Links to 2: `gidi:docs/LAGOS-ISMS.md`, `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14d.md` (0.52); `gidi:docs/living-test-2026-10-14.md` (0.45); `gidi:docs/living-test-2026-10-14b.md` (0.43).

### `gidi:docs/living-test-2026-10-14f.md`
**City living test, 14 Oct 2026 (sixth run): eleven districts, with the new Old Island**. City living test, 14 Oct 2026 (sixth run): eleven districts, with the new Old Island: There are two states: - **Before:** `main` at the start of this work (commit `ea47fc6`, ten districts). - **After:** this branch.
For: bisi, sule, cloth, wharf, minutes, island, brazilian, walked. Last changed 2026-10-14, 83 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14g.md` (0.52); `gidi:docs/living-test-2026-10-14c.md` (0.44); `gidi:docs/living-test-2026-10-14d.md` (0.42).

### `gidi:docs/living-test-2026-10-14g.md`
**City living test, 14 Oct 2026 (seventh run): twelve districts, with the new Heights**. City living test, 14 Oct 2026 (seventh run): twelve districts, with the new Heights: There are two states: - **Before:** `main` at the start of this work (commit `02f2a78`, eleven districts). - **After:** this branch. It does three things: - pins of walled places now stand at their gates - the Palace is safe ground in the data
For: pearl, walk, towers, minutes, kunle, shorter, emeka, gates. Last changed 2026-10-14, 104 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14f.md` (0.52); `gidi:docs/living-test-2026-10-14i.md` (0.51); `gidi:docs/living-test-2026-10-14h.md` (0.5).

### `gidi:docs/living-test-2026-10-14h.md`
**City living test, 14 Oct 2026 (eighth run): the Heights v2**. City living test, 14 Oct 2026 (eighth run): the Heights v2: There are two states: - **Before:** `main` at commit `47b75ef` (the Heights v1). - **After:** this branch.
For: beach, bisi, minutes, sunday, pearl, kunle, island, drive. Last changed 2026-10-14, 57 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14i.md` (0.51); `gidi:docs/living-test-2026-10-14g.md` (0.5); `gidi:docs/living-test-2026-10-14j.md` (0.39).

### `gidi:docs/living-test-2026-10-14i.md`
**City living test, 14 Oct 2026 (ninth run): the Heights v3**. City living test, 14 Oct 2026 (ninth run): the Heights v3: There are two states: - **Before:** `main` at commit `a679778` (the Heights v2). - **After:** this branch: the golf course, bigger Ikoyi houses in five architectural styles, and a floating street tied in.
For: pearl, club, golf, minutes, walk, kunle, towers, course. Last changed 2026-10-14, 42 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14g.md` (0.51); `gidi:docs/living-test-2026-10-14h.md` (0.51); `gidi:docs/living-test-2026-10-14j.md` (0.39).

### `gidi:docs/living-test-2026-10-14j.md`
**City living test, 14 Oct 2026 (tenth run): thirteen districts, with the new Frontier**. City living test, 14 Oct 2026 (tenth run): thirteen districts, with the new Frontier: There are two states: - **Before:** `main` at commit `10b9708` (twelve districts). - **After:** this branch: the Frontier, and the Heights rebuilt once with `keep_gateways`.
For: frontier, femi, toll, plaza, ride, walk, pearl, refinery. Last changed 2026-10-14, 66 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14g.md` (0.46); `gidi:docs/audit/frontier.md` (0.43); `gidi:docs/CITY-LIVING-TEST.md` (0.41).

### `gidi:docs/living-test-2026-10-14k.md`
**City living test, 15 Oct 2026 (eleventh run): Old Shore**. City living test, 15 Oct 2026 (eleventh run): Old Shore: There are two states: - **Before:** `main` at commit `cf613f8` (thirteen districts). - **After:** this branch: Old Shore, built in parallel with the Border.
For: shore, sade, fish, hunter, minutes, tools, thirteen, roundabout. Last changed 2026-10-15, 52 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/oldshore-pattern-study.md` (0.49); `gidi:docs/living-test-2026-10-15m.md` (0.43); `gidi:docs/CITY-LIVING-TEST.md` (0.32).

### `gidi:docs/living-test-2026-10-14l.md`
**City living test, 15 Oct 2026: the Border**. City living test, 15 Oct 2026: the Border: There are two states: - **Before:** `main` at commit `cf613f8` (thirteen districts). - **After:** this branch: the Border, and Railside rebuilt once with `keep_gateways`.
For: dayo, funmi, coconut, emeka, railside, border, checkpoint, rode. Last changed 2026-10-15, 64 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14d.md` (0.33); `gidi:docs/living-test-2026-10-14g.md` (0.3); `gidi:docs/CITY-LIVING-TEST.md` (0.3).

### `gidi:docs/living-test-2026-10-15-gutters.md`
**City living test, 15 Oct 2026: open gutters (ism 15, group 1)**. City living test, 15 Oct 2026: open gutters (ism 15, group 1): `scripts/isms.py` now puts open gutters into the city data, with plank and slab crossings at doors and side streets. Two Haiku residents walked the numbers through `scripts/explore_city.py`, whose `look` and `home` now also report gutters.
For: gutter, gutters, blocked, slabs, plank, adeleke, door, fifteen. Last changed 2026-10-15, 31 lines.
Links to 5: `gidi:docs/img/gutters-estate.png`, `gidi:docs/img/gutters-maze.png`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/isms.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/ISMS-BUILD.md` (0.34); `gidi:docs/living-test-2026-10-13.md` (0.15); `gidi:docs/pilot-foodgate.md` (0.13).

### `gidi:docs/living-test-2026-10-15n.md`
**City living test, 15 Oct 2026: road clean-up, pass 1**. City living test, 15 Oct 2026: road clean-up, pass 1: The first of four road passes. `scripts/roadclean.py` now runs inside the bake, after every road is gathered and before the civic layer. It fixes what the 3D audit (`scripts/audit3d.py`) finds, by fixed rules. No building moves, and no road is run through a building.
For: lesser, pass, changed, fifteen, mains, loses, tidying, straightened. Last changed 2026-10-15, 38 lines.
Links to 4: `gidi:docs/img/roads-clean.png`, `gidi:scripts/audit3d.py`, `gidi:scripts/check_district.py`, `gidi:scripts/roadclean.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/junctions.md` (0.23); `gidi:docs/road-heights.md` (0.17); `gidi:docs/living-test-2026-10-15m.md` (0.13).

### `gidi:docs/studies/airport.md`
**The Airport: the deep study**. The Airport: the deep study: Inspired by Murtala Muhammed International Airport, Ikeja. Study area: 15.81 km², 15.81 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: airport, median, touching, storeys, transit, service, tenth, restaurant. Last changed 2026-10-15, 126 lines.
Links to 2: `gidi:docs/img/study-airport.png`, `gidi:scripts/study_deep.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/studies/estate.md` (0.8); `gidi:docs/studies/heights.md` (0.77); `gidi:docs/studies/hub.md` (0.77).

## Near-orphans

### `gidi:docs/bazaar-pattern-study.md`
**The Bazaar pattern study: Ojo round the electronics market → The Bazaar (v1)**. The Bazaar pattern study: Ojo round the electronics market → The Bazaar (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: bazaar, expressway, electronics, fair, wholesale, median, avenue, plazas. Last changed 2026-10-14, 125 lines.
Links to 12: `gidi:data/results/lga_table.json`, `gidi:docs/img/bazaar-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:web/gen-bazaar.json`, `gidi:web/network.json`
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.38); `gidi:docs/railside-pattern-study.md` (0.37); `gidi:docs/jungle-pattern-study.md` (0.36).

### `gidi:docs/border-pattern-study.md`
**Border pattern study: Badagry → the Border (v1)**. Border pattern study: Badagry → the Border (v1): Status: generated for review (15 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: badagry, border, bush, expressway, estimated, sprawl, post, worldcover. Last changed 2026-10-15, 137 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/border-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_boxheights.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/bazaar-pattern-study.md` (0.29); `gidi:docs/living-test-2026-10-14l.md` (0.28); `gidi:docs/capital-pattern-study.md` (0.27).

### `gidi:docs/estate-pattern-study.md`
**Estate pattern study: Ikeja GRA, Magodo and Omole → the Estate (v1)**. Estate pattern study: Ikeja GRA, Magodo and Omole → the Estate (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: estates, ikeja, gates, gra's, kosofe, estate's, omole's, typical. Last changed 2026-10-14, 141 lines.
Links to 15: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/estate-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py`, `gidi:scripts/study_landmarks.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.36); `gidi:docs/railside-pattern-study.md` (0.34); `gidi:docs/oldisland-pattern-study.md` (0.31).

### `gidi:docs/foodgate-pattern-study.md`
**Food Gate pattern study: Ojota–Ketu–Mile 12 (Kosofe) → Food Gate (v1)**. Food Gate pattern study: Ojota–Ketu–Mile 12 (Kosofe) → Food Gate (v1): Status: generated for review (13 Oct 2026). Same method as the other districts: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: kosofe, northern, mile, adeleke, maze's, ketu, median, corridor. Last changed 2026-10-14, 172 lines.
Links to 12: `gidi:data/results/lga_table.json`, `gidi:docs/img/foodgate-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:web/gen-foodgate.json`, `gidi:web/network.json`
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.38); `gidi:docs/jungle-pattern-study.md` (0.37); `gidi:docs/capital-pattern-study.md` (0.34).

### `gidi:docs/frontier-pattern-study.md`
**Frontier pattern study: the Lekki peninsula → the Frontier (v1)**. Frontier pattern study: the Lekki peninsula → the Frontier (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: frontier, peninsula, cells, awoyaya, empty, tracts, lekki, ajah. Last changed 2026-10-14, 177 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/frontier-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_boxheights.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/heights-pattern-study.md` (0.32); `gidi:docs/audit/frontier.md` (0.3); `gidi:docs/living-test-2026-10-14j.md` (0.29).

### `gidi:docs/heights-pattern-study.md`
**Heights pattern study: Ikoyi, Victoria Island and Banana Island → the Heights (v3)**. Heights pattern study: Ikoyi, Victoria Island and Banana Island → the Heights (v3): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: ikoyi, boxes, island, hipped, course, victoria, golf, booths. Last changed 2026-10-14, 208 lines.
Links to 17: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/heights-vs-real.png`, `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_boxheights.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/oldisland-pattern-study.md` (0.35); `gidi:docs/living-test-2026-10-14h.md` (0.35); `gidi:docs/frontier-pattern-study.md` (0.32).

### `gidi:docs/hub-pattern-study.md`
**Hub pattern study: Oshodi/Isolo + Surulere → The Hub (v1)**. Hub pattern study: Oshodi/Isolo + Surulere → The Hub (v1): Status: generated for review (13 Oct 2026). Same method as the Maze: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.** Data: OpenStreetMap (ODbL), Lagos extract, plus building heights from Google Open Buildings 2.5D (via `data/results/lga_table.json`). Area studied: Oshodi/Isolo + Surulere LGAs, 64.6 km² by the OpenStreetMap boundaries. The height and people table uses the government land areas, which add up to 75.9 km²; the shares are not affected.
For: slip, knot, stadium, maze, northern, terminal, percentile, station. Last changed 2026-10-13, 278 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/img/hub-station-skywalk.png`, `gidi:docs/img/hub-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/draw_gen.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/landmarks.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.43); `gidi:docs/jungle-pattern-study.md` (0.34); `gidi:docs/foodgate-pattern-study.md` (0.33).

### `gidi:docs/junctions.md`
**Junctions (pass 3 of the road work)**. Junctions (pass 3 of the road work): Status: built 15 Oct 2026. `scripts/junctions.py` runs inside the bake, after the road clean-up and before the road heights.
For: roundabouts, ring, wahab, radius, roundabout, ajasa, give-way, oladipo. Last changed 2026-10-15, 70 lines.
Links to 3: `gidi:docs/img/roundabouts.png`, `gidi:scripts/check_district.py`, `gidi:scripts/junctions.py`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-15n.md` (0.23); `gidi:docs/hub-pattern-study.md` (0.19); `gidi:docs/railside-pattern-study.md` (0.14).

### `gidi:docs/jungle-pattern-study.md`
**Jungle City pattern study: Ajegunle (+ Festac) → Jungle City (v1)**. Jungle City pattern study: Ajegunle (+ Festac) → Jungle City (v1): Status: generated for review (13 Oct 2026). Same method as the Maze and the Hub: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: jungle, flats, median, ajegunle, expressway, adeleke, maze's, festac. Last changed 2026-10-14, 246 lines.
Links to 13: `gidi:data/results/lga_table.json`, `gidi:docs/img/jungle-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/draw_gen.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:web/gen-jungle.json` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.49); `gidi:docs/foodgate-pattern-study.md` (0.37); `gidi:docs/bazaar-pattern-study.md` (0.36).

### `gidi:docs/living-test-2026-10-15m.md`
**City living test, 15 Oct 2026 (twelfth run): all fifteen districts**. City living test, 15 Oct 2026 (twelfth run): all fifteen districts: Old Shore and the Border were built in parallel, on separate branches (living tests 14k and 14l). The Border was merged first. This run checks the city once both are combined: main at `a94e9ee` (the Border and the 3D kit) plus Old Shore.
For: combined, shore, shore's, fifteen, walk, hunter, trips, palace. Last changed ?, 30 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14k.md` (0.43); `gidi:docs/oldshore-pattern-study.md` (0.36); `gidi:docs/CITY-LIVING-TEST.md` (0.24).

### `gidi:docs/oldisland-pattern-study.md`
**Old Island pattern study: Lagos Island → Old Island (v1)**. Old Island pattern study: Lagos Island → Old Island (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: island, island's, core's, fountains, bridge's, waterfront, x-junctions, core. Last changed 2026-10-14, 143 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/oldisland-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/heights-pattern-study.md` (0.35); `gidi:docs/oldshore-pattern-study.md` (0.33); `gidi:docs/estate-pattern-study.md` (0.31).

### `gidi:docs/oldshore-pattern-study.md`
**Old Shore pattern study: old Ikorodu → Old Shore (v1)**. Old Shore pattern study: old Ikorodu → Old Shore (v1): Status: generated for review (15 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: shore, jetty, ikorodu's, ikorodu, pins, ferry, fish, town. Last changed 2026-10-15, 145 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/oldshore-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_boxheights.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14k.md` (0.49); `gidi:docs/living-test-2026-10-15m.md` (0.36); `gidi:docs/oldisland-pattern-study.md` (0.33).

### `gidi:docs/port-pattern-study.md`
**The Port pattern study: Apapa → The Port (v1)**. The Port pattern study: Apapa → The Port (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: port, apapa, quay, yard, yards, container, farm, reserve. Last changed 2026-10-14, 128 lines.
Links to 12: `gidi:data/results/lga_table.json`, `gidi:docs/img/port-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:web/gen-port.json`, `gidi:web/network.json`
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/bazaar-pattern-study.md` (0.33); `gidi:docs/living-test-2026-10-14c.md` (0.31); `gidi:docs/watertown-pattern-study.md` (0.28).

### `gidi:docs/railside-pattern-study.md`
**Railside pattern study: Agege, Ifako/Ijaye and Alimosho → Railside (v1)**. Railside pattern study: Agege, Ifako/Ijaye and Alimosho → Railside (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: lgas, railside, capital's, landmarks, median, pipeline, sprawl, mounds. Last changed 2026-10-14, 125 lines.
Links to 14: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/railside-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py`, `gidi:scripts/study_landmarks.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.41); `gidi:docs/bazaar-pattern-study.md` (0.37); `gidi:docs/estate-pattern-study.md` (0.34).

### `gidi:docs/terrain.md`
**Gidi terrain (v1, for review)**. Gidi terrain (v1, for review): The ground under the whole map, `web/terrain.json`: a 40 m grid in decimetres, made by `scripts/terrain.py`. The review picture is made by `scripts/draw_terrain.py`.
For: smoothing, ridges, ridge, valleys, area's, raises, features, edits. Last changed 2026-10-15, 55 lines.
Links to 5: `gidi:docs/img/terrain.png`, `gidi:scripts/draw_terrain.py`, `gidi:scripts/terrain.py`, `gidi:web/terrain-edits.json`, `gidi:web/terrain.json`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:docs/LAGOS-ISMS.md` (0.15); `gidi:docs/oldshore-pattern-study.md` (0.14); `gidi:docs/data/deep-check/SUMMARY.md` (0.13).

### `gidi:docs/watertown-pattern-study.md`
**Water Town pattern study: the Makoko–Iwaya and Bariga waterfront → Water Town (v1)**. Water Town pattern study: the Makoko–Iwaya and Bariga waterfront → Water Town (v1): Status: generated for review (13 Oct 2026; v2 the same day: the land is rebuilt as fingers running down to the shore). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets, houses and stilt houses from the rules. **No real street, building or name is copied into Gidi.**
For: fingers, stilt, huts, sawmill's, canoe, village, land, boardwalks. Last changed 2026-10-14, 164 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/img/watertown-fingers.png`, `gidi:docs/img/watertown-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:study-mainland-shomolu-landmarks.json` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/port-pattern-study.md` (0.28); `gidi:docs/living-test-2026-10-13c.md` (0.26); `gidi:docs/maze-pattern-study.md` (0.25).

## Every document, by folder

## (top)
### `gidi-data:README.md`
**gidi-data: Gidi's study store**. gidi-data: Gidi's study store: What Gidi studies Lagos from: open datasets, the Google study shots, reference pictures, the kit tests, textures and people assets. It lived inside World Drive's folder (`~/Real-world`) until 24 Oct 2026; the owner moved it out ("take out the Gidi stuff from real world").
For: datasets, shots, reference, scripts, assets, notes, folder, deep-study. Last changed 2026-10-24, 23 lines.
Links to 4: `gidi-data:research/data/pull-data.sh`, `gidi-data:research/refs/REVIEW.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/DATA-SOURCES.md`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:decisions/CODEBASE.md` (0.27); `gidi:decisions/NOW.md` (0.14); `gidi:decisions/DECISIONS.md` (0.13).

## gidi-data:research/google/estate
### `gidi-data:research/google/estate/NOTES.md`
**The Estate: Magodo, Omole, Ikeja GRA (study, 18 Oct 2026). Study only; nothing copied.**. The Estate: Magodo, Omole, Ikeja GRA (study, 18 Oct 2026). Study only; nothing copied.: - Planned: long parallel streets bending with the land, blocks ~60 m wide (two rows of plots back to back) x 200-300 m. - A main drive cuts across; closes end at the estate's edge (the green valley); a clear edge between estate and bush. - Plots in even rows, houses set back with compound walls; roofs: terracotta, grey, some blue.
For: rows, valley, unplanned, parallel, planned, drive, closes, omole. Last changed 2026-10-24, 26 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi:docs/estate-pattern-study.md` (0.15); `gidi-data:research/google/maze/NOTES.md` (0.13); `gidi:docs/lagos-study/STUDY.md` (0.12).

## gidi-data:research/google/ibudo
### `gidi-data:research/google/ibudo/NOTES.md`
**Ìbùdó study: Oshodi (19 Oct 2026). Study only: nothing here is copied into Gidi.**. Ìbùdó study: Oshodi (19 Oct 2026). Study only: nothing here is copied into Gidi.: Views (Google Maps / Street View, Jul 2021 and Apr 2024): 01 interchange from above (300 m): the expressway crossing, the Terminal 3 oval, the footbridge, the market west of it. 02 market and bridge from above (250 m): Oshodi Market's red roofs packed between Oshodi Rd and the rail; dense shops.
For: twin, steel, adekoya, oshodi, shop, poles, awnings, wires. Last changed 2026-10-24, 35 lines.
Links to 1: `gidi:docs/TWINS.md`
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi:docs/hand/ibudo/README.md` (0.28); `gidi:docs/hand/ibudo/child_plan.md` (0.25); `gidi-data:research/google/ibudo/study/INVENTORY.md` (0.23).

## gidi-data:research/google/ibudo/study
### `gidi-data:research/google/ibudo/study/INVENTORY.md`
**Ìbùdó study, phase 1: Oshodi and Ojuelegba inventory (19 Oct 2026)**. Ìbùdó study, phase 1: Oshodi and Ojuelegba inventory (19 Oct 2026): Study only, from Google Maps satellite with labels and Street View. Nothing here is traced or copied into Gidi; it describes how the two real places are built and how they work, so Ìbùdó's streets and places can be invented from them.
For: cres, oshodi, ojuelegba, yaba, arena, ilupeju, railway, army. Last changed 2026-10-24, 280 lines.
Links to 0: 
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi:scripts/inventory.py`).
Nearest in words: `gidi:docs/hand/ibudo/child_plan.md` (0.55); `gidi-data:research/google/ibudo/NOTES.md` (0.23); `gidi:docs/lagos-study/STUDY.md` (0.2).

## gidi-data:research/google/kits/old-town
### `gidi-data:research/google/kits/old-town/KIT.md`
**Dense old town kit**. Dense old town kit: This is the kit list for the dense old towns of Lagos, ready for the owner to check. It is built only from the Street View shots in this folder. Their notes are in `shots.tsv`. A number like ot42 means shot `ot42_*.jpg`.
For: eyes, shots, desk, steel, sheet, timber, plank, example. Last changed 2026-10-24, 682 lines.
Links to 7: `gidi-data:research/google/kits/old-town/tests/facade_hand.py`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/kit_draft.py`, `gidi:legacy/blender/kit_test.py`
Backlinks: 8 documents (`gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md`, `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md`, `gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md`, `gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`), 13 code files (`gidi-data:research/google/kits/old-town/tests/ot13/mk13_first.py`, `gidi-data:research/google/kits/old-town/tests/ot149/mk149_first.py`, `gidi-data:research/google/kits/old-town/tests/ot45/mk45_first.py`, `gidi-data:research/google/kits/old-town/tests/ot73/mk73_first.py`, `gidi:legacy/blender/gidi_kit/core.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.22); `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.2); `gidi:decisions/NOW.md` (0.19).

## gidi-data:research/google/kits/old-town/tests/ot149
### `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md`
**Kit eye test 3: ot149, Mushin, Ayantuga St (Street View, Jul 2021, heading 180)**. Kit eye test 3: ot149, Mushin, Ayantuga St (Street View, Jul 2021, heading 180): The test: do the kit's parts hold on a third street they were not made for? The owner's eye judges. This is not a pass.
For: photo, turned, apron, photo's, render, cage, camera, toned. Last changed 2026-10-24, 79 lines.
Links to 6: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/ot149/hand149.py`, `gidi-data:research/google/kits/old-town/tests/ot149/mk149_first.py`, `gidi-data:research/google/kits/old-town/tests/ot149/mk149_pass.py`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`, `gidi:legacy/blender/kit_draft.py`
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.36); `gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md` (0.32); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.32).

## gidi-data:research/google/kits/old-town/tests/ot175
### `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md`
**Kit eye test 1: ot175, Ilasamaja/Mushin, Olayiwola Liasu St (Jul 2021)**. Kit eye test 1: ot175, Ilasamaja/Mushin, Olayiwola Liasu St (Jul 2021): `side_by_side.jpg` shows the Street View on the left and the rebuild on the right, both 1200x670. It is now pass 3 (ground, sun, clutter, grime), also saved as `sbs_p3_final.jpg`. The earlier passes, in order: `sbs_v1.jpg`-`sbs_v3.jpg` (untextured), `sbs_tex1_first.jpg` and `sbs_tex2.jpg` (textured), `sbs_p3_first.jpg` (pass 3's first try). `map_pass2.json` is the map as it stood before pass 3.
For: reused, camera, darker, colour, sacks, pass, ruts, dark. Last changed 2026-10-24, 234 lines.
Links to 9: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/facade_hand.py`, `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/roadbed.py`, `gidi:legacy/blender/gidi_kit/textured.py`, `gidi:legacy/blender/kit_draft.py`, `gidi:legacy/blender/kit_test.py`
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.35); `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md` (0.32); `gidi:decisions/NOW.md` (0.27).

## gidi-data:research/google/kits/old-town/tests/ot45
### `gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md`
**Kit eye test 5: ot45, Mushin, Ladipo St (Street View, Jul 2021, heading 180)**. Kit eye test 5: ot45, Mushin, Ladipo St (Street View, Jul 2021, heading 180): The test: do the kit's parts hold on a fifth street they were not made for? The owner's eye judges. This is not a pass.
For: photo's, tractor, rubbish, bonneted, desk, dirt, flatbed, median. Last changed 2026-10-24, 137 lines.
Links to 13: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`, `gidi-data:research/google/kits/old-town/tests/ot45/closeups45.sh`, `gidi-data:research/google/kits/old-town/tests/ot45/hand45.py`, `gidi-data:research/google/kits/old-town/tests/ot45/hand45_2.py`, `gidi-data:research/google/kits/old-town/tests/ot45/mk45_first.py`, `gidi-data:research/google/kits/old-town/tests/ot45/mk45_pass.py`, `gidi-data:research/google/kits/old-town/tests/ot45/run45.sh`, `gidi-data:research/google/kits/old-town/tests/ot45/sbs.py`, `gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:legacy/blender/kit_draft.py` ...
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md` (0.28); `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md` (0.27); `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.27).

## gidi-data:research/google/kits/old-town/tests/ot73
### `gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`
**Kit eye test 4: ot73, Epe, Ogunmule Akinlogba St (Street View, May 2024, heading 180)**. Kit eye test 4: ot73, Epe, Ogunmule Akinlogba St (Street View, May 2024, heading 180): The test: do the kit's parts hold on a fourth street they were not made for? The owner's eye judges. This is not a pass.
For: photo's, drafted, kerbs, grass, balls, fence, lean, smooth. Last changed 2026-10-24, 76 lines.
Links to 8: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/ot149/closeups149.sh`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`, `gidi-data:research/google/kits/old-town/tests/ot73/hand73.py`, `gidi-data:research/google/kits/old-town/tests/ot73/mk73_first.py`, `gidi-data:research/google/kits/old-town/tests/ot73/mk73_pass.py`, `gidi:legacy/blender/city_run.py`, `gidi:legacy/blender/kit_draft.py`
Backlinks: 1 documents (`gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md` (0.32); `gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md` (0.28); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.21).

## gidi-data:research/google/kits/old-town/tests/ot91
### `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md`
**Kit eye test 2: ot91, Isale Eko, Balogun area (Street View, date n/a, heading 0)**. Kit eye test 2: ot91, Isale Eko, Balogun area (Street View, date n/a, heading 0): The test: do the parts built for ot175 hold on a street they were not made for? The owner's eye judges. This is not a pass.
For: jitter, stored, positions, records, goods, scaffold, render, seeded. Last changed 2026-10-24, 168 lines.
Links to 4: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/facade_hand.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/kit_draft.py`
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md` (0.36); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.35); `gidi:docs/MAP-FORMAT.md` (0.31).

## gidi-data:research/google/kits/old-town/tests/ut01_emmanuel
### `gidi-data:research/google/kits/old-town/tests/ut01_emmanuel/inventory.md`
**Ultimate test 1: Shomolu, Emmanuel St junction (Street View, Jul 2021), three angles**. Ultimate test 1: Shomolu, Emmanuel St junction (Street View, Jul 2021), three angles: The owner's ultimate test (DECISIONS, 23 Oct): list every thing in the real pictures, model each one clean to a standard look (whole, from every side, wear as a layer), rebuild the picture from those things alone, then rebuild the other angles.
For: angles, gidi-game, emmanuel, bench, crates, timber, pallet, cart. Last changed 2026-10-24, 102 lines.
Links to 8: `gidi-game:tools/block_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/pickup_build.py`, `gidi-game:tools/pole_build.py`, `gidi-game:tools/stall_build.py`, `gidi-game:tools/umbrella_build.py`, `gidi-game:tools/wall_build.py`
Backlinks: 2 documents (`gidi:decisions/CHECKS.md`, `gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:decisions/NOW.md` (0.3); `gidi-game:docs/ASSET-INVENTORY.md` (0.29); `gidi:docs/look/research-housing.md` (0.24).

## gidi-data:research/google/maze
### `gidi-data:research/google/maze/NOTES.md`
**The Maze: Mushin + Shomolu (study, 18 Oct 2026). Screenshots are for study only; nothing here is copied into Gidi.**. The Maze: Mushin + Shomolu (study, 18 Oct 2026). Screenshots are for study only; nothing here is copied into Gidi.: - Coverage: Mushin 75-85% roof, Shomolu ~85%. Almost no open ground; sand only in small yards. - Grain: long terraced one- and two-storey houses (~10 m deep, 15-30 m long), in rows along the streets; block interiors filled with more rows reached by 1-3 m alleys. Blocks ~60 x 150 m.
For: shomolu, mushin, terraced, hierarchy, alleys, curving, interiors, queued. Last changed 2026-10-24, 15 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.23); `gidi:docs/look/research-buildings.md` (0.13); `gidi-data:research/google/estate/NOTES.md` (0.13).

## gidi-data:research/google/twins
### `gidi-data:research/google/twins/NOTES.md`
**(no title)**. Twins outside Ìbùdó (Street View, 19 Oct): ikorodu_kokoro_abu_st_sprawl_stalls (Feb 2017): a sprawl street, tar with sandy edges, a long row of zinc-roofed stalls on timber posts selling bags and plastics, an open drain with tyres, bungalows, palms, okadas. Twin: sprawl street, shed row, open gutter.
For: sprawl, kokoro, zinc-roofed, twins, plastics, selling, stalls, sandy. Last changed 2026-10-24, 3 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi-data:research/google/ibudo/NOTES.md` (0.17); `gidi:docs/border-pattern-study.md` (0.11); `gidi:docs/look/research-commerce.md` (0.1).

## gidi-data:research/google/video1-street
### `gidi-data:research/google/video1-street/NOTES.md`
**Video 1 street: reference notes (22 Oct 2026)**. Video 1 street: reference notes (22 Oct 2026): Video 1 (`../../refs/video1/`) is an AI-made "Lagos game" clip. It shows a third-person view under a flyover, a levy quest, danfos, a crowd and stalls, and wet broken ground with litter. These notes say what the real places look like, so the test street is built from Lagos and not from the clip.
For: deck, kerb, piers, palisade, obalende, shade, ojuelegba, buses. Last changed 2026-10-24, 51 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 3 code files (`gidi-game:tools/underdeck_build.py`, `gidi:scripts/design_density.py`, `gidi:scripts/district_profiles.py`).
Nearest in words: `gidi:docs/look/research-transport.md` (0.25); `gidi:docs/road-heights.md` (0.22); `gidi:docs/look/research-street.md` (0.2).

## gidi-data:research/refs
### `gidi-data:research/refs/REVIEW.md`
**Reference review (Claude, 15 Oct 2026): for the owner to correct and tag**. Reference review (Claude, 15 Oct 2026): for the owner to correct and tag: Numbers match the contact sheets (sorted by file name). **Not Lagos** means not Lagos, Nigeria, in my view. Commons matched the Spanish and Portuguese word *lago* ("lake") and the town of Lagos in Portugal. Nothing is deleted yet: confirm and I'll remove them.
For: umbrellas, portugal, assets, tomato, yaba, question, oshodi, green-black. Last changed 2026-10-24, 126 lines.
Links to 0: 
Backlinks: 3 documents (`gidi-data:README.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/hand/maze-hub-lagos.md`), 0 code files ().
Nearest in words: `gidi-data:research/google/ibudo/NOTES.md` (0.2); `gidi-data:research/google/ibudo/study/INVENTORY.md` (0.17); `gidi:docs/look/research-commerce.md` (0.17).

## gidi-data:textures
### `gidi-data:textures/README.md`
**Gidi textures (outside the repo)**. Gidi textures (outside the repo): Downloaded 22 Oct 2026 with the owner's OK. Poly Haven, CC0 (free for any use, including a sold game). 2K maps per surface: diffuse, nor_gl (OpenGL normal: Blender; flip green for Unreal or use Unreal's flip option), rough, displacement, ao where offered.
For: plaster, flip, iron, asphalt, damaged, rough, painted, metal. Last changed 2026-10-24, 9 lines.
Links to 0: 
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.25); `gidi:docs/look/research-buildings.md` (0.16); `gidi:docs/look/research-housing.md` (0.13).

## (top)
### `gidi-game:ASSETS.md`
**Hand-made assets**. Hand-made assets: | Asset | Where | Source | Status | |---|---|---|---| | Danfo Basic 2.0 (font): the owner's danfo lettering (BirdFont, July 2022), spaced, kerned and given punctuation by script (tools/font_space.py, font_punct.py) | Art/Fonts/DanfoBasic.ttf (built by tools/font_build.sh from Art/Fonts/src: the 2022 letters and Alfa Slab One) | the owner, built on Alfa Slab One (JM Solé), SIL Open Font License 1.1 (Art/Fonts/OFL.txt) | to use: danfo bodywork, signboards, the game's titles |
For: font, content, claude, makehuman, danfo, plate, gidiplate, axles. Last changed 2026-10-24, 34 lines.
Links to 31: `gidi-game:Art/People/hawker/hawker.blend`, `gidi-game:Art/People/hawker/spec.json`, `gidi-game:Art/Plates/plates.json`, `gidi-game:Art/Vehicles/BrtBuilt/brt_parts.blend`, `gidi-game:Art/Vehicles/BrtBuilt/brt_red_parts.blend`, `gidi-game:Art/Vehicles/BrtBuilt/red.json`, `gidi-game:Art/Vehicles/Danfo/danfo.blend`, `gidi-game:Art/Vehicles/KekeBuilt/keke_parts.blend`, `gidi-game:Art/Vehicles/MolueBuilt/molue_parts.blend`, `gidi-game:Art/Vehicles/Okada/okada.blend`, `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_plates.py` ...
Backlinks: 5 documents (`gidi-game:CLAUDE.md`, `gidi-game:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`), 2 code files (`gidi-game:.gitignore`, `gidi-game:Content/Python/gidi_underdeck.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.25); `gidi-game:docs/ASSET-INVENTORY.md` (0.23); `gidi:decisions/IDEAS.md` (0.18).

### `gidi-game:CLAUDE.md`
**Gidi game (Unreal)**. Gidi game (Unreal): Read the map repo's `decisions/` first (`~/gidi/decisions/NOW.md`, `DECISIONS.md`): the same rules apply here.
For: push, repo's, commit, generates, commands, unreal, paragraph, proof. Last changed 2026-10-24, 13 lines.
Links to 4: `gidi-game:.claude/settings.json`, `gidi-game:ASSETS.md`, `gidi-game:tools/kit_fields.py`, `gidi:decisions/DECISIONS.md`
Backlinks: 2 documents (`gidi:README.md`, `gidi:decisions/CODEBASE.md`), 23 code files (`gidi:.claude/hooks/checked-before-commit.sh`, `gidi:.claude/hooks/checks-before-commit.sh`, `gidi:.claude/hooks/checks-before-stop.sh`, `gidi:.claude/hooks/repo.sh`, `gidi:.claude/hooks/review-before-push.sh`).
Nearest in words: `gidi:CLAUDE.md` (0.41); `gidi:docs/UNREAL-PORT-PLAN.md` (0.19); `gidi-game:README.md` (0.17).

### `gidi-game:README.md`
**Gidi: the game**. Gidi: the game: The Unreal Engine 5.8 project for Gidi. The city itself lives in the map repo, [NewDara-Star/gidi](https://github.com/NewDara-Star/gidi): its data and the kit's tiles.
For: editor, import, repo, meshy, wasd, scripting, tiles, console. Last changed 2026-10-24, 56 lines.
Links to 15: `gidi-game:.mcp.json`, `gidi-game:ASSETS.md`, `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_underdeck.py`, `gidi-game:docs/PERFORMANCE.md`, `gidi-game:tools/editor.sh`, `gidi-game:tools/import.sh`, `gidi-game:tools/measure.sh`, `gidi-game:tools/mode.sh`, `gidi-game:tools/play.sh`, `gidi-game:tools/shot.sh` ...
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi-game:docs/PERFORMANCE.md` (0.33); `gidi:decisions/NOW.md` (0.26); `gidi:docs/UNREAL-PORT-PLAN.md` (0.23).

## gidi-game:docs
### `gidi-game:docs/ASSET-INVENTORY.md`
**What's already in the project (check here before building anything)**. What's already in the project (check here before building anything): The owner's rule (19 Oct): look at what we have before building from scratch. Gidi's own things (danfo, keke, molue, BRT, plates, brand, labels) are built by us; everything else starts from these. Paths are under `Content/`.
For: recipes, tools, manny, asphalt, concrete, build, animations, map's. Last changed 2026-10-23, 21 lines.
Links to 9: `gidi-game:tools/block_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/pickup_build.py`, `gidi-game:tools/pole_build.py`, `gidi-game:tools/stall_build.py`, `gidi-game:tools/umbrella_build.py`, `gidi-game:tools/wall_build.py`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 2 code files (`gidi-game:.gitignore`, `gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ut01_emmanuel/inventory.md` (0.29); `gidi-game:ASSETS.md` (0.23); `gidi:decisions/NOW.md` (0.21).

### `gidi-game:docs/PERFORMANCE.md`
**Performance: modes, near detail, streaming, budgets**. Performance: modes, near detail, streaming, budgets: The owner's rule (gidi `decisions/DECISIONS.md`, 22 Oct, "Build light, look full"): build in a light mode, play in the mode the machine can carry, flip to full only to look and take pictures. Near things carry detail and far things are simple. What the camera can't see is not drawn. The world streams in pieces around the player. Every level has a budget,
For: tools, lumen, editor, mode, modes, play, scalability, saved. Last changed 2026-10-24, 112 lines.
Links to 12: `gidi-game:Config/DefaultDeviceProfiles.ini`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:Content/Python/gidi_stream.py`, `gidi-game:tools/editor.sh`, `gidi-game:tools/import.sh`, `gidi-game:tools/measure.sh`, `gidi-game:tools/measure_csv.py`, `gidi-game:tools/mode.sh`, `gidi-game:tools/mode_sg.py`, `gidi-game:tools/play.sh`, `gidi-game:tools/stream.sh`, `gidi:decisions/DECISIONS.md`
Backlinks: 3 documents (`gidi-game:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`), 8 code files (`gidi-game:Config/DefaultDeviceProfiles.ini`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:Content/Python/gidi_stream.py`, `gidi-game:tools/measure.sh`, `gidi-game:tools/measure_csv.py`).
Nearest in words: `gidi-game:README.md` (0.33); `gidi:decisions/NOW.md` (0.15); `gidi:decisions/DECISIONS.md` (0.13).

## (top)
### `gidi:CLAUDE.md`
**Gidi**. Gidi: An open-world city inspired by Lagos, built from data and by hand. The owner works across more than one Claude account.
For: commit, push, hook, account, frozen, loosen, session, checked. Last changed 2026-10-24, 18 lines.
Links to 6: `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:scripts/inventory.py`, `gidi:scripts/rebuild_areas.py`
Backlinks: 2 documents (`gidi:README.md`, `gidi:decisions/CODEBASE.md`), 23 code files (`gidi:.claude/hooks/checked-before-commit.sh`, `gidi:.claude/hooks/checks-before-commit.sh`, `gidi:.claude/hooks/checks-before-stop.sh`, `gidi:.claude/hooks/repo.sh`, `gidi:.claude/hooks/review-before-push.sh`).
Nearest in words: `gidi-game:CLAUDE.md` (0.41); `gidi:decisions/README.md` (0.33); `gidi:decisions/DECISIONS.md` (0.25).

### `gidi:README.md`
**Gidi**. Gidi: The city for an open-world game: Gidi is real Lagos miniaturised, 51 districts, each street and place drawn by hand from the real one. This repo is the map. It holds every road, block, building and thing the game puts there, as records in `map/`, plus the drawing board they are made on. The game itself (the builders and the Unreal project) is
For: repos, drawing, airbus, provided, glo, odbl, records, newdara-star. Last changed 2026-10-24, 32 lines.
Links to 9: `gidi:CLAUDE.md`, `gidi:decisions/CODEBASE.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:legacy/OLD-MAP.md`, `gidi:scripts/board_server.py`, `gidi:scripts/check_map.py`, `gidi:scripts/check_rules.py`, `gidi:scripts/inventory.py`, `gidi:web/board.html`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:decisions/CODEBASE.md` (0.28); `gidi:CLAUDE.md` (0.24); `gidi:decisions/NOW.md` (0.23).

## gidi:decisions
### `gidi:decisions/CHECKS.md`
**Which check holds each rule**. Which check holds each rule: Every rule in `DECISIONS.md` has a row here: the check that enforces it, or why none can. `scripts/check_rules.py` runs before every commit and push (`.claude/hooks/checks-before-commit.sh`): it fails when a rule has no row, and lists every rule marked **GAP** (a map rule nothing checks yet). So "are we covering all bases?" is
For: process, gidi-game, rule, review, owner's, re-draft, twin, fail. Last changed 2026-10-24, 101 lines.
Links to 18: `gidi-data:research/google/kits/old-town/tests/ut01_emmanuel/inventory.md`, `gidi-game:tools/fields.py`, `gidi-game:tools/kit_fields.py`, `gidi:.claude/hooks/checked-before-commit.sh`, `gidi:.claude/hooks/checks-before-commit.sh`, `gidi:.claude/hooks/checks-before-stop.sh`, `gidi:.claude/hooks/review-before-push.sh`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/DATA-SOURCES.md`, `gidi:schema/kit_reads.json`, `gidi:scripts/check_district.py` ...
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`), 3 code files (`gidi:.claude/hooks/repo.sh`, `gidi:.claude/hooks/review-before-push.sh`, `gidi:scripts/check_rules.py`).
Nearest in words: `gidi:decisions/DECISIONS.md` (0.45); `gidi:decisions/NOW.md` (0.4); `gidi:decisions/CODEBASE.md` (0.32).

### `gidi:decisions/CODEBASE.md`
**What the code holds: the three repos, one page**. What the code holds: the three repos, one page: Read this before building anything new, so new work starts from what exists. Every file, with what it says it is, when it last changed and who points to it, is in `docs/inventory/INVENTORY.md`. What looks dead or broken is in `docs/inventory/SUSPECTS.md`. Since 24 Oct also (owner: "use the compiler to know what every piece of code is connected
For: scripts, old-map, gidi-game, board, inventory, map's, board's, committed. Last changed 2026-10-24, 172 lines.
Links to 130: `gidi-game:ASSETS.md`, `gidi-game:Config/DefaultDeviceProfiles.ini`, `gidi-game:Content/Python/gidi_cam.py`, `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:Content/Python/gidi_paint.py`, `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_plates.py`, `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_signs.py` ...
Backlinks: 5 documents (`gidi:CLAUDE.md`, `gidi:README.md`, `gidi:decisions/CHECKS.md`, `gidi:decisions/README.md`, `gidi:legacy/OLD-MAP.md`), 2 code files (`gidi:.claude/hooks/checks-before-stop.sh`, `gidi:docs/lagos-study/similar/scripts/common.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.37); `gidi:decisions/CHECKS.md` (0.32); `gidi:decisions/DECISIONS.md` (0.29).

### `gidi:decisions/DECISIONS.md`
**Decisions (the owner's; newest first)**. Decisions (the owner's; newest first): - **The story: Tunde's** (15 Oct 2026). The owner's confirmed story points live in `decisions/story/acts-2-3-draft.md`: - oja is weed, carried as cargo - the boss's 360 debt and the company bike - "how did you not know how your bike got stolen?"
For: hand, we're, view, records, kits, build, laptop, owner's. Last changed 2026-10-24, 136 lines.
Links to 39: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-game:ASSETS.md`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/kit_fields.py`, `gidi-game:tools/person_build.py`, `gidi-game:tools/plates.py`, `gidi-game:tools/umbrella_build.py`, `gidi:decisions/CHECKS.md`, `gidi:decisions/story/acts-2-3-draft.md`, `gidi:docs/BOARD.md`, `gidi:docs/DATA-SOURCES.md`, `gidi:docs/DEEP-STUDY.md` ...
Backlinks: 13 documents (`gidi-data:README.md`, `gidi-game:CLAUDE.md`, `gidi-game:docs/PERFORMANCE.md`, `gidi:CLAUDE.md`, `gidi:decisions/CHECKS.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`, `gidi:decisions/README.md` ...), 3 code files (`gidi:.claude/hooks/review-before-push.sh`, `gidi:scripts/check_rules.py`, `gidi:scripts/rebuild_areas.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.52); `gidi:decisions/CHECKS.md` (0.45); `gidi:docs/MAP-FORMAT.md` (0.33).

### `gidi:decisions/IDEAS.md`
**Ideas (not decided; newest first)**. Ideas (not decided; newest first): - **Our own Lagos motion from video, and AI video** (owner, 23 Oct). Motion2MixamoRig (github.com/MaxLiu22/Motion2MixamoRig, code Apache-2.0, experimental): a video of one person, whole body in frame, becomes motion on a Mixamo character (.glb for Blender/Unreal); Blender add-on tested on Apple Silicon, slow but fine on CPU (3-15 min per 30 s clip). Fills the gap Mixamo's library leaves: Lagos-only moves (basin on the head, conductor hanging off the door, frying akara, bargaining, climbing on an okada), filmed by the owner or friends who agree, never strangers' clips. **Catch:** it needs SMPL-X, non-commercial by default (a commercial licence is a separate deal), and the GVHMR weights have their own licence: use it for study and prototypes (person spots), then licence it or redo final animations with a sale-cleared tool before shipping. To set up (needs the owner's OK): repo + Python packages; about 5 GB of weights on first run; the SMPL-X file (owner signs up on the SMPL-X site); a Mixamo FBX from the owner's Adobe account. Mixamo itself: free library, retarget onto City Sample/MetaHuman in Unreal; usable in a shipped game, raw files not shared.
For: motion, refs, video, metahuman, yoruba, talk, sound, danfo. Last changed 2026-10-24, 73 lines.
Links to 4: `gidi:decisions/lived-in.md`, `gidi:decisions/world-life.md`, `gidi:docs/lagos-study/LIVING.md`, `gidi:docs/lagos-study/roads/NAMES.md`
Backlinks: 4 documents (`gidi:CLAUDE.md`, `gidi:decisions/NOW.md`, `gidi:decisions/README.md`, `gidi:docs/lagos-study/roads/NAMES.md`), 0 code files ().
Nearest in words: `gidi:decisions/lived-in.md` (0.24); `gidi:decisions/NOW.md` (0.23); `gidi:decisions/DECISIONS.md` (0.22).

### `gidi:decisions/NOW.md`
**Where the work stands (update at the end of every session)**. Where the work stands (update at the end of every session): **HANDOVER, 22 Oct 2026 ~23:00 (owner switching Claude accounts). Start here.** State: the new map (real Lagos at 1:3, 51 districts) has its format, its board tools and its first district's roads; the old-town kit has had 4 random eye tests. Nothing is running. Serve the board from main: `cd ~/gidi && ~/.venvs/gidi/bin/python scripts/board_server.py --port 8779`, open `http://127.0.0.1:8779/web/board.html?frame=new` (port 8778 serves the old regen worktree: old code).
For: gidi-game, unreal, records, hand, sent, pass, dress, board. Last changed 2026-10-24, 272 lines.
Links to 101: `gidi-data:research/google/estate/NOTES.md`, `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`, `gidi-data:research/google/kits/old-town/tests/ut01_emmanuel/inventory.md`, `gidi-game:ASSETS.md`, `gidi-game:Art/People/hawker/spec.json`, `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_signs.py`, `gidi-game:Content/Python/gidi_surfaces.py`, `gidi-game:docs/PERFORMANCE.md`, `gidi-game:tools/block_build.py` ...
Backlinks: 4 documents (`gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md`, `gidi-game:CLAUDE.md`, `gidi:CLAUDE.md`, `gidi:decisions/README.md`), 2 code files (`gidi:.claude/hooks/review-before-push.sh`, `gidi:web/hand/hub.json`).
Nearest in words: `gidi:decisions/DECISIONS.md` (0.52); `gidi:docs/MAP-FORMAT.md` (0.45); `gidi:decisions/CHECKS.md` (0.4).

### `gidi:decisions/README.md`
**Decisions and ideas**. Decisions and ideas: The owner works across more than one Claude account. This folder is the shared memory: **read it first in every session**, and add to it whenever the owner decides something or a good idea comes up. Newest first within each file.
For: ideas, decided, instructions, session, update, whenever, keeping, repos. Last changed 2026-10-24, 9 lines.
Links to 4: `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:CLAUDE.md` (0.33); `gidi:README.md` (0.16); `gidi:decisions/DECISIONS.md` (0.1).

### `gidi:decisions/lived-in.md`
**The lived-in layer: what every GTA does, and Gidi's plan**. The lived-in layer: what every GTA does, and Gidi's plan: The owner asked on 24 Oct 2026 for research from public material on how GTA's worlds feel alive, across every game, and for a "lived-in layer" plan for Gidi. **A proposal, not decided.** It builds on `world-life.md` (rhythm, systems, moments, texture: *what* Gidi's life is) and the IDEAS entry "What makes Los Santos feel lived in" (23 Oct). This file is about *the machinery*: what records and rules make that life show up in the game.
For: grandtheftwiki, spots, moments, player, proposed, speech, mods, hour. Last changed 2026-10-24, 154 lines.
Links to 2: `gidi:decisions/world-life.md`, `gidi:docs/lagos-study/LIVING.md`
Backlinks: 4 documents (`gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:docs/lagos-study/LIVING.md`), 0 code files ().
Nearest in words: `gidi:decisions/IDEAS.md` (0.24); `gidi:decisions/world-life.md` (0.23); `gidi:decisions/DECISIONS.md` (0.17).

## gidi:decisions/story
### `gidi:decisions/story/README.md`
**The story of Gidi**. The story of Gidi: Tunde, an okada rider, in debt to the boss who runs the motor park. The city opens in three acts: Survive, Hustle, Empire (`docs/gidi-districts-v0.3.md`).
For: acts, paste, account, boss's, story, roadmap, prototyping, puts. Last changed 2026-10-15, 22 lines.
Links to 4: `gidi:decisions/story/act-1-draft.md`, `gidi:decisions/story/acts-2-3-draft.md`, `gidi:docs/CITY-LIVING-TEST.md`, `gidi:docs/gidi-districts-v0.3.md`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:decisions/story/acts-2-3-draft.md` (0.31); `gidi:decisions/story/act-1-draft.md` (0.29); `gidi:decisions/story/novels/README.md` (0.24).

### `gidi:decisions/story/act-1-draft.md`
**Gidi Act 1: draft (the owner's outline, 15 Oct 2026, with Claude's notes)**. Gidi Act 1: draft (the owner's outline, 15 Oct 2026, with Claude's notes): **Status:** a draft for the story pass, stage 3 of `gidi-roadmap.md` (not in this repo yet). The owner decides; the notes are suggestions. The flowchart, `gidi-act1-flow.mermaid`, isn't in this repo; the flow below is the same in words.
For: boss, fares, tunde, bike, alpha, boss's, debt, money. Last changed 2026-10-16, 109 lines.
Links to 0: 
Backlinks: 4 documents (`gidi:decisions/story/README.md`, `gidi:decisions/story/acts-2-3-draft.md`, `gidi:decisions/story/novels/1-the-ledger.md`, `gidi:docs/hand/maze-hub-lagos.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/acts-2-3-draft.md` (0.48); `gidi:decisions/story/novels/1-the-ledger.md` (0.37); `gidi:decisions/story/novels/README.md` (0.33).

### `gidi:decisions/story/acts-2-3-draft.md`
**Gidi Acts 2 and 3: working draft (updated 15 Oct 2026 after the owner's feedback)**. Gidi Acts 2 and 3: working draft (updated 15 Oct 2026 after the owner's feedback): Builds on `act-1-draft.md`. The owner didn't like the pacing of Claude's first Acts 2–3 path (one run per district, the fake-revenge scapegoat, the finale structure). Only what the owner confirmed or asked for is kept below; Claude's proposals are marked as such.
For: tunde, boss, boys, bike, claude's, debt, boss's, fight. Last changed 2026-10-15, 77 lines.
Links to 1: `gidi:decisions/story/act-1-draft.md`
Backlinks: 3 documents (`gidi:decisions/DECISIONS.md`, `gidi:decisions/story/README.md`, `gidi:decisions/story/novels/1-the-ledger.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/act-1-draft.md` (0.48); `gidi:decisions/story/novels/1-the-ledger.md` (0.42); `gidi:decisions/story/novels/README.md` (0.39).

## gidi:decisions/story/novels
### `gidi:decisions/story/novels/1-the-ledger.md`
**1. The Ledger**. 1. The Ledger: *Claude's draft, 15 Oct 2026. It builds on the owner's confirmed story (`../act-1-draft.md`, `../acts-2-3-draft.md`) and adds people.*
For: chairman, tunde, player, ledger, bike, alpha, tunde's, boys. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:decisions/story/act-1-draft.md`, `gidi:decisions/story/acts-2-3-draft.md`
Backlinks: 1 documents (`gidi:decisions/story/novels/README.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/novels/2-union.md` (0.48); `gidi:decisions/story/novels/3-the-phone.md` (0.45); `gidi:decisions/story/acts-2-3-draft.md` (0.42).

### `gidi:decisions/story/novels/2-union.md`
**2. Union**. 2. Union: *Claude's draft, 15 Oct 2026. It keeps the owner's Act 1 (the steal, the boss's rescue, the okada on hire purchase, the robbery), then gives the city its own clock: an election.*
For: election, envelopes, chairman, tunde, lorry's, wins, ledger, union. Last changed 2026-10-15, 75 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/story/novels/README.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/novels/1-the-ledger.md` (0.48); `gidi:decisions/story/novels/3-the-phone.md` (0.35); `gidi:decisions/story/acts-2-3-draft.md` (0.28).

### `gidi:decisions/story/novels/3-the-phone.md`
**3. The Phone**. 3. The Phone: *Claude's draft, 15 Oct 2026. It keeps the owner's Act 1 (the steal, the rescue, the okada on hire purchase), then turns the open world into a thriller: one object that keeps ringing.*
For: captain, phone, adaeze, garba, tunde, chairman, captain's, voice. Last changed 2026-10-15, 79 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/story/novels/README.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/novels/1-the-ledger.md` (0.45); `gidi:decisions/story/novels/2-union.md` (0.35); `gidi:decisions/story/acts-2-3-draft.md` (0.26).

### `gidi:decisions/story/novels/README.md`
**Three stories for Gidi (Claude's drafts, 15 Oct 2026, for the owner to pick from)**. Three stories for Gidi (Claude's drafts, 15 Oct 2026, for the owner to pick from): The owner asked for "two or three novels of the story" to read, pick from, and build their own. These are short stories, about 15 minutes' reading each, not full novels. Each one names the people who drive the plot and the side characters who give it colour, and it's told the way it would play in an open world.
For: story, debt, novels, drugs, stories, betting, task, force. Last changed 2026-10-15, 36 lines.
Links to 4: `gidi:decisions/story/novels/1-the-ledger.md`, `gidi:decisions/story/novels/2-union.md`, `gidi:decisions/story/novels/3-the-phone.md`, `gidi:docs/LAYOUT-V2.md`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:decisions/story/acts-2-3-draft.md` (0.39); `gidi:decisions/story/act-1-draft.md` (0.33); `gidi:decisions/story/README.md` (0.24).

## gidi:decisions
### `gidi:decisions/world-life.md`
**Life in Gidi: what makes the world feel like it exists**. Life in Gidi: what makes the world feel like it exists: The owner's thinking from 16 Oct 2026, and Claude's proposals. The research behind it: `docs/research/LIFE-IN-LAGOS.md`. **Ideas, not decided**, unless marked as decided.
For: naira, betting, player, currency, radio, everyone, preacher, scan. Last changed 2026-10-16, 146 lines.
Links to 1: `gidi:docs/research/LIFE-IN-LAGOS.md`
Backlinks: 4 documents (`gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:decisions/lived-in.md`, `gidi:docs/research/LIFE-IN-LAGOS.md`), 0 code files ().
Nearest in words: `gidi:docs/research/LIFE-IN-LAGOS.md` (0.28); `gidi:decisions/lived-in.md` (0.23); `gidi:decisions/IDEAS.md` (0.22).

## gidi:docs
### `gidi:docs/BOARD.md`
**The drawing board**. The drawing board: The owner, 16 Oct 2026: "we should hand draw... we should know where something meets something... where the roads start, where the roads end, where the houses are, we should be able to move them."
For: click, bake, drag, dashed, edit, edits, board, select. Last changed 2026-10-24, 98 lines.
Links to 13: `gidi:scripts/board_server.py`, `gidi:scripts/check_district.py`, `gidi:scripts/compounds.py`, `gidi:scripts/fronts.py`, `gidi:scripts/ground.py`, `gidi:scripts/groundpaint.py`, `gidi:scripts/hand.py`, `gidi:scripts/real_underlay.py`, `gidi:scripts/roadends.py`, `gidi:scripts/things.py`, `gidi:scripts/trees.py`, `gidi:web/board.html` ...
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:decisions/NOW.md` (0.25); `gidi:docs/pilot-foodgate.md` (0.19); `gidi:docs/MAP-FORMAT.md` (0.19).

### `gidi:docs/CITY-LIVING-TEST.md`
**City living test: Haiku agents live in Gidi and report how moving around feels**. City living test: Haiku agents live in Gidi and report how moving around feels: Run this after every district is merged, and after any fix to roads, paths, rail or canals. It finds what the numeric checks (`check_district.py`) miss: places you can't reach, absurd detours, everything funnelling onto one road, houses with no way in, and whether districts feel like one city.
For: walk, ride, lives, foot, okada, interchange, lead, walks. Last changed 2026-10-16, 184 lines.
Links to 5: `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:web/gidi-data.js`, `gidi:web/locked.json`
Backlinks: 8 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/story/README.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/living-test-2026-10-13.md`, `gidi:docs/living-test-2026-10-13b.md`, `gidi:docs/living-test-2026-10-13c.md`, `gidi:docs/living-test-2026-10-14.md`, `gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14b.md` (0.52); `gidi:docs/living-test-2026-10-14.md` (0.51); `gidi:docs/living-test-2026-10-13c.md` (0.47).

### `gidi:docs/DATA-SOURCES.md`
**Data sources, and what to delete later**. Data sources, and what to delete later: Everything we've downloaded to study real Lagos lives on Daramola's Mac in `~/gidi-data/research/data/` (about 20 GB, mostly Google's 2.5D tiles). The OpenStreetMap extract (`lagos.osm.pbf`, 55 MB) is gone from the Mac; the repo's links to it were removed on 24 Oct.
For: final, cdla, delete, studies, licence, google, downloaded, outlines. Last changed 2026-10-24, 31 lines.
Links to 4: `gidi:docs/DEEP-STUDY.md`, `gidi:scripts/deep_prep.py`, `gidi:scripts/study_google.py`, `gidi:web/terrain.json`
Backlinks: 5 documents (`gidi-data:README.md`, `gidi:decisions/CHECKS.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/REBUILD-PLAN.md`), 0 code files ().
Nearest in words: `gidi:docs/REBUILD-PLAN.md` (0.25); `gidi:docs/gidi-data-plan.md` (0.14); `gidi-data:README.md` (0.13).

### `gidi:docs/DEEP-STUDY.md`
**The deep study: every district's inspiration, from all the data**. The deep study: every district's inspiration, from all the data: The owner asked for this on 15 Oct 2026: "the research should look at everything in the data and take them into consideration". Every Gidi district is rebuilt in the v2 frame (`docs/LAYOUT-V2.md`) by one shared generator. Each district gets its own profile, and the profile is set from this study.
For: types, wobble, touching, fabric, settings, district's, bands, counts. Last changed 2026-10-24, 65 lines.
Links to 9: `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/LAYOUT-V2.md`, `gidi:scripts/deep_check.py`, `gidi:scripts/deep_prep.py`, `gidi:scripts/deep_profile.py`, `gidi:scripts/deep_report.py`, `gidi:scripts/rename_mains.py`, `gidi:scripts/structure.py`, `gidi:scripts/study_deep.py`
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/DATA-SOURCES.md`, `gidi:docs/LAYOUT-V2.md`), 5 code files (`gidi:scripts/deep_prep.py`, `gidi:scripts/deep_profile.py`, `gidi:scripts/deep_tune.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/study_deep.py`).
Nearest in words: `gidi:docs/studies/border.md` (0.3); `gidi:docs/studies/yaba.md` (0.28); `gidi:docs/studies/port.md` (0.26).

### `gidi:docs/DISTRICT-BRIEF.md`
**Brief: build one Gidi district**. Brief: build one Gidi district: One session = one district. Read this brief, `README.md` and `docs/maze-pattern-study.md` (the worked example), then do the steps.
For: scale, seed, neighbourhood-level, worked, district's, oldshore, bazaar, frontier. Last changed 2026-10-24, 101 lines.
Links to 32: `gidi:README.md`, `gidi:data/results/lga_table.json`, `gidi:docs/CITY-LIVING-TEST.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/LAGOS-LOOK.md`, `gidi:docs/audit/README.md`, `gidi:docs/maze-pattern-study.md`, `gidi:legacy/blender/city_run.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:scripts/audit3d.py`, `gidi:scripts/bake_web.py` ...
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DEEP-STUDY.md`, `gidi:legacy/OLD-MAP.md`), 1 code files (`gidi:scripts/build_viewer.py`).
Nearest in words: `gidi:docs/look/COVERAGE.md` (0.28); `gidi:legacy/OLD-MAP.md` (0.25); `gidi:docs/LAGOS-ISMS.md` (0.22).

### `gidi:docs/FLOW-AUDIT.md`
**City flow audit, 22 Oct 2026**. City flow audit, 22 Oct 2026: Read-only: Gidi's frame (`web/layout-v2.json`, border roads in `web/network.json`, baked mains) against real Lagos's big roads (Overture motorway/trunk/primary, rail) at 1:4. Transform: UTM 31N, origin E 507,720 / N 712,110; X = 1500 + dE/4, Y = 6625 - dN/4.
For: arterial, flow, campus, upgrade, mainland, lagos's, north, mains. Last changed 2026-10-22, 27 lines.
Links to 2: `gidi:web/layout-v2.json`, `gidi:web/network.json`
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/STUDY.md` (0.24); `gidi:docs/lagos-study/councils.md` (0.18); `gidi:docs/LAYOUT-V2.md` (0.18).

### `gidi:docs/ISMS-BUILD.md`
**Building the Lagos-isms: what exists, what's missing, and the prompt**. Building the Lagos-isms: what exists, what's missing, and the prompt: The "feel like Lagos" pass. All fifteen districts are built from measured patterns. Now the isms in `docs/LAGOS-ISMS.md` go into the city, partly by rule and partly by hand. The topography (`feature/terrain`, `web/terrain.json`) comes first, because floods depend on it.
For: docs, gutter, safe, missing, one-way, edits, hand, rates. Last changed 2026-10-23, 118 lines.
Links to 17: `gidi:README.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/LAGOS-LIGHT.md`, `gidi:docs/UNREAL-PORT-PLAN.md`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/isms.py`, `gidi:web/app.js` ...
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:legacy/OLD-MAP.md`), 2 code files (`gidi:scripts/isms.py`, `gidi:web/isms-edits.json`).
Nearest in words: `gidi:docs/living-test-2026-10-15-gutters.md` (0.34); `gidi:docs/LAGOS-ISMS.md` (0.28); `gidi:docs/DISTRICT-BRIEF.md` (0.21).

### `gidi:docs/KIT-GAPS.md`
**Kit gaps: things the map now has that the 3D kit can't draw well yet**. Kit gaps: things the map now has that the 3D kit can't draw well yet: Started 15 Oct 2026 with the Food Gate pilot (`docs/REBUILD-PLAN.md`). Each line: what the data has, what the kit does today, and what it needs. Newest first within each group.
For: version, stored, furniture, vertex, data, kit's, kitchen, they're. Last changed 2026-10-19, 56 lines.
Links to 7: `gidi:docs/REBUILD-PLAN.md`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/gidi_kit/zinc.py`, `gidi:scripts/compounds.py`, `gidi:scripts/gen_fabric.py`
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/hand/maze-hub-lagos.md`, `gidi:docs/kit/MODELLER-BRIEF-ACT1.md`, `gidi:docs/pilot-foodgate.md`), 6 code files (`gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/props.py`, `gidi:legacy/blender/gidi_kit/street.py`).
Nearest in words: `gidi:docs/kit/MODELLER-BRIEF-ACT1.md` (0.48); `gidi:decisions/NOW.md` (0.22); `gidi:docs/look/research-buildings.md` (0.21).

### `gidi:docs/LAGOS-ISMS.md`
**Lagos-isms: the eccentricities in the real data (a running log)**. Lagos-isms: the eccentricities in the real data (a running log): **What this is.** While each district is studied, we log the real places' oddities: the things a tidy generator would never make, but that make Lagos feel like Lagos. For each one: - what it is - where it shows up in the real data (LGA and coordinates)
For: suits, one-way, kosofe, ikeja, wetland, acute, expressway, reserve. Last changed 2026-10-23, 276 lines.
Links to 7: `gidi:data/results/lga_table.json`, `gidi:data/tools/pull-data.sh`, `gidi:docs/ISMS-BUILD.md`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:scripts/isms.py`, `gidi:scripts/study_isms.py`
Backlinks: 18 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`, `gidi:docs/LAGOS-LOOK.md`, `gidi:docs/border-pattern-study.md`, `gidi:docs/estate-pattern-study.md`, `gidi:docs/frontier-pattern-study.md` ...), 3 code files (`gidi:legacy/blender/gidi_kit/rules.py`, `gidi:scripts/isms.py`, `gidi:scripts/study_isms.py`).
Nearest in words: `gidi:docs/ISMS-BUILD.md` (0.28); `gidi:docs/estate-pattern-study.md` (0.28); `gidi:docs/border-pattern-study.md` (0.26).

### `gidi:docs/LAGOS-LIGHT.md`
**Lagos light: why the city looks different**. Lagos light: why the city looks different: The owner's observation: photos taken in Nigeria look different from photos taken abroad. The vibrancy and the feel of the light aren't the same. Most of it is physics. This is the lighting brief for Gidi's look, in the browser now and in Unreal later (`docs/UNREAL-PORT-PLAN.md`).
For: shadows, light, abroad, haze, contrast, dusk, soft, warm. Last changed 2026-10-15, 61 lines.
Links to 1: `gidi:docs/UNREAL-PORT-PLAN.md`
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/ISMS-BUILD.md`), 0 code files ().
Nearest in words: `gidi:docs/hand/lagos-pass.md` (0.15); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.13); `gidi:docs/look/research-street.md` (0.11).

### `gidi:docs/LAGOS-LOOK.md`
**The Lagos look: a seeded Blender kit that styles Gidi from its data**. The Lagos look: a seeded Blender kit that styles Gidi from its data: **What this is.** Everything in Gidi gets its look from what the map data already knows about it: - its kind (front house, back house, shed, stalls, kiosk, …) - its storeys - its district (and so the character of that district's real inspiration)
For: attributes, conditions, contact, tile, character, markings, flats, material. Last changed 2026-10-23, 167 lines.
Links to 48: `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:docs/look/COVERAGE.md`, `gidi:docs/look/img/catalogue.jpg`, `gidi:docs/look/img/kinds-1.jpg`, `gidi:docs/look/img/kinds-2.jpg`, `gidi:docs/look/img/ladi-lane-overview.jpg`, `gidi:docs/look/img/ladi-lane-street.jpg`, `gidi:docs/look/img/shop-close.jpg`, `gidi:docs/look/img/showcase.jpg`, `gidi:docs/look/img/vehicles-people.jpg`, `gidi:docs/look/research-buildings.md` ...
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/research/LIFE-IN-LAGOS.md`, `gidi:legacy/OLD-MAP.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:docs/look/research-housing.md` (0.23); `gidi:docs/look/research-landmarks.md` (0.23); `gidi:docs/look/research-buildings.md` (0.22).

### `gidi:docs/LAYOUT-V2.md`
**Gidi v2: the layout**. Gidi v2: the layout: Chosen by the owner on 15 Oct 2026: a fictional Lagos with its real shape first, our own twists after. The first map (8.8 × 6.7 km) was boxy and squeezed the far ends of Lagos in.
For: harbour, channel, lagoon, creek, yaba, study's, akoka, frozen. Last changed 2026-10-16, 82 lines.
Links to 13: `gidi:docs/DEEP-STUDY.md`, `gidi:docs/img/layout-v2-island.png`, `gidi:docs/img/layout-v2.png`, `gidi:scripts/district_profiles.py`, `gidi:scripts/frame_network.py`, `gidi:scripts/freeze_district.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/layout_v2.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_core.py`, `gidi:web/hand/foodgate.json`, `gidi:web/layout-v2.json` ...
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/story/novels/README.md`, `gidi:docs/DEEP-STUDY.md`), 4 code files (`gidi:scripts/bake_web.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/frame_network.py`, `gidi:scripts/layout_v2.py`).
Nearest in words: `gidi:docs/lagos-study/councils.md` (0.24); `gidi:docs/lagos-study/STUDY.md` (0.23); `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.21).

### `gidi:docs/MAP-FORMAT.md`
**The new map's data format (draft 0.1, for the owner to approve)**. The new map's data format (draft 0.1, for the owner to approve): The new map is the one ground truth (decisions, 22 Oct: "everything that we do must be in map data. Every single thing"). The drawing board saves into it. The Blender kit and the Unreal import read it. Nothing else holds the city.
For: record, dress, field, records, stroke, face, value, relief. Last changed 2026-10-24, 598 lines.
Links to 19: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-game:tools/fields.py`, `gidi-game:tools/kit_fields.py`, `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`, `gidi:decisions/CHECKS.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/lived-in.md`, `gidi:docs/lagos-study/roads/EARTH-CHECK.md`, `gidi:docs/map-format-example/d15/district.json`, `gidi:docs/map-format-example/d15/dress/128_60.json`, `gidi:docs/map-format-example/d15/plan.json` ...
Backlinks: 7 documents (`gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md`, `gidi:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`, `gidi:docs/map-format-example/README.md`, `gidi:legacy/README.md`), 9 code files (`gidi-game:tools/block_build.py`, `gidi-game:tools/kit_fields.py`, `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`, `gidi:schema/map_schema.json`).
Nearest in words: `gidi:decisions/NOW.md` (0.45); `gidi:decisions/DECISIONS.md` (0.33); `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.31).

### `gidi:docs/REBUILD-PLAN.md`
**Rebuilding Gidi from Google's data**. Rebuilding Gidi from Google's data: Decided 15 Oct 2026. The first fifteen districts were measured from OpenStreetMap, so they inherited what OSM happened to map. Their gaps became our gaps. We rebuild from Google's data and the owner's eye on Google Earth: the map first, the story after.
For: google's, outlines, bends, slots, street's, osm's, scattered, extensions. Last changed 2026-10-15, 39 lines.
Links to 3: `gidi:docs/DATA-SOURCES.md`, `gidi:docs/data/google-vs-osm.json`, `gidi:docs/img/structure-google-osm-gidi.png`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/KIT-GAPS.md`, `gidi:docs/pilot-foodgate.md`), 4 code files (`gidi:legacy/blender/city.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/structure.py`).
Nearest in words: `gidi:docs/pilot-foodgate.md` (0.3); `gidi:docs/DATA-SOURCES.md` (0.25); `gidi:docs/DEEP-STUDY.md` (0.13).

### `gidi:docs/TWINS.md`
**Real twins: every type in Gidi and the real thing it comes from**. Real twins: every type in Gidi and the real thing it comes from: Made by `python3 scripts/twins.py` from the map and `web/twins.json` (the twins, kept by hand). Pictures live in `~/gidi-data/research/` (outside the repo). **none** = no twin yet; **red** = twin named, no picture; **amber** = pictures saved
For: none, amber, oshodi, pictures, twin, status, type, yaba. Last changed 2026-10-24, 283 lines.
Links to 2: `gidi:scripts/twins.py`, `gidi:web/twins.json`
Backlinks: 4 documents (`gidi-data:research/google/ibudo/NOTES.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi:scripts/twins.py`).
Nearest in words: `gidi-data:research/google/ibudo/NOTES.md` (0.17); `gidi-data:research/refs/REVIEW.md` (0.13); `gidi:docs/hand/ibudo/child_plan.md` (0.12).

### `gidi:docs/UNREAL-PORT-PLAN.md`
**Unreal port plan**. Unreal port plan: Agreed with the owner on 15 Oct 2026.
For: unreal, importer, meshes, browser, reimport, export, data, materials. Last changed 2026-10-23, 56 lines.
Links to 5: `gidi:decisions/DECISIONS.md`, `gidi:legacy/blender/city.py`, `gidi:scripts/audit3d.py`, `gidi:web/gidi-data.js`, `gidi:web/terrain.json`
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/ISMS-BUILD.md`, `gidi:docs/LAGOS-LIGHT.md`), 0 code files ().
Nearest in words: `gidi-game:README.md` (0.23); `gidi:decisions/NOW.md` (0.22); `gidi:decisions/DECISIONS.md` (0.2).

## gidi:docs/audit
### `gidi:docs/audit/README.md`
**3D audit, all districts**. 3D audit, all districts: Each district has its own page here with the details. Rerun with `.venv/bin/python scripts/audit3d.py`.
For: rerun, kinds, page, details, overshoots, knife-edge, misses, audit. Last changed 2026-10-15, 24 lines.
Links to 16: `gidi:docs/audit/bazaar.md`, `gidi:docs/audit/border.md`, `gidi:docs/audit/capital.md`, `gidi:docs/audit/estate.md`, `gidi:docs/audit/foodgate.md`, `gidi:docs/audit/frontier.md`, `gidi:docs/audit/heights.md`, `gidi:docs/audit/hub.md`, `gidi:docs/audit/jungle.md`, `gidi:docs/audit/maze.md`, `gidi:docs/audit/oldisland.md`, `gidi:docs/audit/oldshore.md` ...
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:docs/audit/hub.md` (0.45); `gidi:docs/audit/bazaar.md` (0.43); `gidi:docs/audit/capital.md` (0.43).

### `gidi:docs/audit/bazaar.md`
**3D audit: The Bazaar**. 3D audit: The Bazaar: `.venv/bin/python scripts/audit3d.py bazaar` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: bazaar, past, kinds, builder, overshoots, scrap, knife-edge, unfinished. Last changed 2026-10-15, 26 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/estate.md` (0.65); `gidi:docs/audit/hub.md` (0.63); `gidi:docs/audit/border.md` (0.6).

### `gidi:docs/audit/border.md`
**3D audit: The Border**. 3D audit: The Border: `.venv/bin/python scripts/audit3d.py border` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: kinds, builder, border, sport, pitch, danger, fishing, booth. Last changed 2026-10-15, 24 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/hub.md` (0.79); `gidi:docs/audit/maze.md` (0.72); `gidi:docs/audit/jungle.md` (0.67).

### `gidi:docs/audit/capital.md`
**3D audit: The Capital**. 3D audit: The Capital: `.venv/bin/python scripts/audit3d.py capital` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: capital, kinds, builder, ayinde, bust, overshoots, knife-edge, misses. Last changed 2026-10-15, 25 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/hub.md` (0.64); `gidi:docs/audit/estate.md` (0.61); `gidi:docs/audit/border.md` (0.57).

### `gidi:docs/audit/estate.md`
**3D audit: The Estate**. 3D audit: The Estate: `.venv/bin/python scripts/audit3d.py estate` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: kinds, past, shonibare, builder, mansion, clubhouse, overshoots, knife-edge. Last changed 2026-10-15, 25 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/hub.md` (0.73); `gidi:docs/audit/border.md` (0.65); `gidi:docs/audit/bazaar.md` (0.65).

### `gidi:docs/audit/foodgate.md`
**3D audit: Food Gate**. 3D audit: Food Gate: `.venv/bin/python scripts/audit3d.py foodgate` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: foodgate, kinds, builder, extension, sport, stage, pitch, overshoots. Last changed 2026-10-15, 28 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/look/COVERAGE.md` (0.45); `gidi:docs/audit/hub.md` (0.31); `gidi:docs/audit/border.md` (0.28).

### `gidi:docs/audit/frontier.md`
**3D audit: The Frontier**. 3D audit: The Frontier: `.venv/bin/python scripts/audit3d.py frontier` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: frontier, kinds, toll, builder, landmark, flare, bare, disputed. Last changed 2026-10-15, 31 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14j.md` (0.43); `gidi:docs/audit/border.md` (0.35); `gidi:docs/audit/estate.md` (0.34).

### `gidi:docs/audit/heights.md`
**3D audit: The Heights**. 3D audit: The Heights: `.venv/bin/python scripts/audit3d.py heights` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: heights, kinds, mbanefo, builder, hassan, oldisland, nightclub, beach. Last changed 2026-10-15, 29 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/estate.md` (0.63); `gidi:docs/audit/hub.md` (0.61); `gidi:docs/audit/border.md` (0.57).

### `gidi:docs/audit/hub.md`
**3D audit: The Hub**. 3D audit: The Hub: `.venv/bin/python scripts/audit3d.py hub` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: kinds, builder, sport, pitch, overshoots, knife-edge, warehouse, misses. Last changed 2026-10-15, 25 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/maze.md` (0.86); `gidi:docs/audit/border.md` (0.79); `gidi:docs/audit/jungle.md` (0.77).

### `gidi:docs/audit/jungle.md`
**3D audit: Jungle City**. 3D audit: Jungle City: `.venv/bin/python scripts/audit3d.py jungle` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: jungle, kinds, cafe, builder, studio, sport, pitch, overshoots. Last changed 2026-10-15, 26 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/hub.md` (0.77); `gidi:docs/audit/maze.md` (0.7); `gidi:docs/audit/border.md` (0.67).

### `gidi:docs/audit/maze.md`
**3D audit: The Maze**. 3D audit: The Maze: `.venv/bin/python scripts/audit3d.py maze` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: maze, kinds, builder, sport, pitch, overshoots, knife-edge, transformer. Last changed 2026-10-15, 25 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/hub.md` (0.86); `gidi:docs/audit/border.md` (0.72); `gidi:docs/audit/jungle.md` (0.7).

### `gidi:docs/audit/oldisland.md`
**3D audit: Old Island**. 3D audit: Old Island: `.venv/bin/python scripts/audit3d.py oldisland` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: oldisland, remi, past, kinds, degrees, builder, brazilian, overshoots. Last changed 2026-10-15, 32 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/look/COVERAGE.md` (0.49); `gidi:docs/audit/heights.md` (0.3); `gidi:docs/look/research-landmarks.md` (0.23).

### `gidi:docs/audit/oldshore.md`
**3D audit: Old Shore**. 3D audit: Old Shore: `.venv/bin/python scripts/audit3d.py oldshore` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: oldshore, past, kinds, lateef, builder, barge, sport, rack. Last changed 2026-10-15, 32 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/hub.md` (0.2); `gidi:docs/audit/estate.md` (0.19); `gidi:docs/look/COVERAGE.md` (0.19).

### `gidi:docs/audit/port.md`
**3D audit: The Port**. 3D audit: The Port: `.venv/bin/python scripts/audit3d.py port` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: port, past, kinds, builder, cellblock, crane, villa, trailer. Last changed 2026-10-15, 27 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/estate.md` (0.55); `gidi:docs/audit/hub.md` (0.55); `gidi:docs/audit/maze.md` (0.5).

### `gidi:docs/audit/railside.md`
**3D audit: Railside**. 3D audit: Railside: `.venv/bin/python scripts/audit3d.py railside` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: railside, fadipe, kinds, past, builder, lawal, roundabout, kehinde. Last changed 2026-10-15, 33 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/hub.md` (0.45); `gidi:docs/audit/estate.md` (0.34); `gidi:docs/railside-pattern-study.md` (0.33).

### `gidi:docs/audit/watertown.md`
**3D audit: Water Town**. 3D audit: Water Town: `.venv/bin/python scripts/audit3d.py watertown` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south).
For: watertown, kinds, builder, stilt, raft, shed, sawdust, overshoots. Last changed 2026-10-15, 25 lines.
Links to 1: `gidi:scripts/audit3d.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/audit/hub.md` (0.41); `gidi:docs/audit/estate.md` (0.39); `gidi:docs/audit/border.md` (0.37).

## gidi:docs
### `gidi:docs/bazaar-pattern-study.md`
**The Bazaar pattern study: Ojo round the electronics market → The Bazaar (v1)**. The Bazaar pattern study: Ojo round the electronics market → The Bazaar (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: bazaar, expressway, electronics, fair, wholesale, median, avenue, plazas. Last changed 2026-10-14, 125 lines.
Links to 12: `gidi:data/results/lga_table.json`, `gidi:docs/img/bazaar-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:web/gen-bazaar.json`, `gidi:web/network.json`
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.38); `gidi:docs/railside-pattern-study.md` (0.37); `gidi:docs/jungle-pattern-study.md` (0.36).

### `gidi:docs/border-pattern-study.md`
**Border pattern study: Badagry → the Border (v1)**. Border pattern study: Badagry → the Border (v1): Status: generated for review (15 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: badagry, border, bush, expressway, estimated, sprawl, post, worldcover. Last changed 2026-10-15, 137 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/border-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_boxheights.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/bazaar-pattern-study.md` (0.29); `gidi:docs/living-test-2026-10-14l.md` (0.28); `gidi:docs/capital-pattern-study.md` (0.27).

### `gidi:docs/capital-pattern-study.md`
**The Capital pattern study: central Ikeja → The Capital (v1)**. The Capital pattern study: central Ikeja → The Capital (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: capital, ikeja, estimated, cantonment, typical, gateways, range, shrine. Last changed 2026-10-14, 159 lines.
Links to 14: `gidi:data/results/lga_table.json`, `gidi:docs/img/capital-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:scripts/study_undermapped.py`, `gidi:study-capital-core.json` ...
Backlinks: 2 documents (`gidi:docs/living-test-2026-10-14.md`, `gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/railside-pattern-study.md` (0.41); `gidi:docs/bazaar-pattern-study.md` (0.38); `gidi:docs/estate-pattern-study.md` (0.36).

## gidi:docs/data/deep-check
### `gidi:docs/data/deep-check/SUMMARY.md`
**(no title)**. Each cell is Gidi against its real inspiration (0% = the same; ⚠ = more than 20% off). "Squares" = built 500 m squares measured (under 5: a small sample).
For: skew, squares, sample, inspiration, saba, cell, touching, small. Last changed 2026-10-16, 22 lines.
Links to 0: 
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/look/COVERAGE.md` (0.22); `gidi:docs/audit/README.md` (0.2); `gidi:docs/studies/airport.md` (0.19).

## gidi:docs
### `gidi:docs/estate-pattern-study.md`
**Estate pattern study: Ikeja GRA, Magodo and Omole → the Estate (v1)**. Estate pattern study: Ikeja GRA, Magodo and Omole → the Estate (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: estates, ikeja, gates, gra's, kosofe, estate's, omole's, typical. Last changed 2026-10-14, 141 lines.
Links to 15: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/estate-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py`, `gidi:scripts/study_landmarks.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.36); `gidi:docs/railside-pattern-study.md` (0.34); `gidi:docs/oldisland-pattern-study.md` (0.31).

### `gidi:docs/foodgate-pattern-study.md`
**Food Gate pattern study: Ojota–Ketu–Mile 12 (Kosofe) → Food Gate (v1)**. Food Gate pattern study: Ojota–Ketu–Mile 12 (Kosofe) → Food Gate (v1): Status: generated for review (13 Oct 2026). Same method as the other districts: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: kosofe, northern, mile, adeleke, maze's, ketu, median, corridor. Last changed 2026-10-14, 172 lines.
Links to 12: `gidi:data/results/lga_table.json`, `gidi:docs/img/foodgate-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:web/gen-foodgate.json`, `gidi:web/network.json`
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.38); `gidi:docs/jungle-pattern-study.md` (0.37); `gidi:docs/capital-pattern-study.md` (0.34).

### `gidi:docs/frontier-pattern-study.md`
**Frontier pattern study: the Lekki peninsula → the Frontier (v1)**. Frontier pattern study: the Lekki peninsula → the Frontier (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: frontier, peninsula, cells, awoyaya, empty, tracts, lekki, ajah. Last changed 2026-10-14, 177 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/frontier-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_boxheights.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/heights-pattern-study.md` (0.32); `gidi:docs/audit/frontier.md` (0.3); `gidi:docs/living-test-2026-10-14j.md` (0.29).

### `gidi:docs/gidi-data-plan.md`
**Gidi data plan: everything we need to build accurate districts (v1, 13 Oct 2026)**. Gidi data plan: everything we need to build accurate districts (v1, 13 Oct 2026): **Rule:** we study real Lagos to learn its patterns, then build our own world. Nothing real is traced or shipped.
For: cc-by, blocked, daramola's, tier, token, eti-osa, mapillary, wealth. Last changed 2026-10-24, 186 lines.
Links to 4: `gidi:data/results/heights.py`, `gidi:data/results/heights_by_lga.json`, `gidi:data/results/landpop.py`, `gidi:data/results/lga_table.json`
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/look/research-roads.md`), 0 code files ().
Nearest in words: `gidi:docs/LAGOS-ISMS.md` (0.18); `gidi:docs/lagos-lgas-research.md` (0.17); `gidi:docs/lagos-study/councils.md` (0.17).

### `gidi:docs/gidi-districts-v0.3.md`
**Gidi: 15 districts (map v0.3)**. Gidi: 15 districts (map v0.3): 13 October 2026. Built from the 20-LGA research (`lagos-lgas-research.md`). Places that felt alike were merged into one district. Sizes come from the map's polygons: 21.4 km² of district land in an 8.8 × 6.7 km frame, plus the lagoon, the ocean, and farms and bush that aren't built on. All names are working titles. Every real name, rite and person stays out of the game (see the sacred list in the research).
For: missions, outside, okada, heartland, dawn, banned, port, nights. Last changed 2026-10-13, 90 lines.
Links to 1: `gidi:docs/lagos-lgas-research.md`
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/story/README.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-lgas-research.md` (0.27); `gidi:docs/CITY-LIVING-TEST.md` (0.23); `gidi:legacy/OLD-MAP.md` (0.17).

## gidi:docs/hand
### `gidi:docs/hand/borrowed-lagos.md`
**Borrowed from Lagos: real places reimagined in Gidi (16 Oct 2026)**. Borrowed from Lagos: real places reimagined in Gidi (16 Oct 2026): The owner's direction: "take inspiration from the places to build the area... also from places that didn't inspire the districts, to give a taste of everywhere, tastefully and tactfully... research the actual Lagos map and see things you could take and creatively integrate."
For: placed, saba, channel, capital, mall, national, museum, great. Last changed 2026-10-23, 72 lines.
Links to 2: `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/monuments.py`
Backlinks: 2 documents (`gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`), 4 code files (`gidi:scripts/layout_v2.py`, `gidi:web/hand/capital.json`, `gidi:web/hand/heights.json`, `gidi:web/hand/port.json`).
Nearest in words: `gidi:docs/CITY-LIVING-TEST.md` (0.22); `gidi:docs/look/research-landmarks.md` (0.19); `gidi:docs/LAYOUT-V2.md` (0.18).

## gidi:docs/hand/ibudo
### `gidi:docs/hand/ibudo/README.md`
**Ìbùdó, spot 1: the market road under the Ring Road flyover (design v1, 19 Oct)**. Ìbùdó, spot 1: the market road under the Ring Road flyover (design v1, 19 Oct): Oshodi, studied on Google Earth and Street View (`~/gidi-data/research/google/ibudo/`, notes there), rebuilt one-for-one first, then made ours (the owner's method: like the fonts and the danfo). `design_v1.png`: metres, north up, 320 x 320 m.
For: one-for-one, flyover, oshodi, rusty-roof, flyover's, project's, footbridge, parasols. Last changed 2026-10-24, 19 lines.
Links to 0: 
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi-data:research/google/ibudo/NOTES.md` (0.28); `gidi-data:research/google/video1-street/NOTES.md` (0.15); `gidi:decisions/DECISIONS.md` (0.14).

### `gidi:docs/hand/ibudo/child_plan.md`
**Ìbùdó plan v3, the child of Oshodi and Ojuelegba (owner, 19 Oct 2026). Each area is a real place set down at true scale (1 m = 1 m, north up): a real point (anchor_real, lat/lon) sits on a Gidi point (anchor_gidi, map metres, y south). Any Gidi point in an area maps back to the real point under it: that real street is its twin, photographed there. Study in ~/gidi-data/research/google/ibudo/study/.**. Ìbùdó plan v3, the child of Oshodi and Ojuelegba (owner, 19 Oct 2026). Each area is a real place set down at true scale (1 m = 1 m, north up): a real point (anchor_real, lat/lon) sits on a Gidi point (anchor_gidi, map metres, y south). Any Gidi point in an area maps back to the real point under it: that real street is its twin, photographed there. Study in ~/gidi-data/research/google/ibudo/study/.: | Gidi area | Real place | Real box (lat, lon) | Real streets in it | |---|---|---|---| | Oshodi core | Oshodi: the interchange, Oshodi Market (red sheds, the mosque inside), Oshodi Rd, the Brown St grid of shop houses, the rail and the trunk road side by side | 6.5524 to 6.5601, 3.3465 to 3.3542 | Oshodi Rd, Brown St, Adekoya St, Araromi St, Banjoko St, Ogunlana St, Oredeyin St, Church St, Boladale St, Kunle Akinosi St, Macarthy Ln |
For: oshodi, mafoluku, cres, ojuelegba, osolo, jibowu, coach, arena. Last changed 2026-10-24, 32 lines.
Links to 0: 
Backlinks: 0 documents (), 1 code files (`gidi:scripts/child_plan.py`).
Nearest in words: `gidi-data:research/google/ibudo/study/INVENTORY.md` (0.55); `gidi-data:research/google/ibudo/NOTES.md` (0.25); `gidi:docs/lagos-study/STUDY.md` (0.16).

## gidi:docs/hand
### `gidi:docs/hand/lagos-pass.md`
**The Lagos pass (owner, 19 Oct)**. The Lagos pass (owner, 19 Oct): A place in Gidi is "Lagos" only when the owner has looked at it, rendered, and said so. Getting one spot there, all the way, teaches the technique; every decision made on the way becomes a rule other places can use (the data carries it), but each
For: overcast, bags, haze, conductors, billboards, videos, element, spot. Last changed 2026-10-24, 52 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/DECISIONS.md`), 1 code files (`gidi-game:tools/props_build.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.17); `gidi:decisions/DECISIONS.md` (0.17); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.17).

### `gidi:docs/hand/maze-hub-lagos.md`
**The Maze and the Hub: what makes them unmistakably Lagos (agreed 16 Oct 2026)**. The Maze and the Hub: what makes them unmistakably Lagos (agreed 16 Oct 2026): The first hand-made districts: Act 1 opens here (`decisions/story/act-1-draft.md`). Each item says what it is, where it goes in Gidi, how it gets built (the hand files, `scripts/hand.py`), and where it comes from: - **photo:** the owner's reference photos (`~/gidi-data/research/refs/REVIEW.md`)
For: brief, photo, story, print, yard, assets, bowl, pedro. Last changed 2026-10-24, 53 lines.
Links to 6: `gidi:decisions/story/act-1-draft.md`, `gidi:docs/KIT-GAPS.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:scripts/hand.py`, `gidi:web/districts_info.json`, `gidi:web/locked.json`
Backlinks: 2 documents (`gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi:web/hand/hub.json`).
Nearest in words: `gidi:docs/kit/MODELLER-BRIEF-ACT1.md` (0.18); `gidi:docs/living-test-2026-10-13b.md` (0.18); `gidi:decisions/story/README.md` (0.17).

### `gidi:docs/hand/monument-briefs.md`
**Monuments: what each needs (19 Oct)**. Monuments: what each needs (19 Oct): The owner's rule: Meshy for statues and monuments nobody walks into; structures people walk into or under are built in Blender part by part. Credits are spent in two steps: a concept picture first (nano-banana-2, 6 credits), the owner approves
For: bronze, concept, credits, menu, plinth, picture, stone, eyo-style. Last changed 2026-10-19, 30 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:docs/hand/borrowed-lagos.md` (0.14); `gidi:docs/look/research-landmarks.md` (0.14); `gidi:decisions/NOW.md` (0.11).

## gidi:docs
### `gidi:docs/heights-pattern-study.md`
**Heights pattern study: Ikoyi, Victoria Island and Banana Island → the Heights (v3)**. Heights pattern study: Ikoyi, Victoria Island and Banana Island → the Heights (v3): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: ikoyi, boxes, island, hipped, course, victoria, golf, booths. Last changed 2026-10-14, 208 lines.
Links to 17: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/heights-vs-real.png`, `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_boxheights.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/oldisland-pattern-study.md` (0.35); `gidi:docs/living-test-2026-10-14h.md` (0.35); `gidi:docs/frontier-pattern-study.md` (0.32).

### `gidi:docs/hub-pattern-study.md`
**Hub pattern study: Oshodi/Isolo + Surulere → The Hub (v1)**. Hub pattern study: Oshodi/Isolo + Surulere → The Hub (v1): Status: generated for review (13 Oct 2026). Same method as the Maze: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.** Data: OpenStreetMap (ODbL), Lagos extract, plus building heights from Google Open Buildings 2.5D (via `data/results/lga_table.json`). Area studied: Oshodi/Isolo + Surulere LGAs, 64.6 km² by the OpenStreetMap boundaries. The height and people table uses the government land areas, which add up to 75.9 km²; the shares are not affected.
For: slip, knot, stadium, maze, northern, terminal, percentile, station. Last changed 2026-10-13, 278 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/img/hub-station-skywalk.png`, `gidi:docs/img/hub-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/draw_gen.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/landmarks.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.43); `gidi:docs/jungle-pattern-study.md` (0.34); `gidi:docs/foodgate-pattern-study.md` (0.33).

### `gidi:docs/junctions.md`
**Junctions (pass 3 of the road work)**. Junctions (pass 3 of the road work): Status: built 15 Oct 2026. `scripts/junctions.py` runs inside the bake, after the road clean-up and before the road heights.
For: roundabouts, ring, wahab, radius, roundabout, ajasa, give-way, oladipo. Last changed 2026-10-15, 70 lines.
Links to 3: `gidi:docs/img/roundabouts.png`, `gidi:scripts/check_district.py`, `gidi:scripts/junctions.py`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-15n.md` (0.23); `gidi:docs/hub-pattern-study.md` (0.19); `gidi:docs/railside-pattern-study.md` (0.14).

### `gidi:docs/jungle-pattern-study.md`
**Jungle City pattern study: Ajegunle (+ Festac) → Jungle City (v1)**. Jungle City pattern study: Ajegunle (+ Festac) → Jungle City (v1): Status: generated for review (13 Oct 2026). Same method as the Maze and the Hub: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: jungle, flats, median, ajegunle, expressway, adeleke, maze's, festac. Last changed 2026-10-14, 246 lines.
Links to 13: `gidi:data/results/lga_table.json`, `gidi:docs/img/jungle-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/draw_gen.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:web/gen-jungle.json` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.49); `gidi:docs/foodgate-pattern-study.md` (0.37); `gidi:docs/bazaar-pattern-study.md` (0.36).

## gidi:docs/kit
### `gidi:docs/kit/MODELLER-BRIEF-ACT1.md`
**Brief for the kit modeller: the Act 1 gaps**. Brief for the kit modeller: the Act 1 gaps: Copy everything below the line into the modeller's session.
For: furniture, you're, plastic, chair, wheelbarrow, kitchen, cutscene, ticket. Last changed 2026-10-23, 40 lines.
Links to 11: `gidi:docs/KIT-GAPS.md`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/new_kit_sheet.py`, `gidi:web/gidi-data.js`
Backlinks: 1 documents (`gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:docs/KIT-GAPS.md` (0.48); `gidi:docs/hand/maze-hub-lagos.md` (0.18); `gidi:docs/look/research-leisure.md` (0.17).

## gidi:docs
### `gidi:docs/lagos-lgas-research.md`
**Lagos, one local government at a time: research for Gidi**. Lagos, one local government at a time: research for Gidi: 13 October 2026. Twenty researchers, one per local government area (LGA), each asked what makes the place itself: buildings, landmarks, roads, markets, transport, sound and smell, people, food, history, danger, environment, sacred things, pop culture, what Gidi can borrow and what to avoid. The full reports are below the summary, unedited.
For: unverified, unsourced, wikipedia, opened, languages, yoruba, festivals, religion. Last changed 2026-10-13, 2800 lines.
Links to 0: 
Backlinks: 5 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/gidi-districts-v0.3.md`, `gidi:docs/lagos-study/LIVING.md`, `gidi:docs/lagos-study/STUDY.md`, `gidi:docs/lagos-study/councils.md`), 1 code files (`gidi:scripts/map02.py`).
Nearest in words: `gidi:docs/lagos-study/LIVING.md` (0.32); `gidi:docs/lagos-study/councils.md` (0.3); `gidi:docs/gidi-districts-v0.3.md` (0.27).

## gidi:docs/lagos-study
### `gidi:docs/lagos-study/LIVING.md`
**Living in each district: the 51, for the brush and the lived-in layer**. Living in each district: the 51, for the brush and the lived-in layer: Study file (24 Oct 2026). Real place names live here and in other study files only, never in `map/`. The Gidi names come from `roads/NAMES.md`.
For: brush, draft, careful, traders, spots, workers, moving, activities. Last changed 2026-10-24, 555 lines.
Links to 6: `gidi:decisions/lived-in.md`, `gidi:docs/lagos-lgas-research.md`, `gidi:docs/lagos-study/STUDY.md`, `gidi:docs/lagos-study/councils.md`, `gidi:docs/lagos-study/roads/NAMES.md`, `gidi:docs/research/LIFE-IN-LAGOS.md`
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:decisions/lived-in.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-lgas-research.md` (0.32); `gidi:docs/lagos-study/councils.md` (0.2); `gidi:decisions/lived-in.md` (0.16).

### `gidi:docs/lagos-study/STUDY.md`
**How the whole Lagos map works: a study before cutting districts**. How the whole Lagos map works: a study before cutting districts: 22 Oct 2026. Read-only. Asked for by the owner's decision "Gidi is Lagos, miniaturised; the map starts again". This is evidence for a later frame proposal. It does not cut districts.
For: belt, bldg, ikorodu, tilt, planned, lekki, surveyed, mean. Last changed 2026-10-24, 322 lines.
Links to 6: `gidi:data/results/heights.py`, `gidi:data/results/heights_by_lga.json`, `gidi:data/results/lga_table.json`, `gidi:docs/lagos-study/councils.md`, `gidi:docs/lagos-study/roads/scripts/gaz.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`
Backlinks: 6 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`, `gidi:docs/lagos-study/LIVING.md`, `gidi:docs/lagos-study/councils.md`, `gidi:docs/lagos-study/similar/SIMILAR.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/councils.md` (0.58); `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.35); `gidi:docs/lagos-study/roads/ROADS.md` (0.35).

### `gidi:docs/lagos-study/councils.md`
**Lagos councils: the 20 LGAs and 37 LCDAs**. Lagos councils: the 20 LGAs and 37 LCDAs: 22 Oct 2026. Companion to `STUDY.md`. Read-only study; nothing here is a district yet.
For: known, lcdas, zones, amuwo-odofin, lcda, apapa, mainland, ikorodu. Last changed 2026-10-24, 212 lines.
Links to 2: `gidi:data/results/heights_by_lga.json`, `gidi:docs/lagos-study/STUDY.md`
Backlinks: 5 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`, `gidi:docs/lagos-study/LIVING.md`, `gidi:docs/lagos-study/STUDY.md`, `gidi:docs/lagos-study/similar/SIMILAR.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/STUDY.md` (0.58); `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.4); `gidi:docs/lagos-study/roads/ROADS.md` (0.34).

## gidi:docs/lagos-study/roads
### `gidi:docs/lagos-study/roads/EARTH-CHECK.md`
**Google Earth check of the borders (22 Oct 2026)**. Google Earth check of the borders (22 Oct 2026): `ROADS.md` section 6 left 15 borders the data could not settle. Each was looked at on Google Maps satellite (zoom 13 to 16) at the coordinates below. Study only: the 29 screenshots stay outside the repo, in `~/gidi-data/research/google/lagos-study/border-checks/` (file names carry the check number and the map
For: east, west, likely, north, trace, isolo, neutral, ikorodu. Last changed 2026-10-24, 274 lines.
Links to 2: `gidi:docs/lagos-study/roads/ROADS.md`, `gidi:docs/lagos-study/roads/places.csv`
Backlinks: 4 documents (`gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:docs/lagos-study/roads/NAMES.md`, `gidi:docs/lagos-study/roads/ROADS.md`), 1 code files (`gidi:scripts/frame_study.py`).
Nearest in words: `gidi:docs/lagos-study/roads/ROADS.md` (0.56); `gidi:docs/lagos-study/councils.md` (0.4); `gidi:docs/lagos-study/STUDY.md` (0.35).

### `gidi:docs/lagos-study/roads/NAMES.md`
**Echo names for the 51 districts (draft, 22 Oct 2026)**. Echo names for the 51 districts (draft, 22 Oct 2026): Working names for the 51 districts in `EARTH-CHECK.md` ("District list after the checks"), as the map format's fourth call asks (`decisions/DECISIONS.md`, "The map format's four calls", point 4; the rule is in `decisions/IDEAS.md`, "Place names: echo names"). **Every name here is a draft: the owner reviews it**, and any of them can change later.
For: yoruba, consonant, english, vowel, sound, leke, mile, none. Last changed 2026-10-22, 115 lines.
Links to 4: `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:docs/lagos-study/roads/EARTH-CHECK.md`, `gidi:docs/lagos-study/roads/places.csv`
Backlinks: 3 documents (`gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:docs/lagos-study/LIVING.md`), 0 code files ().
Nearest in words: `gidi:decisions/IDEAS.md` (0.22); `gidi:docs/lagos-lgas-research.md` (0.13); `gidi:docs/lagos-study/LIVING.md` (0.12).

### `gidi:docs/lagos-study/roads/ROADS.md`
**Roads first, districts by their borders**. Roads first, districts by their borders: Step 1 of the new map plan (22 Oct): Gidi is real Lagos made smaller, at 1:3, in a frame about 27 × 10.5 km. This study lays down the skeleton of real roads, cuts Lagos into places along its real borders, measures every border, and joins places into districts only where they really touch and are alike.
For: morogbo, north-east, imota, land, ijegun-egba, west, apapa, swamp. Last changed 2026-10-24, 510 lines.
Links to 29: `gidi:docs/lagos-study/roads/EARTH-CHECK.md`, `gidi:docs/lagos-study/roads/borders.csv`, `gidi:docs/lagos-study/roads/districts.csv`, `gidi:docs/lagos-study/roads/districts_55.png`, `gidi:docs/lagos-study/roads/districts_55_inner.png`, `gidi:docs/lagos-study/roads/districts_60.png`, `gidi:docs/lagos-study/roads/districts_60_inner.png`, `gidi:docs/lagos-study/roads/districts_65.png`, `gidi:docs/lagos-study/roads/districts_65_inner.png`, `gidi:docs/lagos-study/roads/ladder.csv`, `gidi:docs/lagos-study/roads/not_neighbours.csv`, `gidi:docs/lagos-study/roads/places.csv` ...
Backlinks: 2 documents (`gidi:decisions/NOW.md`, `gidi:docs/lagos-study/roads/EARTH-CHECK.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.56); `gidi:docs/lagos-study/similar/SIMILAR.md` (0.39); `gidi:docs/lagos-study/STUDY.md` (0.35).

## gidi:docs/lagos-study/similar
### `gidi:docs/lagos-study/similar/GOOGLE-CHECK.md`
**The close calls, checked on Google satellite (22 Oct 2026)**. The close calls, checked on Google satellite (22 Oct 2026): The similarity numbers (`SIMILAR.md`) flagged 10 merges as close or doubtful. Each pair was looked at side by side on Google satellite, about 1 km across, at each unit's seed point. Study only: the pictures stay outside the repo (`~/gidi-data/research/google/lagos-study/close-calls/`, sheet `close_calls.jpg`).
For: obalende-onikan, split, joins, splits, magodo-omole, roofs, gbagada, okota-ikotun. Last changed 2026-10-24, 31 lines.
Links to 1: `gidi:docs/lagos-study/similar/SIMILAR.md`
Backlinks: 1 documents (`gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/STUDY.md` (0.22); `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.2); `gidi:docs/lagos-study/roads/ROADS.md` (0.2).

### `gidi:docs/lagos-study/similar/SIMILAR.md`
**Which places are alike: numbers for cutting districts**. Which places are alike: numbers for cutting districts: 22 Oct 2026. Read-only study. It gives numbers for how many districts, and which places merge. It does not decide. Builds on `docs/lagos-study/STUDY.md` and `councils.md`, and reuses their 250 m grids.
For: belt, land, bungalow, ogba-agidingbi-alausa, isheri-olowora, ijora-badia, apapa-tin, alaba-ojo-lasu. Last changed 2026-10-24, 957 lines.
Links to 12: `gidi:docs/lagos-study/STUDY.md`, `gidi:docs/lagos-study/councils.md`, `gidi:docs/lagos-study/roads/scripts/report.py`, `gidi:docs/lagos-study/similar/ladder.csv`, `gidi:docs/lagos-study/similar/pairs.csv`, `gidi:docs/lagos-study/similar/scripts/analyse.py`, `gidi:docs/lagos-study/similar/scripts/finger.py`, `gidi:docs/lagos-study/similar/scripts/know.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`, `gidi:docs/lagos-study/similar/scripts/seeds.py`, `gidi:docs/lagos-study/similar/scripts/units.py`, `gidi:docs/lagos-study/similar/units.csv`
Backlinks: 2 documents (`gidi:decisions/NOW.md`, `gidi:docs/lagos-study/similar/GOOGLE-CHECK.md`), 4 code files (`gidi:docs/lagos-study/similar/scripts/appendix.py`, `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`, `gidi:docs/lagos-study/similar/scripts/report.py`).
Nearest in words: `gidi:docs/lagos-study/similar/districts.md` (0.9); `gidi:docs/lagos-study/roads/ROADS.md` (0.39); `gidi:docs/lagos-study/STUDY.md` (0.33).

### `gidi:docs/lagos-study/similar/districts.md`
**At 90%: 81 districts (71 after folding tiny plain units)**. At 90%: 81 districts (71 after folding tiny plain units): Rich or distinct units still alone (24): Isale Eko-Idumota-Marina, Ikoyi-Banana Island, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Ogijo-Sagamu Rd, Isheri-Olowora (Ikosi-Isheri), UNILAG, Ebute Metta-Oyingbo-Otto-Iddo, Makoko-Iwaya, Surulere (Ojuelegba-Bode Thomas-Stadium), Ilupeju, Papa Ajao-Ladipo, Oshodi-Mafoluku, Apapa-Tin Can, Ijora-Badia, Ajegunle (Ajeromi), Amukoko-Layeni (Ifelodun), Mile 2-Amuwo, Kirikiri-Navy Town, Alaba-Ojo-LASU, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.
For: ftz-dangote, agric-majidun-ogolonto, makoko-iwaya, ijora-badia, eko-idumota-marina, isheri-olowora, allen-opebi-computer, ogba-agidingbi-alausa. Last changed 2026-10-22, 469 lines.
Links to 0: 
Backlinks: 0 documents (), 2 code files (`gidi:docs/lagos-study/similar/scripts/appendix.py`, `gidi:docs/lagos-study/similar/scripts/report.py`).
Nearest in words: `gidi:docs/lagos-study/similar/SIMILAR.md` (0.9); `gidi:docs/lagos-study/roads/ROADS.md` (0.33); `gidi:docs/lagos-study/STUDY.md` (0.17).

## gidi:docs
### `gidi:docs/living-test-2026-10-13.md`
**City living test, 13 Oct 2026: the Maze, the Hub, Jungle City**. City living test, 13 Oct 2026: the Maze, the Hub, Jungle City: This is the first run of `docs/CITY-LIVING-TEST.md`, done on the whole built city.
For: minutes, walk, skywalk, jungle, interchange, station, tool, session. Last changed 2026-10-13, 108 lines.
Links to 4: `gidi:docs/CITY-LIVING-TEST.md`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:web/gidi-data.js`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-13b.md` (0.68); `gidi:docs/living-test-2026-10-13c.md` (0.6); `gidi:docs/living-test-2026-10-14.md` (0.5).

### `gidi:docs/living-test-2026-10-13b.md`
**City living test, 13 Oct 2026 (second run): the Maze, the Hub, Jungle City, Food Gate**. City living test, 13 Oct 2026 (second run): the Maze, the Hub, Jungle City, Food Gate: This is the second run of `docs/CITY-LIVING-TEST.md` today. It covers the whole built city after the owner's five fixes and the new district, Food Gate.
For: minutes, walk, interchange, jungle, stadium's, mile, yard, maze. Last changed 2026-10-13, 135 lines.
Links to 3: `gidi:docs/CITY-LIVING-TEST.md`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-13c.md` (0.72); `gidi:docs/living-test-2026-10-13.md` (0.68); `gidi:docs/living-test-2026-10-14.md` (0.59).

### `gidi:docs/living-test-2026-10-13c.md`
**City living test, 13 Oct 2026 (third run): all five districts**. City living test, 13 Oct 2026 (third run): all five districts: This is the third run of `docs/CITY-LIVING-TEST.md` today. It is the first run with all five built districts: the Maze, the Hub, Jungle City, Food Gate and the new Water Town.
For: minutes, walk, stilt, tool, foot, jungle, town, footbridge. Last changed 2026-10-13, 135 lines.
Links to 6: `gidi:docs/CITY-LIVING-TEST.md`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/walknet.py`, `gidi:web/districts_info.json`, `gidi:web/locked.json`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-13b.md` (0.72); `gidi:docs/living-test-2026-10-14.md` (0.63); `gidi:docs/living-test-2026-10-13.md` (0.6).

### `gidi:docs/living-test-2026-10-14.md`
**City living test, 14 Oct 2026: six districts, with the new Capital**. City living test, 14 Oct 2026: six districts, with the new Capital: This is the test in `docs/CITY-LIVING-TEST.md`, run on the whole built city after the Capital was added. It also covers Water Town v2 (fingers to the shore) and the boss's post, which this branch carries.
For: minutes, capital, walk, gadget, secretariat, fingers, village, mile. Last changed 2026-10-14, 127 lines.
Links to 4: `gidi:docs/CITY-LIVING-TEST.md`, `gidi:docs/capital-pattern-study.md`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14b.md` (0.65); `gidi:docs/living-test-2026-10-13c.md` (0.63); `gidi:docs/living-test-2026-10-13b.md` (0.59).

### `gidi:docs/living-test-2026-10-14b.md`
**City living test, 14 Oct 2026 (second run): seven districts, with the new Bazaar**. City living test, 14 Oct 2026 (second run): seven districts, with the new Bazaar: This run tests four changes on this branch: - **The fair block count:** the generator fix that came with it gives Jungle City and the Capital fewer collector streets. - **The okada ban zone** in the Capital. - **The new district:** the Bazaar.
For: walk, gadget, ride, dead-end, tool, minutes, village, jungle. Last changed 2026-10-14, 97 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14.md` (0.65); `gidi:docs/living-test-2026-10-13c.md` (0.53); `gidi:docs/living-test-2026-10-14d.md` (0.53).

### `gidi:docs/living-test-2026-10-14c.md`
**City living test, 14 Oct 2026 (third run): eight districts, with the new Port**. City living test, 14 Oct 2026 (third run): eight districts, with the new Port: There are two states: - **Before:** `main` at the start of this work (commit `1925734`, seven districts). - **After:** this branch, with the Port.
For: reserve, minutes, yard, port, container, chidi, okada, ngozi. Last changed 2026-10-14, 71 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14f.md` (0.44); `gidi:docs/living-test-2026-10-14.md` (0.43); `gidi:docs/living-test-2026-10-13c.md` (0.42).

### `gidi:docs/living-test-2026-10-14d.md`
**City living test, 14 Oct 2026 (fourth run): nine districts, with the new Railside**. City living test, 14 Oct 2026 (fourth run): nine districts, with the new Railside: There are two states: - **Before:** `main` at the start of this work (commit `8a23e34`, eight districts). - **After:** this branch.
For: re-laid, railside, roundabout, interchange, walk, capital, minutes, nine. Last changed 2026-10-14, 67 lines.
Links to 2: `gidi:docs/LAGOS-ISMS.md`, `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14b.md` (0.53); `gidi:docs/living-test-2026-10-14.md` (0.52); `gidi:docs/living-test-2026-10-14e.md` (0.52).

### `gidi:docs/living-test-2026-10-14e.md`
**City living test, 14 Oct 2026 (fifth run): ten districts, with the new Estate**. City living test, 14 Oct 2026 (fifth run): ten districts, with the new Estate: There are two states: - **Before:** `main` at the start of this work (commit `22daecd`, nine districts). - **After:** this branch.
For: capital's, senator's, musa's, okada, gadget, estate's, walk, emeka. Last changed 2026-10-14, 68 lines.
Links to 2: `gidi:docs/LAGOS-ISMS.md`, `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14d.md` (0.52); `gidi:docs/living-test-2026-10-14.md` (0.45); `gidi:docs/living-test-2026-10-14b.md` (0.43).

### `gidi:docs/living-test-2026-10-14f.md`
**City living test, 14 Oct 2026 (sixth run): eleven districts, with the new Old Island**. City living test, 14 Oct 2026 (sixth run): eleven districts, with the new Old Island: There are two states: - **Before:** `main` at the start of this work (commit `ea47fc6`, ten districts). - **After:** this branch.
For: bisi, sule, cloth, wharf, minutes, island, brazilian, walked. Last changed 2026-10-14, 83 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14g.md` (0.52); `gidi:docs/living-test-2026-10-14c.md` (0.44); `gidi:docs/living-test-2026-10-14d.md` (0.42).

### `gidi:docs/living-test-2026-10-14g.md`
**City living test, 14 Oct 2026 (seventh run): twelve districts, with the new Heights**. City living test, 14 Oct 2026 (seventh run): twelve districts, with the new Heights: There are two states: - **Before:** `main` at the start of this work (commit `02f2a78`, eleven districts). - **After:** this branch. It does three things: - pins of walled places now stand at their gates - the Palace is safe ground in the data
For: pearl, walk, towers, minutes, kunle, shorter, emeka, gates. Last changed 2026-10-14, 104 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14f.md` (0.52); `gidi:docs/living-test-2026-10-14i.md` (0.51); `gidi:docs/living-test-2026-10-14h.md` (0.5).

### `gidi:docs/living-test-2026-10-14h.md`
**City living test, 14 Oct 2026 (eighth run): the Heights v2**. City living test, 14 Oct 2026 (eighth run): the Heights v2: There are two states: - **Before:** `main` at commit `47b75ef` (the Heights v1). - **After:** this branch.
For: beach, bisi, minutes, sunday, pearl, kunle, island, drive. Last changed 2026-10-14, 57 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14i.md` (0.51); `gidi:docs/living-test-2026-10-14g.md` (0.5); `gidi:docs/living-test-2026-10-14j.md` (0.39).

### `gidi:docs/living-test-2026-10-14i.md`
**City living test, 14 Oct 2026 (ninth run): the Heights v3**. City living test, 14 Oct 2026 (ninth run): the Heights v3: There are two states: - **Before:** `main` at commit `a679778` (the Heights v2). - **After:** this branch: the golf course, bigger Ikoyi houses in five architectural styles, and a floating street tied in.
For: pearl, club, golf, minutes, walk, kunle, towers, course. Last changed 2026-10-14, 42 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14g.md` (0.51); `gidi:docs/living-test-2026-10-14h.md` (0.51); `gidi:docs/living-test-2026-10-14j.md` (0.39).

### `gidi:docs/living-test-2026-10-14j.md`
**City living test, 14 Oct 2026 (tenth run): thirteen districts, with the new Frontier**. City living test, 14 Oct 2026 (tenth run): thirteen districts, with the new Frontier: There are two states: - **Before:** `main` at commit `10b9708` (twelve districts). - **After:** this branch: the Frontier, and the Heights rebuilt once with `keep_gateways`.
For: frontier, femi, toll, plaza, ride, walk, pearl, refinery. Last changed 2026-10-14, 66 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14g.md` (0.46); `gidi:docs/audit/frontier.md` (0.43); `gidi:docs/CITY-LIVING-TEST.md` (0.41).

### `gidi:docs/living-test-2026-10-14k.md`
**City living test, 15 Oct 2026 (eleventh run): Old Shore**. City living test, 15 Oct 2026 (eleventh run): Old Shore: There are two states: - **Before:** `main` at commit `cf613f8` (thirteen districts). - **After:** this branch: Old Shore, built in parallel with the Border.
For: shore, sade, fish, hunter, minutes, tools, thirteen, roundabout. Last changed 2026-10-15, 52 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/oldshore-pattern-study.md` (0.49); `gidi:docs/living-test-2026-10-15m.md` (0.43); `gidi:docs/CITY-LIVING-TEST.md` (0.32).

### `gidi:docs/living-test-2026-10-14l.md`
**City living test, 15 Oct 2026: the Border**. City living test, 15 Oct 2026: the Border: There are two states: - **Before:** `main` at commit `cf613f8` (thirteen districts). - **After:** this branch: the Border, and Railside rebuilt once with `keep_gateways`.
For: dayo, funmi, coconut, emeka, railside, border, checkpoint, rode. Last changed 2026-10-15, 64 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14d.md` (0.33); `gidi:docs/living-test-2026-10-14g.md` (0.3); `gidi:docs/CITY-LIVING-TEST.md` (0.3).

### `gidi:docs/living-test-2026-10-15-gutters.md`
**City living test, 15 Oct 2026: open gutters (ism 15, group 1)**. City living test, 15 Oct 2026: open gutters (ism 15, group 1): `scripts/isms.py` now puts open gutters into the city data, with plank and slab crossings at doors and side streets. Two Haiku residents walked the numbers through `scripts/explore_city.py`, whose `look` and `home` now also report gutters.
For: gutter, gutters, blocked, slabs, plank, adeleke, door, fifteen. Last changed 2026-10-15, 31 lines.
Links to 5: `gidi:docs/img/gutters-estate.png`, `gidi:docs/img/gutters-maze.png`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/isms.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/ISMS-BUILD.md` (0.34); `gidi:docs/living-test-2026-10-13.md` (0.15); `gidi:docs/pilot-foodgate.md` (0.13).

### `gidi:docs/living-test-2026-10-15m.md`
**City living test, 15 Oct 2026 (twelfth run): all fifteen districts**. City living test, 15 Oct 2026 (twelfth run): all fifteen districts: Old Shore and the Border were built in parallel, on separate branches (living tests 14k and 14l). The Border was merged first. This run checks the city once both are combined: main at `a94e9ee` (the Border and the 3D kit) plus Old Shore.
For: combined, shore, shore's, fifteen, walk, hunter, trips, palace. Last changed ?, 30 lines.
Links to 1: `gidi:scripts/check_district.py`
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14k.md` (0.43); `gidi:docs/oldshore-pattern-study.md` (0.36); `gidi:docs/CITY-LIVING-TEST.md` (0.24).

### `gidi:docs/living-test-2026-10-15n.md`
**City living test, 15 Oct 2026: road clean-up, pass 1**. City living test, 15 Oct 2026: road clean-up, pass 1: The first of four road passes. `scripts/roadclean.py` now runs inside the bake, after every road is gathered and before the civic layer. It fixes what the 3D audit (`scripts/audit3d.py`) finds, by fixed rules. No building moves, and no road is run through a building.
For: lesser, pass, changed, fifteen, mains, loses, tidying, straightened. Last changed 2026-10-15, 38 lines.
Links to 4: `gidi:docs/img/roads-clean.png`, `gidi:scripts/audit3d.py`, `gidi:scripts/check_district.py`, `gidi:scripts/roadclean.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/junctions.md` (0.23); `gidi:docs/road-heights.md` (0.17); `gidi:docs/living-test-2026-10-15m.md` (0.13).

## gidi:docs/look
### `gidi:docs/look/COVERAGE.md`
**Kit coverage: everything in Gidi's data, and whether the kit builds it**. Kit coverage: everything in Gidi's data, and whether the kit builds it: Made by `python3 legacy/blender/coverage.py` from `web/gen-*.json`, `web/civic.json` and `legacy/blender/gidi_kit/registry.py`. Do not edit by hand.
For: oldisland, foodgate, watertown, bazaar, railside, port, capital, oldshore. Last changed 2026-10-23, 145 lines.
Links to 3: `gidi:legacy/blender/coverage.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:web/civic.json`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 1 code files (`gidi:legacy/blender/coverage.py`).
Nearest in words: `gidi:docs/audit/oldisland.md` (0.49); `gidi:docs/audit/foodgate.md` (0.45); `gidi:docs/audit/watertown.md` (0.33).

### `gidi:docs/look/research-buildings.md`
**Lagos buildings and their parts: a catalogue for the Gidi generator**. Lagos buildings and their parts: a catalogue for the Gidi generator: Rule zero: this is pattern research. Nothing here names a building to copy; Gidi invents its own.
For: elite, select, white, often, older, painted, long-span, green. Last changed 2026-10-14, 697 lines.
Links to 0: 
Backlinks: 7 documents (`gidi:docs/LAGOS-LOOK.md`, `gidi:docs/look/research-civic.md`, `gidi:docs/look/research-commerce.md`, `gidi:docs/look/research-housing.md`, `gidi:docs/look/research-landmarks.md`, `gidi:docs/look/research-leisure.md`, `gidi:docs/look/research-religious.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-housing.md` (0.66); `gidi:docs/look/research-street.md` (0.48); `gidi:docs/look/research-leisure.md` (0.47).

### `gidi:docs/look/research-civic.md`
**Civic and public-service buildings: a catalogue for the Gidi generator**. Civic and public-service buildings: a catalogue for the Gidi generator: Scope: hospitals, clinics, chemists, police (stations, command, posts, checkpoints, barracks), fire, government offices, customs, prison, army, courts, cemeteries, post offices, traffic/task-force posts, and power-company offices and transformers. This builds on `docs/look/research-buildings.md` sections 10.7, 10.8, 10.11 and 10.12, and on `docs/look/research-street.md` sections 2.2 and 3.8. It goes further and does not repeat those sections.
For: white, agency, crest, police, colours, steel, select, variants. Last changed 2026-10-14, 647 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-transport.md` (0.5); `gidi:docs/look/research-housing.md` (0.49); `gidi:docs/look/research-leisure.md` (0.46).

### `gidi:docs/look/research-commerce.md`
**Gidi commerce catalogue: markets, shops, commerce and industry**. Gidi commerce catalogue: markets, shops, commerce and industry: Purpose: specs for the seeded Blender kit. This builds on `docs/look/research-buildings.md` §6 (shop bays, container shop, kiosk, stall, plaza) and `docs/look/research-street.md` §6 (stall goods, umbrellas, chairs, generators, water tanks, night light). Those base specs are **not repeated**. Where they apply, this file refers to them as `B§6.x` and `S§6.x`.
For: mapping, select, condition, variants, steel, props, white, timber. Last changed 2026-10-16, 883 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-transport.md` (0.55); `gidi:docs/look/research-housing.md` (0.55); `gidi:docs/look/research-leisure.md` (0.48).

### `gidi:docs/look/research-housing.md`
**Lagos housing types beyond the front/back house: a catalogue for the Gidi kit**. Lagos housing types beyond the front/back house: a catalogue for the Gidi kit: Scope: every housing type (and the housing-adjacent structures that sit on residential plots) that the Gidi census lists, other than the generic front/back house that `docs/look/research-buildings.md` already covers. This file builds on that document (§0 constants, §1 rooming house, §7 Brazilian house, §8 stilt house, §9 elite) and goes deeper. It does not repeat its paint palette, weathering grammar or sandcrete constants. Use those as the base layer.
For: elite, steel, white, mapping, condition, select, decayed, flats. Last changed 2026-10-14, 926 lines.
Links to 1: `gidi:docs/look/research-buildings.md`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-buildings.md` (0.66); `gidi:docs/look/research-commerce.md` (0.55); `gidi:docs/look/research-leisure.md` (0.54).

### `gidi:docs/look/research-landmarks.md`
**Lagos landmarks as patterns: a catalogue for Gidi's invented landmarks**. Lagos landmarks as patterns: a catalogue for Gidi's invented landmarks: Rule zero applies here more than anywhere else. A landmark is the thing a player will recognise, so **every Gidi landmark must be an original design**. Real Lagos structures appear below only as references for a *type*: what makes that kind of thing striking, how big it is, what it is made of and how it ages. Each item ends with 1-2 invented Gidi designs that share the spirit but not the silhouette of any real one.
For: white, oldisland, canon, condition, reference, concrete, select, painted. Last changed 2026-10-14, 735 lines.
Links to 3: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`, `gidi:web/districts_info.json`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 2 code files (`gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/monuments.py`).
Nearest in words: `gidi:docs/look/research-transport.md` (0.46); `gidi:docs/look/research-housing.md` (0.44); `gidi:docs/look/research-leisure.md` (0.44).

### `gidi:docs/look/research-leisure.md`
**Gidi catalogue: education, sport, leisure and nightlife places**. Gidi catalogue: education, sport, leisure and nightlife places: This catalogue extends `docs/look/research-buildings.md` and `docs/look/research-street.md`. It does not repeat their walls, gates, roofs, generators, umbrellas, plastic chairs or crowd tables. It reuses them by name: "compound wall (buildings §4)", "event canopy (street §6.3)".
For: white, condition, elite, painted, mapping, select, variants, props. Last changed 2026-10-14, 800 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-housing.md` (0.54); `gidi:docs/look/research-transport.md` (0.49); `gidi:docs/look/research-commerce.md` (0.48).

### `gidi:docs/look/research-religious.md`
**Gidi look research: religious buildings and places**. Gidi look research: religious buildings and places: Scope: mosques, churches, white-garment churches, prayer camps, storefront worship, roadside prayer spaces, traditional shrines and festival structures, and how each one sits in the street. Builds on `docs/look/research-buildings.md` §10.5–10.6 and `research-street.md` (loudspeakers, banners, Friday/Sunday dress). This file goes deeper. It does not repeat those sections.
For: dome, white, green, prayer, mosque, blue, hall, minaret. Last changed 2026-10-14, 625 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-housing.md` (0.48); `gidi:docs/look/research-buildings.md` (0.46); `gidi:docs/look/research-leisure.md` (0.46).

### `gidi:docs/look/research-roads.md`
**Gidi ground catalogue: roads in every condition, drains, ground, water, vegetation, refuse**. Gidi ground catalogue: roads in every condition, drains, ground, water, vegetation, refuse: This catalogue covers the honest Lagos: roads that are mud with potholes of water, mushy laterite lanes, failed asphalt, choked drains. It builds on `docs/look/research-street.md` §1 and §6.7–6.9, and does not repeat what is there: road widths by class, kerb paint colours, median types, basic drain sizes, basic pothole density, the tree census. It goes deeper on **condition** and on **how to select it from data**.
For: select, mapping, sand, asphalt, laterite, mains, research-street, refuse. Last changed 2026-10-23, 1147 lines.
Links to 2: `gidi:docs/look/research-street.md`, `gidi:legacy/blender/gidi_kit/rules.py`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-street.md` (0.38); `gidi:docs/look/research-transport.md` (0.37); `gidi:docs/look/research-commerce.md` (0.36).

### `gidi:docs/look/research-street.md`
**Gidi street catalogue: roads, vehicles, people, signage, props**. Gidi street catalogue: roads, vehicles, people, signage, props: This is research for a procedural generator. It studies real Lagos and describes patterns only. Every brand is described generically, and Gidi must invent its own names, liveries and slogans.
For: select, black, white, yellow, colours, blue, often, painted. Last changed 2026-10-14, 923 lines.
Links to 0: 
Backlinks: 9 documents (`gidi:docs/LAGOS-LOOK.md`, `gidi:docs/look/research-civic.md`, `gidi:docs/look/research-commerce.md`, `gidi:docs/look/research-landmarks.md`, `gidi:docs/look/research-leisure.md`, `gidi:docs/look/research-religious.md`, `gidi:docs/look/research-roads.md`, `gidi:docs/look/research-transport.md` ...), 2 code files (`gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/street.py`).
Nearest in words: `gidi:docs/look/research-vehicles.md` (0.53); `gidi:docs/look/research-transport.md` (0.48); `gidi:docs/look/research-buildings.md` (0.48).

### `gidi:docs/look/research-transport.md`
**Gidi transport and infrastructure catalogue**. Gidi transport and infrastructure catalogue: Research for the seeded Blender kit. Rule zero applies: real Lagos is studied as a pattern only. All names, liveries and logos in the kit must be invented; real places below are examples of a pattern, not things to copy.
For: white, mapping, select, condition, colours, steel, yellow, blue. Last changed 2026-10-14, 886 lines.
Links to 1: `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-commerce.md` (0.55); `gidi:docs/look/research-housing.md` (0.53); `gidi:docs/look/research-civic.md` (0.5).

### `gidi:docs/look/research-vehicles.md`
**Gidi vehicle catalogue: everything that moves on Lagos roads and water**. Gidi vehicle catalogue: everything that moves on Lagos roads and water: Research for the seeded Blender kit. **Rule zero:** study real Lagos, build our own city. Every real model, operator, union, agency and brand below is a *pattern reference* only. In Gidi, invent the liveries, names, logos, plates and slogans; describe makes only as body shapes ("1980s boxy rear-engine van", "bonneted American-style tractor").
For: rear, occupants, black, street-research, mapping, select, white, dimensions. Last changed 2026-10-14, 1288 lines.
Links to 1: `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/LAGOS-LOOK.md`), 1 code files (`gidi:legacy/blender/gidi_kit/vehicles.py`).
Nearest in words: `gidi:docs/look/research-street.md` (0.53); `gidi:docs/look/research-transport.md` (0.44); `gidi:docs/look/research-commerce.md` (0.39).

## gidi:docs/map-format-example
### `gidi:docs/map-format-example/README.md`
**Worked example of the new map format**. Worked example of the new map format: One short home street in district d15 (20 m, invented names), written as the map would hold it (docs/MAP-FORMAT.md):
For: lean-to's, lean-to, gutter's, shop-under-flats, bungalow's, example, stamped, pothole. Last changed 2026-10-22, 10 lines.
Links to 6: `gidi:docs/MAP-FORMAT.md`, `gidi:docs/map-format-example/d15/district.json`, `gidi:docs/map-format-example/d15/dress/128_60.json`, `gidi:docs/map-format-example/d15/plan.json`, `gidi:schema/kit_reads.json`, `gidi:scripts/check_map.py`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:docs/MAP-FORMAT.md` (0.26); `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.14); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.14).

## gidi:docs
### `gidi:docs/maze-pattern-study.md`
**Maze pattern study: Mushin + Shomolu → The Maze (v2)**. Maze pattern study: Mushin + Shomolu → The Maze (v2): Status: v2, regenerated with the current generator for review (13 Oct 2026). v1 was the first build; section 5 compares the two. Method: **Option 2.** We measure the real place, turn the numbers into rules, and generate original streets and houses from the rules. **No real street or building geometry is copied into Gidi.** Data: OpenStreetMap (ODbL), Lagos extract, plus building heights, people, tree cover and terrain from `data/results/lga_table.json`. Area studied: Mushin + Shomolu LGAs, 33.7 km².
For: maze, adeleke, median, gateways, mushin, crossings, shomolu, track. Last changed 2026-10-16, 254 lines.
Links to 17: `gidi:data/results/lga_table.json`, `gidi:docs/img/maze-vs-real.png`, `gidi:scripts/bake_web.py`, `gidi:scripts/build_viewer.py`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/draw_gen.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py` ...
Backlinks: 2 documents (`gidi:docs/DISTRICT-BRIEF.md`, `gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/jungle-pattern-study.md` (0.49); `gidi:docs/hub-pattern-study.md` (0.43); `gidi:docs/foodgate-pattern-study.md` (0.38).

### `gidi:docs/oldisland-pattern-study.md`
**Old Island pattern study: Lagos Island → Old Island (v1)**. Old Island pattern study: Lagos Island → Old Island (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: island, island's, core's, fountains, bridge's, waterfront, x-junctions, core. Last changed 2026-10-14, 143 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/oldisland-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/heights-pattern-study.md` (0.35); `gidi:docs/oldshore-pattern-study.md` (0.33); `gidi:docs/estate-pattern-study.md` (0.31).

### `gidi:docs/oldshore-pattern-study.md`
**Old Shore pattern study: old Ikorodu → Old Shore (v1)**. Old Shore pattern study: old Ikorodu → Old Shore (v1): Status: generated for review (15 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: shore, jetty, ikorodu's, ikorodu, pins, ferry, fish, town. Last changed 2026-10-15, 145 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/oldshore-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_boxheights.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/living-test-2026-10-14k.md` (0.49); `gidi:docs/living-test-2026-10-15m.md` (0.36); `gidi:docs/oldisland-pattern-study.md` (0.33).

### `gidi:docs/pilot-foodgate.md`
**The Food Gate pilot: the first district rebuilt from Google's data**. The Food Gate pilot: the first district rebuilt from Google's data: Built 15 Oct 2026, from the plan in `docs/REBUILD-PLAN.md`. Food Gate is the test of whether moving from OpenStreetMap to Google's data was worth it, before the other districts and the new ones follow.
For: google's, outlines, furniture, walkways, generator's, pilot, widths, rafts. Last changed 2026-10-24, 48 lines.
Links to 10: `gidi:docs/KIT-GAPS.md`, `gidi:docs/REBUILD-PLAN.md`, `gidi:docs/data/structure-foodgate.json`, `gidi:docs/img/pilot-foodgate-2d.png`, `gidi:scripts/check_district.py`, `gidi:scripts/cross_sections.py`, `gidi:scripts/furniture.py`, `gidi:scripts/structure.py`, `gidi:scripts/study_structure.py`, `gidi:web/terrain-edits.json`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 1 code files (`gidi:scripts/deep_profile.py`).
Nearest in words: `gidi:docs/REBUILD-PLAN.md` (0.3); `gidi:docs/KIT-GAPS.md` (0.2); `gidi:docs/BOARD.md` (0.19).

### `gidi:docs/port-pattern-study.md`
**The Port pattern study: Apapa → The Port (v1)**. The Port pattern study: Apapa → The Port (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: port, apapa, quay, yard, yards, container, farm, reserve. Last changed 2026-10-14, 128 lines.
Links to 12: `gidi:data/results/lga_table.json`, `gidi:docs/img/port-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:web/gen-port.json`, `gidi:web/network.json`
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/bazaar-pattern-study.md` (0.33); `gidi:docs/living-test-2026-10-14c.md` (0.31); `gidi:docs/watertown-pattern-study.md` (0.28).

### `gidi:docs/railside-pattern-study.md`
**Railside pattern study: Agege, Ifako/Ijaye and Alimosho → Railside (v1)**. Railside pattern study: Agege, Ifako/Ijaye and Alimosho → Railside (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: lgas, railside, capital's, landmarks, median, pipeline, sprawl, mounds. Last changed 2026-10-14, 125 lines.
Links to 14: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/railside-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_isms.py`, `gidi:scripts/study_landmarks.py` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.41); `gidi:docs/bazaar-pattern-study.md` (0.37); `gidi:docs/estate-pattern-study.md` (0.34).

## gidi:docs/research
### `gidi:docs/research/LIFE-IN-LAGOS.md`
**Life in Lagos: what it's like to live there**. Life in Lagos: what it's like to live there: A research pass, 16 Oct 2026, for the owner's ask: "immerse yourself in what it's like to live in Lagos".
For: japa, guardian, what's, december, true, feels, rent, power. Last changed 2026-10-16, 329 lines.
Links to 4: `gidi:decisions/DECISIONS.md`, `gidi:decisions/world-life.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/LAGOS-LOOK.md`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/world-life.md`, `gidi:docs/lagos-study/LIVING.md`), 0 code files ().
Nearest in words: `gidi:decisions/world-life.md` (0.28); `gidi:docs/lagos-lgas-research.md` (0.24); `gidi:decisions/lived-in.md` (0.15).

## gidi:docs
### `gidi:docs/road-heights.md`
**Road heights (pass 2 of the road work)**. Road heights (pass 2 of the road work): Status: built 15 Oct 2026. `scripts/roadz.py` runs inside the bake, right after the road clean-up (`scripts/roadclean.py`).
For: deck, ramp, headroom, culverts, deck's, approaches, cable, piers. Last changed 2026-10-23, 87 lines.
Links to 8: `gidi:docs/img/bridge-landings.png`, `gidi:docs/img/road-heights.png`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:scripts/check_district.py`, `gidi:scripts/roadclean.py`, `gidi:scripts/roadz.py`, `gidi:web/terrain.json`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 1 code files (`gidi:legacy/blender/city.py`).
Nearest in words: `gidi-data:research/google/video1-street/NOTES.md` (0.22); `gidi:docs/look/research-transport.md` (0.18); `gidi:docs/living-test-2026-10-15n.md` (0.17).

## gidi:docs/studies
### `gidi:docs/studies/airport.md`
**The Airport: the deep study**. The Airport: the deep study: Inspired by Murtala Muhammed International Airport, Ikeja. Study area: 15.81 km², 15.81 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: airport, median, touching, storeys, transit, service, tenth, restaurant. Last changed 2026-10-15, 126 lines.
Links to 2: `gidi:docs/img/study-airport.png`, `gidi:scripts/study_deep.py`
Backlinks: 0 documents (), 0 code files ().
Nearest in words: `gidi:docs/studies/estate.md` (0.8); `gidi:docs/studies/heights.md` (0.77); `gidi:docs/studies/hub.md` (0.77).

### `gidi:docs/studies/bazaar.md`
**The Bazaar: the deep study**. The Bazaar: the deep study: Inspired by Ojo (electronics market) + Trade Fair. Study area: 21.78 km², 21.49 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, power, touching, storeys, tenth, education, energy, transit. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-bazaar.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.85); `gidi:docs/studies/foodgate.md` (0.83); `gidi:docs/studies/railside.md` (0.82).

### `gidi:docs/studies/border.md`
**The Border: the deep study**. The Border: the deep study: Inspired by Badagry. Study area: 24.72 km², 20.74 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, tenth, roman, squares, land, power. Last changed 2026-10-15, 125 lines.
Links to 2: `gidi:docs/img/study-border.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/foodgate.md` (0.81); `gidi:docs/studies/oldshore.md` (0.8); `gidi:docs/studies/jungle.md` (0.79).

### `gidi:docs/studies/capital.md`
**The Capital: the deep study**. The Capital: the deep study: Inspired by Ikeja. Study area: 15.64 km², 15.64 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, developed, power, touching, storeys, tenth, service, squares. Last changed 2026-10-15, 125 lines.
Links to 2: `gidi:docs/img/study-capital.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.88); `gidi:docs/studies/estate.md` (0.86); `gidi:docs/studies/maze.md` (0.86).

### `gidi:docs/studies/estate.md`
**The Estate: the deep study**. The Estate: the deep study: Inspired by Magodo, Omole, Ikeja GRA. Study area: 24.26 km², 24.21 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, tenth, barrier, service, transportation, squares. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-estate.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.88); `gidi:docs/studies/capital.md` (0.86); `gidi:docs/studies/oldshore.md` (0.86).

### `gidi:docs/studies/foodgate.md`
**Food Gate: the deep study**. Food Gate: the deep study: Inspired by Kosofe (Mile 12, Ketu, Ojota). Study area: 19.24 km², 19.2 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, power, developed, tenth, religious, transit. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-foodgate.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.9); `gidi:docs/studies/port.md` (0.86); `gidi:docs/studies/hub.md` (0.86).

### `gidi:docs/studies/frontier.md`
**The Frontier: the deep study**. The Frontier: the deep study: Inspired by Lekki + Ibeju-Lekki. Study area: 91.01 km², 88.92 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, barrier, tenth, power, squares, land. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-frontier.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.89); `gidi:docs/studies/maze.md` (0.86); `gidi:docs/studies/heights.md` (0.86).

### `gidi:docs/studies/heights.md`
**The Heights: the deep study**. The Heights: the deep study: Inspired by Ikoyi, VI, Banana Island. Study area: 19.09 km², 16.99 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, service, tenth, barrier, historic, squares. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-heights.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/frontier.md` (0.86); `gidi:docs/studies/estate.md` (0.83); `gidi:docs/studies/capital.md` (0.82).

### `gidi:docs/studies/hub.md`
**The Hub: the deep study**. The Hub: the deep study: Inspired by Oshodi + Ojuelegba (Surulere). Study area: 64.56 km², 64.5 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: transit, median, touching, storeys, transportation, tenth, squares, land. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-hub.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/estate.md` (0.88); `gidi:docs/studies/port.md` (0.88); `gidi:docs/studies/oldshore.md` (0.88).

### `gidi:docs/studies/jungle.md`
**Jungle City: the deep study**. Jungle City: the deep study: Inspired by Ajegunle + Festac. Study area: 11.93 km², 11.85 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, communication, tenth, power, transit, squares. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-jungle.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/frontier.md` (0.84); `gidi:docs/studies/oldshore.md` (0.83); `gidi:docs/studies/hub.md` (0.83).

### `gidi:docs/studies/maze.md`
**The Maze: the deep study**. The Maze: the deep study: Inspired by Mushin + Shomolu. Study area: 33.66 km², 32.92 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, tenth, power, transit, dealer, transportation. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-maze.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.87); `gidi:docs/studies/frontier.md` (0.86); `gidi:docs/studies/capital.md` (0.86).

### `gidi:docs/studies/oldisland.md`
**Old Island: the deep study**. Old Island: the deep study: Inspired by Lagos Island. Study area: 9.38 km², 5.9 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: recreation, median, service, touching, storeys, travel, tenth, pedestrian. Last changed 2026-10-15, 125 lines.
Links to 2: `gidi:docs/img/study-oldisland.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.81); `gidi:docs/studies/estate.md` (0.81); `gidi:docs/studies/capital.md` (0.8).

### `gidi:docs/studies/oldshore.md`
**Old Shore: the deep study**. Old Shore: the deep study: Inspired by Ikorodu + Epe. Study area: 20.35 km², 19.82 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, power, tenth, religious, transit, squares. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-oldshore.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/foodgate.md` (0.9); `gidi:docs/studies/frontier.md` (0.89); `gidi:docs/studies/hub.md` (0.88).

### `gidi:docs/studies/port.md`
**The Port: the deep study**. The Port: the deep study: Inspired by Apapa + Mile 2 + the prison. Study area: 26.96 km², 19.36 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, storeys, pier, tenth, power, transit, transportation. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-port.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.88); `gidi:docs/studies/foodgate.md` (0.86); `gidi:docs/studies/oldshore.md` (0.86).

### `gidi:docs/studies/railside.md`
**Railside: the deep study**. Railside: the deep study: Inspired by Agege + Ifako-Ijaiye + Alimosho. Study area: 215.35 km², 215.35 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: power, median, touching, storeys, tenth, squares, land, beauty. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-railside.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.87); `gidi:docs/studies/capital.md` (0.85); `gidi:docs/studies/hub.md` (0.84).

### `gidi:docs/studies/watertown.md`
**Water Town: the deep study**. Water Town: the deep study: Inspired by Makoko + Bariga + Agboyi + the sawmill. Study area: 7.27 km², 5.45 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, christian, storeys, tenth, education, power, venue. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-watertown.png`, `gidi:scripts/study_deep.py`
Backlinks: 1 documents (`gidi:docs/audit/README.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/yaba.md` (0.85); `gidi:docs/studies/oldshore.md` (0.85); `gidi:docs/studies/frontier.md` (0.85).

### `gidi:docs/studies/yaba.md`
**Saba: the deep study**. Saba: the deep study: Inspired by Yaba and Akoka: the university, Sabo, Ojuelegba. Study area: 12.88 km², 10.64 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: median, touching, education, storeys, service, tenth, financial, transportation. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:docs/img/study-yaba.png`, `gidi:scripts/study_deep.py`
Backlinks: 0 documents (), 1 code files (`gidi:scripts/district_profiles.py`).
Nearest in words: `gidi:docs/studies/maze.md` (0.86); `gidi:docs/studies/hub.md` (0.85); `gidi:docs/studies/watertown.md` (0.85).

## gidi:docs
### `gidi:docs/terrain.md`
**Gidi terrain (v1, for review)**. Gidi terrain (v1, for review): The ground under the whole map, `web/terrain.json`: a 40 m grid in decimetres, made by `scripts/terrain.py`. The review picture is made by `scripts/draw_terrain.py`.
For: smoothing, ridges, ridge, valleys, area's, raises, features, edits. Last changed 2026-10-15, 55 lines.
Links to 5: `gidi:docs/img/terrain.png`, `gidi:scripts/draw_terrain.py`, `gidi:scripts/terrain.py`, `gidi:web/terrain-edits.json`, `gidi:web/terrain.json`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:docs/LAGOS-ISMS.md` (0.15); `gidi:docs/oldshore-pattern-study.md` (0.14); `gidi:docs/data/deep-check/SUMMARY.md` (0.13).

### `gidi:docs/watertown-pattern-study.md`
**Water Town pattern study: the Makoko–Iwaya and Bariga waterfront → Water Town (v1)**. Water Town pattern study: the Makoko–Iwaya and Bariga waterfront → Water Town (v1): Status: generated for review (13 Oct 2026; v2 the same day: the land is rebuilt as fingers running down to the shore). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets, houses and stilt houses from the rules. **No real street, building or name is copied into Gidi.**
For: fingers, stilt, huts, sawmill's, canoe, village, land, boardwalks. Last changed 2026-10-14, 164 lines.
Links to 16: `gidi:data/results/lga_table.json`, `gidi:docs/img/watertown-fingers.png`, `gidi:docs/img/watertown-vs-real.png`, `gidi:scripts/check_district.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_analyse.py`, `gidi:scripts/study_connect.py`, `gidi:scripts/study_core.py`, `gidi:scripts/study_extract.py`, `gidi:scripts/study_landmarks.py`, `gidi:study-mainland-shomolu-landmarks.json` ...
Backlinks: 1 documents (`gidi:legacy/OLD-MAP.md`), 0 code files ().
Nearest in words: `gidi:docs/port-pattern-study.md` (0.28); `gidi:docs/living-test-2026-10-13c.md` (0.26); `gidi:docs/maze-pattern-study.md` (0.25).

## gidi:legacy
### `gidi:legacy/OLD-MAP.md`
**The old map (13-21 Oct 2026): what it was**. The old map (13-21 Oct 2026): what it was: The first Gidi: 15, then 17, invented districts generated from patterns measured in real Lagos (OpenStreetMap, then Google's data), baked into `web/gidi-data.js`, hand-edited in `web/hand/`, styled by the Blender kit in `legacy/blender/`. On 22 Oct the owner restarted the map as real Lagos miniaturised (decisions/DECISIONS.md); this
For: statistics, banned, generated, okadas, gateways, stadiums, extract, island. Last changed 2026-10-24, 52 lines.
Links to 44: `gidi:data/results/lga_table.json`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/CITY-LIVING-TEST.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/LAGOS-LOOK.md`, `gidi:docs/bazaar-pattern-study.md`, `gidi:docs/border-pattern-study.md`, `gidi:docs/capital-pattern-study.md`, `gidi:docs/estate-pattern-study.md` ...
Backlinks: 2 documents (`gidi:README.md`, `gidi:legacy/README.md`), 0 code files ().
Nearest in words: `gidi:docs/heights-pattern-study.md` (0.25); `gidi:docs/DISTRICT-BRIEF.md` (0.25); `gidi:docs/LAGOS-ISMS.md` (0.25).

### `gidi:legacy/README.md`
**Legacy: the old map's kit (frozen)**. Legacy: the old map's kit (frozen): What the old map was and its parts: `OLD-MAP.md`.
For: tiles, frozen, tab's, fields, builder, legacy, old-town, builders. Last changed 2026-10-24, 14 lines.
Links to 5: `gidi:docs/MAP-FORMAT.md`, `gidi:legacy/OLD-MAP.md`, `gidi:legacy/blender/city.py`, `gidi:schema/map_schema.json`, `gidi:web/gidi-data.js`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/DISTRICT-BRIEF.md`, `gidi:docs/ISMS-BUILD.md`), 1 code files (`gidi:scripts/audit3d.py`).
Nearest in words: `gidi:decisions/CODEBASE.md` (0.22); `gidi:decisions/NOW.md` (0.2); `gidi:CLAUDE.md` (0.19).

## gidi:map/d15
### `gidi:map/d15/BUILDINGS.md`
**Mùṣá: the buildings draft and its hand pass**. Mùṣá: the buildings draft and its hand pass: Drafted by `scripts/draft_buildings.py` (owner, 23 Oct: real footprints, then hand). 1457 houses in 41 blocks. Each block's number is its place in size order. After the run, 31 houses that crossed the district line were taken out (the tool now keeps only houses wholly inside), leaving 1426; the counts below are from before that.
For: redrafted, hand, pass, lanes, twin's, redrawn, close-zoom, cleared. Last changed 2026-10-24, 143 lines.
Links to 2: `gidi:map/d15/STREETS.md`, `gidi:scripts/draft_buildings.py`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi:scripts/draft_buildings.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.19); `gidi:decisions/DECISIONS.md` (0.13); `gidi:map/d15/STREETS.md` (0.09).

### `gidi:map/d15/STREETS.md`
**Mùṣá (district 15): the road plan and where each street comes from**. Mùṣá (district 15): the road plan and where each street comes from: Roads only, drawn on the new frame (1:3). Every kept street sits on its real line, squeezed to the frame, at its real width (never shrunk). Real names live here only, never in the map. Buildings come later.
For: repeats, lane, nearby, parallel, missing, twin, alhaji, home. Last changed 2026-10-24, 536 lines.
Links to 0: 
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`, `gidi:map/d15/BUILDINGS.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.15); `gidi-data:research/google/ibudo/study/INVENTORY.md` (0.13); `gidi:decisions/NOW.md` (0.12).

