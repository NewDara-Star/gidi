# The drawing board

The owner, 16 Oct 2026: "we should hand draw... we should know where something meets something... where the roads start, where the roads end, where the houses are, we should be able to move them."

The drawing board is where the map is made by hand. Under it lies a study of real Lagos at 1:3 (the new frame, 27 x 10.5 km); on top, every road, plot, wall, building, lean-to, stall, pole, tree, place and person spot of the map is drawn, moved, turned and deleted, record by record. Each save writes whole records into `map/<dNN>/` (the format is `docs/MAP-FORMAT.md`), and the map is the truth: the builders in the game repo build what it says.

## Open it

```
python3 scripts/board_server.py [--port 8777]
```

Then open http://127.0.0.1:8777/web/board.html (or the port you gave).

- Without the server the study still shows, but nothing loads or saves.
- The address bar keeps where you are looking (`#x,y,zoom`). Bookmark a spot, or send it to someone.

## The study underlay

Real Lagos, miniaturised, to draw over. Switch each layer in the top bar: water, motorways, trunk, primary and secondary roads, ramps, rail, bridges, the districts' outlines, the unsure lines, real places, and, zoomed in, the real roofs. It is a study aid only: real names and lines are shown and never written into the map (a new district's outline is the one thing copied, when it is first started).

The underlay is generated (`web/frame-study.js` by `scripts/frame_study.py`, `web/frame-tiles/` by `scripts/frame_footprints.py`) and never committed. Those scripts can't be re-run today (their inputs are lost; NOW's Owed list); a copy is in `~/gidi-data/frame-backup-25oct/`.

## Drawing

Pick the district to draw in, then a tool (its key in brackets):

| Tool | Key | What it does |
|---|---|---|
| Select | `V` | Click to select; drag to move. `R` / `Shift R` turns 15°, `[` `]` turns 1°, `Delete` removes. The side panel shows every field, and asks for the ones still unset. |
| Street | `S` | A road, street, lane or path: click points, `Enter` to finish, `Backspace` takes back a point. |
| Building, Plot | `B`, `P` | Drag a box. |
| Wall | `W` | Click points, `Enter` to finish. |
| Gate | `G` | Click a wall where the gate starts, then where it ends. |
| Lean-to | `L` | Click a building side or a wall where it starts, then where it ends. |
| Tree | `T` | Click to plant. |
| Furniture | `F` | Stalls, poles, parked vehicles, furniture, heaps: click to place. |
| Place | `A` | What the game uses a spot for: drag a box. |
| Surface | `U` | Click a road to give it the surface. |
| Frontage | `E` | Click a plot's side that faces a street. |
| Stamp | `K` | Copy records, with their dress, from the map or a stamp source (`map-stamps/`, the format example), then place them; `R`, `[` `]` turn the copy. |
| Face | `C` | Click a building's side to dress it: windows, doors, shopfronts, stains, add-ons (the face editor). |
| Goods | `O` | Click inside a lean-to, stall, heap or bin to put an item there. |
| Ground | `D` | Paint a patch of ground: click points, `Enter` to finish. |
| Relief | `H` | Drag a box for a bump-and-dip grid; click a cell to raise it, `⌥`-click to lower. |
| Litter | `X` | Click to drop a piece of litter. |
| Brush | `N` | Brush litter, goods, relief or ground paint; every stroke writes full records. `⌥` erases, `[` `]` size the brush. |
| Person | `I` | A person spot: where someone does something, and when. Click (drag to face them). |
| Wire | `J` | Click a pole, then another pole (a line) or a house side or wall (a drop); `Shift` keeps going from the last pole. |

- **Pan:** drag empty ground, hold `Space`, or use the right button. Scroll to zoom. `0` shows the whole frame.
- **Undo:** `⌘Z` takes back the last save or delete, as long as nothing has changed it since.
- **Unset fields:** a record may be saved before every value is known. It shows dashed amber, each missing field in red in the panel. The board never fills a value in.

## Checks

The server runs `scripts/check_map.py` on the district after every save; each record's problems come back with its id and show red on the board. The same checker runs before every commit.

## Files

- `web/board.html`: the page. `web/frame.js`: the study underlay and the view. `web/mapedit.js`: the map editor. `web/faceedit.js`: the face editor.
- `scripts/board_server.py`: serves the repo on 127.0.0.1 only, loads and saves whole records by id (MAP-FORMAT section 6 has the calls), and writes only `map/`.
- `schema/map_schema.json`: the fields the panel offers and the server accepts.
