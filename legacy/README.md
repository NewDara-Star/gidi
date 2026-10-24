# Legacy: the old map's kit (frozen)

What the old map was and its parts: `OLD-MAP.md`.

`legacy/blender/` is the Blender kit of the **old generated city** (the 17 frozen districts, `web/gidi-data.js`, the 3D
tab's tiles) and of the first old-town eye tests (ot175, ot91, ot149, ot73, ot45). It is kept only so that old map still
builds: its tiles (6,12 / 7,12 / 8,13 checked) come out byte-identical from here.

**Not for new work.** The new map (`map/`, `docs/MAP-FORMAT.md`) is built by the builders in the game repo
(`~/gidi-game/tools/*_build.py`), which read map records. Do not add parts, fields or fixes here; a thing the new map
needs is a builder or a builder field there, and its fields go in `schema/map_schema.json`.

Run the old city's tiles: `blender -b --factory-startup -P legacy/blender/city.py -- --tiles "6,12;7,12" --out web/city`.
