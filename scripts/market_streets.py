# Market streets, run by bake_web.py on the final roads (after the clean-up and the junctions). The owner's ruling (15 Oct
# 2026, from Mile 12, Oshodi, Idumota): round a market, traders take the walkways and the carriageway too, under umbrellas
# and on tables, and the traffic squeezes through a running lane kept clear down the middle (cross_sections.MARKET_CLEAR).
# Each side of each market street is a declared zone in out["encroach"] (kind "market street"); the tables are buildings of
# kind "stalls". Never in the running lane, never on a crossing road's carriageway, never on a building or the water.
import math, random, zlib
from shapely.geometry import LineString, Polygon, box
from shapely.affinity import rotate, translate
from shapely.ops import unary_union, substring
from shapely.strtree import STRtree
import cross_sections as XS

REACH = 90.0        # streets this near a market become market streets
DENSITY = 0.9       # share of table spots taken
ROW = 1.9           # table depth 1.5 m + 0.4 m between rows


def _lines(g):
    if g.is_empty:
        return []
    return [g] if g.geom_type == 'LineString' else [x for p in getattr(g, 'geoms', []) for x in _lines(p)]


def market_streets(out, districts):
    rep = {'zones': 0, 'tables': 0}
    roads = [('street', LineString(p)) for k in ('streets',) for L in (out.get(k) or {}).values() for p in L if len(p) > 1]
    roads += [('lane', LineString(p)) for L in (out.get('lanes') or {}).values() for p in L if len(p) > 1]
    roads += [('main', LineString(m['pts'])) for m in out['mains']]
    roads += [(a['cls'] if a['cls'] in XS.SECTIONS else 'art', LineString(a['pts'])) for a in out['arterials']]
    carriage = [(g, g.buffer(XS.half(k), cap_style=2)) for k, g in roads]
    ct = STRtree([c for g, c in carriage])
    wet = unary_union([Polygon(w) for w in out['water'] + out['ocean']])
    for d in districts:
        rnd = random.Random(zlib.crc32(d.encode()) + 7)   # stable across runs (Python's hash() is not)
        markets = [Polygon(p['pts']) for p in (out.get('parcels') or {}).get(d, []) if p['kind'] == 'market']
        if not markets:
            continue
        L = out['buildings'][d]
        B = [Polygon(b[1:]).buffer(0) for b in L if len(b) > 3]
        bt = STRtree(B)
        placed = []
        grid = {}
        for mk in markets:
            for k, g in roads:
                if k not in XS.MARKET_CLEAR or g.distance(mk) > REACH:
                    continue
                band = XS.walkway_band(k)
                clear = XS.MARKET_CLEAR[k] / 2
                outer = band[1] + 0.5 * (XS.building_line(k) - band[1])
                for seg in _lines(g.intersection(mk.buffer(REACH))):
                    if seg.length < 6:
                        continue
                    own = g.buffer(1.0)   # the same road listed again (an edge road both districts keep) is not a crossing road
                    others = unary_union([carriage[j][1] for j in ct.query(seg.buffer(outer + 1)) if carriage[j][0] is not g and not own.contains(carriage[j][0].intersection(seg.buffer(outer + 1)))] or [box(0, 0, 0, 0)])
                    sides = [seg.buffer(sg * outer, single_sided=True, cap_style=2).difference(seg.buffer(clear, cap_style=2)).difference(others) for sg in (1, -1)]
                    for zs in sides:
                        for zp in getattr(zs, 'geoms', [zs]):
                            if zp.geom_type == 'Polygon' and zp.area > 1:
                                out.setdefault('encroach', []).append({'kind': 'market street', 'd': d, 'pts': [[round(x, 1), round(y, 1)] for x, y in zp.exterior.coords]})
                                rep['zones'] += 1
                    zone_in = unary_union(sides).buffer(-0.12)   # rounding never puts a corner in the lane
                    rows = [clear + 0.15 + 0.75 + ROW * i for i in range(max(1, int((outer - clear - 0.3) // ROW + (1 if (outer - clear - 0.3) % ROW > 1.0 else 0))))]
                    for sd in (1, -1):
                        for off in rows:
                            t = 1.5
                            while t < seg.length - 1.5:
                                w = rnd.uniform(1.2, 2.2)
                                step = w + rnd.uniform(0.15, 0.6)   # shoulder to shoulder, as real market tables stand
                                if rnd.random() <= DENSITY:
                                    q = seg.interpolate(t + w / 2)
                                    q2 = seg.interpolate(min(seg.length, t + 1))
                                    a = math.atan2(q2.y - q.y, q2.x - q.x)
                                    dp = 1.5
                                    r = rotate(box(-w / 2, -dp / 2, w / 2, dp / 2), a + math.radians(rnd.gauss(0, 3)), origin=(0, 0), use_radians=True)
                                    r = translate(r, q.x - math.sin(a) * off * sd, q.y + math.cos(a) * off * sd)
                                    gx, gy = int(r.centroid.x // 10), int(r.centroid.y // 10)
                                    if zone_in.contains(r) and not wet.intersects(r) and not any(B[j].distance(r) < 0.2 for j in bt.query(r.buffer(0.2))) \
                                            and not any(o.distance(r) < 0.1 for i in (-1, 0, 1) for j in (-1, 0, 1) for o in grid.get((gx + i, gy + j), [])):
                                        placed.append(r)
                                        grid.setdefault((gx, gy), []).append(r)
                                t += step
        for r in placed:
            L.append(['stalls'] + [[round(x, 1), round(y, 1)] for x, y in list(r.exterior.coords)[:-1]])
            if (out.get('storeys') or {}).get(d) is not None:
                out['storeys'][d].append(1)
            if (out.get('styles') or {}).get(d) is not None:
                out['styles'][d].append(None)
        rep['tables'] += len(placed)
    return rep
