# Suspects

Made by `scripts/inventory.py`. A list to read, not to delete: a tool run by hand can be alive with nothing pointing to it.

## Code and documents nothing points to

### gidi (27)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `data/tools/probe-tiles.sh` | 6 | 2026-10-13 | Reads only the first 128 KB of each height tile (its location), so we can skip tiles outside Lagos. Takes about a minut… |
| `scripts/study_village.py` | 24 | 2026-10-13 | Waterfront studies: split the buildings on the water (stilt villages: more than 60 m from any mapped road) from the lan… |
| `scripts/draw_terrain.py` | 27 | 2026-10-15 | The terrain review map: colour relief with hillshade, land 0-3 m (flood-prone) marked, contours every 2 m, district out… |
| `scripts/deep_summary.py` | 34 | 2026-10-16 | All districts against their studies on one page (docs/data/deep-check/*.json, from scripts/deep_check.py). Usage: pytho… |
| `scripts/child_plan.py` | 60 | 2026-10-19 | A district's child plan (owner, 19 Oct 2026: a district is the child of its real inspirations): draws docs/hand/<dir>/c… |
| `scripts/hand_spots/ibudo_spot1.py` | 90 | 2026-10-19 | Ìbùdó spot 1 (docs/hand/ibudo/design_v1.png, the owner's approval 19 Oct 2026): Oshodi rebuilt one-for-one beside the R… |
| `legacy/blender/act1_sheet.py` | 71 | 2026-10-23 | The Act 1 kit pieces side by side (docs/KIT-GAPS.md, "New in the v2 layout"): the face-me-I-face-you block, the motor p… |
| `legacy/blender/catalogue.py` | 48 | 2026-10-23 | Contact sheet of the kit: the same footprint built for each district character and several seeds. |
| `legacy/blender/gidi_kit/__init__.py` | 1 | 2026-10-23 |  |
| `legacy/blender/gidi_kit/detail.py` | 20 | 2026-10-23 | Detail level for the whole kit: 'full' for renders, 'web' for the streamed city (flat roof sheets, flat lettering, ligh… |
| `legacy/blender/gidi_kit/facade.py` | 404 | 2026-10-23 | A walk-up's street face, close up (the facade pass, 22 Oct 2026): what Balogun and Isale Eko faces carry on top of the … |
| `legacy/blender/gidi_kit/roadside.py` | 240 | 2026-10-23 | Roadside furniture that makes a road read and lets you find your way: street lights (single and double arm, solar ones … |
| `legacy/blender/kinds_sheet.py` | 70 | 2026-10-23 | Contact sheet of every registered kind (except houses), each built on footprints taken from the real data, a few seeds … |
| `legacy/blender/lights_sheet.py` | 23 | 2026-10-23 | Traffic lights, street-light ads, the new statues. blender -b --factory-startup -P legacy/blender/lights_sheet.py |
| `legacy/blender/montage.py` | 23 | 2026-10-23 | Stitch legacy/blender/out/kinds/*.jpg into one labelled sheet: python3 legacy/blender/montage.py [out.jpg] [cols] |
| `legacy/blender/monuments_sheet.py` | 27 | 2026-10-23 | Every monument in the kit side by side. blender -b --factory-startup -P legacy/blender/monuments_sheet.py -- [--out leg… |
| `legacy/blender/new_kit_sheet.py` | 40 | 2026-10-23 | The newest kit pieces side by side: the container truck, the 911 food lorry, the trains, the Crown Hall, the central mo… |
| `legacy/blender/new_kit_sheet2.py` | 58 | 2026-10-23 | Contact sheets for the second batch: --part vehicles (service vehicles, the molue, port machines, boats) or --part plac… |
| `legacy/blender/reach_sheet.py` | 17 | 2026-10-23 | The Reach, close up. blender -b --factory-startup -P legacy/blender/reach_sheet.py |
| `legacy/blender/roadside_sheet.py` | 28 | 2026-10-23 | The roadside kit side by side: lamps, a direction sign, a gantry, speed and no-parking discs, a dressed bridge deck. bl… |
| `legacy/blender/vehicles_sheet.py` | 39 | 2026-10-23 | Line-up of every vehicle in its conditions, and a crowd of every dress type. blender -b --factory-startup -P legacy/ble… |
| `legacy/blender/wear_sheet.py` | 80 | 2026-10-23 | A street of Maze houses on their own, to judge wear and age close up (no tile build). blender -b --factory-startup -P l… |
| `docs/lagos-study/similar/scripts/appendix.py` | 27 | 2026-10-24 | Appendix A and B of SIMILAR.md (unit fingerprints, neighbour pairs) from analysis.json. |
| `docs/lagos-study/similar/scripts/plot_units.py` | 25 | 2026-10-24 | Map of the study units (SIMILAR.md's unit pictures), drawn with common.py. |
| `scripts/design_density.py` | 198 | 2026-10-24 | A density pass: fill a district the way its real counterpart is built (Claude's design pass, owner 17 Oct 2026: "build … |
| `scripts/study_structure.py` | 130 | 2026-10-24 | Structure study of a district's inspiration from Google Open Buildings v3 (outlines) and OSM (streets), and the same me… |
| `scripts/twin_photos.py` | 48 | 2026-10-24 | Street twins' pictures for one built area of a child district (docs/hand/<dir>/twins/<area>.json). plan:   python3 scri… |

### gidi-game (2)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `tools/fab_list.sh` | 9 | 2026-10-19 | What's in the project from Fab (added = in Content/Fab). tools/fab_list.sh |
| `tools/loose_build.py` | 55 | 2026-10-23 | Goods and litter lying loose on the ground, built in Blender: blender -b -P tools/loose_build.py -- <out.blend> [recipe… |

### gidi-data (3)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `research/data/probe-tiles.sh` | 6 | 2026-10-24 | Reads only the first 128 KB of each height tile (its location), so we can skip tiles outside Lagos. Takes about a minut… |
| `research/google/kits/old-town/tests/ot13/mk13_first.py` | 55 | 2026-10-24 | ot13 map as first written from the Street View frame: only KIT.md section 12 fields, by eye (usage: mk13_first.py map_f… |
| `research/google/kits/old-town/tools/part_view.py` | 87 | 2026-10-24 | Render kit parts alone (outside the repo; a test tool). blender -b --factory-startup -P part_view.py -- --gidi <repo> -… |

## In to-delete/, for the owner to delete (93 files, 6.5 MB)

Not read for references or names; why each went is in `to-delete/README.md`.

- `to-delete/README.md`
- `to-delete/decisions/NOW-log-16-22-oct.md`
- `to-delete/docs/CITY-LIVING-TEST.md`
- `to-delete/docs/DISTRICT-BRIEF.md`
- `to-delete/docs/FLOW-AUDIT.md`
- `to-delete/docs/ISMS-BUILD.md`
- `to-delete/docs/KIT-GAPS.md`
- `to-delete/docs/LAGOS-LOOK.md`
- `to-delete/docs/LAYOUT-V2.md`
- `to-delete/docs/REBUILD-PLAN.md`
- `to-delete/docs/TWINS.md`
- `to-delete/docs/UNREAL-PORT-PLAN.md`
- `to-delete/docs/audit/README.md`
- `to-delete/docs/audit/bazaar.md`
- `to-delete/docs/audit/border.md`
- `to-delete/docs/audit/capital.md`
- `to-delete/docs/audit/estate.md`
- `to-delete/docs/audit/foodgate.md`
- `to-delete/docs/audit/frontier.md`
- `to-delete/docs/audit/heights.md`
- `to-delete/docs/audit/hub.md`
- `to-delete/docs/audit/jungle.md`
- `to-delete/docs/audit/maze.md`
- `to-delete/docs/audit/oldisland.md`
- `to-delete/docs/audit/oldshore.md`
- `to-delete/docs/audit/port.md`
- `to-delete/docs/audit/railside.md`
- `to-delete/docs/audit/watertown.md`
- `to-delete/docs/data/deep-check/SUMMARY.md`
- `to-delete/docs/data/deep-check/airport.json`
- `to-delete/docs/data/deep-check/bazaar.json`
- `to-delete/docs/data/deep-check/border.json`
- `to-delete/docs/data/deep-check/capital.json`
- `to-delete/docs/data/deep-check/estate.json`
- `to-delete/docs/data/deep-check/foodgate.json`
- `to-delete/docs/data/deep-check/frontier.json`
- `to-delete/docs/data/deep-check/heights.json`
- `to-delete/docs/data/deep-check/hub.json`
- `to-delete/docs/data/deep-check/jungle.json`
- `to-delete/docs/data/deep-check/maze.json`
- `to-delete/docs/data/deep-check/oldisland.json`
- `to-delete/docs/data/deep-check/oldshore.json`
- `to-delete/docs/data/deep-check/port.json`
- `to-delete/docs/data/deep-check/railside.json`
- `to-delete/docs/data/deep-check/watertown.json`
- `to-delete/docs/data/deep-check/yaba.json`
- `to-delete/docs/data/google-vs-osm.json`
- `to-delete/docs/data/structure-foodgate.json`
- `to-delete/docs/gidi-districts-v0.3.md`
- `to-delete/docs/hand/lagos-pass.md`
- `to-delete/docs/img/act1-kit-sheet.jpg`
- `to-delete/docs/img/bridge-landings.png`
- `to-delete/docs/img/gutters-estate.png`
- `to-delete/docs/img/gutters-maze.png`
- `to-delete/docs/img/hub-knot.png`
- `to-delete/docs/img/hub-map.png`
- `to-delete/docs/img/layout-v2-island.png`
- `to-delete/docs/img/pilot-foodgate-2d.png`
- `to-delete/docs/img/pilot-foodgate-3d-district.jpg`
- `to-delete/docs/img/pilot-foodgate-3d-market-sheds.jpg`
- `to-delete/docs/img/pilot-foodgate-3d-market.jpg`
- `to-delete/docs/img/pilot-foodgate-3d-street_level.jpg`
- `to-delete/docs/img/pilot-foodgate-3d-streets.jpg`
- `to-delete/docs/img/pilot-ground-plan-junction.png`
- `to-delete/docs/img/road-heights.png`
- `to-delete/docs/img/roads-clean.png`
- `to-delete/docs/img/roundabouts.png`
- `to-delete/docs/img/structure-google-osm-gidi.png`
- `to-delete/docs/img/v2-frame-baked.png`
- `to-delete/docs/junctions.md`
- `to-delete/docs/kit/MODELLER-BRIEF-ACT1.md`
- `to-delete/docs/living-test-2026-10-13.md`
- `to-delete/docs/living-test-2026-10-13b.md`
- `to-delete/docs/living-test-2026-10-13c.md`
- `to-delete/docs/living-test-2026-10-14.md`
- `to-delete/docs/living-test-2026-10-14b.md`
- `to-delete/docs/living-test-2026-10-14c.md`
- `to-delete/docs/living-test-2026-10-14d.md`
- `to-delete/docs/living-test-2026-10-14e.md`
- `to-delete/docs/living-test-2026-10-14f.md`
- `to-delete/docs/living-test-2026-10-14g.md`
- `to-delete/docs/living-test-2026-10-14h.md`
- `to-delete/docs/living-test-2026-10-14i.md`
- `to-delete/docs/living-test-2026-10-14j.md`
- `to-delete/docs/living-test-2026-10-14k.md`
- `to-delete/docs/living-test-2026-10-14l.md`
- `to-delete/docs/living-test-2026-10-15-gutters.md`
- `to-delete/docs/living-test-2026-10-15m.md`
- `to-delete/docs/living-test-2026-10-15n.md`
- `to-delete/docs/look/COVERAGE.md`
- `to-delete/docs/pilot-foodgate.md`
- `to-delete/docs/road-heights.md`
- `to-delete/docs/terrain.md`

## Names of files that exist nowhere

Paths named in a document or in code that match no file in any repo (outputs and caches skipped).

- `gidi:decisions/CHECKS.md`: `tools/bake.sh`
- `gidi:decisions/CODEBASE.md`: `concept.py`, `fabric.py`, `lagoon.py`, `lgamap.py`, `lgas.py`, `scripts/compare.py`, `scripts/gen3d.py`, `sea.py`, `study.py`, `tools/bake.sh`, `tools/perf.sh`
- `gidi:decisions/DECISIONS.md`: `tools/perf.sh`
- `gidi:decisions/story/README.md`: `gidi-performance-capture.md`, `gidi-roadmap.md`
- `gidi:decisions/story/act-1-draft.md`: `gidi-roadmap.md`
- `gidi:decisions/story/acts-2-3-draft.md`: `gidi-performance-capture.md`
- `gidi:docs/lagos-study/STUDY.md`: `classify.py`, `feat.py`, `grid_bld.py`, `grid_orient.py`, `rasters.py`, `roads.py`
- `gidi:docs/lagos-study/similar/scripts/appendix.py`: `appendix.md`
- `gidi:scripts/deep_summary.py`: `out.md`
