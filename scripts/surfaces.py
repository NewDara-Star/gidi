# Road surfaces (owner, 16 Oct 2026: "sometimes you have roads... not particularly paved... marshy ground... so much grime it barely
# looks like it's tarred... in the poorer areas"). Every road and street gets a surface, by rule, the same every run:
#   tar        tarred, in fair shape                 worn       tarred, potholed, broken edges, patched
#   interlock  interlocking paving bricks (Old Island's old downtown, estates: the owner's photo #1)
#   laterite   unpaved red-brown earth               sand       unpaved pale sand (the sandy estates and the coast)
#   mud        unpaved and waterlogged: standing water, grime, ruts (low, wet, poor places)
# Arterials and expressways are tar (a share worn). Each district has a street mix (MIX, below: Claude's judgement from the owner's
# reference photos and the parts of the data that can be trusted; Overture tags most of Lagos's local streets "unpaved" wherever it
# tags them, even mostly tarred Yaba, so those tags don't set it). On a street the mix then leans: the first stretch off a main road
# tends to tar; low ground (under 2 m), the water's edge (within 150 m) and the open fabric types lean to unpaved and mud.
# Writes out["surfaces"] = {"mains": [...], "arterials": [...], "streets": {d: [...]}, "lanes": {d: [...]}}, one per road, in order.
import math, zlib, json
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

KINDS = ['tar', 'worn', 'interlock', 'laterite', 'sand', 'mud']
# district street mix (shares of tar, worn, interlock, laterite, sand, mud); the owner can change any row
MIX = {
    'heights':   [.55, .15, .25, .00, .05, .00],   # Ikoyi, VI: tarred and interlock estates
    'capital':   [.45, .35, .10, .07, .00, .03],   # Ikeja: tarred, many worn
    'estate':    [.40, .20, .30, .05, .05, .00],   # gated estates: interlock inside the gates
    'oldisland': [.25, .35, .30, .00, .00, .10],   # the old downtown: interlock and broken tar, flooded corners
    'yaba':      [.35, .40, .10, .10, .00, .05],   # Saba: mostly tarred, mostly worn
    'hub':       [.20, .40, .05, .25, .00, .10],   # Oshodi: worn tar, red earth behind
    'maze':      [.15, .40, .05, .30, .00, .10],   # Mushin: worn, unpaved back streets
    'foodgate':  [.15, .35, .05, .30, .00, .15],   # Ketu, Mile 12: worn, muddy by the market and the river
    'railside':  [.10, .30, .05, .40, .00, .15],   # Agege: unpaved, muddy by the rail (owner: the muddy rail-side markets)
    'airport':   [.40, .30, .05, .20, .00, .05],
    'port':      [.20, .45, .00, .15, .05, .15],   # Apapa: wrecked tar under the trucks, waterlogged
    'jungle':    [.05, .30, .00, .30, .05, .30],   # Ajegunle: reclaimed marsh; floods every rainy season
    'watertown': [.00, .10, .00, .20, .20, .50],   # Makoko's land side: mud and sand, boardwalks beyond
    'bazaar':    [.10, .25, .05, .40, .05, .15],   # Ojo: red earth
    'border':    [.05, .20, .00, .45, .15, .15],   # Badagry: earth and sand, wet by the creek
    'oldshore':  [.10, .25, .00, .40, .10, .15],   # Ikorodu: red earth
    'frontier':  [.20, .10, .20, .05, .40, .05],   # Lekki and beyond: sand roads between the estates, interlock inside them
}
MAIN_WORN = {'port': .6, 'hub': .45, 'maze': .45, 'jungle': .5, 'railside': .4, 'foodgate': .4, 'bazaar': .35, 'border': .35, 'oldshore': .35}


def _u(key):
    """A number in [0, 1) from a key, the same every run."""
    return (zlib.crc32(key.encode()) % 100000) / 100000.0


def pick(shares, u):
    t = 0.0
    for k, s in zip(KINDS, shares):
        t += s
        if u < t:
            return k
    return KINDS[-1]


def lean(shares, wet, near_main, open_zone):
    """The district's mix, leaned for this street: wet places toward mud, near a main road toward tar, open fabric toward earth."""
    s = list(shares)
    poor = min(1.0, shares[5] * 4)   # wet ground turns to mud only where the district has mud at all (a low street in Ikoyi is just worn)
    if wet:
        s[5] += 0.25 * poor; s[3] += 0.05 * poor; s[1] += 0.10 * (1 - poor); s[0] *= 1 - 0.5 * poor; s[2] *= 1 - 0.5 * poor
    if near_main:
        s[0] += 0.20; s[1] += 0.10; s[5] *= 0.5
    if open_zone:
        s[3] += 0.10; s[4] += 0.05; s[0] *= 0.7
    t = sum(s)
    return [x / t for x in s]


def surfaces(out, terrain=None, zones=None):
    """zones: {district: [(polygon, is_open)]} from the generated files' fabric zones (optional)."""
    water = unary_union([Polygon(w).buffer(0) for w in out['water'] + out['ocean']])
    near_w = water.buffer(150)
    mainU = unary_union([LineString(m['pts']) for m in out['mains'] if len(m['pts']) > 1] +
                        [LineString(a['pts']) for a in out['arterials'] if a['cls'] != 'bridge'])
    main_band = mainU.buffer(40)

    def ground(x, y):
        if not terrain:
            return 5.0
        C, Z = terrain['cell_m'], terrain['z']
        i, j = min(max(int(y / C), 0), terrain['h'] - 1), min(max(int(x / C), 0), terrain['w'] - 1)
        return Z[i * terrain['w'] + j] / 10

    S = {'arterials': [], 'mains': [], 'streets': {}, 'lanes': {}}
    for a in out['arterials']:
        S['arterials'].append('worn' if _u('art/' + a['name']) < 0.25 else 'tar')
    for i, m in enumerate(out['mains']):
        d = m.get('d', '')
        S['mains'].append('worn' if _u(f'main/{d}/{i}') < MAIN_WORN.get(d, 0.25) else 'tar')
    from collections import Counter, defaultdict
    tally = Counter()

    def chains(L):
        """Street pieces that carry straight on through a junction (within 30 deg) share one chain id: one street, one dice roll."""
        par = list(range(len(L)))
        def find(i):
            while par[i] != i:
                par[i] = par[par[i]]; i = par[i]
            return i
        ends = defaultdict(list)   # node -> [(piece, heading away from the node)]
        for i, p in enumerate(L):
            if len(p) < 2:
                continue
            for e, (a, b) in ((0, (p[0], p[1])), (1, (p[-1], p[-2]))):
                ends[(round(a[0]), round(a[1]))].append((i, math.atan2(b[1] - a[1], b[0] - a[0])))
        for node, es in ends.items():
            used = set()
            pairs = sorted(((abs(abs(math.remainder(h1 - h2, 2 * math.pi)) - math.pi), i, j) for x, (i, h1) in enumerate(es) for (j, h2) in es[x + 1:] if i != j))
            for dev, i, j in pairs:   # straightest pairs first; each piece carries on into one other at most
                if dev < math.radians(30) and i not in used and j not in used:
                    par[find(i)] = find(j); used |= {i, j}
        return [find(i) for i in range(len(L))]

    for kind in ('streets', 'lanes'):
        for d, L in out.get(kind, {}).items():
            mix = MIX.get(d, [.3, .3, .05, .2, .05, .1])
            zs = (zones or {}).get(d, [])
            ch = chains(L)
            res = []
            for i, p in enumerate(L):
                if len(p) < 2:
                    res.append('laterite'); continue
                g = LineString(p); c = g.interpolate(0.5, normalized=True)
                wet = near_w.contains(c) or ground(c.x, c.y) < 2.0
                nm = main_band.intersects(Point(p[0])) or main_band.intersects(Point(p[-1]))
                op = any(z.contains(c) for z, o in zs if o)
                sh = lean(mix, wet, nm, op)
                if kind == 'lanes':   # lanes are rarely tarred
                    sh = lean([sh[0] * .3, sh[1] * .6, sh[2], sh[3] + .1, sh[4], sh[5] * 1.3], False, False, False)
                k = pick(sh, _u(f'{kind}/{d}/chain{ch[i]}'))   # the street's own roll; its ground still leans each piece
                res.append(k); tally[(d, k)] += g.length
            S[kind][d] = res
    out['surfaces'] = S
    return tally


if __name__ == '__main__':   # test on the baked map: python3 scripts/surfaces.py
    G = json.loads(open('web/gidi-data.js').read()[len('window.GIDI='):-1])
    T = json.load(open('web/terrain.json'))
    import glob
    Z = {}
    for f in glob.glob('web/gen-*.json'):
        F = json.load(open(f))
        if F.get('layout') == 'v2':
            Z[F['id']] = [(Polygon(z['pts']), any(w in z['type'] for w in ('open', 'sparser', 'spaced'))) for z in F.get('zones', [])]
    tally = surfaces(G, T, Z)
    by_d = {}
    for (d, k), L in tally.items():
        by_d.setdefault(d, {})[k] = by_d.setdefault(d, {}).get(k, 0) + L
    for d, v in sorted(by_d.items()):
        t = sum(v.values())
        print(f"{d:10}", ' '.join(f"{k} {v.get(k, 0) / t:4.0%}" for k in KINDS))
