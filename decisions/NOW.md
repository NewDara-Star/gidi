# Where the work stands (update at the end of every session)

**16 Oct 2026, evening.** Gidi v2 is merged (PR #54): it's the live map.

**Done: Gidi v2 is built and frozen.**
- **The v2 layout:**
  - 17 districts at 1:4, about 133,000 buildings
  - Old Island as an island, with Banana Island
  - the Long, Channel, Wharf, Creek, Cable and Fishermen's bridges
- **Every district came from its deep study** (`docs/studies/`), with fabric-type zones. Two calibration passes, then the generator stopped (the stop line, `DECISIONS.md`).
- **Hand fixes:**
  - link streets for cut-off clusters
  - Creekside Road for the Bazaar's creek strip
  - Banana Island's causeway road
  - houses off building lines, overlaps and stranded tables cleared

  All are recorded as edits in `web/hand/<id>.json`.
- **All 17 frozen** (`web/hand/<id>.json`, `"layout": "v2"`). The frozen bake reproduces the city exactly and is byte-identical run to run.
- **Checks:** 16 of 17 districts pass every check (`scripts/check_district.py`, now on the finished map). The Bazaar still needs chemists near the creek strip, a hand-placing job.
- **Fit to real Lagos:** 64% of measures within 20% (`docs/data/deep-check/SUMMARY.md`).
- **Road surfaces** on every road (tar, worn, interlock, laterite, sand, mud), drawn in the 2D ground plan.
- **Hand files can now:** add, delete or name roads; set surfaces; label furniture; plus the building and furniture edits.

**Next:**
1. ~~The Maze and Hub list~~: agreed 16 Oct (`docs/hand/maze-hub-lagos.md`); names settled (Press Row, Gari Yard).
2. Hand-make the Maze and the Hub from that list (in progress). Rebuild and lock the opening.
3. The next districts, one by one, the same way.

**Later:**
- the look pass from the references
- kerbs (roads pass 4)
- isms groups
- the data delete-later list
