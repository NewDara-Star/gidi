// The kit: a geometry batcher plus the pieces everything is assembled from
// (bevelled walls, framed windows with burglar bars, corrugated roofs, rounded people and vehicles).
const KIT = (() => {
  const V = (x, y, z) => new THREE.Vector3(x, y, z);
  const WHITE = new THREE.Color(1, 1, 1);
  // colours are written in sRGB hex and converted once to the renderer's linear space
  const _cc = new Map();
  const col = (hex) => { if (hex && hex.isColor) return hex; let c = _cc.get(hex); if (!c) { c = new THREE.Color(hex).convertSRGBToLinear(); _cc.set(hex, c); } return c; };
  const shadeHex = (hex, f) => { const c = new THREE.Color(hex); c.multiplyScalar(f); return c.getHex(); };

  // ---------- batching ----------
  const _prep = new WeakMap();
  function prep(geo) {
    let p = _prep.get(geo); if (p) return p;
    const g = geo.index ? geo.toNonIndexed() : geo;
    if (!g.attributes.normal) g.computeVertexNormals();
    p = { pos: g.attributes.position.array, nor: g.attributes.normal.array, uv: g.attributes.uv ? g.attributes.uv.array : null, col: g.attributes.color ? g.attributes.color.array : null, n: g.attributes.position.count };
    _prep.set(geo, p); return p;
  }
  const _m3 = new THREE.Matrix3();
  class Builder {
    constructor() { this.g = {}; }
    grp(k) { return this.g[k] || (this.g[k] = { pos: [], nor: [], uv: [], col: [] }); }
    // add a geometry transformed by m. o: { shade(x,y,z)->factor, su, sv, rect:[u0,v0,u1,v1] }
    geo(k, geo, m, color, o) {
      const P = prep(geo), G = this.grp(k), e = m.elements; _m3.getNormalMatrix(m); const ne = _m3.elements;
      const c = color == null ? WHITE : col(color);
      const shade = o && o.shade, su = (o && o.su) || 1, sv = (o && o.sv) || 1, rect = o && o.rect;
      for (let i = 0; i < P.n; i++) {
        const x = P.pos[i * 3], y = P.pos[i * 3 + 1], z = P.pos[i * 3 + 2];
        const wx = e[0] * x + e[4] * y + e[8] * z + e[12], wy = e[1] * x + e[5] * y + e[9] * z + e[13], wz = e[2] * x + e[6] * y + e[10] * z + e[14];
        G.pos.push(wx, wy, wz);
        const nx = P.nor[i * 3], ny = P.nor[i * 3 + 1], nz = P.nor[i * 3 + 2];
        const ax = ne[0] * nx + ne[3] * ny + ne[6] * nz, ay = ne[1] * nx + ne[4] * ny + ne[7] * nz, az = ne[2] * nx + ne[5] * ny + ne[8] * nz, l = Math.hypot(ax, ay, az) || 1;
        G.nor.push(ax / l, ay / l, az / l);
        let u = P.uv ? P.uv[i * 2] : 0, v = P.uv ? P.uv[i * 2 + 1] : 0;
        if (rect) { u = rect[0] + (rect[2] - rect[0]) * u; v = rect[1] + (rect[3] - rect[1]) * v; } else { u *= su; v *= sv; }
        G.uv.push(u, v);
        const f = shade ? shade(wx, wy, wz) : 1;
        if (color == null && P.col) G.col.push(P.col[i * 3] * f, P.col[i * 3 + 1] * f, P.col[i * 3 + 2] * f);
        else G.col.push(c.r * f, c.g * f, c.b * f);
      }
    }
    // triangle; colours per vertex (ca, cb, cc may be hex or Color). want: optional normal the face must agree with.
    tri(k, a, b, c, ua, ub, uc, ca, cb, cc, want) {
      let n = new THREE.Vector3().subVectors(b, a).cross(new THREE.Vector3().subVectors(c, a));
      if (want && n.dot(want) < 0) { [b, c] = [c, b]; [ub, uc] = [uc, ub]; [cb, cc] = [cc, cb]; n.negate(); }
      n.normalize();
      const G = this.grp(k);
      [[a, ua, ca], [b, ub, cb], [c, uc, cc]].forEach(([p, uv, cl]) => {
        const C = cl == null ? WHITE : col(cl);
        G.pos.push(p.x, p.y, p.z); G.nor.push(n.x, n.y, n.z); G.uv.push(uv[0], uv[1]); G.col.push(C.r, C.g, C.b);
      });
    }
    // a b c d around the quad; cs is one colour or four
    quad(k, a, b, c, d, uvs, cs, want) {
      const C = Array.isArray(cs) ? cs : [cs, cs, cs, cs];
      const U = uvs || [[0, 0], [1, 0], [1, 1], [0, 1]];
      let w = want || new THREE.Vector3().subVectors(b, a).cross(new THREE.Vector3().subVectors(c, a));
      this.tri(k, a, b, c, U[0], U[1], U[2], C[0], C[1], C[2], w);
      this.tri(k, a, c, d, U[0], U[2], U[3], C[0], C[2], C[3], w);
    }
    // meshes, one per key
    build(materials, parent, shadows) {
      const out = [];
      for (const key in this.g) {
        const G = this.g[key]; if (!G.pos.length) continue;
        const geo = new THREE.BufferGeometry();
        geo.setAttribute('position', new THREE.Float32BufferAttribute(G.pos, 3));
        geo.setAttribute('normal', new THREE.Float32BufferAttribute(G.nor, 3));
        geo.setAttribute('uv', new THREE.Float32BufferAttribute(G.uv, 2));
        geo.setAttribute('color', new THREE.Float32BufferAttribute(G.col, 3));
        geo.computeBoundingSphere();
        const m = new THREE.Mesh(geo, materials(key));
        const sh = shadows ? shadows(key) : [true, true];
        m.castShadow = sh[0]; m.receiveShadow = sh[1]; m.userData.key = key;
        parent.add(m); out.push(m);
      }
      this.g = {};
      return out;
    }
    // { key: BufferGeometry with vertex colours }, for things built once and placed many times (vehicles)
    geos() {
      const out = {};
      for (const key in this.g) {
        const G = this.g[key]; const geo = new THREE.BufferGeometry();
        geo.setAttribute('position', new THREE.Float32BufferAttribute(G.pos, 3));
        geo.setAttribute('normal', new THREE.Float32BufferAttribute(G.nor, 3));
        geo.setAttribute('uv', new THREE.Float32BufferAttribute(G.uv, 2));
        geo.setAttribute('color', new THREE.Float32BufferAttribute(G.col, 3));
        geo.computeBoundingSphere(); out[key] = geo;
      }
      this.g = {};
      return out;
    }
    // one BufferGeometry from everything added (for instancing)
    geometry(key = 'x') {
      const G = this.g[key]; const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(G.pos, 3));
      geo.setAttribute('normal', new THREE.Float32BufferAttribute(G.nor, 3));
      geo.setAttribute('uv', new THREE.Float32BufferAttribute(G.uv, 2));
      geo.computeBoundingSphere(); delete this.g[key];
      return geo;
    }
  }
  function merge(parts) { const b = new Builder(); parts.forEach(([g, m]) => b.geo('x', g, m)); return b.geometry('x'); }

  // ---------- transforms ----------
  const _q = new THREE.Quaternion(), _e = new THREE.Euler();
  const M = (x, y, z, ry = 0, sx = 1, sy = 1, sz = 1, rx = 0, rz = 0) => new THREE.Matrix4().compose(V(x, y, z), _q.setFromEuler(_e.set(rx, ry, rz, 'YXZ')), V(sx, sy, sz));
  // A frame on a wall: u along the wall, v up (absolute y), w out of the wall. (nx, nz) is the outward normal.
  function face(px, pz, nx, nz) {
    const t = V(nz, 0, -nx), up = V(0, 1, 0), n = V(nx, 0, nz);
    const B = new THREE.Matrix4().makeBasis(t, up, n);
    return (u, v, w, sx = 1, sy = 1, sz = 1, rz = 0, rx = 0) => {
      const m = new THREE.Matrix4().compose(V(0, 0, 0), _q.setFromEuler(_e.set(rx, 0, rz, 'XYZ')), V(sx, sy, sz));
      m.premultiply(B); m.setPosition(px + t.x * u + n.x * w, v, pz + t.z * u + n.z * w); return m;
    };
  }

  // ---------- base shapes ----------
  const G = {
    box: new THREE.BoxGeometry(1, 1, 1),
    plane: new THREE.PlaneGeometry(1, 1),
    cyl: new THREE.CylinderGeometry(1, 1, 1, 10),
    cyl6: new THREE.CylinderGeometry(1, 1, 1, 6),
    cone: new THREE.ConeGeometry(1, 1, 8),
    sph: new THREE.SphereGeometry(1, 9, 6),
    sphLo: new THREE.SphereGeometry(1, 6, 4),
    ico: new THREE.IcosahedronGeometry(1, 0),
    ico1: new THREE.IcosahedronGeometry(1, 1),
    tyre: new THREE.TorusGeometry(1, 0.34, 4, 9),
    dome: new THREE.SphereGeometry(1, 9, 3, 0, Math.PI * 2, 0, Math.PI / 2),
    disc: new THREE.CircleGeometry(1, 12).rotateX(-Math.PI / 2),
  };
  // a rounded box (bevelled on every edge), cached by size
  const _rb = new Map();
  function rbox(w, h, d, r) {
    const k = [w, h, d, r].map(v => v.toFixed(2)).join(',');
    let g = _rb.get(k); if (g) return g;
    r = Math.min(r, w / 2 - 0.001, h / 2 - 0.001, d / 2 - 0.001);
    // rounded rectangle in x-y, inset by r so the bevel brings it back to w x h
    const ri = r * 0.5, wi = w / 2 - ri, hi = h / 2 - ri, c = ri * 0.9;
    const sh = new THREE.Shape();
    sh.moveTo(-wi + c, -hi); sh.lineTo(wi - c, -hi); sh.quadraticCurveTo(wi, -hi, wi, -hi + c); sh.lineTo(wi, hi - c); sh.quadraticCurveTo(wi, hi, wi - c, hi);
    sh.lineTo(-wi + c, hi); sh.quadraticCurveTo(-wi, hi, -wi, hi - c); sh.lineTo(-wi, -hi + c); sh.quadraticCurveTo(-wi, -hi, -wi + c, -hi);
    g = new THREE.ExtrudeGeometry(sh, { depth: Math.max(0.001, d - 2 * ri), bevelEnabled: true, bevelThickness: ri, bevelSize: ri, bevelSegments: 1, curveSegments: 2 });
    g.translate(0, 0, -(d - 2 * ri) / 2);
    _rb.set(k, g); return g;
  }
  // a capsule along +y, from y = 0 to y = len (plus the round ends)
  function capsule(r, len, seg = 6, k = 2) {
    const pts = [];
    for (let i = 0; i <= k; i++) { const a = -Math.PI / 2 + (i / k) * Math.PI / 2; pts.push(new THREE.Vector2(Math.max(0.0001, Math.cos(a) * r), Math.sin(a) * r)); }
    for (let i = 0; i <= k; i++) { const a = (i / k) * Math.PI / 2; pts.push(new THREE.Vector2(Math.max(0.0001, Math.cos(a) * r), len + Math.sin(a) * r)); }
    return new THREE.LatheGeometry(pts, seg);
  }
  const lathe = (pts, seg) => new THREE.LatheGeometry(pts.map(p => new THREE.Vector2(Math.max(0.0001, p[0]), p[1])), seg);

  // ---------- polygon helpers ----------
  const centroid = (poly) => { let x = 0, z = 0; poly.forEach(p => { x += p[0]; z += p[1]; }); return [x / poly.length, z / poly.length]; };
  const area = (poly) => { let a = 0; for (let i = 0; i < poly.length; i++) { const p = poly[i], q = poly[(i + 1) % poly.length]; a += p[0] * q[1] - q[0] * p[1]; } return a / 2; };
  // offset a convex polygon outward by d (mitred)
  function grow(poly, d) {
    const s = area(poly) > 0 ? 1 : -1, n = poly.length;
    const nrm = (a, b) => { const dx = b[0] - a[0], dz = b[1] - a[1], l = Math.hypot(dx, dz) || 1; return [s * dz / l, -s * dx / l]; };
    return poly.map((p, i) => {
      const a = nrm(poly[(i - 1 + n) % n], p), b = nrm(p, poly[(i + 1) % n]);
      const k = 1 + a[0] * b[0] + a[1] * b[1];
      return [p[0] + (a[0] + b[0]) / k * d, p[1] + (a[1] + b[1]) / k * d];
    });
  }
  // cut every corner by c: a quad becomes an octagon (the bevelled corner)
  function chamfer(poly, c) {
    const out = [], n = poly.length;
    poly.forEach((p, i) => {
      const a = poly[(i - 1 + n) % n], b = poly[(i + 1) % n];
      const la = Math.hypot(a[0] - p[0], a[1] - p[1]), lb = Math.hypot(b[0] - p[0], b[1] - p[1]);
      const ca = Math.min(c, la * 0.3), cb = Math.min(c, lb * 0.3);
      out.push([p[0] + (a[0] - p[0]) / la * ca, p[1] + (a[1] - p[1]) / la * ca], [p[0] + (b[0] - p[0]) / lb * cb, p[1] + (b[1] - p[1]) / lb * cb]);
    });
    return out;
  }
  // outward unit normal of edge i
  function edgeOut(poly, i) {
    const a = poly[i], b = poly[(i + 1) % poly.length], c = centroid(poly);
    let nx = b[1] - a[1], nz = -(b[0] - a[0]); const l = Math.hypot(nx, nz) || 1; nx /= l; nz /= l;
    if (nx * ((a[0] + b[0]) / 2 - c[0]) + nz * ((a[1] + b[1]) / 2 - c[1]) < 0) { nx = -nx; nz = -nz; }
    return [nx, nz];
  }

  // vertical walls around a convex polygon; colours at the bottom and top; optional top cap; inward = faces point in
  function prism(b, key, pts, y0, y1, cBot, cTop, o = {}) {
    const c = centroid(pts); let u = 0;
    for (let i = 0; i < pts.length; i++) {
      const A = pts[i], B = pts[(i + 1) % pts.length], len = Math.hypot(B[0] - A[0], B[1] - A[1]);
      let [nx, nz] = edgeOut(pts, i); if (o.inward) { nx = -nx; nz = -nz; }
      const us = o.uScale || 1, vs = o.vScale || 1;
      b.quad(key, V(A[0], y0, A[1]), V(B[0], y0, B[1]), V(B[0], y1, B[1]), V(A[0], y1, A[1]),
        [[u / us, y0 / vs], [(u + len) / us, y0 / vs], [(u + len) / us, y1 / vs], [u / us, y1 / vs]], [cBot, cBot, cTop, cTop], V(nx, 0, nz));
      u += len;
    }
    if (o.cap) {
      const up = V(0, 1, 0), C = V(c[0], y1, c[1]);
      for (let i = 0; i < pts.length; i++) { const A = pts[i], B = pts[(i + 1) % pts.length]; b.tri(o.capKey || key, C, V(A[0], y1, A[1]), V(B[0], y1, B[1]), [c[0] / 5, c[1] / 5], [A[0] / 5, A[1] / 5], [B[0] / 5, B[1] / 5], o.capCol || cTop, o.capCol || cTop, o.capCol || cTop, up); }
    }
  }
  // flat polygon (any simple polygon) at height y
  function flat(b, key, pts, y, color, uvs = 5) {
    const shape = new THREE.Shape(pts.map(p => new THREE.Vector2(p[0], -p[1])));
    const g = new THREE.ShapeGeometry(shape); g.rotateX(-Math.PI / 2);
    const uv = g.attributes.uv, pos = g.attributes.position; for (let i = 0; i < uv.count; i++) uv.setXY(i, pos.getX(i) / uvs, pos.getZ(i) / uvs);
    b.geo(key, g, M(0, y, 0), color); g.dispose();
  }
  // a flat ribbon along a polyline (roads, kerbs, drains)
  function ribbon(b, key, pts, w, y, color, o = {}) {
    if (pts.length < 2) return;
    pts = pts.map(p => [p[0], p[1]]);
    if (o.extend) {
      const a = pts[0], b2 = pts[1]; let dx = a[0] - b2[0], dz = a[1] - b2[1], l = Math.hypot(dx, dz) || 1;
      pts[0] = [a[0] + dx / l * o.extend, a[1] + dz / l * o.extend];
      const n = pts.length, c = pts[n - 1], d = pts[n - 2]; dx = c[0] - d[0]; dz = c[1] - d[1]; l = Math.hypot(dx, dz) || 1;
      pts[n - 1] = [c[0] + dx / l * o.extend, c[1] + dz / l * o.extend];
    }
    const L = [], Rr = []; let acc = 0; const vs = [];
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i], a = pts[Math.max(0, i - 1)], q = pts[Math.min(pts.length - 1, i + 1)];
      let tx = q[0] - a[0], tz = q[1] - a[1]; const tl = Math.hypot(tx, tz) || 1; tx /= tl; tz /= tl;
      const nx = -tz, nz = tx; let k = 1;
      if (i > 0 && i < pts.length - 1) { const ux = p[0] - a[0], uz = p[1] - a[1], ul = Math.hypot(ux, uz) || 1; k = Math.min(2.5, 1 / Math.max(0.4, Math.abs((-uz / ul) * nx + (ux / ul) * nz))); }
      if (i > 0) acc += Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
      vs.push(acc / (o.uScale || w));
      L.push(V(p[0] + nx * w / 2 * k, y, p[1] + nz * w / 2 * k)); Rr.push(V(p[0] - nx * w / 2 * k, y, p[1] - nz * w / 2 * k));
    }
    const up = V(0, 1, 0);
    for (let i = 0; i < pts.length - 1; i++) b.quad(key, Rr[i], L[i], L[i + 1], Rr[i + 1], [[0, vs[i]], [1, vs[i]], [1, vs[i + 1]], [0, vs[i + 1]]], color, up);
  }
  // along a polyline
  function along(pts, s) {
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i], b = pts[i + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]);
      if (s <= l) { const t = s / l; return { x: a[0] + (b[0] - a[0]) * t, z: a[1] + (b[1] - a[1]) * t, dx: (b[0] - a[0]) / l, dz: (b[1] - a[1]) / l }; }
      s -= l;
    }
    const a = pts[pts.length - 2], b = pts[pts.length - 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
    return { x: b[0], z: b[1], dx: (b[0] - a[0]) / l, dz: (b[1] - a[1]) / l };
  }
  const length = (pts) => { let s = 0; for (let i = 0; i < pts.length - 1; i++) s += Math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]); return s; };
  function offsetLine(pts, d) {
    return pts.map((p, i) => { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)]; const tx = b[0] - a[0], tz = b[1] - a[1], l = Math.hypot(tx, tz) || 1; return [p[0] - tz / l * d, p[1] + tx / l * d]; });
  }
  function distSeg(px, pz, a, b) { const dx = b[0] - a[0], dz = b[1] - a[1], l2 = dx * dx + dz * dz || 1; let t = ((px - a[0]) * dx + (pz - a[1]) * dz) / l2; t = Math.max(0, Math.min(1, t)); return Math.hypot(px - (a[0] + t * dx), pz - (a[1] + t * dz)); }
  function distLine(px, pz, pts) { let d = 1e9; for (let i = 0; i < pts.length - 1; i++) d = Math.min(d, distSeg(px, pz, pts[i], pts[i + 1])); return d; }
  function inPoly(px, pz, poly) { let ins = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const xi = poly[i][0], zi = poly[i][1], xj = poly[j][0], zj = poly[j][1]; if (((zi > pz) !== (zj > pz)) && (px < (xj - xi) * (pz - zi) / (zj - zi) + xi)) ins = !ins; } return ins; }
  function sag(a, b, s, n = 8) { const out = []; for (let i = 0; i < n; i++) { const f = t => V(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t - s * 4 * t * (1 - t), a.z + (b.z - a.z) * t); out.push(f(i / n), f((i + 1) / n)); } return out; }

  // A burglar-bar grille, unit size (1 x 1, centred), built once: bars are three-sided prisms (no hidden faces).
  const GRILLE = (() => {
    const b = new Builder(), t = 0.035, d = 0.035;
    const bar = (x0, y0, x1, y1) => { // front and two sides of a thin bar from (x0,y0) to (x1,y1)
      const dx = x1 - x0, dy = y1 - y0, l = Math.hypot(dx, dy), nx = -dy / l * t / 2, ny = dx / l * t / 2;
      const p = (x, y, z) => V(x, y, z);
      const a = p(x0 + nx, y0 + ny, d), bb = p(x1 + nx, y1 + ny, d), c = p(x1 - nx, y1 - ny, d), e = p(x0 - nx, y0 - ny, d);
      b.quad('x', e, c, bb, a, null, null, V(0, 0, 1));
      b.quad('x', p(x0 + nx, y0 + ny, 0), p(x1 + nx, y1 + ny, 0), bb, a, null, null, V(nx, ny, 0));
      b.quad('x', p(x0 - nx, y0 - ny, 0), p(x1 - nx, y1 - ny, 0), c, e, null, null, V(-nx, -ny, 0));
    };
    for (let i = 0; i < 5; i++) { const x = -0.5 + (i + 0.5) / 5; bar(x, -0.52, x, 0.52); }
    [-1 / 3, 0, 1 / 3].forEach(y => bar(-0.56, y, 0.56, y));
    const r = 0.13; bar(-r, 0, 0, r); bar(0, r, r, 0); bar(r, 0, 0, -r); bar(0, -r, -r, 0); // the diamond in the middle
    bar(-0.56, 0.52, 0.56, 0.52); bar(-0.56, -0.52, 0.56, -0.52);
    return b.geometry('x');
  })();
  // naco louvre blades, unit size: five tilted strips
  const LOUVRE = (() => {
    const b = new Builder();
    for (let i = 0; i < 5; i++) { const y = -0.5 + (i + 0.5) / 5; b.quad('x', V(-0.49, y - 0.07, 0.045), V(0.49, y - 0.07, 0.045), V(0.49, y + 0.07, 0), V(-0.49, y + 0.07, 0), null, null, V(0, 0.5, 1)); }
    return b.geometry('x');
  })();

  // ---------- architectural pieces ----------
  // A window: frame, glass, naco louvre blades, sill, and (optionally) burglar bars. F is a wall frame.
  function windowPiece(b, F, u, v, o) {
    const w = o.w || 1.0, h = o.h || 1.2;
    b.geo('paint', G.box, F(u, v, 0.03, w + 0.2, h + 0.2, 0.12), o.trim);              // frame
    b.geo(o.lit ? 'glassLit' : 'glass', G.plane, F(u, v, 0.095, w, h), o.glass);       // glass
    if (o.louvres) b.geo('glass', LOUVRE, F(u, v, 0.1, w, h, 1), 0x9fb4bd);
    b.geo('paint', G.box, F(u, v - h / 2 - 0.13, 0.1, w + 0.4, 0.08, 0.24), o.trim);    // sill
    b.geo('paint', G.box, F(u, v + h / 2 + 0.14, 0.06, w + 0.36, 0.1, 0.16), o.trim);   // lintel
    if (o.bars) b.geo('metal', GRILLE, F(u, v, 0.16, w + 0.04, h + 0.04, 1), o.barCol);
  }
  // a door: frame and a panelled steel door
  function doorPiece(b, F, u, o) {
    b.geo('paint', G.box, F(u, 1.12, 0.03, 1.15, 2.35, 0.12), o.trim);
    b.geo('metal', G.box, F(u, 1.05, 0.07, 0.95, 2.1, 0.06), o.door);
    [0.6, 1.5].forEach(y => b.geo('metal', G.box, F(u, y, 0.1, 0.7, 0.6, 0.03), shadeHex(o.door, 0.82)));
    b.geo('metal', G.box, F(u + 0.33, 1.05, 0.12, 0.05, 0.12, 0.04), 0xd8c070);
  }
  // shop front: dark opening with a half-raised rolling shutter
  function shopPiece(b, F, u, w, o) {
    b.geo('glass', G.plane, F(u, 1.25, 0.02, w, 2.5), 0x241c16);
    b.geo('paint', G.box, F(u, 2.56, 0.03, w + 0.2, 0.14, 0.14), o.trim);
    [-1, 1].forEach(s => b.geo('paint', G.box, F(u + s * (w / 2 + 0.05), 1.25, 0.03, 0.14, 2.5, 0.14), o.trim));
    const up = o.open == null ? 0.6 : o.open; const sh = 2.4 * (1 - up);
    b.geo('shutter', G.plane, F(u, 2.5 - sh / 2, 0.06, w - 0.05, sh), o.shutter, { su: 1, sv: sh / 0.12 });
    b.geo('metal', G.cyl, F(u, 2.45, 0.12, 0.13, w, 0.13, Math.PI / 2), shadeHex(o.shutter, 0.8));
  }

  // ---------- people ----------
  // Unit person, 1.7 m, facing +z, made of parts; each part is one instanced mesh with its own colour per person.
  const PEOPLE = (() => {
    const sk = [], top = [], trousers = [], wrapper = [], dark = [], gele = [], cap = [], load = [];
    sk.push([new THREE.SphereGeometry(1, 8, 5), M(0, 1.6, 0.0, 0, 0.118, 0.135, 0.124)]);
    sk.push([G.cyl6, M(0, 1.47, 0, 0, 0.05, 0.12, 0.05)]);
    sk.push([G.ico, M(0, 1.6, 0.11, 0, 0.028, 0.034, 0.03)]); // nose
    [-1, 1].forEach(s => {
      sk.push([capsule(0.046, 0.24, 5, 1), M(s * 0.245, 0.86, 0.02, 0, 1, 1, 1, -0.08, s * 0.06)]);   // forearm
      sk.push([G.ico, M(s * 0.25, 0.83, 0.03, 0, 0.055, 0.06, 0.05)]);                                // hand
    });
    top.push([lathe([[0, 0.8], [0.16, 0.82], [0.175, 0.95], [0.185, 1.12], [0.205, 1.28], [0.19, 1.37], [0.11, 1.44], [0, 1.45]], 7), M(0, 0, 0, 0, 1, 1, 0.66)]);
    [-1, 1].forEach(s => top.push([capsule(0.064, 0.2, 4, 1), M(s * 0.225, 1.1, 0, 0, 1, 1, 1, 0, s * 0.1)]));  // sleeves
    [-1, 1].forEach(s => trousers.push([capsule(0.078, 0.74, 5, 1), M(s * 0.088, 0.1, 0, 0, 1, 1, 1, 0, s * 0.02)]));
    trousers.push([lathe([[0, 0.78], [0.17, 0.79], [0.17, 0.88], [0, 0.89]], 7), M(0, 0, 0, 0, 1, 1, 0.7)]);
    wrapper.push([lathe([[0, 0.08], [0.2, 0.09], [0.215, 0.35], [0.2, 0.65], [0.18, 0.86], [0, 0.88]], 7), M(0, 0, 0, 0, 1, 1, 0.74)]);
    dark.push([G.dome, M(0, 1.625, -0.005, 0, 0.126, 0.13, 0.13)]);
    [-1, 1].forEach(s => dark.push([G.ico, M(s * 0.088, 0.045, 0.04, 0, 0.065, 0.05, 0.12)]));
    gele.push([G.ico1, M(0, 1.74, -0.01, 0, 0.17, 0.11, 0.16)]);
    gele.push([G.ico, M(0, 1.8, -0.07, 0, 0.16, 0.11, 0.05, -0.4)]);
    cap.push([lathe([[0, 1.7], [0.122, 1.7], [0.13, 1.76], [0.1, 1.84], [0, 1.85]], 8), M(0.0, 0, 0, 0, 1, 1, 1, 0, 0.12)]);
    load.push([lathe([[0, 1.76], [0.26, 1.77], [0.33, 1.9], [0.31, 1.91], [0.24, 1.8], [0, 1.8]], 10), M(0, 0, 0)]);
    load.push([G.ico1, M(0, 1.9, 0, 0, 0.26, 0.12, 0.26)]);
    const g = (l) => merge(l);
    return { skin: g(sk), top: g(top), trousers: g(trousers), wrapper: g(wrapper), dark: g(dark), gele: g(gele), cap: g(cap), load: g(load) };
  })();

  // A seated rider, merged into a vehicle (x forward).
  function rider(b, x, y, z, o) {
    const m = (px, py, pz, sx, sy, sz, rx = 0, rz = 0, ry = 0) => M(x + px, y + py, z + pz, ry, sx, sy, sz, rx, rz);
    b.geo('paint', PEOPLE.top, m(-0.05, -0.75, 0, 1, 1, 1, 0.2, 0, Math.PI / 2), o.top);                    // torso leaning forward
    b.geo('paint', G.sph, m(0.27, 0.86, 0, 0.118, 0.135, 0.124), o.skin);                                    // head
    b.geo('paint', G.sph, m(0.25, 0.9, 0, 0.155, 0.14, 0.15), o.helmet || 0x1b1b1b);                        // helmet or hair
    [-1, 1].forEach(s => {
      b.geo('paint', capsule(0.078, 0.42, 6), m(0, 0.02, s * 0.1, 1, 1, 1, 0, -Math.PI / 2 + 0.1), o.bottom); // thigh
      b.geo('paint', capsule(0.066, 0.55, 6), m(0.45, -0.58, s * 0.13, 1, 1, 1, 0, 0.15), o.bottom);        // shin
      b.geo('paint', capsule(0.05, 0.5, 6), m(0.68, 0.2, s * 0.2, 1, 1, 1, 0, 0.98), o.top);                // arm to the handlebar
    });
  }

  // ---------- vehicles (x forward, built at the origin) ----------
  function wheel(b, x, z, r, w) {
    b.geo('paint', G.cyl, M(x, r, z, 0, r, w, r, Math.PI / 2), 0x1d1d1d);
    b.geo('metal', G.cyl, M(x, r, z + Math.sign(z) * 0.02, 0, r * 0.5, w, r * 0.5, Math.PI / 2), 0xb8bcc0);
  }
  function extrude(shape, depth, bevel) {
    const g = new THREE.ExtrudeGeometry(shape, { depth: depth - 2 * bevel, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel * 0.8, bevelSegments: 2, curveSegments: 4 });
    g.translate(0, 0, -(depth - 2 * bevel) / 2); return g;
  }
  // Danfo-style bus, an original shape: flat back, high round roof, short sloping snout, wheel arches.
  const DANFO_BODY = (() => {
    const s = new THREE.Shape();
    s.moveTo(-2.2, 0.36); s.lineTo(-1.98, 0.36); s.absarc(-1.55, 0.36, 0.43, Math.PI, 0, true);
    s.lineTo(1.12, 0.36); s.absarc(1.55, 0.36, 0.43, Math.PI, 0, true); s.lineTo(2.25, 0.36);
    s.quadraticCurveTo(2.42, 0.38, 2.42, 0.62); s.lineTo(2.4, 1.0); s.quadraticCurveTo(2.36, 1.18, 2.0, 1.26);
    s.quadraticCurveTo(1.72, 1.5, 1.5, 2.0); s.quadraticCurveTo(1.42, 2.14, 1.2, 2.15);
    s.lineTo(-2.0, 2.15); s.quadraticCurveTo(-2.36, 2.15, -2.38, 1.85); s.lineTo(-2.38, 0.6); s.quadraticCurveTo(-2.38, 0.36, -2.2, 0.36);
    return extrude(s, 1.86, 0.12);
  })();
  const DANFO_GLASS = (() => {
    const s = new THREE.Shape();
    s.moveTo(-2.12, 1.38); s.lineTo(1.25, 1.38); s.lineTo(1.6, 1.38); s.quadraticCurveTo(1.5, 1.7, 1.35, 1.98); s.lineTo(-2.0, 1.98); s.quadraticCurveTo(-2.12, 1.98, -2.12, 1.86); s.closePath();
    const g = new THREE.ExtrudeGeometry(s, { depth: 1.9, bevelEnabled: false, curveSegments: 4 }); g.translate(0, 0, -0.95); return g;
  })();
  function danfo(b, o) {
    const body = o.body || 0xf4c21b;
    b.geo('paint', DANFO_BODY, M(0, 0, 0), body);
    b.geo('glass', DANFO_GLASS, M(0, 0, 0), 0x22313a);
    b.geo('glass', G.box, M(1.62, 1.62, 0, 0, 0.05, 0.62, 1.62, 0, -0.62), 0x22313a);   // windscreen
    b.geo('glass', G.box, M(-2.4, 1.66, 0, 0, 0.04, 0.5, 1.5), 0x22313a);              // back window
    [-1.25, -0.4, 0.45].forEach(x => b.geo('paint', G.box, M(x, 1.68, 0, 0, 0.1, 0.62, 1.92), body)); // pillars
    [0.98, 1.14].forEach(y => b.geo('paint', G.box, M(0, y, 0, 0, 4.5, 0.07, 1.9), 0x161616));      // the black bands
    b.geo('paint', G.box, M(0.4, 0.95, -0.94, 0, 0.92, 1.2, 0.02), 0x2a2a2a);                     // sliding door line
    b.geo('paint', rbox(0.3, 0.26, 1.9, 0.08), M(2.42, 0.5, 0), 0x202020);                         // bumpers
    b.geo('paint', rbox(0.25, 0.24, 1.9, 0.08), M(-2.42, 0.48, 0), 0x202020);
    [-0.66, 0.66].forEach(z => { b.geo('emit', G.sphLo, M(2.42, 0.86, z, 0, 0.05, 0.11, 0.13), 0xfff4d6); b.geo('emitRed', G.box, M(-2.44, 1.0, z * 1.1, 0, 0.03, 0.2, 0.12), 0xd02020); });
    [-1.55, 1.55].forEach(x => [-0.82, 0.82].forEach(z => wheel(b, x, z, 0.36, 0.26)));
    b.geo('metal', G.box, M(-0.5, 2.3, 0.72, 0, 3.0, 0.05, 0.05), 0x2a2a2a); b.geo('metal', G.box, M(-0.5, 2.3, -0.72, 0, 3.0, 0.05, 0.05), 0x2a2a2a);
    for (let x = -1.9; x <= 0.9; x += 0.7) b.geo('metal', G.box, M(x, 2.27, 0, 0, 0.05, 0.12, 1.5), 0x2a2a2a);
    if (o.load) b.geo('paint', rbox(1.6, 0.45, 1.2, 0.15), M(-0.7, 2.55, 0, 0.05), o.load);
    if (o.sticker) {
      b.geo('sign', G.plane, M(-2.47, 1.66, 0, -Math.PI / 2, 1.4, 0.44, 1), null, { rect: o.sticker });
      b.geo('sign', G.plane, M(-1.0, 0.72, 0.945, 0, 1.2, 0.36, 1), null, { rect: o.sticker2 || o.sticker });
    }
  }
  function okada(b, o) {
    [-0.68, 0.68].forEach(x => {
      b.geo('paint', G.tyre, M(x, 0.33, 0, 0, 0.26, 0.26, 0.26), 0x161616);
      b.geo('metal', G.cyl, M(x, 0.33, 0, 0, 0.08, 0.12, 0.08, Math.PI / 2), 0xb0b0b0);
    });
    b.geo('paint', G.sph, M(0.28, 0.86, 0, 0, 0.32, 0.15, 0.17), o.body);                     // tank
    b.geo('paint', capsule(0.13, 0.62, 7), M(-0.62, 0.84, 0, 0, 1, 1, 1, 0, -Math.PI / 2), 0x1a1a1a);   // seat
    b.geo('metal', rbox(0.45, 0.32, 0.26, 0.06), M(0.02, 0.5, 0), 0x6a6a6a);                   // engine
    b.geo('metal', G.box, M(0.62, 0.72, 0, 0, 0.05, 0.85, 0.05, 0, 0.35), 0x8a8a8a);           // fork
    b.geo('metal', G.box, M(0.5, 1.12, 0, 0, 0.05, 0.05, 0.74), 0x2a2a2a);                     // handlebar
    b.geo('emit', G.sphLo, M(0.7, 1.0, 0, 0, 0.06, 0.09, 0.09), 0xfff4d6);
    b.geo('paint', rbox(0.5, 0.1, 0.3, 0.04), M(-0.9, 0.86, 0), 0x2a2a2a);                     // rack
    b.geo('metal', G.cyl, M(-0.35, 0.42, 0.17, 0, 0.045, 0.75, 0.045, 0, Math.PI / 2 - 0.12), 0xc8c8c8); // exhaust
    if (o.rider) rider(b, -0.2, 0.92, 0, o.rider);
    if (o.passenger) rider(b, -0.68, 0.98, 0, o.passenger);
  }
  const KEKE_BODY = (() => {
    const s = new THREE.Shape();
    s.moveTo(-1.15, 0.3); s.lineTo(0.9, 0.3); s.quadraticCurveTo(1.35, 0.3, 1.38, 0.75); s.quadraticCurveTo(1.4, 1.05, 1.18, 1.12);
    s.lineTo(0.75, 1.12); s.lineTo(0.55, 0.7); s.lineTo(-1.15, 0.7); s.quadraticCurveTo(-1.25, 0.7, -1.25, 0.6); s.lineTo(-1.25, 0.4); s.quadraticCurveTo(-1.25, 0.3, -1.15, 0.3);
    return extrude(s, 1.25, 0.08);
  })();
  function keke(b, o) {
    const body = o.body || 0xf2c21b;
    b.geo('paint', KEKE_BODY, M(0, 0, 0), body);
    b.geo('paint', rbox(2.2, 0.16, 1.36, 0.07), M(-0.1, 1.92, 0), o.canopy || 0x2e7d32);   // canopy
    b.geo('paint', rbox(0.1, 0.9, 1.32, 0.04), M(-1.2, 1.4, 0), o.canopy || 0x2e7d32);     // back panel
    [[-1.12, -0.6], [-1.12, 0.6], [0.9, -0.55], [0.9, 0.55]].forEach(([x, z]) => b.geo('metal', G.box, M(x, 1.42, z, 0, 0.05, 1.0, 0.05), 0x1a1a1a));
    b.geo('glass', G.box, M(1.0, 1.5, 0, 0, 0.03, 0.72, 1.06, 0, -0.18), 0x2b3a44);
    b.geo('paint', rbox(1.1, 0.12, 1.0, 0.05), M(-0.45, 0.82, 0), 0x2a2a2a);
    b.geo('emit', G.sphLo, M(1.38, 0.95, 0, 0, 0.05, 0.08, 0.08), 0xfff4d6);
    wheel(b, 1.05, 0, 0.25, 0.14); wheel(b, -0.8, 0.6, 0.25, 0.14); wheel(b, -0.8, -0.6, 0.25, 0.14);
    if (o.sticker) b.geo('sign', G.plane, M(-1.26, 1.4, 0, -Math.PI / 2, 1.0, 0.31, 1), null, { rect: o.sticker });
  }
  const CAR_BODY = (() => {
    const s = new THREE.Shape();
    s.moveTo(-2.05, 0.3); s.lineTo(-1.7, 0.3); s.absarc(-1.35, 0.3, 0.36, Math.PI, 0, true); s.lineTo(1.0, 0.3); s.absarc(1.35, 0.3, 0.36, Math.PI, 0, true);
    s.lineTo(2.05, 0.3); s.quadraticCurveTo(2.25, 0.32, 2.25, 0.62); s.quadraticCurveTo(2.2, 0.86, 1.6, 0.9); s.lineTo(0.95, 0.94);
    s.quadraticCurveTo(0.7, 1.32, 0.3, 1.36); s.lineTo(-0.85, 1.36); s.quadraticCurveTo(-1.3, 1.32, -1.6, 0.96); s.lineTo(-2.0, 0.92);
    s.quadraticCurveTo(-2.25, 0.9, -2.25, 0.62); s.quadraticCurveTo(-2.25, 0.3, -2.05, 0.3);
    return extrude(s, 1.72, 0.12);
  })();
  const CAR_GLASS = (() => {
    const s = new THREE.Shape();
    s.moveTo(0.82, 0.98); s.quadraticCurveTo(0.62, 1.26, 0.28, 1.29); s.lineTo(-0.82, 1.29); s.quadraticCurveTo(-1.2, 1.26, -1.45, 0.98); s.closePath();
    const g = new THREE.ExtrudeGeometry(s, { depth: 1.66, bevelEnabled: false, curveSegments: 4 }); g.translate(0, 0, -0.83); return g;
  })();
  function car(b, o) {
    b.geo('paint', CAR_BODY, M(0, 0, 0), o.body);
    b.geo('glass', CAR_GLASS, M(0, 0, 0), 0x1f2a31);
    b.geo('glass', G.box, M(0.84, 1.13, 0, 0, 0.04, 0.45, 1.4, 0, -0.95), 0x1f2a31);
    b.geo('glass', G.box, M(-1.5, 1.13, 0, 0, 0.04, 0.42, 1.4, 0, 0.8), 0x1f2a31);
    b.geo('paint', G.box, M(-0.25, 1.13, 0, 0, 0.08, 0.34, 1.7), o.body);
    [-1.35, 1.35].forEach(x => [-0.78, 0.78].forEach(z => wheel(b, x, z, 0.33, 0.22)));
    [-0.6, 0.6].forEach(z => { b.geo('emit', G.sphLo, M(2.22, 0.66, z, 0, 0.04, 0.08, 0.16), 0xfff4d6); b.geo('emitRed', G.box, M(-2.24, 0.74, z, 0, 0.03, 0.1, 0.22), 0xd02020); });
  }

  return { V, M, col, shadeHex, Builder, merge, face, G, rbox, capsule, lathe, centroid, area, grow, chamfer, edgeOut, prism, flat, ribbon, along, length, offsetLine, distLine, inPoly, sag,
    windowPiece, doorPiece, shopPiece, PEOPLE, rider, danfo, okada, keke, car };
})();
