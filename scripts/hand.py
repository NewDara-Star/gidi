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
#   {"op": "move building", "at": [x, y], "by": [dx, dy], "rotate": deg (optional, about its middle, after the move)}
#   {"op": "add furniture", "kind": "lasma post", "x": .., "y": .., "ang": ..}
#   {"op": "delete furniture", "at": [x, y], "kind": "pole" (optional)}  the nearest within 2 m
#   {"op": "move furniture", "at": [x, y], "kind": "pole" (optional), "to": [x, y], "ang": deg (optional)}  the nearest within 2 m
#   {"op": "move monument", "at": [x, y], "to": [x, y], "ang": deg (optional)}  /  {"op": "delete monument", "at": [x, y]}  the nearest within 3 m
#   {"op": "delete place", "name": "..."}
#   {"op": "reshape building", "at": [x, y], "kind": .., "pts": [...]}  /  {"op": "reshape parcel" | "reshape zone", "at", "pts"}   a new outline
#   {"op": "reshape street", "at": [x, y], "pts": [...]}   a road edit: the street, lane or district main nearest the point takes a new line
# (scripts/board_server.py writes these from the drawing board, web/board.html)
#   {"op": "add zone", "kind": "market street", "pts": [[x, y], ...]}
#   {"op": "add place", "name": "...", "type": "story", "x": .., "y": .., "note": "..."}   a named place (pin)
#   {"op": "move place", "name": "...", "x": .., "y": ..}
#   {"op": "add parcel", "kind": "motor park", "pts": [[x, y], ...]}  /  {"op": "delete parcel", "at": [x, y]}
#   {"op": "add monument", "model": "statue:founder" | "clock_tower" | "led_board" | "sculpture" | "lighthouse" | "arch" ..., "x", "y", "ang" (deg), "name", "span" (arch)}
# road edits (owner, 16 Oct: hand placement covers roads, streets and labels), applied early in the bake, before the clean-up, so a
# road placed by hand gets its junctions, gutters, furniture and surface like any other:
#   {"op": "add street", "kind": "street" | "lane" | "main", "pts": [[x, y], ...], "name": "..." (mains)}
#   {"op": "delete street", "at": [x, y]}                          the street or lane piece nearest the point (within 3 m)
#   {"op": "name road", "at": [x, y], "name": "..."}               the main road nearest the point (within 3 m) takes the name
#   {"op": "add structure", "kind": "skywalk", "name": "...", "pts": [...], "width": 3, "layer": 1}   a deck: the bake gives it heights
#   {"op": "cut street", "at": [x, y], "gap": 10}                   the street stops short both sides of the point (a dead end at a canal or the tracks)
#   {"op": "delete building", ..., "early": true}                   cleared for a road placed by hand: removed with the road edits
# labels and surfaces, applied after the surfaces are set:
#   {"op": "set surface", "at": [x, y], "surface": "mud"}          tar, worn, interlock, laterite, sand or mud
#   {"op": "name", "at": [x, y], "kind": "bus stop", "name": "..."}  a piece of furniture within 2 m gets a name (its label)
import glob, json, math, os
from shapely.geometry import Point, Polygon


# Everything a district owns in the map data. A frozen district keeps all of it in "snapshot" (scripts/freeze_district.py):
# the bake replaces the district with its snapshot at the very end, then applies its edits. Arterials, the rail, the water and
# the ferries cross many districts and stay shared.
OWNED_DICT = ('streets', 'lanes', 'paths', 'buildings', 'storeys', 'styles', 'parcels', 'walls', 'study')
OWNED_BY_D = ('mains', 'pois', 'structures', 'canals', 'gates', 'encroach', 'safe_ground', 'gutters', 'furniture', 'monuments')
OWNED_BY_PLACE = ('junctions', 'quays', 'boardwalks')


LAYOUT = 'v2'   # hand files carry the frame they were placed in ("layout", v1 when missing); only the current frame's are applied


THAW = {x for x in os.environ.get('GIDI_THAW', '').split(',') if x}   # districts rebuilt from their base and every hand edit, to be frozen again


def _files():
    """The current frame's hand files. A thawed district (GIDI_THAW) comes back without its snapshot, with every edit it ever had (those
    filed as applied when it was frozen, then the new ones) applied in their stages: the frozen state again, plus the new edits."""
    for f in sorted(glob.glob('web/hand/*.json')):
        H = json.load(open(f))
        if H.get('layout', 'v1') == LAYOUT:
            if H['district'] in THAW:
                H = dict(H); H.pop('snapshot', None); H['edits'] = H.get('applied', []) + H.get('edits', [])
            yield f, H


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


DECK_KEYS = ('pts', 'z', 'over', 'clear')   # what roadz.py works out for a deck: its line with the ramps on, its heights


def restore(out, d, S, keep_decks=False):
    P = Polygon([x for x in out['districts'] if x['id'] == d][0]['poly'][0])
    if keep_decks:   # the decks as this bake's roadz just made them, not as they were frozen (or every ramp fix is undone at the end)
        now = {(x.get('kind'), x.get('name')): x for x in out.get('structures', []) if x.get('d') == d and 'z' in x}
        S = dict(S, structures=[dict(x, **{k: now[(x.get('kind'), x.get('name'))][k] for k in DECK_KEYS if k in now[(x.get('kind'), x.get('name'))]})
                                if (x.get('kind'), x.get('name')) in now else x for x in S.get('structures', [])])
    for k in OWNED_DICT:
        if k in S:
            out.setdefault(k, {})[d] = S[k]
    for k in OWNED_BY_D:
        out[k] = [x for x in out.get(k, []) if x.get('d') != d] + S.get(k, [])
    gids = {g['id'] for g in S.get('gutters', [])}
    out['gutter_crossings'] = [c for c in out.get('gutter_crossings', []) if not c.get('gutter') in gids and not str(c.get('gutter', '')).startswith(d + '/')] + S.get('gutter_crossings', [])
    for k in OWNED_BY_PLACE:
        out[k] = [x for x in out.get(k, []) if not P.contains(_where(x))] + S.get(k, [])


def apply_snapshots(out, keep_decks=False):
    rep = {}
    for f, H in _files():
        if H.get('snapshot'):
            restore(out, H['district'], H['snapshot'], keep_decks)
            rep[H['district']] = sum(len(v) if isinstance(v, list) else 0 for v in H['snapshot'].values())
    return rep


def districts_frozen():
    out = set()
    for f, H in _files():
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
    for f, H in _files():
        d = H['district']; F = H.get('frozen') or {}
        if stage == 'tables':
            for pts in F.get('tables', []):
                _add_building(out, d, 'stalls', pts)
            out.setdefault('encroach', []).extend(dict(z, d=d) for z in F.get('encroach', []))
            rep[d] = len(F.get('tables', []))
        else:
            out.setdefault('furniture', []).extend(dict(f_, d=d) for f_ in F.get('furniture', []))
            rep[d] = len(F.get('furniture', []))
    return rep


ROAD_OPS = ('add street', 'delete street', 'name road', 'cut street', 'add structure', 'reshape street')
LABEL_OPS = ('set surface', 'name')


def apply_road_edits(out):
    from shapely.geometry import LineString
    rep = {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op == 'delete building' and e.get('early'):   # cleared for a road placed by hand: gone before the clean-up sees the road
                P = Point(e['at'])
                hit = [i for i, b in enumerate(out['buildings'].get(d, [])) if len(b) > 3 and Polygon(b[1:]).buffer(0.3).contains(P)]
                if hit:
                    _drop_building(out, d, hit[0]); rep[d] = rep.get(d, 0) + 1
                else:
                    print('  hand edit found nothing at', e['at'], op, e.get('note', ''))
                continue
            if op not in ROAD_OPS:
                continue
            if op == 'add street':
                pts = [[round(x, 1), round(y, 1)] for x, y in e['pts']]
                if e.get('kind', 'street') == 'main':
                    out['mains'].append({'d': d, 'name': e.get('name', ''), 'pts': pts, 'hand': True})
                else:
                    out.setdefault('lanes' if e.get('kind') == 'lane' else 'streets', {}).setdefault(d, []).append(pts)
            elif op == 'delete street':
                P = Point(e['at']); best = None
                for k in ('streets', 'lanes'):
                    for i, p in enumerate((out.get(k) or {}).get(d, [])):
                        if len(p) > 1:
                            dd = LineString(p).distance(P)
                            if dd < 3 and (best is None or dd < best[0]):
                                best = (dd, k, i)
                if best:
                    out[best[1]][d].pop(best[2])
                else:
                    print('  hand edit found no street at', e['at'], e.get('note', ''))
            elif op == 'cut street':   # a street stops short on both sides of a point: it dead-ends at a canal bank or the tracks
                from shapely.ops import substring
                P = Point(e['at']); gap = e.get('gap', 10.0); cut = 0
                for k in ('streets', 'lanes'):   # every piece through the point (two pieces often meet right at a crossing)
                    L_ = (out.get(k) or {}).get(d, []); new = []
                    for p in L_:
                        g = LineString(p) if len(p) > 1 else None
                        if g is None or g.distance(P) > 4.0:   # cut points come from the finished map; before the clean-up a street can sit a little off
                            new.append(p); continue
                        t = g.project(P); cut += 1
                        parts = [substring(g, 0, t - gap / 2) if t > gap / 2 else None, substring(g, t + gap / 2, g.length) if t + gap / 2 < g.length else None]
                        new += [[[round(x, 1), round(y, 1)] for x, y in q.coords] for q in parts if q is not None and q.length > 3]
                    if L_:
                        out[k][d] = new
                if not cut:
                    print('  hand edit found no street to cut at', e['at'], e.get('note', ''))
            elif op == 'reshape street':   # the street, lane or main nearest the point (within 4 m) takes a new line: {"at", "pts"}
                P = Point(e['at']); best = None
                for k in ('streets', 'lanes'):
                    for i, p in enumerate((out.get(k) or {}).get(d, [])):
                        if len(p) > 1:
                            dd = LineString(p).distance(P)
                            if dd < 4 and (best is None or dd < best[0]):
                                best = (dd, k, i)
                for i, m in enumerate(out['mains']):
                    if m.get('d') == d and len(m['pts']) > 1:
                        dd = LineString(m['pts']).distance(P)
                        if dd < 4 and (best is None or dd < best[0]):
                            best = (dd, 'mains', i)
                pts = [[round(x, 1), round(y, 1)] for x, y in e['pts']]
                if not best:
                    print('  hand edit found no street to reshape at', e['at'], e.get('note', ''))
                elif best[1] == 'mains':
                    out['mains'][best[2]]['pts'] = pts
                else:
                    out[best[1]][d][best[2]] = pts
            elif op == 'add structure':   # a deck over the ground: {"kind": "skywalk" | "flyover" | "footbridge", "name", "pts", "width", "layer"}
                out.setdefault('structures', []).append({'d': d, 'kind': e['kind'], 'name': e.get('name', ''), 'pts': e['pts'],
                                                         'width': e.get('width', 3), 'layer': e.get('layer', 1)})
            elif op == 'name road':
                P = Point(e['at'])
                c = [(LineString(m['pts']).distance(P), i) for i, m in enumerate(out['mains']) if len(m['pts']) > 1]
                c = [x for x in c if x[0] < 3]
                if c:
                    out['mains'][min(c)[1]]['name'] = e['name']
                else:
                    print('  hand edit found no main road at', e['at'], e.get('note', ''))
            rep[d] = rep.get(d, 0) + 1
    return rep


def apply_label_edits(out):
    from shapely.geometry import LineString
    rep = {}
    S = out.get('surfaces') or {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            if e['op'] not in LABEL_OPS:
                continue
            P = Point(e['at'])
            if e['op'] == 'set surface':
                best = None
                for k in ('streets', 'lanes'):
                    for i, p in enumerate((out.get(k) or {}).get(d, [])):
                        if len(p) > 1 and LineString(p).distance(P) < 3 and (best is None or LineString(p).distance(P) < best[0]):
                            best = (LineString(p).distance(P), k, i)
                for i, m in enumerate(out['mains']):
                    if len(m['pts']) > 1 and LineString(m['pts']).distance(P) < 3 and (best is None or LineString(m['pts']).distance(P) < best[0]):
                        best = (LineString(m['pts']).distance(P), 'mains', i)
                if not best:
                    print('  hand edit found no road at', e['at'], e.get('note', '')); continue
                if best[1] == 'mains':
                    S['mains'][best[2]] = e['surface']
                else:
                    S[best[1]][d][best[2]] = e['surface']
            else:
                c = [(Point(f_['x'], f_['y']).distance(P), i) for i, f_ in enumerate(out.get('furniture', [])) if f_['kind'] == e.get('kind', f_['kind'])]
                c = [x for x in c if x[0] < 15.0]   # the nearest of its kind: furniture is placed again when a district is thawed
                if c:
                    out['furniture'][min(c)[1]]['name'] = e['name']
                else:
                    print('  hand edit found no', e.get('kind', 'furniture'), 'at', e['at'], e.get('note', '')); continue
            rep[d] = rep.get(d, 0) + 1
    return rep


WALL_OPS = ('cut wall', 'delete wall', 'add wall', 'add gate', 'delete gate')
DETAIL_OPS = ('set front', 'add tree', 'move tree', 'delete tree')


def apply_detail_edits(out):
    """Edits to the house fronts and trees (scripts/fronts.py, scripts/trees.py), after they are worked out:
    {"op": "set front", "at": [x, y], "kind": .., "e": side, "shop": 0/1, "aw": canopy m, "bal": [sides]}   any of e/shop/aw/bal
    {"op": "add tree", "x", "y", "kind": "palm"|"broad"}  /  {"op": "move tree", "at", "to"}  /  {"op": "delete tree", "at"} (within 2 m)"""
    rep = {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op not in DETAIL_OPS:
                continue
            if op == 'set front':
                P = Point(e['at'])
                hit = [i for i, b in enumerate(out['buildings'][d]) if len(b) > 3 and (not e.get('kind') or b[0] == e['kind']) and Polygon(b[1:]).buffer(0.3).contains(P)]
                if not hit:
                    print('  hand edit found no house at', e['at'], e.get('note', '')); continue
                F = out.setdefault('fronts', {}).setdefault(d, {}).setdefault(str(hit[0]), {'e': 0, 'shop': 0, 'aw': 0.0, 'bal': []})
                for k in ('e', 'shop', 'aw', 'bal'):
                    if k in e:
                        F[k] = e[k]
            else:
                T = out.setdefault('trees', {}).setdefault(e.get('d', d), [])
                if op == 'add tree':
                    T.append([round(e['x'], 1), round(e['y'], 1), e.get('kind', 'broad')])
                else:
                    P = Point(e['at'])
                    c = [(Point(t[0], t[1]).distance(P), i) for i, t in enumerate(T)]
                    c = [x for x in c if x[0] < 2.0]
                    if not c:
                        print('  hand edit found no tree at', e['at'], e.get('note', '')); continue
                    if op == 'delete tree':
                        T.pop(min(c)[1])
                    else:
                        T[min(c)[1]][0:2] = [round(e['to'][0], 1), round(e['to'][1], 1)]
            rep[d] = rep.get(d, 0) + 1
    return rep


def apply_wall_edits(out):
    """Edits to the compound walls (scripts/compounds.py), after they are worked out:
    {"op": "cut wall", "at": [x, y], "gap": 3}   an opening in the wall nearest the point (within 2 m)
    {"op": "delete wall", "at": [x, y]}          the whole wall piece nearest the point (within 2 m)
    {"op": "add wall", "pts": [...]}  /  {"op": "add gate", "x", "y"}  /  {"op": "delete gate", "at": [x, y]} (within 2 m)"""
    from shapely.geometry import LineString
    from shapely.ops import substring
    rep = {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op not in WALL_OPS:
                continue
            W = out.setdefault('compound_walls', {}).setdefault(d, [])
            Gt = out.setdefault('compound_gates', {}).setdefault(d, [])
            if op in ('cut wall', 'delete wall'):
                P = Point(e['at'])
                c = [(LineString(w).distance(P), i) for i, w in enumerate(W) if len(w) > 1]
                c = [x for x in c if x[0] < 2.0]
                if not c:
                    print('  hand edit found no wall at', e['at'], e.get('note', '')); continue
                i = min(c)[1]
                if op == 'delete wall':
                    W.pop(i)
                else:
                    g = LineString(W[i]); t = g.project(P); gap = e.get('gap', 3.0)
                    keep = [q for q in (substring(g, 0, t - gap / 2) if t > gap / 2 else None, substring(g, t + gap / 2, g.length) if t + gap / 2 < g.length else None) if q is not None and q.length >= 0.5]
                    W[i:i + 1] = [[[round(x, 1), round(y, 1)] for x, y in q.coords] for q in keep]
            elif op == 'add wall':
                W.append([[round(x, 1), round(y, 1)] for x, y in e['pts']])
            elif op == 'add gate':
                Gt.append([round(e['x'], 1), round(e['y'], 1)])
            elif op == 'delete gate':
                P = Point(e['at'])
                c = [(Point(q).distance(P), i) for i, q in enumerate(Gt)]
                c = [x for x in c if x[0] < 2.0]
                if c:
                    Gt.pop(min(c)[1])
                else:
                    print('  hand edit found no gate at', e['at'], e.get('note', '')); continue
            rep[d] = rep.get(d, 0) + 1
    return rep


def apply_edits(out):
    rep = {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op in ROAD_OPS or op in LABEL_OPS or op in WALL_OPS or op in DETAIL_OPS or e.get('early'):
                continue   # applied earlier in the bake (apply_road_edits, apply_label_edits)
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
                    dx, dy = e.get('by', [0, 0]); b = out['buildings'][d][i]
                    pts = [[x + dx, y + dy] for x, y in b[1:]]
                    if e.get('rotate'):   # turned about its middle
                        cx, cy = sum(q[0] for q in pts) / len(pts), sum(q[1] for q in pts) / len(pts)
                        c, s_ = math.cos(math.radians(e['rotate'])), math.sin(math.radians(e['rotate']))
                        pts = [[cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c] for x, y in pts]
                    out['buildings'][d][i] = [b[0]] + [[round(x, 1), round(y, 1)] for x, y in pts]
            elif op == 'reshape building':   # the building holding the point takes a new outline: {"at", "kind", "pts"}
                P = Point(e['at'])
                hit = [i for i, b in enumerate(out['buildings'][d]) if len(b) > 3 and (not e.get('kind') or b[0] == e['kind']) and Polygon(b[1:]).buffer(0.3).contains(P)]
                if not hit:
                    print('  hand edit found nothing at', e['at'], op, e.get('note', '')); continue
                out['buildings'][d][hit[0]] = [out['buildings'][d][hit[0]][0]] + [[round(x, 1), round(y, 1)] for x, y in e['pts']]
            elif op in ('reshape parcel', 'reshape zone'):   # the plot (or market zone) holding the point takes a new outline
                P = Point(e['at']); pts = [[round(x, 1), round(y, 1)] for x, y in e['pts']]
                L_ = (out.get('parcels') or {}).get(d, []) if op == 'reshape parcel' else [z for z in out.get('encroach', []) if z.get('d') == d]
                hit = [q for q in L_ if Polygon(q['pts']).buffer(0.5).contains(P)]
                if not hit:
                    print('  hand edit found nothing at', e['at'], op, e.get('note', '')); continue
                hit[0]['pts'] = pts + ([pts[0]] if pts[0] != pts[-1] else [])   # plots and zones are closed rings
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
            elif op == 'move furniture':   # the nearest of its kind within 2 m goes to "to", turned to "ang"
                P = Point(e['at'])
                c = [(Point(f_['x'], f_['y']).distance(P), i) for i, f_ in enumerate(out.get('furniture', [])) if not e.get('kind') or f_['kind'] == e['kind']]
                c = [x for x in c if x[0] < 2.0]
                if not c:
                    print('  hand edit found no furniture at', e['at'], e.get('note', '')); continue
                f_ = out['furniture'][min(c)[1]]
                f_['x'], f_['y'] = e['to']
                if 'ang' in e:
                    f_['ang'] = e['ang']
            elif op in ('move monument', 'delete monument'):   # the nearest within 3 m
                P = Point(e['at'])
                c = [(Point(m['x'], m['y']).distance(P), i) for i, m in enumerate(out.get('monuments', []))]
                c = [x for x in c if x[0] < 3.0]
                if not c:
                    print('  hand edit found no monument at', e['at'], e.get('note', '')); continue
                if op == 'delete monument':
                    out['monuments'].pop(min(c)[1])
                else:
                    m = out['monuments'][min(c)[1]]
                    m['x'], m['y'] = e['to']
                    if 'ang' in e:
                        m['ang'] = e['ang']
            elif op == 'delete place':
                n0 = len(out['pois'])
                out['pois'] = [p for p in out['pois'] if p['name'] != e['name']]
                if len(out['pois']) == n0:
                    print('  hand edit found no place called', e['name']); continue
            elif op == 'add place':   # a named place (a pin): {"name", "type", "x", "y", "note"}
                out['pois'].append({'name': e['name'], 'type': e['type'], 'note': e.get('note', ''), 'd': d, 'x': e['x'], 'y': e['y'], 'hand': True})
            elif op == 'move place':  # a named place moves: {"name", "x", "y"}
                q = next((p for p in out['pois'] if p['name'] == e['name']), None)
                if q is None:
                    print('  hand edit found no place called', e['name']); continue
                q['x'], q['y'] = e['x'], e['y']
                if e.get('describe'):   # the place's description changes too
                    q['note'] = e['describe']
            elif op == 'add parcel':   # a plot (yard, park, market...): {"kind", "pts", "name"}
                out.setdefault('parcels', {}).setdefault(d, []).append({'kind': e['kind'], 'pts': e['pts']})
            elif op == 'delete parcel':   # the plot holding the point
                P = Point(e['at']); L_ = (out.get('parcels') or {}).get(d, [])
                hit = [i for i, q in enumerate(L_) if Polygon(q['pts']).buffer(0.5).contains(P)]
                if hit:
                    L_.pop(hit[0])
                else:
                    print('  hand edit found no plot at', e['at'], e.get('note', ''))
            elif op == 'add monument':   # placed by hand (blender/gidi_kit/monuments.py): {"model", "x", "y", "ang", "name", "span"}
                out.setdefault('monuments', []).append({k: e[k] for k in ('model', 'x', 'y', 'ang') if k in e} | {'d': d, 'name': e.get('name', ''), **({'span': e['span']} if 'span' in e else {})})
            elif op == 'add zone':
                out.setdefault('encroach', []).append({'kind': e['kind'], 'd': d, 'pts': e['pts']})
            rep[d] = rep.get(d, 0) + 1
    return rep
