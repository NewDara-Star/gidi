# Ideas (not decided; newest first)

- **Someone else building the same way** (30 Oct; owner shared a Bengaluru game's maker's posts: "Seee"). He keeps a
  second Unreal level where everything in his game has a plain twin: lanes as coloured lines with direction arrows,
  every tree, lamp and parked car a simple shape with its kind and id written over it, layers by kind, "Go to #id",
  edits saved back to the data. His reason: models cannot see a finished scene the way people do, so a labelled
  version lets the model and the person point at the same thing by id. The owner's view (30 Oct): Gidi already works
  this way, with everything in the map data by id and the board to see it, so no separate 3D twin ("if I'm making our
  own 3D, 3D... you get like extra work. We already have the idea of making everything on the map data"). The owner
  has messaged him.

- **What GTA's own files taught us** (27 Oct; owner: "it's not so much graphics and more like very, very tiny
  interactions written into code... carefully thought out one by one and layered on top of each other"). From
  studying GTA V's files from the inside (DECISIONS "Study other games from the inside"; the study with its evidence
  stays off the repos, `~/gidi-data/research/gta/GTA-STUDY.md`; nothing copied). In our words, as Gidi would do it:
  1. **Traffic and people exist only near the player.** They are made just out of sight ahead and quietly removed
     behind, from a fixed pool; far away they use cheap physics, and very far traffic is only moving lights. The city
     feels full on a laptop because only a small ring of it is ever alive.
  2. **Who is on the street is a timetable** per kind of area, per two-hour slot, weekdays and weekends apart: how
     many people and cars, and which kinds. The owner's picture: school closes at 3, on Fridays at 1:30, and at that
     hour the street fills with children in uniform. Gidi's version: a timetable record per area type (market,
     school street, estate, motor park, waterfront), written from Lagos life.
  3. **Who can appear** is a named mix per area (the Mùṣá mix: hawkers, okada riders, mechanics, market women...),
     for people, vehicles and the props they carry.
  4. **Life is hundreds of small "someone does this here" spots**, each a short pre-made action (sit at the bus stop,
     fry akara, sweep the shop front, argue with the conductor), with conditions (rain, hour, rich or poor area) and
     chains (walk from the kiosk to the gate). Researched from Lagos one by one and scattered over the map, each
     running on its own: together they read as life. Gidi has the `person_spot` record for this; none placed yet.
  5. **People react, Lagos style**: a list of things people notice (bad driving, a crash, a fight, a bursting tyre)
     and how each kind of person answers: insults, "you dey craze?", crowds gathering, a mob, people filming.
  6. **Roads carry driving rules** placed by hand along every road: lanes each way, one-way, speed, how busy, what may
     use it, turns not allowed. AI cars follow these like rails. Gidi's road centrelines are the start; the rules go
     on them in the finishing pass.
  7. **Junction rules**: who runs each junction (lights, a warden, police, nobody) and how traffic flows there.
  8. **Small moments wake only near the player** (a breakdown, a preacher on the bus, a street fight), rate-limited.
  9. **Sound zones**: each area's sound by hour and weather, plus speakers (a music shop, a church, a generator).
  10. **Crime is seen by witnesses**, who report it; who responds depends on the area (traffic officers, checkpoints,
      area boys, a mob).
  11. **Local light and air**: the look of each hour and weather, dust, haze, flies by the market.
  12. **Driving feel in three layers kept apart**: each vehicle's own sheet (a danfo top-heavy, a keke that tips, an
      okada that leans); the input layer, with a wheel mode that turns the steering help off; helpers you can turn
      down. Then tune it on the owner's wheel until it feels right (the owner prefers Forza's feel to GTA's).
  13. **Parked-car spawners**: "a keke usually waits here, 6am to 10pm", and places where nothing parks.
  14. **Hard budgets**: a fixed number of cars, people and objects, decided for the laptop before crowds are built.
  15. **Few bodies, many outfits**: variety from clothes and colours, not from many models.
  **When** (owner, 27 Oct): in the finishing passes after every district is at the working bar (lanes, timetables,
  activities brushed on the map), step by step over years, not rushed. Builds on "The lived-in layer" below.
- **Gidi City hour to hour, and the pilot** (lagos-life-designer's research, 27 Oct, checked as noted there:
  docs/gidi-city-research.md). Its proposals, for the owner to take, change or drop: start friends-only, voice through
  the PS5 or Steam party; meet at "the joint" (a buka or beer parlour with a table and a chalkboard), three or four
  short rounds, a danfo ride between them; Lagos moments made by the city, never by a player, 2-4 an hour. The pilot:
  Ludo, then Whot!, at one table (Ayò, draughts and chess share its code: about a month for all five); the first
  slice "Friday night at the joint" with the owner, their brother and a friend on PC. Chess as a game to watch, a
  children's club on a stilt veranda in Makoro (Gidi's own, never the real charity). Gameplay Football: code free to
  reuse, its animations' licence unknown, months to port; read it and build a 2v2 from scratch. Faces through
  MetaHuman from an iPhone. Not to attempt early: strangers, open voice, real money, ranked play, more than ~8 players.
- **Run on R2, like FC** (owner, 27 Oct, playing GTA: "I really like the fact that I'm using R2 to run. Like, the effort
  is given"; GTA's tap-X-to-sprint does not feel natural to someone who mostly plays FC). Claude's view, to research
  before deciding: hold R2 to run on foot by default, so R2 means "go faster" on foot and in a vehicle alike (it is the
  accelerator in GTA's cars); a "classic" preset with GTA's tap-to-sprint; every button remappable, and run as hold or
  toggle, which the accessibility guidelines ask for anyway (no repeated tapping). FC is huge in Nigeria, so many of
  Gidi's players may share the owner's habit. Owed: how the big open-world games map run (GTA, RDR2, Cyberpunk,
  Spider-Man, Sleeping Dogs) and what R2 then does on foot (aim is usually L2/R2).
- **Our own Lagos motion from video, and AI video** (owner, 23 Oct). Motion2MixamoRig (github.com/MaxLiu22/Motion2MixamoRig, code Apache-2.0, experimental): a video of one person, whole body in frame, becomes motion on a Mixamo character (.glb for Blender/Unreal); Blender add-on tested on Apple Silicon, slow but fine on CPU (3-15 min per 30 s clip). Fills the gap Mixamo's library leaves: Lagos-only moves (basin on the head, conductor hanging off the door, frying akara, bargaining, climbing on an okada), filmed by the owner or friends who agree, never strangers' clips. **Catch:** it needs SMPL-X, non-commercial by default (a commercial licence is a separate deal), and the GVHMR weights have their own licence: use it for study and prototypes (person spots), then licence it or redo final animations with a sale-cleared tool before shipping. To set up (needs the owner's OK): repo + Python packages; about 5 GB of weights on first run; the SMPL-X file (owner signs up on the SMPL-X site); a Mixamo FBX from the owner's Adobe account. Mixamo itself: free library, retarget onto City Sample/MetaHuman in Unreal; usable in a shipped game, raw files not shared.
  - **AI video** (Claude's view, owner agreed in talk): good for previs/animatics, screens inside the world (shop TVs, Nollywood on a parlour TV, junction ads), motion reference and pitch mood; not for final cutscenes (faces and props drift between shots, look won't match the game, no fine control, rights and Steam's AI disclosure, players' reaction). Plan stays: comic panels first, then cutscenes in the engine with our models, City Sample people and MetaHuman faces from the owner's voice takes. Paid video tools: confirm model and cost first.
- **The lived-in layer** (owner asked, 24 Oct): research across every GTA (III to VI, plus RDR2) on how the world feels alive, and a plan in nine parts as map records: district mix by day type and 2-hour slot, person spots (+ chance, days, group, named, with), routes and world states, talk by context, the Lagos crowd that gathers, moments, jobs as scripted steps, standing per district, traffic by road. Life staged near the player; only a named few keep a real day (GTA IV's cut schedules). In full: `lived-in.md`.
- **What makes Los Santos feel lived in, and what Gidi takes from it** (owner asked, 23 Oct; web research, sources below). Already ours: study a real city in bulk, then mix it (Rockstar: 250,000+ photos, landmarks right but "placement screwy"); everything placed by hand ("every tree"); wear everywhere (chipped poles, grime that reads even in miniature). The gaps for Gidi, each one map records:
  - **Who lives where, by hour:** GTA's per-zone list of people and vehicles by time of day (`popcycle`). A district record could hold its mix: Mùṣá okadas, kekes, danfos, traders, apprentices; Victory Island SUVs and drivers waiting; joggers at dawn, the night crowd at the beer parlour.
  - **Person spots (scenario points):** hand-placed spots where someone does something (smoking outside a shop, chatting on a bench, the gardener). These make a street feel lived in more than any crowd. For Gidi: the BetGidi agent and the men watching the TV through the shutter, the akara fryer, the mechanic under a car, the tout at the danfo door, the gala seller in traffic. A record with place, activity and hours (already on the board's list).
  - **Vehicle scenes:** the broken-down danfo that never moves, the keke rank, okadas at the junction, a truck unloading at Ladipo.
  - **Brands everywhere:** 40-60 invented brands on walls, umbrellas, buses, kiosks, radio. First one: BetGidi (brand canvas, 23 Oct, https://claude.ai/artifact/59JAAyvyoG3KuFQ29jgNiy: violet, lime, coral; "Gidi no dey sleep", "Na your turn").
  - **Where GTA falls short and Gidi can win:** most buildings can't be entered, so they feel flat, and ordinary people mostly just run. Lagos frontages are open (lock-ups, stalls, verandas): a few steps inside each go far.
  - Sound, overheard talk, day/night and rain: see "Life in the streets" below.
  - Sources: Garbut interview (vortez.net), New Yorker "Idling in Los Santos" (allnightmenu.la), gtamods.com Popcycle.dat, GTAForums scenario list, weareopen.coop critique.
- **Life in Gidi** (16 Oct): what makes the world feel like it exists. Rhythm, systems (NEPA, fuel, go-slow), moments (the bus preacher), texture, bus stop names the Lagos way, invented brands, Bet Gidi, naira, a radio made for Gidi, life after the story, online later, face scans. In full: `world-life.md`.
- **Story as a tour of the map** (15 Oct). In GTA III, IV and V the story mostly walks the player through the city district by district. If Gidi ever gets a story, it can be layers of jobs and people that open the districts one by one.
  - GTA III: a revenge ladder through gangs.
  - GTA IV: the immigrant's lie of the dream.
  - GTA V: three crossing lives and heists.
- **What the new districts could offer** (placeholders, for the owner):
  - **The Airport:** arrivals touts, cargo and smuggling, rich people passing through, police at every gate.
  - **Saba:** students and young people, tech hubs in old houses, the junction under the flyover, nightlife.
  - **The Gold Island** (after Banana Island): the most expensive address, behind one gated causeway: a place to get into, someone's home, or a view across the water.

## Gidi's brand identity (owner, 19 Oct; refs in ~/gidi-data/research/refs/brand/, study only)
- Danfo yellow and black, a third colour sparingly (the red and blue of hand-painted lettering).
- Illustration: flat black silhouettes on yellow, rough printed texture, everyday street life (also the comic-panel cutscenes).
- Lettering: Danfo Basic (done, gidi-game Art/Fonts) for painted bodywork and titles; a brush secondary font like danfo
  window lettering (fat rounded capitals, white highlight and outline); wobbly hand lettering for posters, drawn one-off.
- A coat of arms for Gidi, designed fresh (Lagos's arms are reference only); options for the owner to choose.
- Gidi number plates (outline of Gidi, a slogan, district codes) on every vehicle the data places.
- Danfo backs as data: each danfo its own window slogan and pictograms, from an invented list.
- Proposed order: a one-page brand sheet; coat-of-arms options; the brush font; plates and slogans into the data and kit.
- **The main menu** (owner, 19 Oct, after God of War's): the menu items down one side in our Gidi lettering; the one you
  highlight lights up in colour, and the other side shows a Gidi monument or something only Gidi has (The Reach, the Marigold
  Screen, a danfo...), cycling. Refs: ~/gidi-data/research/refs/brand/identity (the owner's ÈKÓ poster: a black-and-white
  cut-out landmark on danfo yellow, pattern-filled letters, the stripes down the edge; a red-and-black line drawing of street
  life on yellow; a skyline of landmarks, stock, study only). Open: black and white or full colour.
- **Meshy's role** (owner, 19 Oct): complex sculptures, and a starting point when there's no obvious way into a build (learn
  from it, then build our own modular version). Vehicles and kit pieces are built part by part.
- **Gidi UI** (owner, 19 Oct): "something beautiful and unique, our own style": the illustration style, plus stickers, plus a
  legible but stylised font for the interfaces (custom, like the rest). The owner is collecting inspiration to send; wait
  for it before drawing. Montserrat's full family (OFL) is a candidate base for the UI face.
- **People** (owner, 19 Oct): first the hawker with the basin of drinks, built with MakeHuman in Blender (MPFB, CC0 assets) and judged in a render; then the full frame (refs/lagos-life 09, the motor park) and what it shows is missing; **then try MetaHuman** (Unreal), above all for animation: faces driven from a phone video (MetaHuman Animator), which suits the owner voice-acting the characters himself. If MakeHuman people don't hold up, MetaHuman replaces them.


## Life in the streets: what makes people stay (owner, 22 Oct)
The owner: "people randomly having like chatter conversations"; "beer parlour talk... somebody on the road looking at a newspaper... stupid football takes"; music; bus stop names. Lagos Life (browser, 2026) drew millions of players in its first days on curiosity alone, then had "nothing going on" (the owner played it). Curiosity brings people once; life and things to do keep them.
- **Overheard talk:** groups that argue as you pass: the newspaper stand (football, politics, prices), the beer parlour, the barber's, the bus queue, the market women, the mechanics. Short lines, many of them, in pidgin, Yoruba and English, picked by place and time (match day, fuel queue, rain, NEPA off).
- **Bus stops you hear before you see:** conductors calling the stops and routes from the danfo door, the stop's name on a painted sign or a wall; the same names on the map.
- **Sound and music:** radio from shops and buses, a station or two of our own music, generator hum, church and mosque, hawkers' calls.
- **Things going on:** jobs anyone in Lagos knows (conductor, okada, hawking, a levy run), checkpoints, the light going off, rain that floods the street, traffic that locks up.
- **Dense, not huge:** a small part of the city full of life beats a big empty one; the Underdeck is the first place to prove it, and short clips of it are how people hear about the game.

## Living in each district (24 Oct, research, awaiting the owner)
- **The okada map as a rule:** okadas banned in the inner councils (raids, seizures; they still run the back streets) and free in the outer ring, as in Lagos since 2022. Tunde's risk zone is the centre, his home ground the edge (`docs/lagos-study/LIVING.md`).
- **Four first mix templates:** the market, the dormitory suburb, the estate and the never-sleeps junction, each then set by hand per district.
- **18 more person activities** (bake_bread, carry_headload, run_press, smoke_fish, shuck_oysters, saw_timber, butcher_meat, test_speaker, collect_levy, play_chess, dj, spray_money, jog, study, mould_blocks, farm, queue_atm, cyber_work and others); each tied to a district in LIVING.md.

## Place names: echo names (22 Oct; the rule is decided, the 51 names await the owner)
The sound-alike rule below is now a decision (DECISIONS, "Invented names only"); what still waits is the owner's review of the names in `docs/lagos-study/roads/NAMES.md`.

The owner asked whether Gidi's places could just be parodies of the real names, since Gidi is Lagos made smaller. Invented names stay the rule. The proposal is **echo names**: built from Yoruba (or the place's own language) the way Lagos names are, close enough in sound or meaning that a Lagosian smiles and knows where they are, never a straight copy and never a cheap pun. Saba for Yaba is the model. Big landmarks get the clearest echo; quiet places get plain new names in the same style. Brands and businesses are always invented (Gidi's own). One name list for all 51 districts, made with the owner.

**The rule (owner, 22 Oct): sound-alike in the same language.** "Make the names sound similar. So if something is English, it should be English. Something is Yoruba, it should be Yoruba." Yaba → Saba, Computer Village → Gadget Village. A Lagosian should hear the real name in the Gidi one: the same rhythm and mostly the same sounds, with one or two changed. English names get English sound-alikes, Yoruba (and Awori, Egun) names get Yoruba ones that still sound like real Yoruba words or names, and mixed names keep the mix. A sound-alike may also have a decent meaning, but sound comes first; a name that only shares the meaning is out. It must never be the real name, a real nearby place, rude or a cheap shot. Old Gidi names stay only if they pass. Working drafts for all 51: `docs/lagos-study/roads/NAMES.md`, for the owner to review.

## A living test for the new map (24 Oct, from the old map's living tests)
- **Walk and ride the city between named places,** once a few districts join: cheap agents on foot, danfo, okada and keke, a standard trip list run after every change, each trip's length against its real one. On the old map this found what the numbers missed: places you can't reach, absurd detours, everything funnelling onto one road, houses with no way in, an okada ban that cut a district off. The lessons: `docs/OLD-MAP-LESSONS.md` ("Checking").

- **Distribution and the money** (26 Oct, owner shared a postmortem where $560k Steam gross became $73k take-home):
  the cuts are the store (30%), refunds, US withholding (30% on US sales when the seller's country has no US tax
  treaty; Nigeria has none, the UK has one), a publisher's share, local tax, partners; Unreal adds 5% only past
  $1M gross per game. Open: where the company sits (a treaty country cuts the withholding). Settled by the owner on
  26 Oct (DECISIONS.md): self-published, PS5 and Steam, digital only; players at home pay with dollar cards. To
  research with sources before choosing where the company sits.

- **Gidi Online: a shared city for connection** (owner, 26 Oct): many Nigerians abroad are lonely; next to the story,
  Gidi can be a place to meet friends, talk and do things together, as FC's Clubs is for the owner. Activities are the
  soul of a shared space and must be good enough to bring people back. The owner's examples (a wider idea, not the
  list): racing with people, free driving around the city to let off steam (as in Forza), football, basketball,
  tennis, table tennis. Your own face on your character (as FC's face scan was meant to be). For the map now: the
  courts, pitches, school grounds and race-worthy roads it holds are where these happen. Not decided; online play
  (servers, matchmaking, moderation) is a large cost to research before choosing.
- **Nigerians don't ask for refunds; they stop buying from you** (owner, 26 Oct): the first game has to earn trust.

## Gidi's look: an art style or plain realism? (owner asked, 27 Oct; not decided)
The owner likes Fortnite's look though it isn't realistic, and Rematch's. Claude's recommendation: **real Lagos, painted
light**: real sizes, real materials and all the grime (no toy look), but the light and colours chosen by us like a
painter's, a fixed colour list per district, a little simplification in the surfaces (Rematch's way), not photo-chasing.
Why: plain realism costs the most and ages fastest (GTA V now looks off: its hand-set orange sun and early-clipping
highlights, from its own files, `~/gidi-data/research/look/LOOK-STUDY.md`); a chosen look ages well and makes Gidi
recognisable in one frame. To decide by eye: one Mùṣá street rendered three ways when Unreal work resumes (map first).
Fortnite: not downloaded (owner, 27 Oct: "We can get our art style without it").

## Missions: the goal fixed, the way open (owner, 27 Oct; not decided)
More posts the owner shared, 28 Oct: players wanting "numerous ways to get to an outcome" in Rockstar missions after
Baldur's Gate 3, Rob Nelson reported as saying GTA 6 missions get more freedom (not checked), and a reply that RDR2's
missions are still fun on rails. Same point: fix the outcome, open the way.
The owner stopped playing GTA over one mission: a target flees on a bike and must be shot; ramming him with a car "did
nothing", and shooting from a moving car needed a steadiness that made it a chore. "You have to go through a certain
step to get a predetermined goal. You cannot take another step." They also note Red Dead pulls you into exploring while
GTA is mission-led, and that players ask for open worlds "with lots of 'side' stuff to complete" (a post the owner shared).
For Gidi: a mission states the outcome (he must not reach the bridge; the package must get to Oshodi by six) and accepts
any way the world allows: a car, a friend, a shortcut, a bribe, a crowd. Fail only on the outcome, never on the method.
Being checked in the files (NOW item 13): how GTA's mission scripts force the method (damage immunity flags on
targets, scripted chases, fail conditions), in Vice City Stories' script and, if the owner approves the download of a
script reader, GTA V's.
What the files showed (27 Oct; ~/gidi-data/research/gta/MISSION-METHOD.md and ~/gidi-data/research/psp/PSP-NOTES.md):
Vice City Stories forces the method often (a character made immune to cars in 37 of 59 story missions; a fleeing
dealer put on a vehicle and then made ram-proof; fail lines like "You used a gun."). GTA V mostly fails on outcomes
(747 fail lines; only 8 about the wrong way or time, none asking for a weapon); it shuts the way with chases on rails
("Chop": the rider ram-proof and never knocked off), invincible things the player would naturally attack, and "too
early" fails; it rewards a style with medals instead of failing the other ways. For Gidi: the outcome fails, never
the method; a rule, if any, is said up front; style earns a bonus, not a fail.
