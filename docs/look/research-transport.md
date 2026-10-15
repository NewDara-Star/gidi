# Gidi transport and infrastructure catalogue

Research for the seeded Blender kit. Rule zero applies: real Lagos is studied as a pattern only. All names, liveries and logos in the kit must be invented; real places below are examples of a pattern, not things to copy.

Builds on `docs/look/research-street.md` §2 (poles, transformers, lamps, bus stops, footbridges) and §3.7 (trucks). This file goes deeper on those items and covers the large transport structures that the street file leaves out.

Tags: **[src]** means the figure comes from a listed source. **[est]** means an estimate from photos and engineering norms. Hex colours are always approximations.

District keys (as in the kit): `dense_mainland`, `sprawl`, `old_island`, `elite`, `civic`, `waterfront`, `port`.

---

## Summary table

| # | Item | Scale | Key districts | Gidi census items |
|---|------|-------|---------------|-------------------|
| 1 | Multi-storey bus interchange | 3 storeys, ~30,000 m² per terminal | civic, dense_mainland hubs | "Gidi Interchange", "terminal" |
| 2 | Motor park (intra-city) | 0.2–1.5 ha | dense_mainland, old_island, sprawl | "Boss's motor park", "Island Motor Park" |
| 3 | Interstate coach terminal | 0.5–3 ha | dense_mainland edges, sprawl gateways | "Northern Bus Park" |
| 4 | BRT lane and station | 20–40 m station | expressway corridors | BRT station, BRT lane |
| 5 | Colonial narrow-gauge line and station | single storey + long shed | old_island, dense_mainland | old rail station, rail corridor |
| 6 | New light-rail viaduct and elevated station | 8–10 m deck | civic, dense_mainland, old_island | new rail station |
| 7 | Level crossing and rail corridor with shanties | 15–30 m strip | dense_mainland | level crossing, corridor shanties |
| 8 | Truck park and trailer queue | 1–10 ha / km-long queue | port, dense_mainland | "truck park", "trailer" |
| 9 | Container yard and stacks | hectares | port | "stack", "Container Yard" |
| 10 | Port cranes (mobile harbour, STS, RTG) and reach stackers | 25–80 m | port | "crane" |
| 11 | Customs shed and port gate | 20–80 m sheds | port | customs shed, gate |
| 12 | Airport perimeter fence and approach lights | km-long | sprawl/civic edge | "Airport Fence" |
| 13 | Jetties: canoe, ferry terminal, speedboat, barge | 5–60 m | waterfront, old_island, elite | "Canoe Jetty", "jetty" |
| 14 | Flyover and life under it | 400–1,500 m | dense_mainland, old_island | "Under the Bridge" |
| 15 | Pedestrian footbridge / skywalk | 30–60 m span | expressways | footbridge, skywalk |
| 16 | Long lagoon bridge | 10–12 km | crosses lagoon | "Long Bridge" |
| 17 | Cable-stayed toll bridge | ~1.4 km, 90 m pylon | elite | "Cable Bridge" |
| 18 | Toll plaza | 60–150 m wide | elite/sprawl expressway | "toll booth" |
| 19 | Checkpoints (several agencies) | 10–40 m | everywhere except elite core | checkpoint |
| 20 | Roundabouts with statues; interchanges and ramps | 30–80 m dia | civic, elite, dense_mainland | roundabout, interchange, ramp |
| 21 | Power: 33/11 kV lines, poles, transformers | | all | pole, line, transformer |
| 22 | Telecom masts (ground and rooftop) | 15–60 m | all | mast |
| 23 | Street lights (grid and solar) and CCTV | 6–12 m | all | street light, CCTV |
| 24 | Canals, footbridges, culverts | 5–60 m wide | dense_mainland, waterfront | "Gang Canal", "Canal 7", culvert |
| 25 | Pipelines and pipeline right-of-way | 0.3–1 m pipes | sprawl, port, dense_mainland | pipeline |

---

## 1. Multi-storey bus interchange ("Gidi Interchange", "terminal")

**Pattern:** the Oshodi interchange. It is three multi-storey terminals that replace 13 informal parks under and around an expressway knot. Each terminal is about 30,000 m² [src estateintel/Wikipedia]. Pedestrian bridges and skywalks link them [src Planet Projects]. The design target was about 1 million passengers a day, but only about 6,400 a day used it in the first year [src ThisDay]. The developer counts 5,600 bus loadings a day across the parks it replaced [src Planet Projects]. The terminals were designed for about 820 buses [src Wikipedia]. A redesign to link them with rail has been announced [src BusinessDay].

- **Looks like:**
  - A long, low, three-storey block, 120–200 m × 60–90 m [est].
  - Bus decks with ramps: buses load on the ground floor and on a ramped first deck. Passenger concourses, shops and offices sit above [est].
  - Floor plates are exposed concrete. Façade bands are metal cladding or perforated screens in state colours (blue/white/yellow) [est]. A large back-lit name sign sits on top.
  - Enclosed glazed skywalks 4–5 m wide run to the other terminals and over the expressway [est].
  - CCTV and floodlight towers, 15–25 m high, stand in the forecourt [est].
  - At street level just outside, the informal park comes back: danfos, hawkers and touts crowd the edges.
- **Kit parts:**
  - `term_block`: 3 storeys, floor-to-floor 5.0 m on the bus deck and 4.0 m above [est]. Columns 0.8 × 0.8 m on a 10–12 m grid [est]. Upstand parapets 1.1 m high.
  - `bus_ramp`: 7–8 m wide, slope 1:12, with a concrete parapet [est].
  - `loading_bay`: a saw-tooth or linear island 3.5 × 15 m per bay, with a canopy and a route-number sign. 20–40 bays per deck [est].
  - `skywalk`: a box truss 4.5 m wide × 3.5 m high. Glazing or perforated panels. Span 30–45 m. Underside clearance 5.5–6.0 m over roads [est].
  - `cctv_tower`: a 20 m lattice or tapered tube with 3–6 camera heads and a floodlight crown [est].
  - `ticket_kiosk`: 2 × 2 m glazed booth.
  - `rooftop_sign`: 1.5–2.5 m letters.
- **Colours:**
  - Concrete `#B9B4A8` (new) to `#8E8A80` (worn).
  - Cladding blue `#1F4E9A`, white `#F2F2EE`, accent yellow `#F2C230`.
  - Skywalk steel grey `#6E747A`.
  - Glass tinted blue-green `#5D7F86`.
- **Materials:** RC frame, aluminium composite panels, steel trusses, polycarbonate or glass roofs over the bays, epoxy-painted floors with bay markings.
- **Variants:**
  - Flagship 3-terminal hub with skywalks (1 per city).
  - Smaller 1–2 storey terminal at a secondary hub (2–4 per city): about 60 × 40 m, one deck [est].
  - Garage-style "modern park" built by the union: a single-storey shed plus offices.
- **Condition states:**
  - **New:** clean cladding, lit signs, working escalators.
  - **Worn:** dark streaks under every slab edge, dead sign letters, escalators stopped, mesh torn on the skywalks.
  - **Decayed:** hawkers inside the concourses, cladding panels missing, standing water on the bus deck, floodlights dark.
  - **Half-built or abandoned:** a bare RC frame with rebar starter bars and blue plastic sheeting.
- **Props and life:**
  - **Day:** queues at the bays, uniformed staff in reflective vests, state buses (blue/white or red), danfos at the edge, wheelbarrow porters, sachet-water sellers.
  - **Night:** floodlit deck, buses parked in rows overnight, security guards. Generator hum.
- **SELECT BY:** the biggest `dense_mainland` or `civic` node where 3+ main roads, a rail line and a flyover meet. Exactly one flagship. Smaller terminals sit on main roads with distance to an arterial of 0.
- **Gidi mapping:** "Gidi Interchange", "terminal".

---

## 2. Motor park, intra-city ("Boss's motor park", "Island Motor Park")

**Pattern:** open, union-run parks such as those under and beside bridges and at market edges. Touts ("agbero") charge drivers about ₦3,000 or more a day [src ICIR]. A driver may pay a loading fee equal to one or two passengers' fares each time the bus loads [src Ikeja Record]. The state has banned the union from parks more than once, yet the agberos come back in plain clothes [src TheCable, Daily Trust].

- **Looks like:**
  - An unpaved or patchy asphalt yard with red-earth puddles. Danfos (yellow with black stripes) are nose-in in rows, labelled by destination.
  - A walled perimeter with a gate arch: two block pillars carrying a painted sign board ("XYZ BRANCH, UNIT ...", invented) [est].
  - A union office: a one-room block or a container, with a painted name panel, a bench outside, and an umbrella.
  - The levy table: a plastic table under a beach umbrella at the exit, with a ticket book and a tin box.
  - Food shacks, a mechanic corner, a mosque or prayer mat area, and a public toilet with a "PAY ₦50" sign.
- **Kit parts:**
  - `park_yard`: 40 × 60 m to 100 × 150 m [est].
  - `gate_arch`: two 0.6 × 0.6 m pillars 3.5–4.5 m high, sign board 6–10 × 1.2 m [est].
  - `union_office`: a 3 × 4 m block hut, 2.8 m high, with a corrugated mono-pitch roof and a painted door (green `#2E7D32`, blue `#1F4E9A` or white with red text). Or a 20-ft shipping container office with a cut door and window [est].
  - `levy_table`: a 0.8 × 0.8 m plastic table, 2 chairs and a 2 m umbrella (red/white or a brand print).
  - `loading_lane`: a painted or chalked line. A destination board on a pole: wood 0.6 × 0.4 m, hand-painted ("OSHODI"-style names invented).
  - `shack`: 2.5 × 3 m timber frame with a zinc roof (food, phone charging, POS).
  - `loader_shelter`: steel posts holding a 6–12 m zinc canopy over a bench.
- **Colours:**
  - Laterite `#A6573A` and mud `#6E4A33`.
  - Danfo yellow `#F2B705`.
  - Zinc `#9AA0A4` (new) to rust `#8A4B2A`.
  - Union office paint in green/white or a party colour.
- **Materials:** compacted laterite, broken asphalt, block, zinc sheet, timber, tarpaulin.
- **Variants:**
  - Open lot (55%).
  - Under-bridge park (25%, see item 14).
  - Roadside "garage" along a kerb (15%).
  - Concreted "modern" park with shelters (5%).
- **Condition states:**
  - **New/regulated:** paved, painted bays, state signboard, shelters.
  - **Worn:** potholes, faded paint.
  - **Decayed:** flooded hollows, refuse heap, wrecked buses on blocks.
  - **Contested or abandoned:** gate locked, a taped government notice ("SEALED BY ORDER OF ..."), yard empty.
- **Props and life:**
  - **Day:** callers shouting the destination, drivers under the shade, hawkers with trays on their heads, POS umbrellas, wheelbarrow pushers, keke queue at the gate.
  - **Night:** a few buses sleeping inside, a fire in a drum, generator light at the food shack, guards on a bench.
- **SELECT BY:** `dense_mainland` / `old_island`, with a market nearby and distance to a main road < 50 m. One per 1–2 km² in dense areas. In `sprawl`, one at each junction town. Never inside `elite` cores. A "Boss's" park gets a bigger office, painted portraits, and a flag.
- **Gidi mapping:** "Boss's motor park", "Island Motor Park".

---

## 3. Interstate coach terminal ("Northern Bus Park")

**Pattern:** company-run luxury-bus parks, once clustered on one street and later moved to designated peripheral sites with a concessionaire [src Daily Trust, BusinessDay]. Companies have their own walled yards with a waiting lounge and ticketing [src intercity.ng].

- **Looks like:**
  - Walled compounds side by side along a road. Each has a sliding gate and a large company sign in bold colours (invent the liveries).
  - Inside: a 2-storey office and lounge block with a glazed ticket counter, a long open-sided waiting shed with rows of plastic or metal seats, and a luggage scale.
  - 12 m coaches (white with diagonal colour stripes) parked herringbone. Some are double-axle, 45–59 seats.
  - A northern-route variant has an open lot of older 18-seat buses and lorries with goods on the roof racks, plus a mosque.
- **Kit parts:**
  - `coach_yard`: 50 × 80 m [est].
  - `lounge_block`: 2 storeys, 20 × 10 m, with a canopy across the front [est].
  - `waiting_shed`: 30 × 8 m on steel portal frames, ridge 5 m [est].
  - `coach`: 12 × 2.55 × 3.6 m [est].
  - `company_sign`: a 8 × 2 m board on a 6 m pole.
  - `luggage_cage`: 3 × 3 m mesh.
- **Colours:** coach white `#F4F4F2` with stripe red `#C62828`, green `#2E7D32` or blue `#1565C0`. Sheds are blue zinc `#3B6EA8`.
- **Variants:**
  - Company yard (60%).
  - Shared state terminal (20%).
  - Informal northern park with lorries (20%).
- **Condition states:**
  - **New:** clean terminals with tiled lounges.
  - **Worn:** rust-streaked sheds, buses with bald tyres.
  - **Abandoned:** a sealed company office with a padlocked gate.
- **Props and life:** porters, bags wrapped in "Ghana-must-go" checked sacks, cattle or yam on the northern lorries, night departures 5–6 am with headlights and a crowd.
- **SELECT BY:** the edge of `dense_mainland` or a `sprawl` gateway on the expressway out of the city, with distance to an expressway < 200 m. The northern park sits near a market for grain, cattle or onions.
- **Gidi mapping:** "Northern Bus Park".

---

## 4. BRT lane and station

**Pattern:** median-running BRT with a bus station on each side, reached by pedestrian bridges [src LAMATA/BusinessDay]. On one extension corridor, an old road 7.5 m wide with a 2 m median was widened with two new BRT lanes [src LAMATA]. That corridor plan had 15 stations at 8 locations, plus 7–10 footbridges [src BusinessDay/Channels]. The regulated bus colours are blue and white [src LAMATA]. Users complain that the footbridges are too far apart and too high, and a study suggested adding lifts [src NITT study].

- **Looks like:**
  - Two kerbed bus lanes in the median, with yellow/black separator blocks and "BRT ONLY" painted in the lane.
  - A station island 0.9–1.0 m high (to match the bus floor), with a long steel shelter, a turnstile hut at the ramp end, and a ramp to a footbridge.
  - The roof is a curved metal or polycarbonate sheet in blue/white. Station names on a lit panel.
  - Older "first-generation" stops are just a raised kerb with a small shelter.
- **Kit parts:**
  - `brt_lane`: 3.5–3.65 m per lane, a separator kerb 0.3 m high × 0.3 m wide [est], and a red or plain asphalt surface.
  - `brt_station`: a platform 25–45 m × 3.5–5 m × 0.9 m. Columns at 5–6 m centres, canopy height 3.2–3.5 m [est].
  - `ticket_booth`: a 2.5 × 2.5 m glazed hut with a turnstile row of 3–4.
  - `access_ramp`: 1:12 with 1.2 m handrails, or a stair to the footbridge.
  - `separator_block`: 1.0 × 0.3 × 0.3 m precast.
  - `brt_bus`: 12 m high-floor bus, blue/white or red/white (invent).
- **Colours:**
  - Shelter blue `#1F4E9A`, white `#F2F2EE` and steel `#8E959B`.
  - Separator yellow `#F2C230` and black `#1A1A1A`.
  - Red bus-lane paint `#9C3B2E` on some stretches [est].
- **Variants:**
  - Full median station with a footbridge (50%).
  - Kerbside stop with shelter (30%).
  - Terminal at the corridor end: a large canopy, 4–8 bays, depot (20%).
- **Condition states:**
  - **New:** glass intact, LED signs.
  - **Worn:** panels missing, rust stains, turnstiles broken.
  - **Decayed:** shelter stripped, a hawker inside, private cars and okadas using the lane.
- **Props and life:** long queues at rush hour that spill onto the ramp. Officials in vests. Cars that break into the lane get stopped. At night the station is dimly lit with a guard on a chair.
- **SELECT BY:** expressways and main arterials (distance to main road 0) in `dense_mainland`, `civic` and `sprawl` corridors. One station every 0.8–1.5 km [est]. A terminal at the end of each line.
- **Gidi mapping:** BRT station, BRT lane.

---

## 5. Colonial narrow-gauge line and station

**Pattern:** a 1,067 mm gauge line from 1898 [src Wikipedia NRC], with a big railway compound holding old coaches, workshops and staff quarters [src Guardian]. New standard-gauge tracks have been squeezed in beside it, with the old tracks shifted [src Daily Trust].

- **Looks like:**
  - A long single-storey station building (some have 2 storeys at the centre). Thick walls painted cream with a brown or green dado, timber louvred doors, and a deep verandah on cast-iron or timber posts.
  - A hipped corrugated roof (red-brown rust). A low concrete platform 0.3–0.6 m high.
  - A painted name board on two posts at each end.
  - Rusted sidings with dead coaches (faded green/cream or maroon), a water tower, a signal box, and a workshop shed with a saw-tooth roof.
- **Kit parts:**
  - `old_station`: 40–80 × 10–12 m, eaves 4 m, verandah 3 m deep, posts at 3 m [est].
  - `platform_low`: 100–200 × 4–6 m × 0.45 m, with a painted edge [est].
  - `name_board`: 4 × 0.8 m, white with black letters, on two posts.
  - `track_1067`: rails 1.067 m apart on timber or concrete sleepers, ballast `#6F6A62`.
  - `dead_coach`: 18–20 m long, 2.7 m wide, rust-scabbed.
  - `water_tower`: a steel tank 4 × 4 × 3 m on a 6 m frame.
  - `signal_post`: semaphore, 6 m.
  - `workshop_shed`: 60 × 25 m with a saw-tooth roof.
- **Colours:**
  - Walls cream `#E8DCC0` to stained `#C7B898`.
  - Trim brown `#5C3B23` or bottle green `#2F5D3A`.
  - Roof rust `#8A4B2A`.
  - Coaches green `#3F6B4A` / cream, faded.
- **Variants:**
  - Main station with compound (10%).
  - Wayside halt: a 10 × 5 m shed and a short platform (60%).
  - Abandoned halt overrun by a market (30%).
- **Condition states:**
  - **Kept up:** fresh paint, flower pots.
  - **Worn:** peeling paint, broken louvres.
  - **Decayed:** roof gaps, trees growing from the gutters.
  - **Abandoned:** coaches used as homes, laundry on the rails.
- **Props and life:** commuters walking on the tracks, traders spreading goods on the rails and sleepers in the evening [src Daily Trust], goats, a crowd climbing onto a slow train, a staff bicycle.
- **SELECT BY:** `old_island` and old parts of `dense_mainland` along the rail corridor. The compound sits at the junction near the lagoon.
- **Gidi mapping:** old rail station, rail corridor.

---

## 6. New light-rail viaduct and elevated station

**Pattern:**
- **The electric line:** a 27 km line with 13 stations, 1,435 mm gauge, and a fully separated right-of-way with no level crossings [src Wikipedia Blue Line]. It runs at grade in the expressway median, then goes elevated for the last 5.5 km to an elevated terminal by the harbour that connects with ferries [src Ripples/Channels]. The trains are Chinese "Type B" EMUs with a top speed of 100 km/h, run at 80 km/h [src Wikipedia]. Platforms are island style [src SCB].
- **The diesel line:** a 27 km line beside the standard-gauge mainline [src Wikipedia Red Line]. It has a 620 m flyover over the tracks in the civic centre [src ThisDay], and 10 vehicle bridges plus pedestrian crossings [src Wikipedia]. One multi-level station sits 300 m from a big intercity station [src Wikipedia].

- **Looks like:**
  - A twin-track box-girder viaduct on single round or hammer-head piers. Deck underside 8–10 m above the road [est].
  - Stations: a big curved metal roof (silver/white), a glazed concourse level, and stairs/escalators down to both sides of the road.
  - Stations in the median have a fenced island platform at grade, with a footbridge.
  - Two tracks at grade inside a 2.4 m palisade or concrete wall, topped with razor wire.
- **Kit parts:**
  - `viaduct_span`: a box girder 9–10 m wide, 2.0–2.5 m deep. Spans 25–35 m. Piers 2 m in diameter or 2 × 3 m hammer-head, 8–12 m tall [est].
  - `elev_station`: a platform 100–120 m long (for 4–6 cars) and 10–12 m wide (island). Concourse at +6 m, platform at +12 m. A roof shell 130 × 25 m [est].
  - `stair_tower`: 6 × 10 m with escalator and stair, glazed.
  - `at_grade_platform`: island, 110 × 8 m × 1.1 m.
  - `ohl_mast` (for the electric line): steel H-mast every 50 m, 6 m tall, with a cantilever [est].
  - `emu`: 19 m cars × 2.8 m wide, 4 cars [est]. White body with a colour band (invent).
  - `palisade`: 2.4 m, steel, painted green or grey.
  - The old diesel stock, invented: a white or red streamlined power car with coaches.
- **Colours:**
  - Concrete `#C4C0B6` new to `#9A958B` stained.
  - Roof silver `#C9CDD0`.
  - Glass `#6C8C93`.
  - Station accent colour per line (blue `#1F5FA8`, red `#C62828`) [est].
  - Palisade green `#3E6B3A`.
- **Variants:**
  - Elevated station (40%).
  - At-grade island in a median (40%).
  - Big intercity station on the standard-gauge line: a 3-storey hall with a monumental entrance, 150–200 m wide [est] (20%).
- **Condition states:**
  - **New:** spotless.
  - **Worn:** rust tears from the bearings, graffiti on the piers.
  - **Under construction or stalled:** bare piers with rebar sticking out and no deck. Stalled stations get squatters [src BusinessDay "abandoned Blue Line stations"].
- **Props and life:** under the viaduct are parked danfos, car washes, mechanic stalls and sleeping bodies. On the platform there are security staff in uniform and card turnstiles. At night the station is lit cool white.
- **SELECT BY:** from the `civic` centre to `old_island` along the expressways, and the old rail corridor through `dense_mainland`. The line goes elevated where `old_island` or the harbour edge begins.
- **Gidi mapping:** new rail station, viaduct.

---

## 7. Level crossing and rail corridor with shanties

**Pattern:** traders sell on the rails at several stations in the evening [src Daily Trust]. Automatic barriers are vandalised again and again; underpasses and overpasses are replacing the crossings, with 11 planned [src Gazette]. The state clears shanties along the right-of-way, but they come back [src NAN].

- **Looks like:**
  - Tracks crossing a busy road with a red/white barrier arm (often broken), a small gate hut, crossing signs and rubber or concrete panels between the rails.
  - On both sides: a 15–30 m strip of zinc-and-timber shacks with their backs to the line, plus refuse, stalls, smoke from cooking, and laundry.
  - Where a new line runs alongside, a palisade wall divides old from new, and shanties lean on the wall.
- **Kit parts:**
  - `crossing_barrier`: a 6–8 m arm in red/white stripes `#D32F2F`/`#F5F5F5` on a pivot post 1 m tall [est].
  - `gate_hut`: 2 × 2 m block with a flat roof.
  - `crossing_panel`: concrete slabs 1.2 × 2.5 m.
  - `x_sign`: a saltire 1.2 m on a 3 m post.
  - `rail_shanty`: 3 × 3 m to 4 × 6 m, 2.2–2.6 m tall. Zinc roof held down by tyres and blocks. Timber or zinc walls. Tarpaulin. Sited 2–4 m from the rail [est].
  - `rail_stall`: goods on cloths or mats laid across the sleepers.
- **Variants:**
  - Gated crossing (30%).
  - Unguarded crossing (50%).
  - Replaced by an under- or overpass (20%).
- **Condition states:**
  - Freshly cleared: rubble, plus a red "X" painted on walls.
  - Regrowing: half rebuilt.
  - Full corridor: continuous rows of shacks.
- **Props and life:** a train horn makes traders snatch goods off the rails. A keke jam at the crossing. Okadas squeeze under the arm.
- **SELECT BY:** the rail corridor through `dense_mainland`. Shanty density rises with distance from an elevated new-line section. No shanties within the `civic` core.
- **Gidi mapping:** level crossing, rail corridor shanties.

---

## 8. Truck park and trailer queue ("truck park", "trailer")

**Pattern:** port-bound trucks park on the expressways and on bridges, take two lanes, and cause queues lasting days [src BusinessDay, ThisDay]. Official truck parks and a call-up system have been added, but parking spills back to the road.

- **Looks like:**
  - A km-long line of 40-ft articulated trucks, often parked two abreast on one side of the expressway, sometimes on bridge decks.
  - Drivers sleep under the trailers or in hammocks between the axles.
  - Kiosks, buka food stalls, and mechanics set up beside the line.
  - Truck parks: big laterite lots with a gate, a weighbridge, a toilet block and a tea stall.
- **Kit parts:**
  - `trailer_rig`: tractor 6.5 m + trailer 12.2 m. Total 18–19 m long, 2.5 m wide, 4.0 m tall with a 40-ft box [est]. Cabs in faded red, white, blue, yellow or green (often "Mack-style" or Chinese cabs).
  - `flatbed_rig`: no box, or one 20-ft box.
  - `tanker`: 12 m cylinder, silver or white with a colour band.
  - `truck_park_lot`: 150 × 300 m [est].
  - `weighbridge`: an 18 × 3 m steel deck with a 3 × 3 m hut.
  - `gate`: barrier arm plus a container office.
- **Colours:**
  - Container boxes in shipping-line colours (see item 9).
  - Rust `#8A4B2A`.
  - Laterite `#A6573A`.
- **Variants:**
  - On-road queue (60%).
  - Official park (25%).
  - Informal lot on wasteland (15%).
- **Condition states:**
  - Orderly: a single file.
  - Gridlock: double-parked, with the carriageway reduced to one lane.
  - Broken-down rigs: jacked up, tyres off, boxes sitting on the road.
- **Props and life:** truck pushers, tyre-repair stands made of a compressor and tyre stack, fuel hawkers with jerrycans, touts collecting for "call-up". At night: cab lights, cooking fires, and orange sodium light.
- **SELECT BY:** `port` and its access roads within 5–8 km [est]. Queues sit on roads with distance to the port gate < 5 km. Parks sit on large `port`/`sprawl` lots.
- **Gidi mapping:** "truck park", "trailer".

---

## 9. Container yard and stacks ("stack", "Container Yard")

**Pattern:** a 55 ha terminal handling 1 million+ TEU a year [src Konecranes]. Off-dock empty depots (Ijora-style ones and inland ones) fill vacant lots.

- **Looks like:**
  - Blocks of containers in rows 4–5 high in RTG yards, or 4–6 high for empties handled by empty handlers.
  - Lanes between blocks. Concrete or interlocking-paver ground with yellow lane lines.
  - High-mast floodlights (30–40 m) across the yard.
  - Off-dock depots stack empties 6–8 high right up to the perimeter wall, so they show over the wall from the street.
- **Kit parts:**
  - `container_20`: 6.06 × 2.44 × 2.59 m.
  - `container_40`: 12.19 × 2.44 × 2.59 m (high-cube 2.90 m).
  - `stack_block`: 6 rows wide × 4–5 tiers × n bays (RTG). Gap 0.3–0.4 m between rows.
  - `yard_lane`: 15–25 m wide.
  - `high_mast`: 35 m tube with a ring of 8–12 floodlights.
  - `reefer_rack`: steel frame 3 tiers high with power sockets.
  - `perimeter_wall`: 3 m block with razor wire.
- **Colours** (invent the liveries, keep the families):
  - Rust-red `#8F3B2A`, maroon `#6E2B2B`, blue `#2A4F7A`, light blue `#4F86B5`, green `#3D6B4A`, grey `#7C8186`, orange `#C96B2C`, white `#E9E7E1`, yellow `#D9A928`.
  - Ground concrete `#A8A49C`.
  - Lane lines yellow `#E5B830`.
- **Variants:**
  - On-dock RTG yard (50%).
  - Off-dock empty depot (35%).
  - Abandoned box clutter by the road (15%).
- **Condition states:**
  - New boxes are crisp.
  - Worn boxes have rust streaks and dents.
  - Decayed boxes are rust-brown and holed. In the city they get reused as shops and offices (link to the kit's container-shop item).
- **Props and life:** reach stackers, terminal tractors, people in hard hats and orange or yellow hi-vis vests. Yard lit bright at night.
- **SELECT BY:** `port` only for on-dock yards. Off-dock depots sit in `port` or on `dense_mainland` plots within 3 km of the port [est].
- **Gidi mapping:** "stack", "Container Yard".

---

## 10. Port cranes and handling machines ("crane")

**Pattern:**
- The older port runs **13 mobile harbour cranes** (not STS gantries), 27–30 RTGs rated 41 t, and 13 reach stackers rated 45–46 t [src Konecranes, Guardian, Port Technology].
- The new deep-sea port has **5 Super-Post-Panamax STS cranes and 15 RTGs** [src Container News].

- **Kit parts:**
  - `sts_crane`:
    - A-frame boom with the boom raised to 80–95 m. Lift height 40–50 m above the quay.
    - Rail gauge 30.5 m, outreach 60–70 m, legs 18 m apart along the quay [est].
    - Colours: white `#EDEDEA`, blue `#2F5C9A`, or red `#B33A2E` trim. Orange or red aviation lights.
  - `mobile_harbour_crane`:
    - A rubber-tyred undercarriage 16 × 16 m on outriggers, with a tower 30–40 m and a boom reaching 50–60 m [est].
    - Colour: yellow `#E5B32A` or white/blue.
  - `rtg`:
    - 24 m span over 6 rows plus a truck lane. 18–25 m tall. 8 or 16 wheels.
    - Colour: blue `#2F5C9A`, yellow, or white [est].
  - `reach_stacker`: 11 × 4.2 m body, 4.5 m to the cab. The boom extends to stack 5 high. Yellow `#E5B32A` or red.
  - `empty_handler`: a 30 m mast forklift that lifts boxes from the side.
  - `terminal_tractor`: a short cab with a 12 m chassis.
- **Variants:**
  - Old-port mobile cranes and reach stackers.
  - Deep-sea port STS and RTG.
  - Bulk/general berth with a ship crane and grab.
- **Condition:** new cranes are white or blue and clean. Old ones are faded, with streaked rust and patches of fresh paint.
- **Life:** the steady clank of containers, ship hulls behind, night-time floodlit.
- **SELECT BY:** `port` quay edge. STS cranes only at the deep-water berth.
- **Gidi mapping:** "crane".

---

## 11. Customs shed, port gate and bonded warehouse

- **Looks like:**
  - A gate complex with a long canopy over 4–8 truck lanes, booths, barrier arms, a scanner building and an agency flagpole.
  - Large old transit sheds: steel portal frame or RC, 60–120 m long, with rusted sliding doors.
  - A customs office in 2–3 storeys of 1970s concrete with louvre windows and a green/white agency band.
- **Kit parts:**
  - `transit_shed`: 80 × 30 m, eaves 8 m, a corrugated roof at 10°, sliding doors 6 × 6 m [est].
  - `gate_canopy`: 30–60 m × 15 m on 6 m columns [est].
  - `scanner_hall`: 40 × 8 × 7 m.
  - `booth`: 2 × 3 m.
  - `office_block`: 3 storeys, 30 × 12 m.
  - `flagpole_trio`: 3 poles × 10 m.
- **Colours:**
  - Shed grey `#8B9096` / rust `#8A4B2A`.
  - Agency olive or green `#4B5D3A` with white `#F2F2EE`.
  - Gate canopy white with a coloured fascia.
- **Condition:** old sheds have rusted walls and broken windows. Containers can be "overtime" for months inside abandoned warehouses.
- **Life:** clearing agents in shirts with folders, uniformed customs officers in olive, queues of trucks, money-changers.
- **SELECT BY:** `port` gate roads.
- **Gidi mapping:** customs shed, port gate.

---

## 12. Airport perimeter fence and approach lights ("Airport Fence")

**Pattern:** the fence has many breaches. Houses in neighbouring districts share the airport's perimeter fence. ICAO guidance calls for at least 6 m between the fence and any structure and a cleared 3 m zone on each side, which Lagos falls short of [src BusinessDay, ThisDay].

- **Looks like:**
  - A 2.4–3.0 m chain-link or weld-mesh fence on concrete or steel posts, topped with a Y-arm of barbed or razor wire [est]. Some stretches are a block wall with wire on top.
  - Outside: a strip of grass, refuse, and houses built right up to it. A goat path and a hole cut in the mesh.
  - Inside: a patrol road, then grass.
  - Approach-light masts on frangible poles in a line beyond the runway end, sometimes running across rough ground and fields. Red/white-checked hazard beacons on high structures nearby.
- **Kit parts:**
  - `airport_fence`: posts at 3 m centres, mesh 2.4 m, Y-arm 0.6 m, 3 strands of barbed wire plus a coil [est].
  - `fence_sign`: "RESTRICTED AREA / TRESPASSERS WILL BE PROSECUTED". Red on white, 0.6 × 0.4 m, every 100 m [est].
  - `watch_tower`: a 2 × 2 m cabin on a 6 m frame.
  - `approach_light`: a frangible 1–8 m pole with a crossbar of 5 lights. Rows 30 m apart, extending 300–900 m [est]. Lights are white; the threshold bar is green and the runway end red.
  - `patrol_road`: 4 m.
- **Colours:** galvanised `#A3A8AD`, rusting `#8A4B2A`, block wall white with a blue band, approach-light poles orange/white `#E86A1A`.
- **Variants:**
  - Mesh with razor wire (60%).
  - Block wall (30%).
  - New anti-climb "358" mesh (10%).
- **Condition:** new is taut and bright. Worn mesh is torn, with a path through and refuse dumped by it.
- **Life:** planes low overhead, kids watching, a squatter shack against the wall, a security patrol pickup.
- **SELECT BY:** the edge of `sprawl` / `civic` next to the airport. Approach lights cross `sprawl` land beyond the runway ends.
- **Gidi mapping:** "Airport Fence".

---

## 13. Jetties ("Canoe Jetty", "jetty")

**Pattern:** the state is installing concrete floating pontoons at many jetties. Upgraded units are six-sided for docking all round [src Guardian, Shipping Position]. A €410m programme covers 78 electric ferries and 25 terminals [src Shipping Position]. The harbour-front jetty links with the elevated rail terminal [src ITS Nigeria]. In the lagoon settlement, people board dugout canoes from a makeshift reinforced-concrete jetty [src WATHI/Guardian].

- **Variants:**
  - **Canoe jetty (45%):**
    - A sand-filled or timber landing, or a few concrete steps into the water.
    - Planks on stilts 5–20 m long × 1–1.5 m wide.
    - Dugout canoes 4–10 m long (street file), plus planked boats 8–12 m with an outboard and a tarpaulin roof.
    - Paddlers with long poles.
  - **Public ferry terminal (20%):**
    - A small terminal building (12 × 8 m, glass, a curved roof), a covered gangway 20–40 m, and a concrete pontoon 15 × 6 m to a hexagon about 15 m across [est].
    - Life-jacket racks. A waiting shed with a blue/white branded fascia.
  - **Speedboat jetty (20%):**
    - Private ones in `elite` areas: steel or timber pier with cleats.
    - 7–10 m fibreglass speedboats with a canopy and orange life jackets.
    - Marina pontoons.
  - **Barge/sand landing (15%):**
    - A sloping ramp of laterite or sand. Steel sand barges 20–40 m × 6–8 m, rusted, with a crane or conveyor.
    - Heaps of dredged sand, tipper trucks, a sawmill with log rafts floating nearby.
- **Kit parts:**
  - `pontoon_hex` / `pontoon_rect`: concrete, freeboard 0.6 m, with tyre fenders and bollards [est].
  - `gangway`: steel, hinged, 1.5–2.0 m wide with a canopy.
  - `stilt_jetty`: posts at 1.5–2 m centres and a timber deck.
  - `ferry`: 15–20 m catamaran or monohull, white with a coloured band.
  - `canoe`, `planked_boat`, `speedboat`, `sand_barge`.
  - `jetty_sign`: an arched gate sign on 2 posts.
  - `life_jacket_rack`.
- **Colours:**
  - Concrete `#B3AFA6`.
  - Timber grey `#7A6E5E` / wet `#4E4436`.
  - Ferry white `#F2F2EE` with blue `#1F5FA8`.
  - Life jackets orange `#F26B1D`.
  - Lagoon water `#4F5B4A` (brown-green) [est].
- **Condition:** new pontoons are clean and grey. Old timber jetties have rotten boards and plastic bottles caught in the water hyacinth.
- **Life:** traders loading goods, fish smoking, women selling food from boats, kids swimming. At night a single bulb on a pole.
- **SELECT BY:** `waterfront` (canoe jetties). Public terminals at `old_island`/`civic` shore nodes. Speedboat jetties at `elite` shores. Barge landings at `port`/`waterfront` edges and sawmills.
- **Gidi mapping:** "Canoe Jetty", "jetty".

---

## 14. Flyovers and life under them ("Under the Bridge")

**Pattern:** markets live under bridges: electronics under one expressway bridge (demolished 2016), a decades-old market under another bridge (fire, then a ban) [src Guardian, ICIR]. Trading carries on under other bridges despite eviction orders [src Guardian]. One big under-bridge is where buses to anywhere on the island load [src transport guide].

- **Looks like:**
  - An RC deck 8–20 m wide on rows of columns (single circular or square columns, or pier frames with a crossbeam). Underside 5.5–8 m above the road [est].
  - Underneath: a dim world of danfos loading, keke stands, stalls, mechanics, people sleeping on mats, prayer spots and refuse.
  - The columns are covered in posters, painted adverts and soot. Water drips from deck joints.
- **Kit parts:**
  - `flyover_span`: T-beam or box deck 1.2–1.8 m deep, spans 20–30 m [est].
  - `pier`: 1.2–1.8 m round, or a 2 m portal frame with a 1.5 m cross-head [est].
  - `bridge_parapet`: New Jersey shape 0.8–1.1 m, painted yellow/black on the ramps.
  - `ramp`: 1:20, with retaining walls.
  - `under_stall`: zinc roof sheets fixed to a timber frame 2.2 m high. Tables and umbrellas.
  - `danfo_bay`: painted lines on the pier walls ("BAY 3", destination).
  - `fence_under`: green mesh fence put up by the state after an eviction.
- **Colours:**
  - Concrete `#A9A49A`, soot `#4A4844`.
  - Faded yellow/black parapet `#E5B830`/`#1A1A1A`.
  - Posters in a mix of colours.
  - Under-bridge light: dim `#3B3A36` by day, lit by orange sodium `#FFB15C` and LED strips at night.
- **Variants:**
  - Park under the bridge (40%).
  - Market under the bridge (30%).
  - Fenced and empty, with greenery or paving (20%).
  - Homeless camp (10%).
- **Condition states:**
  - New flyover: clean, lit.
  - Worn: stained, with lights dead.
  - Burnt: blackened soffit and melted signs, after a fire.
  - Cleared: rubble, a gov't notice and a fence.
- **Life:** day is loud with horns and callers. Night has fires, music from phone speakers, and okadas waiting.
- **SELECT BY:** the main junctions of `dense_mainland` and `old_island` flyovers. More life where a market sits within 300 m [est].
- **Gidi mapping:** "Under the Bridge", flyovers, interchange ramps.

---

## 15. Pedestrian footbridges and skywalks

Adds to street file §2.6.

- **Types:**
  - **Steel truss (50%):** a Warren truss with a mesh, roofed or open, painted green, blue or grey. Old ones get replaced for being dilapidated [src ThisDay].
  - **RC deck (30%):** a concrete deck on 2–3 piers with steel railings, and switchback stair towers.
  - **New covered skywalk (20%):** steel with a polycarbonate roof, sometimes with lifts that are often broken.
- **Kit parts:**
  - Deck 2.5–4.0 m wide, clearance 5.5–6.0 m, span 30–60 m.
  - Stair: 1.5–2.0 m wide, 3 flights with landings.
  - Billboard panel on the side: 12 × 3 m.
- **Colours:** green `#3E7B3A`, blue `#2856A6`, rust `#8A4B2A`.
- **Condition:** broken treads, missing mesh, and smells of urine at the landings.
- **Life:** hawkers on landings, beggars, a phone-card seller, and people still running across the road below.
- **SELECT BY:** expressways near markets, BRT stations and bus parks. One per 0.5–1.5 km.
- **Gidi mapping:** footbridge, skywalk.

---

## 16. Long lagoon bridge ("Long Bridge")

**Pattern:** an 11.8 km prestressed RC bridge with 8 lanes (4 each way), built in two phases from 1976 to 1990 [src Wikipedia]. Piles go 36–54 m deep, 1,500 mm in diameter over the main crossing [src Wikipedia]. It has a mid-way link ramp to the mainland and views over the stilt settlement and the university shore [src Wikipedia]. Repairs have closed it in phases (bearings, expansion joints) [src Wikipedia].

- **Looks like:**
  - A long, low, slightly curving dual deck over brown water on rows of piers.
  - Deck 5–12 m above the water, rising to about 15 m at navigation openings [est].
  - Street lights on the median at 30–40 m.
  - The parapets are low concrete with a steel rail.
- **Kit parts:**
  - `long_deck`: two decks of 4 lanes, 15–16 m each, with a 1–2 m gap or a central barrier. Total width about 32–34 m [est].
  - Span 30–40 m. Piers: 2–3 columns with a cap per deck [est].
  - `parapet`: 1.0 m concrete with a 0.3 m rail.
  - `median_lamp`: twin-arm, 10 m.
  - `exit_ramp`: a spiral or diagonal to the shore.
  - `expansion_joint`: a metal strip across the deck.
- **Colours:** concrete `#BDB8AD` above and algae-stained `#5E6B55` at the waterline. Lamps are galvanised.
- **Condition:** potholed patches and dark stains along the joints. Repair works close one side with orange barriers.
- **Life:** fishermen in canoes under the spans, nets on stakes in the lagoon, sand dredgers, stalled cars, people at the rail looking at the water. Traffic jams at rush hour. At night a line of lamps over black water.
- **SELECT BY:** one per city, crossing the lagoon from `dense_mainland` to `old_island`. It passes beside `waterfront` stilt settlements.
- **Gidi mapping:** "Long Bridge".

---

## 17. Cable-stayed toll bridge ("Cable Bridge")

**Pattern:** 1.36 km in total: a 722 m approach plus a 635 m cable-stayed main bridge. One pylon about 90–91 m high with 28 stay cables 55–119 m long, and a 225 m suspended main span. 9 m of headroom over the water. The toll gate is at one end [src Structurae, World Highways, ConstructAfrica].

- **Looks like:**
  - A single concrete pylon (A or inverted-Y form) [est], with fans of white-sheathed cables to an edge-girder deck.
  - The approach is a long, low beam viaduct.
  - At night the pylon is lit with colour-changing LEDs [est].
  - People jog and walk on the footpaths.
- **Kit parts:**
  - `pylon`: 90 m tall, legs 3 × 4 m [est].
  - `stay_cable`: 0.2 m diameter, white sheathing.
  - `deck`: 2 × 2 lanes plus footpaths. 22–25 m wide, 2.5 m deep [est].
  - `approach_viaduct`: spans 30 m on single piers.
  - `bridge_lamp`: modern LED, 10 m.
  - `toll_plaza` at one end (item 18).
- **Colours:** pylon light concrete `#D2CEC4`, cables white `#F2F2EE`, rails grey, LED purple/blue/green at night.
- **Condition:** mostly well kept, with some stains and dead lamps.
- **Life:** joggers in the morning, people taking photos, police patrol cars, prams on Sundays. Small canoes below.
- **SELECT BY:** one per city, between two `elite` districts across a creek.
- **Gidi mapping:** "Cable Bridge".

---

## 18. Toll plaza ("toll booth")

**Pattern:** a PPP concession with three planned plazas along the coastal expressway. Lanes are tagged by type: e-tag express, prepaid card, mixed, open [src Wikipedia, LCC]. A cable bridge has its own toll gate.

- **Looks like:**
  - A wide fan of 8–16 lanes under a large canopy (barrel or flat steel roof with a branded fascia).
  - Concrete islands with booths. Barrier arms. Overhead lane signals (green arrow / red X).
  - An admin building at the side, and CCTV.
- **Kit parts:**
  - `toll_canopy`: 60–150 m × 20–25 m, clearance 5.5–6 m [est].
  - `toll_island`: 25 × 2.2 m with a nose cushion painted yellow/black.
  - `toll_booth`: 1.8 × 3.0 m, glazed, with a 2.6 m roof.
  - `barrier_arm`: 3.5 m.
  - `lane_signal`.
  - `admin_block`: 2 storeys.
  - `tag_reader` gantry.
- **Colours:** canopy white `#F0F0EC` with a fascia stripe (invent the colours, for example teal `#00796B` or orange), yellow/black islands, signs in white on blue.
- **Variants:**
  - Operating (60%).
  - Burnt or abandoned after unrest: charred booths and a bent canopy (15%).
  - Reopened with new booths (25%).
- **Life:** queues and horns. Hawkers walk between the lanes. Okadas avoid it by the side.
- **SELECT BY:** `elite`/`sprawl` expressways and at the ends of the "Cable Bridge".
- **Gidi mapping:** "toll booth".

---

## 19. Checkpoints (different agencies)

**Pattern:** police, traffic, vehicle-inspection, drug, customs and road-safety agencies all stop vehicles [src Failed Architecture]. 21 stops were counted over about 15 miles on the border road, and more than 50 between the port and Mile 2 [src Failed Architecture]. Checkpoints cluster in poorer areas and almost vanish in elite areas [src Failed Architecture].

- **Kit parts (by type):**
  - **Police:**
    - A 3–6 m line of barriers: steel spike strip, a plank with nails, a tyre stack, or a drum painted with red/white bands [est].
    - A rusted "STOP" sign leaning on a tyre. A patrol van (blue/white or black, invented). Beach umbrella and plastic chair.
    - Officers in black or blue, with rifles.
    - *Highway:* concrete cones, spike strips and yellow barricade poles [src Failed Architecture].
  - **Traffic warden:** yellow/maroon-style uniform (invent the colours) and a small kiosk at the junction.
  - **Customs (border/port roads):** a tent or kiosk, a tarpaulin, and olive uniforms.
  - **Road-safety agency:** a reflective-vest team with a white pickup and orange cones.
  - **Military:** sandbag emplacement, drums and khaki tents (port and border roads only).
  - **Vigilante (night):** a fire in a barrel, a rope across the road, sticks, and torches. A painted warning board reads "NO MOVEMENT AFTER 10PM" [src Failed Architecture].
  - **Estate gate:** see the street file. A boom barrier with a gatehouse, in `elite`.
- **Dimensions:** drum 0.58 m diameter × 0.88 m. Tyre 1.0 m. Spike strip 3–4 m. Tent 3 × 3 m. Cones 0.75 m.
- **Colours:** red/white drums `#D32F2F`/`#F5F5F5`, rusty `#8A4B2A`, olive `#4B5D3A`, reflective yellow `#D7FF3A`.
- **Condition:** blackened drums, warped planks, loose sandbags.
- **SELECT BY:** port roads (many), the border road, `dense_mainland` main roads, and night-time back streets (vigilante). Rare in `elite` cores, `civic` near the centre.
- **Gidi mapping:** checkpoint.

---

## 20. Roundabouts with statues; interchanges and ramps

**Pattern:** big public statues stood on roundabouts, including a "Victory" figure and a headless "Liberation" figure. They were moved when the junction was rebuilt for traffic, and a 6 m (20 ft) bust went up at another junction [src Daily Trust, ThisDay]. Statues as gateway markers are a common trope.

- **Looks like:**
  - A round island 20–60 m across with a kerb painted yellow/black or black/white.
  - Lawn and palms, sometimes a fountain and a tiled plinth.
  - A bronze or painted-fibreglass figure 3–8 m tall on a 2–4 m plinth: a traditional ruler, a drummer, a statesman, or a group of figures.
  - An agency or bank logo on a small sponsor sign.
- **Kit parts:**
  - `roundabout`: 20–60 m diameter, with a 0.25 m kerb.
  - `plinth`: tiled, 3 × 3 × 2.5 m.
  - `statue`: generic forms (figure, bust, abstract).
  - `fountain_ring`.
  - `sponsor_sign`: 2 × 1 m.
  - `interchange_ramp`: 7.5 m wide, 1:20 grade.
  - `cloverleaf`: loops with a 50–70 m radius.
- **Colours:** bronze `#6E4E2E`, gold-paint figures `#C9A23A`, plinth white or terracotta tiles, lawn `#4F7D3A`.
- **Variants:**
  - Statue roundabout (40%).
  - Plain landscaped roundabout (40%).
  - Converted to signalised junction or flyover (20%).
- **Condition:** new is lush, with the fountain working. Decayed means a dry fountain, brown grass, hawkers on the island and a plinth with tiles missing.
- **SELECT BY:** `civic` and `elite` gateways, plus the main junctions of `old_island`. Interchanges on expressways.
- **Gidi mapping:** roundabout, interchange, ramps.

---

## 21. Electricity: 33/11 kV lines, poles, transformers

Adds to street file §2.1–2.2.

- **33 kV lines:** concrete poles 12–15 m, or steel lattice towers (high-voltage feeders) 25–40 m high on a 4–8 m square base [est]. Long insulator strings.
- **132/330 kV transmission:** lattice towers 35–50 m tall, 300–400 m apart, crossing `sprawl` in cleared corridors 30–50 m wide [est]. The corridors are often built over with shanties.
- **Injection substation:** a 40 × 60 m plot behind a 2.4 m wall, holding gantries 8–10 m tall, 2–3 power transformers (big grey tanks with radiators), a control building and a "DANGER" sign.
- **Transformer types:**
  - **Pole-mounted H-frame (45%):** platform at 3–4 m. Some have a steel ladder and fuse boxes.
  - **Ground on a plinth in a cage (40%):** a 1.5 m plinth inside a 3 × 4 m cage, 2.4 m high, of mesh or block with a mesh door. Cables hang out of a feeder pillar beside it [est].
  - **Kiosk / package unit (15%):** green or grey metal housing, 2 × 2 × 2.2 m, in `elite` areas [est].
- **Signs:** "DANGER 11,000 VOLTS", invented distribution-company markings, and community painted labels ("CDA TRANSFORMER, DON'T URINATE HERE").
- **Colours:** tank grey `#8C8F8A`, oil stains black, cage green `#3E6B3A`.
- **Condition:** new is clean grey. Decayed shows oil weeps, burnt bushings, a scorched pole and loose cables. A "blown" transformer has a black scorch on the pole.
- **Life:** a crowd of community folks on the day a new transformer arrives. Electricians climbing poles without harnesses.
- **SELECT BY:** street file rules, plus substations every 3–5 km [est] and transmission corridors through `sprawl`.
- **Gidi mapping:** pole, line, transformer.

---

## 22. Telecom masts (ground and rooftop)

**Pattern:** Lagos has the most towers in Nigeria (5,851 in an older count). Most sites are on the ground, with equipment in metal shelters and diesel generators where there is no grid [src UNILAG journal, Guardian]. The state removed 95+ illegal masts after a building collapse linked to a rooftop mast, and banned hollow-pipe masts in 2014 [src Guardian, Vanguard]. Residents complain about generator noise and vibration [src BusinessDay].

- **Looks like:**
  - **Ground site:**
    - A plot of 15 × 15 m to 20 × 20 m with a 2.4–3 m block wall topped with razor wire, or a mesh fence. A steel gate shows the tower-company sign, a site ID and "DANGER" [est].
    - Inside: a 3- or 4-legged lattice tower 30–60 m tall, an equipment shelter or outdoor cabinets, a 40–60 kVA diesel generator, a diesel tank, solar panels on some sites.
    - Panel antennas in sectors at the top and microwave dishes in the middle.
    - A red/white tower near the airport, otherwise grey galvanised.
  - **Rooftop:** a 6–15 m self-supporting lattice or a pole frame on a 2–4 storey roof, with guy wires, cabinets and a generator on the roof or by the gate.
  - **Monopole:** 20–30 m in `elite` and `civic` areas, sometimes disguised as a palm tree.
- **Kit parts:**
  - `lattice_tower`: base 5–8 m wide, tapering to 1.5 m at the top. Heights 30/45/60 m [est].
  - `antenna_sector`: 3 × panels 1.3–2.6 m × 0.3 m.
  - `mw_dish`: 0.6–1.2 m.
  - `shelter`: 3 × 2.5 × 2.7 m metal.
  - `gen_set`: 2.5 × 1.1 × 1.5 m, plus a tank.
  - `site_wall`: 2.4 m.
  - `rooftop_frame`: 6–15 m.
  - `monopole`.
  - Aviation lamp at the top.
- **Colours:** galvanised `#A3A8AD`, red/white aviation bands `#D32F2F`/`#F5F5F5`, shelter white or beige, tower-company wall paint (invent: blue or green band).
- **Variants** (by district):
  - `dense_mainland`: 40% ground, 60% rooftop.
  - `sprawl`: 90% ground.
  - `elite`: monopole and rooftop.
- **Condition:** new is shiny. Worn shows rust at the joints and diesel stains at the base. Abandoned sites are a bare tower with no antennas and a padlocked gate.
- **Life:** a security man on a bench at the gate, a diesel tanker refuelling, generator noise heard from neighbours' homes.
- **SELECT BY:** one per 0.3–1 km² in dense areas [est], one per 1–3 km² in sprawl. Rooftop masts on 2+ storey buildings in `dense_mainland`/`old_island`.
- **Gidi mapping:** mast.

---

## 23. Street lights and CCTV

Adds to street file §2.3.

**Pattern:** a 2009 pilot put solar-powered cameras on three bridges. About 1,000 federal cameras followed, then about 2,000 state cameras, and a plan for 10,000–13,000 HD cameras [src BusinessDay, Guardian, Channels]. Critics say many cameras fail because there is no lighting or power [src Guardian]. "Light-Up" street lighting programmes are pushed by the state assembly and some local governments [src Radio Nigeria].

- **CCTV kit:**
  - `cctv_pole`: 8–12 m tapered octagonal steel. 1–2 bullet cameras plus a PTZ dome on arms. An equipment box at 3 m. A solar panel (1.0 × 0.7 m) and battery box on some [est].
  - `cctv_tower` at hubs: 15–25 m (item 1).
  - Wall-mounted cameras on banks, shops and estate gates.
- **Street-light kit:**
  - Grid twin-arm lamps on the median, 10–12 m.
  - Solar all-in-one, 6–9 m.
  - Decorative lamps in `elite` areas.
  - **New:** "gateway" signature gantries with LED name letters on bridges and civic gateways [est].
- **Colours:** galvanised `#A3A8AD`, solar panel `#1E2A44`, camera white `#EDEDEA`.
- **Condition:** dead lamps 30–60% in worn areas, a solar panel stolen leaving a bare bracket, CCTV hanging by its cable.
- **SELECT BY:** CCTV at junctions in `civic`, `elite`, on bridges and at hubs. Rare in `dense_mainland` side streets.
- **Gidi mapping:** street light, CCTV.

---

## 24. Canals, footbridges, culverts ("Gang Canal", "Canal 7")

**Pattern:** the state runs a numbered system of primary drainage channels ("System 1" is the widest on the mainland) and regularly dredges 28+ of them [src LASG/Guardian/Dredging Today]. It clears structures off collector drains [src Guardian].

- **Looks like:**
  - **Primary canal:** 10–40 m wide at the top [est], a trapezoidal earth channel, or a lined section with RC walls 2–4 m deep [est].
    - Black-green water with refuse mats, water hyacinth and plastic.
    - Shacks built along the banks and over the edge on stilts.
    - Dredged silt heaped on the banks. An excavator on a pontoon.
  - **Secondary canal:** 3–8 m wide, with RC walls and RC slab covers in places.
  - **Footbridges:**
    - Plank: 2–3 planks on posts with no rail.
    - Steel: an I-beam with chequer plate and a pipe railing.
    - RC: a 1.5–2.5 m wide slab with low walls.
    - Some charge a toll at a little table.
- **Kit parts:**
  - `canal_trap`: bottom 6–20 m, side slope 1:1.5 [est].
  - `canal_lined`: RC walls 0.3 m thick, 2.5 m high, with a 0.5 m coping painted with a "NO DUMPING" stencil.
  - `plank_bridge`: span 5–12 m, width 0.6–1.0 m.
  - `steel_footbridge`: span 8–25 m, width 1.5 m.
  - `rc_footbridge`: span 6–15 m.
  - `culvert`: box 1.5 × 1.5 m to 3 × 3 m with wing walls, or a pipe 0.6–1.2 m [est].
  - `trash_boom`, `silt_heap`, `canal_shack` (a stilt shack 3 × 4 m).
- **Colours:** water `#3B4A35` (stagnant) / `#5B5B48`, refuse in mixed colours, concrete `#A9A49A` with green algae `#55704A`, silt black `#2E2A24`.
- **Variants:**
  - Earth canal (50%).
  - Lined canal (35%).
  - Covered culvert under a road (15%).
- **Condition:**
  - Freshly dredged: banks bare, water flowing.
  - Choked: you can almost walk on the refuse.
  - Flooding: water over the banks in the rainy season.
- **Life:** kids fishing with nets, people scavenging plastic, toilets hanging over the water, canoes in the wide canals.
- **SELECT BY:** `dense_mainland` low-lying areas and `waterfront`. Canals run toward the lagoon. Footbridges every 100–300 m [est] where there is housing on both sides.
- **Gidi mapping:** "Gang Canal", "Canal 7", culvert, canal footbridge.

---

## 25. Pipelines and pipeline right-of-way

**Pattern:** gas and water pipelines in the rail corridor delayed rail works [src Daily Trust]. Products pipelines cross `sprawl` and `port` areas in cleared rights-of-way, with tapping and fires as hazards.

- **Looks like:**
  - A 20–30 m cleared strip of grass marked with concrete or yellow posts every 100 m ("PIPELINE ROW, DO NOT DIG").
  - Where it surfaces: a 0.3–1.0 m steel pipe on concrete saddles, painted grey or yellow, with valve stations in a fenced compound.
  - Paths and markets encroach on it, and jerrycans are left near tapping points.
- **Kit parts:**
  - `pipe_run`: diameter 0.3–1.0 m, on saddles every 6–10 m, 0.5–1.0 m off the ground.
  - `row_marker`: a 1.2 m post, yellow `#E5B830` with black.
  - `valve_station`: a 20 × 20 m mesh compound with pipes and a hut.
  - `pipe_bridge`: a steel pipe on a truss over a canal or creek.
- **Colours:** pipe grey `#8E959B` or yellow, rust patches, scorched black where tapped.
- **Condition:** new is clean paint. Old is rusty. A burnt stretch has blackened ground and grass.
- **SELECT BY:** `sprawl` and `port` edges, the rail corridor, and canal crossings.
- **Gidi mapping:** pipeline.

---

## Sources

- https://thisdaylive.com/index.php/2020/01/13/oshodi-transport-interchange-targets-1m-passengers
- https://estateintel.com/insights/oshodi-regeneration-plans-begin-with-70m-transport-interchange
- https://planetprojectsltd.com/projects/oshodi-transport-interchange
- https://www.discoverlagos.ng/post/understanding-the-scale-of-the-oshodi-transport-interchange
- https://businessday.ng/news/article/lagos-to-redesign-oshodi-transport-interchange-commissioner/
- https://en.wikipedia.org/wiki/Oshodi_Bus_Terminal
- https://www.icirnigeria.org/nurtw-mc-oluomo-dares-lagos-govt-national-body-as-icir-report-stirs-reawakening-part-1/
- https://guardian.ng/news/nigeria/touts-untamed-monsters-that-rule-lagos-roads/
- https://www.thecable.ng/?p=673337
- https://dailytrust.com/?p=1061710
- https://ikejarecord.com/?p=3102
- https://eyesofalagosboy.com/2024/11/19/photo-of-the-week-obalende-concrete-and-history/
- https://www.nigeriahousingmarket.com/news/lagos-transport-union-unveils-president-bola-ahmed-tinubu-modern-garage-facility
- https://www.dailytrust.com.ng/lagos-seals-off-chisco-ifex-guo-other-transporters-offices.html
- https://intercity.ng/blog/motor-parks-in-lagos-and-destinations
- https://www.lamata-ng.com/bus-services/
- https://archive.businessday.ng/executive-motoring/article/lamata-makes-45-progess-on-mile-12-ikorodu-brt-project/
- https://www.channelstv.com/2012/09/07/33677/
- https://blogs.worldbank.org/transport/urban-transport-lagos-shows-africa-way-forward-again
- https://journal.nitt.gov.ng/index.php/njlt-2019/article/view/10
- https://thisdaylive.com/index.php/2017/09/21/lagos-declares-two-night-restriction-on-ikorodu-road
- https://en.wikipedia.org/wiki/Blue_Line_(Lagos_Transit)
- https://en.wikipedia.org/wiki/Red_Line_(Lagos_Transit)
- https://scbist.com/scb/foreign-railways/projects/lagosrailmasstransit/index.htm
- https://businessday.ng/transport/article/abandoned-lagos-blue-line-stations-turns-criminals-den/
- https://thisdaylive.com/index.php/2023/12/20/sanwo-olu-opens-ikeja-red-line-flyover
- https://en.wikipedia.org/wiki/Nigerian_Railway_Corporation
- https://guardian.ng/?p=2910331
- https://dailytrust.com/?p=859004
- https://gazettengr.com/train-crash-nrc-begins-building-bridges-at-level-crossings/
- https://businessday.ng/transport/article/fg-lasg-to-arrest-traders-on-lagos-rail-tracks-over-accidents/
- https://nannews.ng/2023/09/30/lagos-govt-begins-clearing-shanties-obstructions-along-red-rail-line-project
- https://businessday.ng/apapa-gridlock-eases-as-decongestion-processes-commence/ (and businessday.ng/?p=39914)
- https://thisdaylive.com/index.php/2016/04/10/stakeholders-seek-fresh-options-to-end-apapa-gridlock
- https://www.kclifttrucks.com/discover/stacking-up-successes-in-nigeria
- https://www.porttechnology.org/news/apmt-apapa-accelerates-equipment-upgrade/
- https://guardian.ng/?p=1347253
- https://container-news.com/lekki-port-receives-rtgs-and-sts-cranes/
- https://www.porttechnology.org/news/lekki-port-receives-second-ship-with-handling-equipment/
- https://www.thisdaylive.com/2019/07/21/security-breach-faan-identifies-violator-awards-contract-for-perimeter-fencing/
- https://businessday.ng/exclusives/article/private-developers-encroachment-into-airport-land-threatens-security-at-mmia/
- https://leadership.ng/reclaim-encroached-land-around-lagos-airport-expert-urges-fg/
- https://guardian.ng/news/nigeria/metro/lagos-omi-eko-project-rolls-out-concrete-floating-jetties-statewide/
- https://leadership.ng/lagos-installs-pontoons-in-jetties-to-modernise-water-transportation/
- https://shippingposition.com.ng/lagos-begins-upgrade-of-waterway-infrastructure/
- https://www.itsnigeria.org/?p=5640
- https://www.wathi.org/inside-makoko-danger-and-ingenuity-in-the-worlds-biggest-floating-slum-tolu-ogunlesi-the-guardian/
- https://guardian.ng/opinion/columnists/on-oshodi-market-demolition/
- https://www.icirnigeria.org/illegal-traders-get-48-hour-notice-to-vacate-apongbon-bridge/
- https://radionigerialagos.gov.ng/?p=7863
- https://en.wikipedia.org/wiki/Third_Mainland_Bridge
- https://www.ice.org.uk/what-is-civil-engineering/infrastructure-projects/third-mainland-bridge-lagos
- https://structurae.net/en/structures/lekki-ikoyi-link-bridge
- https://www.worldhighways.com/feature/nigerias-giant-city-lagos-benefit-new-cable-stayed-bridge
- https://constructafrica.com/node/70
- https://en.wikipedia.org/wiki/Lekki-Ikoyi_Link_Bridge
- https://en.wikipedia.org/wiki/Admiralty_Circle_Plaza
- https://failedarchitecture.com/checkpoint-city/
- https://www.vanguardngr.com/2011/12/commuters-groan-over-multiple-checkpoints-along-lagos-badagry-expressway/amp/
- https://guardian.ng/saturday-magazine/why-police-officers-defy-igps-order-to-disband-checkpoints/
- https://www.dailytrust.com.ng/awo-felas-statues-not-destroyed-lagos-govt.html
- https://thisdaylive.com/index.php/2017/09/24/new-awolowo-statue
- https://jer.unilag.edu.ng/article/download/987/785
- https://guardian.ng/business-services/lagos-decommissions-over-95-illegally-installed-telecom-masts/
- https://www.vanguardngr.com/2014/01/lasg-de-commissions-unapproved-communication-masts-lagos/amp/
- https://businessday.ng/opinion/article/are-these-masts-not-killing-us/
- https://businessday.ng/exclusives/article/concerns-over-cctvs-in-lagos-as-insecurity-heightens-in-north/
- https://guardian.ng/news/concerns-as-lagos-grapples-with-high-crime-rates-despite-cctv-cameras/
- https://www.channelstv.com/2018/05/12/lagos-govt-to-install-10000-cctv-cameras-across-state/
- https://radionigerialagos.gov.ng/?p=21180
- https://guardian.ng/news/lagos-government-inspects-ongoing-clearance-dredging-of-drainage-channels-canals/
- https://dredgingtoday.com/?p=74467
- https://moelagos.gov.ng/lasg-commences-massive-dredging-of-drainage-channels-and-canals/
