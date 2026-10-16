# After districts are generated side by side (the v2 frame), two of them can pick the same road name, or two roads sharing a first name
# ("Ayinde Road" and "Ayinde Street"), because neither saw the other's choice. This pass keeps each first name with the first district
# (in a fixed order) and gives the others fresh names from a reserve, the same every run. Arterials and the frame's border roads
# (web/network.json) keep theirs; nothing in a district may share a first name with them. The reserve avoids names that are famous
# Lagos people or streets (invented names only). A district's border roads take the frame's current names.
# Usage: python3 scripts/rename_mains.py      (rewrites web/gen-<id>.json for every v2 district)
import glob, json, random

ORDER = ['border', 'bazaar', 'jungle', 'port', 'maze', 'hub', 'railside', 'capital', 'estate', 'foodgate', 'watertown', 'oldshore',
         'oldisland', 'heights', 'frontier', 'airport', 'yaba']
RESERVE = ['Abiodun', 'Adebisi', 'Adekunle', 'Adeniran', 'Adesina', 'Afolayan', 'Agboola', 'Ajibade', 'Akinwale', 'Alabi', 'Amusa', 'Aro',
           'Ashafa', 'Ayodele', 'Babalola', 'Badmus', 'Bakare', 'Bisiriyu', 'Dada', 'Durojaiye', 'Ebute', 'Edun',
           'Ekundayo', 'Falana', 'Fasanmi', 'Folarin', 'Gbadebo', 'Idris', 'Igwe', 'Ishola', 'Jegede', 'Kadiri', 'Kazeem',
           'Komolafe', 'Lasisi', 'Lawani', 'Mustapha', 'Obi', 'Odutola', 'Ogunbiyi',
           'Ogunlana', 'Okeke', 'Okoro', 'Olabode', 'Olaniyan', 'Oloyede', 'Omotosho', 'Onyeka', 'Opeyemi', 'Orelope',
           'Osho', 'Oyebanji', 'Oyewole', 'Raheem', 'Rotimi', 'Shittu', 'Sodipo', 'Somade', 'Sotunde', 'Suleiman', 'Thomas', 'Tiamiyu',
           'Ubani', 'Wemimo', 'Williams-Ade', 'Yakubu', 'Zubair']
G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
NET = json.load(open('web/network.json'))
taken = {a['name'].split()[0] for a in G['arterials']} | {e['name'].split()[0] for e in NET['edges'].values() if e.get('name')}
ends = lambda pts: tuple(sorted([(round(pts[0][0]), round(pts[0][1])), (round(pts[-1][0]), round(pts[-1][1]))]))
EDGE_BY_ENDS = {ends(e['pts']): e for e in NET['edges'].values()}
rnd = random.Random(1611)
pool = [n for n in RESERVE if n not in taken]
rnd.shuffle(pool)
report = {}
for did in ORDER:
    f = f'web/gen-{did}.json'
    try:
        F = json.load(open(f))
    except FileNotFoundError:
        continue
    if F.get('layout') != 'v2':
        continue
    ren = {}; changed = False
    for m in F['mains']:   # border roads: whatever the frame calls them now (matched by their ends)
        if m.get('edge_with') is not None:
            e = EDGE_BY_ENDS.get(ends(m['pts']))
            if e and e.get('name') and m.get('name') != e['name']:
                m['name'] = e['name']; changed = True
    for m in F['mains']:
        n = m.get('name')
        if not n or m.get('edge_with') is not None or n in ren.values():
            continue   # unnamed links; border roads belong to the frame
        first = n.split()[0]
        if n in ren:
            m['name'] = ren[n]; continue
        if first in taken:
            new = f"{pool.pop()} {n.split(' ', 1)[1] if ' ' in n else 'Road'}"
            ren[n] = new; m['name'] = new; taken.add(new.split()[0])
        else:
            taken.add(first)
    if ren or changed:
        for m in F['mains']:
            if m.get('name') in ren:
                m['name'] = ren[m['name']]
        json.dump(F, open(f, 'w'), separators=(',', ':'))
    report[did] = len(ren)
print('renamed:', {k: v for k, v in report.items() if v}, '| reserve names left:', len(pool))
