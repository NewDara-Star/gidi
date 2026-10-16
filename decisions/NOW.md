# Where the work stands (update at the end of every session)

**16 Oct 2026, late.** Gidi v2 is the live map, hand-made from here on (the stop line, `DECISIONS.md`).

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

**Next, booked by the owner:**
- **Saturday 18 Oct: the Google Earth study.** The owner sends screenshots of each inspired place: straight down from about 300 m (keep the scale bar and coordinates), a tilted 3D view, and Street View. They live outside the repo (`~/Real-world/research/google/<district>/`); only measurements go into the data (study yes, lift no). Start with the Maze and the Hub.
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
