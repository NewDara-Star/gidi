# What the old map taught: still true for the new one

The old generated map (13-21 Oct 2026) is history (`legacy/OLD-MAP.md`; DECISIONS, "The new map is the truth"). Its plans
and pass reports were deleted on 25 Oct (git tag `before-cleanup-25oct` holds them). Before they went, each was read for what still holds for the new map
(real Lagos at 1:3, drawn by hand) and the builders. That is this page. Each lesson names the file it came from, in git
history (`git show before-cleanup-25oct:to-delete/<path>`).

## Real Lagos, measured (facts, not generator rules)

- **The ground** (`docs/terrain.md`): a ridge in the north-west (Ikeja, Agege, Magodo: medians 24-36 m, the highest tenth
  above 40-53 m), a middle ground with medians of 7-8 m (Mushin-Shomolu, Oshodi-Surulere), and a lagoon fringe where half the land or more is under 3 m (Makoko-Iwaya,
  Lagos Island, Apapa, Ikoyi-VI, Lekki, Badagry). Mushin and Oshodi have low creek strips (11-17% of land under 3 m), and
  Ketu-Mile 12 runs down to river lowland (44% under 3 m). Copernicus GLO-30 is a surface model: roofs and trees are in it, so
  the ground is the lowest pixel of each cell of about 90 m, an estimate, not a survey. The new map sits on real Lagos at 1:3,
  so its ground can be the real surface shrunk, without the old map's stretching and 300 m smoothing (which wiped the creek
  strips out).
- **How a Lagos block is built** (`docs/REBUILD-PLAN.md`, `docs/pilot-foodgate.md`): blocks are filled to their edges, deep
  buildings follow the street's line even round bends, gaps are narrow slots, the backs are built over. Real Ketu-Mile 12 in
  500 m squares: 2,608 buildings per km², 38% of the ground built on, 78% of the street front built up, 8.6 m between front
  buildings, 75% touching a neighbour, 23% under 40 m², a typical building 116 m². OpenStreetMap misses half or more of the
  buildings in most places, so it is never the source for counts (Google Open Buildings v3 or Microsoft are).
- **Markets** (`docs/REBUILD-PLAN.md`): Mile 12 is a dense mass of sheds of every size, built onto each other, each cluster at
  its own slight angle, spilling into the streets round it. A grid of stall rows reads as a market in Manchester (the owner's
  words: Ashton-under-Lyne).
- **How Lagos flows** (`docs/FLOW-AUDIT.md`): the mainland middle is joined by the Oshodi-Oworonshoki Expressway (Oshodi to
  Third Mainland); the exits north are the Lagos-Ibadan road at Berger and the Lagos-Abeokuta road at Abule Egba; Apapa reaches
  the north by Apapa Road and the Ijora Causeway; Ebute Metta, Oyingbo, Otto and Costain are the mainland's bridgehead. The old
  map missed each of these and trips ran 1.5-3 times their real length. The new map is on the real roads, so it has them, as
  long as the hand-drawn plan keeps them: a district plan that drops one of these breaks the city's flow.
- **Lagos's oddities as places, not bugs** (`docs/ISMS-BUILD.md`, from `docs/LAGOS-ISMS.md`): streets ending at a canal, drain
  or the rail; two dead ends a wall apart; houses on drain banks; shops, canopies and kiosks in the road's width; markets on the
  carriageway; main roads with a side street every 30 m, a market and bus stops; five-way junctions and acute merges; people
  forced onto expressways (bus stops on them, worn paths on the shoulder, crossings through the median); gates across streets;
  one-way streets; streets laid out before the houses; open gutters with plank and slab crossings (planks for homes in poorer
  places, slabs for shops and gates). In the new map each of these is drawn where its real twin has it.
- **Places the old map found missing** (`docs/ISMS-BUILD.md`, owner 15 Oct): betting shops as common as chemists (small
  kiosks with viewing benches by markets and parks, a few big viewing centres); the airport as its own zone with touts at the
  car park; a walled university with hostels and a bukateria strip at the gate; "hotels" renting rooms by the hour on night
  strips, shown, never explicit, never on safe ground.

## Building the things on the map (for the builders in gidi-game)

From `docs/KIT-GAPS.md`, `docs/road-heights.md`, `docs/junctions.md` and `docs/hand/lagos-pass.md`:
- **A building on a slope needs a plinth or a step:** a block base down to the ground, steps at the door. Standing level on
  the ground under its middle leaves the downhill side floating.
- **Roofs from above:** real roofs are mostly rusted brown and grey zinc, with many flat concrete roofs, often with rebar
  standing up for the next floor; bright new zinc reads wrong. Walls are faded, splashed with red earth at the foot, often bare
  block.
- **Ground is never one colour:** compacted dirt, concrete slabs, sand, puddles, refuse and weeds, by use (yard, roadside,
  market floor, waste ground).
- **Informal bus stops** are the norm: a sign on a pole, a bench or a kiosk, a worn patch, people waiting; the steel shelter is
  for the big roads only.
- **Pole wires** need to know which poles are one run (the map says it: the new map's `wire` records).
- **Decks:** flyovers clear 5.5 m and ramp at about 6.5%; rail bridges clear 6 m; lagoon bridges clear 4 m for canoes, 8 m
  over the ferry channel, and hold their height to the shore before the approach ramp comes down on land. A flyover too short
  to climb is the usual mistake. The road stays at grade beside the ramp as the service road, as at Lagos flyovers, and side
  streets meet the service road, not the ramp. Waterfront roads are walled shores (the Marina, the Bar Beach road). Canals cross
  under roads in culverts level with the road. Stilt-village paths over water are plank boardwalks.
- **Junctions:** Lagos traffic lights stand on poles at the corners, often broken or dark, with an officer's box at the big
  ones; a roundabout's island has a kerb, grass or paving and often a statue or palms. In the new map a junction's kind comes
  from its real twin, not from a rule.
- **What a busy Lagos spot needs to read as Lagos** (the 19 Oct frame against the owner's motor park photo, in order of how
  much each changed the picture): many more people (dozens in the aisles, conductors at open doors), the mess of life (tables,
  plastic chairs, coolers, buckets, nylon bags, trays), wear on the vehicles, dirty ground (oil, puddles, broken pavers,
  gutters with slabs, sand at the edges), real fronts on the buildings (balconies, AC units, signboards, burglary bars, tanks),
  an overcast heavy sky, billboards and street life, a phone photo's lens.

## Unreal and the data (from `docs/UNREAL-PORT-PLAN.md`)

- **Never hand-edit in Unreal what the data owns:** a reimport wipes it. Unreal-only work (light, mission triggers, cutscene
  sets, interiors) goes on its own layers that a reimport never touches.
- **Coordinates:** the map is metres with y south; Unreal is centimetres on its own axes, so the importer scales and flips once.
- **Gameplay data** (safe ground, okada ban zones, checkpoints) becomes volumes or data layers the game logic reads; Unreal
  makes its own navigation mesh.
- **Repeated things are instanced:** export each once (vehicles, people, lights, signs, trees) and place them from the data.
- **The browser tiles are not for Unreal:** merged meshes for a viewer; the importer builds from records.

## Checking (from the old map's checks and living tests)

- **A check that reads only the last line of each report misses failures** (the pilot found a Water Town failure that way). The
  hooks of 24 Oct read every check's exit code.
- **Living tests found what numbers missed:** places you can't reach, absurd detours, everything funnelling onto one road,
  houses with no way in. Cheap agents walking and riding the city between named places, with a standard trip list run after
  every change, showed each fix's cost (a trip 12% longer, a link removed). Worth doing again on the new map once a few
  districts join (IDEAS, "A living test for the new map").
- **Okada bans cut districts off:** in the old map the okada could not legally reach the Frontier because its only road ran
  through a ban zone. In the new map the ban follows real Lagos (inner councils, `docs/lagos-study/LIVING.md`), and every
  outer place must still be reachable by okada without crossing one.
