# Mùṣá (district 15): the road plan and where each street comes from

Roads only, drawn on the new frame (1:3). Every kept street sits on its real line, squeezed to the frame, at its real width (never shrunk). Real names live here only, never in the map. Buildings come later.

## Count

- Real streets inside the border (Overture study, rail left out): about **658**: 15 skeleton roads (expressways, trunk, mains), 145 named local streets, and about 498 unnamed street pieces longer than 30 Gidi m (1396 pieces in all). 212.6 km of real street, 70.9 km at Gidi scale.
- Kept (22 Oct): **62 streets in 64 records**; after the owner's calls (23 Oct): 56 streets in 59 road records, plus a rail, a station and the market (the expressway and Western Avenue are each two records that start at an inside junction, so their first point lies in the district), 17.8 km. That is about 1 in 11 of the real streets: every skeleton road, every main, and about 40 local streets kept for life, kit tests and links.
- Kinds: 6 motorway records, 1 trunk, 11 main roads, 12 local mains, 5 market streets, 27 home streets, 2 lanes.
- Values: only what was seen. Widths measured on Google satellite at z19 (17 records) or taken from the kit shots; surfaces, kerbs, medians and drains from the kit Street View shots (ot numbers). Everything else is left missing, so the board shows it amber (needs a value). check_map has no red: it passes, and every field left missing is counted on its TODO line.

## Defining places and the streets that carry them

- **Ojuwoye / Mushin market core** (east of the Agege Motor Road at the Isolo Road junction): m01, m06, s03 (Dada Iyalode), s04 (Oguntoye), s02 (Post Office Road).
- **Ladipo spare parts market**: the whole market is in Mùṣá (owner, 23 Oct: the border moved north-west to take it from Isolo-Ladipo, 30). m07 (Ladipo Street, now on its real line through the market to the expressway), the market lane, the market's place record (its real outline), s01 (Ayantuga, west end).
- **Palm Avenue timber market**: m08.
- **Daleko market** at the Isolo Road / expressway corner: m06, s39.
- **Mushin General Hospital** side, between Palm Avenue and Isolo Road: s38.
- **LUTH and the College of Medicine, Idi-Araba**: m10 (Ishaga Road, the gate road), m26 (Apesin, the spine from the Agege Motor Road), s11 (Ajegunle market lane), s14 (Bello).
- **Eko Boys High School**: s10 (Martins), s07 (Ogungbaiye), s12 (Laniyan), s13 (Folami).
- **Bishop Aggey field**: s15, s16 (Olayiwola Liasu, Ilasamaja).
- **Mushin station and the rail**: the rail record (the real line for the district's stretch) and the station record at the real station point (its area and platform are placeholders to draw from Google Earth); m18 (Olateju), m15/m15b (Kayode Street and the flyover over the rail).
- **Idi-Oro junction** (Agege Motor Road meets Ikorodu Road and Western Avenue): m01, m04b, m05a, m25 (Bishop Fashoro).
- **Motor park at the Agege Motor Road / Isolo Road junction**: m01, m06 (the park itself is a place for later).
- **Idi-Araba canal**: no road; the south edge in the west follows it. s17 (Abeokuta) runs down to it.

## The owner's calls (23 Oct)

- **The south lobe went to Surulere** (13). The cut follows Itire Road (m11), which stays in Mùṣá as its south edge, with the Ojuelegba link (m14) to Western Avenue. The real Idi-Araba canal runs further north (its bridges: Abeokuta Street, Mushin Road, Ishaga Road, Ikorodu Road, about y 6250 to 6370), so Idi-Araba and LUTH stay in Mùṣá; the lobe's streets are south of Itire Road.
- **Ladipo market is all in Mùṣá:** the border moved north-west to the expressway and the market's north end.
- **Edge roads** belong to the district on the side where the road's life is; the neighbour joins onto them. The expressway's west service road lives on the Isolo side, so Isolo-Ladipo (30) draws it.
- **Rail and stations** have record types now (`rail`, `station`, MAP-FORMAT section 2).
- **Service roads are their own streets** (`service_road`). The expressway's 41 m corridor is split into 25 m of carriageways and median plus a 7 m service road each side (estimate: check on z19). Streets that met the expressway now meet its east service road; Isolo Road still meets the carriageway (it crosses on a bridge, an interchange to draw later). Western Avenue's side road is not split yet: which side it runs is still to be seen.

## Kept streets

| Gidi id | key | real street | kind | width | why kept | values seen |
|---|---|---|---|---|---|---|
| rd-kxa8hz1b | m01 | Agege Motor Road | trunk | 21.5 | the trunk through Mushin; crosses the north edge (Ilupeju) and ends at Idi-Oro on Ikorodu Road | ot64: kerbed median with black-and-white stripes; width z19 at 6.53379,3.35349: two carriageways and the median |
| rd-qc8rcv8v | m02a | Oshodi-Apapa Expressway | motorway | 25.0 | the west edge (Isolo-Ladipo beyond); seam | width z19 at 6.52569,3.33561: both carriageways and both service roads, one corridor |
| rd-cjk9hvop | m02b | Oshodi-Apapa Expressway | motorway | 25.0 | the west edge (Isolo-Ladipo beyond); seam | width z19 at 6.52569,3.33561: both carriageways and both service roads, one corridor |
| rd-3079cryq | m04 | Ikorodu Road | motorway | 40.0 | the east edge (Yaba and Shomolu beyond); seam | width z19 at 6.52835,3.36743: both carriageways and the BRT lanes |
| rd-i4klmw3w | m04b | Ikorodu Road (Idi-Oro bend) | motorway | 40.0 | Ikorodu Road bending into Western Avenue at Idi-Oro; seam | width as m04 |
| rd-avaupyki | m05a | Western Avenue | motorway | 35.0 | the south-east edge (Yaba, Surulere beyond); seam | width z19 at 6.50798,3.36336: both carriageways and the side road |
| rd-cb2h4xa5 | m06 | Isolo Road | main_road | 16.0 | the main road west to the expressway; Daleko market on it | z19 satellite 06 (16 m kerb to kerb); ot87/ot88 jersey barrier |
| rd-og05m8ig | m07 | Ladipo Street | main_road | missing | the spare-parts market's street: from the expressway's east service road through the market, then south-east to the Agege Motor Road | ot45 (Ladipo St, just over the edge): low concrete median, worn tar |
| rd-htzqbqr8 | m08 | Palm Avenue | main_road | 11.5 | the timber market street (ot146); Isolo Road to Agege Motor Road and on | ot146: wide tar, earth edges, no kerb; width z19 at 6.53696,3.35144 |
| rd-aqj6lgu3 | m09 | Mushin Road (Idi-Araba side) | main_road | 9.0 | skeleton: Isolo Road south past Ishaga Road to Itire | width z19 at 6.52155,3.34725 |
| rd-ulqkx258 | m10 | Ishaga Road | main_road | 13.5 | skeleton: the Idi-Araba (LUTH) road; median and lamps (ot176) | ot176: two lanes, low concrete median; width z19 at 6.51817,3.35224, with the median |
| rd-r3kcqjjf | m11 | Itire Road | main_road | 13.0 | skeleton: Itire side east to Ojuelegba | width z19 at 6.51210,3.35752 |
| rd-nz39jh82 | m14 | Ojuelegba Road (piece inside) | main_road | missing | skeleton: Itire Road on to Ojuelegba under Western Avenue | none yet |
| rd-wh8bgje0 | m15 | Kayode Street | main_road | missing | skeleton: Ikorodu Road over the rail into Mushin | none yet |
| rd-3bmlmvqc | m15b | Mushin Flyover Bridge | main_road | missing | the flyover over the rail: Kayode Street to Ogunmokun and Coker | none yet |
| rd-8odjq68t | m16 | Majolate Street | local_main | missing | skeleton (secondary) on the north-east edge | none yet |
| rd-ug65yhy2 | m17 | Ilupeju Road | main_road | missing | crosses into Ilupeju (north-east lobe); ot86 | none yet |
| rd-3g52z5ck | m18 | Olateju Street | local_main | 8.5 | main street beside the rail; Mushin station; ot24 | ot24: tar with broad sand shoulders; width z19 at 6.53502,3.35908 |
| rd-9wkc2te6 | m19 | Coker Road | local_main | 8.0 | main street; ot151 | ot151: worn tar about 8 m, earth edges |
| rd-nl2ol8e2 | m20 | Sokunbi Street | local_main | missing | main street north of Ayantuga | none yet |
| rd-90g2sje2 | m21 | Akanro Street | local_main | 8.5 | the west cross street: expressway to Mushin Road | width z19 at 6.52095,3.34122 |
| rd-qy07dnq8 | m22 | Adeoyo Street | local_main | missing | the west spine, Isolo Road south; ot62 | none yet |
| rd-76xj78h3 | m25 | Bishop Fashoro Street | local_main | missing | Idi-Oro spine from Agege Motor Road | none yet |
| rd-roqq0v3w | m26 | Apesin Street on to the LUTH gate | local_main | missing | Idi-Araba spine: Agege Motor Road to the hospital and on to Ishaga Road | none yet |
| rd-zwt7kfiu | m27 | Paul Okuntola Street | local_main | missing | the long link from the Mushin junction to Ishaga Road | none yet |
| rd-qqm8wpxb | m02c | Oshodi-Apapa Expressway, east service road (north) | service_road | 7.0 | the slow road beside the expressway, where streets join it (owner, 23 Oct) | split from the 41 m z19 corridor: check |
| rd-sdso0qxv | m02d | Oshodi-Apapa Expressway, east service road (south) | service_road | 7.0 | as m02c, south of the inside junction | as m02c |
| rd-cbrqj76p | s40 | Alhaji Akinwunmi Street (Ladipo market) | market_street | missing | a lane into the market off Ladipo Street | none yet |
| rd-sfzm9yds | s01 | Ayantuga Street | market_street | 9.0 | kit test ot149; corner shops, kiosks, cage stalls | ot149 kit test (Ayantuga St) |
| rd-rqewtwxy | s02 | Post Office Road | home_street | missing | NIPOST; links Agege Motor Road to Coker Road | none yet |
| rd-d4z92y9r | s03 | Dada Iyalode Street (Ojuwoye market) | market_street | missing | the busy market core (ot08, ot126) | ot08/ot126: broken, puddled earth street in the market core |
| rd-xafls8id | s04 | Oguntoye Street | market_street | missing | market street of plank and zinc kiosks (ot07, ot127) | ot07/ot127: sandy unpaved market street |
| rd-yfxvt7jz | s06 | Alasalat Street | lane | missing | bungalow lane, sand and red earth (ot25) | ot25: sand and red-earth lane, no kerb |
| rd-d929n8kd | s07 | Ogungbaiye Street | home_street | missing | home street (ot89); links Paul Okuntola to Idi-Oro | none yet |
| rd-vlz0dge8 | s08 | Abibu Street | home_street | missing | open drains with slab bridges (ot06, ot125) | ot06/ot125: open concrete drains both sides, slab bridges, worn tar into sand |
| rd-0bb0jt00 | s10 | Martins Street | home_street | missing | to Eko Boys High School | none yet |
| rd-oq1a8vtd | s11 | Ajegunle Street (Idi-Araba) | market_street | missing | market lane with the mosque (ot63) | ot63: narrow dark tar strip, market lane |
| rd-345rcotj | s12 | Laniyan Street | lane | missing | shack row by Eko Boys (ot141) | ot141: muddy earth road, puddles, no drain |
| rd-y3099jnt | s13 | Folami Street | home_street | missing | gated plots, mosque (ot61); Laniyan to Agege Motor Road | none yet |
| rd-afuo4fxw | s14 | Bello Street | home_street | missing | Idi-Araba side street (ot23) | ot23: grey tar, no kerb |
| rd-353wkzd5 | s15 | Olayiwola Liasu Street (with Sadiku Street west) | home_street | 7.0 | kit test ot175; expressway to Ilasamaja Road | ot175: tar about 7 m, earth edges |
| rd-c77w49vw | s16 | Ilasamaja Road | local_main | missing | the old Ilasamaja road past Bishop Aggey field to Mushin Road | none yet |
| rd-lmd6wbjh | s17 | Abeokuta Street | home_street | missing | the west N-S street down to the canal | none yet |
| rd-gj6642yg | s18 | Ayuba Daudu Street | home_street | missing | south of Akanro; links Abeokuta to the canal side | none yet |
| rd-b9jn4qv9 | s19 | Olushoga Street | home_street | missing | workshop sheds (ot174) | ot174: sandy earth, no kerb, no drain |
| rd-9o8evlkl | s20 | Omowunmi Street | home_street | missing | school and vulcaniser off Isolo Road (ot05, ot124) | ot05/ot124: sandy earth, no tar, open drain with slab bridge |
| rd-98o0vo6c | s21 | Olorunsogo Street | home_street | missing | the Olorunsogo quarter, west of Agege Motor Road | none yet |
| rd-n63xdcg0 | s22 | Idera Street | home_street | missing | east of the rail, to Majolate | none yet |
| rd-oahy2qpj | s23 | Adeshiyan Street | home_street | missing | north-east lobe off Ilupeju Road | none yet |
| rd-9g6edwp4 | s24 | Amodu Street | home_street | missing | east of the rail; to Agege Motor Road | none yet |
| rd-f782px4g | s25 | Ogunmokun Street | home_street | missing | Coker to the flyover side | none yet |
| rd-eahkl6c0 | s26 | Alhaji Lasisi Street | home_street | missing | Idi-Oro, by the rail | none yet |
| rd-3c3x0ks3 | s27 | Aborishade Road | home_street | missing | south of the canal | none yet |
| rd-30weiws7 | s28 | Dosunmu Road | home_street | missing | to Falolu and the Itire side | none yet |
| rd-3glzzql1 | s33 | Cole Street | home_street | missing | Ishaga side to Western Avenue | none yet |
| rd-3m6drqc3 | s34 | Atunrase Street | home_street | missing | Ishaga Road to Bishop Fashoro | none yet |
| rd-htzfpp2k | s36 | Onipede Street | home_street | missing | south of the canal | none yet |
| rd-fmvbnpr3 | s38 | Alokolaro Crescent | home_street | missing | crescent between Palm Avenue and Isolo Road | none yet |
| rd-tk3atl5n | s39 | Daleko market road | market_street | missing | Daleko market off Isolo Road | none yet |

Edge roads (the expressway, Ikorodu Road, Western Avenue, Majolate Street, Isolo Road's west end) run along the border, partly over it. They are drawn here along the district's stretch, and end where the neighbour takes over. Roads that cross the border end on it (seams): Agege Motor Road at Ilupeju (north), Ladipo Street and Palm Avenue (north-west), Ikorodu Road (north-east), Itire and Ojuelegba Roads (south-east), Ogunlana Drive and Akerele Road (south), Mushin Road (south-west).

## Dropped streets, by area

Named streets inside the border with more than 30 m of line that are not kept, one per line. On top of these, about 500 unnamed street pieces are dropped: the repeated parallel home streets and closes between the kept ones.

### south of the canal (Itire side, Randle, Akerele, Karimu) (50)

- Abati George Avenue: repeats a kept parallel street nearby
- Abijade Street: repeats a kept parallel street nearby
- Abimbola Shadipe Street: repeats a kept parallel street nearby
- Abina Street: repeats a kept parallel street nearby
- Adebayo Street: repeats a kept parallel street nearby
- Adedoyin Road: repeats a kept parallel street nearby
- Adeniji Street: repeats a kept parallel street nearby
- Akintan Street: repeats a kept parallel street nearby
- Akinyemi Thompson Street: repeats a kept parallel street nearby
- Anjorin Street: repeats a kept parallel street nearby
- Apena Street: repeats a kept parallel street nearby
- Awoyemi Close: repeats a kept parallel street nearby
- Ayilara Street: repeats a kept parallel street nearby
- Babalola Street: repeats a kept parallel street nearby
- Banire Street: repeats a kept parallel street nearby
- Benson Street: repeats a kept parallel street nearby
- Bola Street: repeats a kept parallel street nearby
- Daniyan Street: repeats a kept parallel street nearby
- Durojaiye Street: repeats a kept parallel street nearby
- Durojaiye street: repeats a kept parallel street nearby
- Fasanya Street: repeats a kept parallel street nearby
- Fashina Street: repeats a kept parallel street nearby
- Folarin Street: repeats a kept parallel street nearby
- Gbaja Street: repeats a kept parallel street nearby
- I.K Dairo Street: repeats a kept parallel street nearby
- Ibidun Street: repeats a kept parallel street nearby
- Ishola Street: repeats a kept parallel street nearby
- James Robertson Street: repeats a kept parallel street nearby
- Kasali Street: repeats a kept parallel street nearby
- Lawani Street: repeats a kept parallel street nearby
- Lawanson Road: repeats a kept parallel street nearby
- Mabo Street: repeats a kept parallel street nearby
- Makinde Street: repeats a kept parallel street nearby
- Okeolu Street: repeats a kept parallel street nearby
- Okoh Drive: repeats a kept parallel street nearby
- Olorogun Street: repeats a kept parallel street nearby
- Olufowobi Street: repeats a kept parallel street nearby
- Omobola Street: repeats a kept parallel street nearby
- Omolewa Street: repeats a kept parallel street nearby
- Onasanya Street: repeats a kept parallel street nearby
- Onitolo Street: repeats a kept parallel street nearby
- Oseni Street: repeats a kept parallel street nearby
- Owodele Close: repeats a kept parallel street nearby
- Oyekan Street: repeats a kept parallel street nearby
- Oyenekan Street: repeats a kept parallel street nearby
- Remilekun Road: repeats a kept parallel street nearby
- Salawu Street: repeats a kept parallel street nearby
- Taiwo Way: repeats a kept parallel street nearby
- Taju Thompson Street: repeats a kept parallel street nearby
- Wuraola Street: repeats a kept parallel street nearby

### north (Olorunsogo, Odi-Olowo, Ojuwoye, Palm Avenue) (11)

- Adekunle St: repeats a kept parallel street nearby
- Alhaji Awoyejo Street: repeats a kept parallel street nearby
- Awoyokun St: repeats a kept parallel street nearby
- Fagbile St: repeats a kept parallel street nearby
- Lawanson Crescent: repeats a kept parallel street nearby
- Ogunsanya Street: repeats a kept parallel street nearby
- Olapido Sode St: repeats a kept parallel street nearby
- Omodigbo Street: repeats a kept parallel street nearby
- Sosanya St: repeats a kept parallel street nearby
- Sule Bada St: repeats a kept parallel street nearby
- Tawose St: repeats a kept parallel street nearby

### Idi-Araba and Idi-Oro (17)

- Adeleke Street: repeats a kept parallel street nearby
- Agoro Street: repeats a kept parallel street nearby
- Akinhanmin Street: repeats a kept parallel street nearby
- Akodu Street: repeats a kept parallel street nearby
- Aluko Close: repeats a kept parallel street nearby
- Awoniyi Street: repeats a kept parallel street nearby
- Ayandeji Street: repeats a kept parallel street nearby
- Bakare Street: repeats a kept parallel street nearby
- Buraimoh Street: repeats a kept parallel street nearby
- Cardoso street: repeats a kept parallel street nearby
- Caxton Close: repeats a kept parallel street nearby
- Ikeolu Street: repeats a kept parallel street nearby
- Ogunfunmi Street: repeats a kept parallel street nearby
- Ogunjobi Street: repeats a kept parallel street nearby
- Ojerinde Street: repeats a kept parallel street nearby
- Onifade street: repeats a kept parallel street nearby
- Thani-Olodo Street: repeats a kept parallel street nearby

### north-west (Isolo Road, Daleko, Mushin hospital) (3)

- Akinyemi Crescent: repeats a kept parallel street nearby
- Araromi Street: repeats a kept parallel street nearby
- Layi Oyekanmi Street: repeats a kept parallel street nearby

### middle-west (Akanro, Ilasamaja, Bishop Aggey) (9)

- Apapa-Oworonshoki Expressway: repeats a kept parallel street nearby
- Gbolahan Street: repeats a kept parallel street nearby
- Igbehinadun Street: repeats a kept parallel street nearby
- Ishaga Close: repeats a kept parallel street nearby
- Morgan Street: repeats a kept parallel street nearby
- Odubiyi Street: repeats a kept parallel street nearby
- Omosolape Street: repeats a kept parallel street nearby
- Shittu Street: repeats a kept parallel street nearby
- Technical Street: repeats a kept parallel street nearby

Dropped on purpose from the first draft: Odulana Street (its line could not be told apart from the market lanes by the Agege Motor Road; the market is carried by Oguntoye and Dada Iyalode), Iyalla Street (it is the west end of Ayantuga on the real line), Olyide Street (could not be placed for sure; s38 carries the hospital side), the expressway's east service road (inside the expressway record's 41 m), Lawanson Road and Herbert Macaulay Way (almost all outside: Itire-Lawanson and Yaba draw them).

## Given to Surulere (13), 23 Oct

These were drawn here and left the district with the south lobe. Surulere takes them when it is drawn.

| Gidi id | key | real street | kind | width | why kept | values seen |
|---|---|---|---|---|---|---|
| rd-urhrpqbl | m05b | Western Avenue | motorway | 35.0 | the south-east edge (Yaba, Surulere beyond); seam | width z19 at 6.50798,3.36336: both carriageways and the side road |
| rd-qxdyk8w6 | m13 | Ogunlana Drive (piece inside) | main_road | missing | skeleton seam with Surulere | none yet |
| rd-rru8n6n2 | m23 | Randle Avenue | local_main | missing | south main street off Itire Road | none yet |
| rd-s7qbst8a | m24 | Akerele Road | local_main | missing | south main street (Surulere side) | none yet |
| rd-rxxu7366 | s29 | Falolu Road | home_street | missing | south lobe N-S | none yet |
| rd-3fomj9ap | s30 | Bishop Crowther Street | home_street | missing | south lobe E-W, Falolu to Randle | none yet |
| rd-6zdeymgc | s31 | Karimu Street | home_street | missing | the long south-east street | none yet |
| rd-pp320oeu | s32 | Clegg Street | home_street | missing | south-east to Western Avenue | none yet |

## Lanes drawn by hand (23 Oct, owner: "lanes on dropped streets")

Drawn from the Google study of each block's real twin (satellite at the twin spot, real = 3 x Gidi from the frame's
corner); only the pattern is taken (direction, spacing, where the streets begin and end), never Google's lines. Values
are left missing (amber) like every street not yet measured.

**Block B1** (between the expressway's east service road, Ladipo Street, Palm Avenue and Isolo Road). Redrawn 23 Oct
from a close-zoom study (owner: zoom in for the details): the first lanes were offsets from Ladipo Street read at z16 and
missed the real grid. The real twin is two places: a warehouse strip along the expressway (big sheds and yards) west of
Alhaji Akinwunmi and Alhaji Amusa Streets, and the dense Ladipo-Odunsi grid east of them. The grid fans out from the
Akinwunmi/Ladipo apex: its long streets (Oloruntoyin-Okesanya, Olapeju-Olasonde, Osoro-Shotinoye, then Ikale, Oremeji,
Aladesuru) run south-south-east, crossed by Oloje, Ojekunle, Jumoke Way and Sebanjo; south of Jumoke the streets turn
(Awanatu, Sadiku, Omoleran north-north-east; Dada and Akinbayode east). Each lane below lies on its real street's line;
about one real street in two is kept, 35-55 m apart, so two rows of real-size houses stand between them. Alhaji
Akinwunmi joins its kept stretch at the Ladipo market (rd-cbrqj76p).

| Gidi id | real twin | kind | from, to |
|---|---|---|---|
| rd-wwc5xw6r | Alhaji Akinwunmi Street | home_street | its market stretch to Bello Street (the strip's east edge) |
| rd-leh07psm | Bello Street | home_street | the expressway's east service road to the Olanibi bus stop |
| rd-jq923w3v | Bello Street's east end, past Omoba Foods | lane | Akinwunmi's corner to Oloje Street |
| rd-oe3ndnqj | Alhaji Amusa Street | home_street | Bello Street to Isolo Road |
| rd-vt757j5a | Olanibi Street | local_main | the bus stop to Isolo Road |
| rd-zvenwhp0 | Ojekunle Street (Fatai Atere Way's west leg) | local_main | the Olanibi bus stop to Ladipo Street |
| rd-wizltkz5 | Oloruntoyin Street, then Okesanya Street | lane | Akinwunmi to Sebanjo Street |
| rd-ua9h579y | Osoro Street, then Shotinoye Street | lane | Akinwunmi's market stretch to Sebanjo Street |
| rd-t0f428b6 | Odushina Street | lane | Akinwunmi to Oloje Street |
| rd-q1xvtu3t | Oloje Street | lane | Bello's east end to Osoro Street |
| rd-nec7uo7x | Jumoke Way | lane | the Jakande street to Shotinoye Street |
| rd-j54ymnoy | Ogunmefun Street | lane | Jumoke Way to Oremeji Street |
| rd-bg3ujvct | Oremeji Street | lane | Ogunmefun Street to Sebanjo's west end |
| rd-pz8kfbdt | Sebanjo Street | lane | Ladipo Street to Oremeji Street |
| rd-7g32eziy | the street from the Olanibi bus stop past Jakande Plaza | lane | the bus stop to Sebanjo's west end (Kingdom Against Kingdom) |
| rd-dboedcs1 | Awanatu Street | lane | the Jakande street to Akinbayode Street |
| rd-fxei4ynh | Dada Street | lane | Awanatu Street to Sadiku Street |
| rd-03o2r4u5 | Sadiku Street | lane | the Jakande street to Akinbayode Street |
| rd-c5n44yad | Omoleran Street | lane | the Jakande street to Isolo Road |
| rd-ve4qwm14 | Akinbayode Street | lane | Olanibi Street to Omoleran Street |

**Block B0** (Ishaga Road, Bishop Fashoro Street, the Agege Motor Road edge, Ajegunle and Atunrase Streets). Redrawn 23 Oct from a close-zoom study (z18, shot scale checked against known roads; owner: zoom in for the details): the first nine lanes were read at z16 and missed most of the real streets. The real twin is Idi-Araba: the LUTH campus with the College of Medicine and its staff quarters (Roads 1, 4, 6 and 8, the long drive, the canal road), Eko Boys and Birch Freeman High Schools, and the dense housing round it: the Olaniyi-Alao Adegboyega streets north-east, the Takuro-Ojerinde-Kajola grid west of the campus, Cardoso-Omoniyi-Martins south, Lawani-Ogunfunmi-Akobi over the canal. Each lane lies on its real street's line; real dead ends are kept as dead ends. Left out for spacing or because the boundary road already carries them: Kobiti (too close to Bishop Street), Owokoniran Close, Abibu and Akodu west, Kusey, Arogbe, Kelani, Ojitoju, Akintola, Owodele, Obanimola, Ewumi, Karimu, and the stream path (it is Atunrase Street, the edge). Removed: the nine z16 lanes rd-d68pbjgh, rd-g9taxf2k, rd-g6v156jj, rd-w0uqy2s9, rd-erfcf0tx, rd-8xdqzq9d, rd-phi8eic8, rd-jm7fmw8p, rd-9ozcrkqs.

| Gidi id | real twin | kind | note |
|---|---|---|---|
| rd-7uajwuxt | Owokoniran Street | lane |  |
| rd-su4tdfqc | Eniola Street, then Akobi Crescent over the canal | lane |  |
| rd-ht4h23eq | Bankole Street, then Akintulu Street | lane | real dead end at its west end |
| rd-ycxjs88t | Olaniyi Street, then Matuwo Street | local_main | crosses the Agege Motor Road to its far side (rd-et552uc8) |
| rd-odaola3x | Rev. Asekun Lane | lane | real dead end |
| rd-ukrlud0u | the bending street from Olaniyi down to Alao Adegboyega | lane |  |
| rd-xwiedrw2 | Alao Adegboyega Street | lane | real dead end at its west end |
| rd-8mm4jnop | Fasoro Lane | lane |  |
| rd-yp7rd186 | LUTH's long drive | service_road | joins Fagbenro Street |
| rd-gtkm5cxg | Fagbenro Street | lane |  |
| rd-y7rfqvf1 | Akinola Street, then LUTH Road 1 | service_road |  |
| rd-zpb4ffh6 | LUTH Road 1, west | service_road | to Ishaga Road |
| rd-ep3ddbio | LUTH Road 1, east | service_road |  |
| rd-8rjr3ndf | LUTH Road 8 | service_road | real dead end at its west end |
| rd-rpxzoyty | LUTH Road 6, then the staff quarters road | service_road | real dead end at its south end |
| rd-zai52ajf | LUTH's canal road | service_road |  |
| rd-rfra6ops | Takuro Street | lane | joins Ojerinde Street |
| rd-bqhbzj4y | Ojerinde Street | lane |  |
| rd-pp06u4v5 | Wonuola Street | lane |  |
| rd-0udahnvp | Alasalat Street | lane |  |
| rd-ru7lycas | Moshalasi Street | lane |  |
| rd-wzenm1tr | Kajola Street | lane |  |
| rd-1ajcm4xn | Adeyemi Street | lane |  |
| rd-ca5m65kw | Kosobameji Street, then Onifade Street | lane |  |
| rd-ssz6ymgc | Cardoso Street | lane | joins Martins Street |
| rd-trz9qjln | Omoniyi Street | lane |  |
| rd-ixprqj8g | Martins Street's south stretch | lane |  |
| rd-ed2dooh3 | Akodu Street, into the Eko Boys pocket | lane | real dead end at its east end |
| rd-0yuaaxhr | Ogunfunmi Street | lane |  |
| rd-zr9sx05c | Akobi Crescent | lane |  |
| rd-xvy8425r | Lawani Street | lane | joins Ishaga Road |
| rd-8beruwdd | Akin Baruwa Street | lane |  |
| rd-zoczvixp | Atunrase Street's north arm | lane |  |
| rd-w51808dt | LUTH Road 4, then the diagonal past the staff school | service_road | real dead end at its north-east end |
| rd-upzxrowm | Apesin Street | lane |  |
| rd-r444jznj | Agoro Street | lane |  |

**Block B2** (Ishaga Road, the Itire Street and Lawanson Road edges, Aborishade Road, Abati George and Dosunmu Streets, Michael Ogun Street and the Itire-Ishaga junction). Redrawn 23 Oct from a close-zoom study (z18 at the checked shot scale; owner: zoom in for the details): the first seven lanes were read at z16 and missed most of the real streets. The real twin is Idi-Araba south of Ishaga Road and Itire-Lawanson: north of the canal, the Folarin-Oyekanmi grid east of Itire Street and the Garuba Musa-Igbira-Obele streets below the mosque; south of it, Durojaiye and Olufowobi, Omobola running up into Alves Street, the Kasali-Folarin-Ik Daro-Akinyemi Thompson streets down to Lawanson Road, the Adedoyin Road pocket by the Lawanson market, and Durojaiye, Bello, Adeniji and Adebayo Streets east of Michael Ogun. About one real street in two is kept, 40-80 m apart at real size. Streets that end on the district's edge (Itire Street, Lawanson Road) stop there until the seam pass. Left out for spacing: Oyewuwo, Seriki, Haruna, Olawepo, Agbole, Oduwawo, Wuraola, Abijade, Aina, Fashina, Ojikutu, the Lawanson Market lane, Daniyan's south-bank stretch. Removed: the seven z16 lanes rd-i6s2bf4s, rd-a0jvm3x0, rd-uheomc6y, rd-tfs65na7, rd-nybc6644, rd-b9u5qmox, rd-oiymgele.

| Gidi id | real twin | kind |
|---|---|---|
| rd-x5gbmfao | Folarin Street | lane |
| rd-d7mpoq41 | Babalola Street's east end, then Oyekanmi Street | lane |
| rd-bm7zt6yx | the street along the canal's north bank, past Prince Heirs College | lane |
| rd-r9bbqsd1 | Durodola Street | lane |
| rd-3glst27l | Adekunle Street | lane |
| rd-ldpvzbt7 | Abati Street | lane |
| rd-r2lepc3j | Garuba Musa Street | lane |
| rd-lnoqvges | Mallam Gana Street, then the Addide Iwaya street west to Garuba Musa | lane |
| rd-qhwuhayy | the unnamed street between Olawepo Lane and Mallam Gana | lane |
| rd-l3rs3wjs | Igbira Road, then Igbira Street to the canal | lane |
| rd-30966k78 | Obele Road (its east-west stretch, then north to Ishaga Road) | lane |
| rd-laaw1anj | Daniyan Street on the canal's north bank | lane |
| rd-jcfqk5jf | the road past the Chapel of the Healing Cross | lane |
| rd-j817mtxs | Durojaiye Street's north end, then Olufowobi Street | lane |
| rd-ffpzwd6r | Omobola Street, then Alves Street north to Aborishade | home_street |
| rd-psjkkw9f | Oseni Street | lane |
| rd-emmu81lr | Asoluka Street | lane |
| rd-uufgfc7r | Kasali Street | lane |
| rd-ytjvbcdm | Folarin Street (Lawanson) | lane |
| rd-gb8kkto3 | Ik Daro Street | lane |
| rd-9c0gondv | Akinyemi Thompson Street | lane |
| rd-790or58e | Oke Olu Street | lane |
| rd-s40am6tw | Babalola Street (Lawanson) | lane |
| rd-zhn2pif5 | Abati George Street | lane |
| rd-k17bq15t | Adedoyin Road | home_street |
| rd-ls7vi4p6 | Obafemi Ajayi Street | lane |
| rd-nvm72nt7 | Caltos Drive | lane |
| rd-vq96bf9e | Okon Drive | lane |
| rd-3ir5l1tj | Aborishade Road's south end | lane |
| rd-608fssnq | Babashola Street, then Oyenekan Street to the canal | lane |
| rd-8crtp77o | Fasanya Street | lane |
| rd-1uh80t1y | Taju Thompson Drive | lane |
| rd-fp25sdd6 | Durojaiye Street (east), then Adeniji Street | home_street |
| rd-ozs3ry4y | Bello Street | lane |
| rd-i10tsslu | Adeniji Street (north-south) | lane |
| rd-xd115opd | Adebayo Street | lane |

**Block B3** (Ogunmokun Street, the Agege Motor Road, the Ikorodu Road edge and Kayode Street; the rail runs through it). Redrawn 24 Oct from a close-zoom study (six z18 shots at the checked shot scale; owner: zoom in for the details): the first fifteen lanes were read at z16 and missed most of the real streets. The real twin is Fadeyi and Idi-Oro beside Mushin station. East of the rail: Lesi and Lawanson Crescents and Matanmi Street under Kayode, the Giwa-Cole-Adesina-Aiyetoro/Akinola streets crossed by Oluwakemi, Jacob and Ayonuga Streets, then Euba/Haruna, New Balogun, Oyedele, Ereko, Fasanya and the east-west Ayonuga; further south Adewusi, Brown Lane, Kadiri, Ojelade and Lawani Streets to the Ikorodu Road edge, and Bada and Kugbuyi Streets down to Jibowu. West of the rail: the Buraimoh-Igbarere-Imoru-Ojo-Amodu-Oyegunle-Akinbiyi grid by Elegba Festival Drive, Ijaiye, Igbeyin Adun, Ogunsanya, Awoyejo and Adegbite Streets round Mushin Main Market, and Ali, Ashaoku, Anifowoshe, Adedeji and Idumagbo Streets in the corner off the north-south Ogunmokun Street. Streets on the rail side still end at the rail (Smith and Ago-Owu Streets run beside it). Left out for spacing: Smith, Coker (Fadeyi) north end, Alarape, Ogunlobi, Thanni Olodo, Odili, Labinjo, Aileru, Safebirth. Removed: the fifteen z16 lanes rd-mzaial2i, rd-jdq1vk2j, rd-ye8zhvw4, rd-vhulohlp, rd-vx27esql, rd-r5gc47ia, rd-abbx5rnv, rd-70q1fgdg, rd-n2ald4yc, rd-1383lbsh, rd-8fe89b52, rd-h6vwsegj, rd-65shqr4p, rd-iwrs1m4t, rd-et552uc8.

| Gidi id | real twin | kind |
|---|---|---|
| rd-4553yz2m | Lesi Crescent | lane |
| rd-b0xmuid5 | Lawanson Crescent | lane |
| rd-23dgcrr6 | Matanmi Street | lane |
| rd-5f7exkiz | Giwa Street | lane |
| rd-d2h8std9 | Oluwakemi Street | lane |
| rd-fh7ahv9d | the street down to Opeloyeru Street | lane |
| rd-f5ms4r2b | Ago-Owu Street | lane |
| rd-ihiofwck | Cole Street | lane |
| rd-rktb8bj7 | Jacob Street | lane |
| rd-x0nmzqqy | Adesina Street | lane |
| rd-jxc6hu8b | Ayonuga Street (north-south) | lane |
| rd-32ty8fh6 | Akorohunfayo Street | lane |
| rd-h0a9i5fg | Aiyetoro Street, then Akinola Street | lane |
| rd-67sg60rp | Euba Street, then Haruna Street | lane |
| rd-wt3bztea | Enilola Lane, then Aridagbe Street | lane |
| rd-habxxo75 | New Balogun Street | lane |
| rd-c6x0jntc | Coker Lane | lane |
| rd-wovdjsau | Oyedele Street | lane |
| rd-jz7sq90i | Ereko Street | lane |
| rd-f6q1n1wy | Fasanya Street (Fadeyi) | lane |
| rd-ii9itgbq | Ayonuga Street (east-west) | lane |
| rd-3rgiuuc4 | Adewusi Street | lane |
| rd-j8goyo7h | Brown Lane | lane |
| rd-aa7ee22h | Kadiri Street | lane |
| rd-gxcqgoq3 | Ojelade Street | lane |
| rd-rv4ry0w9 | Lawani Street | lane |
| rd-rey9587t | Bada Street (north-south) | lane |
| rd-p3sthhi8 | Bada Street (east-west) | lane |
| rd-khx710gd | Kugbuyi Street | lane |
| rd-hzvl6lf5 | Daniel Street | lane |
| rd-l96ihryl | the street off the Agege Motor Road by the pharmacy | lane |
| rd-340okaz6 | the street off the Agege Motor Road by the children's hospital | lane |
| rd-pruajgib | Agbekolade Street | lane |
| rd-m61sp7km | Olorunnibe Street | lane |
| rd-tweirlz8 | Buraimoh Street | lane |
| rd-rbhmxjfp | Igbarere Street | lane |
| rd-eoffh636 | Imoru Street | lane |
| rd-lwd1maam | Ojo Street (south of Elegba Festival Drive) | lane |
| rd-tpu9jzp8 | Ojo Street, then Oluwapo Street | lane |
| rd-tiivalui | Amodu Street | lane |
| rd-pj8cd3wg | Oyegunle Street | lane |
| rd-ius2ua2s | Akinbiyi Street | lane |
| rd-f4ggg0x2 | Ijaiye Street | lane |
| rd-ziw0h5ax | Igbeyin Adun Street | lane |
| rd-8hoarai5 | Ogunsanya Street | lane |
| rd-v4erxr45 | Alhaji Awoyejo Street | lane |
| rd-esu3rasg | Adegbite Street | lane |
| rd-1h2058d6 | Ali Street | lane |
| rd-pbwqrjkc | Ashaoku Street, on north-east past Ali Street | lane |
| rd-c666dphk | Anifowoshe Street | lane |
| rd-97wkrkzt | the street past the packaging works | lane |
| rd-qf3o0ux0 | the short street south from the packaging works | lane |
| rd-xvn9otuq | the street behind the Agege Motor Road | lane |
| rd-74ayh5is | Adedeji Street | lane |
| rd-kfww6jfn | Idumagbo Street | lane |

**Block B4** (Ladipo Street, Palm Avenue and the district's north-east edge). Redrawn 24 Oct from a close-zoom study (five z18 shots at the checked shot scale; owner: zoom in for the details): the first six lanes were read at z16. The real twin is the Ladipo spare parts market and the Matori industrial estate: Jimade Street through the market, the estate road running north from it and east past the warehouses, the cross road over the sheds, the short streets off Ladipo Street by the bank (Unity Close among them), and the east-west street on the estate's north edge; in the residential corner by Palm Avenue, Badejo Kalesanwo, Oduduwa, Efon Alaye, Ikole and C.A.C. Streets, with Omodigbo Street's north end joining Palm Avenue. Fatai Atere Way (rd-99r8996c) was already on its real line and is kept. Streets that end on the district's edge stop there until the seam pass; the estate streets that end among the sheds are real dead ends. Removed: the six z16 lanes rd-tdvlj3x3, rd-fujb836w, rd-dntx4fhp, rd-2rumos81, rd-44hhdxyo, rd-l791gps5.

| Gidi id | real twin | kind |
|---|---|---|
| rd-yeqmwvdn | Jimade Street (the Ladipo market street) | market_street |
| rd-vnres9ex | the Matori estate road: north from Jimade Street, then east past the warehouses | service_road |
| rd-cpn887is | the estate road across the sheds, Jimade Street to the north road | lane |
| rd-s5h4f0w5 | the street off Ladipo Street by the bank | lane |
| rd-ypmlhk6e | Unity Close | lane |
| rd-yp8z89b0 | the street north to the estate's edge | lane |
| rd-cfhigpz4 | the east-west street at the estate's north edge | lane |
| rd-145fsri7 | the street off Ladipo Street past the warehouses | lane |
| rd-kvh4h6jq | the short street behind the bank | lane |
| rd-m64dyubf | Badejo Kalesanwo Street | lane |
| rd-gjzqjyr2 | Oduduwa Street | lane |
| rd-nssllco8 | Efon Alaye Street | lane |
| rd-tn5e2vxk | Ikole Street | lane |
| rd-0wdqpabq | C.A.C. Street | lane |
| rd-sznt34c5 | Omodigbo Street's north end | lane |

**Block B5** (Olayiwola Liasu, Ilasamaja Road, Itire Road, Akanro, Ayuba Dawodu and Olusanya Streets). Redrawn 24 Oct from a close-zoom study (three z18 shots at the checked shot scale; owner: zoom in for the details): the first three lanes were read at z16 and two of them sat off the real lines. The real twin is the Akanro / Ilasamaja side. North of Akanro Street: Oladeinde Coker Street bending up to the Karimu Agoro street, Alfa Nda Street, Alhaji Isiaka Nda Street, Oba Lane, Ajose Street, Olafimihan Street (its west end runs up Moriamo Ajoke Street's line to Ilasamaja Road), Okunade Street and Onayiogbo Street. South of it: Oladosu Sanusi running on as Mopelola and Tanimowo Streets, Shobowale Street, Afisi Street on to Ojo Street, Ogunbowale Street and the Date Palm school street, Kekereowo Street on to Babalola Street and Itire Road, Olajide Street, the street past the Christ Apostolic Church, and Omosolape Street beyond the canal. Ayuba Dawodu and Akanro Streets were already on their real lines and are kept. Left out for spacing: Anofiu, Moriamo Ajoke's south end, Church Close, Odofin and Alhaji Alaka, Oyinkan, Irokosu, Ganiyu Hassan, Olusanya (Gidi's west edge road is its twin). Removed: the three z16 lanes rd-jkhasg5m, rd-zu0ao8aa, rd-9p5skecq.

| Gidi id | real twin | kind |
|---|---|---|
| rd-nj3sfh8p | Oladeinde Coker Street | lane |
| rd-4h8mnpoo | the street by Karimu Agoro Street, Ilasamaja Road to Alfa Nda Street | lane |
| rd-dla5ljj1 | Alfa Nda Street | lane |
| rd-yj4woxpz | Alhaji Isiaka Nda Street, on south past Akanro Street | lane |
| rd-jc0mdz0x | Oba Lane | lane |
| rd-iro9fmv2 | Olafimihan Street | lane |
| rd-56ovxs0k | Okunade Street | lane |
| rd-u80w77ph | Ajose Street | lane |
| rd-364h94tc | Onayiogbo Street | lane |
| rd-jaf53pf0 | Oladosu Sanusi, Mopelola and Tanimowo Streets | lane |
| rd-h1lgtwi5 | Shobowale Street | lane |
| rd-iz10prdy | Afisi Street on to Ojo Street | lane |
| rd-9ho3snky | Ogunbowale Street | lane |
| rd-5y1k9nk7 | the street by Date Palm High School | lane |
| rd-kvx590dw | Kekereowo Street on to Babalola Street | lane |
| rd-uy3bbwus | Olajide Street | lane |
| rd-n8hut0ew | the street past the Christ Apostolic Church, to the canal side | lane |
| rd-k2glzog0 | Omosolape Street | lane |

**Small blocks, first batch (B6, B7, B9), studied at close zoom (z17)** (owner, 23 Oct: zoom in to get the details).
Real streets here are 50-60 m apart, which is under 20 m at 1:3, too tight for a house on each side; so about one real
street in two is kept, the main ones.

B6 (Ilupeju's Mushin end and Onipanu, between the rail and Tinubu Road). Tinubu Road is the district edge (a seam).
Egbeyemi Street crosses the narrow north strip edge to edge and comes back at the seam pass.

| Gidi id | real twin | kind | from, to |
|---|---|---|---|
| rd-pf99fopw | Ilupeju Road (Mushin end) | local_main | the lane by Adeshiyan Street to the Tinubu Road edge |
| rd-f0cw4h6z | the unnamed street from Igbaja Street down to Ajegunle Street | lane | in the block to Ilupeju Road's twin |
| rd-xjd6yh6c | Akinbola Street | lane | the west edge to the unnamed street |
| rd-xclnzrz2 | the unnamed east-west street south of Akinbola, to Tinubu Road | lane | the unnamed street to the edge |
| rd-rou8v2ci | Awoyokun Street | lane | Sosanya's twin to Ajegunle's twin |
| rd-h8120zyk | Sosanya Street on to Ojewere Street | lane | Idera Road's twin to Ali Lane's twin by Mushin station |
| rd-524395x5 | Ajegunle Street (Mushin) | lane | Awoyokun's twin south |
| rd-m0yjgudq | Fagbile Street | lane | Sosanya's twin to Ajegunle's twin |
| rd-z7y18cz7 | Ali Lane | lane | Sosanya's twin to Olapido Sode's twin |
| rd-771zvqoe | Olapido Sode Street | lane | Ajegunle's twin to the east edge |

B6 re-checked 24 Oct at z18 at the checked shot scale (three shots down the block). The lanes above sit within a couple of metres of their real streets, but the block's middle (the Ilupeju side between the rail, the Adeshiyan Street road and Oyewole Street) had no streets at all beyond the base road loop. Added there: Oke-Arin, Ibiteye and Ajenifuja Streets west of Adeshiyan; Shyllon Street on both sides of the base road (which runs on its middle stretch); Ibadan and Shobayo Streets up from Shyllon; Iseyin and Adegboyega Streets across to Oyewole, and Tawose Street between them and Idera Road. Left out for spacing: the south arm of Ajenifuja, Church Street, Bambe Street.

| Gidi id | real twin | kind |
|---|---|---|
| rd-udhlvf7d | Oke-Arin Street | lane |
| rd-khhejacj | Ibiteye Street | lane |
| rd-jb2o4e6d | Ajenifuja Street | lane |
| rd-ozzwa52h | Shyllon Street (west of the Adeshiyan road) | lane |
| rd-81xgmq7j | Shyllon Street (east of the Adeshiyan road) | lane |
| rd-dnrpnn94 | Ibadan Street | lane |
| rd-i9d8jkyo | Shobayo Street | lane |
| rd-hnz8n85y | Iseyin Street | lane |
| rd-tzcgktxu | Adegboyega Street | lane |
| rd-fotehnel | Tawose Street | lane |

B7 (the Apapa-Oshodi Expressway side by Isolo Road: factories along the expressway, Oye Primary School, houses east). Re-checked 24 Oct at z18 at the checked shot scale (two shots): the five z17 lanes sat up to 8 m off (Adisa Thomas Street ran diagonally). Now Shasere Ajibade Street end to end; on the factory side, the warehouse roads off the expressway's service road (past the Community Secondary School, by the bank, past ECS, by Kuramo Industries) and both arms of Ifelodun Street; east of Shasere, the Daleko market street, the Grace Baptist street off Adeoya Close, Chief Olu Adekoya Street to Olu Aina Street, Dele Viju Close, the P and P college street, Adisa Thomas, Taofik Abolaji and Majekodunmi Streets; and in the strip between Olu Aina and Adeoyo Streets, Igbo Owu and Adefuwa Streets. Removed: rd-a3ok14xh, rd-q7px2xqw, rd-5dpnprkh, rd-ngnuvohi, rd-90x3jf29.

| Gidi id | real twin | kind |
|---|---|---|
| rd-z3i9yyex | Shasere Ajibade Street | home_street |
| rd-0i4ei708 | the Daleko market street | lane |
| rd-i3tv1gvr | the street past Grace Baptist Church, off Adeoya Close | lane |
| rd-4m50afsk | the warehouse road by the bank, off the expressway | lane |
| rd-tfrak2nd | Chief Olu Adekoya Street | lane |
| rd-2sb6jwlg | the factory road by Kuramo Industries | lane |
| rd-zh0fu8w7 | the road past the Community Secondary School | lane |
| rd-kjbrkrej | the warehouse road past ECS | lane |
| rd-avjtnca0 | Ifelodun Street (the north-south arm) | lane |
| rd-ns5g7sgs | Dele Viju Close | lane |
| rd-ygloxipl | the street past the P and P college, off Adeoyo Street | lane |
| rd-t07adhpt | Adisa Thomas Street | lane |
| rd-wzqwmk8q | Taofik Abolaji Street | lane |
| rd-vvycykua | Majekodunmi Street | lane |
| rd-s96wwwah | Ifelodun Street (the east-west arm) | lane |
| rd-nxtksffe | Igbo Owu Street | lane |
| rd-39eedx9o | Adefuwa Street | lane |

B8 (Fashoro and Ojuelegba: east of Bishop Street and Atunrase Street, down to Ojuelegba Road, the expressway side the east edge). Read 24 Oct at z18 at the checked shot scale (three shots); it had no streets of its own but the base lane on Cole Street. North of Apena Street: the Olode-Okuta Street loop with Odejayi Crescent on to Ramos Street and Odejayi's north arm, Akinwande, Rosamond and Akinhanmi Streets, Haastrup and Omololu Streets with Ibidun's east arm, and Apena Street through to Ibidun Street. South of it to Ojuelegba Road: Onasanya, Mabo, Banire, Ibidun (beside the canal) and Ayilara Streets. The Lagos Anglican Girls Grammar School grounds stay open. Left out for spacing: Oludipe Street, Shodipe Close, Karimu, Shitawu and Ororedo Streets.

| Gidi id | real twin | kind |
|---|---|---|
| rd-m76g0s16 | Olode-Okuta Street | lane |
| rd-njs0ka5v | Odejayi Crescent on to Ramos Street | lane |
| rd-skzfzgm3 | Odejayi Crescent (the north arm) | lane |
| rd-peirz7h1 | Akinwande Street | lane |
| rd-uo9tlyvq | Rosamond Street | lane |
| rd-lv47qmiy | Akinhanmi Street | lane |
| rd-0cpdhblw | Haastrup Street | lane |
| rd-3ysvvjrs | Omololu Street | lane |
| rd-cq1ohmmi | Ibidun Street (the east arm) | lane |
| rd-5d0hjnqv | Apena Street | lane |
| rd-potxzar5 | Onasanya Street | lane |
| rd-qb94w1lg | Mabo Street | lane |
| rd-s783qtw5 | Banire Street | lane |
| rd-ukmi0p9d | Ibidun Street, beside the canal | lane |
| rd-4d9x8zni | Ayilara Street | lane |

B9 (Bamgboye / Owo, between Adeoyo, Olusoga and Ilasamaja Road). Re-checked 24 Oct at z18 at the checked shot scale: the four z17 lanes were within about 5 m, but Bamgboye Street stopped halfway and Alafia Street's north end sat 8 m west. Redrawn on the real lines, Bamgboye now running through to the district's east edge. Adeshile and Moliki Streets are still left as gaps for spacing. Removed: rd-kjitnqqz, rd-31p2dumv, rd-w8jhnt3x, rd-9gbercvs.

| Gidi id | real twin | kind |
|---|---|---|
| rd-wqe12uoj | Bamgboye Street | lane |
| rd-regiv15v | Olanrewaju Street | lane |
| rd-4a3m9gq5 | Alafia Street | lane |
| rd-kmzid1cy | Owo Street on to Da-Silva Avenue | lane |

B11 (Araromi and Church Street: between Adeoyo Street, Isolo Road, Itire Road and Olusoga/Awawu Streets). Read 24 Oct at z18 at the checked shot scale (three shots). The north-west: Layi Oyekanmi Street from Isolo Road to Omu Street, Araromi Street from Layi Oyekanmi round its south leg to Church Street, and Olawoyin Street from Church Street up to Araromi. Across the middle Church Street runs from the Olusoga corner to Ademoshun Street; Alafia Street carries on from Church Street to B9's Alafia lane; Ewenla Street runs on to Daniel Street from Omowunmi to Olusoga; Ademoshun Street from Isolo Road to Church Street. Left out for spacing: Sanusi Street (beside Isolo Road), Rabiatu Idowu Street, Omowunmi Street's diagonal, Okesanya, Cameroon, Showunmi and Tamitope Streets.

| Gidi id | real twin | kind |
|---|---|---|
| rd-0gu6klk4 | Layi Oyekanmi Street | lane |
| rd-m9b20y08 | Araromi Street | lane |
| rd-wsadnelk | Olawoyin Street | lane |
| rd-fb96tfq9 | Church Street | lane |
| rd-hjh48h6m | Alafia Street (north of Olusoga) | lane |
| rd-rby6c85s | Ewenla Street on to Daniel Street | lane |
| rd-pilgciql | Ademoshun Street | lane |

B10 (Ladipo: between Palm Avenue, Owhin Street, Ladipo Street, Agege Motor Road's side and Isolo Road, round the dead-end road on Ogunoye and Oguntoye Streets). Read 24 Oct at z18 at the checked shot scale (five shots). Across from Owhin Street to Ladipo Street: Ofada, Oliyide and Iyalla Streets, then Aromire and Olufunmilayo Streets lower down. Down the middle: Tadeyo Street from Oliyide to Isolo Road, and Ogunoye Street from Ladipo Street to the dead-end road's tip, which now joins it to the rest. East of Ogunoye: Ojo Road on to Wey Street through to Agege Motor Road's side, and Odulana Street from Ladipo Street to Wey Street. Left out for spacing: Adekitan Street's east arm, Folarin and Alaba Streets, Sholanke, Moroluke and Dakobiri Streets.

| Gidi id | real twin | kind |
|---|---|---|
| rd-cr6a2j9l | Ofada Street | lane |
| rd-f6n5u0g1 | Oliyide Street | lane |
| rd-tjdct2l3 | Iyalla Street | lane |
| rd-h0p4xdbd | Tadeyo Street | lane |
| rd-549qul9s | Ogunoye Street | lane |
| rd-qmm0iloh | Aromire Street | lane |
| rd-xp0cgtsa | Olufunmilayo Street | lane |
| rd-hvwdw3gi | Ojo Road on to Wey Street | lane |
| rd-xjvsti21 | Odulana Street | lane |

B15 (Papa Ajao, north of Ladipo: between Palm Avenue, Ladipo Street, Agege Motor Road and Oluwole Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Olaseinde Street runs from Ladipo Street to Agege Motor Road and Oshinfuye Street on to Taiwo Lane below it; Omodigbo Street on to Balogun Street and Buari Street run from Palm Avenue down to Ladipo Street. Left out for spacing: Anipele Street, Solomon Close, Disu Street's north end.

| Gidi id | real twin | kind |
|---|---|---|
| rd-80nwmh8a | Olaseinde Street | lane |
| rd-mw3dwbpl | Oshinfuye Street on to Taiwo Lane | lane |
| rd-xrm36c1i | Omodigbo Street on to Balogun Street | lane |
| rd-gqsv49g9 | Buari Street | lane |

B14 (Idi-Oro to Ishaga Road: between Itire Street, Isolo Road, Paul Okuntola and Ajegunle Streets, and Ishaga Road). Read 24 Oct at z18 at the checked shot scale (two shots, north and south). The north arm has one spine, Oloruntosin Street on to Alasalat Street up to Isolo Road, crossed by Ogun Street, with Ajorin Street running on south and east to Paul Okuntola Street. The wider south part has Bakare Street from Itire Street down to Ishaga Road, with Ilora, Morgan and Gbolahan Streets across it. Left out for spacing: Sarunmi Street, John Street, Ayandeji Street, Olajide Street, Lawal Street, Taiwo Street.

| Gidi id | real twin | kind |
|---|---|---|
| rd-p224w40k | Oloruntosin Street on to Alasalat Street | lane |
| rd-x37bsf38 | Ogun Street | lane |
| rd-d9ib0rdk | Ajorin Street | lane |
| rd-13cjjcjg | Bakare Street | lane |
| rd-8p3596pi | Ilora Street | lane |
| rd-blho77vn | Morgan Street | lane |
| rd-x1ebutg6 | Gbolahan Street | lane |

B13 (central Mushin: between Post Office Road, Coker Street and Isolo Road, round the dead end of Dada Iyalode and Abolade Streets). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Abiodun Street runs from Post Office Road down through the block, cut in two where it crosses Abolade Street; Mumuni Street on to Adebesin Street runs from Dada Iyalode Street to Coker Street; Oluwoye Street runs from Abolade Street to Isolo Road, with Aganran Street from it to Abiodun Street. Left out for spacing: Williams Ladega Street, Olapade Street, Olumorokun Street, Ogunmokun Street and the short unnamed streets east of Abiodun.

| Gidi id | real twin | kind |
|---|---|---|
| rd-cvnc099q | Abiodun Street (north of Abolade Street) | lane |
| rd-ed6egqst | Abiodun Street | lane |
| rd-qpyslofn | Mumuni Street on to Adebesin Street | lane |
| rd-0gi2ewca | Oluwoye Street | lane |
| rd-0pmc0xha | Aganran Street | lane |

B16 (Ilasamaja, between Akanro Street, Lamina Street and the expressway, down to the district edge; the rest of B16 is the thin strip between the two carriageways north of it, left as it is). Read 24 Oct at z18 at the checked shot scale (one shot on the block's south end, where its land is). Ajeabo Street runs from Akanro Street to the district edge; Odunaike Street from Akanro Street down to Kekereowo Street, which runs from Ajeabo Street to Lamina Street; Oremeji Street runs in from Lamina Street and on south as Olaide Awoye Street to the district edge. Left out for spacing: Olayinka Street, Technical Street, Waidi Apesin Street, Owoseni Street.

| Gidi id | real twin | kind |
|---|---|---|
| rd-6qjnbv9a | Ajeabo Street | lane |
| rd-5z414dfc | Odunaike Street | lane |
| rd-upn7sjm7 | Kekereowo Street | lane |
| rd-vuw2n757 | Oremeji Street on to Olaide Awoye Street | lane |

B17 (around Mushin General Hospital: between Palm Avenue, Isolo Road and Lapite Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Akinsola Crescent runs down from Adekitan Street, round its bottom bend and up as Ofada Street on to Oduntan Street to the block's north-east edge; Folarin Street runs from that edge down past the hospital and on east as Alokolaro Crescent to Lapite Street. Left out for spacing: Salako Street, Igbore Street, the hospital's ring road, Olufunmilayo Street.

| Gidi id | real twin | kind |
|---|---|---|
| rd-dn9auxmx | Akinsola Crescent on to Ofada Street and Oduntan Street | lane |
| rd-uwom6nbe | Folarin Street on to Alokolaro Crescent | lane |

B18 (Idi-Oro, between Agege Motor Road, Folami Street and Labinjo Street's south bend). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Abeokuta Street and Labinjo Street run from Agege Motor Road down across the block; Makinde Street runs from Labinjo Street to Folami Street, and Alamutu Street from it down to the block's south-west edge. Left out for spacing: Shoremekun Street, Labinjo Close, Adeyanju Street, Wilkey Street, Odesanya Close.

| Gidi id | real twin | kind |
|---|---|---|
| rd-7qnvm1jp | Abeokuta Street | lane |
| rd-9eb5vovf | Labinjo Street | lane |
| rd-emgqj1wh | Makinde Street | lane |
| rd-12jdsl3e | Alamutu Street | lane |

B19 (Ilupeju side of Mushin: the strip between Shokunbi Street and Olateju Street, south of Vono Road). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Olorunnisola, Alayaki and Ashafihan Streets cross the strip from Shokunbi Street to Olateju Street, about one cross street in two. Left out for spacing: Alhaji Otta Street, the street past the bus stop between Alayaki and Ashafihan, Odusami Street.

| Gidi id | real twin | kind |
|---|---|---|
| rd-vp2j6h9n | Olorunnisola Street | lane |
| rd-jc6sxw9f | Alayaki Street | lane |
| rd-txt3yk6k | Ashafihan Street | lane |

B20 (the long strip between Olateju Street and the railway, from Olorunnisola Street down to Tade Lane). Read 24 Oct at z18 at the checked shot scale (two shots, north and south, at 3.3593). Olorunnisola Street runs in from Olateju Street and turns south as Akinbode Street down the strip; Araba Street crosses it from Olateju Street to a dead end short of the railway; Hanson Lane runs from Olateju Street to the railway further south. Left out for spacing: Tinuola Street, the Fashina Streets, Agunbiade Street, Gbenle Street, Danmegoro Street, Tade Lane.

| Gidi id | real twin | kind |
|---|---|---|
| rd-2elgaw22 | Olorunnisola Street on to Akinbode Street | lane |
| rd-lsk0nkts | Araba Street | lane |
| rd-6bv2yosa | Hanson Lane | lane |

B21 (west of Shokunbi Street, between Fafolu Street and Ayantuga Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Oyo Street and Ashafihan Street cross the block from its west edge to Shokunbi Street, carrying on the lines of B19's Alayaki and Ashafihan lanes across it. Left out for spacing: Akinboro Lane, Alhaji Otta Street, Banire Street, Ishadare Street.

| Gidi id | real twin | kind |
|---|---|---|
| rd-sq9yr86z | Oyo Street | lane |
| rd-cc9tth8j | Ashafihan Street | lane |

B22 (between Olorunsogo Street, Fafolu Street and Ayantuga Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Oyo Street runs down from Fafolu Street to Macaulay Street, carrying on B21's Oyo lane; Macaulay Street crosses the block from Olorunsogo Street to Fafolu Street, where it carries on as B21's Ashafihan lane. Left out for spacing: the street from Fafolu Street down to Alli Close, Alli Close.

| Gidi id | real twin | kind |
|---|---|---|
| rd-x0hilxfr | Oyo Street | lane |
| rd-x7eslkeo | Macaulay Street | lane |

B23 (between Coker Street, Olateju Street and Ogunmokun Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Olomowewe Street runs through the block from Olateju Street down to Ogunmokun Street; its south end meets Gidi's Ogunmokun road (rd-f782px4g), which runs south of the real line there. Left out for spacing: Jinadu Street (about 85 m from Olomowewe at Olateju).

| Gidi id | real twin | kind |
|---|---|---|
| rd-pee3ohfv | Olomowewe Street | lane |

B24 (between Akintan Street, Martins Street, the Agege Motor Road side and Onifade Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Omoniyi Street runs down from the block's north edge to the Gidi road at Ogungbaiye Street, where the older Omoniyi lane (rd-trz9qjln) carries on south; Adeyemi Street crosses the block from Akintan Street to Martins Street. Left out for spacing: Kelani Street and Ogungbaiye Street (each about 75-80 m from Adeyemi).

| Gidi id | real twin | kind |
|---|---|---|
| rd-96wuk9tz | Omoniyi Street (north stretch) | lane |
| rd-zq9bs5v6 | Adeyemi Street (east of Akintan) | lane |

B25 (between Shokunbi Street, Olateju Street, Ayantuga Street and Coker Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Onanuga Street crosses the block from Shokunbi Street to Olateju Street; Olufemi Onanuga Street runs from it down to Coker Street. Left out for spacing: Danmegoro Street (about 63 m from Onanuga at Olateju), the short street from Ayantuga Street down to Danmegoro, Wahabi Street.

| Gidi id | real twin | kind |
|---|---|---|
| rd-n9c6t57b | Onanuga Street | lane |
| rd-0j8zaiv8 | Olufemi Onanuga Street | lane |

B26 (Ilasamaja side: between Sadiku Street, Akanro Street, Oladele Street and Agoro Bogunbolu Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). Gbangba Street runs from Sadiku Street down to Akanro Street, on to the end point of the older lane south of it (rd-5z414dfc). Left out for spacing: Oladele Street's north leg (about 40 m from the block's west edge), Araba Baptist Church Street and Oladeinde Coker Street, Olagbaiye Street (a dead end).

| Gidi id | real twin | kind |
|---|---|---|
| rd-196r6fwm | Gbangba Street | lane |

B28 (between Ayantuga Street, Kumuyi Street, Post Office Road and Olumorokun Street). Read 24 Oct at z18 at the checked shot scale (one shot, the block fits it). The block's west half is a school compound with its own driveways (not drawn as streets); Bakare Close runs in from Kumuyi Street to a real dead end. Left out for spacing: Dawodu Lane, the other dead end off Kumuyi Street.

| Gidi id | real twin | kind |
|---|---|---|
| rd-si9baapu | Bakare Close | lane |
