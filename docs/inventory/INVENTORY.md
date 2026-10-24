# Inventory of the three repos

Made by `scripts/inventory.py` (gidi): every git-tracked file in gidi, gidi-game and Real-world. "Refs" is how many other files name it (imports, links, mentions). Binary files are counted per folder. Run it again to refresh; do not edit by hand.

## gidi

604 files.

### gidi/.

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `.gitignore` | 14 | 2026-10-23 | 4 |  |
| `CLAUDE.md` | 16 | 2026-10-23 | 28 | Gidi: An open-world city inspired by Lagos, built from data and by hand. The owner works across more than one Claude account. |
| `README.md` | 32 | 2026-10-23 | 9 | Gidi: The city for an open-world game: Gidi is real Lagos miniaturised, 51 districts, each street and place drawn by hand from the real one. This repo is the m… |

Data: 86 files, 0.3 MB (.json); unpointed: 80.

### gidi/data

Data: 1 files, 0.0 MB (.geojson); unpointed: 0.

### gidi/data/results

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `heights.py` | 33 | 2026-10-13 | 3 | Per-LGA building height stats from Google Open Buildings 2.5D (2023), read at ~4 m (the data's effective resolution). |
| `landpop.py` | 43 | 2026-10-13 | 1 | Per-LGA land cover (ESA WorldCover 2021), surface height (Copernicus DSM), population (WorldPop 2020). |

Data: 2 files, 0.0 MB (.json); unpointed: 0.

### gidi/data/tools

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `probe-tiles.sh` | 6 | 2026-10-13 | 0 | Reads only the first 128 KB of each height tile (its location), so we can skip tiles outside Lagos. Takes about a minute. |
| `pull-data.sh` | 22 | 2026-10-13 | 2 | Gidi data pull. Run on the Mac (Terminal): bash ~/Real-world/research/data/pull-data.sh Downloads open datasets for the Lagos study into this folder. Safe to s… |

### gidi/decisions

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `CHECKS.md` | 99 | 2026-10-23 | 4 | Which check holds each rule: Every rule in `DECISIONS.md` has a row here: the check that enforces it, or why none can. `scripts/check_rules.py` runs with every… |
| `DECISIONS.md` | 134 | 2026-10-24 | 12 | Decisions (the owner's; newest first): - **The story: Tunde's** (15 Oct 2026). The owner's confirmed story points live in `decisions/story/acts-2-3-draft.md`: … |
| `IDEAS.md` | 73 | 2026-10-24 | 4 | Ideas (not decided; newest first): - **Our own Lagos motion from video, and AI video** (owner, 23 Oct). Motion2MixamoRig (github.com/MaxLiu22/Motion2MixamoRig,… |
| `NOW.md` | 272 | 2026-10-24 | 4 | Where the work stands (update at the end of every session): **HANDOVER, 22 Oct 2026 ~23:00 (owner switching Claude accounts). Start here.** State: the new map … |
| `README.md` | 9 | 2026-10-15 | 9 | Decisions and ideas: The owner works across more than one Claude account. This folder is the shared memory: **read it first in every session**, and add to it w… |
| `lived-in.md` | 154 | 2026-10-24 | 4 | The lived-in layer: what every GTA does, and Gidi's plan: The owner asked on 24 Oct 2026 for research from public material on how GTA's worlds feel alive, acro… |
| `world-life.md` | 146 | 2026-10-16 | 4 | Life in Gidi: what makes the world feel like it exists: The owner's thinking from 16 Oct 2026, and Claude's proposals. The research behind it: `docs/research/L… |

### gidi/decisions/story

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `README.md` | 22 | 2026-10-15 | 9 | The story of Gidi: Tunde, an okada rider, in debt to the boss who runs the motor park. The city opens in three acts: Survive, Hustle, Empire (`docs/gidi-distri… |
| `act-1-draft.md` | 109 | 2026-10-16 | 4 | Gidi Act 1: draft (the owner's outline, 15 Oct 2026, with Claude's notes): **Status:** a draft for the story pass, stage 3 of `gidi-roadmap.md` (not in this re… |
| `acts-2-3-draft.md` | 77 | 2026-10-15 | 3 | Gidi Acts 2 and 3: working draft (updated 15 Oct 2026 after the owner's feedback): Builds on `act-1-draft.md`. The owner didn't like the pacing of Claude's fir… |
| `novels/1-the-ledger.md` | 127 | 2026-10-15 | 1 | 1. The Ledger: *Claude's draft, 15 Oct 2026. It builds on the owner's confirmed story (`../act-1-draft.md`, `../acts-2-3-draft.md`) and adds people.* |
| `novels/2-union.md` | 75 | 2026-10-15 | 1 | 2. Union: *Claude's draft, 15 Oct 2026. It keeps the owner's Act 1 (the steal, the boss's rescue, the okada on hire purchase, the robbery), then gives the city… |
| `novels/3-the-phone.md` | 79 | 2026-10-15 | 1 | 3. The Phone: *Claude's draft, 15 Oct 2026. It keeps the owner's Act 1 (the steal, the rescue, the okada on hire purchase), then turns the open world into a th… |
| `novels/README.md` | 36 | 2026-10-15 | 9 | Three stories for Gidi (Claude's drafts, 15 Oct 2026, for the owner to pick from): The owner asked for "two or three novels of the story" to read, pick from, a… |

### gidi/docs

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `BOARD.md` | 98 | 2026-10-22 | 2 | The drawing board: The owner, 16 Oct 2026: "we should hand draw... we should know where something meets something... where the roads start, where the roads end… |
| `CITY-LIVING-TEST.md` | 184 | 2026-10-16 | 6 | City living test: Haiku agents live in Gidi and report how moving around feels: Run this after every district is merged, and after any fix to roads, paths, rai… |
| `DATA-SOURCES.md` | 31 | 2026-10-15 | 3 | Data sources, and what to delete later: Everything we've downloaded to study real Lagos lives on Daramola's Mac in `~/Real-world/research/data/` (about 20 GB, … |
| `DEEP-STUDY.md` | 65 | 2026-10-16 | 8 | The deep study: every district's inspiration, from all the data: The owner asked for this on 15 Oct 2026: "the research should look at everything in the data a… |
| `DISTRICT-BRIEF.md` | 101 | 2026-10-24 | 2 | Brief: build one Gidi district: One session = one district. Read this brief, `README.md` and `docs/maze-pattern-study.md` (the worked example), then do the ste… |
| `FLOW-AUDIT.md` | 27 | 2026-10-22 | 1 | City flow audit, 22 Oct 2026: Read-only: Gidi's frame (`web/layout-v2.json`, border roads in `web/network.json`, baked mains) against real Lagos's big roads (O… |
| `ISMS-BUILD.md` | 118 | 2026-10-23 | 3 | Building the Lagos-isms: what exists, what's missing, and the prompt: The "feel like Lagos" pass. All fifteen districts are built from measured patterns. Now t… |
| `KIT-GAPS.md` | 56 | 2026-10-19 | 9 | Kit gaps: things the map now has that the 3D kit can't draw well yet: Started 15 Oct 2026 with the Food Gate pilot (`docs/REBUILD-PLAN.md`). Each line: what th… |
| `LAGOS-ISMS.md` | 276 | 2026-10-23 | 19 | Lagos-isms: the eccentricities in the real data (a running log): **What this is.** While each district is studied, we log the real places' oddities: the things… |
| `LAGOS-LIGHT.md` | 61 | 2026-10-15 | 1 | Lagos light: why the city looks different: The owner's observation: photos taken in Nigeria look different from photos taken abroad. The vibrancy and the feel … |
| `LAGOS-LOOK.md` | 167 | 2026-10-23 | 3 | The Lagos look: a seeded Blender kit that styles Gidi from its data: **What this is.** Everything in Gidi gets its look from what the map data already knows ab… |
| `LAYOUT-V2.md` | 82 | 2026-10-16 | 7 | Gidi v2: the layout: Chosen by the owner on 15 Oct 2026: a fictional Lagos with its real shape first, our own twists after. The first map (8.8 × 6.7 km) was bo… |
| `MAP-FORMAT.md` | 598 | 2026-10-24 | 14 | The new map's data format (draft 0.1, for the owner to approve): The new map is the one ground truth (decisions, 22 Oct: "everything that we do must be in map … |
| `REBUILD-PLAN.md` | 39 | 2026-10-15 | 6 | Rebuilding Gidi from Google's data: Decided 15 Oct 2026. The first fifteen districts were measured from OpenStreetMap, so they inherited what OSM happened to m… |
| `TWINS.md` | 283 | 2026-10-19 | 3 | Real twins: every type in Gidi and the real thing it comes from: Made by `python3 scripts/twins.py` from the map and `web/twins.json` (the twins, kept by hand)… |
| `UNREAL-PORT-PLAN.md` | 56 | 2026-10-23 | 3 | Unreal port plan: Agreed with the owner on 15 Oct 2026. |
| `bazaar-pattern-study.md` | 125 | 2026-10-14 | 0 | The Bazaar pattern study: Ojo round the electronics market → The Bazaar (v1): Status: generated for review (14 Oct 2026). Same method as every district: we mea… |
| `border-pattern-study.md` | 137 | 2026-10-15 | 0 | Border pattern study: Badagry → the Border (v1): Status: generated for review (15 Oct 2026). Same method as every district: we measure the real place, turn the… |
| `capital-pattern-study.md` | 159 | 2026-10-14 | 1 | The Capital pattern study: central Ikeja → The Capital (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real pla… |
| `estate-pattern-study.md` | 141 | 2026-10-14 | 0 | Estate pattern study: Ikeja GRA, Magodo and Omole → the Estate (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the … |
| `foodgate-pattern-study.md` | 172 | 2026-10-14 | 0 | Food Gate pattern study: Ojota–Ketu–Mile 12 (Kosofe) → Food Gate (v1): Status: generated for review (13 Oct 2026). Same method as the other districts: we measu… |
| `frontier-pattern-study.md` | 177 | 2026-10-14 | 0 | Frontier pattern study: the Lekki peninsula → the Frontier (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real… |
| `gidi-data-plan.md` | 186 | 2026-10-13 | 1 | Gidi data plan: everything we need to build accurate districts (v1, 13 Oct 2026): **Rule:** we study real Lagos to learn its patterns, then build our own world… |
| `gidi-districts-v0.3.md` | 90 | 2026-10-13 | 1 | Gidi: 15 districts (map v0.3): 13 October 2026. Built from the 20-LGA research (`lagos-lgas-research.md`). Places that felt alike were merged into one district… |
| `heights-pattern-study.md` | 208 | 2026-10-14 | 0 | Heights pattern study: Ikoyi, Victoria Island and Banana Island → the Heights (v3): Status: generated for review (14 Oct 2026). Same method as every district: … |
| `hub-pattern-study.md` | 278 | 2026-10-13 | 0 | Hub pattern study: Oshodi/Isolo + Surulere → The Hub (v1): Status: generated for review (13 Oct 2026). Same method as the Maze: we measure the real place, turn… |
| `junctions.md` | 70 | 2026-10-15 | 0 | Junctions (pass 3 of the road work): Status: built 15 Oct 2026. `scripts/junctions.py` runs inside the bake, after the road clean-up and before the road height… |
| `jungle-pattern-study.md` | 246 | 2026-10-14 | 0 | Jungle City pattern study: Ajegunle (+ Festac) → Jungle City (v1): Status: generated for review (13 Oct 2026). Same method as the Maze and the Hub: we measure … |
| `lagos-lgas-research.md` | 2800 | 2026-10-13 | 5 | Lagos, one local government at a time: research for Gidi: 13 October 2026. Twenty researchers, one per local government area (LGA), each asked what makes the p… |
| `living-test-2026-10-13.md` | 108 | 2026-10-13 | 0 | City living test, 13 Oct 2026: the Maze, the Hub, Jungle City: This is the first run of `docs/CITY-LIVING-TEST.md`, done on the whole built city. |
| `living-test-2026-10-13b.md` | 135 | 2026-10-13 | 0 | City living test, 13 Oct 2026 (second run): the Maze, the Hub, Jungle City, Food Gate: This is the second run of `docs/CITY-LIVING-TEST.md` today. It covers th… |
| `living-test-2026-10-13c.md` | 135 | 2026-10-13 | 0 | City living test, 13 Oct 2026 (third run): all five districts: This is the third run of `docs/CITY-LIVING-TEST.md` today. It is the first run with all five bui… |
| `living-test-2026-10-14.md` | 127 | 2026-10-14 | 0 | City living test, 14 Oct 2026: six districts, with the new Capital: This is the test in `docs/CITY-LIVING-TEST.md`, run on the whole built city after the Capit… |
| `living-test-2026-10-14b.md` | 97 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (second run): seven districts, with the new Bazaar: This run tests four changes on this branch: - **The fair block count:** the g… |
| `living-test-2026-10-14c.md` | 71 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (third run): eight districts, with the new Port: There are two states: - **Before:** `main` at the start of this work (commit `19… |
| `living-test-2026-10-14d.md` | 67 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (fourth run): nine districts, with the new Railside: There are two states: - **Before:** `main` at the start of this work (commit… |
| `living-test-2026-10-14e.md` | 68 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (fifth run): ten districts, with the new Estate: There are two states: - **Before:** `main` at the start of this work (commit `22… |
| `living-test-2026-10-14f.md` | 83 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (sixth run): eleven districts, with the new Old Island: There are two states: - **Before:** `main` at the start of this work (com… |
| `living-test-2026-10-14g.md` | 104 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (seventh run): twelve districts, with the new Heights: There are two states: - **Before:** `main` at the start of this work (comm… |
| `living-test-2026-10-14h.md` | 57 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (eighth run): the Heights v2: There are two states: - **Before:** `main` at commit `47b75ef` (the Heights v1). - **After:** this … |
| `living-test-2026-10-14i.md` | 42 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (ninth run): the Heights v3: There are two states: - **Before:** `main` at commit `a679778` (the Heights v2). - **After:** this b… |
| `living-test-2026-10-14j.md` | 66 | 2026-10-14 | 0 | City living test, 14 Oct 2026 (tenth run): thirteen districts, with the new Frontier: There are two states: - **Before:** `main` at commit `10b9708` (twelve di… |
| `living-test-2026-10-14k.md` | 52 | 2026-10-15 | 0 | City living test, 15 Oct 2026 (eleventh run): Old Shore: There are two states: - **Before:** `main` at commit `cf613f8` (thirteen districts). - **After:** this… |
| `living-test-2026-10-14l.md` | 64 | 2026-10-15 | 0 | City living test, 15 Oct 2026: the Border: There are two states: - **Before:** `main` at commit `cf613f8` (thirteen districts). - **After:** this branch: the B… |
| `living-test-2026-10-15-gutters.md` | 31 | 2026-10-15 | 0 | City living test, 15 Oct 2026: open gutters (ism 15, group 1): `scripts/isms.py` now puts open gutters into the city data, with plank and slab crossings at doo… |
| `living-test-2026-10-15m.md` | 30 |  | 0 | City living test, 15 Oct 2026 (twelfth run): all fifteen districts: Old Shore and the Border were built in parallel, on separate branches (living tests 14k and… |
| `living-test-2026-10-15n.md` | 38 | 2026-10-15 | 0 | City living test, 15 Oct 2026: road clean-up, pass 1: The first of four road passes. `scripts/roadclean.py` now runs inside the bake, after every road is gathe… |
| `maze-pattern-study.md` | 254 | 2026-10-16 | 1 | Maze pattern study: Mushin + Shomolu → The Maze (v2): Status: v2, regenerated with the current generator for review (13 Oct 2026). v1 was the first build; sect… |
| `oldisland-pattern-study.md` | 143 | 2026-10-14 | 0 | Old Island pattern study: Lagos Island → Old Island (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place,… |
| `oldshore-pattern-study.md` | 145 | 2026-10-15 | 0 | Old Shore pattern study: old Ikorodu → Old Shore (v1): Status: generated for review (15 Oct 2026). Same method as every district: we measure the real place, tu… |
| `pilot-foodgate.md` | 48 | 2026-10-15 | 1 | The Food Gate pilot: the first district rebuilt from Google's data: Built 15 Oct 2026, from the plan in `docs/REBUILD-PLAN.md`. Food Gate is the test of whethe… |
| `port-pattern-study.md` | 128 | 2026-10-14 | 0 | The Port pattern study: Apapa → The Port (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the n… |
| `railside-pattern-study.md` | 125 | 2026-10-14 | 0 | Railside pattern study: Agege, Ifako/Ijaye and Alimosho → Railside (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure … |
| `road-heights.md` | 87 | 2026-10-23 | 1 | Road heights (pass 2 of the road work): Status: built 15 Oct 2026. `scripts/roadz.py` runs inside the bake, right after the road clean-up (`scripts/roadclean.p… |
| `terrain.md` | 55 | 2026-10-15 | 0 | Gidi terrain (v1, for review): The ground under the whole map, `web/terrain.json`: a 40 m grid in decimetres, made by `scripts/terrain.py`. The review picture … |
| `watertown-pattern-study.md` | 164 | 2026-10-14 | 0 | Water Town pattern study: the Makoko–Iwaya and Bariga waterfront → Water Town (v1): Status: generated for review (13 Oct 2026; v2 the same day: the land is reb… |

Binary: 1 files, 0.3 MB (1 .png).

### gidi/docs/audit

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `README.md` | 24 | 2026-10-15 | 9 | 3D audit, all districts: Each district has its own page here with the details. Rerun with `.venv/bin/python scripts/audit3d.py`. |
| `bazaar.md` | 26 | 2026-10-15 | 1 | 3D audit: The Bazaar: `.venv/bin/python scripts/audit3d.py bazaar` writes this. The checks are listed in the script. Coordinates are map metres (x east, y sout… |
| `border.md` | 24 | 2026-10-15 | 1 | 3D audit: The Border: `.venv/bin/python scripts/audit3d.py border` writes this. The checks are listed in the script. Coordinates are map metres (x east, y sout… |
| `capital.md` | 25 | 2026-10-15 | 1 | 3D audit: The Capital: `.venv/bin/python scripts/audit3d.py capital` writes this. The checks are listed in the script. Coordinates are map metres (x east, y so… |
| `estate.md` | 25 | 2026-10-15 | 1 | 3D audit: The Estate: `.venv/bin/python scripts/audit3d.py estate` writes this. The checks are listed in the script. Coordinates are map metres (x east, y sout… |
| `foodgate.md` | 28 | 2026-10-15 | 1 | 3D audit: Food Gate: `.venv/bin/python scripts/audit3d.py foodgate` writes this. The checks are listed in the script. Coordinates are map metres (x east, y sou… |
| `frontier.md` | 31 | 2026-10-15 | 1 | 3D audit: The Frontier: `.venv/bin/python scripts/audit3d.py frontier` writes this. The checks are listed in the script. Coordinates are map metres (x east, y … |
| `heights.md` | 29 | 2026-10-15 | 1 | 3D audit: The Heights: `.venv/bin/python scripts/audit3d.py heights` writes this. The checks are listed in the script. Coordinates are map metres (x east, y so… |
| `hub.md` | 25 | 2026-10-15 | 1 | 3D audit: The Hub: `.venv/bin/python scripts/audit3d.py hub` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south). |
| `jungle.md` | 26 | 2026-10-15 | 1 | 3D audit: Jungle City: `.venv/bin/python scripts/audit3d.py jungle` writes this. The checks are listed in the script. Coordinates are map metres (x east, y sou… |
| `maze.md` | 25 | 2026-10-15 | 1 | 3D audit: The Maze: `.venv/bin/python scripts/audit3d.py maze` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south). |
| `oldisland.md` | 32 | 2026-10-15 | 1 | 3D audit: Old Island: `.venv/bin/python scripts/audit3d.py oldisland` writes this. The checks are listed in the script. Coordinates are map metres (x east, y s… |
| `oldshore.md` | 32 | 2026-10-15 | 1 | 3D audit: Old Shore: `.venv/bin/python scripts/audit3d.py oldshore` writes this. The checks are listed in the script. Coordinates are map metres (x east, y sou… |
| `port.md` | 27 | 2026-10-15 | 1 | 3D audit: The Port: `.venv/bin/python scripts/audit3d.py port` writes this. The checks are listed in the script. Coordinates are map metres (x east, y south). |
| `railside.md` | 33 | 2026-10-15 | 1 | 3D audit: Railside: `.venv/bin/python scripts/audit3d.py railside` writes this. The checks are listed in the script. Coordinates are map metres (x east, y sout… |
| `watertown.md` | 25 | 2026-10-15 | 1 | 3D audit: Water Town: `.venv/bin/python scripts/audit3d.py watertown` writes this. The checks are listed in the script. Coordinates are map metres (x east, y s… |

### gidi/docs/data

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `deep-check/SUMMARY.md` | 22 | 2026-10-16 | 0 | Each cell is Gidi against its real inspiration (0% = the same; ⚠ = more than 20% off). "Squares" = built 500 m squares measured (under 5: a small sample). |

Data: 36 files, 0.3 MB (.json); unpointed: 30.

### gidi/docs/hand

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `borrowed-lagos.md` | 72 | 2026-10-23 | 6 | Borrowed from Lagos: real places reimagined in Gidi (16 Oct 2026): The owner's direction: "take inspiration from the places to build the area... also from plac… |
| `ibudo/README.md` | 19 | 2026-10-19 | 9 | Ìbùdó, spot 1: the market road under the Ring Road flyover (design v1, 19 Oct): Oshodi, studied on Google Earth and Street View (`~/Real-world/research/google/… |
| `ibudo/child_plan.md` | 32 | 2026-10-20 | 1 | Ìbùdó plan v3, the child of Oshodi and Ojuelegba (owner, 19 Oct 2026). Each area is a real place set down at true scale (1 m = 1 m, north up): a real point (an… |
| `lagos-pass.md` | 52 | 2026-10-19 | 2 | The Lagos pass (owner, 19 Oct): A place in Gidi is "Lagos" only when the owner has looked at it, rendered, and said so. Getting one spot there, all the way, te… |
| `maze-hub-lagos.md` | 53 | 2026-10-16 | 3 | The Maze and the Hub: what makes them unmistakably Lagos (agreed 16 Oct 2026): The first hand-made districts: Act 1 opens here (`decisions/story/act-1-draft.md… |
| `monument-briefs.md` | 30 | 2026-10-19 | 1 | Monuments: what each needs (19 Oct): The owner's rule: Meshy for statues and monuments nobody walks into; structures people walk into or under are built in Ble… |
| `realnames.txt` | 8421 | 2026-10-21 | 6 |  |

Data: 16 files, 0.5 MB (.json); unpointed: 14.

Binary: 6 files, 1.5 MB (6 .png).

### gidi/docs/img

Binary: 59 files, 25.7 MB (53 .png, 6 .jpg).

### gidi/docs/kit

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `MODELLER-BRIEF-ACT1.md` | 40 | 2026-10-23 | 1 | Brief for the kit modeller: the Act 1 gaps: Copy everything below the line into the modeller's session. |

### gidi/docs/lagos-study

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `LIVING.md` | 555 | 2026-10-24 | 3 | Living in each district: the 51, for the brush and the lived-in layer: Study file (24 Oct 2026). Real place names live here and in other study files only, neve… |
| `STUDY.md` | 322 | 2026-10-22 | 5 | How the whole Lagos map works: a study before cutting districts: 22 Oct 2026. Read-only. Asked for by the owner's decision "Gidi is Lagos, miniaturised; the ma… |
| `councils.md` | 212 | 2026-10-22 | 4 | Lagos councils: the 20 LGAs and 37 LCDAs: 22 Oct 2026. Companion to `STUDY.md`. Read-only study; nothing here is a district yet. |
| `roads/EARTH-CHECK.md` | 274 | 2026-10-22 | 5 | Google Earth check of the borders (22 Oct 2026): `ROADS.md` section 6 left 15 borders the data could not settle. Each was looked at on Google Maps satellite (z… |
| `roads/NAMES.md` | 115 | 2026-10-22 | 3 | Echo names for the 51 districts (draft, 22 Oct 2026): Working names for the 51 districts in `EARTH-CHECK.md` ("District list after the checks"), as the map for… |
| `roads/ROADS.md` | 510 | 2026-10-22 | 2 | Roads first, districts by their borders: Step 1 of the new map plan (22 Oct): Gidi is real Lagos made smaller, at 1:3, in a frame about 27 × 10.5 km. This stud… |
| `roads/scripts/borders.py` | 147 | 2026-10-22 | 1 | Every border between two places: what it is, how long, whether built land meets across it; plus each place's fingerprint and the similarity of every pair (the … |
| `roads/scripts/common.py` | 28 | 2026-10-22 | 14 | Shared paths and the 50 m grid. The 50 m grid nests 5 x 5 inside the earlier study's 250 m grid. |
| `roads/scripts/gaz.py` | 238 | 2026-10-22 | 4 | Neighbourhood names for naming places. [K] general knowledge: points are approximate (+-0.5-1 km), not measured. Extends the earlier study's list (docs/lagos-s… |
| `roads/scripts/ladder.py` | 140 | 2026-10-22 | 1 | Join places into districts: only places that really touch (built land meets across 200 m or more of their border) and are alike enough. The Google checks of 22… |
| `roads/scripts/network.py` | 226 | 2026-10-22 | 1 | Measure the skeleton, choose the real extent that fits Gidi's 27 x 10.5 km frame at 1:3, draw it. ---------- 1. the frame: the 81 x 31.5 km real window (27 x 1… |
| `roads/scripts/ob50.py` | 25 | 2026-10-22 | 1 | Open Buildings v3 (confidence >= 0.65) onto the 50 m grid: count and roof area per cell. Streams the 430 MB csv.gz in chunks; keeps only two small grids in mem… |
| `roads/scripts/places.py` | 256 | 2026-10-22 | 3 | Cut Lagos land into places bounded by real borders, on the 50 m grid. Borders: big roads (motorway, trunk, primary), rail, narrow water (canals, creeks), secon… |
| `roads/scripts/plot_places.py` | 56 | 2026-10-22 | 2 | Pictures of the places: coloured pieces, border lines, names. Optional argument: a group label per place (districts). |
| `roads/scripts/report.py` | 116 | 2026-10-22 | 2 | District maps for the chosen thresholds, the old unit pairs that are not real neighbours, and the close calls for Google. ---------- old units: which of the fi… |
| `roads/scripts/skeleton.py` | 70 | 2026-10-22 | 1 | The skeleton: every motorway, trunk, primary and secondary road (with their links), rail, bridges. Overture segments -> skel.pkl (one record per segment, UTM 3… |
| `roads/scripts/wc50.py` | 32 | 2026-10-22 | 1 | ESA WorldCover (10 m) onto the 50 m grid: share of water (80), wetland (90), mangrove (95), built (50), trees (10). Read in strips at ~16 m so memory stays sma… |
| `similar/GOOGLE-CHECK.md` | 31 | 2026-10-22 | 1 | The close calls, checked on Google satellite (22 Oct 2026): The similarity numbers (`SIMILAR.md`) flagged 10 merges as close or doubtful. Each pair was looked … |
| `similar/SIMILAR.md` | 957 | 2026-10-22 | 6 | Which places are alike: numbers for cutting districts: 22 Oct 2026. Read-only study. It gives numbers for how many districts, and which places merge. It does n… |
| `similar/districts.md` | 469 | 2026-10-22 | 2 | At 90%: 81 districts (71 after folding tiny plain units): Rich or distinct units still alone (24): Isale Eko-Idumota-Marina, Ikoyi-Banana Island, Victoria Isla… |
| `similar/scripts/analyse.py` | 101 | 2026-10-22 | 2 | ---- fingerprint vectors ---- neighbours: shared land edge, or across <=750 m of water ---- distinctiveness, richness ---- contiguity-constrained average-linka… |
| `similar/scripts/appendix.py` | 27 | 2026-10-22 | 0 | Appendix A and B of SIMILAR.md (unit fingerprints, neighbour pairs) from analysis.json. |
| `similar/scripts/common.py` | 43 | 2026-10-22 | 14 | Shared by the similarity study's plot scripts: the grids, the units, the LGA lines. Needs the grids in ../lagos/ (feat.npz, class.npz), which were never commit… |
| `similar/scripts/finger.py` | 52 | 2026-10-22 | 1 | Per-unit fingerprint from the 250 m grids + Overture places + knowledge lists. Overture places (confidence >= 0.5) |
| `similar/scripts/know.py` | 86 | 2026-10-22 | 2 | [K] general knowledge, not measured. Per unit: markets ; hubs (motor parks, interchanges, stations, jetties) ; landmarks (campus, port, industry, institutions,… |
| `similar/scripts/plot_units.py` | 25 | 2026-10-22 | 0 | Map of the study units (SIMILAR.md's unit pictures), drawn with common.py. |
| `similar/scripts/plots.py` | 59 | 2026-10-22 | 2 | ---- similarity.png ---- ladder pictures |
| `similar/scripts/report.py` | 31 | 2026-10-22 | 2 | SIMILAR.md's ladder: how many districts at each similarity threshold, from analysis.json. |
| `similar/scripts/seeds.py` | 91 | 2026-10-22 | 2 | Unit seeds: name / lat,lon ; lat,lon ... Coordinates from general knowledge [K], approximate (+-0.5-1 km). A unit = the 250 m cells closest (by road-penalised … |
| `similar/scripts/units.py` | 70 | 2026-10-22 | 1 | Draw units: road- and council-penalised nearest-seed growth over 250 m land cells. fill lga id for gap cells from nearest lga cell big-road raster: motorway / … |

Data: 8 files, 0.5 MB (.csv); unpointed: 0.

Binary: 19 files, 13.0 MB (19 .png).

### gidi/docs/look

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `COVERAGE.md` | 145 | 2026-10-23 | 2 | Kit coverage: everything in Gidi's data, and whether the kit builds it: Made by `python3 legacy/blender/coverage.py` from `web/gen-*.json`, `web/civic.json` an… |
| `research-buildings.md` | 697 | 2026-10-14 | 7 | Lagos buildings and their parts: a catalogue for the Gidi generator: Rule zero: this is pattern research. Nothing here names a building to copy; Gidi invents i… |
| `research-civic.md` | 647 | 2026-10-14 | 1 | Civic and public-service buildings: a catalogue for the Gidi generator: Scope: hospitals, clinics, chemists, police (stations, command, posts, checkpoints, bar… |
| `research-commerce.md` | 883 | 2026-10-16 | 1 | Gidi commerce catalogue: markets, shops, commerce and industry: Purpose: specs for the seeded Blender kit. This builds on `docs/look/research-buildings.md` §6 … |
| `research-housing.md` | 926 | 2026-10-14 | 1 | Lagos housing types beyond the front/back house: a catalogue for the Gidi kit: Scope: every housing type (and the housing-adjacent structures that sit on resid… |
| `research-landmarks.md` | 735 | 2026-10-14 | 3 | Lagos landmarks as patterns: a catalogue for Gidi's invented landmarks: Rule zero applies here more than anywhere else. A landmark is the thing a player will r… |
| `research-leisure.md` | 800 | 2026-10-14 | 1 | Gidi catalogue: education, sport, leisure and nightlife places: This catalogue extends `docs/look/research-buildings.md` and `docs/look/research-street.md`. It… |
| `research-religious.md` | 625 | 2026-10-14 | 1 | Gidi look research: religious buildings and places: Scope: mosques, churches, white-garment churches, prayer camps, storefront worship, roadside prayer spaces,… |
| `research-roads.md` | 1147 | 2026-10-23 | 1 | Gidi ground catalogue: roads in every condition, drains, ground, water, vegetation, refuse: This catalogue covers the honest Lagos: roads that are mud with pot… |
| `research-street.md` | 923 | 2026-10-14 | 11 | Gidi street catalogue: roads, vehicles, people, signage, props: This is research for a procedural generator. It studies real Lagos and describes patterns only.… |
| `research-transport.md` | 886 | 2026-10-14 | 1 | Gidi transport and infrastructure catalogue: Research for the seeded Blender kit. Rule zero applies: real Lagos is studied as a pattern only. All names, liveri… |
| `research-vehicles.md` | 1288 | 2026-10-14 | 2 | Gidi vehicle catalogue: everything that moves on Lagos roads and water: Research for the seeded Blender kit. **Rule zero:** study real Lagos, build our own cit… |

Binary: 9 files, 3.0 MB (9 .jpg).

### gidi/docs/map-format-example

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `README.md` | 10 | 2026-10-22 | 9 | Worked example of the new map format: One short home street in district d15 (20 m, invented names), written as the map would hold it (docs/MAP-FORMAT.md): |

Data: 3 files, 0.0 MB (.json); unpointed: 0.

### gidi/docs/research

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `LIFE-IN-LAGOS.md` | 329 | 2026-10-16 | 2 | Life in Lagos: what it's like to live there: A research pass, 16 Oct 2026, for the owner's ask: "immerse yourself in what it's like to live in Lagos". |

### gidi/docs/studies

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `airport.md` | 126 | 2026-10-15 | 0 | The Airport: the deep study: Inspired by Murtala Muhammed International Airport, Ikeja. Study area: 15.81 km², 15.81 km² of it land. Made by `scripts/study_dee… |
| `bazaar.md` | 127 | 2026-10-15 | 1 | The Bazaar: the deep study: Inspired by Ojo (electronics market) + Trade Fair. Study area: 21.78 km², 21.49 km² of it land. Made by `scripts/study_deep.py` fro… |
| `border.md` | 125 | 2026-10-15 | 1 | The Border: the deep study: Inspired by Badagry. Study area: 24.72 km², 20.74 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heigh… |
| `capital.md` | 125 | 2026-10-15 | 1 | The Capital: the deep study: Inspired by Ikeja. Study area: 15.64 km², 15.64 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and height… |
| `estate.md` | 127 | 2026-10-15 | 1 | The Estate: the deep study: Inspired by Magodo, Omole, Ikeja GRA. Study area: 24.26 km², 24.21 km² of it land. Made by `scripts/study_deep.py` from Google's bu… |
| `foodgate.md` | 127 | 2026-10-15 | 1 | Food Gate: the deep study: Inspired by Kosofe (Mile 12, Ketu, Ojota). Study area: 19.24 km², 19.2 km² of it land. Made by `scripts/study_deep.py` from Google's… |
| `frontier.md` | 127 | 2026-10-15 | 1 | The Frontier: the deep study: Inspired by Lekki + Ibeju-Lekki. Study area: 91.01 km², 88.92 km² of it land. Made by `scripts/study_deep.py` from Google's build… |
| `heights.md` | 127 | 2026-10-15 | 1 | The Heights: the deep study: Inspired by Ikoyi, VI, Banana Island. Study area: 19.09 km², 16.99 km² of it land. Made by `scripts/study_deep.py` from Google's b… |
| `hub.md` | 127 | 2026-10-15 | 1 | The Hub: the deep study: Inspired by Oshodi + Ojuelegba (Surulere). Study area: 64.56 km², 64.5 km² of it land. Made by `scripts/study_deep.py` from Google's b… |
| `jungle.md` | 127 | 2026-10-15 | 1 | Jungle City: the deep study: Inspired by Ajegunle + Festac. Study area: 11.93 km², 11.85 km² of it land. Made by `scripts/study_deep.py` from Google's building… |
| `maze.md` | 127 | 2026-10-15 | 1 | The Maze: the deep study: Inspired by Mushin + Shomolu. Study area: 33.66 km², 32.92 km² of it land. Made by `scripts/study_deep.py` from Google's buildings an… |
| `oldisland.md` | 125 | 2026-10-15 | 1 | Old Island: the deep study: Inspired by Lagos Island. Study area: 9.38 km², 5.9 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and hei… |
| `oldshore.md` | 127 | 2026-10-15 | 1 | Old Shore: the deep study: Inspired by Ikorodu + Epe. Study area: 20.35 km², 19.82 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and … |
| `port.md` | 127 | 2026-10-15 | 1 | The Port: the deep study: Inspired by Apapa + Mile 2 + the prison. Study area: 26.96 km², 19.36 km² of it land. Made by `scripts/study_deep.py` from Google's b… |
| `railside.md` | 127 | 2026-10-15 | 1 | Railside: the deep study: Inspired by Agege + Ifako-Ijaiye + Alimosho. Study area: 215.35 km², 215.35 km² of it land. Made by `scripts/study_deep.py` from Goog… |
| `watertown.md` | 127 | 2026-10-15 | 1 | Water Town: the deep study: Inspired by Makoko + Bariga + Agboyi + the sawmill. Study area: 7.27 km², 5.45 km² of it land. Made by `scripts/study_deep.py` from… |
| `yaba.md` | 127 | 2026-10-15 | 1 | Saba: the deep study: Inspired by Yaba and Akoka: the university, Sabo, Ojuelegba. Study area: 12.88 km², 10.64 km² of it land. Made by `scripts/study_deep.py`… |

### gidi/legacy

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `README.md` | 14 | 2026-10-23 | 9 | Legacy: the old map's kit (frozen): What the old map was and its parts: `OLD-MAP.md`. |

### gidi/legacy/blender

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `act1_sheet.py` | 71 | 2026-10-23 | 0 | The Act 1 kit pieces side by side (docs/KIT-GAPS.md, "New in the v2 layout"): the face-me-I-face-you block, the motor park office (and a shot inside it), the b… |
| `catalogue.py` | 48 | 2026-10-23 | 1 | Contact sheet of the kit: the same footprint built for each district character and several seeds. |
| `city.py` | 1104 | 2026-10-23 | 16 | Build the whole city (everything in web/gidi-data.js) as streamable tiles. |
| `city_run.py` | 121 | 2026-10-23 | 7 | Generate the whole city as tiles, in parallel Blender processes, and write the manifest. |
| `coverage.py` | 60 | 2026-10-23 | 3 | Writes docs/look/COVERAGE.md: every kind of thing in Gidi's data, how many, where, and whether the kit can build it yet. Plain Python (no Blender): python3 leg… |
| `generate.py` | 458 | 2026-10-23 | 5 | Build part of Gidi in Blender from the generated map data, every object styled by rules. |
| `gidi_kit/__init__.py` | 1 | 2026-10-23 | 0 |  |
| `gidi_kit/archetypes.py` | 613 | 2026-10-23 | 3 | Archetypes: whole objects assembled from parts, driven by rules. |
| `gidi_kit/blocks.py` | 151 | 2026-10-23 | 6 | A parametric building block that most non-house kinds are made from, plus shared pieces (signs with names, flagpoles, perimeter walls with gates, domes, minare… |
| `gidi_kit/boats.py` | 92 | 2026-10-23 | 1 | Boats on the lagoon: the ferries and water buses on the ferry routes, outboard canoes round Water Town, and the sand-dredging barges. Research-transport (lagoo… |
| `gidi_kit/core.py` | 227 | 2026-10-23 | 42 | Core of the Gidi kit: seeded randomness and a mesh builder. |
| `gidi_kit/detail.py` | 20 | 2026-10-23 | 0 | Detail level for the whole kit: 'full' for renders, 'web' for the streamed city (flat roof sheets, flat lettering, lighter bars and louvres, fewer cylinder seg… |
| `gidi_kit/draft.py` | 1333 | 2026-10-23 | 4 | The draft desk: the old kit's seeded rules, run once on a spot to write what they choose into its map as full records (decisions, 22 Oct: one ground truth; KIT… |
| `gidi_kit/facade.py` | 404 | 2026-10-23 | 15 | A walk-up's street face, close up (the facade pass, 22 Oct 2026): what Balogun and Isale Eko faces carry on top of the wall, its windows and its balconies. Eve… |
| `gidi_kit/goods.py` | 323 | 2026-10-23 | 2 | Goods and clutter: what fills a Lagos lean-to, stall or shop door. Sacks, tarps, nylon bags, crates, stacked plastics, cloth and cartons, piled against the wal… |
| `gidi_kit/gutters.py` | 156 | 2026-10-23 | 3 | The gutters the data lays along the roads (scripts/isms.py, GD['gutters']): open or covered with slabs, and the stretches it marks blocked, with green water or… |
| `gidi_kit/kinds.py` | 695 | 2026-10-23 | 9 | Archetypes for the rest of the data's building kinds. Each builder takes the object's attributes `a` (poly, storeys, district, ...) and its Rng, and returns (o… |
| `gidi_kit/landmarks.py` | 337 | 2026-10-23 | 8 | Named landmarks: a place on the map that needs a model of its own, by its name. |
| `gidi_kit/materials.py` | 304 | 2026-10-23 | 19 | Master materials. Each reads the mesh's 'Col' (paint colour) and 'Wear' (0..1) attributes, so a handful of materials cover every colour and age. The same pair … |
| `gidi_kit/monuments.py` | 413 | 2026-10-23 | 10 | Monuments and street landmarks, all invented (README rule zero): roundabout and corner statues (a founder in agbada, a masquerade, a talking-drummer), welded s… |
| `gidi_kit/oldtown.py` | 1167 | 2026-10-23 | 2 | The dense old town kit, driven by the map (decisions: "The map tells the kit what goes where"). |
| `gidi_kit/parcels.py` | 553 | 2026-10-23 | 5 | Parcels: the plots and grounds in the data (web/gidi-data.js 'parcels'), each with its surface and the furniture that makes it read: pitches with goalposts, a … |
| `gidi_kit/parts.py` | 694 | 2026-10-23 | 4 | Kit pieces. Each adds faces to a MeshBuilder, in world space, from a spec dict that the rules fill in (so the look of every piece is chosen from data, never ha… |
| `gidi_kit/people.py` | 145 | 2026-10-23 | 9 | People of Lagos streets, from docs/look/research-street.md section 4 (clothing, skin, density). Real proportions (1.55-1.85 m, head about 1/7.5 of height), sta… |
| `gidi_kit/places.py` | 854 | 2026-10-23 | 3 | Kinds built on the parametric block: civic, religious, commercial, housing types, leisure and transport buildings. Each picks a style and colours from research… |
| `gidi_kit/props.py` | 249 | 2026-10-23 | 13 | Small props shared by the Act 1 pieces (docs/KIT-GAPS.md, "New in the v2 layout"): plastic chairs, benches, water drums, jerrycans, umbrellas, tables, a wheelb… |
| `gidi_kit/registry.py` | 51 | 2026-10-23 | 5 | Which builder makes which thing in the data. generate.py and coverage.py both read this. |
| `gidi_kit/roadbed.py` | 211 | 2026-10-23 | 4 | The ground of a street piece as real geometry: a Lagos street is "just ground", up here, down there, all over the place. |
| `gidi_kit/roadside.py` | 240 | 2026-10-23 | 2 | Roadside furniture that makes a road read and lets you find your way: street lights (single and double arm, solar ones with their panel; a share dead, as in La… |
| `gidi_kit/rules.py` | 207 | 2026-10-23 | 17 | The rules: from what the data knows about an object to how it looks. |
| `gidi_kit/street.py` | 546 | 2026-10-23 | 8 | Street kit: road surfaces in every condition (from fresh asphalt to rutted mud), potholes that hold rainwater, markings, painted kerbs, speed bumps, open drain… |
| `gidi_kit/structures.py` | 538 | 2026-10-23 | 2 | Structures and city-scale lines: flyovers and rail bridges, skywalks, canal footbridges, jetties, expressways with Jersey barriers, the Long Bridge on piers, t… |
| `gidi_kit/textured.py` | 301 | 2026-10-23 | 4 | Photo textures on the kit's material slots (the eye tests now; the same files go into Unreal later, so the look the owner passes is the one that ships). |
| `gidi_kit/vehicles.py` | 954 | 2026-10-23 | 5 | Vehicles of Lagos roads, from docs/look/research-vehicles.md (sizes [src] where it had them). Every builder adds faces to a MeshBuilder at matrix M (x forward,… |
| `gidi_kit/wear.py` | 261 | 2026-10-23 | 5 | Age on the houses, in the vertex colours and in thin overlays on the walls. |
| `gidi_kit/zinc.py` | 169 | 2026-10-23 | 4 | Corrugated zinc the way Lagos roofs are: sheet by sheet. |
| `kinds_sheet.py` | 70 | 2026-10-23 | 0 | Contact sheet of every registered kind (except houses), each built on footprints taken from the real data, a few seeds side by side. blender -b --factory-start… |
| `kit_draft.py` | 30 | 2026-10-23 | 6 | The draft desk: write a first draft of every record a spot's map needs (decisions, 22 Oct: one ground truth; KIT.md section 12, "Records"). The old kit's seede… |
| `kit_test.py` | 212 | 2026-10-23 | 2 | A kit eye test: build one Street View spot from its map record with the old town kit and shoot it from the Street View's own camera (decisions: "A kit is prove… |
| `lights_sheet.py` | 23 | 2026-10-23 | 0 | Traffic lights, street-light ads, the new statues. blender -b --factory-startup -P legacy/blender/lights_sheet.py |
| `montage.py` | 23 | 2026-10-23 | 0 | Stitch legacy/blender/out/kinds/*.jpg into one labelled sheet: python3 legacy/blender/montage.py [out.jpg] [cols] |
| `monuments_sheet.py` | 27 | 2026-10-23 | 1 | Every monument in the kit side by side. blender -b --factory-startup -P legacy/blender/monuments_sheet.py -- [--out legacy/blender/out/monuments.jpg] |
| `new_kit_sheet.py` | 40 | 2026-10-23 | 2 | The newest kit pieces side by side: the container truck, the 911 food lorry, the trains, the Crown Hall, the central mosque and a flyover with painted piers. b… |
| `new_kit_sheet2.py` | 58 | 2026-10-23 | 1 | Contact sheets for the second batch: --part vehicles (service vehicles, the molue, port machines, boats) or --part places (cathedral, heritage, civic tower, ma… |
| `reach_sheet.py` | 17 | 2026-10-23 | 1 | The Reach, close up. blender -b --factory-startup -P legacy/blender/reach_sheet.py |
| `roadside_sheet.py` | 28 | 2026-10-23 | 1 | The roadside kit side by side: lamps, a direction sign, a gantry, speed and no-parking discs, a dressed bridge deck. blender -b --factory-startup -P legacy/ble… |
| `scene.py` | 95 | 2026-10-23 | 14 | Shared scene setup for previews: sky, sun, ground, camera, render settings. |
| `vehicles_sheet.py` | 39 | 2026-10-23 | 0 | Line-up of every vehicle in its conditions, and a crowd of every dress type. blender -b --factory-startup -P legacy/blender/vehicles_sheet.py -- [--out legacy/… |
| `wear_sheet.py` | 80 | 2026-10-23 | 1 | A street of Maze houses on their own, to judge wear and age close up (no tile build). blender -b --factory-startup -P legacy/blender/wear_sheet.py -- [--detail… |

### gidi/map-stamps/ut01_emmanuel

Data: 4 files, 0.0 MB (.json); unpointed: 2.

### gidi/map/d15

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `BUILDINGS.md` | 143 | 2026-10-24 | 3 | Mùṣá: the buildings draft and its hand pass: Drafted by `scripts/draft_buildings.py` (owner, 23 Oct: real footprints, then hand). 1457 houses in 41 blocks. Eac… |
| `STREETS.md` | 536 | 2026-10-24 | 2 | Mùṣá (district 15): the road plan and where each street comes from: Roads only, drawn on the new frame (1:3). Every kept street sits on its real line, squeezed… |

Data: 2 files, 1.0 MB (.json); unpointed: 0.

### gidi/schema

Data: 2 files, 0.0 MB (.json); unpointed: 0.

### gidi/scripts

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `audit3d.py` | 279 | 2026-10-23 | 21 | 3D audit: does a district's map make a proper city when the kit builds it? |
| `autoclean.py` | 194 | 2026-10-21 | 6 | The clean-up after the real areas, in every bake (owner, 21 Oct 2026: a fix made once must reach everything already built). Run after the hand edits, the road … |
| `bake_web.py` | 449 | 2026-10-21 | 16 | Bake Gidi map v0.3 into JSON for the web map: districts, water, arterials, generated local streets, POIs. Units: metres, origin top-left, y down. Map units fro… |
| `board_server.py` | 475 | 2026-10-24 | 7 | The drawing board's server (owner, 16 Oct 2026: "we should hand draw... know where something meets something"). |
| `build_viewer.py` | 22 | 2026-10-18 | 2 | Assemble the one-file Gidi Maps page (2D + 3D) from the baked data: web/gidi-maps.html. Run after scripts/bake_web.py. Then publish web/gidi-maps.html to the l… |
| `check_district.py` | 511 | 2026-10-21 | 48 | Independent checker for a generated district.  Usage: python3 scripts/check_district.py <id> Prints a PASS/FAIL line per check; exits 1 if any fails.  Import a… |
| `check_map.py` | 484 | 2026-10-24 | 10 | The new map's checker (docs/MAP-FORMAT.md; owner, 22 Oct 2026: "one ground truth"). Nothing in the map is guessed: a record with an unknown field, a missing fi… |
| `check_real.py` | 162 | 2026-10-22 | 5 | How close the map is to the real places it is the child of (owner, 21 Oct 2026: "nobody checks how close it is to the real place"). For every area of a distric… |
| `check_rules.py` | 18 | 2026-10-21 | 4 | Every rule in decisions/DECISIONS.md has a row in decisions/CHECKS.md saying what holds it (owner, 21 Oct 2026: gaps must not turn up only when someone asks). … |
| `child_plan.py` | 60 | 2026-10-19 | 0 | A district's child plan (owner, 19 Oct 2026: a district is the child of its real inspirations): draws docs/hand/<dir>/child_plan.json over the district's outli… |
| `compounds.py` | 141 | 2026-10-23 | 7 | Compound walls, in the map data (owner, 16 Oct 2026: if it's in the 3D, it's in the 2D). |
| `cross_sections.py` | 37 | 2026-10-15 | 18 | Gidi's road cross-sections: one table, read by the generator, the bake (written into the data as "cross_sections"), the space checker and the 3D kit. Agreed wi… |
| `deep_check.py` | 103 | 2026-10-16 | 3 | Does a generated district come out like its inspiration? Measures a gen file the way the deep study measured real Lagos (the same structure measures, scripts/s… |
| `deep_prep.py` | 80 | 2026-10-15 | 2 | Deep study, step 1 (docs/DEEP-STUDY.md): one pass over the big building files, cut per district, so the 17 district studies can run side by side. Reads Google … |
| `deep_profile.py` | 120 | 2026-10-16 | 3 | From a district's deep study (docs/data/deep/<id>.json) to its generator settings, and its fabric-type zones (docs/DEEP-STUDY.md). |
| `deep_report.py` | 105 | 2026-10-15 | 1 | Deep study, step 3: the study of a district (docs/data/deep/<id>.json) as a page a designer can read, ending in the targets its generator profile has to hit. U… |
| `deep_summary.py` | 34 | 2026-10-16 | 0 | All districts against their studies on one page (docs/data/deep-check/*.json, from scripts/deep_check.py). Usage: python3 scripts/deep_summary.py [out.md]     … |
| `deep_tune.py` | 49 | 2026-10-16 | 2 | One calibration pass (docs/DEEP-STUDY.md): each district's own miss against its study (docs/data/deep-check/<id>.json, written by scripts/deep_check.py) scales… |
| `design_density.py` | 198 | 2026-10-18 | 0 | A density pass: fill a district the way its real counterpart is built (Claude's design pass, owner 17 Oct 2026: "build it based off the Lagos you see"). Writes… |
| `district_profiles.py` | 754 | 2026-10-18 | 19 | Per-district settings for gen_fabric.py. Each number says where it comes from. A district with no profile gets the generator's original (v1) behaviour. The Maz… |
| `draft_buildings.py` | 303 | 2026-10-23 | 5 | A district's first draft of buildings, from its real blocks' own houses (owner, 23 Oct: "real footprints, then hand"). |
| `draw_area.py` | 79 | 2026-10-22 | 3 | One Ìbùdó area side by side with its real place, at the same scale and frame: the map as baked (left) and the real footprints and roads it was built from (righ… |
| `draw_gen.py` | 75 | 2026-10-15 | 4 | Draw a generated district (and optionally the real comparison square) at the same scale. |
| `draw_terrain.py` | 27 | 2026-10-15 | 1 | The terrain review map: colour relief with hillshade, land 0-3 m (flood-prone) marked, contours every 2 m, district outlines. Usage: python3 scripts/draw_terra… |
| `explore_city.py` | 207 | 2026-10-15 | 12 | Explore the generated Gidi districts on foot or by okada. Data: web/gidi-data.js (the baked city; run scripts/bake_web.py first). Run from the repo root: pytho… |
| `fabric_metrics.py` | 51 | 2026-10-13 | 2 | Same yardstick for real and generated fabric: streets [(cls, LineString)], buildings [Polygon], area Polygon (metres). |
| `fix_gutters_to_sections.py` | 73 | 2026-10-15 | 1 | One-off correction for a frozen district: its gutters were placed at the 3D kit's old road widths (a 7 m street, a 14 m main road) by scripts/isms.py; the agre… |
| `frame_footprints.py` | 93 | 2026-10-22 | 2 | Real roofs under the new frame, for the drawing board's zoomed-in "Real roofs" layer (web/board.html?frame=new). |
| `frame_network.py` | 132 | 2026-10-16 | 3 | The v2 frame's shared roads (docs/LAYOUT-V2.md): every district border becomes one named road, drawn once here, so districts can be generated side by side and … |
| `frame_study.py` | 303 | 2026-10-22 | 6 | The new frame's study layers for the drawing board (owner, 22 Oct 2026: Gidi is real Lagos miniaturised at 1:3, in a 27 x 10.5 km frame; roads first, districts… |
| `freeze_district.py` | 24 | 2026-10-16 | 12 | Freeze a district: write everything it owns in the baked map (scripts/hand.py: snapshot) into web/hand/<id>.json, so from now on the bake loads it as it is and… |
| `fronts.py` | 136 | 2026-10-23 | 7 | House fronts in the map data: which side faces the street, shop fronts, their canopies and the balconies (owner, 16 Oct 2026: if it's in the 3D, it's in the 2D… |
| `furniture.py` | 161 | 2026-10-17 | 6 | Street furniture as data, run by bake_web.py after the junctions and heights (the ground plan of the Google rebuild). Every pole, street light, traffic light, … |
| `gen_fabric.py` | 1849 | 2026-10-18 | 22 | Original street + building generator for one Gidi district. Nothing here is copied from a real map: the inputs are only the statistics in study-<id>.json / stu… |
| `ground.py` | 216 | 2026-10-18 | 6 | Ground use: what every square metre of Gidi is for, and who may be on it (owner, 17 Oct 2026: "it's important to have the entire system understand where people… |
| `groundpaint.py` | 133 | 2026-10-18 | 5 | The ground itself, painted in the map data (owner, 17 Oct 2026: "even the grain of sand on the ground... everything in the data"; batch 3 of what the kit used … |
| `hand.py` | 721 | 2026-10-23 | 25 | Hand files (owner, 15 Oct 2026: "less generator, more hand placing"): web/hand/<district>.json holds what is placed by hand in a district, and the bake applies… |
| `hand_fix_checks.py` | 33 | 2026-10-21 | 1 | The clean-up after a real-area build, written as hand edits (owner: "clean up everything by hand"): reads the baked map and writes hand edits into web/hand/<di… |
| `hand_fix_lines.py` | 86 | 2026-10-16 | 5 | Hand fix: houses that reach over a street's building line in the finished map (web/gidi-data.js). The bake's road clean-up extends and straightens streets afte… |
| `hand_links.py` | 82 | 2026-10-16 | 4 | Hand placing helper: streets cut off from the city's road network (a cluster that only met a shore road, now a footpath in the v2 frame) each get one link stre… |
| `houses.py` | 222 | 2026-10-23 | 6 | What stands on and beside each house, and which building each place takes over, in the map data (owner, 17 Oct 2026: everything in the data; batch 2 of what th… |
| `isms.py` | 523 | 2026-10-23 | 10 | The Lagos-isms, placed by rule into the baked city data (docs/ISMS-BUILD.md, docs/LAGOS-ISMS.md). Runs inside scripts/bake_web.py after the road clean-up (road… |
| `junctions.py` | 253 | 2026-10-15 | 2 | Junctions, run by bake_web.py after the road clean-up and before the heights (pass 3 of the road work). |
| `landmarks.py` | 204 | 2026-10-13 | 8 | Big pieces a district is known for, laid out before (or after) the ordinary street fabric. Used by gen_fabric.py when a district profile asks for them (the Hub… |
| `layout_v2.py` | 219 | 2026-10-20 | 5 | Gidi v2 layout (owner's choice, 15 Oct 2026): a fictional Lagos at ONE even scale, 1:4 (docs/LAYOUT-V2.md). District positions = their inspirations' real posit… |
| `map02.py` | 88 | 2026-10-13 | 2 | Gidi map v0.2 (drawn in units of 0.8 km; 1.25 units = 1 km): 15 districts merged from Lagos's 20 LGAs (see lagos-lgas-research.md). Schematic, km grid. stilts |
| `market_streets.py` | 91 | 2026-10-16 | 3 | Market streets, run by bake_web.py on the final roads (after the clean-up and the junctions). The owner's ruling (15 Oct 2026, from Mile 12, Oshodi, Idumota): … |
| `real_underlay.py` | 60 | 2026-10-22 | 2 | The real place under each Ìbùdó area, for the drawing board's "Real place" layer: the real footprints (Google Open Buildings v3) and roads (Overture) each area… |
| `realnames.py` | 91 | 2026-10-21 | 5 | Gidi's names are its own: no name on the map may share its core with a real name around the places Gidi is a child of. |
| `rebuild_areas.py` | 108 | 2026-10-22 | 9 | Ìbùdó's areas built again from their real places, every one, in the child plan's order (owner, 21 Oct 2026: "if you fix a bug in the future", it must reach eve… |
| `rename_mains.py` | 60 | 2026-10-16 | 1 | After districts are generated side by side (the v2 frame), two of them can pick the same road name, or two roads sharing a first name ("Ayinde Road" and "Ayind… |
| `roadclean.py` | 476 | 2026-10-23 | 5 | Rule-based clean-up of the baked road network, run by bake_web.py before the civic layer. Fixes what scripts/audit3d.py finds (D, R5, R1, R4, R2, R3), using th… |
| `roadends.py` | 250 | 2026-10-17 | 9 | Road ends (owner, 17 Oct 2026: "the road quite literally just ends abruptly"). |
| `roadtypes.py` | 131 | 2026-10-18 | 2 | What kind of road each street is (owner, 18 Oct 2026: "I don't think we understand things like closes, crescents, drives, ways"). The streets are stored in pie… |
| `roadz.py` | 506 | 2026-10-16 | 5 | Road heights, run by bake_web.py after the road clean-up (scripts/roadclean.py). Pass 2 of the road work. |
| `structure.py` | 131 | 2026-10-15 | 5 | How a place is built, not just how much: the structure measures of the Google rebuild (docs/REBUILD-PLAN.md). measure(buildings, streets, area) works the same … |
| `study_analyse.py` | 258 | 2026-10-13 | 17 | Pattern study, step 2: turn the raw inspiration data into rules (statistics only; nothing is copied into Gidi). ---------- ROADS ---------- noded drive network… |
| `study_boxheights.py` | 31 | 2026-10-14 | 6 | Height bands for a neighbourhood-level study: data/results/heights.py measures whole LGAs; this measures the part of an LGA inside lon/lat boxes, the same way … |
| `study_connect.py` | 53 | 2026-10-13 | 16 | Pattern study, step 3: gateways to neighbours (deduplicated) and the spread of fabric density over 1 km squares. cluster crossings within 120 m (dual carriagew… |
| `study_core.py` | 37 | 2026-10-14 | 17 | Pick representative real 1 km squares (median and dense) and measure them with the same yardstick used on Gidi. |
| `study_deep.py` | 490 | 2026-10-16 | 19 | Deep study, step 2 (docs/DEEP-STUDY.md): everything the data says about one district's real inspiration, for its generator profile. Sources (numbers only go in… |
| `study_extract.py` | 53 | 2026-10-13 | 16 | Pattern study, step 1: pull everything OSM knows about an inspiration area (OSM, ODbL). Data stays local; only statistics are used. |
| `study_google.py` | 100 | 2026-10-15 | 1 | How much does OSM miss? Google Open Buildings v3 (machine-traced from satellite imagery, CC BY 4.0) against the OSM buildings of each district's study area, ce… |
| `study_isms.py` | 134 | 2026-10-14 | 9 | Pattern study, the "Lagos-isms": eccentricities in the real data that a tidy generator would never make, counted the same way for every studied area so they ca… |
| `study_landmarks.py` | 80 | 2026-10-13 | 15 | Pattern study, step 5 (Hub and any transit district): sizes of the big structures a district is known for. Flyover spans, interchanges (clusters of slip roads)… |
| `study_structure.py` | 130 | 2026-10-15 | 1 | Structure study of a district's inspiration from Google Open Buildings v3 (outlines) and OSM (streets), and the same measures on Gidi's district, square by squ… |
| `study_undermapped.py` | 38 | 2026-10-15 | 4 | Pattern study, for an area where OSM has mapped the streets but only a fraction of the buildings (central Ikeja: OSM footprints cover 10-14% of land that ESA W… |
| `study_village.py` | 24 | 2026-10-13 | 1 | Waterfront studies: split the buildings on the water (stilt villages: more than 60 m from any mapped road) from the land ones. Writes study-<id>-village.json (… |
| `study_wellmapped.py` | 39 | 2026-10-14 | 5 | Pattern study, for an area where OSM maps the streets everywhere but the buildings only in some neighbourhoods (the Estate: Ikeja GRA is traced, most of Magodo… |
| `surfaces.py` | 152 | 2026-10-16 | 2 | Road surfaces (owner, 16 Oct 2026: "sometimes you have roads... not particularly paved... marshy ground... so much grime it barely looks like it's tarred... in… |
| `terrain.py` | 106 | 2026-10-15 | 3 | Gidi's ground: a height grid for the whole map (web/terrain.json), from the land under each district's real inspiration. Each district takes the relief of its … |
| `things.py` | 687 | 2026-10-23 | 9 | Things the 3D kit used to invent, now in the map data (owner, 17 Oct 2026: "everything should be in the data... even the grain of sand... if everything is in t… |
| `trees.py` | 88 | 2026-10-23 | 6 | Trees in the map data (owner, 16 Oct 2026: if it's in the 3D, it's in the 2D). |
| `twin_photos.py` | 48 | 2026-10-20 | 0 | Street twins' pictures for one built area of a child district (docs/hand/<dir>/twins/<area>.json). plan:   python3 scripts/twin_photos.py plan ibudo <area>    … |
| `twins.py` | 70 | 2026-10-19 | 2 | Every type in Gidi and its real twin (owner, 19 Oct 2026: "let's know what every type of item and building as well to the type of surface, so we know we have a… |
| `walknet.py` | 104 | 2026-10-15 | 5 | The walking and riding network of the built districts, shared by explore_city.py (the living test) and bake_web.py (placing schools, places of worship and chem… |
| `whats_here.py` | 105 | 2026-10-15 | 1 | What is on the ground here? Everything the map holds at one spot, from the built data (web/gidi-data.js): the district and the ground's height, the surface (ca… |

### gidi/scripts/hand_spots

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `ibudo_real_area.py` | 385 | 2026-10-22 | 3 | Ìbùdó, one area of the child plan built from its real place (owner, 19 Oct 2026: "you are taking streets from this place ... so you can have real life images t… |
| `ibudo_spot1.py` | 90 | 2026-10-19 | 0 | Ìbùdó spot 1 (docs/hand/ibudo/design_v1.png, the owner's approval 19 Oct 2026): Oshodi rebuilt one-for-one beside the Ring Road flyover, written as hand edits … |

### gidi/web

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `app.js` | 550 | 2026-10-23 | 4 | Gidi Maps: a Google Maps–style viewer for the Gidi city plan (map v0.3). Data: window.GIDI (metres, origin top-left, y down). React 18 UMD, no JSX. |
| `board.html` | 94 | 2026-10-22 | 10 | Gidi Drawing Board |
| `board.js` | 890 | 2026-10-22 | 3 | The Gidi drawing board (owner, 16 Oct 2026): a clean plan of the city to scale, where every road edge, plot, house and piece of street furniture can be seen ex… |
| `faceedit.js` | 235 | 2026-10-22 | 1 | The face editor on the new frame's board (docs/MAP-FORMAT.md, "faces"): one face of a building drawn flat, u across from the face's first corner, z up from the… |
| `frame.js` | 239 | 2026-10-22 | 2 | The drawing board's new frame (owner, 22 Oct 2026): real Lagos miniaturised at 1:3 in a 27 x 10.5 km frame, as study layers to draw the new map on by hand. Ope… |
| `mapedit.js` | 1458 | 2026-10-24 | 5 | The new map's editor on the drawing board's new frame (board.html?frame=new; docs/MAP-FORMAT.md). Draws and saves the plan layer, record by record, in map/<dis… |
| `shell.html` | 196 | 2026-10-17 | 2 | Gidi Maps |
| `view3d.js` | 531 | 2026-10-23 | 3 | Gidi Maps, 3D view. Close in, the city is the Blender kit's own models (legacy/blender/city_run.py writes them as 400 m tiles to web/city/<detail>/tiles): they… |

Data: 26 files, 12.1 MB (.json); unpointed: 2.

Binary: 3 files, 94.2 MB (1 .json, 1 .js, 1 .html).

### gidi/web/hand

Data: 11 files, 8.1 MB (.json); unpointed: 9.

Binary: 8 files, 22.1 MB (8 .json).

## gidi-game

456 files.

### gidi-game/.

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `.gitattributes` | 17 | 2026-10-19 | 0 |  |
| `.gitignore` | 44 | 2026-10-24 | 4 |  |
| `ASSETS.md` | 34 | 2026-10-19 | 6 | Hand-made assets: / Asset / Where / Source / Status / /---/---/---/---/ / Danfo Basic 2.0 (font): the owner's danfo lettering (BirdFont, July 2022), spaced, ke… |
| `CLAUDE.md` | 9 | 2026-10-17 | 28 | Gidi game (Unreal): Read the map repo's `decisions/` first (`~/gidi/decisions/NOW.md`, `DECISIONS.md`): the same rules apply here. |
| `README.md` | 56 | 2026-10-24 | 9 | Gidi: the game: The Unreal Engine 5.8 project for Gidi. The city itself lives in the map repo, [NewDara-Star/gidi](https://github.com/NewDara-Star/gidi): its d… |

Data: 1 files, 0.0 MB (.json); unpointed: 0.

Binary: 1 files, 0.0 MB (1 .uproject).

### gidi-game/Art/Brand

Data: 1 files, 0.0 MB (.json); unpointed: 0.

Binary: 2 files, 0.1 MB (2 .png).

### gidi-game/Art/Buildings

Data: 4 files, 0.0 MB (.json); unpointed: 4.

Binary: 9 files, 5.4 MB (4 .blend, 4 .glb, 1 .jpg).

### gidi-game/Art/Fonts

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `OFL-GidiBrush.txt` | 96 | 2026-10-19 | 1 |  |
| `OFL.txt` | 95 | 2026-10-19 | 2 |  |
| `src/montserrat/OFL.txt` | 93 | 2026-10-19 | 2 |  |
| `src/titanone/OFL.txt` | 95 | 2026-10-19 | 2 |  |

Binary: 10 files, 1.1 MB (7 .ttf, 3 .png).

### gidi-game/Art/Frames

Binary: 2 files, 47.6 MB (1 .blend, 1 .png).

### gidi-game/Art/People

Data: 11 files, 0.0 MB (.json); unpointed: 10.

Binary: 12 files, 33.8 MB (11 .blend, 1 .png).

### gidi-game/Art/Plates

Data: 1 files, 0.0 MB (.json); unpointed: 0.

Binary: 9 files, 0.6 MB (8 .png, 1 .jpg).

### gidi-game/Art/Props

Data: 33 files, 0.0 MB (.json); unpointed: 33.

Binary: 95 files, 21.9 MB (40 .blend, 39 .glb, 9 .jpg, 7 .png).

### gidi-game/Art/Textures

Binary: 15 files, 20.1 MB (15 .jpg).

### gidi-game/Art/Vehicles

Data: 33 files, 0.0 MB (.json); unpointed: 29.

Binary: 120 files, 242.8 MB (62 .glb, 36 .blend, 14 .jpg, 8 .png).

### gidi-game/Config

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `DefaultDeviceProfiles.ini` | 102 | 2026-10-24 | 4 | sections: DeviceProfiles, Gidi_Work DeviceProfile, Gidi_Low DeviceProfile, Gidi_High DeviceProfile, Gidi_Full DeviceProfile, MacEditor DeviceProfile |
| `DefaultEditor.ini` | 1 | 2026-10-17 | 0 | sections:  |
| `DefaultEditorPerProjectUserSettings.ini` | 5 | 2026-10-17 | 0 | sections: /Script/ModelContextProtocolEngine.ModelContextProtocolSettings |
| `DefaultEngine.ini` | 70 | 2026-10-24 | 1 | sections: /Script/EngineSettings.GameMapsSettings, /Script/Engine.RendererSettings, /Script/WindowsTargetPlatform.WindowsTargetSettings, /Script/LinuxTargetPla… |
| `DefaultGame.ini` | 5 | 2026-10-17 | 0 | sections: /Script/EngineSettings.GeneralProjectSettings |
| `DefaultInput.ini` | 85 | 2026-10-17 | 0 | sections: /Script/Engine.InputSettings |

### gidi-game/Content/Gidi

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `Hand/.gitkeep` | 1 | 2026-10-17 | 0 |  |

Binary: 8 files, 0.1 MB (8 .uasset).

### gidi-game/Content/Python

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `.gitkeep` | 1 | 2026-10-17 | 0 |  |
| `gidi_cam.py` | 16 | 2026-10-18 | 3 | Put the check camera in the city level: tools/shot.sh moves it, the game starts looking through it (auto-activates). |
| `gidi_heroes.py` | 258 | 2026-10-22 | 9 | Hero models in the city: hand-made vehicles (Art/Vehicles, made by tools/vehicle_prep.py) placed wherever the map data puts one of their kind (the data's "thin… |
| `gidi_import.py` | 379 | 2026-10-24 | 5 | The Gidi importer: the city in Unreal, made from the map repo's data (the map is never final, so this runs again and again). |
| `gidi_look.py` | 49 | 2026-10-18 | 5 | The city's light and lens, set once in Gidi_City (run headless: tools/look.sh, or from gidi_import's _environment). |
| `gidi_modes.py` | 106 | 2026-10-24 | 3 | The crowd per mode (decisions: "Build light, look full"; docs/PERFORMANCE.md). |
| `gidi_paint.py` | 131 | 2026-10-19 | 2 | Painted panels that wear: M_GidiPaint, for the built vehicles' paint slots (gidi_heroes.py). |
| `gidi_photo.py` | 96 | 2026-10-19 | 1 | Photo mode, for pictures to post: one danfo placed where it's wanted, a cinema camera on it, the sun where the picture wants it. Run headless before the game (… |
| `gidi_plates.py` | 201 | 2026-10-19 | 5 | Number plates in Unreal: every vehicle its own number, from one material (tools/plates.py draws the pieces into Art/Plates). |
| `gidi_play.py` | 80 | 2026-10-24 | 4 | The playable spot: Ìbùdó's Market Road under the Ring Road flyover (the map's spot 1), as its own level you play in. |
| `gidi_signs.py` | 88 | 2026-10-18 | 1 | Shop signs and painted lettering in Unreal, from the kit's tile records (gidi repo web/city/<detail>/tiles/<t>.json "signs"). |
| `gidi_stream.py` | 82 | 2026-10-24 | 3 | The city streams in pieces around the player (decisions: "Build light, look full", (4); docs/PERFORMANCE.md). |
| `gidi_surfaces.py` | 353 | 2026-10-19 | 4 | Textured surfaces: the city's walls, roofs, roads and ground get real texture, still in the kit's colours. |
| `gidi_underdeck.py` | 282 | 2026-10-24 | 5 | The underdeck: a playable test street, a danfo park under a flyover pair (the owner, 22 Oct: video 1's real match, "try to build Obalende"). Its own level, Pla… |

### gidi-game/docs

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `ASSET-INVENTORY.md` | 21 | 2026-10-23 | 2 | What's already in the project (check here before building anything): The owner's rule (19 Oct): look at what we have before building from scratch. Gidi's own t… |
| `PERFORMANCE.md` | 112 | 2026-10-24 | 11 | Performance: modes, near detail, streaming, budgets: The owner's rule (gidi `decisions/DECISIONS.md`, 22 Oct, "Build light, look full"): build in a light mode,… |

### gidi-game/tools

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `block_build.py` | 557 | 2026-10-23 | 2 | The rendered block, built in Blender part by part: blender -b -P tools/block_build.py -- <out.blend> [recipe.json] |
| `brt_build.py` | 288 | 2026-10-23 | 1 | The BRT bus, built in Blender part by part: blender -b -P tools/brt_build.py -- <out.blend> [variant.json] |
| `danfo_build.py` | 521 | 2026-10-23 | 9 | The danfo, built in Blender part by part (not generated): blender -b -P tools/danfo_build.py -- <out.blend> [variant.json] |
| `editor.sh` | 26 | 2026-10-24 | 5 | Open the editor in a mode: tools/editor.sh [work/low/high/full] [underdeck/ibudo/<map path>]   (any order) the mode   defaults to this machine's choice (tools/… |
| `fab_list.sh` | 9 | 2026-10-19 | 1 | What's in the project from Fab (added = in Content/Fab). tools/fab_list.sh |
| `fields.py` | 121 | 2026-10-23 | 20 | What a builder reads from its recipe, declared beside its code and held to it (gidi decisions, 23 Oct: the interface works both ways: a field a builder grows m… |
| `font_brush.py` | 227 | 2026-10-19 | 2 | Gidi Brush, the painted danfo lettering: ~/.venvs/gidi/bin/python tools/font_brush.py <TitanOne.ttf> <out.ttf> |
| `font_build.sh` | 26 | 2026-10-19 | 1 | Build Danfo Basic from its sources (Art/Fonts/src): the owner's 2022 letters and Alfa Slab One, the font they were drawn from. tools/font_build.sh   ->  Art/Fo… |
| `font_plate.py` | 135 | 2026-10-19 | 1 | Gidi Plate, the number-plate face: ~/.venvs/gidi/bin/python tools/font_plate.py <Montserrat-Bold.ttf> <out.ttf> |
| `font_punct.py` | 120 | 2026-10-19 | 2 | Punctuation for Danfo Basic, from its base font: ~/.venvs/gidi/bin/python tools/font_punct.py <danfo.ttf> <AlfaSlabOne.ttf> <out.ttf> |
| `font_space.py` | 165 | 2026-10-19 | 6 | Space and kern a font by measurement (the owner's Danfo Basic, 2022: "I could not get the tracking or kerning right"). |
| `font_specimen.py` | 42 | 2026-10-19 | 1 | Specimen sheets for a font, to judge it by eye (zoom in): ~/.venvs/gidi/bin/python tools/font_specimen.py <font.ttf> <out dir> |
| `frame_motorpark.py` | 276 | 2026-10-19 | 1 | The first Lagos-pass frame: the Àdàrú motor park beside the expressway, seen from a footbridge (after the owner's photo, refs/lagos-life/09): blender -b -P too… |
| `furniture_build.py` | 271 | 2026-10-23 | 2 | Street furniture, built in Blender part by part: blender -b -P tools/furniture_build.py -- <out.blend> [recipe.json] |
| `goods_kit.py` | 349 | 2026-10-23 | 5 | Goods, built from a map `goods` record's rows: import goods_kit as G; G.build(rows, frame) -> objects. |
| `import.sh` | 19 | 2026-10-19 | 5 | Bring the city in from the gidi repo: tools/import.sh maze / all / "25,9;25,10"  [--force] [--full] Close the Unreal editor first. GIDI_REPO points at the map … |
| `keke_build.py` | 357 | 2026-10-23 | 1 | The keke, built in Blender part by part: blender -b -P tools/keke_build.py -- <out.blend> [variant.json] |
| `kit_fields.py` | 242 | 2026-10-23 | 16 | Every builder's fields, collected and held against the map: python tools/kit_fields.py [--map=~/gidi] [--records=<map dir>] [--write] |
| `labels.py` | 97 | 2026-10-19 | 2 | Bottle labels for Gidi's invented drinks: ~/.venvs/gidi/bin/python tools/labels.py  (writes Art/Props/Labels/<brand>.png) |
| `lettering.py` | 129 | 2026-10-19 | 3 | Lettering laid out for a sticker: ~/.venvs/gidi/bin/python tools/lettering.py <font.ttf> <text> <cap metres> <arc radius or 0> <outline metres> <out.json> [--b… |
| `look.sh` | 8 | 2026-10-18 | 1 | Set the city's light and lens (Content/Python/gidi_look.py) headless; GIDI_LOOK='{"ev_bias": -1.5}' tries other values. |
| `loose_build.py` | 55 | 2026-10-23 | 0 | Goods and litter lying loose on the ground, built in Blender: blender -b -P tools/loose_build.py -- <out.blend> [recipe.json] |
| `lorry_build.py` | 671 | 2026-10-23 | 2 | The container lorry, built in Blender part by part: blender -b -P tools/lorry_build.py -- <out.blend> [recipe.json] |
| `make_textures.py` | 118 | 2026-10-18 | 4 | Seamless detail textures for the city's surfaces, made from noise (no photographs, so nothing to license and nothing to copy). |
| `map_build.py` | 257 | 2026-10-23 | 3 | The map, built: python tools/map_build.py <map dir> <district> <out folder> [--box=x0,y0,x1,y1] [--camera=x,y,z,turn,pitch,fov] [--spot=<spot.json>] [--origin=… |
| `measure.sh` | 11 | 2026-10-24 | 4 | Measure a play level in a mode against its budget (docs/PERFORMANCE.md): tools/measure.sh [underdeck/ibudo] [work/low/high/full/old] [seconds] [shot.png] Runs … |
| `measure_csv.py` | 98 | 2026-10-24 | 2 | Read the CSV profile tools/measure.sh just took and write Saved/Perf/<spot>_<mode>.txt: the level's numbers against its budget (BUDGET below, docs/PERFORMANCE.… |
| `mode.sh` | 17 | 2026-10-24 | 4 | Flip the editor's mode: tools/mode.sh work/low/high/full   (docs/PERFORMANCE.md; the presets: Config/DefaultDeviceProfiles.ini) The editor takes this mode's de… |
| `mode_sg.py` | 19 | 2026-10-24 | 2 | The scalability levels (sg.*) of a Gidi mode, as console commands: python tools/mode_sg.py Gidi_Work -> "sg.ShadowQuality 0, sg.TextureQuality 1, ...". Read fr… |
| `molue_build.py` | 369 | 2026-10-23 | 1 | The molue, built in Blender part by part: blender -b -P tools/molue_build.py -- <out.blend> [variant.json] |
| `perf.sh` | 22 | 2026-10-19 | 1 | The laptop test (decisions: at least 30 frames a second at 1080p on the owner's M4, 16 GB): tools/perf.sh "x y z pitch yaw" name [seconds] Runs the game at 192… |
| `person_build.py` | 293 | 2026-10-23 | 3 | A Gidi person, built with MakeHuman in Blender (MPFB, CC0 assets): blender -b -P tools/person_build.py -- <spec.json> <out.blend> [render.png] |
| `photo.sh` | 19 | 2026-10-19 | 2 | Photo mode: tools/photo.sh '<GIDI_PHOTO json>' name [seconds]  (Content/Python/gidi_photo.py says what the json holds) Places the photo danfo and a cinema came… |
| `pickup_build.py` | 516 | 2026-10-23 | 2 | The pickup, built in Blender part by part: blender -b -P tools/pickup_build.py -- <out.blend> [recipe.json] |
| `plates.py` | 246 | 2026-10-19 | 8 | Gidi's number plates: ~/.venvs/gidi/bin/python tools/plates.py  (writes Art/Plates/) |
| `play.sh` | 89 | 2026-10-24 | 9 | Play a spot: tools/play.sh [underdeck] [work/low/high/full] [build]   (any order; defaults: Ìbùdó, work) (no name)  Ìbùdó's Market Road under the flyover (Cont… |
| `pole_build.py` | 357 | 2026-10-23 | 2 | The street pole, built in Blender part by part: blender -b -P tools/pole_build.py -- <out.blend> [recipe.json] |
| `prop_basin_final.py` | 369 | 2026-10-19 | 1 | The basin of drinks, finished (the proof that a blockout becomes real): blender -b -P tools/prop_basin_final.py -- <out folder> [render.png] |
| `props_build.py` | 259 | 2026-10-19 | 2 | Street props for the Lagos pass (docs/hand/lagos-pass.md, the owner's photos in refs/lagos-life/): blender -b -P tools/props_build.py -- <out folder> |
| `shot.sh` | 20 | 2026-10-19 | 3 | A check picture of the imported city: tools/shot.sh "x y z pitch yaw" name  (map metres: x east, y south; degrees) Puts a camera in Gidi_City (headless), runs … |
| `spot_assemble.py` | 223 | 2026-10-23 | 3 | A spot rebuilt from its records and rendered from the photo's camera: python tools/spot_assemble.py <spot.json> <out folder> |
| `spot_to_map.py` | 336 | 2026-10-23 | 2 | A test spot as map records: python tools/spot_to_map.py <spot.json> <stamp dir> <district> --origin=x,y [--name=<stamp>] |
| `stall_build.py` | 363 | 2026-10-23 | 2 | The street stall with its goods, built in Blender part by part: blender -b -P tools/stall_build.py -- <out.blend> [recipe.json] |
| `stream.sh` | 8 | 2026-10-24 | 2 | Put the city's tiles on streaming volumes (Content/Python/gidi_stream.py; tools/import.sh does it after every import): a tile is drawn within 600 m of its edge… |
| `surfaces.sh` | 8 | 2026-10-18 | 2 | Textured surfaces (Content/Python/gidi_surfaces.py): make the textures, build the material, re-point the imported meshes. Headless. |
| `trace_mark.py` | 39 | 2026-10-19 | 1 | A mark's outline traced from its picture: ~/.venvs/gidi/bin/python tools/trace_mark.py <mark.png> <out.json> |
| `umbrella_build.py` | 318 | 2026-10-23 | 3 | The market umbrella, built in Blender part by part: blender -b -P tools/umbrella_build.py -- <out.blend> [recipe.json] |
| `underdeck_build.py` | 1133 | 2026-10-22 | 3 | The underdeck set: a danfo park under a flyover pair, built from the study of the real one (the owner, 22 Oct: "try to build Obalende"; refs ~/Real-world/resea… |
| `underdeck_extras.py` | 73 | 2026-10-22 | 3 | The underdeck's extra models, from the hand-made ones (generated into Saved/Underdeck, never committed): blender -b -P tools/underdeck_extras.py -- [out folder… |
| `vehicle_export.py` | 22 | 2026-10-19 | 1 | A built vehicle's game models from its Blender file: blender -b <name>_parts.blend -P tools/vehicle_export.py -- <out base> |
| `vehicle_kit.py` | 405 | 2026-10-23 | 15 | The shared pieces of the vehicle builders (Blender), copied from tools/danfo_build.py so the keke, the molue and the BRT build the same way: start() clears the… |
| `vehicle_look.py` | 121 | 2026-10-19 | 2 | Look renders of a built vehicle: blender -b <parts.blend> -P tools/vehicle_look.py -- <out.jpg> [view ...] [--size W] |
| `vehicle_prep.py` | 329 | 2026-10-19 | 3 | A generated vehicle (Meshy) made game-ready in Blender: blender -b -P tools/vehicle_prep.py -- <in.glb> <out.glb> <spec.json> |
| `vehicle_stickers.py` | 192 | 2026-10-23 | 6 | Badges and stickers in 3D, for the vehicle builders (Blender): thin raised pieces, each its own object, so they stay sharp and come off for a variant. |
| `wall_build.py` | 558 | 2026-10-23 | 2 | The boundary wall or fence and its gates, built in Blender part by part: blender -b -P tools/wall_build.py -- <out.blend> [recipe.json] |
| `wear_layer.py` | 265 | 2026-10-23 | 3 | The wear layer: dust, grime, rust, fading and damp put on top of clean built parts, in Blender's shaders. |
| `winshot.py` | 24 | 2026-10-24 | 3 | Save one window of a running process as a picture: ~/.venvs/gidi/bin/python tools/winshot.py <pid> <out.png> (the game's own screenshot is taken on its first d… |

## Real-world

300 files.

### Real-world/.

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `.gitignore` | 20 | 2026-10-05 | 4 |  |
| `CLAUDE.md` | 184 | 2026-10-05 | 28 | World Drive: driving simulator in real places: A desktop driving simulator (three.js r186 WebGPU in Electron) set in real places rebuilt from open map data. Th… |
| `ROADMAP.md` | 496 | 2026-10-05 | 5 | Running order: The plan for the driving simulator, in order. Update this file as items move. Rule: research how the industry does each thing first (simulators,… |

### Real-world/.claude

Data: 1 files, 0.0 MB (.json); unpointed: 0.

### Real-world/.claude/hooks

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `guard-git.sh` | 31 | 2026-10-04 | 2 | Before a shell command: commits and pushes go through the repo's git hooks, never around them. Exit 2 blocks the command and tells Claude why. Changing the hoo… |
| `outbound-guard.sh` | 33 | 2026-10-04 | 1 | Before a shell command or web fetch: the project's hard rules on what goes out and what comes in. No Google Street View imagery, no personal data in request he… |
| `session-start.sh` | 10 | 2026-10-04 | 1 | Session start: switch on the repo's git hooks (.githooks) and make sure the game's dependencies are installed so the checks can run. |
| `stop-checks.sh` | 25 | 2026-10-04 | 1 | End of a turn: if code is changed and not committed, the typecheck and tests must pass, or Claude goes back to fix them. Cached by the exact change, so an unch… |

### Real-world/.githooks

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `commit-msg` | 16 | 2026-10-04 | 1 |  |
| `lib.sh` | 38 | 2026-10-04 | 4 | Shared helpers for the git hooks. Sourced, not run. A hook must never fail without saying why. Paths whose changes need the checks and a Story: the app, its te… |
| `pre-commit` | 39 | 2026-10-04 | 1 |  |
| `pre-push` | 30 | 2026-10-04 | 1 |  |
| `review.sh` | 90 | 2026-10-05 | 2 | A second Claude reads CLAUDE.md, the commit messages and the diff of a push, and blocks it with findings when a change breaks a rule there. If a finding is wro… |

### Real-world/docs

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `blender-assets.md` | 174 | 2026-10-05 | 12 | 3D assets to build in Blender (with a local Claude + BlenderMCP): How to use this: open Claude Code on the Mac in the repo folder, with BlenderMCP connected. P… |

### Real-world/game

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `.gitignore` | 6 | 2026-10-04 | 4 |  |
| `README.md` | 90 | 2026-10-04 | 9 | World Drive: A driving simulator set in real places rebuilt from open map data: a driving school for the Irish test (Finglas, Dublin) plus a world explorer (Ya… |
| `globe.html` | 45 | 2026-10-04 | 3 | World Drive |
| `index.html` | 139 | 2026-10-04 | 7 | World Drive — drive real places |
| `vite.config.ts` | 15 | 2026-10-04 | 1 |  |

Data: 3 files, 0.1 MB (.json); unpointed: 0.

Binary: 4 files, 0.9 MB (3 .png, 1 .jsonc).

### Real-world/game/desktop

Binary: 2 files, 0.0 MB (2 .cjs).

### Real-world/game/public

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `globe/CREDITS.md` | 12 | 2026-10-04 | 13 | Globe images: All three are the example images shipped with the `three-globe` npm package by Vasco Asturiano (MIT, https://github.com/vasturiano/three-globe, `… |
| `models/CREDITS.md` | 80 | 2026-10-05 | 13 | 3D models: - `car_concept.glb`: "CarConcept" from the Khronos glTF Sample Assets (https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/CarConcep… |
| `tex/CREDITS.md` | 12 | 2026-10-04 | 13 | CC0 textures used in the city: - asphalt: asphalt_02 (Poly Haven, Rob Tuytel, CC0) - footpath: concrete_pavement (Poly Haven, Charlotte Baglioni, CC0) - brick:… |

Data: 7 files, 0.2 MB (.json); unpointed: 2.

Binary: 102 files, 68.1 MB (66 .glb, 32 .jpg, 3 .bin, 1 .png).

### Real-world/game/src

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `client/audio.ts` | 224 | 2026-10-04 | 3 | Synthesised street sound: no audio files to download. A filtered-noise traffic bed that swells with nearby vehicles, a faint city murmur, and positional horns … |
| `client/autodrive.ts` | 634 | 2026-10-05 | 7 |  |
| `client/avatar.ts` | 147 | 2026-10-04 | 3 |  |
| `client/carmodel.ts` | 131 | 2026-10-04 | 4 |  |
| `client/carphysics.ts` | 691 | 2026-10-04 | 12 |  |
| `client/cities.ts` | 94 | 2026-10-05 | 4 | Per-city look and rules. The zone name in the URL (?city=finglas) picks one. |
| `client/crowd.ts` | 350 | 2026-10-04 | 6 |  |
| `client/drive.ts` | 577 | 2026-10-04 | 8 |  |
| `client/facade.ts` | 475 | 2026-10-05 | 22 |  |
| `client/g29.ts` | 429 | 2026-10-04 | 7 | Direct Logitech G29 / G923 (PlayStation) driver over WebHID. |
| `client/gardens.ts` | 315 | 2026-10-04 | 6 |  |
| `client/globe.css` | 73 | 2026-10-04 | 1 |  |
| `client/globe.ts` | 296 | 2026-10-04 | 4 |  |
| `client/graphics.ts` | 172 | 2026-10-05 | 5 |  |
| `client/grass.ts` | 153 | 2026-10-05 | 3 |  |
| `client/input.ts` | 121 | 2026-10-04 | 2 | Keyboard (WASD / arrows, Shift to run) and touch: a floating joystick on the left half of the screen, camera drag on the right half. |
| `client/main.ts` | 1392 | 2026-10-05 | 10 |  |
| `client/map.ts` | 333 | 2026-10-04 | 4 |  |
| `client/mirrors.ts` | 88 | 2026-10-04 | 3 |  |
| `client/models.ts` | 116 | 2026-10-05 | 8 |  |
| `client/nav.ts` | 374 | 2026-10-04 | 8 |  |
| `client/net.ts` | 138 | 2026-10-04 | 2 |  |
| `client/nightfx.ts` | 29 | 2026-10-04 | 3 |  |
| `client/props.ts` | 396 | 2026-10-04 | 13 |  |
| `client/roadnet.ts` | 341 | 2026-10-04 | 21 | The road rules of a place, baked from a SUMO network (tools/bake/bake_net.py): every lane with its shape and speed limit, how lanes connect through each juncti… |
| `client/roadrender.ts` | 258 | 2026-10-04 | 8 |  |
| `client/roadsigns.ts` | 300 | 2026-10-05 | 6 |  |
| `client/rules.ts` | 206 | 2026-10-04 | 12 |  |
| `client/search.ts` | 105 | 2026-10-04 | 3 | Map search: places, streets and house numbers. House numbers come from OpenStreetMap (tools/bake/osm_features.py); in Finglas OSM has about a quarter of them (… |
| `client/streetdetail.ts` | 186 | 2026-10-04 | 3 |  |
| `client/style.css` | 227 | 2026-10-04 | 1 |  |
| `client/sun.ts` | 55 | 2026-10-05 | 4 | Where the sun is in the sky for a place and a moment: NOAA's solar position equations (fractional year, declination, equation of time, hour angle; NOAA Global … |
| `client/textures.ts` | 122 | 2026-10-04 | 8 |  |
| `client/traffic.ts` | 350 | 2026-10-04 | 5 |  |
| `client/trafficnet.ts` | 1108 | 2026-10-05 | 21 |  |
| `client/trees.ts` | 157 | 2026-10-05 | 5 |  |
| `client/wheel.ts` | 500 | 2026-10-04 | 7 |  |
| `client/world.ts` | 1012 | 2026-10-05 | 14 |  |
| `server/index.ts` | 27 | 2026-10-04 | 0 |  |
| `server/zone.ts` | 307 | 2026-10-04 | 1 |  |
| `shared/moderation.ts` | 50 | 2026-10-04 | 1 | First-line chat filter. Runs on the server for every message, so it must be cheap and deterministic. It targets the scams common on Nigerian platforms: phone n… |
| `shared/protocol.ts` | 132 | 2026-10-04 | 5 | Wire protocol shared by the game client and the zone server. |

Data: 1 files, 0.0 MB (.json); unpointed: 0.

### Real-world/game/tests

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `autodrive-people.test.mts` | 69 | 2026-10-05 | 1 | The dev autodrive stops for a person in the road anywhere on its route, not only on the crossing of the next junction. Bug reproduced (Mac screenshot runs, hap… |
| `autodrive.test.mts` | 121 | 2026-10-05 | 0 | Dev autodrive (autodrive.ts), headless on the real Finglas network with real traffic, the real car physics and the examiner: the four drivers do what their tes… |
| `carlights.test.mts` | 25 | 2026-10-05 | 0 | Traffic cars' lights from what they're doing (trafficnet.ts carLights): -1 indicates left, 1 right, as the player's indicator does. |
| `check.ts` | 33 | 2026-10-04 | 25 | Tiny pass/fail helpers for the headless tests (run with tsx). Each test file calls check()/within() and finally done(), which sets the exit code. |
| `crowd.test.mts` | 114 | 2026-10-04 | 1 | The human pedestrians' stride logic and loading (crowd.ts), headless. The drawing itself needs a GPU; everything that decides who a pedestrian is, which clip t… |
| `examiner.test.mts` | 55 | 2026-10-04 | 0 | The examiner (rules.ts) on a real Finglas signalled junction: a careless drive (too fast, no signal, no mirrors, through the red) collects faults; a careful on… |
| `ffb.test.mts` | 82 | 2026-10-04 | 0 | The wheel's output pacing (research/11-wheel-ffb.md): one report in flight, newest value per channel, no stop/restart at zero, values in the ranges the Logitec… |
| `gardens.test.mts` | 98 | 2026-10-04 | 0 | Front gardens on the real Finglas map (gardens.ts), headless: where the walls, hedges, driveways and bins go, and that nothing lands somewhere a car or a house… |
| `grass.test.mts` | 36 | 2026-10-05 | 0 | Grass blades near the camera (grass.ts). What the GPU draws is checked on the Mac; these are the numbers and cells the shader relies on. |
| `hooks.test.mts` | 34 | 2026-10-04 | 0 | The Claude-side git guard blocks commands that go around the repo's git hooks, and nothing else: a false block stops honest work. |
| `input.test.mts` | 54 | 2026-10-04 | 0 | Keyboard and wheel together (wheel.ts), headless: a plugged-in wheel with its pedals at rest must not silently cancel the keyboard. |
| `models.test.mts` | 53 | 2026-10-05 | 0 | The shipped models carry what the game reads from them (docs/blender-assets.md): named empties at their real positions, named lenses and lights, four named whe… |
| `nav.test.mts` | 65 | 2026-10-04 | 0 | The sat-nav (nav.ts) on real Finglas, headless. |
| `network.test.mts` | 66 | 2026-10-04 | 1 | The baked Finglas road network carries what the driving test turns on: roundabouts, mini-roundabouts with give-way-to-the-right, multi-lane roads, signals, rea… |
| `overtake.test.mts` | 139 | 2026-10-05 | 1 | Traffic doesn't swing into the oncoming lane round a player who is waiting. Bug reproduced (Mac screenshot run svc/005-006, and headless: 17 times in 80 minute… |
| `paintmask.test.mts` | 34 | 2026-10-05 | 1 | Finding a car's paint in its body texture (tools/assets/paintmask.py, run by build_traffic_cars.py): the paint is tinted per car in the game, so getting it wro… |
| `pedestrians.test.mts` | 46 | 2026-10-04 | 1 | Walkers' legs keep pace with how far they actually walk, whatever the frame rate: the stride phase gained per metre is the same at 30 and 120 fps, and one huge… |
| `physics.test.mts` | 151 | 2026-10-04 | 0 | The car physics against published figures (research/08-vehicle-physics.md): a VW Polo 1.0 TSI DSG for the test car, and a loaded HiAce-class danfo. |
| `repo.test.mts` | 41 | 2026-10-04 | 0 | The project's standing rules that can be checked in the files themselves: every asset is credited, and no personal data or keys are committed. |
| `run.mjs` | 16 | 2026-10-04 | 1 | Runs every tests/*.test.mts with tsx, one after another, and fails if any fails. |
| `search.test.mts` | 46 | 2026-10-04 | 0 | Map search (search.ts) on the real Finglas data: house numbers from OSM, places, streets. Test addresses are picked from the data, never typed in. |
| `signals.test.mts` | 33 | 2026-10-05 | 0 | Signal placement (roadsigns.ts signalPlacement), shared by the plain boxes and the Irish signal models: the head faces the traffic it controls, red is on top, … |
| `sun.test.mts` | 48 | 2026-10-05 | 0 | The sun is where it really is for the place and date (sun.ts, NOAA's equations), not Lagos's fixed 06:45-18:45 day used for every place before. Reference times… |
| `traffic.test.mts` | 42 | 2026-10-04 | 1 | AI traffic and pedestrians on the real Finglas network, simulated headless for three minutes of game time: they obey signals, people stay off car lanes, cars d… |
| `trees.test.mts` | 75 | 2026-10-05 | 0 | Street trees with a level of detail (trees.ts): the nearest are real trees (ez-tree), the rest low-poly crowns, nothing drawn past the draw distance, and every… |
| `vehicles.test.mts` | 106 | 2026-10-05 | 0 | Real vehicle models replace the traffic's boxes (NetTraffic.setVehicleModels): a missing or empty model keeps the box, one model can serve two kinds, and every… |

Data: 1 files, 0.0 MB (.json); unpointed: 1.

### Real-world/game/tools

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `bots.mjs` | 76 | 2026-10-04 | 0 | Load test: N bots walk around a point, chat occasionally, and report what they receive. Usage: node tools/bots.mjs [count=150] [seconds=30] [url=ws://127.0.0.1… |

### Real-world/reference

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `README.md` | 13 | 2026-10-04 | 9 | Reference photos: Look at photos while modelling; don't keep them. `.gitignore` refuses everything here except this README and each asset's `preview.png` (your… |

### Real-world/reference/bollard_steel

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/bus_dublin_dd

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/bus_shelter

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/bus_stop_pole

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_service_bin_lorry

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_service_taxi

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_service_tow

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_service_truck

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_service_van

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_traffic_1

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_traffic_2

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_traffic_3

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_traffic_4

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/car_traffic_5

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/garden_wall_pier

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/garden_wall_section_1m

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/lamp_post_led

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/post_box_pillar

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/telecom_cabinet

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/traffic_signal_head

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/traffic_signal_pole

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/reference/wheelie_bin

Binary: 1 files, 0.6 MB (1 .png).

### Real-world/research

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `01-open-world-projects.md` | 402 | 2026-10-04 | 0 | 01 — Existing open-world / GTA-style / social-3D projects we can learn from, lift from, or fork: *Research date: 2026-10-04. Goal: a browser-based, GTA-Online-… |
| `02-networking-voice-moderation.md` | 436 | 2026-10-04 | 0 | 02 — Networking, Proximity Voice & Chat Moderation for a Shared-World Lagos Game: *Research date: October 2026. Prices change often; every figure below is a pl… |
| `03-real-lagos-map-pipeline.md` | 367 | 2026-10-04 | 0 | 03 — Real Lagos map pipeline (data sources, tooling, licensing): Goal: a walkable 3D version of real Lagos in the browser that runs on low-end Android phones, … |
| `04-devices-visuals-lagos-life.md` | 310 | 2026-10-04 | 0 | 04 — Devices, Visual Direction & Real Lagos Life: Research date: 2026-10-04. Scope: a browser-only, no-download, guest-first open-world social life game set in… |
| `05-driving-sim-graphics-and-world.md` | 310 | 2026-10-04 | 1 | 05 — Driving-sim graphics, "drive anywhere", physics, narration and Electron: Research date: 2026-10-04. Scope: the Electron desktop driving sim (`game/`, thre… |
| `06-teleoperator-teardown.md` | 185 | 2026-10-04 | 0 | 06 — Teleoperator (teleoperator.mindblown.ai) teardown: why it looks real: Research date: 2026-10-04. Read-only analysis of the public client bundle. **No code… |
| `07-djentic-marsgt-teardown.md` | 327 | 2026-10-04 | 0 | 07: Teardown of drive.djentic.ai and mars-gt.vercel.app: Date: 2026-10-04. Read-only analysis of the shipped bundles. **No code was copied into the project.** … |
| `08-vehicle-physics.md` | 94 | 2026-10-04 | 3 | 08: Vehicle physics, the industry approach and our parameters: Date: 2026-10-04. Owner's rule: research how simulators do it, then build. |
| `09-opensource-sims.md` | 451 | 2026-10-04 | 0 | 09: How open-source driving sims actually work (source-code teardown): Date: 2026-10-04. Owner's complaint: the driving is "all over the place", including the … |
| `10-commercial-sims.md` | 464 | 2026-10-04 | 0 | 10: How commercial driving games work inside, and what "Forza-level feel" needs: Date: 2026-10-04. Scope: public sources only (developer statements, official s… |
| `11-wheel-ffb.md` | 496 | 2026-10-04 | 1 | 11: Wheel input and force feedback (Logitech G29 / G923): Date: 2026-10-04. Trigger: the owner says the wheel connection feels "crazy, all over the place" (G29… |
| `12-web-driving-games.md` | 381 | 2026-10-04 | 0 | 12: Web driving games: how they get their feel, and what we're missing: Date: 2026-10-04. Read-only teardown. **No code was copied into the project.** Every pr… |
| `13-driving-school-and-real-world.md` | 478 | 2026-10-04 | 0 | 13: What it takes to build a real-world driving school simulator: Date: 2026-10-04. Scope: the products closest to ours (driving-school and training simulators… |
| `14-image-blaster.md` | 46 | 2026-10-04 | 0 | 14: image-blaster (neilsonnn/image-blaster), what it is and what we can use: Date: 2026-10-04. Repo: https://github.com/neilsonnn/image-blaster (MIT). |
| `15-what-it-takes.md` | 55 | 2026-10-04 | 2 | 15: What it takes to build a real-world driving simulator: Date: 2026-10-04. This merges research 06–14 into one picture: every system a real-world driving sim… |
| `16-tokyo-teardown.md` | 370 | 2026-10-04 | 2 | 16: Teardown of jeantimex/tokyo ("Procedural Tokyo"): Date: 2026-10-04. Source: https://github.com/jeantimex/tokyo, cloned at commit `def9476` (one shallow com… |
| `17-boundless-nyc-and-digital-twins.md` | 361 | 2026-10-04 | 1 | 17: BoundlessNYC teardown, and open digital twins we could use: Date: 2026-10-04. Two parts: a teardown of [mkturkcan/boundless-nyc](https://github.com/mkturkc… |
| `18-colombo-skylines.md` | 253 | 2026-10-04 | 0 | 18: Colombo: Skylines (team-watchdog/colombo-skylines), a teardown: Date: 2026-10-04. Repo cloned at commit `190388c` (6 Sep 2024, shallow clone, so earlier hi… |
| `19-city-digital-twins.md` | 466 | 2026-10-04 | 0 | 19: Cities that publish their own 3D model, and how to import them: Date: 2026-10-04. Goal: find places whose government already publishes a 3D city model or d… |
| `20-human-npcs.md` | 323 | 2026-10-04 | 1 | 20: Human NPCs that look like people: Date: 2026-10-04. Goal: replace the box pedestrians (`traffic.ts` `walker()`, two step poses swapped per frame in `traffi… |
| `21-self-driving-for-npcs.md` | 606 | 2026-10-05 | 0 | 21: What self-driving code teaches us about NPC drivers: Date: 2026-10-04. Question: how do the serious open-source self-driving and traffic-agent projects dec… |
| `22-open-source-looked-at-on-the-mac.md` | 108 | 2026-10-05 | 0 | 22: Open-source city and driving projects, run on the Mac and read: Date: 2026-10-05. Question: which open-source projects that do what we do (a real place, re… |
| `23-vehicles-look.md` | 354 | 2026-10-05 | 0 | 23: How our traffic vehicles look, against Dublin and against games: Date: 2026-10-05. Question: from the driver's seat in Finglas, how far are our traffic veh… |
| `24-buildings-look.md` | 304 | 2026-10-05 | 0 | 24: How our buildings look, next to real Finglas and the best open renderers: Date: 2026-10-05. Question: from a car on a Finglas road, what makes our houses, … |
| `25-roads-look.md` | 306 | 2026-10-05 | 0 | 25: How our roads look, against Irish standards and good games: Date: 2026-10-05. Question: how far are our streets (surface, markings, kerbs, footpaths, junct… |

### Real-world/research/data

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `extrude_budget_prototype.py` | 54 | 2026-10-04 | 1 |  |
| `overture_bbox_fetch.py` | 36 | 2026-10-04 | 1 |  |

Data: 3 files, 1.0 MB (.csv, .json); unpointed: 0.

Binary: 14 files, 16.2 MB (10 .parquet, 2 .tif, 1 .png, 1 .gz).

### Real-world/tools/assets

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `build_bus.py` | 239 | 2026-10-05 | 3 | Build bus_dublin_dd.glb (docs/blender-assets.md, section 2) in Blender. |
| `build_service_vehicles.py` | 217 | 2026-10-05 | 3 | Build the service vehicles (bin lorry, postal van, service truck, tow truck, taxi) from a CC-BY base. |
| `build_street_furniture.py` | 527 | 2026-10-05 | 5 | Build the Finglas street furniture (docs/blender-assets.md, section 4) in Blender. |
| `build_traffic_cars.py` | 293 | 2026-10-05 | 5 | Build car_traffic_1..5.glb (docs/blender-assets.md, section 3) from a CC-BY base. |
| `fetch_polyhaven_models.py` | 59 | 2026-10-05 | 0 | Download CC0 Poly Haven models (glTF, 1k textures) into assets-src/polyhaven/<id>/. |
| `fetch_textures.py` | 99 | 2026-10-04 | 3 | Download the CC0 texture sets the city shader uses into game/public/tex/. |
| `paintmask.py` | 40 | 2026-10-05 | 3 | Find the paint in a car's body texture (pure NumPy, so it's testable without Blender). |
| `people/.gitignore` | 2 | 2026-10-04 | 4 |  |
| `people/build_people.mjs` | 227 | 2026-10-04 | 4 | Builds the game's pedestrians from Microsoft Rocketbox (MIT, https://github.com/microsoft/Microsoft-Rocketbox). See research/20-human-npcs.md. |

Data: 2 files, 0.0 MB (.json); unpointed: 0.

### Real-world/tools/bake

| file | lines | changed | refs | what it says it is |
|---|---|---|---|---|
| `add_place.py` | 144 | 2026-10-04 | 4 | Bake a real place into the game in one command, and list it on the world map. |
| `bake_net.py` | 305 | 2026-10-04 | 6 | Pack a SUMO .net.xml into the game's compact road-rules file (LNT1). |
| `bake_world.py` | 346 | 2026-10-04 | 11 | Bake a playable world tile from Overture Maps extracts. |
| `build_net.sh` | 27 | 2026-10-04 | 5 | Build a SUMO road network (lanes, right-of-way, signal programs, footpaths, crossings) from an OSM file: real OSM when it could be fetched (lanes, turn lanes, … |
| `fetch_heights.py` | 95 | 2026-10-04 | 2 | Fetch Google Open Buildings 2.5D Temporal (2023) building heights for a bbox. |
| `mini_roundabouts.py` | 53 | 2026-10-04 | 3 | Mark mini-roundabouts in a SUMO network so everyone gives way to traffic on them. |
| `osm_features.py` | 132 | 2026-10-04 | 5 | Bake the OSM features that aren't roads: street lamps, house numbers, walls and hedges. |
| `osm_fetch.py` | 157 | 2026-10-04 | 3 | Fetch real OpenStreetMap road data for a bounding box, for SUMO's netconvert. |
| `overture_fetch.py` | 36 | 2026-10-04 | 1 |  |
| `overture_to_osm.py` | 190 | 2026-10-04 | 2 | Rebuild an OSM XML file from Overture transportation + infrastructure. |

Data: 1 files, 0.0 MB (.json); unpointed: 0.
