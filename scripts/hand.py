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
#   {"op": "delete place", "name": "...", "at": [x, y] (optional: only the one within 5 m)}
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
#   {"op": "delete structure", "name": "..."}                 the district's decks of that name come down
#   {"op": "add path", "pts": [[x, y], ...]}                    a footpath: market aisles, rail-side walks
#   {"op": "delete path", "at": [x, y]}                        the footpath nearest the point (within 3 m)
#   {"op": "delete main", "at": [x, y]}                        the district main road nearest the point (within 4 m)
#   {"op": "cut street", "at": [x, y], "gap": 10}                   the street stops short both sides of the point (a dead end at a canal or the tracks)
#   {"op": "delete building", ..., "early": true}                   cleared for a road placed by hand: removed with the road edits
#   {"op": "clear area", "wkt": shape, "places_wkt": shape}     an area built again from its real place (scripts/rebuild_areas.py): with the road
#       edits, its streets and lanes are cut back to its edge (a part left outside stays if it is over 15 m and joined on), its paths,
#       plots, mains (over half inside) and buildings go; with the other edits, the buildings placed since and its places and decks go.
#       One shape, not a delete per thing: nothing in it can be missed because it moved.
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


MISSES = []   # hand edits that found nothing to act on: the checks fail on any (scripts/check_district.py, check 17)
_D = [None]


def _miss(*a):
    print(*a)
    MISSES.append({'d': _D[0], 'what': ' '.join(str(x) for x in a).strip()})


def _files():
    """The current frame's hand files. A thawed district (GIDI_THAW) comes back without its snapshot, with every edit it ever had (those
    filed as applied when it was frozen, then the new ones) applied in their stages: the frozen state again, plus the new edits."""
    for f in sorted(glob.glob('web/hand/*.json')):
        H = json.load(open(f))
        if H.get('layout', 'v1') == LAYOUT:
            if H['district'] in THAW:
                H = dict(H); H.pop('snapshot', None); H['edits'] = H.get('applied', []) + H.get('edits', [])
            elif H.get('snapshot'):   # edits whose result the snapshot doesn't hold (things, surfaces, houses, paint, fronts, walls are
                # made again every bake): replayed from those already applied, or freezing would drop them
                H = dict(H); H['edits'] = [e for e in H.get('applied', []) if e['op'] in REPLAY] + H.get('edits', [])
            gen = f'web/hand/gen/{H["district"]}.json'   # the district's areas, built again from their real places (scripts/rebuild_areas.py)
            if os.path.exists(gen):   # come first: the hand edits are fixes on top of them
                H = dict(H); H['edits'] = json.load(open(gen))['edits'] + H.get('edits', [])
            _D[0] = H['district']
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


_BOX = {}   # id(footprint) -> (footprint, its box): a footprint changed is a new list, so its box is worked out again


def _hits(out, d, P, kind=None):
    """The buildings of district d (in order) whose footprint, 30 cm wider, holds the point P, of that kind if one is given.
    A box test first: the bake replays tens of thousands of these over tens of thousands of footprints."""
    x, y = P.x, P.y; hit = []
    for i, b in enumerate((out.get('buildings') or {}).get(d, [])):
        if len(b) <= 3 or (kind and b[0] != kind):
            continue
        c = _BOX.get(id(b))
        if c is None or c[0] is not b:
            xs = [q[0] for q in b[1:]]; ys = [q[1] for q in b[1:]]
            c = _BOX[id(b)] = (b, (min(xs) - 0.31, min(ys) - 0.31, max(xs) + 0.31, max(ys) + 0.31))
        bx = c[1]
        if bx[0] <= x <= bx[2] and bx[1] <= y <= bx[3] and Polygon(b[1:]).buffer(0.3).contains(P):
            hit.append(i)
    return hit


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


ROAD_OPS = ('add street', 'delete street', 'name road', 'cut street', 'add structure', 'delete structure', 'add path', 'delete path', 'delete main', 'reshape street')
LABEL_OPS = ('set surface', 'name')


def _clear_area(out, d, e, stage):
    """{"op": "clear area"} (see the top of this file). stage 'road' (apply_road_edits) or 'late' (apply_edits)."""
    from shapely import wkt
    from shapely.geometry import LineString
    from shapely.prepared import prep
    C = wkt.loads(e['wkt']); PC = prep(C); x0, y0, x1, y1 = C.bounds
    def inside_box(pts):
        xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
        return not (max(xs) < x0 or min(xs) > x1 or max(ys) < y0 or min(ys) > y1)
    B = (out.get('buildings') or {}).get(d, [])
    from autoclean import ring_pts
    for i in range(len(B) - 1, -1, -1):
        if len(B[i]) > 3 and inside_box(B[i][1:]) and PC.intersects(Polygon(B[i][1:])):
            P = Polygon(B[i][1:]).buffer(0)
            if P.intersection(C).area < 0.5 * P.area:   # a building the shape only clips is cut back to it (35 cm clear), not lost: a
                Q = P.difference(C.buffer(0.35))        # 13,000 m2 warehouse went for 860 m2 over the next area's line (22 Oct 2026)
                Q = max(getattr(Q, 'geoms', [Q]), key=lambda q: q.area) if not Q.is_empty else Q
                if not Q.is_empty and Q.geom_type == 'Polygon' and Q.area >= 6 and len(ring_pts(Q)) >= 3:
                    B[i] = [B[i][0]] + ring_pts(Q)
                    continue
            _drop_building(out, d, i)
    if stage == 'late':
        A = wkt.loads(e.get('places_wkt', e['wkt'])); PA = prep(A)
        out['pois'] = [p for p in out['pois'] if not (p.get('d') == d and p.get('type') != 'story' and PA.contains(Point(p['x'], p['y'])))]   # the story's places stay
        out['structures'] = [x for x in out.get('structures', []) if not (x.get('d') == d and len(x['pts']) > 1 and PA.intersects(LineString(x['pts'])))]
        return
    Cb = C.buffer(1)
    for k in ('paths',):
        L_ = (out.get(k) or {}).get(d)
        if L_:
            out[k][d] = [p for p in L_ if len(p) < 2 or not inside_box(p) or not PC.intersects(LineString(p))]
    P_ = (out.get('parcels') or {}).get(d)
    if P_:
        out['parcels'][d] = [q for q in P_ if not (inside_box(q['pts']) and Polygon(q['pts']).buffer(0).intersection(C).area > 0.3 * Polygon(q['pts']).buffer(0).area)]
    out['mains'] = [m for m in out['mains'] if not (m.get('d') == d and len(m['pts']) > 1 and inside_box(m['pts'])
                                                    and LineString(m['pts']).intersection(C).length > 0.5 * LineString(m['pts']).length)]
    cut = []
    for k in ('streets', 'lanes'):
        keep = []
        for p in (out.get(k) or {}).get(d, []):
            g = LineString(p) if len(p) > 1 else None
            if g is not None and inside_box(p) and PC.intersects(g) and g.intersection(C).length >= 2:
                cut.append((k, g))
            else:
                keep.append(p)
        if (out.get(k) or {}).get(d) is not None:
            out[k][d] = keep
    if not cut:
        return
    from shapely.strtree import STRtree
    live = [LineString(p) for k in ('streets', 'lanes') for p in (out.get(k) or {}).get(d, []) if len(p) > 1]   # every way in the district, not only
    live += [LineString(m['pts']) for m in out['mains'] if len(m['pts']) > 1]                                    # those near the edge: a street's far end
    live += [LineString(a['pts']) for a in out.get('arterials', []) if len(a['pts']) > 1]                         # can be what joins it on
    lt = STRtree(live)
    for k, g in cut:   # what is left outside the area stays if it is long enough and joined on at an end, or if the area only clips it
        rest = g.difference(Cb)
        clipped = g.intersection(C).length < 0.5 * g.length
        for part in getattr(rest, 'geoms', [rest]):
            if part.geom_type != 'LineString' or part.length <= 15:
                continue
            ends = [Point(part.coords[j]) for j in (0, -1)]
            if clipped or any(live[int(i)].distance(e) < 1.5 for e in ends for i in lt.query(e.buffer(1.5))):
                pts = [[round(x, 1), round(y, 1)] for x, y in part.coords]
                out.setdefault(k, {}).setdefault(d, []).append(pts)


def apply_road_edits(out):
    _BOX.clear()   # footprints may have been changed in place since the last stage
    from shapely.geometry import LineString
    rep = {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op == 'delete building' and e.get('early'):   # cleared for a road placed by hand: gone before the clean-up sees the road
                P = Point(e['at'])
                hit = _hits(out, d, P)
                if hit:
                    _drop_building(out, d, hit[0]); rep[d] = rep.get(d, 0) + 1
                else:
                    _miss('  hand edit found nothing at', e['at'], op, e.get('note', ''))
                continue
            if op == 'clear area':
                _clear_area(out, d, e, 'road'); rep[d] = rep.get(d, 0) + 1
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
                    _miss('  hand edit found no street at', e['at'], e.get('note', ''))
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
                    _miss('  hand edit found no street to cut at', e['at'], e.get('note', ''))
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
                    _miss('  hand edit found no street to reshape at', e['at'], e.get('note', ''))
                elif best[1] == 'mains':
                    out['mains'][best[2]]['pts'] = pts
                else:
                    out[best[1]][d][best[2]] = pts
            elif op == 'add structure':   # a deck over the ground: {"kind": "skywalk" | "flyover" | "footbridge", "name", "pts", "width", "layer"}
                out.setdefault('structures', []).append({'d': d, 'kind': e['kind'], 'name': e.get('name', ''), 'pts': e['pts'],
                                                         'width': e.get('width', 3), 'layer': e.get('layer', 1)})
            elif op == 'add path':   # a footpath (no gutters, no traffic): {"pts"}
                out.setdefault('paths', {}).setdefault(d, []).append([[round(x, 1), round(y, 1)] for x, y in e['pts']])
            elif op == 'delete path':   # the footpath nearest the point (within 3 m)
                P = Point(e['at']); L_ = (out.get('paths') or {}).get(d, [])
                c = [(LineString(p).distance(P), i) for i, p in enumerate(L_) if len(p) > 1]
                c = [x for x in c if x[0] < 3]
                if c:
                    L_.pop(min(c)[1])
                else:
                    _miss('  hand edit found no path at', e['at'], e.get('note', ''))
            elif op == 'delete main':   # a district main road taken away: {"at"} (the main nearest the point, within 4 m)
                P = Point(e['at'])
                c = [(LineString(m['pts']).distance(P), i) for i, m in enumerate(out['mains']) if m.get('d') == d and len(m['pts']) > 1]
                c = [x for x in c if x[0] < 4]
                if c:
                    out['mains'].pop(min(c)[1])
                else:
                    _miss('  hand edit found no main at', e['at'], e.get('note', ''))
            elif op == 'delete structure':   # a deck taken down: {"name"} (every piece of that name in the district)
                n0 = len(out.get('structures', []))
                out['structures'] = [x for x in out.get('structures', []) if not (x.get('d') == d and x.get('name') == e['name'])]
                if len(out['structures']) == n0:
                    _miss('  hand edit found no structure named', e['name'])
            elif op == 'name road':
                P = Point(e['at'])
                c = [(LineString(m['pts']).distance(P), i) for i, m in enumerate(out['mains']) if len(m['pts']) > 1]
                c = [x for x in c if x[0] < 3]
                if c:
                    out['mains'][min(c)[1]]['name'] = e['name']
                else:
                    _miss('  hand edit found no main road at', e['at'], e.get('note', ''))
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
                    _miss('  hand edit found no road at', e['at'], e.get('note', '')); continue
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
                    _miss('  hand edit found no', e.get('kind', 'furniture'), 'at', e['at'], e.get('note', '')); continue
            rep[d] = rep.get(d, 0) + 1
    return rep


WALL_OPS = ('cut wall', 'delete wall', 'add wall', 'add gate', 'delete gate')
DETAIL_OPS = ('set front', 'add tree', 'move tree', 'delete tree')
THING_OPS = ('add thing', 'move thing', 'delete thing')
HOUSE_OPS = ('set house',)
PAINT_OPS = ('add paint', 'delete paint')
REPLAY = ('set surface',) + WALL_OPS + DETAIL_OPS + THING_OPS + HOUSE_OPS + PAINT_OPS   # see _files


def apply_paint_edits(out):
    """{"op": "add paint", "k": "grass" | "dry grass" | "mud" | "dirt" | "sand" | "concrete", "pts": ring}  /
    {"op": "delete paint", "at": [x, y], "k" (optional)}: the painted area holding the point (scripts/groundpaint.py)."""
    rep = {}
    A = out.setdefault('ground_paint', {}).setdefault('areas', [])
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            if e['op'] not in PAINT_OPS:
                continue
            if e['op'] == 'add paint':
                A.append({'k': e['k'], 'pts': [[round(x, 1), round(y, 1)] for x, y in e['pts']], 'd': d, 's': 0})
            else:
                P = Point(e['at'])
                hit = [i for i, a in enumerate(A) if (not e.get('k') or a['k'] == e['k']) and len(a['pts']) > 2 and Polygon(a['pts']).buffer(0).contains(P)]
                if not hit:
                    _miss('  hand edit found no paint at', e['at'], e.get('note', '')); continue
                A.pop(hit[-1])
            rep[d] = rep.get(d, 0) + 1
    return rep


def apply_house_edits(out):
    """{"op": "set house", "at": [x, y], "kind" (optional), "flat": 0/1, "unf": 0/1, "tank": [x, y] | 0, "dish": [x, y] | 0, "tyres": n}:
    the house holding the point takes any of these (scripts/houses.py)."""
    _BOX.clear()   # footprints may have been changed in place since the last stage
    rep = {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            if e['op'] not in HOUSE_OPS:
                continue
            P = Point(e['at'])
            hit = _hits(out, d, P, e.get('kind'))
            if not hit:
                _miss('  hand edit found no house at', e['at'], e.get('note', '')); continue
            h = out.setdefault('houses', {}).setdefault(d, {}).setdefault(str(hit[0]), {'flat': 1, 'unf': 0, 'tank': 0, 'dish': 0, 'tyres': 0})
            for k in ('flat', 'unf', 'tank', 'dish', 'tyres'):
                if k in e:
                    h[k] = e[k]
            rep[d] = rep.get(d, 0) + 1
    return rep


def apply_thing_edits(out):
    """Edits to the things the bake places (scripts/things.py): parked vehicles, people standing, boats, trains, stalls.
    {"op": "add thing", "k": kind, "x", "y", "a": degrees, ...}  /  {"op": "move thing", "at", "k" (optional), "to", "a" (optional)}
    /  {"op": "delete thing", "at", "k" (optional)}: the nearest within 2 m."""
    rep = {}
    T = out.setdefault('things', [])
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op not in THING_OPS:
                continue
            if op == 'add thing':
                T.append({k: v for k, v in e.items() if k not in ('op', 'note')} | {'d': e.get('d', d)})
            else:
                P = Point(e['at'])
                c = [(Point(t['x'], t['y']).distance(P), i) for i, t in enumerate(T) if not e.get('k') or t['k'] == e['k']]
                c = [x for x in c if x[0] < 2.0]
                if not c:
                    _miss('  hand edit found no', e.get('k', 'thing'), 'at', e['at'], e.get('note', '')); continue
                if op == 'delete thing':
                    T.pop(min(c)[1])
                else:
                    t = T[min(c)[1]]
                    t['x'], t['y'] = e['to']
                    if 'a' in e:
                        t['a'] = e['a']
            rep[d] = rep.get(d, 0) + 1
    return rep


LATE = []   # furniture edits that found nothing in apply_edits: tried again once the bush furniture is placed


def apply_late_furniture(out):
    """The furniture edits apply_edits could not place: the poles and lights out in the bush are placed after it."""
    n = 0
    for d, e in LATE:
        _D[0] = d
        P = Point(e['at'])
        key, lim = ('monuments', 3.0) if e['op'].endswith('monument') else ('furniture', 2.0)
        c = [(Point(f_['x'], f_['y']).distance(P), i) for i, f_ in enumerate(out.get(key, [])) if key == 'monuments' or not e.get('kind') or f_['kind'] == e['kind']]
        c = [x for x in c if x[0] < lim]
        if not c:
            _miss('  hand edit found no', key[:-1] if key == 'monuments' else 'furniture', 'at', e['at'], e.get('note', '')); continue
        if e['op'].startswith('delete'):
            out[key].pop(min(c)[1])
        else:
            f_ = out[key][min(c)[1]]
            f_['x'], f_['y'] = e['to']
            if 'ang' in e:
                f_['ang'] = e['ang']
        n += 1
    LATE.clear()
    return n


def apply_detail_edits(out):
    """Edits to the house fronts and trees (scripts/fronts.py, scripts/trees.py), after they are worked out:
    {"op": "set front", "at": [x, y], "kind": .., "e": side, "shop": 0/1, "aw": canopy m, "bal": [sides]}   any of e/shop/aw/bal
    {"op": "add tree", "x", "y", "kind": "palm"|"broad"}  /  {"op": "move tree", "at", "to"}  /  {"op": "delete tree", "at"} (within 2 m)"""
    _BOX.clear()   # footprints may have been changed in place since the last stage
    rep = {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op not in DETAIL_OPS:
                continue
            if op == 'set front':
                P = Point(e['at'])
                hit = _hits(out, d, P, e.get('kind'))
                if not hit:
                    _miss('  hand edit found no house at', e['at'], e.get('note', '')); continue
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
                        _miss('  hand edit found no tree at', e['at'], e.get('note', '')); continue
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
                    _miss('  hand edit found no wall at', e['at'], e.get('note', '')); continue
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
                    _miss('  hand edit found no gate at', e['at'], e.get('note', '')); continue
            rep[d] = rep.get(d, 0) + 1
    return rep


def apply_edits(out):
    _BOX.clear()   # footprints may have been changed in place since the last stage
    rep = {}
    for f, H in _files():
        d = H['district']
        for e in H.get('edits', []):
            op = e['op']
            if op in ROAD_OPS or op in LABEL_OPS or op in WALL_OPS or op in DETAIL_OPS or e.get('early'):
                continue   # applied earlier in the bake (apply_road_edits, apply_label_edits)
            if op == 'add building':
                _add_building(out, d, e['kind'], e['pts'], e.get('storeys', 1))
            elif op == 'clear area':
                _clear_area(out, d, e, 'late')
            elif op == 'set storeys':   # the building holding the point gets this many storeys: {"at", "kind" (optional), "storeys"}
                P = Point(e['at'])
                hit = _hits(out, d, P, e.get('kind'))
                if not hit:
                    _miss('  hand edit found nothing at', e['at'], op, e.get('note', '')); continue
                out['storeys'][d][hit[0]] = int(e['storeys'])
            elif op in ('delete building', 'move building'):
                P = Point(e['at'])
                hit = _hits(out, d, P, e.get('kind'))
                if not hit:
                    _miss('  hand edit found nothing at', e['at'], op, e.get('note', '')); continue
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
                hit = _hits(out, d, P, e.get('kind'))
                if not hit:
                    _miss('  hand edit found nothing at', e['at'], op, e.get('note', '')); continue
                out['buildings'][d][hit[0]] = [out['buildings'][d][hit[0]][0]] + [[round(x, 1), round(y, 1)] for x, y in e['pts']]
            elif op in ('reshape parcel', 'reshape zone'):   # the plot (or market zone) holding the point takes a new outline
                P = Point(e['at']); pts = [[round(x, 1), round(y, 1)] for x, y in e['pts']]
                L_ = (out.get('parcels') or {}).get(d, []) if op == 'reshape parcel' else [z for z in out.get('encroach', []) if z.get('d') == d]
                hit = [q for q in L_ if Polygon(q['pts']).buffer(0.5).contains(P)]
                if not hit:
                    _miss('  hand edit found nothing at', e['at'], op, e.get('note', '')); continue
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
                    LATE.append((d, e))   # out in the bush: its furniture is placed after the road ends (apply_late_furniture)
            elif op == 'move furniture':   # the nearest of its kind within 2 m goes to "to", turned to "ang"
                P = Point(e['at'])
                c = [(Point(f_['x'], f_['y']).distance(P), i) for i, f_ in enumerate(out.get('furniture', [])) if not e.get('kind') or f_['kind'] == e['kind']]
                c = [x for x in c if x[0] < 2.0]
                if not c:
                    LATE.append((d, e)); continue
                f_ = out['furniture'][min(c)[1]]
                f_['x'], f_['y'] = e['to']
                if 'ang' in e:
                    f_['ang'] = e['ang']
            elif op in ('move monument', 'delete monument'):   # the nearest within 3 m
                P = Point(e['at'])
                c = [(Point(m['x'], m['y']).distance(P), i) for i, m in enumerate(out.get('monuments', []))]
                c = [x for x in c if x[0] < 3.0]
                if not c:
                    LATE.append((d, e)); continue   # one the bake places by rule (scripts/things.py): after it is placed
                if op == 'delete monument':
                    out['monuments'].pop(min(c)[1])
                else:
                    m = out['monuments'][min(c)[1]]
                    m['x'], m['y'] = e['to']
                    if 'ang' in e:
                        m['ang'] = e['ang']
            elif op == 'delete place':   # every place of that name, or with "at" only the one within 5 m of it
                n0 = len(out['pois'])
                out['pois'] = [p for p in out['pois'] if p['name'] != e['name'] or ('at' in e and Point(p['x'], p['y']).distance(Point(e['at'])) > 5)]
                if len(out['pois']) == n0:
                    _miss('  hand edit found no place called', e['name']); continue
            elif op == 'add place':   # a named place (a pin): {"name", "type", "x", "y", "note"}
                out['pois'].append({'name': e['name'], 'type': e['type'], 'note': e.get('note', ''), 'd': d, 'x': e['x'], 'y': e['y'], 'hand': True})
            elif op == 'move place':  # a named place moves: {"name", "x", "y"}
                q = next((p for p in out['pois'] if p['name'] == e['name']), None)
                if q is None:
                    _miss('  hand edit found no place called', e['name']); continue
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
                    _miss('  hand edit found no plot at', e['at'], e.get('note', ''))
            elif op == 'add monument':   # placed by hand (blender/gidi_kit/monuments.py): {"model", "x", "y", "ang", "name", "span"}
                out.setdefault('monuments', []).append({k: e[k] for k in ('model', 'x', 'y', 'ang') if k in e} | {'d': d, 'name': e.get('name', ''), **({'span': e['span']} if 'span' in e else {})})
            elif op == 'add zone':
                out.setdefault('encroach', []).append({'kind': e['kind'], 'd': d, 'pts': e['pts']})
            rep[d] = rep.get(d, 0) + 1
    return rep
