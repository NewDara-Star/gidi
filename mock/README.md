# Gidi Mock

Walk and drive through the whole generated city. It's the **Mock** tab of the Gidi map (2D · 3D · Mock), and it also runs as a desktop app.

- **The world:** Gidi's own kit (`blender/`), built from the city data. Every building, road, parcel, structure and landmark comes out of `blender/city.py` as 400 m tiles. Full detail streams in round you, a lighter build further out, and the data's massing on the horizon.
- **The behaviour:** taken from the owner's Real-world sim (`~/Real-world/game/src/client`, copied into `src/` and adapted). Only behaviour is taken; every model is Gidi's:
  - car physics (Rapier, Pacejka tyres, automatic gearbox)
  - G29/G923 force feedback and rev lights over WebHID
  - wheel, pad and keyboard input
  - traffic on a SUMO lane network (signals, give-way, queues, overtaking a stopped player)
  - pedestrians on footpaths and crossings

## Play it
Double-click **`Play Gidi.command`** in the repo root, or run `cd mock && npm install && npm run desktop`. That opens the map; click the **Mock** tab (or a place on the map, then Mock) to drop in there.

- **Unbuilt districts** (The Border, Old Shore, The Frontier) are fenced off with site hoarding. You can't walk or drive in until they're built.
- **Crowds and traffic follow how busy a place is.** Each district has a people-per-km² figure from the research (`DENSITY` in `src/world.ts`): Jungle City, The Maze, The Hub and Old Island are packed, The Estate and The Heights are quiet. Markets, stations, pitches, churches, mosques and schools pull extra people round them.
- **Where you can go comes from the walk map** (`tools/walkmap/bake_walk.py`, 1 m cells in 400 m tiles). It marks every cell as blocked, ground, pavement or path, road, bridge deck, jetty or boardwalk, or water. On foot you can go anywhere but blocked cells and water, roads included. Where you can't go you stop, and you slide along walls. AI walkers keep to pavements and paths. Your car meets a low wall at the shore, open where roads, bridges and jetties reach the water. Bridges and flyovers carry everyone at the kit's deck heights. **M** shows the walk map round you.
- **Press N to write a fix note.** It saves to `mock/notes/NOTES.md` with where you were (district, map coordinates, on foot or driving, the hour) and a screenshot. Open the Mock at that spot again with `?xy=x,y`.

## Build it (once, and after the city or the kit changes)
1. **The city tiles.** Run `python3 blender/city_run.py`.
   - It takes about an hour on this Mac: the full detail runs two tiles at a time, because each one needs about 6 GB of RAM.
   - Output goes to `web/city/full`, `web/city/web` and `web/city/manifest.json`.
   - Gaps (data kinds with no builder yet) are listed in the manifest.
2. **The lane network.** Run these from the repo root, with SUMO in `.venv` (`python3 -m venv .venv && .venv/bin/pip install eclipse-sumo pyproj`):
   ```sh
   python3 tools/roadnet/gidi_to_osm.py web/city/net/gidi.osm web/city/net/gidi.world.json
   PATH=$PWD/.venv/bin:$PATH sh tools/roadnet/build_net.sh web/city/net/gidi.osm web/city/net/gidi.net.xml right
   .venv/bin/python tools/roadnet/bake_net.py web/city/net/gidi.net.xml web/city/net/gidi.osm web/city/net/gidi.world.json web/city/net/gidi.net.bin
   ```
3. **The walk map.** Run `python3 tools/walkmap/bake_walk.py` (2 seconds; it needs `web/city/monuments.json` from step 1).
4. **The fleet and people.** Run `blender -b --factory-startup -P blender/export_fleet.py`, which writes to `mock/public/models/`.
5. **The app.** Run `cd mock && npm install && npm run desktop`. That builds `mock/dist` and opens Gidi (the map, with the Mock tab).

In a browser, serve the repo root (for example `python3 -m http.server` in `~/gidi`) and open `/web/gidi-maps.html`. The published map shows the Mock tab, but the city tiles aren't online, so use the desktop app for the Mock.

## Controls
- **On foot:**
  - WASD to walk, Shift to run, drag to look.
  - **F** gets you into a danfo, **G** into a car, on the nearest lane.
  - **T** steps the hour.
  - **N** writes a note for the fix list, **M** shows the walk map.
- **Driving (keyboard):**
  - W gas, S brake, A/D steer.
  - X/Z move the selector toward D/P (foot on the brake), B parking brake.
  - C switches between cockpit and chase camera, F gets out.
- **G29/G923:** click **🎮 Connect wheel**. The wheel's rotation is set to the vehicle's steering, force feedback comes from the front tyres, and the rev lights are live. A pad works through the Gamepad API.

## Files
| File | What |
|---|---|
| `src/main.ts` | The Mock: loading, the player on foot and at the wheel, cameras, HUD, force feedback |
| `src/world.ts` | Gidi's city data in the sim's frame (metres, x east, z south, centred). Footprints for collisions, estate walls, the lane network, water, massing per tile, spawning |
| `src/tiles.ts` | Streams `web/city` tiles by distance. Rebuilds the kit's materials in TSL, with weathering from each vertex's wear |
| `src/signals.ts` | Visible traffic lights on the traffic's own signal clock |
| `src/trafficnet.ts`, `carphysics.ts`, `drive.ts`, `wheel.ts`, `g29.ts`, `input.ts`, `roadnet.ts`, `graphics.ts`… | From Real-world. Changes are marked "Gidi:". The changes are: Gidi's fleet and walkers, the LNT2 network (16-bit signal index), and the player wearing a kit model |
| `desktop/main.cjs` | Electron: serves the repo over `app://`, grants the Logitech wheel over WebHID, and has screenshot modes (`GIDI_SHOT`, `GIDI_MAPSHOT`) |
