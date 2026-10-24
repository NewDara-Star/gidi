# Which places are alike: numbers for cutting districts

22 Oct 2026. Read-only study. It gives numbers for how many districts, and which places merge. It does not decide.
Builds on `docs/lagos-study/STUDY.md` and `councils.md`, and reuses their 250 m grids.

Pictures: `units.png` (the 81 units), `similarity.png` (every neighbour link, coloured by similarity), `ladder_85.png`, `ladder_75.png`, `ladder_65.png` (the districts at three levels).
Tables: `units.csv` (fingerprints), `pairs.csv` (neighbour pairs), `ladder.csv` (every merge). Scripts, in `scripts/` (they read `~/gidi-data` and the earlier study grids; never committed data): `seeds.py`, `units.py`, `finger.py`, `know.py`, `analyse.py`, `report.py`, `plots.py`.

Marks: [OB] Open Buildings v3 (conf >= 0.65), [H] 2.5D heights 2023, [OV] Overture, [WC] WorldCover, [WP] WorldPop, [K] general knowledge (not measured).

## The short answer

| Similarity threshold | Districts | After folding tiny plain units* |
|---|---|---|
| 90% | 81 | 71 |
| 85% | 78 | 68 |
| 80% | 67 | 57 |
| 75% | 56 | 46 |
| 70% | 48 | 39 |
| **65%** | **36** | **29** |
| **60%** | **28** | **23** |
| 55% | 19 | 15 |
| 50% | 15 | 11 |

\* A tiny plain unit has under 3 km² of built land (under 0.33 km² at 1:3) and no high richness. Examples: UNILAG, Ijora-Badia, Oworonshoki, Isheri-Olowora. Too small to be a district at 1:3; it becomes a place inside its most alike neighbour.

**Recommendation: about 23 to 29 districts.** Three candidates:
1. **23 districts (60%, tiny units folded).** The leanest map that still keeps the stand-out places apart: the Island core, VI, Ikoyi-Obalende, Oshodi, Ikeja's three pieces (GRA, Allen-Computer Village, the industrial estate), Ajegunle, Mile 2, Makoko, the Dangote end. The big belts merge: Alimosho north, Alimosho south with Festac, Ikorodu, east Lekki to Epe, Ojo to Badagry. Closest to the earlier study's 18-20 groups, plus the hero places.
2. **29 districts (65%, tiny units folded).** Splits what 60% lumps but probably should not: Apapa stays apart from Trade Fair-Satellite Town; Alaba stays apart from the Badagry road; Ladipo, Ajao Estate and Gbagada-Maryland stay their own; the north estate belt (Magodo, Omole-Berger) stays with Ketu-Ojota but apart from Gbagada; Badore stays apart. My pick if the budget allows. Each district averages ~3.8 km² of built land at 1:3.
3. **36 districts (65%, nothing folded).** Same as 2, but the small distinct pieces (UNILAG, Ijora Badia, Oworonshoki, Ilupeju, Amukoko, Isheri-Olowora, the Agric-Majidun creek side) stand as their own small districts. Only if the game wants many small hero places.

Below 60% it breaks. At 55% one blob runs from Ketu to Surulere and Ikeja (19 units, 132 km² built), and Ikorodu joins Epe and east Lekki. That is chaining, not likeness.

## How the units were drawn

- **81 units**, from the LCDAs and well-known neighbourhoods [K]. Each has one to four seed points (`seeds.py`).
- **The area is all Lagos land:** every 250 m land cell inside the 20 LGA polygons, with the gaps between the rough polygons filled. 2,947 km² of land, 997 km² built (roof cover >= 10%) [OB]. No gaps, no overlaps. Water cells are left out.
- **Each cell joins the nearest seed by a penalised walk:** one step per cell, +2 to cross a motorway, trunk or primary road cell [OV], +1 to cross rail, +4 to cross an LGA line, 8 per cell across water. So boundaries run along LGA lines, big roads and water where they can. Small stray fragments join the unit they touch most.
- Outer units are big because they hold bush (Epe town-Noforija 319 km² of land, 23 km² built). That is why areas are given twice: land, and built.
- Lagos Island and Eti-Osa LGA lines are rough (STUDY.md limits). Some units carry odd edges: Apapa-Tin Can takes the Lighthouse Beach spit; Lekki FTZ-Dangote sits partly in the Epe polygon.

## The fingerprint

For each unit (full table in Appendix A and `units.csv`):
- **Character mix:** share of the unit's land in each of the 17 classes of STUDY.md [OB][H][OV][WC].
- **Built form, on built cells only:** buildings per km², median roof size, share of roof in buildings >= 1,000 m² (industry), mean height and share at 4+ storeys [H], grid regularity (street and building directions, 1.0 = perfect grid), roof cover.
- **Life:** people per km² of built land [WP], street km per km², share of street that is major (motorway to secondary), Overture places per km² [OV].
- **How built-up:** share of the unit's land that is built.
- **Functions:** markets, hubs (motor parks, interchanges, stations, jetties) and landmarks (campuses, ports, industry, sights), listed by hand per unit [K] (`know.py`), and Overture counts of markets, transit and campuses [OV]. Overture places are noisy (a "Ladipo market" pin in Apapa), so the [K] lists carry more weight.

## Similarity, distinctiveness, richness

- **Similarity % = 100 x (1 - D).** D is half "character mix" and half "built form and life":
  - Character part: the Hellinger distance between the two class mixes, divided by the largest such distance between any two units in Lagos.
  - Built-form part: each of the 12 numbers is standardised across the 81 units (log for densities, people, places; square root for 4+ share; clipped at 3 standard deviations). The part is the root-mean-square difference, divided by the largest such difference between any two units.
  - So 100% = identical; 0% = as unlike as the two most unlike units in Lagos.
- **Neighbours:** units that share an edge on land (179 pairs), or face each other across 750 m of water or less (6 pairs, all round the harbour mouth). 185 pairs in all (Appendix B, `similarity.png`). Median neighbour similarity: 60%. Range: 26% (Bariga-Akoka vs UNILAG) to 86% (Agege vs Orile Agege-Dopemu).
- **Distinctiveness % = 100 - similarity to its most alike neighbour.** High means it is unlike every neighbour. Most distinct: UNILAG 62, Makoko 55, Ijora-Badia 52, Mile 2-Amuwo 48, Agric-Majidun 45, VI 41, Isheri-Olowora 41, Oshodi, Allen-Computer Village and the Ikeja industrial estate 40, Lekki FTZ 39, Isale Eko 39. Least: Agege pair 14, Badagry pair 15, Ipaja-Alagbado 15, Epe pair 15.
- **Richness (0-100):** 40% variety of classes (effective number of built classes), 40% count of [K] markets, hubs and landmarks (log), 20% count of [OV] markets, transit and campuses (log). Richest: Apapa-Tin Can 84, Isale Eko 83, Alaba-Ojo-LASU 82, VI 81, Surulere core 79, Ebute Metta-Oyingbo-Otto-Iddo 77, Ikoyi 72, Kirikiri-Navy Town 71, Ogba-Alausa industrial 70. Richness leans on my [K] lists; treat it as a guide.
- **Stand-out units** (distinctiveness >= 35% or richness >= 70): 24 units, listed per threshold in Appendix D.

## The merge ladder

- Contiguity-constrained, average-linkage merging. At each step, the two touching groups with the highest average similarity (over all their unit pairs) join. Only neighbours can join. 80 steps, from 81 units to 1 (Appendix C, `ladder.csv`).
- Count at a threshold = the number of groups just before the first merge that scores below it.
- First merges (83-86%): the two Agege units; Agbara with Badagry; Ipaja with Alagbado; Epe with Ejinrin; Okokomaiko with Ijanikin; Iyana Ipaja with Abule Egba; Magodo with Ojodu-Berger-Omole. The repeating outer fabric goes first.
- Mid ladder (70-82%): Igando-Idimu-Iba; Ikota-VGC with Ajah; Shomolu with Mushin, then Aguda and Itire (the central dense core); Ketu with Ojota; Lekki Phase 1 with Ikate; Airport with Ikeja Along-Cantonment; Obalende with Ikoyi.
- Late (60-70%): Yaba with Ebute Metta and Surulere (70); the estate belt with Ketu-Ojota (67); Gbagada with Maryland (67), then with Ketu-Ojota-Magodo (61.5); Festac into the Okota-Ikotun group (66); Ilupeju with Ladipo (64); Ajao Estate with the airport (63); Alaba into the Badagry road (62); Apapa with Trade Fair-Kirikiri-Satellite Town (61); Bariga-Akoka into the central core (61). Allen-Computer Village with the Ikeja industrial estate comes just under the line (59.9).
- Last to join anything: Isale Eko with Ikoyi-Obalende-Onikan (58), Oshodi with the airport group (53), VI with the Island (50), Ajegunle (46), Oworonshoki (44), Ikeja GRA (44), Makoko (43), Mile 2 (41), Lekki FTZ (41), Ijora-Badia (37), UNILAG (29), and last of all Ilupeju-Ladipo (29).

### Who stays alone
- At 75%: all 24 stand-out units are still alone.
- At 65%: 19 still alone. Joined by then: Ikoyi (with Obalende, Onikan), Surulere core and Ebute Metta (with Yaba), Kirikiri (with Satellite Town, Trade Fair), Ogijo (into Ikorodu).
- At 60%: 14 still alone: Isale Eko, VI, Lekki FTZ, Agric-Majidun, Isheri-Olowora, UNILAG, Makoko, Oshodi, Ijora-Badia, Ajegunle, Mile 2, Ikeja GRA, Allen-Computer Village, Ikeja industrial estate. Apapa and Alaba have merged by then.

## How sure: the weight test

The half-and-half weight is a choice. With 30% on character mix (70% on built form), or 70% on character mix:

| Threshold | 30 / 70 | 50 / 50 (used) | 70 / 30 |
|---|---|---|---|
| 75% | 52 | 56 | 60 |
| 70% | 39 | 48 | 53 |
| 65% | 27 | 36 | 43 |
| 60% | 21 | 28 | 36 |
| 55% | 17 | 19 | 21 |

The order of merges changes little; the threshold shifts. Read the threshold as soft. The candidate counts (23-29 folded) hold within this band.

## Sizes at 1:3

All 81 units: 997 km² built, so **~111 km² built at 1:3** (the continuous metro alone is 82 km², STUDY.md). At 60%, the five big belts take 66% of that: Ikorodu 19.6 km² at 1:3, east Lekki-Epe 14.2, Ojo-Badagry 13.4, Alimosho north and Agege 13.2, Alimosho south with Festac 12.5. These are the stretches to squeeze. The stand-out places are small: Isale Eko 0.3 km², VI 0.5, Oshodi 0.6, Ajegunle 0.6, Makoko 0.4 at 1:3 (built). Uneven shrink (STUDY.md) matters more than the count.

## Uncertain: a Google Earth look would decide

Data limits first, then close calls.
1. **Isale Eko-Idumota-Marina, Mushin, VI.** Joined roofs merge in [OB], so density and roof size are wrong. VI also reads 48% "open": the Eko Atlantic fill counts as bush. Its distinctiveness is likely right; its numbers are not.
2. **Ikoyi-Banana Island with Obalende and Onikan (merge at 69-71%).** Villas and towers vs a motor park and old town. The data says alike; the street says not. Look at Obalende.
3. **Makoko-Iwaya.** Stilts over water are partly missing and heights are off (STUDY.md). Its own district or a part of Ebute Metta?
4. **Festac into the Okota-Ikotun group (66%).** A planned 1977 estate merging with sprawl because both read "grid". Look at Festac vs Ikotun and Igando street grain.
5. **Magodo and Omole (Ojodu-Berger) merge at 83%, then with Ketu-Ojota at 67%.** Bent planned estates read as organic, so they look like Ketu. Look at the gates and walls.
6. **Gbagada with Maryland (67%), then with Ketu-Ojota-Magodo (61.5%).** An estate town, a flyover junction and a market belt. Probably three different things.
7. **Apapa-Tin Can with Kirikiri, Satellite Town, Trade Fair (61%).** Port vs estates. Kirikiri's tank farms may belong with Apapa; Satellite Town with Festac.
8. **Alaba-Ojo-LASU into the Badagry road (62%).** The market and the barracks vs a bungalow corridor.
9. **Ilupeju and Papa Ajao-Ladipo (64%).** Factories vs the auto-parts market. Together or into Mushin and Isolo?
10. **Ajao Estate with the airport (63%).** An estate by the fence; or part of Oshodi-Isolo?
11. **Bariga-Akoka into the central core (61%).** The lagoon edge and Ilaje waterfront vs Mushin's grain.
12. **Agric-Majidun-Ogolonto and Isheri-Olowora.** Mostly creek and swamp. Fold into Ikorodu and Ketu, or keep as a creek district?
13. **Badore with east Lekki (61%).** A lagoon-side town; or part of Ajah?
14. **Ijora-Badia.** Fold into Apapa, Ebute Metta or Iganmu? Lowest similarity to all three.

## Limits

- Units come from seed points [K]. Moving a seed moves a boundary by up to ~1 km. Unit lines are not LCDA lines.
- Median roof size counts every roof, so outbuildings pull it down (Ikoyi reads 84 m²).
- The 750 m water rule leaves out the long bridges (Third Mainland, Carter). Those places only meet through land chains.
- Richness uses my hand lists [K]. A unit I know less about scores lower.
- Average linkage is one choice. Single linkage chains even more; complete linkage keeps more small districts.

## Appendix A. Unit fingerprints

Full numbers, all 17 class shares and the knowledge lists: `units.csv`. Here: the main columns. Densities are per km² of built cells (roof cover >= 10%). Classes: the three biggest shares of the unit's land.

| # | Unit | LGA | Land km² | Built km² | Bldg/km² | Median roof m² | Big-roof % | Height m | 4+ % | Grid | People/km² | Street km/km² | Major % | Top classes | Markets K/OV | Hubs K/OV | Landmarks K | Rich | Distinct % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Isale Eko-Idumota-Marina | Lagos Island | 3 | 2.7 | 2552 | 96 | 8 | 9.1 | 17 | 0.38 | 15857 | 25.6 | 34 | bungalow belt 33, dense core 30, towers 19 | 6/13 | 5/4 | 8 | 83 | 38 |
| 2 | Onikan-Lafiaji (Lagos Island East) | Lagos Island | 2 | 1.0 | 1679 | 109 | 12 | 8.4 | 18 | 0.54 | 11679 | 20.7 | 28 | bungalow belt 35, towers 23, scattered 23 | 1/0 | 0/2 | 5 | 54 | 31 |
| 3 | Obalende | Lagos Island | 2 | 1.4 | 1722 | 84 | 14 | 7.7 | 15 | 0.46 | 11059 | 21.7 | 46 | bungalow belt 59, villa/estate 17, towers 14 | 1/3 | 2/1 | 2 | 54 | 29 |
| 4 | Ikoyi-Banana Island | Eti Osa | 17 | 13.0 | 1495 | 84 | 7 | 8.4 | 14 | 0.58 | 7440 | 15.7 | 22 | bungalow belt 37, towers 27, villa/estate 15 | 1/3 | 2/2 | 7 | 72 | 29 |
| 5 | Victoria Island | Eti Osa | 12 | 4.9 | 1458 | 102 | 13 | 9.6 | 18 | 0.76 | 5836 | 16.8 | 31 | open 48, towers 20, grid 9 | 2/2 | 3/0 | 8 | 81 | 41 |
| 6 | Oniru-Lekki Phase 1 | Eti Osa | 15 | 13.1 | 1784 | 79 | 7 | 7.0 | 9 | 0.83 | 4977 | 17.6 | 19 | grid 64, villa/estate 11, bungalow belt 10 | 1/5 | 2/0 | 5 | 61 | 24 |
| 7 | Ikate-Agungi-Osapa-Jakande | Eti Osa | 24 | 15.9 | 1921 | 80 | 5 | 6.5 | 8 | 0.83 | 3752 | 18.3 | 10 | grid 42, open 15, villa/estate 12 | 1/3 | 1/2 | 5 | 65 | 22 |
| 8 | Ikota-VGC-Chevron | Eti Osa | 20 | 14.0 | 1841 | 76 | 5 | 6.1 | 5 | 0.78 | 3154 | 15.2 | 12 | grid 40, villa/estate 19, bungalow belt 17 | 1/1 | 1/2 | 4 | 59 | 19 |
| 9 | Ajah-Abraham Adesanya | Eti Osa | 42 | 24.0 | 1676 | 67 | 4 | 5.2 | 2 | 0.74 | 2768 | 14.5 | 11 | grid 26, scattered 22, bungalow belt 20 | 2/2 | 2/2 | 3 | 63 | 19 |
| 10 | Badore | Eti Osa | 19 | 11.9 | 1951 | 86 | 1 | 5.4 | 2 | 0.53 | 3952 | 13.4 | 8 | bungalow belt 56, open 19, scattered 9 | 1/1 | 1/0 | 2 | 40 | 29 |
| 11 | Sangotedo | Eti Osa | 40 | 12.1 | 1636 | 90 | 2 | 4.9 | 2 | 0.67 | 2534 | 14.4 | 12 | open 35, scattered 20, bungalow belt 14 | 1/2 | 1/0 | 3 | 53 | 20 |
| 12 | Awoyaya-Lakowe | Ibeju Lekki | 190 | 29.3 | 1828 | 77 | 4 | 4.5 | 1 | 0.64 | 1897 | 13.4 | 13 | open 66, scattered 9, bungalow belt 9 | 1/2 | 1/0 | 4 | 53 | 20 |
| 13 | Eleko-Akodo-Ibeju | Ibeju Lekki | 211 | 18.1 | 1680 | 72 | 8 | 4.6 | 3 | 0.71 | 2335 | 9.5 | 24 | open 80, scattered 11 | 1/0 | 1/0 | 4 | 46 | 21 |
| 14 | Lekki FTZ-Dangote | Epe | 268 | 10.6 | 1164 | 62 | 26 | 7.6 | 24 | 0.78 | 2454 | 7.4 | 15 | open 74, swamp 13, scattered 9 | 0/0 | 1/0 | 4 | 46 | 39 |
| 15 | Epe town-Noforija | Epe | 319 | 23.4 | 1609 | 90 | 4 | 4.1 | 1 | 0.56 | 3966 | 11.2 | 19 | open 80, scattered 8 | 2/2 | 2/0 | 3 | 54 | 15 |
| 16 | Ejinrin-Agbowa | Epe | 280 | 5.9 | 1318 | 94 | 5 | 3.8 | 1 | 0.48 | 3772 | 8.9 | 23 | open 90, scattered 6 | 1/0 | 1/0 | 2 | 33 | 15 |
| 17 | Ikorodu town | Ìkòròdú | 35 | 29.6 | 2314 | 80 | 2 | 4.5 | 0 | 0.56 | 3878 | 15.0 | 10 | bungalow belt 63, grid 18, dense sprawl 11 | 2/4 | 3/4 | 3 | 62 | 20 |
| 18 | Agric-Majidun-Ogolonto | Ìkòròdú | 20 | 2.8 | 1949 | 74 | 8 | 5.0 | 4 | 0.49 | 10313 | 12.1 | 39 | swamp 59, open 15, scattered 13 | 1/0 | 2/1 | 1 | 41 | 45 |
| 19 | Isawo-Owutu-Odogunyan | Ìkòròdú | 42 | 30.5 | 2458 | 86 | 0 | 4.4 | 0 | 0.58 | 4013 | 14.1 | 4 | bungalow belt 49, grid 17, dense sprawl 14 | 1/0 | 2/0 | 2 | 52 | 20 |
| 20 | Ogijo-Sagamu Rd | Ìkòròdú | 34 | 22.8 | 1938 | 78 | 14 | 5.4 | 11 | 0.58 | 2954 | 13.3 | 1 | bungalow belt 38, scattered 19, grid 17 | 1/0 | 1/0 | 2 | 49 | 35 |
| 21 | Igbogbo-Baiyeku | Ìkòròdú | 68 | 51.4 | 1917 | 83 | 2 | 4.2 | 1 | 0.56 | 3287 | 13.6 | 4 | bungalow belt 64, grid 16, scattered 15 | 1/0 | 2/0 | 1 | 45 | 19 |
| 22 | Ijede | Ìkòròdú | 72 | 42.5 | 1840 | 82 | 1 | 4.0 | 0 | 0.59 | 3116 | 14.1 | 4 | bungalow belt 44, scattered 18, grid 16 | 1/0 | 1/0 | 2 | 40 | 19 |
| 23 | Imota | Ìkòròdú | 101 | 27.2 | 1705 | 81 | 1 | 3.6 | 0 | 0.57 | 2480 | 13.7 | 4 | open 42, scattered 29, bungalow belt 20 | 1/0 | 0/0 | 2 | 40 | 23 |
| 24 | Ketu-Mile 12-Ikosi | Kosofe | 18 | 11.8 | 2571 | 87 | 2 | 5.2 | 1 | 0.49 | 22173 | 16.1 | 11 | bungalow belt 43, dense core 11, dense sprawl 11 | 2/2 | 3/1 | 1 | 58 | 25 |
| 25 | Ojota-Ogudu | Kosofe | 13 | 7.3 | 2566 | 78 | 4 | 5.8 | 2 | 0.53 | 25128 | 15.6 | 18 | bungalow belt 34, swamp 32, dense core 11 | 2/2 | 3/1 | 2 | 60 | 25 |
| 26 | Magodo | Kosofe | 8 | 7.1 | 2758 | 76 | 1 | 5.8 | 2 | 0.54 | 20612 | 14.5 | 2 | bungalow belt 46, dense core 29, grid 12 | 0/1 | 1/0 | 2 | 49 | 17 |
| 27 | Isheri-Olowora (Ikosi-Isheri) | Kosofe | 10 | 2.4 | 1768 | 76 | 1 | 5.1 | 1 | 0.63 | 15318 | 12.9 | 7 | open 63, bungalow belt 18, scattered 10 | 1/0 | 1/0 | 2 | 39 | 41 |
| 28 | Gbagada | Kosofe | 7 | 6.8 | 2428 | 83 | 5 | 6.1 | 4 | 0.57 | 30468 | 16.6 | 16 | bungalow belt 56, dense core 15, grid 15 | 1/0 | 2/2 | 2 | 54 | 33 |
| 29 | Oworonshoki | Kosofe | 8 | 2.9 | 3779 | 62 | 1 | 5.2 | 1 | 0.46 | 23956 | 15.4 | 14 | swamp 46, dense sprawl 17, stilts 11 | 1/0 | 2/0 | 1 | 49 | 35 |
| 30 | Shomolu-Pedro-Onipanu | Shomolu | 7 | 7.1 | 3261 | 103 | 3 | 5.8 | 3 | 0.52 | 35293 | 18.5 | 10 | dense core 63, bungalow belt 12, grid 9 | 2/4 | 3/1 | 1 | 59 | 18 |
| 31 | Bariga-Akoka | Shomolu | 5 | 4.8 | 3483 | 84 | 2 | 5.4 | 1 | 0.44 | 27122 | 18.2 | 14 | dense sprawl 40, dense core 24, bungalow belt 19 | 2/1 | 2/2 | 3 | 66 | 33 |
| 32 | UNILAG | Shomolu | 2 | 1.0 | 1180 | 63 | 21 | 6.9 | 14 | 0.49 | 18262 | 11.5 | 15 | campus 86, bungalow belt 7 | 0/0 | 2/0 | 1 | 41 | 62 |
| 33 | Yaba-Sabo-Jibowu | Shomolu | 5 | 5.1 | 2216 | 86 | 6 | 6.0 | 5 | 0.55 | 20309 | 18.5 | 16 | bungalow belt 61, grid 14, dense core 13 | 3/1 | 3/0 | 3 | 64 | 31 |
| 34 | Ebute Metta-Oyingbo-Otto-Iddo | Lagos Mainland | 6 | 4.7 | 2494 | 86 | 7 | 6.3 | 5 | 0.55 | 22800 | 16.3 | 24 | bungalow belt 40, grid 15, dense core 14 | 2/7 | 4/2 | 3 | 77 | 30 |
| 35 | Makoko-Iwaya | Lagos Mainland | 4 | 3.9 | 4979 | 44 | 2 | 6.5 | 9 | 0.51 | 17032 | 12.3 | 11 | dense core 31, stilts 27, grid 18 | 2/2 | 1/0 | 2 | 60 | 55 |
| 36 | Surulere (Ojuelegba-Bode Thomas-Stadium) | Surulere | 10 | 9.2 | 2450 | 88 | 12 | 6.6 | 10 | 0.51 | 25126 | 18.5 | 19 | bungalow belt 33, dense core 22, industry 17 | 2/6 | 2/8 | 4 | 79 | 29 |
| 37 | Aguda-Ijesha-Coker | Surulere | 11 | 10.6 | 2812 | 109 | 8 | 6.4 | 6 | 0.51 | 33299 | 17.3 | 15 | dense core 57, bungalow belt 16, industry 14 | 3/5 | 1/2 | 2 | 60 | 24 |
| 38 | Itire-Lawanson | Mushin | 3 | 3.1 | 3402 | 103 | 8 | 5.8 | 5 | 0.54 | 26496 | 19.4 | 19 | dense core 46, dense sprawl 26, grid tenement 20 | 2/1 | 1/1 | 1 | 50 | 22 |
| 39 | Iganmu-Orile | Apapa | 5 | 4.6 | 2795 | 96 | 8 | 6.2 | 6 | 0.59 | 24878 | 16.2 | 29 | dense core 35, bungalow belt 21, grid tenement 20 | 1/1 | 2/2 | 3 | 62 | 24 |
| 40 | Mushin-Idi Araba-Odi Olowo | Mushin | 6 | 5.6 | 3229 | 96 | 5 | 6.1 | 4 | 0.48 | 34329 | 19.8 | 20 | dense core 72, bungalow belt 13, dense sprawl 6 | 3/4 | 3/2 | 3 | 60 | 18 |
| 41 | Ilupeju | Mushin | 3 | 2.8 | 2036 | 81 | 33 | 8.5 | 26 | 0.62 | 37500 | 19.6 | 32 | industry 53, dense core 20, bungalow belt 16 | 1/2 | 1/1 | 2 | 51 | 36 |
| 42 | Papa Ajao-Ladipo | Mushin | 3 | 3.2 | 1482 | 80 | 46 | 8.9 | 30 | 0.59 | 50833 | 16.6 | 19 | industry 71, military 16, grid tenement 6 | 1/3 | 2/0 | 1 | 47 | 36 |
| 43 | Oshodi-Mafoluku | Oshodi/Isolo | 6 | 5.8 | 3077 | 94 | 4 | 6.1 | 3 | 0.59 | 64884 | 18.4 | 20 | dense core 46, grid tenement 16, bungalow belt 15 | 3/3 | 3/2 | 1 | 67 | 40 |
| 44 | Ajao Estate | Oshodi/Isolo | 5 | 3.9 | 2119 | 72 | 22 | 7.0 | 11 | 0.60 | 45077 | 14.5 | 12 | bungalow belt 33, industry 26, grid 11 | 0/2 | 1/0 | 2 | 54 | 33 |
| 45 | Isolo | Oshodi/Isolo | 8 | 8.4 | 2615 | 88 | 15 | 6.6 | 10 | 0.55 | 31821 | 17.1 | 16 | dense core 49, industry 21, bungalow belt 16 | 2/1 | 2/1 | 1 | 58 | 26 |
| 46 | Okota-Ago Palace | Oshodi/Isolo | 22 | 20.4 | 2504 | 75 | 2 | 5.6 | 3 | 0.72 | 10006 | 15.4 | 8 | grid 49, bungalow belt 29, dense sprawl 10 | 1/2 | 1/0 | 2 | 46 | 22 |
| 47 | Ejigbo | Oshodi/Isolo | 8 | 6.6 | 3591 | 67 | 1 | 5.2 | 1 | 0.58 | 34884 | 15.8 | 9 | dense sprawl 39, bungalow belt 19, grid tenement 14 | 2/1 | 1/0 | 1 | 56 | 20 |
| 48 | Apapa-Tin Can | Apapa | 31 | 13.2 | 1900 | 66 | 20 | 7.2 | 14 | 0.55 | 13060 | 11.9 | 14 | open 29, scattered 17, bungalow belt 15 | 2/4 | 3/3 | 5 | 84 | 32 |
| 49 | Ijora-Badia | Apapa | 3 | 2.2 | 1147 | 80 | 34 | 8.4 | 24 | 0.60 | 16913 | 14.3 | 28 | port 35, industry 31, villa/estate 15 | 1/1 | 2/0 | 2 | 54 | 52 |
| 50 | Ajegunle (Ajeromi) | Ajeromi/Ifelodun | 6 | 5.6 | 2446 | 122 | 10 | 5.7 | 3 | 0.78 | 75830 | 16.0 | 17 | grid tenement 53, grid 13, bungalow belt 6 | 2/5 | 2/0 | 2 | 64 | 37 |
| 51 | Amukoko-Layeni (Ifelodun) | Ajeromi/Ifelodun | 3 | 2.6 | 3441 | 125 | 5 | 5.7 | 2 | 0.60 | 36472 | 16.0 | 7 | dense sprawl 31, grid tenement 31, dense core 29 | 1/3 | 1/0 | 0 | 46 | 37 |
| 52 | Mile 2-Amuwo | Amuwo Odofin | 11 | 10.1 | 1958 | 51 | 23 | 7.2 | 15 | 0.73 | 42104 | 16.0 | 24 | grid 36, bungalow belt 28, industry 28 | 1/0 | 3/3 | 1 | 52 | 48 |
| 53 | Kirikiri-Navy Town | Amuwo Odofin | 31 | 9.1 | 1765 | 66 | 18 | 6.2 | 9 | 0.78 | 8826 | 12.5 | 9 | open 30, swamp 23, military 9 | 0/4 | 1/0 | 4 | 71 | 31 |
| 54 | Festac | Amuwo Odofin | 12 | 8.6 | 2398 | 56 | 3 | 5.1 | 1 | 0.71 | 5029 | 16.8 | 9 | grid 39, bungalow belt 33, scattered 13 | 2/0 | 2/1 | 2 | 52 | 30 |
| 55 | Satellite Town | Amuwo Odofin | 30 | 14.6 | 2068 | 80 | 10 | 5.5 | 4 | 0.81 | 6344 | 14.9 | 6 | grid 28, swamp 20, scattered 18 | 1/2 | 1/0 | 2 | 60 | 31 |
| 56 | Trade Fair-Abule Ado | Ojo | 29 | 12.2 | 1623 | 81 | 11 | 5.4 | 6 | 0.73 | 3948 | 13.5 | 9 | military 27, open 20, grid 20 | 3/4 | 1/2 | 2 | 65 | 34 |
| 57 | Alaba-Ojo-LASU | Ojo | 36 | 11.1 | 2409 | 77 | 5 | 5.3 | 2 | 0.54 | 15330 | 14.6 | 15 | swamp 49, bungalow belt 13, open 8 | 2/5 | 2/0 | 2 | 82 | 28 |
| 58 | Okokomaiko | Ojo | 37 | 15.7 | 2884 | 77 | 1 | 4.6 | 0 | 0.61 | 15440 | 13.4 | 8 | swamp 29, open 22, bungalow belt 19 | 1/0 | 1/0 | 1 | 39 | 16 |
| 59 | Iba | Ojo | 19 | 15.8 | 2682 | 81 | 1 | 4.6 | 0 | 0.58 | 11212 | 14.2 | 3 | bungalow belt 48, dense sprawl 24, grid 18 | 1/0 | 1/0 | 0 | 36 | 19 |
| 60 | Ijanikin-Igbo Elerin | Ojo | 48 | 15.4 | 2493 | 76 | 2 | 4.3 | 1 | 0.59 | 10999 | 12.4 | 8 | open 33, swamp 21, bungalow belt 21 | 1/0 | 1/0 | 2 | 49 | 16 |
| 61 | Agbara-Morogbo | Badagry | 131 | 42.1 | 1893 | 82 | 1 | 3.8 | 0 | 0.59 | 2292 | 10.9 | 6 | open 38, bungalow belt 25, scattered 18 | 1/0 | 1/0 | 2 | 40 | 15 |
| 62 | Badagry town-Seme | Badagry | 243 | 36.6 | 1710 | 78 | 2 | 3.7 | 0 | 0.57 | 2442 | 11.2 | 8 | open 54, scattered 18, swamp 14 | 2/2 | 2/0 | 4 | 53 | 15 |
| 63 | Iyana Ipaja | Alimosho | 7 | 6.8 | 3749 | 59 | 1 | 5.1 | 1 | 0.49 | 20935 | 18.2 | 9 | dense sprawl 70, dense core 19, grid 8 | 1/3 | 2/0 | 1 | 47 | 16 |
| 64 | Ipaja-Ayobo-Mosan | Alimosho | 34 | 31.1 | 3371 | 65 | 1 | 4.5 | 0 | 0.55 | 15408 | 16.5 | 3 | dense sprawl 59, grid 18, bungalow belt 17 | 2/2 | 2/1 | 1 | 54 | 15 |
| 65 | Alagbado-Agbado | Alimosho | 18 | 18.1 | 3666 | 63 | 2 | 4.7 | 0 | 0.52 | 17774 | 16.9 | 5 | dense sprawl 79, bungalow belt 9, grid 7 | 1/0 | 2/0 | 1 | 42 | 15 |
| 66 | Egbeda-Akowonjo | Alimosho | 12 | 11.2 | 3255 | 72 | 2 | 5.5 | 1 | 0.52 | 19339 | 16.9 | 8 | dense core 42, dense sprawl 25, grid 14 | 2/2 | 2/2 | 0 | 59 | 25 |
| 67 | Idimu | Alimosho | 13 | 12.0 | 2980 | 74 | 1 | 4.7 | 0 | 0.58 | 13133 | 16.0 | 3 | bungalow belt 39, dense sprawl 38, grid 19 | 1/1 | 1/0 | 0 | 37 | 16 |
| 68 | Ikotun | Alimosho | 22 | 21.2 | 3197 | 74 | 3 | 5.3 | 1 | 0.68 | 15818 | 15.9 | 6 | grid 33, dense sprawl 31, grid tenement 14 | 1/1 | 1/2 | 0 | 51 | 22 |
| 69 | Igando | Alimosho | 49 | 34.4 | 3090 | 73 | 0 | 4.6 | 0 | 0.61 | 10642 | 15.2 | 4 | dense sprawl 29, grid 22, bungalow belt 22 | 1/1 | 1/0 | 3 | 55 | 19 |
| 70 | Egbe | Alimosho | 8 | 7.8 | 3361 | 67 | 1 | 5.1 | 1 | 0.51 | 29616 | 16.4 | 10 | dense sprawl 63, bungalow belt 19, dense core 11 | 1/0 | 1/1 | 0 | 39 | 20 |
| 71 | Ikeja GRA | Ikeja | 6 | 4.9 | 1755 | 65 | 8 | 6.6 | 8 | 0.73 | 30274 | 14.8 | 10 | grid 47, bungalow belt 28, military 22 | 0/0 | 1/0 | 3 | 47 | 36 |
| 72 | Allen-Opebi-Computer Village | Ikeja | 6 | 5.4 | 2327 | 84 | 10 | 6.6 | 7 | 0.53 | 16455 | 20.0 | 20 | bungalow belt 55, dense core 23, industry 10 | 2/6 | 2/0 | 3 | 64 | 40 |
| 73 | Ogba-Agidingbi-Alausa industrial | Ikeja | 19 | 18.0 | 2146 | 64 | 31 | 7.6 | 19 | 0.55 | 12198 | 17.1 | 13 | industry 47, bungalow belt 20, dense core 14 | 1/4 | 2/2 | 5 | 70 | 40 |
| 74 | Ojodu-Berger-Omole | Ikeja | 7 | 7.0 | 3040 | 74 | 1 | 6.1 | 3 | 0.52 | 14668 | 16.1 | 10 | dense core 42, bungalow belt 36, dense sprawl 11 | 1/2 | 2/1 | 2 | 51 | 17 |
| 75 | Maryland-Onigbongbo | Ikeja | 3 | 2.4 | 2027 | 73 | 13 | 6.9 | 10 | 0.57 | 25939 | 17.1 | 24 | bungalow belt 69, military 21 | 1/0 | 3/0 | 1 | 44 | 33 |
| 76 | Airport (MMIA) | Ikeja | 11 | 3.8 | 2408 | 70 | 14 | 6.4 | 10 | 0.54 | 27996 | 14.8 | 18 | airport 63, bungalow belt 11, dense sprawl 9 | 0/0 | 2/2 | 2 | 45 | 22 |
| 77 | Ikeja Along-Cantonment | Ikeja | 7 | 4.2 | 1884 | 77 | 16 | 6.2 | 6 | 0.57 | 21142 | 17.1 | 18 | airport 38, bungalow belt 16, industry 9 | 1/0 | 1/2 | 2 | 62 | 22 |
| 78 | Agege-Pen Cinema | Agege | 7 | 6.8 | 3790 | 78 | 2 | 5.4 | 1 | 0.46 | 38412 | 18.5 | 17 | dense core 43, dense sprawl 41, bungalow belt 12 | 2/1 | 2/2 | 2 | 57 | 14 |
| 79 | Orile Agege-Dopemu | Agege | 4 | 3.9 | 3666 | 83 | 3 | 5.5 | 2 | 0.47 | 18937 | 18.1 | 16 | dense core 44, dense sprawl 43, grid tenement 8 | 2/2 | 1/2 | 1 | 47 | 14 |
| 80 | Ifako-Ijaiye-Iju | Ifako/Ijaye | 12 | 11.8 | 3148 | 71 | 4 | 5.6 | 3 | 0.50 | 19372 | 16.0 | 9 | dense core 34, dense sprawl 29, bungalow belt 27 | 2/1 | 2/1 | 1 | 56 | 21 |
| 81 | Abule Egba-Ojokoro | Ifako/Ijaye | 14 | 14.4 | 3516 | 64 | 1 | 5.2 | 1 | 0.52 | 31367 | 17.8 | 8 | dense sprawl 60, dense core 18, grid tenement 10 | 1/3 | 2/0 | 2 | 52 | 16 |

## Appendix B. All neighbour pairs, most alike first

Land = the units touch. Water = across 750 m of water or less. Also in `pairs.csv` (with the two parts of the distance).

| Unit A | Unit B | Link | Similarity % |
|---|---|---|---|
| Agege-Pen Cinema | Orile Agege-Dopemu | land | 86 |
| Agbara-Morogbo | Badagry town-Seme | land | 85 |
| Ipaja-Ayobo-Mosan | Alagbado-Agbado | land | 85 |
| Epe town-Noforija | Ejinrin-Agbowa | land | 85 |
| Okokomaiko | Ijanikin-Igbo Elerin | land | 84 |
| Iyana Ipaja | Abule Egba-Ojokoro | land | 84 |
| Ipaja-Ayobo-Mosan | Idimu | land | 84 |
| Magodo | Ojodu-Berger-Omole | land | 83 |
| Alagbado-Agbado | Abule Egba-Ojokoro | land | 82 |
| Shomolu-Pedro-Onipanu | Mushin-Idi Araba-Odi Olowo | land | 82 |
| Iba | Igando | land | 81 |
| Igbogbo-Baiyeku | Ijede | land | 81 |
| Ikota-VGC-Chevron | Ajah-Abraham Adesanya | land | 81 |
| Ikorodu town | Isawo-Owutu-Odogunyan | land | 81 |
| Sangotedo | Awoyaya-Lakowe | land | 80 |
| Ejigbo | Egbe | land | 80 |
| Idimu | Igando | land | 80 |
| Eleko-Akodo-Ibeju | Epe town-Noforija | land | 79 |
| Agege-Pen Cinema | Ifako-Ijaiye-Iju | land | 79 |
| Ijanikin-Igbo Elerin | Agbara-Morogbo | land | 79 |
| Okota-Ago Palace | Ikotun | land | 78 |
| Itire-Lawanson | Mushin-Idi Araba-Odi Olowo | land | 78 |
| Airport (MMIA) | Ikeja Along-Cantonment | land | 78 |
| Ikate-Agungi-Osapa-Jakande | Ikota-VGC-Chevron | land | 78 |
| Ifako-Ijaiye-Iju | Abule Egba-Ojokoro | land | 77 |
| Ijede | Imota | land | 77 |
| Awoyaya-Lakowe | Eleko-Akodo-Ibeju | land | 77 |
| Ejigbo | Ikotun | land | 76 |
| Aguda-Ijesha-Coker | Itire-Lawanson | land | 76 |
| Ikorodu town | Igbogbo-Baiyeku | land | 76 |
| Aguda-Ijesha-Coker | Iganmu-Orile | land | 76 |
| Oniru-Lekki Phase 1 | Ikate-Agungi-Osapa-Jakande | land | 75 |
| Egbeda-Akowonjo | Egbe | land | 75 |
| Agege-Pen Cinema | Abule Egba-Ojokoro | land | 75 |
| Ketu-Mile 12-Ikosi | Ojota-Ogudu | land | 75 |
| Mushin-Idi Araba-Odi Olowo | Isolo | land | 74 |
| Iyana Ipaja | Ipaja-Ayobo-Mosan | land | 74 |
| Ipaja-Ayobo-Mosan | Abule Egba-Ojokoro | land | 74 |
| Eleko-Akodo-Ibeju | Ejinrin-Agbowa | land | 74 |
| Idimu | Egbe | land | 74 |
| Iyana Ipaja | Egbeda-Akowonjo | land | 74 |
| Iyana Ipaja | Agege-Pen Cinema | land | 73 |
| Egbeda-Akowonjo | Orile Agege-Dopemu | land | 73 |
| Ajah-Abraham Adesanya | Sangotedo | land | 73 |
| Alaba-Ojo-LASU | Okokomaiko | land | 72 |
| Badore | Sangotedo | land | 71 |
| Ketu-Mile 12-Ikosi | Magodo | land | 71 |
| Obalende | Ikoyi-Banana Island | land | 71 |
| Idimu | Ikotun | land | 71 |
| Surulere (Ojuelegba-Bode Thomas-Stadium) | Iganmu-Orile | land | 71 |
| Surulere (Ojuelegba-Bode Thomas-Stadium) | Aguda-Ijesha-Coker | land | 71 |
| Okota-Ago Palace | Festac | land | 71 |
| Ikotun | Egbe | land | 70 |
| Ebute Metta-Oyingbo-Otto-Iddo | Surulere (Ojuelegba-Bode Thomas-Stadium) | land | 70 |
| Awoyaya-Lakowe | Ejinrin-Agbowa | land | 70 |
| Onikan-Lafiaji (Lagos Island East) | Obalende | land | 69 |
| Kirikiri-Navy Town | Satellite Town | land | 69 |
| Yaba-Sabo-Jibowu | Surulere (Ojuelegba-Bode Thomas-Stadium) | land | 69 |
| Iyana Ipaja | Orile Agege-Dopemu | land | 69 |
| Ikotun | Igando | land | 69 |
| Apapa-Tin Can | Kirikiri-Navy Town | land | 68 |
| Itire-Lawanson | Isolo | land | 68 |
| Ojota-Ogudu | Gbagada | land | 67 |
| Gbagada | Maryland-Onigbongbo | land | 67 |
| Surulere (Ojuelegba-Bode Thomas-Stadium) | Mushin-Idi Araba-Odi Olowo | land | 67 |
| Ipaja-Ayobo-Mosan | Egbeda-Akowonjo | land | 67 |
| Ajao Estate | Isolo | land | 67 |
| Shomolu-Pedro-Onipanu | Bariga-Akoka | land | 67 |
| Satellite Town | Trade Fair-Abule Ado | land | 66 |
| Okokomaiko | Iba | land | 66 |
| Badore | Awoyaya-Lakowe | land | 66 |
| Okota-Ago Palace | Ejigbo | land | 66 |
| Ojota-Ogudu | Oworonshoki | land | 65 |
| Ikorodu town | Ijede | land | 65 |
| Ajah-Abraham Adesanya | Badore | land | 65 |
| Isawo-Owutu-Odogunyan | Ogijo-Sagamu Rd | land | 65 |
| Gbagada | Shomolu-Pedro-Onipanu | land | 65 |
| Iba | Ijanikin-Igbo Elerin | land | 64 |
| Ikeja GRA | Maryland-Onigbongbo | land | 64 |
| Ilupeju | Papa Ajao-Ladipo | land | 64 |
| Ikorodu town | Ogijo-Sagamu Rd | land | 64 |
| Ajegunle (Ajeromi) | Amukoko-Layeni (Ifelodun) | land | 63 |
| Festac | Satellite Town | land | 63 |
| Iganmu-Orile | Ajegunle (Ajeromi) | land | 62 |
| Surulere (Ojuelegba-Bode Thomas-Stadium) | Itire-Lawanson | land | 62 |
| Egbeda-Akowonjo | Idimu | land | 62 |
| Ogijo-Sagamu Rd | Imota | land | 62 |
| Isale Eko-Idumota-Marina | Onikan-Lafiaji (Lagos Island East) | land | 62 |
| Eleko-Akodo-Ibeju | Lekki FTZ-Dangote | land | 61 |
| Satellite Town | Alaba-Ojo-LASU | land | 61 |
| Ejinrin-Agbowa | Imota | land | 61 |
| Iganmu-Orile | Amukoko-Layeni (Ifelodun) | land | 61 |
| Ajao Estate | Airport (MMIA) | land | 60 |
| Oshodi-Mafoluku | Ajao Estate | land | 60 |
| Allen-Opebi-Computer Village | Ogba-Agidingbi-Alausa industrial | land | 60 |
| Ikoyi-Banana Island | Oniru-Lekki Phase 1 | land | 60 |
| Isawo-Owutu-Odogunyan | Isheri-Olowora (Ikosi-Isheri) | land | 59 |
| Shomolu-Pedro-Onipanu | Yaba-Sabo-Jibowu | land | 59 |
| Lekki FTZ-Dangote | Epe town-Noforija | land | 59 |
| Ikoyi-Banana Island | Victoria Island | land | 59 |
| Festac | Ikotun | land | 58 |
| Festac | Trade Fair-Abule Ado | land | 57 |
| Ketu-Mile 12-Ikosi | Isheri-Olowora (Ikosi-Isheri) | land | 57 |
| Yaba-Sabo-Jibowu | Mushin-Idi Araba-Odi Olowo | land | 57 |
| Bariga-Akoka | Yaba-Sabo-Jibowu | land | 56 |
| Gbagada | Bariga-Akoka | land | 56 |
| Ojota-Ogudu | Maryland-Onigbongbo | land | 56 |
| Agric-Majidun-Ogolonto | Ojota-Ogudu | land | 55 |
| Ogba-Agidingbi-Alausa industrial | Maryland-Onigbongbo | land | 54 |
| Aguda-Ijesha-Coker | Ajegunle (Ajeromi) | land | 54 |
| Papa Ajao-Ladipo | Ajao Estate | land | 53 |
| Allen-Opebi-Computer Village | Ikeja Along-Cantonment | land | 53 |
| Ogba-Agidingbi-Alausa industrial | Ikeja Along-Cantonment | land | 53 |
| Alaba-Ojo-LASU | Iba | land | 52 |
| Trade Fair-Abule Ado | Igando | land | 52 |
| Okota-Ago Palace | Mile 2-Amuwo | land | 52 |
| Ikorodu town | Imota | land | 52 |
| Victoria Island | Oniru-Lekki Phase 1 | land | 52 |
| Oworonshoki | Bariga-Akoka | land | 52 |
| Magodo | Ogba-Agidingbi-Alausa industrial | land | 52 |
| Oshodi-Mafoluku | Ikeja Along-Cantonment | land | 52 |
| Trade Fair-Abule Ado | Iba | land | 52 |
| Ejigbo | Airport (MMIA) | land | 51 |
| Trade Fair-Abule Ado | Alaba-Ojo-LASU | land | 51 |
| Ikeja GRA | Ikeja Along-Cantonment | land | 51 |
| Gbagada | Ilupeju | land | 51 |
| Mile 2-Amuwo | Festac | land | 51 |
| Isolo | Okota-Ago Palace | land | 50 |
| Isale Eko-Idumota-Marina | Ebute Metta-Oyingbo-Otto-Iddo | land | 50 |
| Ilupeju | Maryland-Onigbongbo | land | 50 |
| Ajao Estate | Ejigbo | land | 50 |
| Papa Ajao-Ladipo | Isolo | land | 50 |
| Agric-Majidun-Ogolonto | Ketu-Mile 12-Ikosi | land | 50 |
| Kirikiri-Navy Town | Festac | land | 50 |
| Victoria Island | Apapa-Tin Can | water | 49 |
| Ogba-Agidingbi-Alausa industrial | Ojodu-Berger-Omole | land | 49 |
| Ikeja GRA | Allen-Opebi-Computer Village | land | 48 |
| Ogba-Agidingbi-Alausa industrial | Ifako-Ijaiye-Iju | land | 48 |
| Egbeda-Akowonjo | Ikeja Along-Cantonment | land | 48 |
| Apapa-Tin Can | Ijora-Badia | land | 48 |
| Ilupeju | Oshodi-Mafoluku | land | 47 |
| Oshodi-Mafoluku | Airport (MMIA) | land | 47 |
| Ojota-Ogudu | Ogba-Agidingbi-Alausa industrial | land | 46 |
| Ikeja GRA | Ogba-Agidingbi-Alausa industrial | land | 46 |
| Onikan-Lafiaji (Lagos Island East) | Apapa-Tin Can | water | 46 |
| Egbeda-Akowonjo | Airport (MMIA) | land | 45 |
| Agric-Majidun-Ogolonto | Isheri-Olowora (Ikosi-Isheri) | land | 45 |
| Ebute Metta-Oyingbo-Otto-Iddo | Makoko-Iwaya | land | 45 |
| Magodo | Isheri-Olowora (Ikosi-Isheri) | land | 45 |
| Ogba-Agidingbi-Alausa industrial | Agege-Pen Cinema | land | 43 |
| Obalende | Victoria Island | water | 43 |
| Aguda-Ijesha-Coker | Okota-Ago Palace | land | 43 |
| Mile 2-Amuwo | Kirikiri-Navy Town | land | 43 |
| Trade Fair-Abule Ado | Ikotun | land | 42 |
| Oshodi-Mafoluku | Ikeja GRA | land | 42 |
| Iganmu-Orile | Apapa-Tin Can | land | 42 |
| Ketu-Mile 12-Ikosi | Ogba-Agidingbi-Alausa industrial | land | 42 |
| Agric-Majidun-Ogolonto | Isawo-Owutu-Odogunyan | land | 42 |
| Yaba-Sabo-Jibowu | Makoko-Iwaya | land | 42 |
| Ogba-Agidingbi-Alausa industrial | Orile Agege-Dopemu | land | 42 |
| Shomolu-Pedro-Onipanu | Ilupeju | land | 41 |
| Itire-Lawanson | Okota-Ago Palace | land | 41 |
| Ebute Metta-Oyingbo-Otto-Iddo | Ijora-Badia | land | 41 |
| Gbagada | Oworonshoki | land | 41 |
| Ikeja Along-Cantonment | Orile Agege-Dopemu | land | 41 |
| Makoko-Iwaya | Surulere (Ojuelegba-Bode Thomas-Stadium) | land | 40 |
| Isheri-Olowora (Ikosi-Isheri) | Ojodu-Berger-Omole | land | 39 |
| Surulere (Ojuelegba-Bode Thomas-Stadium) | Ijora-Badia | land | 39 |
| Ilupeju | Ikeja GRA | land | 39 |
| Obalende | Apapa-Tin Can | water | 39 |
| UNILAG | Yaba-Sabo-Jibowu | land | 38 |
| Ajegunle (Ajeromi) | Mile 2-Amuwo | land | 37 |
| Ikorodu town | Agric-Majidun-Ogolonto | land | 37 |
| Papa Ajao-Ladipo | Oshodi-Mafoluku | land | 36 |
| Aguda-Ijesha-Coker | Mile 2-Amuwo | land | 35 |
| Isale Eko-Idumota-Marina | Apapa-Tin Can | water | 34 |
| Iganmu-Orile | Ijora-Badia | land | 34 |
| Mushin-Idi Araba-Odi Olowo | Papa Ajao-Ladipo | land | 32 |
| Apapa-Tin Can | Ajegunle (Ajeromi) | land | 32 |
| UNILAG | Makoko-Iwaya | land | 32 |
| Ajegunle (Ajeromi) | Kirikiri-Navy Town | land | 30 |
| Shomolu-Pedro-Onipanu | Papa Ajao-Ladipo | land | 29 |
| Apapa-Tin Can | Amukoko-Layeni (Ifelodun) | land | 26 |
| Isale Eko-Idumota-Marina | Ijora-Badia | water | 26 |
| Bariga-Akoka | UNILAG | land | 26 |

## Appendix C. The merge ladder, step by step

Each step joins the two touching groups that are most alike on average. Also in `ladder.csv`. A step can score a little higher than the one before it (average linkage does that); the threshold counts stop at the first step below the line.

| Step | Similarity % | Joins | With | Districts after |
|---|---|---|---|---|
| 1 | 86.3 | Agege-Pen Cinema | Orile Agege-Dopemu | 80 |
| 2 | 85.2 | Agbara-Morogbo | Badagry town-Seme | 79 |
| 3 | 85.1 | Ipaja-Ayobo-Mosan | Alagbado-Agbado | 78 |
| 4 | 84.6 | Epe town-Noforija | Ejinrin-Agbowa | 77 |
| 5 | 84.2 | Okokomaiko | Ijanikin-Igbo Elerin | 76 |
| 6 | 83.9 | Iyana Ipaja | Abule Egba-Ojokoro | 75 |
| 7 | 82.8 | Magodo | Ojodu-Berger-Omole | 74 |
| 8 | 81.6 | Shomolu-Pedro-Onipanu | Mushin-Idi Araba-Odi Olowo | 73 |
| 9 | 81.2 | Iba | Igando | 72 |
| 10 | 82.2 | Idimu | Iba + Igando | 71 |
| 11 | 81.0 | Igbogbo-Baiyeku | Ijede | 70 |
| 12 | 80.6 | Ikota-VGC-Chevron | Ajah-Abraham Adesanya | 69 |
| 13 | 80.5 | Ikorodu town | Isawo-Owutu-Odogunyan | 68 |
| 14 | 80.0 | Sangotedo | Awoyaya-Lakowe | 67 |
| 15 | 79.9 | Ejigbo | Egbe | 66 |
| 16 | 78.3 | Okota-Ago Palace | Ikotun | 65 |
| 17 | 78.2 | Ipaja-Ayobo-Mosan + Alagbado-Agbado | Iyana Ipaja + Abule Egba-Ojokoro | 64 |
| 18 | 77.7 | Airport (MMIA) | Ikeja Along-Cantonment | 63 |
| 19 | 76.4 | Eleko-Akodo-Ibeju | Epe town-Noforija + Ejinrin-Agbowa | 62 |
| 20 | 76.3 | Aguda-Ijesha-Coker | Itire-Lawanson | 61 |
| 21 | 78.7 | Shomolu-Pedro-Onipanu + Mushin-Idi Araba-Odi Olowo | Aguda-Ijesha-Coker + Itire-Lawanson | 60 |
| 22 | 76.3 | Ifako-Ijaiye-Iju | Agege-Pen Cinema + Orile Agege-Dopemu | 59 |
| 23 | 76.6 | Egbeda-Akowonjo | Ifako-Ijaiye-Iju + Agege-Pen Cinema + Orile Agege-Dopemu | 58 |
| 24 | 75.5 | Oniru-Lekki Phase 1 | Ikate-Agungi-Osapa-Jakande | 57 |
| 25 | 75.2 | Ketu-Mile 12-Ikosi | Ojota-Ogudu | 56 |
| 26 | 74.5 | Isolo | Shomolu-Pedro-Onipanu + Mushin-Idi Araba-Odi Olowo + Aguda-Ijesha-Coker + Itire-Lawanson | 55 |
| 27 | 73.5 | Igbogbo-Baiyeku + Ijede | Ikorodu town + Isawo-Owutu-Odogunyan | 54 |
| 28 | 73.3 | Iganmu-Orile | Isolo + 4 more | 53 |
| 29 | 73.0 | Ejigbo + Egbe | Egbeda-Akowonjo + Ifako-Ijaiye-Iju + Agege-Pen Cinema + Orile Agege-Dopemu | 52 |
| 30 | 72.6 | Ipaja-Ayobo-Mosan + Alagbado-Agbado + Iyana Ipaja + Abule Egba-Ojokoro | Ejigbo + 5 more | 51 |
| 31 | 71.1 | Obalende | Ikoyi-Banana Island | 50 |
| 32 | 70.9 | Ikota-VGC-Chevron + Ajah-Abraham Adesanya | Oniru-Lekki Phase 1 + Ikate-Agungi-Osapa-Jakande | 49 |
| 33 | 70.8 | Agbara-Morogbo + Badagry town-Seme | Okokomaiko + Ijanikin-Igbo Elerin | 48 |
| 34 | 69.9 | Sangotedo + Awoyaya-Lakowe | Eleko-Akodo-Ibeju + Epe town-Noforija + Ejinrin-Agbowa | 47 |
| 35 | 69.6 | Ebute Metta-Oyingbo-Otto-Iddo | Surulere (Ojuelegba-Bode Thomas-Stadium) | 46 |
| 36 | 70.1 | Yaba-Sabo-Jibowu | Ebute Metta-Oyingbo-Otto-Iddo + Surulere (Ojuelegba-Bode Thomas-Stadium) | 45 |
| 37 | 69.4 | Onikan-Lafiaji (Lagos Island East) | Obalende + Ikoyi-Banana Island | 44 |
| 38 | 69.3 | Imota | Sangotedo + Awoyaya-Lakowe + Eleko-Akodo-Ibeju + Epe town-Noforija + Ejinrin-Agbowa | 43 |
| 39 | 69.2 | Kirikiri-Navy Town | Satellite Town | 42 |
| 40 | 68.8 | Idimu + Iba + Igando | Okota-Ago Palace + Ikotun | 41 |
| 41 | 67.2 | Trade Fair-Abule Ado | Kirikiri-Navy Town + Satellite Town | 40 |
| 42 | 67.2 | Gbagada | Maryland-Onigbongbo | 39 |
| 43 | 67.0 | Ogijo-Sagamu Rd | Igbogbo-Baiyeku + Ijede + Ikorodu town + Isawo-Owutu-Odogunyan | 38 |
| 44 | 66.7 | Magodo + Ojodu-Berger-Omole | Ketu-Mile 12-Ikosi + Ojota-Ogudu | 37 |
| 45 | 66.1 | Festac | Idimu + Iba + Igando + Okota-Ago Palace + Ikotun | 36 |
| 46 | 64.3 | Amukoko-Layeni (Ifelodun) | Iganmu-Orile + 5 more | 35 |
| 47 | 63.6 | Ilupeju | Papa Ajao-Ladipo | 34 |
| 48 | 63.1 | Ajao Estate | Airport (MMIA) + Ikeja Along-Cantonment | 33 |
| 49 | 62.4 | Alaba-Ojo-LASU | Agbara-Morogbo + Badagry town-Seme + Okokomaiko + Ijanikin-Igbo Elerin | 32 |
| 50 | 61.5 | Gbagada + Maryland-Onigbongbo | Magodo + Ojodu-Berger-Omole + Ketu-Mile 12-Ikosi + Ojota-Ogudu | 31 |
| 51 | 61.4 | Apapa-Tin Can | Trade Fair-Abule Ado + Kirikiri-Navy Town + Satellite Town | 30 |
| 52 | 60.8 | Badore | Imota + 5 more | 29 |
| 53 | 60.8 | Bariga-Akoka | Amukoko-Layeni (Ifelodun) + 6 more | 28 |
| 54 | 59.9 | Allen-Opebi-Computer Village | Ogba-Agidingbi-Alausa industrial | 27 |
| 55 | 59.6 | Ipaja-Ayobo-Mosan + 9 more | Festac + Idimu + Iba + Igando + Okota-Ago Palace + Ikotun | 26 |
| 56 | 59.3 | Yaba-Sabo-Jibowu + 2 more | Bariga-Akoka + 7 more | 25 |
| 57 | 59.0 | Gbagada + 5 more | Yaba-Sabo-Jibowu + 10 more | 24 |
| 58 | 57.5 | Isale Eko-Idumota-Marina | Onikan-Lafiaji (Lagos Island East) + Obalende + Ikoyi-Banana Island | 23 |
| 59 | 57.4 | Isheri-Olowora (Ikosi-Isheri) | Ogijo-Sagamu Rd + Igbogbo-Baiyeku + Ijede + Ikorodu town + Isawo-Owutu-Odogunyan | 22 |
| 60 | 57.8 | Badore + 6 more | Isheri-Olowora (Ikosi-Isheri) + 5 more | 21 |
| 61 | 57.2 | Allen-Opebi-Computer Village + Ogba-Agidingbi-Alausa industrial | Gbagada + 16 more | 20 |
| 62 | 56.6 | Alaba-Ojo-LASU + Agbara-Morogbo + Badagry town-Seme + Okokomaiko + Ijanikin-Igbo Elerin | Apapa-Tin Can + Trade Fair-Abule Ado + Kirikiri-Navy Town + Satellite Town | 19 |
| 63 | 53.3 | Ipaja-Ayobo-Mosan + 15 more | Allen-Opebi-Computer Village + 18 more | 18 |
| 64 | 52.9 | Oshodi-Mafoluku | Ajao Estate + Airport (MMIA) + Ikeja Along-Cantonment | 17 |
| 65 | 50.5 | Ikota-VGC-Chevron + 3 more | Badore + 12 more | 16 |
| 66 | 50.0 | Ipaja-Ayobo-Mosan + 34 more | Oshodi-Mafoluku + Ajao Estate + Airport (MMIA) + Ikeja Along-Cantonment | 15 |
| 67 | 49.8 | Victoria Island | Isale Eko-Idumota-Marina + 3 more | 14 |
| 68 | 45.5 | Ajegunle (Ajeromi) | Ipaja-Ayobo-Mosan + 38 more | 13 |
| 69 | 44.2 | Oworonshoki | Ajegunle (Ajeromi) + 39 more | 12 |
| 70 | 43.5 | Ikeja GRA | Oworonshoki + 40 more | 11 |
| 71 | 43.3 | Agric-Majidun-Ogolonto | Ikota-VGC-Chevron + 16 more | 10 |
| 72 | 42.6 | Makoko-Iwaya | Ikeja GRA + 41 more | 9 |
| 73 | 41.4 | Mile 2-Amuwo | Makoko-Iwaya + 42 more | 8 |
| 74 | 40.6 | Lekki FTZ-Dangote | Agric-Majidun-Ogolonto + 17 more | 7 |
| 75 | 38.7 | Alaba-Ojo-LASU + 8 more | Mile 2-Amuwo + 43 more | 6 |
| 76 | 39.3 | Lekki FTZ-Dangote + 18 more | Alaba-Ojo-LASU + 52 more | 5 |
| 77 | 36.5 | Ijora-Badia | Victoria Island + 4 more | 4 |
| 78 | 32.4 | Lekki FTZ-Dangote + 71 more | Ijora-Badia + 5 more | 3 |
| 79 | 28.9 | UNILAG | Lekki FTZ-Dangote + 77 more | 2 |
| 80 | 28.7 | Ilupeju + Papa Ajao-Ladipo | UNILAG + 78 more | 1 |

## Appendix D. Districts at each threshold


### At 90%: 81 districts (71 after folding tiny plain units)

Rich or distinct units still alone (24): Isale Eko-Idumota-Marina, Ikoyi-Banana Island, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Ogijo-Sagamu Rd, Isheri-Olowora (Ikosi-Isheri), UNILAG, Ebute Metta-Oyingbo-Otto-Iddo, Makoko-Iwaya, Surulere (Ojuelegba-Bode Thomas-Stadium), Ilupeju, Papa Ajao-Ladipo, Oshodi-Mafoluku, Apapa-Tin Can, Ijora-Badia, Ajegunle (Ajeromi), Amukoko-Layeni (Ifelodun), Mile 2-Amuwo, Kirikiri-Navy Town, Alaba-Ojo-LASU, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.

| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |
|---|---|---|---|---|---|
| 1 | Igbogbo-Baiyeku | 68 | 51.4 | 5.7 | - |
| 2 | Ijede | 72 | 42.5 | 4.7 | - |
| 3 | Agbara-Morogbo | 131 | 42.1 | 4.7 | - |
| 4 | Badagry town-Seme | 243 | 36.6 | 4.1 | - |
| 5 | Igando | 49 | 34.4 | 3.8 | - |
| 6 | Ipaja-Ayobo-Mosan | 34 | 31.1 | 3.5 | - |
| 7 | Isawo-Owutu-Odogunyan | 42 | 30.5 | 3.4 | - |
| 8 | Ikorodu town | 35 | 29.6 | 3.3 | - |
| 9 | Awoyaya-Lakowe | 190 | 29.3 | 3.3 | - |
| 10 | Imota | 101 | 27.2 | 3.0 | - |
| 11 | Ajah-Abraham Adesanya | 42 | 24.0 | 2.7 | - |
| 12 | Epe town-Noforija | 319 | 23.4 | 2.6 | - |
| 13 | Ogijo-Sagamu Rd | 34 | 22.8 | 2.5 | - |
| 14 | Ikotun | 22 | 21.2 | 2.4 | - |
| 15 | Okota-Ago Palace | 22 | 20.4 | 2.3 | - |
| 16 | Eleko-Akodo-Ibeju | 211 | 18.1 | 2.0 | - |
| 17 | Alagbado-Agbado | 18 | 18.1 | 2.0 | - |
| 18 | Ogba-Agidingbi-Alausa industrial | 19 | 18.0 | 2.0 | - |
| 19 | Ikate-Agungi-Osapa-Jakande | 24 | 15.9 | 1.8 | - |
| 20 | Iba | 19 | 15.8 | 1.8 | - |
| 21 | Okokomaiko | 37 | 15.7 | 1.7 | - |
| 22 | Ijanikin-Igbo Elerin | 48 | 15.4 | 1.7 | - |
| 23 | Satellite Town | 30 | 14.6 | 1.6 | - |
| 24 | Abule Egba-Ojokoro | 14 | 14.4 | 1.6 | - |
| 25 | Ikota-VGC-Chevron | 20 | 14.0 | 1.6 | - |
| 26 | Apapa-Tin Can | 31 | 13.2 | 1.5 | - |
| 27 | Oniru-Lekki Phase 1 | 15 | 13.1 | 1.5 | - |
| 28 | Ikoyi-Banana Island | 17 | 13.0 | 1.4 | - |
| 29 | Trade Fair-Abule Ado | 29 | 12.2 | 1.4 | - |
| 30 | Sangotedo | 40 | 12.1 | 1.3 | - |
| 31 | Idimu | 13 | 12.0 | 1.3 | - |
| 32 | Badore | 19 | 11.9 | 1.3 | - |
| 33 | Ketu-Mile 12-Ikosi | 18 | 11.8 | 1.3 | - |
| 34 | Ifako-Ijaiye-Iju | 12 | 11.8 | 1.3 | - |
| 35 | Egbeda-Akowonjo | 12 | 11.2 | 1.2 | - |
| 36 | Alaba-Ojo-LASU | 36 | 11.1 | 1.2 | - |
| 37 | Lekki FTZ-Dangote | 268 | 10.6 | 1.2 | - |
| 38 | Aguda-Ijesha-Coker | 11 | 10.6 | 1.2 | - |
| 39 | Mile 2-Amuwo | 11 | 10.1 | 1.1 | - |
| 40 | Surulere (Ojuelegba-Bode Thomas-Stadium) | 10 | 9.2 | 1.0 | - |
| 41 | Kirikiri-Navy Town | 31 | 9.1 | 1.0 | - |
| 42 | Festac | 12 | 8.6 | 1.0 | - |
| 43 | Isolo | 8 | 8.4 | 0.9 | - |
| 44 | Egbe | 8 | 7.8 | 0.9 | - |
| 45 | Ojota-Ogudu | 13 | 7.3 | 0.8 | - |
| 46 | Magodo | 8 | 7.1 | 0.8 | - |
| 47 | Shomolu-Pedro-Onipanu | 7 | 7.1 | 0.8 | - |
| 48 | Ojodu-Berger-Omole | 7 | 7.0 | 0.8 | - |
| 49 | Gbagada | 7 | 6.8 | 0.8 | - |
| 50 | Iyana Ipaja | 7 | 6.8 | 0.8 | - |
| 51 | Agege-Pen Cinema | 7 | 6.8 | 0.8 | - |
| 52 | Ejigbo | 8 | 6.6 | 0.7 | - |
| 53 | Ejinrin-Agbowa | 280 | 5.9 | 0.7 | - |
| 54 | Oshodi-Mafoluku | 6 | 5.8 | 0.6 | - |
| 55 | Mushin-Idi Araba-Odi Olowo | 6 | 5.6 | 0.6 | - |
| 56 | Ajegunle (Ajeromi) | 6 | 5.6 | 0.6 | - |
| 57 | Allen-Opebi-Computer Village | 6 | 5.4 | 0.6 | - |
| 58 | Yaba-Sabo-Jibowu | 5 | 5.1 | 0.6 | - |
| 59 | Victoria Island | 12 | 4.9 | 0.5 | - |
| 60 | Ikeja GRA | 6 | 4.9 | 0.5 | - |
| 61 | Bariga-Akoka | 5 | 4.8 | 0.5 | - |
| 62 | Ebute Metta-Oyingbo-Otto-Iddo | 6 | 4.7 | 0.5 | - |
| 63 | Iganmu-Orile | 5 | 4.6 | 0.5 | - |
| 64 | Ikeja Along-Cantonment | 7 | 4.2 | 0.5 | - |
| 65 | Makoko-Iwaya | 4 | 3.9 | 0.4 | - |
| 66 | Ajao Estate | 5 | 3.9 | 0.4 | - |
| 67 | Orile Agege-Dopemu | 4 | 3.9 | 0.4 | - |
| 68 | Airport (MMIA) | 11 | 3.8 | 0.4 | - |
| 69 | Papa Ajao-Ladipo | 3 | 3.2 | 0.4 | - |
| 70 | Itire-Lawanson | 3 | 3.1 | 0.3 | - |
| 71 | Oworonshoki | 8 | 2.9 | 0.3 | - |
| 72 | Agric-Majidun-Ogolonto | 20 | 2.8 | 0.3 | - |
| 73 | Ilupeju | 3 | 2.8 | 0.3 | - |
| 74 | Isale Eko-Idumota-Marina | 3 | 2.7 | 0.3 | - |
| 75 | Amukoko-Layeni (Ifelodun) | 3 | 2.6 | 0.3 | - |
| 76 | Isheri-Olowora (Ikosi-Isheri) | 10 | 2.4 | 0.3 | - |
| 77 | Maryland-Onigbongbo | 3 | 2.4 | 0.3 | - |
| 78 | Ijora-Badia | 3 | 2.2 | 0.2 | - |
| 79 | Obalende | 2 | 1.4 | 0.2 | - |
| 80 | Onikan-Lafiaji (Lagos Island East) | 2 | 1.0 | 0.1 | - |
| 81 | UNILAG | 2 | 1.0 | 0.1 | - |

### At 85%: 78 districts (68 after folding tiny plain units)

Rich or distinct units still alone (24): Isale Eko-Idumota-Marina, Ikoyi-Banana Island, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Ogijo-Sagamu Rd, Isheri-Olowora (Ikosi-Isheri), UNILAG, Ebute Metta-Oyingbo-Otto-Iddo, Makoko-Iwaya, Surulere (Ojuelegba-Bode Thomas-Stadium), Ilupeju, Papa Ajao-Ladipo, Oshodi-Mafoluku, Apapa-Tin Can, Ijora-Badia, Ajegunle (Ajeromi), Amukoko-Layeni (Ifelodun), Mile 2-Amuwo, Kirikiri-Navy Town, Alaba-Ojo-LASU, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.

| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |
|---|---|---|---|---|---|
| 1 | Agbara-Morogbo, Badagry town-Seme | 374 | 78.7 | 8.7 | 85 |
| 2 | Igbogbo-Baiyeku | 68 | 51.4 | 5.7 | - |
| 3 | Ipaja-Ayobo-Mosan, Alagbado-Agbado | 52 | 49.2 | 5.5 | 85 |
| 4 | Ijede | 72 | 42.5 | 4.7 | - |
| 5 | Igando | 49 | 34.4 | 3.8 | - |
| 6 | Isawo-Owutu-Odogunyan | 42 | 30.5 | 3.4 | - |
| 7 | Ikorodu town | 35 | 29.6 | 3.3 | - |
| 8 | Awoyaya-Lakowe | 190 | 29.3 | 3.3 | - |
| 9 | Imota | 101 | 27.2 | 3.0 | - |
| 10 | Ajah-Abraham Adesanya | 42 | 24.0 | 2.7 | - |
| 11 | Epe town-Noforija | 319 | 23.4 | 2.6 | - |
| 12 | Ogijo-Sagamu Rd | 34 | 22.8 | 2.5 | - |
| 13 | Ikotun | 22 | 21.2 | 2.4 | - |
| 14 | Okota-Ago Palace | 22 | 20.4 | 2.3 | - |
| 15 | Eleko-Akodo-Ibeju | 211 | 18.1 | 2.0 | - |
| 16 | Ogba-Agidingbi-Alausa industrial | 19 | 18.0 | 2.0 | - |
| 17 | Ikate-Agungi-Osapa-Jakande | 24 | 15.9 | 1.8 | - |
| 18 | Iba | 19 | 15.8 | 1.8 | - |
| 19 | Okokomaiko | 37 | 15.7 | 1.7 | - |
| 20 | Ijanikin-Igbo Elerin | 48 | 15.4 | 1.7 | - |
| 21 | Satellite Town | 30 | 14.6 | 1.6 | - |
| 22 | Abule Egba-Ojokoro | 14 | 14.4 | 1.6 | - |
| 23 | Ikota-VGC-Chevron | 20 | 14.0 | 1.6 | - |
| 24 | Apapa-Tin Can | 31 | 13.2 | 1.5 | - |
| 25 | Oniru-Lekki Phase 1 | 15 | 13.1 | 1.5 | - |
| 26 | Ikoyi-Banana Island | 17 | 13.0 | 1.4 | - |
| 27 | Trade Fair-Abule Ado | 29 | 12.2 | 1.4 | - |
| 28 | Sangotedo | 40 | 12.1 | 1.3 | - |
| 29 | Idimu | 13 | 12.0 | 1.3 | - |
| 30 | Badore | 19 | 11.9 | 1.3 | - |
| 31 | Ketu-Mile 12-Ikosi | 18 | 11.8 | 1.3 | - |
| 32 | Ifako-Ijaiye-Iju | 12 | 11.8 | 1.3 | - |
| 33 | Egbeda-Akowonjo | 12 | 11.2 | 1.2 | - |
| 34 | Alaba-Ojo-LASU | 36 | 11.1 | 1.2 | - |
| 35 | Agege-Pen Cinema, Orile Agege-Dopemu | 11 | 10.7 | 1.2 | 86 |
| 36 | Lekki FTZ-Dangote | 268 | 10.6 | 1.2 | - |
| 37 | Aguda-Ijesha-Coker | 11 | 10.6 | 1.2 | - |
| 38 | Mile 2-Amuwo | 11 | 10.1 | 1.1 | - |
| 39 | Surulere (Ojuelegba-Bode Thomas-Stadium) | 10 | 9.2 | 1.0 | - |
| 40 | Kirikiri-Navy Town | 31 | 9.1 | 1.0 | - |
| 41 | Festac | 12 | 8.6 | 1.0 | - |
| 42 | Isolo | 8 | 8.4 | 0.9 | - |
| 43 | Egbe | 8 | 7.8 | 0.9 | - |
| 44 | Ojota-Ogudu | 13 | 7.3 | 0.8 | - |
| 45 | Magodo | 8 | 7.1 | 0.8 | - |
| 46 | Shomolu-Pedro-Onipanu | 7 | 7.1 | 0.8 | - |
| 47 | Ojodu-Berger-Omole | 7 | 7.0 | 0.8 | - |
| 48 | Gbagada | 7 | 6.8 | 0.8 | - |
| 49 | Iyana Ipaja | 7 | 6.8 | 0.8 | - |
| 50 | Ejigbo | 8 | 6.6 | 0.7 | - |
| 51 | Ejinrin-Agbowa | 280 | 5.9 | 0.7 | - |
| 52 | Oshodi-Mafoluku | 6 | 5.8 | 0.6 | - |
| 53 | Mushin-Idi Araba-Odi Olowo | 6 | 5.6 | 0.6 | - |
| 54 | Ajegunle (Ajeromi) | 6 | 5.6 | 0.6 | - |
| 55 | Allen-Opebi-Computer Village | 6 | 5.4 | 0.6 | - |
| 56 | Yaba-Sabo-Jibowu | 5 | 5.1 | 0.6 | - |
| 57 | Victoria Island | 12 | 4.9 | 0.5 | - |
| 58 | Ikeja GRA | 6 | 4.9 | 0.5 | - |
| 59 | Bariga-Akoka | 5 | 4.8 | 0.5 | - |
| 60 | Ebute Metta-Oyingbo-Otto-Iddo | 6 | 4.7 | 0.5 | - |
| 61 | Iganmu-Orile | 5 | 4.6 | 0.5 | - |
| 62 | Ikeja Along-Cantonment | 7 | 4.2 | 0.5 | - |
| 63 | Makoko-Iwaya | 4 | 3.9 | 0.4 | - |
| 64 | Ajao Estate | 5 | 3.9 | 0.4 | - |
| 65 | Airport (MMIA) | 11 | 3.8 | 0.4 | - |
| 66 | Papa Ajao-Ladipo | 3 | 3.2 | 0.4 | - |
| 67 | Itire-Lawanson | 3 | 3.1 | 0.3 | - |
| 68 | Oworonshoki | 8 | 2.9 | 0.3 | - |
| 69 | Agric-Majidun-Ogolonto | 20 | 2.8 | 0.3 | - |
| 70 | Ilupeju | 3 | 2.8 | 0.3 | - |
| 71 | Isale Eko-Idumota-Marina | 3 | 2.7 | 0.3 | - |
| 72 | Amukoko-Layeni (Ifelodun) | 3 | 2.6 | 0.3 | - |
| 73 | Isheri-Olowora (Ikosi-Isheri) | 10 | 2.4 | 0.3 | - |
| 74 | Maryland-Onigbongbo | 3 | 2.4 | 0.3 | - |
| 75 | Ijora-Badia | 3 | 2.2 | 0.2 | - |
| 76 | Obalende | 2 | 1.4 | 0.2 | - |
| 77 | Onikan-Lafiaji (Lagos Island East) | 2 | 1.0 | 0.1 | - |
| 78 | UNILAG | 2 | 1.0 | 0.1 | - |

### At 80%: 67 districts (57 after folding tiny plain units)

Rich or distinct units still alone (24): Isale Eko-Idumota-Marina, Ikoyi-Banana Island, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Ogijo-Sagamu Rd, Isheri-Olowora (Ikosi-Isheri), UNILAG, Ebute Metta-Oyingbo-Otto-Iddo, Makoko-Iwaya, Surulere (Ojuelegba-Bode Thomas-Stadium), Ilupeju, Papa Ajao-Ladipo, Oshodi-Mafoluku, Apapa-Tin Can, Ijora-Badia, Ajegunle (Ajeromi), Amukoko-Layeni (Ifelodun), Mile 2-Amuwo, Kirikiri-Navy Town, Alaba-Ojo-LASU, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.

| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |
|---|---|---|---|---|---|
| 1 | Igbogbo-Baiyeku, Ijede | 140 | 93.9 | 10.4 | 81 |
| 2 | Agbara-Morogbo, Badagry town-Seme | 374 | 78.7 | 8.7 | 85 |
| 3 | Iba, Idimu, Igando | 81 | 62.2 | 6.9 | 82 |
| 4 | Ikorodu town, Isawo-Owutu-Odogunyan | 76 | 60.1 | 6.7 | 81 |
| 5 | Ipaja-Ayobo-Mosan, Alagbado-Agbado | 52 | 49.2 | 5.5 | 85 |
| 6 | Sangotedo, Awoyaya-Lakowe | 230 | 41.4 | 4.6 | 80 |
| 7 | Ikota-VGC-Chevron, Ajah-Abraham Adesanya | 62 | 38.0 | 4.2 | 81 |
| 8 | Okokomaiko, Ijanikin-Igbo Elerin | 86 | 31.1 | 3.5 | 84 |
| 9 | Epe town-Noforija, Ejinrin-Agbowa | 600 | 29.3 | 3.3 | 85 |
| 10 | Imota | 101 | 27.2 | 3.0 | - |
| 11 | Ogijo-Sagamu Rd | 34 | 22.8 | 2.5 | - |
| 12 | Ikotun | 22 | 21.2 | 2.4 | - |
| 13 | Iyana Ipaja, Abule Egba-Ojokoro | 22 | 21.2 | 2.4 | 84 |
| 14 | Okota-Ago Palace | 22 | 20.4 | 2.3 | - |
| 15 | Eleko-Akodo-Ibeju | 211 | 18.1 | 2.0 | - |
| 16 | Ogba-Agidingbi-Alausa industrial | 19 | 18.0 | 2.0 | - |
| 17 | Ikate-Agungi-Osapa-Jakande | 24 | 15.9 | 1.8 | - |
| 18 | Satellite Town | 30 | 14.6 | 1.6 | - |
| 19 | Magodo, Ojodu-Berger-Omole | 15 | 14.1 | 1.6 | 83 |
| 20 | Apapa-Tin Can | 31 | 13.2 | 1.5 | - |
| 21 | Oniru-Lekki Phase 1 | 15 | 13.1 | 1.5 | - |
| 22 | Ikoyi-Banana Island | 17 | 13.0 | 1.4 | - |
| 23 | Shomolu-Pedro-Onipanu, Mushin-Idi Araba-Odi Olowo | 13 | 12.7 | 1.4 | 82 |
| 24 | Trade Fair-Abule Ado | 29 | 12.2 | 1.4 | - |
| 25 | Badore | 19 | 11.9 | 1.3 | - |
| 26 | Ketu-Mile 12-Ikosi | 18 | 11.8 | 1.3 | - |
| 27 | Ifako-Ijaiye-Iju | 12 | 11.8 | 1.3 | - |
| 28 | Egbeda-Akowonjo | 12 | 11.2 | 1.2 | - |
| 29 | Alaba-Ojo-LASU | 36 | 11.1 | 1.2 | - |
| 30 | Agege-Pen Cinema, Orile Agege-Dopemu | 11 | 10.7 | 1.2 | 86 |
| 31 | Lekki FTZ-Dangote | 268 | 10.6 | 1.2 | - |
| 32 | Aguda-Ijesha-Coker | 11 | 10.6 | 1.2 | - |
| 33 | Mile 2-Amuwo | 11 | 10.1 | 1.1 | - |
| 34 | Surulere (Ojuelegba-Bode Thomas-Stadium) | 10 | 9.2 | 1.0 | - |
| 35 | Kirikiri-Navy Town | 31 | 9.1 | 1.0 | - |
| 36 | Festac | 12 | 8.6 | 1.0 | - |
| 37 | Isolo | 8 | 8.4 | 0.9 | - |
| 38 | Egbe | 8 | 7.8 | 0.9 | - |
| 39 | Ojota-Ogudu | 13 | 7.3 | 0.8 | - |
| 40 | Gbagada | 7 | 6.8 | 0.8 | - |
| 41 | Ejigbo | 8 | 6.6 | 0.7 | - |
| 42 | Oshodi-Mafoluku | 6 | 5.8 | 0.6 | - |
| 43 | Ajegunle (Ajeromi) | 6 | 5.6 | 0.6 | - |
| 44 | Allen-Opebi-Computer Village | 6 | 5.4 | 0.6 | - |
| 45 | Yaba-Sabo-Jibowu | 5 | 5.1 | 0.6 | - |
| 46 | Victoria Island | 12 | 4.9 | 0.5 | - |
| 47 | Ikeja GRA | 6 | 4.9 | 0.5 | - |
| 48 | Bariga-Akoka | 5 | 4.8 | 0.5 | - |
| 49 | Ebute Metta-Oyingbo-Otto-Iddo | 6 | 4.7 | 0.5 | - |
| 50 | Iganmu-Orile | 5 | 4.6 | 0.5 | - |
| 51 | Ikeja Along-Cantonment | 7 | 4.2 | 0.5 | - |
| 52 | Makoko-Iwaya | 4 | 3.9 | 0.4 | - |
| 53 | Ajao Estate | 5 | 3.9 | 0.4 | - |
| 54 | Airport (MMIA) | 11 | 3.8 | 0.4 | - |
| 55 | Papa Ajao-Ladipo | 3 | 3.2 | 0.4 | - |
| 56 | Itire-Lawanson | 3 | 3.1 | 0.3 | - |
| 57 | Oworonshoki | 8 | 2.9 | 0.3 | - |
| 58 | Agric-Majidun-Ogolonto | 20 | 2.8 | 0.3 | - |
| 59 | Ilupeju | 3 | 2.8 | 0.3 | - |
| 60 | Isale Eko-Idumota-Marina | 3 | 2.7 | 0.3 | - |
| 61 | Amukoko-Layeni (Ifelodun) | 3 | 2.6 | 0.3 | - |
| 62 | Isheri-Olowora (Ikosi-Isheri) | 10 | 2.4 | 0.3 | - |
| 63 | Maryland-Onigbongbo | 3 | 2.4 | 0.3 | - |
| 64 | Ijora-Badia | 3 | 2.2 | 0.2 | - |
| 65 | Obalende | 2 | 1.4 | 0.2 | - |
| 66 | Onikan-Lafiaji (Lagos Island East) | 2 | 1.0 | 0.1 | - |
| 67 | UNILAG | 2 | 1.0 | 0.1 | - |

### At 75%: 56 districts (46 after folding tiny plain units)

Rich or distinct units still alone (24): Isale Eko-Idumota-Marina, Ikoyi-Banana Island, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Ogijo-Sagamu Rd, Isheri-Olowora (Ikosi-Isheri), UNILAG, Ebute Metta-Oyingbo-Otto-Iddo, Makoko-Iwaya, Surulere (Ojuelegba-Bode Thomas-Stadium), Ilupeju, Papa Ajao-Ladipo, Oshodi-Mafoluku, Apapa-Tin Can, Ijora-Badia, Ajegunle (Ajeromi), Amukoko-Layeni (Ifelodun), Mile 2-Amuwo, Kirikiri-Navy Town, Alaba-Ojo-LASU, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.

| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |
|---|---|---|---|---|---|
| 1 | Igbogbo-Baiyeku, Ijede | 140 | 93.9 | 10.4 | 81 |
| 2 | Agbara-Morogbo, Badagry town-Seme | 374 | 78.7 | 8.7 | 85 |
| 3 | Iyana Ipaja, Ipaja-Ayobo-Mosan, Alagbado-Agbado, Abule Egba-Ojokoro | 74 | 70.4 | 7.8 | 80 |
| 4 | Iba, Idimu, Igando | 81 | 62.2 | 6.9 | 82 |
| 5 | Ikorodu town, Isawo-Owutu-Odogunyan | 76 | 60.1 | 6.7 | 81 |
| 6 | Eleko-Akodo-Ibeju, Epe town-Noforija, Ejinrin-Agbowa | 811 | 47.4 | 5.3 | 79 |
| 7 | Okota-Ago Palace, Ikotun | 43 | 41.6 | 4.6 | 78 |
| 8 | Sangotedo, Awoyaya-Lakowe | 230 | 41.4 | 4.6 | 80 |
| 9 | Ikota-VGC-Chevron, Ajah-Abraham Adesanya | 62 | 38.0 | 4.2 | 81 |
| 10 | Egbeda-Akowonjo, Agege-Pen Cinema, Orile Agege-Dopemu, Ifako-Ijaiye-Iju | 35 | 33.7 | 3.7 | 78 |
| 11 | Okokomaiko, Ijanikin-Igbo Elerin | 86 | 31.1 | 3.5 | 84 |
| 12 | Oniru-Lekki Phase 1, Ikate-Agungi-Osapa-Jakande | 39 | 29.0 | 3.2 | 75 |
| 13 | Imota | 101 | 27.2 | 3.0 | - |
| 14 | Shomolu-Pedro-Onipanu, Aguda-Ijesha-Coker, Itire-Lawanson, Mushin-Idi Araba-Odi Olowo | 27 | 26.4 | 2.9 | 79 |
| 15 | Ogijo-Sagamu Rd | 34 | 22.8 | 2.5 | - |
| 16 | Ketu-Mile 12-Ikosi, Ojota-Ogudu | 31 | 19.1 | 2.1 | 75 |
| 17 | Ogba-Agidingbi-Alausa industrial | 19 | 18.0 | 2.0 | - |
| 18 | Satellite Town | 30 | 14.6 | 1.6 | - |
| 19 | Ejigbo, Egbe | 16 | 14.4 | 1.6 | 80 |
| 20 | Magodo, Ojodu-Berger-Omole | 15 | 14.1 | 1.6 | 83 |
| 21 | Apapa-Tin Can | 31 | 13.2 | 1.5 | - |
| 22 | Ikoyi-Banana Island | 17 | 13.0 | 1.4 | - |
| 23 | Trade Fair-Abule Ado | 29 | 12.2 | 1.4 | - |
| 24 | Badore | 19 | 11.9 | 1.3 | - |
| 25 | Alaba-Ojo-LASU | 36 | 11.1 | 1.2 | - |
| 26 | Lekki FTZ-Dangote | 268 | 10.6 | 1.2 | - |
| 27 | Mile 2-Amuwo | 11 | 10.1 | 1.1 | - |
| 28 | Surulere (Ojuelegba-Bode Thomas-Stadium) | 10 | 9.2 | 1.0 | - |
| 29 | Kirikiri-Navy Town | 31 | 9.1 | 1.0 | - |
| 30 | Festac | 12 | 8.6 | 1.0 | - |
| 31 | Isolo | 8 | 8.4 | 0.9 | - |
| 32 | Airport (MMIA), Ikeja Along-Cantonment | 18 | 8.0 | 0.9 | 78 |
| 33 | Gbagada | 7 | 6.8 | 0.8 | - |
| 34 | Oshodi-Mafoluku | 6 | 5.8 | 0.6 | - |
| 35 | Ajegunle (Ajeromi) | 6 | 5.6 | 0.6 | - |
| 36 | Allen-Opebi-Computer Village | 6 | 5.4 | 0.6 | - |
| 37 | Yaba-Sabo-Jibowu | 5 | 5.1 | 0.6 | - |
| 38 | Victoria Island | 12 | 4.9 | 0.5 | - |
| 39 | Ikeja GRA | 6 | 4.9 | 0.5 | - |
| 40 | Bariga-Akoka | 5 | 4.8 | 0.5 | - |
| 41 | Ebute Metta-Oyingbo-Otto-Iddo | 6 | 4.7 | 0.5 | - |
| 42 | Iganmu-Orile | 5 | 4.6 | 0.5 | - |
| 43 | Makoko-Iwaya | 4 | 3.9 | 0.4 | - |
| 44 | Ajao Estate | 5 | 3.9 | 0.4 | - |
| 45 | Papa Ajao-Ladipo | 3 | 3.2 | 0.4 | - |
| 46 | Oworonshoki | 8 | 2.9 | 0.3 | - |
| 47 | Agric-Majidun-Ogolonto | 20 | 2.8 | 0.3 | - |
| 48 | Ilupeju | 3 | 2.8 | 0.3 | - |
| 49 | Isale Eko-Idumota-Marina | 3 | 2.7 | 0.3 | - |
| 50 | Amukoko-Layeni (Ifelodun) | 3 | 2.6 | 0.3 | - |
| 51 | Isheri-Olowora (Ikosi-Isheri) | 10 | 2.4 | 0.3 | - |
| 52 | Maryland-Onigbongbo | 3 | 2.4 | 0.3 | - |
| 53 | Ijora-Badia | 3 | 2.2 | 0.2 | - |
| 54 | Obalende | 2 | 1.4 | 0.2 | - |
| 55 | Onikan-Lafiaji (Lagos Island East) | 2 | 1.0 | 0.1 | - |
| 56 | UNILAG | 2 | 1.0 | 0.1 | - |

### At 70%: 48 districts (39 after folding tiny plain units)

Rich or distinct units still alone (23): Isale Eko-Idumota-Marina, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Ogijo-Sagamu Rd, Isheri-Olowora (Ikosi-Isheri), UNILAG, Ebute Metta-Oyingbo-Otto-Iddo, Makoko-Iwaya, Surulere (Ojuelegba-Bode Thomas-Stadium), Ilupeju, Papa Ajao-Ladipo, Oshodi-Mafoluku, Apapa-Tin Can, Ijora-Badia, Ajegunle (Ajeromi), Amukoko-Layeni (Ifelodun), Mile 2-Amuwo, Kirikiri-Navy Town, Alaba-Ojo-LASU, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.

| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |
|---|---|---|---|---|---|
| 1 | Ikorodu town, Isawo-Owutu-Odogunyan, Igbogbo-Baiyeku, Ijede | 216 | 154.0 | 17.1 | 76 |
| 2 | Ejigbo, Iyana Ipaja, Ipaja-Ayobo-Mosan, Alagbado-Agbado, Egbeda-Akowonjo, Egbe, Agege-Pen Cinema, Orile Agege-Dopemu, Ifako-Ijaiye-Iju, Abule Egba-Ojokoro | 124 | 118.5 | 13.2 | 75 |
| 3 | Okokomaiko, Ijanikin-Igbo Elerin, Agbara-Morogbo, Badagry town-Seme | 459 | 109.8 | 12.2 | 75 |
| 4 | Oniru-Lekki Phase 1, Ikate-Agungi-Osapa-Jakande, Ikota-VGC-Chevron, Ajah-Abraham Adesanya | 101 | 67.0 | 7.4 | 73 |
| 5 | Iba, Idimu, Igando | 81 | 62.2 | 6.9 | 82 |
| 6 | Eleko-Akodo-Ibeju, Epe town-Noforija, Ejinrin-Agbowa | 811 | 47.4 | 5.3 | 79 |
| 7 | Okota-Ago Palace, Ikotun | 43 | 41.6 | 4.6 | 78 |
| 8 | Sangotedo, Awoyaya-Lakowe | 230 | 41.4 | 4.6 | 80 |
| 9 | Shomolu-Pedro-Onipanu, Aguda-Ijesha-Coker, Itire-Lawanson, Iganmu-Orile, Mushin-Idi Araba-Odi Olowo, Isolo | 40 | 39.4 | 4.4 | 76 |
| 10 | Imota | 101 | 27.2 | 3.0 | - |
| 11 | Ogijo-Sagamu Rd | 34 | 22.8 | 2.5 | - |
| 12 | Ketu-Mile 12-Ikosi, Ojota-Ogudu | 31 | 19.1 | 2.1 | 75 |
| 13 | Ogba-Agidingbi-Alausa industrial | 19 | 18.0 | 2.0 | - |
| 14 | Satellite Town | 30 | 14.6 | 1.6 | - |
| 15 | Obalende, Ikoyi-Banana Island | 19 | 14.4 | 1.6 | 71 |
| 16 | Magodo, Ojodu-Berger-Omole | 15 | 14.1 | 1.6 | 83 |
| 17 | Apapa-Tin Can | 31 | 13.2 | 1.5 | - |
| 18 | Trade Fair-Abule Ado | 29 | 12.2 | 1.4 | - |
| 19 | Badore | 19 | 11.9 | 1.3 | - |
| 20 | Alaba-Ojo-LASU | 36 | 11.1 | 1.2 | - |
| 21 | Lekki FTZ-Dangote | 268 | 10.6 | 1.2 | - |
| 22 | Mile 2-Amuwo | 11 | 10.1 | 1.1 | - |
| 23 | Surulere (Ojuelegba-Bode Thomas-Stadium) | 10 | 9.2 | 1.0 | - |
| 24 | Kirikiri-Navy Town | 31 | 9.1 | 1.0 | - |
| 25 | Festac | 12 | 8.6 | 1.0 | - |
| 26 | Airport (MMIA), Ikeja Along-Cantonment | 18 | 8.0 | 0.9 | 78 |
| 27 | Gbagada | 7 | 6.8 | 0.8 | - |
| 28 | Oshodi-Mafoluku | 6 | 5.8 | 0.6 | - |
| 29 | Ajegunle (Ajeromi) | 6 | 5.6 | 0.6 | - |
| 30 | Allen-Opebi-Computer Village | 6 | 5.4 | 0.6 | - |
| 31 | Yaba-Sabo-Jibowu | 5 | 5.1 | 0.6 | - |
| 32 | Victoria Island | 12 | 4.9 | 0.5 | - |
| 33 | Ikeja GRA | 6 | 4.9 | 0.5 | - |
| 34 | Bariga-Akoka | 5 | 4.8 | 0.5 | - |
| 35 | Ebute Metta-Oyingbo-Otto-Iddo | 6 | 4.7 | 0.5 | - |
| 36 | Makoko-Iwaya | 4 | 3.9 | 0.4 | - |
| 37 | Ajao Estate | 5 | 3.9 | 0.4 | - |
| 38 | Papa Ajao-Ladipo | 3 | 3.2 | 0.4 | - |
| 39 | Oworonshoki | 8 | 2.9 | 0.3 | - |
| 40 | Agric-Majidun-Ogolonto | 20 | 2.8 | 0.3 | - |
| 41 | Ilupeju | 3 | 2.8 | 0.3 | - |
| 42 | Isale Eko-Idumota-Marina | 3 | 2.7 | 0.3 | - |
| 43 | Amukoko-Layeni (Ifelodun) | 3 | 2.6 | 0.3 | - |
| 44 | Isheri-Olowora (Ikosi-Isheri) | 10 | 2.4 | 0.3 | - |
| 45 | Maryland-Onigbongbo | 3 | 2.4 | 0.3 | - |
| 46 | Ijora-Badia | 3 | 2.2 | 0.2 | - |
| 47 | Onikan-Lafiaji (Lagos Island East) | 2 | 1.0 | 0.1 | - |
| 48 | UNILAG | 2 | 1.0 | 0.1 | - |

### At 65%: 36 districts (29 after folding tiny plain units)

Rich or distinct units still alone (19): Isale Eko-Idumota-Marina, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Isheri-Olowora (Ikosi-Isheri), UNILAG, Makoko-Iwaya, Ilupeju, Papa Ajao-Ladipo, Oshodi-Mafoluku, Apapa-Tin Can, Ijora-Badia, Ajegunle (Ajeromi), Amukoko-Layeni (Ifelodun), Mile 2-Amuwo, Alaba-Ojo-LASU, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.

| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |
|---|---|---|---|---|---|
| 1 | Ikorodu town, Isawo-Owutu-Odogunyan, Ogijo-Sagamu Rd, Igbogbo-Baiyeku, Ijede | 251 | 176.8 | 19.6 | 72 |
| 2 | Ejigbo, Iyana Ipaja, Ipaja-Ayobo-Mosan, Alagbado-Agbado, Egbeda-Akowonjo, Egbe, Agege-Pen Cinema, Orile Agege-Dopemu, Ifako-Ijaiye-Iju, Abule Egba-Ojokoro | 124 | 118.5 | 13.2 | 75 |
| 3 | Sangotedo, Awoyaya-Lakowe, Eleko-Akodo-Ibeju, Epe town-Noforija, Ejinrin-Agbowa, Imota | 1142 | 116.0 | 12.9 | 72 |
| 4 | Okota-Ago Palace, Festac, Iba, Idimu, Ikotun, Igando | 136 | 112.4 | 12.5 | 71 |
| 5 | Okokomaiko, Ijanikin-Igbo Elerin, Agbara-Morogbo, Badagry town-Seme | 459 | 109.8 | 12.2 | 75 |
| 6 | Oniru-Lekki Phase 1, Ikate-Agungi-Osapa-Jakande, Ikota-VGC-Chevron, Ajah-Abraham Adesanya | 101 | 67.0 | 7.4 | 73 |
| 7 | Shomolu-Pedro-Onipanu, Aguda-Ijesha-Coker, Itire-Lawanson, Iganmu-Orile, Mushin-Idi Araba-Odi Olowo, Isolo | 40 | 39.4 | 4.4 | 76 |
| 8 | Kirikiri-Navy Town, Satellite Town, Trade Fair-Abule Ado | 90 | 35.9 | 4.0 | 68 |
| 9 | Ketu-Mile 12-Ikosi, Ojota-Ogudu, Magodo, Ojodu-Berger-Omole | 46 | 33.2 | 3.7 | 71 |
| 10 | Yaba-Sabo-Jibowu, Ebute Metta-Oyingbo-Otto-Iddo, Surulere (Ojuelegba-Bode Thomas-Stadium) | 21 | 19.0 | 2.1 | 70 |
| 11 | Ogba-Agidingbi-Alausa industrial | 19 | 18.0 | 2.0 | - |
| 12 | Onikan-Lafiaji (Lagos Island East), Obalende, Ikoyi-Banana Island | 20 | 15.4 | 1.7 | 70 |
| 13 | Apapa-Tin Can | 31 | 13.2 | 1.5 | - |
| 14 | Badore | 19 | 11.9 | 1.3 | - |
| 15 | Alaba-Ojo-LASU | 36 | 11.1 | 1.2 | - |
| 16 | Lekki FTZ-Dangote | 268 | 10.6 | 1.2 | - |
| 17 | Mile 2-Amuwo | 11 | 10.1 | 1.1 | - |
| 18 | Gbagada, Maryland-Onigbongbo | 10 | 9.2 | 1.0 | 67 |
| 19 | Airport (MMIA), Ikeja Along-Cantonment | 18 | 8.0 | 0.9 | 78 |
| 20 | Oshodi-Mafoluku | 6 | 5.8 | 0.6 | - |
| 21 | Ajegunle (Ajeromi) | 6 | 5.6 | 0.6 | - |
| 22 | Allen-Opebi-Computer Village | 6 | 5.4 | 0.6 | - |
| 23 | Victoria Island | 12 | 4.9 | 0.5 | - |
| 24 | Ikeja GRA | 6 | 4.9 | 0.5 | - |
| 25 | Bariga-Akoka | 5 | 4.8 | 0.5 | - |
| 26 | Makoko-Iwaya | 4 | 3.9 | 0.4 | - |
| 27 | Ajao Estate | 5 | 3.9 | 0.4 | - |
| 28 | Papa Ajao-Ladipo | 3 | 3.2 | 0.4 | - |
| 29 | Oworonshoki | 8 | 2.9 | 0.3 | - |
| 30 | Agric-Majidun-Ogolonto | 20 | 2.8 | 0.3 | - |
| 31 | Ilupeju | 3 | 2.8 | 0.3 | - |
| 32 | Isale Eko-Idumota-Marina | 3 | 2.7 | 0.3 | - |
| 33 | Amukoko-Layeni (Ifelodun) | 3 | 2.6 | 0.3 | - |
| 34 | Isheri-Olowora (Ikosi-Isheri) | 10 | 2.4 | 0.3 | - |
| 35 | Ijora-Badia | 3 | 2.2 | 0.2 | - |
| 36 | UNILAG | 2 | 1.0 | 0.1 | - |

### At 60%: 28 districts (23 after folding tiny plain units)

Rich or distinct units still alone (14): Isale Eko-Idumota-Marina, Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, Isheri-Olowora (Ikosi-Isheri), UNILAG, Makoko-Iwaya, Oshodi-Mafoluku, Ijora-Badia, Ajegunle (Ajeromi), Mile 2-Amuwo, Ikeja GRA, Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial.

| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |
|---|---|---|---|---|---|
| 1 | Ikorodu town, Isawo-Owutu-Odogunyan, Ogijo-Sagamu Rd, Igbogbo-Baiyeku, Ijede | 251 | 176.8 | 19.6 | 72 |
| 2 | Badore, Sangotedo, Awoyaya-Lakowe, Eleko-Akodo-Ibeju, Epe town-Noforija, Ejinrin-Agbowa, Imota | 1161 | 127.9 | 14.2 | 69 |
| 3 | Alaba-Ojo-LASU, Okokomaiko, Ijanikin-Igbo Elerin, Agbara-Morogbo, Badagry town-Seme | 496 | 120.9 | 13.4 | 70 |
| 4 | Ejigbo, Iyana Ipaja, Ipaja-Ayobo-Mosan, Alagbado-Agbado, Egbeda-Akowonjo, Egbe, Agege-Pen Cinema, Orile Agege-Dopemu, Ifako-Ijaiye-Iju, Abule Egba-Ojokoro | 124 | 118.5 | 13.2 | 75 |
| 5 | Okota-Ago Palace, Festac, Iba, Idimu, Ikotun, Igando | 136 | 112.4 | 12.5 | 71 |
| 6 | Oniru-Lekki Phase 1, Ikate-Agungi-Osapa-Jakande, Ikota-VGC-Chevron, Ajah-Abraham Adesanya | 101 | 67.0 | 7.4 | 73 |
| 7 | Apapa-Tin Can, Kirikiri-Navy Town, Satellite Town, Trade Fair-Abule Ado | 121 | 49.1 | 5.5 | 65 |
| 8 | Shomolu-Pedro-Onipanu, Bariga-Akoka, Aguda-Ijesha-Coker, Itire-Lawanson, Iganmu-Orile, Mushin-Idi Araba-Odi Olowo, Isolo, Amukoko-Layeni (Ifelodun) | 48 | 46.8 | 5.2 | 70 |
| 9 | Ketu-Mile 12-Ikosi, Ojota-Ogudu, Magodo, Gbagada, Ojodu-Berger-Omole, Maryland-Onigbongbo | 56 | 42.4 | 4.7 | 66 |
| 10 | Yaba-Sabo-Jibowu, Ebute Metta-Oyingbo-Otto-Iddo, Surulere (Ojuelegba-Bode Thomas-Stadium) | 21 | 19.0 | 2.1 | 70 |
| 11 | Ogba-Agidingbi-Alausa industrial | 19 | 18.0 | 2.0 | - |
| 12 | Onikan-Lafiaji (Lagos Island East), Obalende, Ikoyi-Banana Island | 20 | 15.4 | 1.7 | 70 |
| 13 | Ajao Estate, Airport (MMIA), Ikeja Along-Cantonment | 23 | 11.9 | 1.3 | 68 |
| 14 | Lekki FTZ-Dangote | 268 | 10.6 | 1.2 | - |
| 15 | Mile 2-Amuwo | 11 | 10.1 | 1.1 | - |
| 16 | Ilupeju, Papa Ajao-Ladipo | 6 | 6.0 | 0.7 | 64 |
| 17 | Oshodi-Mafoluku | 6 | 5.8 | 0.6 | - |
| 18 | Ajegunle (Ajeromi) | 6 | 5.6 | 0.6 | - |
| 19 | Allen-Opebi-Computer Village | 6 | 5.4 | 0.6 | - |
| 20 | Victoria Island | 12 | 4.9 | 0.5 | - |
| 21 | Ikeja GRA | 6 | 4.9 | 0.5 | - |
| 22 | Makoko-Iwaya | 4 | 3.9 | 0.4 | - |
| 23 | Oworonshoki | 8 | 2.9 | 0.3 | - |
| 24 | Agric-Majidun-Ogolonto | 20 | 2.8 | 0.3 | - |
| 25 | Isale Eko-Idumota-Marina | 3 | 2.7 | 0.3 | - |
| 26 | Isheri-Olowora (Ikosi-Isheri) | 10 | 2.4 | 0.3 | - |
| 27 | Ijora-Badia | 3 | 2.2 | 0.2 | - |
| 28 | UNILAG | 2 | 1.0 | 0.1 | - |

### At 55%: 19 districts (15 after folding tiny plain units)

Rich or distinct units still alone (10): Victoria Island, Lekki FTZ-Dangote, Agric-Majidun-Ogolonto, UNILAG, Makoko-Iwaya, Oshodi-Mafoluku, Ijora-Badia, Ajegunle (Ajeromi), Mile 2-Amuwo, Ikeja GRA.

| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |
|---|---|---|---|---|---|
| 1 | Badore, Sangotedo, Awoyaya-Lakowe, Eleko-Akodo-Ibeju, Epe town-Noforija, Ejinrin-Agbowa, Ikorodu town, Isawo-Owutu-Odogunyan, Ogijo-Sagamu Rd, Igbogbo-Baiyeku, Ijede, Imota, Isheri-Olowora (Ikosi-Isheri) | 1421 | 307.1 | 34.1 | 63 |
| 2 | Okota-Ago Palace, Ejigbo, Festac, Iba, Iyana Ipaja, Ipaja-Ayobo-Mosan, Alagbado-Agbado, Egbeda-Akowonjo, Idimu, Ikotun, Igando, Egbe, Agege-Pen Cinema, Orile Agege-Dopemu, Ifako-Ijaiye-Iju, Abule Egba-Ojokoro | 260 | 230.9 | 25.7 | 67 |
| 3 | Apapa-Tin Can, Kirikiri-Navy Town, Satellite Town, Trade Fair-Abule Ado, Alaba-Ojo-LASU, Okokomaiko, Ijanikin-Igbo Elerin, Agbara-Morogbo, Badagry town-Seme | 616 | 170.0 | 18.9 | 62 |
| 4 | Ketu-Mile 12-Ikosi, Ojota-Ogudu, Magodo, Gbagada, Shomolu-Pedro-Onipanu, Bariga-Akoka, Yaba-Sabo-Jibowu, Ebute Metta-Oyingbo-Otto-Iddo, Surulere (Ojuelegba-Bode Thomas-Stadium), Aguda-Ijesha-Coker, Itire-Lawanson, Iganmu-Orile, Mushin-Idi Araba-Odi Olowo, Isolo, Amukoko-Layeni (Ifelodun), Allen-Opebi-Computer Village, Ogba-Agidingbi-Alausa industrial, Ojodu-Berger-Omole, Maryland-Onigbongbo | 149 | 131.6 | 14.6 | 61 |
| 5 | Oniru-Lekki Phase 1, Ikate-Agungi-Osapa-Jakande, Ikota-VGC-Chevron, Ajah-Abraham Adesanya | 101 | 67.0 | 7.4 | 73 |
| 6 | Isale Eko-Idumota-Marina, Onikan-Lafiaji (Lagos Island East), Obalende, Ikoyi-Banana Island | 24 | 18.1 | 2.0 | 64 |
| 7 | Ajao Estate, Airport (MMIA), Ikeja Along-Cantonment | 23 | 11.9 | 1.3 | 68 |
| 8 | Lekki FTZ-Dangote | 268 | 10.6 | 1.2 | - |
| 9 | Mile 2-Amuwo | 11 | 10.1 | 1.1 | - |
| 10 | Ilupeju, Papa Ajao-Ladipo | 6 | 6.0 | 0.7 | 64 |
| 11 | Oshodi-Mafoluku | 6 | 5.8 | 0.6 | - |
| 12 | Ajegunle (Ajeromi) | 6 | 5.6 | 0.6 | - |
| 13 | Victoria Island | 12 | 4.9 | 0.5 | - |
| 14 | Ikeja GRA | 6 | 4.9 | 0.5 | - |
| 15 | Makoko-Iwaya | 4 | 3.9 | 0.4 | - |
| 16 | Oworonshoki | 8 | 2.9 | 0.3 | - |
| 17 | Agric-Majidun-Ogolonto | 20 | 2.8 | 0.3 | - |
| 18 | Ijora-Badia | 3 | 2.2 | 0.2 | - |
| 19 | UNILAG | 2 | 1.0 | 0.1 | - |