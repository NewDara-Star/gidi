"""What stands on and beside each house, and which building each place takes over, in the map data (owner, 17 Oct 2026:
everything in the data; batch 2 of what the kit used to invent).

- out["roles"][d][str(i)] = {"type", "name"}: a point place (police station, fire station, clinic, fuel station, bank,
  chemist, office, nightclub, warehouse, betting shop) or a named landmark takes over a building. The rule is the kit's
  (blender/city.py poi_overrides): the nearest front or back house of its district within 120 m that no other place has
  taken, in the order of the places. The kit used to keep its answer in a cache file that went stale when the map changed.
- out["houses"][d][str(i)] = {"flat": 1 | 0, "unf": 1 | 0, "tank": [x, y] | 0, "dish": [x, y] | 0, "tyres": n}: a front, back
  or shed house's roof (flat or pitched, the kit's share by character and storeys; pitched needs four corners), whether
  its top storey is unfinished (columns and rebar; the share by district, two storeys or more), the water tank on a flat
  roof, the satellite dish, tyres holding down a zinc roof.
- out["things"] gains, each where the ground allows it (scripts/ground.py):
    a generator beside a house (the kit's share), at its back wall;
    the fire engines and ambulances parked out front of fire stations, hospitals and clinics, and a church's old molue;
    the police pound: wrecked cars and a heap of seized okadas behind a police station.

The draws use the kit's Rng and its shares (blender/gidi_kit/rules.py), so the bake stays byte-identical. Looks that take no
ground (paint, window type, roof colour) stay with the kit for now. Hand edits: "set house" (scripts/hand.py).
"""
import math

from shapely.geometry import Point, Polygon
from shapely.strtree import STRtree

import ground as GU
from things import Rng, CHARACTER, condition

FLAT_P = {'dense': {1: 0.08, 2: 0.5, 3: 0.75, 4: 0.95}, 'sprawl': {1: 0.05, 2: 0.4, 3: 0.7, 4: 0.9}, 'old_island': {1: 0.1, 2: 0.4, 3: 0.7, 4: 0.9},
          'elite': {1: 0.2, 2: 0.3, 3: 0.5, 4: 0.8}, 'civic': {1: 0.2, 2: 0.5, 3: 0.75, 4: 0.95}}   # blender/gidi_kit/rules.py C[...]
SHARE = {   # tank, dish, generator, roof tyres (rules.py C[...]; waterfront and port as dense)
    'dense': (0.6, 0.3, 0.4, 0.35), 'sprawl': (0.55, 0.35, 0.45, 0.2), 'old_island': (0.5, 0.3, 0.35, 0.2),
    'elite': (0.7, 0.5, 0.2, 0.0), 'civic': (0.6, 0.35, 0.35, 0.05),
}
UNFINISHED_SHARE = {'maze': 0.006, 'hub': 0.011, 'jungle': 0.004, 'foodgate': 0.0, 'watertown': 0.002, 'capital': 0.0,
                    'bazaar': 0.014, 'port': 0.014, 'railside': 0.041, 'estate': 0.001, 'oldisland': 0.0, 'heights': 0.0}
POI_PLACES = {'police', 'fire', 'fuel', 'bank', 'chemist', 'hospital', 'clinic', 'gov', 'council', 'night', 'industry', 'betting'}   # registry.POI_PLACES
LANDMARKS = {'The Palace', 'Shore Palace', 'The Crown Hall', 'Railside Jumat Mosque', 'Old Island Central Mosque', 'Cathedral of Christ',
             'Heritage Strip', 'Secretariat', 'Cloth Market', 'Alade Electronics Market'}   # landmarks.BY_NAME: a model of their own
HOUSES = ('front', 'back', 'shed')


def _ccw(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))) > 0


def _out_normal(pts, j):
    p, q = pts[j], pts[(j + 1) % len(pts)]
    L = math.dist(p, q) or 1.0
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    return (uy, -ux) if _ccw(pts) else (-uy, ux)   # as scripts/fronts.py: y runs south


def roles(out):
    B = out['buildings']
    cent = {(d, i): Polygon(b[1:]).centroid for d, L in B.items() for i, b in enumerate(L) if len(b) > 3 and b[0] in ('front', 'back')}
    civic = [(s['type'], s['name'], Polygon(s['pts']).centroid) for s in out.get('safe_ground', [])]
    named_plots = {}
    for poi in out['pois']:   # a landmark stands on the nearest civic plot of its type within 300 m (blender/city.py NAMED_PLOTS)
        if poi['name'] in LANDMARKS:
            q = Point(poi['x'], poi['y'])
            c = [(q.distance(p), n) for t, n, p in civic if t == poi['type'] and n not in named_plots]
            if c and min(c)[0] < 300:
                named_plots[min(c)[1]] = poi['name']
    res, used = {}, set()
    for poi in out['pois']:
        t = poi['type']
        if poi['name'] in LANDMARKS and poi['name'] not in named_plots.values():
            t = 'named'
        elif t not in POI_PLACES:
            continue
        q = Point(poi['x'], poi['y'])
        best = None
        for (d, i), c in cent.items():
            if d != poi.get('d') or (d, i) in used:
                continue
            dd = q.distance(c)
            if dd < 120 and (best is None or dd < best[0] or (dd == best[0] and (d, i) < best[1])):
                best = (dd, (d, i))
        if best:
            used.add(best[1])
            res.setdefault(best[1][0], {})[str(best[1][1])] = {'type': t, 'name': poi['name']}
    out['roles'] = {d: dict(sorted(v.items(), key=lambda kv: int(kv[0]))) for d, v in sorted(res.items())}
    out['named_plots'] = dict(sorted(named_plots.items()))
    return sum(len(v) for v in res.values())


def houses(out, G=None):
    G = G or GU.Ground(out)
    B = out['buildings']
    polys = [Polygon(b[1:]).buffer(0) for L in B.values() for b in L if len(b) > 3]
    BT = STRtree(polys)
    fronts = out.get('fronts') or {}
    T = out.setdefault('things', [])
    res, rep = {}, {'flat': 0, 'unfinished': 0, 'tank': 0, 'dish': 0, 'tyres': 0, 'generator': 0, 'generator refused': 0}

    def free(x, y, kind, pad=0.4):   # the ground allows it, and no building is in the way
        q = Point(x, y)
        return GU.allowed(G(x, y), kind) and not any(polys[j].distance(q) < pad for j in BT.query(q.buffer(pad)))

    for d in sorted(B):
        ch = CHARACTER.get(d, 'dense')
        shares = SHARE.get(ch, SHARE['dense'])
        flat_p = FLAT_P.get(ch, FLAT_P['dense'])
        st = (out.get('storeys') or {}).get(d, [])
        R = {}
        for i, b in enumerate(B[d]):
            if b[0] not in HOUSES or len(b) < 4:
                continue
            pts = [tuple(p) for p in b[1:]]
            if pts[0] == pts[-1]:
                pts = pts[:-1]
            n = len(pts)
            s = st[i] if i < len(st) else 1
            rng = Rng('house', d, i)
            unf = int(s >= 2 and Rng(d, 'unfinished', i).chance(UNFINISHED_SHARE.get(d, 0.0)))
            flat = int(rng.chance(flat_p.get(min(s, 4), 0.9)) or unf or n != 4)
            cx, cy = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
            h = {'flat': flat, 'unf': unf, 'tank': 0, 'dish': 0, 'tyres': 0}
            if rng.chance(shares[0]) and flat:
                h['tank'] = [round(pts[0][0] * 0.6 + cx * 0.4, 1), round(pts[0][1] * 0.6 + cy * 0.4, 1)]
            if rng.chance(shares[1]):
                h['dish'] = [round(pts[2 % n][0] * 0.8 + cx * 0.2, 1), round(pts[2 % n][1] * 0.8 + cy * 0.2, 1)] if flat else \
                    ([round(cx, 1), round(cy, 1)] if rng.chance(0.5) else 0)
            if rng.chance(shares[2]):   # a generator at the back wall, else any wall where the ground allows it
                e = (fronts.get(d, {}).get(str(i), {}).get('e', 0) + 2) % n
                placed = False
                for side in [e] + [k for k in range(n) if k != e]:
                    p, q = pts[side], pts[(side + 1) % n]
                    L = math.dist(p, q)
                    if L < 2.0:
                        continue
                    nx, ny = _out_normal(pts, side)
                    u = rng.between(-L / 4, L / 4)
                    mx, my = (p[0] + q[0]) / 2 + (q[0] - p[0]) / L * u + nx * 0.9, (p[1] + q[1]) / 2 + (q[1] - p[1]) / L * u + ny * 0.9
                    mx, my = round(mx, 1), round(my, 1)   # tested where it will be written
                    if free(mx, my, 'generator'):
                        T.append({'k': 'generator', 'x': round(mx, 1), 'y': round(my, 1), 'a': round(math.degrees(math.atan2(ny, nx)) % 360, 1), 'd': d, 'house': i})
                        placed = True
                        rep['generator'] += 1
                        break
                if not placed:
                    rep['generator refused'] += 1
            if not flat and rng.chance(shares[3]):
                h['tyres'] = 2 + rng.randrange(0, 3)
            for k in ('flat', 'unf'):
                rep['flat' if k == 'flat' else 'unfinished'] += h[k]
            rep['tank'] += bool(h['tank']); rep['dish'] += bool(h['dish']); rep['tyres'] += bool(h['tyres'])
            R[str(i)] = h
        res[d] = R
    out['houses'] = res
    return rep


def service(out, G=None):
    """Fire engines and ambulances out front of fire stations, hospitals and clinics, a church's old bus (a quarter of them),
    and the police pound behind each police station: parked where the ground allows."""
    G = G or GU.Ground(out)
    T = out.setdefault('things', [])
    B = out['buildings']
    rep = {}

    def park(k, x, y, a, d, **kw):
        x, y = round(x, 1), round(y, 1)   # tested where it will be written
        L = {'fire': 9.0, 'ambulance': 5.6, 'molue': 11.0, 'car': 4.8, 'okada': 2.1}.get(k, 4)
        ends = [(x + math.cos(math.radians(a)) * L / 2, y + math.sin(math.radians(a)) * L / 2), (x - math.cos(math.radians(a)) * L / 2, y - math.sin(math.radians(a)) * L / 2)]
        if all(GU.allowed(G(px, py), k) for px, py in [(x, y)] + ends):
            T.append(dict({'k': k, 'x': round(x, 1), 'y': round(y, 1), 'a': round(a % 360, 1), 'd': d}, **kw))
            rep[k] = rep.get(k, 0) + 1
            return True
        rep[k + ' refused'] = rep.get(k + ' refused', 0) + 1
        return False

    def sites(pts, e):   # points out from side e of a ring, and its outward heading
        n = len(pts)
        p, q = pts[e % n], pts[(e + 1) % n]
        L = math.dist(p, q) or 1.0
        nx, ny = _out_normal(pts, e % n)
        return p, q, L, nx, ny

    jobs = []
    for d, R in sorted((out.get('roles') or {}).items()):
        for si, r in R.items():
            b = B[d][int(si)]
            pts = [tuple(p) for p in b[1:]]
            e = (out.get('fronts') or {}).get(d, {}).get(si, {}).get('e', 0)
            jobs.append((d, r['type'], r['name'], pts, e))
    for s in out.get('safe_ground', []):
        if s['type'] in ('hospital', 'clinic', 'church'):
            pts = [tuple(p) for p in s['pts'][:-1]]
            jobs.append((s['d'], s['type'], s['name'], pts, 0))
    for d, t, name, pts, e in jobs:
        rng = Rng('service', t, name)
        p, q, L, nx, ny = sites(pts, e)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        head = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        if t in ('fire', 'hospital', 'clinic') or (t == 'church' and Rng('molue', name).chance(0.25)):
            k = 'fire' if t == 'fire' else 'molue' if t == 'church' else 'ambulance'
            for j in range(2 if k == 'fire' else 1):
                for out_m in (4.5, 6.5, 8.5):   # out front, as close as the ground allows
                    off = (j - (0.5 if k == 'fire' else 0)) * 3.4
                    if park(k, mx + nx * out_m + (q[0] - p[0]) / L * off, my + ny * out_m + (q[1] - p[1]) / L * off, head, d, c='worn'):
                        break
        if t == 'police':   # the pound behind: seized cars, rusting, and a heap of okadas
            p, q, L, nx, ny = sites(pts, e + 2)
            mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
            for k in range(rng.randrange(3, 7)):
                u, v = rng.between(-L / 2.5, L / 2.5), rng.between(3, 9)
                park('car', mx + (q[0] - p[0]) / L * u + nx * v, my + (q[1] - p[1]) / L * u + ny * v, rng.between(0, 360), d, c='wreck', s=rng.pick(['saloon', 'suv', 'pickup']))
            for k in range(rng.randrange(4, 10)):
                u, v = rng.between(-L / 3, L / 3), rng.between(1.5, 3)
                park('okada', mx + (q[0] - p[0]) / L * u + nx * v, my + (q[1] - p[1]) / L * u + ny * v, rng.between(0, 360), d, c='battered', heap=1)
    return rep


def place(out):
    G = GU.Ground(out)
    rep = {'roles': roles(out)}
    rep['houses'] = houses(out, G)
    rep['service'] = service(out, G)
    out['things'] = sorted(out['things'], key=lambda t: (t['k'], t['x'], t['y']))
    return rep
