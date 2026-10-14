# The Lagos look: a seeded Blender kit that styles Gidi from its data

**What this is.** Everything in Gidi gets its look from what the map data already knows about it:
- its kind (front house, back house, shed, stalls, kiosk, …)
- its storeys
- its district (and so the character of that district's real inspiration)
- which face looks onto a street, and how far away that street is
- how far it is from a main road
- whether it is unfinished (at the district's rate from [LAGOS-ISMS.md](LAGOS-ISMS.md), #8)

Rules turn those attributes into parts and specs, and a seed per object gives variety that is stable: the same building always comes out the same.

**Where it comes from.**
- Pattern research on real Lagos, in two catalogues: [buildings and their parts](look/research-buildings.md) and [streets, vehicles, people, signage and props](look/research-street.md).
- Both are patterns only (rule zero): no real building, name or brand is copied. Numbers marked [est] are estimates to tune by eye. Numbers marked [src] are sourced.
- Visual target: bright, detailed stylized realism (owner's reference screenshots, 14 Oct 2026). That means:
  - real proportions
  - real materials, with Lagos wear
  - glossy vehicles
  - busy streets

## How to run it (Blender 5.1, headless)
| Command | What it does |
|---|---|
| `blender -b --factory-startup -P blender/catalogue.py -- --seeds 3` | Contact sheet: the same footprint built for each district character, storeys 1–3, several seeds. `--cam close` gives an eye-level shot of one shop house. |
| `blender -b --factory-startup -P blender/generate.py -- --district maze --at 2620,4392 --r 140 --out blender/out/ladi-lane` | Builds the area around a point from `web/gen-<district>.json`, styled by the rules. Renders `overview.jpg` and `street.jpg` (eye level on the street with the most shop fronts). `--glb` exports glTF, `--blend` saves the scene. |

Output goes to `blender/out/`, which is not committed.

## How it is built (`blender/gidi_kit/`)
| File | What |
|---|---|
| `core.py` | `Rng`: a random stream from any key (district, building index, salt). `MeshBuilder`: faces with a material, a colour and a wear value. Polygon helpers. |
| `materials.py` | Eight or so master materials. Each reads the mesh's `Col` and `Wear` attributes, so one material serves every paint colour and every age. Wear adds the Lagos weather: red-earth splash at the foot of walls, rain streaks, chalky sun-faded paint, zinc that goes dull and rusts in streaks down the ribs, stained concrete. The same two attributes can drive material instances in Unreal. |
| `parts.py` | The kit pieces (see the list below). |
| `rules.py` | District → character (dense mainland, sprawl, old island, elite, civic, waterfront, port). Per character: paint and roof palettes, wear and wealth ranges, window-type and bar-pattern shares, how often roofs are flat by storeys, and the odds of balconies, compound walls, shops, hand-painted signs, tanks, dishes, generators and tyres on the roof. `house_spec()` turns a building's attributes into every part's spec. |
| `archetypes.py` | `house` (front, back and shed), `stall`, `kiosk`. Kinds without an archetype yet are built as plain houses. |

The kit pieces in `parts.py`:
- walls: chamfered corners, plinth, floor bands
- windows: naco louvres, casement or sliding, with frame, sill and hood
- burglar bars: vertical, grid, diamond, sun-ray or scroll
- steel doors, roller-shutter shop fronts with a step
- balconies with precast balusters or a steel rail
- corrugated zinc and long-span roofs, as real ribbed geometry:
  - ribs run square to the eave
  - each sheet ages on its own
  - gable or hip
- flat roofs with parapet and coping
- ribbed water tanks on steel stands, satellite dishes, tyres holding sheets down, caged generators
- unfinished storeys: columns, rods, stepped block courses
- compound walls with pillars, coping, broken bottles or razor wire, and a steel gate
- signboards with 3D lettering and a phone number
- zinc awnings on timber posts

## Previews
| | |
|---|---|
| ![](look/img/catalogue.jpg) | ![](look/img/shop-close.jpg) |
| ![](look/img/ladi-lane-overview.jpg) | ![](look/img/ladi-lane-street.jpg) |

## Next
1. **Street life, from the street catalogue.**
   - poles, wire tangles and transformers
   - open drains with slab crossings
   - kerbs, potholes and markings by road class
   - litter
   - danfo, okada, keke and cars
   - people in ankara, with head loads
   - umbrellas and stalls with goods by market type
2. **Archetypes for the other kinds in the data.**
   - brazilian house, stilt, mansion, gatehouse, flats, plaza, phone mall
   - church, mosque, school, clinic, fuel, bank
   - container, warehouse, bakery, sawmill, pen
3. **Feed the research numbers into `rules.py`.** The [est] figures get tuned by eye against reference photos.
4. **Unreal hand-off.**
   - weld vertices and make LODs: the 140 m Ladi Lane glTF is 284 MB unwelded
   - export per archetype and variant
   - a material-instance setup that reads `Col` and `Wear`
