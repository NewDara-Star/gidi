# Unreal port plan

Agreed with the owner on 15 Oct 2026.

## When
Once the map is final:
- all fifteen districts are built (done)
- the terrain and the hand-made Lagos-isms are in
- the 3D models we need have been touched up

**Wait until then.** The Unreal ground and road layout depend on the terrain and the isms.

## How
- **The data stays the master copy.** The generator and its files remain the source of truth: `web/gidi-data.js`, `web/gen-*.json`, and the terrain grid (`web/terrain.json`, in progress). Unreal assembles the world from them.
- **Meshes come from the Blender kit** (`blender/`), exported for Unreal: houses by style, kiosks, tanks, booths, vehicles, boats.
- **A one-time Unreal importer** (Unreal's PCG tools, or an editor Python script) reads the JSON and places the meshes:
  - buildings: footprint, kind, storeys and style
  - streets, lanes, paths, bridges and flyovers become splines
  - parcels and pins
- **The terrain** becomes an Unreal Landscape.
- **Gameplay data:** safe ground, okada ban zones and checkpoints become volumes or data layers the game logic can read. Unreal generates its own walking navigation (navmesh).
- **World size:** Gidi is about 9 × 7 km. World Partition streams it, and the ~29,000 buildings go in as instanced meshes.
- **Hand work in Unreal goes on top:** hero buildings, interiors, set pieces. The city itself is not placed by hand.

## Things to remember
- **Changes don't flow live.** A map change reaches Unreal only when the importer is re-run.
- **Coordinates:** the map is in metres with y running south. Unreal uses centimetres and its own axes, so the importer scales and flips once.
- **Not ported:** the browser 3D view (three.js) is a viewer only. Materials, lighting and weather are redone properly in Unreal.
