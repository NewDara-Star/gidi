# City living test, 15 Oct 2026 (twelfth run): all fifteen districts

Old Shore and the Border were built in parallel, on separate branches (living tests 14k and 14l). The Border was merged first. This run checks the city once both are combined: main at `a94e9ee` (the Border and the 3D kit) plus Old Shore.

## What was checked
- **Every district regenerates:** fourteen districts from the combined code come out byte-identical to main; Old Shore is the only new one.
- **`check_district.py`:** all fifteen pass.
- **Everyday places:** every home in all fifteen districts has a school, a place of worship and a chemist within 10 minutes (bake).
- **Safe ground:** 256 places, each with its plot, among them the Palace, the Shore Palace and the Heritage Strip.
- **Standard trips:** all 52 earlier trips are unchanged from main. Old Shore's four new trips:

| Trip | Mode | Result |
|---|---|---|
| Old Quarter → Shore Fish Market | walk | 877 m / 10.5 min / ×1.44 |
| Ferry Jetty → Hunter Roundabout | walk | 843 m / 10.1 min / ×1.06 |
| Shore Fish Market → Mile Market | ride | 4,553 m / 11.9 min / ×1.17 (104 m on foot) |
| Hunter Roundabout → Shore Palace | walk | 814 m / 9.8 min / ×1.28 |

These differ by a few metres from Old Shore's own test (14k): it was regenerated on the combined code.

## Fixed while combining
- **The Frontier's refinery ground drew black in the 2D map:** the 2D map had no colour for a refinery plot. It now uses the industrial colour.
- **Two footnotes shared a mark** in the Lagos-isms table (‖). Old Shore's became §.

## Open, carried over
- Okadas can't legally reach the Frontier (its only roads run through the Heights' ban).
- Old Shore hangs off one road (Northern Road); the ferries are drawn but the tools can't use them yet.
- The walking tool doesn't know the Border's checkpoints, so the shortest walk still uses the road.
- Badagry town and Epe are outside the local OSM extract, so the Border and Old Shore are studied on what is covered.
