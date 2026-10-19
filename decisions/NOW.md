# Where the work stands (update at the end of every session)

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

**19 Oct (main session, Claude):**
- **The Danfo font is done** (gidi-game `Art/Fonts/DanfoBasic.ttf`, OFL): the owner's 2022 font on Alfa Slab One, spaced and kerned, with punctuation; X and Y redrawn. Brand sheet draft (colours approved): https://claude.ai/artifact/MxjXim5sLv27pNv1m5PCH3. Still to build: the wobbly brush font (no two letters alike), the Gidi plate system and its font (study Lagos plates first), a coat of arms, organic illustrations from the image model. The owner is still deciding the back-window lettering.
- **Real vehicle models, pipeline proven on the danfo** (gidi-game #14, #16): a Meshy reference sheet (no brand, the owner's D mark is the badge) → Meshy 3D (36 credits) → `tools/vehicle_prep.py` + a `spec.json` (true size, 80k faces, wheels on axles, the sliding door its own part, a cabin with benches, real glass, windscreen squared off). Rebuildable. Renders: `~/Real-world/research/models/danfo/`.
- **Danfos in Unreal at the data's 1,374 spots** (`gidi_heroes.py`, branch vehicles/heroes-in-unreal): the parked model (`danfo_static.glb`) imported once as Nanite, placed in each tile's level. The kit session is asked to stop drawing those danfos in the tiles Unreal imports.
- **Keke and okada reference sheets made** (`~/Real-world/research/models/keke`, `okada`; 12 credits). Their 3D step (30 credits each) waits on the owner allowing Meshy's 3D tool in Claude Code's auto mode.
- **Next:** wear per danfo (from the data's condition), D badge and plates as decals, keke and okada 3D, then korope, molue, BRT blue and red; plate study; brush font; run `tools/perf.sh`.

**18 Oct (main session, Claude):**
- **The Estate's streets redrawn from the study** (Magodo, Omole, Ikeja GRA; #103): a spine drive, parallel streets two plot rows apart ending in closes, two crescents, 8 gated links to the main roads instead of 17. Frozen again; all 17 districts pass.
- **Road types in the data** (#102, #103): close, crescent, drive, avenue, street, lane (`scripts/roadtypes.py`), on the board's road panel.
- **Unreal looks like the study now** (gidi-game #6, #7): the city was washed out by auto exposure and an extra gamma node (both gone; `gidi_look.py` sets the light). Textured surfaces (`gidi_surfaces.py`): detail, normals, rain streaks, grime from each face's wear, corrugated zinc, laid on from the world position (the web tiles' Draco packing ruins the kit's UVs). Noise textures for now (`tools/make_textures.py`); the owner is adding Megascans surfaces (`tools/fab_list.sh` lists what's in). Shots need time for new shaders (the grey checkerboard is Unreal's stand-in while they compile).
- **A kit session runs alongside** (Claude, its own worktree, `blender/` only, single-tile tests; it waits while `~/gidi-worktrees/out/LOCK` exists, which `tools/bake.sh` holds).
- **Next:** rebuild and import the Maze (walls, fixes) once the owner closes Unreal; swap the Megascans surfaces in, capped at 2K; measure frames per second on the laptop; a house `ac` count in the data; then real models for what repeats and the City Sample crowd at the data's people; then the next district's network from its study.
- Research: estate network notes in `~/Real-world/research/google/estate/NOTES.md`; the two reference videos in `~/Real-world/research/games/`.

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
- **Houses age in Unreal too** (`gidi_kit/wear.py`): the Blender shader's wear never reached Unreal (its material read the vertex colour alone; it now adds fine grime from the wear in the vertex alpha). The walls now carry the big shapes in their colours and in thin overlays: splash, fading, grime runs, rust from the bars, patches, broken render, meter boxes on the data's service drops. AC units are drawn only where a house's data counts them (`ac`, not in the data yet). Pictures: `blender/wear_sheet.py -- --vc` (Unreal's view, back faces culled).
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
- **Later: the Google Earth study.** The owner sends screenshots of each inspired place: straight down from about 300 m (keep the scale bar and coordinates), a tilted 3D view, and Street View. They live outside the repo (`~/Real-world/research/google/<district>/`); only measurements go into the data (study yes, lift no). Start with the Maze and the Hub.
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
