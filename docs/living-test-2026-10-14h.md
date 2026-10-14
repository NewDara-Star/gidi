# City living test, 14 Oct 2026 (eighth run): the Heights v2

There are two states:
- **Before:** `main` at commit `47b75ef` (the Heights v1).
- **After:** this branch.

**What changed:** only the Heights. It now has three things v1 didn't:
- a Victoria Island side: an office-and-hotel grid with no compound walls, south of Waterfront Drive
- an Ikoyi side north of the drive
- shacks, bars and horse shelters on Sunday Beach

The other eleven districts regenerate byte-identical, so this run used the three agents who use the Heights:
- **Kunle,** a driver in the Heights
- **Bisi,** next door on Old Island
- **Tunde,** an okada rider into the Heights

## How life feels (short version)
- **The two sides read differently on foot:**
  - Kunle's `look` on the north side found houses, boys' quarters, gatehouses and generators, and no offices.
  - On the south side he found office and hotel blocks, the three towers, and no gatehouses.
- **The Ikoyi side is still close-knit:** from a north-side house, a mosque, a school and a church are all within 6 minutes, and the Gold Island is 4.4 minutes away.
- **Sunday Beach** is 9 minutes from the Club Strip and 18 minutes from the Cloth Market (Bisi).
- **The okada picture is unchanged:**
  - From the boss's park, a Heights run is 18–22 minutes, then 470–870 m on foot to the door.
  - The beach is the farthest drop, 865 m from the nearest legal road.
- **The opening is intact:** Tunde's room → The steal is 1.9 minutes.

## Verified problems, and what was fixed
1. **Fixed (generator):** walls round plots on the VI side.
   - **What was wrong:** the quarter was cut to the district's outline, but the edge roads bend up to 16 m outside it, so plots facing them counted as Ikoyi. The first row of plots on Waterfront Drive was tested only 2 m in.
   - **The fix:** the quarter now reaches the edge roads, and a plot is tested 15 m in. No compound wall is left south of the drive.
2. **Open, carried over:** the Heights and Old Island are both okada-banned, so the beach, the Club Strip and the Gold Island are 470–870 m on foot from a legal road. This is a story-map question.

## Not problems (checked)
- **The sand isn't walkable** (Kunle): the shacks face the shore road and are reached from it; nobody walks the open sand on the map's network.
- **"Sunday Beach is outside the built districts"** (Bisi, Tunde): the beach lies beyond the shore road, outside the district's outline, as the stilt village does for Water Town.
- **The thin office grid** (Kunle, Bisi): real Victoria Island mixes homes with offices too. The VI side has 59 office or hotel blocks among its houses.
- **The island at 6521,5111:** a sketch street of the unbuilt Frontier.
- **The chemist 9.9 minutes from Kunle's house:** within the 10-minute rule.

## Standard trips
| Trip | Mode | Before (v1) | After (v2) |
|---|---|---|---|
| The 37 trips outside the Heights | | | unchanged (Island Motor Park → Mile Market by 1 m) |
| Pearl Towers → Club Strip | walk | 427 m / 5.1 min / ×1.33 | 495 m / 5.9 min / ×1.46 |
| The Gold Island → Pearl Towers | walk | 912 m / 10.9 min / ×1.30 | 1,054 m / 12.6 min / ×1.45 |
| Cable Bridge → Sunday Beach | walk | 1,247 m / 15.0 min / ×1.06 | 1,605 m / 19.3 min / ×1.24 (the beach pin is now on a bar on the sand) |
| Pearl Towers → Cloth Market | walk | 1,090 m / 13.1 min / ×1.11 | 1,070 m / 12.8 min / ×1.11 |
| Club Strip → Gidi Interchange | ride | 5,742 m / 20.5 min / ×1.37 | 5,826 m / 20.7 min / ×1.39 |

## City measures
| | Before | After |
|---|---|---|
| Everyday places within 10 min, every district | 100% | 100% |
| `check_district.py` | pass (12) | pass (12) |
| Every district regenerates byte-identical | yes | yes |
