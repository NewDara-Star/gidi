# City living test, 15 Oct 2026: the Border

There are two states:
- **Before:** `main` at commit `cf613f8` (thirteen districts).
- **After:** this branch: the Border, and Railside rebuilt once with `keep_gateways`.

Old Shore was built at the same time on its own branch; this test doesn't include it. The other twelve districts regenerate byte-identical. Three agents ran:
- **New: Dayo,** a rice runner on the Border
- **Emeka** (the Bazaar, next door)
- **Funmi** (Railside, rebuilt)

## How life feels (short version)
- **The Border by okada is quick:**
  - Coconut Beach to the Border Post is 2.9 minutes, the Border Post to Checkpoint Mile 1.2.
  - Coconut Beach to the Bazaar's electronics market is 5.1 minutes.
- **Everyday places are close:** from Dayo's house a church is 71 m away, a school 58 m and a chemist 139 m.
- **The edges join:**
  - Emeka rode from his lock-up to the Border Post in 5.4 minutes along the expressway.
  - Funmi rode from Railside's bakeries to Checkpoint Mile in 6.4 minutes, crossing from Railside into the Border on one street.
- **The checkpoints can be walked round:**
  - with the expressway taken out of the walking network, the west end still reaches the east end: 1.28–1.46 km, against 1.21–1.25 km along the road
  - the bush paths and back streets go round every post
  - the tool's shortest walk still prefers the road, because the walk doesn't avoid checkpoints (Dayo)
- **The opening and the rest of the city:** unchanged.

## Verified problems, and what was fixed
1. **Fixed (generator): a checkpoint's drums stood across a side street's mouth.** Posts now skip any spot where their drums would touch a side street.
2. **Fixed (generator): the Border's main road would have crossed into finished Railside.** It now meets the neighbours' edge roads in a T (`t_into_done`), so it makes no new crossing.
3. **Open, tool:**
   - the walk and ride don't know about checkpoints (Dayo): a run that avoids the posts has to be found by hand
   - drums aren't a cost to an okada
4. **Open, carried over:**
   - okada rides longer than walks (Emeka)
   - pedestrians routed along the expressway (Emeka)
   - repeated names pick one place without saying so ("Railside" finds Railside Primary School No. 9, Funmi and Dayo)

## Not problems (checked)
- **"Coconut Beach is outside the built districts"** (Dayo): his `look` points were in the sea, south of the district.
- **"Home can't be a fisherman's hut"** (Dayo): `home N` gives ordinary houses first; the huts are listed by `look`.
- **"Bale Market is shut today"** (Funmi): it opens Monday, Wednesday and Friday; the tool has no days.
- **The far-house count** went from 116 to 120: the Border adds 8 houses 45–46.5 m from a way, and Railside's rebuild removes 4.

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| The other 46 earlier trips | | | unchanged |
| Estate Club → Gidi Interchange | ride | 2,875 m / 7.0 min / ×1.55 | 3,069 m / 7.5 min / ×1.66 (through rebuilt Railside) |
| **Border Post → Checkpoint Mile (new)** | ride | — | **496 m / 1.2 min / ×1.00** |
| **Bush Paths → Checkpoint Mile (new)** | walk | — | **681 m / 8.2 min / ×1.25** |
| **Heritage Strip → Coconut Beach (new)** | walk | — | **1,010 m / 12.1 min / ×1.16** |
| **Coconut Beach → Alade Electronics Market (new)** | ride | — | **1,636 m / 5.1 min / ×1.61** |
| **Checkpoint Mile → Gidi Interchange (new)** | ride | — | **2,278 m / 5.6 min / ×1.33** |

## City measures
| | Before | After |
|---|---|---|
| Districts built | 13 | 14 |
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| Houses over 45 m from a way (the tool's count) | 116 | 120 |
| `check_district.py` | pass (13) | pass (14) |
| Every district regenerates byte-identical | yes | yes (Railside rebuilt once with `keep_gateways`) |
| Lagos-isms logged | 14 isms × 15 areas | 14 isms × 16 areas |
