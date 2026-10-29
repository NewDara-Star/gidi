# The look of Gidi: render notes

Where the work on Gidi's look stands, so it can be picked up again (owner, 29 Oct: "save the render notes in a
folder so we don't lose them whenever we want to keep doing iteration work on the look of Gidi"). The pictures,
scripts and test files live outside the repo in `~/gidi-data/research/look-test-29oct/` (105 MB). These notes
say what each one is, what the owner said, and what was found. The running order item is `decisions/NOW.md` 04.

## Where it stands (29 Oct)

- **Stylized, not realism** (owner: "realism as a concept makes a game dated quick"; "going stylized means you have
  a look"), with a photo mode worth selling.
- **The target** (owner, five reference pictures, "This is the perfect style"): clean 3D shapes; brushwork, wear,
  chips and grime painted into each surface's texture; soft, near-real light; each object in its own strong colour.
- **The method that works:** paint one object at a time into its own textures (bake maps, then dry-brush stamps).
  Approved on the danfo: "the texture looks very nice now... I like the level of the texture".
- **Ruled out:** stroke noise made in the shader (owner: "less like painterly and more like a pattern... made by a
  computer"; the white chips looked like confetti).
- **Owed to the dress pass:** more detailed models (owner: "we have to make our models a lot better, like a lot
  more detailed... that's a future thing... when we're doing dress work").
- **To work out when the look resumes:** what the owner likes in looks 1 and 2 (below, "Something I can't place").

## 1. The seven-look test (the street corner)

`scene.py` builds one Lagos street corner from the game's own models at real size (`street.blend`). `style.py` and
`style2.py` render it in one of seven looks, as a wide shot, a face (the hawker) and an object (the danfo's nose).
`sheet.py` puts them on one numbered sheet.

| # | Look (file) | What it is |
|---|---|---|
| 1 | Grainy film (`look_film.png`) | Smooth real shading, a cool sky, colour slightly held back, film grain, vignette, warm grade |
| 2 | Painted Lagos (`look_painted.png`) | Smooth shading, a warm sky, colour pushed, a Kuwahara paint filter |
| 3 | Comic ink (`look_comic.png`) | |
| 4 | Poster colour (`look_poster.png`) | |
| 5 | Toon-real (`look_toonreal.png`) | |
| 6 | Flat planes (`look_planar.png`) | Made after the owner's second reference picture |
| 7 | Painterly faceted (`look_faceted.png`) | Made after the owner's Olise picture |

Settings for 1 and 2 are read from `style.py`; 3 to 7 are not described here (read `style.py`). Face and object
versions are `face_*.png` and `object_*.png`; the sheets are `sheet_wide/face/object.jpg`. The owner's two
reference pictures for this test are `1d197ac5-image.jpg` and `fac1674b-image.jpg` (not checked which is which).
`16427b52-image.jpg` is another picture the owner sent (not checked what it was for).

**The owner's picks:** 2 Painted Lagos, 7 Painterly faceted and 4 Poster colour, to be mixed into one Gidi look.
7 read "a little bit more low poly", not painted. What is wanted: "that brush type of texture and contrast"; each
thing vibrant in its own colour ("the houses are supposed to like have like their own color"); composed like a
photographer's edit, not one filter over everything. Spider-Man's look is loved but not to be copied.

## 2. Gidi look v1 to v4 (the street corner)

- **v1** (`gidi.py`; `gidi_wide/face/object.png`): the light broken by a stroke pattern into hard bands, each stroke
  a slightly different colour, colour pushed per object (skin gentler), lavender shadows, a golden sun, haze, a face
  light for close-ups. Research: brushed-shading and oil-paint shaders bend the light through a stroke map; Arcane
  paints its strokes into textures. By eye: the brush texture shows, but it read as camouflage on the danfo.
- **v2** (`gidi2.py`; `gidi2_*.png`), after the five reference pictures: soft sun and sky fill, two stroke layers
  in each surface's colour, grime toward the ground. By eye: the light and faces read well, but the strokes are too
  fine and faint to read as painted, and there is no edge wear.
- **v3, v4** (`gidi3.py`, `gidi4.py`; `gidi3_*`, `gidi4_*`, `gidi4b_object.png`): bolder stroke noise; v4 adds chips
  on hard edges from an edge map (`edges.py`: Blender's Dirty Vertex Colors, convex edges bright, corners dark).
  **Rejected by the owner** (the quote at the top). This is what made the method change to painting each object.

The owner's five "perfect style" pictures are in `refs-perfect-style/` (9 files: the Olise poster, diner bottles,
Atomic Heart sauce bottles and cans, a fridge with a TV and stickers, jerry cans, barrels and cones, the Ludia
alley, motel door 106; 6867 and 6871 are the same bottles). For study, never copied into Gidi.

## 3. The painted danfo (`painted-danfo/`)

How stylized props are textured in the industry (80.lv breakdowns): a base fill, paint layers per part, edge wear
through a mask, grunge passes, usually in Substance Painter. Blender has no curvature bake; bevel and ambient
occlusion bakes stand in (BlenderNation, StraySpark).

1. `bake.py` (on `~/gidi-game/Art/Vehicles/DanfoBuilt/danfo_r01.blend`): gives each painted part its own UV layout
   and bakes four maps: edges, corners and creases (ambient occlusion), height, and paint colour with a mask.
2. `paint2.py`, the approved painter: dry-brush stamps studied from the reference pictures. Square-ended strokes
   with bristle lines and ragged ends. The colour shifts rather than the brightness (darker = deeper and richer,
   lighter = paler and greyer). Many short thin streaks straight down, a few wide smears across, big calm areas
   left alone. Soft runs from under ledges, dust smeared low down, and torn chips only on edges, showing a pale
   layer with a thin dark line under them. (`paint.py` was v1, which the owner called weird artifacts.)
3. `turn.py`: renders the danfo turning (front, side, rear) in the look's sun and sky. `arch.py` renders the wheel
   arch close up; `liner.py` bakes the arch-liner mask.

Renders: `turn_*` (painter v1), `turn2_*` (v2, approved), `turn3_*` and `turn4_*` (colour and glass fixes). The
`study/` folder holds the crops of the reference pictures the brushes were studied from.

**Found on the way:**
- Blender's AgX colour setting greyed the colours; the "Standard" setting keeps them strong.
- The grainy windows came from a dithered see-through glass. Smooth glass (blended, dark blue-green, painted light
  streaks) fixed it in the test; Unreal has its own glass material.
- The arches showed the seats and floor because the danfo had no wheel wells. Fixed in the builder, in gidi-game
  #107: all thirteen danfos rebuilt with wells.

## 4. The painted keke (`painted-keke/`)

The same scripts on `~/gidi-game/Art/Vehicles/KekeBuilt/keke_parts.blend`. The change that turns them into a recipe:
each part's texture size comes from its surface area (about 400 pixels a metre, 256 to 2048), and the brush is
scaled so the strokes are the same size in metres as on the danfo's body (`<part>_k.txt` beside the maps).

**Found:**
- In full sun the keke's lemon yellow clipped: 74% of the side panel at full brightness, which hid the strokes. At
  −0.5 exposure, 0% (`kturn_*_ev.png`, `keke_sheet.jpg`). Whether to lower the exposure or paint bright colours a
  shade deeper is the owner's call.
- By eye: the wear reads lighter than on the danfo, and on the curved side of the keke's back body the streaks run
  slanted, not straight down (not yet traced to the height map or the UV layout).

## 5. Something I can't place (29 Oct, late)

The owner, looking at the street render again (saved as `owner-liked-29oct-street.jpg`; by eye it is look 1,
Grainy film; the owner: "probably one of the first 2"): "there's something I like about them that I can't quite
place just yet... When we further develop our own look later we will find out what stands out to me."

Measured on that picture: average saturation 32%; the brightest part about 83% (211 of 255), so nothing is pure
white; warm all over (average red 127, green 113, blue 95); grain; soft light with clear shadows. That is the
opposite of the keke's clipped yellow. One idea to try, not decided: the painted textures on the objects with a
grade like this over the whole picture.

## Still open

- When the look resumes: what stands out in looks 1 and 2; the keke's slanted streaks; bright colours kept under
  clipping; then the next objects (a wall, the red generator, a drum). Turn the painter into a gidi-game tool once
  two or three objects pass.
- More detailed models in the dress pass.
- The chosen look written into `decisions/DECISIONS.md`, rebuilt in Unreal as its own materials and post-process
  (Blender's shader maths does not carry over), and measured there. The owner asked for 30 fps on 8 GB; this Mac
  reports 16 GB, so which machine is meant is still to ask.

## Re-running

- Street corner: `blender -b --factory-startup -P scene.py -- street.blend`, then
  `blender -b street.blend -P style2.py -- <look> <out.png> [wide|face|object]` or
  `blender -b street.blend -P gidi4.py -- <out.png> [wide|face|object]`.
- A painted object: `blender -b <model.blend> -P bake.py -- maps`, then
  `~/.venvs/gidi/bin/python paint2.py maps painted 7`, then `blender -b maps/uv.blend -P turn.py -- painted <prefix>`
  (run from the object's folder; the keke's copies carry the area-based sizes).
- Not checked: `p0_*`, `p1/`, `preview.py`, `probe.py` and `inv.py` are earlier working files from the same night,
  not described here.
