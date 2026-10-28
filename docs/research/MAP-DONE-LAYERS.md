# What a "map done" district holds: the layer list (draft)

A draft for the owner and Claude to go through (28 Oct, the owner said yes to adding 11 layers and marking which draw lines: see "Added 28 Oct" at the end) (NOW 16 c; DECISIONS "'Done' is the map's bar", 27 Oct). Map done
means every layer a finished open-world area holds is in the district's records, so that later the kits only read
them: a house already says its kind, storeys and colour; a junction already says who goes first; a street already
says what drives on it at 8 in the morning. Nothing here is decided. Written by an agent on 27 Oct; the main session re-checked
its map counts and schema gaps (the Checked section at the end); the rest is not checked.

**Sources read for it:**
- GTA V's files, our reading: `~/gidi-data/research/gta/FINISHED-AREA.md` (three 0.16 km² sample boxes: a dense
  housing area, a shopping street, a port). Its figures are quoted below as **reference figures only**, never as
  targets: Gidi's targets come from the real Lagos place. No names, code or data from the game go into Gidi.
- `docs/research/FINISHED-AREA-INDUSTRY.md` (studio stages, Unreal's City Sample, UN-Habitat).
- The owner's list (27 Oct): "timetable, litter, infrastructure, civil services, houses, streets, the kind of cars,
  the kind of traffic lights, traffic symbols, the road color, I can't remember everything", widened.
- What the map holds now: every `map/dNN/plan.json` and `district.json` counted (table below), against
  `schema/map_schema.json` and `docs/MAP-FORMAT.md`.
- The building studies, in `docs/lagos-study/buildings/` (d12, d13, d15 to d19), for the kinds the map lacks.
- Also read for proposals already written: `decisions/lived-in.md` (days, district mix, moments, states),
  `docs/research/LIFE-IN-LAGOS.md`, `docs/BOARD.md` (the board's tools and brushes).

## What the map holds now (counted 27 Oct)

Records per district, read from `map/*/plan.json` and `district.json` (python -I, json only). Area is the district
outline's area in Gidi m² (shapely). **No district has a dress layer yet**: there is no `map/*/dress/` folder, so
faces, roof sheets, wall bays, gutter pieces, ground, relief, ground marks, litter, goods, posters and people are all 0.
There are also 0 frontages, 0 lean-tos and 0 person spots anywhere.

| district | Gidi km² | building | road | place | plot | wall | pole | wire | stall | vehicle | tree | furniture | mast | heap | rail | station |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d09 | 1.392 | 1,472 | 1,015 | 273 | 16 | 47 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| d12 | 0.966 | 963 | 882 | 235 | 3 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| d13 | 0.670 | 738 | 629 | 229 | 15 | 38 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| d14 | 0.572 | 687 | 367 | 204 | 4 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **d15 Mùṣá** | 1.214 | 4,268 | 363 | 555 | 4 | 21 | 579 | 360 | 726 | 824 | 92 | 85 | 15 | 12 | 1 | 1 |
| d16 | 0.475 | 395 | 300 | 107 | 17 | 32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| d17 | 0.709 | 831 | 669 | 206 | 9 | 39 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| d18 | 0.296 | 144 | 186 | 27 | 2 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| d19 | 0.259 | 286 | 144 | 44 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| d27 | 1.333 | 1,988 | 1,071 | 436 | 14 | 43 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| d28 | 1.686 | 1,703 | 1,190 | 273 | 24 | 65 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **all** | | 13,475 | 6,816 | 2,589 | 109 | 314 | 579 | 360 | 726 | 824 | 92 | 85 | 15 | 12 | 1 | 1 |

What the fields carry (same count):
- **Buildings:** all 13,475 have `kind`, `storeys` and `footprint`; 13,474 have `ground_floor`. Only Mùṣá's 4,268
  (31.7%) have `storey_h`, `roof`, `finish` (with its wall `colour`), `windows`, `outside_stair` and `wear`; the
  other 9,207 have no colour and no roof. 1,587 point to a place; 10 carry `use`. Kinds used: compound_house 7,365,
  face_me_bungalow 2,530, shop_under_flats 1,386, walkup 1,170, shack 791, kiosk_row 129, shed 92, school 9,
  church 1, market_block 1, station_hall 1. Storeys: 1: 3,082; 2: 8,900; 3: 1,285; 4: 208.
- **Roads:** all 6,816 carry `kind`, `width`, `surface`, `sand_cover`, both kerbs, `median`, `crown` and
  `ground_look` (the colours per layer: tar, earth, dust, mud). But 6,445 of the 6,453 roads outside Mùṣá say in
  their note that these are Mùṣá's commonest values, "to read": they are filled, not read. 0 roads carry a `name`.
  Gutters: 171 roads, all in Mùṣá (171 of its 363). Verges: 351 roads, all in Mùṣá. Surfaces: tar_worn 6,682,
  sand 71, earth 46, interlock 11, concrete 3, tar_new 2, laterite 1. **No road field says lanes, direction, speed
  or markings.**
- **Places:** 2,589; 7 have `hours`; 1 has a `name`. Kinds: church 1,336, school 524, clinic 203, buka 166, bar 96,
  garage 69, mosque 64, bank 45, fuel 42, bus_stop 20, police 15, motor_park 4, chemist 3, market 2.
- **Mùṣá per Gidi km²** (count / 1.214): buildings 3,516; places 457; poles 477 (182 with a lamp, 12 with a
  transformer); wires 297; stalls 598; parked vehicles 679 (saloon 601, danfo 73, okada 58, keke 54, lorry 14,
  bus 11, pickup 7, suv 6, in all districts' total); trees 76; furniture 70.
- Street length (centrelines summed, / outline area): 27.5 (d19) to 49.5 (d27) km per Gidi km², Mùṣá 37.4. My own
  run, not clipped to the outline; `scripts/working_bar.py`'s figures (27.5-47.8, FINISHED-AREA-INDUSTRY.md Checked
  section) may clip, so they differ a little.

## How to read the tables

- **Now:** does the map format hold the layer today? **yes** (a record type or field exists), **partly** (some of
  it, named), **no**. Then how much of the drawn map fills it.
- **Brush:** how it would be put on the board. **brush now** (one of the four brushes: litter, goods, relief, ground
  paint); **brush could** (many of the same along a street or over an area, so a new brush fits, every piece stored
  in full as the four calls require); **tool** (an existing one-by-one board tool or the side panel); **new tool**
  (nothing on the board places it yet); **table** (a district- or road-level table typed in, not painted).
- **Done when:** the measure. A real figure from the real place where one can be read (Google Maps, satellite,
  Street View, Open Buildings, Overture). Reference figures are labelled with their file. *guess* marks my guesses.
  "Not read yet" means nobody has the real figure.
- **Lines:** **yes** if the layer draws or moves a line on the map (a road edge, a drain, a plot, a footprint), so it
  must be settled before a district is "working"; **no** if it sits on lines already drawn.
- Densities per km² compare directly because houses, cars and stalls stay real size on the 1:3 map; only street
  length per km² does not (FINISHED-AREA-INDUSTRY.md, finding 1).

## A. Ground and roads

| # | Layer | What it is | Why the game needs it | Done when | Now | Brush | Lines |
|---|---|---|---|---|---|---|---|
| A1 | Streets on real lines | every road, street, lane and path, its kind | driving, walking, the map players read | 100% of length on a real line (STREETS.md per district); street km per km² matches the real district read from Google Maps (owed, NOW 16 f). Reference: UN-Habitat at least 18 km/km²; GTA V's files 23-50 road km/km² (FINISHED-AREA.md) | yes: `road.centreline`, `road.kind` (10 kinds); 6,816 roads | tool (Street) | yes |
| A2 | Road width | kerb to kerb | traffic fits; roads take their real share of land | every road's width read from satellite; road share of land against the real district (UN-Habitat: 20-30% of urban land for roads and parking, FINISHED-AREA-INDUSTRY.md) | yes: `road.width`; on all | tool | yes |
| A3 | Road surface and colour (the owner's "road color") | tar new or worn, laterite, sand, earth, interlock; its colours per layer | the look of every street; poor and wet places read as such (DECISIONS 16 Oct "Roads have surfaces") | 100% of roads with a surface and colours **read** from Street View or the owner's photos, none left "to read"; Overture's surface tags are not trusted (DECISIONS, "Data caution") | yes: `surface`, `sand_cover`, `ground_look`; filled on all, but 6,445 outside Mùṣá are Mùṣá's defaults "to read" | tool (Surface); patches by brush now (ground paint) | no |
| A4 | Lanes and direction | lanes each way; one-way streets; divided roads | traffic needs lanes to drive; a one-way street driven the wrong way is a Lagos moment | every road with more than one lane, or one-way, says so, read from Street View and Google Maps (one-way arrows: whether Google shows them in Lagos *not checked*). Reference: GTA V's files 45-97 lane-km/km², 28-57% of length one direction only (counts divided roads too) (FINISHED-AREA.md) | **no** field | table (per road, in the panel) | yes |
| A5 | Speed and road class for driving | how fast traffic goes on each road | driving feel; traffic that crawls on Ikorodu-type roads and races on the expressway | every road kind has a speed; per-road where real speed differs (*guess*: Street View cannot show speed; read from Google Maps typical traffic, not checked) | **no** | table | no |
| A6 | Kerbs, medians, road crown | raised kerb, drain wall, painted kerb, median barrier | the road's edge and what cars hit | every main road's kerbs and median read from Street View | yes: `kerb_left/right`, `kerb_paint`, `median`, `crown`; on all, mostly `none` (6,712 left kerbs) and defaults outside Mùṣá | tool | yes |
| A7 | Roadside drains | open, slab-covered or earth gutters, their state | the Lagos street edge; flooding; slabs to trip on | share of road length with its drains read per side from Street View; 100% of roads read | yes: `road.gutters`, dress `gutter_pieces`; 171 roads, all Mùṣá | tool now; brush could (along a road) | yes |
| A8 | Walkways, verges and drain crossings | the strip beside the road, the slab or plank over the drain at each gate | walking; every gate reachable | every gate and shop door over a drain has its crossing; verges read | yes: `verges`, `crossings`, kerb `raised_pavement`; 351 roads with verges, all Mùṣá | tool; brush could | yes |
| A9 | Road markings | lane lines, zebra crossings, stop lines, painted kerbs, BRT lane lines | traffic symbols the owner named; where markings are worn or absent, that is the look too | every main road's markings read from Street View (most local streets have none, *guess*) | **partly**: only `kerb_paint` (1 road) | brush could (a line along a road) | no |
| A10 | Bumps, potholes, ruts, speed breakers | the road's broken surface, home-made speed breakers | driving feel; the Lagos road | potholes and breakers per km of road, read on a Street View sample (figure not read yet) | **partly**: dress `relief` and `ground_marks` (potholes, ruts); no kind says "speed breaker"; 0 placed | brush now (relief); tool (Relief) | no |
| A11 | Ground off the road | yards, open ground, sand, laterite, grass, mud, puddles, water | every square metre has a ground (DECISIONS "Account for every square metre") | 100% of open land painted with a kind (the industry draft's topic 10, FINISHED-AREA-INDUSTRY.md) | yes: dress `ground` (12 kinds); 0 placed | brush now (ground paint) | no |
| A12 | Big drains and canals | the open storm channels and canals across the city | floods, bridges over them, a landmark of Lagos | every canal seen on Google Maps and satellite drawn | **no** (only a `ground` patch of `water`) | new tool | yes |
| A13 | Bridges, flyovers, footbridges | roads in the air, overhead footbridges over expressways | crossings; the Lagos skyline of flyovers | every flyover and footbridge on Google Maps drawn | **partly**: road points with height, kind `ramp`; no piers, rails or footbridge structure | tool (Street, with heights) | yes |
| A14 | Water, shore, water lanes, jetties | the lagoon, creeks, the canoe channels of the stilt town, landing places | Makoro's stilt town (DECISIONS "Makoro keeps its stilt town"); boats | shoreline drawn; every channel in the stilt town drawn (d19 study, finding 3) | **partly**: `ground` kind `water` with a level `z`; no water lane or jetty | brush now (ground paint); new tool for lanes | yes |
| A15 | Rail and stations | the line, level crossings, stations | trains, crossings, the station crowd | every line and station on Google Maps drawn | yes: `rail`, `station`; 1 each, Mùṣá | tool | yes |
| A16 | Trees and plants | palms, shade trees, plantain, shrubs, grass | shade, the look from above against the satellite | trees per km² against the satellite (figure not read yet; WorldCover reads 30% trees in d18, d18 study) | yes: `tree` (6 kinds), `ground` kind `grass`; 92 trees, all Mùṣá | tool; brush could | no |
| A17 | Ground height and where it floods | the lie of the land over a district: high ground, low ground, the streets that flood in the rains | water runs downhill; flooded streets are a Lagos season | every district's low ground and flood streets read (Google satellite after rain, news reports; method *not decided*) | **partly**: dress `relief` is a fine grid in mm for bumps, `ground` kind `water` has a level `z`; no district height, no flood area | brush now (relief, for small ground); new tool for flood areas | no |
| A18 | Road rules beyond lanes | no right turn, no lorries, slip lanes (the street's name is C16) | AI traffic needs the rules (GTA V's paths carry 25 kinds of road attribute, GTA-STUDY.md section 5, item 1) | every rule seen on Street View or Google Maps set | **no**: no turn ban, vehicle ban or slip lane | table; tool for slip lanes | yes |

## B. Traffic

| # | Layer | What it is | Why the game needs it | Done when | Now | Brush | Lines |
|---|---|---|---|---|---|---|---|
| B1 | Junctions and who goes first | each meeting of 3+ roads and its rule: lights, roundabout, warden, nobody | traffic cannot cross without it | every junction of 3+ roads has a rule. Reference: 30-116 junctions per 0.16 km² box in GTA V's files, 188-725 per km² *(arithmetic)* (FINISHED-AREA.md) | **partly**: roads join by sharing a point; no junction record or rule | new tool (click a junction) | yes |
| B2 | Traffic lights (the owner's "kind of traffic lights") | the lights, their kind, whether they work | the owner named them; dead lights with a warden are Lagos | every lit junction on Google Maps or Street View drawn, with working or not (*guess*: many are dark). Reference: 0-3 signal junctions per 0.16 km² box (FINISHED-AREA.md) | **no** | new tool | no |
| B3 | Traffic signs and street-name boards (the owner's "traffic symbols") | stop, no entry, no parking, BRT only, speed, direction boards, street-name blades | the owner named them; finding the way | signs per km of main road read from Street View (figure not read yet); every named street has a name board where real | **partly**: `pole.boards` (street-name blades only); no sign record | new tool; brush could (along a road) | no |
| B4 | Moving traffic: what drives where and when (the owner's "kind of cars") | the mix of okada, keke, danfo, molue, BRT, cars, lorries, tankers, carts per road kind and hour; okada and keke bans | the street at 8 am is not the street at 11 pm | a table per district per 2-hour slot whose shares add to 100 (lived-in.md, "the district mix", proposed), seeded from LIVING.md and Street View; method for real counts *not decided* | **no** (the old map had an `okada_ban` field, LIFE-IN-LAGOS.md line 64; the new schema has none) | table | no |
| B5 | Parked vehicles | each parked car, danfo, keke, lorry, wreck: kind, colour, spot | the street's look; cars to take | parked vehicles per 100 m of street, against a Street View sample (figure not read yet). Mùṣá now 679 per Gidi km². Reference: 1,050-2,081 parked-car spots per km² (FINISHED-AREA.md) | yes: `vehicle` (13 kinds, per-kind detail); 824, all Mùṣá | tool; brush could (along a kerb) | no |
| B6 | Transport routes and timetables (the owner's "timetable") | danfo, molue and BRT routes, their stops in order, how often by hour; train and ferry times | getting about; the conductor's route call; missions | every bus stop on at least one route; routes read from Google Maps (whether it carries Lagos danfo routes *not checked*) | **no** | table | no |
| B7 | Bus stops, lay-bys, shelters, BRT stations | where people wait and vehicles stop | the bus stop crowd, touts | 0 real bus stops missing (Google Maps); each with its shelter or none read | **partly**: place `bus_stop` (20 in all); no shelter or lay-by structure | tool (Place); new tool for the shelter | yes |
| B8 | Motor parks, okada and keke ranks | parks, and the ranks at junctions | the busiest spots in a district | 0 real parks missing (Google Maps); every rank seen on Street View drawn | **partly**: place and plot `motor_park` (4 places); no rank kind (activity `wait_on_okada` exists) | tool | yes |
| B9 | Fuel stations | the forecourt, canopy, pumps, queue | fuel, fuel queues (a world state, E7) | 0 real stations missing (Overture, Google Maps) | **partly**: place `fuel` (42), crossing kind `grate`; no canopy or pump | tool; new kind | yes |
| B10 | Traffic police, wardens, checkpoints | who stands in the road | the "roger" at the checkpoint, the warden at the dead light | every busy junction and checkpoint seen has its spots | **partly**: activities `direct_traffic`, `police_check` (person spots, 0 placed) | tool (Person) | no |
| B11 | Vehicle spawn spots and no-spawn areas | where a vehicle usually appears and when (a keke waiting at a junction 6 am to 10 pm), and where nothing may appear | parked and waiting vehicles that change through the day without a fixed record each (GTA V: car generators and no-spawn zones, GTA-STUDY.md section 5, item 14) | every rank, park and kerb the street view shows busy has a spawn spot with hours (figure not read yet) | **no** (`vehicle` records are fixed) | tool; brush could (along a kerb) | no |
| B12 | Boats and planes | canoes in the stilt town's channels, ferries on the lagoon, planes at the airport | the water and the sky move too | every channel and jetty has its boats; the airport has its planes (*owner's call* on how many) | **no** | tool, once the kinds exist | no |

## C. Buildings (the owner's "houses")

| # | Layer | What it is | Why the game needs it | Done when | Now | Brush | Lines |
|---|---|---|---|---|---|---|---|
| C1 | Footprints and cover | each house's outline | the district looks like the real place from above | cover between Google's 90%- and 80%-precision figures (CLAUDE.md, gated in `working_bar.py`); Mùṣá 43.22% against 43.26-47.65% (NOW 16) | yes: `building.footprint`; 13,475 | tool; draft from Open Buildings | yes |
| C2 | Kind | what sort of house | the kit builds from it; it says who lives there | every house has a kind that fits its block's real fabric (the building studies) | yes: `kind` (14 kinds); on all (gaps in C12) | tool | no |
| C3 | Storeys and heights | storeys and each storey's height | the skyline | storey mix within 2 points of Google's 2.5D per band (as d15's study measured) | yes: `storeys` on all; `storey_h` on Mùṣá's 4,268 only | tool | no |
| C4 | Wall finish and colour (the owner's "colour") | render, bare block, tiles; the paint | a house "already says its colour" (DECISIONS) | 100% of houses with a finish and colour, read from Street View or satellite per block | yes: `finish`; on Mùṣá's 4,268 only (31.7%) | tool; brush could (a block's colours) | no |
| C5 | Roof | form, material, rust, colour | the overhead view against Google Earth | 100% with a roof; roof colours against the satellite by eye | yes: `roof`; on Mùṣá's 4,268 only | tool | no |
| C6 | Ground floor | home, lock-up shops, workshop, stalls | street life sits on it | 100% set, front houses read from Street View | yes: `ground_floor`; 13,474 of 13,475 | tool | no |
| C7 | Faces | windows, doors, shopfronts, balconies, burglar bars, stains, AC units, shop signs | the street look close up | every house on a street front has its faces (back houses: *owner's call*) | yes: dress `faces`; 0 placed | tool (Face); stamp | no |
| C8 | Frontages, walls, gates, fences | the plot's edge on the street, its wall and gate | the street edge; gates to enter | every plot edge on a street has a frontage | yes: `frontage`, `wall` (126 gates on 314 walls); 0 frontages | tool (Frontage, Wall, Gate) | yes |
| C9 | Lean-tos, stalls, kiosks, containers | the shade and selling things on the front | markets spill onto the road (DECISIONS) | per 100 m of shop front, against Street View (figure not read yet) | yes: `leanto`, `stall` (10 kinds); 0 lean-tos; 726 stalls, all Mùṣá | tool; stamp; brush could | no |
| C10 | Plots and grounds | compounds, school, church and market grounds, yards | landmarks walled with a gate (the working bar) | every landmark ground drawn and walled | yes: `plot` (12 kinds); 109 | tool | yes |
| C11 | Places in houses | what each building is used for in the game | shops, food, faith, money, missions | 0 real places missing (Overture; the working bar's row) | yes: `place`, `building.place`; 2,589 places, 1,587 houses linked | tool (Place) | no |
| C12 | Kinds the map lacks | hall of residence, faculty block, detached house in a yard (d18 study); house on stilts over water (d19 study); hospital block (owed, d13 study and d13 BUILDINGS.md hand pass 5); estate slab blocks (d13's Royal Estate, nearest kind walkup, *my reading*); factory and warehouse (only `shed`); fuel station canopy | without them the nearest kind is a guess (d18 study's words) | 0 blocks whose study fabric has no kind | **no** | tool, once the kinds exist | yes |
| C13 | Unfinished buildings and scaffolding | houses under build, rebar stubs, scaffolds | half-built houses are common in Lagos (*guess*) | per km² against the satellite (figure not read yet) | **partly**: kind and plot `under_build`, add-on `rebar_stubs`; `scaffold` is "still to add" (MAP-FORMAT.md) | tool | no |
| C14 | Rooftop clutter | water tanks, dishes, masts, generators on roofs | the overhead look. Reference: about 500 rooftop props per 0.16 km² housing box (FINISHED-AREA.md) | per house against the satellite by eye | **partly**: face add-ons (water tank, dish, mast), `furniture` with a height `z`; nothing for a roof's top as such | tool | no |
| C15 | Interiors: which buildings open | the doors the player can go through | shops, homes, missions. Reference: 0-2 interiors per 0.16 km² box (FINISHED-AREA.md) | a list per district of enterable places (*owner's call*) | **partly**: `building.use` (10 set); no interior | table | no |
| C16 | Names | the name of every road, market, school, church, mosque and landmark, as a Gidi sound-alike (DECISIONS "Place names: sound-alikes") | the map players read, the satnav, the conductor's call, missions | every road with a real name has its Gidi name; every place with a real name too | **partly**: `road.name` (0 of 6,816) and `place.name` (1 of 2,589) | table; tool | no |

## D. Services and infrastructure (the owner's "infrastructure" and "civil services")

| # | Layer | What it is | Why the game needs it | Done when | Now | Brush | Lines |
|---|---|---|---|---|---|---|---|
| D1 | Power lines | poles, mains, service drops, transformers | the Lagos skyline of wires; NEPA | poles per km of street against Street View (figure not read yet); Mùṣá 477 poles per Gidi km² | yes: `pole`, `wire`; 579 poles, 360 wires, 12 transformers, all Mùṣá | tool (Wire); brush could (a pole line) | no |
| D2 | Generators | house and shop generators | NEPA off: the whole street's sound and light (LIFE-IN-LAGOS.md section 3) | per frontage from Street View (figure not read yet) | yes: `furniture` kind `generator`; 1 | tool; brush could | no |
| D3 | Street lights | lamps on poles, tall lamp standards on main roads, solar lamps; working or dead | night; safety | lamps per km of road read from Street View (figure not read yet). Reference: City Sample 1,740 lamp posts per km² (FINISHED-AREA-INDUSTRY.md, *not checked* by the main session) | **partly**: `pole.lamp` (steel arm, solar), `lamp_reach`; 182 lamps, Mùṣá; no "working" field | tool | no |
| D4 | Phone masts | lattice towers, monopoles | skyline landmarks | every mast seen on satellite or Street View drawn | yes: `mast`; 15, Mùṣá | tool | no |
| D5 | Water | tanks on stands, boreholes, wells, taps, water sellers | the daily water run | per block from Street View (figure not read yet) | **partly**: `furniture` water_tank, tank_stand; add-on water_tank; activities fetch_water, sell_water; no borehole or well | tool | no |
| D6 | Refuse | bins, dumps, collection points, cart pushers, refuse trucks | the street's dirt and who carries it | every dump seen on satellite or Street View drawn | **partly**: `heap` kind rubbish (12), `furniture` bin (0); no dump-site kind; no refuse truck among vehicle kinds | tool | no |
| D7 | Litter | sachets, bags, bottles on the ground and in drains | the owner named it | pieces per m² of street on a Street View sample (figure not read yet). Reference: about 443 rubbish props in the 0.16 km² housing box (FINISHED-AREA.md) | yes: dress `litter`, gutter `caught`; 0 placed | brush now (litter) | no |
| D8 | Civil services | police stations, fire stations, hospitals, clinics, schools, council offices, courts, post offices; their vehicles (police pickup, fire engine, ambulance) | the owner named them; safe ground (never crime sites, LIFE-IN-LAGOS.md) | 0 missing against Overture and Google Maps inside the outline | **partly**: place kinds police, clinic, school; `pickup.police`; no fire station, hospital, council office, court or post office; no fire engine or ambulance | tool, once the kinds exist | yes |
| D9 | Faith, trade and money places | churches, mosques, markets, bukas, bars, betting, banks, chemists, garages | where people go | 0 real places missing (Overture; the working bar's row) | yes: 18 place kinds | tool (Place) | no |
| D10 | Billboards, adverts, posters | big roadside boards, painted walls, posters, shop signs | the city's loudest look | per km of main road against Street View (figure not read yet) | **partly**: dress `posters`, `faces.signs`, `wall_bays.daubs`, umbrella prints; no big billboard | tool; new kind | no |

## E. Life and time (the owner's "timetable")

| # | Layer | What it is | Why the game needs it | Done when | Now | Brush | Lines |
|---|---|---|---|---|---|---|---|
| E1 | Person spots | where someone does something, how many, at what hours | the people layer; finished means people as dense as objects (FINISHED-AREA.md lesson) | every place, bus stop, lock-up row and junction has its spots (lived-in.md aim); per 100 m of street against Street View (figure not read yet). Reference: 2,188-6,925 activity spots per km² (FINISHED-AREA.md) | yes: `person_spot` (69 activities, hours, count); 0 placed | tool (Person); brush could | no |
| E2 | Day types | weekday, Friday, Saturday, Sunday, Sanitation Saturday, market days | the Jumat crowd and Sunday best only on their days | every spot and place says its days (lived-in.md, `days` proposed) | **no** | table | no |
| E3 | The area's day: how many people and vehicles, by hour | per 2-hour slot, the most people and vehicles and the share by Lagos group | the street fills and empties right | a table per district per slot, shares adding to 100 (lived-in.md "district mix", proposed). Reference: each area in GTA V's files caps people, cars and parked cars per time row (FINISHED-AREA.md) | **no** | table | no |
| E4 | Opening hours | when a place is open | shops shut at night, the beer parlour opens | 100% of places with hours | yes: `place.hours` (text); 7 of 2,589 | tool | no |
| E5 | Who the area is | wealth, how rough, how fast police come, which people live and work here | who is cast; how the street treats the player | every district has them (LIVING.md sheets as a start) | **no**. Reference: each area in GTA V's files carries a roughness level and a police response level (FINISHED-AREA.md) | table | no |
| E6 | Small events | the bus preacher, wedding convoy, drivers' quarrel, accident | surprise on a known street | a first list per district (lived-in.md: 10 for the first district, proposed). Reference: 1-6 event trigger points per 0.16 km² box (FINISHED-AREA.md) | **no** (`moment` proposed) | new tool | no |
| E7 | World states | NEPA off, rain, fuel scarce, task-force raid, street party, market day | the city changes; spots switch on and off | each state lists what it changes (lived-in.md, `state` proposed) | **no** | table | no |
| E8 | Routines | a walk to the borehole, queue, fill, carry home; boarding the danfo | people go somewhere, not only stand | *guess*: a few per district first | **no** (`route` proposed) | new tool | no |
| E9 | Animals | goats, chickens, dogs, rats | street life. Reference: 32 animal points in the 0.16 km² housing box (FINISHED-AREA.md) | per district against Street View (figure not read yet) | **no** | tool, once a kind exists | no |
| E10 | Things that change with the hour | shutters up or down, stalls packed away, umbrellas closed, gates shut at night | night looks different from day. Reference: 1-29 time-switched objects per 0.16 km² box (FINISHED-AREA.md) | every shopfront, stall and gate says its open hours, or follows its place's | **partly**: `open` on shopfronts, umbrellas and gates is one value, not by hour | table | no |
| E11 | Language of an area | what is spoken in each area and by whom: Yoruba, Pidgin, Hausa, Igbo, English | every voice line (the bus preacher, the tout, the trader) is recorded in a language; the area decides which | every district says its languages and shares, by the people kinds of E5 (from the study notes; method *not decided*) | **no** | table | no |
| E12 | Group and vehicle scenes | several people and things that make one scene: a broken-down danfo and its stranded passengers, a wedding party, a street football match | one spot holds a whole moment, not one person (GTA V: scenario clusters and vehicle scenes, GTA-STUDY.md section 5, item 5) | a first list per district (*guess*: a few) | **partly**: `person_spot` has a `count`, so several people can share an activity; no scene that joins people and vehicles | new tool | no |
| E13 | What people wear | the clothes of each area and day: work clothes, school uniforms, Friday and Sunday best, market wrappers | who is cast looks like the area | every district and day type says its dress (from Street View and the study notes) | **partly**: `person_look` gives one person `clothes` and `colours`; nothing says the clothes of an area or a day | table | no |

## F. Sound and light

| # | Layer | What it is | Why the game needs it | Done when | Now | Brush | Lines |
|---|---|---|---|---|---|---|---|
| F1 | Sound zones | market roar, expressway, lagoon, quiet compound | the city is heard before it is seen; sound makes a small map feel big (FINISHED-AREA-INDUSTRY.md) | every part of a district in one zone; by ear. Reference: 2-15 zones centred in a 0.16 km² box (FINISHED-AREA.md) | **no** | brush could (paint zones) | no |
| F2 | Sound at a spot | church and mosque speakers, generators, music shops, touts, welding | the street's voice | every speaker and generator says what it plays and when. Reference: 0-12 fixed emitters per 0.16 km² box (FINISHED-AREA.md) | **partly**: `furniture` speaker and generator, add-on speaker; nothing says what it plays or when | tool | no |
| F3 | Night lights | which windows, shops and lamps are lit; generator-lit or dark; lanterns | night is half the game; NEPA off | per street by eye against real night photos (FINISHED-AREA-INDUSTRY.md topic 11). Reference: 3,362-5,969 far lights per km² (FINISHED-AREA.md) | **no** | table; brush could | no |
| F4 | Air and mood | haze, grill smoke, dust, harmattan, lagoon mist | the look of each area at each hour. Reference: 10-39 mood boxes touch a 0.16 km² box (FINISHED-AREA.md) | every district has its zones (*owner's call*) | **no** | brush could | no |

## G. Story and play

| # | Layer | What it is | Why the game needs it | Done when | Now | Brush | Lines |
|---|---|---|---|---|---|---|---|
| G1 | Story and mission spots | where the story and missions start and happen; safe houses | Tunde's story is layered on the world (DECISIONS "Open world first") | every mission's spots are records (*owner's call*, after the map) | **partly**: place kind `story` and game use `story` exist; 0 placed | tool (Place) | no |
| G2 | Closed areas | areas shut for a mission or a part of the story, without redrawing the map | GTA V shuts roads and areas with switches in its scripts (a restricted-areas script and per-mission switches), not in its map files (STORY-AND-MAP.md section 2) | each closed area has its outline and its reason (*owner's call*) | **no** | new tool (draw an area) | no |
| G3 | Map icons | what the player's map and phone show: places, shops, missions | finding the way | every place kind has its icon (a table, not per place) | **no** | table | no |

**Not map layers** (built in Unreal from the records, so not in this list): far stand-ins, collision, walking and
driving meshes, the frame rate (FINISHED-AREA-INDUSTRY.md topics 13-14). Grass counts and decals vary too much
between areas to be a bar (FINISHED-AREA.md, layer 12).

## The count

**76 layers** (65 in the first draft, 11 added 28 Oct). The format holds **28 yes, 25 partly, 23 no.** **20 layers draw
lines**; the other 56 sit on top of them.

| group | layers | yes | partly | no | draw lines |
|---|---|---|---|---|---|
| A. Ground and roads | 18 | 9 | 5 | 4 | 11 |
| B. Traffic | 12 | 1 | 6 | 5 | 4 |
| C. Buildings | 16 | 11 | 4 | 1 | 4 |
| D. Services and infrastructure | 10 | 5 | 5 | 0 | 1 |
| E. Life and time | 13 | 2 | 3 | 8 | 0 |
| F. Sound and light | 4 | 0 | 1 | 3 | 0 |
| G. Story and play | 3 | 0 | 1 | 2 | 0 |

**The line layers, settled for "working"** (owner, 28 Oct: "what can we do on the list that gets a map to working so
we can have all the district set and not have to start drawing new lines after a district has been made"): A1
streets, A2 widths, A4 lanes (they set the width), A6 kerbs and medians, A7 roadside drains, A8 walkways and verges,
A12 canals, A13 bridges and flyovers with their ramps, A14 shore and jetties, A15 rail and stations, A18 slip lanes,
B1 junction shapes (a roundabout takes land), B7 lay-bys and BRT stations, B8 motor parks, B9 fuel stations, C1
footprints, C8 plot edges, walls and gates, C10 plots and grounds, C12 the missing kinds' footprints, D8 the grounds
of civil services. A district at "working" has every one of these read against Google and drawn; every later layer
only dresses it.

"Yes" is the format, not the data: of the 28, most are empty or placeholder outside Mùṣá, and the whole dress layer
is empty everywhere.

## The format gaps, in one list

1. **Road lanes and direction** (A4): lanes each way, one-way.
2. **Road speed** (A5).
3. **Road markings** (A9): lines, zebras, stop lines, BRT lane.
4. **Speed breakers** as their own kind (A10).
5. **Canals and big drains** (A12).
6. **Bridge structure and footbridges** (A13): piers, rails, an overhead footbridge.
7. **Water lanes and jetties** (A14).
8. **Junctions with a rule** (B1).
9. **Traffic lights**, working or dead (B2).
10. **Traffic signs** (B3).
11. **Moving traffic mix** by road, district and hour, and okada/keke bans (B4).
12. **Transport routes and timetables** (B6).
13. **Bus shelters and lay-bys** (B7); **okada and keke ranks** (B8); **fuel canopies and pumps** (B9).
14. **Building kinds:** hall of residence, faculty block, detached house in a yard, house on stilts over water,
    hospital block, estate slab block, factory or warehouse, fuel canopy (C12).
15. **Scaffold** (C13, already "still to add" in MAP-FORMAT.md).
16. **Roof-top things** placed on a roof (C14).
17. **Interiors / enterable** list (C15).
18. **A lamp's working or dead** (D3).
19. **Boreholes and wells** (D5); **refuse dump sites and refuse trucks** (D6).
20. **Civil-service places and vehicles:** fire station, hospital, council office, court, post office; fire engine,
    ambulance (D8).
21. **Big billboards** (D10).
22. **Days** on spots and places (E2).
23. **District mix by hour** (E3).
24. **Area character:** wealth, roughness, police response, people kinds (E5).
25. **Moments, states, routines** (E6-E8).
26. **Animals** (E9).
27. **Open or shut by hour** for shopfronts, stalls, gates (E10).
28. **Sound zones** and **what a sound source plays** (F1-F2).
29. **Night lights** (F3) and **air/mood zones** (F4).
30. **District height and flood areas** (A17).
31. **Road rules:** turn bans, vehicle bans, slip lanes (A18).
32. **Vehicle spawn spots and no-spawn areas** (B11).
33. **Boats and planes** as vehicle kinds (B12).
34. **Language of an area** (E11).
35. **Scenes** joining people and vehicles (E12).
36. **Clothes per area and day** (E13).
37. **Closed areas** (G2).
38. **Map icons** per place kind (G3).

## What I could not read, and what is not checked

- **No real Lagos figure is read in this note** for: parked cars, poles, lamps, signs, traffic lights, litter,
  person spots, stalls or trees per km or km². Each says "figure not read yet": reading them needs Street View
  samples per district (Chrome), which this job did not do.
- **Google Maps in Lagos:** whether it shows one-way arrows, danfo routes, traffic lights or typical speeds was not
  checked; I did not open Chrome.
- **GTA V figures** are quoted from FINISHED-AREA.md as written. That file says its own scripts area_scan.py,
  zone_box.py and rel_box.py were not re-run by the main session, and that its 12-layer list is the agent's reading. I
  ran nothing in `~/gta5`. The "rubbish props" and "rooftop props" counts come from groups named that way in the game's
  files; what each piece is was not read.
- **City Sample per-km² figures** (lamp posts and the rest) are marked *not checked* in FINISHED-AREA-INDUSTRY.md
  (Epic's page returned 403); UN-Habitat's lines were checked there.
- **Street length:** my figures (27.5-49.5 km per Gidi km²) sum whole centrelines over the outline's area; I did not
  read how `working_bar.py` measures, so the small difference from its 27.5-47.8 is not explained.
- **Building studies:** I read the kind-gap passages of d13, d16, d18 and d19 and searched all seven, not every line;
  d14, d09, d27 and d28 have no study yet (NOW 16 h).
- **"Estate slab block" and "fuel canopy"** as missing kinds are my reading, not a study's call: the d13 study calls
  Royal Estate "estate flats" and maps it to `walkup (flats) in rows`, so the owner may judge walkup enough.
- I did not look at the board in Chrome, so "brush could" is a judgement from `docs/BOARD.md`, not a test.
- How the counts were made: one python -I pass over `map/*/plan.json` and `district.json`, counting record types,
  fields present, kinds, and notes containing "to read"; area with shapely on `district.outline`. Re-run it to check.

## Checked (main session, 27 Oct)

- Re-counted from map/*/*.json by the main session: 13,475 houses, 4,268 (31.7%) with a roof (all Mùṣá), every house
  with kind and storeys; 6,816 roads, none named, 6,445 of the 6,453 outside Mùṣá carrying "to read" in their record;
  2,589 places, 7 with hours; no dress folder under map/; poles 579, wires 360, stalls 726, vehicles 824, trees 92,
  furniture 85, masts 15, heaps 12 (Mùṣá only). As written.
- schema/map_schema.json searched: no field for lane count, speed or one-way; no traffic light or traffic sign record
  (the `sign` record is a sign on a building face, as the note says); no hospital, fire station, borehole, billboard,
  hall of residence, stilt or detached-house kind ("lane" there is a road kind, not a lane count). As written.
- One file name fixed (a range written as one file).
- Not checked: every real-Lagos figure is "not read yet" (Street View samples owed); the GTA reference figures are
  from FINISHED-AREA.md (four of its scripts re-run 27 Oct, three not); the brush column is judged from docs/BOARD.md,
  not tried on the board; the 65 rows' wording and grouping are the agent's, for the owner to go through.

## Added 28 Oct (main session)

The owner asked whether the list was complete and whether it had been read against the GTA findings. It had been
read against one of the three GTA notes only: its sources name `FINISHED-AREA.md`, not `GTA-STUDY.md` (section 5,
"The 15 things Gidi is most likely missing") or `STORY-AND-MAP.md`. Both were read by the main session on 28 Oct, and
the owner's own example (a preacher on a bus, with his voice and language) was set against the rows. Added: A17,
A18, B11, B12, C16, E11, E12, E13 and the new group G (G1-G3). The "Lines" column was added to every row.

Not added, and why:
- **Things the player uses** (ATMs, food sellers): already held. Every one of the 2,589 places carries `uses`
  (game uses: buy, eat, money, fix_vehicle and the rest), counted 28 Oct. Claude had named it missing in chat; it is not.
- **Weather:** already in two rows, rain as a world state (E7) and harmattan and haze as mood (F4).
- **Spawning around the player, far-away crowds, the driving sheet, reactions, budgets** (GTA-STUDY.md section 5,
  items 2, 6, 7, 13, 15): built in Unreal, not held in the map.

Checked (main session, 28 Oct): read three times (owner: "Read over thrice"). First, every row read against the
reason for its Lines mark. Second, a python -I pass over the file: 76 layer rows, every table row 8 cells; per group
yes/partly/no and Lines counted from the rows themselves (the count table above is that output). Third, the new
rows' "Now" column against `schema/map_schema.json` and the map: `road.name` exists (0 of 6,816 filled),
`place.name` (1 of 2,589), `place.uses` (on all 2,589), place kind and game use `story` (0 placed), `relief` is a mm
grid, `person_look` has `clothes` and `colours` per person (this third read corrected the row, which first said
it had no clothes); no field for language, flood, spawn, scene, closed area, icon, boat or
plane (grep). Not checked: the Lines marks are the main session's judgement, for the owner to go through; GTA-STUDY.md's
readings are its own (checked when written, 27 Oct).
