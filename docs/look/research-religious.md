# Gidi look research: religious buildings and places

Scope: mosques, churches, white-garment churches, prayer camps, storefront worship, roadside prayer spaces, traditional shrines and festival structures, and how each one sits in the street.
Builds on `docs/look/research-buildings.md` §10.5–10.6 and `research-street.md` (loudspeakers, banners, Friday/Sunday dress). This file goes deeper. It does not repeat those sections.

Rule zero holds. Real places below (the Lagos Island Central Mosque, the Marina cathedral, the Mowe and Ota camps, the Shitta-Bey mosque) are cited only as examples of a pattern. Every Gidi name is invented. Denomination brands are described generically. No real logo, crest or name should appear on a Gidi sign.

Tags: **[src]** comes from a source listed at the end. **[est]** is my estimate from general knowledge of Lagos street imagery. Most dimensions here are [est]. Published sources give almost no measured dimensions for ordinary Lagos worship buildings; the measured ones are landmark-only.

---

## 0. Summary table

| # | Item | Kit kind | Typical size (footprint, height) | Where (district character) | Share of worship sites [est] | Gidi census names |
|---|---|---|---|---|---|---|
| 1 | Central mosque (green dome, two minarets) | `mosque_central` | 35×50 m site, hall 25×30 m, dome 12–15 m, minarets 25–35 m | old_island, dense_mainland, civic | <1% | Maze Central Mosque, Island Central Mosque, Old Shore Central Mosque |
| 2 | Jumat (Friday) mosque | `mosque_jumat` | 15×20 m hall, dome 5–8 m, 1–2 minarets 12–20 m | all except elite cores | 4% | (Jumat mosques) |
| 3 | Market mosque | `mosque_market` | 8×12 m, often upper floor over shops | next to markets | 2% | (market mosques) |
| 4 | Neighbourhood mosque (mosalasi) | `mosque_small` | 6×10 m, 1 storey, small cap dome or none | dense_mainland, old_island, sprawl, waterfront | 15% | (small neighbourhood mosques) |
| 5 | Roadside / compound prayer space | `prayer_space` | 3×6 m slab or mat patch | everywhere with Muslim traders: markets, parks, petrol stations | 15% (as sites) | (praying mats, ablution taps, kettles) |
| 6 | Northern community mosque | `mosque_north` | 8×14 m, low walls, small or no minaret | Hausa quarters in dense_mainland (Mile 12, Agege pattern), port | 2% | (mosques in northern communities) |
| 7 | Heritage Afro-Brazilian mosque | `mosque_heritage` | 15×18 m, 2 storeys, pediment façade | old_island only | <0.5% | (optional landmark) |
| 8 | Cathedral (Anglican/Catholic) | `church_cathedral` | 25×60 m nave, tower 30–45 m | old_island, civic | <0.5% | Cathedral of Christ |
| 9 | Old mission/parish church | `church_orthodox` | 12×25 m gable hall, small belfry | old_island, dense_mainland, old towns | 6% | (old churches) |
| 10 | Warehouse Pentecostal church | `church_warehouse` | 20–35 m span × 30–60 m, eaves 6–8 m | dense_mainland, sprawl, port, industrial edges | 14% | Fire of Zion Ministries, Victory Tabernacle |
| 11 | Megachurch auditorium | `church_mega` | 80–200 m across, 15–25 m high | sprawl (expressway edge), elite edge | <0.5% | (megachurch auditoriums) |
| 12 | Prayer camp / prayer city | `prayer_camp` | 50–2,500 ha campus | sprawl edge, expressway corridor | special | Prayer City Camp |
| 13 | White-garment parish (Aladura) | `church_whitegarment` | 10×20 m hall, white walls, compound with sand | dense_mainland, waterfront, sprawl | 8% | White Garment Parish of Light |
| 14 | Shore / lagoon worship ground | `worship_shore` | open sand patch 20×40 m, staffs, candles | waterfront, beaches, lagoon edges | 1% | Shoreline White Garment Church |
| 15 | Estate church | `church_estate` | 15×30 m modern hall, glazed gable | elite (both), upper sprawl estates | 3% | Covenant Cathedral |
| 16 | Storefront church | `church_storefront` | one or two shop bays, 4–8 m frontage | dense_mainland, sprawl, plaza blocks | 25% | (small storefront churches) |
| 17 | Church signage set | `sign_church` | boards 1.2×2.4 m to 6×12 m billboards | everywhere, main roads | n/a | (signboards, banners, crusade posters) |
| 18 | Traditional shrine (generic) | `shrine` | 1.5×2 m hut to 6×8 m enclosure under a tree | old_island, old towns, palace precincts, sprawl villages | 1% | (traditional shrines) |
| 19 | Festival structures (generic) | `festival_set` | temporary: canopies, barriers, stands | palace square, old_island main streets | event only | (festival structures) |
| 20 | Street-life layer for all worship | `worship_life` | props, cars, sound, light by day of week | all | n/a | (loudspeakers, generators, parking, traffic, lighting) |

Shares are of all worship sites in a dense mainland ward [est]. In Lagos, small churches heavily outnumber everything else by count. Mosques are fewer per km² than churches overall, but they are close to parity on the old island and in Yoruba-Muslim-majority mainland wards. "Worship centres anywhere" is a known Lagos planning complaint; in 2015 the state sealed 53 churches, mosques and hotels, and some were residential flats converted to worship [src: citifm, thewillnews].

---

## Palette shared by this file

| Token | Hex | Use |
|---|---|---|
| mosque_green | #1F7A3A | domes, trims, minaret bands, gates |
| mosque_green_light | #4CAF50 | newer paint, fibreglass domes |
| mosque_green_faded | #6E9C6A | sun-faded green after 5+ years |
| mosque_white | #F4F2EA | walls |
| mosque_cream | #EDE3C8 | older walls |
| dome_gold | #C9A13B | anodised or painted gold dome, finial crescent |
| dome_silver | #B8BEC4 | aluminium/zinc-clad dome |
| dome_blue | #2F6FA6 | less common dome colour (10%) |
| church_cream | #EFE6D2 | orthodox church render |
| stone_grey | #9C9A92 | stone-look render on cathedrals |
| roof_red_oxide | #8E3B2A | old corrugated roofs painted red |
| shed_silver | #C3C7CA | new aluzinc roofs and walls |
| shed_blue | #2B5C9E | blue long-span roofing sheet |
| shed_rust | #8A4B2A | aged roofing |
| whitegarment_white | #FAFAF7 | robes, walls, flags |
| whitegarment_blue | #2E64B8 | window trim, door bands, sashes (blue is the commonest second colour on Aladura buildings [est]) |
| candle_yellow | #F2D14B | candle flame / wax, sashes |
| banner_red | #D32027 | crusade banners, "fire" themes |
| banner_purple | #6A2C91 | banners, pulpit drapes |
| banner_royal_blue | #1E3FA0 | banners |
| banner_gold | #E2B23A | banner text and borders |
| shrine_white_cloth | #EDEBE4 | cloth wraps on shrine trees |
| shrine_red_cloth | #B5281F | red cloth (some shrines) |
| laterite | #A5532E | bare compound soil |
| beach_sand | #D9C49A | shore worship grounds |

---

## 1. Central mosque (green dome, two minarets)

The Gidi census asks for a green dome with two minarets. Real Lagos pattern: the Lagos Island Central Mosque has a 15 m gold-clad aluminium dome, four minarets (two small over the entrance, two tall at the wings), a 750 m² prayer hall, about one acre of site and about 50 m of frontage on a busy commercial street. It has a riwaq (column arcade) at the entrance, a courtyard, an office block, a library, the Chief Imam's flat, and a drive-in garage and vaults under the building [src: Wikipedia]. Mainland "central mosques" in local governments are smaller versions of the same type, often green-domed [est].

- **Looks like:**
  - A white or cream block of 2–3 storeys' height on a large lot, set hard against a busy street with a short forecourt.
  - One big central dome, green (or gold) with a crescent finial, on a drum with small arched windows.
  - Two tall minarets at the front corners or flanking the hall, slim square-to-octagonal shafts with one or two balconies and a small onion cap, each balcony with loudspeaker horns.
  - A row of pointed or horseshoe arches along the front (arcade), green-painted metal gates, and a big Arabic-and-English name board over the gate.
  - Ablution block to one side with a row of 10–20 taps; shoe racks at the doors.
- **Kit parts:**
  - `hall`: box 25×30 m [est], 10–12 m high, parapet with crenellation strip (small stepped merlons 0.4 m).
  - `dome`: hemisphere or slightly pointed, 12–15 m diameter [src 15 m for the real example], on a 2–3 m drum with 8–16 arched slits; finial 2–3 m pole with crescent 1 m across.
  - `minaret` ×2: shaft 2.5–3.5 m across, 25–35 m tall [est], balconies at 60% and 85% height (ring 1 m wider than shaft, with railing), top cap dome 2.5 m + crescent; four loudspeaker horns per balcony.
  - `riwaq`: 7–11 arches, bay 3.5 m, column 0.5 m, height 5–6 m.
  - `forecourt`: paved, 8–12 m deep, with gate pillars 3 m high and topped by small domes.
  - `ablution`: 1-storey block 4×12 m, open front, waist-high tap rail with 12–20 taps, tiled trough, drain.
  - `annex`: 3–4 storey office/school block in matching white/green.
  - `name_board`: 1.2×8 m, green background, white Arabic line above and English line below.
- **Dimensions:** site 35×50 to 60×80 m; frontage 40–60 m [src 50 m example]; hall 750–1,500 m²; capacity 3,000–10,000 worshippers including courtyard and street overflow [est].
- **Colours:** walls mosque_white #F4F2EA; dome mosque_green #1F7A3A (60%), dome_gold #C9A13B (30%), dome_silver (10%); green bands at parapet and minaret balconies; arches outlined green; windows green-tinted or clear glass with green frames; gates green.
- **Materials:** reinforced concrete frame and block, cement render, painted; dome concrete shell or aluminium/steel cladding; terrazzo or ceramic tile floors; marble or tile on the front piers.
- **Variants:** two tall minarets (census default) 50%; four minarets 20% (two small over gate); one minaret 20%; minarets attached to the façade as twin towers framing the door 10%. Dome alone 70%; one big dome plus 2–4 small corner domes 30%.
- **Condition states:**
  - New: bright white, saturated green, crisp edges, glass intact, gold finial shiny.
  - Worn (default): rain streaks under every parapet and balcony (dark grey #5A5A55 vertical streaks), green faded to #6E9C6A, some tiles missing, AC units added on side walls.
  - Decayed: black mould band on lower 1 m, cracked render, rust on the dome cladding seams, loudspeaker wires draped. Central mosques are rarely decayed; they are rebuilt or repainted for Ramadan.
  - Under construction: very common for central mosques. Concrete frame up, dome formwork or a bare grey shell, minaret shafts with rebar starter bars sticking up, a "Donate to the building project" board with a drawing of the finished mosque.
- **Props and life:**
  - Day, Friday 12:30–14:30: road blocked or narrowed; overflow rows on mats in the street and forecourt; okada and cars parked double; sellers of caps, prayer beads, perfume oil, miswak sticks, books and mats at the gate; beggars at the gate; plastic kettles everywhere.
  - Day, other days: a few men at the ablution taps, shoe racks half-full, the gate open, traders sitting in the shade of the arcade.
  - Night: dome floodlit from below (white or green LED), strings of green LEDs along the minaret balconies, a lit crescent; during Ramadan, extra bulbs and evening crowds for the breaking of the fast and late prayers.
  - Sound: call to prayer five times a day from the minaret horns; the dawn call around 05:15 is the defining sound of Muslim wards.
- **SELECT BY:** `kind=mosque_central`; one per Gidi district centre at most; old_island ↑↑, dense_mainland ↑, civic ↑; on a main road or major square; plot ≥ 1,500 m²; wealth mid–high; condition usually new/worn.
- **Gidi mapping:** Maze Central Mosque, Island Central Mosque, Old Shore Central Mosque. Suggest Island Central (old_island) = gold or green dome with four minarets and riwaq, tightest street; Maze Central (dense_mainland) = green dome, two minarets, annex school; Old Shore Central (waterfront/old town) = green dome, two shorter minarets, more worn, open sandy forecourt.

---

## 2. Jumat (Friday) mosque

The second tier: a ward's Friday mosque, large enough for the Friday congregation of several streets. Usually named after the area or a founder ("Jamiu ... Jumat Mosque" is a common Yoruba naming pattern; Gidi should invent its own).

- **Looks like:**
  - A 1–2 storey white hall on a corner plot, with green trim and a fence wall with a green gate.
  - One medium dome (5–8 m) on the roof, often off-centre over the mihrab end; or a flat roof with a small dome only on the minaret.
  - One minaret (sometimes two) 12–20 m tall at the front corner, square in plan, with loudspeakers.
  - A long signboard over the gate; arched windows with green burglar bars.
  - Upper floor often a women's section or Arabic school (madrasa) with a separate outside stair.
- **Kit parts:**
  - `hall`: 15×20 m [est], 1–2 storeys (4 m per storey), parapet with green band.
  - `dome`: 5–8 m, green fibreglass or painted concrete, crescent finial 0.6 m.
  - `minaret`: 2×2 m square shaft, 12–20 m, one balcony, cap dome 1.5 m; or a simple steel lattice pole with horns (20% of poorer ones).
  - `fence`: 2.1 m block wall painted white with green coping; double steel gate 3.6 m, green, with arched top and crescent cut-out.
  - `ablution`: tap rail against the fence, 6–10 taps, small concrete trough; a PVC overhead tank (black, 2,000–5,000 L) on a steel stand 4–6 m high.
  - `madrasa_stair`: open concrete stair on the side.
  - `sign`: 0.9×4 m board.
- **Dimensions:** hall 250–500 m² [est]; capacity 500–1,500 [est]; plot 600–1,200 m².
- **Colours:** white/cream walls with mosque_green bands (75%); all-green walls (10%); white with blue (10%); white with gold dome (5%).
- **Materials:** sandcrete block, render, emulsion paint; dome GRP/fibreglass (newer) or concrete; burglar bars mild steel painted green; floor tile with carpet rolls inside.
- **Variants:** dome + minaret 55%; minaret only 25%; dome only 10%; neither, just a cupola on the parapet 10%. Two-storey with madrasa 40%.
- **Condition states:** new (sharp green, glossy tile); worn (default: faded green, streaks, patched render, plastic chairs stacked outside); decayed (peeling paint, rusty gate, loudspeaker horns broken and rewired, fence cracked); half-built (second floor bare columns with rebar, a "Building Fund" board).
- **Props and life:** Friday 12:30–14:30 the side street is closed by worshippers on mats and plastic sheets; cars parked on both kerbs; a wheelbarrow seller of water sachets; kettles lined in rows; children in white jalabiya and caps. Daily prayers: 5–30 people. Evening: madrasa children reciting under fluorescent tubes. Night: one or two fluorescent tubes over the gate, a green neon or LED crescent on the minaret, generator humming at Isha prayer if no grid power.
- **SELECT BY:** `kind=mosque_jumat`; old_island ↑↑, dense_mainland ↑, sprawl, waterfront; one per 1–2 km² in Muslim-leaning wards [est]; corner plots and secondary streets; wealth low–mid.
- **Gidi mapping:** Jumat mosques.

---

## 3. Market mosque

Big Lagos markets have a mosque inside or at the edge, often built by the market association, and many traders pray on mats inside the stalls.

- **Looks like:**
  - Either a small free-standing hall squeezed between stall rows, or an upper-floor prayer hall over lock-up shops with a green-painted façade and a dome on the roof.
  - A tiny minaret or just a pole with two loudspeaker horns over the roof line.
  - An ablution corner with a big plastic drum and kettles at the market edge.
- **Kit parts:**
  - `shop_base`: 2–4 lock-up shops 3×4 m with roller shutters (ground floor).
  - `prayer_floor`: 8×12 m upper floor, open sides with arched openings or louvres, green railing.
  - `dome_small`: 3–4 m GRP dome or a cupola on a square drum.
  - `horn_pole`: 6–10 m galvanised pole with 2–4 horn speakers.
  - `ablution_corner`: 2×3 m tiled area, 4 taps, a 1,000 L blue/black drum.
- **Dimensions:** 80–150 m² prayer floor [est]; 2 storeys total.
- **Colours:** green façade over a dirty market base; dome green or silver; shop shutters grey/blue with painted shop names.
- **Variants:** upper-floor over shops 50%; standalone small hall 35%; an open-sided roofed shed (shade structure) with mats 15%.
- **Condition:** usually worn or decayed (market grime, soot, water staining); new only after market rebuilding.
- **Props and life:** at prayer times traders put down goods and line up on mats in the aisles nearby; kettles, sandals in heaps; wheelbarrows parked. Night: mostly closed, market dark; a lone bulb.
- **SELECT BY:** `kind=mosque_market`; within 0–100 m of a market polygon; dense_mainland, old_island, port.
- **Gidi mapping:** market mosques.

---

## 4. Small neighbourhood mosque (mosalasi)

The commonest mosque by count in Muslim-leaning wards: a converted ground-floor room, a single-storey hall in a compound, or a small purpose-built block. Many Lagos mosques were later sealed for noise or for operating in residential flats [src: citifm 2015], which shows how many are improvised.

- **Looks like:**
  - A one-storey hall the width of a plot, painted green and white, with "MASJID" or "Mosque" plus a name painted over the door in green letters.
  - A small cap dome (1.5–3 m) on the parapet or none; a short square minaret stub (5–8 m) or a pole with two horns tied on.
  - Louvre windows with green burglar bars; a curtain at the door; shoes outside.
  - A tap on the side wall with a drain channel; kettles on a shelf or the ground.
- **Kit parts:**
  - `hall_small`: 6×10 to 8×15 m, 3.5 m high, parapet 0.6 m.
  - `cupola`: 1.5–3 m dome on a 1 m square drum, sometimes four mini-domes on the corners (0.6 m) instead.
  - `minaret_stub`: 1.2×1.2 m shaft, 5–8 m, flat cap or mini dome; or `horn_pole` 6–8 m.
  - `name_paint`: hand-painted letters 0.3 m high on the fascia.
  - `tap_point`: one or two standpipe taps at 0.6 m, a low step, a concrete gutter.
  - `kettle_set`: 6–20 plastic kettles.
- **Dimensions:** 60–150 m² [est]; capacity 50–200.
- **Colours:** wall white/cream with green dado (lower 1 m green #1F7A3A, upper white) 40%; full green walls 20%; plain cream with green doors/windows 30%; blue-and-white 10%.
- **Materials:** block and render; roof corrugated sheets behind the parapet; tiled or cement floor with mats.
- **Variants:** purpose-built hall 50%; converted shop/room in a residential building (marked only by paint and a board) 30%; open-sided roofed slab (zinc roof on posts, half-wall 1 m) 20%.
- **Condition:** new (rare); worn (default); decayed (paint chalky, wall algae, rusted horn, cracked slab); half-built (block walls to lintel level, used anyway with a tarpaulin roof).
- **Props and life:** men in caps resting on a bench outside; children; a goat tethered (sprawl); a small Arabic school signboard; Eid: ram sellers nearby. Night: one fluorescent tube, sometimes a small LED crescent.
- **SELECT BY:** `kind=mosque_small`; dense_mainland ↑, old_island ↑, sprawl ↑, waterfront (stilt version on timber in waterfront: plank hall with green paint, horn pole); back streets; wealth low; frequency 2–6 per km² in Muslim wards [est].
- **Gidi mapping:** small neighbourhood mosques.

---

## 5. Roadside and compound prayer space

Not a building. A defined patch where people pray daily, found outside shops, at motor parks, petrol stations, markets, office car parks and building sites.

- **Looks like:**
  - A raised concrete slab or tiled rectangle, sometimes with a low 0.3–0.5 m kerb, facing roughly east-north-east (Gidi can use a fixed qibla bearing; for Lagos, qibla is about 62° from north, east-north-east [est from geometry]).
  - Mats (raffia, plastic woven or carpet strips) rolled up when not in use; at prayer times laid in rows.
  - A tap or a drum of water with a tin cup, and a cluster of plastic kettles.
  - Sometimes a corrugated sheet roof on four steel posts; sometimes painted "Prayer Ground" or a green rectangle on a wall.
- **Kit parts:**
  - `slab`: 3×6 m, 0.15–0.3 m high, cement or green-painted tiles.
  - `roof_shade` (40%): zinc roof 3.5×6.5 m on 4 posts 2.5 m high.
  - `mat_rows`: mats 0.7×1.2 m (single) or 1×2 m rolls in rows, colours mixed: red #B23A30, green #2E7D4F, blue #2B5AA0, beige raffia #C8B07A.
  - `kettle`: plastic, 18 cm tall, colours random (red, blue, green, yellow, white, black); 3–15 per site.
  - `water`: tap on a pipe stand 0.7 m, or a 200 L blue drum, or a 25 L yellow jerrycan.
  - `mihrab_mark` (optional): a small painted arch on a wall at the front.
- **Dimensions:** 15–40 m² [est].
- **Variants:** bare mats on pavement (no slab) 35%; slab without roof 25%; roofed slab 30%; carpeted room-corner inside a shop (visible through the door) 10%.
- **Condition:** mats new/clean vs faded and torn; slab cracked; roof rusted.
- **Props and life:** at the five prayer times (dawn, ~13:00, ~16:00, ~18:45 sunset, ~20:00) 2–20 people line up; traders leave goods with a neighbour; okada riders pray beside parked bikes. Off-time: kettles on the slab, mats rolled, someone sleeping in the shade.
- **SELECT BY:** `kind=prayer_space`; attached to markets, motor parks, petrol stations, mechanic villages, building sites; dense_mainland, port, sprawl ↑; probability higher where district Muslim share is high.
- **Gidi mapping:** praying mats on the roadside, ablution taps, kettles.

---

## 6. Mosque in a northern community (Hausa quarter)

Lagos has long-established Hausa and other northern settlements, with leaders (Sarkin Hausawa) and their own mosques. Agege's name is tied to Hausa settlers, and the Agege Central Mosque's leadership involves the Sarkin Hausawa [src: Wikipedia Agege, Gazette 2025]. Mile 12 and similar markets for produce and livestock have large northern trading communities [src: news reports].

- **Looks like:**
  - Lower, plainer and more horizontal than Yoruba mosques: a 1-storey hall with flat roof, a parapet with small pointed merlons (horn-like "zanko" points at the corners) recalling northern Nigerian earth architecture [est].
  - Walls in earth tones (ochre, sand, pale terracotta) or white; less green; Arabic calligraphy painted over the door; sometimes geometric relief patterns.
  - Small or no dome; minaret short (8–12 m) and square, tapering, sometimes in the same ochre.
  - In the street: an entrance hall (zaure-like) and a forecourt where men sit on mats or benches; Quranic school children (almajiri) with slates and plastic bowls.
- **Kit parts:**
  - `hall_flat`: 8×14 m, 3.5–4 m, flat roof, parapet with 0.5 m pointed corner pinnacles.
  - `minaret_taper`: base 2.5 m to top 1.5 m, 8–12 m high, crenellated top, horns.
  - `relief_band`: painted geometric strip 0.6 m under the parapet.
  - `bench_shade`: timber bench and a zinc canopy 3×4 m.
- **Colours:** ochre #C89A5A, sand #D7BE8E, terracotta #B0623B, white; door frames dark green or blue; calligraphy black/green.
- **Materials:** block render with sand-texture paint; mostly not real earth in Lagos [est].
- **Variants:** earth-tone northern style 40%; ordinary white-green style 45%; a mat ground under a tree with a horn pole 15%.
- **Condition:** mostly worn/decayed (low-income settlements); paint dusty.
- **Props and life:** kaftans, caps, Fulani hats; suya grills nearby at night; tea sellers ("mai shayi") with kettles and a lantern; cattle or ram pens (port/sprawl livestock markets); wheelbarrows of produce; trucks from the north parked. Night: kerosene or LED lanterns, a single bulb.
- **SELECT BY:** `kind=mosque_north`; in a `northern_quarter` sub-zone of dense_mainland (produce market, cattle market, truck parks), port; wealth low.
- **Gidi mapping:** mosques in northern communities.

---

## 7. Heritage Afro-Brazilian mosque (old island landmark)

Late-19th-century mosques built by Afro-Brazilian returnee craftsmen. The Lagos example (1891–94, a national monument from 2013) has a square plan, a Brazilian Baroque façade, a brick front with ceramic cladding divided by stone pillars, floral pinnacles, a central triangular pediment and a gable roof [src: Wikipedia, mosqpedia, Eyes of a Lagos Boy]. The earlier Central Mosque (1913, demolished 1983) was also in this style [src: Wikipedia].

- **Looks like:** a 2-storey façade like a Brazilian townhouse: pilasters, arched windows with mouldings, a pediment with a raised crescent/Arabic panel, corner pinnacles shaped like urns or small minarets, a pitched roof behind. Not domed.
- **Kit parts:** `facade_baroque` 15 m wide × 9–11 m high with 5 bays; pilasters 0.5 m; pediment 6 m wide × 2 m high; 4 pinnacles 1.5 m; arched windows 1.2×2.4 m with timber shutters; a small minaret turret 10–14 m (optional).
- **Colours:** cream #EDE3C8, ochre accents #C9A24A, green shutters #2F6B3F, white mouldings; aged with grey grime.
- **Condition:** worn to decayed; heritage plaque.
- **SELECT BY:** old_island only, 0–1 per district; landmark flag.
- **Gidi mapping:** optional character piece for Island Central area; not in census list.

---

## 8. Cathedral (Anglican / Catholic)

Lagos Island has a Norman Gothic Anglican cathedral (built 1924–46) on the Marina and a French/Gothic Revival Catholic cathedral (1934–39) nearby, the latter by Afro-Brazilian-linked architects [src: Wikipedia both; Archnet]. Gidi's "Cathedral of Christ" is a generic Gothic Revival cathedral, not a copy.

- **Looks like:**
  - A long stone-grey or cream rendered nave with pointed (Gothic) or round (Norman) arched windows and buttresses.
  - One main tower (or two front towers) with a belfry and a spire or crenellated top; a large rose or tall lancet window on the west front.
  - A walled close with lawn, palms and old trees, a car park, a vicarage/clergy house and a church hall/school.
  - A big noticeboard at the gate with service times.
- **Kit parts:**
  - `nave`: 22–28 m wide × 55–70 m long [est], walls 12–15 m, steep gable roof (45–55°), clerestory optional.
  - `tower`: 6–8 m square, 30–45 m to top of spire [est]; belfry louvres; clock face 2 m (50%).
  - `west_front`: gable with rose window 4–5 m diameter or triple lancets 2×8 m; main door pointed arch 3×6 m, timber.
  - `buttress`: every 5–6 m bay, 0.8×1.5 m stepped.
  - `close_wall`: 2.4 m wall with railings, gates with a cross on top.
  - `noticeboard`: 1.5×2.5 m on posts, blue or maroon background.
  - `hall`: 2-storey 15×30 m block nearby in matching colours.
- **Colours:** stone_grey #9C9A92 or church_cream #EFE6D2 render; trim white; roof dark grey slate-look #4A4D52 or red oxide sheets #8E3B2A; stained glass deep blue/red/gold; doors dark brown #4A2E1E.
- **Materials:** concrete/brick with stone-look render; some real stone; long-span roof truss; stained glass.
- **Variants:** single central tower 50%; twin west towers 30%; tower-less with bellcote 20%. Gothic 70%, Romanesque/Norman round-arched 30%.
- **Condition:** well kept (new/worn) on main roads; grime streaks under every ledge in rainy-season black #3A3A38; tropical moss at the base; restoration scaffolding (bamboo or steel) 10%.
- **Props and life:** Sunday 07:00–13:00 several services; formal dress, choir robes, cars filling the close and both sides of the street; wardens with reflective vests directing traffic; weddings Saturday with decorated cars and a canopy; funerals with brass band. Weekdays quiet; office workers in the close at lunch. Night: tower floodlit (warm white), the cross lit; Christmas lights strings on the façade in December.
- **SELECT BY:** `kind=church_cathedral`; old_island (one), civic (one); main road or waterfront marina; plot ≥ 5,000 m²; wealth high; condition new/worn.
- **Gidi mapping:** Cathedral of Christ.

---

## 9. Old mission / parish church (Anglican, Catholic, Methodist, Baptist)

The ordinary parish church of the older denominations, in old towns and mainland neighbourhoods dating from 1900–1980.

- **Looks like:** a rendered gable hall with pointed or round arched windows, a front porch, a small belfry or bellcote with a cross, a fence and a gate with a signboard bearing the church name, diocese and service times; often with a primary school sharing the compound.
- **Kit parts:** `hall` 12×25 m [est], walls 6–7 m, gable roof 35°; `porch` 4×3 m; `belfry` 2×2 m, 12–18 m, or `bellcote` on gable apex 1.5 m with a bell; `windows` arched 1×2.4 m, louvres inside; `cross` 1.5 m on apex; `sign` 1.2×2.4 m on two posts.
- **Colours:** cream/white walls with a coloured plinth (brown #6B4A2F, maroon #6E2430, or blue); roof red oxide or aluzinc; windows blue or brown frames.
- **Variants:** gable hall 60%; hall + tower 25%; modern "A-frame" 1970s style with steep roof to the ground 15%.
- **Condition:** worn (default), decayed in old towns (stained, roof rust, broken louvres), renovated with new aluzinc roof and tiles (30%).
- **Props and life:** Sunday cars on the street, women in matching aso-ebi lace and headties, a mobile ice-cream bicycle, a church bookstall. Night: one floodlight on the cross.
- **SELECT BY:** `kind=church_orthodox`; old_island, old towns, dense_mainland, civic; secondary roads; often next to a school polygon.
- **Gidi mapping:** Anglican/Catholic old churches.

---

## 10. Warehouse Pentecostal church

Pentecostal congregations in Lagos occupy former offices, warehouses and cinemas, and purpose-built long-span sheds, often without regard to planning rules [src: Lawanson; Adeboye "A Church in a Cinema Hall?"; USC CRCC]. A former Yaba cinema houses a church [src: Modern Ghana]. Church emblems appear on buildings, vehicles and hoardings across the streetscape [src: IJURR 2024].

- **Looks like:**
  - A big steel-portal shed, either a reused factory/warehouse or a new one: low-pitch gable roof (10–15°), wall cladding of aluzinc or blue long-span sheets above a 1.2–2.4 m block dado.
  - The gable end faces the street and carries a huge vinyl banner or painted fascia with the ministry name in bold coloured letters, a logo (dove, flame, globe, crown, open Bible), the pastor's photo and the slogan.
  - Side walls open above the dado or fitted with long rows of louvres and big wall fans; a canopy (lean-to) over the entrance.
  - A gated forecourt car park (laterite or interlock paving), a gatehouse, a generator house, and a PVC tank tower.
- **Kit parts:**
  - `shed`: span 20–35 m, length 30–60 m, eaves 6–8 m, ridge 8–11 m [est]; portal frames every 6 m (I-section, painted grey or blue).
  - `cladding`: trapezoidal sheet, rib 0.2 m; dado block 1.2–2.4 m rendered.
  - `gable_banner`: 6×15 m flex-vinyl banner on a steel frame or tied to the cladding; or `fascia_letters` 1.2 m high painted/3D.
  - `entrance_canopy`: 6×10 m lean-to, steel posts, with a flex banner hanging from it.
  - `gatehouse`: 2.5×2.5 m hut.
  - `genset_house`: 3×4 m with louvred sides and exhaust pipe; or an open genset under a zinc roof.
  - `tank_tower`: steel stand 4–6 m with 2× 3,000–5,000 L PVC tanks (black #1A1A1A or blue #2B5C9E).
  - `parking`: 20–100 car spaces [est]; many sites have no space and use the street.
  - `pylon_sign`: steel pole sign 6–9 m tall with a lightbox 2×4 m at the road.
- **Dimensions:** 600–2,000 m² floor; capacity 500–3,000 on plastic chairs [est].
- **Colours:** shed_silver #C3C7CA (45%), shed_blue #2B5C9E (30%), cream-painted cladding (10%), rusty/older #8A4B2A (15%). Banners: red/white with flames, royal blue/white/gold, purple/gold, white with a gradient band; text in white with drop-shadows.
- **Materials:** steel portal frame, aluzinc sheets, sandcrete dado, PVC flex banner, interlock pavers.
- **Variants:**
  - Reused factory/warehouse in an industrial estate 35%.
  - Purpose-built shed on a residential/sprawl plot 40%.
  - Converted cinema/hall (masonry, flat-front façade with a big name panel) 10%.
  - "Open-sided tabernacle": roof on columns only, no walls, used while the real building is constructed (often beside a half-built concrete auditorium) 15%. The open-sided form matches the photo-essay description of a big camp hall as "a huge warehouse-like construction without walls" [src: National Geographic].
- **Condition states:** new (clean sheets, crisp banner); worn (default: sun-faded banner, magenta and red going pink, sagging vinyl, rust streaks at sheet laps); decayed (torn banner flapping, missing sheets, rusted gate, weeds in the forecourt); abandoned (congregation moved: banner removed or torn, "FOR LEASE"/"Warehouse to let" sign, padlock).
- **Props and life:**
  - Sunday 07:00–14:00 (often two or three services) and midweek evenings (Tuesday/Wednesday 17:30–20:00) and night vigils (Friday 22:00–05:00, often monthly).
  - Ushers in matching uniforms and reflective vests directing cars; cars parked on both kerbs for 100–300 m; church buses (white 18-seat or coaster buses with the church name painted on the side); okada drop-offs; snacks and gala/drinks sellers outside.
  - Loudspeaker stacks inside, sound spilling through open sides; LASEPA enforcement against outdoor horns and loudspeakers and for exceeding 55 dB (day) / 45 dB (night) residential limits is periodic [src: ThisDay, Gulf News, Guardian].
  - Night: fluorescent tubes or LED floods visible through the louvres; the pylon lightbox; the generator running; coloured stage light (blue/purple) glowing through the open sides; strings of LED along the gable at events.
- **SELECT BY:** `kind=church_warehouse`; dense_mainland ↑, sprawl ↑↑, port (old warehouses) ↑, industrial edges; plot ≥ 800 m²; main road or one block off; wealth mid; every 300–800 m on mainland arterials [est].
- **Gidi mapping:** Fire of Zion Ministries (red/flame banner, blue shed, reused warehouse), Victory Tabernacle (open-sided tabernacle next to a half-built auditorium); generic converted warehouse churches with banners.

---

## 11. Megachurch auditorium

The biggest Pentecostal halls, mostly on the city edges along the expressways. The Ota example opened in 1999 with 50,400 seats, built in under 12 months, on a large campus [src: Wikipedia Faith Tabernacle]; a project summary gives 25 m ceiling height and 100 m wings [src: LinkedIn, low confidence]. The Mowe camp's new arena is reported in news as "3 km × 3 km", a figure that is clearly exaggerated [src: Guardian; treat as hyperbole].

- **Looks like:**
  - A huge low building, a fan, octagon, or a rectangle of several hundred metres, cream/white walls, a wide band of glazing or louvres, a sweeping metal roof.
  - A monumental front: a portico or glass gable entrance, the church name in large 3D letters, flagpoles, a fountain or roundabout.
  - Car parks the size of districts, with numbered zones and lighting masts; internal roads; LED screens outside.
- **Kit parts:**
  - `auditorium`: 120×150 m [est] (fan or rectangle), eaves 15–20 m, ridge 20–30 m; roof long-span steel truss, colour aluzinc or blue/green.
  - `portico`: 30–60 m wide, columns 1–1.5 m, 12–18 m high; or glazed entrance wall.
  - `name_letters`: 2–3 m high, gold/white, lit at night.
  - `screens`: outdoor LED screens 6×10 m.
  - `car_park`: 5,000–20,000 spaces [est]; light masts 15–25 m every 60 m.
  - `ancillary`: offices, chalets, schools, bank branches, fuel station on campus.
- **Colours:** walls cream #EFE6D2 or white; roof blue #2B5C9E / green #2F7A4A / silver; glass blue-green tinted #6A9AA6; gold letters.
- **Variants:** fan/theatre plan 40%; rectangular shed with rows of portal frames (open sides) 40%; dome or circular 20%.
- **Condition:** new/worn; vast open-sided older arenas kept but showing rust.
- **Props and life:** monthly night meetings bring 300,000–500,000 people and block the expressway both ways for hours [src: Pulitzer Center]; annual conventions exceed one million [src: Pulitzer Center]; buses, hawkers, makeshift parking on the verge; choirs of hundreds, giant screens [src: National Geographic]. Night: the whole campus lit like a stadium; masts, coloured façades, tail-lights of the queue for kilometres.
- **SELECT BY:** `kind=church_mega`; sprawl edge on a primary road/expressway; plot ≥ 20 ha; wealth n/a (landmark); max 1–2 per map.
- **Gidi mapping:** megachurch auditoriums.

---

## 12. Prayer camp / prayer city

A church-owned campus town. The Mowe camp covers over 2,500 ha with over 5,000 houses, roads, waste collection, a police station, a hospital, supermarkets, banks, a post office, a fun fair, schools, a printing press, a Bible college and a power plant [src: Wikipedia]. Its population grew from about 12,000 (2018) to an estimated 200,000 (2023) [src: Wikipedia]. Smaller camps line the same expressway corridor; scholars call this Pentecostal "enclave urbanism" [src: Lawanson]. Churches provide roads, bridges, electricity, water, healthcare, banking and housing [src: IJURR 2024].

- **Looks like:**
  - A gate arch over a divided boulevard with the camp name, flags and a security post; inside, unusually clean tarred roads with kerbs painted black-and-white, street lights, and roundabouts with monuments (open Bible, dove, globe).
  - Zones: arenas (open-sided sheds), chalets and guest houses, staff estates of identical bungalows, shops, banks, a hospital, schools, a fuel station.
  - Signposts in a single house colour scheme; hoardings with the founder's image and event dates.
  - On the access road: hawkers, buses, and queues on event nights.
- **Kit parts:**
  - `gate_arch`: span 20–30 m, 10–14 m high, name panel 2 m, flagpoles ×6 10 m.
  - `boulevard`: dual 7.3 m carriageways, 3–5 m planted median with palms, street lights every 30 m.
  - `arena`: open-sided shed 100×200 m+ (see §11 and §10 open variant).
  - `chalet_row`: 1-storey 8×12 m bungalows, identical, pastel.
  - `camp_signs`: blue or green directional signs with white letters.
  - `roundabout_monument`: 6–10 m sculpture.
- **Colours:** house colours of the camp (e.g. blue and white, or red and gold); kerbs black/white #111/#F2F2F2; signs uniform.
- **Variants:** "prayer city" (full town) 10%; medium prayer camp (one arena, chalets, shops; 10–60 ha) 50%; small "prayer mountain"/retreat (a fenced bush plot with open sheds and a hilltop cross) 40%.
- **Condition:** core well kept (new/worn); edges half-built: plots with foundations, signboards "Plot reserved for..." and bush.
- **Props and life:** thousands of parked buses on event nights; tents; sleeping mats under sheds; vendors of water, bread, anointing oil, Bibles, CDs; police and traffic wardens; at quiet times a tidy campus town with residents, joggers, school buses.
- **SELECT BY:** `kind=prayer_camp`; sprawl edge on an expressway corridor; very large parcel; 1 per map plus 2–4 smaller camps along the same corridor.
- **Gidi mapping:** Prayer City Camp; prayer camps.

---

## 13. White-garment parish (Celestial / Cherubim-and-Seraphim style)

Aladura churches, founded in Nigeria and Benin and strongest in Lagos and Ogun [src: Wikipedia CCC, C&S]. Members wear one-piece white robes (sutana / aso-funfun / "the garment") and worship barefoot; white is linked with purity [src: The Manor; Wikipedia]. Gidi: generic, respectful, no real crests.

- **Looks like:**
  - A white-painted hall, often modest, with blue trim; a wide central door; plain or pointed windows; a cross and sometimes a painted eye, star, or crescent-and-star symbol on the gable (generic for Gidi: a white cross on a blue panel).
  - The compound is often sand-covered (fresh beach sand spread on the floor and yard is a recognised practice [est]); everyone removes shoes at the gate; rows of slippers at the entry.
  - Inside, visible through doors: white walls, candles on stands, a curtain or rails in front of the altar, benches.
  - A small separate prayer hut or bell stand in the yard; flagpoles with white or blue flags; a signboard with the parish name and "Parish" number.
- **Kit parts:**
  - `hall`: 10×20 m [est], walls 4–5 m, gable roof 25° or flat parapet; or a long single-storey building.
  - `gable_symbol`: cross 2 m on a blue panel 2×3 m.
  - `yard_sand`: 10×15 m sand area, beach_sand #D9C49A.
  - `shoe_rows`: 20–200 slippers at the threshold.
  - `candle_stand`: 1.2 m stand with 3–7 candles; candle sticks in the yard sand.
  - `bell_post`: 3 m post with a hand bell or metal ring.
  - `flagpole`: 6 m with white flag.
  - `sign`: 1×3 m white board with blue lettering.
- **Colours:** whitegarment_white #FAFAF7 walls, whitegarment_blue #2E64B8 trim and doors, sometimes light blue #8FB7E3; gold or yellow highlights; roofs aluzinc or blue sheets. Robes white; sashes or belts in blue, purple, red, gold or green depending on rank [est].
- **Materials:** block and render; or (poor/waterfront) timber planks painted white on piles; zinc roofs.
- **Variants:** proper parish hall 45%; converted house/compound (a residential plot with a tent shed in the yard) 30%; timber/zinc hall (waterfront, sprawl edge) 25%.
- **Condition:** the paint is renewed often because white shows dirt: new (gleaming); worn (default: grey splash band 0.5 m at base, red laterite dust); decayed (algae, chalking, sagging zinc).
- **Props and life:** Sunday 09:00–14:00 and weekday evening services and vigils; drums, bells, singing; white-robed people walking barefoot through the streets to and from service, with families and children [src: The Manor]; Bibles, candles, small water bottles; robe tailor nearby. Night: candles and fluorescent tubes, white walls glowing; vigils with drums.
- **SELECT BY:** `kind=church_whitegarment`; dense_mainland ↑, waterfront ↑↑, sprawl, old towns; back streets; wealth low–mid; near water bodies ↑.
- **Gidi mapping:** White Garment Parish of Light.

---

## 14. Shore and lagoon worship ground (white-garment, plus others)

Beaches have long hosted white-garment groups praying at the water's edge, "casting and binding into the ocean" [src: Eyes of a Lagos Boy, TheCable Lifestyle on the old beach]. Lagoon and creek edges host similar open-air prayer spots, and some white-garment parishes sit right on the shore [est].

- **Looks like:**
  - An open area of sand by the sea or lagoon, sometimes defined by a ring of stones or a low fence, with a few poles carrying white flags; a wooden cross 2–3 m stuck in the sand; candles in the sand; a zinc-roofed shelter on poles.
  - Groups of white-robed, barefoot worshippers in circles or lines facing the water; a leader with a staff or bell; buckets of water, bottles, fruit and candles.
  - Shoreline church: a white-painted plank or block hall on stilts or a sand platform, with a jetty, canoes, and a painted sign facing the water.
- **Kit parts:**
  - `ground`: 20×40 m sand patch, beach_sand #D9C49A, wet edge darker #A8936A.
  - `flag_poles` ×3–7: 4–6 m bamboo or steel, white cloth flags 1×1.5 m (some blue).
  - `cross_post`: 2–3 m timber, white-painted.
  - `shelter`: zinc roof 4×6 m on 6 timber posts 2.4 m.
  - `candle_ring`: 7–20 candles in sand.
  - `stilt_church` (shoreline variant): 8×16 m plank hall on 1–1.5 m piles, white planks, blue window shutters, zinc roof, jetty 10–20 m.
- **Colours:** white, blue, sand; at night candle_yellow #F2D14B pools of light.
- **Variants:** beach prayer ground 40%; lagoon-edge prayer spot (mud, mangrove, rocks) 30%; shoreline/stilt church 30%.
- **Condition:** flags weathered grey-yellow, torn; shelter rusty; after storms, swept away (the beach ground has no fixed state). Coastal surges have destroyed beach shacks in the past [src: Wikipedia Kuramo].
- **Props and life:** dawn and night most active (05:00–07:00, 21:00–02:00 vigils); people wading knee-deep; footprints; canoes drawn up; fishermen nearby. Night: dozens of candle flames, a battery lamp, white robes reading as pale shapes in moonlight.
- **SELECT BY:** `kind=worship_shore`; waterfront and any district with a beach/lagoon edge; outside port and elite seafronts (or at their unmanaged ends); low wealth.
- **Gidi mapping:** Shoreline White Garment Church; beach and lagoon-side worship.

---

## 15. Estate church

Churches inside or at the gate of planned estates and elite areas: polished, modern, well-parked.

- **Looks like:**
  - A modern hall with a tall glazed gable or a pointed "A" front, often with a freestanding steel or concrete cross tower 15–25 m; cladding in stone tiles, ACP (aluminium composite panel) bands, and blue glass.
  - Landscaped forecourt, interlock car park with painted bays, palms, a fountain, a gatehouse with barrier; a separate children's church and offices.
  - Name in brushed steel letters on a stone feature wall.
- **Kit parts:**
  - `hall`: 15×30 to 25×45 m, 8–12 m high; gable glazing curtain wall 8×10 m.
  - `cross_tower`: 1.5×1.5 m concrete blade or steel lattice, 15–25 m, cross 3 m (LED lit).
  - `feature_wall`: 2.5×10 m, stone-look tile, steel letters 0.6 m.
  - `car_park`: 80–300 bays, interlock, painted lines, shade sails.
  - `gatehouse_barrier`: 2.5×2.5 m hut + 4 m barrier arm red/white.
- **Colours:** white #F6F6F4, light grey ACP #C9CDD1, charcoal #3D4045, blue glass #3E6E8E, gold or silver lettering; landscaping green.
- **Materials:** RC frame, curtain-wall glass, ACP, porcelain tile, steel.
- **Variants:** Pentecostal modern (glass, LED) 60%; orthodox modern (Anglican/Catholic in GRA: brick-look, bell tower) 30%; converted villa (a large house with a sign and a tent extension) 10%.
- **Condition:** new/worn mostly; "worn" = stained ACP joints, tired landscaping.
- **Props and life:** Sunday: SUVs, drivers waiting under trees, security in black, ushers, a coffee/snack stand; weddings with florists. Weekdays quiet. Night: uplit façade, LED cross, bollard lights.
- **SELECT BY:** `kind=church_estate`; elite ↑↑, upper sprawl estates ↑; plot ≥ 2,000 m²; inside an estate gate or on the estate's main road.
- **Gidi mapping:** Covenant Cathedral.

---

## 16. Storefront church

The most common church by count. One or two shop bays in a plaza, ground floor of a house, or a container/kiosk-scale room, with plastic chairs and a pulpit. The state has sealed worship centres operating in residential flats and makeshift structures [src: citifm 2015, Gulf News].

- **Looks like:**
  - A shop frontage with the roller shutter rolled up, or glass doors, under a big flex banner with the ministry name, logo, slogans ("Where Miracles Happen", "Come and be blessed") and service times.
  - Inside: plastic chairs in rows (white or red), a pulpit with a cloth drape (purple, white, gold), a keyboard and drum set, two speakers on stands, a fan.
  - Sometimes upstairs in a commercial building, with a banner hung across the balcony.
- **Kit parts:**
  - `bay`: 4×8 m per shop, 3.5 m high; 1–3 bays.
  - `front_banner`: 1.2–1.8 × 4–8 m flex, tied with rope at corners.
  - `door_sign`: A3/A2 laminated service-times poster.
  - `chairs`: monobloc plastic chairs, white #F2F2F2 or red #C62828 or blue #1E5AA8, 20–80.
  - `pulpit`: 1.2 m stand, drape 0.6×1.2 m.
  - `speakers`: 2 on tripod stands; occasionally one horn speaker over the door.
  - `canopy` (optional): fabric gazebo 3×3 m outside for overflow.
- **Colours:** the building's own paint plus the banner (see §17).
- **Variants:** shop bay in a plaza 50%; ground floor of a residential building 25%; upper-floor hall 15%; container or zinc kiosk on a vacant plot 10%.
- **Condition:** banner new (bright) / faded (pink-washed reds, cracked vinyl) / torn; shutter dented; if closed, the banner remains on a shuttered shop.
- **Props and life:** Sunday mornings and weekday evenings: singing and amplified preaching onto the street; worshippers' okada parked; outside, the next shop (a barber, a POS stand) keeps trading. Night: one LED tube inside, a small lightbox sign (20%).
- **SELECT BY:** `kind=church_storefront`; ground floor of `plaza`/`shophouse` in dense_mainland ↑↑, sprawl ↑↑, port; back and secondary streets; wealth low.
- **Gidi mapping:** small storefront churches in shops.

---

## 17. Church signage: signboards, banners, crusade posters

Church emblems are everywhere in Lagos: on buildings, vehicles and advertising hoardings [src: IJURR 2024]. Event banners and posters are already listed in `research-street.md`; this section gives the kit specifics.

- **Looks like:**
  - Directional signboards at junctions: a cluster of 5–15 small boards on posts or nailed to an electric pole, each with a church name and an arrow ("200m", "Turn Left").
  - Permanent boards at the gate: rectangular, 1.2×2.4 m, on two steel posts, white or blue background, logo at left, name in bold, address and service times below.
  - Event banners: flex-vinyl 1×3 m to 3×10 m strung between poles across or along roads, for crusades, conventions, revivals, "Holy Ghost" night events, with the pastor's and guest preacher's photos, dates and venue.
  - Posters: A2/A3 posters pasted in layers on walls, pillars and bridge piers, overlapping and peeling.
  - Billboards: 6×12 m or 4×8 m billboards on main roads for big churches and camps.
  - Vehicle livery: church buses with names painted in large letters along the side.
- **Kit parts:**
  - `dir_cluster`: post 3 m with 5–15 boards 0.3×1.2 m each, assorted colours.
  - `gate_board`: 1.2×2.4 m panel on 2 posts 2.4 m high.
  - `cross_banner`: flex 1×6 m to 1.2×12 m, ropes to poles; sag 0.2–0.4 m.
  - `poster_wall`: decal layer of overlapping A2 posters (aspect 0.7), 20–60% coverage, with peeling and rain streaks.
  - `billboard`: steel monopole 10–14 m with a 6×12 m face; floodlights at the top edge.
  - `bus_livery`: decal on 18-seat white bus side.
- **Colours:** typical banner schemes [est]: red-to-orange flame gradient with white/yellow text 25%; royal blue with gold 20%; purple with gold/white 15%; white with blue and red 15%; black with gold (night events) 10%; green/white 5%; multicolour 10%. Fonts: heavy italic sans and script, white with a black drop-shadow.
- **Variants & condition:** new (saturated), faded (after ~3 months sun: red → pink #E58C9A, blue → pale #7B9CC9), torn (strips hanging), skeleton (frame only). Posters: fresh / layered / scraped to paper pulp.
- **Props and life:** banners go up 2–4 weeks before an event and stay long after. Political posters and burial posters share the same walls.
- **SELECT BY:** density rises with church count and with main-road proximity; dir_cluster at junctions within 500 m of churches; billboards on primary roads only; elite: few, smaller, regulated.
- **Gidi mapping:** church signboards, banners, crusade posters.

---

## 18. Traditional shrine (generic, respectful)

Traditional Yoruba religion remains present: palace precincts, family compounds, groves and sacred trees, and festivals. Gidi should depict shrines generically and respectfully: no named deity iconography, no sacrifices shown, and only the outer form.

- **Looks like:**
  - A small hut or open shelter, often under a big old tree (iroko or similar), with white cloth tied around the trunk; a low wall or fence around it; a closed door or curtain.
  - Inside or in front, unseen or partly hidden: clay pots, cowries, carved posts (keep generic: plain pots and a covered object).
  - In old towns, a shrine house in a family compound or near the palace: a 1-room building with a pitched zinc roof and a decorated door; a small plaque.
  - Grove variant: a patch of untouched trees in a built-up area, fenced, with a gate.
- **Kit parts:**
  - `shrine_hut`: 1.5×2 to 3×4 m, walls 2 m, zinc or thatch-look roof, door 0.8×1.8 m with a cloth.
  - `sacred_tree`: large tree (crown 15–20 m) with cloth wrap band 1 m, white #EDEBE4 or red #B5281F (rarer).
  - `enclosure`: 1.2 m low wall or bamboo fence 6×8 m.
  - `pots`: 3–6 clay pots 0.3–0.5 m, terracotta #9A5A3A.
  - `grove`: tree cluster 20×30 m to 1 ha with fence.
- **Colours:** earth tones, white cloth, faded red; whitewashed walls #EFEDE6 with dark grime.
- **Variants:** tree shrine 40%; compound shrine house 30%; palace-precinct shrine 15%; grove 15%.
- **Condition:** mostly worn/old by nature; well-swept ground around active ones; overgrown inactive ones.
- **Props and life:** quiet most of the time; elders sitting nearby; occasional palm-frond decorations; during festivals, crowds and drums.
- **SELECT BY:** `kind=shrine`; old_island (palace precinct) ↑, old towns ↑↑, sprawl villages ↑; adjacency to palace polygons, old trees and unbuilt patches; never on main roads; very low density (1–3 per district).
- **Gidi mapping:** traditional shrines.

---

## 19. Festival structures (generic)

Lagos Island's masquerade festival is held only on special occasions (funerals of Obas or chiefs, coronations, special celebrations); the main Lagos Island highway from the bridge end to a central square is closed and the procession goes to the palace; the masquerades wear white [src: Prime Business Africa, Discover Lagos]. Other festivals impose curfews on some towns, and residents have asked for them to be confined to night [src: NAN on Ikorodu]. Gidi: invent its own festival with white-robed processional figures and palace-square staging; avoid copying any real masquerade's costume or hat.

- **Looks like:**
  - Streets closed with police barriers and tape; crowds lining the route; rows of white/blue canopy tents for dignitaries in front of the palace; a stage with speakers; colourful pennant strings across the streets; banners announcing the festival.
  - Processional figures in flowing white robes with staffs, moving in groups; drummers; spectators in coordinated outfits.
- **Kit parts:**
  - `canopy_tent`: 5×10 m frame tents, white/blue striped or plain white, 3 m eaves, rows of chairs with white covers.
  - `stage`: 8×6 m truss stage with backdrop banner and speaker stacks.
  - `barrier`: 2 m steel crowd barriers; police pickup trucks parked across roads.
  - `pennants`: triangular flags on strings, multicolour.
  - `banner_arch`: inflatable or truss arch 8 m over the road.
- **Colours:** white dominant; palace colours accents (choose a Gidi palace colour, e.g. maroon #7A1F2B and gold); flags multicolour.
- **Variants:** procession day 40%; palace-square ceremony 40%; curfew night (streets empty, shutters closed, a few figures) 20%.
- **Condition:** temporary; after the event: litter, sachets, torn pennants, tents being dismantled.
- **SELECT BY:** event state only; old_island palace square and main street; old towns.
- **Gidi mapping:** festival structures.

---

## 20. Street-life layer for all worship sites

Cross-cutting rules for any worship building. Sources: noise enforcement and decibel limits [src: ThisDay, Gulf News, Guardian, Channels, LASEPA]; road blocking for religious events is illegal and enforced, with named Yaba, Ojokoro and Ikoyi street incidents [src: Ikeja Record 2024]; expressway gridlock on church event nights [src: Pulitzer Center, Guardian 2013, Daily Trust 2017].

- **Loudspeakers:**
  - Mosques: 2–8 horn speakers (grey/white, 0.4–0.6 m bell) on minaret balconies or a pole, angled outwards at four compass points.
  - Churches: column speakers and subwoofers inside; outside horns on the gable or a pole 10–30% [est]; enforcement removes outdoor horns, so newer/elite sites have none.
  - Audio: mosque call 5×/day (dawn ~05:15); church evening services and Friday vigils to 02:00–05:00.
- **Generators:** at every worship site off-grid or as backup: small petrol "I better pass my neighbour" type 0.5×0.4 m beside storefront churches; diesel 20–200 kVA in sound-proof canopies (green, grey, yellow, blue boxes 1×2.5×1.5 m to 1.5×4×2 m) at warehouse churches, central mosques and estate churches; exhaust soot stain on the wall behind.
- **Parking and traffic by day:**
  - Friday 12:00–14:30 near mosques: cars double-parked, side roads closed, worshippers praying on mats in the street.
  - Sunday 07:00–14:00 near churches: both kerbs lined for 100–300 m; ushers in reflective vests; main-road slowdowns.
  - Saturday: weddings and burials (decorated cars, canopies, brass bands).
  - Event nights (camps, crusades): expressway gridlock both ways for hours, buses parked on verges, hawkers in the traffic.
  - Weekdays: low activity; storefront churches closed; mosques with small groups at prayer times.
- **Night lighting:**
  - Mosque: green or white LED floods on dome and minarets, a lit crescent, green LED strings on balconies.
  - Church: lit cross (white or red LED, neon in older), pylon lightbox, glow through louvres, coloured stage light (blue/purple), white floods in car parks.
  - White-garment: candles and fluorescent tubes; white walls glowing.
  - Festive seasons: Ramadan lights on mosques; December Christmas lights on churches and estates.
- **Clutter:** shoe racks/slipper heaps (mosque, white-garment), plastic kettles (mosque), plastic chairs stacked (churches), tent canopies for overflow, banners, offering-box signs, "Do not park in front of this gate" painted on neighbours' gates, water sachet litter after services.
- **SELECT BY:** apply to every worship object by type; scale intensity with capacity, distance to main road (traffic spill only within 300 m of a main road), and time-of-week state.
- **Gidi mapping:** loudspeakers, generators, parked cars on Sunday/Friday, traffic, night lighting.

---

## Selection quick-reference (for the kit's chooser)

| District character | Most common worship objects (in order) [est] |
|---|---|
| dense_mainland | storefront church, small mosque, prayer space, warehouse church, white-garment parish, Jumat mosque, northern mosque (in northern quarters), market mosque |
| sprawl | storefront church, warehouse church, small mosque, white-garment parish, prayer camps along the expressway, megachurch (1 per map), estate churches in estates |
| old_island | small mosque, Jumat mosque, central mosque, heritage mosque, cathedral, old parish church, shrine near palace, festival set |
| old towns (Ikorodu/Epe pattern) | small mosque, old parish church, central mosque, shrine/grove, white-garment parish |
| elite | estate church, modern orthodox church, small modern mosque (white/green, tidy), almost no storefronts, banners minimal |
| civic | central mosque, cathedral/orthodox church, mosque/chapel in government compounds |
| waterfront | stilt small mosque, white-garment parish (timber), shoreline worship ground, storefront church in the market strip |
| port | warehouse church in old sheds, market/prayer spaces at truck parks, northern mosque, small mosque |

Wealth bumps: low → storefront, timber, decayed; mid → warehouse, Jumat; high → estate church, central mosque new.
Main road: banners, pylon signs and billboards ↑; mosque minaret height ↑; back street: small mosque, prayer space, storefront.

---

## Sources

- Lagos Central Mosque (dome, minarets, hall area, frontage): https://en.wikipedia.org/wiki/Lagos_Central_Mosque
- Shitta-Bey Mosque (Afro-Brazilian façade, dates): https://en.wikipedia.org/wiki/Shitta-Bey_Mosque , https://mosqpedia.org/en/mosque/1435 , https://eyesofalagosboy.com/2024/04/29/photo-of-the-week-shitta-bey-mosque-lagos-then-and-now/ , https://mavcor.yale.edu/node/3739
- Afro-Brazilian style in Lagos: https://primeprogressng.com/social-impact/the-afro-brazilian-architecture-that-shaped-lagos-city/ , https://guardian.ng/life/two-cities-one-soul-the-link-between-lagos-and-brazil/ , https://ir.unilag.edu.ng/handle/123456789/7187
- Cathedral Church of Christ (Norman Gothic, 1924–46): https://en.wikipedia.org/wiki/Cathedral_Church_of_Christ,_Lagos
- Holy Cross Cathedral (Gothic Revival, 1934–39): https://en.wikipedia.org/wiki/Holy_Cross_Cathedral,_Lagos , https://www.archnet.org/sites/19868 , https://ir.unilag.edu.ng/handle/123456789/7173
- Lawanson, Planning and Pentecostalism in the spatial (re)configuration of Lagos: https://ir.unilag.edu.ng/handle/123456789/10166 , https://link.springer.com/chapter/10.1007/978-3-030-82475-4_10
- Millington, Garbin, Coleman, Neo-Pentecostal urban infrastructures in Lagos (IJURR 2024): https://www.ijurr.org/article/neo-pentecostal-urban-infrastructures-in-lagos-nigeria-ontology-politics-poetics/
- Adeboye, A Church in a Cinema Hall?: https://ir.unilag.edu.ng/handle/123456789/11873
- Cinema to church in Yaba: https://www.modernghana.com/nollywood/4024/gradually-the-cinemas-return-in-nigeria.html
- USC CRCC on Lagos Pentecostal spaces: https://crcc.usc.edu/?p=75792
- Redemption Camp (area, facilities, population): https://en.wikipedia.org/wiki/Redemption_Camp , https://guardian.ng/sunday-magazine/newsfeature/redemption-city-of-god-where-everything-works/ , https://www.vanguardngr.com/2015/08/expectations-high-as-rccg-all-sufficient-god-convention-begins/
- Faith Tabernacle, Ota (50,400 seats, 1999): https://en.wikipedia.org/wiki/Faith_Tabernacle
- National Geographic, Life in Lagos: the deafening roar of big religion: https://www.nationalgeographic.com/photography/article/life-in-lagos-the-deafening-roar-of-big-religion
- Pulitzer Center, Holy Ghost night traffic: https://www.pulitzercenter.org/stories/getting-ready-holy-ghost-night-lagos-redemption-camp
- Expressway congestion and church events: https://guardian.ng/?p=1013137 , https://www.pressreader.com/nigeria/daily-trust/20170807/281702614804476
- Noise enforcement and decibel limits: https://thisdaylive.com/index.php/2016/07/08/dealing-with-noise-pollution-in-lagos , https://gulfnews.com/world/africa/lagos-shuts-churches-mosques-over-noise-pollution-1.1855656 , https://citifmonline.com/2015/12/nigeria-shuts-down-53-churches-mosques-over-noise-pollution/ , https://www.channelstv.com/2012/05/22/lagos-shuts-down-worship-centres/ , https://guardian.ng/?p=1066106 , https://lasepa.gov.ng/?p=88718 , https://www.thecable.ng/?p=396285
- Road blocking for religious events: https://ikejarecord.com/lagos-taskforce-warns-against-blocking-roads-for-parties-religious-events
- Celestial Church of Christ: https://en.wikipedia.org/wiki/Celestial_Church_of_Christ
- Cherubim and Seraphim: https://en.wikipedia.org/wiki/Cherubim_and_Seraphim_Society
- White garment photo essay: https://themanor.africa/?p=40610
- Beach worship memories: https://eyesofalagosboy.com/2020/06/10/kuramo-beauty-in-the-eyes-of-the-beer-holder/ , https://lifestyle.thecable.ng/?p=213374 , https://en.wikipedia.org/wiki/Kuramo_Beach
- Agege and Hausa settlement, mosque leadership: https://en.wikipedia.org/wiki/Agege , https://gazettengr.com/agege-lg-seals-popular-mosalasi-alhaja-over-leadership-tussle/ , https://guardian.ng/?p=1136818
- Masquerade festival route and occasions: https://www.primebusiness.africa/?p=240475 , https://www.discoverlagos.ng/post/the-return-of-the-eyo-festival
- Festival curfews (Ikorodu): https://nannews.ng/restrict-oro-festival-to-night-ikorodu-residents-plead/
- Existing Gidi research: /Users/Star/gidi/docs/look/research-buildings.md , /Users/Star/gidi/docs/look/research-street.md
