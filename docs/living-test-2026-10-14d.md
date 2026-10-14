# City living test, 14 Oct 2026 (fourth run): nine districts, with the new Railside

There are two states:
- **Before:** `main` at the start of this work (commit `8a23e34`, eight districts).
- **After:** this branch.

Ten Haiku agents ran:
- **New: Funmi,** a bread seller in Railside
- Ngozi (the Capital, re-laid in this branch)
- Emeka (the Bazaar)
- Tunde (okada)
- Mama Ronke (the Hub)
- Kemi (Jungle City)
- Sule (Food Gate)
- Bola (Water Town)
- Chidi (the Port)
- the chase

I re-ran every problem they reported and checked it by hand.

## How life feels (short version)
- **Railside is the city's commuter belt.**
  - Bakery Row to the roundabout market is a 6-minute walk at dawn.
  - The market roundabout to the Hub's interchange is 6 minutes by okada.
  - Funmi's house, 17 m from the rail, is 4 minutes by okada from the interchange, over the Ring Road rail bridge.
  - It's okada heartland: no ban, long roads, low houses.
- **The Capital was re-laid** (see the Railside study). Gadget Village to the Allen strip is now 232 m (2.8 minutes); it was 373 m.
- **The opening is intact:** stall → boss's post 1.6 minutes, stall → motor park 5.1.
- **Everyday places:** every home in all nine districts has a school, a place of worship and a chemist within 10 minutes. The worst is 10.0 minutes.

## Verified problems, and what was fixed
1. **Fixed: the Capital's main road crossed the rail at ground level in Railside.** Funmi walked over it. It now crosses on a 46 m bridge, as real major roads there do, 4 times in 6.
2. **Fixed: a street ran across the market roundabout's island.** The bust stood in the road. Streets now stop at every roundabout's ring; the Capital had the same problem, unseen.
3. **Fixed (tool): rides with both ends inside the Capital's ban zone** went out through Railside and the Hub (Gadget Village → Secretariat, ×5.73). The tool now says to walk.
4. **Open: Bakery Row → the cattle market** is 531 m for 211 m (×2.52). The cattle market's gate faces away.
5. **Open, carried over:**
   - okada rides longer than walks wherever walkers use paths, skywalks or footbridges
   - one Jungle City walk crosses the expressway at grade (`walk 2500,5200 2500,5800`)
   - pins in the middle of walled plots: the prison is 83 m from a way, the tank farm 102 m

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| The 22 earlier trips outside the Capital and the Bazaar | | | unchanged |
| Gadget Village → Allen Roundabout Strip | walk | 373 m / 4.5 min / ×1.85 | **232 / 2.8 / ×1.82** (re-laid Capital) |
| Gadget Village → Gidi Interchange | walk | 1,142 / 13.7 / ×1.30 | 1,127 / 13.5 / ×1.28 |
| Capital centre → Gidi Interchange | ride | 1,763 / 9.3 | 1,724 / 9.2 |
| Alade Electronics Market → Gidi Interchange | ride | 1,465 / 5.0 | 1,647 / 5.4 (the Bazaar kept its crossings) |
| **Ayo Bakery Row → Roundabout Market (new)** | walk | — | **520 m / 6.2 min / ×1.17** |
| **Roundabout Market → Gidi Interchange (new)** | ride | — | **2,194 m / 5.9 min** |

## City measures
| | Before | After |
|---|---|---|
| Districts built | 8 | 9 |
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| `check_district.py` | pass (8) | pass (9) |
| Every district regenerates byte-identical | yes | yes |
| Lagos-isms logged | — | 11 isms × 11 studied areas (`docs/LAGOS-ISMS.md`) |

## Tool artefacts (not city problems)
- **Islands at 673,4721 and 2020,2619:** sketch roads of the unbuilt Border and Estate.
- **`look` and `home` take numbers only;** district names aren't places.
- **The "you pass" list includes the trip's own ends.**
- **`places` is long:** 342 places across nine districts.
