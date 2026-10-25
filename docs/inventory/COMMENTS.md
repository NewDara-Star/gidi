# Comments that name what does not exist

Made by `scripts/inventory.py` with `scripts/code_graph.py`. Every comment and docstring in the three repos is read for the code names it mentions (`backticked` words, snake_case, camelCase, name()); each must exist as a name in the code, a file, a map schema field or a record key. These do not: the comment is out of date, has a typo, or names something outside the repos (a Blender or Unreal API, a library), which is fine and can be read past. 14 comments in 12 files.

## `gidi-data:research/google/kits/old-town/tests/ot149/tone.py`
- line 1: `old_hex`. "Measure a wall's colour in the Street View and in the render over the same box (SV pixels; the render is scaled"

## `gidi-data:research/google/kits/old-town/tools/part_view.py`
- line 1: `half_length`, `half_width`. "Render kit parts alone (outside the repo; a test tool)."

## `gidi-game:tools/junction_geo.py`
- line 1: `minArcRadius`. "Where roads meet: each junction's shape and where each road stops short of it. Plain Python (no Blender), read by the"

## `gidi-game:tools/lettering.py`
- line 1: `fontTools`. "Lettering laid out for a sticker: ~/.venvs/gidi/bin/python tools/lettering.py <font.ttf> <text> <cap metres> <arc radius or 0>"

## `gidi:legacy/blender/gidi_kit/parts.py`
- line 166: `window_spec`. "A window on a wall frame F at (u along, z centre height). spec from rules.window_spec."

## `gidi:scripts/code_graph.py`
- line 1: `backticked`, `snake_case`, `camelCase`. "The code graph, for scripts/inventory.py (owner, 24 Oct: "use the compiler to know what every single piece of code,"
- line 280: `backticked`. "# `backticked`: each name in it"

## `gidi:scripts/draft_roads.py`
- line 1: `arXiv`. "A district's first draft of each road's surface, width, kerbs, drains and verges, from Street View readings by hand."

## `gidi:scripts/js_symbols.mjs`
- line 12: `constructor`. "// no prototype: a name like `constructor` is a name"
- line 32: `let`. "// functions held in a const, and constants at the top of the file (a nested `let` is a local, not a piece of code)"

## `gidi:scripts/surfaces.py`
- line 69: `is_open`. "zones: {district: [(polygon, is_open)]} from the generated files' fabric zones (optional)."

## `gidi:scripts/things.py`
- line 283: `street_art_sites`. "# murals and billboards (street_art_sites)"

## `gidi:scripts/walknet.py`
- line 87: `node_a`, `dist_a`, `node_b`, `dist_b`. "(node_a, dist_a, node_b, dist_b, off): the two ends of the nearest way, how far along it each is, and the step onto it."

## `gidi:web/frame.js`
- line 71: `i_j`. "// "i_j" -> null (loading) | false (none) | Float32Array[] (rings)"

