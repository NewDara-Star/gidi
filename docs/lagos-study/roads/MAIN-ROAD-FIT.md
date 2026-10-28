# Do the drawn districts sit on the real main roads? (28 Oct)

The owner (28 Oct): lay the roads of the whole of Gidi first, main roads and bridges, "very, very sure that we get
it correctly", then go district by district so each district joins them; "if the stuff I've done earlier is correct,
all our districts that we have done already, their roads should line up to the new roads now perfectly". Before that
layer is drawn, `scripts/main_road_fit.py` measures how the 11 drawn districts' roads sit on the real main roads
today: Overture's motorway, trunk, primary and secondary lines (OpenStreetMap's) in the Gidi frame, sampled every 3 m
inside each outline, each sample "on" when it falls on one of our roads' paved width (plus 1 m).

| District | Real main road inside (km Gidi) | On our roads | Median miss of the off samples | Stretches of 30 m+ with no road (total) |
|---|---|---|---|---|
| d09 | 10.85 | 99% | 5.2 m | 1 (51 m) |
| d12 | 5.24 | 90% | 7.5 m | 9 (375 m) |
| d13 | 7.53 | 87% | 11.6 m | 10 (435 m) |
| d14 | 5.70 | 65% | 97.4 m | 22 (1,152 m) |
| d15 | 13.77 | 96% | 17.6 m | 5 (231 m) |
| d16 | 5.93 | 59% | 23.3 m | 26 (2,139 m) |
| d17 | 5.26 | 97% | 10.6 m | 1 (36 m) |
| d18 | 1.08 | 96% | 6.4 m | 0 |
| d19 | 0.28 | 74% | 7.3 m | 1 (42 m) |
| d27 | 10.46 | 94% | 8.6 m | 6 (306 m) |
| d28 | 11.77 | 93% | 8.6 m | 6 (288 m) |

What it says: seven districts sit on the real main roads for 90% or more of their length; d13 is at 87%; d14,
d16 and d19 do not. d16's motorway is only 7% on: its biggest stretches (around Gidi 14310,7470, real 6.48573,
3.39301) are the Third Mainland Bridge and its interchange at Ebute Metta, read on Google's satellite at z17 (28 Oct,
by eye): an elevated expressway with ramps over the water, which our map does not have. d14's misses (Gidi
11700-11900, 6600-7200) are not looked at yet.

How far to trust the measure: a control moved every real line sideways and re-ran the fit. d09 fell from 99% on to
88% at 10 m and 65% at 30 m; d15 from 96% to 85% and 37%. So the measure tells a 10 m miss from a fit, but on wide
roads and in dense networks a line some metres off still lands on some road, so the "on" share is lenient; the
listed stretches are the useful part, each to be read on Google before it is called a gap. Overture's lines are
OpenStreetMap mappers' work and thin in Lagos; where Google Maps shows a road they lack, that is not caught here.

What follows (NOW 16 m): the city road layer, drawn once for the whole map from the real lines and read on Google,
with every bridge and flyover's height; then each district's roads measured against it, the layer winning.

Checked: the script run on all 11 districts (the table is its output); the shift control run on d09 and d15 at 0, 10
and 30 m; one d16 stretch read on Google satellite by eye. Not checked: every other stretch; whether Overture is
right where it disagrees with us; widths (Overture has few).
