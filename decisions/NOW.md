# Where the work stands (update at the end of every session)

**HANDOVER, 24 Oct 2026 (evening). Start here.** Read `DECISIONS.md` (the standing rules; replaced ones are in `HISTORY.md`),
then this page. What the repos hold: `CODEBASE.md` and `docs/inventory/` (`scripts/inventory.py`). The real Lagos research:
`docs/RESEARCH.md`. What the old map taught: `docs/OLD-MAP-LESSONS.md`.

**Running order** (owner, 25 Oct: "keep a running order". Work down it without asking "next?"; tick an item when it is
merged and checked, add new ones where they belong, and say here when the owner reorders it).
00. [ ] **Clean-up first (owner, 25 Oct evening, DECISIONS "Delete what we no longer use"):** run scripts/inventory.py,
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
     CODEBASE rewritten for the new layout, gidi-game PERFORMANCE's "what is on", MAP-FORMAT's board and import parts,
     the `?frame=new` mentions); history docs carry a note at their top; `scripts/inventory.py` now counts the names not
     marked as gone: 1 left, the output file `appendix.py` writes (not a pointer).
   - [ ] step 4b: NOW.md's dated log and DECISIONS trimmed to what is current (the replaced parts to HISTORY.md).
   Then item 0(b) widened: every kit (all the builders, not only stalls) as shared pieces drawn as instances.
1. [x] Road lines: 54 of the 62 corners in d15 hand-edited (gidi #332, #333): 12 repeated points dropped, 14
   doubling-back places cut (in 9 roads), 28 tight corners smoothed. The 8 left turn on junction nodes (check_map
   lists them) and go to item 2.
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
   Next builders in order: poles (4 variants; wires stay unique), then vehicles (keke_build exports no .glb; saloon,
   okada, bus and suv have no builder, 676 of d15's 824 vehicles; danfo and lorry have _static variants), then stalls
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

**Owed: written down as "next" and not yet done** (swept from both repos' commits and docs, 25 Oct; each goes into an
item above, or stays here until it does. Rule in CLAUDE.md: every new "next" lands here or in the order, same change):
- Into item 0: plank stalls carry 17-30 material slots, one per timber shade: one material for the shades (gidi-game
  PERFORMANCE.md, 25 Oct); per-instance colour for the windows (custom data, in place of tint MIs; the ISM and UV-shift
  custom data are in, #90); plank bridges instanced (4a5d9d3); HLOD for the far city and streaming for the new map's city, the engine's World Partition first, measured (gidi-game
  PERFORMANCE.md "what is on").
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
Alongside, whenever a build waits: study passes over the saved Street View shots for new kits and activities, one
question per pass (memory: repeat passes on photos).
Done: measure_csv reads a named street's level (gidi-game #90). Road kit edges (gutters, plank and slab bridges, kerbs, covered drains, grates, earth ditches: gidi-game
#80-#86); roads laid along their real lines (#87, #88).

**State.** The new map (real Lagos at 1:3, 27 x 10.5 km, 51 districts) has its format (`docs/MAP-FORMAT.md`), the board's
tools (plan, dress, brushes, person spots, wires, clock) and its first district, Mùṣá (15 Mushin): 357 roads, the rail and its
station, and 4,275 houses drafted from real footprints and redrawn block by block (all 42 blocks read by 25 Oct; B27, a factory, and four slivers left as they were). The kit is the game repo's
builders (`gidi-game/tools/*_build.py`), read from the map's records by `tools/map_build.py`; the Emmanuel St round trip
passed. The old generated map is history: deleted 25 Oct (git tag `before-cleanup-25oct`). Nothing is running. Board:
`cd ~/gidi && ~/.venvs/gidi/bin/python scripts/board_server.py --port 8779`, then
`http://127.0.0.1:8779/web/board.html`.

**Done 24 Oct.**
- Hooks: "nothing is claimed without proof" (checks before every commit, push and stop; a `Checked:` paragraph; a second
  model reviews each push). gidi #273, gidi-game #70.
- Gidi's study store moved out of World Drive's folder into `~/gidi-data` (#275); gidi-game's `tools/perf.sh` removed.
- Unreal's editor RAM: 9.2 GB to 5.9 GB on Underdeck (gidi-game #69, below).
- Inventory v2 (#276): `scripts/inventory.py` reads the code by its parsers (Python `ast`, the TypeScript compiler for JS),
  checks every comment that names a file or function, and maps the documents as a vault (links, orphans).
- **Branches:** every merged branch deleted after checking its work is in main (gidi 198 local and 197 remote, gidi-game 27
  and all remote); the unmerged ones were checked against the decisions, found replaced, saved as patches in
  `~/gidi-data/to-delete/branches/` and removed (PR #18 closed). Each repo now has only `main`.
- **Triage:** 91 old-map docs and pictures moved out (deleted 25 Oct, git tag `before-cleanup-25oct`); 14 replaced decisions and 3 dropped ideas moved to `decisions/HISTORY.md`; the sound-alike names rule is in
  DECISIONS ("Invented names only"); CHECKS rows made honest where only an old-map check held a rule; the old log of this
  page (16-22 Oct) went with them.

- **Kit pieces** (gidi-game #79, the rule "Save what makes a house, not each house"): block_build's windows and doors are
  shared pieces (`kit_pieces`), placed by each house's `.pieces.json` with that house's own slot colours. Full street:
  7 pieces, 9,292 placed, files 785 MB (853 before), 16.8 ms frame, GPU median 19.6 ms (16.2 before: one actor per
  piece). Next: instanced meshes (ISM/HISM, Custom Primitive Data for colour); measure_csv.py reads Play_Street's
  scene file even for a named test street (fix); split the other builders (walls and gates, vehicles, stall goods,
  poles).

**Done 25 Oct.**
- Mùṣá's roads: crossings over the gutters and crowns (#316, 946 crossings); the street edge drafted from the Street View
  notes (#317, 2,693 records after the re-run: poles, wires, vehicles, stalls, trees); "the road comes first" recorded, and
  check_map fails a house on a road (#318); kits into pieces, Meshy where stuck, the credits expiring 11 Nov (#319).
- **Road kit, first pieces** (gidi-game branch `kit/road-drain`, the owner's order: roads with gutters, bridges, kerbs and
  verges first): `tools/road_build.py` builds a road record's ground, open drains, silt and water, plank and slab bridges
  and litter, with the dirt in vertex colours (which M_GidiSurface reads); `tools/road_look.py` renders it with copies of
  the Unreal slots from a Street View camera, and `tools/kit_compare.py` sets the two side by side (test spot g01, Ogunmokun
  St). Litter and each bridge's boards are records, drafted once by `tools/road_draft.py`. The owner, 25 Oct: "make sure it
  looks very, very close... all the grime, all the dirt". Not close yet: the drain reads narrower than the photo's; the
  walls look clean from the road; bottles too big; no cables under the bridge; boards too even.
  **Owed to "One ground truth":** the road's few cm of relief and the drain walls' chipped tops are still noise in the
  builder; they become records with the road's bump and pothole records.
  Next: kerbs (painted, raised), grated covers, earth drains, then laying the pieces along the real centrelines, road in
  kit_fields' BUILDERS, then trees, masts and heaps.
- **Road kit, look pass 2** (gidi-game #81): the drain walls' inner faces now carry the dirt (a `frange` bug had left them
  two rows deep), road_look mirrors Unreal's T_Streaks term, test renders use Khronos PBR Neutral (AgX greyed the sand:
  foreground sand now 224,199,163 against the photo's 213,192,164), planks bleached to the photo, drain litter coated by
  the silt water. Pictures sent to the owner. Still toy-like: litter shapes (puffy sachets, crisp paper), smeared board
  grain, flat black silt, the drain narrower than the photo's.
- **Road kit, look pass 3** (gidi-game #82): litter as crumpled, sun-faded film half under sand (the photo's heap is pale
  pink, cream and mint); drain silt dries grey-brown with the road's sand drifting in; board grain de-aliased (it was
  finer than the 1 cm vertices). Boards still read soft: grain belongs in a scanned wood texture along each board's UVs,
  which needs a download. Next: kerbs (painted, raised), grated covers, earth drains.
- **Plank bridges' wood** (gidi-game #83; owner: "Yes download"): Poly Haven rough_wood (CC0, 7.6 MB; the project's own
  woods were polished or veneer) laid along each board's UVs, in the test renders and in Unreal's new M_GidiTimber. Boards
  read as weathered timber; g01z boards 205,191,171 against the photo's 219,194,162. Not yet seen on a mesh in Unreal.
  Swap sits at 5.9-6.3 GB: the watchdog stops headless Unreal within a minute until the Mac is restarted.
- **Kerbs** (gidi #325, gidi-game #84): roads can say a painted kerb's colours (`kerb_paint`; black and white when
  absent; rd-sdso0qxv set red and white from its reading). The road kit builds painted_bw kerbs 0.40 m tall in
  0.915 m paint blocks (measured on test spot g02, the yellow-and-black kerb at the Ogunmokun St rail crossing:
  paint within 12-20 levels of the photo: yellow 12, black 16-20, the render darker) and raised_pavement HB2 kerbs with the footway at their top; where a drain
  takes over the edge, a cast block closes the join, and drains now have end walls. Open: g02's road reads warm tan
  against the photo's grey (the ground pass); the kerb-to-drain block is plain.
- **Covered drains and grates** (gidi #327, gidi-game #85): gutters can carry a `covers` table (len, gap, slab/grate/missing,
  lift, tilt, wear), drafted once by road_draft.py; crossings can be `grate`. Test spots: ot03 Ajose St (both sides
  covered: the slabs read as one low strip with fine joints) and g03 Sadiku St (an 8 m grate crossing at a filling
  station: 16 panels, three short slot rows), both by eye beside the photo after 2-3 passes. Open: the photo's slots are
  fewer and longer; roads read too tan or too black against the photos' grey dusty tar (the ground pass); not tried on a
  curve or in Unreal.
- **Earth ditches** (gidi-game #86): tested against ot135 (Ogunkoya Shina, Olodi); banks inside the record's width,
  slumped, damp, mossy in patches, grey-green standing water. Weeds wait for the plants kit.
- **Roads laid along their real lines** (gidi-game #87, #88; gidi #329): road_build bends what it builds along the
  record's centreline, corners rounded on circles as wide as the road reaches (the spline-mesh way). Tested on d15
  rd-oahy2qpj (295 m, three right-angle turns): 0 folds except where its line zigzags. check_map now lists 62 road
  corners in d15 the kit would fold (12 repeated points, 14 lines doubling back, 36 corners too tight for their legs) as
  amber TODO: each is a hand edit of the line on the board. Next: those hand edits; junctions (each road is laid alone,
  the joins are not built yet); then trees, masts, heaps (Meshy before 11 Nov).

**Waiting on the owner.**
1. **People** (settled 24 Oct, DECISIONS "People"): MakeHuman one-mesh crowd, MetaHuman for the people you interact with,
   one skeleton; crowd people fully interactive (punch, run over, react, ragdoll). The proof still to run, when the Mac is
   free and with the owner's go: N one-mesh people against N City Sample people in the Underdeck, low and high. (Settled 24 Oct: the draft desk stays in `legacy/`, deleted with it 25 Oct; gidi-data stays on
   this Mac with no remote; the untracked `Claude outputs/` folder, the 13-14 Oct Ladi Lane mock, moved to
   `~/gidi-data/to-delete/claude-outputs-13-14-oct/`.)
2. **The lived-in records** (`decisions/lived-in.md`): a yes on `mix`, `route`, `state`, `moment`, `job`; and on the 18 new
   `person_activity` values (`docs/lagos-study/LIVING.md`).
3. **Names** (#208, `docs/lagos-study/roads/NAMES.md`): Lagos → "Lagoon" in-game, or just "Gidi"? Ìkòrodò / Okotun too
   close? Mile 2→Mile 10, Mile 12→Mile 20? Mùṣá reads like Hausa "Musa"? Tone marks? The name of Gidi's Obalende (working
   name Underdeck).
4. **Kit eye tests** (the owner's eye judges; all fails so far): `~/gidi-data/research/google/kits/old-town/tests/` ot175,
   ot91, ot149, ot73, ot45, and ut01_emmanuel (angle A v2, layers 1-7: verdicts pending; the pickup still reads weird).
5. **Download OK?** a CC0 grass texture (Poly Haven, ~10-20 MB) for verges.
6. **Restart the Mac** when the owner is home (about two hours after 24 Oct evening; swap 4.3 GB); then re-measure
   work mode's shadow pass.

**Next, in order.**
1. ~~**The old map, viewable only**~~ (24 Oct): replaced by item 00 (25 Oct): the old map and kit were deleted, kept at git
   tag `before-cleanup-25oct`; `web/city/` deleted with gidi-game's old importer (00, step 3).
2. **Mùṣá** (decided 24 Oct late, DECISIONS "Finish the map's first layer first": the plan layer everywhere first, a few fields per building, then house-type rules; the B1 sample is in `~/gidi-data/research/google/b1/STUDY.md`): the plan layer is done for every block: the small blocks were read 25 Oct (B30 got Oladeinde Coker Street, 21 houses; B31, B33, B35 and B36 were redrafted with no lane, 16, 13, 7 and 5 houses, B33's Ogidan Street left out for spacing and its railway strip, real bare ground, flagged; B34, B40 and B41, empty before, got 11, 2 and 1 houses; B32 and B37-B39 are slivers 3-16 m real wide, left empty); storeys drafted 25 Oct (`scripts/draft_storeys.py`, each house's real source found by shape, its Open Buildings 2.5D height read: 3,523 houses at 1-4 storeys; 35 read at 5+ and 787 with no source or no height left for a Street View check, listed in BUILDINGS.md); kind and ground floor drafted 25 Oct for the same 3,523 (`scripts/draft_kinds.py`: size, storeys and the street faced; lock-ups on busy roads); looks drafted 25 Oct for the same 3,523 (`scripts/draft_looks.py`: storey heights, roof, walls, windows, stair and wear by kind, shares from the old-town KIT.md study); the 35 read at 5+ checked in Street View 25 Oct (Hand pass 42: all 1-4 storeys, 2.5D read 13.5-20.5 m there); the 787 without storeys given their neighbours' median 25 Oct (`scripts/draft_storeys_nearby.py`; a sample of two judged in Street View were both wrong and fixed: rough, for the block-by-block pass), so every house now has all its fields; **finishing Mùṣá (owner 25 Oct, memory finish-musha-test: street by street, the final test is an Unreal overhead like Google Earth's plus random street views): roads read in Street View 25 Oct (#314: 529 points, 255 of 357 roads seen, `scripts/draft_roads.py`, STREETS.md "Roads read in Street View"; the read widths put 2,338 houses on carriageways, settled by hand pass 43: 2,301 set back, 377 cut, 70 left out, 4,275 houses); next: crossings over the gutters, the street edge from road_reads.tsv's edge column (walls, gates, kiosks, poles, parked cars, trees), ground patches, the gidi-game builders for road/ground/edge (research first), then the Unreal tests;** next the hand pass: schools, factory and B33's strip, front houses on busy roads, then the hero streets, then the other six core districts; B27 is the Vono Road factory compound (big sheds, no streets inside), left as it is for the per-building pass; B12, the corner by Palm Avenue, was read at z18 within B4's redo (its six lanes are in B4's table in STREETS.md) (B11, B10, B15, B14, B13, B16-B26, B28 and B29 done 24 Oct: 7, 9, 4, 7, 5, 4, 2, 4, 3, 3, 2, 2, 1, 2, 2, 1, 1 and 1 streets, 133, 169, 77, 113, 99, 55, 67, 56, 45, 51, 39, 24, 39, 28, 21, 19, 22 and 22 houses; B28 and B29 hold real school compounds the draft fills with houses, for the per-building pass); B0-B5's close-zoom recheck is done; then block by block
   kind, storeys, ground floor and roof from the shots; Western Avenue's side road, the Isolo Road interchange, the tidy-ups
   (Isolo Road kink near Omowunmi, Olushoga's zigzag); then its mix and person spots by hand from LIVING.md.
3. **Rebuild the old kit's things the new way** (owner, 24 Oct): one builder at a time from the list in
   `docs/OLD-KIT.md`, zinc roof sheets and lean-tos first. **First done, waiting on the owner's eye (24 Oct):** the zinc lean-to, gidi-game #72
   (`tools/leanto_build.py`; `Art/Props/LeantoBuilt/GAPS.md` lists 12 gaps against the photos, 5 closed, 1 closed in shape, 6 open
   with reasons; `look_v1.jpg` is photo | old kit | new). The map format gained each sheet's `hang` and `bend` (gidi #280).
   The owner on v1 (24 Oct): "not bad", "the rust looks very good", it lacks a bit of texture: fine dents, grain and dirt in
   the textures next. **Done (24 Oct, gidi-game #73):** `tools/zinc_kit.py`, the sheets shared by the lean-to and the
   block's roof: grain, pits and run-down streaks added; the look is three images per slope in the .glb (v1's shader rust
   would not have reached Unreal); option `lod` 0/1/2 (ot197 43,492 / 8,386 / 900 faces; a bungalow's roof about 36,000
   near, was 486,528). `Art/Buildings/BlockBuilt/ROOF-GAPS.md` and `roof_look_v1.jpg`: open are the ridge cap, open eaves
   with rafter ends, the barge board (none in the format) and v1 reading patchier than real roofs from the street.
   **Rule since (24 Oct): "One near model; Nanite draws near to far"** (DECISIONS): no far versions per builder; each makes one
   near model within a budget, its fine look baked into images. Held by gidi-game `tools/look_travels.py` (#74, in the hooks).
   Owed: the wear layer (the dust and grime on every built thing is Blender shader math and does not reach Unreal yet), the
   spot's ground, person outfits, the basin test. **Street test done (24 Oct, gidi-game #75-#77; numbers in gidi-game
   `docs/PERFORMANCE.md`):** 375 built houses round a Mùṣá lane (`tools/play.sh street`). It could not load at first (each
   roof slope its own images, ~4,500 uncompressed; the roof edge's ribs 26.5 M of 28.1 M triangles); research showed games
   share tiling images, so `zinc_kit.shared()` makes 6.4 m zinc tiles (24 for the street) and the edge is one row. Now 18.9 M
   triangles, 60 fps in high at eye level, 59 from 15 m up, 6.9 GB, texture pool 111 MB. The houses are plain (flat paint,
   no wear, black window holes), so this is a floor. **Budgets set (owner's yes, 24 Oct; DECISIONS "One near model"):** a
   building at most 300,000 triangles (held by gidi-game `tools/look_travels.py`), an ordinary house 80,000 as the target,
   a scene 30 M in high; props and vehicles open until measured. **New rule: "Save what makes a house, not each house"**
   (DECISIONS): shared kit pieces placed by each house's record. **Research done for the next step** (how the pros
   make many buildings real): modular kits placed as instances (City Sample: 24 kits, 2,000+ meshes, corner/wall/entrance
   per storey), trim sheets (one image set for all frames, sills, bands), per-house variation through Custom Primitive
   Data on one material, wear as tiling grime + vertex-paint masks + decals, fake rooms behind windows (interior mapping).
   **Next:** windows and doors as shared kit pieces, wall wear, then measure again; bake the wear layer; the roofs' patchiness tuned against the photos at street distance; then ridge cap, barge board, open eaves (map
   fields first); gutters. **Builders still to make for the map:** frontage, heap, tree, road, ground (`tools/kit_fields.py` lists 24
   record types no builder draws yet). What the old Blender kit already worked out for each, and what else it
   held: `docs/OLD-KIT.md`.
4. **Unreal:** a real Mùṣá block (~500 buildings) against the budgets, with the owner's go and the watchdog on (gidi-game
   `tools/watchdog.sh`). The volumetric clouds are the dearest GPU pass over the roofs (8.5 ms): a lighter sky for work mode.
   VoiceMode's whisper and kokoro services are disabled on this Mac (24 Oct, owner; `launchctl enable gui/501/com.voicemode.<name>` to undo). Always open the editor with `tools/editor.sh`.
5. **The board:** district outline editing; load only the districts in view; a day filter once spots have `days`.
6. Then the other six core districts (Ayégúnlẹ̀ 9, Agunda 12, Sọ̀rọ̀lérè 13, Ìtìrí 14, Ṣọmọlá 27, Gbàgede 28).

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

## Log (newest first)

**24 Oct 2026: living in each district** (`docs/lagos-study/LIVING.md`, study file). Chrome was not connected, so instead of photos: one sheet for each of the 51 districts: measured people, density, buildings, big roofs and listed places (WorldPop, Open Buildings, Overture), a wealth band A-E, who lives there, the day, work, vehicles, what the brush and person spots must show, a mix draft (busiest groups and hours) and the sacred and tragedy flags. It also has the okada map (banned inner councils, open outer ring) and 18 proposed activities missing from `person_activity` (bake_bread, carry_headload, run_press, smoke_fish, collect_levy, play_chess and others; adding them needs the owner's yes). Next: when Chrome is back, check each sheet against Street View, the thin sheets first (Agunda, Ìlúpẹ̀lẹ́, Starlight Town, Ìwà, the outer Ikorodu towns, Àgbàlá), then Mùṣá's mix by hand from its sheet.

**24 Oct 2026: Unreal's editor RAM (owner's go while away; a watchdog killed Unreal before the Mac could freeze).** Two causes, both fixed in gidi-game #69 (which also commits the 22 Oct modes work that was only on disk): the editor re-applied Epic scalability right after the mode's device profile, so "work" ran at Epic with ray tracing on (now `tools/editor.sh [mode] [underdeck|ibudo]` opens it with the mode's sg.* held); and the editor loads every sublevel hung on a level, so all 62 City Sample people loaded on open (play levels are now saved twice: `<level>` without them for the editor, `<level>_Game` with them for `tools/play.sh`). Editor on Underdeck, 4 min idle: 9.2 GB before, 5.9 GB now, swap flat (an empty level is 4.9 GB, the editor's floor). Numbers in gidi-game `docs/PERFORMANCE.md`. Open: work's shadow pass ran slower than high's in the 22 Oct game numbers; re-measure after a Mac restart (swap sits at 4.3 GB until then). Next for Unreal: a real Mùṣá block (~500 buildings) against the budgets. Always open the editor with `tools/editor.sh`, and keep the watchdog on (scratchpad `perf/watchdog.sh`, worth moving into gidi-game `tools/`).

**24 Oct 2026: the lived-in layer plan** (`decisions/lived-in.md`, proposal for the owner). Public research on every GTA's lived-in machinery, and Gidi's plan: five new records (`mix`, `route`, `state`, `moment`, `job`), new person-spot fields, standing, and an order of work (the owner's yes, then the board's clock and day filters, then Mùṣá's mix and spots by hand). Nothing built yet.

**24 Oct 2026: the board's brushes and person spots** (branch `board/brushes`). Work an earlier session left uncommitted in `~/gidi-worktrees/brushes` (23 Oct) was replayed onto main and finished: the Brush tool (N) paints litter, goods (on the ground or hung), relief and ground paint, every piece stored in full (MAP-FORMAT "Brushes"); litter starts on the old kit's street mix; an eraser (⌥); one stroke is one save and one undo. The Person tool (I) places `person_spot` records (activity, hours, count, what it belongs to; 68 Lagos activities). Tested headless (Playwright with the installed Chrome, not the extension): all six save and undo. Pole wires (Wire, J) and the Clock filter for person spots' hours were added the same day (branch `board/wires-clock`, tested headless). Still to do on the board: the outline editor, a day filter once spots have `days`. The old worktree can go once this is merged. Chrome extension was not connecting this session (Mùṣá's small blocks were done 25 Oct).

**23 Oct 2026, night: the builders are the kit; the interface works both ways.** The owner's direction (DECISIONS, "The interface works both ways; the builders are the kit"): items are objects with properties, the map tells each placed item what it has, kits improve from photos retroactively, "let the new builders become the kits going forward". Plan, steps 1-2 done:
1. **Old kit archived** (gidi #244): `blender/` is `legacy/blender/` (frozen, never extended; legacy tiles byte-identical).
2. **Builders declare their fields** (gidi-game #66, gidi #245): every map builder has `FIELDS` (path, type, absent meaning); `tools/fields.py` stops a build reading an undeclared key; `tools/kit_fields.py --map=~/gidi` checks both ways (0 fail, 24 flagged: record types no builder draws yet: road, frontage, leanto, heap, rail, station, mast, tree, roof_sheets, wall_bays, gutter_pieces, ground, relief, ground_marks, and fields like building.kind/storeys/ground_floor/outside_stair, vehicle.cab/lean/load/cover, faces.blotch, posters.face); `--write` writes `schema/kit_reads.json`; `--discover - <spot.json>` runs all 107 recipe builds strict. Schema gained per-kind vehicle objects (`pickup`, `danfo`, ...), the person `look` in full, new poses, umbrella `diameter`. The pole's poster now comes from the `posters` record; keke/molue/brt take the vehicle `colour`.

3. **One map reader** (gidi-game #67): `tools/map_build.py <map dir> <dNN> <out> [--box] [--camera] [--spot] [--origin]` turns plan + dress records into builder recipes (each builder's FIELDS/RECORDS read in reverse; tables become row lists; several goods records on one parent are one load) and builds them with spot_assemble; record types with no builder yet are listed. 4. **Emmanuel St round trip, passed:** gidi-game #68 `tools/spot_to_map.py` (the reader's inverse) wrote `angle_a/spot.json` as 29 map records, `map-stamps/ut01_emmanuel/d27/` (check_map 0 problems; every required field written in full with the builder's own default; a thing's wear on its record: new `wear` on stall, furniture, vehicle, people and the wall object; enums gained `hilux4` and ground floor `flats`), and `map_build.py` rebuilt the scene from those records alone: the same 26 things, the render matches `all_layers_p2` (scratchpad side-by-side sent). Person dials absent = MPFB's 0.5 (person_build FIELDS). 5. **Mùṣá (d15) buildings, draft in** (owner: "real footprints, then hand"; "lanes on dropped streets"): `scripts/draft_buildings.py map/d15` fills each block with its real twin block's own houses (Microsoft footprints, ODbL, numbers only), moved but never scaled or turned. Anchors run round the block edge, each anchor's fabric is shifted up to 7 m off the roads, and any house still caught is nudged up to 6 m away. Result: 1,426 houses, about 25-30% cover. Each record has only a footprint and a note, so the board shows them amber. `map/d15/BUILDINGS.md` lists, per block, the 110 real houses that landed on a road. Hand pass 1 done: of the houses on roads, 44 were set back on clear land and 60 left out where the frontage was full; roads stay on their real lines (1,470 houses). Hand pass 2: 173 overlapping houses trimmed to party walls. Hand pass 3: block B1 (Ladipo-Odunsi) studied on Google satellite, 11 lanes drawn by hand on its real grid, houses redrafted with the new `--frontage` mode (the twin's own houses turned to face the lanes) and the warehouse strip with its sheds (`--sizes`): 298 buildings, 53% cover. The owner (23 Oct): always check Google Maps and Earth to know the houses and streets. Hand pass 4: block B0 (Idi-Araba, LUTH) the same way: 9 streets (LUTH's drives as service roads), housing redrafted with `--frontage`, the campus copied (343 buildings). Hand pass 5: block B2 (Ishaga Road to Lawanson): 7 lanes, 367 buildings. Hand pass 6: block B3 (Mushin station to Ikorodu Road): 15 lanes, 339 buildings. Hand pass 7: block B4 (Ladipo market, Matori estate): 7 streets, 214 buildings. Hand pass 8: block B5 (Akanro, Ilasamaja): 3 lanes, 190 buildings. The six big blocks are done. Hand pass 9: small blocks B6, B7, B9 at close zoom (owner: zoom in for the details; B0-B5 were studied only at z16, so they get a z17-18 recheck next). Hand pass 10: B1 redone at close zoom: 20 lanes on the real streets (the first ten were offsets from Ladipo Street), 347 buildings. The study shots are about 5.7% smaller than their URL zoom (a 17z shot converts at zoom 16.92; check with an overlay of known roads); Hand pass 11: B0 redone at close zoom (z18 at the checked scale): 36 streets on the real lines (LUTH's roads as service roads, the nine z16 lanes removed), 520 buildings at 49% cover. Hand pass 12: B2 redone the same way: 36 streets on the real lines (the seven z16 lanes removed), 531 buildings at 50% cover. Hand pass 13: B3 redone the same way: 55 streets on the real lines (the fifteen z16 lanes removed), 434 buildings at 49% cover. Hand pass 14: B4 redone the same way: 15 streets on the real lines (the six z16 lanes removed), 251 buildings at 52% cover. Hand pass 15: B5 redone the same way: 18 streets on the real lines (the three z16 lanes removed), 329 buildings at 53% cover. Hand pass 16: B7 and B9 re-checked the same way (17 and 4 streets on the real lines). Hand pass 17: B6 re-checked: 10 streets added in its empty middle. Hand pass 18: B8 given 15 real streets (it had none). Next B11, B10, B15, B14, B12 and the rest, then block by block: kind, storeys, ground floor and roof from the ot shots (storeys may use the Open Buildings 2.5D heights, numbers only); lanes and footpaths drawn by hand on the gaps the dropped streets leave, biggest blocks first (the NW, Ladipo side). Then the other six core districts. Builders still to make for the map: frontage (a wall object could go through wall_build), lean-to, heap, tree, road, ground. Scene gaps still open at Emmanuel St: foreground passer-by and motorbike, left sheet fence and lane sheds, shacks and zinc roofs, lean-tos, trees, wires, darker stained ground, the plank leaf's colour and papers, the pickup's crease and grille.

**23 Oct 2026, late: angle A v2 (ultimate test 1).** The owner's verdict on v1 was a fail: "nothing like the picture"; the pass mark is the picture itself. So close-ups were taken from the same Street View pano (`ut01_emmanuel/closeups/`, read in inventory.md "Close-up reading": the "fence" is a street security gate with open steel leaves and a PUBLIC NOTICE; a spiked railing; a dark timber double gate; a double-cab pickup; a cart of jerrycans). Built (gidi-game #57): wall finish `railing`, a per-leaf gate `open` list, gate `posters`, goods `jerrycan`, pickup `cab: double` (`police_double` recipe), and **`tools/wear_layer.py`**, the wear layer the assembler puts on every thing and on the ground, at each record's wear. Map keys in gidi #235 (new check type `angles`). `angle_a/spot.json` v2 re-laid from the close-ups; `sbs_v2.jpg` sent to the owner. The pickup faces the photo at turn 245. Still missing: 5 people (`tools/person_build.py`, MakeHuman), the saloons down the lane (City Sample, needs Unreal), the compound shacks and zinc roofs behind the railing, the lane sheds and trees, the lean-to stalls on the right, the overhead wires. The scene is too pale and flat (the photo is denser and darker), the block is a little wide, and the pickup reads as a toy. Next: those, in that order, then v3; the owner picks the toys.

**23 Oct 2026, evening: layer by layer (owner: "make each element, put it on its own layer, perfect that layer before we move on").** `spot_assemble --only=name` renders one thing alone from the photo's camera and lays it over the photo (gidi-game #58); a spot's `look` (e.g. "High Contrast") matches the film's contrast to Street View (#59). **Layer 1, the block** (pass 3): 2 windows a floor on the short end facing the lane, a hip roof, drip-edge damp streaks from each floor (`wear_layer._drips`, block parts carry `drips`); `block_layer_p3.jpg` sent, the owner's verdict pending. **Layer 2, the pickup** (#59): rebuilt as a lofted, smoothed Hilux body (no boxes), front skins (dark bumper, big grille with slats and badge, wrap-round lamps), round mirrors, new body `hilux4` (the 4x4 police double cab), optional `wheels: alloy`. Placed in `angle_a/spot.json` at [4.99, 5.94], turn 255, wear 0.15; `pickup_layer_p1.jpg` sent (photo / v2 / now / model). Still off: the exact grille and lamp outlines, mirror stalks thin. Recipe keys `body`/`wheels` are not in the map schema yet. Next layers, biggest first: cart, timber gate; then people, saloons, shacks, sheds and trees, wires.

**Layer 3, the street gate** (gidi-game #60): re-laid from the photo as two records, `gate_L` (one leaf swung out, -60, pier at u0) and `gate_R` (closed, pier at u1, the PUBLIC NOTICE and papers), black sheet steel, dark painted piers, spiked tops; new gate keys `piers`, `spikes`, poster `lines` (schema + MAP-FORMAT). `gate_layer_p1.jpg` sent. The old `street_gate` record is kept in `spot_v3_pre_gate.json`.

**Layer 4, the stall and umbrellas** (gidi-game #61): the red umbrella solid red with its printed badges and word (`prints`), the green one fully open, low, its head cocked (`head_tilt`) on a black pole (`pole_colour`), the bench short and tall (`height`) where the man sits, the stall taller and darker with its basket. Wear lowered per thing in the spot (stall 0.2, umbrellas 0.15-0.2): at 0.5 the wear layer greys timber and pales cloth past the photo. `stall_layer_p1.jpg` sent.

**Layer 5, the water cart** (gidi-game #62, gidi #241): a barred cage on a low bed (cart `sides`), cans standing upright with coloured caps, one black spoked wheel (`spokes`), the handlebar leaning to the boy (`handle_tilt`); placed at [7.41, -5.49], turn 206. `cart_layer_p1.jpg` sent.

**Layer 6, the timber front** (gidi-game #63): the near-black compound wall stands 13 m out, square to the camera, with its double gate's right leaf open on the orange door; the loose plank leaf is its own record `plank_leaf`, edge-on at about 9-10 m. The wear layer had bleached every board silver: a plank wall with `painted: true` (tarred boards) now wears as paint (a material's `wear_class`). `timber_layer_p1.jpg` sent. Still off: the leaf is greyer than the photo's warm brown and has no frame or papers; the fence's timber posts read pale. Owner verdicts pending on layers 1-6. Next: people (`tools/person_build.py`), then saloons (Unreal), shacks and zinc roofs, sheds and trees, lean-tos, wires.

**Owner, on the whole scene (`all_layers_p1.jpg`, every built thing rendered together without the photo):** "done really well"; the jerrycan cart singled out as good; **the pickup still stands out as weird**: go back to it.

**Layer 7, the people** (gidi-game #64): six people from spot records (`build: person`): the cart boy (push, leant), the man lying face down on the long bench (`lie_prone`; the bench moved under him to [8.63, -8.22], turn 315), the woman in maroon walking, the tall man in the light-blue kaftan perched on the bench (`sit`, seat 0.68), the seller behind the stall (`hold`), the kid in yellow down the lane. Clothes are MakeHuman suits tinted in two tones split at the waist, or dyed. Note: a spot `turn` runs clockwise as seen from the camera (spot angle = -turn). `all_layers_p2.jpg` sent. Not yet: the blurred passer-by and motorbike in the left foreground, the woman's paper, faces (MakeHuman defaults). Next: the pickup again, then the left sheet fence and lane sheds, shacks and roofs, the ground (darker, stained) and wires.

**23 Oct 2026: ultimate test 1 (Emmanuel St, Shomolu), first things built in gidi-game.** The owner's ultimate test (DECISIONS): list every thing in the three real pictures (`~/gidi-data/research/google/kits/old-town/tests/ut01_emmanuel/inventory.md`, 29 items), model each clean and whole, rebuild angle A from records, then B and C. Done: the **market umbrella** (#45, `tools/umbrella_build.py`: panels, sag, scalloped hem, valance, ribs and stretchers, open/half/closed, tyre/bucket/drum base, tilt; 4 recipes) and the **pickup** (#46, `tools/pickup_build.py`: Hilux-shape police pickup and old 504-shape pickup, shell from three outlines intersected, kicked-up frame carrying the bed, police light bar and bed benches, crates or sacks, tailgate up/down/missing, wreck keys; 4 recipes, `Art/Vehicles/PickupBuilt/look_v1.jpg`). Then the **rendered block** (#47, `tools/block_build.py`: the map's building + faces records; buildings 1-2 as cream_balconies_3s and maroon_panels_2s), the **street pole** (#48/#49, `tools/pole_build.py`: the map's pole + wire records; timber/concrete/steel, arm, transformer, lamp, boxes, stay, poster, street-name blades), the **wall and fence** (#50, `tools/wall_build.py`: the map's wall record + posters; sheet, plank, render, bare block, breeze screen, piers, tops, sheet_steel/bar/plank gates with open and sag; 5 recipes). Owner's eye caught two things, both fixed: the street-name blades have a thin white line top and bottom (#50, `rim`), and the leaning pole's tangle was for effect: now the knot is the service wire records tied at `lash` (#51). Then the knot rebuilt as one-piece wires (#52), the **stall builder and goods kit** (#53, `tools/stall_build.py` + `tools/goods_kit.py`: plank stall, table, rack, kiosk, cage stall, tarp on poles; every goods kind built from its row), **furniture** (#54, `tools/furniture_build.py`: every furniture kind incl. the generator), **carts** (#55: push cart and vulcaniser's trolley as stall kind cart, compressor and tyre changer). Schema keys added in gidi #227-#232. Before building the next thing, check City Sample/Fab/Megascans first. Then the woven basket and litter pieces (goods kit, gidi-game #56) and the **spot assembler** (#56, `tools/spot_assemble.py`: a spot file of camera, ground, sky and things by builder and recipe; builds, places, renders from the photo's point). **Angle A rebuilt, v1:** `tests/ut01_emmanuel/angle_a/` (spot.json, sbs_v1.jpg), sent to the owner. Next: the owner picks items that look like toys, one by one, and each is fixed in place; still missing from the scene: people, saloons (City Sample, needs Unreal on), sheds and distant houses, wear. Map record types whose fields match each item's recipe keys (e.g. an umbrella record) are still to add.

**23 Oct 2026: the container lorry built the danfo way (gidi-game #43).** The owner, on the ot45 lorries: the danfo has hundreds of variations, so build the lorry the same way; "zoom in on details and connecting parts". `~/gidi-game/tools/lorry_build.py` builds it part by part (cab-over or bonneted tractor with a full frame and running gear, air lines, skeletal or flatbed trailer with kingpin, legs and axles, ISO boxes with castings, corrugation and door hardware). A recipe is the map's own `container` record (its keys), plus assembly and damage keys (box 40/20/20r/2x20/none, axles, roof, deflector, exhaust, doors, dents, glass, mirrors, bumper, wheels_missing). 12 recipes, sheets in `Art/Vehicles/LorryBuilt/` (look_v1, close_v1 = joints, range_v1). **The gidi kit's vehicles (`legacy/blender/gidi_kit/vehicles.py`) are stand-ins: never improve them; built vehicles live in gidi-game** (danfo, keke, molue, BRT, lorry). Next: put the lorry in `gidi_heroes.py` and make the kit leave containers out of its tiles (when Unreal is on, the owner's go); show ot45 with the built lorries; then revisits, ot13, ot62, board brushes.

**23 Oct 2026: ot45 pass 2 (Ladipo St).** `tests/ot45/side_by_side_pass2.jpg`. Added from records: litter `dust` and `buried`, `crumb` litter (desk `crumbs`), median `streaks` and sand `drift` (desk `grime`), container `box_ribs` (desk from `box_wave`/`box_fade`/`box_dents`), `rim_colour` (rims with hub and nuts), `tractor_marks`, `beam_marks`; the bonneted tractor rebuilt from profiles (rounded bonnet, arched wings, grille, mirrors). The gap now has lock-ups, a green tarp, a sign and a man. ot91/ot149 pixel-identical, ot175/ot73 max 3/255, legacy tiles byte-identical. Fields in KIT.md section 12 ("ot45 pass 2").

**23 Oct 2026: kit eye test 5, ot45 (Ladipo St, Mushin), done; the owner judges.** `~/gidi-data/research/google/kits/old-town/tests/ot45/` (sbs_first.jpg = kit as on main; side_by_side.jpg after one pass; closeups/tractor_sbs.jpg, median_sbs.jpg). A new view: the camera looks straight across a dual carriageway at a low concrete median, a rubbish-strewn dirt strip and two parked container lorries (red box on a flatbed, blue box behind an old bonneted tractor). The pass added, all from records: a `median_wall` part (drafted cast lengths, chips, cracks; a `median` with no record is a MissingRecord), flat `sheet` litter, rubbish `bands` on the draft desk (desk only; the kit reads pieces), a bonneted tractor, a flatbed trailer, unstriped trailers, painted `box_marks` on containers; and a fix: each further street piece gets its own ground material (before, the last street's colours painted every street). The dirt strip is a hand edit of the ground grid. ot91/ot149/ot73 pixel-identical, ot175 as before (max 4/255), legacy tiles 6,12 / 7,12 / 8,13 byte-identical. Still differs: rubbish reads as crisp scattered cards (needs dust, burial, crumbs, sand banked at the median), the tractor is boxy, containers too clean (no dents, waves, logo), background sheds wrong. New fields in KIT.md section 12 ("fifth eye test"); the MAP-FORMAT converter must learn them too. Next draws: ot13, then ot62.

**22 Oct 2026, midnight: the dress editors on the board.** Face editor (Face tool C, or a building's Face buttons): one face drawn flat, u along, z up; drag boxes for windows, doors, shopfronts, balconies, screens, stains, add-ons, signs, awnings; every field in a side form. Goods (O) in a lean-to's, stall's, heap's or bin's frame, Litter (X), Ground paint (D), Relief (H: a grid raised and lowered cell by cell). Each piece is one table row: pick, drag, delete it alone; a new piece takes the picked one's values except where it lies; anything not drawn or chosen stays unset (amber, "missing value"). Convention set in MAP-FORMAT: on a face, u is a piece's middle, a window's or stain's z its bottom (the owner can turn that round). Next: brushes, person spots, pole wires.

**22 Oct 2026, near midnight: Stamp, Frontage, dress tiles on the board.** The new frame now reads and writes the dress layer: dress records go to the 100 m tile of their parent (a lean-to's goods and sheets follow its host), a moved record takes its dress along, and the board loads the tiles in view. **Stamp (K):** copy a record with everything on it (faces, roof sheets, lean-tos, goods, wires) from the map, the example, or any `map-stamps/<name>/` folder (where converted test spots go, in Gidi metres), turn it with R or [ ], click to place; full values, new ids, a `from` note. **Frontage (E):** click a plot side; it finds the road, the side and the setback, and a wall for walled kinds. **Lean-tos on walls and frontages**, with "Put it on the other side". Documented in `docs/MAP-FORMAT.md` (sections 2, 3, 6). Next on the board: the face editor, goods, ground paint, relief and litter, then brushes, person spots and pole wires.

**22 Oct 2026, late night: the board draws the new map.** The new frame (`web/board.html?frame=new`) now draws and saves the plan layer into `map/<dNN>/district.json` + `plan.json` (`web/mapedit.js`, the `/api/map/*` calls in `scripts/board_server.py`, listed in `docs/MAP-FORMAT.md` section 6). Pick "Draw in..." a district, Start it (outline from the frame study, name left empty for the echo names), then Select, Street, Building, Plot, Wall, Gate, Lean-to, Tree, Furniture (stall, pole, vehicle, furniture, heap), Place, Surface; every field in the side panel, missing ones in red, nothing filled in silently. Saved records with fields still to set show dashed amber; check_map.py runs on every save and its problems show red. Streets snap to map roads (a shared point joins them) and, with "Snap to real roads", onto the real line under the pointer; nothing is copied from the study. The old map's save path is unchanged. **No district is drawn yet: `map/` is empty.** Next: draw the central core by hand; later brushes, the dress layer, Frontage, Stamp (MAP-FORMAT.md next steps).

**22 Oct 2026, night: the frame's districts, the first kit test, textures.**
- **The new map's data format, drafted** (`docs/MAP-FORMAT.md`, `schema/map_schema.json`, `scripts/check_map.py`, example in `docs/map-format-example/`): one folder per district, a plan file (roads, plots, frontages, footprints, storeys, lean-tos, stalls, poles, vehicles, places) and 100 m dress tiles (every window, stain, roof sheet, slab, sack, litter piece, ground patch, bump), stable random ids, Gidi metres (y south), small things as table rows, stamps stored in full with a `from` note. The checker rejects unknown or missing fields, broken links, real names, and kit parts reading fields the map lacks. Size: a dense core district about 6.5 MB plan + 120 MB dress; the whole city about 0.6 GB plan + 7-8 GB dress, so the dress layer moves to its own repo past 1 GB. **Waiting on the owner:** brushes or stamps only; table rows for small things; the dress repo; district names. Then the board's save calls and the kit reading it.
- **Districts settled by real borders:** the roads study (`docs/lagos-study/roads/ROADS.md`, #190: the real skeleton at 1:3 in the 27 x 10.5 km frame, 819 named places, borders, counts) and the Google Earth checks of its 15 doubtful lines (`EARTH-CHECK.md`, #191) give **51 districts** (48 if Iba, UNILAG and Odogunyan fold in), each a real place or real neighbours, with the split lines through the central core (7), the west sprawl (6) and the Ikorodu belt (5 + Imota). The owner: the number doesn't matter, "any number that passes"; what matters is a true mini Lagos. **Every unsure and to-trace line is now settled by a vote of map sources** (EARTH-CHECK.md, "Source votes (22 Oct)": Google labels and area cards, satellite, the OSM map, LGA lines, written sources; majority wins). All 18 came out *likely*, none a coin-toss, so the board shows no pink or amber lines. Still 51 districts, with members moved: Adelabu to Aguda, Ogunlana to Itire, Itire cut at the Idi-Araba canal (north to Mushin), Agungi west to Lekki Phase 1, Oworonshoki to Gbagada-Ogudu, Command to Agbado-Oke Odo, the Jakande Estate pieces to Okota and Ikotun-Igando, Majidun north-east cut at the 3.489 valley and Odogunyan south of the Fourth Mainland reserve to Ikorodu Town; 45 renamed Ijegun-Abaranje-Isheri Osun, 49 Igbogbo-Bayeku. Next: the hand-drawn plan on the skeleton.
- **The new frame is on the board:** `web/board.html?frame=new` (or the "New frame" button) shows the real skeleton at 1:3 by class, water, the 51 districts (unsure lines, pink dashed, only for a coin-toss vote: none now), the place names, and real roofs when zoomed in. Study layers only, never map data; build them with `scripts/frame_study.py` and `scripts/frame_footprints.py` (outputs gitignored). Drawing tools on it now write the new map format (see the line above).
- **Old town kit:** `~/gidi-data/research/google/kits/old-town/KIT.md` (199 shots) sent to the owner. First eye test running: random spot ot175 (Olayiwola Liasu St, Ilasamaja), written as map data, rebuilt from kit parts in Blender, rendered from the Street View camera, side by side for the owner (decision #188).
- **Kit reads only map records (one ground truth):** the old town kit throws no dice now. A new spot gets a first draft of its records from `legacy/blender/kit_draft.py` (the old seeded rules, kept in `gidi_kit/draft.py`, run once and written into the map); after that the records are the map's and are edited by hand. A missing record is an error. Record formats: KIT.md section 12, "Records". ot175 and ot91 are drafted and render as before; the old city generators build byte-identical tiles.
- **Kit eye test 3, ot149 (Ayantuga St, Mushin), done; the owner judges:** `tests/ot149/` (sbs_first.jpg is the kit as merged; side_by_side.jpg after one pass). The pass added: one roof over a plot turned to the street, shopfronts carried onto a turned face, the photo's sky colour (`shot.sky_seen`), a concrete apron on either side, drain depth and a gone slab as records, sand heaps, zinc wall sheets (`facade.panels`). ot175 and ot91 render unchanged. Then the open items were fixed (PR kit/ot149-fixes): flush drain slabs (`proud_m`), off-road ground colour from the record (`ground_colours.beyond`, `ground_band_m`), a cage-stall part and a glass cabinet, signs with thickness, sag, tears and peels, a denser frontage, and paint toned to the photo on ot149, ot91 and ot175 (`tone.py`; before/after images in each test folder). Next draws: ot73, ot45.
- **Kit eye test 4, ot73 (Ogunmule Akinlogba St, Epe), done; the owner judges:** `tests/ot73/` (sbs_first.jpg is the kit as merged; side_by_side.jpg after one pass). This is a new kind of street: a wide tarred town road with kerbs, grass verges and a bare-block fence. The pass added kerbs, grass verges, steel-arm street lamps and block stacks, a clean tar edge (`tar_fray`), and a pole leaned by the map. ot91, ot149 and ot175 render unchanged. Open: low-poly ball trees (the bush needs a leafier part), no okada rider, no grass texture (a download needs the owner's OK). Next draw: ot45.
- **Textures:** 22 CC0 surfaces from Poly Haven at 2K in `~/gidi-data/textures/` (zinc, sheet steel, plaster, block, concrete, asphalt, laterite/dirt/mud, timber), the same files for Blender tests and Unreal, keyed by each part's material slot.
- **Performance work stopped** after the laptop froze (Unreal measuring loop at 8.9 GB); restart only with the owner's go, smaller window, one run at a time, people made cheap not cut (#186, #189). The modes work is committed (gidi-game #69, 24 Oct).
- **Laptop:** old 2021-22 adware auto-starts found and moved to `~/Quarantine/adware-2026-10-22/` (no miner); the owner to restart the Mac.

**22 Oct 2026, evening: roads first, kits, the kit test** (DECISIONS.md, #182-#184). The seed-point units behind the district count glued Gbagada to Maryland by swallowing Anthony Village (the owner caught it), so the plan now starts from Lagos's real roads at 1:3, places cut by their real borders, joined only where they touch and are alike. A helper is writing that study to `docs/lagos-study/roads/` (skeleton, places by border, new count, a Google-check list). The plan is hand-made; the models come from kits, one per kind of place, each proven by rebuilding random Street View spots one-for-one. The 2D map carries the fields a kit needs (house type, storeys, gutters...); the kit never decides placement. The Reach goes with Gidi's Festac-inspired place.
- **Kit study 1, dense old town, running:** `~/gidi-data/research/google/kits/old-town/` (outside the repo): ot01-ot18 from Shomolu, Mushin, Isale Eko and Ajegunle with notes in `shots.tsv`; a helper is taking it to about 200 shots and writing `KIT.md` (house types, parts and how often, plots, streets, gutters, ground, trade, vehicles, people, and the map fields the kit needs) for the owner to check. Next: the owner checks the list, parts in Blender, then the first kit test (one random spot rebuilt side by side).
- **Roads and borders study, done (22 Oct)** (`docs/lagos-study/roads/ROADS.md`): skeleton of real roads (in the 1:3 frame, real km: motorway 108, trunk 162, primary 270, secondary 423, rail 120; 121 bridges; frame = lon 3.005-3.737, lat 6.403-6.689, 90% of Lagos roofs); 819 places cut by real borders and named; every border measured; districts join only where built land really touches. In the frame, folded: 65% → 59, 60% → 48, 55% → 38. Pick 59 (VI apart from Ikoyi, Festac its own). 104 of the first study's 185 neighbour pairs do not really touch. 15 Google Earth checks listed (VI/Ikoyi, Ajegunle vs the central core, the west sprawl and Ikorodu belt need splitting by hand). Next: the owner picks a count.
- **Open for the owner:** the district count after the roads study; the name of Gidi's Obalende (working name Underdeck).

**22 Oct 2026, later: the district numbers and the video 1 street study.**
- **How many districts** (`docs/lagos-study/similar/SIMILAR.md`): 81 units cover all Lagos land, each with a fingerprint (character mix, density, roof size, height, grid, people, places); similarity between neighbours; the closest neighbours merge step by step. Districts at each similarity level: 85% → 78, 75% → 56, 65% → 36 (29 with tiny plain units folded in), 60% → 28 (23 folded). Below 60% unlike places chain into blobs. Recommendation: **23 to 29 districts, pick 29** (65%, folded). The owner decides. Merges to check in Google Earth first: Ikoyi with Obalende-Onikan, Festac into Okota-Ikotun, Gbagada with Maryland, Apapa with Trade Fair-Satellite Town, Alaba into the Badagry road, Ilupeju with Ladipo, Ajao Estate with the airport. Bad data: Isale Eko, Mushin, VI (joined roofs), Makoko (stilts). **Checked on Google satellite the same day** (`docs/lagos-study/similar/GOOGLE-CHECK.md`): 8 of the 10 doubtful merges are wrong (split them) and 2 are right (Bariga with Shomolu, Badore with east Lekki). Net about 29 districts with changed members; Google backs 29 over 23.
- **Video 1 test street, step 1 (reference study), started:** 11 Street View shots + `NOTES.md` in `~/gidi-data/research/google/video1-street/` (Ojuelegba, Oshodi, Obalende, Mile 2): ground, kerbs, puddles, litter, the deck and piers, danfo parks, trade, people. Obalende's danfo park under the deck is the closest real match to video 1. The owner (22 Oct): build Obalende, skip the other flyovers. Shots 12-16 + notes added; a helper is building it in gidi-game as `Play_Underdeck` (branch play/underdeck; invented names only in the game). Next steps of the plan: ground materials, dress the flyover set against the video's frames, play systems (levy run, heat, money, rep, HUD), people with cloth. Anything that costs money is priced and confirmed first.

**22 Oct 2026, step 1 done: the whole-Lagos study** (`docs/lagos-study/`: STUDY.md, councils.md, character/skeleton pictures; built on Google Open Buildings v3 + the 2023 heights, then Overture, WorldCover, WorldPop and knowledge, every claim sourced). Lagos is a fan from the Island; flow crosses at Oshodi and Ojota-Maryland; 17 character classes, zones measured. About 18-20 candidate groups (6 that could stand alone, 8-9 merges, sprawl to squeeze hard); the data does not set the number. Scale: houses real size means 1:4 keeps about 1 local street in 21, 1:3 about 1 in 11; the shrink can be uneven. Next: the picture study in Google Earth / Street View (32 spots in STUDY.md's last table; screenshots to `~/gidi-data/research/google/lagos-study/`), then the frame proposal for the owner.

**22 Oct 2026, late: the map starts again as Lagos miniaturised** (DECISIONS.md, same day). Step 1, now: understand how the whole of Lagos works (all councils, by character and by the road network) before cutting districts. Step 2: a proposal for the new frame (real network at the chosen scale, places grouped into districts with reasons), for the owner to check. Nothing is built until the owner passes it. The hand pass and the road fixes below are paused: they belong to the old frame.
