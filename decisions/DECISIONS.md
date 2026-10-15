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
- **Layout v2 at 1:4** (15 Oct). A fictional Lagos at one even scale, about 19.6 × 9.3 km. Each district sits where its inspiration really is; coasts and borders drawn fresh. See `docs/LAYOUT-V2.md`.
- **New districts:**
  - **The Airport,** where the real airport sits.
  - **Saba** (the owner's name), the Yaba/Akoka district, with **Lagoon University** on the lagoon.
- **Old Island is a true island,** with Gidi's versions of Third Mainland (the Long Bridge), Carter (Channel Bridge), Eko (Wharf Bridge) and the Lekki–Ikoyi Link (Cable Bridge, tolled). Banana Island sits off the Heights on a causeway.
- **Regenerate, don't move the old frozen Food Gate block.** The new map leads. The pilot's value lives in the generator rules; the old file is kept as a record.
- **One shared generator, one profile per district, run in parallel.** Not 17 separate generators.
- **The research must be detailed:** "look at everything in the data". Every district has a deep study (`docs/DEEP-STUDY.md`, `docs/studies/`).
- **Hand-place, not tune.** The generator gives the base; then exact hand placement and clean-up through hand files (`web/hand/<id>.json`).
- **Freeze everything** once a district is built, so any spot can be quizzed (`scripts/whats_here.py`). The map must come out the same every time.
- **Account for every square metre:** carriageway, gutter, walkway, building line, declared encroachment. Furniture never stands on the road; decks are decks. Road widths: `scripts/cross_sections.py`.
- **Markets spill onto the road:** traders take the carriageway, with a lane kept clear.

## Data and research
- **Google: study yes, lift no.** Studying Lagos with Google (Earth, Maps, Street View, Open Buildings) is fair game. Never copy Google's imagery or geometry into Gidi. Numbers only.
- **Never fetch:** Pinterest, Nominatim, Overpass. Never read or use the `gta5` folder. Mapillary: no access.
- **Look first:** every look decision comes from reference images the owner recognises by place (`~/Real-world/research/refs/REVIEW.md`).
- **Keep a delete-later list** of downloaded data (`docs/DATA-SOURCES.md`).

## How to work
- **Git:** never push to main; branches and PRs. Self-merge is fine when the checks or living test pass. Docs-only PRs can merge directly.
- **Writing:** plain words for a designer, honest critique, one recommendation. Look at what you make before showing it.
- **Hold-offs:** don't publish to the live artifact link (a different account). Don't start Unreal work until the owner says go.
- **Cost:** use cheaper models where possible (Pro plan).
