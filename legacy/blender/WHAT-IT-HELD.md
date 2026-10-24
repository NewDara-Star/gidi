# The old Blender kit: what it held, and what the builders can take from it

The owner (24 Oct): "we took a lot of time to build stuff in the old Blender kit... can we see what we need in the old
Blender kit, so we see what we need to remodel". This page answers that. The kit is frozen (DECISIONS, "The interface
works both ways; the builders are the kit"): nothing here is extended. A builder in `gidi-game/tools/*_build.py` is made
fresh, whole and clean, from real pictures; what it can take from here is the **knowledge** (what Lagos has, the sizes,
the parts, the fields a record needs), never the mesh.

`gidi_kit/` is about 12,000 lines, with 437 public functions in 29 modules. Its renders are in `out/` on this Mac (not
committed): `kinds-sheet*.jpg`, `new_kit*.jpg`, `vehicles*.jpg`, `monuments.jpg`, `roadside.jpg`, `lights.jpg`,
`the_reach.jpg`, `showcase.jpg`, and one picture per kind in `out/kinds/`. Most of it reads as toys (the owner, 23 Oct):
boxes with window grids, flat colours, no wear and no clutter. That is because most of it was made 13-16 Oct to fill a
generated city fast, before the look target and the kit tests.

Two layers, of very different worth:
- **The city kit (13-19 Oct):** `archetypes`, `kinds`, `places`, `blocks`, `parts`, `rules`, `registry`, `landmarks`,
  `monuments`, `parcels`, `structures`, `roadside`, `street`, `gutters`, `vehicles`, `people`, `boats`, `props`, `materials`,
  `detail`, `core`. 76 kinds of building, about 30 kinds of ground, some 35 vehicles, 19 monuments and 20 structures, built by
  seeded rules. Low detail. Its worth is the
  **list**: every kind of Lagos thing the old map needed, each with its research note.
- **The old town kit (22-23 Oct):** `oldtown`, `facade`, `goods`, `roadbed`, `zinc`, `wear`, `textured`, `draft`, and
  `kit_test.py`, `kit_draft.py`. Built for the five eye tests (ot175, ot91, ot149, ot73, ot45) from Street View, driven
  by records, with the field lists in KIT.md section 12. Its worth is the **fields and the methods**: these are the
  closest thing to the builders and were never ported.

## What the new map needs now, and where the old kit already worked it out

`gidi-game/tools/kit_fields.py` lists the map's record types that no builder draws yet. For each, the old kit's file
that holds the know-how:

| Record type no builder draws | Old kit know-how | What to take |
|---|---|---|
| `road`, `relief`, `ground`, `ground_marks` | `roadbed.py` (the street as real ground: crown, relief grid, sandy edges, ruts), `street.py` (road conditions from fresh tar to rutted mud, potholes holding water, markings, kerbs, bumps), `draft.ground_grids` | the ground's fields and how they shape the sheet; the six road conditions |
| `frontage`, `wall_bays` | `oldtown.frontage`, `oldtown.plain_wall`, `oldtown.breeze_screen`, `draft.plain_wall_bays`, `draft.frontage` | how a frontage fills (bays, breeze blocks, posters, marks) |
| `leanto` | `oldtown.leanto`, `oldtown.leanto_frame`, `draft.leanto` | the frame, sheet roof, posts, what hangs from the front plate |
| `roof_sheets` | `zinc.py` (sheet by sheet: each its own brown or grey, rust at the eave, the odd new sheet, laps, sag, stones holding them down) | the whole method; it matched the Google roofs |
| `gutter_pieces` | `gutters.py` (the U-channel, silt and green water, blocked stretches, plank and slab crossings), `street.drain` | sizes and states |
| `heap` | `street.refuse_heap`, `draft.refuse_heap`, `oldtown.sand_heap`, `goods.py` | heap shapes; goods already have `goods_kit.py` |
| `tree` | `parcels.tree`, `draft.tree` (ball trees: the eye tests failed them; a real tree needs a fresh start, check Fab first) | only placement fields |
| `mast` | `oldtown.lattice_mast`, `oldtown.mono_frame` | parts list |
| `rail`, `station` | `structures.rail`, `places.station`, `vehicles` (diesel loco, coach, wagon) | gauge, ballast, platform parts |

## What already has a builder (the builder is better; nothing to take)

| Old kit | Builder now |
|---|---|
| `vehicles.danfo`, `brt`, `keke`, `molue`, `container_truck`, `police_pickup` | `danfo_build`, `brt_build`, `keke_build`, `molue_build`, `lorry_build`, `pickup_build` |
| `parts.walls`, `window`, `door`, `balcony`, `roller_shutter`, `facade.*`, `archetypes.house` (the storey building) | `block_build` |
| `street.pole`, `wire`, `transformer` | `pole_build` |
| `parts.compound_wall`, `oldtown.sheet_gate` | `wall_build` |
| `archetypes.stall`, `oldtown.plank_stall`, `cage_stall`, `glass_cabinet`, `display_cabinet`, `drinks_fridge` | `stall_build` |
| `goods.py` | `goods_kit.py`, `loose_build` |
| `props.*` (chairs, benches, drums, jerrycans, basins, umbrellas, tables, generator) | `furniture_build`, `umbrella_build`, `props_build` |
| `people.py` (box people) | `person_build` (MakeHuman), City Sample |
| `wear.py`, `materials.py` (wear in vertex colours) | `wear_layer.py` |

## Still only in the old kit: the list of what to build later

Each is a builder to make when the map first needs it, from real pictures, the way the danfo was. Order: what the
first districts (Mùṣá and its neighbours) will hold first.

1. **Small buildings of the street:** kiosk, lock-up (open and shut), container shop, face-me-I-face-you, buka, lean-to
   extension, unfinished house (rebar up for the next floor), gatehouse, water tank stand (`archetypes`, `kinds`).
2. **Street furniture that makes a road read:** street lights (a share dead), traffic lights, direction signs and
   gantries, speed discs, police kiosk, warden post, bus shelter (`roadside`, `places.bus_shelter`).
3. **Vehicles not built yet:** okada (with rider, passenger, load), korope, saloon cars (City Sample first), tipper,
   tanker, water tanker, cement mixer, refuse compactor, fire engine, ambulance, task force truck, push cart and
   wheelbarrow (`vehicles`).
4. **Places with their own shape:** mosque (domes, minarets), church, school, clinic and hospital, police and fire
   station, fuel station, bank branch, chemist, betting shop, motor park, market sheds, warehouse and works, bakery,
   print shop, phone mall, plaza, hotel, nightclub, flats, villa, mansion, office and bank towers (`places`,
   `parcels`, `blocks`). The old ones are boxes; their research notes and colours are what to take.
5. **City-scale structures:** flyover and its ramps and service road, skywalk, footbridges, jetties, the expressway
   with Jersey barriers, the long lagoon bridge, the cable bridge, canals and culverts, boardwalks, estate walls and
   gates (`structures`; deck clearances in `docs/OLD-MAP-LESSONS.md`).
6. **The water:** ferry, water bus, outboard canoe, dredger, stilt houses, rafts, fishing huts, smoke racks
   (`boats`, `kinds`).
7. **Grounds:** pitch, court, pool, golf course, stadium bowl, airfield, tank farm, landfill, prison, barracks, pond
   (`parcels`).
8. **Monuments** (placed by hand; Meshy may design the sculptural ones, model and cost first): The Reach (the owner's
   own artwork), statues on roundabouts, clock tower, lighthouse, welcome arches, LED boards, billboards, murals
   (`monuments`, `landmarks`). Parked until their districts are drawn.

## How to use this page

When a builder is made, read the old function named here for its list of parts and its research note, then build from
the real pictures. Cross the row off here in the same change. Nothing in `legacy/blender/` is edited, and the legacy
tiles 6,12 / 7,12 / 8,13 stay byte-identical.

The **draft desk** (`gidi_kit/draft.py`, `kit_draft.py`: the seeded rules that write a first draft of a spot's records)
stays here in `legacy/` (owner, 24 Oct). It is run as it is; its rules are not extended.
