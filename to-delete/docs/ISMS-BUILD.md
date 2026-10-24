# Building the Lagos-isms: what exists, what's missing, and the prompt

The "feel like Lagos" pass. All fifteen districts are built from measured patterns. Now the isms in `docs/LAGOS-ISMS.md` go into the city, partly by rule and partly by hand. The topography (`feature/terrain`, `web/terrain.json`) comes first, because floods depend on it.

## Audit (15 Oct 2026)
"Map" means the 2D generator and its data (`scripts/gen_fabric.py`, `web/gen-*.json`, `web/gidi-data.js`). "Kit" means the Blender kit (`legacy/blender/`), which draws the 3D city from that data.

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
| 15 | Open gutters | built (15 Oct: `scripts/isms.py`, drawn in the 2D map) | open drains, slabs, rubbish, green water, invented by the kit | done in the data; the kit should now read `gutters` and `gutter_crossings` instead of inventing them |

Also in the kit already: road condition and potholes, refuse heaps, litter, poles and tangled wires, transformers, kerbs.

## Missing places (owner, 15 Oct 2026)
Gidi is our city, so these are invented to fit it, not copied. They're built in the same hand pass.

| Place | Now | Plan |
|---|---|---|
| **Betting shops** | 13 in the whole city | As common as chemists: small shopfront betting kiosks with viewing benches on main roads, by markets and motor parks. Most in the Maze, Jungle City, the Hub, Railside and the Bazaar; a few big viewing centres. Placed by the everyday-places layer, like chemists. |
| **The airport** | only the "Airport Fence" pin at the Capital's edge | Gidi's front door, on the unbuilt land north of the Capital, behind the fence that's already there: a runway, a terminal, cargo sheds, an airport road, and a car park with touts. Its own zone, not squeezed into a district. Story: arrivals, cargo theft, the boys at the airport. **First of this group.** |
| **A university** | none (the "colleges" are secondary schools) | A walled campus with faculties, hostels, a guarded gate and a bukateria strip outside, by the lagoon (near Water Town and the Maze) or beside the Bazaar. |
| **Brothels** | none | Shown as places, never explicitly: "hotels" renting rooms by the hour, on the night strips (the Capital's roundabout strip, by the Hub's motor parks, Old Island, by the Port). Mostly story spots, never on safe ground. |

## How it should work
- **The map stays the master copy** (`docs/UNREAL-PORT-PLAN.md`). An ism lives in the data first; the kit and later Unreal only draw it.
- **By rule, then by hand:**
  - A new step, `scripts/isms.py`, runs after the generator. It places each ism at its measured rate where it fits, and writes it into the district data.
  - A hand file, `web/isms-edits.json`, lets the owner add, move or delete any one by hand. Hand edits always win.
- **Deterministic:** the same seed gives the same isms. A district's houses and streets only change where an ism needs them to (a missing link cuts a street; a market spill takes road space).
- **Safe ground:** no ism that brings crime or danger goes on safe ground. That includes churches, mosques, schools, hospitals, clinics, palaces and the Heritage Strip.
- **Checks and test:** `check_district.py` must still pass, with its rules extended where an ism breaks one on purpose. A short living test checks that the isms make life harder in the right places without cutting anyone off.

## Data
`scripts/isms.py` runs in the bake (`scripts/bake_web.py`) after the road clean-up and the road heights, once the safe ground is listed. It adds three keys to `web/gidi-data.js`. Units are metres, y down, like the rest of the data. The same seed (2026) gives the same gutters.

**`gutters`**: one entry per run, which is an unbroken stretch of one gutter, open or covered.
| Key | Meaning |
|---|---|
| `id` | `<road id>:<side>:<n>`, for example `maze/street/22:L:0`. Stable between bakes while the road is unchanged, so hand edits can name it. |
| `road` | The road it runs beside, as the kit names roads: `<district>/street/<i>`, `<district>/lane/<i>`, `main/<i>` (index in `mains`), `art/<name>` (an arterial or expressway). |
| `d` | District id; null for the odd stretch of arterial outside every district. |
| `kind` | `lane`, `street`, `main`, `art` or `exp`. |
| `side` | `L` or `R`: left or right when walking along the road's points on the map. |
| `state` | `open` (a channel you can fall into) or `covered` (under slabs, a walkway). |
| `w`, `depth` | Channel width and depth in metres. |
| `pts` | The centre line, `[[x, y], ...]`, about 4 m out from the road's middle (half its width + 0.3 m + half the channel). |
| `len` | Length in metres. |
| `blocked` | Optional, open runs only: `[{"from", "to", "fill"}]`, metres along the run. `fill` is `rubbish` or `green_water`. |
| `hand` | True on an item added or changed by hand. |

A covered run is also where a gutter passes under a house front or a compound-wall gate, and where it passes safe ground. Where a gutter meets a bigger road it stops (it flows into that road's gutter); where a side street meets it, it carries on and a crossing sits over it.

**`gutter_crossings`**: a plank or slab over an open run.
| Key | Meaning |
|---|---|
| `id` | `<gutter id>:c<n>`. |
| `gutter` | The run it crosses. |
| `at` | Metres along that run to the middle of the crossing. |
| `pt`, `ang` | Where it is `[x, y]`, and the run's heading there in degrees (0 = east, 90 = south on the map). The crossing's length runs along this heading; it spans the channel. |
| `kind` | `plank` (home entrances in poorer districts) or `slab` (shops, gates, kiosks, stall rows, side streets, wealthier houses). |
| `mat` | `plank`, `old door`, `metal sheet` for a plank; `concrete` for a slab. |
| `w` | Length along the run, in metres. A stall row gets 5 to 10 m of slabs. |
| `of` | `entrance` (then `bld`: `[district id, building index]`) or `street` (then `road`: the side street's id). |

**`gutter_rates`**: the rates and class factors used, so the kit can see them.

**Rates per district** (`RATES` in `scripts/isms.py`; `has` is the chance a side of a street has a gutter, `cover` the share under slabs, `blocked` the share of the open length that is blocked): the Maze 0.97 / 0.20 / 0.50, the Hub 0.95 / 0.30 / 0.40, Jungle City 0.95 / 0.15 / 0.60, Food Gate 0.93 / 0.25 / 0.50, the Bazaar 0.93 / 0.30 / 0.40, Water Town 0.90 / 0.08 / 0.65, Railside 0.90 / 0.25 / 0.40, the Frontier 0.75 / 0.35 / 0.15, the Border 0.75 / 0.25 / 0.35, Old Island 0.98 / 0.40 / 0.55, Old Shore 0.93 / 0.35 / 0.45, the Port 0.90 / 0.40 / 0.40, the Capital 0.95 / 0.60 / 0.25, the Estate 0.98 / 0.92 / 0.05, the Heights 0.98 / 0.95 / 0.03. Mains are covered more than streets (half of what is left, so about 60% in the Maze), arterials 88%, expressways 80%; a lane carries one gutter, on a random side, and is rarely covered.

**Safe ground:** a gutter within 12 m of a church, mosque, school, clinic, hospital, palace or the Heritage Strip is covered, never open, and nothing is blocked within 30 m of one (a resident at the gate sees 25 m). `check_district.py` (check 14) fails if a blocked stretch touches the 12 m zone.

**Hand edits** go in `web/isms-edits.json`, applied after the rules so they always win:
```
{"gutters": {"add": [<whole run>], "delete": ["<id>"], "edit": {"<id>": {"state": "covered", "blocked": []}}},
 "gutter_crossings": {"add": [], "delete": [], "edit": {"<id>": {"pt": [x, y]}}}}
```
`edit` changes the named fields (to move an item, give a new `pts` or `pt`). Deleting a gutter takes its crossings with it. A name that no longer exists prints a warning in the bake.

**Not in this data yet:** water levels, flooding (ism 10) and which stretches back up in the rain. The blocked stretches are where that will start.

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
> 7. The missing places (the table above): the airport first, then betting shops, the university, the brothels
>
> For each one:
> - Put it in the map data first: `scripts/isms.py` after the generator, with the rates per district from LAGOS-ISMS.md, plus `web/isms-edits.json` for hand edits.
> - Draw it in the 2D map (`web/app.js`, `web/shell.html`) and the 3D view (`web/view3d.js`). Then have the Blender kit read it from the data instead of inventing it (gutters especially: `legacy/blender/generate.py` and `legacy/blender/city.py`).
> - Extend `check_district.py` where an ism breaks a rule on purpose.
> - Teach `scripts/explore_city.py` where it matters: a missing link really blocks a walk; a one-way street is one-way for a ride.
> - Look at the result in 2D and 3D before showing it.
>
> Work on a branch per group and open a PR per group. Don't push to main. Run a short living test with Haiku agents, one persona in the districts the group touches, and write docs/living-test-<date>.md.
>
> Use cheaper models: Sonnet for building, Haiku for living-test agents and checks. Keep to plain words in docs and PRs.
>
> Safe ground and the sacred list (README) always hold.
