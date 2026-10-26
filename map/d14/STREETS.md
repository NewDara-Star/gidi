# Ìtìrí (district 14): the road plan and where each street comes from

Roads only, drawn on the new frame (1:3) at real widths. Real names live here only, never in the map. Houses and
places come in their own passes (NOW item 11).

## Count (Ìtìrí hand pass 1, 26 Oct)

- District: 0.57 km² (Gidi), 1150 × 866 m, across Lawanson Road from Mùṣá (15).
- Real streets crossing the border (Overture segments, subtype road): 967 street pieces, 32.5 km inside at Gidi scale:
  700 residential (24.1 km), 117 secondary, 59 service, 34 tertiary, 30 unclassified, 22 primary, 4 motorway,
  1 unknown; and 11 foot pieces (7 footway, 3 path, 1 steps; 172 m) left out, as in Mùṣá.
- Kept: **every street**, 367 road records, 23.6 km: 1 motorway, 4 service roads, 15 main roads, 17 local mains,
  151 home streets, 179 lanes. Unlike Mùṣá (1 in 11), nothing is thinned: Ìtìrí's density (about 41 km/km² at Gidi
  scale) is close to Mùṣá's kept 37, and the working bar wants real streets on their real lines.
- Industry note (the selection question): cartographic generalisation (stroke-based street selection, mesh density)
  thins networks when a map is shown smaller than life. Gidi draws streets at real width on a 1:3 frame, so the
  real network fits without thinning; the methods were read and not needed here.

## How the lines were drawn

- Each named street is its Overture segments merged into one line per (name, kind), clipped to the border, pieces
  under 8 m dropped, no simplifying (simplifying removed junction vertices). An unnamed residential piece is a lane.
- Kinds: primary and secondary → main_road, tertiary and unclassified → local_main, named residential → home_street,
  unnamed residential and service → lane. Widths and values are Mùṣá's commonest for the kind (7.0, 8.5, 10.75 m),
  except where read.
- **Pairs**: Overture draws a divided street twice. Any two records within 4 m along more than 70% of both were merged
  into their midline, the longer id kept, the width the kind's plus the gap between them to the nearest half metre (Ijesha Road 13.5,
  Ogunlana Drive 13.5 and 14.0, Adeniyi and Akpoguma 11.0, one lane 10.5). Each merged record's note says so.
- **Apapa-Oworonshoki Expressway**: one 25 m motorway record, rd-8d0d36df, the midline of the two carriageways (4.5 m
  apart), from Mùṣá's rd-cjk9hvop end (12115.05,6370.41), 548 m, with rd-cjk9hvop's values (jersey median).
- **Slips**: Overture's primary pieces named for the expressway are its slip roads: four service_road records, each cut
  where it ran inside the motorway's 25 m; a fifth (rd-eed59480) lay wholly inside it and went.
- **Lawanson Road** (Ìtìrí's main street, the "road's life" side of the seam; Mùṣá's border followed its line,
  so Mùṣá had dropped it): four records, rd-9b617c8f (west end, tertiary, 8.5 m), rd-b07e1c75 and rd-2af50ddf at
  **10.2 m** (read at z19 at 6.51172,3.34365), rd-8a21166c and rd-f31c385c at **13.0 m** (13-14.5 m read at
  6.51273,3.35049; 13.0 so it meets Itire Road at one width). Clipping to the border left three gaps (17, 14 and
  23 m) where the line touches the seam; they were closed with straight joins within 1.2 m of the real line.

## The seam with Mùṣá (hand pass 1)

- Itire Road stays Mùṣá's (rd-r3kcqjjf). The Lawanson/Ogunlana junction node moved to Itire Road's real start
  (12826.4,6490.63), so the three meet on one point.
- Mùṣá's Dosunmu Street (rd-30weiws7) now ends at Lawanson (229.4 m, was 248.1; its verges and gutters clipped).
  Ìtìrí's 10.5 m lane piece on top of it (rd-0bd85f4f) went.
- Abeokuta Street: Ìtìrí's piece rd-9e33f97f is the stub south of Mùṣá's rd-lmd6wbjh.
- Mùṣá lanes that ran up to Lawanson (rd-3ir5l1tj, rd-9c0gondv, rd-gb8kkto3, rd-uufgfc7r, rd-ytjvbcdm, rd-zhn2pif5)
  now end on its centreline; rd-cjk9hvop and rd-sdso0qxv gained junction vertices.
- **Mùṣá houses in Ìtìrí's carriageways**: the road comes first. 25 Mùṣá houses stood in Lawanson, Mushin Road or a lane;
  22 had their front cut back to the carriageway edge + 0.05 m (each note gives the m² before and after), and 3 left
  under 12 m² or a third of themselves went (b-11a07824, b-5d145ef8, b-9eca34fa; no place linked them).
- Owed: Ogunlana Drive runs on the Sọ̀rọ̀lérè (13) seam; which district owns it is decided when Surulere is drawn.

## Every road record

| id | real name | kind | width m | length m | source |
|---|---|---|---|---|---|
| rd-8d0d36df | Apapa-Oworonshoki Expressway (carriageways) | motorway | 25.0 | 548.3 | midline of the two carriageways, values from Mùṣá rd-cjk9hvop |
| rd-1fb50e71 | Apapa-Oworonshoki Expressway | service_road | 7.0 | 32.5 | expressway slip, cut where it ran inside the motorway |
| rd-3d023846 | Apapa-Oworonshoki Expressway | service_road | 7.0 | 96.7 | expressway slip, cut where it ran inside the motorway |
| rd-8a12e51c | Apapa-Oworonshoki Expressway | service_road | 7.0 | 108.3 | expressway slip, cut where it ran inside the motorway |
| rd-f9676572 | Apapa-Oworonshoki Expressway | service_road | 7.0 | 46.8 | expressway slip, cut where it ran inside the motorway |
| rd-4388eab9 | (unnamed) | main_road | 10.75 | 8.0 | Overture line, width Mùṣá's for the kind |
| rd-d429b75f | (unnamed) | main_road | 10.75 | 17.8 | Overture line, width Mùṣá's for the kind |
| rd-d0c617ec | Ijesha Road | main_road | 13.5 | 494.4 | Overture pair merged to its midline |
| rd-2af50ddf | Lawanson Road | main_road | 10.2 | 183.5 | width read at z19 (study only); Overture pair merged to its midline |
| rd-8a21166c | Lawanson Road | main_road | 13.0 | 47.4 | width read at z19 (study only); Overture pair merged to its midline |
| rd-b07e1c75 | Lawanson Road | main_road | 10.2 | 139.3 | width read at z19 (study only); Overture pair merged to its midline |
| rd-f31c385c | Lawanson Road | main_road | 13.0 | 195.6 | width read at z19 (study only); Overture pair merged to its midline |
| rd-8078760d | Mushin Road | main_road | 10.75 | 16.6 | Overture line, width Mùṣá's for the kind |
| rd-95e589a5 | Mushin Road | main_road | 10.75 | 33.5 | Overture line, width Mùṣá's for the kind |
| rd-45205df9 | Ogunlana Drive | main_road | 13.5 | 67.2 | Overture pair merged to its midline |
| rd-586381eb | Ogunlana Drive | main_road | 14.0 | 39.7 | Overture pair merged to its midline |
| rd-629cec20 | Ogunlana Drive | main_road | 10.75 | 221.7 | Overture line, width Mùṣá's for the kind |
| rd-7fd4aeca | Ogunlana Drive | main_road | 10.75 | 15.5 | Overture line, width Mùṣá's for the kind |
| rd-9d9983bf | Ogunlana Drive | main_road | 10.75 | 11.0 | Overture line, width Mùṣá's for the kind |
| rd-d7cf5502 | Ogunlana Drive | main_road | 10.75 | 78.9 | Overture line, width Mùṣá's for the kind |
| rd-74e0bbf8 | (unnamed) | local_main | 8.5 | 14.3 | Overture line, width Mùṣá's for the kind |
| rd-b8196c1c | (unnamed) | local_main | 8.5 | 71.4 | Overture line, width Mùṣá's for the kind |
| rd-b92b7935 | (unnamed) | local_main | 8.5 | 14.8 | Overture line, width Mùṣá's for the kind |
| rd-ad7cb980 | Adeniyi Street | local_main | 11.0 | 221.6 | Overture pair merged to its midline |
| rd-64d21715 | Akpoguma Street | local_main | 8.5 | 22.0 | Overture line, width Mùṣá's for the kind |
| rd-6a24c307 | Akpoguma Street | local_main | 11.0 | 36.4 | Overture pair merged to its midline |
| rd-cc6b3d56 | Akpoguma Street | local_main | 8.5 | 41.3 | Overture line, width Mùṣá's for the kind |
| rd-5f27601c | Alhaji Masha Road | local_main | 8.5 | 23.3 | Overture line, width Mùṣá's for the kind |
| rd-e04c3cee | Alhaji Masha Road | local_main | 8.5 | 19.7 | Overture line, width Mùṣá's for the kind |
| rd-177e7ba7 | Baiye Street | local_main | 8.5 | 36.2 | Overture line, width Mùṣá's for the kind |
| rd-09453b6f | Cole Street | local_main | 8.5 | 261.3 | Overture line, width Mùṣá's for the kind |
| rd-19b2d3f6 | Itire Road | local_main | 8.5 | 16.9 | Overture line, width Mùṣá's for the kind |
| rd-4b8ac1dc | Jubril Martins Street | local_main | 8.5 | 362.9 | Overture line, width Mùṣá's for the kind |
| rd-730ec296 | Kabiyesi Street | local_main | 8.5 | 28.7 | Overture line, width Mùṣá's for the kind |
| rd-9b617c8f | Lawanson Road | local_main | 8.5 | 91.3 | Overture line, width Mùṣá's for the kind |
| rd-fbef86f9 | Olatilewa Street | local_main | 8.5 | 16.5 | Overture line, width Mùṣá's for the kind |
| rd-ab634fae | Olufemi Street | local_main | 8.5 | 139.5 | Overture line, width Mùṣá's for the kind |
| rd-95432ac6 | Abayomi Street | home_street | 7.0 | 181.1 | Overture line, width Mùṣá's for the kind |
| rd-9e33f97f | Abeokuta Street | home_street | 7.0 | 13.5 | Overture line, width Mùṣá's for the kind |
| rd-6bc9ecee | Abimbola Street | home_street | 7.0 | 20.9 | Overture line, width Mùṣá's for the kind |
| rd-d61ee371 | Abiodun Wright Street | home_street | 7.0 | 125.4 | Overture line, width Mùṣá's for the kind |
| rd-2eb3109c | Adamson Street | home_street | 7.0 | 47.8 | Overture line, width Mùṣá's for the kind |
| rd-118231ad | Adebisi Close | home_street | 7.0 | 33.3 | Overture line, width Mùṣá's for the kind |
| rd-4f21eb0b | Adebisi Street | home_street | 7.0 | 33.2 | Overture line, width Mùṣá's for the kind |
| rd-8aa387b1 | Adedeji Street | home_street | 7.0 | 158.4 | Overture line, width Mùṣá's for the kind |
| rd-71289f92 | Adefimihan Street | home_street | 7.0 | 131.9 | Overture line, width Mùṣá's for the kind |
| rd-3d3c7fa3 | Adegbola Street | home_street | 7.0 | 83.1 | Overture line, width Mùṣá's for the kind |
| rd-0acced8a | Adegoke Street | home_street | 7.0 | 136.6 | Overture line, width Mùṣá's for the kind |
| rd-1070e7d9 | Adegoke Street Link | home_street | 7.0 | 25.3 | Overture line, width Mùṣá's for the kind |
| rd-b000ad69 | Adekoya Street | home_street | 7.0 | 52.1 | Overture line, width Mùṣá's for the kind |
| rd-0280206a | Adekunle Kuy Street | home_street | 7.0 | 104.7 | Overture line, width Mùṣá's for the kind |
| rd-010ab44f | Adenike Street | home_street | 7.0 | 24.6 | Overture line, width Mùṣá's for the kind |
| rd-42c04150 | Adeniyi Street | home_street | 7.0 | 63.4 | Overture line, width Mùṣá's for the kind |
| rd-7054b783 | Adeniyi Street | home_street | 7.0 | 13.1 | Overture line, width Mùṣá's for the kind |
| rd-eced0e00 | Adeosun Street | home_street | 7.0 | 148.7 | Overture line, width Mùṣá's for the kind |
| rd-40ece18e | Aderibigbe Street | home_street | 7.0 | 120.2 | Overture line, width Mùṣá's for the kind |
| rd-d82a5c19 | Adeshina Street | home_street | 7.0 | 76.2 | Overture line, width Mùṣá's for the kind |
| rd-88cc606f | Afolabi Dada Street | home_street | 7.0 | 51.5 | Overture line, width Mùṣá's for the kind |
| rd-d807b0a5 | Agbela Street | home_street | 7.0 | 27.4 | Overture line, width Mùṣá's for the kind |
| rd-bae4d5d1 | Agoro Street | home_street | 7.0 | 16.5 | Overture line, width Mùṣá's for the kind |
| rd-ee71c2a1 | Aina Street | home_street | 7.0 | 193.9 | Overture line, width Mùṣá's for the kind |
| rd-058ff40a | Ajao Street | home_street | 7.0 | 186.5 | Overture line, width Mùṣá's for the kind |
| rd-dbba6c78 | Ajoke Street | home_street | 7.0 | 114.6 | Overture line, width Mùṣá's for the kind |
| rd-744b0794 | Akanji Street | home_street | 7.0 | 81.4 | Overture line, width Mùṣá's for the kind |
| rd-6ad3975a | Akin Oluwolaba Road | home_street | 7.0 | 49.9 | Overture line, width Mùṣá's for the kind |
| rd-2f92c4a8 | Akindelu Street | home_street | 7.0 | 62.6 | Overture line, width Mùṣá's for the kind |
| rd-96a21afd | Akinkunmi Street | home_street | 7.0 | 144.7 | Overture line, width Mùṣá's for the kind |
| rd-e11bba7e | Akinwunmi Street | home_street | 7.0 | 61.4 | Overture line, width Mùṣá's for the kind |
| rd-e3a6bcce | Akinyele Street | home_street | 7.0 | 42.7 | Overture line, width Mùṣá's for the kind |
| rd-475f244f | Akpoguma Street | home_street | 7.0 | 256.4 | Overture line, width Mùṣá's for the kind |
| rd-df0f0729 | Alafia Street | home_street | 7.0 | 182.2 | Overture line, width Mùṣá's for the kind |
| rd-0359b3be | Aleje Street | home_street | 7.0 | 39.9 | Overture line, width Mùṣá's for the kind |
| rd-9639aa93 | Alhaji Nuru Street | home_street | 7.0 | 66.7 | Overture line, width Mùṣá's for the kind |
| rd-a834a208 | Alhaji Otun Street | home_street | 7.0 | 23.0 | Overture line, width Mùṣá's for the kind |
| rd-b640424b | Anjorin Lane | home_street | 7.0 | 24.6 | Overture line, width Mùṣá's for the kind |
| rd-dfe3282f | Anjorin Street | home_street | 7.0 | 157.8 | Overture line, width Mùṣá's for the kind |
| rd-e27eeea9 | Arowosere Street | home_street | 7.0 | 56.1 | Overture line, width Mùṣá's for the kind |
| rd-a1bd9848 | Ashimowu Bakare Street | home_street | 7.0 | 181.3 | Overture line, width Mùṣá's for the kind |
| rd-65ab95b7 | Ayepe Street | home_street | 7.0 | 90.6 | Overture line, width Mùṣá's for the kind |
| rd-0bbadf16 | Ayisatu Street | home_street | 7.0 | 52.3 | Overture line, width Mùṣá's for the kind |
| rd-53cc367e | Ayo Idowu Close | home_street | 7.0 | 42.5 | Overture line, width Mùṣá's for the kind |
| rd-8620f0eb | Ayodele Street | home_street | 7.0 | 128.7 | Overture line, width Mùṣá's for the kind |
| rd-ad055a35 | Babatunde Road | home_street | 7.0 | 125.2 | Overture line, width Mùṣá's for the kind |
| rd-0b43405f | Badaru Street | home_street | 7.0 | 52.0 | Overture line, width Mùṣá's for the kind |
| rd-496120e2 | Balogun Lane | home_street | 7.0 | 64.5 | Overture line, width Mùṣá's for the kind |
| rd-93bf9fcc | Balogun Street | home_street | 7.0 | 25.1 | Overture line, width Mùṣá's for the kind |
| rd-d8f395ca | Baoku Street | home_street | 7.0 | 35.8 | Overture line, width Mùṣá's for the kind |
| rd-c9abda39 | Brown Road | home_street | 7.0 | 28.4 | Overture line, width Mùṣá's for the kind |
| rd-57d463fb | Buraimoh Street | home_street | 7.0 | 101.1 | Overture line, width Mùṣá's for the kind |
| rd-7cc18070 | Coast-U Feli Street | home_street | 7.0 | 23.8 | Overture line, width Mùṣá's for the kind |
| rd-2ca2e404 | Dayo Ojutiku Street | home_street | 7.0 | 99.2 | Overture line, width Mùṣá's for the kind |
| rd-8fa732b6 | Dipo Olubi Street | home_street | 7.0 | 146.7 | Overture line, width Mùṣá's for the kind |
| rd-bc55d25b | Durojaiye Street | home_street | 7.0 | 83.2 | Overture line, width Mùṣá's for the kind |
| rd-577a7406 | Ebenezer Lane | home_street | 7.0 | 22.7 | Overture line, width Mùṣá's for the kind |
| rd-e9190f62 | Ebun Street | home_street | 7.0 | 51.3 | Overture line, width Mùṣá's for the kind |
| rd-b9bd2468 | Elaloro Street | home_street | 7.0 | 68.9 | Overture line, width Mùṣá's for the kind |
| rd-6fa29a32 | Eloseh Street | home_street | 7.0 | 70.5 | Overture line, width Mùṣá's for the kind |
| rd-63315c20 | Eniyanosoro Beyioku Road | home_street | 7.0 | 84.1 | Overture line, width Mùṣá's for the kind |
| rd-0889d103 | Erinosho Street | home_street | 7.0 | 257.6 | Overture line, width Mùṣá's for the kind |
| rd-00a9fb86 | Eshinlokun Street | home_street | 7.0 | 76.0 | Overture line, width Mùṣá's for the kind |
| rd-f41778b3 | Fajobi Olaofe Street | home_street | 7.0 | 19.9 | Overture line, width Mùṣá's for the kind |
| rd-ede72da8 | Folawiyo Bankole Street | home_street | 7.0 | 109.7 | Overture line, width Mùṣá's for the kind |
| rd-0017b628 | Gasper Street | home_street | 7.0 | 104.0 | Overture line, width Mùṣá's for the kind |
| rd-fe7c919b | Gbadamosi Street | home_street | 7.0 | 29.0 | Overture line, width Mùṣá's for the kind |
| rd-287e1e9c | Ibidun Street | home_street | 7.0 | 66.6 | Overture line, width Mùṣá's for the kind |
| rd-89a56b41 | Idowu Street | home_street | 7.0 | 67.2 | Overture line, width Mùṣá's for the kind |
| rd-b47b6dc9 | Igbesa Street | home_street | 7.0 | 59.9 | Overture line, width Mùṣá's for the kind |
| rd-41e335f7 | Ijaiye Street | home_street | 7.0 | 169.2 | Overture line, width Mùṣá's for the kind |
| rd-24e4960c | Ikenne Close | home_street | 7.0 | 12.3 | Overture line, width Mùṣá's for the kind |
| rd-6ef8fd67 | Ikenne Street | home_street | 7.0 | 76.5 | Overture line, width Mùṣá's for the kind |
| rd-799f18a8 | Ikpoh Street | home_street | 7.0 | 69.1 | Overture line, width Mùṣá's for the kind |
| rd-da593a08 | Ilarogun Close | home_street | 7.0 | 28.0 | Overture line, width Mùṣá's for the kind |
| rd-fc5ee612 | Ilesanmi Street | home_street | 7.0 | 153.0 | Overture line, width Mùṣá's for the kind |
| rd-ee28429c | Isiba Street | home_street | 7.0 | 97.0 | Overture line, width Mùṣá's for the kind |
| rd-7c602b1c | Itelorun Street | home_street | 7.0 | 78.4 | Overture line, width Mùṣá's for the kind |
| rd-094d57cc | Jimoh Ojuku Street | home_street | 7.0 | 60.0 | Overture line, width Mùṣá's for the kind |
| rd-032a66f8 | Joe Dunmade Close | home_street | 7.0 | 57.2 | Overture line, width Mùṣá's for the kind |
| rd-6b5f8217 | Kabiyesi Street | home_street | 7.0 | 57.2 | Overture line, width Mùṣá's for the kind |
| rd-70e5e7c1 | Kabiyesi Street | home_street | 7.0 | 36.4 | Overture line, width Mùṣá's for the kind |
| rd-503c7e8e | Kadiri Street | home_street | 7.0 | 81.4 | Overture line, width Mùṣá's for the kind |
| rd-f096e9a7 | Karounwi Street | home_street | 7.0 | 159.3 | Overture line, width Mùṣá's for the kind |
| rd-9d9b749a | Koya Street | home_street | 7.0 | 39.6 | Overture line, width Mùṣá's for the kind |
| rd-8eeeeda7 | Ladejobi Street | home_street | 7.0 | 46.3 | Overture line, width Mùṣá's for the kind |
| rd-cb0b976f | Manugo Street | home_street | 7.0 | 53.2 | Overture line, width Mùṣá's for the kind |
| rd-588d1025 | Memedu Aremu Street | home_street | 7.0 | 110.0 | Overture line, width Mùṣá's for the kind |
| rd-eb605ed8 | Modupe Ore Crescent | home_street | 7.0 | 75.8 | Overture line, width Mùṣá's for the kind |
| rd-7da2ca67 | Mogaji Close | home_street | 7.0 | 17.5 | Overture line, width Mùṣá's for the kind |
| rd-1ebb84ee | Molusi Street | home_street | 7.0 | 96.0 | Overture line, width Mùṣá's for the kind |
| rd-6ba2b21b | Muniru Baruwa Street | home_street | 7.0 | 47.8 | Overture line, width Mùṣá's for the kind |
| rd-9d30c424 | Mutairu Onigbanjo Street | home_street | 7.0 | 154.5 | Overture line, width Mùṣá's for the kind |
| rd-29fe0c5d | Obasun Link Street | home_street | 7.0 | 8.1 | Overture line, width Mùṣá's for the kind |
| rd-21032350 | Odubiyi Street | home_street | 7.0 | 187.9 | Overture line, width Mùṣá's for the kind |
| rd-fba3c931 | Oduduwa Street | home_street | 7.0 | 52.8 | Overture line, width Mùṣá's for the kind |
| rd-72eac8bf | Ogunlana Street | home_street | 7.0 | 73.6 | Overture line, width Mùṣá's for the kind |
| rd-b39f5b13 | Ogunleye Street | home_street | 7.0 | 86.4 | Overture line, width Mùṣá's for the kind |
| rd-eef61ff2 | Ogunsami Street | home_street | 7.0 | 243.2 | Overture line, width Mùṣá's for the kind |
| rd-8f3751cc | Okeona Street | home_street | 7.0 | 120.3 | Overture line, width Mùṣá's for the kind |
| rd-99587e46 | Oladeinde Street | home_street | 7.0 | 37.9 | Overture line, width Mùṣá's for the kind |
| rd-500ce8bc | Olagunju Close | home_street | 7.0 | 23.1 | Overture line, width Mùṣá's for the kind |
| rd-fc78859e | Olaide Street | home_street | 7.0 | 132.4 | Overture line, width Mùṣá's for the kind |
| rd-3e14a279 | Olaitan Odularu Street | home_street | 7.0 | 204.0 | Overture line, width Mùṣá's for the kind |
| rd-ac4c3c66 | Olaitan Onasanya Street | home_street | 7.0 | 23.5 | Overture line, width Mùṣá's for the kind |
| rd-48cc70f7 | Olamojuba Street | home_street | 7.0 | 94.5 | Overture line, width Mùṣá's for the kind |
| rd-8025cd9a | Olaogun Street | home_street | 7.0 | 24.5 | Overture line, width Mùṣá's for the kind |
| rd-e52e544b | Olaogun Street | home_street | 7.0 | 38.5 | Overture line, width Mùṣá's for the kind |
| rd-58832f21 | Olaseni Diyaolu Street | home_street | 7.0 | 54.3 | Overture line, width Mùṣá's for the kind |
| rd-b886bb91 | Olatilewa Street | home_street | 7.0 | 190.2 | Overture line, width Mùṣá's for the kind |
| rd-0fa8068b | Olayemi Street | home_street | 7.0 | 31.6 | Overture line, width Mùṣá's for the kind |
| rd-4f5310b0 | Olukole Close | home_street | 7.0 | 14.0 | Overture line, width Mùṣá's for the kind |
| rd-d93b1251 | Olukole Street | home_street | 7.0 | 141.5 | Overture line, width Mùṣá's for the kind |
| rd-74df6dd6 | Olushola Keku Street | home_street | 7.0 | 89.7 | Overture line, width Mùṣá's for the kind |
| rd-8cfe2139 | Ominiyi Street | home_street | 7.0 | 55.5 | Overture line, width Mùṣá's for the kind |
| rd-cacd0d59 | Omodunni Street | home_street | 7.0 | 78.8 | Overture line, width Mùṣá's for the kind |
| rd-e68e95c8 | Omosebi Street | home_street | 7.0 | 15.5 | Overture line, width Mùṣá's for the kind |
| rd-2a6a5020 | Omosolape Street | home_street | 7.0 | 61.0 | Overture line, width Mùṣá's for the kind |
| rd-3829817b | Onadeko Street | home_street | 7.0 | 84.5 | Overture line, width Mùṣá's for the kind |
| rd-349d2378 | Onibuore Street | home_street | 7.0 | 40.6 | Overture line, width Mùṣá's for the kind |
| rd-996727cc | Onibuore Street | home_street | 7.0 | 47.4 | Overture line, width Mùṣá's for the kind |
| rd-dfe49db9 | Onibuore Street | home_street | 7.0 | 95.9 | Overture line, width Mùṣá's for the kind |
| rd-ec4ff756 | Oremeji Street | home_street | 7.0 | 72.8 | Overture line, width Mùṣá's for the kind |
| rd-4f987102 | Oshoba Close | home_street | 7.0 | 51.2 | Overture line, width Mùṣá's for the kind |
| rd-f61b4879 | Oshofisan Street | home_street | 7.0 | 79.8 | Overture line, width Mùṣá's for the kind |
| rd-7c7e1a25 | Raimi Street | home_street | 7.0 | 36.3 | Overture line, width Mùṣá's for the kind |
| rd-8bbb8cdc | Ramoni Oke Street | home_street | 7.0 | 92.9 | Overture line, width Mùṣá's for the kind |
| rd-1c85c635 | Ramoni Street | home_street | 7.0 | 138.0 | Overture line, width Mùṣá's for the kind |
| rd-ecf86609 | Rosanwo Street | home_street | 7.0 | 95.5 | Overture line, width Mùṣá's for the kind |
| rd-71d40848 | Saibu Lawal Street | home_street | 7.0 | 29.3 | Overture line, width Mùṣá's for the kind |
| rd-ba0ce940 | Salami Bashorun Street | home_street | 7.0 | 117.6 | Overture line, width Mùṣá's for the kind |
| rd-11ea59df | Salami Oke Street | home_street | 7.0 | 28.2 | Overture line, width Mùṣá's for the kind |
| rd-574c1693 | Sam Shonibare Street | home_street | 7.0 | 88.2 | Overture line, width Mùṣá's for the kind |
| rd-a467e20b | Sam Shonibare Street | home_street | 7.0 | 24.1 | Overture line, width Mùṣá's for the kind |
| rd-b535717d | Sam Shonibare Street | home_street | 7.0 | 90.9 | Overture line, width Mùṣá's for the kind |
| rd-7ea4ef01 | Sariyu Street | home_street | 7.0 | 63.4 | Overture line, width Mùṣá's for the kind |
| rd-2d0eccf4 | Shaki Crescent | home_street | 7.0 | 92.3 | Overture line, width Mùṣá's for the kind |
| rd-228c5bed | Shofidiya Close | home_street | 7.0 | 25.5 | Overture line, width Mùṣá's for the kind |
| rd-9b005163 | Shonde Street | home_street | 7.0 | 41.2 | Overture line, width Mùṣá's for the kind |
| rd-daf8aed1 | Shotayo Hughes Street | home_street | 7.0 | 95.0 | Overture line, width Mùṣá's for the kind |
| rd-962a0b8b | Shoyinka Street | home_street | 7.0 | 95.1 | Overture line, width Mùṣá's for the kind |
| rd-107c4fa4 | Shoyomokun Street | home_street | 7.0 | 79.7 | Overture line, width Mùṣá's for the kind |
| rd-ecc6159d | Simisola Street | home_street | 7.0 | 71.3 | Overture line, width Mùṣá's for the kind |
| rd-deb93b25 | Subuola Road | home_street | 7.0 | 72.3 | Overture line, width Mùṣá's for the kind |
| rd-b21af2d5 | Tali Eniola Street | home_street | 7.0 | 99.8 | Overture line, width Mùṣá's for the kind |
| rd-dc212dcd | Temidire Street | home_street | 7.0 | 48.9 | Overture line, width Mùṣá's for the kind |
| rd-f768bea7 | Tossou Street | home_street | 7.0 | 45.9 | Overture line, width Mùṣá's for the kind |
| rd-a5b2173b | Twins Street | home_street | 7.0 | 134.1 | Overture line, width Mùṣá's for the kind |
| rd-cabe7422 | Victoria Street | home_street | 7.0 | 39.0 | Overture line, width Mùṣá's for the kind |
| rd-ab1c3000 | Yaru Street | home_street | 7.0 | 67.5 | Overture line, width Mùṣá's for the kind |
| rd-7fc63f2c | Zamba Street | home_street | 7.0 | 165.2 | Overture line, width Mùṣá's for the kind |
| rd-003163a8 | (unnamed) | lane | 7.0 | 131.7 | Overture line, width Mùṣá's for the kind |
| rd-00963a22 | (unnamed) | lane | 7.0 | 13.4 | Overture line, width Mùṣá's for the kind |
| rd-0206f47f | (unnamed) | lane | 7.0 | 72.2 | Overture line, width Mùṣá's for the kind |
| rd-037ff6d7 | (unnamed) | lane | 7.0 | 40.4 | Overture line, width Mùṣá's for the kind |
| rd-045745b5 | (unnamed) | lane | 7.0 | 41.9 | Overture line, width Mùṣá's for the kind |
| rd-051cf511 | (unnamed) | lane | 7.0 | 133.3 | Overture line, width Mùṣá's for the kind |
| rd-05a86216 | (unnamed) | lane | 7.0 | 34.4 | Overture line, width Mùṣá's for the kind |
| rd-068edd83 | (unnamed) | lane | 7.0 | 14.8 | Overture line, width Mùṣá's for the kind |
| rd-0774e0d1 | (unnamed) | lane | 7.0 | 53.4 | Overture line, width Mùṣá's for the kind |
| rd-07b590c7 | (unnamed) | lane | 7.0 | 33.7 | Overture line, width Mùṣá's for the kind |
| rd-07f68f9f | (unnamed) | lane | 7.0 | 30.8 | Overture line, width Mùṣá's for the kind |
| rd-0a04e11c | (unnamed) | lane | 7.0 | 5.3 | Overture line, width Mùṣá's for the kind |
| rd-0d9096ba | (unnamed) | lane | 7.0 | 25.5 | Overture line, width Mùṣá's for the kind |
| rd-0dcb2eb3 | (unnamed) | lane | 7.0 | 18.8 | Overture line, width Mùṣá's for the kind |
| rd-0e5d7299 | (unnamed) | lane | 7.0 | 14.9 | Overture line, width Mùṣá's for the kind |
| rd-0ec45374 | (unnamed) | lane | 7.0 | 24.7 | Overture line, width Mùṣá's for the kind |
| rd-0f0a9839 | (unnamed) | lane | 7.0 | 41.0 | Overture line, width Mùṣá's for the kind |
| rd-0f7b6c2f | (unnamed) | lane | 7.0 | 29.0 | Overture line, width Mùṣá's for the kind |
| rd-10fc6ba5 | (unnamed) | lane | 7.0 | 72.6 | Overture line, width Mùṣá's for the kind |
| rd-11c521b0 | (unnamed) | lane | 7.0 | 25.1 | Overture line, width Mùṣá's for the kind |
| rd-121233e2 | (unnamed) | lane | 7.0 | 50.7 | Overture line, width Mùṣá's for the kind |
| rd-1506caa6 | (unnamed) | lane | 7.0 | 25.7 | Overture line, width Mùṣá's for the kind |
| rd-1663e106 | (unnamed) | lane | 7.0 | 72.1 | Overture line, width Mùṣá's for the kind |
| rd-19040add | (unnamed) | lane | 7.0 | 28.6 | Overture line, width Mùṣá's for the kind |
| rd-1a61dea0 | (unnamed) | lane | 7.0 | 159.4 | Overture line, width Mùṣá's for the kind |
| rd-1a6c760e | (unnamed) | lane | 7.0 | 26.0 | Overture line, width Mùṣá's for the kind |
| rd-1b0d90d3 | (unnamed) | lane | 7.0 | 16.9 | Overture line, width Mùṣá's for the kind |
| rd-1bb18469 | (unnamed) | lane | 7.0 | 23.6 | Overture line, width Mùṣá's for the kind |
| rd-1bff4864 | (unnamed) | lane | 7.0 | 66.6 | Overture line, width Mùṣá's for the kind |
| rd-1f6884ef | (unnamed) | lane | 7.0 | 26.7 | Overture line, width Mùṣá's for the kind |
| rd-1fa988ee | (unnamed) | lane | 7.0 | 25.7 | Overture line, width Mùṣá's for the kind |
| rd-21142d8b | (unnamed) | lane | 7.0 | 26.7 | Overture line, width Mùṣá's for the kind |
| rd-231d41b1 | (unnamed) | lane | 7.0 | 22.8 | Overture line, width Mùṣá's for the kind |
| rd-2485d38f | (unnamed) | lane | 7.0 | 55.1 | Overture line, width Mùṣá's for the kind |
| rd-2505f00d | (unnamed) | lane | 7.0 | 22.0 | Overture line, width Mùṣá's for the kind |
| rd-26c037f4 | (unnamed) | lane | 7.0 | 25.8 | Overture line, width Mùṣá's for the kind |
| rd-283c122d | (unnamed) | lane | 7.0 | 24.7 | Overture line, width Mùṣá's for the kind |
| rd-298fc378 | (unnamed) | lane | 7.0 | 13.6 | Overture line, width Mùṣá's for the kind |
| rd-2e62c648 | (unnamed) | lane | 7.0 | 23.1 | Overture line, width Mùṣá's for the kind |
| rd-2f655fb3 | (unnamed) | lane | 7.0 | 38.9 | Overture line, width Mùṣá's for the kind |
| rd-3277bb30 | (unnamed) | lane | 7.0 | 54.0 | Overture line, width Mùṣá's for the kind |
| rd-344de239 | (unnamed) | lane | 7.0 | 18.4 | Overture line, width Mùṣá's for the kind |
| rd-3793211b | (unnamed) | lane | 7.0 | 13.9 | Overture line, width Mùṣá's for the kind |
| rd-37c228b0 | (unnamed) | lane | 7.0 | 150.0 | Overture line, width Mùṣá's for the kind |
| rd-38147786 | (unnamed) | lane | 7.0 | 27.2 | Overture line, width Mùṣá's for the kind |
| rd-3864a72f | (unnamed) | lane | 10.5 | 22.4 | Overture pair merged to its midline |
| rd-3908227b | (unnamed) | lane | 7.0 | 55.3 | Overture line, width Mùṣá's for the kind |
| rd-3adaa838 | (unnamed) | lane | 7.0 | 15.3 | Overture line, width Mùṣá's for the kind |
| rd-3c596d42 | (unnamed) | lane | 7.0 | 39.0 | Overture line, width Mùṣá's for the kind |
| rd-3c843903 | (unnamed) | lane | 7.0 | 15.7 | Overture line, width Mùṣá's for the kind |
| rd-3d020b44 | (unnamed) | lane | 7.0 | 23.4 | Overture line, width Mùṣá's for the kind |
| rd-3d371e95 | (unnamed) | lane | 7.0 | 22.5 | Overture line, width Mùṣá's for the kind |
| rd-452e8451 | (unnamed) | lane | 7.0 | 22.2 | Overture line, width Mùṣá's for the kind |
| rd-45a691c3 | (unnamed) | lane | 7.0 | 27.1 | Overture line, width Mùṣá's for the kind |
| rd-4644973c | (unnamed) | lane | 7.0 | 20.2 | Overture line, width Mùṣá's for the kind |
| rd-46c7cf85 | (unnamed) | lane | 7.0 | 83.3 | Overture line, width Mùṣá's for the kind |
| rd-47c81beb | (unnamed) | lane | 7.0 | 50.7 | Overture line, width Mùṣá's for the kind |
| rd-47f92a13 | (unnamed) | lane | 7.0 | 17.6 | Overture line, width Mùṣá's for the kind |
| rd-4a3ad792 | (unnamed) | lane | 7.0 | 30.7 | Overture line, width Mùṣá's for the kind |
| rd-4b7aa6ac | (unnamed) | lane | 7.0 | 31.7 | Overture line, width Mùṣá's for the kind |
| rd-4ccc8b52 | (unnamed) | lane | 7.0 | 9.0 | Overture line, width Mùṣá's for the kind |
| rd-4e43153b | (unnamed) | lane | 7.0 | 19.6 | Overture line, width Mùṣá's for the kind |
| rd-4e58a075 | (unnamed) | lane | 7.0 | 52.7 | Overture line, width Mùṣá's for the kind |
| rd-4f537d3f | (unnamed) | lane | 7.0 | 11.2 | Overture line, width Mùṣá's for the kind |
| rd-51bc5bd7 | (unnamed) | lane | 7.0 | 23.8 | Overture line, width Mùṣá's for the kind |
| rd-5410b1b9 | (unnamed) | lane | 7.0 | 158.4 | Overture line, width Mùṣá's for the kind |
| rd-5461fb96 | (unnamed) | lane | 7.0 | 9.2 | Overture line, width Mùṣá's for the kind |
| rd-548ec04d | (unnamed) | lane | 7.0 | 30.6 | Overture line, width Mùṣá's for the kind |
| rd-594105d2 | (unnamed) | lane | 7.0 | 34.4 | Overture line, width Mùṣá's for the kind |
| rd-5d832ad1 | (unnamed) | lane | 7.0 | 52.3 | Overture line, width Mùṣá's for the kind |
| rd-60b5dd7d | (unnamed) | lane | 7.0 | 109.5 | Overture line, width Mùṣá's for the kind |
| rd-60c36fd9 | (unnamed) | lane | 7.0 | 70.4 | Overture line, width Mùṣá's for the kind |
| rd-60f0d0ad | (unnamed) | lane | 7.0 | 103.1 | Overture line, width Mùṣá's for the kind |
| rd-61343252 | (unnamed) | lane | 7.0 | 58.5 | Overture line, width Mùṣá's for the kind |
| rd-64aabbcd | (unnamed) | lane | 7.0 | 22.6 | Overture line, width Mùṣá's for the kind |
| rd-681c5231 | (unnamed) | lane | 7.0 | 130.4 | Overture line, width Mùṣá's for the kind |
| rd-6858b63f | (unnamed) | lane | 7.0 | 91.1 | Overture line, width Mùṣá's for the kind |
| rd-690cfb01 | (unnamed) | lane | 7.0 | 50.0 | Overture line, width Mùṣá's for the kind |
| rd-6a8d2ab9 | (unnamed) | lane | 7.0 | 23.8 | Overture line, width Mùṣá's for the kind |
| rd-6d10f6e0 | (unnamed) | lane | 7.0 | 16.7 | Overture line, width Mùṣá's for the kind |
| rd-6e22c44f | (unnamed) | lane | 7.0 | 103.9 | Overture line, width Mùṣá's for the kind |
| rd-6e586afe | (unnamed) | lane | 7.0 | 17.8 | Overture line, width Mùṣá's for the kind |
| rd-72cd8dc2 | (unnamed) | lane | 7.0 | 22.3 | Overture line, width Mùṣá's for the kind |
| rd-75b10e35 | (unnamed) | lane | 7.0 | 59.2 | Overture line, width Mùṣá's for the kind |
| rd-76546a55 | (unnamed) | lane | 7.0 | 11.1 | Overture line, width Mùṣá's for the kind |
| rd-766a906e | (unnamed) | lane | 7.0 | 87.4 | Overture line, width Mùṣá's for the kind |
| rd-7727009b | (unnamed) | lane | 7.0 | 23.4 | Overture line, width Mùṣá's for the kind |
| rd-77da3589 | (unnamed) | lane | 7.0 | 107.5 | Overture line, width Mùṣá's for the kind |
| rd-78661816 | (unnamed) | lane | 7.0 | 12.1 | Overture line, width Mùṣá's for the kind |
| rd-78ba85cf | (unnamed) | lane | 7.0 | 95.5 | Overture line, width Mùṣá's for the kind |
| rd-7f2cb74c | (unnamed) | lane | 7.0 | 37.2 | Overture line, width Mùṣá's for the kind |
| rd-8021d095 | (unnamed) | lane | 7.0 | 21.0 | Overture line, width Mùṣá's for the kind |
| rd-81d0735c | (unnamed) | lane | 7.0 | 21.9 | Overture line, width Mùṣá's for the kind |
| rd-824e1a63 | (unnamed) | lane | 7.0 | 208.6 | Overture line, width Mùṣá's for the kind |
| rd-828466cd | (unnamed) | lane | 7.0 | 22.5 | Overture line, width Mùṣá's for the kind |
| rd-83959654 | (unnamed) | lane | 7.0 | 32.9 | Overture line, width Mùṣá's for the kind |
| rd-839929b5 | (unnamed) | lane | 7.0 | 20.8 | Overture line, width Mùṣá's for the kind |
| rd-83d672c8 | (unnamed) | lane | 7.0 | 59.3 | Overture line, width Mùṣá's for the kind |
| rd-84593faa | (unnamed) | lane | 7.0 | 17.7 | Overture line, width Mùṣá's for the kind |
| rd-862bc393 | (unnamed) | lane | 7.0 | 24.2 | Overture line, width Mùṣá's for the kind |
| rd-89c78af8 | (unnamed) | lane | 7.0 | 22.9 | Overture line, width Mùṣá's for the kind |
| rd-8dbc4613 | (unnamed) | lane | 7.0 | 137.7 | Overture line, width Mùṣá's for the kind |
| rd-8e3b9c2a | (unnamed) | lane | 7.0 | 31.9 | Overture line, width Mùṣá's for the kind |
| rd-8f881320 | (unnamed) | lane | 7.0 | 67.0 | Overture line, width Mùṣá's for the kind |
| rd-91f4cd2d | (unnamed) | lane | 7.0 | 37.4 | Overture line, width Mùṣá's for the kind |
| rd-92f57ddd | (unnamed) | lane | 7.0 | 48.4 | Overture line, width Mùṣá's for the kind |
| rd-94459bd1 | (unnamed) | lane | 7.0 | 14.1 | Overture line, width Mùṣá's for the kind |
| rd-95affed8 | (unnamed) | lane | 7.0 | 24.4 | Overture line, width Mùṣá's for the kind |
| rd-97bac96d | (unnamed) | lane | 7.0 | 13.3 | Overture line, width Mùṣá's for the kind |
| rd-9a9c4cae | (unnamed) | lane | 7.0 | 14.2 | Overture line, width Mùṣá's for the kind |
| rd-9d302add | (unnamed) | lane | 7.0 | 72.9 | Overture line, width Mùṣá's for the kind |
| rd-9efb3737 | (unnamed) | lane | 7.0 | 97.7 | Overture line, width Mùṣá's for the kind |
| rd-a3e5230a | (unnamed) | lane | 7.0 | 19.3 | Overture line, width Mùṣá's for the kind |
| rd-a4e158b3 | (unnamed) | lane | 7.0 | 19.3 | Overture line, width Mùṣá's for the kind |
| rd-a6ffb6b1 | (unnamed) | lane | 7.0 | 12.7 | Overture line, width Mùṣá's for the kind |
| rd-a72bbb50 | (unnamed) | lane | 7.0 | 9.5 | Overture line, width Mùṣá's for the kind |
| rd-a76480a8 | (unnamed) | lane | 7.0 | 29.3 | Overture line, width Mùṣá's for the kind |
| rd-a81ceb6e | (unnamed) | lane | 7.0 | 45.3 | Overture line, width Mùṣá's for the kind |
| rd-a9bbe336 | (unnamed) | lane | 7.0 | 20.5 | Overture line, width Mùṣá's for the kind |
| rd-aab6ecd3 | (unnamed) | lane | 7.0 | 32.9 | Overture line, width Mùṣá's for the kind |
| rd-ac9f83cd | (unnamed) | lane | 7.0 | 19.5 | Overture line, width Mùṣá's for the kind |
| rd-aedb9c92 | (unnamed) | lane | 7.0 | 37.3 | Overture line, width Mùṣá's for the kind |
| rd-b059a5a4 | (unnamed) | lane | 7.0 | 18.5 | Overture line, width Mùṣá's for the kind |
| rd-b54a2a48 | (unnamed) | lane | 7.0 | 34.1 | Overture line, width Mùṣá's for the kind |
| rd-b5adecfb | (unnamed) | lane | 7.0 | 35.7 | Overture line, width Mùṣá's for the kind |
| rd-b6f32b94 | (unnamed) | lane | 7.0 | 95.2 | Overture line, width Mùṣá's for the kind |
| rd-b6f6cd95 | (unnamed) | lane | 7.0 | 21.3 | Overture line, width Mùṣá's for the kind |
| rd-b74d79e8 | (unnamed) | lane | 7.0 | 28.3 | Overture line, width Mùṣá's for the kind |
| rd-b8432309 | (unnamed) | lane | 7.0 | 21.9 | Overture line, width Mùṣá's for the kind |
| rd-ba21e177 | (unnamed) | lane | 7.0 | 20.8 | Overture line, width Mùṣá's for the kind |
| rd-ba696d48 | (unnamed) | lane | 7.0 | 24.7 | Overture line, width Mùṣá's for the kind |
| rd-ba9d47ec | (unnamed) | lane | 7.0 | 10.8 | Overture line, width Mùṣá's for the kind |
| rd-bdb14732 | (unnamed) | lane | 7.0 | 40.7 | Overture line, width Mùṣá's for the kind |
| rd-c0233967 | (unnamed) | lane | 7.0 | 71.2 | Overture line, width Mùṣá's for the kind |
| rd-c31b25f3 | (unnamed) | lane | 7.0 | 28.8 | Overture line, width Mùṣá's for the kind |
| rd-c42738d4 | (unnamed) | lane | 7.0 | 39.2 | Overture line, width Mùṣá's for the kind |
| rd-c570a081 | (unnamed) | lane | 7.0 | 41.9 | Overture line, width Mùṣá's for the kind |
| rd-c5be012b | (unnamed) | lane | 7.0 | 8.2 | Overture line, width Mùṣá's for the kind |
| rd-c78f85e8 | (unnamed) | lane | 7.0 | 19.1 | Overture line, width Mùṣá's for the kind |
| rd-c7d39ab4 | (unnamed) | lane | 7.0 | 20.1 | Overture line, width Mùṣá's for the kind |
| rd-ca451130 | (unnamed) | lane | 7.0 | 40.0 | Overture line, width Mùṣá's for the kind |
| rd-cac372d6 | (unnamed) | lane | 7.0 | 138.2 | Overture line, width Mùṣá's for the kind |
| rd-cbd5a805 | (unnamed) | lane | 7.0 | 21.6 | Overture line, width Mùṣá's for the kind |
| rd-ccccf314 | (unnamed) | lane | 7.0 | 14.9 | Overture line, width Mùṣá's for the kind |
| rd-cd269c85 | (unnamed) | lane | 7.0 | 12.3 | Overture line, width Mùṣá's for the kind |
| rd-cddb1e60 | (unnamed) | lane | 7.0 | 36.8 | Overture line, width Mùṣá's for the kind |
| rd-d19e459e | (unnamed) | lane | 7.0 | 9.9 | Overture line, width Mùṣá's for the kind |
| rd-d2eae14a | (unnamed) | lane | 7.0 | 22.0 | Overture line, width Mùṣá's for the kind |
| rd-d3842d1b | (unnamed) | lane | 7.0 | 113.9 | Overture line, width Mùṣá's for the kind |
| rd-d3b72b71 | (unnamed) | lane | 7.0 | 23.9 | Overture line, width Mùṣá's for the kind |
| rd-d5864145 | (unnamed) | lane | 7.0 | 32.7 | Overture line, width Mùṣá's for the kind |
| rd-d74a495c | (unnamed) | lane | 7.0 | 46.6 | Overture line, width Mùṣá's for the kind |
| rd-ddf64f0a | (unnamed) | lane | 7.0 | 23.2 | Overture line, width Mùṣá's for the kind |
| rd-de578898 | (unnamed) | lane | 7.0 | 105.7 | Overture line, width Mùṣá's for the kind |
| rd-de9ce4e2 | (unnamed) | lane | 7.0 | 19.0 | Overture line, width Mùṣá's for the kind |
| rd-df92636c | (unnamed) | lane | 7.0 | 14.1 | Overture line, width Mùṣá's for the kind |
| rd-e14d21cf | (unnamed) | lane | 7.0 | 47.5 | Overture line, width Mùṣá's for the kind |
| rd-e4863be7 | (unnamed) | lane | 7.0 | 96.1 | Overture line, width Mùṣá's for the kind |
| rd-e72c8b81 | (unnamed) | lane | 7.0 | 25.1 | Overture line, width Mùṣá's for the kind |
| rd-e8264c0f | (unnamed) | lane | 7.0 | 58.3 | Overture line, width Mùṣá's for the kind |
| rd-e8849daa | (unnamed) | lane | 7.0 | 24.3 | Overture line, width Mùṣá's for the kind |
| rd-e91da28b | (unnamed) | lane | 7.0 | 20.5 | Overture line, width Mùṣá's for the kind |
| rd-ec1f6d27 | (unnamed) | lane | 7.0 | 23.0 | Overture line, width Mùṣá's for the kind |
| rd-eefd4dca | (unnamed) | lane | 7.0 | 22.9 | Overture line, width Mùṣá's for the kind |
| rd-ef39a3ad | (unnamed) | lane | 7.0 | 92.1 | Overture line, width Mùṣá's for the kind |
| rd-f0876669 | (unnamed) | lane | 7.0 | 9.1 | Overture line, width Mùṣá's for the kind |
| rd-f0ca4322 | (unnamed) | lane | 7.0 | 159.5 | Overture line, width Mùṣá's for the kind |
| rd-f238384b | (unnamed) | lane | 7.0 | 24.4 | Overture line, width Mùṣá's for the kind |
| rd-f25eb715 | (unnamed) | lane | 7.0 | 56.6 | Overture line, width Mùṣá's for the kind |
| rd-f7dc5f85 | (unnamed) | lane | 7.0 | 22.9 | Overture line, width Mùṣá's for the kind |
| rd-f7e670e9 | (unnamed) | lane | 7.0 | 15.2 | Overture line, width Mùṣá's for the kind |
| rd-fa05f0d8 | (unnamed) | lane | 7.0 | 45.7 | Overture line, width Mùṣá's for the kind |
| rd-fa2dc6e1 | (unnamed) | lane | 7.0 | 48.8 | Overture line, width Mùṣá's for the kind |
| rd-fa6f7af2 | (unnamed) | lane | 7.0 | 24.9 | Overture line, width Mùṣá's for the kind |
| rd-facda9dc | (unnamed) | lane | 7.0 | 54.5 | Overture line, width Mùṣá's for the kind |
| rd-fb9260e0 | (unnamed) | lane | 7.0 | 89.6 | Overture line, width Mùṣá's for the kind |
| rd-fbeebc06 | (unnamed) | lane | 7.0 | 62.5 | Overture line, width Mùṣá's for the kind |
| rd-fc8330c2 | (unnamed) | lane | 7.0 | 23.9 | Overture line, width Mùṣá's for the kind |
| rd-fdbb1884 | Technical Street | lane | 7.0 | 92.3 | Overture line, width Mùṣá's for the kind |
