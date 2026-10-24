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
