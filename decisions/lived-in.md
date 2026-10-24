# The lived-in layer: what every GTA does, and Gidi's plan

The owner asked on 24 Oct 2026 for research from public material on how GTA's worlds feel alive, across every game, and for a "lived-in layer" plan for Gidi. **A proposal, not decided.** It builds on `world-life.md` (rhythm, systems, moments, texture: *what* Gidi's life is) and the IDEAS entry "What makes Los Santos feel lived in" (23 Oct). This file is about *the machinery*: what records and rules make that life show up in the game.

Sources are modding wikis, the modders' file notes, developer interviews and press. Rockstar has published very little itself, so the file details are the community's reading of the game files. Nothing here comes from Rockstar's files or the gta5 folder; only the ideas are taken, never their data or text.

## The one lesson first

Obbe Vermeij, Rockstar North's technical director through GTA III to IV, told Edge that Leslie Benzies wanted every ped in GTA IV to have a home, a job and a daily drive to work. It was built, then cut: it cost too much CPU and memory, and it broke missions (a target stuck in traffic, on the subway or at home at the wrong time). His view was that players are happy with people who are "a little bit fake and shallow" ([arynews](https://arynews.tv/gta-4-was-going-to-be-a-much-more-realistic-game-but), [gtaboom](https://www.gtaboom.com/gta-4-almost-gave-every-npc-a-home-and-a-job-78a8), [gaminghq](https://gaminghq.eu/2026/08/18/gta-4-scrapped-realistic-npc-daily-life-system/)).

Every GTA since has felt alive the same way. **Life is staged near the player, from rules tied to places and the clock.** Nobody is simulated across the city. RDR2 went one step further, giving a named few real routines ([mein-mmo](https://mein-mmo.de/en/3-npcs-red-dead-redemption-2-einen-tag,286499)). A critic notes that even those routines live in the bubble around the player ([gamingbolt](https://gamingbolt.com/red-dead-redemption-2s-immersion-is-on-another-level-compared-to-cyberpunk-2077)).

**For Gidi:** the lived-in layer is records on the map: who is where, doing what, at what hour. The game stages them in a ring round the player. Only a short list of named people get a real day.

## What each game added

| Game | What it added to the lived-in feel |
|---|---|
| **III** (2001) | Peds and traffic spawned round the player, by zone. Traffic lights run three phases (north-south, east-west, people crossing), set by how the light model faces. A one-star wanted level for running a red light was tried and cut ([gamerant](https://gamerant.com/grand-theft-auto-3-annoying-wanted-level-feature-removed/)). Every mission is a script thread in `main.scm` ([grandtheftwiki](https://www.grandtheftwiki.com/Mission_Scripting_%28Overview%29)). |
| **Vice City** (2002) | `pedgrp.dat`: one line of 16 ped types per kind of zone (default, street, docks...), with separate night lines ([grandtheftwiki](https://www.grandtheftwiki.com/Pedgrp.dat/GTAVC)). The city's look changes with who is in it. |
| **San Andreas** (2004) | `popcycle.dat`: per zone type, weekday and weekend, 2-hour slots. Each slot gives the most people, the most cars, and the shares of dealers, gangs, cops and the rest, adding to 100 (the modders' notes on popcycle.dat; [nexusmods](https://www.nexusmods.com/gta4/mods/616)). **Ped attractors** (2D effects on models: seats, ATMs, shelters, dancers) pull passing peds into an action; a script "brain" can run on each ped that uses one ([opcode 0884](https://gtag.sannybuilder.com/opcode-database/opcode/0884/), [0621](https://gtag.sannybuilder.com/opcode-database/opcode/0621/), [074C](https://gtag.sannybuilder.com/opcode-database/opcode/074C/)). **Gang turf:** colour-shaded zones, with darker shading for more gang members. Kill a few rivals to start a three-wave war; rivals attack back later ([gta wiki](https://gta.fandom.com/wiki/Gangs_in_GTA_San_Andreas), [gtabase](https://gtabase.com/gta-san-andreas/gangs)). |
| **IV** (2008) | Euphoria (NaturalMotion): bodies react physically instead of playing set animations. Peds flee, fight back or call for help, and bystanders react to each other. Overheard phone calls, fender-bender arguments, umbrellas in the rain (Slate's 2008 review; [gta5-mods umbrellas](https://www.gta5-mods.com/scripts/umbrellas)). Per-ped schedules were built and cut (above). `popcycle` grows to cover scenarios and parked cars as well as peds and cars, and what kind of ped appears in which district ([nexusmods](https://www.nexusmods.com/gta4/mods/865)). |
| **V** (2013) | **Scenario points** (`.ymt`): hand-placed spots, each with an action, hours, a chance, a model set, and flags such as no-spawn. Points can be **chained** into routes, and **grouped**, so a group switches on or off with a mission or with Online (bank staff, Ammu-Nation, police station) ([gta5-mods comments](https://www.gta5-mods.com/maps/malibu-mansion-scenario), [CodeWalker](https://github.com/dexyfex/CodeWalker)). There were so many that the 256-type limit needed a patch for mods. **Ambient speech by context:** `GENERIC_HI`, `GENERIC_INSULT`, `GENERIC_HOWS_IT_GOING` and hundreds more, each with variants by sex, age and mood ([FiveM speech list](https://docs.fivem.net/docs/game-references/speeches/)). **Random events:** 57 (60 on later versions) at fixed spots. They start when the player comes near and are shown with a blue, red or blue-and-red dot. Most come back if ignored, and they pay in money, stats or a car ([grandtheftwiki](https://www.grandtheftwiki.com/Random_Events)). Strangers and Freaks are people with small stories, on the map under their name, some opening only after a condition ([grandtheftwiki](https://www.grandtheftwiki.com/Strangers_and_Freaks)). A real witness system exists in the code but is unused: seeing a crime is enough ([gtaboom](https://www.gtaboom.com/gta-5-gets-rdrs-witness-system-42f2)). Hand-built world: Garbut's team "considered the placement of every tree", working from Google, Street View and road trips ([gamingbolt](https://gamingbolt.com/grand-theft-auto-5s-world-v-is-absolutely-hand-crafted-features-unlimited-draw-distance), [MCV](https://mcvuk.com/?p=80936)). |
| **Online** | The same world, with scenario groups switched per mode, plus businesses players own, and rivals and raids against them. Not for Gidi now (`world-life.md`, Online). |
| **RDR2** (2018) | Named NPCs with scripted days: one leaves the saloon at 8 for a two-hour walk to the farm; another works the cattle yard 10:00 to 21:15. Witnesses must reach someone to report. Bounty and honour change how people treat you ([mein-mmo](https://mein-mmo.de/en/3-npcs-red-dead-redemption-2-einen-tag,286499), [dexerto](https://www.dexerto.fr/red-dead-redemption/que-se-passe-il-suivez-pnj-red-dead-redemption-2-pendant-journee-entiere-216145/)). |
| **VI** (due 19 Nov 2026) | Nothing confirmed in writing. The trailers show dense, mixed beach and boardwalk crowds, and social-media clips of strange NPC moments ([gtaintel](https://gtaintel.com/news/gta-6-npc-density-and-crowd-tech), [kotaku](https://kotaku.com/gta-6-beach-leak-has-fans-going-wild-over-crowd-density-best-leak-ive-ever-seen-2000727929)). One footage reading puts full detail within about 30 m of the camera, which is unconfirmed ([gamegpu](https://en.gamegpu.com/news/igry/rockstar-mozhet-ogranichit-rendering-npc-v-gta-6-distantsiej-30-metrov)). A Rockstar North patent (Hynd, Parr) gives each driver its own traits and has them read the road kind (slower in residential streets) and route round jams. It sets traffic density by road kind (main roads fuller than side streets), and names the old faults: NPCs fading in front of you, collisions seen too late, no plan for a roadblock ([VGC](https://www.videogameschronicle.com/news/gta6-npc-improvements-patent/)). A rumour says speech lines are tagged by whether a crime was seen or only heard, the hour and the weather (unconfirmed). |

## The machinery, in nine parts

These parts are shared by all the games and named here so Gidi can have each one.

1. **The mix: who is around, by place and hour.** A table per kind of area, by day type and time slot: how many people, how many vehicles, and the shares of each group. It decides the crowd before any single person exists. (SA/IV popcycle, VC pedgrp.)
2. **Spots: where someone does one thing.** Hand-placed, with an action, hours, a chance and who does it. They make a street feel lived in more than any crowd. (V scenario points, SA attractors.)
3. **Chains and switches.** Spots linked into a route (walk to the stall, queue, buy, leave), and spot groups switched on and off by the world's state: open or shut, a mission, a raid. (V chains and groups.)
4. **Talk by context.** Each person has a voice; the game asks for a context (greet, insult, bumped, saw a crash) and the voice says one of many lines for it. Two-person spots carry overheard conversations. (V speech contexts, IV phone calls.)
5. **Reactions.** What a person does when something happens near them: flee, fight, film, call someone, gather. Witnesses carry news. (IV Euphoria and bystanders, RDR2 witnesses.)
6. **Moments: small events at fixed spots.** They start when the player comes near, run their own script, and come back or not. (V random events.)
7. **Jobs: missions as scripted steps.** A launcher at a place and hour, with conditions, then steps: go, talk, drive, wait, fight, deliver. (Every GTA's mission scripts; V's Strangers and Freaks.)
8. **Standing per area.** Who holds a place, and how they treat you there. (SA turf, RDR2 honour.)
9. **Traffic by road.** Density and driving by road kind, each driver with its own traits. (The VI patent; every game's car mix.)

Behind all nine is **the bubble:** everything is staged inside a ring round the player and let go behind them. Only named people keep a day.

## Gidi's lived-in layer: the plan

All of it is records in the map, placed and set by hand on the board. Checks are programs. Nothing here is a generator rule, and nothing changes the frozen base. Each part says what exists already and what is proposed.

### 1. The district mix (`mix`, proposed: one per district, or per fabric type within it)
- **Day types:** weekday, Friday (Jumat), Saturday, Sunday, Sanitation Saturday (the last Saturday of the month, empty until 10). Then market days, set per market, and December.
- **2-hour slots,** 12 a day. Each slot has the most people per hectare of street, the most vehicles, and shares by **Lagos groups** that add to 100. The groups: traders, hawkers, artisans and apprentices, okada riders, keke and danfo crews (drivers, conductors, touts), office workers, students and pupils, the market women, area boys, police and LASTMA, the devout (Friday, Sunday), the party crowd (Saturday night), children, the old.
- **Vehicles in the same table:** okada, keke, danfo, molue, BRT, private cars, SUVs with drivers, lorries and tankers, carts (truck-pushers).
- **Examples to set by hand:** Mùṣá at 7 on a weekday is thick with okadas, traders opening and pupils. Victory Island at 9 has drivers waiting by SUVs. Ladipo market is full from 8 to 6 and empty at night apart from the guards. Any district at 23:00 is the beer parlour, the vigil and the danger hours.
- **A check (program):** shares add to 100; every district has a mix; the mix's busy hours agree with its places' `hours`.

- **District briefs:** `docs/lagos-study/LIVING.md` has a sheet for each of the 51 districts (people, wealth, day, work, vehicles, the busiest groups and hours) to seed each mix, and lists activities the spot list is missing.

### 2. Person spots (exists: `person_spot`, PR #267)
Done: `at`, `turn`, `activity` (68 Lagos activities), `hours`, `count`, `parent`, `place`. Proposed additions, each a small field:
- `chance` (0 to 1): not every spot is used every day, so the street changes from visit to visit.
- `days`: weekday, Friday and so on, from the day types above. The Jumat crowd and the Sunday-best walk only on their days.
- `group`: who does it, from the mix's groups, so the right person is cast.
- `named`: a named person's id. That person keeps a real day (below).
- `with`: the other spots that make one scene: two men at draughts, the mechanic and his apprentice, a quarrel and its crowd.

**Hand-placing them is the main job of the layer.** Aim for every place, every bus stop, every lock-up row and every junction to have its spots. They are placed street by street from the pictures, like the houses.

### 3. Chains and switches (proposed)
- **`route` (a chain):** spots in order with waits. Walk from the gate to the borehole, queue, fill, carry home. Board the danfo at the stop. The okada rank's turn-taking.
- **`state` (a switch):** named world states that turn spots and moments on or off. Each record lists the states it needs (`when`) or that stop it (`unless`). The first states:
  - `nepa_off`, by area and hour: generators on, shops dark, the cheer when light returns
  - `rain`, which brings umbrellas, shelter under eaves and flooded gutters
  - `fuel_scarce`, which brings queues and jerrycans
  - `raid`, when the task force comes and traders pack up and run
  - `owambe`, a street closed for a party
  - `market_day`
  - `story`, switched on by jobs

### 4. Talk (proposed: `voice` and `line` data, written for Gidi)
- **Voices:** language mix (Pidgin, Yoruba, Igbo, Hausa, English, and switching), age, group, temper.
- **Contexts,** Gidi's own list:
  - greet the player, insult, bumped into, near-miss with a car
  - haggle, sales calls: the hawker's shout, the conductor's route call ("Saba–Under Bridge–Ladi!")
  - saw a fight, saw a crash, "thief!"
  - NEPA took light, light is back, rain, heat, traffic
  - prayer, blessing, football results, betting wins and losses
- **Overheard talk:** a `with` scene can carry a short exchange, such as two traders on prices or a phone call about rent. The lines are written by Claude and read by Nigerian voice actors, the same as the radio (`world-life.md`).
- **The rumour idea:** tag lines by whether the speaker saw something or only heard about it. Carried into Gidi's news chain (part 5), the street retells what the player did.

### 5. Reactions: the Lagos crowd (proposed)
GTA's people mostly run. A Lagos crowd **gathers**, and that is the winning difference (IDEAS: where GTA falls short).
- **How each group reacts to the same event differs:** traders shutter, area boys come closer, the old scold, children watch, someone films.
- **The crowd judges:** a crash, a fight or a quarrel draws a ring of people. The ring takes sides and speaks (talk contexts).
- **"Thief!":** a chase that grows as it goes.
- **News moves by mouth:** a witness's report spreads along the spots near them. Who saw it, and where, decides what the police and the area boys know (RDR2's idea, which V left unused).
- **Safe ground stays:** churches, mosques, schools, hospitals and clinics are never crime sites (`world-life.md`).

### 6. Moments (proposed: `moment` record, at a fixed spot)
`at`, `radius` (starts when the player comes inside it), `hours`, `days`, `when`/`unless` states, `chance`, `repeat` (`once`, `daily`, `weekly`), `script` (its steps, as jobs use), and a reward or none. The first list is in `world-life.md` ("Moments"): the bus preacher, the medicine seller, change for the fare, the drivers' quarrel, the wedding convoy, the burial, the borehole driller, the crusade. GTA V had 57; Gidi's first district could carry 10.

### 7. Jobs: missions as scripted steps (proposed: `job` record)
- **The launcher:** a person or place, hours, days, the conditions (jobs done, standing, money), and how it shows: a name on the map, like Strangers and Freaks.
- **The steps,** from a short list:
  - `go_to`, `talk`, `wait`, `drive`, `follow`, `chase`
  - `deliver`, `collect`, `buy`, `sell`, `fight`, `escape`, `hide`
  - `switch_state` (turns a state on, such as `story` for a scene group)
  - `cutscene` (a comic panel, per the animation plan)
- **Each step has its fail cases.** A job's targets are named people placed by the job, never the open crowd. That is how GTA kept missions safe once the per-ped schedules were cut.
- **The story as a tour of the map:** jobs open the districts one by one (IDEAS, 15 Oct).

### 8. Standing per district (proposed)
Not gang wars. It is standing with the motor-park union, the area boys, the market women's association, the police and the community. It changes prices, the touts' manners, who helps you and who reports you. SA's shaded turf map becomes a standing map.

### 9. Traffic by road (partly in the map already: road `kind` and `width`)
- **Density by road kind and hour:** taken from the mix.
- **Driving traits by vehicle:**
  - okadas filter and ride against traffic
  - danfos stop anywhere for a fare
  - molues lean
  - SUVs with drivers push through
- **Fixed vehicle scenes as spots:** the broken-down danfo, the keke rank, the lorry unloading at Ladipo.

### The bubble and the named few
- **The bubble:** the game stages the mix, the spots and the moments in a ring round the player, then lets them go. Distance tiers follow the laptop budgets (Work / Play / Full): full detail close by, simple figures further out, nobody past the ring.
- **Named people:** a short list (say 20 per district, set by hand) keep a real day across their own spots. Mama Àdùkẹ́ opens her buka at 7, goes to market at 11 and closes at 9. The player can find them again; jobs and moments come from them.
- **No one else is simulated.** That is GTA IV's lesson.

## Order of work (proposed)
1. **The owner's yes** on the five new records (`mix`, `route`, `state`, `moment`, `job`), the person-spot fields, and standing. Each goes into MAP-FORMAT before any is built.
2. **Board:** the clock filter for spot hours (already on the to-do list), then a day-type filter. Then mix tables per district in a side panel.
3. **Mùṣá first:** its mix by hand, then spots street by street with the houses (hand pass), its named people, and its first 10 moments.
4. **Checks:**
   - every place has spots in its hours
   - mix shares add to 100
   - every spot's activity fits its parent (a `fry_food` spot needs a stall or a frontage)
   - every moment's states exist
5. **In Unreal, when the owner says go:** City Sample crowds read the mix and the spots (Mass AI for the far crowd, Smart Objects for the spots); the talk lines come after.

## What Gidi does not take
- Rockstar's files, data, scripts, speech lines or names. Only the ideas, from public writing. The gta5 folder's port and `mirror.rar` stay unopened.
- City-wide schedules for everyone (IV's cut).
- People who only flee. Gidi's crowd gathers, judges and talks.

## Sources
- Vermeij and GTA IV's cut schedules: [arynews](https://arynews.tv/gta-4-was-going-to-be-a-much-more-realistic-game-but), [gtaboom](https://www.gtaboom.com/gta-4-almost-gave-every-npc-a-home-and-a-job-78a8), [gaminghq](https://gaminghq.eu/2026/08/18/gta-4-scrapped-realistic-npc-daily-life-system/), [thehooknews](https://www.thehooknews.com/article/gta-4-npc-system-proved-too-broken-to-keep); GTA III red-light star: [gamerant](https://gamerant.com/grand-theft-auto-3-annoying-wanted-level-feature-removed/)
- Population files: [grandtheftwiki pedgrp.dat (VC)](https://www.grandtheftwiki.com/Pedgrp.dat/GTAVC), [nexusmods GTA IV popcycle mods](https://www.nexusmods.com/gta4/mods/865), [616](https://www.nexusmods.com/gta4/mods/616), [OpenIV popgroups.ymt](https://openiv.com/bugs/view.php?id=628)
- SA attractors: [Sanny Builder opcode 0884](https://gtag.sannybuilder.com/opcode-database/opcode/0884/), [0621](https://gtag.sannybuilder.com/opcode-database/opcode/0621/), [074C](https://gtag.sannybuilder.com/opcode-database/opcode/074C/)
- SA turf: [GTA wiki](https://gta.fandom.com/wiki/Gangs_in_GTA_San_Andreas), [gtabase](https://gtabase.com/gta-san-andreas/gangs), [grandtheftwiki](https://www.grandtheftwiki.com/Gang_Warfare_in_GTA_San_Andreas)
- Mission scripts: [grandtheftwiki overview](https://www.grandtheftwiki.com/Mission_Scripting_%28Overview%29), [SCM language](https://www.grandtheftwiki.com/SCM_Language), [Create a Mission](https://www.grandtheftwiki.com/Create_a_Mission), [Sanny Builder forum](https://sannybuilder.com/forums/viewtopic.php?id=554)
- V scenarios: [gta5-mods (scenario timing, NO_SPAWN)](https://www.gta5-mods.com/maps/malibu-mansion-scenario), [CodeWalker](https://github.com/dexyfex/CodeWalker)
- V speech: [FiveM speech list](https://docs.fivem.net/docs/game-references/speeches/); random events: [grandtheftwiki](https://www.grandtheftwiki.com/Random_Events); [Strangers and Freaks](https://www.grandtheftwiki.com/Strangers_and_Freaks); witnesses: [gtaboom](https://www.gtaboom.com/gta-5-gets-rdrs-witness-system-42f2), [Crime Witness mod](https://www.gta5-mods.com/scripts/crime-witness)
- Garbut and the hand-built world: [gamingbolt](https://gamingbolt.com/grand-theft-auto-5s-world-v-is-absolutely-hand-crafted-features-unlimited-draw-distance), [MCV](https://mcvuk.com/?p=80936), [dualshockers](https://www.dualshockers.com/grand-theft-auto-vs-art-director-on-creating-los-santos-id-never-want-to-rebuild-a-city/)
- RDR2 routines: [mein-mmo](https://mein-mmo.de/en/3-npcs-red-dead-redemption-2-einen-tag,286499), [dexerto](https://www.dexerto.fr/red-dead-redemption/que-se-passe-il-suivez-pnj-red-dead-redemption-2-pendant-journee-entiere-216145/), [gamingbolt](https://gamingbolt.com/red-dead-redemption-2s-immersion-is-on-another-level-compared-to-cyberpunk-2077)
- VI: [VGC patent](https://www.videogameschronicle.com/news/gta6-npc-improvements-patent/), [gtaintel](https://gtaintel.com/news/gta-6-npc-density-and-crowd-tech), [kotaku](https://kotaku.com/gta-6-beach-leak-has-fans-going-wild-over-crowd-density-best-leak-ive-ever-seen-2000727929), [gamegpu](https://en.gamegpu.com/news/igry/rockstar-mozhet-ogranichit-rendering-npc-v-gta-6-distantsiej-30-metrov)
