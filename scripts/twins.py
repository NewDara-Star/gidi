"""Every type in Gidi and its real twin (owner, 19 Oct 2026: "let's know what every type of item and building as well to the type of
surface, so we know we have a real life twin"). Reads the map (web/gidi-data.js) for the types and their counts, and web/twins.json
for the twins (kept by hand); writes docs/TWINS.md. New types in the map show up on the next run with no twin yet.

web/twins.json: {"<group>/<type>": {"twin": what it is in Lagos, "where": a real place it was seen (and coordinates if known),
"pics": [paths under ~/gidi-data/research/], "status": "green" once the owner has passed the model against the pictures}}.
Status: none = no twin yet; red = twin named, no picture; amber = pictures saved, studied; green = modelled and passed by the owner.
Pictures stay outside the repo (study yes, lift no).
Usage: python3 scripts/twins.py
"""
import json
import os
from collections import Counter

S = open('web/gidi-data.js').read()
G = json.loads(S[S.index('{'):S.rstrip().rstrip(';').rindex('}') + 1])
T = json.load(open('web/twins.json')) if os.path.exists('web/twins.json') else {}
RES = os.path.expanduser('~/gidi-data/research')


def flat(v):
    if isinstance(v, dict):
        for x in v.values():
            yield from flat(x)
    elif isinstance(v, list):
        for x in v:
            yield from flat(x)
    elif isinstance(v, str):
        yield v


groups = {
    'building': Counter(b[0] for d in G['buildings'].values() for b in d),
    'plot': Counter(p['kind'] for d in G['parcels'].values() for p in d),
    'road': Counter([a['cls'] for a in G['arterials']] + ['main'] * len(G['mains']) + list(flat(G.get('road_types', {})))),
    'road surface': Counter(flat(G.get('surfaces', {}))),
    'ground': Counter({k: 1 for k in ('mud', 'dirt', 'sand', 'grass', 'dry grass', 'puddles', 'litter', 'weeds', 'laterite')}),
    'market zone': Counter(z.get('kind') for z in G.get('encroach', [])),
    'deck': Counter(s['kind'] for s in G.get('structures', [])),
    'street item': Counter(f['kind'] for f in G.get('furniture', [])),
    'vehicle and thing': Counter(t.get('k', '').split(':')[0] for t in G.get('things', [])),
    'monument': Counter((m.get('model') or '').split(':')[0] for m in G.get('monuments', [])),
    'house detail': Counter({k: 1 for k in ('flat roof', 'unfinished top', 'water tank', 'satellite dish', 'tyres on the roof', 'generator')}),
    'tree': Counter(t[2] for d in G.get('trees', {}).values() for t in d if len(t) > 2),
    'gutter': Counter({k: 1 for k in ('open gutter', 'covered gutter', 'gutter crossing')}),
}
out = ['# Real twins: every type in Gidi and the real thing it comes from', '',
       'Made by `python3 scripts/twins.py` from the map and `web/twins.json` (the twins, kept by hand). Pictures live in',
       '`~/gidi-data/research/` (outside the repo). **none** = no twin yet; **red** = twin named, no picture; **amber** = pictures saved',
       'and studied; **green** = modelled and passed by the owner against the pictures.', '']
tot = Counter()
rows = []
for g, C in groups.items():
    rows.append(f'## {g.capitalize()}s' if not g.endswith('s') else f'## {g.capitalize()}')
    rows += ['', '| Type | In the map | Real twin | Seen at | Pictures | Status |', '|---|---|---|---|---|---|']
    for k, n in sorted(C.items(), key=lambda kv: -kv[1]):
        if not k:
            continue
        t = T.get(f'{g}/{k}', {})
        pics = [p for p in t.get('pics', []) if os.path.exists(os.path.join(RES, p))]
        st = t.get('status') or ('amber' if pics else 'red' if t.get('twin') else 'none')
        tot[st] += 1
        cnt = '' if n == 1 and g in ('ground', 'house detail', 'gutter') else f'{n:,}'
        rows.append(f"| {k} | {cnt} | {t.get('twin', '')} | {t.get('where', '')} | {len(pics) or ''} | {st} |")
    rows.append('')
out.append('**' + ', '.join(f'{tot[s]} {s}' for s in ('green', 'amber', 'red', 'none')) + f'** of {sum(tot.values())} types.')
out.append('')
open('docs/TWINS.md', 'w').write('\n'.join(out + rows))
print(dict(tot))
