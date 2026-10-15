# Building the Lagos-isms: what exists, what's missing, and the prompt

The "feel like Lagos" pass. All fifteen districts are built from measured patterns. Now the isms in `docs/LAGOS-ISMS.md` go into the city, partly by rule and partly by hand. The topography (`feature/terrain`, `web/terrain.json`) comes first, because floods depend on it.

## Audit (15 Oct 2026)
"Map" means the 2D generator and its data (`scripts/gen_fabric.py`, `web/gen-*.json`, `web/gidi-data.js`). "Kit" means the Blender kit (`blender/`), which draws the 3D city from that data.

| # | Ism | In the map | In the kit | Missing |
|---|---|---|---|---|
| 1 | Streets dead-ending at a canal or drain | partly (the Maze's canal) | — | dead ends placed at canals and big drains |
| 2 | Streets dead-ending at the rail | partly (Railside, the Maze) | — | more stubs at the rail, with worn crossings |
| 3 | Missing links | — | — | two dead ends a wall apart: a street cut by a wall |
| 4 | Buildings on drain banks | Water Town's stilts only | — | houses right on a canal or drain edge |
| 5 | Buildings in the road reserve | kiosks only | kiosks | shop extensions, canopies and kiosks inside the road's width |
| 6 | Markets spilling onto the carriageway | — | — | stalls, umbrellas and wares on the road at market fronts |
| 7 | Roads doing too many jobs | — | — | side streets every ~30 m on a main road, market on it, bus stops |
| 8 | Unfinished buildings | the Frontier (half-built houses) | half-built storeys, at each district's rate | done |
| 9 | Odd junctions | — | — | five-way junctions, acute merges, slip roads |
| 10 | Flood-prone low spots | — | wet roads and pothole water from the LGA's low-land share | real low spots from the terrain, flood zones, standing water |
| 11 | Pedestrians forced onto expressways | footbridges in a few places | — | bus stops on the expressway, worn paths along the hard shoulder, crossings through the median |
| 12 | Gates across streets | built (the Estate, the Heights) | gatehouses, barriers | done |
| 13 | One-way streets | — | — | a direction on streets at each district's rate (the map, the tools, signs) |
| 14 | Streets ahead of houses | built (the Frontier) | — | done |
| 15 | Open gutters | — | open drains, slabs, rubbish, green water | gutters in the map data (which side, covered or open, blocked stretches), plank and slab crossings at entrances |

Also in the kit already: road condition and potholes, refuse heaps, litter, poles and tangled wires, transformers, kerbs.

## How it should work
- **The map stays the master copy** (`docs/UNREAL-PORT-PLAN.md`). An ism lives in the data first; the kit and later Unreal only draw it.
- **By rule, then by hand:**
  - A new step, `scripts/isms.py`, runs after the generator. It places each ism at its measured rate where it fits, and writes it into the district data.
  - A hand file, `web/isms-edits.json`, lets the owner add, move or delete any one by hand. Hand edits always win.
- **Deterministic:** the same seed gives the same isms. A district's houses and streets only change where an ism needs them to (a missing link cuts a street; a market spill takes road space).
- **Safe ground:** no ism that brings crime or danger goes on safe ground. That includes churches, mosques, schools, hospitals, clinics, palaces and the Heritage Strip.
- **Checks and test:** `check_district.py` must still pass, with its rules extended where an ism breaks one on purpose. A short living test checks that the isms make life harder in the right places without cutting anyone off.

## The prompt (paste into a new session)
> Read README.md, docs/LAGOS-ISMS.md, docs/ISMS-BUILD.md, docs/LAGOS-LIGHT.md and docs/UNREAL-PORT-PLAN.md. Build the missing Lagos-isms into Gidi, following "How it should work" in docs/ISMS-BUILD.md.
>
> Order:
> 1. Gutters (15), with plank and slab crossings
> 2. Buildings in the road reserve (5) and markets on the carriageway (6)
> 3. The broken network: missing links (3), dead ends at canals and rail (1, 2), odd junctions (9)
> 4. Hostile expressways (11) and roads doing too many jobs (7)
> 5. One-way streets (13)
> 6. Floods (10) and buildings on drain banks (4), once `web/terrain.json` is merged
>
> For each one:
> - Put it in the map data first: `scripts/isms.py` after the generator, with the rates per district from LAGOS-ISMS.md, plus `web/isms-edits.json` for hand edits.
> - Draw it in the 2D map (`web/app.js`, `web/shell.html`) and the 3D view (`web/view3d.js`). Then have the Blender kit read it from the data instead of inventing it (gutters especially: `blender/generate.py` and `blender/city.py`).
> - Extend `check_district.py` where an ism breaks a rule on purpose.
> - Teach `scripts/explore_city.py` where it matters: a missing link really blocks a walk; a one-way street is one-way for a ride.
> - Look at the result in 2D and 3D before showing it.
>
> Work on a branch per group and open a PR per group. Don't push to main. Run a short living test with Haiku agents, one persona in the districts the group touches, and write docs/living-test-<date>.md.
>
> Use cheaper models: Sonnet for building, Haiku for living-test agents and checks. Keep to plain words in docs and PRs.
>
> Safe ground and the sacred list (README) always hold.
