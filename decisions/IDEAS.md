# Ideas (not decided; newest first)

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
