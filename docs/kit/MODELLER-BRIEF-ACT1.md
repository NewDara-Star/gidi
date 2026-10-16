# Brief for the kit modeller: the Act 1 gaps

Copy everything below the line into the modeller's session.

---

You're building new pieces for the Gidi 3D kit in Blender: `blender/gidi_kit/`, driven by `blender/city.py`. Gidi is an invented city inspired by Lagos. The map data is already placed by hand: every piece below already has a position, a footprint or a point, and a kind in `web/gidi-data.js`. The kit just can't draw them yet. The full list, with notes, is in `docs/KIT-GAPS.md` under "New in the v2 layout".

**Rules**
- Work on a branch, never on main. Open a PR; self-merge when it builds.
- Follow the existing builders: buildings in `archetypes.py` (`def name(a, rng, collection=None)`), furniture in `street.py` and `roadside.py`, vehicles in `vehicles.py`, monuments in `monuments.py`. Register building kinds in `blender/gidi_kit/registry.py` (next to `'kiosk'`); furniture kinds are dispatched in `city.py`'s furniture loop (next to `f_['kind'] == 'transformer'`).
- Deterministic: use only the `rng` you're handed, never `random` or `hash()`. Same data, same model, every time.
- Low poly, stylised realism, game-ready: look at `vehicles.py`'s danfo and `monuments.py` for the level of detail.
- Worn, never new. Rusted zinc, faded paint, rain stains at the base of walls, bare blockwork, dust.
- Sacred places are never crime sites; don't put gang or crime props on churches, mosques, schools or clinics.
- Render a contact sheet of what you made (see `blender/new_kit_sheet.py`) and look at it before you open the PR. Put the sheet in the PR.

**Build these, in this order (the opening of the story happens here)**

1. **Face-me-I-face-you** (building kind `face-me`; Tunde's block in the Maze). One storey, about 22 × 9.5 m. A corridor down the middle with five rooms a side, a door at each end. Pitched rusted-zinc roof, low eaves, burglary bars on small windows. At the back: a shared toilet and bathroom block and a kitchen corner with soot on the wall. Washing lines across the yard, a bench and plastic chairs at the front door, a generator in a cage, jerrycans.
2. **The motor park office** (kind `office`; the boss's office in the Hub, the first cutscene). Dingy and makeshift: a converted 20 ft shipping container, or a zinc-walled shed on a block base. A hand-painted union sign above the door, a bench and a blue water drum outside, a padlock, a satellite dish. The interior must be modelled, because the cutscene is shot inside: a desk with a ledger, two plastic chairs and one office chair, a standing fan, a bare bulb, a peeling church calendar, a cash box, a small TV on a stool.
3. **Agbero** (furniture `agbero`): a standing man (from `people.py`) with a ticket book and a fan of notes folded lengthways between his fingers. Two or three poses.
4. **Buka** (kind `buka`; the Flyover Buka in the Maze): a lean-to kitchen against a wall. Big pots on coal and firewood, a glass food display, long benches and a table under a tarpaulin, plastic plates, a hand-painted name board.
5. **Wheelbarrow vendor, fruit seller, parking boy** (furniture `wheelbarrow vendor`, `fruit seller`, `parking boy`): a wheelbarrow of phone cases and chargers under an umbrella; a fruit tray on a folding table; a parking boy's plastic chair, ticket book and a reflective vest.
6. **Bread hawker** (furniture `bread hawker`): loaves in clear nylon, on a head tray and on a wheelbarrow, both versions.
7. **Police kiosk** (furniture `police kiosk`): a small red-and-white booth with a tiny window, beside a bus stop. A plastic chair outside.
8. **Rail market** (zone `rail market`, the Hub): traders' low tables and mats on the ballast right beside the rails, umbrellas, basins of goods. The tables must be easy to lift as one group (a train comes through).
9. **Task force truck** (furniture `task force truck`): a battered pickup in faded government colours with seized okadas piled in the back.
10. **Overhead direction sign** (furniture `overhead sign`): a green steel gantry across a main road, white text panels. Leave the text to `city.py`.
11. **Lock-up dressing for Ladi Lane** (the chase line): an open variant of the market lock-up. Shutter rolled up, goods stacked to the roof (engine parts, tyres, phone boxes, fabric bolts), a tarpaulin awning out over the aisle, crates and a trolley in front.

**Later (not needed for Act 1)**
- The Glasshouse mall (kind `mall`): a three-storey black-glass box with a car park in front.
- The airport terminal and control tower; the runway with its markings and lights.
- Campus buildings: lecture halls, hostels, a senate building.
- The Banana Island causeway gatehouse.
- The informal bus stop: a sign on a pole and a worn patch, for the side streets.

When you're done, list in the PR what you built and which kinds now draw.
