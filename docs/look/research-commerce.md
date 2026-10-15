# Gidi commerce catalogue: markets, shops, commerce and industry

Purpose: specs for the seeded Blender kit. This builds on `docs/look/research-buildings.md` §6 (shop bays, container shop, kiosk, stall, plaza) and `docs/look/research-street.md` §6 (stall goods, umbrellas, chairs, generators, water tanks, night light). Those base specs are **not repeated**. Where they apply, this file refers to them as `B§6.x` and `S§6.x`.

Tags: **[src]** means the figure comes from a source listed at the end. **[est]** means an estimate from photos, general knowledge or engineering norms.

Rule zero: every brand, name and livery below is generic. Real places appear only as examples of a pattern.

---

## 0. Summary table

| # | Item | Gidi census name(s) | Main district character | Footprint / height [est] | Priority |
|---|---|---|---|---|---|
| 1 | Shared market kit (stall modules, lanes, sheds, gates) | all markets | all | stall 2×2 m; shed bay 2×2.5 m | **core** |
| 2 | Car-parts market | Ladi Lane Parts Market | dense mainland | 4–12 ha; lock-ups 3×4 m | high |
| 3 | Electronics market | Alade Electronics Market | dense mainland / Ojo-type | 10–200 ha; lock-ups 3×3 m | high |
| 4 | Half-built wholesale plazas | Fair Wholesale Plazas | Ojo/Trade-Fair dense mainland | 30×60 m blocks, 2–5 st | high |
| 5 | Produce / food wholesale market | Mile Market | Kosofe dense mainland | 20–40 ha; lorry bays | high |
| 6 | Cloth market | Cloth Market | old island | lanes 2–3 m; plazas 3–6 st | high |
| 7 | Grain yard | Daleko Grain Yard | dense mainland | 2–5 ha; sack warehouses | med |
| 8 | Plank / timber market on a canal | Boundary Plank Market | waterfront | 200–600 m canal edge | med |
| 9 | Livestock market and abattoir | Oko Cattle Market & Abattoir, pen | sprawl edge | 10–20 ha; pens 10×20 m | med |
| 10 | Fish market at a jetty with smoking racks | (fish market) | waterfront / old town | jetty 30–80 m | med |
| 11 | Roundabout market | Ikotun-style Roundabout Market | sprawl / dense mainland | ring 60–120 m dia | med |
| 12 | Periodic market days | (market-day flag) | old towns, sprawl | n/a (behaviour) | med |
| 13 | Phone malls / converted houses | Gadget Village | civic-edge mainland (Ikeja-type) | 15×30 m plot, 3–4 st | high |
| 14 | Shopping plaza (generic) | plaza | dense mainland, sprawl | 20×40 m, 2–4 st | high |
| 15 | Container shops and container jail | Container Court | all mainland, port | 6.06×2.44×2.59 m | high |
| 16 | Kiosk types | kiosk | all | 1.2–2.4 m boxes | **core** |
| 17 | Print shops and kiosks on house fronts | Pedro Print Row | dense mainland (Shomolu-type) | 2×2 m bolt-ons | med |
| 18 | Bakeries | Ayo Bakery Row | sprawl (Agege-type) | 8×15 m shed | med |
| 19 | Sawmill | Okobaba Sawmill, saw shed, sawdust | waterfront | 6–15 ha | med |
| 20 | Scrap yards | scrap yard | dense mainland, port | 0.2–3 ha | med |
| 21 | Mechanic villages and vulcanisers | mechanic village, vulcaniser | all mainland | 0.5–3 ha; 1×1 m roadside | high |
| 22 | Warehouses and industrial estates | warehouse, estate | port, Ikeja/Ilupeju-type | 30×60 m sheds | high |
| 23 | Factories ("works") | works | industrial | 60×120 m | med |
| 24 | Bank branches | bank | all except slum | 15×25 m, 2–3 st | high |
| 25 | Bank towers on a waterfront | Bank Row, bank tower | old island / elite | 20–30 st, 80–125 m | med |
| 26 | Office blocks | office | civic, elite, old island | 4–12 st | med |
| 27 | Fuel stations and black-market fuel | fuel station | all main roads | plot 50×50 m | **core** |
| 28 | Clearing-agent kiosks | Collector Row | port | 2.4×6 m units | med |
| 29 | Tank farm with pipe racks | tank farm | port | tanks Ø20–40 m | med |
| 30 | Refinery towers and flare stack | refinery | port / far sprawl | towers 40–80 m; flare 80–120 m | low |
| 31 | Landfill with smoke and scavengers | landfill | sprawl edge | 40 ha, mound 15–30 m | med |
| 32 | Colonial brick waterworks (1915) | waterworks | old town / sprawl | 12×30 m hall | low (landmark) |
| 33 | Pipeline corridor tapped at night | pipeline corridor | sprawl / waterfront edge | 15–30 m wide strip | low |
| 34 | Market signage, generators, night lighting (market-specific add-ons) | all | all | n/a | core |

---

## 1. Shared market kit (used by items 2–12)

**Looks like:** Markets are built from a few repeated modules. These are rusty zinc lean-tos on timber poles, concrete-block lock-up rows with steel doors, long shed roofs over concrete slab tables, and tarp-and-umbrella fillers. Lanes are narrow and wet, and the ground is mud or broken concrete with an open drain. Every free metre gets filled, and goods spill 0.5–1.5 m into the lane.

**Kit parts:**
- `stall_open`: 4 timber poles 75×75 mm, 2.0–2.4 m high. Raised plank table 1.5–2.0 × 0.9 m at 0.8 m. Mono-pitch zinc sheet roof 2.2×2.4 m, sloped 5–10°, overhanging 0.3 m [est].
- `stall_shed_bay`: one bay of a government/LGA market shed. RC or steel columns at 4–6 m centres. Continuous double-pitch long-span roof with its ridge at 4.5–6 m. Concrete slab tables 2.0 × 1.2 m at 0.75 m, divided by 100 mm block upstands. Aisles 1.5–2.0 m [est].
- `lockup`: block cell 3.0 m wide × 3.0–4.0 m deep × 3.0 m clear, flat RC slab or mono-pitch roof. Front is a galvanised roller shutter or a 2-leaf steel door, with a padlock hasp at 0.3 m. Sold in rows of 6–40 back-to-back, so a double row is 7–8 m deep [est]. The ~8,400 lock-ups at Ikotun-type markets [src: Wikipedia Ikotun] give density: about 1 lock-up per 5–8 m² of market gross area [est].
- `lockup_spill`: a 0.6–1.2 m deep display zone in front of the shutter. It holds a goods-specific pile (see each market), a stool and a 2–3 m umbrella.
- `lane`: 1.2–3.0 m wide, a concrete or mud strip with a centre or side drain 0.3–0.5 m wide, covered with broken slabs or planks.
- `market_gate`: a rendered block arch 6–10 m wide × 5–7 m high with a painted name panel ("___ MARKET" in red/blue on white) and a steel swing gate or none. Two block pillars carry the market association's board [est].
- `association_office`: a 1–2 storey block, 6×8 m, painted the association colours, with a flag pole and a notice board [est].
- `toilet_block`: a 4×6 m block with "PAY TOILET N__" painted, a water tank on a stand, and a queue [est].
- `loading_strip`: market-edge road with 2–4 lorries nose-in, wheelbarrows and push-carts (`truck_pusher`: timber flatbed 2.4×1.2 m on 2 car wheels, T-handle).

**Dimensions / colours / materials:**
- Zinc: new `#B9BEC2`, galvanised dull `#9EA3A6`, rust `#8A5A3A`, deep rust `#5E3A22`.
- Tarps: blue `#2F5FA8`, orange `#E8742A`, green `#3E8E4A`, striped "Ghana-must-go" check (red/blue/white).
- Lock-up shutters: galvanised, or painted blue `#2C5DA8`, green `#2E7D4F`, maroon `#7A2430`, cream `#E9DFC6`.
- Concrete `#9C978E`, wet `#6E6A63`. Market mud `#4A3B2C`.

**Variants (share of stall area) [est]:**
- Open stalls 40%, lock-ups 35%, formal shed bays 15%, ground-mat sellers 10%.
- A rich or newly rebuilt market shifts to 70% lock-ups and a plaza ring.

**Condition states:**
- *New/rebuilt:* painted lock-ups in one colour, numbered stencils ("B-114"), straight lanes, new zinc.
- *Worn:* mixed shutter colours, tarps tied under roofs, drains clogged.
- *Decayed:* collapsing roofs, sheets missing, ground slabs broken, refuse heaps 1–2 m high at lane ends.
- *Burnt (markets burn often):* blackened lock-up row, roofless, twisted sheets, with traders already back under tarps in front [est].
- *Demolished:* a rubble field with rebar and single remaining walls; traders on the road edge.

**Props and life:**
- *Day:* 1 trader per 2–4 m of lane edge, 1 porter per 20 m. Wheelbarrows and head-pans, plus a stream of buyers 0.5–1.5 persons/m² at peak [est]. Food sellers (rice, swallow, sachet water) walk through. Market levy collectors carry receipt books.
- *Night:* most markets close by 18:00–19:00. Shutters come down and padlocks go on. Night guards (a hunter-type watchman with a bench and fire) take over. Produce and grain markets run lorry offloading all night under floodlights and generator light.

**SELECT BY:** `market_type` chooses the goods, the share of stalls and lock-ups, and which market-specific parts appear. `wealth` sets the share of lock-ups and the plaza ring. `condition` sets roof decay. `distance_to_main_road`: road-edge spill when < 30 m.

**Gidi mapping:** base for every market census item.

---

## 2. Car-parts market — "Ladi Lane Parts Market"

**Looks like:**
- Narrow streets of 1–3 storey shops, every frontage piled with used imported parts. Engines sit on the ground, gearboxes stack 3 high, bumpers lean in fans and doors hang on walls.
- The ground is black and glossy with spilt oil. Everything is a rust/grease palette lit by bright painted signs.
- Parts sit in stacks around the edges of the lots. A few yards hold whole "cut" car halves (front clips) imported for parts.
- Car dealers park rows of used cars along the edges [src: Wikipedia Ladipo]. The market runs on Ladi-type streets in a Mushin-type district [src].

**Kit parts:**
- `parts_lockup`: `lockup` with a 1–2 m spill apron and a wooden or steel rack 2.0 h × 1.5 w carrying headlamps, filters and belts.
- `engine_pile`: 3–8 engine blocks 0.7×0.6×0.7 m on pallets or tyres, with gearboxes 0.6×0.4×0.4 m [est].
- `bumper_fan`: 5–15 bumpers 1.8 m leaning against a wall at 70°, in mixed colours (silver, black, white, red).
- `door_wall`: car doors hung on nails 2 high, in mixed paints.
- `cut_clip`: car front halves 2.0×1.8×1.4 m in a stack 2–3 high in a yard [est].
- `tyre_stack`: towers of 6–12 tyres Ø0.6–0.7 m.
- `oil_ground` decal: black `#1A1714` with a sheen of roughness 0.2, and rainbow patches.
- `parts_shed`: a timber lean-to 3×6 m over the apron.

**Dimensions:** 4–12 ha [est]. Lock-ups 3×4 m. Street 4–6 m with 1–2 m spill each side, so 2–3 m of free lane. Plazas 2–3 storey with upper parts warehouses [est].

**Colours:** rust `#7B4A2C`, grease black `#1E1B18`, engine grey `#6B6E70`, cast aluminium `#A9ABA8`, signs yellow `#F2C200` on black, white on red `#C8282A`.

**Materials:** cast iron, aluminium, sheet steel, rubber, oily concrete.

**Variants:** used ("tokunbo") parts 70%, new boxed parts 20% (clean shelves, cartons, glass fronts), with 10% dealer car lots [est].

**Condition:** *worn* is the default. *Decayed* adds oil-flooded drains and a burnt corner. A *sealed* state (government closure for environmental breaches [src: New Telegraph]) shows shutters shut, red "SEALED BY ORDER" stencils and empty lanes.

**Props and life:** buyers with old parts in hand, mechanics test-fitting, boys carrying an engine on a pole between two. Danfo and pickup loading. Small generators at every 2nd shop. Night: shut, with only watchmen.

**SELECT BY:** `market_type=parts`, dense_mainland, near an expressway interchange. `wealth` low–mid. Pairs with item 21 (mechanic village) within 500 m.

**Gidi mapping:** Ladi Lane Parts Market.

---

## 3. Electronics market — "Alade Electronics Market"

**Looks like:**
- A city of lock-up rows and plazas covering many streets. Wholesale cartons are stacked to head height outside every shop: TVs, speakers, fridges, generators.
- Dense flex banners and painted fascia across every frontage. Small generators on old tyres hum at every 2–3 shops.
- Tall steel radio/telecom masts (guyed lattice) rise between the plazas, because each block has its own telecom base station and a shop "antenna" tradition.
- Lettered and numbered shop codes ("Shop A170") are painted on shutters [src: connectciti listing]. Size is quoted as 30,000+ shops [src: Culture Trip] and very large in area [src, approximate].

**Kit parts:**
- `elec_lockup`: 3.0×3.0 m [census spec] × 3.0 m, roller shutter, with a white tile floor visible. Glass display counter 1.2×0.5×1.0 m set at the opening.
- `carton_stack`: boxes in sizes TV 1.1×0.2×0.7, speaker 0.5×0.45×0.8, fridge 0.6×0.65×1.5. Brown kraft `#B08A5A` with a printed colour panel. Stacks 1.5–2.5 m high, 1–3 deep in front of the shutter.
- `gen_on_tyre`: small generator (S§6.4) set on a flat car tyre to damp vibration, with a red fuel can and an exhaust pointed at the lane.
- `radio_mast`: lattice mast 30–45 m, 0.6–1.2 m triangular section, red/white bands at 6 m intervals, guyed, or a self-support tower on the roof of a 3 storey plaza (15–25 m extra). Panel antennas and microwave dishes Ø0.6–1.2 m [est].
- `plaza_arcade`: see item 4/14.
- `repair_bench`: a table 1.2×0.6 m with a soldering station, opened TVs, an anglepoise lamp, under an umbrella.

**Dimensions:** lanes 2–4 m between rows [S§6.1]. Rows of 20–40 lock-ups. Plazas 2–4 storey.

**Colours:** cartons `#B08A5A`; banners in invented telecom yellow `#FFCC00`, red `#E2231A`, blue `#1F4FA0`; shutters galvanised; mast red `#D22B2B`/white.

**Variants:** wholesale white goods 30%, AV (TV/speakers) 30%, phones and accessories 20%, generators and power equipment 10%, repair 10% [est].

**Condition:** *new plaza blocks* (recently commissioned "modern complexes" [src: FMINO]). *Worn* (default). *Condemned* (buildings flagged "beyond redemption" [src: Wikipedia Alaba]) with red X stencils, "DEMOLISH" text and cracked columns. *Demolished* rubble.

**Props and life:** buyers arguing, touts at gates ("customer, what you want?"), push-carts with fridges, loaders, music blaring from test speakers. Night: closed. A few security lights and mast aviation lights (red `#FF2020` blink).

**SELECT BY:** `market_type=electronics`; dense_mainland (Ojo/Trade-Fair type); close to an expressway. Masts appear at density 1 per 100–150 m [est].

**Gidi mapping:** Alade Electronics Market (lock-up rows 3×3 m, generators on tyres, radio masts).

---

## 4. Half-built wholesale plazas — "Fair Wholesale Plazas"

**Looks like:**
- 2–5 storey RC frame blocks whose ground floor is fully trading while the upper floors are bare frames with rebar sticking out of the column heads.
- Each block is long (30–60 m), with a gallery corridor on each floor and stairs at the ends.
- Lower shops have painted shutters and banners. The upper floors are raw grey concrete with hollow-block infill on some bays only, and props and formwork still standing.
- Typical of trade-fair zones where plazas were built bay-by-bay as traders paid [est].

**Kit parts:**
- `plaza_frame`: columns 300×300 mm at 3.5–4 m centres, slab 150 mm, floor-to-floor 3.3–3.6 m, gallery 1.8–2.4 m deep with a 1.0 m parapet or nothing.
- `rebar_crown`: 4–8 bars 12–16 mm × 1.0–1.5 m up from each top column, bent and rusty `#6B3B22`.
- `bay_state`: per bay, one of: finished shop (shutter and sign), block infill only, open frame, timber props (eucalyptus poles Ø80 mm at 0.8 m grid).
- `stair_core`: open RC stair 1.2 m wide at the ends.
- `ground_ring`: kiosks and umbrellas around the base.

**Dimensions:** 30–60 × 15–25 m plan [est]. Shop bays 3×4 m.

**Colours:** raw concrete `#A39E95` → stained `#7C776F` with black streaks; block `#B6B1A6`; finished bay paint cream `#E9DFC6`/sky `#8EC1E5`.

**Variants (by storeys completed) [est]:** G only plus frame 1 floor 30%; G+1 finished, frame above 40%; G+2/3 finished, roof frame unfinished 20%; complete 10%.

**Condition:** *half-built* is the default. *Stalled* (5+ years): green algae, shrubs in slabs, rust running down, banners faded. *Abandoned:* squatters' tarps on upper floors, laundry.

**Props and life:** goods hoisted by rope, water tanks perched on unfinished slabs, "THIS PLAZA IS FOR ___ ASSOCIATION" boards, sand and gravel heaps at the base.

**SELECT BY:** `market_type=wholesale`, dense_mainland Ojo-type; `condition` half-built share ↑ when `wealth` mid. Storey count from `storeys` attribute, with finished floors = `storeys × rand(0.3–0.8)`.

**Gidi mapping:** Fair Wholesale Plazas.

---

## 5. Produce / food wholesale market — "Mile Market"

**Looks like:**
- A massive wet market at an expressway edge where long-distance lorries from the north arrive daily with tomatoes, peppers, onions, beans and grain [src: BusinessDay].
- Lorries park in a dense herd with buyers squeezed between them [src: Babilown 2011]. Their high wooden side-boards are packed with baskets and sacks, and loaders are on top passing goods down.
- Behind them are sheds and open stalls with mountains of onion sacks, pepper heaps on tarps and baskets of tomatoes. Rotten tomato pulp turns the ground red-brown.
- Yams are stacked like firewood in log piles.

**Kit parts:**
- `produce_lorry`: a 2-axle (Bedford/Mercedes-911-type generic) or 3-axle tipper-type truck, 8–10 m long, 2.5 m wide. Wooden high-sided body 1.8–2.5 m above the bed, painted panels and sayings. The load is mounded up to 4–4.5 m total height, roped and netted [est].
- `tomato_basket`: woven raffia/palm basket, conical, Ø0.6 top, 0.5–0.6 m high, filled and topped with leaves. Newer: plastic crate 0.55×0.36×0.3 (the regulated alternative) [est].
- `pepper_heap`: on tarp 2×3 m, mound 0.3–0.5 m; scotch bonnet red `#D8352A`, yellow `#F2B705`, tatashe red bell `#B5231C`.
- `onion_sack`: mesh/jute sack 0.5×0.9 m, red onion `#8E3B4A`, stacked in walls 2–3 m high.
- `yam_stack`: tubers 0.3–0.6 m long, Ø0.1–0.15, brown `#6A4B33`, laid in log piles 1.5 h × 3 long or inside a stick-fenced "barn".
- `offload_chain`: 3–6 loaders in a line, sacks on head.
- `rot_decal`: red-brown pulp mush `#5A2A1E` with flies.

**Dimensions:** 20–40 ha [est]; lorry yard on 30–50% of the area; sheds 6–10 m deep in rows of 50–100 m.

**Colours:** red/yellow produce on blue tarps; lorry bodies painted yellow `#E2B23A`, green `#3C7A3A`, red `#B62A22`, with hand-lettered slogans.

**Variants (by goods zone) [est]:** tomato/pepper 35%, onion 20%, yam 15%, grains/beans 15%, leafy veg/other 15%.

**Condition:** default *worn, wet*. Seasonal: *glut* (heaps everywhere, rot ↑) vs *scarcity* (fewer lorries, empty bays [src: Babilown]). *Clash/closure* state: lorries diverted to roadside markets elsewhere [src: Guardian].

**Props and life:**
- *Day:* buyer women with head-pans, wheelbarrows, Hausa-speaking porters, keke and danfo jam, police checkpoint on the approach.
- *Night:* lorries arrive and unload from about 22:00–05:00 under generator floodlights and bulbs on poles. Bonfires. Porters sleep on sacks and under lorries [est].

**SELECT BY:** `market_type=produce`; dense_mainland Kosofe-type; on an expressway edge `distance_to_main_road < 50 m`; near a city entrance.

**Gidi mapping:** Mile Market (lorries unloading pepper, tomatoes, onions, yams).

---

## 6. Cloth market — "Cloth Market"

**Looks like:**
- A maze of very narrow lanes in the old island, 2–3 m wide, walled by 3–6 storey plazas. Every ground floor is a cloth shop, and bolts are stacked to the ceiling and spill outside.
- Lace, wax print and woven cloth hang from rails above doors, so the lane becomes a canyon of colour.
- Porters push large wooden carts or head-load bales because lorries can't reach inside [src: Discover Lagos].
- Different streets specialise: lace on one, ready-made on another, electronics on a third [src: Discover Lagos].

**Kit parts:**
- `cloth_shop`: bay 2.5–3.5 m wide × 4–6 deep, shelving to 3 m with folded bolts (0.3×0.25×1.1 m each). A front rail at 2.2–2.6 m with hanging lengths 2–4 m.
- `bolt_stack`: folded cloth stacks on tables.
- `cloth_canopy`: tarps and cloth strung across the lane at 3 m (sun shade).
- `porter_cart` ("truck-pusher"): 2.4×1.2 m flatbed on 2 car wheels with bales roped in jute/plastic woven bags. `head_bale`: 0.6×0.4×0.4 on a head pad.
- `plaza_old`: 3–6 storey 1970s–90s RC blocks with balcony galleries, signs on every floor and AC units.

**Dimensions:** lanes 2–3 m [census, consistent with S§6.1], with 1 m usable after spill; blocks 10–20 m frontages.

**Colours (highest saturation in Gidi):** wax prints with indigo `#24356B`, orange `#E8742A`, yellow `#F2C200`, green `#2E8B3A`, magenta `#C21E6E`; lace white `#F4F1EA`, gold `#C9A24A`, wine `#6E1E35`; woven strip cloth (aso-oke style) burgundy/gold stripes.

**Variants [est]:** wax print 40%, lace/brocade 30%, ready-made 20%, accessories (beads, gele headties, shoes) 10%.

**Condition:** *worn* default; *burnt plaza* (fires recur) with a blackened facade above still-trading shops; *old plaza decayed* with spalling balconies.

**Props and life:** densest crowd in Gidi, 1.5–3 persons/m² on Saturdays [est]; women buyers, shop boys calling, tailor tape measures, wheelbarrow porters, okadas squeezing. Night: shut; lanes dark except a few bulbs, piles of cartons and rubbish.

**SELECT BY:** `market_type=cloth`; old_island; `storeys` 3–6; lanes the narrowest in the city.

**Gidi mapping:** Cloth Market.

---

## 7. Grain yard — "Daleko Grain Yard"

**Looks like:**
- A wholesale market for bags of rice, beans, groundnut oil, palm oil, semolina and sugar [src: Legit.ng] arranged as walled warehouse lock-ups opening onto a yard.
- 50 kg woven polypropylene sacks in walls of 15–25 high on pallets. Trucks back in, and loaders carry sacks on their heads and shoulders.
- Spilt grain in the dust, pigeons, oil jerrycans in rows. Shanties grow at the edges and get cleared [src: Nairametrics].

**Kit parts:**
- `grain_store`: block lock-up 4–6 m wide × 6–10 m deep × 4 m, steel double door 3 m wide.
- `sack_50kg`: 0.9×0.5×0.2 m when laid flat; white PP `#EDEBE4` with a coloured print band (invented brands: red, green, blue rice logos), beans in brown jute `#9A7B4F`.
- `sack_wall`: 10–25 layers on timber pallets 1.2×1.0.
- `oil_jerrycan`: 25 L, 0.38×0.27×0.43; groundnut oil yellow-clear, palm oil orange-red `#B8471C`, can yellow `#E8C547`.
- `drum`: 200 L steel drum Ø0.58×0.88, blue/black.

**Dimensions:** 2–5 ha [est]; yard 20–40 m wide for truck turning.

**Variants [est]:** rice 40%, beans 20%, oils 20%, flour/sugar/semolina 20%.

**Condition:** worn concrete yard, potholes with water; *cleared edge* state after shanty removal.

**Props and life:** forklift rare; human chain loading; 10 t trucks and pickups; dust haze. Night: shut and guarded, with a few trucks parked waiting.

**SELECT BY:** `market_type=grain`; dense_mainland near the produce/food market cluster; industrial edge.

**Gidi mapping:** Daleko Grain Yard.

---

## 8. Plank / timber market on a canal — "Boundary Plank Market"

**Looks like:**
- A long canal bank or lagoon creek lined with timber sheds where sawn planks are stacked in big blocks.
- Logs float in the water bound into rafts, waiting for the saw. Canoes ferry planks.
- Sheds are open timber frames with old zinc, and the ground is a soft brown carpet of sawdust and bark.
- Often co-located with the sawmill (item 19). Timber comes by water rafting [src: Guardian].

**Kit parts:**
- `plank_stack`: sawn boards 50×300×3,660 mm ("2×12 by 12 ft") [est, standard local sizes: 2×2, 2×3, 2×4, 1×12, 2×12 in. by 12 ft]. Stacked crib-style 1–2.5 m high, fresh `#C9A56B` → weathered grey `#8E8578`.
- `plank_shed`: timber poles, zinc roof 6×12 m, open sides.
- `canal_edge`: timber pile revetment (planks nailed to piles) + mud bank.
- `raft`: logs Ø0.6–1.2 m × 6–12 m, chained or wired in groups of 10–40 [src: Guardian (sorted into rafts by wires and timber dogs)].
- `canoe`: dug-out/plank canoe 6–10 m × 1 m, black tar `#1F1A16`.

**Dimensions:** canal 10–30 m wide; market strip 200–600 m × 30–60 m [est].

**Variants:** plank market alone 50%, attached to sawmill 50%.

**Condition:** *worn* (default), *flooded* (high tide submerges the lower stacks), *fire* (sawdust fires; blackened stacks).

**Props and life:** carpenters buying, pickups loading, planks on heads, boys poling canoes. Night: dark, with a few kerosene/LED lamps on the guard huts and smoke from sawdust burning.

**SELECT BY:** `market_type=plank`; waterfront; `on_water/canal`; near sawmill.

**Gidi mapping:** Boundary Plank Market.

---

## 9. Livestock market and abattoir — "Oko Cattle Market & Abattoir", "pen"

**Looks like:**
- A walled complex of three parts: an open-air cattle market where herds of white humped zebu with long horns stand in dusty pens or loosely tethered; a lairage (holding pens, roofed); and slaughter halls (long sheds with concrete floors and drains).
- The drains run red to a channel outside. Hides are spread or hung to dry, and the smell of singed skin from hide-burning fires hangs in the air (hides are often burned with tyres as fuel [est]).
- Cattle arrive packed in lorries from the north [src: OALib study]. A cattle crush-way leads from market to lairage [src: VON].
- Long internal roads (600 m reconstructed road) [src: VON], incinerator, refrigerated meat vans [src: VON].

**Kit parts:**
- `pen`: steel-pipe or timber-rail fence 1.4–1.6 m high, 3–4 rails, 10×20 m, gate 3 m; ground manure-mud `#4A3A26`. Some with a zinc shade roof on 4 poles over half.
- `crush_way`: a 0.8–0.9 m wide fenced chute, 1.8 m high, 30–80 m long.
- `slaughter_hall`: steel portal shed 20×60 m, eaves 5–6 m, open sides 1.5 m wall; floor screed with gutters 0.3 m.
- `red_gutter`: open drain 0.4–0.6 m wide, liquid `#6E1A14` → dark `#3A0E0A`; puddles.
- `hide_rack`: timber rails 1.5 m with hides; `singe_fire`: tyre ring fire with black smoke.
- `cattle`: zebu humped, white `#E8E2D6` / red `#8A3E26` / black-and-white, horns 0.5–1 m (long lyre-horned types) [est].
- `livestock_lorry`: lorry with high timber/steel slats, cattle standing.
- `ram_line`: rams tethered along a road edge (festival days [src: Guardian Kara]).

**Dimensions:** 10–20 ha [est]; pens in rows of 10–30.

**Variants:** cattle market + abattoir (full) 40%; roadside cattle market under a flyover (Kara-type) 30% [src: Kara articles]; small LGA slaughter slab (10×15 m shed) 30%.

**Condition:** *operating* (default, red drains, smoke); *sealed* (closed for unsanitary practices [src: Arise]) — gate shut, notice; *rebuilt* (new white-painted halls, cold vans).

**Props and life:** Fulani herders with sticks and wide hats, butchers in bloody white aprons/singlet, meat wheelbarrows, vultures/egrets on roofs, dogs. Night: cattle low in the dark; slaughter from 03:00–06:00 under bulbs [est].

**SELECT BY:** `market_type=livestock`; sprawl edge / dense_mainland fringe; near expressway or rail; far from elite.

**Gidi mapping:** Oko Cattle Market & Abattoir, pen.

---

## 10. Fish market at a jetty with smoking racks

**Looks like:**
- A wharf/jetty on the lagoon where canoes nose in. On land, an open shed of concrete slab tables with fish basins, and behind it a smoke-hazed yard of fish-smoking ovens tended by women.
- Drum ovens are cut-down oil drums with a wire mesh rack on top; box/mud ovens are rectangular brick or mud kilns with mesh trays stacked 3–6 high [src: AJOL survey: drum, box and mud ovens].
- Smoked fish (golden-brown to black) piled in baskets. Old towns have the biggest fish market of the region (Epe-type) [src: Wikipedia Oluwo]. A modernised version has 339 shops in neat rows [src: ThisDay].
- The only working jetty is often the fish-market jetty [src: Shipping Position].

**Kit parts:**
- `jetty`: concrete deck on piles 3–5 m wide × 30–80 m, or timber deck on palm piles; steps down to water.
- `drum_oven`: 200 L drum Ø0.58, cut to 0.6–0.9 m, side fire hole 0.3×0.25, mesh grill on top, soot black `#1B1714`, rust.
- `box_oven` (Chorkor-type): block/mud rectangle 2.0×1.0×0.8 m with 2 fire holes, stacked wooden-framed mesh trays 1.0×2.0 up to 6 high [src: PIND (Chorkor oven)].
- `smoke_rack`: timber rack 1.2 h with fish lines.
- `smoked_fish`: catfish curled rings, bonga, panla (hake) [src: TheCable]; colour `#9C6A2F` to `#3A2414`.
- `firewood_pile`, `mangrove_bundle`.
- `fish_basin`: enamel/plastic basins Ø0.5, ice in polythene.
- `canoe` (see item 8), motor canoes with outboard.

**Dimensions:** shed 15×40 m; smoking yard 20×30 m with 20–60 ovens [est].

**Variants:** fresh fish wharf 40%, smoking yard 40% (Makoko-type waterfront [src: TheCable]), modern market hall 20%.

**Condition:** worn and sooty (default); *modern rebuilt* (white tiles, blue shutters); *decayed* jetty with missing slabs.

**Props and life:** women from 03:30 preparing [src: TheCable], men mending nets and canoes [src: Guardian], gulls, cats, buyers with coolers. Night: smoke glow orange under racks, kerosene lamps, canoes landing at dawn.

**SELECT BY:** `market_type=fish`; waterfront or old_island/old-town lagoon edge; `on_water`.

**Gidi mapping:** fish market at a jetty with smoking racks.

---

## 11. Roundabout market — "Ikotun-style Roundabout Market"

**Looks like:**
- A big traffic roundabout whose central island and every approach edge have been swallowed by trade. Lock-up rows of the main market (open-air, ~8,400 lock-ups [src: Wikipedia Ikotun]) back onto the road, and street traders and danfos fill the carriageway [src: Blueprint].
- Umbrellas ring the island, tables block one lane, and buses load in the roundabout itself.
- Enforcement teams periodically clear traders [src: ThisDay]; roundabout slated for removal in road works [src: Guardian].

**Kit parts:**
- `roundabout_island`: Ø30–60 m kerbed island with a dry-grass centre, a monument or billboard, and a ring of 40–80 umbrella stalls at the kerb [est].
- `lane_takeover`: tables and mats occupying 1–2 m of the outer lane.
- `bus_park_edge`: danfo nosed-in, conductor shouting.
- `market_backwall`: lock-up rows facing the road.

**Variants:** island trade 50%; approach-only 30%; cleared (after enforcement: empty island with debris, only a few hawkers) 20%.

**Condition:** default busy/worn; *cleared* state.

**Props and life:** hawkers between cars, task-force pickup, a traffic warden on the island. Night: lantern and LED-lit stalls on edges, suya fires, headlight streams.

**SELECT BY:** `junction_type=roundabout` AND district dense_mainland/sprawl AND market within 300 m.

**Gidi mapping:** Ikotun-style Roundabout Market.

---

## 12. Periodic market days (behaviour)

**Looks like:** In old towns and sprawl edges, open squares and road verges are near-empty most days but fill on market day with mats, umbrellas and trucks. Forest-zone West Africa favours 4-day and 8-day market weeks [src: Cambridge, Hill 1966]; modern Yoruba practice often uses the 7-day week [src: DiscoverYoruba].

**Kit parts:** `market_square_empty` (bare concrete slabs, a few skeletal stall frames without roofs, a shade tree); `market_day_overlay` (spawn mats, umbrellas, stalls, lorries).

**Rule [est]:** each periodic market gets `cycle ∈ {4, 8, 7}` days (shares 40/20/40) and a `phase` from its seed. In-game day `d` is a market day if `(d + phase) % cycle == 0`. On market days: stall density ×4, traffic ×2. Off days: 10% occupancy.

**SELECT BY:** old_island old towns (Ikorodu/Epe type), sprawl (Badagry type).

**Gidi mapping:** periodic market days.

---

## 13. Phone malls / converted houses — "Gadget Village"

**Looks like:**
- A former residential quarter where bungalows and 2-storey houses have been converted to phone and accessory plazas.
- A bungalow front becomes a row of 2×2 m glass cubicles; others are rebuilt as 3–4 storey phone malls on the same plot.
- Iron kiosks and standalone umbrellas fill every frontage [src: Rest of World]. LED-strewn display stands [src: Rest of World].
- Seven main streets; central street is busiest [src: Rest of World]. Origin: by 2001 homeowners sold properties converted into plazas [src: Rest of World]. 300-shop complex demolished on 24 hours' notice [src: Rest of World/Substack].

**Kit parts:**
- `converted_bungalow`: existing bungalow kit with front wall removed, 3–6 cubicles 2×2 m with aluminium-and-glass fronts, ceramic tile floors, signs across the old roof eave.
- `phone_mall`: on 15×30 m plot, 3–4 storeys; ground floor fully glazed cubicles; upper galleries 1.5–2 m deep with steel balustrade; facade ACP cladding silver `#C0C3C6` / blue `#1F4FA0` / red `#C8282A` and big LED-backlit name "___ PLAZA"/"___ MALL"; external generator cage 2×3 m; AC condensers.
- `iron_kiosk`: steel box 1.2×1.2×2.2 with glass top display.
- `phone_stand`: tabletop glass case 1.0×0.5×0.4 on a table, LED strip.
- `repair_bench` (see item 3).

**Variants [est]:** converted bungalow 35%, purpose-built phone mall 3–4 st 40%, kiosks/umbrella clusters 25%.

**Condition:** new (bright ACP, LED), worn (faded banners, broken panels), *demolished* (complex razed).

**Props and life:** touts, "UK used"/repair boys, POS stands, buses; night: LED strips lit, cleared by 20:00.

**SELECT BY:** civic-adjacent dense mainland (Ikeja type); `storeys` 1–4; residential street grid repurposed.

**Gidi mapping:** Gadget Village; phone malls.

---

## 14. Shopping plaza (generic)

Base: B§6.5. Additions:
- **Kit parts:** `plaza_signband` (full-width parapet name 1.2–2 m tall), `plaza_carpark` (front forecourt 8–15 m, unmarked, cars and umbrellas), `plaza_gate` (steel sliding gate at the forecourt), `gen_house` (block hut 3×4).
- **Variants:** neighbourhood 2-storey (50%), main-road 3–4 storey with ACP (35%), mall-style with glass (15%; elite and Lekki-type sprawl) [est].
- **Condition:** new ACP → peeling panels; tiles falling off; half-let shutters with "SHOP TO LET" banners.
- **SELECT BY:** main road, dense_mainland or sprawl; elite gets glass mall variant.
- **Gidi mapping:** shopping plazas.

---

## 15. Container shops and "Container Court"

**Looks like:** 20 ft containers (6.06×2.44×2.59 m [src: ISO]) on blocks, a doorway or full side cut out, a steel flap propped as awning. Used as shops, offices, site cabins and, in Gidi, a container used as a holding cell ("Container Court").

**Container jail (Gidi invention):** no source found for a real Lagos container jail; treat as fiction built from patterns of container offices and police posts. Spec: one 20 ft container, doors chained with padlock, small cut window 0.3×0.6 with welded bars; painted dark blue `#1F2E4A` with hand-stencilled white "HOLDING" text; next to it a block police/task-force post 3×4 m with a bench and a corrugated awning; floodlight on a pole; red-white barrier.

**Kit parts:** `container_20` (corrugation pitch 0.27 m), `container_40` (12.19 m), `door_cut`, `flap_awning`, `container_jail` (above), `block_plinth`.

**Colours:** original livery maroon `#7A2E26`, blue `#2B4E8A`, green `#2E6B4A`, grey `#7D8287`; repainted telecom yellow, bank orange.

**Variants [est]:** airtime/POS 35%, drinks/provisions 25%, office/site cabin 20%, barber/tailor 10%, storage 10%. Container jail: one-off.

**Condition:** new paint; rust bloom around cut edges; dented; abandoned (doors open, bush).

**SELECT BY:** main roads, junctions, port; Container Court at a civic/port edge.

**Gidi mapping:** container shops; Container Court.

---

## 16. Kiosk types

Base: B§6.3. Specific types:

| Type | Body | Size (w×d×h) [est] | Colour | Signature props |
|---|---|---|---|---|
| Recharge / POS | metal or wood box, or just a table + umbrella | 1.2×0.8×2.2 | telecom yellow `#FFCC00`, green `#00A651`, red `#E2231A`; bank orange `#F26A21` | POS terminal, "POS HERE / WITHDRAWAL / TRANSFER" sign, small generator, phone charging strip |
| Provisions ("mallam" shop) | timber box with shelf front | 2.4×1.5×2.4 | faded blue or green | stacked sachet milk, noodles, sugar cubes, biscuits clipped on strings; bench; bulb |
| Newspapers | rack board + table | 1.5×0.6 table, A-frame 1.2 h | red/white | papers pinned by clothespeg to a board at 1.5 m; free readers' crowd |
| Pure water | stack outside a shop/house | bags of 20 sachets (0.4×0.3×0.2) stacked 1–1.5 m | clear plastic with blue print `#2F78C2` | chest freezer, "PURE WATER" sign, ice blocks |

**Condition:** new vivid paint → faded, rust, tarp patches.

**SELECT BY:** every street; POS/recharge near bus stops and banks; provisions at back streets and estate gates; newspaper at junctions in civic/old island.

**Gidi mapping:** kiosk types.

---

## 17. Print shops and kiosks — "Pedro Print Row"

**Looks like:** a residential street in a print district where most houses have small print kiosks bolted on as afterthoughts [src: TechCabal; "about 200 print shops"]. Lean-to rooms 2×2 to 3×4 m against house fronts, holding small offset presses, guillotines, screen-printing tables; ream boxes, wedding invitation cards, calendars drying on lines; colourful banners outside.

**Kit parts:** `print_lean_to` (block or sheet-steel room, mono-pitch zinc, 2×2–3×4 m, front open with grille), `offset_press` (1.5×1.0×1.4 m, green/grey), `guillotine` (1.2×0.8×1.3), `screen_table` (2×1 m), `paper_reams` (0.3×0.22×0.05 in boxes), `drying_line` with sheets, `ink_drum`.

**Variants:** large print hall (converted bungalow, 10×15 m) 20%; kiosk 60%; flex-print shop with wide-format printer and rolled banners 20% [est].

**Condition:** worn; paper waste piles; ink stains.

**Props/life:** customers waiting for jobs, generators, night work before festivals/elections (lights till 23:00).

**SELECT BY:** dense_mainland (Shomolu type); back streets; 1–2 storey houses.

**Gidi mapping:** Pedro Print Row.

---

## 18. Bakeries — "Ayo Bakery Row"

**Looks like:** low sheds and converted bungalows where dense white tin loaves are baked (lidded Pullman tins [src: Culture Custodian / Real Bread]). Brick/clay ovens fired by wood (firewood now banned for commercial cooking, bakeries pushed to LPG [src: Guardian]). Outside: firewood stacks, bread-van and hawker queues, trays of loaves on heads.

**Kit parts:** `bake_shed` (8×15 m, block walls, high zinc roof with vents, chimney 6–8 m of block or steel Ø0.4), `wood_oven` (brick 2.5×3×1.5 m, arched mouth 0.6 m, soot), `bread_tin` (0.3×0.11×0.11 m, black steel, in racks of 40), `proof_rack` (steel 1.8 h), `firewood_stack` (1.5 m high), `bread_tray` (on heads, 0.6×0.4, loaves in printed polythene), `bread_van` (white panel van).

**Variants:** wood oven 40% (old), diesel/gas oven 50%, industrial 10% [est].

**Condition:** sooty wall above the oven door; flour dust white on everything.

**Props/life:** night baking 02:00–06:00 with a glowing oven mouth; dawn hawkers depart with trays.

**SELECT BY:** sprawl (Agege type); back streets; `wealth` low–mid.

**Gidi mapping:** Ayo Bakery Row.

---

## 19. Sawmill — "Okobaba Sawmill", "saw shed", "sawdust"

**Looks like:** a large lagoon-edge sawmill site with 2,000+ sawmill operators [src: Guardian/BusinessDay], supplying 80–90% of the city's wood [src: Guardian]. Floating log rafts at the edge sorted by wire and timber dogs [src: Guardian/Eyes of a Lagos Boy]; rafts historically up to 600 m long, 50 m wide, 2 m deep [src: Guardian]. On land: saw sheds with big band saws, sawdust mountains smouldering, shanties of the workers between.

**Kit parts:**
- `saw_shed`: steel or timber portal 8×20 m, eaves 4 m, rusty zinc, open sides; band saw (wheels Ø1.5 m, frame 4 m high) and log carriage rails 10 m.
- `log_raft`: logs Ø0.6–1.2 × 6–12 m, bound, floating.
- `log_ramp`: earth/timber slipway from water to shed.
- `sawdust_pile`: cone Ø5–15 m, 2–5 m high, `#B88A55` fresh → `#5A3E2A` burnt/wet; smoke wisps from smouldering core.
- `plank_stack` (item 8).
- `worker_shanty`: plank huts on stilts.

**Variants:** large site 60%; small single-saw shed 40%. Relocation state: *abandoned* (state relocated millers to a new timber village [src: BusinessDay]) — empty sheds, sawdust only.

**Condition:** worn; fire scars; decayed.

**Props/life:** logs winched by hand and tractors, loud saws, boys diving to bind rafts, canoes. Night: sawdust glow and smoke.

**SELECT BY:** waterfront; lagoon edge; near rail/bridge (Ebute Metta pattern).

**Gidi mapping:** Okobaba Sawmill, saw shed, sawdust.

---

## 20. Scrap yards

**Looks like:** walled or open yards of crushed cars, iron bars, aluminium and copper piles; weighing scales; dealers buying from scavengers with handcarts; a market for iron and steel products also handles "accidented vehicles" and old company equipment [src: Vanguard Owode]. Prices set daily by recycler rates [src: technext/edgex].

**Kit parts:** `scrap_mound` (2–5 m high, rust), `car_hulk` (stripped car shells stacked 2–3), `platform_scale` (1×1 m steel deck with beam), `scrap_cart` (handcart 1.5 m), `sort_heap` (copper `#B06A3A`, aluminium `#B9BBB8`), `cutting_torch_set` (gas bottles).

**Variants:** street scrap dealer (fenced 10×20 m) 60%; big scrap market 30%; port scrap export yard 10% [est].

**Condition:** always worn; *burnt* (fires with tyres).

**SELECT BY:** dense_mainland, port, near landfill.

**Gidi mapping:** scrap yards.

---

## 21. Mechanic villages and vulcanisers

**Mechanic village looks like:** a gated yard of mechanics' sheds and pits — a "disorganised maze of car parts and men in grease-stained blue overalls" [src: Zikoko]; a shared gate, vehicles locked inside at 22:00 [src: Zikoko]; electricians, panel beaters, sprayers alongside mechanics [src: Zikoko]. Many date from 1981 land allocations [src: Guardian].

**Kit parts:** `mech_shed` (timber/steel lean-to 4×6 m, zinc), `pit` (0.8×4×1.5 m), `car_on_blocks`, `engine_hoist` (A-frame steel 3 m with chain), `spray_booth` (tarp enclosure, overspray stains), `panel_beater_bench`, `blue_overall` people, `gate_kiosk`.

**Vulcaniser looks like:** roadside 1×1 m spot with a compressor (scavenged AC compressor on a small motor [src: HNN] or a petrol twin [src: Jiji]), a tyre-shaped painted sign, tyres stacked, a bowl of water to find leaks, kerosene-heated patch clamp [src: HNN], a wooden bench, umbrella. One on almost every block [src: HNN].

**Vulcaniser kit:** `compressor` (0.8×0.4×0.6, red tank), `tyre_sign` (tyre painted white with "VULCANIZER" lettering, often on a pole), `water_bowl`, `tyre_stack`, `bead_breaker` (lever).

**Variants:** mechanic village 0.5–3 ha [est]; roadside mechanic (on the shoulder) 40% of mechanic presence; vulcaniser every 100–300 m on main roads [est].

**Condition:** oily ground always; *demolished* village (task force [src: Gazette]).

**Props/life:** test drives, horns, revving; night: closed, some cars left on road.

**SELECT BY:** all mainland; vulcanisers on main roads, junctions, filling station edges.

**Gidi mapping:** mechanic villages and vulcanisers.

---

## 22. Warehouses and industrial estates

**Looks like:** walled estates of steel portal sheds with low-pitch long-span roofs in faded blue/green/white, roller doors 5–6 m high, loading aprons, trailers, gatehouses. Examples: 6,870 m² four-bay warehouse; 7,420 m² three-warehouse compound with offices [src: Nigeria Property Centre]. Estates sit in Ikeja/Ilupeju/Oregun-type zones [src: Estate Intel].

**Kit parts:** `warehouse_shed` (30×60 m, eaves 8–10 m, ridge +2 m, 6° pitch; walls block 3 m then sheet cladding), `roller_door` (5×5 m), `office_front` (2-storey block 8×30 m against shed), `loading_apron`, `trailer` (container on skeleton trailer), `gatehouse` (2.5×2.5 m with barrier), `perimeter_wall` (2.4–3 m with razor coil), `security_light` (pole floodlight).

**Colours:** cladding blue `#3D6A9E`, green `#4F7F57`, white `#E5E6E2`, rust streaks; walls cream with blue/green band.

**Variants:** port bonded warehouse 30%, industrial estate shed 50%, private compound store 20%.

**Condition:** new cladding; faded and streaked; roof sheets missing; abandoned (collapsed roof, bush).

**SELECT BY:** port; industrial estate in civic/dense_mainland; near rail and expressway.

**Gidi mapping:** warehouses and industrial estates.

---

## 23. Factories ("works")

**Looks like:** large walled compounds with tall sheds, a chimney 20–40 m, silos or tanks, conveyors, a painted name on the gable ("___ WORKS"), staff bus park, gatehouse. Many older works are idle or partly closed.

**Kit parts:** `factory_hall` (60×120 m, 10–15 m eaves, sawtooth roof option), `chimney` (brick or steel Ø1–2 m, 20–40 m, soot ring), `silo` (Ø6–10 m, 15–25 m), `conveyor`, `staff_bus`, `gable_sign`.

**Variants:** food/beverage 30%, plastics/chemicals 25%, steel/building materials 25%, textiles (often closed) 20% [est].

**Condition:** running (smoke, lights), idle (rust, no trucks), abandoned (broken windows, trees).

**SELECT BY:** industrial estates, port; Ikeja/Ilupeju type.

**Gidi mapping:** factories ("works").

---

## 24. Bank branches

**Looks like:** 2–3 storey block with a glazed ground floor, cladding in the bank's colour (generic: orange, red, purple, blue, green), canopy over entrance, ATM gallery with 2–4 ATMs in an outside lobby, security doorway (cylindrical airlock door), car park with gate, big generator in a cage, armed guard. POS umbrellas cluster outside.

**Kit parts:** `bank_branch` (15×25 m, 2–3 st), `atm_gallery` (3×4 m glass box), `airlock_door` (Ø1.4 m glass cylinder), `logo_panel` (backlit 2×1 m on pole), `bank_genset_cage`, `car_park`.

**Colours (generic liveries):** orange `#F26A21`, red `#C8102E`, purple `#5B2C83`, navy `#0E2D6E`, green `#00843D`.

**Variants:** standalone branch 60%, ground floor of plaza 30%, cash centre/ATM kiosk only 10%.

**Condition:** new (polished, LED), dated (old tiles, faded), closed (signs removed).

**Props/life:** queues at ATMs, POS hawkers, cash-in-transit van, night: lit ATM gallery and logo.

**SELECT BY:** main road, all districts except waterfront slum; density higher in civic/old island.

**Gidi mapping:** bank branches.

---

## 25. Bank towers on a waterfront — "Bank Row", "bank tower"

**Looks like:** a waterfront boulevard of 20–30 storey bank headquarters. Real example of the pattern: a 28-storey, 124 m bank HQ (1991–1999) on the island marina [src: Wikipedia/SkyscraperPage]; ~20-storey ~80 m tower facing the lagoon [src: Nigeria Housing Market]. 1970s–90s concrete and glass slabs, curtain-wall towers, rooftop logos, helipads.

**Kit parts:** `bank_tower` (25×40 m slab, 20–30 st, floor 3.6–4 m), curtain wall in blue-green glass `#3E6C78` or bronze `#5A4636`, concrete fins, rooftop logo 6–10 m, podium 2–4 st with banking hall, waterfront road and seawall.

**Variants:** modernist slab (1970s, concrete grid) 40%; postmodern glass 40%; new glass 20%.

**Condition:** maintained; dated (stained concrete, missing panels); vacant (dark floors).

**Props/life:** bankers, hawkers on pavement, gridlock, night: lit logos and some floors.

**SELECT BY:** old_island waterfront, elite (VI type) boulevards.

**Gidi mapping:** Bank Row, bank tower.

---

## 26. Office blocks

**Looks like:** 4–12 storey RC frames with horizontal window bands, ACP or tile cladding, rooftop water tanks, generators at grade, signage at top ("___ HOUSE"), a security post.

**Kit parts:** `office_block` (20×30, 4–12 st, 3.5 m floors), `ac_split_units`, `roof_tank_row`, `name_band`.

**Variants:** government office (old, cream/green paint) 30%; private 1980s (tile, tinted glass) 40%; new glass/ACP 30%.

**Condition:** maintained; stained and patched; abandoned (half-empty, missing windows).

**SELECT BY:** civic, elite, old island, main road.

**Gidi mapping:** office blocks.

---

## 27. Fuel stations and black-market fuel

**Looks like:** a flat forecourt with a big steel canopy over pump islands, a shop/office block behind, underground tanks with manhole lids, a tall price pylon. The main pump must be ≥15 m from road edge; stations ≥400 m apart; max 4 per 2 km both sides [src: DPR guideline via Nigerian Lawyer]. Lagos highway stations need ≥2,500 m² land; max 9 pumps/18 nozzles [src: Nigerian Lawyer].

**Kit parts:**
- `canopy`: steel space frame 24–36×12–18 m, 5.5–6 m clearance, fascia 1–1.2 m deep in brand colours with underlights [est].
- `pump_island`: concrete island 4×1.2×0.2, 1–2 dispensers 1.0×0.5×1.9 m.
- `station_kiosk`: block 6×8 m office/shop, with lubricant shelves.
- `price_pylon`: 6–8 m high with LED price digits.
- `tank_lids`: 4–6 manhole covers in a line.
- `tanker`: 33,000 L articulated tanker unloading with hose to manhole, fire extinguisher, cones.
- `queue`: cars lined up 200–500 m during scarcity [src: Channels].
- `jerrycan_seller`: roadside man with 5–20 jerrycans (yellow `#E8C547`, 10–25 L), a funnel and a hose, often at a bend near a station [src: ICIR/Channels].
- `black_market_drum`: blue drum on a table with a siphon.

**Colours (generic brand liveries):** green `#00843D`/yellow; red `#C8102E`/white; blue `#0057A8`/white; orange.

**Variants:** major brand 40%; independent "mega station" 30%; small independent (2 pumps, faded) 30% [est].

**Condition:** new; worn (faded canopy, broken lights); *dry* (no fuel, "NO FUEL" sign, rope across); abandoned (canopy rust, bush); scarcity scene adds queues and jerrycans.

**Props/life:** attendants in uniform, okada/keke queue, mini-generators being filled; night: canopy floodlit, the brightest light on a road.

**SELECT BY:** main roads, 400 m spacing; scarcity flag adds black market.

**Gidi mapping:** fuel stations (canopy, pumps, kiosk, tanker unloading, black-market jerrycans).

---

## 28. Clearing-agent kiosks — "Collector Row"

**Looks like:** at port gates, rows of small offices in containers, sheds and kiosks: clearing and forwarding agents, "C&F" signs, document photocopy, food stalls; trucks queue outside port gates for hours or days [src: Shipping Position, BusinessDay].

**Kit parts:** `agent_container_office` (20 ft container with window AC and door, white or blue), `agent_kiosk` (2×2.5 m), `photocopy_table`, `sign_board` ("___ NIG LTD — CLEARING & FORWARDING"), `truck_queue` (container trailers parked bumper to bumper along road edges).

**Variants:** container office 50%, shed row 30%, umbrella table 20%.

**Condition:** worn, dusty.

**Props/life:** agents with files, customs uniforms, tea sellers; night: truck queue with drivers sleeping under trailers.

**SELECT BY:** port; within 1 km of port gate.

**Gidi mapping:** Collector Row.

---

## 29. Tank farm with pipe racks

**Looks like:** a walled cluster of white or silver cylindrical tanks with bunded areas, pipe racks, tanker loading gantry, and long queue of tankers outside. Average tank farm capacity ~30 million litres; ~80% of the country's tank farms sit in Apapa-type port districts [src: BusinessDay].

**Kit parts:** `storage_tank` (Ø20–40 m, 12–18 m high, white `#E7E7E2` with rust streaks, spiral stair), `bund_wall` (1.5 m), `pipe_rack` (steel 3–6 m high, 2–4 tiers), `loading_gantry` (steel 6–8 m, arms), `tanker_queue`, `fire_ring`.

**Variants:** large depot 40%, small farm 60%.

**Condition:** maintained; rusted; abandoned.

**SELECT BY:** port.

**Gidi mapping:** tank farm with pipe racks.

---

## 30. Refinery towers and flare stack

**Looks like:** a large industrial complex (real example of pattern 2,635 ha in a free zone [src: offshore-technology]) with distillation columns, cracking units, tank farms and a flare stack. Mooring buoys offshore [src: Reuters via IOL].

**Kit parts:** `distillation_column` (Ø4–8 m, 40–80 m), `cracker_structure` (steel frame 30×30×60 m), `flare_stack` (Ø1–2 m, 80–120 m, flame 5–20 m orange `#FF8A1A` with heat shimmer, night glow), `tank_field`, `pipe_corridor`.

**Variants:** operating vs construction (cranes) [est].

**SELECT BY:** port or far sprawl coast.

**Gidi mapping:** refinery towers and flare stack.

---

## 31. Landfill with smoke and scavengers

**Looks like:** a ~40 ha mound of garbage (100-acre) [src: Vanguard], in use for 30+ years [src: Vanguard]; smoke from internal fires, fires lasting days [src: TheCable]; scavengers with sacks, hand carts, burning tyres to extract wire [src: ThisDay]; bulldozers spreading, compactor trucks.

**Kit parts:** `landfill_mound` (15–30 m high, terraced), `smoke_plume` (grey `#7A7672`, black at tyre fires), `scavenger` (with sack and hook), `scrap_pile` (sorted bottles, plastics), `bulldozer`, `waste_truck`, `shanty_ring` (scavenger huts), `buyers_scale` (item 20 platform scale), cattle/goats grazing.

**Variants:** active landfill; closed (grassed); burning.

**SELECT BY:** sprawl edge, near expressway.

**Gidi mapping:** landfill.

---

## 32. Colonial brick waterworks (1915)

**Looks like:** the first waterworks was built in 1910 [src: Lagos Water] with preserved equipment [src: Lagos Water]; Gidi's 1915 date is fiction. Red brick pump house with arched windows, iron roof trusses, a tall chimney, settling basins and a tower.

**Kit parts:** `pump_hall` (12×30 m, 8 m high, red brick `#8E3B2A`, arched windows 1.2×2.5 m, keystone, slate/iron roof), `brick_chimney` (Ø1.5 m, 25 m), `settling_basin` (concrete 20×40 m), `water_tower` (steel tank on frame 15 m), `date_plaque` ("1915").

**Condition:** maintained heritage; worn; derelict.

**SELECT BY:** old town edge / sprawl hills; unique landmark.

**Gidi mapping:** waterworks.

---

## 33. Pipeline corridor tapped at night

**Looks like:** a cleared strip with buried pipe, marker posts, burnt patches, jerrycans and canoes hidden; vandals tap valves to siphon fuel into containers [src: Sweetcrude/Channels]; repairs cleared right-of-way and added observation towers [src: Sweetcrude]; navy recovered 100,000+ jerrycans [src: Daily Trust].

**Kit parts:** `row_strip` (15–30 m bush cleared), `marker_post` (yellow/black 1.5 m), `valve_pit`, `observation_tower` (steel 10–15 m), `jerrycan_cluster`, `burn_scar` (black ground).

**Night:** headlamp torches, canoes on creek, fumes.

**SELECT BY:** sprawl / waterfront edge.

**Gidi mapping:** pipeline corridor tapped at night.

---

## 34. Market signage, generators, night lighting

- **Signage:** hand-painted boards and flex banners (S§5); market association boards; shop codes ("A170"); goods-specific symbols (tyre, phone, cloth).
- **Generators:** market-specific: on tyres in electronics markets; big floodlight sets in produce/grain yards (S§6.4).
- **Night lighting:** produce markets (floodlights, generator bulbs); fish smoking glow; fuel station canopies; bank logos; LED in phone malls.

**Gidi mapping:** all market items.

---

## Sources

- https://en.wikipedia.org/wiki/Ladipo_Market
- https://nairametrics.com/2025/09/07/top-7-largest-auto-spare-parts-markets-in-lagos/
- https://newtelegraphng.com/again-ladipo-spare-parts-market-sealed-over-environmental-breaches/
- https://en.wikipedia.org/wiki/Alaba_International_Market
- https://theculturetrip.com/africa/nigeria/articles/the-best-markets-in-nigeria
- https://connectciti.com/listing/globaltech-electronics-mall
- https://fmino.gov.ng/defence-minister-unveils-new-face-of-alaba-hails-market-as-africas-emerging-technology-hub/
- https://archive.businessday.ng/features/article/mile-12-market-preferred-destination-for-lagos-wholesalers-retailers/
- https://babilown.com/2011/08/08/nigeria-rise-in-food-prices-unleash-anguish/
- https://guardian.ng/?p=102844
- https://www.discoverlagos.ng/post/balogun-market-the-heartbeat-of-lagos-commerce
- https://besttravelwriting.com/2009/02/28/travel-and-shopping-bronze-market-hopping-around-lagos/
- https://www.legit.ng/699262-top-10-foodstuff-markets-lagos.html
- https://nairametrics.com/tag/daleko-market/
- https://guardian.ng/features/the-wood-merchants/
- https://businessday.ng/news/article/lagos-set-for-relocation-of-okobaba-sawmillers-to-ikorodu/
- https://eyesofalagosboy.com/2023/07/18/photo-of-the-week-from-raft-to-furniture/
- https://von.gov.ng/?p=367477
- https://oalib-perpustakaan.upi.edu/Record/doaj_3b177e4add0a4fab923c53b036a87cdb/Description
- https://www.arise.tv/lagos-government-shuts-down-illegal-abattoir-in-oko-oba-confiscate-contaminated-meat
- https://nairametrics.com/2025/10/18/lagos-abattoirs-8-major-slaughterhouses-powering-n328-billion-beef-market/
- https://guardian.ng/?p=2847977
- https://www.nigeriahousingmarket.com/news/ogun-state-kara-cattle-market-persists-17-months-after-official-relocation-order
- https://en.wikipedia.org/wiki/Oluwo_fish_market
- https://thisdaylive.com/index.php/2022/08/01/epe-the-new-hub-for-sports-modern-fish-trading
- https://shippingposition.com.ng/boat-operators-urge-lasg-to-build-jetties-in-epe/
- https://www.thecable.ng/?p=466204
- https://www.ajol.info/index.php/gjas/article/view/202982
- https://pindfoundation.org/2018report/content/footprints.pdf
- https://en.wikipedia.org/wiki/Ikotun
- https://blueprint.ng/lagos-taskforce-conducts-enforcement-operation-clear-illegal-street-traders/
- https://thisdaylive.com/index.php/2017/01/06/lagos-to-prosecute-38-street-traders-33-miscreants
- https://cambridge.org/core/journals/journal-of-african-history/article/abs/notes-on-traditional-market-authority-and-market-periodicity-in-west-africa1/31871FCD18E53DFB68BCC9345ADF2923
- https://discoveryoruba.com/yoruba-markets-and-market-days/
- https://restofworld.org/2022/tech-markets-lagos-nigeria/
- https://aidesolutionshub.substack.com/p/the-uncertain-future-of-lagos-computer
- https://en.wikipedia.org/wiki/Ikeja
- https://techcabal.com/2016/01/14/the-printivo-story/
- https://culturecustodian.com/making-dough-the-legend-of-agege-bread-the-culture-custodian/
- https://www.sustainweb.org/realbread/articles/may26-agege-a-go-go/
- https://guardian.ng/?p=2891526
- https://www.vanguardngr.com/2014/10/58-lock-shops-108-vehicles-razed-owode-onirin-market/amp/
- https://technext24.com/reviews/how-nigerias-scrap-metal-industry-works/
- https://www.zikoko.com/?p=369878
- https://guardian.ng/?p=1449108
- https://gazettengr.com/lagos-task-force-demolishes-mechanic-villages-in-lagos/
- https://www.historynewsnetwork.org/blog/9210
- https://jiji.ng/ojo/manufacturing-equipments/twin-cylinder-petrol-air-compressor-6FbcGPEv50si9DDADOWASWco.html
- https://estateintel.com/get-real-time-data-on-lagoss-industrial-real-estate-market
- https://nigeriapropertycentre.com/commercial/warehouses/lagos/ilupeju/showtype
- https://nigeriapropertycentre.com/commercial/warehouses/lagos/ikeja/oregun/showtype
- https://en.wikipedia.org/wiki/Union_Bank_Building_(Lagos)
- https://skyscraperpage.com/b31850
- https://www.nigeriahousingmarket.com/lagos/uba-house-marina-the-iconic-landmark-of-nigerias-financial-capital
- https://thenigerialawyer.com/requirements-for-filling-fuel-stations-in-nigeria/
- https://www.channelstv.com/2024/08/18/gridlock-queues-as-fuel-scarcity-hits-lagos/
- https://www.icirnigeria.org/lagos-residents-groan-as-fuel-scarcity-bites-harder/
- https://shippingposition.com.ng/?p=20621
- https://www.vanguardngr.com/2020/12/tin-can-gridlock-drives-up-trucking-cost-by-over-100/
- https://businessday.ng/exclusives/article/apapa-what-becomes-of-money-spinning-port-city-post-dangote-refinery/
- https://www.offshore-technology.com/projects/dangote-refinery-lagos/
- https://iol.co.za/business-report/international/2019-08-12-dangote-oil-refinery-delayed-until-end-of-2020/
- https://www.vanguardngr.com/2018/03/panic-olusosun-dumpsite-environmental-hazards/amp/
- https://thecable.ng/photos-fire-still-burning-ojota-dumpsite-six-days
- https://thisdaylive.com/index.php/2023/10/25/lagos-dislodges-scavengers-at-olusosun-dumpsite
- https://lagoswater.org/
- https://en.wikipedia.org/wiki/Lagos_Water_Corporation
- https://sweetcrudereports.com/welcome-to-arepo-where-vandals-are-kings
- https://www.channelstv.com/2012/09/17/nnpc-blames-fuel-scarcity-in-lagos-on-vandalised-arepo-pipeline/
- https://dailytrust.com/?p=757956
