# Look test: Ladi Lane in two styles

Art-direction test, not production. Same map data (`area.json`, the Ladi Lane opening area), same kit, same camera spots, two looks:

- **A, stylized clean:** bright low-poly, chunky shapes, flat colours, soft shadows, blue sky with clouds, tidy kerbs and wires.
- **B, stylized gritty:** the same shapes and palette plus Lagos wear: a grime shader (rain streaks, stains, red mud splash, chalky uneven paint, rust on roofs and metal), open drains, wire tangles, litter, puddles, unfinished storeys with rods, hand-painted signs, wall writing and posters, a denser crowd.

Open `ladi-lane-look.html` (one self-contained file) and use the A/B switch, the five camera buttons and Dusk.
Every model is built in code (`src/kit.js`); no downloaded models or images; every name and brand is invented.

| File | What |
|---|---|
| `src/kit.js` | Geometry batcher + kit: bevelled walls, framed windows with burglar bars and louvres, doors, shop shutters, corrugated roofs, rounded people (instanced), danfo, okada, keke, car |
| `src/world.js` | Lays the kit on the map data in three layers: common, clean-only, gritty-only |
| `src/main.js` | Grime shader + baked contact AO, sky, clouds, sun shadows that follow the camera, dusk bloom, crowd, traffic, cameras, UI |
| `src/tex.js` | Canvas textures: sign atlases (clean and hand-painted), ankara print, roof ridges, AO map |
| `build.py` | Bundles into `ladi-lane-look.html` |
| `shoot.js` | Matching screenshots: `NODE_PATH=~/node_modules node look/shoot.js [views] [a,b] [day|dusk]` |
