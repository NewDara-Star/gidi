# Code map

Made by `scripts/inventory.py` with `scripts/code_graph.py`: every function, class, method and top-level constant in gidi, gidi-game and gidi-data, read by the parsers (JavaScript read by the TypeScript compiler at /Users/Star/stride-web/node_modules/typescript). 7257 pieces of code in 266 files: 21 used nowhere, 114 used only by name where their file is not imported (a hint: a call by string, or dead). "Imported by" is Python imports; a page's scripts share its names. A file run as a script (by a shell line, Blender, the board) shows in INVENTORY.md's "Refs", not here.

## Used nowhere (by file)

- `gidi-game:Content/Python/gidi_signs.py`: `place_signs` (function, line 55)
- `gidi-game:tools/map_build.py`: `BUILDER` (const, line 45)
- `gidi-game:tools/plates.py`: `PLATE` (const, line 28)
- `gidi:docs/lagos-study/roads/scripts/common.py`: `C250` (const, line 13), `lga_shapes` (function, line 24)
- `gidi:legacy/blender/city.py`: `_clear` (function, line 287), `blocks_faces` (function, line 453)
- `gidi:legacy/blender/gidi_kit/blocks.py`: `street_face` (function, line 33)
- `gidi:legacy/blender/wear_sheet.py`: `at_` (const, line 67), `at_` (const, line 67)
- `gidi:scripts/frame_footprints.py`: `NJ` (const, line 35)
- `gidi:scripts/frame_study.py`: `group_poly` (function, line 254), `inD` (const, line 266)
- `gidi:scripts/gen_fabric.py`: `paths_u` (const, line 839)
- `gidi:scripts/hand_spots/ibudo_spot1.py`: `alley_ground` (const, line 59)
- `gidi:scripts/junctions.py`: `R_MAX` (const, line 19)
- `gidi:scripts/map02.py`: `SWEEP` (const, line 35)
- `gidi:scripts/study_analyse.py`: `pnames` (const, line 219)
- `gidi:scripts/terrain.py`: `H_` (const, line 26)
- `gidi:web/board.js`: `gkey` (function, line 72), `segDir` (function, line 130)

## Every code file

### `gidi-data:research/data/results/heights.py`
8 defined (8 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/data/results/landpop.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/facade_hand.py`
54 defined (53 used, 1 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot13/mk13_first.py`
3 defined (3 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot13/sbs.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot149/hand149.py`
56 defined (56 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot149/mk149_first.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot149/mk149_pass.py`
17 defined (17 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`
14 defined (14 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot45/hand45.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot45/hand45_2.py`
1 defined (1 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot45/mk45_first.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot45/mk45_pass.py`
17 defined (17 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot45/mk45_pass2.py`
11 defined (11 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot45/sbs.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot73/hand73.py`
2 defined (2 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot73/mk73_first.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/ot73/mk73_pass.py`
17 defined (17 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tools/part_view.py`
46 defined (44 used, 2 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/textured.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tools/sheet.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:Content/Python/gidi_cam.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:Content/Python/gidi_heroes.py`
20 defined (20 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_paint.py`, `gidi-game:Content/Python/gidi_plates.py`. Imported by: `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `HERE` in `gidi-game:Content/Python/gidi_underdeck.py`; `DEST` in `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `TILE` in `gidi-game:Content/Python/gidi_import.py`; `HERO_V` in `gidi-game:Content/Python/gidi_underdeck.py`; `HEROES` in `gidi-game:Content/Python/gidi_underdeck.py`; `_is_paint` in `gidi-game:Content/Python/gidi_underdeck.py`; `say` in `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `_master` in `gidi-game:Content/Python/gidi_street.py`; `_sig` in `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `_import` in `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `load` in `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `place` in `gidi-game:Content/Python/gidi_import.py`

### `gidi-game:Content/Python/gidi_import.py`
31 defined (31 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_stream.py`, `gidi-game:Content/Python/gidi_surfaces.py`. Imported by: `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `STATE` in `gidi-game:Content/Python/gidi_underdeck.py`; `say` in `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `masters` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `_slot_kind` in `gidi-game:Content/Python/gidi_underdeck.py`; `_pipeline` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `_environment` in `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `tile_map` in `gidi-game:Content/Python/gidi_play.py`; `_sig` in `gidi-game:Content/Python/gidi_underdeck.py`

### `gidi-game:Content/Python/gidi_look.py`
2 defined (2 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `apply` in `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`

### `gidi-game:Content/Python/gidi_modes.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `people_levels` in `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `open_clean` in `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `add_level` in `gidi-game:Content/Python/gidi_play.py`; `save_play` in `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `scene_count` in `gidi-game:Content/Python/gidi_play.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`

### `gidi-game:Content/Python/gidi_paint.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_surfaces.py`. Imported by: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_photo.py`.
Used elsewhere: `MASTER` in `gidi-game:Content/Python/gidi_heroes.py`; `MASTER_V` in `gidi-game:Content/Python/gidi_heroes.py`; `WEAR` in `gidi-game:Content/Python/gidi_heroes.py`; `say` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_photo.py`; `master` in `gidi-game:Content/Python/gidi_heroes.py`; `instance` in `gidi-game:Content/Python/gidi_heroes.py`

### `gidi-game:Content/Python/gidi_photo.py`
29 defined (29 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_paint.py`, `gidi-game:Content/Python/gidi_plates.py`. Imported by: nothing.

### `gidi-game:Content/Python/gidi_plates.py`
18 defined (18 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `HERE` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `ART` in `gidi-game:Content/Python/gidi_heroes.py`; `DEST` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `MASTER` in `gidi-game:Content/Python/gidi_heroes.py`; `MASTER_V` in `gidi-game:Content/Python/gidi_heroes.py`; `SPEC` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `say` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `number_for` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `data_for` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_photo.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `_master` in `gidi-game:Content/Python/gidi_heroes.py`; `instances` in `gidi-game:Content/Python/gidi_heroes.py`

### `gidi-game:Content/Python/gidi_play.py`
22 defined (22 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_modes.py`. Imported by: nothing.

### `gidi-game:Content/Python/gidi_scan_export.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:Content/Python/gidi_signs.py`
6 defined (5 used, 0 maybe, 1 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:Content/Python/gidi_stream.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_import.py`.
Used elsewhere: `MAP` in `gidi-game:Content/Python/gidi_import.py`; `say` in `gidi-game:Content/Python/gidi_import.py`; `apply` in `gidi-game:Content/Python/gidi_import.py`

### `gidi-game:Content/Python/gidi_street.py`
21 defined (21 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_modes.py`. Imported by: nothing.

### `gidi-game:Content/Python/gidi_surfaces.py`
28 defined (28 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_paint.py`.
Used elsewhere: `GEN` in `gidi-game:Content/Python/gidi_import.py`; `MATS` in `gidi-game:Content/Python/gidi_import.py`; `_scan` in `gidi-game:Content/Python/gidi_paint.py`; `say` in `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_paint.py`; `textures` in `gidi-game:Content/Python/gidi_paint.py`; `instances` in `gidi-game:Content/Python/gidi_import.py`

### `gidi-game:Content/Python/gidi_underdeck.py`
25 defined (25 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_import.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:Content/Python/gidi_plates.py`. Imported by: nothing.

### `gidi-game:tools/block_build.py`
50 defined (50 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`, `gidi-game:tools/zinc_kit.py`. Imported by: nothing.

### `gidi-game:tools/brt_build.py`
65 defined (63 used, 2 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`, `gidi-game:tools/vehicle_stickers.py`. Imported by: nothing.

### `gidi-game:tools/danfo_build.py`
83 defined (81 used, 2 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_stickers.py`. Imported by: nothing.

### `gidi-game:tools/fields.py`
19 defined (19 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/junction_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/leanto_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/map_build.py`, `gidi-game:tools/molue_build.py`, `gidi-game:tools/person_build.py`, `gidi-game:tools/pickup_build.py`, `gidi-game:tools/pole_build.py`, `gidi-game:tools/road_build.py`, `gidi-game:tools/spot_to_map.py`, `gidi-game:tools/stall_build.py`, `gidi-game:tools/umbrella_build.py`, `gidi-game:tools/wall_build.py`.
Used elsewhere: `OPTIONS` in `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`; `kind` in `gidi-game:tools/block_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/junction_build.py`, `gidi-game:tools/loose_build.py`; `name` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/leanto_build.py`; `get` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/furniture_build.py`; `items` in `gidi-game:tools/danfo_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/lorry_build.py`; `values` in `gidi-game:tools/lorry_build.py`, `gidi-game:tools/road_build.py`, `gidi-game:tools/spot_to_map.py`; `track` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/furniture_build.py`

### `gidi-game:tools/font_brush.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/font_space.py`. Imported by: nothing.

### `gidi-game:tools/font_plate.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/font_space.py`. Imported by: nothing.

### `gidi-game:tools/font_punct.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/font_space.py`. Imported by: nothing.

### `gidi-game:tools/font_space.py`
13 defined (9 used, 4 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:tools/font_brush.py`, `gidi-game:tools/font_plate.py`, `gidi-game:tools/font_punct.py`, `gidi-game:tools/lettering.py`.
Used elsewhere: `SIDE` in `gidi-game:tools/font_plate.py`; `Flat` in `gidi-game:tools/font_brush.py`, `gidi-game:tools/font_plate.py`, `gidi-game:tools/font_punct.py`, `gidi-game:tools/lettering.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`, `gidi:scripts/things.py`; `main` in `gidi-game:tools/font_brush.py`, `gidi-game:tools/font_plate.py`, `gidi-game:tools/font_punct.py`

### `gidi-game:tools/font_specimen.py`
3 defined (3 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/frame_motorpark.py`
70 defined (70 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/furniture_build.py`
46 defined (46 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/vehicle_kit.py`. Imported by: nothing.

### `gidi-game:tools/goods_kit.py`
34 defined (34 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/vehicle_kit.py`. Imported by: `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`.
Used elsewhere: `PHI` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `rgb` in `gidi-game:tools/stall_build.py`; `Goods` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `m` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `bm` in `gidi-game:tools/stall_build.py`; `box` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `cyl` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `ring` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `done` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`; `build` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`; `materials` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`; `litter` in `gidi-game:tools/loose_build.py`

### `gidi-game:tools/img_diff.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/junction_build.py`
28 defined (28 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/road_build.py`. Imported by: nothing.

### `gidi-game:tools/junction_geo.py`
43 defined (43 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`.
Used elsewhere: `T_WALL` in `gidi-game:tools/road_build.py`; `add` in `gidi-game:tools/map_build.py`; `left` in `gidi-game:tools/road_build.py`; `length` in `gidi-game:tools/road_build.py`; `at` in `gidi-game:tools/map_build.py`; `edge` in `gidi-game:tools/road_build.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `side` in `gidi-game:tools/road_build.py`; `out` in `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`; `groups` in `gidi-game:tools/map_build.py`; `junction` in `gidi-game:tools/map_build.py`; `nodes` in `gidi-game:tools/map_build.py`; `pieces` in `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`; `clear_of` in `gidi-game:tools/map_build.py`; `recipe` in `gidi-game:tools/map_build.py`; `d` in `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`; `roads` in `gidi-game:tools/map_build.py`; `P` in `gidi-game:tools/road_build.py`; `j` in `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`; `gs` in `gidi-game:tools/road_build.py`

### `gidi-game:tools/keke_build.py`
84 defined (82 used, 2 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`, `gidi-game:tools/vehicle_stickers.py`. Imported by: nothing.

### `gidi-game:tools/kit_compare.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/kit_fields.py`
20 defined (20 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`.
Used elsewhere: `TOOLS` in `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`; `GAME` in `gidi-game:tools/spot_to_map.py`; `declared` in `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`; `base` in `gidi-game:tools/spot_to_map.py`; `map_path` in `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`; `a` in `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`; `opt` in `gidi-game:tools/map_build.py`, `gidi-game:tools/spot_to_map.py`

### `gidi-game:tools/labels.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/lap_check.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/leanto_build.py`
36 defined (34 used, 2 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`, `gidi-game:tools/zinc_kit.py`. Imported by: nothing.

### `gidi-game:tools/lettering.py`
38 defined (38 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/font_space.py`. Imported by: nothing.

### `gidi-game:tools/look_travels.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/loose_build.py`
5 defined (5 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/vehicle_kit.py`. Imported by: nothing.

### `gidi-game:tools/lorry_build.py`
68 defined (63 used, 5 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`. Imported by: nothing.

### `gidi-game:tools/make_textures.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/map_build.py`
33 defined (32 used, 0 maybe, 1 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/junction_geo.py`, `gidi-game:tools/kit_fields.py`. Imported by: `gidi-game:tools/street_test.py`.
Used elsewhere: `load` in `gidi-game:tools/street_test.py`; `rows` in `gidi-game:tools/street_test.py`; `recipe` in `gidi-game:tools/street_test.py`; `things` in `gidi-game:tools/street_test.py`; `localise` in `gidi-game:tools/street_test.py`; `a` in `gidi-game:tools/street_test.py`; `OUT` in `gidi-game:tools/street_test.py`; `recs` in `gidi-game:tools/street_test.py`; `ts` in `gidi-game:tools/street_test.py`; `x` in `gidi-game:tools/street_test.py`; `y` in `gidi-game:tools/street_test.py`; `z` in `gidi-game:tools/street_test.py`; `turn` in `gidi-game:tools/street_test.py`; `pitch` in `gidi-game:tools/street_test.py`

### `gidi-game:tools/measure_csv.py`
33 defined (33 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/memreport_later.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/mode_sg.py`
3 defined (3 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/molue_build.py`
75 defined (74 used, 1 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`, `gidi-game:tools/vehicle_stickers.py`. Imported by: nothing.

### `gidi-game:tools/person_build.py`
86 defined (85 used, 1 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`. Imported by: nothing.

### `gidi-game:tools/pickup_build.py`
57 defined (55 used, 2 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`, `gidi-game:tools/vehicle_stickers.py`. Imported by: nothing.

### `gidi-game:tools/piece_match.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/plates.py`
29 defined (28 used, 0 maybe, 1 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/pole_build.py`
60 defined (59 used, 1 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`. Imported by: nothing.

### `gidi-game:tools/prop_basin_final.py`
121 defined (121 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/props_build.py`
37 defined (35 used, 2 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/road_build.py`
99 defined (98 used, 1 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/junction_geo.py`. Imported by: `gidi-game:tools/junction_build.py`.
Used elsewhere: `A` in `gidi-game:tools/junction_build.py`; `FIELDS` in `gidi-game:tools/junction_build.py`; `HW` in `gidi-game:tools/junction_build.py`; `SURF` in `gidi-game:tools/junction_build.py`; `T_WALL` in `gidi-game:tools/junction_build.py`; `KERB` in `gidi-game:tools/junction_build.py`; `SAND_C` in `gidi-game:tools/junction_build.py`; `EARTH` in `gidi-game:tools/junction_build.py`; `SILT_WET` in `gidi-game:tools/junction_build.py`; `SILT_CRUST` in `gidi-game:tools/junction_build.py`; `WATER` in `gidi-game:tools/junction_build.py`; `lerp3` in `gidi-game:tools/junction_build.py`; `n3` in `gidi-game:tools/junction_build.py`; `smooth` in `gidi-game:tools/junction_build.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `vert` in `gidi-game:tools/junction_build.py`; `face` in `gidi-game:tools/junction_build.py`; `part` in `gidi-game:tools/junction_build.py`; `grid` in `gidi-game:tools/junction_build.py`; `fsplit` in `gidi-game:tools/junction_build.py`; `frange` in `gidi-game:tools/junction_build.py`; `rows` in `gidi-game:tools/junction_build.py`; `road_z` in `gidi-game:tools/junction_build.py`; `road_colour` in `gidi-game:tools/junction_build.py`; `slot_of` in `gidi-game:tools/junction_build.py`; `runs` in `gidi-game:tools/junction_build.py`; `silt_z` in `gidi-game:tools/junction_build.py`; `water_z` in `gidi-game:tools/junction_build.py`; `wall_colour` in `gidi-game:tools/junction_build.py`; `make_objects` in `gidi-game:tools/junction_build.py`

### `gidi-game:tools/road_draft.py`
14 defined (14 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/road_look.py`
50 defined (50 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/scan_shrink.py`
2 defined (2 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/spot_assemble.py`
20 defined (20 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/wear_layer.py`. Imported by: nothing.

### `gidi-game:tools/spot_to_map.py`
25 defined (25 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/kit_fields.py`. Imported by: nothing.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`

### `gidi-game:tools/stall_build.py`
74 defined (73 used, 1 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/vehicle_kit.py`. Imported by: nothing.

### `gidi-game:tools/street_ground.py`
17 defined (17 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/street_join.py`
0 defined (0 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/street_test.py`
34 defined (34 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/map_build.py`. Imported by: nothing.

### `gidi-game:tools/trace_mark.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/umbrella_build.py`
59 defined (58 used, 1 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`. Imported by: nothing.

### `gidi-game:tools/underdeck_build.py`
90 defined (90 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`

### `gidi-game:tools/underdeck_extras.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/vehicle_export.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/vehicle_kit.py`
33 defined (33 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/leanto_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`, `gidi-game:tools/pickup_build.py`, `gidi-game:tools/pole_build.py`, `gidi-game:tools/stall_build.py`, `gidi-game:tools/umbrella_build.py`, `gidi-game:tools/wall_build.py`, `gidi-game:tools/zinc_kit.py`.
Used elsewhere: `MATS` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/leanto_build.py`; `ROOT` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/molue_build.py`; `sc` in `gidi-game:tools/block_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/leanto_build.py`, `gidi-game:tools/lorry_build.py`; `mat` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/keke_build.py`; `rgb` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/keke_build.py`; `start` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/keke_build.py`; `obj` in `gidi-game:tools/block_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/keke_build.py`; `apply_mods` in `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/pickup_build.py`, `gidi-game:tools/umbrella_build.py`; `solidify` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`; `smooth` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `_box` in `gidi-game:tools/goods_kit.py`; `boolean` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/pickup_build.py`; `cut` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`; `copy` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/leanto_build.py`; `prism` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `prism_yz` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `prism_xy` in `gidi-game:tools/block_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/pickup_build.py`; `grow` in `gidi-game:tools/pickup_build.py`; `box` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/goods_kit.py`; `tube` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/leanto_build.py`; `cylinder` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `join` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/furniture_build.py`, `gidi-game:tools/keke_build.py`; `fillet` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `lin` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`; `arc` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `loft` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `opening` in `gidi-game:tools/block_build.py`, `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`; `cut_door` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `wheel` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`; `arc_shell` in `gidi-game:tools/keke_build.py`, `gidi-game:tools/lorry_build.py`, `gidi-game:tools/molue_build.py`, `gidi-game:tools/pickup_build.py`

### `gidi-game:tools/vehicle_look.py`
68 defined (67 used, 1 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/vehicle_prep.py`
77 defined (77 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/vehicle_stickers.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:tools/brt_build.py`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/molue_build.py`, `gidi-game:tools/pickup_build.py`.
Used elsewhere: `SC` in `gidi-game:tools/danfo_build.py`, `gidi-game:tools/pickup_build.py`; `vinyl` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`; `frame` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/molue_build.py`; `mark` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/molue_build.py`; `star` in `gidi-game:tools/danfo_build.py`; `oval` in `gidi-game:tools/danfo_build.py`; `rect` in `gidi-game:tools/molue_build.py`; `tape` in `gidi-game:tools/danfo_build.py`; `text` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/danfo_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/molue_build.py`; `plate` in `gidi-game:tools/brt_build.py`, `gidi-game:tools/keke_build.py`, `gidi-game:tools/molue_build.py`; `plate_mount` in `gidi-game:tools/danfo_build.py`, `gidi-game:tools/pickup_build.py`

### `gidi-game:tools/wall_build.py`
61 defined (61 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/vehicle_kit.py`. Imported by: nothing.

### `gidi-game:tools/wear_layer.py`
17 defined (16 used, 1 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:tools/spot_assemble.py`.
Used elsewhere: `ground` in `gidi-game:tools/spot_assemble.py`; `apply` in `gidi-game:tools/spot_assemble.py`; `find_wear` in `gidi-game:tools/spot_assemble.py`

### `gidi-game:tools/winshot.py`
5 defined (5 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/zinc_kit.py`
33 defined (33 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/vehicle_kit.py`. Imported by: `gidi-game:tools/block_build.py`, `gidi-game:tools/leanto_build.py`.
Used elsewhere: `RUST_DARK` in `gidi-game:tools/block_build.py`; `table` in `gidi-game:tools/leanto_build.py`; `hexmix` in `gidi-game:tools/block_build.py`; `slope` in `gidi-game:tools/block_build.py`, `gidi-game:tools/leanto_build.py`

### `gidi:data/results/heights.py`
8 defined (8 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:data/results/landpop.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:docs/lagos-study/roads/scripts/borders.py`
84 defined (77 used, 7 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:docs/lagos-study/roads/scripts/common.py`
18 defined (16 used, 0 maybe, 2 unused). Imports: none of ours. Imported by: `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/ladder.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/ob50.py`, `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:docs/lagos-study/roads/scripts/plot_places.py`, `gidi:docs/lagos-study/roads/scripts/report.py`, `gidi:docs/lagos-study/roads/scripts/skeleton.py`, `gidi:docs/lagos-study/roads/scripts/wc50.py`, `gidi:scripts/frame_footprints.py`, `gidi:scripts/frame_study.py`.
Used elsewhere: `DATA` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/ob50.py`, `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:docs/lagos-study/roads/scripts/skeleton.py`; `SCR` in `gidi:docs/lagos-study/roads/scripts/report.py`; `LAGOS` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/places.py`; `WORK` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/ladder.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/ob50.py`; `OUT` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/ladder.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/plot_places.py`; `T` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/ob50.py`, `gidi:docs/lagos-study/roads/scripts/places.py`; `TI` in `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/places.py`; `X0` in `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:docs/lagos-study/roads/scripts/plot_places.py`, `gidi:scripts/frame_study.py`; `Y0` in `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:docs/lagos-study/roads/scripts/plot_places.py`, `gidi:scripts/frame_study.py`; `C` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:docs/lagos-study/roads/scripts/plot_places.py`; `NX` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/ob50.py`, `gidi:docs/lagos-study/roads/scripts/places.py`; `NY` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/ob50.py`, `gidi:docs/lagos-study/roads/scripts/places.py`; `SCALE` in `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:scripts/frame_footprints.py`, `gidi:scripts/frame_study.py`; `FRAME` in `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:scripts/frame_footprints.py`, `gidi:scripts/frame_study.py`; `ij` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/ob50.py`, `gidi:docs/lagos-study/roads/scripts/places.py`; `up` in `gidi:docs/lagos-study/roads/scripts/borders.py`, `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:docs/lagos-study/roads/scripts/report.py`

### `gidi:docs/lagos-study/roads/scripts/gaz.py`
2 defined (2 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/places.py`.
Used elsewhere: `load` in `gidi:docs/lagos-study/roads/scripts/network.py`, `gidi:docs/lagos-study/roads/scripts/places.py`

### `gidi:docs/lagos-study/roads/scripts/ladder.py`
47 defined (45 used, 2 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:docs/lagos-study/roads/scripts/network.py`
79 defined (73 used, 6 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`, `gidi:docs/lagos-study/roads/scripts/gaz.py`. Imported by: nothing.

### `gidi:docs/lagos-study/roads/scripts/ob50.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:docs/lagos-study/roads/scripts/places.py`
89 defined (88 used, 1 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`, `gidi:docs/lagos-study/roads/scripts/gaz.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`.
Used elsewhere: `segs` in `gidi:legacy/blender/city.py`; `F` in `gidi:legacy/blender/city.py`; `water` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `n` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `z` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `idx` in `gidi:legacy/blender/city.py`; `z` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `idx` in `gidi:legacy/blender/city.py`; `G` in `gidi:legacy/blender/generate.py`; `gx` in `gidi:legacy/blender/city.py`; `gy` in `gidi:legacy/blender/city.py`; `gi` in `gidi:legacy/blender/city.py`; `size` in `gidi:legacy/blender/city.py`; `u` in `gidi:legacy/blender/city.py`; `pts` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `pc` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `cx` in `gidi:legacy/blender/generate.py`; `cy` in `gidi:legacy/blender/generate.py`; `inside` in `gidi:legacy/blender/city.py`; `P` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`

### `gidi:docs/lagos-study/roads/scripts/plot_places.py`
14 defined (13 used, 1 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: `gidi:docs/lagos-study/roads/scripts/report.py`.
Used elsewhere: `Pz` in `gidi:docs/lagos-study/roads/scripts/report.py`; `place` in `gidi:docs/lagos-study/roads/scripts/report.py`; `PL` in `gidi:docs/lagos-study/roads/scripts/report.py`; `roof` in `gidi:docs/lagos-study/roads/scripts/report.py`; `draw` in `gidi:docs/lagos-study/roads/scripts/report.py`; `frame_box` in `gidi:docs/lagos-study/roads/scripts/report.py`; `INNER` in `gidi:docs/lagos-study/roads/scripts/report.py`; `labs` in `gidi:docs/lagos-study/roads/scripts/report.py`

### `gidi:docs/lagos-study/roads/scripts/report.py`
35 defined (32 used, 3 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`, `gidi:docs/lagos-study/roads/scripts/plot_places.py`. Imported by: nothing.

### `gidi:docs/lagos-study/roads/scripts/skeleton.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:docs/lagos-study/roads/scripts/wc50.py`
5 defined (5 used, 0 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:docs/lagos-study/similar/scripts/analyse.py`
43 defined (41 used, 2 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:docs/lagos-study/similar/scripts/appendix.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:docs/lagos-study/similar/scripts/common.py`
22 defined (22 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`.
Used elsewhere: `F` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `K` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`; `Un` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `ny` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `nx` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `ext` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `NAMES` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`; `draw_lga` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`; `boundaries` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `centroid` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `STATE` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `CORE` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`; `INNER` in `gidi:docs/lagos-study/similar/scripts/plot_units.py`, `gidi:docs/lagos-study/similar/scripts/plots.py`

### `gidi:docs/lagos-study/similar/scripts/finger.py`
23 defined (22 used, 1 maybe, 0 unused). Imports: `gidi:docs/lagos-study/similar/scripts/know.py`. Imported by: nothing.

### `gidi:docs/lagos-study/similar/scripts/know.py`
2 defined (2 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:docs/lagos-study/similar/scripts/finger.py`.
Used elsewhere: `KNOW` in `gidi:docs/lagos-study/similar/scripts/finger.py`; `items` in `gidi:docs/lagos-study/similar/scripts/finger.py`

### `gidi:docs/lagos-study/similar/scripts/plot_units.py`
8 defined (5 used, 3 maybe, 0 unused). Imports: `gidi:docs/lagos-study/similar/scripts/common.py`. Imported by: nothing.

### `gidi:docs/lagos-study/similar/scripts/plots.py`
17 defined (15 used, 2 maybe, 0 unused). Imports: `gidi:docs/lagos-study/similar/scripts/common.py`. Imported by: nothing.

### `gidi:docs/lagos-study/similar/scripts/report.py`
11 defined (8 used, 3 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:docs/lagos-study/similar/scripts/seeds.py`
2 defined (2 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:docs/lagos-study/similar/scripts/units.py`.
Used elsewhere: `load` in `gidi:docs/lagos-study/similar/scripts/units.py`

### `gidi:docs/lagos-study/similar/scripts/units.py`
27 defined (27 used, 0 maybe, 0 unused). Imports: `gidi:docs/lagos-study/similar/scripts/seeds.py`. Imported by: nothing.

### `gidi:legacy/blender/act1_sheet.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/catalogue.py`
15 defined (14 used, 1 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/city.py`
91 defined (88 used, 1 maybe, 2 unused). Imports: `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/city_run.py`
18 defined (18 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:legacy/blender/coverage.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:legacy/blender/generate.py`
67 defined (67 used, 0 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/places.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/gidi_kit/__init__.py`
0 defined (0 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:legacy/blender/gidi_kit/archetypes.py`
17 defined (17 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/props.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/gidi_kit/zinc.py`. Imported by: `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `house` in `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/places.py`; `extension` in `gidi:legacy/blender/gidi_kit/registry.py`; `stall` in `gidi:legacy/blender/gidi_kit/registry.py`; `kiosk` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `face_me` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `park_office` in `gidi:legacy/blender/act1_sheet.py`; `buka` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `lockup_open` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `office` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/gidi_kit/registry.py`

### `gidi:legacy/blender/gidi_kit/blocks.py`
8 defined (7 used, 0 maybe, 1 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/parts.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`.
Used elsewhere: `STOREY` in `gidi:legacy/blender/gidi_kit/kinds.py`; `faces` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/places.py`; `block` in `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`; `perimeter` in `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`; `flagpole` in `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`; `dome` in `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`; `minaret` in `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/places.py`

### `gidi:legacy/blender/gidi_kit/boats.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/new_kit_sheet2.py`.
Used elsewhere: `hull` in `gidi:legacy/blender/gidi_kit/kinds.py`; `ferry` in `gidi:legacy/blender/new_kit_sheet2.py`; `water_bus` in `gidi:legacy/blender/new_kit_sheet2.py`; `outboard_canoe` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet2.py`; `dredger` in `gidi:legacy/blender/new_kit_sheet2.py`; `BUILDERS` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet2.py`

### `gidi:legacy/blender/gidi_kit/core.py`
26 defined (26 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/facade.py`, `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/props.py`, `gidi:legacy/blender/gidi_kit/roadbed.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/gidi_kit/zinc.py`, `gidi:legacy/blender/kinds_sheet.py`, `gidi:legacy/blender/kit_test.py`, `gidi:legacy/blender/lights_sheet.py`, `gidi:legacy/blender/monuments_sheet.py`, `gidi:legacy/blender/new_kit_sheet.py`, `gidi:legacy/blender/new_kit_sheet2.py`, `gidi:legacy/blender/reach_sheet.py`, `gidi:legacy/blender/roadside_sheet.py`, `gidi:legacy/blender/scene.py`, `gidi:legacy/blender/vehicles_sheet.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `Rng` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:scripts/board_server.py`, `gidi:scripts/things.py`; `child` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`; `pick` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`; `chance` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`; `between` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`; `MissingRecord` in `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `need` in `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/roadbed.py`, `gidi:legacy/blender/gidi_kit/street.py`; `hex_rgb` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`; `shade` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/draft.py`; `MeshBuilder` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `face` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `box` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/boats.py`; `merge_mesh` in `gidi:legacy/blender/gidi_kit/parts.py`; `to_object` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `frame` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/facade.py`; `at` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`; `centroid` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`; `signed_area` in `gidi:legacy/blender/gidi_kit/archetypes.py`; `ccw` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`; `edge_out` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`; `offset` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`; `chamfer` in `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `prism` in `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`

### `gidi:legacy/blender/gidi_kit/detail.py`
5 defined (5 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/props.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/gidi_kit/zinc.py`, `gidi:legacy/blender/kit_test.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `LEVEL` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/kit_test.py`; `web` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/gutters.py`; `segs` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `SIGNS` in `gidi:legacy/blender/city.py`; `record_text` in `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/props.py`

### `gidi:legacy/blender/gidi_kit/draft.py`
64 defined (63 used, 1 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/roadbed.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/gidi_kit/zinc.py`. Imported by: `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/gidi_kit/zinc.py`, `gidi:legacy/blender/kit_draft.py`.
Used elsewhere: `R` in `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/street.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `zinc_slope` in `gidi:legacy/blender/gidi_kit/zinc.py`; `slab_blotch` in `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/zinc.py`; `blotch` in `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/wear.py`; `roof_pitched` in `gidi:legacy/blender/gidi_kit/parts.py`; `patch` in `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/wear.py`; `bare_block` in `gidi:legacy/blender/gidi_kit/wear.py`; `age_face` in `gidi:legacy/blender/gidi_kit/wear.py`; `litter_piece` in `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/street.py`; `refuse_heap` in `gidi:legacy/blender/gidi_kit/street.py`; `pole` in `gidi:legacy/blender/gidi_kit/street.py`; `tree` in `gidi:legacy/blender/gidi_kit/parcels.py`; `person` in `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/street.py`; `band` in `gidi:legacy/blender/gidi_kit/parcels.py`; `gutter` in `gidi:legacy/blender/gidi_kit/gutters.py`; `_slabs` in `gidi:legacy/blender/gidi_kit/gutters.py`; `street` in `gidi:legacy/blender/gidi_kit/street.py`; `props` in `gidi:legacy/blender/gidi_kit/street.py`; `spot` in `gidi:legacy/blender/kit_draft.py`

### `gidi:legacy/blender/gidi_kit/facade.py`
20 defined (20 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/parts.py`. Imported by: `gidi:legacy/blender/gidi_kit/oldtown.py`.
Used elsewhere: `MORTAR` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `window` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `pipe` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `wire` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `tarp` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `bars` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `draw` in `gidi:legacy/blender/gidi_kit/oldtown.py`

### `gidi:legacy/blender/gidi_kit/goods.py`
29 defined (29 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/props.py`. Imported by: `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`.
Used elsewhere: `SACK` in `gidi:legacy/blender/gidi_kit/draft.py`; `TARP` in `gidi:legacy/blender/gidi_kit/draft.py`; `BAG` in `gidi:legacy/blender/gidi_kit/draft.py`; `CLOTH` in `gidi:legacy/blender/gidi_kit/draft.py`; `PLASTIC` in `gidi:legacy/blender/gidi_kit/draft.py`; `CARTON` in `gidi:legacy/blender/gidi_kit/draft.py`; `soft` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `tarp` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `PRINT` in `gidi:legacy/blender/gidi_kit/draft.py`; `PRODUCE` in `gidi:legacy/blender/gidi_kit/draft.py`; `CRATE` in `gidi:legacy/blender/gidi_kit/draft.py`; `BOTTLE` in `gidi:legacy/blender/gidi_kit/draft.py`; `WHITE_CARTON` in `gidi:legacy/blender/gidi_kit/draft.py`; `BALE` in `gidi:legacy/blender/gidi_kit/draft.py`; `bale` in `gidi:legacy/blender/gidi_kit/draft.py`; `sack_open` in `gidi:legacy/blender/gidi_kit/draft.py`; `crate` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `carton` in `gidi:legacy/blender/gidi_kit/draft.py`; `_at` in `gidi:legacy/blender/gidi_kit/draft.py`; `leaf` in `gidi:legacy/blender/gidi_kit/draft.py`; `draw` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `weather` in `gidi:legacy/blender/gidi_kit/oldtown.py`

### `gidi:legacy/blender/gidi_kit/gutters.py`
17 defined (17 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/draft.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `DUST` in `gidi:legacy/blender/city.py`; `DIRT` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `RUBBISH` in `gidi:legacy/blender/gidi_kit/draft.py`; `PIECE` in `gidi:legacy/blender/gidi_kit/draft.py`; `pieces` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `gutter` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/wear_sheet.py`; `_slabs` in `gidi:legacy/blender/gidi_kit/draft.py`

### `gidi:legacy/blender/gidi_kit/kinds.py`
36 defined (36 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:legacy/blender/gidi_kit/street.py`. Imported by: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/structures.py`.
Used elsewhere: `STOREY` in `gidi:legacy/blender/gidi_kit/archetypes.py`; `footprint` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/places.py`; `T` in `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/parcels.py`; `_done` in `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/places.py`; `stilt` in `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `canoe` in `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/structures.py`; `raft` in `gidi:legacy/blender/gidi_kit/registry.py`; `sawdust` in `gidi:legacy/blender/gidi_kit/registry.py`; `_mound` in `gidi:legacy/blender/gidi_kit/parcels.py`; `brazilian` in `gidi:legacy/blender/gidi_kit/registry.py`; `gatehouse` in `gidi:legacy/blender/gidi_kit/registry.py`; `_chair` in `gidi:legacy/blender/gidi_kit/places.py`; `generator` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `water_tank` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `container` in `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `stack` in `gidi:legacy/blender/gidi_kit/registry.py`; `trailer` in `gidi:legacy/blender/gidi_kit/registry.py`; `pen` in `gidi:legacy/blender/gidi_kit/registry.py`; `cow` in `gidi:legacy/blender/gidi_kit/parcels.py`; `scrap` in `gidi:legacy/blender/gidi_kit/registry.py`; `checkpoint` in `gidi:legacy/blender/gidi_kit/registry.py`; `container_shop` in `gidi:legacy/blender/gidi_kit/registry.py`; `mound` in `gidi:legacy/blender/gidi_kit/registry.py`; `unfinished_house` in `gidi:legacy/blender/gidi_kit/registry.py`; `refinery_column` in `gidi:legacy/blender/gidi_kit/registry.py`; `flare_stack` in `gidi:legacy/blender/gidi_kit/registry.py`; `colonial_house` in `gidi:legacy/blender/gidi_kit/registry.py`; `fishing_hut` in `gidi:legacy/blender/gidi_kit/registry.py`; `border_booth` in `gidi:legacy/blender/gidi_kit/registry.py`; `border_canopy` in `gidi:legacy/blender/gidi_kit/registry.py`

### `gidi:legacy/blender/gidi_kit/landmarks.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/places.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/new_kit_sheet.py`, `gidi:legacy/blender/new_kit_sheet2.py`.
Used elsewhere: `crown_hall` in `gidi:legacy/blender/new_kit_sheet.py`; `central_mosque` in `gidi:legacy/blender/new_kit_sheet.py`; `cathedral` in `gidi:legacy/blender/new_kit_sheet2.py`; `first_storey_house` in `gidi:legacy/blender/gidi_kit/kinds.py`; `heritage_strip` in `gidi:legacy/blender/new_kit_sheet2.py`; `civic_tower` in `gidi:legacy/blender/new_kit_sheet2.py`; `market_block` in `gidi:legacy/blender/new_kit_sheet2.py`; `refinery` in `gidi:legacy/blender/new_kit_sheet2.py`; `freedom_ground` in `gidi:legacy/blender/new_kit_sheet2.py`; `BY_NAME` in `gidi:legacy/blender/city.py`; `PARCEL_BY_NAME` in `gidi:legacy/blender/city.py`; `build` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/registry.py`

### `gidi:legacy/blender/gidi_kit/materials.py`
18 defined (18 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/lights_sheet.py`, `gidi:legacy/blender/monuments_sheet.py`, `gidi:legacy/blender/new_kit_sheet.py`, `gidi:legacy/blender/new_kit_sheet2.py`, `gidi:legacy/blender/reach_sheet.py`, `gidi:legacy/blender/roadside_sheet.py`, `gidi:legacy/blender/scene.py`, `gidi:legacy/blender/vehicles_sheet.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `add` in `gidi:legacy/blender/city.py`; `link` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/scene.py`; `mix` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `math` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `ramp` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/scene.py`; `master` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`

### `gidi:legacy/blender/gidi_kit/monuments.py`
23 defined (22 used, 1 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/structures.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/lights_sheet.py`, `gidi:legacy/blender/monuments_sheet.py`, `gidi:legacy/blender/new_kit_sheet2.py`, `gidi:legacy/blender/reach_sheet.py`.
Used elsewhere: `founder` in `gidi:legacy/blender/monuments_sheet.py`; `masquerade` in `gidi:legacy/blender/monuments_sheet.py`; `drummer` in `gidi:legacy/blender/monuments_sheet.py`; `statue` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/lights_sheet.py`, `gidi:legacy/blender/monuments_sheet.py`, `gidi:legacy/blender/new_kit_sheet2.py`; `sculpture` in `gidi:legacy/blender/monuments_sheet.py`; `clock_tower` in `gidi:legacy/blender/monuments_sheet.py`; `lighthouse` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/monuments_sheet.py`; `arch` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/monuments_sheet.py`; `led_board` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/monuments_sheet.py`; `horse` in `gidi:legacy/blender/gidi_kit/parcels.py`; `horse_rider` in `gidi:legacy/blender/new_kit_sheet2.py`; `hunter` in `gidi:legacy/blender/new_kit_sheet2.py`; `beach_arch` in `gidi:legacy/blender/new_kit_sheet2.py`; `mural_wall` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet2.py`; `billboard` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet2.py`; `the_reach` in `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/reach_sheet.py`; `three_elders` in `gidi:legacy/blender/lights_sheet.py`; `saxophonist` in `gidi:legacy/blender/lights_sheet.py`; `BUILDERS` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/new_kit_sheet2.py`

### `gidi:legacy/blender/gidi_kit/oldtown.py`
39 defined (38 used, 1 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/facade.py`, `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/props.py`, `gidi:legacy/blender/gidi_kit/roadbed.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/gidi_kit/zinc.py`. Imported by: `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/kit_test.py`.
Used elsewhere: `STATE_WEAR` in `gidi:legacy/blender/gidi_kit/draft.py`; `mat` in `gidi:legacy/blender/gidi_kit/draft.py`; `rects` in `gidi:legacy/blender/gidi_kit/draft.py`; `faces` in `gidi:legacy/blender/gidi_kit/draft.py`; `_on_face` in `gidi:legacy/blender/gidi_kit/draft.py`; `plank_shutter` in `gidi:legacy/blender/gidi_kit/draft.py`; `leanto_frame` in `gidi:legacy/blender/gidi_kit/draft.py`; `leanto` in `gidi:legacy/blender/gidi_kit/draft.py`; `plank_stall` in `gidi:legacy/blender/gidi_kit/draft.py`; `cage_stall` in `gidi:legacy/blender/gidi_kit/draft.py`; `glass_cabinet` in `gidi:legacy/blender/gidi_kit/draft.py`; `SNACKS` in `gidi:legacy/blender/gidi_kit/draft.py`; `display_cabinet` in `gidi:legacy/blender/gidi_kit/draft.py`; `drinks_fridge` in `gidi:legacy/blender/gidi_kit/draft.py`; `POSTER` in `gidi:legacy/blender/gidi_kit/draft.py`; `mono_frame` in `gidi:legacy/blender/gidi_kit/draft.py`; `building` in `gidi:legacy/blender/gidi_kit/draft.py`; `frontage` in `gidi:legacy/blender/gidi_kit/draft.py`; `median_wall` in `gidi:legacy/blender/gidi_kit/draft.py`; `build` in `gidi:legacy/blender/kit_test.py`

### `gidi:legacy/blender/gidi_kit/parcels.py`
35 defined (35 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/street.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/new_kit_sheet2.py`.
Used elsewhere: `_flat` in `gidi:legacy/blender/gidi_kit/landmarks.py`; `_bbox_frame` in `gidi:legacy/blender/gidi_kit/landmarks.py`; `_scatter` in `gidi:legacy/blender/gidi_kit/landmarks.py`; `tree` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `pitch` in `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `green` in `gidi:legacy/blender/gidi_kit/landmarks.py`; `square` in `gidi:legacy/blender/new_kit_sheet2.py`; `refinery` in `gidi:legacy/blender/new_kit_sheet2.py`; `BUILDERS` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/new_kit_sheet2.py`; `build` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/registry.py`

### `gidi:legacy/blender/gidi_kit/parts.py`
25 defined (25 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/gidi_kit/zinc.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/facade.py`, `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/props.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `STOREY` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`; `cyl` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/facade.py`; `bar` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/facade.py`; `text` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/monuments.py`; `walls` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`; `burglar_bars` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/roadside.py`; `window` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/facade.py`; `door` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`; `roller_shutter` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `balcony` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`; `corrugated` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`; `roof_slopes` in `gidi:legacy/blender/gidi_kit/draft.py`; `roof_pitched` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `roof_flat` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `water_tank` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/kinds.py`; `satellite_dish` in `gidi:legacy/blender/gidi_kit/archetypes.py`; `tyre` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/facade.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`; `generator` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/wear_sheet.py`; `unfinished_storey` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/places.py`; `_band_face` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `compound_wall` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/places.py`; `signboard` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`; `awning` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`

### `gidi:legacy/blender/gidi_kit/people.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/parts.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/props.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/vehicles_sheet.py`.
Used elsewhere: `SKIN` in `gidi:legacy/blender/gidi_kit/draft.py`; `ANKARA` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/props.py`; `PLAIN` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/props.py`; `DRESS` in `gidi:legacy/blender/gidi_kit/draft.py`; `L` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/boats.py`; `sphere` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/street.py`; `limb` in `gidi:legacy/blender/gidi_kit/monuments.py`; `person` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/draft.py`; `seated_rider` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/vehicles_sheet.py`

### `gidi:legacy/blender/gidi_kit/places.py`
58 defined (56 used, 2 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/blocks.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:legacy/blender/gidi_kit/street.py`. Imported by: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/registry.py`.
Used elsewhere: `_poly` in `gidi:legacy/blender/gidi_kit/landmarks.py`; `_done` in `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`; `mosque` in `gidi:legacy/blender/gidi_kit/registry.py`; `church` in `gidi:legacy/blender/gidi_kit/registry.py`; `school` in `gidi:legacy/blender/gidi_kit/registry.py`; `clinic` in `gidi:legacy/blender/gidi_kit/registry.py`; `phone_mall` in `gidi:legacy/blender/gidi_kit/registry.py`; `plaza` in `gidi:legacy/blender/gidi_kit/registry.py`; `strip` in `gidi:legacy/blender/gidi_kit/registry.py`; `bakery` in `gidi:legacy/blender/gidi_kit/registry.py`; `print_shop` in `gidi:legacy/blender/gidi_kit/registry.py`; `warehouse` in `gidi:legacy/blender/gidi_kit/registry.py`; `tank` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `crane` in `gidi:legacy/blender/gidi_kit/registry.py`; `flats` in `gidi:legacy/blender/gidi_kit/registry.py`; `mansion` in `gidi:legacy/blender/gidi_kit/registry.py`; `villa` in `gidi:legacy/blender/gidi_kit/registry.py`; `tower` in `gidi:legacy/blender/gidi_kit/registry.py`; `bank_tower` in `gidi:legacy/blender/gidi_kit/registry.py`; `office` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `barracks` in `gidi:legacy/blender/gidi_kit/registry.py`; `cellblock` in `gidi:legacy/blender/gidi_kit/registry.py`; `hotel` in `gidi:legacy/blender/gidi_kit/registry.py`; `nightclub` in `gidi:legacy/blender/gidi_kit/registry.py`; `stands` in `gidi:legacy/blender/gidi_kit/registry.py`; `terminal` in `gidi:legacy/blender/gidi_kit/registry.py`; `station` in `gidi:legacy/blender/gidi_kit/registry.py`; `toll_booth` in `gidi:legacy/blender/gidi_kit/registry.py`; `toll_canopy` in `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/registry.py`; `cctv_tower` in `gidi:legacy/blender/gidi_kit/registry.py`

### `gidi:legacy/blender/gidi_kit/props.py`
22 defined (22 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/street.py`. Imported by: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`.
Used elsewhere: `CHAIR_COLS` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/street.py`; `UMBRELLA_COLS` in `gidi:legacy/blender/gidi_kit/street.py`; `chair` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/street.py`; `bench` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/street.py`; `table` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/street.py`; `drum` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`; `jerrycan` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/goods.py`; `crate` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `basin` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/goods.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/street.py`; `umbrella` in `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/street.py`; `wheelbarrow` in `gidi:legacy/blender/gidi_kit/street.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`; `loaves` in `gidi:legacy/blender/gidi_kit/street.py`; `washing_line` in `gidi:legacy/blender/gidi_kit/archetypes.py`; `board` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`; `soot` in `gidi:legacy/blender/gidi_kit/archetypes.py`; `coal_fire` in `gidi:legacy/blender/gidi_kit/archetypes.py`; `notes_fan` in `gidi:legacy/blender/gidi_kit/street.py`; `ticket_book` in `gidi:legacy/blender/gidi_kit/street.py`; `generator` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `bin_drum` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `awning` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`

### `gidi:legacy/blender/gidi_kit/registry.py`
7 defined (6 used, 1 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/kinds_sheet.py`.
Used elsewhere: `BUILDINGS` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/kinds_sheet.py`; `CIVIC_PLOTS` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/kinds_sheet.py`; `POI_PLACES` in `gidi:legacy/blender/city.py`; `PARCELS` in `gidi:legacy/blender/city.py`; `CIVIC` in `gidi:legacy/blender/city.py`; `builder` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`

### `gidi:legacy/blender/gidi_kit/roadbed.py`
17 defined (17 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`. Imported by: `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`.
Used elsewhere: `COLOURS` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `_smooth` in `gidi:legacy/blender/gidi_kit/draft.py`; `grids` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `_ruts` in `gidi:legacy/blender/gidi_kit/draft.py`; `_edge_rut` in `gidi:legacy/blender/gidi_kit/draft.py`; `height` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `bare` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `layers` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `build` in `gidi:legacy/blender/gidi_kit/oldtown.py`

### `gidi:legacy/blender/gidi_kit/roadside.py`
16 defined (16 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/props.py`. Imported by: `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:legacy/blender/lights_sheet.py`, `gidi:legacy/blender/roadside_sheet.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `street_light` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:legacy/blender/lights_sheet.py`, `gidi:legacy/blender/roadside_sheet.py`; `direction_sign` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/roadside_sheet.py`; `gantry` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/roadside_sheet.py`; `disc_sign` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/roadside_sheet.py`; `traffic_light` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/lights_sheet.py`; `police_kiosk` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`; `warden_post` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/wear_sheet.py`

### `gidi:legacy/blender/gidi_kit/rules.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`. Imported by: `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `CHARACTER` in `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`; `UNFINISHED_SHARE` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `FLOOD` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `STREET` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `C` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/places.py`; `C` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/places.py`; `C` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/places.py`; `compound_spec` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/wear_sheet.py`; `house_spec` in `gidi:legacy/blender/gidi_kit/archetypes.py`

### `gidi:legacy/blender/gidi_kit/street.py`
24 defined (24 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/props.py`. Imported by: `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/places.py`, `gidi:legacy/blender/gidi_kit/props.py`, `gidi:legacy/blender/gidi_kit/structures.py`.
Used elsewhere: `road_condition` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `turning_head` in `gidi:legacy/blender/city.py`; `road` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `markings` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `kerbs` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `speed_bump` in `gidi:legacy/blender/generate.py`; `drain` in `gidi:legacy/blender/generate.py`; `pole` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`; `wire` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `transformer` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/places.py`; `LITTER` in `gidi:legacy/blender/gidi_kit/draft.py`; `litter_piece` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/kinds.py`; `refuse_heap` in `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `agbero` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`; `wheelbarrow_vendor` in `gidi:legacy/blender/act1_sheet.py`; `fruit_seller` in `gidi:legacy/blender/act1_sheet.py`; `parking_boy` in `gidi:legacy/blender/act1_sheet.py`; `bread_hawker` in `gidi:legacy/blender/act1_sheet.py`; `rail_market` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`

### `gidi:legacy/blender/gidi_kit/structures.py`
29 defined (29 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/kinds.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/street.py`. Imported by: `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/new_kit_sheet.py`, `gidi:legacy/blender/roadside_sheet.py`.
Used elsewhere: `RAMP` in `gidi:legacy/blender/city.py`; `profile` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet.py`, `gidi:legacy/blender/roadside_sheet.py`; `deck_line` in `gidi:legacy/blender/roadside_sheet.py`; `MURAL_PALETTES` in `gidi:legacy/blender/gidi_kit/monuments.py`; `flyover` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet.py`; `approach` in `gidi:legacy/blender/city.py`; `skywalk` in `gidi:legacy/blender/city.py`; `snap_footbridge` in `gidi:legacy/blender/city.py`; `CANAL_W` in `gidi:legacy/blender/city.py`; `footbridge` in `gidi:legacy/blender/city.py`; `jetty` in `gidi:legacy/blender/city.py`; `expressway` in `gidi:legacy/blender/city.py`; `BRIDGE_H` in `gidi:legacy/blender/city.py`; `long_bridge` in `gidi:legacy/blender/city.py`; `cable_bridge` in `gidi:legacy/blender/city.py`; `rail` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet.py`; `canal` in `gidi:legacy/blender/city.py`; `culvert` in `gidi:legacy/blender/city.py`; `quay` in `gidi:legacy/blender/city.py`; `boardwalk` in `gidi:legacy/blender/city.py`; `estate_wall` in `gidi:legacy/blender/city.py`; `estate_gate` in `gidi:legacy/blender/city.py`

### `gidi:legacy/blender/gidi_kit/textured.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/kit_test.py`.
Used elsewhere: `apply` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/kit_test.py`

### `gidi:legacy/blender/gidi_kit/vehicles.py`
56 defined (56 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/props.py`. Imported by: `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/new_kit_sheet.py`, `gidi:legacy/blender/new_kit_sheet2.py`, `gidi:legacy/blender/vehicles_sheet.py`.
Used elsewhere: `condition` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `L` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `body` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `lamp` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `danfo` in `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/vehicles_sheet.py`; `korope` in `gidi:legacy/blender/vehicles_sheet.py`; `brt` in `gidi:legacy/blender/vehicles_sheet.py`; `keke` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/vehicles_sheet.py`; `okada` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `saloon` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `car` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `task_force_truck` in `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/city.py`; `tipper` in `gidi:legacy/blender/vehicles_sheet.py`; `tanker` in `gidi:legacy/blender/vehicles_sheet.py`; `wheelbarrow` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/vehicles_sheet.py`; `CONTAINER_COLS` in `gidi:legacy/blender/gidi_kit/draft.py`; `container_truck` in `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/new_kit_sheet.py`; `lorry_911` in `gidi:legacy/blender/new_kit_sheet.py`; `wagon` in `gidi:legacy/blender/new_kit_sheet.py`; `TRAIN` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet.py`; `ambulance` in `gidi:legacy/blender/new_kit_sheet2.py`; `molue` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet2.py`; `forklift` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/new_kit_sheet2.py`; `BUILDERS` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/new_kit_sheet2.py`, `gidi:legacy/blender/vehicles_sheet.py`; `LENGTH` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/new_kit_sheet2.py`, `gidi:legacy/blender/vehicles_sheet.py`; `COMMERCIAL` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`; `mix` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`

### `gidi:legacy/blender/gidi_kit/wear.py`
25 defined (25 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/parts.py`. Imported by: `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `DIRT` in `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `GRIME` in `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `RUST` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `CEMENT` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `BLOCK` in `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `MORTAR` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `OFF` in `gidi:legacy/blender/gidi_kit/draft.py`; `mix` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `smooth` in `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `Weather` in `gidi:legacy/blender/gidi_kit/parts.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `wall` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `prism` in `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `seen` in `gidi:legacy/blender/gidi_kit/parts.py`; `foot` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `DARK` in `gidi:legacy/blender/gidi_kit/oldtown.py`; `streak` in `gidi:legacy/blender/gidi_kit/draft.py`; `patch` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `bare_block` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `lnb_arm` in `gidi:legacy/blender/gidi_kit/archetypes.py`; `marks` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`; `age_face` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/draft.py`; `meter_drop` in `gidi:legacy/blender/city.py`, `gidi:legacy/blender/wear_sheet.py`

### `gidi:legacy/blender/gidi_kit/zinc.py`
11 defined (11 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/draft.py`. Imported by: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`.
Used elsewhere: `RUST` in `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `COVER` in `gidi:legacy/blender/gidi_kit/draft.py`; `_mix` in `gidi:legacy/blender/gidi_kit/parts.py`; `sag_at` in `gidi:legacy/blender/gidi_kit/archetypes.py`; `sheets` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `slope` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `GRIME` in `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`; `slab` in `gidi:legacy/blender/gidi_kit/draft.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/parts.py`

### `gidi:legacy/blender/kinds_sheet.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/registry.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/kit_draft.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/draft.py`. Imported by: nothing.

### `gidi:legacy/blender/kit_test.py`
35 defined (35 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/oldtown.py`, `gidi:legacy/blender/gidi_kit/textured.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/lights_sheet.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/montage.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:legacy/blender/monuments_sheet.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/new_kit_sheet.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/new_kit_sheet2.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/boats.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/landmarks.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/gidi_kit/parcels.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/reach_sheet.py`
3 defined (3 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/monuments.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/roadside_sheet.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/structures.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/scene.py`
5 defined (5 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`. Imported by: `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`, `gidi:legacy/blender/generate.py`, `gidi:legacy/blender/kinds_sheet.py`, `gidi:legacy/blender/kit_test.py`, `gidi:legacy/blender/lights_sheet.py`, `gidi:legacy/blender/monuments_sheet.py`, `gidi:legacy/blender/new_kit_sheet.py`, `gidi:legacy/blender/new_kit_sheet2.py`, `gidi:legacy/blender/reach_sheet.py`, `gidi:legacy/blender/roadside_sheet.py`, `gidi:legacy/blender/vehicles_sheet.py`, `gidi:legacy/blender/wear_sheet.py`.
Used elsewhere: `reset` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`; `sky_and_sun` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/generate.py`; `ground` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/city.py`; `camera` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/generate.py`; `render` in `gidi-data:research/google/kits/old-town/tools/part_view.py`, `gidi:legacy/blender/act1_sheet.py`, `gidi:legacy/blender/catalogue.py`, `gidi:legacy/blender/generate.py`

### `gidi:legacy/blender/vehicles_sheet.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/people.py`, `gidi:legacy/blender/gidi_kit/vehicles.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:legacy/blender/wear_sheet.py`
23 defined (21 used, 0 maybe, 2 unused). Imports: `gidi:legacy/blender/gidi_kit/archetypes.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:legacy/blender/gidi_kit/detail.py`, `gidi:legacy/blender/gidi_kit/gutters.py`, `gidi:legacy/blender/gidi_kit/materials.py`, `gidi:legacy/blender/gidi_kit/parts.py`, `gidi:legacy/blender/gidi_kit/roadside.py`, `gidi:legacy/blender/gidi_kit/rules.py`, `gidi:legacy/blender/gidi_kit/wear.py`, `gidi:legacy/blender/scene.py`. Imported by: nothing.

### `gidi:scripts/audit3d.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/autoclean.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`, `gidi:scripts/hand.py`. Imported by: `gidi:scripts/bake_web.py`, `gidi:scripts/hand.py`, `gidi:scripts/hand_fix_checks.py`, `gidi:scripts/rebuild_areas.py`.
Used elsewhere: `R` in `gidi:scripts/bake_web.py`, `gidi:scripts/hand_fix_checks.py`, `gidi:scripts/rebuild_areas.py`; `L` in `gidi:scripts/bake_web.py`; `ring_pts` in `gidi:scripts/hand.py`, `gidi:scripts/hand_fix_checks.py`; `_valid` in `gidi:scripts/hand_fix_checks.py`; `plan` in `gidi:scripts/bake_web.py`, `gidi:scripts/hand_fix_checks.py`; `clean` in `gidi:scripts/bake_web.py`, `gidi:scripts/rebuild_areas.py`; `join` in `gidi:scripts/bake_web.py`, `gidi:scripts/hand.py`, `gidi:scripts/rebuild_areas.py`

### `gidi:scripts/bake_web.py`
87 defined (85 used, 2 maybe, 0 unused). Imports: `gidi:scripts/autoclean.py`, `gidi:scripts/compounds.py`, `gidi:scripts/cross_sections.py`, `gidi:scripts/fronts.py`, `gidi:scripts/furniture.py`, `gidi:scripts/groundpaint.py`, `gidi:scripts/hand.py`, `gidi:scripts/houses.py`, `gidi:scripts/isms.py`, `gidi:scripts/junctions.py`, `gidi:scripts/market_streets.py`, `gidi:scripts/realnames.py`, `gidi:scripts/roadclean.py`, `gidi:scripts/roadends.py`, `gidi:scripts/roadtypes.py`, `gidi:scripts/roadz.py`, `gidi:scripts/surfaces.py`, `gidi:scripts/things.py`, `gidi:scripts/trees.py`, `gidi:scripts/walknet.py`. Imported by: nothing.

### `gidi:scripts/board_server.py`
46 defined (46 used, 0 maybe, 0 unused). Imports: `gidi:scripts/check_map.py`. Imported by: nothing.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/things.py`; `log_message` in `gidi:scripts/code_graph.py`; `do_GET` in `gidi:scripts/code_graph.py`; `do_POST` in `gidi:scripts/code_graph.py`

### `gidi:scripts/build_viewer.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/check_district.py`
36 defined (36 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`, `gidi:scripts/ground.py`, `gidi:scripts/walknet.py`. Imported by: nothing.

### `gidi:scripts/check_map.py`
48 defined (48 used, 0 maybe, 0 unused). Imports: `gidi:scripts/realnames.py`. Imported by: `gidi:scripts/board_server.py`.
Used elsewhere: `ROOT` in `gidi:scripts/board_server.py`; `SCHEMA` in `gidi:scripts/board_server.py`; `ID_RE` in `gidi:scripts/board_server.py`; `errors` in `gidi:scripts/board_server.py`; `parse` in `gidi:scripts/board_server.py`; `anchor` in `gidi:scripts/board_server.py`; `tile_of` in `gidi:scripts/board_server.py`; `canonical` in `gidi:scripts/board_server.py`; `check` in `gidi:scripts/board_server.py`; `args` in `gidi:scripts/board_server.py`; `top` in `gidi:scripts/board_server.py`; `files` in `gidi:scripts/board_server.py`; `recs` in `gidi:scripts/board_server.py`; `by` in `gidi:scripts/board_server.py`

### `gidi:scripts/check_real.py`
11 defined (11 used, 0 maybe, 0 unused). Imports: `gidi:scripts/realnames.py`. Imported by: nothing.

### `gidi:scripts/check_rules.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/child_plan.py`
18 defined (16 used, 2 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/code_graph.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/inventory.py`, `gidi:tests/test_inventory.py`.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `find_ts` in `gidi:tests/test_inventory.py`; `build` in `gidi:scripts/inventory.py`, `gidi:tests/test_inventory.py`; `write` in `gidi:scripts/inventory.py`

### `gidi:scripts/compounds.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `REACH` in `gidi:scripts/bake_web.py`; `compounds` in `gidi:scripts/bake_web.py`

### `gidi:scripts/cross_sections.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/autoclean.py`, `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/design_density.py`, `gidi:scripts/fix_gutters_to_sections.py`, `gidi:scripts/furniture.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/ground.py`, `gidi:scripts/groundpaint.py`, `gidi:scripts/hand_fix_lines.py`, `gidi:scripts/market_streets.py`, `gidi:scripts/roadends.py`, `gidi:scripts/things.py`.
Used elsewhere: `SECTIONS` in `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/design_density.py`, `gidi:scripts/fix_gutters_to_sections.py`; `SECTIONS` in `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/design_density.py`, `gidi:scripts/fix_gutters_to_sections.py`; `MARKET_CLEAR` in `gidi:scripts/ground.py`, `gidi:scripts/market_streets.py`; `half` in `gidi:scripts/check_district.py`, `gidi:scripts/fix_gutters_to_sections.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/ground.py`; `walkway_band` in `gidi:scripts/check_district.py`, `gidi:scripts/furniture.py`, `gidi:scripts/groundpaint.py`, `gidi:scripts/market_streets.py`; `building_line` in `gidi:scripts/autoclean.py`, `gidi:scripts/check_district.py`, `gidi:scripts/design_density.py`, `gidi:scripts/gen_fabric.py`

### `gidi:scripts/deep_check.py`
37 defined (35 used, 2 maybe, 0 unused). Imports: `gidi:scripts/structure.py`. Imported by: nothing.

### `gidi:scripts/deep_prep.py`
18 defined (18 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/deep_profile.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`.
Used elsewhere: `STOREY_BANDS` in `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`; `h_bands` in `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`; `rules` in `gidi:scripts/district_profiles.py`, `gidi:scripts/gen_fabric.py`; `zones` in `gidi:scripts/gen_fabric.py`

### `gidi:scripts/deep_report.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/deep_summary.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/deep_tune.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: `gidi:scripts/district_profiles.py`. Imported by: nothing.

### `gidi:scripts/design_density.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`. Imported by: nothing.

### `gidi:scripts/district_profiles.py`
23 defined (23 used, 0 maybe, 0 unused). Imports: `gidi:scripts/deep_profile.py`. Imported by: `gidi:scripts/deep_tune.py`, `gidi:scripts/gen_fabric.py`.
Used elsewhere: `height_bands` in `gidi:scripts/gen_fabric.py`; `STOREY_BANDS` in `gidi:scripts/gen_fabric.py`; `estate` in `gidi:scripts/gen_fabric.py`; `border` in `gidi:scripts/gen_fabric.py`; `profile` in `gidi:scripts/deep_tune.py`, `gidi:scripts/gen_fabric.py`

### `gidi:scripts/doc_vault.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/inventory.py`.
Used elsewhere: `WORD` in `gidi:scripts/inventory.py`; `build` in `gidi:scripts/inventory.py`; `write` in `gidi:scripts/inventory.py`

### `gidi:scripts/draft_buildings.py`
27 defined (26 used, 1 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/draft_kinds.py`, `gidi:scripts/draft_storeys.py`.
Used elsewhere: `FU` in `gidi:scripts/draft_storeys.py`; `FV` in `gidi:scripts/draft_storeys.py`; `RH` in `gidi:scripts/draft_storeys.py`; `FRONT` in `gidi:scripts/draft_kinds.py`; `WIDTH` in `gidi:scripts/draft_kinds.py`; `footprints` in `gidi:scripts/draft_storeys.py`; `main` in `gidi:scripts/draft_kinds.py`, `gidi:scripts/draft_storeys.py`

### `gidi:scripts/draft_crossings.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/draft_edge.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: `gidi:scripts/draft_roads.py`. Imported by: nothing.

### `gidi:scripts/draft_kinds.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: `gidi:scripts/draft_buildings.py`. Imported by: `gidi:scripts/draft_storeys_nearby.py`.
Used elsewhere: `KIOSK` in `gidi:scripts/draft_storeys_nearby.py`; `main` in `gidi:scripts/draft_storeys_nearby.py`

### `gidi:scripts/draft_looks.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/draft_roads.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/draft_edge.py`.
Used elsewhere: `common` in `gidi:scripts/draft_edge.py`; `fields` in `gidi:scripts/draft_edge.py`; `main` in `gidi:scripts/draft_edge.py`

### `gidi:scripts/draft_storeys.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: `gidi:scripts/draft_buildings.py`. Imported by: nothing.

### `gidi:scripts/draft_storeys_nearby.py`
2 defined (2 used, 0 maybe, 0 unused). Imports: `gidi:scripts/draft_kinds.py`. Imported by: nothing.

### `gidi:scripts/draw_area.py`
33 defined (31 used, 2 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/draw_gen.py`
25 defined (23 used, 2 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/draw_terrain.py`
19 defined (15 used, 4 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/explore_city.py`
40 defined (40 used, 0 maybe, 0 unused). Imports: `gidi:scripts/fabric_metrics.py`, `gidi:scripts/walknet.py`. Imported by: nothing.

### `gidi:scripts/fabric_metrics.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_core.py`, `gidi:scripts/walknet.py`.
Used elsewhere: `lines` in `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/walknet.py`; `extend` in `gidi:scripts/gen_fabric.py`; `noded` in `gidi:scripts/explore_city.py`, `gidi:scripts/gen_fabric.py`, `gidi:scripts/walknet.py`; `measure` in `gidi:scripts/gen_fabric.py`, `gidi:scripts/study_core.py`

### `gidi:scripts/fix_gutters_to_sections.py`
16 defined (15 used, 1 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`. Imported by: nothing.

### `gidi:scripts/frame_footprints.py`
17 defined (15 used, 1 maybe, 1 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:scripts/frame_network.py`
17 defined (16 used, 1 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/frame_study.py`
58 defined (55 used, 1 maybe, 2 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:scripts/freeze_district.py`
11 defined (11 used, 0 maybe, 0 unused). Imports: `gidi:scripts/hand.py`. Imported by: nothing.

### `gidi:scripts/fronts.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `fronts` in `gidi:scripts/bake_web.py`

### `gidi:scripts/furniture.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `furniture` in `gidi:scripts/bake_web.py`

### `gidi:scripts/gen_fabric.py`
498 defined (491 used, 6 maybe, 1 unused). Imports: `gidi:scripts/cross_sections.py`, `gidi:scripts/deep_profile.py`, `gidi:scripts/district_profiles.py`, `gidi:scripts/fabric_metrics.py`, `gidi:scripts/landmarks.py`. Imported by: nothing.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`

### `gidi:scripts/ground.py`
16 defined (15 used, 1 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`. Imported by: `gidi:scripts/check_district.py`, `gidi:scripts/houses.py`, `gidi:scripts/things.py`.
Used elsewhere: `allowed` in `gidi:scripts/check_district.py`, `gidi:scripts/houses.py`, `gidi:scripts/things.py`; `Ground` in `gidi:scripts/check_district.py`, `gidi:scripts/houses.py`, `gidi:scripts/things.py`; `__init__` in `gidi:scripts/things.py`; `rules` in `gidi:scripts/things.py`

### `gidi:scripts/groundpaint.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `_ring` in `gidi:scripts/bake_web.py`; `paint` in `gidi:scripts/bake_web.py`

### `gidi:scripts/hand.py`
39 defined (39 used, 0 maybe, 0 unused). Imports: `gidi:scripts/autoclean.py`. Imported by: `gidi:scripts/autoclean.py`, `gidi:scripts/bake_web.py`, `gidi:scripts/freeze_district.py`, `gidi:scripts/hand_spots/ibudo_real_area.py`, `gidi:scripts/rebuild_areas.py`.
Used elsewhere: `LAYOUT` in `gidi:scripts/bake_web.py`, `gidi:scripts/freeze_district.py`; `MISSES` in `gidi:scripts/bake_web.py`, `gidi:scripts/rebuild_areas.py`; `_D` in `gidi:scripts/rebuild_areas.py`; `_files` in `gidi:scripts/rebuild_areas.py`; `snapshot` in `gidi:scripts/freeze_district.py`; `apply_snapshots` in `gidi:scripts/bake_web.py`; `districts_frozen` in `gidi:scripts/bake_web.py`; `_drop_building` in `gidi:scripts/autoclean.py`; `apply_frozen` in `gidi:scripts/bake_web.py`; `_clear_area` in `gidi:scripts/hand_spots/ibudo_real_area.py`; `apply_road_edits` in `gidi:scripts/bake_web.py`, `gidi:scripts/rebuild_areas.py`; `apply_label_edits` in `gidi:scripts/bake_web.py`; `apply_paint_edits` in `gidi:scripts/bake_web.py`; `apply_house_edits` in `gidi:scripts/bake_web.py`; `apply_thing_edits` in `gidi:scripts/bake_web.py`; `apply_late_furniture` in `gidi:scripts/bake_web.py`; `apply_detail_edits` in `gidi:scripts/bake_web.py`; `apply_wall_edits` in `gidi:scripts/bake_web.py`; `apply_edits` in `gidi:scripts/bake_web.py`, `gidi:scripts/rebuild_areas.py`

### `gidi:scripts/hand_fix_checks.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: `gidi:scripts/autoclean.py`. Imported by: nothing.

### `gidi:scripts/hand_fix_lines.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`. Imported by: nothing.

### `gidi:scripts/hand_links.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/hand_spots/ibudo_real_area.py`
90 defined (90 used, 0 maybe, 0 unused). Imports: `gidi:scripts/hand.py`. Imported by: nothing.

### `gidi:scripts/hand_spots/ibudo_spot1.py`
20 defined (19 used, 0 maybe, 1 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/houses.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: `gidi:scripts/ground.py`, `gidi:scripts/things.py`. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `houses` in `gidi:scripts/bake_web.py`; `place` in `gidi:scripts/bake_web.py`

### `gidi:scripts/inventory.py`
18 defined (18 used, 0 maybe, 0 unused). Imports: `gidi:scripts/code_graph.py`, `gidi:scripts/doc_vault.py`. Imported by: nothing.

### `gidi:scripts/isms.py`
36 defined (36 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `gutters` in `gidi:scripts/bake_web.py`; `apply_edits` in `gidi:scripts/bake_web.py`; `run` in `gidi:scripts/bake_web.py`; `src` in `gidi:scripts/bake_web.py`

### `gidi:scripts/js_symbols.mjs`
8 defined (8 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/junctions.py`
11 defined (9 used, 1 maybe, 1 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `junctions` in `gidi:scripts/bake_web.py`

### `gidi:scripts/landmarks.py`
13 defined (13 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/gen_fabric.py`.
Used elsewhere: `rect` in `gidi:scripts/gen_fabric.py`; `direction_at` in `gidi:scripts/gen_fabric.py`; `pts` in `gidi:scripts/gen_fabric.py`; `build_interchange` in `gidi:scripts/gen_fabric.py`; `skywalks` in `gidi:scripts/gen_fabric.py`; `place_reserved` in `gidi:scripts/gen_fabric.py`; `u_road` in `gidi:scripts/gen_fabric.py`; `back_road` in `gidi:scripts/gen_fabric.py`; `ring_road` in `gidi:scripts/gen_fabric.py`; `stands` in `gidi:scripts/gen_fabric.py`; `stall_rows` in `gidi:scripts/gen_fabric.py`

### `gidi:scripts/layout_v2.py`
61 defined (58 used, 3 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/map02.py`
16 defined (14 used, 1 maybe, 1 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/market_streets.py`
5 defined (5 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `REACH` in `gidi:scripts/bake_web.py`; `market_streets` in `gidi:scripts/bake_web.py`

### `gidi:scripts/real_underlay.py`
8 defined (8 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/realnames.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`, `gidi:scripts/check_map.py`, `gidi:scripts/check_real.py`.
Used elsewhere: `PICS` in `gidi:scripts/check_real.py`; `core` in `gidi:scripts/bake_web.py`, `gidi:scripts/check_map.py`, `gidi:scripts/check_real.py`; `cores` in `gidi:scripts/check_map.py`, `gidi:scripts/check_real.py`; `rename` in `gidi:scripts/bake_web.py`; `c` in `gidi:scripts/bake_web.py`, `gidi:scripts/check_map.py`

### `gidi:scripts/rebuild_areas.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: `gidi:scripts/autoclean.py`, `gidi:scripts/hand.py`, `gidi:scripts/walknet.py`. Imported by: nothing.

### `gidi:scripts/rename_mains.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/roadclean.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `clean` in `gidi:scripts/bake_web.py`

### `gidi:scripts/roadends.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `road_ends` in `gidi:scripts/bake_web.py`

### `gidi:scripts/roadtypes.py`
10 defined (10 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `types` in `gidi:scripts/bake_web.py`

### `gidi:scripts/roadz.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `heights` in `gidi:scripts/bake_web.py`

### `gidi:scripts/structure.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/deep_check.py`, `gidi:scripts/study_deep.py`, `gidi:scripts/study_structure.py`.
Used elsewhere: `measure` in `gidi:scripts/deep_check.py`, `gidi:scripts/study_deep.py`, `gidi:scripts/study_structure.py`

### `gidi:scripts/study_analyse.py`
139 defined (136 used, 2 maybe, 1 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/study_boxheights.py`
11 defined (11 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/study_connect.py`
29 defined (29 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/study_core.py`
20 defined (20 used, 0 maybe, 0 unused). Imports: `gidi:scripts/fabric_metrics.py`. Imported by: nothing.

### `gidi:scripts/study_deep.py`
175 defined (174 used, 1 maybe, 0 unused). Imports: `gidi:scripts/structure.py`. Imported by: nothing.

### `gidi:scripts/study_extract.py`
20 defined (20 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `way` in `gidi:scripts/realnames.py`; `node` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_paint.py`, `gidi-game:Content/Python/gidi_plates.py`, `gidi-game:Content/Python/gidi_surfaces.py`

### `gidi:scripts/study_google.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/study_isms.py`
68 defined (67 used, 1 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/study_landmarks.py`
45 defined (45 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/study_structure.py`
41 defined (41 used, 0 maybe, 0 unused). Imports: `gidi:scripts/structure.py`. Imported by: nothing.

### `gidi:scripts/study_undermapped.py`
12 defined (11 used, 1 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/study_village.py`
18 defined (16 used, 2 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/study_wellmapped.py`
25 defined (24 used, 1 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/surfaces.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `KINDS` in `gidi:scripts/bake_web.py`; `surfaces` in `gidi:scripts/bake_web.py`

### `gidi:scripts/terrain.py`
39 defined (34 used, 4 maybe, 1 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/things.py`
41 defined (41 used, 0 maybe, 0 unused). Imports: `gidi:scripts/cross_sections.py`, `gidi:scripts/ground.py`. Imported by: `gidi:scripts/bake_web.py`, `gidi:scripts/houses.py`.
Used elsewhere: `CHARACTER` in `gidi:scripts/houses.py`; `Rng` in `gidi:scripts/houses.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `pick` in `gidi:scripts/houses.py`; `chance` in `gidi:scripts/houses.py`; `between` in `gidi:scripts/houses.py`; `condition` in `gidi:scripts/houses.py`; `cent` in `gidi:scripts/houses.py`; `things` in `gidi:scripts/bake_web.py`, `gidi:scripts/houses.py`; `place` in `gidi:scripts/bake_web.py`

### `gidi:scripts/trees.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/bake_web.py`.
Used elsewhere: `trees` in `gidi:scripts/bake_web.py`

### `gidi:scripts/twin_photos.py`
14 defined (14 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/twins.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/walknet.py`
8 defined (8 used, 0 maybe, 0 unused). Imports: `gidi:scripts/fabric_metrics.py`. Imported by: `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/rebuild_areas.py`.
Used elsewhere: `ways_of` in `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/rebuild_areas.py`; `ban_zone` in `gidi:scripts/explore_city.py`; `graph` in `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/explore_city.py`, `gidi:scripts/rebuild_areas.py`; `Reach` in `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/rebuild_areas.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:legacy/blender/gidi_kit/core.py`, `gidi:scripts/board_server.py`; `attach` in `gidi:scripts/bake_web.py`, `gidi:scripts/explore_city.py`; `from_points` in `gidi:scripts/bake_web.py`, `gidi:scripts/check_district.py`, `gidi:scripts/rebuild_areas.py`; `to_point` in `gidi:scripts/check_district.py`, `gidi:scripts/rebuild_areas.py`

### `gidi:scripts/whats_here.py`
22 defined (22 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:tests/test_inventory.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: `gidi:scripts/code_graph.py`. Imported by: nothing.

### `gidi:web/app.js`
32 defined (32 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:web/board.html#87`
0 defined (0 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:web/board.js`
114 defined (112 used, 0 maybe, 2 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `$` in `gidi:web/faceedit.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `css` in `gidi:web/faceedit.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `dist` in `gidi:web/mapedit.js`; `segDist` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `nearestOnSeg` in `gidi:web/mapedit.js`; `lineDist` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `inPoly` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `centroid` in `gidi:web/mapedit.js`; `segsCross` in `gidi:web/mapedit.js`; `polysOverlap` in `gidi:web/mapedit.js`; `f` in `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `bboxOf` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `districtAt` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `thingPts` in `gidi:web/mapedit.js`; `toW` in `gidi:web/frame.js`; `resize` in `gidi:web/faceedit.js`, `gidi:web/frame.js`; `fit` in `gidi:web/faceedit.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `saveView` in `gidi:web/frame.js`; `viewBB` in `gidi:web/frame.js`; `hit` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `KIND_FILL` in `gidi:web/mapedit.js`; `SURF` in `gidi:web/mapedit.js`; `path` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `draw` in `gidi:web/faceedit.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `outline` in `gidi:web/mapedit.js`; `box` in `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `drawScale` in `gidi:web/frame.js`; `editPts` in `gidi:web/mapedit.js`; `handleAt` in `gidi:web/mapedit.js`; `rectFrom` in `gidi:web/mapedit.js`

### `gidi:web/faceedit.js`
38 defined (38 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `$` in `gidi:web/board.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `esc` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `clone` in `gidi:web/mapedit.js`; `r2` in `gidi:web/mapedit.js`; `fp` in `gidi:web/mapedit.js`; `height` in `gidi:web/board.js`, `gidi:web/frame.js`; `items` in `gidi:web/mapedit.js`; `num` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `commit` in `gidi:web/board.js`; `fit` in `gidi:web/board.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `toS` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `draw` in `gidi:web/board.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `css` in `gidi:web/board.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `input` in `gidi:web/board.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `setTool` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `close` in `gidi:web/board.js`, `gidi:web/frame.js`, `gidi:web/mapedit.js`; `open` in `gidi:web/mapedit.js`

### `gidi:web/frame.js`
25 defined (25 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `$` in `gidi:web/board.js`, `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `css` in `gidi:web/board.js`, `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `bboxOf` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `hit` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `inPoly` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `segDist` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `lineDist` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `districtAt` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `toW` in `gidi:web/board.js`; `resize` in `gidi:web/board.js`, `gidi:web/faceedit.js`; `fit` in `gidi:web/board.js`, `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `saveView` in `gidi:web/board.js`; `viewFromHash` in `gidi:web/board.js`; `viewBB` in `gidi:web/board.js`; `path` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `draw` in `gidi:web/board.js`, `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `text` in `gidi:web/faceedit.js`; `drawScale` in `gidi:web/board.js`; `where` in `gidi:web/board.js`, `gidi:web/mapedit.js`; `focus` in `gidi:web/mapedit.js`

### `gidi:web/mapedit.js`
177 defined (177 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `$` in `gidi:web/board.js`, `gidi:web/faceedit.js`, `gidi:web/frame.js`; `css` in `gidi:web/board.js`, `gidi:web/faceedit.js`, `gidi:web/frame.js`; `esc` in `gidi:web/board.js`, `gidi:web/faceedit.js`; `clone` in `gidi:web/faceedit.js`; `r2` in `gidi:web/faceedit.js`; `dist` in `gidi:web/board.js`; `nearestOnSeg` in `gidi:web/board.js`; `segDist` in `gidi:web/board.js`, `gidi:web/frame.js`; `lineDist` in `gidi:web/board.js`, `gidi:web/frame.js`; `inPoly` in `gidi:web/board.js`, `gidi:web/frame.js`; `centroid` in `gidi:web/board.js`; `bboxOf` in `gidi:web/board.js`, `gidi:web/frame.js`; `hit` in `gidi:web/board.js`, `gidi:web/frame.js`; `segsCross` in `gidi:web/board.js`; `o` in `gidi:web/board.js`, `gidi:web/faceedit.js`; `polysOverlap` in `gidi:web/board.js`; `rectFrom` in `gidi:web/board.js`; `editPts` in `gidi:web/board.js`; `c` in `gidi:web/board.js`, `gidi:web/faceedit.js`, `gidi:web/frame.js`; `z` in `gidi:web/board.js`, `gidi:web/faceedit.js`; `rec` in `gidi:web/faceedit.js`; `recsOf` in `gidi:web/faceedit.js`; `newId` in `gidi:web/faceedit.js`; `save` in `gidi:web/board.js`, `gidi:web/faceedit.js`; `del` in `gidi:web/board.js`; `undo` in `gidi:web/board.js`, `gidi:web/faceedit.js`; `start` in `gidi:web/board.js`, `gidi:web/faceedit.js`, `gidi:web/frame.js`; `KINDS` in `gidi:web/board.js`; `setTool` in `gidi:web/board.js`, `gidi:web/faceedit.js`; `thingPts` in `gidi:web/board.js`

### `gidi:web/view3d.js`
39 defined (39 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

