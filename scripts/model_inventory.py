"""What is to be modelled, and where each thing stands (owner, 26 Oct: "get a proper inventory of the items that are
supposed to be modeled"; DECISIONS "Working first, polish later").

  ~/.venvs/gidi/bin/python scripts/model_inventory.py [--write]

For every record type the kit draws (schema `kit: true`) and every kind of it in the map's districts: how many there are,
the gidi-game builder that makes it, and whether the Unreal street test places it (built, a stand-in, or not at all).
Read from the files, not kept by hand: the map (map/d*/plan.json), the schema, gidi-game's builders (tools/*_build.py),
schema/kit_reads.json (which builder reads which record), gidi-game tools/street_test.py (THINGS: what the street test
places besides the houses) and Content/Python/gidi_street.py (HERO, STAND_IN: the vehicles). A kind counts as built when
its name appears in its builder's source (a builder with no kinds of its own builds every kind). --write writes
docs/MODEL-INVENTORY.md; without it, prints.
"""
import ast
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.expanduser('~/gidi-game')
OUT = os.path.join(ROOT, 'docs', 'MODEL-INVENTORY.md')


def assigned(path, name):
    """A module-level literal (tuple or dict) from a gidi-game file, read without importing it (they need Unreal)."""
    for node in ast.parse(open(path).read()).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit(f'{name} not found in {path}')


def main():
    schema = json.load(open(os.path.join(ROOT, 'schema', 'map_schema.json')))
    kit = [k for k, v in schema['records'].items() if v.get('kit')]
    reads = json.load(open(os.path.join(ROOT, 'schema', 'kit_reads.json')))['parts']
    builders_of = collections.defaultdict(list)            # record type -> builders that read it
    for part in reads:
        b, rec = part.split('.')
        builders_of[rec].append(b)
    source = {os.path.basename(p)[:-len('_build.py')]: open(p).read() for p in glob.glob(os.path.join(GAME, 'tools', '*_build.py'))}
    things = set(assigned(os.path.join(GAME, 'tools', 'street_test.py'), 'THINGS')) | {'block'}
    street = os.path.join(GAME, 'Content', 'Python', 'gidi_street.py')
    hero, stand_in = assigned(street, 'HERO'), assigned(street, 'STAND_IN')
    heroes = os.path.join(GAME, 'Content', 'Python', 'gidi_heroes.py')   # each hero's folder under Art/Vehicles
    folder = dict(re.findall(r"'(\w+)': \{'folder': '(\w+)'", open(heroes).read()))

    count = collections.Counter()
    for f in sorted(glob.glob(os.path.join(ROOT, 'map', 'd*', 'plan.json'))):
        for r in json.load(open(f))['records']:
            if r.get('type') in kit:
                count[(r['type'], r.get('kind'))] += 1
    rows = []
    for rec in kit:
        kinds = sorted({k for (t, k) in count if t == rec}, key=lambda k: -count[(rec, k)]) or [None]
        for kind in kinds:
            n = count[(rec, kind)]
            hand = None
            if rec == 'vehicle':                            # a vehicle's builder is that kind's own: no kind to look for
                b = hero.get(kind, kind)
                bs = built = [b] if b in source else []
                if not bs and b in folder:                  # a hand-made model, not a builder
                    hand = f'hand model (Art/Vehicles/{folder[b]})'
                    built = [hand]
            else:
                bs = ['umbrella'] if (rec, kind) == ('stall', 'umbrella') else ['stall'] if rec == 'stall' else \
                    [b for b in builders_of.get(rec, []) if b in source]
                # a builder that switches on its record's kind must name this one; the rest build every kind (wires: the pole's)
                own_kinds = lambda b: rec in ('stall', 'furniture') and re.search(r"KIND (==|in) ", source[b])
                built = [b for b in bs if kind is None or not own_kinds(b) or f"'{kind}'" in source[b]]
            if rec == 'vehicle':
                unreal = 'yes' if kind in hero and built else ('stand-in (City Sample)' if kind in stand_in else 'no')
            else:
                unreal = 'yes' if built and any(b in things for b in built) else 'no'
            if not built:
                state = 'no builder' if not bs else f"builder has no '{kind}'"
            elif unreal == 'yes':
                state = 'working'
            else:
                state = 'built, not placed in Unreal' if unreal == 'no' else 'built, Unreal has a stand-in'
            names = [hand] if hand else [f'{b}_build' for b in (built or bs)]
            rows.append((rec, kind or '', n, ', '.join(names) or '-', unreal, state))

    tally = collections.Counter('builder lacks the kind' if r[5].startswith('builder has') else r[5] for r in rows if r[2])
    lines = ['# What is to be modelled', '',
             'WRITTEN by `scripts/model_inventory.py --write` (do not edit by hand): every record type the kit draws and every kind',
             'of it on the map, its gidi-game builder, and whether the Unreal street test places it. Owner, 26 Oct: models work first,',
             'look passes later (DECISIONS "Working first, polish later"). "Built" means the kind is named in its builder; it says',
             'nothing of how it looks. "In Unreal" is the street test (gidi-game tools/street_test.py), not yet the whole city.', '',
             'Kinds on the map now: ' + '; '.join(f'{k}: {v}' for k, v in sorted(tally.items())) + '.', '',
             '| record | kind | on the map | builder | in Unreal | state |', '|---|---|---|---|---|---|']
    lines += [f'| {a} | {b} | {c} | {d} | {e} | {f} |' for a, b, c, d, e, f in sorted(rows, key=lambda r: (r[2] == 0, r[0], -r[2]))]
    lines += ['', 'Record types with 0 on the map are not drawn in any district yet (the dress layer: faces, roof sheets, goods,',
              'posters, litter, people and the rest); their builders are listed so the gap is seen before they are drawn.', '']
    text = '\n'.join(lines)
    if '--write' in sys.argv:
        open(OUT, 'w').write(text)
        print(f'wrote {OUT}: {len(rows)} rows')
    else:
        print(text)


main()
