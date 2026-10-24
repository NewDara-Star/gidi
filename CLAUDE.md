# Gidi

An open-world city inspired by Lagos, built from data and by hand. The owner works across more than one Claude account.

**The one rule that keeps us out of circles (owner, 22 Oct):** buildings, streets and places are fixed BY HAND (the records in `map/<dNN>/`, drawn on the board; the new map is the truth, owner 24 Oct). Checks are programs. Never fix a map gap by changing a builder or generator rule (`scripts/hand_spots/*`, `rebuild_areas.py`, gen_*): the generated base is frozen. If a check finds a gap, the answer is a hand edit at that spot, or a fix to the check itself.

**The kit is the game repo's builders** (`~/gidi-game/tools/*_build.py`, 23 Oct): they build what the new map's records say. `legacy/blender/` is the old generated city's kit, frozen and kept only so the old map still builds; never extend it.

**Nothing is claimed without proof (owner, 24 Oct).** Hooks in `.claude/` hold it for gidi and gidi-game: the checks run before every commit, push and stop, and block on failure (a check that can't run blocks too); every code or map commit has a `Checked:` paragraph (what was run or looked at, what it showed, in numbers; "by eye" where it was by eye; what wasn't checked); a second model reviews every push and blocks claims with nothing behind them. Commit and push in separate commands. Never loosen a check to pass it, never work around a hook: if one is wrong, fix the hook in its own commit and say why. Say what you checked; an agent's report is checked before it is passed on.

**Research the industry standard first (owner, 24 Oct: "not just when we're stuck... when we want to start stuff, see how the industry standard is").** When starting anything new (a look, a model, a tool, a level, a performance fix), first find how studios, the engine's makers and expert artists do it (docs, talks, breakdowns, tutorials), adapt that, and say in the commit what was found and where. Not only when stuck: the street test of 375 houses could not load until research showed what games do (shared tiling textures, detail in images instead of triangles). Downloads still need the owner's OK.

**Read `decisions/` first, every session:**
- `decisions/NOW.md`: where the work stands and what's next.
- `decisions/DECISIONS.md`: the owner's standing decisions and rules.
- `decisions/IDEAS.md`: ideas not decided yet.
- `decisions/CODEBASE.md`: what the three repos hold, live or old (from `scripts/inventory.py`).

When the owner decides something, or a good idea comes up, add it there. Update `NOW.md` before the session ends, so the next account picks up where this one stopped.
