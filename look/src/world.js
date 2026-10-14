// Lays the kit out on the Ladi Lane opening area (the real Gidi map data).
// Three layers: common (both looks), clean (A only) and grit (B only). The toggle just flips layer visibility
// and the grime uniform, so A and B are the same shapes in the same places.
const WORLD = (() => {
  const K = KIT;
  const { V, M, G, Builder, face, prism, flat, ribbon, along, length, offsetLine, distLine, inPoly, centroid, grow, chamfer, edgeOut, sag, shadeHex } = K;
  const { R, pick, rnd } = TEX;

  const WIDTH = { main: 14, street: 7, lane: 3.5, 'market aisle': 4 };
  const ROADC = { main: 0x4b4f55, street: 0x585b60, lane: 0xc08f62, 'market aisle': 0x9c9386 };
  const ROAD_Y = { main: 0.06, street: 0.05, lane: 0.045, 'market aisle': 0.07 };
  const STOREY = 3.1;
  // bright stylized paints, trims, roofs
  const PAINT = [0xf3d9a4, 0xf2a56b, 0x8fcbe6, 0x9fd8a8, 0xf5c95a, 0xf1eee6, 0xeb9f9f, 0xb9a8e3, 0x7fd1c4];
  const TRIM = [0xffffff, 0xfff6e2, 0x2f6fae, 0xd9542f, 0x2f8a5e];
  const ROOFC = [0x9aa7ae, 0x3f86b8, 0xc4573c, 0x3f9a6c, 0x9aa7ae, 0xb7bec2];
  const BARS = [0x262626, 0x2f6a3e, 0x7a2a2a, 0x2c4f7a, 0x262626];
  const DOORS = [0x2f5d8a, 0x8a2f2f, 0x2e6b4a, 0x3a3a3a, 0x6b4a2e];
  const SKIN = [0x5a3622, 0x6e4329, 0x4a2b1b, 0x7c5033, 0x3d2416];
  const TOPS = [0xd7263d, 0x1b998b, 0xf46036, 0x2e294e, 0xf2c14e, 0x5bc0eb, 0x9bc53d, 0xe55934, 0x8e44ad, 0xffffff, 0x0b6e4f, 0xfa7921, 0xc2185b];
  const BOTTOMS = [0x263238, 0x3e2723, 0x1a237e, 0x4e342e, 0x212121, 0x546e7a, 0xd9cfb8];
  const WRAP = [0xe65100, 0x6a1b9a, 0x00838f, 0xad1457, 0xf9a825, 0x2e7d32, 0x1565c0, 0xd7263d];
  const HEADGEAR = [0xf2c14e, 0xd7263d, 0x5bc0eb, 0x8e44ad, 0x1b998b, 0xfa7921, 0xffffff];

  // ---------- every sign, sticker and painted writing (invented names only) ----------
  const PAIRS = [['#1f5fa8', '#ffffff'], ['#f2c21b', '#1a1a1a'], ['#c8322b', '#ffffff'], ['#2d7d46', '#ffffff'], ['#ffffff', '#c8322b'], ['#f08a24', '#1a1a1a'], ['#ffffff', '#1f3f8a']];
  const SHOPS = ["GOD'S GRACE VENTURES", 'BLESSED HANDS\nMOTOR SPARES', 'CHUKS & SONS\nAUTO PARTS', 'NO WEAPON SHALL\nPROSPER ENT.', 'ALHAJI BELLO TYRES',
    'EMEKA ELECTRICALS', 'TRUST IN GOD\nBATTERIES', 'IYA BASIRAT\nPROVISIONS', 'UNIQUE TOUCH\nFASHION HOME', 'OLUWASEUN CHEMIST\n& STORES', 'HOLY GHOST FIRE\nMECHANIC WORKSHOP',
    'AJE BUTTER\nBARBING SALON', 'PHONE REPAIRS\n& ACCESSORIES', 'MIGHTY GRACE\nWELDING WORKS', 'ADUNNI HAIR\nSTUDIO', 'DIVINE FAVOUR\nVULCANISER'];
  const STALLS = ['CHIDI MOTORS\nGENUINE PARTS', 'TOKUNBO PARTS\nNO FAKE', 'BRAKE PADS\n& FILTERS', 'SHOCK ABSORBERS\nNA HERE', 'ALHAJI\nSPARE PARTS', "GOD'S TIME\nAUTO PARTS", 'OKEKE & BROS\nENGINE PARTS', 'OGA NA BOSS\nGEARBOX'];
  const KIOSKS = ['RECHARGE CARD\n& POS HERE', 'PURE WATER\nCOLD MINERALS', 'POS • TRANSFER\nWITHDRAWAL'];
  const SHACKS = ['PURE WATER\nCOLD MINERALS', 'RECHARGE CARD\n& POS HERE', 'PHONE REPAIRS\nCHARGING 100', 'MAMA EKO\nPROVISIONS', 'VULCANISER\n24 HOURS', 'BOLE & FISH\nHOT HOT'];
  const STICKERS = [['WOLE PELU\nCHANGE EH', '#f2d13a', '#111111', '#000000'], ['GOD IS THE\nGREATEST', '#ffffff', '#1f5fa8', '#7fb3e0'], ['NO FOOD FOR\nLAZY MAN', '#111111', '#f2d13a', '#b3221b'],
    ['EXCUSE ME SIR\nNA ME BE THIS', '#ffffff', '#b3221b', '#000000'], ['NO CONDITION\nIS PERMANENT', '#f2d13a', '#1f3f8a', '#000000'], ['FEAR WOMEN\nRESPECT MAMA', '#c8322b', '#ffffff', '#000000']];
  const PAINTS = [['THIS HOUSE IS\nNOT FOR SALE', '#b0201a'], ['THIS HOUSE IS NOT FOR SALE\nBEWARE OF 419', '#b0201a'], ['DO NOT URINATE HERE\nBY ORDER', '#1c1c1c'],
    ['TOKUNBO ENGINE\n0803 412 7781', '#b0201a'], ['BUY & SELL\nCALL 0805 330 1902', '#1f3f8a'], ['POST NO BILL', '#1c1c1c'], ['ALL KINDS OF\nSPARE PARTS', '#b0201a'],
    ['DO NOT URINATE\nHERE!!', '#1c1c1c'], ['NO PARKING\nBY ORDER', '#1f3f8a'], ['GEARBOX & ENGINE\n0816 220 0471', '#b0201a']];
  const POSTERS = [['CRUSADE', '3 NIGHTS OF FIRE', '#c62828', '#fff'], ['VOTE BABA', 'GIDI NEEDS YOU', '#1b5e20', '#ffeb3b'], ['HOLY GHOST', 'NIGHT • FRI', '#1a237e', '#fff'], ['LESSONS', 'POST-UTME • WAEC', '#f9a825', '#000'],
    ['OWAMBE', 'LIVE BAND • SAT', '#6a1b9a', '#fff'], ['RIP', 'CELEBRATION OF LIFE', '#212121', '#fff'], ['CRUSADE', '3 NIGHTS OF FIRE', '#c62828', '#fff'], ['VOTE BABA', 'GIDI NEEDS YOU', '#1b5e20', '#ffeb3b']];
  function signs() {
    TEX.setSeed(55);
    const e = []; const phone = () => '0803 ' + Math.floor(R(100, 999)) + ' ' + Math.floor(R(1000, 9999));
    const sg = (id, text, i, o = {}) => { const [bg, fg] = PAIRS[i % PAIRS.length]; e.push(Object.assign({ kind: 'sign', id, text, bg, fg, shadow: true }, o)); };
    SHOPS.forEach((t, i) => sg('shop' + i, t, i, { phone: phone() }));
    STALLS.forEach((t, i) => sg('stall' + i, t, i + 3, { phone: '0806 ' + Math.floor(R(100, 999)) + ' ' + Math.floor(R(1000, 9999)) }));
    KIOSKS.forEach((t, i) => e.push({ kind: 'sign', id: 'kiosk' + i, text: t, bg: '#ffffff', fg: '#c62828' }));
    SHACKS.forEach((t, i) => e.push({ kind: 'sign', id: 'shack' + i, text: t, bg: '#ffffff', fg: '#c62828' }));
    e.push({ kind: 'sign', id: 'mamaput', text: 'MAMA PUT\nAMALA • EWEDU • GBEGIRI', bg: '#f2d13a', fg: '#b3221b' });
    e.push({ kind: 'sign', id: 'pos', text: 'POS\nTRANSFER • WITHDRAWAL', bg: '#ffffff', fg: '#1565c0' });
    e.push({ kind: 'sign', id: 'danger', text: 'DANGER\n11,000 VOLTS', bg: '#ffffff', fg: '#c62828' });
    e.push({ kind: 'sign', id: 'refuse', text: 'DO NOT DUMP\nREFUSE HERE', bg: '#ffffff', fg: '#1a1a1a' });
    e.push({ kind: 'sign', id: 'busstop', text: 'BUS STOP\nLADI LANE', bg: '#f2d13a', fg: '#111111' });
    STICKERS.forEach(([t, bg, fg, sh], i) => e.push({ kind: 'sticker', id: 'stk' + i, text: t, bg, fg, sh }));
    PAINTS.forEach(([t, c], i) => e.push({ kind: 'paint', id: 'paint' + i, text: t, col: c }));
    e.push({ kind: 'posters', id: 'post0', list: POSTERS.slice(0, 4) }, { kind: 'posters', id: 'post1', list: POSTERS.slice(4, 8) });
    return e;
  }
  // one poster of the eight (they sit four to a cell)
  const posterRect = (uv, i) => { const r = uv('post' + (i < 4 ? 0 : 1)), k = i % 4, w = (r[2] - r[0]) / 4; return [r[0] + k * w, r[1], r[0] + (k + 1) * w, r[3]]; };

  // prebuilt vehicles: { key: geometry }, shared by parked and moving ones
  function vehicleSet(uv) {
    const make = (fn, o) => { const b = new Builder(); fn(b, o); return b.geos(); };
    const stk = (i) => uv('stk' + (i % STICKERS.length));
    const person = (o = {}) => ({ top: o.top || pick(TOPS), bottom: pick(BOTTOMS), skin: pick(SKIN), helmet: o.helmet });
    return {
      danfo: [0, 1, 2, 3, 4, 5].map(i => make(K.danfo, { sticker: stk(i), sticker2: stk(i + 2), load: i % 3 === 0 ? pick([0xc8a96e, 0x3f51b5, 0x8d6e63]) : null })),
      car: [0x8a8f92, 0x2f3d4c, 0xb03a2e, 0xe8e6df, 0x3f6a4a, 0x2a6fb0].map(c => make(K.car, { body: c })),
      keke: [0, 1, 2].map(i => make(K.keke, { sticker: stk(i + 1), canopy: [0x2e7d32, 0x1a1a1a, 0x1f5fa8][i] })),
      okadaRider: [0xb71c1c, 0x111111, 0x1565c0, 0x2e7d32].map((c, i) => make(K.okada, { body: c, rider: person({ top: pick([0xfdd835, 0x1565c0, 0x2e7d32, 0xff6f00]), helmet: pick([0x1b1b1b, 0xc62828, 0xfdd835]) }), passenger: i % 2 ? person() : null })),
      okadaParked: [0xb71c1c, 0x111111, 0x1565c0].map(c => make(K.okada, { body: c, rider: person({ top: pick([0xfdd835, 0x1565c0, 0xff6f00]), helmet: 0x1b1b1b }) })),
    };
  }
  const placeGeos = (b, geos, m) => { for (const k in geos) b.geo(k, geos[k], m); };

  function build(scene, D, mats, uv) {
    TEX.setSeed(20261015);
    const C = new Builder(), A = new Builder(), B = new Builder();
    const groups = { common: new THREE.Group(), clean: new THREE.Group(), grit: new THREE.Group(), dusk: new THREE.Group() };
    Object.values(groups).forEach(g => scene.add(g));
    const people = { common: [], grit: [] };
    const lamps = [], pools = [], aoShapes = [];
    const NEAR = 175; const near = (x, z, r = NEAR) => Math.hypot(x, z) < r;
    const pins = D.pins;
    const veh = vehicleSet(uv);

    // ---------- ground and roads ----------
    C.geo('ground', G.plane, M(0, 0, 0, 0, 900, 900, 1, -Math.PI / 2), 0xd09868);
    const roads = D.lines.map(l => ({ k: l.k, n: l.n, pts: l.p.map(p => [p[0], p[1]]), w: WIDTH[l.k] || 2.5 }));
    const nearRoad = (x, z, pad = 0, skip) => roads.some(r => r !== skip && distLine(x, z, r.pts) < r.w / 2 + pad);
    roads.forEach(r => {
      if (r.k === 'street' || r.k === 'main') ribbon(C, 'ground', r.pts, r.w + 3.2, 0.03, 0xc69468, { extend: 2 });
    });
    roads.forEach(r => ribbon(C, 'ground', r.pts, r.w + (r.k === 'street' ? 0.6 : 0), ROAD_Y[r.k] || 0.04, ROADC[r.k] || 0xc08f62, { extend: r.k === 'main' ? 0 : 3 }));
    const market = D.parcels.find(p => p.k === 'market'); const mpoly = market.p.slice(0, -1);
    flat(C, 'ground', mpoly, 0.045, 0xa89f90);
    const parks = D.parcels.filter(p => p.k === 'motor park').map(p => p.p.slice(0, -1));
    parks.forEach(pp => flat(C, 'ground', pp, 0.05, 0xb08e6a));

    // rail
    (D.rail || []).forEach(pts => {
      ribbon(C, 'ground', pts, 4.2, 0.12, 0x8a8378);
      [-0.72, 0.72].forEach(o => { const l = offsetLine(pts, o); for (let i = 0; i < l.length - 1; i++) { const a = l[i], b = l[i + 1], L = Math.hypot(b[0] - a[0], b[1] - a[1]); C.geo('metal', G.box, M((a[0] + b[0]) / 2, 0.3, (a[1] + b[1]) / 2, -Math.atan2(b[1] - a[1], b[0] - a[0]), L, 0.15, 0.08), 0x7a6a5a); } });
      const L = length(pts); for (let s = 0; s < L; s += 0.8) { const p = along(pts, s); C.geo('paint', G.box, M(p.x, 0.19, p.z, -Math.atan2(p.dz, p.dx), 0.22, 0.12, 2.4), 0x5a4c40); }
    });

    // Ring Road: median kerbs, lane dashes
    const ring = roads.find(r => r.n === 'Ring Road');
    let S0 = 0;
    if (ring) {
      let bd = 1e9; const L = length(ring.pts);
      for (let s = 0; s < L; s += 1) { const p = along(ring.pts, s); const d = Math.hypot(p.x + 26, p.z - 15); if (d < bd) { bd = d; S0 = s; } }
      for (let s = 0; s < L; s += 1.0) { const p = along(ring.pts, s); C.geo('paint', G.box, M(p.x, 0.27, p.z, -Math.atan2(p.dz, p.dx), 0.98, 0.45, 0.5), (Math.floor(s) % 2) ? 0xf0c21f : 0x1a1a1a); }
      [-3.5, 3.5].forEach(o => { const l = offsetLine(ring.pts, o); const Ll = length(l); for (let s = 0; s < Ll; s += 7) { const p = along(l, s); C.geo('ground', G.plane, M(p.x, 0.075, p.z, -Math.atan2(p.dz, p.dx), 3, 0.16, 1, -Math.PI / 2), 0xf2f0ea); } });
      [-6.6, 6.6].forEach(o => ribbon(C, 'ground', offsetLine(ring.pts, o), 0.16, 0.072, 0xf2f0ea));
    }

    // ---------- kerbs (A) and open drains (B) along streets ----------
    roads.filter(r => r.k === 'street' || r.k === 'main').forEach(r => {
      [-1, 1].forEach(side => {
        const off = offsetLine(r.pts, side * (r.w / 2 + 0.75)); const L = length(off); let run = [];
        const flush = () => {
          if (run.length > 2) {
            ribbon(B, 'water', run, 0.55, 0.03, 0x2f3326);
            [-0.36, 0.36].forEach(o => { const lip = offsetLine(run, o); for (let i = 0; i < lip.length - 1; i++) { const a = lip[i], b = lip[i + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]); B.geo('paint', G.box, M((a[0] + b[0]) / 2, 0.11, (a[1] + b[1]) / 2, -Math.atan2(b[1] - a[1], b[0] - a[0]), l + 0.05, 0.22, 0.14), 0xa8a296); } });
            const kerb = offsetLine(run, -side * 0.45);
            for (let i = 0; i < kerb.length - 1; i++) { const a = kerb[i], b = kerb[i + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]); A.geo('paint', G.box, M((a[0] + b[0]) / 2, 0.09, (a[1] + b[1]) / 2, -Math.atan2(b[1] - a[1], b[0] - a[0]), l + 0.02, 0.18, 0.22), 0xe2ded6); }
            ribbon(A, 'ground', run, 1.3, 0.055, 0xd8d2c6); // a tidy paved strip where B has the drain
          }
          run = [];
        };
        for (let s = 0; s <= L; s += 1.2) {
          const p = along(off, s);
          const bad = !near(p.x, p.z) || nearRoad(p.x, p.z, 0.6, r) || inPoly(p.x, p.z, mpoly);
          if (bad) flush(); else run.push([p.x, p.z]);
          if (!bad && rnd() < 0.035) B.geo('paint', G.box, M(p.x, 0.24, p.z, -Math.atan2(p.dz, p.dx), 1.3, 0.12, 1.1), 0xb0aa9e);
        }
        flush();
      });
    });
    // speed bumps (both), puddles and potholes (B)
    roads.filter(r => r.k === 'street').slice(0, 4).forEach((r, i) => {
      const L = length(r.pts); if (L < 30) return;
      const p = along(r.pts, L * (0.3 + 0.2 * i % 0.5)); const ang = -Math.atan2(p.dz, p.dx) + Math.PI / 2;
      for (let k = -3; k <= 3; k++) C.geo('paint', K.rbox(1, 0.14, 0.8, 0.06), M(p.x + Math.cos(-ang) * k, 0.08, p.z + Math.sin(-ang) * k, ang), k % 2 ? 0x1a1a1a : 0xf0c21f);
    });
    for (let i = 0; i < 26; i++) {
      const r = pick(roads.filter(r => r.k !== 'main' && near(r.pts[0][0], r.pts[0][1], 220))); const L = length(r.pts); const p = along(r.pts, R(2, L - 2));
      B.geo(i < 16 ? 'water' : 'ground', G.disc, M(p.x + R(-1.5, 1.5), 0.085, p.z + R(-1.5, 1.5), R(0, 3), R(0.6, 2.2), 1, R(0.4, 1.4)), i < 16 ? 0x3a3b30 : 0x3a332b);
    }

    // ---------- buildings ----------
    const blds = D.bldg.map(b => ({ ...b, poly: b.p.map(p => [p[0], p[1]]) }));
    const houses = blds.filter(b => b.k === 'front' || b.k === 'back' || b.k === 'shed');
    const inAnyBuilding = (x, z, pad, self) => blds.some(b => b !== self && inPoly(x, z, pad ? grow(b.poly, pad) : b.poly));
    const tundeRoom = blds.find(b => inPoly(pins["Tunde's room"][0], pins["Tunde's room"][1], b.poly));
    const flatCandidates = [];
    let shopI = 0;

    function roof(b, poly, H, pal, flatRoof, core) {
      const e0 = Math.hypot(poly[1][0] - poly[0][0], poly[1][1] - poly[0][1]), e1 = Math.hypot(poly[2][0] - poly[1][0], poly[2][1] - poly[1][1]);
      const short = Math.min(e0, e1), long = Math.max(e0, e1);
      if (flatRoof) {
        const oct = chamfer(poly, 0.22);
        prism(C, 'paint', oct, H, H + 0.75, PAINT[pal], PAINT[pal]);
        prism(C, 'paint', grow(oct, -0.18), H, H + 0.75, 0xb8b2a6, 0xb8b2a6, { inward: true });
        prism(C, 'paint', grow(oct, 0.07), H + 0.75, H + 0.9, 0xf4f1ea, 0xf4f1ea);
        prism(C, 'paint', grow(oct, -0.18), H + 0.75, H + 0.9, 0xf4f1ea, 0xf4f1ea, { inward: true });
        flat(C, 'paint', poly, H + 0.03, 0xb8b2a6);
        return 'flat';
      }
      const gp = grow(poly, 0.45);
      const [A1, B1, C1, D1] = e0 >= e1 ? gp : [gp[1], gp[2], gp[3], gp[0]];
      const rise = Math.min(2.2, 0.3 * short), y0 = H - 0.12;
      const hip = core && long / short < 1.7 && rnd() < 0.6;
      const mid = (p, q) => [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2];
      let m1 = mid(A1, D1), m2 = mid(B1, C1);
      if (hip) { const dx = m2[0] - m1[0], dz = m2[1] - m1[1], l = Math.hypot(dx, dz); const k = Math.min(0.45, (short / 2) / l); m1 = [m1[0] + dx * k, m1[1] + dz * k]; m2 = [m2[0] - dx * k, m2[1] - dz * k]; }
      const P = (p, y) => V(p[0], y, p[1]);
      const a = P(A1, y0), bb = P(B1, y0), c = P(C1, y0), d = P(D1, y0), M1 = P(m1, H + rise), M2 = P(m2, H + rise);
      const rc = pick(ROOFC), up = V(0, 1, 0);
      const ridge = Math.hypot(B1[0] - A1[0], B1[1] - A1[1]) / 0.2, slope = Math.hypot(short / 2 + 0.45, rise);
      // the two long slopes; corrugations run down the slope
      const u1 = hip ? Math.hypot(m1[0] - A1[0], m1[1] - A1[1]) / 0.2 : 0;
      b.quad('roof', a, bb, M2, M1, [[0, 0], [ridge, 0], [ridge - u1, slope], [u1, slope]], [shadeHex(rc, 0.92), shadeHex(rc, 0.92), rc, rc], up);
      b.quad('roof', c, d, M1, M2, [[0, 0], [ridge, 0], [ridge - u1, slope], [u1, slope]], [shadeHex(rc, 0.92), shadeHex(rc, 0.92), rc, rc], up);
      if (hip) {
        const sw = Math.hypot(D1[0] - A1[0], D1[1] - A1[1]) / 0.2;
        b.tri('roof', d, a, M1, [0, 0], [sw, 0], [sw / 2, slope], rc, rc, rc, up);
        b.tri('roof', bb, c, M2, [0, 0], [sw, 0], [sw / 2, slope], rc, rc, rc, up);
      } else {
        // gable ends in the wall colour, on the wall line (not the overhang)
        const wc = PAINT[pal];
        const [oA, oB, oC, oD] = e0 >= e1 ? poly : [poly[1], poly[2], poly[3], poly[0]];
        const apex = (p, q) => V((p[0] + q[0]) / 2, H + rise - 0.14, (p[1] + q[1]) / 2);
        [[V(oB[0], H, oB[1]), V(oC[0], H, oC[1]), apex(oB, oC)], [V(oD[0], H, oD[1]), V(oA[0], H, oA[1]), apex(oD, oA)]].forEach(t => {
          b.tri('paint', t[0], t[1], t[2], [0, 0], [1, 0], [0.5, 1], wc, wc, wc); b.tri('paint', t[1], t[0], t[2], [0, 0], [1, 0], [0.5, 1], wc, wc, wc);
        });
      }
      // ridge cap and fascia boards
      const rl = M1.distanceTo(M2);
      if (rl > 0.3) b.geo('roof', G.box, M((M1.x + M2.x) / 2, M1.y + 0.04, (M1.z + M2.z) / 2, -Math.atan2(M2.z - M1.z, M2.x - M1.x), rl + 0.2, 0.12, 0.3), shadeHex(rc, 0.75), { su: 0.01, sv: 0.01 });
      if (core) [[a, bb], [c, d]].forEach(([p, q]) => { const l = p.distanceTo(q); b.geo('paint', G.box, M((p.x + q.x) / 2, p.y - 0.08, (p.z + q.z) / 2, -Math.atan2(q.z - p.z, q.x - p.x), l, 0.18, 0.05), 0xf4f1ea); });
      return { a, bb, M1, M2 };
    }

    houses.forEach((b) => {
      const poly = b.poly, c = centroid(poly), core = !b.ctx;
      const s = b.k === 'shed' ? 1 : b.s, H = s * STOREY;
      const pal = Math.floor(rnd() * PAINT.length), trim = pick(TRIM), bars = pick(BARS), door = pick(DOORS);
      const oct = chamfer(poly, core ? 0.22 : 0.15);
      const wc = PAINT[pal];
      // walls: lighter at the top, darker at the foot (baked occlusion)
      prism(C, 'paint', oct, 0, H, shadeHex(wc, 0.8), wc);
      prism(C, 'paint', grow(oct, 0.05), 0, 0.5, shadeHex(wc, 0.55), shadeHex(wc, 0.6));
      for (let k = 1; k < s; k++) prism(C, 'paint', grow(oct, 0.07), k * STOREY - 0.08, k * STOREY + 0.1, 0xf4f1ea, 0xf4f1ea);
      aoShapes.push({ poly, strength: 0.55, spread: 1.8 });
      const flatRoof = s >= 4 || (s >= 2 && rnd() < 0.55);
      const rf = roof(C, poly, H, pal, flatRoof, core);
      if (flatRoof && core && s >= 2 && b !== tundeRoom && near(c[0], c[1], 120)) flatCandidates.push({ b, H, oct });

      // which face looks onto a street
      let facing = 0, best = 1e9;
      if (core) for (let i = 0; i < 4; i++) {
        const A2 = poly[i], B2 = poly[(i + 1) % 4], mx = (A2[0] + B2[0]) / 2, mz = (A2[1] + B2[1]) / 2;
        const d = Math.min(...roads.filter(r => r.k !== 'lane').map(r => distLine(mx, mz, r.pts) - r.w / 2));
        if (d < best) { best = d; facing = i; }
      }
      b.facing = facing; b.roadDist = best; b.c = c; b.H = H; b.pal = pal;
      const shop = core && b.k === 'front' && best < 9 && rnd() < 0.7;

      // windows, doors, shop fronts
      for (let i = 0; i < 4; i++) {
        const A2 = poly[i], B2 = poly[(i + 1) % 4], len = Math.hypot(B2[0] - A2[0], B2[1] - A2[1]);
        const [nx, nz] = edgeOut(poly, i);
        const F = face((A2[0] + B2[0]) / 2, (A2[1] + B2[1]) / 2, nx, nz);
        const use = len - (core ? 1.2 : 1.6);
        let n = Math.floor(use / (core ? 2.6 : 3.4)); if (n < 1 && use > 1.2) n = 1;
        const us = []; for (let j = 0; j < n; j++) us.push((j - (n - 1) / 2) * use / Math.max(1, n));
        for (let k = 0; k < s; k++) {
          const v = k * STOREY + 1.6;
          us.forEach((u, j) => {
            if (k === 0 && core && i === facing) {
              if (shop && Math.abs(u) < 2.2) return; // the shop front takes the middle
              if (!shop && j === Math.floor((n - 1) / 2)) { K.doorPiece(C, F, u, { trim, door }); return; }
            }
            if (b.k === 'shed' && rnd() < 0.5) return;
            if (core) K.windowPiece(C, F, u, v, { trim, glass: 0x2c3e48, bars: k === 0 || rnd() < 0.5, barCol: bars, louvres: true, lit: rnd() < 0.4 });
            else { C.geo('paint', G.plane, F(u, v, 0.02, 1.15, 1.35), trim); C.geo(rnd() < 0.35 ? 'glassLit' : 'glass', G.plane, F(u, v, 0.04, 0.9, 1.1), 0x2c3e48); }
          });
        }
        if (shop && i === facing) {
          const w = Math.min(len - 1.4, 3.4);
          K.shopPiece(C, F, 0, w, { trim, shutter: pick([0x9aa3a8, 0x2f6fae, 0x2e7d4f, 0xc0c4c6]), open: R(0.55, 0.85) });
          // signboard above the shop
          const sw = Math.min(len - 0.4, 4.2);
          C.geo('paint', G.box, F(0, 2.98, 0.08, sw + 0.14, 0.72, 0.1), 0x3a3a3a);
          C.geo('sign', G.plane, F(0, 2.98, 0.14, sw, 0.62), null, { rect: uv('shop' + (shopI++ % SHOPS.length)) });
          if (rnd() < 0.5) { // corrugated awning on two posts
            const dep = 1.6, aw = Math.min(len, 5);
            C.geo('roof', G.plane, F(0, 2.45, dep / 2 + 0.05, aw, dep, 1, 0, -Math.PI / 2 + 0.22), pick(ROOFC), { su: aw / 0.2, sv: 1 });
            [-1, 1].forEach(sd => C.geo('metal', G.box, F(sd * aw / 2 * 0.95, 1.2, dep, 0.07, 2.4, 0.07), 0x5b4636));
          }
          lamps.push(F(0, 2.75, 0.5).elements.slice(12, 15));
          C.geo('emit', G.sphLo, F(0, 2.72, 0.35, 0.08, 0.08, 0.08), 0xfff1c8);
          // goods out front, more of them in B
          for (let g = 0; g < 4; g++) (g < 2 ? C : B).geo('paint', G.box, F(R(-w / 2, w / 2), 0.25, R(0.5, 1.2), R(0.35, 0.7), R(0.3, 0.7), R(0.35, 0.6), R(-0.2, 0.2)), pick([0xc8a96e, 0x1565c0, 0x3d3d3d, 0xc62828, 0xf9a825, 0x2e7d32]));
        }
      }
      if (!core) return;
      // dressing
      if (flatRoof && rnd() < 0.75) { // water tank on a stand
        const t = [poly[0][0] * 0.62 + c[0] * 0.38, poly[0][1] * 0.62 + c[1] * 0.38];
        C.geo('paint', K.lathe([[0, 0], [0.72, 0], [0.75, 0.1], [0.75, 1.25], [0.62, 1.45], [0.25, 1.55], [0.25, 1.65], [0, 1.65]], 12), M(t[0], H + 1.4, t[1]), pick([0x1d1d1d, 0x1d1d1d, 0x2f6fae]));
        C.geo('metal', G.box, M(t[0], H + 1.36, t[1], 0, 1.7, 0.08, 1.7), 0x5a5a5a);
        [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([u, v]) => C.geo('metal', G.box, M(t[0] + u * 0.78, H + 0.68, t[1] + v * 0.78, 0, 0.07, 1.36, 0.07), 0x4a4a4a));
      }
      if (rnd() < 0.3) { const P = poly[2]; C.geo('paint', new THREE.SphereGeometry(0.45, 10, 5, 0, Math.PI * 2, 0, 0.9), M(P[0] * 0.8 + c[0] * 0.2, H + (flatRoof ? 1.3 : 0.5), P[1] * 0.8 + c[1] * 0.2, R(0, 6), 1, 1, 1, -1.0), 0xeeeeee); }
      if (!flatRoof && rf.a && rnd() < 0.45) for (let k = 0; k < 2 + Math.floor(rnd() * 3); k++) { // old tyres holding the sheets down (B)
        const t = R(0.15, 0.85), u = R(0.3, 0.7); const p = rf.a.clone().lerp(rf.bb, t).lerp(rf.M1.clone().lerp(rf.M2, t), u);
        B.geo('paint', G.tyre, M(p.x, p.y + 0.12, p.z, 0, 0.3, 0.3, 0.3, Math.PI / 2 + 0.3), 0x161616);
      }
      if (b.k !== 'shed' && rnd() < 0.4) { // generator in its cage
        const i = Math.floor(rnd() * 4), A2 = poly[i], B2 = poly[(i + 1) % 4]; const [nx, nz] = edgeOut(poly, i);
        const gx = (A2[0] + B2[0]) / 2 + nx * 1.0, gz = (A2[1] + B2[1]) / 2 + nz * 1.0;
        if (!nearRoad(gx, gz, 0.8) && !inAnyBuilding(gx, gz, 0.2, b)) {
          const ang = -Math.atan2(B2[1] - A2[1], B2[0] - A2[0]);
          C.geo('paint', K.rbox(0.85, 0.6, 0.6, 0.08), M(gx, 0.35, gz, ang), pick([0x2e7d32, 0xc62828, 0xf9a825, 0x37474f]));
          for (let u = -1; u <= 1; u += 0.25) C.geo('metal', G.box, M(gx + Math.cos(ang) * u * 0.6 + Math.sin(ang) * 0.45, 0.55, gz - Math.sin(ang) * u * 0.6 + Math.cos(ang) * 0.45, ang, 0.03, 1.1, 0.03), 0x2a2a2a);
          C.geo('metal', G.box, M(gx, 1.1, gz, ang, 1.25, 0.04, 0.95), 0x2a2a2a);
        }
      }
      // B: an AC unit or washing on a line
      if (s >= 2 && rnd() < 0.35) {
        const i = (facing + 1 + Math.floor(rnd() * 3)) % 4, A2 = poly[i], B2 = poly[(i + 1) % 4]; const [nx, nz] = edgeOut(poly, i);
        const F = face((A2[0] + B2[0]) / 2, (A2[1] + B2[1]) / 2, nx, nz);
        if (rnd() < 0.5) B.geo('paint', K.rbox(0.8, 0.5, 0.45, 0.05), F(R(-1, 1), STOREY + 2.6, 0.25), 0xdedad2);
        else { const y = STOREY + 2.5; B.geo('metal', G.box, F(0, y, 0.35, 3.2, 0.015, 0.015), 0x333333); for (let k = 0; k < 5; k++) B.geo('paint', G.box, F(-1.3 + k * 0.62, y - 0.32, 0.35, 0.5, 0.6, 0.02, R(-0.05, 0.05)), pick(TOPS)); }
      }
    });

    // B: unfinished storeys going up on a few flat roofs: columns, part walls, rods, a scaffold pole
    flatCandidates.filter((x, i) => i % 5 === 1).slice(0, 6).forEach(({ b, H }) => {
      const poly = b.poly, y0 = H + 0.05, top = y0 + STOREY;
      poly.forEach(P => {
        const c = b.c, px = P[0] * 0.94 + c[0] * 0.06, pz = P[1] * 0.94 + c[1] * 0.06;
        B.geo('paint', G.box, M(px, (y0 + top) / 2, pz, 0, 0.32, STOREY, 0.32), 0x9c9890);
        for (let r = 0; r < 4; r++) B.geo('metal', G.cyl6, M(px + (r % 2 ? 0.1 : -0.1), top + 0.7, pz + (r > 1 ? 0.1 : -0.1), 0, 0.016, R(1.0, 1.6), 0.016, R(-0.1, 0.1), R(-0.1, 0.1)), 0x7a4426);
      });
      for (let i = 0; i < 2; i++) { // part-built block walls, stepped
        const A2 = poly[i], B2 = poly[(i + 1) % 4], len = Math.hypot(B2[0] - A2[0], B2[1] - A2[1]); const [nx, nz] = edgeOut(poly, i);
        const F = face((A2[0] + B2[0]) / 2, (A2[1] + B2[1]) / 2, nx, nz);
        const n = Math.floor(len / 0.45);
        for (let k = 0; k < n; k++) { const h = Math.max(0.2, (rnd() < 0.7 ? R(0.8, 2.2) : R(0.2, 0.6))); const course = Math.round(h / 0.225) * 0.225; B.geo('paint', G.box, F(-len / 2 + (k + 0.5) * len / n, y0 + course / 2, -0.12, len / n - 0.02, course, 0.2), shadeHex(0x9a968c, R(0.9, 1.05))); }
      }
      B.geo('paint', G.box, M(b.c[0] + R(-1, 1), y0 + 0.25, b.c[1] + R(-1, 1), R(0, 3), 1.6, 0.5, 1.0), 0x8a857a); // cement bags
      B.geo('paint', G.cyl6, M(poly[2][0], H + 2.0, poly[2][1], 0, 0.06, 7, 0.06, 0.06, 0.05), 0x8a6a44);    // scaffold pole
    });

    // B: painted writing and posters on walls near the street
    const walls = houses.filter(b => b.k !== 'shed' && !b.ctx);
    const writeOn = (b, id, side) => {
      if (!b) return; const i = (b.facing + side) % 4, A2 = b.poly[i], B2 = b.poly[(i + 1) % 4], len = Math.hypot(B2[0] - A2[0], B2[1] - A2[1]); const [nx, nz] = edgeOut(b.poly, i);
      const F = face((A2[0] + B2[0]) / 2, (A2[1] + B2[1]) / 2, nx, nz);
      B.geo('wallPaint', G.plane, F(0, 1.0, 0.03, Math.min(len - 0.6, 4.6), 1.15), null, { rect: uv(id) });
    };
    writeOn(walls.find(b => b.k === 'back' && b.roadDist < 12), 'paint0', 1);
    writeOn(walls.filter(b => b.roadDist < 12)[9], 'paint1', 1);
    writeOn(walls.filter(b => b.roadDist < 12)[16], 'paint2', 3);
    walls.filter(b => b.roadDist < 10).forEach(b => {
      if (rnd() > 0.5) return;
      const f = b.facing, A2 = b.poly[f], B2 = b.poly[(f + 1) % 4], len = Math.hypot(B2[0] - A2[0], B2[1] - A2[1]); const [nx, nz] = edgeOut(b.poly, f);
      const F = face((A2[0] + B2[0]) / 2, (A2[1] + B2[1]) / 2, nx, nz);
      const n = 2 + Math.floor(rnd() * 4);
      for (let k = 0; k < n; k++) B.geo('sign', G.plane, F(R(-0.42, 0.42) * len, R(1.0, 1.5), 0.13 + k * 0.002, 0.55, 0.75, 1, R(-0.06, 0.06)), null, { rect: posterRect(uv, Math.floor(rnd() * 8)) });
    });

    // compound walls with gates; B adds broken bottles on top
    houses.filter(b => b.k !== 'shed' && b !== tundeRoom && !b.ctx).forEach(b => {
      if (rnd() > 0.45) return;
      const fp = grow(b.poly, 2.2);
      for (let i = 0; i < 4; i++) {
        const A2 = fp[i], B2 = fp[(i + 1) % 4], L = Math.hypot(B2[0] - A2[0], B2[1] - A2[1]); const ang = -Math.atan2(B2[1] - A2[1], B2[0] - A2[0]);
        let run = null;
        const flush = () => {
          if (!run) return; const n = run.n, x = (run.x0 + run.x1) / 2, z = (run.z0 + run.z1) / 2;
          C.geo('paint', G.box, M(x, 1.0, z, ang, n + 0.02, 2.0, 0.22), 0xd8ccb4); C.geo('paint', G.box, M(x, 2.05, z, ang, n + 0.04, 0.1, 0.28), 0xf1ece0);
          run = null;
        };
        for (let s = 0; s < L; s += 1.0) {
          const t = (s + 0.5) / L, x = A2[0] + (B2[0] - A2[0]) * t, z = A2[1] + (B2[1] - A2[1]) * t;
          if (nearRoad(x, z, 0.9) || inAnyBuilding(x, z, 0.4, b) || inPoly(x, z, mpoly)) { flush(); continue; }
          const isGate = i === b.facing && Math.abs(t - 0.5) * L < 1.6;
          if (isGate) { flush(); C.geo('metal', G.box, M(x, 1.0, z, ang, 1.02, 2.0, 0.08), 0x2b4a66); }
          else { if (!run) run = { x0: x, z0: z, n: 0 }; run.x1 = x; run.z1 = z; run.n++; const r0 = run; r0.x0 = r0.x0; }
          if (!isGate && rnd() < 0.5) B.geo('glass', G.box, M(x, 2.14, z, ang, 0.8, 0.1, 0.08, 0, R(-0.5, 0.5)), pick([0x2f6b3a, 0x8a6a2a, 0x6f8a8f]));
        }
        flush();
      }
    });

    // ---------- the market ----------
    const aisles = D.aisles.map(a => a.map(p => [p[0], p[1]]));
    const ew = aisles.reduce((a, b) => Math.abs(b[1][0] - b[0][0]) > Math.abs(a[1][0] - a[0][0]) ? b : a);
    const stalls = blds.filter(b => b.k === 'stalls');
    const steal = stalls.find(b => inPoly(pins['The steal'][0], pins['The steal'][1], grow(b.poly, 0.5)));
    stalls.forEach((b, si) => {
      const poly = b.poly;
      aoShapes.push({ poly, strength: 0.3, spread: 0.9 });
      const e0 = Math.hypot(poly[1][0] - poly[0][0], poly[1][1] - poly[0][1]), e1 = Math.hypot(poly[2][0] - poly[1][0], poly[2][1] - poly[1][1]);
      const [A1, B1, C1, D1] = e0 >= e1 ? poly : [poly[1], poly[2], poly[3], poly[0]];
      const dAB = distLine((A1[0] + B1[0]) / 2, (A1[1] + B1[1]) / 2, ew), dCD = distLine((C1[0] + D1[0]) / 2, (C1[1] + D1[1]) / 2, ew);
      const [F1, F2, K1, K2] = dAB < dCD ? [A1, B1, C1, D1] : [C1, D1, A1, B1];
      const ang = -Math.atan2(F2[1] - F1[1], F2[0] - F1[0]);
      const fx = (F1[0] + F2[0]) / 2, fz = (F1[1] + F2[1]) / 2, kx = (K1[0] + K2[0]) / 2, kz = (K1[1] + K2[1]) / 2;
      const len = Math.max(e0, e1), dep = Math.min(e0, e1);
      const ofx = (fx - kx) / dep, ofz = (fz - kz) / dep;
      [F1, F2, K1, K2].forEach((P, i) => C.geo('metal', G.box, M(P[0], i < 2 ? 1.45 : 1.25, P[1], ang, 0.1, i < 2 ? 2.9 : 2.5, 0.1), 0x6b5440));
      // lean-to roof, front higher
      const rf = V(fx + ofx * 0.6, 2.95, fz + ofz * 0.6), rk = V(kx - ofx * 0.3, 2.45, kz - ofz * 0.3);
      const ux = Math.cos(-ang) * (len / 2 + 0.3), uz = Math.sin(-ang) * (len / 2 + 0.3);
      const rc = pick(ROOFC);
      C.quad('roof', V(rf.x - ux, rf.y, rf.z - uz), V(rf.x + ux, rf.y, rf.z + uz), V(rk.x + ux, rk.y, rk.z + uz), V(rk.x - ux, rk.y, rk.z - uz), [[0, 0], [len / 0.2, 0], [len / 0.2, 1], [0, 1]], rc, V(0, 1, 0));
      // back wall of old roofing sheets
      C.geo('roof', G.plane, M(kx, 1.15, kz, ang, len, 2.3, 1), shadeHex(pick(ROOFC), 0.9), { su: len / 0.2, sv: 1 });
      C.geo('roof', G.plane, M(kx, 1.15, kz, ang + Math.PI, len, 2.3, 1), shadeHex(rc, 0.85), { su: len / 0.2, sv: 1 });
      // shelves of stock
      const bx = kx + ofx * 0.35, bz = kz + ofz * 0.35;
      if (b !== steal) for (let sh = 0; sh < 3; sh++) {
        C.geo('paint', G.box, M(bx, 0.7 + sh * 0.55, bz, ang, len * 0.85, 0.04, 0.4), 0x6b5440);
        for (let k = 0; k < len * 1.4; k++) { if (rnd() < 0.3) continue; const t = (k / (len * 1.4) - 0.45) * len * 0.85; C.geo(rnd() < 0.5 ? 'metal' : 'paint', G.box, M(0, 0, 0, 0, R(0.14, 0.4), R(0.12, 0.35), R(0.15, 0.3)).premultiply( M(bx + Math.cos(-ang) * t, 0.85 + sh * 0.55, bz + Math.sin(-ang) * t, ang + R(-0.3, 0.3))), pick([0x2b2b2b, 0x4a4a4a, 0x6d6d6d, 0x8a7a66, 0xb0a89a, 0xf9a825, 0xc62828, 0x1565c0])); }
      }
      // counter
      const cx = fx - ofx * 0.5, cz = fz - ofz * 0.5;
      C.geo('paint', K.rbox(len * 0.9, 0.9, 0.6, 0.06), M(cx, 0.45, cz, ang), pick([0xb08a62, 0x9c7752, 0xc49a6c]));
      if (rnd() < 0.35) { // tarpaulin pulled out over the walkway
        const out = R(1.2, 2.2), tx = fx + ofx * (0.6 + out / 2), tz = fz + ofz * (0.6 + out / 2);
        let a2 = ang; if (Math.sin(a2) * ofx + Math.cos(a2) * ofz < 0) a2 += Math.PI;
        C.geo('tarp', G.plane, M(tx, 2.75, tz, a2, len * R(0.6, 1.0), out, 1, -Math.PI / 2 - 0.12), pick([0x1e6fd0, 0x1e6fd0, 0xf07a1e, 0x2e9d52, 0xe8e8e8]));
        C.geo('metal', G.box, M(tx + ofx * out / 2, 1.35, tz + ofz * out / 2, 0, 0.05, 2.7, 0.05), 0x6b5440);
      }
      if (b === steal) return;
      // goods spill out front (more in B)
      const n = 4 + Math.floor(rnd() * 6);
      for (let k = 0; k < n; k++) {
        const L = k < 4 ? C : B;
        const t = R(-0.45, 0.45) * len, gx = cx + Math.cos(-ang) * t, gz = cz + Math.sin(-ang) * t, kind = rnd(), out = R(0.8, 1.6);
        if (kind < 0.3) { const h = 2 + Math.floor(rnd() * 5); for (let j = 0; j < h; j++) L.geo('paint', G.tyre, M(gx + ofx * out + R(-0.03, 0.03), 0.11 + j * 0.21, gz + ofz * out + R(-0.03, 0.03), 0, 0.3, 0.3, 0.3, Math.PI / 2), 0x161616); }
        else if (kind < 0.45) { for (let j = 0; j < 5; j++) L.geo('paint', G.box, M(gx + j * 0.21 * Math.cos(-ang), 1.04, gz + j * 0.21 * Math.sin(-ang), ang, 0.18, 0.28, 0.12), pick([0xf9a825, 0x2e7d32, 0xc62828, 0x1565c0, 0x212121])); }
        else if (kind < 0.6) L.geo('metal', G.cyl, M(gx + ofx * 0.5, 1.05, gz + ofz * 0.5, ang, 0.05, 2.2, 0.05, 0.3), 0x8d8d8d);
        else if (kind < 0.75) L.geo('metal', K.rbox(R(0.5, 0.8), R(0.4, 0.6), R(0.4, 0.6), 0.06), M(gx + ofx * out, 0.27, gz + ofz * out, ang + R(-0.4, 0.4)), pick([0x5f5f5f, 0x7a6a58, 0x3d3d3d]));
        else if (kind < 0.88) { for (let j = 0; j < 4; j++) L.geo('paint', G.box, M(gx + ofx * out + j * 0.32 * Math.cos(-ang), 0.11, gz + ofz * out + j * 0.32 * Math.sin(-ang), ang, 0.3, 0.22, 0.18), 0x151515); }
        else L.geo('paint', K.rbox(1.6, 0.35, 0.12, 0.05), M(gx + ofx * 0.7, 0.55, gz + ofz * 0.7, ang, 1, 1, 1, 0, 1.2), pick([0xd0d0d0, 0x1d1d1d, 0x8a1c1c, 0x2f3d4c]));
      }
      if (rnd() < 0.7) for (let j = 0; j < 7; j++) C.geo('paint', G.tyre, M(fx + ofx * 0.3 + Math.cos(-ang) * (j - 3) * 0.32, 2.3, fz + ofz * 0.3 + Math.sin(-ang) * (j - 3) * 0.32, ang, R(0.12, 0.2), R(0.12, 0.2), 0.1), pick([0x111111, 0x111111, 0x2e7d32, 0xc62828]));
      if (si % 2 === 0) {
        let a2 = ang; if (Math.sin(a2) * ofx + Math.cos(a2) * ofz < 0) a2 += Math.PI;
        const sw = Math.min(len - 0.3, 3.4);
        C.geo('paint', G.box, M(fx + ofx * 0.47, 2.5, fz + ofz * 0.47, a2, sw + 0.1, 0.9, 0.05), 0x3a3a3a);
        C.geo('sign', G.plane, M(fx + ofx * 0.5, 2.5, fz + ofz * 0.5, a2 + R(-0.03, 0.03), sw, 0.8, 1), null, { rect: uv('stall' + (si / 2 % STALLS.length)) });
      }
      if (si % 5 === 0) { lamps.push([fx + ofx * 0.4, 2.55, fz + ofz * 0.4]); C.geo('emit', G.sphLo, M(fx + ofx * 0.4, 2.55, fz + ofz * 0.4, 0, 0.08, 0.1, 0.08), 0xfff1c8); }
    });
    // push carts
    const pushcart = (x, z, a) => {
      C.geo('paint', K.rbox(2.0, 0.1, 1.0, 0.04), M(x, 0.75, z, a), 0xb08a62);
      [-1, 1].forEach(u => C.geo('paint', G.tyre, M(x + Math.sin(a) * u * 0.55, 0.33, z + Math.cos(a) * u * 0.55, a, 0.28, 0.28, 0.28), 0x1a1a1a));
      C.geo('metal', G.box, M(x - Math.cos(a) * 1.4, 0.85, z + Math.sin(a) * 1.4, a, 0.9, 0.05, 0.05), 0x6b5440);
      for (let i = 0; i < 4; i++) C.geo('paint', G.box, M(x + R(-0.6, 0.6), 0.95, z + R(-0.3, 0.3), a, R(0.3, 0.6), R(0.2, 0.4), R(0.3, 0.5)), pick([0x8d6e63, 0x1565c0, 0x3d3d3d, 0xc8a96e]));
    };
    aisles.forEach(a => { const L = length(a); for (let s = 8; s < L - 8; s += R(14, 26)) { const p = along(a, s); const o = rnd() < 0.5 ? -1.3 : 1.3; if (Math.hypot(p.x - pins['The steal'][0], p.z - pins['The steal'][1]) < 14) continue; pushcart(p.x - p.dz * o, p.z + p.dx * o, -Math.atan2(p.dz, p.dx)); } });

    // the steal: Mama Put's food stall
    if (steal) {
      const [px, pz] = pins['The steal']; const cz2 = pz + 1.5;
      const pot = (x, r, h, c) => { C.geo('metal', K.lathe([[0, 0], [r * 0.85, 0], [r, h * 0.3], [r, h], [r * 1.06, h * 1.02], [0, h * 1.02]], 14), M(x, 0.9, cz2), c); };
      pot(px - 1.4, 0.42, 0.55, 0x2b2b2b); pot(px - 0.4, 0.38, 0.45, 0x9e9e9e); pot(px + 0.4, 0.3, 0.35, 0x8a5a3c);
      C.geo('paint', K.rbox(0.7, 0.5, 0.45, 0.06), M(px + 1.4, 1.15, cz2, 0.1), 0x1565c0);
      for (let i = 0; i < 8; i++) C.geo('paint', K.lathe([[0, 0], [0.09, 0], [0.14, 0.08], [0, 0.08]], 10), M(px + 2.2 + (i % 4) * 0.3, 0.9, cz2 + (i > 3 ? 0.2 : -0.1)), pick([0xe53935, 0xffffff, 0x43a047]));
      C.geo('paint', G.cyl, M(px - 2.3, 0.92, cz2, 0, 0.25, 0.04, 0.25), 0xd7ccc8);
      for (let i = 0; i < 7; i++) C.geo('paint', G.ico, M(px - 2.3 + R(-0.15, 0.15), 0.97, cz2 + R(-0.15, 0.15), R(0, 3), 0.05, 0.04, 0.05), 0x8d3b1f);
      C.geo('paint', K.rbox(2.6, 0.45, 0.35, 0.05), M(px + 0.5, 0.25, pz + 3.7), 0x8d6e63);
      C.geo('paint', K.rbox(1.2, 0.05, 0.6, 0.02), M(px + 0.5, 0.72, pz + 4.4), 0xf5f5f5);
      C.geo('paint', G.box, M(px, 2.45, pz + 2.44, 0, 3.3, 0.95, 0.04), 0x3a3a3a);
      C.geo('sign', G.plane, M(px, 2.45, pz + 2.47, 0, 3.2, 0.85, 1), null, { rect: uv('mamaput') });
      C.geo('sign', G.plane, M(px, 2.45, pz + 2.41, Math.PI, 3.2, 0.85, 1), null, { rect: uv('mamaput') });
      lamps.push([px, 2.6, cz2]); C.geo('emit', G.sphLo, M(px, 2.6, cz2, 0, 0.09, 0.11, 0.09), 0xfff1c8);
    }

    // market perimeter wall: painted panels and a red mud band; B adds painted ads
    const gaps = []; aisles.forEach(a => gaps.push(a[0], a[a.length - 1]));
    let adI = 3; const mc = centroid(mpoly);
    for (let i = 0; i < mpoly.length; i++) {
      const A2 = mpoly[i], B2 = mpoly[(i + 1) % mpoly.length], L = Math.hypot(B2[0] - A2[0], B2[1] - A2[1]), ang = -Math.atan2(B2[1] - A2[1], B2[0] - A2[0]);
      for (let s = 0; s < L; s += 1) {
        const t = (s + 0.5) / L, x = A2[0] + (B2[0] - A2[0]) * t, z = A2[1] + (B2[1] - A2[1]) * t;
        if (gaps.some(g => Math.hypot(g[0] - x, g[1] - z) < 4.5)) continue;
        const panel = Math.floor(s / 7) % 4;
        C.geo('paint', G.box, M(x, 1.2, z, ang, 1.02, 2.4, 0.25), [0xe9dcc0, 0xd9cba9, 0xa9d1c0, 0xf0c98a][panel]);
        C.geo('paint', G.box, M(x, 0.25, z, ang, 1.03, 0.5, 0.27), 0x9a5a36);
        C.geo('paint', G.box, M(x, 2.45, z, ang, 1.04, 0.1, 0.32), 0xf4f1ea);
        if (s % 9 === 4) {
          let a2 = ang; const ox = x - mc[0], oz = z - mc[1]; if (Math.sin(a2) * ox + Math.cos(a2) * oz < 0) a2 += Math.PI;
          B.geo('wallPaint', G.plane, M(x + Math.sin(a2) * 0.14, 1.45, z + Math.cos(a2) * 0.14, a2, 3.2, 0.8, 1), null, { rect: uv('paint' + adI) });
          adI = adI >= 9 ? 3 : adI + 1;
        }
      }
    }

    // ---------- kiosks, umbrellas, the boss's post ----------
    blds.filter(b => b.k === 'kiosk').forEach((b, i) => {
      const c = centroid(b.poly), ang = -Math.atan2(b.poly[1][1] - b.poly[0][1], b.poly[1][0] - b.poly[0][0]);
      C.geo('paint', K.rbox(2.2, 2.3, 1.6, 0.12), M(c[0], 1.15, c[1], ang), pick([0xfdd835, 0x1e88e5, 0xe53935, 0x43a047]));
      C.geo('roof', K.rbox(2.6, 0.1, 2.0, 0.04), M(c[0], 2.38, c[1], ang), 0xb7bec2, { su: 0.01, sv: 0.01 });
      [1, -1].forEach(sd => C.geo('sign', G.plane, M(c[0] + Math.sin(ang) * 0.82 * sd, 1.9, c[1] + Math.cos(ang) * 0.82 * sd, ang + (sd < 0 ? Math.PI : 0), 2.0, 0.52, 1), null, { rect: uv('kiosk' + (i % 3)) }));
      aoShapes.push({ poly: b.poly, strength: 0.3, spread: 0.8 });
    });
    // umbrellas: striped cones built from coloured slices
    const umbrella = (x, z, cs) => {
      const n = 12, r = 1.5, h = 0.55, y = 2.35, a0 = R(0, 6);
      for (let i = 0; i < n; i++) {
        const a = a0 + i / n * Math.PI * 2, b = a0 + (i + 1) / n * Math.PI * 2;
        C.tri('tarp', V(x, y + h, z), V(x + Math.cos(a) * r, y, z + Math.sin(a) * r), V(x + Math.cos(b) * r, y, z + Math.sin(b) * r), [0, 0], [1, 0], [1, 1], cs[i % cs.length], cs[i % cs.length], cs[i % cs.length], V(0, 1, 0));
      }
      C.geo('metal', G.cyl6, M(x, 1.18, z, 0, 0.03, 2.35, 0.03), 0xdddddd);
    };
    const UMB = [[0xe53935, 0xffffff], [0x1e88e5, 0xfdd835], [0x43a047, 0xffffff], [0xfb8c00, 0x3949ab]];
    const chair = (b, x, z, a, col) => {
      b.geo('paint', K.rbox(0.46, 0.06, 0.46, 0.02), M(x, 0.45, z, a), col);
      b.geo('paint', K.rbox(0.46, 0.42, 0.05, 0.02), M(x - Math.sin(a) * 0.22, 0.68, z - Math.cos(a) * 0.22, a, 1, 1, 1, -0.12), col);
      [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([u, v]) => b.geo('paint', G.cyl6, M(x + u * 0.19, 0.22, z + v * 0.19, a, 0.025, 0.45, 0.025), col));
    };
    const bp = pins["Boss's post"];
    {
      const [x, z] = bp;
      [[-2, -2], [2, -2], [2, 2], [-2, 2]].forEach(([u, v]) => C.geo('metal', G.cyl6, M(x + u, 1.3, z + v, 0, 0.04, 2.6, 0.04), 0xcfcfcf));
      for (let i = 0; i < 8; i++) C.geo('tarp', G.plane, M(x - 2.3 + (i + 0.5) * 4.6 / 8, 2.62, z, 0, 4.6 / 8, 4.6, 1, -Math.PI / 2), i % 2 ? 0xffffff : 0x1565c0);
      chair(C, x - 0.5, z + 0.4, Math.PI / 2, 0xeeeeee); chair(C, x + 0.7, z - 0.9, 0.2, 0xd32f2f); chair(C, x + 1.1, z + 1.0, -0.4, 0xd32f2f); chair(C, x - 1.3, z - 0.8, 1.0, 0xeeeeee);
      C.geo('paint', K.rbox(0.9, 0.05, 0.6, 0.02), M(x + 0.2, 0.72, z + 0.1), 0x8d6e63);
      C.geo('paint', K.rbox(0.6, 0.45, 0.4, 0.06), M(x - 1.5, 0.23, z + 1.2), 0xe53935);
      C.geo('paint', G.box, M(x + 0.2, 0.76, z + 0.1, 0, 0.3, 0.02, 0.2), 0xf5f5f5);
      lamps.push([x, 2.5, z]); C.geo('emit', G.sphLo, M(x, 2.5, z, 0, 0.09, 0.11, 0.09), 0xfff1c8);
      umbrella(x + 6, z + 6, UMB[0]); umbrella(x + 9, z - 6, UMB[1]);
      [[x + 6, z + 6], [x + 9, z - 6]].forEach(([ux, uz]) => { C.geo('paint', K.rbox(0.8, 0.75, 0.5, 0.05), M(ux, 0.38, uz), 0xfafafa); chair(C, ux, uz + 0.8, Math.PI, 0x1e88e5); });
      C.geo('sign', G.plane, M(x + 6, 0.62, z + 5.74, Math.PI, 0.78, 0.3, 1), null, { rect: uv('pos') });
    }
    if (ring) for (let i = 0; i < 9; i++) { const p = along(offsetLine(ring.pts, -(ring.w / 2 + 2.8)), S0 - 40 + i * 13 + R(-3, 3)); if (!inAnyBuilding(p.x, p.z, 0.5)) umbrella(p.x, p.z, pick(UMB)); }

    // ---------- poles and wires: tidy in A, a tangle in B ----------
    const poles = [], wiresA = [], wiresB = [];
    roads.filter(r => r.k === 'street' || r.k === 'main').forEach((r, ri) => {
      const side = ri % 2 ? 1 : -1, off = offsetLine(r.pts, side * (r.w / 2 + 1.7)), L = length(off); let prev = null;
      for (let s = 4; s < L; s += 27) {
        const p = along(off, s);
        if (!near(p.x, p.z, 200) || inAnyBuilding(p.x, p.z, 0.4) || nearRoad(p.x, p.z, 0.3) || inPoly(p.x, p.z, mpoly)) { prev = null; continue; }
        const ang = -Math.atan2(p.dz, p.dx) + Math.PI / 2;
        C.geo('paint', G.cyl6, M(p.x, 4.5, p.z, ang, 0.13, 9, 0.13, R(-0.025, 0.025), R(-0.025, 0.025)), 0xa8a49a);
        C.geo('metal', G.box, M(p.x, 8.4, p.z, ang, 1.7, 0.1, 0.1), 0x5d5d5d);
        const tops = [-0.75, 0, 0.75].map(u => V(p.x + Math.cos(-ang) * u, 8.5, p.z + Math.sin(-ang) * u));
        if (prev) tops.forEach((t, i) => { wiresA.push(...sag(prev[i], t, 0.35)); wiresB.push(...sag(prev[i], t, 0.8)); });
        prev = tops; poles.push({ x: p.x, z: p.z, top: tops[1] });
      }
    });
    houses.filter(b => !b.ctx).forEach(b => {
      let bestP = null, bd = 1e9; poles.forEach(p => { const d = Math.hypot(p.x - b.c[0], p.z - b.c[1]); if (d < bd) { bd = d; bestP = p; } });
      if (!bestP || bd > 40) return;
      const corner = b.poly[Math.floor(rnd() * 4)];
      wiresA.push(...sag(bestP.top, V(corner[0], Math.min(b.H, 6.2) - 0.3, corner[1]), 0.4, 6));
      const n = rnd() < 0.5 ? 3 : 2;
      for (let k = 0; k < n; k++) { const cc = b.poly[Math.floor(rnd() * 4)]; wiresB.push(...sag(bestP.top, V(cc[0], Math.min(b.H, 6.2) - 0.3, cc[1]), R(0.6, 1.8), 6)); }
    });
    { // transformer by the market mouth
      const x = bp[0] + 4, z = bp[1] - 14;
      [-0.9, 0.9].forEach(u => C.geo('paint', G.cyl6, M(x + u, 3.75, z, 0, 0.13, 7.5, 0.13), 0xa8a49a));
      C.geo('metal', K.rbox(1.4, 1.1, 0.9, 0.1), M(x, 4.6, z), 0x6d8b7f);
      C.geo('metal', G.box, M(x, 4.0, z, 0, 2.2, 0.12, 1.0), 0x4a4a4a);
      C.geo('sign', G.plane, M(x, 2.4, z + 0.14, 0, 0.8, 0.3, 1), null, { rect: uv('danger') });
      poles.slice(0, 6).forEach(p => { wiresA.push(...sag(V(x, 5.2, z), p.top, 0.4, 8)); wiresB.push(...sag(V(x, 5.2, z), p.top, 1.2, 8)); wiresB.push(...sag(V(x + 0.3, 5.0, z), p.top, 1.6, 8)); });
    }

    // ---------- B: refuse heap and litter ----------
    {
      const x = 62, z = 62;
      B.geo('paint', G.ico1, M(x, 0, z, 0.3, 4.2, 1.2, 3.0), 0x4a3e30);
      for (let i = 0; i < 60; i++) B.geo('paint', G.box, M(x + R(-3.8, 3.8), R(0.2, 1.0), z + R(-2.6, 2.6), R(0, 6), R(0.15, 0.5), R(0.08, 0.3), R(0.15, 0.5)), pick([0x1565c0, 0x111111, 0xffffff, 0xc62828, 0x2e7d32, 0x6d4c41, 0xfdd835]));
      C.geo('metal', G.cyl6, M(x - 5, 1.1, z - 3, 0, 0.04, 2.2, 0.04), 0x444444);
      C.geo('sign', G.plane, M(x - 5, 2.0, z - 2.95, 0, 1.4, 0.5, 1), null, { rect: uv('refuse') });
      // A: the same corner kept clean, with two bins
      [[x - 3.5, z - 2], [x - 2.4, z - 2]].forEach(([bx, bz]) => A.geo('paint', K.lathe([[0, 0], [0.32, 0], [0.36, 0.9], [0.4, 0.95], [0, 0.95]], 10), M(bx, 0, bz), 0x2e7d32));
    }
    const litter = (x, z) => {
      const k = rnd();
      if (k < 0.45) B.geo('paint', G.plane, M(x, 0.09, z, R(0, 6), R(0.12, 0.3), R(0.12, 0.3), 1, -Math.PI / 2), pick([0xffffff, 0xdfe9f2, 0x9ccbe8, 0xf2f2f2])); // sachets, paper
      else if (k < 0.7) B.geo('paint', G.cyl6, M(x, 0.12, z, R(0, 6), 0.05, 0.24, 0.05, Math.PI / 2), pick([0x6fb5d8, 0x2f8a4a, 0xeeeeee, 0x8a5a2a])); // bottles
      else if (k < 0.9) B.geo('paint', G.ico, M(x, 0.12, z, R(0, 6), R(0.12, 0.25), R(0.1, 0.18), R(0.12, 0.25)), pick([0x111111, 0x1e6fd0, 0xd32f2f, 0xffffff])); // nylon bags
      else B.geo('paint', G.box, M(x, 0.1, z, R(0, 6), 0.3, 0.2, 0.25), pick([0xc8a96e, 0xd8cdb8])); // a carton
    };
    roads.filter(r => r.k !== 'main').forEach(r => { const L = length(r.pts); for (let i = 0; i < L / 3; i++) { const side = rnd() < 0.5 ? -1 : 1; const p = along(offsetLine(r.pts, side * (r.w / 2 + R(-0.4, 1.2))), R(0, L)); if (near(p.x, p.z, 150) && !inAnyBuilding(p.x, p.z, 0.1)) litter(p.x, p.z); } });
    aisles.forEach(a => { const L = length(a); for (let s = 0; s < L; s += 0.9) { const p = along(a, s); litter(p.x + R(-2, 2), p.z + R(-2, 2)); } });
    if (ring) { const l = offsetLine(ring.pts, -(ring.w / 2 + 1.5)); for (let i = 0; i < 260; i++) { const p = along(l, S0 + R(-120, 140)); litter(p.x + R(-1.5, 1.5), p.z + R(-1, 1)); } }

    // ---------- billboard, bus stop, street lamps on Ring Road ----------
    if (ring) {
      const p = along(offsetLine(ring.pts, ring.w / 2 + 6), S0 + 35), ang = -Math.atan2(p.dz, p.dx) + Math.PI;
      [-4, 4].forEach(u => C.geo('metal', G.box, M(p.x + Math.cos(-ang) * u, 4.5, p.z + Math.sin(-ang) * u, ang, 0.35, 9, 0.35), 0x5f6b70));
      C.geo('metal', K.rbox(12.4, 4.9, 0.25, 0.08), M(p.x - Math.sin(ang) * 0.15, 10.5, p.z - Math.cos(ang) * 0.15, ang), 0x2f3a40);
      C.geo('sign', G.plane, M(p.x, 10.5, p.z, ang, 12, 4.5, 1), null, { rect: uv('billboard') });
      for (let u = -4.5; u <= 4.5; u += 3) { const q = V(p.x + Math.cos(-ang) * u + Math.sin(ang) * 1.0, 13.2, p.z + Math.sin(-ang) * u + Math.cos(ang) * 1.0); C.geo('emit', G.box, M(q.x, q.y, q.z, ang, 0.5, 0.12, 0.25), 0xfff1c8); lamps.push([q.x, q.y - 0.2, q.z]); }
      const q = along(offsetLine(ring.pts, -(ring.w / 2 + 1.8)), S0 - 25);
      C.geo('metal', G.cyl6, M(q.x, 1.5, q.z, 0, 0.05, 3, 0.05), 0x777777);
      C.geo('sign', G.plane, M(q.x, 2.7, q.z + 0.03, 0, 1.2, 0.6, 1), null, { rect: uv('busstop') });
      C.geo('sign', G.plane, M(q.x, 2.7, q.z - 0.03, Math.PI, 1.2, 0.6, 1), null, { rect: uv('busstop') });
      // street lamps along the median
      const L = length(ring.pts);
      for (let s = 12; s < L; s += 32) {
        const p2 = along(ring.pts, s); if (!near(p2.x, p2.z, 260)) continue; const a = -Math.atan2(p2.dz, p2.dx);
        C.geo('metal', G.cyl6, M(p2.x, 4.5, p2.z, 0, 0.09, 9, 0.09), 0x7d8790);
        [-1, 1].forEach(sd => {
          const hx = p2.x + Math.sin(a) * sd * 2.2, hz = p2.z + Math.cos(a) * sd * 2.2;
          C.geo('metal', G.box, M((p2.x + hx) / 2, 8.9, (p2.z + hz) / 2, a + Math.PI / 2, 2.3, 0.08, 0.08), 0x7d8790);
          C.geo('metal', K.rbox(0.7, 0.16, 0.3, 0.06), M(hx, 8.85, hz, a + Math.PI / 2), 0x5d666e);
          C.geo('emit', G.box, M(hx, 8.76, hz, a + Math.PI / 2, 0.55, 0.03, 0.2), 0xfff1c8);
          lamps.push([hx, 8.6, hz]); pools.push([hx, hz, 7]);
        });
      }
    }

    // ---------- trees ----------
    let trees = 0;
    for (let i = 0; i < 500 && trees < 10; i++) {
      const x = R(-130, 130), z = R(-130, 130);
      if (nearRoad(x, z, 2) || inAnyBuilding(x, z, 2.5) || inPoly(x, z, grow(mpoly, 2))) continue;
      trees++;
      C.geo('paint', K.lathe([[0.32, 0], [0.22, 0.6], [0.18, 3.2], [0, 3.3]], 7), M(x, 0, z), 0x6b4f38);
      for (let k = 0; k < 5; k++) C.geo('leaf', G.ico, M(x + R(-1.4, 1.4), R(3.6, 5.2), z + R(-1.4, 1.4), R(0, 6), R(1.4, 2.2), R(1.1, 1.7), R(1.4, 2.2)), pick([0x3f8f3a, 0x4f9e3e, 0x5aad45]));
      aoShapes.push({ poly: [[x - 2, z - 2], [x + 2, z - 2], [x + 2, z + 2], [x - 2, z + 2]], strength: 0.25, spread: 1.5 });
    }

    // ---------- roadside shacks on the market side of Ring Road ----------
    if (ring) {
      const shack = offsetLine(ring.pts, -(ring.w / 2 + 5.2));
      for (let i = 0; i < 9; i++) {
        const p = along(shack, S0 - 70 + i * 16 + R(-2, 2)); if (inAnyBuilding(p.x, p.z, 1.2) || inPoly(p.x, p.z, grow(mpoly, 1))) continue;
        const ang = -Math.atan2(p.dz, p.dx), a2 = ang + Math.PI;
        C.geo('paint', K.rbox(2.6, 2.4, 2.0, 0.1), M(p.x, 1.2, p.z, ang), pick([0x1e88e5, 0xfdd835, 0xe53935, 0x43a047, 0xf57c00, 0x8e24aa]));
        C.geo('roof', G.box, M(p.x, 2.5, p.z, ang, 3.2, 0.06, 2.8, 0.08), pick(ROOFC), { su: 16, sv: 1 });
        C.geo('sign', G.plane, M(p.x + Math.sin(a2) * 1.02, 2.0, p.z + Math.cos(a2) * 1.02, a2, 2.4, 0.6, 1), null, { rect: uv('shack' + (i % SHACKS.length)) });
        if (rnd() < 0.6) umbrella(p.x + Math.sin(a2) * 2.4 + R(-1, 1), p.z + Math.cos(a2) * 2.4, pick(UMB));
        chair(C, p.x + Math.sin(a2) * 1.6 + 0.8, p.z + Math.cos(a2) * 1.6, a2, pick([0xe0e0e0, 0xd32f2f, 0x1e88e5]));
        aoShapes.push({ poly: [[p.x - 1.4, p.z - 1.2], [p.x + 1.4, p.z - 1.2], [p.x + 1.4, p.z + 1.2], [p.x - 1.4, p.z + 1.2]], strength: 0.35, spread: 1 });
        if (rnd() < 0.5) chair(B, p.x + Math.sin(a2) * 2.2 - 0.6, p.z + Math.cos(a2) * 2.2 + 0.5, R(0, 6), 0xd32f2f);
      }
    }

    // ---------- parked vehicles ----------
    if (ring) {
      const fwd = ring.pts, stop = offsetLine(fwd, -5.2);
      [S0 - 31, S0 - 24, S0 - 17].forEach((s, i) => { const p = along(stop, s); placeGeos(C, veh.danfo[i], M(p.x, 0, p.z, -Math.atan2(p.dz, p.dx) + Math.PI, 1, 1, 1, 0, 0.02)); });
      const op = offsetLine(fwd, -(ring.w / 2 + 1.2));
      for (let i = 0; i < 7; i++) { const p = along(op, S0 - 8 + i * 1.3); placeGeos(C, veh.okadaParked[i % 3], M(p.x, 0, p.z, -Math.atan2(p.dz, p.dx) + Math.PI / 2 + R(-0.2, 0.2))); }
    }
    parks.forEach(pp => {
      const c = centroid(pp), a0 = Math.atan2(pp[1][1] - pp[0][1], pp[1][0] - pp[0][0]);
      for (let r = -1; r <= 1; r += 2) for (let k = -3; k <= 3; k++) {
        if (rnd() < 0.2) continue; const u = k * 2.6, v = r * 7;
        placeGeos(C, pick(veh.danfo), M(c[0] + Math.cos(a0) * u - Math.sin(a0) * v, 0, c[1] + Math.sin(a0) * u + Math.cos(a0) * v, -a0 + Math.PI / 2, 1, 1, 1, 0, R(-0.02, 0.02)));
      }
    });
    // B: a stripped car carcass on blocks by a street
    { const r = roads.filter(r => r.k === 'street' && near(r.pts[0][0], r.pts[0][1], 120))[2]; if (r) { const p = along(offsetLine(r.pts, r.w / 2 + 2.2), 10); const m = M(p.x, 0.12, p.z, -Math.atan2(p.dz, p.dx), 1, 1, 1, 0, 0.04); const g = veh.car[0]; B.geo('paint', g.paint, m, 0x7a6a5a); B.geo('glass', g.glass, m, 0x151515); } }

    // ---------- people ----------
    // A gets the common crowd; B adds the rest (the dense crowd)
    const person = (layer, x, z, a, o = {}) => {
      const woman = o.woman !== undefined ? o.woman : rnd() < 0.5;
      people[layer].push({
        x, z, a, h: o.h || R(1.55, 1.85), woman, skin: pick(SKIN), top: o.top || pick(TOPS), bottom: o.bottom || pick(BOTTOMS), wrap: o.wrap || pick(WRAP),
        print: o.print !== undefined ? o.print : rnd() < 0.5, gele: woman && rnd() < 0.55 ? pick(HEADGEAR) : null, cap: !woman && rnd() < 0.25 ? pick(HEADGEAR) : null, load: o.load || (rnd() < 0.05 ? pick([0xc8a96e, 0x9ccbe8, 0xc62828]) : null),
      });
    };
    const split = (shareA) => rnd() < shareA ? 'common' : 'grit';
    const busy = (x, z) => !inAnyBuilding(x, z, 0.35) && !(steal && Math.hypot(x - pins['The steal'][0], z - pins['The steal'][1]) < 2.5);
    aisles.forEach(a => { const L = length(a); for (let s = 2; s < L - 2; s += R(0.7, 1.8)) { const p = along(a, s); const x = p.x + R(-1.7, 1.7), z = p.z + R(-1.7, 1.7); if (busy(x, z)) person(split(0.35), x, z, rnd() < 0.5 ? -Math.atan2(p.dz, p.dx) + Math.PI / 2 : -Math.atan2(p.dz, p.dx) - Math.PI / 2); } });
    { let n = 0; for (let i = 0; i < 3000 && n < 240; i++) { const x = R(-110, 60), z = R(-45, 60); if (!inPoly(x, z, mpoly) || !busy(x, z)) continue; person(split(0.3), x, z, R(0, 6)); n++; } }
    stalls.forEach(b => { if (b === steal || rnd() < 0.25) return; const c = centroid(b.poly); person('common', c[0] + R(-1, 1), c[1] + R(-0.4, 0.4), R(0, 6)); });
    if (steal) {
      const [px, pz] = pins['The steal'];
      person('common', px - 0.8, pz + 0.7, 0, { woman: true, wrap: 0x6a1b9a, top: 0xffc107, h: 1.66, print: true });
      person('common', px + 0.9, pz + 3.95, Math.PI, { woman: false }); person('common', px - 0.2, pz + 3.95, Math.PI, { woman: true }); person('common', px + 2.6, pz + 2.6, Math.PI * 0.9, { woman: false, top: 0x2e7d32 });
      for (let i = 0; i < 5; i++) person('grit', px + R(-4, 5), pz + R(4.5, 7), R(0, 6));
    }
    person('common', bp[0] - 0.5, bp[1] + 0.4, Math.PI / 2, { top: 0x111111, bottom: 0x111111, woman: false, h: 1.82, print: false });
    person('common', bp[0] + 1.6, bp[1] - 0.4, 2.0, { top: 0xffffff, woman: false });
    person('common', bp[0] + 1.9, bp[1] + 0.9, 2.6, { top: 0xf9a825, woman: false });
    for (let i = 0; i < 26; i++) person(split(0.4), bp[0] + R(-3, 12), bp[1] + R(-9, 9), R(0, 6));
    if (ring) {
      const sideL = offsetLine(ring.pts, -(ring.w / 2 + 2.2));
      for (let i = 0; i < 90; i++) { const p = along(sideL, S0 + R(-90, 110)); if (!inAnyBuilding(p.x, p.z, 0.3)) person(split(0.35), p.x + R(-1, 1), p.z + R(-1, 1), R(0, 6), { load: rnd() < 0.15 ? pick([0xc8a96e, 0x9ccbe8, 0xff7043]) : null }); }
      const sideS = offsetLine(ring.pts, -(ring.w / 2 + 2.6));
      for (let i = 0; i < 34; i++) { const p = along(sideS, S0 - 25 + R(-7, 7)); person(split(0.4), p.x + R(-1.2, 1.2), p.z + R(-1.5, 1.0), R(0, 6)); }
      const north = offsetLine(ring.pts, ring.w / 2 + 2.0);
      for (let i = 0; i < 40; i++) { const p = along(north, S0 + R(-80, 100)); if (!inAnyBuilding(p.x, p.z, 0.3)) person(split(0.3), p.x + R(-0.8, 0.8), p.z + R(-0.8, 0.8), R(0, 6)); }
    }
    roads.filter(r => r.k === 'street').forEach(r => { const L = length(r.pts); for (let i = 0; i < L / 9; i++) { const p = along(offsetLine(r.pts, (rnd() < 0.5 ? -1 : 1) * (r.w / 2 + 0.2)), R(0, L)); if (near(p.x, p.z, 190) && !inAnyBuilding(p.x, p.z, 0.3)) person(split(0.45), p.x, p.z, R(0, 6)); } });

    // ---------- finish ----------
    const shadows = (key) => (['ground', 'water', 'wallPaint'].includes(key) || key === 'emit') ? [false, true] : [true, true];
    C.build(mats, groups.common, shadows); A.build(mats, groups.clean, shadows); B.build(mats, groups.grit, shadows);
    const lineMat = new THREE.LineBasicMaterial({ color: 0x161616 });
    groups.clean.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(wiresA), lineMat));
    groups.grit.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(wiresB), lineMat));
    // dusk light pools under lamps
    const pb = new Builder();
    lamps.forEach(([x, y, z]) => pools.push([x, z, Math.min(6, y * 1.2)]));
    pools.forEach(([x, z, r]) => pb.geo('pool', G.plane, M(x, 0.12, z, 0, r * 2, r * 2, 1, -Math.PI / 2), 0xffb35c));
    pb.build(mats, groups.dusk, () => [false, false]);

    return { groups, people, roads, ring, aisles, pins, parks, S0, lamps, aoShapes, veh, mpoly };
  }

  return { build, signs };
})();
