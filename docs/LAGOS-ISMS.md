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
- **The 30 m Copernicus DEM is not on this machine.** Low ground comes from each LGA's share of land below 3 m and 5 m (`data/results/lga_table.json`, made from that DEM) and from mapped wetland.

## The numbers (per km² of each study area, unless it says otherwise)

| | Maze (Mushin + Shomolu) | Hub (Oshodi + Surulere) | Jungle (Ajegunle) | Festac (Amuwo Odofin) | Food Gate (Kosofe corridor) | Water Town (Makoko–Bariga) | Capital (central Ikeja) | Ikeja (whole) | Bazaar (Ojo market) | Port (Apapa) | Railside (Agege, Ifako, Alimosho) | Estate (Ikeja GRA, Magodo, Omole) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Area studied, km² | 34 | 65 | 12 | 135 | 19 | 7 | 16 | 49 | 22 | 27 | 215 | 24 |
| Streets dead-ending at a canal or drain | 1.6 | 0.7 | 0.8 | 0.1 | **2.7** | 1.9 | 0.2 | 0.4 | 0.4 | 0.2 | 0.3 | 1.2 |
| Streets dead-ending at the rail | **0.6** | 0.1 | 0 | 0 | 0 | 0 | 0.2 | 0.1 | 0 | 0.2 | 0.02 | 0 |
| Missing links (two dead ends < 25 m apart) | 1.0 | 1.0 | 0.5 | 0.5 | 1.5 | 1.0 | **2.4** | 2.0 | 0.4 | 0.2 | 0.9 | 1.9 |
| Buildings on a drainage channel or its bank | 3.3 | 1.6 | 2.9 | 0.1 | 6.7 | **48** | 0 | 0.1 | 1.0 | 1.8 | 0.7 | 0.04 |
| Buildings in the road reserve | 102 | 79 | **158** | 22 | 45 | 92 | 9 | 12 | 66 | 54 | 87 | 21 |
| Markets reaching a main road's carriageway | 5 of 7 | 5 of 7 | 3 of 5 | 4 of 7 | 9 of 15 | — | 4 of 8 | 7 of 20 | 3 of 5 | 3 of 5 | 6 of 12 | 5 of 11 |
| Side streets joining main roads, per km | 5.0 | 5.0 | 3.5 | 3.1 | 3.9 | 0.4 | 5.2 | 4.8 | 2.6 | 3.4 | **10.4** | 3.4 |
| Unfinished buildings (tagged), per km² | 9 | 19 | 10 | 15 | 0.2 | 3 | 0 | 1 | 14 | 14 | **79** | 0.6 |
| …as a share of all buildings | 0.6% | 1.1% | 0.4% | 2.8% | 0% | 0.2% | 0% | 0.4% | 1.4% | 1.4% | **4.1%** | 0.1% |
| Junctions where five or more roads meet | 0 | 0.02 | 0 | 0.02 | 0 | 0 | 0.06 | 0.02 | 0 | 0.04 | 0 | 0 |
| Junctions where two roads meet under 25° | 0.4 | 0.5 | 0.2 | 0.2 | 0.6 | 0.6 | **0.8** | 0.6 | 0 | 0.7 | 0.2 | 0.3 |
| Buildings standing in mapped wetland | 0 | 0.1 | **243** | 4.7 | 0.3 | 0 | 0 | 0 | 4.5 | 4.4 | 0 | 0 |
| Land below 3 m (the LGA, from the DEM) | 0–15% | 5–13% | 11% | 44% | 57% | 55% | 0% | 0% | 32% | 48% | 0–5% | 0% (Ikeja), 57% (Kosofe) |
| Expressway and trunk road, km | 63 | 82 | 15 | 48 | 31 | 27 | 27 | 66 | 35 | 30 | 33 | 30 |
| …bus stops on them | 5 | 9 | 0 | 0 | 8 | 0 | 3 | 8 | 0 | 0 | 0 | 1 |
| …longest stretch with no mapped way across on foot | 9.5 km | 5.3 km | 1.6 km | 2.5 km | 3.7 km | 9.5 km* | 9.3 km | 5.3 km | **12.0 km** | 3.5 km | 4.7 km | 5.4 km |
| **Gates across residential streets, per km² (new)** | 2.2 | 1.8 | 0.2 | 2.0 | 3.1 | 1.8 | 2.2 | 3.0 | 0.6 | 0.3 | 2.5 | **5.2** |

\* Water Town's is the long lagoon bridge, where nobody crosses on foot.

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

### 12. Gates across streets (new with the Estate)
- **What:** a gate or barrier across a residential street, with a gateman. Estates, closes and walled streets shut the public road, at least at night.
- **Where:**
  - Ikeja GRA, Magodo and Omole: 5.2 per km² mapped, twice the rate anywhere else (3.3601, 6.6481 in Omole; 3.3925, 6.6029 by Magodo). A median 13 m in from the main road.
  - The rest of Lagos: 0.2–3.1 per km², most in the Kosofe corridor (3.1), Ikeja as a whole (3.0) and Railside's sprawl (2.5).
- **Read with care:** gates are under-mapped everywhere (only 12% of the estates' street entries off a main road show one).
- **Suits:**
  - **the Estate:** built (every estate street gated where it leaves a public road, and the main gate on the road in from the Capital)
  - **Railside** and **Food Gate:** a few gated closes off the main road
  - **the Heights** and **the Frontier** (estates of their own)
- **Also in the Estate's real data:** streets that end at a stream in a valley (1.2 per km², Magodo, 3.3755, 6.6094), and missing links (1.9 per km², Omole's north, 3.3771, 6.6349), where two estates meet wall to wall. Few buildings reach into the road (21 per km², against 79–158 in the dense districts): the walls stand back.

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

## Log
- **14 Oct 2026:** the Estate's study (Ikeja GRA, Magodo, Omole) added, and a new ism measured for every area: gates across residential streets.
- **14 Oct 2026:** the log started. The backlog for the eight finished districts' studies was measured with `study_isms.py`, plus Railside's study (Agege, Ifako/Ijaye, Alimosho).
