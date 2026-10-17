# The drawing board

The owner, 16 Oct 2026: "we should hand draw... we should know where something meets something... where the roads start, where the roads end, where the houses are, we should be able to move them."

The drawing board is a clean plan of Gidi to scale, in the browser. Every road edge, plot, wall, house, piece of street furniture and place is drawn where it stands, and can be checked, moved, turned, deleted or added. Each edit is saved as a hand edit (`web/hand/<district>.json`), the same edits the bake applies, so the bake, the checks and the 3D city all follow the drawing. The map data stays the master copy.

## Open it

```
python3 scripts/board_server.py
```

Then open http://127.0.0.1:8777/web/board.html.

- Without the server the board still opens (from any local server), but read-only.
- The address bar keeps where you are looking (`#x,y,zoom`). Bookmark a spot, or send it to someone.

## What it shows

- **Roads at true width, in bands:** the walkway, the gutter, then the carriageway in its surface colour (tar, worn, interlock, laterite, sand, mud), from the agreed cross-sections. Junctions merge where the bands overlap. Dashed lines run down the main roads and arterials, and named roads carry their names.
- **Decks:** flyovers, bridges and ramps, with a dashed outline.
- **Gutters:** open or covered.
- **Plots and walls:** plots dashed green, estate walls as dark lines, market-street zones in amber.
- **Compound walls and gates:** brick-red lines and blue squares. The bake works them out (`scripts/compounds.py`): a share of houses is walled by district (a third in the dense districts, nearly all in the estates), each compound reaches 2 m round its house, stops at the walkway and at other buildings, and neighbours share one wall line. The 3D draws exactly these walls.
- **Buildings:** each footprint, tinted by use: homes, trade, civic, works, water.
- **Street furniture,** each kind with its own symbol:
  - poles, street lights (with the arm), traffic lights
  - bus stops, LASMA posts, transformers, police kiosks
  - overhead signs, the task force truck, people placed by hand
- **Monuments** (stars) and **named places** (pins).
- **Layers:** each of the above can be switched off in the top bar.

## The checks (red outlines)

Problems the built city would have, found live as you work:
- **A building or a compound wall on a road:** inside the carriageway or gutter. Stalls and kiosks in a declared market-street zone are the market spill and are allowed, as `scripts/check_district.py` allows them.
- **Overlapping buildings:** an edge crossing, or a corner well inside another.
- **Furniture in the carriageway, or inside a building.**

The bar at the bottom counts the problems in view. **Click the count to go to each problem in turn.** Zoom in past about 0.6 px per metre for the checks to run.

## Editing

| Tool | Key | What it does |
|---|---|---|
| Select | `V` | Click to select; drag to move. Furniture snaps to the walkway, facing the road; hold `Shift` to place it freely. `R` / `Shift R` turns 15°, `[` `]` turns 1°, `Delete` removes, `⌘Z` undoes. |
| Reshape | (select) | A selected building, plot, zone or street shows handles. Drag a **square** to move a corner or point (corners snap to nearby corners; a street's ends snap onto other roads), drag a **circle** to add one, `⌥`-click a square to remove one. Buildings, furniture and monuments also take **exact numbers** in the side panel: width, depth, angle and middle (setting a size makes a building a rectangle), or x, y and angle. |
| Furniture | `F` | Pick a kind, click to place (it snaps to the walkway). |
| Building | `B` | Pick a kind, drag a box. Turn it afterwards with `R`. |
| Street | `S` | Pick street, lane or main, then click points. Points snap onto existing roads, ends first, so a new street joins the network exactly. `Enter` finishes, `Backspace` takes back a point, `Esc` cancels. |
| Surface | `U` | Pick a surface, click a road. |
| Wall | `W` | Draw a compound wall: click points, `Enter` to finish. Select a wall to delete the piece or cut a 3 m opening where you clicked. |
| Gate | `G` | Click a wall to put a gate in it; select a gate and press `Delete` to remove it. |

- **Pan:** drag empty ground, hold `Space`, or use the right button. Scroll to zoom.
- **Name:** bus stops, traffic lights, LASMA posts and police kiosks can be named in the side panel. That's the label they carry, such as a bus stop's name.
- **Not deletable here:** main roads and arterials. They're the city's frame, from the layout.

## From the board to the city

1. **Each edit is written into the district's hand file at once,** and kept in `web/board-pending.json`, which isn't committed. The board shows pending edits on top of the last bake. The bottom bar says how many there are.
2. **Ask Claude to "bake the board".** Claude runs the bake:
   - Road edits (street added, deleted, cut or reshaped, a road named) in a frozen district need a thaw bake (`GIDI_THAW=<districts>`), then the district is frozen again. The bar flags these.
   - The other edits apply in an ordinary bake.
   - Then the district checks, then the tiles in the edited area.
3. **Undo (`⌘Z`)** takes back the last board edit, as long as it hasn't been baked. After a bake, undo with a new edit.

## New hand-file operations (16 Oct 2026, for the board)

- `move building` takes an optional `rotate` (degrees, about its middle, after the move).
- `move furniture`: `{at, kind, to, ang}`. The nearest of its kind within 2 m.
- `move monument` / `delete monument`: `{at, to, ang}` / `{at}`. The nearest within 3 m.
- `delete place`: `{name}`.
- Compound walls (applied after `scripts/compounds.py`): `cut wall` `{at, gap}`, `delete wall` `{at}`, `add wall` `{pts}`, `add gate` `{x, y}`, `delete gate` `{at}`.
- `reshape building`: `{at, kind, pts}`; `reshape parcel` / `reshape zone`: `{at, pts}`. A new outline.
- `reshape street`: `{at, pts}`. A road edit: the street, lane or district main nearest the point takes a new line.

## Files

- `web/board.html`, `web/board.js`: the board, one canvas, no libraries.
- `scripts/board_server.py`: serves the repo on 127.0.0.1 and saves edits. It accepts only the hand-file operations, and writes only `web/hand/` and `web/board-pending.json`.
- `scripts/hand.py`: applies the edits in the bake.
