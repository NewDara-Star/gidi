# Where the work stands (update at the end of every session)

**HANDOVER, 25 Oct 2026. Start here.** Read `DECISIONS.md` (the standing rules; replaced ones are in `HISTORY.md`),
then this page. What the repos hold: `CODEBASE.md` and `docs/inventory/` (`scripts/inventory.py`). The real Lagos research:
`docs/RESEARCH.md`. What the old map taught: `docs/OLD-MAP-LESSONS.md`. This page's dated log and done lists (22-25 Oct)
are in `HISTORY.md`, word for word; what they still owed is in the running order and the Owed list below.

**Running order** (owner, 25 Oct: "keep a running order". Work down it without asking "next?"; tick an item when it is
merged and checked, add new ones where they belong, and say here when the owner reorders it).
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
     grounds walled and gated). Ayégúnlẹ̀ is at the working bar; map picture looked at and sent 26 Oct (the empty middle band is wetland, scrub and the barracks: d09 BUILDINGS hand pass 4).
   - Agunda (d12), started 26 Oct: roads done (hand pass 1, map/d12/STREETS.md: 882 records, 44.6 km, every real street
     but what Ìtìrí, Sọ̀rọ̀lérè and Ayégúnlẹ̀ hold; the Apapa-Oworonshoki Expressway one 25 m record on the west border;
     the seam joined on Agunda's side). Houses done (hand pass 2, map/d12/BUILDINGS.md: 963, each with a kind and
     storeys, 15.2% of the district). Places done (hand pass 3: 234, 0 real places missing); working_bar d12 PASS.
     Landmarks done (hand pass 4: 3 walled plots). **At the working bar** (26 Oct); its map picture looked at and sent.
     Its bus stops and motor parks owed (below).
   - Ṣọmọlá (d27), started 26 Oct: roads done (hand pass 1, map/d27/STREETS.md: 1,071 records, 66.0 km, every real
     street but what Mùṣá holds; Ikorodu Road on from Mùṣá's end, Third Mainland Bridge and Third Axial Road meeting at
     the Gbagada interchange with its two ramps, the Apapa-Oworonshoki Expressway on the south border). Houses done
     (hand pass 2, map/d27/BUILDINGS.md: 1,988, each with a kind and storeys, 16.7% of the district). Next: places,
     bus stops and motor parks, landmarks, working_bar d27 and the map picture.

**Owed: written down as "next" and not yet done** (swept from both repos' commits and docs, 25 Oct; each goes into an
item above, or stays here until it does. Rule in CLAUDE.md: every new "next" lands here or in the order, same change):
- **Meshy's credits run out on 11 Nov** (owner, 26 Oct: none used yet): before then, spend them on the hard shapes code
  can't get right (DECISIONS: monuments, sculptural one-offs; first candidates the landmarks the districts' map work
  names), each cost stated first. Map work comes first; this is done around it.
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
- The map picture's GAP row (CHECKS.md): nothing yet fails a district closed without its picture; working_bar could
  run `scripts/map_picture.py`'s gap count and fail on red land beside the district.
- A hospital house type (Randle's two blocks are walkup and face_me_bungalow stand-ins, d13 hand pass 5); the landmark
  grounds' own buildings (the stadium's bowl and stands, the schools, the Tejuosho market, the factory) to the look pass.
- When Mile 2-Amuwo Odofin (6), Kirikiri-Tin Can (8) and Apapa (10) are drawn: Ayégúnlẹ̀'s two expressway records
  (rd-b2b8a5cc, rd-f1478f6a) run on their shared border, half their width over those districts' frame land; take them
  as held, join their streets to them, and settle the border line by hand (d09 STREETS.md).
- Ayégúnlẹ̀'s bus stops and motor parks beyond Overture's two stops (Boundary, Mosafejo, the expressway stops), read on
  the map (study only) and drawn as Ìtìrí's park (d09 BUILDINGS hand pass 3).
- Ayégúnlẹ̀'s wetland and scrub band across its middle (about x 11,500-12,450, y 8,440-8,570, from Overture's land):
  painted as scatter areas when the district's ground is drawn (d09 BUILDINGS hand pass 4).
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
- Ṣọmọlá's 5 tall height readings (5+ storeys) took their neighbours' 2 storeys (map/d27/BUILDINGS.md): three are
  29-39 m2, too small for it; the two larger (b-5097e7c0 166 m2, b-7c249835 169 m2) to look at on Street View and the
  satellite (the look pass, unless one is a landmark).
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
