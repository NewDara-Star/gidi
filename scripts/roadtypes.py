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
        merged = linemerge(unary_union([g for _, g in pieces]))
        chains = list(getattr(merged, 'geoms', [merged]))
        others = chains + big
        T = STRtree(others)
        CT = STRtree(chains)
        ctype = []
        for k, c in enumerate(chains):
            ends = [Point(c.coords[0]), Point(c.coords[-1])]

            def meets(q):   # the roads an end touches, other than its own chain
                return [j for j in T.query(q.buffer(TOUCH)) if j != k and others[j].distance(q) < TOUCH]
            m0, m1 = meets(ends[0]), meets(ends[1])
            chord = ends[0].distance(ends[1]) or 1.0
            t = 'street'
            if (not m0 or not m1) and c.length < CLOSE_MAX:
                t = 'close'
            elif m0 and m1 and set(m0) & set(m1) and c.length > 50 and c.length / chord > CRESCENT_BEND:
                t = 'crescent'
            elif ch == 'elite' and m0 and m1 and c.length >= DRIVE_MIN:
                t = 'drive'
            elif ch in ('civic', 'elite') and m0 and m1 and c.length >= AVENUE_MIN and c.length / chord < 1.08:
                t = 'avenue'
            ctype.append(t)
        for i, g in pieces:   # each piece takes the type of the chain it lies on
            mid = g.interpolate(0.5, normalized=True)
            ks = [k for k in CT.query(mid.buffer(0.5)) if chains[k].distance(mid) < 0.5]
            t = ctype[ks[0]] if ks else 'street'
            res[f'{d}/street/{i}'] = t
            rep[t] = rep.get(t, 0) + 1
    out['road_types'] = dict(sorted(res.items()))
    return rep
