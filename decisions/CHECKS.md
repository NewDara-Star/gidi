# Which check holds each rule

Every rule in `DECISIONS.md` has a row here: the check that enforces it, or why none can. `scripts/check_rules.py` runs with every bake:
it fails when a rule has no row, and lists every rule marked **GAP** (a map rule nothing checks yet). So "are we covering all bases?" is
answered by this table, not by asking. A new rule goes in `DECISIONS.md` and here in the same change.

Checks: `check_district.py` (1–17, every district), `check_real.py` (R1–R5, N1: the areas built from real places), the bake's
DETERMINISTIC line (`tools/bake.sh`).

| Rule | How it is held | Checked by |
|---|---|---|
| The story: Tunde's | story docs | not a map rule |
| Open world first; narrative optional | direction | not a map rule |
| Gidi is our city. | direction | owner's review |
| Invented names only. | no real name from the studied places on the map; shapes from data are allowed as twins (study yes, lift no) | N1 |
| Safe ground: | places flagged safe are never crime sites | GAP: no crime sites in the data yet; check when they come |
| If it's in the 3D, it's in the 2D | the kit places nothing of its own | kit session (gidi-game importer) |
| Hand-making happens on the drawing board | process | not a map rule |
| The browser 3D is a quick preview; the full scene is for Unreal | process | not a map rule |
| The map is never final | the importer and the area builds are re-runnable (`scripts/rebuild_areas.py`) | 17, R0 |
| Layout v2 at 1:4 | the frame | 4, 6, 7 |
| New districts: | the district list | 4 |
| Old Island is a true island, | water around it | 3 |
| Regenerate, don't move the old frozen Food Gate block. | process | not a map rule |
| One shared generator, one profile per district, run in parallel. | process | not a map rule |
| The research must be detailed: | studies in docs | owner's review |
| The Reach moves to Jungle City, on Carnival Avenue | a monument edit | 12 |
| Monuments are placed by hand | `add monument` edits | 12, 17 |
| Claude decides when the owner says so | process | not a map rule |
| Know when to stop generating; then hand-make Gidi | process | not a map rule |
| The hand pass covers infrastructure and labels | furniture and labels placed by hand land where meant | 15, 17 |
| Roads have surfaces; poorer areas have unpaved and marshy ones | every road has a surface | GAP: no check that a street's surface matches what its twin photos show (earth, laterite, tar, interlock) |
| Hand-place, not tune. | hand edits on top of the built base | 17 |
| Freeze everything | the map comes out the same every bake | DETERMINISTIC |
| Account for every square metre: | carriageway, gutter, walkway, building line, encroachment | 1, 2, 3, 14, 15, 16 |
| Markets spill onto the road: | tables in declared zones, a lane kept clear | 1 (zones); GAP: no check that a lane stays clear |
| Everything is in the data | things are objects with positions | 16 |
| Every road end is something | no road just stops | 9 |
| Claude builds Gidi | process | not a map rule |
| Google: study yes, lift no. | Google pictures stay outside the repo | by hand (never committed) |
| Never fetch: | process | not a map rule |
| Look first: | references | owner's review |
| Keep a delete-later list | `docs/DATA-SOURCES.md` | by hand |
| Git: | branches, PRs | GitHub |
| Writing: | process | not a map rule |
| Hold-offs: | process | not a map rule |
| Unreal (go, 17 Oct): | importer | gidi-game |
| Cost: | process | not a map rule |
| The look target | renders | owner's review |
| The laptop is the target machine | frame rate | gidi-game measures |
| Build order: outward from the Maze, not story order | process | not a map rule |
| Consoles later: | process | not a map rule |
| Number plates | gidi-game | gidi-game |
| Fonts are custom | gidi-game | gidi-game |
| Vehicles are built like the fonts | gidi-game | gidi-game |
| The first goal: the street video's scene | gidi-game | owner's review |
| Meshy's place | process | not a map rule |
| Matching Lagos | match passes | owner's review |
| The kit session gets exact lists | process | not a map rule |
| The Lagos pass | owner looks | owner's review |
| Light by default on the laptop | process | not a map rule |
| People | gidi-game | gidi-game |
| Places are built like the fonts and the danfo | rebuilt one-for-one first | R1, R2, R4 |
| Every street has a real twin | every twin street on the map; every street on the map has a twin | R3, R6 |
| District by district, matched to real life at plan level first | counts and lengths against the real place | R1, R2, R4 |
| Every type has a real twin too | each type records its real source | GAP: comes with the item register |
| A district is the child of its real inspirations, built only from real pieces | built from real data only | R1, R2, R3, R6 |
| Seams between child districts | shared lines and gateways | 4, 5, 6, 7 |
| Gidi stays Gidi, not a clone of Lagos | direction | owner's review |
| Take the interesting parts | the child plan | owner's review |
| A livable world before the story | what the twin photos show is on the map near where it was seen | R5 |
| The item register, once per finished district | every item typed | GAP: the register is not built yet |
| Match passes | renders against references | owner's review |
| Fixes reach everything already built | areas rebuilt from source every time; hand fixes that no longer land fail | 17, R0 |
| Hand-made, checked by programs; the base is frozen | `scripts/rebuild_areas.py` | refuses to run unless `GIDI_REBUILD_OK=owner`; every hand edit must land (check 17, `check_district.py`); a change to the area builder shows in review |
| Real Lagos roads, no ideal road template | roads on their real lines, buildings on their real spots, no building cut for a template | GAP: road-line offset check and city flow audit being built (22 Oct) |
| Gidi is Lagos, miniaturised; the map starts again | every district traced to the real places it sits on; positions and network against real Lagos at the chosen scale | GAP: the whole-Lagos study and new frame come first (22 Oct) |
| The new map is 1:3, about 27 x 10.5 km | map size and positions against real Lagos at 1:3 | GAP: comes with the new frame |
| Roads first, districts by their borders | the skeleton is the real road network at 1:3; every district edge is a real border; merged places really touch | GAP: comes with the road skeleton and the border map (22 Oct) |
| The plan is hand-made; the models come from kits | the plan has no generated content; every modelled thing names its kit and its reference pictures | GAP: comes with the new plan and the first kit (22 Oct) |
| A kit is proven by rebuilding real streets from it | each kit's test spots: picture beside the rebuild, held or not, and what was fixed | GAP: comes with the first kit (22 Oct) |
| The map tells the kit what goes where | every kit part is driven by a map field; nothing placed without one | GAP (23 Oct): `schema/kit_reads.json` is now written from the game builders' own `FIELDS` (gidi-game `tools/kit_fields.py --write`); `scripts/check_map.py --kit schema/kit_reads.json` holds the schema to it. Open: record types no builder draws yet (roads, frontages, lean-tos, heaps, trees, masts, rail, ground, roof sheets, wall bays) |
| The interface works both ways; the builders are the kit | every builder key is declared and is a map field; a build that reads an undeclared key stops; schema fields no builder reads are flagged | gidi-game `tools/fields.py` (every build) and `tools/kit_fields.py --map=<gidi>` (exit 1 on a builder field the map cannot say; 0 fail on 23 Oct, 27 flagged); `--records=<map dir>` lists records missing a field |
| The Reach goes with Festac into the new map | The Reach stands in the Festac-inspired place | GAP: comes with the new map |
| Build light, look full: modes, near-detail and streaming | frame time and memory per level in Work, Low, High and Full; budgets per level | GAP: comes with the mode switch in gidi-game (22 Oct) |
| The owner's eye passes a kit | each test spot: Street View picture beside the rebuild from the same camera, the owner's pass/fail and notes | GAP: comes with the first kit test (22 Oct) |
| People come from a kit too | every person on the shared skeleton; outfits from the checked list; crowd scenes side by side with Street View; crowd held at budget, not cut | GAP: comes with the people kit (22 Oct) |
| One ground truth: everything the kit shows is in the map data | every object the kit builds traces to one map record; the kit has no seeds, scatters or spacing rules; changing a record changes the build | GAP (draft 22 Oct): the new map's format and `scripts/check_map.py` (no unknown or missing field, every link lands); holds once the kit reads the new map |
| The ultimate test: rebuild the real picture, then its other angles | each kit spot has inventory.md (every thing in the picture) and side by sides for its first camera and at least one other angle | GAP (23 Oct): by eye in each test folder; no script yet |
| Model clean, then wear it | builders (gidi-game tools/*_build.py) make clean parts; wear is a separate material layer driven by the record's condition | GAP (23 Oct): by eye, on sheets of one object from new to almost dead; no script yet |
| Know it up close, thin it far away | each new object has close-up sheets of its details and joints; distance versions are made from the full model | GAP (23 Oct): by eye (close_vN.jpg next to each built object); no script yet |
| Look how the pros do it | a working method | not a map rule |
| A robust kit, not a matched photo | every kit test pass has turntable sheets for its new objects and a top view plus a second street angle with nothing missing or hollow | GAP (23 Oct): checked by eye in each test folder (closeups/objects/, other_views_passN.jpg); no script yet |
| Mùṣá's borders, edge roads, rail and service roads | `scripts/check_map.py map`: every plan record's first point is inside its district (so an edge road is in one district only); `rail`, `station` and `service_road` are in the schema | PARTIAL (23 Oct): the inside check runs; no check yet that a neighbour does not redraw an edge road |
| A kit item grows; it splits only when it stops fitting | a new recipe key leaves the old recipes building the same; a new builder says in its docstring why it is not a key on an existing one; recipe keys match record fields | GAP (23 Oct): checked by eye at review; no script yet |
| Rules draft, records rule; re-draft on request | a rule change in the draft desk changes no stored record; a re-draft is written beside the current records, keeps hand edits, and lands only on the owner's word | GAP (23 Oct): no re-draft tool yet; holds today because draft rules run only when a spot is first drafted |
| The map format's four calls | check_map.py: brush output stored as full records; small things as rows; dress size reported; every district has a name | PART: the board runs check_map.py on every save and shows the problems (district names included); brushes not built yet (22 Oct) |
