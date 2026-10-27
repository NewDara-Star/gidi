# Makoro (district 19): the road plan and where each street comes from

Roads only, drawn on the new frame (1:3) at real widths. Real names live here only, never in the map. Houses and
places come in their own passes (NOW item 11).

## Count (Makoro hand pass 1, 27 Oct)

- District: 0.259 km² (Gidi), 567 × 734 m, the outline from the frame study (Makoko), named Makoro (its working name
  in docs/lagos-study/roads/NAMES.md, the owner to review). Two drawn neighbours: Saba (17) on the west, 934 m of shared
  border, and Lagoon University (18) on the north, 550 m; the lagoon and the districts not yet drawn on the other sides.
- Kept: **every street** inside the border but what its neighbours already hold, 144 road records, 7.13 km: 5 main
  roads, 7 local mains, 30 home streets, 102 lanes (about 28 km/km²).
- **Third Mainland Bridge** crosses the district's south-east corner for about 60 m (Overture's motorway, both
  carriageways): not drawn here; the bridge goes in whole by hand over the lagoon (NOW).

## How the lines were drawn

- As Lagoon University: each named street is its Overture segments merged per (name, kind), clipped to the border,
  pieces under 8 m dropped; Mùṣá's commonest values for the kind, to read.
- **Pairs**: none (no two records within 4 m along most of both).
- **Joins and the seam**: every road end the check found inside or within 1 m of another road was put on that road's
  line; Makoro's points moved, never its neighbours': map/d17 and map/d18 are unchanged (git diff, 0 lines).
- **First points inside**: roads reversed where their first point lay on or past the border, or split at an inside
  vertex where both ends did (rd-7f3618b1, split 7.7 m and 4.8 m: rd-24f03ba3 is its piece).
- **By hand**: lane rd-9964e2ac started on the Lagoon University seam node, spiked 2.4 m back out over the border and
  returned to the node; its other end only touched the border with nothing meeting it there. The spike and that end
  went, and it was reversed so it starts inside and ends on the node (7 -> 4 points). rd-7d2d314f, a 10 m closed loop
  at a junction of three local mains, went; the three (rd-325023fc, rd-828d8ae1, rd-8580b0ed) end on one node at its
  centre (moved 1.6-1.9 m). A 95 m closed lane (rd-1f1e690d) is a real loop street and stays.

## Every road

| id | real name | kind | width m | length m |
|---|---|---|---|---|
| rd-ee6344d1 | Adetia Olulu Street | home_street | 7.0 | 80.2 |
| rd-eb13ed2c | Ajoke Street | home_street | 7.0 | 157.0 |
| rd-76ef65d9 | Ayato Street | home_street | 7.0 | 90.4 |
| rd-fca76d74 | Balogun Street | home_street | 7.0 | 77.4 |
| rd-325023fc | Church Street | local_main | 8.5 | 127.4 |
| rd-15dfda60 | Clinic Road Lagos Mainland | main_road | 10.75 | 27.9 |
| rd-5de5c728 | Clinic Road Lagos Mainland | main_road | 10.75 | 41.6 |
| rd-5e71064c | Clinic Road Lagos Mainland | main_road | 10.75 | 49.5 |
| rd-a30a6a75 | Clinic Road Lagos Mainland | main_road | 10.75 | 21.5 |
| rd-a42ef54b | Clinic Road Lagos Mainland | main_road | 10.75 | 10.2 |
| rd-1ea5faeb | Falodun Street | home_street | 7.0 | 25.6 |
| rd-47335d4f | Falodun Street | home_street | 7.0 | 15.6 |
| rd-4c4f457b | Falodun Street | home_street | 7.0 | 76.7 |
| rd-2126b24b | Gbede Street | home_street | 7.0 | 70.0 |
| rd-944951e4 | Gbeto Street | home_street | 7.0 | 70.2 |
| rd-828d8ae1 | Igbehinadun Street | local_main | 8.5 | 54.1 |
| rd-a3bc415e | Igbore Street | home_street | 7.0 | 66.5 |
| rd-f8b55f72 | Ishola Street | home_street | 7.0 | 61.3 |
| rd-1ddbc022 | Iwaya Road | local_main | 8.5 | 407.1 |
| rd-0041971b | Joseph Harrison Street | home_street | 7.0 | 147.4 |
| rd-a213f82b | Joseph Harrison Street | home_street | 7.0 | 154.4 |
| rd-17b3977c | Karimu Ikotun Street | home_street | 7.0 | 130.6 |
| rd-7a9d8b06 | Makoko Road | home_street | 7.0 | 173.8 |
| rd-a0b710b5 | Makoko Road | local_main | 8.5 | 101.6 |
| rd-a27ac3a6 | Noble Street | home_street | 7.0 | 15.1 |
| rd-60af57a5 | Obalowu Street | home_street | 7.0 | 62.2 |
| rd-3e24fb71 | Ogayemi Street | home_street | 7.0 | 35.8 |
| rd-5b37fa9e | Ogayemi Street | home_street | 7.0 | 78.2 |
| rd-8046fa3d | Olaboye Olaleye Street | home_street | 7.0 | 62.9 |
| rd-96ee6354 | Owodunni Street | home_street | 7.0 | 138.6 |
| rd-12639618 | Oyediran Street | local_main | 8.5 | 90.6 |
| rd-54f425d2 | Pedro Street | home_street | 7.0 | 61.2 |
| rd-21f04156 | Ramotu Street | home_street | 7.0 | 152.7 |
| rd-95a3589b | Sariyu Street | local_main | 8.5 | 154.7 |
| rd-a15fbfdf | Shodipe Street | home_street | 7.0 | 30.8 |
| rd-d6d07182 | Tokunbo Street | home_street | 7.0 | 94.3 |
| rd-1d7ab31c | Victoria Street | home_street | 7.0 | 69.2 |
| rd-47634d58 | Wegbo Street | home_street | 7.0 | 70.9 |
| rd-550a7081 | Yovi Street | home_street | 7.0 | 99.7 |
| rd-75b5fbf4 | Zansi Close | home_street | 7.0 | 76.7 |
| rd-c379843c | Zansi Close | home_street | 7.0 | 33.6 |
| rd-00c23990 | (unnamed) | lane | 7.0 | 54.5 |
| rd-01f8d2ae | (unnamed) | lane | 7.0 | 17.1 |
| rd-02f296ca | (unnamed) | lane | 7.0 | 15.7 |
| rd-02ffdd52 | (unnamed) | lane | 7.0 | 11.8 |
| rd-03235208 | (unnamed) | lane | 7.0 | 60.0 |
| rd-056a9090 | (unnamed) | lane | 7.0 | 50.0 |
| rd-15cfe60b | (unnamed) | lane | 7.0 | 48.3 |
| rd-16e0d140 | (unnamed) | lane | 7.0 | 26.7 |
| rd-1bcd76bc | (unnamed) | lane | 7.0 | 37.5 |
| rd-1cb2c4c6 | (unnamed) | lane | 7.0 | 38.7 |
| rd-1ccc629b | (unnamed) | lane | 7.0 | 37.7 |
| rd-1eab0833 | (unnamed) | lane | 7.0 | 26.6 |
| rd-1ed6afc5 | (unnamed) | lane | 7.0 | 13.5 |
| rd-1ee9c189 | (unnamed) | lane | 7.0 | 109.5 |
| rd-1f1e690d | (unnamed) | lane | 7.0 | 94.7 |
| rd-1f230f56 | (unnamed) | lane | 7.0 | 34.0 |
| rd-20026df7 | (unnamed) | lane | 7.0 | 77.0 |
| rd-25176785 | (unnamed) | lane | 7.0 | 29.2 |
| rd-26636b69 | (unnamed) | lane | 7.0 | 20.5 |
| rd-27a2a3b2 | (unnamed) | lane | 7.0 | 14.5 |
| rd-2b5c8c23 | (unnamed) | lane | 7.0 | 36.9 |
| rd-2e90974a | (unnamed) | lane | 7.0 | 15.9 |
| rd-2efd823d | (unnamed) | lane | 7.0 | 9.6 |
| rd-37b816a7 | (unnamed) | lane | 7.0 | 17.2 |
| rd-3bcacee7 | (unnamed) | lane | 7.0 | 44.7 |
| rd-44ac2cc2 | (unnamed) | lane | 7.0 | 30.5 |
| rd-464bd450 | (unnamed) | lane | 7.0 | 29.9 |
| rd-469a753e | (unnamed) | lane | 7.0 | 50.6 |
| rd-471ea923 | (unnamed) | lane | 7.0 | 11.1 |
| rd-4b130b1f | (unnamed) | lane | 7.0 | 15.1 |
| rd-4b99ab8a | (unnamed) | lane | 7.0 | 24.3 |
| rd-5935ceb3 | (unnamed) | lane | 7.0 | 16.8 |
| rd-598854ff | (unnamed) | lane | 7.0 | 8.6 |
| rd-601a0904 | (unnamed) | lane | 7.0 | 23.5 |
| rd-623c0a77 | (unnamed) | lane | 7.0 | 64.7 |
| rd-660b0ab7 | (unnamed) | lane | 7.0 | 10.5 |
| rd-6c6b79b7 | (unnamed) | lane | 7.0 | 16.5 |
| rd-6d2adee8 | (unnamed) | lane | 7.0 | 19.5 |
| rd-6ddfbbaf | (unnamed) | lane | 7.0 | 9.8 |
| rd-6eaf54e4 | (unnamed) | lane | 7.0 | 15.8 |
| rd-71dfd55a | (unnamed) | lane | 7.0 | 37.3 |
| rd-74397a00 | (unnamed) | lane | 7.0 | 18.2 |
| rd-764784b5 | (unnamed) | lane | 7.0 | 19.7 |
| rd-7e78621a | (unnamed) | lane | 7.0 | 19.6 |
| rd-7f3618b1 | (unnamed) | lane | 7.0 | 4.8 |
| rd-8580b0ed | (unnamed) | local_main | 8.5 | 17.3 |
| rd-8818e615 | (unnamed) | lane | 7.0 | 24.2 |
| rd-890d5d25 | (unnamed) | lane | 7.0 | 17.8 |
| rd-8a8348f6 | (unnamed) | lane | 7.0 | 32.5 |
| rd-8cba1d21 | (unnamed) | lane | 7.0 | 16.6 |
| rd-8f19ae2c | (unnamed) | lane | 7.0 | 33.4 |
| rd-92b4be24 | (unnamed) | lane | 7.0 | 9.4 |
| rd-94661e80 | (unnamed) | lane | 7.0 | 42.4 |
| rd-9637fba8 | (unnamed) | lane | 7.0 | 25.6 |
| rd-98b75d9f | (unnamed) | lane | 7.0 | 10.8 |
| rd-98ec05b7 | (unnamed) | lane | 7.0 | 34.0 |
| rd-9964e2ac | (unnamed) | lane | 7.0 | 10.9 |
| rd-9da46095 | (unnamed) | lane | 7.0 | 75.7 |
| rd-a2a9ed26 | (unnamed) | lane | 7.0 | 31.7 |
| rd-a4190624 | (unnamed) | lane | 7.0 | 50.4 |
| rd-a42551ae | (unnamed) | lane | 7.0 | 17.1 |
| rd-a49f3493 | (unnamed) | lane | 7.0 | 119.0 |
| rd-a5ca7daa | (unnamed) | lane | 7.0 | 25.1 |
| rd-a8a49303 | (unnamed) | lane | 7.0 | 54.7 |
| rd-aaa57d9f | (unnamed) | lane | 7.0 | 34.9 |
| rd-ad9d0cd3 | (unnamed) | lane | 7.0 | 45.5 |
| rd-afe09db9 | (unnamed) | lane | 7.0 | 17.6 |
| rd-b0eec968 | (unnamed) | lane | 7.0 | 21.1 |
| rd-b108fd07 | (unnamed) | lane | 7.0 | 31.0 |
| rd-b12d9d0a | (unnamed) | lane | 7.0 | 94.6 |
| rd-b3d52452 | (unnamed) | lane | 7.0 | 47.7 |
| rd-b507d6b8 | (unnamed) | lane | 7.0 | 79.6 |
| rd-bc2b831e | (unnamed) | lane | 7.0 | 61.8 |
| rd-be951395 | (unnamed) | lane | 7.0 | 18.6 |
| rd-c5b8c5b8 | (unnamed) | lane | 7.0 | 63.5 |
| rd-c863f981 | (unnamed) | lane | 7.0 | 76.0 |
| rd-cc1ae7c2 | (unnamed) | lane | 7.0 | 33.0 |
| rd-cc2fe135 | (unnamed) | lane | 7.0 | 77.4 |
| rd-ceb244ba | (unnamed) | lane | 7.0 | 15.6 |
| rd-d2d948bb | (unnamed) | lane | 7.0 | 15.0 |
| rd-d49616c2 | (unnamed) | lane | 7.0 | 25.6 |
| rd-d5c307e2 | (unnamed) | lane | 7.0 | 20.7 |
| rd-d5ceb37c | (unnamed) | lane | 7.0 | 15.6 |
| rd-d90108c5 | (unnamed) | lane | 7.0 | 58.6 |
| rd-dc407a3d | (unnamed) | lane | 7.0 | 20.8 |
| rd-de8250dc | (unnamed) | lane | 7.0 | 51.3 |
| rd-dfa5bcea | (unnamed) | lane | 7.0 | 20.1 |
| rd-e0945b35 | (unnamed) | lane | 7.0 | 17.1 |
| rd-e23c07a2 | (unnamed) | lane | 7.0 | 41.2 |
| rd-e2fb4317 | (unnamed) | lane | 7.0 | 28.1 |
| rd-e499bb24 | (unnamed) | lane | 7.0 | 37.6 |
| rd-e4eed620 | (unnamed) | lane | 7.0 | 77.6 |
| rd-eb3c0bfc | (unnamed) | lane | 7.0 | 63.0 |
| rd-edc43b29 | (unnamed) | lane | 7.0 | 19.8 |
| rd-ee74cbe4 | (unnamed) | lane | 7.0 | 29.5 |
| rd-f0f70f91 | (unnamed) | lane | 7.0 | 52.5 |
| rd-f1938d9c | (unnamed) | lane | 7.0 | 44.7 |
| rd-f2ef7027 | (unnamed) | lane | 7.0 | 26.8 |
| rd-f2f6de70 | (unnamed) | lane | 7.0 | 23.7 |
| rd-f5d0e70c | (unnamed) | lane | 7.0 | 19.4 |
| rd-fc3709dc | (unnamed) | lane | 7.0 | 30.5 |
| rd-fd0258ae | (unnamed) | lane | 7.0 | 60.5 |
| rd-24f03ba3 | (unnamed) (split off rd-7f3618b1) | lane | 7.0 | 7.7 |
