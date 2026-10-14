/* Gidi Maps, 3D view: the same city data (window.GIDI) as extruded buildings, raised flyovers and flat ground,
   drawn with three.js r147 (UMD) and MapControls. Map metres: x east, y south. Three.js: X = x, Z = y, Y = up.
   Exposes window.GidiView3D (a React component) for app.js. */
(function () {
  const { useEffect, useRef, useState } = React;
  const h = React.createElement;
  const G = window.GIDI;
  const STOREY = 3.1;

  function tokens() {
    const cs = getComputedStyle(document.documentElement);
    const v = (n, f) => (cs.getPropertyValue(n).trim() || f);
    const dark = matchMedia("(prefers-color-scheme: dark)").matches && document.documentElement.getAttribute("data-theme") !== "light" || document.documentElement.getAttribute("data-theme") === "dark";
    return {
      dark, bush: v("--bush", "#e7eadb"), land: v("--land", "#f5f3ee"), water: v("--water", "#a9d3f5"), ocean: v("--ocean", "#9fcbef"),
      st: v("--st", "#ffffff"), mn: v("--mn", "#ffffff"), ar: v("--ar", "#f5c542"), bridge: v("--bridge", "#e6e1d6"),
      market: v("--p-market", "#f6dfc2"), industrial: v("--p-industrial", "#e3e3e6"), school: v("--p-school", "#f3ebc4"), pitch: v("--p-pitch", "#cfe8c4"), park: v("--p-park", "#d9dde8"),
      sky: dark ? "#1c232c" : "#dfe8ef", a1: v("--a1", "#1e8e3e"), a2: v("--a2", "#c98400"), a3: v("--a3", "#d93025"),
    };
  }
  const C = (s) => new THREE.Color(s);

  // ---------- geometry helpers ----------
  function flatPoly(rings, y) {   // rings: [outer, ...holes] in map metres
    const sh = new THREE.Shape(rings[0].map((p) => new THREE.Vector2(p[0], p[1])));
    for (const hole of rings.slice(1)) sh.holes.push(new THREE.Path(hole.map((p) => new THREE.Vector2(p[0], p[1]))));
    const g = new THREE.ShapeGeometry(sh); g.rotateX(Math.PI / 2); g.translate(0, y, 0); return g;
  }
  function ribbon(lines, width, y, out) {   // flat strips along polylines; appends triangles to out (array of numbers)
    const hw = width / 2;
    for (const pts of lines) for (let i = 0; i < pts.length - 1; i++) {
      const [x0, z0] = pts[i], [x1, z1] = pts[i + 1]; const L = Math.hypot(x1 - x0, z1 - z0); if (L < 0.01) continue;
      const nx = -(z1 - z0) / L * hw, nz = (x1 - x0) / L * hw;
      // extend a little past each joint so corners don't gap
      const ex = (x1 - x0) / L * hw * 0.9, ez = (z1 - z0) / L * hw * 0.9;
      const a = [x0 - ex + nx, z0 - ez + nz], b = [x0 - ex - nx, z0 - ez - nz], c = [x1 + ex - nx, z1 + ez - nz], d = [x1 + ex + nx, z1 + ez + nz];
      out.push(a[0], y, a[1], b[0], y, b[1], c[0], y, c[1], a[0], y, a[1], c[0], y, c[1], d[0], y, d[1]);
    }
    return out;
  }
  function geomFrom(pos, col) {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
    if (col) g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals(); return g;
  }
  function hash(i) { let x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }

  // walls and roofs for every generated building, one merged mesh
  function buildings(T) {
    const pos = [], col = [];
    const walls = T.dark ? ["#6d6a66", "#75706a", "#6a6f72", "#7a7369"] : ["#e9e2d6", "#e3d9c8", "#dcdcd6", "#e6dccd", "#d9d2c4"];
    const tin = T.dark ? ["#6e4a3a", "#5f4d42", "#6b6560"] : ["#a3684a", "#8f5f47", "#9a8f84", "#b07a58"];
    const flat = T.dark ? "#77746f" : "#cfcac0";
    const special = { works: T.dark ? "#7a3f2e" : "#b05a3c", mound: T.dark ? "#4a4236" : "#9c8a6a", bakery: T.dark ? "#8a6a3a" : "#d9a85b", crane: T.dark ? "#8a5b2e" : "#d9822b", stack: T.dark ? "#3b6a8a" : "#4f8fc0", tank: T.dark ? "#8a8f96" : "#e6e8eb", villa: T.dark ? "#6b6250" : "#d8cfb8", cellblock: T.dark ? "#55595e" : "#9aa0a6", tower: T.dark ? "#55595e" : "#80868b", trailer: T.dark ? "#5b5650" : "#b0b4ba", plaza: T.dark ? "#5d6670" : "#c9c1b0", unfinished: T.dark ? "#4a4a4a" : "#b5b5b5", pen: T.dark ? "#5b5650" : "#a59d92", scrap: T.dark ? "#5a4636" : "#8a6a4f", container: T.dark ? "#2f5a8a" : "#3b78b8", "phone mall": T.dark ? "#4f6a86" : "#86a6c8", strip: T.dark ? "#8a3b33" : "#c8645a", hall: T.dark ? "#5e4a86" : "#9b7fc7", office: T.dark ? "#5d6670" : "#c3cad3", barracks: T.dark ? "#55603f" : "#a3ad84", bust: T.dark ? "#888" : "#555", canopy: T.dark ? "#7a4a8c" : "#a86cc1", warehouse: T.dark ? "#5d6670" : "#b9c0c8", stalls: T.dark ? "#8a5b2e" : "#d69a55", school: T.dark ? "#7b6a3c" : "#e1c46a", kiosk: T.dark ? "#4f6a86" : "#7ea2c6", shed: T.dark ? "#5b5650" : "#a59d92", gatehouse: T.dark ? "#8a3b33" : "#c8645a", generator: T.dark ? "#3f4348" : "#5f646a", "water tank": T.dark ? "#2f5a8a" : "#3b78b8", mansion: T.dark ? "#7a6a55" : "#efe6d2", clubhouse: T.dark ? "#5e4a86" : "#9b7fc7" };
    let n = 0, count = 0;
    const tmp = new THREE.Color();
    for (const [id, list] of Object.entries(G.buildings || {})) {
      const st = (G.storeys || {})[id] || [];
      list.forEach((b, i) => {
        n++;
        const kind = b[0], ring = b.slice(1); const s = st[i] || 1;
        if (kind !== "generator" && kind !== "water tank") count++;   // generator houses and tanks are not counted as buildings
        const H = kind === "stalls" ? 3 : kind === "canopy" ? 2.8 : kind === "mound" ? 5 : kind === "crane" ? 32 : kind === "tank" ? 14 : kind === "stack" ? 7.8 : kind === "trailer" ? 4 : kind === "pen" ? 2.4 : kind === "scrap" ? 2.5 : kind === "container" ? 2.6 : kind === "bust" ? 4 : kind === "kiosk" ? 2.6 : kind === "shed" ? 2.6 : kind === "raft" ? 0.6 : kind === "sawdust" ? 2 : kind === "generator" ? 1.8 : kind === "water tank" ? 5.5 : kind === "stilt" || kind === "stilt bar" ? s * STOREY + 1.8 : s * STOREY + (s <= 2 ? 0.6 : 0.3);
        const wallC = special[kind] || walls[Math.floor(hash(n) * walls.length)];
        const roofC = special[kind] || (s <= 2 && hash(n + 7) < 0.62 ? tin[Math.floor(hash(n + 3) * tin.length)] : flat);
        const k = ring.length;
        for (let j = 0; j < k; j++) {   // walls, darker at the foot for a little depth
          const [x0, z0] = ring[j], [x1, z1] = ring[(j + 1) % k];
          pos.push(x0, 0, z0, x1, 0, z1, x1, H, z1, x0, 0, z0, x1, H, z1, x0, H, z0);
          tmp.set(wallC); const top = [tmp.r, tmp.g, tmp.b]; tmp.multiplyScalar(0.72); const bot = [tmp.r, tmp.g, tmp.b];
          col.push(...bot, ...bot, ...top, ...bot, ...top, ...top);
        }
        tmp.set(roofC);
        for (let j = 1; j < k - 1; j++) {   // roof fan
          pos.push(ring[0][0], H, ring[0][1], ring[j + 1][0], H, ring[j + 1][1], ring[j][0], H, ring[j][1]);
          col.push(tmp.r, tmp.g, tmp.b, tmp.r, tmp.g, tmp.b, tmp.r, tmp.g, tmp.b);
        }
      });
    }
    const m = new THREE.Mesh(geomFrom(pos, col), new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }));
    m.userData.count = count; return m;
  }

  // flyovers (decks on pillars), skywalks and canal footbridges
  function structures(T) {
    const group = new THREE.Group();
    const deckM = new THREE.MeshLambertMaterial({ color: C(T.dark ? "#6b6f75" : "#e4dfd5"), side: THREE.DoubleSide });
    const sideM = new THREE.MeshLambertMaterial({ color: C(T.dark ? "#4b4f55" : "#b9b3a8"), side: THREE.DoubleSide });
    for (const s of G.structures || []) {
      const y = s.kind === "skywalk" ? 6.5 : s.kind === "footbridge" ? 1.2 : s.kind === "jetty" ? 0.9 : 7 * (s.layer || 1);
      const top = ribbon([s.pts], s.width, y, []);
      group.add(new THREE.Mesh(geomFrom(top), deckM));
      // deck edge (a strip hanging 1.2 m below each side) and pillars every ~28 m
      const pts = s.pts, edge = [];
      for (let i = 0; i < pts.length - 1; i++) {
        const [x0, z0] = pts[i], [x1, z1] = pts[i + 1]; const L = Math.hypot(x1 - x0, z1 - z0); if (!L) continue;
        const nx = -(z1 - z0) / L * s.width / 2, nz = (x1 - x0) / L * s.width / 2;
        for (const sg of [1, -1]) {
          const ax = x0 + nx * sg, az = z0 + nz * sg, bx = x1 + nx * sg, bz = z1 + nz * sg;
          const lip = Math.min(1.2, y);
          edge.push(ax, y, az, bx, y, bz, bx, y - lip, bz, ax, y, az, bx, y - lip, bz, ax, y - lip, az);
        }
        if (s.kind === "flyover") for (let t = 14; t < L; t += 28) {
          const p = new THREE.Mesh(new THREE.BoxGeometry(2.2, y - 1.2, 2.2), sideM);
          p.position.set(x0 + (x1 - x0) * t / L, (y - 1.2) / 2, z0 + (z1 - z0) * t / L); group.add(p);
        }
      }
      group.add(new THREE.Mesh(geomFrom(edge), sideM));
    }
    return group;
  }

  function buildScene(T) {
    const scene = new THREE.Scene();
    scene.background = C(T.sky);
    scene.fog = new THREE.Fog(T.sky, 9000, 26000);
    scene.add(new THREE.HemisphereLight(T.dark ? 0x9fb3c8 : 0xffffff, T.dark ? 0x2a2d31 : 0xd9d2c3, T.dark ? 0.6 : 0.62));
    const sun = new THREE.DirectionalLight(0xffffff, T.dark ? 0.4 : 0.42); sun.position.set(-0.6, 1, -0.35); scene.add(sun);

    const [MW, MH] = G.size;
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(MW + 30000, MH + 30000), new THREE.MeshLambertMaterial({ color: C(T.bush) }));
    ground.rotation.x = -Math.PI / 2; ground.position.set(MW / 2, -0.3, MH / 2); scene.add(ground);
    const flatM = (c) => new THREE.MeshLambertMaterial({ color: C(c), side: THREE.DoubleSide });
    for (const r of G.ocean) scene.add(new THREE.Mesh(flatPoly([r], 0.05), flatM(T.ocean)));
    scene.add(new THREE.Mesh(flatPoly(G.water, 0.1), flatM(T.water)));

    const pick = [];
    for (const d of G.districts) {
      const tint = C(T.land).lerp(C(T["a" + d.act]), T.dark ? 0.1 : 0.07);
      const m = new THREE.Mesh(flatPoly(d.poly, 0.2), new THREE.MeshLambertMaterial({ color: tint, side: THREE.DoubleSide }));
      m.userData.district = d.id; scene.add(m); pick.push(m);
    }
    const PC = { market: T.market, "under-bridge": T.market, industrial: T.industrial, station: T.industrial, school: T.school, pitch: T.pitch, stadium: T.pitch, "motor park": T.park, "bus-terminal": T.park, "bus terminal": T.park, estate: T.pitch, "lorry park": T.park, park: T.pitch, sawmill: T.industrial, government: T.industrial, garden: T.pitch, barracks: T.pitch, airfield: T.pitch, plazas: T.industrial, livestock: T.market, "container yard": T.industrial, "tank farm": T.industrial, villas: T.pitch, prison: T.industrial, "truck park": T.park, waterworks: T.industrial, landfill: T.market, pipeline: T.pitch, compound: T.pitch, club: T.pitch, pool: T.water, court: T.market };
    for (const list of Object.values(G.parcels || {})) for (const p of list) scene.add(new THREE.Mesh(flatPoly([p.pts], 0.35), flatM(PC[p.kind] || T.industrial)));

    const lanes = [], streets = [], mains = [], arts = [];
    for (const list of Object.values(G.lanes || {})) ribbon(list, 3, 0.45, lanes);
    for (const list of Object.values(G.streets)) ribbon(list, 6, 0.5, streets);
    ribbon(G.mains.map((m) => m.pts), 10, 0.55, mains);
    ribbon(G.arterials.filter((a) => a.cls !== "bridge").map((a) => a.pts), 22, 0.6, arts);
    const roadM = (c) => new THREE.MeshLambertMaterial({ color: C(c), side: THREE.DoubleSide });
    scene.add(new THREE.Mesh(geomFrom(lanes), roadM(T.st)));
    scene.add(new THREE.Mesh(geomFrom(streets), roadM(T.st)));
    scene.add(new THREE.Mesh(geomFrom(mains), roadM(T.mn)));
    scene.add(new THREE.Mesh(geomFrom(arts), roadM(T.ar)));
    // water bridges ride above the lagoon
    const br = []; ribbon(G.arterials.filter((a) => a.cls === "bridge").map((a) => a.pts), 24, 9, br);
    scene.add(new THREE.Mesh(geomFrom(br), roadM(T.bridge)));
    // rail: dark ballast with a light centre line
    scene.add(new THREE.Mesh(geomFrom(ribbon([G.rail.pts], 7, 0.65, [])), roadM(T.dark ? "#3a3e44" : "#8f8b84")));
    scene.add(new THREE.Mesh(geomFrom(ribbon([G.rail.pts], 1.6, 0.7, [])), roadM(T.dark ? "#8a8f96" : "#d8d4cc")));
    for (const c of G.canals || []) scene.add(new THREE.Mesh(geomFrom(ribbon([c.pts], 4, 0.62, [])), roadM(T.water)));   // 4 m of water; the banks are walkable
    const foot = []; for (const list of Object.values(G.paths || {})) ribbon(list, 1.5, 0.66, foot);
    scene.add(new THREE.Mesh(geomFrom(foot), roadM(T.dark ? "#7a6a55" : "#c9b48f")));
    if (G.boardwalks) scene.add(new THREE.Mesh(geomFrom(ribbon(G.boardwalks, 2.5, 1.2, [])), roadM(T.dark ? "#7a6a55" : "#b59b76")));

    // compound walls, 2.4 m high, and the estate gates' barriers (a red-and-white pole across the street, 1.1 m up)
    const wallM = new THREE.MeshLambertMaterial({ color: C(T.dark ? "#6d6a66" : "#d9d2c4"), side: THREE.DoubleSide }), wp = [];
    for (const list of Object.values(G.walls || {})) for (const pts of list) for (let i = 0; i < pts.length - 1; i++) {
      const [x0, z0] = pts[i], [x1, z1] = pts[i + 1];
      wp.push(x0, 0, z0, x1, 0, z1, x1, 2.4, z1, x0, 0, z0, x1, 2.4, z1, x0, 2.4, z0);
    }
    if (wp.length) scene.add(new THREE.Mesh(geomFrom(wp), wallM));
    const gp = []; for (const q of G.gates || []) { const [[x0, z0], [x1, z1]] = q.pts; gp.push(x0, 1.0, z0, x1, 1.0, z1, x1, 1.25, z1, x0, 1.0, z0, x1, 1.25, z1, x0, 1.25, z0); }
    if (gp.length) scene.add(new THREE.Mesh(geomFrom(gp), new THREE.MeshLambertMaterial({ color: C("#d93025"), side: THREE.DoubleSide })));
    const b = buildings(T); scene.add(b);
    scene.add(structures(T));
    return { scene, pick, buildingCount: b.userData.count };
  }

  function bboxOf(pts) { let a = [1e9, 1e9, -1e9, -1e9]; for (const [x, y] of pts) a = [Math.min(a[0], x), Math.min(a[1], y), Math.max(a[2], x), Math.max(a[3], y)]; return a; }

  // ---------- the React component ----------
  function View3D({ sel, select, onReady }) {
    const host = useRef(null), labels = useRef(null);
    const api = useRef(null);
    const [info, setInfo] = useState(null);

    useEffect(() => {
      const el = host.current;
      const renderer = new THREE.WebGLRenderer({ antialias: true, logarithmicDepthBuffer: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
      el.appendChild(renderer.domElement);
      const camera = new THREE.PerspectiveCamera(40, 1, 2, 60000);
      const controls = new THREE.MapControls(camera, renderer.domElement);
      controls.enableDamping = true; controls.dampingFactor = 0.12; controls.screenSpacePanning = false;
      controls.maxPolarAngle = 1.32; controls.minDistance = 60; controls.maxDistance = 20000;

      let world = null;
      const build = () => {
        if (world) world.scene.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
        world = buildScene(tokens());
        setInfo({ built: Object.keys(G.buildings || {}).length, total: G.districts.length, count: world.buildingCount });
      };
      build();

      const [MW, MH] = G.size;
      const lookAt = (bb, instant) => {
        if (el.clientWidth > 760) { const w = bb[2] - bb[0]; bb = [bb[0] - w * 0.42, bb[1], bb[2], bb[3]]; }   // keep it clear of the side panel
        const cx = (bb[0] + bb[2]) / 2, cz = (bb[1] + bb[3]) / 2, span = Math.max(bb[2] - bb[0], bb[3] - bb[1], 300);
        const dist = span * 1.15;
        const to = { t: new THREE.Vector3(cx, 0, cz), p: new THREE.Vector3(cx - dist * 0.25, dist * 0.78, cz + dist * 0.62) };
        const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (instant || reduce) { controls.target.copy(to.t); camera.position.copy(to.p); controls.update(); return; }
        const from = { t: controls.target.clone(), p: camera.position.clone() }, t0 = performance.now();
        fly = (now) => { const k = Math.min(1, (now - t0) / 700), e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
          controls.target.lerpVectors(from.t, to.t, e); camera.position.lerpVectors(from.p, to.p, e); if (k >= 1) fly = null; };
      };
      let fly = null;
      lookAt([0, 0, MW, MH * 0.95], true);

      const resize = () => { const w = el.clientWidth, hh = el.clientHeight; renderer.setSize(w, hh); camera.aspect = w / hh; camera.updateProjectionMatrix(); };
      const ro = new ResizeObserver(resize); ro.observe(el); resize();

      // labels: district names far out, landmarks up close
      const LBL = G.districts.map((d) => { const b = bboxOf(d.poly[0]); return { kind: "d", id: d.id, text: d.name, x: (b[0] + b[2]) / 2, z: (b[1] + b[3]) / 2, act: d.act }; })
        .concat(G.pois.map((p, i) => ({ kind: "p", id: i, text: p.name, x: p.x, z: p.y, type: p.type, civic: !!p.civic })).filter((l) => !l.civic));
      const lblEls = LBL.map((l) => {
        const b = document.createElement("button");
        b.className = l.kind === "d" ? "dlabel ui a" + l.act : "poi ui t-" + l.type;
        b.innerHTML = l.kind === "d" ? `<span class="dn"></span>` : `<span class="pin"></span><span class="plabel"></span>`;
        if (l.kind === "d") b.querySelector(".dn").textContent = l.text;
        else { b.querySelector(".pin").textContent = (window.GIDI_TYPE && window.GIDI_TYPE[l.type] || {}).glyph || "•"; b.querySelector(".plabel").textContent = l.text; }
        b.addEventListener("click", () => select(l.kind === "d" ? { kind: "district", id: l.id } : { kind: "poi", id: l.id }, false));
        b.hidden = true; labels.current.appendChild(b); return b;
      });
      const v = new THREE.Vector3(), vc = new THREE.Vector3();
      const placeLabels = () => {
        const w = el.clientWidth, hh = el.clientHeight, dist = camera.position.distanceTo(controls.target);
        LBL.forEach((l, i) => {
          const e = lblEls[i];
          const show = (l.kind === "d" ? dist > 2600 : dist < 2600) && isFinite(l.x) && isFinite(l.z);
          v.set(l.x, l.kind === "d" ? 40 : 12, l.z);
          vc.copy(v).applyMatrix4(camera.matrixWorldInverse);   // behind the camera: never show
          v.project(camera);
          if (!show || vc.z > -1 || v.z > 1 || v.x < -1.1 || v.x > 1.1 || v.y < -1.1 || v.y > 1.1) { e.hidden = true; return; }
          if (l.kind === "p") { const dd = camera.position.distanceTo(new THREE.Vector3(l.x, 0, l.z)); if (dd > 3200) { e.hidden = true; return; } }
          e.hidden = false; e.style.left = ((v.x + 1) / 2 * w) + "px"; e.style.top = ((1 - v.y) / 2 * hh) + "px";
        });
      };

      // click a district to select it
      const ray = new THREE.Raycaster(), mouse = new THREE.Vector2(); let down = null;
      const onDown = (e) => { down = [e.clientX, e.clientY]; };
      const onUp = (e) => {
        if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 5) return; down = null;
        const r = renderer.domElement.getBoundingClientRect();
        mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
        ray.setFromCamera(mouse, camera); const hit = ray.intersectObjects(world.pick)[0];
        select(hit ? { kind: "district", id: hit.object.userData.district } : null, false);
      };
      renderer.domElement.addEventListener("pointerdown", onDown); renderer.domElement.addEventListener("pointerup", onUp);

      let raf, compass = document.getElementById("compass3d");
      const loop = (now) => {
        raf = requestAnimationFrame(loop);
        if (fly) fly(now);
        controls.update(); renderer.render(world.scene, camera); placeLabels();
        if (compass) { const az = Math.atan2(camera.position.x - controls.target.x, camera.position.z - controls.target.z); compass.style.transform = `rotate(${az}rad)`; }
      };
      raf = requestAnimationFrame(loop);

      const mq = matchMedia("(prefers-color-scheme: dark)"); const onTheme = () => build(); mq.addEventListener("change", onTheme);
      const mo = new MutationObserver(onTheme); mo.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });

      api.current = {
        lookAt,
        zoom: (f) => { const off = camera.position.clone().sub(controls.target).multiplyScalar(f); camera.position.copy(controls.target).add(off); },
        home: () => lookAt([0, 0, MW, MH * 0.95]),
        north: () => { const d = camera.position.distanceTo(controls.target), pol = controls.getPolarAngle();
          const to = new THREE.Vector3(controls.target.x, controls.target.y + d * Math.cos(pol), controls.target.z + d * Math.sin(pol));
          const from = camera.position.clone(), t0 = performance.now(); fly = (now) => { const k = Math.min(1, (now - t0) / 500); camera.position.lerpVectors(from, to, k); if (k >= 1) fly = null; }; },
      };
      onReady && onReady(api.current);
      return () => {
        cancelAnimationFrame(raf); ro.disconnect(); mq.removeEventListener("change", onTheme); mo.disconnect(); controls.dispose();
        world.scene.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
        renderer.dispose(); el.removeChild(renderer.domElement); labels.current && (labels.current.innerHTML = "");
        onReady && onReady(null);
      };
    }, []);

    // follow the selection
    useEffect(() => {
      if (!api.current || !sel) return;
      if (sel.kind === "district") { const d = G.districts.find((x) => x.id === sel.id); api.current.lookAt(bboxOf(d.poly[0])); }
      else if (sel.kind === "poi") { const p = G.pois[sel.id]; api.current.lookAt([p.x - 220, p.y - 220, p.x + 220, p.y + 220]); }
      else if (sel.kind === "road") api.current.lookAt(bboxOf(G.arterials[sel.id].pts));
      else if (sel.kind === "street") api.current.lookAt(bboxOf(G.mains[sel.id].pts));
    }, [sel]);

    return h("div", { className: "v3d" },
      h("div", { ref: host, className: "v3d-canvas", "aria-label": "3D view of Gidi. Drag to move, right-drag or two fingers to tilt and turn, scroll to zoom." }),
      h("div", { ref: labels, className: "overlay v3d-labels" }),
      info && h("div", { className: "built ui" },
        h("b", null, `${info.built} of ${info.total}`), " districts built · ", info.count.toLocaleString(), " buildings",
        h("span", null, "Other districts show their sketch streets until they're generated.")));
  }
  window.GidiView3D = View3D;
})();
