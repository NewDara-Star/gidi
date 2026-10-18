"""The rules: from what the data knows about an object to how it looks.

An object's attributes (kind, storeys, district, distance to a main road, frontage, ...) choose
its archetype and every part's spec. All numbers live in the tables below so research can
tune them without touching the builders. Sources and reasoning: docs/LAGOS-LOOK.md.
"""
from .core import hex_rgb, shade

# ---------------------------------------------------------------- districts -> character
# A district's real inspiration decides its character, which sets palettes, wear and wealth.
CHARACTER = {
    'maze': 'dense', 'hub': 'dense', 'jungle': 'dense', 'foodgate': 'dense', 'bazaar': 'dense',
    'railside': 'sprawl', 'frontier': 'sprawl', 'border': 'sprawl',
    'oldisland': 'old_island', 'oldshore': 'old_island',
    'estate': 'elite', 'heights': 'elite',
    'capital': 'civic', 'watertown': 'waterfront', 'port': 'port',
}

# Share of buildings left unfinished, from docs/LAGOS-ISMS.md (#8), per district's real inspiration.
UNFINISHED_SHARE = {
    'maze': 0.006, 'hub': 0.011, 'jungle': 0.004, 'foodgate': 0.0, 'watertown': 0.002, 'capital': 0.0,
    'bazaar': 0.014, 'port': 0.014, 'railside': 0.041, 'estate': 0.001, 'oldisland': 0.0, 'heights': 0.0,
}

# Share of the real inspiration's land below 3 m (docs/LAGOS-ISMS.md, from the LGA DEM): floods, wet roads.
FLOOD = {'maze': 0.08, 'hub': 0.09, 'jungle': 0.45, 'foodgate': 0.57, 'watertown': 0.55, 'capital': 0.0, 'bazaar': 0.32,
         'port': 0.48, 'railside': 0.03, 'estate': 0.2, 'oldisland': 0.97, 'heights': 0.54, 'frontier': 0.5, 'border': 0.4, 'oldshore': 0.4}
# The street kit per character: drain size and cover, wire tangle, litter, kerb paint, poles of timber.
STREET = {
    'dense': dict(drain=(0.5, 0.45), cover=0.3, rubbish=0.6, drops=(2, 4), litter=1.0, kerb='yellow', wood_pole=0.15, heaps=1.0, bumps=0.3),
    'sprawl': dict(drain=(0.5, 0.45), cover=0.25, rubbish=0.5, drops=(1, 3), litter=0.7, kerb='grey', wood_pole=0.1, heaps=0.8, bumps=0.3),
    'old_island': dict(drain=(0.45, 0.5), cover=0.4, rubbish=0.6, drops=(2, 4), litter=1.0, kerb='white', wood_pole=0.35, heaps=0.8, bumps=0.2),
    'elite': dict(drain=(0.45, 0.45), cover=0.92, rubbish=0.05, drops=(0, 1), litter=0.05, kerb='white', wood_pole=0.0, heaps=0.0, bumps=1.0),
    'civic': dict(drain=(0.6, 0.5), cover=0.6, rubbish=0.3, drops=(1, 2), litter=0.4, kerb='yellow', wood_pole=0.0, heaps=0.3, bumps=0.4),
    'waterfront': dict(drain=(0.5, 0.4), cover=0.1, rubbish=0.8, drops=(1, 3), litter=1.3, kerb='grey', wood_pole=0.4, heaps=1.5, bumps=0.1),
    'port': dict(drain=(0.9, 0.8), cover=0.4, rubbish=0.6, drops=(1, 2), litter=1.0, kerb='yellow', wood_pole=0.1, heaps=1.2, bumps=0.1),
}

# ---------------------------------------------------------------- per character
C = {
    'dense': dict(
        wear=(0.45, 0.85), wealth=(0.1, 0.45),
        paints={'#efe2c4': 4, '#f3c9a0': 3, '#bcd9e6': 3, '#c8e3c0': 3, '#f0d27a': 2, '#f4f1ea': 3, '#e9b3ad': 2, '#d3c8ea': 1, '#bfe5dc': 1},
        trims={'#ffffff': 4, '#2f6fae': 1, '#c4512e': 1, '#2f7d55': 1, '#3a3a3a': 1},
        roof_cols={'#a7b0b5': 5, '#9c3a26': 2, '#2f5f8f': 2, '#2f6b45': 1, '#6b4a33': 1},
        flat_roof_p={1: 0.08, 2: 0.5, 3: 0.75, 4: 0.95},
        window={'louvre': 6, 'casement': 2, 'sliding': 2}, bars_p=0.85,
        bar_patterns={'vertical': 4, 'diamond': 2, 'grid': 2, 'sunray': 1.5, 'scroll': 1},
        bar_cols={'#262626': 5, '#2f6b45': 2, '#7a2a2a': 2, '#2c4f7a': 1, '#d9d9d9': 1},
        balcony_p=0.35, rail={'balusters': 1, 'steel': 2}, compound_p=0.3, wall_top={'bottles': 3, 'plain': 2, 'razor': 1},
        shop_p=0.7, hand_sign_p=0.75, tank_p=0.6, dish_p=0.3, gen_p=0.4, roof_tyres_p=0.35, mixed_sheets_p=0.4,
        profile={'sine': 3, 'trapezoid': 1}),
    'sprawl': dict(
        wear=(0.35, 0.75), wealth=(0.15, 0.5),
        paints={'#f1e6cc': 4, '#f3d0a8': 3, '#cfe0e8': 2, '#d6ead0': 2, '#f2dc8c': 2, '#f6f3ec': 3, '#eab9b2': 1},
        trims={'#ffffff': 4, '#2f6fae': 1, '#8a2f2f': 1, '#3a3a3a': 1},
        roof_cols={'#a7b0b5': 3, '#8f3a2a': 3, '#2f5f8f': 2, '#2f6b45': 2},
        flat_roof_p={1: 0.05, 2: 0.4, 3: 0.7, 4: 0.9},
        window={'louvre': 4, 'casement': 2, 'sliding': 3}, bars_p=0.8,
        bar_patterns={'vertical': 3, 'diamond': 2, 'grid': 2, 'sunray': 2, 'scroll': 1},
        bar_cols={'#262626': 4, '#2f6b45': 2, '#7a2a2a': 2, '#d9d9d9': 1},
        balcony_p=0.3, rail={'balusters': 2, 'steel': 1}, compound_p=0.55, wall_top={'bottles': 2, 'plain': 2, 'razor': 1},
        shop_p=0.6, hand_sign_p=0.7, tank_p=0.55, dish_p=0.35, gen_p=0.45, roof_tyres_p=0.2, mixed_sheets_p=0.25,
        profile={'sine': 1, 'trapezoid': 2}),
    'old_island': dict(
        wear=(0.5, 0.9), wealth=(0.15, 0.5),
        paints={'#e8c98a': 3, '#c9dcc0': 2, '#e6b8a8': 2, '#b9d0e0': 2, '#efe6d2': 3, '#d8a86a': 1},
        trims={'#ffffff': 5, '#2f5f4a': 1, '#7a3a2a': 1},
        roof_cols={'#9aa3a8': 3, '#8f3a2a': 3, '#5a4a3a': 1},
        flat_roof_p={1: 0.1, 2: 0.4, 3: 0.7, 4: 0.9},
        window={'louvre': 3, 'casement': 5, 'sliding': 1}, bars_p=0.75,
        bar_patterns={'vertical': 3, 'scroll': 3, 'sunray': 2, 'grid': 1},
        bar_cols={'#262626': 4, '#2f5f4a': 2, '#7a2a2a': 2},
        balcony_p=0.5, rail={'balusters': 3, 'steel': 1}, compound_p=0.1, wall_top={'plain': 2, 'bottles': 1},
        shop_p=0.8, hand_sign_p=0.7, tank_p=0.5, dish_p=0.3, gen_p=0.35, roof_tyres_p=0.2, mixed_sheets_p=0.4,
        profile={'sine': 3, 'trapezoid': 1}),
    'elite': dict(
        wear=(0.05, 0.3), wealth=(0.7, 1.0),
        paints={'#f6f4ef': 5, '#e9e4d8': 3, '#d9d6cf': 2, '#efe0c6': 2, '#cfd8dc': 1},
        trims={'#ffffff': 3, '#3a3a3a': 2, '#8a6a4a': 1},
        roof_cols={'#3d4448': 3, '#6b2f2a': 2, '#2c4f7a': 2, '#5a4a3a': 1, '#2f5f45': 1},
        flat_roof_p={1: 0.2, 2: 0.3, 3: 0.5, 4: 0.8},
        window={'sliding': 6, 'casement': 3, 'louvre': 0.5}, bars_p=0.4,
        bar_patterns={'vertical': 3, 'scroll': 2, 'grid': 1},
        bar_cols={'#262626': 5, '#ffffff': 1, '#8a6a4a': 1},
        balcony_p=0.6, rail={'balusters': 3, 'steel': 2}, compound_p=0.95, wall_top={'razor': 3, 'plain': 2},
        shop_p=0.1, hand_sign_p=0.1, tank_p=0.7, dish_p=0.5, gen_p=0.2, roof_tyres_p=0.0, mixed_sheets_p=0.0,
        profile={'trapezoid': 1}),
    'civic': dict(
        wear=(0.2, 0.5), wealth=(0.4, 0.7),
        paints={'#f3eee2': 4, '#efe0c0': 3, '#d8e6ec': 2, '#e9ecef': 2},
        trims={'#ffffff': 3, '#2f5f8f': 1, '#3a3a3a': 1},
        roof_cols={'#9aa3a8': 2, '#8f3a2a': 2, '#2c4f7a': 2, '#3d4448': 1},
        flat_roof_p={1: 0.2, 2: 0.5, 3: 0.75, 4: 0.95},
        window={'sliding': 4, 'casement': 2, 'louvre': 2}, bars_p=0.6,
        bar_patterns={'vertical': 3, 'grid': 2, 'diamond': 1},
        bar_cols={'#262626': 4, '#2c4f7a': 1},
        balcony_p=0.3, rail={'steel': 2, 'balusters': 1}, compound_p=0.6, wall_top={'plain': 2, 'razor': 1},
        shop_p=0.5, hand_sign_p=0.35, tank_p=0.6, dish_p=0.35, gen_p=0.35, roof_tyres_p=0.05, mixed_sheets_p=0.1,
        profile={'trapezoid': 2, 'sine': 1}),
}
C['waterfront'] = dict(C['dense'], wear=(0.6, 0.95), wealth=(0.0, 0.25), compound_p=0.05, shop_p=0.4, balcony_p=0.1)
C['port'] = dict(C['dense'], wear=(0.55, 0.9), compound_p=0.4)

SHOP_NAMES = ["GOD'S GRACE VENTURES", 'BLESSED HANDS\nMOTOR SPARES', 'CHUKS & SONS\nAUTO PARTS', 'NO WEAPON SHALL\nPROSPER ENT.',
              'EMEKA ELECTRICALS', 'TRUST IN GOD\nBATTERIES', 'IYA BASIRAT\nPROVISIONS', 'UNIQUE TOUCH\nFASHION HOME', 'MIGHTY GRACE\nWELDING WORKS',
              'ADUNNI HAIR\nSTUDIO', 'DIVINE FAVOUR\nVULCANISER', 'PHONE REPAIRS\n& ACCESSORIES', 'OLUWASEUN\nCHEMIST', 'AJE BUTTER\nBARBING SALON']
SIGN_PAIRS = [('#1f5fa8', '#ffffff'), ('#f2c21b', '#1a1a1a'), ('#c8322b', '#ffffff'), ('#2d7d46', '#ffffff'), ('#ffffff', '#c8322b'), ('#f08a24', '#1a1a1a')]


def _c(rng, table):
    return hex_rgb(rng.pick(table))


def compound_spec(character, rng):
    """How a compound wall from the data looks, by the district's character (the same ranges the houses' own walls used)."""
    ch = C.get(character, C['dense'])
    wealth = rng.between(*ch['wealth'])
    return dict(h=rng.between(1.9, 2.6) + 0.6 * wealth, paint=_c(rng, ch['paints']), coping=hex_rgb('#f2efe6'), top=rng.pick(ch['wall_top']),
                gate=_c(rng, {'#2b4a66': 2, '#3a3a3a': 2, '#7a2a2a': 1, '#2e6b4a': 1}), wear=rng.between(*ch['wear']), gap=rng.between(1.6, 3.0))


# A district's own colours, measured from the Google Earth study of the places it is drawn from (study yes, lift no: only the
# numbers). They override its character's. The Maze, from Mushin and Shomolu close up (18 Oct 2026): rusty zinc most of all,
# grey zinc, a painted roof now and then; dusty cream, off-white and bare block walls, a few faded pastels.
DISTRICT_LOOK = {
    'maze': dict(
        roof_cols={'#6e4f40': 5, '#7c5c4b': 4, '#5b4237': 3, '#8f8a84': 3, '#a49c93': 2, '#4a63a0': 0.6, '#9c4a36': 0.4, '#4b6b55': 0.3},
        paints={'#cdbba2': 4, '#d8cfbf': 3, '#b7a58e': 2, '#9d968b': 2, '#c9b8a8': 1, '#b9c2c0': 1, '#c7c19a': 1},
        trims={'#ffffff': 2, '#3a3a3a': 2, '#2f5f8f': 1, '#7a3b2a': 1},
        mixed_sheets_p=0.6, wear=(0.55, 0.9)),
}


def house_spec(a, rng):
    """Everything about a house's look, from its attributes `a`:
    kind, storeys, district, near_main (m), frontage (m to the street it faces)."""
    ch = dict(C[CHARACTER.get(a['district'], 'dense')], **DISTRICT_LOOK.get(a['district'], {}))
    s = a['storeys']
    wealth = rng.between(*ch['wealth']) + (0.15 if a.get('near_main', 99) < 25 else 0) + 0.05 * (s - 1)
    wear = min(1.0, max(0.0, rng.between(*ch['wear']) - 0.25 * (wealth - 0.3)))
    paint = _c(rng, ch['paints'])
    trim = _c(rng, ch['trims'])
    unfinished = a.get('unfinished', False)
    flat = rng.chance(ch['flat_roof_p'].get(min(s, 4), 0.9)) or unfinished or len(a['poly']) != 4  # pitched roofs need a quad
    H = a.get('house')   # the data's roof, tank, dish and tyres (scripts/houses.py): the draws still happen, so the looks stay put
    if H is not None:
        flat = bool(H['flat']) or len(a['poly']) != 4
    win_type = rng.pick(ch['window'])
    if wealth > 0.6 and win_type == 'louvre':
        win_type = 'sliding'
    bars = rng.pick(ch['bar_patterns']) if rng.chance(ch['bars_p']) else 'none'
    spec = dict(
        storeys=s, wealth=wealth, wear=wear, paint=paint, trim=trim, chamfer=0.18,
        plinth=shade(paint, 0.55) if rng.chance(0.5) else hex_rgb(rng.pick({'#6b6b66': 2, '#7a4a2e': 1, '#2f4f6f': 1})),
        bare=False, unfinished=unfinished,
        window=dict(type=win_type, w=rng.pick([0.9, 1.0, 1.2]) if win_type != 'sliding' else 1.4, h=1.2,
                    frame=trim if win_type != 'sliding' else hex_rgb('#b8bcc0'), glass=hex_rgb(rng.pick({'#24343e': 3, '#2c4a3a': 1, '#3a4652': 1})),
                    mullion=hex_rgb('#b8bcc0'), bars=bars, bar_col=_c(rng, ch['bar_cols']), wear=wear, hood=rng.chance(0.3)),
        bay=rng.between(2.4, 3.0),
        door=dict(frame=trim, door=_c(rng, {'#2f5d8a': 2, '#8a2f2f': 2, '#2e6b4a': 2, '#3a3a3a': 2, '#6b4a2e': 1}), wear=wear),
        roof=dict(form='flat') if flat else dict(
            form=rng.pick({'gable': 3, 'hip': 2 + 3 * wealth}), pitch_deg=rng.between(14, 24), overhang=rng.between(0.35, 0.6),
            profile=rng.pick(ch['profile']), col=_c(rng, ch['roof_cols']), col2=_c(rng, ch['roof_cols']), mixed=rng.chance(ch['mixed_sheets_p']),
            wear=min(1, wear + rng.between(0, 0.25)), wall_wear=wear, gable_col=paint, fascia=trim, fascia_wood=rng.chance(0.4)),
        parapet=dict(parapet_h=rng.between(0.6, 1.0), paint=paint, trim=trim, slab=hex_rgb('#8f8a80'), wear=wear),
        balcony_p=ch['balcony_p'] if s > 1 else 0,
        bal_faces=a['front']['bal'] if a.get('front') else None,   # the data's balconies (scripts/fronts.py): only where they clear neighbours and roads
        balcony=dict(slab=hex_rgb('#c9c3b6'), rail=rng.pick(ch['rail']), rail_col=trim if rng.chance(0.6) else paint, wear=wear),
        shop=a['front']['shop'] if a.get('front') else (a['kind'] == 'front' and a.get('frontage', 99) < 9 and rng.chance(ch['shop_p']) and not a.get('walled')),   # the data decides (scripts/fronts.py)
        shutter=dict(col=_c(rng, {'#9aa3a8': 3, '#2f6fae': 1, '#2e7d4f': 1, '#c0c4c6': 2}), open=rng.between(0.4, 0.9), wear=wear),
        sign=None,
        compound=None,
        tank=dict(r=rng.pick([0.55, 0.7, 0.85]), h=rng.pick([1.1, 1.4, 1.7]), stand=rng.between(0.8, 1.6), col=_c(rng, {'#1d1d1d': 5, '#2f5f9f': 2, '#2f6b45': 1}), wear=wear) if rng.chance(ch['tank_p']) else None,
        dish=rng.chance(ch['dish_p']), generator=dict(col=_c(rng, {'#c62828': 2, '#2e7d32': 2, '#f9a825': 2, '#37474f': 1}), wear=wear) if rng.chance(ch['gen_p']) else None,
        roof_tyres=rng.chance(ch['roof_tyres_p']),
    )
    if H is not None:
        if H['tank'] and not spec['tank']:
            spec['tank'] = dict(r=0.7, h=1.4, stand=1.2, col=hex_rgb('#1d1d1d'), wear=wear)
        if not H['tank']:
            spec['tank'] = None
        spec['tank_at'] = H['tank'] or None
        spec['dish'], spec['dish_at'] = bool(H['dish']), H['dish'] or None
        spec['generator'] = None   # a thing in the data, drawn with the other things
        spec['roof_tyres'] = H['tyres']
    if spec['roof']['form'] != 'flat':  # corrugated zinc: 76 mm sine; long-span aluminium: ~200 mm trapezoid ribs
        sine = spec['roof']['profile'] == 'sine'
        spec['roof'].update(pitch=0.076 if sine else 0.2, depth=0.018 if sine else 0.032)
    if spec['shop']:
        bg, fg = SIGN_PAIRS[rng.randrange(len(SIGN_PAIRS))]
        hand = rng.chance(ch['hand_sign_p'])
        spec['sign'] = dict(text=rng.pick(SHOP_NAMES), bg=hex_rgb(bg), fg=hex_rgb(fg), hand=hand, wear=wear if hand else wear * 0.4,
                            phone='080' + str(rng.randrange(3, 9)) + ' ' + str(rng.randrange(100, 999)) + ' ' + str(rng.randrange(1000, 9999)),
                            wobble=rng.between(-0.03, 0.03) if hand else None)
        aw = a['front']['aw'] if a.get('front') else (rng.between(1.2, 1.8) if rng.chance(0.5) else 0)   # the data's canopy depth, clear of the road
        spec['awning'] = dict(depth=aw, col=spec['roof']['col'] if not flat else _c(rng, ch['roof_cols']), wear=min(1, wear + 0.1)) if aw else None
    if rng.chance(ch['compound_p']) and a['kind'] != 'shed' and not spec['shop']:  # shops open straight onto the street
        spec['compound'] = dict(h=rng.between(1.9, 2.6) + 0.6 * wealth, paint=_c(rng, ch['paints']), coping=trim, top=rng.pick(ch['wall_top']),
                                gate=_c(rng, {'#2b4a66': 2, '#3a3a3a': 2, '#7a2a2a': 1, '#2e6b4a': 1}), wear=wear, gap=rng.between(1.6, 3.0))
    return spec
