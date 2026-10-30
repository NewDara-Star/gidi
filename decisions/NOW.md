# Where the work stands (update at the end of every session)

**Start here.** Read `DECISIONS.md` (the standing rules; replaced ones are in `HISTORY.md`), then this page. What the
repos hold: `CODEBASE.md` and `docs/inventory/` (`scripts/inventory.py`). The real Lagos research: `docs/RESEARCH.md`.

**This page holds only what is live** (owner, 29 Oct: a page every session loads must not grow with history). What is
done is in `DONE.md`: one line per ticked item (date, what, PR, ids), and, under "NOW.md on 29 Oct", this page as it
stood before it was cut, word for word, with every measurement and reading behind the lines below. To find past work:
`git log --all --grep=<id or word>` (every commit's `Checked:` paragraph), then `grep -n <id> decisions/*.md`. Search
by id (rd-..., b-..., jn-..., dNN, #PR) first: an id has no synonyms.

**Running order** (owner, 25 Oct: "keep a running order". Work down it without asking "next?"; when an item is merged
and checked, its line moves to DONE.md; add new ones where they belong, and say here when the owner reorders it).

000. [ ] **The network to a drive, first** (owner, 28 Oct, DECISIONS "The whole network first, to a drive in Unreal").
   Districts already drawn are leftovers while this is built (DECISIONS, owner 29 Oct): they never move a network road,
   get no fixes or long notes; a clash with one is one line in that district's list (below, "District leftovers").
   (a) Third Mainland Bridge, Ikorodu Road: done (DONE.md).
   (b) The other main roads in d00 (`scripts/city_network.py`'s list), every junction a shared point named for its real
   place and district; slip roads and ramps at real length (DECISIONS "1:3 sets where things are"):
   - Corner sweep finished 30 Oct (passes 1-16, each in DONE.md): d00 has no ROAD corner rows left. For the street
     pass: the bypass's end at Egbe Road
     rd-6d1e566d is eased inside Overture's hook by up to 8 m; its junction waits for a published design or the street pass.
     Orchid Road's small roundabout at (20840, 9433) waits for the street pass; so does New Festac Bridge Road,
     where rd-c56ec7e1 and rd-35ed3005 end loose at (11785.32, 8080.44). Helper:
     Gidi metres to lat, lon from the frame corner in scripts/draft_buildings.py (FU 500525, FV 707825, 1:3, y south).
     Then the rest read one by one (real bends at 1:3 left for the drive, draft kinks eased).
   - [ ] **District borders, the 22 Oct way** (DECISIONS, owner 29 Oct): read where the 51 came from; council
     boundaries as a reference (downloaded 30 Oct, owner's OK: HDX OCHA nga_admin_boundaries.geojson.zip, Office of
     the Surveyor General, CC BY-IGO, in ~/gidi-data/research/data/admin-boundaries-nga/; Lagos is its 20 councils
     at level 2, no wards); after roads, rail and water, cut the map on its hard edges,
     read each piece's character, split or join; each border shown to the owner.
   - [ ] The 15 interchanges' open parts (each junction's done part and its numbers: DONE.md snapshot, item 000):
     - Ojota: how far the slips leave the land on Street View (rd-7b01bdb8: in the map its start is 9-11 m over the
       land, higher than the 7.5 m deck; 30 Oct, Street View Jun 2021 at 6.59514 N 3.38186 E and 6.59394 N 3.38236 E
       shows the roads round the north loop near the ground, a bank by the crossing, no height read; the Overture loop
       for it not found by id); Ikorodu Road's own 4 slips 500-570 real m out; the twins catalogue's two old flat-join
       rows.
     - Jibowu / Murtala: Western Avenue's bridge 150 m south; Western Avenue's
       service roads and slips; d13 rd-955a0307 drawn twice with the city layer's.
     - Maryland: link bridge rd-c0fe3e17's clearance over the canal once water is drawn (its deck comes down to
       1.5-3 m over the land's dip at s 340-370, 30 Oct); whether Street
       View shows the south pair's openings (30 Oct: Jun 2021 at 6.57435 N 3.36906 E, not seen either way).
     - Oshodi: westbound link to the frontage road (Overture c530e1) does not fit at 1:3 (needs rd-9266faaf carried
       west past ramp rd-6a2d3255, or left out; decide with the Airport ramps' levels).
     - Airport Road junction: ramps' bridges and the expressway's levels (flat now); west service road rd-8d6f0550's
       levels with the ramps'; the real loop north (Overture 5e5af0, b58652, fb1327, 350fd6) with the ramps' levels;
       rd-70ccddf6's 6% step at (12749.4, 4907.0) looked at again in the drive; which curving ramp is rd-39b7e0c0
       and which rd-0f54d744 (7.8 and 8.8 m on satellite, 8.7 kept).
     - Oworonshoki: Diya Street slip rd-e923727a's lanes (width read rough, 12 m; Street View Mar 2024 at 6.54686 N
       3.39660 E, 30 Oct: no lane paint, about two lanes by eye between parapets, people walking on its kerbs; lane
       count not set); Diya Street's level-3 bridge (d27's pass); the links' far ends 14-29 m off the real spots.
     - Third Mainland's Lagos Island end: which road is on top (Street View); Ring Road raised (level 1); slips to
       Adeniji Adele (Overture has none, read at z18); the Lagoon Highway's heights.
     - Lagos Island cloverleaf: rd-252c0e0f / rd-ee4feee6 joined or ended with Lagos Island's streets; loops b44bf9
       and 2b32e6 meeting Third Axial under Ring Road read at z18; Ring Road's curve west against the lagoon edge;
       Idumagbo Avenue rd-4aeee6d8 joined (Google labels it Adeniji Adele Bridge); the four outer
       slips' width (8.7 m; satellite 9-12 m, no clear edge, 30 Oct).
     - Osborne (Osborne Road rd-a39f888e): link rd-289fa504's two decks' lanes (width read rough, 28 m; no lane paint
       on either deck, each about two to three lanes wide by eye, Street View Jul 2021 at 6.46216 N 3.41914 E, 30 Oct;
       lane count not set); loop rd-82b977fa overlaps the Lagoon Highway rd-fb8f7300 by up to 5.8 m at 8.7 m (0.9 m
       more at 10.5 m, 30 Oct), settled with the highway's heights.
     - Ijora on Apapa Road: east frontage road (Overture 6dfa61, 63aefb) from slip rd-9ffc6c80's loose end to
       the east link rd-9b4f42f6 waits for the Eko Bridge rd-62a2320f's
       levels; Mobil Road rd-85e1874d and Wharf Road on (street pass); which carriageway is on top (Street View) and
       whether Apapa Road stays raised to the Eko Bridge; widths of the loops rd-afd75ba3 and rd-399391e3 (not told
       apart on satellite) and the links south (rd-294c09f7, rd-714694a5, rd-e79bf93a, rd-a726bd01, rd-5b076100,
       rd-f2e0ead0).
     - Ijora on the Badagry Expressway: frontage roads the slips end on (Overture 6dfa61, 745b12, a9cbc5, 83aefb,
       ea9474); Eric Moore Road's bridge and links (54c741, c417d8, 3a5200, 7396da), rd-1533d520 redrawn with them;
       the merge onto the link north and the turn-back loop read at z18; widths (30 Oct, satellite at 6.4764 N
       3.3642 E: the bands where slips rd-001dc84f, rd-9ffc6c80, rd-cc5af0f9 run read 11-15 m but were not told
       apart from Apapa Road's carriageways beside them; Street View first).
     - Tin Can: Tincan Island Port Road drawn in its district and loops rd-2b1023ff, rd-4615c8ad joined; the bridge's
       real run over the creek (Street View); the outer loop rd-4615c8ad's width on its east side (8.7 kept: 7.3-8.0 m
       on the west, unclear in the east).
     - Mile 2: the deck's clearance read on Street View under the bridge (30 Oct, rough: Street View Apr 2024 at
       6.46008 N 3.31474 E looking east along the Badagry Expressway, a bridge with lorries on it some 50-150 m ahead,
       danfos under it give about 5.5-7 m clear by eye, so about 7-8.5 m to its deck top with the deck's depth; the
       map has the Apapa-Oworonshoki deck 7.1-7.6 m over the land; not changed. Not sure it is the same bridge: the
       pano at 6.46004 N 3.31581 E stands on a raised road east of it; read again from closer).
     - Kirikiri: bridge road rd-be737149's west end joined to its district's streets, and its second bridge with the
       water; its east end runs 110 m on d09's rd-44cd2dee (d09 line); Kirikiri Road joined to the expressway at
       (11597.34, 8907.57) in d09's pass, read on Google first.
     - Kirikiri to Tin Can: the S-bend's 96 m bends looked at again in the drive.
     - Iyana-Ipaja: Ipaja Road north of the roundabout is the district's; the BRT lane's own bridge (Overture 3602e7);
       Google z18 and Street View; the link rd-67b33568's width (lost in the bus park on satellite; 8.7 kept).
     - Anthony: the loop off the westbound bridge (Overture 7f326d) left out; Ikorodu Road's six slips here; Anthony
       Village Road on (762511) and the loose ends of Apapa Road and rd-0fbc2dcc joined; the side streets' 6 m
       corners read at z18.
     - Third Mainland's fork at Ebute-Metta: rd-b0b218e4's loose end (Overture 94da8b); which link is on top (Street
       View) and the bridge's height over the swamp; with Clinic Road eastbound rd-a8efbae0 at 14.0 m, rd-750432c4
       and rd-e38c8fd1 end 5.8 m off its node, inside it (a staggered join for the junction kit).
     - Ring Road over Awolowo Road: Ring Road raised level 2 (Street View); Awolowo Road rd-747e0c42's east end;
       whether it really meets the Marina junction's road.
     - Eko Bridge's Lagos Island end: Apogbon Bridge south (Overture f1f330, d17eac), the Inner Ring Road and Adeniji
       Adele Road on; the bridge's height on to Apogbon and the loops' heights (Street View).
     - Abule Ado loop bridge (8900, 8530): the service roads the ramps and links land on; streets at the ramps' loose
       ends; Street View; widths: ramps rd-2ab78c89, rd-166a257a read on hazy satellite (8.8-10.8 and 7.3-9.3 m, 8.7
       kept, 30 Oct), Street View to settle; links rd-3622e3bd, rd-f3179f2f (11.0 m) not readable (satellite hazy
       there; the nearest Street View, Nov 2016 at 6.45576 N 3.24559 E, is under the bridge, not on it).
     - Airport Road rd-37c2a1ad: its real lift (level 1) over Airport Road's crossing near (11665, 4485).
   - [ ] The Apapa-Oworonshoki Expressway's service roads, open parts: Oshodi's westbound link (above); the loose
     start of Anthony's west link rd-0fbc2dcc joined to the streets west of Ikorodu Road; Tincan Island Port Road in
     the street pass; widths.
   - [ ] The Fourth Mainland's ends when its design is read (no published layout found, 29 Oct; kept as being built).
   - [ ] Loose ends: 37 left after 6 gaps closed (29 Oct); the junctions' own are in their lines above.
   - [ ] Badagry's and Lekki's carriageways left as two lines (rd-52faba3e's are up to 100.5 m apart).
   - [ ] Each road's width read, longest first; the junction place names read.
   - [ ] Twins catalogue: jn-30917770 (Clinic Road at Herbert Macaulay Way) open, read when the fork's streets are drawn.
   - [ ] Third Mainland Bridge rd-e7a23019: heights z (no published deck height; GLO-30 a weak reading); then Ìbùdó
     Mẹ́ta's lane rd-0877e4b9 put back under the deck (record in map/d16/plan.json's git history); the Ṣọmọlá lanes
     ending on the bridge at grade (rd-80254433, rd-efb526e0) read on Google.
   - [ ] Ikorodu Road: heights z and the flyovers (Fadeyi, Jibowu, Ojota, Maryland); BRT lanes as records; bus bays;
     the strips at Ojota north (71.4 m); Mùṣá's Jibowu flyover rd-avaupyki still in d15; the service roads' ends read
     on Google; the roof lost under it given back in Mùṣá, Ṣọmọlá, Gbàgede (Mùṣá 43.06% vs Google's 43.26%).
   - [ ] The land (DECISIONS "The land's own height too"): water beds (4.6% of points, held at 0); Unreal reads it as
     one Landscape; a check for the slope under houses and roads; the board shows the land.
   - [ ] The 11 drawn districts' roads measured against the city layer, the layer winning; a check row that a
     district's roads sit on it where they meet.
   (c) [ ] Rail into d00 after the roads, on the real lines, ignoring what the districts drew (owner, 29 Oct); #453
   (d15's rail) closed as replaced by it.
   (d) [ ] Water into d00 (the `water` record exists, MAP-FORMAT section 2); Unreal's map_build reading d00 and a kit
   part for water.
   (e) [ ] gidi-game builds d00 alone on the land with a car to drive: first a road kit of shared instanced pieces,
   researched from studios and Epic first; the kit read from many Street View photos of Lagos roads (study only), with
   a done list of what matters on a road ticked on the map (owner, 29 Oct: "Please don't forget"): [ ] the list itself
   from the photos first (lanes and markings, kerbs and gutters, open drains and slabs, medians and barriers, bus stops
   and BRT lanes, junction lights, signs, street lights, footbridges, the ground under flyovers, wear and potholes,
   roadside sellers' spots); the vehicles at real size (car, danfo, keke, okada).
   (f) [ ] The owner drives it.
   Owed: [ ] the board shows the CLASH list; [ ] the research on how studios build a city from a real place
   (~/gidi-data/research/OPEN-WORLD-CITY-METHOD.md) read and checked, and this order changed if it shows a better way;
   [ ] a search script (in scripts/, not written yet): one search over git history, DONE.md and NOW.md that also tries each road's names from
   the map records and a short list of synonyms (owner, 29 Oct: "what if... grep fails?"); a meaning search only if
   that is not enough (a model download, asked first).

04. [ ] **Art style** (paused for the roads; all of it in `docs/look/LOOK-NOTES.md`, scripts in
   ~/gidi-data/research/look-test-29oct/, committed in gidi-data 29 Oct). When it resumes: [ ] start from what stands
   out to the owner in looks 1 (Grainy film) and 2 (Painted Lagos); [ ] the painter's "down" on curved parts (the
   keke's tub); bright paints kept under clipping (the owner's call by eye); the next objects (a wall, the red
   generator, a drum); the painter as a gidi-game tool once two or three pass; [ ] models more detailed, in the dress
   pass; [ ] the chosen look into DECISIONS, rebuilt in Unreal and measured there (8 GB or 16 GB machine: ask).

03. [ ] **Map and brush first; Unreal on hold** (owner, 26 Oct; they may take it back). The Unreal items (02(a1)-(a3)
   and (c), 0, 2-8) are kept here, not worked, until the owner says.

02. [ ] **Working first** (owner, 26 Oct). (a1) [ ] furniture placed in the street test; (a2) [ ] rail and station
   builders, simple; (a3) [ ] the container shop. (b2) [ ] suv and pickup (pickup_build exports no _static.glb; brt_build
   none), replacing the last stand-ins; then stalls with goods and printed umbrellas; (c) roads as simple shapes with
   tiling textures and decals; (d) World Partition in place of our streaming, then the shadow and Nanite pool sizes and
   the volumetric clouds decided on that city. Saloon owed (b1a): a close look in Unreal and photo passes (ot162 etc.):
   tail lamps on red, blobby mirrors, the C-pillar notch, the Corolla and Accord FLOAT cuts, the windscreen fins.

0. [ ] **Pieces as instances** (owner, 25 Oct): (b) each builder split into shared pieces in turn (stalls, poles,
   vehicles and the saloon done: DONE.md); then the rest.

2. [ ] Junctions in the kit: research how road tools build them; the T and crossroads against photos. Left from 25 Oct:
   the motorway merge at 13294,6305 (a 115k-face patch over a house); the one invalid patch (12547.9, 6070.6); the box
   with houses (block_build fails on an L-shaped pitched roof: item 5); the -0.048 m point.
3. [ ] Trees, masts, heaps and weeds: builders tested against photos; Meshy for hard shapes before credits expire 11 Nov.
4. [ ] Ground: road and verge colours (grey dusty tar), sand and earth as the map paints them.
5. [ ] Houses read their records' storeys and kind.
6. [ ] Mùṣá in Unreal: the overhead against Google Earth's Mushin, street views against Street View.
7. [ ] Lighter Gidi people (one skinned mesh, no grooms), through Mass with detail by distance.
8. [ ] Owed checks: a script that every "next" written in a commit since 25 Oct is cited on this page, run at stop;
   the per-level budget check; the other 35 GAP rows in CHECKS.md.

16. [ ] **Working means it matches the real place** (owner, 27 Oct). Comes before item 11's next district. Cover
   measured 27 Oct (DONE.md snapshot): Mùṣá 43.22% fails the band 43.26-47.65% by 0.04 points; the others at a third
   to a half of Google's.
   (b) [ ] `scripts/draft_buildings.py` drafts from Google Open Buildings v3, Microsoft only where Google has none.
   (c) [ ] What "done" means: docs/research/MAP-DONE-LAYERS.md (76 layers + 15 line-sweep candidates). Next: the owner
   goes through the layers and the 15; line sweep round two by a fresh helper; unchecked claims checked before their
   rows go into working_bar.py; each new record kind gets a test spot in Unreal.
   (d) [ ] The 11 drawn districts brought to the DENSITY row by hand, one agent per district reading Chrome, Claude
   checking and editing.
   (f) [ ] Streets by the ratio (DECISIONS, owner 27 Oct): each district's real street km per km² read from Google
   Maps; a street-density row in working_bar.py; the drawn districts thinned by hand, defining streets first; trial on
   Mùṣá.
   (g) Scout notes d10, d11, d29, d30 checked; owed before each is drawn: its Google look and the web claims listed.
   (h) [ ] Owed from the building studies: Deeper Life hall in Gbàgede redrawn smaller (real 4,703 m², ours 442);
   Ebute Ilaje's shacks; Okunade Estate's detached houses; Ìtìrí's D14-41 and Gbàgede's D28-126 split in the street
   pass; Mùṣá's hand pass (LUTH at 44% vs 22%, factories half empty, houses too big); the four new house kinds and a
   kit for each; Makoro with its stilt town.
   (k) [ ] The square survey: (1) the owner settles the ten pilot squares (docs/lagos-study/squares/d15-pilot.md) and
   the seven questions; (2) the blind read scored; (3) the rail drawn on to the outline; (4) rail and per-square rows
   in working_bar.py; (5) if the miss rate is low, all 250 Mùṣá squares in blind pairs.
   (l) [ ] Study first, then lines, district by district: Mùṣá first (squares against the 29 line layers, lines by
   hand, dress, a check row), then the other ten, then the undrawn.
   (i) [ ] The Google look for d13, d14, d16, d17, d18, d19, d27, d28 (d09, d12, d15 done); d15's by-eye readings
   re-looked in Chrome before Mùṣá's hand pass uses them.
   (j) [ ] Away mode in gidi-game: branch hooks/away-mode (c4a1164) merged; the hook seen answering a real prompt.
   (e) [ ] Then the topic passes, one agent per topic, Mùṣá first.

11. [ ] The other 40 districts to "working", breadth-first, after the network (11 drawn: d09, d12-d19, d27, d28;
   their state in DONE.md snapshot, item 11). Ìbùdó Mẹ́ta (d16) owes the railway compound, the Federal Medical Centre
   and the Red Line station with the railway; it is under the density bar (11.4% vs 26.4-30.5%).

12. [ ] **Gidi City, the shared space** (owner, 27 Oct). (b) [ ] online from the start: research a shared world in UE5
   before Unreal resumes; (c) [ ] controls of the big open-world games, and R2 on foot; (d) four ideas owed from the
   studio packs: [ ] a NOT ASSESSED answer for the checks, [ ] FOUND/ABSENT in the agents' briefs, [ ] a hook that
   blocks district-scout stopping without its note, [ ] passing-state notes carry what would end them; (f) [ ] a
   one-page "Gidi City at the end".

13. [ ] **What are we not thinking about?** (owner, 27 Oct). GTA-STUDY.md's 15 gaps for the owner to pick from.
   (a) [ ] the locked archives (CodeWalker's key search and archive reader ported to Python); (c) [ ] the owner's PSP
   games for how a story is built (~/gidi-data/research/psp/discs/); (d) [ ] how clean, real-looking games get their
   look, and road grime from GTA's own shader, decal and timecycle files; (e) missions: IDEAS "Missions: the goal
   fixed, the way open".

14. [ ] **A faster board test, run alongside the old one** (owner, 27 Oct). (a) [ ] a self-test of planted problems;
   (b) [ ] trial: both tests on every district, lists matching line for line; (c) [ ] then the fast test every time,
   the old one at each district's close and weekly.

15. [ ] **Know what's in the code base, routinely** (owner, 27 Oct): scripts/inventory.py at every session start and
   after each compaction; docs/inventory and CODEBASE.md refreshed when the repos change; as a DECISIONS rule with its
   CHECKS row, its own commit.

**District leftovers** (one line per clash, for each district's own turn; detail in DONE.md snapshot, item 000):
- d09: Kirikiri junction 109 clash + 27 node rows; Kirikiri to Tin Can 40 + 11 (14 houses under roads); Tin Can 30
  houses and streets (rd-f1478f6a still on the expressway 175 m, rd-86aea104 on a loop); Mile 2: 18 houses, 19 streets
  (houses b-2fe7abd3, b-9e425fbe, b-33e30e85; streets rd-b2b8a5cc, rd-fb81677f, rd-a9d4115f,
  rd-7fd9e952 and more); Tin Can's streets also rd-6a1edf61, rd-6bb4f684, rd-84ca7bdd, rd-b45f16c6, rd-d9222226,
  rd-d9912b10, rd-cd2781a4, rd-d2139b18, rd-d9c43b32, rd-e5cca523, rd-f5a1740e, rd-fe5e0e67; rd-6727064e crosses the new expressway piece without a shared point; with loop rd-2b1023ff at
  10.5 m: 9 houses' clashes larger, and street ends rd-2c0c9f67, rd-6a1edf61, rd-84ca7bdd, rd-86aea104, rd-d9912b10,
  rd-ea4776e0 now NODE rows inside it.
- d12: rows from Isolo Road and the Airport Road junction; Ijora: rd-0009669d, rd-6741a469, rd-e4dd8803, b-03eb90ec
  beside the west road; frontage road rd-beb7773a: rd-fe80ec1c, rd-31de79b1, rd-5d55c27c; Badagry Ijora: streets
  rd-63ff2dcb, rd-b645f07f, rd-da8895b1 re-joined; rd-9df13b08, rd-e71a0ffa, rd-f150b7c4 on the expressway.
- d13: rd-c92310d9, rd-02b98288 round Murtala's bridge; rd-41075d23 re-joined on the ground; rd-955a0307.
- d14: rows from Isolo Road.
- d15: Isolo Road deck rd-isodeck1 is the wrong way round (the expressway goes over); rd-qc8rcv8v crossed twice at the
  knot and 3 rows at the Airport Road junction; rd-qqm8wpxb lies on the east service road 533 m (9 clash, 5 node rows);
  rd-avaupyki re-joined on the ground; at Agege Motor Road rd-798553cb by Isolo Road, rd-cb2h4xa5 and rd-0gi2ewca end 2.0
  and 4.4 m off its node and rd-cb2h4xa5, rd-xafls8id, rd-hvwdw3gi cross it with no node (3 clash, 2 node rows; pass 12).
- d16: rd-d6e90d7a, rd-3ee9757d, b-c3e45656 by the Eko Bridge's tie; houses and streets under the Ebute-Metta links.
- d17: rd-9e64ec60 (Murtala drawn again, under the deck), rd-5acd2735, rd-96ed58e3, rd-0c855838, rd-7ec58da0,
  rd-b2d9b4b0; rd-188b1a2a re-joined; Clinic Road's end 1 m from rd-96ed58e3 / rd-93fdb33d; houses b-120302f2,
  b-2ce5fff2, b-a8591e2f and streets rd-65ae9b6c, rd-768e6e2a by the Clinic Road links; Jibowu's east service road at
  11 m (30 Oct): rd-1a3d2748, rd-32d111e0 end inside it with no junction, rd-d76aa192's end 4.7 m from its node;
  Clinic Road eastbound rd-a8efbae0 at 14.0 m (30 Oct): b-120302f2, b-2ce5fff2, b-a8591e2f further under it,
  rd-41e54459's end a NODE row 6.2 m from its node.
- d19: rd-d6d07182 under rd-aae94fd5 for 12 m, crossed by both links; b-20052ac2, b-74a64b3f, b-494e9843; rd-a27ac3a6,
  rd-00c23990, rd-a15fbfdf; with the fork's links at 10.0 m: 23 house clashes larger, b-4655f02f and b-fa201702
  new, street ends rd-325023fc, rd-7a9d8b06, rd-a0b710b5 now NODE rows inside rd-7382f27e; with Clinic Road eastbound
  rd-a8efbae0 at 14.0 m: b-012287e1, b-20052ac2, b-494e9843, b-d879cf99 further under it, b-d9224f21 new, rd-00c23990's
  end inside it with no node, rd-a27ac3a6's end a NODE row 6.2 m from its node.
- d27: b-560314a0 under an Oworonshoki link; rd-20954906, rd-80254433 crossing it; 14 rows from Anthony's service roads; its ramp
  rd-a557b7a2 still holds rd-e923727a's old start points (eased in pass 16) and runs on it 61 m (1 clash row);
  Oworonshoki's links at 10.5 m (30 Oct): houses b-2798e61a, b-6baf47f5 newly under rd-7a24933e, rd-8e84bcfc ends
  inside it, 13 street ends 4.4-5.7 m from the links' nodes (NODE rows: rd-02e38b95, rd-04d48b48, rd-20954906,
  rd-241002da, rd-395d5c12, rd-3c4bd7ed, rd-570636d8, rd-95ef5c6d, rd-ae0fbe3b, rd-c7428a3d, rd-d9fdf047 twice).
- d28: rd-db0655fe ends loose inside Ikorodu Road; Ojota's 24 street rows under ramps; Anthony: 31 houses,
  rd-cbaebc6a (the expressway again, 193 m), rd-90772fe4, rd-79282a08, rd-ae7949a3, rd-30407730; 43 rows from the
  service roads; rd-eb7f5d73's end 5.6 m from rd-e28cb5e7's node (Oworonshoki's links at 10.5 m, 30 Oct).
- d30 (Isolo-Ladipo, when drawn): Isolo Road stays on the ground under the expressway, as d00 has it.
- d11 (Ijora-Iganmu-Costain, when drawn): Western Avenue on south from d13's rd-32d33ffa end (13241.36, 7384.58);
  the 5 Apapa Road pieces on Agunda's east border; the Lagos-Badagry Expressway carried across Agunda's corner from
  d09's rd-b2b8a5cc end (12568.69, 7733.91).
- d06, d08, d10 (when drawn): Ayégúnlẹ̀'s expressway records rd-b2b8a5cc, rd-f1478f6a on their border taken as held.

**Owed: written down as "next" and not yet done** (each goes into an item above, or stays here until it does; rule in
CLAUDE.md: every new "next" lands here or in the order, same change):
- Meshy's credits run out on 11 Nov: spend them on hard shapes code can't get right, cost stated first.
- Saba (d17) and Makoro (d19) audit of 27 Oct, to fix in 16(d): Makoro's east half (59 houses vs Google's ~5,900);
  12 four-storey walkups on the lagoon edge to 1-2; d17's 64 near-miss road ends, 30 broken streets, 122 dead stops
  (d19: 2, 2, 37); seams with d16, d18, d19, d27; Akoka Road's doubling-backs; pc-044db919, pc-472dd1cc off the road;
  rd-a4ed4412 a 27.2 m stub; pl-sab44155 linked to pc-c01928e5, pl-sabc962e to pc-0de85f48,
  pl-sabb6735, pl-sab35696; three houses on water in d17's north-east; every road tar_worn
  with no median. The auditor's lists re-run, not copied.
- The look pass (after every district is working): schools' and factory's faces, the factory wall's advert; B28's
  name; laterite and concrete roads, an interlock layer; sound-alike place names and hours; the 787 houses' storeys,
  kind, ground floor, roof from the shots; LIVING.md sheets against Street View; buildings for Mùṣá's six, Ìtìrí's 65
  and Sọ̀rọ̀lérè's 53 place squares; Ìtìrí's and Sọ̀rọ̀lérè's houses filled up and their 5+ readings checked; Mùṣá's
  mix and person spots; the brush layer; the hero streets.
- Tall readings to look at on Street View in the look pass: d12 b-0e26f361, b-6493aef7, b-e9e29b9e; d27 b-5097e7c0,
  b-7c249835; d28 b-e058528f, b-ae17f158; d19 8 (b-0dcdd67b among them); d18 b-8bd534f5; d17 b-e9b783b2; d16 b-c0559b50;
  d14 b-7aa9e512.
- Bus stops and motor parks read on the map (study only), as Ìtìrí's park: d09 (Boundary, Mosafejo, the expressway),
  d13 (Ojuelegba, the stadium, Masha, Adeniran Ogunsanya), d12, d28, d27, d17 (Yaba, Sabo, Jibowu's coach parks),
  d19 (canoe landings), d18 (campus shuttle, the gate's park).
- Mushin station's footbridge from the hall b-mshstn01 over the tracks (a path with z, 6 m over the rail; a rail clearance check with it).
- Road kit (Unreal on hold): road points' z, decks, parapets, piers; the board server reloading check_map.py on change.
- Real names in d13, d14, d15 record notes: strip to ids and sound-alikes, or reword STREETS.md; its own commit.
- `scripts/map_picture.py`'s near view places far names: keep them inside the frame (a tool fix).
- The map picture's GAP row: working_bar could run map_picture's gap count.
- A hospital house type (Randle's blocks); landmark grounds' own buildings to the look pass.
- Ayégúnlẹ̀'s middle band (x 11,500-12,450, y 8,440-8,570) is a narrow canal with packed houses, not wetland: drawn so.
- Agunda's rd-cd2a7637 and Ṣọmọlá's rd-f58919a3 run half over the land beside them: the district there takes them as
  held. Widths to read: Alhaji Masha Road 13.5 m; the 25 m and 40 m expressway and Ikorodu Road records; Murtala
  rd-9e64ec60's 10.75 m and median.
- Trunk roads come in as lanes in the roads draft: each district checks its trunk roads by hand (as Saba's three).
- `working_bar.place_kind` misses denominational churches (pentecostal 181 and others): fix the check, then add the
  missed churches by hand in d15, d14, d13, d09, d12, d27.
- University Road rd-cbdf1d43's last 18 m (ending on Saba's rd-beee86ae) over Saba's rd-0dd14298: the seam's hand pass decides.
- Third Mainland Bridge over Makoro's corner and on over the lagoon (with item 000).
- Ìbùdó Mẹ́ta's bridges and ramps as decks (Eko Bridge, the Third Mainland ramps, Clinic Road, Carter Bridge, the Ijora
  Causeway, the Oyingbo Flyover): with item 000.
- Lagoon University's campus wall: 5 gates of 38-157 m to close in the look pass.
- Ìbùdó Mẹ́ta's cleared sawmill ground (owner, 27 Oct): old timber, sawdust, a broken shed, a hoarding, a street-football
  pitch and a canoe landing; with d16's landmarks.
- Into item 0: one material for the plank stalls' shades; per-instance window colour; HLOD and World Partition measured.
- Plates: the new map's districts each want a row and a sound-alike code, then `tools/plates.py` again.
- Vehicles: fold M_GidiPaint_Instanced into M_GidiPaint; the near danfo's broken shadow sliver; the underdeck level
  rebuilt; the twelve old `lorry_ot45_*` models checked.
- Not understood yet, measure again: work mode slower than high on Underdeck; the over-the-roofs GPU median; Nanite's
  fallback triangle count (95b0053).
- Road kit never imported into Unreal (6a26dd1, dc5e664); its look still off against the photos (drain width, walls,
  bottles, cables, kerb block, grates; not tried on a curve); relief and chipped tops to become records.
- Plants kit for the ditch banks (55c14e7): item 3.
- The frame study, only if the frame changes: its grids' scripts to write again from docs/lagos-study/STUDY.md
  (copy in ~/gidi-data/frame-backup-25oct/).
- MAP-FORMAT "Next steps": `gidi-map/1.0`; a real-names list; the twin catalogue with ids; the board's outline editor,
  day filter, loading only districts in view.
- Builders from the 24 Oct tests: zinc roof gaps (ROOF-GAPS.md), wall wear, gutters, wear baked into images, frontage
  and ground builders (`tools/kit_fields.py`), outfits, the basin test, the lorry into `gidi_heroes.py`.
- Emmanuel St (ut01), after the owner's verdicts: the listed fixes, then angles B and C.
Alongside, whenever a build waits: study passes over the saved Street View shots for new kits and activities.

**State.** The new map: real Lagos at 1:3, 27 x 10.5 km, 51 districts, format in `docs/MAP-FORMAT.md`; d00 the city
layer (main roads, land); 11 districts drawn. The kit is gidi-game's builders, read by `tools/map_build.py`. Board:
`cd ~/gidi && ~/.venvs/gidi/bin/python scripts/board_server.py --port 8779`, then `http://127.0.0.1:8779/web/board.html`.
Map check: `~/.venvs/gidi/bin/python scripts/check_map.py`. Unreal (on hold): gidi-game `tools/editor.sh` with
`tools/watchdog.sh`. VoiceMode's whisper and kokoro are disabled (`launchctl enable gui/501/com.voicemode.<name>`).
gidi-data's notes and scripts are on GitHub, private (NewDara-Star/gidi-data, 30 Oct; push after each commit); its
data, pictures and .blend files, and the other-game studies (research/gta, research/psp, ignored), are on this Mac
only: Time Machine failed to mount its disk on 29 Oct.

**Waiting on the owner.**
1. People: the proof run (N one-mesh people against N City Sample people in the Underdeck) when the Mac is free.
2. The lived-in records (`decisions/lived-in.md`): a yes on `mix`, `route`, `state`, `moment`, `job` and the 18 new
   `person_activity` values.
3. Names (`docs/lagos-study/roads/NAMES.md`): Lagoon or Gidi; Ìkòrodò / Okotun; Mile 2/12; Mùṣá; tone marks; Obalende.
4. Kit eye tests: ut01_emmanuel angle A v2, layers 1-7 (the pickup reads weird).
5. Download OK? a CC0 grass texture (Poly Haven, ~10-20 MB) for verges.
6. Restart the Mac when home; then re-measure work mode's shadow pass.
7. The look: 8 GB or 16 GB as the target machine; exposure or deeper paint for bright colours.

**Parked** (decided or asked for, not being worked on now).
- The built danfo's wear material in the game; the keke, korope, molue and BRT the same way.
- Gidi Brush as a font; coat of arms; the brand sheet; the main menu and the UI (the owner is collecting references).
- The Reach in the Festac-inspired district (5), when it is drawn.
- Bus stops and junctions named the Lagos way, for the conductors' calls.
- Unreal look fixes from 18 Oct: check whether they still show with the builders' models first.
- Consoles: PlayStation Partners when there is a playable piece. Tunde's story, layered on the world.
- A living test for the new map, once a few districts join (IDEAS).
- The Underdeck's play systems (levy run, heat, money, rep, HUD) and people with cloth.
