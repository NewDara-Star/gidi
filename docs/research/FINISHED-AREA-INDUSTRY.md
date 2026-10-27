# What a "finished" area means in the industry

Research for NOW item 16 (c) and (f), 27 Oct 2026. Every claim below has the URL it came from. Each source is marked
**[read]** (I read the page text myself), **[snippet]** (I saw only a search-result snippet or a summary of it,
not the page), or **[blocked]** (the page would not load). Numbers worked out here from a source are marked
*(arithmetic)*.

Not covered here: GTA V's own files (NOW 16 c(1) is a separate job). Talks I could not read because the GDC Vault was
down for maintenance on 27 Oct: Elan Ruskin's *Marvel's Spider-Man: A Technical Postmortem*, David Santiago's
*Procedurally Crafting Manhattan*, and CD Projekt's *Building Night City: The Technology*.

---

## 1. How studios take an area from blockout to final

### The named stages

No studio has published one standard list. The same order comes up again and again, though, with different names:

| Source | Stages, in order |
|---|---|
| The Level Design Book (Robert Yang) **[read]** https://book.leveldesignbook.com/process/overview | pre-production, (combat design), layout (top-down 2D), **blockout** (playable 3D rough draft, playtested), scripting, lighting, **environment art** (one or more "art pass" rounds), release |
| World of Level Design (AlexG) **[read]** https://worldofleveldesign.com/categories/ue4/bsp-03-level-workflow.php | Blockout/Prototype pass, Gameplay pass, Meshing pass (blocks become "mostly finished" meshes), Lighting pass, Post Process and Effects pass, **Polish pass** (blocking volumes, audio, effects, reflection actors, particles, testing and bug fixing) |
| Daniel McGowan (Senior Environment Artist, Amazon Game Studios) on 80 Level, 14 Dec 2017 **[read]** https://80.lv/articles/the-stages-of-environment-art-in-gamedev | Level brief, key art and map layouts, level design blockout, **proxy phase** (modular pieces at the right proportions; also used to track asset counts), production concepts, final assets, **polish/set dressing** (props, decals, signage), lighting (runs through the whole of production) |
| Aaron Myers (lead artist, *KotOR II*, Obsidian), designer diary, 2004 **[read]** http://www.gamebanshee.com/ux6 | "blocked" (temporary textures, low-detail geometry), then built/textured with a first lighting pass, then final polish, then signed off as "done" from an art perspective; "three to five weeks" per area per artist |
| Guerrilla, *Horizon Forbidden West* (GDC 2022), on Game Developer **[read]** https://gamedeveloper.com/gdc2022/take-a-peek-inside-the-level-design-process-of-horizon-forbidden-west | paper prototypes, skeleton block-out, "first playable" ready for playtest feedback, then "a long process of iteration and parallel development until it's time to ship" |
| Blizzard, *Diablo IV* open-world level art (GDC 2024) **[snippet]** https://mahreenfatima.artstation.com/projects/wred8Y (403 when fetched) | a step-by-step process from blockout to shippable quality; the open world is split into **POIs** (points of interest) and the **wilderness** between them |

What they share:

- **Blockout / greybox / graybox** means the same thing in every source: simple shapes, playable, at the right size,
  and no attention to looks. Yang: build the level "without worrying about how it looks", put in placeholder NPCs and
  items, and write down which sizes must not change before the art pass ("No one can read your mind")
  **[read]** https://www.blog.radiator.debacle.us/2017/09/how-to-graybox-blockout-3d-video-game.html
- **The art pass replaces blocks without changing the play.** Env art is "cosmetic decoration of a level ... while
  preserving its core functionality and gameplay". Work "in stages", "START BIG", and keep small detail for later
  passes **[read]** https://book.leveldesignbook.com/process/env-art
- **Set dressing / polish** is the props, decals and signage pass (McGowan), and the prop count is "often limited by
  team resources and schedule" **[read]** (80 Level link above).
- **Lighting** is either its own pass (World of Level Design) or a thread running through the whole of production (McGowan).
- **Done is judged in context:** you need to see assets next to each other "to know if an asset is 'finished' or
  not", and "sometimes a 50% finished art asset can actually be 100% 'finished enough'" **[read]**
  (Level Design Book env-art link above).

### City games in particular

City-specific production stages are not published in anything I could read. What I found:

- **Rockstar North (GTA V):** Aaron Garbut, quoted from an Edge interview: "We always use the same process: working
  with real cities, starting on a macro level to define the districts we want to use, and working down"; landmarks are
  decided "once we get to the individual building level" **[read]**
  https://www.playstationlifestyle.net/2014/01/02/rockstar-art-director-id-never-want-to-rebuild-a-city-thinks-it-would-be-less-satisfying-for-everyone/
- **Rockstar (GTA VI):** the map is "always the first thing that Rockstar does on these big open-world games"
  (Jason Schreier, after visiting Rockstar North). He says a few artists worked on the map from 2015, years before full
  production **[read]**
  https://www.techradar.com/gaming/rockstar-artists-have-been-working-on-gta-6-for-11-years-to-plan-out-the-map-co-head-says-roads-are-narrower-than-gta-5s-which-had-a-ripple-effect-as-the-studio-had-to-add-even-more-buildings-all-these-things-sort-of-come-to-bite-you-later
- **Ubisoft (Watch Dogs, Chicago):** they started from "a top view of Chicago, the actual Chicago map", put it in the
  editor and "carved into it", then went "street by street putting in neighborhoods, landmarks" (a level designer named
  Arriola, quoted from the Chicago Tribune) **[read, second-hand]**
  https://legallysociable.com/2014/05/15/designing-a-big-city-for-more-gaming-enjoyment/ (the Tribune original would not load)
- **Insomniac (Spider-Man):** crimes and vignettes are placed by procedural systems that find suitable spots
  (SIGGRAPH 2019 abstract) **[read]** https://history.siggraph.org/?p=82780. In Santiago's words, the procedural
  systems ended up used to "author, modify and monitor much more content than planned" **[read]**
  https://www.gamedeveloper.com/programming/video-procedurally-creating-manhattan-for-i-marvel-s-spider-man-i-
- **Ubisoft (AC Unity):** Notre Dame is "proportionally 1:1 with the real thing". About a quarter of buildings have
  interiors (level designer Bruno Saint Andre) **[read]** https://kotaku.com/assassins-creed-unitys-paris-is-huge-really-huge-1588817927
- **Saints Row, Sleeping Dogs, Cyberpunk:** I found no stage list for any of them. On Sleeping Dogs, all I could find
  is that the city is "four distinct areas" meant to capture the essence of Hong Kong **[read]**
  https://www.gamingnexus.com/News/25918/Sleeping-Dogs-behind-the-scenes-of-Hong-Kong

---

## 2. How studios shrink a real city

### What they said and did

- **Rockstar, GTA V (Los Angeles):** Garbut: "I'd never want to rebuild a city"; "We compress, we edit, we emphasise
  certain things"; "We'll move entire districts about geographically, never mind individual buildings"; the result
  feels more like "the popular perception of the place" than the real city **[read]** (PlayStation LifeStyle link above).
  A fan analysis says Rockstar kept "the major roads, highways and rough relative locations" of landmarks, and that
  "There are significantly more streets in LA than what LS depicts" (Aron Gerencser) **[read]**
  https://www.gtaboom.com/How_Well_Does_GTA_V's_Map_Emulate_Los_Angeles. No scale ratio is given by Rockstar.
  Fan figures (about 1% of LA County's area) are **[snippet]** only.
- **Rockstar, GTA VI (Miami): narrower roads, more buildings.** Garbut told Schreier that "the roads are
  significantly narrower in GTA 6 than they were in GTA 5". The narrower roads and denser traffic were planned from
  the start. Knock-on effect: they needed more buildings around them ("All these things sort of come [back] to bite you
  later") **[read]** (TechRadar link above; TechRadar's own line calls it "a fictional Los Angeles", but the game is set
  in Vice City/Miami. That is the article's slip). PSU and MP1st report the same and add that GTA V's wide roads let
  players "easily circumvent other traffic" **[read]**
  https://www.psu.com/news/grand-theft-auto-vi-includes-significantly-narrower-roads-than-gta-v-weapons-system-more-like-red-dead-redemption-2/ ,
  https://mp1st.com/news/gta-6-features-narrower-roads-than-gta-5-wanted-weapons-system-more-like-red-dead-redemption-2
  (primary source: Schreier's video https://www.youtube.com/watch?v=lZ5iiT8IqY0, not watched).
- **Insomniac, Spider-Man (Manhattan): fewer streets, not narrower ones.** A fan measurement puts the map at
  "roughly a 1/4 scale" of the part of Manhattan it covers (about 4.6 mi²), which is about 1:2 along each side
  *(arithmetic)*. Central Park is shrunk harder ("a little bit less than 1/7"). Cross streets are dropped ("the next
  street after 107th is 103rd"). Some streets are invented ("Garvin") to carry the grid north. The north of the
  island is cut off at 132nd St (Alex Gibson) **[read]**
  https://twinfinite.net/news/heres-how-big-spider-man-ps4s-open-world-map-is-compared-to-manhattan/.
  Insomniac never gave an official size **[snippet]** https://www.gamesradar.com/spider-man-ps4-map-size
- **Ubisoft, Watch Dogs (Chicago): density over size.** Jonathan Morin: "One thing I wanted to promote with Watch
  Dogs was density, a lot more than scale"; "I don't want size just becoming a space between A and B" **[read]**
  https://gamingbolt.com/watch-dogs-render-of-chicago-compares-to-gta-5s-los-santos-in-density (from Eurogamer).
  They dropped the straight grid: "too many right angles". Curved roads, because "It's better for the game play if you
  can't see far ahead of yourself" **[read, second-hand]** (legallysociable link above). The same blog says
  "Four-lane roads became six lanes" and buildings were "pressed together". That is the blogger's own wording, not
  sourced to the developer **[read, unattributed]**.
- **Ubisoft, Watch Dogs 2 (San Francisco):** a level-design director told GameStar that they used Google Maps, left a lot
  out, moved roads, changed proportions and trimmed whole districts **[snippet]**
  https://www.gamestar.de/artikel/watch-dogs-2-so-viel-san-francisco-steckt-im-spiel,3303617.html (403).
- **Ubisoft, Watch Dogs Legion (London):** 8 of Inner London's 12 boroughs, from Wellington Arch to the Isle of Dogs
  and from Camden Market to Brixton (Clint Hocking). How much it was shortened was "not known" **[read]**
  https://www.pcgamesn.com/watch-dogs-legion/map-size. A figure of "about 30% shorter" distances is **[snippet]** only.
- **Hangar 13, Mafia: Definitive Edition (Lost Heaven): wider streets, softer corners.** They "redesigned the city to
  make it more fun to spend time in your car, widening streets and reducing 90 degree angles", and the city is "a bit
  more crowded" **[read]** https://www.pcgamer.com/mafia-definitive-edition-aims-to-make-lost-haven-more-fun-to-drive-around/.
  They kept the 2002 map as a guideline, and the districts and main roads are largely unchanged **[snippet]**
  https://www.gamepressure.com/newsroom/mafia-remake-heres-new-map-of-lost-heaven/z92133
- **United Front, Sleeping Dogs (Hong Kong):** four districts (Kennedy Town, North Point, Central, Aberdeen). A
  review said places were "noticeably minimized" **[snippet]** https://www.techradar.com/news/weaving-through-the-streets-of-hong-kong-with-sleeping-dogs-designer
  (the page loaded without its text).
- **SCS, American Truck Simulator: changed the scale itself.** Moved from 1:35 to 1:20 because "perhaps the greatest
  number of complaints" were about scale. That made "75% longer roads outside the cities", and they revisited "the
  placement of cities and crossroads". The post gives no scale for the cities themselves **[read]**
  https://blog.scssoft.com/2016/06/the-rescale.html. "Cities don't follow the ratio at all, and SCS has never said what
  scale it uses for them" **[read]** https://racinggames.gg/article/why-american-truck-simulators-map-scale-is-running-out-of-room.
  A forum claim of "1:3 in cities" is **[snippet]**, unverified.
- **Hiding a short street:** "you should avoid designing straight roads" (curves hide a street's short length).
  "A carefully designed soundscape can suggest a much larger virtual city" **[read]**
  https://filmstories.co.uk/features/citycraft-suggesting-size-and-complexity/

### Real-world yardsticks for street density

- **UN-Habitat:** "the street network should encompass at least 30 per cent of the land with at least 18 km of street
  length per square kilometer". Their model is a 1 km² grid of 9 + 9 streets **111 m apart**. Arterials are
  **800-1,000 m** apart. Real cities use "20-30 per cent of urban land and 40-60 per cent of commercial centre land"
  for roads and parking **[read]** (UN-Habitat, *A New Strategy of Sustainable Neighbourhood Planning: Five
  Principles*, 2014)
  https://unhabitat.org/sites/default/files/documents/2019-05/five_principles_of_sustainable_neighborhood_planning.pdf
- **Epic's Matrix Awakens city:** "over 260 km of roads" on "Sixteen kilometers square" = **about 16 km of road per
  km²** *(arithmetic)*, close to UN-Habitat's 18. **[read]**
  https://www.unrealengine.com/en-US/blog/introducing-the-matrix-awakens-an-unreal-engine-5-experience

### The three most useful findings for Gidi

1. **Shrinking a real city means dropping streets, not shrinking them** (Spider-Man drops cross streets and invents a
   few; Los Santos has "significantly more streets" missing than LA). On a map shrunk k times along each side, keeping
   every street multiplies street length per km² by k *(arithmetic)*. At 1:3, about a third of the real street length
   is all that fits at real density.
2. **Road width is a creative dial that studios turn both ways, and it costs land either way:** GTA VI made roads
   *narrower* than GTA V's for denser traffic, and that forced more buildings. Mafia DE and (by one blog) Watch Dogs made
   them *wider* for driving.
3. **Scale can be uneven on purpose:** Rockstar "compress, edit, emphasise" and move whole districts. Spider-Man
   shrinks Central Park harder than the streets. SCS changed the whole map's scale when players complained, and scales
   cities differently from roads. Gidi's DECISIONS already say "the shrink is uneven" (22 Oct). These studios show it
   can also be uneven *by district*.

---

## 3. Unreal Engine's own guidance: City Sample (The Matrix Awakens)

- **Size and counts** **[read]** (Epic blog above): 16 km²; "seven million instanced assets"; "seven thousand buildings
  made of thousands of modular pieces, 45,073 parked cars (of which 38,146 are drivable), over 260 km of roads, 512 km
  of sidewalk, 1,248 intersections, 27,848 lamp posts, and 12,422 manholes". Per km² *(arithmetic)*: about 440
  buildings, 16 km of road, 32 km of sidewalk, 78 intersections, 1,740 lamp posts, 780 manholes and 2,800 parked cars.
  These are figures for a generated American downtown, a reference for the method only, not a target for Lagos.
- **How it was generated** **[read]** https://dev.epicgames.com/documentation/en-us/unreal-engine/city-sample-project-unreal-engine-demonstration :
  Houdini makes the city shape, road network, freeway, building placement and metadata, exported as "a huge point
  cloud". Unreal's **Rule Processor** turns that into "thousands of instances". The build stages run in dependency
  order: **City Layout → Roads → Freeway → Lots and Sidewalks → Traffic / Buildings / Ground → Street Furniture /
  Decals / Audio**. Buildings come from a shape grammar, one rule set per style. Epic's blog: rules decide everything
  "from the size of the roads and the height of the buildings, all the way down to the amount of debris on the
  sidewalks", so "you can regenerate the entire city, right up until the last day of delivery" **[read]**.
- **The Houdini side** **[read]** https://dev.epicgames.com/documentation/en-us/unreal-engine/city-sample-quick-start-for-generating-a-city-and-freeway-using-houdini :
  city outline curve, then arterial curves, then road network (block merge and smoothing), then zones (height
  falloff), then freeway (4 or 6 lanes), then ramps, then lots and buildings, then city furniture, then export.
  Small City is about 1 km across, Big City about 5 km.
- **The Unreal side** **[read]** https://dev.epicgames.com/documentation/en-us/unreal-engine/city-sample-quick-start-for-generating-a-city-and-freeway-in-unreal-engine-5 :
  import the point cloud and geometry, then run the rule processors, then set up the parking and traffic-light data,
  then **build the ZoneGraph for traffic** (zone shapes for lanes, traffic lights, parking spaces; "Navigation Paths
  for traffic and pedestrians"), then **build World Partition HLODs**, then play.
- **Layers in a finished City Sample block** (from the two pages above): road surface and decals; traffic lanes as
  ZoneGraph zone shapes with tags; traffic lights; parking spaces with parked cars; sidewalks with pedestrian lanes;
  **Mass** spawners for crowds, intersections, traffic and parked vehicles; crowd behaviour in StateTree; buildings;
  street furniture, decals and trash (Nanite); audio; Lumen lighting; World Partition cells; Data Layers (procedural
  objects, rooftop props, freeway); HLODs; One File Per Actor. Crowd, Traffic and Parked Cars have **density
  sliders** in World Settings, with no numbers given **[read]**.
- **World Partition** **[read]** https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine :
  one level cut into streamed grid cells (cell size and loading range are settings). "Using more than one grid can
  negatively impact performance". HLODs are built per cell as stand-ins seen from far away.
- **Engine status:** MassTraffic "is not an official plugin" outside City Sample. MassCrowd is official but
  experimental **[snippet]** https://forums.unrealengine.com/t/ue-5-7-city-sample-broken/2701997 (forum thread). On UE
  5.7, City Sample traffic needed a manual rebuild of `CityTrafficBuilder_BP` **[snippet]** (same thread). This matters
  for Gidi on 5.8.
- **Could not read:** Epic's ZoneGraph, MassEntity detail and PCG overview pages (they render empty or sit behind
  Cloudflare). The MassEntity page gives only "a gameplay-focused framework for data-oriented calculations" **[read]**.

---

## 4. Published "definition of done" / milestone checklists

- **Four levels of done** (Mike Cohn, describing what "a number of game studios" do) **[read]**
  https://www.mountaingoatsoftware.com/blog/multiple-levels-of-done : (1) the idea can be evaluated (art not final);
  (2) the feature is integrated into the game; (3) shippable, "good enough to include in a public release";
  (4) "tuned, polished, and as good as the team reasonably knows how to make it".
- **Filament Games exit criteria** **[read]** https://www.filamentgames.com/blog/alpha-beta-gold-commitment-high-quality-game-development :
  **Alpha**: "roughly feature-complete"; art "not all placeholder"; performance "minimally viable"; key sound effects in.
  **Beta**: "There are no placeholder art assets"; "All art assets match the style guide"; "All interactions have sound
  effects"; target framerate "in a majority of tested scenarios". **Gold**: target framerate "in all tested
  scenarios"; enough sound variety to avoid "noticeable/distracting repetition".
- **Placeholder share as a milestone** (e.g. alpha up to 50% placeholder art) **[snippet]**
  https://davidmullich.com/2011/11/14/milestone-abcs-alpha-beta-and-contract
- **KotOR II:** an area is "done" from an art perspective after blocked → built/textured + first light → final polish
  **[read]** (gamebanshee link above).
- I found **no published environment-art checklist for an open-world city block** from a AAA studio. The closest are
  the pass lists in section 1 and City Sample's build stages in section 3.

---

## What this means for Gidi

### The stages, as Gidi could name them

Gidi's own words already line up with the industry's: the **working bar** (26 Oct) is a blockout. It is playable in
the data, at the right size, with no looks. The industry then expects a **first playable/integrated** stage (built in
Unreal, walkable, drivable), then an **art pass** (kits replace blocks), then **set dressing**, **lighting**, and
**polish/sign-off**. For Gidi, "finished" could be Cohn's level 3 per district: shippable, with polish (level 4) left
for hero streets later, as in the breadth-first rule of 26 Oct.

### Draft list of topics for a finished district, each with how it could be measured

This is a draft for the owner and Claude to agree (NOW 16 c). Numbers from City Sample or UN-Habitat are yardsticks
only. Each Lagos target should come from the real place (Google Maps, satellite, Street View).

| # | Topic (layer) | How it could be measured |
|---|---|---|
| 1 | **Roads and streets** on real lines | % of road length on a real line (existing); street km per km² and % of land under road, against the real district read from Google Maps (UN-Habitat 18 km/km² and 30% as an outside yardstick) |
| 2 | **Traffic lanes and junctions** (Unreal ZoneGraph) | every drivable road has lanes, joined at every junction (0 dead ends that aren't real dead ends); junctions with lights/control where real; one test drive across the district without a stuck car |
| 3 | **Walkways and crossings** (pedestrian lanes) | pedestrian lane km per road km; every house frontage reachable on foot; 0 walls across a lane |
| 4 | **Buildings** | cover inside the Google Open Buildings band (existing DENSITY row); 100% with kind and storeys; 0 overlaps; every house fronts a road or lane |
| 5 | **Places, landmarks, bus stops, motor parks** | 0 real places missing (existing); each landmark walled with a gate (existing) |
| 6 | **Street furniture and clutter** (poles, wires, signs, kiosks, generators, gutters, manholes) | count per km of road, against counts from Street View shots of the real street |
| 7 | **Parked vehicles and parking spots** | spots per km of road, against Street View |
| 8 | **Crowd and traffic population** | agents per km² at rush hour and at night, against real counts from Street View or video; Mass density settings written per district |
| 9 | **Activities and vignettes** (markets, roadside trades, scenes; Spider-Man's "crimes and vignettes") | spots per km², each with a real reference picture |
| 10 | **Ground and scatter** (sand, mud, drains, grass verges) | % of open ground painted with a ground type, 0 unpainted |
| 11 | **Lighting, day and night** | night shot from 3 fixed cameras: light sources per street; by eye against real night photos |
| 12 | **Sound zones** | every district covered by an ambience zone; by ear |
| 13 | **Collision and navigation** | walk and drive every street: 0 fall-throughs, 0 stuck spots |
| 14 | **Performance** | HLOD built; frame time on the M4 in Work mode at the 30 fps / 1080p target, from 3 fixed cameras |
| 15 | **Art level** | placeholder share (Filament: beta = 0 placeholders); kit pieces match the photo references |
| 16 | **The look test** | overhead shot against Google Earth, plus street shots against Street View, by eye (Mùṣá's test of 25 Oct) |

### The street-density problem: the options, and who did what

The problem (NOW 16 f): roads at full width on a 1:3 map make our street length per km² 2.1-3.7x the real figure,
so blocks are small and roads take the land.

| Option | Who did it | What it costs Gidi |
|---|---|---|
| **A. Drop more streets** (keep the main roads and the streets with character; leave out repeats) | Insomniac (cross streets left out); Rockstar ("significantly more streets in LA"); Gidi's own 22 Oct rule (uneven shrink, about 1 local street in 11) | fewer real streets per district; the dropped ones can come back as lanes and footpaths (the 23 Oct rule) |
| **B. Narrower roads** (true Lagos widths, or narrower still on minor streets) | Rockstar GTA VI ("significantly narrower" than GTA V; it forced more buildings and denser traffic) | goes against "roads at full real width" (25 Oct), so it is the owner's call; tighter driving |
| **C. Wider roads for driving** | Hangar 13 Mafia DE; Watch Dogs (blog claim, unsourced) | makes our problem worse; listed only to show both directions exist |
| **D. Less compression where it matters** (a gentler scale in hero districts, harder in sprawl) | Rockstar ("compress, edit, emphasise", whole districts moved); Insomniac (Central Park shrunk harder than the rest); SCS (rescaled the whole map; cities at their own scale) | a bigger map, or squeezing other districts more |
| **E. Density over size** (a smaller map with more in it) | Ubisoft Watch Dogs (Morin) | this is option A, chosen on purpose |
| **F. Hide shortness** (curves, blocked views, sound) | Watch Dogs Chicago (no straight grid); Film Stories' "CityCraft" | does not change the land roads take, only how big the city feels |

**What is still owed before the owner chooses:** the real street km per km² and road share of land in each drawn
district, read from Google Maps (NOW 16 f). The same for GTA V's Los Santos from its files (NOW 16 c(1)). Then put
both next to UN-Habitat's 18 km/km² and 30%, and the Matrix city's 16 km/km². Our own figures are in the Checked
section below (from `scripts/working_bar.py`).

## Checked (main session, 27 Oct)

- UN-Habitat's two lines (at least 30% of land and at least 18 km of street per km²; streets 111 m apart in the model;
  20-30% of urban land used for roads and parking): re-read in the PDF's own text (PyMuPDF), all four found word for
  word.
- Epic's Matrix Awakens figures (260 km of road, 16 km²): **not checked**; the page returned 403 to the main session.
- GTA VI's narrower roads, Spider-Man's dropped streets, Mafia's wider streets, SCS's rescale, the City Sample build
  order and the per-km² Matrix counts: **not checked** yet; they are the agent's reading, with its links above.
- Set against Gidi (working_bar.py and the Saba/Makoro audit, 27 Oct): our street length is 27.5-47.8 km per km²
  (UN-Habitat's floor is 18; Overture's real Lagos 8.4-17.1, thin). Saba's carriageways take 32.8% of its land,
  Makoro's 18.5%, near UN-Habitat's 20-30% band. Off the roads, Saba's houses cover 21.4% of the land against
  Google's 38.5% there. All four are the auditor's figures, **not re-run**; if they hold, more of the cover gap is
  houses not drawn than land lost to roads, but that is not yet a finding.
