# Where the work stands (update at the end of every session)

**HANDOVER, 25 Oct 2026. Start here.** Read `DECISIONS.md` (the standing rules; replaced ones are in `HISTORY.md`),
then this page. What the repos hold: `CODEBASE.md` and `docs/inventory/` (`scripts/inventory.py`). The real Lagos research:
`docs/RESEARCH.md`. What the old map taught: `docs/OLD-MAP-LESSONS.md`. This page's dated log and done lists (22-25 Oct)
are in `HISTORY.md`, word for word; what they still owed is in the running order and the Owed list below.

**Running order** (owner, 25 Oct: "keep a running order". Work down it without asking "next?"; tick an item when it is
merged and checked, add new ones where they belong, and say here when the owner reorders it).
000. [ ] **The network to a drive, first (owner, 28 Oct, DECISIONS "The whole network first, to a drive in Unreal"):**
   (a) [x] Third Mainland Bridge, [x] Ikorodu Road (abcaf53); (b) [ ] the other main roads in d00 from
   `scripts/city_network.py`'s list, longest first (the expressways, Herbert Macaulay, Murtala Muhammed, Western and
   Eastern Avenue, Funsho Williams, Apapa road, Lagos-Badagry, Lekki-Epe; the bridges Eko and Carter; Fourth Mainland
   and Lekki Regional as being built), every junction a shared point and named in its record for the real place it stands for and the district it lands in, so a district's streets know where they meet the network when it is remade (owner, 28 Oct: "we need to be able to match them to the actual spot in the districts, so we can add them slip roads and streets"); slip roads and ramps drawn with their main road at real length (DECISIONS "1:3 sets where things are"); (b1) [ ] the main roads drafted into d00 (`scripts/draft_network.py`, 28 Oct: 137 roads, 184 Gidi km; neatnet merge, 1:3, widths a default by kind "not read"; interchange leftovers taken off; check_map passes after 4 hand fixes, listed in the commit). By hand still: [x] its ends cut back from Third Mainland and Ikorodu Road joined to them (18, flat, read with the crossings; the network is then 6 pieces, the biggest 187.4 of 201.4 km and the whole frame wide; the others: Idi-Iroko road in the north-west corner, 12.2 km, joined only outside the frame, and four bits of 0.1 to 0.9 km at Lekki, the Eko end and the east edge, to read); [x] its 21 crossings and its 17 spots joined to the hand roads read on Google satellite (28 Oct; `~/gidi-data/research/twins/crossings-read.tsv`): 18 flyovers, 8 slip roads, 3 forks at a ramp's foot, 4 flat junctions (1 not seen), 2 the same road meeting itself, 3 on the unbuilt Fourth Mainland; [ ] the 15 interchanges they belong to drawn by hand with their decks' heights and slip roads at real length, biggest first: Ojota, Jibowu, Maryland, Oshodi, Oworonshoki, Third Mainland's Lagos Island end, the Lagos Island cloverleaf, Osborne, Ijora (Apapa Road), Ijora (Badagry Expressway), Tin Can, Iyana-Ipaja, and the Fourth Mainland's ends when its design is read; [ ] its 34 loose ends read (a real end or a gap); [ ] Badagry's and Lekki's carriageways left as two lines; [ ] each road's width read, longest first; [ ] the junction place names read (nearest frame-study place today). The Fourth Mainland Bridge and the coastal road kept (owner, 28 Oct), the bridge as being built; (c) [ ] rail into d00 (PR #453 waits for the
   owner); (d) [ ] water into d00; (e) [ ] gidi-game builds d00 alone on the land (relief grids as one Landscape,
   roads from road_build) with a car to drive; (f) [ ] the owner drives it. District work waits except what a piece
   forces; clashes with district work are listed by check_map (CLASH), not fixed (DECISIONS "Clashes with district
   work are listed"). Owed: [ ] the board shows the CLASH list (today it shows check_map's failures only, not
   looked at for clashes); [ ] research on how studios build a city from a real place
   (~/gidi-data/research/OPEN-WORLD-CITY-METHOD.md, agent running 28 Oct) read and checked, and this order changed
   if it shows a better way.
00. [x] **Clean-up first (owner, 25 Oct evening, DECISIONS "Delete what we no longer use"):** run scripts/inventory.py,
   read it in two passes (what each part is; then what it does and whether anything live uses it), then delete in
   both repos what is no longer used or true: dead code and tools, wrappers that repeat an engine feature, old logs and
   dated notes whose lesson is written down, `legacy/` and the old map's Unreal side if nothing live needs them; NOW.md
   and DECISIONS.md trimmed to what is current. Each deletion a commit saying what went and why, checks run.
   Steps (git tag `before-cleanup-25oct` on main keeps every deleted file):
   - [x] step 1: `to-delete/` deleted (gidi, branch clean/to-delete).
   - [x] step 2: the old generated map and kit deleted (284 files: old scripts, `legacy/`, old web files, study-*.json).
   - [x] step 3 (gidi-game #96): the street and underdeck levels no longer borrow from the old importer (masters and import
     settings in `gidi_surfaces`, sky in `gidi_look`, hero state in `gidi_heroes`); the importer, streaming, signs, check
     camera, Ìbùdó level and photo mode deleted with their tools and generated levels; default map Play_Street;
     `tools/plates.py` reads `web/frame-study.js`; this repo's `web/city/` (3.7 GB, untracked) deleted.
   - [x] step 3a (gidi-game #97): tB measured again: GPU 13.9/13.8 ms (was 15.2/14.7), memory 5,987/6,000 MB, same
     picture (0.07% of pixels); why the GPU is ~1 ms lower is not found.
   - [x] step 3b: the second reading of the inventory. gidi-game #98, #99: dead names out of the builders,
     `frame_motorpark.py` deleted, `props_build.py` and `prop_basin_final.py` kept as live recipes. Here: dead names out
     of `frame_study.py`, `frame_footprints.py` and the roads and similarity study scripts; the old map pictures nothing
     pointed to (v0.3, the v1 terrain, the v2 layout) deleted; the research docs kept (`docs/RESEARCH.md` maps each to
     the new districts). gidi-data: the old kit's part viewer deleted (local commit; it has no remote). Untracked: the
     old test streets' levels and folders (5.6 GB), Saved/Shots, StagedBuilds and Cooked (4.1 GB), logs before 25 Oct,
     the old perf files, this repo's SUMO-era `.venv/` and `study-*.pkl` caches (684 MB).
   - [x] step 4: docs that name deleted files. Live docs fixed line by line (BOARD.md rewritten for today's board,
     CODEBASE rewritten for the new layout, gidi-game PERFORMANCE's "what is on" (#100), MAP-FORMAT's board and import parts,
     the `?frame=new` mentions); history docs carry a note at their top; `scripts/inventory.py` now counts the names not
     marked as gone: 1 left, the output file `appendix.py` writes (not a pointer).
   - [x] step 4b: NOW.md's dated log, done lists and old "Next, in order" moved to `HISTORY.md` word for word, each
     "next" in them that was still open carried into item 10, the Owed list or Parked; three replaced decisions moved
     out of DECISIONS (the browser 3D preview, "Claude decides", "Build order: outward from the Maze") and three given
     a *Now:* note. Rules that still have a GAP row stay, so no GAP is closed by moving it.
   Then item 0(b) widened: every kit (all the builders, not only stalls) as shared pieces drawn as instances.
01. [x] **The fighter's camera looked straight down (owner, 25 Oct: "it's never showing like over the shoulder").**
   Fixed (gidi-game #102). Cause: on the Mac the first mouse event after the mouse-look mapping is added carries the
   cursor's distance from the screen corner as one move (start pitch -89.9 with the cursor low, -52.5 with it high;
   yaw likewise off), SDL's known macOS bug. `gidi_player.py` makes BP_GidiPlayerController (the Combat one, holding
   the PlayerStart's direction at pitch -10 for the first second) and BP_GidiGameMode; both play levels use it. After:
   first frame -10/11.18 on the street, -10/90 under the deck, mouse look and W move checked. The measure levels keep
   their fixed Cam_Measure (30 m up), so the measuring pictures stay overhead on purpose.
1. [x] Road lines: 54 of the 62 corners in d15 hand-edited (gidi #332, #333): 12 repeated points dropped, 14
   doubling-back places cut (in 9 roads), 28 tight corners smoothed. The 8 left turn on junction nodes (check_map
   lists them) and go to item 2.
03. [ ] **Map and brush first; Unreal on hold (owner, 26 Oct, DECISIONS "Map and brush first, Unreal on hold"; they
   may take it back):** the work is the map on the board in Chrome until every district is complete: Mùṣá to working
   (item 10), then the other districts to working, breadth-first (item 11); polish after (the look pass). The Unreal items wait
   (02(a1)-(a3) and (c), 0, 2-8): kept here, not worked, until the owner says.
02. [ ] **Working first (owner, 26 Oct, DECISIONS "Working first, polish later"):** (a) [x] the inventory of what is to be
   modelled: `docs/MODEL-INVENTORY.md`, written by `scripts/model_inventory.py --write` from the map, the schema, the
   builders and the street test. Of the 40 kinds on the map: 18 working in Unreal; 13 built but not placed (roads: 0(c);
   furniture: (a1)); pickup built with a stand-in still in Unreal (0(b2)); no builder for suv (0(b2)), tree palm and shade,
   mast, heap (item 3), rail and station (a2); container_shop not in stall_build (a3). (a1) [ ] furniture placed in the
   street test; (a2) [ ] rail and station builders, simple; (a3) [ ] the container shop (a container on blocks).
   (b) the map completed (item 10, on the board in Chrome); (c) the game working on it (items 0(b2)-(d), 6). Model look
   passes (0(b1a) and the like) wait.
0. [ ] **Pieces as instances, first (owner, 25 Oct, DECISIONS "Pieces placed as instances"):** the audit found
   only block_build splits pieces (windows and doors, as one actor each, not instances) and 97% of a test house's
   triangles are its own roof sheets (46,308 of 47,631); the 25 Oct "Kits into pieces" never reached this list.
   (a) [x] Done 25 Oct (gidi-game #90): the street (475 houses now) with roof edges as 19 shared pieces and every
   piece instanced, measured against a same-day build of main: files 900 -> 373 MB, actors 10,436 -> 1,183, but
   frame 60 fps in both, GPU 16.2 -> 15.7 ms, process memory 7,156 vs 7,193 MB. The files shrink; the memory is not
   the houses' triangles (Nanite streams them). So, reordered: (a2) [x] what fills it (gidi-game #91): an empty copy of
   the level uses 5.8 GB with no houses, nine tenths graphics pools of fixed size (Metal heaps 3.1 GB, 1.3-1.4 of them
   unused; Nanite/scene buffers 0.9; render targets 0.5; UAV textures 0.44); the 475 houses add ~0.8 GB; no leak over
   5 min; the measure's CSV profiler adds ~0.5 GB of its own. Next, one at a time: (a3) [x] the packaged game (gidi-game #92,
   tools/package.sh): empty 4,231 MB, street ~4,535 (editor 5,850 / 6,666), so the houses cost a player ~0.3 GB and
   ~3.5 GB of fixed graphics memory is the floor; (a4) [x] the fixed pools, one at a time in the packaged game
   (gidi-game perf/pools, PERFORMANCE.md "The fixed pools"): shadow pool 1024 pages and Nanite pool 256 MB together
   free ~0.55 GB on the street with no change seen from the lane's camera, either alone ~0; texture pool, Lumen and the
   two Metal heap settings 0; clouds off 192 MB. No default changed; (a5) [x] the roof edge pieces' faults (gidi-game #94): close up there were three, all
   fixed in zinc_kit: sheets a hip cuts keep their modelled strip (1,616 of 23,556); pieces whole ribs wide, so laps
   nest (20,586 laps within 0.052 rib, tools/lap_check.py; slits before); each piece turned to meet the sheet's 5-7 mm
   belly and sag. Seen in Blender only; (b) each builder split in turn, for the files,
   actors and World Partition (its first street in Unreal also shows the new edge pieces, not yet seen there).
   Progress 25 Oct (gidi-game kit/stall-pieces): plain stalls and umbrellas as 3 shared pieces (street_test --things
   --thing-pieces): 117 things 126 -> 24 actors, 118 -> 4 meshes, frame and GPU the same, memory ~0.12 GB lower (a hint).
   Poles done (gidi-game #101): d15's 579 poles are 4 shapes, each one shared piece, the wires the pole's own mesh, the
  lean now a rotation (an instance has no shear); whole vs piece in Blender 0-5 of 480,000 pixels; 58 poles in Unreal
  67 -> 49 actors, 59 -> 41 meshes, frame, GPU and memory the same (PERFORMANCE.md "Poles as pieces").
  Vehicles placed from shared models (gidi-game kit/vehicle-instances, PERFORMANCE.md "Vehicles as instances"): the
  street test's 53 (200 m) from the built heroes (danfo, keke, okada, lorry, molue for the buses) in their condition's
  paint with their own plates, City Sample cars standing in for saloon, suv and pickup; as instances 62 -> 40 actors,
  frame and memory no different measurably; the plate material prints on instances (v5), the paint has a copy for
  instances. The cost is the stand-ins: 27 City Sample cars ~2.4 ms GPU and 1.3 GB (60 -> 55 fps), the 26 built ones
  0.37 M triangles. So next, before stalls: (b1) [x] our own saloon (601 in d15), built the danfo's way (gidi-game
  #104, merged; `tools/saloon_build.py`: Corolla, Camry, Accord, nine recipes, opaque glass, M_GidiPaint, _static
  25-28.5 k faces; schema `vehicle.saloon` here): 25 saloons on the street test GPU 15.0-15.8 -> 13.0-13.1 ms, 7.4 ->
  6.2 GB, 41.8 -> 3.8 M triangles (PERFORMANCE.md "Our own saloon"). Saloon owed: (b1a) [ ] a close look in Unreal (only
  the raised camera so far) and photo passes against ot162 and the other saloon photos (ot122, ot149, ot175, ot198,
  ot73); on a red body the tail lamps blend into the paint; the mirrors are blobby; a dark notch at the top of the rear
  quarter (C-pillar); the Corolla's quarter glass and the Accord's door_FR cut by the FLOAT fallback (clean by eye);
  thin fins in the body at the windscreen's lower corners by the mirrors (three trials did not move them). Pass 1 done
  (gidi-game saloon-pass1: mirror, wipers, tail lamps off the wing top); the rest waits (item 02).
  (b2) [ ] suv and pickup (pickup_build exports no _static.glb yet; brt_build none either), replacing the last stand-ins. Then stalls
   with goods/posters and printed umbrellas; (c) roads as simple shapes with tiling textures and decals; (d) World Partition in
   place of our tile streaming; on that city, decide the shadow and Nanite pool sizes (smaller saves ~0.55 GB, PERFORMANCE.md;
   check over the roofs and down a long street for overflow) and whether the volumetric clouds stay (192 MB and the
   largest GPU pass over the roofs, 8.5 ms) or become a cheaper sky.
2. [ ] Junctions: research how road tools build them, then a junction piece where roads meet, the roads cut back to
   it (and the 8 corners check_map still lists, all on junction nodes). Roads that meet now share a point (#335);
   the kit must also join the 50 staggered junctions check_map counts (two nodes a few metres apart, inside each
   other's road) into one junction each; tested on a T and a crossroads against photos.
   Progress 25 Oct: duplicate roads cut back (#336); gidi-game #89 merged: `tools/junction_geo.py` (each junction's
   shape from the roads, staggered ones grouped; `--check`: 554 junctions, 553 patches valid, cuts median 5.66 m),
   `tools/junction_build.py` (the patch and the drains turning its corners), and map_build now lays each road as
   stretches between junctions (the 3 seams in one test box: steps median 0.000 m, max 0.005, one point at
   -0.048 not yet traced). Left: the motorway merge at 13294,6305 (70 m2 over a house,
   a 115k-face patch); the one invalid patch (12547.9,6070.6, a corner on check_map's list); the T and crossroads
   against photos; the box with houses (block_build fails on an L-shaped pitched roof there: item 5); the -0.048 point.
3. [ ] Trees, masts, heaps (92, 15 and 12 records in d15) and weeds: builders tested against photos; Meshy for the hard
   shapes before the credits expire on 11 Nov (cost stated first).
4. [ ] Ground: the road and verge colours (grey dusty tar, not tan or black), sand and earth as the map paints them.
5. [ ] Houses read their records' storeys and kind.
6. [ ] Mùṣá in Unreal (after the owner restarts the Mac): the overhead against Google Earth's Mushin, street views
   against Street View.
7. [ ] Lighter Gidi people (one skinned mesh, no grooms) so low and high carry a crowd again (gidi-game
   docs/PERFORMANCE.md, "the next step" since 24 Oct); through Mass with detail by distance.
8. [ ] Owed checks: a new check (a script in scripts/, not written yet) that every "next" / "to come" / "own commit" written in a commit since
   25 Oct is cited on this page, run at stop; then the per-level budget check (CHECKS.md GAP); the other 35 GAP rows
   in CHECKS.md are each a check still owed, worked through after Mùṣá.
9. [x] Clean-up from the inventory (25 Oct): folded into item 00 (`legacy/` deleted 25 Oct; the old map's Unreal side,
   its importer and streaming, Gidi_City and Play_Ibudo, deleted in 00 step 3, gidi-game #96).
10. [x] Mùṣá to "working" (DECISIONS "Every district to working first", owner 26 Oct). Drawn so far, hand passes 1-58 in
   BUILDINGS.md: roads at read widths, houses with kinds and storeys, 516 Overture places in their houses, bus stops,
   the Jibowu coach yard, the market, the two schools and the factory with walls and gates, the rail and station
   platforms, the danfo park at the Agege Motor Road / Isolo Road junction (hand pass 59), check and board at 0
   problems; Olushoga's zigzag and the Omowunmi kink measured on their real lines (pass 59, no change). Western Avenue's side road (hand pass 60). Isolo Road's bridge over the expressway (hand pass 61). The station hall (hand pass 62). Called at the bar on 26 Oct too soon: the bar check (scripts/working_bar.py, item
   11) then found 37 real places with no place near (6 inside drawn grounds, 3 roadside, 28 to place: hand pass 63) and LUTH's campus
   with no wall or gates (owed since hand pass 4). Both done in hand pass 63: working_bar.py d15 PASS (0 real places
   missing of 421, 4 plots all walled and gated), check at 0, 26 Oct. Everything else
   that was owed here moved to the look pass in the Owed list.
16. [ ] **Working means it matches the real place (owner, 27 Oct; CLAUDE.md "Google first" and "Working means it
   matches").** Comes before item 11's next district. Measured 27 Oct, building cover inside each outline, ours vs
   Google Open Buildings v3 (confidence 0.65 / 0.7 / 0.75): Mùṣá 43.2% vs 47.7 / 45.9 / 43.2; Ìbùdó Mẹ́ta 11.4% vs
   30.5 / 29.0 / 26.4; Saba 14.4% vs 31.5 / 30.5 / 29.1; Makoro 13.1% vs 44.9 / 40.9 / 34.9; Sọ̀rọ̀lérè 15.1% vs
   37.1 / 35.7 / 33.6 (Mùṣá to two decimals: 43.22% vs 47.67 / 45.92 / 43.19). Mùṣá is near Google's figures, the
   other four are at a third to a half; by the band in (a), Mùṣá fails by 0.04 points (43.22%
   against 43.26-47.65%) and Ìbùdó Mẹ́ta at 11.39% against 26.49-30.45%; the other nine are not run against it yet
   (item 16 d brings them up). Mùṣá's item 10 tick stands for the bar of 26 Oct, not this one. Street length (ours vs Overture's network, per real km²): ours is 2.1x
   (Mùṣá) to 3.7x (Saba) the real figure, so our blocks are smaller than real and roads take more of the land; read
   against Google Maps before it is gated (Overture is OpenStreetMap's network, thin in Lagos).
   (a) [x] `scripts/working_bar.py`: a DENSITY row (cover between Google's figures at Lagos's 90%- and 80%-precision
       thresholds, from Google's per-tile threshold file: a download, the owner asked first; the blocks furthest
       below listed; street length printed, not gated yet), and its CHECKS.md row.
   (b) [ ] `scripts/draft_buildings.py` drafts from Google Open Buildings v3 (owner asked, 27 Oct: "Should you switch
       the house drafting to Google's data? Please do that"), Microsoft only where Google has no house; the
       industry-standard read first (Google's own guidance on confidence thresholds), said in the commit.
   (c) [ ] What "done" means, researched before it is written (owner, 27 Oct: "research, look at the map, look at our
       district... look at GTA, look at the code in GTA, see what done means according to their definition, then both
       of us will come and talk about it"): agents read (1) GTA V's own files for what a finished block holds per
       km² (placed objects, scenario spots, traffic lanes, population zones, sound zones), (2) how studios and the
       engine's makers define a finished open-world area, (3) Mùṣá against both; Claude checks every claim; then the
       owner and Claude agree the list. Every topic gets how it is measured. Mùṣá is not done until each passes.
       "Working" is re-read against it. **Owner, 27 Oct: map done is now the bar for every district** (DECISIONS
       "Done is the map's bar"). The draft list is written and its counts checked: docs/research/MAP-DONE-LAYERS.md
       (65 layers in six groups; the format holds 28, partly 20, not 17; 29 format gaps). Next: the owner and Claude
       go through the 65 layers, cut and change them, then each agreed layer gets its measure and its row in a check.
       28 Oct, owner "yes": 11 layers added (A17, A18, B11, B12, C16, E11-E13, G1-G3, from GTA-STUDY.md section 5,
       STORY-AND-MAP.md and the owner's preacher example) and a Lines mark on every row: 76 layers, 20 draw lines,
       which "working" settles first. Next: the owner listens through the 76 and cuts or changes them; each new record
       kind gets a test spot in Unreal (DECISIONS "One test spot", 28 Oct).
       In progress (28 Oct, owner: working means every line settled, DECISIONS "Every district to working", changed
       28 Oct): the line sweep, three helpers (GTA V's files, industry and planning standards, our own repos and
       studies), then further rounds until one finds almost nothing new; each finding checked; then the line rows
       go into working_bar.py (CHECKS GAP). Round one done and checked in part (28 Oct): 15 candidates merged at the
       end of MAP-DONE-LAYERS.md (two Lines marks to change, A17 and C3; nine new rows; four rows widened), with
       what was and was not checked in ~/gidi-data/research/LINE-LAYERS-CHECKED.md. Next: the owner goes through
       the 15; round two by a fresh helper; the unchecked claims checked before their row goes in.
   (d) [ ] The 11 districts drawn so far (d09, d12-d19, d27, d28) re-measured and brought to the DENSITY row by hand:
       one agent per district reads it in Chrome (Google Maps, satellite at z17-18, Street View) and proposes fixes
       with evidence; Claude checks every claim and makes the edits, one editor per district at a time.
   (f) [ ] Our streets are 2.1-3.7x as dense per km² as the real ones (roads at full width on a 1:3 map), so blocks
       come out small and roads take the land. A creative call for the owner, options with numbers first (how GTA V
       shrank Los Angeles while keeping road widths, read from its files and talks; what share of land roads take in
       real Lagos, in Mùṣá and in GTA's Los Santos).
       **Decided by the owner, 27 Oct (DECISIONS "Streets by the ratio"):** roads keep their full width; the number of
       streets follows the scale, so a district's street km per km² matches the real one, picked by hand from a study
       of the whole district that keeps its defining streets. Owed: (1) each district's real street km per km² read
       from Google Maps (Overture is thin), (2) a street-density row in working_bar.py once (1) gives a figure to
       match, (3) the drawn districts' streets thinned by hand to it, defining streets first. No dropped street turns
       into a footpath (DECISIONS "No forced footpaths"). Order per district (DECISIONS "Study the district first"):
       several checked study passes wide and close; a 1:3 plan with streets and buildings by the ratio; the owner sees
       the thinning before it is drawn. Trial on one district first: Mùṣá, its building study done (docs/lagos-study/buildings/d15.md), then its owed
       hand pass (16 h).
   (g) [x] The four scout notes of 27 Oct (docs/lagos-study/districts/d10, d11, d29, d30) checked claim by claim, 28
       Oct: one checking agent each, with a re-runnable script (docs/lagos-study/districts/scripts/, one per note) the
       main session re-ran; corrections in place, marked "corrected on check" or "added on check" (markers: d10 18, d11 10, d29 19, d30 10);
       each note ends with its Checked list. Owed before each is drawn: its Google look in Chrome (DECISIONS "Every district gets its own Google look"),
       and the web claims that rest on search summaries only or on pages that refused the fetch (listed per note).
   (h) [ ] A building study per district (.claude/agents/building-study.md, owner 27 Oct: "start studying the house
       types... is this residential?"): one agent per district, the drawn eleven first, each checked line by line.
       Done and checked: all eleven drawn districts, d09, d12-d19, d27, d28 (docs/lagos-study/buildings/; the last four 28
       Oct). Real cover against ours: d09 42.0/16.0%, d14 47.0/18.7%, d27 39.2/16.7%, d28 27.3/13.0%. Owed from them:
       the Deeper Life hall in Gbàgede redrawn smaller, fitting its ground at 1:3, fan-shaped, facing Ajayi Aina (real
       4,703 m², ours 442 m²; owner 28 Oct, DECISIONS "The Deeper Life hall is drawn smaller"; d28.md); Ebute Ilaje's shacks over the lagoon (d27.md) join the
       stilt house below; Okunade Estate's detached houses (d27.md) join the d18 kinds below; Ìtìrí's D14-41 and
       Gbàgede's D28-126 are each many real blocks Overture's streets leave joined, their streets read from Google Maps
       in the street pass (16f); Mùṣá's hand pass (its match hides LUTH drawn at 44% against 22% and the factories
       half empty; our houses median 84 m² against Google's 169: fewer, bigger houses at the same cover); the four new
       house kinds in the map format, approved by the owner 28 Oct (DECISIONS "New kinds of house"): stilt house over
       water (Makoro's stilt town is about 28% of d19), detached house in a yard, hall of residence, faculty block; then
       a kit for each in gidi-game (owner: "more kits to make for the instances"); Makoro drawn with its
       stilt town (owner, 27 Oct: DECISIONS "Makoro keeps its stilt town").
   (k) [ ] The square survey (owner, 28 Oct, DECISIONS "Looking is turned into counting"). Pilot read: ten Mùṣá
       squares (docs/lagos-study/squares/d15-pilot.md); nine of ten have a line ours lacks, seven a ground or walled
       plot; the railway stops 83 m short of d15-1612 and about 290 m Gidi of it is missing inside the outline. Next:
       (1) the owner settles the ten squares and the seven open questions (the answer key), at home on the computer
       (owner, 28 Oct, at work); (2) a helper reads the same ten blind, its misses counted against the key: started
       28 Oct before the key, since the read does not need it (~/gidi-data/research/squares/d15-blind-1.md), scored
       once the key is settled; (3) the rail drawn on to the outline by hand, with its
       walls; (4) a rail row and a per-square cover row in working_bar.py; (5) if the miss rate is low, all 250 Mùṣá
       squares by helpers in blind pairs, then Mùṣá's line hand pass from them.
   (m) [ ] **The city road layer, before the districts** (owner, 28 Oct: "lay out roads for the entire map... the
       main roads, the bridges... whenever we now want to lay the streets, we make sure that the streets connect to
       the bridges properly... we have to be very, very sure that we get it correctly"; DECISIONS "Roads first,
       districts by their borders", 22 Oct, step 1 never drawn as records). Comes before (l)'s drawing step.
       (1) [x] how today's districts sit on the real main roads: scripts/main_road_fit.py,
       docs/lagos-study/roads/MAIN-ROAD-FIT.md (seven of 11 at 90%+ on; d14 65%, d16 59% with the Third Mainland
       Bridge interchange missing, d19 74%); (2) [x] a home for city-wide roads in the format: `map/d00/`, the city
       layer (MAP-FORMAT section 1); (2b) [x] a water record in the format (`water`, MAP-FORMAT section 2: an outline
       for sea, lagoon, pond, marsh; a centreline with widths for river, creek, canal; d00 holds it) (owner, 28 Oct: "real roads and interconnections as
       well as its waters are the only things we are taking from Lagos one to one"); [ ] still owed: Unreal's
       map_build.py reading d00 and a kit part for water (while Unreal is on hold); (2c) [x] the real network to draw from: `scripts/city_network.py` (Overture's
       motorway 120.7, trunk 124.1, primary 135.0, secondary 201.4 km Gidi inside the frame; rail 45.6 km; 2,535
       junctions; 36.1 km of motorway flagged under construction, the Fourth Mainland Bridge and Lekki Regional Road:
       built too, owner 28 Oct, asked first where they would cut something already drawn); (3) every motorway, trunk, primary and secondary road of the frame, every bridge and
       flyover with its height, the rail and the water edges, drawn by hand from the real lines, widths and heights
       read on Google, piece by piece, the owner checking each piece. Piece 1 [x] the Third Mainland Bridge (rd-e7a23019, moved from Ṣọmọlá into d00 at its full real length, 3,266 m Gidi; 33.1 m wide with a 3.5 m median and four lanes each way, ICE's figure, read 28 Oct, replacing a by-eye 37 m; for it 6 Ṣọmọlá houses left out and 25 cut, 3 lanes moved off it, 2 removed: Ṣọmọlá's rd-7292fb80, Ìbùdó Mẹ́ta's rd-0877e4b9); owed on it: [ ] its heights z (Overture flags it raised all the way, but Street View at Oworonshoki, Jul 2021, shows it at grade there; no published deck height found (Wikipedia, ICE); Copernicus GLO-30 reads 5.8-6.4 m on the deck at s 2250-2550 against 0 beside it, the rest of the deck flattened with the lagoon, a weak reading at 30 m), [ ] then put back Ìbùdó Mẹ́ta's lane rd-0877e4b9 under the deck (removed 28 Oct: it ran under the bridge with no height to pass under; its record is in the git history of map/d16/plan.json), [ ] the Ṣọmọlá lanes that end on the bridge at grade (rd-80254433, rd-efb526e0 and others at the interchange) read on Google, as the real road is fenced there. Piece 2 [x] Ikorodu Road (28 Oct): the four 40 m district records (Mùṣá rd-i4klmw3w, rd-3079cryq, Ṣọmọlá rd-7a9ab6b8, Gbàgede rd-9e02217d) replaced in d00 by the express in four pieces at widths read on Google satellite by eye (motorway 27.5 m at Onipanu, 19.6 m at Obanikoro, trunk 45.7 m at lon 3.42 and 35.5 m at lon 3.45, each with a concrete median) and its service roads both sides where Overture has them (s 100-2310 and 2530-3180), 4.8-6.7 m, with slips; 32 district roads that were Ikorodu Road drawn twice removed; 45 houses left out and 42 cut back (2,805 m2 and 2,142 m2 of roof); check_map's city layer may hold service_road; working_bar's place check measures a point on the city layer's road from the whole road's outer edge. Owed on it: [ ] its heights z and the flyovers (Fadeyi, Jibowu, Ojota, Maryland), [ ] the BRT lanes as their own records, [ ] the bus bays, [ ] the Ojota and Jibowu interchange shapes, [ ] the strips at Ojota north (71.4 m overall read, not split), [ ] Mùṣá's Jibowu flyover rd-avaupyki still in d15, [ ] the service roads' ends read on Google (taken from Overture, not checked), [ ] the roof lost under it given back by hand in Mùṣá, Ṣọmọlá and Gbàgede (Mùṣá's cover 43.06%, below Google's 43.26%); (3t) [ ] the land's height (DECISIONS "The land's own height too", owner 28 Oct): data in hand [x] GEDTM30 v1.2 bare-earth heights for the frame, downloaded 28 Oct with the owner's OK (8 MB, ~/gidi-data/research/data/gedtm30/, README there gives source, licence CC BY 4.0 and the credit); DeltaDTM was the first choice but its host would not connect from this Mac (port 443 closed), FABDEM is non-commercial. Checked against our Copernicus GLO-30 at 9 places on land: within 1.8 m. Inside the frame: -2.0 to 74.2 m, median 5.7 m; its own uncertainty median 0.58 m. Not checked: the earlier note that Zenodo's page calls it for testing (the v1.2 record's licence field reads cc-by-4.0; its description not re-read). In the map [x] (28 Oct): the land as 297 relief grids in map/d00/dress (1 km each, 10 m between points, 2,893,347 points, -2.8 to 72.2 m, 14.3 MB), drafted by `scripts/draft_terrain.py`; `check_map.py` holds them to one spacing, the whole frame and equal shared edges; MAP-FORMAT says a thing's z is above the land. Owed on it: [ ] the water beds (4.6% of points have no reading, open water, held at 0 until the water records carry depth), [ ] Unreal reads the land as one Landscape (2,701 x 1,051 points fits 22 x 9 components of 126 quads; Epic's tiled heightmap import is reported broken in 5.7-5.8 on the forums, not tried), [ ] a check that a house's footprint and a road's width sit on land without a step too big (the slope under them), [ ] the board shows the land (how it draws d00's relief grids today not looked at); (4) the 11 drawn districts' roads measured
       against it and fixed by hand where they miss, the layer winning; (5) a check row: a district's roads must sit
       on the city layer where they meet it.
   (l) [ ] **Study first, then lines, district by district** (owner, 28 Oct, DECISIONS "Study the district first, then
       scale it, then draw", widened 28 Oct). The 15 line-sweep findings are in MAP-DONE-LAYERS's tables (83 layers, 29 lines). Order: Mùṣá (d15)
       first: (1) all 250 squares studied against the 29 line layers, written per square in
       docs/lagos-study/squares/d15/ (helpers in blind pairs once the answer key, 16 k, gives their miss rate; Claude
       checks every reading it uses); (2) the lines drawn by hand from that study, the study winning where the map
       disagrees, roads and outline kept; (3) dress; (4) a check row counting the map against the study. Then d09,
       d12-d14, d16-d19, d27, d28 the same way, then the undrawn districts. The Google look (16 i) is each district's
       first wide read, before its squares.
   (i) [ ] The Google look for the eleven drawn districts (d09, d12-d19, d27, d28), owner 28 Oct: "even the ones drawn
       needs its own look in Google Maps, satellite and Street View" (DECISIONS "Every district gets its own Google
       look"). One agent per district in Chrome: Maps for streets and places, satellite at z17-18 for blocks and density,
       Street View for the street look; written into the district's study notes, checked by the main session, before
       the density and street hand passes (d, f). Done: d15 (docs/lagos-study/google/d15.md, 28 Oct); d09 (docs/lagos-study/google/d09.md, 28 Oct: its 65 table rows and district counts re-run by the main session, all agree; it finds no water drawn though canals and a creek run through, roofs at 16% against Google 42%, fields and a container lot drawn as houses, 71 of 121 street names missing); d12 (docs/lagos-study/google/d12.md, 28 Oct: its 71 table rows and district counts re-run by the main session, all agree; one one-off distance corrected, S9 to the expressway 18.4 m not 15.1; it finds no water drawn though a canal network, creeks and a 500 x 400 m marsh run through, houses in the marsh, roofs at 15% against Google 41%, no market places, 123 of 191 street names missing). Of its map figures
       the main session re-ran the north-west box, roof shares, trees, shacks, kiosks, market and police counts and the
       street names, and later the r30 column, coordinates, outline tests and medians with
       docs/lagos-study/google/scripts/d15_look.py (21 of 23 views agree; S13 corrected to 9 houses). Its readings of the real place are the agent's, by eye, not yet re-looked (the
       north-west belt as sheds under our drawn flats, LUTH as ward blocks in lawns, four open grounds drawn as houses,
       a canal and a drain we lack, 9+ markets, 20 street names absent and 2 perhaps drawn under shorter names); the
       main session re-looks those key spots in Chrome before Mùṣá's hand pass uses them. Still to look: d13, d14, d16, d17, d18, d19, d27, d28.
   (j) [ ] Away mode in gidi-game (DECISIONS "Away mode", 28 Oct): its `.claude/settings.json` calls gidi's
       away-allow.sh and timeline.sh; committed on its own branch there (hooks/away-mode, c4a1164), ticked here once merged. Also owed: see the hook
       answer a real prompt (its log, ~/.claude/gidi-away.log, read the first morning after a night's work).
   (e) [ ] Then the topic passes ("the recursive loop", owner 27 Oct): one agent per topic going over each district
       again and again until its topic passes, Mùṣá first.
11. [ ] The other 50 districts to "working", breadth-first: the core six first (Ayégúnlẹ̀ 9, Agunda 12, Sọ̀rọ̀lérè 13,
   Ìtìrí 14, Ṣọmọlá 27, Gbàgede 28), then outward. Per district, in one sitting: roads read and set, houses, Overture
   places, bus stops and motor parks, landmarks, check at 0, then `scripts/working_bar.py dNN` passing (written 26 Oct; CHECKS.md
   row PART).
   - Ìtìrí (d14), started 26 Oct: roads done (hand pass 1, map/d14/STREETS.md: 367 records, every real street, 99% of
     road length on a real line, Lawanson Road at read widths, the seam with Mùṣá joined; working_bar d15 still PASS).
     Houses done (hand pass 2, map/d14/BUILDINGS.md: 687, each with a kind and storeys, drafted on the 37 main roads
     then cut back from the lanes). Places, the 2 bus stops and the Itire Road
     Motor Park done (hand pass 3: 202 places, 0 real places missing; working_bar d14 PASS). Landmarks done (hand
     pass 4: two school grounds, a factory and a church ground, walled with a gate each). **Ìtìrí is at the working bar**
     (working_bar d14 PASS, check 0, the board's own test 0, 26 Oct). 
   - Sọ̀rọ̀lérè (d13), started 26 Oct: roads done (hand pass 1, map/d13/STREETS.md: 452 records, every real street
     but 31 pieces under Western Avenue, 100% of road length on a real line; Western Avenue carried on from Mùṣá's
     flyover; Ogunlana Drive stays Ìtìrí's). Houses done (hand pass 2, map/d13/BUILDINGS.md: 518, each with a kind and storeys, 14.4%
     of the district, drafted on the 17 main roads then cut back from every road). Places done (hand pass 3: 143 places, 0 real places missing, 1 bus stop; working_bar d13
     PASS, with no landmark plot yet). The south lobe below Itire Road (Randle, Akerele, Falolu, Karimu, Clegg; in
     no district till now, the owner's 23 Oct decision) added to the outline, its streets drawn (hand pass 4, d13
     STREETS.md: 177 new roads; district now 0.670 km²). Its houses drawn (hand pass 4, d13 BUILDINGS.md: 222, 17.2% of the lobe). Its places drawn (d13 BUILDINGS hand pass 4: 76 more, 219 in all, 0 real places missing; working_bar d13 PASS,
     no landmark plot yet). Landmarks done (hand pass 5, d13
     BUILDINGS.md: 15 grounds walled with a gate each: 11 schools, the factory, the Tejuosho market, the stadium, and
     Randle's echo, the general hospital's compound, given care). **Sọ̀rọ̀lérè is at the working bar** (working_bar d13
     PASS, check 0, the board's own test 0, map picture gap 0, 26 Oct).
   - Ayégúnlẹ̀ (d09), started 26 Oct: roads done (hand pass 1, map/d09/STREETS.md: 1,015 records, 63.7 km, every real
     street but 18 pieces under the expressways, 98% of road length on a real line; the Lagos-Badagry and
     Apapa-Oworonshoki Expressways one 25 m record each along the border). Houses done (hand pass 2,
     map/d09/BUILDINGS.md: 1,472, each with a kind and storeys, 16.0% of the district). Places done (hand pass 3: 262
     places, 0 real places missing, 2 bus stops; working_bar d09 PASS). Landmarks done (hand pass 4: 16
     grounds walled and gated). Ayégúnlẹ̀ is at the working bar; map picture looked at and sent 26 Oct (the empty middle band was read as wetland, scrub and the barracks in d09 BUILDINGS hand pass 4; the building study of 28 Oct shows it is a canal with packed houses, see the Owed item).
   - Agunda (d12), started 26 Oct: roads done (hand pass 1, map/d12/STREETS.md: 882 records, 44.6 km, every real street
     but what Ìtìrí, Sọ̀rọ̀lérè and Ayégúnlẹ̀ hold; the Apapa-Oworonshoki Expressway one 25 m record on the west border;
     the seam joined on Agunda's side). Houses done (hand pass 2, map/d12/BUILDINGS.md: 963, each with a kind and
     storeys, 15.2% of the district). Places done (hand pass 3: 234, 0 real places missing); working_bar d12 PASS.
     Landmarks done (hand pass 4: 3 walled plots). **At the working bar** (26 Oct); its map picture looked at and sent.
     Its bus stops and motor parks owed (below).
   - Ṣọmọlá (d27), started 26 Oct: roads done (hand pass 1, map/d27/STREETS.md: 1,071 records, 66.0 km, every real
     street but what Mùṣá holds; Ikorodu Road on from Mùṣá's end, Third Mainland Bridge and Third Axial Road meeting at
     the Gbagada interchange with its two ramps, the Apapa-Oworonshoki Expressway on the south border). Houses done
     (hand pass 2, map/d27/BUILDINGS.md: 1,988, each with a kind and storeys, 16.7% of the district). Places done (hand pass 3: 427,
     0 real places missing); working_bar d27 PASS. Landmarks done (hand pass 4: 14 walled plots). **At the working
     bar** (26 Oct); its map picture looked at and sent. Its bus stops and motor parks owed (below).
   - Gbàgede (d28), started 26 Oct: roads done (hand pass 1, map/d28/STREETS.md: 1,190 records, 65.5 km, every real
     street inside the border; Ikorodu Road, the Apapa-Oworonshoki Expressway and the Third Axial Road on from
     Ṣọmọlá's ends, the cloverleaf's ramps in the north-west notch). Houses done (hand pass 2, map/d28/BUILDINGS.md:
     1,702 houses, 13.0% cover, the board's test 0). Places done (hand pass 3: 261, the denominational churches taken
     by hand; working_bar d28 PASS). Landmarks done (hand pass 4: 24 walled plots, the Deeper Life church's ground by
     Ajayi Aina Street kept whole with its hall). **At the working bar** (26 Oct); its map picture looked at and sent.
     Its bus stops and motor parks owed (below).
   - Saba (d17), started 26 Oct: roads done (hand pass 1, map/d17/STREETS.md: 669 records, 33.9 km, every real street
     but what its neighbours hold; Murtala Muhammed Way drawn again as one record, the trunk roads set to main roads,
     Ikorodu Road left to Mùṣá's expressway). Houses done (hand pass 2, map/d17/BUILDINGS.md:
     831, each with a kind and storeys, 14.4% of the district, the board's test 0). Places done (hand pass 3: 202, one bus stop by hand;
     working_bar d17 PASS). Landmarks done (hand pass 4: 9 walled plots). **At the working bar** (27 Oct);
     its map picture looked at and sent. Its bus stops and motor parks owed (below).
   - Lagoon University (d18, the frame study's UNILAG; its working name in NAMES.md), started 27 Oct: roads done
     (hand pass 1, map/d18/STREETS.md: 186 records, 8.3 km, every real street but what Saba holds); houses done (hand
     pass 2, map/d18/BUILDINGS.md: 144, cover 7.3%, the campus left to the landmark plots); places done (hand pass 3: 26,
     one bus stop by hand at the main gate). Landmarks done (hand pass 4: the campus as one walled
     school ground kept whole with its inside roads, 71% of the district, and its clinic compound). **At the working
     bar** (27 Oct); its map picture looked at and sent.
   - Makoro (d19, the frame study's Makoko; its working name in NAMES.md), started 27 Oct: roads done (hand pass 1,
     map/d19/STREETS.md: 144 records, 7.1 km, every real street but what Saba and Lagoon University hold); houses
     done (hand pass 2, map/d19/BUILDINGS.md: 286, cover 13.1%); places done (hand pass 3: 44, a bus stop by
     hand). Landmarks done (hand pass 4: one walled hospital compound, the only landmark ground Overture has in
     Makoro). **At the working bar** (27 Oct); its map picture looked at and sent. Its canoe landings, stops and
     8 tall readings owed (below).
   - Ìbùdó Mẹ́ta (d16, the frame study's Ebute Metta-Oyingbo-Otto; its working name in NAMES.md; study note
     docs/lagos-study/districts/d16.md), started 27 Oct: roads done (hand pass 1, map/d16/STREETS.md: 300 records,
     19.5 km, every real street but what Saba and Makoro hold; Clinic Road's second carriageway dropped by hand, as its
     neighbours hold one). Its bridges and ramps owed (below). Houses done (hand pass 2, map/d16/BUILDINGS.md: 402
     houses, 11.4% cover; one tall reading, b-c0559b50, given 2 storeys from nearby: owed a Street View look). Places done (hand pass 3: 98 places, the bus stop by
     the Oyingbo terminal, two seam places by hand on free ground; working bar PASS). Landmarks done (hand pass 4: 17
     plots from Overture's land use and the bus terminal's outline, Oyingbo Market as a 4-storey market block read off
     satellite, the cleared sawmill ground at Oko-Baba). Owed: the railway compound (Jaekel House), the Federal Medical
     Centre and the Red Line station, with the railway; the sawmill ground's football pitch and canoe landing, and
     Oyingbo Market's look, in the look pass.
     Not at the working bar under the 27 Oct density rule (item 16): cover 11.4% against Google's 26.4-30.5%.

12. [ ] **Gidi City, the shared space (owner, 27 Oct, DECISIONS "Gidi City: a shared space that feels like home").**
   The map work (item 11) stays first; alongside it, by the agents in `.claude/agents/` (district-scout,
   map-auditor, lagos-life-designer; made 27 Oct, their reports checked before they are passed on):
   (a) [x] what a player does hour to hour, the pilot shared activity and a first playable slice for the owner and
   their friends: researched 27 Oct (docs/gidi-city-research.md, IDEAS "Gidi City hour to hour"); the owner decides;
   (b) [ ] online from the start: before Unreal resumes, research how a shared world is built in UE5 (players per
   session, Epic Online Services and crossplay, servers and their cost, testing on PC with friends first, what PS5
   development needs, voice chat, moderation and safety, age rating);
   (c) [ ] controls: how the big open-world games map run (GTA, RDR2, Cyberpunk, Spider-Man, Sleeping Dogs) and what
   R2 does on foot if it runs (IDEAS "Run on R2, like FC");
   (d) [x] the open-source studio packs, read 27 Oct (an agent's triage; its quotes and counts were taken from the
   two clones, about a quarter of the big pack's 638 files read in full, the rest by description; Solo Studio's 34
   all read): install neither. The big pack's 49 agents all ask "May I write?" first, 2 of its 15 hooks can block, and
   it would cost about 10,900 tokens a session; Solo Studio's hooks and skills probably never load. Five ideas owed,
   rewritten for Gidi, each in its own commit:
     - [ ] a NOT ASSESSED answer for the checks, so a missing value never passes quietly ("a gate you have not
       watched fail is not a gate");
     - [ ] each input in map-auditor's and district-scout's briefs marked FOUND or ABSENT, NOT ASSESSED with no data;
     - [ ] a hook that blocks when district-scout stops without writing its note (the owner's OK given, 27 Oct);
     - [ ] notes that describe a passing state (e.g. "Unreal on hold") carry what would end it;
     - [x] dropped (owner, 27 Oct): a guard on whole-file reads of big markdown; "Important things are in the nuances,
       and if you ignore the nuances, you ignore the important things". Big files are read in full, in parts if need be;
   (e) [x] dropped (owner, 27 Oct): the roadmap and the story's twelve flowcharts stay with the owner's other
   account; "just build the world and we'll think about story afterwards";
   (f) [ ] a one-page "Gidi City at the end" from DECISIONS, IDEAS and the story, for the owner to cut and change.
13. [ ] **What are we not thinking about?** (owner, 27 Oct, DECISIONS "Study other games from the inside"): study GTA
   V's unpacked files (`~/gta5/playgta5`) to learn what a living world needs and how it was solved simply (traffic
   that appears around you, crowds and what they do at each spot and hour, driving feel; the owner finds Forza's
   driving better than GTA's "arcadey" feel), then Forza 2's repo when the owner brings it (a download: ask). Write
   it as our own notes, in plain words, with "what Gidi should think about" for each; nothing copied. First: a reader
   for the game's archive files, written by us; any program from the folder is run only on the owner's OK.
   First pass done 27 Oct (a helper; its counts spot-checked by Claude: 115 schedules, 248 handling entries,
   77,248 road nodes and 80,592 links, Gidi's 0 lane fields and 0 person spots): `~/gidi-data/research/gta/GTA-STUDY.md`
   (off the repos: it quotes GTA's counts). Its 15 gaps, for the owner to pick from: traffic fields on roads (lanes,
   one-way, speed), spawning around the player, population by area and hour, who can appear, people's spots with
   conditions and chains, reactions, cheap far-away life, junction rules, ambient sound, moments that wake near the
   player, crime and witnesses, local light moods, a driving sheet per vehicle with a wheel profile, parked-car
   spawners, hard budgets. The lessons, in our words: IDEAS "What GTA's own files taught us".
   Next: (a) [ ] the locked archives: CodeWalker's source downloaded (owner's OK, 27 Oct) to `~/gidi-data/tools/`; a
   helper is porting its key search and archive reader to Python, run over the browser port's engine file;
   (b) [x] Forza 2: dropped (owner, 27 Oct: "If the Forza thing is not useful... then there's no point"; the repo
   found was a machine-translated Windows port with no game files). The owner still wants driving that is not arcadey;
   (c) [ ] the owner's PSP games for how a story is built, read from the discs themselves (owner, 27 Oct: "the entire
   truth will always be in code"; talks only point where to look). Copied out of iCloud with the owner's OK to
   `~/gidi-data/research/psp/discs/`. Found in iCloud Drive, `Mac Archive 2026-08/PPSSPP/`: God of War Ghost of
   Sparta and Chains of Olympus, Harry Potter and the Goblet of Fire (not Chamber of Secrets), and GTA Vice City
   Stories; (d) [ ] how clean, real-looking games get their look (owner, 27 Oct): Rematch (Unreal), Mortal Kombat 1's
   colours, Spider-Man; and how roads get their dirt and grime, read from GTA's own files (its shaders, decal and
   timecycle files: "don't do as I say, do as I do"). For games we have no files of, the lesson is marked "from talks,
   not seen in files". Every lesson written down in IDEAS. (e) [ ] how GTA's missions force one method (owner, 27 Oct: ramming a
   fleeing target "did nothing"): read 27 Oct in Vice City Stories' script and program and GTA V's scripts (the native-name list
   and PPSSPP's decryption source downloaded with the owner's OK); IDEAS "Missions: the goal fixed, the way open". Rematch and MK1: not needed (owner, 27 Oct: "Don't worry about rematch"; Fortnite too: "We can get our art
   style without it"); their look lessons stay marked "from talks, not seen in files".
14. [ ] **A faster board test, run alongside the old one (owner, 27 Oct: "used in tandem... so nothing falls through
   any gap"; plan agreed: "this plan").** The board test (bpall.js on web/mapedit.js boardProblems) takes 65-80 min for
   the 11 drawn districts. First time where the hour goes (not measured yet). If it is the pair-by-pair compare, the
   fast test buckets houses and roads into map squares and runs the same exact touch test on pairs that share a square.
   (a) [ ] a self-test of planted problems (a house on a road, two houses overlapping, a house across a square's edge),
   on a scratch copy, that both tests must catch, run first every time; (b) [ ] trial: both tests on every district,
   their lists matching line for line, a mismatch blocks the commit until explained by hand; (c) [ ] after the trial,
   the fast test every time, the old one at each district's close (before its map picture) and once a week; any
   mismatch goes back to (b). Its own commit, after Ìbùdó Mẹ́ta.
15. [ ] **Know what's in the code base, routinely (owner, 27 Oct: "you should do that routinely... to have like a
   headspace").** scripts/inventory.py (3 s) run at every session start and after each compaction, its SUSPECTS read;
   the committed docs/inventory and CODEBASE.md (last 26 Oct) refreshed when the repos changed. First run 27 Oct: 888
   files (gidi 308, gidi-game 540, gidi-data 40), code 3,720 pieces (2 unused), 1 line naming a file that is not there
   (docs/lagos-study/similar/scripts/appendix.py). As a DECISIONS rule with its CHECKS row, its own commit.

**Owed: written down as "next" and not yet done** (swept from both repos' commits and docs, 25 Oct; each goes into an
item above, or stays here until it does. Rule in CLAUDE.md: every new "next" lands here or in the order, same change):
- **Meshy's credits run out on 11 Nov** (owner, 26 Oct: none used yet): before then, spend them on the hard shapes code
  can't get right (DECISIONS: monuments, sculptural one-offs; first candidates the landmarks the districts' map work
  names), each cost stated first. Map work comes first; this is done around it.
- The Saba (d17) and Makoro (d19) audit of 27 Oct (map-auditor, read-only; its cover figures and three findings
  re-checked by Claude: pc-472dd1cc 34.6 of 36 m² on carriageway, rd-a4ed4412 a 27.2 m stub, 14 four-storey houses in
  d19), to fix by hand in item 16 (d): Makoro's east half (59 houses where Google has about 5,900; footpaths or water
  for the stilt town); 12 four-storey walkups on the lagoon edge set to 1-2 storeys; 64 road ends 0-3 m short of a
  road in d17 and 2 in d19; 30 broken-in-two streets in d17, 2 in d19; 122 dead stops in d17, 37 in d19; seams not
  joined with d16 (Clinic Road, Murtala), d18, d19 and d27; Akoka Road's three doubling-backs and three repeated
  points; pc-044db919 and pc-472dd1cc off the road; pl-sab44155 a church_ground linked to pc-c01928e5; pl-sabc962e
  linked to pc-0de85f48; pl-sabb6735's two school places; pl-sab35696 a school house, not a walled plot; three
  houses on water in d17's north-east; every road tar_worn with no median; Murtala's three free pieces through d11 (to
  d11's Owed). The auditor's full lists (ends, odd kinds and storeys) are to be re-run, not copied: its scripts were in
  a scratch folder.
- The Lagos-Badagry Expressway stops at Agunda's edge: d09's rd-b2b8a5cc (25 m motorway) ends at (12568.69, 7733.91),
  13 m from the d09/d12 line, and no road wider than 13 m lies within 300 m of that end in d12 (checked 27 Oct from
  the plan files, after the d11 scout's note found it). Drawn by hand across Agunda's corner to d11's border when d11
  is drawn (a seam pass; Agunda's houses give way).
- The look pass (after every district is working, hero streets first; DECISIONS "Every district to working first"),
  moved from Mùṣá's item 10 on 26 Oct: the schools' and factory's faces and the factory wall's ice-cream advert; B28's
  real name to read; laterite and concrete roads sampled from their own panos, and a layer for interlock's pavers
  (`ground_look` lacks one); the places' sound-alike names (owner: later) and hours; the 787 houses given their
  neighbours' storeys, then kind, ground floor and roof block by block from the shots; ground patches; the `LIVING.md`
  sheets checked against Street View (thin ones first: Agunda, Ìlúpẹ̀lẹ́, Starlight Town, Ìwà, the outer Ikorodu
  towns, Àgbàlá); buildings for Mùṣá's six place squares in open ground (hand pass 63) and Ìtìrí's 65 (d14 hand pass 3) and Sọ̀rọ̀lérè's 53 (d13 hand pass 3); Ìtìrí's houses filled up and its four grounds' buildings (18.8% of the district against the real 37.5%; d14 BUILDINGS hand pass 2) and b-7aa9e512's storeys (2.5D read 5+) checked in Street View; Sọ̀rọ̀lérè's houses filled up (14.4%) and its six 5+ readings (d13 BUILDINGS hand pass 2) checked in Street View; Mùṣá's mix and person spots (after the owner's yes, Waiting 2); the brush layer; the hero streets.
- Mushin station's footbridge: from the hall b-mshstn01 over the tracks to both platforms, as the real one (a path
  whose points carry z, clear of the rail by 6 m; the check reads road z only, so rail clearance is a check to add
  with it). With item a2's rail and station builders, which also build `station_hall`.
- For Isolo-Ladipo (d30), when it is drawn: Isolo Road's deck goes on from the seam at 6.7 m over the expressway's west
  half and west service road, then ramps down at 6.5% with lanes at grade beside it, as d15's side (hand pass 61).
- For the road kit in gidi-game (Unreal is on hold): road points' z, the deck, its parapets and piers; and the board
  server reloading check_map.py when it changes (it holds the old road-node check until restarted: on 26 Oct it showed
  rd-isodeck1 crossing rd-qqm8wpxb with no node, which the new check passes as a bridge).
- Real names in record notes (push review, 26 Oct): d13, d14 and d15 road and district notes name real streets
  (Western Avenue, Ojuelegba, Ogunlana Drive...) while each STREETS.md says real names live there only. Settle it once:
  strip the notes to ids and sound-alikes, or reword the STREETS.md line; in its own commit.
- `scripts/map_picture.py`'s near view (26 Oct, Ṣọmọlá's): the frame stops at the near district's neighbours, but
  the names of drawn districts further off are still placed, stretching the picture with a blank lower half. Keep the
  names inside the frame (a fix to the tool, in its own commit).
- The map picture's GAP row (CHECKS.md): nothing yet fails a district closed without its picture; working_bar could
  run `scripts/map_picture.py`'s gap count and fail on red land beside the district.
- A hospital house type (Randle's two blocks are walkup and face_me_bungalow stand-ins, d13 hand pass 5); the landmark
  grounds' own buildings (the stadium's bowl and stands, the schools, the Tejuosho market, the factory) to the look pass.
- When Mile 2-Amuwo Odofin (6), Kirikiri-Tin Can (8) and Apapa (10) are drawn: Ayégúnlẹ̀'s two expressway records
  (rd-b2b8a5cc, rd-f1478f6a) run on their shared border, half their width over those districts' frame land; take them
  as held, join their streets to them, and settle the border line by hand (d09 STREETS.md).
- Ayégúnlẹ̀'s bus stops and motor parks beyond Overture's two stops (Boundary, Mosafejo, the expressway stops), read on
  the map (study only) and drawn as Ìtìrí's park (d09 BUILDINGS hand pass 3).
- Ayégúnlẹ̀'s middle band (about x 11,500-12,450, y 8,440-8,570): not wetland and scrub as hand pass 4 read it from
  Overture's land, but a narrow canal with houses packed to both banks (docs/lagos-study/buildings/d09.md: 1,733 Google
  buildings at 36% cover there against our 97 at 12%); the canal drawn as a narrow open strip with houses to it, only
  its west end by Signals Barracks open ground with trees, and the band's houses filled in the density hand pass.
- Sọ̀rọ̀lérè's bus stops and motor parks beyond Overture's one stop: Ojuelegba's park and stops, the stadium, Masha,
  Adeniran Ogunsanya, read on the map (study only) and drawn as Ìtìrí's park (d13 BUILDINGS hand pass 3).
- Agunda's Apapa-Oworonshoki Expressway record rd-cd2a7637 runs on its west border, half its width over the frame land
  west of it: the district drawn there takes it as held and draws its first 70 m (d12 STREETS.md). Ijora-Iganmu-Costain
  (d11) draws the 5 Apapa Road pieces on Agunda's east border. Alhaji Masha Road's 13.5 m (merged in two rounds) to
  read against the satellite first.
- Ṣọmọlá's Apapa-Oworonshoki Expressway record rd-f58919a3 runs on its south border, about half its width over the
  land south of it: the district drawn there takes it as held. Third Mainland Bridge and Third Axial Road leave
  Ṣọmọlá's border north-east and south: the districts there go on from their ends. Their 25 m widths (Ayégúnlẹ̀'s
  expressway's) to read against the satellite.
- Agunda's bus stops and motor parks: Overture has 2 stops and no park; a study of the map for its real ones (Aguda,
  Ogunlana Drive, Coker, Orile, the expressway stops), as Ayégúnlẹ̀'s.
- Agunda's 9 tall height readings (5+ storeys) took their neighbours' 2-3 storeys (map/d12/BUILDINGS.md): six are
  29-53 m2, too small for it; the three larger (b-0e26f361 103 m2, b-6493aef7 194 m2, b-e9e29b9e 135 m2) to look at
  on Street View and the satellite (the look pass, unless one is a landmark).
- The roads draft's kinds have no trunk: Overture's trunk roads come in as lanes. Saba set its three by hand (main
  roads, map/d17/STREETS.md); each district drawn next checks its trunk roads the same way. Saba's Murtala Muhammed Way
  (rd-9e64ec60, 10.75 m) is a divided road: its width and median to read against the satellite.
- Ikorodu Road along Gbàgede's west border is in d00 since 28 Oct (its record rd-9e02217d removed), and Ikorodu Road's north stretch crosses the north-west notch in five short pieces: the districts drawn there
  take them as held and draw on from them. The cloverleaf's own centre lies outside the notch. The 40 m and 25 m
  widths to read against the satellite, as Ṣọmọlá's.
- `working_bar.place_kind` gives no kind to real churches whose Overture category names a denomination
  (pentecostal 181, Roman Catholic 176, Baptist 104, Anglican 71, protestant 58, Jehovah's Witness 3 across Lagos's
  places): fix the check in its own commit, then add the missed churches by hand in the districts already at the bar
  (Mùṣá, Ìtìrí, Sọ̀rọ̀lérè, Ayégúnlẹ̀, Agunda, Ṣọmọlá). Gbàgede took its 22 by hand (map/d28/BUILDINGS.md).
- Gbàgede's bus stops and motor parks: Overture has 2 stops and no park; a study of the map for its real ones (Gbagada
  phase 1 and 2, the expressway stops, Ifako, Anthony by Ikorodu Road), as Ṣọmọlá's.
- Ṣọmọlá's bus stops and motor parks: Overture has 2 stops and no park; a study of the map for its real ones (Shomolu,
  Bariga, Pedro, Ikorodu Road by Mùṣá, the Gbagada interchange, the expressway stops), as Agunda's.
- Ṣọmọlá's 5 tall height readings (5+ storeys) took their neighbours' 2 storeys (map/d27/BUILDINGS.md): three are
  29-39 m2, too small for it; the two larger (b-5097e7c0 166 m2, b-7c249835 169 m2) to look at on Street View and the
  satellite (the look pass, unless one is a landmark).
- Gbàgede's 5 tall height readings (5+ storeys) took their neighbours' 1-2 storeys (map/d28/BUILDINGS.md): three are
  18-36 m2, too small for it; the two larger (b-e058528f 284 m2, b-ae17f158 124 m2) to look at on Street View and the
  satellite (the look pass, unless one is a landmark).
- Saba's bus stops and motor parks: Overture has none inside Saba; one stop was put by hand on Ikorodu Road by the
  coach terminal (map/d17/BUILDINGS.md). A study of the map for its real ones (Yaba's stop and market park, Sabo,
  Jibowu's coach parks, the Ikorodu Road and Herbert Macaulay Way stops), as Gbàgede's.
- Lagoon University's University Road (rd-cbdf1d43) ends on Saba's node on rd-beee86ae, its last 18 m over Saba's
  7 m lane rd-0dd14298, drawn twice there (map/d18/STREETS.md): the seam's hand pass decides which keeps the stretch.
- Third Mainland Bridge crosses Makoro's south-east corner for about 60 m (map/d19/STREETS.md) and runs on over the
  lagoon, drawn in no district yet: draw it whole by hand (both carriageways, its real width read first), with
  Ṣọmọlá's end of it (above).
- Ìbùdó Mẹ́ta's bridges and ramps (map/d16/STREETS.md): not drawn, Eko Bridge 689 m, Third Mainland Bridge 598 m along
  its water edge and 1,231 m of unnamed ramps (Overture's motorways, all raised); drawn on the ground for now but
  raised in Overture, Clinic Road 505 m (Saba's and Makoro's pieces too), Carter Bridge 298 m, the Ijora Causeway, the
  Oyingbo Flyover Bridge: draw them by hand as decks and ramps (as Mùṣá's rd-isodeck1), with Third Mainland Bridge.
- Lagoon University's campus wall: 5 gates of 38-157 m where campus roads run along the wall's line (map/d18/
  BUILDINGS.md hand pass 4): close them with railings or a wall set back off the road in the look pass.
- Makoro's stops and parks: one stop by hand on its spine street (map/d19/BUILDINGS.md); its canoe landings and
  water stops to a study of the map, with Saba's and Lagoon University's.
- Lagoon University's stops and parks: one stop by hand at the main gate (map/d18/BUILDINGS.md); the campus
  shuttle's stops and the gate's motor park to a study of the map, with Saba's.
- Makoro's 8 tall height readings (5+ storeys read; 7 in its north-east corner) took 3 or 4 storeys from their
  neighbours, b-0dcdd67b 2 (map/d19/BUILDINGS.md): to look at on Street View in the look pass.
- Ìbùdó Mẹ́ta (d16): the sawmill ground is **cleared** (owner, 27 Oct: "If the sawmill has already moved to another
  site, then clear it"; the real one moved to Agbowa in May 2025). Claude's call on what makes it worth a visit: open
  waterfront ground in a packed town, with what was left behind (stacked old timber, sawdust, a broken shed, a
  hoarding for the coming redevelopment), room for a street-football pitch and a canoe landing. To draw with d16's
  landmarks.
- Lagoon University's tall height reading b-8bd534f5 (76 m2, 5+ storeys read) took its neighbours' 3 storeys
  (map/d18/BUILDINGS.md): to look at on Street View in the look pass.
- Saba's 2 tall height readings (5+ storeys) took their neighbours' 2 storeys (map/d17/BUILDINGS.md): b-1b827014 is
  40 m2, too small for it; b-e9b783b2 (143 m2) to look at on Street View and the satellite (the look pass, unless it
  is a landmark).
- For Ijora-Iganmu-Costain (d11), when it is drawn: Western Avenue goes on south from Sọ̀rọ̀lérè's rd-32d33ffa end
  (13241.36,7384.58), 25 m, its values (d13 STREETS.md).
- Into item 0: plank stalls carry 17-30 material slots, one per timber shade: one material for the shades (gidi-game
  PERFORMANCE.md, 25 Oct); per-instance colour for the windows (custom data, in place of tint MIs; the ISM and UV-shift
  custom data are in, #90); plank bridges instanced (4a5d9d3); HLOD for the far city and streaming for the new map's city, the engine's World Partition first, measured (gidi-game
  PERFORMANCE.md "what is on").
- Plates: `plates.json`'s district rows and codes are the old map's districts; Mùṣá (d15) has none, so the street's
  vehicles print the 'bush' row (GDI) for now (gidi-game `gidi_street.PLATE_DISTRICT`). The new map's districts each
  want a row and a code (sound-alike, DECISIONS), then the plate textures made again (`tools/plates.py`).
- Vehicles (gidi-game kit/vehicle-instances): `M_GidiPaint_Instanced` is a generated copy of M_GidiPaint for instances;
  fold it into M_GidiPaint (instance space reads as local space on an actor) once that file's local change is settled;
  the near danfo's shadow drawn as a broken sliver as an actor, whole as an instance (not traced); the underdeck level
  not rebuilt since the lorries joined the heroes; the twelve old `lorry_ot45_*` test models in Art/Vehicles/LorryBuilt
  to check (old kit or live).
- Not understood yet, measure again: work mode slower than high on Underdeck; the over-the-roofs GPU median above the
  frame median; Nanite's fallback triangle count against the GPU's own (95b0053).
- Road kit: never imported into Unreal (6a26dd1, dc5e664 "Unreal not run"); the drain litter's next look pass (dc5e664).
- Plants kit for the ditch banks (55c14e7): item 3.
- The frame study, only if the frame changes: `scripts/frame_study.py` and `frame_footprints.py` read the roads study's
  working files (network.json, skel.pkl, wc50.npz, places.npz/json), written to a temp folder (`common.py` SCR) and gone;
  the roads study itself reads the first study's 250 m grids, whose scripts are lost too (CODEBASE "Known problems").
  A re-run means writing those grids' scripts again from `docs/lagos-study/STUDY.md` (raw data all in
  `~/gidi-data/research/data/`) with SCR in `~/gidi-data`. Until then `web/frame-study.js` and `web/frame-tiles/` stand
  (copy in `~/gidi-data/frame-backup-25oct/`).
- docs/MAP-FORMAT.md "Next steps": the format to `gidi-map/1.0` after the owner's answers; a real-names list for the
  whole frame; the twin catalogue with ids; the board's district outline editor, day filter, and loading only the
  districts in view.
- Road kit's look, still off against the photos (25 Oct passes): the drain narrower than g01's, its walls clean from
  the road, bottles too big, no cables under the plank bridge, the kerb-to-drain block plain, the grates' slots fewer
  and longer in the photos (ot03, g03); not tried on a curve. The road's few cm of relief and the drain walls' chipped
  tops are still noise in `road_build.py`: they become records with the road's bump and pothole records ("One ground
  truth").
- Builders, from the 24 Oct roof and street tests: the zinc roof's open gaps (gidi-game
  `Art/Buildings/BlockBuilt/ROOF-GAPS.md`: ridge cap, open eaves with rafter ends, the barge board, map fields first;
  patchiness at street distance); wall wear; gutters; the wear layer baked into images (`wear_layer.py` is Blender shader
  math and does not reach Unreal); builders still to make for frontage and ground (`tools/kit_fields.py` lists the
  record types no builder draws); person outfits; the basin test. The built lorry into `gidi_heroes.py` (not there yet).
- Emmanuel St (ut01), after the owner's verdicts (Waiting 4): the blurred passer-by and motorbike, the left sheet fence
  and lane sheds, shacks and zinc roofs, trees, wires, darker stained ground, the plank leaf's colour and papers, the
  pickup's crease and grille; then angles B and C ("The ultimate test").
Alongside, whenever a build waits: study passes over the saved Street View shots for new kits and activities, one
question per pass (memory: repeat passes on photos).

**State.** The new map (real Lagos at 1:3, 27 x 10.5 km, 51 districts) has its format (`docs/MAP-FORMAT.md`), the board's
tools (plan, dress, brushes, person spots, wires, clock) and its first district, Mùṣá (15 Mushin): 357 roads, the rail and its
station, and 4,275 houses drafted from real footprints and redrawn block by block (all 42 blocks read by 25 Oct; B27, a factory, and four slivers left as they were). The kit is the game repo's
builders (`gidi-game/tools/*_build.py`), read from the map's records by `tools/map_build.py`; the Emmanuel St round trip
passed. The old generated map is history: deleted 25 Oct (git tag `before-cleanup-25oct`). Nothing is running. Board:
`cd ~/gidi && ~/.venvs/gidi/bin/python scripts/board_server.py --port 8779`, then
`http://127.0.0.1:8779/web/board.html`. Unreal: open the editor with gidi-game `tools/editor.sh`, always with
`tools/watchdog.sh` on. VoiceMode's whisper and kokoro services are disabled on this Mac (24 Oct, owner;
`launchctl enable gui/501/com.voicemode.<name>` to undo).

**Waiting on the owner.**
1. **People** (settled 24 Oct, DECISIONS "People"): MakeHuman one-mesh crowd, MetaHuman for the people you interact with,
   one skeleton; crowd people fully interactive (punch, run over, react, ragdoll). The proof still to run, when the Mac is
   free and with the owner's go: N one-mesh people against N City Sample people in the Underdeck, low and high.
2. **The lived-in records** (`decisions/lived-in.md`): a yes on `mix`, `route`, `state`, `moment`, `job`; and on the 18 new
   `person_activity` values (`docs/lagos-study/LIVING.md`).
3. **Names** (#208, `docs/lagos-study/roads/NAMES.md`): Lagos → "Lagoon" in-game, or just "Gidi"? Ìkòrodò / Okotun too
   close? Mile 2→Mile 10, Mile 12→Mile 20? Mùṣá reads like Hausa "Musa"? Tone marks? The name of Gidi's Obalende (working
   name Underdeck).
4. **Kit eye tests** (the owner's eye judges): `~/gidi-data/research/google/kits/old-town/tests/ut01_emmanuel`, rebuilt by
   the builders (angle A v2, layers 1-7: verdicts pending; the pickup still reads weird). ot175, ot91, ot149, ot73 and
   ot45 in the same folder were the old kit's tests (all fails; the kit was deleted 25 Oct, what they taught is in
   `docs/OLD-KIT.md`).
5. **Download OK?** a CC0 grass texture (Poly Haven, ~10-20 MB) for verges.
6. **Restart the Mac** when the owner is home (about two hours after 24 Oct evening; swap 4.3 GB); then re-measure
   work mode's shadow pass.

**Parked (decided or asked for, not being worked on now; from the 19 Oct list, still open).**
- The built danfo's recipes and wear material (needs Fab), into the game in place of the Meshy one; the keke, korope, molue
  and BRT the same way.
- Gidi Brush as a real font file; coat of arms options; the brand sheet; the main menu and the wider Gidi UI (the owner is
  collecting references).
- The Reach in the Festac-inspired district (5 Festac), when it is drawn.
- Bus stops and junctions named the Lagos way, for the conductors' calls.
- Unreal look fixes from 18 Oct (paint lost under scans, orange dust strips, blue ground patches, plain flat roofs): check
  whether they still show with the builders' models before fixing.
- Consoles: apply to PlayStation Partners when there is a playable piece. The story (Tunde's), layered on the world.
- A living test for the new map, once a few districts join (IDEAS).
- The Underdeck's play systems (levy run, heat, money, rep, HUD) and people with cloth (the 22 Oct plan for video 1).
