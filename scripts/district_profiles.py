# Per-district settings for gen_fabric.py. Each number says where it comes from.
# A district with no profile gets the generator's original (v1) behaviour. The Maze got its own profile in v2; its edge roads
# and gateways in web/network.json are kept exactly ("keep_gateways"), because the Hub was built against them.
import json, os

def _lga_table():
    return json.load(open("data/results/lga_table.json"))

def height_bands(lgas):
    """Share of built area in each height band, weighted by each LGA's land area (Google Open Buildings 2.5D via lga_table.json).
    Bands (metres): 0-4.5, 4.5-7.5, 7.5-10.5, 10.5-13.5, 13.5-20, 20-40, 40+  ->  storeys 1, 2, 3, 4, 5-6, 7-13, 14+ (about 3 m a storey)."""
    T = _lga_table(); tot = [0.0] * 7; land = 0.0
    for n in lgas:
        r = T[n]; land += r["land_km2"]
        for i, v in enumerate(r["h_bands"]): tot[i] += v * r["land_km2"]
    s = sum(tot); return [v / s for v in tot]

STOREY_BANDS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 6), (7, 13), (14, 20)]

def _hotel(poi, LM):
    """Mean size and height of the tagged hotels in the study area (about 3 m a storey)."""
    hs = [h for h in LM.get("hotels", []) if h.get("height_m")]
    if not hs: return None
    return {"poi": poi, "m2": sum(h["m2"] for h in hs) / len(hs), "storeys": max(1, round(sum(float(h["height_m"]) for h in hs) / len(hs) / 3.0))}

def hub(ST, LM):
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # block long side = street spacing x elongation (the Maze's 150 m came from the same rule: 73 x 2.0)
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Close", "Avenue", "Crescent", "Way", "Drive", "Lane")}
    return {
        "lgas": ["Oshodi/Isolo", "Surulere"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},  # same spread as the Maze's 120/150/185 (95-240)
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.9,            # share of cross streets lined up with the one across the rib (X junction)
        "cross_scale": 1.5,           # cross-street spacing stretch (the Maze used one knob for both; the Hub needs ribs and cross streets tuned apart)
        "size_lo_u": 0.4,             # house sizes drawn from the upper 60% of the real distribution (plots shrink many of them to fit)
        "dead_end": 0.03,             # ribs that stop short on purpose; clipping around the rail and big parcels already makes plenty
        "big_front": 0.6,             # share of main-road plots that get one big building (shops, plazas), tuned to the real 7-9% over 400 m2
        "internal_mains": 0,          # 3 arterials + 4 edge roads already give more main road per km2 than real (3.3); see the study doc
        "name_endings": ends,
        "interchange": {
            "flyover_m": LM["flyover_spans_m"]["p75"],         # the long flyover over a road + rail knot (p50 spans are single over-rail bridges)
            "rail_bridge_m": LM["flyover_spans_m"]["p50"],     # major roads bridge the rail 92% of the time
            "slip_roads": round(LM["interchanges"]["slip_roads_each"]["p50"]),
            "slip_road_m": LM["interchanges"]["slip_road_m_each"]["p50"] / LM["interchanges"]["slip_roads_each"]["p50"],
            "skywalk_m": LM["footbridges"]["length_m"]["p50"], "skywalks_per_km_art": LM["footbridges"]["per_km_of_major_road"],
        },
        # big places carved out before streets are drawn (they are bigger than the biggest real block)
        "reserve": [
            {"kind": "bus terminal", "poi": "Gidi Interchange", "m2": LM["bus_stations"]["max_m2"], "aspect": 2.2, "front": "art", "near_knot": True,
             "building": {"kind": "terminal", "share": 0.55, "storeys": 3}},     # 3 storeys: Daramola's district model ("three-storey bus terminal")
            {"kind": "station", "poi": "Hub Rail Station", "m2": 2600, "aspect": 5.0, "front": "rail",
             "building": {"kind": "station", "m2": LM["rail_station_building_m2"][0], "storeys": 2}},
            {"kind": "stadium", "poi": "National Bowl", "m2": LM["stadium"]["stadium_ground_m2"][0], "aspect": 1.35, "front": None,
             "bowl_m2": LM["stadium"]["bowl_building_m2"][0], "storeys": 4,
             "access_roads": 2},   # owner's review: a second vehicle access from another side (one road made the okada run x2.40)
        ],
        # smaller places taken from finished blocks, as in the Maze
        "parcels": [
            {"kind": "motor park", "poi": "Boss's motor park", "ha": LM["bus_stations"]["area_m2"]["p75"] / 1e4, "near_main": True, "gate": "nearest"},   # its driveway onto the nearest road
            {"kind": "industrial", "ha": "from_study", "cap_ha": 3.0, "near": "rail_far_from_knot", "near_main": True},
            {"kind": "school", "ha": round(ST["landuse_polygons_ha"]["school"][1] / ST["landuse_polygons_ha"]["school"][0], 2), "near_main": False},   # real mean school compound
            {"kind": "pitch", "ha": round(ST["landuse_polygons_ha"]["pitch"][1] / ST["landuse_polygons_ha"]["pitch"][0], 2), "near_main": False},     # real mean pitch
        ],
        "hotel": _hotel("Stadium Highlife Hotel", LM),
        # owner's review (Oct 2026): the same walking rules as the Maze (rail paths, worn crossings every 150-200 m,
        # lanes start on streets, nothing over 44 m from a way), and a skywalk from the terminal to the station
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200],
                 "cut_every_m": 90, "cut_max_m": 130},   # owner's review: the rail-side blocks west of Ayinde Avenue were too deep (walks x2.6-3.5)
        "station_skywalk": {"name": "Station skywalk", "width": 4},   # over Ring Road and the rail, as at the real interchange
        "lock": {"parcels": ["Boss's motor park"]},   # the opening: the boss watches the chase from here (web/locked.json)
        "keep_gateways": True,   # rebuilt after the Capital: its crossings with the Capital (and all others) stay as agreed
    }

def maze(ST, LM):
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 73 x 2.0 = 146 m, the v1 Maze's 150 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Avenue", "Close", "Way", "Crescent", "Lane")}
    mk = sorted(LM["markets_m2"]); mk = [m for m in mk if m < 50000]   # the one 21 ha market is a whole quarter, not a parcel
    return {
        "lgas": ["Mushin", "Shomolu"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.5,            # v1 value: half the cross streets line up (real: 84% T, 16% X)
        "cross_scale": 1.35,          # same stretch as the ribs, as in v1
        "size_lo_u": 0.5,             # house sizes from the upper half of the real range (plots shrink many of them)
        "back_row": 0.45,             # chance of a back house behind the front one; v1's 0.85 left the front row at ~50% (real 61-63%)
        "dead_end": 0.12,
        "big_front": 0.08,            # a few big shops and workshops on the main roads (real: 2-5% of buildings over 400 m2)
        "internal_mains": 1,          # the through-road only: its two gateways are already agreed with Jungle City and Food Gate
        "keep_gateways": True,        # web/network.json already holds the Maze's edge roads and crossings; the Hub was built against them
        "name_endings": ends,
        # majors crossing the rail: 4 of 6 on a bridge (67%), so the through-road bridges it; residential streets cross at level (real: 15 level crossings)
        "rail_bridge_m": LM["flyover_spans_m"]["p50"], "level_crossings": 1,
        # big places carved out before streets are drawn
        "reserve": [
            {"kind": "market", "poi": "Ladi Lane Parts Market", "m2": mk[len(mk) // 2], "aspect": 1.6, "front": "art"},   # median market; 4 of 5 touch a major road
        ],
        # smaller places taken from finished blocks
        "parcels": [
            {"kind": "industrial", "poi": "Daleko Grain Yard", "ha": "from_study", "cap_ha": 3.0, "near": "rail", "near_main": False,   # houses and yards hug the line
             "gate": "north"},   # owner's review: a north entrance onto the nearest street (it only opened to the south)
            {"kind": "motor park", "ha": round(LM["bus_stations"]["area_m2"]["p25"] / 1e4, 2), "near": "junction", "near_main": True, "min_w": 35},  # small park where the through-road meets Ring Road
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2), "near_main": False},   # median compound: the mean (2.4 ha) is pulled up by campuses
            {"kind": "pitch", "ha": round(LM["pitch_m2"]["p50"] / 1e4, 2), "near_main": False},     # median: a small street-football pitch
        ],
        "walk": {"rail_path_m": 4.5,          # a footpath each side of the line, inside its 6 m clear strip
                 "cross_every_m": [150, 200]},   # worn crossings over the rail (owner's call; OSM maps only 15 level crossings, one per 1.1 km)
        "rail_frontage": True,           # plots along the line are built 6 m from the track (real: 658 buildings within 30 m, 247 within 15 m); off for the Hub
        "fence_parcels": True,           # dead ends stop at a parcel's fence (off for the Hub, so its merged result stays as reviewed)
        "canal_footbridges": 1,         # Daramola's model: "a canal with a footbridge (the gang line)"; streets cross it on culverts
        "print_row": {"poi": "Pedro Print Row", "length_m": 180, "storeys": [2, 3]},   # house-front presses on 2-3 storey houses (district model)
        "spots": [{"poi": "Transformer 44", "kind": "transformer", "w": 3.0, "d": 2.5}],   # one transformer feeding a whole block
        # the opening (owner, Oct 2026): Tunde's room is a short walk from the parts market; The steal is the stall at its near (east)
        # end; the chase runs the length of the market and comes out across Idowu Street from the boss's motor park in the Hub
        "named": [{"poi": "The steal", "from": ["stalls"]},
                  {"poi": "Tunde's room", "from": ["back"]}],
        "market_through_aisle": True,   # an aisle along the market's length as well as across it: the chase route
        "post": {"poi": "Boss's post", "market": "Ladi Lane Parts Market", "from": "The steal", "m": [6, 4]},   # the boss sits here during the opening
        "lock": {"reserve": ["Ladi Lane Parts Market"], "buildings": ["The steal", "Tunde's room", "Boss's post"]},   # the opening, fixed for good (web/locked.json)
        "clear_access": True,           # streets stop at the market's own road instead of running beside it (living test, Oct 2026)
    }

def jungle(ST, LM):
    """Jungle City: Ajegunle (Ajeromi/Ifelodun, studied on its own) with a Festac estate block (Amuwo Odofin, study-festac*.json)."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 74 x 2.6 = 193 m: Ajegunle's blocks are long, on a regular grid
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Lane", "Crescent", "Close")}
    FE = json.load(open("study-festac.json"))
    return {
        "lgas": ["Ajeromi/Ifelodun"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.5, "dead_end": 0.12,
        "cross_scale": 1.8,           # cross streets far apart: Ajegunle is long east-west streets with few cross streets
        "sector_split_ha": 19,        # fewer collector streets: blocks counted like the real squares (closed) were 57/km2 against 42-44
        "size_lo_u": 0.65,            # house sizes from the upper 35% of the real range (plots shrink many of them)
        "back_row": 0.65,
        "courtyard_m": [0.8, 2.0],    # tighter compounds than Mushin's 1.5-4 m: real gaps 0.8-0.9 m, ground built on 41-43%
        "big_front": 0.15,            # few big buildings: 3% over 400 m2, 1.3 per km2 over 1,500 m2
        "internal_mains": 1, "continue_mains": True,   # the Maze's Adeleke Road carries on south to the coast
        "exp_bridge_m": LM["flyover_spans_m"]["p50"],  # ...over the Coastal Expressway on a flyover
        "exp_footbridges": {"m": LM["footbridges"]["length_m"]["p50"], "per_km": LM["footbridges"]["per_km_of_major_road"],
                            "max_gap_m": 300},   # owner's review: no stretch of the expressway over 300 m without a way across on foot
        "name_endings": ends,
        "reserve": [   # the plank market faces the expressway (real markets and retail: median 2.2 ha, 4 m from a main road)
            {"kind": "market", "poi": "Boundary Plank Market", "m2": ST["markets_and_retail"]["ha"]["p50"] * 1e4, "aspect": 1.6, "front": "art"},
        ],
        "parcels": [
            {"kind": "estate", "ha": round(FE["blocks"]["area_m2"]["p75"] / 1e4, 2), "uv": [0.15, 0.35], "near_main": True, "min_w": 60,   # one Festac block (p75: room for a few rows)
             "block_m": [16, 24], "gap_m": 4.5, "garden_m": 20, "shop_share": 0.5, "storeys": 4},   # Festac flats: 16 x 24 m, 4.5 m apart (measured); 4 storeys is the district model's "1970s estate flats"
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2), "near_main": False, "gate": "nearest"},   # a gate onto the nearest street (with fewer collectors, its block can be deep)
            {"kind": "pitch", "ha": round(LM["pitch_m2"]["p50"] / 1e4, 2), "near_main": False},
        ],
        "hotel": {"poi": "Ireti Hotel", "m2": ST["buildings"]["footprint_m2"]["p90"], "storeys": 3},   # "tiny hotels": a big house's footprint (p90), 3 storeys; no hotels mapped
        "named": [{"poi": "Jahman Sound Studio", "kind": "studio", "from": ["front"]},
                  {"poi": "Network Plus Café", "kind": "cafe", "from": ["front"]}],
        "canal_footbridges": 1,
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "rail_frontage": True,
        "clear_access": True,           # living test (Oct 2026): streets join the market's own road instead of running beside it
        "keep_gateways": True,          # rebuilt after the Bazaar: its crossings with the Bazaar (and all others) stay as agreed
    }

def foodgate(ST, LM):
    """Food Gate: the Ojota-Ketu-Mile 12 corridor of Kosofe (study-foodgate*, a box inside the LGA; whole Kosofe is in study-kosofe*,
    mostly wetland). Heights from Kosofe in lga_table.json. A produce district: the night market, lorries, the interstate bus park."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 81 x 1.9 = 153 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Close", "Crescent", "Avenue")}
    return {
        "lgas": ["Kosofe"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.4, "cross_scale": 1.35,
        "dead_end": 0.95,             # nearly every long rib stops short: real dead ends 0.40-0.42 per junction, the most of any district so far
        "size_lo_u": 0.7, "plot_u": [0.65, 0.99],   # wider plots, bigger houses (real typical house 152-168 m2)
        "back_row": 0.45, "big_front": 0.12,
        "vacant": 0.4,                # many empty and half-built plots: real squares are only 15-27% built on
        "internal_mains": 1, "continue_mains": True,   # the Maze's Adeleke Road carries on north
        "name_endings": ends,
        "reserve": [
            # the produce market that runs at night: the real Ketu Market (6.3 ha; Mile 12 itself is 12.5 ha, 7% of this district), on the arterial
            {"kind": "market", "poi": "Mile Market", "m2": 63099, "aspect": 1.8, "front": "art"},
            # interstate coaches: the real Mile 12 Bus Terminal (1.1 ha), on the arterial, with a low terminal shed
            {"kind": "bus terminal", "poi": "Northern Bus Park", "m2": LM["bus_stations"]["max_m2"], "aspect": 2.2, "front": "art",
             "building": {"kind": "terminal", "share": 0.3, "storeys": 1}},
        ],
        "parcels": [
            {"kind": "lorry park", "ha": round(LM["parking_lots_m2"]["p75"] / 1e4, 2), "near": "res:market", "near_main": False, "gate": "nearest"},   # the 1.8-1.9 ha yards by the market
            {"kind": "park", "poi": "Freedom Ground", "ha": 0.89, "near_main": True},   # the largest mapped park (0.89 ha); a stage at one end
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2), "near_main": False},
            {"kind": "pitch", "ha": round(LM["pitch_m2"]["p50"] / 1e4, 2), "near_main": False},
        ],
        "road_footbridges": [   # real: 0.71 per km of major road; 48 m (p75) clears the arterial
            {"near": "market", "cls": ["art"], "m": LM["footbridges"]["length_m"]["p75"], "name": "Market footbridge"},
            {"near": "bus terminal", "cls": ["art"], "m": LM["footbridges"]["length_m"]["p75"], "name": "Bus park footbridge"}],
        "spots": [{"poi": "Long Bridge checkpoint", "kind": "checkpoint", "w": 4.0, "d": 3.0}],   # the taskforce post on the road to the bridge
        "jetty": {"poi": "Agboyi Creek Villages", "name": "Agboyi canoe jetty", "m": 15},   # the creek villages are reached only by canoe
        "market_through_aisle": True, "clear_access": True,
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True,
        "keep_gateways": True,   # rebuilt after Water Town: its crossings with Water Town (and all others) stay as agreed
    }

def watertown(ST, LM):
    """Water Town: the Makoko-Iwaya and Bariga waterfront (study-watertown*, two boxes inside Lagos Mainland + Shomolu).
    The land fabric is calibrated on the land buildings; the stilt village on study-watertown-village.json (the buildings on the water)."""
    V = json.load(open("study-watertown-village.json"))
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Close", "Way")}
    return {
        "lgas": ["Lagos Mainland", "Shomolu"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense land squares
        "x_junction": 0.0, "cross_scale": 4.5, "dead_end": 0.9, "size_lo_u": 0.4, "plot_u": [0.3, 0.9],
        "back_row": 0.9, "courtyard_m": [0.5, 1.5], "big_front": 0.1, "vacant": 0.18,
        # streets run down to the shore as fingers and most stop short of the water (the real waterfront: ~10 km of road per km2,
        # about half the junctions dead ends); short side lanes branch off them into the compounds, and a few cross links tie them
        "fingers": {"stop_m": [25, 45], "through": 0.4, "spur_every_m": 200, "spur_m": [30, 55]},
        "internal_mains": 0,          # Ring Road crosses it; the real waterfront has little main road (0.6-1.6 km/km2)
        "name_endings": ends,
        "edge_rail_bridge_m": LM["flyover_spans_m"]["p50"],   # Okafor Road over the rail: majors cross on bridges (Mainland + Shomolu 6 of 6; Mushin + Shomolu 4 of 6)
        "parcels": [
            {"kind": "sawmill", "poi": "Okobaba Sawmill", "ha": 1.5, "near": "shore", "near_main": False, "gate": "nearest"},   # on the water, with log rafts
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2), "near_main": False},
        ],
        "stilt_village": {"poi": "Stilt Village", "near": "bridge", "shift_m": -170, "bar_poi": "The Stilt Bar", "seed": 42,   # built with seed 42 (v1)
                          "length_m": 300, "depth_m": 190,            # about 5.7 ha of water (the real village is 41 ha: chosen, not scaled)
                          "spine_every_m": 34,                        # boardwalks; a canoe lane between each pair of hut rows
                          "cross_every_m": 70,                        # plank walkways across the lanes
                          "hut_m": [V["short_side_m"]["p50"], V["long_side_m"]["p50"]], "gap_m": V["gap_m"]["p50"],
                          "second_row": 0.4},                         # tuned to the real 46% cover
        "jetty": {"poi": "Canoe Jetty", "name": "Canoe Jetty", "m": 20},   # canoes to the creeks and Old Shore
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "rail_frontage": True, "clear_access": True,
        "lock": {"parcels": ["Okobaba Sawmill"]},   # the sawmill chase's ground stays put when the land fabric is rebuilt (web/locked.json)
        "keep_gateways": True,   # rebuilt after the Port: its crossings with the Port (and all others) stay as agreed
    }

def capital(ST, LM):
    """The Capital: central Ikeja (study-capital*, a box round the phone market, Allen and the state secretariat; GRA is left to the
    Estate). OSM maps Ikeja's streets well but few of its buildings: building density is estimated (scripts/study_undermapped.py)
    and house sizes come from the whole LGA (study-ikeja*). Heights from Ikeja in lga_table.json, the tallest LGA so far."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Way", "Close", "Avenue", "Crescent", "Drive")}
    return {
        "lgas": ["Ikeja"],
        "sizes_from": "ikeja",
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.5, "cross_scale": 2.2, "dead_end": 0.1, "size_lo_u": 0.5, "plot_u": [0.55, 0.99],   # bigger houses (real typical 187 m2)
        "sector_split_ha": 30,        # fewer collector streets: 59 blocks/km2 against the real 31-49 (counted closed); 30 since Railside
        "spurs": {"spur_every_m": 250, "spur_m": [25, 45]},   # a few dead-end side streets (real 0.14-0.17 dead ends per junction)
        "back_row": 0.55, "big_front": 0.5, "vacant": 0.08,   # offices, plazas and banks on the main roads (real: 16% over 400 m2)
        "internal_mains": 2,          # real main roads 4-5.5 km/km2: the most of any district so far
        "name_endings": ends,
        "roundabout": {"poi": "Allen Roundabout Strip", "r_m": 22, "strip_m": 160},   # the all-night strip round a roundabout with a bust
        "zone": {"poi": "Gadget Village", "r_m": 120, "kind": "phone mall", "min_m2": 80, "storeys": [3, 4], "kiosk_every_m": 9},   # 4.5 ha of the real 14 ha
        "halls": [{"poi": "The Shrine", "kind": "hall", "m2": 1200, "storeys": 2}],   # the live-music hall (the real compound is 0.2 ha)
        "parcels": [
            {"kind": "government", "poi": "Secretariat", "ha": 3.0, "near_main": True, "storeys": 5, "slab_m": [90, 16], "slab_gap_m": 50},
            {"kind": "barracks", "poi": "Cantonment", "ha": 4.0, "near_main": False, "block_m": [40, 9], "gap_m": 9, "parade_m": 44, "gate": "nearest"},
            {"kind": "airfield", "poi": "Airport Fence", "ha": 3.5, "near_main": False},   # the airport's grass edge behind its fence
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2), "near_main": False},
            {"kind": "pitch", "ha": round(LM["pitch_m2"]["p75"] / 1e4, 2), "near_main": False},
        ],
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "rail_frontage": True, "clear_access": True,
        "t_into_done": True,     # built after the Hub and Food Gate: its main roads T into their edge roads instead of asking them for new crossings
        "keep_gateways": True,   # rebuilt after Railside: its crossings with Railside (and all others) stay as agreed
    }

def bazaar(ST, LM):
    """The Bazaar: Ojo round the electronics market (study-bazaar*, a box 3.175-3.240 E, 6.450-6.480 N: the market, Iyana-Iba,
    Mami Market and the cantonment's edge; whole Ojo is in study-ojo*). Heights from Ojo in lga_table.json: mostly 1-2 storeys."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 82 x 1.8 = 149 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Way", "Lane")}
    JL = json.load(open("study-jungle-landmarks.json"))   # no footbridge is mapped in the box; the Coastal Expressway's are Jungle City's
    return {
        "lgas": ["Ojo"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.0, "cross_scale": 6, "dead_end": 1.0,   # long streets, few cross streets, every long one stops short
        "spurs": {"spur_every_m": 120, "spur_m": [30, 60]},   # short dead-end side streets: real dead ends 0.42-0.54 per junction, 92-97% T
        "sector_split_ha": 45,        # few collector streets: real blocks 18-27 per km2 (counted closed)
        "size_lo_u": 0.3, "back_row": 0.5, "big_front": 0.05, "vacant": 0.25,   # small houses (real typical 79-100 m2), a quarter of plots empty
        "internal_mains": 1, "t_into_done": True,
        "exp_bridge_m": LM["flyover_spans_m"]["p50"],
        "exp_footbridges": {"m": JL["footbridges"]["length_m"]["p50"], "per_km": JL["footbridges"]["per_km_of_major_road"], "max_gap_m": 300},   # the owner's rule
        "name_endings": ends,
        "reserve": [   # the electronics market: 7 ha of lock-up rows (the real one is 23 ha, a fifth of this district), on the expressway
            {"kind": "market", "poi": "Alade Electronics Market", "m2": 70000, "aspect": 1.6, "front": "art"},
        ],
        "parcels": [
            {"kind": "plazas", "poi": "Fair Wholesale Plazas", "ha": 2.5, "near_main": True, "block_m": [36, 22], "unfinished_every": 3, "gate": "nearest"},   # every third plaza never finished
            {"kind": "livestock", "poi": "Rago Yard", "ha": 1.5, "near_main": False, "pen_m": [8, 5], "lane_m": 4, "scrap_piles": 8, "gate": "nearest"},
            {"kind": "barracks", "poi": "Barracks", "ha": 4.0, "near_main": True, "block_m": [40, 9], "gap_m": 9, "parade_m": 44, "gate": "nearest"},
            {"kind": "school", "ha": round(LM["school_m2"]["p25"] / 1e4, 2), "near_main": False, "gate": "nearest", "min_w": 70},
            {"kind": "pitch", "ha": 0.15, "near_main": False},
        ],
        "keep_gateways": True,   # rebuilt after Railside: its crossings stay as agreed
        "spots": [{"poi": "Container Court", "kind": "container", "w": 12.2, "d": 2.5},                 # the shipping-container jail
                  {"poi": "Barracks checkpoint", "at": "Barracks", "kind": "checkpoint", "w": 4.0, "d": 3.0}],   # "checkpoint outside"
        "market_through_aisle": True,
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "rail_frontage": True, "clear_access": True,
    }

def port(ST, LM):
    """The Port: Apapa LGA (study-port*, the whole LGA: the port, Tincan Island, the reserve and the dense streets by the creek).
    Heights from Apapa in lga_table.json. Most of the real port is open yard: few buildings, low cover, long main roads."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 75 x 2.4 = 179 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Road", "Street", "Avenue", "Crescent", "Lane", "Close")}
    return {
        "lgas": ["Apapa"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.3, "cross_scale": 2.0, "dead_end": 0.05,   # real dead ends only 0.06-0.08 per junction
        "sector_split_ha": 80,        # few collector streets: the yards and the reserve already cut the land up
        "size_lo_u": 0.7, "plot_u": [0.6, 0.99], "back_row": 0.4, "big_front": 0.4, "vacant": 0.35,   # bigger houses, many empty plots (real cover 16-23%)
        "internal_mains": 0,          # the expressway, Ring Road and the edge roads already give more main road than real (3.3-4.2 km/km2)
        "exp_bridge_m": LM["flyover_spans_m"]["p50"],
        "exp_footbridges": {"m": LM["footbridges"]["length_m"]["p50"], "per_km": LM["footbridges"]["per_km_of_major_road"], "max_gap_m": 300},   # the owner's rule
        "name_endings": ends,
        "reserve": [
            # the port: 16 ha of the real 281 ha, on the lagoon quay (the district model: container stacks, gantry cranes, customs sheds)
            {"kind": "container yard", "poi": "Container Yard", "m2": 160000, "aspect": 1.8, "front": None, "near": "shore", "access_roads": 2},
            # the tank farm, also on the quay: tanks of 14 m radius in a grid
            {"kind": "tank farm", "poi": "Tank Farm", "m2": 50000, "aspect": 1.4, "front": None, "near": "shore", "tank_r_m": 14},
            # the night market under the expressway's approach to the Wharf Bridge
            {"kind": "under bridge", "poi": "Liverpool Under-Bridge", "m2": 9000, "aspect": 3.0, "front": "art"},
        ],
        "parcels": [
            {"kind": "villas", "poi": "Old Reserve Avenue", "ha": 5.0, "near_main": False, "min_w": 110, "block_m": [18, 13], "gap_m": [24, 22], "margin_m": 10, "building": "villa", "avenue": True},   # bungalows either side of the reserve's own avenue   # bungalows in big gardens
            {"kind": "prison", "poi": "Kiri Prison", "ha": 3.0, "near_main": False, "block_m": [42, 11], "gap_m": [10, 14], "margin_m": 14, "building": "cellblock", "gate": "nearest"},
            {"kind": "truck park", "ha": round(LM["parking_lots_m2"]["p75"] / 1e4, 2), "near": "res:tank farm", "near_main": False,
             "block_m": [16, 2.8], "gap_m": [3, 4], "building": "trailer", "gate": "nearest"},   # tankers queue here for days
            {"kind": "school", "ha": 1.2, "near_main": False, "gate": "nearest", "min_w": 70},
            {"kind": "pitch", "ha": round(LM["pitch_m2"]["p50"] / 1e4, 2), "near_main": False},
        ],
        "spots": [{"poi": "Collector Row", "kind": "checkpoint", "w": 4.0, "d": 3.0, "shift_m": 0},   # police, traffic, union, area boys: pay each one
                  {"poi": "Collector Row 2", "at": "Collector Row", "kind": "checkpoint", "w": 4.0, "d": 3.0, "shift_m": 100},
                  {"poi": "Collector Row 3", "at": "Collector Row", "kind": "checkpoint", "w": 4.0, "d": 3.0, "shift_m": -100},
                  {"poi": "Collector Row 4", "at": "Collector Row", "kind": "checkpoint", "w": 4.0, "d": 3.0, "shift_m": 150}],
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "rail_frontage": True, "clear_access": True,
    }

def railside(ST, LM):
    """Railside: Agege, Ifako/Ijaye and Alimosho (study-railside*, the three whole LGAs: commuter sprawl along the railway).
    Heights from the three LGAs in lga_table.json. The district model: bakeries, the cattle market, the market roundabout,
    the old waterworks, the pipeline, the landfill."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 83 x 2.1 = 174 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Close", "Avenue", "Crescent")}
    return {
        "lgas": ["Agege", "Ifako/Ijaye", "Alimosho"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.0, "cross_scale": 2.2, "dead_end": 0.6,   # real dead ends 0.25-0.40 per junction, 88-99% T
        "sector_split_ha": 25,
        "size_lo_u": 0.6, "plot_u": [0.5, 0.99], "back_row": 0.5, "big_front": 0.1, "vacant": 0.1,   # real typical house 127-175 m2
        "internal_mains": 2, "t_into_done": True, "continue_mains": True,   # the Capital's main road carries on in
        "rail_bridge_m": LM["flyover_spans_m"]["p50"],   # ...and over the rail on a bridge (real: 4 of 6 major-road crossings bridged)
        "roundabout": {"poi": "Ikotun-style Roundabout Market", "r_m": 26, "strip_m": 0, "name": "Market Roundabout"},   # four exits; the market sits on it
        "name_endings": ends,
        "parcels": [
            {"kind": "market", "poi": "Ikotun-style Roundabout Market", "ha": 3.0, "near": "roundabout", "near_main": True},   # lock-ups on the roundabout
            {"kind": "livestock", "poi": "Oko Cattle Market & Abattoir", "ha": 3.0, "near_main": False, "pen_m": [10, 6], "lane_m": 5, "scrap_piles": 0, "gate": "nearest", "min_w": 90},
            {"kind": "waterworks", "poi": "Iju Waterworks (1915)", "ha": 2.0, "near_main": False, "works_m": [40, 18], "tanks": 2, "tank_r_m": 11, "gate": "nearest", "min_w": 80},
            {"kind": "landfill", "poi": "Railside Landfill", "ha": round(ST["landuse_polygons_ha"]["landfill"][1] / ST["landuse_polygons_ha"]["landfill"][0], 1), "near_main": False,
             "block_m": [14, 14], "gap_m": [12, 12], "margin_m": 8, "building": "mound", "gate": "nearest", "min_w": 90},   # real mean landfill ~8 ha
            {"kind": "market", "poi": "Bale Market (Mon/Wed/Fri)", "ha": 1.5, "near_main": True},
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2) if LM.get("school_m2") else 1.0, "near_main": False, "gate": "nearest", "min_w": 70},
            {"kind": "pitch", "ha": 0.15, "near_main": False},
        ],
        "zone": {"poi": "Ayo Bakery Row", "r_m": 70, "kind": "bakery", "min_m2": 50, "storeys": [1, 2], "kiosk_every_m": 1000},   # house fronts turned into bakeries
        "pipeline": {"poi": "Pipeline Corridor", "bearing_deg": 20, "width_m": 24},   # the line's cleared right of way
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "rail_frontage": True, "clear_access": True,
    }

def estate(ST, LM):
    """The Estate: Ikeja GRA, Magodo and Omole (study-estate*, three boxes inside Ikeja and Kosofe: the estates only, as the brief says).
    OSM maps the streets of all three but the buildings only in Ikeja GRA: building figures come from GRA's traced cells
    (scripts/study_wellmapped.py). Heights from Ikeja and Kosofe in lga_table.json. The district model: gated streets, gatemen,
    duplexes behind high walls, generators and water tanks, quiet tree-lined streets, a church and a mosque at the centre."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 84 x 2.1 = 176 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Way", "Close", "Crescent", "Avenue")}
    return {
        "lgas": ["Ikeja", "Kosofe"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.1, "cross_scale": 2.0, "dead_end": 0.9,
        "sector_split_ha": 40,        # few collector streets: real blocks 22-24 per km2 (counted closed), the fewest of any district
        "spurs": {"spur_every_m": 45, "spur_m": [40, 90]},   # closes: real dead ends 0.52-0.65 per junction, the most of any district
        "size_lo_u": 0.6, "plot_u": [0.6, 0.99], "back_row": 0.6, "courtyard_m": [1.5, 3], "big_front": 0.0, "vacant": 0.18,   # big houses, a boys' quarters behind; empty plots
        "setback_m": [6, 12], "side_garden_m": [4, 10],   # a front yard behind the wall and a garden down the side (real edge-to-street median 15-19 m)
        "kiosk_every_m": 400,         # quiet streets: few kiosks
        "internal_mains": 1, "t_into_done": True, "continue_mains": True,   # the Capital's main road carries on in, through the main gate
        "name_endings": ends,
        "parcels": [
            # where the men above the boss meet: a 0.6 ha compound, a three-storey house, boys' quarters, a gatehouse, generators, a pool
            {"kind": "compound", "poi": "The Senator's House", "ha": 0.6, "near_main": False, "gate": "nearest", "min_w": 70,
             "buildings": [["mansion", [30, 18], [0.0, 0.1]], ["back", [16, 6], [0.55, -0.6]], ["generator", [4, 2.5], [-0.6, -0.6]],
                           ["generator", [4, 2.5], [-0.45, -0.6]], ["water tank", [3, 3], [0.75, 0.55]]],
             "grounds": [["pool", [12, 5], [-0.45, 0.55]]]},
            # the quiet bar for big men: a clubhouse, a pool and a tennis court behind the wall
            {"kind": "club", "poi": "Estate Club", "ha": 0.8, "near_main": True, "gate": "nearest", "min_w": 70,
             "buildings": [["clubhouse", [34, 20], [-0.35, 0.0]]],
             "grounds": [["pool", [25, 12], [0.25, 0.45]], ["court", [36, 18], [0.45, -0.4]]]},
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2), "near_main": False, "gate": "nearest", "min_w": 70},   # a private school
            {"kind": "pitch", "ha": 0.15, "near_main": False},
        ],
        # the gates (real: 5.1 street gates per km2 mapped, twice any other district; a median 13 m in from the main road)
        "estate_gates": {"in_m": 13, "house_m": [3.5, 3.0], "main_in_m": 30, "main_house_m": [6, 4], "poi": "Estate Gate"},
        "plot_walls": {"gate_m": 4.0, "vacant_walled": 0.5, "parcels": ["compound", "club", "school"]},   # high walls round every plot (the district model)
        "yard_kit": {"generator": 0.85, "generator_m": [2.6, 1.6], "water tank": 0.6, "tank_m": [2.4, 2.4]},   # generators and water tanks (the district model)
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]}, "lane_passages": False,   # no short cuts through walled compounds
        "fence_parcels": True, "clear_access": True, "drop_doubled_streets": True,
    }

def oldisland(ST, LM):
    """Old Island: Lagos Island (study-oldisland*, the island itself: the LGA's outline is mostly lagoon, so the study is boxed to the
    island). OSM maps the streets everywhere but traces the buildings fully only in the old core (Isale Eko): building figures come from
    its traced cells (scripts/study_wellmapped.py). Heights from Lagos Island in lga_table.json. The district model: the palace, the cloth
    market with lanes only porters can enter, decaying Brazilian houses, bank towers on the waterfront, a fenced square with fountains."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 79 x 1.8 = 143 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Way", "Square", "Avenue", "Lane")}
    mk = sorted(LM["markets_m2"])
    return {
        "lgas": ["Lagos Island"],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.95, "cross_scale": 1.3, "dead_end": 0.05,   # real: 67-81% T, the most X junctions of any district; 0.07-0.12 dead ends
        "size_lo_u": 0.5, "back_row": 0.5, "courtyard_m": [0.5, 1.5], "big_front": 0.08, "vacant": 0.02,   # real typical house 142 m2, 4-8% over 400 m2; houses 0.7-1.0 m apart
        "internal_mains": 1,
        "bridge_links": True,   # the two bridges from the mainland land on the island's edge road
        "keep_gateways": True,   # the Heights was built after it: its edge road and crossings are reused exactly
        "name_endings": ends,
        "reserve": [   # the cloth market: the island's big markets run 0.5-9.5 ha; this one is the upper quartile, on Waterfront Drive
            {"kind": "market", "poi": "Cloth Market", "m2": mk[3 * len(mk) // 4], "aspect": 1.6, "front": "art"},
        ],
        "market_aisle_m": 2.5,   # cloth market lanes 2-3 m wide: porters with head loads, no barrows (district model)
        "parcels": [
            # the palace: a walled compound, the palace house round a forecourt, the chiefs' houses behind (never a crime site)
            {"kind": "palace", "poi": "The Palace", "ha": 0.8, "near_main": False, "gate": "nearest", "min_w": 70,
             "buildings": [["palace", [42, 22], [0.0, 0.25]], ["back", [18, 7], [0.6, -0.55]], ["back", [18, 7], [-0.6, -0.55]]],
             "grounds": [["forecourt", [30, 18], [0.0, -0.45]]]},
            {"kind": "motor park", "poi": "Island Motor Park", "ha": round(LM["bus_stations"]["area_m2"]["p50"] / 1e4, 2), "near_main": True, "gate": "nearest"},
            # the fenced square with fountains (district model), on a main road
            {"kind": "square", "ha": 0.35, "near_main": True, "gate": "nearest",
             "grounds": [["fountain", [6, 6], [-0.4, 0.0]], ["fountain", [6, 6], [0.4, 0.0]]]},
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2), "near_main": False, "gate": "nearest", "min_w": 60},
            {"kind": "pitch", "ha": 0.15, "near_main": False},
        ],
        "walled": ["palace", "square"],
        # the Brazilian Quarter: the houses round the pin are the returnee houses, brick with arches and shutters, two storeys
        "zone": {"poi": "Brazilian Quarter", "r_m": 90, "kind": "brazilian house", "min_m2": 60, "storeys": [2, 2], "kiosk_every_m": 1000},
        # Bank Row: glass towers on the waterfront road (real: Lagos Island has 1% of its built area at 14+ storeys)
        "halls": [{"poi": "Bank Row", "kind": "bank tower", "m2": 900, "aspect": 1.5, "storeys": 18, "shore": True} for _ in range(4)],
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "clear_access": True,
    }

def heights(ST, LM):
    """The Heights: Ikoyi, Victoria Island and Banana Island (study-heights*, three boxes inside Eti Osa, as the brief says). OSM traces
    the buildings well in all three (90% of the 250 m cells), so every figure is measured on the study itself. Heights come from the boxes
    too (Google Open Buildings 2.5D, scripts/study_boxheights.py): Eti Osa as a whole is mostly Lekki's low estates and would hide the
    towers. The district model: glass towers, gated mansions on cul-de-sacs, a cable-stayed toll bridge, a club strip, a beach, leafy roads."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el * 0.6   # 109 x 2.7 = 295 m counts the long VI blocks; the closes and side streets of Ikoyi run shorter
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Close", "Road", "Avenue", "Crescent", "Drive")}
    return {
        "lgas": ["Eti Osa"],
        # storeys 1, 2, 3, 4, 5-6, 7-13, 14+ by built area, measured on the three boxes (Eti Osa whole: 31/50/13/3/2/1/0)
        "h_bands": [0.1884, 0.4511, 0.185, 0.0595, 0.0467, 0.0426, 0.0266],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.1, "cross_scale": 2.0, "dead_end": 0.3,
        "sector_split_ha": 40,
        "spurs": {"spur_every_m": 150, "spur_m": [40, 90]},   # closes: real dead ends 0.33-0.41 per junction
        "size_lo_u": 0.35, "plot_u": [0.5, 0.95], "back_row": 0.4, "courtyard_m": [1, 2.5], "big_front": 0.12, "vacant": 0.33,   # big houses: a rich man's area (owner, Oct 2026), bigger than Ikoyi's real 140-146 m2
        "setback_m": [8, 16], "side_garden_m": [1.5, 4],   # real edge-to-street median 22 m, the deepest of any district
        "kiosk_every_m": 500,
        "internal_mains": 2, "t_into_done": True, "continue_mains": True,   # real main roads 4.3-5.3 km per km2
        "bridge_links": True,   # the Cable Bridge lands on the north shore's edge road
        "toll": {"bridge": "Cable Bridge", "poi": "Cable Bridge", "in_m": 30},
        "keep_gateways": True,   # the Frontier was built after it: its edge roads and crossings are reused exactly
        "name_endings": ends,
        "parcels": [
            # The Gold Island: a walled enclave of billionaires' houses on reclaimed sand, one gate (real Banana Island: about 3 ha a street)
            {"kind": "enclave", "poi": "The Gold Island", "ha": 3.5, "near_main": False, "gate": "nearest", "min_w": 120,
             "buildings": [["mansion", [32, 20], [-0.55, -0.45]], ["mansion", [32, 20], [0.0, -0.45]], ["mansion", [32, 20], [0.55, -0.45]],
                           ["mansion", [32, 20], [-0.35, 0.45]], ["mansion", [32, 20], [0.3, 0.45]], ["gatehouse", [6, 4], [0.85, 0.0]]],
             "grounds": [["pool", [12, 6], [-0.55, -0.05]], ["pool", [12, 6], [0.0, -0.05]], ["pool", [12, 6], [0.55, -0.05]]]},
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2) if LM.get("school_m2") else 1.0, "near_main": False, "gate": "nearest", "min_w": 70},
            {"kind": "pitch", "ha": 0.15, "near_main": False},
        ],
        # the gates: real 6.1 street gates per km2 mapped, the most of any area. Only the closes are gated here (district model:
        # "gated mansions on cul-de-sacs"); the through streets stay open
        "estate_gates": {"in_m": 13, "house_m": [3.5, 3.0], "main_in_m": 30, "main_house_m": [6, 4], "closes_only": True, "main_gates": False},
        "plot_walls": {"gate_m": 4.0, "vacant_walled": 0.6, "parcels": ["enclave", "school", "golf course"]},   # mansions behind walls (district model)
        "yard_kit": {"generator": 0.85, "generator_m": [2.6, 1.6], "water tank": 0.5, "tank_m": [2.4, 2.4]},
        # the club strip: the houses round the pin are clubs and lounges (district model: valets and touts)
        "zone": {"poi": "Club Strip", "r_m": 80, "kind": "nightclub", "min_m2": 120, "storeys": [1, 3], "kiosk_every_m": 1000},
        # Pearl Towers: luxury apartment towers on a main road (real: 2.7% of the boxes' built area is 14+ storeys, 4.3% 7-13)
        # the Victoria Island side (owner, Oct 2026): south of Waterfront Drive, towards the beach, an office-and-hotel grid with no compound
        # walls. Measured on the VI box alone (study-hvi-core): 264-410 buildings per km2, typical 281-293 m2, 29-33% over 400 m2, 74-80% T
        # (a grid: more crossroads), 0.32 dead ends per junction; Ikoyi's box alone: 520-619 per km2, typical 140-146 m2, 16-17% over 400
        "quarter": {"south_of": "Waterfront Drive", "office_m2": 400,
                    "rules": {"x_junction": 0.6, "dead_end": 0.1, "spurs": None, "size_lo_u": 0.35, "plot_u": [0.7, 0.99], "back_row": 0.15,
                              "vacant": 0.42, "setback_m": [8, 16], "side_garden_m": [3, 8], "big_front": 0.08, "no_walls": True}},
        # the Ikoyi side's houses in five styles (owner, Oct 2026: "variety in architecture"; see the study, section 8)
        "styles": {"outside_quarter": True, "modern": 0.22, "mansion_m2": 450, "mediterranean": 0.35},
        # the golf club (owner, Oct 2026; real: two golf courses, 77 ha, in the study's Ikoyi box): a 6 ha course on the Ikoyi side,
        # carved out before the streets so they run round it; a clubhouse, greens, bunkers and a pond
        "reserve": [{"kind": "golf course", "poi": "Heights Golf Club", "m2": 60000, "aspect": 1.6, "front": None,
                     "buildings": [["clubhouse", [30, 16], [0.85, 0.0]]],
                     "grounds": [["green", [22, 16], [-0.75, -0.55]], ["green", [22, 16], [-0.3, 0.6]], ["green", [22, 16], [0.25, -0.6]], ["green", [22, 16], [0.55, 0.55]],
                                 ["bunker", [12, 7], [-0.6, -0.35]], ["bunker", [12, 7], [0.4, -0.3]], ["pond", [40, 22], [-0.05, 0.05]]]}],
        # Sunday Beach (owner, Oct 2026): shacks, bars and a horse shelter on the sand beyond the shore road (district model: "beach with shacks and horses")
        "beach": {"poi": "Sunday Beach", "every_m": [14, 30], "depth_m": 22, "mix": [6, 3, 1]},
        "halls": [{"poi": "Pearl Towers", "kind": "apartment tower", "m2": 1100, "aspect": 1.3, "storeys": 20, "within_m": 250, "front_m": 20} for _ in range(3)],   # behind a front yard, like the houses
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]}, "lane_passages": False,
        "fence_parcels": True, "clear_access": True, "drop_doubled_streets": True,
    }

def frontier(ST, LM):
    """The Frontier: the Lekki peninsula (study-frontier*, three boxes: Lekki Phase 1 and Ajah-Sangotedo in Eti Osa, Awoyaya-Lakowe in
    Ibeju-Lekki). OSM's extract stops short of the refinery end. Buildings are traced well in Lekki Phase 1 and Ajah but only in part
    further out, where WorldCover shows the empty cells really are empty (laid-out estates, no houses yet): building figures come from
    Ajah's traced cells (scripts/study_wellmapped.py), and the emptiness is built as walled, never-built plots. Heights from the boxes.
    The district model: one long road past a toll plaza, half-built estates, fenced empty plots with two owners, a refinery, an eroding beach."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 83 x 2.2 = 183 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Close", "Crescent", "Way", "Avenue", "Drive")}
    return {
        "lgas": ["Eti Osa", "Ibeju Lekki"],
        # storeys 1, 2, 3, 4, 5-6, 7-13, 14+ by built area, on the boxes (Open Buildings 2.5D): Lekki-Ajah 27/54/15/3/1/0/0, Awoyaya 49/45/5/1/0/0/0, by land
        "h_bands": [0.384, 0.493, 0.094, 0.018, 0.0085, 0.0024, 0.0001],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.1, "cross_scale": 2.0, "dead_end": 0.4,
        "sector_split_ha": 40,
        "spurs": {"spur_every_m": 120, "spur_m": [40, 90]},   # estate closes: real 0.23-0.44 dead ends per junction
        "size_lo_u": 0.5, "plot_u": [0.5, 0.95], "back_row": 0.3, "courtyard_m": [1, 3], "big_front": 0.15,   # real (Ajah) typical 200 m2
        "vacant": 0.55,   # more than half the plots never built: laid-out estates ahead of the houses (Awoyaya's street cells: 44% with no mapped buildings)
        "vacant_blocks": {"share": 0.45, "vacant": 0.92, "built_vacant": 0.25},   # ...in tracts: 45% of blocks almost empty, the rest a quarter empty
        "setback_m": [4, 10], "side_garden_m": [1.5, 4],   # real edge-to-street median 14-24 m
        "kiosk_every_m": 200,
        "unfinished_share": 0.06,   # half-built houses (real: 1.7% tagged under construction, a floor; the district model: "half-built estates")
        "internal_mains": 1, "t_into_done": True, "continue_mains": True,
        "bridge_links": True,   # the Cable Bridge from the Heights lands on the north shore's edge road
        "name_endings": ends,
        "reserve": [   # the refinery on the lagoon shore: tanks on one half, the process plant (columns, a flare stack) on the other
            {"kind": "refinery", "poi": "Refinery", "m2": 120000, "aspect": 1.5, "front": None, "near": "shore", "tank_r_m": 16}],
        "toll_plaza": {"poi": "Toll Plaza", "road": "Peninsula Expressway", "booths": 7},
        # the disputed plots: round the pin, most plots are walled and empty ("this land is not for sale"; every plot has two owners)
        "quarter": {"around": "Disputed Plots", "r_m": 180, "rules": {"vacant": 0.75, "back_row": 0.1}},
        # the eroding beach: a few fishermen's shacks on what is left of the sand
        "beach": {"poi": "Eroding Beach", "every_m": [40, 90], "depth_m": 6, "mix": [1, 0, 0]},
        "parcels": [
            {"kind": "school", "ha": 1.0, "near_main": False, "gate": "nearest", "min_w": 60},
            {"kind": "pitch", "ha": 0.15, "near_main": False},
        ],
        "plot_walls": {"gate_m": 4.0, "vacant_walled": 0.4, "parcels": ["school"]},   # built plots walled, and a share of the empty ones: "every fence is a fight"
        "yard_kit": {"generator": 0.6, "generator_m": [2.6, 1.6], "water tank": 0.3, "tank_m": [2.4, 2.4]},
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]}, "lane_passages": False,
        "fence_parcels": True, "clear_access": True, "drop_doubled_streets": True,
    }

def oldshore(ST, LM):
    """Old Shore: old Ikorodu (study-oldshore*, one box over the old town centre and the Ebute lagoon shore, inside Ikorodu LGA).
    Epe is not in the local OSM extract, so it is not studied. OSM traces Ikorodu's buildings well. Heights from the box (Open
    Buildings 2.5D). The district model: a fish market at a jetty with smoking racks and barges, a ferry jetty, a founder statue on
    the garage roundabout, a low-rise old town with its own king, a barge yard."""
    sp = ST["parallel_street_spacing_m"]["p50"]; el = ST["blocks"]["elongation_long_over_short"]["p50"]
    p50 = sp * el   # 84 x 1.9 = 160 m
    ends = {k: v for k, v in ST["street_name_endings"].items() if k in ("Street", "Road", "Close", "Crescent", "Avenue")}
    return {
        "lgas": ["Ìkòròdú"],
        # storeys 1, 2, 3, 4, 5-6, 7-13, 14+ by built area, on the box (Open Buildings 2.5D); the whole LGA is 64/32/2/1/1/0/0
        "h_bands": [0.4011, 0.5445, 0.0467, 0.0055, 0.0021, 0.0001, 0.0],
        "cross_every": {"p25": p50 * 0.8, "p50": p50, "p75": p50 * 1.233, "lo": p50 * 0.633, "hi": p50 * 1.6},
        # calibration knobs, tuned by sweeping seeds until the metrics sit between the real typical and dense squares (see the study doc)
        "x_junction": 0.1, "cross_scale": 2.2, "dead_end": 0.7,
        "sector_split_ha": 25,
        "spurs": {"spur_every_m": 150, "spur_m": [30, 70]},   # real dead ends 0.21-0.42 per junction
        "size_lo_u": 0.45, "plot_u": [0.4, 0.95], "back_row": 0.3, "big_front": 0.05, "vacant": 0.27,   # real typical house 160-167 m2, 1,090-1,263 per km2
        "internal_mains": 2, "t_into_done": True, "continue_mains": True,
        # the garage roundabout where the two mains meet, with the invented founder's statue on its island
        "roundabout": {"poi": "Hunter Roundabout", "r_m": 22, "strip_m": 0, "name": "Hunter Roundabout"},
        # the ferry jetty where the ferries from the Heights and Water Town come in, and the fish market's own jetty for the canoes
        "jetty": [{"poi": "Ferry Jetty", "name": "Ferry Jetty", "m": 40, "ferry": True},
                  {"poi": "Shore Fish Market", "name": "Fish Market Jetty", "m": 30, "pin": False}],
        "fish_market": {"poi": "Shore Fish Market", "smoke_share": 0.3},   # a third of its stalls are smoking racks
        "name_endings": ends,
        "parcels": [
            {"kind": "market", "poi": "Shore Fish Market", "ha": 1.2, "near": "shore", "near_main": False},
            # the barge yard: half-built barges on the slipway and a workshop shed
            {"kind": "barge yard", "poi": "Barge Yard", "ha": 1.5, "near": "shore", "near_main": False, "gate": "nearest",
             "buildings": [["barge", [32, 8], [-0.35, -0.35]], ["barge", [32, 8], [-0.35, 0.3]], ["barge", [26, 7], [0.35, 0.3]], ["shed", [16, 10], [0.55, -0.45]]]},
            # the old town king's palace (sacred list: never a crime site)
            {"kind": "palace", "poi": "Shore Palace", "ha": 0.5, "near_main": False, "gate": "nearest", "min_w": 55,
             "buildings": [["palace", [30, 16], [0.0, 0.25]], ["back", [14, 6], [0.55, -0.55]], ["back", [14, 6], [-0.55, -0.55]]],
             "grounds": [["forecourt", [22, 14], [0.0, -0.45]]]},
            {"kind": "motor park", "ha": round(LM["bus_stations"]["area_m2"]["p50"] / 1e4, 2) if LM.get("bus_stations", {}).get("n") else 0.4, "near": "roundabout", "near_main": True},   # the garage
            {"kind": "school", "ha": 1.0, "near_main": False, "gate": "nearest", "min_w": 60},
            {"kind": "pitch", "ha": 0.15, "near_main": False},
        ],
        "walled": ["palace", "barge yard"],
        # the Old Quarter: low old houses with corrugated roofs round the pin (the district model's "low-rise old town")
        "zone": {"poi": "Old Quarter", "r_m": 140, "kind": "old house", "min_m2": 40, "storeys": [1, 1], "kiosk_every_m": 1000},
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "clear_access": True,
    }

def profile(did, ST):
    f = f"study-{did}-landmarks.json"
    LM = json.load(open(f)) if os.path.exists(f) else {}
    return {"hub": hub, "maze": maze, "jungle": jungle, "foodgate": foodgate, "watertown": watertown, "capital": capital, "bazaar": bazaar, "port": port, "railside": railside, "estate": estate, "oldisland": oldisland, "heights": heights, "frontier": frontier, "oldshore": oldshore}.get(did, lambda ST, LM: {})(ST, LM)
