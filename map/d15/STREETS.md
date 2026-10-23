# Mùṣá (district 15): the road plan and where each street comes from

Roads only, drawn on the new frame (1:3). Every kept street sits on its real line, squeezed to the frame, at its real width (never shrunk). Real names live here only, never in the map. Buildings come later.

## Count

- Real streets inside the border (Overture study, rail left out): about **658**: 15 skeleton roads (expressways, trunk, mains), 145 named local streets, and about 498 unnamed street pieces longer than 30 Gidi m (1396 pieces in all). 212.6 km of real street, 70.9 km at Gidi scale.
- Kept (22 Oct): **62 streets in 64 records**; after the owner's calls (23 Oct): 56 streets in 59 road records, plus a rail, a station and the market (the expressway and Western Avenue are each two records that start at an inside junction, so their first point lies in the district), 17.8 km. That is about 1 in 11 of the real streets: every skeleton road, every main, and about 40 local streets kept for life, kit tests and links.
- Kinds: 6 motorway records, 1 trunk, 11 main roads, 12 local mains, 5 market streets, 27 home streets, 2 lanes.
- Values: only what was seen. Widths measured on Google satellite at z19 (17 records) or taken from the kit shots; surfaces, kerbs, medians and drains from the kit Street View shots (ot numbers). Everything else is left missing, so the board shows it amber (needs a value). check_map has no red: every problem it lists is a missing field.

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

**Block B1** (between the expressway's east service road, Ladipo Street, Palm Avenue and Isolo Road). The real twin is
two places: a warehouse strip along the expressway (big sheds and yards: the SCOA, Kia, Afprint and NAFDAC side) and,
east of Alhaji Amusa / Olanibi Street, the dense Ladipo-Odunsi grid, streets about 70 m apart parallel to Ladipo
Street's south-east leg (Shotinoye, Olasode, Ikale, Orenaji) crossed at right angles (Ojekunle, Adeolu, Sebanjo), houses
wall to wall. Kept at 1:3: the strip's edge street and its way in from the expressway, four of the grid's long streets
(one in three, 36 m apart, so two real-size houses stand back to back between them) and four cross streets. Houses: the grid's blocks are lined with the twin's own houses turned to face their lanes (`draft_buildings.py --frontage`); the strip's with the twin's own sheds (`--sizes=600,20000`).

| Gidi id | real twin | kind | from, to |
|---|---|---|---|
| rd-xv349h4t | Olanibi / Alhaji Amusa Street (the warehouse strip's east edge) | home_street | Isolo Road to Ladipo Street, 100 m east of the service road |
| rd-u279z4ax | Bello Street (west end) | home_street | the expressway's east service road to the Olanibi twin |
| rd-e0xhkawc | Shotinoye Street | lane | parallel to Ladipo Street's south-east leg, 36 m in |
| rd-bnvso03s | Ikale / Olasode Street | lane | 72 m in |
| rd-yjd1xo0i | Orenaji / Aledesuru Street | lane | 108 m in |
| rd-cu7mk008 | Alhaji Lamidi / Awonatu Street | lane | 144 m in, the Olanibi twin to Sebanjo's twin (fills the big south block) |
| rd-yixf7hb6 | Yusuph Street | lane | Ladipo Street to the Olanibi twin |
| rd-5dd0t1l1 | Ojekunle Street | lane | Ladipo Street to the Olanibi twin |
| rd-zsmjw1sh | Adeolu Street / Jumoke Way | lane | Ladipo Street to the Olanibi twin |
| rd-xtsicy57 | Sebanjo Street | lane | Ladipo Street to Isolo Road |

**Block B0** (Ishaga Road, Bishop Fashoro Street, the Agege Motor Road edge, Ajegunle and Atunrase Streets). The real
twin is Idi-Araba: the LUTH campus with the College of Medicine and its staff quarters (internal drives, big buildings,
greens, the canal on its south-east side), Eko Boys and Birch Freeman High Schools, and irregular housing streets about
100 m apart east of the canal to Bishop Street and west of the campus (Takuro, Olaleye). Kept: LUTH's main drive from
the north gate (Apesin's end) to Ishaga Road, Road 4 and the staff quarters road, and six housing streets.

| Gidi id | real twin | kind | from, to |
|---|---|---|---|
| rd-d68pbjgh | LUTH's main drive | service_road | the north gate (Apesin's end) to Ishaga Road |
| rd-g9taxf2k | LUTH Road 4 | service_road | the main drive towards the canal (ends in the campus) |
| rd-g6v156jj | the staff quarters road | service_road | the main drive to Laniyan Street, by Akintola |
| rd-w0uqy2s9 | Olaniyi Street | lane | the staff quarters road past Birch Freeman to the Agege Motor Road edge |
| rd-erfcf0tx | Alao Adegboyega Street | lane | Olaniyi's twin to Bishop Fashoro Street |
| rd-8xdqzq9d | Lawani Street on to Ogunfunmi Street | lane | Ishaga Road to Bishop Fashoro Street, south of the canal |
| rd-phi8eic8 | Takuro Street | lane | Ajegunle Street to LUTH's main drive |
| rd-jm7fmw8p | Olaleye Street | lane | Takuro's twin north (ends in the block) |
| rd-9ozcrkqs | Akintola / Apesin Street | lane | LUTH's main drive to Laniyan Street, by Eko Boys |

**Block B2** (Ishaga Road, Itire Road, Ajegunle, Onipede, Mushin Road's end, Bello, Atunrase, Aborishade and Dosunmu
Streets). The real twin is the Ishaga Road / Lawanson side of Itire: north of the canal, short north-south streets
about 90 m apart running from Ishaga Road down to Daniyan Street on the canal bank; south-west of it, north-west to
south-east streets running down to Lawanson Road; and a pocket by Adedoyin Road. Kept: three of the north streets
(Abati and Moshalashi left as gaps), Daniyan on the canal, two south-west streets and Adedoyin.

| Gidi id | real twin | kind | from, to |
|---|---|---|---|
| rd-i6s2bf4s | Daniyan Street (north of the canal) | lane | the west edge along the canal to Igbira's twin |
| rd-a0jvm3x0 | Adekunle Street | lane | Ishaga Road to Daniyan's twin |
| rd-uheomc6y | Garuba Musa Street | lane | Ishaga Road to Daniyan's twin |
| rd-tfs65na7 | Igbira Street | lane | Ishaga Road to Daniyan's twin |
| rd-nybc6644 | Alves Street | lane | Onipede's side down towards Lawanson (ends in the block) |
| rd-b9u5qmox | Odunsi Street | lane | south of the canal down towards Lawanson (ends in the block) |
| rd-oiymgele | Adedoyin Road | lane | the pocket by Aborishade, west to east |

**Block B3** (Ogunmokun Street, the Agege Motor Road, the Ikorodu Road edge and Kayode Street; the rail runs through
it). The real twin is the Mushin station side of Fadeyi: east of the rail, a close grid of short east-west streets (Giwa,
Cole, Adesina, Aiyetoro / Akinola, Ayonuga, Adewusi) crossed by the long north-south Haruna, Ayonuga and Akorohunfayo
Streets, running to the Ikorodu Road service lane; west of the rail, crooked streets off Ogunmokun and Smith Streets,
and Agbekolade and Olorunnibe off the Agege Motor Road. Streets on the rail side end at the rail, as the real ones end at
Ago-Owu and Smith Streets beside it.

| Gidi id | real twin | kind | from, to |
|---|---|---|---|
| rd-mzaial2i | Giwa Street | lane | the rail side to Akorohunfayo's twin |
| rd-jdq1vk2j | Cole Street | lane | the rail side to Akorohunfayo's twin |
| rd-ye8zhvw4 | Haruna Street | lane | Cole's twin south (ends in the block) |
| rd-vhulohlp | Adesina Street | lane | the rail side east (ends in the block) |
| rd-vx27esql | Aiyetoro Street / Akinola Street | lane | the rail side to the Ikorodu Road edge |
| rd-r5gc47ia | Ayonuga Street (north-south) | lane | Aiyetoro's twin south |
| rd-abbx5rnv | Ayonuga Street (east-west) | lane | the north-south Ayonuga to the Ikorodu Road edge |
| rd-70q1fgdg | Adewusi Street | lane | the rail side to the Ikorodu Road edge |
| rd-n2ald4yc | Bada Street | lane | Adewusi's twin south towards Jibowu (ends in the block) |
| rd-1383lbsh | Oluwakemi Street | lane | Kayode Street's side south to Akorohunfayo's twin |
| rd-8fe89b52 | Akorohunfayo Street | lane | Oluwakemi's twin past Giwa and Cole to Aiyetoro's twin |
| rd-h6vwsegj | the unnamed street south of Ogunmokun (by the NDO lounge) | lane | Ogunmokun's side towards Smith Street |
| rd-65shqr4p | the unnamed cross street off Smith Street | lane | the rail side west (ends in the block) |
| rd-iwrs1m4t | Agbekolade Street | lane | the Agege Motor Road to the rail side |
| rd-et552uc8 | Olorunnibe Street | lane | the Agege Motor Road to the rail side |

**Block B4** (Ladipo Street, Palm Avenue and the district's north-east edge). The real twin is the Ladipo spare parts
market and the Matori industrial estate: long market sheds and warehouses on a few wide roads (Jimade Street through the
market, Fatai Atere Way crossing to Matori, the estate road along the north side), and a residential corner by Palm
Avenue on short streets (Badejo Kalesanwo, Oduduwa, Ikole, C.A.C.). Fatai Atere Way and Jimade end on the district edge;
they carry on in the neighbour when that seam is joined by hand.

| Gidi id | real twin | kind | from, to |
|---|---|---|---|
| rd-99r8996c | Fatai Atere Way | local_main | Ladipo Street to the north-east edge |
| rd-tdvlj3x3 | Jimade Street (the Ladipo market street) | market_street | Ladipo Street by Daraju to Fatai Atere's twin at the edge |
| rd-fujb836w | the Matori estate road along the north side | service_road | Ladipo Street to the edge |
| rd-dntx4fhp | Badejo Kalesanwo Street | lane | Ladipo Street east (ends in the block) |
| rd-2rumos81 | Oduduwa Street | lane | Ladipo Street east (ends in the block) |
| rd-44hhdxyo | Ikole Street | lane | Oduduwa's twin to Palm Avenue |
| rd-l791gps5 | C.A.C. Street | lane | Oduduwa's twin side to Palm Avenue |
