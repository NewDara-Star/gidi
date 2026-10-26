# What the code holds: the three repos, one page

Read this before building anything new, so new work starts from what exists. Every file, with what it says it is,
when it last changed and who points to it, is in `docs/inventory/INVENTORY.md`. What looks dead or broken is in
`docs/inventory/SUSPECTS.md`. Also (owner, 24 Oct: "use the compiler to know what every piece of code is connected
to, and that every comment is correct"; "know what every document is meant for, like an Obsidian vault"):
`CODEMAP.md` (every function, class, method and constant, read by Python's `ast` and the TypeScript parser, with where
it is used and what nothing uses; `scripts/code_graph.py`), `COMMENTS.md` (comments naming code that exists nowhere)
and `VAULT.md` (every document: what it is for, its links, its backlinks, its nearest documents, orphans first;
`scripts/doc_vault.py`, graph in `vault.json`). The JavaScript parser is the TypeScript compiler already on this Mac
(stride-web's copy; `$GIDI_TS` points elsewhere); without it CODEMAP says JavaScript was not read.
`tests/test_inventory.py` holds the checker to its cases and runs with the hooks. All are made by
`scripts/inventory.py`; the hooks run it on every commit, and it can be run by hand:

    ~/.venvs/gidi/bin/python scripts/inventory.py

"Nothing uses it" is not "delete it" (owner, 25 Oct): a tool written for where Gidi is going stays without a caller.
What belongs to the old map or the old kit goes.

## The map in one breath

On 22 Oct the map restarted: Gidi is real Lagos miniaturised at 1:3, 51 districts, every record drawn by hand on the
board. The generated city of 13-21 Oct (the old map) and its Blender kit were deleted on 25 Oct (git tag
`before-cleanup-25oct` in gidi and gidi-game holds them; `docs/OLD-MAP-LESSONS.md` and `docs/OLD-KIT.md` keep what they
taught).
- **gidi** holds the map (`map/`, in the format `docs/MAP-FORMAT.md`), its checks and the drawing board.
- **gidi-game** holds the builders (Blender scripts that build each thing a map record names: they are the kit) and the
  Unreal project that plays it.
- **gidi-data** is the study store: datasets, Google study shots, references, textures (about 22 GB, on this Mac
  only).

## gidi (`~/gidi`, 259 files)

| Where | What |
|---|---|
| `decisions/` | the owner's decisions, ideas, where the work stands, this page; `HISTORY.md` the replaced decisions; `story/` is Tunde's story |
| `map/d15/` | Mùṣá (Mushin), the first district: `district.json`, `plan.json` (roads, blocks, buildings), `STREETS.md`, `BUILDINGS.md` |
| `schema/` | `map_schema.json` (every record type and field) and `kit_reads.json` (what the builders read, written by gidi-game `tools/kit_fields.py`) |
| `map-stamps/` | records made from a test spot (`ut01_emmanuel`), to stamp onto the board |
| `docs/MAP-FORMAT.md`, `docs/map-format-example/` | the format, and a worked example (also a stamp source) |
| `scripts/check_map.py`, `realnames.py` | the map's checker (`check_map.py map`: PASS means no problem; fields still to fill are counted on its TODO line); no real name on the map (`docs/hand/realnames.txt`) |
| `scripts/map_picture.py` | a picture of the map at every district's close: the whole city and a close view, red where land a drawn district should hold is held by none |
| `scripts/check_rules.py` | every rule in DECISIONS.md has a row in CHECKS.md |
| `scripts/board_server.py`, `web/board.html`, `frame.js`, `mapedit.js`, `faceedit.js`, `docs/BOARD.md` | the drawing board: serves the repo on 127.0.0.1, saves whole records into `map/` |
| `scripts/frame_study.py`, `frame_footprints.py` | the board's study underlay (`web/frame-study.js`, `web/frame-tiles/`: generated, never committed; can't be re-run, see below) |
| `scripts/draft_*.py` | a district's first drafts, each from real numbers or Street View readings: buildings, storeys (and from neighbours), kinds, roads, crossings, what stands along the roads, looks. Re-drafted only when the owner asks |
| `scripts/inventory.py`, `code_graph.py`, `doc_vault.py`, `js_symbols.mjs` | this inventory |
| `docs/lagos-study/` | the study of all of real Lagos behind the 51 districts: `STUDY.md`, `councils.md`, `roads/`, `similar/`, `LIVING.md` |
| `docs/RESEARCH.md` | the index of the Lagos research: which new districts each study serves |
| `scripts/study_boxheights.py`, `data/` | height bands for parts of an LGA; per-LGA numbers (`data/results/`) and the download scripts (`data/tools/`) |

**Research written for the old map** (its real Lagos numbers hold; each page says at its top what was deleted):
the pattern studies (15 in `docs/`, such as `docs/maze-pattern-study.md`) and the deep studies (`docs/studies/`,
`docs/data/deep/`, `docs/DEEP-STUDY.md`), with their pictures in `docs/img/`; `docs/look/research-*.md`,
`docs/LAGOS-ISMS.md`, `docs/LAGOS-LIGHT.md`, `docs/research/LIFE-IN-LAGOS.md`, `docs/lagos-lgas-research.md`,
`docs/gidi-data-plan.md`, `docs/DATA-SOURCES.md`; `docs/hand/` (`maze-hub-lagos.md`, `borrowed-lagos.md`,
`monument-briefs.md`).

## gidi-game (`~/gidi-game`, 502 files; `Content/` is mostly generated or from Fab)

| Where | What |
|---|---|
| `tools/*_build.py` | the builders: one thing each, part by part, from a recipe that is the map record's own fields: block, wall, pole, stall, leanto, furniture, umbrella, junction, road, pickup, lorry, danfo, keke, molue, brt, person, loose, props. Shared: `vehicle_kit.py`, `vehicle_stickers.py`, `goods_kit.py`, `zinc_kit.py`, `junction_geo.py`, `wear_layer.py` |
| `tools/fields.py`, `kit_fields.py` | each builder declares its fields; checked against the map both ways |
| `tools/map_build.py`, `spot_to_map.py`, `spot_assemble.py`, `road_draft.py` | map records to recipes and a rendered scene, and back; a road's loose things drafted as records |
| `tools/street_test.py`, `street_join.py`, `street_ground.py`, `Content/Python/gidi_street.py` | the street test: Mùṣá houses round a lane, built and measured in Unreal |
| `Content/Python/gidi_underdeck.py`, `tools/underdeck_build.py`, `underdeck_extras.py` | the underdeck test street |
| `Content/Python/gidi_surfaces.py`, `gidi_look.py`, `gidi_heroes.py`, `gidi_modes.py`, `tools/surfaces.sh`, `make_textures.py` | the masters, surfaces and import settings; a level's sky and lens; the built vehicles brought in; the modes |
| `tools/play.sh`, `editor.sh`, `mode.sh`, `mode_sg.py`, `measure.sh`, `measure_csv.py`, `memreport.sh`, `memreport_later.py`, `package.sh`, `watchdog.sh`, `winshot.py`, `docs/PERFORMANCE.md` | playing, the modes, measuring, and the watchdog |
| `tools/img_diff.py`, `kit_compare.py`, `road_look.py`, `piece_match.py`, `lap_check.py`, `look_travels.py`, `vehicle_look.py` | test pictures and comparisons |
| `Content/Python/gidi_paint.py`, `gidi_plates.py`, `tools/plates.py`, `font_*.py`, `labels.py`, `lettering.py`, `trace_mark.py` | paint, number plates, Gidi's fonts and lettering |
| `tools/vehicle_prep.py`, `vehicle_export.py` | a Meshy model made game-ready (for the hard shapes code can't do); a built vehicle's game models |
| `Content/Python/gidi_scan_export.py`, `tools/scan_export.sh`, `scan_shrink.py`, `fab_list.sh` | the project's Megascans as images for the Blender tests; what came from Fab |
| `Art/` | hand-made assets in Git LFS (vehicles, props, people, fonts, plates, textures); listed in `ASSETS.md` |
| `docs/ASSET-INVENTORY.md` | what the project already has (City Sample, Fab, Megascans): check before building |

## gidi-data (`~/gidi-data`): Gidi's study store, about 22 GB

Moved out of World Drive's folder (`~/Real-world`) on 24 Oct (owner: "take out the Gidi stuff from real world"),
with its tree kept. A local git repo with no remote: it tracks only our own text (notes, the kit tests' records,
READMEs: 40 files, read by the inventory); the data stays on this Mac. Its `README.md` lists the folders:
- `research/data/`: the datasets (Google Open Buildings, Microsoft, Overture, WorldPop, WorldCover, DEM, deep-cache), about 20 GB
- `research/google/`: the Google study shots and the kit tests (`kits/old-town/tests/`, their notes)
- `research/refs/`, `research/models/`, `research/games/`: reference pictures, models and look-target clips
- `textures/polyhaven/`: the CC0 surfaces used by Blender and Unreal
- `assets/makehuman/`: the people assets

`~/Real-world` is World Drive alone (the owner's driving simulator, a different game); Gidi uses none of it. Two Lagos
files it tracks were copied into `gidi-data/research/data/`, since gidi reads them.

## Deleted on 25 Oct (clean-up 00; git tag `before-cleanup-25oct`)

The old map and everything that made, checked, viewed or played it: 71 scripts (the studies, the generator,
the bake and its passes, the hand edits, the district checks), `legacy/`, the old web viewer and data, the 86 study
files, `to-delete/` (the old plans and pass reports), `web/city/` (the 3D tiles); in gidi-game the importer, tile
streaming, signs, check camera, the Ìbùdó level and photo mode, and the 19 Oct motor park frame. Untracked: the old
test levels, builds, logs, the SUMO-era `.venv/` and `~/gidi-worktrees/`. `docs/OLD-MAP-LESSONS.md` and
`docs/OLD-KIT.md` say what was kept from them.

## Known problems

- **The first Lagos study's scripts are lost** (`STUDY.md` lists them): never committed, nowhere on disk. Its numbers
  stand, but can't be rebuilt.
- **The roads study and the frame study can't be re-run** (found 25 Oct): their working files lived in a temp folder
  and are gone, and the roads study reads the lost study's grids. Their outputs stand (`docs/lagos-study/roads/`,
  `web/frame-study.js`, with a copy in `~/gidi-data/frame-backup-25oct/`); what a re-run takes is in NOW's Owed list.
- **"Freeze everything" has no check** (CHECKS.md GAP): its old check was the old map's bake, deleted with it.
- gidi-data has no remote: a private GitHub remote for its text only is the owner's call.
