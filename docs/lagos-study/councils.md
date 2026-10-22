# Lagos councils: the 20 LGAs and 37 LCDAs

22 Oct 2026. Companion to `STUDY.md`. Read-only study; nothing here is a district yet.

**Sources, marked on every row:**
- **[OB]** Google Open Buildings v3, Lagos (conf >= 0.65; 2.52 M buildings inside the 20 LGA polygons).
- **[H]** Google Open Buildings 2.5D Temporal 2023 heights (48 tiles, read at ~4 m; "4+" = share of built pixels 10.5 m or taller, about 4 storeys and up).
- **[OV]** Overture roads, land use and places.
- **[WP]** WorldPop 2020 (constrained). **[WC]** ESA WorldCover 2021.
- **[G]** the Google Earth / Street View notes already in `~/Real-world/research/google/`.
- **[R]** the earlier 20-LGA research (`~/gidi/docs/lagos-lgas-research.md`).
- **[K]** general knowledge of Lagos (not measured; check before relying on it).

The LGA polygons (`lagos_lgas_utm31.geojson`) are rough: Lagos Island's polygon takes in most of the lagoon, and Amuwo Odofin's reaches far inland. LCDAs have no polygons in the data, so LCDA rows are [K] only.

## The measured table [OB][H][OV][WP]

"Built" = 250 m cells with at least 10% roof cover. Street km/km² = drivable Overture streets over built cells. Grid = how much street length runs in one pair of directions (1.0 = perfect grid; ~0.4 = organic). Align = the same for building long axes.

| LGA | Land km² | Buildings | Bldg/km² (built) | Mean footprint m² | Area in ≥1000 m² roofs | Street km/km² | Grid | Align | Mean height m | 4+ storeys % | People (WP) | People/km² land |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Agege | 11 | 41,592 | 3,697 | 130 | 3% | 18.3 | 0.44 | 0.44 | 5.5 | 2.0 | 350,557 | 31,160 |
| Ajeromi-Ifelodun | 12 | 31,228 | 2,747 | 182 | 8% | 16.0 | 0.64 | 0.72 | 5.7 | 2.8 | 622,832 | 53,577 |
| Alimosho | 178 | 508,769 | 3,267 | 108 | 1% | 16.2 | 0.57 | 0.55 | 4.8 | 0.6 | 2,589,866 | 14,554 |
| Amuwo-Odofin | 105 | 109,935 | 1,979 | 134 | 14% | 14.9 | 0.73 | 0.80 | 6.1 | 7.6 | 868,831 | 8,304 |
| Apapa | 20 | 32,752 | 2,058 | 140 | 18% | 12.5 | 0.56 | 0.60 | 7.2 | 13.7 | 244,429 | 12,494 |
| Badagry | 378 | 184,638 | 1,808 | 105 | 1% | 11.0 | 0.53 | 0.61 | 3.8 | 0.2 | 426,388 | 1,127 |
| Epe | 828 | 77,445 | 1,535 | 123 | 8% | 10.4 | 0.52 | 0.56 | 4.3 | 3.0 | 382,226 | 461 |
| Eti-Osa | 170 | 208,261 | 1,740 | 146 | 5% | 15.7 | 0.72 | 0.77 | 6.3 | 6.2 | 542,972 | 3,190 |
| Ibeju-Lekki | 438 | 123,826 | 1,674 | 117 | 8% | 11.2 | 0.70 | 0.76 | 5.0 | 5.4 | 238,493 | 543 |
| Ifako-Ijaiye | 26 | 85,196 | 3,287 | 120 | 3% | 16.8 | 0.50 | 0.51 | 5.4 | 1.9 | 564,251 | 21,495 |
| Ikeja | 48 | 79,732 | 2,106 | 162 | 23% | 17.0 | 0.59 | 0.56 | 7.3 | 15.0 | 658,437 | 13,593 |
| Ikorodu | 372 | 455,762 | 2,013 | 114 | 3% | 13.9 | 0.55 | 0.58 | 4.3 | 1.7 | 928,746 | 2,494 |
| Kosofe | 71 | 113,847 | 2,633 | 127 | 2% | 15.4 | 0.51 | 0.51 | 5.6 | 1.9 | 1,104,883 | 15,589 |
| Lagos Island | 6 | 10,938 | 2,206 | 148 | 10% | 23.7 | 0.44 | 0.42 | 8.7 | 17.2 | 76,848 | 12,808 |
| Lagos Mainland | 11 | 33,586 | 3,389 | 106 | 8% | 15.4 | 0.57 | 0.54 | 6.6 | 9.1 | 211,441 | 19,555 |
| Mushin | 18 | 49,790 | 2,771 | 164 | 16% | 18.9 | 0.53 | 0.53 | 6.8 | 11.6 | 644,816 | 35,823 |
| Ojo | 144 | 169,692 | 2,522 | 117 | 3% | 13.4 | 0.58 | 0.61 | 4.7 | 1.2 | 1,012,518 | 7,019 |
| Oshodi-Isolo | 43 | 109,901 | 2,680 | 140 | 7% | 16.3 | 0.62 | 0.64 | 6.0 | 4.7 | 1,222,590 | 28,682 |
| Shomolu | 15 | 41,574 | 2,850 | 141 | 4% | 18.0 | 0.47 | 0.49 | 5.8 | 2.9 | 411,409 | 26,867 |
| Surulere | 21 | 54,181 | 2,657 | 160 | 10% | 17.7 | 0.50 | 0.48 | 6.5 | 8.3 | 644,510 | 30,240 |

What the numbers say, in short:
- **Tallest:** Lagos Island (8.7 m mean, 17% at 4+ storeys), Ikeja (7.3, 15%), Apapa (7.2, 14%), Mushin (6.8, 12%) [H]. Lowest: Badagry (3.8), Ikorodu and Epe (4.3) [H]. Mean heights match the earlier `heights_by_lga.json` to 0.1 m.
- **Most industrial roof:** Ikeja 23%, Apapa 18%, Mushin 16%, Amuwo-Odofin 14% of roof area in buildings over 1,000 m² [OB].
- **Most regular:** Amuwo-Odofin (Festac), Eti-Osa (Lekki), Ibeju-Lekki (new layouts), Ajeromi (a reclaimed grid) [OB][OV]. **Most organic:** Lagos Island, Agege, Shomolu, Surulere [OB][OV].
- **Most crowded:** Ajeromi-Ifelodun at 53,600 people/km² [WP], then Mushin, Agege, Surulere, Oshodi (28,000-36,000).
- **Biggest:** Alimosho alone has 509,000 buildings and 2.6 M people [OB][WP], a fifth of all Lagos buildings.

## The 20 LGAs

Zones = measured character classes (km²) from `STUDY.md` [OB][H][OV][WC]. Everything in "Known for" and "Life" is [K] unless marked.

### Island side

**Lagos Island** (with LCDA **Lagos Island East**)
- Where: the old island town at the harbour mouth, west of Ikoyi. Neighbours: Lagos Mainland and Apapa across the water, Eti-Osa (Ikoyi, Obalende) east.
- Zones: towers and mid-rise on the Marina/Broad Street edge (1.2 km², 13 m mean height, 37% 4+ storeys) [H]; dense organic core of Isale Eko, Idumota, Balogun behind it. The buildings data reads the core as only 2,200 bldg/km²: joined roofs merge into big blocks, so this is a data gap (see picture list).
- Known for: Iga Idunganran (the Oba's palace), Balogun, Idumota, Jankara, Oluwole, Ebute Ero markets; Tinubu Square; Brazilian Quarter (Campos Square, Popo Aguda); CMS bus terminal; Marina banks; Lagos Central Mosque; Holy Cross cathedral; Eyo festival; Freedom Park (old Broad Street prison). Lagos Island East: Obalende/Ikoyi edge, Onikan (Onikan stadium, National Museum, MUSON Centre).
- Life: porters with head loads, cloth and goods markets that spill into every street, traffic jammed on Nnamdi Azikiwe and Martins Street; empty CBD at night; Eyo days [R].
- Main roads: Carter Bridge, Eko Bridge, Third Mainland exit at Adeniji Adele, the Marina, Broad Street, Nnamdi Azikiwe, Inner Ring Road [OV].
- Street grain: 23.7 km of street per km², the densest in Lagos; grid 0.44 (organic) [OV].

**Eti-Osa** (LCDAs **Ikoyi-Obalende**, **Iru-Victoria Island**, **Eti-Osa East**)
- Where: Ikoyi, Victoria Island and the Lekki peninsula to Ajah. Neighbours: Lagos Island, Ibeju-Lekki, Apapa across the harbour.
- Zones: towers and mid-rise in Ikoyi, VI and Banana Island (10.2 km², 10 m mean, 20% 4+) [H]; a planned grid belt of Lekki Phase 1, Oniru, Ikate, Osapa, Agungi (28 km², grid 0.88) [OB][OV]; villa and new-estate belt of Ikota, VGC, Chevron, Ajah (12 km², 670-880 bldg/km², 185-200 m² footprints) [OB]; looser layouts and new build beyond Ajah toward Sangotedo and Badore.
- Known for: Ikoyi (old colonial reservation, Falomo, Awolowo Road, Bourdillon, Banana Island), Obalende (motor park, the bus hub under the bridge), VI (Bar Beach, Eko Atlantic, Adeola Odeku, Ahmadu Bello Way, embassies, the Civic Centre), Lekki (toll plaza and the 2020 shooting, Lekki Conservation Centre, Elegushi and Oniru beaches, Jakande market, Lekki market, Ikota shopping complex), Ajah (Ajah market and the roundabout jam, Ilaje/Ajah waterfront, Badore). Itedo and Ilado waterfront villages; Otodo-Gbame (evicted 2017) [R].
- Life: the rich side; gated estates, gyms, lounges, office towers; under it a working town of drivers, guards, mallams, keke riders and fishing villages on the lagoon edge.
- Main roads: Lekki-Epe Expressway (single biggest trunk, 128 km of carriageway in Overture, both ways), Ozumba Mbadiwe, Ahmadu Bello Way, Admiralty Way, Falomo and Lekki-Ikoyi link bridges, Third Mainland feeding into Obalende [OV].

**Ibeju-Lekki** (LCDA **Lekki**)
- Where: the long peninsula east of Ajah to the Epe lagoon. Neighbours: Eti-Osa, Epe.
- Zones: 316 km² open land; scattered new build and gridded layouts along the expressway (Awoyaya, Lakowe, Eleko, Akodo); the refinery and free zone at the east end (port & tank farm + industry, footprints 325-1,030 m², 42-60% 4+) [OB][H].
- Known for: Dangote refinery and fertiliser plant, Lekki Free Trade Zone, Lekki Deep Sea Port, Lakowe golf estate, Pan-Atlantic University, La Campagne Tropicana, beaches (Eleko, Akodo); land disputes and omo onile [R].
- Life: new estates and building sites, sand-filling trucks, villages between.
- Main roads: Lekki-Epe Expressway, Eleko Beach Road, the new Lekki Coastal Road and Regional Road (being built; check) [OV].

**Epe** (LCDAs **Ikosi-Ejinrin**, **Eredo**)
- Where: the lagoon town at the east end, 60 km from the Island. Neighbours: Ikorodu, Ibeju-Lekki, Ogun State.
- Zones: 691 km² open land; Epe town (12.6 km² bungalow belt, 1,460 bldg/km², 4.1 m mean height) and a gridded new layout at Noforija [OB][H].
- Known for: Epe fish market at the lagoon, Oba's palace, Kayo-Kayo festival, Lagos State University's Epe campus, Lekki-Epe Expressway's end at the T-junction, Ejinrin's old market and jetty, Agbowa, Itoikin [R][K].
- Life: fish, timber, farms, ferries; quiet town.
- Main roads: Lekki-Epe Expressway, Epe-Ijebu-Ode road, Ikorodu-Itoikin-Epe road [OV].

### Inner mainland

**Lagos Mainland** (LCDA **Yaba**)
- Where: Ebute Metta, Oyingbo, Otto, Iddo, Yaba, Makoko, at the mainland end of Carter, Eko and Third Mainland bridges. Neighbours: Lagos Island across the water, Surulere, Shomolu, Mushin, Apapa.
- Zones: the Ebute Metta / Oyingbo / Yaba railway grid (2.4 km², grid 0.83) [OB][OV]; Makoko waterfront and stilts (1.6 km², 6,400 bldg/km², 50 m² mean footprint) [OB]; Otto and Ijora tank and depot strip [OB].
- Known for: Iddo terminus and the old railway town; Oyingbo market; Costain roundabout; Yaba (Tejuosho market, Yaba market, UNILAG next door in Akoka, Yaba College of Technology, Herbert Macaulay Way, "Yabacon Valley" tech hubs, the old psychiatric hospital); Makoko and the Okobaba sawmill on the water; Alagomeji, Sabo, Abule Ijesha [R].
- Main roads: Herbert Macaulay Way, Murtala Muhammed Way, Ikorodu Road start at Jibowu, Third Mainland Bridge, Iddo Road, Western Avenue (east edge), the rail and the Red Line [OV].

**Surulere** (LCDAs **Itire-Ikate**, **Coker-Aguda**)
- Where: south-central mainland between Yaba and Mushin. Neighbours: Mushin, Lagos Mainland, Apapa, Ajeromi, Amuwo-Odofin, Oshodi-Isolo.
- Zones: dense inner core (8.8 km²) [OB]; bungalow belt; the Iganmu / Orile industry strip (Nigerite, National Arts Theatre, Costain) [OB].
- Known for: National Stadium, Teslim Balogun stadium, National Theatre at Iganmu, Ojuelegba junction (bus stop, Wizkid's "Ojuelegba"), Adeniran Ogunsanya shopping street, Bode Thomas, Masha, Aguda, Ijesha, Lawanson, Itire, Coker, Orile; Shitta; middle-class family houses and old cinemas [R].
- Main roads: Western Avenue, Funsho Williams Avenue, Ojuelegba Road, Bode Thomas, Lagos-Badagry Expressway (Orile), Apapa-Oshodi Expressway (west edge) [OV].

**Mushin** (LCDA **Odi-Olowo/Ojuwoye**)
- Where: the dense centre between Oshodi, Surulere and Yaba. Neighbours: Oshodi-Isolo, Ikeja, Shomolu, Surulere, Lagos Mainland.
- Zones: dense inner core (7.3 km²); industry and warehouses along the expressway and Ilupeju edge (4.4 km², footprints ~250 m²) [OB]; the highest street density in the inner mainland (18.9 km/km²) [OV].
- Known for: Ladipo auto-parts market, Ojuwoye market, Idi-Araba (LUTH teaching hospital, big northern community), Papa Ajao, Palm Avenue, Olateju, Isale Eko of Mushin, Odi-Olowo; area-boy and ticketing reputation [R]. [G] notes: 75-85% roof cover, terraced 1-2 storey houses in rows, blocks ~60 x 150 m, 6-8 m streets.
- Main roads: Agege Motor Road, Apapa-Oshodi Expressway, Ikorodu Road edge, Western Avenue edge, the rail [OV].

**Shomolu** (LCDA **Bariga**)
- Where: north of Yaba, on the lagoon side, between Ikorodu Road and Third Mainland Bridge. Neighbours: Kosofe, Lagos Mainland, Mushin, Ikeja.
- Zones: dense inner core (5.2 km²); Bariga dense sprawl (4 km², 3,980 bldg/km²); UNILAG campus edge [OB]; waterfront at Ilaje-Bariga and Ago Egun [K].
- Known for: print shops in homes (Shomolu printing), Pedro, Palmgrove, Onipanu, Fadeyi, Bariga (street rap, Ilaje fishing settlement), Gbagada edge, Akoka [R].
- Main roads: Ikorodu Road, Third Mainland Bridge, Shomolu-Pedro roads, Gbagada expressway (Oworonshoki) [OV].

**Oshodi-Isolo** (LCDAs **Isolo**, **Ejigbo**)
- Where: the middle mainland, south and east of the airport. Neighbours: Ikeja, Mushin, Surulere, Alimosho, Amuwo-Odofin.
- Zones: dense inner core around Oshodi and Mafoluku (5.1 km², 70,000 people/km²) [OB][WP]; industry along the Apapa-Oshodi Expressway and Isolo / Ilupeju (9.3 km² shared with Mushin) [OB]; planned grid of Okota, Ago Palace, Isolo estate (26 km², shared with Alimosho) [OB][OV]; Ejigbo dense sprawl.
- Known for: Oshodi interchange and transport terminals (Terminal 1-3), the Oshodi market under the bridge, Arena market, Mafoluku, Ajao Estate (by the airport fence), Isolo industrial estate, Okota, Ago Palace Way, Ejigbo, Ilasamaja, Shogunle; the airport's south side [R][G].
- Main roads: Apapa-Oshodi Expressway, Oshodi-Oworonshoki Expressway, Agege Motor Road, Airport Road, Ago Palace Way, Isolo Road, rail [OV].

**Apapa** (LCDA **Apapa-Iganmu**)
- Where: the port peninsula across the harbour from the Island. Neighbours: Ajeromi-Ifelodun, Surulere, Lagos Mainland, Amuwo-Odofin.
- Zones: port and tank farm (3.6 km², footprints 250 m², 37% 4+) [OB][H]; Apapa GRA and Olodi bungalow belt; Ijora and Iganmu industry [OB].
- Known for: Apapa and Tin Can Island ports, tank farms and trailers queued for kilometres, Apapa GRA, Apapa Amusement Park, Liverpool Road, Wharf Road, Ijora Badia, Ijora causeway, Iganmu; the "Apapa gridlock" [R].
- Main roads: Apapa-Oshodi Expressway, Wharf Road, Apapa Road, Ijora Causeway, Eko Bridge, Liverpool Road, the old rail to the port [OV].

**Ajeromi-Ifelodun** (LCDA **Ifelodun**)
- Where: Ajegunle, wedged between the ports, the Badagry and Apapa expressways and the canal. Neighbours: Apapa, Surulere, Amuwo-Odofin.
- Zones: dense grid tenement (5.9 km², 61,000 people/km², building alignment 0.92) [OB][WP]: a regular grid of old reclaimed swamp, not organic.
- Known for: "Jungle City", Ajegunle's music (Daddy Showkey, Daddy Fresh), Boundary market, Olodi, Tolu, Layeni, Alakoto, Kirikiri canal; dense multi-ethnic tenements [R].
- Main roads: Lagos-Badagry Expressway (north edge), Apapa-Oshodi Expressway (east), Boundary Road, Mobil Road [OV][K].

**Amuwo-Odofin** (LCDA **Oriade**)
- Where: south-west of the centre on the Badagry corridor, with Festac, Mile 2, Satellite Town, Kirikiri. Neighbours: Ojo, Alimosho, Oshodi-Isolo, Surulere, Ajeromi, Apapa.
- Zones: the largest planned grid in Lagos (Festac, Amuwo, Satellite Town, Mile 2, 26 km², grid 0.85) [OB][OV]; the naval and army land at Ojo/Navy Town (3.4 km²) [OV]; port & tank farm at Kirikiri / Tin Can west (1.9 km²) [OB]; Trade Fair complex; swamps to the south [WC].
- Known for: Festac Town (1977 festival estate, "Festac 419" reputation), Mile 2 interchange and tanker park, Trade Fair Complex (ASPAMDA auto market, BBA), Kirikiri prisons, Satellite Town, Abule Ado (2020 pipeline blast), Ijegun, Agboju, Alakija [R].
- Main roads: Lagos-Badagry Expressway (and its Blue Line), Festac 1st-7th Avenues, Mile 2-Oshodi road, Mile 2-Apapa [OV].

### Outer mainland

**Ikeja** (LCDAs **Onigbongbo**, **Ojodu**)
- Where: the state capital, north of Oshodi, east of the airport. Neighbours: Agege, Alimosho, Ifako-Ijaiye, Kosofe, Shomolu, Mushin, Oshodi-Isolo.
- Zones: the airport (14 km²) [OV]; the Ikeja industrial estate (Ogba, Oregun, Agidingbi, Alausa: 12.8 km², 48% of roof in big buildings, 27% 4+) [OB][H]; Ikeja GRA (planned grid, 4.6 km²) [OB][OV]; Allen / Opebi / Computer Village commercial belt; Ikeja Cantonment (army) [OV].
- Known for: Alausa secretariat (state government), Computer Village (phones), Allen Avenue nightlife, Ikeja GRA, Ikeja City Mall, Ikeja Along, Ikeja Under Bridge, the old Fela Shrine (Agidingbi), Maryland, Ojodu-Berger (motor park and bus stop to Ibadan road), Omole Phase 1 [R].
- Main roads: Obafemi Awolowo Way, Mobolaji Bank-Anthony Way, Kodesoh, Agege Motor Road, Lagos-Abeokuta (Ikeja Along), Ikorodu Road (Maryland/Ojota), Lagos-Ibadan (Berger), Airport Road, Kudirat Abiola Way (Oregun), rail and Red Line [OV].

**Agege** (LCDA **Orile Agege**)
- Where: the railway trading town north of Ikeja. Neighbours: Ikeja, Alimosho, Ifako-Ijaiye.
- Zones: dense inner core and dense sprawl split almost half and half (4.8 + 4.9 km²), 31,000 people/km², organic (grid 0.44) [OB][WP][OV].
- Known for: Agege bread, Agege railway station and market by the tracks, Pen Cinema junction, Agege abattoir and cattle market (Abattoir/Oko Oba), Agege stadium, Dopemu, Oko Oba, northern Hausa quarter (Sabo) [R].
- Main roads: Agege Motor Road, Old Abeokuta Road, Pen Cinema flyover, Oba Ogunji Road, rail [OV].

**Ifako-Ijaiye** (LCDA **Ojokoro**)
- Where: the north edge on the Ogun border. Neighbours: Agege, Alimosho, Ikeja, Ogun State.
- Zones: dense sprawl (11.3 km²) and dense inner core (6.4 km²) around Abule Egba, Iju and Ifako [OB].
- Known for: Iju waterworks (1915), Abule Egba (the junction and 2006 pipeline fire), Ojokoro, Ijaiye, Fagba, Iju-Ishaga (2012 plane crash), Agbado and Oke-Aro on the border [R].
- Main roads: Lagos-Abeokuta Expressway, Iju road, Ijaiye road, Ojokoro road [OV].

**Alimosho** (LCDAs **Agbado/Oke-Odo**, **Ayobo-Ipaja**, **Egbe-Idimu**, **Igando-Ikotun**, **Mosan-Okunola**)
- Where: the huge west-central sprawl west of the airport. Neighbours: Ikeja, Agege, Ifako-Ijaiye, Oshodi-Isolo, Ojo, Amuwo-Odofin, Ogun State.
- Zones: one contiguous dense outer sprawl of 51 km² in the north (Iyana Ipaja, Alagbado, Abule Egba, Ojokoro), 22 km² around Ikotun-Igando, 15 km² at Egbe-Ejigbo, 13 km² at Ipaja-Ayobo-Idimu [OB]; dense inner core at Egbeda-Akowonjo (9.9 km²) [OB][H]; a surveyed grid south of Isolo (Okota / Ago Palace side, 26 km² shared) [OB][OV]. Mean height 4.8 m, 0.6% 4+: almost all bungalows and 2-storey houses [H].
- Known for: Iyana Ipaja and Ikotun roundabouts and markets, Egbeda, Igando (general hospital, Solous landfill), Idimu, Ipaja, Ayobo, Isheri-Olofin, Akowonjo, Abesan estate, LASU-Isheri road; Lagos's largest LGA by people [R].
- Main roads: Lagos-Abeokuta Expressway (east edge), Ipaja Road, Egbeda-Idimu Road, Idimu-Ikotun Road, Egbe Road, LASU-Isheri Road, Airport-Alimosho bypass (new) [OV].

**Kosofe** (LCDAs **Agboyi-Ketu**, **Ikosi-Isheri**)
- Where: the north-east gateway along Ikorodu Road and the Lagos-Ibadan Expressway. Neighbours: Ikeja, Shomolu, Ikorodu, Ogun State.
- Zones: bungalow belts (Ketu/Ojota/Gbagada 17.7 km²; Mile 12/Omole/Berger 19.5 km²) [OB]; dense inner core at Ketu-Ikosi (5 km²) [OB]; swamps and creeks on the lagoon side (14.6 km²) [WC]; Magodo and Omole estates read as bungalow belt, not grid, because their streets bend (see STUDY.md limits) [OB][G].
- Known for: Mile 12 food market (northern trucks), Ketu, Ojota (Gani Fawehinmi park, the chemical/spare-parts market, Ojota bus park), Magodo GRA phase 1 and 2, Omole phase 2, Isheri, Gbagada (and its estate), Oworonshoki (waterfront, demolitions), Agboyi creek villages [R][G].
- Main roads: Ikorodu Road, Lagos-Ibadan Expressway, Oshodi-Oworonshoki Expressway, Third Mainland Bridge start, CMD Road (Magodo-Ikosi), Isheri road [OV].

**Ojo** (LCDAs **Oto-Awori**, **Iba**)
- Where: the west corridor on the Badagry road. Neighbours: Amuwo-Odofin, Alimosho, Badagry.
- Zones: Ojo military cantonment (11.6 km²) [OV]; LASU main campus (1.9 km²) [OV]; Alaba / Okokomaiko dense sprawl (4.8 km²) [OB]; gridded layouts at Ijanikin and Iba [OB][OV]; 30 km² of swamp and mangrove on the creek [WC].
- Known for: Alaba International (electronics) market with its own governance, Okokomaiko, Iyana Iba, Ojo barracks, LASU, Igbo-Elerin, Agboju, Era, the creek villages (Irede, Ibeshe); speedboat smuggling [R].
- Main roads: Lagos-Badagry Expressway (Blue Line along it), Old Ojo Road, Igbo-Elerin road, Iyana Iba road [OV].

**Badagry** (LCDAs **Olorunda**, **Badagry West**)
- Where: the far west to the Benin border. Neighbours: Ojo, Ogun State, Benin.
- Zones: 184 km² open land, 51 km² swamp; bungalow belt from Agbara to Badagry town (27 km² at Agbara-Morogbo) [OB][WC]; lowest heights in Lagos (3.8 m) [H].
- Known for: Badagry town, slave-route museums and the Point of No Return, Gberefu island, Agbara industrial estate (on the Ogun line), Seme border, Topo, Ajido, Gbaji, coconut beaches, Zangbeto [R].
- Main roads: Lagos-Badagry Expressway (to Seme), Badagry-Ilaro road [OV].

**Ikorodu** (LCDAs **Ikorodu North**, **Ikorodu West**, **Igbogbo-Baiyeku**, **Ijede**, **Imota**)
- Where: the big north-east town on the lagoon. Neighbours: Kosofe, Epe, Ogun State.
- Zones: one bungalow belt of 139 km² (Ikorodu, Igbogbo, Ijede, Isawo, Ogolonto), the largest single zone in Lagos [OB]; dense sprawl at Ikorodu town centre (2.9 km²); surveyed grids at the edges; industry at Ogijo / Sagamu Road (5.7 km²) [OB]; Lagos State University of Science and Technology [OV].
- Known for: Ikorodu garage and Sabo market, Ikorodu ferry terminal, Majidun, Ogolonto, Ebute, Isawo, Agric, Owutu, Igbogbo, Ijede, Imota (rice mill), Odogunyan, Oro traditions [R].
- Main roads: Ikorodu Road / Lagos-Ikorodu, Ikorodu-Sagamu Road, Ikorodu-Itoikin road, Ijede road, Ebute road [OV].

## The 37 LCDAs at a glance [K]

| LGA | LCDAs | Count |
|---|---|---|
| Agege | Orile Agege | 1 |
| Ajeromi-Ifelodun | Ifelodun | 1 |
| Alimosho | Agbado/Oke-Odo, Ayobo-Ipaja, Egbe-Idimu, Igando-Ikotun, Mosan-Okunola | 5 |
| Amuwo-Odofin | Oriade | 1 |
| Apapa | Apapa-Iganmu | 1 |
| Badagry | Olorunda, Badagry West | 2 |
| Epe | Ikosi-Ejinrin, Eredo | 2 |
| Eti-Osa | Ikoyi-Obalende, Iru-Victoria Island, Eti-Osa East | 3 |
| Ibeju-Lekki | Lekki | 1 |
| Ifako-Ijaiye | Ojokoro | 1 |
| Ikeja | Onigbongbo, Ojodu | 2 |
| Ikorodu | Ikorodu North, Ikorodu West, Igbogbo-Baiyeku, Ijede, Imota | 5 |
| Kosofe | Agboyi-Ketu, Ikosi-Isheri | 2 |
| Lagos Island | Lagos Island East | 1 |
| Lagos Mainland | Yaba | 1 |
| Mushin | Odi-Olowo/Ojuwoye | 1 |
| Ojo | Oto-Awori, Iba | 2 |
| Oshodi-Isolo | Isolo, Ejigbo | 2 |
| Shomolu | Bariga | 1 |
| Surulere | Itire-Ikate, Coker-Aguda | 2 |
| **Total** | | **37** |

The LCDAs follow old town and community lines more than character. Several cut across one character zone (Alimosho's five all sit in the same bungalow sprawl), and some hold two very different places (Ikoyi-Obalende: billionaire villas and a motor park). They are useful as names, not as district lines.
