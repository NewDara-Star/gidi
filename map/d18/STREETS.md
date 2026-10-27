# Lagoon University (district 18): the road plan and where each street comes from

Roads only, drawn on the new frame (1:3) at real widths. Real names live here only, never in the map. Houses and
places come in their own passes (NOW item 11).

## Count (Lagoon University hand pass 1, 27 Oct)

- District: 0.296 km² (Gidi), 750 × 700 m, the outline from the frame study (UNILAG), named Lagoon University (its
  working name in docs/lagos-study/roads/NAMES.md, the owner to review). One drawn neighbour: Saba (17), on the west, 1,118 m of shared border; the
  lagoon and the districts not yet drawn on the other sides.
- Kept: **every street** inside the border but what Saba already holds, 186 road records, 8.34 km: 4 main
  roads, 7 local mains, 26 home streets, 149 lanes (about 28 km/km²; Saba 48: the university's
  grounds are open).

## How the lines were drawn

- As Saba: each named street is its Overture segments merged per (name, kind), clipped to the border, pieces under
  8 m dropped; Mùṣá's commonest values for the kind, to read. Akoka Road (82% along Saba's) left to Saba.
- **Trunk roads**: none in Overture here (the draft's kinds have no trunk, NOW; this draft read trunk as a main road
  in case).
- **Pairs** (two records within 4 m along more than 70% of both) merged to their midline, the width the kind's plus
  the gap, to read: University Road 16.5, 13.0 and 13.0 (three stretches), Commercial Road 11.5, Akinpelu Adesola Road
  11.0.
- **Joins and the seam**: every road end the check found inside or within 1 m of another road was put on that road's
  line; Lagoon University's points moved, never Saba's: three Saba records gained vertices on their own lines where Lagoon University's
  streets meet them (rd-beee86ae 6 -> 9, rd-f457aa87 16 -> 17, rd-d2b25ed0 2 -> 3 points; none moved more than
  0.005 m, their ends unchanged). A fourth vertex the steps had put on Saba's rd-382d0ebf, 0.9 m from its end and
  met by no road, was taken back out (the check found it almost meeting a Saba lane's end).
- **First points inside**: roads reversed where their first point lay on or past the border, or split at an inside
  vertex where both ends did.
- **By hand**: a 12 m loop at University Road's end lying wholly on Saba's main road rd-beee86ae (drawn twice) went.
  University Road's east stretch (rd-50c17625) was one record running out on one carriageway and back on the other,
  about 3 m apart: drawn again as one line on their midline from the junction node, 13.0 m as the road's other
  pairs. Four tiny closed loops at junction nodes, drawn twice over the junction, went: three main-road pieces of
  10-16 m (rd-2c9889a0, rd-594addae, rd-ea4fd90c) and a lane's 18 m spike (rd-d2bd9246); the roads that met them
  were joined again.
  University Road's west end (rd-cbdf1d43) ran out to a Saba lane's end and back, then about 25 m on top of Saba's
  main road rd-beee86ae, doubling back on itself: its line now runs from its 28th point straight over that lane's
  two end nodes to Saba's node on rd-beee86ae and stops there (44 -> 32 points, 272.5 -> 239.2 m); the lane
  rd-19fc93c6 that met the dropped points starts on the new line. Its last 18 m still lie over Saba's 7 m lane
  rd-0dd14298 (Saba's, frozen): owed to the seam's hand pass (NOW).

## Every road

| id | real name | kind | width m | length m |
|---|---|---|---|---|
| rd-88efb37b | Abdul Atta Road | home_street | 7.0 | 86.2 |
| rd-bb99c4cb | Abdul Karimu Street | home_street | 7.0 | 206.1 |
| rd-2f21f06c | Ajoke Street | home_street | 7.0 | 78.5 |
| rd-3a617e9c | Akinpelu Adesola Road | local_main | 11.0 | 237.2 |
| rd-ff10dc3e | Alvan Ikoku | home_street | 7.0 | 140.8 |
| rd-b7f867b6 | Audu Baale Street | home_street | 7.0 | 135.4 |
| rd-8b1270b6 | Balogun Street | home_street | 7.0 | 60.1 |
| rd-da2c802c | College of Medicine Road | home_street | 7.0 | 100.0 |
| rd-62765a6f | Commercial Road | local_main | 11.5 | 234.0 |
| rd-398eb5e9 | DLI Road | home_street | 7.0 | 95.3 |
| rd-7e83fad4 | DLI Road | home_street | 7.0 | 12.7 |
| rd-fda1e786 | Eni-Njoku Road | home_street | 7.0 | 38.6 |
| rd-101a3efc | FBA Walkway | lane | 7.0 | 72.4 |
| rd-f0adeeef | International School Road | local_main | 8.5 | 231.8 |
| rd-7fdace45 | Jibowu Close | home_street | 7.0 | 19.7 |
| rd-1bdcc524 | Kosoko Drive | home_street | 7.0 | 16.9 |
| rd-222cdf03 | Kosoko Drive | home_street | 7.0 | 17.9 |
| rd-62160353 | Kosoko Drive | home_street | 7.0 | 44.6 |
| rd-e2caec04 | Kosoko Drive | home_street | 7.0 | 11.0 |
| rd-f484643e | Kosoko Drive | home_street | 7.0 | 123.9 |
| rd-aae4983e | Majaro Street | home_street | 7.0 | 146.5 |
| rd-06c90b0e | Olumo Street | local_main | 8.5 | 67.2 |
| rd-aeedf423 | Otunba Payne Street | home_street | 7.0 | 203.7 |
| rd-fb55da79 | Owodunni Street | home_street | 7.0 | 7.6 |
| rd-52153841 | Ozolua Road | home_street | 7.0 | 103.9 |
| rd-74924639 | Pedro Street | home_street | 7.0 | 22.5 |
| rd-a59c26c7 | Ransom Kuti Road | home_street | 7.0 | 89.1 |
| rd-b26336f3 | Ransome Kuti Road | home_street | 7.0 | 121.4 |
| rd-e8c6cecc | Tafawa Balewa Way | local_main | 8.5 | 199.3 |
| rd-50c17625 | University Road | main_road | 13.0 | 41.8 |
| rd-8fe12b33 | University Road | main_road | 13.0 | 75.1 |
| rd-a63967f5 | University Road | main_road | 13.0 | 141.0 |
| rd-cbdf1d43 | University Road | main_road | 16.5 | 239.2 |
| rd-5ade0e89 | Victoria Street | home_street | 7.0 | 51.1 |
| rd-1b996860 | Wegbo Street | home_street | 7.0 | 23.1 |
| rd-3a18e376 | Zenith Bank Drive | home_street | 7.0 | 121.2 |
| rd-05c28688 | Zoology | lane | 7.0 | 94.8 |
| rd-002cb381 | (unnamed) | lane | 7.0 | 69.3 |
| rd-01e46108 | (unnamed) | lane | 7.0 | 9.5 |
| rd-0509a49a | (unnamed) | lane | 7.0 | 11.8 |
| rd-063bdec7 | (unnamed) | local_main | 8.5 | 207.9 |
| rd-0a3e197c | (unnamed) | lane | 7.0 | 11.3 |
| rd-0aa953d9 | (unnamed) | lane | 7.0 | 15.6 |
| rd-0af57907 | (unnamed) | lane | 7.0 | 13.8 |
| rd-0bd1336f | (unnamed) | lane | 7.0 | 15.3 |
| rd-0d338e7d | (unnamed) | lane | 7.0 | 11.2 |
| rd-0d4797ce | (unnamed) | lane | 7.0 | 32.5 |
| rd-0df4199f | (unnamed) | lane | 7.0 | 15.6 |
| rd-0dfeaf9c | (unnamed) | lane | 7.0 | 100.9 |
| rd-102547fa | (unnamed) | lane | 7.0 | 38.3 |
| rd-14ea4306 | (unnamed) | lane | 7.0 | 31.7 |
| rd-1729e0bc | (unnamed) | lane | 7.0 | 60.8 |
| rd-1766189b | (unnamed) | lane | 7.0 | 14.9 |
| rd-18eacb47 | (unnamed) | lane | 7.0 | 35.1 |
| rd-19fc93c6 | (unnamed) | lane | 7.0 | 19.0 |
| rd-1d26b132 | (unnamed) | lane | 7.0 | 24.7 |
| rd-1ed68d4f | (unnamed) | lane | 7.0 | 21.9 |
| rd-200faa0c | (unnamed) | lane | 7.0 | 232.2 |
| rd-21191aa1 | (unnamed) | lane | 7.0 | 33.6 |
| rd-227112d9 | (unnamed) | lane | 7.0 | 16.6 |
| rd-2580aa46 | (unnamed) | lane | 7.0 | 15.5 |
| rd-26308710 | (unnamed) | lane | 7.0 | 34.5 |
| rd-36227de2 | (unnamed) | lane | 7.0 | 17.3 |
| rd-36c22ddc | (unnamed) | lane | 7.0 | 29.3 |
| rd-37870772 | (unnamed) | lane | 7.0 | 43.1 |
| rd-37adc46a | (unnamed) | lane | 7.0 | 29.6 |
| rd-39f4cb85 | (unnamed) | local_main | 8.5 | 27.2 |
| rd-3a2a8309 | (unnamed) | lane | 7.0 | 50.4 |
| rd-3a8bdc3d | (unnamed) | lane | 7.0 | 12.9 |
| rd-3cb6063a | (unnamed) | lane | 7.0 | 36.5 |
| rd-3e4ac9ba | (unnamed) | lane | 7.0 | 18.2 |
| rd-3fbb3220 | (unnamed) | lane | 7.0 | 20.0 |
| rd-4121fa20 | (unnamed) | lane | 7.0 | 9.7 |
| rd-41398fd3 | (unnamed) | lane | 7.0 | 87.5 |
| rd-419a1bcd | (unnamed) | lane | 7.0 | 8.3 |
| rd-420224a2 | (unnamed) | lane | 7.0 | 19.3 |
| rd-44918a86 | (unnamed) | lane | 7.0 | 16.7 |
| rd-47c85c22 | (unnamed) | lane | 7.0 | 14.7 |
| rd-485635dd | (unnamed) | lane | 7.0 | 14.1 |
| rd-4b3f1c7a | (unnamed) | lane | 7.0 | 21.0 |
| rd-4cbf1562 | (unnamed) | lane | 7.0 | 19.1 |
| rd-4cca8c73 | (unnamed) | lane | 7.0 | 16.8 |
| rd-4d352cfd | (unnamed) | lane | 7.0 | 20.6 |
| rd-4dddbf2b | (unnamed) | lane | 7.0 | 16.7 |
| rd-4fb8daa1 | (unnamed) | lane | 7.0 | 54.4 |
| rd-50a5a7b3 | (unnamed) | lane | 7.0 | 24.7 |
| rd-5240f27c | (unnamed) | lane | 7.0 | 49.8 |
| rd-53c64ace | (unnamed) | lane | 7.0 | 40.2 |
| rd-549e72c6 | (unnamed) | lane | 7.0 | 20.7 |
| rd-5a8c238b | (unnamed) | lane | 7.0 | 19.7 |
| rd-5ab7c5d7 | (unnamed) | lane | 7.0 | 72.0 |
| rd-6342369a | (unnamed) | lane | 7.0 | 57.6 |
| rd-64211df3 | (unnamed) | lane | 7.0 | 18.3 |
| rd-65427c78 | (unnamed) | lane | 7.0 | 49.4 |
| rd-656b2cc4 | (unnamed) | lane | 7.0 | 24.1 |
| rd-65c65c04 | (unnamed) | lane | 7.0 | 19.4 |
| rd-6895fb83 | (unnamed) | lane | 7.0 | 34.2 |
| rd-68cbef81 | (unnamed) | lane | 7.0 | 20.2 |
| rd-69153389 | (unnamed) | lane | 7.0 | 17.5 |
| rd-6ab676df | (unnamed) | lane | 7.0 | 25.4 |
| rd-6d1d187d | (unnamed) | lane | 7.0 | 86.1 |
| rd-6e62b22c | (unnamed) | lane | 7.0 | 10.5 |
| rd-6efddd1c | (unnamed) | lane | 7.0 | 19.3 |
| rd-6f5c2609 | (unnamed) | lane | 7.0 | 37.1 |
| rd-70beb510 | (unnamed) | lane | 7.0 | 20.7 |
| rd-70c8f98c | (unnamed) | lane | 7.0 | 19.9 |
| rd-72d60c62 | (unnamed) | lane | 7.0 | 66.3 |
| rd-73f2ee8d | (unnamed) | lane | 7.0 | 34.9 |
| rd-7457076c | (unnamed) | lane | 7.0 | 13.8 |
| rd-74c3fece | (unnamed) | lane | 7.0 | 13.7 |
| rd-74e18d4a | (unnamed) | lane | 7.0 | 52.4 |
| rd-764ee780 | (unnamed) | lane | 7.0 | 53.2 |
| rd-76b0dddb | (unnamed) | lane | 7.0 | 24.9 |
| rd-7c8e2c80 | (unnamed) | lane | 7.0 | 18.4 |
| rd-7edc3bda | (unnamed) | lane | 7.0 | 20.3 |
| rd-85c1d3a4 | (unnamed) | lane | 7.0 | 23.8 |
| rd-87161f4e | (unnamed) | lane | 7.0 | 30.4 |
| rd-87502ec0 | (unnamed) | lane | 7.0 | 94.6 |
| rd-893de4b2 | (unnamed) | lane | 7.0 | 12.9 |
| rd-8ae61d7a | (unnamed) | lane | 7.0 | 50.6 |
| rd-8b8f359e | (unnamed) | lane | 7.0 | 62.2 |
| rd-8bfe852c | (unnamed) | lane | 7.0 | 16.6 |
| rd-8f485710 | (unnamed) | lane | 7.0 | 29.9 |
| rd-8f5a17f9 | (unnamed) | lane | 7.0 | 18.0 |
| rd-94f07ca8 | (unnamed) | lane | 7.0 | 24.4 |
| rd-951988cb | (unnamed) | lane | 7.0 | 42.4 |
| rd-99f58aae | (unnamed) | lane | 7.0 | 21.8 |
| rd-9c15884b | (unnamed) | lane | 7.0 | 11.7 |
| rd-9c17c8be | (unnamed) | lane | 7.0 | 13.1 |
| rd-9e4d19f2 | (unnamed) | lane | 7.0 | 65.4 |
| rd-9faa7d3a | (unnamed) | lane | 7.0 | 41.8 |
| rd-9fdba020 | (unnamed) | lane | 7.0 | 18.1 |
| rd-a0f893ba | (unnamed) | lane | 7.0 | 36.0 |
| rd-a4279862 | (unnamed) | lane | 7.0 | 36.3 |
| rd-a49131be | (unnamed) | lane | 7.0 | 18.1 |
| rd-a4ae04bb | (unnamed) | lane | 7.0 | 17.4 |
| rd-a672eb31 | (unnamed) | lane | 7.0 | 18.7 |
| rd-a7252ca2 | (unnamed) | lane | 7.0 | 16.5 |
| rd-a7d97480 | (unnamed) | lane | 7.0 | 30.5 |
| rd-aaac5af3 | (unnamed) | lane | 7.0 | 34.2 |
| rd-ab2fcbcf | (unnamed) | lane | 7.0 | 14.7 |
| rd-adfd7ec4 | (unnamed) | lane | 7.0 | 23.7 |
| rd-b1c2864c | (unnamed) | lane | 7.0 | 9.4 |
| rd-b3911fd2 | (unnamed) | lane | 7.0 | 12.6 |
| rd-b3978de2 | (unnamed) | lane | 7.0 | 28.5 |
| rd-b4dada42 | (unnamed) | lane | 7.0 | 11.4 |
| rd-b4efd803 | (unnamed) | lane | 7.0 | 10.9 |
| rd-b74319c8 | (unnamed) | lane | 7.0 | 25.6 |
| rd-b87d9b0a | (unnamed) | lane | 7.0 | 47.4 |
| rd-b9906e0b | (unnamed) | lane | 7.0 | 23.1 |
| rd-ba2c20c9 | (unnamed) | lane | 7.0 | 19.2 |
| rd-baaee880 | (unnamed) | lane | 7.0 | 14.3 |
| rd-bdedbdf2 | (unnamed) | lane | 7.0 | 33.9 |
| rd-beeb24aa | (unnamed) | lane | 7.0 | 17.8 |
| rd-c37701d1 | (unnamed) | lane | 7.0 | 21.8 |
| rd-c5c29691 | (unnamed) | lane | 7.0 | 19.6 |
| rd-c70cfb16 | (unnamed) | lane | 7.0 | 20.9 |
| rd-c71599e6 | (unnamed) | lane | 7.0 | 12.1 |
| rd-c7b4a176 | (unnamed) | lane | 7.0 | 22.7 |
| rd-c7dc0519 | (unnamed) | lane | 7.0 | 57.4 |
| rd-cb919b50 | (unnamed) | lane | 7.0 | 23.1 |
| rd-cba3526d | (unnamed) | lane | 7.0 | 9.1 |
| rd-ceb0613d | (unnamed) | lane | 7.0 | 11.6 |
| rd-d0dd97d2 | (unnamed) | lane | 7.0 | 25.2 |
| rd-d1521526 | (unnamed) | lane | 7.0 | 81.4 |
| rd-d1bd835f | (unnamed) | lane | 7.0 | 40.7 |
| rd-d26b7d19 | (unnamed) | lane | 7.0 | 8.5 |
| rd-dd68b62d | (unnamed) | lane | 7.0 | 46.2 |
| rd-e0aedfa3 | (unnamed) | lane | 7.0 | 22.7 |
| rd-e183247a | (unnamed) | lane | 7.0 | 19.9 |
| rd-e31c3d47 | (unnamed) | lane | 7.0 | 8.6 |
| rd-e457aa90 | (unnamed) | lane | 7.0 | 18.9 |
| rd-e4e394a3 | (unnamed) | lane | 7.0 | 53.5 |
| rd-e57c6181 | (unnamed) | lane | 7.0 | 31.7 |
| rd-ea507b0c | (unnamed) | lane | 7.0 | 29.6 |
| rd-eb763afe | (unnamed) | lane | 7.0 | 22.1 |
| rd-eec1876b | (unnamed) | lane | 7.0 | 16.5 |
| rd-efa0db54 | (unnamed) | lane | 7.0 | 19.3 |
| rd-f043b2ef | (unnamed) | lane | 7.0 | 32.3 |
| rd-f1d671d0 | (unnamed) | lane | 7.0 | 32.9 |
| rd-f26862f8 | (unnamed) | lane | 7.0 | 18.7 |
| rd-f28ad33a | (unnamed) | lane | 7.0 | 13.7 |
| rd-f732ee3c | (unnamed) | lane | 7.0 | 68.3 |
| rd-f964ee55 | (unnamed) | lane | 7.0 | 12.3 |
| rd-f9875655 | (unnamed) | lane | 7.0 | 26.3 |
| rd-fbbe23e3 | (unnamed) | lane | 7.0 | 21.2 |
