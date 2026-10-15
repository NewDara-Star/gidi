# Hand files (owner, 15 Oct 2026: "less generator, more hand placing"): web/hand/<district>.json holds what is placed by hand
# in a district, and the bake applies it last, so hand work always wins and nothing is regenerated out from under it.
#
#   {"district": "foodgate",
#    "frozen": {"tables": [[[x, y], ...], ...], "encroach": [{"kind", "pts"}...], "furniture": [{"kind", "x", "y", "ang"}...]},
#    "edits": [ ...applied in order... ]}
#
# frozen: generated once and then kept exactly (scripts/freeze_district.py writes it). While a district has frozen items, the
# bake does not generate its market streets or its street furniture again.
# edits, each {"op": ..., "note": "why"}:
#   {"op": "add building", "kind": "kiosk", "pts": [[x, y], ...]}          a footprint, storeys 1 unless "storeys"
#   {"op": "delete building", "at": [x, y], "kind": "stalls" (optional)}  the building whose footprint holds the point
#   {"op": "move building", "at": [x, y], "by": [dx, dy]}
#   {"op": "add furniture", "kind": "lasma post", "x": .., "y": .., "ang": ..}
#   {"op": "delete furniture", "at": [x, y], "kind": "pole" (optional)}  the nearest within 2 m
#   {"op": "add zone", "kind": "market street", "pts": [[x, y], ...]}
import glob, json, os
from shapely.geometry import Point, Polygon


# Everything a district owns in the map data. A frozen district keeps all of it in "snapshot" (scripts/freeze_district.py):
# the bake replaces the district with its snapshot at the very end, then applies its edits. Arterials, the rail, the water and
# the ferries cross many districts and stay shared.
OWNED_DICT = ('streets', 'lanes', 'paths', 'buildings', 'storeys', 'styles', 'parcels', 'walls', 'study')
OWNED_BY_D = ('mains', 'pois', 'structures', 'canals', 'gates', 'encroach', 'safe_ground', 'gutters', 'furniture')
OWNED_BY_PLACE = ('junctions', 'quays', 'boardwalks')


def _where(item):
    if isinstance(item, dict):
        if 'x' in item:
            return Point(item['x'], item['y'])
        return Polygon(item['pts']).centroid if len(item['pts']) > 2 else Point(item['pts'][0])
    return Point(item[len(item) // 2])   # a boardwalk: a list of points


def snapshot(out, d):
    P = Polygon([x for x in out['districts'] if x['id'] == d][0]['poly'][0])
    S = {k: (out.get(k) or {}).get(d) for k in OWNED_DICT if (out.get(k) or {}).get(d) is not None}
    for k in OWNED_BY_D:
        S[k] = [x for x in out.get(k, []) if x.get('d') == d]
    gids = {g['id'] for g in S.get('gutters', [])}
    S['gutter_crossings'] = [c for c in out.get('gutter_crossings', []) if c.get('gutter') in gids]
    for k in OWNED_BY_PLACE:
        S[k] = [x for x in out.get(k, []) if P.contains(_where(x))]
    return S


def restore(out, d, S):
    P = Polygon([x for x in out['districts'] if x['id'] == d][0]['poly'][0])
    for k in OWNED_DICT:
        if k in S:
            out.setdefault(k, {})[d] = S[k]
    for k in OWNED_BY_D:
        out[k] = [x for x in out.get(k, []) if x.get('d') != d] + S.get(k, [])
    gids = {g['id'] for g in S.get('gutters', [])}
    out['gutter_crossings'] = [c for c in out.get('gutter_crossings', []) if not c.get('gutter') in gids and not str(c.get('gutter', '')).startswith(d + '/')] + S.get('gutter_crossings', [])
    for k in OWNED_BY_PLACE:
        out[k] = [x for x in out.get(k, []) if not P.contains(_where(x))] + S.get(k, [])


def apply_snapshots(out):
    rep = {}
    for f in sorted(glob.glob('web/hand/*.json')):
        H = json.load(open(f))
        if H.get('snapshot'):
            restore(out, H['district'], H['snapshot'])
            rep[H['district']] = sum(len(v) if isinstance(v, list) else 0 for v in H['snapshot'].values())
    return rep


def districts_frozen():
    out = set()
    for f in glob.glob('web/hand/*.json'):
        H = json.load(open(f))
        if H.get('frozen') or H.get('snapshot'):
            out.add(H['district'])
    return out


def _add_building(out, d, kind, pts, storeys=1):
    out['buildings'][d].append([kind] + [[round(x, 1), round(y, 1)] for x, y in pts])
    if (out.get('storeys') or {}).get(d) is not None:
        out['storeys'][d].append(storeys)
    if (out.get('styles') or {}).get(d) is not None:
        out['styles'][d].append(None)


def _drop_building(out, d, i):
    for k in ('buildings', 'storeys', 'styles'):
        a = (out.get(k) or {}).get(d)
        if a is not None and len(a) > i:
            a.pop(i)


def apply_frozen(out, stage):
    """stage 'tables' (with the market streets, before the heights) or 'furniture' (where the furniture is placed)."""
    rep = {}
    for f in sorted(glob.glob('web/hand/*.json')):
        H = json.load(open(f)); d = H['district']; F = H.get('frozen') or {}
        if stage == 'tables':
            for pts in F.get('tables', []):
                _add_building(out, d, 'stalls', pts)
            out.setdefault('encroach', []).extend(dict(z, d=d) for z in F.get('encroach', []))
            rep[d] = len(F.get('tables', []))
        else:
            out.setdefault('furniture', []).extend(dict(f_, d=d) for f_ in F.get('furniture', []))
            rep[d] = len(F.get('furniture', []))
    return rep


def apply_edits(out):
    rep = {}
    for f in sorted(glob.glob('web/hand/*.json')):
        H = json.load(open(f)); d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op == 'add building':
                _add_building(out, d, e['kind'], e['pts'], e.get('storeys', 1))
            elif op in ('delete building', 'move building'):
                P = Point(e['at'])
                hit = [i for i, b in enumerate(out['buildings'][d]) if len(b) > 3 and (not e.get('kind') or b[0] == e['kind']) and Polygon(b[1:]).buffer(0.3).contains(P)]
                if not hit:
                    print('  hand edit found nothing at', e['at'], op, e.get('note', '')); continue
                i = hit[0]
                if op == 'delete building':
                    _drop_building(out, d, i)
                else:
                    dx, dy = e['by']; b = out['buildings'][d][i]
                    out['buildings'][d][i] = [b[0]] + [[round(x + dx, 1), round(y + dy, 1)] for x, y in b[1:]]
            elif op == 'add furniture':
                out.setdefault('furniture', []).append({k: e[k] for k in ('kind', 'x', 'y', 'ang')} | {'road': e.get('note', ''), 'd': d})
            elif op == 'delete furniture':
                P = Point(e['at'])
                c = [(Point(f_['x'], f_['y']).distance(P), i) for i, f_ in enumerate(out.get('furniture', [])) if not e.get('kind') or f_['kind'] == e['kind']]
                c = [x for x in c if x[0] < 2.0]
                if c:
                    out['furniture'].pop(min(c)[1])
                else:
                    print('  hand edit found no furniture at', e['at'], e.get('note', ''))
            elif op == 'add zone':
                out.setdefault('encroach', []).append({'kind': e['kind'], 'd': d, 'pts': e['pts']})
            rep[d] = rep.get(d, 0) + 1
    return rep
