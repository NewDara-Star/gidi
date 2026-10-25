# Code map

Made by `scripts/inventory.py` with `scripts/code_graph.py`: every function, class, method and top-level constant in gidi, gidi-game and gidi-data, read by the parsers (JavaScript read by the TypeScript compiler at /Users/Star/stride-web/node_modules/typescript). 3735 pieces of code in 136 files: 8 used nowhere, 68 used only by name where their file is not imported (a hint: a call by string, or dead). "Imported by" is Python imports; a page's scripts share its names. A file run as a script (by a shell line, Blender, the board) shows in INVENTORY.md's "Refs", not here.

## Used nowhere (by file)

- `gidi-data:research/google/kits/old-town/tests/facade_hand.py`: `sh_` (const, line 197)
- `gidi-game:tools/map_build.py`: `BUILDER` (const, line 45)
- `gidi-game:tools/plates.py`: `PLATE` (const, line 28)
- `gidi:docs/lagos-study/roads/scripts/common.py`: `C250` (const, line 13), `lga_shapes` (function, line 24)
- `gidi:scripts/frame_footprints.py`: `NJ` (const, line 35)
- `gidi:scripts/frame_study.py`: `group_poly` (function, line 254), `inD` (const, line 266)

## Every code file

### `gidi-data:research/data/results/heights.py`
8 defined (8 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/data/results/landpop.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tests/facade_hand.py`
54 defined (53 used, 0 maybe, 1 unused). Imports: none of ours. Imported by: nothing.

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
46 defined (44 used, 2 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-data:research/google/kits/old-town/tools/sheet.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:Content/Python/gidi_heroes.py`
17 defined (17 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_paint.py`, `gidi-game:Content/Python/gidi_plates.py`. Imported by: `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `HERE` in `gidi-game:Content/Python/gidi_underdeck.py`; `DEST` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `STATE` in `gidi-game:Content/Python/gidi_underdeck.py`; `HERO_V` in `gidi-game:Content/Python/gidi_underdeck.py`; `HEROES` in `gidi-game:Content/Python/gidi_underdeck.py`; `_is_paint` in `gidi-game:Content/Python/gidi_underdeck.py`; `say` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `_master` in `gidi-game:Content/Python/gidi_street.py`; `_sig` in `gidi-game:Content/Python/gidi_underdeck.py`; `_import` in `gidi-game:Content/Python/gidi_underdeck.py`; `load` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`

### `gidi-game:Content/Python/gidi_look.py`
3 defined (3 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `environment` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `apply` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`

### `gidi-game:Content/Python/gidi_modes.py`
9 defined (9 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `people_levels` in `gidi-game:Content/Python/gidi_underdeck.py`; `open_clean` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `save_play` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `scene_count` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`

### `gidi-game:Content/Python/gidi_paint.py`
7 defined (7 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_surfaces.py`. Imported by: `gidi-game:Content/Python/gidi_heroes.py`.
Used elsewhere: `MASTER` in `gidi-game:Content/Python/gidi_heroes.py`; `MASTER_V` in `gidi-game:Content/Python/gidi_heroes.py`; `WEAR` in `gidi-game:Content/Python/gidi_heroes.py`; `say` in `gidi-game:Content/Python/gidi_heroes.py`; `master` in `gidi-game:Content/Python/gidi_heroes.py`; `instance` in `gidi-game:Content/Python/gidi_heroes.py`

### `gidi-game:Content/Python/gidi_plates.py`
18 defined (18 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `HERE` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `ART` in `gidi-game:Content/Python/gidi_heroes.py`; `DEST` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `MASTER` in `gidi-game:Content/Python/gidi_heroes.py`; `MASTER_V` in `gidi-game:Content/Python/gidi_heroes.py`; `SPEC` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `say` in `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `number_for` in `gidi-game:Content/Python/gidi_underdeck.py`; `data_for` in `gidi-game:Content/Python/gidi_underdeck.py`; `_master` in `gidi-game:Content/Python/gidi_heroes.py`; `instances` in `gidi-game:Content/Python/gidi_heroes.py`

### `gidi-game:Content/Python/gidi_scan_export.py`
6 defined (6 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:Content/Python/gidi_street.py`
21 defined (21 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:Content/Python/gidi_surfaces.py`. Imported by: nothing.

### `gidi-game:Content/Python/gidi_surfaces.py`
33 defined (33 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:Content/Python/gidi_paint.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`.
Used elsewhere: `HERE` in `gidi-game:Content/Python/gidi_underdeck.py`; `JUNK` in `gidi-game:Content/Python/gidi_underdeck.py`; `_scan` in `gidi-game:Content/Python/gidi_paint.py`; `say` in `gidi-game:Content/Python/gidi_paint.py`, `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `textures` in `gidi-game:Content/Python/gidi_paint.py`; `_master` in `gidi-game:Content/Python/gidi_street.py`; `masters` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`; `slot_kind` in `gidi-game:Content/Python/gidi_underdeck.py`; `pipeline` in `gidi-game:Content/Python/gidi_street.py`, `gidi-game:Content/Python/gidi_underdeck.py`

### `gidi-game:Content/Python/gidi_underdeck.py`
25 defined (25 used, 0 maybe, 0 unused). Imports: `gidi-game:Content/Python/gidi_heroes.py`, `gidi-game:Content/Python/gidi_look.py`, `gidi-game:Content/Python/gidi_modes.py`, `gidi-game:Content/Python/gidi_plates.py`, `gidi-game:Content/Python/gidi_surfaces.py`. Imported by: nothing.

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
Used elsewhere: `SIDE` in `gidi-game:tools/font_plate.py`; `Flat` in `gidi-game:tools/font_brush.py`, `gidi-game:tools/font_plate.py`, `gidi-game:tools/font_punct.py`, `gidi-game:tools/lettering.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi:scripts/board_server.py`; `main` in `gidi-game:tools/font_brush.py`, `gidi-game:tools/font_plate.py`, `gidi-game:tools/font_punct.py`

### `gidi-game:tools/font_specimen.py`
3 defined (3 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/frame_motorpark.py`
70 defined (70 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/furniture_build.py`
46 defined (46 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/goods_kit.py`, `gidi-game:tools/vehicle_kit.py`. Imported by: nothing.

### `gidi-game:tools/goods_kit.py`
34 defined (34 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/vehicle_kit.py`. Imported by: `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`.
Used elsewhere: `PHI` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `rgb` in `gidi-game:tools/stall_build.py`; `Goods` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:scripts/board_server.py`; `m` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `bm` in `gidi-game:tools/stall_build.py`; `box` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `cyl` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `ring` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/stall_build.py`; `done` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`; `build` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`; `materials` in `gidi-game:tools/furniture_build.py`, `gidi-game:tools/loose_build.py`, `gidi-game:tools/stall_build.py`; `litter` in `gidi-game:tools/loose_build.py`

### `gidi-game:tools/img_diff.py`
12 defined (12 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi-game:tools/junction_build.py`
28 defined (28 used, 0 maybe, 0 unused). Imports: `gidi-game:tools/fields.py`, `gidi-game:tools/road_build.py`. Imported by: nothing.

### `gidi-game:tools/junction_geo.py`
43 defined (43 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`.
Used elsewhere: `T_WALL` in `gidi-game:tools/road_build.py`; `add` in `gidi-game:tools/map_build.py`; `left` in `gidi-game:tools/road_build.py`; `length` in `gidi-game:tools/road_build.py`; `at` in `gidi-game:tools/map_build.py`; `edge` in `gidi-game:tools/road_build.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:scripts/board_server.py`; `side` in `gidi-game:tools/road_build.py`; `out` in `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`; `groups` in `gidi-game:tools/map_build.py`; `junction` in `gidi-game:tools/map_build.py`; `nodes` in `gidi-game:tools/map_build.py`; `pieces` in `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`; `clear_of` in `gidi-game:tools/map_build.py`; `recipe` in `gidi-game:tools/map_build.py`; `d` in `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`; `roads` in `gidi-game:tools/map_build.py`; `P` in `gidi-game:tools/road_build.py`; `j` in `gidi-game:tools/map_build.py`, `gidi-game:tools/road_build.py`; `gs` in `gidi-game:tools/road_build.py`

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
Used elsewhere: `A` in `gidi-game:tools/junction_build.py`; `FIELDS` in `gidi-game:tools/junction_build.py`; `HW` in `gidi-game:tools/junction_build.py`; `SURF` in `gidi-game:tools/junction_build.py`; `T_WALL` in `gidi-game:tools/junction_build.py`; `KERB` in `gidi-game:tools/junction_build.py`; `SAND_C` in `gidi-game:tools/junction_build.py`; `EARTH` in `gidi-game:tools/junction_build.py`; `SILT_WET` in `gidi-game:tools/junction_build.py`; `SILT_CRUST` in `gidi-game:tools/junction_build.py`; `WATER` in `gidi-game:tools/junction_build.py`; `lerp3` in `gidi-game:tools/junction_build.py`; `n3` in `gidi-game:tools/junction_build.py`; `smooth` in `gidi-game:tools/junction_build.py`; `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:scripts/board_server.py`; `vert` in `gidi-game:tools/junction_build.py`; `face` in `gidi-game:tools/junction_build.py`; `part` in `gidi-game:tools/junction_build.py`; `grid` in `gidi-game:tools/junction_build.py`; `fsplit` in `gidi-game:tools/junction_build.py`; `frange` in `gidi-game:tools/junction_build.py`; `rows` in `gidi-game:tools/junction_build.py`; `road_z` in `gidi-game:tools/junction_build.py`; `road_colour` in `gidi-game:tools/junction_build.py`; `slot_of` in `gidi-game:tools/junction_build.py`; `runs` in `gidi-game:tools/junction_build.py`; `silt_z` in `gidi-game:tools/junction_build.py`; `water_z` in `gidi-game:tools/junction_build.py`; `wall_colour` in `gidi-game:tools/junction_build.py`; `make_objects` in `gidi-game:tools/junction_build.py`

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
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:scripts/board_server.py`

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
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:scripts/board_server.py`

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
89 defined (85 used, 4 maybe, 0 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`, `gidi:docs/lagos-study/roads/scripts/gaz.py`. Imported by: nothing.

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

### `gidi:scripts/board_server.py`
38 defined (38 used, 0 maybe, 0 unused). Imports: `gidi:scripts/check_map.py`. Imported by: nothing.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`; `log_message` in `gidi:scripts/code_graph.py`; `do_GET` in `gidi:scripts/code_graph.py`; `do_POST` in `gidi:scripts/code_graph.py`

### `gidi:scripts/check_map.py`
48 defined (48 used, 0 maybe, 0 unused). Imports: `gidi:scripts/realnames.py`. Imported by: `gidi:scripts/board_server.py`.
Used elsewhere: `ROOT` in `gidi:scripts/board_server.py`; `SCHEMA` in `gidi:scripts/board_server.py`; `ID_RE` in `gidi:scripts/board_server.py`; `errors` in `gidi:scripts/board_server.py`; `parse` in `gidi:scripts/board_server.py`; `anchor` in `gidi:scripts/board_server.py`; `tile_of` in `gidi:scripts/board_server.py`; `canonical` in `gidi:scripts/board_server.py`; `check` in `gidi:scripts/board_server.py`; `args` in `gidi:scripts/board_server.py`; `top` in `gidi:scripts/board_server.py`; `files` in `gidi:scripts/board_server.py`; `recs` in `gidi:scripts/board_server.py`; `by` in `gidi:scripts/board_server.py`

### `gidi:scripts/check_rules.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/code_graph.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/inventory.py`, `gidi:tests/test_inventory.py`.
Used elsewhere: `__init__` in `gidi-game:tools/fields.py`, `gidi-game:tools/font_space.py`, `gidi:scripts/board_server.py`; `find_ts` in `gidi:tests/test_inventory.py`; `build` in `gidi:scripts/inventory.py`, `gidi:tests/test_inventory.py`; `write` in `gidi:scripts/inventory.py`

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

### `gidi:scripts/frame_footprints.py`
17 defined (15 used, 1 maybe, 1 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:scripts/frame_study.py`
58 defined (55 used, 1 maybe, 2 unused). Imports: `gidi:docs/lagos-study/roads/scripts/common.py`. Imported by: nothing.

### `gidi:scripts/inventory.py`
18 defined (18 used, 0 maybe, 0 unused). Imports: `gidi:scripts/code_graph.py`, `gidi:scripts/doc_vault.py`. Imported by: nothing.

### `gidi:scripts/js_symbols.mjs`
8 defined (8 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:scripts/realnames.py`
4 defined (4 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: `gidi:scripts/check_map.py`.
Used elsewhere: `core` in `gidi:scripts/check_map.py`; `cores` in `gidi:scripts/check_map.py`

### `gidi:scripts/study_boxheights.py`
11 defined (11 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.

### `gidi:tests/test_inventory.py`
15 defined (15 used, 0 maybe, 0 unused). Imports: `gidi:scripts/code_graph.py`. Imported by: nothing.

### `gidi:web/faceedit.js`
38 defined (38 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `$` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `esc` in `gidi:web/mapedit.js`; `clone` in `gidi:web/mapedit.js`; `r2` in `gidi:web/mapedit.js`; `fp` in `gidi:web/mapedit.js`; `height` in `gidi:web/frame.js`; `items` in `gidi:web/mapedit.js`; `num` in `gidi:web/mapedit.js`; `fit` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `toS` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `draw` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `css` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `input` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `setTool` in `gidi:web/mapedit.js`; `close` in `gidi:web/frame.js`, `gidi:web/mapedit.js`; `open` in `gidi:web/mapedit.js`

### `gidi:web/frame.js`
25 defined (25 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `$` in `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `css` in `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `bboxOf` in `gidi:web/mapedit.js`; `hit` in `gidi:web/mapedit.js`; `inPoly` in `gidi:web/mapedit.js`; `segDist` in `gidi:web/mapedit.js`; `lineDist` in `gidi:web/mapedit.js`; `districtAt` in `gidi:web/mapedit.js`; `resize` in `gidi:web/faceedit.js`; `fit` in `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `path` in `gidi:web/mapedit.js`; `draw` in `gidi:web/faceedit.js`, `gidi:web/mapedit.js`; `text` in `gidi:web/faceedit.js`; `where` in `gidi:web/mapedit.js`; `focus` in `gidi:web/mapedit.js`

### `gidi:web/mapedit.js`
177 defined (177 used, 0 maybe, 0 unused). Imports: none of ours. Imported by: nothing.
Used elsewhere: `$` in `gidi:web/faceedit.js`, `gidi:web/frame.js`; `css` in `gidi:web/faceedit.js`, `gidi:web/frame.js`; `esc` in `gidi:web/faceedit.js`; `clone` in `gidi:web/faceedit.js`; `r2` in `gidi:web/faceedit.js`; `segDist` in `gidi:web/frame.js`; `lineDist` in `gidi:web/frame.js`; `inPoly` in `gidi:web/frame.js`; `bboxOf` in `gidi:web/frame.js`; `hit` in `gidi:web/frame.js`; `o` in `gidi:web/faceedit.js`; `c` in `gidi:web/faceedit.js`, `gidi:web/frame.js`; `z` in `gidi:web/faceedit.js`; `rec` in `gidi:web/faceedit.js`; `recsOf` in `gidi:web/faceedit.js`; `newId` in `gidi:web/faceedit.js`; `save` in `gidi:web/faceedit.js`; `undo` in `gidi:web/faceedit.js`; `start` in `gidi:web/faceedit.js`, `gidi:web/frame.js`; `setTool` in `gidi:web/faceedit.js`; `get` in `gidi:web/faceedit.js`, `gidi:web/frame.js`; `ring` in `gidi:web/frame.js`; `at` in `gidi:web/frame.js`; `h` in `gidi:web/faceedit.js`, `gidi:web/frame.js`; `on` in `gidi:web/faceedit.js`; `key` in `gidi:web/faceedit.js`, `gidi:web/frame.js`; `down` in `gidi:web/frame.js`; `move` in `gidi:web/frame.js`; `up` in `gidi:web/frame.js`; `path` in `gidi:web/frame.js`

