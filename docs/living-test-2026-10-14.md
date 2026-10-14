# City living test, 14 Oct 2026: six districts, with the new Capital

This is the test in `docs/CITY-LIVING-TEST.md`, run on the whole built city after the Capital was added. It also covers Water Town v2 (fingers to the shore) and the boss's post, which this branch carries.

There are two states:
- **Before:** `main` at the start of this work (commit `1db3434`).
- **After:** this branch.

Both are measured with the same `explore_city.py`.

Seven Haiku agents ran on the after state, one per persona:
- **New: Ngozi,** a phone trader in the Capital's Gadget Village
- Tunde, okada rider
- Mama Ronke, food seller on foot in the Hub
- Kemi, a student in Jungle City
- Sule, a night porter in Food Gate
- Bola, a canoe paddler in Water Town
- the chase

I re-ran every problem they reported and checked it by hand before it went into this file.

## How life feels (short version)
- **The Capital joins the city.**
  - From its centre an okada reaches the Interchange in 3.3 minutes and Mile Market in 3.6. Before, neither had a route.
  - On foot, Gadget Village is 14 minutes from the Interchange and 19 from Mile Market.
  - Inside, the phone malls to the Allen roundabout strip is 3.5 minutes.
- **It feels like a different kind of place.** The roads are wide and run straight through, and there are few dead ends. Big buildings stand on the main roads. The walled places, the Secretariat, the barracks and the airfield edge, make you go round them.
- **The opening is intact.**
  - Room → stall: 1.9 minutes.
  - Stall → boss's post, straight down the aisle: 1.6 minutes.
  - Post → motor park: 3.6 minutes.
  - Four separate ways lead out of the market.
- **Everyday life:** every home in all six districts has a school, a place of worship and a chemist or clinic within 10 minutes. The worst is 9.9 minutes, in the Capital.
- **What still grates:**
  - Short walks to a place inside a walled plot or behind a compound go round the block, ×2.5–3.7. Examples: the Secretariat → the Shrine, and a Capital home → its primary school.
  - Okadas go the long way round where walkers use footbridges and skywalks. The tool doesn't yet stop okadas at the Capital's edge, where they are banned.

## The days (shortened)
- **Ngozi (Capital, on foot):**
  - Home (2177,3639) to the strip: 8.5 minutes. The Shrine: 10.8. The Secretariat: 14.5. The airport fence: 10.2.
  - Hospital 6.1 minutes, primary school 6.3, church 8.0.
  - The Interchange is 12 minutes on foot and Mile Market 16. By okada from the edge, each is under 3.5 minutes.
- **Tunde:**
  - Room to the boss's park: 6.9 minutes on foot, 1.4 by bike.
  - Ladi Lane to Gadget Village by okada: 1,625 m, ×1.39.
  - Northern Bus Park to Ireti Hotel: 7 minutes.
- **Mama Ronke (the Hub):**
  - Under the Bridge to the primary school: 1.6 minutes. The bank: 5.9. Ladi Lane: 11.6.
  - Into the Capital: Gadget Village is 14.5 minutes on foot.
- **Kemi (Jungle City):**
  - School: 6.8–12.9 minutes. Boundary Plank Market: 7–9 minutes.
  - The Secretariat: 8.9 minutes by okada.
- **Sule (Food Gate):**
  - Mile Market to the bus park: 6.0 minutes over the footbridge.
  - Into the Capital: Gadget Village is 19.3 minutes on foot or 3.5 by okada.
- **Bola (Water Town):**
  - Walking along a finger (x 3,950): ×1.25. Across fingers at the inland end (y 4,150): ×1.21. Across at the shore end: ×2.4–2.7, because the fingers don't join there. That's the shape.
  - The jetty: 13 minutes. The school: 7. A church: 8.4.
- **The chase:**
  - Stall → post: 137 m, ×1.07.
  - Escapes: north ×1.54, east ×1.47, south-east by Ring Road ×1.74, west through the aisle ×1.10.

## Standard trips
| Trip | Mode | Before: m / min / detour | After: m / min / detour |
|---|---|---|---|
| Tunde's room → The steal | walk | 161 / 1.9 / ×1.50 | 161 / 1.9 / ×1.50 |
| **The steal → boss's post (new)** | walk | — | **137 / 1.6 / ×1.07** |
| The steal → boss's motor park | walk | 429 / 5.1 / ×1.29 | 429 / 5.1 / ×1.29 |
| The steal → Gang Canal | walk | 496 / 6.0 / ×1.49 | 496 / 6.0 / ×1.49 |
| Maze house by the rail → Ladi Lane | walk | 828 / 9.9 / ×1.37 | 828 / 9.9 / ×1.37 |
| Gidi Interchange → Hub Rail Station | walk | 220 / 2.6 / ×1.04 | 220 / 2.6 / ×1.04 |
| Boss's motor park → Ladi Lane | ride | 477 / 1.1 / ×1.73 | 477 / 1.1 / ×1.73 |
| Under the Bridge → Daleko Grain Yard | walk | 1,222 / 14.7 / ×1.28 | 1,222 / 14.7 / ×1.28 |
| Jungle City centre → Interchange | ride | 2,201 / 5.3 / ×1.43 | 2,201 / 5.3 / ×1.43 |
| Food Gate house → Mile Market | walk | 639 / 7.7 / ×1.18 | 639 / 7.7 / ×1.18 |
| Mile Market → Ladi Lane | ride | 1,569 / 3.8 / ×1.33 | 1,569 / 3.8 / ×1.33 |
| Jungle City 3017,5225 → 3029,5181 | walk | 147 / 1.8 / ×3.23 | 147 / 1.8 / ×3.23 |
| Water Town centre → Interchange | ride | 2,083 / 5.0 / ×1.21 | 2,226 / 5.3 / ×1.29 (fingers) |
| Stilt Village → Canoe Jetty | walk | 963 / 11.6 / ×1.11 | 963 / 11.6 / ×1.11 |
| Stilt Village → Mile Market | walk | 1,123 / 13.5 / ×1.21 | 1,196 / 14.4 / ×1.29 (fingers) |
| **Capital centre (1980,3300) → Interchange (new)** | ride | no route (not built) | **1,358 / 3.3 / ×1.36** |
| **Capital centre → Mile Market (new)** | ride | no route | **1,490 / 3.6 / ×1.32** |
| **Gadget Village → Allen Roundabout Strip (new)** | walk | — | **295 / 3.5 / ×1.47** |
| **Gadget Village → Interchange (new)** | walk | — | **1,167 / 14.0 / ×1.33** |

## City measures
| | Before | After | Target |
|---|---|---|---|
| School / worship / chemist within 10 min, every district | 100% (5 districts) | **100% (6 districts)** | 100% |
| Worst walk to an everyday place | 9.9 min | 9.9 min (Capital school) | ≤ 10 min |
| Walking islands inside the built districts | 0 | 0 | 0 |
| Walking islands at the study border | 6 | 5 | tiny pieces only |
| Houses > 45 m from a way (tool, by house centre) | 51 of 10,777 | 72 of 11,955 | 0 by wall (`check_district.py` passes) |
| `check_district.py`, all districts | pass | **pass (6)** | all pass |
| Every district regenerates byte-identical | yes (5) | **yes (6)** | yes |

## Verified problems (real), with coordinates
1. **Short walks around walled plots** (open, a design choice for now):
   - `walk "Secretariat" "The Shrine"`: 698 m for 282 m, ×2.47.
   - `walk 2177,3639 "Capital Primary School No. 8"`: 522 m for 143 m, ×3.65.
   - `walk 2177,3639 "Cantonment"`: 431 m for 174 m, ×2.47. The barracks has one gate.
   - Walled government, school and barracks plots are real, but a second gate on the Secretariat and the barracks would make short walks less roundabout.
2. **Okadas aren't stopped at the Capital's edge** (open). The map marks the Capital okada-banned, but `ride` routes straight through it. The tool, and later the game, need a ban zone; this is a question for the owner in the Capital study.
3. **Still open from the last test:**
   - okada detours round skywalks (Interchange → station, ×3.47)
   - the Hub's 254 m rail gap
   - pedestrians walking along arterials
   - long walks to a place behind a back house

## Tool artefacts (not city problems)
- **Islands at 2289,5243, 1737,4959, 3304,5540, 1404,3596 and 2020,2619:** all outside the built districts. They are the unbuilt neighbours' sketch roads cut at the border (now including the Estate's and Railside's next to the Capital).
- **"1,166 m unnamed street"** in a walk: several unnamed streets in a row are summed into one line.
- **Pins in the middle of big plots:** the Cantonment (84 m from a way) and the Secretariat (50 m), as with Mile Market. Also "inside the bust" when standing on the Allen roundabout pin.
- **Name lookup picks the first match:** Alafia Pharmacy, Excellence Academy, Remedy Stores and Fresh Life Pharmacy all exist in more than one district. Use X,Y.
- **"Agboyi Creek Villages" reached on land:** the pin is the jetty's end.
- **No time of day, bus or train** in the tool.

## What was fixed in this session
- **The Capital built** (see `docs/capital-pattern-study.md`).
- **From this test (tool):**
  - `home N district` picks a house in one district. Four agents had landed in the Capital, which comes first.
  - Water Town's bent shore roads no longer read "outside the built districts".
- **Generator:**
  - the half-route bug
  - `t_into_done`
  - the Hub keeps its crossings, so it stays identical when regenerated
