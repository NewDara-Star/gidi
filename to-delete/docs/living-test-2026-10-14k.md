# City living test, 15 Oct 2026 (eleventh run): Old Shore

There are two states:
- **Before:** `main` at commit `cf613f8` (thirteen districts).
- **After:** this branch: Old Shore, built in parallel with the Border.

The other thirteen districts regenerate byte-identical, so two agents ran:
- **New: Iya Sade,** a fish trader in Old Shore
- **Tunde** (okada)

## How life feels (short version)
- **The fish run works.** From the Shore Fish Market to Food Gate's Mile Market is an okada ride along Northern Road: 4.6 km in 12.5 minutes, 142 m of it on foot. To the Ladi Lane Parts Market is 14.5 minutes.
- **The old town is close-knit:**
  - From the Old Quarter, the Shore Palace is 2 minutes away on foot.
  - A chemist is 2.9, a school 3.4, a church 6.0 and a mosque 7.9.
  - The fish market is 10.7 minutes, the Ferry Jetty 9.1.
- **Into the city:** Hunter Roundabout → Gidi Interchange is 14.5 minutes by okada. On foot the city is over an hour away: Old Shore is a town apart, joined by one road.
- **The palace is safe ground.** `look` there says so.
- **The opening is intact:** Tunde's room → The steal is 1.9 minutes.

## Verified problems, and what was fixed
1. **Fixed (tools): every Old Shore home scored 0% for everyday places within 10 minutes.**
   - **Why:** the reach check kept only the city's biggest walking network, and Old Shore, with no built neighbour, was a network of its own.
   - **The fix:** it now keeps every sizeable network (200 junctions or more).
2. **Fixed (tools): Northern Road was cut between Food Gate and Old Shore.**
   - **Why:** the tools clipped arterials to 120 m round the built districts.
   - **The fix:** a stretch running between two built areas is now kept whole. Old Shore joins the city's network, and no other district's pins or standard trips change.
3. **Open, design:** Old Shore hangs off one road (Northern Road). The ferries are drawn but can't be used in the tools yet.

## Not problems (checked)
- **"The Ferry Jetty is outside the built districts"** (Tunde): the pin is at the jetty's far end, over the water.
- **"The hospital is 16.7 minutes away"** (Iya Sade): hospitals aren't in the 10-minute everyday check (school, place of worship, chemist).
- **"`home` can't pick an Old Quarter house"** (Iya Sade): `home` takes a district, not a quarter. A tool limitation.
- **"Inside a building at Hunter Roundabout"** (Iya Sade): that's the founder's statue on its island.

## Standard trips
| Trip | Mode | Before (main) | After |
|---|---|---|---|
| The 47 earlier trips | | | unchanged |
| **Old Quarter → Shore Fish Market (new)** | walk | — | **894 m / 10.7 min / ×1.51** |
| **Ferry Jetty → Hunter Roundabout (new)** | walk | — | **849 m / 10.2 min / ×1.07** |
| **Shore Fish Market → Mile Market (new)** | ride | — | **4,622 m / 12.5 min / ×1.19** |
| **Hunter Roundabout → Shore Palace (new)** | walk | — | **697 m / 8.4 min / ×1.40** |

## City measures
| | Before | After |
|---|---|---|
| Everyday places within 10 min, every district | 100% | 100% |
| Walking islands inside the built districts | 0 | 0 |
| `check_district.py` | pass (13) | pass (14) |
| Every district regenerates byte-identical | yes | yes |
