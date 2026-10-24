# The Lagos research: what we know, and which new districts it serves

Everything gidi holds about real Lagos, in one place. Most of it was written for the old map (13-21 Oct), but what it
measured is real Lagos, so it still holds for the new map (real Lagos at 1:3). Only its Gidi parts are history: the old
district names, the generator settings, the "Gidi against real" columns. Read the real numbers; skip the old-map parts.
New districts are named by number and real place (`docs/lagos-study/roads/NAMES.md` has the echo names).

## The new map's own study (22-24 Oct)

| File | What |
|---|---|
| `docs/lagos-study/STUDY.md` | how the whole Lagos map works, before cutting districts |
| `docs/lagos-study/councils.md` | the 20 LGAs and 37 LCDAs |
| `docs/lagos-study/roads/` | the real road skeleton at 1:3 (ROADS), the border checks (EARTH-CHECK), the echo names (NAMES) |
| `docs/lagos-study/similar/` | which places are alike (the first cut, replaced by "Roads first"; the Google checks still hold) |
| `docs/lagos-study/LIVING.md` | living in each of the 51 districts: people, wealth, work, vehicles, the day |

## Measured places (13-16 Oct): fabric numbers for the new districts

Two kinds of study per place, named by the old district's id. The **pattern study** (in `docs/`, for example
`docs/maze-pattern-study.md`) measured streets and buildings
from OpenStreetMap: street density, grid order, junction kinds, block sizes, building sizes, orientation, gaps, front and
back rows. OSM misses many buildings in Lagos, so its building counts are floors. The **deep study**
(in `docs/studies/`, numbers in `docs/data/deep/`, method in `docs/DEEP-STUDY.md`) measured the same
places from Google Open Buildings, Microsoft, Overture, WorldCover, WorldPop and Copernicus: buildings, heights, land cover,
ground, water, places.

| Real place studied | Pattern study | Deep study | New districts it serves |
|---|---|---|---|
| Mushin, Shomolu | `maze-pattern-study.md` | `studies/maze.md` | 15 Mushin, 27 Shomolu-Bariga |
| Oshodi, Isolo, Surulere | `hub-pattern-study.md` | `studies/hub.md` | 32 Oshodi-Mafoluku, 30 Isolo-Ladipo, 13 Surulere, 14 Itire |
| Ajegunle, Festac | `jungle-pattern-study.md` | `studies/jungle.md` | 9 Ajegunle, 5 Festac |
| Ojota, Ketu, Mile 12 (Kosofe) | `foodgate-pattern-study.md` | `studies/foodgate.md` | 38 Ketu-Mile 12 |
| Makoko-Iwaya, Bariga waterfront | `watertown-pattern-study.md` | `studies/watertown.md` | 19 Makoko, 27 Shomolu-Bariga |
| central Ikeja | `capital-pattern-study.md` | `studies/capital.md` | 35 Computer Village-Allen-Maryland, 36 Alausa-Oregun-Ogba |
| Ojo, round the electronics market | `bazaar-pattern-study.md` | `studies/bazaar.md` | 3 Alaba-Ojo-Trade Fair |
| Apapa | `port-pattern-study.md` | `studies/port.md` | 10 Apapa, 8 Kirikiri-Tin Can |
| Agege, Ifako-Ijaiye, Alimosho | `railside-pattern-study.md` | `studies/railside.md` | 37 Agege-Ifako-Ijaiye, 40-43 |
| Ikeja GRA, Magodo, Omole | `estate-pattern-study.md` | `studies/estate.md` | 34 Ikeja GRA, 39 Magodo-Omole-Berger |
| Lagos Island | `oldisland-pattern-study.md` | `studies/oldisland.md` | 20 Lagos Island |
| Ikoyi, Victoria Island, Banana Island | `heights-pattern-study.md` | `studies/heights.md` | 21 Ikoyi, 22 Victoria Island |
| the Lekki peninsula | `frontier-pattern-study.md` | `studies/frontier.md` | 23-26 Lekki to Sangotedo |
| Badagry (its eastern strip) | `border-pattern-study.md` | `studies/border.md` | 1 Agbara-Morogbo, 2 Okokomaiko |
| old Ikorodu | `oldshore-pattern-study.md` | `studies/oldshore.md` | 47 Ikorodu Town, 48-51 |
| the airport | | `studies/airport.md` | 33 Airport |
| Yaba, Akoka | | `studies/yaba.md` | 17 Yaba, 18 UNILAG |

## How Lagos looks and lives

| File | What |
|---|---|
| [buildings](look/research-buildings.md), [civic](look/research-civic.md), [commerce](look/research-commerce.md), [housing](look/research-housing.md), [landmarks](look/research-landmarks.md), [leisure](look/research-leisure.md), [religious](look/research-religious.md), [roads](look/research-roads.md), [street](look/research-street.md), [transport](look/research-transport.md), [vehicles](look/research-vehicles.md) | the look catalogues in `docs/look/` (written for the old kit; the things they list are real) |
| `docs/LAGOS-ISMS.md` | the eccentricities in the real data, a running log |
| `docs/LAGOS-LIGHT.md` | why Lagos looks different: haze, sun, dust |
| `docs/research/LIFE-IN-LAGOS.md` | what it is like to live there |
| `docs/lagos-lgas-research.md` | one local government at a time |
| `docs/gidi-data-plan.md` | building heights by LGA (storey bands), people, trees and ground by LGA, 13 Oct; its "blockers" no longer hold. The numbers are in `data/results/lga_table.json` |
| `docs/hand/maze-hub-lagos.md` | what makes Mushin, Shomolu and Oshodi unmistakably Lagos (agreed with the owner 16 Oct, written with the old district names) |
| `docs/hand/borrowed-lagos.md` | 30 real Lagos landmarks and the Gidi versions planned for them (old district names; The Reach now goes with Festac) |
| `docs/hand/monument-briefs.md` | what each monument needs (parked) |
| `docs/OLD-MAP-LESSONS.md` | what the old map's passes taught that still holds |
| `decisions/world-life.md`, `decisions/lived-in.md` | Gidi's life: rhythm, systems, moments; the GTA research and the lived-in plan |

Outside the repo, in `~/gidi-data/research/`: the Google study shots per district, the kit tests (`google/kits/`), the
reference pictures (`refs/`), the look-target clips (`games/`).
