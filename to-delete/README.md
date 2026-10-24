# to-delete: for the owner to delete

The owner asked (24 Oct) that what has no use any more is moved here, not deleted: they delete it themselves. Each file keeps
its old path under `to-delete/`, so `git log -- <old path>` still finds its history. Nothing here is read by any program
(`scripts/inventory.py` lists this folder as "to delete" and leaves it out of the orphan and missing-name counts).

Before a file moved, it was read for what still holds for the new map. Those lessons are in `docs/OLD-MAP-LESSONS.md`; the
real Lagos research that stays is indexed in `docs/RESEARCH.md`.

## Moved 24 Oct (91 files, 6.4 MB)

| Files | What they were | Why they go | What replaced them, or where their lessons went |
|---|---|---|---|
| `docs/living-test-2026-10-1*.md` (18), `docs/CITY-LIVING-TEST.md` | agents walking and riding the old generated map | test a map that is history | lessons in OLD-MAP-LESSONS ("Checking"); IDEAS, "A living test for the new map" |
| `docs/audit/*` (16) | old districts measured against real Lagos | measured the generator's output | the real numbers stay in `docs/studies/` and the pattern studies |
| `docs/data/deep-check/*` (15), `docs/data/google-vs-osm.json`, `docs/data/structure-foodgate.json` | the generator's calibration against the deep study | calibration is banned (the generated base is frozen) | the deep study itself stays (`docs/data/deep/`) |
| `docs/LAYOUT-V2.md`, `docs/gidi-districts-v0.3.md`, `docs/DISTRICT-BRIEF.md` | the 1:4 layout and its 17 districts | replaced by real Lagos at 1:3 and the 51 districts (22 Oct) | `docs/lagos-study/`, `NAMES.md` |
| `docs/REBUILD-PLAN.md`, `docs/pilot-foodgate.md` | rebuilding the generator from Google | the plan is hand-made now | block and market facts in OLD-MAP-LESSONS |
| `docs/terrain.md`, `docs/road-heights.md`, `docs/junctions.md` | the generator's ground, deck and junction rules | rules for the frozen generator | real ground medians, deck clearances, junction facts in OLD-MAP-LESSONS |
| `docs/FLOW-AUDIT.md` | the old map's missing corridors | the new map is on the real roads | the corridors in OLD-MAP-LESSONS |
| `docs/ISMS-BUILD.md` | building the isms into the generator | generator work | the isms as places, and the missing places, in OLD-MAP-LESSONS; `docs/LAGOS-ISMS.md` stays |
| `docs/KIT-GAPS.md`, `docs/kit/MODELLER-BRIEF-ACT1.md`, `docs/look/COVERAGE.md`, `docs/LAGOS-LOOK.md` | the old Blender kit's gaps and briefs | the old kit is frozen; the builders are the kit (23 Oct) | builder lessons in OLD-MAP-LESSONS |
| `docs/hand/lagos-pass.md` | the old map's Lagos pass | replaced by "the owner's eye passes a kit" | the motor-park frame list in OLD-MAP-LESSONS |
| `docs/TWINS.md` | a real twin per old building type | old-map types | the idea lives on in the ultimate test |
| `docs/UNREAL-PORT-PLAN.md` | the first Unreal plan | done or replaced by gidi-game's builders | Unreal lessons in OLD-MAP-LESSONS |
| `docs/img/*` (19) | pictures used only by the files above | nothing else links them | |

## Outside git

`~/gidi-data/to-delete/branches/` holds patches saved from the branches and worktrees removed on 24 Oct (unmerged work that
later decisions replaced): `hand/ibudo-plan-v2`, `look/style-test` (PR #18, closed), `kit/lockups`, the uncommitted changes
of `hand/ibudo-areas-12` and of the board brushes worktree, and its empty test district `map/d21`. They are too big for git
history, so they are kept there for the owner to look at or delete.
