/* Gidi Maps, 3D view. Close in, the city is the Blender kit's own models (blender/city_run.py writes
   them as 400 m tiles to web/city/<detail>/tiles): they stream in round where you're looking, the
   light "web" build out to about a kilometre and the full build right up close. Zoomed out, and
   wherever a tile isn't loaded, the city data (window.GIDI) stands in as extruded buildings, raised
   decks and flat ground. The dark theme is Gidi at night: lit windows and street lamps.
   three.js r147 (UMD), MapControls, GLTFLoader + DRACOLoader. Map metres: x east, y south.
   Three.js: X = x, Z = y, Y = up. Exposes window.GidiView3D (a React component) for app.js. */
(function () {
  const { useEffect, useRef, useState } = React;
  const h = React.createElement;
  const G = window.GIDI;
  const STOREY = 3.1;
  const TILE = 400;
  const tileKey = (x, z) => `${Math.floor(x / TILE)}_${Math.floor(z / TILE)}`;
  // where the kit's tiles are: beside the page by default (web/city/), or window.GIDI_TILES
  const TILES_BASE = window.GIDI_TILES || "city/";

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
  function ribbonZ(pts, width, ys, out) {   // like ribbon, one polyline whose height ys[i] varies point by point
    const hw = width / 2;
    for (let i = 0; i < pts.length - 1; i++) {
      const [x0, z0] = pts[i], [x1, z1] = pts[i + 1]; const L = Math.hypot(x1 - x0, z1 - z0); if (L < 0.01) continue;
      const nx = -(z1 - z0) / L * hw, nz = (x1 - x0) / L * hw, y0 = ys[i], y1 = ys[i + 1];
      out.push(x0 + nx, y0, z0 + nz, x0 - nx, y0, z0 - nz, x1 - nx, y1, z1 - nz, x0 + nx, y0, z0 + nz, x1 - nx, y1, z1 - nz, x1 + nx, y1, z1 + nz);
    }
    return out;
  }
  function deckYs(d) {   // a deck's heights above the ground under it: the map's z less a straight line between its two ends (both on the ground)
    const acc = [0]; for (let i = 1; i < d.pts.length; i++) acc.push(acc[i - 1] + Math.hypot(d.pts[i][0] - d.pts[i - 1][0], d.pts[i][1] - d.pts[i - 1][1]));
    const S = acc[acc.length - 1] || 1, a = d.z[0], b = d.z[d.z.length - 1];
    return d.z.map((z, i) => Math.max(0.3, z - (a + (b - a) * acc[i] / S)));
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
    const byTile = new Map();   // the stand-in boxes, one mesh per kit tile so each hides when its models arrive
    let pos, col;
    const walls = T.dark ? ["#6d6a66", "#75706a", "#6a6f72", "#7a7369"] : ["#e9e2d6", "#e3d9c8", "#dcdcd6", "#e6dccd", "#d9d2c4"];
    const tin = T.dark ? ["#6e4a3a", "#5f4d42", "#6b6560"] : ["#a3684a", "#8f5f47", "#9a8f84", "#b07a58"];
    const flat = T.dark ? "#77746f" : "#cfcac0";
    const special = { works: T.dark ? "#7a3f2e" : "#b05a3c", mound: T.dark ? "#4a4236" : "#9c8a6a", bakery: T.dark ? "#8a6a3a" : "#d9a85b", crane: T.dark ? "#8a5b2e" : "#d9822b", stack: T.dark ? "#3b6a8a" : "#4f8fc0", tank: T.dark ? "#8a8f96" : "#e6e8eb", villa: T.dark ? "#6b6250" : "#d8cfb8", cellblock: T.dark ? "#55595e" : "#9aa0a6", tower: T.dark ? "#55595e" : "#80868b", trailer: T.dark ? "#5b5650" : "#b0b4ba", plaza: T.dark ? "#5d6670" : "#c9c1b0", unfinished: T.dark ? "#4a4a4a" : "#b5b5b5", pen: T.dark ? "#5b5650" : "#a59d92", scrap: T.dark ? "#5a4636" : "#8a6a4f", container: T.dark ? "#2f5a8a" : "#3b78b8", "phone mall": T.dark ? "#4f6a86" : "#86a6c8", strip: T.dark ? "#8a3b33" : "#c8645a", hall: T.dark ? "#5e4a86" : "#9b7fc7", office: T.dark ? "#5d6670" : "#c3cad3", barracks: T.dark ? "#55603f" : "#a3ad84", bust: T.dark ? "#888" : "#555", canopy: T.dark ? "#7a4a8c" : "#a86cc1", warehouse: T.dark ? "#5d6670" : "#b9c0c8", stalls: T.dark ? "#8a5b2e" : "#d69a55", school: T.dark ? "#7b6a3c" : "#e1c46a", kiosk: T.dark ? "#4f6a86" : "#7ea2c6", shed: T.dark ? "#5b5650" : "#a59d92", gatehouse: T.dark ? "#8a3b33" : "#c8645a", generator: T.dark ? "#3f4348" : "#5f646a", "water tank": T.dark ? "#2f5a8a" : "#3b78b8", mansion: T.dark ? "#7a6a55" : "#efe6d2", clubhouse: T.dark ? "#5e4a86" : "#9b7fc7", palace: T.dark ? "#8a7a3a" : "#e8d590", "bank tower": T.dark ? "#3f6a8f" : "#8fb8d8", "brazilian house": T.dark ? "#7a4a35" : "#c98a62", "apartment tower": T.dark ? "#355a7a" : "#7fa8cc", nightclub: T.dark ? "#7a2f55" : "#c0628f", "toll booth": T.dark ? "#8a3b33" : "#c8645a", "office block": T.dark ? "#4f5d6e" : "#aebccc", "beach shack": T.dark ? "#6b5636" : "#d8b47a", "beach bar": T.dark ? "#8a4a22" : "#e8955a", "horse shelter": T.dark ? "#5a4636" : "#9c7a5c", column: T.dark ? "#55606b" : "#8d9aa6", "flare stack": T.dark ? "#8a3b33" : "#c84a3a", "unfinished house": T.dark ? "#5a5a5a" : "#a8a8a4", "toll canopy": T.dark ? "#8a3b33" : "#c8645a", "fishing hut": T.dark ? "#6b5636" : "#c9a87a", "colonial house": T.dark ? "#8a7a55" : "#f0e2b0", drums: T.dark ? "#8a3b33" : "#d9622b", "border booth": T.dark ? "#2f5a8a" : "#3b78b8", "border canopy": T.dark ? "#2f5a8a" : "#3b78b8", checkpoint: T.dark ? "#8a3b33" : "#c8645a", "smoke rack": T.dark ? "#3f2e22" : "#6b4a33", barge: T.dark ? "#3b556b" : "#5f86a8", "old house": T.dark ? "#6b5a4a" : "#b89a7e" };
    let n = 0, count = 0;
    const tmp = new THREE.Color();
    // house styles (the Heights: "variety in architecture"): walls, roof colour, and a hipped roof of this height (0 = flat)
    const STYLE = { "colonial bungalow": { wall: ["#f2efe8", "#ece6da"], roof: "#a4473a", hip: 2.4 }, duplex: { wall: ["#e8d9bd", "#dcc9a8"], roof: "#6e4b3a", hip: 2.0 },
      "mediterranean villa": { wall: ["#e7b98a", "#f0cfa6"], roof: "#c0602d", hip: 1.8 }, "modern villa": { wall: ["#f7f7f5", "#d9dde0"], roof: "#5d646b", hip: 0 },
      mansion: { wall: ["#efe6d2", "#e4dccb"], roof: "#4d5560", hip: 3.2 } };
    const shade = (c) => { tmp.set(c); if (T.dark) tmp.multiplyScalar(0.55); return "#" + tmp.getHexString(); };
    function hipRoof(ring, H, rh) {   // a hipped roof on a four-cornered house: a ridge along the long side, slopes down to every wall
      const d = (p, q) => Math.hypot(q[0] - p[0], q[1] - p[1]);
      const cx = (ring[0][0] + ring[1][0] + ring[2][0] + ring[3][0]) / 4, cz = (ring[0][1] + ring[1][1] + ring[2][1] + ring[3][1]) / 4;
      const l1 = d(ring[0], ring[1]), l2 = d(ring[1], ring[2]);
      const [p, q, L, W] = l1 >= l2 ? [ring[0], ring[1], l1, l2] : [ring[1], ring[2], l2, l1];
      const ux = (q[0] - p[0]) / L, uz = (q[1] - p[1]) / L, e = Math.max(0, L / 2 - W / 2);
      const R = [[cx - ux * e, cz - uz * e], [cx + ux * e, cz + uz * e]], out = [];
      for (let j = 0; j < 4; j++) {
        const a = ring[j], b = ring[(j + 1) % 4];
        const ra = d(a, R[0]) <= d(a, R[1]) ? R[0] : R[1], rb = d(b, R[0]) <= d(b, R[1]) ? R[0] : R[1];
        out.push(a[0], H, a[1], b[0], H, b[1], rb[0], H + rh, rb[1]);
        if (ra !== rb) out.push(a[0], H, a[1], rb[0], H + rh, rb[1], ra[0], H + rh, ra[1]);
      }
      return out;
    }
    for (const [id, list] of Object.entries(G.buildings || {})) {
      const st = (G.storeys || {})[id] || [], sty = (G.styles || {})[id] || [];
      list.forEach((b, i) => {
        n++;
        const kind = b[0], ring = b.slice(1); const s = st[i] || 1;
        const key = tileKey(ring[0][0], ring[0][1]);
        if (!byTile.has(key)) byTile.set(key, { pos: [], col: [] });
        ({ pos, col } = byTile.get(key));
        if (kind !== "generator" && kind !== "water tank") count++;   // generator houses and tanks are not counted as buildings
        const H = kind === "stalls" ? 3 : kind === "canopy" ? 2.8 : kind === "mound" ? 5 : kind === "crane" ? 32 : kind === "tank" ? 14 : kind === "stack" ? 7.8 : kind === "trailer" ? 4 : kind === "pen" ? 2.4 : kind === "scrap" ? 2.5 : kind === "container" ? 2.6 : kind === "bust" ? 4 : kind === "kiosk" ? 2.6 : kind === "shed" ? 2.6 : kind === "raft" ? 0.6 : kind === "sawdust" ? 2 : kind === "drums" ? 1.0 : kind === "border canopy" ? 6 : kind === "border booth" ? 2.6 : kind === "column" ? 42 : kind === "flare stack" ? 64 : kind === "toll canopy" ? 6 : kind === "toll booth" ? 2.6 : kind === "generator" ? 1.8 : kind === "water tank" ? 5.5 : kind === "stilt" || kind === "stilt bar" ? s * STOREY + 1.8 : s * STOREY + (s <= 2 ? 0.6 : 0.3);
        const SS = STYLE[sty[i]];
        const wallC = SS ? shade(SS.wall[Math.floor(hash(n) * SS.wall.length)]) : special[kind] || walls[Math.floor(hash(n) * walls.length)];
        const roofC = SS ? shade(SS.roof) : special[kind] || (s <= 2 && hash(n + 7) < 0.62 ? tin[Math.floor(hash(n + 3) * tin.length)] : flat);
        const k = ring.length;
        for (let j = 0; j < k; j++) {   // walls, darker at the foot for a little depth
          const [x0, z0] = ring[j], [x1, z1] = ring[(j + 1) % k];
          pos.push(x0, 0, z0, x1, 0, z1, x1, H, z1, x0, 0, z0, x1, H, z1, x0, H, z0);
          tmp.set(wallC); const top = [tmp.r, tmp.g, tmp.b]; tmp.multiplyScalar(0.72); const bot = [tmp.r, tmp.g, tmp.b];
          col.push(...bot, ...bot, ...top, ...bot, ...top, ...top);
        }
        tmp.set(roofC);
        if (SS && SS.hip && k === 4) {
          const rp = hipRoof(ring, H, SS.hip); pos.push(...rp);
          for (let j = 0; j < rp.length / 3; j++) col.push(tmp.r, tmp.g, tmp.b);
        } else for (let j = 1; j < k - 1; j++) {   // roof fan
          pos.push(ring[0][0], H, ring[0][1], ring[j + 1][0], H, ring[j + 1][1], ring[j][0], H, ring[j][1]);
          col.push(tmp.r, tmp.g, tmp.b, tmp.r, tmp.g, tmp.b, tmp.r, tmp.g, tmp.b);
        }
      });
    }
    const group = new THREE.Group(), meshes = new Map();
    const mat = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide });
    for (const [key, a] of byTile) { const m = new THREE.Mesh(geomFrom(a.pos, a.col), mat); meshes.set(key, m); group.add(m); }
    group.userData.count = count; group.userData.byTile = meshes; return group;
  }

  // flyovers (decks on pillars), skywalks and canal footbridges
  function structures(T, byTile) {   // each deck goes into the tile of its middle (byTile: key -> Group)
    const group = new THREE.Group();
    const into = (key) => { if (!byTile.has(key)) { const g = new THREE.Group(); byTile.set(key, g); group.add(g); } return byTile.get(key); };
    const deckM = new THREE.MeshLambertMaterial({ color: C(T.dark ? "#6b6f75" : "#e4dfd5"), side: THREE.DoubleSide });
    const sideM = new THREE.MeshLambertMaterial({ color: C(T.dark ? "#4b4f55" : "#b9b3a8"), side: THREE.DoubleSide });
    for (const s of G.structures || []) {
      if (s.kind === "culvert") continue;   // flush with the road: nothing to stand in for
      const sloped = (s.kind === "flyover" || s.kind === "approach") && s.z;
      const ys = sloped ? deckYs(s) : null;
      const y = s.kind === "skywalk" ? 6.5 : s.kind === "footbridge" ? 1.2 : s.kind === "jetty" ? 0.9 : sloped ? Math.max(...ys) : 7 * (s.layer || 1);
      const mid = s.pts[Math.floor(s.pts.length / 2)], tg = into(tileKey(mid[0], mid[1]));
      const top = sloped ? ribbonZ(s.pts, s.width, ys, []) : ribbon([s.pts], s.width, y, []);
      tg.add(new THREE.Mesh(geomFrom(top), deckM));
      // deck edge (a strip hanging 1.2 m below each side) and pillars every ~28 m
      const pts = s.pts, edge = [];
      for (let i = 0; i < pts.length - 1; i++) {
        const [x0, z0] = pts[i], [x1, z1] = pts[i + 1]; const L = Math.hypot(x1 - x0, z1 - z0); if (!L) continue;
        const nx = -(z1 - z0) / L * s.width / 2, nz = (x1 - x0) / L * s.width / 2;
        for (const sg of [1, -1]) {
          const ax = x0 + nx * sg, az = z0 + nz * sg, bx = x1 + nx * sg, bz = z1 + nz * sg;
          const ya = sloped ? ys[i] : y, yb = sloped ? ys[i + 1] : y, la = Math.min(1.2, ya), lb = Math.min(1.2, yb);
          edge.push(ax, ya, az, bx, yb, bz, bx, yb - lb, bz, ax, ya, az, bx, yb - lb, bz, ax, ya - la, az);
        }
        if (s.kind === "flyover" && (sloped ? i % 5 === 2 : true)) for (let t = sloped ? L / 2 : 14; t < L; t += 28) {
          const yp = sloped ? (ys[i] + ys[i + 1]) / 2 : y; if (yp < 2.5) continue;
          const p = new THREE.Mesh(new THREE.BoxGeometry(2.2, yp - 1.2, 2.2), sideM);
          p.position.set(x0 + (x1 - x0) * t / L, (yp - 1.2) / 2, z0 + (z1 - z0) * t / L); tg.add(p);
        }
      }
      tg.add(new THREE.Mesh(geomFrom(edge), sideM));
    }
    return group;
  }

  function buildScene(T) {
    const scene = new THREE.Scene();
    const flat = new THREE.Group();   // ground, water, roads and plots from the data; sinks under the models close in
    const stand = new Map();          // tile key -> Group of stand-in decks (and the building box mesh)
    scene.background = C(T.sky);
    scene.fog = new THREE.Fog(T.sky, 9000, 26000);
    const fogFar = scene.fog;
    // light as the Ladi Lane mock had it: a pale harmattan sky, warm bounce off the red earth, a warm sun
    scene.add(new THREE.HemisphereLight(T.dark ? 0x7f93b8 : 0xcfe0ee, T.dark ? 0x2a2d31 : 0x8a5a3a, T.dark ? 0.55 : 0.75));
    if (!T.dark) {
      const skyU = { top: { value: new THREE.Color(0x8fb4cf) }, bottom: { value: new THREE.Color(0xe6d6bc) } };
      const sky = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 16), new THREE.ShaderMaterial({
        side: THREE.BackSide, depthWrite: false, fog: false, uniforms: skyU,
        vertexShader: "varying vec3 vp; void main(){ vp = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
        fragmentShader: "uniform vec3 top; uniform vec3 bottom; varying vec3 vp; void main(){ float h = clamp(normalize(vp).y * 1.6, 0.0, 1.0); gl_FragColor = vec4(mix(bottom, top, pow(h, 0.7)), 1.0); }",
      }));
      sky.renderOrder = -1; sky.frustumCulled = false;
      scene.userData.sky = sky; scene.add(sky);
    }
    // the sun, casting shadows over the ground round the view centre (KitTiles moves it along)
    const sun = new THREE.DirectionalLight(T.dark ? 0x9fb3d8 : 0xffe2b8, T.dark ? 0.2 : 2.3);
    sun.castShadow = !T.dark;
    sun.shadow.mapSize.set(4096, 4096);
    Object.assign(sun.shadow.camera, { left: -450, right: 450, top: 450, bottom: -450, near: 10, far: 3000 });
    sun.shadow.camera.updateProjectionMatrix();
    sun.shadow.bias = -0.0006; sun.shadow.normalBias = 0.6;
    scene.add(sun, sun.target);
    scene.userData.sun = sun;
    scene.add(flat);

    const [MW, MH] = G.size;
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(MW + 30000, MH + 30000), new THREE.MeshLambertMaterial({ color: C(T.bush) }));
    ground.rotation.x = -Math.PI / 2; ground.position.set(MW / 2, -0.3, MH / 2); flat.add(ground);
    const flatM = (c) => new THREE.MeshLambertMaterial({ color: C(c), side: THREE.DoubleSide });
    for (const r of G.ocean) flat.add(new THREE.Mesh(flatPoly([r], 0.05), flatM(T.ocean)));
    flat.add(new THREE.Mesh(flatPoly(G.water, 0.1), flatM(T.water)));

    const pick = [];
    for (const d of G.districts) {
      const tint = C(T.land).lerp(C(T["a" + d.act]), T.dark ? 0.1 : 0.07);
      const m = new THREE.Mesh(flatPoly(d.poly, 0.2), new THREE.MeshLambertMaterial({ color: tint, side: THREE.DoubleSide }));
      m.userData.district = d.id; flat.add(m); pick.push(m);
    }
    const PC = { market: T.market, "under-bridge": T.market, industrial: T.industrial, station: T.industrial, school: T.school, pitch: T.pitch, stadium: T.pitch, "motor park": T.park, "bus-terminal": T.park, "bus terminal": T.park, estate: T.pitch, "lorry park": T.park, park: T.pitch, sawmill: T.industrial, government: T.industrial, garden: T.pitch, barracks: T.pitch, airfield: T.pitch, plazas: T.industrial, livestock: T.market, "container yard": T.industrial, "tank farm": T.industrial, villas: T.pitch, prison: T.industrial, "truck park": T.park, waterworks: T.industrial, landfill: T.market, pipeline: T.pitch, compound: T.pitch, club: T.pitch, pool: T.water, court: T.market, palace: T.pitch, square: T.pitch, enclave: T.dark ? "#5a5240" : "#efe3c2", "golf course": T.dark ? "#3f6b3a" : "#9fd18b", green: T.dark ? "#4f8a47" : "#c3ebb0", bunker: T.dark ? "#6b6040" : "#efe0b0", pond: T.water, refinery: T.industrial, forecourt: T.market, fountain: T.water, "barge yard": T.industrial };
    for (const list of Object.values(G.parcels || {})) for (const p of list) flat.add(new THREE.Mesh(flatPoly([p.pts], 0.35), flatM(PC[p.kind] || T.industrial)));

    const lanes = [], streets = [], mains = [], arts = [];
    for (const list of Object.values(G.lanes || {})) ribbon(list, 3, 0.45, lanes);
    for (const list of Object.values(G.streets)) ribbon(list, 6, 0.5, streets);
    ribbon(G.mains.map((m) => m.pts), 10, 0.55, mains);
    ribbon(G.arterials.filter((a) => a.cls !== "bridge").map((a) => a.pts), 22, 0.6, arts);
    const roadM = (c) => new THREE.MeshLambertMaterial({ color: C(c), side: THREE.DoubleSide });
    flat.add(new THREE.Mesh(geomFrom(lanes), roadM(T.st)));
    flat.add(new THREE.Mesh(geomFrom(streets), roadM(T.st)));
    flat.add(new THREE.Mesh(geomFrom(mains), roadM(T.mn)));
    flat.add(new THREE.Mesh(geomFrom(arts), roadM(T.ar)));
    // water bridges ride above the lagoon
    const brM = roadM(T.bridge), brTile = new Map();
    for (const a of G.arterials.filter((a) => a.cls === "bridge")) {
      const ys = a.z ? deckYs(a) : null;
      for (let i = 0; i < a.pts.length - 1; i++) {   // in 40 m pieces, each in its tile (the map's points are 5 m apart)
        const [x0, z0] = a.pts[i], [x1, z1] = a.pts[i + 1], n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, z1 - z0) / 40));
        for (let k = 0; k < n; k++) {
          const p = [[x0 + (x1 - x0) * k / n, z0 + (z1 - z0) * k / n], [x0 + (x1 - x0) * (k + 1) / n, z0 + (z1 - z0) * (k + 1) / n]];
          const key = tileKey((p[0][0] + p[1][0]) / 2, (p[0][1] + p[1][1]) / 2);
          if (!brTile.has(key)) brTile.set(key, []);
          if (ys) { const y0 = ys[i] + (ys[i + 1] - ys[i]) * k / n, y1 = ys[i] + (ys[i + 1] - ys[i]) * (k + 1) / n; ribbonZ(p, 24, [y0, y1], brTile.get(key)); }
          else ribbon([p], 24, 9, brTile.get(key));
        }
      }
    }
    // rail: dark ballast with a light centre line
    flat.add(new THREE.Mesh(geomFrom(ribbon([G.rail.pts], 7, 0.65, [])), roadM(T.dark ? "#3a3e44" : "#8f8b84")));
    flat.add(new THREE.Mesh(geomFrom(ribbon([G.rail.pts], 1.6, 0.7, [])), roadM(T.dark ? "#8a8f96" : "#d8d4cc")));
    for (const c of G.canals || []) flat.add(new THREE.Mesh(geomFrom(ribbon([c.pts], 4, 0.62, [])), roadM(T.water)));   // 4 m of water; the banks are walkable
    const foot = []; for (const list of Object.values(G.paths || {})) ribbon(list, 1.5, 0.66, foot);
    flat.add(new THREE.Mesh(geomFrom(foot), roadM(T.dark ? "#7a6a55" : "#c9b48f")));
    if (G.boardwalks) flat.add(new THREE.Mesh(geomFrom(ribbon(G.boardwalks, 2.5, 1.2, [])), roadM(T.dark ? "#7a6a55" : "#b59b76")));

    // compound walls, 2.4 m high, and the estate gates' barriers (a red-and-white pole across the street, 1.1 m up)
    const wallM = new THREE.MeshLambertMaterial({ color: C(T.dark ? "#6d6a66" : "#d9d2c4"), side: THREE.DoubleSide }), wp = [];
    for (const list of Object.values(G.walls || {})) for (const pts of list) for (let i = 0; i < pts.length - 1; i++) {
      const [x0, z0] = pts[i], [x1, z1] = pts[i + 1];
      wp.push(x0, 0, z0, x1, 0, z1, x1, 2.4, z1, x0, 0, z0, x1, 2.4, z1, x0, 2.4, z0);
    }
    if (wp.length) flat.add(new THREE.Mesh(geomFrom(wp), wallM));
    const gp = []; for (const q of G.gates || []) { const [[x0, z0], [x1, z1]] = q.pts; gp.push(x0, 1.0, z0, x1, 1.0, z1, x1, 1.25, z1, x0, 1.0, z0, x1, 1.25, z1, x0, 1.25, z0); }
    if (gp.length) flat.add(new THREE.Mesh(geomFrom(gp), new THREE.MeshLambertMaterial({ color: C("#d93025"), side: THREE.DoubleSide })));
    const b = buildings(T); scene.add(b);
    scene.add(structures(T, stand));
    for (const [key, m] of b.userData.byTile) { if (!stand.has(key)) { const g = new THREE.Group(); stand.set(key, g); scene.add(g); } stand.get(key).userData.boxes = m; }
    for (const [key, tri] of brTile) { if (!stand.has(key)) { const g = new THREE.Group(); stand.set(key, g); scene.add(g); } stand.get(key).add(new THREE.Mesh(geomFrom(tri), brM)); }
    return { scene, pick, flat, stand, fogFar, dark: T.dark, buildingCount: b.userData.count };
  }


  // ---------- the kit's models, streamed by tile ----------
  // Kit materials come back by name (blender/gidi_kit/materials.py); colours ride on the vertices.
  function kitMaterial(name, dark) {
    // both sides: some kit faces are wound the other way (they look fine in Blender, which draws
    // both sides), and three would show those as holes into the model. Back faces get their
    // normal flipped, so they are lit as if built the right way round.
    const base = { vertexColors: true, roughness: 0.85, metalness: 0, side: THREE.DoubleSide, shadowSide: THREE.FrontSide };
    if (name === "glass") return new THREE.MeshStandardMaterial({ ...base, roughness: 0.08, metalness: 0.4 });
    if (name === "glass_lit") return new THREE.MeshStandardMaterial({ ...base, roughness: 0.08, metalness: 0.4, emissive: dark ? 0xffc77a : 0x000000, emissiveIntensity: dark ? 0.9 : 0 });
    if (name === "lamp") return new THREE.MeshBasicMaterial({ color: dark ? 0xffe2a8 : 0x9a9a92, side: THREE.DoubleSide });
    if (name === "emit") return new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide });
    if (name === "water") return new THREE.MeshStandardMaterial({ ...base, roughness: 0.12, metalness: 0.1 });
    if (name === "zinc" || name === "steel") return new THREE.MeshStandardMaterial({ ...base, roughness: 0.45, metalness: 0.45 });
    if (name === "asphalt") return new THREE.MeshStandardMaterial({ ...base, roughness: 0.95 });
    return new THREE.MeshStandardMaterial(base);
  }

  class KitTiles {
    constructor(world, dark) {
      this.world = world; this.dark = dark;
      this.group = new THREE.Group(); world.scene.add(this.group);
      this.loaded = new Map();   // key -> { detail, obj } | "loading"
      this.mats = new Map(); this.manifest = null; this.busy = 0; this.lastKey = ""; this.lastAt = 0;
      this.failed = new Set();   // "k/detail" that wouldn't load: use the other detail there
      this.newLoader();
      fetch(TILES_BASE + "manifest.json").then((r) => (r.ok ? r.json() : null)).then((m) => { this.manifest = m; }, () => {});
    }
    newLoader() {   // again after a failed decode: an aborted decoder fails every tile after it (the old one isn't disposed: another tile may still be decoding on it)
      this.draco = new THREE.DRACOLoader();
      this.draco.setDecoderPath("https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/libs/draco/");   // decoder 1.5.6: the full tiles are too big for r147's
      this.draco.setWorkerLimit(1);
      this.loader = new THREE.GLTFLoader(); this.loader.setDRACOLoader(this.draco);
    }
    material(name) {
      if (!this.mats.has(name)) this.mats.set(name, kitMaterial(name, this.dark));
      return this.mats.get(name);
    }
    // camera distance d from the target decides how much to load: none far out, the light build to
    // ~1.2 km, the full build for the nearest tiles when you're right in
    update(now, target, d) {
      if (!this.manifest || now - this.lastAt < 250) return;
      this.lastAt = now;
      const close = d < 2600;
      const ring = !close ? -1 : d < 1200 ? 1 : 2;   // a light tile is ~1M triangles: 9 to 25 of them
      const full = d < 450;                          // a full one is ~7M: only the tile you're over
      const tx = Math.floor(target.x / TILE), ty = Math.floor(target.z / TILE);
      const want = new Map();
      for (let dx = -ring; dx <= ring; dx++) for (let dy = -ring; dy <= ring; dy++) {
        const k = `${tx + dx}_${ty + dy}`, have = this.manifest.tiles[k];
        if (!have) continue;
        const r = Math.max(Math.abs(dx), Math.abs(dy));
        const ok = (d) => have[d] && !this.failed.has(k + "/" + d);
        const det = full && r === 0 && ok("full") ? "full" : ok("web") ? "web" : ok("full") ? "full" : "";
        if (det) want.set(k, [det, r]);
      }
      for (const [k, v] of [...this.loaded]) {   // drop what's out of range (a change of detail swaps when the new one arrives)
        if (v === "loading" || k.includes("#")) continue;
        if (!want.has(k)) this.drop(k);
      }
      // sink the data's flat ground under the models while any are up; show stand-ins where they aren't
      this.world.flat.position.y = close ? -1.6 : 0;
      const sun = this.world.scene.userData.sun;   // shadows follow the view centre, on the same heading as ever
      sun.target.position.set(target.x, 0, target.z); sun.position.set(target.x - 1000, 1050, target.z - 600); sun.target.updateMatrixWorld();
      for (const [k, g] of this.world.stand) {
        const up = this.loaded.get(k), has = up && up !== "loading";
        g.visible = !has; if (g.userData.boxes) g.userData.boxes.visible = !has;
      }
      const order = [...want.entries()].sort((a, b) => a[1][1] - b[1][1]);
      for (const [k, [det]] of order) {
        if (this.busy >= 2 || (det === "full" && this.busy > 0)) break;   // never decode a full tile alongside others
        const cur = this.loaded.get(k);
        if (cur === "loading" || (cur && cur.detail === det) || this.loaded.get(k + "#next") === "loading") continue;
        this.fetchTile(k, det, !!cur);
      }
    }
    fetchTile(k, det, upgrade) {
      const slot = upgrade ? k + "#next" : k;
      this.loaded.set(slot, "loading"); this.busy++;
      const [ax, ay] = k.split("_").map(Number);
      let over = false;
      const fail = () => { if (over) return; over = true; this.busy--; this.loaded.delete(slot); this.failed.add(k + "/" + det); this.newLoader(); };
      const timer = setTimeout(fail, det === "full" ? 60000 : 30000);   // an aborted decoder never calls back
      this.loader.load(TILES_BASE + det + "/tiles/" + k + ".glb", (gltf) => {
        if (over) return;
        over = true; clearTimeout(timer); this.busy--;
        const obj = gltf.scene;
        obj.position.set(ax * TILE, 0, (ay + 1) * TILE);   // the tile's corner (Blender's y north is the map's y south)
        obj.traverse((o) => {
          if (!o.isMesh) return;
          const name = ((o.material && o.material.name) || "paint").split(".")[0];
          if (o.material && o.material.dispose) o.material.dispose();
          o.material = this.material(name);
          o.castShadow = o.receiveShadow = name !== "emit" && name !== "lamp";
        });
        if (upgrade) { this.drop(k); this.loaded.delete(slot); }
        else this.loaded.delete(slot);
        this.group.add(obj); this.loaded.set(k, { detail: det, obj });
      }, undefined, () => { clearTimeout(timer); fail(); });
    }
    drop(k) {
      const v = this.loaded.get(k);
      if (v && v !== "loading") { this.group.remove(v.obj); v.obj.traverse((o) => o.geometry && o.geometry.dispose()); }
      this.loaded.delete(k);
    }
    dispose() {
      for (const k of [...this.loaded.keys()]) this.drop(k);
      for (const m of this.mats.values()) m.dispose();
      this.world.scene.remove(this.group);
    }
  }

  function bboxOf(pts) { let a = [1e9, 1e9, -1e9, -1e9]; for (const [x, y] of pts) a = [Math.min(a[0], x), Math.min(a[1], y), Math.max(a[2], x), Math.max(a[3], y)]; return a; }

  // ---------- the React component ----------
  function View3D({ sel, select, onReady }) {
    const host = useRef(null), labels = useRef(null);
    const api = useRef(null);
    const [info, setInfo] = useState(null);

    useEffect(() => {
      const el = host.current;
      // no logarithmic depth: it breaks the sun's shadows; near and far follow the zoom instead (loop)
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.outputEncoding = THREE.sRGBEncoding;
      renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;   // the Ladi Lane mock's look
      renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;

      renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
      el.appendChild(renderer.domElement);
      const camera = new THREE.PerspectiveCamera(40, 1, 0.5, 60000);
      const controls = new THREE.MapControls(camera, renderer.domElement);
      controls.enableDamping = true; controls.dampingFactor = 0.12; controls.screenSpacePanning = false;
      controls.maxPolarAngle = 1.45; controls.minDistance = 25; controls.maxDistance = 20000;

      let world = null, kit = null;
      const build = () => {
        if (kit) kit.dispose();
        if (world) world.scene.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
        const T = tokens();
        world = buildScene(T);
        kit = new KitTiles(world, T.dark);
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
        controls.update();
        const dist = camera.position.distanceTo(controls.target);
        const near = Math.max(0.5, dist * 0.01), far = Math.max(8000, dist * 30);
        if (Math.abs(camera.near - near) > near * 0.2 || camera.far !== far) { camera.near = near; camera.far = far; camera.updateProjectionMatrix(); }
        kit.update(now, controls.target, dist);
        const sky = world.scene.userData.sky;
        if (sky) { sky.position.copy(camera.position); sky.scale.setScalar(far * 0.9); }
        if (!world.dark) {
          if (dist < 2600) {   // harmattan haze close in, thinning as you pull back
            if (!world.scene.fog.isFogExp2) world.scene.fog = new THREE.FogExp2(0xdccfb6, 0);
            world.scene.fog.density = 0.45 / Math.max(dist, 250);
          } else if (world.scene.fog.isFogExp2) world.scene.fog = world.fogFar;
        }
        renderer.render(world.scene, camera); placeLabels();
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
      window.__gidi3d = { ...api.current, camera, controls, renderer, world: () => world, tiles: () => kit && [...kit.loaded.keys()] };   // for checking the view from a script
      return () => {
        cancelAnimationFrame(raf); ro.disconnect(); mq.removeEventListener("change", onTheme); mo.disconnect(); controls.dispose(); kit.dispose();
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
