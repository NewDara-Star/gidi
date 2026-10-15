# Gidi vehicle catalogue: everything that moves on Lagos roads and water

Research for the seeded Blender kit. **Rule zero:** study real Lagos, build our own city. Every real model, operator, union, agency and brand below is a *pattern reference* only. In Gidi, invent the liveries, names, logos, plates and slogans; describe makes only as body shapes ("1980s boxy rear-engine van", "bonneted American-style tractor").

This file builds on `docs/look/research-street.md` §3 (vehicles) and §5.5 (vehicle text). It goes deeper on profiles, dimensions, wheels, glazing, doors, loads, condition and selection. Where it repeats a figure from that file, the figure is checked or refined here.

**Tags:** [src] = from a listed source (numbered at the end, e.g. [src 3]); [est] = my estimate from photos, general knowledge of the base vehicle, or proportion. Manufacturer spec figures for a base vehicle are tagged [src] when a source was read in this session, otherwise [est, base-vehicle spec].

**Research limit:** The web-search budget for this session ran out partway through. Boats, okada union details, truck-pusher carts, police/agency liveries and ambulance livery rest on fewer sources and more estimates than the buses and tricycles. Those sections are marked.

**On "Tambulu":** No source turned up for "Tambulu" as a Lagos bus name. The well-attested Lagos name for the smaller yellow minibus is **korope** (Yoruba; "korope" is the minibus, "danfo" the larger bus) [src 1, 2]. The owner's "mini danfo / Tambulu" is almost certainly the korope (see item 4). Treat "Tambulu" as unverified. In Gidi we can use our own nickname anyway.

**On census items:** The brief asks for a mapping to "census items below", but no census list came with the brief. Each item therefore gets a proposed kit id (`veh.*`, `boat.*`, `cart.*`). Rename them to match the real census when it is merged.

---

## 0. Shared conventions for the kit

### 0.1 Axes and units
- Metres. Origin at the centre of the ground contact patch, +Y forward, +Z up.
- Wheel sizes are given as rim inches and an overall tyre diameter in metres. The tyre diameter is what to model.

### 0.2 Shared condition states (apply to every road vehicle)

| State | Share on mainland roads [est] | What changes |
|---|---|---|
| `new` | 10% (40% in `elite`) | Clean gloss paint, all glass, matching panels, chrome intact, legible plates, tyres black. |
| `worn` | 45% | Paint chalky on roof/bonnet (UV fade 10-25% lighter, less saturated), small dents, scuffed bumpers, one hubcap missing, dust film on lower 0.3 m, cracked windscreen corner, stickers. |
| `battered` | 35% | Mismatched panel (primer grey `#8A8D8C`, a different yellow, or bare filler `#C9C1AE`), rust bubbles at arches and sills (`#7A3E1E`, `#9C5A2E`), bumper missing or tied on with wire, one light dead or taped, door that does not close, bald tyres, sagging rear. |
| `wreck` | 10% (as parked/derelict props) | No glass, no wheels (on blocks or rims), body rust-brown `#6B3A22` through faded paint, weeds through the floor, used as storage, a shop or a sleeping place. |

- Rust is placed first at wheel arches, sill line, door bottoms and the lower 0.15 m of panels. On boxy vans, also at the windscreen corners and the gutter line.
- Fade is strongest on horizontal surfaces (roof, bonnet).
- Dust is red-brown laterite `#A8643A` in `sprawl`, and grey `#8E8A80` in the city.

### 0.3 Shared palette (vehicle-specific)

| Name | Hex | Use |
|---|---|---|
| Transit yellow, fresh | `#F2C200` | Danfo, korope, keke |
| Transit yellow, faded | `#E0B43A` | Typical danfo |
| Transit yellow, chalky | `#D6B867` | Old danfo roof |
| Stripe black | `#141414` | Stripes, bumpers |
| Tyre black | `#1C1C1C`, worn `#2E2D2B` | All |
| Primer grey | `#8A8D8C` | Replacement panels |
| Body filler | `#C9C1AE` | Repairs |
| Rust light / dark | `#9C5A2E` / `#6B3A22` | Ageing |
| Chrome / steel | `#B8BCBF` | Trim, tankers |
| Galvanised | `#9EA3A6` | Tankers, racks |
| Canvas black | `#151515`, faded `#3A3A3A` | Keke canopy |
| Tarpaulin blue | `#2F5FA8` | Truck covers, boat canopies |
| Keg yellow | `#E0B020` | Jerrycans |
| Life-jacket orange | `#FF6A13` | Boats |

### 0.4 Selection attributes used below
`district` (dense_mainland, sprawl, old_island, elite, civic, waterfront, port), `road_class` (expressway, main, street, lane, water), `wealth` (0-1), `condition` (0-1, 1 = new), `near` (market, bus_park, bus_stop, construction, port_gate, barracks, filling_station, jetty, sawmill), `time` (day, night), `period` (now, retro).

---

## 1. Summary table

| # | Item | Kit id | Size L×W×H (m) | Where (top districts) | Share of road traffic [est] |
|---|---|---|---|---|---|
| 1 | Keke (tricycle taxi), passenger + cargo | `veh.keke`, `veh.keke_cargo` | 2.66×1.30×1.70 | sprawl, dense_mainland back streets, estate feeders | 10-25% on streets, ~0 on expressways |
| 2 | Okada (motorcycle taxi) + private bikes, dispatch bikes | `veh.okada`, `veh.bike_dispatch` | 2.02×0.74×1.06 | sprawl, dense back streets | 10-30% on streets, low on main roads |
| 3 | Danfo (yellow 14-18 seat minibus) | `veh.danfo_t3`, `veh.danfo_jvan` | 4.57×1.84×1.95 | dense_mainland, old_island, sprawl main roads | 20-40% on main roads |
| 4 | Korope (small minibus) | `veh.korope` | 3.40×1.48×1.90 | feeder routes, sprawl, estates | 5-15% on feeders |
| 5 | Newer high-roof minibus / regulated mid-capacity | `veh.minibus_hiroof` | 5.38×1.88×2.29 | main roads, interstate parks | 5% |
| 6 | Molue (historical big yellow bus) | `veh.molue` | 9.5×2.5×3.1 | retro scenes; one hulk in dense_mainland/port | ~0 now |
| 7 | BRT and regulated city buses | `veh.bus_brt`, `veh.bus_flm` | 12.0×2.55×3.2 / 8.5×2.4×3.0 | expressway BRT lanes, terminals | 2-5% on BRT corridors |
| 8 | Staff bus / coaster | `veh.coaster` | 6.99×2.03×2.63 | civic, elite offices, port, schools | 2% |
| 9 | Interstate luxury coach | `veh.coach` | 12.5×2.55×3.7 | expressways, luxury parks | 1-3% on exit expressways |
| 10 | Private cars (sedan, SUV, jeep, pickup, MPV) | `veh.car_*` | 4.5×1.75×1.47 (sedan) | everywhere; SUVs in elite | 30-60% |
| 11 | Yellow taxi / ride-hail | `veh.taxi_yellow` | as sedan | old_island, airport, hotels | 1-3% |
| 12 | Tipper / sand truck | `veh.tipper` | 8.5×2.5×3.4 | sprawl construction, quarries, lagoon sand landings | 2-8% |
| 13 | Fuel tanker | `veh.tanker_fuel` | 16.5×2.5×3.7 | port, expressways, depots | 5-25% |
| 14 | Container trailer | `veh.trailer_box` | 16.5×2.5×4.0 | port, expressways | 5-35% |
| 15 | Flatbed/rigid lorry + "mammy wagon" (bolekaja) | `veh.lorry_wood`, `veh.mammy_wagon` | 7.2×2.4×3.2 (loaded 4.5+) | markets (food from the north), dense_mainland | 1-3% |
| 16 | Water tanker (rigid) | `veh.tanker_water` | 8.0×2.5×3.2 | sprawl, elite estates | <1% |
| 17 | Refuse: compactor, open tipper, informal cart | `veh.refuse_compactor`, `veh.refuse_open` | 8.2×2.5×3.4 | everywhere at dawn | <1% |
| 18 | Light trucks, box vans, pickups | `veh.lighttruck_box`, `veh.pickup` | 5.3×1.86×1.8 | markets, shops | 3-6% |
| 19 | Police pickups and vans | `veh.police_pickup`, `veh.police_van` | 5.3×1.86×1.82 | junctions, checkpoints | <1% (very visible) |
| 20 | Military trucks and pickups | `veh.mil_truck`, `veh.mil_pickup` | 7.5×2.5×3.0 | near barracks, expressway checkpoints | <0.5% |
| 21 | Checkpoint set | `prop.checkpoint_*` | 6-12 m road length | expressways at night, port, elite gates | n/a |
| 22 | Ambulance | `veh.ambulance` | 5.3×1.9×2.4 | civic hospitals, expressways | <0.2% |
| 23 | Traffic / task-force / tow / fire | `veh.traffic_*`, `veh.tow`, `veh.fire` | various | junctions, impound yards | <0.5% |
| 24 | Truck pusher cart (omolanke-type) | `cart.pusher` | 2.6×1.1×0.8 | old_island markets, dense_mainland | many in markets |
| 25 | Wheelbarrow | `cart.barrow` | 1.5×0.65×0.65 | markets, construction, water | many |
| 26 | Bicycle (+ vendor bikes) | `veh.bicycle` | 1.75×0.6×1.05 | sprawl, waterfront paths | few |
| 27 | Water vendor cart (mai ruwa) and shoulder yoke | `cart.water`, `prop.yoke` | 2.4×1.2×1.2 | dense_mainland, sprawl, waterfront | common |
| 28 | Dugout paddle canoe | `boat.dugout` | 4-8×0.5-0.9 | waterfront canals | dominant on water |
| 29 | Plank fishing/transport canoe with outboard | `boat.plank_outboard` | 8-14×1.2-1.8 | lagoon | common |
| 30 | Trader canoe (floating shop) | `boat.trader` | 4-6×0.7 | waterfront canals | common |
| 31 | Sand canoe and sand dredger | `boat.sand_canoe`, `boat.dredger` | 10-18 m / 20-30 m | lagoon shores near sand landings | common |
| 32 | Wooden passenger ferry boat | `boat.ferry_wood` | 12-16×2.5×2.2 | jetties | common |
| 33 | Fibreglass speedboat / water taxi | `boat.speed` | 8-12×2.4×1.8 | jetties, elite marinas | common |
| 34 | State ferry / catamaran | `boat.ferry_state` | 15-25×5×4 | main jetties | few |
| 35 | Log raft (sawmill) | `boat.lograft` | 15-30×4-8 | sawmill waterfront | many at sawmill |
| 36 | Barge, tug, pontoon, wrecks | `boat.barge`, `boat.tug`, `boat.wreck` | 20-60 m | port, lagoon edges | few |
| 37 | Police/navy gunboat, water ambulance | `boat.patrol` | 8-12 m | jetties, port | rare |

Behaviour and placement rules are in §8. Traffic mixes per district and road class are in §8.6.

---

## 2. Road passenger vehicles

### 1. Keke (tricycle taxi) — "Keke Marwa" / "Keke Napep" type

**Looks like:**
- A three-wheeled auto-rickshaw: one front wheel, two rear wheels, steel body tub, and a fabric or vinyl canopy on a tube frame.
- Driver alone on a front centre saddle with motorcycle-style handlebars. A rear bench for 3 across. Lagos practice adds 1 passenger squeezed beside the driver on the saddle edge [est].
- Lagos body is **yellow**, with a black or dark-green canopy [src street-research]. Black is the dominant canopy colour [est].
- Roll-down side curtains (black canvas or clear PVC) are tied up with straps in dry weather and dropped in rain.
- The rear of the canopy carries the biggest sticker/slogan field on the vehicle.
- The widely used local nicknames are tied to the state programmes that popularised it ("Marwa", "Napep"). In Gidi use our own nickname.

**Kit parts:**
- `tub`: lower body shell, 2.66 m long, widest 1.30 m at the rear wheels, a narrow nose 0.55 m wide carrying the headlamp. Front "apron" panel with a centre headlamp, two small indicators, and a chrome or black nose strip.
- `windscreen`: flat glass 1.05 m wide × 0.55 m tall, single wiper, with a 0.10-0.15 m sticker strip along the top edge.
- `canopy`: three steel tube hoops plus a rectangular roof, flat to slightly domed, 1.70 m to the top. Fabric skin on the sides behind the driver. Open door gaps both sides (no doors; there is a 0.9-1.0 m tall opening each side for the bench).
- `rear_panel`: canvas or vinyl rear with a small rear window (0.5×0.25 m clear PVC). Slogan field 1.1×0.4 m.
- `bench`: rear bench 1.15 m wide, foam in vinyl (black/red/brown), with a backrest. A storage cavity under it for the engine (rear-engined).
- `wheels`: three 8-inch rims with 4.00-8 tyres (about 0.47 m overall diameter) [src 4]. The rear axle has a 1.15 m track [est].
- `curtains`: optional roll-up side flaps, rolled bundle 0.1 m diameter at the roof edge, or dropped.
- `spare`: a spare wheel on the rear panel, sometimes with a printed cover.
- `mudflaps`: 2 rear mudflaps, often with a printed slogan or name.

**Dimensions:** Length 2.658 m, width 1.30 m, height 1.70 m, wheelbase 2.00 m, ground clearance 0.20 m, kerb weight about 400 kg [src 4]. The bench sits at about 0.65 m and the driver saddle at about 0.75 m [est]. Engine: about 200-236 cc, rear-mounted, small exhaust exiting low on the left rear [est].

**Colours (hex):**
- Body yellow `#F0C419`. It fades to `#DDB64A`, and older ones are patched with a brighter repaint `#F7D117` in places.
- Canopy black `#151515` → faded `#3A3A3A` → grey-brown `#55504A`. Sometimes dark green `#1F4A2E` or navy `#1E2A44` [est].
- A black or green body stripe along the lower tub, 0.05 m [est].
- Chrome or black trim. Red tail lamps. Amber indicators.
- Electric keke newcomers are boxier and come in other colours (a green has been reported in the street research [src street-research]).

**Materials:** Pressed steel tub, steel tube frame, PVC-coated canvas canopy, PVC curtains, vinyl seat.

**Variants (rough shares in Lagos [est]):**
- `passenger_classic` 80%: as above.
- `passenger_closed` 8%: aftermarket hard side panels or fixed clear PVC windows. Sometimes a homemade "door" bar across the opening.
- `cargo_flatbed` 5%: same front half with a short cab roof. Behind it, a steel flat tray 1.4×1.25 m with 0.3 m drop sides. Carries crates of drinks, gas cylinders, sacks of rice, plastic chairs, water kegs. Length about 2.9-3.1 m [est].
- `cargo_box` 3%: tray with a steel or plywood box 1.2 m tall. Used for bread, water sachets (pure water), and gas. Painted with business name and phone numbers (invent).
- `electric_square` 4% and growing: a squarer, taller body with a hard roof, often a lighter colour.

**Loads (roof and rear):** Passengers' bags go under the bench. Market loads stick out of the sides: a bag of rice on a lap, a bundle of firewood, an upright gas cylinder, live chickens in a raffia basket. Cargo kekes often overload: sacks stacked 1.0 m above the tray [est].

**Stickers and slogans:**
- Rear canopy: a big hand-painted or printed phrase. Religious ("Blessed by the Most High"-type), pithy proverbs, warnings ("Don't Envy Me"-type), names ("Mama's Boy"-type), and football-club badges.
- Windscreen top strip: one line in gold or white vinyl capitals.
- A union or permit number painted on the side in black or white stencil, 0.08 m tall: e.g. "GD-12-3456" (invent).
- A route permit sticker (square, 0.1 m) on the windscreen.
- Gidi: write originals only (see §9).

**Condition states:**
- `new`: bright yellow, crisp black canopy, clear PVC.
- `worn`: canopy faded and baggy, PVC yellowed and cloudy, mud on the lower tub.
- `battered`: torn canopy patched with a contrasting fabric, a dented nose, a missing headlamp rim, a rear-panel slogan half peeled, a bench with exposed foam.
- `wreck`: no canopy, just the tub on rims behind a mechanic shed; the tube frame rusts orange.

**Occupants:** 1 driver + 3 behind (+1 beside the driver, often). Up to 6 in off-peak back streets [est]. Cargo: 1 driver, maybe 1 loader riding on top of the goods.

**Props and life around it:**
- Day: a rank of 5-20 kekes nose-to-tail at an estate gate or junction ("keke park"). A loader/caller shouting a destination. Drivers chatting, leaning on the canopy. One keke always half-pulled-out with the driver tinkering with the engine.
- Night: a single weak headlamp, often yellowish. Interior dark. Some have LED strip lights in the canopy (blue, pink) [est].

**SELECT BY:**
- `road_class` in (street, lane, main road in sprawl). Barred from expressways, bridges and many central roads since the 2020 restriction (6 LGAs, 9 LCDAs, 10 highways, 41 bridges) [src 9]. Small numbers still use restricted roads [src 9].
- `district`: highest in `sprawl` and `dense_mainland`; feeder ranks at `elite` estate gates (but not inside the estate); a few in `old_island` back lanes; none in `port` main roads.
- `wealth`: inverse.
- `near`: bus_stop (feeder rank within 50 m), market.

**Gidi mapping:** `veh.keke` (passenger variants), `veh.keke_cargo` (flatbed and box). Also a `prop.keke_rank` cluster.

---

### 2. Okada (motorcycle taxi)

**Looks like:**
- An upright 100-150 cc commuter motorcycle: round headlamp in a small cowl, a long flat dual seat, a rear carrier rack, crash bars, a chain guard, a high front mudguard.
- Rider in a reflective or union vest over everyday clothes. A passenger sits astride behind (women sometimes sit side-saddle).
- Bikes are commonly black or red with chrome; Indian and Chinese makes dominate [src street-research].

**Kit parts:**
- `frame_body`: a 2.02 m commuter bike body with tank, side covers and an engine block.
- `seat`: a long seat 0.75 m, often in a **fringed or patterned seat cover** (red, leopard print, black faux-leather with tassels).
- `crash_bars`: tube guards on both sides at the engine.
- `rack`: a rear carrier 0.4×0.3 m, extended by welders to 0.6 m for cargo [est].
- `mudflaps`: long rubber mudflap front and rear, with printed text.
- `mirrors`: two round mirrors on stalks, often one missing.
- `wheels`: 17-inch rims, front 3.00-17, rear 100/90-17 (about 0.60 m overall diameter) [src 5]. Spoked rims with drum brakes.
- `rider_vest`: a reflective vest with a large back number (0.15 m digits) and a union name panel.
- `helmet`: full or half helmet; often not worn but hung on the mirror or worn by the rider only.

**Dimensions:** Length 2.016 m, width 0.74 m, height 1.055 m, wheelbase 1.285 m, kerb weight about 125 kg [src 5]. Seat height about 0.80 m [est].

**Colours (hex):**
- Black `#1A1A1A` (45%), red `#B0201C` (30%), blue `#1E3E8C` (10%), silver/grey `#A9ACB0` (10%), other (5%) [est].
- Chrome exhaust and crash bars `#B8BCBF`, rust-spotted on old bikes.
- Vest colours: fluorescent green `#C8E636`, orange `#FF7A1A`, yellow `#F2E21A`, or a darker union colour with reflective silver stripes `#D8D8D8`. Gidi: invent one union colour per district.

**Variants (shares [est]):**
- `okada_classic` 70%: as above.
- `okada_boxed` 10%: a rear delivery box 0.45×0.45×0.45 m, branded for a dispatch firm (invent). These are the delivery/dispatch bikes, now common across Lagos.
- `okada_ride_hail` 5%: newer bikes with a matching branded helmet for the passenger and a phone holder. Several app operators existed until the 2022 ban [est].
- `private_commuter` 15%: same body with no vest, used by artisans and workers.
- `power_bike` (rare, elite): a large sports or touring bike, seen in convoys or with riders in leather.

**Loads:** The okada is a cargo vehicle too.
- A gas cylinder strapped upright on the rack.
- Two 25 L kegs on each side.
- A 50 kg bag of rice across the seat.
- Planks or steel rods 4-6 m long balanced along the side, sticking out 2 m ahead and behind.
- A sheet of plywood or a mattress held by the passenger.
- Crates of eggs stacked 0.8 m high.
- Live goat across the tank (occasional).
Model 3-4 load meshes that attach to the rack or seat.

**Stickers and slogans:** Short phrases on the front mudflap and the rear mudflap; a name on the fuel tank; a union permit sticker on the front cowl. Gidi originals.

**Condition states:**
- `new`: shiny tank, plastic film still on the seat cover, no dents.
- `worn`: faded tank paint, bent rack, mismatched mirror.
- `battered`: rusty exhaust, cracked side cover, a seat cover torn to the foam, a headlamp cracked or taped, a missing mudguard.
- `wreck`: a frame without wheels in a mechanic yard, or impounded and stacked in a heap of 50-500 bikes at an impound yard (crushing events are publicised) [est].

**Occupants:** Rider + 1 passenger typical; 2 passengers common on back streets; a mother with a child between [est]. Helmets: rider 50% in back streets, passenger 10% [est].

**Props and life around it:**
- Day: an "okada park" at a junction or street mouth: 3-10 bikes angled to the kerb, riders sitting on their bikes or under an umbrella or a tree, a union official with a ledger at a plastic table.
- Night: a single headlamp, often weak; riders cluster under a lit kiosk. Many back-street areas have curfews on bikes [est].

**SELECT BY:**
- `road_class` street/lane: high. Main roads: low to medium in `sprawl`. Expressways and bridges: near zero (restricted since 2020 in many LGAs and on highways; reports say a ban covered more of Lagos from 2022) [src 9, street-research].
- `district`: `sprawl` > `dense_mainland` > `waterfront` landward edge > `old_island` lanes. `elite` interiors only as dispatch bikes.
- `wealth`: inverse, except dispatch bikes that serve wealth.

**Gidi mapping:** `veh.okada`, `veh.bike_dispatch`, load attachments `prop.okada_load_*`, rider `npc.okada_rider`.

---

### 3. Danfo (the yellow minibus)

**Looks like:**
- The defining Lagos vehicle. A boxy cab-over van in **cadmium yellow with two black horizontal stripes** along each side [src 6, 7]. Most often a 1979-1992 European rear-engined boxy van (the T3/Vanagon type) [src 6, 7]. Newer fleets include Japanese cab-over vans [src 8].
- A flat front, slightly raked windscreen, a short flat nose with the grille slot below the screen, rectangular headlamps, and a big black bumper.
- The kerb-side **sliding door is open or missing**, with the conductor hanging out of it.
- Inside, the factory seats are replaced by wooden or metal benches, four people per row [src 7].

**Kit parts (T3-type profile; `veh.danfo_t3`):**
- `body`: a box with a gently curved roof edge, flat sides, 4.57 m long.
  - Front face nearly vertical (about 10-12° back-rake), with a 0.15 m nose.
  - A black plastic strip under the windscreen, with the grille slot.
  - Rectangular single or twin headlamps (0.18×0.13 m) in the lower front.
  - A black bumper 0.18 m tall wrapping round the corners.
- `windscreen`: about 1.55×0.75 m, single pane; often cracked (a radiating crack from one corner); with a 0.12 m tinted sticker strip at the top.
- `cab_doors`: two front hinged doors with a window and a quarter vent.
- `side_glazing`: behind the cab, on each side, 3 equal-ish window panes along the passenger box, plus the sliding door glass on the kerb side.
  - Window band from z = 1.05 m to 1.65 m [est].
  - A **black band** painted around the window line is common [src street-research].
- `slide_door`: a kerb-side (right side; Nigeria drives on the right) sliding door 1.0 m wide. States: closed / open slid back / removed (opening with a bare frame).
- `rear`: a top-hinged tailgate with a large rear window; the engine is low under the rear floor. The tail lamps are vertical blocks at the lower corners.
  - Rear engine-cooling louvres behind the rear side window (on the T3 type) [est].
- `stripes`: two parallel black stripes, each about 0.08-0.12 m [est]: one at the waist (just under the window band, z ≈ 0.95 m), one at sill level (z ≈ 0.45 m). Some buses have one wide stripe only.
- `roof_rack` (optional): welded steel tube rack 2.4×1.5 m, 0.15 m rails, painted black or bare rusty. Loads: sacks, a bicycle, foam mattresses, basins, plastic chairs, sheets of zinc.
- `ladder` (optional, rear): a short welded steel ladder to the rack.
- `wheels`: 14-inch steel rims, 185R14 tyres (about 0.65 m overall diameter) [est, base-vehicle spec]. Hubcaps mostly missing. Steel wheels black or rust.
- `interior`: 4 benches in rows of 4 (plank seats with a steel frame, sometimes foam). A tip-up seat by the door. Bare metal floor. Exposed roof metal, no headlining [src 7].

**Dimensions (T3-type base):** Length 4.57 m, width 1.84 m, height 1.95 m, wheelbase 2.46 m [src street-research, base-vehicle spec]. Ground clearance about 0.18 m; it often sags 0.03-0.06 m at the rear [est].

**Kit parts (newer Japanese cab-over type; `veh.danfo_jvan`):** Same yellow-and-two-black-stripes livery on a semi-cab-over van with a short sloping nose. Length 4.69 m, width 1.69 m, height 1.98-2.1 m, wheelbase about 2.33-2.66 m, 14-15-inch wheels [est, base-vehicle spec]. Two side windows larger and more rounded at the corners. Sliding door on the kerb side.

**Colours (hex):**
- Yellow fresh `#F2C200`, typical faded `#E0B43A`, chalky roof `#D6B867`.
- Stripes and bumpers `#141414`.
- Window rubber black. Glass tinted `#2B3A3A` at 30% opacity, dusty.
- Mismatched panels on 15% [src street-research]: primer grey, an older yellow, or green `#3E6B3A`.
- Roof sometimes painted white `#EDEDE8` or black to reduce heat [est].

**Materials:** Pressed steel (dented), glass, rubber, plywood floor, steel benches.

**Variants (rough shares [est]):**
- `t3_classic` 55% (higher in `dense_mainland`).
- `jvan` 35% (Japanese cab-over, often in better condition).
- `long_wheelbase` 10%: a longer, higher-roof van (§5).
- The older Kombi-type (split-screen, 1960s-70s) appears only in `period: retro` [src 7].

**Stickers and slogans:**
- Windscreen top strip: a single phrase in white or gold, 0.08 m caps.
- Rear window: a full-width phrase, sometimes in English, sometimes Yoruba; a photo sticker of the owner or a pastor (rare now); a football badge.
- Side: owner nickname hand-painted in black above the stripe, behind the front door.
- A route board on the dashboard (a cardboard or plastic sign with 2 place names, invent).
- A 2018 law restricts slogans and stickers on commercial vehicles, but it is not enforced on danfos [src 7].
- Mandatory-ish markers: a painted LG/park code, a stencil serial, and an inspection sticker (invent).

**Condition states:** Most danfos sit at `worn`-to-`battered` (they have been called "war rigs" [src 7]).
- `new`/`refurbished`: freshly respray yellow (often slightly orange `#F5B800`), crisp stripes, chrome-look rims.
- `worn`: faded, stickers, scuffed bumper, a cracked screen.
- `battered`: mismatched door, rust at arches and the windscreen corners, the sliding door missing, the bumper wired on, the rear hatch tied with rope, a smoking exhaust (black soot staining on the rear, `#2A2723`).
- `wreck`: on blocks at a mechanic village; or a burnt-out shell (black/grey `#3A3632`, rust) after a fire.

**Occupants:** Nominal 14; practical 16-18 (four per bench + 2 in the front passenger seat) [src 7, 6]. Plus driver, plus conductor (standing in the doorway or hanging on outside). Off-peak: 2-6 passengers and the conductor yelling for more.

**Props and life around it:**
- Day:
  - At a bus stop: 3-10 danfos nosed at the kerb, double and triple parked in the lane [src street-research]. Conductors shout destinations and wave folded naira notes. Agberos (touts collecting levies) lean on the doors with a ticket book [src 8].
  - A "loading" danfo at a park: a barker at the door, a queue of passengers, the engine running.
- Night: dim headlamps, often one out; no interior light; a conductor visible in the door against the light of a roadside kiosk.
- Breakdowns: a danfo stopped in the right lane with the rear engine lid propped open, the driver crouched, a passenger pushing (push-start), and a branch or a tyre placed 5-10 m behind as a warning triangle [est]. Expect one per 300-600 m of congested main road [est].

**SELECT BY:**
- `road_class` main and expressway service lanes: high. `street`: medium (route streets only). `lane`: none.
- `district`: `dense_mainland` (highest), `old_island`, `sprawl`, `port` (worker routes). `elite` (low; restricted on reform corridors such as the Lekki-Epe pilot from late 2025) [src 2, 10].
- `condition` follows `1 - district poverty` with a wide spread.
- `near`: bus_stop, bus_park, market.

**Gidi mapping:** `veh.danfo_t3`, `veh.danfo_jvan`; NPCs `npc.conductor`, `npc.agbero`; prop `prop.route_board`.

---

### 4. Korope (the smaller yellow minibus; "mini danfo")

**Looks like:**
- A smaller yellow minibus with the same yellow-and-black-stripes livery as the danfo [src 1].
- Several base vehicles. Lagos press names a small Japanese microvan ("Suzuki Every" type) driven as a korope [src 11]. Older small Japanese and European cab-over vans also serve [est].
- Slightly smaller and more manoeuvrable than a danfo, used where demand or roads do not justify a full danfo [src 12].
- Being moved off major highways (Lekki-Epe pilot from 8 Dec 2025) and reassigned to feeder and community routes [src 2, 10].

**Kit parts (microvan korope, `veh.korope_micro`):**
- `body`: a tall narrow box 3.40 m long with a very short sloped nose (0.25 m) and near-vertical sides. The front wheels sit under the front seats.
- `windscreen`: about 1.25×0.7 m.
- `glazing`: 2 side windows behind the front door on each side. A sliding door on the kerb side (and often on both sides on this type).
- `rear`: a top-hinged tailgate with a near-full-height window.
- `wheels`: 12-inch rims, 145R12 tyres (about 0.55 m overall diameter) [est, base-vehicle spec].
- `rack`: a small rack 1.6×1.2 m on 20% [est].

**Dimensions (microvan type):** Length 3.395 m, width 1.475 m, height 1.88-1.90 m, wheelbase about 2.35-2.43 m [est, base-vehicle spec]. Seats: 7-10 crammed (benches 3 across + 2 in front) [est].

**Kit parts (small cab-over van korope, `veh.korope_cabover`):** A 4.3-4.5 m box van, 1.65-1.70 m wide, 1.95 m tall, one-piece flat front, 14-inch wheels; benches for 10-12 [est]. Many are older and rougher than danfos.

**Colours:** Same as danfo. Microvans fade faster and often have a thinner single stripe [est].

**Variants (shares within koropes [est]):** `micro` 45%, `cabover` 45%, `other` (a converted panel van with cut windows, or a minivan with seats removed) 10%.

**Condition states:** As danfo, shifted toward `battered` (koropes are often the cheapest vehicles on the road).

**Occupants:** Driver + 8-12; conductor in the door. Microvans: 1 conductor sitting on the sill with his legs out.

**Props and life:** Korope ranks at feeder junctions and estate gates, mixed with keke ranks. Conductors use shorter calls (one stop name).

**SELECT BY:**
- `road_class` street and main road in `sprawl` and `dense_mainland`; restricted on reform expressway corridors.
- `district` `sprawl` (Lekki-like corridors pre-reform; Alimosho-like everywhere) and `dense_mainland` feeders.
- `wealth`: inverse.

**Gidi mapping:** `veh.korope_micro`, `veh.korope_cabover`. If the owner wants the "Tambulu" name, use it as the Gidi nickname for `veh.korope_micro`.

---

### 5. Newer high-roof minibus / regulated mid-capacity bus

**Looks like:**
- A modern semi-bonneted high-roof van (the late-2000s Japanese long-body type; also Chinese equivalents) with 14-18 seats.
- Used as newer danfos (yellow and black), as interstate "bus" vans at motor parks (white or silver with the operator name), as church and school buses, and as regulated feeder buses in the state's blue-and-white scheme [src 10].

**Kit parts:** A long box with a 0.8 m sloped bonnet, a big windscreen, 4 side windows each side, a kerb-side sliding door, a rear lift gate, 15-inch wheels (about 0.68 m overall diameter), a rear ladder and roof rack on interstate vans [est].

**Dimensions:** Length 5.38 m, width 1.88 m, height 2.285 m, wheelbase 3.11 m [est, base-vehicle spec].

**Colours and liveries [est]:**
- Danfo: yellow `#F2C200` + black stripes.
- Interstate van: white `#F2F2EE` or silver `#B9BCBF` with a company name band in red, green or blue (invent operators).
- Regulated feeder: blue `#1F4FA0` lower body, white `#F4F4F2` upper, a QR permit sticker on the windscreen [src 10].
- Church/school: white with a long text panel (invent).

**Roof loads (interstate):** A tall pile of luggage under a tied tarpaulin (blue or striped), up to 1.0 m high over the roof, roped down; a hen basket; a bag of garri [est].

**Condition:** Generally `new` to `worn`; interstate vans `worn` with road dust on the lower half and the rear.

**Occupants:** Driver + 14-18.

**SELECT BY:** Main roads, `civic` (regulated scheme), bus parks (interstate), churches and schools in `sprawl`/`elite`.

**Gidi mapping:** `veh.minibus_hiroof` with livery `danfo` / `interstate` / `regulated` / `church`.

---

### 6. Molue (historical big yellow bus)

**Looks like:**
- A locally built steel bus body on a medium European truck chassis with a short bonnet (a 1960s-80s "911/1113"-type rigid truck front) [src street-research].
- **Yellow with black stripes**, like a giant danfo [src 13].
- Open door holes (no doors) at the front and rear on the kerb side, with passengers hanging on.
- Window openings with sliding glass or no glass; a flat roof with a front destination box.
- Heavily welded patches on the body [src 14].
- Up to about 80 passengers, most sitting and some standing [src 14]. "As long as there is space for one leg" [src 15].
- Almost extinct: remaining routes in the 2010s were the Lagos-Abeokuta Expressway, the Old Agege Motor Road and the Mile 2 axis [src 13]. Some were converted for other uses [src 13].

**Kit parts:**
- `cab`: short bonnet 1.2 m long, 1.0 m tall at the front, round headlamps, a vertical grille, a one-piece flat windscreen 2.2×0.8 m.
- `body`: a straight-sided box 2.5 m wide, 2.0 m from floor to roof, floor at about 1.0 m.
- `windows`: 8-10 openings per side, each 0.8×0.6 m, with sliding glass on half and nothing on the rest.
- `door_holes`: 2 on the kerb side, 0.9 m wide, one behind the front axle, one ahead of the rear axle, with grab rails and a step.
- `rear`: a flat back with 2 small windows, a ladder and a spare-wheel carrier.
- `roof`: flat, with a roof rail; sometimes luggage.
- `wheels`: 20-inch rims, about 1.0 m overall tyre diameter, twin rear wheels [est].

**Dimensions [est]:** Length 9.5-10.5 m, width 2.5 m, height 3.0-3.2 m, wheelbase 4.8-5.2 m.

**Colours:** Yellow `#E8B828` (often a deeper, more ochre yellow than danfos), black stripes at the waist and above the wheels, black bumpers, and rust everywhere `#8A4A24`.

**Condition:** Always `battered`. In "now" scenes: `wreck` only (a rusting hulk used as a shop, a church office or a sleeping place).

**Occupants:** 50-80; 2-4 people hanging out of each doorway; in period scenes a preacher or a hawker selling medicines on board [est].

**SELECT BY:** `period: retro` main roads in `dense_mainland`/`port`. In `now`: one `wreck` at most per district of `dense_mainland`/`port`.

**Gidi mapping:** `veh.molue` (period), `prop.molue_hulk`.

---

### 7. BRT and regulated city buses

**Looks like:**
- 12 m single-deck, high-floor city buses. The first Lagos BRT (2008) used Indian-built high-floor buses; later fleets included Scandinavian-chassis buses with Brazilian bodies (250 delivered from 2018) [src 16, 17].
- Liveries reported: BRT buses have been blue, and red in a later fleet (imported blue/grey, then repainted red, per one trade source) [src 18, 19]. The state's regulated (non-BRT) bus colours are **blue and white** [src 10, 18].
- Doors on the left (for median stations) and/or right (kerb). A big LED destination display front and side.

**Kit parts:**
- `body`: a 12 m box with a vertical front, big curved windscreen (two panes), rounded roof edges, and a roof AC pod 3×1.8×0.3 m on the rear half.
- `doors`: 2 double-leaf doors (front and middle), 1.2 m wide, glazed.
- `windows`: 6-7 large panes each side, tinted, with a black band.
- `destination`: an LED board 1.8×0.25 m on the front, amber text `#FFB000`.
- `wheels`: 22.5-inch, about 1.05 m overall tyre diameter, twin rear [est].
- High floor: 3 steps up, floor at 0.9 m [est].

**Dimensions:** About 12.0×2.55×3.2 m [src street-research]; wheelbase about 6.0 m [est]. Mid-size regulated buses 8.5-10.5 m [est].

**Colours (Gidi: invent one transit-authority livery, e.g. teal and white, or keep a blue-white family):**
- Blue `#1F4FA0`, white `#F4F4F2`, red `#C0262D`, grey skirt `#55595C` [est for the real families].
- Windows tinted dark `#1E2A30`.

**Variants [est]:** BRT 12 m 60%; medium 9 m feeder 30%; articulated 18 m (rare, future) 10%.

**Condition:** `new` to `worn`. `battered` ones (cracked panels, missing side skirts, faded paint) parked at depots. Burnt-out hulks have appeared after unrest [est].

**Occupants:** 60-100 (about half standing) [est]. Passengers queue in lines at stations.

**Props and life:** Median BRT stations: covered platforms 1 m high with turnstiles, reached by footbridge; queues snaking. Terminal: 10-30 buses parked in rows, a depot shed.

**SELECT BY:** `road_class` expressway with a BRT lane; `district` `civic` and corridors through `dense_mainland`/`sprawl`; terminals at interchanges. Not in `lane`/`street`.

**Gidi mapping:** `veh.bus_brt`, `veh.bus_flm` (feeder), `prop.brt_station`.

---

### 8. Staff bus / coaster

**Looks like:**
- A 26-30 seat midibus with a short sloped bonnet, a big windscreen, a front folding door on the kerb side, a long row of sliding windows, and a rear emergency door.
- Used as company staff buses, school buses, church buses, university shuttles, hotel and airport shuttles, and some interstate runs [est].
- Usually white with company colours, or a brand-painted full livery for banks and telecoms (invent).

**Kit parts:** `body` 6.99 m box with a rounded roof; `door` kerb-side front folding door 0.75 m; `windows` 6-7 per side, sliding, tinted; `ac_pod` (optional) roof unit; `ladder` and `rack` on interstate versions; `wheels` 16-17.5-inch, about 0.78 m overall diameter, twin rear [est].

**Dimensions:** Length 6.99 m, width 2.03 m, height 2.63 m, wheelbase 3.935 m [est, base-vehicle spec].

**Colours [est]:** White `#F2F2EE` 60%; school yellow `#F2C200` with black "SCHOOL BUS" text 15%; company colour band (blue, green, red, purple) on white 25%. Church buses carry a long text name.

**Condition:** Corporate `new`/`worn`; school and church `worn`/`battered`.

**Occupants:** Driver + 26-30.

**SELECT BY:** `civic`, `elite` office districts, `port` (worker buses), schools and churches in `sprawl`. Morning 06:00-08:00 and evening peaks. Parked in company yards and church car parks.

**Gidi mapping:** `veh.coaster` (liveries `staff`, `school`, `church`, `shuttle`).

---

### 9. Interstate luxury coach ("luxurious bus")

**Looks like:**
- A 12-14 m high-deck coach with a raked one-piece windscreen, a tall body, and long tinted window bands. Brazilian- and Chinese-bodied coaches are common; a 59-seat high-decker has been sold into Nigeria [src 20].
- Operators paint bold full liveries: white base with large swooshes in red, green, blue, orange, and the company name 0.6 m tall along the sides and on the rear (invent operator names).
- A rear ladder or no rack (luggage in the belly).

**Kit parts:** `body` coach shell with 3 luggage-bay doors each side; `door` front kerb-side plug door; `windows` 7-8 big panes; `rear` with the engine grille and a big rear window or a full-panel graphic; `mirrors` "rabbit ear" mirrors on stalks; `wheels` 22.5-inch, 2 or 3 axles.

**Dimensions [est]:** Length 12.0-13.7 m, width 2.55 m, height 3.6-3.9 m, wheelbase 6.0-7.5 m.

**Colours [est]:** White `#F4F4F2` base; accents red `#C8102E`, green `#0E7A3B`, royal blue `#1E4FB4`, orange `#F28C1E`; tinted glass `#1A2228`.

**Variants:** Big coach 60%; 30-seat midi-coach 25%; high-roof van (§5) 15% [est].

**Condition:** `worn` (road dust, red laterite on the lower 0.6 m after northern routes); `battered` coaches with cracked bumpers and taped lamps run cheap routes.

**Occupants:** 45-59 seated [src 20], plus a conductor.

**Props and life:** Luxury bus parks: a walled yard with 10-40 coaches parked nose-in, a waiting shed with plastic chairs, ticket kiosks, porters, hawkers of bread and drinks, roof luggage loaders, and a loudspeaker. Lagos moved interstate operations out of the old central parks to designated parks on the city edge in 2017 [src 21]. Departures at dawn; arrivals at night with headlights blazing.

**SELECT BY:** `road_class` expressway (exit corridors) and `near: bus_park` on the city edge (`sprawl`, `dense_mainland` edge); none in `old_island` lanes or `elite` interiors.

**Gidi mapping:** `veh.coach`, `prop.luxury_park`.

---

### 10. Private cars

**Looks like:** A huge range of used ("tokunbo", i.e. foreign-used, imported second-hand) Japanese, Korean, German and American cars, mostly 10-25 years old, plus "Nigerian-used" cars that are older and rougher. New cars and big SUVs dominate in `elite`.

Locals give popular generations nicknames (patterns: a body that looks fat; a car that looks muscular; a car that "came out of nowhere") [est]. Gidi should invent its own nicknames for its own generic bodies.

**Kit bodies (generic profiles; all [est, base-vehicle spec] unless noted):**

| Body | L×W×H (m) | Wheelbase | Wheel (overall dia.) | Share overall | Share `elite` |
|---|---|---|---|---|---|
| `sedan_mid` (mid-size 4-door, 2000s; the commonest Lagos car) | 4.80×1.82×1.47 | 2.77 | 16" (0.66) | 30% | 15% |
| `sedan_compact` (compact 4-door, 2000s) | 4.53×1.70×1.47 | 2.60 | 15" (0.62) | 15% | 5% |
| `sedan_old` (1990s rounded saloon; 1980s boxy saloon in `retro`) | 4.60×1.70×1.40 | 2.60 | 14" (0.60) | 8% | 0% |
| `hatch_small` | 3.80×1.68×1.50 | 2.45 | 14" (0.58) | 6% | 3% |
| `suv_mid` (2000s crossover SUV, curvy) | 4.73×1.85×1.68 | 2.72 | 17" (0.72) | 15% | 25% |
| `suv_big` (boxy full-size 4×4 "jeep") | 4.95×1.97×1.90 | 2.85 | 18" (0.78) | 6% | 25% |
| `suv_square_luxury` (very boxy, upright luxury off-roader) | 4.87×1.98×1.97 | 2.85 | 20" (0.80) | <1% | 5% |
| `mpv` (2000s 7-seat minivan with sliding doors) | 5.08×1.97×1.75 | 3.03 | 16" (0.70) | 8% | 7% |
| `pickup` (double-cab) | 5.33×1.86×1.82 | 3.09 | 17" (0.75) | 5% | 8% |
| `wagon_old` (1980s-90s long estate, long-distance hire) | 4.80×1.73×1.52 | 2.90 | 14" (0.60) | 2% | 0% |
| `luxury_sedan` (executive saloon) | 5.10×1.90×1.47 | 3.05 | 18" (0.70) | 4% | 12% |

**Colours (from the street research, refined [est]):** silver/grey `#A9ACB0` 35%, black `#141414` 20% (40% in `elite`), white `#F0F0EE` 15%, dark blue `#22304F` 8%, champagne/gold `#B8A47A` 8%, dark green `#2E4A3A` 4%, red/maroon `#7A1E22` 5%, other 5%.

**Window layouts:**
- Sedans: 6-light glasshouse (2 doors each side + a small rear quarter).
- SUVs: 6-8 lights; the rear three are tinted very dark `#101418`.
- `elite`: full tint on all windows except the windscreen (a dark tint strip on top).

**Typical modifications [est]:**
- Dark window tint (permits required; very common).
- Chrome aftermarket rims on mid sedans.
- A "body kit" facelift: older SUV bodies retrofitted with a newer front fascia and lamps (a very Lagos pattern; mismatched front vs. rear styling).
- Bull bars on pickups and big SUVs.
- Plastic headlamp covers yellowed.
- Steering-wheel and seat covers; a rosary or a dashboard flag; a scented sachet.
- Stickers on the rear screen: church names, school stickers, estate access stickers (barcode, invent).

**Plates:** Nigerian plates are white with a coloured motif and text; Gidi designs its own (e.g. a white plate with a green coastline band, three letters + three digits + two letters, invent).

**Condition by wealth [est]:**
- `elite`: 70% new/clean, 25% worn, 5% battered (staff cars).
- `dense_mainland`: 10% new, 45% worn, 40% battered, 5% wreck (parked hulks).
- `sprawl`: 15/45/35/5, with heavy laterite dust.

**Occupants:** Driver + 0-4. `elite`: a chauffeur in front + the owner in the back right seat. Convoys: 2-5 black SUVs in a line, one escort pickup with armed police and a siren [est].

**Props and life:**
- Parked two deep on both kerbs of `old_island` streets and at markets; half on the walkway.
- Car washes at road edges (a hose, a drum, a shade umbrella).
- "Rewire" roadside mechanics with a car on a jack.
- At night: headlights, many cars with one headlamp out, hazard lights used in traffic jams.

**SELECT BY:** `wealth` picks body and condition; `district` picks density; `near: market` picks double-parking.

**Gidi mapping:** `veh.car_sedan_mid`, `veh.car_sedan_compact`, `veh.car_sedan_old`, `veh.car_hatch`, `veh.car_suv_mid`, `veh.car_suv_big`, `veh.car_suv_luxury`, `veh.car_mpv`, `veh.car_wagon`, `veh.car_luxury`, `veh.pickup`; prop `prop.convoy`.

---

### 11. Yellow taxi and ride-hail

**Looks like:**
- Lagos street-hail cabs are **yellow with a black stripe** along the sides and painted fleet numbers [src 22]. Mostly privately owned and "almost always in some state of disrepair" [src 22].
- A 2015 scheme proposed replacing the black stripes with the state's colours, outcome unclear [src 22].
- The base car is an older compact or mid sedan (§10). A roof "TAXI" sign is rare [est].
- Ride-hail cars look like ordinary private cars, with a small app sticker on the windscreen.

**Kit parts:** Sedan body + yellow paint `#F2C200` + a 0.10 m black stripe at the waist (or a chequered band in some older fleets) + painted number on the front doors and rear wing (0.10 m digits) + an optional roof sign 0.6×0.15×0.18 m.

**Condition:** `worn`/`battered` 80%.

**Occupants:** Driver + 1-4.

**SELECT BY:** `old_island` main roads, airport, hotels, `civic`; 1-3% of cars. Ride-hail: `elite` and `civic` up to 15% of cars [est].

**Gidi mapping:** `veh.taxi_yellow` (livery on `veh.car_sedan_*`), `veh.ridehail` (sticker variant).

---

## 3. Goods vehicles

### 12. Tipper and sand truck

**Looks like:**
- A 6×4 or 8×4 heavy cab-over truck with a steel tipping box. Chinese cab-over tippers dominate new sales; sand and gravel hauling is a core use [src 23, 24].
- Older European cab-overs and bonneted American-style trucks still run.
- The box is heaped with sharp sand (wet beige), laterite (red-orange), granite chippings (grey) or "stone dust".
- Box sides often carry the owner's name or a slogan; a tarpaulin may be roped over the load.

**Kit parts:**
- `cab`: cab-over block 2.5 m wide, 2.0 m long, roof at 3.2-3.4 m, a big grille, a sun visor, and 2 wide mirrors.
- `box`: a steel tipper body 5.6×2.3×1.5 m (about 20-25 m³), with a cab protector over the cab, a rear swing gate, and vertical ribs every 0.6 m.
- `hoist`: a front telescopic ram (visible when tipped, at 45-50°).
- `chassis`: 3 axles (front + tandem rear) or 4 (2 front + 2 rear); fuel tank and a toolbox along the side.
- `wheels`: 20-inch, 12.00R20 tyres (about 1.12 m overall diameter) [est].
- `load`: a heaped mound, 0.3-0.8 m above the box sides; a loose spill trail.

**Dimensions [est]:** Length 8.5-9.5 m, width 2.5 m, height 3.4 m (cab) / up to 3.6 m with a heaped load; wheelbase 3.8+1.35 m.

**Colours [est]:**
- Cab: red `#B3241C`, white `#EDEDE8`, yellow `#E8B21C`, green `#2C6E3A`, blue `#1F4F9A` (roughly equal shares).
- Box: matching or rust-red `#8F3B2A` with sand stains.
- Loads: sharp sand `#C9B48A` (wet `#A8946A`), laterite `#B5552C`, granite `#8A8A86`.

**Variants [est]:** New Chinese cab-over 50%; older European cab-over 30%; old bonneted 15%; small 2-axle 10-tonne tipper 5%.

**Condition:** Mostly `worn`/`battered`: a cracked windscreen, a missing mirror glass, a box dented and caked with sand. Breakdowns on hills and bridge approaches with the box half-raised.

**Occupants:** Driver + 1-2 "motor boys" (apprentices), one riding on the box rim or the cab roof [est].

**Props and life:** Queues at quarry and sand landings; sand heaps tipped on building sites; a man with a shovel on top; a "sand market" lot with 5-20 trucks along a lagoon shore.

**SELECT BY:** `near: construction` (new estates in `sprawl` Lekki-like corridors), sand landings on the `waterfront`, expressways. `elite`: only on building sites.

**Gidi mapping:** `veh.tipper` (load variants `sand`, `laterite`, `granite`, `empty`), `prop.sand_heap`.

---

### 13. Fuel tanker

**Looks like:**
- An articulated tractor and a cylindrical or elliptical steel/aluminium tank semi-trailer (often around 33,000 L in Nigerian practice [est]).
- Tractors: bonneted American-style (long nose, vertical stacks) are iconic in Nigeria; European and Chinese cab-overs are also common [est].
- The tank is silver, white or painted in marketer colours with the company name and a large "FLAMMABLE" and a hazard diamond.
- A top walkway with a handrail, manhole lids, side ladder, rear valves with hoses, and a "spill box" toolbox.

**Kit parts:**
- `tractor_bonneted`: 6.5 m long, a bonnet 2.0 m, cab roof at 3.3 m, twin chrome exhaust stacks, a big chrome grille, a bull bar, and air horns on the roof.
- `tractor_cabover`: 5.8 m long, a flat cab face, roof at 3.4 m.
- `tank`: a cylinder or elliptical barrel 11.5-12.5 m long, about 2.4 m diameter, top of tank at 3.6-3.8 m, 3-4 manholes, a catwalk rail, a rear ladder, hoses stowed in side tubes, and a 3-axle bogie at the rear.
- `wheels`: 22.5-inch (about 1.05 m overall diameter), 3 trailer axles, twin.

**Dimensions [est]:** Overall rig 16-17.5 m long, 2.5 m wide, 3.7-3.9 m high.

**Colours [est]:**
- Tank: polished/galvanised `#B8BCBF`, white `#EDEDE8`, or brand colours (invent; e.g. a green tank with a yellow band).
- Tractor: red, white, blue, yellow; chrome `#C9CDD0`.
- Grime: black soot on the rear `#2A2723`, fuel drip stains on the tank belly `#4A3A2A`.

**Variants:** Fuel 80%, gas (LPG) "bullet" tanker 10% (white, rounded ends, smaller diameter 2.0 m), bitumen/edible oil 10% [est].

**Condition:** `worn`/`battered`; a significant share shows dents, peeling labels, leaking valves. A burnt-out tanker shell (blackened tank, melted tyres) appears after crashes [est].

**Occupants:** Driver + 1 motor boy.

**Props and life:** Kilometre-long queues parked on the shoulder and in the slow lane near depots and port roads [src street-research]; drivers sleeping in hammocks slung under the trailer, cooking on small stoves beside the wheels; food sellers and mechanics along the queue [est].

**SELECT BY:** `port` (very high), expressways (medium), `near: filling_station` (one tanker discharging), depot tank farms. Not in lanes.

**Gidi mapping:** `veh.tanker_fuel` (tractor variants), `veh.tanker_gas`, `prop.tanker_wreck`, `prop.tanker_queue`.

---

### 14. Container trailer ("trailer")

**Looks like:**
- A tractor with a skeletal or flatbed trailer carrying a 20' or 40' container. In Lagos speech the whole rig is "a trailer" [est].
- Container doors at the rear with vertical locking bars; container colours are faded corporate shipping colours [src street-research].
- Trailers queue for kilometres on port roads, two abreast, and sometimes for days [src street-research].
- Unsecured containers falling off trailers are a known hazard (a container lying on its side at a junction or on a crushed car) [est].

**Kit parts:**
- `tractor` (as §13).
- `trailer_skeletal`: a steel chassis frame 12.5 m with twist-locks, 2-3 axles.
- `trailer_flatbed`: a flat deck 12.5 m.
- `container_20`: 6.06×2.44×2.59 m; `container_40`: 12.19×2.44×2.59 m; `container_40hc`: 12.19×2.44×2.90 m [est, ISO standard].
- Container details: corrugated sides (vertical corrugations, pitch about 0.28 m), corner castings, rear double doors with 4 locking bars.

**Dimensions [est]:** Rig 16.5 m, deck height 1.4 m, top of container 4.0-4.3 m.

**Colours (containers, [est]):** rust red `#8F3B2A` 25%, blue `#2A4F7A` 20%, green `#3D6B4A` 10%, grey `#8A8D8F` 15%, white `#E6E6E2` 10%, orange `#D9662B` 8%, maroon `#5E2328` 7%, yellow `#D8B230` 5%. Fade and rust streaks from the corners.

**Condition:** Containers `worn`; tractors `battered`. Abandoned trailers on blocks along port roads.

**Occupants:** Driver + motor boy.

**SELECT BY:** `port` (60% of traffic with tankers, [src street-research]), expressways to the port and the north, container yards.

**Gidi mapping:** `veh.trailer_box` (container variants), `prop.container_stack`, `prop.trailer_queue`, `prop.container_fallen`.

---

### 15. Rigid lorry with wooden body; mammy wagon (bolekaja)

**Looks like:**
- **Rigid goods lorry:** a short-bonneted 1960s-80s medium truck (the "911"-type front) or a newer cab-over, with a **tall wooden cargo body**: plank sides 1.2-1.8 m tall, often painted, with a front "head board" over the cab. Loads from the north (onions, yams, tomatoes in raffia baskets, cattle, bags of grain) piled high and roped under a tarpaulin, with people sitting on top [est].
- **Mammy wagon / bolekaja:** a light truck converted to carry passengers, with a wooden body, a plywood roof covered in tarpaulin, wooden bench seats, and a painted slogan on the front [src 25]. Historical; rare today [src 25].

**Kit parts:**
- `cab_shortbonnet`: a 1.0 m short bonnet, round headlamps, a vertical grille, a 2-panel windscreen, cab roof at 2.6 m.
- `wood_body`: a timber box 5.0×2.3 m, plank courses of 0.2 m, painted panels (blue, green, red) with floral or geometric border designs; a head board 0.8 m above the cab with a painted slogan; a rear gate with 2 painted panels and a central slogan.
- `load_pile`: a net of baskets/sacks rising 1.5-2.5 m above the sides, wider than the body by 0.2 m each side, under a tarp with ropes; 2-6 people on top.
- `mammy_body`: a wooden passenger body with open sides (half-height wooden panels), 4-6 cross benches, a plywood roof on posts, a rear step, and a roof rack.
- `wheels`: 20-inch, about 1.0 m overall diameter, twin rear.

**Dimensions [est]:** Lorry 7.0-7.5 m long, 2.4 m wide, cab 2.6 m tall, body top 3.2 m, loaded up to 4.5-5.0 m. Mammy wagon 6.5×2.3×3.0 m.

**Colours [est]:** Cab red `#A8261E`, blue `#1E4A8C`, cream `#E8DDC0`, green `#2F6A3A`; wooden body painted with bright bands (yellow `#F0C419`, green `#2E8B3A`, red `#C0262D`, sky blue `#4FA3D8`) over raw timber `#8A6A44`; tarp blue `#2F5FA8` or striped.

**Slogans:** On the head board and the tailgate, hand-painted: proverbs, religious phrases, and humour (the slogan tradition is old and widespread on West African lorries [src 25]); now often replaced by plastic lettering [src 25]. Gidi originals.

**Condition:** `battered` almost always; timber split, paint peeling in flakes, a cab with welded patches.

**Occupants:** Driver + 2 motor boys + 0-10 riders on the load.

**SELECT BY:** `near: market` (food markets on the city edge; produce and cattle markets), expressways from the north, `period: retro` for mammy wagons. Night arrivals with goods unloaded by head porters.

**Gidi mapping:** `veh.lorry_wood` (loads `produce`, `cattle`, `grain`, `empty`), `veh.mammy_wagon` (retro), `veh.lorry_cabover_box` (newer).

---

### 16. Water tanker (rigid)

**Looks like:** A rigid 2-3 axle cab-over or old bonneted truck carrying a cylindrical tank of 10,000-20,000 L, often painted blue or white with "WATER" or "DRINKING WATER" and a phone number (invent). Delivers to estates, building sites and households where public supply is poor [est].

**Kit parts:** `cab` (as tipper or lorry); `tank` 6.0-7.0 m long, 2.0-2.2 m diameter, a top manhole, a rear outlet valve with a canvas hose coiled on a hook; `wheels` 20-inch.

**Dimensions [est]:** 8.0-9.0 m long, 2.5 m wide, 3.2 m high.

**Colours [est]:** Tank sky blue `#3C7FC0` 40%, white `#EDEDE8` 30%, galvanised 20%, other 10%; drip streaks and algae green `#4A6A3A` at the outlet.

**Condition:** `worn`/`battered`.

**Occupants:** Driver + 1.

**Props and life:** Parked at a house gate with a hose over the fence into an overhead tank (`prop.water_tank_stand` from the buildings research); a puddle under the outlet.

**SELECT BY:** `sprawl` (high), `elite` estates (deliveries), building sites; rarely in `dense_mainland` (those use carts).

**Gidi mapping:** `veh.tanker_water`.

---

### 17. Refuse trucks and informal waste carts

**Looks like:**
- **Compactor truck:** a cab-over with a rear compactor body (a smooth curved or ribbed box with a rear hopper and a lift-up tailgate). The state agency deploys compactors and skip trucks, and over 400 private sector (PSP) operators collect waste [src 26, 27].
- **PSP open tipper:** an older tipper with mesh-raised sides and loose refuse heaped high; workers in coveralls ride on top [est].
- **Informal cart pushers:** men with wooden push carts (§24) collecting household waste for a fee, dumping in canals or at transfer points [est].

**Kit parts:** `compactor_body` 4.5×2.4×2.3 m on a cab-over chassis, rear hopper with a steel lip 0.9 m off the ground, side step platforms and grab handles for crew; `skip_loader` (a truck with 2 swing arms and a 6 m³ skip); `open_refuse` a tipper box with mesh extensions; `wheels` 20-inch.

**Dimensions [est]:** Compactor 8.2×2.5×3.4 m; skip loader 7.0×2.5×3.2 m.

**Colours [est]:** Gidi invents an agency colour (e.g. green `#2E7D3A` with white). Real compactors in many Nigerian cities are green or white with agency bands. Grime: brown leachate streaks `#5A4A32` under the tailgate.

**Condition:** New compactors `new`/`worn`; PSP trucks `battered`.

**Occupants:** Driver + 2-4 loaders (hanging on the back steps).

**Props and life:** Dawn rounds (05:00-09:00); refuse heaps on medians and at street corners waiting; a sweeper team in orange or green vests; a transfer point with a heap 3-5 m high and a loader.

**SELECT BY:** All districts; frequency rises with `wealth` (formal) and falls into carts in `dense_mainland`/`waterfront`.

**Gidi mapping:** `veh.refuse_compactor`, `veh.refuse_skip`, `veh.refuse_open`, `prop.refuse_heap`.

---

### 18. Light trucks, box vans and pickups

**Looks like:** 2-5 tonne cab-over light trucks with a dropside deck or a box body (bakeries, beverages, furniture, cement distributors), and single-cab pickups loaded high. Panel vans for courier and church use. Very common at markets and shop strips [est].

**Kit parts:** `cab_light` cab-over 1.7-2.0 m wide; `deck_dropside` 3.5×1.9 m, sides 0.4 m; `box` 3.8×2.0×2.0 m with roll-up or swing doors and a full-side ad (invent); `pickup_single` 5.0×1.76×1.75 m with a 2.3 m bed; 15-16-inch wheels (single front, twin rear on light trucks).

**Dimensions [est]:** Light truck 5.5-6.5×1.9-2.1×2.5-3.2 m; pickup as table §10.

**Colours [est]:** White 50%; beverage/brand colours (red, green, blue, yellow) 30%; others 20%.

**Loads:** Crates of soft drinks stacked 1.5 m; cement bags; plastic chairs nested 2 m tall; foam mattresses; a deep-freezer; iron rods sticking 3 m past the tailgate with a red rag tied on.

**Occupants:** Driver + 1-2; loaders ride on the load.

**SELECT BY:** `near: market`, shop streets, `port` warehouses; `dense_mainland` and `old_island`.

**Gidi mapping:** `veh.lighttruck_dropside`, `veh.lighttruck_box`, `veh.pickup_single`, `veh.van_panel`.

---

## 4. Police, military, emergency and agency vehicles (generic)

Sources here are thin (search budget ran out). Treat liveries as patterns to invent from, not facts.

### 19. Police vehicles

**Looks like:**
- Double-cab pickups (Japanese and American pickups; one state handover listed 55 American-brand pickups and 10 large Japanese 4×4 pickups for the rapid response squad [src 28]).
- **Rear bed with two facing benches** (welded steel bench along each side, sometimes a rollbar), 3-6 armed officers sitting facing outward or inward, rifles upright.
- Liveries: dark/black for rapid-response units, and dark blue or white with blue and a "POLICE" lettering band for patrols [est]. Roof light bar (red/blue) and a siren.
- Patrol vans are worked 24 hours and are often dirty [src 29].
- Also: old saloon patrol cars, a "Black Maria" prisoner van (a closed van with small barred windows), and riot-control trucks (armoured, water cannon) in `civic` at times [est].

**Kit parts:** `pickup_double` body (§10) + `bench_bed` (two 1.6 m benches, 0.45 m high, a rollbar hoop 1.2 m above the bed) + `lightbar` 1.2×0.25×0.12 m + `bullbar` + `lettering` ("POLICE"-style text in Gidi's own wording, e.g. a "GIDI STATE POLICE" placeholder) + 1-2 `rifle` props.

**Dimensions:** As pickup: 5.33×1.86×1.82 m, wheelbase 3.09 m [est, base-vehicle spec]; light bar adds 0.12 m.

**Colours (Gidi to invent; real patterns [est]):** Black `#121212` with white text; dark navy `#1B2440` with a white or light-blue band; white `#F0F0EE` with a blue band `#1E3E8C`. Light bar red `#E0201C` / blue `#1F4FE0`.

**Condition:** `worn` (mud, scratches, a dented bed).

**Occupants:** Driver + 1 in the cab + 3-6 in the bed.

**Props and life:** Parked at a junction with officers standing by the bed; parked across the slow lane at a checkpoint (§21); escorting a convoy at speed with the siren on.

**SELECT BY:** Main roads and expressways (patrols), `elite` (escorts, gates), `civic` (stations), `port` (checkpoints), night (higher share).

**Gidi mapping:** `veh.police_pickup`, `veh.police_van`, `veh.police_saloon`, `veh.prisoner_van`.

### 20. Military vehicles

**Looks like:** Olive or camouflage pickups with mounted benches; 4×4 troop trucks with canvas tilts; occasional armoured personnel carriers at major checkpoints and near barracks [est]. Soldiers sit in the bed with rifles.

**Kit parts:** `mil_pickup` (pickup + camo paint + bench + a pintle mount); `mil_truck` cab-over or bonneted 4×4, 7.5×2.5×3.0 m, a canvas tilt over hoops, 2 axles of big single tyres (about 1.1 m diameter); `apc` boxy 4×4 6.5×2.6×2.6 m (rare).

**Colours [est]:** Olive drab `#4B5320`, desert sand `#C2B280`, woodland camo (`#4B5320`, `#2E2B1E`, `#7A6A4A`, `#1E1E16`), canvas `#5A5A3E`.

**Condition:** `worn`.

**SELECT BY:** `near: barracks`, expressway checkpoints at district boundaries, `port` and `waterfront` (naval pickups in navy grey `#5A6670` with a "NAVY"-type band, invent).

**Gidi mapping:** `veh.mil_pickup`, `veh.mil_truck`, `veh.mil_apc`, `veh.navy_pickup`.

### 21. Checkpoint set

**Looks like [est; street research]:**
- A lane narrowed by **oil drums** painted red and white (or rusty), **old tyres** stacked 2-3 high, a **plank studded with nails** ("spikes") laid across one lane, sometimes a **log** or a steel barrier.
- A pickup parked at an angle; officers standing under a tree or a beach umbrella; a plastic chair; a lamp or a car's headlights at night.
- Traffic slows to walking pace; danfos queue; a hawker sells water.
- Military checkpoints add **sandbag walls** (0.6 m high, 2-3 m long), a small hut, and a "STOP" sign board.

**Kit parts:** `drum` 0.58 m diameter × 0.88 m, red `#C0262D` / white bands, rusty; `tyre_stack`; `spike_plank` 3.0×0.15×0.05 m with nail points; `sandbag_wall` modules 1.0×0.5×0.3 m bags (`#A89A72` faded `#C8BC98`); `sign_stop` 0.6 m octagon on a pole; `umbrella`; `chair_plastic`.

**Dimensions:** Occupies 8-15 m of carriageway length, closes 1 of 2-3 lanes.

**SELECT BY:** Expressways at night (district boundaries), `port` gates, `elite` estate approaches, near barracks. 1 per 3-5 km of expressway at night [est].

**Gidi mapping:** `prop.checkpoint_police`, `prop.checkpoint_military`.

### 22. Ambulance

**Looks like:** A high-roof van (§5 type) or a box-body ambulance on a light truck, white with a reflective chevron or checker band (red, green or yellow) and a roof light bar [est]. The state service runs about 36 ambulances from 4 bases, plus mobile ICUs and **water ambulances** for riverine communities [src 30]. Private hospital ambulances are older vans with hand-lettered names.

**Kit parts:** `van_hiroof` + `lightbar` + `rear_doors` (double) + `band` (a 0.25 m reflective band at the waist) + `cross_or_star` emblem (invent a Gidi emblem).

**Dimensions [est]:** 5.3×1.9×2.4 m.

**Colours [est]:** White `#F4F4F2`, band red `#D32027` or fluorescent yellow-green `#C8E636` with green `#00843D` checks; light bar red/blue.

**Condition:** State: `new`/`worn`. Private: `worn`/`battered`.

**SELECT BY:** `civic` (hospitals), expressway incident points, jetties (water ambulance §37).

**Gidi mapping:** `veh.ambulance`, `veh.ambulance_private`.

### 23. Traffic, task-force, tow and fire vehicles

**Looks like [est; thin sources]:**
- **Traffic agency:** officers in a distinct two-colour uniform (one source says purple-and-yellow [src 31]; another says yellow or orange [src 32]), standing at junctions. Vehicles are pickups and saloons in agency colours with a band and the agency name, and **tow trucks** (a light truck with a boom or a flatbed) that remove broken-down and illegally parked vehicles. Tow trucks are needed constantly for broken-down trucks on port roads [src 33].
- **Environmental / "task force" squads:** open pickups and a lorry with a crane, used for raids on street traders; officers in the bed; seized goods and kiosks piled on the lorry [est].
- **Federal road safety / vehicle inspection:** pickups and saloons with reflective bands; officers in reflective jackets at expressway lay-bys [est].
- **Fire engines:** red cab-over pumpers 8×2.5×3.2 m with ladders on the roof, white bands; often old [est].

**Kit parts:** `traffic_pickup` (pickup + light bar + agency band); `tow_boom` (light truck + boom + hook + chains, yellow `#F2B800` boom); `tow_flatbed` (tilting deck 6 m); `taskforce_lorry` (lorry with a loader crane, cage sides); `fire_engine` (cab-over + equipment lockers with roller shutters + roof ladder); `officer_post` (a 1.0 m round painted drum or a small umbrella stand at a junction).

**Colours (Gidi invents; e.g.):** Traffic agency: white with a wine `#6A1E3A` and yellow `#F2C200` band. Task force: dark green `#1F4A2E`. Fire: red `#C8102E` with white `#F4F4F2`.

**Condition:** `worn`; fire engines often `battered`.

**SELECT BY:** Junctions on main roads (traffic posts, 1 per 2-3 major junctions), `old_island` and `civic` (task force raids near markets), impound yards (`prop.impound_yard` with seized okadas, kekes, cars), fire stations in `civic`.

**Gidi mapping:** `veh.traffic_pickup`, `veh.traffic_saloon`, `veh.tow_boom`, `veh.tow_flatbed`, `veh.taskforce_lorry`, `veh.fire_engine`, `prop.impound_yard`.

---

## 5. Hand-pushed and pedal vehicles

### 24. Truck pusher cart ("truck" / omolanke-type)

**Looks like [est; few sources]:**
- A long, low wooden flat cart on **two car or pickup wheels** (often old tyres, sometimes mismatched), with **two long handles** at the front, pushed or pulled by one man, with a second pushing from behind on heavy loads [street-research].
- The deck is planks on a steel or wooden frame, worn grey and greasy, edged with a strip of tyre rubber or a steel angle.
- Carries anything: market goods, building materials, furniture, scrap metal, refuse, water kegs, a broken-down generator.
- In Lagos speech the cart is often just called a "truck", and pushers have their own unions [est].

**Kit parts:**
- `deck`: 2.2-2.6×1.0-1.2 m, deck at 0.7-0.8 m, plank courses 0.15 m, rails 0.1 m.
- `axle`: a car axle stub or a steel tube axle under the middle, slightly rear of centre.
- `wheels`: 2 car wheels 13-15-inch (0.58-0.65 m overall diameter), black, bald.
- `handles`: 2 long timbers or steel tubes 1.0-1.2 m beyond the deck, joined by a crossbar.
- `stand`: a wooden prop leg at the front.
- `load`: modular stacks (sacks, crates, kegs, zinc sheets, refuse sacks, a fridge).

**Dimensions:** About 2.5-3.0×1.0-1.2 m footprint [street-research], 0.8 m deck; overall with handles 3.4-3.8 m [est].

**Colours [est]:** Weathered timber `#7A6248` → grey `#6A6458`; steel frames painted blue `#2F5FA8`, green `#2E6B3A` or red `#A8261E`, chipped; a painted name on the side rail.

**Variants [est]:** `goods` 60%; `refuse` 25% (sides built up with plywood or mesh, heaped with bagged refuse); `scrap` 10%; `water` 5% (see §27).

**Condition:** `worn` to `battered`; `wreck` as a cart on its side in a market.

**Occupants:** 1-2 pushers; sometimes a child riding the load.

**Props and life:** Clusters of 3-10 at market edges; moving in the road among cars at walking speed (1-1.5 m/s); parked by kerbs overnight chained.

**SELECT BY:** `old_island` (very high, narrow market lanes), `dense_mainland` markets, `port` (scrap), `waterfront` landward edges. Not on expressways.

**Gidi mapping:** `cart.pusher` (load variants), `npc.cart_pusher`.

### 25. Wheelbarrow

**Looks like:** A steel tray barrow with one pneumatic wheel and two handles, black or galvanised [street-research]; used for building materials (sand, blocks), market goods, water kegs (4-6 × 25 L), and a "mobile shop" (sugar cane, fruit, recharge cards) [est].

**Kit parts:** `tray` 0.85×0.65×0.25 m, pressed steel, 80-100 L; `frame` tube; `wheel` 0.40 m diameter; `handles` 1.5 m overall.

**Dimensions:** About 1.5×0.65×0.65 m [street-research, est].

**Colours [est]:** Black `#1E1E1E` 40%, galvanised `#9EA3A6` 30%, green or red 20%, rusted orange `#9C5A2E` 10%.

**Condition:** Mostly `worn`; tray dented, rust holes in `battered`.

**SELECT BY:** `near: market`, `near: construction`, `waterfront`, `sprawl` water-scarce streets.

**Gidi mapping:** `cart.barrow` (loads `sand`, `blocks`, `kegs`, `fruit`, `empty`).

### 26. Bicycle (and vendor bikes)

**Looks like [est]:**
- Heavy roadster bicycles (black, rod brakes, a rear carrier) are uncommon in central Lagos but present in `sprawl` and `waterfront` paths.
- Vendor bikes: an ice-cream bike with a front or rear cool box (white/blue box with a bell or horn), a bread seller with a box on the carrier, a newspaper vendor.
- Children's bikes in estates.

**Kit parts:** `roadster` 1.75 m long, 28-inch wheels (0.71 m), a carrier rack; `cool_box` 0.6×0.4×0.45 m (white `#F2F2EE` with a coloured band and an umbrella); `bread_box` 0.6×0.4×0.4 m.

**Colours [est]:** Black `#1A1A1A`, rust; cool box white with a red/blue band (invent brand).

**SELECT BY:** `sprawl`, `waterfront` landward paths, `elite` estates (kids, ice-cream vendors). Very low on main roads.

**Gidi mapping:** `veh.bicycle`, `veh.bike_vendor_ice`, `veh.bike_vendor_bread`.

### 27. Water vendor cart (mai ruwa / "meruwa") and shoulder yoke

**Looks like:**
- Water sellers (Hausa "mai ruwa", water seller) push carts loaded with **up to 14 yellow 25-litre kegs** [src 34]; reports elsewhere put typical carts at 10-14 jerrycans of 20-25 L [src 35, 36].
- Others carry water on a **shoulder yoke ("garuwa")**: a stick across the shoulders with a rope from each end to a cylindrical metal bucket or can [src 34].
- Sellers buy from households with boreholes, or at car washes, and resell door to door [src 34].
- Vendors are typically young men in T-shirts and shorts or trousers, slippers [src 34].

**Kit parts:**
- `water_cart`: a steel-tube cart, deck 1.6×1.0 m at 0.7 m, two wheels (car or wheelbarrow-type 0.5-0.6 m diameter), long handles 1.0 m; kegs in 2 layers (7+7) tied with rubber straps cut from inner tubes.
- `keg_25`: a 25 L jerrycan, about 0.38×0.25×0.45 m high, screw cap and a moulded handle [est].
- `garuwa_yoke`: a 1.4-1.6 m wooden stick, 2 ropes, 2 cylindrical metal cans 0.3 m diameter × 0.4 m (oil-tin type), galvanised `#9EA3A6` or rusty.

**Dimensions [est]:** Cart footprint 2.4×1.2 m with handles, loaded height 1.2 m.

**Colours:** Kegs yellow `#E0B020` [src 34], faded `#D8BC5A`, grimy `#B8983A`; some white or blue kegs (10%). Cart frame black or rusty. Rubber straps black.

**Condition:** `worn`/`battered`; kegs scuffed, some with green algae inside visible through the translucent plastic `#7A8A3A`.

**Occupants:** 1 pusher (sometimes 2).

**Props and life:** A cart parked at a gate with kegs being handed in; a queue at a borehole tap (a standpipe with a padlocked tap and a meter) [est]; wet ground and a pool.

**SELECT BY:** `dense_mainland` (high), `sprawl` (high where no mains), `waterfront` landward edge, `old_island` back lanes. Not in `elite` (water tankers instead).

**Gidi mapping:** `cart.water`, `prop.keg_25`, `prop.yoke_garuwa`, `prop.borehole_tap`.

---

## 6. Water vehicles (lagoon, creeks, port)

Context: the Lagos Lagoon has around 2,200 boats in commercial use, and officials say most are not seaworthy [src 37]. Paddle canoes are the main transport in stilt settlements [src 38]. A state boatyard has been building 40-passenger ferries [src 39, 37]. This section rests partly on West African canoe data from Ghana (FAO) [src 40], adapted to Lagos.

### 28. Dugout paddle canoe

**Looks like:**
- A carved single-log hull, long and narrow, with sharp raised ends, low freeboard, and a flat-ish bottom. Paddled from the stern or standing up, sometimes poled in shallow water.
- Children as young as five or six paddle canoes in the canals [src 38].
- The hull is dark wet timber, often patched with tin plates and nails, tarred seams, and a bailing bowl inside.

**Kit parts:** `hull_dugout` (lofted log hull with a 0.1-0.2 m sheer rise at each end), `thwarts` 1-2 cross planks, `paddle` (a 1.4-1.6 m paddle with a leaf-shaped blade 0.15 m wide), `pole` (3-4 m bamboo), `bailer` (a cut plastic bottle or enamel bowl).

**Dimensions:** Small one-person canoes 4-5 m × 0.40-0.50 m; medium 6-11 m × 0.70-1.0 m [src 40]. Freeboard 0.15-0.30 m loaded [est]. Hull depth 0.35-0.5 m [est].

**Colours [est]:** Wet dark timber `#3E2E22`, dry `#6A5440`, tarred seams `#141210`; some painted: a band of blue `#2F5FA8`, green, or red near the gunwale, with a name painted on the bow.

**Condition:** `worn` (patched); `wreck` = half-sunk canoes in shallows and under houses.

**Occupants:** 1-4; loads of firewood, plastic water kegs, sacks of charcoal, fish baskets.

**SELECT BY:** `waterfront` canals (dominant), lagoon edges; rarely beyond 300 m from shore.

**Gidi mapping:** `boat.dugout` (sizes `S`, `M`).

### 29. Plank canoe with outboard (fishing and transport)

**Looks like:** A larger plank-built canoe with a wide beam, raised bow, a transom or mount for an outboard (15-40 hp), and a small roof of tarp or corrugated sheet on poles on some. Fishermen cast nets from them; others run cargo and people to outlying communities [src 38, est]. Some carry outboards moored ready for long trips [src 38].

**Kit parts:** `hull_plank` (planked hull with visible strakes and ribs), `outboard` (a 0.5×0.35×1.1 m engine, white/black/grey cowl), `canopy` (4 posts + tarp or zinc), `nets` (heap of net with floats), `fuel_keg`.

**Dimensions:** Large West African canoes reach 12-18 m × 1.3-1.8 m [src 40]; lagoon transport canoes 8-14 × 1.2-1.6 m [est].

**Colours [est]:** Painted hulls common: white `#EDEDE8`, blue `#2F5FA8`, green `#2E8B3A`, yellow `#F0C419`, red `#C0262D` bands; painted names and slogans on the bow (Gidi originals); weathered paint.

**Occupants:** 2-6 fishermen; 10-20 passengers on transport runs (with orange life jackets on some) [est].

**SELECT BY:** `waterfront` (open lagoon), sand landings, fish markets, jetties in `waterfront`/`old_island`.

**Gidi mapping:** `boat.plank_outboard` (roles `fishing`, `cargo`, `passenger`).

### 30. Trader canoe (floating shop)

**Looks like:** A small dugout or plank canoe paddled by a woman (often with a child), loaded with goods for sale: food, water, household goods, sweets, biscuits, bread [src 38]. Some carry a stove and cooking pots to serve hot food [src 38]. A wide umbrella or a raffia hat for shade.

**Kit parts:** `boat.dugout` M + `goods_load` (enamel basins, a stove, coolers, bread trays, sachet-water bags) + `umbrella` (1.8 m, bright stripes).

**Dimensions:** 4-6×0.6-0.8 m [est].

**Colours:** Bright goods against dark hull: enamel basins (red, blue, floral), coolers (blue `#2F5FA8`, red), umbrellas (striped).

**SELECT BY:** `waterfront` canals, near stilt houses (1 per 30-60 m of canal by day [est]).

**Gidi mapping:** `boat.trader`.

### 31. Sand canoe and sand dredger

**Looks like [est; sources sparse]:**
- **Manual sand mining:** divers dive from big wooden canoes with buckets and fill the canoe with wet sand until it sits almost awash (freeboard 0.05-0.10 m). The canoes are paddled or motored to a shore "sand landing" where tippers load (§12).
- **Mechanical dredgers:** a steel pontoon with a crane frame or a pump and a floating pipeline (a line of pipes on drum floats) running to a shore stockpile.

**Kit parts:** `hull_plank` large (12-18 m) + `sand_load` (mounded wet sand `#A8946A`); `dredger_pontoon` 20-30×6-8 m, a cabin, an A-frame, a pump unit, rusty steel `#6B3A22` with yellow `#E8B21C` machinery; `pipeline` (0.5 m pipes on 1 m drum floats, 100-500 m long).

**SELECT BY:** `waterfront` lagoon shores near `sprawl`/`dense_mainland` sand landings; next to a beach of sand heaps with tippers queuing.

**Gidi mapping:** `boat.sand_canoe`, `boat.dredger`, `prop.pipeline_float`, `prop.sand_landing`.

### 32. Wooden passenger ferry boat (commuter)

**Looks like [est]:** A long planked wooden boat with a pointed bow, a roof of plywood or fibreglass on posts with tarpaulin side flaps, rows of wooden benches across, and one or two big outboards on the stern. Life jackets in orange piled or worn (rules require them). Hull painted in bright bands with an operator name (invent). Before the 2010s, vessel limits were around 20 passengers; newer state-built boats carry 40 [src 39].

**Kit parts:** `hull` 12-16×2.4-2.8 m, `canopy_roof` (flat with a slight crown) on 8-12 posts, `benches` 8-12 rows, `outboards` 1-2 × 115-200 hp, `side_flaps` tarps (rolled or down), `life_jackets` (orange piles), `name_board`.

**Dimensions [est]:** 12-16 m long, 2.4-2.8 m beam, 2.2 m from waterline to roof.

**Colours [est]:** White `#EDEDE8` or yellow `#F0C419` hull with a blue `#2F5FA8` or green stripe; roof blue tarp; life jackets `#FF6A13`.

**Condition:** `worn`/`battered`; many of the lagoon fleet are considered not seaworthy [src 37].

**Occupants:** 20-40 + a pilot + a "conductor" at the bow.

**SELECT BY:** Jetties in `waterfront`, `old_island`, `sprawl` lagoon towns (Ikorodu-, Badore-type), and across to the island.

**Gidi mapping:** `boat.ferry_wood`, `prop.jetty`.

### 33. Fibreglass speedboat / water taxi

**Looks like:** A modern fibreglass hull with a deep-V bow, a small console or a full canopy, 2-4 rows of padded seats, twin outboards, and a white hull with a coloured stripe. The state added high-capacity speedboats to its ferry fleet [src 41]. Private ones serve `elite` waterfront homes, beach resorts and the oil-and-gas industry [est].

**Kit parts:** `hull_frp` 8-12×2.4-2.8 m, `console` or `cabin_canopy` (a fibreglass hard top), `seats` padded, `outboards` 2 × 150-250 hp (white or black), `bow_rail` stainless, `fenders`.

**Dimensions [est]:** 8-12 m × 2.4-2.8 m; hard top at 1.8-2.0 m above the waterline.

**Colours [est]:** White `#F4F4F2` hull; stripe blue `#1E4FB4`, red, yellow; seats cream or blue; stainless rails `#C9CDD0`.

**Occupants:** 6-24 [est].

**SELECT BY:** `elite` waterfront (marinas, private jetties), state jetties, resort routes to the sea.

**Gidi mapping:** `boat.speed` (`private`, `public`).

### 34. State ferry / catamaran

**Looks like:** Larger enclosed passenger vessels: a hull (mono or catamaran) with a full cabin of windows, a wheelhouse up front, and a deck rail; 40-passenger and larger [src 39, 37]. Departure from big public jetties with ticket halls.

**Kit parts:** `hull_cat` or `hull_mono` 15-25 m, `cabin` with a window band, `wheelhouse`, `deck_rail`, `boarding_ramp`.

**Dimensions [est]:** 15-25×4.5-6×4 m.

**Colours (Gidi invents) [est]:** White hull and cabin; the transit-authority accent colour band; tinted windows.

**SELECT BY:** Major jetties in `old_island`, `civic`, `elite`, `sprawl` lagoon towns.

**Gidi mapping:** `boat.ferry_state`, `prop.terminal_jetty`.

### 35. Log raft (sawmill)

**Looks like:**
- Logs floated from the delta forests are lashed into **rafts** with wires and "timber dogs" (iron staples), and moored on the water beside the sawmill waiting to be sold [src 42, 43].
- "Many hundreds" of rafts can lie at the sawmill under the bridge [src 44].
- Men walk on the logs with poles and machetes; small canoes thread between rafts.

**Kit parts:** `log` (0.5-1.2 m diameter, 6-12 m long, bark-on, dark brown `#4A3628`, the cut ends paler `#B8946A`), `raft` (10-40 logs side by side in 1-3 rows, wire lashings, staple dogs), `pole` 4 m.

**Dimensions [est]:** A raft 15-30 m long × 4-8 m wide; logs float with 20-40% of their diameter above water.

**SELECT BY:** `waterfront` sawmill district (Okobaba-type) only; 20-200 rafts.

**Gidi mapping:** `boat.lograft`, `prop.log`.

### 36. Barges, tugs, pontoons and wrecks

**Looks like [est]:** Steel deck barges (flat, rusty, with bollards) moored at port quays and lagoon edges; small tugs (a high bow, a wheelhouse, tyre fenders hung along the sides); floating pontoon jetties; and many **half-sunk wrecks** (boats and small ships) along the port and lagoon shores.

**Kit parts:** `barge` 30-60×9-12 m, 2.5 m depth, deck cargo (containers, sand, pipes); `tug` 20-25×7 m, wheelhouse 6 m above water, black hull `#1A1A1A`, red boot top `#A8261E`, white house; `pontoon` 10×4 m with rails; `wreck` (a listing hull, rust `#6B3A22`, a mast at an angle).

**SELECT BY:** `port` (high), lagoon edges near `port`/`waterfront`.

**Gidi mapping:** `boat.barge`, `boat.tug`, `boat.pontoon`, `boat.wreck`.

### 37. Police / navy patrol boat and water ambulance

**Looks like [est]:** Fast fibreglass boats with a hard top, a machine-gun mount on police/navy ones ("gunboats" were donated to the Lagos police in 2015 [src 45]), grey or white with blue/red bands, and a light bar. The state runs water ambulances for riverine communities [src 30].

**Kit parts:** `boat.speed` + `gun_mount` + `lightbar` + `band`.

**Colours [est]:** Navy grey `#5A6670`; police white with blue; ambulance white with red/green band.

**SELECT BY:** `port`, jetties in `civic`/`elite`, rare on canals.

**Gidi mapping:** `boat.patrol`, `boat.ambulance`.

---

## 7. Occupants and loads (cross-reference)

| Vehicle | Driver | Crew | Passengers typical / max | Common loads |
|---|---|---|---|---|
| Keke | 1 | 0 | 3 / 5-6 | Bags, gas cylinder, chickens |
| Okada | 1 | 0 | 1 / 2-3 | Gas, kegs, sacks, long rods, plywood |
| Danfo | 1 | 1 conductor | 14-18 / 20 | Roof: sacks, chairs, mattresses |
| Korope | 1 | 1 | 8-12 / 14 | Small roof load |
| High-roof minibus | 1 | 0-1 | 14-18 | Roof pile under tarp (interstate) |
| Molue | 1 | 1-2 | 50 / 80 | Hawkers, preacher |
| BRT 12 m | 1 | 0 | 60-100 | — |
| Coaster | 1 | 0-1 | 26-30 | — |
| Coach | 1-2 | 1 | 45-59 | Belly luggage |
| Car | 1 | 0 | 0-4 | Roof rack rare; boot open with goods |
| Tipper | 1 | 1-2 boys | 0 | Sand, laterite, granite |
| Tanker / trailer | 1 | 1 boy | 0 | Fuel / container |
| Wooden lorry | 1 | 2 boys | 0-10 on top | Produce, cattle, grain |
| Police pickup | 1 | 1 | 3-6 officers in the bed | Rifles |
| Truck pusher | 1-2 pushers | 0 | 0 | Anything |
| Water cart | 1 | 0 | 0 | 14 kegs |
| Dugout | 1 | 0 | 0-3 | Firewood, kegs, fish |
| Passenger boat | 1 pilot | 1 | 20-40 | Life jackets |

---

## 8. Behaviour and placement (only what affects modelling)

### 8.1 Bus stops (informal)
- A bus stop is a stretch of 30-80 m of kerb lane where danfos, koropes and BRT feeders stop **in the lane**, usually 2-3 abreast [street-research]. Model: a "stop zone" spline that spawns 3-10 stopped danfos at random angles (0-15° to the kerb), with conductors, agberos and hawkers.
- A keke/okada rank sits 10-50 m past the stop, on the side street mouth.
- Hawkers walk between the stopped buses selling drinks, snacks, phone accessories.
- A few danfos have their sliding door facing the stop and a crowd leaning in.

### 8.2 Motor parks ("garages")
- A walled or open yard (0.3-3 ha) of laterite or broken concrete, with parked vehicles in 3-8 rows nose to the loading lane; a loading bay where the next vehicle fills; union offices in containers or block huts; canteens; toilets; mechanics; vulcanizers (tyre repairers); a mosque or church shed.
- Danfo parks: 30-200 vehicles. Interstate parks: 10-40 coaches + 20-100 high-roof vans.
- "Super stations" / interchanges in the big mainland hubs mix all modes [src 8].
- Model as a `prop.motor_park` with a seeded fill of 50-90% occupancy by day, 90-100% by night (vehicles sleep there).

### 8.3 Double parking and kerb occupation
- `old_island` and market streets: cars parked on both sides, half on the walkway, plus a second row in the lane on the busier side; delivery trucks unloading in the lane; push-carts squeezed between.
- `elite`: parking on driveways and in compounds; rows of cars outside banks, malls and churches on Sundays; drivers waiting in parked cars.
- `port`: trailers and tankers parked on both shoulders and the slow lane, in queues 1-10 km [street-research].

### 8.4 Breakdowns and derelicts
- Breakdown frequency on main roads in `dense_mainland`/`port`: one stopped vehicle per 300-600 m at any time [est]. Signs: a bonnet or engine lid up, a jack, branches or a tyre laid in the road behind as a warning, a mechanic under the vehicle.
- Trucks broken down on bridges and port roads are a known congestion cause [src 33].
- Derelicts: abandoned hulks (cars, danfos, trailers, tankers) about 1 per 300 m in `dense_mainland`/`sprawl` [street-research]; impound yards and mechanic villages with 20-500 hulks.

### 8.5 Night
- Many vehicles run with one headlamp or none; tankers and trailers are lit with amber clearance lamps (or a hurricane lantern hung at the rear on old lorries) [est].
- Traffic lights are absent or off at many junctions; headlight glare and brake-light rivers on expressways.
- Danfos and kekes thin out after 22:00; trucks increase (port movements are often at night) [est].
- Checkpoints appear at night.

### 8.6 Traffic mix by district and road class [est]

Shares of moving vehicles (excluding pedestrians and parked).

| | Danfo + korope | Keke | Okada | Cars + taxis | BRT / buses / coasters | Trucks (tanker, trailer, tipper, lorry, light) | Carts (on road) |
|---|---|---|---|---|---|---|---|
| `dense_mainland` main | 30 | 5 | 5 | 40 | 5 | 12 | 3 |
| `dense_mainland` street | 10 | 25 | 25 | 30 | 0 | 5 | 5 |
| `old_island` main | 20 | 0 | 0 | 55 | 5 | 10 | 10 |
| `old_island` lane | 0 | 5 | 5 | 40 | 0 | 10 | 40 |
| `sprawl` main | 25 | 15 | 15 | 30 | 3 | 10 | 2 |
| `sprawl` street | 5 | 30 | 30 | 30 | 0 | 3 | 2 |
| `elite` main | 5 | 0 | 2 | 80 | 5 | 8 | 0 |
| `elite` street | 0 | 0 | 3 (dispatch) | 92 | 0 | 5 | 0 |
| `civic` main | 15 | 0 | 2 | 60 | 10 | 10 | 3 |
| `port` main | 10 | 0 | 2 | 20 | 3 | 65 | 0 |
| `waterfront` edge street | 5 | 20 | 30 | 20 | 0 | 10 | 15 |
| expressway | 15 | 0 | 0 | 50 | 5 | 30 | 0 |

### 8.7 Age and condition dial
- `condition = clamp(0.25 + 0.6*wealth + noise(±0.2))`. Map: >0.8 `new`, 0.5-0.8 `worn`, 0.2-0.5 `battered`, <0.2 `wreck` (only for parked props).
- Commercial vehicles (danfo, korope, keke, okada, trucks) get `condition -= 0.2`.
- `elite` private cars get `condition += 0.2`.

---

## 9. Gidi original slogans (for vehicle text generators)

Patterns observed: faith, patience, envy, destiny, humour, gratitude, a mother's prayers, football loyalty. Never copy real phrases. Seed list (all invented for Gidi):

- "Still Standing By Grace"
- "Patience Pays The Fare"
- "No Shaking, Na Steady Wheel"
- "Mama's Prayer Na My Airbag"
- "Who Knows Tomorrow?"
- "Slow Road, Sure Arrival"
- "Eyes On The Road, Mind On God"
- "Envy Me In Silence"
- "Gidi No Dey Sleep"
- "Iron Sharpens Iron"
- "From Ajo To Owner" (invent district names when used)
- "Small Small, Big Big"
- "Destiny Has No Holiday"
- "Thank You Lord, Next Stop"
- "Hustle Is Not A Crime"
- "Peace Be Upon This Bus"

Placement: windscreen top strip (danfo, keke, lorry headboard), rear window or rear panel (all), mudflaps (okada, trucks), bow of boats. Typefaces: block caps, stencil, hand-painted script. Colours: white or gold `#D4A62A` on black, black on yellow, red outline on white.

---

## 10. Sources

Numbered for [src N] tags. "street-research" = `/Users/Star/gidi/docs/look/research-street.md` and its sources.

1. Africa Check, "Commercial bus ban in Lagos affects Lekki-Epe axis and not entire state": https://africacheck.org/fact-checks/meta-programme-fact-checks/commercial-bus-ban-lagos-nigeria-affects-lekki-epe-axis-and (also https://allafrica.com/stories/202407300159.html)
2. BusinessDay, "LASG defends ban on korope operators after Lekki-Epe protest": https://businessday.ng/transport/article/lasg-defends-ban-on-korope-operators-after-lekki-epe-protest/
3. Discover Lagos, "Lagos government to phase out korope minibuses from major highways": https://www.discoverlagos.ng/post/lagos-government-to-phase-out-korope-minibuses-from-major-highways
4. Bajaj RE brochure (keke dimensions, tyres 4.00-8): https://bajajauto.com/en-tz/-/media/globalbajajauto/common-media/brochure/3wheelers/re-cng-n-t.pdf ; 91Trucks RE listing: https://91trucks.com/auto-rickshaws/bajaj/re-petrol
5. Bajaj Boxer BM150 spec page (okada dimensions, tyres): https://www.bajajauto.com/en-cr/bikes/boxer-bm150 ; https://rwanda.globalbajaj.com/en/Brands/Boxer/Boxer-BM150
6. Wikipedia, "Danfo": https://en.wikipedia.org/wiki/Danfo ; Wiktionary "danfo": https://en.wiktionary.com/wiki/danfo
7. The Autopian, "Why Nigeria's danfo bus drivers might be the craziest...": https://theautopian.com/why-nigerias-danfo-bus-drivers-might-be-the-craziest-and-most-skilled-drivers-on-the-planet
8. MIT Atlas of Popular Transport, "From Danfo to Data: Lagos": https://atlasofpopulartransport.mit.edu/lagos
9. Guardian Nigeria on the 2020 tricycle/okada restriction: https://guardian.ng/opinion/editorial/tricycle-and-motorbikes-painful-but-necessary-ban/ ; https://guardian.ng/news/one-month-after-tricyclists-motorcyclists-back-on-lagos-roads/ ; route lists: https://thecondia.com/full-list-of-roads-local-government-areas-keke-okada-banned-lagos/
10. Gazette Nigeria / Guardian / LAMATA on the Lekki-Epe bus reform (blue-white regulated buses, Dec 2025): https://gazettengr.com/sanwo-olus-government-clarifies-danfo-ban-in-lagos/ ; https://guardian.ng/news/lasg-commits-to-bus-reform-initiative-on-lekki-epe-corridor/ ; https://www.lamata-ng.com/?p=11298
11. Ikeja Record, "Danfo tales: surviving Lagos as a bus driver" (danfo 14-seater, korope microvan): https://ikejarecord.com/danfo-tales-surviving-lagos-as-a-bus-driver ; https://ikejarecord.com/lagos-govt-to-ban-unregistered-danfo-korope-buses-on-lekki-epe-corridor
12. MIT Atlas (as 8), korope description.
13. Daily Trust, "In Lagos, last days of the molue": https://dailytrust.com/in-lagos-last-days-of-the-molue/
14. TheCable Lifestyle on molue capacity and condition: https://lifestyle.thecable.ng/?p=161384
15. Brittle Paper, "Lagos Moves" commentary (molue crowding): https://brittlepaper.com/2017/01/lagos-moves-dan-commentary/
16. LAMATA bus services (BRT Lite, high-floor buses, 220 buses, 22 km): https://www.lamata-ng.com/bus-services/
17. Automotive World on 250 Scania/Marcopolo buses for Lagos: https://www.automotiveworld.com/?p=285188
18. Shipping Position on LAMATA bus colours: https://shippingposition.com.ng/?p=48906
19. Wikipedia, "Transport in Lagos": https://en.wikipedia.org/wiki/Transport_in_Lagos
20. BusinessDay on Marcopolo Paradiso 1350 (59 seats) in Nigeria: https://businessday.ng/?p=313442
21. TheCable, "Lagos says interstate vehicles can no longer ply Ikorodu road": https://thecable.ng/lagos-says-interstate-vehicles-can-no-longer-ply-ikorodu-road ; Daily Trust on sealed offices: https://www.dailytrust.com.ng/lagos-seals-off-chisco-ifex-guo-other-transporters-offices.html
22. AFK Travel, "Getting around Lagos" (yellow cabs with stripes): https://afktravel.com/140/getting-around-lagos-nigeria/ ; NewsCentral on yellow cabs: https://newscentraltv.com/?p=26455 ; Wikipedia "Taxi livery": https://en.wikipedia.org/wiki/Taxi_livery
23. ThisDay, "CFAO Nigeria now official co-distributor of Sinotruk Howo": https://www.thisdaylive.com/2023/03/25/cfao-nigeria-now-official-co-distributor-of-sinotruk-howo/
24. Truck1 listing, used tipper for sale in Lagos: https://www.truck1.ke/trucks/tippers/sinotruk-used-howo-430hp-dump-truck-for-sale-in-nigeria-lagos-a10388708.html ; BusinessDay on Chinese trucks: https://businessday.ng/?p=17174
25. Mammy wagon / bolekaja: https://www.rrncommunity.org/items/14664 ; https://mmmworldwide.org/blogs/take-it-easy-joe/ ; https://www.easaonline.org/downloads/networks/media/43c.pdf ; https://digital.lib.buffalo.edu/items/show/89770
26. Guardian, "LAWMA evacuates 418,500 tonnes of waste in May": https://guardian.ng/news/nigeria/metro/lawma-evacuates-418500-tonnes-of-waste-in-may-ramps-up-sanitation-drive/
27. VON, "Lagos to deploy 220 new compactor trucks": https://von.gov.ng/waste-management-lagos-to-deploy-220-new-compactor-trucks/ ; ThisDay 2021: https://thisdaylive.com/index.php/2021/08/17/sanwo-olu-charges-lagosians-on-waste-bills
28. Guardian, "Ambode donates patrol helicopters, gun boats, vans to police": https://m.guardian.ng/news/ambode-donates-patrol-helicopters-gun-boats-vans-to-police/
29. Lagos Police Command service page (patrol vans): https://lagos.npf.gov.ng/service/details/16 ; BusinessDay on RRS: https://businessday.ng/analysis/article/lagos-rapid-response-squad-and-public-security/
30. Radio Nigeria Lagos, LASAMBUS expansion (36 ambulances, 4 bases, water ambulances): https://radionigerialagos.gov.ng/?p=26853
31. Zikoko, "5 Nigerians share their most memorable experiences with LASTMA": https://www.zikoko.com/general/5-nigerians-share-their-most-memorable-experiences-with-lastma/
32. Headteacher.ng lesson note on FRSC and LASTMA: https://www.headteacher.ng/lesson-plan-on-identification-of-security-agencies-frsc-and-lastma-basic-2/
33. Shipping Position, "LASTMA urges maritime truck drivers to tackle breakdowns": https://shippingposition.com.ng/lastma-urges-maritime-truck-drivers-to-tackle-breakdowns/
34. BusinessDay, "'Meruwas' filling the gap...": https://archive.businessday.ng/features/article/meruwas-filling-gap-helping-clean-water-supply-huge-health-cost/
35. Pulitzer Center on mai ruwa carts: https://pulitzercenter.org/node/25155
36. BBC via WASHplus, "Nigeria: the water vendors": https://washplusblog.fhi360.org/urbanhealthupdates/2009/02/nigeria-the-water-vendors-bbc-news/index.html ; Zikoko water seller: https://www.zikoko.com/money/naira-life/the-water-seller-carting-in-₦82k-every-month/
37. Guardian via PressReader, "Lagos, Caverton target capital flight reduction with local boat production" (2,200 boats, 78% not seaworthy, 40-seat ferries): https://www.pressreader.com/nigeria/the-guardian-nigeria/20240328/281857238542326
38. Makoko canoes: https://www.amusingplanet.com/2014/04/makoko-floating-slum-in-nigeria.html ; https://kolaking.substack.com/p/women-fishers-in-makoko-lagoss-floating ; https://ripplesnigeria.com/living-on-stilts-75-unforgettable-images-of-makoko-will-it-survive-sanwo-olus-smart-city-plan ; https://newscut.mprnews.org/2013/09/photos-inside-makoko-nigerias-venice/index.html
39. Maritime Review, "Ferry fleet launched" (15 × 40-passenger ferries, previous limit 20): https://maritimereview.co.za/Articles/ArtMID/397/ArticleID/338/Ferry-fleet-launched
40. FAO, Ghana canoe sizes: https://www.fao.org/4/R0395E/R0395E02.htm ; FishConsult dugouts: https://fishconsult.org/?p=11808
41. ITS Nigeria / BusinessDay on LAGFERRY high-capacity speedboats: https://www.itsnigeria.org/?p=3927 ; https://businessday.ng/?p=555199
42. Guardian, "The wood merchants" (rafts with wires and timber dogs): https://guardian.ng/features/the-wood-merchants/
43. Eyes of a Lagos Boy, "From raft to furniture": https://eyesofalagosboy.com/2023/07/18/photo-of-the-week-from-raft-to-furniture/
44. Sebastian Barros, "Sawmills" (Ebute Metta log rafts): https://elephant.art/sebastian-barros-sawmills
45. Guardian (as 28), gunboats donated to police.
46. Guardian on Okobaba relocation: https://guardian.ng/news/sanwo-olu-sets-december-deadline-for-relocation-of-oko-baba-sawmill-to-agbowa/
47. Interstate parks guide: https://intercity.ng/blog/motor-parks-in-lagos-and-destinations
48. Guardian, "Danfo... the naked realities of Nigerian automobiles": https://guardian.ng/life/danfo-the-naked-realities-of-nigerian-automobiles/ ; BellaNaija (danfo base vans): https://www.bellanaija.com/2022/01/bird-lagos-danfo-driver/
