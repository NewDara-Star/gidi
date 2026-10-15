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
| `home N [district]` | Pick the N-th house (in one district, e.g. `home 3 hub`) and describe it; the printed #id is not N |
| `look X Y [r]` | What's around a spot: buildings, nearest way, parcels, places, rail/canal distance |
| `walk FROM TO` | Shortest walk at 5 km/h: distance, minutes, detour ×, roads used, places passed, rail crossings, districts crossed |
| `ride FROM TO [--through]` | Same by okada at 25 km/h (no lanes, footpaths or footbridges). It goes round okada ban zones (the Capital, the Port, Old Island, the Heights); `--through` rides through anyway and reports the metres ridden inside the ban |
| `problems` | Houses >45 m from any way, network islands, dead ends |

FROM/TO is part of a place name or `X,Y` in metres (x east, y **south**).

## How to run it
1. Bake, then run `explore_city.py problems` and `overview` yourself first.
2. Launch **one Haiku sub-agent per persona, in parallel** (model: haiku). Each gets one persona below and these rules:
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
  - "The steal" is the stall at the market's near (east) end. The chase runs the length of the market and comes out at the west mouth. The boss sits at his post there, a canopy where his boys collect the park's levy, and sees the chase come out. His motor park is about 200 m further west, across Ring Road, in the Hub.
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
- **Sule, market porter, Food Gate (on foot and by okada):**
  - lives in Food Gate and works the night shift at Mile Market
  - carries loads to the lorry park, to Northern Bus Park over the Northern Road footbridges, and down to the Maze and the Hub
  - checks Freedom Ground, the Long Bridge checkpoint and the canoe jetty, and checks that Food Gate's edges lead somewhere
- **Bola, canoe paddler, Water Town (on foot, by okada, and by canoe):**
  - lives in a stilt house in the village under the Long Bridge, and drinks at the Stilt Bar
  - takes fish to the Canoe Jetty and timber from the Okobaba Sawmill
  - sells at Mile Market and goes into the Maze and the Hub by okada
  - checks that the boardwalks reach the shore roads, and that every hut has a school, a place of worship and a chemist within reach
- **Ngozi, phone trader, the Capital (on foot; okadas are banned there):**
  - rents a counter in a phone mall in Gadget Village and lives in a back house nearby
  - walks to the Allen Roundabout strip at night, the Shrine, the Secretariat on protest day, and the airport fence for pickups
  - goes to the Hub's interchange and Food Gate's bus park for goods, on foot or by okada from the Capital's edge
  - checks that the Capital's edge roads lead into the Estate, Railside, the Hub and Food Gate
- **Emeka, electronics trader, the Bazaar (on foot and by okada):**
  - has a lock-up in Alade Electronics Market and lives in a compound nearby
  - deals with the market's own court (Container Court), buys scrap at Rago Yard, and takes stock to Fair Wholesale Plazas
  - crosses the Coastal Expressway on foot, passes the barracks checkpoint, and rides to Jungle City, the Hub and the Capital (round its okada ban)
- **Chidi, clearing agent, the Port (on foot; okadas are banned there):**
  - clears containers at the Container Yard and lives in the old reserve (Old Reserve Avenue) or the streets by the creek
  - walks past the Tank Farm and the truck park, pays his way along Collector Row, eats at the Liverpool Under-Bridge night market, visits a client at Kiri Prison
  - takes an okada from the Port's edge to Water Town's sawmill, Jungle City and the Bazaar, and checks the expressway footbridges
- **Funmi, bread seller, Railside (on foot and by okada):**
  - lives by the railway and buys bread before dawn at Ayo Bakery Row
  - sells at the Ikotun-style Roundabout Market and the Bale Market, passes the cattle market, the waterworks, the landfill and the pipeline corridor
  - crosses the railway on foot and rides to the Hub's interchange, the Capital's edge and the Bazaar
- **Musa, gateman and night-delivery rider, the Estate (on foot and by okada):**
  - mans the Estate Gate on the main road from the Capital, and lives in a boys' quarters behind a big house
  - delivers at night to The Senator's House and the Estate Club, "deliveries to men you don't question"
  - walks the gated streets, counts the gates and gatehouses on his rounds, and checks that every street gate still lets people walk through
  - rides out to the Capital's edge (round its okada ban), the Hub's interchange and Railside's market
- **Bisi, cloth seller, Old Island (on foot; okadas are banned there):**
  - keeps a stall in the Cloth Market and lives in a Brazilian house in the old quarter
  - sends porters with head loads through the market's narrow lanes, and walks cash to Bank Row's towers on the waterfront
  - passes the palace (never a crime site) and the fenced square, and finds the Island Motor Park's buses
  - walks over the Wharf Bridge to the Port, and takes an okada from the island's edge over the Long Bridge to Water Town and Food Gate
  - checks that both bridges land on a road, and that the island's edge roads lead somewhere
- **Kunle, driver for a rich family, the Heights (on foot; okadas are banned there):**
  - drives for a family on the Gold Island and sleeps in a boys' quarters off a gated close
  - walks the closes past the gatehouses, runs errands to Pearl Towers and the Club Strip at night (valets and touts), and goes to Sunday Beach on his day off
  - walks over the Cable Bridge's toll plaza, and across to Old Island's Cloth Market and the Island Motor Park
  - checks that every gated close still lets him walk in, that the bridge lands on a road, and that the Heights' edge roads lead somewhere
- **Femi, site security on the Frontier (on foot and by okada; okadas ride freely here):**
  - guards an empty plot in the Disputed Plots and lives in a half-finished estate (New Estates)
  - rides the Peninsula Expressway through the Toll Plaza, takes refinery workers to the Refinery's gate, and checks the Eroding Beach on ocean-surge nights
  - rides west into the Heights (banned: where must he drop people?) and over the Cable Bridge
  - checks that the empty tracts still have ways through them, and that every home has its everyday places within reach
- **Iya Sade, fish trader, Old Shore (on foot, by okada and by ferry):**
  - buys the dawn catch at the Shore Fish Market (smoking racks, canoes at the market's jetty) and lives in a low old house in the Old Quarter
  - races fish to Food Gate's Mile Market by okada along Northern Road before it spoils, and meets the ferry at the Ferry Jetty
  - passes the Hunter Roundabout's statue and the garage, the Shore Palace (safe ground) and the Barge Yard
  - checks that her everyday places are within reach, and that Old Shore's roads lead into the city
- **The chase (the opening area is locked, see `web/locked.json`):**
  - runs "The steal" through Ladi Lane Parts Market, and out of the market by different routes
  - counts the escape routes out of the market (it needs 3–4 or more): how many different first turns, and where the dead ends are
  - checks that the boss's end (the west mouth, where the boss's post is) can be reached, but is not the only way out

## Standard trips (track these every test)
| Trip | Mode | Why |
|---|---|---|
| Tunde's room → The steal | walk | His way to the opening scene (rule: under 3 min) |
| The steal → boss's post | walk | The chase down the aisle to where the boss sits |
| The steal → boss's motor park, through the market | walk | The opening chase, out of the market's far end to the boss's base |
| The steal → Gang Canal | walk | Opening chase, gang line |
| Maze house near the rail → Ladi Lane Parts Market | walk | Rail as a barrier |
| Gidi Interchange → Hub Rail Station | walk | Bus–rail transfer |
| Boss's motor park → Ladi Lane Parts Market | ride | Tunde's core run |
| Under the Bridge → Daleko Grain Yard | walk | Trader supply run |
| Newest district centre → Gidi Interchange | ride | Joins the city? |
| Food Gate house (3100,3884) → Mile Market | walk | A porter's way to work |
| Mile Market → Ladi Lane Parts Market | ride | The produce run into the Maze |
| Stilt Village → Canoe Jetty | walk | A paddler's way to work, over the boardwalks |
| Stilt Village → Mile Market | walk | Water Town to the market district |
| Jungle City 3017,5225 → 3029,5181 | walk | The Coastal Expressway as a barrier |
| Gadget Village → Allen Roundabout Strip | walk | The Capital's trade to its night |
| Gadget Village → Gidi Interchange | walk | The Capital to the city's bus hub (no okadas in the Capital) |
| Ladi Lane Parts Market → Gadget Village | ride | Round the Capital's okada ban (and `--through`, metres inside) |
| Alade Electronics Market → Gidi Interchange | ride | The Bazaar to the city's bus hub |
| Bazaar house (1700,5600) → Alade Electronics Market | walk | A trader's way to work, across the expressway |
| Old Reserve Avenue → Container Yard | walk | A clearing agent's way to work in the Port |
| Container Yard → Gidi Interchange | ride | The oja's way from the port into the city (round the Port's okada ban) |
| Ayo Bakery Row → Ikotun-style Roundabout Market | walk | The dawn bread run |
| Ikotun-style Roundabout Market → Gidi Interchange | ride | Railside into the city's bus hub |
| Estate Gate → The Senator's House | walk | The gateman's round to the big house |
| Estate Club → Gidi Interchange | ride | The Estate into the city's bus hub (round the Capital's okada ban) |
| Estate Gate → Gadget Village | walk | The Estate's walk into the Capital |
| Brazilian Quarter → Cloth Market | walk | A cloth seller's way to work |
| Bank Row → The Palace | walk | Across the island, waterfront to palace |
| Cloth Market → Container Yard | walk | Over the Wharf Bridge to the Port |
| Cloth Market → Gidi Interchange | ride | The island into the city's bus hub (walk out of the ban, then the Long Bridge) |
| Island Motor Park → Mile Market | ride | Over the Long Bridge to the food market |
| Pearl Towers → Club Strip | walk | A night out in the Heights |
| The Gold Island → Pearl Towers | walk | A driver's errand out of the enclave |
| Cable Bridge → Sunday Beach | walk | The toll plaza to the beach, across the Heights |
| Pearl Towers → Cloth Market | walk | The Heights to Old Island's market |
| Club Strip → Gidi Interchange | ride | The Heights into the city's bus hub (walk out of two bans, then the Long Bridge) |
| New Estates → Disputed Plots | walk | A guard's way to his post |
| Toll Plaza → Refinery | ride | Refinery workers from the expressway |
| Eroding Beach → Toll Plaza | walk | From the sea to the road |
| Toll Plaza → Pearl Towers | walk | The Frontier into the Heights |
| Refinery → Gidi Interchange | ride | The convoy road into the city (round the bans) |
| Old Quarter → Shore Fish Market | walk | The fish trader's way to the dawn catch |
| Ferry Jetty → Hunter Roundabout | walk | Off the ferry to the garage |
| Shore Fish Market → Mile Market | ride | The fish run along Northern Road (freshness timer) |
| Hunter Roundabout → Shore Palace | walk | Across the old town |

## Targets (what "feels right" means)
- **Walks:** detour × under 1.6 for most walks under 1 km (real dense Lagos is roughly 1.3–1.6). Anything above 2 needs a reason, like a river or a highway.
- **Network:** no walking islands, apart from tiny pieces at the study border.
- **Houses:** none more than 45 m from a street, lane or path.
- **Everyday places:** every house has a chemist and a place of worship within 10 minutes' walk, and a school within 10 minutes. Up to 15 minutes to school is acceptable (owner, Oct 2026).
- **Okada:** most cross-district rides take under 5 minutes.
- **Rail:** pedestrians can cross the rail every 150–250 m (informal crossings count). Vehicles cross at bridges and level crossings.
