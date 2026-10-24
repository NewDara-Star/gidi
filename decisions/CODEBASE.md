# What the code holds: the three repos, one page

Read this before building anything new, so new work starts from what exists. Every file, with what it says it is,
when it last changed and who points to it, is in `docs/inventory/INVENTORY.md`. What looks dead or broken is in
`docs/inventory/SUSPECTS.md`. Since 24 Oct also (owner: "use the compiler to know what every piece of code is connected
to, and that every comment is correct"; "know what every document is meant for, like an Obsidian vault"):
`CODEMAP.md` (every function, class, method and constant, read by Python's `ast` and the TypeScript parser, with where
it is used and what nothing uses; `scripts/code_graph.py`), `COMMENTS.md` (comments naming code that exists nowhere)
and `VAULT.md` (every document: what it is for, its links, its backlinks, its nearest documents, orphans first;
`scripts/doc_vault.py`, graph in `vault.json`). The JavaScript parser is the TypeScript compiler already on this Mac
(stride-web's copy; `$GIDI_TS` points elsewhere); without it CODEMAP says JavaScript was not read.
`tests/test_inventory.py` holds the checker to its cases and runs with the hooks. All are made by
`scripts/inventory.py`; the hooks run it on every commit, and it can be run by hand:

    ~/.venvs/gidi/bin/python scripts/inventory.py

First made on 24 Oct 2026. Counts are tracked files.

Each part is marked:
- **live**: what the work runs on now
- **old map**: the generated city of 13-21 Oct, frozen. It is kept so it still builds and shows on the board. It is
  never extended (CLAUDE.md), and new work never reads from it.
- **history**: what a decision or study left behind; read it, don't build on it
- **other project**: not Gidi
- **to delete**: moved into `to-delete/` (24 Oct) for the owner to delete; `to-delete/README.md` says why each file went.
  The inventory lists these files but doesn't read them for references or names.

## The map in one breath

On 22 Oct the map restarted: Gidi is real Lagos miniaturised, 51 districts, every record drawn by hand on the board.
- **gidi** holds that map (`map/`, in the format `docs/MAP-FORMAT.md`), its checks and the drawing board. It still
  carries the old generated city beside it.
- **gidi-game** holds the builders: Blender scripts that build each thing a map record names (they are the kit). It
  also holds the Unreal project that imports and plays it.
- **gidi-data** is the study store: datasets, Google study shots, references, textures (about 22 GB, on this Mac
  only). Until 24 Oct it lived inside `~/Real-world`, World Drive, the owner's Finglas driving simulator.

## gidi (`~/gidi`, 604 files)

**Live: the new map (22 Oct on)**

| Where | What |
|---|---|
| `decisions/` | the owner's decisions, ideas, where the work stands, this page; `story/` is Tunde's story |
| `map/d15/` | Mùṣá (Mushin), the first district: `district.json`, `plan.json` (roads, blocks, buildings), `STREETS.md`, `BUILDINGS.md` |
| `schema/` | `map_schema.json` (every record type and field) and `kit_reads.json` (what the builders read, written by gidi-game `tools/kit_fields.py`) |
| `map-stamps/` | records made from a test spot (`ut01_emmanuel`), to stamp onto the board |
| `docs/MAP-FORMAT.md`, `docs/map-format-example/` | the format, and a worked example |
| `docs/lagos-study/` | the study of all of real Lagos behind the 51 districts: `STUDY.md`, `councils.md`, `roads/` (ROADS, EARTH-CHECK, NAMES), `similar/`, `LIVING.md` |
| `scripts/check_map.py` | the new map's checker (`check_map.py map`: PASS means no problem; fields still to fill are counted on its TODO line) |
| `scripts/check_rules.py` | every rule in DECISIONS.md has a row in CHECKS.md |
| `scripts/board_server.py` | the drawing board's server: saves board edits into `map/` (and old-map edits into `web/hand/`) |
| `scripts/frame_study.py`, `frame_footprints.py` | the board's study layers for the new frame (written to `web/frame-study.js`, `web/frame-tiles/`: generated, never committed) |
| `scripts/draft_buildings.py` | a district's first draft of buildings from its real blocks' houses (numbers only) |
| `scripts/check_real.py`, `realnames.py` | how close a map is to its real places; no real name on the map |
| `scripts/inventory.py` | this inventory |
| `web/board.html`, `board.js`, `frame.js`, `mapedit.js`, `faceedit.js` | the drawing board: `board.html?frame=new` is the new map's editor |
| `docs/BOARD.md` | the board's tools |
| `docs/RESEARCH.md` | the real Lagos research that stays, and which new districts each study serves |
| `docs/OLD-MAP-LESSONS.md` | what the old map's plans and passes taught that still holds |

**Old map (13-21 Oct, frozen)**

| Where | What |
|---|---|
| `scripts/` (the other ~70) | the old pipeline: study (`study_*`, `deep_*`), generate (`gen_fabric.py`, `district_profiles.py`, `landmarks.py`, `layout_v2.py`, `frame_network.py`), bake (`bake_web.py` and the passes it runs: roadclean, roadz, junctions, roadends, market_streets, isms, furniture, things, houses, fronts, compounds, trees, ground, groundpaint, surfaces, terrain, autoclean), hand (`hand.py`, `hand_*`, `hand_spots/`, `freeze_district.py`, `rebuild_areas.py`), check (`check_district.py`, `audit3d.py`, `explore_city.py`, `walknet.py`) |
| `web/gidi-data.js`, `gen-*.json`, `hand/`, `network.json`, `layout-v2.json`, `terrain*.json`, `locked.json`, `civic.json` and the rest of `web/*.json` | the old map's data: generated, baked and hand-edited |
| `web/app.js`, `shell.html`, `view3d.js`, `gidi-maps.html`, `scripts/build_viewer.py` | the old map viewer (2D and 3D) |
| `study-*.json` (85, at the top of the repo) | each old district's pattern study, read by the generator |
| `legacy/blender/` | the old map's Blender kit; the legacy tiles 6,12 / 7,12 / 8,13 must stay byte-identical; what it holds for the builders: `WHAT-IT-HELD.md` |
| `data/` | per-LGA numbers (`results/`) and the download scripts (`tools/`) |

**Research (written for the old map; its real Lagos numbers still hold).** Indexed in `docs/RESEARCH.md`:
- the pattern studies (15 in `docs/`, such as `docs/maze-pattern-study.md`) and the deep studies (`docs/studies/`, `docs/data/deep/`,
  `docs/DEEP-STUDY.md`), with their pictures in `docs/img/`
- `docs/look/research-*.md`, `docs/LAGOS-ISMS.md`, `docs/LAGOS-LIGHT.md`, `docs/research/LIFE-IN-LAGOS.md`,
  `docs/lagos-lgas-research.md`, `docs/gidi-data-plan.md`, `docs/DATA-SOURCES.md` (what was downloaded, and when it can go)
- `docs/hand/`: `maze-hub-lagos.md`, `borrowed-lagos.md`, `monument-briefs.md`; `ibudo/` and `realnames.txt` are old-map
  data still read by `check_real.py`, `realnames.py` (and so `check_map.py`), `rebuild_areas.py`, `draw_area.py`

**History**
- `decisions/HISTORY.md`: decisions that later ones replaced, and dropped ideas, word for word with what replaced them
- `to-delete/`: the old map's living tests, audits, calibration, plans and passes (91 files, 24 Oct), and this folder's
  old NOW log; their lessons are in `docs/OLD-MAP-LESSONS.md`

## gidi-game (`~/gidi-game`, 456 files; `Content/` is 34 GB on disk, nearly all generated or from Fab)

**Live**

| Where | What |
|---|---|
| `tools/*_build.py` | the builders: one thing each, part by part, from a recipe that is the map record's own fields. Things built: block, wall, pole, stall, furniture, umbrella, pickup, lorry, danfo, keke, molue, brt, person, loose. Shared: `vehicle_kit.py`, `vehicle_stickers.py`, `goods_kit.py`, `wear_layer.py` |
| `tools/fields.py`, `kit_fields.py` | each builder declares its fields; checked against the map both ways |
| `tools/map_build.py`, `spot_to_map.py`, `spot_assemble.py` | map records to recipes and a rendered scene, and back |
| `tools/play.sh`, `editor.sh`, `mode.sh`, `mode_sg.py`, `measure.sh`, `measure_csv.py`, `winshot.py`, `Config/DefaultDeviceProfiles.ini`, `docs/PERFORMANCE.md` | playing, the modes and measuring |
| `Content/Python/gidi_underdeck.py`, `gidi_modes.py`, `tools/underdeck_build.py`, `underdeck_extras.py` | the underdeck test street |
| `Content/Python/gidi_paint.py`, `gidi_plates.py`, `tools/plates.py`, `font_*.py`, `labels.py`, `lettering.py`, `trace_mark.py` | paint, number plates, Gidi's fonts and lettering |
| `Art/` | hand-made assets in Git LFS (vehicles 153, props 128, people 23, fonts, plates, textures); listed in `ASSETS.md` |
| `docs/ASSET-INVENTORY.md` | what the project already has (City Sample, Fab, Megascans): check before building |

**Reads the old map** (still runs, but on the generated city, so it moves to the new map when Unreal does)
- `Content/Python/gidi_import.py`, `tools/import.sh`: the city importer (old map tiles from gidi `web/city/`)
- `gidi_stream.py`, `tools/stream.sh`: tile streaming
- `gidi_heroes.py`: vehicles at the old map's spots
- `gidi_signs.py`: shop signs from the old kit's tiles
- `gidi_look.py`, `gidi_surfaces.py`, `gidi_cam.py`, `tools/shot.sh`, `look.sh`, `surfaces.sh`, `make_textures.py`
- `gidi_play.py`: the Ìbùdó play level
- `tools/perf.sh`: the old laptop test on Gidi_City, removed 24 Oct (gidi-game #70); `measure.sh` replaces it

**History**
- `tools/frame_motorpark.py`, `props_build.py`, `prop_basin_final.py` (the 19 Oct Lagos pass)
- `tools/vehicle_prep.py`, `vehicle_look.py`, `vehicle_export.py`, `photo.sh`, `Content/Python/gidi_photo.py` (the Meshy
  vehicles and photo mode)

## gidi-data (`~/gidi-data`): Gidi's study store, about 22 GB

Moved out of World Drive's folder (`~/Real-world`) on 24 Oct (owner: "take out the Gidi stuff from real world"),
with its tree kept, so every old path reads the same with `gidi-data` for `Real-world`. A local git repo with no
remote: it tracks only our own text (notes, the kit tests' scripts, READMEs: 42 files, read by the inventory); the
data stays on this Mac. Its `README.md` lists the folders:
- `research/data/`: the datasets (Google Open Buildings, Microsoft, Overture, WorldPop, WorldCover, DEM, deep-cache), about 20 GB
- `research/google/`: the Google study shots and the kit tests (`kits/old-town/tests/`, their notes and scripts)
- `research/refs/`, `research/models/`, `research/games/`: reference pictures, models and look-target clips
- `textures/polyhaven/`: the CC0 surfaces used by Blender and Unreal
- `assets/makehuman/`: the people assets

`~/Real-world` is World Drive alone again (tracked, last commit 5 Oct: `game/`, its `tools/`, `research/01-28`), a
different game; Gidi uses none of it. Two Lagos files World Drive tracks (`lagos_copernicus_glo30_dsm.tif`,
`lagos_overture_ferry_and_rail_segments.parquet`) were copied into `gidi-data/research/data/`, since gidi reads them.

## Known problems (24 Oct)

- **The study scripts of `docs/lagos-study/` are lost.** `STUDY.md` lists them (grid_bld, grid_orient, heights, roads,
  rasters, feat, classify, plots, gaz) and six data grids as "all in this folder". They were never committed and
  aren't anywhere on disk. The numbers stand, but can't be rebuilt.
- **A rule was "checked" by a script that never existed.** CHECKS.md held "Freeze everything" with the bake's
  DETERMINISTIC line from `tools/bake.sh`, which was never committed. It is marked GAP now.
- **The OSM extract is gone** (`lagos.osm.pbf`, `adm6.geojson`: the repo held only links to a deleted scratch
  folder). The old-map scripts that read it (`study_extract.py`, `study_isms.py`) can't run. That is fine: OSM is not
  used now.
- **CLAUDE.md's one rule named the old map's hand files** (`web/hand/<district>.json`; fixed 24 Oct, owner: "the new
  map is the truth"). It now names the records in `map/<dNN>/`.
- **`check_map.py map` always said FAIL** (fixed 24 Oct). All 35,707 of its problems were "missing field", so every run
  read FAIL and a real failure looked the same. Fields still to fill are now one TODO line (the board's amber); PASS
  means no problem; `--strict` fails on the TODOs too.
- ~~Unfinished work in old worktrees~~ (settled 24 Oct). Every branch whose work is in main was deleted (gidi 198
  local and 197 remote, gidi-game 27 and all remote); the unfinished ones were checked against the decisions, found
  replaced, saved as patches in `~/gidi-data/to-delete/branches/` and removed, and PR #18 was closed. Each repo has only
  `main` now.
- The board carries both maps. That is why the old map can't simply be moved away: `board.html` loads
  `web/gidi-data.js`, and `board_server.py` writes old-map edits into `web/hand/`.

## Removed on 24 Oct (all in git history, `git log --diff-filter=D --name-only` brings any back)

- `lagos.osm.pbf`, `adm6.geojson`: broken links
- `compare-maze.json`, and the 13 Oct OSM study scripts nothing pointed to: `scripts/compare.py`, `concept.py`,
  `fabric.py`, `lagoon.py`, `lgamap.py`, `lgas.py`, `sea.py`, `study.py`
- `web/three-app.js`, `three-shell.html`, `three-ui.js`, `scripts/gen3d.py`: the first 3D viewer (13 Oct), replaced by
  `web/view3d.js`

## Next clean-ups (the owner said yes to 1-3 on 24 Oct: "the new map is the truth")

1. **The old map, viewable only** (the owner's call, 24 Oct): its baked data and the board's view of it go into `legacy/`
   (the board still draws it); the scripts that make or tune it (the generator, studies, calibration, one-off fixes) go
   into `to-delete/`; the legacy tiles are checked byte-identical before merging. Its history docs went to `to-delete/`
   on 24 Oct.
2. ~~Give Gidi's data store its own folder~~ (done 24 Oct: `~/gidi-data`; 84 lines in gidi and 3 in gidi-game repointed, gidi-game #71; counted with `git diff -U0 origin/main | grep -c '^+.*gidi-data'`, without docs/inventory and this page).
   Open: a private GitHub remote for its text only, the owner's call.
3. ~~Retire `tools/perf.sh`~~ (removed 24 Oct, gidi-game #70). Still open: decide whether the Meshy vehicle path
   (`vehicle_prep.py` and the rest) stays, now that vehicles are built.
4. **A check that keeps this page true**: the hooks (24 Oct) run `inventory.py` with `check_rules.py` on every
   commit and block a new line naming a file that doesn't exist. Open: every new code file starts with what it is.
