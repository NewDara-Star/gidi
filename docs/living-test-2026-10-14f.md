# City living test, 14 Oct 2026 (sixth run): eleven districts, with the new Old Island

There are two states:
- **Before:** `main` at the start of this work (commit `ea47fc6`, ten districts).
- **After:** this branch.

Twelve Haiku agents ran:
- **New: Bisi,** a cloth seller on Old Island
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
- the chase

I re-ran every problem they reported and checked it by hand.

## How life feels (short version)
- **Old Island is a walking town.**
  - Bisi's Brazilian house to her stall in the Cloth Market is a 4.8-minute walk.
  - The palace is 7.7 minutes from home. Bank Row's towers on the far shore are 13.8 minutes from the palace.
  - Every everyday place is within 1.1 km.
- **The bridges work.**
  - Chidi walked from the Port's Old Reserve Avenue over the Wharf Bridge to the Cloth Market in 16.4 minutes.
  - Sule walked from Mile Market over the Long Bridge in 41 minutes. Bola walked from the stilt village in 25.
- **Okadas stop at the ban.** Okadas are banned on the island, so every rider drops passengers at the edge road. From there it is up to 625 m on foot to the Cloth Market (Tunde, Sule). Riders leave by the Long Bridge, since the Wharf Bridge lands in the Port's ban zone.
- **The rest of the city is unchanged.** All 32 earlier standard trips give the same numbers as before.
- **The opening is intact:**
  - Tunde's room → The steal: 1.9 minutes
  - The steal → the boss's post: 1.6 minutes
  - The chase found 4 distinct first turns out of the stall area.
- **Everyday places:** every home in all eleven districts has a school, a place of worship and a chemist within 10 minutes.

## Verified problems, and what was fixed
1. **Fixed (tool): the bridges to the island would have been cut off.** The living-test tool clipped every arterial to 120 m round the built districts, which leaves the middle of a 400 m or 1.6 km bridge out. It now keeps a bridge whole when both its ends are in built districts. It also joins a bridge end that lands within 40 m of a road; the Long Bridge's Water Town end is 18 m short of Adebayo Road.
2. **Fixed (generator): the bridges landed in the water or on the shore line.** Each bridge now has a short link road onto the island's edge road (`bridge_links`).
3. **Open, design:** with the Port and Old Island both banned, an okada can't use the Wharf Bridge at all. Cloth Market → Container Yard by okada is 6.9 km round by the Long Bridge (Bisi). The walk over the Wharf Bridge is 1.9 km. This belongs to the story-map decision on okada bans, like the Estate's.
4. **Open, design:** Bank Row is 924 m on foot from the nearest road an okada may use (Bisi).
5. **Open, carried over:**
   - okada rides longer than walks wherever walkers use paths or footbridges (Funmi, Sule)
   - rides round the Capital's ban (Ngozi, Musa: Gadget Village → Estate Gate ×4.82)
   - pins in the middle of walled plots: the Airport Fence 57 m, Daleko 65 m, the barracks 76 m, Kiri Prison 83 m, the Tank Farm 102 m, and now the Island Motor Park 35 m
   - Bakery Row → the cattle market

## Not problems (checked)
- **Brazilian Quarter → Island Motor Park, ×1.92 (Bisi):** the pin sits inside the park and snaps to the street behind it. Walking to the park's front on Waterfront Drive is ×1.40.
- **"709 m unnamed street outside the built districts" (Sule):** the street is on the island. The label comes from the walk's stretch of bridge over the lagoon.
- **Tunde's room misses 3 minutes (Tunde):** the agent picked a different back house. The locked Tunde's room is 161 m (1.9 minutes) from The steal.
- **The island at 5358,5268:** a 20 m sketch street of the unbuilt Heights, like the Border's at 673,4721.
- **`look 4250 5000` is empty (Bisi):** that point is in the lagoon.

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| The 32 earlier trips | | | unchanged |
| **Brazilian Quarter → Cloth Market (new)** | walk | — | **404 m / 4.8 min / ×1.31** |
| **Bank Row → The Palace (new)** | walk | — | **1,149 m / 13.8 min / ×1.25** |
| **Cloth Market → Container Yard (new)** | walk | — | **1,862 m / 22.3 min / ×1.60** (over the Wharf Bridge) |
| **Cloth Market → Gidi Interchange (new)** | ride | — | **4,997 m / 18.4 min / ×1.70** (625 m on foot out of the ban, then the Long Bridge) |
| **Island Motor Park → Mile Market (new)** | ride | — | **4,011 m / 14.5 min / ×1.38** (406 m on foot, the Long Bridge) |

## City measures
| | Before | After |
|---|---|---|
| Districts built | 10 | 11 |
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| Houses over 45 m from a way (the tool's count) | 106 | 108 (2 on Old Island, both 45–46 m) |
| `check_district.py` | pass (10) | pass (11) |
| Every district regenerates byte-identical | yes | yes |
| Lagos-isms logged | 12 isms × 12 areas | 13 isms × 13 areas |

## Tool artefacts (not city problems)
- **District names aren't places,** and bridges and footbridges can't be used as walk targets.
- **A repeated name picks one of its places** without saying so (Good Health Chemist, Destiny Child College, Secretariat).
- **`home N`** gives ordinary houses first; Brazilian houses and back rooms need `look`.
- **No time of day,** no bus or train trips, and no checkpoint seizures in `ride`.
