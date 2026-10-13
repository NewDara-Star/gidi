# Gidi data plan: everything we need to build accurate districts (v1, 13 Oct 2026)

**Rule:** we study real Lagos to learn its patterns, then build our own world. Nothing real is traced or shipped.

## Blockers right now
- **My workspace is blocked from the internet.** Every open-data server tested on 13 Oct was rejected by the organization's network policy: Mapillary, Google Open Buildings bucket, WorldPop, GHSL, Copernicus DEM, ESA WorldCover, Wikimedia, NASA night lights, DHS. Web search and page reading still work.
- **The link to Daramola's computer was offline.**
- **Fix (pick one):**
  - **A. Allow the domains.** Daramola is the organization owner. In Admin settings → Capabilities → network access, allow these domains:
    - `graph.mapillary.com`, `*.mapillary.com`
    - `storage.googleapis.com`
    - `data.worldpop.org`
    - `jeodpp.jrc.ec.europa.eu`
    - `copernicus-dem-30m.s3.amazonaws.com`
    - `esa-worldcover.s3.eu-central-1.amazonaws.com`
    - `upload.wikimedia.org`, `commons.wikimedia.org`
    - `eogdata.mines.edu`
    - `data.humdata.org`
  - **B. Keep the computer linked.** Leave the Claude desktop app open and linked to this task, so I can download on his computer instead.
  - **C. Download by hand.** Daramola downloads the files and drops them in the chat.

## Google Maps / Earth / Street View
- **Allowed:** Daramola can look at them with his own eyes for feel.
- **Not allowed:** we cannot use them as data.
  - Google's Map Tiles terms forbid tracing or deriving models from Photorealistic 3D Tiles.
  - They also forbid "image analysis", "machine interpretation", geodata extraction, caching and offline use.
  - So no screenshots of Google 3D or Street View go into the generator or to me for measuring.
- **Google Open Buildings 2.5D is the exception.** It is a separate research dataset under CC-BY 4.0 / ODbL, and it is allowed.

## Data list (what, why, source, licence)
| Need | Why | Source | Licence | Status |
|---|---|---|---|---|
| Street network, footprints, land use, rail, drains | Town plan | OpenStreetMap (have it) | ODbL | Done for the Maze |
| **Building heights / storeys** | How tall each district is | Google Open Buildings 2.5D Temporal: height 0–100 m, 4 m effective resolution, 2016–2023 | CC-BY 4.0 or ODbL | Blocked: needs A/B/C |
| Ground height, slopes, flood-low areas | Topology, flooding | Copernicus DEM 30 m | Free, attribution | Blocked |
| Trees, bare ground, water, built-up | Greenery per district (answers "no trees in Mushin") | ESA WorldCover 10 m | CC-BY 4.0 | Blocked |
| Population per 100 m | Crowd and traffic density per district | WorldPop | CC-BY 4.0 | Blocked |
| Wealth proxy | Rich vs poor areas → cars, shops, police | VIIRS night lights (free account), building size, landuse, our LGA research | Free | Blocked |
| Street-level photos | Facades, signs, roofs, wires, how streets look | Mapillary (free API token), Wikimedia Commons | CC-BY-SA | Blocked; needs a token too |
| Daramola's own / family photos | Most accurate | Phone shots in Lagos (shot list below) | Ours | Ask family |
| Traffic mix | What drives where | Published Lagos traffic studies (below) | Facts only | Have it |
| Way of life, times of day, markets, religion, events | City simulation | LGA research doc + Daramola's memory | — | Partly done |

**Keys:** never paste keys in chat. The Mapillary token goes into an environment secret.

**Non-commercial data:** Meta's Relative Wealth Index is CC-BY-NC, so we skip it for a commercial game.

## Research findings so far (13 Oct)
### Storeys and street fronts
- **Storeys:** face-me-I-face-you tenements are typically 1–2 storeys (Bloomberg CityLab, 2022).
  - Rooms open onto a central corridor, with kitchens and toilets in a separate block behind.
  - This matches what OSM shows: deep houses with back buildings.
- **How common they are:** one Guardian Nigeria piece puts tenements at 35–45% of the urban housing stock nationally. It gives no source, so treat it as indicative. It also lists 3-bed bungalows at 15–20%, storey buildings/duplexes at 8–12%, and estates under 5%. Lagos is named as tenement-dominant.
- **Working assumption for the Maze**, until the height data or photos settle it:
  - mostly 1–2 storeys
  - some 3–4 storey newer blocks along main roads
  - a few unfinished frames
- **Not found in any source:** what share of street fronts are shops. We need photos or Daramola's memory.

### Population
- Mushin had 1,321,517 people in the 2006 census and a projected ~1.99 m in 2019 (citypopulation.de).
- The OSM boundary is 17.9 km². That gives about 74,000 people per km² in 2006 and roughly 110,000 per km² by projection.
- Lagos census figures are disputed, so use these for ranking districts, not as exact counts.

### Vehicles
- **Measured traffic mix** (Scientific African, 2023):

  | Road type | Cars | Minibuses (danfo) | Trucks | Motorcycles | Tricycles | Large buses |
  |---|---|---|---|---|---|---|
  | Two-lane collector | 57% | 32% | 2% | 3.5% | 4.5% | 1.5% |
  | Arterial | 35% | 27% | 18% | 10% | not measured | 10% |

- **Fleet:** for years Toyota has dominated. The Corolla was the best seller (≥12% of new sales), then Hilux, Camry and Hiace, then Kia, Hyundai and Honda; Pajero, Prado, Sienna and 4Runner are also common. Sales data is old (2011) and the used ("tokunbo") market isn't counted, so treat this as flavour, not numbers.
- **Plan:** invented brands in wealth tiers. Districts get a tier mix:
  - **Heights / Estate:** big SUVs, luxury saloons, drivers.
  - **Capital:** mid saloons, official cars.
  - **Maze / Jungle / Hub:** old saloons, danfo, keke, okada, trucks on the arterials.
  - **Port:** tankers and container trucks.
- Exact tier shares are our design choice, set by the wealth proxy.


## Building heights by LGA (Google Open Buildings 2.5D, 2023; measured 13 Oct)
- **Method:** pixels read at ~4 m. Built = presence ≥ 0.5. Storeys ≈ 3 m each. The 4.5–7.5 m band mixes tall pitched-roof bungalows with 2-storey houses.
- **Built-up share is low where an LGA includes lagoon water**, e.g. Lagos Island and Eti-Osa.
- **Epe and Ibeju-Lekki are only partly covered** until the eastern tiles are downloaded.
- **Script and results:** `Real-world/research/data/results/heights.py` and `heights_by_lga.json`.

| LGA | Mean height (m) | Under 4.5 m | 4.5–7.5 m | 7.5–10.5 m (3) | 10.5 m+ (4+) |
|---|---|---|---|---|---|
| Lagos Island | 8.8 | 11% | 51% | 21% | 17% |
| Ikeja | 7.3 | 18% | 48% | 19% | 15% |
| Apapa | 7.2 | 26% | 45% | 16% | 13% |
| Mushin | 6.8 | 19% | 53% | 15% | 12% |
| Surulere | 6.6 | 20% | 57% | 14% | 8% |
| Lagos Mainland | 6.6 | 20% | 55% | 16% | 9% |
| Eti-Osa | 6.3 | 31% | 50% | 13% | 6% |
| Oshodi/Isolo | 6.0 | 24% | 58% | 13% | 5% |
| Amuwo Odofin | 6.0 | 34% | 45% | 13% | 8% |
| Ajeromi/Ifelodun | 5.8 | 26% | 61% | 11% | 3% |
| Shomolu | 5.8 | 25% | 62% | 10% | 3% |
| Kosofe | 5.6 | 28% | 60% | 10% | 2% |
| Agege | 5.5 | 28% | 64% | 7% | 2% |
| Ifako-Ijaiye | 5.4 | 33% | 57% | 8% | 2% |
| Alimosho | 4.8 | 46% | 50% | 4% | 1% |
| Ojo | 4.7 | 54% | 41% | 4% | 1% |
| Ibeju-Lekki* | 4.4 | 58% | 37% | 4% | 1% |
| Ikorodu | 4.3 | 64% | 32% | 2% | 2% |
| Badagry | 3.7 | 79% | 20% | 1% | 0% |
| Epe* | 3.7 | 79% | 19% | 1% | 0% |

\* Only partly covered so far.

- **What it means for Gidi:**
  - The whole mainland core is low: 1–2 storeys dominate.
  - The Maze: mostly 1–2 storeys, about 15% 3-storey and about 12% 4+ along the main roads.
  - Old Island and the Capital are the tallest districts.
  - Railside, Bazaar, Old Shore and Border are bungalow country.
  - Heights at Eti-Osa read lower than expected. At 4 m the towers are blurred and much of the land is sand or new estates, so the Heights district needs a closer per-neighbourhood look (Ikoyi, VI, Banana Island).


## Per Gidi district: people, trees, built-up, height, low ground (measured 13 Oct)
- **Sources:** WorldPop 2020 constrained (people per km² of land); ESA WorldCover 2021 (tree and built-up share of land); Open Buildings 2.5D 2023 (heights); Copernicus DSM 30 m (share of the area below 5 m).
- **Districts** are weighted averages of their inspiration LGAs.
- **Caveat on low ground:** the DSM includes rooftops and treetops, and LGA polygons include lagoon water. So "below 5 m" over-counts water-heavy LGAs. Use it to rank districts, not as exact numbers.
- **Files:** `Real-world/research/data/results/lga_table.json` (per LGA), plus the scripts `heights.py` and `landpop.py`.

| District | People/km² | Trees | Built-up | Mean height | 1 storey / 1–2 / 3 / 4+ | Below 5 m |
|---|---|---|---|---|---|---|
| Maze | 26,155 | 3% | 95% | 6.3 m | 22 / 57 / 13 / 7 | 50% |
| Hub | 24,035 | 3% | 93% | 6.2 m | 23 / 58 / 13 / 6 | 66% |
| Railside | 13,596 | 12% | 84% | 4.9 m | 43 / 52 / 5 / 0 | 52% |
| Water Town | 12,796 | 7% | 58% | 5.7 m | 27 / 59 / 11 / 2 | 84% |
| Food Gate | 12,422 | 7% | 53% | 5.6 m | 28 / 60 / 10 / 1 | 84% |
| Estate | 11,670 | 8% | 66% | 6.3 m | 24 / 55 / 14 / 7 | 70% |
| Capital | 10,581 | 9% | 83% | 7.3 m | 18 / 48 / 19 / 15 | 50% |
| Jungle City | 9,723 | 12% | 51% | 6.0 m | 33 / 47 / 13 / 7 | 85% |
| Old Island | 9,090 | 0.4% | 82% | 8.8 m | 11 / 51 / 21 / 17 | 99% |
| Port | 8,843 | 5% | 79% | 7.2 m | 26 / 45 / 16 / 13 | 89% |
| Bazaar | 5,254 | 31% | 39% | 4.7 m | 54 / 41 / 4 / 1 | 77% |
| Heights | 2,338 | 11% | 59% | 6.3 m | 31 / 50 / 13 / 6 | 87% |
| Old Shore | 751 | 60% | 17% | 4.3 m | 67 / 28 / 3 / 3 | 66% |
| Border | 682 | 44% | 17% | 3.7 m | 79 / 20 / 1 / 0 | 71% |
| Frontier | 326 | 54% | 11% | 5.0 m | 56 / 34 / 5 / 6 | 76% |

- **Jungle City is diluted** by Amuwo Odofin. Ajeromi-Ifelodun (Ajegunle) alone is the densest place in Lagos: 44,239 people/km².
- **Water Town and Estate** both borrow from Kosofe, so their numbers overlap.

### Terrain (median surface height by LGA)
- **The north is a gentle ridge:** Ifako-Ijaiye 49 m, Agege 43 m, Ikeja 33 m, Alimosho 24 m.
- **The middle steps down:** Mushin 20 m, Ikorodu 15 m, Oshodi 13 m, Shomolu 9 m.
- **The lagoon edge is flat and low:** Surulere 6 m, Ajegunle 5 m, Apapa 3 m, Lagos Mainland 3 m, Kosofe 3 m, Eti-Osa 3 m, and Lagos Island near 0.

**For Gidi:** the land should rise gently, about 50 m over the city, from the lagoon and coast up to the north (Railside and the Capital highest). The flood-prone flats are Old Island, Port, Jungle City, Water Town and the Heights. Rain floods should hit there first.

## Photo shot list (for family/friends in Lagos, phone is fine)
For each area: Mushin/Shomolu, Ajegunle, Oshodi, Agege, Ikeja GRA, Lagos Island, Makoko, VI/Ikoyi, Lekki.
1. A residential street, standing in the middle, both directions.
2. One house front, straight on; one corner.
3. A compound's inner yard, if they're welcome.
4. A main road with traffic at morning rush and in the evening.
5. A market lane.
6. Roofs from any high point.
7. Drains and canals, bus stops, a motor park.
8. A church and a mosque from the street (outside only).
9. Shop signs and kiosks (we only take the style; names stay invented).
10. Night street with generators and lights.

Rules for the photos:
- Location on, so we can file each photo by area.
- No faces needed.

## Next steps once data flows
1. Heights + land cover + DEM + WorldPop for all 20 LGAs → one table per district: storeys, tree cover, slope, people per km², wealth tier.
2. Feed storeys into the generator and the 3D model.
3. Vehicle tier mix per district.
4. Repeat the pattern study district by district, using the Maze method.

## Sources
- Google Open Buildings 2.5D Temporal: https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1
- Map Tiles API policies: https://developers.google.com/maps/documentation/tile/policies
- Face-me-I-face-you design (Bloomberg): https://www.bloomberg.com/news/features/2022-05-05/the-history-and-design-of-lagos-face-me-i-face-you-homes
- Housing types (Guardian Nigeria): https://guardian.ng/nigerian/what-kind-of-house-do-most-nigerians-live-in/
- Mushin population: https://citypopulation.de/en/nigeria/metrolagos/NGA025016__mushin/
- Lagos traffic composition (Scientific African 2023): https://doaj.org/article/d45bd7e68c2c4ddfa9eb962ca1090503
- Nigerian car market 2010: https://bestsellingcarsblog.com/2011/11/nigeria-2010-corolla-king-of-the-roads/
