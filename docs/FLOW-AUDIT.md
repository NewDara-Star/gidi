# City flow audit, 22 Oct 2026

Read-only: Gidi's frame (`web/layout-v2.json`, border roads in `web/network.json`, baked mains) against real Lagos's big roads
(Overture motorway/trunk/primary, rail) at 1:4. Transform: UTM 31N, origin E 507,720 / N 712,110; X = 1500 + dE/4, Y = 6625 - dN/4.
Distances are Gidi metres. Asked by the owner with the "Real Lagos roads" decision.

## Already flows like Lagos
- The island bridges: Long Bridge for Third Mainland, 485 m off; Wharf for Eko, 329 m; Channel for Carter, 444 m; Creek for Falomo, 193 m.
- Campus Road for Herbert Macaulay, 169 m off. Ayinde Avenue for Awolowo / Bank-Anthony, 92% within 300 m.
- Ring Road for the Apapa-Oshodi Expressway, 307 m off. Northern Road for Ikorodu Road, 462 m off, same district order. Rail 463 m off.
- 58% of real big-road length lies within 300 m of a Gidi arterial (80% with mains and border roads).
- Of 24 real district-to-district links, Gidi has 15 by road and 2 by rail only; 7 are missing.

## Findings, worst first
1. **No east-west corridor through the mainland middle** (real Oshodi-Oworonshoki Expressway, Oshodi to Third Mainland). Trips run 1.5-3x real: Oshodi-Ojota 4.10 km against 1.36, Mushin-Oshodi 2.46 against 0.90, Oshodi-Ikeja 2.90 against 1.54. The Maze holds 10.1 km of real corridor, 1.3 km of Gidi arterial. Fix: upgrade three border roads (Jimoh Way, Usman Avenue, Chukwuma Road, about 2.3 km) into one arterial, Ìbùdó north corner (8932,3712) to Marigold (9799,3094) to Long Bridge Road.
2. **Ìbùdó sits about 1.3 km south-west of its real places** (anchors 0.70-1.96 km off). Ojuelegba-Yaba 1.97 km against 0.54 real. Options: bring the corridors to it (finding 1, plus an Ojuelegba-Saba link of about 1.2 km via Hassan Street), or move Ìbùdó. Later districts must not twin Oshodi, Ilupeju, Anthony or Ojuelegba again.
3. **No way out north** (Lagos-Ibadan at Berger, Lagos-Abeokuta at Abule Egba). Fix: Babatunde Way as an expressway to a north edge gate (1.72 km), and a 300 m stub from the Old Motor Road.
4. **The Port is boxed in**: no Apapa Road / Ijora Causeway north (791 m off). Fix: Vaughan Road + Kunle Street as one arterial, Wharf Bridge head to Campus Road; Mile 2 truck junction in Jungle City.
5. **Lagos Mainland's bridgehead (Ebute Metta, Oyingbo, Otto, Costain) lands in Water Town.** Fix: give Saba the Campus Road strip, or hand-place an Oyingbo-style market and park on Water Town's Campus Road edge.
6. **Railside is a dead end** (one arterial east; no LASU-Isheri road). Fix: upgrade Kolade Road (2.65 km) or a new road north to Ikotun.
7. East end about 0.6 km east of real; order right, no fix needed.
8. Coastal Expressway stops 112 m short of the Ring Road at Mile Two: hand join.

## Verdict
Gidi has about two-thirds of Lagos's flow. The south and the island already flow like Lagos. The mainland middle does not: Oshodi, Mushin,
Maryland, Ojota and Yaba join through side streets. Six or seven road upgrades, mostly on existing border roads (about 9 km), close most of the gap.
