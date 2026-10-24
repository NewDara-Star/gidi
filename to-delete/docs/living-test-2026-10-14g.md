# City living test, 14 Oct 2026 (seventh run): twelve districts, with the new Heights

There are two states:
- **Before:** `main` at the start of this work (commit `02f2a78`, eleven districts).
- **After:** this branch. It does three things:
  - pins of walled places now stand at their gates
  - the Palace is safe ground in the data
  - the Heights is built

Thirteen Haiku agents ran:
- **New: Kunle,** a driver in the Heights
- Tunde (okada)
- Mama Ronke (the Hub)
- Kemi (Jungle City)
- Sule (Food Gate)
- Bola (Water Town)
- Ngozi (the Capital)
- Emeka (the Bazaar)
- Chidi (the Port)
- Funmi (Railside)
- Musa (the Estate)
- Bisi (Old Island)
- the chase

I re-ran every problem they reported and checked it by hand.

## How life feels (short version)
- **The Heights is a quiet place to walk:**
  - Pearl Towers to the Club Strip is a 5-minute walk.
  - From the Gold Island's gate, Pearl Towers is 11 minutes and the Cable Bridge's toll booths under 6.
  - Sunday Beach is 10–15 minutes from anywhere in the district.
  - Every home has a school, a place of worship and a chemist within 10 minutes.
- **It joins Old Island on foot:**
  - Pearl Towers to the Cloth Market is 13 minutes.
  - Bisi walked from her Brazilian house to Pearl Towers in 7.4 minutes.
- **By okada it is far away.** The Heights and Old Island are both banned. A rider from the Club Strip to Gidi Interchange walks 702 m out of the bans first, then rides over the Long Bridge: 5.7 km in 20.5 minutes. Tunde's ride from the boss's park to the Club Strip is 5.7 km in 21 minutes.
- **The gated closes still let people walk in.** A close in the north-west is 269 m end to end through its gate (×1.01).
- **Pins at gates:** trips to the moved places now start and end at their gates.
  - Under the Bridge → Daleko is 171 m shorter.
  - Estate Gate → the Senator's House is 61 m shorter.
  - Bank Row → the Palace is 65 m shorter, but its detour rises to ×1.45, because the gate is on the Palace's near side and the straight line shrinks more than the walk.
- **The Palace is safe ground.** `look` there says so, and the map card shows the tag.
- **The opening is intact:**
  - Tunde's room → The steal: 1.9 minutes
  - The steal → the boss's post: 1.6 minutes
  - The chase found 4 distinct first turns out of the stall area.

## Verified problems, and what was fixed
1. **Fixed (generator): the Heights' cul-de-sacs had no gates.** The first rule gated only closes that open onto a public road, and none do in the Heights. Every cul-de-sac is now gated at its mouth: 20 gates.
2. **Fixed (generator): Pearl Towers could not be placed.** The Heights' houses stand 8–16 m back, so no house was in the "front row" the tower rule looks for. The towers now replace a house up to 20 m back and stand on its line, within 250 m of the pin.
3. **Fixed (check): a rebuilt Old Island house crossed the shore by 0.0104 m².** Coordinates are written to 0.1 m, so the check now allows 0.05 m², as the overlap check does.
4. **Open, new: the Bazaar's barracks checkpoint isn't at the barracks gate (Emeka).**
   - The checkpoint ("Checkpoint outside") stands on the north side at 1369,4823.
   - The barracks' access road, and now its pin, are on the south-east side at 1459,4978, 179 m away.
   - Moving the checkpoint means rebuilding the Bazaar, so it is left for a session on the Bazaar.
5. **Open, small: a few back houses are tall.** The height rule can give a back house a tall band: 19 in the whole city, 1 in the Heights (8 storeys at 5850,4700, Kunle). This is old behaviour.
6. **Open, design:** the Heights is an okada desert. It and Old Island are both banned, so the nearest legal road is up to 700 m away, over the Long Bridge (Kunle, Tunde). This belongs with the other ban questions for the story map.
7. **Open, carried over:**
   - okada rides longer than walks (Mama Ronke, Sule, Bola, Emeka, Funmi)
   - rides round the bans (Kemi, Musa, Ngozi)
   - pedestrians routed along the expressway (Emeka)
   - Bakery Row → the cattle market

## Not problems (checked)
- **"Al-Furqan Mosque is 11.3 minutes" (Kunle), "no mosque within 1 km" (Bola):** the rule is any place of worship within 10 minutes. Kunle's church is 2.7 minutes away, Bola's 9.7.
- **The island at 6521,5111:** a sketch street of the unbuilt Frontier, like the Border's at 673,4721.
- **"No gatehouse" (Kunle, Musa):** the `look` spots were away from the gates. The Heights has 20 gates with gatehouses; the Estate's are on its streets' mouths.
- **Pearl Towers' pin is 39 m off the street (Bisi):** the towers stand behind front yards, like the houses.
- **A house on the same spot as a chemist (Mama Ronke):** civic places take over a real plot by design.

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| The other 24 earlier trips | | | unchanged |
| Gidi Interchange → Hub Rail Station | walk | 220 m / 2.6 min / ×1.04 | 210 m / 2.5 min / ×1.12 (interchange pin at its gate) |
| Under the Bridge → Daleko Grain Yard | walk | 1,222 m / 14.7 min / ×1.28 | 1,051 m / 12.6 min / ×1.25 (Daleko at its gate) |
| Estate Gate → The Senator's House | walk | 750 m / 9.0 min / ×1.24 | 689 m / 8.3 min / ×1.22 |
| Bank Row → The Palace | walk | 1,149 m / 13.8 min / ×1.25 | 1,084 m / 13.0 min / ×1.45 |
| Rides to Gidi Interchange (8 trips) | ride | | 2–7% shorter (its pin moved 29 m to its gate) |
| Island Motor Park → Mile Market | ride | 4,011 m / 14.5 min / ×1.38 | 4,024 m / 14.7 min / ×1.36 (the park's pin at its gate) |
| **Pearl Towers → Club Strip (new)** | walk | — | **427 m / 5.1 min / ×1.33** |
| **The Gold Island → Pearl Towers (new)** | walk | — | **912 m / 10.9 min / ×1.30** |
| **Cable Bridge → Sunday Beach (new)** | walk | — | **1,247 m / 15.0 min / ×1.06** |
| **Pearl Towers → Cloth Market (new)** | walk | — | **1,090 m / 13.1 min / ×1.11** |
| **Club Strip → Gidi Interchange (new)** | ride | — | **5,742 m / 20.5 min / ×1.37** (702 m on foot out of the bans) |

## City measures
| | Before | After |
|---|---|---|
| Districts built | 11 | 12 |
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| Houses over 45 m from a way (the tool's count) | 108 | 113 (3 in the Heights, 4 on Old Island; all 45–46 m) |
| Safe places marked in the data | 0 | 239, with 200 plots |
| `check_district.py` | pass (11) | pass (12) |
| Every district regenerates byte-identical | yes | yes (Old Island rebuilt once with `keep_gateways`) |
| Lagos-isms logged | 13 isms × 13 areas | 13 isms × 14 areas |

## Tool artefacts (not city problems)
- **Names:** district names, roads, bridges, footbridges and parcels can't be used as walk targets. A repeated name picks one of its places without saying so (Secretariat, Cure Pharmacy, Good Health Chemist).
- **`home N`** gives street houses only; stilt houses and boys' quarters need `look`.
- **`look`** takes numbers, not names.
- **No time of day,** no bus or train trips, and no checkpoint seizures in `ride`.
