# Mùṣá: the buildings draft and its hand pass

Drafted by `scripts/draft_buildings.py` (owner, 23 Oct: real footprints, then hand). 1457 houses in 41 blocks. Each block's number is its place in size order. After the run, 31 houses that crossed the district line were taken out (the tool now keeps only houses wholly inside), leaving 1426; the counts below are from before that.

## Hand pass 1 (23 Oct): the houses that fell on a road

The roads stay on their real lines; a copied house on a road fell in the wrong place, not the road. Of the 104 (the table's
110 counted a few twice), 44 were set back by hand on clear land beside where they fell (within 15 m, not turned, each
checked on a picture); 60 were left out, because the frontage beside them already holds its copied houses. 1,470 houses now.

## Hand pass 2 (23 Oct): overlaps

173 houses that overlapped a neighbour (up to 10% of the smaller, 968 m² in all) were trimmed back to the bigger
house's wall, so neighbours share a party wall as in Mushin; the biggest trims were checked on a picture. No two houses
overlap now.

## Hand pass 3 (23 Oct): block B1's lanes and houses, from the Google study

B1 (the expressway's east service road, Ladipo Street, Palm Avenue, Isolo Road) was studied on Google satellite at its
real twin: a warehouse strip along the expressway, then the Ladipo-Odunsi grid, houses wall to wall. Ten streets were
drawn by hand on that pattern (STREETS.md, "Lanes drawn by hand"). The copy draft could not follow lanes drawn by hand,
so B1's houses were redrafted: the grid's blocks with the twin's own houses turned to face their lanes
(`draft_buildings.py --frontage`), the strip with the twin's own sheds (`--sizes=600,20000`), the rest copied. B1 now
holds 298 buildings at 53% cover (it was 132 at 24%). The block numbers in the table below are from the first draft.

## Hand pass 4 (23 Oct): block B0 (Idi-Araba, LUTH), from the Google study

Nine streets drawn by hand on the real twin's pattern (STREETS.md): LUTH's drives as service roads, six housing
streets. Housing blocks redrafted with `--frontage` (50-65% cover); the campus (LUTH, the College of Medicine, Birch
Freeman) keeps copied real buildings with its greens between (`draft_buildings.py`, copy). B0 now holds 343 buildings
(it was 222). LUTH wants its own place record (campus wall and gates) in a later pass.

## Hand pass 5 (23 Oct): block B2 (Ishaga Road to Lawanson), from the Google study

Seven lanes drawn by hand on the real twin's pattern (STREETS.md): the north-south streets off Ishaga Road, Daniyan on
the canal bank, two south-west streets towards Lawanson and Adedoyin's pocket. All four of B2's blocks redrafted with
`--frontage` (54-68% cover per block); 367 buildings (136 before), 51% cover over the whole block.

## Hand pass 6 (23 Oct): block B3 (Mushin station to Ikorodu Road), from the Google study

Fifteen lanes drawn by hand on the real twin's pattern (STREETS.md), on both sides of the rail. B3's four blocks
redrafted with `--frontage` (50-68% cover per block): 339 buildings (150 before), 50% cover. Still empty: the strip
between Bada Street's twin and the Ikorodu Road edge (Bada was joined to Adewusi after the draft), for the next hand pass.

## Hand pass 7 (23 Oct): block B4 (Ladipo market and the Matori estate), from the Google study

Seven streets drawn by hand on the real twin's pattern (STREETS.md). B4's three blocks redrafted with `--frontage` and
`--sizes=12,20000`, so the market sheds and warehouses come through: 214 buildings (40 before), 53% cover.

## Hand pass 8 (23 Oct): block B5 (Akanro, Ilasamaja), from the Google study

Three lanes drawn by hand on the real twin's pattern (STREETS.md). The block redrafted with `--frontage`: 190 buildings
(108 before), 59% cover, in rows along the real streets.

## Hand pass 9 (23 Oct): small blocks B6, B7, B9, studied at close zoom

Lanes from z17 Google shots (STREETS.md); houses redrafted with `--frontage --sizes=12,20000` so the factories by the
expressway and the big halls come through: B6 241 buildings (59% cover), B7 116 (62%), B9 152 (60%).

## Hand pass 10 (23 Oct): block B1 redone from a close-zoom study

B1's lanes were redrawn on the real streets' lines (STREETS.md: 20 streets in place of the 10 offset lanes of hand pass
3). Its houses were cleared and redrafted: the grid with `--frontage --sizes=12,20000`, the warehouse strip with
`--frontage --sizes=300,20000`. B1 now holds 347 buildings at 54% cover.

## Hand pass 11 (23 Oct): block B0 redone from a close-zoom study

B0's lanes were redrawn on the real streets' lines (STREETS.md: 36 streets in place of the 9 lanes of hand pass 4). Its houses were cleared and redrafted: the housing with `--frontage --sizes=12,20000`, the LUTH campus with `--frontage --sizes=300,20000`. B0 now holds 520 buildings at 49% cover (was 343 at 39%).

## Hand pass 59 (26 Oct): the danfo park at the Agege Motor Road / Isolo Road junction; two road shapes looked at

STREETS.md names a motor park at the Agege Motor Road / Isolo Road junction ("the park itself is a place for later"),
which pass 56 missed when it called none in Mùṣá (and pass 57 called Jibowu the one). On the satellite (study only) the
danfos load in the mouth of Isolo Road beside the junction, with no yard off the road. So the park is drawn the way the
bus stops are: pc-ojuwyprk, a motor_park place 6 m deep on Isolo Road's south edge (half on the carriageway, where the
danfos stand), 12 to 42 m west of the junction, clear of the trunk and cut 0.15 m off the houses: 124.3 m2. Uses
pick_up, drop_off, load and unload; hours 05-23, a guess; no name.
Two road shapes owed in NOW item 10 were measured against Overture's real street segments (open data, converted to
Gidi): both are on their real lines, so nothing was redrawn. Olushoga Street (rd-b9jn4qv9) follows four real segments
round a small block, through Olawoyin Street's end and Church Street's start: its 19 points lie 0.01-1.42 m from a real
segment. Omowunmi's hook (rd-9o8evlk2) is a real service lane looping off Isolo Road and back: 5 points, at most 0.10 m
off. The "Isolo Road kink near Omowunmi" was where Omowunmi ran 56 m along Isolo Road, split off as the hook on 25 Oct
(STREETS.md, rd-9o8evlk2's row); Isolo Road's own line now turns 28 degrees at most.

## Hand pass 58 (26 Oct): walls and gates round the two schools and the Vono Road factory

Mùṣá's first `wall` records. Each runs 0.2 m inside its plot's edge (the plot less the roads' carriageways), and is open
where a neighbour's house already closes the compound (B28's north side: five pieces). The reads give the look: "painted
school wall", "long painted school wall" (rows 66, 207, 338), so the schools' walls are rendered, painted cream
(#d8c9a0), 2.1 m, mouldy, piers every bay, with a 4 m two-leaf sheet-steel gate with a wicket (blue, #2f6b8a): B28's at
Bakare Close's dead end (STREETS.md B28), B29's on Post Office Road (chosen: its driveway is not read). The factory
(row 435: "factory wall", "factory fence painted blue"): 2.8 m rendered wall with razor wire, piers every bay, and a 7 m
blue sheet-steel gate on Vono Road beside its gatehouse. B29's plot and place reached 2.1 m2 onto Palm Avenue's
carriageway and the factory's 0.09 m2 onto its road; both were cut back to the carriageway's edge. Still to draw: the
schools' and factory's faces, the ice-cream advert on the factory wall.

## Hand pass 57 (26 Oct): the Jibowu coach yard (and see pass 59: not Mùṣá's only motor park)

The coach yards at Jibowu front Ikorodu Road between Rahony Travels and Polarplus (Google satellite at zoom 19 and the
ySG Park Jibowu point, study only: open 24 hours). Read off the satellite, the yard (about 39 by 50 m real) lands in Gidi
at (13349-13363, 6180-6197), 186 of its 219 m2 on the motorway rd-3079cryq: the road is drawn at its full width, so the
yard moves off it. Houses give way: the two houses that fronted the motorway at that spot, b-a368fc34 (2 storeys, 85 m2)
and b-11567139 (a 28 m2 bungalow), neither holding a place, are removed. Their ground is now pc-jbwyard1, a motor_park of
119 m2 (12.6 by 14.6 m; the two houses' hull, kept 0.15 m clear of the neighbours and the road). Uses pick_up, drop_off,
load and unload; hours 00-24; no name ("name to give (a sound-alike)"). It is small for coaches, about two or three.

## Hand pass 56 (26 Oct): two more bus stops; motor parks looked for

Two real bus stops inside Mùṣá were found on Google Maps (study only: a point each, nothing copied): Mushin Bus Stop, on
trunk rd-kxa8hz1b, and Olosha Bus Stop, on home street rd-0bb0jt00. Each is a 6 m bus_stop square on its road's edge
(pc-7410cdf5, pc-d1518de7), with uses pick_up and drop_off and no name ("name to give (a sound-alike)"). Neither was
within 40 m of the two stops already in from Overture. Motor parks: Google's "motor park" and "garage" searches around
Mùṣá give Itire Road Motor Park (95 m outside Mùṣá, so it belongs to the neighbour), ySG Park Jibowu (its point lands on
Ikorodu Road's carriageway at Mùṣá's edge, 18 m in) and transport companies' offices (God Is Good Motors on the
expressway: an office, not a yard). Daleko, seen on the satellite, is market sheds, not a park. So no motor park was
drawn: Mùṣá's danfos load at its bus stops. Overture's 11 "parking" points and 1 "park" in Mùṣá were read by name: all
are businesses or a school (services firms, events, decor, a builder, a charity, a garden, a private school), none a
park or yard (their spots were not looked at on the satellite); a yard at Jibowu (Lawani Street side) is owed, drawn from the satellite.

## Hand pass 55 (26 Oct): the real churches, mosques, schools, clinics and the rest, as places

Overture's places (open data, CDLA, docs/DATA-SOURCES.md) hold 2,437 points inside Mùṣá. Those whose category, or, for the
vaguer categories, whose name, says what the game uses them for were made into 516 places: 227 churches, 130 schools,
48 garages (mechanics), 32 clinics, 32 bukas, 16 mosques, 16 bars, 4 banks, 4 fuel stations, 3 chemists, 2 police
stations and 2 bus stops. A "religious organization" counts as a church or mosque only when its name says so; a church
newspaper and a fellowship's chapter are left out. A school from the "education" category also needs its name to say so.
Each place's area is the house its point stands in, or the nearest house within 8 m (43 points had none and were left
out). There is one place per house and kind (54 repeats dropped), and none inside the market and the two schools already
drawn (9 dropped). 462 houses now point to their place: a house with two kinds points to the first. A bus stop is a 6 m
square at its point, not a house. One stop stood 16 m off any road and was moved onto the nearest road's edge. No real
names went on the map: each note says "name to give (a sound-alike)", and the place's category and Overture's confidence.
Uses: church and mosque pray, school learn, clinic heal, chemist buy and heal, bank money, fuel fuel and buy, bus stop
pick up and drop off, bar drink and rest, buka eat and buy, garage fix_vehicle, police story. Hours are left empty.

## Hand passes 52-54 (26 Oct): the station's platforms; houses off the road edges and off each other's walls

**52, the station.** The real canopies' two ends were read off Google's satellite (right-click: 6.533319, 3.361079 and
6.531498, 3.361809; study only, two points); in Gidi they fall 2-3 m off the rail's line, 72 m apart. sn-romgcujc now
has two island platforms between those ends, each 3 m wide, 3-6 m either side of the line, and its area is the
corridor (9 m each side) between the ends. The placeholder area was 30 m wide and took in houses. The station building
beside it is not drawn yet.

**53, slivers on the road.** 110 houses reached into a carriageway by less than 1 m2, which the check lets through.
Each was cut back to 0.15 m clear of the carriageway's edge (as in hand pass 43, the road stays): 28 m2 in all,
0.99 m2 at most.

**54, party-wall hairlines.** The board marks a house red when its outline crosses another's (web/mapedit.js
`polysOverlap`), which the check lets through up to 0.5 m2. 1,221 houses crossed a neighbour, mostly by hairlines from
rounding (median 0.002 m2, 0.23 at most). In each pair the smaller house was cut back 2 cm off the bigger one's wall, as
in hand pass 2: 655 houses, 61 m2 in all, 0.48 m2 at most. After that the board's test, run over all of d15, finds no
crossings. Passes 53 and 54 together changed 758 houses (89.7 m2 in all; the smallest house left is 13.3 m2), and each
one's note names its pass.

Left: the board also counts a house as on a road when it falls inside the road's rounded end, i.e. within half the
width of the end point. The check, and pass 53, end a road flat. 106 houses are inside a rounded end, by up to 24 m2,
mostly where a lane stops at a house. Whether a road ends round or flat is a question for the board's test, not the
houses, so it is owed (NOW item 10).

## Hand pass 51 (26 Oct): the rail's, the station's and the market's missing fields

Google's satellite view of the real line at the station (about 70 m across, by eye) shows the standard gauge and the Red
Line side by side: 4 tracks on stone ballast, a concrete wall on each side, and both platforms roofed end to end. So
rl-u7rtwbrj has tracks 4, ballast stone, fence_left and fence_right wall, and corridor 18 m: that is the drafting width
the houses were already set back to (hand passes 47-48), and it holds 4 tracks at about 4 m apart. sn-romgcujc has canopy
true; its area and platforms are still the placeholders from the station point. The spare-parts market pc-4xhy1iet
(after Ladipo) has uses buy, sell, fix_vehicle, load and unload, open 08:00-18:00. d15's check: 0 problems.

## Hand pass 50 (26 Oct): every road's ground colours, from Mushin Street View

357 of the 359 roads had no `ground_look` (the check's 357 "missing field" rows); the other two keep the Ladi Lane shot's.
Each road now has the colours of its own read surface (road_reads.tsv), as the median of a patch of road in a Street View
pano of a Mushin street with that surface. These are lit photo colours (sun or overcast, as noted), not albedo; how much
dust lies on a road is still its `sand_cover`. A surface without a layer leaves it out (no tar on sand, earth, interlock
or concrete).

| surface | roads | tar | dust | earth | mud | from (pano, light) |
|---|---|---|---|---|---|---|
| tar_worn | 225 | #a6937c | #b89e86 | #886e59 | #866e53 | 11 Sadiku St, Jul 2021, sun (bare tar, dusted middle, earth verge) |
| sand | 71 | | #dfbca3 | #d0b99a | #866e53 | 46 Alasalat St, Jul 2021, sun (road middle, apron) |
| earth | 44 | | #b3a18d | #b38a67 | #9b8970 | 8 Wahab St, Jul 2021, overcast (road, apron, wet tyre track) |
| interlock | 11 | | #aea496 | #aca195 | #866e53 | 20 Igbira St, Jul 2021, overcast (dusted pavers, earth edge) |
| concrete | 3 | | #c6bbaf | #886e59 | #866e53 | Igbira St's concrete slab (Daleko Market Rd's road was hidden by a crowd) |
| tar_new | 2 | #655e53 | #6c6352 | #886e59 | #866e53 | 19 Badejo Kalesanwo St, Mar 2024, overcast (middle, edge) |
| laterite | 1 | | #b3a18d | #b38a67 | #9b8970 | none sampled: Wahab St's earth for now |

The mud everywhere but on earth roads is Wahab St's wet earth by the drain (#866e53). Owed (NOW item 10): a laterite and
a concrete road sampled from their own panos; interlock's paver colour has no layer in `ground_look` (the dust stands in).

## Hand pass 49 (26 Oct): front houses on the busy roads given lock-ups

`draft_kinds.py` gave lock-ups only to houses within 3 m of a busy road (market, main, trunk, local main, service), so
front houses standing 3-6 m back stayed homes (the note above). 113 homes stand 3-6 m from a busy road; 69 of them face
it with nothing between (no other building across the gap from the house's nearest point to the road edge, and at least
4 m of the house within 1.5 m of that nearest distance). Each road's Street View reads (road_reads.tsv) were read by
eye: on the 22 roads whose reads show shop rows, lock-ups, kiosks or stall rows, the 57 front houses there were given
lock-ups (45 two-storey compound houses became shop-under-flats; 8 bungalows and 4 shacks kept their kind with lock-ups
on the ground floor; ground storey at least 3.4 m). On rd-76xj78h3, rd-90g2sje2 and rd-c77w49vw (reads: compound walls
and gates) and rd-yp7rd186 and rd-8rjr3ndf (no Street View) the 12 stay homes. Each record's note says which road.

## Hand pass 48 (26 Oct): the 10 houses inside the rail corridor set back

Hand pass 47's measure found 10 houses 7.7-9.0 m from the rail's centre line (inside the 18 m corridor the drafting
keeps clear): b-16cede5b, b-1a6726da, b-2bb2123d, b-42865a3a, b-48838f4b, b-5671f844, b-7c6ca644, b-aa9de80a,
b-d2f534c2, b-e37c0b5c. Each was trimmed on its rail side to 9.5 m from the centre (1 to 27 m2 off, the median 5),
its other sides and its winding kept. Five others stand 9.04-9.35 m from the centre (b-1710cb6d, b-62815b08,
b-7f54d471, b-480b54b4, b-12474b6a), outside the 9 m half-corridor, and are left as they are.

## Hand pass 47 (26 Oct): B33's railway strip looked at again

Hand pass 39 said the real strip along the railway in B33 (between Olateju Street and the rail, now the block at
x 13107-13162, y 5756-5825: block numbers moved when lanes were added) is mostly bare ground. On the underlay at close
zoom the bare ground is a strip of about 4-6 m between the houses and the line, the rest of the block is built; in the
map no house in the block stands nearer than 9.0 m to the rail's centre line, which is that strip. Nothing removed. The
rail's own corridor, tracks, ballast and fences are still unset (the rail record's note; check_map's missing fields).

## Hand pass 46 (26 Oct): the Vono Road factory (the old B27)

The factory inside Vono Road's loop (road_reads 435: factory wall, blue fence) held two drafted shop-under-flats
(b-7dc8c34e, b-4ba51d3c), removed. Drawn in our own layout after the underlay's pattern (big sheds round a loading yard),
not traced: a `compound` plot pl-b27facto on the land between Vono Road, the trunk road and d15's edge, kept 10 m clear
of the rail's centre line (5,469 m2), and
four `shed` records b-b27fac01..04: the big shed in the north tongue (736 m2, 7.5 m, 12.3 m from the rail's centre), the long shed along Vono Road (492
m2), the store along the trunk road (217 m2), all longspan gable roofs and workshop ground floors, and a gatehouse on Vono
Road. The schema has no factory kinds (plot, house or place); shed and compound stand in. Still to draw: the factory wall
and gate, faces.

## Hand pass 45 (26 Oct): the school compounds in B28 and B29

The two real schools (STREETS.md B28 and B29) were filled with drafted houses. Those inside each compound were removed
(B29: b-cedf79a7, b-b76ab891, b-2538195c, b-5c1fe22a; B28: b-1a8f2d7e, b-0c2d321d, b-2e3a7a74, b-b15fa18a) and each
school drawn in our own layout after the real one's pattern on the underlay, not traced: a `school_ground` plot behind
the kept frontage houses, a `school` place on the same outline (uses learn, 07:30-14:00) and classroom blocks of kind
`school`. B29, Ṣokúnlé Primary School (sound-alike of Shokunbi Primary): five blocks round two yards (b-b29sch01..05).
B28, name not read yet: four blocks round one yard (b-b28sch01..04), its gate side at Bakare Close's dead end. Still to
draw: their compound walls, gates and faces.

## Hand pass 44 (25 Oct): houses set back from the 23 lanes given widths by hand

The 23 lanes no Street View reading gave a width were given the gap their houses leave (STREETS.md); where that put a house on a lane or its gutter, the house was set back as in hand pass 43: 162 set back (0.2 m at the median, 1.7 m at most), 65 of them trimmed to a neighbour's wall, 9 cut to the road edge, none left out. After: no house more than 1 m2 inside a carriageway, no overlap over 0.5 m2; 4,275 houses.

## Hand pass 43 (25 Oct): houses set back from the roads' read widths

The roads now carry their widths read in Street View (STREETS.md, "Roads read in Street View"), wider than the defaults the houses were drafted against (a lane was drafted at 4 m, reads 7 m); 2,338 houses fell more than 1 m2 inside a carriageway (by 0.8 m at the median, 1.45 m at the 90th). As in hand pass 1 the road stays and the house moves: each house inside a road's width plus its gutter (0.5 m where the road has gutters) plus 0.1 m was set back straight away from the road's centreline until clear (0.95 m at the median, 4.1 m at most, never turned or scaled), and where it then overlapped a neighbour by up to 10% it was trimmed to the neighbour's wall (914, the party walls of hand pass 2). Where a set-back would not fit (between two roads, or onto a neighbour by more than 10%), the house's road side was cut back to the road edge if 70% of it stayed (377 houses); 70 houses that kept less were left out, the frontage beside them already holding its houses. 2,301 set back, 377 cut, 70 left out, three clipped to the district line: 4,275 houses (was 4,345), 52.7 ha of footprint (was 53.7). After: no house more than 1 m2 inside a carriageway, no two houses overlapping by more than 0.5 m2; Ladipo's lane rd-ua9h579y (8 m, 47 houses on it) and the local main rd-zvenwhp0 (16 m, 29) checked by eye on a before/after picture: the fronts now line the road edges, wall to wall, with a few notched corners where a trim met a neighbour.

## Storeys from neighbours (25 Oct): the 787 houses 2.5D could not read

`scripts/draft_storeys_nearby.py` gave the 787 houses left without storeys (316 whose source was not found again, 471 whose source has no built pixels in 2.5D) the median storeys of the houses within 30 m that have storeys, and one storey under 25 m2: 148 at 1, 598 at 2, 34 at 3, 7 at 4. The industry's way, in its simplest form: missing building heights are estimated from each building's surroundings (Bernard et al., Geoscientific Model Development 15, 7505, 2022). Ten of the 257 over 40 m2 with a known source were sampled for Street View; only four have a pano (the rest stand inside their blocks). By eye: b-60e803a3 on Ogunjobi Street, drafted 1, is 2 storeys, and b-fce1fb5a off Fatai Atere Way, drafted 4, is a low shed beside a factory, 1: both fixed by hand. b-6ccde230 on Kumuyi Street is hidden behind a 2-storey house (drafted 2), and b-0a5d903f's source lies on Shasere Ajibade Street's gate among 4-storey estate blocks (drafted 3): not judged. So the neighbours' median is rough: two of the two judged were wrong. These houses are mostly inside blocks, behind the street fronts; they are for the block-by-block pass by eye. Kind and look then drafted by the rules: 787 and 787. Every house in Mùṣá now has all nine building fields.

## Hand pass 42 (25 Oct): the 35 houses read at 5+ storeys, checked in Street View

Each house's real source (found again by shape, as in `draft_storeys.py`) was looked at in Street View from the nearest pano, turned to face it. At all 15 places seen (by eye), the real buildings stand 1 to 4 storeys where 2.5D read 13.5 to 20.5 m: Wey Street 3 (b-4ec784a4, b-a95f6be4), 95 Ikorodu Road 3 (b-1e8bce96, b-b4d9281c; b-d3c74077 on the same row, no pano, 3), the glass office on Ladipo Street 3 (b-26e696ab, b-a3af8ba5), Ogunjobi Street 2 (b-b694a506), behind the Apapa-Oshodi Expressway 3 (b-7023889b), Omotayo Street 3 (b-10893840), Adeyemi Street 3 (b-2ee0d280), Isolo Road 3 (b-20ed1b22), a lane in Mushin town, its pano unnamed, 2 (b-ac560e2e, b-ec05ab45), a factory's office 2 (b-4814c874, b-e6cddef0), Olanibi Street 4 (b-cc8cd7de), Ojerinde Street 2 (b-ed4c55c7), Fagbile Street 4 (b-af4d738f), Fashoro Street 3 (b-6aca0b33), a hut against LUTH's wall 1 (b-b2c923f0). Not seen, set by what stands around them: the expressway roadside, hidden by trees and parked containers, 2 (b-a5206e7c, b-32be2bf0, b-0b55cfda, b-c3ac3e7a); LUTH's blocks 4 (b-04735228, b-cdc27cce: a 4-storey ward block was seen from Ishaga Road); b-d2b2155c 3; north of Ladipo Street 2 (b-54be215f). Five are pieces of big warehouse halls on Jimade Street and north of Ladipo Street (sources of 700 to 13,000 m2, cut to their Gidi blocks; satellite z18): 1 storey, kind shed, workshop (b-f23a0c0e, b-9382a7c9, b-07549b97, b-a467b536, b-104fa257); b-ded1ce51 (1,384 m2 off the expressway) 1 storey, a shed by the rules. Kind and look then drafted by the rules. So 2.5D over-reads these spots (read 13.5-20.5 m, seen 1-4 storeys): the 86 houses read at 4 storeys may hold some over-reads too, for a later sample. LUTH's two blocks were drafted shop-under-flats by the street rule: they are hospital, for the per-building pass with the schools.

## Looks draft (25 Oct): storey heights, roof, walls, windows, stair and wear by house type

`scripts/draft_looks.py` gave the same 3,523 houses their look from their kind, by shares read in the old-town Street View study (`~/gidi-data/research/google/kits/old-town/KIT.md`, 199 shots, about 32 in Mushin: sections 1 "House types" and 11 "Colour palette"), each house seeded by its own id so a re-run gives the same draft. Roofs: 2,085 rusty zinc (1,668 hip, 112 gable, 305 mono on shacks and kiosks), 910 painted long-span, 251 silver zinc, 249 flat slabs with a parapet (3+ storeys), 25 tile, 3 silver long-span sheds. Walls: 2,886 render (1,086 with a darker base band), 405 bare block, 128 brick tile, 104 stone tile. Windows: 1,673 glass louvre, 759 timber louvre, 574 casement, 517 plank shutter. Outside stairs: 136 concrete and 52 steel on the front. A roof-colour map over x 12270-12500, y 6040-6230 (B30 and around) was looked at by eye against the z18 shot of B30: mostly rusty brown with grey, a few blue, green and beige long-span sheets, as in the shot; the share of coloured long-span may be high there, for the hand pass. Not checked: any house in 3D (the builder in gidi-game reads these fields; no build was run), or each house against its own roof in the shots.

## Kinds draft (25 Oct): kind and ground floor from size, storeys and street

`scripts/draft_kinds.py` gave the 3,523 houses with storeys a kind and ground floor from their footprint, storeys and the street they face (a road edge within 3 m; busy: market, main, trunk, local main and service roads): 1,533 compound houses, 626 shop-under-flats with lock-ups, 729 bungalows (161 with lock-ups on a busy street), 326 walk-ups, 245 shacks, 60 kiosk rows, 4 sheds; 154 face no street. A map of ground floors over x 12300-12700, y 5950-6350 was looked at by eye: lock-ups line the busy roads, homes fill the lanes; some front houses on a busy road stand just over 3 m back and stay homes, for the hand pass. Schools, churches, mosques and markets (B28 and B29's school grounds, B27's factory) are not guessed: they are set by hand. The 822 houses without storeys have no kind yet.

## Storeys draft (25 Oct): storeys from each house's real source

`scripts/draft_storeys.py` found each house's real source footprint again by its shape (2,664 exact, 1,058 cut to a party wall, 307 also nudged off a road; 316 not found) and read the source's height from Google Open Buildings 2.5D 2023 (median of its built pixels). 3,558 sources have 2.5D pixels; read as storeys at about 3 m each: 818 at 1, 2,197 at 2, 422 at 3, 86 at 4, 26 at 5, 5 at 6, 4 at 7. The 3,523 at 1 to 4 storeys were written. Checked in Street View at five sources: 1 storey (a bungalow, and a shed roof on Adeoyo Street), 2 (93 Ayilara Street) and 3 (8 Ilupeju Road) were right; the one at 7 (20 m, on Ikorodu Road) stands among 3-storey blocks. So the 35 houses read at 5 or more are left without storeys for a Street View check by hand: b-04735228, b-07549b97, b-0b55cfda, b-104fa257, b-10893840, b-1e8bce96, b-20ed1b22, b-26e696ab, b-2ee0d280, b-32be2bf0, b-4814c874, b-4ec784a4, b-54be215f, b-6aca0b33, b-7023889b, b-9382a7c9, b-a3af8ba5, b-a467b536, b-a5206e7c, b-a95f6be4, b-ac560e2e, b-af4d738f, b-b2c923f0, b-b4d9281c, b-b694a506, b-c3ac3e7a, b-cc8cd7de, b-cdc27cce, b-d2b2155c, b-d3c74077, b-ded1ce51, b-e6cddef0, b-ec05ab45, b-ed4c55c7, b-f23a0c0e. 822 houses have no storeys yet (35 tall, 316 with no source found, 471 whose source has no 2.5D pixels), for the per-building pass. A nudged house's source is the best corner fit within 25 m and may be a neighbour of the true one; its height is still the street's own.

## Hand pass 41 (25 Oct): the empty small blocks B34, B40 and B41 given houses

B34 (the strip between Ibari road and Olorunsogo Street, north of Fafolu Street), B40 and B41 (wedges between Isolo Road and the streets off it) held no houses; at z18 all three are built up, with no street inside, so their houses were drafted with `--frontage --sizes=12,20000`: B34 11 buildings at 64% cover, B40 2 at 19%, B41 1 at 20%. B32, B37, B38 and B39 stay empty: they are slivers between roads or along the district edge, 3 to 16 m real wide on average.

## Hand pass 40 (25 Oct): blocks B35 and B36 read at close zoom, houses redrafted

B35 is the triangle of Oluwole Street, Ladipo Street and Ibari road; B36 lies between Ibari road and Olumorokun Street, from Ayantuga Street to Post Office Road. Neither has a street inside (read at z18), so no lanes were drawn; their houses were cleared and redrafted with `--frontage --sizes=12,20000`. B35 now holds 7 buildings at 53% cover (was 1 at 13%), B36 5 at 56% (was 3 at 28%).

## Hand pass 39 (25 Oct): block B33 read at close zoom, houses redrafted

B33 lies between Olateju Street and the railway, north of Ogunmokun Street (read at z18). Ogidan Street runs through it about 45 m from Olateju Street, too close to keep, so no lane was drawn; its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B33 now holds 13 buildings at 61% cover (was 5 at 31%). The real strip along the railway is mostly bare ground: the per-building pass should clear the plots there.

## Hand pass 38 (25 Oct): block B31 read at close zoom, houses redrafted

B31 is the strip between Ibari road and Olorunsogo Street, one plot deep with no street of its own (read at z18), so no lane was drawn; its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B31 now holds 16 buildings at 58% cover (was 3 at 25%).

## Hand pass 37 (25 Oct): block B30 given its street at close zoom

B30 got 1 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B30 now holds 21 buildings at 55% cover (was 6 at 34%).

## Hand pass 36 (24 Oct): block B29 given its street at close zoom

B29 got 1 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B29 now holds 22 buildings at 59% cover (was 4 at 30%). South of Danmegoro Street it is a real school compound: the draft fills it with houses for now; the per-building pass should give those plots the school.

## Hand pass 35 (24 Oct): block B28 given its street at close zoom

B28 got 1 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B28 now holds 22 buildings at 67% cover (was 8 at 28%). Its west half is a real school compound: the draft fills it with houses for now; the per-building pass should give those plots the school.

## Hand pass 34 (24 Oct): block B26 given its street at close zoom

B26 got 1 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B26 now holds 19 buildings at 61% cover (was 5 at 28%).

## Hand pass 33 (24 Oct): block B25 given its streets at close zoom

B25 got 2 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B25 now holds 21 buildings at 53% cover (was 10 at 50%).

## Hand pass 32 (24 Oct): block B24 given its streets at close zoom

B24 got 2 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B24 now holds 28 buildings at 52% cover (was 9 at 29%).

## Hand pass 31 (24 Oct): block B23 given its streets at close zoom

B23 got 1 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B23 now holds 39 buildings at 60% cover (was 12 at 31%).

## Hand pass 30 (24 Oct): block B22 given its streets at close zoom

B22 got 2 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B22 now holds 24 buildings at 56% cover (was 12 at 49%).

## Hand pass 29 (24 Oct): block B21 given its streets at close zoom

B21 got 2 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B21 now holds 39 buildings at 63% cover (was 18 at 46%).

## Hand pass 28 (24 Oct): block B20 given its streets at close zoom

B20 got 3 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B20 now holds 51 buildings at 54% cover (was 16 at 34%).

## Hand pass 27 (24 Oct): block B19 given its streets at close zoom

B19 got 3 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B19 now holds 45 buildings at 53% cover (was 16 at 39%).

## Hand pass 26 (24 Oct): block B18 given its streets at close zoom

B18 got 4 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B18 now holds 56 buildings at 52% cover (was 19 at 37%).

## Hand pass 25 (24 Oct): block B17 given its streets at close zoom

B17 got 2 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B17 now holds 67 buildings at 51% cover (was 25 at 40%).

## Hand pass 24 (24 Oct): block B16 given its streets at close zoom

B16 got 4 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B16 now holds 55 buildings at 53% cover (was 16 at 30%), all in its south part; its thin north strip between the two carriageways (about 1 m wide) has none.

## Hand pass 23 (24 Oct): block B13 given its streets at close zoom

B13 got 5 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B13 now holds 99 buildings at 56% cover (was 34 at 33%).

## Hand pass 22 (24 Oct): block B14 given its streets at close zoom

B14 got 7 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B14 now holds 113 buildings at 53% cover (was 49 at 42%).

## Hand pass 21 (24 Oct): block B15 given its streets at close zoom

B15 got 4 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B15 now holds 77 buildings at 52% cover (was 30 at 31%).

## Hand pass 20 (24 Oct): block B10 given its streets at close zoom

B10 got 9 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B10 now holds 169 buildings at 55% cover (was 56 at 36%).

## Hand pass 19 (24 Oct): block B11 given its streets at close zoom

B11 got 7 of its real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B11 now holds 133 buildings at 55% cover (was 66 at 39%).

## Hand pass 18 (24 Oct): block B8 given its streets at close zoom

B8 got its 15 real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B8 now holds 179 buildings at 52% cover (was 69 at 32%).

## Hand pass 17 (24 Oct): block B6 re-checked at close zoom

B6's middle got its 10 real streets (STREETS.md); its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B6 now holds 284 buildings at 58% cover (was 241 at 59%).

## Hand pass 16 (24 Oct): blocks B7 and B9 re-checked at close zoom

B7's and B9's lanes were redrawn on the real streets' lines (STREETS.md: 17 and 4 streets in place of 5 and 4). Their houses were cleared and redrafted with `--frontage --sizes=12,20000`. B7 now holds 156 buildings at 51% cover (was 116 at 62%); B9 157 at 60% (was 152 at 60%).

## Hand pass 15 (24 Oct): block B5 redone from a close-zoom study

B5's lanes were redrawn on the real streets' lines (STREETS.md: 18 streets in place of the 3 lanes of the first pass). Its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B5 now holds 329 buildings at 53% cover (was 190 at 59%).

## Hand pass 14 (24 Oct): block B4 redone from a close-zoom study

B4's lanes were redrawn on the real streets' lines (STREETS.md: 15 streets in place of the 6 lanes of the first pass). Its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B4 now holds 251 buildings at 52% cover (was 214 at 53%).

## Hand pass 13 (24 Oct): block B3 redone from a close-zoom study

B3's lanes were redrawn on the real streets' lines (STREETS.md: 55 streets in place of the 15 lanes of the first pass). Its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B3 now holds 434 buildings at 49% cover (was 339 at 50%).

## Hand pass 12 (23 Oct): block B2 redone from a close-zoom study

B2's lanes were redrawn on the real streets' lines (STREETS.md: 36 streets in place of the 7 lanes of hand pass 5). Its houses were cleared and redrafted with `--frontage --sizes=12,20000`. B2 now holds 531 buildings at 50% cover (was 367 at 51%).

## Real houses that land on a road (hand pass: move the road, or the house if the road is right)

| block | houses | covered | on a road at (Gidi x, y) |
|---|---|---|---|
| 0 | 220 | 30% | 12730, 6231; 12860, 5921; 12964, 6408; 12722, 6229; 13247, 6192; 12893, 6007 |
| 1 | 130 | 24% | 12394, 5780; 12285, 5313; 12410, 5781; 12267, 5614; 12412, 5778; 12289, 5717 |
| 2 | 147 | 30% | 12524, 6355; 13000, 6451; 12496, 6368; 13036, 6491; 13009, 6467; 12926, 6417 |
| 3 | 147 | 30% | 13300, 6237; 13157, 6032; 13104, 5989; 13345, 6115; 13348, 6063; 13234, 5795; 13175, 6008; 13341, 5913; 13182, 6041; 13126, 5997; 13350, 6106; 13226, 6093; 13347, 6135; 13240, 5780 |
| 4 | 46 | 29% | 12843, 5585; 12568, 5509; 12870, 5531; 12453, 5319 |
| 5 | 111 | 39% | 12486, 6341; 12374, 6163; 12375, 6114; 12301, 6264 |
| 6 | 86 | 29% | 13157, 5724; 13088, 5561; 13179, 5792; 13163, 5733 |
| 7 | 46 | 32% | 12343, 5799 |
| 8 | 67 | 31% | 13018, 6435; 13224, 6455; 13213, 6496; 13070, 6504; 13256, 6355 |
| 9 | 58 | 30% | 12687, 6034 |
| 10 | 53 | 34% | 12769, 5877; 12801, 5909; 12645, 5663; 12730, 5897; 12707, 5887 |
| 11 | 62 | 37% | 12722, 5915; 12587, 5894; 12444, 5811; 12738, 5918; 12595, 5898; 12561, 5899 |
| 12 | 32 | 31% | 12872, 5874; 12896, 5928; 12867, 5845; 12886, 5911; 13044, 5781; 12904, 5936 |
| 13 | 46 | 40% | 12640, 6232; 12609, 6222; 12693, 6220; 12703, 6219; 12628, 6227; 12601, 6215; 12607, 6200 |
| 14 | 30 | 31% |  |
| 15 | 18 | 33% | 12283, 6189; 12218, 6239 |
| 16 | 24 | 39% | 12580, 5868; 12493, 5800; 12573, 5860 |
| 17 | 15 | 30% | 13090, 6012; 13055, 5990; 13069, 5996; 13124, 6042; 13018, 5985 |
| 18 | 15 | 36% | 12999, 5674 |
| 19 | 13 | 22% | 13126, 5748; 13088, 5651; 13085, 5680 |
| 20 | 17 | 43% | 12905, 5626; 12934, 5561 |
| 21 | 12 | 50% |  |
| 22 | 12 | 31% |  |
| 23 | 9 | 29% |  |
| 24 | 7 | 35% | 13007, 5694; 13013, 5709; 13085, 5751 |
| 25 | 5 | 28% | 12211, 6108 |
| 26 | 3 | 50% |  |
| 27 | 8 | 28% |  |
| 28 | 3 | 24% | 13019, 5754 |
| 29 | 5 | 28% | 12348, 6121 |
| 30 | 2 | 12% | 12832, 5721; 12849, 5624; 12837, 5651; 12845, 5626 |
| 31 | 0 | 0% | 12853, 6493; 12979, 6502 |
| 32 | 4 | 23% | 13150, 5794 |
| 33 | 0 | 0% | 12884, 5581; 12904, 5551 |
| 34 | 1 | 13% |  |
| 35 | 3 | 29% |  |
| 36 | 0 | 0% |  |
| 37 | 0 | 0% |  |
| 38 | 0 | 0% | 12709, 6164 |
| 39 | 0 | 0% | 12824, 5933 |
| 40 | 0 | 0% | 12611, 5900; 12615, 5902 |
