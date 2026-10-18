# Kit gaps: things the map now has that the 3D kit can't draw well yet

Started 15 Oct 2026 with the Food Gate pilot (`docs/REBUILD-PLAN.md`). Each line: what the data has, what the kit does today, and what it needs. Newest first within each group.

## Buildings
- **Extensions and back rooms built onto a house.** *(First version done: kind `extension`, `archetypes.extension`: one storey, a lean-to or a flat slab.)* The pilot's infill (`scripts/gen_fabric.py`, the Lagos fabric) adds rooms of 8–170 m² that touch the house beside them, as real Lagos does. They're stored as `back` (or `shed` under 15 m²), so the kit draws each one as a separate little house with its own full roof. The kit needs an **extension**: one storey against its neighbour's wall, a lean-to or flat roof, often unplastered blockwork, and a door into the yard.
- **Buildings on a slope.** With `--terrain`, every building stands level on the ground under its middle, so on a slope its downhill side floats a little (Food Gate falls about 2% west to east, about 20 cm under a 10 m house). The kit needs a **plinth or step**: a block base down to the ground, and steps at the door.
- **Paint.** The pastel walls read clean and new. Lagos walls are faded, stained by rain splash at the base, and often bare block. The kit needs more **wear and bare blockwork**. *(First version done 18 Oct: `gidi_kit/wear.py`. All of it is vertex colour and geometry, since Unreal shows the vertex colour alone: red earth up the foot, paint faded in patches, grime from sills, ledges, balconies and parapets, rust from the bars, cement patches, render broken to the block, AC units with their drip (only where the data counts them: a house field `ac` the data doesn't have yet), the meter box and cable where the data's service drop lands. Still missing: a fine texture (plaster grain, hairline cracks) that vertex colour can't carry; that needs Unreal's master material to read the wear in the vertex alpha.)*
- **Roofs.** Seen from above, Food Gate is nearly all bright, new, pitched zinc in red, blue and green. Real Ketu and Mile 12 roofs are mostly rusted brown and grey zinc, with many flat concrete roofs, often with rebar sticking up for the next floor. The kit needs a **roof mix by district** (share of rust, flat concrete, rebar stubs), weighted to old and worn. *(Zinc done 18 Oct: `gidi_kit/zinc.py` lays every zinc roof sheet by sheet in the web tiles too: each sheet its own colour, rust worst at the eave, a new sheet now and then, laps, sag on old roofs, rust run down from the nail lines and lapped edges; no rib geometry in the web tiles (Unreal adds corrugation on 'zinc' faces). Flat concrete roofs darken along the parapet with ponding marks. The mix itself (rust share, flat share) already comes from the data and the districts' looks.)*

## Ground
- **One colour everywhere.** All open ground is the same laterite orange. Real yards and roadsides mix compacted dirt, concrete slabs, sand, puddles, refuse and patches of weed. The kit needs **ground cover by use**: yard, roadside, market floor, waste ground.

## The market
- **Market sheds of every size.** *(First version done: stalls over 40 m² use `archetypes.market_shed`, with posts, one roof or two slopes, tarps and goods.)* The pilot market is clusters of sheds from 8 to 400 m², built onto each other, each cluster at its own slight angle (Mile 12 from Google's outlines). They're stored as `stalls`, and the kit draws each as its lock-up row (a row of four shuttered stalls under one roof), which looks wrong at 300 m² and at 10 m². The kit needs a **market shed**:
  - zinc roofs on timber or steel posts, open sides, tarpaulins
  - goods in heaps and baskets underneath
  - a sheet roof that runs on across neighbouring sheds
- **Market spill on the walkways.** Tables, umbrellas, wheelbarrow displays and mats of goods, in the declared zones (`encroach` in the data). They're stored as small `stalls`. The kit needs **street stalls**: tables, big umbrellas, wheelbarrows, mats.

## Street furniture (now placed by the data, `furniture`)
- **Wires along the poles.** The kit used to hang wires pole to pole along the street it was placing poles on. The data places the poles now, so the pole-to-pole wires are gone (service drops to houses remain). Either the data says which poles are in one run, or the kit links each pole to the next one along the same street.
- **Bus stops.** Lagos bus stops are mostly informal: a sign on a pole, a lay-by, people waiting, a conductor shouting. The kit's steel shelter fits the big roads. The kit needs an **informal stop** as well: a sign, a bench or a kiosk, a worn patch.
- **Traffic lights:** drawn from the data at every signalled junction (four per junction). The kit's light is fine.
- **LASMA posts:** the data places one at each signalled junction (`furniture`, kind `lasma post`). The kit has no builder yet. It needs the traffic wardens' booth: a small yellow-and-green kiosk, or an umbrella and a stand, often with a warden.

## Roads
- **Road widths from the data.** The kit now reads `cross_sections` for districts built to them (the pilot). The other districts still use the kit's own widths (a 7 m street) until they're rebuilt.

## New in the v2 layout (16 Oct 2026)
- **The airfield.** The Airport reserves a fenced airfield, about 1.6 km by 370 m, stored as a reserve of kind `airfield` with nothing built on it. The kit needs:
  - a runway (a hand-placing job first: the line, the markings, the lights)
  - taxiways and an apron
  - grass behind a security fence
- **The airport terminal.** For now it's stored as a `bus terminal` reserve with a two-storey `terminal` building, a stand-in. The kit needs a **terminal**: a long hall, a forecourt and drop-off lane, a car park, a control tower nearby.
- **The campus.** Saba's Lagoon University is a reserved `campus` with a ring road and nothing inside yet. The kit needs **campus buildings**: lecture halls, hostels, a senate building, sports fields, by hand.
- **The Gold Island's causeway gate** (after Banana Island). A gatehouse and barrier where the causeway meets the Heights' shore.
- **Face-me-I-face-you** (kind `face-me`, the Maze: Tunde's block). *(First version done 16 Oct: `archetypes.face_me`: the corridor doors at each end, the front one open; five small barred windows a side; a low rusted gable roof. Behind it are the toilet and bathroom block, the kitchen corner with soot, washing lines and the generator in its cage; a bench and chairs at the door.)* One storey, about 22 by 9.5 m, a corridor down the middle with five rooms a side, a shared toilet and kitchen at the back, washing lines, a bench at the door.
- **People placed by hand on the walkways** (furniture kinds `wheelbarrow vendor`, `fruit seller`, `parking boy`: the Maze's approach to Ladi Lane). *(First version done 16 Oct: `street.wheelbarrow_vendor`, `street.fruit_seller`, `street.parking_boy`.)* The kit needs:
  - a wheelbarrow of phone cases and chargers, with a man in an earpiece
  - a fruit tray table
  - a parking boy's plastic chair and ticket book
- **The motor park's office** (kind `office`, the Hub: the boss's office; the first cutscene, confirmed by the owner 16 Oct). *(First version done 16 Oct: `archetypes.park_office`, for an `office` of one storey under 60 m²; bigger offices stay office blocks. It is a zinc-walled shed on a block base with the door open on its padlock. The inside is modelled for the cutscene: the desk, ledger and cash box, an office chair and two plastic chairs, the standing fan, a bare bulb, the peeling calendar, and the TV on a stool.)* Dingy and makeshift: a converted shipping container or a zinc-walled shed, a painted union sign, a bench and a water drum outside. Inside: a desk with the ledger, plastic chairs, a standing fan that rattles, a bare bulb, a peeling church calendar, a padlock on the door.
- **Agberos** (furniture kind `agbero`): a man with a ticket book and a whip of notes, standing at the gate. *(First version done 16 Oct: `street.agbero`, in three poses: `collect`, `count` and `wave`.)*
- **The buka** (kind `buka`, the Maze: Flyover Buka): a lean-to kitchen, pots on a coal fire, benches. *(First version done 16 Oct: `archetypes.buka`, named from the food place on it.)*
- **Police kiosk** (furniture `police kiosk`): a small red-and-white booth at a bus stop. *(First version done 16 Oct: `roadside.police_kiosk`.)*
- **Overhead direction sign** (furniture `overhead sign`): a green gantry across an arterial. *(Done 16 Oct: `city.py` finds the road it spans and puts the kit's gantry across it, naming where the road goes and the road itself.)*
- **Task force truck** (furniture `task force truck`): a pickup with seized okadas in the back, parked at a junction. *(First version done 16 Oct: `vehicles.task_force_truck`, parked along the road beside it.)*
- **Rail market** (zone `rail market`, the Hub): traders' tables on the ballast beside the tracks, lifted when a train comes. *(First version done 16 Oct: `street.rail_market`, one pitch every 1.9 m in the zone, kept 2.4 m off the track. The zone is one object named `rail market`, so it can be cleared as a group. The browser tiles still merge it with the rest of the tile.)*
- **Ladi Lane's lock-ups, open** (the chase line). *(Done 16 Oct: `archetypes.lockup_open`. The small stalls along the aisle of the `Ladi Lane` story place stand open, with their shutters rolled up and goods stacked to the roof: engine parts, tyres, phone boxes or bolts of fabric. Tarpaulin awnings reach over the aisle, and crates and trolleys stand in front.)*
- **The Glasshouse** (kind `mall`, Marigold Junction in the Capital, after the Maryland mall): a black-glass box, three storeys, a car park in front, signage on the glass.
- **Bread hawker** (furniture `bread hawker`, Railside's Ayo Bakery Row, after Agege): a wheelbarrow or head tray of loaves in nylon, a hawker calling out. *(First version done 16 Oct: `street.bread_hawker`, both versions, chosen per hawker.)*
