# Gidi

An open-world city inspired by Lagos, built from data and by hand. The owner works across more than one Claude account.

**The one rule that keeps us out of circles (owner, 22 Oct):** buildings, streets and places are fixed BY HAND (hand edits in `web/hand/<district>.json`, on the board). Checks are programs. Never fix a map gap by changing a builder or generator rule (`scripts/hand_spots/*`, `rebuild_areas.py`, gen_*): the generated base is frozen. If a check finds a gap, the answer is a hand edit at that spot, or a fix to the check itself.

**The kit is the game repo's builders** (`~/gidi-game/tools/*_build.py`, 23 Oct): they build what the new map's records say. `legacy/blender/` is the old generated city's kit, frozen and kept only so the old map still builds; never extend it.

**Read `decisions/` first, every session:**
- `decisions/NOW.md`: where the work stands and what's next.
- `decisions/DECISIONS.md`: the owner's standing decisions and rules.
- `decisions/IDEAS.md`: ideas not decided yet.

When the owner decides something, or a good idea comes up, add it there. Update `NOW.md` before the session ends, so the next account picks up where this one stopped.
