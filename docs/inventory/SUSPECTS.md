# Suspects

Made by `scripts/inventory.py`. A list to read, not to delete: a tool run by hand can be alive with nothing pointing to it.

## Code and documents nothing points to

### gidi (2)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `data/tools/probe-tiles.sh` | 6 | 2026-10-13 | Reads only the first 128 KB of each height tile (its location), so we can skip tiles outside Lagos. Takes about a minut… |
| `docs/lagos-study/similar/scripts/plot_units.py` | 24 | 2026-10-25 | Map of the study units (SIMILAR.md's unit pictures), drawn with common.py. |

### gidi-game (1)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `tools/loose_build.py` | 55 | 2026-10-23 | Goods and litter lying loose on the ground, built in Blender: blender -b -P tools/loose_build.py -- <out.blend> [recipe… |

### gidi-data (2)

| file | lines | changed | what it says it is |
|---|---|---|---|
| `research/data/probe-tiles.sh` | 6 | 2026-10-24 | Reads only the first 128 KB of each height tile (its location), so we can skip tiles outside Lagos. Takes about a minut… |
| `research/google/kits/old-town/tests/ot13/mk13_first.py` | 55 | 2026-10-24 | ot13 map as first written from the Street View frame: only KIT.md section 12 fields, by eye (usage: mk13_first.py map_f… |

## Names of files that exist nowhere

Paths named in a document or in code that match no file in any repo (outputs and caches skipped).

Not marked as gone (to fix: the line names a file as if it were there):

- `gidi:docs/lagos-study/similar/scripts/appendix.py`: `appendix.md`

Marked as gone (the line says deleted, lost or never committed, or the document is history):

- `gidi-data:research/google/ibudo/NOTES.md`: `docs/TWINS.md`
- `gidi-game:ASSETS.md`: `tools/frame_motorpark.py`
- `gidi-game:tools/props_build.py`: `docs/hand/lagos-pass.md`
- `gidi:decisions/CHECKS.md`: `check_district.py`, `check_real.py`
- `gidi:decisions/DECISIONS.md`: `scripts/compounds.py`, `scripts/cross_sections.py`, `scripts/roadends.py`, `tools/perf.sh`
- `gidi:decisions/HISTORY.md`: `docs/LAYOUT-V2.md`, `docs/TWINS.md`, `docs/hand/lagos-pass.md`, `scripts/autoclean.py`, `scripts/check_real.py`, `scripts/hand_spots/ibudo_real_area.py`, `scripts/rebuild_areas.py`, `scripts/twins.py`
- `gidi:decisions/NOW.md`: `frame_motorpark.py`
- `gidi:decisions/story/README.md`: `gidi-performance-capture.md`, `gidi-roadmap.md`
- `gidi:decisions/story/act-1-draft.md`: `gidi-roadmap.md`
- `gidi:decisions/story/acts-2-3-draft.md`: `gidi-performance-capture.md`
- `gidi:docs/DATA-SOURCES.md`: `scripts/deep_prep.py`, `scripts/study_google.py`
- `gidi:docs/DEEP-STUDY.md`: `deep_prep.py`, `scripts/deep_check.py`, `scripts/deep_prep.py`, `scripts/deep_profile.py`, `scripts/deep_report.py`, `scripts/rename_mains.py`, `scripts/structure.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/LAGOS-ISMS.md`: `scripts/isms.py`, `scripts/study_isms.py`, `study_isms.py`
- `gidi:docs/OLD-KIT.md`: `goods.py`, `gutters.py`, `kit_draft.py`, `kit_test.py`, `materials.py`, `people.py`, `roadbed.py`, `street.py`, `wear.py`, `zinc.py`
- `gidi:docs/OLD-MAP-LESSONS.md`: `docs/FLOW-AUDIT.md`, `docs/ISMS-BUILD.md`, `docs/KIT-GAPS.md`, `docs/REBUILD-PLAN.md`, `docs/UNREAL-PORT-PLAN.md`, `docs/hand/lagos-pass.md`, `docs/junctions.md`, `docs/pilot-foodgate.md`, `docs/road-heights.md`, `docs/terrain.md`
- `gidi:docs/bazaar-pattern-study.md`: `check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_landmarks.py`
- `gidi:docs/border-pattern-study.md`: `check_district.py`, `explore_city.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `scripts/study_undermapped.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_extract.py`, `study_isms.py`, `study_landmarks.py`
- `gidi:docs/capital-pattern-study.md`: `check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `scripts/study_undermapped.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_landmarks.py`
- `gidi:docs/estate-pattern-study.md`: `check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `scripts/study_wellmapped.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_isms.py`, `study_landmarks.py`
- `gidi:docs/foodgate-pattern-study.md`: `scripts/check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_extract.py`, `study_landmarks.py`
- `gidi:docs/frontier-pattern-study.md`: `check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `scripts/study_wellmapped.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_isms.py`, `study_landmarks.py`
- `gidi:docs/hand/borrowed-lagos.md`: `landmarks.py`, `monuments.py`
- `gidi:docs/hand/maze-hub-lagos.md`: `scripts/hand.py`
- `gidi:docs/heights-pattern-study.md`: `bake_web.py`, `check_district.py`, `explore_city.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_extract.py`, `study_isms.py`, `study_landmarks.py`
- `gidi:docs/hub-pattern-study.md`: `check_district.py`, `scripts/check_district.py`, `scripts/district_profiles.py`, `scripts/draw_gen.py`, `scripts/gen_fabric.py`, `scripts/landmarks.py`, `scripts/study_extract.py`, `scripts/study_landmarks.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`
- `gidi:docs/jungle-pattern-study.md`: `scripts/check_district.py`, `scripts/district_profiles.py`, `scripts/draw_gen.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_landmarks.py`
- `gidi:docs/lagos-study/STUDY.md`: `classify.py`, `feat.py`, `grid_bld.py`, `grid_orient.py`, `rasters.py`, `roads.py`
- `gidi:docs/look/research-roads.md`: `rules.py`
- `gidi:docs/maze-pattern-study.md`: `check_district.py`, `scripts/bake_web.py`, `scripts/build_viewer.py`, `scripts/check_district.py`, `scripts/district_profiles.py`, `scripts/draw_gen.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `scripts/study_landmarks.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`
- `gidi:docs/oldisland-pattern-study.md`: `check_district.py`, `explore_city.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `scripts/study_wellmapped.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_isms.py`, `study_landmarks.py`
- `gidi:docs/oldshore-pattern-study.md`: `check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `scripts/walknet.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_isms.py`, `study_landmarks.py`
- `gidi:docs/port-pattern-study.md`: `check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_landmarks.py`
- `gidi:docs/railside-pattern-study.md`: `check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_isms.py`, `study_landmarks.py`
- `gidi:docs/studies/airport.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/bazaar.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/border.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/capital.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/estate.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/foodgate.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/frontier.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/heights.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/hub.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/jungle.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/maze.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/oldisland.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/oldshore.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/port.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/railside.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/watertown.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/studies/yaba.md`: `deep_prep.py`, `scripts/study_deep.py`, `study_deep.py`
- `gidi:docs/watertown-pattern-study.md`: `check_district.py`, `scripts/district_profiles.py`, `scripts/gen_fabric.py`, `scripts/study_extract.py`, `study_analyse.py`, `study_connect.py`, `study_core.py`, `study_landmarks.py`
