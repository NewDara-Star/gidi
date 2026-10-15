# Deep study, step 3: the study of a district (docs/data/deep/<id>.json) as a page a designer can read, ending in the targets its
# generator profile has to hit. Usage: python3 scripts/deep_report.py [ids...]   -> docs/studies/<id>.md
import json, os, sys

NAMES = {'border': 'The Border', 'bazaar': 'The Bazaar', 'jungle': 'Jungle City', 'port': 'The Port', 'maze': 'The Maze', 'hub': 'The Hub',
         'railside': 'Railside', 'capital': 'The Capital', 'estate': 'The Estate', 'foodgate': 'Food Gate', 'watertown': 'Water Town',
         'oldshore': 'Old Shore', 'oldisland': 'Old Island', 'heights': 'The Heights', 'frontier': 'The Frontier', 'airport': 'The Airport',
         'yaba': 'The Campus'}
INFO = json.load(open('web/districts_info.json'))
pc = lambda v: f'{round(100 * v)}%'


def page(did):
    J = json.load(open(f'docs/data/deep/{did}.json'))
    B, Hh, St, Q, P = J['buildings'], J['heights'], J['streets'], J.get('structure_built_squares') or {}, J['places']
    q = lambda k: (Q.get(k) or {}).get('median') if isinstance(Q.get(k), dict) else Q.get(k)
    L = [f"# {NAMES[did]}: the deep study", '',
         f"Inspired by {INFO.get(did, {}).get('inspired', '?')}. Study area: {J['area_km2']} km², {J['land_km2']} km² of it land. "
         f"Made by `scripts/study_deep.py` from Google's buildings and heights, Microsoft's buildings, OpenStreetMap, Overture, WorldCover, WorldPop "
         f"and Copernicus. Gidi takes numbers from this, never an outline, a name or an image.", '',
         f"![{did}](../img/study-{did}.png)", '',
         '## The sources', '',
         f"- **Google** traced {J['sources']['google_all']:,} buildings here; {J['sources']['google_conf70']:,} are confident enough to use (70% or more).",
         f"- **Microsoft** has {J['sources']['microsoft']:,} and **OpenStreetMap** {J['sources']['osm']:,}. Google is the base for every building number below.",
         '- **Places** come from Overture (mostly Google Maps-style listings). They cluster where people map, along main roads, so read them as a floor and a pattern, not a count.',
         '- **Street things** (lamps, signals, bus stops) are badly under-mapped in Lagos. The real numbers are far higher.', '',
         '## The ground and the land', '',
         f"- **Land cover:** {', '.join(f'{k} {pc(v)}' for k, v in sorted(J['land_cover'].items(), key=lambda kv: -kv[1]) if v >= 0.005)}.",
         f"- **Ground height:** median {J['ground']['height_m']['p50']} m, from {J['ground']['height_m']['p10']} m to {J['ground']['height_m']['p90']} m; "
         f"{pc(J['ground']['below_3m_share'])} of the land is below 3 m (flood-prone). Slopes: median {J['ground']['slope_deg']['p50']}°, steepest tenth {J['ground']['slope_deg']['p90']}°.",
         f"- **Water (OSM):** {', '.join(f'{k} {v} km' for k, v in J['osm']['waterways_km'].items()) or 'none mapped'}.",
         f"- **Mapped land use:** {', '.join(f'{k} {pc(v)}' for k, v in list(J['land_use_mapped_share'].items())[:8]) or 'none'}.",
         f"- **People:** about {J['people']['total']:,} ({J['people']['per_km2_land']:,.0f} per km² of land), {J['people']['per_building']} per building, "
         f"{J['people']['per_100m2_floor']} per 100 m² of floor.", '',
         '## The buildings', '',
         f"- **{B['per_km2_land']:,.0f} per km²** over all the land, covering {pc(B['cover_land'])} of it. In the built-up squares: "
         f"**{q('per_km2'):,.0f} per km²**, covering **{pc(q('cover'))}**." if q('per_km2') else f"- {B['per_km2_land']:,.0f} per km² over all the land.",
         f"- **Sizes:** half are under {B['size_m2']['p50']:.0f} m²; a quarter under {B['size_m2']['p25']:.0f} m²; a tenth over {B['size_m2']['p90']:.0f} m². "
         f"By band: {', '.join(f'{k} m² {pc(v)}' for k, v in B['size_bands_share'].items())}.",
         f"- **Shape:** long side median {B['long_side_m']['p50']} m; length to width {B['aspect']['p50']} (a tenth longer than {B['aspect']['p90']}).",
         f"- **Touching:** {pc(B['touching_share'])} of buildings are within a metre of another (shared or nearly shared walls). Nearest gap: median {B['nearest_gap_m']['p50']} m, a tenth over {B['nearest_gap_m']['p90']} m.",
         f"- **Grain:** {pc(B['orientation_share_within_10deg_of_peak'])} of the built area lines up within 10° of one direction.",
    ]
    if Q:
        L += [f"- **Along the streets** (the built squares): the street front is {pc(q('front_occupied'))} occupied; gaps between front buildings median {Q.get('front_gap_m.median')} m "
              f"({pc(Q.get('front_gap_m.share_under_3m', 0))} under 3 m). Buildings sit {Q.get('line_deg.median')}° off square to the street "
              f"({pc(Q.get('line_deg.share_within_10deg', 0))} within 10°). Setback, centre line to front: median {Q.get('setback_m.median')} m.",
              f"- **Blocks:** {pc(Q.get('block_fill.median', 0))} of a block's land is built. Edge band (20 m from the street) {pc(q('edge_cover'))} built, the back {pc(q('back_cover'))}."]
    L += ['', '## Heights', '',
          f"- **Storeys:** {', '.join(f'{k}{"+" if k == "8" else ""}: {pc(v)}' for k, v in Hh['storeys_share'].items() if v >= 0.005)}.",
          f"- **By size:** {', '.join(f'{k} → {v}' for k, v in Hh['storeys_by_size'].items())} (median storeys).",
          f"- **Tall (7+ storeys):** {Hh['tall_7plus_per_km2']} per km². Floor area over land: {Hh['floor_area_ratio_land']}.",
          f"- Heights are Google's 2023 estimates (about 3 m a storey; a pitched zinc roof on a high plinth can read as two storeys).", '',
          '## The streets', '',
          f"- **{St['drivable_km_per_km2']} km of drivable street per km²**, {St['main_km_per_km2']} of it main road. By class: {', '.join(f'{k} {v}' for k, v in St['km_per_km2_land'].items() if v >= 0.05)}.",
          f"- **Junctions:** {St['junctions_per_km2']} per km², {pc(St['T_share'])} of them T's, {pc(St['four_plus_share'])} crossroads. Dead ends: {St['dead_ends_per_km2']} per km².",
          f"- **Blocks:** median {St['block_ha']['p50']} ha (a quarter under {St['block_ha']['p25']} ha, a tenth over {St['block_ha']['p90']} ha). Street lengths between junctions: median {St['segment_m']['p50']} m.",
          f"- **Grain:** {'a grid' if St['grain_entropy'] < 0.85 else 'mixed directions' if St['grain_entropy'] < 0.95 else 'every direction (organic)'} (entropy {St['grain_entropy']}).",
          f"- **Surfaces mapped:** {', '.join(f'{k} {v} km' for k, v in list(St['surface_km'].items())[:6])}.",
          f"- **Bridges and flyovers:** {St['bridge_m']:,.0f} m. Rail: {St['rail_km']} km. Footpaths: {St['paths_km_per_km2']} km per km².", '',
          '## Places', '',
          f"- **{P['total_per_km2']} mapped places per km².** By kind (per km²): {', '.join(f'{k} {v}' for k, v in P['by_kind_per_km2'].items())}.",
          f"- **On the main roads** (within 40 m): {', '.join(f'{k} {pc(v)}' for k, v in P['share_within_40m_of_main_road'].items())}.",
          f"- **Most common listings:** {', '.join(f'{k} ({v})' for k, v in P['top_categories'][:15])}.",
          f"- **OSM markets:** {J['osm']['markets']} ({', '.join(f'{v} ha' for v in J['osm']['market_ha'])}).", '',
          '## Street things', '',
          f"- Per km²: {', '.join(f'{k} {v}' for k, v in list(J['street_things']['count_per_km2'].items())[:12]) or 'none mapped'}.",
          f"- Lines, km per km²: {', '.join(f'{k} {v}' for k, v in J['street_things']['km_per_km2'].items()) or 'none'}.", '',
          '## How it changes across the district', '',
          '| From a main road | Buildings / km² | Built over | Typical size | Mean storeys | Touching |', '|---|---|---|---|---|---|']
    L += [f"| {r['band_m']} m | {r['buildings_per_km2']:,.0f} | {pc(r['cover'])} | {r['size_m2_median']:.0f} m² | {r['storeys_mean']} | {pc(r['touching'])} |" for r in J['away_from_main_roads']]
    L += ['', '| From open water | Buildings / km² | Built over | Typical size | Mean storeys | Touching |', '|---|---|---|---|---|---|']
    L += [f"| {r['band_m']} m | {r['buildings_per_km2']:,.0f} | {pc(r['cover'])} | {r['size_m2_median']:.0f} m² | {r['storeys_mean']} | {pc(r['touching'])} |" for r in J['away_from_water']]
    if J.get('fabric_types'):
        L += ['', '## Fabric types inside the district', '',
              f"The built 250 m squares ({J['built_cells_250m']['cells']}) fall into these types (clustered on density, cover, size, touching, storeys, streets and places):", '',
              '| Type | Share | Buildings / km² | Built over | Typical size | Touching | Storeys | Street km / km² | Places / km² |', '|---|---|---|---|---|---|---|---|---|']
        L += [f"| {t['type']}. {t['name']} | {pc(t['share_of_built_cells'])} | {t['buildings_per_km2']:,.0f} | {pc(t['cover'])} | {t['size_m2_median']:.0f} m² | {pc(t['touching'])} | "
              f"{t['storeys_mean']} | {t['street_km_per_km2']} | {t['places_per_km2']:.0f} |" for t in J['fabric_types']]
    L += ['', '## The biggest buildings', '',
          '| Footprint | Storeys | Nearest listed place |', '|---|---|---|']
    L += [f"| {b['m2']:,} m² | {b['storeys']} | {(b['nearest_place'] or ['—', ''])[1] or '—'} |" for b in J['landmarks_biggest'][:12]]
    L += ['', '## Targets for the generator profile', '',
          'What Gidi\'s version should come out at (built squares unless marked). The check compares the built district with these.', '',
          '| Measure | Target |', '|---|---|']
    T = [('Buildings per km² (built squares, median; p25-p75)', f"{q('per_km2'):,.0f} ({Q['per_km2']['p25']:,.0f}-{Q['per_km2']['p75']:,.0f})" if Q else '—'),
         ('Ground built over', f"{pc(q('cover'))}" if Q else '—'), ('Touching', pc(q('touching')) if Q else '—'),
         ('Under 40 m²', pc(q('under_40m2')) if Q else '—'), ('Street front occupied', pc(q('front_occupied')) if Q else '—'),
         ('Block fill', pc(Q.get('block_fill.median', 0)) if Q else '—'),
         ('Footprint p25 / median / p90', f"{B['size_m2']['p25']:.0f} / {B['size_m2']['p50']:.0f} / {B['size_m2']['p90']:.0f} m²"),
         ('Storeys 1 / 2 / 3 / 4+', ' / '.join(pc(v) for v in [Hh['storeys_share']['1'], Hh['storeys_share']['2'], Hh['storeys_share']['3'],
                                                                 sum(Hh['storeys_share'][k] for k in '45678')])),
         ('Drivable streets', f"{St['drivable_km_per_km2']} km per km²"), ('Junctions; T share', f"{St['junctions_per_km2']} per km²; {pc(St['T_share'])}"),
         ('Dead ends', f"{St['dead_ends_per_km2']} per km²"), ('Block size median', f"{St['block_ha']['p50']} ha"),
         ('Churches / mosques / schools / health per km² (floor)', ' / '.join(str(P['by_kind_per_km2'].get(k, 0)) for k in ('church', 'mosque', 'school', 'health'))),
         ('People per building', str(J['people']['per_building']))]
    L += [f'| {a} | {b} |' for a, b in T]
    os.makedirs('docs/studies', exist_ok=True)
    open(f'docs/studies/{did}.md', 'w').write('\n'.join(L) + '\n')


for d in sys.argv[1:] or sorted(f[:-5] for f in os.listdir('docs/data/deep') if f.endswith('.json')):
    page(d)
    print('wrote docs/studies/' + d + '.md')
