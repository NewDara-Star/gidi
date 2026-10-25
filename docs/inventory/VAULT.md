# The documents, as a vault

Made by `scripts/inventory.py` with `scripts/doc_vault.py`: every markdown document in gidi, gidi-game and gidi-data, what it is for (its title, first line and the words that mark it out), what it links to, what points to it, and the documents nearest it in words. The repo folders open as a vault in Obsidian as they are; `vault.json` holds the same graph.

111 documents: 0 orphans (nothing points to them), 8 near-orphans (only CODEBASE.md or OLD-MAP.md do).

## Orphans

## Near-orphans

### `gidi-data:README.md`
**gidi-data: Gidi's study store**. gidi-data: Gidi's study store: What Gidi studies Lagos from: open datasets, the Google study shots, reference pictures, the kit tests, textures and people assets. It lived inside World Drive's folder (`~/Real-world`) until 24 Oct 2026; the owner moved it out ("take out the Gidi stuff from real world").
For: datasets, shots, reference, assets, notes, scripts, deep-study, cache. Last changed 2026-10-24, 23 lines.
Links to 4: `gidi-data:research/data/pull-data.sh`, `gidi-data:research/refs/REVIEW.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/DATA-SOURCES.md`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:decisions/CODEBASE.md` (0.27); `gidi:decisions/DECISIONS.md` (0.12); `gidi:docs/DATA-SOURCES.md` (0.12).

### `gidi-data:textures/README.md`
**Gidi textures (outside the repo)**. Gidi textures (outside the repo): Downloaded 22 Oct 2026 with the owner's OK. Poly Haven, CC0 (free for any use, including a sold game). 2K maps per surface: diffuse, nor_gl (OpenGL normal: Blender; flip green for Unreal or use Unreal's flip option), rough, displacement, ao where offered.
For: plaster, flip, iron, asphalt, damaged, painted, rough, rusty. Last changed 2026-10-24, 9 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.23); `gidi:docs/look/research-buildings.md` (0.14); `gidi-game:ASSETS.md` (0.13).

### `gidi-game:README.md`
**Gidi: the game**. Gidi: the game: The Unreal Engine 5.8 project for Gidi. The city itself lives in the map repo, [NewDara-Star/gidi](https://github.com/NewDara-Star/gidi): its records (`map/<dNN>/`), drawn on the drawing board.
For: editor, scripting, level's, repo, meshy, committed, unreal, play. Last changed 2026-10-25, 48 lines.
Links to 15: `gidi-game:.mcp.json`, `gidi-game:ASSETS.md`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_surfaces.py`, `gidi-game:Content/Python/gidi_underdeck.py`, `gidi-game:docs/PERFORMANCE.md`, `gidi-game:tools/editor.sh`, `gidi-game:tools/map_build.py`, `gidi-game:tools/measure.sh`, `gidi-game:tools/mode.sh`, `gidi-game:tools/play.sh` ...
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi-game:docs/PERFORMANCE.md` (0.27); `gidi:decisions/DECISIONS.md` (0.22); `gidi:decisions/NOW.md` (0.22).

### `gidi:README.md`
**Gidi**. Gidi: The city for an open-world game: Gidi is real Lagos miniaturised, 51 districts, each street and place drawn by hand from the real one. This repo is the map. It holds every road, block, building and thing the game puts there, as records in `map/`, plus the drawing board they are made on. The game itself (the builders and the Unreal project) is
For: repos, airbus, provided, drawing, newdara-star, contributors, glo, odbl. Last changed 2026-10-25, 32 lines.
Links to 9: `gidi:CLAUDE.md`, `gidi:decisions/CODEBASE.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:docs/OLD-MAP-LESSONS.md`, `gidi:scripts/board_server.py`, `gidi:scripts/check_map.py`, `gidi:scripts/check_rules.py`, `gidi:scripts/inventory.py`, `gidi:web/board.html`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:decisions/CODEBASE.md` (0.27); `gidi:decisions/NOW.md` (0.22); `gidi:decisions/DECISIONS.md` (0.2).

### `gidi:decisions/README.md`
**Decisions and ideas**. Decisions and ideas: The owner works across more than one Claude account. This folder is the shared memory: **read it first in every session**, and add to it whenever the owner decides something or a good idea comes up. Newest first within each file.
For: session, decided, ideas, instructions, keeping, update, whenever, newest. Last changed 2026-10-24, 9 lines.
Links to 4: `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:CLAUDE.md` (0.23); `gidi:README.md` (0.13); `gidi:decisions/DECISIONS.md` (0.09).

### `gidi:decisions/story/README.md`
**The story of Gidi**. The story of Gidi: Tunde, an okada rider, in debt to the boss who runs the motor park. The city opens in three acts: Survive, Hustle, Empire.
For: paste, acts, account, boss's, story, roadmap, prototyping, empire. Last changed 2026-10-25, 18 lines.
Links to 2: `gidi:decisions/story/act-1-draft.md`, `gidi:decisions/story/acts-2-3-draft.md`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/acts-2-3-draft.md` (0.33); `gidi:decisions/story/act-1-draft.md` (0.32); `gidi:decisions/story/novels/README.md` (0.24).

### `gidi:decisions/story/novels/README.md`
**Three stories for Gidi (Claude's drafts, 15 Oct 2026, for the owner to pick from)**. Three stories for Gidi (Claude's drafts, 15 Oct 2026, for the owner to pick from): The owner asked for "two or three novels of the story" to read, pick from, and build their own. These are short stories, about 15 minutes' reading each, not full novels. Each one names the people who drive the plot and the side characters who give it colour, and it's told the way it would play in an open world.
For: story, debt, novels, drugs, stories, force, betting, task. Last changed 2026-10-25, 36 lines.
Links to 4: `gidi:decisions/story/novels/1-the-ledger.md`, `gidi:decisions/story/novels/2-union.md`, `gidi:decisions/story/novels/3-the-phone.md`, `gidi:docs/lagos-study/roads/NAMES.md`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/acts-2-3-draft.md` (0.39); `gidi:decisions/story/act-1-draft.md` (0.34); `gidi:decisions/story/README.md` (0.24).

### `gidi:docs/map-format-example/README.md`
**Worked example of the new map format**. Worked example of the new map format: One short home street in district d15 (20 m, invented names), written as the map would hold it (docs/MAP-FORMAT.md):
For: lean-to's, gutter's, lean-to, example, stand-in, shop-under-flats, bungalow's, stamped. Last changed 2026-10-22, 10 lines.
Links to 6: `gidi:docs/MAP-FORMAT.md`, `gidi:docs/map-format-example/d15/district.json`, `gidi:docs/map-format-example/d15/dress/128_60.json`, `gidi:docs/map-format-example/d15/plan.json`, `gidi:schema/kit_reads.json`, `gidi:scripts/check_map.py`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:docs/MAP-FORMAT.md` (0.25); `gidi:decisions/NOW.md` (0.13); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.13).

## Every document, by folder

## (top)
### `gidi-data:README.md`
**gidi-data: Gidi's study store**. gidi-data: Gidi's study store: What Gidi studies Lagos from: open datasets, the Google study shots, reference pictures, the kit tests, textures and people assets. It lived inside World Drive's folder (`~/Real-world`) until 24 Oct 2026; the owner moved it out ("take out the Gidi stuff from real world").
For: datasets, shots, reference, assets, notes, scripts, deep-study, cache. Last changed 2026-10-24, 23 lines.
Links to 4: `gidi-data:research/data/pull-data.sh`, `gidi-data:research/refs/REVIEW.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/DATA-SOURCES.md`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:decisions/CODEBASE.md` (0.27); `gidi:decisions/DECISIONS.md` (0.12); `gidi:docs/DATA-SOURCES.md` (0.12).

## gidi-data:research/google/estate
### `gidi-data:research/google/estate/NOTES.md`
**The Estate: Magodo, Omole, Ikeja GRA (study, 18 Oct 2026). Study only; nothing copied.**. The Estate: Magodo, Omole, Ikeja GRA (study, 18 Oct 2026). Study only; nothing copied.: - Planned: long parallel streets bending with the land, blocks ~60 m wide (two rows of plots back to back) x 200-300 m. - A main drive cuts across; closes end at the estate's edge (the green valley); a clear edge between estate and bush. - Plots in even rows, houses set back with compound walls; roofs: terracotta, grey, some blue.
For: valley, unplanned, rows, drive, parallel, planned, closes, network. Last changed 2026-10-24, 26 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi:docs/estate-pattern-study.md` (0.15); `gidi:docs/lagos-study/STUDY.md` (0.11); `gidi-data:research/google/maze/NOTES.md` (0.11).

## gidi-data:research/google/ibudo
### `gidi-data:research/google/ibudo/NOTES.md`
**Ìbùdó study: Oshodi (19 Oct 2026). Study only: nothing here is copied into Gidi.**. Ìbùdó study: Oshodi (19 Oct 2026). Study only: nothing here is copied into Gidi.: Views (Google Maps / Street View, Jul 2021 and Apr 2024): 01 interchange from above (300 m): the expressway crossing, the Terminal 3 oval, the footbridge, the market west of it. 02 market and bridge from above (250 m): Oshodi Market's red roofs packed between Oshodi Rd and the rail; dense shops.
For: adekoya, twin, oshodi, steel, shop, awnings, poles, footbridge. Last changed 2026-10-24, 35 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/ibudo/study/INVENTORY.md` (0.21); `gidi:docs/look/research-transport.md` (0.19); `gidi:docs/look/research-commerce.md` (0.19).

## gidi-data:research/google/ibudo/study
### `gidi-data:research/google/ibudo/study/INVENTORY.md`
**Ìbùdó study, phase 1: Oshodi and Ojuelegba inventory (19 Oct 2026)**. Ìbùdó study, phase 1: Oshodi and Ojuelegba inventory (19 Oct 2026): Study only, from Google Maps satellite with labels and Street View. Nothing here is traced or copied into Gidi; it describes how the two real places are built and how they work, so Ìbùdó's streets and places can be invented from them.
For: cres, oshodi, ojuelegba, yaba, arena, army, stadium, ilupeju. Last changed 2026-10-24, 280 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 2 code files (`gidi:scripts/code_graph.py`, `gidi:scripts/inventory.py`).
Nearest in words: `gidi-data:research/google/ibudo/NOTES.md` (0.21); `gidi:docs/lagos-study/STUDY.md` (0.19); `gidi:docs/lagos-lgas-research.md` (0.18).

## gidi-data:research/google/kits/old-town
### `gidi-data:research/google/kits/old-town/KIT.md`
**Dense old town kit**. Dense old town kit: This is the kit list for the dense old towns of Lagos, ready for the owner to check. It is built only from the Street View shots in this folder. Their notes are in `shots.tsv`. A number like ot42 means shot `ot42_*.jpg`.
For: eyes, shots, desk, steel, example, sheet, timber, fields. Last changed 2026-10-24, 682 lines.
Links to 2: `gidi-data:research/google/kits/old-town/tests/facade_hand.py`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`
Backlinks: 11 documents (`gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md`, `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md`, `gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md`, `gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md`, `gidi-game:Art/Props/LeantoBuilt/GAPS.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md` ...), 6 code files (`gidi-data:research/google/kits/old-town/tests/ot13/mk13_first.py`, `gidi-data:research/google/kits/old-town/tests/ot149/mk149_first.py`, `gidi-data:research/google/kits/old-town/tests/ot45/mk45_first.py`, `gidi-data:research/google/kits/old-town/tests/ot73/mk73_first.py`, `gidi-game:tools/road_build.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.2); `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.18); `gidi:decisions/NOW.md` (0.18).

## gidi-data:research/google/kits/old-town/tests/ot149
### `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md`
**Kit eye test 3: ot149, Mushin, Ayantuga St (Street View, Jul 2021, heading 180)**. Kit eye test 3: ot149, Mushin, Ayantuga St (Street View, Jul 2021, heading 180): The test: do the kit's parts hold on a third street they were not made for? The owner's eye judges. This is not a pass.
For: apron, turned, photo, photo's, cage, render, toned, camera. Last changed 2026-10-24, 79 lines.
Links to 5: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/ot149/hand149.py`, `gidi-data:research/google/kits/old-town/tests/ot149/mk149_first.py`, `gidi-data:research/google/kits/old-town/tests/ot149/mk149_pass.py`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.34); `gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md` (0.31); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.3).

## gidi-data:research/google/kits/old-town/tests/ot175
### `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md`
**Kit eye test 1: ot175, Ilasamaja/Mushin, Olayiwola Liasu St (Jul 2021)**. Kit eye test 1: ot175, Ilasamaja/Mushin, Olayiwola Liasu St (Jul 2021): `side_by_side.jpg` shows the Street View on the left and the rebuild on the right, both 1200x670. It is now pass 3 (ground, sun, clutter, grime), also saved as `sbs_p3_final.jpg`. The earlier passes, in order: `sbs_v1.jpg`-`sbs_v3.jpg` (untextured), `sbs_tex1_first.jpg` and `sbs_tex2.jpg` (textured), `sbs_p3_first.jpg` (pass 3's first try). `map_pass2.json` is the map as it stood before pass 3.
For: reused, pass, camera, darker, sacks, textured, colour, ruts. Last changed 2026-10-24, 234 lines.
Links to 2: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/facade_hand.py`
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.33); `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md` (0.3); `gidi:decisions/NOW.md` (0.25).

## gidi-data:research/google/kits/old-town/tests/ot45
### `gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md`
**Kit eye test 5: ot45, Mushin, Ladipo St (Street View, Jul 2021, heading 180)**. Kit eye test 5: ot45, Mushin, Ladipo St (Street View, Jul 2021, heading 180): The test: do the kit's parts hold on a fifth street they were not made for? The owner's eye judges. This is not a pass.
For: photo's, tractor, rubbish, bonneted, desk, dirt, flatbed, wings. Last changed 2026-10-24, 137 lines.
Links to 12: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`, `gidi-data:research/google/kits/old-town/tests/ot45/closeups45.sh`, `gidi-data:research/google/kits/old-town/tests/ot45/hand45.py`, `gidi-data:research/google/kits/old-town/tests/ot45/hand45_2.py`, `gidi-data:research/google/kits/old-town/tests/ot45/mk45_first.py`, `gidi-data:research/google/kits/old-town/tests/ot45/mk45_pass.py`, `gidi-data:research/google/kits/old-town/tests/ot45/run45.sh`, `gidi-data:research/google/kits/old-town/tests/ot45/sbs.py`, `gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:scripts/check_rules.py`
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md` (0.27); `gidi:decisions/NOW.md` (0.27); `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.26).

## gidi-data:research/google/kits/old-town/tests/ot73
### `gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`
**Kit eye test 4: ot73, Epe, Ogunmule Akinlogba St (Street View, May 2024, heading 180)**. Kit eye test 4: ot73, Epe, Ogunmule Akinlogba St (Street View, May 2024, heading 180): The test: do the kit's parts hold on a fourth street they were not made for? The owner's eye judges. This is not a pass.
For: photo's, drafted, kerbs, balls, grass, rider, fence, lean. Last changed 2026-10-24, 76 lines.
Links to 6: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/ot149/closeups149.sh`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`, `gidi-data:research/google/kits/old-town/tests/ot73/hand73.py`, `gidi-data:research/google/kits/old-town/tests/ot73/mk73_first.py`, `gidi-data:research/google/kits/old-town/tests/ot73/mk73_pass.py`
Backlinks: 1 documents (`gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md` (0.31); `gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md` (0.27); `gidi:decisions/NOW.md` (0.22).

## gidi-data:research/google/kits/old-town/tests/ot91
### `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md`
**Kit eye test 2: ot91, Isale Eko, Balogun area (Street View, date n/a, heading 0)**. Kit eye test 2: ot91, Isale Eko, Balogun area (Street View, date n/a, heading 0): The test: do the parts built for ot175 hold on a street they were not made for? The owner's eye judges. This is not a pass.
For: jitter, stored, positions, goods, scaffold, records, test, render. Last changed 2026-10-24, 168 lines.
Links to 2: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/facade_hand.py`
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md` (0.34); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.33); `gidi:decisions/NOW.md` (0.28).

## gidi-data:research/google/kits/old-town/tests/ut01_emmanuel
### `gidi-data:research/google/kits/old-town/tests/ut01_emmanuel/inventory.md`
**Ultimate test 1: Shomolu, Emmanuel St junction (Street View, Jul 2021), three angles**. Ultimate test 1: Shomolu, Emmanuel St junction (Street View, Jul 2021), three angles: The owner's ultimate test (DECISIONS, 23 Oct): list every thing in the real pictures, model each one clean to a standard look (whole, from every side, wear as a layer), rebuild the picture from those things alone, then rebuild the other angles.
For: angles, crates, emmanuel, gidi-game, bench, pallet, pickup, timber. Last changed 2026-10-24, 102 lines.
Links to 8: `gidi-game:tools/block_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/pickup_build.py`, `gidi-game:tools/pole_build.py`, `gidi-game:tools/stall_build.py`, `gidi-game:tools/umbrella_build.py`, `gidi-game:tools/wall_build.py`
Backlinks: 2 documents (`gidi:decisions/CHECKS.md`, `gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:decisions/NOW.md` (0.3); `gidi-game:docs/ASSET-INVENTORY.md` (0.29); `gidi:docs/look/research-housing.md` (0.2).

## gidi-data:research/google/maze
### `gidi-data:research/google/maze/NOTES.md`
**The Maze: Mushin + Shomolu (study, 18 Oct 2026). Screenshots are for study only; nothing here is copied into Gidi.**. The Maze: Mushin + Shomolu (study, 18 Oct 2026). Screenshots are for study only; nothing here is copied into Gidi.: - Coverage: Mushin 75-85% roof, Shomolu ~85%. Almost no open ground; sand only in small yards. - Grain: long terraced one- and two-storey houses (~10 m deep, 15-30 m long), in rows along the streets; block interiors filled with more rows reached by 1-3 m alleys. Blocks ~60 x 150 m.
For: shomolu, mushin, terraced, hierarchy, alleys, curving, coverage, interiors. Last changed 2026-10-24, 15 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.2); `gidi-data:research/google/estate/NOTES.md` (0.11); `gidi:docs/look/research-buildings.md` (0.11).

## gidi-data:research/google/twins
### `gidi-data:research/google/twins/NOTES.md`
**(no title)**. Twins outside Ìbùdó (Street View, 19 Oct): ikorodu_kokoro_abu_st_sprawl_stalls (Feb 2017): a sprawl street, tar with sandy edges, a long row of zinc-roofed stalls on timber posts selling bags and plastics, an open drain with tyres, bungalows, palms, okadas. Twin: sprawl street, shed row, open gutter.
For: sprawl, kokoro, twins, zinc-roofed, plastics, selling, stalls, sandy. Last changed 2026-10-24, 3 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/ibudo/NOTES.md` (0.17); `gidi:docs/border-pattern-study.md` (0.1); `gidi:docs/look/research-commerce.md` (0.1).

## gidi-data:research/google/video1-street
### `gidi-data:research/google/video1-street/NOTES.md`
**Video 1 street: reference notes (22 Oct 2026)**. Video 1 street: reference notes (22 Oct 2026): Video 1 (`../../refs/video1/`) is an AI-made "Lagos game" clip. It shows a third-person view under a flyover, a levy quest, danfos, a crowd and stalls, and wet broken ground with litter. These notes say what the real places look like, so the test street is built from Lagos and not from the clip.
For: deck, piers, palisade, kerb, obalende, ojuelegba, shade, buses. Last changed 2026-10-24, 51 lines.
Links to 0: 
Backlinks: 2 documents (`gidi-data:research/google/kits/old-town/tests/ot73/NOTES.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi:docs/look/research-transport.md` (0.23); `gidi:docs/look/research-street.md` (0.18); `gidi-data:research/google/ibudo/NOTES.md` (0.16).

## gidi-data:research/refs
### `gidi-data:research/refs/REVIEW.md`
**Reference review (Claude, 15 Oct 2026): for the owner to correct and tag**. Reference review (Claude, 15 Oct 2026): for the owner to correct and tag: Numbers match the contact sheets (sorted by file name). **Not Lagos** means not Lagos, Nigeria, in my view. Commons matched the Spanish and Portuguese word *lago* ("lake") and the town of Lagos in Portugal. Nothing is deleted yet: confirm and I'll remove them.
For: assets, portugal, umbrellas, tomato, question, yaba, oshodi, green-black. Last changed 2026-10-24, 126 lines.
Links to 0: 
Backlinks: 3 documents (`gidi-data:README.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/hand/maze-hub-lagos.md`), 0 code files ().
Nearest in words: `gidi-data:research/google/ibudo/NOTES.md` (0.18); `gidi:docs/look/research-commerce.md` (0.15); `gidi-data:research/google/ibudo/study/INVENTORY.md` (0.15).

## gidi-data:textures
### `gidi-data:textures/README.md`
**Gidi textures (outside the repo)**. Gidi textures (outside the repo): Downloaded 22 Oct 2026 with the owner's OK. Poly Haven, CC0 (free for any use, including a sold game). 2K maps per surface: diffuse, nor_gl (OpenGL normal: Blender; flip green for Unreal or use Unreal's flip option), rough, displacement, ao where offered.
For: plaster, flip, iron, asphalt, damaged, painted, rough, rusty. Last changed 2026-10-24, 9 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.23); `gidi:docs/look/research-buildings.md` (0.14); `gidi-game:ASSETS.md` (0.13).

## (top)
### `gidi-game:ASSETS.md`
**Hand-made assets**. Hand-made assets: | Asset | Where | Source | Status | |---|---|---|---| | Danfo Basic 2.0 (font): the owner's danfo lettering (BirdFont, July 2022), spaced, kerned and given punctuation by script (tools/font_space.py, font_punct.py) | Art/Fonts/DanfoBasic.ttf (built by tools/font_build.sh from Art/Fonts/src: the 2022 letters and Alfa Slab One) | the owner, built on Alfa Slab One (JM Solé), SIL Open Font License 1.1 (Art/Fonts/OFL.txt) | to use: danfo bodywork, signboards, the game's titles |
For: content, font, claude, tools, makehuman, gidiplate, ambientcg, plates. Last changed 2026-10-25, 36 lines.
Links to 32: `gidi-game:Art/People/hawker/hawker.blend`, `gidi-game:Art/People/hawker/spec.json`, `gidi-game:Art/Plates/plates.json`, `gidi-game:Art/Vehicles/BrtBuilt/brt_parts.blend`, `gidi-game:Art/Vehicles/BrtBuilt/brt_red_parts.blend`, `gidi-game:Art/Vehicles/BrtBuilt/red.json`, `gidi-game:Art/Vehicles/Danfo/danfo.blend`, `gidi-game:Art/Vehicles/KekeBuilt/keke_parts.blend`, `gidi-game:Art/Vehicles/MolueBuilt/molue_parts.blend`, `gidi-game:Art/Vehicles/Okada/okada.blend`, `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_plates.py` ...
Backlinks: 4 documents (`gidi-game:CLAUDE.md`, `gidi-game:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`), 2 code files (`gidi-game:.gitignore`, `gidi-game:Content/Python/gidi_underdeck.py`).
Nearest in words: `gidi-game:docs/ASSET-INVENTORY.md` (0.22); `gidi:decisions/IDEAS.md` (0.18); `gidi:decisions/DECISIONS.md` (0.17).

## gidi-game:Art/Buildings/BlockBuilt
### `gidi-game:Art/Buildings/BlockBuilt/ROOF-GAPS.md`
**Zinc on the block's roof: the gaps**. Zinc on the block's roof: the gaps: The rebuild rule (gidi DECISIONS "Rebuild the old kit's things the new way"): the old roof beside real ones, the gaps written down, the new build beside the same photos with each gap marked. The sheet: `roof_look_v1.jpg` (the photos are Street View, kept for study only: ot17 14 Oyeshile St, ot25 50 Alasalat St, ot42 11 Raufu Alajo St, ot172 5 Rasheed
For: sheets, sheet, eave, closed, format, lapped, ribs, roof's. Last changed 2026-10-24, 28 lines.
Links to 2: `gidi-game:Art/Props/LeantoBuilt/GAPS.md`, `gidi-game:tools/zinc_kit.py`
Backlinks: 2 documents (`gidi-game:Art/Props/LeantoBuilt/GAPS.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/zinc_kit.py`).
Nearest in words: `gidi-game:Art/Props/LeantoBuilt/GAPS.md` (0.51); `gidi:decisions/NOW.md` (0.14); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.13).

## gidi-game:Art/Props/LeantoBuilt
### `gidi-game:Art/Props/LeantoBuilt/GAPS.md`
**The zinc lean-to: the old kit against the real ones**. The zinc lean-to: the old kit against the real ones: The first rebuild under gidi DECISIONS "Rebuild the old kit's things the new way" (24 Oct). Before building, the old kit's lean-to (the ot175 kit eye test, pass 5: `~/gidi-data/research/google/kits/old-town/tests/ot175/closeups/goods_sbs.jpg`)
For: purlins, lapped, beam, sheet, lean-to, rust, sheets, closed. Last changed 2026-10-24, 39 lines.
Links to 5: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-game:Art/Buildings/BlockBuilt/ROOF-GAPS.md`, `gidi-game:tools/leanto_build.py`, `gidi-game:tools/vehicle_look.py`, `gidi-game:tools/zinc_kit.py`
Backlinks: 2 documents (`gidi-game:Art/Buildings/BlockBuilt/ROOF-GAPS.md`, `gidi:decisions/NOW.md`), 1 code files (`gidi-game:tools/zinc_kit.py`).
Nearest in words: `gidi-game:Art/Buildings/BlockBuilt/ROOF-GAPS.md` (0.51); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.14); `gidi:decisions/NOW.md` (0.14).

## (top)
### `gidi-game:CLAUDE.md`
**Gidi game (Unreal)**. Gidi game (Unreal): Read the map repo's `decisions/` first (`~/gidi/decisions/NOW.md`, `DECISIONS.md`): the same rules apply here.
For: push, repo's, commit, generates, commands, unreal, paragraph, master. Last changed 2026-10-24, 13 lines.
Links to 4: `gidi-game:.claude/settings.json`, `gidi-game:ASSETS.md`, `gidi-game:tools/kit_fields.py`, `gidi:decisions/DECISIONS.md`
Backlinks: 4 documents (`gidi:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/HISTORY.md`, `gidi:decisions/NOW.md`), 22 code files (`gidi:.claude/hooks/checked-before-commit.sh`, `gidi:.claude/hooks/checks-before-commit.sh`, `gidi:.claude/hooks/checks-before-stop.sh`, `gidi:.claude/hooks/repo.sh`, `gidi:.claude/hooks/review-before-push.sh`).
Nearest in words: `gidi:CLAUDE.md` (0.37); `gidi-game:README.md` (0.17); `gidi:decisions/CHECKS.md` (0.13).

### `gidi-game:README.md`
**Gidi: the game**. Gidi: the game: The Unreal Engine 5.8 project for Gidi. The city itself lives in the map repo, [NewDara-Star/gidi](https://github.com/NewDara-Star/gidi): its records (`map/<dNN>/`), drawn on the drawing board.
For: editor, scripting, level's, repo, meshy, committed, unreal, play. Last changed 2026-10-25, 48 lines.
Links to 15: `gidi-game:.mcp.json`, `gidi-game:ASSETS.md`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_surfaces.py`, `gidi-game:Content/Python/gidi_underdeck.py`, `gidi-game:docs/PERFORMANCE.md`, `gidi-game:tools/editor.sh`, `gidi-game:tools/map_build.py`, `gidi-game:tools/measure.sh`, `gidi-game:tools/mode.sh`, `gidi-game:tools/play.sh` ...
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi-game:docs/PERFORMANCE.md` (0.27); `gidi:decisions/DECISIONS.md` (0.22); `gidi:decisions/NOW.md` (0.22).

## gidi-game:docs
### `gidi-game:docs/ASSET-INVENTORY.md`
**What's already in the project (check here before building anything)**. What's already in the project (check here before building anything): The owner's rule (19 Oct): look at what we have before building from scratch. Gidi's own things (danfo, keke, molue, BRT, plates, brand, labels) are built by us; everything else starts from these. Paths are under `Content/`.
For: recipes, tools, manny, asphalt, concrete, animations, map's, build. Last changed 2026-10-23, 21 lines.
Links to 9: `gidi-game:tools/block_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/pickup_build.py`, `gidi-game:tools/pole_build.py`, `gidi-game:tools/stall_build.py`, `gidi-game:tools/umbrella_build.py`, `gidi-game:tools/wall_build.py`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 2 code files (`gidi-game:.gitignore`, `gidi-game:tools/underdeck_build.py`).
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ut01_emmanuel/inventory.md` (0.29); `gidi-game:ASSETS.md` (0.22); `gidi:decisions/NOW.md` (0.18).

### `gidi-game:docs/PERFORMANCE.md`
**Performance: modes, near detail, streaming, budgets**. Performance: modes, near detail, streaming, budgets: The owner's rule (gidi `decisions/DECISIONS.md`, 22 Oct, "Build light, look full"): build in a light mode, play in the mode the machine can carry, flip to full only to look and take pictures. Near things carry detail and far things are simple. What the camera can't see is not drawn. The world streams in pieces around the player. Every level has a budget,
For: tools, mode, lumen, editor, play, modes, unrealeditor, saved. Last changed 2026-10-25, 286 lines.
Links to 16: `gidi-game:Config/DefaultDeviceProfiles.ini`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:tools/editor.sh`, `gidi-game:tools/img_diff.py`, `gidi-game:tools/lap_check.py`, `gidi-game:tools/measure.sh`, `gidi-game:tools/measure_csv.py`, `gidi-game:tools/memreport.sh`, `gidi-game:tools/mode.sh`, `gidi-game:tools/mode_sg.py`, `gidi-game:tools/package.sh`, `gidi-game:tools/piece_match.py` ...
Backlinks: 4 documents (`gidi-game:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`), 8 code files (`gidi-game:Config/DefaultDeviceProfiles.ini`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:tools/look_travels.py`, `gidi-game:tools/measure.sh`, `gidi-game:tools/measure_csv.py`).
Nearest in words: `gidi-game:README.md` (0.27); `gidi-game:docs/ASSET-INVENTORY.md` (0.16); `gidi:decisions/NOW.md` (0.16).

## (top)
### `gidi:CLAUDE.md`
**Gidi**. Gidi: An open-world city inspired by Lagos, built from data and by hand. The owner works across more than one Claude account.
For: commit, trial, checked, forget, push, showed, session, hook. Last changed 2026-10-25, 22 lines.
Links to 6: `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:docs/OLD-KIT.md`, `gidi:scripts/inventory.py`
Backlinks: 4 documents (`gidi:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/HISTORY.md`, `gidi:decisions/NOW.md`), 22 code files (`gidi:.claude/hooks/checked-before-commit.sh`, `gidi:.claude/hooks/checks-before-commit.sh`, `gidi:.claude/hooks/checks-before-stop.sh`, `gidi:.claude/hooks/repo.sh`, `gidi:.claude/hooks/review-before-push.sh`).
Nearest in words: `gidi-game:CLAUDE.md` (0.37); `gidi:decisions/DECISIONS.md` (0.27); `gidi:decisions/CHECKS.md` (0.23).

### `gidi:README.md`
**Gidi**. Gidi: The city for an open-world game: Gidi is real Lagos miniaturised, 51 districts, each street and place drawn by hand from the real one. This repo is the map. It holds every road, block, building and thing the game puts there, as records in `map/`, plus the drawing board they are made on. The game itself (the builders and the Unreal project) is
For: repos, airbus, provided, drawing, newdara-star, contributors, glo, odbl. Last changed 2026-10-25, 32 lines.
Links to 9: `gidi:CLAUDE.md`, `gidi:decisions/CODEBASE.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:docs/OLD-MAP-LESSONS.md`, `gidi:scripts/board_server.py`, `gidi:scripts/check_map.py`, `gidi:scripts/check_rules.py`, `gidi:scripts/inventory.py`, `gidi:web/board.html`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:decisions/CODEBASE.md` (0.27); `gidi:decisions/NOW.md` (0.22); `gidi:decisions/DECISIONS.md` (0.2).

## gidi:decisions
### `gidi:decisions/CHECKS.md`
**Which check holds each rule**. Which check holds each rule: Every rule in `DECISIONS.md` has a row here: the check that enforces it, or why none can. `scripts/check_rules.py` runs before every commit and push (`.claude/hooks/checks-before-commit.sh`): it fails when a rule has no row, and lists every rule marked **GAP** (a map rule nothing checks yet). So "are we covering all bases?" is
For: gidi-game, process, held, builder, rule, fails, instances, review. Last changed 2026-10-25, 96 lines.
Links to 23: `gidi-data:research/google/kits/old-town/tests/ut01_emmanuel/inventory.md`, `gidi-game:tools/fields.py`, `gidi-game:tools/kit_fields.py`, `gidi-game:tools/look_travels.py`, `gidi-game:tools/mode_sg.py`, `gidi-game:tools/play.sh`, `gidi:.claude/hooks/checked-before-commit.sh`, `gidi:.claude/hooks/checks-before-commit.sh`, `gidi:.claude/hooks/checks-before-stop.sh`, `gidi:.claude/hooks/review-before-push.sh`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/HISTORY.md` ...
Backlinks: 5 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/HISTORY.md`, `gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`), 3 code files (`gidi:.claude/hooks/repo.sh`, `gidi:.claude/hooks/review-before-push.sh`, `gidi:scripts/check_rules.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.52); `gidi:decisions/DECISIONS.md` (0.5); `gidi:decisions/CODEBASE.md` (0.36).

### `gidi:decisions/CODEBASE.md`
**What the code holds: the three repos, one page**. What the code holds: the three repos, one page: Read this before building anything new, so new work starts from what exists. Every file, with what it says it is, when it last changed and who points to it, is in `docs/inventory/INVENTORY.md`. What looks dead or broken is in `docs/inventory/SUSPECTS.md`. Since 24 Oct also (owner: "use the compiler to know what every piece of code is connected
For: scripts, gidi-game, district's, draft, inventory, board's, deleted, map's. Last changed 2026-10-25, 179 lines.
Links to 98: `gidi-game:ASSETS.md`, `gidi-game:Config/DefaultDeviceProfiles.ini`, `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:Content/Python/gidi_paint.py`, `gidi-game:Content/Python/gidi_plates.py`, `gidi-game:Content/Python/gidi_surfaces.py`, `gidi-game:Content/Python/gidi_underdeck.py`, `gidi-game:docs/ASSET-INVENTORY.md`, `gidi-game:docs/PERFORMANCE.md`, `gidi-game:tools/editor.sh` ...
Backlinks: 4 documents (`gidi:CLAUDE.md`, `gidi:README.md`, `gidi:decisions/NOW.md`, `gidi:decisions/README.md`), 3 code files (`gidi:.claude/hooks/checks-before-stop.sh`, `gidi:docs/lagos-study/similar/scripts/common.py`, `gidi:scripts/doc_vault.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.42); `gidi:decisions/CHECKS.md` (0.36); `gidi:decisions/DECISIONS.md` (0.32).

### `gidi:decisions/DECISIONS.md`
**Decisions (the owner's standing rules)**. Decisions (the owner's standing rules): What still guides the work. A decision that a later one replaced, or that held only for the old map, is in `HISTORY.md`, with what replaced it. Where a later decision changed part of one, the change is noted at its end. Each rule has a row in `CHECKS.md`. Ideas not decided yet are in `IDEAS.md`.
For: kits, we're, records, view, blender, hand, laptop, unreal. Last changed 2026-10-25, 142 lines.
Links to 26: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-game:ASSETS.md`, `gidi-game:docs/PERFORMANCE.md`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/kit_fields.py`, `gidi-game:tools/person_build.py`, `gidi-game:tools/plates.py`, `gidi-game:tools/umbrella_build.py`, `gidi:CLAUDE.md`, `gidi:decisions/CHECKS.md`, `gidi:decisions/HISTORY.md`, `gidi:decisions/IDEAS.md` ...
Backlinks: 12 documents (`gidi-data:README.md`, `gidi-game:CLAUDE.md`, `gidi-game:docs/PERFORMANCE.md`, `gidi:CLAUDE.md`, `gidi:decisions/CHECKS.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/HISTORY.md`, `gidi:decisions/NOW.md` ...), 2 code files (`gidi:.claude/hooks/review-before-push.sh`, `gidi:scripts/check_rules.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.51); `gidi:decisions/CHECKS.md` (0.5); `gidi:decisions/CODEBASE.md` (0.32).

### `gidi:decisions/HISTORY.md`
**Decisions that were replaced (history)**. Decisions that were replaced (history): The owner's decisions that later ones replaced, or that held only for the old generated map (13-21 Oct). Kept so we know what was decided before and why it changed; none of them guides new work. Moved out of `DECISIONS.md` on 24 Oct, word for
For: replaced, hand-made, miniaturised, hand, frozen, plan, builder, programs. Last changed 2026-10-25, 61 lines.
Links to 9: `gidi:CLAUDE.md`, `gidi:decisions/CHECKS.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/OLD-MAP-LESSONS.md`, `gidi:docs/data/deep/hub.json`, `gidi:docs/hand/borrowed-lagos.md`, `gidi:scripts/check_rules.py`
Backlinks: 4 documents (`gidi:decisions/CHECKS.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:decisions/DECISIONS.md` (0.29); `gidi:decisions/CODEBASE.md` (0.24); `gidi:decisions/NOW.md` (0.22).

### `gidi:decisions/IDEAS.md`
**Ideas (not decided; newest first)**. Ideas (not decided; newest first): - **Our own Lagos motion from video, and AI video** (owner, 23 Oct). Motion2MixamoRig (github.com/MaxLiu22/Motion2MixamoRig, code Apache-2.0, experimental): a video of one person, whole body in frame, becomes motion on a Mixamo character (.glb for Blender/Unreal); Blender add-on tested on Apple Silicon, slow but fine on CPU (3-15 min per 30 s clip). Fills the gap Mixamo's library leaves: Lagos-only moves (basin on the head, conductor hanging off the door, frying akara, bargaining, climbing on an okada), filmed by the owner or friends who agree, never strangers' clips. **Catch:** it needs SMPL-X, non-commercial by default (a commercial licence is a separate deal), and the GVHMR weights have their own licence: use it for study and prototypes (person spots), then licence it or redo final animations with a sale-cleared tool before shipping. To set up (needs the owner's OK): repo + Python packages; about 5 GB of weights on first run; the SMPL-X file (owner signs up on the SMPL-X site); a Mixamo FBX from the owner's Adobe account. Mixamo itself: free library, retarget onto City Sample/MetaHuman in Unreal; usable in a shipped game, raw files not shared.
For: refs, motion, video, metahuman, yoruba, talk, danfo, sound. Last changed 2026-10-24, 68 lines.
Links to 5: `gidi:decisions/lived-in.md`, `gidi:decisions/world-life.md`, `gidi:docs/OLD-MAP-LESSONS.md`, `gidi:docs/lagos-study/LIVING.md`, `gidi:docs/lagos-study/roads/NAMES.md`
Backlinks: 5 documents (`gidi:CLAUDE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/HISTORY.md`, `gidi:decisions/README.md`, `gidi:docs/lagos-study/roads/NAMES.md`), 0 code files ().
Nearest in words: `gidi:decisions/lived-in.md` (0.24); `gidi:decisions/DECISIONS.md` (0.22); `gidi:decisions/world-life.md` (0.21).

### `gidi:decisions/NOW.md`
**Where the work stands (update at the end of every session)**. Where the work stands (update at the end of every session): **HANDOVER, 24 Oct 2026 (evening). Start here.** Read `DECISIONS.md` (the standing rules; replaced ones are in `HISTORY.md`), then this page. What the repos hold: `CODEBASE.md` and `docs/inventory/` (`scripts/inventory.py`). The real Lagos research:
For: gidi-game, pass, records, sent, unreal, editor, layer, dress. Last changed 2026-10-25, 331 lines.
Links to 79: `gidi-data:research/google/estate/NOTES.md`, `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`, `gidi-data:research/google/kits/old-town/tests/ut01_emmanuel/inventory.md`, `gidi-game:Art/Buildings/BlockBuilt/ROOF-GAPS.md`, `gidi-game:Art/Props/LeantoBuilt/GAPS.md`, `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:docs/PERFORMANCE.md`, `gidi-game:tools/block_build.py`, `gidi-game:tools/editor.sh`, `gidi-game:tools/fields.py`, `gidi-game:tools/furniture_build.py` ...
Backlinks: 4 documents (`gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md`, `gidi-game:CLAUDE.md`, `gidi:CLAUDE.md`, `gidi:decisions/README.md`), 1 code files (`gidi:.claude/hooks/review-before-push.sh`).
Nearest in words: `gidi:decisions/CHECKS.md` (0.52); `gidi:decisions/DECISIONS.md` (0.51); `gidi:decisions/CODEBASE.md` (0.42).

### `gidi:decisions/README.md`
**Decisions and ideas**. Decisions and ideas: The owner works across more than one Claude account. This folder is the shared memory: **read it first in every session**, and add to it whenever the owner decides something or a good idea comes up. Newest first within each file.
For: session, decided, ideas, instructions, keeping, update, whenever, newest. Last changed 2026-10-24, 9 lines.
Links to 4: `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:CLAUDE.md` (0.23); `gidi:README.md` (0.13); `gidi:decisions/DECISIONS.md` (0.09).

### `gidi:decisions/lived-in.md`
**The lived-in layer: what every GTA does, and Gidi's plan**. The lived-in layer: what every GTA does, and Gidi's plan: The owner asked on 24 Oct 2026 for research from public material on how GTA's worlds feel alive, across every game, and for a "lived-in layer" plan for Gidi. **A proposal, not decided.** It builds on `world-life.md` (rhythm, systems, moments, texture: *what* Gidi's life is) and the IDEAS entry "What makes Los Santos feel lived in" (23 Oct). This file is about *the machinery*: what records and rules make that life show up in the game.
For: grandtheftwiki, spots, moments, proposed, speech, player, mods, jobs. Last changed 2026-10-24, 154 lines.
Links to 2: `gidi:decisions/world-life.md`, `gidi:docs/lagos-study/LIVING.md`
Backlinks: 5 documents (`gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/lagos-study/LIVING.md`), 0 code files ().
Nearest in words: `gidi:decisions/IDEAS.md` (0.24); `gidi:decisions/world-life.md` (0.22); `gidi:docs/lagos-study/LIVING.md` (0.15).

## gidi:decisions/story
### `gidi:decisions/story/README.md`
**The story of Gidi**. The story of Gidi: Tunde, an okada rider, in debt to the boss who runs the motor park. The city opens in three acts: Survive, Hustle, Empire.
For: paste, acts, account, boss's, story, roadmap, prototyping, empire. Last changed 2026-10-25, 18 lines.
Links to 2: `gidi:decisions/story/act-1-draft.md`, `gidi:decisions/story/acts-2-3-draft.md`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/acts-2-3-draft.md` (0.33); `gidi:decisions/story/act-1-draft.md` (0.32); `gidi:decisions/story/novels/README.md` (0.24).

### `gidi:decisions/story/act-1-draft.md`
**Gidi Act 1: draft (the owner's outline, 15 Oct 2026, with Claude's notes)**. Gidi Act 1: draft (the owner's outline, 15 Oct 2026, with Claude's notes): **Status:** a draft for the story pass, stage 3 of `gidi-roadmap.md` (not in this repo yet). The owner decides; the notes are suggestions. The flowchart, `gidi-act1-flow.mermaid`, isn't in this repo; the flow below is the same in words.
For: boss, tunde, bike, boss's, fares, alpha, debt, paying. Last changed 2026-10-16, 109 lines.
Links to 0: 
Backlinks: 4 documents (`gidi:decisions/story/README.md`, `gidi:decisions/story/acts-2-3-draft.md`, `gidi:decisions/story/novels/1-the-ledger.md`, `gidi:docs/hand/maze-hub-lagos.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/acts-2-3-draft.md` (0.53); `gidi:decisions/story/novels/1-the-ledger.md` (0.42); `gidi:decisions/story/novels/README.md` (0.34).

### `gidi:decisions/story/acts-2-3-draft.md`
**Gidi Acts 2 and 3: working draft (updated 15 Oct 2026 after the owner's feedback)**. Gidi Acts 2 and 3: working draft (updated 15 Oct 2026 after the owner's feedback): Builds on `act-1-draft.md`. The owner didn't like the pacing of Claude's first Acts 2–3 path (one run per district, the fake-revenge scapegoat, the finale structure). Only what the owner confirmed or asked for is kept below; Claude's proposals are marked as such.
For: tunde, boss, bike, boss's, boys, claude's, debt, fight. Last changed 2026-10-15, 77 lines.
Links to 1: `gidi:decisions/story/act-1-draft.md`
Backlinks: 3 documents (`gidi:decisions/DECISIONS.md`, `gidi:decisions/story/README.md`, `gidi:decisions/story/novels/1-the-ledger.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/act-1-draft.md` (0.53); `gidi:decisions/story/novels/1-the-ledger.md` (0.46); `gidi:decisions/story/novels/README.md` (0.39).

## gidi:decisions/story/novels
### `gidi:decisions/story/novels/1-the-ledger.md`
**1. The Ledger**. 1. The Ledger: *Claude's draft, 15 Oct 2026. It builds on the owner's confirmed story (`../act-1-draft.md`, `../acts-2-3-draft.md`) and adds people.*
For: tunde, chairman, ledger, bike, player, alpha, tunde's, mama. Last changed 2026-10-15, 127 lines.
Links to 2: `gidi:decisions/story/act-1-draft.md`, `gidi:decisions/story/acts-2-3-draft.md`
Backlinks: 1 documents (`gidi:decisions/story/novels/README.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/novels/2-union.md` (0.51); `gidi:decisions/story/novels/3-the-phone.md` (0.48); `gidi:decisions/story/acts-2-3-draft.md` (0.46).

### `gidi:decisions/story/novels/2-union.md`
**2. Union**. 2. Union: *Claude's draft, 15 Oct 2026. It keeps the owner's Act 1 (the steal, the boss's rescue, the okada on hire purchase, the robbery), then gives the city its own clock: an election.*
For: tunde, election, envelopes, chairman, lorry's, ledger, wins, lorry. Last changed 2026-10-15, 75 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/story/novels/README.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/novels/1-the-ledger.md` (0.51); `gidi:decisions/story/novels/3-the-phone.md` (0.37); `gidi:decisions/story/acts-2-3-draft.md` (0.33).

### `gidi:decisions/story/novels/3-the-phone.md`
**3. The Phone**. 3. The Phone: *Claude's draft, 15 Oct 2026. It keeps the owner's Act 1 (the steal, the rescue, the okada on hire purchase), then turns the open world into a thriller: one object that keeps ringing.*
For: captain, phone, tunde, adaeze, garba, tunde's, chairman, captain's. Last changed 2026-10-15, 79 lines.
Links to 0: 
Backlinks: 1 documents (`gidi:decisions/story/novels/README.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/novels/1-the-ledger.md` (0.48); `gidi:decisions/story/novels/2-union.md` (0.37); `gidi:decisions/story/acts-2-3-draft.md` (0.29).

### `gidi:decisions/story/novels/README.md`
**Three stories for Gidi (Claude's drafts, 15 Oct 2026, for the owner to pick from)**. Three stories for Gidi (Claude's drafts, 15 Oct 2026, for the owner to pick from): The owner asked for "two or three novels of the story" to read, pick from, and build their own. These are short stories, about 15 minutes' reading each, not full novels. Each one names the people who drive the plot and the side characters who give it colour, and it's told the way it would play in an open world.
For: story, debt, novels, drugs, stories, force, betting, task. Last changed 2026-10-25, 36 lines.
Links to 4: `gidi:decisions/story/novels/1-the-ledger.md`, `gidi:decisions/story/novels/2-union.md`, `gidi:decisions/story/novels/3-the-phone.md`, `gidi:docs/lagos-study/roads/NAMES.md`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:decisions/story/acts-2-3-draft.md` (0.39); `gidi:decisions/story/act-1-draft.md` (0.34); `gidi:decisions/story/README.md` (0.24).

## gidi:decisions
### `gidi:decisions/world-life.md`
**Life in Gidi: what makes the world feel like it exists**. Life in Gidi: what makes the world feel like it exists: The owner's thinking from 16 Oct 2026, and Claude's proposals. The research behind it: `docs/research/LIFE-IN-LAGOS.md`. **Ideas, not decided**, unless marked as decided.
For: naira, betting, currency, player, football, radio, scan, everyone. Last changed 2026-10-16, 146 lines.
Links to 1: `gidi:docs/research/LIFE-IN-LAGOS.md`
Backlinks: 4 documents (`gidi:decisions/IDEAS.md`, `gidi:decisions/lived-in.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/research/LIFE-IN-LAGOS.md`), 0 code files ().
Nearest in words: `gidi:docs/research/LIFE-IN-LAGOS.md` (0.27); `gidi:decisions/lived-in.md` (0.22); `gidi:decisions/IDEAS.md` (0.21).

## gidi:docs
### `gidi:docs/BOARD.md`
**The drawing board**. The drawing board: The owner, 16 Oct 2026: "we should hand draw... we should know where something meets something... where the roads start, where the roads end, where the houses are, we should be able to move them."
For: bake, click, drag, edit, edits, dashed, select, furniture. Last changed 2026-10-24, 98 lines.
Links to 2: `gidi:scripts/board_server.py`, `gidi:web/board.html`
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`), 0 code files ().
Nearest in words: `gidi:docs/MAP-FORMAT.md` (0.18); `gidi:decisions/NOW.md` (0.17); `gidi:decisions/CODEBASE.md` (0.14).

### `gidi:docs/DATA-SOURCES.md`
**Data sources, and what to delete later**. Data sources, and what to delete later: Everything we've downloaded to study real Lagos lives on Daramola's Mac in `~/gidi-data/research/data/` (about 20 GB, mostly Google's 2.5D tiles). The OpenStreetMap extract (`lagos.osm.pbf`, 55 MB) is gone from the Mac; the repo's links to it were removed on 24 Oct.
For: final, cdla, delete, studies, licence, outlines, downloaded, google's. Last changed 2026-10-24, 31 lines.
Links to 1: `gidi:docs/DEEP-STUDY.md`
Backlinks: 4 documents (`gidi-data:README.md`, `gidi:decisions/CHECKS.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`), 0 code files ().
Nearest in words: `gidi:docs/gidi-data-plan.md` (0.12); `gidi-data:README.md` (0.12); `gidi:decisions/DECISIONS.md` (0.11).

### `gidi:docs/DEEP-STUDY.md`
**The deep study: every district's inspiration, from all the data**. The deep study: every district's inspiration, from all the data: The owner asked for this on 15 Oct 2026: "the research should look at everything in the data and take them into consideration". Every Gidi district is rebuilt by one shared generator. Each district gets its own profile, and the profile is set from this study.
For: types, wobble, touching, district's, measures, settings, fabric, measured. Last changed 2026-10-25, 65 lines.
Links to 0: 
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/DATA-SOURCES.md`, `gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/border.md` (0.22); `gidi:docs/studies/yaba.md` (0.21); `gidi:docs/studies/airport.md` (0.19).

### `gidi:docs/LAGOS-ISMS.md`
**Lagos-isms: the eccentricities in the real data (a running log)**. Lagos-isms: the eccentricities in the real data (a running log): **What this is.** While each district is studied, we log the real places' oddities: the things a tidy generator would never make, but that make Lagos feel like Lagos. For each one: - what it is - where it shows up in the real data (LGA and coordinates)
For: suits, one-way, expressway, reserve, kosofe, island, railside, acute. Last changed 2026-10-25, 276 lines.
Links to 4: `gidi-game:tools/road_build.py`, `gidi:data/results/lga_table.json`, `gidi:data/tools/pull-data.sh`, `gidi:docs/OLD-KIT.md`
Backlinks: 14 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/HISTORY.md`, `gidi:docs/OLD-MAP-LESSONS.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/border-pattern-study.md`, `gidi:docs/estate-pattern-study.md`, `gidi:docs/frontier-pattern-study.md`, `gidi:docs/hand/maze-hub-lagos.md` ...), 0 code files ().
Nearest in words: `gidi:docs/border-pattern-study.md` (0.26); `gidi:docs/estate-pattern-study.md` (0.26); `gidi:docs/jungle-pattern-study.md` (0.22).

### `gidi:docs/LAGOS-LIGHT.md`
**Lagos light: why the city looks different**. Lagos light: why the city looks different: The owner's observation: photos taken in Nigeria look different from photos taken abroad. The vibrancy and the feel of the light aren't the same. Most of it is physics. This is the lighting brief for Gidi's look, in the browser now and in Unreal later.
For: shadows, light, abroad, haze, contrast, dusk, warm, soft. Last changed 2026-10-25, 61 lines.
Links to 0: 
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.11); `gidi:docs/look/research-street.md` (0.1); `gidi:docs/look/research-transport.md` (0.08).

### `gidi:docs/MAP-FORMAT.md`
**The new map's data format (draft 0.1, for the owner to approve)**. The new map's data format (draft 0.1, for the owner to approve): The new map is the one ground truth (decisions, 22 Oct: "everything that we do must be in map data. Every single thing"). The drawing board saves into it. The Blender kit and the Unreal import read it. Nothing else holds the city.
For: dress, record, field, stroke, value, records, degrees, face. Last changed 2026-10-25, 599 lines.
Links to 19: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-game:tools/fields.py`, `gidi-game:tools/kit_fields.py`, `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`, `gidi:decisions/CHECKS.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/lived-in.md`, `gidi:docs/OLD-KIT.md`, `gidi:docs/lagos-study/roads/EARTH-CHECK.md`, `gidi:docs/map-format-example/d15/district.json`, `gidi:docs/map-format-example/d15/dress/128_60.json` ...
Backlinks: 6 documents (`gidi-data:research/google/kits/old-town/tests/ot45/NOTES.md`, `gidi:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`, `gidi:docs/map-format-example/README.md`), 10 code files (`gidi-game:tools/block_build.py`, `gidi-game:tools/kit_fields.py`, `gidi-game:tools/map_build.py`, `gidi-game:tools/road_draft.py`, `gidi-game:tools/spot_to_map.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.41); `gidi:decisions/DECISIONS.md` (0.31); `gidi-data:research/google/kits/old-town/tests/ot91/NOTES.md` (0.28).

### `gidi:docs/OLD-KIT.md`
**The old Blender kit: what it held, and what the builders can take from it**. The old Blender kit: what it held, and what the builders can take from it: The owner (24 Oct): "we took a lot of time to build stuff in the old Blender kit... can we see what we need in the old Blender kit, so we see what we need to remodel". This page answers that. The kit is frozen (DECISIONS, "The interface works both ways; the builders are the kit"): nothing here is extended. A builder in `gidi-game/tools/*_build.py` is made
For: builder, know-how, worth, builders, fields, conditions, page, sheet. Last changed 2026-10-25, 98 lines.
Links to 5: `gidi-data:research/google/kits/old-town/KIT.md`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/kit_fields.py`, `gidi-game:tools/wear_layer.py`, `gidi:docs/OLD-MAP-LESSONS.md`
Backlinks: 7 documents (`gidi:CLAUDE.md`, `gidi:decisions/CHECKS.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/MAP-FORMAT.md`), 0 code files ().
Nearest in words: `gidi:decisions/NOW.md` (0.24); `gidi:decisions/DECISIONS.md` (0.24); `gidi:decisions/CHECKS.md` (0.23).

### `gidi:docs/OLD-MAP-LESSONS.md`
**What the old map taught: still true for the new one**. What the old map taught: still true for the new one: The old generated map (13-21 Oct 2026) is history, deleted 25 Oct (git tag `before-cleanup-25oct`; DECISIONS, "The new map is the truth"). Its plans and pass reports were deleted on 25 Oct (git tag `before-cleanup-25oct` holds them). Before they went, each was read for what still holds for the new map
For: ramp, reimport, unreal, viewing, misses, often, living, missed. Last changed 2026-10-25, 89 lines.
Links to 2: `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/lagos-study/LIVING.md`
Backlinks: 7 documents (`gidi:README.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/HISTORY.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:docs/OLD-KIT.md`, `gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:decisions/NOW.md` (0.21); `gidi:decisions/DECISIONS.md` (0.18); `gidi:docs/LAGOS-ISMS.md` (0.16).

### `gidi:docs/RESEARCH.md`
**The Lagos research: what we know, and which new districts it serves**. The Lagos research: what we know, and which new districts it serves: Everything gidi holds about real Lagos, in one place. Most of it was written for the old map (13-21 Oct), but what it measured is real Lagos, so it still holds for the new map (real Lagos at 1:3). Only its Gidi parts are history: the old district names, the generator settings, the "Gidi against real" columns. Read the real numbers; skip the old-map parts.
For: shomolu-bariga, measured, echo, serves, festac, written, districts, island. Last changed 2026-10-24, 66 lines.
Links to 60: `gidi:data/results/lga_table.json`, `gidi:decisions/lived-in.md`, `gidi:decisions/world-life.md`, `gidi:docs/DEEP-STUDY.md`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/LAGOS-LIGHT.md`, `gidi:docs/OLD-MAP-LESSONS.md`, `gidi:docs/bazaar-pattern-study.md`, `gidi:docs/border-pattern-study.md`, `gidi:docs/capital-pattern-study.md`, `gidi:docs/estate-pattern-study.md`, `gidi:docs/foodgate-pattern-study.md` ...
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/STUDY.md` (0.23); `gidi:docs/lagos-study/councils.md` (0.22); `gidi:docs/LAGOS-ISMS.md` (0.19).

### `gidi:docs/bazaar-pattern-study.md`
**The Bazaar pattern study: Ojo round the electronics market → The Bazaar (v1)**. The Bazaar pattern study: Ojo round the electronics market → The Bazaar (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: bazaar, expressway, electronics, wholesale, fair, jungle, plazas, avenue. Last changed 2026-10-14, 125 lines.
Links to 2: `gidi:data/results/lga_table.json`, `gidi:docs/img/bazaar-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/jungle-pattern-study.md` (0.33); `gidi:docs/capital-pattern-study.md` (0.3); `gidi:docs/railside-pattern-study.md` (0.3).

### `gidi:docs/border-pattern-study.md`
**Border pattern study: Badagry → the Border (v1)**. Border pattern study: Badagry → the Border (v1): Status: generated for review (15 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: border, badagry, bush, expressway, estimated, post, sprawl, bazaar. Last changed 2026-10-15, 137 lines.
Links to 4: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/border-vs-real.png`, `gidi:scripts/study_boxheights.py`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/bazaar-pattern-study.md` (0.3); `gidi:docs/LAGOS-ISMS.md` (0.26); `gidi:docs/frontier-pattern-study.md` (0.25).

### `gidi:docs/capital-pattern-study.md`
**The Capital pattern study: central Ikeja → The Capital (v1)**. The Capital pattern study: central Ikeja → The Capital (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: capital, estimated, ikeja, cantonment, railside, gateways, typical, shrine. Last changed 2026-10-14, 159 lines.
Links to 2: `gidi:data/results/lga_table.json`, `gidi:docs/img/capital-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/railside-pattern-study.md` (0.4); `gidi:docs/estate-pattern-study.md` (0.34); `gidi:docs/foodgate-pattern-study.md` (0.31).

### `gidi:docs/estate-pattern-study.md`
**Estate pattern study: Ikeja GRA, Magodo and Omole → the Estate (v1)**. Estate pattern study: Ikeja GRA, Magodo and Omole → the Estate (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: estates, ikeja, gates, gra's, kosofe, estate's, omole's, quarters. Last changed 2026-10-14, 141 lines.
Links to 3: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/estate-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.34); `gidi:docs/railside-pattern-study.md` (0.31); `gidi:docs/heights-pattern-study.md` (0.26).

### `gidi:docs/foodgate-pattern-study.md`
**Food Gate pattern study: Ojota–Ketu–Mile 12 (Kosofe) → Food Gate (v1)**. Food Gate pattern study: Ojota–Ketu–Mile 12 (Kosofe) → Food Gate (v1): Status: generated for review (13 Oct 2026). Same method as the other districts: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: kosofe, northern, food, mile, adeleke, maze's, ketu, corridor. Last changed 2026-10-14, 172 lines.
Links to 2: `gidi:data/results/lga_table.json`, `gidi:docs/img/foodgate-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.35); `gidi:docs/capital-pattern-study.md` (0.31); `gidi:docs/jungle-pattern-study.md` (0.3).

### `gidi:docs/frontier-pattern-study.md`
**Frontier pattern study: the Lekki peninsula → the Frontier (v1)**. Frontier pattern study: the Lekki peninsula → the Frontier (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: frontier, peninsula, cells, tracts, awoyaya, refinery, empty, flare. Last changed 2026-10-14, 177 lines.
Links to 4: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/frontier-vs-real.png`, `gidi:scripts/study_boxheights.py`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/heights-pattern-study.md` (0.31); `gidi:docs/border-pattern-study.md` (0.25); `gidi:docs/LAGOS-ISMS.md` (0.22).

### `gidi:docs/gidi-data-plan.md`
**Gidi data plan: everything we need to build accurate districts (v1, 13 Oct 2026)**. Gidi data plan: everything we need to build accurate districts (v1, 13 Oct 2026): **Rule:** we study real Lagos to learn its patterns, then build our own world. Nothing real is traced or shipped.
For: cc-by, blocked, daramola's, tier, token, mapillary, eti-osa, saloons. Last changed 2026-10-24, 186 lines.
Links to 4: `gidi:data/results/heights.py`, `gidi:data/results/heights_by_lga.json`, `gidi:data/results/landpop.py`, `gidi:data/results/lga_table.json`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/look/research-roads.md`), 0 code files ().
Nearest in words: `gidi:docs/LAGOS-ISMS.md` (0.18); `gidi:docs/RESEARCH.md` (0.17); `gidi:docs/lagos-lgas-research.md` (0.16).

## gidi:docs/hand
### `gidi:docs/hand/borrowed-lagos.md`
**Borrowed from Lagos: real places reimagined in Gidi (16 Oct 2026)**. Borrowed from Lagos: real places reimagined in Gidi (16 Oct 2026): The owner's direction: "take inspiration from the places to build the area... also from places that didn't inspire the districts, to give a taste of everywhere, tastefully and tactfully... research the actual Lagos map and see things you could take and creatively integrate."
For: placed, capital, saba, channel, mall, national, museum, rail's. Last changed 2026-10-25, 72 lines.
Links to 0: 
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/HISTORY.md`, `gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.21); `gidi:docs/look/research-landmarks.md` (0.2); `gidi:docs/LAGOS-ISMS.md` (0.2).

### `gidi:docs/hand/maze-hub-lagos.md`
**The Maze and the Hub: what makes them unmistakably Lagos (agreed 16 Oct 2026)**. The Maze and the Hub: what makes them unmistakably Lagos (agreed 16 Oct 2026): The first hand-made districts: Act 1 opens here (`decisions/story/act-1-draft.md`). Each item says what it is, where it goes in Gidi, how it gets built (the hand files, `scripts/hand.py`), and where it comes from: - **photo:** the owner's reference photos (`~/gidi-data/research/refs/REVIEW.md`)
For: brief, photo, story, yard, assets, print, daleko, bowl. Last changed 2026-10-25, 53 lines.
Links to 2: `gidi:decisions/story/act-1-draft.md`, `gidi:docs/LAGOS-ISMS.md`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.17); `gidi:decisions/story/README.md` (0.14); `gidi-data:research/refs/REVIEW.md` (0.14).

### `gidi:docs/hand/monument-briefs.md`
**Monuments: what each needs (19 Oct)**. Monuments: what each needs (19 Oct): The owner's rule: Meshy for statues and monuments nobody walks into; structures people walk into or under are built in Blender part by part. Credits are spent in two steps: a concept picture first (nano-banana-2, 6 credits), the owner approves
For: bronze, concept, credits, menu, rider, masquerade, saxophonist, eyo-style. Last changed 2026-10-19, 30 lines.
Links to 0: 
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/hand/borrowed-lagos.md` (0.14); `gidi:docs/look/research-landmarks.md` (0.13); `gidi:docs/OLD-KIT.md` (0.08).

## gidi:docs
### `gidi:docs/heights-pattern-study.md`
**Heights pattern study: Ikoyi, Victoria Island and Banana Island → the Heights (v3)**. Heights pattern study: Ikoyi, Victoria Island and Banana Island → the Heights (v3): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: ikoyi, island, boxes, island's, beach, hipped, golf, course. Last changed 2026-10-14, 208 lines.
Links to 4: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/heights-vs-real.png`, `gidi:scripts/study_boxheights.py`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/oldisland-pattern-study.md` (0.34); `gidi:docs/frontier-pattern-study.md` (0.31); `gidi:docs/estate-pattern-study.md` (0.26).

### `gidi:docs/hub-pattern-study.md`
**Hub pattern study: Oshodi/Isolo + Surulere → The Hub (v1)**. Hub pattern study: Oshodi/Isolo + Surulere → The Hub (v1): Status: generated for review (13 Oct 2026). Same method as the Maze: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.** Data: OpenStreetMap (ODbL), Lagos extract, plus building heights from Google Open Buildings 2.5D (via `data/results/lga_table.json`). Area studied: Oshodi/Isolo + Surulere LGAs, 64.6 km² by the OpenStreetMap boundaries. The height and people table uses the government land areas, which add up to 75.9 km²; the shares are not affected.
For: slip, knot, maze, stadium, northern, terminal, skywalks, percentile. Last changed 2026-10-13, 278 lines.
Links to 3: `gidi:data/results/lga_table.json`, `gidi:docs/img/hub-station-skywalk.png`, `gidi:docs/img/hub-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.38); `gidi:docs/foodgate-pattern-study.md` (0.28); `gidi:docs/jungle-pattern-study.md` (0.25).

### `gidi:docs/jungle-pattern-study.md`
**Jungle City pattern study: Ajegunle (+ Festac) → Jungle City (v1)**. Jungle City pattern study: Ajegunle (+ Festac) → Jungle City (v1): Status: generated for review (13 Oct 2026). Same method as the Maze and the Hub: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: jungle, flats, expressway, adeleke, ajegunle, maze's, footbridge, maze. Last changed 2026-10-14, 246 lines.
Links to 2: `gidi:data/results/lga_table.json`, `gidi:docs/img/jungle-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/maze-pattern-study.md` (0.44); `gidi:docs/bazaar-pattern-study.md` (0.33); `gidi:docs/foodgate-pattern-study.md` (0.3).

### `gidi:docs/lagos-lgas-research.md`
**Lagos, one local government at a time: research for Gidi**. Lagos, one local government at a time: research for Gidi: 13 October 2026. Twenty researchers, one per local government area (LGA), each asked what makes the place itself: buildings, landmarks, roads, markets, transport, sound and smell, people, food, history, danger, environment, sacred things, pop culture, what Gidi can borrow and what to avoid. The full reports are below the summary, unedited.
For: unverified, unsourced, opened, wikipedia, languages, sourced, yoruba, festivals. Last changed 2026-10-13, 2800 lines.
Links to 0: 
Backlinks: 5 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/lagos-study/LIVING.md`, `gidi:docs/lagos-study/STUDY.md`, `gidi:docs/lagos-study/councils.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/LIVING.md` (0.32); `gidi:docs/lagos-study/councils.md` (0.3); `gidi:docs/lagos-study/STUDY.md` (0.26).

## gidi:docs/lagos-study
### `gidi:docs/lagos-study/LIVING.md`
**Living in each district: the 51, for the brush and the lived-in layer**. Living in each district: the 51, for the brush and the lived-in layer: Study file (24 Oct 2026). Real place names live here and in other study files only, never in `map/`. The Gidi names come from `roads/NAMES.md`.
For: brush, careful, draft, traders, workers, spots, moving, okada. Last changed 2026-10-24, 555 lines.
Links to 6: `gidi:decisions/lived-in.md`, `gidi:docs/lagos-lgas-research.md`, `gidi:docs/lagos-study/STUDY.md`, `gidi:docs/lagos-study/councils.md`, `gidi:docs/lagos-study/roads/NAMES.md`, `gidi:docs/research/LIFE-IN-LAGOS.md`
Backlinks: 6 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:decisions/lived-in.md`, `gidi:docs/OLD-MAP-LESSONS.md`, `gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-lgas-research.md` (0.32); `gidi:docs/lagos-study/councils.md` (0.2); `gidi:decisions/lived-in.md` (0.15).

### `gidi:docs/lagos-study/STUDY.md`
**How the whole Lagos map works: a study before cutting districts**. How the whole Lagos map works: a study before cutting districts: 22 Oct 2026. Read-only. Asked for by the owner's decision "Gidi is Lagos, miniaturised; the map starts again". This is evidence for a later frame proposal. It does not cut districts.
For: belt, bldg, tilt, ikorodu, mile, surveyed, planned, lekki. Last changed 2026-10-24, 322 lines.
Links to 6: `gidi:data/results/heights.py`, `gidi:data/results/heights_by_lga.json`, `gidi:data/results/lga_table.json`, `gidi:docs/lagos-study/councils.md`, `gidi:docs/lagos-study/roads/scripts/gaz.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`
Backlinks: 7 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/lagos-study/LIVING.md`, `gidi:docs/lagos-study/councils.md`, `gidi:docs/lagos-study/similar/SIMILAR.md`), 2 code files (`gidi-game:tools/junction_geo.py`, `gidi:scripts/draft_kinds.py`).
Nearest in words: `gidi:docs/lagos-study/councils.md` (0.58); `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.35); `gidi:docs/lagos-study/roads/ROADS.md` (0.34).

### `gidi:docs/lagos-study/councils.md`
**Lagos councils: the 20 LGAs and 37 LCDAs**. Lagos councils: the 20 LGAs and 37 LCDAs: 22 Oct 2026. Companion to `STUDY.md`. Read-only study; nothing here is a district yet.
For: zones, known, lcdas, amuwo-odofin, lcda, apapa, mainland, neighbours. Last changed 2026-10-24, 212 lines.
Links to 2: `gidi:data/results/heights_by_lga.json`, `gidi:docs/lagos-study/STUDY.md`
Backlinks: 6 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/lagos-study/LIVING.md`, `gidi:docs/lagos-study/STUDY.md`, `gidi:docs/lagos-study/similar/SIMILAR.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/STUDY.md` (0.58); `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.4); `gidi:docs/lagos-study/roads/ROADS.md` (0.35).

## gidi:docs/lagos-study/roads
### `gidi:docs/lagos-study/roads/EARTH-CHECK.md`
**Google Earth check of the borders (22 Oct 2026)**. Google Earth check of the borders (22 Oct 2026): `ROADS.md` section 6 left 15 borders the data could not settle. Each was looked at on Google Maps satellite (zoom 13 to 16) at the coordinates below. Study only: the 29 screenshots stay outside the repo, in `~/gidi-data/research/google/lagos-study/border-checks/` (file names carry the check number and the map
For: east, west, south, likely, trace, north, expressway, isolo. Last changed 2026-10-24, 274 lines.
Links to 2: `gidi:docs/lagos-study/roads/ROADS.md`, `gidi:docs/lagos-study/roads/places.csv`
Backlinks: 4 documents (`gidi:decisions/NOW.md`, `gidi:docs/MAP-FORMAT.md`, `gidi:docs/lagos-study/roads/NAMES.md`, `gidi:docs/lagos-study/roads/ROADS.md`), 1 code files (`gidi:scripts/frame_study.py`).
Nearest in words: `gidi:docs/lagos-study/roads/ROADS.md` (0.59); `gidi:docs/lagos-study/councils.md` (0.4); `gidi:docs/lagos-study/STUDY.md` (0.35).

### `gidi:docs/lagos-study/roads/NAMES.md`
**Echo names for the 51 districts (draft, 22 Oct 2026)**. Echo names for the 51 districts (draft, 22 Oct 2026): Working names for the 51 districts in `EARTH-CHECK.md` ("District list after the checks"), as the map format's fourth call asks (`decisions/DECISIONS.md`, "The map format's four calls", point 4; the rule is in `decisions/IDEAS.md`, "Place names: echo names"). **Every name here is a draft: the owner reviews it**, and any of them can change later.
For: yoruba, consonant, english, vowel, sound, mile, leke, sounds. Last changed 2026-10-22, 115 lines.
Links to 4: `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:docs/lagos-study/roads/EARTH-CHECK.md`, `gidi:docs/lagos-study/roads/places.csv`
Backlinks: 7 documents (`gidi:decisions/CHECKS.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/IDEAS.md`, `gidi:decisions/NOW.md`, `gidi:decisions/story/novels/README.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/lagos-study/LIVING.md`), 0 code files ().
Nearest in words: `gidi:decisions/IDEAS.md` (0.2); `gidi:docs/lagos-lgas-research.md` (0.13); `gidi:docs/lagos-study/LIVING.md` (0.12).

### `gidi:docs/lagos-study/roads/ROADS.md`
**Roads first, districts by their borders**. Roads first, districts by their borders: Step 1 of the new map plan (22 Oct): Gidi is real Lagos made smaller, at 1:3, in a frame about 27 × 10.5 km. This study lays down the skeleton of real roads, cuts Lagos into places along its real borders, measures every border, and joins places into districts only where they really touch and are alike.
For: morogbo, north-east, imota, east, ijegun-egba, west, apapa, swamp. Last changed 2026-10-24, 510 lines.
Links to 29: `gidi:docs/lagos-study/roads/EARTH-CHECK.md`, `gidi:docs/lagos-study/roads/borders.csv`, `gidi:docs/lagos-study/roads/districts.csv`, `gidi:docs/lagos-study/roads/districts_55.png`, `gidi:docs/lagos-study/roads/districts_55_inner.png`, `gidi:docs/lagos-study/roads/districts_60.png`, `gidi:docs/lagos-study/roads/districts_60_inner.png`, `gidi:docs/lagos-study/roads/districts_65.png`, `gidi:docs/lagos-study/roads/districts_65_inner.png`, `gidi:docs/lagos-study/roads/ladder.csv`, `gidi:docs/lagos-study/roads/not_neighbours.csv`, `gidi:docs/lagos-study/roads/places.csv` ...
Backlinks: 2 documents (`gidi:decisions/NOW.md`, `gidi:docs/lagos-study/roads/EARTH-CHECK.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.59); `gidi:docs/lagos-study/similar/SIMILAR.md` (0.36); `gidi:docs/lagos-study/councils.md` (0.35).

## gidi:docs/lagos-study/similar
### `gidi:docs/lagos-study/similar/GOOGLE-CHECK.md`
**The close calls, checked on Google satellite (22 Oct 2026)**. The close calls, checked on Google satellite (22 Oct 2026): The similarity numbers (`SIMILAR.md`) flagged 10 merges as close or doubtful. Each pair was looked at side by side on Google satellite, about 1 km across, at each unit's seed point. Study only: the pictures stay outside the repo (`~/gidi-data/research/google/lagos-study/close-calls/`, sheet `close_calls.jpg`).
For: obalende-onikan, split, joins, splits, magodo-omole, okota-ikotun, gbagada, maryland. Last changed 2026-10-24, 31 lines.
Links to 1: `gidi:docs/lagos-study/similar/SIMILAR.md`
Backlinks: 1 documents (`gidi:decisions/NOW.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/STUDY.md` (0.21); `gidi:docs/lagos-study/roads/ROADS.md` (0.2); `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.2).

### `gidi:docs/lagos-study/similar/SIMILAR.md`
**Which places are alike: numbers for cutting districts**. Which places are alike: numbers for cutting districts: 22 Oct 2026. Read-only study. It gives numbers for how many districts, and which places merge. It does not decide. Builds on `docs/lagos-study/STUDY.md` and `councils.md`, and reuses their 250 m grids.
For: belt, bungalow, ogba-agidingbi-alausa, isheri-olowora, ijora-badia, apapa-tin, alaba-ojo-lasu, agric-majidun-ogolonto. Last changed 2026-10-24, 957 lines.
Links to 12: `gidi:docs/lagos-study/STUDY.md`, `gidi:docs/lagos-study/councils.md`, `gidi:docs/lagos-study/roads/scripts/report.py`, `gidi:docs/lagos-study/similar/ladder.csv`, `gidi:docs/lagos-study/similar/pairs.csv`, `gidi:docs/lagos-study/similar/scripts/analyse.py`, `gidi:docs/lagos-study/similar/scripts/finger.py`, `gidi:docs/lagos-study/similar/scripts/know.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`, `gidi:docs/lagos-study/similar/scripts/seeds.py`, `gidi:docs/lagos-study/similar/scripts/units.py`, `gidi:docs/lagos-study/similar/units.csv`
Backlinks: 2 documents (`gidi:decisions/NOW.md`, `gidi:docs/lagos-study/similar/GOOGLE-CHECK.md`), 4 code files (`gidi:docs/lagos-study/similar/scripts/appendix.py`, `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`, `gidi:docs/lagos-study/similar/scripts/report.py`).
Nearest in words: `gidi:docs/lagos-study/similar/districts.md` (0.92); `gidi:docs/lagos-study/roads/ROADS.md` (0.36); `gidi:docs/lagos-study/STUDY.md` (0.31).

### `gidi:docs/lagos-study/similar/districts.md`
**At 90%: 81 districts (71 after folding tiny plain units)**. At 90%: 81 districts (71 after folding tiny plain units): Rich or distinct units still alone (24): Isale Eko-Idumota-Marina, Ikoyi-Banana Island, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Ogijo-Sagamu Rd, Isheri-Olowora (Ikosi-Isheri), UNILAG, Ebute Metta-Oyingbo-Otto-Iddo, Makoko-Iwaya, Surulere (Ojuelegba-Bode Thomas-Stadium), Ilupeju, Papa Ajao-Ladipo, Oshodi-Mafoluku, Apapa-Tin Can, Ijora-Badia, Ajegunle (Ajeromi), Amukoko-Layeni (Ifelodun), Mile 2-Amuwo, Kirikiri-Navy Town, Alaba-Ojo-LASU, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.
For: ftz-dangote, agric-majidun-ogolonto, eko-idumota-marina, isheri-olowora, allen-opebi-computer, ogba-agidingbi-alausa, ijora-badia, makoko-iwaya. Last changed 2026-10-22, 469 lines.
Links to 0: 
Backlinks: 0 documents (), 2 code files (`gidi:docs/lagos-study/similar/scripts/appendix.py`, `gidi:docs/lagos-study/similar/scripts/report.py`).
Nearest in words: `gidi:docs/lagos-study/similar/SIMILAR.md` (0.92); `gidi:docs/lagos-study/roads/ROADS.md` (0.33); `gidi:docs/lagos-study/STUDY.md` (0.17).

## gidi:docs/look
### `gidi:docs/look/research-buildings.md`
**Lagos buildings and their parts: a catalogue for the Gidi generator**. Lagos buildings and their parts: a catalogue for the Gidi generator: Rule zero: this is pattern research. Nothing here names a building to copy; Gidi invents its own.
For: elite, select, often, white, long-span, older, painted, green. Last changed 2026-10-14, 697 lines.
Links to 0: 
Backlinks: 7 documents (`gidi:docs/RESEARCH.md`, `gidi:docs/look/research-civic.md`, `gidi:docs/look/research-commerce.md`, `gidi:docs/look/research-housing.md`, `gidi:docs/look/research-landmarks.md`, `gidi:docs/look/research-leisure.md`, `gidi:docs/look/research-religious.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-housing.md` (0.63); `gidi:docs/look/research-street.md` (0.45); `gidi:docs/look/research-leisure.md` (0.43).

### `gidi:docs/look/research-civic.md`
**Civic and public-service buildings: a catalogue for the Gidi generator**. Civic and public-service buildings: a catalogue for the Gidi generator: Scope: hospitals, clinics, chemists, police (stations, command, posts, checkpoints, barracks), fire, government offices, customs, prison, army, courts, cemeteries, post offices, traffic/task-force posts, and power-company offices and transformers. This builds on `docs/look/research-buildings.md` sections 10.7, 10.8, 10.11 and 10.12, and on `docs/look/research-street.md` sections 2.2 and 3.8. It goes further and does not repeat those sections.
For: agency, crest, white, police, pound, variants, secretariat, select. Last changed 2026-10-14, 647 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-transport.md` (0.47); `gidi:docs/look/research-housing.md` (0.45); `gidi:docs/look/research-commerce.md` (0.43).

### `gidi:docs/look/research-commerce.md`
**Gidi commerce catalogue: markets, shops, commerce and industry**. Gidi commerce catalogue: markets, shops, commerce and industry: Purpose: specs for the seeded Blender kit. This builds on `docs/look/research-buildings.md` §6 (shop bays, container shop, kiosk, stall, plaza) and `docs/look/research-street.md` §6 (stall goods, umbrellas, chairs, generators, water tanks, night light). Those base specs are **not repeated**. Where they apply, this file refers to them as `B§6.x` and `S§6.x`.
For: mapping, select, condition, variants, steel, props, plazas, timber. Last changed 2026-10-16, 883 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-transport.md` (0.52); `gidi:docs/look/research-housing.md` (0.51); `gidi:docs/look/research-leisure.md` (0.45).

### `gidi:docs/look/research-housing.md`
**Lagos housing types beyond the front/back house: a catalogue for the Gidi kit**. Lagos housing types beyond the front/back house: a catalogue for the Gidi kit: Scope: every housing type (and the housing-adjacent structures that sit on residential plots) that the Gidi census lists, other than the generic front/back house that `docs/look/research-buildings.md` already covers. This file builds on that document (§0 constants, §1 rooming house, §7 Brazilian house, §8 stilt house, §9 elite) and goes deeper. It does not repeat its paint palette, weathering grammar or sandcrete constants. Use those as the base layer.
For: elite, steel, condition, mapping, white, flats, variants, select. Last changed 2026-10-14, 926 lines.
Links to 1: `gidi:docs/look/research-buildings.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-buildings.md` (0.63); `gidi:docs/look/research-commerce.md` (0.51); `gidi:docs/look/research-leisure.md` (0.5).

### `gidi:docs/look/research-landmarks.md`
**Lagos landmarks as patterns: a catalogue for Gidi's invented landmarks**. Lagos landmarks as patterns: a catalogue for Gidi's invented landmarks: Rule zero applies here more than anywhere else. A landmark is the thing a player will recognise, so **every Gidi landmark must be an original design**. Real Lagos structures appear below only as references for a *type*: what makes that kind of thing striking, how big it is, what it is made of and how it ages. Each item ends with 1-2 invented Gidi designs that share the spirit but not the silhouette of any real one.
For: oldisland, white, canon, condition, reference, designs, select, concrete. Last changed 2026-10-14, 735 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-transport.md` (0.42); `gidi:docs/look/research-leisure.md` (0.41); `gidi:docs/look/research-housing.md` (0.4).

### `gidi:docs/look/research-leisure.md`
**Gidi catalogue: education, sport, leisure and nightlife places**. Gidi catalogue: education, sport, leisure and nightlife places: This catalogue extends `docs/look/research-buildings.md` and `docs/look/research-street.md`. It does not repeat their walls, gates, roofs, generators, umbrellas, plastic chairs or crowd tables. It reuses them by name: "compound wall (buildings §4)", "event canopy (street §6.3)".
For: white, condition, elite, club, painted, select, mapping, variants. Last changed 2026-10-14, 800 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-housing.md` (0.5); `gidi:docs/look/research-transport.md` (0.45); `gidi:docs/look/research-commerce.md` (0.45).

### `gidi:docs/look/research-religious.md`
**Gidi look research: religious buildings and places**. Gidi look research: religious buildings and places: Scope: mosques, churches, white-garment churches, prayer camps, storefront worship, roadside prayer spaces, traditional shrines and festival structures, and how each one sits in the street. Builds on `docs/look/research-buildings.md` §10.5–10.6 and `research-street.md` (loudspeakers, banners, Friday/Sunday dress). This file goes deeper. It does not repeat those sections.
For: dome, white, prayer, mosque, green, hall, minaret, blue. Last changed 2026-10-14, 625 lines.
Links to 2: `gidi:docs/look/research-buildings.md`, `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-housing.md` (0.44); `gidi:docs/look/research-buildings.md` (0.42); `gidi:docs/look/research-leisure.md` (0.42).

### `gidi:docs/look/research-roads.md`
**Gidi ground catalogue: roads in every condition, drains, ground, water, vegetation, refuse**. Gidi ground catalogue: roads in every condition, drains, ground, water, vegetation, refuse: This catalogue covers the honest Lagos: roads that are mud with potholes of water, mushy laterite lanes, failed asphalt, choked drains. It builds on `docs/look/research-street.md` §1 and §6.7–6.9, and does not repeat what is there: road widths by class, kerb paint colours, median types, basic drain sizes, basic pothole density, the tree census. It goes deeper on **condition** and on **how to select it from data**.
For: select, mapping, sand, mains, research-street, asphalt, laterite, refuse. Last changed 2026-10-25, 1147 lines.
Links to 1: `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-street.md` (0.36); `gidi:docs/look/research-transport.md` (0.35); `gidi:docs/look/research-commerce.md` (0.34).

### `gidi:docs/look/research-street.md`
**Gidi street catalogue: roads, vehicles, people, signage, props**. Gidi street catalogue: roads, vehicles, people, signage, props: This is research for a procedural generator. It studies real Lagos and describes patterns only. Every brand is described generically, and Gidi must invent its own names, liveries and slogans.
For: select, black, white, yellow, often, colours, expressways, blue. Last changed 2026-10-14, 923 lines.
Links to 0: 
Backlinks: 9 documents (`gidi:docs/RESEARCH.md`, `gidi:docs/look/research-civic.md`, `gidi:docs/look/research-commerce.md`, `gidi:docs/look/research-landmarks.md`, `gidi:docs/look/research-leisure.md`, `gidi:docs/look/research-religious.md`, `gidi:docs/look/research-roads.md`, `gidi:docs/look/research-transport.md` ...), 0 code files ().
Nearest in words: `gidi:docs/look/research-vehicles.md` (0.5); `gidi:docs/look/research-buildings.md` (0.45); `gidi:docs/look/research-transport.md` (0.44).

### `gidi:docs/look/research-transport.md`
**Gidi transport and infrastructure catalogue**. Gidi transport and infrastructure catalogue: Research for the seeded Blender kit. Rule zero applies: real Lagos is studied as a pattern only. All names, liveries and logos in the kit must be invented; real places below are examples of a pattern, not things to copy.
For: white, select, mapping, condition, colours, steel, yellow, deck. Last changed 2026-10-14, 886 lines.
Links to 1: `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-commerce.md` (0.52); `gidi:docs/look/research-housing.md` (0.49); `gidi:docs/look/research-civic.md` (0.47).

### `gidi:docs/look/research-vehicles.md`
**Gidi vehicle catalogue: everything that moves on Lagos roads and water**. Gidi vehicle catalogue: everything that moves on Lagos roads and water: Research for the seeded Blender kit. **Rule zero:** study real Lagos, build our own city. Every real model, operator, union, agency and brand below is a *pattern reference* only. In Gidi, invent the liveries, names, logos, plates and slogans; describe makes only as body shapes ("1980s boxy rear-engine van", "bonneted American-style tractor").
For: rear, occupants, street-research, black, mapping, select, dimensions, yellow. Last changed 2026-10-14, 1288 lines.
Links to 1: `gidi:docs/look/research-street.md`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/look/research-street.md` (0.5); `gidi:docs/look/research-transport.md` (0.41); `gidi:docs/look/research-commerce.md` (0.36).

## gidi:docs/map-format-example
### `gidi:docs/map-format-example/README.md`
**Worked example of the new map format**. Worked example of the new map format: One short home street in district d15 (20 m, invented names), written as the map would hold it (docs/MAP-FORMAT.md):
For: lean-to's, gutter's, lean-to, example, stand-in, shop-under-flats, bungalow's, stamped. Last changed 2026-10-22, 10 lines.
Links to 6: `gidi:docs/MAP-FORMAT.md`, `gidi:docs/map-format-example/d15/district.json`, `gidi:docs/map-format-example/d15/dress/128_60.json`, `gidi:docs/map-format-example/d15/plan.json`, `gidi:schema/kit_reads.json`, `gidi:scripts/check_map.py`
Backlinks: 1 documents (`gidi:decisions/CODEBASE.md`), 0 code files ().
Nearest in words: `gidi:docs/MAP-FORMAT.md` (0.25); `gidi:decisions/NOW.md` (0.13); `gidi-data:research/google/kits/old-town/tests/ot175/NOTES.md` (0.13).

## gidi:docs
### `gidi:docs/maze-pattern-study.md`
**Maze pattern study: Mushin + Shomolu → The Maze (v2)**. Maze pattern study: Mushin + Shomolu → The Maze (v2): Status: v2, regenerated with the current generator for review (13 Oct 2026). v1 was the first build; section 5 compares the two. Method: **Option 2.** We measure the real place, turn the numbers into rules, and generate original streets and houses from the rules. **No real street or building geometry is copied into Gidi.** Data: OpenStreetMap (ODbL), Lagos extract, plus building heights, people, tree cover and terrain from `data/results/lga_table.json`. Area studied: Mushin + Shomolu LGAs, 33.7 km².
For: maze, adeleke, gateways, crossings, mushin, track, footbridge, gang. Last changed 2026-10-16, 254 lines.
Links to 2: `gidi:data/results/lga_table.json`, `gidi:docs/img/maze-vs-real.png`
Backlinks: 2 documents (`gidi:decisions/CODEBASE.md`, `gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/jungle-pattern-study.md` (0.44); `gidi:docs/hub-pattern-study.md` (0.38); `gidi:docs/foodgate-pattern-study.md` (0.35).

### `gidi:docs/oldisland-pattern-study.md`
**Old Island pattern study: Lagos Island → Old Island (v1)**. Old Island pattern study: Lagos Island → Old Island (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: island, island's, bridge's, palace, core's, fountains, shore, waterfront. Last changed 2026-10-14, 143 lines.
Links to 3: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/oldisland-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/heights-pattern-study.md` (0.34); `gidi:docs/oldshore-pattern-study.md` (0.31); `gidi:docs/estate-pattern-study.md` (0.25).

### `gidi:docs/oldshore-pattern-study.md`
**Old Shore pattern study: old Ikorodu → Old Shore (v1)**. Old Shore pattern study: old Ikorodu → Old Shore (v1): Status: generated for review (15 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: shore, jetty, pins, ikorodu's, ikorodu, town, ferry, fish. Last changed 2026-10-15, 145 lines.
Links to 4: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/oldshore-vs-real.png`, `gidi:scripts/study_boxheights.py`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/oldisland-pattern-study.md` (0.31); `gidi:docs/watertown-pattern-study.md` (0.23); `gidi:docs/foodgate-pattern-study.md` (0.22).

### `gidi:docs/port-pattern-study.md`
**The Port pattern study: Apapa → The Port (v1)**. The Port pattern study: Apapa → The Port (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: port, apapa, quay, yard, farm, yards, container, reserve. Last changed 2026-10-14, 128 lines.
Links to 2: `gidi:data/results/lga_table.json`, `gidi:docs/img/port-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/bazaar-pattern-study.md` (0.28); `gidi:docs/watertown-pattern-study.md` (0.25); `gidi:docs/capital-pattern-study.md` (0.22).

### `gidi:docs/railside-pattern-study.md`
**Railside pattern study: Agege, Ifako/Ijaye and Alimosho → Railside (v1)**. Railside pattern study: Agege, Ifako/Ijaye and Alimosho → Railside (v1): Status: generated for review (14 Oct 2026). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets and buildings from the rules. **No real street, building or name is copied into Gidi.**
For: railside, lgas, capital's, landmarks, pipeline, roundabout, ijaye, mounds. Last changed 2026-10-14, 125 lines.
Links to 3: `gidi:data/results/lga_table.json`, `gidi:docs/LAGOS-ISMS.md`, `gidi:docs/img/railside-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/capital-pattern-study.md` (0.4); `gidi:docs/estate-pattern-study.md` (0.31); `gidi:docs/bazaar-pattern-study.md` (0.3).

## gidi:docs/research
### `gidi:docs/research/LIFE-IN-LAGOS.md`
**Life in Lagos: what it's like to live there**. Life in Lagos: what it's like to live there: A research pass, 16 Oct 2026, for the owner's ask: "immerse yourself in what it's like to live in Lagos".
For: japa, feels, what's, guardian, december, true, rent, sapa. Last changed 2026-10-25, 329 lines.
Links to 3: `gidi:decisions/DECISIONS.md`, `gidi:decisions/world-life.md`, `gidi:docs/LAGOS-ISMS.md`
Backlinks: 4 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/world-life.md`, `gidi:docs/RESEARCH.md`, `gidi:docs/lagos-study/LIVING.md`), 0 code files ().
Nearest in words: `gidi:decisions/world-life.md` (0.27); `gidi:docs/lagos-lgas-research.md` (0.22); `gidi:decisions/IDEAS.md` (0.15).

## gidi:docs/studies
### `gidi:docs/studies/airport.md`
**The Airport: the deep study**. The Airport: the deep study: Inspired by Murtala Muhammed International Airport, Ikeja. Study area: 15.81 km², 15.81 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: airport, touching, transit, airline, restaurant, tenth, service, squares. Last changed 2026-10-15, 126 lines.
Links to 1: `gidi:docs/img/study-airport.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/estate.md` (0.73); `gidi:docs/studies/capital.md` (0.7); `gidi:docs/studies/heights.md` (0.7).

### `gidi:docs/studies/bazaar.md`
**The Bazaar: the deep study**. The Bazaar: the deep study: Inspired by Ojo (electronics market) + Trade Fair. Study area: 21.78 km², 21.49 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, power, energy, tenth, education, transit, store, squares. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-bazaar.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.79); `gidi:docs/studies/foodgate.md` (0.76); `gidi:docs/studies/railside.md` (0.75).

### `gidi:docs/studies/border.md`
**The Border: the deep study**. The Border: the deep study: Inspired by Badagry. Study area: 24.72 km², 20.74 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, tenth, roman, squares, catholic, power, worship, services. Last changed 2026-10-15, 125 lines.
Links to 1: `gidi:docs/img/study-border.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/foodgate.md` (0.75); `gidi:docs/studies/oldshore.md` (0.72); `gidi:docs/studies/jungle.md` (0.71).

### `gidi:docs/studies/capital.md`
**The Capital: the deep study**. The Capital: the deep study: Inspired by Ikeja. Study area: 15.64 km², 15.64 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: developed, power, touching, tenth, manufacturer, squares, beauty, planning. Last changed 2026-10-15, 125 lines.
Links to 1: `gidi:docs/img/study-capital.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.83); `gidi:docs/studies/estate.md` (0.81); `gidi:docs/studies/maze.md` (0.8).

### `gidi:docs/studies/estate.md`
**The Estate: the deep study**. The Estate: the deep study: Inspired by Magodo, Omole, Ikeja GRA. Study area: 24.26 km², 24.21 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, tenth, barrier, transportation, developed, squares, hospital, beauty. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-estate.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.84); `gidi:docs/studies/capital.md` (0.81); `gidi:docs/studies/oldshore.md` (0.8).

### `gidi:docs/studies/foodgate.md`
**Food Gate: the deep study**. Food Gate: the deep study: Inspired by Kosofe (Mile 12, Ketu, Ojota). Study area: 19.24 km², 19.2 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, power, developed, tenth, religious, transit, worship, organization. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-foodgate.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.86); `gidi:docs/studies/hub.md` (0.82); `gidi:docs/studies/port.md` (0.82).

### `gidi:docs/studies/frontier.md`
**The Frontier: the deep study**. The Frontier: the deep study: Inspired by Lekki + Ibeju-Lekki. Study area: 91.01 km², 88.92 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, barrier, tenth, power, grocery, squares, beauty, planning. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-frontier.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.84); `gidi:docs/studies/maze.md` (0.81); `gidi:docs/studies/heights.md` (0.81).

### `gidi:docs/studies/heights.md`
**The Heights: the deep study**. The Heights: the deep study: Inspired by Ikoyi, VI, Banana Island. Study area: 19.09 km², 16.99 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, tenth, historic, barrier, service, squares, communication, hotel. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-heights.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/frontier.md` (0.81); `gidi:docs/studies/estate.md` (0.77); `gidi:docs/studies/capital.md` (0.76).

### `gidi:docs/studies/hub.md`
**The Hub: the deep study**. The Hub: the deep study: Inspired by Oshodi + Ojuelegba (Surulere). Study area: 64.56 km², 64.5 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: transit, touching, transportation, tenth, squares, beauty, power, christian. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-hub.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/estate.md` (0.84); `gidi:docs/studies/port.md` (0.84); `gidi:docs/studies/oldshore.md` (0.84).

### `gidi:docs/studies/jungle.md`
**Jungle City: the deep study**. Jungle City: the deep study: Inspired by Ajegunle + Festac. Study area: 11.93 km², 11.85 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, communication, tenth, power, transit, squares, cemetery, worship. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-jungle.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/frontier.md` (0.79); `gidi:docs/studies/oldshore.md` (0.77); `gidi:docs/studies/hub.md` (0.77).

### `gidi:docs/studies/maze.md`
**The Maze: the deep study**. The Maze: the deep study: Inspired by Mushin + Shomolu. Study area: 33.66 km², 32.92 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, tenth, dealer, power, transit, transportation, developed, squares. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-maze.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.82); `gidi:docs/studies/frontier.md` (0.81); `gidi:docs/studies/capital.md` (0.8).

### `gidi:docs/studies/oldisland.md`
**Old Island: the deep study**. Old Island: the deep study: Inspired by Lagos Island. Study area: 9.38 km², 5.9 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: recreation, touching, service, travel, pedestrian, tenth, barrier, transit. Last changed 2026-10-15, 125 lines.
Links to 1: `gidi:docs/img/study-oldisland.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.75); `gidi:docs/studies/estate.md` (0.74); `gidi:docs/studies/capital.md` (0.73).

### `gidi:docs/studies/oldshore.md`
**Old Shore: the deep study**. Old Shore: the deep study: Inspired by Ikorodu + Epe. Study area: 20.35 km², 19.82 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, power, tenth, religious, transit, developed, squares, beauty. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-oldshore.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/foodgate.md` (0.86); `gidi:docs/studies/frontier.md` (0.84); `gidi:docs/studies/hub.md` (0.84).

### `gidi:docs/studies/port.md`
**The Port: the deep study**. The Port: the deep study: Inspired by Apapa + Mile 2 + the prison. Study area: 26.96 km², 19.36 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, pier, tenth, power, transit, transportation, developed, squares. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-port.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.84); `gidi:docs/studies/foodgate.md` (0.82); `gidi:docs/studies/oldshore.md` (0.81).

### `gidi:docs/studies/railside.md`
**Railside: the deep study**. Railside: the deep study: Inspired by Agege + Ifako-Ijaiye + Alimosho. Study area: 215.35 km², 215.35 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: power, touching, tenth, squares, beauty, planning, landfill, health. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-railside.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.81); `gidi:docs/studies/hub.md` (0.79); `gidi:docs/studies/capital.md` (0.79).

### `gidi:docs/studies/watertown.md`
**Water Town: the deep study**. Water Town: the deep study: Inspired by Makoko + Bariga + Agboyi + the sawmill. Study area: 7.27 km², 5.45 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, christian, tenth, education, venue, power, transit, worship. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-watertown.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/oldshore.md` (0.8); `gidi:docs/studies/yaba.md` (0.79); `gidi:docs/studies/frontier.md` (0.79).

### `gidi:docs/studies/yaba.md`
**Saba: the deep study**. Saba: the deep study: Inspired by Yaba and Akoka: the university, Sabo, Ojuelegba. Study area: 12.88 km², 10.64 km² of it land. Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.
For: touching, education, tenth, financial, service, transportation, squares, beauty. Last changed 2026-10-15, 127 lines.
Links to 1: `gidi:docs/img/study-yaba.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/studies/hub.md` (0.8); `gidi:docs/studies/maze.md` (0.8); `gidi:docs/studies/watertown.md` (0.79).

## gidi:docs
### `gidi:docs/watertown-pattern-study.md`
**Water Town pattern study: the Makoko–Iwaya and Bariga waterfront → Water Town (v1)**. Water Town pattern study: the Makoko–Iwaya and Bariga waterfront → Water Town (v1): Status: generated for review (13 Oct 2026; v2 the same day: the land is rebuilt as fingers running down to the shore). Same method as every district: we measure the real place, turn the numbers into rules, and generate original streets, houses and stilt houses from the rules. **No real street, building or name is copied into Gidi.**
For: fingers, stilt, huts, village, sawmill's, canoe, shore, okafor. Last changed 2026-10-14, 164 lines.
Links to 3: `gidi:data/results/lga_table.json`, `gidi:docs/img/watertown-fingers.png`, `gidi:docs/img/watertown-vs-real.png`
Backlinks: 1 documents (`gidi:docs/RESEARCH.md`), 0 code files ().
Nearest in words: `gidi:docs/port-pattern-study.md` (0.25); `gidi:docs/oldshore-pattern-study.md` (0.23); `gidi:docs/maze-pattern-study.md` (0.2).

## gidi:map/d15
### `gidi:map/d15/BUILDINGS.md`
**Mùṣá: the buildings draft and its hand pass**. Mùṣá: the buildings draft and its hand pass: Drafted by `scripts/draft_buildings.py` (owner, 23 Oct: real footprints, then hand). 1457 houses in 41 blocks. Each block's number is its place in size order. After the run, 31 houses that crossed the district line were taken out (the tool now keeps only houses wholly inside), leaving 1426; the counts below are from before that.
For: redrafted, pass, cleared, zoom, hand, given, holds, lanes. Last changed 2026-10-25, 263 lines.
Links to 6: `gidi:map/d15/STREETS.md`, `gidi:scripts/draft_buildings.py`, `gidi:scripts/draft_kinds.py`, `gidi:scripts/draft_looks.py`, `gidi:scripts/draft_storeys.py`, `gidi:scripts/draft_storeys_nearby.py`
Backlinks: 5 documents (`gidi:decisions/CHECKS.md`, `gidi:decisions/CODEBASE.md`, `gidi:decisions/DECISIONS.md`, `gidi:decisions/NOW.md`, `gidi:map/d15/STREETS.md`), 1 code files (`gidi:scripts/draft_buildings.py`).
Nearest in words: `gidi:decisions/NOW.md` (0.21); `gidi:decisions/DECISIONS.md` (0.12); `gidi-data:research/google/kits/old-town/tests/ot149/NOTES.md` (0.11).

### `gidi:map/d15/STREETS.md`
**Mùṣá (district 15): the road plan and where each street comes from**. Mùṣá (district 15): the road plan and where each street comes from: Roads only, drawn on the new frame (1:3). Every kept street sits on its real line, squeezed to the frame, at its real width (never shrunk). Real names live here only, never in the map. Buildings come later.
For: lane, repeats, nearby, parallel, twin, shot, south, isolo. Last changed 2026-10-25, 708 lines.
Links to 5: `gidi:map/d15/BUILDINGS.md`, `gidi:map/d15/road_reads.tsv`, `gidi:scripts/draft_crossings.py`, `gidi:scripts/draft_edge.py`, `gidi:scripts/draft_roads.py`
Backlinks: 3 documents (`gidi:decisions/CODEBASE.md`, `gidi:decisions/NOW.md`, `gidi:map/d15/BUILDINGS.md`), 0 code files ().
Nearest in words: `gidi:docs/lagos-study/roads/EARTH-CHECK.md` (0.17); `gidi-data:research/google/ibudo/study/INVENTORY.md` (0.13); `gidi:map/d15/BUILDINGS.md` (0.1).

