# Unit seeds: name | lat,lon ; lat,lon ... Coordinates from general knowledge [K], approximate (+-0.5-1 km).
# A unit = the 250 m cells closest (by road-penalised walking distance, inside one LGA polygon, on land) to any of its seeds.
SEEDS = """
Isale Eko-Idumota-Marina|6.4600,3.3850;6.4530,3.3910;6.4570,3.3800
Onikan-Lafiaji (Lagos Island East)|6.4460,3.4000
Obalende|6.4490,3.4060
Ikoyi-Banana Island|6.4520,3.4350;6.4560,3.4470;6.4440,3.4200
Victoria Island|6.4290,3.4200;6.4250,3.4100
Oniru-Lekki Phase 1|6.4330,3.4500;6.4470,3.4720
Ikate-Agungi-Osapa-Jakande|6.4380,3.4900;6.4480,3.5100;6.4440,3.5250
Ikota-VGC-Chevron|6.4460,3.5420;6.4400,3.5300
Ajah-Abraham Adesanya|6.4670,3.5730;6.4720,3.6030
Badore|6.5050,3.5950
Sangotedo|6.4700,3.6300
Awoyaya-Lakowe|6.4730,3.6900;6.4800,3.7300
Eleko-Akodo-Ibeju|6.4500,3.8400;6.4450,3.9200
Lekki FTZ-Dangote|6.4300,4.0000;6.4200,4.0500
Epe town-Noforija|6.5850,3.9830;6.5900,3.9600
Ejinrin-Agbowa|6.6300,3.8800;6.6500,3.7200
Ikorodu town|6.6170,3.5080
Agric-Majidun-Ogolonto|6.6050,3.4600;6.5990,3.4800
Isawo-Owutu-Odogunyan|6.6450,3.4800;6.6600,3.4900
Ogijo-Sagamu Rd|6.6800,3.5150
Igbogbo-Baiyeku|6.5900,3.5300
Ijede|6.5700,3.5900
Imota|6.6600,3.6400
Ketu-Mile 12-Ikosi|6.6080,3.3990;6.5970,3.3880
Ojota-Ogudu|6.5860,3.3800;6.5780,3.3870
Magodo|6.6150,3.3850
Isheri-Olowora (Ikosi-Isheri)|6.6380,3.4050
Gbagada|6.5550,3.3850;6.5620,3.3800
Oworonshoki|6.5550,3.4050
Shomolu-Pedro-Onipanu|6.5400,3.3800;6.5380,3.3650
Bariga-Akoka|6.5400,3.3900;6.5250,3.3920
UNILAG|6.5170,3.3990
Yaba-Sabo-Jibowu|6.5100,3.3780;6.5190,3.3710
Ebute Metta-Oyingbo-Otto-Iddo|6.4880,3.3800;6.4800,3.3850;6.4720,3.3830
Makoko-Iwaya|6.4970,3.3880;6.5050,3.3920
Surulere (Ojuelegba-Bode Thomas-Stadium)|6.5070,3.3640;6.4950,3.3550
Aguda-Ijesha-Coker|6.4930,3.3350;6.4950,3.3250;6.4800,3.3350
Itire-Lawanson|6.5150,3.3400
Iganmu-Orile|6.4770,3.3550;6.4720,3.3420
Mushin-Idi Araba-Odi Olowo|6.5300,3.3500;6.5170,3.3550
Ilupeju|6.5530,3.3600
Papa Ajao-Ladipo|6.5420,3.3420
Oshodi-Mafoluku|6.5540,3.3437;6.5600,3.3300
Ajao Estate|6.5450,3.3200
Isolo|6.5300,3.3200;6.5250,3.3350
Okota-Ago Palace|6.5100,3.3050
Ejigbo|6.5550,3.3000
Apapa-Tin Can|6.4430,3.3630;6.4430,3.3700;6.4380,3.3420
Ijora-Badia|6.4680,3.3720
Ajegunle (Ajeromi)|6.4550,3.3330
Amukoko-Layeni (Ifelodun)|6.4620,3.3450
Mile 2-Amuwo|6.4640,3.3140;6.4600,3.3000
Kirikiri-Navy Town|6.4450,3.3050;6.4490,3.2910
Festac|6.4680,3.2830
Satellite Town|6.4500,3.2600
Trade Fair-Abule Ado|6.4650,3.2550;6.4700,3.2300
Alaba-Ojo-LASU|6.4600,3.1900;6.4650,3.2000
Okokomaiko|6.4700,3.1640
Iba|6.4950,3.1850
Ijanikin-Igbo Elerin|6.4900,3.1300
Agbara-Morogbo|6.5050,3.0800;6.4700,3.0700
Badagry town-Seme|6.4180,2.8850;6.4300,2.8000
Iyana Ipaja|6.6120,3.2960
Ipaja-Ayobo-Mosan|6.6150,3.2600;6.6000,3.2300;6.6350,3.2700
Alagbado-Agbado|6.6650,3.2700
Egbeda-Akowonjo|6.5920,3.2900;6.6000,3.3050
Idimu|6.5800,3.2500
Ikotun|6.5500,3.2650
Igando|6.5550,3.2350;6.5150,3.2200
Egbe|6.5650,3.2800
Ikeja GRA|6.5800,3.3530
Allen-Opebi-Computer Village|6.6000,3.3550;6.5940,3.3420
Ogba-Agidingbi-Alausa industrial|6.6150,3.3500;6.6170,3.3590;6.6320,3.3440;6.6020,3.3680
Ojodu-Berger-Omole|6.6400,3.3750;6.6380,3.3650
Maryland-Onigbongbo|6.5710,3.3670
Airport (MMIA)|6.5770,3.3210;6.5850,3.3100
Ikeja Along-Cantonment|6.6040,3.3250;6.5850,3.3400
Agege-Pen Cinema|6.6250,3.3200
Orile Agege-Dopemu|6.6120,3.3100
Ifako-Ijaiye-Iju|6.6450,3.3250;6.6600,3.3300
Abule Egba-Ojokoro|6.6440,3.3030;6.6600,3.3000
""".strip()
def load():
    out=[]
    for l in SEEDS.splitlines():
        nm,pts=l.split('|'); out.append((nm,[tuple(map(float,p.split(','))) for p in pts.split(';')]))
    return out
