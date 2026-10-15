# Kit gaps: things the map now has that the 3D kit can't draw well yet

Started 15 Oct 2026 with the Food Gate pilot (`docs/REBUILD-PLAN.md`). Each line: what the data has, what the kit does today, and what it needs. Newest first within each group.

## Buildings
- **Extensions and back rooms built onto a house.** *(First version done: kind `extension`, `archetypes.extension`: one storey, a lean-to or a flat slab.)* The pilot's infill (`scripts/gen_fabric.py`, the Lagos fabric) adds rooms of 8–170 m² that touch the house beside them, as real Lagos does. They're stored as `back` (or `shed` under 15 m²), so the kit draws each one as a separate little house with its own full roof. The kit needs an **extension**: one storey against its neighbour's wall, a lean-to or flat roof, often unplastered blockwork, and a door into the yard.
- **Buildings on a slope.** With `--terrain`, every building stands level on the ground under its middle, so on a slope its downhill side floats a little (Food Gate falls about 2% west to east, about 20 cm under a 10 m house). The kit needs a **plinth or step**: a block base down to the ground, and steps at the door.
- **Roofs.** Seen from above, Food Gate is nearly all bright, new, pitched zinc in red, blue and green. Real Ketu and Mile 12 roofs are mostly rusted brown and grey zinc, with many flat concrete roofs, often with rebar sticking up for the next floor. The kit needs a **roof mix by district** (share of rust, flat concrete, rebar stubs), weighted to old and worn.
- **Paint.** The pastel walls read clean and new. Lagos walls are faded, stained by rain splash at the base, and often bare block. The kit needs more **wear and bare blockwork**.

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
