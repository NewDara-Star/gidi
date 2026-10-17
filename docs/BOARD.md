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
- **Shops, canopies and balconies:** a shop's front side in thick orange, its canopy as an orange box, balconies as dashed blue boxes, all to scale. The bake works them out (`scripts/fronts.py`): a shop at the kit's share for its district, half the shops with a canopy cut short of the carriageway, balconies only where the 1.1 m slab clears neighbours and roads.
- **Trees:** green circles, about the size of the crown; palms with spokes. The bake plants them (`scripts/trees.py`) at the kit's densities, clear of roads, buildings, walls, furniture and water, including the bush outside the districts.
- **Compound walls and gates:** brick-red lines and blue squares. The bake works them out (`scripts/compounds.py`): a share of houses is walled by district (a third in the dense districts, nearly all in the estates), each compound reaches 2 m round its house, stops at the walkway and at other buildings, and neighbours share one wall line. The 3D draws exactly these walls.
- **Buildings:** each footprint, tinted by use: homes, trade, civic, works, water.
- **Street furniture,** each kind with its own symbol:
  - poles, street lights (with the arm), traffic lights
  - bus stops, LASMA posts, transformers, police kiosks
  - overhead signs, the task force truck, people placed by hand
- **Road signs:** direction signs before the big junctions, speed limits after them, no-parking discs by the markets, gantries over the expressways and bridges (`scripts/things.py`, the rules the kit used to run itself).
- **Road ends:** a close's round turning space, in its road's surface. A road that stops short of anything is ringed in red (`scripts/roadends.py`).
- **Vehicles and people** (layer "Vehicles & people"): every parked car, keke, okada and bus at the road edges and in the parks, the people standing in the markets and parks, the port's machines, the boats, canoes, trains and rail stalls, each to scale and turned the way it faces. The bake places them (`scripts/things.py`); traffic and walkers move in the game, so the data holds how many and what kind ("life"), not where each one is.
- **Ground use** (layer, off at first): what each piece of ground is for (`scripts/ground.py`): the parking strips at the carriageway's edges in blue, motor parks, markets, yards and other plots tinted, the rail corridor. The bottom bar names the ground under the mouse and who may be on it.
- **Monuments** (stars) and **named places** (pins).
- **Layers:** each of the above can be switched off in the top bar.

## The checks (red outlines)

Problems the built city would have, found live as you work:
- **A canopy over the carriageway, or a balcony or canopy into a neighbour.**
- **A tree in the road or inside a building.**
- **A building or a compound wall on a road:** inside the carriageway or gutter. Stalls and kiosks in a declared market-street zone are the market spill and are allowed, as `scripts/check_district.py` allows them.
- **Overlapping buildings:** an edge crossing, or a corner well inside another.
- **Furniture in the carriageway, or inside a building.**
- **A thing on the wrong ground:** a car on a junction's carriageway, the tracks or the water, a person in the road or the gutter, a boat on land. Each kind of ground says who may be on it (`scripts/ground.py`), and `check_district.py` check 16 tests the same.
- **A road that stops short:** it meets no road, house, gate or water.

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
| Tree | `T` | Pick broad or palm, click to plant. Drag a tree to move it; `Delete` removes it. |
| Gate | `G` | Click a wall to put a gate in it; select a gate and press `Delete` to remove it. |

- **Pan:** drag empty ground, hold `Space`, or use the right button. Scroll to zoom.
- **A house's front:** select a front or back house. The panel sets its front side, whether it's a shop, its canopy depth, and which sides have a balcony.
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
- Fronts and trees (applied after `scripts/fronts.py` and `scripts/trees.py`): `set front` `{at, kind, e, shop, aw, bal}` (any of them), `add tree` `{x, y, kind}`, `move tree` `{at, to}`, `delete tree` `{at}`. A tree in the bush is edited through the nearest district's hand file with `"d": "bush"`.
- Compound walls (applied after `scripts/compounds.py`): `cut wall` `{at, gap}`, `delete wall` `{at}`, `add wall` `{pts}`, `add gate` `{x, y}`, `delete gate` `{at}`.
- `reshape building`: `{at, kind, pts}`; `reshape parcel` / `reshape zone`: `{at, pts}`. A new outline.
- `reshape street`: `{at, pts}`. A road edit: the street, lane or district main nearest the point takes a new line.

## Files

- `web/board.html`, `web/board.js`: the board, one canvas, no libraries.
- `scripts/board_server.py`: serves the repo on 127.0.0.1 and saves edits. It accepts only the hand-file operations, and writes only `web/hand/` and `web/board-pending.json`.
- `scripts/hand.py`: applies the edits in the bake.
