# Gidi street catalogue: roads, vehicles, people, signage, props

This is research for a procedural generator. It studies real Lagos and describes patterns only. Every brand is described generically, and Gidi must invent its own names, liveries and slogans.

Legend:
- **[src]** means a cited source supports the figure (see Sources).
- **[est]** means an estimate from general knowledge of Lagos street imagery and from comparable standards (Nigerian Federal Highway Manual practice, British-derived kerb and drain conventions). The web turned up no Lagos-specific spec for these.
- Hex values are always approximations of weathered, sun-faded colours as seen in photos, not paint-chart values.

District keys used in SELECT BY:
- `dense_mainland`: Mushin, Oshodi, Ajegunle-like areas.
- `old_island`: Lagos Island, Idumota, Balogun.
- `elite`: Ikoyi, VI, Banana Island, GRA.
- `sprawl`: Agege, Alimosho, Ikorodu outskirts.
- `waterfront`: Makoko-like.
- `port`: Apapa-like.

---

## 1. ROADS

### 1.1 Carriageway by class
| Class | Lanes | Lane width | Total paved | Notes |
|---|---|---|---|---|
| Expressway (Lagos-Ibadan, Ikorodu Rd, Lekki-Epe type) | 3+3, sometimes 4+4; plus BRT lane each way on BRT corridors | 3.5–3.65 m [est] | 2×11–15 m + median 1–6 m [est] | Rigid concrete (light grey `#9A9890`) or asphalt (`#3A3A38`, fading to `#5E5C57`). Lekki-Epe was rebuilt as a six-lane rigid concrete carriageway with a truck lane each way [src VON]. Service roads run alongside on parts. |
| Main road / arterial (Herbert Macaulay, Agege Motor Rd type) | 2+2, often undivided or with a low kerb median | 3.0–3.5 m | 12–16 m | Bus-stop lay-bys are rare: danfos stop in the lane. |
| Street (residential/commercial) | 2 lanes, unmarked | ~3 m | 6–8 m | Usually no centre line. Edges are crumbling, with sand and laterite shoulders. |
| Lane / close / "crescent" | 1–2, unmarked | n/a | 3.5–5.5 m | In sprawl often unpaved red laterite. In old_island they are 2.5–4 m wide and lined wall-to-wall with shops. |

**Surfaces and frequency [est]:**
- Expressways: about 100% paved.
- Main roads: about 95% paved, with 20–40% of the length patched.
- Streets: `elite` about 95% paved (some with interlocking pavers), `dense_mainland` about 70%, `sprawl` 30–50% (the rest laterite).
- Lanes in `sprawl`: about 70% unpaved.

**Paint and markings:**
- White dashed lane lines: 3 m dash, 6–9 m gap, 0.10–0.15 m wide [est].
- Yellow solid edge line on expressways.
- Zebra crossings are rare.
- Markings are faded: 50–80% worn on main roads [est]. Freshly re-marked roads appear only near government showcase projects.
- BRT lanes are separated by low concrete kerb or separator blocks, sometimes painted yellow and black.

**SELECT BY:**
- `road_class` sets width and lane count.
- Wealth sets marking freshness and patch density.
- `elite` and newly built corridors get crisp paint.
- `dense_mainland` and `sprawl` get faded paint and broken edges.

### 1.2 Kerbs (painted)
- **Look:** Precast concrete kerb blocks about 0.9–1.0 m long, painted in alternating bands, one band per block or two per block. The statutory colours are **black-and-white** or **yellow-and-black**. Lagos argued in court that green-and-white kerbs were illegal [src BusinessDay].
- **Dimensions [est]:**
  - Upstand 0.15–0.25 m.
  - Block 0.125–0.15 m thick, 0.9–1.0 m long.
  - Some medians use high 0.4–0.5 m "mountable-not" kerbs.
- **Colours:**
  - Yellow `#E8C21A`, sun-faded to `#D9B85A`.
  - Black `#1C1C1C`, faded to `#3B3B3B`.
  - White `#EDEBE4`, dirtied to `#C9C4B5`.
- **Weathering:**
  - Grime band at the bottom 5 cm (`#6B5A45`).
  - Chipped corners.
  - Missing blocks: 1 in 20 on main roads, 1 in 5 in `dense_mainland` [est].
  - Sand drifts piled against the kerb.
- **Variants:**

  | Variant | Share [est] |
  |---|---|
  | Yellow/black | 50% |
  | Black/white | 40% |
  | Unpainted grey | 10% (side streets) |
  | Green/white | Rare. Illegal, but seen as an LGA showpiece. |

- **SELECT BY:**
  - Painted kerbs go on expressways, main roads, medians, roundabouts and the edges of government frontages.
  - Unpainted kerbs or none at all go on streets and lanes.
  - Freshness rises with wealth and with nearness to a government building.

### 1.3 Medians
- **Variants [est]:**
  1. **New Jersey concrete barrier.** Base 0.6 m, height 0.8–0.9 m, segments 3–6 m long. Plain grey `#A8A59C` or painted in yellow/black bands. About 35% of expressway medians. Often gapped where people climb over.
  2. **Raised kerb median, earth-filled.** 1–6 m wide, painted kerbs, filled with grass, sand or weeds. About 40%. In `elite` and on showpiece roads it is planted with low hedges, palms or bougainvillea. Elsewhere it holds bare sand, refuse and hawkers.
  3. **Painted precast blocks** (temporary, 0.5×0.5×1 m) at diversions. About 10%.
  4. **None** (painted line only, or nothing). Usual on main roads in `dense_mainland`.
- **Planted median plants:**
  - Dwarf palms.
  - Foxtail palms in `elite`.
  - Ixora (red flowers, `#D9332B`) and croton hedges (variegated `#B8A23A`/`#7A2E1E`).
  - Grass (`#6E8F3A`, browning to `#A39466` in the dry season).
- **SELECT BY:**
  - Expressways get Jersey or raised medians.
  - `elite` gets a planted median.
  - `dense_mainland` main roads get a broken, bare median.
  - A footbridge nearby means fewer climb-through gaps.

### 1.4 Walkways / sidewalks
- **Width [est]:**
  - Main roads: 1.5–3.0 m, but effectively 0.5–1 m usable because of traders, cars and generators.
  - Streets: often absent, so walkers use the drain slab or the road edge.
- **Materials:**
  - **Interlocking concrete pavers.** Hexagonal or "I/dog-bone" shapes, about 0.2×0.1×0.06–0.08 m. Grey `#8E8B84` or with red/charcoal accents (`#8A4B3A`, `#4A4A48`). Very common since the 2000s on rebuilt roads.
  - Cast slabs over the drain (see 1.5).
  - Broken asphalt.
  - Packed earth.
- **Weathering:**
  - Sunken patches.
  - Pavers lifted by roots.
  - Oil stains near mechanic spots (`#2A2622`).
  - Red laterite dust at the edges.
- **SELECT BY:**
  - Pavers go on `elite` and new corridors, and on main roads in `dense_mainland` (heavily occupied).
  - Earth goes on `sprawl` streets.
  - Near a market or bus stop, at least 70% of the walkway width is occupied by stalls.

### 1.5 Open drains / gutters
- **Look:** Rectangular concrete or block-lined channels along one or both road edges. Lagos drainage is a disconnected network of shallow gutters that carry household wastewater to streets and canals [src Pulitzer].
- **Dimensions [est]:**

  | Drain | Width | Depth |
  |---|---|---|
  | Street drain | 0.45–0.6 m | 0.45–0.9 m |
  | Main-road drain | 0.9–1.5 m | 1.0–1.8 m |
  | Primary canal (e.g. Ojora/Jibowu style) | 5–20 m | earth or concrete banks |

  - Walls are 0.15–0.2 m thick, sandcrete block plastered or cast concrete.
- **Covers:**
  - Precast slabs 0.6–1.0 m long × drain width, 0.1–0.15 m thick.
  - Coverage: main roads 50–80% covered, `dense_mainland` streets 20–50%, `elite` 90% covered or grated.
  - Gaps from missing or stolen slabs [src Guardian].
  - Cut-outs, and small concrete or plank bridges at each shop entrance.
- **Contents and colour:**
  - Stagnant grey-green water (`#4F5A3C`) or black silt (`#2B2A24`).
  - Sachets and bottles.
  - Plants growing in silt.
  - Concrete walls stained `#7A7466` with a green algae line (`#5D6B3A`) at the waterline.
- **SELECT BY:**
  - All paved street classes have a drain.
  - `elite` gets covered drains.
  - `dense_mainland`, `old_island` and `sprawl` get open, partly choked drains.
  - The canal sits on district low ground or the waterfront.

### 1.6 Potholes and patching
- **Potholes:**
  - Diameter 0.3–3 m, depth 0.05–0.3 m [est].
  - In the wet season they fill with brown water (`#7A5A3A`).
  - Edges are ragged, with aggregate showing.
- **Density per 100 m [est]:**

  | District | Potholes |
  |---|---|
  | `elite` | 0–1 |
  | Main roads in `dense_mainland` | 2–6 |
  | `sprawl` | 5–15 (or the whole road is broken) |
  | `port` | worst: craters 5–10 m wide where trucks queue |

- **Patching:**
  - Darker rectangles of fresh asphalt (`#2B2B29`) on faded grey.
  - Sand, rubble or concrete fill, often by local "area boys" or residents asking for tips.
- **SELECT BY:** Inverse of wealth, and multiplied by truck traffic (`port`).

### 1.7 Speed bumps
- **Look:** Home-made asphalt or concrete humps. Some have painted stripes (yellow/black or white), but most are unpainted.
- **Dimensions [est]:** Height 0.08–0.2 m, often too high. Length 0.5–1.5 m. Sometimes in pairs or triples (rumble set).
- **Placement:** In front of schools, churches, mosques and estate gates. Every 50–150 m on `elite` estate roads.
- **SELECT BY:**
  - Residential streets get them, with gated estates getting the most.
  - Expressways have none.

### 1.8 Shoulders and red earth
- **Laterite:**
  - Red-orange to brown: `#B5562E` (wet), `#C4703D` (dry), `#A0522D`, dusty pale `#C9926A`.
  - Lagos coastal soil is often pale sand: `#D8C9A3` on the Island and Lekki, `#BFAE8A` greyish.
- **Rule:**
  - Laterite (red) dominates on the mainland and inland (`sprawl`, Agege, Ikorodu).
  - Pale sand dominates on the Island, Lekki and `waterfront`.
- **Weathering:** Dust gets kicked onto the asphalt edge as a gradient 0.3–1 m wide.

---

## 2. STREET INFRASTRUCTURE

### 2.1 Electricity poles
- **Type:** Basically concrete poles for medium and low voltage (33 kV / 11 kV / 415 V) [src JICA]. Older wooden poles survive in older streets: creosote brown `#5A4632`, grey-weathered `#7E776B`. Steel tubular poles appear on some new lines.
- **Dimensions [est]:**
  - Concrete poles: 9–12 m for LV/11 kV, 12–15 m for 33 kV. Square-tapered section, 0.2–0.3 m at the base.
  - Spacing: 30–50 m (LV), 60–80 m (33 kV).
  - Crossarms: galvanised steel channel 1.5–2.4 m (LV/11 kV) or 2.4–3 m, with white or brown ceramic insulators.
- **Wires:**
  - 3–4 bare aluminium conductors.
  - Plus spaghetti: house service drops (black PVC), with 5–20 drop wires per pole in `dense_mainland`.
  - Old cable-TV and telecom lines.
  - Wires sag 0.5–1.5 m between poles.
  - Illegal tap-offs. Kite remains and nylon bags snagged on wires.
- **Weathering:**
  - Concrete greyed `#9C978C` with black rust/water streaks.
  - Some with exposed rebar at the base.
  - Leaning 2–8° [est].
  - Posters pasted on the base 0–2.5 m high.
  - Painted numbering.
- **SELECT BY:**
  - Everywhere except along `elite` estate cores, where cables run underground.
  - Wire tangle density rises with density.
  - Wooden poles go in older streets of `old_island`, `dense_mainland` and Yaba-like areas.

### 2.2 Transformers
- **Look:** Pole-mounted H-frame (two poles, platform 3–4 m up) or ground-mounted on a plinth inside a chain-link or blockwork cage. Grey tank `#8C8F8A` with radiator fins and three bushings.
- **Dimensions [est]:** Tank about 1.2×0.8×1.5 m (300–500 kVA).
- **Extras:**
  - A painted or stencilled ownership notice from the distribution company (invent).
  - "DANGER" signs with a lightning bolt.
  - Community-labelled "CDA" paint.
- **Frequency [est]:** One per 2–6 streets. Often there is a cage with a generator next to it on a market street.
- **SELECT BY:** Street junctions and estate entrances.

### 2.3 Street lamps
- **Variants:**
  - **Galvanised steel pole with a single or double arm.** 8–12 m, with cobra-head sodium or LED heads. On expressways and main roads. Spacing 30–40 m, often on the median (double arm). Many do not work: [est] 30–60% dark.
  - **Solar street lamp.** 6–9 m pole with an angled panel (0.6×1.0 m, blue-black `#1E2A44`) on top and an all-in-one LED head. Common since the 2010s on LGA roads, in `sprawl` estates and on bridges. Battery box on the pole at 3 m.
  - **Decorative twin-globe or lantern lamps** in `elite` estates and VI boulevards.
- **Light colour:**
  - Sodium `#FFB15C` (older).
  - LED cool `#E8F0FF` (newer).
  - Solar is dimmer, at about 40% of grid brightness.
- **SELECT BY:**
  - Expressways get median twin-arm lamps.
  - `elite` gets decorative lamps.
  - `sprawl` gets sparse solar lamps.
  - `dense_mainland` side streets get almost none: light comes from shops and generators.

### 2.4 Traffic lights
- **Look:** Standard three-aspect heads (red, amber, green) on galvanised poles or gantries, often with a countdown timer display. Many are solar-powered with a panel on top.
- **Frequency:** Low. Many junctions are run by uniformed traffic wardens (see People) or have nothing at all.
- **SELECT BY:** Big junctions in `elite` and on central main roads. Rare in `sprawl`.

### 2.5 Bus stops
- **Informal:** Most stops are simply a known spot with a crowd, a few hawkers, danfos double-parked and conductors shouting. There may be a painted name on a wall or a small signpost.
- **Standard shelter [est]:**
  - Steel frame 4–8 m long, 2–2.5 m deep, 2.6–3 m high.
  - Curved or sloped polycarbonate or metal roof.
  - Bench seat and advertising panel.
  - Colours: blue/white `#1F4E9A`/`#FFFFFF` or state-branded.
- **BRT station:**
  - Raised platform about 0.9 m above road, in the median.
  - Steel-and-glass or metal shelter 20–40 m long.
  - Ramps or a footbridge for access, plus turnstiles.
  - 44 shelters were upgraded on the extension corridor [src SSATP/LAMATA].
  - The Lagos regulated bus colour is blue and white [src LAMATA].
- **SELECT BY:**
  - A BRT station goes on expressway corridors with a BRT lane.
  - Shelters go on main roads.
  - Informal stops are dense at junctions, markets and under bridges.

### 2.6 Pedestrian bridges
- **Look:**
  - Steel truss or concrete deck with stairs (often no ramp).
  - Mesh or railing sides, painted green, blue or grey.
  - Large billboards often mounted on the bridge sides as "bridge panels".
- **Dimensions [est]:** Clear height about 5.5 m. Deck width 2.5–3.5 m. Spans 30–60 m. Stair flights of about 25–35 steps.
- **Life:** Hawkers on the stairs, beggars, and people still crossing below.
- **SELECT BY:** Expressways and wide arterials near markets, bus parks and BRT stations. One per 0.5–1.5 km on busy corridors.

### 2.7 Billboards
- **Types and sizes:**

  | Type | Face | Support | Frequency [est] |
  |---|---|---|---|
  | 48-sheet | ~6.1×3.05 m [src papersizes] | 1–2 steel posts, 4–8 m to bottom of face | Common on main roads |
  | 96-sheet | ~12.2×3.05 m [src AdQuick] | 2–3 posts | Expressways |
  | Unipole | 12–15 × 4–6 m, often double- or triple-sided | Single 1–1.5 m dia steel column, "over 40 ft" (12 m+) [src schoolings] | Expressways, interchanges |
  | Gantry | Spans the carriageway, 15–30 m | Truss across the road | Expressways (priced higher) [src ABSSAA] |
  | Portrait / backlit "mupi" | 1.2×1.8 m | On walkway | `elite` |
  | LED digital | 6×3 to 12×4 m | Unipole | VI, Ikeja, Lekki: glows at night |
  | Rooftop | 6–12 m wide | On buildings | `dense_mainland`, `old_island` |

- **Content (invent):**
  - Telecom.
  - Beer and spirits.
  - Banks.
  - Seasoning cubes.
  - Churches and crusades.
  - Politicians (huge faces, especially in election season).
  - Real estate.
  - Betting.
- **Weathering:**
  - Torn flex faces flapping (strips), bare frames with lattice visible.
  - Rust `#8A4B2A`.
  - "Space available" plus a phone number.
  - A catwalk ladder up the post.
- **SELECT BY:**
  - Unipoles and gantries go on expressways.
  - 48-sheets go on main roads.
  - Rooftop boards go in `dense_mainland`.
  - LED boards go in `elite`.
  - Few or no boards on side streets.

### 2.8 Road signs
- **Look:**
  - Directional signs: green with white text on expressways, and blue in places.
  - Regulatory signs: red ring.
  - Warning signs: red triangle.
  - UK/Vienna-style shapes.
- **Weathering:** Many are bent, faded or stickered over, or missing their faces.
- **Extras:**
  - "LASTMA"-style enforcement warnings (invent an agency name for Gidi).
  - "No Parking", "Do Not Drop / Pick Passengers Here".
- **SELECT BY:** Expressways and main roads. Rare on streets.

---

## 3. VEHICLES

### 3.1 Danfo (yellow minibus)
- **Base vehicle:** Mostly a 1979–1992 European rear-engine boxy cab-over van (T3-type) [src Autopian, Wikipedia]. Later fleets mix in Japanese cab-over vans and Chinese minibuses. Model generically as a **flat-front boxy van with a slight windscreen rake and a rear engine** for the old type, and a **short-nose 12–18 seat van** for newer ones.
- **Dimensions** (T3-type base): Length 4.57 m, width 1.84 m, height ~1.95 m, wheelbase 2.46 m [src Wikipedia].
- **Capacity:** Nominally 14. In practice 4 per bench row, plus 2 in the front passenger seat [src Autopian].
- **Livery:**
  - Body yellow `#F2C200`, faded to `#E0B43A`, chalky `#D6B867`.
  - **Two parallel black horizontal stripes** along the sides [src Red Bull], each about 0.08–0.12 m, at waist and sill line [est].
  - Black bumpers.
  - Sometimes a white or black roof.
  - Commonly a black band around the windows.
- **Windows:**
  - Four side window panes per side behind the cab.
  - Sliding side door on the kerb side (right-hand, since Nigeria drives on the right). Usually **removed or left open**, and the conductor hangs there.
  - Rear hatch with window.
  - Windscreen often cracked.
- **Interior:** Wooden or metal benches, bare metal [src Autopian].
- **Roof:** About 30% have a roof rack (welded steel tube) with luggage or goods [est].
- **Stickers and slogans** (body, rear and windscreen top strip), patterns only:
  - Religious ("God's Time Is The Best"-type).
  - Proverbs.
  - "No Condition Is Permanent"-style.
  - Football clubs.
  - Hand-lettered names.
  - A route board on the windscreen.
  - A 2018 law nominally restricts slogans [src Autopian]. **Gidi:** write original slogans.
- **Condition:**
  - Dents, rust bubbles (`#7A3E1E`) at the wheel arches.
  - Mismatched panels: about 15% have a primer-grey or green door or panel.
  - Missing hubcaps. One headlight out.
  - Exhaust smoke.
- **Frequency:** On main roads in `dense_mainland`, 20–40% of vehicles [est].
- **SELECT BY:**
  - Main roads and bus stops in `dense_mainland`, `old_island` and `sprawl`.
  - Few in `elite` interiors.
  - Banned on some corridors (e.g. the planned Lekki-Epe ban) [src Ventures].
- **Variant: korope.** A smaller yellow minivan (older Japanese/European small van) on short feeder routes. Smaller and boxy, with the same livery.

### 3.2 Molue (historical)
- **Look:**
  - Built on a European medium flatbed truck chassis (the "911"-type cab, short bonnet) with a locally made steel passenger body [src Daily Trust/Wikipedia LSTC].
  - Yellow and black livery.
  - Open doorways front and rear.
  - Windows with no glass.
  - Up to about 80 passengers, many standing [src TheCable].
- **Dimensions [est]:** Length 9–11 m, width 2.5 m, height 3.0–3.2 m. Short bonnet about 1.2 m.
- **SELECT BY:**
  - Historical/nostalgia only: a single rusting hulk parked in `sprawl` or `dense_mainland`.
  - Or a "period" scene.
  - Rare otherwise (phased out late 2000s).

### 3.3 BRT and city buses
- **Look:**
  - 12 m high-floor buses.
  - Standard Lagos regulated scheme is **blue and white** [src LAMATA]: blue `#1F4FA0`, white `#F4F4F2`, sometimes a red accent stripe.
  - Two-door mass-transit buses were ordered painted red at one point [src TheCable 2022].
  - Destination LED board.
  - Left-side doors at platform height for median stations.
- **Dimensions:** About 12×2.55×3.2 m. Rebuilt fleets total 434 buses in a 2015 launch [src LAMATA].
- **Gidi:** Invent a single bold scheme for the Gidi transit authority, e.g. blue with white and a band, NOT the real one exactly.
- **SELECT BY:** The BRT lane on expressway corridors, and terminals.

### 3.4 Okada (motorcycle taxi)
- **Bike:** 100–150 cc commuter motorcycles, mostly Indian and Chinese makes. Model generically as an upright standard bike with a long flat seat, carrier rack and crash bars.
  - Body colours: black `#1A1A1A` (most common), red `#B0201C`, blue `#1E3E8C`.
  - Often a fringed seat cover and mudflaps.
- **Dimensions [est]:** Length ~2.0 m, width ~0.8 m, height ~1.1 m, seat height ~0.8 m.
- **Rider:**
  - Helmet required by policy [src TheCable 2012], but passengers often go helmetless.
  - Union **reflective vest** with name and number [src TheCable]. Vest colours in fluorescent green/orange/yellow (`#C8E636`, `#FF7A1A`) or union-coloured (invent).
  - Slippers or sneakers.
- **Load:** 1 passenger typical, sometimes 2. Goods loads (gas cylinders, sacks).
- **Status:** Banned in many Lagos LGAs since 2022 [src Africanews], but still common in back streets and `sprawl`.
- **SELECT BY:**
  - Side streets, `sprawl`, and the outskirts of `dense_mainland`.
  - Clusters of 3–10 parked at junction "okada parks".
  - Few on expressways, bridges or `elite` (banned).
- **Variant:** App-based delivery bikes with a box (invent branding).

### 3.5 Keke (tricycle taxi)
- **Look:**
  - Three-wheel auto-rickshaw.
  - **Yellow body** in Lagos [src TechCabal], with a black canvas or vinyl canopy roof.
  - Roll-down side curtains (black or clear plastic) in rain.
  - Driver front centre, bench for 3 behind (often 4 + 1 beside the driver).
- **Dimensions** (typical Indian 4-stroke autorickshaw) [est from spec sheets]: Length ~2.63 m, width ~1.30 m, height ~1.70–1.75 m, wheelbase ~2.0 m.
- **Colours:**
  - Yellow `#F0C419`.
  - Canopy black `#151515`, faded `#3A3A3A`.
  - Green `#2E8B3A` for electric newcomers (square body) [src TechCabal].
- **Extras:**
  - Stickers and slogans across the rear canopy panel.
  - Union numbers painted on.
- **SELECT BY:**
  - Inner streets, `sprawl` and estate feeders.
  - Restricted on main routes in parts of Lagos.

### 3.6 Private cars
- **Body types [est share]:**

  | Body type | Share |
  |---|---|
  | Mid-size sedans (Japanese mid-90s to 2010s, "tokunbo" = imported used) | 45% |
  | SUVs and crossovers | 25% (60% in `elite`) |
  | Compact hatchbacks | 10% |
  | Pickups | 5% |
  | Minivans and old station wagons | 10% |
  | Luxury SUVs (black, tinted) | `elite` and convoys |

- **Colours [est]:**

  | Colour | Hex | Share |
  |---|---|---|
  | Silver/grey | `#A9ACB0` | 35% |
  | Black | `#141414` | 20% (higher in `elite`) |
  | White | `#F0F0EE` | 15% |
  | Dark blue | `#22304F` | 8% |
  | Champagne/gold | `#B8A47A` | 8% |
  | Dark green, red, other | | 14% |

- **Condition:** Wide range. Bumper dents, faded clearcoat on roofs and bonnets, a mismatched wing, plates.
- **Plates:** Nigerian plate pattern is white with green/blue text and a map motif. **Gidi:** design its own plate pattern.
- **Taxis:**
  - Older yellow-and-black-striped sedan taxis (rare now).
  - Ride-hail looks like any private car.
- **SELECT BY:**
  - Wealth sets age, the SUV share and the black share.
  - Parking density is high in `old_island`, at markets and in VI offices.

### 3.7 Trucks, tankers, trailers
- **Fuel tankers:**
  - Articulated, cylindrical tank 12–13 m.
  - Tank body silver/white with a coloured band or company colours (invent).
  - Very common queued on `port` roads.
- **Container trailers:** 20' and 40' (6.1/12.2 m) boxes in faded corporate shipping colours (rust red `#8F3B2A`, blue `#2A4F7A`, green `#3D6B4A`, grey).
  - Old European/Asian cab-overs and bonneted American-style tractors.
  - Queues for km in `port`, parked two-abreast on roads [est].
- **Tipper trucks** with sand or laterite. Old flatbed lorries with wooden side boards painted with slogans (bolekaja-style art: bright painted bodies, sometimes hand-painted pictures).
- **"Mammy wagon"/flatbed:** Rear tailgate with hand-painted proverbs.
- **SELECT BY:**
  - `port`: trailers and tankers about 60% of traffic.
  - Expressways: 15%.
  - Tippers near construction in `sprawl` and Lekki-like areas.

### 3.8 Police and official vehicles (generic)
- **Police:**
  - Pickups with a canopy or open back with benches, dark blue/black or white with blue bands.
  - Officers sitting in the back. A roof light bar.
- **Traffic agency:** White/yellow cars or pickups with an agency band (invent).
- **Military:** Olive or camouflage trucks near barracks.
- **Checkpoints:**
  - Wooden plank with nails or a tyre on the road.
  - Drums painted red and white.
- **SELECT BY:** Junctions, `port`, `elite` gates, and night checkpoints on expressways.

### 3.9 Other wheeled things
- **Wheelbarrows:** Steel tray, black or galvanised, single wheel, about 1.5×0.6 m. Used to carry goods and water kegs.
- **Push-carts ("truck pushers"):**
  - Long wooden flat cart, about 2.5–3×1.2 m, on two car wheels.
  - Very common in markets and `old_island`.
- **Water vendor carts:** 6–12 yellow 25 L jerrycans ("kegs", `#E0B020`).
- **Hand trucks:** Small two-wheel sack barrows.
- **SELECT BY:** Markets, `old_island` lanes and `sprawl` water-scarce streets.

---

## 4. PEOPLE

### 4.1 Skin tones
- Predominantly dark to medium-dark brown.
- Range [est]: `#3B2219`, `#4A2C20`, `#5C3A28`, `#6E4630`, `#8A5A3C`, lighter `#A8744E` (about 5%).
- Weight the darker half most.
- A few expatriates (lighter tones) in `elite`/VI: ~2–5% there, ~0% elsewhere.

### 4.2 Clothing
- **Western casual (most common, ~50–65% of street people [est]):**
  - T-shirts, polos, jeans, trousers, sneakers.
  - Football jerseys (club colours: red, blue, white).
  - Slippers and slides (very common).
- **Ankara (wax print):**
  - Bold repeating motifs (circles, leaves, concentric shapes).
  - Dominant palettes:
    - Orange `#E86A1C`, indigo `#2B3A8C`, yellow `#F2B705`.
    - Green `#1E8C4E`, red `#C2272D`, magenta `#B0236B`, turquoise `#1FA3A3`.
  - Usually 3–5 colours per print, on a contrasting ground.
  - Worn as a dress, skirt and blouse, shirt, or a wrapper. Common on women (~30–45%) and some men (shirts).
- **Buba and sokoto (men):**
  - Loose top to mid-thigh, round neck, and drawstring trousers.
  - Plain or patterned.
  - Colours: white, cream `#E9E0CC`, sky blue `#9EC5E8`, grey, brown, maroon.
- **Agbada (men, formal):**
  - Wide flowing outer robe (span ~2.5 m when arms open) over buba and sokoto.
  - Often embroidered at the neck.
  - Worn to events, Fridays and Sundays.
  - Fabrics: brocade or damask in navy, wine, cream or white, or lace.
- **Kaftan / senator (men):**
  - Long straight-cut tunic below the knee, plain colours with neat piping.
  - Very common office and smart wear.
  - Colours: black, navy, grey, white, wine, olive.
- **Fila (cap):**
  - Men's soft cap: the folded **abeti-aja** ("dog-ear") or a tall cylinder.
  - Matched or contrasting to the outfit.
  - Hausa-style embroidered round cap in the north-influenced quarters.
- **Gele (head-tie):**
  - Women's stiff head-tie, sculpted high and fan-like (up to 0.3–0.5 m above the head) for events.
  - Everyday, it is a simple scarf tie.
  - Aso-oke or damask in gold `#C9A227`, coral, emerald, purple, silver.
- **Aso-ebi:** Group uniform fabric at parties and weddings. **Everyone in a group wears the same fabric colour**, e.g. 30–200 people in coral and gold. Saturday party streets.
- **Iro and buba (women):** Wrapper skirt plus blouse, with an extra shoulder piece (iborun/ipele).
- **Market women:**
  - Wrapper (ankara or plain) tied at the waist over a blouse or tee.
  - Head scarf.
  - A small purse tied into the wrapper.
  - Head load: basins and bowls (aluminium `#B8B8B4`, plastic in red, blue or green), 0.5–0.7 m across, stacked goods.
- **Hawkers:**
  - Trays (aluminium or wooden, 0.5–0.8 m) on the head with a cloth pad ring.
  - Glass display boxes of snacks.
  - Coolers or basins of drinks and pure water.
  - Hanging bags of goods (phone cards, chargers, puff-puff, plantain chips, newspapers, groundnuts, gala-type sausage rolls: generic).
  - Weave through traffic at go-slows [src Discover Lagos].
- **School uniforms:**
  - Very common morning and afternoon (07:00–08:00, 14:00–16:00).
  - Pinafores or shirt-and-shorts in solid school colours: checked or plain blue `#2E5FA8`, green `#2E7D46`, maroon `#7A1F2B`, purple, yellow, with white or cream shirts.
  - Berets or hats. Backpacks.
  - Children in groups of 2–10.
- **Work uniforms:**
  - Traffic wardens: white shirt + maroon/wine trousers + beret (pattern: two-tone uniform with a cap; invent Gidi's colours).
  - Police: black/dark uniforms.
  - Security guards: dark blue/black with a peaked cap.
  - Waste workers: orange or green overalls.
  - Construction workers: no PPE or a hard hat, bare chest, slippers.
  - Mechanics: oil-stained overalls.
  - Bank staff: suits.
  - Road sweepers: orange vests and brooms.
- **Conductors:** Young men in tees or singlets, hanging at the danfo door, holding a fold of naira notes between the fingers, shouting destinations.
- **Okada riders:** See 3.4. Often a cap or a helmet worn loosely, vest, slippers or shoes.
- **Religious dress:**
  - White garment churches: white robes, barefoot.
  - Muslim men: white jalabiya, kufi caps.
  - Women: hijab in many colours. Common on Fridays.
- **SELECT BY:**

  | Context | Mix |
  |---|---|
  | `elite`/VI office | Kaftan/senator, suits, western smart; fewer wrappers |
  | Markets | Wrappers, head loads, hawkers, push-carts |
  | Saturday afternoon near halls | Agbada, gele, aso-ebi clusters |
  | Friday near mosques | Jalabiya, caps |
  | Sunday morning near churches | Smart traditional |
  | Weekday 07–08 and 14–16 | School uniforms |
  | `sprawl` | Casual and labour wear |

### 4.3 Crowd density [est, persons per 100 m of street frontage]
| Place / time | Density |
|---|---|
| Market street, `old_island`, 10:00–16:00 | 150–400 (shoulder-to-shoulder; street fully occupied) |
| Bus stop or junction under a bridge (Oshodi-type), rush hour 06:30–09:30, 17:00–20:00 | 100–300 |
| `dense_mainland` main road, daytime | 40–100 |
| `dense_mainland` residential street, evening | 20–50 (people outside on chairs) |
| `sprawl` street | 5–20 |
| `elite` estate street | 0–5 (guards, drivers, gardeners, a hawker) |
| `elite` VI commercial | 10–40 |
| `port` truck queue | 10–30 (drivers, mechanics, food sellers) |
| `waterfront` | 20–60, many in canoes |
| Night 22:00+ | ×0.1–0.3, but bus parks and night markets stay busy |

- Walkers use the road edge where the walkway is blocked.
- The share standing still (traders, people waiting) is 30–60% in markets.

---

## 5. SIGNAGE

### 5.1 Hand-painted signs
- **Lettering:**
  - Bold sans or block capitals, often with a drop shadow or outline.
  - Slightly uneven baseline. Mixed sizes.
  - Prices or phone numbers in a contrasting colour.
  - Simple painted pictures: a haircut head for a barber, a cut glass for a beer bar, a tyre for a vulcaniser, a jerrycan.
- **Background colours:**
  - White `#F2F0E8`, yellow `#F2C200`, sky blue `#4DA6E0`, red `#C72A22`, green `#1E8C4E`.
- **Text colours:** Black, red, blue.
- **Boards:**
  - Plywood or zinc sheet 0.6×1.2 m to 1.2×2.4 m.
  - Nailed to a wall above the doorway or on 2 wooden or steel poles about 2–3 m high at the street edge.
  - Arrow boards ("→ 50m").
- **Barber, salon and tailoring signs** often paint example portraits.
- **Weathering:** Faded, peeling flakes, rust streaks from nails, sun-bleached reds to `#D87A6E`.
- **Frequency [est]:**

  | District | Hand-painted share of shop signs |
  |---|---|
  | `dense_mainland` | 40% |
  | `sprawl` | 60% |
  | `old_island` | 25% (more flex) |
  | `elite` | <5% |

### 5.2 Printed flex banners
- **Look:**
  - PVC flex print, glossy, saturated colours, photographic.
  - Stretched on a wood or steel frame or tied with rope at the grommets.
  - Bank-, telecom- or drink-sponsored shop fascia: the sponsor's brand colour fills the board with the shop name in a corner. **Gidi:** invent sponsor colours, e.g. a fictional telco in purple.
- **Sizes:** Shop fascia 0.6–1.2 m tall × shop width (3–6 m). Event banners 1×3 m to 2×6 m strung across streets or on fences.
- **Event banners:** Burial ("Celebration of Life" with a portrait), birthday, church crusade, political ("Vote" with a face), "Grand Opening". Event colours are bright gradients.
- **Weathering:** Sagging, torn corners, fading of cyan first (yellow and magenta tint remains).
- **SELECT BY:**
  - Main roads and commercial streets.
  - Event banners near halls and churches, and on Friday or Saturday.
  - Political banners: everywhere in election season.

### 5.3 Wall paint and stencils
- **Phone numbers:** Painted large (0.15–0.3 m digits) on walls, with offers like "Borehole Drilling", "Tiles", "We Buy Scrap", "Land For Sale", "Plumber". 1–3 per wall stretch in `dense_mainland`/`sprawl` [est].
- **"THIS HOUSE IS NOT FOR SALE / BEWARE OF 419":**
  - Spray-painted or brushed on walls and gates of empty or disputed houses [src Somerset House, Eyes of a Lagos Boy].
  - Usually red or black, rough hand.
  - Sometimes with "BY ORDER" or "Family of …".
  - Frequency: one per 20–50 houses on older streets [est].
- **"POST NO BILL":** Black or red capitals on walls and fences. Often ignored, so posters sit right beside it.
- **"DO NOT URINATE HERE"** (sometimes with a threat), "NO PARKING", "NO WASTE DUMPING".
- **Government marks:**
  - Red "X" or "Remove" plus a stencil code: a demolition or contravention notice.
  - Building-control stencils.
  - Red X marks with a date.
- **Posters:**
  - A4 to A2 paper posters pasted in rows and grids on walls, poles and bridge columns.
  - Content: churches, crusades, burial notices with photos, parties, lessons, political.
  - Peeling layers.
- **SELECT BY:** Walls along `dense_mainland`, `old_island` and `sprawl` streets. Rare in `elite`, which has clean painted walls with razor wire.

### 5.4 Shop signs
- **Placement:**
  - Above the shop door or shutter, 2.2–3.5 m up.
  - Sometimes projecting.
  - A-frame boards on the walkway.
- **Size:** Shop fascia 0.6–1.0 m high × 2.5–6 m wide.
- **Shop units:** Typically container-like 2.5–3.5 m wide lock-up shops with steel roller shutters (grey `#8C8C8C`, often stencilled with the shop name) or folding steel doors.
- **Also:**
  - Converted **shipping containers** as kiosks (painted in sponsor colours).
  - Phone-card and POS kiosks with umbrella.

### 5.5 Vehicle text (danfo, keke, trucks)
- **Types:**
  - Rear-window stickers, top-windscreen strip lettering (gold or white on dark).
  - Religious phrases, proverbs, humour, names.
- **Typeface:** Stencil, block or decorative.
- **Gidi:** Original slogans only.

---

## 6. PROPS AND STREET LIFE

### 6.1 Market stalls by type
- **Common structure:**
  - Wooden table or stall about 1.2–2×0.8–1 m, 0.8–0.9 m high.
  - Covered by a corrugated zinc roof (galvanised `#9EA3A6`, rusted `#8A5A3A`) on wooden poles, 2.0–2.4 m high.
  - Or a tarpaulin (blue `#2F5FA8`, green, orange) or a big umbrella.
  - Rows 1–1.5 m apart.
- **Food market:**
  - Basins and enamel bowls of tomatoes (`#D8352A`) and peppers (scotch bonnet red/yellow).
  - Onions in sacks.
  - Yams stacked.
  - Plantain bunches (green `#5D8A2A` to yellow).
  - Dried fish, stockfish (grey-brown).
  - Garri and rice in open sacks with measuring tins ("paint-bucket" or "derica" cups).
  - Palm oil in jerrycans (orange-red `#B8471C`).
  - Sitting traders on low stools.
- **Spare parts market (Ladipo-type, used parts) [src Proshare]:**
  - Engines and gearboxes on the ground.
  - Tyres stacked.
  - Bumpers leaned on walls.
  - Ground oil-soaked black.
  - Rusty, dark palette.
- **Electronics (Alaba / Computer Village-type) [src]:**
  - Lock-up shops and stalls with phone cases.
  - Speakers, TVs and boxes stacked high outside.
  - Glass display cabinets.
  - Bright flex banners.
  - Branded umbrellas.
  - Crowded alleys 2–4 m wide.
- **Cloth (Balogun-type):**
  - Bolts of ankara, lace and aso-oke stacked and hung.
  - Fabrics draped from rails.
  - Lanes 2–3 m wide, multi-storey plazas.
  - Very high colour saturation.
- **Pots and plastics:** Stacks of coloured plastic basins, buckets, chairs, aluminium pots.
- **SELECT BY:**
  - Food markets in every district except `elite` (which gets a small "mallam" kiosk).
  - Parts markets in `dense_mainland`.
  - Cloth and electronics in `old_island` and in market districts.

### 6.2 Umbrellas
- **Look:**
  - Large market or beach umbrella, 2.0–3.0 m diameter, 2.2–2.5 m high.
  - Pole set in a tyre-and-concrete or bucket base.
  - 8 panels, sponsor-branded in a corporate colour, alternating with white.
- **Colours** (use invented Gidi brands):
  - Telecom-yellow `#FFCC00`.
  - Telecom-green `#00A651`.
  - Telecom-red `#E2231A`.
  - Bank orange `#F26A21`.
  - Purple `#5B2C83`.
  - Drink blue.
- **Older:** Plain faded rainbow-panel umbrellas.
- **Weathering:** Fading, mismatched panels, torn edges.
- **Frequency:** 1 per 2–5 stalls in open markets [est]. Phone-card, POS and recharge points always have one.
- **SELECT BY:** Markets, bus stops, junction kiosks, walkway traders.

### 6.3 Plastic chairs and tables
- **Look:** Monobloc stackable plastic chairs (white `#F2F2F0`, red `#C8282A`, blue `#2C5DA8`, green `#2E8B3A`) and matching square tables.
- **Dimensions:**
  - Chair seat height 0.45 m, overall height 0.8 m.
  - Table 0.7–0.8 m square, 0.7 m high.
- **Uses:**
  - Beer parlours, roadside food spots ("bukka"), barbers, waiting areas.
  - Event canopies: white or striped canopy tents 3×3 m to 6×12 m with rows of chairs (Saturday parties; block the whole street).
- **SELECT BY:** Bars and food spots on streets, evening scenes, party days.

### 6.4 Generators
- **Small ("I-better-pass-my-neighbour" class, 0.65–1 kVA):**
  - Red or yellow plastic and steel open frame, about 0.4×0.35×0.35 m.
  - Ubiquitous at small shops and kiosks.
  - Red `#C8201E`, yellow `#F2C200`.
- **Medium (2.5–7 kVA):**
  - Open tube frame or box, 0.6–0.8 m.
  - Shops and homes.
  - Black, red or yellow-green.
- **Large (20–500 kVA "soundproof"):**
  - Sheet-metal canopy boxes 1.5–5 m long, 1–1.5 m wide, 1.2–2 m tall.
  - Grey, green, cream or blue.
  - Exhaust pipe up a wall.
  - Inside a welded **steel cage** (anti-theft) or a block enclosure.
  - Diesel tank and stains below (`#2A2622`).
- **Frequency [est]:** In `dense_mainland`, at least one generator outside every 1–3 shops. In `elite`, one large caged unit per compound.
- **SELECT BY:**
  - Size scales with wealth and building size.
  - Night or outage scenes add exhaust haze and noise.

### 6.5 Water tanks
- **Look:**
  - Rotomoulded plastic tanks, black `#1A1A1A` (most common) or blue/white/beige.
  - Corrugated cylindrical body.
- **Sizes:**
  - 500 L (Ø0.8 m × 1.1 m).
  - 1,000 L (Ø1.1 × 1.3 m).
  - 2,000 L (Ø1.4 × 1.6 m).
  - 5,000 L (Ø1.9 × 2.1 m).
- **Mounting:** On rooftops or on **steel stands** 3–6 m tall (angle-iron towers) next to houses, often fed by a borehole.
- **Frequency:** One per building in most districts. In `elite` it is hidden on roofs.
- **SELECT BY:** Every building. Also communal borehole tanks plus tap stands with jerrycans in `sprawl`.

### 6.6 Night lighting
- Fluorescent tubes (`#E6F5FF`), cold LED strip lights and bare bulbs (`#FFD27A`) from shops.
- Kerosene lanterns, now rare.
- Rechargeable LED lamps on hawker trays.
- Phone torches.
- Roadside fires for roasting corn and suya grills (orange `#FF7A1A` glow plus smoke).
- Generator-powered.
- Most side streets are dark apart from shopfronts.
- Headlight streams on expressways.
- LED billboards in `elite`.
- **SELECT BY time:** At dusk (18:30–19:30), the light shifts sharply to orange-pink and road haze rises. After 19:00, trader lamps and generator hum.

### 6.7 Refuse heaps and litter
- **Refuse heaps:**
  - On medians, under bridges, at drain ends and on empty plots.
  - 1–5 m piles of black and coloured nylon bags (`#1C1C1C`, blue, red), food waste and ash.
  - Often smouldering.
  - Waste bins rare. Large green or blue skip containers at official points in `elite`/main roads.
- **Litter:**
  - **Pure water sachets** (500 mL clear plastic pouches, printed in blue or green; torn empties are the dominant litter item) [src SmartCitiesDive].
  - Black and coloured nylon bags.
  - PET bottles.
  - Styrofoam takeaway packs (white).
  - Energy-drink cans.
  - Corn husks and orange peels.
- **Density [est]:**

  | District | Pieces per m² of road edge and drain |
  |---|---|
  | `dense_mainland` | 10–40 |
  | Markets | 50+ |
  | `elite` | <1 |

- **SELECT BY:** Inverse wealth. Peaks at markets, bus stops, under bridges and in drains.

### 6.8 Other props
- **Gas cylinders:** 12.5 kg (green or blue) at refill points.
- **Vulcaniser stands:** Tyres, a compressor and a painted sign.
- **Phone-charging stands and POS umbrellas.**
- **Fuel in jerrycans:** Yellow or grey, sold at roadside during scarcity.
- **Suya spot:** Grill with charcoal glow, at night.
- **Corn roasters:** Metal pan grill.
- **Tyres:** Stacked tyres and tyre planters painted white, used as boundary markers.
- **Abandoned vehicle hulks:** About 1 per 300 m in `dense_mainland`/`sprawl` [est].
- **Barbed or razor wire and broken-glass tops** on walls (`elite`: electric fence wires plus coiled razor).
- **Security sheds and gatehouses** at estate entrances, with a boom gate in red and white.
- **Mosque and church loudspeakers** on poles.
- **Wooden kiosks:**
  - Painted in sponsor colours, ~1.5×1.2×2.2 m.
  - A "mallam" provisions kiosk with tins stacked high.
- **Vendors' tables of phone accessories.**
- **Bicycle and pushcart ice-cream** (generic: a box on the bike with a bell).
- **Plastic jerrycans:** Everywhere. Yellow `#E8B420`, blue.

### 6.9 Trees and plants
- **Street tree census:** 4,017 street trees across 16 LGAs, 46 species, 87% non-native [src Trees, Forests and People 2024].
  - Top species by far: **Polyalthia longifolia (mast tree / "masquerade tree")** at 27.3%. Tall narrow columnar conifer-like tree, 8–15 m, drooping dark green leaves `#2E4A22`, planted in rows along fences.
  - Ikeja had the most street trees. Lagos Island had only 2 in the survey.
- **Other common trees [est from general imagery]:**
  - **Indian almond (Terminalia catappa).** 10–20 m, tiered horizontal branches, leaves large and glossy, turning red `#B23A26` before falling.
    - Very common in compounds and as shade at bus stops and mechanic spots.
    - Fruit litter.
  - **Neem.** 8–15 m, fine leaves, dense shade. More in the north-influenced and older quarters.
  - **Coconut palm.** 15–25 m, leaning. Beaches, VI, Lekki and the `waterfront`.
  - **Oil palm.** Shaggy trunk, 10–15 m. `sprawl`, vacant plots.
  - **Royal and foxtail palms.** `elite` boulevards, medians and estates.
  - **Flame tree (Delonix regia).** Red bloom `#E2442A` (dry season). Gardens and older GRAs.
  - **Mango** (dense dark round crown) and **pawpaw** in compounds.
  - **Banana/plantain** clumps by houses.
  - **Weeping fig and ficus** in `elite`.
  - **Bamboo clumps.**
  - **Mangroves** at the lagoon edge (`waterfront`).
- **Ground plants:**
  - Spear grass and weeds in cracks.
  - Bougainvillea over walls (magenta `#C2185B`, orange).
  - Ixora and croton hedges.
  - Potted plants on concrete planters.
  - Water hyacinth mats on lagoon water (`#4E7A2E`).
- **SELECT BY:**
  - `elite`: tree-lined (palms, Polyalthia, old canopy).
  - `old_island`: almost no trees.
  - `dense_mainland`: an occasional almond or neem at junctions.
  - `sprawl`: palms, mango and bush on vacant plots.
  - `waterfront`: coconut and mangrove.

---

## 7. DISTRICT PROFILES (how it all varies)

| Feature | dense_mainland | old_island | elite | sprawl | waterfront | port |
|---|---|---|---|---|---|---|
| Road state | Patched, potholes 2–6/100 m | Narrow, congested, patched | Smooth, marked, speed bumps | Laterite lanes, craters | Plank walkways, canals | Cratered, truck-churned |
| Kerb paint | Faded yellow/black | Faded | Fresh black/white or yellow/black | Rare | None | Faded, broken |
| Drains | Open, choked | Open, deep | Covered/grated | Earth ditches | Lagoon | Open, oily |
| Walkway | Pavers, fully traded on | Fully traded on | Pavers, empty | Earth | Boardwalk | Truck-parked |
| Poles and wires | Concrete, dense tangle | Old wooden and concrete, tangles | Few or underground | Concrete, sparse, leaning | Few, improvised | Concrete |
| Vehicles | Danfo 30%, keke, okada, tokunbo cars | Cars, push-carts, danfos at edges | SUVs, ride-hail, few danfos | Okada, keke, danfo, tippers | Canoes (dugout, 4–10 m) | Tankers, trailers 60% |
| People / 100 m | 40–100 | 150–400 | 0–40 | 5–20 | 20–60 | 10–30 |
| Signage | Hand-painted + flex | Flex dense, cloth/electronics | Corporate, clean | Hand-painted, phone numbers | Minimal | Company signs, fuel |
| Refuse | Heaps under bridges | Market litter | Clean | Vacant-plot dumping | Water litter, sachets | Oil, tyres |
| Trees | Few | Almost none | Many | Palms, mango, bush | Coconut, mangrove | Few |
| Night | Shop fluorescents, generators | Busy till ~21:00 | Street lamps, LED boards | Dark, solar lamps | Lanterns, very dark | Truck lights, floodlights |

**Waterfront (Makoko-like) details [src Makoko sources]:**
- Houses on hardwood stilts driven into the lagoon bed. Walls of planks, roofs of corrugated iron, plus bamboo and polythene.
- Dugout canoes for transport and as floating shops (women selling food and water).
- Water dark brown-green `#4A4A32`.
- Smoke from fish-smoking.
- **Gidi:** Stilt villages of 1–2 storey plank houses (wood `#7A5A3C` weathered to `#8E8676`) on 0.15–0.25 m poles, 1–2.5 m above water.

**Time of day:**
- 05:30–07:00: dawn rush, workers, school children start.
- 07:00–10:00: peak traffic ("go-slow"), hawkers in traffic.
- 10:00–16:00: market peak.
- 16:00–20:00: evening rush.
- 18:30–19:15: dusk, sky orange to purple.
- 20:00+: bars, suya and food spots lit, generators on.
- Sanitation days (historic, monthly Saturday mornings): empty streets.

---

## Sources
- https://theautopian.com/why-nigerias-danfo-bus-drivers-might-be-the-craziest-and-most-skilled-drivers-on-the-planet
- https://en.wikipedia.org/wiki/Volkswagen_Type_2_(T3)
- https://www.redbull.com/ng-en/events/red-bull-danfo-rally/red-bull-danfo-rally-what-is-a-danfo
- https://ikejarecord.com/danfo-tales-surviving-lagos-as-a-bus-driver
- https://culturecustodian.com/the-danfo-story-on-lagos-enduring-cultural-icon/
- https://venturesnewsletter.substack.com/p/the-danfos-last-bus-stop
- https://naija.yafri.ca/governor-ambode-going-phase-danfo-buses-lagos/
- https://www.ecofinagency.com/public-management/1303-36593-nigeria-lagos-to-kick-start-bus-reform-initiative-with-97-million
- https://dailytrust.com/in-lagos-last-days-of-the-molue/
- https://en.wikipedia.org/wiki/Lagos_State_Transport_Corporation
- https://lifestyle.thecable.ng/?p=161384
- https://www.lamata-ng.com/bus-services/
- https://www.ssatp.org/sites/ssatp/files/2018_Annual_Meeting_Abuja/Day3/UTM/LAMATA%20-%20BRT%20Development%20and%20Associated%20Institutional%20Building%20Aspects%20%282%29_.pdf
- https://blogs.worldbank.org/en/transport/urban-transport-lagos-shows-africa-way-forward-again
- https://www.thecable.ng/?p=519941
- https://techcabal.com/2026/03/19/a-ride-in-bolt-three-wheelers/
- https://www.africanews.com/amp/2022/06/01/ban-on-motorbike-taxi-okada-begins-in-nigeria-s-lagos/
- https://www.thecable.ng/?p=218335
- https://www.thecable.ng/?p=769097
- https://archive.businessday.ng/breaking-news/article/lagos-to-sue-tan-others-over-illegal-road-adverts/
- https://von.gov.ng/lagos-opens-18-7km-six-lane-expressway/
- https://guardian.ng/?p=1292956
- https://pulitzercenter.org/node/30445
- https://openjicareport.jica.go.jp/pdf/11846656_02.pdf
- https://papersizes.io/billboard
- https://www.adquick.com/answers/billboards/standard-billboard-dimensions-and-common-out-of-home-advertising-formats
- https://schoolings.org/costs-advert-rates-of-non-digital-digital-billboards-advertising-in-lagos-state-latest-prices/
- https://abiastate.gov.ng/wp-content/uploads/2025/02/ABSSAA_RATES_UPDATED1.pdf
- https://www.discoverlagos.ng/post/the-lagos-go-slow-a-tourist-s-unexpected-cultural-experience
- https://www.smartcitiesdive.com/ex/sustainablecitiescollective/clean-drinking-water-lagos-many-options-few-solutions/55571/
- https://www.somersethouse.org.uk/whats-on/the-419
- https://eyesofalagosboy.com/2023/08/28/photo-of-the-week-this-house-is-not-for-sale/
- https://doaj.org/article/7f33da4b4a0d49d8bbdac9205ca910d8 (Lagos street tree census, Trees, Forests and People 2024)
- https://guardian.ng/property/lagos-government-ikoyi-residents-bicker-over-trees-felling-parks-destruction/
- https://www.wathi.org/inside-makoko-danger-and-ingenuity-in-the-worlds-biggest-floating-slum-tolu-ogunlesi-the-guardian/
- https://www.amusingplanet.com/2014/04/makoko-floating-slum-in-nigeria.html
- https://kuwaittimes.com/article/38836/world/demolitions-cast-adrift-residents-of-africas-biggest-floating-slum/
- https://urbannext.net/alaba-2/
- https://proshare.co/articles/tinubu-reopens-ladipo-market

Caveat: Lagos government agencies (LASAA, LAMATA, the Ministry of Works) publish no structure or road-width specs online that I could find. Most dimensions marked [est] are calibrated from comparable standards and photo knowledge, and should be checked against reference photos before they are hard-coded.
