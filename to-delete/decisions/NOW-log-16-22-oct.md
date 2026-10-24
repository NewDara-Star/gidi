# The old log of decisions/NOW.md, 16-22 Oct 2026

Moved out of NOW.md on 24 Oct: the old generated map's work (history). The old 22 Oct handover is kept here too.

**HANDOVER, 22 Oct 2026 ~23:00 (owner switching Claude accounts). Start here.**
State: the new map (real Lagos at 1:3, 51 districts) has its format, its board tools and its first district's roads; the old-town kit has had 4 random eye tests. Nothing is running. Serve the board from main: `cd ~/gidi && ~/.venvs/gidi/bin/python scripts/board_server.py --port 8779`, open `http://127.0.0.1:8779/web/board.html?frame=new` (port 8778 serves the old regen worktree: old code).

Decided today (DECISIONS.md): one ground truth (#198: the kit draws only map records, no seeds/scatters); the map format's four calls (#205: brushes yes, small things as table rows, dress layer to its own repo past 1 GB, working names for all 51 now). Owner, not yet in DECISIONS: district and place names are **sound-alikes in the real name's own language** (Yaba→Saba, Computer Village→Gadget Village; `docs/lagos-study/roads/NAMES.md`, #208); border calls are settled by a vote of several map sources, the owner is not a cartographer (#201, all 17 "likely").

Waiting on the owner:
1. **Mùṣá (Mushin, d15) road plan, PR #214: the owner's calls are in (23 Oct), merged.** The south lobe below Itire Road went to Surulere (its 7 streets listed in `map/d15/STREETS.md` for Surulere to take), the line moved north-west so all of Ladipo market is in Mùṣá (Ladipo Street on its real line, a market lane, the market as a place), the expressway's east service road is its own street (the west one is Isolo-Ladipo's), and the rail and Mushin station are records (new `rail` and `station` types; the station's area and platform are placeholders). Still to do: Western Avenue's side road, the Isolo Road interchange, the tidy-ups (Isolo Road kink near Omowunmi, Olushoga's zigzag), then plots and buildings.
2. **Names** (#208): Lagos → "Lagoon" in-game, or just "Gidi"? Ìkòrodò / Okotun too close? Mile 2→Mile 10, Mile 12→Mile 20 OK? Mùṣá reads like Hausa "Musa"? Tone marks (Òkòtó, Agbègbè, Ṣọmọlá, Ìtìrí).
3. **Kit eye tests** (all fails so far, owner's eye judges): `~/gidi-data/research/google/kits/old-town/tests/` ot175 (5 passes, Mushin), ot91 (Balogun), ot149 (Ayantuga, Mushin), ot73 (Epe town road), ot45 (Ladipo St median and container lorries, 23 Oct); each folder has side_by_side.jpg, NOTES.md (what still differs, next steps). Owner's last word: "we need to be a little bit more detailed". Recurring gaps: busy frontages (hung clothes, crowds), leafy trees/bush, okada rider, sandy ground near houses.
4. **Download OK?** a CC0 grass texture (Poly Haven, ~10-20 MB) for verges.
5. **Board convention:** on a face, a window's/stain's z is its bottom (sill), u its middle (MAP-FORMAT); the kit must read the new map that way.

Next, in order:
- **Board** (PRs #209, #211, #213 done: plan tools, Stamp K, Frontage E, lean-tos on walls, dress tiles, face editor C, goods O, litter X, ground D, relief H): still to build: district outline editing (brushes, person spots, pole wires and the clock done 24 Oct, see above), load only districts in view. List in `docs/MAP-FORMAT.md` next steps.
- **Kit** (PRs #193-#212; `legacy/blender/gidi_kit/` oldtown.py, facade.py, goods.py, roadbed.py, textured.py, draft.py; `legacy/blender/kit_test.py`): it reads only records now (MissingRecord on a gap); converted test-spot records use KIT names, a converter to the MAP-FORMAT names is needed, then write them to `map-stamps/<name>/` so they stamp onto the board. Next random draw: **ot13** (the 6th; seed 20261022, `random.choice` over shots.tsv; ot45 done 23 Oct). Shared parts used by the frozen old map: any change must keep legacy tiles 6,12 / 7,12 / 8,13 byte-identical.
- **Map:** after the owner's review of #214, Mùṣá's plots and buildings, then the other six core districts (Ayégúnlẹ̀ 9, Agunda 12, Sọ̀rọ̀lérè 13, Ìtìrí 14, Ṣọmọlá 27, Gbàgede 28 — see NAMES.md).
- **People and cars** come from Unreal's City Sample, not Blender boxes (owner agreed); Unreal only with the owner's go, one heavy job at a time.
- Laptop: restart still advised (10 GB wired after the freeze; swap 4.3 GB on 24 Oct); Chrome extensions to review (OrangeMonkey, Lightning Autofill, Google Forms Auto Filler).


**22 Oct 2026: STOP rule-tuning.** The generated base is frozen (`DECISIONS.md`, 22 Oct; `rebuild_areas.py` refuses to run). Next work is the hand pass on Ìbùdó: go area by area through the checker pictures (`scripts/draw_area.py`, with `GIDI_LOST_DIR` to see what was not kept) and the `check_real` fails below, and fix each gap with hand edits in `web/hand/hub.json`: add/move/reshape buildings, add or delete streets, add places. Worst areas first: spare_parts and ilupeju (picture score 2), then the 3s. The building-line question is no longer a rule change: where a real building should stand closer to the road, place it by hand.

**22 Oct 2026, real Lagos roads (owner decision, #174) and the flow audit (`docs/FLOW-AUDIT.md`).** The building line and fixed road widths are no longer rules: roads on their real lines at real widths, buildings on their real spots, a clash moves the road. Measured in Ìbùdó: streets and lanes are 86% within 2 m of their real lines; the problem is the big roads: 86 real buildings (about 50,000 m2) stand where Gidi put the Ring Road or a main and real Lagos has none (ilupeju worst: the Ring Road cuts diagonally across houses instead of running between the real service roads). Plan: (1) move the Ring Road and off-line mains onto their real lines by hand, ends kept at district edges; (2) put the real buildings back by hand; (3) take the building line out of the bake's clean-up and add a check flagging a building across a road where the real road does not run; (4) real widths, no walkways, once the frame is settled. City flow: about two-thirds of Lagos's flow; the mainland middle is missing (no Oshodi-Oworonshoki corridor, Ìbùdó 1.3 km south-west of its real places, no exit north, Port and Railside dead ends). Owner to choose the frame fixes.

**22 Oct 2026, hand pass done so far (#170-#172):** every real building an area lost for "no way within 40 m" is now a hand edit in `web/hand/hub.json` on its real footprint, with footpaths routed between existing buildings into the yards (none crosses a building), in spare_parts, ilupeju, oshodi_core, civic, osolo_way, itire_rd, surulere, airport_rd and ajao (about 260 buildings, 50 footpaths). Where a Gidi building already stood, or two neighbouring areas listed the same real building, the extra copy was left out. The edits were made with a scratch router (out of the repo): take the area's lost footprints from a `GIDI_LOST_DIR` run, drop any on an existing building, route each cluster's footpath on a 1 m grid round the buildings from the nearest way. Before/after pictures were sent to the owner. All 17 districts pass, bake deterministic. Biggest visible gain: civic's empty middle. Left on purpose: the building-line losses (owner's rule; place by hand where a building should stand closer). Next: the areas the checker scored 3 that still look off beside their real place (arena, ojuelegba's west inset), the stray edge roads, then the R3/R6 single streets, all by hand on the board.

**21 Oct 2026 (main session, Claude; branch `regen/areas`, worktree `~/gidi-worktrees/regen`).** The owner asked: close the gaps, make every fix reach what is already built, check how close each area is to the real place and to the livable-world rules, and find out why rebuilds were slow.
- **Fixes reach everything built** (new rule in `DECISIONS.md`): Ìbùdó's 15 areas are no longer kept as 29,000 frozen hand edits. `scripts/rebuild_areas.py <base>` builds all 15 again from their real places into `web/hand/gen/hub.json` (generated, never edited by hand) in about 5 minutes; the bake applies it before `web/hand/hub.json`, which now keeps only the real hand fixes (29). After any change to the builder (`scripts/hand_spots/ibudo_real_area.py`), the child plan or the real data: make a base (bake with `web/hand/gen/` moved away), run `rebuild_areas.py` on it, then `~/gidi-worktrees/tools/bake.sh <worktree>` (outside the repo).
  - Each area is one `clear area` edit plus what it adds; the clean-up (`scripts/autoclean.py`: building lines, overlaps, reach, scraps) runs in every bake, so a fix to it reaches every area.
  - After all areas: cut-off street groups are joined to the nearest rooted way ("Gidi link"), and houses out of walking reach of a chemist, church/mosque or school get one (Overture misses most small ones).
  - Story places (type `story`) survive any area clearing.
- **Why rebuilds were slow:** three bakes per area pass, three passes, and 30,000 replayed edits each doing linear lookups. Now one bake (about 6 minutes, 4 of them street furniture) after one rebuild; `~/gidi-worktrees/tools/bake.sh` bakes twice to prove the bake is deterministic, about 13 minutes.
- **New checks:**
  - `scripts/check_real.py` (run by the bake script, written to `out/cd/real.txt`): per area against its real place: buildings and built-up area, street length by kind, twin streets on the map, every street has a twin, kinds of place, livable things the photos show (R5), and no real names anywhere (N1).
  - `scripts/check_rules.py` + `decisions/CHECKS.md`: every rule in `DECISIONS.md` mapped to the check that tests it. Five rules have no check yet: safe ground, surfaces against the photos, market lanes kept clear, every type has a real twin, the item register.
  - `scripts/draw_area.py <area>`: Gidi beside the real footprints and roads, side by side, for a checking agent.
  - Check 17: every hand edit landed (the bake lists misses in `hand_misses`).
- **Real names:** the name pickers use common surnames, and some match real streets near the studied places (Taiwo, Makinde, Babatunde...). `docs/hand/realnames.txt` (made by `scripts/realnames.py`) lists every real name near the twins; the bake swaps any clash for an invented name at the very end (`realnames.rename`).
- **District checks for Ìbùdó:** all pass again after the rebuild (overlaps, cut-off lanes, reach, hand edits landed). The clean-up now repeats until nothing is left, compares footprints as they are stored (rounded to 0.1 m), and cuts 15 cm past a building line so rounding cannot bring a touch back; the join's links are always lanes (the clean-up takes street pieces under 3 m as scraps).
- **Merged (22 Oct):** #156-#158 (rebuild, clean-up, real names, R1 cut-back); #159 + #161: a real dual carriageway is one Gidi main (counted once where a run over 30 m lies within 12 m of a counted main; a junction is not a second side; mains' twins found within 10 m; Gidi's arterials/expressways left out of R2 main, like the real trunk roads); #162: a real place beside another kind of place is kept (it was dropped within 15 m of any place; 26 more places, ajao's government office and itire_rd's clinic back). All 17 districts pass, bake deterministic, 680/680 photographed twins kept.
- **Still failing (check_real, 23):**
  - R2 main: ilupeju 116%, itire_rd 128%. Every map main there lies on a real main's twin, so what is left is how the real figure is counted (e.g. slip roads), not extra roads.
  - R2 lane: airport_rd 130%, civic 148%, itire_rd 119%. Not stray roads: the joins. The builder runs a real lane on up to 30 m past its area's edge to the nearest way (the seam), and links join cut-off groups to a main (31 at rebuild, 4 at bake; e.g. an 81 m link in civic at (7955,3939)). Decide: count joins as Gidi's own (leave them out of R2), or find the real connection instead of a straight link.
  - R3/R6: single lanes/streets without a twin or gone, 1-6 per area.
  - Building lines: about 100,000 m2 of real built-up is lost to them (main 6.3 m, street 4.1 m from the centre line; real Lagos builds closer): the owner's rule, so ask before changing. About 30,000 m2 more has no way within 40 m.
  - R5 livable: the map has no POS stand, loading bay, okada/keke rank, vulcaniser, kiosk, stalls or betting types yet: they come with the item register.
- **The checker agent (22 Oct, first run):** `python3 scripts/draw_area.py <area> <out.png>` for all 15, shrink them (`sips -Z 1600`: full size stalls an agent), then one agent looks at each beside its real place and scores it 1-5. First scores: church_st, barracks, stadium 5; civic, mafoluku, ajao, surulere 4; oshodi_core, arena, ojuelegba, osolo_way 3; spare_parts, ilupeju 2; airport_rd, itire_rd too thin to judge (draw_area needs a taller frame for strips). Its "wrong expressway paths" and "no Oshodi cloverleaf" are Gidi's layout lines, by design.
  - Fixed from it (#165): a later area's clear dropped every building it touched, so big real warehouses went; now cut back. +208 buildings, +60,000 m2.
  - Still to look at from it: thin housing in ilupeju's west half and south-east, ojuelegba's west inset; civic's compound perimeter rows; stray edge roads (osolo_way west edge, barracks south edge, surulere north-east strip).
  - Then: the checking agent with `scripts/draw_area.py` pictures.

**19 Oct 2026.** Gidi v2 is the live map, hand-made from here on (the stop line, `DECISIONS.md`).

**Done:**
- **All 17 districts frozen,** and all 17 pass every check (`scripts/check_district.py`, on the finished map). The bake is byte-identical run to run.
- **The Maze and the Hub, hand-made** (`docs/hand/maze-hub-lagos.md`):
  - **The opening, north to south:** Tunde's face-me-I-face-you block, the walk-up past the vendors, Mama Bisi Provisions (the steal: bread), Ladi Lane (a 150 m straight aisle), the boss's post.
  - **The rest of the Maze:** Gang Canal crossed twice, Press Row, Transformer 44, the buka, betting shops.
  - **The Hub:** the boss's motor park on Animashaun Street, the union office (the first cutscene, a proposal), the gate and levy table, the agberos, police kiosks, the rail market.
- **Marigold Junction** (after Maryland), where the Capital, the Maze and Food Gate meet: the Glasshouse mall and a footbridge.
- **The borrowed-Lagos list** (`docs/hand/borrowed-lagos.md`): 30 real places mapped onto Gidi to reimagine.
- **Hand files can now:**
  - add, delete, cut and name roads
  - add structures
  - set surfaces
  - add, move and name places and furniture
  - add and delete plots
  - thaw a frozen district (`GIDI_THAW`) for road work

**19 Oct, later (main session, Claude, with two helper agents):**
- **Vehicles built part by part** (gidi-game): the danfo (#22-#25, twelve recipes #32, wearing paint and photo mode #33), the keke (#29), the molue (#30, from memory: needs the owner's photo), the BRT blue and red (#31). Shared helpers: `tools/vehicle_kit.py`, renders `tools/vehicle_look.py`, game models `tools/vehicle_export.py`.
- **In the game:** built danfos at every danfo spot in Àdàrú (a recipe per spot, its own plate, paint worn by the data's condition through `M_GidiPaint`); kekes and molues being added (branch vehicles/keke-molue-game, kit/heroes-keke-molue). After a full reimport the game needs ~20 minutes to compile and settle before a shot is fair.
- **Gidi Brush** is a real font (#28): four drawn copies of every glyph, rotated by `calt` so repeats differ.
- **Photo mode** (`tools/photo.sh`): the GOD IS THE GREATEST danfo, plate ADR-777GD; take 2 sent to the owner; take 3 running (no letterbox, rust in clusters). Still reads as a game: flat road and buildings, paint without reflections; a tight shot is the realistic target for now.
- **UI:** the main menu mock (https://claude.ai/artifact/UeeKiehnc3JQUkpfeiDs5V): Danfo Basic menu, a Gidi vehicle and the district's name beside it, black and white or colour, crumpled-paper texture (ambientCG Paper003, CC0) on the background only. The brand sheet is updated (draft 2).
- **Monuments:** `docs/hand/monument-briefs.md`: seven to Meshy from words (concept picture first, 6 credits each, then 3D on approval), The Reach from the owner's picture, the structures built in Blender. Waiting on the owner's yes for the 42-credit concept round.
- **Owner's asks pending from him:** a molue photo, The Reach picture, Fab wear textures (chipped paint, rusty paint, grime streaks), the Capital's name, black and white or colour for the menu.

**19 Oct, afternoon (main session, Claude):**
- **Districts renamed** (#118): names a conductor can shout, mostly Yoruba: Àdàrú (the Maze), Ìbùdó (the Hub), Ẹ̀gbẹ́-Irin, Ọjà-Ńlá, Etí-Òkun, Òkè-Ọlà, Èbúté-Ńlá, Ìlú-Omi, Ẹnu-Ọjà, Igbó-Ọ̀la, Ààlà, Ọ̀dàn, Pápákọ̀, Saba; Old Island, The Estate, The Capital stay English (the Capital not yet discussed). The old English names are nicknames (`nick` in the data).
- **Plates on the Lagos base** (gidi-game #26, #27): flag, GIDI, NO DEY SLEEP, Gidi's outline, palms, the district's name; ADR-123KD; embossed and glossy in the game.
- **The danfo built part by part** (gidi-game #22-#25, `tools/danfo_build.py`): the T3 base measured, Gidi's tweaks listed; the owner's D in 3D; lettering in the brush style (Titan One wobbled, white flecks) and printed stickers as thin 3D pieces.
- **The kit leaves danfos and okadas out** (#117); Unreal places real models (Meshy danfo and okada for now, each with its own embossed plate).

**Parked, to come back to (the owner asked, 19 Oct):**
1. **The build order's main line: one Maze (Àdàrú) street to the look target, end to end** (real models, the crowd, a walkable character, measured on the laptop). Everything vehicle-side feeds this.
2. Unreal look fixes from 18 Oct: a building's paint lost under its scan, orange dust strips, blue ground patches, plain flat roofs.
3. ~~`tools/perf.sh`~~: removed 24 Oct (owner), never run; `tools/measure.sh` measures the play levels.
4. The built danfo: recipes (a dozen variants), the wear material (needs Fab: chipped painted metal, rusty painted metal, grime/leak decals), into the game in place of the Meshy one.
5. The other vehicles the danfo way: keke (its Meshy 3D blocked by auto mode; may not need it), korope, molue, BRT blue and red.
6. Gidi Brush as a real font file (lettering exists only as a layout tool).
7. Coat of arms options; organic illustrations from the image model; the brand sheet artifact to bring up to date.
8. The main menu (God of War style, a monument beside the menu: black and white or colour, open) and the wider Gidi UI (the owner is collecting references).
9. The Reach to Igbó-Ọ̀la's Carnival Avenue (decided, not yet in the data); Parade Square needs a new centrepiece.
10. Bus stops and junctions named the Lagos way, for the conductors' calls.
11. Data: a house `ac` count; the ground cut along gutters.
12. The kit session stalled since 03:00 on kit/lockups (lock-ups and shop fronts weathered, unpushed); shop signs in Unreal (`gidi_signs.py` written, not run).
13. The Google Earth study of the next districts.

**19 Oct (main session, Claude):**
- **The Danfo font is done** (gidi-game `Art/Fonts/DanfoBasic.ttf`, OFL): the owner's 2022 font on Alfa Slab One, spaced and kerned, with punctuation; X and Y redrawn. Brand sheet draft (colours approved): https://claude.ai/artifact/MxjXim5sLv27pNv1m5PCH3. Still to build: the wobbly brush font (no two letters alike), the Gidi plate system and its font (study Lagos plates first), a coat of arms, organic illustrations from the image model. The owner is still deciding the back-window lettering.
- **Real vehicle models, pipeline proven on the danfo** (gidi-game #14, #16): a Meshy reference sheet (no brand, the owner's D mark is the badge) → Meshy 3D (36 credits) → `tools/vehicle_prep.py` + a `spec.json` (true size, 80k faces, wheels on axles, the sliding door its own part, a cabin with benches, real glass, windscreen squared off). Rebuildable. Renders: `~/gidi-data/research/models/danfo/`.
- **Danfos in Unreal at the data's 1,374 spots** (`gidi_heroes.py`, branch vehicles/heroes-in-unreal): the parked model (`danfo_static.glb`) imported once as Nanite, placed in each tile's level. The kit session is asked to stop drawing those danfos in the tiles Unreal imports.
- **Keke and okada reference sheets made** (`~/gidi-data/research/models/keke`, `okada`; 12 credits). Their 3D step (30 credits each) waits on the owner allowing Meshy's 3D tool in Claude Code's auto mode.
- **Later on 19 Oct:** the danfo has the owner's D badge front and back and a tint per condition; it shows in Unreal on a Nanite material made for hero models (`M_GidiHero`). **Gidi's number plates** (gidi-game `Art/Plates/sheet.png`, `tools/plates.py`): the Gidi Plate font (custom, from Montserrat Bold: narrow, even strokes, slashed zero, a G with a crossbar at the owner's ask), five classes by colour (commercial danfo yellow, private blue, government green, services with a red band, transit blue), district code + three figures + two letters; every vehicle prints its own number from one material (`M_GidiPlate`). The motto "NO DEY SLEEP" is a placeholder for the owner. **The okada** is the second hero vehicle. The keke's 3D step is blocked by Claude Code's auto mode (Meshy spends credits): the owner allows `meshy_multi_image_to_3d` or approves the prompt. Check shots now wait in real seconds and capture the game window (`tools/shot.sh`).
- **Waiting on the kit session:** stop drawing danfos and okadas in the tiles Unreal imports (until then the kit's block versions show through the models).
- **Next:** the keke, korope, molue, BRT blue and red; the full Montserrat family for a lighter Gidi Plate (the plate's small lines) and a Gidi UI face; the brush font; the coat of arms (it replaces the plate's GIDI band); ~~run `tools/perf.sh`~~ (removed 24 Oct; `tools/measure.sh`).

**18 Oct (main session, Claude):**
- **The Estate's streets redrawn from the study** (Magodo, Omole, Ikeja GRA; #103): a spine drive, parallel streets two plot rows apart ending in closes, two crescents, 8 gated links to the main roads instead of 17. Frozen again; all 17 districts pass.
- **Road types in the data** (#102, #103): close, crescent, drive, avenue, street, lane (`scripts/roadtypes.py`), on the board's road panel.
- **Unreal looks like the study now** (gidi-game #6, #7): the city was washed out by auto exposure and an extra gamma node (both gone; `gidi_look.py` sets the light). Textured surfaces (`gidi_surfaces.py`): detail, normals, rain streaks, grime from each face's wear, corrugated zinc, laid on from the world position (the web tiles' Draco packing ruins the kit's UVs). Noise textures for now (`tools/make_textures.py`); the owner is adding Megascans surfaces (`tools/fab_list.sh` lists what's in). Shots need time for new shaders (the grey checkerboard is Unreal's stand-in while they compile).
- **A kit session runs alongside** (Claude, its own worktree, `legacy/blender/` only, single-tile tests; it waits while `~/gidi-worktrees/out/LOCK` exists, which `tools/bake.sh` holds).
- **Next:** rebuild and import the Maze (walls, fixes) once the owner closes Unreal; swap the Megascans surfaces in, capped at 2K; measure frames per second on the laptop; a house `ac` count in the data; then real models for what repeats and the City Sample crowd at the data's people; then the next district's network from its study.
- Research: estate network notes in `~/gidi-data/research/google/estate/NOTES.md`; the two reference videos in `~/gidi-data/research/games/`.

**Overnight 17–18 Oct (Claude, on its own; the owner reviews in Unreal):**
- **The Maze is in Unreal.** `~/gidi-game`: open `Content/Gidi/Generated/Maps/Gidi_City`, press Play, fly with WASD. 22 tiles, each its own level streamed into the city; sun, sky, fog; every surface on four master materials that read the kit's colours. Pictures from inside Unreal: `~/gidi-game/Saved/Shots/` (mat3 from above, street1 at eye level).
  - Import: `tools/import.sh maze` (or `all`, or a tile list), editor closed. Only changed tiles come back in. A 16 GB Mac can't hold full-detail tiles (27 GB in one process), so Unreal takes the light web tiles, a few per Unreal run.
  - Pictures: `tools/shot.sh "x y z pitch yaw" name` (map metres).
  - Learned: the vertex-colour node's output name is empty, not "RGB" (the city came in white); adding a streamed level makes it "current", so the city level is saved by name.
- **Everything the kit invented, batches 1 and 2a, in the data** (#96, #97): vehicles, people, boats, trains, signs, monuments by rule; the **ground-use map** (what each square metre is for, who may be on it); which building each place takes over; each house's roof, tank, dish, tyres, unfinished top; generators, service vehicles, police pounds. The board shows and checks all of it (check 16: things on their ground).
- **Fab and Megascans**: Claude can't browse the owner's library (no scripting in the Fab panel). The owner adds assets in the editor (Window → Fab → Add to Project) into `Content/Fab`; from there the importer can use them. First wish list: laterite, cracked asphalt, concrete, peeling plaster, rusty zinc, mud; coconut and oil palms, a shade tree, weeds; chairs, jerrycans, drums, rubbish.
- **Next:** batch 2b (inside the plots: stalls, graves, pumps, cows, the parks' trees), batch 3 (the ground painted: road wear, potholes, litter, sand, mud), shop signs in Unreal (`gidi_signs.py` is written), the rest of Act 1 in Unreal, then the Google study and Claude's design pass.
- Notes: the bake's Python is `~/.venvs/gidi`; worktrees live in `~/gidi-worktrees` (macOS clears /tmp). A locked Mac locks the keychain, and git can't push until it's unlocked.

**The kit session (18 Oct, Claude; one branch and PR per topic, single-tile tests only):**
- **Houses age in Unreal too** (`gidi_kit/wear.py`): the Blender shader's wear never reached Unreal (its material read the vertex colour alone; it now adds fine grime from the wear in the vertex alpha). The walls now carry the big shapes in their colours and in thin overlays: splash, fading, grime runs, rust from the bars, patches, broken render, meter boxes on the data's service drops. AC units are drawn only where a house's data counts them (`ac`, not in the data yet). Pictures: `legacy/blender/wear_sheet.py -- --vc` (Unreal's view, back faces culled).
- **Zinc roofs sheet by sheet** (`gidi_kit/zinc.py`): Unreal used to get one flat face per roof slope. Now sheets, rust toward the eave, new sheets among old, laps, sag, rust run from the nail lines and sheet edges (the ribs come from Unreal's material); flat concrete roofs stained.
- **Street clutter from the data:** the gutters are drawn at last (open, slabs, blocked); the generators are real petrol sets in rebar cages; the traffic wardens' post has a builder.
- **Compound walls weathered, the light tiles back on budget:** tile 25,9 is 1.38M faces (main before the kit work: 1.31M; at the peak: 1.77M). The light tiles pair zinc sheets, drop thin bars' end caps and hidden gutter faces, and draw fewer streaks; the full build keeps it all. Grime strips no longer hang in the air at wall corners.
- **Inside-out boxes fixed:** the kit's wall frames are mirrors, so sills, frames, doors, signboards and balconies came out inside out; Unreal culls back faces, which is why shop signboards showed black.

**Done 17 Oct:**
- **The map page went blank again** (#91): a comment swallowed a closing brace in the 3D labels. Fixed; the page is now loaded in a browser after every viewer change, not only rebuilt.
- **Unreal: go.** The owner installed Unreal Engine 5.8.3. The game lives in its own private repo, **`~/gidi-game`** (NewDara-Star/gidi-game): an empty Blueprint project with Python, the editor scripting tools and Epic's experimental MCP plugin (it starts with the editor on http://localhost:8000/mcp). The rules: nothing the importer makes is committed (`Content/Gidi/Generated/`, rebuilt from the gidi data every import); hand-made assets go through Git LFS and are listed in `ASSETS.md`. First goal: walk the Maze in Unreal, move a house on the board, re-import, see it move.
- **Road ends** (`scripts/roadends.py`): 2,725 road ends touched nothing. Every end is now one of: joined on to the road it was heading for, cut back (it served nobody), a close with a turning space (drawn in 2D, on the board and in 3D), at a house or gate, at the water, or loose (the board flags it). The Northern Road runs on out of the map instead of stopping in the bush.
- **No more kit-placed poles and lights.** Out in the bush the kit still put up its own poles and street lights (one stood in the middle of a road). They are in the data now like everywhere else (`furniture.py`, bush pass).
- **Meshy** (the owner's paid plan): fine for props and placeholders, not for the city's buildings (those come from the data). Private ownership on paid plans; no real brands or logos; every Meshy asset listed in `gidi-game/ASSETS.md`.

**Next, booked by the owner:**
- **Hand-making happens on the drawing board** from now on (owner, 16 Oct): place and fix things there, then "bake the board".
- **The Google Earth study waits until the city is in Unreal** (owner, 17 Oct): first the Maze importer, then the study.
- **Later: the Google Earth study.** The owner sends screenshots of each inspired place: straight down from about 300 m (keep the scale bar and coordinates), a tilted 3D view, and Street View. They live outside the repo (`~/gidi-data/research/google/<district>/`); only measurements go into the data (study yes, lift no). Start with the Maze and the Hub.
- **The owner storyboards the first cutscene** (the boss's office) as comic panels.

**Done since (16 Oct, night):**
- **Monuments by hand,** the modeler's pieces (`docs/hand/borrowed-lagos.md`): the Founder, the Marigold Screen, the welcome arch, the Saxophonist, the Scrap Rider, the Port Light, the Hunter, the Market Clock, the Masquerade.
- **Parade Square on Old Island,** with **The Reach** at its centre (the owner's choice) and gate riders.
- **The Crown Hall** (after the National Theatre) in the Port.
- **Atlantic Reclaim** (after Eko Atlantic): new land in front of the Heights, a sea wall promenade, glass towers.
- **The Railside bakeries:** a bread depot and hawkers.
- **A name audit:** every real Lagos name out.
- **The boss's office:** dingy and makeshift (the first cutscene, confirmed).

**Done since (16 Oct, afternoon):**
- **The Act 1 kit pieces** by the modeller (#73): the face-me block, the boss's office with its cutscene interior, agberos, the buka, the vendors, bread hawkers, the police kiosk, the rail market, the task force truck, overhead signs, and Ladi Lane's open lock-ups. Brief: `docs/kit/MODELLER-BRIEF-ACT1.md`.
- **Big tiles split** so the browser can load close-ups (#71).
- **Motor parks packed** with buses, yard to yard (#69).
- **The map page** no longer goes blank (#70) and counts its 17 districts (#75).
- **Bridge ramps fixed** (#75, #80): they stopped growing every bake, and the bake's last step no longer puts the old frozen ramps back. Folake Road's rail bridge is 343 m (was 538) and lands; no ramp ends in the air.
- **No trees in the sea** (#81). **Full builds cover the whole map** (#81): the runner had the v1 height hard-coded and skipped the Atlantic coast.
- **77 beach huts out of the sea** (#82): the v2 coast has no beach strip yet.
- **The 3D city rebuilt** with terrain, the new pieces and every fix: 443 tiles, copied into `~/gidi/web/city` on 16 Oct.
- **The drawing board** (`docs/BOARD.md`): a clean plan of the city to scale (road edges, plots, walls, houses, furniture, places) where everything can be checked, moved, turned, deleted and added; edits save as hand edits. Start it with `python3 scripts/board_server.py`, open http://127.0.0.1:8777/web/board.html.
- **The board reshapes and resizes everything** (#86): drag corners and road points, exact sizes and angles. **Compound walls are in the data** (#87): the board shows and edits them, the 3D only draws them (55,666 pieces, none on a road).
- **The browser 3D is light tiles only** (#86): faster builds and no Safari memory crashes.
- **Full builds can stand on the terrain** (`city_run.py --terrain`, #76). A full rebuild with terrain was started 16 Oct; the old 3D tiles (15 Oct, v1 map) explained the trees in the water and the poles in the road.
- **Life in Gidi** (`world-life.md`): the owner's world-building ideas.

**Next:**
1. The rest of the borrowed list:
   - the Northern Road BRT
   - Saba's market tower and Costa Circle
   - the Channel Terminal and the Railway Compound
   - Eastgate Park and Creekside Plaza
   - the Canopy Walk, Ajara Market
   - the Fairground and Carnival Avenue
   - the Cattle Ground
   - the Border's Heritage Museum and beach arch (with care)
2. Each district's "unmistakably Lagos" list (like the Maze and the Hub), placed by hand.

**Later:**
- the look pass from the references
- kerbs (roads pass 4)
- isms groups
- the data delete-later list
- **Gidi's Atlantic beach:** a sand strip along the Frontier and Heights coast, with the beach huts back on it (hand pass)
- the Glasshouse mall and the campus have no kit builders yet (the full build lists them as gaps)

## 19 Oct (late): Ìbùdó as a district
- Market Road is now a plain street (#133, merged).
- Ìbùdó judged as a whole: it doesn't make sense as a district. Plan v2 is proposed in IDEAS.md (`docs/hand/ibudo/plan_v2_proposal.png`): two cores (Oshodi and Ojuelegba), three crossing roads, five belts, several markets. **Next:** the owner says yes or changes it, then rebuild the district plan (thaw the hub, hand ops), keep spot 1, then go on to the match passes. Still to do: delete the stray school pin at (8528, 4096).

## 19 Oct (night): Ìbùdó, the child-district method
- **Rule (DECISIONS.md, #137):** a district is the child of its real inspirations. Ìbùdó = Oshodi + Ojuelegba: study both whole, see what Ìbùdó can hold, then place every street and place from a real one, each with its own pictures. Nothing invented.
- **Running:** a study agent is covering both places (tiles, inventory, ~30 Street View streets) into `~/gidi-data/research/google/ibudo/study/` (INVENTORY.md).
- **Next:** from the inventory, the capacity of Ìbùdó's 4 km², then a child plan with every street labelled by its real source (owner checks), then build by hand, then pictures per street (thousands).
- **Kept on branch `hand/ibudo-plan-v2` (not merged):** the big-pieces version (rail through the crossing, three roads, stadium moved, markets, barracks); all checks pass. Only the rail move is decided; the rest gets checked against the study. "Adekoya Road" there is a real Oshodi street name: rename it.
- **Twins (docs/TWINS.md, #135, #136):** every type has a real twin; 44 of 210 have pictures. Generic "near the area" pictures are type references only, not street twins.
- New hand ops in that branch: `add path`, `delete path`, `delete structure` (scripts/hand.py); checker reads hand-edited paths.
