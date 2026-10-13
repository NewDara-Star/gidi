# City living test: Haiku agents live in Gidi and report how moving around feels

Run this after every district is merged, and after any fix to roads, paths, rail or canals. It finds what the
numeric checks (`check_district.py`) miss: places you can't reach, absurd detours, everything funnelling onto one road,
houses with no way in, and whether districts feel like one city.

## The tool
`python3 scripts/explore_city.py COMMAND` (from the repo root). It reads `web/gidi-data.js`, so **bake first**
(`python3 scripts/bake_web.py`). It covers every district that has generated buildings; `DISTRICTS=maze,hub` limits it.

| Command | What it does |
|---|---|
| `overview` | Districts, building counts by kind and storey, road lengths, parcels |
| `places` | Every landmark and civic place with district and X,Y |
| `home N` | Pick the N-th house and describe it |
| `look X Y [r]` | What's around a spot: buildings, nearest way, parcels, places, rail/canal distance |
| `walk FROM TO` | Shortest walk at 5 km/h: distance, minutes, detour ×, roads used, places passed, rail crossings, districts crossed |
| `ride FROM TO` | Same by okada at 25 km/h (no lanes, footpaths or footbridges) |
| `problems` | Houses >45 m from any way, network islands, dead ends |

FROM/TO is part of a place name or `X,Y` in metres (x east, y **south**).

## How to run it
1. Bake, then run `explore_city.py problems` and `overview` yourself first.
2. Launch **3 Haiku sub-agents in parallel** (model: haiku). Each gets one persona below and these rules:
   - explore only through the tool
   - don't edit files, and don't read the tool source or the data
   - 30–45 commands each
   - report under 450 words in two parts:
     - **A)** a first-person day, with real numbers
     - **B)** a numbered "what's wrong or missing" list, each item with the exact command, the numbers it showed, and coordinates. Nothing invented.
3. **Verify every B item yourself** before reporting it. Re-run the command and look at the geometry. Sort the items into:
   - **real problems** (fix them, or put them on the list for the next session)
   - **tool artefacts:** a pin in the middle of a big plot, edge roads clipped at the study border, a place that sits in an unbuilt district
4. Write `docs/living-test-<YYYY-MM-DD>.md`:
   - the three day-stories (shortened)
   - a table of standard trips (below) with metres, minutes and detour ×, compared with the last test
   - the verified problems, each with coordinates
   - what you fixed
5. Show the owner the short version: how life feels in plain words, then the real problems.

## Personas (rotate, and add one per new district)
- **Tunde, okada rider:**
  - his home is set by the opening, not by a district. Tunde's room is a back room in a compound in the Maze, under 3 minutes' walk from Ladi Lane Parts Market.
  - "The steal" is the stall at the market's near (east) end. The chase runs the length of the market and comes out on the west side. The boss's motor park is just across Idowu Street, in the Hub, and the boss sees the chase from there.
  - starts the day at the boss's motor park
  - passenger runs between the interchange, markets, rail station, stadium and hotel
  - one oja run from a market to the hotel
  - a viewing centre at night
  - looks at the knot under the flyover, the bus terminal, Ring Road, the station and the district borders
- **Mama Ronke, food seller, on foot:**
  - lives in the Hub and trades Under the Bridge
  - buys supplies in the market districts
  - visits a church or mosque, a chemist or clinic, her child's school and the bank
  - catches a bus at the interchange and a train at the station
  - tries the skywalks and footbridges, and walks home past the canal
- **A student or worker in the newest district:**
  - lives there and commutes to the other districts on foot and by okada
  - checks that their everyday places (school, worship, chemist, market, transport) are within reach
  - checks that the new district's edge roads and gateways actually lead somewhere
- **The chase (when the opening area is built):**
  - runs "The steal" through Ladi Lane Parts Market, and out of the market by different routes
  - counts the escape routes out of the market (it needs 3–4 or more): how many different first turns, and where the dead ends are
  - checks that the boss's end (the west side, toward the boss's motor park) can be reached, but is not the only way out

## Standard trips (track these every test)
| Trip | Mode | Why |
|---|---|---|
| Tunde's room → The steal | walk | His way to the opening scene (rule: under 3 min) |
| The steal → boss's motor park, through the market | walk | The opening chase, out of the market's far end to the boss's base |
| The steal → Gang Canal | walk | Opening chase, gang line |
| Maze house near the rail → Ladi Lane Parts Market | walk | Rail as a barrier |
| Gidi Interchange → Hub Rail Station | walk | Bus–rail transfer |
| Boss's motor park → Ladi Lane Parts Market | ride | Tunde's core run |
| Under the Bridge → Daleko Grain Yard | walk | Trader supply run |
| Newest district centre → Gidi Interchange | ride | Joins the city? |

## Targets (what "feels right" means)
- **Walks:** detour × under 1.6 for most walks under 1 km (real dense Lagos is roughly 1.3–1.6). Anything above 2 needs a reason, like a river or a highway.
- **Network:** no walking islands, apart from tiny pieces at the study border.
- **Houses:** none more than 45 m from a street, lane or path.
- **Everyday places:** every house has a chemist, a place of worship and a school within 10 minutes' walk.
- **Okada:** most cross-district rides take under 5 minutes.
- **Rail:** pedestrians can cross the rail every 150–250 m (informal crossings count). Vehicles cross at bridges and level crossings.
