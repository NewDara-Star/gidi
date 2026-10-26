# What is to be modelled

WRITTEN by `scripts/model_inventory.py --write` (do not edit by hand): every record type the kit draws and every kind
of it on the map, its gidi-game builder, and whether the Unreal street test places it. Owner, 26 Oct: models work first,
look passes later (DECISIONS "Working first, polish later"). "Built" means the kind is named in its builder; it says
nothing of how it looks. "In Unreal" is the street test (gidi-game tools/street_test.py), not yet the whole city.

Kinds on the map now: builder lacks the kind: 1; built, Unreal has a stand-in: 1; built, not placed in Unreal: 13; no builder: 7; working: 18.

| record | kind | on the map | builder | in Unreal | state |
|---|---|---|---|---|---|
| building | compound_house | 1941 | block_build | yes | working |
| building | shop_under_flats | 810 | block_build | yes | working |
| building | face_me_bungalow | 768 | block_build | yes | working |
| building | walkup | 353 | block_build | yes | working |
| building | shack | 285 | block_build | yes | working |
| building | kiosk_row | 87 | block_build | yes | working |
| building | shed | 31 | block_build | yes | working |
| furniture | drum | 40 | furniture_build | no | built, not placed in Unreal |
| furniture | tyre_stack | 20 | furniture_build | no | built, not placed in Unreal |
| furniture | water_tank | 14 | furniture_build | no | built, not placed in Unreal |
| furniture | bench | 10 | furniture_build | no | built, not placed in Unreal |
| furniture | generator | 1 | furniture_build | no | built, not placed in Unreal |
| heap | rubbish | 12 | - | no | no builder |
| mast | lattice | 15 | - | no | no builder |
| pole | concrete | 579 | pole_build | yes | working |
| rail | main_line | 1 | - | no | no builder |
| road | lane | 278 | road_build | no | built, not placed in Unreal |
| road | home_street | 31 | road_build | no | built, not placed in Unreal |
| road | local_main | 15 | road_build | no | built, not placed in Unreal |
| road | service_road | 11 | road_build | no | built, not placed in Unreal |
| road | main_road | 10 | road_build | no | built, not placed in Unreal |
| road | market_street | 8 | road_build | no | built, not placed in Unreal |
| road | motorway | 5 | road_build | no | built, not placed in Unreal |
| road | trunk | 1 | road_build | no | built, not placed in Unreal |
| stall | plank_stall | 465 | stall_build | yes | working |
| stall | kiosk | 153 | stall_build | yes | working |
| stall | umbrella | 105 | umbrella_build | yes | working |
| stall | container_shop | 3 | stall_build | no | builder has no 'container_shop' |
| station |  | 1 | - | no | no builder |
| tree | shade | 56 | - | no | no builder |
| tree | palm | 36 | - | no | no builder |
| vehicle | saloon | 601 | saloon_build | yes | working |
| vehicle | danfo | 73 | danfo_build | yes | working |
| vehicle | okada | 58 | hand model (Art/Vehicles/Okada) | yes | working |
| vehicle | keke | 54 | keke_build | yes | working |
| vehicle | lorry | 14 | lorry_build | yes | working |
| vehicle | bus | 11 | molue_build | yes | working |
| vehicle | pickup | 7 | pickup_build | stand-in (City Sample) | built, Unreal has a stand-in |
| vehicle | suv | 6 | - | stand-in (City Sample) | no builder |
| wire | line | 360 | pole_build | yes | working |
| faces |  | 0 | block_build | yes | working |
| frontage |  | 0 | - | no | no builder |
| goods |  | 0 | furniture_build, loose_build, stall_build | yes | working |
| ground |  | 0 | - | no | no builder |
| ground_marks |  | 0 | - | no | no builder |
| gutter_pieces |  | 0 | - | no | no builder |
| leanto |  | 0 | leanto_build | no | built, not placed in Unreal |
| litter |  | 0 | loose_build, road_build | no | built, not placed in Unreal |
| people |  | 0 | person_build | no | built, not placed in Unreal |
| posters |  | 0 | pole_build, stall_build, wall_build | yes | working |
| relief |  | 0 | - | no | no builder |
| roof_sheets |  | 0 | block_build, leanto_build | yes | working |
| wall |  | 0 | wall_build | no | built, not placed in Unreal |
| wall_bays |  | 0 | - | no | no builder |

Record types with 0 on the map are not drawn in any district yet (the dress layer: faces, roof sheets, goods,
posters, litter, people and the rest); their builders are listed so the gap is seen before they are drawn.
