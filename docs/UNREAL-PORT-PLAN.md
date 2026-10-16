# Unreal port plan

Agreed with the owner on 15 Oct 2026.

## When
**Updated 16 Oct 2026 (owner): the map will never be final.** Gidi gets tweaked until the game ships, so Unreal can't wait for a final map. It's one more view of the same data, rebuilt whenever the data changes. The loop is:
1. **Change the data.** The map, the hand files, the kit.
2. **Look in the browser first.** The 2D map and the three.js 3D view: fast, to try things.
3. **Mock up in Blender.** Renders of new looks and buildings.
4. **Reimport into Unreal.** That's where the real game is built.

Unreal work still starts only when the owner says go (`decisions/DECISIONS.md`). When it does, the importer must be re-runnable from day one, not a one-time port.

*Superseded (15 Oct): "Once the map is final… wait until then."*

## How
- **The data stays the master copy.** The generator and its files remain the source of truth: `web/gidi-data.js`, `web/gen-*.json`, and the terrain grid (`web/terrain.json`, in progress). Unreal assembles the world from them.
- **Meshes come from the Blender kit** (`blender/`), exported for Unreal: houses by style, kiosks, tanks, booths, vehicles, boats.
- **A re-runnable Unreal importer** (Unreal's PCG tools, or an editor Python script) reads the JSON and places the meshes, every time the data changes:
  - buildings: footprint, kind, storeys and style
  - streets, lanes, paths, bridges and flyovers become splines
  - parcels and pins
- **The terrain** becomes an Unreal Landscape.
- **Gameplay data:** safe ground, okada ban zones and checkpoints become volumes or data layers the game logic can read. Unreal generates its own walking navigation (navmesh).
- **World size:** Gidi is about 9 × 7 km. World Partition streams it, and the ~29,000 buildings go in as instanced meshes.
- **Hand work in Unreal goes on top:** hero buildings, interiors, set pieces. The city itself is not placed by hand.

## Things to remember
- **Changes reach Unreal on reimport.** Make that one click, or automatic when the data files change.
- **Never hand-edit in Unreal what the data owns.** A reimport wipes it. Map fixes go into the data (the hand files); Unreal-only work goes on its own layers that a reimport never touches: lighting, mission triggers, cutscene sets, interiors.
- **Materials:** Unreal owns them once we move. Models carry only a material name, and Unreal looks it up in its library. Until then, Blender's materials are the reference.
- **Coordinates:** the map is in metres with y running south. Unreal uses centimetres and its own axes, so the importer scales and flips once.
- **Not ported:** the browser 3D view (three.js) is a viewer only. Materials, lighting and weather are redone properly in Unreal.

## Notes from the kit side
Added after the porting conversation on 15 Oct 2026.
- **Meshes: a variant library, or each building's own mesh.** The kit styles every building from its data, seeded, so it always comes out the same. The importer can take either:
  - a library of variants per kind and style that Unreal instances. This is light, suits World Partition, and is what "houses by style" above means.
  - each building's own mesh, exported from the kit. This matches the browser view exactly but is much heavier.
  Pick per kind if needed: instance the common houses and shops, and export landmarks and hero buildings as their own meshes.
- **Export format:** FBX or USD from Blender, without Draco compression. The browser tiles use Draco; it isn't certain Unreal's glTF importer reads it, and FBX/USD is the safer route. Weld vertices and make LODs, or rely on Nanite: the full-detail build runs to 5–7M triangles per 400 m tile, which Nanite handles.
- **Materials:** about 20 master materials, rebuilt in Unreal by the kit's names (paint, concrete, block, zinc, steel, glass, glass_lit, wood, asphalt, mud, water, emit, lamp, …).
  - Colour comes from the vertex colour, and the weathering amount from its alpha. This is how the browser view and the old Mock rebuilt them.
  - At night, `glass_lit` windows and `lamp` heads switch on.
- **Instanced assets and a placement file.** Export the repeated things once each: vehicles, boats, trains, people, street lights (and their banners), signs, gantries, billboards, traffic lights, trees, monuments. `blender/city.py` already computes where each one goes, so add a placement export (JSON: asset, position, heading, variant seed) for the importer.
  - The site lists are `ROADSIDE`, `MONUMENTS`, `BOATS` and `LAMPS`, plus the traffic still per road.
- **The browser tiles are not for Unreal.** `web/city/` holds merged 400 m meshes made for the three.js viewer. The importer places kit assets from the data instead.
- **Behaviour is built in Unreal:**
  - traffic and pedestrians (for example Mass AI and ZoneGraph, from the road data)
  - signals from `signals` in the data, once the 2D pass adds them
  - the day and night cycle
- **Terrain:** when `web/terrain.json` lands, `blender/city.py` (and the browser view) should read it too, so the 3D view tests the terrain the same way it tests the 2D map before the port. The kit builds on flat ground today.
- **Before porting:**
  - run `scripts/audit3d.py` for the whole city, with the hand fixes done
  - M1 to M3 must be at 0 for every district, so nothing the importer meets lacks a mesh
