"""What kind of road each street is (owner, 18 Oct 2026: "I don't think we understand things like closes, crescents, drives,
ways"). The streets are stored in pieces; this joins the pieces back into whole streets (pieces that meet end to end and
carry straight on), types each whole street by its shape and its district, and gives every piece its street's type:

  close      a dead end under CLOSE_MAX m (a turning space, a gate or a house at the end; scripts/roadends.py)
  crescent   leaves a road and comes back onto the same road, bending on the way (longer than its chord by CRESCENT_BEND)
  drive      the long spine of an estate (elite districts): its longest through streets, DRIVE_MIN m and more
  avenue     a long, straight through street in the civic district or the estates, AVENUE_MIN m and more
  street     everything else
  lane       the narrow lanes (as the generator drew them)

out["road_types"] = {road id ("<district>/street/<i>" | "<district>/lane/<i>"): type}. The board shows the type and the kit
can dress by it (trees on avenues, kerbs on drives). Hand edit: "set road type" (scripts/hand.py).
"""
import math

from shapely.geometry import LineString, Point
from shapely.ops import linemerge, unary_union
from shapely.strtree import STRtree

CHARACTER = {'maze': 'dense', 'hub': 'dense', 'jungle': 'dense', 'foodgate': 'dense', 'bazaar': 'dense',
             'railside': 'sprawl', 'frontier': 'sprawl', 'border': 'sprawl', 'oldisland': 'old_island', 'oldshore': 'old_island',
             'estate': 'elite', 'heights': 'elite', 'capital': 'civic', 'watertown': 'waterfront', 'port': 'port'}
CLOSE_MAX = 160.0
CRESCENT_BEND = 1.15
DRIVE_MIN = 500.0
AVENUE_MIN = 600.0
TOUCH = 3.0
STRAIGHT = 35.0   # degrees: a street carries on through a junction along the piece that turns least, if it turns less than this


def _chains(U):
    """Whole streets from the noded network: at every junction a street carries straight on (the piece that turns least,
    under STRAIGHT degrees), so a spine crossed by side streets stays one street."""
    segs = list(getattr(U, 'geoms', [U]))
    key = lambda c: (round(c[0], 1), round(c[1], 1))
    at = {}
    for i, g in enumerate(segs):
        c = list(g.coords)
        for end, (p, q) in ((0, (c[0], c[1])), (1, (c[-1], c[-2]))):
            at.setdefault(key(p), []).append((i, end, math.atan2(q[1] - p[1], q[0] - p[0])))
    nxt = {}   # (segment, end) -> (segment, end) it carries straight on into
    for node, es in at.items():
        pairs = sorted(((abs(math.degrees(math.pi - abs((a[2] - b[2] + math.pi) % (2 * math.pi) - math.pi))), a, b)
                        for k, a in enumerate(es) for b in es[k + 1:] if a[0] != b[0]), key=lambda x: x[0])
        used = set()
        for turn, a, b in pairs:
            if turn < STRAIGHT and a[:2] not in used and b[:2] not in used:
                nxt[a[:2]] = b[:2]; nxt[b[:2]] = a[:2]; used |= {a[:2], b[:2]}
    seen, out = set(), []
    for i in range(len(segs)):
        if i in seen:
            continue
        start, e = i, 0   # walk back to the start of this street, then forward to its end
        while (start, e) in nxt and nxt[(start, e)][0] != i:
            j, ej = nxt[(start, e)]
            if j in seen or j == start:
                break
            start, e = j, 1 - ej
            if start == i:
                break
        cur, ce, line = start, e, []
        while True:
            seen.add(cur)
            c = list(segs[cur].coords)
            c = c if ce == 0 else c[::-1]
            line += c if not line else c[1:]
            n = nxt.get((cur, 1 - ce))
            if n is None or n[0] in seen:
                break
            cur, ce = n
        out.append(LineString(line))
    return out


def _typed(lines, big, rule):
    """Type each line by rule(line, meets at start, meets at end, chord); returns (lines, types, tree)."""
    others = lines + big
    T = STRtree(others)
    ts = []
    for k, c in enumerate(lines):
        e0, e1 = Point(c.coords[0]), Point(c.coords[-1])
        m0 = [j for j in T.query(e0.buffer(TOUCH)) if j != k and others[j].distance(e0) < TOUCH]
        m1 = [j for j in T.query(e1.buffer(TOUCH)) if j != k and others[j].distance(e1) < TOUCH]
        ts.append(rule(c, m0, m1, e0.distance(e1) or 1.0))
    return lines, ts, STRtree(lines)


def types(out):
    big = [LineString(m['pts']) for m in out.get('mains', []) if len(m['pts']) > 1]
    big += [LineString(a['pts']) for a in out.get('arterials', []) if a['cls'] != 'bridge' and len(a['pts']) > 1]
    res, rep = {}, {}
    for d in sorted(out.get('streets') or {}):
        ch = CHARACTER.get(d, 'dense')
        pieces = [(i, LineString(p)) for i, p in enumerate(out['streets'][d]) if len(p) > 1]
        for i, p in enumerate((out.get('lanes') or {}).get(d, [])):
            if len(p) > 1:
                res[f'{d}/lane/{i}'] = 'lane'
        if not pieces:
            continue
        U = unary_union([g for _, g in pieces])
        cmax = CLOSE_MAX * (2 if ch == 'elite' else 1)   # an estate's closes run the depth of a block of plots

        def short(c, m0, m1, chord):   # junction to junction: closes and crescents
            if (not m0 or not m1) and c.length < cmax:
                return 'close'
            if m0 and m1 and set(m0) & set(m1) and c.length > 50 and c.length / chord > CRESCENT_BEND:
                return 'crescent'
            return None

        def long(c, m0, m1, chord):   # straight on through the junctions: drives and avenues
            if ch == 'elite' and m0 and m1 and c.length >= DRIVE_MIN:
                return 'drive'
            if ch in ('civic', 'elite') and m0 and m1 and c.length >= AVENUE_MIN and c.length / chord < 1.08:
                return 'avenue'
            return None
        m = linemerge(U)
        passes = [_typed(list(getattr(m, 'geoms', [m])), big, short), _typed(_chains(U), big, long)]
        for i, g in pieces:   # a piece is a close or crescent if its junction-to-junction run is; else a drive or avenue if its street is
            mid = g.interpolate(0.5, normalized=True)
            t = 'street'
            for lines, ts, tree in passes:
                ks = [k for k in tree.query(mid.buffer(0.5)) if lines[k].distance(mid) < 0.5 and ts[k]]
                if ks:
                    t = ts[ks[0]]
                    break
            res[f'{d}/street/{i}'] = t
            rep[t] = rep.get(t, 0) + 1
    out['road_types'] = dict(sorted(res.items()))
    return rep
