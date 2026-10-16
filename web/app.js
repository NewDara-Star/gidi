/* Gidi Maps: a Google Maps–style viewer for the Gidi city plan (map v0.3).
   Data: window.GIDI (metres, origin top-left, y down). React 18 UMD, no JSX. */
(function () {
  const { useState, useRef, useEffect, useMemo, useCallback, memo } = React;
  const h = React.createElement;
  const G = window.GIDI;
  const [MW, MH] = G.size;

  const ACT_NAME = { 1: "Act 1 · Survive", 2: "Act 2 · Hustle", 3: "Act 3 · Empire" };
  const OKADA = {
    ban: { label: "Okada banned", note: "Taskforce seizes bikes here" },
    sweep: { label: "Okada sweeps", note: "Random taskforce raids" },
    free: { label: "Okada country", note: "Ride freely" },
  };
  const TYPE = {
    story: { label: "Story", glyph: "★" }, market: { label: "Market", glyph: "M" },
    transit: { label: "Transport", glyph: "T" }, danger: { label: "Danger", glyph: "!" },
    check: { label: "Checkpoint", glyph: "✕" }, night: { label: "Nightlife", glyph: "☾" },
    landmark: { label: "Landmark", glyph: "◆" }, industry: { label: "Industry", glyph: "▲" },
    water: { label: "Water", glyph: "≈" }, gov: { label: "Government", glyph: "▣" },
    park: { label: "Motor park", glyph: "≡" }, shopping: { label: "Shopping", glyph: "S" }, food: { label: "Food", glyph: "♨" },
    church: { label: "Church", glyph: "✝", civic: 1, safe: 1 }, mosque: { label: "Mosque", glyph: "☪", civic: 1, safe: 1 },
    school: { label: "School", glyph: "✎", civic: 1, safe: 1 }, hospital: { label: "Hospital", glyph: "H", civic: 1, safe: 1 },
    clinic: { label: "Clinic", glyph: "+", civic: 1, safe: 1 }, chemist: { label: "Chemist", glyph: "℞", civic: 1 },
    police: { label: "Police", glyph: "P", civic: 1 }, fire: { label: "Fire station", glyph: "F", civic: 1 },
    council: { label: "Government", glyph: "▣", civic: 1 }, fuel: { label: "Petrol station", glyph: "⬢", civic: 1 },
    bank: { label: "Bank", glyph: "₦", civic: 1 }, sport: { label: "Football pitch", glyph: "◎", civic: 1 },
    betting: { label: "Betting / viewing centre", glyph: "◇", civic: 1 }, cemetery: { label: "Cemetery", glyph: "†", civic: 1 },
  };
  const CIVIC_ORDER = ["church", "mosque", "school", "hospital", "clinic", "chemist", "police", "fire", "council", "fuel", "bank", "sport", "betting", "cemetery"];
  window.GIDI_TYPE = TYPE;
  const byId = Object.fromEntries(G.districts.map((d) => [d.id, d]));
  const ACT_ORDER = [1, 2, 3];

  const pts2d = (pts) => "M" + pts.map((p) => p[0] + " " + p[1]).join("L");
  const poly2d = (rings) => rings.map((r) => pts2d(r) + "Z").join("");
  const centroid = (ring) => {
    let x = 0, y = 0, a = 0;
    for (let i = 0; i < ring.length - 1; i++) {
      const [x0, y0] = ring[i], [x1, y1] = ring[i + 1];
      const f = x0 * y1 - x1 * y0; a += f; x += (x0 + x1) * f; y += (y0 + y1) * f;
    }
    a *= 0.5; return [x / (6 * a), y / (6 * a)];
  };
  const bbox = (pts) => {
    let a = [Infinity, Infinity, -Infinity, -Infinity];
    pts.forEach(([x, y]) => { a = [Math.min(a[0], x), Math.min(a[1], y), Math.max(a[2], x), Math.max(a[3], y)]; });
    return a;
  };
  const CENT = Object.fromEntries(G.districts.map((d) => [d.id, centroid(d.poly[0])]));
  const LABEL_AT = { hub: [0, -120], maze: [40, -80], watertown: [-60, 120], foodgate: [0, 0], railside: [0, -200] };

  const streetPaths = Object.fromEntries(Object.entries(G.streets).map(([k, v]) => [k, v.map(pts2d).join("")]));
  const rectPath = (pts) => "M" + pts.map((p) => p[0] + " " + p[1]).join("L") + "Z";
  const bldPaths = Object.entries(G.buildings || {}).map(([k, v]) => [k, v.map((b) => rectPath(b.slice(1))).join("")]);
  const parcelPaths = Object.entries(G.parcels || {}).flatMap(([k, v]) => v.map((p, i) => ({ key: k + i, kind: p.kind.replace(" ", "-"), d: rectPath(p.pts) })));
  const lanePaths = Object.entries(G.lanes || {}).map(([k, v]) => [k, v.map(pts2d).join("")]);
  const footPaths = Object.entries(G.paths || {}).map(([k, v]) => [k, v.map(pts2d).join("")]);
  const wallPaths = Object.entries(G.walls || {}).map(([k, v]) => [k, v.map(pts2d).join("")]);
  const gatePath = (G.gates || []).map((q) => pts2d(q.pts)).join("");
  // Open gutters (ism 15, scripts/isms.py): runs beside the roads, open or slab-covered, blocked stretches, and plank/slab crossings
  const subPts = (pts, a, b) => {   // the part of a polyline between two distances along it
    const res = []; let t = 0;
    for (let i = 0; i + 1 < pts.length; i++) {
      const [x0, y0] = pts[i], [x1, y1] = pts[i + 1], L = Math.hypot(x1 - x0, y1 - y0);
      if (t + L > a && t < b && L > 0) {
        const u0 = Math.max(0, (a - t) / L), u1 = Math.min(1, (b - t) / L);
        if (!res.length) res.push([x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0]);
        res.push([x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1]);
      }
      t += L;
    }
    return res;
  };
  const gutterPath = { open: "", covered: "", rubbish: "", green_water: "", slab: "", plank: "" };
  (G.gutters || []).forEach((r) => {
    gutterPath[r.state] += pts2d(r.pts);
    (r.blocked || []).forEach((b) => { const sp = subPts(r.pts, b.from, b.to); if (sp.length > 1) gutterPath[b.fill] += pts2d(sp); });
  });
  (G.gutter_crossings || []).forEach((c) => {
    const a = c.ang * Math.PI / 180, dx = Math.cos(a) * c.w / 2, dy = Math.sin(a) * c.w / 2;
    gutterPath[c.kind] += "M" + (c.pt[0] - dx).toFixed(1) + " " + (c.pt[1] - dy).toFixed(1) + "L" + (c.pt[0] + dx).toFixed(1) + " " + (c.pt[1] + dy).toFixed(1);
  });
  const mainsPath = G.mains.map((m, i) => ({ id: "main" + i, d: pts2d(m.pts), name: m.name, district: m.d }));
  // The ground plan (scripts/cross_sections.py, scripts/furniture.py): districts built to the agreed cross-sections show every
  // road at true width - walkway, gutter, carriageway - and every piece of street furniture where it stands.
  const XS = G.cross_sections || {};
  const PLAN_D = G.districts.filter((d) => d.fabric === "lagos");
  const planIds = new Set(PLAN_D.map((d) => d.id));
  const planClip = PLAN_D.map((d) => poly2d(d.poly)).join("");
  const planRoads = { lane: "", street: "", main: "", art: "", exp: "" };
  Object.entries(G.streets || {}).forEach(([d, L]) => { if (planIds.has(d)) L.forEach((p) => { planRoads.street += pts2d(p); }); });
  Object.entries(G.lanes || {}).forEach(([d, L]) => { if (planIds.has(d)) L.forEach((p) => { planRoads.lane += pts2d(p); }); });
  G.mains.forEach((m) => { if (planIds.has(m.d)) planRoads.main += pts2d(m.pts); });
  G.arterials.forEach((a) => { if (planRoads[a.cls] !== undefined) planRoads[a.cls] += pts2d(a.pts); });
  // road surfaces (scripts/surfaces.py): each street's carriageway in its own surface; tar stays the plain road colour
  const SURF = G.surfaces || {};
  const planSurf = {};
  const addSurf = (cls, s, p) => { if (s && s !== "tar") { const k = cls + "|" + s; planSurf[k] = (planSurf[k] || "") + pts2d(p); } };
  Object.entries(G.streets || {}).forEach(([d, L]) => { if (planIds.has(d)) L.forEach((p, i) => addSurf("street", ((SURF.streets || {})[d] || [])[i], p)); });
  Object.entries(G.lanes || {}).forEach(([d, L]) => { if (planIds.has(d)) L.forEach((p, i) => addSurf("lane", ((SURF.lanes || {})[d] || [])[i], p)); });
  G.mains.forEach((m, i) => { if (planIds.has(m.d)) addSurf("main", (SURF.mains || [])[i], m.pts); });
  G.arterials.forEach((a, i) => { if (planRoads[a.cls] !== undefined) addSurf(a.cls, (SURF.arterials || [])[i], a.pts); });
  const band = (k, part) => { const x = XS[k]; if (!x) return 0; const c = x.carriageway; return part === "c" ? c : part === "g" ? c + 2 * x.gutter : c + 2 * (x.gutter + x.walkway); };
  const FURN = G.furniture || [];
  const islands = (G.junctions || []).filter((j) => j.kind === "roundabout" && j.island_r > 0);

  // Search index
  const INDEX = [
    ...G.districts.map((d) => ({ kind: "district", id: d.id, name: d.name, sub: "District · " + d.inspired })),
    ...G.pois.map((p, i) => ({ kind: "poi", id: i, name: p.name, sub: TYPE[p.type].label + " · " + byId[p.d].name })),
    ...G.arterials.map((a, i) => ({ kind: "road", id: i, name: a.name, sub: "Main road" })),
    ...G.mains.map((m, i) => ({ kind: "street", id: i, name: m.name, sub: "Street · " + byId[m.d].name })),
  ];

  function load(key, def) { try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : def; } catch (e) { return def; } }
  function save(key, v) { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }

  function furnitureGlyph(f, i) {   // street furniture in metres, at its spot; f.ang (degrees) points at the road or the traffic
    const t = `translate(${f.x} ${f.y}) rotate(${f.ang})`;
    if (f.kind === "pole") return h("circle", { key: i, cx: f.x, cy: f.y, r: 0.35, className: "fu-pole" });
    if (f.kind === "street light") return h("g", { key: i, transform: t }, h("line", { x1: 0, y1: 0, x2: 2.2, y2: 0, className: "fu-arm" }), h("circle", { r: 0.55, className: "fu-light" }));
    if (f.kind === "transformer") return h("rect", { key: i, x: -0.8, y: -0.6, width: 1.6, height: 1.2, transform: t, className: "fu-transformer" });
    if (f.kind === "traffic light") return h("g", { key: i, transform: t }, h("rect", { x: -0.35, y: -0.9, width: 0.7, height: 1.8, className: "fu-signal" }),
      h("circle", { cx: 0, cy: -0.5, r: 0.22, fill: "#e53935" }), h("circle", { cx: 0, cy: 0, r: 0.22, fill: "#fbc02d" }), h("circle", { cx: 0, cy: 0.5, r: 0.22, fill: "#43a047" }));
    if (f.kind === "bus stop") return h("g", { key: i, transform: t }, h("rect", { x: -0.6, y: -1.6, width: 1.2, height: 3.2, className: "fu-bus" }),
      h("text", { x: 0, y: 0.45, className: "fu-label", transform: `rotate(${-f.ang})` }, "B"));
    if (f.kind === "lasma post") return h("g", { key: i, transform: t }, h("rect", { x: -0.8, y: -0.8, width: 1.6, height: 1.6, className: "fu-lasma" }),
      h("text", { x: 0, y: 0.45, className: "fu-label", transform: `rotate(${-f.ang})` }, "L"));
    if (["wheelbarrow vendor", "fruit seller", "parking boy", "agbero", "police kiosk", "overhead sign", "task force truck", "bread hawker"].includes(f.kind))   // people placed by hand on the walkway
      return h("g", { key: i }, h("circle", { cx: f.x, cy: f.y, r: 0.6, className: "fu-person" }), h("title", null, f.kind + (f.name ? ": " + f.name : "")));
    return null;
  }

  /* ---------- static map layers (memoised by zoom bucket) ---------- */
  const Base = memo(function Base({ zb, layers, selected }) {
    const z = Math.pow(2, zb);
    const px = (p) => p / z; // screen pixels -> metres
    const w = (metres, minPx) => Math.max(metres, px(minPx));
    const showStreets = z > 0.12;
    return h("g", null,
      h("rect", { x: -2000, y: -2000, width: MW + 4000, height: MH + 4000, className: "bush" }),
      G.ocean.map((r, i) => h("path", { key: "o" + i, d: pts2d(r) + "Z", className: "ocean" })),
      h("path", { d: poly2d(G.water), className: "water" }),
      G.districts.map((d) =>
        h("path", {
          key: d.id, d: poly2d(d.poly), "data-district": d.id,
          className: "land" + (layers.acts ? " act" + d.act : "") + (selected === d.id ? " sel" : ""),
          style: { strokeWidth: px(selected === d.id ? 2.5 : 1) },
        })),
      layers.okada && G.districts.filter((d) => d.okada !== "free").map((d) =>
        h("path", { key: "ok" + d.id, d: poly2d(d.poly), className: "okada-" + d.okada, style: { strokeWidth: px(1.5) }, pointerEvents: "none" })),
      showStreets && h("g", { pointerEvents: "none" }, parcelPaths.map((p) => h("path", { key: p.key, d: p.d, className: "parcel " + p.kind }))),
      z > 0.22 && h("g", { pointerEvents: "none" }, bldPaths.map(([k, d]) => h("path", { key: "b" + k, d, className: "bld", style: { strokeWidth: px(0.5) } }))),
      (G.canals || []).map((c, i) => h("path", { key: "cn" + i, d: pts2d(c.pts), className: "canal", style: { strokeWidth: w(6, 1.2) }, pointerEvents: "none" })),
      z > 0.5 && h("g", { pointerEvents: "none" }, wallPaths.map(([k, d]) => h("path", { key: "w" + k, d, className: "wall", style: { strokeWidth: px(0.6) } }))),
      z > 0.3 && h("g", { pointerEvents: "none" }, lanePaths.map(([k, d]) => h("path", { key: "l" + k, d, className: "lane", style: { strokeWidth: w(3, 0.8) } }))),
      z > 0.5 && h("g", { pointerEvents: "none" }, footPaths.map(([k, d]) => h("path", { key: "fp" + k, d, className: "footpath", style: { strokeWidth: w(1.5, 0.6), strokeDasharray: px(3) + " " + px(2) } }))),
      showStreets && h("g", { pointerEvents: "none" },
        Object.entries(streetPaths).map(([k, d]) => h("path", { key: "sc" + k, d, className: "st-case", style: { strokeWidth: w(9, 1.6) } })),
        Object.entries(streetPaths).map(([k, d]) => h("path", { key: "s" + k, d, className: "st", style: { strokeWidth: w(6, 0.9) } })),
        mainsPath.map((m) => h("path", { key: m.id + "c", d: m.d, className: "mn-case", style: { strokeWidth: w(15, 2.6) } })),
        mainsPath.map((m) => h("path", { key: m.id, id: m.id, d: m.d, className: "mn", style: { strokeWidth: w(11, 1.8) } }))),
      layers.gutters && z > 1.2 && h("g", { pointerEvents: "none", fill: "none", strokeLinecap: "butt", strokeLinejoin: "round" },
        h("path", { d: gutterPath.covered, className: "gut-cov", style: { strokeWidth: w(0.8, 0.9) } }),
        h("path", { d: gutterPath.open, className: "gut-open", style: { strokeWidth: w(0.8, 0.9) } }),
        h("path", { d: gutterPath.rubbish, className: "gut-rubbish", style: { strokeWidth: w(0.8, 0.9) } }),
        h("path", { d: gutterPath.green_water, className: "gut-green", style: { strokeWidth: w(0.8, 0.9) } }),
        h("path", { d: gutterPath.plank, className: "gut-plank", style: { strokeWidth: w(1.3, 1.4) } }),
        h("path", { d: gutterPath.slab, className: "gut-slab", style: { strokeWidth: w(1.5, 1.6) } })),
      G.boardwalks && h("g", { pointerEvents: "none" }, G.boardwalks.map((b, i) => h("path", { key: i, d: pts2d(b), className: "boardwalk", style: { strokeWidth: w(3, 1) } }))),
      h("g", { pointerEvents: "none" },
        G.arterials.map((a, i) => h("path", { key: "ac" + i, d: pts2d(a.pts), className: "ar-case " + a.cls, style: { strokeWidth: w(a.cls === "exp" ? 34 : 26, a.cls === "exp" ? 5.5 : 4.5) } })),
        G.arterials.map((a, i) => h("path", { key: "a" + i, id: "art" + i, d: pts2d(a.pts), className: "ar " + a.cls, style: { strokeWidth: w(a.cls === "exp" ? 26 : 19, a.cls === "exp" ? 3.8 : 3) } }))),
      layers.plan && planClip && z > 0.8 && h("g", { pointerEvents: "none", clipPath: "url(#planclip)", fill: "none", strokeLinecap: "butt", strokeLinejoin: "round" },
        ["exp", "art", "main", "street", "lane"].map((k) => planRoads[k] && h("path", { key: "pw" + k, d: planRoads[k], className: "plan-walk", style: { strokeWidth: band(k, "w") } })),
        ["exp", "art", "main", "street", "lane"].map((k) => planRoads[k] && h("path", { key: "pg" + k, d: planRoads[k], className: "plan-gutter", style: { strokeWidth: band(k, "g") } })),
        ["exp", "art", "main", "street", "lane"].map((k) => planRoads[k] && h("path", { key: "pc" + k, d: planRoads[k], className: "plan-road " + k, style: { strokeWidth: band(k, "c") } })),
        Object.entries(planSurf).map(([k, d]) => h("path", { key: "ps" + k, d, className: "surf-" + k.split("|")[1], style: { strokeWidth: band(k.split("|")[0], "c") } })),
        (G.encroach || []).map((e, i) => h("path", { key: "en" + i, d: pts2d(e.pts) + "Z", className: "plan-spill" }))),
      layers.plan && z > 0.8 && h("g", { pointerEvents: "none" },
        islands.map((j, i) => h("circle", { key: "is" + i, cx: j.x, cy: j.y, r: j.island_r, className: "plan-island" })),
        (G.quays || []).map((q, i) => h("path", { key: "q" + i, d: pts2d(q.pts), className: "plan-quay", style: { strokeWidth: w(1.2, 1.5) } }))),
      layers.plan && z > 1.6 && h("g", { pointerEvents: "none" }, FURN.map((f, i) => furnitureGlyph(f, i))),
      // monuments placed by hand (blender/gidi_kit/monuments.py): a marker and its name; an arch is a bar across its road
      z > 0.5 && h("g", { pointerEvents: "none" }, (G.monuments || []).map((m, i) => m.model === "arch"
        ? h("g", { key: "mo" + i, transform: `translate(${m.x} ${m.y}) rotate(${m.ang + 90})` },
            h("rect", { x: -(m.span || 16) / 2, y: -0.8, width: m.span || 16, height: 1.6, className: "mon-arch" }))
        : h("g", { key: "mo" + i },
            h("circle", { cx: m.x, cy: m.y, r: w(2.2, 4), className: "mon" }),
            z > 1 && h("text", { x: m.x + w(3, 6), y: m.y, className: "mon-label", style: { fontSize: w(4, 10) } }, m.name || m.model)))),
      h("g", { pointerEvents: "none" },   // flyovers and rail bridges sit above the roads; skywalks above everything
        (G.structures || []).filter((s) => s.kind === "flyover").map((s, i) => h("path", { key: "fc" + i, d: pts2d(s.pts), className: "fly-case", style: { strokeWidth: w(s.width + 6, 5) } })),
        (G.structures || []).filter((s) => s.kind === "flyover").map((s, i) => h("path", { key: "f" + i, d: pts2d(s.pts), className: "fly", style: { strokeWidth: w(s.width, 3.6) } }))),
      z > 0.3 && gatePath && h("path", { d: gatePath, className: "gate", style: { strokeWidth: w(1.4, 1.6) }, pointerEvents: "none" }),
      layers.rail && h("g", { pointerEvents: "none" },
        h("path", { d: pts2d(G.rail.pts), className: "rail-case", style: { strokeWidth: px(5) } }),
        h("path", { d: pts2d(G.rail.pts), className: "rail", style: { strokeWidth: px(2.5), strokeDasharray: px(7) + " " + px(5) } })),
      z > 0.22 && h("g", { pointerEvents: "none" }, (G.structures || []).filter((s) => s.kind === "skywalk" || s.kind === "footbridge" || s.kind === "jetty").map((s, i) => h("path", { key: "sw" + i, d: pts2d(s.pts), className: "skywalk", style: { strokeWidth: w(s.width, 1.2) } }))),
      layers.ferries && G.ferries.map((f, i) => h("path", { key: "f" + i, d: pts2d(f.pts), className: "ferry", style: { strokeWidth: px(2), strokeDasharray: px(2) + " " + px(5) }, pointerEvents: "none" })),
      // street names along paths
      layers.names && z > 0.55 && h("g", { pointerEvents: "none", className: "street-names" },
        mainsPath.map((m) => h("text", { key: "t" + m.id, style: { fontSize: px(11) }, dy: px(3.8) },
          h("textPath", { href: "#" + m.id, startOffset: "50%", textAnchor: "middle" }, m.name)))),
      layers.names && z > 0.09 && h("g", { pointerEvents: "none", className: "road-names" },
        G.arterials.map((a, i) => h("text", { key: "at" + i, style: { fontSize: px(11.5) }, dy: px(4) },
          h("textPath", { href: "#art" + i, startOffset: "50%", textAnchor: "middle" }, a.name))))
    );
  });

  /* ---------- the app ---------- */
  function App() {
    const wrap = useRef(null);
    const [size, setSize] = useState({ w: 1000, h: 700 });
    const [view, setView] = useState(null); // {cx, cy, z} z = px per metre
    const [layers, setLayers] = useState(() => ({ civic: true, gutters: true, plan: true, ...load("gidi-layers", { acts: true, okada: true, rail: true, ferries: true, places: true, names: true, civic: true }) }));
    const [sel, setSel] = useState(null); // {kind, id}
    const [q, setQ] = useState("");
    const [focusSearch, setFocusSearch] = useState(false);
    const [cursor, setCursor] = useState(null);
    const [panelOpen, setPanelOpen] = useState(true);
    const drag = useRef(null);
    const pointers = useRef(new Map());
    const anim = useRef(null);
    const [dim, setDim] = useState(() => load("gidi-dim", "2d"));
    const api3d = useRef(null);
    useEffect(() => save("gidi-dim", dim), [dim]);

    useEffect(() => save("gidi-layers", layers), [layers]);

    const fit = useCallback((b, pad = 60, s = size) => {
      const [x0, y0, x1, y1] = b;
      const panel = s.w > 760 && panelOpen ? 400 : 0;
      const bottom = s.w <= 760 && panelOpen ? s.h * 0.45 : 0;
      const z = Math.min((s.w - panel - pad * 2) / (x1 - x0), (s.h - bottom - pad * 2 - 60) / (y1 - y0));
      const cx = (x0 + x1) / 2 - (panel / 2) / z;
      const cy = (y0 + y1) / 2 + (bottom / 2 - 30) / z;
      return { cx, cy, z };
    }, [size, panelOpen]);

    useEffect(() => {
      const el = wrap.current;
      const ro = new ResizeObserver(() => {
        const s = { w: el.clientWidth, h: el.clientHeight };
        setSize(s);
        setView((v) => v || fit([0, 0, MW, MH * 0.97], 24, s));
      });
      ro.observe(el);
      return () => ro.disconnect();
    }, []);

    const flyTo = useCallback((target) => {
      cancelAnimationFrame(anim.current);
      const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce) { setView(target); return; }
      setView((from) => {
        if (!from) return target;
        const t0 = performance.now(), D = 450;
        const step = (t) => {
          const k = Math.min(1, (t - t0) / D), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
          const lz = Math.log(from.z) + (Math.log(target.z) - Math.log(from.z)) * e;
          setView({ cx: from.cx + (target.cx - from.cx) * e, cy: from.cy + (target.cy - from.cy) * e, z: Math.exp(lz) });
          if (k < 1) anim.current = requestAnimationFrame(step);
        };
        anim.current = requestAnimationFrame(step);
        return from;
      });
    }, []);

    const select = useCallback((item, fly = true) => {
      setSel(item); setPanelOpen(true);
      if (!item || !fly) return;
      if (item.kind === "district") flyTo(fit(bbox(byId[item.id].poly[0]), 70));
      else if (item.kind === "poi") { const p = G.pois[item.id]; flyTo(fit([p.x - 260, p.y - 200, p.x + 260, p.y + 200], 40)); }
      else if (item.kind === "road") flyTo(fit(bbox(G.arterials[item.id].pts), 60));
      else if (item.kind === "street") flyTo(fit(bbox(G.mains[item.id].pts), 80));
    }, [fit, flyTo]);

    // pointer pan + pinch
    const toWorld = (sx, sy, v = view) => [v.cx + (sx - size.w / 2) / v.z, v.cy + (sy - size.h / 2) / v.z];
    const zoomAt = (sx, sy, factor) => setView((v) => {
      const z = Math.min(Math.max(v.z * factor, 0.04), 6);
      const [wx, wy] = [v.cx + (sx - size.w / 2) / v.z, v.cy + (sy - size.h / 2) / v.z];
      return { z, cx: wx - (sx - size.w / 2) / z, cy: wy - (sy - size.h / 2) / z };
    });
    const onWheel = (e) => {
      cancelAnimationFrame(anim.current);
      const r = wrap.current.getBoundingClientRect();
      zoomAt(e.clientX - r.left, e.clientY - r.top, Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0018)));
    };
    useEffect(() => {
      const el = wrap.current; const f = (e) => { e.preventDefault(); onWheel(e); };
      el.addEventListener("wheel", f, { passive: false });
      return () => el.removeEventListener("wheel", f);
    });
    const onDown = (e) => {
      if (e.target.closest(".ui")) return;
      cancelAnimationFrame(anim.current);
      wrap.current.setPointerCapture(e.pointerId);
      pointers.current.set(e.pointerId, [e.clientX, e.clientY]);
      drag.current = { x: e.clientX, y: e.clientY, v: view, moved: false, target: e.target };
    };
    const onMove = (e) => {
      const r = wrap.current.getBoundingClientRect();
      if (view) setCursor(toWorld(e.clientX - r.left, e.clientY - r.top));
      if (!pointers.current.has(e.pointerId)) return;
      const prev = pointers.current.get(e.pointerId);
      pointers.current.set(e.pointerId, [e.clientX, e.clientY]);
      if (pointers.current.size === 2) {
        const [a, b] = [...pointers.current.values()];
        const other = [...pointers.current.entries()].find(([id]) => id !== e.pointerId)[1];
        const d0 = Math.hypot(prev[0] - other[0], prev[1] - other[1]), d1 = Math.hypot(a[0] - b[0], a[1] - b[1]);
        if (d0 > 0) zoomAt((a[0] + b[0]) / 2 - r.left, (a[1] + b[1]) / 2 - r.top, d1 / d0);
        if (drag.current) drag.current.moved = true;
        return;
      }
      const d = drag.current; if (!d) return;
      const dx = e.clientX - d.x, dy = e.clientY - d.y;
      if (Math.abs(dx) + Math.abs(dy) > 4) d.moved = true;
      if (d.moved) setView({ ...d.v, cx: d.v.cx - dx / d.v.z, cy: d.v.cy - dy / d.v.z });
    };
    const onUp = (e) => {
      pointers.current.delete(e.pointerId);
      const d = drag.current;
      if (pointers.current.size === 0) drag.current = null;
      else if (pointers.current.size === 1) { const [p] = pointers.current.values(); drag.current = { x: p[0], y: p[1], v: view, moved: true }; }
      if (d && !d.moved && pointers.current.size === 0) {
        const el = document.elementFromPoint(e.clientX, e.clientY);
        const dist = el && el.getAttribute && el.getAttribute("data-district");
        if (dist) select({ kind: "district", id: dist }, false);
        else setSel(null);
      }
    };
    const onDbl = (e) => { if (e.target.closest(".ui")) return; const r = wrap.current.getBoundingClientRect(); zoomAt(e.clientX - r.left, e.clientY - r.top, 2); };

    const results = useMemo(() => {
      const s = q.trim().toLowerCase(); if (!s) return [];
      return INDEX.filter((r) => r.name.toLowerCase().includes(s) || r.sub.toLowerCase().includes(s)).slice(0, 8);
    }, [q]);

    if (!view) return h("div", { ref: wrap, className: "map" });
    const z = view.z;
    const zb = Math.round(Math.log2(z) * 4) / 4;
    const sx = (x) => (x - view.cx) * z + size.w / 2, sy = (y) => (y - view.cy) * z + size.h / 2;
    const selDistrict = sel && sel.kind === "district" ? sel.id : sel && sel.kind === "poi" ? G.pois[sel.id].d : null;

    // scale bar
    const nice = [50, 100, 200, 250, 500, 1000, 2000, 5000];
    const metres = nice.find((n) => n * z > 70) || 5000;
    const scaleLabel = metres >= 1000 ? metres / 1000 + " km" : metres + " m";

    const showPlaces = layers.places && z > 0.17;
    const showPoiLabels = z > 0.3;
    const showCivic = layers.civic && z > 0.32;
    const showCivicLabels = z > 0.75;

    const TOPBAR = () =>
      h("div", { className: "topbar ui" },
        h("div", { className: "search" + (focusSearch && results.length ? " open" : "") },
          h("div", { className: "brand" }, "Gidi"),
          h("input", { id: "search", type: "search", placeholder: "Search districts, places, roads", value: q, autoComplete: "off",
            onChange: (e) => setQ(e.target.value), onFocus: () => setFocusSearch(true), onBlur: () => setTimeout(() => setFocusSearch(false), 150),
            onKeyDown: (e) => { if (e.key === "Enter" && results[0]) { select(results[0]); setQ(""); e.target.blur(); } } }),
          focusSearch && results.length > 0 && h("ul", { className: "results" },
            results.map((r) => h("li", { key: r.kind + r.id },
              h("button", { onMouseDown: (e) => e.preventDefault(), onClick: () => { select(r); setQ(""); document.activeElement.blur(); } },
                h("span", { className: "rn" }, r.name), h("span", { className: "rs" }, r.sub)))))),
        h("div", { className: "chips" },
          [["acts", "Acts"], ["okada", "Okada zones"], ["places", "Landmarks"], ["civic", "Civic"], ["rail", "Rail"], ["ferries", "Ferries"], ["names", "Street names"], ["gutters", "Gutters"], ["plan", "Ground plan"]].map(([k, t]) =>
            h("button", { key: k, className: "chip" + (layers[k] ? " on" : ""), "aria-pressed": layers[k], onClick: () => setLayers({ ...layers, [k]: !layers[k] }) }, t))));
    const is3d = dim === "3d";
    const dimBox = h("div", { className: "dim ui" },
      h("div", { className: "seg", role: "group", "aria-label": "Map view" },
        h("button", { id: "dim2d", "aria-pressed": dim === "2d", onClick: () => setDim("2d") }, "2D"),
        h("button", { id: "dim3d", "aria-pressed": is3d, onClick: () => setDim("3d") }, "3D")),
      is3d && h("button", { className: "compass", "aria-label": "Turn the map to face north", onClick: () => api3d.current && api3d.current.north() }, h("span", { id: "compass3d" })));
    const controls3d = h("div", { className: "controls ui" },
      h("button", { "aria-label": "Zoom in", onClick: () => api3d.current && api3d.current.zoom(0.62) }, "+"),
      h("button", { "aria-label": "Zoom out", onClick: () => api3d.current && api3d.current.zoom(1.6) }, "−"),
      h("button", { "aria-label": "Show all of Gidi", className: "fit", onClick: () => api3d.current && api3d.current.home() }, "⤢"));
    if (is3d) return h("div", { ref: wrap, className: "map" },
      h(window.GidiView3D, { sel, select: (item) => { setSel(item); if (item) setPanelOpen(true); }, onReady: (a) => { api3d.current = a; } }),
      TOPBAR(),
      h(Panel, { sel, select, open: panelOpen, setOpen: setPanelOpen, close: () => setSel(null) }),
      dimBox, controls3d);

    return h("div", { ref: wrap, className: "map", onPointerDown: onDown, onPointerMove: onMove, onPointerUp: onUp, onPointerCancel: onUp, onDoubleClick: onDbl },
      h("svg", { className: "canvas", width: size.w, height: size.h, role: "img", "aria-label": "Map of Gidi" },
        h("defs", null,
          h("pattern", { id: "hatch", width: 8, height: 8, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" },
            h("rect", { width: 2.2, height: 8, className: "hatch-line" })),
          h("pattern", { id: "spill", width: 1.6, height: 1.6, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" },
            h("rect", { width: 0.6, height: 1.6, className: "spill-line" })),
          h("clipPath", { id: "planclip" }, h("path", { d: planClip || "M0 0" }))),
        h("g", { transform: `translate(${size.w / 2} ${size.h / 2}) scale(${z}) translate(${-view.cx} ${-view.cy})` },
          h(Base, { zb, layers, selected: selDistrict }))),
      // overlay labels (constant pixel size)
      h("div", { className: "overlay" },
        G.labels.map((l, i) => h("div", { key: "l" + i, className: "lbl " + l.k, style: { left: sx(l.x), top: sy(l.y) } }, l.t)),
        z < 0.75 && G.districts.map((d) => {
          const [cx, cy] = CENT[d.id]; const o = LABEL_AT[d.id] || [0, 0];
          return h("button", { key: d.id, className: "dlabel ui a" + d.act + (selDistrict === d.id ? " on" : ""), style: { left: sx(cx + o[0]), top: sy(cy + o[1]) },
            onClick: () => select({ kind: "district", id: d.id }) },
            h("span", { className: "dn" }, d.name), z > 0.1 && h("span", { className: "dsub" }, d.area.toFixed(1) + " km²"));
        }),
        G.pois.map((p, i) => {
          const isSel = sel && sel.kind === "poi" && sel.id === i;
          const civic = !!p.civic;
          if (!isSel && (civic ? !showCivic : !showPlaces)) return null;
          const x = sx(p.x), y = sy(p.y);
          if (x < -40 || y < -40 || x > size.w + 40 || y > size.h + 40) return null;
          return h("button", { key: "p" + i, className: "poi ui t-" + p.type + (civic ? " civic" : "") + (isSel ? " on" : ""), style: { left: x, top: y },
            onClick: () => select({ kind: "poi", id: i }), "aria-label": p.name },
            h("span", { className: "pin" }, TYPE[p.type].glyph),
            ((civic ? showCivicLabels : showPoiLabels) || isSel) && h("span", { className: "plabel" }, p.name));
        })),
      // search
      TOPBAR(),
      // side panel
      h(Panel, { sel, select, open: panelOpen, setOpen: setPanelOpen, close: () => setSel(null) }),
      // controls
      h("div", { className: "controls ui" },
        h("button", { "aria-label": "Zoom in", onClick: () => zoomAt(size.w / 2, size.h / 2, 1.6) }, "+"),
        h("button", { "aria-label": "Zoom out", onClick: () => zoomAt(size.w / 2, size.h / 2, 1 / 1.6) }, "−"),
        h("button", { "aria-label": "Show all of Gidi", className: "fit", onClick: () => flyTo(fit([0, 0, MW, MH * 0.97], 24)) }, "⤢")),
      dimBox,
      layers.plan && z > 1.6 && planClip && h("div", { className: "plan-legend ui" },
        h("b", null, "Ground plan"),
        [["walk", "walkway"], ["gutter", "gutter (open drain)"], ["spill", "market street: traders on the road (on purpose)"], ["light", "street light"], ["pole", "electricity pole"],
         ["transformer", "transformer"], ["signal", "traffic light"], ["bus", "bus stop"], ["lasma", "LASMA post"], ["island", "roundabout island"],
         ["person", "a trader or a boy, placed by hand"], ["s-worn", "road: worn tar"], ["s-interlock", "road: interlock paving"], ["s-laterite", "road: unpaved red earth"], ["s-sand", "road: unpaved sand"], ["s-mud", "road: mud, waterlogged"]].map(([k, t]) =>
          h("div", { key: k, className: "lg" }, h("i", { className: "sw-" + k }), t))),
      h("div", { className: "scale ui" },
        h("div", { className: "bar", style: { width: metres * z } }), h("span", null, scaleLabel),
        cursor && h("span", { className: "coord" }, `${(cursor[0] / 1000).toFixed(2)} km E · ${((MH - cursor[1]) / 1000).toFixed(2)} km N`)),
      h("div", { className: "credit ui" }, "Gidi map v0.3 · invented city inspired by Lagos · schematic, not to build from street by street"));
  }

  /* ---------- side panel ---------- */
  function Panel({ sel, select, open, setOpen, close }) {
    let body;
    if (!sel) body = h(Overview, { select });
    else if (sel.kind === "district") body = h(District, { d: byId[sel.id], select });
    else if (sel.kind === "poi") {
      const p = G.pois[sel.id]; const d = byId[p.d];
      body = h("div", { className: "card" },
        h("div", { className: "eyebrow t-" + p.type }, TYPE[p.type].label),
        h("h2", null, p.name),
        h("p", { className: "lead" }, p.note),
        h("button", { className: "link", onClick: () => select({ kind: "district", id: d.id }) }, "In " + d.name + " →"),
        h("div", { className: "chiprow" }, h("span", { className: "tag a" + d.act }, ACT_NAME[d.act]), h("span", { className: "tag ok-" + d.okada }, OKADA[d.okada].label),
          p.safe && h("span", { className: "tag safe" }, "Safe ground: never a crime location")));
    } else if (sel.kind === "road") {
      const a = G.arterials[sel.id];
      body = h("div", { className: "card" }, h("div", { className: "eyebrow" }, "Main road"), h("h2", null, a.name),
        h("p", { className: "lead" }, a.cls === "bridge" ? "Bridge. Okada are banned on Gidi's bridges; the taskforce can seize the bike." : a.cls === "exp" ? "Expressway: trucks, tankers, danfos, go-slow at rush hour." : "Arterial road linking districts."));
    } else {
      const m = G.mains[sel.id]; const d = byId[m.d];
      body = h("div", { className: "card" }, h("div", { className: "eyebrow" }, "Street"), h("h2", null, m.name),
        h("p", { className: "lead" }, "A main street of " + d.name + ". Street names are placeholders."),
        h("button", { className: "link", onClick: () => select({ kind: "district", id: d.id }) }, "In " + d.name + " →"));
    }
    return h("aside", { className: "panel ui" + (open ? "" : " shut") },
      h("div", { className: "panel-head" },
        sel && h("button", { className: "back", onClick: close }, "← All districts"),
        h("button", { className: "toggle", "aria-label": open ? "Hide panel" : "Show panel", onClick: () => setOpen(!open) }, open ? "Hide" : "Show details")),
      open && h("div", { className: "panel-body" }, body));
  }

  function CivicBlock({ items, select }) {
    const groups = CIVIC_ORDER.map((t) => [t, items.filter(([p]) => p.type === t)]).filter(([, l]) => l.length);
    return h("div", { className: "civic" },
      groups.map(([t, l]) => h("details", { key: t, className: "cg t-" + t },
        h("summary", null, h("span", { className: "pin small" }, TYPE[t].glyph), h("span", { className: "cgl" }, TYPE[t].label), h("span", { className: "cgn" }, l.length)),
        h("ul", { className: "plist" }, l.map(([p, i]) => h("li", { key: i },
          h("button", { onClick: () => select({ kind: "poi", id: i }) }, h("span", null, h("span", { className: "pn" }, p.name), h("span", { className: "ps" }, p.note)))))))));
  }

  function Overview({ select }) {
    const total = G.districts.reduce((s, d) => s + d.area, 0);
    return h("div", { className: "card" },
      h("div", { className: "eyebrow" }, "Map v0.3"),
      h("h2", null, "Gidi"),
      h("p", { className: "lead" }, "An invented city with the feeling of Lagos. 15 districts merged from Lagos's 20 local governments, " + total.toFixed(1) + " km² of land around a lagoon. Click a district to see what we model there."),
      h("div", { className: "stats" },
        h("div", null, h("b", null, "15"), h("span", null, "districts")),
        h("div", null, h("b", null, total.toFixed(1)), h("span", null, "km² of land")),
        h("div", null, h("b", null, G.pois.length), h("span", null, "places on the map"))),
      ACT_ORDER.map((a) => h("section", { key: a },
        h("h3", { className: "acth a" + a }, ACT_NAME[a]),
        h("ul", { className: "dlist" }, G.districts.filter((d) => d.act === a).map((d) =>
          h("li", { key: d.id }, h("button", { onClick: () => select({ kind: "district", id: d.id }) },
            h("span", { className: "dl-name" }, d.name),
            h("span", { className: "dl-sub" }, d.inspired),
            h("span", { className: "dl-area" }, d.area.toFixed(1) + " km²"))))))),
      h("h3", null, "Civic life across Gidi"),
      h("div", { className: "civic-totals" }, CIVIC_ORDER.map((t) => { const n = G.pois.filter((p) => p.type === t).length; return n ? h("div", { key: t, className: "ct t-" + t },
        h("span", { className: "pin small" }, TYPE[t].glyph), h("span", null, TYPE[t].label), h("b", null, n)) : null; })),
      h("p", { className: "foot" }, "Churches, mosques, schools, hospitals and clinics are safe ground: part of daily life, never crime locations. Names are invented. Hatched areas: okada banned. Dashed outline: taskforce sweeps."));
  }

  function StudyBlock({ s, d }) {
    const byName = Object.fromEntries(G.districts.map((x) => [x.id, x.name]));
    const kinds = { main: "main road", arterial: "arterial", rail: "rail line", street: "street" };
    const links = {};
    s.links.forEach((g) => { (links[g.to] = links[g.to] || []).push(g.road ? g.road + " (" + kinds[g.kind] + ")" : "a " + kinds[g.kind] + " carries on"); });
    return h("div", { className: "study" },
      h("h3", null, "Town plan check"),
      h("p", { className: "ps" }, "Streets and houses here are generated from the measured pattern of " + d.inspired + ", not traced from a real map."),
      h("table", { className: "stbl" },
        h("thead", null, h("tr", null, h("th", null, ""), h("th", null, "Real, typical"), h("th", null, "Real, dense"), h("th", null, "Gidi"))),
        h("tbody", null, s.rows.map((r, i) => h("tr", { key: i }, r.map((c, j) => j ? h("td", { key: j }, c) : h("th", { key: j, scope: "row" }, c)))))),
      h("h3", null, "Roads to neighbours"),
      h("ul", { className: "links" }, Object.entries(links).map(([k, v]) => h("li", { key: k }, h("b", null, byName[k] || k), ": " + v.join(", ")))));
  }

  function District({ d, select }) {
    const places = G.pois.map((p, i) => [p, i]).filter(([p]) => p.d === d.id && !p.civic);
    const civic = G.pois.map((p, i) => [p, i]).filter(([p]) => p.d === d.id && p.civic);
    return h("div", { className: "card" },
      h("div", { className: "eyebrow" }, "District · inspired by " + d.inspired),
      h("h2", null, d.name),
      h("div", { className: "chiprow" },
        h("span", { className: "tag a" + d.act }, ACT_NAME[d.act]),
        h("span", { className: "tag ok-" + d.okada }, OKADA[d.okada].label),
        h("span", { className: "tag plain" }, d.area.toFixed(1) + " km²")),
      h("p", { className: "lead" }, d.blurb),
      h("dl", { className: "kv" }, h("dt", null, "Oja here"), h("dd", null, d.oja), h("dt", null, "Okada"), h("dd", null, OKADA[d.okada].note)),
      G.study && G.study[d.id] && h(StudyBlock, { s: G.study[d.id], d }),
      h("h3", null, "What to model"),
      h("ul", { className: "model" }, d.model.map((m, i) => h("li", { key: i }, m))),
      h("h3", null, "Between missions"),
      h("ul", { className: "acts" }, d.activities.map((m, i) => h("li", { key: i }, m))),
      h("h3", null, "Civic life (" + civic.length + ")"),
      h(CivicBlock, { items: civic, select }),
      h("h3", null, "Landmarks (" + places.length + ")"),
      h("ul", { className: "plist" }, places.map(([p, i]) => h("li", { key: i },
        h("button", { onClick: () => select({ kind: "poi", id: i }) },
          h("span", { className: "pin small t-" + p.type }, TYPE[p.type].glyph),
          h("span", null, h("span", { className: "pn" }, p.name), h("span", { className: "ps" }, p.note)))))));
  }

  ReactDOM.createRoot(document.getElementById("root")).render(h(App));
})();
