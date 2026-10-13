/* Gidi 3D: Apple Maps–style district model. window.DISTRICT from gen3d.py (x east, y = south, metres). */
(function () {
  const D = window.DISTRICT;
  const el = document.getElementById("scene");
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputEncoding = THREE.sRGBEncoding;
  
  el.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 2, 9000);
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; controls.dampingFactor = 0.08;
  controls.maxPolarAngle = Math.PI * 0.44; controls.minDistance = 35; controls.maxDistance = 2600;
  controls.screenSpacePanning = false;

  /* ---------- palette (light = day, dark = dusk) ---------- */
  const PAL = {
    light: { bg: "#dcd8cf", ground: "#d6d1c6", inside: "#ddd8cd", lane: "#7f7d78", laneEdge: "#c4beb2", main: "#7a7f86", mark: "#ffffff", art: "#6b7077",
      water: "#8cc4e8", canal: "#6aa39b", bank: "#cfcbc2", tint: "#ffffff", hemiSky: "#f4f6ff", hemiGround: "#a89d88", hemi: 0.5, sun: 0.62, fog: "#dcd8cf", tree: "#8dbb76", trunk: "#8a6d55", rail: "#b9b1a5", outline: "#1a73e8" },
    dark: { bg: "#1d2228", ground: "#272c33", inside: "#2d333b", lane: "#4a5059", laneEdge: "#333942", main: "#5a616b", mark: "#c9ccd1", art: "#5f6670",
      water: "#1d3a57", canal: "#21443f", bank: "#3a3f47", tint: "#8a909a", hemiSky: "#9fb3d1", hemiGround: "#2a2f37", hemi: 0.55, sun: 0.55, fog: "#1d2228", tree: "#4f7444", trunk: "#4a3b2e", rail: "#4a4640", outline: "#8ab4f8" },
  };
  const isDark = () => document.documentElement.dataset.theme === "dark" ||
    (document.documentElement.dataset.theme !== "light" && window.matchMedia("(prefers-color-scheme: dark)").matches);
  let pal = isDark() ? PAL.dark : PAL.light;
  const C = (hex) => new THREE.Color(hex);

  /* ---------- lights ---------- */
  const hemi = new THREE.HemisphereLight(pal.hemiSky, pal.hemiGround, pal.hemi); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xffffff, pal.sun);
  sun.position.set(-420, 620, -260); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  const sc = sun.shadow.camera; sc.left = -650; sc.right = 650; sc.top = 650; sc.bottom = -650; sc.near = 50; sc.far = 2200;
  sun.shadow.bias = -0.0006; sun.shadow.normalBias = 0.6;
  scene.add(sun); scene.add(sun.target);

  /* ---------- helpers ---------- */
  const mats = {};
  const mat = (key, hex, opts = {}) => (mats[key] = new THREE.MeshLambertMaterial({ color: C(hex), ...opts }));
  function ribbon(pts, w, y) {
    // flat strip along a polyline, plus round joints (discs)
    const pos = [];
    for (let i = 0; i < pts.length - 1; i++) {
      const [x0, z0] = pts[i], [x1, z1] = pts[i + 1];
      const dx = x1 - x0, dz = z1 - z0, L = Math.hypot(dx, dz) || 1, nx = -dz / L * w / 2, nz = dx / L * w / 2;
      pos.push(x0 + nx, y, z0 + nz, x1 + nx, y, z1 + nz, x1 - nx, y, z1 - nz, x0 + nx, y, z0 + nz, x1 - nx, y, z1 - nz, x0 - nx, y, z0 - nz);
    }
    for (const [x, z] of pts) for (let k = 0; k < 10; k++) {
      const a0 = k / 10 * Math.PI * 2, a1 = (k + 1) / 10 * Math.PI * 2, r = w / 2;
      pos.push(x, y, z, x + Math.cos(a1) * r, y, z + Math.sin(a1) * r, x + Math.cos(a0) * r, y, z + Math.sin(a0) * r);
    }
    return pos;
  }
  function mesh(pos, material, { shadow = false, cast = false } = {}) {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
    g.computeVertexNormals();
    const m = new THREE.Mesh(g, material); m.receiveShadow = shadow; m.castShadow = cast; scene.add(m); return m;
  }
  function dashes(pts, y, dash, gap, w) {
    const pos = [];
    for (let i = 0; i < pts.length - 1; i++) {
      const [x0, z0] = pts[i], [x1, z1] = pts[i + 1]; const L = Math.hypot(x1 - x0, z1 - z0);
      for (let t = 0; t < L; t += dash + gap) {
        const a = t / L, b = Math.min(1, (t + dash) / L);
        pos.push(...ribbon([[x0 + (x1 - x0) * a, z0 + (z1 - z0) * a], [x0 + (x1 - x0) * b, z0 + (z1 - z0) * b]], w, y).slice(0, 18));
      }
    }
    return pos;
  }

  /* ---------- ground ---------- */
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(9000, 9000), mat("ground", pal.ground));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const outlineShape = new THREE.Shape(D.outline.map(([x, z]) => new THREE.Vector2(x, -z)));
  const inside = new THREE.Mesh(new THREE.ShapeGeometry(outlineShape), mat("inside", pal.inside));
  inside.rotation.x = -Math.PI / 2; inside.position.y = 0.02; inside.receiveShadow = true; scene.add(inside);
  // lagoon water if near
  const waterShape = new THREE.Shape(D.water.map(([x, z]) => new THREE.Vector2(x, -z)));
  const waterMesh = new THREE.Mesh(new THREE.ShapeGeometry(waterShape), mat("water", pal.water));
  waterMesh.rotation.x = -Math.PI / 2; waterMesh.position.y = 0.05; scene.add(waterMesh);
  // district edge line
  const edge = new THREE.Line(new THREE.BufferGeometry().setFromPoints(D.outline.map(([x, z]) => new THREE.Vector3(x, 0.4, z))),
    new THREE.LineDashedMaterial({ color: C(pal.outline), dashSize: 8, gapSize: 6, transparent: true, opacity: 0.8 }));
  edge.computeLineDistances(); scene.add(edge);

  /* ---------- roads ---------- */
  const inLanes = D.streets.filter((s) => s.inside), outLanes = D.streets.filter((s) => !s.inside);
  mesh(outLanes.flatMap((s) => ribbon(s.pts, s.w, 0.06)), mat("laneOut", pal.laneEdge), { shadow: true });
  mesh(inLanes.flatMap((s) => ribbon(s.pts, s.w + 2.6, 0.07)), mat("laneEdge", pal.laneEdge), { shadow: true });
  mesh(inLanes.flatMap((s) => ribbon(s.pts, s.w, 0.09)), mat("lane", pal.lane), { shadow: true });
  mesh(D.mains.flatMap((s) => ribbon(s.pts, s.w + 3, 0.1)), mat("mainEdge", pal.laneEdge), { shadow: true });
  mesh(D.mains.flatMap((s) => ribbon(s.pts, s.w, 0.12)), mat("main", pal.main), { shadow: true });
  mesh(D.mains.flatMap((s) => dashes(s.pts, 0.14, 4, 5, 0.35)), mat("mark", pal.mark));
  // canal (sunk, with banks)
  if (D.canal.pts.length) {
    mesh(ribbon(D.canal.pts, D.canal.w + 3, 0.11), mat("bank", pal.bank), { shadow: true });
    mesh(ribbon(D.canal.pts, D.canal.w, 0.13), mat("canal", pal.canal), { shadow: true });
    // footbridges where lanes cross the canal: draw lanes again on top
    mesh(inLanes.flatMap((s) => ribbon(s.pts, s.w, 0.16)).filter(() => true), mats.lane, { shadow: true }).visible = true;
  }
  // rail
  if (D.rail.length) {
    mesh(ribbon(D.rail, 7, 0.15), mat("rail", pal.rail), { shadow: true });
    const rails = [];
    for (const off of [-0.75, 0.75]) {
      const p = D.rail.map(([x, z], i, a) => { const [x2, z2] = a[Math.min(i + 1, a.length - 1)], [x1, z1] = a[Math.max(i - 1, 0)];
        const dx = x2 - x1, dz = z2 - z1, L = Math.hypot(dx, dz) || 1; return [x - dz / L * off, z + dx / L * off]; });
      rails.push(...ribbon(p, 0.25, 0.3));
    }
    mesh(rails, mat("steel", "#5b5f66"));
  }
  // arterials: ground-level or flyover
  for (const a of D.arts) {
    const y = a.elev || 0.12;
    const deck = mesh(ribbon(a.pts, a.w, y + 0.6), mat("art" + a.name, pal.art), { shadow: true, cast: !!a.elev });
    mesh(dashes(a.pts, y + 0.65, 6, 6, 0.4), mats.mark);
    if (a.elev) {
      // deck sides and pillars
      const side = [];
      for (let i = 0; i < a.pts.length - 1; i++) {
        const [x0, z0] = a.pts[i], [x1, z1] = a.pts[i + 1], dx = x1 - x0, dz = z1 - z0, L = Math.hypot(dx, dz), nx = -dz / L * a.w / 2, nz = dx / L * a.w / 2;
        for (const s of [1, -1]) side.push(x0 + nx * s, y - 1, z0 + nz * s, x1 + nx * s, y - 1, z1 + nz * s, x1 + nx * s, y + 1.5, z1 + nz * s,
          x0 + nx * s, y - 1, z0 + nz * s, x1 + nx * s, y + 1.5, z1 + nz * s, x0 + nx * s, y + 1.5, z0 + nz * s);
        for (let t = 15; t < L; t += 32) {
          const px = x0 + dx / L * t, pz = z0 + dz / L * t;
          const p = new THREE.Mesh(new THREE.BoxGeometry(2.2, y, 6), mat("pillar", "#c9c6bf"));
          p.position.set(px, y / 2, pz); p.rotation.y = -Math.atan2(dz, dx); p.castShadow = p.receiveShadow = true; scene.add(p);
        }
      }
      const sm = mesh(side, mat("deckSide", "#d6d2ca", { side: THREE.DoubleSide }), { cast: true });
      // under-bridge road
      mesh(ribbon(a.pts, a.w - 4, 0.11), mat("under", pal.lane), { shadow: true });
    }
  }

  /* ---------- buildings (one merged mesh, vertex colours) ---------- */
  const bp = [], bc = [], col = new THREE.Color();
  function quad(a, b, c, d, color) { bp.push(...a, ...b, ...c, ...a, ...c, ...d); for (let i = 0; i < 6; i++) bc.push(color.r, color.g, color.b); }
  function tri(a, b, c, color) { bp.push(...a, ...b, ...c); for (let i = 0; i < 3; i++) bc.push(color.r, color.g, color.b); }
  const tanks = [];
  for (const L of D.lots) {
    const ca = Math.cos(L.a), sa = Math.sin(L.a), hw = L.w / 2, hd = L.d / 2, H = L.h;
    const P = (u, v, y) => [L.x + u * ca - v * sa, y, L.y + u * sa + v * ca];
    const c = [P(-hw, -hd, 0), P(hw, -hd, 0), P(hw, hd, 0), P(-hw, hd, 0)];
    const t = c.map((p) => [p[0], H, p[2]]);
    col.set(L.c);
    const shade = (f) => col.clone().multiplyScalar(f);
    // walls (outward winding)
    quad(c[0], t[0], t[1], c[1], shade(0.92)); quad(c[1], t[1], t[2], c[2], shade(1.0));
    quad(c[2], t[2], t[3], c[3], shade(0.88)); quad(c[3], t[3], t[0], c[0], shade(0.97));
    // ground-floor shopfront band on street-facing buildings
    if (!L.compound && L.roof !== "open") {
      const sh = col.clone().lerp(new THREE.Color("#5c5a57"), 0.45), b = 2.6, e = 0.06;
      const f0 = P(-hw * 0.85, -hd - e, 0.2), f1 = P(hw * 0.85, -hd - e, 0.2), f2 = P(hw * 0.85, -hd - e, b), f3 = P(-hw * 0.85, -hd - e, b);
      quad(f0, f3, f2, f1, sh);
    }
    if (L.roof === "tin") {
      // gable roof along the long side with small overhang
      const o = 0.45, rh = Math.min(2.2, Math.min(L.w, L.d) * 0.22), along = L.w >= L.d;
      const rc = new THREE.Color(L.rc);
      if (along) {
        const a0 = P(-hw - o, -hd - o, H), a1 = P(hw + o, -hd - o, H), a2 = P(hw + o, hd + o, H), a3 = P(-hw - o, hd + o, H);
        const r0 = P(-hw - o, 0, H + rh), r1 = P(hw + o, 0, H + rh);
        quad(a0, r0, r1, a1, rc.clone().multiplyScalar(0.9)); quad(a2, r1, r0, a3, rc);
        tri(P(-hw, -hd, H), P(-hw, hd, H), P(-hw, 0, H + rh), shade(0.9)); tri(P(hw, hd, H), P(hw, -hd, H), P(hw, 0, H + rh), shade(0.95));
      } else {
        const a0 = P(-hw - o, -hd - o, H), a1 = P(hw + o, -hd - o, H), a2 = P(hw + o, hd + o, H), a3 = P(-hw - o, hd + o, H);
        const r0 = P(0, -hd - o, H + rh), r1 = P(0, hd + o, H + rh);
        quad(a3, r1, r0, a0, rc.clone().multiplyScalar(0.92)); quad(a1, r0, r1, a2, rc);
        tri(P(hw, -hd, H), P(-hw, -hd, H), P(0, -hd, H + rh), shade(0.9)); tri(P(-hw, hd, H), P(hw, hd, H), P(0, hd, H + rh), shade(0.95));
      }
    } else {
      const rc = new THREE.Color(L.roof === "open" ? "#bdbab4" : L.rc);
      quad(t[0], t[3], t[2], t[1], rc);
      if (L.roof === "flat") { // parapet lip
        const p = 0.5, i = 0.35, pc = col.clone().multiplyScalar(0.96);
        const q = (u0, v0, u1, v1) => quad(P(u0, v0, H), P(u0, v0, H + p), P(u1, v1, H + p), P(u1, v1, H), pc);
        q(-hw + i, -hd + i, hw - i, -hd + i); q(hw - i, -hd + i, hw - i, hd - i); q(hw - i, hd - i, -hw + i, hd - i); q(-hw + i, hd - i, -hw + i, -hd + i);
      } else { // unfinished: rebar columns sticking out
        for (const [u, v] of [[-hw + .4, -hd + .4], [hw - .4, -hd + .4], [hw - .4, hd - .4], [-hw + .4, hd - .4]]) {
          const g = 0.25, cc = new THREE.Color("#8e8a84");
          quad(P(u - g, v, H), P(u - g, v, H + 1.6), P(u + g, v, H + 1.6), P(u + g, v, H), cc);
          quad(P(u, v - g, H), P(u, v - g, H + 1.6), P(u, v + g, H + 1.6), P(u, v + g, H), cc);
        }
      }
      if (L.tank) tanks.push(P(hw * 0.4, hd * 0.3, H));
    }
  }
  const bg = new THREE.BufferGeometry();
  bg.setAttribute("position", new THREE.Float32BufferAttribute(bp, 3));
  bg.setAttribute("color", new THREE.Float32BufferAttribute(bc, 3));
  bg.computeVertexNormals();
  const buildings = new THREE.Mesh(bg, new THREE.MeshLambertMaterial({ vertexColors: true, color: C(pal.tint) }));
  buildings.castShadow = buildings.receiveShadow = true; scene.add(buildings);

  // water tanks (instanced)
  const tankG = new THREE.CylinderGeometry(0.9, 0.9, 1.7, 12); tankG.translate(0, 0.85, 0);
  const tankM = new THREE.InstancedMesh(tankG, mat("tank", "#2a3e5c"), tanks.length);
  const m4 = new THREE.Matrix4();
  tanks.forEach((p, i) => { m4.makeTranslation(p[0], p[1], p[2]); tankM.setMatrixAt(i, m4); });
  tankM.castShadow = true; scene.add(tankM);

  // trees (instanced canopy + trunk)
  const canopyG = new THREE.IcosahedronGeometry(1, 1), trunkG = new THREE.CylinderGeometry(0.25, 0.35, 1, 6); trunkG.translate(0, 0.5, 0);
  const canopy = new THREE.InstancedMesh(canopyG, mat("tree", pal.tree, { flatShading: true }), D.trees.length);
  const trunk = new THREE.InstancedMesh(trunkG, mat("trunk", pal.trunk), D.trees.length);
  D.trees.forEach(([x, z, r], i) => {
    m4.compose(new THREE.Vector3(x, r * 1.25 + 1.4, z), new THREE.Quaternion(), new THREE.Vector3(r, r * 0.9, r)); canopy.setMatrixAt(i, m4);
    m4.compose(new THREE.Vector3(x, 0, z), new THREE.Quaternion(), new THREE.Vector3(1, r * 0.6 + 1.2, 1)); trunk.setMatrixAt(i, m4);
  });
  canopy.castShadow = trunk.castShadow = true; scene.add(canopy, trunk);

  /* ---------- landmarks ---------- */
  const LM = D.landmarks;
  // parts market: stall roofs (coloured tarps) on posts, tyre stacks
  const stallG = new THREE.BoxGeometry(1, 1, 1); stallG.translate(0, 0.5, 0);
  const tarpCols = LM.stalls.map((s) => s.c);
  const stallM = new THREE.InstancedMesh(stallG, new THREE.MeshLambertMaterial({ color: 0xffffff }), LM.stalls.length * 2);
  LM.stalls.forEach((s, i) => {
    m4.compose(new THREE.Vector3(s.x, 0, s.y), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, s.a || 0, 0)), new THREE.Vector3(s.w, 2.2, s.d)); stallM.setMatrixAt(i * 2, m4);
    stallM.setColorAt(i * 2, C("#8f8a82"));
    m4.compose(new THREE.Vector3(s.x, 2.6, s.y), new THREE.Quaternion().setFromEuler(new THREE.Euler(0.12, s.a || 0, 0)), new THREE.Vector3(s.w + 1.2, 0.25, s.d + 1.4)); stallM.setMatrixAt(i * 2 + 1, m4);
    stallM.setColorAt(i * 2 + 1, C(s.c));
  });
  stallM.castShadow = stallM.receiveShadow = true; scene.add(stallM);
  const tyreG = new THREE.TorusGeometry(0.42, 0.18, 6, 12); tyreG.rotateX(Math.PI / 2);
  const tyres = new THREE.InstancedMesh(tyreG, mat("tyre", "#2b2b2d"), LM.stalls.length * 4);
  let ti = 0; LM.stalls.forEach((s) => { for (let k = 0; k < 4; k++) { m4.makeTranslation(s.x + s.w / 2 + 0.9, 0.2 + k * 0.36, s.y - s.d / 2 + 0.8); tyres.setMatrixAt(ti++, m4); } });
  scene.add(tyres);
  // grain warehouse
  { const w = LM.warehouse; const g = new THREE.Group(); g.position.set(w.x, 0, w.y); g.rotation.y = -w.a;
    const body = new THREE.Mesh(new THREE.BoxGeometry(w.w, w.h, w.d), mat("wh", "#d8cfbf")); body.position.y = w.h / 2;
    const roof = new THREE.Mesh(new THREE.CylinderGeometry(w.d / 2, w.d / 2, w.w, 3, 1, false), mat("whroof", "#9aa0a6"));
    roof.rotation.z = Math.PI / 2; roof.rotation.x = Math.PI; roof.position.y = w.h + w.d / 4 - 1; roof.scale.set(1, 1, 0.55);
    body.castShadow = body.receiveShadow = roof.castShadow = true; g.add(body, roof);
    for (let k = 0; k < 14; k++) { const sack = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.1, 1.6), mat("sack", "#e9dfc6")); sack.position.set(-w.w / 2 + 3 + (k % 7) * 3, 0.55 + Math.floor(k / 7) * 1.1, w.d / 2 + 3); sack.castShadow = true; g.add(sack); }
    scene.add(g); }
  // food stall where Tunde steals: kiosk + umbrella
  { const f = LM.foodstall; const g = new THREE.Group(); g.position.set(f.x, 0, f.y);
    const k = new THREE.Mesh(new THREE.BoxGeometry(4, 1.1, 2), mat("kiosk", "#c7472f")); k.position.y = 0.55;
    const u = new THREE.Mesh(new THREE.ConeGeometry(3.4, 1.3, 8), mat("umb", "#f3c623")); u.position.y = 3.4;
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 3), mat("pole", "#555")); pole.position.y = 1.5;
    [k, u, pole].forEach((m) => { m.castShadow = true; g.add(m); }); scene.add(g); }
  // transformer 44: pole + box + wires
  { const t = LM.transformer; const g = new THREE.Group(); g.position.set(t.x, 0, t.y);
    for (const dx of [-1.2, 1.2]) { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 9), mats.pole || mat("pole", "#555")); p.position.set(dx, 4.5, 0); p.castShadow = true; g.add(p); }
    const box = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.8, 1.4), mat("tx", "#7d8790")); box.position.y = 5.5; box.castShadow = true; g.add(box);
    scene.add(g); }

  /* ---------- labels (HTML overlay) ---------- */
  const labels = document.getElementById("labels");
  const GLYPH = { story: "★", market: "M", transit: "T", danger: "!", check: "✕", night: "☾", landmark: "◆", industry: "▲", water: "≈", gov: "▣", park: "≡",
    church: "✝", mosque: "☪", school: "✎", hospital: "H", clinic: "+", chemist: "℞", police: "P", fire: "F", council: "▣", fuel: "⬢", bank: "₦", sport: "◎", betting: "◇", cemetery: "†" };
  const tags = [];
  const addTag = (x, y, z, html, cls, onClick) => {
    const d = document.createElement(onClick ? "button" : "div"); d.className = "tag3 " + cls; d.innerHTML = html;
    if (onClick) d.addEventListener("click", onClick);
    labels.appendChild(d); tags.push({ v: new THREE.Vector3(x, y, z), d }); return d;
  };
  D.pois.forEach((p, i) => addTag(p.x, 4, p.y, `<span class="pin t-${p.type}">${GLYPH[p.type] || "•"}</span><span class="pl t-${p.type}">${p.name}</span>`, "poi3" + (p.civic ? " civic3" : ""), () => focusPoi(i)));
  D.mains.filter((m) => m.inside).forEach((m) => { const mid = m.pts[Math.floor(m.pts.length / 2)]; addTag(mid[0], 1, mid[1], m.name, "street3"); });
  D.arts.forEach((a) => { const mid = a.pts[Math.floor(a.pts.length / 2)]; addTag(mid[0], (a.elev || 0) + 2, mid[1], a.name, "road3"); });

  /* ---------- camera moves ---------- */
  let flight = null;
  function flyTo(target, dist, polar, azim) {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const sph = new THREE.Spherical(dist, polar, azim);
    const endPos = new THREE.Vector3().setFromSpherical(sph).add(target);
    const sPos = camera.position.clone(), sTar = controls.target.clone();
    if (reduce) { camera.position.copy(endPos); controls.target.copy(target); return; }
    flight = { t0: performance.now(), D: 900, sPos, sTar, endPos, target };
  }
  const HOME = () => flyTo(new THREE.Vector3(0, 0, 0), 1150, 0.95, Math.PI * 0.18);
  function focusPoi(i) {
    const p = D.pois[i]; flyTo(new THREE.Vector3(p.x, 0, p.y), 170, 0.95, controls.getAzimuthalAngle());
    window.dispatchEvent(new CustomEvent("poi", { detail: i }));
  }
  window.GIDI3D = { focusPoi, home: HOME,
    topDown: (on) => flyTo(controls.target.clone(), on ? Math.max(500, camera.position.distanceTo(controls.target)) : 600, on ? 0.001 : 0.95, controls.getAzimuthalAngle()),
    north: () => flyTo(controls.target.clone(), camera.position.distanceTo(controls.target), controls.getPolarAngle(), 0),
    zoom: (f) => flyTo(controls.target.clone(), Math.min(2600, Math.max(35, camera.position.distanceTo(controls.target) * f)), controls.getPolarAngle(), controls.getAzimuthalAngle()),
  };
  camera.position.set(500, 900, 700); controls.target.set(0, 0, 0); controls.update();
  HOME();

  /* ---------- theme ---------- */
  function applyTheme() {
    pal = isDark() ? PAL.dark : PAL.light;
    scene.background = C(pal.bg); scene.fog = new THREE.Fog(pal.fog, 1400, 4200);
    hemi.color.set(pal.hemiSky); hemi.groundColor.set(pal.hemiGround); hemi.intensity = pal.hemi; sun.intensity = pal.sun;
    const set = (k, v) => mats[k] && mats[k].color.set(v);
    set("ground", pal.ground); set("inside", pal.inside); set("lane", pal.lane); set("laneEdge", pal.laneEdge); set("laneOut", pal.laneEdge);
    set("main", pal.main); set("mainEdge", pal.laneEdge); set("mark", pal.mark); set("water", pal.water); set("canal", pal.canal); set("bank", pal.bank);
    set("tree", pal.tree); set("trunk", pal.trunk); set("rail", pal.rail); set("under", pal.lane);
    D.arts.forEach((a) => set("art" + a.name, pal.art));
    buildings.material.color.set(pal.tint); edge.material.color.set(pal.outline);
  }
  applyTheme();
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", applyTheme);
  new MutationObserver(applyTheme).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

  /* ---------- loop ---------- */
  const compass = document.getElementById("compass-needle");
  const v = new THREE.Vector3();
  function resize() { const w = el.clientWidth, h = el.clientHeight; renderer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix(); }
  new ResizeObserver(resize).observe(el); resize();
  function frame(t) {
    if (flight) {
      const k = Math.min(1, (t - flight.t0) / flight.D), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      camera.position.lerpVectors(flight.sPos, flight.endPos, e); controls.target.lerpVectors(flight.sTar, flight.target, e);
      if (k >= 1) flight = null;
    }
    controls.update();
    sun.target.position.copy(controls.target); sun.position.copy(controls.target).add(new THREE.Vector3(-420, 620, -260));
    renderer.render(scene, camera);
    const w = el.clientWidth, h = el.clientHeight, dist = camera.position.distanceTo(controls.target);
    for (const tg of tags) {
      v.copy(tg.v).applyMatrix4(camera.matrixWorldInverse);
      const front = v.z < -1;
      v.copy(tg.v).project(camera);
      const vis = front && Math.abs(v.x) < 1.1 && Math.abs(v.y) < 1.1;
      const isStreet = tg.d.classList.contains("street3");
      const isCivic = tg.d.classList.contains("civic3");
      tg.d.hidden = !vis || (isStreet && dist > 700) || (isCivic && dist > 520);
      if (vis) tg.d.style.transform = `translate(${(v.x + 1) / 2 * w}px, ${(1 - v.y) / 2 * h}px)`;
      if (tg.d.classList.contains("poi3")) tg.d.classList.toggle("far", tg.d.classList.contains("civic3") ? dist > 260 : dist > 900);
    }
    if (compass) compass.style.transform = `rotate(${-controls.getAzimuthalAngle()}rad)`;
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

})();
