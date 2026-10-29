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
   and Lekki Regional as being built), every junction a shared point and named in its record for the real place it stands for and the district it lands in, so a district's streets know where they meet the network when it is remade (owner, 28 Oct: "we need to be able to match them to the actual spot in the districts, so we can add them slip roads and streets"); slip roads and ramps drawn with their main road at real length (DECISIONS "1:3 sets where things are"); (b1) [ ] the main roads drafted into d00 (`scripts/draft_network.py`, 28 Oct: 137 roads, 184 Gidi km; neatnet merge, 1:3, widths a default by kind "not read"; interchange leftovers taken off; check_map passes after 4 hand fixes, listed in the commit). By hand still: [x] its ends cut back from Third Mainland and Ikorodu Road joined to them (18, flat, read with the crossings; the network is then 6 pieces, the biggest 187.4 of 201.4 km and the whole frame wide; the others: Idi-Iroko road in the north-west corner, 12.2 km, joined only outside the frame, and four bits of 0.1 to 0.9 km at Lekki, the Eko end and the east edge, to read); [x] its 21 crossings and its 17 spots joined to the hand roads read on Google satellite (28 Oct; `~/gidi-data/research/twins/crossings-read.tsv`): 18 flyovers, 8 slip roads, 3 forks at a ramp's foot, 4 flat junctions (1 not seen), 2 the same road meeting itself, 3 on the unbuilt Fourth Mainland; [ ] the 15 interchanges they belong to drawn by hand with their decks' heights and slip roads at real length, biggest first: [x] Ojota (28 Oct: the expressway's deck over Ikorodu Road, 7.5 m lift over 120 m with 4% approaches, and 18 slip roads, Overture's link lines at real size round the crossing turned 2 deg to the drawn roads, each end joined where it meets its road, the two links Overture raises lifted over Ikorodu Road on banks; heights on the 1:3 land; read against Google satellite, four loops; owed on it: [ ] the slip roads' widths read (8.7 m, the FMW manual's one-lane ramp, not read there), [ ] how far they leave the land read on Street View (up to 10.6 m, rd-7b01bdb8, beside the raised links), [ ] the 4 links of Ikorodu Road's own slips 500-570 real m out drawn at their 1:3 spots, [ ] Gbàgede's 5.9 m stub rd-cf9faf2c that still joins the old expressway line flat onto Ikorodu Road under the deck, [ ] the two junction rows of the old flat joins in the twins catalogue updated), [x] Jibowu (28 Oct: Western Avenue's flyover onto Ikorodu Road lifted 7.5 m over the land between Herbert Macaulay Street and Ikorodu Road's west service road, both passing under it (7.67 and 7.51 m clear), down at 5.5% each side on a smoothed profile, steepest 5.9%; the ground roads re-joined on the ground as Overture draws them: Agege Motor Road down the flyover's west side to Herbert Macaulay Street, Herbert Macaulay Street under it to Herbert Macaulay Way, Murtala Muhammed Way (rd-9e50c90a) from the service roads' ends, the two drafts rd-0a697129 and rd-e2c3bc0e merged into it; read on Google satellite; owed on it: [x] Murtala Muhammed Way's own bridge over Herbert Macaulay Street (28 Oct, the owner's choice C, DECISIONS "the crossing moves, not the slope"): 7 m lift, 5.5% ramps (5.8% at its steepest 10 m), 6.9 m clear, the crossing 58 m further along it, Herbert Macaulay Way starting at a ground junction east of it, two ground service roads beside it (rd-2218bb4b, rd-b1b129a5); owed on it: [ ] the district streets round it re-joined in their passes (d17 rd-9e64ec60 is Murtala drawn again, now 0.2 to 6.9 m under the deck where they share points; d17 rd-5acd2735, rd-96ed58e3, rd-0c855838, rd-7ec58da0, rd-b2d9b4b0, d13 rd-c92310d9, rd-02b98288; 8 houses under the new roads), [ ] the twins row jn-a388684f moved from the old crossing (13411.65, 6330.51) to the new ground junction (13456.6, 6373.7), [ ] the service roads' width read (7 m, not read), [ ] Western Avenue's bridge 150 m south (344 m raised real) drawn, [ ] Western Avenue's two service roads and the express/service slips at both ends drawn, [ ] the three district streets joined onto the deck (d13 rd-41075d23, d17 rd-188b1a2a, d15 rd-avaupyki) re-joined on the ground in their district passes, [ ] d13's Herbert Macaulay Street rd-955a0307 drawn twice with the city layer's, [ ] the twins catalogue row jn-a1c42ea1 moved: its node (13351.5, 6301.8) is gone with the merged drafts, the ground junction is now Agege Motor Road at Herbert Macaulay Street (13282.2, 6329.2), and its place read (it says Ojuelegba)), [x] Maryland (28 Oct: Ikorodu Road's express in an underpass 7.0 m under the Mobolaji Bank-Anthony Way junction and on a flyover 7.5 m over the ground junction where the link bridge lands, both crossings carried on to the east service road as the real ones are, ramps at 5.5%, 110 m between them on its old profile (s 1095.8 to 1205.9, measured against the commit before) with one slip pair (rd-fb35cab8, rd-eb682999); the service roads now end and start at the ground junction, not on the express; owed on it: [ ] the second slip pair at the underpass's north mouth (Overture has it at 1:3 inside the ramp), [ ] the link bridge rd-c0fe3e17 raised on its own bridge (Overture: about 600 m at level 2, heights not drafted), [ ] the express's old profile 1.4 m below the land 220 m north of the flyover (s 1526 of rd-db6dfdd1), where the land climbs faster than the 3.5% it was held to on 28 Oct: a cutting or the profile redone, [ ] the slips' width read (8.7 m, not read)), [x] Oshodi (28 Oct: the Apapa-Oworonshoki Expressway on its bridge over Agege Motor Road, 7.7 m over the land smoothed over 60 m, 6.9 m clear, ramps at 5.5% (steepest 5.9%); Agege Motor Road straight under it as Overture's line, the draft's bend onto the expressway in a flat junction taken out; the link from Agege Motor Road onto the expressway, Overture's 308 m loop at real size (rd-cad04ec1); owed on it: [ ] the westbound link off to the expressway's frontage road (Overture, 176 m), that road not in d00, [ ] the twins rows jn-d5d31b03 (two, at the old flat junction 12759.3, 4904.3) moved to the crossing (12788.3, 4892.0) as a flyover, [ ] the link's width read (8.7 m, not read)), [x] Oworonshoki (28 Oct, the owner's choice: real size, the roads bend: the real trumpet as one piece, Overture's four links with Third Axial between their ends, slid along the Apapa-Oworonshoki Expressway and turned 5 deg, its Third Axial ends 3.7 m (the hub) and 8.1 m (where it rejoins) off the drawn road; the expressway ends where its links split (its last 265 m, flat into Third Axial, gone); Third Axial's first 471 m redrawn on the real line; Third Mainland (Ṣọmọlá's hand-pass points) unchanged, links 3 and 4 joining it at its own point (14536.32, 5362.28); links rd-416f06ca (over link 4 and Third Axial, 7.2 and 7.5 m), rd-e28cb5e7, rd-7a24933e, rd-bc322629 (over Third Axial, 7.5 m), steepest 6.0%; the X of links over Third Axial seen on Google satellite by eye; clashes 1163 to 1249 (147 new, 61 gone: d27's streets and houses under the links); owed on it: [ ] link rd-bc322629's 69 deg corner 4 m from Third Mainland (a ROAD row) hand-edited, [ ] Diya Street's slip onto Third Mainland (Overture, 269 m, level 1) at real size: today the draft's 91 m stub rd-e923727a, which d27's Diya Street rd-a557b7a2 is drawn on, [ ] Diya Street's bridge over the junction (Overture level 3) in d27's pass, [ ] the links' far ends meet their road 14-29 m from the real spots: their carriageways are one centreline, [ ] the twins row jn-5333f58c (the old flat join at the expressway's end, 14429.0, 5086.9) moved to the links' split (14172, 5126), [ ] the links' width read (8.7 m, not read)), [x] Third Mainland's Lagos Island end (28 Oct: Ring Road runs on under Third Mainland as the real one, on Overture's westbound Ring Road at 1:3, the draft's two flat joins of Ring Road onto Third Mainland and the stub rd-fd41eee8 taken out; Third Mainland lifted 7.5 m over it (7.48 m clear), ramps at 5.5% (5.9% at its steepest), on into rd-36ade1eb; the Lagoon Highway's first point at Third Mainland's height there (0.59 m, 2.2% to its next point); read on Google satellite by eye; owed on it: [ ] which of the two is on top read on Street View (Overture puts both at level 1), [ ] Ring Road raised as Overture has it (level 1), heights not read, [ ] the slip roads down to Adeniji Adele that the 28 Oct crossings reading names: Overture has none there, read at z18, [x] Ring Road's sharp turn onto rd-700a683a at (14371.8, 8275.7), a draft junction, redrawn with the cloverleaf (28 Oct, gone with rd-700a683a), [ ] the Lagoon Highway's heights (under construction, Overture level 1)), [x] the Lagos Island cloverleaf (29 Oct, redone whole at real size by the owner's rule of 29 Oct, DECISIONS "A big junction keeps its real size and shape": Overture's junction placed whole at real size with its corner where Third Axial becomes Third Mainland Bridge on Third Mainland's end; Third Axial rd-36ade1eb on the middle of its two carriageways to the junction's east corner, which lands 29 m from the next motorway knot, its last 200 m bent onto it (the draft's rd-3d130bf3 taken out; rd-79189454 stays, joining Ring Road east rd-a39f888e on to the knot); Ring Road rd-322bc528 at real size from the south node, 7.48 m over Third Axial, then turned west on a 60 m curve where it stays 35 m clear of the Lagoon Highway (the real north corner lands 13 m from it) and straight to its crossing under Third Mainland; Idumagbo Avenue rd-4aeee6d8 at real size, a loose end; the four loops (rd-4b7c8697, rd-fc4f9a75, rd-7295d681, rd-2db62fc1) and the four outer slips (rd-46b352a3, rd-ecbb93aa, rd-c93b6d4f, rd-2fb123ed) at real size, their ends bent onto their roads (up to 29 m) and cut back by hand where they would run along their road (25-80 m), meeting it at 30 deg or more; rd-252c0e0f, which ran through the junction, cut by hand: its 237 m inside gone, two pieces left (rd-252c0e0f 38 m, rd-ee4feee6 50 m, its end moved 4.2 m onto the knot); grades 6.0% at most; smoothed by hand the same night (Overture's traced points wobbled 1-2 m and made 12-17 m bends: each loop and slip fitted with a smoothing spline moving it 2.6 m at most; the slip rd-2fb123ed's start, a hook off Ring Road, redrawn as a smooth curve leaving it 30 m further back; tightest bends now 25 m (rd-4b7c8697 at its join under the deck) and 34-193 m elsewhere); owed on it: [ ] Ring Road's own sharp bends west of Third Mainland, from the draft (10-11 m at (14054, 8246) and (13914, 8330)), hand-edited for cars in its pass, [ ] rd-252c0e0f's two pieces joined or ended when Lagos Island's streets are drawn, [ ] the loops b44bf9 and 2b32e6 join Third Axial at one point under Ring Road's deck (7.38 m clear): read where they really merge (Google satellite z18), [ ] Ring Road's curve west read against the land and lagoon edge (Google satellite), [ ] Idumagbo Avenue joined when Lagos Island's streets are drawn (Google labels the stretch Adeniji Adele Bridge, not resolved), [ ] the twins rows jn-014e4097, jn-64296779, jn-d7e4ecb5 (draft crossings) moved to the crossing (14576, 8503) and the loops' joins, [ ] the loops', slips' and Ring Road's widths read (8.7 m and 11 m, not read)), [x] Osborne (29 Oct, whole at real size by the same rule: Overture's junction placed at real size on the crossing of Osborne Road rd-a39f888e and the link rd-289fa504, not turned; Osborne Road on its real line from 150 m before its first slip, its west end bent onto the drawn road over 150 m, past the last slip a 308 m curve back to its drawn end (15783.2, 8408.6), the draft's two short corners there gone; the link from the Lagoon Highway at real size, smoothed, its first 287 m past the highway cut and its end bent onto the highway's joint (15193.0, 8194.9) over 120 m, crossing Osborne Road on the ground; Overture's four turn-lane bits folded into that one ground junction; the two loops (rd-149d3209, rd-82b977fa) on bridges 7.47 and 7.48 m over Osborne Road, the two turn-offs (rd-27f1d1e5, rd-a3e9864c) on the land, each landing on the link at its own spot at 30 deg or more, eased on a curve where it would have joined in a hook; tightest bends: Osborne 83 m, link 250 m, loops 43 and 39 m, turn-offs 22 and 28 m; steepest 6.4% (rd-149d3209 on a 5.1 m step) and 6.2% (rd-82b977fa on 1.9-3.2 m steps), the rest 5.9% or less; owed on it: [ ] the loops' 6.2-6.4% short steps smoothed to 6.0%, [ ] rd-27f1d1e5's 22 m bend where it lands on the link (15365, 8470) eased, [ ] Federal Secretariat Road on from the link's loose south end (15365.4, 8478.9), [ ] the link's width read (24 m drafted; Google shows a two-way road), [ ] the north loop's clearance to the Lagoon Highway read, [ ] the twins row jn-185ebef9 checked against the crossing (15250.6, 8312.0), [ ] the loops' and turn-offs' widths read (8.7 m, not read)), [x] Ijora on Apapa Road (29 Oct, whole at real size by the same rule: Overture's junction (13 parts) placed at real size, slid (36, -22) m onto the drawn Apapa Road where it fits best (the real line then within 12 m of the drawn one), not turned; Apapa Road rd-c74ce92c on the middle of its two carriageways, bent onto the drawn knots at the Eko Bridge junction (13246.52, 8126.36) and the turn towards Apapa (13392.28, 8808.66) over 100 m, the drafts rd-87f48130 and rd-2fa249fb (its old line here) taken out, the draft's jog into the Eko Bridge knot redrawn as one curve; raised 7.5 m over the four roads that pass under it and straight between them (398 m), ramps 5.5%, its south ramp running on into rd-2856c48f, held to 5.8% where the land is steeper (z on all its points); Marine Bridge Road rd-7e924dc3, the west road rd-8bbc873e (its street corner eased to 21 m), the links rd-9b4f42f6 and rd-714694a5 on the ground; the big loop rd-399391e3 from Mobil Road on a bridge 7.41-7.51 m over the links; slips and loops rd-f2e0ead0, rd-5b076100, rd-b158299d, rd-afd75ba3, rd-ce943f23, rd-e79bf93a, rd-294c09f7, rd-a726bd01; Mobil Road rd-85e1874d, 236 m, its west end loose; fixes by hand: at 1:3 the Eko Bridge junction and the turn towards Apapa are nearer than the real ones, so the two slips that really leave beyond the Eko knot are cut back 191 and 136 m and the last slip south cut to its first 45 m, and the frontage roads north of the junction (Overture 32a30e, f0f751) are left out; tightest bends 21 m (the west road's corner) and 31-104 m on the slips, 80 m on Apapa Road; steepest 6.0%; clashes 1249 to 1253 (5 new in d12 beside the west road and slip: rd-0009669d, rd-6741a469, rd-e4dd8803, house b-03eb90ec; 1 gone); owed on it: [ ] the frontage roads beside Apapa Road north of the junction drawn, joined at the Eko Bridge junction, [ ] Mobil Road and Wharf Road on from the loose end in the street pass, [ ] the draft's own 8 m bend on rd-2856c48f at (13407, 8834) eased, [ ] the twins rows jn-1cd55c4d, jn-e2c90023, jn-5c5d7b70, jn-994666de, jn-1ed0cd1a (draft crossings on the old line) moved to the new crossings, [ ] which carriageway is on top where Overture has levels 1-2 read on Street View, and whether Apapa Road stays raised on to the Eko Bridge (Overture: level 1 all the way), [ ] the d12 clashes beside the west road joined in d12's street pass, [ ] the widths read (8.7 m slips, 11 m side roads, 24 m Apapa Road, not read)), [x] Ijora on the Badagry Expressway (29 Oct, whole at real size by the same rule: Overture's junction placed at real size, not turned, its crossing (Apapa Road over the expressway's eastbound) on the middle of the chord between the Eko Bridge knot (13378.91, 7611.77) and the Ijora knot (13246.52, 8126.36); Apapa Road rd-c74ce92c between them on the middle of its two carriageways, the real line 53 m off each knot (the drawn line bends where the real one is straight) bent onto both over 200 m, tightest bend 133 m, raised 7.4 m over the expressway (14.4 m over the land, Overture level 2 over level 1; 7.34 and 7.00 m clear), ramps 5.5% to the knots, held to 5.8%; the expressway rd-7fdd61c3 on the middle of its carriageways from the drawn end (13077.42, 7741.35), bent onto it 8 m, up to its split 113 m on, which it reaches part way up (the carriageways go on up to 7.0 m over the land); its eastbound rd-72d3e204 and westbound rd-f9865f51 leaving the split at a small angle; the turn back under Apapa Road rd-f9973534 (34 m bend); the link north rd-9ffc6c80 from Apapa Road up past the eastbound's end and down beside Apapa Road, its start moved 22 m onto the one-line Apapa Road; the slips rd-001dc84f, rd-cc5af0f9 and the crossing link rd-8925b205; the drafts rd-84fd86c9 and rd-e74592ea taken out, rd-1533d520's first 2 points; the slips' far ends left loose (cut back 25 and 45 m to stand clear of rd-8d8116e2 and Apapa Road); steepest 6.0%; clashes 1253 to 1239 (22 gone with the drafts and Apapa Road's old line, 8 new on the expressway: d12 rd-9df13b08, rd-e71a0ffa, rd-f150b7c4); owed on it: [ ] the frontage roads beside Apapa Road the slips really end on (Overture 4c3842, 6dfa61, 745b12, a9cbc5, 83aefb, ea9474) drawn and the loose ends joined, [ ] Eric Moore Road's bridge onto the eastbound and the links under it (Overture 54c741, c417d8, 3a5200, 7396da) drawn, rd-1533d520 redrawn with them, [ ] whether Apapa Road stays raised on to Eko Bridge (Overture: level 1-2 all the way; here it comes down to the land at both knots) read on Street View, [ ] the expressway's merge onto the link north (30 m bend) and the turn back's loop read on Google satellite z18, [ ] the twins rows jn-de37f4e3, jn-f813db45, jn-7c616833, jn-dcb3113b, jn-56e61b50 (the drafts' junctions) moved to the new nodes, [ ] the d12 streets that ended on Apapa Road's old line (rd-63ff2dcb, rd-b645f07f, rd-da8895b1) and on the drafts re-joined in d12's street pass, [ ] the widths read (24 m expressway, 11 m carriageways, 8.7 m slips, not read)), [x] Tin Can (29 Oct, whole at real size by the same rule: Overture's Apapa-Oworonshoki Expressway (both carriageways on bridges) and its two loops down to Tincan Island Port Road placed at real size, slid (-66, -82) m onto the drawn expressway where it fits best (18.8 m off it, root mean square, over the real stretch), not turned; the expressway rd-c0a3f989 and rd-6300e6de on the middle of its carriageways from 30 m before the first loop to 60 m past the last, its two ends eased back onto the drawn line on long curves (97 and 189 m, handle lengths searched for the gentlest; tightest bend 95 m, the real road's own bends here 49-106 m), the knot rd-6300e6de starts at moved 17.5 m onto the new line; raised 7.5 m over the land where the loops pass under it, ramps 5.5% held to 5.8%, z on all points of both records; the loops rd-4615c8ad (817 m) and rd-2b1023ff (727 m) on the land, tightest bends 47 and 36 m, their expressway ends moved 6.8 and 7.3 m onto the one-line road, their port-road ends loose (that road is not in d00); clashes 1239 to 1297 (21 gone, 79 new: 30 d09 houses and d09 streets under the new line and loops); owed on it: [ ] Tincan Island Port Road drawn and the loops joined to it, [ ] the d09 clashes in d09's pass (30 houses; streets rd-f1478f6a, which still runs on the expressway for 175 m, rd-86aea104, 11 m on a loop, rd-6a1edf61, rd-6bb4f684, rd-84ca7bdd, rd-b45f16c6, rd-d9222226, rd-d9912b10, rd-cd2781a4, rd-d2139b18, rd-d9c43b32, rd-e5cca523, rd-f5a1740e, rd-fe5e0e67 and others), [ ] the twins rows jn-39f33d88, jn-b5a7ba6c, jn-12cbfeda, jn-aaddb3b2 moved to the new nodes, [ ] how far the bridge really runs over the creek read on Street View (here it is raised only over the loops), [ ] the widths read (not read)), [x] Iyana-Ipaja (29 Oct, whole at real size by the same rule: Overture's junction (Iyana-Ipaja New Road on its bridge over the Lagos-Abeokuta Expressway, three links on the land, Ipaja Road on the land under the bridge) placed at real size, slid (9, 48) m onto the drawn expressway where it fits best (38.2 m off it, root mean square, within 300 m of the crossing), not turned; the expressway (rd-92d815aa, rd-4d25be78) on the middle of its carriageways for 150 m each side of the crossing, eased back onto the drawn line 450 m out on curves (tightest bend 101 m, corners where they land 1.2 and 0.7 deg); the draft's jog rd-279c90d0 taken out, the knot between the two records moved to where the link from New Road joins; New Road rd-9e6fc47d on the middle of its carriageways from its end at Ipaja Road to 30 m past where its links leave, then landing on the drawn rd-a0c20bd4 403 m along it on a curve (3.6 deg corner; rd-a0c20bd4's first 403 m taken off), raised 7.5 m over the expressway and Ipaja Road (7.49 and 7.51 m), steepest 5.7%, tightest bend 55 m (its own curl at Ipaja Road); the links rd-67b33568, rd-a601faa2, rd-365def05 and Ipaja Road rd-57fbbfbf on the land, their joins redrawn as curves (tightest 54-90 m); no clash changes (d41 not drawn yet); owed on it: [ ] Ipaja Road on north of New Road's end and Ipaja Road's loose end drawn and joined, [ ] the BRT lane's own bridge along the expressway (Overture 3602e7, level 1) drawn, [ ] the service roads beside the expressway drawn, [ ] the twins row jn-c3a2eb99 moved from the old flat crossing (10909.7, 2546.8) to the bridge (10942.2, 2583.5), [ ] read on Google satellite z18 and Street View, [ ] the widths read (18 m expressway and New Road, 8.7 m links, not read)), [ ] the Fourth Mainland's ends when its design is read (29 Oct, searched: no published layout found for either end; Wikipedia (read 29 Oct) has it start at Abraham Adesanya in Ajah and cross the lagoon to Itamaga, Ikorodu, on to the Lagos-Ibadan Expressway, with 9 interchanges, 3 toll plazas, a 4.5 km lagoon bridge and a 2 x 4 lane road with room for a BRT lane, construction not started as of Nov 2023; other papers' six or eight interchanges and three lanes each way not checked; the design documents would be with the Lagos State Ministry of Works; until they are found the bridge's ends stay as the draft drew them, the owner's 'kept as being built', 28 Oct); [ ] its loose ends read (a real end or a gap; 48 on 29 Oct after the junctions, 7 at the frame edge): [x] 6 gaps the draft left where it took Overture's junction bits off closed by hand (29 Oct: five on the Lekki-Epe Expressway, 23-74 m, carried on curves, its junction with rd-b3681a9a moved 6.6 m onto the road's straight line; one on the road at the frame's east edge, 24 m), 37 left; [ ] the rest: the junctions' own loose ends are owed in their entries; read against Overture on 29 Oct (by eye on plots of its roads under ours, names from its records), six sets are junctions the draft broke and the first list of 15 missed, each to go in whole at real size by the same rule: [x] Anthony (29 Oct, whole at real size by the same rule: Overture's junction placed at real size, slid (-93, 75) m onto the drawn Ikorodu Road and expressway where they fit best (27.5 m off, root mean square), not turned; the draft's 160 m gap in the Apapa-Oworonshoki Expressway across Ikorodu Road closed with the real line, on the middle of its carriageways for 150 m each side, eased back onto the drawn rd-70ccddf6 (east of the Oshodi link) and rd-490724c3 on curves of 195 and 334 m (tightest bend 81 m, corners 1.5 and 0.6 deg), the knot between them moved to where the link down to Apapa Road leaves; raised 7.5 m over Ikorodu Road's express and two service roads (7.49, 7.52, 7.50 m), ramps 5.5% held to 5.8%, steepest 5.6%; links rd-b4be5eda (down to Apapa Road, meets the deck 4.7 m up), rd-a550750d (from Anthony Village Road, 5.5 m up) ramping to the deck, steepest 7.6% (the land there is rough: held to the ramp limit both ways, cut 0.53 m into it at most) and 5.9%, rd-0fbc2dcc on the land, its start loose; Apapa Road rd-f458561e and Anthony Village Road rd-1503de43 on the land from Ikorodu Road's east service road, Apapa Road cut back 30 m short of where the expressway's east curve now passes; read on Google satellite by eye (the bridge, the bend away east, the links to Anthony Village Road and Access Road match); clashes 1297 to 1336 (85 new: 31 d28 houses under the new roads, d28 streets under and beside them; 46 gone, mostly the old east piece drawn on d28's rd-cbaebc6a for 565 m, now 193 m); owed on it: [ ] the loop off the westbound bridge down to Ikorodu Road's west service road (Overture 7f326d), left out: it leaves 53 m from the road the bridge crosses, where at 5.8% the deck is still 4 m up (Google satellite shows it as a big loop), [ ] Ikorodu Road's six express-service slips here, [ ] Anthony Village Road on (Overture 762511) and Apapa Road's and the west link's loose ends joined, [ ] the two side streets' 6 m corners read (Google satellite z18) and eased if cars can't take them, [ ] d28's rd-cbaebc6a (the expressway drawn again for 193 m) and d28's streets under the links (rd-90772fe4, rd-79282a08, rd-ae7949a3, rd-30407730) re-joined in d28's pass, [ ] the twins rows at the old ends moved to the crossing, [ ] the widths read (24 m expressway, 8.7 m links, 11 m streets, not read)), [x] Third Mainland Bridge's fork at Ebute-Metta (29 Oct, whole at real size by the same rule: Overture's junction (the bridge's two carriageways, four links to and from Clinic Road's bridge, Clinic Road's eastbound piece) placed at real size, slid (6, -156) m and turned 5 deg onto the drawn bridge where it fits best (14.5 m off it, root mean square, within 700 m); the bridge rd-e7a23019 on the middle of its carriageways from 40 m past one fork to 40 m past the other (1290 m), eased back onto the drawn line on curves of 255 and 195 m (tightest bend 145 m, corners 0.6 and 1.0 deg), drawn points 34-56 replaced, on the land as the rest of it; Clinic Road rd-750432c4 redrawn on the middle of its carriageways from the junction to where it crosses the drawn Herbert Macaulay road rd-2689394b (182 m; real 975 m to there), joined at that crossing; the links rd-e38c8fd1 and rd-f691d9e0 kept whole (they swing up to 75 m out before flying over the bridge), eased onto the one-line bridge 21 m off its middle on curves landing 15 deg off it, 6.87 and 7.50 m over it where they cross; rd-aae94fd5 7.51 m over rd-e38c8fd1, rd-f691d9e0 7.33 m over it; rd-7382f27e and Clinic Road's eastbound rd-a8efbae0 on the land; steepest 6.0% point to point (rd-aae94fd5, rd-e38c8fd1, on 5 m steps, the heights rounded to the cm), 5.9% over 10 m; rd-aae94fd5 joins rd-e38c8fd1 11 m before their shared end and rd-a8efbae0 leaves Clinic Road 15 m on, where they run together; the draft's hook rd-b0b218e4 stays (Saba's streets join it), its end now loose; clashes 1336 to 1389 (100 new: 52 houses of d16, d17 and d19 under the links, their streets; 47 gone with the draft's Clinic Road line); owed on it: [ ] the d16, d17, d19 houses and streets under the links in their passes (at 1:3 the real links, over the swamp in Lagos, land on Ebute-Metta's streets), [ ] Clinic Road's end 1 m from d17's own Herbert Macaulay rd-96ed58e3 and rd-93fdb33d joined in d17's pass, [ ] rd-b0b218e4's loose end read (Overture 94da8b, the ground link into Clinic Road, not drawn), [ ] rd-a8efbae0's 25 m and rd-aae94fd5's 37 m bends where they meet Clinic Road eased, [ ] which link is on top where they cross read on Street View (Overture puts all at level 1), and the bridge's own height over the swamp, [ ] the twins rows at the old join moved, [ ] the widths read (8.7 m links, 24 m Clinic Road, not read)), [x] Ring Road over Awolowo Road at Ahmadu Bello Way (29 Oct, whole at real size by the same rule: Overture's junction (Ring Road's two raised carriageways, Awolowo Road under them, the three links between them) placed at real size, not moved or turned (the drawn knots lie 8.8 and 18.5 m off the real line); Ring Road rd-288c15dd redrawn on the middle of its carriageways from the knot at Third Axial (14876.91, 8704.99) to the junction with the Marina and Ahmadu Bello Way (14651.71, 9102.66), 471 m, its ends bent onto the knots over 100 m, tightest bend 115 m; lifted 7.5 m over Awolowo Road (7.50 m clear), ramps 5.5% held to 5.8%, steepest 6.0% point to point (5.97%), z on all its points, 1.3 m at the knot as Third Axial; the draft's second line and pieces rd-c73c65b1, rd-e3b1dcb5, rd-adc34838, rd-3adf0a21, rd-33c893d7, rd-77f41edb taken out (26 ROAD corner rows on these and the old rd-288c15dd gone, a 178 deg double-back among them; none new); Awolowo Road rd-747e0c42 new, 656 m on the middle of its carriageways, on the land, its west end joined where the drawn road from the Marina junction rd-b05f0ee7 crosses it at 1:3 (20 m of the real line past it left out), its east end loose; the links rd-2191f68a, rd-7e02d6d7, rd-a4abb554 on the land, eased onto the one-line Ring Road as forks landing 15 deg off it (the parting point searched nearest the end first for a 60 m or gentler bend: 25, 60 and 96 m of their real line replaced), their Awolowo ends bent on (1.5-4.0 m) and redrawn as curves; the link from the north-going side really leaves past the Marina junction, which 1:3 brings closer: its first 161 m left out, it leaves 20 m before that junction; tightest bends 83, 41 (the real loop up from Awolowo Road) and 56 m; read on Google satellite by eye (the raised Ring Road, Awolowo Road under it, the links up on the east and down on the west match); clashes unchanged at 1389; owed on it: [ ] Ring Road raised as Overture has it (level 2 all along here, on to the Ring Road Bridge) read on Street View, heights not read, [ ] Awolowo Road's east end and the side streets joined when Lagos Island's (Ikoyi's) streets are drawn, [ ] whether Awolowo Road really meets the Marina junction's road (here a hand join at 1:3) read, [ ] the twins rows jn-6027745e, jn-230c957b, jn-dcb5909a, jn-3269fbec, jn-12eb3860 (the draft's junctions) moved to the new nodes, [ ] the widths read (24 m Ring Road, 11 m Awolowo Road, 8.7 m links, not read)), [x] the Eko Bridge's end on Lagos Island (29 Oct, whole at real size by the same rule: Overture's landing placed at real size, slid (135, 10) m and turned -5 deg onto the drawn bridge where it fits best (17.0 m off it, root mean square, within 800 m); the bridge rd-8d8116e2 on the middle of its carriageways from 200 m before its loops part on down Apogbon Street to where that meets the drawn Marina road rd-b05f0ee7 (at 1:3 the Marina road runs where Apogbon Street does), eased back onto the drawn line on a 163 m curve (bend 529 m, corner 0.4 deg) that lands before the shared points of rd-2eec8135 and rd-3c374b41; now 1233 m (was 945), z on all points, lifted 7.5 m over the Inner Ring Road loop (7.51 m clear), steepest 5.96%; the Marina road rd-b05f0ee7 starts on the bridge's line (its last 334 m, to the old end, taken off); Ring Road rd-322bc528's last 187 m (it stopped 13 m short of the bridge, the hook rd-06606376 on, now taken out) redrawn from its junction with rd-286edfeb as a 116 m curve (bend 61 m) to where the real Ring Road starts; two loops at real size, rd-243b5af1 (off the bridge round the Inner Ring Road and under the bridge to Ring Road, Overture b314f9, 155bdf, 3b5f27, 45672d; leaves the bridge at z 6.59, 5.3 m over the land) and rd-dc498b0b (from Ring Road round onto the bridge, d5113a, 7f048d; joins it at z 5.54, 3.4 m over the land), eased onto the one-line bridge as forks, heights from the roads they join, raised only (never cut into the land), steepest 5.96% and 5.97%; read on Google satellite by eye (the bridge landing, Apogbon Street on south, the big loop round by Adeniji Adele and the loop by Ebute Ero match); check_map passes; clashes 1389 to 1391 (the d16 rows on the bridge's line by Carter Bridge's foot changed: house b-c3e45656 142 m2 under it, was 49.6; rd-3ee9757d now almost meets it); ROAD corner rows 3032 to 3027 (the hook's 5 gone); owed on it: [ ] the Carter Bridge's end, not touched: the drawn Carter Bridge rd-7f4e577e lands flat on rd-286edfeb and rd-2eec8135 at (13951, 8067), the real one lands on Ring Road by two ramps (Overture c0c6ff, e09c20), read and placed whole, [ ] Apogbon Bridge south (Overture f1f330, d17eac) and the Inner Ring Road and Adeniji Adele Road on from the loop drawn, [ ] the d16 clashes beside the bridge's tie (rd-d6e90d7a, rd-3ee9757d, b-c3e45656) in d16's pass, [ ] how high the bridge really runs on to Apogbon and the loops' heights read on Street View (Overture: level 1), [ ] the twins row jn-67d34561 moved, [ ] the widths read (24 m bridge, 8.7 m loops, not read)), [ ] Ring Road's sharp bends west of Third Mainland (owed in the cloverleaf entry), [x] the loop bridge on the Badagry Expressway at (8900, 8530), whole at real size (29 Oct): Overture's two raised ramps (dc8c42, d4e72c, level 1) as rd-2ab78c89 (705 m) and rd-166a257a (607 m), lifted 7.5 m over the expressway (7.64 and 7.49 m clear), steepest 5.95% point to point, their far ends eased onto the one-line expressway as forks; the draft's two 90 m bits redrawn as the real ground links 38524f and 389cfd (rd-f3179f2f 247 m, rd-3622e3bd 278 m), sharing the ramps' street ends, on the land with no z; the expressway's 17 m dent where the bits met it redrawn as one curve (moved 14.9 m at most); fit 10.0 m RMS, slid (-35, -120), turned 3 deg (owed: [ ] the south and north service roads the ramps and links really land on, [ ] the streets at the ramps' loose ends, [ ] Street View, [ ] the widths read (8.7 m ramps not read)), [x] Ojota's two leftover ends (29 Oct: the expressway's draft line rd-a4d4d18c ran on straight to (13754.27, 3260.26), then hooked back 82 m on itself to a point it already passed through; the hook taken off and the line carried on 37 m, turning 1.3 deg, to rd-62d35e3f's first point, now shared, so the expressway runs through Ojota unbroken between its two slip roads); [x] the others read (29 Oct, each loose end against Overture's real roads at 1:3 around it, 250 m and 2400 m real; by eye on the plot, not yet on Google): two real ends, rd-bfbe3545 (ends on Eko Atlantic's coast boulevard, whose streets are district work) and rd-2071dded (ends where it meets two secondary roads, below the network's classes); four gaps, each its own fix: [ ] rd-c6144c6c stops ~450 m short of the road it really runs on to (Overture's primary/secondary goes on to meet rd-f68b428f at about (12680, 3000)), [x] rd-37c2a1ad (the Airport Road) carried on 457 m to the terminal's forecourt (29 Oct: the midline of Overture's two carriageways, 13.7-13.9 m apart at 1:3, turning 0.7 deg at the old end; ends loose at the forecourt; owed: [ ] its real lift (level 1) over Airport Road's crossing at about (11665, 4485), with that street), [ ] rd-ee461730 stops 55 m short of the Lekki expressway rd-e1e529ec where a real street carries on to it, [ ] rd-52faba3e turns off where the real trunk carries on west along y ~9800 past x 15900, not drawn (the biggest; read with the Lekki carriageways item); [ ] Badagry's and Lekki's carriageways left as two lines; [ ] each road's width read, longest first; [ ] the junction place names read (nearest frame-study place today). The Fourth Mainland Bridge and the coastal road kept (owner, 28 Oct), the bridge as being built; (c) [ ] rail into d00 after the roads, laid on the real lines as the roads are, ignoring what the districts drew (owner, 29 Oct: "lay it out after we finished the roads... ignore anything the districts had previously done... the districts are the last things to be done anyway and are supposed to shape around the interconnection"); PR #453, d15's rail drawn on in the district, closed as replaced by it;
   (d) [ ] water into d00; (e) [ ] gidi-game builds d00 alone on the land (relief grids as one Landscape,
   roads from road_build) with a car to drive: first a road kit of shared instanced pieces (lanes, decks, ramps, kerbs, joins), researched from how studios and Epic build road kits before it is made (owner, 29 Oct: "work till the point where you get all the roads, and then begin to make kits for the instances for them, so we can run it in Unreal and drive a real car or danfo or keke or Okada there"); the kit read from many Street View photos of Lagos roads (study only, nothing copied), with a done list of what matters on a road, each ticked on the map as it is drawn and built (owner, 29 Oct: "it would mean a lot of street view photos, and ticking off on the map done list things that are important to the road. Please don't forget"): [ ] the list itself written from the photos first (lanes and markings, kerbs and gutters, open drains and their slabs, medians and barriers, bus stops and BRT lanes, junction lights, signs, street lights, overhead bridges for walkers, the ground under flyovers, road wear and potholes, roadside sellers' spots); the vehicles at real size (car, danfo, keke, okada); (f) [ ] the owner drives it. District work waits except what a piece
   forces; clashes with district work are listed by check_map (CLASH), not fixed (DECISIONS "Clashes with district
   work are listed"). Owed: [x] check_map reads heights where roads meet and cross (28 Oct): a road with no z lies on the land, read from the relief grids, and roads sharing a point share its height within 0.2 m (SHARED_DZ); it found Isolo Road's deck in d15 still drawn on the old 0 m ground, lifted by hand onto the land (+8.25 m), and 24 rows where Ojota's ramps and raised Ikorodu Road meet Gbàgede streets less than 6.7 m below (crossings, and street ends now inside a ramp), listed as clashes for the d28 pass; [ ] the board shows the CLASH list (today it shows check_map's failures only, not
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
       read on Google, piece by piece, the owner checking each piece. Piece 1 [x] the Third Mainland Bridge (rd-e7a23019, moved from Ṣọmọlá into d00 at its full real length, 3,266 m Gidi; 33.1 m wide with a 3.5 m median and four lanes each way, ICE's figure, read 28 Oct, replacing a by-eye 37 m; for it 6 Ṣọmọlá houses left out and 25 cut, 3 lanes moved off it, 2 removed: Ṣọmọlá's rd-7292fb80, Ìbùdó Mẹ́ta's rd-0877e4b9); owed on it: [ ] its heights z (Overture flags it raised all the way, but Street View at Oworonshoki, Jul 2021, shows it at grade there; no published deck height found (Wikipedia, ICE); Copernicus GLO-30 reads 5.8-6.4 m on the deck at s 2250-2550 against 0 beside it, the rest of the deck flattened with the lagoon, a weak reading at 30 m), [ ] then put back Ìbùdó Mẹ́ta's lane rd-0877e4b9 under the deck (removed 28 Oct: it ran under the bridge with no height to pass under; its record is in the git history of map/d16/plan.json), [ ] the Ṣọmọlá lanes that end on the bridge at grade (rd-80254433, rd-efb526e0 and others at the interchange) read on Google, as the real road is fenced there. Piece 2 [x] Ikorodu Road (28 Oct): the four 40 m district records (Mùṣá rd-i4klmw3w, rd-3079cryq, Ṣọmọlá rd-7a9ab6b8, Gbàgede rd-9e02217d) replaced in d00 by the express in four pieces at widths read on Google satellite by eye (motorway 27.5 m at Onipanu, 19.6 m at Obanikoro, trunk 45.7 m at lon 3.42 and 35.5 m at lon 3.45, each with a concrete median) and its service roads both sides where Overture has them (s 100-2310 and 2530-3180), 4.8-6.7 m, with slips; 32 district roads that were Ikorodu Road drawn twice removed; 45 houses left out and 42 cut back (2,805 m2 and 2,142 m2 of roof); check_map's city layer may hold service_road; working_bar's place check measures a point on the city layer's road from the whole road's outer edge. Owed on it: [ ] its heights z and the flyovers (Fadeyi, Jibowu, Ojota, Maryland), [ ] the BRT lanes as their own records, [ ] the bus bays, [ ] the Ojota and Jibowu interchange shapes, [ ] the strips at Ojota north (71.4 m overall read, not split), [ ] Mùṣá's Jibowu flyover rd-avaupyki still in d15, [ ] the service roads' ends read on Google (taken from Overture, not checked), [ ] the roof lost under it given back by hand in Mùṣá, Ṣọmọlá and Gbàgede (Mùṣá's cover 43.06%, below Google's 43.26%); (3t) [ ] the land's height (DECISIONS "The land's own height too", owner 28 Oct): data in hand [x] GEDTM30 v1.2 bare-earth heights for the frame, downloaded 28 Oct with the owner's OK (8 MB, ~/gidi-data/research/data/gedtm30/, README there gives source, licence CC BY 4.0 and the credit); DeltaDTM was the first choice but its host would not connect from this Mac (port 443 closed), FABDEM is non-commercial. Checked against our Copernicus GLO-30 at 9 places on land: within 1.8 m. Inside the frame: -2.0 to 74.2 m, median 5.7 m; its own uncertainty median 0.58 m. Not checked: the earlier note that Zenodo's page calls it for testing (the v1.2 record's licence field reads cc-by-4.0; its description not re-read). In the map [x] (28 Oct): the land as 297 relief grids in map/d00/dress (1 km each, 10 m between points, 2,893,347 points, -2.8 to 72.2 m, 14.3 MB), drafted by `scripts/draft_terrain.py`; [x] redrawn at 1:3 heights (owner, 28 Oct, DECISIONS "The land's own height too"): -0.9 to 24.1 m, 13.3 MB; along Ikorodu Road the 10 m stretches steeper than 8% fell from 31.7% to 1.0%; `check_map.py` holds them to one spacing, the whole frame and equal shared edges; MAP-FORMAT says a thing's z is above the land. Owed on it: [ ] the water beds (4.6% of points have no reading, open water, held at 0 until the water records carry depth), [ ] Unreal reads the land as one Landscape (2,701 x 1,051 points fits 22 x 9 components of 126 quads; Epic's tiled heightmap import is reported broken in 5.7-5.8 on the forums, not tried), [ ] a check that a house's footprint and a road's width sit on land without a step too big (the slope under them), [ ] the board shows the land (how it draws d00's relief grids today not looked at); (4) the 11 drawn districts' roads measured
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
