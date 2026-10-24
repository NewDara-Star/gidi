# Living in each district: the 51, for the brush and the lived-in layer

Study file (24 Oct 2026). Real place names live here and in other study files only, never in `map/`. The Gidi names come from `roads/NAMES.md`.

**What this is for.** The map shows the buildings. The brush, the person spots and the mix (`decisions/lived-in.md`) show everything else that makes a street feel lived in. This file asks, district by district: who lives there, how rich they are, what they do all day, how they get about, and what a Gidi street there must therefore have. It is the brief for each district's `mix` draft and its person spots. It does not replace the photo study: when Chrome is back, every sheet gets checked against Street View of real streets in that district, and the brush follows the photos.

**Build on, don't repeat.** The 20 council (LGA) reports in `docs/lagos-lgas-research.md` (13 Oct) hold the long version: history, landmarks, danger, pop culture, what to borrow and avoid. `councils.md` holds the measured table by council, `STUDY.md` the character map, `docs/research/LIFE-IN-LAGOS.md` the city-wide life. This file cuts all of that down to the 51 districts and adds a measured line for each.

**How sure each line is:**
- **[M]** measured here (see Method).
- **[LGA]** from the council reports, which cite their own sources.
- A link means a page opened for this file.
- **[K]** general knowledge, not checked. Check it against the photos or the owner's memory before leaning on it.

## Method (the measured lines)

- **District shapes:** the 51 rings in `web/frame-study.js` (`window.FRAME.districts`), turned back into real UTM 31N (x 3, offset by the frame origin). Each measurement covers the real twin's area.
- **People:** WorldPop 2020 constrained, UN-adjusted (`~/gidi-data/research/data/worldpop`). It only counts people where it sees buildings, so the numbers for stilt and waterfront districts (Makoko) and for estates still being built are rough.
- **Buildings:** Google Open Buildings v3, confidence ≥ 0.65. Mean footprint in m², and "big roofs" = the share of roof area in buildings over 1,000 m² (warehouses, factories, markets, malls).
- **Places:** Overture places, confidence ≥ 0.5, grouped into church, mosque, shop, food, night, hotel, money, office, school, health, motor, party, beauty, trade, transport and government. **Caveat:** Overture lists businesses that are online, so it over-counts rich areas and offices, and badly under-counts mosques (Mushin shows 308 churches to 12 mosques, which is not the real ratio). Read "places per 10,000 people" as a rough wealth-and-commerce signal only, never as a count.
- Script: the session's `scratchpad/life/measure.py`; the numbers are copied below.

| # | study name | km² | people | people/km² | buildings | mean m² | big roofs % | places /10k | churches : mosques listed |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Agbara-Morogbo | 177.4 | 157,218 | 886 | 68,023 | 101 | 0.8 | 4.1 | 12 : 0 |
| 2 | Okokomaiko-Ijanikin-Otto | 25.3 | 204,347 | 8,090 | 45,352 | 110 | 1.3 | 4.3 | 28 : 2 |
| 3 | Alaba-Ojo-Trade Fair | 44.4 | 328,264 | 7,400 | 71,421 | 131 | 7.7 | 19.8 | 160 : 1 |
| 4 | Iba-Isheri-Olofin | 34.0 | 343,124 | 10,077 | 68,198 | 120 | 2.6 | 7.3 | 50 : 2 |
| 5 | Festac | 7.0 | 35,944 | 5,113 | 16,426 | 121 | 3.2 | 79.0 | 42 : 0 |
| 6 | Mile 2-Amuwo Odofin | 9.1 | 448,669 | 49,304 | 14,635 | 174 | 34.3 | 7.0 | 36 : 1 |
| 7 | Satellite Town | 26.8 | 112,507 | 4,193 | 36,418 | 135 | 7.0 | 54.9 | 142 : 1 |
| 8 | Kirikiri-Tin Can | 36.7 | 141,604 | 3,861 | 18,403 | 121 | 23.7 | 9.3 | 24 : 0 |
| 9 | Ajegunle | 12.5 | 627,840 | 50,107 | 34,767 | 181 | 8.0 | 11.5 | 221 : 9 |
| 10 | Apapa | 13.3 | 132,870 | 9,998 | 18,426 | 153 | 24.3 | 33.2 | 34 : 5 |
| 11 | Ijora-Iganmu-Costain | 6.0 | 100,627 | 16,827 | 6,700 | 203 | 37.2 | 20.8 | 44 : 0 |
| 12 | Aguda-Coker-Orile | 8.7 | 217,370 | 25,014 | 26,294 | 150 | 2.4 | 30.3 | 160 : 2 |
| 13 | Surulere | 4.8 | 109,876 | 23,083 | 11,452 | 144 | 8.9 | 68.3 | 69 : 2 |
| 14 | Itire-Lawanson-Ijesha | 5.2 | 136,095 | 26,426 | 17,205 | 158 | 4.6 | 44.9 | 127 : 8 |
| 15 | Mushin | 10.7 | 341,759 | 32,000 | 36,046 | 143 | 4.7 | 43.4 | 308 : 12 |
| 16 | Ebute Metta-Oyingbo-Otto | 4.3 | 86,338 | 20,172 | 10,094 | 130 | 8.4 | 40.9 | 68 : 0 |
| 17 | Yaba | 6.4 | 121,291 | 19,011 | 13,860 | 146 | 5.1 | 62.4 | 109 : 1 |
| 18 | UNILAG | 2.7 | 34,447 | 12,950 | 3,209 | 135 | 17.2 | 29.9 | 13 : 1 |
| 19 | Makoko | 2.3 | 32,350 | 13,884 | 15,395 | 69 | 0.6 | 29.4 | 34 : 0 |
| 20 | Lagos Island (Eko) | 5.2 | 67,159 | 12,990 | 10,700 | 149 | 10.5 | 376.9 | 255 : 6 |
| 21 | Ikoyi | 16.8 | 100,848 | 5,989 | 21,414 | 157 | 6.6 | 116.1 | 94 : 5 |
| 22 | Victoria Island | 14.0 | 40,204 | 2,866 | 9,894 | 185 | 14.0 | 336.3 | 51 : 1 |
| 23 | Lekki Phase 1 | 30.7 | 98,185 | 3,201 | 46,069 | 144 | 6.1 | 195.7 | 143 : 4 |
| 24 | Lekki-Agungi-Chevron | 20.8 | 53,812 | 2,586 | 26,937 | 168 | 3.6 | 86.6 | 60 : 3 |
| 25 | Ajah | 54.0 | 139,385 | 2,583 | 79,473 | 136 | 3.7 | 59.5 | 103 : 3 |
| 26 | Sangotedo-Abijo-Lakowe | 169.2 | 104,358 | 617 | 71,902 | 125 | 2.5 | 33.3 | 48 : 0 |
| 27 | Shomolu-Bariga | 12.0 | 345,402 | 28,784 | 39,373 | 134 | 1.5 | 39.3 | 347 : 7 |
| 28 | Gbagada-Ogudu | 15.2 | 379,427 | 24,979 | 35,188 | 130 | 4.3 | 23.6 | 153 : 1 |
| 29 | Ilupeju | 4.6 | 141,489 | 30,625 | 6,878 | 208 | 33.1 | 20.1 | 31 : 1 |
| 30 | Isolo-Ladipo | 11.6 | 467,318 | 40,182 | 23,928 | 198 | 30.3 | 17.4 | 142 : 4 |
| 31 | Okota | 13.0 | 220,913 | 17,033 | 31,287 | 136 | 4.9 | 15.3 | 81 : 1 |
| 32 | Oshodi-Mafoluku | 9.4 | 428,843 | 45,817 | 25,321 | 142 | 2.5 | 14.9 | 160 : 2 |
| 33 | Airport (MMIA) | 14.9 | 91,224 | 6,127 | 7,098 | 151 | 25.8 | 24.4 | 15 : 1 |
| 34 | Ikeja GRA-Cantonment | 6.3 | 157,203 | 24,795 | 12,238 | 145 | 5.1 | 29.3 | 58 : 0 |
| 35 | Computer Village-Allen-Maryland | 9.9 | 204,383 | 20,603 | 21,948 | 148 | 5.5 | 122.7 | 174 : 2 |
| 36 | Alausa-Oregun-Ogba | 16.7 | 203,314 | 12,153 | 30,802 | 195 | 37.9 | 107.7 | 232 : 3 |
| 37 | Agege-Ifako-Ijaiye | 28.8 | 665,442 | 23,106 | 96,369 | 125 | 2.6 | 28.3 | 434 : 9 |
| 38 | Ketu-Mile 12 | 33.1 | 325,719 | 9,843 | 35,856 | 133 | 1.5 | 18.1 | 163 : 2 |
| 39 | Magodo-Omole-Berger | 15.6 | 238,320 | 15,316 | 33,856 | 124 | 1.4 | 21.7 | 81 : 3 |
| 40 | Agbado-Oke Odo | 41.7 | 865,149 | 20,742 | 152,222 | 105 | 1.0 | 10.1 | 268 : 2 |
| 41 | Ipaja-Ayobo | 31.7 | 504,819 | 15,945 | 100,236 | 105 | 1.3 | 14.7 | 214 : 1 |
| 42 | Egbeda-Idimu | 23.5 | 434,394 | 18,469 | 74,179 | 122 | 1.9 | 26.0 | 259 : 3 |
| 43 | Ikotun-Igando | 37.4 | 514,594 | 13,770 | 100,352 | 111 | 2.3 | 9.5 | 145 : 0 |
| 44 | Ejigbo | 6.4 | 220,107 | 34,608 | 22,523 | 114 | 0.9 | 10.3 | 67 : 2 |
| 45 | Ijegun-Abaranje-Isheri Osun | 65.0 | 450,965 | 6,934 | 137,585 | 112 | 0.6 | 14.1 | 205 : 2 |
| 46 | Agric-Isawo-Owutu | 55.6 | 155,139 | 2,791 | 64,077 | 116 | 1.4 | 29.2 | 158 : 0 |
| 47 | Ikorodu Town | 20.1 | 79,283 | 3,942 | 41,273 | 125 | 3.9 | 79.2 | 146 : 4 |
| 48 | Odogunyan-Ogijo | 35.5 | 103,427 | 2,913 | 66,873 | 125 | 10.1 | 20.6 | 69 : 2 |
| 49 | Igbogbo-Bayeku | 78.6 | 203,367 | 2,588 | 114,512 | 115 | 0.7 | 15.1 | 97 : 3 |
| 50 | Ijede-Gberigbe | 50.4 | 138,378 | 2,747 | 84,838 | 111 | 0.8 | 7.0 | 25 : 0 |
| 51 | Imota-Ewu-Elepe | 160.9 | 187,979 | 1,168 | 92,975 | 107 | 1.1 | 2.1 | 11 : 0 |

**Numbers that look wrong, and why:**
- **Mile 2 (6):** 449k people on only 14.6k buildings, while Festac (5) next door has 36k. The ring probably takes in the dense Abule-Ado, Alakija and Agboju strips, and WorldPop spreads people onto the big warehouse roofs. Read Mile 2 plus Festac together: about 485k people on 16 km².
- **Ajegunle (9):** 50k/km² measured, against the council report's 81k/km² (about 1 million on 12.5 km²). Both say the same thing: it is the densest place in Gidi.
- **Ilupeju (29) and Isolo (30):** about a third of the roof area is factories, yet they show 30-40k people/km². The people are packed into the residential parts between the factories.
- **Makoko (19):** the stilt houses are partly missed by both datasets. The real count is likely higher.

## Wealth bands (a working scale, set from the numbers plus the reports)

Lagos is not rich districts and poor districts. Almost every district has an estate or GRA corner and a poor edge. The band is the district's *usual* street. The "rich pocket" and "poor edge" lines in each sheet are what the brush must not forget.

- **A, rich:** Ikoyi (21), Victoria Island (22), Lekki Phase 1 (23). Walled compounds, drivers, guards, few people on foot.
- **B, comfortable:** Lekki-Chevron (24), Magodo-Omole (39), Ikeja GRA (34), Apapa GRA (in 10), Surulere's Bode Thomas end (13), Gbagada estates (28), Festac's good Roads (5), Sangotedo-Lakowe estates (26), Alausa-Ogba (36).
- **C, getting by:** Yaba (17), Surulere (13), Ebute Metta (16), Okota (31), Isolo (30), Ilupeju (29), Egbeda-Idimu (42), Satellite Town (7), Ajah (25), Ikorodu Town (47), Ipaja-Ayobo (41), Ijegun-Isheri Osun (45), Agric (46), Computer Village (35, where the money is in the trade, not in the homes).
- **D, poor and packed:** Ajegunle (9), Makoko (19), Mushin (15), Shomolu-Bariga (27), Oshodi (32), Ejigbo (44), Mile 2 (6), Ijora-Badia (11), Aguda-Coker-Orile (12), Itire-Ijesha (14), Agege (37), Ketu-Mile 12 (38), Agbado-Oke Odo (40), Ikotun-Igando (43), Iba (4), Okokomaiko (2).
- **E, edge of town and farms:** Imota (51), Ijede (50), Igbogbo-Bayeku (49), Odogunyan (48), Agbara-Morogbo (1), Kirikiri's creek wards (8).

**Rent as a check:** a single self-contained room in Ijesha went from ₦70k a year (Nov 2020) to ₦200k ([BusinessDay](https://businessday.ng/real-estate/article/why-lagos-tenancy-laws-cant-stem-rent-hike-landlords-tenants-dispute/)). A self-contained room in Ikorodu is about ₦300-400k a year, and one cost-of-living estimate runs from about ₦140k a month for a single person in Ikorodu or Alimosho to over ₦3 million in Ikoyi ([legit.ng](https://www.legit.ng/business-economy/industry/1729120-n300000-6-lagos-neighbourhoods-rent-breaking-budget/), [ownkey](https://ownkey.com/ng/blog/living-in-lagos-monthly-costs-by-neighbourhood); listing sites, rough).

## Where an okada may ride (this shapes Tunde's whole map)

Commercial okada were banned in six councils from 1 June 2022 (Lagos Island, Eti-Osa, Ikeja, Surulere, Lagos Mainland, Apapa), and in four more from 1 Sept 2022 (Mushin, Shomolu, Oshodi-Isolo, Kosofe, with their LCDAs) [LGA]. Enforcement is patchy, with raids and bikes crushed [LGA].

| okada | districts |
|---|---|
| **Banned** (raids, seizures; okadas still run the back streets) | 10-22, 27-36, 38, 39 (most of 39), 44, 23-25 |
| **Allowed** (the okada is the main way home from the bus stop) | 1-9, 26 (Ibeju side), 37, 40-43, 45-51 |

So the inner city is Tunde's risk zone and the outer ring is his home ground. That is a real Lagos split, and Gidi should keep it.

## What runs through every district (so it is not repeated 51 times)

- **The day:** before dawn the mosques call, then the 5 a.m. bean and akara pots, and bread on heads. From 6 to 9 the bus stops crush, then the shops open. Midday is the buka. From 4 to 8 the second crush, then the suya grills and beer parlours. After 22:00 come the generators, the vigils, the guards and the danger hours [LGA, K].
- **The week:** Friday Jumat empties the streets round mosques at 13:00. Saturday is owambe parties (canopies on the road, gele, sprayed money). Sunday morning means church traffic and the street quiet by afternoon. On sanitation and environmental days the streets are empty until 10 [K]. Each market has its own days.
- **The year:** in the rains, June to September, the streets flood and okadas get through where cars can't. In December the people who live abroad come home, with weddings, beach crowds and traffic [K].
- **Everywhere:** POS agents under umbrellas, betting shops, phone chargers, water sellers (sachet and keg), mechanics under trees, Pentecostal banners, mosque loudspeakers, area boys collecting "ticket", LASTMA officers at the big junctions [LGA, K].

## Activities the person-spot list is missing

The 68 activities in `person_activity` (MAP-FORMAT) cover the shared street life. The districts add these, each needed for at least one district below. They are proposed, not added: adding one is a MAP-FORMAT change for the owner's yes.

| proposed activity | where it is needed |
|---|---|
| `bake_bread` (lidded tins, wood oven), `carry_headload` (bread, pans, baskets on the head: different from `carry_load`) | 37 Agege, every district at dawn |
| `butcher_meat`, `herd_cattle` | 37 (abattoir), 3 (Alaba Rago), 38 |
| `run_press` (printing machine), `guillotine_paper` | 27 Shomolu |
| `smoke_fish`, `shuck_oysters`, `mend_net`, `paddle_canoe`, `cast_net` | 19 Makoko, 27 Bariga, 8, 47-50 lagoon edges, 1 |
| `saw_timber` | 16 (Oko-Baba sawmill) |
| `test_speaker`, `repair_electronics`, `strip_parts` | 3 Alaba, 35 Computer Village |
| `collect_levy` (an agbero writing tickets, not a tout calling passengers) | every motor park and market, above all 32, 10, 15 |
| `play_chess` (street tables, railway tracks) | 32 Oshodi, 9 Ajegunle |
| `play_music`, `dj`, `dance_practice` | 9 (AJ sound), 27 (Bariga rap, drummers on jerrycans), 13 |
| `spray_money`, `dance_party` (owambe) | Saturdays everywhere |
| `jog`, `gym_outdoor`, `walk_dog` | 21-24, 28, 39 estates, 5 (good Roads) |
| `study` (book on a bench) | 18 UNILAG, 17 Yaba |
| `grind_pepper` (grinding machine), `pound_yam` | markets, bukas |
| `mould_blocks`, `dig_sand` | 40-51 (the building frontier), 26 |
| `farm`, `tap_palm_wine`, `climb_coconut` | 51, 50, 1, coast of 26 |
| `queue_atm` (a line outside a bank) | 20, 22, 35, every high street |
| `cyber_work` (laptop in a café), `photo_shoot` | 5 Festac, 17 Yaba, 23 Lekki |
| `scoop_fuel` (jerrycans at a burst pipe or a spilled tanker: a moment, not a daily spot) | 6, 8, 40, 45 |

## The 51 sheets

Each sheet: **real twin** (council) · **Gidi name** · **band**. Then: **people**, **day**, **work and places**, **moving** (vehicles), **brush and spots** (what the street must show), **mix draft** (the busiest groups and hours: a seed for the real `mix` table), **careful** (sacred and real-tragedy flags). Short on purpose: the long version is in the council report.

### Inner mainland (the Mùṣá core and its neighbours)

#### 15. Mushin (Mushin LGA) · Mùṣá · D
- **People:** about 935k in the whole council (2022) and 32k/km² measured. Mostly Yoruba; Igbo traders at Ladipo; Hausa at Idi-Araba; LUTH health workers and students [LGA, [expertlisting](https://www.expertlisting.ng/blog/area-guide/lagos/mushin)].
- **Day:** ewa agoyin and akara pots bubbling at 5 a.m.; amala bukas full at midday; suya, charcoal smoke and bar music after the markets close [LGA, [lagosmetropolitan](https://lagosmetropolitan.com/2026/05/30/street-food-culture-in-mushin-a-local-guide/)].
- **Work and places:** markets (Ojuwoye textiles, Daleko rice and beans wholesale, Idi-Oro fresh food), mechanics, factories at Matori, the teaching hospital, the Red Line station [LGA].
- **Moving:** danfo and keke; okada banned since Sept 2022 but still in the back streets; BRT on the edges; Red Line [LGA].
- **Brush and spots:** narrow grid streets of face-me-I-face-you houses (more three-storey flats each year); bukas under flyovers and beside workshops; open drains with rubbish after rain; "ticket" boys at parking spots; one transformer per street cluster [LGA].
- **Mix draft:** traders, artisans and apprentices, hawkers, keke and danfo crews, area boys. Peaks 6-9 and 16-20; a strong night-food slot until 23.
- **Careful:** egungun and oro, the oba, mosques and churches never criminal. Don't replay the 2002 Idi-Araba killings as an ethnic war [LGA].

#### 30. Isolo-Ladipo (Oshodi-Isolo / Mushin) · Ìṣọ́lẹ̀ · C (Ladipo is D at street level)
- **People:** 40k/km² in the homes between the factories; 30% of the roof area is big roofs [M]. Igbo traders dominate Ladipo; Yoruba homes around it [LGA].
- **Day:** Ladipo full 8 to 6, empty at night apart from guards [lived-in.md]; the factories run shifts [K].
- **Work and places:** the Ladipo spare-parts maze (tokunbo parts, buyers from Ghana and Côte d'Ivoire), factories and warehouses, older industrial streets quiet at night [LGA].
- **Moving:** lorries and part-loaded pickups, truck-pushers with parts on carts, danfo; okada banned [LGA].
- **Brush and spots:** engines and doors stacked on the pavement, oil-black ground, parts touts at the lane mouths, gated factory walls with guards [LGA, K].
- **Mix draft:** traders, artisans, carriers and truck-pushers, touts, factory workers (shift change at 7 and 19 [K]).
- **Careful:** the 2016 parking-fee clash: keep it as a fictional union dispute, not Igbo against Yoruba [LGA].

#### 13. Surulere (Surulere LGA) · Sọ̀rọ̀lérè · C, with a B end
- **People:** about 744k in the council (2022) [LGA]; 23k/km² measured in our ring. Long mixed: Yoruba, easterners in Obele, Ikate and Aguda, northerners at Idi-Araba, Afro-Brazilian families [LGA].
- **Day:** Ojuelegba never stops, with clubs and the bus station round the clock [LGA, [NPC](https://nigeriapropertycentre.com/area-guides/lagos/surulere/ojuelegba)]; match days at the stadium.
- **Work and places:** Bode Thomas is the upscale end (business owners, lounges) and Adeniran Ogunsanya the shopping strip with a mall [[propertypro](https://propertypro.ng/guide/areas/bode-thomas-surulere-lagos/)]; one of the first planned middle-class layouts, from the 1950s; the stadiums and the theatre [LGA].
- **Moving:** danfo and korope with conductors calling stops; keke; okada banned; Eko Bridge to the Island [LGA].
- **Brush and spots:** 1950s-70s storey houses and bungalows with tenement compounds behind; plazas and banks on the main strips; stadium-edge football [LGA].
- **Mix draft:** office workers, traders, students, danfo crews, the party crowd (Thursday to Saturday nights, the highest share of any mainland district [K]).
- **Careful:** the Onitire; the Èṣù/Elegba association with the name; no real musicians or union names [LGA].
- **Owner:** born at Randle General Hospital, Surulere: give its echo care when d13 is drawn.

#### 14. Itire-Lawanson-Ijesha (Surulere, Itire-Ikate LCDA) · Ìtìrí · D
- **People:** 26k/km² [M]; rents rising fast (a self-contained room ₦70k to ₦200k a year in four years) [[BusinessDay](https://businessday.ng/real-estate/article/why-lagos-tenancy-laws-cant-stem-rent-hike-landlords-tenants-dispute/)]. Mostly Yoruba working families [K].
- **Day:** the Lawanson market morning; the canal and low streets flood in the rains [LGA].
- **Work and places:** markets, small shops, the motor union's branch at Ijesha [LGA].
- **Moving:** keke strong, danfo on Itire Road; okada banned but common [LGA, K].
- **Brush and spots:** dense side streets, stalls at the junctions, beer joints, and the canal edge with rubbish lines [LGA].
- **Mix draft:** traders, keke crews, artisans, area boys, children.
- **Careful:** the 2019 cult and union clashes: fictional societies only [LGA].

#### 12. Aguda-Coker-Orile (Surulere / Ajeromi-Ifelodun) · Agunda · D
- **People:** 25k/km² [M]; Aguda named for the Afro-Brazilian returnees; easterners settled here [LGA].
- **Work and places:** Coker market; the industrial edge (Iganmu, Iponri); bus stops at Pako, Yeside and Cassette [LGA].
- **Moving:** danfo, keke, trucks on the expressway edge [K].
- **Brush and spots:** older storey houses, market stalls spilling onto the road, low canal-side streets that flood [LGA].
- **Mix draft:** traders, artisans, danfo crews, area boys.
- **Careful:** the 2019 Mushin-boys and Aguda-boys turf fight: invented groups only [LGA].
- **Gap:** thinnest of the inner sheets. Needs the photo pass most.

#### 16. Ebute Metta-Oyingbo-Otto (Lagos Mainland) · Ìbùdó Mẹ́ta · C
- **People:** Egba Christian founders (1867), then railway families; an Igbo-led wood-turners' trade at Oko-Baba [LGA].
- **Day:** the Oyingbo market morning; the train hours on the Red Line [LGA].
- **Work and places:** Oyingbo market (four floors, over 70 kinds of goods), the railway buildings and museum house, the Oko-Baba sawmill on the lagoon, colonial rail houses being turned into studio flats [LGA].
- **Moving:** Red Line and the standard-gauge terminus; danfo; okada banned; canoes and timber rafts at the sawmill [LGA].
- **Brush and spots:** Brazilian-style and colonial houses with balconies; stacks of wood and sawdust at the sawmill; market women at Oyingbo [LGA].
- **Mix draft:** traders and the market women, artisans (sawyers), railway and office workers, danfo crews.
- **Careful:** the Oloto family is the landowner and ruler: never a crime front [LGA].
- **New activity:** `saw_timber`.

#### 17. Yaba (Lagos Mainland, Yaba LCDA) · Saba · C
- **People:** students (two colleges and the university next door), tech workers, traders [LGA].
- **Day:** student mornings; Tejuosho and Yaba markets by day; evening discount sales; cinema at night [LGA].
- **Work and places:** cheap and second-hand clothes markets; the tech hubs; the psychiatric hospital ("Yaba Left") [LGA].
- **Moving:** danfo, BRT, the Red Line station; okada banned [LGA].
- **Brush and spots:** students with laptops in cafés, clothes bales on the ground at Tejuosho, phone and print kiosks [LGA, K].
- **Mix draft:** students, traders, office and tech workers, hawkers, danfo crews.
- **Careful:** no jokes about the psychiatric hospital's patients [LGA].

#### 18. UNILAG (Lagos Mainland / Shomolu, Akoka) · Lagoon University · C
- **People:** students and staff; 17% big roofs (halls, faculties) [M].
- **Day:** term and holiday rhythms; lecture hours; hostel evenings [K].
- **Brush and spots:** campus lawns, the lagoon front, hostel washing lines, `study` on benches, shuttle buses [K].
- **Mix draft:** students (most of it), staff, campus security, food sellers.

#### 19. Makoko (Lagos Mainland) · Makoro · D
- **People:** mostly Egun people, originally from Badagry and Benin, speaking Egun (Gun); six villages, four on the water and two on land; community heads (baales) [LGA].
- **Day:** fishing at dawn, fish smoked by day, canoe traffic all day [LGA, K].
- **Work and places:** fishing, smoked fish, small trade; the water school (built 2013, collapsed 2016) [LGA].
- **Moving:** canoes; the bridge above [LGA].
- **Brush and spots:** stilt houses, plank walkways, smoking ovens, nets, children paddling to school [LGA].
- **Mix draft:** fishers, fish smokers (the women), children, traders by canoe.
- **Careful:** the clearances (2012, 2025-26) can be a story the player lives through, with the state as the threat and the residents never the villains. Never show the Egun as criminals [LGA].
- **New activities:** `smoke_fish`, `paddle_canoe`, `cast_net`, `mend_net`.

#### 27. Shomolu-Bariga (Shomolu LGA, Bariga LCDA) · Ṣọmọlá · D
- **People:** mostly Yoruba (Egba, Awori, Ijebu, Ilaje) [LGA].
- **Day:** print machines all day; forgery rumoured in the early morning; on cult-fight days the shops shut early and the streets are empty by 8 pm [LGA].
- **Work and places:** 200+ print shops in kiosks added onto homes, over 15,000 jobs [[TechCabal](https://techcabal.com/2016/01/14/the-printivo-story/), LGA]; oyster shucking and smoked mackerel on the Bariga waterfront; the Eko Theatre Carnival; Bariga street rap [LGA].
- **Moving:** okada banned (an Anti-Okada Squad); danfo; canoes at Ilaje [LGA].
- **Brush and spots:** kiosk presses in front of multi-storey houses, ink and laminator smell, paper offcuts; stilt houses and a bar on stilts under the bridge; kids drumming on yellow jerrycans [LGA].
- **Mix draft:** printers and apprentices, traders, area boys, waterfront fishers, students (Akoka edge).
- **Careful:** never use real cult names; masquerade and Ifa never as crime imagery [LGA].
- **New activities:** `run_press`, `guillotine_paper`, `shuck_oysters`, `play_music`.

#### 29. Ilupeju (Mushin LGA [K, check]) · Ìlúpẹ̀lẹ́ · C
- **People:** 31k/km² in the homes; a third of the roof area is factories [M].
- **Work and places:** an industrial estate (warehouses, a gas plant) by the bypass and Agege Motor Road [[NPC listings](https://nigeriapropertycentre.com/commercial/warehouses/lagos/ilupeju/showtype)]; residential streets around it [K].
- **Brush and spots:** factory walls, gatemen, tanker and lorry parking, staff buses at shift change [K].
- **Mix draft:** factory workers, drivers, guards, traders at the gates.
- **Gap:** no proper source on who lives here. Photo pass.

#### 11. Ijora-Iganmu-Costain (Apapa / Surulere / Mainland) · Costa · D
- **People:** port and factory workers in informally built Ijora and Badia (along the rail line) [LGA]; 37% big roofs [M].
- **Work and places:** the industrial edge, the theatre at Iganmu, the Costain roundabout [LGA].
- **Moving:** trucks and tankers, the flyovers, danfo [LGA].
- **Brush and spots:** rail-side shacks, warehouses, trucks parked on the shoulders [LGA].
- **Mix draft:** factory and port workers, drivers, traders, area boys.
- **Careful:** the Badia demolitions: the residents are never the villains [K].

### Port and the south-west

#### 9. Ajegunle (Ajeromi-Ifelodun) · Ayégúnlẹ̀ · D
- **People:** about 1 million on 12.5 km² by the council report; 50k/km² measured, the densest in Gidi. Yoruba majority, with Ijaw, Ilaje, Isoko and others, plus neighbouring countries; Pidgin is the music's language [LGA, [Wikipedia](https://en.wikipedia.org/wiki/Ajegunle)].
- **Day:** markets and hawking by day; the dance halls, DJs and hotel event centres by night; chess at street tables [LGA].
- **Work and places:** Boundary market, port work at Apapa and Tin Can, music and studio work, hotels and event centres [LGA, [Vanguard](https://www.vanguardngr.com/2024/12/ajegunle-inside-the-budding-jungle-city-of-stars/)]. Football on sandy pitches that produced national players [LGA].
- **Moving:** okada allowed (not in the ban list); keke and danfo at the roundabouts; the truck queues at the exits [LGA].
- **Brush and spots:** red tomato and pepper stalls against grey tin; barefoot kids; music shops; sand pitches; plank sections in the markets [LGA].
- **Mix draft:** traders, hawkers, children (a big share), okada riders, musicians and the party crowd at night.
- **Careful:** factions named after streets, never ethnic groups [LGA].
- **New activities:** `play_chess`, `play_music`, `dj`.

#### 10. Apapa (Apapa LGA) · Àpapọ̀ · B in the GRA, D in Badia and under the bridges
- **People:** 217k in 2006; Awori first, then port workers and migrants; executives in the GRA [LGA].
- **Day:** horns and trucks around the clock; the GRA quiet; under the bridge a night hub [LGA].
- **Work and places:** the two ports, Customs and clearing agents, tank farms, flour mills, shipping offices [LGA].
- **Moving:** container trucks and tankers parked in queues for days, okada through the gaps (banned since 2022, but it is the only way through) [LGA].
- **Brush and spots:** trailers parked on every shoulder, mud, urine smell on Creek Road; tree-lined GRA avenues behind gates [LGA].
- **Mix draft:** truck drivers and their boys, clearing agents, "traffic managers" collecting tolls, port workers, guards; the GRA almost empty on foot.
- **New activity:** `collect_levy`.

#### 8. Kirikiri-Tin Can (Amuwo-Odofin / Apapa) · Kẹ́rẹ́kẹ́rẹ́-Tin Pan · D, with E creek wards
- **People:** port and tank-farm workers; Awori riverine wards; the prison [LGA].
- **Work and places:** the second port, fuel storage, the prisons [LGA].
- **Moving:** tankers and trucks; boats in the creeks [LGA].
- **Brush and spots:** tank-farm walls, tanker queues, creek-side jetties [LGA].
- **Mix draft:** drivers, port workers, fishers, prison staff and visitors.
- **Careful:** fuel scooping at spills is a moment with real deaths behind it: fictional only [LGA].

#### 6. Mile 2-Amuwo Odofin (Amuwo-Odofin) · Mile 10-Àmúwá · D
- **People:** the busiest junction of the south-west; dense strips at Abule-Ado, Alakija and Agboju [LGA]; Igbo traders strong [LGA].
- **Work and places:** haulage, mechanic villages, the Mile 2 interchange, warehouses (34% big roofs) [LGA, M].
- **Moving:** tanker and trailer gridlock, danfo to everywhere, okada allowed, the Blue Line [LGA, K].
- **Brush and spots:** truck parks, mechanics, bus-stop crowds, cratered roads [LGA].
- **Mix draft:** drivers, mechanics, danfo crews, traders, touts.
- **Careful:** the Abule-Ado pipeline blast: fictional, no real school or victims [LGA].

#### 5. Festac (Amuwo-Odofin) · Fiesta Town · B in the good Roads, D on 1st and 5th Avenue
- **People:** a large Igbo trading population; mixed Christian and Muslim; Pidgin, Yoruba and Igbo [LGA].
- **Day:** an expressway crawl in the morning; bars, hotels and lounges at night [LGA].
- **Work and places:** home businesses everywhere ("everybody is just doing things on their own"); numbered avenues and Roads; a mall with sports bars; a past as a scam suburb (internet cafés) [LGA].
- **Moving:** private cars, danfo, okada allowed, the Blue Line [LGA, K].
- **Brush and spots:** shops built into the front of the 1977 houses, gated "400 Roads" enclaves with streetlights next to dark avenues, canteens named after mamas [LGA].
- **Mix draft:** traders, office workers, young men at cafés, the party crowd (Friday and Saturday), families.
- **New activity:** `cyber_work`.

#### 7. Satellite Town (Amuwo-Odofin) · Starlight Town · C
- **People:** an older estate (about 1960), partly gone poor; creek-side hotels [LGA]; 142 churches listed, a lot for its size [M].
- **Brush and spots:** estate streets gone informal, creek hotels, churches [LGA].
- **Mix draft:** traders, families, worshippers (Sunday, the highest share in the south-west [M, K]).
- **Gap:** photo pass.

#### 3. Alaba-Ojo-Trade Fair (Ojo / Amuwo-Odofin) · Alàgbà and the Grand Fair · C (trade money, poor rooms)
- **People:** Alaba is strongly Igbo and almost all men; Alaba Rago is Hausa and Fulani; Awori first; a very young population [LGA].
- **Day:** Alaba trades 8 to 6, shuts on Sunday and holds its own court on Friday [LGA].
- **Work and places:** West Africa's biggest electronics market (50,000 merchants claimed, about half the stock second-hand); Trade Fair's auto parts and machinery; Rago's grain, yams, scrap and livestock [LGA].
- **Moving:** okada allowed and everywhere; the broken expressway; truck-pushers [LGA].
- **Brush and spots:** speakers stacked on the pavement, workers stripping dead TVs into hybrids, generators in rows; Rago's drains and slaughter waste [LGA].
- **Mix draft:** traders (men), apprentices, carriers, okada riders, the market's own task force.
- **Careful:** the market's own courts and lenders are a world of their own, not "gangsters" [LGA].
- **New activities:** `test_speaker`, `repair_electronics`, `strip_parts`, `herd_cattle`.

#### 2. Okokomaiko-Ijanikin-Otto (Ojo, Oto-Awori LCDA) · Okoromaiko · D on the expressway, C in Ijanikin
- **People:** Awori towns; Ijanikin full of schools and colleges (a federal government college, the university of education, medical colleges) [LGA].
- **Moving:** okada allowed; the expressway transit points at Okokomaiko and Iyana-Iba [LGA].
- **Brush and spots:** students and pupils in uniform, bus stops on the expressway, quiet college town streets [LGA].
- **Mix draft:** pupils and students, traders, okada riders.

#### 4. Iba-Isheri-Olofin (Ojo, Iba LCDA / Alimosho) · Ìwà · D
- **People:** old Awori settlements with their own obas, now sprawl [LGA].
- **Moving:** okada allowed (the main way in), keke [LGA].
- **Brush and spots:** unpaved side streets, block-moulding yards, new houses going up [K].
- **Mix draft:** traders, artisans, okada riders, builders.
- **Gap:** photo pass.

#### 1. Agbara-Morogbo (Badagry / the Ogun border) · Àgbàlá · E
- **People:** 886 people/km², the emptiest bar Sangotedo [M]. Workers for the Agbara industrial estate (44 companies, over 6,000 workers by one account) [[BusinessDay](https://businessday.ng/?p=1047642)]; Awori and Egun villages [LGA].
- **Moving:** the failing Lagos-Badagry expressway (a 45-minute trip taking 3 hours in the rains) [[Guardian](https://guardian.ng/?p=1206725)]; staff buses, okada, lorries; checkpoints toward Seme [LGA].
- **Brush and spots:** factory gates and staff-bus pickups, bush and farmland between settlements, sand roads [K].
- **Mix draft:** factory workers (shift change), farmers, okada riders, traders at junctions.
- **Careful:** Badagry's Zangbeto and vodún shrines: sacred, and never borrow Zangbeto imagery for a game mechanic [LGA].
- **New activities:** `farm`, `climb_coconut`.

### The Island and the Lekki road

#### 20. Lagos Island (Lagos Island LGA) · Lagoon Island · C at home, the city's money by day
- **People:** 13k/km² at night but the most places per person in Gidi (377 per 10k) [M]: a district that fills by day. Old island families (Isale Eko), traders from everywhere [LGA].
- **Day:** traders in from 7; the markets heaving until dusk; the streets thin after 19 [LGA, K].
- **Work and places:** the wholesale markets (Idumota, Balogun: textiles, everything), the Marina offices and banks, the old Brazilian quarter, the oba's palace [LGA].
- **Moving:** okada banned; danfo at Obalende and CMS; ferries; truck-pushers and head-porters in the market lanes [LGA].
- **Brush and spots:** goods stacked to the first floor, porters with headloads, cloth bolts, money changers, the old balconied houses [LGA].
- **Mix draft:** traders, porters and truck-pushers, hawkers, office workers, bank queues.
- **Careful:** the Eyo festival and the oba: sacred, never crime [LGA].
- **New activities:** `carry_headload`, `queue_atm`.

#### 21. Ikoyi (Eti-Osa / Ikoyi-Obalende LCDA) · Ìwòyí · A, with Obalende D next door
- **People:** old money, diplomats, executives; their drivers, guards, cooks and cleaners live elsewhere and commute in [LGA, K].
- **Day:** drivers waiting by SUVs from 7; few people on foot; joggers early and late [K].
- **Brush and spots:** high walls with gatehouses, gatemen on plastic chairs, generators boxed in, clean roads, a mai shai or suya man at the estate corner [K].
- **Mix draft:** guards and gatemen, drivers, domestic staff, joggers; residents barely on foot.
- **New activities:** `jog`, `walk_dog`.

#### 22. Victoria Island (Eti-Osa) · Victory Island · A
- **People:** few residents (2.9k/km²) and 336 places per 10k [M]: towers, offices, hotels, clubs [LGA].
- **Day:** office hours; drivers waiting at 9 [lived-in.md]; the clubs and lounges late into the night [LGA].
- **Moving:** private cars and SUVs, a few danfo, okada banned [LGA].
- **Brush and spots:** guards and drivers in the shade, food vendors serving office staff, valet stands at night [K].
- **Mix draft:** office workers, drivers, guards, hawkers in traffic, the party crowd after 22.
- **Careful:** never recreate the Lekki toll gate shooting as gameplay [LGA].

#### 23. Lekki Phase 1 (Eti-Osa) · Leke Phase 1 · A
- **People:** young professionals, families, restaurants and offices in converted houses; 196 places per 10k [M].
- **Brush and spots:** estate gates, restaurants and lounges, joggers, dog walkers, photo shoots, ride-hailing pickups [K].
- **Mix draft:** office workers, guards, drivers, domestic staff, the party crowd (weekend).
- **New activities:** `photo_shoot`, `jog`.

#### 24. Lekki-Agungi-Chevron (Eti-Osa) · Leke Phase 2 · B
- **People:** estates and the old fishing villages between them [LGA].
- **Brush and spots:** walled estates, construction, the old village with its market [LGA, K].
- **Mix draft:** builders, guards, residents, villagers, traders.

#### 25. Ajah (Eti-Osa) · Àjọ · C
- **People:** the families who can't afford Lekki; commuters to VI [[ownkey](https://ownkey.com/ng/blog/area-guide-ajah-lagos)].
- **Day:** a 65-100 minute morning commute to VI at peak [[nigeriahousingmarket](https://www.nigeriahousingmarket.com/lagos/area-guides/ajah-lagos)]; the Ajah market and roundabout.
- **Moving:** okada banned (Eti-Osa) but strong at the edges; danfo; keke [LGA, K].
- **Mix draft:** commuters (the 5-7 a.m. slot is the largest), traders, okada and keke crews.

#### 26. Sangotedo-Abijo-Lakowe (Eti-Osa / Ibeju-Lekki) · Àyàntẹ̀dó · B in the estates, E between them
- **People:** the fastest-growing part of the Ajah corridor: newer builds, cheaper, a longer commute [[ownkey](https://ownkey.com/ng/blog/ajah-sangotedo-property-guide-lagos)]. Lakowe is a golf estate of about 308 ha, more a weekend and second-home place [[ThisDay](https://thisdaylive.com/index.php/2023/04/18/860040)].
- **Work and places:** a big mall at Sangotedo (with IKEA and a cinema); dozens of named estates; a nature park [[ownkey](https://ownkey.com/ng/blog/ajah-sangotedo-property-guide-lagos)].
- **Brush and spots:** estate gates in the bush, sand-filled plots, half-built houses, block yards [K].
- **Mix draft:** builders and labourers, guards, residents commuting, mall workers.
- **New activities:** `mould_blocks`, `dig_sand`.

### Ikeja and the north

#### 35. Computer Village-Allen-Maryland (Ikeja) · Gadget Village · C
- **People:** over 10,000 shops; registered shop owners plus "free" moving hawkers; Yoruba and Pidgin, Igbo traders [LGA].
- **Day:** loud and crowded by day; Allen and Opebi wake at 21:30 and fill after midnight [LGA].
- **Brush and spots:** converted houses as phone malls, repairers at tables on the pavement, crowds forming round any dispute; noodle and suya stalls at night [LGA].
- **Mix draft:** traders, repairers, hawkers, customers; at night the party crowd and sex workers on Allen.
- **New activities:** `repair_electronics` (also `repair_phone`, which exists).

#### 36. Alausa-Oregun-Ogba (Ikeja / Agege) · Àláṣẹ · B
- **People:** civil servants; factory, media and brewery workers; 38% big roofs [M, LGA].
- **Day:** government hours; protest gatherings at the secretariat [LGA].
- **Brush and spots:** official buildings and a park; factory gates; TV station masts [LGA].
- **Mix draft:** office and civil workers, factory workers, police, drivers.

#### 34. Ikeja GRA-Cantonment (Ikeja) · Ìgbèjà GRA · B (GRA), C (barracks)
- **People:** GRA residents, hotels; soldiers and their families in the barracks [LGA].
- **Brush and spots:** walled high-rise flats and hotels on potholed roads; barracks gates and soldiers [LGA].
- **Mix draft:** guards, drivers, soldiers, hotel staff.
- **Careful:** the 2002 armoury explosion and the canal drownings: a memory for older people, never a joke [LGA].

#### 33. Airport (Ikeja / Oshodi-Isolo) · Gidi International Airport · C
- **Brush and spots:** terminals, touts and taxi drivers, airport staff buses, Mafoluku and Shogunle homes on the edge [LGA, K].
- **Mix draft:** travellers, drivers, staff, touts.

#### 32. Oshodi-Mafoluku (Oshodi-Isolo) · Ọ̀ṣọ́dé · D
- **People:** 46k/km² [M]; before the interchange there were about 200,000 passengers and 1 million people on foot a day [LGA].
- **Day:** never stops; snatching and trouble under the bridge at nightfall [LGA].
- **Work and places:** the transport interchange (three terminals), the markets around it, container shops [LGA].
- **Moving:** every danfo route, BRT, the train line; okada banned [LGA].
- **Brush and spots:** the two levels, with skywalks and CCTV above and touts and pickpockets below; young men playing chess on the railway tracks [LGA].
- **Mix draft:** passengers, touts and levy collectors, hawkers, traders, police.
- **Careful:** the Oke-Afa memorial and the 2002 dead [LGA].
- **New activities:** `collect_levy`, `play_chess`.

#### 31. Okota (Oshodi-Isolo, Isolo LCDA) · Òkòtó · C
- **People:** estates (Igbo estate chairmen named in reports); homes raised against flooding [LGA].
- **Brush and spots:** estate gates, raised houses and steps, flooded roads filled with red earth by the residents [LGA].
- **Mix draft:** commuters, traders, families, keke crews.

#### 44. Ejigbo (Oshodi-Isolo, Ejigbo LCDA) · Èjìdò · D
- **People:** 35k/km² [M]; "many ethnic groups" [LGA].
- **Moving:** the gully-cut Ifoshi Road ("valley of death", a 2-3 minute trip taking 30+); okada banned (riders said they paid levies daily before the ban) [LGA].
- **Brush and spots:** gullies packed with stones, broken roads, dense houses [LGA].
- **Mix draft:** traders, keke crews, artisans, children.
- **Careful:** the oba's palace [LGA].

#### 37. Agege-Ifako-Ijaiye (Agege / Ifako-Ijaiye) · Agbègbè · D
- **People:** 665k [M]; Awori first; Hausa and Fulani by the rail line and the abattoir; heavily Muslim, plus churches; Egba Yoruba in Ifako [LGA].
- **Day:** bread hawkers at dawn; the abattoir's night arrivals; trains across the roads [LGA].
- **Work and places:** Agege bread bakeries; the Oko-Oba abattoir and cattle market; scrap collectors by the tracks [LGA].
- **Moving:** okada allowed; the Red Line; danfo on the expressway [LGA].
- **Brush and spots:** young women with loaves on their heads; red gutters, wood smoke and goats at the abattoir; shanties on the rail land [LGA].
- **Mix draft:** traders, bakers and bread hawkers (5-9), butchers, okada riders, the devout (a strong Friday slot).
- **New activities:** `bake_bread`, `carry_headload`, `butcher_meat`.

#### 38. Ketu-Mile 12 (Kosofe) · Mile 20 · D
- **People:** Hausa trading communities and Yoruba; traders from all six regions [LGA].
- **Day:** lorries from the north unload several times a day; labourers carry produce straight from trucks to buyers; the Ojota terminal [LGA].
- **Moving:** lorries, danfo, BRT on Ikorodu Road; okada banned [LGA].
- **Brush and spots:** pepper and tomato baskets in heaps, rotting produce, porters, trucks reversing [LGA].
- **Mix draft:** porters, traders and the market women, lorry crews, danfo crews.
- **Careful:** the 2016 riot: write it with no "good side" [LGA].

#### 39. Magodo-Omole-Berger (Kosofe / Ikeja) · Ọmọlà · B, Berger and Ojodu C
- **People:** middle and upper class, professionals and families; originally a government reserved area [[ownkey](https://ownkey.com/ng/blog/area-guide-magodo-lagos)].
- **Brush and spots:** estate gates and guards, big compounds (Phase 1 is older and quieter, Phase 2 denser), the Berger bus stop crush outside [[ownkey](https://ownkey.com/ng/blog/area-guide-magodo-lagos)].
- **Mix draft:** guards, domestic staff, school runs, residents; at Berger, traders and danfo crews.

#### 28. Gbagada-Ogudu (Kosofe / Shomolu) · Gbàgede · B in the estates, C round them
- **People:** upper-middle class by its own account: tech workers from Yaba, young families, retirees; gated estates (Phase 1 and 2) [[nigeriahousingmarket](https://www.nigeriahousingmarket.com/lagos/area-guides/gbagada-lagos-neighborhood)]. The Ologudu at Ogudu [LGA].
- **Day:** the bridge commute to the Island [[ownkey](https://ownkey.com/ng/blog/area-guide-gbagada-lagos)].
- **Brush and spots:** estate lawns, the expressway, the Oworonshoki waterfront at the edge (demolished in 2025) [LGA].
- **Mix draft:** commuters, guards, families, traders at the junctions.

#### 40. Agbado-Oke Odo (Ifako, Ojokoro / Alimosho) · Òkè-Ọkà · D
- **People:** 865k, the most people of any district [M]; Egba Yoruba [LGA].
- **Work and places:** the Oke-Odo produce market (yam, garri, palm oil, from Ogun farmers); the end of the Red Line [LGA].
- **Moving:** okada allowed, keke, the train, the Abeokuta expressway [LGA].
- **Brush and spots:** traders spilling onto the expressway, the dumpsite's standing water, low wetland streets that flood [LGA].
- **Mix draft:** traders, okada riders, commuters (the 5-7 a.m. train slot), farmers bringing produce.

### The Alimosho sprawl (the west and north-west ring)

Alimosho is Lagos's biggest suburb (about 4 million projected in 2019) and "the noisiest council in Lagos" [LGA]. The four districts share: commuters out at 5, okada and keke on every side street (allowed), markets at the roundabouts, churches in every hall, floods.

#### 41. Ipaja-Ayobo · Ìpadà-Ayọ̀wá · C
- Outer sprawl with long detours to anywhere [LGA]. Brush: half-paved streets, churches in warehouses, keke parks.
- **Mix draft:** commuters, okada and keke crews, traders, worshippers.

#### 42. Egbeda-Idimu · Ìdílé · C
- One of the oldest settlements (Egba, around 1830); the Gowon Estate's plan eaten away by stalls, car washes and block yards [LGA].
- **Mix draft:** traders, mechanics and car washers, commuters.
- **New activity:** `mould_blocks`.

#### 43. Ikotun-Igando · Okotun · D
- The market and roundabout heart of the south; the landfill edge's smell [LGA].
- **Mix draft:** traders, okada riders, scavengers near the dump, commuters.

#### 45. Ijegun-Abaranje-Isheri Osun · Ìṣẹ́gun · C
- 451k on 65 km², sprawl along the pipeline [M, LGA].
- **Mix draft:** commuters, builders, okada riders, traders.
- **Careful:** pipeline-fire moments are fictional only [LGA].

### Ikorodu and the north-east

#### 47. Ikorodu Town (Ikorodu) · Ìkòrodò · C
- **People:** over a million in the whole council; Ijebu dialect; Igbo traders at the market; the Ayangburen's palace [LGA].
- **Day:** a pre-dawn rush to the garage and BRT, with conductors calling "Mile 12! Obalende!"; busy afternoon markets; a dark outskirts at night; the traditional curfew days [LGA].
- **Moving:** BRT, danfo, okada allowed; the ferry jetty [LGA].
- **Brush and spots:** red-mud side streets that flood, fast-food chains on the main roads, the market [LGA].
- **Mix draft:** commuters (5-7 is the largest slot), traders, okada riders, students.
- **Careful:** the oro curfew: NPCs warn, the game never shows what is behind it [LGA].

#### 46. Agric-Isawo-Owutu · Agro · C
- Corridor stops getting more suburban; outer settlements with poor roads [LGA, [legit.ng](https://www.legit.ng/business-economy/industry/1729120-n300000-6-lagos-neighbourhoods-rent-breaking-budget/)].
- **Mix draft:** commuters, okada riders, builders.

#### 48. Odogunyan-Ogijo · Odò-Àyàn · E
- Outer settlements; most of the Badoo night attacks happened in this outer ring [LGA]; 10% big roofs (factories on the Sagamu road) [M].
- **Mix draft:** factory workers, farmers, okada riders.
- **Careful:** a night-terror story only with an invented gang [LGA].

#### 49. Igbogbo-Bayeku · Ìgboro · E
- Its own oba and LCDA; a state housing scheme of 360 homes [a state news item seen in search, not opened; check]; lagoon villages [LGA].
- **Mix draft:** farmers and fishers, builders, okada riders.

#### 50. Ijede-Gberigbe · Ìjẹ́rí · E
- Its own oba; Egbin, the country's biggest power station; hot springs [LGA, [Wikipedia](https://en.wikipedia.org/wiki/Ikorodu)].
- **Mix draft:** power-station staff, fishers, farmers, okada riders.

#### 51. Imota-Ewu-Elepe · Ìmọ́lẹ̀ · E
- The emptiest per person: 2.1 places per 10k [M]. A rice mill, a university, a big market, a canteen culture; its own oba [LGA].
- **Mix draft:** farmers, students, traders on market days, okada riders.
- **New activities:** `farm`, `tap_palm_wine`.

## What this means for the brush and the mix

1. **Each district's brush palette comes from its sheet,** then is proven against the photos. Mùṣá: food pots, drains, parts, "ticket" boys. Àpapọ̀: trailers. Ṣọmọlá: paper and ink. Agbègbè: bread and cattle. Makoro: nets, smoke and canoes.
2. **The okada map is a game rule, not decoration:** banned inner councils, open outer ring.
3. **Four kinds of day** stand out and should be the first mix templates, each set by hand per district afterwards:
   - the **market** (Ladipo, Alaba, Mile 20, Lagoon Island): full 8 to 6, guarded at night;
   - the **dormitory** (Alimosho, Ikorodu, Oke-Oka): crowds out at 5, home at 20;
   - the **estate** (Ìwòyí, Leke, Ọmọlà): guards and drivers, few on foot;
   - the **never-sleeps** (Ọ̀ṣọ́dé, Sọ̀rọ̀lérè's junction, Gadget Village at night, Ayégúnlẹ̀).
4. **The thin sheets** (Agunda, Ìlúpẹ̀lẹ́, Starlight Town, Ìwà, the Ikorodu outer towns, Àgbàlá) need the Street View pass first when Chrome is back.

## Sources opened for this file

- [BusinessDay: Lagos rents](https://businessday.ng/real-estate/article/why-lagos-tenancy-laws-cant-stem-rent-hike-landlords-tenants-dispute/)
- [Lagos Metropolitan: Mushin street food](https://lagosmetropolitan.com/2026/05/30/street-food-culture-in-mushin-a-local-guide/)
- [ExpertListing: Mushin](https://www.expertlisting.ng/blog/area-guide/lagos/mushin)
- [PropertyPro: Bode Thomas](https://propertypro.ng/guide/areas/bode-thomas-surulere-lagos/)
- [NPC: Ojuelegba](https://nigeriapropertycentre.com/area-guides/lagos/surulere/ojuelegba)
- [Wikipedia: Ajegunle](https://en.wikipedia.org/wiki/Ajegunle)
- [Vanguard: Ajegunle](https://www.vanguardngr.com/2024/12/ajegunle-inside-the-budding-jungle-city-of-stars/)
- [TechCabal: Shomolu printers](https://techcabal.com/2016/01/14/the-printivo-story/)
- [NigeriaHousingMarket: Gbagada](https://www.nigeriahousingmarket.com/lagos/area-guides/gbagada-lagos-neighborhood)
- [Ownkey: Gbagada](https://ownkey.com/ng/blog/area-guide-gbagada-lagos)
- [Ownkey: Ajah-Sangotedo](https://ownkey.com/ng/blog/ajah-sangotedo-property-guide-lagos)
- [Ownkey: Ajah](https://ownkey.com/ng/blog/area-guide-ajah-lagos)
- [NigeriaHousingMarket: Ajah](https://www.nigeriahousingmarket.com/lagos/area-guides/ajah-lagos)
- [ThisDay: Lakowe Lakes](https://thisdaylive.com/index.php/2023/04/18/860040)
- [Ownkey: Magodo](https://ownkey.com/ng/blog/area-guide-magodo-lagos)
- [NPC: Ilupeju warehouses](https://nigeriapropertycentre.com/commercial/warehouses/lagos/ilupeju/showtype)
- [BusinessDay: Agbara industrial estate](https://businessday.ng/?p=1047642)
- [Guardian: Lagos-Ogun industrial corridor roads](https://guardian.ng/?p=1206725)
- [Wikipedia: Ikorodu](https://en.wikipedia.org/wiki/Ikorodu)
- [legit.ng: cheaper Lagos neighbourhoods](https://www.legit.ng/business-economy/industry/1729120-n300000-6-lagos-neighbourhoods-rent-breaking-budget/)
- [Ownkey: monthly costs by neighbourhood](https://ownkey.com/ng/blog/living-in-lagos-monthly-costs-by-neighbourhood)
- Everything marked [LGA] goes back to the sources listed in `docs/lagos-lgas-research.md`.
