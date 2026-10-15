# Gidi ground catalogue: roads in every condition, drains, ground, water, vegetation, refuse

This catalogue covers the honest Lagos: roads that are mud with potholes of water, mushy laterite lanes, failed asphalt, choked drains. It builds on `docs/look/research-street.md` §1 and §6.7–6.9, and does not repeat what is there: road widths by class, kerb paint colours, median types, basic drain sizes, basic pothole density, the tree census. It goes deeper on **condition** and on **how to select it from data**.

Rule zero: this studies real Lagos to build Gidi. No real road, estate or brand is copied. Real places are named only as examples of a pattern.

Tags:
- **[src]** means a listed source supports the figure.
- **[est]** means an estimate from Lagos photo and press imagery and general road-engineering practice. Most condition numbers are [est]. Lagos publishes no condition survey.

Hex values are weathered colours seen in photos, not paint-chart values.

Character keys used in SELECT BY (from `blender/gidi_kit/rules.py`):
- `dense`: Maze, Hub, Jungle, Food Gate, Bazaar.
- `sprawl`: Railside, Frontier, Border.
- `old_island`: Old Island, Old Shore.
- `elite`: Estate, Heights.
- `civic`: Capital.
- `waterfront`: Water Town.
- `port`: Port.

---

## 0. Summary

### 0.1 Items
| # | Item | Kind | Most common where | Model as |
|---|---|---|---|---|
| R1 | New asphalt with markings | road surface | elite, civic, new mains | texture + decals |
| R2 | Worn asphalt | road surface | everywhere paved | texture |
| R3 | Patched asphalt | road surface | dense mains, streets | decals + 1–3 cm relief |
| R4 | Potholed asphalt | road surface | dense, sprawl, port | geometry (cut holes) + water planes |
| R5 | Failed / cratered road | road surface | port, sprawl, flood-low dense | geometry (terrain-like mesh) |
| R6 | Laterite road, dry | unpaved | sprawl, dense back lanes | displaced mesh + dust |
| R7 | Laterite road, wet (mud) | unpaved | sprawl, dense, low ground in rains | displaced mesh + wet shader + puddle planes |
| R8 | Sand road | unpaved | old_shore, waterfront, elite back plots, Lekki-like | soft displaced mesh |
| R9 | Interlocking paver street | road surface | elite, civic, flood-prone fixes | texture + sink/break geometry |
| R10 | Concrete-slab street | road surface | expressways, estate roads, flood fixes | texture + joint decals + step faults |
| R11 | Road under construction | road state | anywhere, on mains | props + milled texture |
| R12 | Flooded street | road state (rainy) | flood-low districts | water plane + props |
| R13 | Erosion gully / washout | road state | slopes, sprawl, drain outfalls | geometry |
| R14 | Road edge breaking into drain | road edge | dense, sprawl, port | geometry |
| D1 | Open U-drain | drainage | all paved streets | geometry |
| D2 | Drain slabs (whole / broken / missing) | drainage | dense, old_island | instanced props |
| D3 | Choked drain | drainage | dense, markets | geometry fill + litter |
| D4 | Culvert | drainage | street crossings, compound gates | geometry |
| D5 | Canal | drainage | canal data | geometry + water |
| E1 | Kerbs (condition) | edge | mains | instanced |
| E2 | Medians (condition) | edge | mains | instanced |
| E3 | Speed bumps | road prop | residential, schools, estates | geometry |
| E4 | Markings and zebras | decal | mains, elite | decals |
| E5 | Sidewalks or none | edge | all | geometry |
| E6 | Shoulders used for trading/parking | edge | dense mains, bus stops | props |
| G1 | Compound floor | ground | every plot | texture |
| G2 | Sand yard | ground | old_shore, sprawl, waterfront | texture |
| G3 | Concrete apron | ground | dense, elite, civic | geometry |
| G4 | Red earth by area | ground | mainland north | texture palette |
| G5 | Grass verge | ground | elite, civic, mains | texture + scatter |
| G6 | Bush on empty plots | ground | sprawl, Lekki-like | scatter |
| G7 | Wetland / swamp | ground | low ground | water + scatter |
| G8 | Lagoon shore | ground | waterfront, port | geometry |
| G9 | Beach and erosion | ground | Old Shore-like coast | geometry |
| G10 | Sand-filled reclaimed land | ground | Heights, Lekki-like edges | texture |
| V1–V8 | Trees, palms, plantain, bamboo, grass, weeds | vegetation | see §5 | instanced + scatter |
| W1–W4 | Refuse heaps, bins, burning, scavengers | refuse | see §6 | props + particles |

### 0.2 The selector, in one line
For each road segment the kit should compute **one condition score** and **one wetness state**, then pick everything from those two numbers:

```
cond  = base[road_class][character] + wealth_bonus - truck_load - flood_low*0.3 - years_since_repair*decay
wet   = season (dry | early_rain | peak_rain | after_storm) x low_ground x drain_state
```

§7 gives the tables to fill these in.

---

## 1. Road surfaces

### R1. New asphalt with markings
- **Looks like:**
  - Uniform near-black, slightly glossy, with fine aggregate texture.
  - Fresh white or yellow paint, crisp edges. Thermoplastic paint shows as slightly raised.
  - Edges are a clean line against fresh painted kerbs. Black/white or yellow/black kerbs are freshly repainted at the same time.
  - In Lagos this lasts 1–3 years on busy mains before patching begins [est]. It often stops abruptly at an LGA or estate boundary, where worn road resumes.
- **Kit parts:**
  - Road mesh with an asphalt material: noise-based aggregate plus a micro-roughness map.
  - Decal strips:
    - Lane dashes 3 m long with 6–9 m gaps, 0.12 m wide (see research-street §1.1).
    - Edge lines 0.15–0.2 m.
    - Zebras (E4).
    - Arrows.
    - "SLOW", "BUS STOP" and "BRT ONLY" text in yellow on BRT lanes.
  - Cat's eyes are rare: about 1 per 18 m on showpiece roads only [est].
- **Colours:**
  - Fresh asphalt `#232322`.
  - After 6 months `#2E2E2C`.
  - White paint `#F1F0EA`.
  - Yellow `#F2C230`.
  - Tyre tracks are darker `#1C1C1B`, 0.25 m wide pairs at about 1.6 m spacing in each lane.
- **Condition states:**
  - New: as above.
  - Year 1–2: the colour lifts to `#3A3A38` and paint wears in the wheel paths.
  - Then it becomes R2.
- **Props and life:**
  - Lane-flouting danfos, LASTMA-style traffic officers at junctions, roadside flex banners announcing "commissioned" roads.
  - Night: streetlights work for the first months, sodium-orange or white LED.
- **SELECT BY:**
  - `elite` streets: about 60% of segments.
  - `civic` mains: about 50%.
  - New expressway or BRT corridor: about 70%.
  - `dense`: about 10% (a recently rehabilitated main only).
  - `sprawl`: 5%.
  - Use a `years_since_repair` < 2 flag.
- **Gidi mapping:** `mains` (all districts), `streets` in Estate, Heights and Capital.

### R2. Worn asphalt
- **Looks like:**
  - Faded grey surface. The fine binder has gone, so coarse stone shows (ravelling).
  - Long cracks follow the wheel paths. Fatigue "crocodile" cracking forms blocks of 0.2–0.5 m in the outer lane [est].
  - Paint is 50–90% gone.
  - Edges crumble back by 0.1–0.5 m and a band of sand or red dust sits on the edge.
  - Oil blots at bus stops and mechanic spots.
- **Kit parts:**
  - Asphalt material with these masks:
    - a crack mask (Voronoi edges, thresholded),
    - a ravel mask (noise-lightened),
    - a wheel-path mask (two bands per lane),
    - an edge-dust gradient 0.3–1 m (`#C4703D` mainland, `#D8C9A3` island).
  - No geometry change except an edge break (R14).
- **Colours:**
  - Grey `#5E5C57`.
  - Very worn `#6F6B63`.
  - Crack lines `#2A2826` with weed green `#6E8A3A` growing in them on low-traffic streets.
  - Oil blots `#24211E`, round, 0.3–1.5 m.
- **Variants:** ravelled 40%, crocodile-cracked 35%, rutted (wheel-path depressions 2–5 cm, R4-lite) 25% [est].
- **SELECT BY:** the default for paved streets aged 3–10 years since repair. Rutting is likelier on truck routes (`port`, `mains`).
- **Gidi mapping:** `streets`, `mains` in all characters except waterfront plank areas.

### R3. Patched asphalt
- **Looks like:**
  - Darker rectangles and blobs on faded grey. Official patches are sharp-cut rectangles 1–6 m long. Informal patches are irregular.
  - Patch types:
    - **Hot-mix patch** (official): black `#2B2B29`, cut rectangle, flush or 1–2 cm proud.
    - **Cold-mix or "palliative"**: slightly grainy, often sunken 1–3 cm after a season.
    - **Concrete patch**: pale `#9C988E` rectangle, common on failed spots in low ground.
    - **Interlocking-stone patch**: a rectangle of grey pavers set into asphalt. The Lagos public works corporation uses pavers as a wet-season repair because hot premix is unsuitable in rain [src ThisDay 2022, Vanguard 2015].
    - **Community fill**: broken blocks, stones, sand and laterite heaped into potholes by residents or by young men collecting tips [src Guardian Ago Palace]. Lumpy, 5–15 cm proud at first, then washed out.
  - After 1–2 rainy seasons, the patch edges crack again and potholes reopen at the patch seam.
- **Kit parts:**
  - Patch decal library with a height offset:
    - 8 rectangles (1×1 to 2×6 m),
    - 6 blobs,
    - a paver patch tile set,
    - a rubble-fill mound mesh (0.5–2 m diameter, 0.05–0.15 m high, broken block chunks 0.1–0.2 m plus gravel).
- **Density [est]:**
  - Patched share of length: dense mains 20–40% (as in research-street), dense streets 10–30%, elite 0–10%.
  - Patch count per 100 m: 3–15 on dense mains.
- **Condition states:**
  - Fresh: high contrast.
  - Aged 1 yr: patch fades to `#3D3C39`, still darker than the surround.
  - Failing: the seam opens into a pothole.
- **Props and life:**
  - Informal fill crews with shovels, a wheelbarrow and a bucket held out for tips.
  - An official crew with an orange or yellow tipper, a hand roller, and cones made of tyres or plastic drums.
- **SELECT BY:**
  - `years_since_repair` 2–8.
  - Wealth 0.2–0.6.
  - Paver patches on `flood_low` segments.
  - Rubble fill on streets and lanes with wealth < 0.3.
- **Gidi mapping:** `mains`, `streets`.

### R4. Potholed asphalt
- **Looks like:**
  - Bowl-shaped holes with ragged, vertical-ish asphalt edges. The broken edge shows a 4–8 cm asphalt layer over a pale laterite or stone base.
  - Holes cluster in wheel paths, at drain edges, at bus stops, and where water stands.
  - In the rains they fill with brown water and drivers cannot see the depth. Potholes "disappear beneath floodwater", which makes them more dangerous [src Guardian Oshodi-Isolo].
  - Vehicles weave to dodge them, so a pothole field slows traffic to walking pace.
- **Pothole size classes:**

  | Class | Diameter | Depth | Share |
  |---|---|---|---|
  | Small | 0.2–0.5 m | 3–8 cm | 50% |
  | Medium | 0.5–1.5 m | 8–20 cm | 35% |
  | Large | 1.5–4 m | 15–40 cm | 13% |
  | Merged field | 4–15 m long | 10–40 cm | 2% |

  - Sizes and shares are [est]. Engineering severity classes, used to set depth bands, are low < 25 mm, moderate 25–50 mm, high > 50 mm [src FHWA LTPP distress manual]. Lagos holes on neglected roads are mostly "high".
- **Density per 100 m of carriageway [est]:**
  - Refines research-street §1.6 by state:
    - Well-kept: 0–1.
    - Neglected street: 5–15.
    - Failing main: 10–30, with merged fields.
- **Water-filled share:**
  - Dry season: 0–10% (only after a shower).
  - Early rains: 30–50%.
  - Peak rains (June and Sept–Oct): 70–100% [est].
  - Water level is 0–5 cm below the rim. The surface is flat brown.
- **Kit parts:**
  - Boolean or displacement cut into the road mesh:
    - rim ring with a jagged profile,
    - inner bowl,
    - floor of loose gravel (`#8E8579`) and laterite mud (`#8A4B2A`).
  - A water plane clipped to the bowl when wet.
  - A splash/ripple decal ring on the far side (tyre spray).
  - Model holes larger than 0.5 m as geometry. Smaller ones can be normal-map plus parallax.
- **Colours:**
  - Rim asphalt `#3A3936`.
  - Exposed base `#B08A5C` (stone base) or `#A0522D` (laterite).
  - Water:
    - laterite areas `#7A5A3A`,
    - sand areas `#7E7462`,
    - after rain, a sky reflection with a muddy tint `#8B7A62`.
- **Props and life:**
  - Okadas and kekes threading the gaps.
  - A danfo tilted 10–15° as one wheel drops in.
  - Splashed pedestrians.
  - A stick or tyre placed in a deep hole as a warning.
  - A branch with a red cloth stuck in a hole.
- **SELECT BY:**
  - Inverse condition score.
  - Multiply density by truck load (`port` ×2–3, `mains` ×1.5) and by `flood_low` (×1.5).
  - Water fill by season.
- **Gidi mapping:** `mains`, `streets`, `lanes` with paving.

### R5. Failed / cratered road (asphalt mostly gone)
- **Looks like:**
  - Less than 30% of the asphalt survives, as islands and slabs with broken edges. The rest is a basin of laterite, stone base, mud and water.
  - Craters 3–10 m wide and 0.3–1 m deep. On truck routes, "gullies too deep for SUVs" with silted drains leaving pools [src ThisDay Apapa].
  - Trucks capsize trying to cross craters at speed [src ThisDay Apapa]. Trucks get stuck in flooded bad sections [src Guardian LSPWC].
  - Residents fill the worst parts with stones and broken blocks after rain [src Guardian Ago Palace].
  - Traffic uses whichever side is shallower, including the wrong side and the shoulder. The road becomes a braided set of tracks.
- **Kit parts:**
  - Treat as terrain: a displaced grid (0.25 m resolution) with these layers:
    - asphalt islands (planar fragments 0.5–4 m, 6 cm thick, broken edges),
    - crater bowls (noise + Voronoi),
    - puddle/lake planes per bowl,
    - rubble mounds,
    - tyre-track ruts.
- **Dimensions:** craters 3–10 m [est]. Standing-water lakes span the full road width, 10–40 m long, 0.2–0.6 m deep [est].
- **Colours:**
  - Mud `#7B4A2A`.
  - Wet laterite `#8C4426`.
  - Base stone `#A99A86`.
  - Asphalt fragments `#45433F`.
  - Lake water `#6E5638`.
  - Truck-oiled mud `#3C332A`.
- **Variants:**
  - Truck-churned (`port`, mains to markets).
  - Washout (water-cut, see R13).
  - Abandoned reconstruction: base layer laid then abandoned; buses avoid it [src Gazette Ikorodu].
- **Props and life:**
  - Stuck trailer with others queued behind, a tipped container, a boy directing traffic for coins.
  - Pushers getting a car out of mud.
  - A broken-down danfo with its bonnet up.
  - Wheelbarrow water and sachet sellers.
  - At night: no lights, so headlights rake the water.
- **SELECT BY:**
  - Condition score < 0.15.
  - `port` mains near the gate: 20–40% of length.
  - `sprawl` streets: 5–15%.
  - `dense` flood-low streets: 5–10%.
  - `elite`: 0% (except a Lekki-like rough stretch outside the estate gate, 2%).
- **Gidi mapping:** Port `mains` (truck park, container yard approaches), Railside and Frontier `streets`, Jungle flood streets.

### R6. Laterite road, dry
- **Looks like:**
  - Red-orange compacted earth, camber barely visible.
  - Two to three bands of tyre ruts, 3–10 cm deep, with a raised crown between them.
  - Loose dust at the edges and in the ruts. Dust plumes behind every vehicle and red dust coats walls, plants and parked cars up to 1 m high.
  - Washboard corrugation (0.5–0.8 m wavelength, 1–3 cm high) on stretches used by fast okadas [est].
  - Exposed stones and old dried-mud rut casts from the last rainy season.
- **Kit parts:**
  - Road mesh:
    - displaced rut channels per wheel line,
    - noise mounds,
    - a corrugation sine along the length (optional),
    - a scatter of 2–8 cm stones.
  - Dust layer: a lighter overlay on edges, walls and parked vehicles (vertex colour on nearby objects to 1 m height).
  - Dust particle card emitter behind vehicles.
- **Width:** lanes 3.5–6 m, streets 6–9 m incl. the walkable edge [est].
- **Colours (dry):**
  - Surface `#C4703D`.
  - Dusty top `#C9926A`.
  - Rut floor (compacted, darker) `#AE5E33`.
  - Dust on walls `#C58A63` at 30–60% blend.
  - Sun-bleached `#D3A07A`.
- **Variants:**
  - Graded (machine-flattened, smooth, after a council grade): 20%.
  - Rutted: 60%.
  - Stony / eroded: 20% [est].
- **Condition and ageing:** graded → rutted within one season → stony with gullies after 2–3 seasons.
- **Props and life:**
  - Okadas dominant, kekes, a tipper with sand.
  - Women sweeping the frontage.
  - Children playing football on the dry road.
  - Harmattan haze (Dec–Feb) makes everything paler.
- **SELECT BY:**
  - `sprawl` lanes: 70% unpaved (research-street).
  - `sprawl` streets: 50–70% unpaved.
  - `dense` back lanes: 20–30%.
  - Season = dry.
  - Mainland north (higher ground) uses red. The coast uses sand (R8).
- **Gidi mapping:** `lanes`, `streets`, paths `cut-through` and `worn crossing` in Railside, Frontier, Border, Bazaar, parts of Maze and Food Gate.

### R7. Laterite road, wet (mud): "very mushy roads"
- **Looks like:**
  - Same road, now dark red-brown and glossy.
  - Ruts deepen to 10–40 cm and fill with water. Puddles often span the **whole width** for 5–30 m.
  - The surface is slick clay. Okadas slide and people walk on the house frontages, on planks, or on stones laid as stepping stones.
  - Commercial vehicles stop using the road and fares rise [src Gazette Ikorodu, ICIR Ikorodu].
  - After a heavy storm: a sheet of orange-brown water crossing the road, carrying sand. Afterwards, sand fans at low points.
  - A day after rain: the edges dry to a crust while the ruts stay full of mud for days.
- **Kit parts:**
  - Same mesh as R6 with these changes:
    - rut depth ×3,
    - puddle planes in every depression (fill to the threshold height),
    - a wet shader (roughness 0.15–0.3, darkened albedo ×0.6),
    - tyre-track decals in mud (tread print, 0.2 m wide),
    - footprints,
    - plank, stone and block stepping-path props along the edges.
  - Optional "trapped vehicle" set piece: a car or danfo sunk 0.2–0.4 m at one axle, with mud spatter up the sides to the windows.
- **Colours (wet):**
  - Mud `#8B4A2B`.
  - Saturated `#7A3E22`.
  - Puddle water `#9A6A42` (opaque, clay-laden, like milky tea with paprika).
  - Splash marks on walls `#9C5A35` up to 0.6 m.
  - Shiny highlights.
- **Variants:** soft mud 50%, ponded (water across the width) 35%, washed-out (R13) 15% [est].
- **Props and life:**
  - Pushers ("help us push") of 3–6 young men.
  - Women with wrappers hitched and slippers in hand.
  - Children with wet uniforms.
  - Planks laid across the low spot.
  - A sand or laterite heap dumped by residents to raise a spot.
  - Kekes with mud to the canopy.
  - At night: mosquito season, frogs.
- **SELECT BY:**
  - Unpaved road AND season ∈ {early_rain, peak_rain, after_storm}.
  - Ponding share rises with `flood_low` and falls with slope.
  - `sprawl` low ground (Alimosho- and Ikorodu-like) is the worst.
- **Gidi mapping:** same as R6, wet-season state.

### R8. Sand road (island and coast)
- **Looks like:**
  - Pale grey-beige loose sand. There are no crisp ruts: the tracks are wide, soft, blurry troughs.
  - Cars dig in and spin. Pedestrians sink to the ankle.
  - In the rains it drains fast (puddles are rarer than on laterite) but scours into small channels. Where the water table is high, black-grey wet sand and standing water sit in hollows for weeks.
  - Shells, coconut husks and palm fronds lie on it near the coast.
  - Often the "road" to a new estate or beach is a sand track between fences.
- **Kit parts:**
  - A soft displaced mesh (low-frequency trough noise), sand ripple normal map, scattered husks and fronds.
  - Wet variant: a darker band where the water table is near the surface.
- **Colours:**
  - Dry `#D8C9A3`, grey `#BFAE8A`, near-white beach sand `#E3D8BD`.
  - Wet `#8F8670`, black-organic wet `#4A453A`.
- **SELECT BY:**
  - Coast and lagoon characters (`old_island` Old Shore, `waterfront` landward lanes, `elite` new plots and Heights-like back plots).
  - Low ground near the lagoon with no laterite import.
  - Lanes and unpaved streets in these districts: 60–90% sand, not laterite.
  - Laterite still appears where a road has been "improved" with trucked-in red earth: a red stripe on pale ground. This is very Lagos [est].
- **Gidi mapping:** Old Shore and Water Town `lanes` and `streets`, Heights and Estate edges, parcels `villas` (construction), beach access.

### R9. Interlocking paver street
- **Looks like:**
  - Grey concrete pavers in I/dog-bone, S or rectangular shapes, 60–80 mm thick, herringbone or stretcher bond. Some streets add a red or charcoal border band.
  - Used on estate roads, government frontages, flood-prone streets, and as patches. Lagos chose permeable interlocking paving for a marshy Victoria Island street to resist groundwater intrusion [src Ojuri 2012]. The public works corporation lays them in the rains [src ThisDay 2022, AllAfrica 2026].
  - How they fail:
    1. Sand washes out of joints and weeds grow in the joints.
    2. Wheel-path rutting and a dish of 3–10 cm where the base is soft.
    3. Edge pavers break loose where there is no kerb restraint.
    4. A sunken bowl 1–4 m across over a soft spot or failed drain, holding water.
    5. Pavers pulled up, stacked or stolen, leaving a pit of sand. Utility trenches are patched with concrete or sand.
    6. Broken corners and cracked pavers under trucks.
- **Kit parts:**
  - Paver texture (tileable, per shape), border band, kerb restraint.
  - Geometry:
    - sink bowls (vertex displacement on a subdivided plane),
    - a missing-paver patch (holes plus a loose stack prop of 10–40 pavers),
    - a raised lip where a root lifts them.
  - Joint weed scatter.
- **Paver dimensions:**
  - I-shape about 225×112×60/80 mm.
  - Rectangle 200×100×60/80 mm.
  - Hexagon about 200 mm across.
  - All [est], standard West African catalogue sizes.
- **Colours:**
  - Grey `#8E8B84` → worn `#7C7870` → dirty `#6A665E`.
  - Red `#8A4B3A`.
  - Charcoal `#4A4A48`.
  - Joint sand `#C9B98F`.
  - Joint weeds `#5E7F2E`.
  - Algae in shade `#4E5A3A`.
- **Condition states:**
  - New: uniform and flat.
  - Worn (3–6 yr): rutted, joints weedy, oil stains.
  - Decayed: bowls holding water, broken edges, 5–20% missing.
  - Abandoned: grass grows through, a sand mound.
- **SELECT BY:**
  - `elite` streets: 30–40%.
  - `civic` streets: 30%.
  - `dense` streets that have been "fixed": 10–20%.
  - Any segment that is `flood_low` with a repair in the last 5 years: ×2 chance.
  - Sidewalks on new corridors (research-street §1.4).
- **Gidi mapping:** `streets` in Estate, Heights, Capital; patch decals elsewhere; parcels `forecourt`, `plazas`, `square`, `government`.

### R10. Concrete-slab street
- **Looks like:**
  - Pale grey rigid pavement in bays 4–6 m long with sawn or tooled joints and a broom-finished surface.
  - Lagos uses it on rebuilt expressways (Lekki-Epe-like, Ikorodu-road-like reconstructions converted to continuous reinforced concrete pavement) [src VON via research-street; Nairametrics Ketu–Mile 12]. Small versions appear on estate roads and on low ground where asphalt keeps failing.
  - How it ages:
    - joint sealant lost, so grass grows in joints;
    - corner breaks;
    - step faulting 1–3 cm between bays;
    - black tyre-rubber and oil stains;
    - on old slabs, exposed aggregate.
  - Informal versions: community-cast concrete strips in a lane, often only the two wheel tracks (2 × 0.6–0.8 m) with sand between them.
- **Kit parts:**
  - Slab texture (broom lines across), joint decal grid, a corner-break decal and mesh chip, a step offset per bay (random 0–3 cm).
  - Wheel-track strip variant for lanes.
- **Colours:**
  - New `#B4B1A9`.
  - Weathered `#9A9890`.
  - Dirty `#87837A`.
  - Joints `#3E3C38`.
  - Rubber marks `#3A3836`.
- **SELECT BY:**
  - Expressways and new BRT corridors.
  - `elite` and `civic` estate roads: 10–20%.
  - `flood_low` dense streets with a recent fix: 5–10%.
  - Wheel-track strips: `sprawl`/`dense` lanes, 5%.
- **Gidi mapping:** expressway `mains`, `structures` ramps/flyovers (deck surface), some `lanes`.

### R11. Road under construction
- **Looks like:**
  - Half the carriageway closed; traffic squeezed onto the other half or onto a service lane. Diversions run for weeks to months; a Lagos main road diversion for repair ran 90 days [src TheCable Ikorodu Road], others two to four weeks [src Nairametrics Ojota, Channels].
  - Construction stages:
    1. Milled surface: grooved grey, 2–5 cm lower, with a step at the edge.
    2. Excavated to laterite.
    3. Stone base layer.
    4. Primed black, with sand thrown on.
    5. New asphalt or concrete.
  - Piles on the shoulder:
    - laterite cones 2–4 m high,
    - granite chippings (grey `#8F8C86`),
    - sharp sand (`#D2B98B`),
    - precast drain sections (U-sections 0.6–1.2 m),
    - kerb blocks,
    - stacked paver pallets.
  - Equipment: grader, roller, excavator, tipper trucks, a bitumen boiler.
  - Barriers:
    - plastic water-filled barriers in red/white or orange/white,
    - concrete blocks,
    - painted drums,
    - tyre stacks,
    - hand-made "ROAD CLOSED / DIVERSION" signs on plywood.
  - Abandoned construction is common. The site freezes at a stage: piles grassed over, barriers knocked over, and the excavated road becomes R5/R7 in the rains [src Gazette Ikorodu].
- **Kit parts:**
  - Milled texture (parallel grooves 1.5 cm pitch), excavated mesh, pile meshes (cone with noise).
  - Barrier set: 1.0–1.2 m long, 0.8 m high plastic units; 0.6×0.6×1.2 m concrete blocks.
  - Signboard 1.2×0.8 m on posts.
  - Machinery instances.
  - A project billboard (generic: government crest + "rehabilitation of …").
- **Colours:**
  - Milled `#6D6A64`.
  - Prime `#1E1D1B` with a shine.
  - Barriers red `#C8302A`, white `#EEEDE8`, orange `#E5752A`.
- **Variants:** active 40%, paused 30%, abandoned 30% [est].
- **Props and life:**
  - Workers in reflective vests.
  - Traffic wardens.
  - Hawkers exploiting the slow traffic.
  - Okadas riding on the piles.
  - Night: one floodlight, or none.
- **SELECT BY:**
  - Seeded: 1–3 segments per district (2–5% of main length).
  - Higher on `mains` and in `civic`/`elite` (active).
  - `sprawl` (abandoned).
  - Dry season (active works). In the rains: paused or abandoned.
- **Gidi mapping:** `mains`, `streets`; ties to `structures` (flyover ramps).

### R12. Flooded street
- **Looks like:**
  - Flood depths by stage (the **flood ladder**):

    | Stage | Depth | What you see |
    |---|---|---|
    | 0 Wet | film | Shiny road, puddles in potholes and ruts |
    | 1 Ponding | 0–10 cm | Drains full, water at the kerb, potholes invisible |
    | 2 Ankle | 10–20 cm | Kerb-to-kerb water, bow waves from cars, traders lift goods |
    | 3 Knee | 30–50 cm | Cars stall and are abandoned; people wade with shoes in hand; water enters ground-floor shops and churches [src AFP/Inhabitat, Kola King, Radio Nigeria] |
    | 4 Wheel-half | 30–40 cm on car scale | A car can be swept off: "once the rainwater gets to half of the wheels it sweeps off your vehicle" [src NEMA via TheCable] |
    | 5 Thigh/waist | 60–100 cm | Estates "fully submerged"; canoes and kids on tyres; cars submerged to the windows [src TheCable Lekki photo, Zikoko] |

    - Stage 3 is the common bad day. Stage 5 happens in a few low estates per year [est].
  - **Water colour:**
    - laterite districts: opaque orange-brown `#8A6A45`;
    - sand districts: grey-brown `#6E6450`;
    - drain-fed water near markets: dark grey-green `#4F5A3C` with a scum line.
  - **Debris:**
    - floating sachets and bottles drifting to the edges in drifts,
    - nylon bags,
    - Styrofoam,
    - a flip-flop,
    - water hyacinth near canals,
    - foam lines.
  - **After it drains:**
    - a mud and silt layer 1–5 cm (`#7A6A55`),
    - a refuse wrack line on walls and fences at peak height,
    - a water stain line on walls (`#6B5D4B`, 2–5 cm band),
    - sandbags,
    - ruined goods drying outside.
- **Kit parts:**
  - A global water plane per low basin, height = stage depth over local terrain. Use a flow-noise normal map, an opacity ramp (opaque in laterite districts), floating litter instances, and wading-people poses.
  - Stalled vehicle set pieces: car with bonnet up, a danfo at an angle, a truck that keeps going and makes a bow wave.
  - Post-flood decal set: silt layer, wrack line, wall stain.
- **Life:**
  - Wading people with goods on their heads.
  - Boys charging to carry people across on their backs or on planks.
  - Canoes in the street at stage 5.
  - Kids swimming.
  - Traders bailing shops.
  - Dark at night (power cut). Phone torches.
- **SELECT BY:**
  - Season ∈ {peak_rain, after_storm}.
  - Stage = f(district low-ground share, local depression, drain_state, distance to canal).
  - Gidi flood-prone districts per the data plan: **Old Island (99% below 5 m), Port 89%, Heights 87%, Jungle 85%, Water Town 84%, Food Gate 84%, Bazaar 77%**.
  - Driest: **Railside, Capital, Maze 50–52%** [src gidi-data-plan].
  - Suggested max stage on a bad day:
    - Old Island, Jungle, Water Town, Port: 3–5.
    - Heights, Estate (Lekki-like flooding of the rich, July 2024 [src Kola King]): 3–4.
    - Food Gate, Bazaar, Hub: 2–3.
    - Maze, Capital, Railside: 1–2 (local depressions only).
- **Gidi mapping:** all road kinds; districts' "flood days" events (Jungle `Canal 7`); `canal`.

### R13. Erosion gully / washout
- **Looks like:**
  - A channel cut by runoff along or across the road. It is V-shaped in laterite (vertical red walls) and U-shaped and wide in sand.
  - On slopes it runs along the lowest wheel path or the road edge. At a drain outfall it cuts back into the road as a headcut.
  - Roads have been "washed away", leaving craters [src Guardian drainage]. A collapsed portion cut a community off for months [src BusinessDay Gberigbe].
  - It exposes pipes, cable and old asphalt layers. Fences and wall footings undercut along it, and occasionally a building corner hangs.
  - Fixes: sandbags, stacked tyres, dumped refuse (used as fill!), broken blocks, and a plank bridge across.
- **Dimensions [est]:**
  - Rill: 0.1–0.3 m wide, 0.05–0.2 m deep.
  - Gully: 0.5–3 m wide, 0.5–2.5 m deep, 10–100 m long.
  - Washout across a road: 2–8 m.
- **Kit parts:**
  - A spline-swept channel with a noisy cross-section, vertical red walls with horizontal strata bands (`#B5562E` / `#C98B5A` / pale `#D6B48A`), a debris floor, an exposed PVC pipe (grey `#9FA3A6`), and a sandbag/tyre fix prop.
- **SELECT BY:**
  - Slope > 2% AND unpaved or failed (cond < 0.2) AND drain absent or choked.
  - Gidi terrain rises north, so Railside, Capital fringes and Bazaar slopes are prime.
  - Sand coasts get wide shallow scours, not gullies.
- **Gidi mapping:** `lanes`, `streets`, paths `cut-through`, `rail path` (embankment toes), drain outfalls into `canal`.

### R14. Road edge breaking into the drain
- **Looks like:**
  - The asphalt edge is undermined where the drain wall has failed or where water from the road pours over it. Bites 0.3–1.5 m into the carriageway and the edge drops 0.1–0.5 m.
  - A broken drain wall leans in. Its top slab is gone. A slice of road has slumped into the channel.
  - Vehicles keep 1 m off the edge, which narrows the road. A tyre or stick is planted as a warning.
- **Kit parts:**
  - An edge-bite boolean along the drain side (scalloped, 0.3–1.5 m), a tilted asphalt slab fragment in the drain, a fallen drain-wall section (block wall chunk), a warning tyre.
- **Frequency [est]:** dense streets 1–3 per 100 m; sprawl 2–5; elite 0.
- **SELECT BY:** paved road with a drain AND cond < 0.4 AND (drain_state = choked or broken).
- **Gidi mapping:** `streets`, `mains` with drains.

---

## 2. Drains, gutters, culverts, canals

### D1. Open U-drain
- **Looks like:**
  - A rectangular channel along one or both sides. Construction varies:
    - precast U-sections (smooth grey, in 1–2 m pieces with joints);
    - in-situ concrete;
    - sandcrete block plastered (rough, flaking).
  - A slab-covered strip often doubles as the "sidewalk".
  - Lagos drains form a disconnected network of shallow gutters [src Pulitzer, in research-street].
- **Dimensions:**
  - Standard precast sizes are 450×450, 600×600, 900×900 and 1200×1200 mm [src West African precast vendor; Indian schedules].
  - Wall thickness 100–150 mm on precast, 150–225 mm on block.
  - Street drains are mostly 450–600 mm; mains 900–1500 mm (research-street §1.5). Primary collectors run 1.5–3 m wide.
  - Freeboard to road edge 0–0.15 m.
- **Colours:**
  - New concrete `#B8B4AA`.
  - Weathered `#8F8B82`.
  - Black water line `#2F2E2A`.
  - Algae band `#5D6B3A`.
  - Silt `#3A3529`.
  - Rust streaks where rebar shows `#8A5530`.
- **Variants:**
  - Open both sides: dense mains.
  - One side: streets.
  - Earth ditch (V, unlined, grassy): sprawl.
  - Trapezoidal lined: on mains, larger.
  - Covered/grated: elite.
- **Condition states:**
  - New: crisp, dry floor or a trickle.
  - Worn: silt 1/4–1/2 full, chipped tops.
  - Decayed: walls cracked or leaning, joints open, grass on top.
  - Abandoned: fully silted, used as a plant bed.
- **SELECT BY:** research-street §1.5 for presence and cover; condition from cond and the drain_state seed. Earth ditch on `sprawl` unpaved.
- **Gidi mapping:** every `streets` and `mains` segment edge.

### D2. Drain slabs (cover)
- **Looks like:**
  - Precast reinforced slabs 0.6–1.0 m long × drain width + 0.1–0.2 m bearing, 0.1–0.15 m thick. Some have a lifting hole or two rebar loops.
  - Shop owners cast their own wider slab to make a forecourt.
  - Slab states:
    - Whole, level.
    - Tilted or rocking.
    - Cracked across.
    - Broken with rebar showing.
    - Missing, either stolen for rebar or never placed [src Guardian, in research-street].
    - Replaced by a plank or a sheet of corrugated iron.
  - People step over the gaps. At night these gaps are hazards.
- **Kit parts:** slab instance set (4 sizes × 5 states), a plank bridge 0.25×2 m, iron sheet, steel grating 1.0×0.5 m (elite).
- **Colours:** slab `#A39F95`, worn `#8B877D`, rebar `#6E4A2E`.
- **Share of covered length:** research-street. Within the covered stretch, state mix [est]:

  | Character | Whole | Broken | Missing/plank |
  |---|---|---|---|
  | `dense` | 60% | 20% | 20% |
  | `elite` | 95% | 4% | 1% |
  | `old_island` | 55% | 20% | 25% |

- **SELECT BY:** character + wealth; a slab is always present in front of shop doors (an access bridge) even on an otherwise open drain.
- **Gidi mapping:** frontages of `buildings` kind `front` with shops.

### D3. Choked drain
- **Looks like:**
  - The drain is filled 50–100% with a mix of black silt, sachets, nylon bags, PET bottles, Styrofoam, coconut husks, sand and grass.
  - Still water: grey-green with a sheen and a scum, or black. In the dry season it is a crusted dry bed with plastic in it. Mosquito larvae; smell (no geometry, but the life signals it: people hold noses).
  - Plants: grass, sedge and occasionally a pawpaw seedling growing on the silt.
  - De-silting heaps: black silt shovelled out onto the road edge in mounds 0.5–1 m, left to dry and often washed back in by the next rain. Very Lagos [est].
- **Kit parts:**
  - Fill mesh at 50–100% of drain height (noise top), litter scatter with a dense instancing of a sachet / bag / bottle library, a water plane with an algae shader, de-silt heap mounds along the edge, weed scatter.
- **Colours:**
  - Green water `#4F5A3C`.
  - Black water `#26241F`.
  - Scum `#7A8045`.
  - Silt `#2B2A24`, dried `#5A5246`.
  - Algae film `#6C7B37`.
- **SELECT BY:** drain_state = choked when (character ∈ {dense, old_island, port, waterfront}) and wealth < 0.4; near markets, bus stops, motor parks: ×2. De-silt heaps appear before the rains (Feb–Apr) and are seeded 1 per 100–300 m.
- **Gidi mapping:** drains near parcels `market`, `motor park`, `bus terminal`, `under bridge`, `lorry park`.

### D4. Culvert
- **Looks like:**
  - Where a drain crosses under a road, a gate, or a junction: a concrete pipe 0.45–1.2 m diameter, or a box culvert 0.6–2 m wide, with headwalls.
  - Inlets are often blocked with a refuse plug. Water backs up and floods the junction (stage 1–3).
  - At compound gates, small pipe culverts (0.3–0.45 m) or slabs.
- **Kit parts:** pipe ring, box mouth, headwall (0.2 m thick, 0.3 m above road), wingwalls, refuse plug.
- **Colours:** concrete `#9D998F`, interior black `#1E1D1A`.
- **SELECT BY:** every drain-to-road crossing; a refuse plug probability = choked-drain probability.
- **Gidi mapping:** `streets`–`mains` junctions, gates (`gates` data), `canal` crossings.

### D5. Canal (refuse, hyacinth)
- **Looks like:**
  - Concrete-lined trapezoids or rectangles 5–20 m wide (research-street), or earth banks with sandbag and block revetments.
  - Water is slow, dark green-brown, often barely moving.
  - Canals are choked with water hyacinth, weeds and refuse despite funding [src Guardian ecology fund]. Plastic, old tyres and debris visibly block flow [src Opinion Nigeria]. Hyacinth mats slow flow by 40–95% (cited secondhand [src Guardian]).
  - Residents and cleaners dump refuse straight in; a canal can be turned into a dumpsite [src Guardian Oke-Afa]. Night dumping by cart pushers [src Ripples].
  - The banks are lined with shanties, latrines on stilts over the water, fish traps, a footbridge of planks or a pipe.
  - Periodic dredging leaves black dredge spoil heaped along the bank, 1–2 m high.
- **Kit parts:**
  - Canal cross-section sweep (lined/earth), a water plane with a slow flow shader, hyacinth mat instances (rosette leaves, 0.2–0.4 m tall, lilac flower spikes `#A88BC9` occasionally), refuse rafts, a tyre instance, a plank footbridge, a stilt latrine, spoil heaps, a mesh trash boom (a line of floats) at some outfalls.
- **Colours:**
  - Water `#3E4A30` to `#4A4A32`.
  - Hyacinth leaves `#4E7A2E`, glossy.
  - Hyacinth mat seen from afar `#5C7F33`.
  - Dredge spoil `#2E2B25`.
  - Concrete lining `#8E8A80` with an algae band.
- **Variants:** lined clean (recently dredged) 15%; lined choked 45%; earth bank with shanties 40% [est].
- **SELECT BY:** `canal` data; choked share rises in `dense`, `waterfront`, `port`; recently dredged just before the rains in `civic`/`elite`.
- **Gidi mapping:** `canal` (Maze, Jungle), paths `canal path`, `pond`, `waterworks`.

---

## 3. Edges: kerbs, medians, bumps, markings, sidewalks, shoulders

Base specs are in research-street §1.2–1.7. This section adds condition and the gaps.

### E1. Kerbs, condition
- **Condition states:**
  - New: fresh paint, straight line.
  - Worn: paint faded 50%, black grime base, sand drifts against it.
  - Decayed: blocks chipped, 1 in 5 missing, buried under sand or silt to the top, broken by turning trucks at junctions.
  - Absent: the road edge just crumbles into earth.
- **Kit parts:** kerb instance with a 4-state material, a missing-block gap, a "buried" variant (only the top 3 cm shows).
- **SELECT BY:** as research-street + cond. Buried variant on sand districts.
- **Gidi mapping:** `mains`.

### E2. Medians, condition
- **Looks like (decayed):**
  - A raised kerb median with bare sand and trampled paths across it at each bus stop. A refuse heap at one end.
  - Traders' tables on it. Sleeping mats under a footbridge.
  - A New Jersey barrier knocked out of line, with a gap people step through.
  - Grass in the dry season goes `#A39466`.
- **SELECT BY:** research-street §1.3 with cond.
- **Gidi mapping:** `mains`.

### E3. Speed bumps
- **Local names:**
  - "Speed breaker" and "bump" are the everyday terms in Nigerian English [est].
  - "Sleeping policeman" is understood (British usage) [est].
  - "Gallop" for a speed bump was not confirmed in any source. Do not use it without a check by the owner.
- **Looks like:**
  - Most are community-made. Self-built bumps are widespread enough that Anambra banned unauthorised ones and the federal works ministry ordered hazardous ones off highways [src Gazette, Guardian, Ripples].
  - Official rubber bumps on Lagos estate roads wear out [src Guardian Aboru].
  - Community shapes:
    - **Asphalt hump:** a sharp mound.
    - **Concrete ridge:** steep, often with exposed stones.
    - **Rope or pipe:** a half-buried PVC pipe or rope across the road (cheap).
    - **Earth hump:** on laterite, a raised ridge of compacted earth, sometimes with a buried log.
    - **Paired/tripled ridges:** "rumble" sets, 0.5–1.5 m apart.
  - Paint is rare: yellow/black or white stripes when present.
- **Dimensions [est]:** height 0.08–0.25 m; base length 0.3–1.5 m; full road width or leaving a 0.5 m gap at the edge that okadas use.
- **Kit parts:** profile-swept hump meshes (5 profiles), a stripe decal, a scuffed-top variant (tyre-rubber black on the crest).
- **Placement:** within 20 m of schools, churches, mosques, estate gates, hospitals; 50–150 m apart on estate streets (research-street); 1–3 per street in dense residential areas [est].
- **SELECT BY:** street or lane (not mains or expressways); near POI kinds `school`, worship, `gates`; `elite` ×2 density, but neater (painted, rubber).
- **Gidi mapping:** `streets`, `lanes`, near parcels `school`, `gates` data.

### E4. Road markings and zebra crossings
- **Zebras:** white bars 0.5 m wide, 0.5 m gaps, 3–4 m long (crossing width) [est]. Rare in Lagos: outside schools in elite, near government frontages, and on some rebuilt corridors. Faded to ghosts elsewhere. People mostly cross at footbridges or anywhere.
- **Other markings:**
  - Yellow box-junction hatching (rare).
  - "STOP" text.
  - BRT yellow lane edge.
  - Diagonal hatching at gores (white, faded).
  - Kerb paint (E1).
- **Fade states:** crisp 100% → 60% (wheel paths gone) → 20% ghost → none. Repaint cycles are irregular and tied to events (commissioning, elections) [est].
- **SELECT BY:** `mains` all; zebras only at school/civic POIs, wealth > 0.5.
- **Gidi mapping:** `mains`, parcels `school`, `government`, `court`.

### E5. Sidewalks or none
- **Variants by share [est]:**

  | Variant | dense | sprawl | elite | old_island | civic |
  |---|---|---|---|---|---|
  | Paver sidewalk with kerb | 25% | 5% | 55% | 30% | 60% |
  | Drain slab only | 40% | 15% | 10% | 45% | 15% |
  | Earth/sand verge | 25% | 70% | 10% | 5% | 10% |
  | Grass verge (G5) | 0% | 5% | 25% | 0% | 15% |
  | None (building to road) | 10% | 5% | 0% | 20% | 0% |

- **Looks like (no sidewalk):** walkers share the road edge with okadas. They walk single file along a narrow beaten-earth line between the drain and traffic.
- **SELECT BY:** character, road class, wealth.
- **Gidi mapping:** `streets`, `mains` edges; paths `link`, `worn crossing`.

### E6. Shoulders used for trading and parking
- **Looks like:**
  - The 2–4 m between the carriageway edge and the drain or wall is fully used:
    - umbrellas and tables,
    - wheelbarrows of fruit,
    - parked tokunbo cars nose-in,
    - mechanics with cars on blocks,
    - vulcanisers,
    - a danfo park,
    - a pile of building sand for sale,
    - a church sign A-frame.
  - The ground there is beaten, oil-blackened earth or broken paving, with an oil stain field (`#2A2622`, 20–40% cover at mechanic spots).
- **Kit parts:** a shoulder ground material (earth + oil decals), a placement grid of stall slots (research-street §6.1), parked car slots at 2.5 m.
- **SELECT BY:** `mains` in dense, old_island, port: 60–90% of shoulder length used; near markets 100%; elite 0–10% (mostly parked cars at gates).
- **Gidi mapping:** `mains`, parcels `market`, `motor park`, `bus terminal`, `truck park`.

---

## 4. Ground

### G1. Compound floors
- **Looks like:**
  - The yard inside a gate, or between a building and its fence.
  - By wealth:
    - Poor: beaten earth, swept clean into brushed arcs every morning (broom marks are visible). A puddle at the low corner in the rains.
    - Middle: cement screed, cracked, with a drain hole to the street.
    - Rich: pavers or tiles, with a gutter and grating.
  - Common details: a mortar-cast step at each door, a well or borehole head, a soakaway lid (concrete disc 1–1.5 m), a septic cover (rectangular slab), a water tank stand, a clothesline, and plastic chairs.
- **Colours:**
  - Swept earth `#B07A52` (mainland) or `#C9B791` (island).
  - Screed `#A8A296`, stained `#8C857A`.
  - Tiles: white or terracotta `#B35A3C`.
- **SELECT BY:** wealth: < 0.3 earth 60% / screed 40%; 0.3–0.6 screed 60% / pavers 40%; > 0.6 pavers or tiles.
- **Gidi mapping:** `walls`/`gates` enclosures (Estate, Heights), compounds in `rules.py` (`compound_p`).

### G2. Sand yard
- **Looks like:** loose pale sand, with footprints, a broom-swept patch at the door, chickens and goats, coconut husks and fish-smoking ash.
- **Colours:** `#D8C9A3`, shaded `#BDAE8A`, ash `#8A8780`.
- **SELECT BY:** Old Shore, Water Town land fringe, sprawl near the lagoon; wealth < 0.4.
- **Gidi mapping:** Old Shore, Water Town plots.

### G3. Concrete apron
- **Looks like:** a cast slab between a shop front and the drain, 1–4 m deep, often stepped up 0.15–0.4 m above the road to keep floods out. Each shop builds its own, so the heights differ between neighbours and walkers step up and down. A tiled apron in front of a pharmacy or a bank.
- **Colours:** `#A39F95`, edge-chipped, oil-stained.
- **SELECT BY:** every shop frontage (`shop` flag in rules.py). Step height rises with `flood_low`: 0.15 m dry districts, 0.3–0.6 m in flood districts [est].
- **Gidi mapping:** `buildings` kind `front` with a shop.

### G4. Red earth colours by area
- **Geology basis:**
  - Lagos sits on Coastal Plain Sands (loose, silty, slightly clayey sand) that weather into laterite inland. These are quarried as road "borrow" fill [src Lagos–Ibadan geotech].
  - Lagos coastal soils are expansive and unstable (montmorillonite clay) [src Uniben thesis].
  - On the islands and lagoon edge: beach sands and lagoonal muds.
- **Gidi palette [est from photos]:**

  | Ground | Districts (Gidi) | Dry | Wet |
  |---|---|---|---|
  | Deep red laterite | Railside (Agege/Ifako ridge), Capital | `#B5562E` | `#7E3A1E` |
  | Orange-brown laterite | Maze, Hub, Bazaar (Ikorodu-like) | `#C4703D` | `#8B4A2B` |
  | Brown sandy loam | Food Gate, Jungle, Port | `#9A7A58` | `#5E4A36` |
  | Pale sand | Old Island, Old Shore, Heights, Estate (Lekki-like) | `#D8C9A3` | `#8F8670` |
  | Black lagoon mud | Water Town, Port shore, Jungle wetland | `#3B362C` | `#2A2620` |
  | Imported red fill on pale ground | new roads in sand districts | `#C4703D` stripe | |

- **SELECT BY:** district + local elevation (terrain rises north, per gidi-data-plan).
- **Gidi mapping:** ground material for every district.

### G5. Grass verge
- **Looks like:** carpet grass or Bermuda-type lawn on elite and civic verges and medians, mowed, with a painted kerb. Elsewhere: tussocky guinea grass and spear grass 0.3–1.5 m on unmaintained verges. Browns out in the dry season and the harmattan.
- **Colours:** wet green `#5E8A34`, dry `#A39466`, scorched `#8A7A55`, tall guinea grass `#7A9442`.
- **SELECT BY:** `elite`, `civic` verges mowed; `sprawl` tall; season sets colour.
- **Gidi mapping:** parcels `green`, `park`, `golf course`, `pitch` (bare-earth goalmouths), `garden`.

### G6. Bush on empty plots
- **Looks like:**
  - Fenced or unfenced vacant plots with:
    - 1–3 m tall elephant grass and guinea grass,
    - siam weed (Chromolaena) thickets,
    - cassava patches,
    - oil palms,
    - a mango tree,
    - a "THIS LAND IS NOT FOR SALE" or "BEWARE OF 419" paint on the wall,
    - a half-built foundation slab with rebar starter bars,
    - a refuse dump at the road edge,
    - footpaths cut diagonally across.
- **Kit parts:** grass card scatter (density 60–90%), bush clusters, a palm, a foundation slab mesh, a painted-warning wall.
- **SELECT BY:** sprawl 10–20% of plots; Lekki-like Heights/Estate edges 5–15%; dense 1–3% (and used as a dump).
- **Gidi mapping:** empty `slots`, undeveloped parcels, Frontier and Border.

### G7. Wetland / swamp
- **Looks like:**
  - Open water channels, sedge meadows, water lily, raffia palms, and remnant mangrove at saline edges.
  - Wetland plants recorded near the Lekki lagoon: sedges (Cyperaceae), the water lily Nymphaea lotus, raffia palm (Raphia hookeri) [src Unilag Ibeju-Lekki]. Mangroves include Rhizophora and the fern Acrostichum. Mangrove is disappearing and grass is taking over [src Unilag palynology].
  - Lekki and Festac lost more than 80% of their wetlands [src Gouni wetland change]. Gidi wetlands should look squeezed: housing pushes in, sand fill eats the edge, refuse floats.
  - Homes built in mapped wetland flood every year (Ajegunle 243 buildings/km²) [src LAGOS-ISMS].
- **Kit parts:**
  - A water plane with reed scatter (sedge clumps 0.5–1.2 m), lily pads, raffia palm (V4), a mangrove clump (stilt roots 1–2 m), sand-fill fingers, refuse rafts.
- **Colours:** water `#4A4A32`, sedge `#6F8A3A`, raffia frond `#5C7A2E`, mangrove leaf `#3E5A2A`, mud `#3B362C`.
- **SELECT BY:** elevation < 1 m and not built; Jungle, Water Town, Port, Heights edges.
- **Gidi mapping:** parcels `pond`; Jungle wetland; Water Town fringe.

### G8. Lagoon shore
- **Looks like:**
  - An irregular edge of fill: sand, sawdust, refuse and broken blocks pushed out into the lagoon to make land, with a revetment of sandbags, tyres, or old boats.
  - Sawdust from sawmills is dumped and rots on the water [src Timberville]. Gidi's sawmill shore (Okobaba-like) should have tan sawdust banks `#B89A6A` going black `#3A3326` at the waterline.
  - Canoes pulled up, fish-smoking sheds, net piles, a jetty of planks.
  - Water colour near shore: brown-green `#4A4A32` (research-street) with a refuse line.
- **Kit parts:** shore spline with a noisy fill edge, sawdust bank mesh, tyre revetment, canoe instances, plank jetty (`structures` jetty).
- **SELECT BY:** waterfront, port, Jungle, Old Island lagoon edges.
- **Gidi mapping:** `structures` `jetty`, parcels `sawmill`, Water Town shore.

### G9. Beach and its erosion
- **Looks like:**
  - Wide near-white sand beach, steep at the waterline, heavy Atlantic surf.
  - Palm-frond and thatch shelters, plastic chairs, horses for hire, coconut palms leaning seaward.
  - Erosion: a sand cliff 1–3 m at the berm, fallen palms with exposed roots, collapsed fences and buildings, sandbag and geotube walls. Tidal erosion took more than 25 m of land at one beach [src AFP via The Citizen]. Rates of up to −11 m/yr on the Ibeju-Lekki axis (1999–2012), while the mean for the Lagos coast was −0.57 m/yr with local gains from nourishment [src Akinluyi 2018].
  - Refuse along the tide line: sachets, flip-flops, bottles, and seaweed.
- **Kit parts:** beach slope mesh, scarp cliff (vertical sand face with root strings), fallen palm, geotube (sand-filled fabric tube 1.5–2 m diameter, grey `#6E6E66` or sand `#BFAE8A`), wrack line scatter.
- **Colours:** sand `#E3D8BD`, wet `#B5A88A`, foam `#F2F0EA`, sea `#3E6E7A` → surf `#7FA6A0`.
- **SELECT BY:** Old Shore coast; Heights/Estate sea edge (if any).
- **Gidi mapping:** coast strips; parcels `club`, `villas` beachfront.

### G10. Sand-filled reclaimed land
- **Looks like:**
  - A flat, pale-grey expanse of dredged sand. Fresh fill is near-white and rippled by wind. It has no vegetation for 1–2 years, then sparse grass and creeping vines.
  - Pipelines (dredge pipe 0.6–0.9 m, steel, rust `#8A5530`) on stands. Bulldozers.
  - A painted sign with a developer's name (generic) and "Phase 2".
  - Ponding in hollows in the rains. Roads are sand tracks (R8) until paved.
  - The pattern behind it: estates on reclaimed swamp blamed for flooding [src Guardian Lekki property owners, TheCable]. Lagos suspended all reclamation in 2025 [src Prime Business Africa], so some fill sites are frozen mid-work.
- **Kit parts:** flat sand plane with ripple normals, dredge pipe instances, berm edges, a frozen-site fence.
- **Colours:** fresh `#E0D6BE`, settled `#C9BC9A`, damp `#9E937B`.
- **SELECT BY:** Heights/Estate edges toward the lagoon; new developments; ages to G6 after 3+ years.
- **Gidi mapping:** parcels `villas`, `enclave`, `estate` under construction; Heights fringe.

---

## 5. Vegetation

The base species list and census are in research-street §6.9 (Polyalthia 27% of street trees, almond, neem, palms, flame tree). Below are modelling specs and the missing items.

### V1. Indian almond (Terminalia catappa)
- **Kit parts:** trunk 0.3–0.6 m; pagoda tiers of horizontal branches at 1.5–2 m spacing; crown 8–15 m wide, 10–20 m tall; leaf cards 0.15–0.25 m.
- **Colours:** green `#3E6B2A`, turning `#B23A26` and yellow `#C9A23A` in dry season; fruit litter `#6B8A2E`/`#5A3A22` under it.
- **Life:** the shade-tree of mechanics, vulcanisers and bus-stop traders. Benches under it.
- **SELECT BY:** dense/sprawl junctions, compounds, motor parks: 1 per 50–150 m of main [est].

### V2. Polyalthia (mast tree)
- **Kit parts:** a columnar cone 1.5–3 m wide, 8–15 m tall, drooping leaf cards; often in a row of 5–20 at 2–4 m spacing along a fence.
- **Colours:** `#2E4A22`.
- **SELECT BY:** elite and civic fences, GRA-like streets; Capital (Ikeja-like had the most street trees [src research-street]).

### V3. Coconut and oil palm
- **Coconut:**
  - Trunk 0.3 m, curved and leaning 5–20°, 10–25 m tall, ringed grey `#8E857A`.
  - Crown of 20–30 fronds 4–6 m long.
  - Nut clusters `#6E8A2E`.
  - Placed on the coast, Old Shore, and Water Town.
- **Oil palm:**
  - Trunk shaggy with frond bases `#5A4A38` (or smooth when old), 8–15 m tall.
  - Crown a dense ball of arched fronds.
  - Placed in sprawl, vacant plots, and the mainland north.
- **Ornamental palms:** royal palm (smooth, grey, a bulging trunk), foxtail, and fan palms in elite.

### V4. Raffia palm
- **Looks like:** a clumping, trunkless-looking palm with enormous fronds up to 10–15 m [est], in swamps.
- **SELECT BY:** wetland G7 only.

### V5. Plantain / banana
- **Kit parts:** clumps of 3–8 pseudostems, 3–6 m tall, with paddle leaves 1.5–2.5 m that tear into strips. A hanging bunch and a purple bud `#5A2A3A`.
- **Colours:** `#5E8A34`, torn edges brown `#8A6A3A`.
- **SELECT BY:** compound backyards (all characters except elite fronts), drain edges (they thrive on wastewater), sprawl plots. 1 clump per 2–5 compounds in dense and sprawl [est].

### V6. Bamboo
- **Looks like:** dense clumps 4–10 m wide and 10–15 m tall, culms 8–12 cm thick, green-yellow `#8FA23A` (or golden `#C9A23A`).
- **SELECT BY:** stream banks, low ground in sprawl, old compounds, the edge of `canal` banks. Rare in the dense core.

### V7. Grass and ground cover
- **Kinds:** spear grass (Imperata) on bare plots, guinea and elephant grass in bush, carpet grass on elite lawns, creeping morning-glory vines on fences and sand.
- **Seasons:** wet green from April–October, brown in Dec–Feb (harmattan).

### V8. Weeds in cracks
- **Looks like:** a green line of grass and small herbs (tridax with yellow-white flowers, goat weed) in asphalt cracks, paver joints, kerb joints, the drain lip and wall bases, and on top of old drain silt. Ferns and moss on shaded damp walls. A fig seedling sprouting from a parapet or a gutter.
- **Density:** rises with wetness and low traffic; low on busy mains (tyres kill it), high on quiet streets and abandoned paving.
- **Kit parts:** a mask-driven scatter of small card clumps (0.05–0.3 m) on crack and joint masks.
- **SELECT BY:** cond < 0.6 AND traffic low; ×2 in the rainy season.

---

## 6. Refuse

Base litter and heap specs are in research-street §6.7. Added here: the system and its states.

### W1. Refuse heaps
- **Looks like:**
  - Dumped at road medians, under bridges, at canal and drain edges, at empty plots, and at the end of a lane.
  - When the official collection fails, heaps spill across the carriageway. Only about 54% of Lagos waste reaches the disposal system; the rest goes to open dumps, drains, roadsides and waterways [src AllAfrica 2026 citing World Bank 2024].
  - Heaps are a mix of black and coloured nylon bags, sachets, food waste, ash, old foam mattresses, and broken plastic chairs.
- **Size states [est]:** fresh pile 1–2 m; established 3–5 m wide, 1–2 m high; a dumpsite across half the road, 10–30 m long.
- **Kit parts:** heap mesh (noise mound + bag/bottle instances on the surface), a spill-out fan, burnt patch decal, flies (particles).
- **Colours:** bags `#1C1C1C`, blue `#2A5BA8`, red `#B5332B`, white `#E6E4DE`; organic `#5A4A30`; ash `#7A7670`; leachate stain `#3A3428`.
- **SELECT BY:** character dense, old_island, port, waterfront; wealth < 0.4; near markets ×3; under `structures` flyovers ×3; Jungle and Maze peak.
- **Gidi mapping:** parcels `under bridge`, `market`, `landfill`; `canal` banks.

### W2. Bins and skips
- **Kit parts:**
  - Skip container about 4×2×1.5 m, green `#2E6B3A` or blue `#2A5BA8`, rusting; usually overflowing and ringed by refuse.
  - Wheelie bins 240 L (green, black) at elite gates.
  - Old drums cut in half, painted with "DUSTBIN" or an LGA name.
  - A Gidi-invented waste agency's livery on a compactor truck: generic white-and-green [est].
- **SELECT BY:** elite and civic: bins at every gate; dense mains: a skip every 300–800 m; sprawl: none.

### W3. Burning
- **Looks like:** many residents burn refuse rather than pay private operators [src NAN]. A smouldering black-and-grey mound with a thin smoke column, black char ring `#2B2A28`, and a grey ash halo. At dumpsites, tyre burning makes black smoke [src ThisDay Olusosun].
- **Kit parts:** smoke volume or cards (light grey `#BDBAB3` from refuse; black `#2A2A2A` from tyres), ember glow decal at night, char decal.
- **SELECT BY:** 20–40% of heaps in sprawl and dense smoulder in the dry season; 5% in the rains [est].

### W4. Scavengers and cart pushers
- **Looks like:**
  - Scavengers with sacks picking plastics and metal from heaps and dumpsites, sometimes living on site [src Wikipedia Olusosun].
  - Cart pushers with wooden handcarts (2 wheels, 1.5–2 m bed, painted sides) collect refuse for a fee, often dumping into canals and medians at night [src Ripples]. Banned at times, still present [src BusinessDay].
  - Scrap buyers pushing carts of metal and calling out for items [est].
- **Kit parts:** handcart prop, sack, scavenger poses, a pile of sorted PET bottles in a woven sack.
- **SELECT BY:** near heaps, dumpsites, markets; night dumping events at canals.
- **Gidi mapping:** parcels `landfill`; `canal`.

---

## 7. Selection tables (put these in `rules.py`)

### 7.1 Road surface mix by road class × character [est]
Shares of length per surface type (R1/R2/R3/R4/R5 asphalt states; R6–R8 unpaved; R9 pavers; R10 concrete).

| Class / character | New R1 | Worn R2 | Patched R3 | Potholed R4 | Failed R5 | Laterite R6/7 | Sand R8 | Pavers R9 | Concrete R10 |
|---|---|---|---|---|---|---|---|---|---|
| mains / dense | 10 | 25 | 30 | 25 | 5 | 0 | 0 | 3 | 2 |
| mains / port | 5 | 15 | 20 | 25 | 30 | 0 | 0 | 0 | 5 |
| mains / elite, civic | 45 | 30 | 10 | 5 | 0 | 0 | 0 | 5 | 5 |
| mains / sprawl | 10 | 25 | 20 | 25 | 15 | 5 | 0 | 0 | 0 |
| mains / old_island | 15 | 30 | 30 | 20 | 3 | 0 | 0 | 2 | 0 |
| streets / dense | 3 | 20 | 20 | 25 | 7 | 15 | 0 | 8 | 2 |
| streets / sprawl | 2 | 10 | 10 | 15 | 8 | 50 | 5 | 0 | 0 |
| streets / elite | 25 | 30 | 5 | 2 | 0 | 0 | 3 | 30 | 5 |
| streets / civic | 15 | 30 | 15 | 8 | 0 | 0 | 0 | 30 | 2 |
| streets / old_island | 5 | 30 | 25 | 20 | 5 | 0 | 5 | 10 | 0 |
| streets / waterfront | 0 | 10 | 10 | 15 | 10 | 10 | 45 | 0 | 0 |
| lanes / dense | 0 | 10 | 10 | 15 | 5 | 50 | 5 | 0 | 5 |
| lanes / sprawl | 0 | 3 | 3 | 7 | 5 | 70 | 10 | 0 | 2 |
| lanes / elite | 5 | 20 | 5 | 5 | 0 | 5 | 30 | 30 | 0 |
| lanes / waterfront, old_shore | 0 | 0 | 0 | 5 | 5 | 10 | 80 | 0 | 0 |

- **Swap rule:** in sand districts (G4 pale sand), the "laterite" column becomes sand except where a road has been "improved" with red fill (30%).
- **Paths:** `boardwalk` → planks (research-street waterfront); `market aisle` → trampled earth or broken concrete with litter; `worn crossing`, `cut-through` → beaten earth footpath 0.5–1.2 m; `rail path` → ballast-edged earth; `canal path` → earth bank, muddy in rain.

### 7.2 Condition score
```
cond = clamp(base + 0.4*(wealth-0.4) - truck - 0.3*flood_low - 0.08*years_since_repair, 0, 1)
base:  mains 0.6, streets 0.5, lanes 0.35
truck: port mains 0.35, other mains 0.1, else 0
flood_low: district below-5 m share mapped to 0..1 (50% -> 0, 99% -> 1)
years_since_repair: seeded per segment, 0-15 (elite 0-5, dense 2-12, sprawl 5-15)
```
Surface by cond on paved segments: > 0.8 R1; 0.6–0.8 R2; 0.4–0.6 R3; 0.2–0.4 R4; < 0.2 R5.

### 7.3 Seasons and wetness

| Season | Months (Lagos) | Rule |
|---|---|---|
| dry | Nov–Mar (harmattan haze Dec–Feb) | R6 dust; pothole water 0–10%; grass brown; burning heaps 20–40% |
| early_rain | Apr–May | puddles; de-silt heaps on roadsides; R7 in low spots |
| peak_rain | Jun–Jul (June wettest, ≈274 mm [src rainfall study]) | R7 everywhere unpaved; potholes 70–100% full; flood stages 1–3 in flood-low districts |
| little dry | Aug [est] | drying crusts, mud ruts |
| second peak | Sep–Oct | as peak_rain, flood stages up to 5 in the lowest districts |
| after_storm | event | flood stage +1 to +2 for 6–48 h, then silt and wrack decals |

- Season length: rains can start in late March and end in early December [src TheCable LASG forecast].
- Annual rainfall about 1,400–2,000 mm [src rainfall study, LASG forecast].

### 7.4 Drain state
```
drain_state ∈ {clear, silted, choked, broken}
p(choked) = 0.6*(1-wealth) * (market or bus stop ? 1.5 : 1) * (character in {dense, old_island, port, waterfront} ? 1 : 0.5)
p(broken) = 0.5*(1-cond)
```
A choked drain adds +1 flood stage to its street during rain.

### 7.5 Per-district quick defaults (Gidi)

| District | Character | Below 5 m | Main ground | Typical street | Worst-case rainy-day street |
|---|---|---|---|---|---|
| Maze | dense | 50% | orange laterite | R3/R4, open drains choked | R4 water-filled, stage 1–2 |
| Hub | dense | 66% | orange laterite | R3/R4 | stage 2–3 at the bus terminal |
| Jungle | dense | 85% | brown loam + black mud | R4/R5, canals choked | stage 3–5 ("flood days") |
| Food Gate | dense | 84% | brown loam | R4, market litter | stage 2–3 |
| Bazaar | dense | 77% | orange laterite | R6/R7 lanes | R7 mud, stage 2 |
| Railside | sprawl | 52% | deep red laterite | R6 dust / R7 mud, gullies | R7 + R13 washouts |
| Frontier, Border | sprawl | 71–76% | red laterite / sand | R6/R8 | R7, wetland edges |
| Old Island | old_island | 99% | pale sand under paving | R2/R3, drains open and deep | stage 2–4 |
| Old Shore | old_island | 66% | pale sand | R8 sand | sand scour, beach erosion |
| Estate | elite | 70% | pale sand | R1/R9 | stage 2–3 in low estates |
| Heights | elite | 87% | pale sand + fill | R1/R9/R10 | stage 3–4 (the rich flood too) |
| Capital | civic | 50% | deep red laterite | R1/R2/R9 | stage 1 |
| Water Town | waterfront | 84% | black mud + sand | R8 + boardwalks | stage 3–5 |
| Port | port | 89% | brown loam + oily mud | R5 craters on mains | R5 lakes + stage 3 |

---

## Sources
- Lagos roads in rains, potholes under floodwater, trucks stuck, community fills:
  - https://guardian.ng/news/heavy-rains-leave-lagos-roads-in-shambles/
  - https://guardian.ng/sunday-magazine/help-our-roads-in-tatters-ago-palace-residents-cry-out/
  - https://guardian.ng/?p=2891513 (LSPWC repairs despite downpours)
  - https://guardian.ng/?p=2890999 (Oshodi-Isolo roads)
  - https://guardian.ng/sunday-magazine/newsfeature/in-aboru-iyana-ipaja-residents-groan-over-bad-roads/
  - https://guardian.ng/?p=2898648 (Ikotun roads)
  - https://gazettengr.com/residents-call-for-speedy-completion-of-igbogbo-baiyeku-road/
  - https://www.icirnigeria.org/residents-of-ikorodu-bemoan-the-aftermath-of-flood-due-to-heavy%E2%80%A8downpours/
  - https://archive.businessday.ng/lagos/article/isheri-oshun-residents-decry-poor-state-of-road/
  - https://ikejarecord.com/?p=2537
- Apapa craters and trucks:
  - https://thisdaylive.com/index.php/2017/08/12/the-tragedy-of-apapa-ii
  - https://thisdaylive.com/index.php/2017/08/05/oshodi-apapa-wharf-road-a-testament-to-failure-in-governance
  - https://thisdaylive.com/index.php/2016/11/18/the-road-to-apapa-ports
- Washouts and collapses:
  - https://guardian.ng/?p=1292956 (poor drainage worsening roads)
  - https://www.pressreader.com/nigeria/business-day-nigeria/20190922/281672551660360 (Gberigbe)
  - https://clone.businessday.ng/?p=429672 (Mile 2 collapse and refuse in drains)
- Interlocking pavers:
  - https://ideas.repec.org/a/ibn/masjnl/v6y2012i5p91.html (Ojuri 2012)
  - https://thisdaylive.com/index.php/2022/07/27/lagos-public-works-sustains-road-maintenance-efforts
  - https://www.vanguardngr.com/2015/05/road-challenges-in-lagos-residents-call-for-govts-intervention/amp/
  - https://allafrica.com/stories/202608050742.html
- Construction and diversions:
  - https://thecable.ng/lagos-to-divert-traffic-on-ikorodu-road-for-90-days-over-repairs
  - https://nairametrics.com/2023/01/14/lagos-announces-partial-road-closure-traffic-diversion-at-ojota/
  - https://nairametrics.com/2020/11/11/lagos-to-close-a-section-of-ketu-mile-12-corridor-of-ikorodu-road/
  - https://www.channelstv.com/2021/04/24/lagos-govt-to-divert-traffic-at-independence-tunnel-on-may-3/
- Flooding:
  - https://kolaking.substack.com/p/10-hour-rainfall-lekki-ikoyi-residents
  - https://www.thecable.ng/?p=1223965 (submerged car, Lekki estate)
  - https://thecable.ng/photos-residents-stranded-cars-submerged-as-flood-ravages-lagos
  - https://www.zikoko.com/?p=361184
  - https://inhabitat.com/?p=2310083
  - https://radionigerialagos.gov.ng/?p=31062
  - https://allafrica.com/stories/202607010113.html
  - https://guardian.ng/news/rain-exposes-lagos-underbelly/
- Canals, hyacinth, refuse:
  - https://guardian.ng/?p=2876036 (ecology fund, canals clogged)
  - https://www.opinionnigeria.com/lagos-is-drowning-in-more-than-rain-by-kator-ifyalem/
  - https://pulitzercenter.org/node/30445
  - https://guardian.ng/?p=2048956 (Oke-Afa canal dumpsite)
  - https://shippingposition.com.ng/despite-n714-million-budget-water-hyacinth-overwhelms-niwa-takes-over-lagos-waterways/
- Waste, burning, scavengers:
  - https://allafrica.com/stories/202606080120.html
  - https://nannews.ng/lagos-residents-lament-air-pollution-seek-stricter-law-enforcement/
  - https://thisdaylive.com/index.php/2023/10/25/lagos-dislodges-scavengers-at-olusosun-dumpsite
  - https://en.wikipedia.org/wiki/Olusosun_landfill
  - https://www.ripplesnigeria.com/lagos-govt-bans-cart-pushers-says-theyre-threat/
  - https://archive.businessday.ng/features/article/death-mega-city/
- Speed bumps:
  - https://guardian.ng/news/fg-orders-removal-of-speed-bumps-on-highways-nationwide/
  - https://ripplesnigeria.com/minister-umahi-orders-removal-of-hazardous-speed-bumps-on-highways-gives-conditions-for-installations
  - https://gazettengr.com/anambra-bans-unauthorised-construction-of-speed-bumps/
  - https://guardian.ng/?p=1055183
- Drains (precast sizes, non-Lagos reference):
  - https://jiji.com.gh/adenta-municipal/building-materials/culverts-u-drains-concrete-round-pipes-precast-manholes-septic-tanks-fKhaEA3aszyiuAujZioKq9Ng.html
  - https://lntsufin.com/product/dc-900-mm-900-mm-2000-mm-u-drain-m-40/17150-2859
  - https://www.scribd.com/document/620199436/Built-Up-Rates-R-C-Drain
- Pothole severity classes: FHWA, Distress Identification Manual for the LTPP Program (FHWA-HRT-13-092), pothole depth bands.
- Soils and geology:
  - https://kwasuspace.kwasu.edu.ng/items/8ab83e58-ff59-4297-8d69-33bd30572352/full
  - https://repository.uniben.edu/sites/default/files/2026-03/ANITA%20BILLONS_2.pdf
  - https://www.citedrive.com/en/discovery/characterization-classification-and-agricultural-potentials-of-some-coastal-plain-sand-derived-soils-in-lagos-state/
- Wetlands and vegetation:
  - https://ir.unilag.edu.ng/handle/123456789/4807 (Ibeju-Lekki wetland flora)
  - https://ir.unilag.edu.ng/handle/123456789/11216 (Late Holocene wetland record)
  - https://eprints.gouni.edu.ng/5445/1/13.Spatial_Changes_in_the_Wetlands_of_Lagos2013b.pdf
- Coast and erosion:
  - https://www.thecitizen.co.tz/news/1840340-5190188-8tlkm1/index.html (AFP, Alpha Beach)
  - https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-fdd66c63-d8e9-4a93-a2eb-a5889e12fb99/c/akinluyi_adebola_assessment_1_2018.pdf
- Reclamation:
  - https://www.primebusiness.africa/lagos-halts-all-land-reclamation-as-flood-risk-federal-clampdown-heighten-tension/
  - https://guardian.ng/news/lekki-property-owners-propose-end-to-sand-filling-flood-management-strategies/
  - https://www.thecable.ng/?p=191935
  - https://guardian.ng/property/experts-worry-over-land-reclamation-dredging-as-environmental-concerns-rise/
- Sawmill shore and Makoko:
  - https://en.wikipedia.org/wiki/Timberville_(Lagos)
  - https://en.wikipedia.org/wiki/Makoko
  - https://seed.uno/articles/enterprise-briefs/enterprise-brief-sawdust-entrepreneurial-initiative-among-oko-baba-communities-in-lagos
- Rainfall and seasons:
  - https://thecable.ng/lagos-issues-excess-rainfall-alert-warns-of-possible-flooding
  - https://radionigerialagos.gov.ng/?p=38910
  - Daily rainfall sequences across Nigeria 1971–2011 (Lagos mean 1,424 mm, June wettest 274 mm), via https://samafind.sama.gov.sa/index.php/EdsRecord/edsair,edsair.doi...........27f247f5f067591a1fae23bd78e5c754
- Project-internal:
  - /Users/Star/gidi/docs/look/research-street.md
  - /Users/Star/gidi/docs/gidi-data-plan.md (per-district low ground)
  - /Users/Star/gidi/docs/LAGOS-ISMS.md (#10 flood-prone low spots)
  - /Users/Star/gidi/blender/gidi_kit/rules.py (character keys)
  - /Users/Star/gidi/web/gen-*.json (data kinds: mains, streets, lanes, paths, canal, parcels, structures)
