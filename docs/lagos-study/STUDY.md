# How the whole Lagos map works: a study before cutting districts

22 Oct 2026. Read-only. Asked for by the owner's decision "Gidi is Lagos, miniaturised; the map starts again". This is evidence for a later frame proposal. It does not cut districts.

Pictures: `skeleton.png` (roads, whole state and metro), `skeleton_inner.png` (Oshodi to the Island), `character.png` (character of every 250 m cell, LGA lines and names). Council table: `councils.md`.

## Sources, and how each claim is marked

| Mark | Source | Used for |
|---|---|---|
| [OB] | Google Open Buildings v3, all Lagos (`open-buildings-v3/lagos_open_buildings_v3.csv.gz`), confidence >= 0.65. Streamed, gridded to 250 m. 3.60 M buildings in the grid box, 2.52 M inside the 20 LGAs | density, footprint size, big-roof share, building alignment |
| [H] | Google Open Buildings 2.5D Temporal 2023, 48 tiles (`open-buildings-2023/tile_*.tif`), read at ~4 m | mean height, share 4+ storeys (>= 10.5 m), tall cells |
| [OV] | Overture: road segments (all classes, bridge flags, connectors), land use, infrastructure, places | road skeleton, street km, junctions, dead ends, street grid, airport/military/campus/industry |
| [WC] | ESA WorldCover 2021 | water, mangrove, wetland, open land |
| [WP] | WorldPop 2020 constrained | people |
| [G] | Google Earth / Street View notes and screenshots in `~/gidi-data/research/google/{estate,ibudo,maze,twins}` | estate, Oshodi and Mushin grain |
| [R] | earlier 20-LGA research, `~/gidi/docs/lagos-lgas-research.md`, and `results/lga_table.json`, `heights_by_lga.json` | what places are known for; checks |
| [K] | general knowledge of Lagos | names, what a place is like, junction names; not measured |

Checks that passed: the 2.5D mean heights per LGA match the earlier `heights_by_lga.json` to 0.1 m [H]. People per LGA match `lga_table.json` within a few percent [WP].

## The size of the thing

- Lagos State land: **2,916 km²**; water and lagoon another ~760 km² [WC].
- Built up (cells with >= 10% roof): **1,046 km²** [OB].
- The one continuous metro (Agbara to Ajah and Ikorodu, joined): **736 km²**, a box about **81 x 32 km**. It holds 1.71 M buildings, 11.3 M people and 10,900 km of drivable street [OB][WP][OV].
- Everything else is separate towns in bush, farm and swamp: Badagry, Epe, the Lekki-Ibeju strip, Imota, Agbowa [OB][WC].
- Street density in the metro: **14.8 km of street per km²**; up to 24 in Lagos Island [OV].

## 1. The road skeleton

Lagos is a **fan from the Island**. Everything converges on three bridges into Lagos Island and on two big crossings on the mainland (Oshodi and Ojota-Maryland). The lagoon blocks the middle, so east-west movement squeezes into a few corridors. [OV][K]

**Big roads in Overture** (carriageway km, each side of a dual road counted; links and unbuilt roads left out): motorway 221 km, trunk 542, primary 616, secondary 708 [OV].

### The corridors, and what each ties together

| Corridor | Runs | Ties together | Source |
|---|---|---|---|
| Third Mainland Bridge | Oworonshoki / Ebute Metta to Adeniji Adele, Lagos Island, ~11.8 km over the lagoon | the north mainland (Gbagada, Ikorodu Road) to the Island | [OV][K] |
| Carter and Eko Bridges, Ijora Causeway | Iddo / Ijora / Costain to the Island | the old mainland and the port to the Island | [OV] |
| Ikorodu Road | Jibowu (Yaba) - Fadeyi - Onipanu - Anthony - Maryland - Ojota - Ketu - Mile 12 - Ikorodu | the main north-east spine; BRT; the food market at Mile 12 | [OV][K] |
| Lagos-Ibadan Expressway | Ojota / Alausa toll gate - Berger - Ogun State | the way out north; motor parks at Berger and Ojota | [OV][K] |
| Agege Motor Road, then Lagos-Abeokuta Expressway | Idi-Oro (Mushin) - Mushin - Oshodi - Ikeja Along - Iyana Ipaja - Abule Egba - Sango | the north-west spine, beside the rail | [OV][G] |
| Apapa-Oshodi Expressway, then Oshodi-Oworonshoki Expressway (Overture: one "Apapa-Oworonshoki Expressway") | Apapa - Ijora - Orile - Mile 2 - Cele - Isolo - Oshodi - Anthony - Gbagada - Oworonshoki | the inner ring road of the mainland; trucks from the port | [OV][G] |
| Lagos-Badagry Expressway (with the Blue Line) | Eko Bridge / Ijora - Orile - Mile 2 - Festac - Trade Fair - Alaba - Okokomaiko - Agbara - Badagry - Seme | the whole west, out to the border | [OV][K] |
| Western Avenue / Funsho Williams, Herbert Macaulay, Murtala Muhammed | Eko Bridge - Iponri - Ojuelegba; Iddo - Oyingbo - Yaba | the old mainland's inner streets to the bridges | [OV] |
| Mobolaji Bank-Anthony Way, Obafemi Awolowo Way, Airport Road | Maryland - Ikeja - Alausa; Oshodi - airport | the capital and the airport | [OV] |
| Ikotun-Egbe, Idimu, Egbeda, LASU-Isheri roads | Alimosho's own ring of market roundabouts | the west sprawl to Oshodi and Ojo | [OV] |
| Ozumba Mbadiwe, Lekki-Epe Expressway | VI - Lekki toll - Lekki Phase 1 - Ikota - Ajah - Sangotedo - Lakowe - Epe | the whole peninsula; the only road east (128 km of carriageway in Overture) | [OV] |
| Ikorodu-Sagamu, Ikorodu-Itoikin-Epe | Ikorodu north and east | Ikorodu to Ogun and Epe | [OV] |

**Rail** [OV][K]: the old Lagos-Kano line (Iddo - Ebute Metta - Yaba - Mushin - Oshodi - Ikeja - Agege - Ifako - Ijoko), with the Red Line metro on the same corridor; the Lagos-Ibadan standard gauge (Ebute Metta to Agege and north); the Blue Line (Marina to Mile 2, along the Badagry road). The rail runs in one straight line through the market towns: Yaba, Mushin, Oshodi, Agege all grew on it.

**Ferries** [OV][K]: Overture has 102 water routes. They fan from the Island's waterfront (CMS / Marina, Ebute Ero, Falomo, Five Cowries) to Ikorodu, Ebute (Ikorodu), Mile 2, Badagry creek, Oworonshoki and Epe. Water is a second network across the lagoon.

**Bridges and flyovers**: Overture flags 345 km of road segments that hold a bridge [OV]. Lagos is stacked: the island bridges, flyovers at Ojota, Maryland, Ikeja, Oshodi, Mile 2, Costain, Obalende, Ajah, and the cloverleaves at Ojota and Mile 2 (`skeleton_inner.png`).

**Roads drawn in Overture that may not exist yet** (dashed grey in the pictures): Fourth Mainland Bridge, Lagoon Highway, 7th Axial Road, Third Axial Road, Lagos-Calabar Coastal Highway, Lekki Regional Road, Omu Creek Road. Some are under construction, some only planned. To check on Google Earth before trusting.

### The main junctions [K, positions approximate; road layout OV]

| Junction | What meets there | Why it matters |
|---|---|---|
| **Oshodi** | Apapa-Oshodi Expressway x Agege Motor Road x rail x Airport Road | the place every route passes; terminals 1-3, market under the bridge [G] |
| **Ojota** | Ikorodu Road x start of Lagos-Ibadan Expressway; cloverleaf | the gate to the north; motor park, Gani Fawehinmi park |
| **Maryland** | Ikorodu Road x Mobolaji Bank-Anthony (to Ikeja) | the turn for the capital; flyover |
| **Anthony** | Ikorodu Road x Oshodi-Oworonshoki Expressway | the mainland's inner ring meets the north spine |
| **Ikeja Along** | Agege Motor Road becomes Lagos-Abeokuta Expressway; Ikeja and Egbeda roads | the north-west gate |
| **Berger** | Lagos-Ibadan Expressway x Ojodu / Omole / Isheri roads | interstate motor park; edge of the estate belt |
| **Mile 2** | Lagos-Badagry x Apapa-Oshodi Expressway | tankers and trailers, the west gate, Blue Line |
| **Costain** | Western Avenue x Eko Bridge x Ijora x Apapa Road | the old mainland's knot to the bridges |
| **Obalende** | Third Mainland and Eko bridgeheads, Ikoyi | the biggest motor park on the Island side, under the bridge |
| **CMS** | Marina x Carter Bridge, bus terminal, ferry | the Island's front door |
| **Lekki toll (Admiralty)** | VI and Ikoyi link bridge into the Lekki-Epe Expressway | the gate to the peninsula |
| Others | Ojuelegba (rail, Western Avenue, Ikorodu Road side), Iyana Ipaja, Abule Egba, Ikotun roundabout, Ketu / Mile 12, Iddo / Otto, Cele, Ijora, Ajah roundabout, Ikorodu garage | each a market and motor park |

**How the network behaves** [OV][K]:
- The mainland is a **grid of a few spines** (Ikorodu Road, Agege Motor Road, the expressway ring, the Badagry road) with dense fabric between them; side streets come straight onto the spines every 80-120 m [G].
- The whole flow narrows to **the bridges**. The Island side (Ikoyi, VI, Lekki) depends on them and on one road east.
- **Junctions are places**: every major junction is a market, a motor park and a flyover together (Oshodi, Ojota, Mile 2, Obalende, Iyana Ipaja, Ikotun) [G][K].

## 2. The character map

Every 250 m cell in the state is put in one of 17 classes from its own measurements (smoothed over 750 m). Rules, in order (the first that fits wins) [OB][H][OV][WC]:

1. water (WorldCover water, almost no buildings)
2. airport, military, campus (Overture land use or airport aprons, if not densely built over)
3. port & tank farm: >= 35% of roof in buildings >= 1,000 m², within 1 km of water
4. industry & warehouses: >= 28% of roof in buildings >= 1,000 m²
5. open land / swamp: < 3% roof
6. scattered new build: 3-10% roof
7. waterfront & stilts: within 600 m of water, mean footprint < 110 m², > 2,400 buildings/km²
8. towers & mid-rise: >= 6% of built pixels 20 m+, or mean height >= 9 m with >= 30% at 4+ storeys
9. low-density villa & new estate: < 1,300 buildings/km² with mean footprint >= 165 m²
10. planned or surveyed grid: regularity >= 0.70 (street directions and building directions both lined up)
11. dense grid tenement: regular, >= 42% roof
12. dense inner core: >= 40% roof or >= 2,800 buildings/km², mean height >= 5.4 m
13. dense outer sprawl: as 12 but lower (mostly bungalows)
14. suburban bungalow belt: everything else that is built (10-40% roof, organic)

### What each class is, measured

| Class | km² | Bldg/km² | Mean footprint m² | Street km/km² | Junctions/km² | Mean height m | People/km² |
|---|---|---|---|---|---|---|---|
| waterfront & stilts | 8 | 4,809 | 69 | 10.8 | 48 | 5.3 | 11,542 |
| dense inner core | 76 | 3,402 | 137 | 18.0 | 95 | 5.9 | 29,361 |
| dense outer sprawl | 142 | 3,612 | 110 | 16.9 | 91 | 4.8 | 18,116 |
| dense grid tenement | 26 | 3,312 | 148 | 17.2 | 84 | 5.7 | 30,767 |
| planned or surveyed grid | 241 | 2,040 | 125 | 14.3 | 67 | 5.0 | 7,912 |
| suburban bungalow belt | 443 | 1,853 | 119 | 12.8 | 62 | 4.6 | 7,089 |
| towers & mid-rise | 12 | 1,354 | 171 | 18.1 | 65 | 10.2 | 7,658 |
| low-density villa & new estate | 29 | 808 | 212 | 13.7 | 54 | 6.3 | 4,831 |
| industry & warehouses | 52 | 1,005 | 266 | 13.2 | 29 | 8.8 | 18,077 |
| port & tank farm | 10 | 731 | 263 | 11.4 | 27 | 10.0 | 11,977 |
| airport | 12 | 366 | 174 | 5.4 | 9 | 7.1 | n/a |
| military & barracks | 17 | 652 | 193 | 9.6 | 26 | 5.0 | n/a |
| campus | 8 | 578 | 170 | 9.1 | 20 | 6.4 | n/a |
| scattered new build | 312 | 471 | 107 | 5.0 | 15 | 4.2 | 2,433 |
| open land, swamp | 1,555 | 12-34 | n/a | 0.2-1.0 | ~1 | n/a | ~300 |

Figures from [OB][H][OV][WP]; class rules as above. The numbers per cell are in `feat.npz` / `class.npz` in this folder.

**What jumps out:**
- **Lagos is low.** Outside the Island side, mean heights are 4-7 m: bungalows and two-storey houses. Only 12 km² is towers (Ikoyi, VI, Banana Island, Marina) [H].
- **Small houses, packed.** A typical house roof is 100-150 m². Dense areas hold 3,300-3,700 buildings per km² and ~17-18 km of street per km² [OB][OV].
- **The density gradient is a ring, not a peak.** The densest people (50-70,000/km²) are in Ajegunle, Oshodi-Mafoluku and Mushin, not on the Island [WP].
- **Planned and organic sit side by side.** Festac, Lekki Phase 1, Ikeja GRA, Ebute Metta, Ajegunle all read as grids (alignment 0.88-0.98); Mushin, Isale Eko, Ikorodu town, Epe and Bariga as organic (0.33-0.46) [OB][OV][G].
- **Industry is in belts along the expressways and rail**, not spread: Ikeja-Ogba-Oregun (12.8 km²), Ilupeju-Isolo-Mushin (9.3), Iganmu-Orile-Ijora, Apapa-Tin Can-Kirikiri, Ogijo, and the refinery at the far east [OB].

### The character zones (contiguous, >= 1 km², named by the places inside them)

From the class map, smoothed (5 x 5 majority) and joined into contiguous areas [OB][H][OV]; names inside each zone are [K].

**Dense cores**
- **Central dense core**: Ojuelegba, Aguda, Ijesha, Itire, Lawanson, Mushin, Idi-Araba, Ladipo, Ilupeju, Isolo edge. 34.8 km², 3,240 bldg/km², 148 m² roofs, mean 5.9 m, 31,800 people/km². One continuous zone across Surulere, Mushin and Shomolu.
- **Oshodi-Mafoluku**: 5.1 km², 70,000 people/km² (the peak in Lagos).
- **North rail-town core**: Agege, Ogba, Iju, Abule Egba, Ifako. 14.7 km², 3,490 bldg/km².
- **Egbeda-Akowonjo-Iyana Ipaja**: 9.9 km².
- **Ketu-Ikosi**: 5 km².
- **Lagos Island core** (Isale Eko, Idumota, Balogun): under-read by the data (see limits), but the street density (23.7 km/km²) is the highest in Lagos [OV].

**Dense grid tenement**
- **Ajegunle** (Ajeromi-Ifelodun): 5.9 km², 61,000 people/km², building alignment 0.92. Regular streets, crowded houses.

**Dense outer sprawl (bungalows)**
- **North-west sprawl**: Iyana Ipaja, Alagbado, Ojokoro, Abule Egba, Agege edge. 51 km² in one piece, 3,690 bldg/km², 106 m² roofs, 4.8 m.
- **Ikotun-Igando**: 21.6 km²; **Egbe-Ejigbo**: 15.1 km²; **Ipaja-Ayobo-Idimu**: 13 km².
- **Alaba-Okokomaiko** (4.8), **Iba** (3.8), **Bariga** (4.1), **Ikorodu town** (2.9).

**Planned or surveyed grids**
- **Festac belt**: Festac, Amuwo, Satellite Town, Mile 2, Trade Fair. 25.9 km², grid 0.85.
- **Lekki Phase 1 belt**: Oniru, Lekki Phase 1, Ikate, Osapa, Agungi. 28.1 km², grid 0.88, mean 6.6 m.
- **Okota / Ago Palace / Isolo south**: 26.4 km², grid 0.82.
- **Ikeja GRA**: 4.6 km², grid 0.79.
- **Ebute Metta / Oyingbo / Yaba railway grid**: 2.4 km², grid 0.83.
- **East Lekki layouts** (Ikota to Sangotedo): 9.8 + 8.8 km².
- **Surveyed layouts at the edges**: Ijanikin, Iba, Ipaja, Noforija, Ikorodu edges, Ibeju (2-9 km² each). These are private grids of plots, not estates in the GRA sense.

**Bungalow belts (the in-between)**
- **Ikorodu**: 139 km² in one piece, 1,855 bldg/km², 4.3 m. The biggest single zone in Lagos.
- **Ketu-Ojota-Gbagada-Anthony-Maryland**: 17.7 km².
- **Mile 12-Omole-Ojodu-Berger-Alausa (the north estate belt)**: 19.5 km². Magodo and Omole are planned [G], but their streets bend with the land, so they score 0.38-0.69 on regularity and land here (see limits).
- **Ojo corridor**: Isheri-Olofin, Okokomaiko, LASU, Alaba, Iba: 23.5 km². **Badagry corridor**: Agbara-Morogbo 27.1 km², Badagry town 9.9 km².
- **East Lekki**: Badore 18.4 km², Sangotedo 12 km², Awoyaya-Lakowe 12.1 km². **Epe town**: 12.6 km².
- **Inner pieces**: Yaba-Jibowu (5.2), Surulere-Ebute Metta-Costain (6.7), Allen-Computer Village-Oregun (5.9), Apapa GRA-Olodi (4.9), Obalende (7.1).

**Towers & mid-rise**
- **Ikoyi-VI-Banana Island**: 10.2 km², 10 m mean, 20% at 4+ storeys.
- **Marina-Broad Street**: 1.2 km², 13.1 m mean, 37% at 4+.

**Villa and new estate**
- **Ikota-VGC** (5.6 km²), **Ajah-Abraham Adesanya** (4.6), east of Sangotedo (2.1): 670-880 bldg/km², 185-205 m² roofs.

**Industry, port and tank farms**
- **Ikeja industrial estate** (Ogba, Oregun, Agidingbi, Alausa): 12.8 km², 48% of roof in big buildings, 27% at 4+.
- **Ilupeju-Isolo-Papa Ajao-Ladipo**: 9.3 km².
- **Mile 2-Orile-Kirikiri strip**: 5.5 km²; **Iganmu-Ijora**: 2.4 km²; **Ogijo / Sagamu Road** (Ikorodu): 5.7 km²; **Trade Fair west**: 2.6 km².
- **Ports**: Apapa wharf 3.6 km², Tin Can / Kirikiri 1.9 km², Ijora-Otto 1.2 km².
- **Dangote refinery and Lekki FTZ**: 5.6 km² at 11.8 m mean height (the tallest outer-Lagos zone), plus a 2.1 km² industry block with 1,030 m² mean footprints.

**Waterfront & stilts**
- **Makoko**: 1.6 km², 6,400 bldg/km², 50 m² roofs.
- A 1.1 km² zone at 6.430, 3.378 (south Apapa shore), not yet identified.
- Ilaje-Bariga, Oworonshoki and Ago Egun lie in this kind of place but read as dense core or sprawl: the cells are mixed.

**Institutions**
- **Airport** (Ikeja/Oshodi): 14 km². **Ojo cantonment**: 11.6 km²; **Navy Town / Ojo**: 3.4 km²; **Ikeja Cantonment**: 1.9 km². **UNILAG**: 2.5 km²; **LASU Ojo**: 1.9 km²; **LASUSTECH Ikorodu**: 2.1 km².

## 3. Councils

The 20 LGAs and 37 LCDAs, with measured numbers, zones, features, roads and neighbours, are in `councils.md`. In one line: **the councils don't follow character.** Alimosho's five LCDAs all sit in one sprawl; Eti-Osa runs from tower blocks to bush; the central dense core spreads over three LGAs [OB][K].

## 4. Natural groupings (evidence for the frame, not the frame)

The test for each place: is its character distinct, does it have its own hubs (market, motor park, landmark), and does it join its neighbours on the real road skeleton? Places that share a measured character and touch merge; places with their own character and hubs stand alone; long stretches of the same fabric get squeezed hard.

### Rich and distinct enough to stand alone

| Group | Places | Why (evidence) |
|---|---|---|
| **The Island** | Isale Eko, Idumota, Balogun, Marina, Broad St, CMS, Onikan, Obalende | towers (13 m) on the waterfront, the densest streets in Lagos (23.7 km/km²) behind; markets, palace, Brazilian quarter, CMS, Obalende park [H][OV][K] |
| **Ikoyi-VI** | Ikoyi, Banana Island, VI, Oniru edge, Eko Atlantic | the only big tower zone (10.2 km², 10 m mean, 20% 4+); embassies, offices, beach, Falomo [H][K] |
| **Oshodi** | Oshodi, Mafoluku, Arena, the interchange, airport's south edge | the peak of crowding (70,000/km²), the meeting of the ring road, the north-west spine and the rail; terminals and market [WP][OV][G] |
| **Old railway mainland** | Ebute Metta, Oyingbo, Otto, Iddo, Yaba, Sabo, Makoko, Costain | a 2.4 km² grid (0.83) beside the stilt town (6,400 bldg/km²) and the tank strip; Iddo terminus, Oyingbo and Tejuosho markets, UNILAG next door, all three island bridges land here [OB][OV][K] |
| **Ajegunle with the port** | Apapa wharf, Tin Can, Ijora, Kirikiri, Ajegunle, Olodi | the port and tank farms (big roofs, 37% 4+) against the densest grid tenement (61,000/km²); the trucks and the people are one story [OB][H][WP] |
| **Ikeja** | Alausa, Ikeja GRA, Allen, Computer Village, the industrial estate, the airport | the capital: a planned GRA (0.79), the biggest industrial zone (12.8 km²), the airport (14 km²), the phone market; heights second only to the Island [OB][OV][H] |

### Neighbours that share a character and could merge

| Group | Places | Shared character (evidence) |
|---|---|---|
| **The central dense core** | Ojuelegba, Surulere, Aguda, Ijesha, Itire, Lawanson, Mushin, Idi-Araba, Ladipo, Papa Ajao, Ilupeju | one continuous 34.8 km² dense inner core (3,240 bldg/km², 5.9 m), with the Ilupeju-Isolo industry belt (9.3 km²) on its north edge [OB][H]. Too big for one district at any scale with houses at real size; it may be one character split in two (Surulere's stadium-and-Ojuelegba south; Mushin's Ladipo-and-Idi-Araba north) |
| **Shomolu-Bariga-Akoka-Gbagada** | Shomolu, Pedro, Palmgrove, Bariga, Akoka, UNILAG, Gbagada, Oworonshoki | dense core and Bariga sprawl (4,000 bldg/km²) on the lagoon edge, with the campus; the print quarter; Third Mainland at its back [OB][K] |
| **The Ikorodu Road belt** | Anthony, Maryland, Ojota, Ketu, Mile 12, Ikosi, Gbagada west | a 17.7 km² bungalow belt plus the Ketu dense core (5 km²), all strung on Ikorodu Road; Mile 12 market and Ojota park as hubs [OB][OV][K] |
| **The north estate belt** | Magodo, Omole, Ojodu, Berger, Isheri, Alausa edge, Ogba residential | the 19.5 km² Mile 12-Omole-Berger belt; planned estates walled off the expressway with one or two gates [G]. This is the owner's example: Omole alone is a pattern, the belt is the district |
| **The north rail towns** | Agege, Pen Cinema, Ogba north, Ifako, Iju, Abule Egba | a 14.7 km² dense core plus the north edge of the 51 km² sprawl; the rail, Agege bread and abattoir, Abule Egba junction [OB][R] |
| **Festac belt** | Festac, Amuwo, Satellite Town, Mile 2, Trade Fair, Kirikiri edge | the largest planned grid (25.9 km², 0.85); Mile 2 hub and Trade Fair market at its corners [OB][OV] |
| **Okota-Isolo-Ejigbo** | Okota, Ago Palace, Isolo, Ejigbo, Ilasamaja, Cele | a 26.4 km² surveyed grid (0.82) and the Egbe-Ejigbo sprawl, between Oshodi and Festac [OB] |
| **Lekki Phase 1 to Ajah** | Lekki toll, Lekki Phase 1, Oniru, Ikate, Osapa, Agungi, Jakande, Ikota, VGC, Chevron, Ajah | the 28 km² planned belt (0.88) and the villa belt (10 km²); one road (Lekki-Epe) with the toll at one end and Ajah roundabout at the other [OB][OV] |
| **Ojo-Alaba corridor** | Alaba, Okokomaiko, LASU, Ojo barracks, Iba, Ijanikin, Igbo-Elerin | a 23.5 km² bungalow belt with the barracks (11.6 km²) and campus; Alaba market the hub; Badagry road its spine [OB][OV] |

### Sparse or repetitive: squeeze hard

| Stretch | Size | What to keep |
|---|---|---|
| **Alimosho sprawl** (Iyana Ipaja, Ipaja, Ayobo, Egbeda, Idimu, Ikotun, Igando, Egbe) | ~100 km² of dense bungalow sprawl in 4 contiguous zones; mean height 4.8 m, 0.6% 4+ [OB][H] | it is the same fabric everywhere: keep the market roundabouts (Iyana Ipaja, Ikotun, Egbeda, Idimu), the landfill, LASU-Isheri road; one district of it |
| **Ikorodu** | 139 km² single bungalow zone, 4.3 m [OB][H] | the town core and garage, Sabo market, ferry terminal, Ogijo industry; one district, very compressed |
| **East Lekki to Ibeju** (Sangotedo, Awoyaya, Lakowe, Eleko, Ibeju) | 300+ km² of open land with 2-18 km² layouts strung on one road [OB][WC] | a drive, a few layouts, the beach, the refinery and port at the end |
| **Epe** | 691 km² open land; a 12.6 km² town [OB][WC] | the lagoon town and fish market as a far place; reachable by road and ferry |
| **Badagry and Agbara** | 184 km² open land, 51 km² swamp; Agbara 27 km² bungalow belt [OB][WC] | the old town, the slave-route sites (handled carefully), the border road, Agbara industry |
| **Creeks and swamps** | 204 km² mangrove and swamp [WC] | the water layer: stilt villages, creeks, boats; no streets |

### Water as its own thing
Makoko, Ilaje-Bariga, Oworonshoki, Ago Egun, Otto, Ijora Badia, Itedo / Ilado and the creek villages are all **waterfront & stilts** or mixed edge cells [OB]. They belong to the districts they touch, but the lagoon itself, with its ferry routes from the Island, behaves like one shared space [OV].

### What the evidence says about counts (not a decision)
- Places that stand alone: about **6**.
- Merged groups on the core mainland: about **8-9**.
- Squeezed outer stretches: about **5**, plus the lagoon.
- That makes roughly **18-20 candidate groups** before any are dropped or joined. The data doesn't fix the number; the owner does.

## 5. Scale: Lagos's metro against a game map

The metro (the one continuous built-up area): **81 x 32 km box, 736 km² built**, 10,900 km of drivable street, 1.71 M buildings [OB][OV].
The arterial skeleton (motorway, trunk, primary, secondary, real lines, no links) is ~790 km of road counted once (Overture counts dual roads twice; this halves motorway and trunk) [OV].

**Houses stay real size**, so a Gidi block holds what a real block holds. The street density stays about the real 14.8 km/km², and the number of streets falls with the square of the scale. The skeleton shrinks with the scale itself (a road 10 km long becomes 10/N km), so it takes a bigger share of the smaller budget.

| Scale | Gidi box (km) | Gidi built area (km²) | Street km that fit | Skeleton (km) | Local streets left (km) | Share of real local streets kept | Buildings that fit |
|---|---|---|---|---|---|---|---|
| 1:3 | 27 x 10.5 | 82 | 1,210 | 263 | 950 | **9.4%** (1 in 11) | ~190,000 |
| 1:4 | 20 x 7.9 | 46 | 680 | 198 | 480 | **4.8%** (1 in 21) | ~107,000 |
| 1:5 | 16 x 6.3 | 29 | 440 | 158 | 280 | **2.8%** (1 in 36) | ~68,000 |
| 1:6 | 13.5 x 5.3 | 20 | 300 | 132 | 170 | **1.7%** (1 in 59) | ~48,000 |

What it means:
- **Big game maps** (GTA V and Red Dead 2 are often quoted at roughly 75-80 km² including water and wild land [K]) are about the size of Gidi's metro at 1:3 to 1:4.
- At **1:4**, a whole LGA like Mushin (18 km²) becomes about 1.1 km²: a handful of streets around Ladipo and Idi-Araba. Alimosho (154 km² built) becomes ~9.6 km², but its fabric is repetitive, so it can take far less.
- At **1:5 or 1:6**, only the skeleton and the hubs survive in most places: one or two streets per neighbourhood. The skeleton eats 36-43% of the street budget.
- Building counts are the hard limit on the laptop: even 1:6 means ~48,000 houses. Most must be cheap (instanced, low detail) and only the hero places finished by hand.
- Shrinking need not be even: the owner's rule (fewer streets, never smaller houses) allows the repetitive belts (Alimosho, Ikorodu, east Lekki) to shrink more, and the rich places (the Island, Oshodi, the old railway mainland) less. A single number is the average, not the rule.

## Limits of this study

- **Joined roofs are under-counted.** In Lagos Island's core, VI and parts of Mushin, Open Buildings merges touching roofs into bigger shapes: Lagos Island reads at only 2,200 bldg/km² while its streets are the densest in Lagos. Cover and density there are floors, not counts [OB].
- **Bent planned estates read as organic.** The regularity measure looks for one grid direction per 750 m. Magodo and Omole bend with the land (0.38-0.69); the Google study shows they are planned [G]. A street-relative measure would fix this.
- **Heights on water are suspect.** Makoko reads 7.8 m mean with 19% at 4+ storeys: stilt houses over water confuse the 2.5D model [H].
- **"Planned or surveyed grid"** mixes true estates (Festac, Lekki Phase 1, Ikeja GRA) with private surveyed plot layouts at the edges (Ikorodu, Ibeju, Ojo). The measure can't tell them apart; gates and walls can [G].
- **The LGA polygons are rough** (Lagos Island takes in the lagoon; Amuwo-Odofin reaches inland), so LGA sums are approximate [OV].
- **Junction and neighbourhood positions** are from knowledge, good to about 0.5-1 km [K]. Overture places are too noisy to place markets (e.g. a "Ladipo Auto Market" pin in Apapa) [OV].
- **Overture double-counts dual carriageways** and holds planned roads (listed above).
- WorldPop is a model; it spreads people by building presence [WP].

## Picture studies to settle what the data can't

For the browser pass (Google Earth top-down, 3D tilt, Street View). Coordinates are approximate (lat, lon).

| # | Place | Lat, lon | View | What to look for |
|---|---|---|---|---|
| 1 | Isale Eko / Idumota | 6.4590, 3.3870 | top + tilt | real building count per block (data merges roofs), heights, how much of each street the market takes |
| 2 | Victoria Island, Adeola Odeku | 6.4300, 3.4180 | top + tilt | offices vs villas vs towers; data calls it a bungalow belt |
| 3 | Banana Island | 6.4560, 3.4470 | top + tilt | plot size, tower count; reads as bungalow belt |
| 4 | Makoko | 6.4970, 3.3880 | top + tilt + water edge | how far the stilts reach into the lagoon (not all in the buildings data); real heights (data says 7.8 m) |
| 5 | Unknown waterfront zone, south Apapa shore | 6.4298, 3.3784 | top | what this 1.1 km² dense small-roof zone is |
| 6 | Magodo | 6.6150, 3.3850 | top | estate edge, gates, how streets bend, where it meets the bush valley |
| 7 | Omole / Ojodu / Berger | 6.6380, 3.3650 | top | the estate belt's gates onto the expressway; Berger motor park |
| 8 | Ojota interchange and park | 6.5860, 3.3800 | top + tilt | the cloverleaf, motor park, Gani Fawehinmi park, chemical market |
| 9 | Maryland | 6.5710, 3.3670 | top + Street View | flyover, bus stops, mall |
| 10 | Ikeja Along | 6.6040, 3.3250 | top + Street View | where Agege Motor Road becomes the expressway; market |
| 11 | Mile 2 | 6.4640, 3.3140 | top + tilt | cloverleaf, tanker parks, Blue Line station |
| 12 | Costain | 6.4930, 3.3720 | top | the knot of Western Avenue, Eko Bridge, Ijora |
| 13 | Obalende | 6.4480, 3.4040 | top + Street View | motor park under the bridge |
| 14 | CMS / Marina | 6.4530, 3.3920 | top + Street View | bus terminal, ferry jetty, Carter Bridge landing |
| 15 | Lekki toll / Admiralty | 6.4370, 3.4360 | top | the toll plaza, link bridge, circle |
| 16 | Ajegunle | 6.4550, 3.3330 | top + Street View | confirm the regular grid (alignment 0.92); canal edge; house type |
| 17 | Mile 12 market | 6.6080, 3.3990 | top + tilt | market size, truck yards |
| 18 | Ikeja industrial estate | 6.6100, 3.3530 | top + tilt | factories vs warehouses vs offices in the big roofs |
| 19 | Alaba market | 6.4600, 3.1900 | top + tilt | market blocks, plazas, how it meets the Badagry road |
| 20 | Trade Fair | 6.4650, 3.2550 | top | the complex, ASPAMDA, BBA |
| 21 | Fourth Mainland Bridge / Lagoon Highway line | 6.4800, 3.5000 | top (latest imagery) | built, under construction or only planned? |
| 22 | Lagos-Calabar Coastal Highway | 6.4250, 3.5200 | top (latest imagery) | built length as of now |
| 23 | Ikorodu town, garage and jetty | 6.6170, 3.5080 | top + Street View | the core's grain, motor park, ferry |
| 24 | Ikotun roundabout | 6.5500, 3.2650 | top + Street View | Alimosho's typical market roundabout and street grain |
| 25 | Dangote refinery | 6.4300, 4.0000 | top | scale of the plant, the port next to it |
| 26 | Epe fish market | 6.5850, 3.9830 | top + Street View | jetty, market, town core |
| 27 | Badagry town | 6.4180, 2.8850 | top + Street View | old town, marina, heritage sites |
| 28 | Otto / Iddo tank strip | 6.4720, 3.3830 | top | is it tank farm, depot or rail yard? |
| 29 | Ijora Badia | 6.4680, 3.3680 | top + Street View | the informal settlement by the rail and causeway |
| 30 | Agege rail market / Pen Cinema | 6.6230, 3.3240 | top + Street View | market on the tracks, the flyover |
| 31 | Oworonshoki waterfront | 6.5550, 3.4050 | top | stilts and the Third Mainland landing |
| 32 | Iganmu / Orile industry | 6.4797, 3.3601 | top | National Theatre, factories, the expressway knot |

## Files

**24 Oct: only the `.md` and `.png` files were committed.** The numbers, grids and scripts below are not on the Mac
any more, so this study can't be rebuilt; its results stand as written.

- `STUDY.md`, `councils.md`, `skeleton.png`, `skeleton_inner.png`, `character.png`
- Numbers: `lga_stats.json` (per LGA), `zones.json` (every contiguous zone >= 1 km²), `feat.npz` / `class.npz` / `hgrid.npz` / `bgrid65.npz` / `rgrid.npz` / `ogrid.npz` (per-cell grids)
- Scripts: `grid_bld.py` (buildings), `grid_orient.py` (building directions), `heights.py` (2.5D), `roads.py`, `rasters.py`, `feat.py`, `classify.py`, `plots.py`, `gaz.py` (knowledge place list)
