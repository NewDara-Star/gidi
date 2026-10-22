# The new map's data format (draft 0.1, for the owner to approve)

The new map is the one ground truth (decisions, 22 Oct: "everything that we do must be in map data. Every single thing").
The drawing board saves into it. The Blender kit and the Unreal import read it. Nothing else holds the city.

This is a draft. No board or kit code reads it yet.

- **Schema:** `schema/map_schema.json` (every record type, field, type, unit and allowed value).
- **Checker:** `scripts/check_map.py` (rejects anything unknown, missing, mistyped, unlinked or real-named).
- **What the kit reads:** `schema/kit_reads.json` (each kit part and the fields it reads).
- **Worked example:** `docs/map-format-example/d15/` (one 20 m street; passes the checker).

## In short

- The map is a folder of plain JSON files: one folder per district, one **plan** file per district and **dress** files in 100 m tiles.
- The **plan layer** is what you draw on the board: roads, plots, frontages, walls, building footprints and storeys, lean-tos, stalls, poles, trees, parked vehicles, places.
- The **dress layer** is the detail on top: every window, door, stain, roof sheet, wall bay, gutter slab, sack, litter piece, poster, person spot, painted ground patch and bump. Each dress record hangs off one plan record.
- Every record has a stable id, a type and only the fields the schema allows. Positions are Gidi metres in the 1:3 frame.
- The kit throws no dice. A field that is absent means "this thing has none", never "the kit picks".
- Many small things (sacks, litter, slabs, windows) are stored as **rows of a table** inside one record, every value written out. That keeps the files about half the size and still explicit.

## 1. Where the data lives

### Folders and files

```
map/
  d15/                      one folder per district (d01 to d51, the study's numbers)
    district.json           the district record: its Gidi name and outline
    plan.json               the plan layer: every plan record in the district
    dress/
      128_60.json           the dress layer, one file per 100 m tile
      128_61.json           (file name = floor(x / 100) _ floor(y / 100))
```

- `map/` sits at the repo root. The board server already serves the whole repo, so the board can read it.
- **One plan file per district.** A dense core district is about 6 to 7 MB at full detail (section 5). That loads in well under a second and diffs record by record.
- **Dress files per 100 m tile.** A dense tile is about 1 to 3 MB. The board, the kit and Unreal load only the tiles they need.
- **A dress record lives in its parent's tile:** the tile of the parent's first point (first footprint point, first centreline point, or `at`). The checker enforces it. Records with no parent (free ground patches, relief grids, people) go in the tile of their own first point.
- **Roads are cut at district lines.** Each road piece lives in one district. Pieces join by sharing an end point exactly (district seams stay hand-joined).

### File layout

Every file is one JSON object:

```json
{"format":"gidi-map/0.1","district":"d15","layer":"dress","tile":[128,60],"records":[
{"id":"b-2pv33692","type":"building", ...},
{"id":"fc-9j6pk5sj","type":"faces", ...}
]}
```

- One record a line, sorted by id. The board writes exactly this. `check_map.py --fix` rewrites a file into it.
- So a git diff shows the records that changed, line by line, and two people editing different records never clash.
- `tile` appears only in dress files.

### Coordinates and units

| What | Rule |
|---|---|
| Frame | Gidi metres in the 1:3 frame, as the board's new frame draws it: x east 0 to 27,000, y **south** 0 to 10,500, z up. (0, 0) is the frame's north-west corner. |
| Lengths | metres, written to 0.01 (a centimetre). No unit suffixes in names: the unit comes from the schema. |
| Heights `z` | metres above the ground under the thing (flat ground plus any relief grid there). Road points may carry a third number: an absolute height, for bridges and ramps. |
| Angles | degrees. `turn` is 0 = facing east (+x), 90 = facing south (+y): clockwise on the board. |
| Colours | `"#rrggbb"`, lower case. |
| Shares, wear, `shade` | 0 to 1; `shade` is a multiplier on a colour (1 = as given). |
| Along a face | `u` = metres along the face from its start corner; `z` = metres up. |
| Footprints and rings | points in order, the first not repeated at the end. Walking from point i to point i+1, the building is on your left on the board. **Face i** is the wall from point i to point i+1. |
| Local frames | goods and hung items sit in their parent's frame: for a lean-to, x along the wall from `u0`, y out from the wall, z above its stand; for a stall, from its `at`, turned by its `turn`. Move the parent and they go with it. |

**Readers:** Unreal is also x forward, y right, z up (left-handed), so Gidi metres go in as they are, times 100 for centimetres, and `turn` is the yaw. Blender flips y (y_blender = -y, turn_blender = -turn).

### Stable ids

- Every record has an `id`: a short type prefix, a dash and 8 random letters and digits, like `b-2pv33692` (a building) or `gd-xvzchtts` (goods).
- Random, not counted, so two accounts adding records on two branches never pick the same id.
- An id never changes: not when the record moves, is edited, or crosses into another tile or district (the file changes, the id does not). A deleted id is never reused.
- District records are the one exception: `d01` to `d51`, the study's numbers (EARTH-CHECK.md).
- Rows inside a table (a sack, a slab, a window) have no id of their own. They are addressed as the record id plus the row number. Nothing links to a single sack, so this costs nothing.

### References to the real place

Every record may carry a `ref`:

```json
"ref": {"twin": "tw-c041", "shots": ["ot175", "ot91"], "kit": "old-town"}
```

| Field | Meaning |
|---|---|
| `twin` | an id in the twin catalogue **outside the repo** (proposed: `~/Real-world/research/twins/index.tsv`: id, real name, real coordinates, notes). The map never holds the real name or coordinates. |
| `shots` | Street View shot ids (`ot175`), never file names (file names carry real street names). |
| `kit` | the kit the thing is modelled from. |

`ref` is history and reference only. No kit part reads it.

### Gidi's own names

- `name` on a district, road or place; `text` on a sign, a wall daub or a gate number.
- The checker compares each one with real names (the same core-word test as the old bake's N1: `docs/hand/realnames.txt`, plus the 819 real places of the new frame when `web/frame-study.js` is present). A clash fails.
- Names are optional on roads and places. A district must have one.

## 2. Record types

Common fields on every record:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `id` | text | yes | the stable id |
| `type` | text | yes | the record type (tables below) |
| `ref` | object | no | reference to the real place (above) |
| `from` | object | no | where a stamp was copied from (section 3) |
| `note` | text | no | a note for people |

**Absent means none.** An optional field left out means the thing does not have it (no fascia, no tarp), never "let the kit decide". Lists and tables are always present, even when empty.

The tables below give each field's meaning. `schema/map_schema.json` holds the exact list of allowed values. `?` marks an optional field.

### Plan layer

#### district (`d15`, in `district.json`)
| Field | Type, units | Example |
|---|---|---|
| `n` | integer, the study's number | `15` |
| `name` | Gidi name | `"Ìgbẹ́kẹ̀lé"` |
| `outline` | list of rings | `[[[12800,6050],[12880,6050],[12880,6120],[12800,6120]]]` |

#### road (`rd-`): roads, streets, lanes and paths
| Field | Type, units | Example |
|---|---|---|
| `kind` | `motorway`, `trunk`, `main_road`, `local_main`, `market_street`, `home_street`, `lane`, `path`, `ramp` | `"home_street"` |
| `name`? | Gidi name | `"Ìrètí Close"` |
| `centreline` | line of [x, y] or [x, y, z] points, m | `[[12830,6088],[12850,6088]]` |
| `width` | m, kerb to kerb (or edge to edge) | `5.2` |
| `surface` | `tar_new`, `tar_worn`, `sand`, `earth`, `laterite`, `interlock`, `concrete`, `plank` | `"tar_worn"` |
| `sand_cover` | `none`, `edges`, `full` | `"edges"` |
| `kerb_left`, `kerb_right` | `none`, `drain_wall`, `painted_bw`, `raised_pavement` | `"drain_wall"` |
| `median` | `none`, `low_concrete`, `jersey` | `"none"` |
| `crown` | m, how much the middle stands above the edges | `0.06` |
| `ground_look` | per layer (`earth`, `dust`, `tar`, `mud`): `colour` and photo `surface` | `{"tar":{"colour":"#4f3b2f","surface":"worn_asphalt"}}` |
| `gutters` | list: `side`, `s0`, `s1` (m along the centreline), `kind` (`open_concrete`, `open_earth`, `slab_covered`, `centre_channel`), `width`, `depth`, `offset` (m from the centreline), `state` (`clear`, `half_blocked`, `water`), `slab_colour`?, `wall_colour`? | `{"side":"left","s0":0,"s1":20,"kind":"slab_covered","width":0.5,"depth":0.45,"offset":3.0,"state":"half_blocked"}` |
| `verges` | list: `side`, `s0`, `s1`, `surface` (`earth`, `concrete_apron`, `sand`, `grass`, `interlock`, `laterite`), `width` | `{"side":"right","s0":0,"s1":20,"surface":"earth","width":1.8}` |
| `crossings` | list: `side`, `s`, `w`, `kind` (`slab_bridge`, `plank_bridge`, `gate_ramp`) | `{"side":"left","s":6.2,"w":1.4,"kind":"slab_bridge"}` |

`left` and `right` are as you walk from the first centreline point to the last, seen on the board. `s` is metres along the centreline from its first point. Two roads join by sharing a point exactly; an end within 1 m of another road but not on it fails the check.

#### plot (`pl-`)
| Field | Type | Example |
|---|---|---|
| `kind` | `house`, `compound`, `shop_row`, `market`, `motor_park`, `church_ground`, `mosque_ground`, `school_ground`, `open_ground`, `under_build`, `yard`, `car_park` | `"shop_row"` |
| `outline` | ring | `[[12831,6083.5],[12841,6083.5],[12841,6074],[12831,6074]]` |
| `place`? | id of a place | `"pc-8bpeyfvg"` |

#### frontage (`fr-`): one side of a plot that faces a street
| Field | Type, units | Example |
|---|---|---|
| `plot`, `road` | ids | |
| `side` | which side of the road | `"left"` |
| `kind` | `shop_line_step`, `leanto_to_road`, `wall_gate`, `platform_house`, `low_wall_bars`, `sheet_fence`, `breeze_fence`, `plank_fence`, `open_forecourt` | `"wall_gate"` |
| `line` | line, m: the wall or shop line (bends allowed) | `[[12831,6092.6],[12850,6092.6]]` |
| `setback` | m from the road edge | `0` |
| `platform`? | `h` (m), `steps`, `front` (m, how far it reaches toward the road), `colour` | `{"h":0.3,"steps":1,"front":1.2,"colour":"#7a7268"}` |
| `wall`? | the wall object (below) | |

**The wall object** (on a frontage, or on a free `wall` record): `h`, `finish` (`render`, `bare_block`, `breeze_block`, `sheet`, `plank`), `colour`, `painted`, `state` (`clean`, `mouldy`), `piers` (`none`, `at_gate`, `every_bay`), `top` (`none`, `razor_wire`, `steel_rail`, `broken_glass`), `surface`?, `gates`: list of `u0`, `u1` (m along the line), `h`, `kind` (`sheet_steel`, `bar`, `plank`), `colour`, `leaves`, `wicket`, `number`? (text), `wear`, `surface`?.

#### wall (`wl-`): a side or back wall not on a street
`plot`?, `line`, `wall` (the wall object above).

#### building (`b-`)
| Field | Type, units | Example |
|---|---|---|
| `plot`? | id | |
| `kind` | `face_me_bungalow`, `walkup`, `shop_under_flats`, `market_block`, `compound_house`, `church`, `mosque`, `school`, `colonial_house`, `kiosk_row`, `shack`, `shed`, `under_build` | `"shop_under_flats"` |
| `footprint` | ring (any outline: L-shapes, wings) | `[[12831,6083.5],[12841,6083.5],[12841,6075],[12831,6075]]` |
| `storeys` | 1 to 12 | `2` |
| `storey_h` | m, one per storey (their sum is the eaves height) | `[3.1, 2.9]` |
| `ground_floor` | `home`, `lock_ups`, `open_stalls`, `workshop`, `arcade`, `cage_stalls` | `"lock_ups"` |
| `roof` | `form` (`hip`, `gable`, `mono`, `flat`), `material` (`zinc`, `longspan`, `tile`, `slab`), `state` (`rusty`, `silver`, `painted`, `new`), `colour`, `pitch` (deg), `eave` (m), `ridge_face`?, `parapet_h`?, `fascia`? (`kind`, `colour`, `h`), `edge`? (`colour`, `h`), `posts`?, `post_foot`?, `surface`? | `{"form":"hip","material":"zinc","state":"rusty","colour":"#7c5c4b","pitch":14,"eave":0.9}` |
| `finish` | `kind` (`render`, `bare_block`, `tile_brick`, `tile_stone`, `tile_pattern`, `plaster_moulded`), `colour`, `trim_colour`?, `side_colour`?, `storey_bands`?, `base_band`? (`colour`, `h`), `surface`? | `{"kind":"render","colour":"#c9b48a","base_band":{"colour":"#7d6f5a","h":0.9}}` |
| `windows` | the building's window look: `kind`, `shutter_colour`?, `bars` (`none`, `vertical`, `grid`, `diamond`, `sunray`, `scroll`), `bar_colour`? | `{"kind":"louvre_glass","bars":"vertical","bar_colour":"#262626"}` |
| `outside_stair` | `none`, `front_concrete`, `front_steel`, `spiral` | `"none"` |
| `wear` | 0 to 1 | `0.7` |
| `place`?, `use`? | the place it belongs to; game uses (not drawn) | `["buy","eat"]` |

#### leanto (`lt-`)
| Field | Type, units | Example |
|---|---|---|
| `against` | id of a building, frontage or wall | |
| `face`? | the building face it leans on (needed when against a building) | `0` |
| `u0`, `u1` | m along that face or line | `0.8`, `6.2` |
| `depth`, `z_wall`, `z_front`, `stand_z` | m | `1.8`, `3.0`, `2.2`, `0.25` |
| `sheet` | `material` (`zinc`, `longspan`, `tarp`, `plank`), `colour`, `state`, `edge_colour`?, `surface`? | |
| `posts` | `none`, `timber`, `steel` | `"timber"` |

#### stall (`st-`): tables, kiosks, umbrellas, carts, fridges
`kind` (`plank_stall`, `table`, `kiosk`, `cage_stall`, `cart`, `umbrella`, `drinks_fridge`, `display_cabinet`, `container_shop`, `rack`), `at`, `turn`, `w`, `d`, `h`, `colour`, `tarp`? (`colour`, `z`, `drop`), `umbrella`? (`r`, `colours`), `place`?.

#### heap (`hp-`)
`kind` (`sand`, `gravel`, `rubbish`, `scrap`, `goods`, `tyres`), `at`, `r`, `h`, `tarp_colour`?. Goods on a heap are a `goods` record.

#### pole (`po-`), wire (`wi-`), mast (`ms-`)
- pole: `kind` (`timber`, `concrete`, `steel`), `at`, `h`, `lean` ([x, y] degrees), `transformer`, `lamp` (`none`, `steel_arm`, `solar`), `arm`, `wear`.
- wire: `from_pole`, then exactly one of `to_pole` or `to_at` ([x, y, z], e.g. a point on a wall), `n` (wires in the run), `sag` (m).
- mast: `kind` (`lattice`, `monopole`), `at`, `h`, `colour`.

#### tree (`tr-`)
`kind` (`palm`, `shade`, `plantain`, `almond`, `neem`, `shrub`), `at`, `h`, `lean`, `form`: a table of `fronds` (turn, droop, len) for a palm, or `lobes` (x, y, z, r) for a broad tree.

#### vehicle (`vh-`): a parked spot
`kind` (`danfo`, `keke`, `okada`, `saloon`, `suv`, `pickup`, `lorry`, `container`, `tanker`, `bus`, `wreck`), `at`, `turn`, `colour`, `cab_colour`?, `lean`?, `tractor`?, `load`? (`kind`: `none`, `roll`, `cargo`, `sacks`; `colour`?), `cover`? (a car cover's colour).

#### furniture (`fu-`)
`kind` (`bench`, `chair`, `stool`, `generator`, `bin`, `water_tank`, `drum`, `tyre_stack`, `gas_rack`, `speaker`, `tank_stand`), `at`, `z`, `turn`, `colour`, `length`?.

#### place (`pc-`): what the game uses a spot for
| Field | Type | Example |
|---|---|---|
| `kind` | `market`, `motor_park`, `bus_stop`, `church`, `mosque`, `school`, `clinic`, `betting`, `bar`, `buka`, `police`, `fuel`, `bank`, `chemist`, `park`, `garage`, `workshop_yard`, `story` | `"buka"` |
| `name`? | Gidi name | `"Mama Àdùkẹ́ Kitchen"` |
| `area` | rings | |
| `uses` | game uses: `buy`, `sell`, `eat`, `drink`, `pray`, `bet`, `pick_up`, `drop_off`, `load`, `unload`, `money`, `rest`, `sleep`, `hide`, `fix_vehicle`, `fuel`, `heal`, `learn`, `story` | `["eat","buy","rest"]` |
| `hours`? | text | `"07-21"` |

A place is not drawn. It is what the item register and the game read. Buildings, plots and stalls point to it with `place`.

### Dress layer

Each dress record has `of`: the plan record it dresses.

#### faces (`fc-`), of a building
`blotch` (six phases of the paint blotch) and `faces`: one entry per face that has anything on it. A face with no entry has nothing on it.

| Face field | Shape | Columns or fields |
|---|---|---|
| `face` | integer | the footprint edge |
| `windows` | table | `u`, `z` (sill), `w`, `h`, `kind`, `open` (0 to 1) |
| `doors` | table | `u`, `w`, `h`, `kind` (`plank`, `steel`, `panel`, `open_dark`, `curtain`), `colour` |
| `shopfronts` | list | `u0`, `u1`, `door` (`plank_shutter`, `roll_up`, `open_dark`, `glass`, `grille`), `colour`, `open`, `planks`? (table: `shade`, `offset`) |
| `balconies` | list | `u0`, `u1`, `storey`, `depth`, `solid_h`, `rail`, `pattern` (`loops`, `pickets`, `solid`), `colour`, `posts` |
| `screens` | list | breeze-block screens: `u0`, `u1`, `out`, `kind`, `colour`, `h`, `cells` (one shade per cell) |
| `stains` | table | `kind` (`streak`, `patch`, `block`, `ac`), `u`, `z`, `w`, `h`, `tint` (`grime`, `rust`, `mould`, `cement`, `damp`), `dark`, `taper` |
| `addons` | table | `kind` (`ac`, `dish`, `water_tank`, `speaker`, `mast`, `meter`, `lamp`, `house_number`, `rebar_stubs`), `u`, `z`, `colour`, `size`, `shade` |
| `signs` | list | `u0`, `u1`, `z0`, `z1`, `bg`, `fg`, `text` |
| `awnings` | table | `u0`, `u1`, `z`, `depth`, `colour` |

A table is written `{"cols": [...], "rows": [[...], ...]}`; the columns must be exactly the schema's, in order. Example window row: `[1.6, 4.0, 1.2, 1.2, "louvre_glass", 0.6]`.

#### roof_sheets (`rs-`), of a building or lean-to
`sag`, `slopes` (each: `face`, `rows`, `ph` (three phases), `sheets` table: `tone` (`main`, `second`, `new`), `shade`, `wear`, `nails` (per row, how rusted each nail line is), `edge` (per row)), `uprights` table (`u`, `lean`, `shade`) for a mono roof's or lean-to's posts.

#### wall_bays (`wb-`), of a frontage or wall
`bays` (each 1.2 m bay: `u`, `w`, `blot`, `patch`, `streaks` table (`u`, `w`, `z_top`, `len`, `dark`), `foot` (damp foot), `broken`? (`u`, `z`, `w`, `h`, `shades`)), `chips` table (`u`, `size`), `daubs` table (`u`, `z`, `text`, `colour`, `size`).

#### posters (`ps-`), of a frontage, wall, pole, stall or building
`face`? and `items`: each `u`, `z`, `w`, `h`, `turn`? (round a pole), `colours`, `torn`, `shade`.

#### gutter_pieces (`gp-`), of a road
`side` and `pieces`: each `s0`, `s1`, `wall_wear`, `water_z`, `mix` (`mud`, `sand`, `water`, `rubbish`), `caught` (litter table), `slabs` table (`tip`, `roll`, `sink`, `dirt`, `dust`, `shade`, `gap`, `broken`; the number of rows is the number of slabs), `joints` table (`slab`, `o`, `w`, `d`, `h`, `du`, `turn`: dirt and weeds in the joints).

#### ground (`gr-`): a painted patch of ground
`of`? (a road or plot), `kind` (`tar`, `earth`, `laterite`, `sand`, `dust`, `mud`, `wet`, `water`, `concrete`, `interlock`, `grass`, `rubble`), `rings`, `order` (later paints over earlier), `z`? (a water level), `lip`? (how proud tar patches stand), `colour`?, `surface`?. Sand, mud and puddles are painted areas, never scatters.

#### relief (`rl-`): bumps and dips
`origin` ([x, y]), `cell` (m), `cols`, `rows`, `z_mm` (cols x rows whole millimetres, row by row). Ground with no relief grid is flat: that is a value, not a guess.

#### ground_marks (`gm-`), of a road or plot
`potholes` table (`x`, `y`, `r`, `depth`, `stretch`, `turn`, `mud`) and `ruts` (each `line`, `w`, `depth`, `mud`, `packed`).

#### litter (`li-`)
`of`? and `pieces` table: `kind` (`sachet`, `bag`, `bottle`, `pack`, `can`, `husk`, `paper`, `rag`, `tyre`), `colour`, `x`, `y`, `z`, `turn`, `tilt`, `w`, `d`, `h`. World positions.

#### goods (`gd-`), of a lean-to, stall, heap or furniture (a bin)
`items` and `hung` tables: `kind` (`sack`, `nylon_bag`, `crate`, `plastic`, `cloth`, `carton`, `bale`, `basin`, `bowl`, `bottle`, `tyre`, `timber`, `part`, `food`, `cabinet`), `colour`, `x`, `y`, `z`, `turn`, `w`, `d`, `h`, `shade`. In the parent's frame.

**One record per item, or a group?** A group: one `goods` record per lean-to (or stall or heap) holding one row per item, every value written. A stamped band of 90 sacks is 90 rows, never "90 sacks here". Separate records with ids would double the size and nothing ever needs to link to one sack.

#### people (`pp-`)
`of`? (a place, road or plot) and `spots` table: `x`, `y`, `z`, `turn`, `h`, `pose` (`stand`, `walk`, `sit`, `squat`, `lean`, `carry`), `look` (an id in the people kit, when it exists).

### KIT.md §12 fields: where each one went

Fields that **became records** (they were knobs for the kit's dice; the dice are gone):

| KIT.md field | Now |
|---|---|
| `goods_kinds`, `goods_fill`, `goods_depth_m`, `goods_tarp`, `goods_tone`, `goods_dust`, `hanging_kinds`, `hanging_fill`, table `items`, `goods`, `goods_colours` | rows of a `goods` record (`items`, `hung`) |
| street `litter` (`per_m2`, `walls`, `ruts`, `from_x`, `to_x`), `gutter_*.litter` | rows of a `litter` record; `caught` rows in gutter pieces |
| `relief` (`amp_m`, `scale_m`, `off_road`), `ground_grid` (the drafted `.npz`: `relief`, `fray`, `tar`, `rut_wob`, `rut_k`) | `relief` grids (whole millimetres) for the bumps; `ground` patches for where tar shows and how its edge frays; `ruts` lines for the ruts' wander |
| `tar_cover`, `tar_patch_m`, `dust_in_low`, `far_dust`, `edge_rut`, `tar_lip_m`, `puddles`, `tar_strips`, `sand_edges` | `ground` patches (with `lip`, `z`) and `ground_marks` |
| `gutter_*.wear`, `dust`, `open_share`, `broken`, `rock` | per-slab rows in `gutter_pieces` |
| `wall_finish.stains`, `wall.render_broken`, `wall.blotch`, `wall.mould_streaks`, `wall.foot_stain_m` | `stains` rows; `wall_bays` |
| `ac_units` (share) | `addons` rows of kind `ac` |
| `window_spots` | `windows` rows per face |
| `stalls_in_road` | `stall` records |

Fields **renamed** (the second name is the alias to drop):

| Keep | Drop |
|---|---|
| `kind` | `type` (as a sub-kind), `house_type`, `street_type`, `frontage_edge`, `car_kind`, `kiosk_kind`, `k` |
| `colour` | `col`, `wall_colour`, `sheet_colour`, `rail_colour` (inside its own object) |
| `turn` (degrees) | `heading_deg`, `facing_deg`, `rz` (radians), `at[3]` |
| `width`, `depth`, `h`, `r` (metres by the schema) | `width_m`, `depth_m`, `h_m`, `w_m`, `eave_depth_m`, `fascia_h_m`, `base_band_h`, `goods_depth_m` |
| `storey_h` (one per storey) | `wall_h_m` |
| `roof.form` + `roof.material` | `roof.type` (`hip_zinc`...) |
| `roof.state`, `sheet.state` | `roof_state` |
| `roof.pitch`, `roof.eave` | `pitch_deg`, `eave_depth_m` |
| `finish` | `wall_finish` |
| `ground_floor` | `ground_floor_use` |
| `u0`, `u1` along a face or line; `s0`, `s1`, `s` along a road | `from_x`, `to_x`, `x0`, `x1`, `upto_x`, `x` (in the spot's street frame) |
| `centreline` | `line` for roads (other lines keep `line`) |
| `stand_z` | `stand_z_m`, `z_m`, `post_foot_m` → `post_foot` |
| `lean` | `lean_deg` |
| `kerb_left`, `kerb_right` | `kerb.left`, `kerb.right` |
| `gutters` (list with `side`) | `gutter_left`, `gutter_right` |
| `verges` (list with `side`) | `verge_left`, `verge_right` |
| `ground_look` | `ground_colours` + `surfaces` |
| `balconies` per face (`u0`, `u1`, `storey`) | `balcony.runs` (`a`, `b`, `out`) |
| `screens` per face | `ground_floor_front.runs` |
| `awnings` rows per face (`u0`, `u1` on the face) | `awnings[]` (`x0`, `x1`, `y`, `out` north or south) |
| `posters` record | `wall.posters[]`, `pole_posters[]`, `side_posters[]` |
| `furniture` kind `bin` with its `goods`/`litter` | `bins[]` |
| `vehicle` | `parked_vehicles[]` |
| `wall.top` | `wall_top` |
| `platform` object | `platform_height_m`, `platform_steps`, `platform_front_y`, `platform_colour` |

**Not map fields** (as KIT.md says): the test camera, sun and sky (`shot`). They stay in the kit test.

**Still to add** (seen, no field yet): `scaffold` (face: `u0`, `u1`, `out`, `h`, `colour`, `tubes`, `boards` tables); `wall_dishes` (as `addons` of kind `dish`: done); a car cover (`vehicle.cover`: done); police livery, a timber stall rack (`stall` kind `rack`: done), a tarp over a roof, corrugated sheet doors. Each gets its field before the kit draws it.

## 3. Stamps

A stamp copies a full record, or a group of them, from a studied spot (or another part of the map) and then you edit it.

- **What is stored:** always the full values, with new ids. Never "copy of", never a live link. Change the source later and the stamp does not change.
- **`from` note**, optional, for history only. No kit part reads it.

```json
"from": {"spot": "ot175", "record": "L1", "date": "2026-10-22", "note": "stamped from the long bungalow, then shortened to 8.7 m"}
```

- **From a test spot to the map:** a test spot's frame is x along its street and y to the left. The stamp tool places the spot's origin O and street heading t on the map, and every point becomes P = O + x·(cos t, sin t) + y·(sin t, -cos t) in Gidi metres (y south). Face positions (`u`, `z`) and local goods frames need no change.
- **A group stamp** (a whole lean-to with its sheets and goods, a building with its faces and roof) keeps the links inside the group: the new `goods` record points at the new lean-to's id.
- The draft desk (`blender/kit_draft.py`) can still write a test spot's first records. After that the records are the map's, edited by hand.

## 4. Validation

```
~/.venvs/gidi/bin/python scripts/check_map.py docs/map-format-example --kit schema/kit_reads.json
PASS  30 records in 3 files, 0 problems
```

`scripts/check_map.py` reads `schema/map_schema.json` and fails on:

- an unknown record type, an unknown field (no guessing, no stray keys), a missing required field;
- a wrong type, a value outside its range, a value not in its list (`"car"` is not a vehicle kind: `saloon`, `suv` or `pickup`);
- a table whose columns are not exactly the schema's, or a row of the wrong length;
- an id in the wrong form, used twice, or a link to a record that is not there or of the wrong type;
- a ring that crosses itself; a footprint that runs the wrong way; `storey_h` not one per storey; a relief grid with the wrong number of values;
- a window, door, stain, shopfront or lean-to off its face (`u` past the face's length, `z` above the building);
- a dress record not in its parent's tile or district; a plan record outside its district;
- a road end within 1 m of another road but not on it;
- a name or sign text that shares its core with a real name;
- a file not in the canonical layout (`--fix` rewrites it).

Tested both ways: the example passes; a broken copy (an extra field, a missing field, a real road name, an unknown vehicle kind, a wire with both ends, a renamed table column, a link to nothing, a lean-to longer than its wall, two roads 0.36 m apart) fails with 13 problems named.

### What each kit part reads

`schema/kit_reads.json` lists each kit part, the record type it draws and the fields it reads (`roof.form`, `faces[].windows`). With `--kit`, the checker fails if:

- a part reads a field the schema does not have (**a part with no field fails**: add the field to the map first);
- a record type the kit draws has no part;
- a drawn field has no part reading it (a field the kit ignores is a gap in the interface).

Fields that are not drawn are listed once in the schema (`not_drawn`: `id`, `ref`, `from`, `note`, `name`, `use`, `uses`, `place`, `plot`, `hours`).

Today the list is kept by hand. When the kit moves to the new map, each builder declares what it reads beside its code:

```python
@reads('building', 'kind', 'footprint', 'storeys', 'storey_h', 'roof', 'finish', 'windows', 'wear')
def building(b, collection=None): ...
```

The registry collects these and writes `kit_reads.json`, so the check always matches the code. The kit's `need()` (MissingRecord) stays as the last guard, but a map that passes `check_map.py` never trips it.

`decisions/CHECKS.md`: this is the start of the check for "The map tells the kit what goes where" and "One ground truth". They stay GAP until the kit reads the new map.

## 5. Size

### Measured

From the example and from the two test spots after kit-test-1 turned them into records (22 Oct, night), re-encoded in this format (values to 0.01, small things as table rows):

| What | Size in this format |
|---|---|
| One table row (a window, stain, slab, sack, litter piece, roof sheet) | 34 to 49 bytes |
| One wall bay | about 140 bytes |
| One relief value (0.5 m grid) | about 3 bytes |
| A plan building record | about 0.7 KB; with its plot and frontage about 1.3 KB |
| Test spot ot175: 9 buildings, 155 m of street, 4 lean-to rows | 332 KB (raw draft 816 KB); buildings 1 to 78 KB, about 19 KB each on average |
| Test spot ot91 (Balogun walk-ups): 10 buildings | 382 KB; about 35 KB a building (one walk-up has 993 stains) |
| Street detail (ot175: gutter slabs, litter, marks) | about 360 bytes a metre |
| Compressed (what git stores) | 5 to 6 times smaller |

Rounding to centimetres and writing small things as rows halves the drafted test maps; the drafted files carry 17-digit numbers.

### One central-core district at full detail

Mushin's Gidi district (d15) is 1.19 km² in the frame. Houses stay real size, so it holds about **4,000 buildings** and **20 km of street** (the study: 3,300 to 3,700 buildings and 17 to 18 km of street per km² in the dense core).

| Part | Count | Size |
|---|---|---|
| Plan: buildings, plots, frontages | 4,000 x 1.3 KB | 5 MB |
| Plan: roads, poles, wires, parked vehicles, stalls | 20 km x 60 B/m | 1.2 MB |
| **Plan layer** | about 20,000 records | **about 6.5 MB** (1.2 MB in git) |
| Dress: faces, roof sheets, wall bays | 4,000 x 25 KB | 100 MB |
| Dress: gutters, litter, ground, goods, people | 20 km x 660 B/m | 13 MB |
| Dress: relief over open ground and streets | 0.7 km² x 12 B/m² | 8 MB |
| **Dress layer** | about 3 million rows in about 15,000 records | **about 120 MB** in 119 tiles, 1 MB a tile on average, up to 3 MB (about 22 MB in git) |

### The whole city

The frame holds about 3 million real roofs; at 1:3 the land is a ninth, so Gidi has about **330,000 buildings** and about **2,300 km of street**. Sprawl houses are simpler (about 15 KB of dress each).

| Layer | Raw | In git (compressed) |
|---|---|---|
| Plan | about 0.6 GB | about 110 MB |
| Dress | about 7 to 8 GB | about 1.4 GB, before history |

### Can git and the board carry it?

- **Board: yes.** It loads one district's plan (about 6.5 MB) and only the dress tiles in view when zoomed in (a few MB). Never the whole city at once.
- **Git, plan layer: yes**, for the whole city.
- **Git, dress layer: one district yes, the whole city no.** 7 to 8 GB of files and 1.4 GB packed (more with history) is past what a GitHub repo should hold, and every account would clone it.

### The split

- **Plan layer** (`plan.json`: roads, plots, frontages, walls, footprints, storeys, roofs' form, lean-tos, stalls, poles, trees, vehicles, places) and **dress layer** (`dress/` tiles: faces, roof sheets, wall bays, gutters, ground, relief, litter, goods, posters, people). Both are hand data. Both are the one ground truth.
- The dress layer starts in this repo at `map/<district>/dress/`.
- When it passes 1 GB on disk (about eight dense districts), it moves to its own repo (`gidi-map-dress`) with the same paths, cloned beside this one. The board, the kit and Unreal read both. Nothing else changes.

## 6. How the board edits it, and how the kit and Unreal read it

### The board

The board stops writing an edit log. Today it appends "add building at (x, y)" operations to `web/hand/<d>.json`, applied to a generated base and found again by position. The new map has no base: the files are the state, and git is the history. The board saves whole records by id.

`scripts/board_server.py` keeps what works (local only on 127.0.0.1, one write at a time, atomic save, finite numbers only, undo) and gets two new calls for the new frame:

- `POST /api/map/save {record}`: checks the record against the schema, writes it into the right file (district, layer, tile) in the canonical layout, replacing the record with that id. A bad record is refused with the checker's message.
- `POST /api/map/delete {id}`: removes it, and refuses while other records still point at it.

| Old board tool or op | New record |
|---|---|
| Select: move, turn, reshape, delete | any record, same id |
| Building (drag a box); `set house`, `set storeys` | `building` (+ `plot`), its `kind`, `storeys`, `storey_h` |
| Street; `reshape street`, `cut street`, `name road` | `road` (ends snap to another road's point) |
| Surface | `road.surface`; ground paint for patches |
| Wall, `cut wall`; Gate | `wall` or `frontage.wall`; `wall.gates` |
| `set front` | `frontage.kind` |
| Tree | `tree` |
| Furniture: pole, street light, transformer | `pole` (`lamp`, `transformer`) |
| Furniture: kiosk, stalls; `add thing` | `stall`, `furniture`, `heap` |
| Furniture: hawkers, parking boy, agbero | `people` spots |
| Furniture: task force truck | `vehicle` |
| `add place`, `move place` | `place` |
| `add paint` | `ground` |
| `add parcel`, `reshape parcel` | `plot` |

New tools the board needs:

1. **Plot** and **Frontage** (pick a plot edge and its road).
2. **Face editor:** one face drawn flat (u across, z up): windows, doors, shopfronts, balconies, screens, stains, add-ons, signs, awnings.
3. **Lean-to** (pick a face and a stretch), **Stall**, **Heap**, **Pole and wire**, **Vehicle**, **Person spot**.
4. **Goods:** place items in a lean-to's or stall's frame, one by one or by stamp.
5. **Ground paint** (patches by kind) and **Relief** (raise and lower grid cells).
6. **Litter** (place pieces).
7. **Stamp:** pick a record or group from a studied spot or the map, place it, get new ids and a `from` note.
8. **Check:** every save runs the record through the schema; a button runs the whole checker on the district.

Roof sheets, wall bays and gutter slabs are numerous and fiddly. At first they come by stamp or the draft desk and are edited as rows in a table panel; a drawing tool for them can come later.

### The kit (Blender)

- Reads `map/<district>/plan.json` and the dress tiles for the area it builds.
- One part per record type (`kit_reads.json`); each part draws only what its records say.
- A kit test spot becomes a box on the map plus its camera; the test reads that box from the map, not its own `map.json`.

### The Unreal import

- The importer in `~/gidi-game` reads the same files. Gidi metres times 100 are Unreal centimetres; x and y go in as they are; `turn` is the yaw.
- It imports tile by tile, so 100 m tiles line up with the world's streaming cells.
- As already decided (17 Oct): it rebuilds from the map every time, and nothing it makes is committed.

## 7. Open questions for the owner

1. **Brushes.** May the board have brushes that write many records in one stroke (a litter brush, a relief brush, a goods band)? Everything they write is stored in full and editable, but where each piece lands is picked by the brush, not placed by your hand. The other way is stamps only: copy studied spots and move pieces by hand.
2. **Small things as table rows.** Sacks, litter pieces, slabs, windows and stains are rows inside one record each (every value written out), not records with their own ids. It halves the size. All right?
3. **The dress layer's own repo.** At full detail the whole city's dress is 7 to 8 GB. All right to move it to its own repo once it passes 1 GB?
4. **District names.** Each district record needs a Gidi name. Name the 51 now (working names), or as each district is built?

## Next steps (not in this PR)

- The owner's answers, then the format becomes `gidi-map/1.0` and a rule in `DECISIONS.md`.
- A real-names list for the whole new frame (every street name in the frame, outside the repo), so the name check covers it.
- The twin catalogue outside the repo, with ids.
- The board's save calls and the first tools (Plot, Building, Road, Frontage) on the new frame.
- The kit reads the new map: a converter for the two test spots, then `@reads` on each part.
