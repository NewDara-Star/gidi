# Which check holds each rule

Every rule in `DECISIONS.md` has a row here: the check that enforces it, or why none can. `scripts/check_rules.py` runs before every commit and push (`.claude/hooks/checks-before-commit.sh`):
it fails when a rule has no row, and lists every rule marked **GAP** (a map rule nothing checks yet). So "are we covering all bases?" is
answered by this table, not by asking. A new rule goes in `DECISIONS.md` and here in the same change.

Checks: `check_map.py` (the new map). The old map's checks (`check_district.py`, `check_real.py`) were deleted with it on 25 Oct; the rows of rules
that held only for the old map went with them to `HISTORY.md` (24 Oct).

| Rule | How it is held | Checked by |
|---|---|---|
| The story: Tunde's | story docs | not a map rule |
| Gidi City: a shared space that feels like home | direction: online, social, the world as the content | owner's review; not a map rule |
| Open world first; narrative optional | direction | not a map rule |
| Gidi is our city. | direction | owner's review |
| Invented names only. | no name on the map shares its core with a real Lagos name (`docs/hand/realnames.txt`); sound-alikes are judged by the owner | `check_map.py` (a name or text sharing a real name's core fails); N1 on the old map; the sound-alike is by ear (owner's review of NAMES.md) |
| Safe ground: | places flagged safe are never crime sites | GAP: no crime sites in the data yet; check when they come |
| If it's in the 3D, it's in the 2D | the kit places nothing of its own | gidi-game `tools/fields.py` (a build that reads an undeclared key stops) |
| Hand-making happens on the drawing board | process | not a map rule |
| The map is never final | the game's builders build from the map's records every time; nothing made from the map is committed in gidi-game | gidi-game `tools/kit_fields.py` (every builder key is a map field); 17 and R0 held it on the old map |
| New districts: | the district list | GAP: the new map has the airport (33) and Yaba-UNILAG (17, 18) in NAMES.md, but no check reads the district list; 4 held it on the old map |
| Old Island is a true island, | water around it | GAP: no water check on the new map yet; 3 held it on the old map |
| The research must be detailed: | studies in docs | owner's review |
| Monuments are placed by hand | `add monument` edits | GAP: the new map has no monument records yet; 12 and 17 held it on the old map |
| The hand pass covers infrastructure and labels | furniture and labels placed by hand land where meant | GAP: `check_map.py` counts fields still unset (its TODO line), not whether every stop, light and label is there; 15 and 17 held it on the old map |
| Roads have surfaces; poorer areas have unpaved and marshy ones | every road has a surface | GAP: no check that a street's surface matches what its twin photos show (earth, laterite, tar, interlock) |
| Freeze everything | the map is hand records in git, with no bake | GAP: nothing checks that a builder makes the same model twice from the same record |
| Account for every square metre: | carriageway, gutter, encroachment; nothing stands on the road (the building line and walkways went with "Real Lagos roads") | PARTIAL (25 Oct): `check_map.py` fails a house more than 1 m2 inside a road's width (`on_road`); not yet stalls, poles or walls (`draft_edge.py` keeps its own off other roads) |
| Markets spill onto the road: | tables in declared zones, a lane kept clear | GAP: no check on the new map, and none anywhere that a lane stays clear; 1 held the zones on the old map |
| Everything is in the data | things are objects with positions | GAP: `check_map.py` checks each record's fields and links, not that everything standing in the world has a record (see "One ground truth"); 16 held it on the old map |
| Every road end is something | no road just stops | PART: `check_map.py` lists road ends that almost land on another road (under 1 m); no check yet that every end is a junction, close, gate, water or map edge; 9 held it on the old map |
| Claude builds Gidi | process | not a map rule |
| Google: study yes, lift no. | Google pictures stay outside the repo | by hand (never committed) |
| Never fetch: | process | not a map rule |
| Look first: | references | owner's review |
| Gidi's data stays on this Mac | `~/gidi-data` has no git remote | by hand: `git -C ~/gidi-data remote` printed nothing (24 Oct) |
| Keep a delete-later list | `docs/DATA-SOURCES.md` | by hand |
| Git: | branches, PRs | GitHub |
| Writing: | process | not a map rule |
| Hold-offs: | process | not a map rule |
| Unreal (go, 17 Oct): | importer | gidi-game |
| Cost: | process | not a map rule |
| The look target | renders | owner's review |
| The laptop is the target machine | frame rate | gidi-game measures |
| Who Gidi is for | process | not a map rule |
| PS5 and Steam, self-published, digital only | process | not a map rule |
| Consoles later: | process | not a map rule |
| Not "GTA for Lagos" | direction: systems and missions come from Lagos life | owner's review; not a map rule |
| Number plates | gidi-game | gidi-game |
| Fonts are custom | gidi-game | gidi-game |
| Vehicles are built like the fonts | gidi-game | gidi-game |
| The first goal: the street video's scene | gidi-game | owner's review |
| Meshy's place | process | not a map rule |
| Matching Lagos | match passes | owner's review |
| The kit session gets exact lists | process | not a map rule |
| Light by default on the laptop | process | not a map rule |
| People | gidi-game | gidi-game |
| Every street has a real twin | every twin street on the map; every street on the map has a twin | GAP: no twin check on the new map; R3 and R6 held it on the old map |
| Take the interesting parts | the child plan | owner's review |
| A livable world before the story | what the twin photos show is on the map near where it was seen | GAP: no check on the new map; R5 held it on the old map |
| The item register, once per finished district | every item typed | GAP: the register is not built yet |
| Match passes | renders against references | owner's review |
| Real Lagos roads, no ideal road template | roads on their real lines, buildings on their real spots, no building cut for a template | GAP: road-line offset check and city flow audit being built (22 Oct) |
| Gidi is Lagos, miniaturised; the map starts again | every district traced to the real places it sits on; positions and network against real Lagos at the chosen scale | GAP: the whole-Lagos study and new frame come first (22 Oct) |
| The new map is 1:3, about 27 x 10.5 km | map size and positions against real Lagos at 1:3 | GAP: comes with the new frame |
| Roads first, districts by their borders | the skeleton is the real road network at 1:3; every district edge is a real border; merged places really touch | GAP: comes with the road skeleton and the border map (22 Oct) |
| The plan is hand-made; the models come from kits | the plan has no generated content; every modelled thing names its kit and its reference pictures | GAP: comes with the new plan and the first kit (22 Oct) |
| A kit is proven by rebuilding real streets from it | each kit's test spots: picture beside the rebuild, held or not, and what was fixed | GAP: comes with the first kit (22 Oct) |
| The map tells the kit what goes where | every kit part is driven by a map field; nothing placed without one | GAP (23 Oct): `schema/kit_reads.json` is now written from the game builders' own `FIELDS` (gidi-game `tools/kit_fields.py --write`); `scripts/check_map.py --kit schema/kit_reads.json` holds the schema to it. Open: record types no builder draws yet (roads, frontages, lean-tos, heaps, trees, masts, rail, ground, roof sheets, wall bays) |
| The interface works both ways; the builders are the kit | every builder key is declared and is a map field; a build that reads an undeclared key stops; schema fields no builder reads are flagged | gidi-game `tools/fields.py` (every build) and `tools/kit_fields.py --map=<gidi>` (exit 1 on a builder field the map cannot say; 0 fail on 23 Oct, 27 flagged); `--records=<map dir>` lists records missing a field |
| The Reach goes with Festac into the new map | The Reach stands in the Festac-inspired place | GAP: comes with the new map |
| Build light, look full: modes, near-detail and streaming | frame time and memory per level in Work, Low, High and Full; budgets per level | GAP: no per-level budget check yet (the modes themselves exist since 22-24 Oct: gidi-game `tools/mode_sg.py`, `tools/play.sh`) |
| One near model; Nanite draws near to far | no builder's look made of Blender-only shader nodes unless owed; every .glb within its kind's triangle budget | gidi-game `tools/look_travels.py` (hooks, every gidi-game commit, push and stop): fails on a new Blender-only look and on an owed file that no longer needs listing; prints each .glb's triangles. PART (24 Oct): buildings held to 300,000 a file; the 80,000 house target, the 30 M scene and props' and vehicles' budgets are not checked yet; owed: the wear layer, the spot's ground, person outfits, the basin test |
| Pieces placed as instances; simple roads; World Partition | kits split into shared pieces placed as instances; roads as simple shapes with tiling textures and decals; World Partition; fine records drawn as instances near the player | GAP (25 Oct): nothing built this way yet (NOW item 0). To come: a check that no placed piece is its own actor (instances only) and that a road .glb stays within a triangle budget per metre |
| Delete what we no longer use; use what the engine has before writing our own; read twice | unused code, tools, logs and dated notes deleted; engine features before our own tools; two-pass reading | GAP: running order item 00 (scripts/inventory.py lists code used nowhere; no check fails on it yet) |
| Map and brush first, Unreal on hold | the work in hand is map and brush work on the board; Unreal items wait in the running order | by eye: the running order (NOW item 03); no check |
| Every district to "working" first, breadth-first | a district counts as working at the bar (roads at real widths, houses with kind and storeys, real places, bus stops and motor parks, landmarks, check at 0); all districts reach it before polish; polish waits in NOW's look-pass line | PART: `scripts/working_bar.py dNN` (run by hand when a district is called working, not on a hook: a district under way fails it) fails on check problems, a house with no kind or storeys, a road under half on a real street (Overture) with nothing saying where it was read, a real place (Overture, the pass-55 categories) with no place of its kind near, no stop or park, a plot with no gated wall; not held: whether widths were read, landmarks not drawn as plots |
| Working first, polish later | every kind on the map has a working model (built, placed in Unreal, light enough) before look passes | GAP: running order item 02(a), docs/MODEL-INVENTORY.md; no check yet fails on a kind with no model |
| Every kit draws instances | each builder exports shared pieces and placements, placed as ISM | GAP: running order item 0(b); no check yet counts builders that still export whole models |
| Save what makes a house, not each house | a house is its own shape plus shared kit pieces placed by its record | GAP (24 Oct): windows and doors are shared pieces in the street test (gidi-game #79), not yet in map builds; no check yet. To come: a check that a building's .glb holds no window, door or bars of its own and that its images are the shared ones |
| Finish the map's first layer first; the parts come from house types | every district's plan layer drawn; each building carries type, storeys, roof, ground floor; pieces drafted by house-type rules | GAP (24 Oct): no check yet. To come: per district, the count of buildings missing those fields (check_map), and a list of districts with no plan layer |
| The owner's eye passes a kit | each test spot: Street View picture beside the rebuild from the same camera, the owner's pass/fail and notes | GAP: comes with the first kit test (22 Oct) |
| People come from a kit too | every person on the shared skeleton; outfits from the checked list; crowd scenes side by side with Street View; crowd held at budget, not cut | GAP: comes with the people kit (22 Oct) |
| One ground truth: everything the kit shows is in the map data | every object the kit builds traces to one map record; the kit has no seeds, scatters or spacing rules; changing a record changes the build | GAP (draft 22 Oct): the new map's format and `scripts/check_map.py` (no unknown field, no missing one with `--strict`, every link lands); holds once the kit reads the new map |
| The ultimate test: rebuild the real picture, then its other angles | each kit spot has inventory.md (every thing in the picture) and side by sides for its first camera and at least one other angle | GAP (23 Oct): by eye in each test folder; no script yet |
| Model clean, then wear it | builders (gidi-game tools/*_build.py) make clean parts; wear is a separate material layer driven by the record's condition | GAP (23 Oct): by eye, on sheets of one object from new to almost dead; no script yet |
| Know it up close, thin it far away | each new object has close-up sheets of its details and joints; distance versions are made from the full model | GAP (23 Oct): by eye (close_vN.jpg next to each built object); no script yet |
| Look how the pros do it, first | a working method | not a map rule; the commit says what was found and where |
| A robust kit, not a matched photo | every kit test pass has turntable sheets for its new objects and a top view plus a second street angle with nothing missing or hollow | GAP (23 Oct): checked by eye in each test folder (closeups/objects/, other_views_passN.jpg); no script yet |
| Kits into pieces; Meshy where stuck | gidi-game `tools/kit_fields.py` lists record types no builder draws yet; triangle budgets (`tools/budgets`, gidi-game #78) | GAP (25 Oct): no check yet that a placed thing is an instance of a shared piece; by eye on the test pictures |
| The road comes first | Every road keeps its read width; houses give way (`scripts/draft_roads.py`, BUILDINGS.md hand passes 43-44) | `check_map.py` (`on_road`): a house more than 1 m2 inside a road's width (half the width each side of the centreline, flat ends) fails. Shown failing on the plan saved before hand pass 43: 2,524 problems; 0 now |
| Houses: real footprints first, then by hand; inner land by lanes | `scripts/draft_buildings.py` skips blocks that hold a building and writes footprints only; `scripts/check_map.py map` lists every house with no kind or storeys (amber) | PARTIAL (23 Oct): no check yet that inner land is within reach of a lane or street |
| Mùṣá's borders, edge roads, rail and service roads | `scripts/check_map.py map`: every plan record's first point is inside its district (so an edge road is in one district only); `rail`, `station` and `service_road` are in the schema | PARTIAL (23 Oct): the inside check runs; no check yet that a neighbour does not redraw an edge road |
| A map picture at every district's close | `scripts/map_picture.py OUT_DIR --near=dNN` prints the land a drawn district should hold that none holds (`gap km2`) and shades it red | GAP (26 Oct): run by hand at each close and the pictures looked at; nothing yet fails a district whose picture was not made |
| A kit item grows; it splits only when it stops fitting | a new recipe key leaves the old recipes building the same; a new builder says in its docstring why it is not a key on an existing one; recipe keys match record fields | GAP (23 Oct): checked by eye at review; no script yet |
| Rules draft, records rule; re-draft on request | a rule change in the draft desk changes no stored record; a re-draft is written beside the current records, keeps hand edits, and lands only on the owner's word | GAP (23 Oct): no re-draft tool yet; holds today because draft rules run only when a spot is first drafted |
| The map format's four calls | check_map.py: brush output stored as full records; small things as rows; dress size reported; every district has a name | PART: the board runs check_map.py on every save and shows the problems (district names included); brushes not built yet (22 Oct) |
| Nothing is claimed without proof | `.claude/hooks/`: `checks-before-commit.sh` (the checks, before every commit and push), `checked-before-commit.sh` (a `Checked:` paragraph with every code or map change), `review-before-push.sh` (a second model, blocks claims with nothing behind them and lying checks), `checks-before-stop.sh` (the checks before a turn ends with code changed) | PART (24 Oct): the hooks run and block; the review is a model's reading, not a proof; an agent's report is checked by hand |
| The new map is the truth | the old map's code and data deleted from gidi (25 Oct); nothing names the store under World Drive's folder | GAP: gidi-game's old importer was deleted 25 Oct (gidi-game #96), so nothing reads the old tiles; `scripts/inventory.py` lists names of deleted files (SUSPECTS) but fails on none |
| Rebuild the old kit's things the new way | each builder made from the old kit's list has a gap list written first (the old render beside real photos), turntable and close-up sheets showing the new model beside the same photos with each gap marked closed or open, and the owner's pass; its row in `docs/OLD-KIT.md` crossed off | GAP (24 Oct): by eye and the owner's pass; `tools/kit_fields.py` lists the record types no builder draws yet, which shrinks as builders come |
