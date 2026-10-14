# City living test, 14 Oct 2026 (ninth run): the Heights v3

There are two states:
- **Before:** `main` at commit `a679778` (the Heights v2).
- **After:** this branch: the golf course, bigger Ikoyi houses in five architectural styles, and a floating street tied in.

Only the Heights changed; the other eleven districts regenerate byte-identical. One agent ran: **Kunle**, a driver and weekend caddie in the Heights.

## How life feels (short version)
- **The golf club** is a short walk from every side: 4.7–5.5 minutes from points west, east and north of it, 7.8 minutes from the south.
- **Crossing past the course:** west to east is 10 minutes on foot, north to south 8.4.
- **Kunle's everyday places:** from his house a church is 4.7 minutes away, a school 5.7 and a chemist 5.9.
- **From the golf club:** the Gold Island is 7.2 minutes and Pearl Towers 9.5.
- **Okadas:** a ride to the golf club still means 700–800 m on foot inside the ban. That's on purpose ("nobody goes to the Heights by okada").

## Verified problems, and what was fixed
1. **Fixed (generator): a 78 m street floated free** where the Gold Island's plot cut it off (6256,4985). A floating street is now tied to the nearest way by a short link when the link is clear of buildings, and is dropped otherwise. No other district had one, so none changed.

## Not problems (checked)
- **"No clubhouse"** (Kunle looked 100 m away): the clubhouse is at the course's east end; `look 5800 5000 80` lists it.
- **"No gate"**: the course is walled, with an opening where its access road leaves; it has no gatehouse, like the Palace. The pin is at the opening.
- **"Mosque 14 minutes"**: the rule is any place of worship within 10 minutes, and his church is 4.7.
- **"The clinic is ×4.96 for 164 m"**: the clinic takes over a house inside a walled compound, and the walk goes round the walls. Every Heights home passes the 10-minute check in the bake.
- **Kunle broke a rule:** he read a saved output file for two coordinates. Those two inputs are discounted; everything else above came from the tool.

## Standard trips
| Trip | Mode | Before (v2) | After (v3) |
|---|---|---|---|
| The 37 trips outside the Heights | | | unchanged (Island Motor Park → Mile Market by 1 m) |
| Pearl Towers → Club Strip | walk | 495 m / 5.9 min / ×1.46 | 626 m / 7.5 min / ×1.33 (the towers moved along the drive) |
| The Gold Island → Pearl Towers | walk | 1,054 m / 12.6 min / ×1.45 | 1,060 m / 12.7 min / ×1.45 |
| Cable Bridge → Sunday Beach | walk | 1,605 m / 19.3 min / ×1.24 | unchanged |
| Pearl Towers → Cloth Market | walk | 1,070 m / 12.8 min / ×1.11 | 937 m / 11.2 min / ×1.13 |
| Club Strip → Gidi Interchange | ride | 5,826 m / 20.7 min / ×1.39 | unchanged |

## City measures
| | Before | After |
|---|---|---|
| Everyday places within 10 min, every district | 100% | 100% |
| `check_district.py` | pass (12) | pass (12) |
| Every district regenerates byte-identical | yes | yes |
