# Lagos-isms: the eccentricities in the real data (a running log)

**What this is.** While each district is studied, we log the real places' oddities: the things a tidy generator would never make, but that make Lagos feel like Lagos. For each one:
- what it is
- where it shows up in the real data (LGA and coordinates)
- how often it happens per km²
- which Gidi district it would suit

**Nothing here is built into Gidi yet.** That is the owner's "make it feel like Lagos" pass, after the whole map is done.

**How it's measured.** `scripts/study_isms.py <study id>` writes `study-<id>-isms.json`, the same yardstick for every studied area. Coordinates are lon,lat, for looking up only; nothing is ever copied.

**Limits of the data:**
- **OSM is incomplete.** Ikeja's buildings and every area's footpaths are under-mapped, so these are floors, not ceilings.
- **OSM centrelines are only good to 2–3 m,** which inflates the "road reserve" count. Read it as a comparison between areas, not a census.
- **Low ground is per LGA, not per street.** It comes from each LGA's share of land below 3 m and 5 m (`data/results/lga_table.json`, made from the 30 m Copernicus DEM) and from mapped wetland. The DEM itself is in the project's data folder (`data/tools/pull-data.sh` puts it there), so a street-by-street measure is possible later. It is a surface model (it includes roofs and trees), which makes built-up ground read high.

## The numbers (per km² of each study area, unless it says otherwise)

| | Maze (Mushin + Shomolu) | Hub (Oshodi + Surulere) | Jungle (Ajegunle) | Festac (Amuwo Odofin) | Food Gate (Kosofe corridor) | Water Town (Makoko–Bariga) | Capital (central Ikeja) | Ikeja (whole) | Bazaar (Ojo market) | Port (Apapa) | Railside (Agege, Ifako, Alimosho) | Estate (Ikeja GRA, Magodo, Omole) | Old Island (Lagos Island, the island) | Heights (Ikoyi, VI, Banana Island) | Frontier (Lekki, Ajah, Awoyaya) | Border (Badagry, the eastern strip) | Old Shore (old Ikorodu) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Area studied, km² | 34 | 65 | 12 | 135 | 19 | 7 | 16 | 49 | 22 | 27 | 215 | 24 | 9 | 19 | 91 | 25 | 20 |
| Streets dead-ending at a canal or drain | 1.6 | 0.7 | 0.8 | 0.1 | **2.7** | 1.9 | 0.2 | 0.4 | 0.4 | 0.2 | 0.3 | 1.2 | 0.3 | 2.1 | 0.1 | 0 | 0.1 |
| Streets dead-ending at the rail | **0.6** | 0.1 | 0 | 0 | 0 | 0 | 0.2 | 0.1 | 0 | 0.2 | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 |
| Missing links (two dead ends < 25 m apart) | 1.0 | 1.0 | 0.5 | 0.5 | 1.5 | 1.0 | 2.4 | 2.0 | 0.4 | 0.2 | 0.9 | 1.9 | 1.4 | **2.7** | 0.8 | 0 | 0.3 |
| Buildings on a drainage channel or its bank | 3.3 | 1.6 | 2.9 | 0.1 | 6.7 | **48** | 0 | 0.1 | 1.0 | 1.8 | 0.7 | 0.04 | 0.5 | 1.7 | 0.01 | 0‖ | 0.2 |
| Buildings in the road reserve | 102 | 79 | **158** | 22 | 45 | 92 | 9 | 12 | 66 | 54 | 87 | 21 | 71 | 14 | 9 | 0.04‖ | 42 |
| Markets reaching a main road's carriageway | 5 of 7 | 5 of 7 | 3 of 5 | 4 of 7 | 9 of 15 | — | 4 of 8 | 7 of 20 | 3 of 5 | 3 of 5 | 6 of 12 | 5 of 11 | 4 of 10 | 10 of 45‡ | 4 of 33 | — | 2 of 3 |
| Side streets joining main roads, per km | 5.0 | 5.0 | 3.5 | 3.1 | 3.9 | 0.4 | 5.2 | 4.8 | 2.6 | 3.4 | **10.4** | 3.4 | 2.9 | 5.3 | 3.5 | 0.8 | 4.2 |
| Unfinished buildings (tagged), per km² | 9 | 19 | 10 | 15 | 0.2 | 3 | 0 | 1 | 14 | 14 | **79** | 0.6 | 0 | 0 | 6 | 0‖ | 0 |
| …as a share of all buildings | 0.6% | 1.1% | 0.4% | 2.8% | 0% | 0.2% | 0% | 0.4% | 1.4% | 1.4% | **4.1%** | 0.1% | 0% | 0% | 1.7% | — | 0% |
| Junctions where five or more roads meet | 0 | 0.02 | 0 | 0.02 | 0 | 0 | 0.06 | 0.02 | 0 | 0.04 | 0 | 0 | 0 | 0.05 | 0.02 | 0 | 0 |
| Junctions where two roads meet under 25° | 0.4 | 0.5 | 0.2 | 0.2 | 0.6 | 0.6 | 0.8 | 0.6 | 0 | 0.7 | 0.2 | 0.3 | **3.1**† | 1.3 | 0.3 | 0.08 | 0.2 |
| Buildings standing in mapped wetland | 0 | 0.1 | **243** | 4.7 | 0.3 | 0 | 0 | 0 | 4.5 | 4.4 | 0 | 0 | 0 | 0 | 0 | 0‖ | 1.6 |
| Land below 3 m (the LGA, from the DEM) | 0–15% | 5–13% | 11% | 44% | 57% | 55% | 0% | 0% | 32% | 48% | 0–5% | 0% (Ikeja), 57% (Kosofe) | **97%** | 54% (Eti Osa) | 54% (Eti Osa), 20% (Ibeju Lekki) | 33% | 14% (Ìkòròdú) |
| Expressway and trunk road, km | 63 | 82 | 15 | 48 | 31 | 27 | 27 | 66 | 35 | 30 | 33 | 30 | 53* | 30 | 109 | 51 | 12 |
| …bus stops on them | 5 | 9 | 0 | 0 | 8 | 0 | 3 | 8 | 0 | 0 | 0 | 1 | 0 | 5 | 13 | 0 | 7§ |
| …longest stretch with no mapped way across on foot | 9.5 km | 5.3 km | 1.6 km | 2.5 km | 3.7 km | 9.5 km* | 9.3 km | 5.3 km | 12.0 km | 3.5 km | 4.7 km | 5.4 km | 9.5 km* | 6.9 km | **27.5 km** | 25.7 km | 1.4 km |
| Gates across residential streets, per km² | 2.2 | 1.8 | 0.2 | 2.0 | 3.1 | 1.8 | 2.2 | 3.0 | 0.6 | 0.3 | 2.5 | 5.2 | 0.2 | **6.1** | 1.5 | 0 | 0.1 |
| One-way streets, share of street length | 14% | 14% | 8% | 14% | 12% | 5% | 36% | 29% | 11% | 27% | 8% | 14% | **40%** | 40% | 18% | 12% | 10% |
| **Streets ahead of houses: street cells with no buildings and under 25% built-up land (new)** | 0% | 0% | 0% | 8.6% | 0% | 4.2% | 0% | 0% | 3.7% | 1.7% | 0.5% | 0% | 0% | 1.3% | **11.6%** | 7.8% | 0% |

\* Water Town's is the long lagoon bridge, where nobody crosses on foot. Old Island's 53 km and 9.5 km are the expressway bridges that leave the island: the study counts their whole length.

† Old Island's acute junctions are mostly slip roads merging into the expressway that rings the island (3.3991, 6.4595; 3.4081, 6.4557), not street corners.

‖ The Border's figures that count buildings are near zero because OSM maps almost none there (27 in 25 km², though WorldCover counts 47% of the land built up): read them as unknown, not as absent.

‡ The Heights' 45 are small shops and retail plots: no market is mapped in its three boxes.

§ Old Shore's 7 bus stops sit on only 12 km of expressway: one every 1.7 km, the closest spacing of any area (the Hub has 9 on 82 km).

One-way streets: the share of the length of primary to residential streets tagged one-way (expressways left out: their carriageways are always one-way). Measured on each study's extract, outside `study_isms.py`.

## The isms, one by one

### 1. Streets that dead-end at a canal or drain
- **What:** a street runs to the water's edge and stops. There's no bridge, just a plank or a wall, though the street carries on beyond.
- **Where:**
  - Kosofe's produce corridor, 2.7 per km² (around 3.3897, 6.5931 and 3.3894, 6.5937)
  - Makoko's edge (3.3890, 6.5007)
  - Mushin (3.3770, 6.5391)
- **Suits:**
  - **Food Gate** and **Water Town**, along any channel
  - **the Maze,** at Gang Canal: today our canal has footbridges every few hundred metres, and real Mushin has more streets that just stop at it

### 2. Streets that dead-end at the rail
- **What:** the street stops at the tracks; people climb over on foot.
- **Where:** Mushin and Shomolu, 0.6 per km² (3.3614, 6.5325 and 3.3705, 6.5100). Also Apapa and central Ikeja, about 0.2 per km².
- **Suits:**
  - **Railside,** all along its line
  - **the Maze** and **the Hub:** they already do this (streets stop at the rail and worn paths cross), so this confirms the rule

### 3. Missing links
- **What:** two streets stop within a few metres of each other and never join. Usually a wall, a fence, a gutter or a disputed plot sits between them.
- **Where:**
  - central Ikeja, 2.4 per km² (3.3585, 6.6002 and 3.3512, 6.6065)
  - Kosofe, 1.5 per km²
  - Oshodi, about 1 per km²
- **Suits:**
  - **the Capital and the Estate:** gated estates and walled compounds cut through-streets
  - **Food Gate**

### 4. Buildings on drainage setbacks
- **What:** houses built on a channel's bank or over it.
- **Where:**
  - Makoko, 48 per km² (3.3890, 6.4956)
  - Kosofe, 6.7 per km² (3.3989, 6.5879)
  - Mushin, 3.3 per km² (3.3989, 6.5351)
- **Suits:**
  - **Water Town:** the land fringe as well as the stilt village
  - **Food Gate**
  - **the Maze,** along Gang Canal: today our canal keeps a clean 4 m bank

### 5. Buildings in the road reserve
- **What:** shops and house fronts that reach into the carriageway's width. Kiosks, extensions and walls narrow the road.
- **Where:**
  - Ajegunle, 158 per km² (3.3554, 6.4545)
  - Mushin, 102 per km² (3.3966, 6.5344)
  - Agege and Alimosho, 87 per km² (3.2742, 6.5565). Almost all on residential streets: 15,649 of the 18,667 there.
- **Read with care:** the count includes OSM's 2–3 m centreline error.
- **Suits:**
  - **Jungle City** and **the Maze**
  - **Railside:** its side streets
  - In Gidi this would mean letting kiosks and fronts creep into the street's clear width.

### 6. Markets spilling onto the carriageway
- **What:** a market that reaches into a main road's lanes. Traders sit on the kerb and in the outer lane.
- **Where:** most markets do it:
  - 9 of 15 in the Kosofe corridor (3.3835, 6.5971)
  - 6 of 12 in Agege and Alimosho (3.3010, 6.6367)
  - 7 of 20 in Ikeja
- **Suits:**
  - **Food Gate** (Mile Market)
  - **the Bazaar** (the electronics market on the expressway)
  - **Railside** (the roundabout market)
  - **the Hub** (Under the Bridge)

### 7. Roads doing too many jobs
- **What:** one main road carries through-traffic, side streets every few metres, bus stops, trading and parking all at once.
- **Where:**
  - Agege, Ifako and Alimosho: 10.4 side streets join each km of main road, twice the Mushin or Ikeja rate. 4% of main road there has a side street every 30 m or less.
  - The Kosofe corridor has the most bus stops on main roads: 0.2 per km.
- **Suits:**
  - **Railside:** its one long road
  - **Food Gate** (Northern Road)
  - **the Hub** (Ring Road)

### 8. Unfinished buildings
- **What:** frames and shells tagged as under construction, often for years.
- **Where:**
  - Agege, Ifako and Alimosho: 79 per km², 4% of all buildings (3.2758, 6.5546)
  - Festac: 2.8%
  - Oshodi: 1.1%
  - Ojo: 1.4%
- **Suits:**
  - **Railside**, the commuter sprawl
  - **the Frontier** (half-built estates)
  - **the Bazaar:** its plazas already have one in three unfinished

### 9. Odd junctions
- **What:** five or more roads meeting at one point, or two roads meeting at a knife-edge angle under 25°.
- **Where:**
  - acute junctions are most common in central Ikeja, 0.8 per km² (3.3333, 6.6015)
  - Apapa, 0.7 per km² (3.3679, 6.4486)
  - Kosofe, 0.6 per km²
  - five-way junctions are rare everywhere, at most 0.06 per km² (Ikeja: 3.3551, 6.5959)
- **Suits:**
  - **the Capital** (its roundabout is already one)
  - **the Port**
  - **Food Gate**
  - Our generator makes almost none: its junctions are 87–100% clean T's.

### 10. Flood-prone low spots
- **What:** homes on low ground or in mapped wetland that flood every rainy season.
- **Where:**
  - Ajegunle: 243 buildings per km² stand in mapped wetland (3.3336, 6.4553)
  - Apapa: 140 ha of wetland touch homes
  - Festac: 1,913 ha of wetland touch homes
  - **Lowest LGAs:** Kosofe (57% of land below 3 m), Lagos Mainland (55%), Apapa (48%), Amuwo Odofin (44%)
  - **Driest:** Ikeja, Agege and Ifako (0% below 3 m)
- **Suits:**
  - **Jungle City:** its flood days are in the district model
  - **Water Town**
  - **the Port**
  - **Food Gate's** creek side
  - Not the Capital or Railside, which stand on high ground.

### 11. Pedestrians forced onto expressways
- **What:** long stretches of expressway with no footbridge, underpass or crossing. People walk on the shoulder or run across.
- **Where:**
  - the Badagry expressway through Ojo: 12 km with no mapped way across (3.1580, 6.4907)
  - the expressways through Mushin and Ikeja: 9.3–9.5 km
  - bus stops sit on the expressway itself in Oshodi (9), Ikeja (8) and the Kosofe corridor (8)
- **Suits:**
  - **the Bazaar:** today it has footbridges every 300 m by the owner's rule. The real stretch would have far fewer, and a bus stop on the shoulder.
  - **the Hub** and **the Capital**
  - **the Frontier** (one long road)

### 12. Gates across streets (from the Estate on)
- **What:** a gate or barrier across a residential street, with a gateman. Estates, closes and walled streets shut the public road, at least at night.
- **Where:**
  - Ikoyi, Victoria Island and Banana Island (the Heights' study): 6.1 per km² mapped, the most of any area (3.4189, 6.4483 in Ikoyi; 3.4491, 6.4619 on Banana Island)
  - Ikeja GRA, Magodo and Omole: 5.2 per km² mapped (3.3601, 6.6481 in Omole; 3.3925, 6.6029 by Magodo). A median 13 m in from the main road.
  - The rest of Lagos: 0.2–3.1 per km², most in the Kosofe corridor (3.1), Ikeja as a whole (3.0) and Railside's sprawl (2.5).
- **Read with care:** gates are under-mapped everywhere (only 12% of the estates' street entries off a main road show one).
- **Suits:**
  - **the Estate:** built (every estate street gated where it leaves a public road, and the main gate on the road in from the Capital)
  - **Railside** and **Food Gate:** a few gated closes off the main road
  - **the Heights:** built (every cul-de-sac gated at its mouth; the through streets stay open)
  - **the Frontier** (estates of its own)
- **Also in the Estate's real data:** streets that end at a stream in a valley (1.2 per km², Magodo, 3.3755, 6.6094), and missing links (1.9 per km², Omole's north, 3.3771, 6.6349), where two estates meet wall to wall. Few buildings reach into the road (21 per km², against 79–158 in the dense districts): the walls stand back.

### 13. One-way streets (new with Old Island)
- **What:** the old core's narrow streets run one way, so a car or a bus goes round the block to reach the house across the road. Walkers and okadas ignore it.
- **Where:**
  - Lagos Island: 40% of the street length is one-way (3.3849, 6.4553; 3.3837, 6.4621 in the old core), the most of any area studied
  - Ikoyi, Victoria Island and Banana Island: 40% too, mostly VI's grid and Ikoyi's dual roads
  - central Ikeja (the Capital's study): 36%; Apapa: 27%
  - everywhere else: 5–14%
- **Suits:**
  - **Old Island:** one-way loops round the cloth market and the palace; traffic jams at every turn
  - **the Capital**, **the Port** and **the Heights**
- **Also in the Heights' real data:**
  - **the most missing links of any area** (2.7 per km², 3.4283, 6.4501 in Ikoyi): closes from neighbouring compounds end back to back, a wall apart
  - **streets that end at the water** (2.1 per km², 3.4229, 6.4249 on VI's lagoon front)
  - **few buildings in the road reserve** (14 per km²): walls and deep front yards stand the houses back 22 m
  - **an expressway with a 6.9 km stretch and no way across on foot** (3.4585, 6.4226), and 5 bus stops on it
- **Also in Lagos Island's real data:**
  - **the lowest ground of any area:** 97% of the LGA's land is below 3 m (Water Town's is 55%): every street is a flood-prone low spot.
  - **an expressway round the island** with slip roads merging at acute angles (3.1 per km², four times anywhere else)
  - **buildings in the road reserve** (71 per km²), about the Hub's rate; the old houses stand on the street line
  - **markets on the carriageway:** 4 of its 10 markets reach a main road

### 14. Streets ahead of houses (new with the Frontier)
- **What:** an estate's streets are laid out, named and sometimes gated before anyone builds. The plots sit empty, fenced or bush, sometimes for years.
- **How it's measured:** 500 m cells with drivable streets (over 3 km per km²) but no mapped buildings (under 3% cover), and less than 25% built-up land in ESA WorldCover. The WorldCover test keeps out cells that are only untraced.
- **Where:**
  - the Lekki peninsula (the Frontier's study): 11.6% of the street cells, the most of any area (3.6788, 6.4406 by Awoyaya)
  - Amuwo Odofin round Festac: 8.6%
  - Water Town's study: 4.2%; the Bazaar's: 3.7%
  - Badagry's eastern strip (the Border's study): 7.8%
  - the dense districts: none
- **Suits:**
  - **the Frontier:** built as whole blocks laid out and almost empty (`vacant_blocks`)
  - **the Border** and **Old Shore** (the other edges of the city)
- **Also in the peninsula's real data:**
  - **the longest expressway stretch with no way across on foot:** 27.5 km (3.7597, 6.4762), more than twice the Bazaar's 12 km
  - **unpaved estate roads** (70% of the tagged streets)
  - **half-built houses:** 1.7% tagged under construction (3.6659, 6.4452), about Railside's level

### Also noted: old Ikorodu (Old Shore's study)
- **In its real data:** bus stops crowded onto the expressway through town (7 on 12 km, 3.4760, 6.6193); markets on the carriageway (2 of its 3, 3.5017, 6.6148); homes in the lagoon-edge wetland (33 buildings, 3.4875, 6.5951); buildings in the road reserve (42 per km²), about Water Town's half.

### 15. Open gutters (new: from the owner, not the data)
- **What:** the owner's description. Open roadside drains, called "gutters" in Lagos:
  - an open concrete U-channel, or dug earth, along the edge of residential streets, often on both sides
  - mostly 40–100 cm wide and up to a metre deep
  - every gate, shop and kiosk crosses it on its own slab, plank, old door or metal sheet; in front of a busy shop it disappears under a run of slabs
  - the water is grey-black and slow or still, full of nylon bags, sachet-water ("pure water") wrappers, bottles and silt, with weeds; it smells and breeds mosquitoes
  - falling into one at night is a classic Lagos misfortune
- **On main roads** the drains are mostly covered by slabs under the walkway, or run as bigger channels set back from the road. Main roads don't read as "gutter streets"; side streets do.
- **Flooding:** rain runs from the gutters into bigger channels, then the canals and the lagoon. When refuse and silt block the gutters, the street becomes the drain. With low ground near the lagoon, that is the classic Lagos flood (ism 10).
- **Not measurable from OSM:** under 1.5% of streets in every studied area have a drain mapped beside them, though nearly every Lagos side street has one. OSM maps the bigger channels, not the gutters. Rates come from the owner's knowledge and the street research.
- **Already in the 3D kit:** `blender/generate.py` draws open drains along road edges with slab covers, rubbish and green water. The share covered and the rubbish come from the district's character (`blender/gidi_kit/rules.py` STREET). Built into the map data and the 2D map on 15 Oct 2026 (`scripts/isms.py`, schema in `docs/ISMS-BUILD.md`); the kit still draws its own.
- **Suits:** every residential district; most of all the dense, waterfront and old-island characters (the Maze, Jungle City, Food Gate, Water Town, Old Island, Railside). Mostly covered in the Estate and the Heights.

## Per district: what to add in the "feel like Lagos" pass
| Gidi district | Strongest isms in its real inspiration |
|---|---|---|
| The Maze | streets ending at the rail and the canal; buildings in the road reserve; houses on the canal bank |
| The Hub | bus stops on the expressway; the market under the bridge on the carriageway; unfinished buildings |
| Jungle City | buildings in wetland (flood days); buildings in the road reserve; the market on the expressway |
| Food Gate | streets ending at drains; houses on drain banks; the market in the carriageway; bus stops on Northern Road |
| Water Town | houses on the channels (the land fringe too); low ground |
| The Capital | missing links (walled compounds); acute junctions; long stretches of expressway with no crossing |
| The Bazaar | the expressway with nowhere to cross; the market on the carriageway; unfinished plazas |
| The Port | acute junctions; wetland at the homes' edge; streets ending at the port rail |
| Railside | one road doing every job (side streets every ~100 m, the market on it); unfinished buildings (4%); streets ending at the line |
| The Estate | missing links where estates meet wall to wall; streets ending at the valley streams; a gate on a close off the main road (gates themselves are built) |
| Old Island | one-way streets (40%); flooding (97% of the land below 3 m); the expressway ring and its slip roads; markets on the carriageway |
| The Border | the expressway with no way across on foot for 25.7 km; lagoon wetland behind the beach (122 ha in the coastal box); little else is mapped |
| Old Shore | bus stops on the expressway through town; markets on the carriageway; homes in the lagoon wetland |
| The Frontier | streets ahead of houses (12% of street cells); the expressway with nowhere to cross for 27.5 km; unpaved estate roads; half-built houses (built) |
| The Heights | one-way streets (40%); missing links where closes meet back to back; streets ending at the lagoon; the expressway with nowhere to cross on foot (gates themselves are built) |

## Log
- **15 Oct 2026:** ism 15 (open gutters) added from the owner's description; OSM doesn't map them.
- **15 Oct 2026:** the Border's study (Badagry LGA's eastern strip, the only part inside the OSM extract) added. Its buildings are almost unmapped, so most counts are unknown.
- **15 Oct 2026:** Old Shore's study (old Ikorodu; Epe is not in the local OSM extract) added. No new ism.
- **14 Oct 2026:** the Frontier's study (Lekki Phase 1, Ajah-Sangotedo, Awoyaya-Lakowe) added, and a new ism measured for every area: streets ahead of houses.
- **14 Oct 2026:** the Heights' study (Ikoyi, Victoria Island, Banana Island; three boxes in Eti Osa) added. No new ism: it tops the gates (6.1 per km²) and missing links (2.7), and ties Lagos Island on one-way streets. The note that the DEM was not on this machine was wrong and is corrected.
- **14 Oct 2026:** Old Island's study (Lagos Island, boxed to the island) added, and a new ism measured for every area: one-way streets.
- **14 Oct 2026:** the Estate's study (Ikeja GRA, Magodo, Omole) added, and a new ism measured for every area: gates across residential streets.
- **14 Oct 2026:** the log started. The backlog for the eight finished districts' studies was measured with `study_isms.py`, plus Railside's study (Agege, Ifako/Ijaye, Alimosho).
