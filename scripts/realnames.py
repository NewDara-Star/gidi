"""Gidi's names are its own: no name on the map may share its core with a real name around the places Gidi is a child of.

  python3 scripts/realnames.py     refresh docs/hand/realnames.txt from the twins, the photo notes and Overture names near them

The bake reads only docs/hand/realnames.txt (so every machine bakes the same map) and renames any clash at the very end,
so a name picker that slips, now or later, never reaches the map.
"""
import csv, glob, hashlib, json, os, re

FILE = 'docs/hand/realnames.txt'
PICS = os.path.expanduser('~/Real-world/research/google/ibudo/twins')
GENERIC = {'road', 'street', 'close', 'avenue', 'crescent', 'way', 'lane', 'drive', 'st', 'rd', 'ave', 'the', 'old', 'new', 'market', 'church',
           'mosque', 'school', 'link', 'bridge', 'expressway', 'service', 'estate', 'park', 'garage', 'motor', 'bus', 'stop', 'junction', 'oshodi',
           'surulere', 'lagos', 'unnamed', 'none'}
# invented names to swap in: common surnames, never a famous Lagos person, each checked against the real list before use
POOL = ['Adeyemi', 'Okafor', 'Ayinde', 'Ogundipe', 'Oladipo', 'Afolabi', 'Oyelaran', 'Odusanya', 'Ajasa', 'Fadipe', 'Oshinowo', 'Olatunji', 'Ireti',
        'Agboola', 'Ilori', 'Durojaiye', 'Ogunleye', 'Nwosu', 'Danjuma', 'Chukwuma', 'Ekpo', 'Mbanefo', 'Popoola', 'Udoh', 'Wahab', 'Akinola', 'Egbe',
        'Ikenna', 'Mojeed', 'Tokunbo', 'Ilesanmi', 'Jaiyeola', 'Kasumu', 'Laniyan', 'Odunsi', 'Sowande', 'Kolade', 'Adesina', 'Oyebanji',
        'Ajibola', 'Omotosho', 'Ezeani', 'Obiora', 'Amadi', 'Yakubu', 'Garba', 'Abiodun', 'Olowe', 'Bakare', 'Opeyemi', 'Ladejobi', 'Awoyemi']


def core(n):
    return ' '.join(w for w in re.findall(r"[a-zà-ÿ']+", (n or '').lower()) if w not in GENERIC and len(w) > 1)


def gather():
    """Every real street and place name around the studied places (needs ~/Real-world)."""
    real = set()
    boxes = []
    for tf in glob.glob('docs/hand/ibudo/twins/*.json'):
        st = json.load(open(tf))['streets']
        real |= {s['real_name'] for s in st if s.get('real_name')}
        at = [s['photo_at'] for s in st if s.get('photo_at')]
        if at:
            la = [q[0] for q in at]; lo = [q[1] for q in at]
            boxes.append((min(la) - 0.01, max(la) + 0.01, min(lo) - 0.01, max(lo) + 0.01))
    for idx in glob.glob(os.path.join(PICS, '*', 'INDEX.tsv')):
        for r in csv.DictReader(open(idx), delimiter='\t'):
            for k in ('real_name', 'panel_street'):
                v = re.sub(r'^[\d\-/ ]+', '', r.get(k) or '').strip()
                if v:
                    real.add(v)
    import pyarrow.parquet as pq
    for f in ('lagos_overture_segment.parquet', 'lagos_overture_place.parquet'):
        t = pq.read_table(os.path.expanduser('~/Real-world/research/data/overture-lagos/' + f), columns=['names', 'bbox'])
        for n, b in zip(t.column('names').to_pylist(), t.column('bbox').to_pylist()):
            if n and n.get('primary') and any(a0 <= b['ymin'] <= a1 and o0 <= b['xmin'] <= o1 for a0, a1, o0, o1 in boxes):
                real.add(n['primary'])
    return sorted({c for c in map(core, real) if len(c) >= 5})


def cores():
    return set(open(FILE).read().split('\n')[1:]) - {''} if os.path.exists(FILE) else set()


def rename(out):
    """Swap the first real word of any clashing name for an invented one; the same name always gets the same swap."""
    C = cores()
    if not C:
        return 0
    pool = [p for p in POOL if p.lower() not in C]
    done = {}

    def fix(n):
        if not n or core(n) not in C:
            return n
        if n not in done:
            words = n.split(' ')
            i = next(k for k, w in enumerate(words) if core(w))
            h = int(hashlib.md5(re.sub(r' \d+$', '', n).encode()).hexdigest(), 16)   # numbered ones ("... 12") all get the same swap
            for j in range(len(pool)):
                cand = ' '.join(words[:i] + [pool[(h + j) % len(pool)]] + words[i + 1:])
                if core(cand) not in C:
                    break
            done[n] = cand
        return done[n]
    for m in out['mains']:
        m['name'] = fix(m.get('name'))
    for p in out['pois']:
        p['name'] = fix(p.get('name'))
    for l in out.get('labels') or []:
        if isinstance(l, dict) and 't' in l:
            l['t'] = fix(l['t'])
    return len(done)


if __name__ == '__main__':
    c = gather()
    open(FILE, 'w').write('# real name cores near the places Gidi is a child of; no Gidi name may match one. Made by scripts/realnames.py\n' + '\n'.join(c) + '\n')
    print(len(c), 'real name cores written to', FILE)
