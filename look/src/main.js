// Renderer, light, sky, the A/B look toggle, dusk bloom, crowd, traffic, cameras and UI.
(() => {
  const D = window.AREA;
  const K = KIT; const { V, M, along, length, offsetLine } = K;
  const { R, pick } = TEX;
  const Q = new URLSearchParams(location.search);
  const mobile = /iPhone|iPad|iPod|Android/.test(navigator.userAgent) || (navigator.maxTouchPoints > 1 && /Mac/.test(navigator.userAgent));

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: Q.has('shot'), powerPreference: 'high-performance' });
  let pixelRatio = Math.min(window.devicePixelRatio, mobile ? 1.5 : 2);
  renderer.setPixelRatio(pixelRatio);
  renderer.setSize(innerWidth, innerHeight);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
  document.getElementById('app').appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, 0.3, 2000);

  // ---------- the look: shared uniforms read by every material ----------
  const LOOK = { uGrit: { value: 0 }, uAO: { value: null }, uAOBox: { value: new THREE.Vector4(-200, -200, 400, 400) } };
  const NOISE = `
    float h31(vec3 p){ p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
    float vnoise(vec3 x){ vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);
      return mix(mix(mix(h31(i), h31(i + vec3(1,0,0)), f.x), mix(h31(i + vec3(0,1,0)), h31(i + vec3(1,1,0)), f.x), f.y),
                 mix(mix(h31(i + vec3(0,0,1)), h31(i + vec3(1,0,1)), f.x), mix(h31(i + vec3(0,1,1)), h31(i + vec3(1,1,1)), f.x), f.y), f.z); }`;
  // contact occlusion for everything near the ground; in B also stains, rain streaks, red mud splash, uneven paint and rust
  const GRIME = `
    {
      vec2 auv = (vWP.xz - uAOBox.xy) / uAOBox.zw;
      float ao = texture2D(uAO, auv).r;
      diffuseColor.rgb *= mix(1.0, ao, 1.0 - smoothstep(0.0, 2.8, vWP.y));
      float g = uGrit * uDirt;
      if (g > 0.001) {
        float wall = 1.0 - abs(vWN.y);
        float n1 = vnoise(vWP * 0.42) * 0.6 + vnoise(vWP * 1.6) * 0.4;
        float n2 = vnoise(vWP * 5.5);
        float streak = vnoise(vec3((vWP.x + vWP.z) * 2.6, vWP.y * 0.16, 3.7));
        float under = smoothstep(0.35, 0.0, fract(vWP.y / 3.1));            // grime collects under each floor line
        float splash = (1.0 - smoothstep(0.0, 0.7 + n1 * 0.7, vWP.y)) * wall;
        float stain = smoothstep(0.42, 0.8, n1) * 0.7 + wall * smoothstep(0.35, 0.85, streak) * (0.5 + under * 0.5);
        diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * vec3(0.46, 0.39, 0.31), clamp(stain * g, 0.0, 0.85));
        float faded = smoothstep(0.55, 0.8, vnoise(vWP * 0.9 + 7.0)) * wall;   // patches where the paint has gone chalky
        diffuseColor.rgb = mix(diffuseColor.rgb, vec3(dot(diffuseColor.rgb, vec3(0.33))) * 1.15, faded * 0.5 * g);
        diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.36, 0.16, 0.08), splash * 0.6 * g);
        diffuseColor.rgb *= 1.0 + (n2 - 0.5) * 0.3 * g;
        if (uRust > 0.0) {
          float r = smoothstep(0.4, 0.72, vnoise(vWP * 0.8) * 0.65 + n2 * 0.35);
          diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.34, 0.13, 0.05) * (0.7 + n2 * 0.6), r * g * uRust);
        }
      }
    }`;
  function patch(mat, o = {}) {
    mat.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, LOOK, { uDirt: { value: o.dirt == null ? 1 : o.dirt }, uRust: { value: o.rust || 0 } });
      sh.vertexShader = 'varying vec3 vWP; varying vec3 vWN;\n' + sh.vertexShader.replace('#include <project_vertex>', `#include <project_vertex>
        vec4 lw = vec4(transformed, 1.0);
        #ifdef USE_INSTANCING
          lw = instanceMatrix * lw;
        #endif
        lw = modelMatrix * lw; vWP = lw.xyz; vWN = normalize(mat3(modelMatrix) * objectNormal);`);
      sh.fragmentShader = 'uniform float uGrit; uniform float uDirt; uniform float uRust; uniform sampler2D uAO; uniform vec4 uAOBox; varying vec3 vWP; varying vec3 vWN;\n' + NOISE + '\n' +
        sh.fragmentShader.replace('#include <color_fragment>', '#include <color_fragment>\n' + GRIME);
    };
    mat.customProgramCacheKey = () => 'look';
    return mat;
  }
  const std = (o, p) => patch(new THREE.MeshStandardMaterial(Object.assign({ roughness: 0.85, metalness: 0, vertexColors: true }, o)), p);

  const ATLAS = TEX.atlases(WORLD.signs());
  const RIDGES = TEX.ridges(false), RIDGES_V = TEX.ridges(true);
  const MATS = {
    paint: std({}),
    metal: std({ roughness: 0.45, metalness: 0.35 }, { dirt: 0.8, rust: 0.6 }),
    roof: std({ roughness: 0.5, metalness: 0.3, bumpMap: RIDGES, bumpScale: 0.3, side: THREE.DoubleSide }, { rust: 1 }),
    shutter: std({ roughness: 0.5, metalness: 0.35, bumpMap: RIDGES_V, bumpScale: 0.3, side: THREE.DoubleSide }, { rust: 0.5 }),
    glass: std({ roughness: 0.15, metalness: 0.3 }, { dirt: 0.3 }),
    glassLit: std({ roughness: 0.15, metalness: 0.3, emissive: 0x000000 }, { dirt: 0.3 }),
    ground: std({ roughness: 1 }),
    water: std({ roughness: 0.05, metalness: 0.2 }, { dirt: 0.2 }),
    leaf: std({ roughness: 0.9, flatShading: true }, { dirt: 0.3 }),
    tarp: std({ roughness: 0.7, side: THREE.DoubleSide }, { dirt: 0.6 }),
    sign: std({ map: ATLAS.a, roughness: 0.7, vertexColors: false, emissive: 0x000000, emissiveMap: ATLAS.a }, { dirt: 0.35 }),
    wallPaint: std({ map: ATLAS.b, roughness: 0.9, vertexColors: false, alphaTest: 0.5, polygonOffset: true, polygonOffsetFactor: -2 }, { dirt: 0.4 }),
    emit: new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }),
    emitRed: new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }),
    pool: new THREE.MeshBasicMaterial({ map: TEX.glow(), vertexColors: true, transparent: true, opacity: 0.55, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }),
  };
  const mats = (k) => MATS[k] || MATS.paint;

  // ---------- sky, clouds, light ----------
  const skyU = { top: { value: new THREE.Color() }, mid: { value: new THREE.Color() }, bottom: { value: new THREE.Color() }, sunDir: { value: V(0, 1, 0) }, sunCol: { value: new THREE.Color() } };
  const sky = new THREE.Mesh(new THREE.SphereGeometry(1500, 32, 16), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: 'varying vec3 vp; void main(){ vp = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: `uniform vec3 top; uniform vec3 mid; uniform vec3 bottom; uniform vec3 sunDir; uniform vec3 sunCol; varying vec3 vp;
      void main(){ vec3 d = normalize(vp); float h = clamp(d.y, 0.0, 1.0);
        vec3 c = mix(bottom, mid, smoothstep(0.0, 0.18, h)); c = mix(c, top, smoothstep(0.15, 0.8, h));
        float s = max(dot(d, normalize(sunDir)), 0.0); c += sunCol * (pow(s, 600.0) * 2.0 + pow(s, 12.0) * 0.25);
        gl_FragColor = vec4(c, 1.0); }`,
  }));
  scene.add(sky);
  scene.fog = new THREE.FogExp2(0xcfe4f2, 0.0022);
  // low-poly clouds: clusters of flattened faceted puffs
  const cloudMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, flatShading: true, fog: false, emissive: 0xffffff, emissiveIntensity: 0.25 });
  {
    TEX.setSeed(31337);
    const cb = new K.Builder();
    for (let i = 0; i < 22; i++) {
      const a = R(0, Math.PI * 2), r = R(420, 900), x = Math.cos(a) * r, z = Math.sin(a) * r, y = R(170, 300), s = R(18, 40);
      for (let k = 0; k < 6; k++) cb.geo('cloud', K.G.ico1, M(x + R(-1.4, 1.4) * s, y + R(-0.15, 0.3) * s, z + R(-0.8, 0.8) * s, R(0, 6), s * R(0.6, 1.0), s * R(0.4, 0.6), s * R(0.6, 1.0)));
    }
    cb.build(() => cloudMat, scene, () => [false, false]);
  }
  const hemi = new THREE.HemisphereLight(0xcfe6ff, 0xb08060, 0.9); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xfff1dc, 2.4);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.04; sun.shadow.radius = 3;
  scene.add(sun, sun.target);
  const SUN_DIR = { day: V(-0.55, 0.72, 0.42).normalize(), dusk: V(-0.95, 0.13, 0.28).normalize() };

  // ---------- the world ----------
  const W = WORLD.build(scene, D, mats, ATLAS.uv);
  LOOK.uAO.value = TEX.aoMap(1024, 200, W.aoShapes);

  // ---------- the crowd: one instanced mesh per body part ----------
  const ANKARA = TEX.ankara(); ANKARA.repeat.set(3, 3);
  const pm = (o, dirt = 0.25) => patch(new THREE.MeshStandardMaterial(Object.assign({ roughness: 0.8 }, o)), { dirt });
  const PM = { skin: pm({ roughness: 0.55 }, 0.1), cloth: pm({}), print: pm({ map: ANKARA }), dark: pm({ roughness: 0.6 }, 0.1) };
  function crowd(list, parent) {
    const P = K.PEOPLE; const parts = {};
    const add = (name, geo, mat, p, color) => { (parts[name] = parts[name] || { geo, mat, items: [] }).items.push([p, color]); };
    list.forEach(p => {
      add('skin', P.skin, PM.skin, p, p.skin); add('dark', P.dark, PM.dark, p, 0x161210);
      add(p.print ? 'topP' : 'top', P.top, p.print ? PM.print : PM.cloth, p, p.top);
      if (p.woman) add('wrap', P.wrapper, PM.print, p, p.wrap); else add('legs', P.trousers, PM.cloth, p, p.bottom);
      if (p.gele) add('gele', P.gele, PM.print, p, p.gele);
      if (p.cap) add('cap', P.cap, PM.cloth, p, p.cap);
      if (p.load) add('load', P.load, PM.cloth, p, p.load);
    });
    const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), up = V(0, 1, 0);
    Object.values(parts).forEach(({ geo, mat, items }) => {
      const im = new THREE.InstancedMesh(geo, mat, items.length);
      items.forEach(([p, c], i) => { const s = p.h / 1.7; m4.compose(V(p.x, 0, p.z), q.setFromAxisAngle(up, p.a), V(s, s, s)); im.setMatrixAt(i, m4); im.setColorAt(i, K.col(c)); });
      im.castShadow = true; im.receiveShadow = true; parent.add(im);
    });
  }
  // keep the five camera spots clear (nobody standing in the lens)
  const spots = (() => { const P = D.pins, st = P['The steal'], out = [[st[0] + 3.5, st[1] + 7.5], [st[0] + 18, st[1] + 8.2]];
    const a = W.aisles.reduce((a, b) => Math.abs(b[1][0] - b[0][0]) > Math.abs(a[1][0] - a[0][0]) ? b : a), w = a[0][0] < a[a.length - 1][0] ? a : a.slice().reverse(), p = along(w, 26); out.push([p.x, p.z]);
    if (W.ring) { const q = along(offsetLine(W.ring.pts, -(W.ring.w / 2 + 0.9)), W.S0 + 25); out.push([q.x, q.z]); }
    return out; })();
  const clear = (l) => l.filter(p => spots.every(([x, z]) => Math.hypot(p.x - x, p.z - z) > 3.2));
  crowd(clear(W.people.common), W.groups.common); crowd(clear(W.people.grit), W.groups.grit);

  // ---------- traffic ----------
  const movers = [];
  const vehicleMesh = (geos) => { const g = new THREE.Group(); for (const k in geos) { const m = new THREE.Mesh(geos[k], mats(k)); m.castShadow = k !== 'emit'; g.add(m); } scene.add(g); return g; };
  const addMover = (geos, path, speed, s0, bob) => movers.push({ obj: vehicleMesh(geos), path, L: length(path), s: s0, v: speed, bob: bob || 0, ph: R(0, 6) });
  TEX.setSeed(777);
  if (W.ring) {
    const fwd = W.ring.pts, back = fwd.slice().reverse();
    [offsetLine(fwd, 2.0), offsetLine(fwd, 5.0), offsetLine(back, 2.0), offsetLine(back, 5.0)].forEach(p => {
      const L = length(p);
      for (let i = 0; i < 4; i++) { const r = TEX.rnd(); addMover(r < 0.45 ? pick(W.veh.danfo) : r < 0.75 ? pick(W.veh.car) : pick(W.veh.keke), p, R(4, 8), (i / 4) * L + R(0, 20), 0.03); }
    });
    for (let i = 0; i < 5; i++) addMover(pick(W.veh.okadaRider), offsetLine(i % 2 ? fwd : back, 5.7), R(9, 12), R(0, 400), 0.02);
  }
  const streets = W.roads.filter(r => r.k === 'street' && length(r.pts) > 60);
  for (let i = 0; i < 9; i++) { const r = streets[i % streets.length]; const p = TEX.rnd() < 0.5 ? r.pts : r.pts.slice().reverse(); addMover(pick(W.veh.okadaRider), offsetLine(p, 1.6), R(6, 10), R(0, length(p)), 0.02); }

  // ---------- dusk bloom: scene -> bright pass -> blur -> add ----------
  const post = (() => {
    const gl2 = renderer.capabilities.isWebGL2;
    const opt = { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, format: THREE.RGBAFormat };
    const rtScene = gl2 ? new THREE.WebGLMultisampleRenderTarget(1, 1, opt) : new THREE.WebGLRenderTarget(1, 1, opt);
    rtScene.texture.encoding = THREE.sRGBEncoding; // materials write display-ready colour
    const rtA = new THREE.WebGLRenderTarget(1, 1, opt), rtB = new THREE.WebGLRenderTarget(1, 1, opt);
    const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1), sc = new THREE.Scene(), quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2)); sc.add(quad);
    const VS = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }';
    const sm = (u, fs) => new THREE.ShaderMaterial({ uniforms: u, vertexShader: VS, fragmentShader: fs, depthTest: false, depthWrite: false });
    const bright = sm({ t: { value: null }, thr: { value: 0.78 } }, 'uniform sampler2D t; uniform float thr; varying vec2 vUv; void main(){ vec3 c = texture2D(t, vUv).rgb; float l = max(c.r, max(c.g, c.b)); gl_FragColor = vec4(c * smoothstep(thr, 1.0, l), 1.0); }');
    const blur = sm({ t: { value: null }, d: { value: new THREE.Vector2() } }, `uniform sampler2D t; uniform vec2 d; varying vec2 vUv;
      void main(){ vec3 c = texture2D(t, vUv).rgb * 0.227;
        c += (texture2D(t, vUv + d * 1.385).rgb + texture2D(t, vUv - d * 1.385).rgb) * 0.316;
        c += (texture2D(t, vUv + d * 3.231).rgb + texture2D(t, vUv - d * 3.231).rgb) * 0.070;
        gl_FragColor = vec4(c, 1.0); }`);
    const comp = sm({ s: { value: rtScene.texture }, b: { value: rtA.texture }, k: { value: 1.1 } }, 'uniform sampler2D s; uniform sampler2D b; uniform float k; varying vec2 vUv; void main(){ gl_FragColor = vec4(texture2D(s, vUv).rgb + texture2D(b, vUv).rgb * k, 1.0); }');
    const size = new THREE.Vector2();
    function resize() { renderer.getDrawingBufferSize(size); rtScene.setSize(size.x, size.y); rtA.setSize(size.x >> 2, size.y >> 2); rtB.setSize(size.x >> 2, size.y >> 2); }
    function pass(m, target) { quad.material = m; renderer.setRenderTarget(target); renderer.render(sc, cam); }
    function render() {
      renderer.setRenderTarget(rtScene); renderer.render(scene, camera);
      bright.uniforms.t.value = rtScene.texture; pass(bright, rtA);
      [1, 2].forEach(k => {
        blur.uniforms.t.value = rtA.texture; blur.uniforms.d.value.set(k / rtA.width, 0); pass(blur, rtB);
        blur.uniforms.t.value = rtB.texture; blur.uniforms.d.value.set(0, k / rtA.height); pass(blur, rtA);
      });
      pass(comp, null);
    }
    return { resize, render };
  })();
  post.resize();

  // ---------- look and time ----------
  let look = Q.get('look') === 'b' ? 'b' : 'a', dusk = Q.get('time') === 'dusk';
  function setLook(l) {
    look = l;
    LOOK.uGrit.value = l === 'b' ? 1 : 0;
    W.groups.clean.visible = l === 'a'; W.groups.grit.visible = l === 'b';
    MATS.sign.map = MATS.sign.emissiveMap = l === 'a' ? ATLAS.a : ATLAS.b; MATS.sign.needsUpdate = true;
    scene.fog.density = l === 'a' ? 0.0016 : 0.002; // B: a little dust in the air
    ui();
  }
  function setTime(d) {
    dusk = d;
    const dir = d ? SUN_DIR.dusk : SUN_DIR.day;
    skyU.sunDir.value.copy(dir);
    if (!d) {
      sun.color.set(0xfff1dc); sun.intensity = 2.5; hemi.color.set(0xcfe6ff); hemi.groundColor.set(0xb08060); hemi.intensity = 0.95;
      skyU.top.value.set(0x2f7fd6); skyU.mid.value.set(0x7fbcef); skyU.bottom.value.set(0xd8ecf8); skyU.sunCol.value.set(0xfff4d8);
      scene.fog.color.set(0xcfe4f2); renderer.toneMappingExposure = 1.0;
      cloudMat.color.set(0xffffff); cloudMat.emissive.set(0xffffff); cloudMat.emissiveIntensity = 0.3;
    } else {
      sun.color.set(0xff9248); sun.intensity = 1.6; hemi.color.set(0x7d7fc0); hemi.groundColor.set(0x5a3a2c); hemi.intensity = 0.55;
      skyU.top.value.set(0x1b2560); skyU.mid.value.set(0x8a5a8e); skyU.bottom.value.set(0xf59a52); skyU.sunCol.value.set(0xffa050);
      scene.fog.color.set(0x8a6a78); renderer.toneMappingExposure = 1.12;
      cloudMat.color.set(0xffc2a0); cloudMat.emissive.set(0xff9a70); cloudMat.emissiveIntensity = 0.35;
    }
    MATS.glassLit.emissive.set(d ? 0xffb55e : 0x000000); MATS.glassLit.emissiveIntensity = 1.5;
    MATS.sign.emissive.set(d ? 0x7a6a58 : 0x000000);
    MATS.emit.color.setScalar(d ? 2.4 : 0.85); MATS.emitRed.color.setScalar(d ? 2.0 : 0.7);
    W.groups.dusk.visible = d;
    ui();
  }

  // shadows follow the camera: wide for the overview, tight and sharp for eye level
  function fitShadow(cx, cz, half) {
    const dir = dusk ? SUN_DIR.dusk : SUN_DIR.day;
    sun.target.position.set(cx, 0, cz); sun.position.set(cx + dir.x * 300, dir.y * 300, cz + dir.z * 300);
    const c = sun.shadow.camera; c.left = -half; c.right = half; c.top = half; c.bottom = -half; c.near = 10; c.far = 800; c.updateProjectionMatrix();
  }

  // ---------- labels ----------
  const labelsEl = document.getElementById('labels');
  const LBL = [['The steal', 'Mama Put stall: the opening steal'], ["Boss's post", "Boss's post"], ["Tunde's room", "Tunde's room"], ['Ladi Lane Parts Market', 'Ladi Lane Parts Market']];
  const labels = LBL.filter(([k]) => D.pins[k]).map(([k, t]) => { const e = document.createElement('div'); e.className = 'lbl'; e.textContent = t; labelsEl.appendChild(e); return { e, p: V(D.pins[k][0], k === 'Ladi Lane Parts Market' ? 8 : 4.2, D.pins[k][1]) }; });
  if (W.ring) { const e = document.createElement('div'); e.className = 'lbl road'; e.textContent = 'Ring Road'; labelsEl.appendChild(e); const p = along(W.ring.pts, W.S0 + 70); labels.push({ e, p: V(p.x, 1, p.z) }); }
  let showLabels = Q.get('labels') !== '0';

  // ---------- cameras ----------
  const orbit = { target: V(-5, 0, 5), r: 210, th: 0.75, ph: 0.92 };
  const eye = { pos: V(), yaw: 0, pitch: 0 };
  let mode = 'orbit', view = 'overview';
  function applyCam() {
    if (mode === 'orbit') {
      const { r, th, ph, target } = orbit;
      camera.position.set(target.x + r * Math.sin(ph) * Math.sin(th), target.y + r * Math.cos(ph), target.z + r * Math.sin(ph) * Math.cos(th));
      camera.lookAt(target); fitShadow(target.x, target.z, Math.min(170, r * 0.75));
    } else {
      camera.position.copy(eye.pos);
      const d = V(Math.cos(eye.pitch) * Math.sin(eye.yaw), Math.sin(eye.pitch), Math.cos(eye.pitch) * Math.cos(eye.yaw));
      camera.lookAt(eye.pos.clone().add(d));
      fitShadow(eye.pos.x + Math.sin(eye.yaw) * 22, eye.pos.z + Math.cos(eye.yaw) * 22, 48);
    }
  }
  function lookFrom(px, py, pz, tx, ty, tz) {
    mode = 'eye'; eye.pos.set(px, py, pz);
    const dx = tx - px, dy = ty - py, dz = tz - pz; eye.yaw = Math.atan2(dx, dz); eye.pitch = Math.atan2(dy, Math.hypot(dx, dz));
    camera.fov = 62; camera.updateProjectionMatrix(); applyCam(); ui();
  }
  function overview() { mode = 'orbit'; Object.assign(orbit, { r: camera.aspect < 0.8 ? 330 : 205, th: 0.75, ph: 0.92 }); orbit.target.set(-5, 0, 5); camera.fov = 55; camera.updateProjectionMatrix(); applyCam(); ui(); }
  const P = D.pins;
  const VIEWS = {
    overview,
    steal: () => lookFrom(P['The steal'][0] + 3.5, 1.62, P['The steal'][1] + 7.5, P['The steal'][0] - 1.5, 1.3, P['The steal'][1]),
    aisle: () => lookFrom(P['The steal'][0] + 18, 1.68, P['The steal'][1] + 8.2, -100, 1.6, 7),
    boss: () => { const a = W.aisles.reduce((a, b) => Math.abs(b[1][0] - b[0][0]) > Math.abs(a[1][0] - a[0][0]) ? b : a); const w = a[0][0] < a[a.length - 1][0] ? a : a.slice().reverse(); const p = along(w, 26); lookFrom(p.x, 1.65, p.z, P["Boss's post"][0], 1.2, P["Boss's post"][1]); },
    tunde: () => {
      const [x, z] = P["Tunde's room"]; let best = null, bd = 1e9;
      W.roads.filter(r => r.k !== 'main').forEach(r => { for (let s = 0; s < length(r.pts); s += 1) { const p = along(r.pts, s); const d = Math.hypot(p.x - x, p.z - z); if (d < bd) { bd = d; best = p; } } });
      lookFrom(best.x + (best.x - x) * 0.4, 1.65, best.z + (best.z - z) * 0.4, x, 2.2, z);
    },
    ring: () => { const p = along(offsetLine(W.ring.pts, -(W.ring.w / 2 + 0.9)), W.S0 + 25); const q = along(W.ring.pts, W.S0 - 40); lookFrom(p.x, 1.68, p.z, q.x, 2.2, q.z - 2); },
  };
  function go(v) { view = v; VIEWS[v](); }

  // pointer input
  const el = renderer.domElement; const ptrs = new Map(); let pinch = null;
  el.addEventListener('pointerdown', e => { el.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY }); });
  el.addEventListener('pointerup', e => { ptrs.delete(e.pointerId); pinch = null; });
  el.addEventListener('pointercancel', e => { ptrs.delete(e.pointerId); pinch = null; });
  el.addEventListener('pointermove', e => {
    if (!ptrs.has(e.pointerId)) return; const prev = ptrs.get(e.pointerId); const dx = e.clientX - prev.x, dy = e.clientY - prev.y; ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (ptrs.size === 1) {
      if (mode === 'orbit') { orbit.th -= dx * 0.005; orbit.ph = Math.max(0.18, Math.min(1.45, orbit.ph - dy * 0.004)); }
      else { eye.yaw -= dx * 0.004; eye.pitch = Math.max(-1.2, Math.min(1.2, eye.pitch + dy * 0.004)); }
    } else if (ptrs.size === 2 && mode === 'orbit') {
      const [a, b] = [...ptrs.values()]; const d = Math.hypot(a.x - b.x, a.y - b.y); const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
      if (pinch) {
        orbit.r = Math.max(12, Math.min(420, orbit.r * pinch.d / d));
        const s = orbit.r * 0.0016, ddx = mx - pinch.mx, ddy = my - pinch.my;
        const rx = Math.cos(orbit.th), rz = -Math.sin(orbit.th), ax = -Math.sin(orbit.th), az = -Math.cos(orbit.th);
        orbit.target.x += -rx * ddx * s + ax * ddy * s; orbit.target.z += -rz * ddx * s + az * ddy * s;
      }
      pinch = { d, mx, my };
    }
    applyCam();
  });
  el.addEventListener('wheel', e => { e.preventDefault(); if (mode === 'orbit') { orbit.r = Math.max(12, Math.min(420, orbit.r * (1 + e.deltaY * 0.001))); applyCam(); } else { camera.fov = Math.max(30, Math.min(80, camera.fov + e.deltaY * 0.03)); camera.updateProjectionMatrix(); } }, { passive: false });
  const keys = {}; addEventListener('keydown', e => keys[e.key.toLowerCase()] = true); addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);
  let walkF = 0;
  const hold = (id, v) => { const b = document.getElementById(id); const on = e => { e.preventDefault(); walkF = v; }, off = () => { walkF = 0; }; b.addEventListener('pointerdown', on); b.addEventListener('pointerup', off); b.addEventListener('pointerleave', off); b.addEventListener('pointercancel', off); };
  hold('fwd', 1); hold('back', -1);

  // ---------- UI ----------
  document.querySelectorAll('[data-view]').forEach(b => b.addEventListener('click', () => go(b.dataset.view)));
  document.querySelectorAll('[data-look]').forEach(b => b.addEventListener('click', () => setLook(b.dataset.look)));
  const tBtn = document.getElementById('time'); tBtn.addEventListener('click', () => setTime(!dusk));
  const lBtn = document.getElementById('lbls'); lBtn.addEventListener('click', () => { showLabels = !showLabels; ui(); });
  function ui() {
    tBtn.textContent = dusk ? 'Day' : 'Dusk';
    lBtn.textContent = showLabels ? 'Hide labels' : 'Labels';
    document.querySelectorAll('[data-look]').forEach(b => b.classList.toggle('on', b.dataset.look === look));
    document.querySelectorAll('[data-view]').forEach(b => b.classList.toggle('on', b.dataset.view === view));
    document.getElementById('walk').hidden = mode !== 'eye';
    document.getElementById('hint').textContent = mode === 'eye' ? 'Drag to look around. Hold ▲ ▼ to walk.' : 'Drag to turn. Pinch or scroll to zoom. Two fingers to move.';
  }
  if (Q.get('ui') === '0') document.body.classList.add('bare');

  // ---------- loop, with a frame-rate guard for phones ----------
  let t0 = performance.now(), acc = 0, frames = 0, slow = 0;
  const fpsEl = document.getElementById('fps');
  const tmp = V();
  function frame(now) {
    const dt = Q.has('shot') ? 0 : Math.min(0.05, (now - t0) / 1000); t0 = now; // screenshots: traffic frozen so A and B match
    movers.forEach(v => {
      v.s = (v.s + v.v * dt) % v.L; const p = along(v.path, v.s);
      v.obj.position.set(p.x, v.bob ? Math.abs(Math.sin(now * 0.004 + v.ph)) * v.bob : 0, p.z);
      v.obj.rotation.y = -Math.atan2(p.dz, p.dx);
    });
    if (mode === 'eye') {
      const f = walkF + (keys['w'] || keys['arrowup'] ? 1 : 0) - (keys['s'] || keys['arrowdown'] ? 1 : 0), sd = (keys['d'] ? 1 : 0) - (keys['a'] ? 1 : 0);
      if (keys['arrowleft']) eye.yaw += dt * 1.5; if (keys['arrowright']) eye.yaw -= dt * 1.5;
      if (f || sd) { eye.pos.x += (Math.sin(eye.yaw) * f - Math.cos(eye.yaw) * sd) * 1.6 * dt; eye.pos.z += (Math.cos(eye.yaw) * f + Math.sin(eye.yaw) * sd) * 1.6 * dt; eye.pos.y = 1.65 + Math.sin(now * 0.012) * 0.025; }
      applyCam();
    }
    if (dusk) post.render(); else { renderer.setRenderTarget(null); renderer.render(scene, camera); }
    const w = innerWidth, h = innerHeight;
    labels.forEach(l => {
      tmp.copy(l.p).project(camera);
      const vis = showLabels && tmp.z < 1 && tmp.z > -1 && Math.abs(tmp.x) < 1.1 && Math.abs(tmp.y) < 1.1 && camera.position.distanceTo(l.p) < (mode === 'eye' ? 60 : 420);
      l.e.style.display = vis ? 'block' : 'none';
      if (vis) l.e.style.transform = `translate(-50%,-100%) translate(${(tmp.x * 0.5 + 0.5) * w}px,${(-tmp.y * 0.5 + 0.5) * h}px)`;
    });
    // if a phone can't hold ~40 fps, drop the resolution a step (never below 1x)
    acc += Math.min(0.05, (performance.now() - (frame.last || now)) / 1000) || dt; frame.last = performance.now(); frames++;
    if (acc > 1) {
      const fps = frames / acc; fpsEl.textContent = Math.round(fps) + ' fps';
      if (fps < 40 && pixelRatio > 1 && !Q.has('shot')) { if (++slow >= 2) { pixelRatio = Math.max(1, pixelRatio - 0.25); renderer.setPixelRatio(pixelRatio); post.resize(); slow = 0; } } else slow = 0;
      acc = 0; frames = 0;
    }
    requestAnimationFrame(frame);
  }
  addEventListener('resize', () => { renderer.setSize(innerWidth, innerHeight); camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); post.resize(); if (mode === 'orbit') overview(); });

  const breakdown = () => { const out = {}; scene.traverse(o => { if (!o.isMesh) return; let g = o; while (g.parent && g.parent !== scene) g = g.parent; const layer = Object.keys(W.groups).find(k => W.groups[k] === g) || 'other'; const k = layer + ':' + (o.userData.key || (o.isInstancedMesh ? 'people' : 'veh')); const n = (o.geometry.index ? o.geometry.index.count : o.geometry.attributes.position.count) / 3 * (o.isInstancedMesh ? o.count : 1); out[k] = (out[k] || 0) + Math.round(n); }); return out; };
  window.GIDI_LOOK = { breakdown, VIEWS, go, setLook, setTime, stats: () => ({ calls: renderer.info.render.calls, triangles: renderer.info.render.triangles, people: W.people.common.length + W.people.grit.length, peopleA: W.people.common.length }) };
  setTime(dusk); setLook(look);
  go(VIEWS[Q.get('view')] ? Q.get('view') : 'overview');
  document.getElementById('loading').remove();
  requestAnimationFrame(frame);
  // headless screenshots: render a few frames, then flag ready
  if (Q.has('shot')) { let n = 0; const tick = () => { if (++n < 6) requestAnimationFrame(tick); else { const s = window.GIDI_LOOK.stats(); document.title = 'READY ' + JSON.stringify(s); } }; requestAnimationFrame(tick); }
})();
