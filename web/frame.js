/* The drawing board's new frame (owner, 22 Oct 2026): real Lagos miniaturised at 1:3 in a 27 x 10.5 km frame, as study
   layers to draw the new map on by hand. Opened with board.html?frame=new; the old map stays at board.html.
   Data: window.FRAME (scripts/frame_study.py) and, zoomed in, web/frame-tiles/ (scripts/frame_footprints.py), Gidi metres,
   y south. A study underlay only: real names and lines are shown here and never written into the map. */
(() => {
  "use strict";
  const F = window.FRAME;
  const $ = (id) => document.getElementById(id);
  const cv = $("cv"), ctx = cv.getContext("2d");
  const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const isDark = () => { const r = document.documentElement.dataset.theme; return r ? r === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; };

  // ------------------------------------------------------------------ the bar: this view has no drawing tools yet
  document.title = "Gidi Drawing Board: new frame";
  document.querySelector(".bar").innerHTML = `
    <div class="group"><span class="title">Gidi drawing board · new frame 1:3</span><select id="district" aria-label="Go to a district"></select></div>
    <div class="group" id="layers"></div>
    <div class="group"><button id="fit" title="The whole frame (0)">Whole frame</button><a href="board.html" id="old" title="The old 17-district map"><button>Old map</button></a><button id="theme" title="Light or dark">◐</button></div>`;
  $("panel").style.display = "none";
  if (!F) {
    document.querySelector(".bar").insertAdjacentHTML("beforeend", '<div class="group"><span class="title" style="color:var(--bad)">No study layers yet: run scripts/frame_study.py</span></div>');
    return;
  }
  const FW = F.frame.w, FH = F.frame.h;

  // ------------------------------------------------------------------ geometry
  const bboxOf = (pts) => { const b = [1e9, 1e9, -1e9, -1e9]; for (const [x, y] of pts) { if (x < b[0]) b[0] = x; if (y < b[1]) b[1] = y; if (x > b[2]) b[2] = x; if (y > b[3]) b[3] = y; } return b; };
  const hit = (bb, v) => !(bb[2] < v[0] || bb[0] > v[2] || bb[3] < v[1] || bb[1] > v[3]);
  function inPoly(p, poly) { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const a = poly[i], b = poly[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]) c = !c; } return c; }
  function segDist(p, a, b) { const dx = b[0] - a[0], dy = b[1] - a[1], L = dx * dx + dy * dy; let t = L ? ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L : 0; t = Math.max(0, Math.min(1, t)); return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy); }
  function lineDist(p, pts) { let m = 1e9; for (let i = 0; i < pts.length - 1; i++) m = Math.min(m, segDist(p, pts[i], pts[i + 1])); return m; }
  const C = F.frame.corners_latlon;   // [lat, lon]: south-west, south-east, north-east, north-west (the frame is not turned)
  function latlon(x, y) {             // Gidi metres -> real lat, lon (bilinear over the corners: good to a few metres)
    const u = x / FW, v = 1 - y / FH;
    const lat = (1 - u) * (1 - v) * C[0][0] + u * (1 - v) * C[1][0] + u * v * C[2][0] + (1 - u) * v * C[3][0];
    const lon = (1 - u) * (1 - v) * C[0][1] + u * (1 - v) * C[1][1] + u * v * C[2][1] + (1 - u) * v * C[3][1];
    return [lat, lon];
  }

  // ------------------------------------------------------------------ the data, indexed once
  F.roads.forEach((r) => (r.bb = bboxOf(r.p)));
  F.water.forEach((w) => (w.bb = bboxOf(w[0])));
  F.districts.forEach((d) => (d.bb = bboxOf(d.rings.flatMap((r) => r[0]))));
  F.lines.forEach((l) => (l.bb = bboxOf(l.p)));
  const districtAt = (p) => F.districts.find((d) => hit(d.bb, [p[0], p[1], p[0], p[1]]) && d.rings.some((r) => inPoly(p, r[0]) && !r.slice(1).some((h) => inPoly(p, h))));

  // ------------------------------------------------------------------ layers
  const LAYERS = { water: true, motorway: true, trunk: true, primary: true, secondary: true, links: true, rail: true, bridges: true, districts: true, unsure: true, places: true, roofs: true };
  const LNAME = { water: "Water", motorway: "Motorway", trunk: "Trunk", primary: "Primary", secondary: "Secondary", links: "Ramps", rail: "Rail", bridges: "Bridges", districts: "Districts", unsure: "Unsure lines", places: "Places", roofs: "Real roofs (zoomed in)" };
  try { Object.assign(LAYERS, JSON.parse(localStorage.getItem("gidi-frame-layers") || "{}")); } catch (e) {}
  const lg = $("layers");
  for (const k of Object.keys(LAYERS)) {
    const l = document.createElement("label");
    l.innerHTML = `<input type="checkbox" ${LAYERS[k] ? "checked" : ""}> ${LNAME[k]}`;
    l.querySelector("input").addEventListener("change", (ev) => { LAYERS[k] = ev.target.checked; try { localStorage.setItem("gidi-frame-layers", JSON.stringify(LAYERS)); } catch (e) {} draw(); });
    lg.appendChild(l);
  }
  const dsel = $("district");
  dsel.innerHTML = '<option value="">Go to a district…</option>' + F.districts.map((d) => `<option value="${d.n}">${d.n}. ${d.name}</option>`).join("");
  dsel.addEventListener("change", () => { const d = F.districts.find((x) => String(x.n) === dsel.value); if (d) fit(d.bb, 80); dsel.value = ""; });

  const PAL = () => isDark()
    ? { motorway: "#ff7b72", trunk: "#f0883e", primary: "#d29922", secondary: "#8b949e", rail: "#bc8cff", bridge: "#e6edf3", dline: "#9aa4b1", dfill: ["rgba(88,166,255,.07)", "rgba(63,185,80,.07)", "rgba(210,153,34,.07)", "rgba(188,140,255,.07)"], unsure: "#ff5fa2", trace: "#f2cc60", roof: "rgba(200,200,190,.35)", frame: "#e8e6e1", land: "#1a1c1f" }
    : { motorway: "#c62828", trunk: "#e8590c", primary: "#d4a017", secondary: "#9a9a92", rail: "#7b3fa0", bridge: "#23262b", dline: "#6b6f76", dfill: ["rgba(31,111,235,.06)", "rgba(26,127,55,.06)", "rgba(191,135,0,.07)", "rgba(123,63,160,.06)"], unsure: "#d6336c", trace: "#b07d00", roof: "rgba(70,60,50,.28)", frame: "#23262b", land: "#f1eee6" };
  // road widths in Gidi metres at 1:3 (a dual carriageway is about 30 m real), never thinner than a hairline on screen
  const RW = { motorway: [10, 2.2], trunk: [8, 1.8], primary: [6, 1.4], secondary: [4, 1.0], rail: [3, 1.2] };

  // ------------------------------------------------------------------ real roofs, loaded per 1 km tile when zoomed in
  const TILES = new Map();   // "i_j" -> null (loading) | false (none) | Float32Array[] (rings)
  let tileIndex = null;
  fetch("frame-tiles/index.json").then((r) => r.ok ? r.json() : null).then((j) => { tileIndex = j; draw(); }).catch(() => {});
  function tile(k) {
    if (TILES.has(k)) return TILES.get(k);
    TILES.set(k, null);
    const [i, j] = k.split("_").map(Number), ox = i * 1000, oy = j * 1000;
    fetch(`frame-tiles/${k}.txt`).then((r) => r.ok ? r.text() : "").then((t) => {
      const rings = [];
      for (const line of t.split("\n")) { if (!line) continue; const a = line.split(","), q = new Float32Array(a.length); for (let n = 0; n < a.length; n += 2) { q[n] = ox + a[n] / 10; q[n + 1] = oy + a[n + 1] / 10; } rings.push(q); }
      TILES.set(k, rings); draw();
    }).catch(() => TILES.set(k, false));
    return null;
  }

  // ------------------------------------------------------------------ the view
  let W = 0, H = 0, DPR = 1, s = 1, ox = 0, oy = 0, hover = null, lastHash = "";
  const toW = (X, Y) => [(X - ox) / s, (Y - oy) / s];
  function resize() { DPR = window.devicePixelRatio || 1; W = cv.clientWidth; H = cv.clientHeight; cv.width = W * DPR; cv.height = H * DPR; draw(); }
  function fit(bb, pad = 40) { s = Math.min((W - 2 * pad) / (bb[2] - bb[0]), (H - 2 * pad - 100) / (bb[3] - bb[1])); ox = W / 2 - s * (bb[0] + bb[2]) / 2; oy = H / 2 + 30 - s * (bb[1] + bb[3]) / 2; saveView(); draw(); }
  function saveView() { try { const c = toW(W / 2, H / 2); lastHash = `#${Math.round(c[0])},${Math.round(c[1])},${s.toFixed(4)}`; history.replaceState(null, "", location.pathname + location.search + lastHash); } catch (e) {} }
  function viewFromHash() { const hv = location.hash.slice(1).split(",").map(Number); if (hv.length !== 3 || !hv.every(isFinite) || hv[2] <= 0) return false; s = hv[2]; ox = W / 2 - s * hv[0]; oy = H / 2 - s * hv[1]; return true; }
  const viewBB = (m = 0) => { const a = toW(0, 0), b = toW(W, H); return [a[0] - m, a[1] - m, b[0] + m, b[1] + m]; };
  function path(pts, close) { ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]); if (close) ctx.closePath(); }

  function draw() {
    if (!W) return;
    const P = PAL(), v = viewBB(50), px = 1 / s;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.fillStyle = css("--paper"); ctx.fillRect(0, 0, W, H);
    ctx.setTransform(DPR * s, 0, 0, DPR * s, DPR * ox, DPR * oy);
    ctx.fillStyle = P.land; ctx.fillRect(0, 0, FW, FH);
    // districts: a faint fill each, so neighbours read apart
    if (LAYERS.districts) for (const d of F.districts) { if (!hit(d.bb, v)) continue; ctx.beginPath(); for (const r of d.rings) for (const ring of r) { ctx.moveTo(ring[0][0], ring[0][1]); for (let i = 1; i < ring.length; i++) ctx.lineTo(ring[i][0], ring[i][1]); ctx.closePath(); } ctx.fillStyle = P.dfill[d.n % 4]; ctx.fill("evenodd"); }
    if (LAYERS.water) { ctx.fillStyle = css("--water"); ctx.strokeStyle = css("--water-line"); ctx.lineWidth = px; for (const w of F.water) { if (!hit(w.bb, v)) continue; ctx.beginPath(); for (const ring of w) { ctx.moveTo(ring[0][0], ring[0][1]); for (let i = 1; i < ring.length; i++) ctx.lineTo(ring[i][0], ring[i][1]); ctx.closePath(); } ctx.fill("evenodd"); ctx.stroke(); } }
    // real roofs: only when the view is under about 4 km across
    const roofsOn = LAYERS.roofs && tileIndex && (v[2] - v[0]) < 4500;
    if (roofsOn) {
      ctx.fillStyle = P.roof;
      for (let i = Math.max(0, Math.floor(v[0] / 1000)); i <= Math.min(27, Math.floor(v[2] / 1000)); i++) for (let j = Math.max(0, Math.floor(v[1] / 1000)); j <= Math.min(11, Math.floor(v[3] / 1000)); j++) {
        const k = i + "_" + j; if (!tileIndex.count[k]) continue;
        const rings = tile(k); if (!rings) continue;
        ctx.beginPath();
        for (const q of rings) { if (q[0] < v[0] || q[0] > v[2] || q[1] < v[1] || q[1] > v[3]) continue; ctx.moveTo(q[0], q[1]); for (let n = 2; n < q.length; n += 2) ctx.lineTo(q[n], q[n + 1]); ctx.closePath(); }
        ctx.fill();
      }
    }
    // roads: secondary under primary under trunk under motorway; ramps thinner; rail dashed; bridges outlined on top
    ctx.lineJoin = "round"; ctx.lineCap = "round";
    for (const k of ["secondary", "primary", "trunk", "motorway"]) {
      if (!LAYERS[k]) continue;
      ctx.strokeStyle = P[k];
      for (const link of [1, 0]) {
        if (link && !LAYERS.links) continue;
        ctx.lineWidth = Math.max(RW[k][0] * (link ? 0.5 : 1), RW[k][1] * (link ? 0.6 : 1) * px);
        ctx.beginPath();
        for (const r of F.roads) if (r.k === k && r.l === link && hit(r.bb, v)) { ctx.moveTo(r.p[0][0], r.p[0][1]); for (let i = 1; i < r.p.length; i++) ctx.lineTo(r.p[i][0], r.p[i][1]); }
        ctx.stroke();
      }
    }
    if (LAYERS.rail) { ctx.strokeStyle = P.rail; ctx.lineWidth = Math.max(RW.rail[0], RW.rail[1] * px); ctx.setLineDash([8 * px, 5 * px]); ctx.beginPath(); for (const r of F.roads) if (r.k === "rail" && hit(r.bb, v)) { ctx.moveTo(r.p[0][0], r.p[0][1]); for (let i = 1; i < r.p.length; i++) ctx.lineTo(r.p[i][0], r.p[i][1]); } ctx.stroke(); ctx.setLineDash([]); }
    if (LAYERS.bridges) { ctx.strokeStyle = P.bridge; ctx.lineCap = "butt"; ctx.lineWidth = Math.max(12, 3 * px); ctx.globalAlpha = 0.85; ctx.beginPath(); for (const r of F.roads) if (r.k === "bridge" && hit(r.bb, v)) { ctx.moveTo(r.p[0][0], r.p[0][1]); for (let i = 1; i < r.p.length; i++) ctx.lineTo(r.p[i][0], r.p[i][1]); } ctx.stroke(); ctx.globalAlpha = 1; ctx.lineCap = "round"; }
    // district borders, then the unsure lines and lines still to trace, dashed in their own colours
    if (LAYERS.districts) { ctx.strokeStyle = P.dline; ctx.lineWidth = 1.4 * px; for (const d of F.districts) if (hit(d.bb, v)) for (const r of d.rings) { path(r[0], true); ctx.stroke(); } }
    if (LAYERS.unsure) for (const l of F.lines) { if (!hit(l.bb, v)) continue; path(l.p); ctx.strokeStyle = l.k === "unsure" ? P.unsure : P.trace; ctx.lineWidth = (l === hover ? 5 : 3) * px; ctx.setLineDash(l.k === "unsure" ? [9 * px, 6 * px] : [3 * px, 5 * px]); ctx.stroke(); ctx.setLineDash([]); }
    // the frame's edge
    ctx.strokeStyle = P.frame; ctx.lineWidth = 2 * px; ctx.strokeRect(0, 0, FW, FH);

    // labels in screen space
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    const taken = [];
    const free = (x0, y0, x1, y1) => { for (const b of taken) if (!(x1 < b[0] || x0 > b[2] || y1 < b[1] || y0 > b[3])) return false; taken.push([x0, y0, x1, y1]); return true; };
    const text = (t, X, Y, font, col, halo = 3) => { ctx.font = font; ctx.lineWidth = halo; ctx.strokeStyle = css("--paper"); ctx.strokeText(t, X, Y); ctx.fillStyle = col; ctx.fillText(t, X, Y); };
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    if (LAYERS.districts) for (const d of F.districts) {
      const X = d.at[0] * s + ox, Y = d.at[1] * s + oy; if (X < -50 || X > W + 50 || Y < -20 || Y > H + 20) continue;
      const t = s < 0.045 ? String(d.n) : `${d.n}. ${d.name}`; ctx.font = "700 13px -apple-system, sans-serif"; const w = ctx.measureText(t).width;
      if (free(X - w / 2 - 2, Y - 9, X + w / 2 + 2, Y + 9)) text(t, X, Y, "700 13px -apple-system, sans-serif", css("--ink"));
    }
    if (LAYERS.unsure) {   // each line's question, at the middle of its longest piece in view
      const done = new Set();
      for (const l of [...F.lines].sort((a, b) => (a === hover ? -1 : b === hover ? 1 : 0))) {
        if (!hit(l.bb, viewBB(0)) || done.has(l.q)) continue;
        const m = l.p[Math.floor(l.p.length / 2)], X = m[0] * s + ox, Y = m[1] * s + oy;
        if (X < 0 || X > W || Y < 0 || Y > H) continue;
        ctx.font = "600 11px -apple-system, sans-serif"; const w = ctx.measureText(l.q).width;
        if (!free(X - w / 2 - 2, Y - 16, X + w / 2 + 2, Y - 2)) continue;
        done.add(l.q); text(l.q, X, Y - 9, "600 11px -apple-system, sans-serif", l.k === "unsure" ? P.unsure : P.trace);
      }
      for (const n of F.notes) { const X = n.at[0] * s + ox, Y = n.at[1] * s + oy + 16; if (X < 0 || X > W || Y < 0 || Y > H) continue; ctx.font = "600 11px -apple-system, sans-serif"; const w = ctx.measureText(n.q).width; if (free(X - w / 2, Y - 7, X + w / 2, Y + 7)) text(n.q, X, Y, "600 11px -apple-system, sans-serif", P.trace); }
    }
    if (LAYERS.places) {   // biggest places first; small ones appear as you zoom in
      const minRoof = s > 0.4 ? 0 : s > 0.2 ? 0.05 : s > 0.1 ? 0.25 : s > 0.06 ? 0.6 : 1.5;
      for (const p of F.places) {
        if (p.r < minRoof) break;
        const X = p.at[0] * s + ox, Y = p.at[1] * s + oy; if (X < 0 || X > W || Y < 0 || Y > H) continue;
        ctx.font = "11px -apple-system, sans-serif"; const w = ctx.measureText(p.n).width;
        if (!free(X - w / 2 - 1, Y + 1, X + w / 2 + 1, Y + 15)) continue;
        ctx.fillStyle = css("--muted"); ctx.beginPath(); ctx.arc(X, Y, 2, 0, 7); ctx.fill();
        text(p.n, X, Y + 8, "11px -apple-system, sans-serif", css("--muted"), 2.5);
      }
    }
    ctx.textAlign = "start"; ctx.textBaseline = "alphabetic";
    drawScale();
    if (LAYERS.roofs && tileIndex && !roofsOn) status3.textContent = "Real roofs show when zoomed in under 4.5 km across";
    else status3.textContent = LAYERS.roofs && !tileIndex ? "No real roofs yet: run scripts/frame_footprints.py" : "Study underlay: real Lagos at 1:3. Not map data.";
  }
  function drawScale() {
    const steps = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000];
    const m = steps.find((x) => x * s > 80) || 10000, L = m * s, X = 16, Y = H - 52;
    ctx.fillStyle = css("--ink"); ctx.fillRect(X, Y, L, 2); ctx.fillRect(X, Y - 5, 1.5, 7); ctx.fillRect(X + L - 1.5, Y - 5, 1.5, 7);
    ctx.font = "11px -apple-system, sans-serif"; ctx.fillText((m >= 1000 ? m / 1000 + " km" : m + " m") + " Gidi (" + (m * 3 >= 1000 ? m * 3 / 1000 + " km" : m * 3 + " m") + " real)", X + L + 6, Y + 3);
  }

  // ------------------------------------------------------------------ status line
  const status1 = $("where"), status2 = $("pending"), status3 = $("checks");
  status2.textContent = `${F.districts.length} districts · ${F.places.length} places in the frame · ${F.lines.length} unsure or to-trace lines`;
  function where(p) {
    const [la, lo] = latlon(p[0], p[1]), d = districtAt(p);
    status1.textContent = `x ${Math.round(p[0])} m, y ${Math.round(p[1])} m · real ${la.toFixed(5)}, ${lo.toFixed(5)}` + (d ? ` · ${d.n}. ${d.name}` : "") + (hover ? ` · ${hover.q}` : "");
  }

  // ------------------------------------------------------------------ pan and zoom
  let drag = null;
  cv.addEventListener("pointerdown", (ev) => { drag = { x: ev.clientX, y: ev.clientY, ox, oy }; cv.setPointerCapture(ev.pointerId); cv.classList.add("panning"); });
  cv.addEventListener("pointermove", (ev) => {
    if (drag) { ox = drag.ox + ev.clientX - drag.x; oy = drag.oy + ev.clientY - drag.y; draw(); return; }
    const p = toW(ev.clientX, ev.clientY);
    let h = null, bd = 6 / s;
    if (LAYERS.unsure) for (const l of F.lines) if (hit(l.bb, [p[0] - bd, p[1] - bd, p[0] + bd, p[1] + bd])) { const d = lineDist(p, l.p); if (d < bd) { bd = d; h = l; } }
    if (h !== hover) { hover = h; draw(); }
    where(p);
  });
  cv.addEventListener("pointerup", () => { if (drag) { drag = null; cv.classList.remove("panning"); saveView(); } });
  cv.addEventListener("wheel", (ev) => {
    ev.preventDefault();
    const k = Math.exp(-ev.deltaY * (ev.ctrlKey ? 0.01 : 0.0015)), ns = Math.max(0.01, Math.min(20, s * k));
    ox = ev.clientX - (ev.clientX - ox) * ns / s; oy = ev.clientY - (ev.clientY - oy) * ns / s; s = ns; draw(); saveView();
  }, { passive: false });
  window.addEventListener("keydown", (ev) => { if (ev.key === "0") fit([0, 0, FW, FH]); });
  $("fit").addEventListener("click", () => fit([0, 0, FW, FH]));
  $("theme").addEventListener("click", () => { const r = document.documentElement; r.dataset.theme = isDark() ? "light" : "dark"; draw(); });
  window.addEventListener("resize", resize);
  window.addEventListener("hashchange", () => { if (location.hash !== lastHash && viewFromHash()) draw(); });
  resize();
  if (!viewFromHash()) fit([0, 0, FW, FH]); else draw();
})();
