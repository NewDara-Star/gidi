/* The new map's editor on the drawing board's new frame (board.html?frame=new; docs/MAP-FORMAT.md). Draws and saves the
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
  const GEOM = { road: "centreline", plot: "outline", building: "footprint", wall: "line", frontage: "line", place: "area", district: "outline" };
  const POINTY = new Set(["stall", "pole", "tree", "vehicle", "furniture", "heap"]);
  function editPts(r) {   // the points a handle edits, and whether they close
    if (!r) return null;
    if (r.type === "road" && Array.isArray(r.centreline)) return { pts: r.centreline, closed: false, set: (q, P) => { q.centreline = P; } };
    if ((r.type === "wall" || r.type === "frontage") && Array.isArray(r.line)) return { pts: r.line, closed: false, set: (q, P) => { q.line = P; } };
    if (r.type === "building" && Array.isArray(r.footprint)) return { pts: r.footprint, closed: true, set: (q, P) => { q.footprint = P; } };
    if (r.type === "plot" && Array.isArray(r.outline)) return { pts: r.outline, closed: true, set: (q, P) => { q.outline = P; } };
    if (r.type === "place" && Array.isArray(r.area) && r.area[0]) return { pts: r.area[0], closed: true, set: (q, P) => { q.area = [P, ...q.area.slice(1)]; } };
    return null;
  }
  function allPts(r) { const e = editPts(r); if (e) return e.pts; if (Array.isArray(r.at)) return [r.at]; const q = leantoQuad(r); return q || []; }
  function moveRec(r, dx, dy) {   // the whole record shifted, every point (heights kept)
    const mv = (p) => [r2(p[0] + dx), r2(p[1] + dy), ...p.slice(2)];
    const q = clone(r);
    if (q.type === "place") q.area = q.area.map((ring) => ring.map(mv));
    else if (GEOM[q.type] && Array.isArray(q[GEOM[q.type]])) q[GEOM[q.type]] = q[GEOM[q.type]].map(mv);
    if (Array.isArray(q.at)) q.at = mv(q.at);
    return q;
  }
  function turnRec(r, deg) {
    const q = clone(r);
    if ("turn" in fieldsOf(q.type) && Array.isArray(q.at)) { q.turn = Math.round(((q.turn || 0) + deg) * 100) / 100; return q; }
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
  function newId(type) {
    const pre = SCHEMA.records[type].prefix, abc = "abcdefghijklmnopqrstuvwxyz0123456789";
    for (;;) { const b = new Uint8Array(8); crypto.getRandomValues(b); const id = pre + "-" + [...b].map((x) => abc[x % 36]).join(""); if (!dOf.has(id)) return id; }
  }
  function setProblems(d, list) {
    const D = DS.get(d); if (!D) return;
    D.probs = new Map(); D.file = [];
    for (const p of list || []) { if (p.id) { if (!D.probs.has(p.id)) D.probs.set(p.id, []); D.probs.get(p.id).push(p); } else D.file.push(p.where + ": " + p.msg); }
  }
  function setRecords(d, records, problems) {
    const old = DS.get(d); if (old) for (const id of old.recs.keys()) dOf.delete(id);
    const D = { recs: new Map(), probs: new Map(), file: [] }; DS.set(d, D);
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
    if (j.exists) setRecords(d, j.records, j.problems); else started.delete(d);
    V.draw(); showPanel();
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
    const j = await api("/api/map/delete", { d, id: r.id });
    if (!j) return;
    DS.get(d).recs.delete(r.id); dOf.delete(r.id); setProblems(d, j.problems);
    if (sel && sel.id === r.id) sel = null; lastMsg = "Deleted"; V.draw(); showPanel();
  }
  async function undo() {
    const j = await api("/api/map/undo", {});
    if (!j) return;
    setRecords(j.d, j.records, j.problems); sel = sel && rec(sel.id); toast("Undone"); lastMsg = "Undone"; V.draw(); showPanel();
  }
  async function start(d) {
    const j = await api("/api/map/start", { d });
    if (!j) return;
    started.add(d); setRecords(d, j.records, j.problems); fillPicker(); toast(`Started ${d}: its outline is from the frame study; its name is still to give`); V.draw(); showPanel();
  }

  // ------------------------------------------------------------------ problems: the checker's, and a few the board sees on its own
  const isMissing = (p) => /^missing field/.test(p.msg);
  function boardProblems(v) {   // a house on a road or on another house, a wall across a road
    const bad = new Map();
    const roads = recsOf(["road"]).filter((r) => Array.isArray(r.centreline) && r.centreline.length > 1 && r.width > 0);
    const bs = recsOf(["building"]).filter((b) => Array.isArray(b.footprint) && b.footprint.length > 2 && hit(bboxOf(b.footprint), v));
    if (V.s < 0.5) return bad;
    const onRoad = (fp, r) => {   // the carriageway (half the width each side of the centreline) reaches into the footprint
      const c = r.centreline, half = r.width / 2 - 0.05;
      if (c.some((p) => inPoly(p, fp))) return true;
      for (let i = 1; i < c.length; i++) for (let j = 0; j < fp.length; j++) { const q = fp[j], q2 = fp[(j + 1) % fp.length]; if (segsCross(c[i - 1], c[i], q, q2) || segDist(q, c[i - 1], c[i]) < half || segDist(c[i - 1], q, q2) < half || segDist(c[i], q, q2) < half) return true; }
      return false;
    };
    for (const b of bs) {
      for (const r of roads) if (onRoad(b.footprint, r)) { bad.set(b.id, "on the road " + r.id); break; }
      if (!bad.has(b.id)) for (const o of bs) if (o !== b && polysOverlap(b.footprint, o.footprint)) { bad.set(b.id, "overlaps " + o.id); break; }
    }
    for (const w of recsOf(["wall"])) if (Array.isArray(w.line) && w.line.length > 1) for (const r of roads) { const half = r.width / 2 - 0.05; if (w.line.some((p, i) => i && r.centreline.some((q, j) => j && (segsCross(w.line[i - 1], p, r.centreline[j - 1], q) || segDist(p, r.centreline[j - 1], q) < half)))) { bad.set(w.id, "across the road " + r.id); break; } }
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
  const TOOLS = [["select", "Select", "V", "Select, move, turn, delete"], ["street", "Street", "S", "A road, street, lane or path: click points, Enter to finish"], ["building", "Building", "B", "Drag a box"], ["plot", "Plot", "P", "Drag a box"], ["wall", "Wall", "W", "Click points, Enter to finish"], ["gate", "Gate", "G", "Click a wall where the gate starts, then where it ends"], ["leanto", "Lean-to", "L", "Click a building side (or a wall) where it starts, then where it ends"], ["tree", "Tree", "T", "Click to plant"], ["furniture", "Furniture", "F", "Stalls, poles, parked vehicles, furniture, heaps: click to place"], ["place", "Place", "A", "What the game uses a spot for: drag a box"], ["surface", "Surface", "U", "Click a road to give it the surface"]];
  const KINDS = () => ({
    street: SCHEMA.enums.road_kind.map((k) => [k, k]), building: SCHEMA.enums.house_type.map((k) => [k, k]), plot: SCHEMA.enums.plot_kind.map((k) => [k, k]),
    tree: SCHEMA.enums.tree_kind.map((k) => [k, k]), place: SCHEMA.enums.place_kind.map((k) => [k, k]), surface: SCHEMA.enums.road_surface.map((k) => [k, k]),
    furniture: [["stall", "stall_kind"], ["pole", "pole_kind"], ["vehicle", "vehicle_kind"], ["furniture", "furniture_kind"], ["heap", "heap_kind"]].map(([t, e]) => [t, SCHEMA.enums[e].map((k) => [t + ":" + k, k])]),
  });
  let tool = "select", sel = null, hover = null, ghost = null, drag = null, linePts = [], cursor = null, snapAt = null, firstClick = null;
  let snapReal = true;
  try { snapReal = localStorage.getItem("gidi-map-snapreal") !== "0"; } catch (e) {}
  function setTool(t) {
    if (!SCHEMA) return;
    tool = t; linePts = []; ghost = null; firstClick = null; snapAt = null;
    document.querySelectorAll("#mtools button").forEach((b) => b.classList.toggle("on", b.dataset.tool === t));
    const ks = $("mkind"), K = KINDS()[t];
    ks.innerHTML = !K ? "" : t === "furniture" ? K.map(([g, L]) => `<optgroup label="${g}">${L.map(([v, l]) => `<option value="${v}">${l}</option>`).join("")}</optgroup>`).join("") : K.map(([v, l]) => `<option value="${v}">${l}</option>`).join("");
    ks.style.display = K ? "" : "none";
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
  function leantoQuad(r) {
    if (r.type !== "leanto") return null;
    const host = rec(r.against); if (!host || !(r.u1 > r.u0)) return null;
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
  const thingR = (r) => r.type === "tree" ? (r.kind === "palm" ? 2.5 : r.kind === "shrub" ? 1 : 3.5) : r.type === "heap" ? (r.r > 0 ? r.r : 1) : 0.3;
  function pick(p) {
    const tol = Math.max(0.5, 7 / V.s);
    let best = null, bd = tol;
    for (const r of recsOf([...POINTY])) { if (!Array.isArray(r.at)) continue; const q = thingPts(r); const d = q && inPoly(p, q) ? 0 : dist(p, r.at) - (r.type === "tree" || r.type === "heap" ? Math.min(thingR(r), 1.2) : 0); if (d < bd) { bd = d; best = r; } }
    if (best) return best;
    for (const r of recsOf(["leanto"])) { const q = leantoQuad(r); if (q && inPoly(p, q)) return r; }
    const bs = recsOf(["building"]).filter((b) => Array.isArray(b.footprint) && b.footprint.length > 2 && inPoly(p, b.footprint));
    if (bs.length) return bs.sort((a, b) => Math.abs(signedArea(a.footprint)) - Math.abs(signedArea(b.footprint)))[0];
    bd = Math.max(0.4, 6 / V.s);
    for (const r of recsOf(["wall", "frontage"])) { if (!Array.isArray(r.line)) continue; const d = lineDist(p, r.line); if (d < bd) { bd = d; best = r; } }
    if (best) return best;
    let rd = 1e9;
    for (const r of recsOf(["road"])) { if (!Array.isArray(r.centreline)) continue; const d = lineDist(p, r.centreline); if (d < Math.max((r.width || 0) / 2, 6 / V.s) && d < rd) { rd = d; best = r; } }
    if (best) return best;
    const pl = recsOf(["plot"]).filter((r) => Array.isArray(r.outline) && r.outline.length > 2 && inPoly(p, r.outline));
    if (pl.length) return pl.sort((a, b) => Math.abs(signedArea(a.outline)) - Math.abs(signedArea(b.outline)))[0];
    return recsOf(["place"]).find((r) => Array.isArray(r.area) && r.area.some((ring) => ring.length > 2 && inPoly(p, ring))) || null;
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
      const o = pick(p); sel = o; showPanel(); V.draw();
      if (o) { drag = { o, start: p, moved: false, before: clone(o) }; return true; }
      return false;   // empty ground: frame.js pans
    }
    if (tool === "street" || tool === "wall") {
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
  function move(ev, p) {
    cursor = p;
    if (drag && drag.vtx !== undefined) {
      let q;
      if (drag.obj.type === "road" && (drag.vtx === 0 || drag.vtx === drag.pts.length - 1)) { const sn = snapPt(p, drag.obj, ev); q = sn.p; drag.snap = sn; snapAt = sn.on || sn.real ? sn.p : null; }
      else q = drag.obj.type === "road" ? [r2(p[0]), r2(p[1])] : cornerSnap(p, drag.obj, ev);
      drag.pts[drag.vtx] = [q[0], q[1], ...(drag.pts[drag.vtx].slice(2))];
      const e = editPts(drag.obj); e.set(drag.obj, drag.pts.map((x) => x.slice())); V.draw(); return true;
    }
    if (drag && drag.o) {
      if (!drag.moved && Math.hypot(...V.toS(p).map((x, i) => x - V.toS(drag.start)[i])) < 4) return true;
      drag.moved = true; V.cv.classList.add("move");
      const m = moveRec(drag.before, p[0] - drag.start[0], p[1] - drag.start[1]);
      Object.keys(drag.o).forEach((k) => delete drag.o[k]); Object.assign(drag.o, m); V.draw(); return true;
    }
    if (drag && drag.box) { const a = drag.box, b = cornerSnap(p, null, ev); ghost = [[a[0], a[1]], [b[0], a[1]], [b[0], b[1]], [a[0], b[1]]]; V.draw(); return true; }
    if (tool === "street" || tool === "wall") { const sn = tool === "street" ? snapPt(p, null, ev) : { p: cornerSnap(p, null, ev) }; snapAt = sn.on || sn.real ? sn.p : null; if (linePts.length) V.draw(); else if (snapAt) V.draw(); return false; }
    if (tool === "select") { const h = handleAt(p); V.cv.style.cursor = h ? "pointer" : ""; const o = pick(p); if (o !== hover) { hover = o; V.draw(); } }
    return false;
  }
  async function up(ev, p) {
    V.cv.classList.remove("move");
    if (drag && drag.vtx !== undefined) {
      const { obj, before, pts, snap } = drag; drag = null; snapAt = null;
      const q = clone(obj), extra = [];
      if (snap && snap.on) { const j = withJunction(snap, pts); if (j) extra.push(j); }
      Object.keys(obj).forEach((k) => delete obj[k]); Object.assign(obj, before);   // the saved one comes back from save()
      await save([q, ...extra]); return;
    }
    if (drag && drag.o) {
      const { o, moved, before } = drag; drag = null;
      if (!moved) return;
      const q = clone(o); Object.keys(o).forEach((k) => delete o[k]); Object.assign(o, before);
      await save([q]); return;
    }
    if (drag && drag.box) {
      const g = ghost; drag = null; ghost = null;
      if (!g || Math.abs(g[2][0] - g[0][0]) < 0.5 || Math.abs(g[2][1] - g[0][1]) < 0.5) { V.draw(); return; }
      const ring = g.map((q) => [r2(q[0]), r2(q[1])]), k = $("mkind").value;
      let r;
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
  const KIND_FILL = (k) => ({ face_me_bungalow: "--home", compound_house: "--home", colonial_house: "--home", walkup: "--home", shop_under_flats: "--trade", market_block: "--trade", kiosk_row: "--trade", church: "--civic", mosque: "--civic", school: "--civic" }[k] || "--works");
  const SURF = { tar_new: "--tar", tar_worn: "--worn", sand: "--sand", earth: "--mud", laterite: "--laterite", interlock: "--interlock" };
  const surfCol = (k) => SURF[k] ? css(SURF[k]) : k === "concrete" ? "#a7a49d" : k === "plank" ? "#8a6a4a" : css("--worn");
  let MAPON = true;
  function path(ctx, pts, close) { ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]); if (close) ctx.closePath(); }
  function drawWorld(ctx, v, px) {
    if (!SCHEMA) return;
    // load the started districts in view once zoomed in to a district or so
    if (v[2] - v[0] < 15000) for (const d of started) if (!DS.has(d) && !loading.has(d)) { const S = studyD(d); if (S && hit(S.bb, v)) load(d); }
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
    for (const r of recsOf(["wire"])) { const a = rec(r.from_pole), b = r.to_pole ? rec(r.to_pole) : null, e = b ? b.at : r.to_at; if (!a || !Array.isArray(a.at) || !Array.isArray(e)) continue; path(ctx, [a.at, e]); ctx.strokeStyle = "#333"; ctx.lineWidth = px; ctx.stroke(); }
    for (const r of recsOf(["place"])) for (const ring of (Array.isArray(r.area) ? r.area : [])) if (ring.length > 2 && inView(ring)) { path(ctx, ring, true); ctx.setLineDash([8 * px, 4 * px]); const b = badness(r); ctx.strokeStyle = b === "bad" ? BAD : b === "incomplete" ? WARN : css("--accent"); ctx.lineWidth = 1.5 * px; ctx.stroke(); ctx.setLineDash([]); }
    // selection, hover, handles, what is being drawn
    const outline = (r, col, w) => {
      ctx.strokeStyle = col; ctx.lineWidth = w * px;
      const e = editPts(r), q = thingPts(r) || leantoQuad(r);
      if (e) { if (r.type === "road") { path(ctx, e.pts); ctx.lineWidth = (r.width || 0) + 6 * px; ctx.globalAlpha = 0.3; ctx.stroke(); ctx.globalAlpha = 1; } else { path(ctx, e.pts, e.closed); ctx.stroke(); } }
      else if (q) { path(ctx, q, true); ctx.stroke(); }
      else if (Array.isArray(r.at)) { ctx.beginPath(); ctx.arc(r.at[0], r.at[1], Math.max(thingR(r), 9 * px), 0, 7); ctx.stroke(); }
    };
    if (hover && hover !== sel && tool === "select") outline(hover, css("--sel"), 1.5);
    if (sel) outline(sel, css("--sel"), 3);
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
    if (snapAt) { ctx.beginPath(); ctx.arc(snapAt[0], snapAt[1], 7 * px, 0, 7); ctx.strokeStyle = css("--ok"); ctx.lineWidth = 2 * px; ctx.stroke(); }
  }
  function drawScreen(ctx) {   // small labels: a building's storeys, a line's length while drawing
    if (!SCHEMA || !MAPON) return;
    ctx.font = "600 11px -apple-system, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
    if (V.s > 3) for (const r of recsOf(["building"])) { if (!Array.isArray(r.footprint) || r.footprint.length < 3) continue; const [X, Y] = V.toS(centroid(r.footprint)); if (X < 0 || Y < 0 || X > V.cv.clientWidth || Y > V.cv.clientHeight) continue; ctx.fillStyle = css("--ink"); ctx.fillText(r.storeys ? String(r.storeys) : "?", X, Y); }
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
        return `<fieldset><legend>${lab}${f.opt ? ` <button data-act="rm" data-p="${esc(p)}">remove</button>` : ""}</legend><table class="tb"><tr>${cols.map(([cn]) => `<th>${cn}</th>`).join("")}<th></th></tr>${v.rows.map((row, i) => `<tr>${row.map((x, j) => `<td><input data-p="${esc(p)}.rows.${i}.${j}" data-b="cell" data-a="${esc(cols[j][1])}" value="${val(x)}"></td>`).join("")}<td><button data-act="rm" data-p="${esc(p)}.rows.${i}">×</button></td></tr>`).join("")}</table><button data-act="row" data-p="${esc(p)}" data-a="${f.arg}">Add a row</button></fieldset>`;
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
  const HELP = `<div id="help"><b>Select</b> (V): click a record; drag to move; drag a square handle to move a corner, a round one to add a corner, <kbd>⌥</kbd>-click a corner to remove it. <kbd>R</kbd>/<kbd>Shift R</kbd> turn 15°, <kbd>[</kbd> <kbd>]</kbd> 1°. <kbd>Delete</kbd> removes, <kbd>⌘Z</kbd> undoes. Drag empty ground, the right button or <kbd>Space</kbd> to pan.<br><br><b>Street</b> (S): click points, <kbd>Enter</kbd> or double-click to finish; points snap onto the map's roads (a shared point joins them) and, with "Snap to real roads", onto the real line under it. <kbd>Shift</kbd> places freely. <b>Building</b> (B), <b>Plot</b> (P), <b>Place</b> (A): drag a box. <b>Wall</b> (W): click points, <kbd>Enter</kbd>. <b>Gate</b> (G): click a wall twice, at each end. <b>Lean-to</b> (L): click a building side twice. <b>Tree</b> (T), <b>Furniture</b> (F): click. <b>Surface</b> (U): click a road.<br><br>Every field shows its value; one in red needs a value (nothing is filled in for you). Outlines: <span style="color:var(--warn)">dashed amber</span> = fields still to set, <span style="color:var(--bad)">red</span> = a problem (check_map.py runs on every save, plus a house on a road or on another house).</div>`;
  function showPanel() {
    const P = $("panel"); if (!SCHEMA || !P) return;
    const keep = P.scrollTop;
    const o = sel;
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
    const F0 = fieldsOf(o.type);
    h += Object.entries(F0).filter(([k]) => !["id", "type", "ref", "from"].includes(k)).map(([k, sp]) => fieldHTML(k, sp, o[k], k)).join("");
    for (const k of ["ref", "from"]) if (o[k]) h += `<div class="fld"><span class="fk">${k}</span><code>${esc(JSON.stringify(o[k]))}</code></div>`;
    h += `<div class="row">${"turn" in F0 || editPts(o) ? `<button id="mrl">⟲ 15°</button><button id="mrr">⟳ 15°</button>` : ""}${o.type !== "district" ? `<button id="mdel">Delete</button>` : ""}</div><hr>` + HELP;
    P.innerHTML = h; P.scrollTop = keep;
    const on = (id, fn) => { const e = $(id); if (e) e.addEventListener("click", fn); };
    on("mrl", () => turnSel(-15)); on("mrr", () => turnSel(15)); on("mdel", () => del(o));
    if ($("nw")) ["nw", "nd", "na", "nx", "ny"].forEach((id) => $(id).addEventListener("change", async () => {
      const [w, dep, a, x, y] = ["nw", "nd", "na", "nx", "ny"].map((i) => parseFloat($(i).value));
      if (![w, dep, a, x, y].every(isFinite) || w < 0.5 || dep < 0.5) { toast("Size needs numbers of at least 0.5 m"); showPanel(); return; }
      const q = clone(o); q.footprint = orient(rectFrom(w, dep, a, x, y)); await save([q]);
    }));
  }
  async function turnSel(deg) { if (!sel) return; const q = turnRec(sel, deg); if (q) await save([q]); }

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
    st.textContent = `#panel .fld{display:grid;grid-template-columns:38% 1fr auto;gap:4px;align-items:center;margin:3px 0}#panel .fk{color:var(--muted);overflow-wrap:anywhere}#panel .fk.bad{color:var(--bad);font-weight:600}#panel fieldset{border:1px solid var(--panel-line);border-radius:6px;margin:6px 0;padding:4px 6px}#panel fieldset.item{border-style:dashed}#panel legend{font-size:12px}#panel select{font:inherit;color:var(--ink);background:var(--paper);border:1px solid var(--panel-line);border-radius:6px;padding:3px 4px;width:100%}#panel .chk{display:flex;flex-wrap:wrap;gap:2px 8px}#panel .chk label{display:flex;gap:3px;align-items:center}#panel .ptrow,#panel .hexrow{display:flex;gap:4px}#panel .hexrow input[type=color]{width:34px;padding:0;height:26px}#panel .tb input{padding:2px 3px}#panel .tb th{font-weight:500;color:var(--muted);text-align:left}#panel .x{padding:1px 6px}#panel .probs{margin:4px 0 8px;font-size:12px}#panel .probs .warn{color:var(--warn)}#panel .probs .bad{color:var(--bad)}#panel code{font-size:11px;overflow-wrap:anywhere}#panel{width:360px}`;
    document.head.appendChild(st);
    const bar = document.querySelector(".bar");
    bar.insertAdjacentHTML("beforeend", `<div class="group"><select id="mdist" aria-label="District to draw in"></select></div><div class="group" id="mtools">${TOOLS.map(([t, l, k, tip]) => `<button data-tool="${t}" title="${tip} (${k})">${l}</button>`).join("")}</div><div class="group"><select id="mkind" aria-label="Kind"></select><label id="msnap" title="While drawing a street, snap onto the real road line under it"><input type="checkbox"${snapReal ? " checked" : ""}> Snap to real roads</label><label title="Show the new map's records"><input type="checkbox" id="mon" checked> Map</label></div>`);
    document.querySelectorAll("#mtools button").forEach((b) => b.addEventListener("click", () => setTool(b.dataset.tool)));
    $("msnap").querySelector("input").addEventListener("change", (ev) => { snapReal = ev.target.checked; try { localStorage.setItem("gidi-map-snapreal", snapReal ? "1" : "0"); } catch (e) {} });
    $("mon").addEventListener("change", (ev) => { MAPON = ev.target.checked; V.draw(); });
    $("mdist").addEventListener("change", (ev) => {
      cur = ev.target.value || null; try { localStorage.setItem("gidi-map-district", cur || ""); } catch (e) {}
      sel = null; const S = cur && studyD(cur); if (S) V.fit(S.bb, 60);
      if (cur && started.has(cur) && !DS.has(cur)) load(cur);
      showPanel(); V.draw();
    });
    const P = $("panel");
    P.style.display = "";
    P.addEventListener("change", (ev) => { const el = ev.target; if (el.type === "color" && el.dataset.for) { const t = P.querySelector(`input[data-p="${CSS.escape(el.dataset.for)}"]:not([type=color])`); if (t) { t.value = el.value; onField(t); } return; } if (el.dataset.p) onField(el); });
    P.addEventListener("click", (ev) => { const b = ev.target.closest("button[data-act]"); if (b) { ev.preventDefault(); onAct(b); } });
    window.addEventListener("keydown", (ev) => {
      if (/^(INPUT|SELECT|TEXTAREA)$/.test(ev.target.tagName)) return;
      if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === "z") { ev.preventDefault(); undo(); return; }
      if (ev.metaKey || ev.ctrlKey) return;
      const k = ev.key.toLowerCase();
      if (k === "escape") { linePts = []; ghost = null; drag = null; firstClick = null; if (tool !== "select") setTool("select"); else { sel = null; showPanel(); } V.draw(); }
      else if (k === "enter" && (tool === "street" || tool === "wall")) finishLine();
      else if (k === "backspace" || k === "delete") { ev.preventDefault(); if ((tool === "street" || tool === "wall") && linePts.length) { linePts.pop(); V.draw(); } else if (sel && sel.type !== "district") del(sel); }
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
    fillPicker();
    if (cur && started.has(cur)) load(cur);
    showPanel(); V.draw();
  }
  return { init, drawWorld, drawScreen, down, move, up, get state() { return { DS, dOf, sel, cur, tool }; } };
})();
