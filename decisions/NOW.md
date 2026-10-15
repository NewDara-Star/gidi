# Where the work stands (update at the end of every session)

**15 Oct 2026, late.** Branch `layout/wire-v2` (not merged; the live map is still v1).

**Done:**
- The map build runs on the v2 frame (`web/layout-v2.json`, terrain rebuilt).
- Border roads drawn once in the frame (`scripts/frame_network.py` writes `web/network.json`).
- Generator frame mode (`scripts/gen_fabric.py`); a Food Gate test build works.
- Deep studies of all 17 districts (`docs/studies/`).

**Next, in order** (detail in `docs/LAYOUT-V2.md`, "Where the rebuild stands"):
1. Profiles from the deep studies, with fabric-type zones; profiles for the Airport and Saba.
2. Generate all 17 side by side; check each against its study's targets.
3. A renaming pass (parallel builds can clash on street names).
4. Show the owner, then freeze each district.

**Story (owner):** write the characters next (`decisions/story/`). Paste `gidi-act1-draft.md` and `gidi-performance-capture.md` into the repo from the other account.

**Later:**
- the look pass from the references
- kerbs (roads pass 4)
- isms groups
- the data delete-later list
