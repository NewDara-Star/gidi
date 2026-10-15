# Lagos housing types beyond the front/back house: a catalogue for the Gidi kit

Scope: every housing type (and the housing-adjacent structures that sit on residential plots) that the Gidi census lists, other than the generic front/back house that `docs/look/research-buildings.md` already covers. This file builds on that document (§0 constants, §1 rooming house, §7 Brazilian house, §8 stilt house, §9 elite) and goes deeper. It does not repeat its paint palette, weathering grammar or sandcrete constants. Use those as the base layer.

Rule zero holds: every real place below is only an example of a pattern. No real building, estate name, logo or brand is to be copied. Census names such as "The Senator's House", "The Gold Island" and "Pearl Towers" are Gidi names. They only borrow the pattern.

Tags: **[src]** is from a listed source (numbered, see the end). **[est]** is my estimate from general knowledge of Lagos streetscapes and building practice. Most dimensions are [est]. Web sources give history and materials, but very few measurements.

Research note: the session's web-search budget ran out part-way through. Elite-modernism, Agboyi creek, and generator-house construction rest more on [est] than the rest.

---

## Summary table

| # | Item | Kit kind(s) | Storeys | Plot / footprint | Districts (Gidi) | Census items covered |
|---|---|---|---|---|---|---|
| 1 | Afro-Brazilian returnee house (sobrado and bungalow) | `brazilian` | 1–3 | 8–15 m frontage, zero setback | old_island | "brazilian house", "Brazilian Quarter" |
| 2 | Stilt house (creek/lagoon) | `stilt` | 1 (rare 2) | 3–6 × 4–8 m | waterfront | "stilt", Makoko-style |
| 3 | Plank walkway, jetty, raft, floating platform | `walkway`, `raft`, `jetty` | — | 0.3–1.2 m wide runs | waterfront | "raft", walkways |
| 4 | Stilt bar / stilt shop / stilt church | `stilt_bar` | 1–2 | 5–8 × 6–10 m | waterfront | "stilt bar" |
| 5 | Creek village (land-edge + stilt mix) | cluster of 2–4 | 1 | village of 30–300 units | waterfront fringe | "Agboyi Creek Villages" |
| 6 | Government estate walk-up flats (1970s–80s) | `estate_flats` | 2–4 | blocks 8–12 × 20–40 m on open lawns | dense_mainland (Festac/Ajegunle-like), sprawl | "flats", "estate" |
| 7 | Estate add-ons: shops in gardens, fenced ground floors | `estate_shop` | 1 | 2.5–4 × 3–6 m | same as 6 | "flats with shops built into gardens" |
| 8 | Face-me-I-face-you rows (yard-row and corridor house) | `rooming_row` | 1–2 | 6–9 × 15–35 m | dense_mainland, old_island fringe | "face-me-I-face-you" |
| 9 | Bungalow types (5 sub-types) | `bungalow` | 1 | 10–18 m wide on ½–1 plot | sprawl, dense_mainland, elite (old) | "bungalow" |
| 10 | Gated-estate duplexes, semis, terraces | `duplex`, `terrace` | 2 (+penthouse) | 6–20 m frontage | elite (GRA/Magodo-like), sprawl (Lekki-like) | "duplex", "terrace", "estate" |
| 11 | Estate gatehouse with barrier | `gatehouse` | 1 | 2.5–6 m booths; gate 8–16 m | elite, sprawl estates, estate flats | "gatehouse", "Estate Gate" |
| 12 | Mansions in five styles | `mansion` | 2–3 (+roof) | 1,000–4,000 m² | elite (Ikoyi/VI/Banana-Island-like) | "mansion", "The Senator's House", "The Gold Island" |
| 13 | Colonial bungalow / villa on leafy avenue | `villa` | 1–2 | 2,000–6,000 m² | elite (old reserve), port (Apapa reserve) | "villa", Apapa reserve, Ikoyi |
| 14 | Glass apartment towers and luxury blocks | `apartment_tower` | 8–35 | 25 × 35 m tower on podium | elite, waterfront-reclaimed | "apartment tower", "Pearl Towers" |
| 15 | High-rise office/residential towers (older concrete) | `tower_old` | 10–25 | 20 × 30 m | old_island, elite, civic | high-rise office/residential |
| 16 | Half-built estates and fenced empty plots | `plot_fenced`, `halfbuilt` | 0–2 | 15 × 30 m plots, sand-filled | sprawl (Lekki/Ibeju-like) | "this land is not for sale" |
| 17 | Shanties along rail lines and under bridges | `shanty` | 1 | 2–4 × 2–4 m | dense_mainland, port, old_island edge | rail/bridge shanties |
| 18 | Beach shacks | `beach_shack` | 1 | 3–6 × 3–6 m | waterfront (ocean side) | beach shacks |
| 19 | Northern (Hausa) community compound | `zango_compound` | 1–2 | 12–25 m courtyard compounds | dense_mainland pockets, old_island (barracks-edge) | northern community |
| 20 | Houses converted to churches, shops, phone malls | `converted_*` | 1–3 | existing plot | dense_mainland, civic (Ikeja-like), elite main roads | converted houses |
| 21 | Boys' quarters (BQ) | `bq` | 1–2 | 3–4 × 8–15 m | everywhere with a main house | "BQ" |
| 22 | Generator house | `generator` | 1 | 1.5 × 2 m to 4 × 6 m | everywhere | "generator" |
| 23 | Stand-alone water tank tower | `water_tank` | — | 2 × 2 to 4 × 4 m base, 3–12 m tall | everywhere, esp. sprawl/estates | "water tank" |

---

## Shared tables (apply to all items)

### A. Plot and setback grammar [src 22 for coverage and setback range; rest est]

| Setting | Plot | Front setback | Side setback | Coverage | Fence |
|---|---|---|---|---|---|
| old_island | 6–15 m frontage × 15–30 m, irregular | 0 m (built to the street line, ground floor often arcaded) | 0 m (party walls) | 85–100% | none; the building is the edge |
| dense_mainland | "1 plot" ≈ 18 × 36 m (648 m²) or half plot 18 × 18 m | 0–3 m (shops to the drain) | 0.6–1.5 m passages | 60–80% (official max 70% for 648 m² high-density [src 22]) | 1.8–2.4 m block wall, often only on sides/back |
| sprawl (old cores) | 1 plot | 3–6 m | 1.5–3 m | 30–50% | 2.1–2.7 m wall, steel gate |
| sprawl (new estates, Lekki-like) | 300–650 m² per unit | 3–6 m | 0–3 m (terraces 0) | 40–60% | estate wall + low unit fences 1.2–1.8 m |
| elite GRA | 1,000–2,500 m² | 6–15 m | 3–6 m | 30–45% | 2.7–3.5 m wall + electric fence |
| elite island (Banana-Island-like) | 1,000–4,000 m² [src 12] | 6–12 m | 3–5 m | 35–50% | 3–3.5 m wall, 0.6 m electric fence |
| government estates | blocks on open land, 10–20 m between blocks | 6–12 m to road | 8–15 m between slabs | 20–30% | originally none; residents add fences |

Lagos permitted setbacks run "generally 3 m to 9 m" [src 22]. Shoreline setbacks on island estates are cited as 30 m, and up to 100–150 m in rules [src 13]. In Gidi, use these as soft rules that are broken more often where wealth is lower and land values are higher.

### B. Condition states (apply per item; item sections list only what differs)

| State | Global changes |
|---|---|
| **new** | Crisp render, saturated paint, clean roof sheet (silver #C9CCCC or coated colour), no streaks. Glass clean. Construction debris (sand pile, block stack) may still be at the plot edge |
| **worn** (5–15 y) | Fading per research-buildings §0, mud band 0.3–0.6 m, streaks under sills, roof dulled to #8C8E8A, rust flecks, a few cracked louvre blades, satellite dishes and AC units added |
| **decayed** (15–40 y unmaintained) | Paint mostly gone, render spalling, rust-through roofs patched with odd sheets, plants in gutters and parapets (fig, fern), broken windows boarded with plywood, wires hanging, informal additions |
| **abandoned / half-built** | No glazing, blocks exposed, starter bars rusting (#7A3E1E), creepers, a "THIS HOUSE IS NOT FOR SALE" or "BEWARE" slogan, a squatter's tarp in one room |

---

## 1. Afro-Brazilian returnee house (sobrado and bungalow)

Builds on research-buildings §7. This section adds the kit breakdown, the Brazilian Quarter street grammar and the decay sequence.

**Looks like**
- A narrow-fronted 2-storey (sometimes 3) house built straight onto the street. A tall ground floor with 3–5 arched openings, and an upper floor with the same number of tall windows over them [src 1, 2, 3].
- Brick (burnt brick [src 5]) under lime/cement stucco. Floral and geometric stucco panels between windows; pilasters at corners; a cornice and a parapet with a central pediment or date panel [src 2, 3].
- Wooden louvred shutters (jalousie) in pairs, often painted a different colour from the walls. Cast/wrought-iron balcony rails on the upper floor [src 1, 3].
- Hipped corrugated roof, often hidden behind the parapet. Ventilation gaps or decorative grilles under the eaves.
- Today: the ground floor is cut open into shop bays with roller shutters, the stucco is half gone with red brick showing through, and a modern 4–6-storey block is squeezed in next door [src 3, 4].

**Kit parts**
- `br_body`: box, frontage 8–15 m (in bays of 2.2–2.6 m), depth 10–20 m, floor-to-floor GF 3.8–4.2 m, upper 3.4–3.8 m [est].
- `br_arch_opening`: semicircular or segmental arch, 1.0–1.2 m wide × 2.4–2.8 m to the crown (GF doors); windows 0.9–1.1 × 2.0–2.4 m [est]. Keystone block 0.2 × 0.3 m.
- `br_shutter_pair`: two leaves of 0.45–0.55 m, horizontal louvres at 60–80 mm pitch, with an optional fixed fanlight in the arch (radial "sunburst" glazing bars or a timber fan).
- `br_pilaster`: 0.3–0.4 m wide, 30–60 mm proud, with a simple capital moulding.
- `br_string_course`: 0.2–0.3 m band at the floor level, 50–80 mm proud.
- `br_stucco_panel`: 0.6 × 0.6 m to 0.8 × 1.2 m rectangles or medallions between windows with floral relief (normal map plus 20–30 mm displacement).
- `br_cornice` + `br_parapet`: cornice 0.3 m, parapet 0.6–1.0 m, balustered or solid, with a central pediment 2–3 m wide × 1–1.5 m high (often carrying a year "18xx/19xx" or initials).
- `br_balcony`: full-width or central balcony 0.8–1.2 m deep on 3–5 iron or stucco brackets; cast-iron railing 1.0 m, with vertical bars and a scroll frieze.
- `br_roof`: hipped corrugated at 20–30°, eaves 0.3–0.5 m where not hidden.
- `br_shop_cut` (modifier): replaces 1–3 GF arches with rectangular openings 2.5–3.2 m wide and a roller shutter (#8F9496 galvanised, or painted blue/green).
- `br_courtyard` (large houses): an internal court 4–8 m square with a gallery on posts [src 1].

**Colours / materials [est unless marked]**

| Part | Fresh | Faded |
|---|---|---|
| Stucco walls | cream #EDE3C8, ochre #E0B04A, salmon #E9A27A, pale blue #9CC7E0, mint #B5D3A0 [src 1: "cream-coloured stucco"] | #CFC3A3, #C9A35A, #C99478, #9FB4BE, #A2B595 |
| Ornament, cornice, arch surrounds | white #F2EFE6 | #D8D2C2 with black #2E3329 in every recess |
| Shutters | bottle green #2F5E3A, oxblood #6B1F22, brown #5A3A28, faded teal #3F7A78 | grey-silvered timber #7D7466 where paint is gone |
| Exposed brick | #9A4E34 to #7E3F2B | with white efflorescence #E5E0D6 |
| Iron rail | black #1E1E1E, or green to match the shutters | rust #8A4B22 |

**Variants and shares [est]**
- 2-storey sobrado with balcony: 45%.
- Single-storey "returnee bungalow" with a front veranda on 4–6 posts: 35%.
- 3-storey merchant house with a pediment and courtyard: 10%.
- Religious/communal (a mosque or church built by returnee masons, with the same ornament scaled up): 10%.

**Condition states**
- **restored** (rare, 5%): crisp white ornament, fresh shutters, plaque, potted plants.
- **worn** (40%): faded colour, a few missing shutter louvres, ground-floor shops.
- **decayed** (45%): 30–60% of the stucco gone in patches (larger at the base and the parapet), shutters missing or nailed shut with plywood, a tree growing from the cornice, roof sheets rusted through, an upper floor maybe unoccupied.
- **ruin/demolition** (10%): roofless shell, or a demolition-site hoarding next to an "X" mark. This follows real heritage losses [src 4, 5].

**Props and life**
- Day: shopkeepers at the GF bays (fabric, cosmetics, mobile accessories), goods hung on the shutters, a parked keke at the kerb, a hand-painted name board over each bay. Grandmothers sitting in the doorway on the veranda type. Overhead wires sagging across the narrow street.
- Night: shops shuttered; single bulbs or LED tubes on the upper floors; a lantern-lit food seller at the corner.
- A heritage plaque (a generic dark-green panel with white text) on 1 in 20.

**SELECT BY**: district = old_island (core weight 1.0; fringe/Ebute-Metta-like 0.3); age band = oldest; main road → `br_shop_cut` probability 0.8 (back street 0.3); wealth low-mid → decayed; a seed picks the 5% restored. In a "Brazilian Quarter" sub-zone, raise density to 40–60% of frontages and keep streets at 5–8 m wide.

**Gidi mapping**: "brazilian house", "Brazilian Quarter".

---

## 2. Stilt house (lagoon and creek)

Builds on research-buildings §8. This section adds the kit and the life layer.

**Looks like**
- Single-room or two-room timber boxes on a forest of thin posts, 1–2 m above dark water. Wall boards are mismatched, roofs are rusty corrugated sheets, and patches of polythene come in many colours [src 6, 7, 21].
- Most are grey, silver and rust from a distance. Bright accents come from tarps, washing, a painted church and branded canoes [src 7].
- Each house has a small front deck where a canoe ties up. Fish are smoked on top of some houses [src 7].
- Electric wires are strung over the water on leaning poles [src 7].
- Houses huddle in irregular rows along 2–5 m canals [est], with no clear grid [src 7].

**Kit parts**
- `st_post`: 0.08–0.15 m round or 0.1 m square timber, 2.5–4 m long (1–2 m visible), on a grid of 1.2–2.0 m, with extra diagonal braces on 1 in 4 bays [est]. (Rail-line shanty posts are cited as driven up to 18 ft into swampy ground [src 20]. Lagoon posts are similar.)
- `st_floor`: plank deck 25–40 mm on 75 × 100 mm joists, floor level 1.0–2.0 m above the water.
- `st_body`: 3–6 × 4–8 m, wall 2.2–2.5 m. Planks are 150–300 mm wide, laid horizontally (60%) or vertically (40%), with gaps of 5–20 mm. Some walls are bamboo mat panels (15%) [src 6].
- `st_window`: unglazed 0.6 × 0.6 m openings with a hinged plank flap, 1–2 per wall.
- `st_door`: plank door 0.7 × 1.8 m opening onto the deck.
- `st_roof`: mono-pitch 10–20° or low gable, corrugated sheet, 0.3–0.6 m overhang on the canal side, held down with old tyres or stones on 1 in 5. Polythene patches 1–3 m².
- `st_deck`: front platform 1–2 m deep across the width, sometimes with a plank bench and a fish-smoking drum.
- `st_latrine`: 1 × 1 m plank box on 4 posts over the water, low door, shared by about 15 households [src 21].

**Colours / materials [est]**
- Fresh plank #8B6E4E; weathered #6E6152; wet base #4A4036; algae line #3A4A30.
- Roof: rust #7A4524, older #5B3420, newer sheet patches #B7BBBD.
- Polythene and tarps: blue #2E6FB7, orange #E07B2A, black #1F1F1F, clear grey #C8CCC8.
- Painted boards (20% of houses): faded blue #5E86A6, green #5E8A5A, yellow #CBB15A.
- Water: #2A2620 with a white scum ring around posts [src 21]; floating PET bottles and hyacinth.

**Variants**
- Plank, one room: 55%.
- Plank, 2–3 rooms with a deck: 20%.
- Bamboo-walled: 15%.
- 2-storey timber "high rise": 3% [src 7].
- Shoreline hybrid with a block lower course: 7%.

**Condition states**
- **new**: yellow-brown planks, silver roof.
- **worn**: grey planks, rust, patches (the default).
- **decayed**: a leaning frame (1–5° tilt), missing boards, roof half tarp.
- **demolished**: post stumps only, charred boards floating. Waterfront demolitions are a recurring real event [src 11, 21].

**Props and life**
- Day: dugout canoes (5–8 m long, 0.7–1.0 m beam, black-brown hull, some branded with paint), women selling food and goods from canoes [src 7], children paddling, nets drying on poles, fish-smoking drums with grey smoke, jerrycans (yellow #E5C12E) bought from shore [src 21], washing lines.
- Night: very dark. A few battery LEDs, a TV glow at a viewing centre, generator hum at a bar or church, lanterns on canoes.

**SELECT BY**: district = waterfront; terrain = water within 0–200 m of the shore; wealth lowest; storeys 1 (2 with p = 0.03 near a community hub). Pair with walkway, raft, sawmill and canoe props.

**Gidi mapping**: "stilt", Makoko-style houses.

---

## 3. Plank walkways, jetties, rafts and floating platforms

**Looks like**
- Narrow, sagging plank catwalks that run house to house, sometimes with one handrail pole. A dilapidated wooden bridge leads to some homes [src 7].
- Shore jetties of concrete or piled timber where canoes moor side by side [src 7].
- Rafts: rafts of logs waiting for the sawmill float in the water, and fishermen stand on floating logs to cast nets [src 7]. Platforms float on plastic drums (the community has a well-known drum-buoyed precedent [src 8, 9]).

**Kit parts [est]**
- `wk_catwalk`: 0.3–0.6 m wide (2–3 planks), on posts every 1.5–2.5 m, 0.6–1.5 m above water, with a sag of 50–150 mm per span. Optional handrail pole at 0.9 m on one side (30%).
- `wk_bridge`: 0.8–1.2 m wide, span 3–6 m, crossing canals, handrails both sides (60%).
- `jetty_concrete`: 2–4 m wide × 8–20 m long slab on piers, with steps to the water. Grey #8E8A80 with green-black tide marks.
- `jetty_timber`: 1.5–3 m wide, piles at 2 m.
- `raft_log`: 10–40 logs, 0.4–0.9 m diameter, 6–12 m long, chained in a mat. Bark brown #5B4433, cut ends pale #C9A776.
- `raft_drum`: a timber deck 3 × 3 m to 6 × 6 m on blue (#2B5FA8) or black plastic drums (0.6 m diameter), freeboard 0.3–0.5 m. It carries a shed, a pump, a fish pen or a small shop.
- `raft_sawdust`: low islands of sawdust/rubbish fill at the shore, 0.2–0.6 m above water, colour #B08A5B to #6D5A44.

**Variants**: catwalk 60%, bridge 15%, jetty 10%, drum platform 5%, log raft 10% (log rafts appear only near sawmills).

**Condition**: new planks pale; worn grey; decayed with missing planks (gaps of 1 in 6) and a broken handrail.

**Props and life**: canoes nosed to jetties, outboard canoes with a yellow fuel can, bamboo push-poles 4–6 m, a man asleep on a log raft, boys diving from the bridge. At night, one bulb at the jetty head.

**SELECT BY**: waterfront; between stilt houses (catwalk density ∝ house density); jetties at shore streets ending in water; log rafts within 150 m of a sawmill (Okobaba-like).

**Gidi mapping**: "raft", walkways and platforms of creek villages.

---

## 4. Stilt bar (and stilt shop / stilt church / stilt clinic)

**Looks like**
- A larger stilt structure, 2–3 times the area of a house, with a wide open deck on the canal side, plastic chairs and a hand-painted name board. Music plays from a speaker [est].
- Community buildings on stilts in the same idiom: a brightly painted church [src 7], a betting kiosk, a football viewing centre, a clinic, a kindergarten [src 7].

**Kit parts [est]**
- `sb_body`: 5–8 × 6–10 m on a heavier post grid (0.15–0.2 m posts at 1.5 m). Wall boards only on 2–3 sides; the canal side is open with a 1.0 m half-wall.
- `sb_deck`: 2–3 m wide wraparound deck with a plank rail.
- `sb_roof`: gable corrugated at 15–20° with a 0.8–1.2 m overhang. Bars favour a painted fascia board 0.4 m high carrying the bar's name.
- `sb_sign`: hand-painted board 2–3 × 0.6 m, or a stretched banner with a beer-style livery (generic: a green-and-gold or a red-and-white drinks band).
- `sb_upper` (20%): a second storey lookout or a "VIP" room under a lower roof.
- Church variant: painted all over in bright blue #2E6FB7, white and yellow, with a cross on the gable and a bell or speaker horn.

**Colours**: base as §2. Bars paint the fascia and front boards in loud colours: red #C8322D, yellow #F2C230, green #2F8F4E, blue #2E6FB7. These fade to chalky versions within 2 years.

**Variants**: bar 40%, provisions shop/kiosk 25%, church 15%, viewing centre/betting 10%, clinic/school 10%.

**Condition**: as §2. Bars are the best maintained, repainted each festive season.

**Props and life**
- Day: plastic chairs (white #F2F2F0, red #C8322D) and tables, crates of bottles, a chest freezer, a canoe "car park" of 4–10 canoes.
- Night: the brightest building in the village. A string of coloured bulbs, a fluorescent tube, generator noise, a TV with football, 10–30 people.

**SELECT BY**: waterfront; one per 30–60 stilt houses; on a main canal or junction; near a jetty.

**Gidi mapping**: "stilt bar".

---

## 5. Creek villages (land-edge + stilt mix, Agboyi-like)

**Looks like [est; thin sources]**
- Small fishing/farming villages on creek banks, mangrove and raffia palm edges. One or two sandy lanes lead to the water.
- On land: bungalows of block or plank with zinc roofs, a church and a mosque, a primary school, a jetty. At the water: a fringe of stilt houses, canoe sheds and fish-drying racks.
- Lower density and greener than a lagoon slum (about a third of Makoko-type settlements are on stilts, the rest on land [src 11]).

**Kit parts [est]**
- Land house: §9 bungalow (mud-block or sandcrete, often unpainted), or a 3 × 5 m plank house on a 0.3–0.5 m block plinth.
- `ck_canoe_shed`: open shed 3 × 8 m, posts plus mono-pitch zinc roof.
- `ck_drying_rack`: raised bamboo racks 1.0 m high × 2 × 4 m with split fish; smoke huts 2 × 2 m of block with a blackened roof.
- `ck_jetty`: §3 timber jetty.
- `ck_bank`: sandbag or tyre retaining walls 0.5–1.0 m, and a mangrove fringe.

**Colours**: sand path #D6C6A0; laterite #A65E3A; mangrove #3E5B35; raffia #6E8A3E; water #3B3A2A (browner than the lagoon).

**Variants**: land-majority village 60%; mixed 30%; mostly stilt 10%.

**Condition**: generally worn or decayed. A few new block houses with silver roofs mark remittance money.

**Props and life**: goats, chickens, a generator at the church, nets, a long canoe ferry with an outboard engine and passengers in life jackets (rare) or none, women processing fish, sawdust, a football pitch of sand.

**SELECT BY**: waterfront districts that touch creeks rather than the open lagoon; distance from the city core is high; density low.

**Gidi mapping**: "Agboyi Creek Villages", floating/stilt platforms of creek villages.

---

## 6. Government estate walk-up flats (1970s–80s; Festac/Jakande/1004-style)

**Background [src].**
- A federal festival town of about 5,000 dwelling units, master-planned on a grid of numbered avenues with alphabetical "closes" and three main gates off an expressway [src 14, 15].
- A state low-cost programme built 16 estates [src 16, 17]. The largest has more than 1,000 blocks of 2- and 3-storey buildings: about 4,272 units, split 2,112 two-bed and 2,160 three-bed [src 17]. The blocks were designed for a 25-year life and decayed after maintenance stopped; some collapsed [src 16].
- An elite federal estate on the island mixed 6 high-rises, 4 low-rises and 4 condominium clusters, with over 1,000 flats on 11 ha [src 18].

**Looks like**
- Long, plain slab blocks of identical flats, 2–4 storeys, repeated in rows on open ground. Flat or low hipped roofs. Every flat has the same balcony and window, so the façade is a strict grid [est].
- Open stairwells with breeze-block (decorative perforated concrete) screens, or open landings with a steel railing.
- Original colour: one estate-wide tone (cream, pale yellow, light grey) with a darker band. Today, each flat owner repaints their own balcony and burglar bars, so the grid has become a patchwork.
- Ground and gardens are invaded by shops, kiosks, churches, mechanic sheds and fences [src 15] (see §7).
- Numbered blocks: large stencilled block numbers ("Block 23", "Flat 4") on the gable end.

**Kit parts [est]**
- `ef_block`: slab 8–11 m deep × 18–40 m long, made of 2–4 stair "cores" each serving 2 flats per floor. Floor-to-floor 2.9–3.1 m, so a 4-storey block (G+3) is 12–13 m to the parapet.
- `ef_bay`: flat bay 7–9 m wide: living-room window 2.4 × 1.2 m (originally naco louvres), bedroom windows 1.2 × 1.2 m.
- `ef_balcony`: recessed or projecting, 1.2–1.5 m deep × 3–4 m wide, with a solid parapet 1.0 m or a steel rail. Often later enclosed with burglar bars, glass or louvres (50% enclosed in worn/decayed).
- `ef_stair_core`: 2.6–3 m wide; open front screen of breeze blocks (300 × 300 mm units, patterns: circles, crosses, diamonds) running the full height, or open landings.
- `ef_roof`: flat slab with a 0.5–0.8 m parapet and black plastic tanks (60%), or a low-pitch hipped zinc (40%; common in state low-cost blocks).
- `ef_gable_number`: block number painted 0.6–1.0 m high, black or white.
- `ef_bungalow_row` (estate variant): 1-storey semi-detached or terraced estate bungalows and 2-storey duplexes in the same colour, on 15 × 30 m plots (Festac-type phases mixed flats with these) [est].

**Layout**: blocks parallel or in staggered rows 12–20 m apart, with grass verges, road reserves 15–30 m, open drains, a few mature almond/neem trees, and parking courts. Original: no fences. Now, chain-link, block walls and gates around single blocks (60%).

**Colours [est]**
- Original body: cream #E8DCB8, pale yellow #EDD58A, light grey #BFC0BA, salmon #E9B595.
- Band: brown #6E4B33, maroon #7A2E2E, dark green #2F5E3A.
- Per-flat repaints: random from the main palette, applied per balcony bay.
- Breeze blocks: unpainted grey #A9A69C or white.

**Variants**
- 3-storey low-cost walk-up (state type): 45%.
- 4-storey federal walk-up: 25%.
- 2-storey "4-flat" block: 15%.
- Estate bungalows/duplex rows: 10%.
- High-rise point block 8–15 floors (elite federal type): 5%.

**Condition states**
- **new (1977–85 look)**: uniform colour, open lawns, no fences, naco windows. Not used in the present day except for flashbacks.
- **worn**: patchwork repaints, enclosed balconies, satellite dishes, fences.
- **decayed** (the default for low-cost blocks): black streaks from every slab edge, exposed rebar at balcony soffits, broken breeze blocks, sagging wires, overflowing tanks, a cracked façade.
- **condemned**: red "X" plus "LASBCA"-style generic stencil ("VACATE"), windows empty, one block propped with timber.

**Props and life**
- Day: generators lined up on the ground floor (one per flat, small "I-better-pass-my-neighbour" sets, red #C8322D or yellow #E5C12E), wires up the façade, clothes on balcony rails, kids playing football between blocks, keke stands at the estate gate, water vendors with "mai ruwa" carts.
- Night: a chequerboard of lit and dark flats. Generator roar at 7–11 pm. Security guards at the block gate.

**SELECT BY**: district = dense_mainland (Festac/Ajegunle-like) or sprawl (older estates). Kind estate; storeys 2–4; layout regular (a grid district patch). Wealth low-mid; age old → decayed. Near an estate gate (§11): a main-avenue frontage gets §7 shops.

**Gidi mapping**: "flats", "estate", government low-cost housing, 3–4-storey walk-ups.

---

## 7. Estate add-ons: shops built into gardens and setbacks

**Looks like**
- The lawn in front of a block of flats is filled with a line of 1-storey lock-up shops, kiosks and container shops facing the avenue. Each is a different colour with its own sign, so the block behind is hidden [src 15].
- Mechanic sheds, churches in tents and "buffer zone" shanties fill the leftover land [src 15].

**Kit parts [est]**
- `es_lockup`: block shop 2.5–3.5 m wide × 3–6 m deep × 2.7–3.0 m tall, with a flat slab roof or mono-pitch zinc falling to the back, a steel roller or folding door, and a 0.3–0.6 m parapet sign band. Built in rows of 3–12 along the boundary.
- `es_container`: 20 ft container (6.06 × 2.44 × 2.59 m) with a cut-out front.
- `es_canopy`: a zinc canopy 1.5–2.5 m deep on steel poles in front.
- `es_tent_church`: steel frame plus white/blue tarpaulin 10 × 20 m, plastic chairs inside.

**Colours**: per shop, from the bright palette (red, yellow, blue, green) or a telecom-style livery band (generic yellow, green or red brand bands painted on the full shop front).

**Variants**: lock-up row 50%, containers 20%, kiosks 20%, tent church/mechanic 10%.

**Condition**: always worn. Demolished shops leave stub walls and rubble (FHA-type clearance [src 15]).

**SELECT BY**: estate flats (§6) facing a main avenue or estate gate; p = 0.7 on main avenues, 0.2 on closes.

**Gidi mapping**: "flats with shops built into gardens".

---

## 8. Face-me-I-face-you rows

research-buildings §1.1 covers the corridor house. This section adds the **yard-row** and **compound-ring** forms and the kit parts that make the rooms legible.

**Looks like**
- **Corridor house** (60%): a central corridor with rooms facing each other.
- **Yard row** (25%): a single-loaded row of 4–10 rooms in one line with a narrow open veranda in front, facing a wall or a matching row across a 2–4 m yard. "Face-me" here means two rows facing across the yard.
- **Compound ring** (15%): rooms around three or four sides of a court, the old-island/ Ebute-Metta pattern.
- Every room door carries a number painted on it. Doors are steel or plank with a curtain behind; windows are wooden louvre or glass louvre with bars. There is a rope washing line across the yard, shared toilets at the end, and a stack of jerrycans.

**Kit parts [est]**
- `ff_room_cell`: 3.0–3.6 m × 3.0–3.6 m, wall height 3.0 m.
- `ff_door`: 0.8–0.9 × 2.1 m; steel sheet (painted brown #5A3A28, green #2F5E3A, or blue) 50%, flush plank 40%, with a curtain 10%. A room number 0.1 m high in white paint.
- `ff_window`: 1.2 × 1.2 m naco louvre (6–8 glass blades) behind a bar grille; wooden shutters on older ones.
- `ff_veranda` (yard row): 1.2–1.8 m deep, concrete floor raised 0.3–0.45 m, posts 0.23 m square at 3–3.6 m centres, a zinc lean-to roof.
- `ff_yard`: 2–4 m wide concrete or bare earth, a central open drain 0.3 m wide.
- `ff_toilet_block`: 2–4 cubicles 1.2 × 1.5 m, plus a bathroom; a 2.4 m high mono-pitch roof; a rusty steel door; a water drum.
- `ff_kitchen_line`: kerosene stoves on stools outside each door, or a lean-to "kitchen" row 1.5 m deep.

**Colours**: per research-buildings §0. Room doors differ (each tenant paints their own) in 40% of houses.

**Variants**: corridor 60% / yard row 25% / ring 15%. Storeys: 1 (70%), 2 (30%; external concrete stair to an upper gallery with a steel rail).

**Condition**: worn 50%, decayed 45%, new 5% (new block-built "face-me" rows on sprawl edges, unpainted, with silver roofs).

**Props and life**
- Day: washing on lines, plastic basins, children, a woman frying akara at the gate, a generator on the veranda, a "To Let: Room" sign 1 in 10.
- Night: one bulb per door (where there is power), many rechargeable lanterns, the radio, a gate locked at 10 pm with a padlock.

**SELECT BY**: dense_mainland and old_island fringe; wealth low; back plots (yard row favoured on back plots, corridor on front plots); storeys 1–2.

**Gidi mapping**: "face-me-I-face-you" rows.

---

## 9. Bungalow types

**Looks like**: single-storey detached houses behind a compound wall, with hip roofs, a front porch on columns and burglar-barred windows. They are the default house of sprawl suburbs [est].

**Sub-types and kit parts [est]**

| Sub-type | Share (sprawl) | Footprint | Distinctives |
|---|---|---|---|
| `bg_two_flat` ("2 × 3-bedroom flats") | 35% | 15–18 × 12–14 m | Symmetrical: two front doors, two porches or one central porch, 4–6 windows across, one hipped roof |
| `bg_detached_family` (3–4 bed) | 25% | 12–16 × 12–15 m | One central porch with 2–4 columns, a car port at the side (zinc or tensile), a decorative gable over the porch |
| `bg_mini_flats` (row of 2–4 "self-contain"/mini-flats) | 15% | 6–8 × 20–30 m | Like a yard row but each unit has its own door, window and porch step |
| `bg_old_hipped` (1960s–70s owner-built, "Lagos bungalow") | 15% | 10–14 × 10–14 m | Steep hip at 25–30°, asbestos or aged zinc, naco windows, a front veranda across the full width, a terrazzo step |
| `bg_unfinished` (bungalow with a raised second-floor slab or starter columns) | 10% | as above | Concrete slab instead of a roof, 4–12 starter columns with rusty rebar, a water tank on the slab, a "future upstairs" plan |

**Common parts**
- Eaves 3.0–3.3 m; plinth 0.45–0.9 m with 3–5 steps; ridge 5–6.5 m.
- Hipped roof 20–30° with 0.45–0.6 m overhang; fascia board 0.2–0.3 m, painted.
- Porch: 2–4 columns 0.23–0.3 m square (round 20%), a flat slab over with a parapet, or a gable "pediment" (30%).
- Windows: casement aluminium (newer, 40%, bronze-tinted glass #4F4A3F); naco louvre (older, 50%); wooden (10%). 1.2 × 1.2 m to 1.5 × 1.8 m, behind steel bar grilles.
- Doors: security steel door ("Turkish"-style pressed panel, dark brown #4A3326 or gold-trimmed) on newer houses; panel timber on older.
- Wall/gate: 2.1–2.7 m block wall (often only half-rendered), a steel sliding or swing gate 3–4 m wide, a pedestrian door within.

**Colours**: research-buildings §0 palette. Sprawl favours cream, peach, sky blue and two-tone with a brown/maroon base band 0.6–0.9 m high (35% of bungalows) [est].

**Condition**: new (silver/coated roof, bright paint, no mud band) 20%; worn 55%; decayed 20%; abandoned 5%.

**Props and life**: a car under the car port; a generator by the gate; a water tank on a stand (§23); plantain and pawpaw in the yard; a dog; laundry; a "Beware of Dog" plaque; a "Pentecostal" sticker on the gate; a satellite dish on the roof. At night a security bulb over the gate and a bulb on the porch.

**SELECT BY**: storeys = 1; district sprawl (weight 0.6), dense_mainland (0.25), old elite GRA (bg_old_hipped, 0.1); distance from the main road large (bungalows dominate back streets). Wealth low-mid → two_flat/mini_flats; mid → detached_family; aspiring → unfinished.

**Gidi mapping**: "bungalow" types.

---

## 10. Gated-estate duplexes, semi-detached houses and terraces

**Looks like**
- Inside a walled estate, repeated 2-storey houses in a uniform developer style along paved closes with kerbs, streetlights and planted verges [src 24].
- Two eras:
  - **1990s–2000s GRA/Magodo/Omole-type**: owner-built detached duplexes, each different. Stone-coated multi-hip roofs, cream/peach render, columned porches, balconies with balusters.
  - **2010s+ Lekki-type developer estates**: uniform terraces and semi-detached units. Grey/white/charcoal contemporary boxes with flat or butterfly roofs, a "pop-out" frame around windows, glass balcony rails, and a small front car pad [src 24].
- Listings describe 4-bed terraces on 280–650 m² per unit, often with a BQ [src 23, 24].

**Kit parts [est]**
- `dx_detached`: 12–18 × 12–16 m, 2 storeys at 3.3–3.6 m, plus a penthouse/roof terrace (25%). On 600–1,000 m² plots. Front setback 6–10 m with interlocking paving; a car port for 2–3 cars.
- `dx_semi`: a mirrored pair, 9–12 m frontage each, a shared party wall, a single roof.
- `dx_terrace`: 3–8 units, 6–8 m frontage each, 10–14 m deep, with a stagger of 0.5–1.5 m every 1–2 units. Each unit has a front car pad 5–6 m, a low wall 1.2 m, and a gate 3 m.
- `dx_maisonette`/stacked: a 3–4-storey block containing 2 duplexes, one above the other.
- Façade parts: a "pop-out" window frame (a 0.2–0.3 m rendered border, charcoal), a vertical feature wall of stone tile or a wood-look strip, frameless glass or steel balcony rails, a double-height entrance glazing strip, a flat roof with a 0.6–1.2 m parapet hiding tanks; or stone-coated hip roofs (classic).
- Windows: aluminium sliding/casement in black or charcoal frames, tinted (bronze #4F4A3F, blue-green #3F5E5E, or reflective silver #9DA4A8).
- Gate: one steel gate per unit, 3–3.5 m wide, sliding, laser-cut pattern panels (contemporary) or spear-top railings (classic). Painted black, charcoal or gold-trimmed.

**Colours [est]**

| Style | Wall | Accent | Roof |
|---|---|---|---|
| Classic | cream #EDE3C8, peach #F2C9A8, sand #D9C3A0 | white trim; brown windows #4A3326 | stone-coated terracotta #8E3B2A, charcoal #3A3C3E, wine #5A2430, green #3E5B3A |
| Contemporary | white #F5F5F2, light grey #C9C8C3 | charcoal #3A3C3E, wood-look #8A5A36, black frames | flat (parapet) |

**Variants (in Lekki-like sprawl estates)**: terrace 40%, semi 25%, detached 25%, stacked maisonette 10%. GRA-like elite: detached 80%, semi 15%, terrace 5%.

**Condition**
- **new/completed**: clean.
- **worn**: black streaks under white parapets within 2–3 years.
- **half-built** (in sprawl, 30% of estate plots): see §16.
- **flood-stained**: a 0.3–0.6 m tide line on low-lying estates.

**Props and life**: an SUV on the car pad, a solar panel array (rising: 10–20% of new units), an inverter-battery box, an AC condenser per room (1–2 per bay) with drain stains, a water-tank cage on the roof, small palms/ixora hedges, a security guard on a plastic chair at the estate entrance, a delivery motorbike. At night: wall lights washing up the façade (warm white), LED strip lights under parapets on contemporary units, perimeter floodlights.

**SELECT BY**: elite (GRA/Magodo-like: classic detached), sprawl (Lekki-like: contemporary terrace/semi). Storeys 2. Inside an estate polygon that has a §11 gate. Wealth mid-high. A seed decides whether the estate is "uniform developer" (all units same style and colour ±5%) or "owner-built" (each unit random).

**Gidi mapping**: duplexes and terraces in gated estates, "estate".

---

## 11. Estate gatehouse with barrier ("Estate Gate")

Residents' associations close estate gates and post private guards at them. The gate is a site of real disputes (lockdowns, guards refusing entry to officials) [src 19]. This section is the full kit; research-buildings §10.15 has only a stub.

**Looks like**
- A road-spanning entrance on the estate's perimeter wall: a pair of masonry piers or an arch with the estate's name in raised letters, one or two lanes, a red-and-white boom barrier (or a manual steel bar on a pivot), and a guard hut beside it.
- Rules boards: "Visitors must register", "No hawkers", "No okada beyond this point", "Speed limit 10 km/h", "Gate closes 11 pm to 5 am".
- Okadas and kekes wait outside because they are not allowed in. A drain bridge and speed bumps sit in front.

**Kit parts [est]**
- `eg_hut`: 2.5 × 2.5 m (small) to 3 × 5 m (2-room: guard room plus toilet), 2.6–3 m tall, flat slab with 0.3 m parapet or a mini hip zinc roof. Sliding glass or louvre windows on 3 sides (for viewing), 0.9–1.2 m sill. Door 0.9 m. Elite: a glazed booth with tinted glass and a pyramid roof.
- `eg_barrier`: boom arm 4–6 m long, 0.1 m square/round, red/white stripes at 0.5 m (red #C8322D, white #F2F2F0), on a 1.0 m high post. Manual variant: a steel pipe with a counterweight of concrete-filled tin.
- `eg_gate`: steel double or sliding gate 6–10 m (spans the road), 2.4–3 m tall, black or green with spear tops; a pedestrian door.
- `eg_piers`: 0.6–1.0 m square, 3–4.5 m tall, caps with globe lamps or pyramid tops; an arch (35%) spanning 8–16 m with a sign band 0.6–1.0 m.
- `eg_name`: raised letters 0.3–0.5 m, gold/brass on a dark band or black on a cream band. Gidi-invented names only.
- `eg_speedbump`: 2–3 humps, 0.1 m high, yellow/black.
- `eg_rules_board`: 1.2 × 0.9 m painted steel on poles, white text on blue or red.
- `eg_drum_chicane` (low-cost estates): oil drums painted red/white or tyres filled with concrete.

**Variants [est]**
- Elite estate with arch and booth: 25%.
- Mid estate with piers, steel gate and block hut: 45%.
- Street gate (residents' association closing a public street, a steel bar gate with a hut): 25%.
- Barricade of drums/a rope only (low-cost): 5%.

**Condition**: elite new. Mid estates worn (rusty gate, faded stripes). Street gates decayed (a broken barrier replaced by a rope or a bamboo pole).

**Props and life**: 1–3 guards in dark uniform (navy/khaki) or a local vigilante in a yellow vest; a plastic chair and a bench; a visitors' log book on a table; a fan; a phone charging extension; a small generator; okada riders waiting outside; a kiosk selling recharge cards just outside the wall. At night: a floodlight on a pier, the gate closed, a torch, a radio playing, horns honking to be let in.

**SELECT BY**: at each estate polygon's road entry points (1–3 per estate); elite → arch/booth; sprawl estates → piers; dense_mainland closes → street gate (p = 0.3 on residential side streets off a main road). Estate flats (§6) get a pier-and-gate form at the main avenue.

**Gidi mapping**: "gatehouse", "Estate Gate".

---

## 12. Mansions in five styles (Ikoyi/VI/Banana-Island-like)

Island elite plots of 1,000–4,000 m² [src 12]. The first island-estate houses were described as in "British and Dubai traditional styles", ostentatious with large gardens. Newer ones go modern with straight lines on smaller plots, and with height caps that are enforced unevenly (demolitions and a building ban followed a collapse) [src 12, 13]. Newer architect-designed houses show deep reveals, natural stone, smooth plaster and big aluminium glazing [src 25, 26].

Share in a Gidi elite-island district [est]: colonial bungalow 8%, 1970s modernist 12%, neo-classical 30%, contemporary box 35%, Dubai style 15%.

### 12a. Colonial bungalow (see §13 for detail)
Large single-storey or raised house with deep verandas, a broad hipped roof and lawns. In an elite-island district they read as the "old money" pocket.

### 12b. 1970s–80s modernist house
**Looks like**: horizontal 2-storey concrete house; a flat roof with a thick fascia; a deep cantilever over a terrace; vertical concrete fins or a breeze-block screen wall (brise-soleil); strip windows; an exposed board-marked concrete or a pebble-dash/"tyrolean" render; a carport under the first floor [est].
**Kit**: body 18–25 × 12–15 m; floor-to-floor 3.3 m; fascia 0.6–0.9 m; fins 0.15 × 0.6 m at 1.0–1.2 m; screen walls of 300 mm breeze blocks; louvre strip windows 0.9 m tall.
**Colours**: off-white #E7E2D6, grey concrete #A9A69C, stained #6E6B63 at the fascia; accent tiles terracotta #9B5B3A or mosaic blue #3C6E9A.
**Condition**: mostly worn/decayed (black fascia streaks, repainted in a brighter colour, plus a new gate).

### 12c. Neo-classical columned mansion ("classic Nigerian mansion")
**Looks like**: symmetrical 2–3-storey house; a double-height portico of 4–8 Corinthian or Ionic columns (0.5–0.8 m diameter, 7–8 m tall); a triangular pediment or curved balcony over the entrance; baluster balconies; arched windows with keystones; quoins at corners; a multi-hip stone-coated roof with a cupola (20%); two gold lions or eagles on the gate piers; a fountain in the forecourt [est].
**Kit**: body 20–30 × 15–20 m; floor-to-floor 3.6–4.0 m; `cl_column` (shaft + capital + base), `cl_pediment`, `cl_balustrade` (balusters 0.6–0.8 m at 0.2 m centres), `cl_quoin` (0.3 × 0.15 m blocks), `cl_dome` (2–4 m diameter).
**Colours**: cream #EDE3C8 and white ornament; or peach #F2C9A8, sand #D9C3A0, pale pink #EBC7C0; roof charcoal #3A3C3E, terracotta #8E3B2A, wine #5A2430, green #3E5B3A; gold accents #C9A04A on gates, rails and lamps.
**Gidi mapping**: "The Senator's House" archetype. Add political props: a flagpole (green-white-green), a 2nd gatehouse, police vans parked outside, a posters wall across the street during campaigns.

### 12d. Contemporary glass and white box
**Looks like**: stacked white and charcoal boxes; a flat roof; cantilevered upper volumes 2–4 m; full-height glazing; frameless glass rails; feature walls of stone or timber-look cladding; a roof terrace with a pergola; a pool visible through a glass rail [src 25, 26].
**Kit**: volumes 8–15 m; floor-to-floor 3.6–4.2 m; `ct_box`, `ct_cantilever`, `ct_glass_wall` (mullions at 1.2–1.5 m, black frames), `ct_fin` (vertical aluminium or timber-look fins 0.05 × 0.2 m at 0.3 m), `ct_pergola`, `ct_lantern` (a glowing glazed stair volume).
**Colours**: white #F5F5F2, warm grey #B5B1A8, charcoal #3A3C3E, timber-look #8A5A36, glass #5E7A80 (day) / #FFE2B0 (lit interior at night).
**Condition**: new or worn (black streaks from parapets, faded timber-look).

### 12e. "Dubai style"
**Looks like**: big and flashy. Tall arched or horseshoe-shaped windows; a mirror-glass curtain wall over the entrance; gold or bronze reflective glass; multi-level balconies with chrome or gold rails; domes or a crown parapet; marble/granite cladding panels; cornices lit with LED strips at night; tall date-palm-like palms in a line along the drive [est; src 12 for "Dubai traditional style"].
**Kit**: body 25–35 × 18–25 m, 3 storeys plus a crown; `db_arch_window` (2–3 m wide × 4–6 m tall), `db_mirror_curtain`, `db_crown_parapet`, `db_dome`; cladding panels 0.6 × 1.2 m.
**Colours**: cream marble #E6DCC8, beige #D2C2A2, gold glass #B59A55, bronze glass #6F5A3C, white; gold rails #C9A04A.
**Gidi mapping**: "The Gold Island" exclusive enclave archetype (mix 12c, 12d and 12e at about 30/40/30, with very large plots, near the water, with private jetties).

### Mansion common parts [est]
- Wall 3.0–3.5 m, rendered and painted the house colour, with 0.5–0.6 m electric fence wires on brackets or razor wire coils, plus CCTV cameras on piers.
- Gate: 5–7 m sliding steel, automated, often a solid panel (no view in); a pedestrian door with an intercom.
- Gatehouse: §11 small hut inside the wall.
- Grounds: interlocking pavers, a lawn, a pool 4 × 10 m, palms (royal palm-like trunks 10–15 m), bougainvillea over walls, a BQ (§21), a generator house (§22), and an underground or stand tank (§23).
- Waterfront plots: a lawn to a sea wall, a jetty with a speedboat.

**Variants by condition**: new 50%, worn 35%, half-built/stalled 10% (a raw concrete frame behind a hoarding), decayed 5% (a disputed estate, grown over).

**Props and life**: SUVs, a driver washing a car outside the gate, guards, a mobile police officer, domestic staff, a gardener with a cutlass. Night: every mansion lit like a hotel (wall washers, floodlights), generators running when the grid fails, a guard dog.

**SELECT BY**: elite (island) + wealth high + plot ≥ 1,000 m²; style chosen by age band (old → 12a/12b; 1990s–2010 → 12c/12e; 2010+ → 12d) and a seed; waterfront proximity raises 12d/12e. Storeys 2–3 (+roof).

**Gidi mapping**: "mansion", "The Senator's House", "The Gold Island".

---

## 13. Colonial bungalow / villa on a leafy avenue (Ikoyi/Apapa reserve-like)

The island cantonment was developed for the British expatriate community and still has many large colonial residences built from about 1900 to 1950 [src 27]. 1920s–30s reclamation laid out new avenues [src 27]. Port towns had a comparable reserve.

**Looks like**
- A wide, low house raised on a plinth or on piers (1.0–1.5 m in early ones), with deep verandas on 2–4 sides, a big hipped roof with wide eaves, and tall timber casement or louvred windows. It is set far back in a lawn of 2,000–6,000 m² under huge trees (rain trees, flamboyant, mango, almond) [est].
- Two-storey variant: a timber or iron upper veranda on columns, an external stair.
- Avenues 15–20 m wide, with no kerbs, grass verges, tree canopies arching over, and low walls (older) or new 3 m walls (now).
- Today many are offices, embassy annexes or clubs, or are being torn down for towers [src 27].

**Kit parts [est]**
- `cv_body`: 15–25 × 12–20 m; floor height 3.6–4.2 m; plinth 0.6–1.5 m with arched vents.
- `cv_veranda`: 2.4–3.6 m deep, posts 0.2–0.3 m square or round (timber or cast iron), a balustrade of timber slats or concrete balusters 0.9 m.
- `cv_roof`: hip or hip-and-gable, 25–35°, eaves overhang 0.9–1.5 m, sheet painted red #8E3B2A or green #3E5B3A (or replaced by stone-coated); ventilating gablets.
- `cv_window`: timber casements 1.0 × 1.8 m with fixed louvred shutters, top-hung fanlights, mosquito mesh.
- `cv_porte_cochere`: car porch 4 × 5 m projecting from the veranda.
- `cv_servants_row`: a §21 BQ row at the rear, plus a detached garage.

**Colours**: white #F2EFE6 or cream #EDE3C8 walls; green #3E5B3A or dark brown #4A3326 woodwork; red/green roofs; lawn #6E8F48; red laterite drive #A65E3A.

**Variants**: single-storey 60%, 2-storey 40%. Use: residence 50%, office/annex 35%, derelict 15%.

**Condition**: maintained (white, lawn cut) 50%; worn 35%; derelict (roof sagging, overgrown, a "LAND FOR LEASE"-type board) 15%.

**Props and life**: old trees, a flagpole (annex), a guard hut at the gate, two cars, a gardener. Night: very quiet, dim lamps, crickets.

**SELECT BY**: elite (oldest sub-zone) and port (Apapa-like reserve); plot ≥ 2,000 m²; age band oldest; distance from a main road medium; next to newer towers in an "infill" mix.

**Gidi mapping**: "villa", Apapa reserve, Ikoyi.

---

## 14. Glass apartment towers and luxury blocks ("Pearl Towers"-like)

A reclaimed-land development's tower cluster has 5 towers of 24–33 floors, of glass, steel, aluminium and reinforced concrete, with penthouses on the top 6–8 floors and 4 apartments per floor [src 28, 29]. Other towers there run 23–33 floors, about 145 m [src 29]. Island towers of 21 storeys have collapsed during construction [src 27].

**Looks like**
- Slender towers on a 2–5-floor parking podium; full curtain-wall glass in blue-green, grey or champagne tints; curved or chamfered plan corners; floor-edge white bands; continuous glass balconies; a lit crown or a sculptural top [est from src 28].
- Mid-rise luxury blocks (8–12 floors): white render plus glass, frameless balcony rails, a gym/pool deck on the roof.
- At the base: a porte-cochère with a canopy, landscaped palms, a guardhouse with a barrier, a generator farm (sound-proof containers) and diesel tanks behind a screen.

**Kit parts [est]**
- `at_podium`: 2–5 floors at 3.0 m; footprint 40 × 60 m; perforated-metal or louvred screens on the car-park floors.
- `at_shaft`: plan 22 × 30 m (4 flats/floor) or 18 × 18 m (2 flats/floor); floor-to-floor 3.2–3.5 m; 12–35 floors.
- `at_curtain`: panels 1.5 × 3.3 m; spandrel bands 0.9 m (opaque).
- `at_balcony`: 2–3 m deep, curved or straight, glass rail 1.1 m.
- `at_crown`: 2–3 floors tall, open frame or lit fins.
- `at_bms`: rooftop plant, water tanks, a helipad marking (rare).

**Colours**: glass blue-green #4F7A82, grey #6E7A82, champagne #B8A57E, dark bronze #4A3F35; frame white #F2F2F0 or silver #C0C4C6; podium cladding beige #CFC3A3. Night: warm interior #FFE2B0 squares in 40–70% of units (lower in new, partly sold towers), white LED crown.

**Variants**: full curtain wall 45%; render + punched glazing 35%; twin/cluster towers 20% (a cluster of 3–5 towers in different glass tints, as in the census "Pearl Towers").

**Condition**: new (clean glass), worn (rust streaks from balcony drains, a few broken or replaced panels with mismatched tint), stalled (concrete frame, tower crane, half the cladding).

**Props and life**: SUVs and a valet, guards with a mirror on a pole checking under cars, a doorman, a boat jetty if on the waterfront. Night: lit lobby, crown lighting, near-silent (central generator in a soundproof housing).

**SELECT BY**: elite (island) or waterfront-reclaimed; wealth high; storeys 8–35; near water or main boulevards; clusters.

**Gidi mapping**: "apartment tower", "Pearl Towers".

---

## 15. High-rise office/residential towers (older concrete stock)

Builds on research-buildings §9.3/§10.1 (an island high-rise sample of 12–25 floors, mostly over 20 years old). Detail added here.

**Looks like**: 1960s–90s towers: a concrete frame grid; projecting sunshade fins or eyebrows over each window; balconies with solid parapets (residential); tinted glass or naco louvres; grey-black streaks over the whole surface; AC boxes in many windows; antennas, telecom masts and big signs on the roof [est].

**Kit parts [est]**
- `to_shaft`: 20 × 30 m; floor-to-floor 3.3–3.6 m; 10–25 floors.
- `to_eyebrow`: 0.6–1.0 m deep horizontal shades at every floor.
- `to_fins`: 0.2 × 0.6–0.9 m vertical fins at 1.2–1.5 m.
- `to_rooftop`: lift motor room 6 × 8 × 3 m; water tanks; a telecom mast 8–15 m; a big branded sign frame (generic).
- `to_ac_box`: split condenser 0.8 × 0.6 × 0.3 m or window unit, on 30–60% of bays.

**Colours**: original white or cream, mostly greyed to #9C988E with streaks #3C3A35; glass bronze #4F4A3F or blue #3F5E7A; mosaic tile spandrels (blue/green) on 20%.

**Variants**: office 50%, residential 35%, mixed 15%. Some refurbished with a new aluminium cladding skin (silver/grey) on the street face only.

**Condition**: worn 50%, decayed 35%, refurbished 10%, abandoned/burnt shell 5%.

**SELECT BY**: old_island CBD, elite, civic; storeys 10–25; main road frontage.

**Gidi mapping**: high-rise office/residential towers.

---

## 16. Half-built estates and fenced empty plots (Lekki/Ibeju-like)

The new-growth corridor is zoned agricultural in parts, and officials say about 80% of buildings there lack approval [src 30]. Land disputes and speculation are rife, and plots trade at ₦1–6 m depending on distance to big projects [src 31, 32]. A fence permit is a first procedural step after planning information [src 30], so fencing a plot is how ownership is claimed.

**Looks like**
- Long stretches of sand-filled land (white-yellow dredged sand) divided by low block fences into rectangles, with a gate opening but no gate. Hand-painted on the fence: "THIS LAND IS NOT FOR SALE", "BEWARE OF 419", "OWNER: [name], [phone]", "BUYER BEWARE", "LAND FOR SALE: CALL …" [est; the slogan genre is in research-buildings §0].
- Estate developments sit at different stages: a grand estate gate and a billboard showing a rendered dream estate, but only 3 finished houses, 10 at roof level, 20 at lintel level and many slabs with starter bars. Grass and casuarina scrub grow between them.
- A guard shack (a "caretaker's" plank hut) on one plot. A water tank on a scaffold. Sand piles and block-moulding yards.

**Kit parts [est]**
- `pf_fence`: 1.0–2.4 m sandcrete wall, unrendered (#A6A196), sometimes 3–6 courses only (0.7–1.4 m), with gaps; a steel gate (rusting) on 30%, a plank or blockwork gate fill on 30%.
- `pf_slogan`: painted letters 0.2–0.4 m tall, red #B02A25 or black #1E1E1E, on a white rendered panel 2–4 m wide. Variants: "NOT FOR SALE", "THIS LAND IS NOT FOR SALE", "BEWARE", "OWNER IS AROUND", "BUYER BEWARE", with a phone number pattern.
- `pf_beacon`: survey beacons (small concrete posts 0.15 × 0.15 × 0.3 m, painted red top) at corners.
- `pf_signboard`: 2.4 × 1.2 m to 6 × 3 m developer board on steel legs, with a rendered image and a big "PLOTS AVAILABLE" (generic, faded); or a "property of [family]" board; or a court-injunction notice board ("SUBJECT TO LITIGATION / DO NOT BUY").
- `pf_caretaker_hut`: 2 × 3 m plank or block hut with a zinc roof.
- `hb_frame`: half-built house stages (re-use research-buildings §5): foundation (DPC plus starter blocks), lintel level (walls 2.1–2.4 m, no slab), slab with starter bars, roof frame without sheets, roofed without plaster.
- `pf_sandfill`: terrain raised 0.5–2.0 m above the original swamp, colour #E6D9B0 (fresh) to #CDBE8E (with grass).

**Variants (share of plots in a Lekki/Ibeju-like sprawl patch)**: empty fenced 35%, empty unfenced with beacons only 15%, half-built 30%, completed 20%.

**Condition**: half-built progresses slowly. Colour changes from fresh grey blocks to green-black algae (2–5 years), rebar rust, trees growing inside rooms (10+ years). Fences crumble at the top course and lose blocks.

**Props and life**: block moulders with moulds and a stack of blocks drying, a tipper truck with sand, labourers (in daytime only), cattle grazing (northern herders, a few cows with long horns), a lone kiosk, a church signboard on an empty plot ("Site of Future Cathedral"). At night: nearly dark, with one or two caretaker lanterns.

**SELECT BY**: sprawl (Lekki/Ibeju-like) far from the core; plot vacancy probability rises with distance from a main road and from completed estates; slogans on 30% of empty-plot fences that face a road.

**Gidi mapping**: half-built estates and fenced empty plots with "this land is not for sale".

---

## 17. Shanties along rail lines and under bridges

Rail-side homes are described as plank frames on planks driven into swampy ground, raised a little above the ground, with planks nailed together hastily, gaps stuffed with rags, polythene or plastic carpet lining, and corrugated roofs that squeak in the wind. Shanties stand a few inches apart behind a row of shops facing the line. There are no toilets, refuse dumps sit in open spaces, and sawdust lies on the ground. One such community had about 11,000 people [src 20]. Lagos regularly clears shanties, stalls, mechanics and bus parks under bridges and along rail corridors, and traders come back within days [src 33, 34, 35].

**Looks like**
- Rail line: a strip of 1-storey shacks and stalls within 2–10 m of the tracks, with trading tables on the ballast itself. Behind them, plank shacks in a dense mat.
- Under a bridge: shacks fitted between the concrete piers, under a ceiling of bridge deck 4–12 m overhead. Mattresses, tarps, cooking smoke, parked minibuses, block moulders and fuel sellers [src 33]. Walls are tarps and boards hung between columns.

**Kit parts [est]**
- `sh_shack`: 2–4 × 2–4 m, wall 1.8–2.2 m; planks, plywood, corrugated sheet offcuts and old banner vinyl (printed flex banners re-used as walls; random colours with fragments of large faces and text); a mono-pitch scrap-sheet roof held down by stones and tyres.
- `sh_stall`: a table 1.2 × 0.8 m under an umbrella (2 m diameter, branded-colour panels) or a tarp on 4 sticks.
- `sh_pier_infill`: tarp/board walls between two bridge piers (pier 1.2–2 m diameter at 20–30 m spacing).
- `sh_mattress_roll`, `sh_cookstove` (three-stone or a metal charcoal stove), `sh_clothesline`.
- `sh_x_mark`: a red painted "X" plus "Quit notice" stencil on nearby walls (enforcement).

**Colours**: grey planks #6E6152, rust #7A4524, banner vinyl fragments (white #F0F0F0 with red/blue/yellow blocks), tarps blue #2E6FB7 and orange; ground black-brown #3A3329 with sawdust #B08A5B.

**Variants**: rail strip 45%, under-bridge 35%, canal/drain bank 20% (similar to canal-side clearances [src 36]).

**Condition**: always decayed/makeshift. A "cleared" state: flattened debris, a lone sofa, smoke from burning piles, a government bulldozer and officials' pickup.

**Props and life**: traders at all hours, minibuses parked under the bridge, a pool of stagnant water, goats, refuse heaps, betting posters, a mechanic, a small generator. At night: bulbs on wires tapped from poles, cooking fires, men sleeping on benches, fewer lights under bridges (dark and risky).

**SELECT BY**: along rail and elevated-road geometry in dense_mainland, old_island edges and port; within 15 m of a rail line or under any bridge deck taller than 4 m; wealth lowest. Tie density to a seeded "enforcement" state: cleared (30%), recolonising (30%), full (40%).

**Gidi mapping**: shanties along rail lines and under bridges.

---

## 18. Beach shacks

On a royal-family-owned city beach there are brightly painted wooden shacks, colourful umbrellas and vendor stalls. Many shacks turn into small nightclubs at night, selling grilled fish and suya [src 37]. A boat-access bay beach has small huts for shade with chairs, a hut rental economy, a pizza place, a beach club, and a fishing community of rusting corrugated-metal shacks among abandoned villas and a few chalets, off-grid [src 38].

**Looks like**
- A row of 1-storey open-fronted timber shacks on the dune line facing the ocean, each painted a different loud colour with its name, with a small bar counter, speakers and a strip of plastic chairs and umbrellas on the sand.
- Thatch or palm-frond shade huts (open, on 4 poles) for rent along the beach [est]. Horses for rides, a lifeguard tower (rare).
- Behind: the fishing settlement of rusty zinc shacks, canoes pulled up on the sand, nets.

**Kit parts [est]**
- `bs_bar`: 3–6 × 3–6 m plank or bamboo frame, floor on 0.3–0.6 m stilts or sand-level concrete, a counter 1.1 m, a mono-pitch or gable roof of zinc or palm thatch with a 1 m overhang, a name board 2 × 0.5 m.
- `bs_hut`: an open shade hut 3 × 3 m, 4 posts 2.4 m, palm-frond/thatch roof (pyramid or gable, thatch thickness 0.2–0.3 m), with a bench or plastic chairs.
- `bs_umbrella`: 2–2.5 m diameter, panels in drinks-brand-like colours (generic red, yellow, green, blue).
- `bs_cabana_vip`: a raised timber deck 4 × 6 m with white drapes (newer beach clubs).
- `bs_fisher_shack`: §17 style in rusty zinc.

**Colours**: shack paints: red #C8322D, yellow #F2C230, green #2F8F4E, blue #2E6FB7, pink #E26A9B, purple #6A3F8F; thatch #A88A55 (fresh) to #6E5E44 (grey, old); sand #E6D2A8; ocean #4A7A8C; foam white.

**Variants**: painted bar shack 40%, shade hut 35%, fishing shack 20%, VIP cabana 5%.

**Condition**: salt-faded paint within one season, rusty nails, sand drifts against walls. Removed/demolished: sand-filled where big road works passed (beaches were demolished for a coastal highway [src 37]).

**Props and life**: day: grilled-fish smoke, music, horses, coconut sellers, footballers, boats landing visitors, families. Night: coloured string lights, speakers, generators, bonfires, many people.

**SELECT BY**: waterfront (ocean beach edge only); density highest near a road access point; fishing shacks at the far ends.

**Gidi mapping**: beach shacks.

---

## 19. Northern (Hausa) community compound ("zango", Sabo-like quarter)

Hausa communities in southern cities typically live in their own quarters under a community head (Sarkin Hausawa), linked to cattle and kola trade and the railway [src 39, 40]. An island Hausa quarter grew from colonial-army barracks people. It has narrow streets, dense old "sturdy" buildings next to tall new ones, a 1907 mosque, tailors, cheap rice-and-stew restaurants, suya spots, sugar-cane and fruit hawkers, and okadas. Other West African nationals live alongside them [src 41]. Hausa compounds in the north are walled enclosures of several buildings housing extended families [src 42]. In Lagos the material is sandcrete, not mud.

**Looks like**
- A walled compound reached through a single entrance room/ porch (zaure-like) from the street. Inside: a sandy or concrete courtyard 8–15 m, rooms around it in 1–2-storey blocks, a well or tank, and a goat pen.
- Street side: a long, plain wall with few windows, painted white, green or light blue, with a green door. A men's bench in front. Hand-painted Arabic-script and Hausa signs on shops [est].
- Neighbourhood: a mosque with a green-and-white minaret and loudspeakers; cattle and ram traders (big around festivals); tea kiosks (mai shai); suya grills; wheelbarrow pushers and water carts ("mai ruwa", a cart with 8–12 yellow jerrycans); tailors with sewing machines on verandas.

**Kit parts [est]**
- `hz_wall`: 2.2–2.7 m street wall, rendered, with a parapet; few windows (0.6 × 0.6 m high-set grilles).
- `hz_zaure`: entrance room 3 × 4 m with a door 1.0 × 2.1 m, sometimes a raised moulded surround (a nod to northern façades: a stepped or arched frame, painted geometric patterns in 15%).
- `hz_courtyard`: 8–15 × 8–15 m, surrounded by room blocks 3–3.5 m deep with verandas 1.2 m.
- `hz_roof`: flat slab with a parapet (50%) or mono-pitch zinc falling inward (50%).
- `hz_mosque_small`: neighbourhood mosque 8 × 12 m with a 10–15 m minaret, a crescent finial, a green dome 3–5 m.
- `hz_kiosk_tea`: 2 × 2 m plank/zinc kiosk with a bench, a kettle and bread loaves.
- `hz_cattle_pen`: rope/timber pen 6 × 10 m, with straw.

**Colours**: white #F2EFE6, mint #B5D3A0, light blue #A9C9DE, beige #D9C3A0; doors and trims green #2F7A4A; geometric paint: ochre #C98B3A, black, green; ground sand #D9C6A0.

**Variants**: courtyard compound 45%; rooming block occupied by Hausa tenants (§8 type) 35%; trading/market compound with stalls and pens 20%.

**Condition**: worn/decayed mostly; mosques kept well painted.

**Props and life**: men in kaftans on benches, tea and bread sellers, suya smoke at dusk, cattle and rams near festival time, water carts, wheelbarrows, okadas, prayer mats outside the mosque at prayer times. Night: suya grills lit by lanterns, tea kiosks open late, mosque lights and loudspeakers.

**SELECT BY**: pockets inside dense_mainland (market/abattoir-adjacent, Mile-12-like produce markets, Agege-like rail towns) and old_island (barracks-edge); a cultural-pocket seed flag; wealth low-mid; near a market and the railway.

**Gidi mapping**: northern (Hausa) community compounds.

---

## 20. Houses converted to churches, shops and phone malls

A tech market grew from about 10 shops in 1997 to more than 3,000 on a residential street. Homeowners sold flats that were turned into shopping plazas; a bungalow became a phone-accessory plaza. The market now spans seven streets of low-rise buildings, plazas, converted bungalows, iron kiosks and standalone umbrellas [src 43, 44]. Regulators have sealed banks and about 80 buildings on a main avenue for illegal residential-to-commercial conversion [src 45], and served notices on residential buildings converted to churches, mosques, clubs and bars [src 46]. Church emblems are everywhere on Lagos streets [src 47].

**Looks like**
- **House-to-church**: a bungalow or duplex with the front wall knocked out or a big zinc/steel extension added in the forecourt. A huge banner (3 × 6 m to 6 × 12 m) on the façade with a flame/dove emblem, the pastor's photo and service times. Rows of plastic chairs visible through open steel doors, speaker horns, a generator, a painted "Parish" signboard at the gate.
- **House-to-shops**: the front fence is removed and replaced by a row of lock-up shops along the boundary (see §7), or the front rooms are opened into shop bays with roller shutters. Signs crowd the eaves.
- **House-to-phone mall/plaza**: a 2–3-storey house or new infill block with an open ground floor, glass-fronted cubicles 2 × 3 m on each floor reached by an external stair and open galleries, a forest of vinyl signs in phone-brand-like colours (generic) and a giant "PLAZA" name, with umbrellas and kiosks in front.
- Also: house-to-school ("Nursery & Primary", murals of ABC and cartoon characters on the wall), house-to-bank-branch (cladding panels over an old duplex), house-to-hotel/lounge.

**Kit parts [est]**
- `cnv_church_banner`: 3 × 6 to 6 × 12 m flex banner on a steel frame or nailed to the parapet.
- `cnv_church_shed`: a forecourt hall 10 × 15 m, steel portal frame, zinc roof 4–5 m high, open sides with half-walls.
- `cnv_shop_bay_cut`: a façade modifier converting windows into 2.5–3.5 m bays with roller shutters.
- `cnv_plaza_gallery`: 1.5–2 m deep gallery with a steel rail on each upper floor; an external stair 1.2 m wide.
- `cnv_sign_cluster`: 6–30 signs of 0.6–1.2 × 2–4 m, stacked to cover the façade.
- `cnv_school_mural`: painted letters and cartoon panels 1–2 m high on the fence.
- `cnv_cladding_skin`: aluminium composite panels (silver #C0C4C6, a bank's corporate colour band) over the front of a duplex.

**Colours**: original house colours, overwhelmed by banners and signs; churches favour white, blue and red banners; shop signs are saturated.

**Variants (of converted houses)**: shops 45%, church 20%, plaza/phone mall 15%, school 10%, office/bank 10%.

**Condition**: conversions are mostly worn. A "sealed" state: a red-painted "SEALED BY ORDER" (generic) on the gate and a padlock and chain.

**Props and life**: churches: crowds on Sunday and weeknights, cars double-parked, ushers in suits, speaker noise. Phone mall: buyers and touts, okadas, generators on the pavement, pirated-CD and accessory hawkers, police patrol. Night: plazas shuttered, church vigils loud and lit.

**SELECT BY**: residential kinds (bungalow, duplex, storey building) with main-road frontage in dense_mainland, civic (Ikeja-like) and elite main roads. Conversion probability rises with traffic: main road 0.5, collector 0.2, back street 0.05. Phone-mall clusters seed a "tech market" sub-zone (several blocks, 70% converted).

**Gidi mapping**: houses converted to churches, shops, phone malls.

---

## 21. Boys' quarters (BQ)

"BQ" is a colonial term for servants' quarters, now also for maids and drivers [src 48]. A late-1950s company design put a single-storey wing of individual rooms along a corridor with a shared kitchen and bathroom [src 49]. Modern listings sell "with BQ", often "self-contained with private access" [src 23, 50].

**Looks like**
- A low row of 2–4 rooms built hard against the rear or side boundary wall of a house plot, facing the back of the main house across a 3–6 m service yard. A mono-pitch zinc roof falls to the boundary.
- In elite houses: a 2-storey BQ block with a laundry, a driver's room and a store, painted to match the house.
- Often doubles as rental income; may have its own side gate.

**Kit parts [est]**
- `bq_row`: rooms 3.0 × 3.0–3.6 m, a block 3.0–3.6 m deep × 6–15 m long; wall 2.7–3.0 m.
- `bq_veranda`: 1.0–1.5 m deep, lean-to roof on 2–4 steel/block posts.
- `bq_roof`: mono-pitch 10–15° (75%) or flat slab (25%, elite).
- `bq_door`: steel or flush door per room; window 0.9 × 1.2 m louvre.
- `bq_kitchen`: an outdoor sink, a gas cylinder and a clothesline.
- `bq_two_storey` (elite): 6 × 12 m with an external stair.

**Colours**: same as the main house, or unpainted render in 40% of mainland cases; roof older/rustier than the main house.

**Variants**: 1-storey row 75%, 2-storey 15%, converted container 5%, BQ built over the garage 5%.

**Condition**: always one level worse than the main house [est].

**Props and life**: a driver washing a car, a maid washing clothes in basins, a small TV, a generator nearby, a clothesline, a gas cylinder, a bicycle, a cat. Night: one bulb, a radio.

**SELECT BY**: any main house with plot area ≥ 450 m² and wealth ≥ mid (p = 0.7 elite, 0.4 sprawl/mainland mid); place at the rear boundary, opposite the gate.

**Gidi mapping**: boys' quarters (BQ) behind houses.

---

## 22. Generator house

The grid is unreliable, so generator noise is a major quality-of-life factor [src 51]. Every compound has some generator. The housing depends on wealth.

**Looks like**
- Low-income: a small petrol set (red, yellow or green, 0.5 × 0.4 × 0.45 m) on the ground, sometimes in a steel-mesh cage padlocked to the wall, with an exhaust hose and a black soot fan on the wall behind.
- Middle: a 1.5 × 2 m block hut with a louvred or mesh door and a slab or zinc roof, a black-stained exhaust pipe sticking out, and a diesel jerrycan next to it.
- Elite: a 4 × 6 m generator house with acoustic louvres, a big diesel set (a sound-proof enclosure 3 × 1.2 × 1.8 m), a changeover switch box on the wall, a fuel tank on a stand, and a vertical exhaust stack above the roof (2–3 m).
- Flats and estates: a row of small sets on the forecourt, each wired up to a different flat.

**Kit parts [est]**
- `gen_small`: 0.5 × 0.4 × 0.45 m, colours red #C8322D, yellow #E5C12E, green #2F8F4E, blue #2E6FB7; a cage 0.8 × 0.6 × 0.7 m of steel mesh.
- `gen_hut`: 1.5 × 2.0 × 2.2 m, block, a door with louvres, an exhaust pipe 75 mm, roof zinc or slab.
- `gen_house`: 4 × 6 × 3 m, ventilation louvres 1.2 × 1.2 m on 2 sides, double steel doors 2 × 2.1 m.
- `gen_canopy`: a sound-proof genset enclosure, 2.5–4 × 1.1–1.5 × 1.5–2.2 m, painted cream #E8DCB8, blue #2E5E8C, green #3E6B4A or yellow; vents on ends.
- `gen_stack`: exhaust pipe 100–200 mm, rising 2–3 m with a rain cap.
- `gen_cable`: thick black cables on the wall to a changeover box (grey 0.4 × 0.3 m).
- `gen_soot`: decal: black fan of soot #1E1E1E on the wall 1–2 m wide.

**Variants**: small set in the open 45%; caged 15%; block hut 25%; elite house with a sound-proof set 15%.

**Condition**: soot, oil stains on the ground (#2A2620), rusty cage, a fuel jerrycan (yellow, green, black), a funnel.

**Props and life**: day: off when grid power is on. Evening (7–11 pm): the soundscape of the city, with a bluish exhaust haze. A technician with an open set and tools on the ground (repairs). Fuel queues at filling stations during scarcity.

**SELECT BY**: every compound (p = 0.9); variant by wealth (low → small/caged; mid → hut; high → gen_house/canopy); estate flats → row of small sets on the ground floor.

**Gidi mapping**: "generator".

---

## 23. Stand-alone water tank tower

Most Lagos homes rely on their own boreholes rather than mains water [src 52]. Elevated steel stands give water pressure by height [src 53]. Steel stands are fabricated and sold widely (on listings sites) [src 54]. Coastal areas have saline water, so treatment plants (filters) are common [src 52].

**Looks like**
- A galvanised or painted steel frame of 4 angle-iron legs with cross bracing, 3–12 m tall, carrying 1–4 black or blue-white plastic tanks (1,000–5,000 L) on a platform. A ladder on one leg. Pipes run down to the house.
- Low-cost: a 1-tank stand 2–4 m on a concrete plinth; or the tank placed on top of a block "tower" (1.5 × 1.5 m block column) or on the roof slab.
- Estates and plazas: a large 6–12 m tower with 4–8 tanks or a concrete overhead tank; a borehole head and a pump house at the foot.

**Kit parts [est]**
- `wt_tank`: vertical cylinder; 1,000 L ≈ 1.1 m diameter × 1.3 m; 2,000 L ≈ 1.4 × 1.6 m; 5,000 L ≈ 1.9 × 2.1 m; ribbed walls; a manhole lid 0.45 m. Colours: black #1E1E1E (60%), blue #2E6FB7 (15%), white/cream #E8E2D2 (10%), green #3E6B4A (10%), red/brown (5%).
- `wt_stand`: 4 legs of 75–100 mm angle or square tube; plan 1.5 × 1.5 m (1 tank) to 3.5 × 3.5 m (4 tanks); X-bracing every 1.5–2 m; platform of steel channels; ladder 0.4 m wide.
- `wt_block_tower`: block or RC column 1.2–1.8 m square, 3–6 m tall, rendered, with a slab top.
- `wt_pipes`: 25–50 mm PVC (grey, white) or galvanised pipes running down the leg.
- `wt_borehole`: a pipe head 0.15 m, a pump control box, a treatment filter cylinder (blue or white 0.3 × 1.5 m), a small block pump house 1.5 × 1.5 m.
- `wt_concrete_overhead` (estates): a concrete box tank 4 × 4 × 2 m on 4 columns, 8–12 m high (old estate flats).

**Variants**: steel stand 1–2 tanks 50%; roof/slab-top tanks 30% (no tower); block tower 10%; multi-tank stand 8%; concrete overhead 2%.

**Condition**: new galvanised silver #C9CCCC; worn: rusty #8A4B22 at joints and legs; decayed: leaning tower (1–3°), green algae down the tank sides, overflow drips staining the ground, a burst tank replaced by a different colour.

**Props and life**: a water vendor's cart or a jerrycan queue in poor areas; an overflow pipe dripping; a borehole driller rig (a truck with a mast) at new plots; an empty tank lying on its side at a building site.

**SELECT BY**: all compounds (p = 0.7 for some tank). Sprawl and estates favour stands (p = 0.6). Dense mainland favours roof-top tanks. Estate flats (§6) favour concrete overhead or multi-tank stands. Coastal/waterfront favour treatment filters. Height: storeys of the house + 1–2 m.

**Gidi mapping**: "water tank" (and the borehole/pump layer).

---

## Sources

1. The Culture Trip, "Discovering the Brazilian Quarter in Lagos": https://theculturetrip.com/africa/nigeria/articles/the-brazilian-quarter-in-lagos
2. Prime Progress, "The Afro-Brazilian architecture that shaped Lagos city": https://primeprogressng.com/social-impact/the-afro-brazilian-architecture-that-shaped-lagos-city/
3. Daily Trust, "Lagos Afro-Brazilian architecture under threat": https://dailytrust.com.ng/lagos-afro-brazilian-architecture-under-threat.html
4. Livin Spaces, "How Iconic Afro-Brazilian Architecture is Disappearing From Lagos": https://livinspaces.net/design-stories/ls-tv/how-iconic-afro-brazilian-architecture-is-disappearing-from-lagos/
5. Wikipedia, "Ilojo Bar": https://en.wikipedia.org/wiki/Ilojo_Bar ; Guardian NG, Olaiya House demolition: https://guardian.ng/property/legacy-protests-against-demolition-of-161-year-old-olaiya-house/ ; ThisDay: https://thisdaylive.com/index.php/2016/09/25/fg-orders-restoration-of-ilojo-bar-national-monument-lagos
6. UNILAG repository, "Socio-economic determinants of urban housing materials types in poor area of Makoko": https://ir.unilag.edu.ng/handle/123456789/12268
7. Ripples Nigeria, "Living on stilts: 75 images of Makoko": https://ripplesnigeria.com/living-on-stilts-75-unforgettable-images-of-makoko-will-it-survive-sanwo-olus-smart-city-plan
8. Archnet, "Makoko Floating School": https://archnet.org/sites/15149
9. Aga Khan Trust for Culture, Makoko Floating School: https://the.akdn/en/how-we-work/our-agencies/aga-khan-trust-culture/akaa/makoko-floating-school
10. WorldAtlas, "What and where is the Makoko slum?": https://www.worldatlas.com/articles/what-and-where-is-the-makoko-slum.html
11. Now I Know, "The battle over the floating slum": https://nowiknow.com/the-battle-over-the-floating-slum/
12. Kola King (Substack), "Banana Island in Lagos is a billionaire's paradise": https://kolaking.substack.com/p/banana-island-in-lagos-is-a-billionaires ; Face2Face Africa: https://face2faceafrica.com/?p=183225
13. Guardian NG, Banana Island demolitions: https://guardian.ng/?p=1334245 ; TheCable: https://thecable.ng/lagos-demolishes-three-storey-building-seals-four-in-banana-island ; Livin Spaces, 19 buildings sealed: https://livinspaces.net/design-stories/news/lagos-state-government-seals-19-more-buildings-in-banana-island-due-to-lack-of-building-permits-and-planning-approval/
14. Wikipedia, "Festac Town": https://en.wikipedia.org/wiki/Festac_Town
15. Vanguard, "FHA demolishes illegal structures, markets in Festac": https://www.vanguardngr.com/2021/06/fha-demolishes-illegal-structures-markets-in-festac/ ; ThisDay, FHA: https://thisdaylive.com/index.php/2023/12/11/fha-setting-the-records-straight-over-festac-demolition
16. Archivi.ng, "The generational trap of housing in Lagos": https://archivi.ng/the-archivist/stories/issue-5/the-generational-trap-of-housing-in-lagos
17. New Telegraph on Abesan estate: https://newtelegraphng.com/?p=706031 ; Wikipedia, LSDPC: https://en.wikipedia.org/wiki/Lagos_State_Development_and_Property_Corporation
18. Wikipedia, "1004 Estate": https://en.wikipedia.org/wiki/1004_Estate
19. ICIR, "Magodo Estate suffers another lockdown": https://www.icirnigeria.org/magodo-estate-suffers-another-lockdown/ ; TheCable, guards and the police commissioner: https://www.thecable.ng/?p=645771
20. The Sun, "Otto Ilogbo: Lagos community where residents dwell in squalor": https://thesun.ng/otto-ilogbo-lagos-community-where-residents-dwell-in-squalor/
21. Amusing Planet, "Makoko, a floating slum in Nigeria": https://www.amusingplanet.com/2014/04/makoko-floating-slum-in-nigeria.html
22. Coverage and setbacks: reference-global, ahr-2022-0008 (density-zone table): https://reference-global.com/article/10.2478/ahr-2022-0008 ; Nairametrics, Lekki demolition notice (setback range): https://nairametrics.com/2021/06/22/lagos-serves-3-day-demolition-notice-on-45-buildings-in-lekki/
23. Nigeria Property Centre, 4-bed terrace with BQ, Lekki Phase 1: https://nigeriapropertycentre.com/for-sale/houses/terraced-duplexes/lagos/lekki/lekki-phase-1/3475381-elegantly-finished-4-bedroom-terrace-self-compound-duplex-with-bq
24. Ownkey, "Area guide: Lekki Phase 2": https://ownkey.com/ng/blog/area-guide-lekki-phase-2-lagos ; BusinessDay, Ikate duplex scheme: https://businessday.ng/sponsored/article/annuva-homes-and-lsdpc-sign-landmark-agreement-to-deliver-premium-duplexes-in-lekki/
25. Livin Spaces, "The White Silhouette" maisonettes: https://livinspaces.net/design-stories/featured-projects/residential-design/the-white-silhouette-by-baron-architecture-introduces-modern-4-bedroom-maisonettes-in-banana-island-lagos/
26. Kola King, "This glowing contemporary residence…": https://kolaking.substack.com/p/this-glowing-contemporary-residence ; AOL, "The 'Lantern House'": https://www.aol.com/architect-tosin-oshinowo-designing-lantern-083423786.html
27. Wikipedia, "Ikoyi": https://en.wikipedia.org/wiki/Ikoyi
28. Wikipedia, "Eko Pearl Towers": https://en.wikipedia.org/wiki/Eko_Pearl_Towers ; developer page: https://ekopearltowers.com/about
29. BusinessDay, "These 7 projects lead luxury residential towers in Eko Atlantic City": https://businessday.ng/real-estate/article/these-7-projects-lead-luxury-residential-towers-in-eko-atlantic-city/
30. TheCable, "80% of buildings in Lekki have no government approval": https://thecable.ng/80-of-buildings-in-lekki-have-no-government-approval-says-commissioner ; ICIR: https://www.icirnigeria.org/concerns-as-lagos-state-marks-80-buildings-for-demolition-in-ibeju-lekki/
31. NBCC/New Telegraph, "Speculators mop up land in Lagos' $15bn Free Trade Zone": https://www.nbcc.org.ng/news-article/speculators-mop-up-land-in-lagos-15bn-free-trade-zone
32. Guardian NG, "Lagos communities battle developers over land ownership": https://guardian.ng/?p=1030571 ; Sahara Reporters (Ibeju-Lekki villages): https://saharareporters.com/2014/07/06/lagos-government-has-not-returned-our-land-falsely-claimed-say-ibeju-lekki-villagers
33. Guardian NG, "Squatters under Ijora Causeway, Blue Line bridges get five-day quit notice": https://guardian.ng/?p=2348434 ; ThisDay: https://www.thisdaylive.com/2024/01/29/lagos-gives-squatters-of-under-ijora-bridge-five-days-to-quit/
34. NAN, "Lagos begins clearing shanties along Red Rail Line": https://nannews.ng/2023/09/30/lagos-govt-begins-clearing-shanties-obstructions-along-red-rail-line-project ; BusinessDay, traders on rail tracks: https://businessday.ng/transport/article/fg-lasg-to-arrest-traders-on-lagos-rail-tracks-over-accidents/
35. Channels TV, Ijora under-bridge: https://www.channelstv.com/2024/02/07/lagos-to-turn-ijora-under-bridge-into-recreational-spot/ ; Guardian NG, Costain shanties: https://guardian.ng/news/nigeria/metro/lagos-govt-clears-shanties-reclaims-costain-bus-stop/
36. Channels TV, "Lagos demolishes 138 shanties at Ajao Estate canal": https://www.channelstv.com/2024/11/15/lagos-demolishes-138-shanties-at-ajao-estate-canal/
37. Discover Lagos, beach guides: https://www.discoverlagos.ng/post/elegushi-royal-beach-the-ultimate-weekend-destination-for-fun-and-sun ; https://discoverlagos.ng/post/a-guide-to-lagos-best-beaches-from-popular-spots-to-hidden-gems ; Ibom Air guide: https://www.ibomair.com/discover-paradise-a-guide-to-the-picturesque-beaches-of-lagos/
38. Strangers Guide, "The regulars of Tarkwa Bay": https://strangersguide.com/articles/the-regulars-of-tarkwa-bay/
39. Wikipedia, "Sabo Quarter": https://en.wikipedia.org/wiki/Sabo_Quarter
40. Salamone, Commission on Legal Pluralism (Hausa in Yoruba cities): https://commission-on-legal-pluralism.com/system/commission-on-legal-pluralism/volumes/42/salamone-art.htm.html
41. Daily Trust, "The Hausas of Obalende": https://dailytrust.com/the-hausas-of-obalende
42. African History Extra, "Hausa urban architecture": https://www.africanhistoryextra.com/p/hausa-urban-architecture-construction
43. Rest of World, "Tech markets, Lagos": https://restofworld.org/2022/tech-markets-lagos-nigeria/
44. Techpoint Africa, relocation of Computer Village: https://techpoint.africa/2018/08/23/relocation-of-computer-village/ ; Wikipedia, "Ikeja": https://en.wikipedia.org/wiki/Ikeja
45. TheCable, "Lagos shuts five bank branches for illegal building use": https://www.thecable.ng/?p=264425
46. TheCable, "Lagos serves 30-day notice to owners of residential buildings converted to clubs, worship centres": https://thecable.ng/lagos-serves-30-day-notice-to-owners-of-residential-buildings-converted-to-clubs-worship-centres
47. IJURR, "Neo-Pentecostal urban infrastructures in Lagos": https://www.ijurr.org/article/neo-pentecostal-urban-infrastructures-in-lagos-nigeria-ontology-politics-poetics/
48. Babilown, "Nigerians and the 'BQ' mentality": https://babilown.com/2011/06/08/akomolede-nigerians-and-the-bq-mentality/
49. Canadian Centre for Architecture, "Bachelors' quarters, Nigeria": https://cca.qc.ca/en/search/details/collection/object/16371
50. Nigeria Property Centre, maisonette with BQ: https://nigeriapropertycentre.com/for-sale/houses/lagos/lekki/lekki-phase-1/3574126-luxury-brand-new-4-bedroom-maisonette-with-bq
51. Ownkey, "Noise and sound insulation in Nigerian property": https://ownkey.com/ng/blog/noise-sound-insulation-nigeria-property
52. Ownkey, "Water supply solutions, Nigeria property": https://ownkey.com/ng/blog/water-supply-solutions-nigeria-property
53. Akvopedia, elevated tanks: https://akvopedia.org/wiki/Special:MobileDiff/19394...20877
54. Jiji listings, water tank towers: https://jiji.ng/building-and-trades-services/water-tank
