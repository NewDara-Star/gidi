# Echo names for the 51 districts (draft, 22 Oct 2026)

Working names for the 51 districts in `EARTH-CHECK.md` ("District list after the checks"), as the map format's fourth
call asks (`decisions/DECISIONS.md`, "The map format's four calls", point 4; the idea is in `decisions/IDEAS.md`,
"Place names: echo names"). **Every name here is a draft: the owner reviews it**, and any of them can change later.

**Study only.** The real district names in the second column stay in this file. They never go into `map/` files or
any other map data; the map gets only the echo name.

## The method

- **Built the way Lagos names are built.** Yoruba words joined and contracted (Òkè + iyì, Owó + gúnlẹ̀), the same
  shapes real names use: a virtue and its reward (Surulere), a thing that lands (Ajegunle), a town that gathers
  (Ilupeju), a hill, a waterside, a market's mouth.
- **Two ways to echo.**
  - *By sound:* a near-rhyme that is also a real Yoruba word with a fitting meaning (Saba for Yaba is the model;
    Àpapọ̀ for Apapa, Gbàgede for Gbagada, Àgbègbè for Agege).
  - *By meaning:* the real name, or what the place is famous for, said another way (Owógúnlẹ̀ for Ajegunle, both
    "money has landed"; Àgólo, "tin", for Tin Can; Ọ̀ṣùpá, "moon", for Satellite Town).
  - The best ones do both.
- **How clear.** The famous places (Lagos Island, VI, Ikoyi, Lekki, Surulere, Yaba, Mushin, Oshodi, Ikeja and
  Computer Village, Ajegunle, Apapa, Festac, Makoko, Ikorodu) get the clearest echo. Quiet districts get plain new
  names in the same style, with only a light echo or none.
- **Never** the real name, a straight copy, a cheap pun, or a word that is rude or unlucky. Words were checked for
  near-homophones with bad meanings (for example, *ìbálé* "virginity" ruled out an "Ibale"; *àjẹ́* "witch" ruled out an
  "Aje").
- **No clash with real places.** Each plain spelling, and each of its words, was checked against
  `docs/hand/realnames.txt` (full cores) and the 819 frame places with their gazetteer names (`places.csv`). Known
  Nigerian town names were avoided too (Iganna, Agbede, Irele, Okuta, Ota). Two drafts failed and were changed: Olorì
  (a core in `realnames.txt`) and Ìdẹ̀ra (a core). "Imole" appears only inside a church's name; it is kept.
- **Old Gidi names reused where they fit** (the 14 Yoruba district names of #118, `scripts/bake_web.py`): Saba, Àdàrú,
  Ìbùdó, Ọjà-Ńlá, Ìlú-Omi, Ẹnu-Ọjà, Pápákọ̀, Ọ̀dàn and Ààlà carry over to the district that took their inspiration.
  Five are not reused, see "Old names not carried over" below.
- **The Reach** stands in Àjọ̀dún (Festac, district 5), on Carnival Avenue, the old Gidi name for its Seventh Avenue
  street (DECISIONS, "The Reach goes with Festac into the new map").
- Tone marks are given as best known; the plain spelling is the form for signs and plain text. A
  Yoruba speaker should check the ones marked *check* below.

## The 51 names

| # | Real district (study only) | Echo name | Plain spelling | Meaning / how built | Why it echoes |
|---|---|---|---|---|---|
| 1 | Agbara-Morogbo | Ààlà | Aala | "boundary, limit". Old Gidi name of the Border | Agbara sits on the Lagos-Ogun line at the frame's west edge; reused from the old Border district |
| 2 | Okokomaiko-Ijanikin-Otto | Ọ̀kọ̀ọ̀kan | Okookan | "one by one" | Sound: *Oko-ko…* opens like Okokomaiko; meaning: the bus stops strung one by one down the Badagry road |
| 3 | Alaba-Ojo-Trade Fair | Ọjà-Ńlá | Oja-Nla | "the great market". Old Gidi name of the Bazaar | Meaning: Alaba International Market and the Trade Fair halls; reused |
| 4 | Iba-Isheri-Olofin | Ìbẹ̀rẹ̀ | Ibere | "the beginning" | Light sound echo of Iba (*Ib-*); a quiet district, plain new name |
| 5 | Festac | Àjọ̀dún | Ajodun | "festival, celebration" | Meaning: FESTAC is the Festival of Arts and Culture; the festival town. The Reach stands here, on Carnival Avenue |
| 6 | Mile 2-Amuwo Odofin | Àmúwá | Amuwa | "what is brought (in)" | Sound: Amuwo to Amuwa, one vowel; meaning: the port's goods and trucks brought through the Mile 2 interchange |
| 7 | Satellite Town | Ìlú-Ọ̀ṣùpá | Ilu-Osupa | "moon town" | Meaning: the moon is the satellite; a Lagosian gets it in a beat |
| 8 | Kirikiri-Tin Can | Àgólo | Agolo | "tin, a tin can" | Meaning: Tin Can Island port said in Yoruba. *check* tone marks (written *agolo* in dictionaries) |
| 9 | Ajegunle | Owógúnlẹ̀ | Owogunle | "money has landed (at home)" | Meaning and build: Ajegunle is *ajé gúnlẹ̀*, "wealth has landed"; *owó* (money) swaps for *ajé*. Its English nickname stays Jungle City |
| 10 | Apapa | Àpapọ̀ | Apapo | "the total, everything gathered together" | Sound: Apapa to Apapọ, one vowel; meaning: the port where all the goods come together |
| 11 | Ijora-Iganmu-Costain | Ìtàgé | Itage | "stage, theatre" | Meaning: the National Theatre at Iganmu (Gidi's The Crown); light sound echo of the *I-* names. *check*: it is a loan from English "stage" |
| 12 | Aguda-Coker-Orile | Orírun | Orirun | "origin, source" | Sound and meaning: Orile ("homeland") to Orírun ("origin"), a near-synonym with the same start |
| 13 | Surulere | Ìfaradàlérè | Ifaradalere | "endurance has its reward" (*ìfaradà ní èrè*) | Build: Surulere is *sùúrù ní èrè*, "patience has its reward"; a near-synonym virtue, same shape and the same *-lere* ending. Spoken short: Faradà |
| 14 | Itire-Lawanson-Ijesha | Ìtura | Itura | "relief, refreshment" | Light sound echo of Itire (*It-…*); plain new name |
| 15 | Mushin | Àdàrú | Adaru | "confusion, a mix-up". Old Gidi name of the Maze | Meaning: Mushin's famous tangle and noise; reused (the Àdàrú motor park is already the Lagos pass's spot 1) |
| 16 | Ebute Metta-Oyingbo-Otto | Etídò-Mẹ́ta | Etido-Meta | "three water-edges" (*etí odò*, the riverside) | Build: Ebute Metta is "three landings"; a different word for the waterside, same *Meta* |
| 17 | Yaba | Saba | Saba | the old Gidi name (#118) | Sound: Yaba to Saba, one letter. The model for the method |
| 18 | UNILAG | Akẹ́kọ̀ọ́ | Akekoo | "student" | Sound: the campus is at Akoka (*Ak-ko…*); meaning: the university town. The school itself keeps its old Gidi name, Lagoon University |
| 19 | Makoko | Ìlú-Omi | Ilu-Omi | "water town". Old Gidi name of Water Town | Meaning: the stilt town on the lagoon; reused |
| 20 | Lagos Island (Eko) | Àkọ́ | Ako | "the first" (the first town) | Sound: Èkó to Àkọ́, the same tones with the vowels changed; meaning: the old first town of the city. Its English nickname stays Old Island |
| 21 | Ikoyi | Òkè-Iyì | Oke-Iyi | "hill of prestige, of honour"; spoken Òkèyì | Sound: Okèyì against Ikoyi; meaning: old money and status. The old Heights name Òkè-Ọlà can name its Banana Island quarter |
| 22 | Victoria Island | Erékùṣù-Ìṣẹ́gun | Isegun Island | "island of victory" | Meaning: Victoria means victory; a Lagosian says "VI", Gidi says "Isegun Island" |
| 23 | Lekki Phase 1 | Ìlẹ̀kẹ̀ | Ileke | "beads" (worn by chiefs and the rich) | Sound: Ileke against Lekki; meaning: adornment and new money |
| 24 | Lekki-Agungi-Chevron | Ìlẹ̀kẹ̀-Kejì | Ileke Keji | "Ìlẹ̀kẹ̀ the second" | Lagos says Lekki Phase 1 and Phase 2 down the same road; the estate strip is Ìlẹ̀kẹ̀'s second part |
| 25 | Ajah | Àjọ | Ajo | "a gathering; the rotating savings group" | Sound: Ajah to Ajo; meaning: the far junction where the roads, buses and the market all gather |
| 26 | Sangotedo-Abijo-Lakowe | Ọ̀dàn | Odan | "open grassland, the plain". Old Gidi name of the Frontier | Meaning: the open, half-built frontier at the end of the peninsula; reused |
| 27 | Shomolu-Bariga | Ìtẹ̀wé | Itewe | "printing" | Meaning: Shomolu is Lagos's printing-press town |
| 28 | Gbagada-Ogudu | Gbàgede | Gbagede | "open square, plaza" | Sound: Gbagada to Gbagede; meaning: open, roomy ground after the dense south |
| 29 | Ilupeju | Ìlú-Pàdé | Ilupade | "the town meets" | Build: Ilupeju is *ìlú pé jọ*, "the town gathered"; a synonym in the same shape |
| 30 | Isolo-Ladipo | Ìṣọ́lẹ̀ | Isole | "keeping watch over the land" | Sound: Isolo to Isole, one vowel. Plain meaning, no joke |
| 31 | Okota | Òkòtó | Okoto | "spinning top" (the child's toy) | Sound: Okota to Okoto, one vowel. *check* the tones (dictionaries give *òkòtó*) |
| 32 | Oshodi-Mafoluku | Ìbùdó | Ibudo | "camp, station, base". Old Gidi name of the Hub | Meaning: Oshodi, the great bus station and interchange; reused |
| 33 | Airport (MMIA) | Pápákọ̀ | Papako | "a vehicle park" (*pápákọ̀ òfurufú*, airport). Old Gidi name | Meaning: the airport; reused. *check*: alone the word means any vehicle park; the full form may be wanted |
| 34 | Ikeja GRA-Cantonment | Ìkẹ́jọba | Ikejoba | "the government's keeping" (*ìkẹ́*, care, + *ìjọba*, government) | Sound: Ikeja + ijoba; meaning: the Government Reserved Area |
| 35 | Computer Village-Allen-Maryland | Abúlé-Ẹ̀rọ | Abule-Ero | "village of machines" | Meaning: Computer Village said in Yoruba. Gadget Village stays as the market's own name |
| 36 | Alausa-Oregun-Ogba | Àláṣẹ | Alase | "one who holds authority" | Sound: Alausa to Alase; meaning: the seat of the state government (Gidi's The Capital) |
| 37 | Agege-Ifako-Ijaiye | Agbègbè | Agbegbe | "the area, the surroundings" | Sound: Agege to Agbegbe, very close |
| 38 | Ketu-Mile 12 | Ẹnu-Ọjà | Enu-Oja | "the market's mouth". Old Gidi name of Food Gate | Meaning: the Mile 12 produce market at the city's northern gate; reused |
| 39 | Magodo-Omole-Berger | Àgbàlá | Agbala | "the walled yard, courtyard" | Meaning: gated, walled estates (Gidi's The Estate). Light sound echo of Magodo's *-a-* |
| 40 | Agbado-Oke Odo | Òkè-Ọkà | Oke-Oka | "hill of grain" | Sound: Oke Odo to Oke-Oka; meaning: *àgbàdo* is maize, *ọkà* is grain. A double echo |
| 41 | Ipaja-Ayobo | Ayọ̀wá | Ayowa | "joy has come" | Build: Ayobo is *ayọ̀ bọ̀*, "joy is coming"; a near-synonym |
| 42 | Egbeda-Idimu | Ìdílé | Idile | "family, household" | Sound: Idimu to Idile; meaning: a family suburb |
| 43 | Ikotun-Igando | Okotun | Okotun | "new farm" (*oko tuntun*, contracted) | Sound: Ikotun to Okotun; meaning: new land at the city's fringe |
| 44 | Ejigbo | Èjìdò | Ejido | "two waters" (*èjì odò*) | Sound: Ejigbo to Ejido; it lies between the Ikotun-Ejigbo stream and the airport water |
| 45 | Ijegun-Abaranje-Isheri Osun | Ìrọ̀rùn | Irorun | "ease, comfort" | Light echo of Ijegun's *I-…un*; a quiet district, plain new name |
| 46 | Agric-Isawo-Owutu | Àgbẹ̀ | Agbe | "farmer" | Sound and meaning: "Agric" (the old agricultural settlement) to Àgbẹ̀ |
| 47 | Ikorodu Town | Ìkórè | Ikore | "harvest" | Sound: *Iko-r…* opens like Ikorodu; meaning: the farm town and its big market |
| 48 | Odogunyan-Ogijo | Odò-Àyàn | Odo-Ayan | "the river of Àyàn" (the drum's spirit) | Sound: Odo-gun-yan to Odo-A-yan |
| 49 | Igbogbo-Bayeku | Ìgboro | Igboro | "the town's open streets" | Sound: Igbogbo to Igboro, one consonant |
| 50 | Ijede-Gberigbe | Ìjẹ́rí | Ijeri | "testimony, witness" | Sound: Ijede to Ijeri |
| 51 | Imota-Ewu-Elepe | Ìmọ́lẹ̀ | Imole | "light" | Sound: Imota to Imole; the city's eastern edge, where the sun comes up |

## Old names not carried over

- **Ẹ̀gbẹ́-Irin** (Railside, "beside the rail", after Agege): its plain spelling contains *Egbe*, a real place
  (Egbe-Idimu, inside district 43). Agege gets Agbègbè. Ẹ̀gbẹ́-Irin can still name the rail quarter inside it.
- **Èbúté-Ńlá** (the Port, "the great harbour"): *Ebute* is the real Ebute Metta (district 16) and Ebute Ero, so a
  Lagosian would look in the wrong place. Apapa gets Àpapọ̀.
- **Igbó-Ọ̀la** (Jungle City): read plainly, *Igbo* is also street slang for cannabis, and with Ajegunle's
  reputation that is a cheap shot. Ajegunle gets Owógúnlẹ̀ and keeps "Jungle City" as its English nickname.
- **Etí-Òkun** (Old Shore, after Ikorodu): *òkun* is the sea, but Ikorodu is on the lagoon, and the name does not
  echo Ikorodu. Ikorodu gets Ìkórè. (The right word for the lagoon edge, *Etí-Ọ̀sà*, is the real Eti-Osa LGA.)
- **Òkè-Ọlà** (the Heights): Ikoyi gets the closer echo Òkè-Iyì; Òkè-Ọlà is free for its Banana Island quarter.
- The English nicknames (Old Island, The Estate, The Capital, The Maze, The Hub, and others) can stay as nicknames
  where their district carries on.

## Unsure, for a Yoruba speaker to check

- **Tone marks:** Àgólo (dictionaries write *agolo*, tone unclear), Òkòtó (one dialect source), Agbègbè, Ìtàgé.
- **Ìtàgé** is a loan of English "stage"; fine in speech, but less "built from Yoruba" than the others.
- **Pápákọ̀** alone means any vehicle park; the old name is kept, but *Pápákọ̀-Òfurufú* is the full word for an airport.
- **Okotun** (43) and **Àmúwá** (6) are one sound off their real names, as close as Saba; the owner may want them
  further away.
- **Àdàrú** ("confusion") for Mushin is a little sharp; it was already the Maze's name, and the game work uses it.
- **Ìfaradàlérè** is long; on signs it may read as Faradà.
