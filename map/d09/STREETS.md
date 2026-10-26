# Ayégúnlẹ̀ (district 9): the road plan and where each street comes from

Roads only, drawn on the new frame (1:3) at real widths. Real names live here only, never in the map. Houses and
places come in their own passes (NOW item 11).

## Count (Ayégúnlẹ̀ hand pass 1, 26 Oct)

- District: 1.392 km² (Gidi), 1700 × 1517 m, the outline from the frame study (Ajegunle), between the Lagos-Badagry
  Expressway on the north-west and the Apapa-Oworonshoki Expressway on the south-west; no neighbour drawn yet.
- Real streets crossing the border (Overture segments, subtype road): 1,696 pieces, 67.8 km inside at Gidi scale:
  1,167 residential (47.9 km), 138 secondary, 125 service, 65 primary, 59 unclassified, 56 motorway, 56 tertiary,
  3 unknown; and 27 foot pieces (17 footway, 8 steps, 2 path; 422 m) left out, as in Mùṣá, Ìtìrí and Sọ̀rọ̀lérè.
- Kept: **every street** but the pieces under the two expressways, 1,015 road records, 63.7 km: 2 motorways,
  4 service roads, 33 main roads, 25 local mains, 86 home streets, 865 lanes. Nothing thinned: about 46 km/km², near
  Ìtìrí's 41; Ayégúnlẹ̀'s maze of unnamed lanes is its character.

## How the lines were drawn

- As Ìtìrí and Sọ̀rọ̀lérè: each named street is its Overture segments merged per (name, kind), clipped to the border,
  pieces under 8 m dropped, no simplifying. Kinds: primary and secondary → main_road, tertiary and unclassified →
  local_main, named residential → home_street, unnamed residential and service → lane; Overture's primary pieces
  named for an expressway → service_road (its slips and side roads); widths and values Mùṣá's commonest for the kind.
  A piece whose both ends lay on the border starts 0.3 m inside it.
- **The two expressways**, each one 25 m motorway record with Ìtìrí's rd-8d0d36df's values: the midline of Overture's
  two carriageways (each carriageway chained piece to piece, the straightest way on at every node), sampled every
  3 m, kept where it runs within 13 m of the border (the border follows them). **Lagos-Badagry Expressway**
  rd-b2b8a5cc, 1,239 m, carriageways 13.6 m apart at 1:3 (about 41 m real: the BRT and rail run between them; 25 m to
  read). **Apapa-Oworonshoki Expressway** rd-f1478f6a, 1,173 m, carriageways 5.1 m apart; one 10 m gap at the
  interchange (11579,8838) closed straight. Most of each line is on the border, so about half its width lies outside
  the outline, over land the frame study gives to Mile 2-Amuwo Odofin (6), Kirikiri-Tin Can (8) and Apapa (10); those
  districts take the expressway as held when they are drawn.
- **Under the expressways**: 18 pieces lay more than 60% inside a 25 m corridor and went (Overture's own slip and
  side pieces); 2 service roads were cut where they ran inside it. Two roads that ended inside the Badagry corridor
  with no slip there were pulled back to its edge (rd-16ac15fb, rd-8cf51ad9; the second then lay wholly on the service
  road rd-fb81677f and went).
- **Pairs** (two records within 4 m along more than 70% of both): merged to their midline, the longer id kept, the
  width the kind's plus the gap: Gaskiya College Road 16.0, Cemetery Road 12.5, College Road 13.0, Mosafejo Street
  14.5, Alaba Oro Road 14.0, Iganmu Road 15.0, 12.5 and 13.0, two unnamed lanes 10.0 and 13.5. All to read.
- **Joins**: every road end the check found inside or within 1 m of another road was put on that road's line (a
  vertex added there); points under 1 m apart became one. rd-7f5ebb59 ran on rd-93e90e99 for its first 14 m and was
  cut back to where it leaves it.

## Under the expressways (left out)

| id | real name | kind | length m |
|---|---|---|---|
| rd-dba79566 | Apapa-Oworonshoki Expressway | service_road | 12.0 |
| rd-98162901 | Apapa-Oworonshoki Expressway | service_road | 75.8 |
| rd-98acd62d | Apapa-Oworonshoki Expressway | service_road | 44.0 |
| rd-5195ce71 | Apapa-Oworonshoki Expressway | service_road | 79.2 |
| rd-c852eca0 | Apapa-Oworonshoki Expressway | service_road | 94.7 |
| rd-dfb68e16 | Apapa-Oworonshoki Expressway | service_road | 82.9 |
| rd-ffd89ed8 | Apapa-Oworonshoki Expressway | service_road | 68.1 |
| rd-0b9ff5b9 | Apapa-Oworonshoki Expressway | service_road | 100.9 |
| rd-c764901f | Apapa-Oworonshoki Expressway | service_road | 80.0 |
| rd-27ddcb0e | Apapa-Oworonshoki Expressway | service_road | 66.6 |
| rd-f7e66021 | Apapa-Oworonshoki Expressway | service_road | 61.0 |
| rd-eb203fc4 | Apapa-Oworonshoki Expressway | service_road | 65.5 |
| rd-93fdfbac | Apapa-Oworonshoki Expressway | service_road | 51.8 |
| rd-2a8bdbfe | Apapa-Oworonshoki Expressway | service_road | 9.4 |
| rd-5eb2bc09 | Lagos-Badagry Expressway | service_road | 50.2 |
| rd-d5fc113f | Lagos-Badagry Expressway | service_road | 67.3 |
| rd-a245825f | Lagos-Badagry Expressway | service_road | 76.8 |
| rd-081551b3 | Lagos-Badagry Expressway | service_road | 601.9 |

## Every road record

| id | real name | kind | width m | length m | source |
|---|---|---|---|---|---|
| rd-f1478f6a | Apapa-Oworonshoki Expressway (carriageways) | motorway | 25.0 | 1173.3 | midline of the two carriageways, values from Ìtìrí rd-8d0d36df |
| rd-b2b8a5cc | Lagos-Badagry Expressway (carriageways) | motorway | 25.0 | 1238.7 | midline of the two carriageways, values from Ìtìrí rd-8d0d36df |
| rd-05f28575 | Apapa-Oworonshoki Expressway | service_road | 7.0 | 22.9 | Overture primary |
| rd-bc02623e | Apapa-Oworonshoki Expressway | service_road | 7.0 | 53.3 | Overture primary; cut back (note) |
| rd-15c21bf5 | Lagos-Badagry Expressway | service_road | 7.0 | 56.8 | Overture primary |
| rd-fb81677f | Lagos-Badagry Expressway | service_road | 7.0 | 222.5 | Overture primary; cut back (note) |
| rd-0a89f19c | (unnamed) | main_road | 10.75 | 135.4 | Overture primary,secondary |
| rd-1d2ba1a1 | (unnamed) | main_road | 10.75 | 266.7 | Overture primary,secondary |
| rd-3ad1e66c | (unnamed) | main_road | 10.75 | 40.9 | Overture primary,secondary |
| rd-6727064e | (unnamed) | main_road | 10.75 | 83.4 | Overture primary,secondary |
| rd-7d7bc310 | (unnamed) | main_road | 10.75 | 50.6 | Overture primary,secondary |
| rd-7f5ebb59 | (unnamed) | main_road | 10.75 | 28.5 | Overture primary,secondary; cut back (note) |
| rd-93e90e99 | (unnamed) | main_road | 10.75 | 132.7 | Overture primary,secondary |
| rd-992df405 | (unnamed) | main_road | 13.5 | 29.9 | Overture primary,secondary; a pair merged to its midline |
| rd-a5989534 | (unnamed) | main_road | 10.75 | 21.7 | Overture primary,secondary |
| rd-bfd29ddf | (unnamed) | main_road | 10.75 | 76.5 | Overture primary,secondary |
| rd-d3f4ecc7 | (unnamed) | main_road | 10.75 | 51.5 | Overture primary,secondary |
| rd-dd5efdb0 | (unnamed) | main_road | 10.75 | 26.9 | Overture primary,secondary |
| rd-e5cca523 | (unnamed) | main_road | 10.75 | 99.7 | Overture primary,secondary |
| rd-f8a67812 | (unnamed) | main_road | 10.75 | 90.2 | Overture primary,secondary |
| rd-6f6cea56 | Alaba Oro Road | main_road | 14.0 | 296.5 | Overture secondary; a pair merged to its midline |
| rd-f40f77e0 | Amore Street | main_road | 10.75 | 130.9 | Overture secondary |
| rd-f02c4ad9 | Cemetery Road | main_road | 12.5 | 398.3 | Overture secondary; a pair merged to its midline |
| rd-af85d6c7 | College Road | main_road | 10.75 | 105.7 | Overture secondary |
| rd-ce3f578b | College Road | main_road | 10.75 | 23.1 | Overture secondary |
| rd-e76fdb2a | College Road | main_road | 13.0 | 60.2 | Overture secondary; a pair merged to its midline |
| rd-24cface8 | Gaskiya College Road | main_road | 10.75 | 32.6 | Overture secondary |
| rd-29eb9884 | Gaskiya College Road | main_road | 16.0 | 224.5 | Overture secondary; a pair merged to its midline |
| rd-0e00db6a | Iganmu Road | main_road | 10.75 | 48.8 | Overture secondary |
| rd-8f799e35 | Iganmu Road | main_road | 15.0 | 106.1 | Overture secondary; a pair merged to its midline |
| rd-ab4c54bd | Iganmu Road | main_road | 10.75 | 34.6 | Overture secondary |
| rd-b42f13df | Iganmu Road | main_road | 12.5 | 102.3 | Overture secondary; a pair merged to its midline |
| rd-d7e81401 | Iganmu Road | main_road | 10.75 | 20.4 | Overture secondary |
| rd-db060952 | Iganmu Road | main_road | 10.75 | 67.2 | Overture secondary |
| rd-dd03f12e | Iganmu Road | main_road | 13.0 | 69.9 | Overture secondary; a pair merged to its midline |
| rd-44cd2dee | Kirikiri Road | main_road | 10.75 | 811.2 | Overture secondary |
| rd-742dae3d | Malu Road | main_road | 10.75 | 65.6 | Overture secondary |
| rd-ea34cfd9 | Malu Road | main_road | 10.75 | 64.7 | Overture secondary |
| rd-fb2db8f0 | Mosafejo Street | main_road | 14.5 | 192.3 | Overture secondary; a pair merged to its midline |
| rd-029b507c | (unnamed) | local_main | 8.5 | 241.6 | Overture tertiary,unclassified |
| rd-2f0453b5 | (unnamed) | local_main | 8.5 | 179.0 | Overture tertiary,unclassified |
| rd-4fe8ce4b | (unnamed) | local_main | 8.5 | 376.2 | Overture tertiary,unclassified |
| rd-51eef380 | (unnamed) | local_main | 8.5 | 104.0 | Overture tertiary,unclassified |
| rd-5f43cdc1 | (unnamed) | local_main | 8.5 | 492.6 | Overture tertiary,unclassified |
| rd-73fe9b4f | (unnamed) | local_main | 8.5 | 255.8 | Overture tertiary,unclassified |
| rd-8ecd3aea | (unnamed) | local_main | 8.5 | 61.6 | Overture tertiary,unclassified |
| rd-c05a3434 | (unnamed) | local_main | 8.5 | 72.0 | Overture tertiary,unclassified |
| rd-c60fcc24 | (unnamed) | local_main | 8.5 | 263.6 | Overture tertiary,unclassified |
| rd-e1b94f35 | (unnamed) | local_main | 8.5 | 123.8 | Overture tertiary,unclassified |
| rd-f2646bdf | (unnamed) | local_main | 8.5 | 42.8 | Overture tertiary,unclassified |
| rd-fb3fe13d | (unnamed) | local_main | 8.5 | 91.4 | Overture tertiary,unclassified |
| rd-a12806b6 | Baala Ayetoro Street | local_main | 8.5 | 170.1 | Overture unclassified |
| rd-166fd6fd | Baale Adeyemo Street | local_main | 8.5 | 148.2 | Overture tertiary |
| rd-f5789930 | Bakare Faro Street | local_main | 8.5 | 132.8 | Overture unclassified |
| rd-c7968489 | Boundary Road | local_main | 8.5 | 23.6 | Overture tertiary |
| rd-6c77d743 | Industrial Road | local_main | 8.5 | 237.6 | Overture unclassified |
| rd-9184af32 | Itire Road | local_main | 8.5 | 127.9 | Overture unclassified |
| rd-4d4a319a | MBA Street | local_main | 8.5 | 374.2 | Overture tertiary |
| rd-eb602bf2 | Marine Road | local_main | 8.5 | 86.6 | Overture tertiary |
| rd-752ac647 | Ojo Road | local_main | 8.5 | 333.1 | Overture tertiary |
| rd-eb3fc3b9 | Okoya Road | local_main | 8.5 | 121.7 | Overture unclassified |
| rd-497f4ef1 | Olayinka Street | local_main | 8.5 | 206.6 | Overture unclassified |
| rd-d48b92d8 | Olum Okun Street | local_main | 8.5 | 99.3 | Overture unclassified |
| rd-a9d4115f | Suru Alaba Road | local_main | 8.5 | 133.7 | Overture tertiary |
| rd-60a83c54 | Abukuru Street | home_street | 7.0 | 297.8 | Overture residential |
| rd-b8d53a9c | Achakpo Street | home_street | 7.0 | 248.4 | Overture residential |
| rd-968f055e | Adejiyan Street | home_street | 7.0 | 192.3 | Overture residential |
| rd-343c56c0 | Agbamu Street | home_street | 7.0 | 253.4 | Overture residential |
| rd-54240163 | Aiyepe Street | home_street | 7.0 | 49.5 | Overture residential |
| rd-b8acfb1a | Akogun Street | home_street | 7.0 | 229.7 | Overture residential |
| rd-6bb4f684 | Akpiri Street | home_street | 7.0 | 172.7 | Overture residential |
| rd-332379b3 | Alhaji Kadiri Salami Street | home_street | 7.0 | 81.1 | Overture residential |
| rd-a009cbdc | Amaechi Street | home_street | 7.0 | 125.7 | Overture residential |
| rd-f08fecd8 | Aniyaloye Street | home_street | 7.0 | 59.5 | Overture residential |
| rd-8dd13ad8 | Anjorin Street | home_street | 7.0 | 26.4 | Overture residential |
| rd-b23a6af5 | Anjorin Street | home_street | 7.0 | 51.8 | Overture residential |
| rd-d28aaa17 | Anthony Agbaje Street | home_street | 7.0 | 48.7 | Overture residential |
| rd-f0f02660 | Anthony Agbaje Street | home_street | 7.0 | 15.2 | Overture residential |
| rd-b9b996f1 | Apasa Street | home_street | 7.0 | 254.7 | Overture residential |
| rd-a4d69e35 | Apena Street | home_street | 7.0 | 129.5 | Overture residential |
| rd-ba1f4254 | Ashogbon Street | home_street | 7.0 | 57.6 | Overture residential |
| rd-4ef94e1c | Atolagbe Street | home_street | 7.0 | 72.0 | Overture residential |
| rd-f290ce6b | Awoyemi Street | home_street | 7.0 | 109.9 | Overture residential |
| rd-3283f4e0 | Bolaji Oloru | home_street | 7.0 | 49.9 | Overture residential |
| rd-f37f0759 | Ebenezer Street | home_street | 7.0 | 113.3 | Overture residential |
| rd-4af330f2 | Ebunotti Street | home_street | 7.0 | 94.8 | Overture residential |
| rd-22b8c39e | Edidi Street | home_street | 7.0 | 196.6 | Overture residential |
| rd-447252ef | Emordi Street | home_street | 7.0 | 217.9 | Overture residential |
| rd-1d6d3d6f | Ezeagu Street | home_street | 7.0 | 313.4 | Overture residential |
| rd-1e9a3ac7 | Fagbemi Street | home_street | 7.0 | 160.5 | Overture residential |
| rd-36145e6e | Freedom Street | home_street | 7.0 | 62.5 | Overture residential |
| rd-7e07c0bd | Goriola Street | home_street | 7.0 | 292.7 | Overture residential |
| rd-d9222226 | Ibafon Street | home_street | 7.0 | 254.0 | Overture residential |
| rd-3136e526 | Idewu Street | home_street | 7.0 | 686.2 | Overture residential |
| rd-2d2479eb | Idi Street | home_street | 7.0 | 263.9 | Overture residential |
| rd-7f9f1ca0 | Igaja Street | home_street | 7.0 | 69.8 | Overture residential |
| rd-a47cd751 | Iludun Close | home_street | 7.0 | 42.4 | Overture residential |
| rd-08e7e99c | Imam Street | home_street | 7.0 | 250.0 | Overture residential |
| rd-96512d79 | Iskalu Lane | home_street | 7.0 | 61.6 | Overture residential |
| rd-18dae711 | Labaka Street | home_street | 7.0 | 125.5 | Overture residential |
| rd-1ef47d6b | Ladega Street | home_street | 7.0 | 375.9 | Overture residential |
| rd-74de987c | Ladipo Street | home_street | 7.0 | 64.5 | Overture residential |
| rd-7c30e995 | Makanjuola Street | home_street | 7.0 | 70.5 | Overture residential |
| rd-d32e831a | Marine Road | home_street | 7.0 | 81.6 | Overture residential |
| rd-4044b2ea | Mission Street | home_street | 7.0 | 86.5 | Overture residential |
| rd-29ba192d | Mokoya Street | home_street | 7.0 | 91.7 | Overture residential |
| rd-477bc83d | Molade Street | home_street | 7.0 | 176.6 | Overture residential |
| rd-bf9a74b9 | Moshalashi Street | home_street | 7.0 | 126.5 | Overture residential |
| rd-b358ed59 | Muri Ojara Street | home_street | 7.0 | 252.0 | Overture residential |
| rd-8b37b665 | Muyibi Street | home_street | 7.0 | 353.6 | Overture residential |
| rd-0c3c1fab | Nosamu Street | home_street | 7.0 | 215.6 | Overture residential |
| rd-5254c4a1 | Oboh Street | home_street | 7.0 | 49.3 | Overture residential |
| rd-3292b8b2 | Odofin Street | home_street | 7.0 | 130.0 | Overture residential |
| rd-dc8194f9 | Odudu Lane | home_street | 7.0 | 47.9 | Overture residential |
| rd-5afabac6 | Oguniyi Street | home_street | 7.0 | 27.6 | Overture residential |
| rd-d6504b68 | Ohuntan Street | home_street | 7.0 | 90.4 | Overture residential |
| rd-9673978d | Ojoku Street | home_street | 7.0 | 74.1 | Overture residential |
| rd-c8355740 | Ojoku Street | home_street | 7.0 | 72.1 | Overture residential |
| rd-f3b50c67 | Ojumola Street | home_street | 7.0 | 13.9 | Overture residential |
| rd-d8a76884 | Okulaja Street | home_street | 7.0 | 153.1 | Overture residential |
| rd-24450aaa | Okunowa Street | home_street | 7.0 | 155.0 | Overture residential |
| rd-ac34d10c | Olowosu Street | home_street | 7.0 | 45.4 | Overture residential |
| rd-fd7fea74 | Olufiditi Street | home_street | 7.0 | 58.1 | Overture residential |
| rd-d46494b4 | Oluwa Street | home_street | 7.0 | 208.6 | Overture residential |
| rd-fa875257 | Oremeji Street | home_street | 7.0 | 63.7 | Overture residential |
| rd-ac48d649 | Orodu Street | home_street | 7.0 | 449.4 | Overture residential |
| rd-fde83fbe | Oshodi Street | home_street | 7.0 | 68.2 | Overture residential |
| rd-2394a0ae | Oshogbo Street | home_street | 7.0 | 74.2 | Overture residential |
| rd-f1b96e29 | Otua Street | home_street | 7.0 | 160.6 | Overture residential |
| rd-5716173e | Otunba Gbadamosi (Esado) Street | home_street | 7.0 | 128.1 | Overture residential |
| rd-bc26cdb2 | Oyebo Street | home_street | 7.0 | 125.0 | Overture residential |
| rd-2971cb75 | Rorobi Street | home_street | 7.0 | 82.4 | Overture residential |
| rd-60d00d25 | Rufai Street | home_street | 7.0 | 95.0 | Overture residential |
| rd-828c51ae | Sadiku Street | home_street | 7.0 | 61.0 | Overture residential |
| rd-83d99214 | Salawu Street | home_street | 7.0 | 102.4 | Overture residential |
| rd-878b2d66 | Sanni Street | home_street | 7.0 | 75.0 | Overture residential |
| rd-6761e0fe | Sanusi Street | home_street | 7.0 | 49.0 | Overture residential |
| rd-0b166b6c | Sidi Street | home_street | 7.0 | 48.3 | Overture residential |
| rd-1973f005 | Sufianu Street | home_street | 7.0 | 98.0 | Overture residential |
| rd-337e48b7 | Taiwo Street | home_street | 7.0 | 170.2 | Overture residential |
| rd-9eaaca4e | Temidire Street | home_street | 7.0 | 190.4 | Overture residential |
| rd-18c2da19 | Tolu Road | home_street | 7.0 | 359.4 | Overture residential |
| rd-75df4f6e | Uweriro Street | home_street | 7.0 | 28.6 | Overture residential |
| rd-4a6b3834 | Uzoh Street | home_street | 7.0 | 351.6 | Overture residential |
| rd-32be0dba | Wilmer Crescent | home_street | 7.0 | 415.9 | Overture residential |
| rd-6d18c8f7 | Yahaya Crescent | home_street | 7.0 | 269.1 | Overture residential |
| rd-3f4791df | Young Lane | home_street | 7.0 | 43.3 | Overture residential |
| rd-5f92ad79 | Yusuf Adebayo Street | home_street | 7.0 | 147.3 | Overture residential |
| rd-965db4d4 | Yusuf Esan Street | home_street | 7.0 | 189.9 | Overture residential |
| rd-13725dab | Zacheus Street | home_street | 7.0 | 81.2 | Overture residential |
| rd-0008dad9 | (unnamed) | lane | 7.0 | 73.5 | Overture residential,service,unknown |
| rd-0059718a | (unnamed) | lane | 7.0 | 40.9 | Overture residential,service,unknown |
| rd-00d6d2c6 | (unnamed) | lane | 7.0 | 28.1 | Overture residential,service,unknown |
| rd-0174119c | (unnamed) | lane | 7.0 | 48.4 | Overture residential,service,unknown |
| rd-01c07ac7 | (unnamed) | lane | 7.0 | 19.9 | Overture residential,service,unknown |
| rd-02204e22 | (unnamed) | lane | 7.0 | 18.1 | Overture residential,service,unknown |
| rd-028095f6 | (unnamed) | lane | 7.0 | 24.6 | Overture residential,service,unknown |
| rd-032f9c9a | (unnamed) | lane | 7.0 | 55.4 | Overture residential,service,unknown |
| rd-0334e694 | (unnamed) | lane | 7.0 | 35.6 | Overture residential,service,unknown |
| rd-033f1324 | (unnamed) | lane | 7.0 | 27.5 | Overture residential,service,unknown |
| rd-035c3b92 | (unnamed) | lane | 7.0 | 21.2 | Overture residential,service,unknown |
| rd-036c49f7 | (unnamed) | lane | 7.0 | 22.6 | Overture residential,service,unknown |
| rd-0386c4f2 | (unnamed) | lane | 7.0 | 118.5 | Overture residential,service,unknown |
| rd-03ddcdce | (unnamed) | lane | 7.0 | 27.4 | Overture residential,service,unknown |
| rd-03e9f07e | (unnamed) | lane | 7.0 | 109.0 | Overture residential,service,unknown |
| rd-042ef1d4 | (unnamed) | lane | 7.0 | 18.5 | Overture residential,service,unknown |
| rd-043436d5 | (unnamed) | lane | 7.0 | 60.0 | Overture residential,service,unknown |
| rd-04e558d4 | (unnamed) | lane | 7.0 | 9.2 | Overture residential,service,unknown |
| rd-04f7e816 | (unnamed) | lane | 7.0 | 84.6 | Overture residential,service,unknown |
| rd-04ff658b | (unnamed) | lane | 7.0 | 39.5 | Overture residential,service,unknown |
| rd-052069ad | (unnamed) | lane | 7.0 | 10.9 | Overture residential,service,unknown |
| rd-0536d701 | (unnamed) | lane | 7.0 | 32.3 | Overture residential,service,unknown |
| rd-054d9224 | (unnamed) | lane | 7.0 | 49.0 | Overture residential,service,unknown |
| rd-05b97138 | (unnamed) | lane | 7.0 | 43.1 | Overture residential,service,unknown |
| rd-063984ae | (unnamed) | lane | 7.0 | 27.4 | Overture residential,service,unknown |
| rd-06a38d9b | (unnamed) | lane | 7.0 | 57.3 | Overture residential,service,unknown |
| rd-06a51f9b | (unnamed) | lane | 7.0 | 57.7 | Overture residential,service,unknown |
| rd-070f94b4 | (unnamed) | lane | 7.0 | 25.7 | Overture residential,service,unknown |
| rd-0712ebc6 | (unnamed) | lane | 7.0 | 12.4 | Overture residential,service,unknown |
| rd-074e3ab8 | (unnamed) | lane | 7.0 | 185.8 | Overture residential,service,unknown |
| rd-07f0f202 | (unnamed) | lane | 7.0 | 24.0 | Overture residential,service,unknown |
| rd-080b322d | (unnamed) | lane | 7.0 | 64.6 | Overture residential,service,unknown |
| rd-081a1de6 | (unnamed) | lane | 7.0 | 24.0 | Overture residential,service,unknown |
| rd-088f4b35 | (unnamed) | lane | 7.0 | 10.7 | Overture residential,service,unknown |
| rd-0ad9c136 | (unnamed) | lane | 7.0 | 108.3 | Overture residential,service,unknown |
| rd-0ae4e4d9 | (unnamed) | lane | 7.0 | 58.2 | Overture residential,service,unknown |
| rd-0b616cc3 | (unnamed) | lane | 7.0 | 21.8 | Overture residential,service,unknown |
| rd-0c110b56 | (unnamed) | lane | 7.0 | 41.0 | Overture residential,service,unknown |
| rd-0c74b340 | (unnamed) | lane | 7.0 | 72.5 | Overture residential,service,unknown |
| rd-0cf0e854 | (unnamed) | lane | 7.0 | 17.4 | Overture residential,service,unknown |
| rd-0d0b5185 | (unnamed) | lane | 7.0 | 70.2 | Overture residential,service,unknown |
| rd-0d65379e | (unnamed) | lane | 7.0 | 22.6 | Overture residential,service,unknown |
| rd-0d87bd8f | (unnamed) | lane | 7.0 | 35.1 | Overture residential,service,unknown |
| rd-0d9fe996 | (unnamed) | lane | 7.0 | 34.6 | Overture residential,service,unknown |
| rd-0dce906d | (unnamed) | lane | 7.0 | 9.6 | Overture residential,service,unknown |
| rd-0e068037 | (unnamed) | lane | 7.0 | 142.3 | Overture residential,service,unknown |
| rd-0e8b4161 | (unnamed) | lane | 7.0 | 35.9 | Overture residential,service,unknown |
| rd-0efb271e | (unnamed) | lane | 7.0 | 24.5 | Overture residential,service,unknown |
| rd-0f07960a | (unnamed) | lane | 7.0 | 69.0 | Overture residential,service,unknown |
| rd-0faec447 | (unnamed) | lane | 7.0 | 23.3 | Overture residential,service,unknown |
| rd-0ff8a2ab | (unnamed) | lane | 7.0 | 110.0 | Overture residential,service,unknown |
| rd-107a0946 | (unnamed) | lane | 7.0 | 25.8 | Overture residential,service,unknown |
| rd-108b3489 | (unnamed) | lane | 7.0 | 48.3 | Overture residential,service,unknown |
| rd-10d9f527 | (unnamed) | lane | 7.0 | 186.3 | Overture residential,service,unknown |
| rd-112f1e1a | (unnamed) | lane | 7.0 | 111.2 | Overture residential,service,unknown |
| rd-11b9009a | (unnamed) | lane | 7.0 | 66.5 | Overture residential,service,unknown |
| rd-11b92ad8 | (unnamed) | lane | 7.0 | 10.6 | Overture residential,service,unknown |
| rd-11d7dee8 | (unnamed) | lane | 7.0 | 24.3 | Overture residential,service,unknown |
| rd-128310c3 | (unnamed) | lane | 7.0 | 133.2 | Overture residential,service,unknown |
| rd-12b96c2a | (unnamed) | lane | 7.0 | 26.0 | Overture residential,service,unknown |
| rd-131093a6 | (unnamed) | lane | 7.0 | 11.4 | Overture residential,service,unknown |
| rd-134dde3a | (unnamed) | lane | 7.0 | 119.8 | Overture residential,service,unknown |
| rd-137420f7 | (unnamed) | lane | 7.0 | 15.8 | Overture residential,service,unknown |
| rd-137bd248 | (unnamed) | lane | 7.0 | 49.5 | Overture residential,service,unknown |
| rd-145d6fa2 | (unnamed) | lane | 7.0 | 28.0 | Overture residential,service,unknown |
| rd-14bd8015 | (unnamed) | lane | 7.0 | 68.7 | Overture residential,service,unknown |
| rd-14c020e2 | (unnamed) | lane | 7.0 | 21.7 | Overture residential,service,unknown |
| rd-14c6cd10 | (unnamed) | lane | 7.0 | 14.9 | Overture residential,service,unknown |
| rd-15ffa712 | (unnamed) | lane | 7.0 | 10.6 | Overture residential,service,unknown |
| rd-16044114 | (unnamed) | lane | 7.0 | 39.5 | Overture residential,service,unknown |
| rd-164246b3 | (unnamed) | lane | 7.0 | 8.8 | Overture residential,service,unknown |
| rd-168df6c1 | (unnamed) | lane | 7.0 | 30.7 | Overture residential,service,unknown |
| rd-16ac15fb | (unnamed) | lane | 7.0 | 67.0 | Overture residential,service,unknown; cut back (note) |
| rd-17a4a57e | (unnamed) | lane | 7.0 | 129.5 | Overture residential,service,unknown |
| rd-17b4ee09 | (unnamed) | lane | 7.0 | 17.7 | Overture residential,service,unknown |
| rd-17c80467 | (unnamed) | lane | 7.0 | 64.9 | Overture residential,service,unknown |
| rd-1824d6be | (unnamed) | lane | 7.0 | 86.2 | Overture residential,service,unknown |
| rd-18ae7b77 | (unnamed) | lane | 7.0 | 34.9 | Overture residential,service,unknown |
| rd-18b488a7 | (unnamed) | lane | 7.0 | 31.2 | Overture residential,service,unknown |
| rd-19032411 | (unnamed) | lane | 7.0 | 51.3 | Overture residential,service,unknown |
| rd-1a83e9ce | (unnamed) | lane | 7.0 | 25.5 | Overture residential,service,unknown |
| rd-1ac4e91e | (unnamed) | lane | 7.0 | 28.2 | Overture residential,service,unknown |
| rd-1b7f85b3 | (unnamed) | lane | 7.0 | 28.5 | Overture residential,service,unknown |
| rd-1bdd4c69 | (unnamed) | lane | 7.0 | 17.4 | Overture residential,service,unknown |
| rd-1cb5cd0f | (unnamed) | lane | 7.0 | 28.1 | Overture residential,service,unknown |
| rd-1d7772fb | (unnamed) | lane | 7.0 | 48.2 | Overture residential,service,unknown |
| rd-1db77422 | (unnamed) | lane | 7.0 | 13.7 | Overture residential,service,unknown |
| rd-1dc4a43f | (unnamed) | lane | 7.0 | 13.4 | Overture residential,service,unknown |
| rd-1de924df | (unnamed) | lane | 7.0 | 18.4 | Overture residential,service,unknown |
| rd-1ebda420 | (unnamed) | lane | 7.0 | 23.7 | Overture residential,service,unknown |
| rd-1eeeac05 | (unnamed) | lane | 7.0 | 30.4 | Overture residential,service,unknown |
| rd-1f3325d1 | (unnamed) | lane | 7.0 | 86.4 | Overture residential,service,unknown |
| rd-1f351cff | (unnamed) | lane | 7.0 | 137.9 | Overture residential,service,unknown |
| rd-1ffc1df4 | (unnamed) | lane | 7.0 | 35.2 | Overture residential,service,unknown |
| rd-2034eaa5 | (unnamed) | lane | 7.0 | 25.9 | Overture residential,service,unknown |
| rd-20441eac | (unnamed) | lane | 7.0 | 25.1 | Overture residential,service,unknown |
| rd-2074123f | (unnamed) | lane | 7.0 | 74.4 | Overture residential,service,unknown |
| rd-20b94358 | (unnamed) | lane | 7.0 | 11.8 | Overture residential,service,unknown |
| rd-214e8bd7 | (unnamed) | lane | 7.0 | 37.5 | Overture residential,service,unknown |
| rd-2170ec02 | (unnamed) | lane | 7.0 | 15.3 | Overture residential,service,unknown |
| rd-2186b310 | (unnamed) | lane | 7.0 | 96.2 | Overture residential,service,unknown |
| rd-21a6e0bb | (unnamed) | lane | 7.0 | 78.6 | Overture residential,service,unknown |
| rd-2278d195 | (unnamed) | lane | 7.0 | 31.7 | Overture residential,service,unknown |
| rd-2316d27b | (unnamed) | lane | 7.0 | 25.6 | Overture residential,service,unknown |
| rd-23410d58 | (unnamed) | lane | 7.0 | 11.4 | Overture residential,service,unknown |
| rd-238878f0 | (unnamed) | lane | 7.0 | 42.2 | Overture residential,service,unknown |
| rd-24199185 | (unnamed) | lane | 7.0 | 404.3 | Overture residential,service,unknown |
| rd-246ad843 | (unnamed) | lane | 7.0 | 52.6 | Overture residential,service,unknown |
| rd-2473d793 | (unnamed) | lane | 7.0 | 169.6 | Overture residential,service,unknown |
| rd-2496e9bb | (unnamed) | lane | 7.0 | 96.6 | Overture residential,service,unknown |
| rd-24a046b0 | (unnamed) | lane | 7.0 | 22.9 | Overture residential,service,unknown |
| rd-25729fcb | (unnamed) | lane | 7.0 | 15.5 | Overture residential,service,unknown |
| rd-25ae86d6 | (unnamed) | lane | 7.0 | 14.8 | Overture residential,service,unknown |
| rd-25d279ca | (unnamed) | lane | 7.0 | 47.6 | Overture residential,service,unknown |
| rd-25f2a649 | (unnamed) | lane | 7.0 | 21.7 | Overture residential,service,unknown |
| rd-26519ad9 | (unnamed) | lane | 7.0 | 40.6 | Overture residential,service,unknown |
| rd-266a9f50 | (unnamed) | lane | 7.0 | 29.9 | Overture residential,service,unknown |
| rd-266ce318 | (unnamed) | lane | 7.0 | 76.4 | Overture residential,service,unknown |
| rd-2692907f | (unnamed) | lane | 7.0 | 19.3 | Overture residential,service,unknown |
| rd-26e88bb3 | (unnamed) | lane | 7.0 | 39.3 | Overture residential,service,unknown |
| rd-26e8ee10 | (unnamed) | lane | 7.0 | 49.9 | Overture residential,service,unknown |
| rd-271b5aa4 | (unnamed) | lane | 7.0 | 38.0 | Overture residential,service,unknown |
| rd-27b43290 | (unnamed) | lane | 7.0 | 34.6 | Overture residential,service,unknown |
| rd-27f0740a | (unnamed) | lane | 7.0 | 13.5 | Overture residential,service,unknown |
| rd-2819ab74 | (unnamed) | lane | 7.0 | 27.4 | Overture residential,service,unknown |
| rd-282ed3c7 | (unnamed) | lane | 7.0 | 14.5 | Overture residential,service,unknown |
| rd-2832e712 | (unnamed) | lane | 7.0 | 15.0 | Overture residential,service,unknown |
| rd-28543aaf | (unnamed) | lane | 7.0 | 15.1 | Overture residential,service,unknown |
| rd-2880e86f | (unnamed) | lane | 7.0 | 16.6 | Overture residential,service,unknown |
| rd-288d086a | (unnamed) | lane | 7.0 | 22.2 | Overture residential,service,unknown |
| rd-28b98c96 | (unnamed) | lane | 7.0 | 21.5 | Overture residential,service,unknown |
| rd-2931e255 | (unnamed) | lane | 7.0 | 21.2 | Overture residential,service,unknown |
| rd-29b755e5 | (unnamed) | lane | 7.0 | 23.9 | Overture residential,service,unknown |
| rd-29b9a016 | (unnamed) | lane | 7.0 | 18.9 | Overture residential,service,unknown |
| rd-29c0d2fd | (unnamed) | lane | 7.0 | 125.9 | Overture residential,service,unknown |
| rd-2a021e06 | (unnamed) | lane | 7.0 | 9.8 | Overture residential,service,unknown |
| rd-2a114695 | (unnamed) | lane | 7.0 | 41.1 | Overture residential,service,unknown |
| rd-2a4ab79b | (unnamed) | lane | 7.0 | 17.7 | Overture residential,service,unknown |
| rd-2a67924d | (unnamed) | lane | 7.0 | 25.7 | Overture residential,service,unknown |
| rd-2a6c629b | (unnamed) | lane | 7.0 | 15.5 | Overture residential,service,unknown |
| rd-2ab80a2e | (unnamed) | lane | 7.0 | 23.3 | Overture residential,service,unknown |
| rd-2ad86a18 | (unnamed) | lane | 7.0 | 43.6 | Overture residential,service,unknown |
| rd-2aff7f2a | (unnamed) | lane | 7.0 | 28.4 | Overture residential,service,unknown |
| rd-2be6c802 | (unnamed) | lane | 7.0 | 82.7 | Overture residential,service,unknown |
| rd-2bf833c1 | (unnamed) | lane | 7.0 | 13.2 | Overture residential,service,unknown |
| rd-2c0c9f67 | (unnamed) | lane | 7.0 | 33.4 | Overture residential,service,unknown |
| rd-2c168e21 | (unnamed) | lane | 7.0 | 26.7 | Overture residential,service,unknown |
| rd-2c56398b | (unnamed) | lane | 7.0 | 31.2 | Overture residential,service,unknown |
| rd-2c9c94f3 | (unnamed) | lane | 7.0 | 69.9 | Overture residential,service,unknown |
| rd-2cb109bb | (unnamed) | lane | 7.0 | 13.6 | Overture residential,service,unknown |
| rd-2cc484a8 | (unnamed) | lane | 7.0 | 12.0 | Overture residential,service,unknown |
| rd-2ce0c331 | (unnamed) | lane | 7.0 | 75.8 | Overture residential,service,unknown |
| rd-2ce9b5e3 | (unnamed) | lane | 7.0 | 12.5 | Overture residential,service,unknown |
| rd-2d55550d | (unnamed) | lane | 7.0 | 62.2 | Overture residential,service,unknown |
| rd-2d5abff6 | (unnamed) | lane | 7.0 | 52.8 | Overture residential,service,unknown |
| rd-2d5b4c87 | (unnamed) | lane | 7.0 | 10.8 | Overture residential,service,unknown |
| rd-2df89c58 | (unnamed) | lane | 7.0 | 17.7 | Overture residential,service,unknown |
| rd-2e129b3c | (unnamed) | lane | 7.0 | 17.7 | Overture residential,service,unknown |
| rd-2e3fe8ee | (unnamed) | lane | 7.0 | 53.3 | Overture residential,service,unknown |
| rd-2f0704a0 | (unnamed) | lane | 7.0 | 76.8 | Overture residential,service,unknown |
| rd-2f157ede | (unnamed) | lane | 7.0 | 18.1 | Overture residential,service,unknown |
| rd-2f8c0cca | (unnamed) | lane | 7.0 | 67.1 | Overture residential,service,unknown |
| rd-2fd046f1 | (unnamed) | lane | 7.0 | 28.8 | Overture residential,service,unknown |
| rd-3009393b | (unnamed) | lane | 7.0 | 28.6 | Overture residential,service,unknown |
| rd-30126503 | (unnamed) | lane | 7.0 | 92.2 | Overture residential,service,unknown |
| rd-30c6550a | (unnamed) | lane | 7.0 | 55.1 | Overture residential,service,unknown |
| rd-314f0790 | (unnamed) | lane | 7.0 | 20.9 | Overture residential,service,unknown |
| rd-3154b9d3 | (unnamed) | lane | 7.0 | 50.4 | Overture residential,service,unknown |
| rd-31be1b81 | (unnamed) | lane | 7.0 | 77.9 | Overture residential,service,unknown |
| rd-31d615dd | (unnamed) | lane | 7.0 | 8.2 | Overture residential,service,unknown |
| rd-31d77493 | (unnamed) | lane | 7.0 | 31.4 | Overture residential,service,unknown |
| rd-32051f2c | (unnamed) | lane | 7.0 | 87.8 | Overture residential,service,unknown |
| rd-326de355 | (unnamed) | lane | 7.0 | 111.4 | Overture residential,service,unknown |
| rd-326f6069 | (unnamed) | lane | 7.0 | 20.3 | Overture residential,service,unknown |
| rd-3288e925 | (unnamed) | lane | 7.0 | 32.7 | Overture residential,service,unknown |
| rd-32ecbfd3 | (unnamed) | lane | 7.0 | 35.1 | Overture residential,service,unknown |
| rd-32f6a389 | (unnamed) | lane | 7.0 | 30.5 | Overture residential,service,unknown |
| rd-3350bd9f | (unnamed) | lane | 7.0 | 8.5 | Overture residential,service,unknown |
| rd-3361b6fd | (unnamed) | lane | 7.0 | 33.3 | Overture residential,service,unknown |
| rd-33679852 | (unnamed) | lane | 7.0 | 57.5 | Overture residential,service,unknown |
| rd-339bbd72 | (unnamed) | lane | 7.0 | 47.4 | Overture residential,service,unknown |
| rd-33c69473 | (unnamed) | lane | 7.0 | 78.2 | Overture residential,service,unknown |
| rd-3465c8cf | (unnamed) | lane | 7.0 | 34.4 | Overture residential,service,unknown |
| rd-3497a429 | (unnamed) | lane | 7.0 | 69.4 | Overture residential,service,unknown |
| rd-34ad9353 | (unnamed) | lane | 7.0 | 40.5 | Overture residential,service,unknown |
| rd-34c11cf7 | (unnamed) | lane | 7.0 | 18.0 | Overture residential,service,unknown |
| rd-35004736 | (unnamed) | lane | 7.0 | 29.1 | Overture residential,service,unknown |
| rd-353f232e | (unnamed) | lane | 7.0 | 36.0 | Overture residential,service,unknown |
| rd-35446f80 | (unnamed) | lane | 7.0 | 18.1 | Overture residential,service,unknown |
| rd-355f6d4a | (unnamed) | lane | 7.0 | 38.6 | Overture residential,service,unknown |
| rd-3590b471 | (unnamed) | lane | 7.0 | 21.6 | Overture residential,service,unknown |
| rd-35bff930 | (unnamed) | lane | 7.0 | 72.2 | Overture residential,service,unknown |
| rd-36307929 | (unnamed) | lane | 7.0 | 86.8 | Overture residential,service,unknown |
| rd-364c4d67 | (unnamed) | lane | 7.0 | 53.6 | Overture residential,service,unknown |
| rd-3671264e | (unnamed) | lane | 7.0 | 28.6 | Overture residential,service,unknown |
| rd-36832c35 | (unnamed) | lane | 7.0 | 84.6 | Overture residential,service,unknown |
| rd-36af0648 | (unnamed) | lane | 7.0 | 99.1 | Overture residential,service,unknown |
| rd-373ef5a4 | (unnamed) | lane | 7.0 | 31.0 | Overture residential,service,unknown |
| rd-374f2ad0 | (unnamed) | lane | 7.0 | 20.5 | Overture residential,service,unknown |
| rd-378008e4 | (unnamed) | lane | 7.0 | 69.5 | Overture residential,service,unknown |
| rd-38a9e130 | (unnamed) | lane | 7.0 | 33.8 | Overture residential,service,unknown |
| rd-393b1e09 | (unnamed) | lane | 7.0 | 26.7 | Overture residential,service,unknown |
| rd-39715f75 | (unnamed) | lane | 7.0 | 52.6 | Overture residential,service,unknown |
| rd-3a18506a | (unnamed) | lane | 7.0 | 11.7 | Overture residential,service,unknown |
| rd-3a443f9f | (unnamed) | lane | 7.0 | 140.5 | Overture residential,service,unknown |
| rd-3a683b57 | (unnamed) | lane | 7.0 | 26.3 | Overture residential,service,unknown |
| rd-3c19831b | (unnamed) | lane | 7.0 | 32.1 | Overture residential,service,unknown |
| rd-3c461a39 | (unnamed) | lane | 7.0 | 34.6 | Overture residential,service,unknown |
| rd-3c6f6f68 | (unnamed) | lane | 7.0 | 57.2 | Overture residential,service,unknown |
| rd-3c7580e1 | (unnamed) | lane | 7.0 | 17.6 | Overture residential,service,unknown |
| rd-3d5eb063 | (unnamed) | lane | 7.0 | 15.8 | Overture residential,service,unknown |
| rd-3d6018a9 | (unnamed) | lane | 7.0 | 107.0 | Overture residential,service,unknown |
| rd-3d827b0b | (unnamed) | lane | 7.0 | 28.0 | Overture residential,service,unknown |
| rd-3d9b3b53 | (unnamed) | lane | 7.0 | 25.5 | Overture residential,service,unknown |
| rd-3df7fa64 | (unnamed) | lane | 7.0 | 20.1 | Overture residential,service,unknown |
| rd-3e54d3d0 | (unnamed) | lane | 7.0 | 25.1 | Overture residential,service,unknown |
| rd-3edada42 | (unnamed) | lane | 7.0 | 38.2 | Overture residential,service,unknown |
| rd-3edf30f5 | (unnamed) | lane | 7.0 | 15.9 | Overture residential,service,unknown |
| rd-3fa22601 | (unnamed) | lane | 7.0 | 36.2 | Overture residential,service,unknown |
| rd-3fa504bd | (unnamed) | lane | 7.0 | 67.4 | Overture residential,service,unknown |
| rd-3fb716c0 | (unnamed) | lane | 7.0 | 12.4 | Overture residential,service,unknown |
| rd-3fe2deb9 | (unnamed) | lane | 7.0 | 10.8 | Overture residential,service,unknown |
| rd-4027a76c | (unnamed) | lane | 7.0 | 11.1 | Overture residential,service,unknown |
| rd-40301758 | (unnamed) | lane | 7.0 | 23.3 | Overture residential,service,unknown |
| rd-4048b82e | (unnamed) | lane | 7.0 | 19.7 | Overture residential,service,unknown |
| rd-40915fa4 | (unnamed) | lane | 7.0 | 66.1 | Overture residential,service,unknown |
| rd-409d0ad3 | (unnamed) | lane | 7.0 | 143.5 | Overture residential,service,unknown |
| rd-40ac63c0 | (unnamed) | lane | 7.0 | 30.0 | Overture residential,service,unknown |
| rd-40acab4e | (unnamed) | lane | 7.0 | 25.6 | Overture residential,service,unknown |
| rd-40d36139 | (unnamed) | lane | 7.0 | 34.0 | Overture residential,service,unknown |
| rd-4123b8c0 | (unnamed) | lane | 7.0 | 139.5 | Overture residential,service,unknown |
| rd-4165f275 | (unnamed) | lane | 7.0 | 25.4 | Overture residential,service,unknown |
| rd-422a45b8 | (unnamed) | lane | 7.0 | 25.1 | Overture residential,service,unknown |
| rd-4235fc8f | (unnamed) | lane | 7.0 | 17.3 | Overture residential,service,unknown |
| rd-4257878c | (unnamed) | lane | 7.0 | 22.6 | Overture residential,service,unknown |
| rd-42891675 | (unnamed) | lane | 7.0 | 80.8 | Overture residential,service,unknown |
| rd-42d71ae1 | (unnamed) | lane | 7.0 | 30.0 | Overture residential,service,unknown |
| rd-4307d2e6 | (unnamed) | lane | 7.0 | 14.9 | Overture residential,service,unknown |
| rd-4311806d | (unnamed) | lane | 7.0 | 23.7 | Overture residential,service,unknown |
| rd-432491c4 | (unnamed) | lane | 7.0 | 33.0 | Overture residential,service,unknown |
| rd-4367057a | (unnamed) | lane | 7.0 | 61.3 | Overture residential,service,unknown |
| rd-43911daf | (unnamed) | lane | 7.0 | 34.6 | Overture residential,service,unknown |
| rd-43af30f5 | (unnamed) | lane | 7.0 | 52.2 | Overture residential,service,unknown |
| rd-43f256a0 | (unnamed) | lane | 7.0 | 27.6 | Overture residential,service,unknown |
| rd-44339d15 | (unnamed) | lane | 7.0 | 55.0 | Overture residential,service,unknown |
| rd-4489c661 | (unnamed) | lane | 7.0 | 22.4 | Overture residential,service,unknown |
| rd-45b28152 | (unnamed) | lane | 7.0 | 19.3 | Overture residential,service,unknown |
| rd-45cbf752 | (unnamed) | lane | 7.0 | 76.2 | Overture residential,service,unknown |
| rd-45e94b53 | (unnamed) | lane | 7.0 | 22.9 | Overture residential,service,unknown |
| rd-462257ae | (unnamed) | lane | 7.0 | 12.0 | Overture residential,service,unknown |
| rd-4654590a | (unnamed) | lane | 7.0 | 47.4 | Overture residential,service,unknown |
| rd-46da2b61 | (unnamed) | lane | 7.0 | 63.1 | Overture residential,service,unknown |
| rd-47239228 | (unnamed) | lane | 7.0 | 16.2 | Overture residential,service,unknown |
| rd-472af14c | (unnamed) | lane | 7.0 | 92.3 | Overture residential,service,unknown |
| rd-47862068 | (unnamed) | lane | 7.0 | 17.9 | Overture residential,service,unknown |
| rd-47f7e67b | (unnamed) | lane | 7.0 | 15.8 | Overture residential,service,unknown |
| rd-47fd418b | (unnamed) | lane | 7.0 | 13.5 | Overture residential,service,unknown |
| rd-4817d5ae | (unnamed) | lane | 7.0 | 8.5 | Overture residential,service,unknown |
| rd-4823d1e9 | (unnamed) | lane | 7.0 | 107.0 | Overture residential,service,unknown |
| rd-4910e874 | (unnamed) | lane | 7.0 | 35.8 | Overture residential,service,unknown |
| rd-497aafb7 | (unnamed) | lane | 7.0 | 12.3 | Overture residential,service,unknown |
| rd-499d7937 | (unnamed) | lane | 7.0 | 46.6 | Overture residential,service,unknown |
| rd-49f2c273 | (unnamed) | lane | 7.0 | 38.4 | Overture residential,service,unknown |
| rd-4a20c51e | (unnamed) | lane | 7.0 | 142.4 | Overture residential,service,unknown |
| rd-4a805103 | (unnamed) | lane | 7.0 | 60.6 | Overture residential,service,unknown |
| rd-4a841e59 | (unnamed) | lane | 7.0 | 62.4 | Overture residential,service,unknown |
| rd-4a9d48c3 | (unnamed) | lane | 7.0 | 19.2 | Overture residential,service,unknown |
| rd-4b36f5a6 | (unnamed) | lane | 7.0 | 32.9 | Overture residential,service,unknown |
| rd-4b614bf5 | (unnamed) | lane | 7.0 | 21.7 | Overture residential,service,unknown |
| rd-4b68f74f | (unnamed) | lane | 7.0 | 44.2 | Overture residential,service,unknown |
| rd-4b91c44c | (unnamed) | lane | 7.0 | 21.2 | Overture residential,service,unknown |
| rd-4ba1af87 | (unnamed) | lane | 7.0 | 18.6 | Overture residential,service,unknown |
| rd-4bbdc52e | (unnamed) | lane | 7.0 | 85.8 | Overture residential,service,unknown |
| rd-4c3e0dd1 | (unnamed) | lane | 7.0 | 92.6 | Overture residential,service,unknown |
| rd-4cd853d8 | (unnamed) | lane | 7.0 | 125.8 | Overture residential,service,unknown |
| rd-4d74e601 | (unnamed) | lane | 7.0 | 134.7 | Overture residential,service,unknown |
| rd-4e103014 | (unnamed) | lane | 7.0 | 26.3 | Overture residential,service,unknown |
| rd-4e145094 | (unnamed) | lane | 7.0 | 41.3 | Overture residential,service,unknown |
| rd-4e2e9792 | (unnamed) | lane | 7.0 | 29.4 | Overture residential,service,unknown |
| rd-4eb34149 | (unnamed) | lane | 7.0 | 50.4 | Overture residential,service,unknown |
| rd-4eec5d9c | (unnamed) | lane | 7.0 | 86.8 | Overture residential,service,unknown |
| rd-4f6443fd | (unnamed) | lane | 7.0 | 25.8 | Overture residential,service,unknown |
| rd-4faf0b4a | (unnamed) | lane | 7.0 | 27.9 | Overture residential,service,unknown |
| rd-5040b8f4 | (unnamed) | lane | 7.0 | 11.1 | Overture residential,service,unknown |
| rd-504fea75 | (unnamed) | lane | 7.0 | 22.5 | Overture residential,service,unknown |
| rd-50f3f778 | (unnamed) | lane | 7.0 | 35.3 | Overture residential,service,unknown |
| rd-510af4ad | (unnamed) | lane | 7.0 | 33.7 | Overture residential,service,unknown |
| rd-5157ce92 | (unnamed) | lane | 7.0 | 50.5 | Overture residential,service,unknown |
| rd-51844449 | (unnamed) | lane | 7.0 | 94.2 | Overture residential,service,unknown |
| rd-5184c23a | (unnamed) | lane | 7.0 | 15.8 | Overture residential,service,unknown |
| rd-51996252 | (unnamed) | lane | 7.0 | 73.6 | Overture residential,service,unknown |
| rd-51ab0192 | (unnamed) | lane | 7.0 | 53.2 | Overture residential,service,unknown |
| rd-51b74b2c | (unnamed) | lane | 7.0 | 51.7 | Overture residential,service,unknown |
| rd-52203274 | (unnamed) | lane | 7.0 | 15.5 | Overture residential,service,unknown |
| rd-524b4d1c | (unnamed) | lane | 7.0 | 33.2 | Overture residential,service,unknown |
| rd-528fb819 | (unnamed) | lane | 7.0 | 11.7 | Overture residential,service,unknown |
| rd-52aeb9d3 | (unnamed) | lane | 7.0 | 195.3 | Overture residential,service,unknown |
| rd-52dd0434 | (unnamed) | lane | 7.0 | 27.5 | Overture residential,service,unknown |
| rd-52f4ba59 | (unnamed) | lane | 7.0 | 18.9 | Overture residential,service,unknown |
| rd-53579548 | (unnamed) | lane | 7.0 | 26.2 | Overture residential,service,unknown |
| rd-53b610b4 | (unnamed) | lane | 7.0 | 46.4 | Overture residential,service,unknown |
| rd-53fb063c | (unnamed) | lane | 7.0 | 28.2 | Overture residential,service,unknown |
| rd-540ff800 | (unnamed) | lane | 7.0 | 20.0 | Overture residential,service,unknown |
| rd-5429bb47 | (unnamed) | lane | 7.0 | 48.6 | Overture residential,service,unknown |
| rd-542c1aa3 | (unnamed) | lane | 7.0 | 13.3 | Overture residential,service,unknown |
| rd-545cf816 | (unnamed) | lane | 7.0 | 51.1 | Overture residential,service,unknown |
| rd-5479f8db | (unnamed) | lane | 7.0 | 18.1 | Overture residential,service,unknown |
| rd-54a15ce2 | (unnamed) | lane | 7.0 | 54.8 | Overture residential,service,unknown |
| rd-55134191 | (unnamed) | lane | 7.0 | 37.1 | Overture residential,service,unknown |
| rd-55cc15be | (unnamed) | lane | 7.0 | 49.4 | Overture residential,service,unknown |
| rd-57ce1d56 | (unnamed) | lane | 7.0 | 71.6 | Overture residential,service,unknown |
| rd-5802eef3 | (unnamed) | lane | 7.0 | 30.6 | Overture residential,service,unknown |
| rd-585229cd | (unnamed) | lane | 7.0 | 22.2 | Overture residential,service,unknown |
| rd-589244d7 | (unnamed) | lane | 7.0 | 39.5 | Overture residential,service,unknown |
| rd-58f4ab94 | (unnamed) | lane | 7.0 | 95.9 | Overture residential,service,unknown |
| rd-5903cc70 | (unnamed) | lane | 7.0 | 10.2 | Overture residential,service,unknown |
| rd-592d25fe | (unnamed) | lane | 7.0 | 179.9 | Overture residential,service,unknown |
| rd-59446336 | (unnamed) | lane | 7.0 | 15.5 | Overture residential,service,unknown |
| rd-594d88f8 | (unnamed) | lane | 7.0 | 24.8 | Overture residential,service,unknown |
| rd-598dffcd | (unnamed) | lane | 7.0 | 171.9 | Overture residential,service,unknown |
| rd-59eaaa77 | (unnamed) | lane | 7.0 | 33.4 | Overture residential,service,unknown |
| rd-5a178c85 | (unnamed) | lane | 7.0 | 36.5 | Overture residential,service,unknown |
| rd-5a7e90f6 | (unnamed) | lane | 7.0 | 67.3 | Overture residential,service,unknown |
| rd-5a9a732f | (unnamed) | lane | 7.0 | 21.4 | Overture residential,service,unknown |
| rd-5ad9ba23 | (unnamed) | lane | 7.0 | 79.3 | Overture residential,service,unknown |
| rd-5b9ead19 | (unnamed) | lane | 7.0 | 26.7 | Overture residential,service,unknown |
| rd-5bed5cbe | (unnamed) | lane | 7.0 | 54.9 | Overture residential,service,unknown |
| rd-5c1aa7d0 | (unnamed) | lane | 7.0 | 74.1 | Overture residential,service,unknown |
| rd-5c534665 | (unnamed) | lane | 7.0 | 4.2 | Overture residential,service,unknown |
| rd-5cc26ce4 | (unnamed) | lane | 7.0 | 48.8 | Overture residential,service,unknown |
| rd-5d2703a9 | (unnamed) | lane | 7.0 | 11.7 | Overture residential,service,unknown |
| rd-5d929074 | (unnamed) | lane | 7.0 | 51.2 | Overture residential,service,unknown |
| rd-5ddf7c7d | (unnamed) | lane | 7.0 | 29.0 | Overture residential,service,unknown |
| rd-5e158ce8 | (unnamed) | lane | 7.0 | 21.3 | Overture residential,service,unknown |
| rd-5e4532dc | (unnamed) | lane | 7.0 | 19.9 | Overture residential,service,unknown |
| rd-5ee619b5 | (unnamed) | lane | 7.0 | 29.3 | Overture residential,service,unknown |
| rd-5f473aad | (unnamed) | lane | 7.0 | 29.3 | Overture residential,service,unknown |
| rd-5f4f9ac5 | (unnamed) | lane | 7.0 | 20.5 | Overture residential,service,unknown |
| rd-5f94dac1 | (unnamed) | lane | 7.0 | 67.2 | Overture residential,service,unknown |
| rd-5fbcc087 | (unnamed) | lane | 7.0 | 63.3 | Overture residential,service,unknown |
| rd-5fdcf566 | (unnamed) | lane | 7.0 | 61.1 | Overture residential,service,unknown |
| rd-604c88b8 | (unnamed) | lane | 7.0 | 38.8 | Overture residential,service,unknown |
| rd-60be2e8f | (unnamed) | lane | 7.0 | 26.2 | Overture residential,service,unknown |
| rd-6171bf01 | (unnamed) | lane | 7.0 | 45.4 | Overture residential,service,unknown |
| rd-63077ed3 | (unnamed) | lane | 7.0 | 22.4 | Overture residential,service,unknown |
| rd-631ed646 | (unnamed) | lane | 7.0 | 38.5 | Overture residential,service,unknown |
| rd-63482969 | (unnamed) | lane | 7.0 | 29.9 | Overture residential,service,unknown |
| rd-6349b7eb | (unnamed) | lane | 7.0 | 23.0 | Overture residential,service,unknown |
| rd-637e686b | (unnamed) | lane | 7.0 | 71.2 | Overture residential,service,unknown |
| rd-63a68790 | (unnamed) | lane | 7.0 | 14.8 | Overture residential,service,unknown |
| rd-63bed189 | (unnamed) | lane | 7.0 | 90.3 | Overture residential,service,unknown |
| rd-64869163 | (unnamed) | lane | 7.0 | 41.1 | Overture residential,service,unknown |
| rd-6506e2b5 | (unnamed) | lane | 7.0 | 106.6 | Overture residential,service,unknown |
| rd-65601f82 | (unnamed) | lane | 7.0 | 65.5 | Overture residential,service,unknown |
| rd-657296ab | (unnamed) | lane | 7.0 | 51.1 | Overture residential,service,unknown |
| rd-65cc05ee | (unnamed) | lane | 7.0 | 52.3 | Overture residential,service,unknown |
| rd-65dc39c8 | (unnamed) | lane | 7.0 | 60.5 | Overture residential,service,unknown |
| rd-65ec0610 | (unnamed) | lane | 7.0 | 35.9 | Overture residential,service,unknown |
| rd-66624e7f | (unnamed) | lane | 7.0 | 56.6 | Overture residential,service,unknown |
| rd-6672f083 | (unnamed) | lane | 7.0 | 28.3 | Overture residential,service,unknown |
| rd-66736880 | (unnamed) | lane | 7.0 | 24.6 | Overture residential,service,unknown |
| rd-66c8e099 | (unnamed) | lane | 7.0 | 12.9 | Overture residential,service,unknown |
| rd-66d14497 | (unnamed) | lane | 7.0 | 24.9 | Overture residential,service,unknown |
| rd-66d59f77 | (unnamed) | lane | 7.0 | 64.0 | Overture residential,service,unknown |
| rd-6739dc89 | (unnamed) | lane | 7.0 | 27.6 | Overture residential,service,unknown |
| rd-6751c5a6 | (unnamed) | lane | 7.0 | 29.2 | Overture residential,service,unknown |
| rd-677e0d7c | (unnamed) | lane | 7.0 | 18.1 | Overture residential,service,unknown |
| rd-68199808 | (unnamed) | lane | 7.0 | 25.4 | Overture residential,service,unknown |
| rd-68551550 | (unnamed) | lane | 7.0 | 18.0 | Overture residential,service,unknown |
| rd-68cc9724 | (unnamed) | lane | 7.0 | 32.0 | Overture residential,service,unknown |
| rd-691ad724 | (unnamed) | lane | 7.0 | 15.5 | Overture residential,service,unknown |
| rd-69a5b4f8 | (unnamed) | lane | 7.0 | 65.7 | Overture residential,service,unknown |
| rd-69e16e98 | (unnamed) | lane | 7.0 | 70.4 | Overture residential,service,unknown |
| rd-6a1edf61 | (unnamed) | lane | 7.0 | 169.3 | Overture residential,service,unknown |
| rd-6ae41f73 | (unnamed) | lane | 7.0 | 20.4 | Overture residential,service,unknown |
| rd-6b018399 | (unnamed) | lane | 7.0 | 51.4 | Overture residential,service,unknown |
| rd-6c75e11b | (unnamed) | lane | 7.0 | 10.6 | Overture residential,service,unknown |
| rd-6cada6e7 | (unnamed) | lane | 7.0 | 22.8 | Overture residential,service,unknown |
| rd-6cc730ef | (unnamed) | lane | 7.0 | 10.0 | Overture residential,service,unknown |
| rd-6ce09c64 | (unnamed) | lane | 7.0 | 55.8 | Overture residential,service,unknown |
| rd-6d17bac2 | (unnamed) | lane | 7.0 | 14.3 | Overture residential,service,unknown |
| rd-6d18c02b | (unnamed) | lane | 7.0 | 20.7 | Overture residential,service,unknown |
| rd-6d1a1f37 | (unnamed) | lane | 7.0 | 27.9 | Overture residential,service,unknown |
| rd-6d3452b5 | (unnamed) | lane | 7.0 | 62.2 | Overture residential,service,unknown |
| rd-6d6cc893 | (unnamed) | lane | 7.0 | 15.8 | Overture residential,service,unknown |
| rd-6db7ac11 | (unnamed) | lane | 7.0 | 108.9 | Overture residential,service,unknown |
| rd-6e49753d | (unnamed) | lane | 7.0 | 18.4 | Overture residential,service,unknown |
| rd-6e4eb521 | (unnamed) | lane | 7.0 | 25.4 | Overture residential,service,unknown |
| rd-6e5c6720 | (unnamed) | lane | 7.0 | 13.7 | Overture residential,service,unknown |
| rd-6e631451 | (unnamed) | lane | 7.0 | 43.2 | Overture residential,service,unknown |
| rd-6fec18eb | (unnamed) | lane | 7.0 | 100.4 | Overture residential,service,unknown |
| rd-714eec25 | (unnamed) | lane | 7.0 | 53.1 | Overture residential,service,unknown |
| rd-715b6571 | (unnamed) | lane | 7.0 | 18.4 | Overture residential,service,unknown |
| rd-71c35361 | (unnamed) | lane | 7.0 | 24.0 | Overture residential,service,unknown |
| rd-7267bc18 | (unnamed) | lane | 7.0 | 31.3 | Overture residential,service,unknown |
| rd-73127d24 | (unnamed) | lane | 7.0 | 10.9 | Overture residential,service,unknown |
| rd-7358e66d | (unnamed) | lane | 7.0 | 18.1 | Overture residential,service,unknown |
| rd-738adfa4 | (unnamed) | lane | 7.0 | 13.8 | Overture residential,service,unknown |
| rd-73ba5e73 | (unnamed) | lane | 7.0 | 75.7 | Overture residential,service,unknown |
| rd-73f444ee | (unnamed) | lane | 7.0 | 67.1 | Overture residential,service,unknown |
| rd-74845f66 | (unnamed) | lane | 7.0 | 252.0 | Overture residential,service,unknown |
| rd-749b4c55 | (unnamed) | lane | 7.0 | 26.6 | Overture residential,service,unknown |
| rd-74a2b676 | (unnamed) | lane | 7.0 | 93.3 | Overture residential,service,unknown |
| rd-74a43627 | (unnamed) | lane | 7.0 | 102.6 | Overture residential,service,unknown |
| rd-74bdde1b | (unnamed) | lane | 7.0 | 53.0 | Overture residential,service,unknown |
| rd-74d4b563 | (unnamed) | lane | 7.0 | 29.7 | Overture residential,service,unknown |
| rd-74d7d8c6 | (unnamed) | lane | 7.0 | 20.5 | Overture residential,service,unknown |
| rd-7546d1c8 | (unnamed) | lane | 7.0 | 48.9 | Overture residential,service,unknown |
| rd-7551d3aa | (unnamed) | lane | 7.0 | 28.8 | Overture residential,service,unknown |
| rd-75995f88 | (unnamed) | lane | 7.0 | 57.3 | Overture residential,service,unknown |
| rd-75a1e615 | (unnamed) | lane | 7.0 | 89.9 | Overture residential,service,unknown |
| rd-76401f1b | (unnamed) | lane | 7.0 | 65.7 | Overture residential,service,unknown |
| rd-767115ce | (unnamed) | lane | 7.0 | 22.4 | Overture residential,service,unknown |
| rd-76a7282c | (unnamed) | lane | 7.0 | 96.5 | Overture residential,service,unknown |
| rd-77069040 | (unnamed) | lane | 7.0 | 22.7 | Overture residential,service,unknown |
| rd-7721c5bb | (unnamed) | lane | 7.0 | 37.7 | Overture residential,service,unknown |
| rd-77383709 | (unnamed) | lane | 7.0 | 8.0 | Overture residential,service,unknown |
| rd-777f7158 | (unnamed) | lane | 7.0 | 14.7 | Overture residential,service,unknown |
| rd-77b09243 | (unnamed) | lane | 7.0 | 28.4 | Overture residential,service,unknown |
| rd-77fa7281 | (unnamed) | lane | 7.0 | 15.4 | Overture residential,service,unknown |
| rd-788785a0 | (unnamed) | lane | 7.0 | 19.0 | Overture residential,service,unknown |
| rd-7970a787 | (unnamed) | lane | 7.0 | 24.5 | Overture residential,service,unknown |
| rd-7974895b | (unnamed) | lane | 7.0 | 14.1 | Overture residential,service,unknown |
| rd-799df526 | (unnamed) | lane | 7.0 | 85.8 | Overture residential,service,unknown |
| rd-79af1955 | (unnamed) | lane | 7.0 | 30.2 | Overture residential,service,unknown |
| rd-7a18c660 | (unnamed) | lane | 7.0 | 39.4 | Overture residential,service,unknown |
| rd-7aec2a1c | (unnamed) | lane | 7.0 | 30.0 | Overture residential,service,unknown |
| rd-7bc83f7f | (unnamed) | lane | 7.0 | 76.5 | Overture residential,service,unknown |
| rd-7bf6d45c | (unnamed) | lane | 7.0 | 85.5 | Overture residential,service,unknown |
| rd-7c34363e | (unnamed) | lane | 7.0 | 28.0 | Overture residential,service,unknown |
| rd-7c451c05 | (unnamed) | lane | 7.0 | 8.2 | Overture residential,service,unknown |
| rd-7c9bc6f4 | (unnamed) | lane | 7.0 | 140.8 | Overture residential,service,unknown |
| rd-7d0552d9 | (unnamed) | lane | 7.0 | 117.9 | Overture residential,service,unknown |
| rd-7d3044d7 | (unnamed) | lane | 7.0 | 59.3 | Overture residential,service,unknown |
| rd-7d56c6cf | (unnamed) | lane | 7.0 | 49.7 | Overture residential,service,unknown |
| rd-7d63ab93 | (unnamed) | lane | 7.0 | 15.3 | Overture residential,service,unknown |
| rd-7db5d973 | (unnamed) | lane | 7.0 | 56.6 | Overture residential,service,unknown |
| rd-7e725411 | (unnamed) | lane | 7.0 | 30.3 | Overture residential,service,unknown |
| rd-7ec55a5a | (unnamed) | lane | 7.0 | 113.3 | Overture residential,service,unknown |
| rd-7ec65c67 | (unnamed) | lane | 7.0 | 26.1 | Overture residential,service,unknown |
| rd-7f33b3a2 | (unnamed) | lane | 7.0 | 50.6 | Overture residential,service,unknown |
| rd-7fa24a07 | (unnamed) | lane | 7.0 | 23.2 | Overture residential,service,unknown |
| rd-7fd9e952 | (unnamed) | lane | 7.0 | 292.0 | Overture residential,service,unknown |
| rd-7ffca4eb | (unnamed) | lane | 7.0 | 48.1 | Overture residential,service,unknown |
| rd-8049af04 | (unnamed) | lane | 7.0 | 22.6 | Overture residential,service,unknown |
| rd-804a9b1e | (unnamed) | lane | 7.0 | 11.6 | Overture residential,service,unknown |
| rd-808f497e | (unnamed) | lane | 7.0 | 108.7 | Overture residential,service,unknown |
| rd-80a12686 | (unnamed) | lane | 7.0 | 25.8 | Overture residential,service,unknown |
| rd-80d2df9b | (unnamed) | lane | 7.0 | 15.9 | Overture residential,service,unknown |
| rd-80de3e27 | (unnamed) | lane | 7.0 | 23.5 | Overture residential,service,unknown |
| rd-813be25a | (unnamed) | lane | 7.0 | 41.5 | Overture residential,service,unknown |
| rd-8202678e | (unnamed) | lane | 7.0 | 73.9 | Overture residential,service,unknown |
| rd-822ff8eb | (unnamed) | lane | 7.0 | 17.1 | Overture residential,service,unknown |
| rd-82a8a4de | (unnamed) | lane | 7.0 | 136.3 | Overture residential,service,unknown |
| rd-83237f67 | (unnamed) | lane | 7.0 | 64.3 | Overture residential,service,unknown |
| rd-837ce96c | (unnamed) | lane | 7.0 | 52.2 | Overture residential,service,unknown |
| rd-83edceb3 | (unnamed) | lane | 7.0 | 35.4 | Overture residential,service,unknown |
| rd-841bd5b0 | (unnamed) | lane | 7.0 | 73.8 | Overture residential,service,unknown |
| rd-844633d7 | (unnamed) | lane | 7.0 | 25.5 | Overture residential,service,unknown |
| rd-844df853 | (unnamed) | lane | 7.0 | 90.7 | Overture residential,service,unknown |
| rd-847cb6a8 | (unnamed) | lane | 7.0 | 33.1 | Overture residential,service,unknown |
| rd-84ca7bdd | (unnamed) | lane | 7.0 | 22.3 | Overture residential,service,unknown |
| rd-84d5ceac | (unnamed) | lane | 7.0 | 9.8 | Overture residential,service,unknown |
| rd-853d0ab8 | (unnamed) | lane | 7.0 | 30.4 | Overture residential,service,unknown |
| rd-8540c0a6 | (unnamed) | lane | 7.0 | 57.5 | Overture residential,service,unknown |
| rd-8555e910 | (unnamed) | lane | 7.0 | 92.0 | Overture residential,service,unknown |
| rd-856e47e2 | (unnamed) | lane | 7.0 | 9.3 | Overture residential,service,unknown |
| rd-85da0ef3 | (unnamed) | lane | 7.0 | 48.5 | Overture residential,service,unknown |
| rd-85fda91e | (unnamed) | lane | 7.0 | 47.6 | Overture residential,service,unknown |
| rd-861bb3ab | (unnamed) | lane | 7.0 | 170.3 | Overture residential,service,unknown |
| rd-863ebca2 | (unnamed) | lane | 7.0 | 43.6 | Overture residential,service,unknown |
| rd-86aea104 | (unnamed) | lane | 7.0 | 88.8 | Overture residential,service,unknown |
| rd-86e49647 | (unnamed) | lane | 7.0 | 41.7 | Overture residential,service,unknown |
| rd-870c79e3 | (unnamed) | lane | 7.0 | 63.8 | Overture residential,service,unknown |
| rd-87273f8d | (unnamed) | lane | 7.0 | 28.7 | Overture residential,service,unknown |
| rd-872c473c | (unnamed) | lane | 7.0 | 34.1 | Overture residential,service,unknown |
| rd-879fb296 | (unnamed) | lane | 7.0 | 47.5 | Overture residential,service,unknown |
| rd-87c62ddc | (unnamed) | lane | 7.0 | 88.2 | Overture residential,service,unknown |
| rd-87cb8056 | (unnamed) | lane | 7.0 | 28.7 | Overture residential,service,unknown |
| rd-87eece57 | (unnamed) | lane | 7.0 | 28.7 | Overture residential,service,unknown |
| rd-8858f788 | (unnamed) | lane | 7.0 | 75.8 | Overture residential,service,unknown |
| rd-887b75cf | (unnamed) | lane | 7.0 | 21.3 | Overture residential,service,unknown |
| rd-887d6d14 | (unnamed) | lane | 7.0 | 28.0 | Overture residential,service,unknown |
| rd-888210fd | (unnamed) | lane | 7.0 | 100.5 | Overture residential,service,unknown |
| rd-88ff67e1 | (unnamed) | lane | 7.0 | 40.8 | Overture residential,service,unknown |
| rd-890ece54 | (unnamed) | lane | 7.0 | 24.1 | Overture residential,service,unknown |
| rd-89396764 | (unnamed) | lane | 7.0 | 34.1 | Overture residential,service,unknown |
| rd-897cb571 | (unnamed) | lane | 7.0 | 14.4 | Overture residential,service,unknown |
| rd-898e468b | (unnamed) | lane | 7.0 | 29.3 | Overture residential,service,unknown |
| rd-8a15e034 | (unnamed) | lane | 7.0 | 43.1 | Overture residential,service,unknown |
| rd-8cec5963 | (unnamed) | lane | 7.0 | 18.0 | Overture residential,service,unknown |
| rd-8d34da61 | (unnamed) | lane | 7.0 | 25.5 | Overture residential,service,unknown |
| rd-8db1be61 | (unnamed) | lane | 7.0 | 28.2 | Overture residential,service,unknown |
| rd-8dbb5a0f | (unnamed) | lane | 7.0 | 31.0 | Overture residential,service,unknown |
| rd-8e04e6ec | (unnamed) | lane | 7.0 | 70.8 | Overture residential,service,unknown |
| rd-8e147f8b | (unnamed) | lane | 7.0 | 31.5 | Overture residential,service,unknown |
| rd-8e5f9ce3 | (unnamed) | lane | 7.0 | 26.2 | Overture residential,service,unknown |
| rd-8ead6fe1 | (unnamed) | lane | 7.0 | 29.9 | Overture residential,service,unknown |
| rd-8ee19efe | (unnamed) | lane | 7.0 | 78.1 | Overture residential,service,unknown |
| rd-8f48a9d9 | (unnamed) | lane | 7.0 | 13.1 | Overture residential,service,unknown |
| rd-8f7731b7 | (unnamed) | lane | 7.0 | 20.5 | Overture residential,service,unknown |
| rd-8ff854c7 | (unnamed) | lane | 7.0 | 57.7 | Overture residential,service,unknown |
| rd-90041394 | (unnamed) | lane | 7.0 | 23.4 | Overture residential,service,unknown |
| rd-90635fa5 | (unnamed) | lane | 7.0 | 67.5 | Overture residential,service,unknown |
| rd-90751319 | (unnamed) | lane | 7.0 | 177.9 | Overture residential,service,unknown |
| rd-91323d0a | (unnamed) | lane | 7.0 | 8.6 | Overture residential,service,unknown |
| rd-91bd7b35 | (unnamed) | lane | 7.0 | 10.1 | Overture residential,service,unknown |
| rd-91e55b78 | (unnamed) | lane | 7.0 | 29.1 | Overture residential,service,unknown |
| rd-91f8d8ea | (unnamed) | lane | 7.0 | 22.8 | Overture residential,service,unknown |
| rd-92348ab1 | (unnamed) | lane | 7.0 | 15.6 | Overture residential,service,unknown |
| rd-92b4366f | (unnamed) | lane | 7.0 | 133.7 | Overture residential,service,unknown |
| rd-9364054b | (unnamed) | lane | 7.0 | 24.4 | Overture residential,service,unknown |
| rd-9410a7d7 | (unnamed) | lane | 7.0 | 74.2 | Overture residential,service,unknown |
| rd-941ff2d2 | (unnamed) | lane | 7.0 | 22.6 | Overture residential,service,unknown |
| rd-9440f7db | (unnamed) | lane | 7.0 | 19.1 | Overture residential,service,unknown |
| rd-94c4f6de | (unnamed) | lane | 7.0 | 41.8 | Overture residential,service,unknown |
| rd-94c67dd2 | (unnamed) | lane | 7.0 | 29.8 | Overture residential,service,unknown |
| rd-951ef537 | (unnamed) | lane | 7.0 | 24.0 | Overture residential,service,unknown |
| rd-95285104 | (unnamed) | lane | 7.0 | 11.2 | Overture residential,service,unknown |
| rd-9591437c | (unnamed) | lane | 7.0 | 28.6 | Overture residential,service,unknown |
| rd-95cf5b00 | (unnamed) | lane | 7.0 | 23.7 | Overture residential,service,unknown |
| rd-9624d9ab | (unnamed) | lane | 7.0 | 15.5 | Overture residential,service,unknown |
| rd-962beffd | (unnamed) | lane | 7.0 | 22.0 | Overture residential,service,unknown |
| rd-96584199 | (unnamed) | lane | 7.0 | 16.8 | Overture residential,service,unknown |
| rd-96714aed | (unnamed) | lane | 7.0 | 41.7 | Overture residential,service,unknown |
| rd-96df2a49 | (unnamed) | lane | 7.0 | 13.4 | Overture residential,service,unknown |
| rd-96e69077 | (unnamed) | lane | 7.0 | 56.4 | Overture residential,service,unknown |
| rd-970947b5 | (unnamed) | lane | 7.0 | 82.2 | Overture residential,service,unknown |
| rd-97ac3b5c | (unnamed) | lane | 7.0 | 12.5 | Overture residential,service,unknown |
| rd-97f72eeb | (unnamed) | lane | 7.0 | 57.5 | Overture residential,service,unknown |
| rd-981a1096 | (unnamed) | lane | 7.0 | 97.9 | Overture residential,service,unknown |
| rd-98b08184 | (unnamed) | lane | 7.0 | 86.8 | Overture residential,service,unknown |
| rd-98c93beb | (unnamed) | lane | 7.0 | 16.4 | Overture residential,service,unknown |
| rd-992a8f8a | (unnamed) | lane | 7.0 | 11.6 | Overture residential,service,unknown |
| rd-996e134d | (unnamed) | lane | 7.0 | 99.0 | Overture residential,service,unknown |
| rd-9a96c70a | (unnamed) | lane | 7.0 | 33.4 | Overture residential,service,unknown |
| rd-9b67f02f | (unnamed) | lane | 7.0 | 19.7 | Overture residential,service,unknown |
| rd-9b92d3c9 | (unnamed) | lane | 7.0 | 47.4 | Overture residential,service,unknown |
| rd-9bf9aa3c | (unnamed) | lane | 7.0 | 59.7 | Overture residential,service,unknown |
| rd-9bf9ba31 | (unnamed) | lane | 7.0 | 15.7 | Overture residential,service,unknown |
| rd-9c18f71c | (unnamed) | lane | 7.0 | 59.0 | Overture residential,service,unknown |
| rd-9d135a4c | (unnamed) | lane | 7.0 | 12.1 | Overture residential,service,unknown |
| rd-9d19dc57 | (unnamed) | lane | 7.0 | 23.1 | Overture residential,service,unknown |
| rd-9d20a906 | (unnamed) | lane | 7.0 | 27.4 | Overture residential,service,unknown |
| rd-9d2709c2 | (unnamed) | lane | 7.0 | 100.3 | Overture residential,service,unknown |
| rd-9d7c4b89 | (unnamed) | lane | 7.0 | 191.9 | Overture residential,service,unknown |
| rd-9d99991b | (unnamed) | lane | 7.0 | 30.8 | Overture residential,service,unknown |
| rd-9e09fcec | (unnamed) | lane | 7.0 | 181.4 | Overture residential,service,unknown |
| rd-9ebe39cf | (unnamed) | lane | 7.0 | 14.8 | Overture residential,service,unknown |
| rd-9f0ff6c8 | (unnamed) | lane | 7.0 | 31.7 | Overture residential,service,unknown |
| rd-9f22f4a3 | (unnamed) | lane | 7.0 | 13.3 | Overture residential,service,unknown |
| rd-9f8aad86 | (unnamed) | lane | 7.0 | 88.5 | Overture residential,service,unknown |
| rd-9f8bb647 | (unnamed) | lane | 7.0 | 20.3 | Overture residential,service,unknown |
| rd-a0252b34 | (unnamed) | lane | 7.0 | 35.6 | Overture residential,service,unknown |
| rd-a0e1fbf7 | (unnamed) | lane | 7.0 | 29.2 | Overture residential,service,unknown |
| rd-a13c7907 | (unnamed) | lane | 7.0 | 38.1 | Overture residential,service,unknown |
| rd-a1555b87 | (unnamed) | lane | 7.0 | 14.5 | Overture residential,service,unknown |
| rd-a16a13a2 | (unnamed) | lane | 7.0 | 14.1 | Overture residential,service,unknown |
| rd-a1849fe3 | (unnamed) | lane | 7.0 | 25.5 | Overture residential,service,unknown |
| rd-a18ed18d | (unnamed) | lane | 7.0 | 11.4 | Overture residential,service,unknown |
| rd-a190090f | (unnamed) | lane | 7.0 | 42.2 | Overture residential,service,unknown |
| rd-a1c03f20 | (unnamed) | lane | 7.0 | 81.5 | Overture residential,service,unknown |
| rd-a1f8885c | (unnamed) | lane | 7.0 | 16.8 | Overture residential,service,unknown |
| rd-a2467f95 | (unnamed) | lane | 7.0 | 11.8 | Overture residential,service,unknown |
| rd-a248582b | (unnamed) | lane | 7.0 | 47.2 | Overture residential,service,unknown |
| rd-a26c1fca | (unnamed) | lane | 7.0 | 112.1 | Overture residential,service,unknown |
| rd-a27b55ef | (unnamed) | lane | 7.0 | 189.2 | Overture residential,service,unknown |
| rd-a3005db6 | (unnamed) | lane | 7.0 | 24.6 | Overture residential,service,unknown |
| rd-a36dab3a | (unnamed) | lane | 7.0 | 16.6 | Overture residential,service,unknown |
| rd-a3c7c1eb | (unnamed) | lane | 7.0 | 35.0 | Overture residential,service,unknown |
| rd-a4498378 | (unnamed) | lane | 7.0 | 29.5 | Overture residential,service,unknown |
| rd-a483f27a | (unnamed) | lane | 7.0 | 11.4 | Overture residential,service,unknown |
| rd-a49b9580 | (unnamed) | lane | 7.0 | 42.4 | Overture residential,service,unknown |
| rd-a4e520f2 | (unnamed) | lane | 7.0 | 41.5 | Overture residential,service,unknown |
| rd-a555a4d5 | (unnamed) | lane | 7.0 | 14.2 | Overture residential,service,unknown |
| rd-a5609238 | (unnamed) | lane | 7.0 | 13.0 | Overture residential,service,unknown |
| rd-a566e8d6 | (unnamed) | lane | 7.0 | 27.3 | Overture residential,service,unknown |
| rd-a5ec7acc | (unnamed) | lane | 7.0 | 39.9 | Overture residential,service,unknown |
| rd-a63c75e5 | (unnamed) | lane | 7.0 | 31.1 | Overture residential,service,unknown |
| rd-a70d6f42 | (unnamed) | lane | 7.0 | 24.4 | Overture residential,service,unknown |
| rd-a72927b3 | (unnamed) | lane | 7.0 | 20.8 | Overture residential,service,unknown |
| rd-a7614755 | (unnamed) | lane | 7.0 | 23.5 | Overture residential,service,unknown |
| rd-a842dd2f | (unnamed) | lane | 7.0 | 38.0 | Overture residential,service,unknown |
| rd-a8d5632c | (unnamed) | lane | 7.0 | 30.3 | Overture residential,service,unknown |
| rd-a8f70649 | (unnamed) | lane | 7.0 | 96.0 | Overture residential,service,unknown |
| rd-a95279bc | (unnamed) | lane | 7.0 | 21.0 | Overture residential,service,unknown |
| rd-a962dc28 | (unnamed) | lane | 7.0 | 16.7 | Overture residential,service,unknown |
| rd-aa450f85 | (unnamed) | lane | 7.0 | 36.6 | Overture residential,service,unknown |
| rd-aa5ac603 | (unnamed) | lane | 7.0 | 26.0 | Overture residential,service,unknown |
| rd-aaf4b183 | (unnamed) | lane | 7.0 | 25.5 | Overture residential,service,unknown |
| rd-ab9bd0c4 | (unnamed) | lane | 7.0 | 41.7 | Overture residential,service,unknown |
| rd-abe54af9 | (unnamed) | lane | 7.0 | 94.6 | Overture residential,service,unknown |
| rd-ac0c5b58 | (unnamed) | lane | 7.0 | 58.4 | Overture residential,service,unknown |
| rd-ac170d6c | (unnamed) | lane | 7.0 | 45.8 | Overture residential,service,unknown |
| rd-ad1a7045 | (unnamed) | lane | 7.0 | 27.5 | Overture residential,service,unknown |
| rd-ad22c546 | (unnamed) | lane | 7.0 | 34.3 | Overture residential,service,unknown |
| rd-adc68d90 | (unnamed) | lane | 7.0 | 34.2 | Overture residential,service,unknown |
| rd-ae01752f | (unnamed) | lane | 7.0 | 16.6 | Overture residential,service,unknown |
| rd-ae4429c6 | (unnamed) | lane | 7.0 | 66.7 | Overture residential,service,unknown |
| rd-ae54e6ae | (unnamed) | lane | 7.0 | 28.5 | Overture residential,service,unknown |
| rd-aea3adec | (unnamed) | lane | 7.0 | 55.0 | Overture residential,service,unknown |
| rd-af63c308 | (unnamed) | lane | 7.0 | 19.4 | Overture residential,service,unknown |
| rd-afb94033 | (unnamed) | lane | 7.0 | 20.3 | Overture residential,service,unknown |
| rd-b01d3adb | (unnamed) | lane | 7.0 | 31.4 | Overture residential,service,unknown |
| rd-b0d0a034 | (unnamed) | lane | 7.0 | 44.9 | Overture residential,service,unknown |
| rd-b0e9364d | (unnamed) | lane | 7.0 | 24.3 | Overture residential,service,unknown |
| rd-b109c1e7 | (unnamed) | lane | 7.0 | 43.8 | Overture residential,service,unknown |
| rd-b10ea841 | (unnamed) | lane | 7.0 | 92.1 | Overture residential,service,unknown |
| rd-b14a118b | (unnamed) | lane | 7.0 | 22.2 | Overture residential,service,unknown |
| rd-b19f72a6 | (unnamed) | lane | 7.0 | 26.4 | Overture residential,service,unknown |
| rd-b1b33859 | (unnamed) | lane | 7.0 | 38.1 | Overture residential,service,unknown |
| rd-b1ed5120 | (unnamed) | lane | 7.0 | 63.1 | Overture residential,service,unknown |
| rd-b1f530af | (unnamed) | lane | 7.0 | 56.3 | Overture residential,service,unknown |
| rd-b26cb29b | (unnamed) | lane | 7.0 | 175.5 | Overture residential,service,unknown |
| rd-b2c8da47 | (unnamed) | lane | 7.0 | 115.9 | Overture residential,service,unknown |
| rd-b323497c | (unnamed) | lane | 7.0 | 61.7 | Overture residential,service,unknown |
| rd-b3bec2e2 | (unnamed) | lane | 7.0 | 11.2 | Overture residential,service,unknown |
| rd-b3c6ec94 | (unnamed) | lane | 7.0 | 103.4 | Overture residential,service,unknown |
| rd-b3ed4f66 | (unnamed) | lane | 7.0 | 63.5 | Overture residential,service,unknown |
| rd-b3f094d0 | (unnamed) | lane | 7.0 | 52.1 | Overture residential,service,unknown |
| rd-b3f5a7e2 | (unnamed) | lane | 7.0 | 64.4 | Overture residential,service,unknown |
| rd-b457e0d2 | (unnamed) | lane | 7.0 | 89.6 | Overture residential,service,unknown |
| rd-b45f16c6 | (unnamed) | lane | 7.0 | 26.0 | Overture residential,service,unknown |
| rd-b4873192 | (unnamed) | lane | 7.0 | 9.7 | Overture residential,service,unknown |
| rd-b497c33a | (unnamed) | lane | 7.0 | 18.3 | Overture residential,service,unknown |
| rd-b4b46235 | (unnamed) | lane | 7.0 | 14.3 | Overture residential,service,unknown |
| rd-b56e1f29 | (unnamed) | lane | 7.0 | 60.3 | Overture residential,service,unknown |
| rd-b596b47e | (unnamed) | lane | 7.0 | 28.6 | Overture residential,service,unknown |
| rd-b5f64696 | (unnamed) | lane | 7.0 | 35.0 | Overture residential,service,unknown |
| rd-b613ab26 | (unnamed) | lane | 7.0 | 15.4 | Overture residential,service,unknown |
| rd-b6755059 | (unnamed) | lane | 7.0 | 11.7 | Overture residential,service,unknown |
| rd-b766c44a | (unnamed) | lane | 7.0 | 174.3 | Overture residential,service,unknown |
| rd-b7da7e5d | (unnamed) | lane | 7.0 | 31.0 | Overture residential,service,unknown |
| rd-b7e9c26a | (unnamed) | lane | 7.0 | 39.3 | Overture residential,service,unknown |
| rd-b836e6da | (unnamed) | lane | 7.0 | 15.6 | Overture residential,service,unknown |
| rd-b953f5b4 | (unnamed) | lane | 7.0 | 21.9 | Overture residential,service,unknown |
| rd-b9ab9547 | (unnamed) | lane | 7.0 | 36.9 | Overture residential,service,unknown |
| rd-b9ece0b4 | (unnamed) | lane | 7.0 | 81.9 | Overture residential,service,unknown |
| rd-b9edb927 | (unnamed) | lane | 7.0 | 83.8 | Overture residential,service,unknown |
| rd-b9f494ca | (unnamed) | lane | 7.0 | 34.0 | Overture residential,service,unknown |
| rd-ba3e9e0d | (unnamed) | lane | 7.0 | 9.8 | Overture residential,service,unknown |
| rd-ba6e2e82 | (unnamed) | lane | 7.0 | 64.7 | Overture residential,service,unknown |
| rd-ba86aef3 | (unnamed) | lane | 7.0 | 78.6 | Overture residential,service,unknown |
| rd-baee4318 | (unnamed) | lane | 7.0 | 29.1 | Overture residential,service,unknown |
| rd-bb136ac4 | (unnamed) | lane | 7.0 | 90.4 | Overture residential,service,unknown |
| rd-bb8093df | (unnamed) | lane | 7.0 | 70.7 | Overture residential,service,unknown |
| rd-bb9179b6 | (unnamed) | lane | 7.0 | 29.0 | Overture residential,service,unknown |
| rd-bbcf2532 | (unnamed) | lane | 7.0 | 24.1 | Overture residential,service,unknown |
| rd-bc4ea421 | (unnamed) | lane | 7.0 | 87.6 | Overture residential,service,unknown |
| rd-bc773157 | (unnamed) | lane | 7.0 | 137.0 | Overture residential,service,unknown |
| rd-bc8fc0fc | (unnamed) | lane | 7.0 | 21.2 | Overture residential,service,unknown |
| rd-bcd67d69 | (unnamed) | lane | 7.0 | 29.6 | Overture residential,service,unknown |
| rd-bd07169f | (unnamed) | lane | 7.0 | 8.2 | Overture residential,service,unknown |
| rd-bd6877da | (unnamed) | lane | 7.0 | 13.8 | Overture residential,service,unknown |
| rd-bda607c3 | (unnamed) | lane | 7.0 | 30.3 | Overture residential,service,unknown |
| rd-bdd67725 | (unnamed) | lane | 7.0 | 49.8 | Overture residential,service,unknown |
| rd-be0462e6 | (unnamed) | lane | 7.0 | 72.2 | Overture residential,service,unknown |
| rd-be25a308 | (unnamed) | lane | 7.0 | 69.1 | Overture residential,service,unknown |
| rd-be5d3fa2 | (unnamed) | lane | 7.0 | 109.8 | Overture residential,service,unknown |
| rd-bedfb1c9 | (unnamed) | lane | 7.0 | 25.8 | Overture residential,service,unknown |
| rd-bf3a6291 | (unnamed) | lane | 7.0 | 14.6 | Overture residential,service,unknown |
| rd-bfc951dd | (unnamed) | lane | 7.0 | 29.7 | Overture residential,service,unknown |
| rd-c01d6ac4 | (unnamed) | lane | 7.0 | 103.4 | Overture residential,service,unknown |
| rd-c01e60a7 | (unnamed) | lane | 7.0 | 103.7 | Overture residential,service,unknown |
| rd-c0e015b3 | (unnamed) | lane | 7.0 | 38.9 | Overture residential,service,unknown |
| rd-c19b9f82 | (unnamed) | lane | 7.0 | 51.7 | Overture residential,service,unknown |
| rd-c1ad1d32 | (unnamed) | lane | 7.0 | 123.6 | Overture residential,service,unknown |
| rd-c1dd4012 | (unnamed) | lane | 7.0 | 64.5 | Overture residential,service,unknown |
| rd-c2531244 | (unnamed) | lane | 7.0 | 31.6 | Overture residential,service,unknown |
| rd-c2e130e2 | (unnamed) | lane | 7.0 | 16.9 | Overture residential,service,unknown |
| rd-c326c4df | (unnamed) | lane | 7.0 | 13.2 | Overture residential,service,unknown |
| rd-c3e55cc1 | (unnamed) | lane | 7.0 | 26.2 | Overture residential,service,unknown |
| rd-c411d0eb | (unnamed) | lane | 7.0 | 14.6 | Overture residential,service,unknown |
| rd-c4d8d9fd | (unnamed) | lane | 7.0 | 37.7 | Overture residential,service,unknown |
| rd-c697289f | (unnamed) | lane | 7.0 | 145.5 | Overture residential,service,unknown |
| rd-c6b0f8c7 | (unnamed) | lane | 7.0 | 156.4 | Overture residential,service,unknown |
| rd-c6ce63a5 | (unnamed) | lane | 7.0 | 19.8 | Overture residential,service,unknown |
| rd-c6d45007 | (unnamed) | lane | 7.0 | 26.9 | Overture residential,service,unknown |
| rd-c77b166d | (unnamed) | lane | 7.0 | 61.8 | Overture residential,service,unknown |
| rd-c807c27d | (unnamed) | lane | 7.0 | 16.7 | Overture residential,service,unknown |
| rd-c84620d7 | (unnamed) | lane | 7.0 | 12.9 | Overture residential,service,unknown |
| rd-c861a25d | (unnamed) | lane | 7.0 | 39.1 | Overture residential,service,unknown |
| rd-c8e2cc73 | (unnamed) | lane | 7.0 | 20.2 | Overture residential,service,unknown |
| rd-c91b8a0b | (unnamed) | lane | 7.0 | 68.9 | Overture residential,service,unknown |
| rd-c987447f | (unnamed) | lane | 7.0 | 30.8 | Overture residential,service,unknown |
| rd-c9c50082 | (unnamed) | lane | 7.0 | 35.1 | Overture residential,service,unknown |
| rd-c9d80864 | (unnamed) | lane | 7.0 | 31.2 | Overture residential,service,unknown |
| rd-ca13cf6b | (unnamed) | lane | 7.0 | 53.0 | Overture residential,service,unknown |
| rd-ca2c7109 | (unnamed) | lane | 7.0 | 78.0 | Overture residential,service,unknown |
| rd-ca2d30bb | (unnamed) | lane | 7.0 | 38.0 | Overture residential,service,unknown |
| rd-ca7caa46 | (unnamed) | lane | 7.0 | 62.4 | Overture residential,service,unknown |
| rd-cabbd8bb | (unnamed) | lane | 7.0 | 180.7 | Overture residential,service,unknown |
| rd-caf6741b | (unnamed) | lane | 7.0 | 23.1 | Overture residential,service,unknown |
| rd-cb3d71b7 | (unnamed) | lane | 7.0 | 33.4 | Overture residential,service,unknown |
| rd-cb41da5d | (unnamed) | lane | 7.0 | 14.1 | Overture residential,service,unknown |
| rd-cb4ccd7b | (unnamed) | lane | 7.0 | 70.2 | Overture residential,service,unknown |
| rd-cb93f8d2 | (unnamed) | lane | 7.0 | 51.7 | Overture residential,service,unknown |
| rd-cbed4008 | (unnamed) | lane | 7.0 | 27.1 | Overture residential,service,unknown |
| rd-cc58c09f | (unnamed) | lane | 7.0 | 31.0 | Overture residential,service,unknown |
| rd-ccbd8c24 | (unnamed) | lane | 7.0 | 38.2 | Overture residential,service,unknown |
| rd-cd1e0166 | (unnamed) | lane | 7.0 | 24.8 | Overture residential,service,unknown |
| rd-cd2781a4 | (unnamed) | lane | 7.0 | 41.3 | Overture residential,service,unknown |
| rd-cde5ea77 | (unnamed) | lane | 7.0 | 11.9 | Overture residential,service,unknown |
| rd-cdf96d64 | (unnamed) | lane | 7.0 | 52.0 | Overture residential,service,unknown |
| rd-ce44bcdf | (unnamed) | lane | 7.0 | 214.6 | Overture residential,service,unknown |
| rd-cec87863 | (unnamed) | lane | 7.0 | 8.0 | Overture residential,service,unknown |
| rd-cedf086b | (unnamed) | lane | 10.0 | 14.9 | Overture residential,service,unknown; a pair merged to its midline |
| rd-cf35ea38 | (unnamed) | lane | 7.0 | 18.2 | Overture residential,service,unknown |
| rd-cf4c9684 | (unnamed) | lane | 7.0 | 104.0 | Overture residential,service,unknown |
| rd-cf7c6a76 | (unnamed) | lane | 7.0 | 102.5 | Overture residential,service,unknown |
| rd-cf8d09d6 | (unnamed) | lane | 7.0 | 48.2 | Overture residential,service,unknown |
| rd-d11218be | (unnamed) | lane | 7.0 | 23.5 | Overture residential,service,unknown |
| rd-d11db1f1 | (unnamed) | lane | 7.0 | 49.3 | Overture residential,service,unknown |
| rd-d15ea956 | (unnamed) | lane | 7.0 | 25.0 | Overture residential,service,unknown |
| rd-d16d6156 | (unnamed) | lane | 7.0 | 11.1 | Overture residential,service,unknown |
| rd-d17d66c3 | (unnamed) | lane | 7.0 | 20.6 | Overture residential,service,unknown |
| rd-d1fe1656 | (unnamed) | lane | 7.0 | 140.8 | Overture residential,service,unknown |
| rd-d2139b18 | (unnamed) | lane | 7.0 | 88.1 | Overture residential,service,unknown |
| rd-d226692f | (unnamed) | lane | 7.0 | 73.5 | Overture residential,service,unknown |
| rd-d2502d80 | (unnamed) | lane | 7.0 | 24.5 | Overture residential,service,unknown |
| rd-d2a781ca | (unnamed) | lane | 7.0 | 20.2 | Overture residential,service,unknown |
| rd-d308407c | (unnamed) | lane | 7.0 | 11.1 | Overture residential,service,unknown |
| rd-d36b764c | (unnamed) | lane | 7.0 | 75.4 | Overture residential,service,unknown |
| rd-d3d7b1f4 | (unnamed) | lane | 7.0 | 10.6 | Overture residential,service,unknown |
| rd-d45c032e | (unnamed) | lane | 7.0 | 89.6 | Overture residential,service,unknown |
| rd-d46f7198 | (unnamed) | lane | 7.0 | 45.6 | Overture residential,service,unknown |
| rd-d547e86d | (unnamed) | lane | 7.0 | 34.6 | Overture residential,service,unknown |
| rd-d557a658 | (unnamed) | lane | 7.0 | 32.5 | Overture residential,service,unknown |
| rd-d5764625 | (unnamed) | lane | 7.0 | 88.1 | Overture residential,service,unknown |
| rd-d5e03909 | (unnamed) | lane | 7.0 | 37.3 | Overture residential,service,unknown |
| rd-d6951d34 | (unnamed) | lane | 7.0 | 57.5 | Overture residential,service,unknown |
| rd-d6c956b3 | (unnamed) | lane | 7.0 | 19.1 | Overture residential,service,unknown |
| rd-d6f2758f | (unnamed) | lane | 7.0 | 28.0 | Overture residential,service,unknown |
| rd-d7178c8b | (unnamed) | lane | 7.0 | 69.5 | Overture residential,service,unknown |
| rd-d7270a99 | (unnamed) | lane | 7.0 | 159.0 | Overture residential,service,unknown |
| rd-d779103d | (unnamed) | lane | 7.0 | 50.0 | Overture residential,service,unknown |
| rd-d783e494 | (unnamed) | lane | 7.0 | 196.9 | Overture residential,service,unknown |
| rd-d8a16847 | (unnamed) | lane | 7.0 | 27.3 | Overture residential,service,unknown |
| rd-d8ae51c4 | (unnamed) | lane | 7.0 | 19.2 | Overture residential,service,unknown |
| rd-d8c20b39 | (unnamed) | lane | 7.0 | 33.7 | Overture residential,service,unknown |
| rd-d91fef57 | (unnamed) | lane | 7.0 | 31.6 | Overture residential,service,unknown |
| rd-d928422e | (unnamed) | lane | 7.0 | 13.5 | Overture residential,service,unknown |
| rd-d988e0c6 | (unnamed) | lane | 7.0 | 100.3 | Overture residential,service,unknown |
| rd-d9912b10 | (unnamed) | lane | 7.0 | 17.9 | Overture residential,service,unknown |
| rd-d9c43b32 | (unnamed) | lane | 7.0 | 19.4 | Overture residential,service,unknown |
| rd-d9d1404f | (unnamed) | lane | 7.0 | 33.5 | Overture residential,service,unknown |
| rd-da8de086 | (unnamed) | lane | 7.0 | 54.9 | Overture residential,service,unknown |
| rd-dbdb000b | (unnamed) | lane | 7.0 | 30.0 | Overture residential,service,unknown |
| rd-dc5179c0 | (unnamed) | lane | 7.0 | 46.2 | Overture residential,service,unknown |
| rd-dd046d59 | (unnamed) | lane | 7.0 | 26.0 | Overture residential,service,unknown |
| rd-dd490139 | (unnamed) | lane | 7.0 | 38.8 | Overture residential,service,unknown |
| rd-dd6ec701 | (unnamed) | lane | 7.0 | 8.6 | Overture residential,service,unknown |
| rd-de30e3bc | (unnamed) | lane | 7.0 | 19.3 | Overture residential,service,unknown |
| rd-dea0e4b3 | (unnamed) | lane | 7.0 | 10.8 | Overture residential,service,unknown |
| rd-dec518f2 | (unnamed) | lane | 7.0 | 49.9 | Overture residential,service,unknown |
| rd-df8e8f54 | (unnamed) | lane | 7.0 | 31.2 | Overture residential,service,unknown |
| rd-dfd8db3e | (unnamed) | lane | 7.0 | 21.4 | Overture residential,service,unknown |
| rd-e060f61a | (unnamed) | lane | 7.0 | 39.2 | Overture residential,service,unknown |
| rd-e0a5bfb5 | (unnamed) | lane | 7.0 | 8.9 | Overture residential,service,unknown |
| rd-e0d0d205 | (unnamed) | lane | 7.0 | 13.5 | Overture residential,service,unknown |
| rd-e0e4626b | (unnamed) | lane | 7.0 | 13.8 | Overture residential,service,unknown |
| rd-e1c60852 | (unnamed) | lane | 7.0 | 15.2 | Overture residential,service,unknown |
| rd-e25a75d1 | (unnamed) | lane | 7.0 | 28.4 | Overture residential,service,unknown |
| rd-e2684caa | (unnamed) | lane | 7.0 | 32.5 | Overture residential,service,unknown |
| rd-e2b78d2b | (unnamed) | lane | 7.0 | 71.2 | Overture residential,service,unknown |
| rd-e2cfac45 | (unnamed) | lane | 7.0 | 14.6 | Overture residential,service,unknown |
| rd-e36361a9 | (unnamed) | lane | 7.0 | 18.0 | Overture residential,service,unknown |
| rd-e375a0fc | (unnamed) | lane | 7.0 | 21.8 | Overture residential,service,unknown |
| rd-e3812746 | (unnamed) | lane | 7.0 | 66.0 | Overture residential,service,unknown |
| rd-e39e52ba | (unnamed) | lane | 7.0 | 55.2 | Overture residential,service,unknown |
| rd-e3ae0f48 | (unnamed) | lane | 7.0 | 32.3 | Overture residential,service,unknown |
| rd-e3f7b86d | (unnamed) | lane | 7.0 | 13.9 | Overture residential,service,unknown |
| rd-e43b11ab | (unnamed) | lane | 7.0 | 9.2 | Overture residential,service,unknown |
| rd-e45f55ce | (unnamed) | lane | 7.0 | 40.3 | Overture residential,service,unknown |
| rd-e4f02cec | (unnamed) | lane | 7.0 | 56.3 | Overture residential,service,unknown |
| rd-e505e568 | (unnamed) | lane | 7.0 | 59.1 | Overture residential,service,unknown |
| rd-e511bd84 | (unnamed) | lane | 7.0 | 30.5 | Overture residential,service,unknown |
| rd-e56a6f26 | (unnamed) | lane | 7.0 | 11.7 | Overture residential,service,unknown |
| rd-e5fa1fa3 | (unnamed) | lane | 7.0 | 23.8 | Overture residential,service,unknown |
| rd-e6509662 | (unnamed) | lane | 7.0 | 44.2 | Overture residential,service,unknown |
| rd-e660263e | (unnamed) | lane | 7.0 | 24.2 | Overture residential,service,unknown |
| rd-e6922fd4 | (unnamed) | lane | 7.0 | 23.3 | Overture residential,service,unknown |
| rd-e6d75ab8 | (unnamed) | lane | 7.0 | 45.8 | Overture residential,service,unknown |
| rd-e7192314 | (unnamed) | lane | 7.0 | 14.4 | Overture residential,service,unknown |
| rd-e7dac9fe | (unnamed) | lane | 7.0 | 44.8 | Overture residential,service,unknown |
| rd-e80d4452 | (unnamed) | lane | 7.0 | 10.7 | Overture residential,service,unknown |
| rd-e877ccf7 | (unnamed) | lane | 7.0 | 52.5 | Overture residential,service,unknown |
| rd-e89fbf21 | (unnamed) | lane | 7.0 | 64.7 | Overture residential,service,unknown |
| rd-e8be9478 | (unnamed) | lane | 7.0 | 21.9 | Overture residential,service,unknown |
| rd-e8e3ca14 | (unnamed) | lane | 7.0 | 71.4 | Overture residential,service,unknown |
| rd-e8f4534f | (unnamed) | lane | 7.0 | 34.4 | Overture residential,service,unknown |
| rd-e8fc45c3 | (unnamed) | lane | 7.0 | 24.7 | Overture residential,service,unknown |
| rd-e9169bc1 | (unnamed) | lane | 7.0 | 41.7 | Overture residential,service,unknown |
| rd-e93f1972 | (unnamed) | lane | 7.0 | 14.9 | Overture residential,service,unknown |
| rd-e96605cb | (unnamed) | lane | 7.0 | 36.1 | Overture residential,service,unknown |
| rd-ea09da1d | (unnamed) | lane | 7.0 | 8.8 | Overture residential,service,unknown |
| rd-ea4776e0 | (unnamed) | lane | 7.0 | 19.7 | Overture residential,service,unknown |
| rd-ea67a296 | (unnamed) | lane | 7.0 | 41.2 | Overture residential,service,unknown |
| rd-eafa172e | (unnamed) | lane | 7.0 | 14.9 | Overture residential,service,unknown |
| rd-eb107a01 | (unnamed) | lane | 7.0 | 14.7 | Overture residential,service,unknown |
| rd-eb6c757d | (unnamed) | lane | 7.0 | 164.6 | Overture residential,service,unknown |
| rd-eb7381ea | (unnamed) | lane | 7.0 | 27.4 | Overture residential,service,unknown |
| rd-ebb97cb1 | (unnamed) | lane | 7.0 | 24.7 | Overture residential,service,unknown |
| rd-ec0eecec | (unnamed) | lane | 7.0 | 118.6 | Overture residential,service,unknown |
| rd-ed746075 | (unnamed) | lane | 7.0 | 78.3 | Overture residential,service,unknown |
| rd-ee3171ea | (unnamed) | lane | 7.0 | 19.5 | Overture residential,service,unknown |
| rd-ee4ccedf | (unnamed) | lane | 7.0 | 39.4 | Overture residential,service,unknown |
| rd-ee597c40 | (unnamed) | lane | 7.0 | 47.2 | Overture residential,service,unknown |
| rd-eec9a2b7 | (unnamed) | lane | 7.0 | 55.1 | Overture residential,service,unknown |
| rd-ef0994fd | (unnamed) | lane | 7.0 | 65.9 | Overture residential,service,unknown |
| rd-efec7ddc | (unnamed) | lane | 7.0 | 29.5 | Overture residential,service,unknown |
| rd-f05afaca | (unnamed) | lane | 7.0 | 27.7 | Overture residential,service,unknown |
| rd-f06da1fb | (unnamed) | lane | 7.0 | 16.0 | Overture residential,service,unknown |
| rd-f0c178f1 | (unnamed) | lane | 7.0 | 57.9 | Overture residential,service,unknown |
| rd-f0e83486 | (unnamed) | lane | 7.0 | 65.8 | Overture residential,service,unknown |
| rd-f0f79b05 | (unnamed) | lane | 7.0 | 31.0 | Overture residential,service,unknown |
| rd-f1764e2c | (unnamed) | lane | 7.0 | 32.1 | Overture residential,service,unknown |
| rd-f21b0d1e | (unnamed) | lane | 7.0 | 8.1 | Overture residential,service,unknown |
| rd-f2847791 | (unnamed) | lane | 7.0 | 11.6 | Overture residential,service,unknown |
| rd-f2f322ce | (unnamed) | lane | 7.0 | 24.4 | Overture residential,service,unknown |
| rd-f33ffe24 | (unnamed) | lane | 7.0 | 70.4 | Overture residential,service,unknown |
| rd-f37a3e44 | (unnamed) | lane | 7.0 | 70.3 | Overture residential,service,unknown |
| rd-f3aede00 | (unnamed) | lane | 7.0 | 81.6 | Overture residential,service,unknown |
| rd-f3b35f6e | (unnamed) | lane | 7.0 | 146.5 | Overture residential,service,unknown |
| rd-f41cb53c | (unnamed) | lane | 7.0 | 16.1 | Overture residential,service,unknown |
| rd-f41cc7da | (unnamed) | lane | 7.0 | 46.2 | Overture residential,service,unknown |
| rd-f4365925 | (unnamed) | lane | 7.0 | 15.3 | Overture residential,service,unknown |
| rd-f4370f84 | (unnamed) | lane | 7.0 | 23.4 | Overture residential,service,unknown |
| rd-f44b5236 | (unnamed) | lane | 7.0 | 15.2 | Overture residential,service,unknown |
| rd-f4c93552 | (unnamed) | lane | 7.0 | 51.8 | Overture residential,service,unknown |
| rd-f57d3d9c | (unnamed) | lane | 7.0 | 10.1 | Overture residential,service,unknown |
| rd-f5a1740e | (unnamed) | lane | 7.0 | 107.7 | Overture residential,service,unknown |
| rd-f617d69e | (unnamed) | lane | 7.0 | 30.5 | Overture residential,service,unknown |
| rd-f628199f | (unnamed) | lane | 7.0 | 15.1 | Overture residential,service,unknown |
| rd-f7363333 | (unnamed) | lane | 7.0 | 89.6 | Overture residential,service,unknown |
| rd-f76bd6b1 | (unnamed) | lane | 7.0 | 22.9 | Overture residential,service,unknown |
| rd-f7b0dcb0 | (unnamed) | lane | 7.0 | 18.0 | Overture residential,service,unknown |
| rd-f7b1e37a | (unnamed) | lane | 7.0 | 85.0 | Overture residential,service,unknown |
| rd-f7fc80e9 | (unnamed) | lane | 7.0 | 50.4 | Overture residential,service,unknown |
| rd-f88423bf | (unnamed) | lane | 7.0 | 55.6 | Overture residential,service,unknown |
| rd-f8dfd29d | (unnamed) | lane | 7.0 | 34.0 | Overture residential,service,unknown |
| rd-f8fb28ca | (unnamed) | lane | 7.0 | 37.8 | Overture residential,service,unknown |
| rd-f91cb3cf | (unnamed) | lane | 7.0 | 36.6 | Overture residential,service,unknown |
| rd-f9971e59 | (unnamed) | lane | 7.0 | 35.7 | Overture residential,service,unknown |
| rd-f9bbb64b | (unnamed) | lane | 7.0 | 75.5 | Overture residential,service,unknown |
| rd-f9ebcb73 | (unnamed) | lane | 7.0 | 127.5 | Overture residential,service,unknown |
| rd-fa0ac40c | (unnamed) | lane | 7.0 | 24.8 | Overture residential,service,unknown |
| rd-fa2de06f | (unnamed) | lane | 7.0 | 28.4 | Overture residential,service,unknown |
| rd-fa49ea96 | (unnamed) | lane | 7.0 | 82.3 | Overture residential,service,unknown |
| rd-fa63ada9 | (unnamed) | lane | 7.0 | 32.5 | Overture residential,service,unknown |
| rd-fb8c5ee3 | (unnamed) | lane | 7.0 | 52.8 | Overture residential,service,unknown |
| rd-fbb66c40 | (unnamed) | lane | 7.0 | 125.4 | Overture residential,service,unknown |
| rd-fc589596 | (unnamed) | lane | 7.0 | 22.0 | Overture residential,service,unknown |
| rd-fcbde204 | (unnamed) | lane | 7.0 | 46.3 | Overture residential,service,unknown |
| rd-fcdd93a5 | (unnamed) | lane | 7.0 | 17.5 | Overture residential,service,unknown |
| rd-fd04acc6 | (unnamed) | lane | 7.0 | 26.6 | Overture residential,service,unknown |
| rd-fe0e7aa5 | (unnamed) | lane | 7.0 | 43.6 | Overture residential,service,unknown |
| rd-fe5e0e67 | (unnamed) | lane | 7.0 | 79.2 | Overture residential,service,unknown |
| rd-fe9b6fb9 | (unnamed) | lane | 7.0 | 79.6 | Overture residential,service,unknown |
| rd-feaf39cc | (unnamed) | lane | 7.0 | 43.5 | Overture residential,service,unknown |
| rd-ffa63a78 | (unnamed) | lane | 7.0 | 75.9 | Overture residential,service,unknown |
| rd-ffe50b4e | (unnamed) | lane | 7.0 | 15.3 | Overture residential,service,unknown |
| rd-ffe9391d | (unnamed) | lane | 7.0 | 57.9 | Overture residential,service,unknown |
| rd-fffd5bd8 | (unnamed) | lane | 7.0 | 10.5 | Overture residential,service,unknown |
| rd-91a38e15 | Industrial Road | lane | 7.0 | 45.8 | Overture service |
