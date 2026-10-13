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
        "lock": {"reserve": ["Ladi Lane Parts Market"], "buildings": ["The steal", "Tunde's room"]},   # the opening, fixed for good (web/locked.json)
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
            {"kind": "school", "ha": round(LM["school_m2"]["p50"] / 1e4, 2), "near_main": False},
            {"kind": "pitch", "ha": round(LM["pitch_m2"]["p50"] / 1e4, 2), "near_main": False},
        ],
        "hotel": {"poi": "Ireti Hotel", "m2": ST["buildings"]["footprint_m2"]["p90"], "storeys": 3},   # "tiny hotels": a big house's footprint (p90), 3 storeys; no hotels mapped
        "named": [{"poi": "Jahman Sound Studio", "kind": "studio", "from": ["front"]},
                  {"poi": "Network Plus Café", "kind": "cafe", "from": ["front"]}],
        "canal_footbridges": 1,
        "walk": {"rail_path_m": 4.5, "cross_every_m": [150, 200]},
        "fence_parcels": True, "rail_frontage": True,
        "clear_access": True,           # living test (Oct 2026): streets join the market's own road instead of running beside it
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
    }

def profile(did, ST):
    f = f"study-{did}-landmarks.json"
    LM = json.load(open(f)) if os.path.exists(f) else {}
    return {"hub": hub, "maze": maze, "jungle": jungle, "foodgate": foodgate, "watertown": watertown}.get(did, lambda ST, LM: {})(ST, LM)
