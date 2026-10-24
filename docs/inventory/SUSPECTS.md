# Suspects

Made by `scripts/inventory.py`. A list to read, not to delete: a tool run by hand can be alive with nothing pointing to it.

## Code and documents nothing points to

### gidi (34)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `data/tools/probe-tiles.sh` | 6 | 2026-10-13 | Reads only the first 128 KB of each height tile (its location), so we can skip tiles outside Lagos. Takes about a minut… |
| `docs/living-test-2026-10-13.md` | 108 | 2026-10-13 | City living test, 13 Oct 2026: the Maze, the Hub, Jungle City: This is the first run of `docs/CITY-LIVING-TEST.md`, don… |
| `docs/living-test-2026-10-13b.md` | 135 | 2026-10-13 | City living test, 13 Oct 2026 (second run): the Maze, the Hub, Jungle City, Food Gate: This is the second run of `docs/… |
| `docs/living-test-2026-10-13c.md` | 135 | 2026-10-13 | City living test, 13 Oct 2026 (third run): all five districts: This is the third run of `docs/CITY-LIVING-TEST.md` toda… |
| `docs/living-test-2026-10-14.md` | 127 | 2026-10-14 | City living test, 14 Oct 2026: six districts, with the new Capital: This is the test in `docs/CITY-LIVING-TEST.md`, run… |
| `docs/living-test-2026-10-14b.md` | 97 | 2026-10-14 | City living test, 14 Oct 2026 (second run): seven districts, with the new Bazaar: This run tests four changes on this b… |
| `docs/living-test-2026-10-14c.md` | 71 | 2026-10-14 | City living test, 14 Oct 2026 (third run): eight districts, with the new Port: There are two states: - **Before:** `mai… |
| `docs/living-test-2026-10-14d.md` | 67 | 2026-10-14 | City living test, 14 Oct 2026 (fourth run): nine districts, with the new Railside: There are two states: - **Before:** … |
| `docs/living-test-2026-10-14e.md` | 68 | 2026-10-14 | City living test, 14 Oct 2026 (fifth run): ten districts, with the new Estate: There are two states: - **Before:** `mai… |
| `docs/living-test-2026-10-14f.md` | 83 | 2026-10-14 | City living test, 14 Oct 2026 (sixth run): eleven districts, with the new Old Island: There are two states: - **Before:… |
| `docs/living-test-2026-10-14g.md` | 104 | 2026-10-14 | City living test, 14 Oct 2026 (seventh run): twelve districts, with the new Heights: There are two states: - **Before:*… |
| `docs/living-test-2026-10-14h.md` | 57 | 2026-10-14 | City living test, 14 Oct 2026 (eighth run): the Heights v2: There are two states: - **Before:** `main` at commit `47b75… |
| `docs/living-test-2026-10-14i.md` | 42 | 2026-10-14 | City living test, 14 Oct 2026 (ninth run): the Heights v3: There are two states: - **Before:** `main` at commit `a67977… |
| `docs/living-test-2026-10-14j.md` | 66 | 2026-10-14 | City living test, 14 Oct 2026 (tenth run): thirteen districts, with the new Frontier: There are two states: - **Before:… |
| `docs/living-test-2026-10-14k.md` | 52 | 2026-10-15 | City living test, 15 Oct 2026 (eleventh run): Old Shore: There are two states: - **Before:** `main` at commit `cf613f8`… |
| `docs/living-test-2026-10-14l.md` | 64 | 2026-10-15 | City living test, 15 Oct 2026: the Border: There are two states: - **Before:** `main` at commit `cf613f8` (thirteen dis… |
| `docs/living-test-2026-10-15-gutters.md` | 31 | 2026-10-15 | City living test, 15 Oct 2026: open gutters (ism 15, group 1): `scripts/isms.py` now puts open gutters into the city da… |
| `docs/living-test-2026-10-15n.md` | 38 | 2026-10-15 | City living test, 15 Oct 2026: road clean-up, pass 1: The first of four road passes. `scripts/roadclean.py` now runs in… |
| `docs/studies/airport.md` | 126 | 2026-10-15 | The Airport: the deep study: Inspired by Murtala Muhammed International Airport, Ikeja. Study area: 15.81 km², 15.81 km… |
| `docs/data/deep-check/SUMMARY.md` | 22 | 2026-10-16 | Each cell is Gidi against its real inspiration (0% = the same; ⚠ = more than 20% off). "Squares" = built 500 m squares … |
| `scripts/deep_summary.py` | 34 | 2026-10-16 | All districts against their studies on one page (docs/data/deep-check/*.json, from scripts/deep_check.py). Usage: pytho… |
| `scripts/design_density.py` | 198 | 2026-10-18 | A density pass: fill a district the way its real counterpart is built (Claude's design pass, owner 17 Oct 2026: "build … |
| `scripts/child_plan.py` | 60 | 2026-10-19 | A district's child plan (owner, 19 Oct 2026: a district is the child of its real inspirations): draws docs/hand/<dir>/c… |
| `scripts/hand_spots/ibudo_spot1.py` | 90 | 2026-10-19 | Ìbùdó spot 1 (docs/hand/ibudo/design_v1.png, the owner's approval 19 Oct 2026): Oshodi rebuilt one-for-one beside the R… |
| `scripts/twin_photos.py` | 48 | 2026-10-20 | Street twins' pictures for one built area of a child district (docs/hand/<dir>/twins/<area>.json). plan:   python3 scri… |
| `legacy/blender/act1_sheet.py` | 71 | 2026-10-23 | The Act 1 kit pieces side by side (docs/KIT-GAPS.md, "New in the v2 layout"): the face-me-I-face-you block, the motor p… |
| `legacy/blender/gidi_kit/__init__.py` | 1 | 2026-10-23 |  |
| `legacy/blender/gidi_kit/detail.py` | 20 | 2026-10-23 | Detail level for the whole kit: 'full' for renders, 'web' for the streamed city (flat roof sheets, flat lettering, ligh… |
| `legacy/blender/kinds_sheet.py` | 70 | 2026-10-23 | Contact sheet of every registered kind (except houses), each built on footprints taken from the real data, a few seeds … |
| `legacy/blender/lights_sheet.py` | 23 | 2026-10-23 | Traffic lights, street-light ads, the new statues. blender -b --factory-startup -P legacy/blender/lights_sheet.py |
| `legacy/blender/montage.py` | 23 | 2026-10-23 | Stitch legacy/blender/out/kinds/*.jpg into one labelled sheet: python3 legacy/blender/montage.py [out.jpg] [cols] |
| `legacy/blender/vehicles_sheet.py` | 39 | 2026-10-23 | Line-up of every vehicle in its conditions, and a crowd of every dress type. blender -b --factory-startup -P legacy/ble… |
| `docs/lagos-study/similar/scripts/appendix.py` | 27 | 2026-10-24 | Appendix A and B of SIMILAR.md (unit fingerprints, neighbour pairs) from analysis.json. |
| `docs/lagos-study/similar/scripts/plot_units.py` | 25 | 2026-10-24 | Map of the study units (SIMILAR.md's unit pictures), drawn with common.py. |

### gidi-game (1)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `tools/loose_build.py` | 55 | 2026-10-23 | Goods and litter lying loose on the ground, built in Blender: blender -b -P tools/loose_build.py -- <out.blend> [recipe… |

### gidi-data (3)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `research/data/probe-tiles.sh` | 6 | 2026-10-24 | Reads only the first 128 KB of each height tile (its location), so we can skip tiles outside Lagos. Takes about a minut… |
| `research/google/kits/old-town/tests/ot13/mk13_first.py` | 55 | 2026-10-24 | ot13 map as first written from the Street View frame: only KIT.md section 12 fields, by eye (usage: mk13_first.py map_f… |
| `research/google/kits/old-town/tools/part_view.py` | 87 | 2026-10-24 | Render kit parts alone (outside the repo; a test tool). blender -b --factory-startup -P part_view.py -- --gidi <repo> -… |

## Names of files that exist nowhere

Paths named in a document or in code that match no file in any repo (outputs and caches skipped).

- `gidi:decisions/CHECKS.md`: `tools/bake.sh`
- `gidi:decisions/CODEBASE.md`: `-pattern-study.md`, `concept.py`, `fabric.py`, `lagoon.py`, `lgamap.py`, `lgas.py`, `scripts/compare.py`, `scripts/gen3d.py`, `sea.py`, `study.py`, `tools/bake.sh`, `tools/perf.sh`
- `gidi:decisions/DECISIONS.md`: `tools/perf.sh`
- `gidi:decisions/NOW.md`: `tools/perf.sh`
- `gidi:decisions/story/README.md`: `gidi-performance-capture.md`, `gidi-roadmap.md`
- `gidi:decisions/story/act-1-draft.md`: `gidi-roadmap.md`
- `gidi:decisions/story/acts-2-3-draft.md`: `gidi-performance-capture.md`
- `gidi:docs/DISTRICT-BRIEF.md`: `-pattern-study.md`
- `gidi:docs/lagos-study/STUDY.md`: `classify.py`, `feat.py`, `grid_bld.py`, `grid_orient.py`, `rasters.py`, `roads.py`
- `gidi:docs/lagos-study/similar/scripts/appendix.py`: `appendix.md`
- `gidi:scripts/deep_summary.py`: `out.md`
