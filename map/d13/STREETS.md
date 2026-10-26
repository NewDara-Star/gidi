# Sọ̀rọ̀lérè (district 13): the road plan and where each street comes from

Roads only, drawn on the new frame (1:3) at real widths. Real names live here only, never in the map. Houses and
places come in their own passes (NOW item 11).

## Count (Sọ̀rọ̀lérè hand pass 1, 26 Oct)

- District: 0.529 km² (Gidi), 867 × 1267 m, south of Mùṣá (15) and Ìtìrí (14): the main body west of Western Avenue
  and the stadium lobe east of it, up to Ojuelegba.
- Real streets crossing the border (Overture segments, subtype road): 955 pieces, 29.1 km inside at Gidi scale:
  469 residential (14.8 km), 181 service, 93 secondary, 60 tertiary, 58 primary, 34 motorway, 18 trunk,
  13 unclassified; and 29 foot pieces (26 footway, 3 steps; 294 m) left out, as in Mùṣá and Ìtìrí.
- Kept: **every street** but the pieces under Western Avenue, 452 road records, 24.8 km: 1 motorway, 16 main roads,
  16 local mains, 115 home streets, 304 lanes. Nothing thinned, as in Ìtìrí.

## How the lines were drawn

- As Ìtìrí: each named street is its Overture segments merged per (name, kind), clipped to the border, pieces under
  8 m dropped, no simplifying. Kinds: primary and secondary → main_road, tertiary and unclassified → local_main, named
  residential → home_street, unnamed residential and service → lane; widths and values Mùṣá's commonest for the kind.
  A piece whose both ends lay on the border starts 0.3 m inside it (a record's first point is inside its district).
- **Pairs** (two records within 4 m along more than 70% of both): merged to their midline, the longer id kept, the
  width the kind's plus the gap: Ojuelegba Road 13.0, Adeniran Ogunsanya Street 13.5, Alhaji Masha Road 11.5,
  Adelabu Street 13.5 and 14.0, Akerele Road 11.0, Herbert Macaulay Street 13.5, two lanes 9.0.
- **Herbert Macaulay Street** is Overture's trunk class: a main_road (13.5 m with its pair gap). Unnamed trunk pieces
  went in with the unnamed lanes (7 m), to read.
- **Western Avenue**: one 25 m motorway record, rd-32d33ffa, the midline of Overture's two carriageways sliced every
  3 m (4.8 m apart at 1:3, so about 14 m real between their centres; 25 m is that gap and one carriageway, to read),
  816 m from where the avenue leaves the border southward (13241.36,7384.58) north to Mùṣá's flyover's first point
  (13207.55,6601.34), shared; values as Mùṣá's rd-avaupyki. Its middle runs on the border, partly on the Mùṣá side.
- **Under the avenue**: 31 pieces (1.55 km) lay more than 60% inside the avenue's 25 m or Mùṣá's flyover, side road
  and trunk: Overture's 26 "Western Avenue" primary pieces (its carriageways and slips), 5 short unnamed pieces and an
  Iponri Estate Road stub. They went; the width holds them.
- **Joins**: every road end the check found inside or within 1 m of another road was put on that road's line (a
  vertex added there); points under 1 m apart became one; a road's own points under 1 m apart lost the one no other
  road shares. Three records lay wholly on another and went (rd-1110afde on Ojuelegba Road, rd-bdc801b0 on Alhaji
  Masha Road, rd-4f6a1e6e on rd-88dbf4a8); three were cut back where they ran on another (see the table).

## The seams

- **Mùṣá**: Mùṣá's flyover rd-avaupyki gained 8 junction vertices where Sọ̀rọ̀lérè's streets meet it (its line
  within 0.005 m of where it was); no Mùṣá end moved.
- **Ìtìrí**: Ogunlana Drive stays Ìtìrí's: its whole line is on Ìtìrí's side of the frame border (0 m inside
  Sọ̀rọ̀lérè), and Sọ̀rọ̀lérè's lane rd-51b26fe5 ends on its node (12755.24,6862.6). No Ìtìrí record changed.
- Western Avenue south of the border (Iponri, Costain) is the next district's (11) to carry on from rd-32d33ffa's end.

## Every road record

| id | real name | kind | width m | length m | source |
|---|---|---|---|---|---|
| rd-32d33ffa | Western Avenue | motorway | 25 | 815.7 | midline of the two carriageways, carried on from Mùṣá's flyover rd-avaupyki, its values |
| rd-58e8c6bb | Adelabu Street | main_road | 10.75 | 45.6 | Overture line, width Mùṣá's for the kind |
| rd-68099138 | Adelabu Street | main_road | 14 | 11.5 | Overture pair merged to its midline |
| rd-88dbf4a8 | Adelabu Street | main_road | 10.75 | 33.0 | Overture line, width Mùṣá's for the kind |
| rd-a862f848 | Adelabu Street | main_road | 13.5 | 168.0 | Overture pair merged to its midline |
| rd-18ca2d5e | Adeniran Ogunsanya Street | main_road | 13.5 | 348.1 | Overture pair merged to its midline |
| rd-ad481d55 | Bassie Ogamba Street | main_road | 10.75 | 92.8 | Overture line, width Mùṣá's for the kind |
| rd-1d8a6faf | Bode Thomas Street | main_road | 10.75 | 581.3 | Overture line, width Mùṣá's for the kind |
| rd-955a0307 | Herbert Macaulay Street | main_road | 13.5 | 121.3 | Overture pair merged to its midline; trunk, so a main_road |
| rd-9b4281b2 | Ojuelegba Road | main_road | 13 | 228.2 | Overture pair merged to its midline |
| rd-ccdc274f | Ojuelegba Road | main_road | 10.75 | 91.6 | Overture line, width Mùṣá's for the kind |
| rd-4a4be91f | (unnamed) | main_road | 10.75 | 35.4 | Overture line, width Mùṣá's for the kind |
| rd-5ac65ff7 | (unnamed) | main_road | 10.75 | 13.5 | Overture line, width Mùṣá's for the kind |
| rd-7f4af018 | (unnamed) | main_road | 10.75 | 22.1 | Overture line, width Mùṣá's for the kind; cut back where it ran on top of rd-95387170 |
| rd-aa64b535 | (unnamed) | main_road | 10.75 | 64.1 | Overture line, width Mùṣá's for the kind |
| rd-b7ac36fe | (unnamed) | main_road | 10.75 | 23.4 | Overture line, width Mùṣá's for the kind |
| rd-d2eea20d | (unnamed) | main_road | 10.75 | 15.0 | Overture line, width Mùṣá's for the kind |
| rd-cf0c7aac | Akerele Road | local_main | 11 | 119.1 | Overture pair merged to its midline |
| rd-1ad9f894 | Alhaji Masha Road | local_main | 11.5 | 428.3 | Overture pair merged to its midline |
| rd-3bffc1f2 | Eric Moore Road | local_main | 8.5 | 148.6 | Overture line, width Mùṣá's for the kind |
| rd-55f4e13c | Eric Moore Road | local_main | 8.5 | 145.9 | Overture line, width Mùṣá's for the kind |
| rd-138d2a3a | Tejuoso Street | local_main | 8.5 | 188.6 | Overture line, width Mùṣá's for the kind |
| rd-1be7f636 | (unnamed) | local_main | 8.5 | 15.7 | Overture line, width Mùṣá's for the kind |
| rd-2a0eb1d9 | (unnamed) | local_main | 8.5 | 70.5 | Overture line, width Mùṣá's for the kind |
| rd-5fc66c17 | (unnamed) | local_main | 8.5 | 68.4 | Overture line, width Mùṣá's for the kind |
| rd-713d3cd8 | (unnamed) | local_main | 8.5 | 11.6 | Overture line, width Mùṣá's for the kind |
| rd-75ac1bf0 | (unnamed) | local_main | 8.5 | 12.3 | Overture line, width Mùṣá's for the kind |
| rd-8f81a4bb | (unnamed) | local_main | 8.5 | 59.1 | Overture line, width Mùṣá's for the kind; cut back where it ran on top of rd-d2f9eb5c |
| rd-99393fb2 | (unnamed) | local_main | 8.5 | 15.2 | Overture line, width Mùṣá's for the kind |
| rd-b289c873 | (unnamed) | local_main | 8.5 | 36.9 | Overture line, width Mùṣá's for the kind |
| rd-b8db5e6b | (unnamed) | local_main | 8.5 | 8.4 | Overture line, width Mùṣá's for the kind |
| rd-d14c2d5d | (unnamed) | local_main | 8.5 | 28.2 | Overture line, width Mùṣá's for the kind |
| rd-d2f9eb5c | (unnamed) | local_main | 8.5 | 15.6 | Overture line, width Mùṣá's for the kind |
| rd-77acd566 | Abibu Oki Close | home_street | 7 | 23.1 | Overture line, width Mùṣá's for the kind |
| rd-cf9e54b2 | Abosede Kuboye Street | home_street | 7 | 31.1 | Overture line, width Mùṣá's for the kind |
| rd-b9c60842 | Adamu Orisha Crescent | home_street | 7 | 44.0 | Overture line, width Mùṣá's for the kind |
| rd-a6625575 | Ade Thianni Street | home_street | 7 | 77.8 | Overture line, width Mùṣá's for the kind |
| rd-696d3760 | Adebola Street | home_street | 7 | 215.7 | Overture line, width Mùṣá's for the kind |
| rd-933689ce | Adedamola Ojoma Close | home_street | 7 | 53.6 | Overture line, width Mùṣá's for the kind |
| rd-bd2c0c62 | Adedapo Street | home_street | 7 | 44.9 | Overture line, width Mùṣá's for the kind |
| rd-d1972455 | Adeniyi Jakande Close | home_street | 7 | 37.8 | Overture line, width Mùṣá's for the kind |
| rd-59b7387d | Adisa Bashua Street | home_street | 7 | 143.3 | Overture line, width Mùṣá's for the kind |
| rd-72bb45be | Adisa Bashua Street | home_street | 7 | 79.5 | Overture line, width Mùṣá's for the kind |
| rd-99866437 | Adisa Bashua Street | home_street | 7 | 75.2 | Overture line, width Mùṣá's for the kind |
| rd-9d2fda92 | Affini Street | home_street | 7 | 24.8 | Overture line, width Mùṣá's for the kind |
| rd-053aabf5 | Agunbiade Street | home_street | 7 | 57.7 | Overture line, width Mùṣá's for the kind |
| rd-c99195a2 | Agusto Close | home_street | 7 | 36.6 | Overture line, width Mùṣá's for the kind |
| rd-d2ab29f2 | Aibu Street | home_street | 7 | 57.3 | Overture line, width Mùṣá's for the kind |
| rd-887ddfe1 | Aiyeleto Street | home_street | 7 | 42.3 | Overture line, width Mùṣá's for the kind |
| rd-8c8b5642 | Ajani Oluare Street | home_street | 7 | 99.5 | Overture line, width Mùṣá's for the kind |
| rd-386e1e3f | Ajibode Street | home_street | 7 | 49.7 | Overture line, width Mùṣá's for the kind |
| rd-f319cd68 | Ajogbe Street | home_street | 7 | 41.6 | Overture line, width Mùṣá's for the kind |
| rd-844979e9 | Alade Close | home_street | 7 | 39.0 | Overture line, width Mùṣá's for the kind |
| rd-69d1ebcc | Alhaji Olaogun Drive | home_street | 7 | 105.8 | Overture line, width Mùṣá's for the kind |
| rd-3d71c680 | Alhaji Tokan Street | home_street | 7 | 89.8 | Overture line, width Mùṣá's for the kind |
| rd-9a089da8 | Aminu Close | home_street | 7 | 33.4 | Overture line, width Mùṣá's for the kind |
| rd-1f25d92c | Anifowoshe Close | home_street | 7 | 30.7 | Overture line, width Mùṣá's for the kind |
| rd-1f515839 | Animashaun Street | home_street | 7 | 79.7 | Overture line, width Mùṣá's for the kind |
| rd-c7d2c781 | Animashaun Street | home_street | 7 | 8.6 | Overture line, width Mùṣá's for the kind |
| rd-cab0f372 | Aralile Street | home_street | 7 | 100.7 | Overture line, width Mùṣá's for the kind |
| rd-dd014ca4 | Asopo Street | home_street | 7 | 36.8 | Overture line, width Mùṣá's for the kind |
| rd-918932ef | Atan Road | home_street | 7 | 58.8 | Overture line, width Mùṣá's for the kind |
| rd-5c618275 | Awolowo Road | home_street | 7 | 39.7 | Overture line, width Mùṣá's for the kind |
| rd-c1c4cbd6 | Awonaike Crescent | home_street | 7 | 59.1 | Overture line, width Mùṣá's for the kind |
| rd-094bc3be | Banjo Street | home_street | 7 | 77.9 | Overture line, width Mùṣá's for the kind |
| rd-c3aa49d5 | Basheer Augusto Street | home_street | 7 | 101.4 | Overture line, width Mùṣá's for the kind |
| rd-bc047c34 | Calabar Street | home_street | 7 | 109.2 | Overture line, width Mùṣá's for the kind |
| rd-9a281a77 | Census Close | home_street | 7 | 293.0 | Overture line, width Mùṣá's for the kind |
| rd-4becbf2f | Chief Bereola Street | home_street | 7 | 51.1 | Overture line, width Mùṣá's for the kind |
| rd-15241ff3 | Chief Onitana Street | home_street | 7 | 48.3 | Overture line, width Mùṣá's for the kind |
| rd-9232ef13 | Chilaka Close | home_street | 7 | 16.9 | Overture line, width Mùṣá's for the kind |
| rd-255c5238 | Clegg Street | home_street | 7 | 127.1 | Overture line, width Mùṣá's for the kind |
| rd-98055630 | Curtis Adeniyi Jones Close | home_street | 7 | 106.3 | Overture line, width Mùṣá's for the kind |
| rd-5fab53de | Dodo Williams Close | home_street | 7 | 16.8 | Overture line, width Mùṣá's for the kind |
| rd-13cccca2 | Eric Manuel Cresent | home_street | 7 | 165.2 | Overture line, width Mùṣá's for the kind |
| rd-138f59b8 | Fagbile Street | home_street | 7 | 85.0 | Overture line, width Mùṣá's for the kind |
| rd-063b9f04 | Femi Ayantuga Crescent | home_street | 7 | 248.4 | Overture line, width Mùṣá's for the kind |
| rd-e594ab4c | Gbadamosi Close | home_street | 7 | 45.5 | Overture line, width Mùṣá's for the kind |
| rd-46e0cd4a | Gbajumo Close | home_street | 7 | 111.7 | Overture line, width Mùṣá's for the kind |
| rd-1f8ce6b1 | Hogan Bassey Close | home_street | 7 | 25.6 | Overture line, width Mùṣá's for the kind |
| rd-69ca4b5d | Hogan Bassey Close | home_street | 7 | 109.9 | Overture line, width Mùṣá's for the kind |
| rd-a93aa32d | Hooper Road | home_street | 7 | 92.2 | Overture line, width Mùṣá's for the kind |
| rd-60d6f46b | Ibezim Obiajulu Street | home_street | 7 | 94.8 | Overture line, width Mùṣá's for the kind |
| rd-95315864 | Ibukun Street | home_street | 7 | 113.2 | Overture line, width Mùṣá's for the kind |
| rd-599cf2e0 | Idera Street | home_street | 7 | 36.9 | Overture line, width Mùṣá's for the kind |
| rd-067e6a09 | Idita Street | home_street | 7 | 57.8 | Overture line, width Mùṣá's for the kind |
| rd-63f9d753 | Iletunmi Street | home_street | 7 | 51.9 | Overture line, width Mùṣá's for the kind |
| rd-8c0a2346 | Imam Dauda Street | home_street | 7 | 137.4 | Overture line, width Mùṣá's for the kind |
| rd-3a53004d | Iponri Estate Road | home_street | 7 | 131.1 | Overture line, width Mùṣá's for the kind |
| rd-c1b1e59d | Iponri Estate Road | home_street | 7 | 71.6 | Overture line, width Mùṣá's for the kind |
| rd-a5341d33 | Ishau Adewale Street | home_street | 7 | 98.4 | Overture line, width Mùṣá's for the kind |
| rd-8d664d57 | Itolo Street | home_street | 7 | 171.5 | Overture line, width Mùṣá's for the kind |
| rd-83689ff1 | Iyun Road | home_street | 7 | 113.4 | Overture line, width Mùṣá's for the kind |
| rd-3eff109e | Jacob street | home_street | 7 | 91.3 | Overture line, width Mùṣá's for the kind |
| rd-33454fec | Jalupon Close | home_street | 7 | 81.0 | Overture line, width Mùṣá's for the kind |
| rd-505574ba | Jalupon Close | home_street | 7 | 59.3 | Overture line, width Mùṣá's for the kind |
| rd-c2e475dd | Jalupon Close | home_street | 7 | 27.0 | Overture line, width Mùṣá's for the kind |
| rd-d174ca73 | Jalupon Close | home_street | 7 | 38.1 | Overture line, width Mùṣá's for the kind |
| rd-b89a5ec3 | James Robertson Street | home_street | 7 | 68.4 | Overture line, width Mùṣá's for the kind |
| rd-66d31563 | Johnson Street | home_street | 7 | 79.6 | Overture line, width Mùṣá's for the kind |
| rd-6abf372d | Kelani Lane | home_street | 7 | 47.3 | Overture line, width Mùṣá's for the kind |
| rd-bfc40590 | Kernel Street | home_street | 7 | 60.9 | Overture line, width Mùṣá's for the kind |
| rd-2f66c3f6 | Laboye Laleye Cresent | home_street | 7 | 32.2 | Overture line, width Mùṣá's for the kind |
| rd-16d74632 | Leigh Street | home_street | 7 | 75.7 | Overture line, width Mùṣá's for the kind |
| rd-0c432bbc | Lisabi Street | home_street | 7 | 29.3 | Overture line, width Mùṣá's for the kind |
| rd-15c20aac | Lisabi Street | home_street | 7 | 21.8 | Overture line, width Mùṣá's for the kind |
| rd-d350ee9f | Lisabi Street | home_street | 7 | 38.7 | Overture line, width Mùṣá's for the kind |
| rd-2c913e1e | Lucinda Johnson Street | home_street | 7 | 85.4 | Overture line, width Mùṣá's for the kind |
| rd-60c093ed | Maja Street | home_street | 7 | 54.4 | Overture line, width Mùṣá's for the kind |
| rd-eaa6945b | Makinde Close | home_street | 7 | 50.8 | Overture line, width Mùṣá's for the kind |
| rd-f635a7ca | Martins Street | home_street | 7 | 57.3 | Overture line, width Mùṣá's for the kind |
| rd-afbe90bc | Matthew Street | home_street | 7 | 164.4 | Overture line, width Mùṣá's for the kind |
| rd-c9b2048a | Mba Street | home_street | 7 | 80.0 | Overture line, width Mùṣá's for the kind |
| rd-ef18afe7 | Mercy Eneli Street | home_street | 7 | 199.3 | Overture line, width Mùṣá's for the kind |
| rd-d81abdb7 | Modupe Johnson Cresent | home_street | 7 | 197.9 | Overture line, width Mùṣá's for the kind |
| rd-62b1ac22 | Moronu Maduagwu Street | home_street | 7 | 87.3 | Overture line, width Mùṣá's for the kind |
| rd-6f3974aa | Muse Street | home_street | 7 | 20.6 | Overture line, width Mùṣá's for the kind |
| rd-e371235c | Mustapha Close | home_street | 7 | 19.0 | Overture line, width Mùṣá's for the kind |
| rd-47c2660e | Nathan Street | home_street | 7 | 176.0 | Overture line, width Mùṣá's for the kind |
| rd-e731f3c7 | Nuru Oniwo | home_street | 7 | 34.7 | Overture line, width Mùṣá's for the kind |
| rd-26317297 | Nuru Oniwo Street | home_street | 7 | 13.7 | Overture line, width Mùṣá's for the kind |
| rd-61ba0594 | Odeku Close | home_street | 7 | 18.1 | Overture line, width Mùṣá's for the kind |
| rd-1f4897a1 | Ogundare Street | home_street | 7 | 24.2 | Overture line, width Mùṣá's for the kind |
| rd-4bacce4c | Olaitan Street | home_street | 7 | 89.9 | Overture line, width Mùṣá's for the kind |
| rd-43740026 | Olajuwon Street | home_street | 7 | 118.3 | Overture line, width Mùṣá's for the kind |
| rd-a989c488 | Olajuwon Street | home_street | 7 | 70.0 | Overture line, width Mùṣá's for the kind |
| rd-fd874e74 | Olufemi Street | home_street | 7 | 99.6 | Overture line, width Mùṣá's for the kind |
| rd-a4e94c4c | Oseni Close | home_street | 7 | 43.2 | Overture line, width Mùṣá's for the kind |
| rd-0f8cb6d4 | Owukori Crescent | home_street | 7 | 93.8 | Overture line, width Mùṣá's for the kind |
| rd-84d9efb5 | Oyabiyi Street | home_street | 7 | 88.1 | Overture line, width Mùṣá's for the kind |
| rd-dc2707f3 | Oyediran Street | home_street | 7 | 80.5 | Overture line, width Mùṣá's for the kind |
| rd-c0857b58 | Oyekan Street | home_street | 7 | 95.0 | Overture line, width Mùṣá's for the kind |
| rd-262f996f | Oyerokun Street | home_street | 7 | 111.2 | Overture line, width Mùṣá's for the kind |
| rd-c0b06cde | Pearse Lane | home_street | 7 | 79.7 | Overture line, width Mùṣá's for the kind |
| rd-fa72e401 | Pearse Street | home_street | 7 | 29.3 | Overture line, width Mùṣá's for the kind |
| rd-97955a16 | Popo Street | home_street | 7 | 88.3 | Overture line, width Mùṣá's for the kind |
| rd-5659b5e7 | Rabiatu Thompson Cresent | home_street | 7 | 218.9 | Overture line, width Mùṣá's for the kind |
| rd-5f791bf0 | Rabiatu Thompson Cresent | home_street | 7 | 39.8 | Overture line, width Mùṣá's for the kind |
| rd-1fa163a8 | Rasaq Balogun Street | home_street | 7 | 328.8 | Overture line, width Mùṣá's for the kind |
| rd-06a186ec | Raufu Williams Crescent | home_street | 7 | 192.9 | Overture line, width Mùṣá's for the kind |
| rd-cf1b3aad | Raufu Williams Crescent | home_street | 7 | 21.1 | Overture line, width Mùṣá's for the kind |
| rd-b6ee35d9 | Rotimi Street | home_street | 7 | 98.1 | Overture line, width Mùṣá's for the kind |
| rd-29ae4709 | Sabiu Ajose Cresent | home_street | 7 | 76.8 | Overture line, width Mùṣá's for the kind |
| rd-b008f557 | Shomade Crescent | home_street | 7 | 130.1 | Overture line, width Mùṣá's for the kind |
| rd-d06b58f7 | Tafawa Balewa Crescent | home_street | 7 | 268.0 | Overture line, width Mùṣá's for the kind |
| rd-35477980 | Tejuosho Avenue | home_street | 7 | 178.5 | Overture line, width Mùṣá's for the kind |
| rd-f2cdb77a | Tejuoso Street | home_street | 7 | 83.2 | Overture line, width Mùṣá's for the kind |
| rd-01330cc5 | Yussuf Sanusi Street | home_street | 7 | 134.6 | Overture line, width Mùṣá's for the kind |
| rd-bbb8a7c8 | Eko Club close | lane | 7 | 52.6 | Overture line, width Mùṣá's for the kind |
| rd-de4f0964 | Iyun Street | lane | 7 | 126.7 | Overture line, width Mùṣá's for the kind |
| rd-26a15de3 | National Stadium Complex | lane | 7 | 330.6 | Overture line, width Mùṣá's for the kind |
| rd-00d70d16 | (unnamed) | lane | 7 | 14.3 | Overture line, width Mùṣá's for the kind |
| rd-0209fcc5 | (unnamed) | lane | 7 | 27.7 | Overture line, width Mùṣá's for the kind |
| rd-02b98288 | (unnamed) | lane | 7 | 33.2 | Overture line, width Mùṣá's for the kind |
| rd-02ecedb1 | (unnamed) | lane | 7 | 26.8 | Overture line, width Mùṣá's for the kind |
| rd-03e43199 | (unnamed) | lane | 7 | 27.1 | Overture line, width Mùṣá's for the kind |
| rd-04c5713a | (unnamed) | lane | 7 | 31.4 | Overture line, width Mùṣá's for the kind |
| rd-04d92d65 | (unnamed) | lane | 7 | 22.6 | Overture line, width Mùṣá's for the kind |
| rd-04eb2928 | (unnamed) | lane | 7 | 41.0 | Overture line, width Mùṣá's for the kind |
| rd-051f6e2f | (unnamed) | lane | 7 | 29.1 | Overture line, width Mùṣá's for the kind |
| rd-06ea9f1d | (unnamed) | lane | 9 | 26.5 | Overture pair merged to its midline |
| rd-08767baf | (unnamed) | lane | 7 | 47.2 | Overture line, width Mùṣá's for the kind |
| rd-090eab8b | (unnamed) | lane | 7 | 27.9 | Overture line, width Mùṣá's for the kind |
| rd-0a02e654 | (unnamed) | lane | 7 | 14.2 | Overture line, width Mùṣá's for the kind |
| rd-0addcbe1 | (unnamed) | lane | 7 | 28.3 | Overture line, width Mùṣá's for the kind |
| rd-0c511b0d | (unnamed) | lane | 7 | 16.1 | Overture line, width Mùṣá's for the kind |
| rd-0d7e66d0 | (unnamed) | lane | 7 | 41.1 | Overture line, width Mùṣá's for the kind |
| rd-0fb23c9b | (unnamed) | lane | 7 | 53.3 | Overture line, width Mùṣá's for the kind |
| rd-0fce880f | (unnamed) | lane | 7 | 9.8 | Overture line, width Mùṣá's for the kind |
| rd-10c9b29e | (unnamed) | lane | 7 | 17.3 | Overture line, width Mùṣá's for the kind |
| rd-10e36bf3 | (unnamed) | lane | 7 | 81.7 | Overture line, width Mùṣá's for the kind |
| rd-1297189a | (unnamed) | lane | 7 | 9.2 | Overture line, width Mùṣá's for the kind |
| rd-14d6fb0e | (unnamed) | lane | 7 | 15.7 | Overture line, width Mùṣá's for the kind |
| rd-16026d5e | (unnamed) | lane | 7 | 28.6 | Overture line, width Mùṣá's for the kind |
| rd-160c1569 | (unnamed) | lane | 7 | 9.3 | Overture line, width Mùṣá's for the kind |
| rd-167ef63b | (unnamed) | lane | 7 | 82.0 | Overture line, width Mùṣá's for the kind |
| rd-1732845f | (unnamed) | lane | 7 | 102.2 | Overture line, width Mùṣá's for the kind |
| rd-188a69b3 | (unnamed) | lane | 7 | 11.9 | Overture line, width Mùṣá's for the kind |
| rd-18a66a91 | (unnamed) | lane | 7 | 16.6 | Overture line, width Mùṣá's for the kind |
| rd-19909352 | (unnamed) | lane | 7 | 13.5 | Overture line, width Mùṣá's for the kind |
| rd-1a48a676 | (unnamed) | lane | 7 | 24.6 | Overture line, width Mùṣá's for the kind |
| rd-1b5aeac6 | (unnamed) | lane | 7 | 11.7 | Overture line, width Mùṣá's for the kind |
| rd-1c825d8a | (unnamed) | lane | 7 | 22.7 | Overture line, width Mùṣá's for the kind |
| rd-1d123169 | (unnamed) | lane | 7 | 17.3 | Overture line, width Mùṣá's for the kind |
| rd-1d96d24f | (unnamed) | lane | 7 | 24.7 | Overture line, width Mùṣá's for the kind |
| rd-1d9ed01e | (unnamed) | lane | 7 | 120.2 | Overture line, width Mùṣá's for the kind |
| rd-1e6a1205 | (unnamed) | lane | 7 | 14.5 | Overture line, width Mùṣá's for the kind |
| rd-1f83b7c8 | (unnamed) | lane | 7 | 57.4 | Overture line, width Mùṣá's for the kind |
| rd-206fced4 | (unnamed) | lane | 7 | 11.7 | Overture line, width Mùṣá's for the kind |
| rd-224f507a | (unnamed) | lane | 7 | 52.2 | Overture line, width Mùṣá's for the kind |
| rd-235aeeb2 | (unnamed) | lane | 7 | 18.2 | Overture line, width Mùṣá's for the kind |
| rd-236ee10c | (unnamed) | lane | 7 | 22.3 | Overture line, width Mùṣá's for the kind |
| rd-23fa9587 | (unnamed) | lane | 7 | 50.2 | Overture line, width Mùṣá's for the kind |
| rd-2406250f | (unnamed) | lane | 7 | 13.5 | Overture line, width Mùṣá's for the kind |
| rd-271e73f1 | (unnamed) | lane | 7 | 17.7 | Overture line, width Mùṣá's for the kind |
| rd-273654a4 | (unnamed) | lane | 7 | 27.1 | Overture line, width Mùṣá's for the kind |
| rd-281f191c | (unnamed) | lane | 7 | 44.3 | Overture line, width Mùṣá's for the kind |
| rd-28592db7 | (unnamed) | lane | 7 | 70.9 | Overture line, width Mùṣá's for the kind |
| rd-288036ff | (unnamed) | lane | 7 | 23.8 | Overture line, width Mùṣá's for the kind |
| rd-28aa1ad7 | (unnamed) | lane | 7 | 27.6 | Overture line, width Mùṣá's for the kind |
| rd-28d9c6bd | (unnamed) | lane | 7 | 10.2 | Overture line, width Mùṣá's for the kind |
| rd-295c4403 | (unnamed) | lane | 7 | 29.5 | Overture line, width Mùṣá's for the kind |
| rd-2c038f7d | (unnamed) | lane | 7 | 32.0 | Overture line, width Mùṣá's for the kind |
| rd-2c6790ea | (unnamed) | lane | 7 | 41.6 | Overture line, width Mùṣá's for the kind |
| rd-2d5aff82 | (unnamed) | lane | 7 | 103.7 | Overture line, width Mùṣá's for the kind |
| rd-2d98afff | (unnamed) | lane | 7 | 10.4 | Overture line, width Mùṣá's for the kind |
| rd-2da835c9 | (unnamed) | lane | 7 | 19.3 | Overture line, width Mùṣá's for the kind |
| rd-2de2c05b | (unnamed) | lane | 7 | 125.6 | Overture line, width Mùṣá's for the kind |
| rd-2e9fdfa5 | (unnamed) | lane | 7 | 36.3 | Overture line, width Mùṣá's for the kind; cut back where it ran on top of rd-c1bc56f0 |
| rd-2f06821e | (unnamed) | lane | 7 | 15.2 | Overture line, width Mùṣá's for the kind |
| rd-2fbb1c20 | (unnamed) | lane | 7 | 21.6 | Overture line, width Mùṣá's for the kind |
| rd-3250272f | (unnamed) | lane | 7 | 11.9 | Overture line, width Mùṣá's for the kind |
| rd-325163b6 | (unnamed) | lane | 7 | 11.5 | Overture line, width Mùṣá's for the kind |
| rd-3283324b | (unnamed) | lane | 7 | 11.2 | Overture line, width Mùṣá's for the kind |
| rd-33087741 | (unnamed) | lane | 7 | 80.1 | Overture line, width Mùṣá's for the kind |
| rd-334de1c3 | (unnamed) | lane | 7 | 19.3 | Overture line, width Mùṣá's for the kind |
| rd-33a9fa08 | (unnamed) | lane | 7 | 15.7 | Overture line, width Mùṣá's for the kind |
| rd-354d29a0 | (unnamed) | lane | 7 | 12.8 | Overture line, width Mùṣá's for the kind |
| rd-359da165 | (unnamed) | lane | 7 | 19.5 | Overture line, width Mùṣá's for the kind |
| rd-3602a62a | (unnamed) | lane | 7 | 13.7 | Overture line, width Mùṣá's for the kind |
| rd-379d446a | (unnamed) | lane | 7 | 65.2 | Overture line, width Mùṣá's for the kind |
| rd-37fc35c7 | (unnamed) | lane | 7 | 44.9 | Overture line, width Mùṣá's for the kind |
| rd-3849dfec | (unnamed) | lane | 7 | 9.3 | Overture line, width Mùṣá's for the kind |
| rd-38ed7702 | (unnamed) | lane | 7 | 31.8 | Overture line, width Mùṣá's for the kind |
| rd-3b49fe4d | (unnamed) | lane | 7 | 95.0 | Overture line, width Mùṣá's for the kind |
| rd-3b9d53e4 | (unnamed) | lane | 7 | 51.4 | Overture line, width Mùṣá's for the kind |
| rd-3dedf7c4 | (unnamed) | lane | 7 | 19.8 | Overture line, width Mùṣá's for the kind |
| rd-3e7d6a36 | (unnamed) | lane | 7 | 13.6 | Overture line, width Mùṣá's for the kind |
| rd-409e797d | (unnamed) | lane | 7 | 22.7 | Overture line, width Mùṣá's for the kind |
| rd-41075d23 | (unnamed) | lane | 7 | 52.7 | Overture line, width Mùṣá's for the kind |
| rd-42277e4b | (unnamed) | lane | 7 | 46.8 | Overture line, width Mùṣá's for the kind |
| rd-424be3d5 | (unnamed) | lane | 7 | 18.7 | Overture line, width Mùṣá's for the kind |
| rd-445212c5 | (unnamed) | lane | 7 | 21.7 | Overture line, width Mùṣá's for the kind |
| rd-448948be | (unnamed) | lane | 7 | 9.8 | Overture line, width Mùṣá's for the kind |
| rd-458212bf | (unnamed) | lane | 7 | 22.6 | Overture line, width Mùṣá's for the kind |
| rd-45f31843 | (unnamed) | lane | 7 | 59.2 | Overture line, width Mùṣá's for the kind |
| rd-4672bb59 | (unnamed) | lane | 7 | 42.7 | Overture line, width Mùṣá's for the kind |
| rd-472c80ab | (unnamed) | lane | 7 | 13.3 | Overture line, width Mùṣá's for the kind |
| rd-495b94a0 | (unnamed) | lane | 7 | 52.8 | Overture line, width Mùṣá's for the kind |
| rd-49cd2e0f | (unnamed) | lane | 7 | 27.5 | Overture line, width Mùṣá's for the kind |
| rd-4b9f16ce | (unnamed) | lane | 7 | 14.9 | Overture line, width Mùṣá's for the kind |
| rd-4bdcffae | (unnamed) | lane | 7 | 35.3 | Overture line, width Mùṣá's for the kind |
| rd-4dde91a9 | (unnamed) | lane | 7 | 25.7 | Overture line, width Mùṣá's for the kind |
| rd-4f0540e4 | (unnamed) | lane | 7 | 62.5 | Overture line, width Mùṣá's for the kind |
| rd-4fa3ba57 | (unnamed) | lane | 7 | 15.6 | Overture line, width Mùṣá's for the kind |
| rd-500a9d49 | (unnamed) | lane | 7 | 30.8 | Overture line, width Mùṣá's for the kind |
| rd-500e4253 | (unnamed) | lane | 7 | 38.9 | Overture line, width Mùṣá's for the kind |
| rd-5054269b | (unnamed) | lane | 7 | 78.5 | Overture line, width Mùṣá's for the kind |
| rd-51b26fe5 | (unnamed) | lane | 7 | 12.7 | Overture line, width Mùṣá's for the kind |
| rd-5408e978 | (unnamed) | lane | 7 | 292.9 | Overture line, width Mùṣá's for the kind |
| rd-590852ad | (unnamed) | lane | 7 | 22.2 | Overture line, width Mùṣá's for the kind |
| rd-5a3cdb4a | (unnamed) | lane | 7 | 33.7 | Overture line, width Mùṣá's for the kind |
| rd-5b410a50 | (unnamed) | lane | 7 | 15.6 | Overture line, width Mùṣá's for the kind |
| rd-5b4a896d | (unnamed) | lane | 7 | 29.2 | Overture line, width Mùṣá's for the kind |
| rd-5e037e2c | (unnamed) | lane | 7 | 24.3 | Overture line, width Mùṣá's for the kind |
| rd-5ecb6897 | (unnamed) | lane | 7 | 9.0 | Overture line, width Mùṣá's for the kind |
| rd-5f90c6c2 | (unnamed) | lane | 7 | 9.6 | Overture line, width Mùṣá's for the kind |
| rd-5fa9ce20 | (unnamed) | lane | 7 | 9.6 | Overture line, width Mùṣá's for the kind |
| rd-60aa3bde | (unnamed) | lane | 7 | 22.0 | Overture line, width Mùṣá's for the kind |
| rd-60b80508 | (unnamed) | lane | 7 | 11.2 | Overture line, width Mùṣá's for the kind |
| rd-618f32e8 | (unnamed) | lane | 7 | 17.4 | Overture line, width Mùṣá's for the kind |
| rd-6222500e | (unnamed) | lane | 7 | 10.2 | Overture line, width Mùṣá's for the kind |
| rd-6261d556 | (unnamed) | lane | 7 | 21.6 | Overture line, width Mùṣá's for the kind |
| rd-629b9ddd | (unnamed) | lane | 7 | 14.2 | Overture line, width Mùṣá's for the kind |
| rd-642145b0 | (unnamed) | lane | 7 | 38.3 | Overture line, width Mùṣá's for the kind |
| rd-646ebc87 | (unnamed) | lane | 7 | 44.9 | Overture line, width Mùṣá's for the kind |
| rd-653a1c05 | (unnamed) | lane | 7 | 15.8 | Overture line, width Mùṣá's for the kind |
| rd-65694368 | (unnamed) | lane | 7 | 22.7 | Overture line, width Mùṣá's for the kind |
| rd-65d23a4f | (unnamed) | lane | 7 | 17.9 | Overture line, width Mùṣá's for the kind |
| rd-67a31597 | (unnamed) | lane | 7 | 12.7 | Overture line, width Mùṣá's for the kind |
| rd-67ad8cdb | (unnamed) | lane | 7 | 21.6 | Overture line, width Mùṣá's for the kind |
| rd-695a7878 | (unnamed) | lane | 7 | 46.2 | Overture line, width Mùṣá's for the kind |
| rd-6aa633df | (unnamed) | lane | 7 | 19.5 | Overture line, width Mùṣá's for the kind |
| rd-6bce5e7a | (unnamed) | lane | 7 | 44.1 | Overture line, width Mùṣá's for the kind |
| rd-6c4198c4 | (unnamed) | lane | 7 | 18.5 | Overture line, width Mùṣá's for the kind |
| rd-6e8848a0 | (unnamed) | lane | 7 | 9.8 | Overture line, width Mùṣá's for the kind |
| rd-6f34aa24 | (unnamed) | lane | 7 | 52.1 | Overture line, width Mùṣá's for the kind |
| rd-70205257 | (unnamed) | lane | 7 | 37.2 | Overture line, width Mùṣá's for the kind |
| rd-7046135d | (unnamed) | lane | 7 | 19.2 | Overture line, width Mùṣá's for the kind |
| rd-723553cb | (unnamed) | lane | 7 | 30.5 | Overture line, width Mùṣá's for the kind |
| rd-728d342f | (unnamed) | lane | 7 | 15.2 | Overture line, width Mùṣá's for the kind |
| rd-728eed51 | (unnamed) | lane | 7 | 8.3 | Overture line, width Mùṣá's for the kind |
| rd-72c75479 | (unnamed) | lane | 7 | 14.7 | Overture line, width Mùṣá's for the kind |
| rd-75318bc3 | (unnamed) | lane | 7 | 41.2 | Overture line, width Mùṣá's for the kind |
| rd-7536a648 | (unnamed) | lane | 7 | 18.1 | Overture line, width Mùṣá's for the kind |
| rd-758b4f91 | (unnamed) | lane | 7 | 18.1 | Overture line, width Mùṣá's for the kind |
| rd-76ef92f0 | (unnamed) | lane | 7 | 18.4 | Overture line, width Mùṣá's for the kind |
| rd-7769720f | (unnamed) | lane | 7 | 49.6 | Overture line, width Mùṣá's for the kind |
| rd-77e14648 | (unnamed) | lane | 7 | 29.0 | Overture line, width Mùṣá's for the kind |
| rd-7836fb75 | (unnamed) | lane | 7 | 23.5 | Overture line, width Mùṣá's for the kind |
| rd-784d1cd5 | (unnamed) | lane | 7 | 54.5 | Overture line, width Mùṣá's for the kind |
| rd-7853ea4b | (unnamed) | lane | 7 | 16.0 | Overture line, width Mùṣá's for the kind |
| rd-78838f05 | (unnamed) | lane | 7 | 29.2 | Overture line, width Mùṣá's for the kind |
| rd-79f158f6 | (unnamed) | lane | 7 | 94.6 | Overture line, width Mùṣá's for the kind |
| rd-7a1ef2fa | (unnamed) | lane | 7 | 29.0 | Overture line, width Mùṣá's for the kind |
| rd-7b448534 | (unnamed) | lane | 7 | 18.3 | Overture line, width Mùṣá's for the kind |
| rd-7baf8c06 | (unnamed) | lane | 7 | 81.2 | Overture line, width Mùṣá's for the kind |
| rd-7bfb89b6 | (unnamed) | lane | 7 | 34.5 | Overture line, width Mùṣá's for the kind |
| rd-7e16aacc | (unnamed) | lane | 7 | 27.0 | Overture line, width Mùṣá's for the kind |
| rd-7e34d9fd | (unnamed) | lane | 7 | 16.3 | Overture line, width Mùṣá's for the kind |
| rd-7e6cf416 | (unnamed) | lane | 7 | 23.8 | Overture line, width Mùṣá's for the kind |
| rd-7f53b8bb | (unnamed) | lane | 7 | 49.9 | Overture line, width Mùṣá's for the kind |
| rd-7ffb9d3e | (unnamed) | lane | 7 | 18.9 | Overture line, width Mùṣá's for the kind |
| rd-82106cae | (unnamed) | lane | 7 | 53.2 | Overture line, width Mùṣá's for the kind |
| rd-821f6f7e | (unnamed) | lane | 7 | 60.9 | Overture line, width Mùṣá's for the kind |
| rd-8320baf4 | (unnamed) | lane | 7 | 41.8 | Overture line, width Mùṣá's for the kind |
| rd-8423bf2e | (unnamed) | lane | 7 | 80.1 | Overture line, width Mùṣá's for the kind |
| rd-8451d6c7 | (unnamed) | lane | 7 | 68.5 | Overture line, width Mùṣá's for the kind |
| rd-8512bab3 | (unnamed) | lane | 7 | 34.7 | Overture line, width Mùṣá's for the kind |
| rd-8522fb29 | (unnamed) | lane | 7 | 12.5 | Overture line, width Mùṣá's for the kind |
| rd-86138d00 | (unnamed) | lane | 7 | 94.5 | Overture line, width Mùṣá's for the kind |
| rd-862cd11d | (unnamed) | lane | 7 | 8.4 | Overture line, width Mùṣá's for the kind |
| rd-86d98b2d | (unnamed) | lane | 7 | 12.8 | Overture line, width Mùṣá's for the kind |
| rd-874712f6 | (unnamed) | lane | 7 | 23.4 | Overture line, width Mùṣá's for the kind |
| rd-875e9ed0 | (unnamed) | lane | 7 | 28.6 | Overture line, width Mùṣá's for the kind |
| rd-8872d130 | (unnamed) | lane | 7 | 30.7 | Overture line, width Mùṣá's for the kind |
| rd-896ac913 | (unnamed) | lane | 7 | 14.0 | Overture line, width Mùṣá's for the kind |
| rd-8a98a697 | (unnamed) | lane | 7 | 56.2 | Overture line, width Mùṣá's for the kind |
| rd-8bda6407 | (unnamed) | lane | 7 | 59.9 | Overture line, width Mùṣá's for the kind |
| rd-8d754ee3 | (unnamed) | lane | 7 | 20.2 | Overture line, width Mùṣá's for the kind |
| rd-8e1c9a09 | (unnamed) | lane | 7 | 12.8 | Overture line, width Mùṣá's for the kind |
| rd-8e30927e | (unnamed) | lane | 7 | 114.8 | Overture line, width Mùṣá's for the kind |
| rd-8fa7707a | (unnamed) | lane | 7 | 44.9 | Overture line, width Mùṣá's for the kind |
| rd-901a06ad | (unnamed) | lane | 7 | 30.1 | Overture line, width Mùṣá's for the kind |
| rd-91f37b06 | (unnamed) | lane | 7 | 45.1 | Overture line, width Mùṣá's for the kind |
| rd-95387170 | (unnamed) | lane | 7 | 198.2 | Overture line, width Mùṣá's for the kind |
| rd-95e668bd | (unnamed) | lane | 7 | 12.5 | Overture line, width Mùṣá's for the kind |
| rd-992b6679 | (unnamed) | lane | 7 | 78.8 | Overture line, width Mùṣá's for the kind |
| rd-9c91343c | (unnamed) | lane | 7 | 67.5 | Overture line, width Mùṣá's for the kind |
| rd-9eb7320e | (unnamed) | lane | 7 | 22.5 | Overture line, width Mùṣá's for the kind |
| rd-9f01f481 | (unnamed) | lane | 7 | 39.9 | Overture line, width Mùṣá's for the kind |
| rd-a1f32419 | (unnamed) | lane | 7 | 11.9 | Overture line, width Mùṣá's for the kind |
| rd-a3fa7594 | (unnamed) | lane | 7 | 165.0 | Overture line, width Mùṣá's for the kind |
| rd-a68a95e5 | (unnamed) | lane | 7 | 17.2 | Overture line, width Mùṣá's for the kind |
| rd-a6aa310b | (unnamed) | lane | 7 | 41.8 | Overture line, width Mùṣá's for the kind |
| rd-a99f27f5 | (unnamed) | lane | 7 | 16.7 | Overture line, width Mùṣá's for the kind |
| rd-aa468917 | (unnamed) | lane | 7 | 29.2 | Overture line, width Mùṣá's for the kind |
| rd-aaff9e9f | (unnamed) | lane | 7 | 14.2 | Overture line, width Mùṣá's for the kind |
| rd-aba9e71c | (unnamed) | lane | 7 | 79.3 | Overture line, width Mùṣá's for the kind |
| rd-ac310187 | (unnamed) | lane | 7 | 44.2 | Overture line, width Mùṣá's for the kind |
| rd-acc1d757 | (unnamed) | lane | 7 | 31.8 | Overture line, width Mùṣá's for the kind |
| rd-ad386890 | (unnamed) | lane | 7 | 14.3 | Overture line, width Mùṣá's for the kind |
| rd-ae3e5096 | (unnamed) | lane | 7 | 33.4 | Overture line, width Mùṣá's for the kind |
| rd-ae980bbd | (unnamed) | lane | 7 | 23.0 | Overture line, width Mùṣá's for the kind |
| rd-ae9b9ff5 | (unnamed) | lane | 7 | 50.6 | Overture line, width Mùṣá's for the kind |
| rd-af686f25 | (unnamed) | lane | 7 | 87.6 | Overture line, width Mùṣá's for the kind |
| rd-afc067c5 | (unnamed) | lane | 7 | 164.9 | Overture line, width Mùṣá's for the kind |
| rd-b0271170 | (unnamed) | lane | 7 | 37.9 | Overture line, width Mùṣá's for the kind |
| rd-b1bbd4d1 | (unnamed) | lane | 7 | 25.2 | Overture line, width Mùṣá's for the kind |
| rd-b289c4f1 | (unnamed) | lane | 7 | 13.9 | Overture line, width Mùṣá's for the kind |
| rd-b3138766 | (unnamed) | lane | 7 | 12.2 | Overture line, width Mùṣá's for the kind |
| rd-b4685938 | (unnamed) | lane | 7 | 27.5 | Overture line, width Mùṣá's for the kind |
| rd-b50013bd | (unnamed) | lane | 7 | 13.1 | Overture line, width Mùṣá's for the kind |
| rd-b527672c | (unnamed) | lane | 7 | 127.2 | Overture line, width Mùṣá's for the kind |
| rd-b58c6035 | (unnamed) | lane | 7 | 12.8 | Overture line, width Mùṣá's for the kind |
| rd-b5bfcb35 | (unnamed) | lane | 7 | 89.9 | Overture line, width Mùṣá's for the kind |
| rd-b8c4ac1f | (unnamed) | lane | 7 | 43.3 | Overture line, width Mùṣá's for the kind |
| rd-b9e4f41e | (unnamed) | lane | 7 | 26.5 | Overture line, width Mùṣá's for the kind |
| rd-ba86debc | (unnamed) | lane | 7 | 21.6 | Overture line, width Mùṣá's for the kind |
| rd-bbfc44a2 | (unnamed) | lane | 7 | 21.0 | Overture line, width Mùṣá's for the kind |
| rd-bd37f69e | (unnamed) | lane | 7 | 55.6 | Overture line, width Mùṣá's for the kind |
| rd-be397957 | (unnamed) | lane | 7 | 9.9 | Overture line, width Mùṣá's for the kind |
| rd-bedf7195 | (unnamed) | lane | 7 | 108.7 | Overture line, width Mùṣá's for the kind |
| rd-c0f638df | (unnamed) | lane | 7 | 36.9 | Overture line, width Mùṣá's for the kind |
| rd-c1bc56f0 | (unnamed) | lane | 7 | 22.5 | Overture line, width Mùṣá's for the kind; its merged line folded back on itself: kept from its join with rd-2e9fdfa5 |
| rd-c23fbe57 | (unnamed) | lane | 7 | 9.9 | Overture line, width Mùṣá's for the kind |
| rd-c30c88c2 | (unnamed) | lane | 7 | 16.5 | Overture line, width Mùṣá's for the kind |
| rd-c4753b57 | (unnamed) | lane | 7 | 14.5 | Overture line, width Mùṣá's for the kind |
| rd-c4916b0c | (unnamed) | lane | 7 | 25.5 | Overture line, width Mùṣá's for the kind |
| rd-c567658f | (unnamed) | lane | 7 | 11.5 | Overture line, width Mùṣá's for the kind |
| rd-c56ec871 | (unnamed) | lane | 7 | 36.4 | Overture line, width Mùṣá's for the kind |
| rd-c68423c2 | (unnamed) | lane | 7 | 45.6 | Overture line, width Mùṣá's for the kind |
| rd-c6f9e47d | (unnamed) | lane | 7 | 16.6 | Overture line, width Mùṣá's for the kind |
| rd-c827d8ca | (unnamed) | lane | 7 | 9.9 | Overture line, width Mùṣá's for the kind |
| rd-c85b7ac9 | (unnamed) | lane | 7 | 15.3 | Overture line, width Mùṣá's for the kind |
| rd-c8bf8894 | (unnamed) | lane | 7 | 15.4 | Overture line, width Mùṣá's for the kind |
| rd-c8cad5f5 | (unnamed) | lane | 7 | 10.3 | Overture line, width Mùṣá's for the kind |
| rd-c92310d9 | (unnamed) | lane | 7 | 24.0 | Overture line, width Mùṣá's for the kind |
| rd-cc273de9 | (unnamed) | lane | 7 | 44.8 | Overture line, width Mùṣá's for the kind |
| rd-cd121f86 | (unnamed) | lane | 7 | 48.1 | Overture line, width Mùṣá's for the kind |
| rd-ce317bf0 | (unnamed) | lane | 7 | 50.0 | Overture line, width Mùṣá's for the kind |
| rd-ce792612 | (unnamed) | lane | 7 | 32.0 | Overture line, width Mùṣá's for the kind |
| rd-cf3f756f | (unnamed) | lane | 7 | 11.5 | Overture line, width Mùṣá's for the kind |
| rd-cf545782 | (unnamed) | lane | 7 | 13.2 | Overture line, width Mùṣá's for the kind |
| rd-cf5ccaea | (unnamed) | lane | 7 | 22.7 | Overture line, width Mùṣá's for the kind |
| rd-cf684aaf | (unnamed) | lane | 7 | 11.8 | Overture line, width Mùṣá's for the kind |
| rd-d039c2a7 | (unnamed) | lane | 7 | 18.4 | Overture line, width Mùṣá's for the kind |
| rd-d0c04da3 | (unnamed) | lane | 7 | 19.6 | Overture line, width Mùṣá's for the kind |
| rd-d0cb5a87 | (unnamed) | lane | 7 | 24.5 | Overture line, width Mùṣá's for the kind |
| rd-d152bf53 | (unnamed) | lane | 7 | 8.6 | Overture line, width Mùṣá's for the kind |
| rd-d357d4fc | (unnamed) | lane | 7 | 29.6 | Overture line, width Mùṣá's for the kind |
| rd-d69a10c6 | (unnamed) | lane | 7 | 157.3 | Overture line, width Mùṣá's for the kind |
| rd-d7d39db7 | (unnamed) | lane | 7 | 19.5 | Overture line, width Mùṣá's for the kind |
| rd-d91e2d9e | (unnamed) | lane | 7 | 41.9 | Overture line, width Mùṣá's for the kind |
| rd-d9785b72 | (unnamed) | lane | 7 | 9.4 | Overture line, width Mùṣá's for the kind |
| rd-d9e207ee | (unnamed) | lane | 7 | 62.8 | Overture line, width Mùṣá's for the kind |
| rd-da757aaa | (unnamed) | lane | 7 | 10.7 | Overture line, width Mùṣá's for the kind |
| rd-db4c55c9 | (unnamed) | lane | 9 | 19.8 | Overture pair merged to its midline |
| rd-db7fea66 | (unnamed) | lane | 7 | 12.2 | Overture line, width Mùṣá's for the kind |
| rd-dbdb97a2 | (unnamed) | lane | 7 | 27.0 | Overture line, width Mùṣá's for the kind |
| rd-dc1b715f | (unnamed) | lane | 7 | 45.5 | Overture line, width Mùṣá's for the kind |
| rd-ddd72e0b | (unnamed) | lane | 7 | 26.3 | Overture line, width Mùṣá's for the kind |
| rd-dfd8642f | (unnamed) | lane | 7 | 43.9 | Overture line, width Mùṣá's for the kind |
| rd-e02df248 | (unnamed) | lane | 7 | 9.6 | Overture line, width Mùṣá's for the kind |
| rd-e06f00bb | (unnamed) | lane | 7 | 24.5 | Overture line, width Mùṣá's for the kind |
| rd-e0c151c1 | (unnamed) | lane | 7 | 22.6 | Overture line, width Mùṣá's for the kind |
| rd-e208e88f | (unnamed) | lane | 7 | 47.8 | Overture line, width Mùṣá's for the kind |
| rd-e26c4068 | (unnamed) | lane | 7 | 71.9 | Overture line, width Mùṣá's for the kind |
| rd-e2a411ea | (unnamed) | lane | 7 | 24.5 | Overture line, width Mùṣá's for the kind |
| rd-e337cffc | (unnamed) | lane | 7 | 16.2 | Overture line, width Mùṣá's for the kind |
| rd-e39405bc | (unnamed) | lane | 7 | 10.6 | Overture line, width Mùṣá's for the kind |
| rd-e3ac00e8 | (unnamed) | lane | 7 | 13.4 | Overture line, width Mùṣá's for the kind |
| rd-e479466d | (unnamed) | lane | 7 | 18.2 | Overture line, width Mùṣá's for the kind |
| rd-e50cb3c4 | (unnamed) | lane | 7 | 17.3 | Overture line, width Mùṣá's for the kind |
| rd-e54057dc | (unnamed) | lane | 7 | 95.9 | Overture line, width Mùṣá's for the kind |
| rd-e630bce6 | (unnamed) | lane | 7 | 18.4 | Overture line, width Mùṣá's for the kind |
| rd-e67b366d | (unnamed) | lane | 7 | 58.0 | Overture line, width Mùṣá's for the kind |
| rd-e6b0b646 | (unnamed) | lane | 7 | 23.7 | Overture line, width Mùṣá's for the kind |
| rd-e714798d | (unnamed) | lane | 7 | 12.2 | Overture line, width Mùṣá's for the kind |
| rd-e73fc701 | (unnamed) | lane | 7 | 15.2 | Overture line, width Mùṣá's for the kind |
| rd-e77cd6ae | (unnamed) | lane | 7 | 37.8 | Overture line, width Mùṣá's for the kind |
| rd-e7cf49b5 | (unnamed) | lane | 7 | 18.5 | Overture line, width Mùṣá's for the kind |
| rd-e86db65c | (unnamed) | lane | 7 | 15.5 | Overture line, width Mùṣá's for the kind |
| rd-e873b4f9 | (unnamed) | lane | 7 | 10.7 | Overture line, width Mùṣá's for the kind |
| rd-e8b3317f | (unnamed) | lane | 7 | 22.0 | Overture line, width Mùṣá's for the kind |
| rd-e991a148 | (unnamed) | lane | 7 | 27.6 | Overture line, width Mùṣá's for the kind |
| rd-e9c88959 | (unnamed) | lane | 7 | 23.7 | Overture line, width Mùṣá's for the kind |
| rd-e9d80f49 | (unnamed) | lane | 7 | 8.4 | Overture line, width Mùṣá's for the kind |
| rd-ea06e822 | (unnamed) | lane | 7 | 22.1 | Overture line, width Mùṣá's for the kind |
| rd-ea514c89 | (unnamed) | lane | 7 | 79.7 | Overture line, width Mùṣá's for the kind |
| rd-eba01e26 | (unnamed) | lane | 7 | 14.7 | Overture line, width Mùṣá's for the kind |
| rd-ebee3b7c | (unnamed) | lane | 7 | 16.7 | Overture line, width Mùṣá's for the kind |
| rd-ed9760db | (unnamed) | lane | 7 | 13.1 | Overture line, width Mùṣá's for the kind |
| rd-edb383fb | (unnamed) | lane | 7 | 31.8 | Overture line, width Mùṣá's for the kind |
| rd-ef0665ad | (unnamed) | lane | 7 | 14.2 | Overture line, width Mùṣá's for the kind |
| rd-efa72883 | (unnamed) | lane | 7 | 52.3 | Overture line, width Mùṣá's for the kind |
| rd-f0542bf4 | (unnamed) | lane | 7 | 28.4 | Overture line, width Mùṣá's for the kind |
| rd-f22ba249 | (unnamed) | lane | 7 | 40.9 | Overture line, width Mùṣá's for the kind |
| rd-f2645844 | (unnamed) | lane | 7 | 20.7 | Overture line, width Mùṣá's for the kind |
| rd-f2e1bbc8 | (unnamed) | lane | 7 | 101.6 | Overture line, width Mùṣá's for the kind |
| rd-f2e2213f | (unnamed) | lane | 7 | 14.8 | Overture line, width Mùṣá's for the kind |
| rd-f2f0ed16 | (unnamed) | lane | 7 | 82.0 | Overture line, width Mùṣá's for the kind |
| rd-f3fccbc6 | (unnamed) | lane | 7 | 11.7 | Overture line, width Mùṣá's for the kind |
| rd-f41a7ef9 | (unnamed) | lane | 7 | 12.5 | Overture line, width Mùṣá's for the kind |
| rd-f497c831 | (unnamed) | lane | 7 | 20.9 | Overture line, width Mùṣá's for the kind |
| rd-f5a17717 | (unnamed) | lane | 7 | 56.5 | Overture line, width Mùṣá's for the kind |
| rd-f6ed33c9 | (unnamed) | lane | 7 | 76.2 | Overture line, width Mùṣá's for the kind |
| rd-fac2b7a0 | (unnamed) | lane | 7 | 29.5 | Overture line, width Mùṣá's for the kind |
| rd-fb529887 | (unnamed) | lane | 7 | 23.4 | Overture line, width Mùṣá's for the kind |
| rd-fcd09181 | (unnamed) | lane | 7 | 38.4 | Overture line, width Mùṣá's for the kind |
| rd-fdab3e1d | (unnamed) | lane | 7 | 12.8 | Overture line, width Mùṣá's for the kind |
| rd-ffcc084d | (unnamed) | lane | 7 | 53.8 | Overture line, width Mùṣá's for the kind |
