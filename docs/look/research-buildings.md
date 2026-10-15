# Lagos buildings and their parts: a catalogue for the Gidi generator

Rule zero: this is pattern research. Nothing here names a building to copy; Gidi invents its own.

**How to read this.** Each entry gives look, dimensions, colours (hex), materials and weathering, variants with rough frequencies, and SELECT BY. Labels:
- **[src]**: backed by a source in the list at the end.
- **[est]**: my estimate from general knowledge of Lagos street scenes and Nigerian building practice. Most numbers are [est]. Web sources rarely give measurements: room sizes, pitches and stilt heights are almost never published. Treat [est] values as starting distributions to tune by eye.

District characters used in SELECT BY:
- `dense_mainland`: Mushin, Shomolu, Ajegunle, Oshodi, Bariga.
- `old_island`: the Lagos Island core and the Brazilian quarter.
- `elite`: Ikoyi, VI, Banana Island, Lekki Phase 1, Ikeja GRA.
- `sprawl`: Agege, Ikorodu, Alimosho, Ibeju-Lekki edge.
- `waterfront`: Makoko-like stilt settlement.
- `port`: Apapa-like warehouses and tank farms.
- `cbd`: Marina and Broad St style.

---

## 0. Global constants (all [est] unless marked)

| Item | Value |
|---|---|
| Sandcrete block (standard) | 450 × 225 × 225 mm ("9-inch"); partition block 450 × 150 × 225 mm ("6-inch") [src: Lagos block-quality study]. Course height with mortar ≈ 0.24 m |
| Block quality | Lagos blocks test far below standard (0.2–1.3 N/mm² vs 3.45 required) [src]. This is why plaster cracks, arrises crumble and walls bulge |
| Floor-to-floor height | 3.0–3.3 m for low-cost housing; 3.3–3.6 m for elite houses and offices; 3.6–4.5 m for ground-floor shops |
| Ground-floor plinth / DPC | Floor 0.3–0.6 m above street (flood). Elite 0.45–0.9 m. Waterfront and flood-prone areas up to 1.0 m |
| Slab edge / floor band | 0.15–0.20 m slab plus a 0.2–0.3 m beam band, often expressed as a horizontal stripe on the façade |
| Column grid | 3.0–4.5 m (residential RC frame); 5–8 m (commercial) |
| Typical plot | "1 plot" ≈ 18 × 36 m (≈ 648 m²) on the mainland. Old-island plots are smaller and irregular (≈ 6–15 m frontage). Elite plots 1,000–2,500 m² |
| Room (rooming house) | ≈ 3.0 × 3.6 m (10 × 12 ft) to 3.6 × 3.6 m (12 × 12 ft). Only one weak source for 12 × 12 ft; the rest is [est] |
| Front setback | `dense_mainland`: 0–3 m. Shops often built right to the gutter, with a 0.6–1.2 m concrete slab bridging the open drain. `elite`: 6–15 m behind a wall |
| Open drain at street edge | 0.45–0.9 m wide, 0.4–1.0 m deep, concrete U-channel, partly slab-covered at gates and shops. Water dark green-black (#2F3A2A) |

**Paint palette (Lagos street, [est]; sampled from memory of typical emulsion colours)**

| Name | Hex (fresh) | Hex (faded, 5–10 y) | Share of painted façades |
|---|---|---|---|
| Cream / off-white | #EDE3C8 | #CFC3A3 | 25% |
| Pale yellow / "Lagos yellow" | #F2D46B | #D4BC72 | 10% (very common on old-island and mainland houses and on commercial vehicles) |
| Sky / baby blue | #9CC7E0 | #9FB4BE | 10% |
| Peach / salmon | #F2B999 | #D3A68C | 8% |
| Light green / mint | #A9D3A0 | #9CB08E | 8% |
| Pale pink | #EDB9C2 | #CDA6A9 | 5% |
| Grey (modern) | #A7A9A8 | #959794 | 8% (rising; elite and newer builds) |
| White (elite) | #F5F5F2 | #DAD8D0 | 10% (most common in `elite`) |
| Brown / terracotta | #9B5B3A | #8A6450 | 4% |
| Two-tone trims | Window surrounds and floor bands in darker colours: maroon #7A2E2E, navy #2D3E6E, forest green #2F5E3A, chocolate #5A3A28 | — | 40% of painted buildings have a contrasting band or trim |
| Unpainted plaster | #B9B2A3 (cement grey-beige) | #9C968A plus dark streaks | 20% of `dense_mainland` façades |
| Exposed sandcrete | #A6A196 | #8E8A80, green-black algae at the base | 10–15% of `dense_mainland`; side and back walls are much more often bare than fronts |

**Weathering grammar (applies to every masonry building, [est])**
- **Rain splash / mud band.** 0.3–0.8 m high at the base, reddish-brown laterite (#8B5A3C) to grey-black (#3C3A35), with a ragged upper edge.
- **Algae and mould streaks.** Black-green (#2E3329) streaks drip from under sills, slab edges, parapet tops and AC drain points. Each streak is 50–200 mm wide and runs 0.5–2 m down. They are worst on north and east faces and under leaking gutters.
- **Fading.** Saturated paints go chalky within 3–5 years. Pale tones lose saturation; blues and greens go grey.
- **Patching.** New-paint rectangles near repaired cracks and around shop fronts (shop owners repaint their own bay). The result is a vertically banded façade with a different colour per shop.
- **Cracks.** Diagonal hairlines from window corners; a horizontal crack at the slab line.
- **Rust bleed.** Orange-brown (#8A4B22) runs below steel balustrades, burglar bars and roof-sheet edges.
- **Posters and writing.** Hand-painted text on walls ("THIS HOUSE IS NOT FOR SALE", "BEWARE OF 419", "POST NO BILL"), black or red, 0.15–0.3 m letters. Mark-out paint: a red "X" on buildings set for demolition. Political posters are pasted in grids near junctions.

---

## 1. Residential kinds in dense mainland (`front`, `back` houses)

### 1.1 Face-me-I-face-you rooming house ("Brazilian" or "rooming" house)
**Look.** A long rectangular block set perpendicular to the street. One central corridor runs from a front door straight to a back door into the yard. Rooms open off both sides with doors facing each other [src: Wikipedia, Bloomberg]. Typically 1–2 storeys [src: Bloomberg]; 3 storeys exist. Street front: a central door with a small porch (2–4 steps, sometimes a short veranda), flanked by one window per front room, so the front is often symmetric. Long sides: a regular rhythm of one window per room. Shared kitchen, toilets and bathrooms sit in a separate low block in the back yard ("yard" or "general toilet") [src].

**Dimensions [est].**
- Footprint: 8–10 m wide × 18–30 m deep.
- Corridor: 1.2–1.8 m wide.
- Rooms: 3.0–3.6 m × 3.0–3.6 m, 4–6 rooms per side per floor, so 8–12 rooms per floor.
- Windows: one per room, 1.2 × 1.2 m.
- Eaves height: about 3.3 m for 1 storey, about 6.5 m for 2.
- Backyard block: about 2.5 m high, mono-pitch zinc roof.

**Roof.** Hip or gable corrugated sheet over the long axis at 15–25°. Older ones are rusty asbestos-cement or corrugated iron. Upper floor (if any) reached by an internal stair at the corridor mid-point or an external stair at the back.

**Materials and weathering.** Sandcrete with cement render, painted on the street face only. Side walls are often bare or raw plaster. Heavily weathered: mud bands, faded paint, rusted roof.

**Variants (share of mainland residential stock, [est]).**
- Bungalow (1 storey): 55%.
- 2 storey: 35%.
- 3 storey: 10%.
- Older pre-1970 versions have arched or decorated front windows (a Brazilian influence).

A Guardian Nigeria table puts single-room and 2-room housing at 35–45% of urban stock (unsourced figure).

**SELECT BY.** kind ∈ {front, back}; district ∈ {dense_mainland, old_island-fringe (Ebute Metta, Yaba), sprawl-older cores}; wealth low; storeys 1–2. `back` plots favour this type even more (back houses rarely have shops).

### 1.2 Bungalow (detached, single family or "flats")
**Look.** Single storey, 10–15 m wide, often 2 flats side by side ("2 × 3-bedroom bungalow"). Front veranda/porch with 2–4 square columns (0.3 × 0.3 m), hipped zinc roof, 0.45–0.6 m overhang.

**Dimensions [est].** Eaves 3.0–3.3 m; ridge 4.5–6.0 m.

**Variants.**
- `sprawl` (Agege, Ikorodu): 60% of houses are bungalows, often within a compound wall, often with an unfinished second building on the same plot.
- `dense_mainland`: 25%.

**SELECT BY.** kind front/back; storeys = 1; sprawl ↑, dense_mainland medium; wealth low-mid; distance to main road large.

### 1.3 "Storey building" (2–4 storey block of flats)
**Look.** RC frame plus block infill. Typically 2 flats per floor ("4 flats" for 2 storeys, "6 flats" for 3 storeys). A strong horizontal slab band at each floor. Front balconies run the width or sit at the centre, with balusters. Stair is either in a central stairwell (lit by perforated breeze blocks or a vertical strip of louvres) or external at the side.

**Dimensions [est].**
- Width 12–16 m, depth 15–20 m.
- Floor-to-floor 3.0–3.3 m, so a 3-storey block (G+2) is about 10 m to the parapet or eaves.
- Balcony depth 1.2–1.8 m (cantilever).

**Roof.** Hip zinc (60%); flat concrete with parapet, often as a "future expansion" with starter bars (30%); gable (10%).

**Ground floor.** If on a busy street, the ground floor is converted to 2–6 shops (see §6). Flats move up.

**Storey distribution, mainland residential frontage [est].**

| Storeys | Share |
|---|---|
| 1 | 45% |
| 2 | 30% |
| 3 | 15% |
| 4 | 7% |
| 5+ | 3% (rising in Yaba, Surulere, Ogba, Lekki) |

**SELECT BY.** Storeys ≥ 2; wealth low-mid to mid; main road increases storeys (+1 on average) and the probability of shops (see §6). Old-island core also skews 2–4 storeys on tiny plots.

### 1.4 Front vs back position on the plot
- **Front house.** Faces the street and is the taller, better-painted of the two. On busy streets 60–80% have shops or a kiosk in front [est].
- **Back house.** Behind the front house, reached by a 1–2 m side passage. Usually a bungalow rooming house or a "boys' quarters" (BQ: a 1-storey row of 2–4 rooms, 3 × 3 m each, mono-pitch roof). Paint is worse or absent. Roof is rustier.
- **Proportion.** Back houses are about 0.5–1 storey lower on average.

---

## 2. Façade parts

### 2.1 Windows

| Type | Look | Size | Frame colours | Era/wealth | Share [est] |
|---|---|---|---|---|---|
| Naco / louvre (glass blades) | 6–12 horizontal glass blades about 150 mm tall in aluminium side clips, tilting open. Glass clear or frosted; many blades missing or broken, replaced with plywood or cardboard | 0.9–1.2 m wide × 1.2–1.5 m, often 2–3 bays per opening | Clips mill aluminium or rusted; surround timber, painted | 1960s–1990s; low-income now | 35% (dense_mainland), 10% (elite) |
| Wooden casement / shutter | Twin timber leaves, solid or glazed; old houses have solid plank shutters | 0.9–1.2 × 1.2–1.5 m | Brown #5A3A28, green #2F5E3A, blue #2D4E7A, faded | Pre-1980; old_island and older mainland | 15% |
| Sliding aluminium | 2–3 panels; glass tinted bronze (#6B5A45), reflective blue-green (#4E7F7A), dark grey or clear | 1.2–2.4 m wide × 1.2–1.5 m | Mill/silver #C0C0C0, bronze #5B4636, black #222, white | 1995–now; dominant in new builds | 40% overall, 70% in new builds |
| Casement aluminium / projected | Hinged aluminium sashes with tinted glass | Up to 1.8 m | Black / bronze | Elite, offices | 5% |
| Floor-to-ceiling glazing / curtain wall | Glass with mullions every 1.2–1.5 m; blue-green, silver or dark tint | Storey height | Silver / black | Elite houses, towers | 5% |

**Further notes [est].**
- **Window head.** A concrete lintel band. Older and mid-wealth houses add a projecting hood or sun-shade ("window hood", 0.3–0.6 m deep, sometimes with a mini sheet roof) above each window. These are very common in older Lagos houses.
- **Sill.** At 0.9–1.0 m. The opening is often framed in a contrasting paint colour, 0.10–0.15 m wide.
- **Insect net.** Green or grey mesh visible inside louvres. Many windows have a curtain visible: wax-print patterns or plain coloured.
- **AC units.** Split-unit condensers bracketed outside below the window: white boxes about 0.8 × 0.55 × 0.3 m. Window units project about 0.4 m. Density: 0–1 per flat (dense_mainland), 2–6 per house (elite). Rust-streaked brackets.

### 2.2 Burglar-proof bars ("burglary proof")
Nearly universal on ground floors (≈ 90%) and very common on upper floors (≈ 70%) [est]. Fixed outside the window or in the reveal, 16–20 mm square or round rod or 25 mm square pipe [src: Jiji listings mention 12–16 mm rod and 19 mm pipe].

**Patterns [est].**

| Pattern | Description | Share | Era/wealth |
|---|---|---|---|
| Plain verticals | Bars at 100–125 mm centres, 1–2 horizontal rails | 35% | All; cheapest |
| Grid / squares | 100–150 mm squares | 15% | All |
| Diamonds / diagonal lattice | 45° lattice of flat bar | 10% | 1980s–90s |
| Scrolls / "S" and "C" curls | Wrought-iron curls between verticals, sometimes with a central motif | 15% | Mid wealth, Lagos favourite |
| Sun-ray / fan | Radiating bars in a semicircular top or at the corners | 8% | Over doors and arched windows; 1970s–90s |
| Spear-head verticals | Verticals with arrow tips | 5% | Gates, fences |
| Square-pipe geometric (modern) | 25 × 25 mm pipe in rectangles, with "laser-cut" panels in elite homes | 12% | 2005–now |

- **Colours.** Black #1E1E1E (40%); white #EFEFEF (15%); silver/aluminium paint #B8B8B8 (10%); same colour as the window frame (brown, green, blue) (25%); rusty, unpainted (10%).
- **Weathering.** Rust bloom at welds and the bottom rail; a rust streak on the wall below.
- **Door versions.** A burglar-proof door (barred gate leaf) sits in front of the main door. Shop fronts have a separate collapsible "accordion" gate.

### 2.3 Balconies and balustrades
- **Precast concrete balusters (vase or bottle shape).** The classic Lagos look on 1970s–2000s storey buildings and many mansions. Balusters 0.6–0.75 m tall at 0.15–0.2 m centres, between a plinth course and a handrail (about 0.15 m wide). Total rail height 0.9–1.0 m. Painted the wall colour or white. Weathered: black streaks; chips revealing grey concrete. Share on mid-wealth balconies: 45% [est].
- **Solid parapet wall balcony.** Block upstand 0.9–1.0 m, rendered, sometimes with a pierced breeze-block band. Share 25%.
- **Steel tube or square pipe rail.** Verticals or horizontals, black, white or silver. Share 20%; rising.
- **Glass and stainless steel.** Elite and new apartments only. Share 10%; elite 50%.
- **Use.** Laundry lines with bright clothes; plastic chairs; potted plants; a generator on the balcony in some flats. Balconies are often enclosed later with burglar bars, so they become cages.

### 2.4 Parapets
- Flat roofs: parapet 0.6–1.2 m.
- Pitched roofs on mid and elite houses: often a "parapet roof" (a parapet hiding the sheet roof) at 0.3–1.0 m, with a coping ledge.
- Elite façades: tall parapet bands of 1.0–2.0 m.
- Overhang 50–100 mm at the coping. Black algae streaks below the coping are very characteristic.

### 2.5 External staircases
Common on 2–3 storey rooming and storey buildings: a side or back exterior RC stair, 0.9–1.2 m wide, with a solid block or baluster rail. Often unpainted grey. Sometimes a steel stair (rusty) up to a rooftop extension. Share among 2+ storey `dense_mainland` buildings: 30% [est].

### 2.6 Porches, steps, plinths
- **Front steps.** 2–5 steps, 0.15–0.18 m risers, terrazzo or tiled (cheap ceramic tiles, often maroon #7A2E2E or beige) or plain screed.
- **Porch.** 1.5–3 m deep, 2–4 columns.
  - Elite: portico with round columns, 0.4–0.6 m diameter, double height, Greek-revival.
  - Mid: square columns or a mosaic-tiled column wrap.
- **Plinth band.** A 0.3–0.9 m band at the base, painted darker: grey #6E6E6E, maroon, black #2A2A2A, brown. Some are tiled or rough-cast pebble-dash. Present on ≈ 40% of painted buildings [est]; it hides the mud band.

### 2.7 Render and exposed block
- **Render.** 15–25 mm cement plaster, wood-float texture. Older buildings have a rough "tyrolean"/spatter finish (grey speckled), popular from the 1970s to the 1990s.
- **Exposed block.** Visible grid of 450 × 225 mm coursing, grey #A6A196, mortar joints slightly darker. Common on side and back walls, fences, unfinished upper floors and BQs.
- **Damp.** Rising damp shows as a tidemark 0.3–1.0 m up, with efflorescence (white salt crust #E8E4DA) and paint peeling in sheets.

### 2.8 Signage on houses (no real brands)
- Hand-painted names and numbers ("No. 14"); church or company names; "TO LET" signs.
- Painted shop fascias: vertical text on pillars.
- Flex banners (vinyl, 1–3 m wide) tied over shop fronts in brights: red, yellow, blue, magenta. They fade to pastel within 1–2 years and tear at the eyelets.
- Telecom-yellow and red/white brand palettes are common on painted walls. For Gidi, use invented brands and generic palettes.

---

## 3. Roofs

### 3.1 Corrugated and long-span sheets
- **Old corrugated iron / galvanised.** Short sheets of about 2.4 m (8 ft), corrugation pitch 76 mm, depth 18 mm, laps visible every 2.4 m. Colour ranges from silver-galvanised #A9ADB0, through grey dull, to rust. Typical in `dense_mainland`, `old_island`, `waterfront` and on back houses.
- **Long-span aluminium.** Trapezoidal profile (ribs at 200 mm; rib height 20–35 mm), sheets running full rafter length. Gauges 0.45–0.70 mm [src supplier]. Colours [src: Lagos supplier list: Blue, Beige, Bush Green, Black, TC/Po red, Ivory White] with hex [est]:

| Colour | Fresh hex | Faded hex | Share of long-span roofs [est] |
|---|---|---|---|
| Brick / "TC red" | #9E3B2C | #9A6052 | 25% |
| Blue | #2E5A8C | #6C88A6 | 15% |
| Bush green | #2F5E3A | #6E8A6C | 15% |
| Charcoal / "North black" | #2A2C2E | #4A4C4E | 15% (rising, modern) |
| Beige / ivory | #D9CBA6 | #CFC6AE | 5% |
| Silver mill-finish | #C4C7C9 | #A9ACAE | 15% |
| Brown / chocolate | #5A3A28 | #7A6455 | 10% |

- **Stone-coated steel tiles.** Shingle-look in charcoal, terracotta, brown or "multi-colour"; small sheet modules. Elite and upper-mid homes since around 2005; very common in Lekki and new estates. Share: elite 50%, mid 15% [est].
- **Asbestos-cement corrugated.** Grey #8F8F88 with black lichen. Old government quarters, barracks, old schools, warehouses. Share 5% overall, 30% in barracks and old schools [est].

**Pitch [est].** Long-span roofs are low: 15–25°. Hipped mid-wealth: 20–30°. Elite multi-hip: 30–40°. Corrugated on rooming houses: 15–20°. Lean-to/mono-pitch back blocks: 8–15°.

**Hip vs gable [est].**

| Roof shape | Share in Lagos residential | Notes |
|---|---|---|
| Hip | 55% | Hip with multiple hips and valleys on L/T plans is typical |
| Gable | 25% | Older houses and BQs; mono-pitch for extensions |
| Concealed (parapet) | 15% | |
| Flat concrete | 5% of houses | Much more for commercial and "future floor" storey buildings |

**Overhang and fascia.**
- Eaves overhang 0.45–0.9 m.
- Fascia board 0.2–0.3 m deep: painted timber (white, brown) on older houses; aluminium/PVC fascia on newer, often white or matching the roof.
- Soffit is often open, showing rafters, or plywood/PVC ceiling boards (white).
- Gutters are rare on low-cost houses (water drips onto the ground, giving a splash line). Elite houses use PVC gutters with downpipes.

**Rust patterns.**
- On galvanised corrugated sheets, rust starts at the laps, the eaves edge, nail heads (orange dots along purlin lines every 0.6–0.9 m) and the bottom third of the slope.
- After 15–25 years the whole sheet is orange-brown (#8A4B22) to dark chocolate (#4A2E1E), mottled with some leftover silver.
- Patch sheets of different ages make a patchwork.
- Long-span aluminium does not rust; it fades and chalks.

**Holding down.** On poor roofs, old tyres, sandcrete blocks, stones and planks lie on the sheets to stop wind lift [est; widely seen]. Frequency: 15–25% of `dense_mainland`/`waterfront` roofs; never in elite.

**Ridge.** A ridge cap along the top; on older roofs it is often a different colour or rust.

### 3.2 Flat concrete roofs
- RC slab with a parapet.
- Surface: grey, stained black (#3E3E3A) with ponding marks; moss.
- Often carry starter bars (column rebar sticking up 0.6–1.5 m) for a future floor. Very common: ≈ 40% of flat-roof residential [est].
- Water tanks, clotheslines and a stair "pent-house" box with a door.

### 3.3 Roof furniture

| Item | Look | Size | Frequency [est] |
|---|---|---|---|
| Plastic water tank | Vertical cylinder, ribbed. Black #1E1E1E (most common), blue #2A5DA8, green #2F6B3A, white/grey, beige | 1,000 L ≈ 1.1 m Ø × 1.2 m; 2,000 L ≈ 1.4 m Ø × 1.5 m; 3,000–5,000 L ≈ 1.7–2.0 m Ø × 1.7–2.0 m | 60% of mainland houses (borehole culture) |
| Tank stand | Steel angle/pipe tower with a top platform; or block/RC column tower | Steel, painted then rusty; 3–6 m high on bungalows, 1–2 m when on a flat roof | Most tanks stand on a stand in the yard or a corner of the roof |
| Borehole pump housing | Small block or steel cage at ground level | 0.6–1 m | Under the tank |
| Satellite dish | Grey/white 0.6–0.9 m pay-TV dish on a wall bracket or roof; older 1.8–3 m mesh dishes on old houses | | 40–60% of houses; 2–4 per storey building (one per flat) |
| TV antenna | Yagi on a 3–6 m pipe mast, often bent or rusted | | 20%, declining |
| Solar panels | Blue-black panels, 1–2 m each, 2–8 per house, on stands or the roof slope | | 5–15% and rising fast (urban fuel prices); elite 30% |
| Generator | 0.6–1 m box on the ground or balcony, red/yellow/green housing; large diesel sets in elite and commercial | — | 70% of households; elite often a soundproof "generator house" |
| Telecom mast | Lattice tower 30–45 m, red/white banded, with a container shelter and a fenced base | | 1 per 0.5–1 km² in dense areas (often in residential compounds) |

---

## 4. Compound walls and gates

**Fence walls.**
- **Height.** Sandcrete block, 1.8–2.7 m in `dense_mainland`, 2.4–3.5 m in `elite` [est]. Piers every 3–3.6 m (0.45 × 0.45 m).
- **Coping.** A concrete coping or cap course projecting 25–50 mm; piers capped with small pyramids or concrete balls.
- **Finish.** Rendered and painted (cream, white or yellow with a darker base band), or bare block (40% in mainland and sprawl).

**Top security [est].**
- Embedded broken bottles: green #3F7A3A, brown #6B3E1E and clear shards set in mortar along the coping, 50–100 mm tall. 20% in mainland; older.
- Spikes: arrowhead steel bars 0.3–0.6 m, black. 25%.
- Razor or concertina wire: 0.45–0.6 m coils, silver. 20%; elite 40%.
- Electric fence: 4–8 thin wires on brackets with white insulators, plus a yellow warning sign. Elite 60%.
- Barbed-wire strands on angle brackets: 15%.

**Gates.**
- **Form.** Steel double leaf, 3.0–4.5 m wide × 2.1–3.0 m high. A pedestrian wicket door (0.8–0.9 m) set into one leaf or beside it.
- **Older gates.** Sheet-steel panels with pressed patterns, vertical bars at the top, spear tips.
- **Elite gates.** Solid sheet-steel or aluminium slats, motorised sliding, black/charcoal/bronze or wood-look.
- **Gate colours [est].**

| Colour | Hex | Share |
|---|---|---|
| Black | #1E1E1E | 35% |
| Dark green | #1F4D2E | 15% |
| Maroon | #6B1F22 | 10% |
| Navy | #1F2E5A | 10% |
| Grey / silver | #9A9A9A | 10% |
| Brown | #4A3020 | 10% |
| Faded / rusty / unpainted | — | 10% |

Many gates carry the house number painted in white, plus "Beware of dog" signs.

**Gatehouse.**
- Small 2 × 2 to 3 × 3 m block cabin beside the gate, roof flat or mono-pitch.
- A window facing the gate and sometimes a peephole slot in the gate.
- Mainland: a plastic chair outside. Elite: a uniformed guard and a boom barrier.

**SELECT BY.**
- Wall height rises with wealth.
- Bottles: old, mainland. Razor or electric wire: elite.
- Front houses with shops often have no compound wall: the shops are the street edge. Back plots and bungalows in sprawl are almost always walled.
- Estates (`elite` and new `sprawl` estates) add estate gates with a barrier and a security post at the street entrance.

---

## 5. Unfinished buildings

**Prevalence.** Very common across Lagos and its sprawl edge. Abandonment is driven by funding gaps and contractor failure [src: Emerald study, irejournals Eti-Osa]. Estimated share of plots with an incomplete structure [est]:

| District | Share |
|---|---|
| sprawl | 15–25% |
| dense_mainland | 5–10% (often an incomplete upper floor on an occupied building) |
| elite | 5% (stalled big projects) |

Durations of 3–15 years are common; some stay for decades [est].

**Stages [est].**

| Stage | What it looks like | Share of unfinished |
|---|---|---|
| 1. Foundation / slab only | DPC course and starter bars; weeds | 15% |
| 2. Block walls to lintel or roof level, no roof | Window openings with no frames; rebar sticks out of columns | 25% |
| 3. RC frame, 1–4 floors, no infill | Bare grey columns (0.23 × 0.23 to 0.3 × 0.45 m) and slabs; rusty starter bars 0.6–1.5 m on top of every column | 20% |
| 4. Roofed, unplastered, unglazed | Building shell with a roof, black openings, no paint | 25% |
| 5. Partly occupied | Ground floor lived in and painted; upper floor raw | 15% |

**Materials and weathering.**
- Concrete turns grey #9A9890, then dark-streaked #5E5C56.
- Rebar rust #7A3E1E bleeds down the columns.
- Plants grow in the cracks.
- A "FOR SALE" or "THIS PROPERTY IS NOT FOR SALE" painted notice, or a Lagos State building-control red "X/STOP WORK" stencil.

**Formwork and scaffolding.**
- Props are timber poles or bamboo, 50–100 mm diameter, irregular and slanted, under slabs.
- Scaffolds are timber/bamboo poles lashed with wire, plus planks. Steel tube scaffolding only on larger commercial jobs.
- Formwork plywood is brown, reddish film-faced or grey.
- A blue/green/orange net or tarpaulin wraps commercial sites.
- The site often holds a sand pile (yellow-ochre #C9A66B, sharp sand grey-beige), stacked blocks and a gravel pile.

**SELECT BY.** sprawl ↑↑; distance from main road: medium to high; storeys planned higher than built; wealth low-mid; also `elite` (Lekki/Ikoyi big frames).

---

## 6. Shops and trade structures

### 6.1 Ground-floor shops in front houses
- **Bays.** Each 3.0–4.0 m wide × 4–6 m deep, height 3.0–3.6 m. Typically 2–6 per frontage.
- **Fronts.**
  - Steel roller shutter (galvanised #A8ACAE, or painted blue/green/grey/red; dented, with rust at the bottom slat): 50%.
  - Folding/accordion steel gate plus a glass door: 20%.
  - Double steel doors: 15%.
  - Timber plank doors (old): 15%.
- **Canopies.** A shop canopy or awning (a mono-pitch long-span sheet on steel brackets, 1–2 m deep) extends over the walkway. Tarpaulin extensions on poles go out over the drain.
- **Signage.** Fascia boards or flex banners 0.6–1.2 m tall; painted pillars.
- **Goods displayed outside.** Stacks of plastic chairs, buckets, crates of drinks, tyres.

**Share.**

| Location | Share of front houses with shops |
|---|---|
| Main road | 70–90% |
| Collector street | 40% |
| Back street | 10% (plus a kiosk) |

**SELECT BY.** kind front; distance to main road small; dense_mainland ↑; storeys any.

### 6.2 Container shops
- 20 ft ISO shipping container, about 6.06 × 2.44 × 2.59 m (a standard size).
- Placed on blocks at the roadside or the edge of a plot. A doorway cut in the long side, with a hinged steel flap that props up as an awning.
- Repainted in telecom or bank colours, or rusty in its original livery colours (maroon, blue, green, grey).
- Uses: phone credit/airtime, POS/mobile money points, drinks.
- 40 ft containers (12.2 m) occasionally serve as offices.

**SELECT BY.** Main roads, junctions, bus stops, edge of markets; sprawl and dense_mainland.

### 6.3 Kiosks
- **Wooden kiosk.** About 1.8–2.4 m wide, 1.2–1.8 m deep, 2.2–2.5 m tall. Plank or plywood box on short legs or blocks with a mono-pitch zinc roof. A front hatch hinges up as an awning or drops as a counter. Painted in a bright colour, often an operator's colour, then faded and peeling. Hand-painted text.
- **Metal kiosk.** Sheet-steel box of the same size, often fabricated with a roller shutter or swing doors. Painted then rusty.
- **Umbrella stand.** A 2–2.5 m diameter umbrella (multicolour, with advertiser panels) over a table. Common at bus stops and junctions.
- **Frequency.** Every 10–30 m along busy mainland roads [est]. Kiosks crowd junctions and bus stops.

### 6.4 Market stalls
- **Construction.** Timber or steel pole frames, about 2 × 2 m per stall, height 2.0–2.4 m. Lean-to or pitched corrugated sheet roofs, rusty, in continuous rows. Sheets overlap at irregular heights, with tarpaulins tied below.
- **Tarps.** Blue #2E6FB7, orange, green, white.
- **Tables.** Raised wooden tables about 0.8 m high.
- **Formal market sheds.** Long RC or steel sheds with a continuous roof and concrete stalls in rows, 2 × 2.5 m each, aisles 1.5–2 m.
- **Edges.** Open drains and fresh-food market areas have umbrellas and a sun-bleached clutter of tarps.

### 6.5 Plazas (multi-storey shop blocks) and "phone malls"
- **Form.** 2–5 storey RC buildings with a ground-floor arcade plus upper galleries. Shops 2.5–4 m wide, 3–4 m deep; the planned ICT-park shops are 10–11 m² [src: Techpoint]. The front is a regular grid of roller shutters or glass shopfronts on every floor. An open corridor/gallery runs along the front with steel or baluster rails. One or two central stairs.
- **Façade.** Ceramic tiles or ACP (aluminium composite panel) cladding in the newer ones (silver, blue, red); dense banners and signage on every gallery.
- **Phone-mall type.** Small shops inside: glass-front cubicles 2 × 2 m, signage-heavy, with many people and phones displayed. Grew out of single-storey shops [src: Wikipedia Ikeja].
- **Naming.** Painted name "XXX PLAZA" in big letters on the parapet.

**SELECT BY.** Commercial districts and markets; main road; 2–5 storeys; dense_mainland/cbd fringe.

---

## 7. Afro-Brazilian ("brazilian") house (old island)

**Look [src: Wikipedia Architecture of Nigeria, Culture Trip, Prime Progress, Daily Trust].**
- Plastered bungalows or 2-storey (sometimes 3-storey) "sobrado" houses.
- Arched windows and doors (segmental or round).
- Stucco ornament: floral plaster panels, pilasters, string courses, decorated plinths and capitals.
- Wooden shutters (louvred jalousie or solid).
- Wrought-iron balconies.
- Ventilation gaps between wall tops and roof.
- Verandas front and/or back; central courtyards in larger ones.
- Colours: cream stucco and bright colours [src].

**Dimensions [est].**
- Frontage 8–15 m, built to the street line (no setback).
- Ground floor about 3.5–4 m high, upper floor 3.5 m. Total eaves height for 2 storeys about 8 m.
- Windows: about 1.0 × 2.0–2.4 m tall (tall, narrow, vertical proportion 1:2+), set rhythmically at 2–2.5 m centres.
- Upper floor: a balcony (about 1 m deep) on brackets, or a projecting central bay.
- Roof: hipped corrugated iron at 20–30°, often hidden behind a decorated parapet with a central pediment, a date panel or a name plaque [est; inspired by the descriptions].

**Colours [est].**
- Walls: cream #EDE3C8, ochre-yellow #E0B04A, pale blue #9CC7E0, pink #E6A7A8, light green #B5D3A0.
- Ornament and trim: white #F2EFE6.
- Shutters: dark green #2F5E3A, oxblood #6B1F22, brown #5A3A28.

**Weathering.** Heavy: lost stucco pieces exposing brick (#9A4E34) or lime/rubble, black mould, roofs rusted through, vegetation on parapets, shutters missing. Many are demolished or replaced [src: Al Jazeera, Daily Trust]. Ground floors are often converted to shops with roller shutters punched into old arches.

**Variants.**
- Single-storey "bungalow" with a front veranda: 40%.
- 2-storey sobrado: 50%.
- Mosque/church-scale (central pediment): 10% [est].

**SELECT BY.** district old_island (also the Ebute Metta and Yaba fringe [src]); age old; kind brazilian; storeys 1–3; wealth low-mid now (decay), or "restored" rarely.

---

## 8. Stilt houses (waterfront, Makoko-like)

**Look [src: Ripples, AmusingPlanet, WorldAtlas, UNILAG].**
- Hardwood posts driven into the lagoon bed.
- Plank (and some bamboo) walls; corrugated iron roofs, often rusty, with tarpaulin or polythene patches "of various colours".
- Narrow canals between houses, travelled by dugout canoe.
- Each house holds 6–10 people.
- Communal latrines over the water. Fish smoking on house tops.
- Sawmills line the shore, with sawdust mounds.
- Plank or bamboo houses are chosen for affordability (57.5% of respondents) [src].

**Dimensions [est].**
- Posts 0.1–0.2 m diameter at 1.5–2.5 m spacing.
- Floor 1.0–2.0 m above the water.
- Houses 3–6 m × 4–8 m, wall height 2.2–2.5 m, mono-pitch or low gable roof at 10–20°.
- A front platform/porch 1–2 m deep where canoes tie up.
- Canals 2–5 m wide; plank catwalks 0.3–0.6 m wide between houses.
- Larger 2-storey timber buildings (churches, community halls, a "high rise") occasionally appear.

**Colours and weathering [est].**
- Planks: raw weathered grey-brown #6E6152 to dark #4A4036, a green algae line at the water (#3A4A30), a black tar line.
- Occasional painted boards: blue, green, yellow, faded.
- Roofs: rusty orange-brown #7A4524 with silver patches; tarps blue #2E6FB7 and orange.
- Water: black-brown #2A2620 with floating debris and water hyacinth (green).

**Variants.** Plank on stilts 70%; bamboo 15%; with block/concrete base at the shore edge 15% [est].

**SELECT BY.** district waterfront; kind stilt; storeys 1 (rarely 2); wealth lowest. Pair with sawmill/saw-shed, fish-smoking and canoe props.

---

## 9. Elite: mansions, gated villas, apartment towers

### 9.1 Mansions / detached villas (Ikoyi, VI, Lekki, Banana Island, GRA style)
- **Look.** 2–3 storeys plus a penthouse or roof terrace, on 1,000–2,500 m² plots behind 2.5–3.5 m walls with an electric fence and a motorised gate, plus a gatehouse.
- **Two dominant styles [est].**
  - "Classic Nigerian mansion" (1990s–2010s, 40%): multi-hip stone-coated roof (charcoal or terracotta), cream/white/peach render, double-height columned portico with Corinthian-ish columns, baluster balconies, arched windows with keystones, tinted glass.
  - "Contemporary box" (2010s–now, 50%): flat roofs with deep fascias/parapets, grey, white and charcoal palette, wood-look cladding strips, stone-tile feature walls, floor-to-ceiling glazing, frameless glass balustrades, cantilevered slabs.
  - Older Ikoyi colonial/modernist bungalows (10%): deep verandas, broad hipped roofs, large lawns [src: Wikipedia, GRAs with deep verandas].
- **Grounds.** Interlocking paving (grey/red/charcoal paver blocks, 200 × 100 mm, zig-zag). Lawns, palm trees, a pool. BQ at the rear. Large generator house. Car port with a tensile fabric shade.
- **Dimensions [est].** Footprint 15–30 m; floor-to-floor 3.6–4.0 m; height 10–14 m.
- **Colours.**

| Style | Walls | Roof |
|---|---|---|
| Classic | Cream #EDE3C8, peach #F2C9A8, white | Terracotta #8E3B2A or charcoal |
| Contemporary | White #F5F5F2, warm grey #B5B1A8, charcoal #3A3C3E | — |

- **Weathering.** Low, but black streaks from parapets still appear on white façades within 2–3 years.
- **SELECT BY.** district elite; wealth high; distance to main road: medium (on quiet estate streets); storeys 2–3.

### 9.2 Terraces / semi-detached (Lekki estates)
- Rows of 3–6 duplexes, 6–8 m frontage each.
- Grey/white contemporary or classic with stone-coated roofs.
- Inside estate walls, with an estate gate.
- SELECT BY: elite/sprawl-new estates; wealth mid-high.

### 9.3 Apartment towers
- 8–25 floors (Eko high-rise stock samples 12–25 floors; 59% over 20 years old [src: FUDMA]).
- **Older (1970s–90s).** Concrete grid with louvres or naco windows, balconies, stained grey-black concrete, tanks on the roof. Common on Lagos Island/Ikoyi and in housing estates such as the Dolphin and 1004-type estates.
- **Newer (2010+).** Glass and white/grey render, frameless glass balconies, crown features, podium car parking 2–4 floors.
- **Dimensions.** Floor-to-floor about 3.2 m. Footprint 20 × 30 m.
- **SELECT BY.** elite/cbd/old_island; storeys 8–25; wealth mid-high (old ones mid).

---

## 10. Commercial and institutional

### 10.1 Bank tower / office tower
- **Look.** CBD (Marina/Broad St style).
  - 1960s–70s modernist slabs: concrete grids, brise-soleil, mosaic tiles. One heritage list names 19- and 25-storey towers [src: Wikipedia].
  - 1990s–2020s: blue, green or silver curtain-wall glass towers, 15–40 floors.
- **Dimensions.** Floor-to-floor 3.6–4.0 m. Ground-floor banking hall double height (6–8 m), with a canopy and bollards.
- **Colours.** Glass blue-green #3E6E78, silver-reflective #A9B4BA, dark #2B3A44. Concrete #B4B0A6, weathered #7C7A74.
- **Weathering.** Old towers: mould-streaked concrete, broken louvres, AC units hung everywhere.
- **SELECT BY.** cbd/elite; main road; storeys 10–40.

### 10.2 Office (mid-rise) and bank branch
- **Office.** 3–8 storeys, ACP cladding (bank and brand colours: red, blue, orange, green), tinted strip glazing, a car park in front, a security post.
- **Bank branch** (on a main road in every district) [est]:
  - 2–3 storeys with a strongly branded ACP façade band and a glass entrance.
  - Security doors (the "airlock" cylinder door is very characteristic).
  - ATM gallery on the side; a canopy over parking; a gate and gatehouse.
  - Generator and diesel tank at the side.
- **SELECT BY.** Main road; any district except waterfront.

### 10.3 Warehouse (port, industrial)
- **Shed.** Steel portal frame, 20–60 m span, 6–12 m eaves, low-pitch long-span roof (5–10°). Walls are block to 2–3 m, then cladding sheet. Large sliding or roller doors, 4–6 m wide.
- **Colours.** Cladding silver, blue or cream; roof silver or rusted. Older ones: rusted asbestos.
- **Surroundings.** Trucks, containers stacked 2–5 high, a gravel or broken-asphalt yard, high walls with razor wire.
- **SELECT BY.** district port; also the Oshodi/Ikeja industrial fringe; on main road/expressway.

### 10.4 Public primary school
- **Look [est; Lagos rebuilds 10–18-classroom blocks [src: Gazette/Guardian]].**
  - 1–2-storey (newer 3-storey) long classroom blocks.
  - Each classroom about 7 × 9 m; an open veranda corridor (1.8–2.4 m) along one side with square columns; louvre or sliding windows; a hipped or gable long-span roof.
  - Blocks arranged in L or U around a sandy or concrete assembly/field area, with a flagpole.
- **Colours [est].** Older: cream with a brown/maroon plinth, or yellow. Rehabilitated: cream/white with a blue, green or brown band; the school name painted large on the gable or fascia; a mural of the alphabet at the gate.
- **Weathering.** Older: rusted roofs, broken louvres, cracked floors.
- **Grounds and type mix.** Compound wall with a signboard. Several schools often share one compound (e.g. "LGEA Primary School I, II, III"). Private nursery/primary schools in converted houses are far more numerous, marked by colourful signboards and painted cartoon murals.
- **SELECT BY.** kind school; any district; plot large; off the main road.

### 10.5 Church
- **Orthodox/older (Anglican, Catholic, Methodist).** Gothic Revival on the old island [src: Wikipedia] or simple gable halls: rendered, with pointed arched windows, a bell tower or front gable with a cross. Colours: cream, white, grey stone-look.
- **Pentecostal "warehouse church" [src: Lawanson, UNILAG].**
  - Converted warehouses or purpose-built long-span steel sheds: wide-span gable roofs, 20–40 m span.
  - Cladding sheet walls or block with open sides (louvres or big openings), plastic chairs inside.
  - A huge banner or painted name with the ministry name across the gable.
  - Car park, generator, a gate with a gatehouse.
- **Small storefront churches.** Ground-floor shops or rooms with a painted sign and banner.
- **Mega-church auditoria.** Huge sheds with cream/white façades and glazed gables.
- **Colours.** Banners in white/red/blue/purple. Sheds: silver/blue/cream.
- **SELECT BY.** dense_mainland and sprawl (warehouse and storefront churches extremely common, every few hundred metres [est]); elite (orthodox, big modern).

### 10.6 Mosque
- **Neighbourhood mosque [est].**
  - Rectangular block hall, often green and white (green #2E7D32 or #1F6B3A trim on white/cream walls).
  - A small dome (2–6 m) of fibreglass, concrete or metal: green, gold or silver.
  - 1–2 slender minarets, 8–20 m tall, as a square or round shaft with a balcony and a small dome/cap on top, carrying loudspeakers.
  - Arched windows; a crescent on the dome finial.
  - Ablution area: a row of taps with a low wall at the side; kettles (plastic, multicolour) lined up.
- **Central/major mosque.** A large central dome about 15 m across, gold/metal-clad, 4 minarets; a riwaq with columns and a courtyard [src: Lagos Central Mosque pages]. Older 1910s–20s Brazilian-baroque mosques have pediments [src].
- **Frequency [est].** Very common on Lagos Island, in Agege, Mushin and Oshodi (Yoruba Muslim majority areas): about as common as churches. Prayer spaces in shops and compounds are marked with mats.
- **SELECT BY.** kind mosque; old_island ↑, dense_mainland, sprawl.

### 10.7 Clinic / hospital
- **Private clinic.** A converted 2-storey house with a big signboard (red cross, green/white), a ramp, a generator. Painted white/cream with a green or blue band.
- **Primary Health Centre (public).** 1-storey long block, cream with a green/blue band, veranda, louvre windows, a signboard.
- **General hospital.** 2–4 storey blocks with walkways and long-span covered links.
- **SELECT BY.** kind clinic; any district; mainland mostly converted houses.

### 10.8 Chemist (patent medicine store / pharmacy)
- **Look.** A ground-floor shop bay with a green signboard or cross sign, a glass display or a counter behind burglar bars, shelves of boxes visible, a roller shutter.
- **Patent medicine stores.** Small kiosks.
- **Pharmacies** (wealthier areas). Glass fronts with a green cross light box.
- **SELECT BY.** front shops on main/collector roads; every few hundred metres.

### 10.9 Fuel station (avoid real brands)
- **Look.**
  - Forecourt canopy: a flat steel space frame, 20–40 × 12–20 m, at 5–6 m clearance. Fascia band 1–1.2 m deep in brand colours.
  - 2–6 pump islands (1 × 4 m concrete) with 2–4 dispensers each.
  - A shop/office block at the back (1–2 storeys) with a lube bay.
  - A tall pylon price sign at the entrance (6–10 m).
  - Underground tanks marked by filler caps. A large generator.
- **Independent stations.** Hand-painted signs, a tired canopy, rust, faded paint. Queues of cars and danfos (yellow minibuses) during scarcity.
- **SELECT BY.** Main road/expressway; any district except waterfront; plot at junctions.

### 10.10 Hotel
- **Mainland small hotels.** 3–5 storeys; a converted residential block with a bold paint scheme (often 2 colours) and "XXX HOTEL & SUITES" lettering on the parapet. Tinted glass, small car park, gate, a sign with stars.
- **Elite hotels.** 10–25-storey glass towers with a porte-cochère.
- **SELECT BY.** Main road; dense_mainland/sprawl (small); elite/cbd (big).

### 10.11 Barracks
- **Look [est].**
  - Long low 1–2-storey blocks in rows (1950s–80s), sometimes 3–4-storey flat blocks.
  - Painted in uniform schemes, typically cream/white walls with a dark green, ochre or brick-red base band and trim. Asbestos or long-span roofs, often rusted.
  - Kerbs and tree trunks painted white (or black and white).
  - Wide spacing; parade grounds; perimeter wall with a guardpost and a boom gate. Signage boards in military colours. Mammy market (stall row) inside.
- **SELECT BY.** kind barracks; regular grid; low density.

### 10.12 Police station
- **Look.**
  - A 1–2-storey block in a compound, in the standard police colour scheme: light blue walls #8DB6D9 or white, with a dark navy band #1F2E5A.
  - Charge-room counter at the front; a signboard. Impounded vehicles rusting in the yard.
  - Older stations: louvres, a veranda, asbestos or zinc roof.
- **SELECT BY.** kind police; main road; any district.

### 10.13 Bakery
- **Look.** A shed or ground-floor unit with a wide door, and a chimney or flue from wood/diesel ovens leaving soot stains (#2A2A28) on the wall above. Bread vans and wheelbarrows outside. A sales window with a signboard. Often in a back street of dense_mainland or sprawl.
- **SELECT BY.** kind bakery; dense_mainland/sprawl.

### 10.14 Sawmill / saw shed
- **Look.**
  - Open shed with a steel or timber frame and a rusty corrugated roof, lean-to or gable at 5–10° on tall posts (4–6 m).
  - A bandsaw or circular-saw bench under the roof.
  - Piles of logs and planks stacked outside, sawdust mounds (pale tan #C8A878 fresh, dark brown #6A4A30 old).
  - Riverside sites: logs floating in the water. Mounds of sawdust burning or smouldering [src: Ripples on Makoko sawmills].
- **SELECT BY.** waterfront edge, port edge, sprawl industrial.

### 10.15 Gatehouse (as standalone kind)
- See §4. 2 × 2–3 × 3 m, 2.4–2.8 m tall, door plus window, flat or mono-pitch roof, painted the compound colour, a plastic chair and a bench. Elite: a glazed booth with a boom barrier.

### 10.16 Palace (traditional ruler, Oba's palace)
- **Look [est].**
  - A walled compound with a large ornate gate and entrance arch, often painted bold (gold/ochre, white, red or royal blue/purple accents).
  - Inside, a mixture of an older courtyard building (single or 2-storey, verandas, carved posts — Yoruba palace tradition [src: Wikipedia]) and modern 2–3-storey blocks with a columned portico.
  - Open courtyard for gatherings; crests and emblems on the gate and pediment.
  - Palace precinct markers: shrines, large trees, an open square in front.
- **SELECT BY.** kind palace; old_island core (and older town cores in sprawl, such as Ikorodu and Epe-type towns).

---

## 11. How appearance varies by area, wealth, age, road position

| Trait | old_island | dense_mainland | sprawl | elite | waterfront | port |
|---|---|---|---|---|---|---|
| Typical storeys | 2–4 (some 10–25 towers) | 1–3 | 1–2 | 2–3 houses; 8–25 towers | 1 | 1–2 sheds |
| Plot frontage | 6–15 m, no setback | 12–18 m, 0–3 m setback | 18 m+, walled | 25–50 m, deep setback | n/a | 50 m+ |
| Main roof | Rusty corrugated, parapets | Long-span plus rusty corrugated mix | Long-span bright colours (red, blue, green) | Stone-coated / flat | Rusty corrugated plus tarps | Silver/rust long-span |
| Façade | Painted render, ornament, many shops | Faded paint, bare side walls, shops | Fresh paint or raw block; many unfinished | White/grey, glass, cladding | Raw timber | Cladding |
| Window | Shutters, louvres | Louvres → sliding | Sliding | Sliding / curtain wall | Openings with plank shutters | High strip |
| Walls/gates | None (street-built) | Short or none at front | Always walled, steel gates | High walls, electric fence | None | High, razor wire |
| Unfinished share | Low | Medium (upper floors) | High | Low-medium | n/a | Low |
| Weathering | Very high | High | Low-medium (new) | Low | Very high | Medium-high |
| Shops density | Very high | High on roads | Medium on roads | Very low (plazas only) | Canoe trade | Kiosks at gates |

**Correlations [est].**
- **Main road vs back street.**
  - Storeys +1. Probability of ground-floor shops 0.7–0.9 vs 0.1.
  - Signage density 5–10×. Kiosks and containers line the frontage. Fresher paint on the front façade (owners repaint for business and regulators push owners on major roads to repaint [src: Gazette 2025]).
  - Back streets: lower, more walled compounds, more raw block, more back houses, more tanks visible.
- **Storeys.** 3+ storeys correlate with a flat or parapet roof, a central stair, balconies with balusters, and sliding windows. Bungalows correlate with hipped zinc, louvres and a veranda.
- **Age.** pre-1970: corrugated iron, shutters/louvres, verandas, arched or hooded windows. 1970–95: louvres, baluster balconies, spatter render, asbestos/corrugated. 1995–now: sliding aluminium, long-span colour roofs, square-pipe burglar bars. 2010–now: stone-coated tiles, grey palettes, glass balustrades, ACP cladding, solar panels.
- **Wealth.** More: whiter paint, less rust, more AC units and dishes, higher walls, electric fences, interlock paving, generator houses. Less: tyre-weighted roofs, polythene patches, bare block, broken louvres, bigger shared-yard blocks.
- **Use.** Commercial: fascia boards, banners, roller shutters, canopies. Religious: banners, domes or big gables, open forecourts. Institutional: uniform paint schemes (police blue/navy; military cream/green; school cream with a coloured band).

---

## Sources
- Face-me-I-face-you (Wikipedia): https://en.wikipedia.org/wiki/Face-me-I-face-you
- Bloomberg, history and design of face-me-I-face-you homes (search summary only; page 403): https://www.bloomberg.com/news/features/2022-05-05/the-history-and-design-of-lagos-face-me-i-face-you-homes
- Guardian NG, What kind of house do most Nigerians live in (search summary): https://guardian.ng/nigerian/what-kind-of-house-do-most-nigerians-live-in/
- UNILAG CHSD, Covid-19 and housing design inadequacy in Lagos: https://chsd.unilag.edu.ng/?p=558
- Architecture of Nigeria (Wikipedia): https://en.wikipedia.org/wiki/Architecture_of_Nigeria
- Prime Progress, Afro-Brazilian architecture that shaped Lagos: https://primeprogressng.com/social-impact/the-afro-brazilian-architecture-that-shaped-lagos-city/
- Culture Trip, Brazilian Quarter in Lagos: https://theculturetrip.com/articles/the-brazilian-quarter-in-lagos
- Daily Trust, Lagos Afro-Brazilian architecture under threat: https://dailytrust.com.ng/lagos-afro-brazilian-architecture-under-threat.html
- Al Jazeera, Is Nigeria's Brazilian heritage under threat?: https://www.aljazeera.com/indepth/features/2016/10/nigeria-brazilian-heritage-threat-161024144110141.html
- Harrison & Igwe, Afro-Brazilian Style of Architecture in Lagos (abstract): https://ir.unilag.edu.ng/handle/123456789/7187
- Sobrado (Wikipedia): https://en.wikipedia.org/wiki/Sobrado_(architecture)
- Ripples Nigeria, 75 images of Makoko: https://ripplesnigeria.com/living-on-stilts-75-unforgettable-images-of-makoko-will-it-survive-sanwo-olus-smart-city-plan
- AmusingPlanet, Makoko: https://www.amusingplanet.com/2014/04/makoko-floating-slum-in-nigeria.html
- WorldAtlas, Makoko: https://www.worldatlas.com/articles/what-and-where-is-the-makoko-slum.html
- UNILAG, Housing material types in Makoko: https://ir.unilag.edu.ng/handle/123456789/12268
- Makoko Floating School (PreventionWeb): https://www.preventionweb.net/news/floating-architecture-makoko-floating-school
- Sandcrete block quality in Lagos metropolis: https://spaj.ukm.my/jsb/index.php/jbp/article/view/156
- Ownkey, Roofing materials compared Nigeria: https://ownkey.com/ng/blog/roofing-materials-compared-nigeria
- Jiji long-span roofing listings (colour lists, gauges): https://jiji.ng/ha/agege/building-materials/0-55-longspan-aluminium-roofing-sheets-a6csp0u9ZDCgqzisyaLncLha.html
- BusinessDay, roofing sheet gauges: https://archive.businessday.ng/real-sector/article/roofing-sheet-makers-make-case-for-0-3mm-as-competition-toughens/
- Jiji burglar-proof listings: https://jiji.ng/263-gates/burglary
- Emerald, abandonment of multi-storey projects in Lagos: https://www.emerald.com/insight/content/doi/10.1108/IJBPA-10-2017-0048/full/html
- IRE Journals, uncompleted buildings in Eti-Osa: https://www.irejournals.com/paper-details/1709595
- Lawanson, Planning and Pentecostalism in Lagos: https://ir.unilag.edu.ng/handle/123456789/10166
- BusinessDay, worship centres anywhere: https://businessday.ng/?p=105873
- Lagos Central Mosque (Wikipedia / Mosqpedia / Archnet): https://en.wikipedia.org/wiki/Lagos_Central_Mosque , https://mosqpedia.org/?p=17952 , https://archnet.org/publications/14316
- Ikeja / Computer Village (Wikipedia): https://en.wikipedia.org/wiki/Ikeja
- Techpoint, Computer Village relocation (shop sizes): https://techpoint.africa/2018/08/23/relocation-of-computer-village/
- FUDMA J. Sci., multi-storey housing stock in Lagos: https://fjs.fudutsinma.edu.ng/index.php/fjs/article/view/5630
- Gazette NG, Lagos facade/repaint appeal (2025): https://gazettengr.com/?p=387966
- Guardian NG, Lagos school regeneration: https://guardian.ng/?p=1214206
- Nigerian water tank prices: https://nigerianqueries.com/water-storage-tank-prices-in-nigeria/
