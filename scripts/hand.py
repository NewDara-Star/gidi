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


def districts_frozen():
    out = set()
    for f in glob.glob('web/hand/*.json'):
        H = json.load(open(f))
        if H.get('frozen'):
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
            out.setdefault('furniture', []).extend(F.get('furniture', []))
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
                out.setdefault('furniture', []).append({k: e[k] for k in ('kind', 'x', 'y', 'ang')} | {'road': e.get('note', '')})
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
