/* The Gidi drawing board (owner, 16 Oct 2026): a clean plan of the city to scale, where every road edge, plot, house and
   piece of street furniture can be seen exactly, checked, moved and placed. Edits are saved as hand-file edits through
   scripts/board_server.py, so the bake, the checks and the 3D follow the drawing. Data: window.GIDI (metres, y south). */
(() => {
  "use strict";
  const G = window.GIDI;
  const $ = (id) => document.getElementById(id);
  const cv = $("cv"), ctx = cv.getContext("2d");
  const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

  // ------------------------------------------------------------------ geometry
  const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
  function segDist(p, a, b) {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = dx * dx + dy * dy;
    let t = L ? ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L : 0; t = Math.max(0, Math.min(1, t));
    return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy);
  }
  function nearestOnSeg(p, a, b) {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = dx * dx + dy * dy;
    let t = L ? ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L : 0; t = Math.max(0, Math.min(1, t));
    return [a[0] + t * dx, a[1] + t * dy];
  }
  function lineDist(p, pts) { let m = 1e9; for (let i = 0; i < pts.length - 1; i++) m = Math.min(m, segDist(p, pts[i], pts[i + 1])); return m; }
  function inPoly(p, poly) {
    let c = false;
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const a = poly[i], b = poly[j];
      if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]) c = !c;
    }
    return c;
  }
  const centroid = (pts) => [pts.reduce((s, q) => s + q[0], 0) / pts.length, pts.reduce((s, q) => s + q[1], 0) / pts.length];
  function cross(o, a, b) { return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]); }
  function segsCross(a, b, c, d) {   // a proper crossing, not a touch
    const d1 = cross(c, d, a), d2 = cross(c, d, b), d3 = cross(a, b, c), d4 = cross(a, b, d), e = 1e-3;
    return ((d1 > e && d2 < -e) || (d1 < -e && d2 > e)) && ((d3 > e && d4 < -e) || (d3 < -e && d4 > e));
  }
  function edgeDist(p, poly) { let m = 1e9; for (let i = 0; i < poly.length; i++) m = Math.min(m, segDist(p, poly[i], poly[(i + 1) % poly.length])); return m; }
  function polysOverlap(A, B) {   // more than a touch: an edge crosses, or a corner sits well inside the other
    for (let i = 0; i < A.length; i++) for (let j = 0; j < B.length; j++) if (segsCross(A[i], A[(i + 1) % A.length], B[j], B[(j + 1) % B.length])) return true;
    for (const p of A) if (inPoly(p, B) && edgeDist(p, B) > 0.15) return true;
    for (const p of B) if (inPoly(p, A) && edgeDist(p, A) > 0.15) return true;
    return false;
  }
  function polyLineDist(poly, a, b) {   // a building to a road segment: 0 if the road runs into it
    if (inPoly(a, poly) || inPoly(b, poly)) return 0;
    let m = 1e9;
    for (let i = 0; i < poly.length; i++) {
      const p = poly[i], q = poly[(i + 1) % poly.length];
      if (segsCross(p, q, a, b)) return 0;
      m = Math.min(m, segDist(p, a, b), segDist(q, a, b), segDist(a, p, q), segDist(b, p, q));
    }
    return m;
  }
  function cutLine(pts, at, gap) {   // a line with an opening of gap metres round the point nearest at (as scripts/hand.py cuts)
    let t = 0, best = 1e9, acc = 0;
    for (let i = 0; i < pts.length - 1; i++) { const q = nearestOnSeg(at, pts[i], pts[i + 1]), d = dist(at, q); if (d < best) { best = d; t = acc + dist(pts[i], q); } acc += dist(pts[i], pts[i + 1]); }
    const sub = (a, b) => { const out = []; let s0 = 0; for (let i = 0; i < pts.length - 1; i++) { const L = dist(pts[i], pts[i + 1]), s1 = s0 + L; const lo = Math.max(a, s0), hi = Math.min(b, s1); if (hi > lo) { const f = (x) => [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * (x - s0) / L, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * (x - s0) / L]; if (!out.length) out.push(f(lo)); out.push(f(hi)); } s0 = s1; } return out; };
    return [sub(0, t - gap / 2), sub(t + gap / 2, acc)].filter((p) => p.length > 1 && p.reduce((a, q, i) => i ? a + dist(p[i - 1], q) : 0, 0) >= 0.5);
  }
  const bboxOf = (pts) => { let b = [1e9, 1e9, -1e9, -1e9]; for (const [x, y] of pts) { b[0] = Math.min(b[0], x); b[1] = Math.min(b[1], y); b[2] = Math.max(b[2], x); b[3] = Math.max(b[3], y); } return b; };
  const r1 = (v) => Math.round(v * 10) / 10;

  // ------------------------------------------------------------------ the model (a copy of the map, with board edits applied on top)
  const XS = G.cross_sections || {};
  const WID = (cls) => { const x = XS[cls]; if (cls === "path") return { c: 2.0, g: 0, w: 0 }; if (!x) return { c: 7, g: 0.8, w: 1.5 }; return { c: x.carriageway, g: x.gutter, w: x.walkway }; };
  const DIST = G.districts.map((d) => ({ id: d.id, name: d.name, poly: d.poly[0], bb: bboxOf(d.poly[0]) }));
  const districtAt = (p) => (DIST.find((d) => p[0] >= d.bb[0] && p[0] <= d.bb[2] && p[1] >= d.bb[1] && p[1] <= d.bb[3] && inPoly(p, d.poly)) || {}).id;
  let M;   // the model
  const CELL = 50;
  function grid() { return new Map(); }
  function gkey(x, y) { return Math.floor(x / CELL) + "," + Math.floor(y / CELL); }
  function gadd(g, item, bb) { for (let x = Math.floor(bb[0] / CELL); x <= Math.floor(bb[2] / CELL); x++) for (let y = Math.floor(bb[1] / CELL); y <= Math.floor(bb[3] / CELL); y++) { const k = x + "," + y; let c = g.get(k); if (!c) g.set(k, (c = new Set())); c.add(item); } }
  function gdel(g, item, bb) { for (let x = Math.floor(bb[0] / CELL); x <= Math.floor(bb[2] / CELL); x++) for (let y = Math.floor(bb[1] / CELL); y <= Math.floor(bb[3] / CELL); y++) { const c = g.get(x + "," + y); if (c) c.delete(item); } }
  function gquery(g, bb) { const out = new Set(); for (let x = Math.floor(bb[0] / CELL); x <= Math.floor(bb[2] / CELL); x++) for (let y = Math.floor(bb[1] / CELL); y <= Math.floor(bb[3] / CELL); y++) { const c = g.get(x + "," + y); if (c) for (const it of c) out.add(it); } return out; }

  function build() {
    M = { B: [], F: [], MON: [], P: [], R: [], PAR: [], WALL: [], ZONE: [], DECK: [], GUT: [], gB: grid(), gF: grid(), gR: grid(), gZ: grid(), gW: grid(), CW: [], GATE: [], version: 0 };
    for (const [d, L] of Object.entries(G.buildings)) {
      const st = (G.storeys || {})[d] || [];
      L.forEach((b, i) => { const o = { t: "b", d, kind: b[0], pts: b.slice(1).map((q) => [q[0], q[1]]), st: st[i] || 1 }; addB(o); });
    }
    (G.furniture || []).forEach((f) => addF({ t: "f", d: f.d, kind: f.kind, x: f.x, y: f.y, ang: f.ang || 0, name: f.name || "" }));
    (G.monuments || []).forEach((m) => M.MON.push({ t: "m", d: m.d, kind: m.model, x: m.x, y: m.y, ang: m.ang || 0, name: m.name || "" }));
    (G.pois || []).forEach((p) => M.P.push({ t: "p", d: p.d, kind: p.type, x: p.x, y: p.y, name: p.name, note: p.note || "" }));
    const S = G.surfaces || {};
    for (const [src, cls] of [["streets", "street"], ["lanes", "lane"], ["paths", "path"]])
      for (const [d, L] of Object.entries(G[src] || {})) L.forEach((pts, i) => { if (pts.length > 1) addR({ t: "r", cls, d, pts: pts.map((q) => [q[0], q[1]]), surf: ((S[src] || {})[d] || [])[i] || "tar", src }); });
    G.mains.forEach((m, i) => addR({ t: "r", cls: "main", d: m.d, pts: m.pts, name: m.name, surf: (S.mains || [])[i] || "tar", src: "mains" }));
    G.arterials.forEach((a, i) => addR({ t: "r", cls: a.cls === "exp" ? "exp" : a.cls === "bridge" ? "bridge" : "art", d: null, pts: a.pts, name: a.name, surf: (S.arterials || [])[i] || "tar", src: "arterials" }));
    for (const [d, L] of Object.entries(G.parcels || {})) L.forEach((p) => M.PAR.push({ t: "plot", d, kind: p.kind, pts: p.pts, bb: bboxOf(p.pts) }));
    for (const [d, L] of Object.entries(G.walls || {})) L.forEach((w) => M.WALL.push({ d, pts: w, bb: bboxOf(w) }));
    (G.encroach || []).forEach((z) => addZ({ t: "zone", d: z.d, kind: z.kind, pts: z.pts }));
    (G.structures || []).forEach((s) => M.DECK.push({ t: "deck", d: s.d, kind: s.kind, name: s.name, pts: s.pts, w: s.width || 8, bb: bboxOf(s.pts) }));
    (G.gutters || []).forEach((g) => M.GUT.push({ pts: g.pts, w: g.w || 0.8, state: g.state, bb: bboxOf(g.pts) }));
    for (const [d, L] of Object.entries(G.compound_walls || {})) L.forEach((w) => addW({ t: "w", d, pts: w.map((q) => [q[0], q[1]]) }));
    for (const [d, L] of Object.entries(G.compound_gates || {})) L.forEach((q) => M.GATE.push({ t: "g", d, x: q[0], y: q[1] }));
    M.WATER = [...(G.water || []), ...(G.ocean || [])].map((r) => ({ pts: r, bb: bboxOf(r) }));
  }
  function addW(o) { o.bb = bboxOf(o.pts); M.CW.push(o); gadd(M.gW, o, o.bb); }
  function delW(o) { gdel(M.gW, o, o.bb); M.CW.splice(M.CW.indexOf(o), 1); }
  function addZ(o) { o.bb = bboxOf(o.pts); M.ZONE.push(o); gadd(M.gZ, o, o.bb); }
  function addB(o) { o.bb = bboxOf(o.pts); M.B.push(o); gadd(M.gB, o, o.bb); }
  function delB(o) { gdel(M.gB, o, o.bb); M.B.splice(M.B.indexOf(o), 1); }
  function moveB(o, fn) { gdel(M.gB, o, o.bb); o.pts = o.pts.map(fn); o.bb = bboxOf(o.pts); gadd(M.gB, o, o.bb); }
  function setPts(b, pts) { gdel(M.gB, b, b.bb); b.pts = pts.map((q) => [q[0], q[1]]); b.bb = bboxOf(b.pts); gadd(M.gB, b, b.bb); }
  const closeRing = (pts) => { const q = pts.map((p) => [p[0], p[1]]); const a = q[0], z = q[q.length - 1]; if (a[0] !== z[0] || a[1] !== z[1]) q.push([a[0], a[1]]); return q; };
  const openRing = (pts) => { const a = pts[0], z = pts[pts.length - 1]; return a[0] === z[0] && a[1] === z[1] ? pts.slice(0, -1) : pts.slice(); };
  function addF(o) { M.F.push(o); gadd(M.gF, o, [o.x, o.y, o.x, o.y]); }
  function delF(o) { gdel(M.gF, o, [o.x, o.y, o.x, o.y]); M.F.splice(M.F.indexOf(o), 1); }
  function moveF(o, x, y) { gdel(M.gF, o, [o.x, o.y, o.x, o.y]); o.x = x; o.y = y; gadd(M.gF, o, [x, y, x, y]); }
  function addR(o) { o.bb = bboxOf(o.pts); o.wd = WID(o.cls === "bridge" ? "bridge" : o.cls); M.R.push(o); gadd(M.gR, o, [o.bb[0] - 20, o.bb[1] - 20, o.bb[2] + 20, o.bb[3] + 20]); }
  function delR(o) { gdel(M.gR, o, [o.bb[0] - 20, o.bb[1] - 20, o.bb[2] + 20, o.bb[3] + 20]); M.R.splice(M.R.indexOf(o), 1); }

  // the same edits scripts/hand.py applies, on the board's copy (for edits made since the last bake)
  function apply(d, e) {
    const op = e.op;
    const findB = (at, kind) => [...gquery(M.gB, [at[0] - 1, at[1] - 1, at[0] + 1, at[1] + 1])].find((b) => b.d === d && (!kind || b.kind === kind) && (inPoly(at, b.pts) || edgeDist(at, b.pts) < 0.3));
    const findF = (at, kind) => { let best = null, bd = 2.0; for (const f of gquery(M.gF, [at[0] - 2, at[1] - 2, at[0] + 2, at[1] + 2])) { const dd = dist(at, [f.x, f.y]); if ((!kind || f.kind === kind) && dd < bd) { best = f; bd = dd; } } return best; };
    const findM = (at) => { let best = null, bd = 3.0; for (const m of M.MON) { const dd = dist(at, [m.x, m.y]); if (dd < bd) { best = m; bd = dd; } } return best; };
    if (op === "add building") addB({ t: "b", d, kind: e.kind, pts: e.pts.map((q) => [q[0], q[1]]), st: e.storeys || 1 });
    else if (op === "delete building") { const b = findB(e.at, e.kind); if (b) delB(b); }
    else if (op === "move building") {
      const b = findB(e.at, e.kind); if (!b) return;
      const [dx, dy] = e.by || [0, 0]; moveB(b, ([x, y]) => [x + dx, y + dy]);
      if (e.rotate) { const c = centroid(b.pts), a = e.rotate * Math.PI / 180, cs = Math.cos(a), sn = Math.sin(a); moveB(b, ([x, y]) => [c[0] + (x - c[0]) * cs - (y - c[1]) * sn, c[1] + (x - c[0]) * sn + (y - c[1]) * cs]); }
    }
    else if (op === "reshape building") { const b = findB(e.at, e.kind); if (b) setPts(b, e.pts); }
    else if (op === "reshape parcel" || op === "reshape zone") { const L = op === "reshape parcel" ? M.PAR : M.ZONE; const q = L.find((z) => z.d === d && inPoly(e.at, z.pts)); if (q) { if (op === "reshape zone") gdel(M.gZ, q, q.bb); q.pts = closeRing(e.pts); q.bb = bboxOf(q.pts); if (op === "reshape zone") gadd(M.gZ, q, q.bb); } }
    else if (op === "reshape street") { let best = null, bd = 4; for (const r of gquery(M.gR, [e.at[0] - 4, e.at[1] - 4, e.at[0] + 4, e.at[1] + 4])) if ((r.cls === "street" || r.cls === "lane" || r.cls === "main" || r.cls === "path") && r.d === d) { const dd = lineDist(e.at, r.pts); if (dd < bd) { best = r; bd = dd; } } if (best) { delR(best); best.pts = e.pts.map((q) => [q[0], q[1]]); addR(best); } }
    else if (op === "delete wall" || op === "cut wall") {
      let best = null, bd = 2; for (const w of gquery(M.gW, [e.at[0] - 2, e.at[1] - 2, e.at[0] + 2, e.at[1] + 2])) if (w.d === d) { const dd = lineDist(e.at, w.pts); if (dd < bd) { best = w; bd = dd; } }
      if (best) { delW(best); if (op === "cut wall") for (const piece of cutLine(best.pts, e.at, e.gap || 3)) addW({ t: "w", d, pts: piece }); }
    }
    else if (op === "add wall") addW({ t: "w", d, pts: e.pts.map((q) => [q[0], q[1]]) });
    else if (op === "add gate") M.GATE.push({ t: "g", d, x: e.x, y: e.y });
    else if (op === "delete gate") { let bi = -1, bd = 2; M.GATE.forEach((g, i) => { const dd = dist(e.at, [g.x, g.y]); if (g.d === d && dd < bd) { bd = dd; bi = i; } }); if (bi >= 0) M.GATE.splice(bi, 1); }
    else if (op === "add furniture") addF({ t: "f", d, kind: e.kind, x: e.x, y: e.y, ang: e.ang || 0, name: "" });
    else if (op === "delete furniture") { const f = findF(e.at, e.kind); if (f) delF(f); }
    else if (op === "move furniture") { const f = findF(e.at, e.kind); if (f) { moveF(f, e.to[0], e.to[1]); if ("ang" in e) f.ang = e.ang; } }
    else if (op === "name") { const f = findF(e.at, e.kind); if (f) f.name = e.name; }
    else if (op === "add monument") M.MON.push({ t: "m", d, kind: e.model, x: e.x, y: e.y, ang: e.ang || 0, name: e.name || "" });
    else if (op === "move monument") { const m = findM(e.at); if (m) { m.x = e.to[0]; m.y = e.to[1]; if ("ang" in e) m.ang = e.ang; } }
    else if (op === "delete monument") { const m = findM(e.at); if (m) M.MON.splice(M.MON.indexOf(m), 1); }
    else if (op === "add place") M.P.push({ t: "p", d, kind: e.type, x: e.x, y: e.y, name: e.name, note: e.note || "" });
    else if (op === "move place") { const p = M.P.find((q) => q.name === e.name); if (p) { p.x = e.x; p.y = e.y; } }
    else if (op === "delete place") { const i = M.P.findIndex((q) => q.name === e.name); if (i >= 0) M.P.splice(i, 1); }
    else if (op === "add parcel") M.PAR.push({ t: "plot", d, kind: e.kind, pts: e.pts, bb: bboxOf(e.pts) });
    else if (op === "delete parcel") { const i = M.PAR.findIndex((q) => q.d === d && inPoly(e.at, q.pts)); if (i >= 0) M.PAR.splice(i, 1); }
    else if (op === "add zone") addZ({ t: "zone", d, kind: e.kind, pts: e.pts });
    else if (op === "add street") addR({ t: "r", cls: e.kind, d, pts: e.pts, name: e.name, surf: "tar", src: e.kind === "main" ? "mains" : e.kind + "s", fresh: true });
    else if (op === "delete street") { let best = null, bd = 3; for (const r of gquery(M.gR, [e.at[0] - 3, e.at[1] - 3, e.at[0] + 3, e.at[1] + 3])) if ((r.cls === "street" || r.cls === "lane") && r.d === d) { const dd = lineDist(e.at, r.pts); if (dd < bd) { best = r; bd = dd; } } if (best) delR(best); }
    else if (op === "set surface") { let best = null, bd = 3; for (const r of gquery(M.gR, [e.at[0] - 3, e.at[1] - 3, e.at[0] + 3, e.at[1] + 3])) { const dd = lineDist(e.at, r.pts); if (dd < bd) { best = r; bd = dd; } } if (best) best.surf = e.surface; }
    else if (op === "name road") { const r = M.R.find((q) => q.cls === "main" && lineDist(e.at, q.pts) < 3); if (r) r.name = e.name; }
    M.version++;
  }

  // ------------------------------------------------------------------ the view
  let W = 0, H = 0, DPR = 1, s = 1, ox = 0, oy = 0, lastHash = "";   // screen = world * s + o
  const toW = (X, Y) => [(X - ox) / s, (Y - oy) / s];
  function resize() { DPR = window.devicePixelRatio || 1; W = cv.clientWidth; H = cv.clientHeight; cv.width = W * DPR; cv.height = H * DPR; draw(); }
  function fit(bb) { const pad = 40; s = Math.min((W - 2 * pad) / (bb[2] - bb[0]), (H - 2 * pad) / (bb[3] - bb[1])); ox = W / 2 - s * (bb[0] + bb[2]) / 2; oy = H / 2 - s * (bb[1] + bb[3]) / 2; saveView(); draw(); }
  function saveView() { try { const c = toW(W / 2, H / 2); lastHash = `#${r1(c[0])},${r1(c[1])},${s.toFixed(3)}`; history.replaceState(null, "", lastHash); } catch (e) {} }
  function viewBB(m = 0) { const a = toW(0, 0), b = toW(W, H); return [a[0] - m, a[1] - m, b[0] + m, b[1] + m]; }
  const hit = (bb, v) => !(bb[2] < v[0] || bb[0] > v[2] || bb[3] < v[1] || bb[1] > v[3]);

  // ------------------------------------------------------------------ checks (what would be wrong in the built city)
  const OK_ON_ROAD = new Set(["overhead sign", "task force truck"]);
  const ON_ART = new Set(["toll booth", "toll canopy", "border booth", "border canopy", "drums", "checkpoint"]);   // they stand on the arterial on purpose
  let checkCache = { v: -1, key: "", bad: new Map() };
  function runChecks(v) {
    const key = v.map((x) => Math.round(x / 50)).join(",");
    if (checkCache.v === M.version && checkCache.key === key) return checkCache.bad;
    const bad = new Map();
    if (s < 0.6) { checkCache = { v: M.version, key, bad }; return bad; }
    const B = [...gquery(M.gB, v)];
    for (const b of B) {
      // the market spill: stalls and kiosks may stand in a declared market-street zone (as scripts/check_district.py allows)
      const spill = (b.kind === "stalls" || b.kind === "kiosk") && [...gquery(M.gZ, b.bb)].some((z) => inPoly(centroid(b.pts), z.pts));
      for (const r of spill ? [] : gquery(M.gR, b.bb)) {
        if (r.cls === "path" || r.cls === "bridge") continue;
        if ((r.cls === "art" || r.cls === "exp") && ON_ART.has(b.kind)) continue;
        const lim = r.wd.c / 2 + r.wd.g;
        for (let i = 0; i < r.pts.length - 1; i++) {
          const a = r.pts[i], c = r.pts[i + 1];
          if (Math.max(a[0], c[0]) < b.bb[0] - lim || Math.min(a[0], c[0]) > b.bb[2] + lim || Math.max(a[1], c[1]) < b.bb[1] - lim || Math.min(a[1], c[1]) > b.bb[3] + lim) continue;
          if (polyLineDist(b.pts, a, c) < lim - 0.05) { bad.set(b, "on the road: " + (r.name || r.cls)); break; }
        }
        if (bad.has(b)) break;
      }
      if (bad.has(b)) continue;
      for (const o of gquery(M.gB, b.bb)) if (o !== b && hit(o.bb, b.bb) && polysOverlap(b.pts, o.pts)) { bad.set(b, "overlaps a " + o.kind); break; }
    }
    for (const w of gquery(M.gW, v)) {   // a compound wall across a road
      for (const r of gquery(M.gR, w.bb)) {
        if (r.cls === "path" || r.cls === "bridge") continue;
        const lim = r.wd.c / 2 + r.wd.g - 0.05; let hitR = false;
        for (let i = 0; i < w.pts.length - 1 && !hitR; i++) for (let j = 0; j < r.pts.length - 1; j++) { const a = w.pts[i], b = w.pts[i + 1], c = r.pts[j], dd = r.pts[j + 1]; if (segsCross(a, b, c, dd) || Math.min(segDist(a, c, dd), segDist(b, c, dd), segDist(c, a, b), segDist(dd, a, b)) < lim) { hitR = true; break; } }
        if (hitR) { bad.set(w, "a wall on the road: " + (r.name || r.cls)); break; }
      }
    }
    for (const f of gquery(M.gF, v)) {
      if (OK_ON_ROAD.has(f.kind)) continue;
      const p = [f.x, f.y];
      for (const r of gquery(M.gR, [f.x - 1, f.y - 1, f.x + 1, f.y + 1])) if (r.cls !== "path" && r.cls !== "bridge" && lineDist(p, r.pts) < r.wd.c / 2 - 0.2) { bad.set(f, "in the carriageway: " + (r.name || r.cls)); break; }
      if (!bad.has(f)) for (const b of gquery(M.gB, [f.x, f.y, f.x, f.y])) if (inPoly(p, b.pts) && edgeDist(p, b.pts) > 0.3) { bad.set(f, "inside a " + b.kind); break; }
    }
    checkCache = { v: M.version, key, bad };
    return bad;
  }

  // ------------------------------------------------------------------ drawing
  const LAYERS = { water: true, roads: true, gutters: true, plots: true, buildings: true, walls: true, furniture: true, places: true, labels: true, checks: true };
  const KIND_FILL = (k) => ({ front: "--home", back: "--home", extension: "--home", "face-me": "--home", "old house": "--home", "brazilian house": "--home", villa: "--home", mansion: "--home", flats: "--home",
    stalls: "--trade", shed: "--trade", kiosk: "--trade", canopy: "--trade", "phone mall": "--trade", bakery: "--trade", buka: "--trade", office: "--trade",
    school: "--civic", barracks: "--civic", cellblock: "--civic", gatehouse: "--civic", checkpoint: "--civic", palace: "--civic", "office block": "--civic", "bank tower": "--civic", hotel: "--civic",
    stilt: "--water-b", raft: "--water-b", "fishing hut": "--water-b", "smoke rack": "--water-b", barge: "--water-b" }[k] || "--works");
  const SURF = (k) => css("--" + ({ tar: "tar", worn: "worn", interlock: "interlock", laterite: "laterite", sand: "sand", mud: "mud" }[k] || "tar"));
  function path(pts, close) { ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]); if (close) ctx.closePath(); }
  let sel = null, hover = null, ghost = null, drag = null, streetPts = [];

  function draw() {
    if (!M) return;
    const v = viewBB(30);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.fillStyle = css("--paper"); ctx.fillRect(0, 0, W, H);
    ctx.setTransform(DPR * s, 0, 0, DPR * s, DPR * ox, DPR * oy);
    const px = 1 / s;   // one screen pixel in metres
    // land: the districts
    for (const d of DIST) { if (!hit(d.bb, v)) continue; path(d.poly, true); ctx.fillStyle = css("--land"); ctx.fill(); }
    if (LAYERS.water) for (const w of M.WATER) { if (!hit(w.bb, v)) continue; path(w.pts, true); ctx.fillStyle = css("--water"); ctx.fill(); ctx.strokeStyle = css("--water-line"); ctx.lineWidth = px; ctx.stroke(); }
    ctx.setLineDash([6 * px, 4 * px]); ctx.strokeStyle = css("--district"); ctx.lineWidth = 1.2 * px;
    for (const d of DIST) if (hit(d.bb, v)) { path(d.poly, true); ctx.stroke(); }
    ctx.setLineDash([]);
    if (LAYERS.plots) for (const p of M.PAR) { if (!hit(p.bb, v)) continue; path(p.pts, true); ctx.fillStyle = css("--plot"); ctx.fill(); ctx.setLineDash([4 * px, 3 * px]); ctx.strokeStyle = css("--plot-line"); ctx.lineWidth = px; ctx.stroke(); ctx.setLineDash([]); }
    if (LAYERS.plots) for (const z of M.ZONE) { if (!hit(z.bb, v)) continue; path(z.pts, true); ctx.fillStyle = css("--zone"); ctx.fill(); ctx.strokeStyle = css("--warn"); ctx.lineWidth = px; ctx.stroke(); }
    // roads, in bands so junctions merge cleanly: walkway, then gutter, then carriageway, then markings
    const R = [...gquery(M.gR, v)].filter((r) => hit(r.bb, v));
    if (LAYERS.roads) {
      ctx.lineJoin = "round"; ctx.lineCap = "butt";
      const band = (fn, col) => { for (const r of R) { const w = fn(r); if (w <= 0) continue; path(r.pts); ctx.strokeStyle = typeof col === "function" ? col(r) : col; ctx.lineWidth = w; ctx.stroke(); } };
      band((r) => r.wd.c + 2 * (r.wd.g + r.wd.w), css("--walk"));
      band((r) => r.wd.g > 0 ? r.wd.c + 2 * r.wd.g : 0, css("--gutter"));
      band((r) => r.wd.c, (r) => SURF(r.surf));
      if (s > 1.2) {   // edge lines: where the carriageway meets the gutter, to the centimetre the kit uses
        ctx.setLineDash([3, 6]); ctx.strokeStyle = "rgba(255,255,255,.75)"; ctx.lineWidth = Math.max(0.12, px);
        for (const r of R) if (r.cls === "main" || r.cls === "art" || r.cls === "exp") { path(r.pts); ctx.stroke(); }
        ctx.setLineDash([]);
      }
    }
    if (LAYERS.roads) for (const k of M.DECK) { if (!hit(k.bb, v)) continue; path(k.pts); ctx.strokeStyle = "rgba(90,90,100,.35)"; ctx.lineWidth = k.w; ctx.stroke(); ctx.strokeStyle = css("--ink"); ctx.lineWidth = px; ctx.setLineDash([2 * px, 2 * px]); ctx.stroke(); ctx.setLineDash([]); }
    if (LAYERS.gutters && s > 1.5) for (const g of M.GUT) { if (!hit(g.bb, v)) continue; path(g.pts); ctx.strokeStyle = g.state === "covered" ? "rgba(110,120,125,.5)" : "rgba(60,80,90,.8)"; ctx.lineWidth = Math.max(g.w * 0.5, px); ctx.stroke(); }
    if (s > 0.8) { ctx.strokeStyle = css("--wall"); ctx.lineWidth = Math.max(0.25, px); for (const w of M.WALL) if (hit(w.bb, v)) { path(w.pts); ctx.stroke(); } }
    // buildings
    const bad = LAYERS.checks ? runChecks(viewBB(0)) : new Map();
    if (LAYERS.buildings) {
      const lw = Math.max(px * 0.8, 0.08);
      for (const b of gquery(M.gB, v)) {
        path(b.pts, true); ctx.fillStyle = css(KIND_FILL(b.kind)); ctx.fill();
        ctx.lineWidth = bad.has(b) ? 3 * px : lw; ctx.strokeStyle = bad.has(b) ? css("--bad") : css("--home-line"); ctx.stroke();
      }
    }
    if (LAYERS.walls && s > 0.6) {
      ctx.strokeStyle = css("--wall"); ctx.lineWidth = Math.max(0.25, 1.4 * px); ctx.lineCap = "butt";
      for (const w of gquery(M.gW, v)) { path(w.pts); ctx.strokeStyle = bad.has(w) ? css("--bad") : "#8a3b2e"; ctx.lineWidth = bad.has(w) ? 3 * px : Math.max(0.25, 1.4 * px); ctx.stroke(); }
      for (const g of M.GATE) if (g.x > v[0] && g.x < v[2] && g.y > v[1] && g.y < v[3]) { const r = Math.max(0.7, 3 * px); ctx.fillStyle = "#1565c0"; ctx.fillRect(g.x - r, g.y - r, 2 * r, 2 * r); }
    }
    // furniture, to true size where it has one, never smaller than a few pixels
    if (LAYERS.furniture && s > 0.9) for (const f of gquery(M.gF, v)) drawFurniture(f, bad.has(f), px);
    for (const m of M.MON) if (m.x >= v[0] && m.x <= v[2] && m.y >= v[1] && m.y <= v[3]) { ctx.save(); ctx.translate(m.x, m.y); ctx.rotate(m.ang * Math.PI / 180); const r = Math.max(2, 6 * px); ctx.beginPath(); for (let k = 0; k < 10; k++) { const a = k * Math.PI / 5, rr = k % 2 ? r * 0.45 : r; ctx.lineTo(rr * Math.sin(a), -rr * Math.cos(a)); } ctx.closePath(); ctx.fillStyle = "#c08a00"; ctx.fill(); ctx.restore(); }
    // selection, hover, ghosts
    const outline = (o, col, w) => { ctx.strokeStyle = col; ctx.lineWidth = w * px; if (o.t === "b" || o.t === "plot" || o.t === "zone") { path(o.pts, true); ctx.stroke(); } else if (o.t === "r") { path(o.pts); ctx.lineWidth = o.wd.c + 6 * px; ctx.globalAlpha = 0.25; ctx.stroke(); ctx.globalAlpha = 1; } else { ctx.beginPath(); ctx.arc(o.x, o.y, Math.max(1.2, 9 * px), 0, 7); ctx.stroke(); } };
    if (hover && hover !== sel) outline(hover, css("--sel"), 1.5);
    if (sel) outline(sel, bad.has(sel) ? css("--bad") : css("--sel"), 3);
    const eh = tool === "select" && editPts(sel);
    if (eh) {
      const P = eh.pts, n = P.length, hs = 5 * px;
      ctx.lineWidth = 1.5 * px;
      for (let i = 0; i < (eh.closed ? n : n - 1); i++) { const a = P[i], b = P[(i + 1) % n]; ctx.beginPath(); ctx.arc((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 3.5 * px, 0, 7); ctx.fillStyle = css("--panel"); ctx.fill(); ctx.strokeStyle = css("--sel"); ctx.stroke(); }
      for (const q of P) { ctx.fillStyle = css("--panel"); ctx.fillRect(q[0] - hs, q[1] - hs, 2 * hs, 2 * hs); ctx.strokeStyle = css("--sel"); ctx.strokeRect(q[0] - hs, q[1] - hs, 2 * hs, 2 * hs); }
    }
    if (ghost) { ctx.fillStyle = css("--ghost"); ctx.strokeStyle = css("--sel"); ctx.lineWidth = 2 * px; path(ghost, true); ctx.fill(); ctx.stroke(); }
    if (streetPts.length) { path(streetPts); ctx.strokeStyle = css("--sel"); ctx.lineWidth = tool === "wall" ? Math.max(0.3, 2 * px) : Math.max(WID(kindSel.value).c, 3 * px); ctx.globalAlpha = 0.5; ctx.stroke(); ctx.globalAlpha = 1; for (const p of streetPts) { ctx.beginPath(); ctx.arc(p[0], p[1], 4 * px, 0, 7); ctx.fillStyle = css("--sel"); ctx.fill(); } }
    // labels in screen space
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    if (LAYERS.labels) drawLabels(R, v);
    if (LAYERS.places && s > 0.25) for (const p of M.P) { if (p.x < v[0] || p.x > v[2] || p.y < v[1] || p.y > v[3]) continue; const X = p.x * s + ox, Y = p.y * s + oy; ctx.fillStyle = css("--accent"); ctx.beginPath(); ctx.arc(X, Y, 4, 0, 7); ctx.fill(); if (s > 0.7) { ctx.font = "600 11px -apple-system, sans-serif"; ctx.fillStyle = css("--ink"); ctx.fillText(p.name, X + 6, Y + 4); } }
    drawScale();
    renderStatus(bad);
  }
  function drawFurniture(f, isBad, px) {
    ctx.save(); ctx.translate(f.x, f.y); ctx.rotate(f.ang * Math.PI / 180);
    const m = Math.max(1, 3 * px), col = isBad ? css("--bad") : null;
    const box = (w, h, fill) => { ctx.fillStyle = col || fill; ctx.fillRect(-w / 2, -h / 2, w, h); ctx.strokeStyle = css("--ink"); ctx.lineWidth = px; ctx.strokeRect(-w / 2, -h / 2, w, h); };
    const dot = (r, fill) => { ctx.beginPath(); ctx.arc(0, 0, r, 0, 7); ctx.fillStyle = col || fill; ctx.fill(); };
    switch (f.kind) {
      case "pole": dot(Math.max(0.18, 1.6 * px), "#5b4a3a"); break;
      case "street light": ctx.strokeStyle = col || "#555"; ctx.lineWidth = Math.max(0.12, px); ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(2.2, 0); ctx.stroke(); dot(Math.max(0.3, 2 * px), "#e0b400"); break;
      case "traffic light": box(0.6, 1.6, "#222"); break;
      case "transformer": box(1.6, 1.2, "#7b8794"); break;
      case "bus stop": box(1.4, 3.2, "#2d6cdf"); break;
      case "lasma post": box(1.6, 1.6, "#e0b400"); break;
      case "police kiosk": box(1.8, 1.8, "#c62828"); break;
      case "overhead sign": box(0.5, 16, "#2e7d32"); break;
      case "task force truck": box(5.2, 2.0, "#5d7a3a"); break;
      default: dot(Math.max(0.4, 2.5 * px), "#8e44ad");   // people placed by hand: agberos, hawkers, vendors
    }
    ctx.restore();
    if (s > 6) { ctx.save(); ctx.setTransform(DPR, 0, 0, DPR, 0, 0); ctx.font = "10px -apple-system, sans-serif"; ctx.fillStyle = css("--muted"); ctx.fillText(f.name || f.kind, f.x * s + ox + 6, f.y * s + oy - 4); ctx.restore(); }
  }
  function drawLabels(R, v) {
    ctx.font = "600 11px -apple-system, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    const done = new Set();
    for (const r of R) {
      if (!r.name || done.has(r.name) || (r.cls !== "main" && r.cls !== "art" && r.cls !== "exp") || s < 0.3) continue;
      let best = null, bl = 0;   // the longest piece in view
      for (let i = 0; i < r.pts.length - 1; i++) { const a = r.pts[i], b = r.pts[i + 1]; const L = dist(a, b); const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]; if (L > bl && m[0] > v[0] && m[0] < v[2] && m[1] > v[1] && m[1] < v[3]) { bl = L; best = [a, b, m]; } }
      if (!best || bl * s < ctx.measureText(r.name).width + 20) continue;
      done.add(r.name);
      let ang = Math.atan2(best[1][1] - best[0][1], best[1][0] - best[0][0]); if (ang > Math.PI / 2) ang -= Math.PI; if (ang < -Math.PI / 2) ang += Math.PI;
      ctx.save(); ctx.translate(best[2][0] * s + ox, best[2][1] * s + oy); ctx.rotate(ang);
      ctx.lineWidth = 3; ctx.strokeStyle = css("--paper"); ctx.strokeText(r.name, 0, 0); ctx.fillStyle = css("--ink"); ctx.fillText(r.name, 0, 0); ctx.restore();
    }
    if (s < 0.5) { ctx.font = "700 13px -apple-system, sans-serif"; for (const d of DIST) { const c = centroid(d.poly); const X = c[0] * s + ox, Y = c[1] * s + oy; if (X > 0 && X < W && Y > 0 && Y < H) { ctx.lineWidth = 3; ctx.strokeStyle = css("--paper"); ctx.strokeText(d.name, X, Y); ctx.fillStyle = css("--ink"); ctx.fillText(d.name, X, Y); } } }
    ctx.textAlign = "start"; ctx.textBaseline = "alphabetic";
  }
  function drawScale() {
    const steps = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000];
    const m = steps.find((x) => x * s > 80) || 5000, L = m * s, X = 16, Y = H - 52;
    ctx.fillStyle = css("--ink"); ctx.fillRect(X, Y, L, 2); ctx.fillRect(X, Y - 5, 1.5, 7); ctx.fillRect(X + L - 1.5, Y - 5, 1.5, 7);
    ctx.font = "11px -apple-system, sans-serif"; ctx.fillText(m >= 1000 ? m / 1000 + " km" : m + " m", X + L + 6, Y + 3);
  }

  // ------------------------------------------------------------------ reshaping: corner handles (drag), midpoint handles (drag to add a corner)
  const RESHAPE_R = new Set(["street", "lane", "main", "path"]);
  function editPts(o) {   // the points a handle edits, and whether they close
    if (!o) return null;
    if (o.t === "b") return { pts: o.pts, closed: true };
    if (o.t === "plot" || o.t === "zone") return { pts: openRing(o.pts), closed: true };
    if (o.t === "r" && RESHAPE_R.has(o.cls) && o.d) return { pts: o.pts, closed: false };
    return null;
  }
  function handleAt(X, Y) {   // a handle of the selection under the screen point
    const e = editPts(sel); if (!e || tool !== "select") return null;
    const P = e.pts, n = P.length;
    for (let i = 0; i < n; i++) if (Math.hypot(P[i][0] * s + ox - X, P[i][1] * s + oy - Y) < 8) return { i, mid: false };
    for (let i = 0; i < (e.closed ? n : n - 1); i++) { const a = P[i], b = P[(i + 1) % n]; const mx = (a[0] + b[0]) / 2 * s + ox, my = (a[1] + b[1]) / 2 * s + oy; if (Math.hypot(mx - X, my - Y) < 7) return { i, mid: true }; }
    return null;
  }
  function setEditPts(o, pts) {   // write edited points back to the object (and its index)
    if (o.t === "b") setPts(o, pts);
    else if (o.t === "plot") { o.pts = closeRing(pts); o.bb = bboxOf(o.pts); }
    else if (o.t === "zone") { gdel(M.gZ, o, o.bb); o.pts = closeRing(pts); o.bb = bboxOf(o.pts); gadd(M.gZ, o, o.bb); }
    else if (o.t === "r") { delR(o); o.pts = pts.map((q) => [q[0], q[1]]); addR(o); }
    M.version++;
  }
  function reshapeEdit(o, before, after) {   // the hand edit for a new outline; "at" is a point on the old one
    const pts = after.map((q) => [r1(q[0]), r1(q[1])]);
    if (o.t === "b") return { op: "reshape building", at: insidePt(before).map(r1), kind: o.kind, pts };
    if (o.t === "plot") return { op: "reshape parcel", at: insidePt(before).map(r1), pts };
    if (o.t === "zone") return { op: "reshape zone", at: insidePt(before).map(r1), pts };
    if (o.t === "r") { let bi = 0, bl = 0; for (let i = 0; i < before.length - 1; i++) { const L = dist(before[i], before[i + 1]); if (L > bl) { bl = L; bi = i; } } const a = before[bi], b = before[bi + 1]; return { op: "reshape street", at: [r1((a[0] + b[0]) / 2), r1((a[1] + b[1]) / 2)], pts }; }
    return null;
  }
  // a rectangle-ish building set to an exact size, angle and middle (from the panel)
  function rectFrom(o, w, dep, angDeg, cx, cy) {
    const a = angDeg * Math.PI / 180, u = [Math.cos(a), Math.sin(a)], v = [-u[1], u[0]];
    return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([i, j]) => [cx + u[0] * i * w / 2 + v[0] * j * dep / 2, cy + u[1] * i * w / 2 + v[1] * j * dep / 2]);
  }

  // ------------------------------------------------------------------ picking
  function pick(p) {
    const tol = Math.max(0.6, 8 / s);
    let best = null, bd = tol;
    for (const f of gquery(M.gF, [p[0] - tol, p[1] - tol, p[0] + tol, p[1] + tol])) { const d = dist(p, [f.x, f.y]); if (d < bd) { bd = d; best = f; } }
    if (best) return best;
    for (const m of M.MON) if (dist(p, [m.x, m.y]) < Math.max(2, tol)) return m;
    for (const q of M.P) if (dist(p, [q.x, q.y]) < Math.max(2, 6 / s)) return q;
    for (const g of M.GATE) if (dist(p, [g.x, g.y]) < Math.max(1, 6 / s)) return g;
    const bs = [...gquery(M.gB, [p[0], p[1], p[0], p[1]])].filter((b) => inPoly(p, b.pts));
    if (bs.length) return bs.sort((a, b) => area(a.pts) - area(b.pts))[0];
    if (LAYERS.walls) { let wb = null, wd = Math.max(0.4, 5 / s); for (const w of gquery(M.gW, [p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2])) { const d = lineDist(p, w.pts); if (d < wd) { wd = d; wb = w; } } if (wb) { wb.clickAt = [p[0], p[1]]; return wb; } }
    let rb = null, rd = 1e9;
    for (const r of gquery(M.gR, [p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5])) { const d = lineDist(p, r.pts); if (d < r.wd.c / 2 + r.wd.g + 0.5 && d < rd) { rd = d; rb = r; } }
    if (rb) return rb;
    const pl = M.PAR.find((q) => hit(q.bb, [p[0], p[1], p[0], p[1]]) && inPoly(p, q.pts));
    return pl || M.ZONE.find((q) => hit(q.bb, [p[0], p[1], p[0], p[1]]) && inPoly(p, q.pts)) || null;
  }
  const area = (pts) => Math.abs(pts.reduce((a, p, i) => { const q = pts[(i + 1) % pts.length]; return a + p[0] * q[1] - q[0] * p[1]; }, 0)) / 2;
  const insidePt = (pts) => { const c = centroid(pts); if (inPoly(c, pts)) return c; for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 2) % pts.length]; const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]; if (inPoly(m, pts)) return m; } return pts[0]; };

  // ------------------------------------------------------------------ saving edits
  let SERVER = true, pendingN = 0, thawN = 0;
  async function send(d, edit) {
    if (!SERVER) { toast("Read-only: start the board server (python3 scripts/board_server.py) to save edits"); return false; }
    try {
      const r = await fetch("/api/edit", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ d, edit }) });
      const j = await r.json(); if (!r.ok) { toast(j.error || "Not saved"); return false; }
      pendingN = j.pending; if (["add street", "delete street", "cut street", "name road", "reshape street"].includes(edit.op)) thawN++;
      return true;
    } catch (e) { SERVER = false; toast("The board server isn't running, so this edit wasn't saved"); return false; }
  }
  async function commit(d, edit) { if (!d) { toast("That's outside every district"); return; } if (await send(d, edit)) { apply(d, edit); draw(); showPanel(); } else { draw(); } }

  // ------------------------------------------------------------------ tools
  const KINDS = {
    furniture: ["pole", "street light", "traffic light", "bus stop", "lasma post", "transformer", "police kiosk", "agbero", "bread hawker", "wheelbarrow vendor", "fruit seller", "parking boy", "overhead sign", "task force truck"],
    building: ["front", "back", "extension", "shed", "kiosk", "stalls", "face-me", "buka", "office", "school", "flats", "office block", "canopy"],
    street: ["street", "lane", "main"],
    surface: ["tar", "worn", "interlock", "laterite", "sand", "mud"],
  };
  let tool = "select";
  const kindSel = $("kind");
  function setTool(t) {
    tool = t; streetPts = []; ghost = null;
    document.querySelectorAll("#tools button").forEach((b) => b.classList.toggle("on", b.dataset.tool === t));
    kindSel.innerHTML = ""; kindSel.parentElement.style.display = KINDS[t] ? "" : "none";
    (KINDS[t] || []).forEach((k) => { const o = document.createElement("option"); o.value = o.textContent = k; kindSel.appendChild(o); });
    cv.className = t === "select" ? "" : "place";
    showPanel(); draw();
  }
  document.querySelectorAll("#tools button").forEach((b) => b.addEventListener("click", () => setTool(b.dataset.tool)));

  // snap a point to the nearest road's centre line or end within 3 m (streets drawn by hand join the network exactly)
  function snapToRoad(p, skip) {
    let best = null, bd = Math.max(3, 10 / s);
    for (const r of gquery(M.gR, [p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10])) {
      if (r === skip) continue;
      for (const e of [r.pts[0], r.pts[r.pts.length - 1]]) { const d = dist(p, e); if (d < bd) { bd = d; best = e.slice(); } }
      for (let i = 0; i < r.pts.length - 1; i++) { const q = nearestOnSeg(p, r.pts[i], r.pts[i + 1]); const d = dist(p, q); if (d < bd * 0.7) { bd = d; best = q; } }
    }
    return best;
  }
  // furniture goes on the walkway: just off the carriageway and gutter of the nearest road, facing it
  function snapToKerb(p) {
    let best = null, bd = 6;
    for (const r of gquery(M.gR, [p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10])) {
      if (r.cls === "path" || r.cls === "bridge") continue;
      for (let i = 0; i < r.pts.length - 1; i++) {
        const a = r.pts[i], b = r.pts[i + 1], q = nearestOnSeg(p, a, b), d = dist(p, q);
        const edge = r.wd.c / 2 + r.wd.g + Math.min(0.6, r.wd.w / 2 || 0.4);
        if (Math.abs(d - edge) < bd) {
          bd = Math.abs(d - edge);
          const nx = d > 1e-6 ? (p[0] - q[0]) / d : -(b[1] - a[1]) / dist(a, b), ny = d > 1e-6 ? (p[1] - q[1]) / d : (b[0] - a[0]) / dist(a, b);
          best = { x: q[0] + nx * edge, y: q[1] + ny * edge, ang: Math.atan2(-ny, -nx) * 180 / Math.PI };
        }
      }
    }
    return best;
  }

  // ------------------------------------------------------------------ pointer and keys
  let panning = null, spaceDown = false;
  cv.addEventListener("pointerdown", (ev) => {
    cv.setPointerCapture(ev.pointerId);
    const p = toW(ev.offsetX, ev.offsetY);
    if (ev.button === 1 || ev.button === 2 || spaceDown) { probList = null; panning = { x: ev.clientX, y: ev.clientY, ox, oy }; cv.classList.add("panning"); return; }
    if (tool === "select") {
      const hnd = handleAt(ev.offsetX, ev.offsetY);
      if (hnd) {
        const e = editPts(sel), before = e.pts.map((q) => q.slice());
        let pts = before.map((q) => q.slice()), i = hnd.i;
        if (hnd.mid) { i = hnd.i + 1; pts.splice(i, 0, [(before[hnd.i][0] + before[(hnd.i + 1) % before.length][0]) / 2, (before[hnd.i][1] + before[(hnd.i + 1) % before.length][1]) / 2]); }
        if (ev.altKey && !hnd.mid) {   // Option/Alt-click a corner: remove it
          if (pts.length <= (e.closed ? 3 : 2)) { toast("It needs at least " + (e.closed ? 3 : 2) + " points"); return; }
          pts.splice(i, 1); const o = sel; setEditPts(o, pts); draw();
          send(o.d, reshapeEdit(o, before, pts)).then((ok) => { if (!ok) { setEditPts(o, before); draw(); } showPanel(); });
          return;
        }
        drag = { vtx: i, o: null, obj: sel, before, pts }; cv.classList.add("move"); return;
      }
      const o = pick(p);
      if (o && (o.t === "b" || o.t === "f" || o.t === "m" || o.t === "p")) { sel = o; drag = { o, start: p, last: p, moved: false }; showPanel(); draw(); return; }
      sel = o; showPanel(); probList = null; panning = { x: ev.clientX, y: ev.clientY, ox, oy, click: true }; draw(); return;
    }
    if (tool === "furniture") { const k = kindSel.value; const sn = ev.shiftKey ? null : snapToKerb(p); const at = sn || { x: p[0], y: p[1], ang: 0 }; commit(districtAt([at.x, at.y]), { op: "add furniture", kind: k, x: r1(at.x), y: r1(at.y), ang: Math.round(at.ang) }); return; }
    if (tool === "building") { drag = { box: p }; return; }
    if (tool === "street") { const q = (!ev.shiftKey && snapToRoad(p)) || p; streetPts.push([r1(q[0]), r1(q[1])]); if (ev.detail >= 2) finishStreet(); draw(); return; }
    if (tool === "wall") { streetPts.push([r1(p[0]), r1(p[1])]); if (ev.detail >= 2) finishWall(); draw(); return; }
    if (tool === "gate") { let wb = null, wd = 2; for (const w of gquery(M.gW, [p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2])) { const d = lineDist(p, w.pts); if (d < wd) { wd = d; wb = w; } } if (!wb) { toast("Click on a wall"); return; } let q = p, bd = 1e9; for (let i = 0; i < wb.pts.length - 1; i++) { const c = nearestOnSeg(p, wb.pts[i], wb.pts[i + 1]); if (dist(p, c) < bd) { bd = dist(p, c); q = c; } } commit(wb.d, { op: "add gate", x: r1(q[0]), y: r1(q[1]) }); return; }
    if (tool === "surface") { const o = pick(p); if (!o || o.t !== "r") { toast("Click on a road"); return; } commit(o.d || districtAt(p), { op: "set surface", at: [r1(p[0]), r1(p[1])], surface: kindSel.value }); return; }
  });
  cv.addEventListener("pointermove", (ev) => {
    const p = toW(ev.offsetX, ev.offsetY);
    $("where").textContent = `x ${p[0].toFixed(1)} m · y ${p[1].toFixed(1)} m · ${districtName(districtAt(p))}`;
    if (panning) { if (Math.hypot(ev.clientX - panning.x, ev.clientY - panning.y) > 3) panning.click = false; ox = panning.ox + ev.clientX - panning.x; oy = panning.oy + ev.clientY - panning.y; draw(); return; }
    if (drag && drag.vtx !== undefined) {
      let q = p;
      if (drag.obj.t === "r" && !ev.shiftKey && (drag.vtx === 0 || drag.vtx === drag.pts.length - 1)) {   // a street's end snaps onto another road
        const sn = snapToRoad(p, drag.obj); if (sn) q = sn;
      } else if (!ev.shiftKey) {   // corners snap to other corners nearby
        let bd = 6 / s; for (const b of gquery(M.gB, [p[0] - 1, p[1] - 1, p[0] + 1, p[1] + 1])) if (b !== drag.obj) for (const c of b.pts) { const d = dist(c, p); if (d < bd) { bd = d; q = c.slice(); } }
      }
      drag.pts[drag.vtx] = [q[0], q[1]]; setEditPts(drag.obj, drag.pts); draw(); return;
    }
    if (drag && drag.o) {
      const o = drag.o; let dx = p[0] - drag.last[0], dy = p[1] - drag.last[1];
      if (!drag.moved && dist(p, drag.start) * s < 4) return;
      if (!drag.moved) { drag.moved = true; drag.orig = o.t === "b" ? o.pts.map((q) => q.slice()) : [o.x, o.y, o.ang]; drag.at = o.t === "b" ? insidePt(o.pts) : [o.x, o.y]; cv.classList.add("move"); }
      if (o.t === "b") moveB(o, ([x, y]) => [x + dx, y + dy]);
      else if (o.t === "f") { const sn = !ev.shiftKey && o.kind !== "overhead sign" ? snapToKerb(p) : null; if (sn) { moveF(o, sn.x, sn.y); o.ang = sn.ang; } else moveF(o, o.x + dx, o.y + dy); }
      else { o.x += dx; o.y += dy; }
      drag.last = p; M.version++; draw(); return;
    }
    if (drag && drag.box) { const a = drag.box; ghost = [[a[0], a[1]], [p[0], a[1]], [p[0], p[1]], [a[0], p[1]]]; draw(); return; }
    if (tool === "select") { cv.style.cursor = handleAt(ev.offsetX, ev.offsetY) ? "pointer" : ""; const o = pick(p); if (o !== hover) { hover = o; draw(); } }
  });
  cv.addEventListener("pointerup", async (ev) => {
    cv.classList.remove("panning", "move");
    if (panning) { const wasClick = panning.click; panning = null; saveView(); if (wasClick && tool === "select") { /* selection already set */ } return; }
    if (drag && drag.vtx !== undefined) {
      const { obj, before, pts } = drag; drag = null;
      const ok = await send(obj.d || districtAt(centroid(before)), reshapeEdit(obj, before, pts));
      if (!ok) setEditPts(obj, before);
      draw(); showPanel(); return;
    }
    if (drag && drag.o) {
      const { o, moved } = drag; drag = null;
      if (!moved) return;
      let edit;
      if (o.t === "b") { const c0 = centroid(drag_orig(o)), c1 = centroid(o.pts); edit = { op: "move building", at: [r1(dragAt[0]), r1(dragAt[1])], kind: o.kind, by: [r1(c1[0] - c0[0]), r1(c1[1] - c0[1])] }; }
      else if (o.t === "f") edit = { op: "move furniture", at: [r1(dragOrig[0]), r1(dragOrig[1])], kind: o.kind, to: [r1(o.x), r1(o.y)], ang: Math.round(o.ang) };
      else if (o.t === "m") edit = { op: "move monument", at: [r1(dragOrig[0]), r1(dragOrig[1])], to: [r1(o.x), r1(o.y)] };
      else if (o.t === "p") edit = { op: "move place", name: o.name, x: r1(o.x), y: r1(o.y) };
      const ok = await send(o.d || districtAt([o.x, o.y]), edit);
      if (!ok) revert(o);
      draw(); showPanel(); return;
    }
    if (drag && drag.box) {
      const g = ghost; drag = null; ghost = null;
      if (g && Math.abs(g[2][0] - g[0][0]) > 1 && Math.abs(g[2][1] - g[0][1]) > 1) { const pts = g.map((q) => [r1(q[0]), r1(q[1])]); commit(districtAt(centroid(pts)), { op: "add building", kind: kindSel.value, pts }); }
      draw();
    }
  });
  // what a drag started from (kept outside the drag object, which is cleared before the edit is sent)
  let dragOrig = null, dragAt = null, dragPts = null;
  const drag_orig = () => dragPts;
  cv.addEventListener("pointerdown", () => { if (drag && drag.o) { const o = drag.o; dragPts = o.t === "b" ? o.pts.map((q) => q.slice()) : null; dragAt = o.t === "b" ? insidePt(o.pts) : null; dragOrig = o.t !== "b" ? [o.x, o.y, o.ang] : null; } });
  function revert(o) {
    if (o.t === "b" && dragPts) { moveB(o, (q, i) => dragPts[i]); }
    else if (o.t === "f" && dragOrig) { moveF(o, dragOrig[0], dragOrig[1]); o.ang = dragOrig[2]; }
    else if (dragOrig) { o.x = dragOrig[0]; o.y = dragOrig[1]; }
    M.version++;
  }
  cv.addEventListener("wheel", (ev) => {
    ev.preventDefault(); probList = null;
    const k = Math.exp(-ev.deltaY * (ev.ctrlKey ? 0.01 : 0.0015)), p = toW(ev.offsetX, ev.offsetY);
    s = Math.min(80, Math.max(0.02, s * k)); ox = ev.offsetX - p[0] * s; oy = ev.offsetY - p[1] * s; draw(); clearTimeout(cv._t); cv._t = setTimeout(saveView, 300);
  }, { passive: false });
  cv.addEventListener("contextmenu", (e) => e.preventDefault());
  function finishWall() { const pts = streetPts; streetPts = []; if (pts.length < 2) { draw(); return; } commit(districtAt(pts[0]), { op: "add wall", pts }); }
  function finishStreet() {
    const pts = streetPts; streetPts = [];
    if (pts.length < 2) { draw(); return; }
    const k = kindSel.value, edit = { op: "add street", kind: k, pts };
    if (k === "main") { const n = prompt("Name of the new main road?"); if (!n) { draw(); return; } edit.name = n; }
    commit(districtAt(pts[Math.floor(pts.length / 2)]), edit);
  }
  async function rotateSel(deg) {
    const o = sel; if (!o) return;
    if (o.t === "b") { const at = insidePt(o.pts); const c = centroid(o.pts), a = deg * Math.PI / 180, cs = Math.cos(a), sn = Math.sin(a); const before = o.pts.map((q) => q.slice());
      moveB(o, ([x, y]) => [c[0] + (x - c[0]) * cs - (y - c[1]) * sn, c[1] + (x - c[0]) * sn + (y - c[1]) * cs]); M.version++; draw();
      if (!(await send(o.d, { op: "move building", at: [r1(at[0]), r1(at[1])], kind: o.kind, by: [0, 0], rotate: deg }))) { moveB(o, (q, i) => before[i]); M.version++; } }
    else if (o.t === "f") { const a0 = o.ang; o.ang = Math.round(o.ang + deg); M.version++; draw(); if (!(await send(o.d, { op: "move furniture", at: [r1(o.x), r1(o.y)], kind: o.kind, to: [r1(o.x), r1(o.y)], ang: o.ang }))) { o.ang = a0; M.version++; } }
    else if (o.t === "m") { const a0 = o.ang; o.ang = Math.round(o.ang + deg); draw(); if (!(await send(o.d, { op: "move monument", at: [r1(o.x), r1(o.y)], to: [r1(o.x), r1(o.y)], ang: o.ang }))) o.ang = a0; }
    draw(); showPanel();
  }
  async function deleteSel() {
    const o = sel; if (!o) return;
    let d = o.d, edit;
    if (o.t === "b") edit = { op: "delete building", at: insidePt(o.pts).map(r1), kind: o.kind };
    else if (o.t === "f") edit = { op: "delete furniture", at: [r1(o.x), r1(o.y)], kind: o.kind };
    else if (o.t === "m") edit = { op: "delete monument", at: [r1(o.x), r1(o.y)] };
    else if (o.t === "p") edit = { op: "delete place", name: o.name };
    else if (o.t === "plot") edit = { op: "delete parcel", at: insidePt(o.pts).map(r1) };
    else if (o.t === "w") edit = { op: "delete wall", at: (o.clickAt || o.pts[0]).map(r1) };
    else if (o.t === "g") edit = { op: "delete gate", at: [r1(o.x), r1(o.y)] };
    else if (o.t === "r") {
      if (o.cls !== "street" && o.cls !== "lane") { toast("Main roads and arterials are the city's frame: they can't be deleted here"); return; }
      const mid = o.pts[Math.floor(o.pts.length / 2)], prev = o.pts[Math.floor(o.pts.length / 2) - 1] || o.pts[0];
      edit = { op: "delete street", at: [r1((mid[0] + prev[0]) / 2), r1((mid[1] + prev[1]) / 2)] };
    }
    else { toast("That can't be deleted here yet"); return; }
    sel = null; await commit(d || districtAt(edit.at || [o.x, o.y]), edit);
  }
  window.addEventListener("keydown", (ev) => {
    if (ev.target.tagName === "INPUT") return;
    if (ev.key === " ") { spaceDown = true; cv.classList.add("pan"); ev.preventDefault(); return; }
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === "z") { ev.preventDefault(); undo(); return; }
    const k = ev.key.toLowerCase();
    if (k === "escape") { streetPts = []; ghost = null; drag = null; if (tool !== "select") setTool("select"); else { sel = null; showPanel(); } draw(); }
    else if (k === "enter" && tool === "street") finishStreet();
    else if (k === "enter" && tool === "wall") finishWall();
    else if (k === "backspace" || k === "delete") { ev.preventDefault(); if ((tool === "street" || tool === "wall") && streetPts.length) { streetPts.pop(); draw(); } else deleteSel(); }
    else if (k === "r") rotateSel(ev.shiftKey ? -15 : 15);
    else if (k === "[" ) rotateSel(-1); else if (k === "]") rotateSel(1);
    else if (k === "v") setTool("select"); else if (k === "f") setTool("furniture"); else if (k === "b") setTool("building"); else if (k === "s") setTool("street"); else if (k === "u") setTool("surface"); else if (k === "w") setTool("wall"); else if (k === "g") setTool("gate");
  });
  window.addEventListener("keyup", (ev) => { if (ev.key === " ") { spaceDown = false; cv.classList.remove("pan"); } });

  async function undo() {
    if (!SERVER) return;
    const r = await fetch("/api/undo", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
    const j = await r.json(); if (!r.ok) { toast(j.error); return; }
    sel = null; await loadPending(); toast("Undone");
  }

  // ------------------------------------------------------------------ panel and status
  const districtName = (id) => (DIST.find((d) => d.id === id) || {}).name || "outside the districts";
  function row(k, v) { return `<tr><td>${k}</td><td>${v}</td></tr>`; }
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function showPanel() {
    const P = $("panel"), o = sel;
    const help = `<div id="help"><b>Select</b>: click a thing; drag it to move (furniture snaps to the walkway; hold <kbd>Shift</kbd> to place freely). <kbd>R</kbd>/<kbd>Shift R</kbd> turn 15°, <kbd>[</kbd> <kbd>]</kbd> turn 1°, <kbd>Delete</kbd> removes, <kbd>⌘Z</kbd> undoes. Selected buildings, plots, zones and streets show handles: drag a square to move a corner, a circle to add one, <kbd>⌥</kbd>-click to remove one; exact sizes in the panel. Drag empty ground or hold <kbd>Space</kbd> to pan; scroll to zoom.<br><br><b>Furniture</b>: click to place. <b>Building</b>: drag a box. <b>Street</b>: click points (they snap onto roads to join them), <kbd>Enter</kbd> to finish. <b>Surface</b>: click a road. <b>Wall</b>: click points, <kbd>Enter</kbd> to finish. <b>Gate</b>: click a wall.<br><br>Red outlines are problems the built city would have: a house or a wall on a road, overlapping buildings, a pole in the carriageway.</div>`;
    if (!o) { P.innerHTML = `<h3>${tool === "select" ? "Nothing selected" : "Placing: " + tool}</h3>` + help; return; }
    const bad = runChecks(viewBB(0)).get(o);
    let h = "";
    if (o.t === "b") { const bb = o.bb, c = centroid(o.pts); const e0 = dist(o.pts[0], o.pts[1]), e1 = dist(o.pts[1], o.pts[2] || o.pts[0]); h = `<h3>Building: ${esc(o.kind)}</h3><table>${row("District", districtName(o.d))}${row("Middle", `${c[0].toFixed(1)}, ${c[1].toFixed(1)} m`)}${row("Size", `${e0.toFixed(1)} × ${e1.toFixed(1)} m`)}${row("Footprint", area(o.pts).toFixed(0) + " m²")}${row("Storeys", o.st)}${row("Facing", (Math.atan2(o.pts[1][1] - o.pts[0][1], o.pts[1][0] - o.pts[0][0]) * 180 / Math.PI).toFixed(0) + "°")}</table>`; }
    else if (o.t === "f") h = `<h3>${esc(o.kind)}</h3><table>${row("District", districtName(o.d))}${row("At", `${o.x.toFixed(1)}, ${o.y.toFixed(1)} m`)}${row("Turned", Math.round(o.ang) + "°")}${o.name ? row("Name", esc(o.name)) : ""}</table>${["bus stop", "traffic light", "lasma post", "police kiosk"].includes(o.kind) ? `<label class="k">Name (the label it carries)</label><input id="nm" value="${esc(o.name)}" placeholder="e.g. Under Bridge">` : ""}`;
    else if (o.t === "m") h = `<h3>Monument: ${esc(o.name || o.kind)}</h3><table>${row("Model", esc(o.kind))}${row("At", `${o.x.toFixed(1)}, ${o.y.toFixed(1)} m`)}${row("Turned", Math.round(o.ang) + "°")}</table>`;
    else if (o.t === "p") h = `<h3>${esc(o.name)}</h3><table>${row("Type", esc(o.kind))}${row("District", districtName(o.d))}${row("At", `${o.x.toFixed(1)}, ${o.y.toFixed(1)} m`)}</table><p class="k">${esc(o.note)}</p>`;
    else if (o.t === "r") { const L = o.pts.reduce((a, p, i) => i ? a + dist(o.pts[i - 1], p) : 0, 0); h = `<h3>${esc(o.name || "A " + o.cls)}</h3><table>${row("Kind", o.cls)}${row("District", districtName(o.d) )}${row("Length", L.toFixed(0) + " m")}${row("Carriageway", o.wd.c + " m")}${row("Gutters", o.wd.g + " m each side")}${row("Walkways", o.wd.w + " m each side")}${row("Surface", o.surf)}${row("Starts", `${o.pts[0][0].toFixed(1)}, ${o.pts[0][1].toFixed(1)}`)}${row("Ends", `${o.pts[o.pts.length - 1][0].toFixed(1)}, ${o.pts[o.pts.length - 1][1].toFixed(1)}`)}</table>`; }
    else if (o.t === "w") { const L = o.pts.reduce((a, q, i) => i ? a + dist(o.pts[i - 1], q) : 0, 0); h = `<h3>Compound wall</h3><table>${row("District", districtName(o.d))}${row("Length", L.toFixed(1) + " m")}</table><p class="k">Worked out by the bake round walled houses (scripts/compounds.py). Delete the piece, or cut a 3 m opening where you clicked.</p><div class="row"><button id="cutw">Cut an opening here</button></div>`; }
    else if (o.t === "g") h = `<h3>Gate</h3><table>${row("District", districtName(o.d))}${row("At", `${o.x.toFixed(1)}, ${o.y.toFixed(1)} m`)}</table>`;
    else if (o.t === "plot" || o.t === "zone") h = `<h3>${o.t === "plot" ? "Plot" : "Zone"}: ${esc(o.kind)}</h3><table>${row("District", districtName(o.d))}${row("Area", area(o.pts).toFixed(0) + " m²")}</table>`;
    if (o.t === "b") { const c = centroid(o.pts), w = dist(o.pts[0], o.pts[1]), dep = dist(o.pts[1], o.pts[2] || o.pts[0]), ang = Math.atan2(o.pts[1][1] - o.pts[0][1], o.pts[1][0] - o.pts[0][0]) * 180 / Math.PI;
      h += `<hr><b>Exact size and place</b>${o.pts.length !== 4 ? '<p class="k">Setting a size makes it a rectangle.</p>' : ""}<table>${row("Width (m)", `<input id="nw" type="number" step="0.1" value="${w.toFixed(1)}">`)}${row("Depth (m)", `<input id="nd" type="number" step="0.1" value="${dep.toFixed(1)}">`)}${row("Angle (°)", `<input id="na" type="number" step="1" value="${ang.toFixed(0)}">`)}${row("Middle x", `<input id="nx" type="number" step="0.1" value="${c[0].toFixed(1)}">`)}${row("Middle y", `<input id="ny" type="number" step="0.1" value="${c[1].toFixed(1)}">`)}</table><p class="k">Or drag a corner square; drag a round handle to add a corner; ⌥-click a corner to remove it.</p>`; }
    if (o.t === "f" || o.t === "m") h += `<hr><b>Exact place</b><table>${row("x", `<input id="fx" type="number" step="0.1" value="${o.x.toFixed(1)}">`)}${row("y", `<input id="fy" type="number" step="0.1" value="${o.y.toFixed(1)}">`)}${row("Angle (°)", `<input id="fa" type="number" step="1" value="${Math.round(o.ang)}">`)}</table>`;
    if (o.t === "plot" || o.t === "zone" || (o.t === "r" && RESHAPE_R.has(o.cls) && o.d)) h += `<p class="k">Drag a corner square to reshape; drag a round handle to add a point; ⌥-click a point to remove it.${o.t === "r" ? " A street's ends snap onto other roads." : ""}</p>`;
    h += bad ? `<p class="bad">⚠ ${esc(bad)}</p>` : (o.t === "b" || o.t === "f") ? `<p class="ok">No problems found</p>` : "";
    h += `<div class="row">${["b", "f", "m"].includes(o.t) ? `<button id="rl">⟲ 15°</button><button id="rr">⟳ 15°</button>` : ""}<button id="del">Delete</button></div><hr>` + help;
    P.innerHTML = h;
    const on = (id, fn) => { const e = $(id); if (e) e.addEventListener("click", fn); };
    on("rl", () => rotateSel(-15)); on("rr", () => rotateSel(15)); on("del", deleteSel);
    on("cutw", () => { const at = (o.clickAt || o.pts[0]).map(r1); sel = null; commit(o.d, { op: "cut wall", at, gap: 3 }); });
    const num = (id) => parseFloat(($(id) || {}).value);
    if (o.t === "b" && $("nw")) ["nw", "nd", "na", "nx", "ny"].forEach((id) => $(id).addEventListener("change", async () => {
      const w = num("nw"), dep = num("nd"), a = num("na"), x = num("nx"), y = num("ny");
      if (![w, dep, a, x, y].every(isFinite) || w < 0.5 || dep < 0.5) { toast("Size needs numbers of at least 0.5 m"); showPanel(); return; }
      const before = o.pts.map((q) => q.slice()), after = rectFrom(o, w, dep, a, x, y);
      setEditPts(o, after); draw();
      if (!(await send(o.d, reshapeEdit(o, before, after)))) setEditPts(o, before);
      draw(); showPanel();
    }));
    if ((o.t === "f" || o.t === "m") && $("fx")) ["fx", "fy", "fa"].forEach((id) => $(id).addEventListener("change", async () => {
      const x = num("fx"), y = num("fy"), a = num("fa"); if (![x, y, a].every(isFinite)) return;
      const at = [r1(o.x), r1(o.y)], was = [o.x, o.y, o.ang];
      if (o.t === "f") moveF(o, x, y); else { o.x = x; o.y = y; } o.ang = a; M.version++; draw();
      const edit = o.t === "f" ? { op: "move furniture", at, kind: o.kind, to: [r1(x), r1(y)], ang: Math.round(a) } : { op: "move monument", at, to: [r1(x), r1(y)], ang: Math.round(a) };
      if (!(await send(o.d, edit))) { if (o.t === "f") moveF(o, was[0], was[1]); else { o.x = was[0]; o.y = was[1]; } o.ang = was[2]; M.version++; }
      draw(); showPanel();
    }));
    const nm = $("nm"); if (nm) nm.addEventListener("change", () => commit(o.d, { op: "name", at: [r1(o.x), r1(o.y)], kind: o.kind, name: nm.value }));
  }
  function renderStatus(bad) {
    const n = { road: 0, overlap: 0, furn: 0 };
    for (const [o, why] of bad) { if (o.t === "f") n.furn++; else if (why.startsWith("on the road")) n.road++; else n.overlap++; }
    $("checks").innerHTML = s < 0.6 ? "Zoom in to check" : `In view: <b style="color:${n.road ? css("--bad") : "inherit"}">${n.road}</b> on a road · <b style="color:${n.overlap ? css("--bad") : "inherit"}">${n.overlap}</b> overlapping · <b style="color:${n.furn ? css("--bad") : "inherit"}">${n.furn}</b> furniture misplaced`;
    $("pending").textContent = !SERVER ? "Read-only (no board server)" : pendingN ? `${pendingN} edit${pendingN > 1 ? "s" : ""} not baked yet${thawN ? ` (${thawN} road edit${thawN > 1 ? "s" : ""}: needs a thaw bake)` : ""}` : "Everything is baked";
  }
  // click the problem count to go to each problem in view in turn
  let probI = 0, probList = null;   // the problems in view when you first click; panning or zooming starts a new list
  $("checks").style.cursor = "pointer"; $("checks").title = "Go to the next problem";
  $("checks").addEventListener("click", () => {
    if (!probList) { probList = [...runChecks(viewBB(0)).keys()]; probI = 0; }
    const list = probList; if (!list.length) { probList = null; toast("No problems in view"); return; }
    const o = list[probI++ % list.length]; toast(`Problem ${((probI - 1) % list.length) + 1} of ${list.length}`); const c = o.t === "b" ? centroid(o.pts) : [o.x, o.y];
    sel = o; s = Math.max(s, 6); ox = W / 2 - c[0] * s; oy = H / 2 - c[1] * s; saveView(); draw(); showPanel();
  });
  let toastT; function toast(t) { const e = $("toast"); e.textContent = t; e.style.display = "block"; clearTimeout(toastT); toastT = setTimeout(() => (e.style.display = "none"), 3500); }

  // ------------------------------------------------------------------ layers, districts, theme
  const LNAME = { water: "Water", roads: "Roads", gutters: "Gutters", plots: "Plots", buildings: "Buildings", walls: "Walls", furniture: "Furniture", places: "Places", labels: "Labels", checks: "Checks" };
  for (const k of Object.keys(LAYERS)) { const l = document.createElement("label"); l.innerHTML = `<input type="checkbox" ${LAYERS[k] ? "checked" : ""}> ${LNAME[k]}`; l.querySelector("input").addEventListener("change", (e) => { LAYERS[k] = e.target.checked; draw(); }); $("layers").appendChild(l); }
  const dsel = $("district");
  dsel.innerHTML = `<option value="">Go to a district…</option>` + DIST.map((d) => `<option value="${d.id}">${esc(d.name)}</option>`).join("");
  dsel.addEventListener("change", () => { const d = DIST.find((x) => x.id === dsel.value); if (d) fit(d.bb); dsel.value = ""; });
  $("theme").addEventListener("click", () => { const r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; r.dataset.theme = dark ? "light" : "dark"; try { localStorage.setItem("board-theme", r.dataset.theme); } catch (e) {} draw(); });
  try { const t = localStorage.getItem("board-theme"); if (t) document.documentElement.dataset.theme = t; } catch (e) {}

  // ------------------------------------------------------------------ start
  async function loadPending() {
    build();
    try {
      const r = await fetch("/api/pending", { cache: "no-store" }); if (!r.ok) throw new Error();
      const j = await r.json(); SERVER = true;
      const fresh = j.edits.filter((e) => e.t > j.data_time);   // older ones are in the baked map already
      for (const e of fresh) apply(e.d, e.edit);
      pendingN = fresh.length; thawN = fresh.filter((e) => e.thaw).length;
    } catch (e) { SERVER = false; }
    draw(); showPanel();
  }
  window.addEventListener("resize", resize);
  W = cv.clientWidth; H = cv.clientHeight; DPR = window.devicePixelRatio || 1; cv.width = W * DPR; cv.height = H * DPR;

  function viewFromHash() {   // #x,y,zoom: a spot to bookmark or share; changing it moves the view
    const hv = location.hash.slice(1).split(",").map(Number);
    if (hv.length !== 3 || !hv.every(isFinite)) return false;
    s = hv[2]; ox = W / 2 - hv[0] * s; oy = H / 2 - hv[1] * s; return true;
  }
  window.addEventListener("hashchange", () => { if (location.hash !== lastHash && viewFromHash()) draw(); });
  const hv = location.hash.slice(1).split(",").map(Number);
  if (viewFromHash()) {}
  else { const d = DIST.find((x) => x.id === "maze"); s = 1; fit(d.bb); }
  setTool("select");
  loadPending();
})();
