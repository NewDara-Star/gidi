/* The new map's editor on the drawing board's new frame (board.html; docs/MAP-FORMAT.md). Draws and saves the
   plan layer, record by record, in map/<district>/district.json and plan.json through scripts/board_server.py, which runs
   scripts/check_map.py on every save. Everything is drawn by hand over the study underlay (web/frame.js): nothing from the
   study is copied into the map, except a new district's outline when it is first started. A field nobody has set stays
   unset and the panel says it needs a value: the board never fills one in. Only containers start filled: empty lists, and
   "none" for a kind that has a none (no kerb, no median, no outside stair), shown in the panel like any other value. */
window.MAPEDIT = (() => {
  "use strict";
  let V = null, F = null, SCHEMA = null;
  const $ = (id) => document.getElementById(id);
  const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const clone = (o) => JSON.parse(JSON.stringify(o));
  const r2 = (v) => Math.round(v * 100) / 100;

  // ------------------------------------------------------------------ geometry
  const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
  function nearestOnSeg(p, a, b) {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = dx * dx + dy * dy;
    let t = L ? ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L : 0; t = Math.max(0, Math.min(1, t));
    return [a[0] + t * dx, a[1] + t * dy];
  }
  const segDist = (p, a, b) => dist(p, nearestOnSeg(p, a, b));
  function lineDist(p, pts) { let m = 1e9; for (let i = 0; i < pts.length - 1; i++) m = Math.min(m, segDist(p, pts[i], pts[i + 1])); return m; }
  function ringDist(p, pts) { let m = 1e9; for (let i = 0; i < pts.length; i++) m = Math.min(m, segDist(p, pts[i], pts[(i + 1) % pts.length])); return m; }
  function inPoly(p, poly) { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const a = poly[i], b = poly[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]) c = !c; } return c; }
  const centroid = (pts) => [pts.reduce((s, q) => s + q[0], 0) / pts.length, pts.reduce((s, q) => s + q[1], 0) / pts.length];
  const signedArea = (r) => r.reduce((a, p, i) => { const q = r[(i + 1) % r.length]; return a + p[0] * q[1] - q[0] * p[1]; }, 0) / 2;
  const orient = (r) => (signedArea(r) > 0 ? r.slice().reverse() : r);   // a footprint runs with the building on its left (check_map.py)
  const lineLen = (pts) => pts.reduce((a, p, i) => (i ? a + dist(pts[i - 1], p) : 0), 0);
  const bboxOf = (pts) => { const b = [1e9, 1e9, -1e9, -1e9]; for (const [x, y] of pts) { b[0] = Math.min(b[0], x); b[1] = Math.min(b[1], y); b[2] = Math.max(b[2], x); b[3] = Math.max(b[3], y); } return b; };
  const hit = (bb, v) => !(bb[2] < v[0] || bb[0] > v[2] || bb[3] < v[1] || bb[1] > v[3]);
  function along(pts, p) {   // metres along a line to the point on it nearest p, and how far off it p is
    let best = { s: 0, off: 1e9, i: 0 }, acc = 0;
    for (let i = 0; i < pts.length - 1; i++) { const q = nearestOnSeg(p, pts[i], pts[i + 1]), d = dist(p, q); if (d < best.off) best = { s: acc + dist(pts[i], q), off: d, i, q }; acc += dist(pts[i], pts[i + 1]); }
    return best;
  }
  function pointAlong(pts, s) { let acc = 0; for (let i = 0; i < pts.length - 1; i++) { const L = dist(pts[i], pts[i + 1]); if (acc + L >= s || i === pts.length - 2) { const t = L ? Math.max(0, Math.min(1, (s - acc) / L)) : 0; return [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t, i]; } acc += L; } return [pts[0][0], pts[0][1], 0]; }
  function segsCross(a, b, c, d) { const o = (p, q, r) => (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]); const e = 1e-3, d1 = o(c, d, a), d2 = o(c, d, b), d3 = o(a, b, c), d4 = o(a, b, d); return ((d1 > e && d2 < -e) || (d1 < -e && d2 > e)) && ((d3 > e && d4 < -e) || (d3 < -e && d4 > e)); }
  function polysOverlap(A, B) {
    for (let i = 0; i < A.length; i++) for (let j = 0; j < B.length; j++) if (segsCross(A[i], A[(i + 1) % A.length], B[j], B[(j + 1) % B.length])) return true;
    return A.some((p) => inPoly(p, B) && ringDist(p, B) > 0.15) || B.some((p) => inPoly(p, A) && ringDist(p, A) > 0.15);
  }
  function rectFrom(w, dep, angDeg, cx, cy) {   // a rectangle of an exact size, angle and middle (from the panel)
    const a = angDeg * Math.PI / 180, u = [Math.cos(a), Math.sin(a)], v = [-u[1], u[0]];
    return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([i, j]) => [r2(cx + u[0] * i * w / 2 + v[0] * j * dep / 2), r2(cy + u[1] * i * w / 2 + v[1] * j * dep / 2)]);
  }
  // dress records: the world points of their pieces, a relief grid's box, the frame goods sit in
  const TILE = 100;
  const rowsOf = (t) => (t && Array.isArray(t.rows) && Array.isArray(t.cols) ? t.rows.map((row) => Object.fromEntries(t.cols.map((c, i) => [c, row[i]]))) : []);
  function piecePts(r) {
    const t = r.type === "litter" ? r.pieces : r.type === "people" ? r.spots : r.type === "ground_marks" ? r.potholes : null;
    const P = rowsOf(t).filter((o) => isFinite(o.x) && isFinite(o.y)).map((o) => [o.x, o.y]);
    if (r.type === "ground_marks") for (const u of (r.ruts || [])) if (Array.isArray(u.line)) P.push(...u.line);
    return P;
  }
  function reliefBox(r) { if (!r || r.type !== "relief" || !Array.isArray(r.origin) || !(r.cell > 0) || !(r.cols >= 2) || !(r.rows >= 2)) return null; const [x, y] = r.origin, w = (r.cols - 1) * r.cell, h = (r.rows - 1) * r.cell; return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; }
  function goodsFrame(par, get) {   // docs/MAP-FORMAT.md "Local frames": origin o, x along ux, y along uy (metres)
    if (!par) return null;
    if (par.type === "leanto") { const q = leantoQuad(par, get); if (!q) return null; const L = dist(q[0], q[1]) || 1, ux = [(q[1][0] - q[0][0]) / L, (q[1][1] - q[0][1]) / L]; return { o: q[0], ux, uy: [-ux[1], ux[0]] }; }
    if (!Array.isArray(par.at)) return null;
    const a = (par.turn || 0) * Math.PI / 180; return { o: par.at, ux: [Math.cos(a), Math.sin(a)], uy: [-Math.sin(a), Math.cos(a)] };
  }
  function boxPts(at, w, d, turn) { const a = (turn || 0) * Math.PI / 180, u = [Math.cos(a), Math.sin(a)], v = [-u[1], u[0]]; return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([i, j]) => [at[0] + u[0] * i * w / 2 + v[0] * j * d / 2, at[1] + u[1] * i * w / 2 + v[1] * j * d / 2]); }

  // ------------------------------------------------------------------ the schema (schema/map_schema.json)
  function spec(sp) { const opt = sp.endsWith("?"), t = sp.replace(/\?$/, "").trim(), sp1 = t.indexOf(" "), kind = sp1 < 0 ? t : t.slice(0, sp1), [base, arg] = kind.split(":"); return { base, arg, rng: sp1 < 0 ? "" : t.slice(sp1 + 1), opt }; }
  const fieldsOf = (type) => Object.assign({}, SCHEMA.common, SCHEMA.records[type].fields);
  function defaults(shape) {   // only containers and "none": never a measured or chosen value
    const o = {};
    for (const [k, sp] of Object.entries(shape)) {
      const f = spec(sp); if (f.opt) continue;
      if (f.base === "objs") o[k] = [];
      else if (f.base === "obj") o[k] = defaults(SCHEMA.shapes[f.arg]);
      else if (f.base === "enum" && SCHEMA.enums[f.arg].includes("none")) o[k] = "none";
    }
    return o;
  }
  const GEOM = { road: "centreline", rail: "centreline", station: "area", plot: "outline", building: "footprint", wall: "line", frontage: "line", place: "area", district: "outline" };
  const POINTY = new Set(["stall", "pole", "tree", "vehicle", "furniture", "heap", "person_spot"]);
  function editPts(r) {   // the points a handle edits, and whether they close
    if (!r) return null;
    if (r.type === "road" && Array.isArray(r.centreline)) return { pts: r.centreline, closed: false, set: (q, P) => { q.centreline = P; } };
    if (r.type === "rail" && Array.isArray(r.centreline)) return { pts: r.centreline, closed: false, set: (q, P) => { q.centreline = P; } };
    if (r.type === "station" && Array.isArray(r.area) && r.area[0]) return { pts: r.area[0], closed: true, set: (q, P) => { q.area = [P, ...q.area.slice(1)]; } };
    if ((r.type === "wall" || r.type === "frontage") && Array.isArray(r.line)) return { pts: r.line, closed: false, set: (q, P) => { q.line = P; } };
    if (r.type === "building" && Array.isArray(r.footprint)) return { pts: r.footprint, closed: true, set: (q, P) => { q.footprint = P; } };
    if (r.type === "plot" && Array.isArray(r.outline)) return { pts: r.outline, closed: true, set: (q, P) => { q.outline = P; } };
    if (r.type === "place" && Array.isArray(r.area) && r.area[0]) return { pts: r.area[0], closed: true, set: (q, P) => { q.area = [P, ...q.area.slice(1)]; } };
    if (r.type === "ground" && Array.isArray(r.rings) && r.rings[0]) return { pts: r.rings[0], closed: true, set: (q, P) => { q.rings = [P, ...q.rings.slice(1)]; } };
    return null;
  }
  function wireEnds(r, get = rec) {   // a wire's two ends on the ground plan: its pole, then the other pole or its point on a house
    const a = get(r.from_pole), b = r.to_pole ? get(r.to_pole) : null, e = b ? b.at : r.to_at;
    return a && Array.isArray(a.at) && Array.isArray(e) ? [a.at, e.slice(0, 2)] : null;
  }
  function allPts(r, get = rec) { if (r.type === "wire") return wireEnds(r, get) || []; const e = editPts(r); if (e) return e.pts; if (Array.isArray(r.at)) return [r.at]; const q = leantoQuad(r, get) || reliefBox(r); if (q) return q; const P = piecePts(r); if (P.length) return P; const g = goodsFrame(get(r.of), get); return g ? [g.o] : []; }

  // ------------------------------------------------------------------ moving, turning and relinking a record by its schema
  // Every point a record holds moves (heights kept); a "turn" turns, a lean turns with it; table rows with world x, y move
  // (litter, potholes, people; goods and tree lobes sit in their parent's frame and need nothing). Links in ids are renamed;
  // a link not in ids is dropped, to be set again on the map (it shows as needing a value when it is required).
  const WORLD_T = new Set(["litter_piece", "pothole", "person"]);
  function xform(o, shape, X) {
    for (const [k, sp] of Object.entries(shape)) {
      if (!(k in o) || o[k] === null) continue;
      const f = spec(sp), v = o[k];
      if (f.base === "id") { if (X.ids) { if (X.ids.has(v)) o[k] = X.ids.get(v); else delete o[k]; } }
      else if (f.base === "pt" && k === "lean") o[k] = X.rot(v);
      else if ((f.base === "pt" || f.base === "pt3") && Array.isArray(v)) o[k] = X.f(v);
      else if ((f.base === "line" || f.base === "ring") && Array.isArray(v)) o[k] = v.map(X.f);
      else if (f.base === "rings" && Array.isArray(v)) o[k] = v.map((r) => r.map(X.f));
      else if (f.base === "num" && k === "turn" && X.deg) o[k] = Math.round((((v + X.deg) % 360) + 360) % 360 * 100) / 100;
      else if (f.base === "obj" && v && typeof v === "object") xform(v, SCHEMA.shapes[f.arg], X);
      else if (f.base === "objs" && Array.isArray(v)) v.forEach((x) => xform(x, SCHEMA.shapes[f.arg], X));
      else if (f.base === "table" && v && Array.isArray(v.rows)) {
        const c = (n) => v.cols.indexOf(n), ix = c("x"), iy = c("y"), it = c("turn");
        for (const row of v.rows) {
          if (WORLD_T.has(f.arg) && ix >= 0 && isFinite(row[ix]) && isFinite(row[iy])) { const q = X.f([row[ix], row[iy]]); row[ix] = q[0]; row[iy] = q[1]; }
          else if (f.arg === "lobe" && isFinite(row[ix]) && isFinite(row[iy])) { const q = X.rot([row[ix], row[iy]]); row[ix] = q[0]; row[iy] = q[1]; }
          if ((WORLD_T.has(f.arg) || f.arg === "frond") && it >= 0 && isFinite(row[it]) && X.deg) row[it] = Math.round((((row[it] + X.deg) % 360) + 360) % 360 * 100) / 100;
        }
      }
    }
  }
  function reliefTurned(r, X) {   // a relief grid stays square to the frame: turned, it is sampled again onto a new grid
    const n = r.cols, m = r.rows, c = r.cell, z = (i, j) => (i >= 0 && j >= 0 && i < n && j < m ? r.z_mm[j * n + i] : 0);
    const P = reliefBox(r).map(X.f), b = bboxOf(P), cols = Math.max(2, Math.round((b[2] - b[0]) / c) + 1), rows = Math.max(2, Math.round((b[3] - b[1]) / c) + 1), out = [];
    const a = -X.deg * Math.PI / 180, cs = Math.cos(a), sn = Math.sin(a), O = X.f(r.origin);
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
      const dx = b[0] + i * c - O[0], dy = b[1] + j * c - O[1], u = (dx * cs - dy * sn) / c, w = (dx * sn + dy * cs) / c, i0 = Math.floor(u), j0 = Math.floor(w), fu = u - i0, fw = w - j0;
      out.push(u < -0.01 || w < -0.01 || u > n - 0.99 || w > m - 0.99 ? 0 : Math.round(z(i0, j0) * (1 - fu) * (1 - fw) + z(i0 + 1, j0) * fu * (1 - fw) + z(i0, j0 + 1) * (1 - fu) * fw + z(i0 + 1, j0 + 1) * fu * fw));
    }
    r.origin = [r2(b[0]), r2(b[1])]; r.cols = cols; r.rows = rows; r.z_mm = out;
  }
  function transformed(r, X) {   // a copy of r, moved, turned and relinked
    const q = clone(r);
    if (q.type === "relief" && X.deg && Array.isArray(q.z_mm) && reliefBox(q)) { reliefTurned(q, X); const o = q.origin; delete q.origin; xform(q, fieldsOf(q.type), X); q.origin = o; }
    else xform(q, fieldsOf(q.type), X);
    return q;
  }
  function mover(pivot, at, deg, ids = null) {
    const a = deg * Math.PI / 180, cs = Math.cos(a), sn = Math.sin(a);
    return { deg, ids, f: (p) => { const dx = p[0] - pivot[0], dy = p[1] - pivot[1]; return [r2(at[0] + dx * cs - dy * sn), r2(at[1] + dx * sn + dy * cs), ...p.slice(2)]; }, rot: (v) => [r2(v[0] * cs - v[1] * sn), r2(v[0] * sn + v[1] * cs)] };
  }
  const moveRec = (r, dx, dy) => transformed(r, mover([0, 0], [dx, dy], 0));
  function turnRec(r, deg) {
    const q = clone(r);
    if ("turn" in fieldsOf(q.type) && Array.isArray(q.at)) { q.turn = Math.round(((((q.turn || 0) + deg) % 360) + 360) % 360 * 100) / 100; return q; }
    const e = editPts(q); if (!e || e.pts.length < 2) return null;
    const c = centroid(e.closed ? e.pts : [e.pts[0], e.pts[e.pts.length - 1]]), a = deg * Math.PI / 180, cs = Math.cos(a), sn = Math.sin(a);
    e.set(q, e.pts.map((p) => [r2(c[0] + (p[0] - c[0]) * cs - (p[1] - c[1]) * sn), r2(c[1] + (p[0] - c[0]) * sn + (p[1] - c[1]) * cs), ...p.slice(2)]));
    return q;
  }

  // ------------------------------------------------------------------ the map, as loaded from the server
  const DS = new Map();      // "d15" -> { recs: Map(id -> record), probs: Map(id -> [{field, msg}]), file: [msg] }
  const dOf = new Map();     // record id -> its district
  let started = new Set(), loading = new Set(), cur = null, SERVER = true, lastMsg = "";
  const dId = (n) => "d" + String(n).padStart(2, "0");
  const studyD = (d) => F.districts.find((x) => dId(x.n) === d);
  const dHere = (p) => { const s = V.districtAt(p); return s ? dId(s.n) : null; };
  const rec = (id) => { const d = dOf.get(id); return d && DS.has(d) ? DS.get(d).recs.get(id) : null; };
  const recsOf = (types) => { const out = []; for (const D of DS.values()) for (const r of D.recs.values()) if (!types || types.includes(r.type)) out.push(r); return out; };
  const taken = new Set();   // ids handed out this session (a stamp makes many before any is saved)
  function newId(type) {
    const pre = SCHEMA.records[type].prefix, abc = "abcdefghijklmnopqrstuvwxyz0123456789";
    for (;;) { const b = new Uint8Array(8); crypto.getRandomValues(b); const id = pre + "-" + [...b].map((x) => abc[x % 36]).join(""); if (!dOf.has(id) && !taken.has(id)) { taken.add(id); return id; } }
  }
  function setProblems(d, list) {
    const D = DS.get(d); if (!D) return;
    D.probs = new Map(); D.file = [];
    for (const p of list || []) { if (p.id) { if (!D.probs.has(p.id)) D.probs.set(p.id, []); D.probs.get(p.id).push(p); } else D.file.push(p.where + ": " + p.msg); }
  }
  function setRecords(d, records, problems, tiles) {
    const old = DS.get(d); if (old) for (const id of old.recs.keys()) dOf.delete(id);
    const D = { recs: new Map(), probs: new Map(), file: [], tiles: new Set(tiles || []), got: new Set() }; DS.set(d, D);
    for (const r of records) { D.recs.set(r.id, r); dOf.set(r.id, d); }
    setProblems(d, problems);
  }
  async function api(path, body) {
    try {
      const r = body === undefined ? await fetch(path, { cache: "no-store" }) : await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const j = await r.json(); SERVER = true;
      if (!r.ok) { toast(j.error || "Not saved"); return null; }
      return j;
    } catch (e) { SERVER = false; toast("The board server isn't running (python3 scripts/board_server.py), so nothing was saved"); renderStatus(); return null; }
  }
  async function loadList() { const j = await api("/api/map/list"); if (j) { started = new Set(j.districts); fillPicker(); V.draw(); } }
  async function load(d) {
    if (loading.has(d)) return; loading.add(d);
    const j = await api("/api/map/load?d=" + d); loading.delete(d);
    if (!j) return;
    if (j.exists) setRecords(d, j.records, j.problems, j.tiles); else started.delete(d);
    V.draw(); showPanel();
  }
  async function loadTiles(d, tiles) {   // the dress layer, 100 m tile by tile, only where the view is
    const j = await api("/api/map/tiles?d=" + d + "&t=" + tiles.join(","));
    const D = DS.get(d); if (!j || !D) return;
    for (const r of j.records) { D.recs.set(r.id, r); dOf.set(r.id, d); }
    V.draw();
  }
  function applyChanges(d, changed, removed, problems) {
    const D = DS.get(d); if (!D) return;
    for (const r of changed || []) { D.recs.set(r.id, r); dOf.set(r.id, d); }
    for (const id of removed || []) { D.recs.delete(id); dOf.delete(id); }
    setProblems(d, problems);
  }
  // save whole records (grouped by district); on a refusal the district is loaded again so the board shows what is saved
  async function save(records) {
    const by = new Map();
    for (const r of records) { const d = dOf.get(r.id) || r._d; if (!by.has(d)) by.set(d, []); by.get(d).push(r); }
    let ok = true;
    for (const [d, list] of by) {
      const j = await api("/api/map/save", { d, records: list.map((r) => { const q = { ...r }; delete q._d; return q; }) });
      if (!j) { ok = false; await load(d); continue; }
      const D = DS.get(d);
      for (const r of list) { delete r._d; D.recs.set(r.id, r); dOf.set(r.id, d); }
      setProblems(d, j.problems); lastMsg = "Saved";
    }
    if (sel) sel = rec(sel.id); V.draw(); showPanel(); return ok;
  }
  async function create(r, at, extra = []) {   // a new record in the district under at
    const d = dHere(at);
    if (!d) { toast("That's outside every district"); V.draw(); return false; }
    if (!started.has(d)) { toast(`${d} isn't started: pick it under "Draw in" to start it`); V.draw(); return false; }
    r._d = d;
    const ok = await save([r, ...extra]);
    if (ok) { sel = rec(r.id); showPanel(); V.draw(); }
    return ok;
  }
  async function del(r) {
    const d = dOf.get(r.id);
    const j = await api("/api/map/delete", { d, id: r.id, children: true });   // with the dress records that dress it
    if (!j) return;
    applyChanges(d, [], j.removed, j.problems);
    if (sel && !rec(sel.id)) sel = null; lastMsg = "Deleted" + (j.removed.length > 1 ? ` with ${j.removed.length - 1} dress record${j.removed.length > 2 ? "s" : ""}` : ""); toast(lastMsg); V.draw(); showPanel();
  }
  async function undo() {
    const j = await api("/api/map/undo", {});
    if (!j) return;
    applyChanges(j.d, j.changed, j.removed, j.problems); sel = sel && rec(sel.id); toast("Undone"); lastMsg = "Undone"; V.draw(); showPanel();
  }
  async function start(d) {
    const j = await api("/api/map/start", { d });
    if (!j) return;
    started.add(d); setRecords(d, j.records, j.problems, []); fillPicker(); loadSources(); toast(`Started ${d}: its outline is from the frame study; its name is still to give`); V.draw(); showPanel();
  }

  // ------------------------------------------------------------------ problems: the checker's, and a few the board sees on its own
  const isMissing = (p) => /^missing (field|value)/.test(p.msg);
  function boardProblems(v) {   // a house on a road or on another house, a wall across a road
    const bad = new Map();
    const roads = recsOf(["road"]).filter((r) => Array.isArray(r.centreline) && r.centreline.length > 1 && r.width > 0);
    const bs = recsOf(["building"]).filter((b) => Array.isArray(b.footprint) && b.footprint.length > 2 && hit(bboxOf(b.footprint), v));
    if (V.s < 0.5) return bad;
    const onRoad = (fp, r) => {   // the carriageway (half the width each side of the centreline) reaches into the footprint
      // flat at the road's two ends, round on the outside of its bends, as the check draws it (check_map.py: buffer with
      // cap_style=2), so a lane that stops at a house's wall does not bulge into it (owner, 26 Oct)
      const c = r.centreline, half = r.width / 2 - 0.05;
      if (c.some((p) => inPoly(p, fp))) return true;
      for (let i = 1; i < c.length; i++) {
        const a = c[i - 1], b = c[i], L = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1, n = [-(b[1] - a[1]) / L * half, (b[0] - a[0]) / L * half];
        if (polysOverlap(fp, [[a[0] + n[0], a[1] + n[1]], [b[0] + n[0], b[1] + n[1]], [b[0] - n[0], b[1] - n[1]], [a[0] - n[0], a[1] - n[1]]])) return true;
      }
      for (let i = 1; i < c.length - 1; i++) {   // a bend's round join: a fan on the outside of the turn only
        const a = c[i - 1], m = c[i], b = c[i + 1], a1 = Math.atan2(m[1] - a[1], m[0] - a[0]);
        let d = Math.atan2(b[1] - m[1], b[0] - m[0]) - a1; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI;
        if (Math.abs(d) < 1e-3) continue;
        const s = d > 0 ? -1 : 1, fan = [m];   // a left turn's outside is on the right
        for (let k = 0; k <= 6; k++) { const t = a1 + d * k / 6 + s * Math.PI / 2; fan.push([m[0] + Math.cos(t) * half, m[1] + Math.sin(t) * half]); }
        if (polysOverlap(fp, fan)) return true;
      }
      return false;
    };
    for (const b of bs) {
      for (const r of roads) if (onRoad(b.footprint, r)) { bad.set(b.id, "on the road " + r.id); break; }
      if (!bad.has(b.id)) for (const o of bs) if (o !== b && polysOverlap(b.footprint, o.footprint)) { bad.set(b.id, "overlaps " + o.id); break; }
    }
    // a wall is its line 0.2 m thick, tested against the same carriageway as a house (flat ends; owner, 26 Oct)
    const wallStrip = (a, b) => { const L = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1, n = [-(b[1] - a[1]) / L * 0.1, (b[0] - a[0]) / L * 0.1];
      return [[a[0] + n[0], a[1] + n[1]], [b[0] + n[0], b[1] + n[1]], [b[0] - n[0], b[1] - n[1]], [a[0] - n[0], a[1] - n[1]]]; };
    for (const w of recsOf(["wall"])) if (Array.isArray(w.line) && w.line.length > 1) for (const r of roads) { if (w.line.some((p, i) => i && (r.centreline.some((q, j) => j && segsCross(w.line[i - 1], p, r.centreline[j - 1], q)) || onRoad(wallStrip(w.line[i - 1], p), r)))) { bad.set(w.id, "across the road " + r.id); break; } }
    return bad;
  }
  let boardBad = new Map();
  const probsOf = (r) => { const D = DS.get(dOf.get(r.id)); return (D && D.probs.get(r.id)) || []; };
  function badness(r) {   // "bad" (a real problem), "incomplete" (fields still to set) or ""
    if (boardBad.has(r.id)) return "bad";
    const P = probsOf(r); if (!P.length) return "";
    return P.every(isMissing) ? "incomplete" : "bad";
  }

  // ------------------------------------------------------------------ tools
  const TOOLS = [["select", "Select", "V", "Select, move, turn, delete"], ["street", "Street", "S", "A road, street, lane or path: click points, Enter to finish"], ["building", "Building", "B", "Drag a box"], ["plot", "Plot", "P", "Drag a box"], ["wall", "Wall", "W", "Click points, Enter to finish"], ["gate", "Gate", "G", "Click a wall where the gate starts, then where it ends"], ["leanto", "Lean-to", "L", "Click a building side (or a wall) where it starts, then where it ends"], ["tree", "Tree", "T", "Click to plant"], ["furniture", "Furniture", "F", "Stalls, poles, parked vehicles, furniture, heaps: click to place"], ["place", "Place", "A", "What the game uses a spot for: drag a box"], ["surface", "Surface", "U", "Click a road to give it the surface"], ["frontage", "Frontage", "E", "Click a plot's side that faces a street"], ["stamp", "Stamp", "K", "Copy records (with their dress) from the map or a source and place them"], ["face", "Face", "C", "Click a building's side to dress it: windows, doors, shopfronts, stains, add-ons"], ["goods", "Goods", "O", "Click inside a lean-to, stall, heap or bin to put an item there"], ["ground", "Ground", "D", "Paint a patch of ground: click points, Enter to finish"], ["relief", "Relief", "H", "Drag a box for a bump-and-dip grid; click a cell to raise it, ⌥-click to lower"], ["litter", "Litter", "X", "Click to drop a piece of litter"], ["brush", "Brush", "N", "Brush litter, goods, relief or ground paint: every stroke writes full records (⌥ erases)"], ["person", "Person", "I", "A person spot: where someone does something, and when. Click (drag to face them)"], ["wire", "Wire", "J", "Click a pole, then another pole (a line) or a house side or wall (a drop to the house); Shift keeps going from the last pole"]];
  const KINDS = () => ({
    street: SCHEMA.enums.road_kind.map((k) => [k, k]), building: SCHEMA.enums.house_type.map((k) => [k, k]), plot: SCHEMA.enums.plot_kind.map((k) => [k, k]),
    tree: SCHEMA.enums.tree_kind.map((k) => [k, k]), place: SCHEMA.enums.place_kind.map((k) => [k, k]), surface: SCHEMA.enums.road_surface.map((k) => [k, k]), frontage: SCHEMA.enums.frontage_kind.map((k) => [k, k]),
    goods: [["on the ground", "items"], ["hung", "hung"]].map(([g, t]) => [g, SCHEMA.enums.goods_kind.map((k) => [t + ":" + k, k])]),
    ground: SCHEMA.enums.ground_kind.map((k) => [k, k]), litter: SCHEMA.enums.litter_kind.map((k) => [k, k]), relief: [["0.5", "new grid: 0.5 m cells"], ["0.25", "new grid: 0.25 m cells"], ["1", "new grid: 1 m cells"]],
    brush: [["litter", "litter brush"], ["goods:items", "goods brush (on the ground)"], ["goods:hung", "goods brush (hung)"], ["relief", "relief brush"], ["ground", "ground paint brush"]],
    person: SCHEMA.enums.person_activity.map((k) => [k, k]),
    wire: [["", "kind: line to a pole, service to a house"], ...SCHEMA.enums.wire_kind.map((k) => [k, k])],
    furniture: [["stall", "stall_kind"], ["pole", "pole_kind"], ["vehicle", "vehicle_kind"], ["furniture", "furniture_kind"], ["heap", "heap_kind"]].map(([t, e]) => [t, SCHEMA.enums[e].map((k) => [t + ":" + k, k])]),
  });
  let selRow = null;   // a picked row of a dress table (a goods item, a litter piece): {id, t, i}
  let tool = "select", sel = null, hover = null, ghost = null, drag = null, linePts = [], cursor = null, snapAt = null, firstClick = null;
  let snapReal = true, hoverEdge = null, wireFrom = null;   // wireFrom: the pole a wire being drawn starts at
  let clockOn = false, clockH = 7, wireZ = "";   // wireZ: the height (m) a drop meets the house, as you set it in the panel   // the clock filter: person spots out at clockH bright, the rest faint
  const WALLED = new Set(["wall_gate", "low_wall_bars", "sheet_fence", "breeze_fence", "plank_fence"]);   // frontages whose front is a wall
  try { snapReal = localStorage.getItem("gidi-map-snapreal") !== "0"; wireZ = localStorage.getItem("gidi-map-wirez") || ""; } catch (e) {}
  function outAt(r, h) {   // is a person spot out at hour h? spans with `to` before `from` run past midnight
    return Array.isArray(r.hours) && r.hours.some((s) => s && isFinite(s.from) && isFinite(s.to) && (s.from <= s.to ? h >= s.from && h < s.to : h >= s.from || h < s.to));
  }
  const hhmm = (h) => String(Math.floor(h)).padStart(2, "0") + ":" + (h % 1 ? "30" : "00");
  function setTool(t) {
    if (!SCHEMA) return;
    tool = t; linePts = []; ghost = null; firstClick = null; wireFrom = null; snapAt = null; hoverEdge = null; placing = null; pickBox = null;
    if (t === "stamp") sel = null;
    if (t === "stamp") loadSources().then(() => { if (tool !== "stamp") return; let k = ""; try { k = localStorage.getItem("gidi-map-stampsrc") || ""; } catch (e) {} if (!SRC && k) loadSrc(k); else showPanel(); });
    document.querySelectorAll("#mtools button").forEach((b) => b.classList.toggle("on", b.dataset.tool === t));
    const ks = $("mkind"), K = KINDS()[t];
    ks.innerHTML = !K ? "" : Array.isArray(K[0][1]) ? K.map(([g, L]) => `<optgroup label="${g}">${L.map(([v, l]) => `<option value="${v}">${l}</option>`).join("")}</optgroup>`).join("") : K.map(([v, l]) => `<option value="${v}">${l}</option>`).join("");
    ks.style.display = K ? "" : "none";
    if (t === "brush") { if (![...ks.options].some((o) => o.value === BR.mode)) BR.mode = ks.value; ks.value = BR.mode; }
    $("mwirezl").style.display = t === "wire" ? "" : "none";
    $("msnap").style.display = t === "street" || (t === "select" && sel && sel.type === "road") ? "" : "none";
    V.cv.className = t === "select" ? "" : "place";
    showPanel(); V.draw();
  }

  // snapping: onto the map's own roads first (so streets join on one shared point), then onto the real road line (a helper)
  function snapPt(p, skip, ev) {
    if (ev && ev.shiftKey) return { p };
    const tol = 10 / V.s; let best = null, bd = tol;
    for (const r of recsOf(["road"])) { if (r === skip || !Array.isArray(r.centreline)) continue; for (const q of r.centreline) { const d = dist(p, q); if (d < bd) { bd = d; best = { p: q.slice(0, 2), on: r, vertex: true }; } } }
    if (best) return best;
    bd = 8 / V.s;
    for (const r of recsOf(["road"])) { if (r === skip || !Array.isArray(r.centreline)) continue; const a = along(r.centreline, p); if (a.off < bd) { bd = a.off; best = { p: [r2(a.q[0]), r2(a.q[1])], on: r, seg: a.i }; } }
    if (best) return best;
    if (snapReal && (tool === "street" || (drag && drag.obj && drag.obj.type === "road"))) {
      bd = 10 / V.s; const b = [p[0] - bd, p[1] - bd, p[0] + bd, p[1] + bd];
      for (const r of F.roads) { if (r.k === "rail" || !hit(r.bb, b)) continue; const a = along(r.p, p); if (a.off < bd) { bd = a.off; best = { p: [r2(a.q[0]), r2(a.q[1])], real: true }; } }
      if (best) return best;
    }
    return { p: [r2(p[0]), r2(p[1])] };
  }
  function cornerSnap(p, skip, ev) {   // building, plot and wall corners snap to each other's corners
    if (ev && ev.shiftKey) return [r2(p[0]), r2(p[1])];
    let best = null, bd = 7 / V.s;
    for (const r of recsOf(["building", "plot", "wall", "frontage"])) { if (r === skip) continue; const e = editPts(r); if (!e) continue; for (const q of e.pts) { const d = dist(p, q); if (d < bd) { bd = d; best = q.slice(0, 2); } } }
    return best || [r2(p[0]), r2(p[1])];
  }
  function withJunction(sn, pts) {   // a point snapped onto the middle of another road becomes a point of that road too
    if (!sn.on || sn.vertex || sn.seg === undefined) return null;
    const r = clone(sn.on), c = r.centreline;
    if (c.some((q) => dist(q, sn.p) < 0.005)) return null;
    c.splice(sn.seg + 1, 0, sn.p.slice()); return r;
  }

  // ------------------------------------------------------------------ picking
  function leantoQuad(r, get = rec) {
    if (!r || r.type !== "leanto") return null;
    const host = get(r.against); if (!host || !(r.u1 > r.u0)) return null;
    let a, b;
    if (host.type === "building" && Array.isArray(host.footprint) && Number.isInteger(r.face) && r.face < host.footprint.length) {
      const fp = host.footprint, p = fp[r.face], q = fp[(r.face + 1) % fp.length], L = dist(p, q) || 1, u = [(q[0] - p[0]) / L, (q[1] - p[1]) / L];
      a = [p[0] + u[0] * r.u0, p[1] + u[1] * r.u0]; b = [p[0] + u[0] * r.u1, p[1] + u[1] * r.u1];
    } else if (Array.isArray(host.line)) { a = pointAlong(host.line, r.u0); b = pointAlong(host.line, r.u1); }
    else return null;
    const L = dist(a, b) || 1, n = [-(b[1] - a[1]) / L, (b[0] - a[0]) / L], dep = r.depth > 0 ? r.depth : 1;   // out to the right: away from the building
    return [[a[0], a[1]], [b[0], b[1]], [b[0] + n[0] * dep, b[1] + n[1] * dep], [a[0] + n[0] * dep, a[1] + n[1] * dep]];
  }
  const VSIZE = { danfo: [4.8, 2.0], keke: [2.8, 1.3], okada: [2.1, 0.8], saloon: [4.6, 1.8], suv: [4.8, 1.9], pickup: [5.2, 1.9], lorry: [8.6, 2.5], container: [17.2, 2.5], tanker: [11.5, 2.5], bus: [11, 2.6], wreck: [4.6, 1.8] };   // drawing sizes only
  function thingPts(r) {
    if (!Array.isArray(r.at)) return null;
    if (r.type === "vehicle") { const z = VSIZE[r.kind] || [4, 2]; return boxPts(r.at, z[0], z[1], r.turn); }
    if (r.type === "stall") return boxPts(r.at, r.w > 0 ? r.w : 1, r.d > 0 ? r.d : 1, r.turn);
    if (r.type === "furniture") return boxPts(r.at, r.length > 0 ? r.length : 0.8, 0.6, r.turn);
    return null;
  }
  const thingR = (r) => r.type === "tree" ? (r.kind === "palm" ? 2.5 : r.kind === "shrub" ? 1 : 3.5) : r.type === "heap" ? (r.r > 0 ? r.r : 1) : r.type === "person_spot" ? 0.35 : 0.3;
  const MAPW = { list: (types) => recsOf(types), get: (id) => rec(id) };
  function pick(p, W = MAPW) {   // the record under p: small things first, then lean-tos, buildings, the ground, lines, roads, plots, places
    const tol = Math.max(0.5, 7 / V.s), L = W.list;
    let best = null, bd = tol;
    for (const r of L([...POINTY])) { if (!Array.isArray(r.at)) continue; const q = thingPts(r); const d = q && inPoly(p, q) ? 0 : dist(p, r.at) - (r.type === "tree" || r.type === "heap" ? Math.min(thingR(r), 1.2) : 0); if (d < bd) { bd = d; best = r; } }
    for (const r of L(["litter", "people", "ground_marks"])) for (const q of piecePts(r)) { const d = dist(p, q); if (d < bd) { bd = d; best = r; } }
    for (const r of L(["wire"])) { const E = wireEnds(r, W.get); if (!E) continue; const d = lineDist(p, E) + 0.1; if (d < bd) { bd = d; best = r; } }   // overhead, so before the houses under it
    for (const r of L(["goods"])) { const g = goodsFrame(W.get(r.of), W.get); if (!g) continue; for (const o of [...rowsOf(r.items), ...rowsOf(r.hung)]) { if (![o.x, o.y].every(isFinite)) continue; const d = dist(p, [g.o[0] + g.ux[0] * o.x + g.uy[0] * o.y, g.o[1] + g.ux[1] * o.x + g.uy[1] * o.y]); if (d < bd) { bd = d; best = r; } } }
    if (best) return best;
    for (const r of L(["leanto"])) { const q = leantoQuad(r, W.get); if (q && inPoly(p, q)) return r; }
    const bs = L(["building"]).filter((b) => Array.isArray(b.footprint) && b.footprint.length > 2 && inPoly(p, b.footprint));
    if (bs.length) return bs.sort((a, b) => Math.abs(signedArea(a.footprint)) - Math.abs(signedArea(b.footprint)))[0];
    const gs = L(["ground"]).filter((r) => Array.isArray(r.rings) && r.rings.some((g) => Array.isArray(g) && g.length > 2 && inPoly(p, g)));
    if (gs.length) return gs.sort((a, b) => (b.order || 0) - (a.order || 0))[0];
    bd = Math.max(0.4, 6 / V.s);
    for (const r of L(["wall", "frontage"])) { if (!Array.isArray(r.line)) continue; const d = lineDist(p, r.line); if (d < bd) { bd = d; best = r; } }
    if (best) return best;
    let rd = 1e9;
    for (const r of L(["road"])) { if (!Array.isArray(r.centreline)) continue; const d = lineDist(p, r.centreline); if (d < Math.max((r.width || 0) / 2, 6 / V.s) && d < rd) { rd = d; best = r; } }
    if (best) return best;
    const pl = L(["plot"]).filter((r) => Array.isArray(r.outline) && r.outline.length > 2 && inPoly(p, r.outline));
    if (pl.length) return pl.sort((a, b) => Math.abs(signedArea(a.outline)) - Math.abs(signedArea(b.outline)))[0];
    return L(["place"]).find((r) => Array.isArray(r.area) && r.area.some((ring) => ring.length > 2 && inPoly(p, ring))) || L(["relief"]).find((r) => reliefBox(r) && inPoly(p, reliefBox(r))) || null;
  }
  function plotEdgeAt(p) {   // the plot side under p, for a frontage
    const tol = Math.max(0.4, 8 / V.s); let best = null;
    for (const r of recsOf(["plot"])) { const o = r.outline; if (!Array.isArray(o) || o.length < 3) continue; for (let i = 0; i < o.length; i++) { const d = segDist(p, o[i], o[(i + 1) % o.length]); if (d < tol && (!best || d < best.off)) best = { r, i, a: o[i], b: o[(i + 1) % o.length], off: d }; } }
    return best;
  }
  // the rows of dress tables, one by one: a goods item (in its parent's frame), a litter piece, a person spot, a pothole
  const PIECE_T = { goods: ["items", "hung"], litter: ["pieces"], people: ["spots"], ground_marks: ["potholes"] };
  function pieceXY(r, o, get = rec) {
    if (!o || ![o.x, o.y].every(isFinite)) return null;
    if (r.type !== "goods") return [o.x, o.y];
    const g = goodsFrame(get(r.of), get); return g ? [g.o[0] + g.ux[0] * o.x + g.uy[0] * o.y, g.o[1] + g.ux[1] * o.x + g.uy[1] * o.y] : null;
  }
  function pieceAt(p, types = Object.keys(PIECE_T)) {   // the row under p: {r, t, i}
    const tol = Math.max(0.15, 6 / V.s); let best = null, bd = tol;
    for (const r of recsOf(types)) for (const t of PIECE_T[r.type]) rowsOf(r[t]).forEach((o, i) => { const q = pieceXY(r, o); if (q && dist(p, q) < bd) { bd = dist(p, q); best = { r, t, i }; } });
    return best;
  }
  function toLocal(r, p) {   // a map point as a row's x, y: world metres, or the goods parent's frame
    if (r.type !== "goods") return [r2(p[0]), r2(p[1])];
    const g = goodsFrame(rec(r.of), rec); if (!g) return null; const dx = p[0] - g.o[0], dy = p[1] - g.o[1];
    return [r2(dx * g.ux[0] + dy * g.ux[1]), r2(dx * g.uy[0] + dy * g.uy[1])];
  }
  function goodsHostAt(p) {   // the lean-to, stall, heap or bin under p
    for (const r of recsOf(["stall", "furniture"])) { const q = thingPts(r); if (q && inPoly(p, q)) return r; }
    for (const r of recsOf(["heap"])) if (Array.isArray(r.at) && dist(p, r.at) < thingR(r)) return r;
    for (const r of recsOf(["leanto"])) { const q = leantoQuad(r); if (q && inPoly(p, q)) return r; }
    return null;
  }
  const rowSel = () => (selRow && sel && selRow.id === sel.id && sel[selRow.t] && rowsOf(sel[selRow.t])[selRow.i] ? selRow : null);
  function addPiece(p) {   // Goods and Litter: one more row, at p; like the picked row in every other value, or unset
    const tt = tool, [t, kind] = tt === "goods" ? $("mkind").value.split(":") : ["pieces", $("mkind").value];
    let r, host = null;
    if (tt === "goods") { host = goodsHostAt(p); if (!host) { toast("Click inside a lean-to, stall, heap or bin"); return; } r = recsOf(["goods"]).find((g) => g.of === host.id); }
    else r = sel && sel.type === "litter" ? sel : recsOf(["litter"]).find((l) => piecePts(l).some((q) => dist(q, p) < 5));
    if (r) r = clone(r);
    else {
      r = { id: newId(tt), type: tt }; if (host) r.of = host.id;
      for (const [k, sp] of Object.entries(SCHEMA.records[tt].fields)) { const f = spec(sp); if (f.base === "table") r[k] = { cols: SCHEMA.tables[f.arg].map(([c]) => c), rows: [] }; }   // empty tables: containers only
      r._d = host ? dOf.get(host.id) : dHere(p);
      if (!r._d || !started.has(r._d)) { toast(r._d ? `${r._d} isn't started: pick it under "Draw in" to start it` : "That's outside every district"); return; }
    }
    const xy = toLocal(r, p); if (!xy) return;
    const rs = rowSel(), like = rs && sel.type === tt ? rowsOf(sel[rs.t])[rs.i] : null, o = {};
    for (const c of r[t].cols) o[c] = like && c !== "x" && c !== "y" ? like[c] : null;
    o.kind = kind; o.x = xy[0]; o.y = xy[1];
    r[t].rows.push(r[t].cols.map((c) => o[c])); const i = r[t].rows.length - 1;
    save([r]).then((ok) => { if (ok) { sel = rec(r.id); selRow = { id: r.id, t, i }; showPanel(); V.draw(); } });
  }
  function openFace(b, i) {
    if (!b || b.type !== "building" || !window.FACEEDIT) return;
    sel = b; showPanel(); V.draw();
    window.FACEEDIT.open({ SCHEMA, rec, recsOf, save, newId, toast, undo, dOf, closed: () => { sel = sel && rec(sel.id); showPanel(); V.draw(); } }, b, i);
  }
  function handleAt(p) {
    const e = tool === "select" && editPts(sel); if (!e) return null;
    const P = e.pts, n = P.length, near = (q, px) => { const S = V.toS(q), T = V.toS(p); return Math.hypot(S[0] - T[0], S[1] - T[1]) < px; };
    for (let i = 0; i < n; i++) if (near(P[i], 8)) return { i, mid: false };
    for (let i = 0; i < (e.closed ? n : n - 1); i++) { const a = P[i], b = P[(i + 1) % n]; if (near([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], 7)) return { i, mid: true }; }
    return null;
  }
  function edgeAt(p) {   // the building side or wall line under p, for gates and lean-tos
    const tol = Math.max(0.4, 8 / V.s);
    let best = null;
    for (const b of recsOf(["building"])) { const fp = b.footprint; if (!Array.isArray(fp) || fp.length < 3) continue; for (let i = 0; i < fp.length; i++) { const q = fp[(i + 1) % fp.length], np = nearestOnSeg(p, fp[i], q), d = dist(p, np); if (d < tol && (!best || d < best.off)) best = { r: b, face: i, u: r2(dist(fp[i], np)), off: d, len: dist(fp[i], q) }; } }
    for (const w of recsOf(["wall", "frontage"])) { if (!Array.isArray(w.line)) continue; const a = along(w.line, p); if (a.off < tol && (!best || a.off < best.off)) best = { r: w, u: r2(a.s), off: a.off, len: lineLen(w.line) }; }
    return best;
  }

  // ------------------------------------------------------------------ stamps (docs/MAP-FORMAT.md §3)
  // Copy a record, or a group, from a source (the map, the worked example, a converted test spot under map-stamps/) and
  // place it: full values, new ids, links inside the group kept, a "from" note. Never a live link to the source.
  let SOURCES = [], SRC = null, srcKey = "", picked = [], placing = null, stampDeg = 0, pickBox = null;
  const srcW = () => ({ list: (types) => (SRC ? [...SRC.recs.values()].filter((r) => r.type !== "district" && (!types || types.includes(r.type))) : []), get: (id) => (SRC ? SRC.recs.get(id) || null : null) });
  async function loadSources() { const j = await api("/api/map/sources"); if (j) SOURCES = j.sources; }
  async function loadSrc(key) {
    srcKey = key; picked = []; placing = null; SRC = null;
    try { localStorage.setItem("gidi-map-stampsrc", key); } catch (e) {}
    if (!key) { showPanel(); V.draw(); return; }
    const [src, d] = key.split("|"), j = await api(`/api/map/source?src=${encodeURIComponent(src)}&d=${d}`);
    if (j && srcKey === key) SRC = { src, d, recs: new Map(j.records.map((r) => [r.id, r])) };
    showPanel(); V.draw();
  }
  function groupOf(ids) {   // the picked records and what hangs on them: dress (of), lean-tos (against), wires (from_pole)
    const W = srcW(), all = W.list(null), out = new Map(), q = [...ids];
    while (q.length) { const id = q.pop(); if (out.has(id)) continue; const r = W.get(id); if (!r) continue; out.set(id, r); for (const c of all) if (!out.has(c.id) && (c.of === id || c.against === id || c.from_pole === id || c.parent === id)) q.push(c.id); }
    return [...out.values()];
  }
  function rootOf(id) {   // a lean-to or a dress record has no place of its own: copy what it stands on, with it
    const W = srcW(), seen = new Set(); let r = W.get(id);
    while (r && !seen.has(r.id)) { seen.add(r.id); const up = W.get(r.against || r.of || r.parent); if (!up) break; r = up; }
    return r ? r.id : id;
  }
  function groupPts(G) { const W = srcW(), P = []; for (const r of G) P.push(...allPts(r, W.get).map((q) => q.slice(0, 2))); return P; }
  function startPlacing() {
    const G = groupOf(picked); if (!G.length) return;
    const P = groupPts(G); if (!P.length) { toast("Nothing in that group has a place on the map"); return; }
    const b = bboxOf(P); placing = { G, pivot: [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2] }; stampDeg = 0;
    toast(`Placing ${G.length} record${G.length > 1 ? "s" : ""}: click to put a copy down, R or [ ] to turn, Esc to stop`); showPanel(); V.draw();
  }
  function stampCopies(at) {   // the group, moved to at and turned, with new ids
    const { G, pivot } = placing, ids = new Map(G.map((r) => [r.id, newId(r.type)])), X = mover(pivot, at, stampDeg, ids), day = new Date().toISOString().slice(0, 10);
    const spot = SRC.src === "map" ? "map/" + SRC.d : SRC.src + "/" + SRC.d;
    return G.map((r) => { const q = transformed(r, X); q.id = ids.get(r.id); q.from = { spot, record: r.id, date: day }; if (r.from && r.from.spot) q.from.note = `it came there from ${r.from.spot} ${r.from.record}`; return q; });
  }
  async function placeStamp(at) {
    const d = dHere(at);
    if (!d || !started.has(d)) { toast(d ? `${d} isn't started: pick it under "Draw in" to start it` : "That's outside every district"); return; }
    const C = stampCopies(at);
    for (const b of C) if (b.type === "building" && !b.plot && Array.isArray(b.footprint)) { const pl = recsOf(["plot"]).find((q) => Array.isArray(q.outline) && inPoly(centroid(b.footprint), q.outline)); if (pl) b.plot = pl.id; }   // the plot it now stands in
    for (const r of C) r._d = d;
    if (await save(C)) { lastMsg = `Stamped ${C.length} record${C.length > 1 ? "s" : ""}`; toast(lastMsg + ` in ${d}`); }
  }
  function drawRec(ctx, r, get, px, col, fill) {   // a record's outline, plainly: the stamp source and the copy being placed
    ctx.strokeStyle = col; ctx.lineWidth = 1.5 * px;
    const e = editPts(r), q = thingPts(r) || leantoQuad(r, get) || reliefBox(r);
    if (r.type === "road" && e) { path(ctx, e.pts); ctx.lineCap = "butt"; ctx.lineWidth = Math.max(r.width || 0, 3 * px); ctx.globalAlpha = 0.35; ctx.stroke(); ctx.globalAlpha = 1; return; }
    if (r.type === "place") return;
    const P = e ? e.pts : q;
    if (P && P.length > 1) { path(ctx, P, !e || e.closed); if (fill && (!e || e.closed)) { ctx.fillStyle = fill; ctx.fill(); } ctx.stroke(); return; }
    if (Array.isArray(r.at)) { ctx.beginPath(); ctx.arc(r.at[0], r.at[1], Math.max(thingR(r), 3 * px), 0, 7); ctx.stroke(); return; }
    for (const c of piecePts(r)) { ctx.beginPath(); ctx.arc(c[0], c[1], Math.max(0.1, 1.5 * px), 0, 7); ctx.fillStyle = col; ctx.fill(); }
  }
  function drawStamp(ctx, v, px) {
    if (tool !== "stamp" || !SRC) return;
    const W = srcW(), PUR = "#a24bd6";
    if (SRC.src !== "map") for (const r of W.list(null)) { const P = allPts(r, W.get); if (P.length && hit(bboxOf(P), v)) drawRec(ctx, r, W.get, px, "rgba(162,75,214,.75)"); }
    for (const r of groupOf(picked)) drawRec(ctx, r, W.get, px * 2, PUR, "rgba(162,75,214,.25)");
    if (pickBox && pickBox.b) { path(ctx, [pickBox.a, [pickBox.b[0], pickBox.a[1]], pickBox.b, [pickBox.a[0], pickBox.b[1]]], true); ctx.strokeStyle = PUR; ctx.lineWidth = px; ctx.setLineDash([4 * px, 3 * px]); ctx.stroke(); ctx.setLineDash([]); }
    if (placing && cursor) {
      const X = mover(placing.pivot, cursor, stampDeg), G = placing.G.map((r) => transformed(r, X)), M = new Map(G.map((r) => [r.id, r])), get = (id) => M.get(id) || null;
      for (const r of G) drawRec(ctx, r, get, px * 1.5, PUR, "rgba(162,75,214,.3)");
    }
  }

  // ------------------------------------------------------------------ brushes (decisions: "The map format's four calls", "One ground truth")
  // A stroke writes full records: the same table rows the one-by-one tools write (a litter piece, a goods item), a relief
  // grid's cells, a ground patch's rings, every value written out. No seed, no density, nothing the kit has to expand.
  // Chance is used only here, while brushing, to pick where each piece lies and the values the panel sets to "random";
  // a column left "unset" stays unset (amber). A stroke is one save, so one undo takes the whole stroke back.
  const BR = { mode: "litter", size: 1.5, spacing: 0.4, erase: false, scatter: { litter: "clumps", goods: "even" }, pull: { litter: 0.7, goods: 0 },
    cols: { litter_piece: { kind: { m: "mix" }, colour: { m: "mix" }, z: { m: "value", v: 0 }, turn: { m: "range", a: 0, b: 360 }, tilt: { m: "range", a: -10, b: 10 }, w: { m: "mix" }, d: { m: "mix" }, h: { m: "mix" }, age: { m: "mix" }, buried: { m: "mix" } } },
    relief: { op: "raise", mm: 20 }, ground: { kind: "", colour: "", broken: 0.5 } };
  try {   // the last brush settings, kept per board (a convenience: the map holds only what the strokes wrote)
    const o = JSON.parse(localStorage.getItem("gidi-map-brush") || "{}");
    if (o && typeof o === "object") for (const [k, v] of Object.entries(o)) { if (k === "cols" && v && typeof v === "object") { for (const [tb, C] of Object.entries(v)) BR.cols[tb] = Object.assign(BR.cols[tb] || {}, C); } else if (BR[k] && typeof BR[k] === "object" && v && typeof v === "object") Object.assign(BR[k], v); else if (k in BR) BR[k] = v; }
  } catch (e) {}
  const saveBR = () => { try { localStorage.setItem("gidi-map-brush", JSON.stringify(BR)); } catch (e) {} };
  const BR_T = { litter: "litter_piece", "goods:items": "item", "goods:hung": "item" };   // the table each brush writes rows of
  const famOf = (mode) => (mode === "litter" ? "litter" : mode.startsWith("goods") ? "goods" : null);
  let stroke = null, brAlt = false;
  const maker = (tb, c) => (BR.cols[tb] && BR.cols[tb][c]) || { m: "unset" };
  // "natural mix" (litter only): sizes mostly small, some medium, a few big; ages fresh, weathered and old, the old ones
  // often part buried. Each is picked once per piece, at stroke time, and every value is written into its row.
  const LIT_SIZE = { sachet: [0.12, 0.07, 0.01], bag: [0.3, 0.25, 0.12], bottle: [0.24, 0.07, 0.07], pack: [0.16, 0.1, 0.04], can: [0.12, 0.066, 0.066], husk: [0.18, 0.12, 0.1], paper: [0.21, 0.15, 0.005], rag: [0.4, 0.3, 0.04], tyre: [0.6, 0.6, 0.18] };   // w, d, h of a usual one, m
  // the street mix (the old kit's litter list, deleted 25 Oct with that kit): colour, kind, how common; paper, rags and tyres only when picked
  const LIT_MIX = [["#e8f0f4", "sachet", 5], ["#9ccbe8", "sachet", 2], ["#1c1c1c", "bag", 3], ["#1e6fd0", "bag", 1], ["#d32f2f", "bag", 1], ["#cfe3d6", "bottle", 2], ["#ffffff", "pack", 1.5], ["#c0c0c0", "can", 1], ["#d9b85a", "husk", 1]];
  const LIT_COL = { paper: ["#d8d4cc", "#c9c3b5", "#e8e6e0", "#c8b48a"], rag: ["#c62828", "#f9a825", "#1f6fb8", "#2e9a46", "#e8dcc0", "#3b2a1a"], tyre: ["#1c1c1c"] };
  function fromMix(L) { let u = Math.random() * L.reduce((a, x) => a + x[2], 0); for (const x of L) { u -= x[2]; if (u <= 0) return x; } return L[L.length - 1]; }
  const RIGID = new Set(["bottle", "can", "tyre"]);   // these come in fewer sizes
  const MIXABLE = new Set(["kind", "colour", "w", "d", "h", "age", "buried"]);
  const rnd = (a, b) => a + Math.random() * (b - a);
  const r3 = (v) => Math.round(v * 1000) / 1000;
  function pieceCtx(tb) {   // one piece's kind, size class and age, so its columns agree with each other
    const P = { kind: maker(tb, "kind").m === "mix" ? null : makeVal(tb, "kind", "enum:litter_kind") };
    if (maker(tb, "kind").m === "mix") { const x = fromMix(LIT_MIX); P.kind = x[1]; P.colour = x[0]; }
    const u = Math.random(); let k = u < 0.72 ? rnd(0.6, 1) : u < 0.93 ? rnd(1, 1.7) : rnd(1.8, 3);
    if (RIGID.has(P.kind)) k = 1 + (k - 1) * 0.35;
    P.k = k;
    const a = Math.random();
    if (a < 0.3) { P.age = r2(rnd(0, 0.2)); P.buried = 0; }
    else if (a < 0.7) { P.age = r2(rnd(0.3, 0.65)); P.buried = Math.random() < 0.3 ? r2(rnd(0.05, 0.25)) : 0; }
    else { P.age = r2(rnd(0.7, 1)); P.buried = Math.random() < 0.7 ? r2(rnd(0.2, 0.85)) : 0; }
    return P;
  }
  function makeVal(tb, c, sp, P) {   // one piece's value for a column: unset (null), the value, a random one between two, one of a list, or the natural mix
    const M = maker(tb, c), f = spec(sp);
    if (M.m === "value" && M.v !== undefined && M.v !== null && M.v !== "") return M.v;
    if (M.m === "range" && isFinite(M.a) && isFinite(M.b)) { const v = M.a + Math.random() * (M.b - M.a); return f.base === "int" ? Math.round(v) : r2(v); }
    if (M.m === "pick" && Array.isArray(M.list) && M.list.length) return M.list[Math.floor(Math.random() * M.list.length)];
    if (M.m === "mix" && P && tb === "litter_piece") {
      if (c === "age" || c === "buried") return P[c];
      if (c === "colour") { if (P.colour) return P.colour; const L = LIT_MIX.filter((x) => x[1] === P.kind); return L.length ? fromMix(L)[0] : LIT_COL[P.kind] ? LIT_COL[P.kind][Math.floor(Math.random() * LIT_COL[P.kind].length)] : null; }
      const i = ["w", "d", "h"].indexOf(c); if (i < 0) return null;
      const base = (LIT_SIZE[P.kind] || [0.2, 0.15, 0.05])[i]; return Math.max(0.001, r3(base * P.k * rnd(0.9, 1.1)));
    }
    return null;
  }
  function kindFilter(tb) { const M = maker(tb, "kind"); return M.m === "value" && M.v ? [M.v] : M.m === "pick" && M.list && M.list.length ? M.list : null; }   // what the eraser takes (every kind when none is chosen)
  function hostShape(h) {   // goods lie inside their lean-to, stall, heap or bin
    if (h.type === "heap") return (p) => dist(p, h.at) <= thingR(h);
    const q = h.type === "leanto" ? leantoQuad(h) : thingPts(h); return q ? (p) => inPoly(p, q) : () => false;
  }
  function brushDown(ev, p) {
    const mode = BR.mode, d = dHere(p), erase = BR.erase || ev.altKey;
    const S = { mode, erase, d, dd: d, last: p, path: [p], touched: new Map(), made: [], cells: new Map(), n: 0 };   // touched: id -> its record before the stroke
    if (!d || !started.has(d) || !DS.has(d)) { toast(d ? `${d} isn't started: pick it under "Draw in" to start it` : "That's outside every district"); return; }
    if (mode === "ground" && erase) { toast("The ground brush has no eraser: pick a patch with Select and delete it, or drag its corners"); return; }
    if (mode === "relief" && !recsOf(["relief"]).some((r) => dOf.get(r.id) === d && reliefBox(r) && inPoly(p, reliefBox(r)))) { toast("Start on a relief grid: drag a box with Relief (H) first, then brush it"); return; }
    if ((mode === "litter" || mode.startsWith("goods")) && !erase) {
      const [rt, t] = mode === "litter" ? ["litter", "pieces"] : ["goods", mode.split(":")[1]];
      let r, host = null;
      if (rt === "goods") { host = goodsHostAt(p); if (!host) { toast("Start the stroke inside a lean-to, stall, heap or bin"); return; } r = recsOf(["goods"]).find((g) => g.of === host.id); S.dd = dOf.get(host.id); }
      else r = sel && sel.type === "litter" && dOf.get(sel.id) === d ? sel : recsOf(["litter"]).find((l) => dOf.get(l.id) === d && piecePts(l).some((q) => dist(q, p) < 5));
      if (r) S.touched.set(r.id, clone(r));
      else {   // a new record, shown while brushing and saved at the end
        r = { id: newId(rt), type: rt }; if (host) r.of = host.id;
        for (const [k, sp] of Object.entries(SCHEMA.records[rt].fields)) { const f = spec(sp); if (f.base === "table") r[k] = { cols: SCHEMA.tables[f.arg].map(([c]) => c), rows: [] }; }
        DS.get(S.dd).recs.set(r.id, r); dOf.set(r.id, S.dd); S.made.push(r.id);
      }
      const fam = famOf(mode);
      Object.assign(S, { r, t, tb: BR_T[mode], fam, inside: host ? hostShape(host) : () => true, pts: rowsOf(r[t]).map((o) => pieceXY(r, o)).filter(Boolean),
        clumps: BR.scatter[fam] === "clumps", pull: Math.max(0, Math.min(1, +BR.pull[fam] || 0)), edges: edgesFor(d, host), roofs: fam === "litter" ? roofsIn(d) : [] });
    }
    stroke = S; dab(p, 0); V.draw();
  }
  // Where pieces land. "Clumps" (litter's default) goes along the stroke in spells: a clump (a few tight heaps, dense in the
  // middle), a thin trail (a piece now and then), an empty gap; the spell lengths are thrown as the brush moves. "Even" keeps
  // darts where no piece lies closer than the spacing. The pull moves a share of the pieces up against the nearest edge.
  function edgesFor(d, host) {   // the lines rubbish collects against: kerbs, the foot of walls and houses, stall and lean-to sides, poles
    if (host) { const q = host.type === "leanto" ? leantoQuad(host) : thingPts(host); return q ? q.map((a, i) => [a, q[(i + 1) % q.length]]) : []; }
    const E = [], mine = (r) => dOf.get(r.id) === d, ring = (q) => q.forEach((a, i) => E.push([a, q[(i + 1) % q.length]]));
    for (const r of recsOf(["road"])) if (mine(r) && Array.isArray(r.centreline) && r.width > 0) {
      const C = r.centreline, h = r.width / 2;
      for (let i = 0; i < C.length - 1; i++) { const a = C[i], b = C[i + 1], L = dist(a, b) || 1, n = [-(b[1] - a[1]) / L * h, (b[0] - a[0]) / L * h]; E.push([[a[0] + n[0], a[1] + n[1]], [b[0] + n[0], b[1] + n[1]]], [[a[0] - n[0], a[1] - n[1]], [b[0] - n[0], b[1] - n[1]]]); }
    }
    for (const r of recsOf(["building"])) if (mine(r) && Array.isArray(r.footprint) && r.footprint.length > 2) ring(r.footprint);
    for (const r of recsOf(["wall", "frontage"])) if (mine(r) && Array.isArray(r.line)) for (let i = 0; i < r.line.length - 1; i++) E.push([r.line[i], r.line[i + 1]]);
    for (const r of recsOf(["leanto", "stall", "furniture", "vehicle"])) { if (!mine(r)) continue; const q = r.type === "leanto" ? leantoQuad(r) : thingPts(r); if (q) ring(q); }
    for (const r of recsOf(["pole", "tree", "heap"])) if (mine(r) && Array.isArray(r.at)) E.push([r.at, r.at]);
    return E;
  }
  const roofsIn = (d) => recsOf(["building"]).filter((r) => dOf.get(r.id) === d && Array.isArray(r.footprint) && r.footprint.length > 2).map((r) => ({ fp: r.footprint, bb: bboxOf(r.footprint) }));
  function pulled(q, R) {   // up against the nearest edge within reach, most pieces hard against it, a few a little off
    let best = null, bd = R + 1;
    for (const [a, b] of stroke.edges) { if (Math.min(a[0], b[0]) - bd > q[0] || Math.max(a[0], b[0]) + bd < q[0] || Math.min(a[1], b[1]) - bd > q[1] || Math.max(a[1], b[1]) + bd < q[1]) continue; const e = nearestOnSeg(q, a, b), dd = dist(q, e); if (dd < bd) { bd = dd; best = e; } }
    if (!best || bd < 1e-4) return q;
    const t = 0.03 + bd * 0.35 * Math.random() ** 2;
    return [best[0] + (q[0] - best[0]) / bd * t, best[1] + (q[1] - best[1]) / bd * t];
  }
  const gauss = () => Math.sqrt(-2 * Math.log(1 - Math.random())) * Math.cos(2 * Math.PI * Math.random());
  function putPiece(q, minD) {   // one row at q, if it lands where it may
    const S = stroke;
    if (S.pull > 0 && Math.random() < S.pull) q = pulled(q, Math.max(0.05, +BR.size || 1));
    if (!S.inside(q) || S.roofs.some((b) => q[0] >= b.bb[0] && q[0] <= b.bb[2] && q[1] >= b.bb[1] && q[1] <= b.bb[3] && inPoly(q, b.fp))) return false;
    for (const o of S.pts) if (Math.abs(o[0] - q[0]) < minD && Math.abs(o[1] - q[1]) < minD && dist(o, q) < minD) return false;
    const xy = toLocal(S.r, q); if (!xy) return false;
    const tab = S.r[S.t], T = S.T || (S.T = new Map(SCHEMA.tables[S.tb])), P = S.tb === "litter_piece" ? pieceCtx(S.tb) : null;
    tab.rows.push(tab.cols.map((cn) => (cn === "x" ? xy[0] : cn === "y" ? xy[1] : P && cn === "kind" ? P.kind : makeVal(S.tb, cn, T.get(cn) || "num", P))));
    S.pts.push(q); S.n++; return true;
  }
  function dab(c, step) {   // one touch of the brush at c, step metres on from the last
    const S = stroke, R = Math.max(0.05, +BR.size || 1);
    if (S.mode === "ground") return;
    if (S.mode === "relief") return reliefDab(c, R);
    if (S.erase) return eraseDab(c, R);
    const sp = Math.max(0.02, +BR.spacing || 0.3);
    if (!S.clumps) { for (let k = 0, n = Math.min(300, Math.ceil(2 * R * R / (sp * sp))); k < n; k++) { const a = Math.random() * 2 * Math.PI, rr = R * Math.sqrt(Math.random()); putPiece([c[0] + rr * Math.cos(a), c[1] + rr * Math.sin(a)], sp); } return; }
    const ph = S.ph || (S.ph = { k: "", left: 0 });
    ph.left -= step;
    if (ph.left <= 0) {   // the next spell: after a clump a trail or a gap, after a gap mostly a clump
      const u = Math.random();
      ph.k = ph.k === "" ? "clump" : ph.k === "clump" ? (u < 0.6 ? "trail" : "gap") : ph.k === "trail" ? (u < 0.55 ? "clump" : "gap") : (u < 0.7 ? "clump" : "trail");
      ph.left = R * (ph.k === "clump" ? rnd(0.6, 1.4) : ph.k === "trail" ? rnd(0.8, 2.5) : rnd(0.6, 2));
      if (ph.k === "clump") for (let m = 1 + (Math.random() < 0.35) + (Math.random() < 0.15); m > 0; m--) {   // one to three heaps, each a cloud thick in the middle
        const a = Math.random() * 2 * Math.PI, rr = R * 0.6 * Math.sqrt(Math.random()), o = [c[0] + rr * Math.cos(a), c[1] + rr * Math.sin(a)], sg = R * rnd(0.12, 0.35);
        const n = Math.max(3, Math.min(60, Math.round(Math.PI * sg * sg / (sp * sp) * rnd(1.2, 2.4))));
        for (let k = 0, got = 0; k < n * 3 && got < n; k++) got += putPiece([o[0] + gauss() * sg, o[1] + gauss() * sg], sp * 0.45) ? 1 : 0;
      }
    }
    if (ph.k === "trail") {   // a piece every few spacings, near the brush's line
      let e = step / (sp * rnd(3, 7)); for (; e > 0; e--) if (Math.random() < Math.min(1, e)) { const g = Math.min(R, Math.abs(gauss()) * R * 0.3), a = Math.random() * 2 * Math.PI; putPiece([c[0] + g * Math.cos(a), c[1] + g * Math.sin(a)], sp); }
    }
  }
  function eraseDab(c, R) {   // take the rows of the chosen kinds under the brush
    const S = stroke, [rt, ts] = S.mode === "litter" ? ["litter", ["pieces"]] : ["goods", [S.mode.split(":")[1]]], K = kindFilter(BR_T[S.mode]);
    for (const r of recsOf([rt])) {
      if (dOf.get(r.id) !== S.d) continue;
      for (const t of ts) {
        const tab = r[t]; if (!tab || !Array.isArray(tab.rows)) continue;
        const ki = tab.cols.indexOf("kind"), keep = tab.rows.filter((row) => { const q = pieceXY(r, Object.fromEntries(tab.cols.map((cn, i) => [cn, row[i]]))); return !(q && dist(q, c) <= R && (!K || K.includes(row[ki]))); });
        if (keep.length === tab.rows.length) continue;
        if (!S.touched.has(r.id)) S.touched.set(r.id, clone(r));
        S.n += tab.rows.length - keep.length; tab.rows = keep;
      }
    }
  }
  function reliefDab(c, R) {   // each cell under the stroke changes once, softer toward the brush's edge
    const S = stroke, op = BR.relief.op, mm = +BR.relief.mm || 0, sg = S.erase ? -1 : 1;
    for (const r of recsOf(["relief"])) {
      const b = reliefBox(r); if (!b || dOf.get(r.id) !== S.d || !Array.isArray(r.z_mm)) continue;
      const g = r.cell, i0 = Math.max(0, Math.ceil((c[0] - R - r.origin[0]) / g)), i1 = Math.min(r.cols - 1, Math.floor((c[0] + R - r.origin[0]) / g)), j0 = Math.max(0, Math.ceil((c[1] - R - r.origin[1]) / g)), j1 = Math.min(r.rows - 1, Math.floor((c[1] + R - r.origin[1]) / g));
      if (i0 > i1 || j0 > j1) continue;
      if (!S.touched.has(r.id)) { S.touched.set(r.id, clone(r)); S.cells.set(r.id, new Set()); }
      const done = S.cells.get(r.id), z0 = S.touched.get(r.id).z_mm, at = (i, j) => z0[j * r.cols + i] || 0;
      for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) {
        const k = j * r.cols + i, dd = dist([r.origin[0] + i * g, r.origin[1] + j * g], c); if (dd > R || done.has(k)) continue;
        done.add(k); S.n++;
        const w = 1 - (dd / R) ** 2; let z = at(i, j);
        if (op === "raise") z += sg * mm * w; else if (op === "lower") z -= sg * mm * w;
        else if (op === "bumps") z += (Math.random() * 2 - 1) * mm * w;
        else if (op === "smooth") { let s = 0, n = 0; for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) { const ii = i + di, jj = j + dj; if (ii >= 0 && jj >= 0 && ii < r.cols && jj < r.rows) { s += at(ii, jj); n++; } } z += (s / n - z) * w; }
        else if (op === "flatten") z *= 1 - w;
        r.z_mm[k] = Math.round(z);
      }
    }
  }
  function brushMove(p) {   // dabs at even steps along the pointer's path, so a fast stroke leaves no gaps
    const S = stroke, step = Math.max(0.05, (+BR.size || 1) / (S.mode === "ground" ? 4 : 2));
    for (let L = dist(S.last, p); L >= step; L = dist(S.last, p)) { const t = step / L, q = [S.last[0] + (p[0] - S.last[0]) * t, S.last[1] + (p[1] - S.last[1]) * t]; S.last = q; S.path.push(q); dab(q, step); }
    V.draw();
  }
  async function brushUp() {
    const S = stroke; stroke = null; if (!S) return;
    if (S.mode === "ground") { S.path.push(cursor || S.last); return groundStroke(S); }
    const out = [];
    for (const [id, before] of S.touched) { const r = rec(id); if (!r) continue; out.push(clone(r)); Object.keys(r).forEach((k) => delete r[k]); Object.assign(r, before); }   // the saved ones come back from the save
    for (const id of S.made) { const r = rec(id); DS.get(dOf.get(id)).recs.delete(id); dOf.delete(id); if (r) out.push(r); }
    const empty = (q) => (q.type === "litter" ? !q.pieces.rows.length : q.type === "goods" ? !q.items.rows.length && !q.hung.rows.length : false);
    const keep = out.filter((q) => !empty(q)), gone = out.filter((q) => empty(q) && !S.made.includes(q.id)).map((q) => q.id);   // a record left with no rows goes
    if (!S.n || (!keep.length && !gone.length)) { V.draw(); return; }
    const what = S.mode === "relief" ? `Brushed ${S.n} relief cell${S.n > 1 ? "s" : ""}` : `${S.erase ? "Erased" : "Brushed"} ${S.n} ${S.mode === "litter" ? "litter piece" : "goods item"}${S.n > 1 ? "s" : ""}`;
    await saveStroke(S.dd, keep, gone, what);
  }
  async function saveStroke(d, records, remove, what) {
    const j = await api("/api/map/save", { d, records, remove });
    if (!j) { await load(d); return; }
    applyChanges(d, records, j.removed, j.problems); lastMsg = what; toast(what + ": ⌘Z takes the whole stroke back");
    if (sel) sel = rec(sel.id); V.draw(); showPanel();
  }
  async function groundStroke(S) {
    const rings = sweptRings(S.path, Math.max(0.05, +BR.size || 1)); if (!rings.length) { V.draw(); return; }
    const g = { id: newId("ground"), type: "ground", rings, order: Math.max(0, ...recsOf(["ground"]).map((x) => x.order || 0)) + 1 };
    if (BR.ground.kind) g.kind = BR.ground.kind;   // left out, it needs a value (amber)
    if (/^#[0-9a-f]{6}$/.test(BR.ground.colour || "")) g.colour = BR.ground.colour;
    await saveStroke(S.d, [g], [], `Painted ${g.kind || "ground (kind still to set)"}${rings.length > 1 ? `, ${rings.length} patches` : ""}`);
  }
  function valueNoise() {   // smooth noise in -1..1 over the plane, its table thrown now (stroke time) and never stored
    const T = Float32Array.from({ length: 1024 }, () => Math.random() * 2 - 1), h = (i, j) => T[(Math.imul(i, 374761393) ^ Math.imul(j, 668265263)) >>> 22], sm = (t) => t * t * (3 - 2 * t);
    return (x, y) => { const i = Math.floor(x), j = Math.floor(y), u = sm(x - i), v = sm(y - j), a = h(i, j), b = h(i + 1, j), c = h(i, j + 1), d = h(i + 1, j + 1); return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v; };
  }
  function sweptRings(path, R) {   // the outline of the ground the stroke covers: cells on a fine grid, holes filled, edges traced
    // A broken edge: the reach from the stroke swells and bites with noise at two sizes, and crumbs lie loose just past it.
    const br = Math.max(0, Math.min(1, +BR.ground.broken || 0)), amp = 0.55 * br, Rx = R * (1 + amp * 1.6);
    const c = Math.max(0.04, R / (br > 0 ? 8 : 4)), b = bboxOf(path), x0 = b[0] - Rx - 2 * c, y0 = b[1] - Rx - 2 * c, nx = Math.ceil((b[2] - b[0] + 2 * Rx) / c) + 5, ny = Math.ceil((b[3] - b[1] + 2 * Rx) / c) + 5;
    if (nx * ny > 3e6) { toast("That stroke is too big for one patch: paint it in shorter strokes or with a smaller brush"); return []; }
    const D = new Float32Array(nx * ny).fill(1e9), segs = path.length > 1 ? path.slice(1).map((q, i) => [path[i], q]) : [[path[0], path[0]]];
    for (const [a, q] of segs) {
      const i0 = Math.max(0, Math.floor((Math.min(a[0], q[0]) - Rx - x0) / c)), i1 = Math.min(nx - 1, Math.ceil((Math.max(a[0], q[0]) + Rx - x0) / c)), j0 = Math.max(0, Math.floor((Math.min(a[1], q[1]) - Rx - y0) / c)), j1 = Math.min(ny - 1, Math.ceil((Math.max(a[1], q[1]) + Rx - y0) / c));
      for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) { const k = j * nx + i, dd = segDist([x0 + (i + 0.5) * c, y0 + (j + 0.5) * c], a, q); if (dd < D[k]) D[k] = dd; }
    }
    const F = new Uint8Array(nx * ny), N1 = valueNoise(), N2 = valueNoise(), N3 = valueNoise(), s1 = 1 / (0.8 * R), s2 = 1 / (0.25 * R), s3 = 1 / (0.12 * R);
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const k = j * nx + i; if (D[k] > Rx) continue;
      if (!br) { F[k] = D[k] <= R ? 1 : 0; continue; }
      const x = x0 + (i + 0.5) * c, y = y0 + (j + 0.5) * c, reach = R * (1 + amp * (0.65 * N1(x * s1, y * s1) + 0.35 * N2(x * s2, y * s2)));
      F[k] = D[k] <= reach || (D[k] <= Rx && N3(x * s3, y * s3) > 1 - 0.5 * br) ? 1 : 0;   // inside the swelling reach, or a crumb
    }
    for (let pass = 0, fixed = 1; fixed && pass < 4; pass++) {   // two cells touching only at a corner make a ring cross itself: fill one side
      fixed = 0;
      for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) { const k = j * nx + i, a = F[k], b2 = F[k + 1], c2 = F[k + nx], d = F[k + nx + 1]; if (a === d && b2 === c2 && a !== b2) { if (a) F[k + 1] = 1; else F[k] = 1; fixed = 1; } }
    }
    const out = new Uint8Array(nx * ny), st = [0]; out[0] = 1;   // the outside, flooded from a corner; what it can't reach is painted
    while (st.length) { const k = st.pop(), i = k % nx, j = (k - i) / nx; for (const [ii, jj] of [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]) { if (ii < 0 || jj < 0 || ii >= nx || jj >= ny) continue; const kk = jj * nx + ii; if (!out[kk] && !F[kk]) { out[kk] = 1; st.push(kk); } } }
    const on = (i, j) => i >= 0 && j >= 0 && i < nx && j < ny && !out[j * nx + i];
    const nxt = new Map(), key = (i, j) => i + "," + j, edge = (a, q) => { const k = key(...a); if (!nxt.has(k)) nxt.set(k, []); nxt.get(k).push(q); };
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {   // each painted cell's sides that face the outside, clockwise on the board
      if (!on(i, j)) continue;
      if (!on(i, j - 1)) edge([i, j], [i + 1, j]); if (!on(i + 1, j)) edge([i + 1, j], [i + 1, j + 1]);
      if (!on(i, j + 1)) edge([i + 1, j + 1], [i, j + 1]); if (!on(i - 1, j)) edge([i, j + 1], [i, j]);
    }
    const rings = [];
    for (const [k0, L] of nxt) while (L.length) {
      const loop = [k0.split(",").map(Number)];
      let v = L.pop();
      while (key(...v) !== k0) { loop.push(v); const M = nxt.get(key(...v)); if (!M || !M.length) break; v = M.pop(); }
      let P = loop.filter((p, i) => { const a = loop[(i + loop.length - 1) % loop.length], q = loop[(i + 1) % loop.length]; return (p[0] - a[0]) * (q[1] - p[1]) - (p[1] - a[1]) * (q[0] - p[0]) !== 0; }).map(([i, j]) => [x0 + i * c, y0 + j * c]);
      if (P.length < 3) continue;
      const S = simplifyRing(P, c * 0.6); if (S.length >= 3 && !ringCrosses(S)) P = S;
      P = P.map((p) => [r2(p[0]), r2(p[1])]);
      if (Math.abs(signedArea(P)) > Math.max(0.02, 2 * c * c) && !ringCrosses(P)) rings.push(P);
    }
    return rings;
  }
  function simplifyRing(P, tol) {   // Douglas-Peucker on a closed ring, split at the point farthest from the first
    const dp = (L) => { if (L.length < 3) return L; let im = 0, dm = 0; for (let i = 1; i < L.length - 1; i++) { const d = segDist(L[i], L[0], L[L.length - 1]); if (d > dm) { dm = d; im = i; } } return dm <= tol ? [L[0], L[L.length - 1]] : dp(L.slice(0, im + 1)).slice(0, -1).concat(dp(L.slice(im))); };
    let f = 0; P.forEach((p, i) => { if (dist(p, P[0]) > dist(P[f], P[0])) f = i; });
    return dp(P.slice(0, f + 1)).slice(0, -1).concat(dp(P.slice(f).concat([P[0]])).slice(0, -1));
  }
  function ringCrosses(P) { const n = P.length; for (let i = 0; i < n; i++) for (let j = i + 2; j < n; j++) { if (i === 0 && j === n - 1) continue; if (segsCross(P[i], P[(i + 1) % n], P[j], P[(j + 1) % n])) return true; } return false; }
  function parentNear(p) {   // what a new person spot belongs to: the stall, lean-to, vehicle, furniture or heap it stands at, else the house it is in (a link, not a value)
    const d = dHere(p); let best = null, bd = 1.5;
    for (const r of recsOf(["stall", "vehicle", "furniture", "heap", "leanto"])) {
      if (dOf.get(r.id) !== d) continue;
      const q = r.type === "leanto" ? leantoQuad(r) : thingPts(r), dd = q ? (inPoly(p, q) ? 0 : ringDist(p, q)) : Array.isArray(r.at) ? Math.max(0, dist(p, r.at) - thingR(r)) : 1e9;
      if (dd < bd) { bd = dd; best = r; }
    }
    return best || recsOf(["building"]).find((r) => dOf.get(r.id) === d && Array.isArray(r.footprint) && r.footprint.length > 2 && inPoly(p, r.footprint)) || null;   // else the house it is in
  }
  function drawBrush(ctx, px) {
    if (tool !== "brush" || !cursor) return;
    const R = Math.max(0.05, +BR.size || 1), er = (stroke ? stroke.erase : BR.erase || brAlt) && BR.mode !== "ground";
    if (stroke && stroke.mode === "ground" && stroke.path.length) { path(ctx, stroke.path.concat([cursor])); ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = /^#[0-9a-f]{6}$/.test(BR.ground.colour || "") ? BR.ground.colour : GROUND[BR.ground.kind] || "#8a7a66"; ctx.globalAlpha = 0.6; ctx.lineWidth = 2 * R; ctx.stroke(); ctx.globalAlpha = 1; ctx.lineCap = "butt"; }
    ctx.beginPath(); ctx.arc(cursor[0], cursor[1], R, 0, 7); ctx.strokeStyle = er ? css("--bad") : css("--sel"); ctx.lineWidth = 1.5 * px; ctx.setLineDash(er ? [4 * px, 3 * px] : []); ctx.stroke(); ctx.setLineDash([]);
  }
  function colHTML(tb, c, cs) {   // how the brush gives one column its value
    const f = spec(cs), M = maker(tb, c), da = (fld) => `data-br="col" data-tb="${tb}" data-c="${c}" data-f="${fld}"`;
    const modes = [["unset", "unset"], ["value", "this value"]].concat(f.base === "num" || f.base === "int" ? [["range", "random between"]] : []).concat(f.base === "enum" || f.base === "hex" ? [["pick", "random from"]] : []).concat(tb === "litter_piece" && MIXABLE.has(c) ? [["mix", c === "age" || c === "buried" ? "natural mix: fresh, old, buried" : c === "kind" ? "street mix: sachets, bags, bottles..." : c === "colour" ? "its kind's colours" : "natural mix: mostly small, a few big"]] : []);
    let inp = "";
    if (M.m === "value") inp = f.base === "enum" ? `<select ${da("v")}><option value="">— pick —</option>${SCHEMA.enums[f.arg].map((e) => `<option${e === M.v ? " selected" : ""}>${e}</option>`).join("")}</select>` : f.base === "hex" ? `<span class="hexrow"><input ${da("v")} value="${esc(M.v || "")}" placeholder="#rrggbb"><input type="color" ${da("v")} value="${esc(M.v || "#808080")}"></span>` : `<input type="number" step="any" ${da("v")} value="${M.v ?? ""}" placeholder="${esc(f.rng)}">`;
    else if (M.m === "range") inp = `<span class="ptrow"><input type="number" step="any" ${da("a")} value="${M.a ?? ""}" placeholder="from"><input type="number" step="any" ${da("b")} value="${M.b ?? ""}" placeholder="to"></span>`;
    else if (M.m === "pick") inp = f.base === "enum" ? `<div class="chk">${SCHEMA.enums[f.arg].map((e) => `<label><input type="checkbox" ${da("list")} value="${e}"${(M.list || []).includes(e) ? " checked" : ""}>${e}</label>`).join("")}</div>` : `<input ${da("list")} value="${esc((M.list || []).join(", "))}" placeholder="#rrggbb, #rrggbb, …">`;
    return `<div class="brc"><span class="fk${M.m === "unset" ? " unset" : ""}" title="${esc(cs)}">${c}</span><select ${da("m")}>${modes.map(([v, l]) => `<option value="${v}"${v === M.m ? " selected" : ""}>${l}</option>`).join("")}</select>${inp ? `<div class="bri">${inp}</div>` : ""}</div>`;
  }
  function brushHTML() {
    const m = BR.mode, tb = BR_T[m], lab = { litter: "litter", "goods:items": "goods on the ground", "goods:hung": "goods hung", relief: "relief", ground: "ground paint" }[m] || m;
    let h = `<h3>Brush: ${esc(lab)}</h3><div class="fld"><span class="fk">size (radius, m)</span><input type="number" step="any" min="0.05" data-br="size" value="${BR.size}"></div>`;
    if (tb) {
      const fam = famOf(m);
      h += `<div class="fld"><span class="fk">spacing (m)</span><input type="number" step="any" min="0.02" data-br="spacing" value="${BR.spacing}"></div>`;
      h += `<div class="fld"><span class="fk">how they lie</span><select data-br="scatter">${[["clumps", "clumps, trails and gaps"], ["even", "even"]].map(([v, l]) => `<option value="${v}"${BR.scatter[fam] === v ? " selected" : ""}>${l}</option>`).join("")}</select></div>`;
      h += `<div class="fld"><span class="fk">pull to edges</span><select data-br="pull">${[[0, "off"], [0.4, "some"], [0.7, "most"], [1, "all"]].map(([v, l]) => `<option value="${v}"${Math.abs((+BR.pull[fam] || 0) - v) < 0.05 ? " selected" : ""}>${l}</option>`).join("")}</select></div>`;
    }
    if (m !== "ground") h += `<div class="fld"><span class="fk">${m === "relief" ? "the other way" : "erase"}</span><label><input type="checkbox" data-br="erase"${BR.erase ? " checked" : ""}> ${m === "relief" ? "lower where it raises (or hold ⌥)" : "take pieces away (or hold ⌥)"}</label></div>`;
    if (tb) h += `<fieldset><legend>Each ${m === "litter" ? "piece" : "item"}'s values${tb === "item" ? " (x, y in the host's frame)" : ""}</legend>${SCHEMA.tables[tb].filter(([c]) => c !== "x" && c !== "y").map(([c, cs]) => colHTML(tb, c, cs)).join("")}</fieldset><p class="k">Where each one lies (x, y) comes from the stroke${tb === "item" ? ", inside the lean-to, stall, heap or bin it starts in" : ""}: in clumps (a few tight heaps, then a thin trail or an empty gap, the lengths thrown as you brush) or evenly, none closer than the spacing (closer inside a clump). Pull to edges moves that share of them against the nearest ${tb === "item" ? "side of the host" : "kerb line, wall or house foot, stall or lean-to side, pole or tree"}; litter never lands on a roof. Street mix (kind and colour): the old kit's street litter, sachets most, then black and coloured bags, bottles, packs, cans and corn husks, each in its own colours; paper, rags and tyres only when you pick them. Natural mix: sizes about 7 in 10 small, 2 medium, 1 in 14 big (bottles, cans and tyres vary less); ages 3 in 10 fresh, 4 weathered, 3 old, most of the old part buried. "Random" values are picked now, once, and stored; "unset" stays unset (amber) for you to give. The eraser takes the pieces under it of the kinds chosen above (every kind when kind is unset or the street mix).</p>`;
    if (m === "relief") h += `<div class="fld"><span class="fk">what it does</span><select data-br="op">${["raise", "lower", "bumps", "smooth", "flatten"].map((o) => `<option${o === BR.relief.op ? " selected" : ""}>${o}</option>`).join("")}</select></div><div class="fld"><span class="fk">by (mm)</span><input type="number" step="1" data-br="mm" value="${BR.relief.mm}"></div><p class="k">Brush over a relief grid (draw one with Relief, H). Each cell under the stroke changes once, less toward the brush's edge; bumps are random heights picked now and stored, cell by cell.</p>`;
    if (m === "ground") h += `<div class="fld"><span class="fk">kind</span><select data-br="gkind"><option value="">— needs a value —</option>${SCHEMA.enums.ground_kind.map((k) => `<option${k === BR.ground.kind ? " selected" : ""}>${k}</option>`).join("")}</select></div><div class="fld"><span class="fk">colour (optional)</span><span class="hexrow"><input data-br="gcolour" value="${esc(BR.ground.colour || "")}" placeholder="none: #rrggbb"><input type="color" data-br="gcolour" value="${esc(BR.ground.colour || "#808080")}"></span></div><div class="fld"><span class="fk">broken edge</span><select data-br="broken">${[[0, "clean"], [0.3, "a little"], [0.5, "broken"], [0.8, "very broken"]].map(([v, l]) => `<option value="${v}"${Math.abs((+BR.ground.broken || 0) - v) < 0.05 ? " selected" : ""}>${l}</option>`).join("")}</select></div><p class="k">One stroke is one painted patch over the earlier ones, stored as rings: the ground the stroke covers, its edge swelling and bitten at two sizes, with loose crumbs just past it (each crumb its own ring). The edge is thrown now, at stroke time, and stored point by point.</p>`;
    return h + `<p class="k">Change the brush with the kind list above; <kbd>[</kbd> <kbd>]</kbd> size. One stroke is one save: <kbd>⌘Z</kbd> takes it all back.</p>`;
  }
  function brushField(el) {
    const k = el.dataset.br, v = el.value;
    if (k === "size" || k === "spacing") { const n = Number(v); if (isFinite(n) && n > 0) BR[k] = n; }
    else if (k === "erase") BR.erase = el.checked;
    else if (k === "op") BR.relief.op = v; else if (k === "mm") BR.relief.mm = Number(v) || 0;
    else if (k === "gkind") BR.ground.kind = v; else if (k === "gcolour") BR.ground.colour = v.trim().toLowerCase(); else if (k === "broken") BR.ground.broken = Math.max(0, Math.min(1, Number(v) || 0));
    else if (k === "scatter") BR.scatter[famOf(BR.mode)] = v; else if (k === "pull") BR.pull[famOf(BR.mode)] = Number(v) || 0;
    else if (k === "col") {
      const tb = el.dataset.tb, c = el.dataset.c, f = el.dataset.f, cs = new Map(SCHEMA.tables[tb]).get(c), M = { ...maker(tb, c) };
      if (f === "m") M.m = v;
      else if (f === "v") { const q = parseVal({ dataset: { b: "cell", a: cs }, value: v }); if (q.err) { toast(q.err); return; } M.v = q.v; }
      else if (f === "a" || f === "b") M[f] = v.trim() === "" ? undefined : Number(v);
      else if (f === "list") M.list = spec(cs).base === "enum" ? [...$("panel").querySelectorAll(`input[data-br="col"][data-c="${c}"][data-f="list"]`)].filter((x) => x.checked).map((x) => x.value) : v.split(",").map((x) => x.trim().toLowerCase()).filter((x) => /^#[0-9a-f]{6}$/.test(x));
      BR.cols[tb] = BR.cols[tb] || {}; BR.cols[tb][c] = M;
    }
    saveBR(); if (el.dataset.f === "m" || el.dataset.f === "v" || k === "gcolour") showPanel(); V.draw();
  }

  // ------------------------------------------------------------------ pointer (frame.js hands over the left button)
  function down(ev, p) {   // true when the editor takes the click (frame.js pans otherwise); saving runs on its own
    if (!SCHEMA) return false;
    if (tool === "select") {
      const h = handleAt(p);
      if (h) {
        const e = editPts(sel), before = clone(sel); let pts = e.pts.map((q) => q.slice()), i = h.i;
        if (h.mid) { i = h.i + 1; const a = pts[h.i], b = pts[(h.i + 1) % pts.length]; pts.splice(i, 0, [r2((a[0] + b[0]) / 2), r2((a[1] + b[1]) / 2)]); }
        if (ev.altKey && !h.mid) {   // ⌥-click a corner: remove it
          if (pts.length <= (e.closed ? 3 : 2)) { toast("It needs at least " + (e.closed ? 3 : 2) + " points"); return true; }
          pts.splice(i, 1); const q = clone(sel); e.set(q, pts); save([q]); return true;
        }
        drag = { vtx: i, obj: sel, before, pts, closed: e.closed }; V.cv.classList.add("move"); return true;
      }
      const pc = pieceAt(p);
      if (pc) { sel = pc.r; selRow = { id: pc.r.id, t: pc.t, i: pc.i }; drag = { row: pc, start: p, moved: false }; showPanel(); V.draw(); return true; }   // one piece: drag moves just it
      const o = pick(p); sel = o; selRow = null; showPanel(); V.draw();
      if (o) { drag = { o, start: p, moved: false, before: clone(o), fol: followers(o).map((f) => ({ f, before: clone(f) })) }; return true; }
      return false;   // empty ground: frame.js pans
    }
    if (tool === "stamp") {
      if (placing) { placeStamp(p); return true; }
      if (!SRC) { toast("Pick what to copy from, in the panel"); return true; }
      const o = pick(p, srcW());
      if (!o) { pickBox = { a: p }; return true; }   // empty ground: drag a box round what to copy
      const id = rootOf(o.id);
      if (ev.shiftKey) { picked = picked.includes(id) ? picked.filter((x) => x !== id) : [...picked, id]; showPanel(); V.draw(); return true; }
      picked = [id]; startPlacing(); return true;
    }
    if (tool === "frontage") {
      const e = plotEdgeAt(p);
      if (!e) { toast("Click on the side of a plot that faces a street"); return true; }
      const mid = [(e.a[0] + e.b[0]) / 2, (e.a[1] + e.b[1]) / 2];
      let best = null, bd = 40;
      for (const r of recsOf(["road"])) { if (!Array.isArray(r.centreline) || r.centreline.length < 2) continue; const a = along(r.centreline, mid); if (a.off < bd) { bd = a.off; best = { r, a }; } }
      if (!best) { toast("No street within 40 m of that side: draw the street first"); return true; }
      const c = best.r.centreline, i = best.a.i, dx = c[i + 1][0] - c[i][0], dy = c[i + 1][1] - c[i][1], q = best.a.q;
      const side = (mid[0] - q[0]) * dy - (mid[1] - q[1]) * dx > 0 ? "left" : "right";   // as you walk the street from its first point (y south)
      let line = [e.a.slice(0, 2), e.b.slice(0, 2)];
      const ux = line[1][0] - line[0][0], uy = line[1][1] - line[0][1];
      if ((q[0] - mid[0]) * -uy + (q[1] - mid[1]) * ux < 0) line = line.reverse();   // the line runs with the street on its right: a lean-to on it stands toward the street
      const kind = $("mkind").value, r = { id: newId("frontage"), type: "frontage", plot: e.r.id, road: best.r.id, side, kind, line, ...defaults(SCHEMA.records.frontage.fields) };
      if (best.r.width > 0) r.setback = r2(Math.max(0, best.a.off - best.r.width / 2));   // measured from the drawing: the street's edge to the plot side
      if (WALLED.has(kind)) r.wall = defaults(SCHEMA.shapes.wall);
      create(r, mid); return true;
    }
    if (tool === "brush") { brushDown(ev, p); return true; }
    if (tool === "person") {   // click an existing spot to pick and drag it; elsewhere a new one, facing where you drag
      const o = pick(p);
      if (o && o.type === "person_spot") { sel = o; selRow = null; showPanel(); V.draw(); drag = { o, start: p, moved: false, before: clone(o), fol: [] }; return true; }
      drag = { spot: [r2(p[0]), r2(p[1])] }; return true;
    }
    if (tool === "wire") { wireClick(ev, p); return true; }
    if (tool === "face") { const e = edgeAt(p); if (!e || e.face === undefined) { toast("Click on a building's side"); return true; } openFace(e.r, e.face); return true; }
    if (tool === "goods" || tool === "litter") {
      const pc = pieceAt(p, [tool]);
      if (pc) { sel = pc.r; selRow = { id: pc.r.id, t: pc.t, i: pc.i }; drag = { row: pc, start: p, moved: false }; showPanel(); V.draw(); return true; }
      addPiece(p); return true;
    }
    if (tool === "relief") {
      const R = recsOf(["relief"]).find((r) => reliefBox(r) && inPoly(p, reliefBox(r)));
      if (R && Array.isArray(R.z_mm)) {   // one cell up (or down with ⌥), 10 mm, or 50 with Shift
        const i = Math.max(0, Math.min(R.cols - 1, Math.round((p[0] - R.origin[0]) / R.cell))), j = Math.max(0, Math.min(R.rows - 1, Math.round((p[1] - R.origin[1]) / R.cell))), q = clone(R);
        q.z_mm[j * R.cols + i] = (q.z_mm[j * R.cols + i] || 0) + (ev.altKey ? -1 : 1) * (ev.shiftKey ? 50 : 10); sel = R; save([q]); return true;
      }
      drag = { box: [r2(p[0]), r2(p[1])] }; return true;
    }
    if (tool === "street" || tool === "wall" || tool === "ground") {
      const sn = tool === "street" ? snapPt(p, null, ev) : { p: cornerSnap(p, null, ev) };
      linePts.push(sn); if (ev.detail >= 2) finishLine(); V.draw(); return true;
    }
    if (tool === "building" || tool === "plot" || tool === "place") { drag = { box: cornerSnap(p, null, ev) }; return true; }
    if (tool === "tree" || tool === "furniture") {
      const at = [r2(p[0]), r2(p[1])], k = $("mkind").value;
      let r;
      if (tool === "tree") r = { id: newId("tree"), type: "tree", kind: k, at, ...defaults(SCHEMA.records.tree.fields) };
      else { const [t, kind] = k.split(":"); r = { id: newId(t), type: t, kind, at, ...defaults(SCHEMA.records[t].fields) }; }
      create(r, at); return true;
    }
    if (tool === "surface") {
      const o = pick(p); if (!o || o.type !== "road") { toast("Click on a road"); return true; }
      const q = clone(o); q.surface = $("mkind").value; save([q]); return true;
    }
    if (tool === "gate" || tool === "leanto") {
      const e = edgeAt(p);
      if (!e) { toast(tool === "gate" ? "Click on a wall" : "Click on a building's side or a wall"); return true; }
      if (tool === "gate" && !(e.r.type === "wall" || (e.r.type === "frontage" && e.r.wall))) { toast("Click on a wall (a wall record, or a frontage with a wall)"); return true; }
      if (!firstClick) { firstClick = e; toast("Now click where it ends, on the same " + (e.face !== undefined ? "side" : "wall")); V.draw(); return true; }
      const a = firstClick; firstClick = null;
      if (a.r.id !== e.r.id || a.face !== e.face) { toast("Both ends go on the same " + (a.face !== undefined ? "side" : "wall") + ": start again"); V.draw(); return true; }
      const u0 = Math.min(a.u, e.u), u1 = Math.max(a.u, e.u);
      if (u1 - u0 < 0.2) { toast("That's too short: start again"); V.draw(); return true; }
      if (tool === "gate") {
        const q = clone(e.r); q.wall = q.wall || defaults(SCHEMA.shapes.wall); q.wall.gates = q.wall.gates || [];
        q.wall.gates.push({ u0, u1, ...defaults(SCHEMA.shapes.gate) }); sel = q; save([q]); return true;
      }
      const r = { id: newId("leanto"), type: "leanto", against: e.r.id, u0, u1, ...defaults(SCHEMA.records.leanto.fields) };
      if (e.face !== undefined) r.face = e.face;
      r._d = dOf.get(e.r.id); save([r]).then((ok) => { if (ok) { sel = rec(r.id); showPanel(); V.draw(); } }); return true;
    }
    return false;
  }
  async function wireClick(ev, p) {   // first a pole; then a pole (the line between them) or a house side or wall (a drop to the house)
    const o = pick(p), pole = o && o.type === "pole" ? o : null;
    if (!wireFrom) {
      if (!pole) { toast("Click a pole to start the wire"); return; }
      wireFrom = pole; toast("Now click the other pole, or the house side or wall it runs to"); V.draw(); return;
    }
    const from = wireFrom, k = $("mkind").value;
    const r = { id: newId("wire"), type: "wire", from_pole: from.id, ...defaults(SCHEMA.records.wire.fields) };
    if (pole) {
      if (pole.id === from.id) { toast("That's the pole it starts at: click another"); return; }
      r.to_pole = pole.id; r.kind = k || "line";
    } else {
      const e = edgeAt(p);
      if (!e) { toast("Click another pole, or a house side or wall"); return; }
      let at;
      if (e.face !== undefined) { const fp = e.r.footprint, a = fp[e.face], q = fp[(e.face + 1) % fp.length], L = dist(a, q) || 1; at = [a[0] + (q[0] - a[0]) * e.u / L, a[1] + (q[1] - a[1]) * e.u / L]; }
      else at = pointAlong(e.r.line, e.u);
      const h = Number(wireZ);
      if (!(wireZ !== "" && isFinite(h) && h > 0)) { toast("Set \"tied at\" in the top bar first: how high the wire meets the house or wall"); $("mwirez").focus(); return; }
      r.to_at = [r2(at[0]), r2(at[1]), r2(h)];
      r.kind = k || "service";
    }
    r._d = dOf.get(from.id);
    const ok = await save([r]);
    if (!ok) return;
    sel = rec(r.id); wireFrom = pole && ev.shiftKey ? pole : null;
    showPanel(); V.draw();
  }
  function move(ev, p) {
    cursor = p;
    if (tool === "wire") { if (wireFrom) V.draw(); return false; }
    if (pickBox) { pickBox.b = p; V.draw(); return true; }
    if (tool === "brush") { brAlt = ev.altKey; if (stroke) brushMove(p); else V.draw(); return !!stroke; }
    if (drag && drag.spot) { drag.to = p; V.draw(); return true; }
    if (tool === "stamp") { if (placing) V.draw(); else { const o = SRC && pick(p, srcW()); if (o !== hover) { hover = o; V.draw(); } } return false; }
    if (tool === "frontage") { const e = plotEdgeAt(p); if ((e && e.r.id + e.i) !== (hoverEdge && hoverEdge.r.id + hoverEdge.i)) { hoverEdge = e; V.draw(); } return false; }
    if (drag && drag.vtx !== undefined) {
      let q;
      if (drag.obj.type === "road" && (drag.vtx === 0 || drag.vtx === drag.pts.length - 1)) { const sn = snapPt(p, drag.obj, ev); q = sn.p; drag.snap = sn; snapAt = sn.on || sn.real ? sn.p : null; }
      else q = drag.obj.type === "road" ? [r2(p[0]), r2(p[1])] : cornerSnap(p, drag.obj, ev);
      drag.pts[drag.vtx] = [q[0], q[1], ...(drag.pts[drag.vtx].slice(2))];
      const e = editPts(drag.obj); e.set(drag.obj, drag.pts.map((x) => x.slice())); V.draw(); return true;
    }
    if (drag && drag.row) {
      if (!drag.moved && Math.hypot(...V.toS(p).map((x, i) => x - V.toS(drag.start)[i])) < 4) return true;
      const { r, t, i } = drag.row, xy = toLocal(r, p); if (!xy) return true;
      if (!drag.moved) { drag.moved = true; drag.before = r[t].rows[i].slice(); }
      const c = r[t].cols; r[t].rows[i][c.indexOf("x")] = xy[0]; r[t].rows[i][c.indexOf("y")] = xy[1]; V.draw(); return true;
    }
    if (drag && drag.o) {
      if (!drag.moved && Math.hypot(...V.toS(p).map((x, i) => x - V.toS(drag.start)[i])) < 4) return true;
      drag.moved = true; V.cv.classList.add("move");
      const dx = p[0] - drag.start[0], dy = p[1] - drag.start[1], m = moveRec(drag.before, dx, dy);
      Object.keys(drag.o).forEach((k) => delete drag.o[k]); Object.assign(drag.o, m);
      for (const { f, before } of drag.fol || []) { const q = moveRec(before, dx, dy); Object.keys(f).forEach((k) => delete f[k]); Object.assign(f, q); }   // its person spots go with it
      V.draw(); return true;
    }
    if (drag && drag.box) { const a = drag.box, b = cornerSnap(p, null, ev); ghost = [[a[0], a[1]], [b[0], a[1]], [b[0], b[1]], [a[0], b[1]]]; V.draw(); return true; }
    if (tool === "street" || tool === "wall" || tool === "ground") { const sn = tool === "street" ? snapPt(p, null, ev) : { p: cornerSnap(p, null, ev) }; snapAt = sn.on || sn.real ? sn.p : null; if (linePts.length) V.draw(); else if (snapAt) V.draw(); return false; }
    if (tool === "select") { const h = handleAt(p); V.cv.style.cursor = h ? "pointer" : ""; const o = pick(p); if (o !== hover) { hover = o; V.draw(); } }
    return false;
  }
  async function up(ev, p) {
    V.cv.classList.remove("move");
    if (stroke) { await brushUp(); return; }
    if (drag && drag.spot) {   // a new person spot: what it does from the kind list; facing set only when dragged (else it needs a value)
      const at = drag.spot, to = drag.to; drag = null;
      const r = { id: newId("person_spot"), type: "person_spot", at, activity: $("mkind").value, ...defaults(SCHEMA.records.person_spot.fields) };
      if (to) { const A = V.toS(at), B = V.toS(to); if (Math.hypot(B[0] - A[0], B[1] - A[1]) > 6) r.turn = Math.round((Math.atan2(to[1] - at[1], to[0] - at[0]) * 180 / Math.PI + 360) % 360); }
      const par = parentNear(at); if (par) r.parent = par.id;
      await create(r, at); return;
    }
    if (pickBox) {
      const { a, b } = pickBox; pickBox = null;
      if (b && Math.abs(b[0] - a[0]) * V.s > 4 && Math.abs(b[1] - a[1]) * V.s > 4) {
        const box = [Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.max(a[0], b[0]), Math.max(a[1], b[1])], W = srcW();
        const inside = W.list(null).filter((r) => { const P = allPts(r, W.get); return P.length && P[0][0] >= box[0] && P[0][0] <= box[2] && P[0][1] >= box[1] && P[0][1] <= box[3]; });
        picked = [...new Set(inside.map((r) => rootOf(r.id)))];
        if (picked.length) startPlacing(); else toast("Nothing in that box");
      }
      V.draw(); return;
    }
    if (drag && drag.vtx !== undefined) {
      const { obj, before, pts, snap } = drag; drag = null; snapAt = null;
      const q = clone(obj), extra = [];
      if (snap && snap.on) { const j = withJunction(snap, pts); if (j) extra.push(j); }
      Object.keys(obj).forEach((k) => delete obj[k]); Object.assign(obj, before);   // the saved one comes back from save()
      await save([q, ...extra]); return;
    }
    if (drag && drag.row) {
      const { row, moved, before } = drag; drag = null;
      if (!moved) return;
      const q = clone(row.r); row.r[row.t].rows[row.i] = before;   // the saved one comes back from save()
      await save([q]); return;
    }
    if (drag && drag.o) {
      const { o, moved, before, fol } = drag; drag = null;
      if (!moved) return;
      const back = (x, b) => { const q = clone(x); Object.keys(x).forEach((k) => delete x[k]); Object.assign(x, b); return q; };   // the saved ones come back from save()
      await save([back(o, before), ...(fol || []).map(({ f, before: b }) => back(f, b))]); return;
    }
    if (drag && drag.box) {
      const g = ghost; drag = null; ghost = null;
      if (!g || Math.abs(g[2][0] - g[0][0]) < 0.5 || Math.abs(g[2][1] - g[0][1]) < 0.5) { V.draw(); return; }
      const ring = g.map((q) => [r2(q[0]), r2(q[1])]), k = $("mkind").value;
      let r;
      if (tool === "relief") {   // a flat grid (every cell 0 mm: flat is a value), to raise and lower by hand
        const c = Number(k) > 0 ? Number(k) : 0.5, b = bboxOf(ring), cols = Math.max(2, Math.round((b[2] - b[0]) / c) + 1), rows = Math.max(2, Math.round((b[3] - b[1]) / c) + 1);
        if (cols * rows > 40000) { toast("That grid is too big (over 40,000 cells): draw a smaller box or use bigger cells"); V.draw(); return; }
        await create({ id: newId("relief"), type: "relief", origin: [r2(b[0]), r2(b[1])], cell: c, cols, rows, z_mm: Array(cols * rows).fill(0) }, ring[0]); return;
      }
      if (tool === "building") r = { id: newId("building"), type: "building", kind: k, footprint: orient(ring), ...defaults(SCHEMA.records.building.fields) };
      else if (tool === "plot") r = { id: newId("plot"), type: "plot", kind: k, outline: ring };
      else r = { id: newId("place"), type: "place", kind: k, area: [ring], uses: [] };
      if (tool === "building") { const pl = recsOf(["plot"]).find((q) => Array.isArray(q.outline) && inPoly(centroid(ring), q.outline)); if (pl) r.plot = pl.id; }   // the plot it stands in: a link, not a value
      await create(r, ring[0]);
    }
  }
  async function finishLine() {
    const L = linePts; linePts = []; snapAt = null;
    if (L.length < 2) { V.draw(); return; }
    const pts = L.map((x) => x.p);
    if (tool === "ground") {   // painted over every earlier patch
      if (pts.length < 3) { toast("A patch needs at least 3 points"); V.draw(); return; }
      const order = Math.max(0, ...recsOf(["ground"]).map((g) => g.order || 0)) + 1;
      await create({ id: newId("ground"), type: "ground", kind: $("mkind").value, rings: [pts], order }, pts[0]); return;
    }
    if (tool === "wall") { await create({ id: newId("wall"), type: "wall", line: pts, wall: defaults(SCHEMA.shapes.wall) }, pts[0]); return; }
    const r = { id: newId("road"), type: "road", kind: $("mkind").value, centreline: pts, ...defaults(SCHEMA.records.road.fields) };
    const extra = new Map();   // roads the new one joins mid-way get the shared point
    for (const sn of L) { if (!sn.on) continue; const base = extra.get(sn.on.id) || sn.on; const j = withJunction({ ...sn, on: base, seg: along(base.centreline, sn.p).i }, null); if (j) extra.set(j.id, j); }
    const mid = pts[Math.floor(pts.length / 2)];
    if (!(await create(r, mid, [...extra.values()].filter((x) => dOf.get(x.id) === dHere(mid))))) return;
    const other = [...extra.values()].filter((x) => dOf.get(x.id) !== dHere(mid));
    if (other.length) await save(other);
  }

  // ------------------------------------------------------------------ drawing (world metres; frame.js has set the transform)
  const KIND_FILL = (k) => ({ face_me_bungalow: "--home", compound_house: "--home", colonial_house: "--home", walkup: "--home", shop_under_flats: "--trade", market_block: "--trade", kiosk_row: "--trade", church: "--civic", mosque: "--civic", school: "--civic", station_hall: "--civic" }[k] || "--works");
  const SURF = { tar_new: "--tar", tar_worn: "--worn", sand: "--sand", earth: "--mud", laterite: "--laterite", interlock: "--interlock" };
  const GROUND = { tar: "#3e3e40", earth: "#8a6a4a", laterite: "#a0522d", sand: "#d6c08a", dust: "#b8a688", mud: "#5a4632", wet: "#4b555e", water: "#3b6e8f", concrete: "#a7a49d", interlock: "#9a8070", grass: "#5f8a3a", rubble: "#8d8478" };   // drawing colours only
  const surfCol = (k) => SURF[k] ? css(SURF[k]) : k === "concrete" ? "#a7a49d" : k === "plank" ? "#8a6a4a" : css("--worn");
  let MAPON = true;
  function path(ctx, pts, close) { ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]); if (close) ctx.closePath(); }
  function drawWorld(ctx, v, px) {
    if (!SCHEMA) return;
    // load the started districts in view once zoomed in to a district or so
    if (v[2] - v[0] < 15000) for (const d of started) if (!DS.has(d) && !loading.has(d)) { const S = studyD(d); if (S && hit(S.bb, v)) load(d); }
    // and the dress tiles in view once zoomed in to a street or so
    if (v[2] - v[0] < 1500) for (const [d, D] of DS) {
      if (!D.tiles.size) continue; const want = [];
      for (let tx = Math.floor(v[0] / TILE); tx <= Math.floor(v[2] / TILE); tx++) for (let ty = Math.floor(v[1] / TILE); ty <= Math.floor(v[3] / TILE); ty++) { const k = tx + "_" + ty; if (D.tiles.has(k) && !D.got.has(k)) { D.got.add(k); want.push(k); } }
      if (want.length) loadTiles(d, want);
    }
    if (cur) { const S = studyD(cur); if (S) { ctx.strokeStyle = css("--accent"); ctx.lineWidth = 2.5 * px; ctx.setLineDash([10 * px, 6 * px]); for (const r of S.rings) { path(ctx, r[0], true); ctx.stroke(); } ctx.setLineDash([]); } }
    if (!MAPON) return;
    boardBad = boardProblems(v);
    const BAD = css("--bad"), WARN = css("--warn");
    const edge = (r, normal, w) => { const b = badness(r); ctx.strokeStyle = b === "bad" ? BAD : b === "incomplete" ? WARN : normal; ctx.lineWidth = b ? Math.max(w, 2.5 * px) : w; ctx.setLineDash(b === "incomplete" ? [5 * px, 3 * px] : []); ctx.stroke(); ctx.setLineDash([]); };
    const inView = (pts) => pts && pts.length && hit(bboxOf(pts), v);
    for (const r of recsOf(["place"])) for (const ring of (Array.isArray(r.area) ? r.area : [])) if (ring.length > 2 && inView(ring)) { path(ctx, ring, true); ctx.fillStyle = "rgba(31,111,235,.06)"; ctx.fill(); }
    for (const r of recsOf(["road"])) {
      const c = r.centreline; if (!Array.isArray(c) || c.length < 2 || !inView(c)) continue;
      ctx.lineJoin = "round"; ctx.lineCap = "butt";
      if (r.width > 0) { path(ctx, c); ctx.strokeStyle = surfCol(r.surface); ctx.lineWidth = r.width; ctx.stroke(); }
      path(ctx, c); const b = badness(r);
      ctx.strokeStyle = b === "bad" ? BAD : b === "incomplete" ? WARN : "rgba(255,255,255,.7)"; ctx.lineWidth = (b ? 2 : 1) * px; ctx.setLineDash(r.width > 0 ? [6 * px, 5 * px] : [3 * px, 3 * px]); ctx.stroke(); ctx.setLineDash([]);
      if (V.s > 1.5) for (const q of [c[0], c[c.length - 1]]) { ctx.beginPath(); ctx.arc(q[0], q[1], 2.5 * px, 0, 7); ctx.fillStyle = css("--ink"); ctx.fill(); }
    }
    for (const r of recsOf(["station"])) for (const ring of [...(Array.isArray(r.area) ? r.area : []), ...(Array.isArray(r.platforms) ? r.platforms : [])]) if (Array.isArray(ring) && ring.length > 2 && inView(ring)) { path(ctx, ring, true); ctx.fillStyle = "rgba(120,120,130,.35)"; ctx.fill(); edge(r, "#555", px); }
    for (const r of recsOf(["rail"])) {   // the corridor, then the sleepers' dash down the middle
      const c = r.centreline; if (!Array.isArray(c) || c.length < 2 || !inView(c)) continue;
      if (r.corridor > 0) { path(ctx, c); ctx.strokeStyle = "rgba(110,100,90,.45)"; ctx.lineWidth = r.corridor; ctx.stroke(); }
      path(ctx, c); ctx.setLineDash([4 * px, 3 * px]); edge(r, "#222", 2.5 * px); ctx.setLineDash([]);
    }
    // the ground: painted patches (later order over earlier) and relief grids
    for (const r of recsOf(["ground"]).sort((a, b) => (a.order || 0) - (b.order || 0))) for (const ring of (Array.isArray(r.rings) ? r.rings : [])) {
      if (!Array.isArray(ring) || ring.length < 3 || !inView(ring)) continue;
      path(ctx, ring, true); ctx.fillStyle = r.colour || GROUND[r.kind] || "#8a7a66"; ctx.globalAlpha = 0.85; ctx.fill(); ctx.globalAlpha = 1; edge(r, "rgba(0,0,0,.25)", px);
    }
    for (const r of recsOf(["relief"])) { const q = reliefBox(r); if (!q || !inView(q)) continue; if (V.s > 6 && Array.isArray(r.z_mm)) { const c = r.cell; for (let j = 0; j < r.rows; j++) for (let i = 0; i < r.cols; i++) { const z = r.z_mm[j * r.cols + i] || 0; if (!z) continue; const al = Math.min(0.6, 0.15 + Math.abs(z) / 150); ctx.fillStyle = z > 0 ? `rgba(255,170,60,${al})` : `rgba(40,110,220,${al})`; ctx.fillRect(r.origin[0] + i * c - c / 2, r.origin[1] + j * c - c / 2, c, c); } } path(ctx, q, true); ctx.setLineDash([3 * px, 3 * px]); edge(r, "rgba(255,170,60,.8)", px); ctx.setLineDash([]); }
    for (const r of recsOf(["plot"])) { if (!Array.isArray(r.outline) || r.outline.length < 3 || !inView(r.outline)) continue; path(ctx, r.outline, true); ctx.fillStyle = css("--plot"); ctx.fill(); ctx.setLineDash([4 * px, 3 * px]); const b = badness(r); ctx.strokeStyle = b === "bad" ? BAD : b === "incomplete" ? WARN : css("--plot-line"); ctx.lineWidth = (b ? 2 : 1) * px; ctx.stroke(); ctx.setLineDash([]); }
    for (const r of recsOf(["building"])) { const fp = r.footprint; if (!Array.isArray(fp) || fp.length < 3 || !inView(fp)) continue; path(ctx, fp, true); ctx.fillStyle = css(KIND_FILL(r.kind)); ctx.fill(); edge(r, css("--home-line"), Math.max(px, 0.08)); }
    for (const r of recsOf(["wall", "frontage"])) {
      const L = r.line; if (!Array.isArray(L) || L.length < 2 || !inView(L)) continue;
      path(ctx, L); edge(r, r.type === "wall" ? "#8a3b2e" : "#d4731c", Math.max(0.25, 1.4 * px));
      for (const g of ((r.wall || {}).gates || [])) { if (!(g.u1 > g.u0)) continue; const a = pointAlong(L, g.u0), b = pointAlong(L, g.u1); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.strokeStyle = "#1565c0"; ctx.lineWidth = Math.max(0.5, 4 * px); ctx.stroke(); }
    }
    for (const r of recsOf(["leanto"])) { const q = leantoQuad(r); if (!q || !inView(q)) continue; path(ctx, q, true); ctx.fillStyle = "rgba(150,155,150,.55)"; ctx.fill(); edge(r, "#6b6f76", px); }
    for (const r of recsOf(["stall", "vehicle", "furniture"])) { const q = thingPts(r); if (!q || !inView(q)) continue; path(ctx, q, true); ctx.fillStyle = r.type === "vehicle" ? "rgba(74,127,191,.75)" : r.type === "stall" ? "rgba(201,162,39,.8)" : "rgba(142,68,173,.7)"; ctx.fill(); edge(r, css("--ink"), px); }
    for (const r of recsOf(["heap", "tree"])) { if (!Array.isArray(r.at) || !inView([r.at])) continue; ctx.beginPath(); ctx.arc(r.at[0], r.at[1], thingR(r), 0, 7); ctx.fillStyle = r.type === "tree" ? "rgba(50,120,50,.32)" : "rgba(140,110,80,.5)"; ctx.fill(); edge(r, r.type === "tree" ? "#3d7a32" : "#6d5a44", Math.max(px, 0.08)); }
    for (const r of recsOf(["pole"])) { if (!Array.isArray(r.at) || !inView([r.at])) continue; ctx.beginPath(); ctx.arc(r.at[0], r.at[1], Math.max(0.2, 2.5 * px), 0, 7); ctx.fillStyle = "#5b4a3a"; ctx.fill(); edge(r, "#5b4a3a", px); }
    for (const r of recsOf(["wire"])) {
      const E = wireEnds(r); if (!E) continue; const b = badness(r);
      path(ctx, E); ctx.strokeStyle = b === "bad" ? BAD : "#333"; ctx.lineWidth = Math.max(px, (r.n > 1 ? 1.6 : 1) * px); ctx.setLineDash(r.kind === "service" ? [4 * px, 2 * px] : []); ctx.stroke(); ctx.setLineDash([]);
      if (b === "incomplete") { const m = [(E[0][0] + E[1][0]) / 2, (E[0][1] + E[1][1]) / 2]; ctx.beginPath(); ctx.arc(m[0], m[1], 3 * px, 0, 7); ctx.strokeStyle = WARN; ctx.lineWidth = 1.5 * px; ctx.stroke(); }
      if (!r.to_pole && Array.isArray(r.to_at)) { ctx.beginPath(); ctx.arc(E[1][0], E[1][1], 2 * px, 0, 7); ctx.fillStyle = "#333"; ctx.fill(); }
    }
    if (tool === "wire" && wireFrom && Array.isArray(wireFrom.at)) {
      ctx.beginPath(); ctx.arc(wireFrom.at[0], wireFrom.at[1], 6 * px, 0, 7); ctx.strokeStyle = css("--sel"); ctx.lineWidth = 2 * px; ctx.stroke();
      if (cursor) { path(ctx, [wireFrom.at, cursor]); ctx.globalAlpha = 0.6; ctx.setLineDash([4 * px, 3 * px]); ctx.stroke(); ctx.setLineDash([]); ctx.globalAlpha = 1; }
    }
    // small things: goods in their parent's frame, litter, potholes and ruts, person spots
    for (const r of recsOf(["goods"])) {
      const g = goodsFrame(rec(r.of), rec); if (!g || !inView([g.o])) continue;
      for (const o of [...rowsOf(r.items), ...rowsOf(r.hung)]) {
        if (![o.x, o.y].every(isFinite)) continue; const c = [g.o[0] + g.ux[0] * o.x + g.uy[0] * o.y, g.o[1] + g.ux[1] * o.x + g.uy[1] * o.y], t = Math.atan2(g.ux[1], g.ux[0]) * 180 / Math.PI + (o.turn || 0), sized = o.w > 0 && o.d > 0;
        path(ctx, boxPts(c, sized ? o.w : 0.3, sized ? o.d : 0.3, t), true); ctx.fillStyle = o.colour || "#c9b48a"; ctx.fill(); if (!sized) { ctx.strokeStyle = WARN; ctx.lineWidth = px; ctx.setLineDash([2 * px, 2 * px]); ctx.stroke(); ctx.setLineDash([]); }   // no size yet: drawn small, dashed
      }
      const b = badness(r); if (b) { ctx.beginPath(); ctx.arc(g.o[0], g.o[1], 4 * px, 0, 7); ctx.fillStyle = b === "bad" ? BAD : WARN; ctx.fill(); }
    }
    for (const r of recsOf(["litter", "people", "ground_marks"])) {
      const P = piecePts(r); if (!P.length || !inView(P)) continue; const b = badness(r);
      if (r.type === "ground_marks") { for (const u of (r.ruts || [])) if (Array.isArray(u.line) && u.line.length > 1) { path(ctx, u.line); ctx.strokeStyle = "rgba(60,40,25,.55)"; ctx.lineWidth = u.w > 0 ? u.w : 0.5; ctx.stroke(); } for (const o of rowsOf(r.potholes)) if (isFinite(o.x)) { ctx.beginPath(); ctx.arc(o.x, o.y, o.r > 0 ? o.r : 0.4, 0, 7); ctx.fillStyle = "rgba(50,35,25,.7)"; ctx.fill(); } }
      else for (const o of rowsOf(r.type === "litter" ? r.pieces : r.spots)) { if (!isFinite(o.x)) continue; ctx.beginPath(); ctx.arc(o.x, o.y, r.type === "people" ? Math.max(0.25, 3 * px) : Math.max(o.w > 0 ? o.w / 2 : 0.06, 1.5 * px), 0, 7); ctx.fillStyle = r.type === "people" ? "#e0457b" : (o.colour || "#ddd"); if (r.type === "litter" && o.age > 0) ctx.globalAlpha = 1 - 0.5 * Math.min(1, o.age); ctx.fill(); ctx.globalAlpha = 1; if (r.type === "litter" && o.buried > 0.15) { ctx.strokeStyle = "rgba(70,50,30,.8)"; ctx.lineWidth = Math.max(0.02, px); ctx.stroke(); } if (r.type === "people" && isFinite(o.turn)) { const a = o.turn * Math.PI / 180; ctx.beginPath(); ctx.moveTo(o.x, o.y); ctx.lineTo(o.x + Math.cos(a) * 0.5, o.y + Math.sin(a) * 0.5); ctx.strokeStyle = "#e0457b"; ctx.lineWidth = Math.max(0.06, px); ctx.stroke(); } }
      if (b) { const c = P[0]; ctx.beginPath(); ctx.arc(c[0], c[1], 5 * px, 0, 7); ctx.strokeStyle = b === "bad" ? BAD : WARN; ctx.lineWidth = 2 * px; ctx.stroke(); }
    }
    for (const r of recsOf(["person_spot"])) {   // a person from above: shoulders across the way they face, a head, a facing tick
      if (!Array.isArray(r.at) || !inView([r.at])) continue;
      const [x, y] = r.at, R = Math.max(0.22, 4.5 * px), b = badness(r), col = "#e0457b", a = isFinite(r.turn) ? r.turn * Math.PI / 180 : null;
      ctx.globalAlpha = clockOn && !outAt(r, clockH) ? 0.15 : 1;
      if (r.parent) { const par = rec(r.parent), Q = par && allPts(par); if (Q && Q.length) { const c = Array.isArray(par.at) ? par.at : centroid(Q); path(ctx, [r.at, c]); ctx.strokeStyle = "rgba(224,69,123,.5)"; ctx.lineWidth = px; ctx.setLineDash([2 * px, 2 * px]); ctx.stroke(); ctx.setLineDash([]); } }
      if (a !== null) { ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * R * 0.5, y + Math.sin(a) * R * 0.5); ctx.lineTo(x + Math.cos(a) * R * 2.3, y + Math.sin(a) * R * 2.3); ctx.strokeStyle = col; ctx.lineWidth = Math.max(0.05, 2 * px); ctx.stroke(); }
      ctx.beginPath(); ctx.ellipse(x, y, R, R * 0.55, a === null ? 0 : a + Math.PI / 2, 0, 7); ctx.fillStyle = col; ctx.fill();
      ctx.beginPath(); ctx.arc(x, y, R * 0.42, 0, 7); ctx.fillStyle = "#3a2218"; ctx.fill();
      if (b) { ctx.beginPath(); ctx.arc(x, y, R * 1.4, 0, 7); ctx.strokeStyle = b === "bad" ? BAD : WARN; ctx.lineWidth = 1.5 * px; ctx.setLineDash(b === "incomplete" ? [3 * px, 2 * px] : []); ctx.stroke(); ctx.setLineDash([]); }
      ctx.globalAlpha = 1;
    }
    if (drag && drag.spot && cursor) { const at = drag.spot; ctx.beginPath(); ctx.arc(at[0], at[1], Math.max(0.22, 4.5 * px), 0, 7); ctx.fillStyle = "rgba(224,69,123,.6)"; ctx.fill(); if (drag.to) { path(ctx, [at, drag.to]); ctx.strokeStyle = "#e0457b"; ctx.lineWidth = 2 * px; ctx.stroke(); } }
    for (const r of recsOf(["place"])) for (const ring of (Array.isArray(r.area) ? r.area : [])) if (ring.length > 2 && inView(ring)) { path(ctx, ring, true); ctx.setLineDash([8 * px, 4 * px]); const b = badness(r); ctx.strokeStyle = b === "bad" ? BAD : b === "incomplete" ? WARN : css("--accent"); ctx.lineWidth = 1.5 * px; ctx.stroke(); ctx.setLineDash([]); }
    // selection, hover, handles, what is being drawn
    const outline = (r, col, w) => {
      ctx.strokeStyle = col; ctx.lineWidth = w * px;
      const e = editPts(r), q = thingPts(r) || leantoQuad(r);
      if (e) { if (r.type === "road") { path(ctx, e.pts); ctx.lineWidth = (r.width || 0) + 6 * px; ctx.globalAlpha = 0.3; ctx.stroke(); ctx.globalAlpha = 1; } else { path(ctx, e.pts, e.closed); ctx.stroke(); } }
      else if (q) { path(ctx, q, true); ctx.stroke(); }
      else if (r.type === "wire") { const E = wireEnds(r); if (E) { path(ctx, E); ctx.stroke(); } }
      else if (Array.isArray(r.at)) { ctx.beginPath(); ctx.arc(r.at[0], r.at[1], Math.max(thingR(r), 9 * px), 0, 7); ctx.stroke(); }
    };
    if (hover && hover !== sel && tool === "select") outline(hover, css("--sel"), 1.5);
    if (sel) outline(sel, css("--sel"), 3);
    const rs = rowSel(); if (rs) { const q = pieceXY(sel, rowsOf(sel[rs.t])[rs.i]); if (q) { ctx.beginPath(); ctx.arc(q[0], q[1], Math.max(0.3, 7 * px), 0, 7); ctx.strokeStyle = css("--sel"); ctx.lineWidth = 2.5 * px; ctx.stroke(); } }
    const eh = tool === "select" && editPts(sel);
    if (eh) {
      const P = eh.pts, n = P.length, hs = 5 * px; ctx.lineWidth = 1.5 * px;
      for (let i = 0; i < (eh.closed ? n : n - 1); i++) { const a = P[i], b = P[(i + 1) % n]; ctx.beginPath(); ctx.arc((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 3.5 * px, 0, 7); ctx.fillStyle = css("--panel"); ctx.fill(); ctx.strokeStyle = css("--sel"); ctx.stroke(); }
      for (const q of P) { ctx.fillStyle = css("--panel"); ctx.fillRect(q[0] - hs, q[1] - hs, 2 * hs, 2 * hs); ctx.strokeStyle = css("--sel"); ctx.strokeRect(q[0] - hs, q[1] - hs, 2 * hs, 2 * hs); }
    }
    if (ghost) { ctx.fillStyle = css("--ghost"); ctx.strokeStyle = css("--sel"); ctx.lineWidth = 2 * px; path(ctx, ghost, true); ctx.fill(); ctx.stroke(); }
    if (linePts.length) {
      const P = linePts.map((x) => x.p).concat(cursor ? [snapAt || cursor] : []);
      path(ctx, P); ctx.strokeStyle = css("--sel"); ctx.lineWidth = Math.max(tool === "wall" ? 0.3 : 0.5, 3 * px); ctx.globalAlpha = 0.6; ctx.stroke(); ctx.globalAlpha = 1;
      for (const x of linePts) { ctx.beginPath(); ctx.arc(x.p[0], x.p[1], 4 * px, 0, 7); ctx.fillStyle = x.on ? css("--ok") : css("--sel"); ctx.fill(); }
    }
    if (firstClick) { const e = firstClick; let at; if (e.face !== undefined) { const fp = e.r.footprint, p0 = fp[e.face], q = fp[(e.face + 1) % fp.length], L = dist(p0, q) || 1; at = [p0[0] + (q[0] - p0[0]) * e.u / L, p0[1] + (q[1] - p0[1]) * e.u / L]; } else at = pointAlong(e.r.line, e.u); ctx.beginPath(); ctx.arc(at[0], at[1], 5 * px, 0, 7); ctx.fillStyle = css("--sel"); ctx.fill(); }
    if (hoverEdge && tool === "frontage") { path(ctx, [hoverEdge.a, hoverEdge.b]); ctx.strokeStyle = css("--sel"); ctx.lineWidth = 4 * px; ctx.stroke(); }
    drawStamp(ctx, v, px);
    drawBrush(ctx, px);
    if (snapAt) { ctx.beginPath(); ctx.arc(snapAt[0], snapAt[1], 7 * px, 0, 7); ctx.strokeStyle = css("--ok"); ctx.lineWidth = 2 * px; ctx.stroke(); }
  }
  function drawScreen(ctx) {   // small labels: a building's storeys, a line's length while drawing
    if (!SCHEMA || !MAPON) return;
    ctx.font = "600 11px -apple-system, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    if (V.s > 3) for (const r of recsOf(["building"])) { if (!Array.isArray(r.footprint) || r.footprint.length < 3) continue; const [X, Y] = V.toS(centroid(r.footprint)); if (X < 0 || Y < 0 || X > V.cv.clientWidth || Y > V.cv.clientHeight) continue; ctx.fillStyle = css("--ink"); ctx.fillText(r.storeys ? String(r.storeys) : "?", X, Y); }
    if (V.s > 9) for (const r of recsOf(["person_spot"])) { if (!Array.isArray(r.at) || (clockOn && !outAt(r, clockH))) continue; const [X, Y] = V.toS(r.at); if (X < 0 || Y < 0 || X > V.cv.clientWidth || Y > V.cv.clientHeight) continue; ctx.font = "500 10px -apple-system, sans-serif"; ctx.fillStyle = "#b8285e"; ctx.fillText((r.activity || "?").replace(/_/g, " ") + (r.count > 1 ? " ×" + r.count : ""), X, Y + 16); ctx.font = "600 11px -apple-system, sans-serif"; }
    if (linePts.length && cursor) { const P = linePts.map((x) => x.p).concat([snapAt || cursor]); const [X, Y] = V.toS(P[P.length - 1]); ctx.fillStyle = css("--ink"); ctx.fillText(lineLen(P).toFixed(1) + " m", X + 30, Y - 12); }
    ctx.textAlign = "start"; ctx.textBaseline = "alphabetic";
    renderStatus();
  }

  // ------------------------------------------------------------------ the panel: every field of the record, from the schema
  function fieldHTML(k, sp, v, p) {
    const f = spec(sp), has = v !== undefined, need = !f.opt && !has;
    const lab = `<span class="fk${need ? " bad" : ""}" title="${esc(sp)}">${esc(k)}${need ? " · needs a value" : ""}</span>`;
    const da = (extra = "") => `data-p="${esc(p)}" data-b="${f.base}" data-a="${esc(f.arg || "")}"${extra}`;
    const val = (x) => (x === undefined || x === null ? "" : esc(x));
    const ph = f.opt ? "none" : "needs a value";
    let c;
    switch (f.base) {
      case "enum": c = `<select ${da()}><option value="">${f.opt ? "— none —" : "— needs a value —"}</option>${SCHEMA.enums[f.arg].map((e) => `<option${e === v ? " selected" : ""}>${e}</option>`).join("")}</select>`; break;
      case "enums": c = `<div class="chk">${SCHEMA.enums[f.arg].map((e) => `<label><input type="checkbox" ${da()} value="${e}"${(v || []).includes(e) ? " checked" : ""}>${e}</label>`).join("")}</div>`; break;
      case "num": case "int": c = `<input type="number" step="any" ${da()} value="${val(v)}" placeholder="${ph}${f.rng ? " (" + esc(f.rng) + ")" : ""}">`; break;
      case "nums": c = `<input ${da()} value="${val(has ? v.join(", ") : "")}" placeholder="${ph}: numbers, a comma between">`; break;
      case "bool": c = `<select ${da()}><option value="">${f.opt ? "— none —" : "— needs a value —"}</option><option value="true"${v === true ? " selected" : ""}>yes</option><option value="false"${v === false ? " selected" : ""}>no</option></select>`; break;
      case "hex": c = `<span class="hexrow"><input ${da()} value="${val(v)}" placeholder="${ph}: #rrggbb"><input type="color" data-for="${esc(p)}" value="${has ? esc(v) : "#808080"}" title="Pick a colour"></span>`; break;
      case "hexes": case "strs": c = `<input ${da()} value="${val(has ? v.join(", ") : "")}" placeholder="${ph}: a comma between">`; break;
      case "pt": case "pt3": c = `<span class="ptrow">${["x", "y", "z"].slice(0, f.base === "pt" ? 2 : 3).map((a, i) => `<input type="number" step="any" ${da(` data-i="${i}"`)} value="${has ? val(v[i]) : ""}" placeholder="${a}">`).join("")}</span>`; break;
      case "id": { const types = f.arg.split(","), d = sel ? dOf.get(sel.id) : cur, opts = [...((DS.get(d) || { recs: new Map() }).recs.values())].filter((r) => types.includes(r.type) && r.id !== (sel && sel.id));
        c = `<select ${da()}><option value="">${f.opt ? "— none —" : "— needs a value —"}</option>${opts.map((r) => `<option value="${r.id}"${r.id === v ? " selected" : ""}>${r.id} ${esc(r.kind || r.type)}</option>`).join("")}${has && !opts.some((r) => r.id === v) ? `<option selected>${esc(v)}</option>` : ""}</select>`; break; }
      case "line": c = has ? `<span class="k">${v.length} points, ${lineLen(v).toFixed(1)} m (drag the handles)</span>` : ""; break;
      case "ring": c = has ? `<span class="k">${v.length} corners, ${Math.abs(signedArea(v)).toFixed(1)} m² (drag the handles)</span>` : ""; break;
      case "rings": c = has ? `<span class="k">${v.length} ring${v.length > 1 ? "s" : ""}, ${v.reduce((a, r) => a + Math.abs(signedArea(r)), 0).toFixed(0)} m²</span>` : ""; break;
      case "obj": {
        const shape = SCHEMA.shapes[f.arg];
        if (!has) return `<div class="fld">${lab}<button data-act="add" data-p="${esc(p)}" data-k="obj" data-a="${f.arg}">${f.opt ? "Add" : "Add (needed)"}</button></div>`;
        return `<fieldset><legend>${lab}${f.opt ? ` <button data-act="rm" data-p="${esc(p)}">remove</button>` : ""}</legend>${Object.entries(shape).map(([kk, ss]) => fieldHTML(kk, ss, v[kk], p + "." + kk)).join("")}</fieldset>`;
      }
      case "objs": {
        const shape = SCHEMA.shapes[f.arg];
        return `<fieldset><legend>${lab} <span class="k">${has ? v.length : 0}</span></legend>${(v || []).map((o, i) => `<fieldset class="item"><legend>${f.arg} ${i + 1} <button data-act="rm" data-p="${esc(p + "." + i)}">remove</button></legend>${Object.entries(shape).map(([kk, ss]) => fieldHTML(kk, ss, o[kk], p + "." + i + "." + kk)).join("")}</fieldset>`).join("")}<button data-act="push" data-p="${esc(p)}" data-a="${f.arg}">Add a ${f.arg}</button></fieldset>`;
      }
      case "table": {
        const cols = SCHEMA.tables[f.arg];
        if (!has) return `<div class="fld">${lab}<button data-act="add" data-p="${esc(p)}" data-k="table" data-a="${f.arg}">${f.opt ? "Add a table" : "Add (needed)"}</button></div>`;
        return `<fieldset><legend>${lab}${f.opt ? ` <button data-act="rm" data-p="${esc(p)}">remove</button>` : ""}</legend><div class="tbw"><table class="tb"><tr>${cols.map(([cn]) => `<th>${cn}</th>`).join("")}<th></th></tr>${v.rows.map((row, i) => `<tr${rowSel() && p === selRow.t && i === selRow.i ? ' class="on"' : ""}>${row.map((x, j) => `<td><input data-p="${esc(p)}.rows.${i}.${j}" data-b="cell" data-a="${esc(cols[j][1])}" value="${val(x)}"></td>`).join("")}<td><button data-act="rm" data-p="${esc(p)}.rows.${i}">×</button></td></tr>`).join("")}</table></div><button data-act="row" data-p="${esc(p)}" data-a="${f.arg}">Add a row</button></fieldset>`;
      }
      default: c = `<input ${da()} value="${val(v)}" placeholder="${ph}">`;
    }
    return `<div class="fld">${lab}${c}${has && f.opt && !["obj", "objs", "table", "line", "ring", "rings"].includes(f.base) ? ` <button class="x" data-act="rm" data-p="${esc(p)}" title="Make it none">×</button>` : ""}</div>`;
  }
  function getPath(o, p) { return p.split(".").reduce((a, k) => (a == null ? undefined : a[k]), o); }
  function setPath(o, p, v) {
    const ks = p.split("."), last = ks.pop(), par = ks.reduce((a, k) => a[k], o);
    if (v === undefined) { if (Array.isArray(par)) par.splice(+last, 1); else delete par[last]; }
    else par[last] = v;
  }
  function parseVal(el) {
    const b = el.dataset.b, raw = el.value.trim();
    const cs = b === "cell" ? spec(el.dataset.a) : null, base = cs ? cs.base : b;
    if (raw === "" && base !== "enums") return { v: b === "cell" ? null : undefined };
    if (base === "num" || base === "int") { const n = Number(raw); return isFinite(n) ? { v: n } : { err: `"${raw}" isn't a number` }; }
    if (base === "nums") { const L = raw.split(/[\s,]+/).filter(Boolean).map(Number); return L.every(isFinite) ? { v: L } : { err: "Numbers only, with a comma between" }; }
    if (base === "bool") return { v: raw === "true" };
    if (base === "hex") return { v: raw.toLowerCase() };
    if (base === "hexes" || base === "strs") return { v: raw.split(",").map((x) => x.trim()).filter(Boolean).map((x) => (base === "hexes" ? x.toLowerCase() : x)) };
    return { v: raw };
  }
  async function onField(el) {
    if (!sel) return;
    const r = clone(sel), p = el.dataset.p, b = el.dataset.b;
    let v;
    if (b === "enums") v = [...$("panel").querySelectorAll(`input[data-p="${CSS.escape(p)}"]`)].filter((x) => x.checked).map((x) => x.value);
    else if (b === "pt" || b === "pt3") {
      const ins = [...$("panel").querySelectorAll(`input[data-p="${CSS.escape(p)}"]`)], vals = ins.map((x) => x.value.trim());
      if (vals.every((x) => x === "")) v = undefined;
      else if (vals.every((x) => x !== "" && isFinite(Number(x)))) v = vals.map(Number);
      else return;   // wait for the other numbers
    } else { const q = parseVal(el); if (q.err) { toast(q.err); return; } v = q.v; }
    setPath(r, p, v);
    await save([r]);
  }
  async function onAct(btn) {
    if (!sel) return;
    const r = clone(sel), p = btn.dataset.p, a = btn.dataset.a, act = btn.dataset.act;
    if (act === "add") setPath(r, p, btn.dataset.k === "table" ? { cols: SCHEMA.tables[a].map(([c]) => c), rows: [] } : defaults(SCHEMA.shapes[a]));
    else if (act === "push") { const L = getPath(r, p) || []; L.push(defaults(SCHEMA.shapes[a])); setPath(r, p, L); }
    else if (act === "row") { const t = getPath(r, p); t.rows.push(t.cols.map(() => null)); }
    else if (act === "rm") setPath(r, p, undefined);
    await save([r]);
  }
  const HELP = `<div id="help"><b>Select</b> (V): click a record; drag to move; drag a square handle to move a corner, a round one to add a corner, <kbd>⌥</kbd>-click a corner to remove it. <kbd>R</kbd>/<kbd>Shift R</kbd> turn 15°, <kbd>[</kbd> <kbd>]</kbd> 1°. <kbd>Delete</kbd> removes, <kbd>⌘Z</kbd> undoes. Drag empty ground, the right button or <kbd>Space</kbd> to pan.<br><br><b>Street</b> (S): click points, <kbd>Enter</kbd> or double-click to finish; points snap onto the map's roads (a shared point joins them) and, with "Snap to real roads", onto the real line under it. <kbd>Shift</kbd> places freely. <b>Building</b> (B), <b>Plot</b> (P), <b>Place</b> (A): drag a box. <b>Wall</b> (W): click points, <kbd>Enter</kbd>. <b>Gate</b> (G): click a wall twice, at each end. <b>Lean-to</b> (L): click a building side or a wall twice; on a wall it stands on the right of the wall's line ("Put it on the other side" turns the line round). <b>Tree</b> (T), <b>Furniture</b> (F): click. <b>Surface</b> (U): click a road. <b>Frontage</b> (E): click a plot's side that faces a street; it finds the street, the side and the setback. <b>Stamp</b> (K): copy records with everything on them, from the map or a source, and place copies.<br><br><b>The dress layer.</b> <b>Face</b> (C): click a building's side to open it in the face editor (or a Face button in a building's panel). <b>Goods</b> (O): click inside a lean-to, stall, heap or bin to put an item there. <b>Litter</b> (X): click to drop a piece (it joins the litter record you picked, or one within 5 m). With a piece picked, the next one takes its values except where it lies. Drag a piece to move it, <kbd>Delete</kbd> removes just it; its row is lit in the panel's table. <b>Ground</b> (D): click points, <kbd>Enter</kbd>: a painted patch, over the earlier ones. <b>Relief</b> (H): drag a box for a flat grid; click a cell to raise it 10 mm (<kbd>Shift</kbd> 50), <kbd>⌥</kbd>-click to lower.<br><br><b>Brush</b> (N): pick litter, goods (on the ground or hung), relief or ground paint in the kind list; size, spacing and each value in the panel (unset, a value, random between two, or random from a list). Every stroke writes full rows (litter pieces, goods items, relief cells, a ground patch's outline), editable one by one; <kbd>⌥</kbd>-drag erases (relief: lowers); <kbd>[</kbd> <kbd>]</kbd> size; <kbd>⌘Z</kbd> undoes a whole stroke. <b>Person</b> (I): a person spot, where someone does something and when: click to place it (the activity from the kind list), drag to face them; it links to the stall, lean-to, vehicle, furniture or heap it stands at and moves and turns with it; hours, count and the rest in the panel. <b>Clock</b> (top bar): drag it to an hour and the spots out then stay bright, the rest go faint. <b>Wire</b> (J): click a pole, then another pole (a line) or a house side or wall (a drop, tied at the height in the top bar); <kbd>Shift</kbd> goes on from the last pole.<br><br>Every field shows its value; one in red needs a value (nothing is filled in for you). Outlines: <span style="color:var(--warn)">dashed amber</span> = fields still to set, <span style="color:var(--bad)">red</span> = a problem (check_map.py runs on every save, plus a house on a road or on another house).</div>`;
  function showPanel() {
    const P = $("panel"); if (!SCHEMA || !P) return;
    const keep = P.scrollTop;
    const o = sel;
    if (tool === "brush") { P.innerHTML = brushHTML() + "<hr>" + HELP; P.scrollTop = keep; return; }
    if (!o && tool === "stamp") {
      const opts = SOURCES.flatMap((x) => x.districts.map((d) => [x.src + "|" + d, (x.src === "map" ? "the map" : x.src) + " · " + d]));
      const G = picked.length ? groupOf(picked) : [], cnt = {}; for (const r of G) cnt[r.type] = (cnt[r.type] || 0) + 1;
      P.innerHTML = `<h3>Stamp</h3><div class="fld"><span class="fk">copy from</span><select id="msrc"><option value="">— pick a source —</option>${opts.map(([v, l]) => `<option value="${esc(v)}"${v === srcKey ? " selected" : ""}>${esc(l)}</option>`).join("")}</select></div>`
        + (SRC ? `<div class="row"><button id="msrcgo">Show the source</button></div><p class="k">${SRC.recs.size} records in ${esc(SRC.src)}/${SRC.d}${SRC.src === "map" ? "" : ", drawn in purple where they lie"}.</p>` : "")
        + (G.length ? `<p><b>${placing ? "Placing" : "Picked"}</b>: ${Object.entries(cnt).map(([t, n]) => `${n} ${t}`).join(", ")}${placing ? ` · turned ${stampDeg}°` : ""}</p>${placing ? "" : `<div class="row"><button id="mplace">Place it (Enter)</button></div>`}` : "")
        + `<p class="k">Click a record to copy it with everything on it (faces, roof sheets, lean-tos, goods, wires); <kbd>Shift</kbd>-click to pick more, then <kbd>Enter</kbd>; or drag a box. Then click on the map to put a copy down, and again for another. <kbd>R</kbd>, <kbd>[</kbd> <kbd>]</kbd> turn it; <kbd>Esc</kbd> stops.</p><p class="k">Each copy holds the full values with new ids and a "from" note, never a link to the source. A link to something outside the copy (its plot, its street) is left for you to set again; a building takes the plot it lands in.</p>`;
      $("msrc").addEventListener("change", (ev) => loadSrc(ev.target.value));
      const go = $("msrcgo"); if (go) go.addEventListener("click", () => { const W = srcW(), Pp = W.list(null).flatMap((r) => allPts(r, W.get)); if (Pp.length) V.fit(bboxOf(Pp), 60); });
      const pl = $("mplace"); if (pl) pl.addEventListener("click", startPlacing);
      return;
    }
    if (!o && tool === "wire") {
      P.innerHTML = `<h3>Wire</h3><p class="k">Click a pole, then the other pole: a line between them. Or click a pole, then a house side or a wall: a drop to the house, tied at the height in the top bar ("tied at"). <kbd>Shift</kbd>-click the second pole to go on from it. <kbd>Esc</kbd> stops. The kind comes from the list (line to a pole, service to a house, unless you pick one); wires in the run (n) and the sag are yours to set in the panel.</p><hr>` + HELP;
      P.scrollTop = keep; return;
    }
    if (!o) {
      let h = `<h3>${tool === "select" ? "Nothing selected" : "Drawing: " + tool}</h3>`;
      if (!cur) h += `<p class="k">Pick the district to draw in, under "Draw in". Its outline comes from the frame study; everything else is drawn by hand.</p>`;
      else if (!started.has(cur)) { const S = studyD(cur); h += `<p><b>${cur}</b> (study: ${esc(S ? S.name : "?")}) isn't started.</p><p class="k">Starting it writes map/${cur}/district.json with its number and its outline from the frame study, and an empty plan. Its name stays empty for you to give.</p><div class="row"><button id="mstart">Start ${cur}</button></div>`; }
      else if (DS.has(cur)) {
        const D = DS.get(cur), dr = D.recs.get(cur), n = D.recs.size - 1, bad = [...D.recs.values()].filter((r) => badness(r) === "bad").length, inc = [...D.recs.values()].filter((r) => badness(r) === "incomplete").length;
        h += `<p><b>${cur}</b>: ${n} record${n === 1 ? "" : "s"} · ${inc} with fields to set · ${bad} with problems</p>${D.file.length ? `<p class="bad">${D.file.map(esc).join("<br>")}</p>` : ""}<div class="row"><button id="mcheck">Check ${cur}</button><button id="mseld">The district record</button></div>`;
        void dr;
      }
      P.innerHTML = h + "<hr>" + HELP;
      const st = $("mstart"); if (st) st.addEventListener("click", () => start(cur));
      const ck = $("mcheck"); if (ck) ck.addEventListener("click", async () => { const j = await api("/api/map/check", { d: cur }); if (j) { setProblems(cur, j.problems); toast(j.problems.length ? `${j.problems.length} problem${j.problems.length > 1 ? "s" : ""} in ${cur}` : `${cur} passes check_map.py`); V.draw(); showPanel(); } });
      const sd = $("mseld"); if (sd) sd.addEventListener("click", () => { sel = rec(cur); showPanel(); V.draw(); });
      return;
    }
    const d = dOf.get(o.id), probs = probsOf(o), bb = boardBad.get(o.id);
    let h = `<h3>${esc(o.type)}${o.kind ? ": " + esc(o.kind) : ""}</h3><p class="k">${esc(o.id)} · in ${d}</p>`;
    if (bb) h += `<p class="bad">⚠ ${esc(bb)}</p>`;
    if (probs.length) h += `<div class="probs">${probs.map((q) => `<div class="${isMissing(q) ? "warn" : "bad"}">${esc((q.field ? q.field + ": " : "") + q.msg)}</div>`).join("")}</div>`;
    else if (!bb) h += `<p class="ok">check_map.py: no problems</p>`;
    if (o.type === "building" && Array.isArray(o.footprint) && o.footprint.length === 4) {
      const fp = o.footprint, c = centroid(fp), w = dist(fp[0], fp[1]), dep = dist(fp[1], fp[2]), ang = Math.atan2(fp[1][1] - fp[0][1], fp[1][0] - fp[0][0]) * 180 / Math.PI;
      h += `<fieldset><legend>Exact size and place</legend><div class="fld"><span class="fk">width, depth (m)</span><span class="ptrow"><input id="nw" type="number" step="0.1" value="${w.toFixed(2)}"><input id="nd" type="number" step="0.1" value="${dep.toFixed(2)}"></span></div><div class="fld"><span class="fk">angle (°)</span><input id="na" type="number" step="1" value="${ang.toFixed(1)}"></div><div class="fld"><span class="fk">middle x, y</span><span class="ptrow"><input id="nx" type="number" step="0.1" value="${c[0].toFixed(2)}"><input id="ny" type="number" step="0.1" value="${c[1].toFixed(2)}"></span></div><p class="k">Face 0 runs from the first corner to the second.</p></fieldset>`;
    }
    const fb = o.type === "building" ? o : o.type === "faces" ? rec(o.of) : null;
    if (fb && Array.isArray(fb.footprint) && fb.footprint.length > 2) { const fc = recsOf(["faces"]).find((r) => r.of === fb.id); h += `<fieldset><legend>Faces: open one in the face editor</legend><div class="chips">${fb.footprint.map((_, i) => `<button data-face="${i}">Face ${i}${fc && (fc.faces || []).some((f) => f.face === i) ? " ●" : ""}</button>`).join("")}</div></fieldset>`; }
    const kids = recsOf(null).filter((c) => c.of === o.id || c.against === o.id), par = o.of && rec(o.of), host = o.type === "leanto" && rec(o.against);
    if (kids.length) h += `<fieldset><legend>On it</legend><div class="chips">${kids.map((c) => `<button data-go="${c.id}">${esc(c.type)} ${c.id}</button>`).join("")}</div></fieldset>`;
    if (par) h += `<div class="row"><button data-go="${par.id}">It dresses ${esc(par.type)} ${par.id}</button></div>`;
    if (host && Array.isArray(host.line)) h += `<div class="row"><button id="mflip" title="It stands on the right of its ${host.type}'s line; this turns the line round, keeping gates and lean-tos where they are">Put it on the other side</button></div>`;
    const F0 = fieldsOf(o.type);
    h += Object.entries(F0).filter(([k]) => !["id", "type", "ref", "from"].includes(k)).map(([k, sp]) => fieldHTML(k, sp, o[k], k)).join("");
    for (const k of ["ref", "from"]) if (o[k]) h += `<div class="fld"><span class="fk">${k}</span><code>${esc(JSON.stringify(o[k]))}</code></div>`;
    h += `<div class="row">${"turn" in F0 || editPts(o) ? `<button id="mrl">⟲ 15°</button><button id="mrr">⟳ 15°</button>` : ""}${o.type !== "district" ? `<button id="mdel">Delete</button>` : ""}</div><hr>` + HELP;
    P.innerHTML = h; P.scrollTop = keep;
    const on1 = P.querySelector("tr.on"); if (on1) on1.scrollIntoView({ block: "nearest" });
    const on = (id, fn) => { const e = $(id); if (e) e.addEventListener("click", fn); };
    on("mrl", () => turnSel(-15)); on("mrr", () => turnSel(15)); on("mdel", () => del(o)); on("mflip", () => flipSide(o));
    if ($("nw")) ["nw", "nd", "na", "nx", "ny"].forEach((id) => $(id).addEventListener("change", async () => {
      const [w, dep, a, x, y] = ["nw", "nd", "na", "nx", "ny"].map((i) => parseFloat($(i).value));
      if (![w, dep, a, x, y].every(isFinite) || w < 0.5 || dep < 0.5) { toast("Size needs numbers of at least 0.5 m"); showPanel(); return; }
      const q = clone(o); q.footprint = orient(rectFrom(w, dep, a, x, y)); await save([q]);
    }));
  }
  async function flipSide(lt) {   // a lean-to stands on the right of its wall's line: turn the line round to move it across
    const host = rec(lt.against); if (!host || !Array.isArray(host.line)) return;
    if (recsOf(null).some((c) => c.of === host.id)) { toast(`${host.id} is dressed already (wall bays or posters): its line can't turn round under them`); return; }
    const L = lineLen(host.line), q = clone(host), fl = (o) => { if (isFinite(o.u0) && isFinite(o.u1)) { const a = o.u0; o.u0 = r2(Math.max(0, L - o.u1)); o.u1 = r2(L - a); } };
    q.line = host.line.slice().reverse();
    if (q.wall && Array.isArray(q.wall.gates)) q.wall.gates.forEach(fl);
    const lts = recsOf(["leanto"]).filter((x) => x.against === host.id).map((x) => { const y = clone(x); fl(y); return y; });
    if (await save([q, ...lts])) toast(`${host.id}'s line turned round: its lean-to${lts.length > 1 ? "s" : ""} now stand${lts.length > 1 ? "" : "s"} on the other side`);
  }
  async function turnSel(deg) {   // its person spots turn with it, round the same middle
    if (!sel) return; const q = turnRec(sel, deg); if (!q) return;
    const e = editPts(sel), c = Array.isArray(sel.at) ? sel.at : e && e.pts.length > 1 ? centroid(e.closed ? e.pts : [e.pts[0], e.pts[e.pts.length - 1]]) : null;
    await save([q, ...(c ? followers(sel).map((f) => transformed(f, mover(c, c, deg))) : [])]);
  }
  const followers = (o) => (o && o.type !== "person_spot" ? recsOf(["person_spot"]).filter((f) => f.parent === o.id) : []);   // person spots that belong to o move and turn with it

  // ------------------------------------------------------------------ status, the bar, keys
  let probI = 0;
  function renderStatus() {
    let el = $("mapstat");
    if (!el) { el = document.createElement("div"); el.id = "mapstat"; el.style.cursor = "pointer"; el.title = "Go to the next record with a problem or a field to set"; $("status").appendChild(el); el.addEventListener("click", nextProblem); }
    if (!SERVER) { el.innerHTML = `<b style="color:var(--bad)">Read-only: no board server</b>`; return; }
    let n = 0, inc = 0, bad = 0;
    for (const D of DS.values()) for (const r of D.recs.values()) { n++; const b = badness(r); if (b === "bad") bad++; else if (b === "incomplete") inc++; }
    el.innerHTML = `Map: ${started.size} district${started.size === 1 ? "" : "s"} started · ${n} records loaded · <b style="color:${inc ? "var(--warn)" : "inherit"}">${inc}</b> to finish · <b style="color:${bad ? "var(--bad)" : "inherit"}">${bad}</b> with problems${lastMsg ? " · " + lastMsg : ""}`;
  }
  function nextProblem() {
    const L = []; for (const D of DS.values()) for (const r of D.recs.values()) if (badness(r) && r.type !== "district") L.push(r);
    if (!L.length) { toast("No records with problems or fields to set"); return; }
    const r = L[probI++ % L.length], P = allPts(r); sel = r; toast(`${(probI - 1) % L.length + 1} of ${L.length}: ${r.id}`);
    if (P.length) { const c = centroid(P); V.focus(c[0], c[1], 6); } showPanel();
  }
  function fillPicker() {
    const s = $("mdist"); if (!s) return;
    s.innerHTML = `<option value="">Draw in…</option>` + F.districts.map((x) => `<option value="${dId(x.n)}"${dId(x.n) === cur ? " selected" : ""}>${dId(x.n)} · ${esc(x.name)}${started.has(dId(x.n)) ? " ✓" : ""}</option>`).join("");
  }
  function buildBar() {
    const st = document.createElement("style");
    st.textContent = `#panel .fld{display:grid;grid-template-columns:38% 1fr auto;gap:4px;align-items:center;margin:3px 0}#panel .fk{color:var(--muted);overflow-wrap:anywhere}#panel .fk.bad{color:var(--bad);font-weight:600}#panel fieldset{border:1px solid var(--panel-line);border-radius:6px;margin:6px 0;padding:4px 6px}#panel fieldset.item{border-style:dashed}#panel legend{font-size:12px}#panel select{font:inherit;color:var(--ink);background:var(--paper);border:1px solid var(--panel-line);border-radius:6px;padding:3px 4px;width:100%}#panel .chk{display:flex;flex-wrap:wrap;gap:2px 8px}#panel .chk label{display:flex;gap:3px;align-items:center}#panel .ptrow,#panel .hexrow{display:flex;gap:4px}#panel .hexrow input[type=color]{width:34px;padding:0;height:26px}#panel .tb input{padding:2px 3px}#panel .tb th{font-weight:500;color:var(--muted);text-align:left}#panel .x{padding:1px 6px}#panel .probs{margin:4px 0 8px;font-size:12px}#panel .probs .warn{color:var(--warn)}#panel .probs .bad{color:var(--bad)}#panel code{font-size:11px;overflow-wrap:anywhere}#panel{width:360px}#panel .chips{display:flex;flex-wrap:wrap;gap:4px}#panel .chips button{font-size:11px}#panel .tb tr.on input{outline:2px solid var(--sel)}#panel .tbw{overflow-x:auto}#panel fieldset{min-width:0}#panel .tb input{min-width:44px}.bar{right:392px}#mtools{flex-wrap:wrap}#panel .brc{display:grid;grid-template-columns:30% 1fr;gap:3px 4px;align-items:center;margin:3px 0}#panel .brc .bri{grid-column:1/3}#panel .fk.unset{color:var(--warn)}`;
    document.head.appendChild(st);
    const bar = document.querySelector(".bar");
    bar.insertAdjacentHTML("beforeend", `<div class="group"><select id="mdist" aria-label="District to draw in"></select></div><div class="group" id="mtools">${TOOLS.map(([t, l, k, tip]) => `<button data-tool="${t}" title="${tip} (${k})">${l}</button>`).join("")}</div><div class="group"><select id="mkind" aria-label="Kind"></select><label id="msnap" title="While drawing a street, snap onto the real road line under it"><input type="checkbox"${snapReal ? " checked" : ""}> Snap to real roads</label><label id="mwirezl" title="How high a drop to a house meets the house or wall (m)">tied at <input id="mwirez" type="number" step="0.1" min="0" style="width:52px" placeholder="m"></label><label title="Show the new map's records"><input type="checkbox" id="mon" checked> Map</label></div><div class="group" title="The clock: person spots out at this hour stay bright, the rest go faint"><label><input type="checkbox" id="mclock"> Clock</label><input type="range" id="mclockh" min="0" max="23.5" step="0.5" value="${clockH}" style="width:110px"><span id="mclockt" class="k">${hhmm(clockH)}</span></div>`);
    document.querySelectorAll("#mtools button").forEach((b) => b.addEventListener("click", () => setTool(b.dataset.tool)));
    $("mkind").addEventListener("change", () => { if (tool === "brush") { BR.mode = $("mkind").value; saveBR(); showPanel(); V.draw(); } });
    $("msnap").querySelector("input").addEventListener("change", (ev) => { snapReal = ev.target.checked; try { localStorage.setItem("gidi-map-snapreal", snapReal ? "1" : "0"); } catch (e) {} });
    $("mon").addEventListener("change", (ev) => { MAPON = ev.target.checked; V.draw(); });
    $("mwirez").value = wireZ; $("mwirez").addEventListener("change", (ev) => { wireZ = ev.target.value.trim(); try { localStorage.setItem("gidi-map-wirez", wireZ); } catch (e) {} });
    const clockShow = () => { const n = recsOf(["person_spot"]), out = n.filter((r) => outAt(r, clockH)); $("mclockt").textContent = hhmm(clockH) + (clockOn ? ` · ${out.length} of ${n.length} out` : ""); V.draw(); };
    $("mclock").addEventListener("change", (ev) => { clockOn = ev.target.checked; clockShow(); });
    $("mclockh").addEventListener("input", (ev) => { clockH = Number(ev.target.value); if (!clockOn) { clockOn = true; $("mclock").checked = true; } clockShow(); });
    $("mdist").addEventListener("change", (ev) => {
      cur = ev.target.value || null; try { localStorage.setItem("gidi-map-district", cur || ""); } catch (e) {}
      sel = null; const S = cur && studyD(cur); if (S) V.fit(S.bb, 60);
      if (cur && started.has(cur) && !DS.has(cur)) load(cur);
      showPanel(); V.draw();
    });
    const P = $("panel");
    P.style.display = "";
    P.addEventListener("change", (ev) => { const el = ev.target; if (el.dataset.br) { brushField(el); return; } if (el.type === "color" && el.dataset.for) { const t = P.querySelector(`input[data-p="${CSS.escape(el.dataset.for)}"]:not([type=color])`); if (t) { t.value = el.value; onField(t); } return; } if (el.dataset.p) onField(el); });
    P.addEventListener("click", (ev) => {
      const g = ev.target.closest("button[data-go]"); if (g) { sel = rec(g.dataset.go); const Q = sel && allPts(sel); if (Q && Q.length && !hit(bboxOf(Q), V.view())) { const c = centroid(Q); V.focus(c[0], c[1], V.s); } showPanel(); V.draw(); return; }
      const fc = ev.target.closest("button[data-face]"); if (fc && sel) { openFace(sel.type === "faces" ? rec(sel.of) : sel, +fc.dataset.face); return; }
      const b = ev.target.closest("button[data-act]"); if (b) { ev.preventDefault(); onAct(b); }
    });
    window.addEventListener("keydown", (ev) => {
      if (/^(INPUT|SELECT|TEXTAREA)$/.test(ev.target.tagName)) return;
      if (window.FACEEDIT && window.FACEEDIT.isOpen()) return;   // the face editor has the keys
      if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === "z") { ev.preventDefault(); undo(); return; }
      if (ev.metaKey || ev.ctrlKey) return;
      const k = ev.key.toLowerCase();
      if (k === "escape") { if (placing || picked.length) { placing = null; picked = []; showPanel(); V.draw(); return; } linePts = []; ghost = null; drag = null; firstClick = null; wireFrom = null; if (tool !== "select") setTool("select"); else { sel = null; showPanel(); } V.draw(); }
      else if (placing && (k === "r" || k === "[" || k === "]")) { stampDeg += k === "r" ? (ev.shiftKey ? -15 : 15) : k === "[" ? -1 : 1; V.draw(); }
      else if (k === "enter" && tool === "stamp" && picked.length && !placing) startPlacing();
      else if (k === "enter" && (tool === "street" || tool === "wall" || tool === "ground")) finishLine();
      else if (k === "backspace" || k === "delete") {
        ev.preventDefault();
        if ((tool === "street" || tool === "wall" || tool === "ground") && linePts.length) { linePts.pop(); V.draw(); }
        else if (rowSel()) { const q = clone(sel); q[selRow.t].rows.splice(selRow.i, 1); selRow = null; save([q]); }   // just the piece
        else if (sel && sel.type !== "district") del(sel);
      }
      else if (tool === "brush" && (k === "[" || k === "]")) { BR.size = r2(Math.max(0.1, Math.min(50, BR.size * (k === "]" ? 1.25 : 0.8)))); saveBR(); showPanel(); V.draw(); }
      else if (k === "r") turnSel(ev.shiftKey ? -15 : 15);
      else if (k === "[") turnSel(-1); else if (k === "]") turnSel(1);
      else { const t = TOOLS.find((x) => x[2].toLowerCase() === k); if (t) setTool(t[0]); }
    });
  }
  let toastT;
  function toast(t) { const e = $("toast"); if (!e) return; e.textContent = t; e.style.display = "block"; clearTimeout(toastT); toastT = setTimeout(() => (e.style.display = "none"), 3500); }

  async function init(view) {
    V = view; F = view.F;
    buildBar();
    try { SCHEMA = await (await fetch("../schema/map_schema.json", { cache: "no-store" })).json(); } catch (e) { toast("Couldn't read schema/map_schema.json"); return; }
    try { cur = localStorage.getItem("gidi-map-district") || null; } catch (e) {}
    setTool("select");
    await loadList();
    await loadSources();
    fillPicker();
    if (cur && started.has(cur)) load(cur);
    showPanel(); V.draw();
  }
  return { init, drawWorld, drawScreen, down, move, up, get state() { return { DS, dOf, sel, cur, tool, SOURCES, SRC, picked }; } };
})();
