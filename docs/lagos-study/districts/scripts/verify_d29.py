"""Re-check the data claims of docs/lagos-study/districts/d29.md (the scout note of 27 Oct).

Run:  ~/.venvs/gidi/bin/python -I verify_d29.py
Prints one line per claim: id | what the note stated BEFORE the 28 Oct check | what the data gives | verdict.
FALSE rows are the claims corrected in d29.md ("corrected on check"); SEE rows print numbers to judge by eye.
Web claims are not in this script (see d29.md's "Checked:" list).
Sources read: web/frame-study.js (frame outline, frame roads, districts), map/d15|d27|d28 plan.json,
district.json and STREETS.md, docs/lagos-study/roads/places.csv, borders.csv, EARTH-CHECK.md,
NAMES.md, docs/lagos-study/LIVING.md, STUDY.md, docs/lagos-lgas-research.md, and Overture
(~/gidi-data/research/data/overture-lagos: place, segment, land_use, infrastructure). Overture's land
use and infrastructure carry the OSM tags they came from (source_tags), so they stand in as a second
read of the note's OSM claims; claims only Overpass could answer (lanes, gauge, buildings) are listed
as NOT CHECKABLE here.
Game positions use scripts/working_bar.py's own gidi() (imported, not copied).
"""
import collections
import json
import os
import re
import sys

import numpy as np
import pyarrow.parquet as pq
import shapely
from shapely import wkb
from shapely.geometry import LineString, Point, Polygon
from pyproj import Transformer

ROOT = os.path.expanduser("~/gidi")
OV = os.path.expanduser("~/gidi-data/research/data/overture-lagos/")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from working_bar import gidi as wb_gidi  # noqa: E402

T = Transformer.from_crs(4326, 32631, always_xy=True)


def gidi(lon, lat):
    return wb_gidi(lon, lat, T)


ROWS = []
TALLY = collections.Counter()


def claim(cid, stated, found, ok):
    v = {True: "TRUE", False: "FALSE", None: "SEE"}[ok]
    TALLY[v] += 1
    ROWS.append(f"{cid:<8} | stated: {stated} | found: {found} | {v}")


def near(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def r0(p):
    return tuple(round(v, 1) for v in p)


# ---------------------------------------------------------------- frame
s = open(os.path.join(ROOT, "web/frame-study.js")).read()
F = json.loads(s[s.index("{"): s.rstrip().rstrip(";").rindex("}") + 1])
DIST = {}
for z in F["districts"]:
    DIST[z["n"]] = shapely.unary_union([Polygon(r[0], r[1:]) for r in z["rings"]])
P = DIST[29]
ring = F["districts"][[z["n"] for z in F["districts"]].index(29)]["rings"]
ringpts = [tuple(p) for p in ring[0][0]]

# ---------------------------------------------------------------- Overture loads (bbox-filtered)
BOX = (3.343, 3.370, 6.538, 6.575)


def inbox(b):
    return b["xmax"] > BOX[0] and b["xmin"] < BOX[1] and b["ymax"] > BOX[2] and b["ymin"] < BOX[3]


def to_game(g):
    return shapely.transform(g, lambda a: np.array([gidi(x, y) for x, y in a]))


def load(name):
    t = pq.read_table(OV + name)
    bb = t.column("bbox").to_pylist()
    idx = [i for i, b in enumerate(bb) if inbox(b)]
    rows = t.take(idx).to_pylist()
    for r in rows:
        r["_g"] = to_game(wkb.loads(r["geometry"]))
        r["_n"] = (r.get("names") or {}).get("primary") or ""
    return rows


places = load("lagos_overture_place.parquet")
segs = load("lagos_overture_segment.parquet")
landuse = load("lagos_overture_land_use.parquet")
infra = load("lagos_overture_infrastructure.parquet")
pin = [r for r in places if P.contains(r["_g"])]

# ================================================================ section 1
claim("1.1", "outline 0.513 km2 game, 4.62 km2 real", f"{P.area/1e6:.4f} km2 game, {P.area*9/1e6:.2f} real",
      round(P.area / 1e6, 3) == 0.513 and round(P.area * 9 / 1e6, 2) == 4.62)
claim("1.2", "one ring of 48 points", f"{len(ring)} ring(s), {len(ringpts)} pts incl. closing = {len(set(ringpts))} distinct",
      len(ring) == 1 and len(set(ringpts)) == 48)
b = P.bounds
claim("1.3", "bbox x 12575-13342, y 4275-5458", f"x {b[0]:.1f}-{b[2]:.1f}, y {b[1]:.1f}-{b[3]:.1f}",
      near(b, (12575, 4275, 13342, 5458), 1))
inv = Transformer.from_crs(32631, 4326, always_xy=True)
lo0, la0 = inv.transform(b[0] * 3 + 500525, 707825 + (10500 - b[3]) * 3)
lo1, la1 = inv.transform(b[2] * 3 + 500525, 707825 + (10500 - b[1]) * 3)
claim("1.4", "6.540-6.5725 N, 3.346-3.367 E", f"{la0:.4f}-{la1:.4f} N, {lo0:.4f}-{lo1:.4f} E",
      abs(la0 - 6.540) < 0.001 and abs(la1 - 6.5725) < 0.001 and abs(lo0 - 3.346) < 0.001 and abs(lo1 - 3.367) < 0.001)

ec = [l for l in open(os.path.join(ROOT, "docs/lagos-study/roads/EARTH-CHECK.md")) if l.startswith("| 29 |")]
claim("1.5", "members Ilupeju + Shogunle east of Agege Motor Road [EC row 29]", ec[0].strip() if ec else "row missing",
      bool(ec) and "Shogunle east of Agege Motor Road" in ec[0])

cant = [r for r in landuse if r["_n"] == "Ikeja Cantonment"][0]
cg = cant["_g"]
sh = {k: cg.intersection(v).area / cg.area for k, v in DIST.items() if cg.intersects(v)}
inside = cg.intersection(P).area
claim("1.6", "cantonment 191,086 m2 of 513,494 m2 (37%)", f"{inside:,.0f} of {P.area:,.0f} ({inside/P.area:.1%})",
      round(inside) == 191086 and round(P.area) == 513494)
claim("1.7", "polygon 92.6% d29, 7.3% d35, 0.1% d34",
      ", ".join(f"d{k} {v:.2%}" for k, v in sorted(sh.items()) if v > 0), abs(sh[29] - .926) < .001 and abs(sh[35] - .073) < .001)
st = dict(cant["source_tags"] or {})
claim("1.8", "alt name Nigerian Army Cantonment, landuse military", f"{st.get('alt_name')}, landuse {st.get('landuse')}",
      st.get("alt_name") == "Nigerian Army Cantonment" and st.get("landuse") == "military")
pl = [l for l in open(os.path.join(ROOT, "docs/lagos-study/roads/places.csv")) if l.startswith("6,")]
claim("1.9", "'Shogunle, east of Agege Motor Road' fabric barracks", pl[0].split(",")[3] if pl else "?",
      bool(pl) and ",barracks," in pl[0])
cp = [r for r in pin if "Millitary Cantonment" in r["_n"]]
claim("1.10", "Overture 'Ikeja Millitary Cantonment' 6.5618,3.3608 = game 13121,4668",
      f"{cp[0]['_n']} game {r0((cp[0]['_g'].x, cp[0]['_g'].y))}" if cp else "none",
      bool(cp) and near((cp[0]["_g"].x, cp[0]["_g"].y), (13121, 4668), 2))

arena = [r for r in landuse if r["_n"] == "The Arena"][0]
ag = arena["_g"]
claim("1.11", "The Arena 15,489 m2, wholly in d29, ~3%, alt name Nigerian Army Shopping Arena",
      f"{ag.area:,.0f} m2, in d29 {ag.intersection(P).area/ag.area:.0%}, {ag.area/P.area:.1%}, alt {dict(arena['source_tags']).get('alt_name')}",
      round(ag.area) == 15489 and ag.intersection(P).area / ag.area > .999)
ind = [r for r in landuse if r["class"] == "industrial" and r["_g"].intersects(P)]
areas = sorted(round(r["_g"].area) for r in ind)
whole = all(r["_g"].intersection(P).area / r["_g"].area > .999 for r in ind)
claim("1.12", "two industrial polygons 80,332 and 50,077 m2, both wholly inside, about 25%",
      f"{len(ind)} polygons {areas}, wholly inside {whole}, {sum(areas)/P.area:.1%}",
      areas == [50077, 80332] and whole)

ils = gidi(3.36416, 6.55188)
d27 = json.load(open(os.path.join(ROOT, "map/d27/district.json")))
d27o = [r for r in d27["records"] if r["type"] == "district"][0]["outline"]


def outline_poly(o):
    t, depth = o, 0
    while not isinstance(t[0], (int, float)):
        t, depth = t[0], depth + 1
    if depth == 2:
        return Polygon(o[0], o[1:])
    return shapely.unary_union([Polygon(p[0], p[1:]) for p in o])


D27 = outline_poly(d27o)
claim("1.13", "Indian Language School 6.55188,3.36416 = game 13245,5033, in d27's drawn outline",
      f"game {r0(ils)}, in d27 {D27.contains(Point(ils))}, in d29 frame {P.contains(Point(ils))}",
      near(ils, (13245, 5033), 1) and D27.contains(Point(ils)))

# "residential estate west of Coker Road" and "the streets east of Coker Road and south of y 5025 are in d27"
coker = [r for r in segs if r["_n"] == "Coker Road"]
cx = np.mean([c[0] for r in coker for c in r["_g"].coords])
side = {}
for nm in ["Johnson Street", "Olutanda Street", "Ilaka Street", "Ashimowu Jibowu Street", "Ashimowa Close",
           "Olusoji Idowu Street", "Akinsete Drive", "Oyetola Idowu Street", "Oduwobi Street", "Adeyinka Street",
           "Esther Oshiyemi Street", "Folayemi Street", "Micheal Adekoya Street", "Bello Crescent", "Adepebga Street",
           "Aina Eleko Street", "Iya Oloye Crescent"]:
    rs = [r for r in segs if r["_n"] == nm and r["_g"].intersects(P)]
    if not rs:
        side[nm] = "not inside"
        continue
    g = shapely.unary_union([r["_g"].intersection(P) for r in rs])
    c = g.centroid
    side[nm] = f"x{c.x:.0f},y{c.y:.0f} {'E' if c.x > cx else 'W'}{' N-of-expwy' if c.y < 4790 else ''}"
east = [k for k, v in side.items() if " E" in v or v.split()[1].startswith("E")]
claim("1.14", "the residential estate is west of Coker Road (sections 1 and 3: 'south of the expressway, west of Coker Road')",
      f"Coker Road mean x {cx:.0f}; " + "; ".join(f"{k} {v}" for k, v in side.items()), False)

lcda = [r for r in pin if r["_n"].startswith("Odiolowo Ojuwoye Local Council")]
claim("1.15", "LCDA office on Town Planning Way at 13104,4856",
      f"{lcda[0]['_n']} at {r0((lcda[0]['_g'].x, lcda[0]['_g'].y))}" if lcda else "none",
      bool(lcda) and near((lcda[0]["_g"].x, lcda[0]["_g"].y), (13104, 4856), 1))
nm = [l for l in open(os.path.join(ROOT, "docs/lagos-study/roads/NAMES.md")) if l.startswith("| 29 |")]
claim("1.16", "NAMES.md row 29: Ìlúpẹ̀lẹ́, 'the gentle town'", nm[0].strip() if nm else "?",
      bool(nm) and "Ìlúpẹ̀lẹ́" in nm[0] and "the gentle town" in nm[0])
liv = open(os.path.join(ROOT, "docs/lagos-study/LIVING.md")).read()
claim("1.17", "LIVING's LGA '[K, check]'", re.search(r"#### 29\..*", liv).group(0), "[K, check]" in re.search(r"#### 29\..*", liv).group(0))
lga = open(os.path.join(ROOT, "docs/lagos-lgas-research.md")).read().splitlines()
claim("1.18", "LGA lines 1224/1639: canal Oke-Afa, at least 600 drowned, ~1,100 died; 1684 real victims/name to avoid",
      f"1224: {lga[1223][:90]}... | 1684: {lga[1683]}", "Oke-Afa" in lga[1223] and "cantonment" in lga[1683])

# ================================================================ section 2: seams
nb = {30: (15, 667), 32: (12, 574), 15: (6, 391), 27: (6, 452), 35: (4, 602), 34: (3, 586), 28: (2, 419)}
tot = 0
for n, (pts, L) in nb.items():
    zp = set(tuple(p) for r in [z for z in F["districts"] if z["n"] == n][0]["rings"] for rr in r for p in rr)
    shp = len(set(ringpts) & zp)
    sl = P.exterior.intersection(DIST[n].boundary.buffer(1)).length
    tot += sl
    claim(f"2.d{n}", f"{pts} points, {L} m", f"{shp} points, {sl:.0f} m", shp == pts and round(sl) == L)
others = [n for n in DIST if n not in nb and n != 29 and P.exterior.intersection(DIST[n].boundary.buffer(1)).length > 0]
claim("2.sum", "seams sum 3,691 m, perimeter 3,676 m; no other neighbour", f"sum {tot:.0f}, perimeter {P.length:.0f}, others {others}",
      abs(tot - 3691) <= 1 and round(P.length) == 3676 and not others)
for dn, n, want in (("d15", 15, 6), ("d27", 27, 6), ("d28", 28, 2)):
    j = json.load(open(os.path.join(ROOT, f"map/{dn}/district.json")))
    o = [r for r in j["records"] if r["type"] == "district"][0]["outline"]
    M = outline_poly(o)
    zp = set(tuple(p) for r in [z for z in F["districts"] if z["n"] == n][0]["rings"] for rr in r for p in rr)
    shared = set(ringpts) & zp
    flat = set(tuple(c) for c in M.exterior.coords) if M.geom_type == "Polygon" else set(
        tuple(c) for g in M.geoms for c in g.exterior.coords)
    extra = f", outline vs frame differs {M.symmetric_difference(DIST[n]).area:,.0f} m2" if n == 15 else ""
    claim(f"2.map{n}", f"{dn}/district.json holds all {want} shared points" + (", 308,404 m2 off the frame" if n == 15 else ""),
          f"{len(shared & flat)} of {len(shared)}{extra}",
          len(shared & flat) == want and (n != 15 or round(M.symmetric_difference(DIST[n]).area) == 308404))

# neighbours' road ends at the d29 edge
names = {}
for dn in ("d15", "d27", "d28"):
    for line in open(os.path.join(ROOT, f"map/{dn}/STREETS.md")):
        if line.startswith("| rd-") or line.startswith("| rl-"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            names[c[0]] = c[2] if dn == "d15" else c[1]
REC = {}
ends = collections.defaultdict(list)
for dn in ("d15", "d27", "d28"):
    for r in json.load(open(os.path.join(ROOT, f"map/{dn}/plan.json")))["records"]:
        if r["type"] in ("road", "rail"):
            REC[r["id"]] = (dn, r)
            for e in (r["centreline"][0], r["centreline"][-1]):
                dd = P.exterior.distance(Point(e))
                if dd < 6 or P.contains(Point(e)):
                    ends[dn].append((r["id"], names.get(r["id"], "?"), r.get("kind"), r.get("width"), r0(e),
                                     round(dd, 1), P.contains(Point(e))))
for dn in ends:
    ROWS.append(f"   info  | {dn} road/rail ends within 6 m of the d29 frame edge or inside it:")
    for e in ends[dn]:
        ROWS.append(f"         |   {e}")

ik = REC["rd-9e02217d"][1]
claim("2.r1", "d28 rd-9e02217d motorway 40 m from (13342.0,4695.8) to (13349.6,5025.2)",
      f"{ik['kind']} {ik['width']} m from {r0(ik['centreline'][0])} to {r0(ik['centreline'][-1])}",
      ik["width"] == 40 and {r0(ik["centreline"][0]), r0(ik["centreline"][-1])} >= {(13342.0, 4695.8)} and
      any(near(c, (13349.6, 5025.2), .1) for c in (ik["centreline"][0], ik["centreline"][-1])))
seam = LineString([(13341.7, 4608.3), (13341.7, 4775.0)])
ikl = LineString(ik["centreline"])
xs = [c[0] for c in ik["centreline"]]
claim("2.r1b", "about 20 m of d29's east strip is road (half of 40 m)",
      f"centreline x {min(xs):.1f}-{max(xs):.1f} vs d29 edge x 13341.7: west half reaches x {min(xs)-20:.1f}-{max(xs)-20:.1f}, "
      f"so {13341.7-(min(xs)-20):.1f} to {13341.7-(max(xs)-20):.1f} m of d29", None)
d28t = open(os.path.join(ROOT, "map/d28/STREETS.md")).read()
claim("2.r1c", "quote 'about half its width over the land west of it, which the district drawn there takes as held'",
      "found in d28 STREETS.md" if "about half its width over the land west of it, which the\n    district drawn there takes as held" in d28t or "about half its width over the land west of it" in d28t else "not found",
      "about half its width over the land west of it" in d28t)
ex = REC["rd-cbaebc6a"][1]
e0 = ex["centreline"][0]
claim("2.r2", "d28 rd-cbaebc6a (25 m) leaves Ikorodu Road at 'the shared point' (13345.46,4791.6), a point d29's expressway must start at",
      f"start {r0(e0)}, {ex['width']} m; that point is {P.exterior.distance(Point(e0)):.1f} m EAST of d29's edge (x 13341.7), "
      f"inside d29 {P.contains(Point(e0))}: a d28 road junction on its own Ikorodu Road, not a border point", False)
for rid, nmx, pt in (("rd-2fdc4dd5", "Anthony Village Road", (13344.3, 4759.4)), ("rd-c44a7b2c", "lane", (13342.3, 4704.9))):
    r = REC[rid][1]
    hit = [c for c in (r["centreline"][0], r["centreline"][-1]) if near(c, pt, .1)]
    claim(f"2.{rid[3:7]}", f"d28 {nmx} ends at {pt}", f"{names.get(rid)} end {r0(hit[0]) if hit else 'no end there'}", bool(hit))
ap = REC["rd-0bdae85c"][1]
ape = min((ap["centreline"][0], ap["centreline"][-1]), key=lambda c: P.exterior.distance(Point(c)))
claim("2.d28x", "d28 road ends on the seam: Ikorodu Road, expressway, Anthony Village Road, a lane (four)",
      f"also {names.get('rd-0bdae85c')} rd-0bdae85c (main road 10.75 m) ends at {r0(ape)}, "
      f"{P.exterior.distance(Point(ape)):.1f} m off the edge: not in the note", False)

stated27 = {"rd-396710ba": [(13175.0, 5225.3)], "Association Avenue": [(13158.3, 5169.4)],
            "Kolawole Shonibare Street": [(13158.3, 5144.0)], "lane1": [(13158.3, 5120.1)],
            "Adeola Adeleye Street": [(13175.0, 5081.2)], "Basheer Augusto Close": [(13176.7, 5056.0)],
            "Oba Nle Aro Street": [(13175.0, 5028.1), (13254.0, 5025.2)], "Aina George Street": [(13254.0, 5025.2)],
            "Oremeji Street": [(13236.8, 5026.2)], "Olusoji Idowu Street": [(13315.4, 5027.2)],
            "lane2": [(13302.9, 5025.0)], "lane3": [(13175.3, 5264.2)], "main": [(13177.7, 5274.7)]}
e27 = ends["d27"]
allpts = [e[4] for e in e27]
miss = [(k, p) for k, ps in stated27.items() for p in ps if not any(near(p, q, .15) for q in allpts)]
within3 = [e for e in e27 if e[5] <= 3]
unlisted = [e for e in e27 if not any(near(e[4], p, .15) for ps in stated27.values() for p in ps)]
claim("2.d27", "Ṣọmọlá's 13 road ends on the seam (14 points listed)",
      f"listed points not found: {miss}; within 3 m: {len(within3)} ends on {len(set(e[0] for e in within3))} records; "
      f"within 6 m but not listed: {[(e[0], e[1], e[4], e[5]) for e in unlisted if e[4] not in [p for ps in stated27.values() for p in ps]]}",
      None)
bp = REC["rd-396710ba"][1]
claim("2.bp", "Ilupeju Bye Pass rd-396710ba local main 8.5 m", f"{bp['kind']} {bp['width']} ({names.get('rd-396710ba')})",
      bp["kind"] == "local_main" and bp["width"] == 8.5)
d27c = [k for k, v in names.items() if v == "Coker Road" and REC.get(k, ("",))[0] == "d27"]
fc = [r for r in F["roads"] if r["n"] == "Coker Road" and LineString(r["p"]).intersects(P)]
fcb = shapely.unary_union([LineString(r["p"]).intersection(P) for r in fc]).bounds
claim("2.coker", "Coker Road (frame x 13152-13179) not drawn by Ṣọmọlá", f"d27 Coker Road records {d27c}; frame x {fcb[0]:.0f}-{fcb[2]:.0f}",
      not d27c and round(fcb[0]) == 13152 and round(fcb[2]) == 13179)
rl = REC["rl-u7rtwbrj"][1]
claim("2.rail", "d15 rl-u7rtwbrj 4 tracks, 18 m, stone, walls both sides, ends inside d29 at (12998.7,5378.3)",
      f"{rl['tracks']} tracks, {rl['corridor']} m, {rl['ballast']}, {rl['fence_left']}/{rl['fence_right']}, end {r0(rl['centreline'][-1])} inside {P.contains(Point(rl['centreline'][-1]))}",
      rl["tracks"] == 4 and rl["corridor"] == 18 and P.contains(Point(rl["centreline"][-1])))
ug = REC["rd-ug65yhy2"][1]
claim("2.ug", "d15 Ilupeju Road rd-ug65yhy2 main road 8.5 m ends 3.2 m off at (13018.3,5448.3)",
      f"{ug['kind']} {ug['width']}, end {r0(ug['centreline'][0])} {P.exterior.distance(Point(ug['centreline'][0])):.1f} m",
      ug["width"] == 8.5 and abs(P.exterior.distance(Point(ug["centreline"][0])) - 3.2) < .1)
for rid, pt in (("rd-f0cw4h6z", (13140.0, 5360.0)), ("rd-xjd6yh6c", (13090.5, 5360.3))):
    r = REC[rid][1]
    hit = [c for c in (r["centreline"][0], r["centreline"][-1]) if near(c, pt, .1)]
    claim(f"2.{rid[3:7]}", f"d15 lane ends at {pt}", f"{r['kind']} end {r0(hit[0]) if hit else 'none'}", bool(hit))
km = REC["rd-kxa8hz1b"][1]
ke = km["centreline"][-1]
claim("2.amr", "d15 Agege Motor Road rd-kxa8hz1b trunk 21.5 m stops at (12943.5,5458.7), 70 m short of d29",
      f"{km['kind']} {km['width']}, end {r0(ke)}, {P.distance(Point(ke)):.1f} m from the d29 outline",
      km["width"] == 21.5 and near(ke, (12943.5, 5458.7), .1) and abs(P.distance(Point(ke)) - 70) < 5)

# ================================================================ section 3: roads
fr = collections.Counter()
for r in F["roads"]:
    L = LineString(r["p"]).intersection(P).length
    if L:
        fr[(r["n"], r["k"])] += L
fv = {k: round(v) for k, v in fr.items()}
claim("3.f1", "frame rail 2,308 (SGR 1,415 + unnamed 893)", f"SGR {fv.get(('Lagos–Ibadan SGR','rail'))}, unnamed {fv.get(('','rail'))}",
      fv.get(("Lagos–Ibadan SGR", "rail")) == 1415 and fv.get(("", "rail")) == 893)
claim("3.f2", "expressway 2,178 (motorway 1,078, secondary 1,100)",
      f"motorway {fv.get(('Apapa-Oworonshoki Expressway','motorway'))}, secondary {fv.get(('Apapa-Oworonshoki Expressway','secondary'))}, "
      f"+ bridge {fv.get(('Apapa-Oworonshoki Expressway','bridge'))} and misspelt 'Oworonsoki' {fv.get(('Apapa-Oworonsoki Expressway','motorway'),0)+fv.get(('Apapa-Oworonsoki Expressway','bridge'),0)} not counted",
      fv.get(("Apapa-Oworonshoki Expressway", "motorway")) == 1078)
claim("3.f3", "Town Planning Way 669; Ikorodu Road 946 (primary 584, motorway 362); Agege Motor Road 423; Coker Road 369; unnamed motorway 263, secondary 261",
      f"{fv.get(('Town Planning Way','secondary'))}; {fv.get(('Ikorodu Road','primary'))}+{fv.get(('Ikorodu Road','motorway'))}; {fv.get(('Agege Motor Road','trunk'))}; {fv.get(('Coker Road','secondary'))}; {fv.get(('','motorway'))}, {fv.get(('','secondary'))}",
      [fv.get(k) for k in [("Town Planning Way", "secondary"), ("Ikorodu Road", "primary"), ("Ikorodu Road", "motorway"),
                           ("Agege Motor Road", "trunk"), ("Coker Road", "secondary"), ("", "motorway"), ("", "secondary")]]
      == [669, 584, 362, 423, 369, 263, 261])
claim("3.f4", "7.5 km in all", f"{sum(fr.values())/1000:.2f} km", round(sum(fr.values()) / 1000, 1) == 7.5)
road = [r for r in segs if r["subtype"] == "road" and r["_g"].intersects(P)]
tl = sum(r["_g"].intersection(P).length for r in road)
ul = sum(r["_g"].intersection(P).length for r in road if not r["_n"])
claim("3.o1", "Overture 24.3 km of road inside, 15.1 km unnamed", f"{tl/1000:.1f} km, unnamed {ul/1000:.1f} km",
      round(tl / 1000, 1) == 24.3 and round(ul / 1000, 1) == 15.1)


def segset(name, cls=None):
    return [r for r in segs if r["_n"] == name and (cls is None or r["class"] == cls) and r["_g"].intersects(P)]


def clipbounds(rs):
    g = shapely.unary_union([r["_g"].intersection(P) for r in rs])
    return tuple(round(v) for v in g.bounds), g.length


def oneway(rs):
    return sum(1 for r in rs if any(a["access_type"] == "denied" and (a.get("when") or {}).get("heading") == "backward"
                                     for a in (r["access_restrictions"] or [])))


def refs(rs):
    return sorted(set(x["ref"] for r in rs for x in (r["routes"] or []) if x.get("ref")))


amr = segset("Agege Motor Road")
claim("3.amr", "Agege Motor Road trunk, ref A5, one-way pieces, paved (lanes 2: OSM only)",
      f"classes {set(r['class'] for r in amr)}, refs {refs(amr)}, one-way {oneway(amr)}/{len(amr)}, surfaces {collections.Counter(x['value'] for r in amr for x in (r['road_surface'] or []))}",
      refs(amr) == ["A5"] and oneway(amr) == len(amr))
# outline follows Agege Motor Road within a few m from y 4400 to 5400
amr_all = shapely.unary_union([r["_g"] for r in segs if r["_n"] == "Agege Motor Road"])
west = [c for c in P.exterior.coords if c[0] < 13100]
dev = []
for y in range(4400, 5401, 50):
    hline = LineString([(12500, y), (13100, y)])
    a = amr_all.intersection(hline)
    o = P.exterior.intersection(hline)
    if a.is_empty or o.is_empty:
        continue
    ax = min(g.x for g in getattr(a, "geoms", [a]))
    ox = min(g.x for g in getattr(o, "geoms", [o]))
    dev.append((y, round(ox - ax)))
ds = []
for i in range(0, int(P.exterior.length), 10):
    p_ = P.exterior.interpolate(i)
    if 4400 <= p_.y <= 5400 and p_.x < 13000:
        ds.append(p_.distance(amr_all))
ds.sort()
claim("3.amr2", "outline follows Agege Motor Road to within a few metres from y 4400 to 5400",
      f"outline points every 10 m on the west side (y 4400-5400) to the nearest carriageway line: n {len(ds)}, median {ds[len(ds)//2]:.0f} m, "
      f"{sum(d <= 5 for d in ds)/len(ds):.0%} within 5 m, {sum(d <= 10 for d in ds)/len(ds):.0%} within 10 m, max {ds[-1]:.0f} m", None)
rails = [r for r in segs if r["subtype"] == "rail" and r["_g"].intersects(P)]
claim("3.rail1", "Overture calls all three rail pieces standard gauge", f"{[(r['_n'], r['class']) for r in rails]}",
      len(rails) == 3 and all(r["class"] == "standard_gauge" for r in rails))
rail_all = shapely.unary_union([r["_g"] for r in rails])
offs = []
for y in range(4400, 5451, 50):
    hline = LineString([(12500, y), (13100, y)])
    a = amr_all.intersection(hline)
    rr = rail_all.intersection(hline)
    if a.is_empty or rr.is_empty:
        continue
    ax = max(g.x for g in getattr(a, "geoms", [a]))
    rx = min(g.x for g in getattr(rr, "geoms", [rr]))
    offs.append((y, round(rx - ax)))
claim("3.rail2", "rail inside d29 along the whole west edge, 5-30 game m east of Agege Motor Road",
      f"rail's west line x minus the road's east carriageway x, every 50 m: {offs}; rail inside y {rail_all.intersection(P).bounds[1]:.0f}-{rail_all.intersection(P).bounds[3]:.0f}",
      None)
exm = segset("Apapa-Oworonshoki Expressway", "motorway") + segset("Apapa-Oworonsoki Expressway", "motorway")
bx, _ = clipbounds(exm)
claim("3.exp1", "expressway motorway, ref F265, one-way, bridge pieces; carriageways inside bbox x 12803-13347, y 4791-4888",
      f"refs {refs(exm)}, one-way {oneway(exm)}/{len(exm)}, bridge pieces {sum(1 for r in exm if any('is_bridge' in x['values'] for x in (r['road_flags'] or [])))}; clipped bbox x {bx[0]}-{bx[2]}, y {bx[1]}-{bx[3]}",
      near(bx, (12803, 4791, 13347, 4888), 1))
exs = segset("Apapa-Oworonshoki Expressway", "secondary")
bs, _ = clipbounds(exs)
claim("3.exp2", "service roads of the same name span y 4734-4908", f"y {bs[1]}-{bs[3]}", (bs[1], bs[3]) == (4734, 4908))
bl = [l for l in open(os.path.join(ROOT, "docs/lagos-study/roads/borders.csv")) if l.startswith('"Shogunle, east of Agege Motor Road",Ilupeju')]
claim("3.exp3", "borders.csv: Shogunle east | Ilupeju, big road 1.85 km", bl[0].strip() if bl else "none", bool(bl) and "big road 1.85 km" in bl[0])
d28s = [l for l in d28t.splitlines() if l.startswith("| rd-cbaebc6a")]
claim("3.exp4", "Gbàgede drew the expressway 25 m", d28s[0] if d28s else "?", bool(d28s) and "| 25.0 |" in d28s[0])
tpw = segset("Town Planning Way")
b2, _ = clipbounds(tpw)
claim("3.tpw", "Town Planning Way secondary, two-way and one-way pieces, x 12821-13339, y 4840-4911",
      f"classes {set(r['class'] for r in tpw)}, one-way {oneway(tpw)}/{len(tpw)}, x {b2[0]}-{b2[2]}, y {b2[1]}-{b2[3]}",
      b2 == (12821, 4840, 13339, 4911) and 0 < oneway(tpw) < len(tpw))
byp = segset("Ilupeju Bye Pass")
b3, L3 = clipbounds(byp)
ends_b = [tuple(round(v) for v in c) for r in byp for c in (r["_g"].coords[0], r["_g"].coords[-1])]
claim("3.byp", "Bye Pass unclassified, one-way pieces; (13171,5228) to (12963,5313), 447 m inside",
      f"classes {set(r['class'] for r in byp)}, one-way {oneway(byp)}/{len(byp)}, clipped bbox {b3}, {L3:.0f} m inside "
      f"(both carriageways), {sum(r['_g'].length for r in byp):.0f} m unclipped; (13171,5228) an end {(13171, 5228) in ends_b}, (12963,5313) an end {(12963, 5313) in ends_b}",
      round(L3) == 447)
xing = shapely.unary_union([r["_g"] for r in byp]).intersection(rail_all)
claim("3.byp2", "the bypass crosses the rail at about (12971,5312)", f"crossings {[r0((g.x, g.y)) for g in getattr(xing, 'geoms', [xing])]}",
      any(near((g.x, g.y), (12971, 5312), 10) for g in getattr(xing, "geoms", [xing])))
b4, _ = clipbounds(coker)
claim("3.coker", "Coker Road secondary, mostly one-way pieces, paved; (13178,4845) to (13168,5230)",
      f"{set(r['class'] for r in coker)}, one-way {oneway(coker)}/{len(coker)} pieces, paved {sum(1 for r in coker if any(x['value']=='paved' for x in (r['road_surface'] or [])))}/{len(coker)}, bbox {b4}",
      False if oneway(coker) <= len(coker) / 2 else True)
m15 = REC["rd-9wkc2te6"][1]
dd = LineString(m15["centreline"]).distance(P)
dc = LineString(m15["centreline"]).distance(shapely.unary_union([LineString(r["p"]) for r in fc]))
claim("3.coker2", "Mùṣá's separate Coker Road (8.0 m) is further south, 312 m off", f"rd-9wkc2te6 {m15['width']} m, {dd:.0f} m from d29's outline ({dc:.0f} m from d29's Coker Road itself)",
      m15["width"] == 8.0 and abs(dd - 312) < 5)
ia = segset("Ilupeju Industrual Avenue")
b5, _ = clipbounds(ia)
ic = segset("Industrial Cresent")
b6, _ = clipbounds(ic)
claim("3.ind", "Industrial Avenue ('Industrual', residential, paved) x 12868-13051, y 4903-5278; Crescent 12994-13058, 4858-4997",
      f"Avenue {set(r['class'] for r in ia)} {b5}; Crescent {b6}", b5 == (12868, 4903, 13051, 5278) and b6 == (12994, 4858, 13058, 4997))
ikr = segset("Ikorodu Road")
claim("3.ikr", "Ikorodu Road motorway with tunnel pieces and primary service roads; ref A1 (OSM)",
      f"classes {collections.Counter(r['class'] for r in ikr)}, tunnel pieces {sum(1 for r in ikr if any('is_tunnel' in x['values'] for x in (r['road_flags'] or [])))}, refs in Overture {refs(ikr)} (A1 not in Overture: not checked)",
      None)
afw = segset("Adekunle Fajuyi Way")
_, L7 = clipbounds(afw)
ends_a = [tuple(round(v) for v in c) for r in afw for c in (r["_g"].coords[0], r["_g"].coords[-1])]
claim("3.afw", "Adekunle Fajuyi Way tertiary, (12568,4296) to (13150,4230), 346 m inside",
      f"{set(r['class'] for r in afw)}, ends {sorted(set(ends_a))}, {L7:.0f} m inside", abs(L7 - 346) < 2)
tr = segset("Trailhead Pl.") + segset("Trailhead Rd")
b8, _ = clipbounds(tr)
claim("3.trail", "'Trailhead Pl.' and 'Trailhead Rd' in the cantonment, 13194-13308, 4619-4683", f"{b8}, inside cantonment polygon {cg.contains(shapely.unary_union([r['_g'] for r in tr]).centroid)}",
      b8 == (13194, 4619, 13308, 4683))
inner = ["Johnson Street", "Olutanda Street", "Ashimowu Jibowu Street", "Ashimowa Close", "Ilaka Street", "Adepebga Street",
         "Oyetola Idowu Street", "Olusoji Idowu Street", "Oduwobi Street", "Adeyinka Street", "Esther Oshiyemi Street",
         "Folayemi Street", "Aina Eleko Street", "Iya Oloye Crescent", "Micheal Adekoya Street", "Akinsete Drive", "Bello Crescent"]
found = {n: len(segset(n)) for n in inner}
claim("3.inner", "the listed inner streets exist inside (Overture spellings)", f"{found}; 'Olutunda' spelling {len(segset('Olutunda Street'))}",
      all(found.values()))
claim("3.mad", "Michael Adekoya one-way", f"one-way {oneway(segset('Micheal Adekoya Street'))}/{len(segset('Micheal Adekoya Street'))}",
      oneway(segset("Micheal Adekoya Street")) == len(segset("Micheal Adekoya Street")))
sc = collections.Counter()
for n in inner:
    for r in segset(n):
        for x in (r["road_surface"] or []):
            sc[x["value"]] += 1
        if not r["road_surface"]:
            sc["no tag"] += 1
claim("3.unpaved", "most inner streets are tagged unpaved", f"Overture pieces of the listed streets: {dict(sc)}",
      sc["unpaved"] > sc["paved"])

# ================================================================ section 4: table (lat/lon -> game, and the Overture points)
rows = [("cantonment centre", 6.5665, 3.3567, (12971, 4496)), ("mosque in cantonment", 6.5669, 3.3572, (12987, 4478)),
        ("tennis court", 6.5665, 3.3632, (13208, 4493)), ("Arena", 6.5640, 3.3504, (12736, 4588)),
        ("Oshodi station", 6.5573, 3.3514, (12775, 4835)), ("Terminal 3", 6.5566, 3.3527, (12823, 4860)),
        ("building site", 6.5579, 3.3519, (12795, 4812)), ("LASTMA office", 6.5582, 3.3568, (12972, 4799)),
        ("Drivers Institute", 6.5593, 3.3556, (12929, 4761)), ("market", 6.5576, 3.3607, (13116, 4823)),
        ("LCDA", 6.5567, 3.3603, (13104, 4856)), ("police", 6.5529, 3.3602, (13097, 4997)),
        ("ind north", 6.5602, 3.3592, (13061, 4727)), ("ind south", 6.5500, 3.3566, (12967, 5102)),
        ("GSK clinic", 6.5547, 3.3544, (12886, 4930)), ("D2 clinic", 6.5561, 3.3562, (12950, 4877)),
        ("Shodex", 6.5589, 3.3665, (13332, 4775)), ("Funtasticaland", 6.5534, 3.3661, (13315, 4975)),
        ("Andela", 6.5537, 3.3662, (13318, 4965)), ("Kiss FM", 6.5526, 3.3666, (13336, 5008)),
        ("Elizade", 6.5574, 3.3665, (13330, 4829)), ("LSDPC", 6.5567, 3.3649, (13273, 4854)),
        ("Bazaar", 6.5545, 3.3656, (13296, 4937)), ("SPAR", 6.5564, 3.3596, (13078, 4868)),
        ("AAA", 6.5553, 3.3633, (13212, 4909)), ("Gurudwara", 6.5530, 3.3621, (13170, 4991)),
        ("City of Praise", 6.5572, 3.3623, (13176, 4839)), ("Celestial", 6.5505, 3.3603, (13108, 5085)),
        ("Rock's Place", 6.5492, 3.3618, (13158, 5132)), ("Covenant", 6.5462, 3.3587, (13045, 5242)),
        ("St Paul's", 6.5461, 3.3618, (13160, 5245)), ("Our Lady", 6.5440, 3.3594, (13068, 5324)),
        ("Fountain", 6.5535, 3.3552, (12914, 4974)), ("Tawakaltu", 6.5435, 3.3602, (13100, 5342)),
        ("NASFAT", 6.5558, 3.3611, (13131, 4888)), ("Treasure House", 6.5500, 3.3615, (13148, 5103)),
        ("Grammar", 6.5554, 3.3538, (12863, 4902)), ("Anthony BRT", 6.5571, 3.3667, (13340, 4842)),
        ("fuel 1", 6.5589, 3.3641, (13242, 4776)), ("fuel 2", 6.5524, 3.3569, (12977, 5014)),
        ("basketball", 6.5462, 3.3580, (13019, 5244))]
bad = []
for nmx, la, lo, want in rows:
    g = gidi(lo, la)
    if not near(g, want, 6):
        bad.append((nmx, want, r0(g)))
claim("4.conv", f"{len(rows)} lat/lon -> game conversions in the table (tolerance 6 m, the 4-decimal rounding)",
      f"off: {bad}" if bad else "all agree", not bad)

ovchk = [("Shodex Garden", (13332, 4775), None), ("Funtasticaland", (13315, 4975), .93), ("Andela Epic Tower", (13318, 4965), None),
         ("98.9 Kiss Fm", (13336, 5008), None), ("Elizade", (13330, 4829), None), ("Lagos State Development and Property", (13273, 4854), None),
         ("The Bazaar", (13296, 4937), None), ("Shop Perfect", (13296, 4955), None), ("Taj Restaurant", (13296, 4974), None),
         ("SPAR Nigeria", (13078, 4868), None), ("AAA Indian", (13212, 4909), None), ("Pondicheri", (13102, 5030), None),
         ("Zaika", (13175, 5035), None), ("Gurudwara Nanak Darbar", (13170, 4991), .38),
         ("The Redeemed Christian Church of God City Of Praise", (13176, 4839), .91),
         ("Celestial Church of Christ Ilupeju Estate Parish 1", (13108, 5085), .96), ("RCCG,The Rock's Place", (13158, 5132), .90),
         ("RCCG Covenant Center", (13045, 5242), .97), ("St. Paul's African Church", (13160, 5245), .71),
         ("Our Lady Queen of Apostles", (13068, 5324), .88), ("The Fountain Of Life Church", (12914, 4974), .77),
         ("Tawakaltu Mosque", (13100, 5342), .54), ("NASFAT Secretariat", (13131, 4888), .25), ("Nasfat Agency for Zakat", None, .66),
         ("Treasure House School Lagos", (13148, 5103), .95), ("Ilupeju Senior Grammar School", (12863, 4902), .47),
         ("Ilupeju Police Station", (13097, 4997), None), ("Lagos State Drivers Institute", (12929, 4761), None),
         ("Lagos State Traffic Management Authority", (12972, 4799), None), ("Ilupeju Model Market", (13116, 4823), None)]
for key, pos, conf in ovchk:
    hits = [r for r in pin if r["_n"].startswith(key)]
    if not hits:
        claim("4.ov", f"{key} at {pos}", "not found inside", False)
        continue
    best = min(hits, key=lambda r: Point(pos).distance(r["_g"]) if pos else 0)
    gp = (best["_g"].x, best["_g"].y)
    dpos = Point(pos).distance(best["_g"]) if pos else 0
    ok = dpos <= 3 and (conf is None or abs(best["confidence"] - conf) < .006)
    claim("4.ov", f"{key} at {pos} conf {conf}",
          f"{best['_n']} at {r0(gp)} ({dpos:.0f} m), conf {best['confidence']:.2f}" + (f"; other hits {[ (h['_n'], r0((h['_g'].x,h['_g'].y))) for h in hits if h is not best]}" if len(hits) > 1 else ""),
          ok)
gas = [r for r in pin if r["basic_category"] == "gas_station" or r["_n"] == "TotalEnergies"]
claim("4.fuel", "fuel stations at 13242,4776 and 12977,5014 [OSM][OV]",
      f"Overture TotalEnergies points: {[(r['basic_category'], r0((r['_g'].x, r['_g'].y))) for r in gas]}", None)
amr_d = Point(12977, 5014).distance(amr_all)
nr = sorted((r["_g"].distance(Point(12977, 5014)), r["_n"]) for r in segs if r["_n"])[0]
sv = sorted((r["_g"].distance(Point(13240, 4776)), r["_n"], r["class"]) for r in segs if r["_n"])[0]
claim("4.fuel2", "the fuel station at 12977,5014 is 'by Agege Motor Road'; the other on the expressway's service road",
      f"{amr_d:.0f} m from Agege Motor Road; nearest named road {nr[1]} {nr[0]:.0f} m; 13240,4776: nearest {sv[1]} ({sv[2]}) {sv[0]:.0f} m", amr_d < 40)
st_ = [r for r in infra if r["_n"] == "Oshodi" and r["class"] == "railway_station"]
plat = [r for r in infra if r["class"] == "platform" and dict(r["source_tags"] or {}).get("railway") == "platform" and r["_g"].intersects(P)]
pb = shapely.unary_union([r["_g"] for r in plat]).bounds
claim("4.stn", "station 12775,4835; two platform ways 12758-12790, 4801-4870, on the seam with d30/d32",
      f"station {r0((st_[0]['_g'].x, st_[0]['_g'].y))}; {len(plat)} platforms, bbox {tuple(round(v) for v in pb)}; "
      f"platform shares {[{k: round(p['_g'].intersection(v).area/p['_g'].area, 2) for k, v in DIST.items() if p['_g'].intersects(v) and p['_g'].intersection(v).area > 0} for p in plat]}",
      len(plat) == 2 and near(pb, (12758, 4801, 12790, 4870), 2))
t3 = [r for r in infra if r["_n"].startswith("Oshodi Transport Interchange - Terminal 3")]
t3t = dict(t3[0]["source_tags"]) if t3 else {}
claim("4.t3", "Terminal 3 at 12823,4860, 5 levels, 'Buses to Lagos East'",
      f"centroid {r0((t3[0]['_g'].centroid.x, t3[0]['_g'].centroid.y))}, levels {t3t.get('building:levels')}, '{t3t.get('description')}'",
      bool(t3) and t3t.get("building:levels") == "5" and t3t.get("description") == "Buses to Lagos East")
t12 = [r for r in infra if re.search(r"Terminal [12]\b", r["_n"])]
claim("4.t12", "Terminals 1 and 2 outside, west (12768,4922; 12754,4888)",
      f"{[(r['_n'], r0((r['_g'].centroid.x, r['_g'].centroid.y)), 'inside' if P.contains(r['_g'].centroid) else 'outside') for r in t12]}", None)
cons = [r for r in landuse if r["class"] == "construction" and r["_g"].intersects(P)]
claim("4.cons", "building site (landuse construction) at 12795,4812", f"{[r0((r['_g'].centroid.x, r['_g'].centroid.y)) for r in cons]}",
      any(near((r["_g"].centroid.x, r["_g"].centroid.y), (12795, 4812), 5) for r in cons))
mk = [r for r in landuse if r["_n"] == "Market" and r["_g"].intersects(P)]
claim("4.mkt", "OSM 'Market' 752 m2 at 13116,4823", f"{[(round(r['_g'].area), r0((r['_g'].centroid.x, r['_g'].centroid.y))) for r in mk]}",
      any(round(r["_g"].area) == 752 for r in mk))
for nmx, area, cen, bbx, poly in (("ind north", 50077, (13061, 4727), (12789, 4622, 13333, 4832), None),
                                  ("ind south", 80332, (12967, 5102), (12815, 4809, 13119, 5395), None),
                                  ("cantonment", None, (12971, 4496), (12622, 4224, 13320, 4768), cg),
                                  ("Arena", 15489, (12736, 4588), (12659, 4496, 12814, 4681), ag)):
    if poly is None:
        poly = [r["_g"] for r in ind if round(r["_g"].area) == area][0]
    bb_ = poly.bounds
    bc = ((bb_[0] + bb_[2]) / 2, (bb_[1] + bb_[3]) / 2)
    claim("4.poly", f"{nmx}: centre {cen}, bbox {bbx}", f"bbox {tuple(round(v) for v in bb_)}, bbox centre {r0(bc)}, centroid {r0((poly.centroid.x, poly.centroid.y))}",
          near(bb_, bbx, 2) and (near(bc, cen, 6) or near((poly.centroid.x, poly.centroid.y), cen, 6)))
bk = [r for r in landuse if dict(r["source_tags"] or {}).get("sport") == "basketball" and r["_g"].intersects(P)]
claim("4.bball", "basketball court 13019,5244 [OSM][OV]", f"OSM pitch {[r0((r['_g'].centroid.x, r['_g'].centroid.y)) for r in bk]}",
      any(near((r["_g"].centroid.x, r["_g"].centroid.y), (13019, 5244), 3) for r in bk))
brt = [r for r in infra if r["_n"] == "Anthony Bus Stop"]
claim("4.brt", "Anthony BRT stop 13340,4842", f"{[(r0((r['_g'].x, r['_g'].y)), dict(r['source_tags']).get('bus_stop:category'), 'inside' if P.contains(r['_g']) else 'outside') for r in brt]}",
      any(near((b_["_g"].x, b_["_g"].y), (13340, 4842), 2) for b_ in brt))
note = open(os.path.join(ROOT, "docs/lagos-study/districts/d29.md")).read().splitlines()
hdr = [i for i, l in enumerate(note) if l.startswith("| Real place |")][0]
nrows = 0
for l in note[hdr + 2:]:
    if not l.startswith("|"):
        break
    nrows += 1
claim("4.count", "Counted: 38 table rows", f"{nrows} rows under the header", nrows == 38)

# ================================================================ section 5
pl206 = [l for l in open(os.path.join(ROOT, "docs/lagos-study/roads/places.csv")) if l.startswith("206,")]
claim("5.fab1", "Shogunle east 2.8 km2, 1,356/km2, median 74, height 7.9, grid 0.742, 14.9 km/km2", pl[0].split(",")[3:16] if pl else "?",
      bool(pl) and all(x in pl[0] for x in (",2.8,", ",1356,", ",74.0,", ",7.89,", ",0.742,", ",14.9,")))
claim("5.fab2", "Ilupeju 1.82 km2, 2,057/km2, median 82, 38% big, 8.45 m, grid 0.608, 19.3 km/km2", pl206[0].split(",")[2:16] if pl206 else "?",
      bool(pl206) and all(x in pl206[0] for x in (",1.82,", ",2057,", ",82.0,", ",0.38,", ",8.45,", ",0.608,", ",19.3,")))
l29 = re.search(r"^\| 29 \| Ilupeju.*$", liv, re.M).group(0)
claim("5.liv", "LIVING: 141,489 people, 30,625/km2, 6,878 buildings, mean 208 m2, 33.1% big roofs, 31 : 1, band C", l29,
      all(x in l29 for x in ("141,489", "30,625", "6,878", "| 208 |", "33.1", "31 : 1")) and "Ilupeju (29)" in liv)
claim("5.liv2", "'a third of the roof area is factories'; warehouses; tankers/lorries/staff buses; 'Gap: no proper source'",
      re.search(r"#### 29\.[\s\S]*?\*\*Gap:\*\*[^\n]*", liv).group(0).replace("\n", " ")[:600], None)
okl = liv.splitlines()[96]
claim("5.okada", "okada banned in Mushin from 1 Sept 2022, patchy [LIV line 97]", okl[:200], "1 Sept 2022" in okl and "Mushin" in okl)
study = open(os.path.join(ROOT, "docs/lagos-study/STUDY.md")).read()
claim("5.st", "[ST] cantonment 1.9 km2; Ilupeju-Isolo-Mushin industry belt 9.3 km2",
      f"{'Ikeja Cantonment**: 1.9 km²' in study}, {'Ilupeju-Isolo-Mushin (9.3)' in study}",
      "Ikeja Cantonment**: 1.9 km²" in study and "Ilupeju-Isolo-Mushin (9.3)" in study)
claim("5.lga", "LGA 1103: Aug 2021 more than 20 cars and shops smashed across Ilupeju and Shomolu (cult wars)", lga[1102].strip(),
      "more than 20 cars" in lga[1102] and "Confraternity" in "\n".join(lga[1096:1100]) or "confraternity" in "\n".join(lga[1096:1100]))
bc = collections.Counter(r["basic_category"] for r in pin)
claim("5.ov", "435 places; 14 Christian places of worship, 22 religious organisations, 1 mosque, 19 event services, 5 hotels",
      f"{len(pin)} places; christian {bc['christian_place_of_worship']}, religious_org {bc['religious_organization']}, mosque {bc['muslim_place_of_worship']}, event {bc['event_or_party_service']}, hotel {bc['hotel']}",
      len(pin) == 435 and bc["christian_place_of_worship"] == 14 and bc["religious_organization"] == 22 and
      bc["muslim_place_of_worship"] == 1 and bc["event_or_party_service"] == 19 and bc["hotel"] == 5)
wat = [w for w in F["water"] if Polygon(w[0], w[1:]).intersects(P)]
wl = [r for r in landuse if r["subtype"] in ("water",) and r["_g"].intersects(P)]
claim("5.water", "no water inside", f"frame water polygons touching the outline: {len(wat)}; Overture water land use: {len(wl)} (OSM's own read not repeated)",
      not wat and not wl)

# ================================================================ section 6
claim("6.st", "[ST]: Mùṣá and Ṣọmọlá are the dense core (and Ilupeju, by contrast, is not)",
      "STUDY.md lines 136 and 213 put Ilupeju itself in the central dense core list, with the Ilupeju-Isolo industry belt on its north edge",
      None)

print("\n".join(ROWS))
print(f"\n{dict(TALLY)}  (SEE = the printed numbers are the verdict; read them)")
