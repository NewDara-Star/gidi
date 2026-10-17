# Decisions (the owner's; newest first)

## The world
- **The story: Tunde's** (15 Oct 2026). The owner's confirmed story points live in `decisions/story/acts-2-3-draft.md`:
  - oja is weed, carried as cargo
  - the boss's 360 debt and the company bike
  - "how did you not know how your bike got stolen?"
  - freeing other boys from the same trap
  - the standoff ending

  Act 1 is the first build target, and the characters get written next.
- **Open world first; narrative optional** (15 Oct 2026). "The entire world right now feels more placeholder and open world for me than having a set narrative." Districts are defined by what a player can do and meet there. The world comes first and is built to stand on its own; Tunde's story is layered on it. Don't push plot or characters beyond what the owner has confirmed.
- **Gidi is our city.** Inspired by Lagos but our own. Data is a starting point; the owner's vision and the game's needs win.
- **Invented names only.** No real Lagos names or geometry in the game; shapes are drawn fresh, never traced.
- **Safe ground:** churches, mosques, schools, hospitals, clinics and places flagged `safe` are never crime sites. Sacred traditions are never criminal.

## The map
- **If it's in the 3D, it's in the 2D** (owner, 16 Oct 2026). The map data describes everything that takes up ground: roads, plots, houses, walls, furniture. The 3D only dresses it: windows, roofs, paint, wear. It never places things of its own. Compound walls moved into the data (`scripts/compounds.py`); balconies, canopies, trees and parked vehicles follow the same way.
- **Hand-making happens on the drawing board** (16 Oct). A clean plan of the city to scale where everything can be checked, moved, resized, reshaped, added and deleted (`docs/BOARD.md`). Edits save as hand edits; "bake the board" makes them real.
- **The browser 3D is a quick preview; the full scene is for Unreal** (owner, 16 Oct): "the only reason I want a 3d view is to quickly see what the world will look like... speed is important." Light tiles only.
- **The map is never final** (owner, 16 Oct). Gidi is tweaked until the game ships. Unreal will be one more view of the data, rebuilt by a re-runnable importer (`docs/UNREAL-PORT-PLAN.md`).
- **Layout v2 at 1:4** (15 Oct). A fictional Lagos at one even scale, about 19.6 × 9.3 km. Each district sits where its inspiration really is; coasts and borders drawn fresh. See `docs/LAYOUT-V2.md`.
- **New districts:**
  - **The Airport,** where the real airport sits.
  - **Saba** (the owner's name), the Yaba/Akoka district, with **Lagoon University** on the lagoon.
- **Old Island is a true island,** with Gidi's versions of Third Mainland (the Long Bridge), Carter (Channel Bridge), Eko (Wharf Bridge) and the Lekki–Ikoyi Link (Cable Bridge, tolled). The Gold Island (after Banana Island) sits off the Heights on the Crescent Causeway.
- **Regenerate, don't move the old frozen Food Gate block.** The new map leads. The pilot's value lives in the generator rules; the old file is kept as a record.
- **One shared generator, one profile per district, run in parallel.** Not 17 separate generators.
- **The research must be detailed:** "look at everything in the data". Every district has a deep study (`docs/DEEP-STUDY.md`, `docs/studies/`).
- **The Reach stands in Parade Square, Old Island** (16 Oct). The Reach is the kit's sculpture after the owner's own artwork: a woman reaching out to an Eyo-style masquerade, about 14 m across. It stands at the centre of Parade Square, Gidi's great civic square (after Tafawa Balewa Square), with horse riders at the square's gates.
- **Monuments are placed by hand** (16 Oct). The kit's pieces (`blender/gidi_kit/monuments.py`, `landmarks.py`) are placed with the `add monument` hand edit. The plan is in `docs/hand/borrowed-lagos.md`. A district with any hand-placed monument keeps only those.
- **Claude decides when the owner says so** (16 Oct). "Decide. I trust your judgment." On 16 Oct Claude:
  - merged Gidi v2 (PR #54)
  - renamed **Pedro Print Row to Press Row** and **Daleko Grain Yard to Gari Yard** (both real Lagos names)
  - kept **Ladi Lane** (invented; a nod to Ladipo, not a copy) and **National Bowl**
  - accepted all 23 items of the Maze and Hub list (`docs/hand/maze-hub-lagos.md`)

  Decisions made this way are recorded here like any other, and the owner can reverse any of them.
- **Know when to stop generating; then hand-make Gidi** (16 Oct). "It's important to know when to stop generating and start hand making Gidi, including checking out what makes Lagos unmistakably Lagos and working with them on the map... so we are not in generator hell."
  - **The stop line:** the 16 Oct build (all 17 districts from the deep studies, calibration pass 2, link roads) is the last generated base. Remaining check failures are fixed by hand, then every district is frozen. No more calibration passes or rebuilds.
  - **Then, district by district** (the Maze and the Hub first: Act 1 opens there):
    1. a list of what makes the place unmistakably Lagos, from the owner's photos, the deep study and `docs/LAGOS-ISMS.md`, checked by the owner
    2. placed by hand at exact spots through the hand files, labelled and noted
    3. the opening rebuilt and locked (the Maze and the Hub)
    4. freeze, show the owner, next district
- **The hand pass covers infrastructure and labels** (16 Oct). Hand placement must place infrastructure properly and label it properly: bus stops, traffic lights, street lights, roads, streets, everything. The hand files already add, move and delete buildings and furniture. They need:
  - road and street edits (add, move, delete, with the width class)
  - names and labels on everything
  - checks that nothing stands on a carriageway
- **Roads have surfaces; poorer areas have unpaved and marshy ones** (16 Oct). Some Lagos roads barely look like roads: marshy ground, grime and mud, a truck driving through (the owner's photo). Every road and street carries a surface:
  - tarred
  - worn tar (potholes, broken edges)
  - unpaved laterite or sand
  - mud (waterlogged, standing water, grime)

  Main roads stay tarred, even when broken. Mud goes to the poorer, wetter places: low ground, near water, back streets, the open fabric types.

  **Data caution:** Overture tags most of Lagos's local streets "unpaved" where it tags them at all (98% even in Yaba, which is mostly tarred), so the tags are checked against Street View and the owner's photos before they set anything.
- **Hand-place, not tune.** The generator gives the base; then exact hand placement and clean-up through hand files (`web/hand/<id>.json`).
- **Freeze everything** once a district is built, so any spot can be quizzed (`scripts/whats_here.py`). The map must come out the same every time.
- **Account for every square metre:** carriageway, gutter, walkway, building line, declared encroachment. Furniture never stands on the road; decks are decks. Road widths: `scripts/cross_sections.py`.
- **Markets spill onto the road:** traders take the carriageway, with a lane kept clear.
- **Everything is in the data** (17 Oct: "even the grain of sand on the ground... if everything is in the data, we'll be able to better place stuff"). Anything that stands somewhere is an object in the data, with its own position (parked cars, stalls, water tanks, signs, people's spots). What is too fine to place one by one (sand, grass, litter, stains) is in the data as painted areas with a kind, a density and a seed, so it can be seen, checked and changed on the board. The kit and Unreal only dress what the data says; they invent nothing.
- **Every road end is something** (17 Oct): a junction, a close with a turning space, a gate or house, the water, or the edge of the map. A road never just stops (`scripts/roadends.py`; the board flags loose ends).

## Data and research
- **Claude builds Gidi** (17 Oct: "you can build Gidi all by yourself... have an opinion. Build it based off the Lagos you see from the screenshots"). Claude makes the design calls from what it sees of Lagos; the owner reviews in Unreal and adds their own ideas after. Hundreds of Google Earth screenshots are fine (the owner accepted the risk under Google's terms); they stay in `~/Real-world/research/google/<district>/`, never in the repo, and are deleted when Gidi is done. Each district gets a short "what I changed and why".
- **Google: study yes, lift no.** Studying Lagos with Google (Earth, Maps, Street View, Open Buildings) is fair game. Never copy Google's imagery or geometry into Gidi. Numbers only.
- **Never fetch:** Pinterest, Nominatim, Overpass. Never read or use the `gta5` folder. Mapillary: no access.
- **Look first:** every look decision comes from reference images the owner recognises by place (`~/Real-world/research/refs/REVIEW.md`).
- **Keep a delete-later list** of downloaded data (`docs/DATA-SOURCES.md`).

## How to work
- **Git:** never push to main; branches and PRs. Self-merge is fine when the checks or living test pass. Docs-only PRs can merge directly.
- **Writing:** plain words for a designer, honest critique, one recommendation. Look at what you make before showing it.
- **Hold-offs:** don't publish to the live artifact link (a different account).
- **Unreal (go, 17 Oct):** the game is its own repo, `~/gidi-game`. The gidi data is the master copy: the importer rebuilds the city from it every time and nothing it makes is committed. Hand-made assets go through Git LFS, each listed in `ASSETS.md`.
- **Cost:** use cheaper models where possible (Pro plan).
