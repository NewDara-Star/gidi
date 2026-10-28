# Mùṣá square pilot, 28 Oct

The owner (28 Oct): "since you're a machine, you need to find out ways that you would not miss obvious things"; "make
sure the plan actually works in practice... and figure out ways that we can check that the plan actually works".
This is the first trial of the square-by-square survey (DECISIONS "Looking is turned into counting"), on ten squares of
Mùṣá, read by the main session. It is also the start of the answer key: the owner settles these ten, then a helper
reads them blind and its misses are counted against the key.

## The method as run

1. `scripts/square_survey.py d15` cuts the district into squares of 70 m Gidi (210 m real): 250 squares at least half
   inside the outline. `--pick=10` takes ten spread evenly across Google's roof cover (Open Buildings v3 at the
   90%-precision threshold for Lagos's tile, 0.749), so the sparse, middling and dense squares are all in.
2. For each square the script gives the real centre, a Google Maps satellite link at zoom 19, the cover (Google's and
   ours), our counts by record type and a picture of our map there.
3. Each square read in Chrome at zoom 19, never a wider view: four quarter zooms of the 210 m square (each quarter
   about 105 m real on 662 px, nothing shrunk away). Labels were left on after the first square (they give the names;
   the search panel covers only the far left edge, outside the square). Street View where a line was in doubt (one
   square so far: the walled plot on Adefuwa St).
4. The same questions for every square, with "none" as an answer: streets (surface, width class); kerbs, medians,
   drains; walkways and passages; canals, water, rail, bridges; bus stops, lay-bys, motor parks, fuel; walls and
   gates; plots and grounds (yards, car parks, fields, compounds); shop rows; utility and civil compounds; kinds of
   building the map lacks; cover.

At 1:3 a real square holds about nine times our houses, so squares are compared by shares and kinds, never roof by
roof.

## What the ten squares show (main session's readings, by eye, not yet settled by the owner)

| Square | Google / ours cover | Lines the real place has that ours lacks |
|---|---|---|
| d15-0308 Olu Aina St | 48% / 51% | a walled empty plot about 50 x 60 m (Street View: block wall, posters); an open earth drain on Adefuwa St; car-park yards inside blocks |
| d15-1214 Idi-Oro, LUTH side | 14% / 39% | a sports field (S.O.N. field) and a school ground; bush over half the square; a car park; a canal at the edge |
| d15-0913 Ojerinde St | 33% / 46% | the College of Medicine campus edge (a boundary line, a wall by the look); a surface car park about 60 x 50 m |
| d15-1517 Ikorodu Road | 38% / 36% | a walled army compound with sheds and yard; two marks on the road that may be bus stops |
| d15-0405 Ogunmefun St | 42% / 56% | a paved car-park yard with trees; a garden yard inside a block; passages between houses |
| d15-1612 Kadiri St | 44% / 52% | **the railway**: several tracks between walls; ours stops 83 m short (see below); a mosque ground and a school yard |
| d15-1418 Ayilara St | 46% / 57% | a walled church ground with a paved forecourt; two bus stops on the main road; rows of small roofless walled rectangles (not settled) |
| d15-0517 Asoluka St | 49% / 38% | little beyond streets and roofs: the plainest square; a small sandy patch at a junction |
| d15-0406 Sadiku St | 52% / 51% | small courtyards in compounds; a car yard on Sadiku St (not settled) |
| d15-0203 industrial north-west | 75% / 64% | factory compounds with yards, a row of parked lorries, a large open yard; a dark line between sheds (drain or gap, not settled) |

In nine of the ten squares the real place has a line ours lacks; in seven it is a ground or walled plot (our map has
one plot across the ten). Mùṣá's cover passes for the whole district, but square by square it is off: ours is 2.8x
Google's at d15-1214 and short by 11 points at d15-0517 and d15-0203. The Google look (`docs/lagos-study/google/d15.md`)
had already named LUTH as ward blocks in lawns and four open grounds drawn as houses; these squares agree.

**The railway gap.** Our rail record (`rl-u7rtwbrj`) runs from Gidi (12999,5378) to (13246,5994). Overture's three
standard-gauge segments run on inside the outline to about y 6260 and leave it at the east edge (x about 13350): about
290 m Gidi of the railway, with its walls, is missing inside Mùṣá. No check caught it: `working_bar.py` has no rail row.
The fix is a hand edit (owed, NOW 16 k), and a rail row in the line checks.

## Not settled (for the owner, or Street View)

1. d15-1418: the rows of small roofless walled rectangles by Ithadu-L-Islam: a burial ground or roofless stalls?
2. d15-1517: the two round marks on Ikorodu Road: bus stops or lay-bys?
3. d15-0913: the boundary between the town and the campus: a wall?
4. d15-0913: the long green strip beside Ojerinde St: a drain, a verge or a planted strip?
5. d15-0406: the cars packed on Sadiku St: a dealer's yard?
6. d15-0203: the dark line between the sheds: a drain or a gap?
7. d15-0308: the small boxes on the Olu Aina St verge: kiosks or containers?

## What the trial taught about the method

- Quarter zooms show what the full view hid: rows of lorries, walls round plots, the rail's walls, passages.
- Labels came back on when the page reloaded; the method now says so instead of assuming they are off.
- A script found what the eye could not settle: the rail's real length inside the outline.
- Each square took about five minutes of reading; 250 squares is about 20 hours for Mùṣá alone. Helpers (one per
  group of squares, blind pairs) are the way to scale it, once their miss rate on the answer key is known.

## Checked

Re-run: `scripts/square_survey.py d15` (250 squares) and `--pick=10` (the ten squares, their cover figures and counts
as in the table); the Overture rail lengths inside the outline (866, 902, 866 m Gidi, to y 6260) and our rail's points,
by a script run in the session. Looked at: the ten squares in Chrome, four quarter zooms each, by eye; one Street View
(2 Adefuwa St, July 2021). Not checked: every reading in the table is the main session's, by eye, and not yet
settled by the owner; the seven items above; no second reader yet.
