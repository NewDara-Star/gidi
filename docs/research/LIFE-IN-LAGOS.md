# Life in Lagos: what it's like to live there

A research pass, 16 Oct 2026, for the owner's ask: "immerse yourself in what it's like to live in Lagos".

`docs/LAGOS-ISMS.md` covers the city's physical oddities (dead ends, gutters, buildings in the road). This one covers **the life**: how people get around, pay, eat, pray, party, fear, fight and get by.

Each section gives:
- **What's true:** facts, with the source and its date.
- **How it feels:** the lived texture.
- **For Gidi:** what the game can do with it.

**Rules that still hold:**
- Real names and places here are research only. Gidi invents its own (`decisions/DECISIONS.md`).
- Churches, mosques, schools, hospitals and clinics are never crime sites.
- Faith is life, never a joke.
- The game takes ideas from `decisions/world-life.md`.

**On sources:** many numbers come from news reports and blogs, some years old. They're marked with dates. Where sources disagree, both figures are given. Treat them as the right size, not as census figures.

---

## The one idea underneath everything: the city taxes you at every step, and everyone has a workaround

The state is weak where it matters every day: power, water, refuse, roads, transport. So Lagosians run their own versions:
- the generator for power
- the borehole and the pure-water sachet for water
- the cart pusher for refuse
- the danfo for transport
- the POS agent for cash
- the area boys, the vigilante and the mob for security

Every one of these has someone collecting a fee:
- the agbero at the bus stop
- the policeman's "roger" at the checkpoint
- the omo onile at the foundation of a new house
- the agent's commission on a flat
- the POS charge on your own money

**Living in Lagos is a running negotiation.** You're never just doing a thing. You're paying, persuading, waiting or dodging while you do it. That negotiation is the gameplay texture Gidi should be built on: small frictions, small fees, small favours, and talking your way through.

---

## 1. Moving around

**What's true:**
- **Traffic.** Lagosians lose about **four hours a day** to traffic, by a government estimate ([AllAfrica, Dec 2025](https://allafrica.com/stories/202512220348.html)). Before the BRT, a typical trip from the mainland to the Island took **two hours** ([World Bank](https://blogs.worldbank.org/en/transport/lagos-bus-rapid-transit-system-decongesting-and-depolluting-mega-cities-0)).
- **The BRT is a small share of trips.** LAMATA said in April 2026 that it carries about **100,000 passengers a day, roughly 1.5% of commuters**, and that the state needs about 15,000 high-capacity buses ([Gazette, Apr 2026](https://gazettengr.com/lagos-needs-15000-high-capacity-buses-to-meet-growing-population-demand-lamata/)). Another source says over 350,000 ([Think Global Health](https://www.thinkglobalhealth.org/article/learning-lagos)). Either way, the danfo is how Lagos moves.
- **Peak fares.** A danfo fare in the morning rush can be **many times** the mid-morning fare ([Think Global Health](https://www.thinkglobalhealth.org/article/learning-lagos)). Fares on busy routes more than double in December. Regulated bus fares went up 13% in March 2026 ([Holafly](https://esim.holafly.com/finance/cost-of-living-nigeria/)).
- **Okada and keke bans.** Since 2020 they're banned in six local governments, nine LCDAs and ten highways, and the ban keeps growing. The task force seizes them by the hundred: **668 in one week** in August 2025, when a mob attacked the officials ([Nairametrics, Aug 2025](https://nairametrics.com/2025/08/18/lagos-impounds-668-okada-in-one-week-as-mob-attacks-government-officials/)), and 65 in Ikoyi in February 2026 ([AllAfrica, Feb 2026](https://allafrica.com/stories/202602030077.html)). Seized bikes are forfeited through the courts.
- **Bus stop names** come from landmarks: churches, trades, old buildings, crafts, farmland. They mix Yoruba and English. Conductors clip them when they shout ("Oshod! Iyanoworo Oshod!"), and keep using the old name after a stop is renamed ([Obiorah 2021](https://arbitrer.fib.unand.ac.id/index.php/arbitrer/article/view/272); [WATHI](https://wathi.org/initiative-lagos/contributions-initiatives-lagos/danfo-tales-in-the-big-city); [Legit](https://www.legit.ng/entertainment/celebrities/1666555-charly-boy-wa-o-danfo-conductor-calls-baddo-bus-stop-by-man-questions-video/)).

**How it feels:**
- You leave home at 5:30 to beat traffic and still meet it.
- The conductor hangs out of the door shouting the route. The fare changes with the time and the rain.
- "Owa o!" means there's space. "Wole!" means get in fast. "Shift!" means four on a bench for three.
- "Conductor, my change!" is a fight with no end. He has no change, and you'll get it "at the next bus stop".
- In go-slow, the city comes to your window: hawkers, beggars, phone sellers, preachers, newspaper boys.
- Okadas squeeze through gaps no car can, until a task force van appears and everyone scatters.

**For Gidi:**
- Danfo fares go up with the rush, the rain and December.
- Conductors chant real route strings of invented stops.
- The change argument is a dialogue moment.
- Okada zones are already in the data (`okada_ban`). Task force raids clear a street in seconds, and they're a chase.
- Go-slow is a place, not a delay: a moving market with its own sellers and scams.

---

## 2. A roof over your head

**What's true:**
- **The law caps advance rent at one year for new tenants,** but it's rarely enforced. Landlords still ask for **two years upfront** ([Ownkey 2026](https://ownkey.com/ng/blog/renting-in-lagos); [OAL](https://oal.law/?p=1012545)).
- **On top of the rent:** the custom is **10% agency fee plus 10% "legal" or "agreement" fee**. Earlier caps of 5% (2015, 2022) were ignored. A 2025–26 bill would cap commission at 5%; in May 2026 it was still at committee stage ([Ownkey](https://ownkey.com/ng/blog/real-estate-agent-commission-fees-nigeria-who-pays); [BrandSpur](https://brandspurng.com/?p=200487)). Moving in can cost **3–4 years of monthly rent at once**.
- **The state has condemned** landlords' rent hikes and "extortionate" agency fees ([Gazette, Jul 2026](https://gazettengr.com/sanwo-olu-govt-condemns-lagos-landlords-indiscriminate-rent-hike-extortionate-agency-fee/)). Agents' illegal commissions shut young people out ([Guardian](https://guardian.ng/features/how-agents-shut-young-people-out-of-affordable-housing-in-lagos-with-illegal-commissions/)).
- **Building a house:** the **omo onile** ("sons of the soil") charge developers at each stage: fencing, foundation, roofing, and more recently plastering and wiring. One reported foundation fee was **₦500,000**, haggled down, with work stopped until it was paid. They have stopped sites, seized tools, and hurt people. A 2016 law sets 5–21 years for land theft; three years later "no significant improvement" ([BusinessDay](https://businessday.ng/real-estate/article/property-protection-law-land-grabbing-yet-to-see-improvement-3yrs-after/); [Guardian](https://guardian.ng/property/land-grabbers-resurgence-in-lagos-threatens-homeownership/)).

**How it feels:**
- The face-me-I-face-you: one room, a corridor, the whole family's life through the wall, and one toilet for ten rooms with a queue at dawn.
- The landlord lives on the ground floor and has rules: no visitors after 10, gate locked at 11, light bill shared by the room, quarrels over who used the pumping machine.
- The agent shows you the flat, wants "inspection fee", then disappears.
- The wall says "THIS HOUSE IS NOT FOR SALE. BEWARE OF 419" because someone tried to sell it twice.
- Half-built houses with rebar sticking out are slow savings in concrete, and the omo onile have been paid at every stage.

**For Gidi:**
- Tunde's room costs a year upfront, and the rent is a story pressure. The landlord is a character.
- Buying property after the story means the agent, the "legal fee", and the omo onile at the foundation: a living fee system, and a mission line.
- Houses not for sale, and houses for sale twice.
- Half-built houses everywhere (the kit has the unfinished house).

---

## 3. Power: "NEPA has taken light"

**What's true:**
- **Band A** is the top tier, promised at least **20 hours a day**, and still misses. Ikeja Electric apologised on 2 Oct 2026 for five Band A feeders missing it. One Oshodi feeder gave **no power at all** on 30 Sept ([Legit, Oct 2026](https://www.legit.ng/business-economy/energy/1734220-apologise-ikeja-electric-issues-fresh-notice-band-a-customers-power-supply-shortfall/)).
- **Akoka and Shomolu** went days without power in mid-September 2026 under load-shedding ([Gazette, Sep 2026](https://gazettengr.com/?p=501812)).
- **Planned grid works** cut power 8 am–5 pm daily for about three weeks in 2025 ([Prime Business](https://www.primebusiness.africa/?p=232877)).
- **The Band A tariff** jumped to around ₦206–225/kWh in 2024–25 from about ₦68 ([Arise](https://arise.tv/electricity-union-threatens-power-outage-across-nigeria-in-protest-of-tariff-hike/amp)). The exact current figure needs NERC's own order.
- **Water depends on power too:** "We can't pump water from our boreholes because there is no light" ([NERC NORA / BGS](https://earthwise.bgs.ac.uk/index.php/Case_Study_Use_Perceptions_Groundwater_Lagos)).

**How it feels:**
- The light goes and a groan goes up from the whole street. Then, one by one, generators start: the "I better pass my neighbour" small one, the diesel big one at the shop.
- The air fills with fumes and noise.
- When light comes back, children shout "UP NEPA!" and everyone rushes to charge phones, iron clothes and pump water.
- People with solar or inverters are quietly envied.
- Nobody says "the power company". It's still "NEPA", decades after the name changed.

**For Gidi:**
- Power is a city system, the strongest single immersion lever on this list. Each district or feeder has a schedule, and blackouts roll across the map.
- When the light goes: street lights die, the generators' sound and glow take over, and shops without generators close. The radio reports it.
- "UP NEPA!" when it returns.
- Gameplay: darkness helps or hurts, fuel for the generator is a cost, and a transformer is a target or a mission. The Maze already has "Transformer 44".

---

## 4. Water and refuse

**What's true:**
- **Water.** In a 2019 survey of 500 households, **68% use a private borehole daily**. **95% drink sachet or bottled water at least weekly**. Only **33% use piped public water daily**. Even borehole owners mostly drink packaged water ([BGS case study](https://earthwise.bgs.ac.uk/index.php/Case_Study_Use_Perceptions_Groundwater_Lagos); [IAEA/INIS](https://inis.iaea.org/records/p06av-sd235)). A third of boreholes and over 80% of shallow wells showed unsafe E. coli. Sachet water quality varies widely ([ICIR](https://www.icirnigeria.org/investigation-bacteria-acids-odour-the-pure-water-you-drink-is-filled-with-impurities/)). In July 2026, residents bought water from community boreholes because compound water came out "mixed with soil" ([Gazette](https://gazettengr.com/lagos-residents-lament-poor-public-water-supply-seek-alternatives/)).
- **Refuse.** Collection is meant to be by licensed PSP operators, who often don't come weekly, sometimes not for a month, and still bill. So residents pay **cart pushers ₦200–500** a load, and the cart pushers dump in canals and on road verges. LAWMA arrests them and seizes their tricycles ([Guardian](https://guardian.ng/sunday-magazine/cityfile/pesidents-lament-lawma-psps-poor-operation-as-cart-pushers-become-alternative/); [ICIR](https://www.icirnigeria.org/lagos-state-govt-clamps-down-on-cart-pushers/); [Gazette, Jul 2026](https://gazettengr.com/lawma-arrests-cart-pushers-over-illegal-waste-disposal-along-lagos-badagry-expressway/)). LAWMA says it clears 3,000 "black spots" a day.

**How it feels:**
- "Pure water! Pure water!": the sachet you bite open at the corner, the empty sachets in every gutter.
- The jerrycans lined up at the borehole tap. The pumping machine argument with the landlord.
- The cart pusher's bell, and the refuse heap by the canal that grows until someone burns it.

**For Gidi:**
- Pure-water hawkers are everywhere. Sachets litter the gutters (gutters are in the data).
- Jerrycan queues at boreholes.
- Refuse heaps at canal edges and black spots, smoke from burning heaps.
- Cart pushers as NPCs, and a LAWMA raid as a moment.

---

## 5. Money

**What's true:**
- **Prices (2026).** Petrol averaged **₦1,330 a litre** in May 2026, up from ₦1,245 in April. Food prices in Lagos markets rose with diesel and transport costs ([Nairametrics, May 2026](https://nairametrics.com/2026/05/27/food-prices-spike-in-may-as-sellers-pass-cost-to-lagosians/)). It hit ₦1,400 in places in July as crude passed $100 ([Guardian](https://guardian.ng/?p=2905790)).
- **Exchange rate:** about **₦1,350–1,500 to the dollar** ([Holafly](https://esim.holafly.com/finance/cost-of-living-nigeria/)).
- **Monthly budgets.** A single adult needs roughly ₦450,000–750,000 a month on the mainland and ₦0.8–1.6 million or more on the Island. Commuting costs ₦30,000–75,000 a month by public transport. **A buka meal costs ₦1,500–3,000** ([Nigeria Housing Market](https://www.nigeriahousingmarket.com/guides/cost-of-living-in-lagos); [Guardian](https://guardian.ng/?p=2905790)).
- **POS agents are the cash system,** because ATMs fail. There are millions of POS terminals against fewer than about 21,500 ATMs. **Withdrawing ₦5,000 costs about ₦200.** Agents crowd each other on a single street, many earn under minimum wage, and they queue at banks for float ([ThisDay, Feb 2026](https://www.thisdaylive.com/2026/02/01/the-rise-of-pos-agents-as-nigerias-new-cash-bank/); [TechEconomy](https://techeconomy.ng/200-for-5000-how-pos-charges-are-changing-everyday-transactions-in-nigeria)).
- **Fuel scarcity comes and goes.** Queues for hours, stations hoarding, jerrycan sellers by the roadside at double the pump price, four litres for ₦5,000 when patience runs out ([Guardian](https://guardian.ng/news/long-queues-traffic-snarl-ups-in-lagos-as-petrol-scarcity-persists/); [BusinessDay](https://businessday.ng/news/article/fuel-scarcity-back-again-as-black-market-sells-at-n900-litre/)).

**How it feels:**
- "Yesterday's price is not today's price." The bread you bought last week is smaller this week, at the same price.
- "Sapa" (being broke) is a daily character.
- Everyone does transfers: "send me your account number", "the network is bad, the transfer will reflect". The POS umbrella on every corner with its sign: "WITHDRAWAL / TRANSFER / AIRTIME".
- Haggling is normal. A fixed price is a sign you're in a mall.
- Everyone has a side hustle.

**For Gidi:**
- Naira at Lagos prices (`decisions/world-life.md`). Prices move with the city's state: fuel scarcity, December, inflation over the game's months.
- **POS stands** as the cash points, with a fee to withdraw. Pickpocketing a POS stand is a crime option, and a job.
- **Haggling** as a skill in markets.
- **Fuel queues** and **jerrycan sellers** when a scarcity event hits.
- Transfers and "it will reflect" as phone gameplay.

---

## 6. The people who collect: agberos, unions, police

**What's true:**
- **Agberos.** The word first meant a tout who loads passengers at a motor park. Now they stand at bus stops too and charge every danfo, keke and okada. Almost all are union (NURTW) members.
- **Their named levies:** "owo weekend", "owo loading", "owo olopa" (for the police), "owo task force", "owo organising", "owo traffic", "owo environmental".
- **The scale:** a driver pays an estimated **₦3,000 a day**, about **₦123 billion a year** in total ([Global Voices, 2022](https://globalvoices.org/2022/07/18/nigerias-lagos-gangs-terrorize-citizens-extort-transport-workers-and-wreak-havoc/); [Guardian](https://guardian.ng/news/nigeria/touts-untamed-monsters-that-rule-lagos-roads/)).
- **The rules don't stop them.** They were banned at parks and stops in 2012. The union was suspended in 2022, and the touts kept going "in mufti". A flat **₦800 daily levy** replaced the many fees, and the agberos still rule the roads ([Daily Trust](https://dailytrust.com/?p=1061710); [Guardian](https://guardian.ng/features/one-year-after-introducing-n800-daily-levy-agberos-still-rule-lagos-roads/)). Drivers say the union serves itself ([Al Jazeera, 2020](https://www.aljazeera.com/features/2020/10/14/thugs-cops-and-unions-the-trials-of-public-bus-drivers-in-lagos)).
- **Police checkpoints.** Officers ask keke riders for **₦200**, and a second shift comes in the afternoon. The Ikorodu–Epe road has **at least 14 checkpoints**. They're set on bends where traffic slows, which makes the gridlock worse ([Guardian](https://guardian.ng/?p=2067260); [Radio Nigeria](https://radionigerialagos.gov.ng/?p=29292); [Guardian opinion](https://guardian.ng/opinion/the-political-economy-of-lagos-police-checkpoints/)).
- **Traffic officers (LASTMA).** Drivers pay ₦5,000–10,000 to get an impounded bus back. Fake LASTMA officers in reflective jackets extort motorists too; one confessed to making **₦35,000 a day** ([Guardian](https://guardian.ng/news/bus-driver-alleges-extortion-by-lastma-officials/); [Prime Business](https://www.primebusiness.africa/?p=45312)).
- **Mob justice.** A "thief!" shout can end in a beating or a burning. Cases include two suspected phone thieves burned at a bus stop in 2022, two suspected POS robbers in Igando, and police rescuing a suspect from a mob in Surulere. It's illegal, and the police plead with crowds to hand suspects over ([Guardian](https://guardian.ng/news/scourge-of-jungle-justice/); [Gazette](https://gazettengr.com/two-pos-robbers-killed-in-jungle-justice-by-lagos-mob-police/)).

**How it feels:**
- The agbero slaps the side of the bus and the driver hands notes out of the window without stopping. Notes folded lengthways between the fingers.
- "Roger me" at the checkpoint: the hand on the window, the "anything for the boys?".
- Fear of the crowd as much as of the police: the city judges and punishes in seconds, which is why Tunde running with stolen bread is truly dangerous.

**For Gidi:**
- **Levies as a system.** Every danfo pays at every stop. When the player drives a danfo, the fees eat the profit.
- **Agberos are the Hub's power,** and the boss runs them. A union politics mission line.
- **Checkpoints:** pay, talk or run. Some officers are fake.
- **The crowd.** In Act 1's "Ole!" chase the crowd is the danger: the chase is a race to get away before the crowd closes. **Show its threat, not lynching.** Never depict burning; cut away. Handle with care.

---

## 7. Work and hustle

**What's true:**
- **Most work is informal:** trading, transport, artisans, hawking.
- **Street hawking is banned under a 2003 law.** Both buyer and seller can be fined (reports say ₦90,000 or six months). Enforcement is chases and seized goods. One woman died fleeing enforcement officers, and in the reprisal ten BRT buses were vandalised ([BusinessDay](https://businessday.ng/columnist/article/differentiating-between-area-boys-omoniles-street-hawkers/); [Gulf News/AFP](https://gulfnews.com/amp/story/world%2Fafrica%2Fno-hawking-no-trading-lagos-bans-street-selling-1.1869103)). A hawker's reply: she has no money to rent a shop.
- **Market associations rule the markets.** The Iyaloja-General heads the market women and men: disputes, rules, advocacy. Appointments are political; Computer Village traders protested having leaders imposed. Research on one market found "despotic and extortionist" governance where most women traders have no voice ([Wikipedia: Pelewura](https://en.wikipedia.org/wiki/Alimotu_Pelewura); [UEA, Oke Arin study](https://ueaeprints.uea.ac.uk/66836/); [The Nigeria Lawyer](https://thenigerialawyer.com/computer-village-protests-i-have-power-to-appoint-anyone-as-iyaloja-tinubu-ojo/)).
- **Betting.** In a 2025 study of undergraduates aged 18–24, 30% bet in the past year, and **nearly half of those who bet met problem-gambling criteria** ([World Lottery Association summary](https://publications.world-lotteries.org/reaching-emerging-adults/research/sports-betting-among-nigerian-undergraduates-daniel-et-al-2025)). A betting shop on every street, "where most of the unemployed youths spend their time" ([Substack, 2023](https://unusualsnewsletter.substack.com/p/the-relevance-of-betshops-in-the)). Virtual football in the shops since at least 2015 ([SBC News](https://sbcnews.co.uk/technology/2015/05/11/inspired-gaming-enters-nigeria-with-surebet247/)). Betting as "Nigeria's new side hustle" ([BusinessDay](https://businessday.ng/news/article/how-sports-betting-became-nigerias-new-side-hustle/)).
- **Leaving.** "Japa" (to flee, now to emigrate) is a whole national mood. "Japa", "agbero", "419" and others entered the Oxford English Dictionary in 2025 ([Prime Business](https://primebusiness.africa/agbero-yahoo-boy-japa-suya-16-other-nigerian-words-enter-oxford-english-dictionary)).

**How it feels:**
- Everybody sells something, and everybody knows someone who knows someone.
- The hawker runs when the task force comes and comes back in ten minutes.
- In the betting shop, men argue about Arsenal at 11 am with slips in their hands. One wins big, and the whole street hears about it.
- Young graduates do three hustles and still plan to japa.

**For Gidi:**
- The **hustle loop** after the story: hawking, POS, driving, trading.
- **Enforcement raids** as world events.
- **Market associations** as a power: the Maze's market has its own leader, and you need their blessing to trade there.
- **Bet Gidi** with fictional and virtual football, in-game money only (`decisions/world-life.md`).
- The **japa** mood in dialogue: everyone wants out, and a "japa" mission line is a natural ending option.

---

## 8. Faith

**What's true:**
- **Faith is everywhere and loud:** churches in converted flats and warehouses, mosques on every few streets, night vigils.
- **The state seals worship centres for noise.** 53 churches, mosques and hotels were shut in 2015. The limits are 55 dB by day and 45 dB at night in homes. Makeshift structures can't host vigils. More sealings in Dec 2023 and Sept 2025 ([Citi FM, 2015](https://citifmonline.com/2015/12/nigeria-shuts-down-53-churches-mosques-over-noise-pollution/); [LASEPA](https://lasepa.gov.ng/?p=88718); [Guardian](https://guardian.ng/?p=1066106)).

**How it feels:**
- The call to prayer at dawn, the vigil's drums and amplified tongues at 2 am through the wall. Crusade posters on every pole: "COME AND RECEIVE YOUR MIRACLE".
- Fridays the mosque streets fill; Sundays the roads near big churches jam with Sunday best.
- The bus preacher, the "God's time is the best" stickers, the danfo blessed by the pastor.
- People of both faiths in one family, at each other's weddings.

**For Gidi:**
- Faith as sound and rhythm: the call to prayer, vigils, Jumat, Sunday traffic.
- The bus preacher moment.
- Crusade posters and church signs as texture.
- Noise complaints and sealing as a world detail, never mockery.
- **Safe ground everywhere:** never crime sites, never targets.

---

## 9. Celebration

**What's true:**
- **Owambe:** lavish Yoruba parties for weddings, birthdays, funerals, chieftaincy titles.
  - **Aso-ebi** (matching cloth worn by family and friends) defines the look.
  - **Spraying money** on dancers is central, as thanks, support and status. It's been illegal since 2007 (six months or ₦50,000) and ignored for years, until a recent crackdown with arrests and convictions.
  - **Now guests drop notes into silver bowls,** or spray printed "portrait notes" ([NPR via WWNO, Aug 2025](https://www.wwno.org/2025-08-10/in-nigeria-the-government-is-cracking-down-on-money-spraying-at-festive-events); [eNCA](https://enca.com/opinion/crackdown-curbs-nigerias-festive-spraying-cash-culture); [Wikipedia](https://en.wikipedia.org/wiki/Owanbe)).
- **Detty December:** about **1.2 million visitors** in December 2024, 60% from within Nigeria. Diaspora returnees ("IJGB", "I just got back") drive the spending, over $220m in 2023. Concerts, VIP tickets ₦120,000–300,000 in 2025, bars at three times normal rates, fares more than double. In the 2023–24 downturn many Lagosians cut back while the parties went on ([AllAfrica, Dec 2025](https://allafrica.com/stories/202512220348.html); [Al Jazeera, 2024](https://www.aljazeera.com/features/2024/12/25/nigerias-celebratory-detty-december-turns-sombre-amid-economic-woes); [Radio Nigeria, 2025](https://radionigerialagos.gov.ng/?p=35594)).

**How it feels:**
- Saturdays a street is blocked with canopies and plastic chairs. The live band plays fuji or juju, the MC hails big men by name, and the jollof and small chops come round.
- Uninvited guests and "who sent you?"
- In December the whole city is louder, pricier, slower and happier.

**For Gidi:**
- **Saturday owambes** as world events: streets closed, the sound, guests in aso-ebi. Crash one for food, money or a contact.
- **Spraying,** and the bowl now that spraying is risky.
- **December:** the city full, prices up, the concerts, returnees as NPCs and marks.

---

## 10. Food

**What's true:**
- **Morning:** akara (bean fritters) with pap or Agege bread, and ewa agoyin (soft beans in pepper sauce) with bread.
- **Daytime:** boli (roast plantain) with groundnut, and the buka.
- **Night:** suya, and the northern **mai shai** stand: noodles, eggs, bread and tea, from late evening into the night ([OkayAfrica](https://www.okayafrica.com/heres-your-ultimate-guide-to-nigerian-street-food/232652); [Eat Drink Lagos](https://www.eatdrinklagos.com/roll-call/2019/9/17/5-street-foods-you-have-to-eat-in-nigeria-before-you-die)).
- **A buka meal costs ₦1,500–3,000** (section 5).

**How it feels:**
- Smoke from the boli grill at the junction.
- The suya man's lamp at night.
- The akara woman's pan before dawn.
- Bread in nylon on the hawker's head.
- "Mama, put meat."

**For Gidi:**
- **Food by time of day.** Morning akara and bread hawkers (Railside's bakery row), boli at junctions, bukas at noon, suya lamps and mai shai at night.
- **Smoke and lamps as light and VFX.**
- **Eating as health and story.** Tunde steals bread because he's hungry.

---

## 11. The calendar

- **The rains** (`to-delete/docs/LAGOS-LOOK.md` covers the look):
  - The rainy season runs April–October: early rains April–June, the peak July–September ([2026 flood guide](https://ejsdprogram.hedang.org/wp-content/uploads/2026/07/2026-FLOOD-GUIDE-FOR-LAGOS-STATE.pdf)).
  - Floods hit poor and rich areas alike: Ikorodu in Aug 2025, when residents were told to relocate, and Lekki ([Sahara Reporters, Aug 2025](https://saharareporters.com/2025/08/05/lagos-government-asks-residents-flood-prone-areas-relocate-ahead-heavy-downpour-flash)). In June 2026 roads were submerged across the city ([The Star/Xinhua, Jul 2026](https://www.thestar.com.my/news/world/2026/07/01/roundup-severe-flooding-cripples-nigeria039s-commercial-hub-lagos)).
- **Harmattan** (Dec–Feb): dust haze, cool mornings.
- **Sanitation Saturday** came back in **April 2026**: the last Saturday of the month, 6:30–8:30 am, **officially without movement restrictions** (a court struck them down in 2016). The first ones saw low turnout, and **arrests and extortion by officials and street urchins** in Mushin, Agege, Oshodi and Surulere ([Guardian](https://guardian.ng/news/nigeria/metro/mixed-reactions-as-monthly-sanitation-resumes-in-lagos-after-10-year-break/); [Channels, Mar 2026](https://www.channelstv.com/2026/03/19/environmental-sanitation-why-lagos-wont-restrict-movement-commissioner/)). That's a perfect Lagos detail: a civic duty with someone collecting on it.
- **December** (section 9).

**For Gidi:** weather and calendar events. The game's months carry the rains, the floods, harmattan, sanitation Saturdays and December.

---

## 12. How people talk

- **Pidgin with Yoruba,** fast and clipped, with transport and pop-culture metaphors ([Discover Lagos](https://www.discoverlagos.ng/post/the-language-of-lagos-understanding-pidgin-slang-and-the-local-lexicon)).
- **Greetings:** "How far?" (what's up), "How body?" (how are you).
- **Trouble:** "wahala" (trouble), "no wahala" (it's fine).
- **Money:** "sapa" (being broke): "sapa don catch me".
- **Leaving:** "japa" (to emigrate).
- **Parties and lies:** "gbedu" (a banger, a party), "lamba" (a lie, a smooth line) ([Wikipedia: Sapa](https://en.wikipedia.org/wiki/Sapa_(slang)); [Wikipedia: Japa](https://en.wikipedia.org/wiki/Japa_(slang))).
- **Words in the Oxford English Dictionary since 2025:** agbero, japa, 419, "abi", eba and others.
- **Respect is in the words:**
  - "Oga" and "madam" for strangers.
  - "Aunty" and "uncle" for elders.
  - "Mummy so-and-so" by your child's name.
  - Kneeling or prostrating to greet elders.

**For Gidi:**
- NPC barks in layers, switching languages mid-line.
- Respect forms in dialogue: Tunde says "sir" and "ma", and the boss is "Oga".
- Subtitles that keep the Pidgin and gloss it lightly, never translating it flat.

---

## What to build first (a recommendation)

The biggest return for the work, in this order:
1. **Power cuts** (section 3). One system changes light, sound, shops and gameplay across the whole city, and it's unmistakably Lagos.
2. **Bus stop names and conductor chants** (section 1). Cheap: it's names in the data and audio later. It makes the city *sound* right.
3. **Levies and checkpoints** (section 6). The "negotiation" texture, and it ties straight into the Hub's story.
4. **Food by time of day and the hawkers** (sections 7 and 10). They fill the streets with life in the hand pass.
5. **The calendar** (section 11): Saturdays, the rains, December.

---

## Gaps (for a later pass, or for the owner's Google Earth study on Saturday)

- **Generators and solar:** current shares by income. No good source was found.
- **Police:** life after the EndSARS protests (2020) and the mood now.
- **Schools and children:** the school run, uniforms, "lesson" (after-school tutoring).
- **Health:** chemists as the first doctor, hospital deposits before treatment.
- **Nollywood and music:** street culture, the CD sellers now gone, the streaming era.
- **Nightlife by district,** from the mainland beer parlour to the Island lounge.
- **The owner's own memories.** Nothing beats them. Every section here should be checked against "is that how it felt to you?".

Sources are linked in each section.
