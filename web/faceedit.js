/* The face editor on the new frame's board (docs/MAP-FORMAT.md, "faces"): one face of a building drawn flat, u across from
   the face's first corner, z up from the ground, with its windows, doors, shopfronts, balconies, screens, stains, add-ons,
   signs and awnings. Drag a box to add one, drag it to move it, drag a corner to size it; every field is in the side form.
   Each change saves the building's whole faces record through the map editor (web/mapedit.js), like any other record.
   What a drag gives (where and how big) is measured from the drawing; every other value stays unset until you give it,
   or comes from the piece you had picked ("like the picked one"), the way a stamp does. Opened from a building's panel. */
window.FACEEDIT = (() => {
  "use strict";
  let H = null, B = null, FI = 0, FC = null, tool = "select", selK = null, selI = -1, drag = null, cv = null, ctx = null, T = null, box = null;
  const $ = (id) => document.getElementById(id);
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const clone = (o) => JSON.parse(JSON.stringify(o));
  const r2 = (v) => Math.round(v * 100) / 100;
  // what each piece is called, which field holds it, and its enum for the kind picker
  const KEYS = [["windows", "Window", "window_kind", "kind"], ["doors", "Door", "door_kind", "kind"], ["shopfronts", "Shopfront", "shopfront_door", "door"], ["balconies", "Balcony", null], ["screens", "Screen", "screen_kind", "kind"], ["stains", "Stain", "stain_kind", "kind"], ["addons", "Add-on", "addon_kind", "kind"], ["signs", "Sign", null], ["awnings", "Awning", null]];
  const COL = { windows: "#5aa0d8", doors: "#8a5a3a", shopfronts: "#c9a227", balconies: "#d0d0c8", screens: "#b0a080", stains: "#5a4a3a", addons: "#e0457b", signs: "#f2c200", awnings: "#1f6fb8" };
  const isTable = (k) => { const sp = H.SCHEMA.shapes.face[k]; return sp && sp.startsWith("table:"); };
  const shapeOf = (k) => { const sp = H.SCHEMA.shapes.face[k], a = sp.split(":")[1].replace(/\?$/, ""); return sp.startsWith("table:") ? Object.fromEntries(H.SCHEMA.tables[a]) : H.SCHEMA.shapes[a]; };
  const fp = () => B.footprint, nF = () => fp().length;
  const faceLen = () => { const p = fp()[FI], q = fp()[(FI + 1) % nF()]; return Math.hypot(q[0] - p[0], q[1] - p[1]); };
  const storeyH = () => (Array.isArray(B.storey_h) && B.storey_h.length ? B.storey_h : Array(B.storeys > 0 ? B.storeys : 1).fill(3));   // 3 m a storey only to draw by when none is set
  const height = () => storeyH().reduce((a, b) => a + b, 0);
  const storeyBase = (n) => storeyH().slice(0, Math.max(0, n - 1)).reduce((a, b) => a + b, 0);
  const entry = () => (FC && Array.isArray(FC.faces) ? FC.faces.find((f) => f.face === FI) : null);
  function items(k) {   // the pieces under a key, as objects (table rows read through their columns)
    const E = entry(); if (!E || !E[k]) return [];
    if (isTable(k)) { const t = E[k]; return Array.isArray(t.rows) ? t.rows.map((row) => Object.fromEntries(t.cols.map((c, i) => [c, row[i]]))) : []; }
    return Array.isArray(E[k]) ? E[k] : [];
  }
  function putItem(E, k, i, o) {   // write o back as piece i (or a new one when i is -1); returns its index
    if (isTable(k)) { const t = E[k]; const row = t.cols.map((c) => (o[c] === undefined ? null : o[c])); if (i < 0) { t.rows.push(row); return t.rows.length - 1; } t.rows[i] = row; return i; }
    if (i < 0) { E[k].push(o); return E[k].length - 1; } E[k][i] = o; return i;
  }
  const num = (v, d) => (typeof v === "number" && isFinite(v) ? v : d);
  function boxOf(k, o) {   // [u0, z0, u1, z1] on the face; sizes not yet set are drawn small so the piece can be seen and picked
    const u = num(o.u, 0), w = num(o.w, 0.6), h = num(o.h, 0.6), gh = Math.min(storeyH()[0], 3.2) - 0.4;
    switch (k) {
      case "windows": case "stains": return [u - w / 2, num(o.z, 0), u + w / 2, num(o.z, 0) + h];
      case "doors": return [u - w / 2, 0, u + w / 2, num(o.h, 2.1)];
      case "addons": { const s = num(o.size, 0.4); return [u - s / 2, num(o.z, 0) - s / 2, u + s / 2, num(o.z, 0) + s / 2]; }
      case "shopfronts": return [num(o.u0, 0), 0, num(o.u1, 1), gh];
      case "balconies": { const z = storeyBase(num(o.storey, 2)); return [num(o.u0, 0), z, num(o.u1, 1), z + Math.max(num(o.solid_h, 0), 1.0)]; }
      case "screens": return [num(o.u0, 0), 0, num(o.u1, 1), num(o.h, 1.2)];
      case "signs": return [num(o.u0, 0), num(o.z0, 2.5), num(o.u1, 1), num(o.z1, 3)];
      case "awnings": return [num(o.u0, 0), num(o.z, 2.6) - 0.2, num(o.u1, 1), num(o.z, 2.6)];
    }
    return [0, 0, 0, 0];
  }
  function setBox(k, o, b) {   // the measured fields from a box drawn on the face
    const [u0, z0, u1, z1] = [r2(Math.min(b[0], b[2])), r2(Math.max(0, Math.min(b[1], b[3]))), r2(Math.max(b[0], b[2])), r2(Math.max(b[1], b[3]))];
    const mid = r2((u0 + u1) / 2), w = r2(u1 - u0), h = r2(z1 - z0);
    switch (k) {
      case "windows": case "stains": Object.assign(o, { u: mid, z: z0, w, h }); break;
      case "doors": Object.assign(o, { u: mid, w, h: z1 }); break;
      case "addons": Object.assign(o, { u: mid, z: r2((z0 + z1) / 2) }); if (w > 0.15 || h > 0.15) o.size = r2(Math.max(w, h)); break;
      case "shopfronts": Object.assign(o, { u0, u1 }); break;
      case "balconies": { let n = 1; while (n < storeyH().length && storeyBase(n + 1) <= z0 + 0.3) n++; Object.assign(o, { u0, u1, storey: Math.max(2, n) }); break; }   // a balcony stands on an upper floor
      case "screens": Object.assign(o, { u0, u1, h: z1 }); break;
      case "signs": Object.assign(o, { u0, u1, z0, z1 }); break;
      case "awnings": Object.assign(o, { u0, u1, z: z1 }); break;
    }
  }
  const GEO = { windows: ["u", "z", "w", "h"], stains: ["u", "z", "w", "h"], doors: ["u", "w", "h"], addons: ["u", "z", "size"], shopfronts: ["u0", "u1"], balconies: ["u0", "u1", "storey"], screens: ["u0", "u1", "h"], signs: ["u0", "u1", "z0", "z1"], awnings: ["u0", "u1", "z"] };

  // ------------------------------------------------------------------ saving
  function freshEntry() { const E = { face: FI }; for (const [k, sp] of Object.entries(H.SCHEMA.shapes.face)) if (k !== "face") E[k] = sp.startsWith("table:") ? { cols: H.SCHEMA.tables[sp.split(":")[1]].map(([c]) => c), rows: [] } : []; return E; }   // empty containers only
  async function commit(mut) {   // change a copy of the faces record and save it whole
    const q = FC ? clone(FC) : { id: H.newId("faces"), type: "faces", of: B.id, faces: [], _d: H.dOf.get(B.id) };
    let E = q.faces.find((f) => f.face === FI); if (!E) { E = freshEntry(); q.faces.push(E); q.faces.sort((a, b) => a.face - b.face); }
    for (const [k, sp] of Object.entries(H.SCHEMA.shapes.face)) if (k !== "face" && !E[k]) E[k] = sp.startsWith("table:") ? { cols: H.SCHEMA.tables[sp.split(":")[1]].map(([c]) => c), rows: [] } : [];
    const ret = mut(E);
    if (!(await H.save([q]))) return null;
    FC = H.rec(q.id); B = H.rec(B.id) || B; draw(); form(); return ret;
  }

  // ------------------------------------------------------------------ the view
  function fit() {   // metres to pixels: the face fills the canvas with a margin
    const W = cv.clientWidth, Hh = cv.clientHeight, L = Math.max(faceLen(), 1), Z = Math.max(height() + 1.5, 4), s = Math.min((W - 80) / L, (Hh - 70) / Z);
    T = { s, ox: (W - L * s) / 2, oy: Hh - 40 };
  }
  const toS = (u, z) => [T.ox + u * T.s, T.oy - z * T.s];
  const toF = (x, y) => [(x - T.ox) / T.s, (T.oy - y) / T.s];
  function draw() {
    if (!cv) return;
    const dpr = window.devicePixelRatio || 1; cv.width = cv.clientWidth * dpr; cv.height = cv.clientHeight * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); fit();
    const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim(), L = faceLen(), Hb = height();
    ctx.fillStyle = css("--paper") || "#222"; ctx.fillRect(0, 0, cv.clientWidth, cv.clientHeight);
    const [a, b] = [toS(0, 0), toS(L, Hb)];
    ctx.fillStyle = (B.finish && B.finish.colour) || "#9a9488"; ctx.fillRect(a[0], b[1], b[0] - a[0], a[1] - b[1]);
    ctx.strokeStyle = "rgba(0,0,0,.35)"; ctx.setLineDash([5, 4]); let z = 0;
    for (const h of storeyH().slice(0, -1)) { z += h; const y = toS(0, z)[1]; ctx.beginPath(); ctx.moveTo(a[0], y); ctx.lineTo(b[0], y); ctx.stroke(); }
    ctx.setLineDash([]); ctx.strokeStyle = css("--ink") || "#ddd"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(10, a[1]); ctx.lineTo(cv.clientWidth - 10, a[1]); ctx.stroke(); ctx.lineWidth = 1;
    ctx.fillStyle = css("--muted") || "#999"; ctx.font = "11px -apple-system, sans-serif"; ctx.textAlign = "center";
    for (let u = 0; u <= L + 1e-6; u += 1) { const x = toS(u, 0)[0]; ctx.fillRect(x, a[1], 1, 5); if (u % (T.s < 30 ? 5 : 1) === 0) ctx.fillText(u + " m", x, a[1] + 17); }
    ctx.textAlign = "start";
    for (const [k] of KEYS) items(k).forEach((o, i) => {
      const [u0, z0, u1, z1] = boxOf(k, o), p = toS(u0, z1), q = toS(u1, z0), on = k === selK && i === selI;
      ctx.globalAlpha = k === "stains" ? 0.55 : 0.85; ctx.fillStyle = (k === "signs" ? o.bg : k === "windows" || k === "stains" ? null : o.colour) || COL[k]; ctx.fillRect(p[0], p[1], q[0] - p[0], q[1] - p[1]); ctx.globalAlpha = 1;
      const unset = Object.values(o).some((v) => v === null || v === undefined) || Object.keys(shapeOf(k)).some((c) => !shapeOf(k)[c].endsWith("?") && !(c in o));
      ctx.strokeStyle = on ? css("--sel") || "#4af" : unset ? css("--warn") || "#e0a030" : "rgba(0,0,0,.6)"; ctx.lineWidth = on ? 2.5 : 1.2; ctx.setLineDash(unset && !on ? [4, 3] : []); ctx.strokeRect(p[0], p[1], q[0] - p[0], q[1] - p[1]); ctx.setLineDash([]); ctx.lineWidth = 1;
      if (q[0] - p[0] > 34) { ctx.fillStyle = "#111"; ctx.fillText(k === "signs" ? (o.text || "sign") : String(o.kind || o.door || o.pattern || k.slice(0, -1)), p[0] + 3, p[1] + 12); }
      if (on) for (const c of [[p[0], p[1]], [q[0], p[1]], [q[0], q[1]], [p[0], q[1]]]) { ctx.fillStyle = css("--panel") || "#fff"; ctx.fillRect(c[0] - 4, c[1] - 4, 8, 8); ctx.strokeStyle = css("--sel") || "#4af"; ctx.strokeRect(c[0] - 4, c[1] - 4, 8, 8); }
    });
    if (box) { const p = toS(Math.min(box[0], box[2]), Math.max(box[1], box[3])), q = toS(Math.max(box[0], box[2]), Math.min(box[1], box[3])); ctx.strokeStyle = css("--sel") || "#4af"; ctx.setLineDash([4, 3]); ctx.strokeRect(p[0], p[1], q[0] - p[0], q[1] - p[1]); ctx.setLineDash([]); }
    $("fe-title").textContent = `${B.id} · face ${FI} of ${nF()} · ${L.toFixed(2)} m long, ${Hb.toFixed(1)} m high${Array.isArray(B.storey_h) ? "" : " (storey heights not set: drawn at 3 m)"}`;
  }

  // ------------------------------------------------------------------ pointer
  function hitAt(x, y) {   // the piece under the pointer, smallest first; and a corner of the picked one
    if (selK) { const o = items(selK)[selI]; if (o) { const [u0, z0, u1, z1] = boxOf(selK, o), C = [[u0, z1], [u1, z1], [u1, z0], [u0, z0]]; for (let c = 0; c < 4; c++) { const s = toS(...C[c]); if (Math.abs(s[0] - x) < 7 && Math.abs(s[1] - y) < 7) return { k: selK, i: selI, corner: c }; } } }
    const [u, z] = toF(x, y); let best = null, ba = 1e9;
    for (const [k] of KEYS) items(k).forEach((o, i) => { const b = boxOf(k, o), A = (b[2] - b[0]) * (b[3] - b[1]); if (u >= b[0] - 0.05 && u <= b[2] + 0.05 && z >= b[1] - 0.05 && z <= b[3] + 0.05 && A < ba) { ba = A; best = { k, i }; } });
    return best;
  }
  function onDown(ev) {
    const r = cv.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top, f = toF(x, y);
    if (tool === "select") {
      const h = hitAt(x, y);
      if (!h) { selK = null; selI = -1; draw(); form(); return; }
      selK = h.k; selI = h.i; const o = items(h.k)[h.i];
      drag = { k: h.k, i: h.i, corner: h.corner, start: f, b0: boxOf(h.k, o), o: clone(o), moved: false }; draw(); form(); return;
    }
    box = [f[0], f[1], f[0], f[1]]; drag = { make: tool }; draw();
  }
  function onMove(ev) {
    if (!drag) return;
    const r = cv.getBoundingClientRect(), f = toF(ev.clientX - r.left, ev.clientY - r.top);
    if (drag.make) { box[2] = f[0]; box[3] = f[1]; draw(); return; }
    const du = f[0] - drag.start[0], dz = f[1] - drag.start[1]; if (!drag.moved && Math.hypot(du, dz) * T.s < 3) return; drag.moved = true;
    const b = drag.b0.slice();
    if (drag.corner === undefined) { b[0] += du; b[2] += du; b[1] += dz; b[3] += dz; }
    else { const ux = drag.corner === 0 || drag.corner === 3 ? 0 : 2, zx = drag.corner < 2 ? 3 : 1; b[ux] += du; b[zx] += dz; }
    const o = clone(drag.o); setBox(drag.k, o, b); drag.live = o;
    const E = entry(); if (E) putItem(E, drag.k, drag.i, o); draw();
  }
  async function onUp() {
    const d = drag; drag = null; if (!d) return;
    if (d.make) {
      const b = box; box = null; const k = d.make, small = Math.abs(b[2] - b[0]) < 0.1 && Math.abs(b[3] - b[1]) < 0.1;
      if (small && k !== "addons") { draw(); H.toast("Drag a box on the face to draw it"); return; }
      const like = selK === k ? items(k)[selI] : null, o = {};
      for (const c of Object.keys(shapeOf(k))) if (!shapeOf(k)[c].endsWith("?")) o[c] = null;
      if (like) for (const [c, v] of Object.entries(like)) if (!GEO[k].includes(c)) o[c] = clone(v);   // like the picked one
      const kk = KEYS.find((x) => x[0] === k); if (kk[2] && $("fe-kind").value) o[kk[3]] = $("fe-kind").value;
      for (const c of Object.keys(o)) if (o[c] === null && !isTable(k)) delete o[c];   // an object's unset field is left out (needs a value)
      setBox(k, o, b);
      const i = await commit((E) => putItem(E, k, -1, o)); if (i !== null) { selK = k; selI = i; draw(); form(); }
      return;
    }
    if (d.moved && d.live) { const o = d.live; await commit((E) => putItem(E, d.k, d.i, o)); }
  }

  // ------------------------------------------------------------------ the side form: every field of the picked piece
  function input(c, sp, v) {
    const base = sp.replace(/\?$/, "").split(" ")[0].split(":"), opt = sp.endsWith("?"), has = v !== null && v !== undefined;
    const lab = `<span class="fk${!opt && !has ? " bad" : ""}">${esc(c)}${!opt && !has ? " · needs a value" : ""}</span>`;
    let w;
    if (base[0] === "enum") w = `<select data-c="${c}" data-s="${esc(sp)}"><option value="">${opt ? "— none —" : "— needs a value —"}</option>${H.SCHEMA.enums[base[1]].map((e) => `<option${e === v ? " selected" : ""}>${e}</option>`).join("")}</select>`;
    else if (base[0] === "bool") w = `<select data-c="${c}" data-s="${esc(sp)}"><option value="">— needs a value —</option><option value="true"${v === true ? " selected" : ""}>yes</option><option value="false"${v === false ? " selected" : ""}>no</option></select>`;
    else if (base[0] === "hex") w = `<span class="hexrow"><input data-c="${c}" data-s="${esc(sp)}" value="${has ? esc(v) : ""}" placeholder="#rrggbb"><input type="color" data-for="${c}" value="${has ? esc(v) : "#808080"}"></span>`;
    else if (base[0] === "table") w = `<span class="k">${has && v.rows ? v.rows.length + " rows (in the building's panel)" : "none"}</span>`;
    else if (base[0] === "nums") w = `<input data-c="${c}" data-s="${esc(sp)}" value="${has ? esc(v.join(", ")) : ""}" placeholder="numbers, a comma between">`;
    else w = `<input data-c="${c}" data-s="${esc(sp)}"${base[0] === "num" || base[0] === "int" ? ' type="number" step="any"' : ""} value="${has ? esc(v) : ""}" placeholder="${opt ? "none" : "needs a value"}${sp.includes(" ") ? " (" + esc(sp.split(" ").slice(1).join(" ").replace(/\?$/, "")) + ")" : ""}">`;
    return `<div class="fld">${lab}${w}</div>`;
  }
  function form() {
    const P = $("fe-form"); if (!P) return;
    const o = selK ? items(selK)[selI] : null;
    if (!o) {
      const n = KEYS.map(([k, l]) => [l, items(k).length]).filter((x) => x[1]);
      P.innerHTML = `<h3>Face ${FI}</h3><p class="k">${n.length ? n.map(([l, c]) => `${c} ${l.toLowerCase()}${c > 1 ? "s" : ""}`).join(", ") : "Nothing on this face yet."}</p><p class="k">Pick a piece above, then drag a box on the face: where and how big come from the box; the kind from the list; every other value is yours to give in this form. With a piece picked, the next one you draw of the same sort takes its values (not its place or size).</p><p class="k">u is metres along the face from its first corner (the footprint's corner ${FI}); z is metres up. A window's, stain's and door's u is its middle; z is its bottom (a window's sill); an add-on's z is its middle.</p><p class="k">Select: drag to move, drag a corner to size, <kbd>Delete</kbd> removes, <kbd>⌘Z</kbd> undoes, <kbd>Esc</kbd> closes.</p>`;
      return;
    }
    const S = shapeOf(selK);
    P.innerHTML = `<h3>${esc(KEYS.find((x) => x[0] === selK)[1])} ${selI + 1}</h3>` + Object.entries(S).map(([c, sp]) => input(c, sp, o[c])).join("") + `<div class="row"><button id="fe-del">Remove it</button></div>`;
    $("fe-del").addEventListener("click", removeSel);
  }
  async function onForm(el) {
    if (!selK) return;
    const c = el.dataset.c, sp = el.dataset.s, base = sp.replace(/\?$/, "").split(" ")[0].split(":")[0], raw = el.value.trim();
    let v = null;
    if (raw !== "") {
      if (base === "num" || base === "int") { v = Number(raw); if (!isFinite(v)) { H.toast(`"${raw}" isn't a number`); return; } }
      else if (base === "bool") v = raw === "true";
      else if (base === "nums") { v = raw.split(/[\s,]+/).filter(Boolean).map(Number); if (!v.every(isFinite)) { H.toast("Numbers only, with a comma between"); return; } }
      else if (base === "hex") v = raw.toLowerCase();
      else v = raw;
    }
    const k = selK, i = selI, o = clone(items(k)[i]);
    if (v === null && !isTable(k)) delete o[c]; else o[c] = v;
    await commit((E) => putItem(E, k, i, o));
  }
  async function removeSel() {
    if (!selK) return; const k = selK, i = selI; selK = null; selI = -1;
    await commit((E) => { if (isTable(k)) E[k].rows.splice(i, 1); else E[k].splice(i, 1); });
  }

  // ------------------------------------------------------------------ open, close, keys
  function setTool(t) {
    tool = t; document.querySelectorAll("#fe-tools button").forEach((b) => b.classList.toggle("on", b.dataset.t === t));
    const kk = KEYS.find((x) => x[0] === t), s = $("fe-kind");
    s.innerHTML = kk && kk[2] ? H.SCHEMA.enums[kk[2]].map((e) => `<option>${e}</option>`).join("") : ""; s.style.display = kk && kk[2] ? "" : "none";
    if (kk && selK === t) { const o = items(t)[selI]; if (o && o[kk[3]]) s.value = o[kk[3]]; }
    cv.style.cursor = t === "select" ? "default" : "crosshair";
  }
  function onKey(ev) {
    if (!B) return;
    if (/^(INPUT|SELECT|TEXTAREA)$/.test(ev.target.tagName)) return;
    ev.stopPropagation();
    const k = ev.key.toLowerCase();
    if ((ev.metaKey || ev.ctrlKey) && k === "z") { ev.preventDefault(); H.undo().then(() => { FC = FC && H.rec(FC.id); if (!FC) FC = H.recsOf(["faces"]).find((r) => r.of === B.id) || null; selK = null; selI = -1; draw(); form(); }); return; }
    if (k === "escape") { if (tool !== "select") setTool("select"); else if (selK) { selK = null; selI = -1; draw(); form(); } else close(); }
    else if (k === "backspace" || k === "delete") { ev.preventDefault(); removeSel(); }
  }
  function close() { const el = $("faceed"); if (el) el.remove(); window.removeEventListener("keydown", onKey, true); window.removeEventListener("resize", draw); B = null; FC = null; H.closed && H.closed(); }
  function goFace(n) { FI = ((n % nF()) + nF()) % nF(); selK = null; selI = -1; draw(); form(); }
  function open(host, building, face) {
    if (B) close();
    H = host; B = building; FI = face || 0; FC = H.recsOf(["faces"]).find((r) => r.of === B.id) || null; selK = null; selI = -1;
    if (!Array.isArray(B.footprint) || B.footprint.length < 3) { H.toast("The building needs a footprint first"); B = null; return; }
    document.body.insertAdjacentHTML("beforeend", `<div id="faceed"><div class="fe-bar"><b>Face editor</b><button id="fe-prev" title="The face before">◀</button><span id="fe-title"></span><button id="fe-next" title="The next face">▶</button><span class="group" id="fe-tools"><button data-t="select">Select</button>${KEYS.map(([k, l]) => `<button data-t="${k}">${l}</button>`).join("")}</span><select id="fe-kind" aria-label="Kind"></select><button id="fe-close">Close (Esc)</button></div><div class="fe-body"><canvas id="fe-cv"></canvas><div id="fe-form"></div></div></div>`);
    if (!$("fe-style")) { const st = document.createElement("style"); st.id = "fe-style"; st.textContent = `#faceed{position:fixed;inset:0;z-index:50;background:var(--paper,#1e1e1e);display:flex;flex-direction:column;color:var(--ink);font:13px -apple-system,sans-serif}#faceed .fe-bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--panel-line)}#faceed .fe-bar button.on{background:var(--accent);color:#fff}#fe-title{min-width:300px}#faceed .fe-body{flex:1;display:flex;min-height:0}#fe-cv{flex:1;min-width:0;height:100%}#fe-form{width:320px;overflow:auto;padding:8px 12px;border-left:1px solid var(--panel-line);background:var(--panel)}#fe-form .fld{display:grid;grid-template-columns:38% 1fr;gap:4px;align-items:center;margin:3px 0}#fe-form .fk{color:var(--muted)}#fe-form .fk.bad{color:var(--bad);font-weight:600}#fe-form select,#fe-form input{font:inherit;width:100%;box-sizing:border-box}#fe-form .hexrow{display:flex;gap:4px}#fe-form .hexrow input[type=color]{width:34px;padding:0}#fe-form .k{color:var(--muted)}`; document.head.appendChild(st); }
    cv = $("fe-cv"); ctx = cv.getContext("2d");
    cv.addEventListener("pointerdown", (ev) => { cv.setPointerCapture(ev.pointerId); onDown(ev); });
    cv.addEventListener("pointermove", onMove); cv.addEventListener("pointerup", onUp);
    document.querySelectorAll("#fe-tools button").forEach((b) => b.addEventListener("click", () => setTool(b.dataset.t)));
    $("fe-prev").addEventListener("click", () => goFace(FI - 1)); $("fe-next").addEventListener("click", () => goFace(FI + 1)); $("fe-close").addEventListener("click", close);
    const P = $("fe-form");
    P.addEventListener("change", (ev) => { const el = ev.target; if (el.type === "color" && el.dataset.for) { const t = P.querySelector(`input[data-c="${el.dataset.for}"]:not([type=color])`); if (t) { t.value = el.value; onForm(t); } return; } if (el.dataset.c) onForm(el); });
    window.addEventListener("keydown", onKey, true); window.addEventListener("resize", draw);
    setTool("select"); draw(); form();
  }
  return { open, close, isOpen: () => !!B };
})();
