# Per-district settings for gen_fabric.py. Each number says where it comes from.
# The Maze has no profile: the generator keeps its original (v1) behaviour for it, so the finished Maze can be reproduced.
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
             "bowl_m2": LM["stadium"]["bowl_building_m2"][0], "storeys": 4},
        ],
        # smaller places taken from finished blocks, as in the Maze
        "parcels": [
            {"kind": "motor park", "poi": "Boss's motor park", "ha": LM["bus_stations"]["area_m2"]["p75"] / 1e4, "near_main": True},
            {"kind": "industrial", "ha": "from_study", "cap_ha": 3.0, "near": "rail_far_from_knot", "near_main": True},
            {"kind": "school", "ha": round(ST["landuse_polygons_ha"]["school"][1] / ST["landuse_polygons_ha"]["school"][0], 2), "near_main": False},   # real mean school compound
            {"kind": "pitch", "ha": round(ST["landuse_polygons_ha"]["pitch"][1] / ST["landuse_polygons_ha"]["pitch"][0], 2), "near_main": False},     # real mean pitch
        ],
        "hotel": _hotel("Stadium Highlife Hotel", LM),
    }

def profile(did, ST):
    f = f"study-{did}-landmarks.json"
    LM = json.load(open(f)) if os.path.exists(f) else {}
    return {"hub": hub}.get(did, lambda ST, LM: {})(ST, LM)
