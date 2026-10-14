// Small procedural canvas textures. Everything is drawn in code: no photos, no downloads.
const TEX = (() => {
  let seed = 7;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  const R = (a, b) => a + (b - a) * rnd();
  const pick = (arr) => arr[Math.floor(rnd() * arr.length) % arr.length];
  const setSeed = (s) => { seed = s; };

  function canvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
  function toTex(c, rep, srgb = true) {
    const t = new THREE.CanvasTexture(c);
    if (srgb) t.encoding = THREE.sRGBEncoding;
    t.anisotropy = 4;
    if (rep) t.wrapS = t.wrapT = THREE.RepeatWrapping;
    return t;
  }
  function speckle(g, x, y, w, h, n, alpha, light, dark, size) {
    for (let i = 0; i < n; i++) {
      g.fillStyle = rnd() < 0.5 ? `rgba(${light},${alpha * rnd()})` : `rgba(${dark},${alpha * rnd()})`;
      const s = (size || 2) * (0.5 + rnd());
      g.fillRect(x + rnd() * w, y + rnd() * h, s, s);
    }
  }
  function blotch(g, x, y, r, col, a) {
    const gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, `rgba(${col},${a})`); gr.addColorStop(1, `rgba(${col},0)`);
    g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
  }

  // Corrugation profile for roofs and shutters, used as a bump map (one ridge per texture repeat).
  function ridges(vertical) {
    const c = vertical ? canvas(4, 32) : canvas(32, 4), g = c.getContext('2d');
    for (let x = 0; x < 32; x++) { const v = Math.round(128 + 127 * Math.sin(x / 32 * Math.PI * 2)); g.fillStyle = `rgb(${v},${v},${v})`; vertical ? g.fillRect(0, x, 4, 1) : g.fillRect(x, 0, 1, 4); }
    return toTex(c, true, false);
  }

  // Ankara-like print, white based so instance colours tint it.
  function ankara() {
    const S = 128, c = canvas(S, S), g = c.getContext('2d');
    g.fillStyle = '#ffffff'; g.fillRect(0, 0, S, S);
    for (let y = 0; y < S; y += 32) for (let x = (y / 32) % 2 ? 16 : 0; x < S + 16; x += 32) {
      g.fillStyle = '#3a2a20'; g.beginPath(); g.arc(x, y + 16, 11, 0, Math.PI * 2); g.fill();
      g.fillStyle = '#f4e9c8'; g.beginPath(); g.arc(x, y + 16, 7, 0, Math.PI * 2); g.fill();
      g.fillStyle = '#9a8a70'; g.beginPath(); g.arc(x, y + 16, 3, 0, Math.PI * 2); g.fill();
    }
    g.strokeStyle = '#8a7a64'; g.lineWidth = 3;
    for (let y = 0; y < S; y += 32) { g.beginPath(); for (let x = 0; x <= S; x += 8) g.lineTo(x, y + ((x / 8) % 2 ? 3 : -3)); g.stroke(); }
    return toTex(c, true);
  }

  // Soft round glow for light pools on the ground at dusk.
  function glow() {
    const S = 128, c = canvas(S, S), g = c.getContext('2d');
    const gr = g.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.4, 'rgba(255,255,255,0.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, S, S);
    return toTex(c, false);
  }

  // ---------- the sign atlas ----------
  // 2048 x 2048, cells of 512 x 128. The billboard takes a 1024 x 384 block at the bottom left.
  // Both styles share the layout, so one sign material just swaps its map.
  const AW = 2048, CW = 512, CH = 128;
  const BB = { x: 0, y: 1664, w: 1024, h: 384 };
  function cellRect(i) {
    // skip the six cells covered by the billboard (rows 13-15, cols 0-1)
    let k = -1, r = 0, col = 0;
    for (let n = 0; n < 64; n++) { r = Math.floor(n / 4); col = n % 4; if (r >= 13 && col < 2) continue; if (++k === i) break; }
    return { x: col * CW, y: r * CH, w: CW, h: CH };
  }
  const uvOf = (rc) => [rc.x / AW, 1 - (rc.y + rc.h) / AW, (rc.x + rc.w) / AW, 1 - rc.y / AW]; // u0 v0 u1 v1

  function fitText(g, ln, x, y, maxW) {
    const w = g.measureText(ln).width; const sx = Math.min(1, maxW / w);
    g.save(); g.translate(x, y); g.scale(sx, 1); g.fillText(ln, 0, 0); g.restore();
  }
  // A: printed, tidy
  function cleanSign(g, rc, text, o) {
    const { x, y, w, h } = rc;
    g.fillStyle = o.bg; g.fillRect(x, y, w, h);
    g.fillStyle = o.fg; g.fillRect(x, y + h - 10, w, 10);
    const lines = text.split('\n'); const fs = lines.length > 1 ? 38 : 54;
    g.font = `800 ${fs}px "Avenir Next", "Helvetica Neue", Arial, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillStyle = o.fg;
    lines.forEach((ln, i) => fitText(g, ln, x + w / 2, y + h / 2 - 6 + (i - (lines.length - 1) / 2) * (fs + 2), w - 48));
    if (o.phone) { g.font = '600 15px Arial, sans-serif'; g.fillStyle = o.bg; g.fillText(o.phone, x + w / 2, y + h - 5); }
  }
  // B: hand painted, uneven, faded
  function paintedSign(g, rc, text, o) {
    const { x, y, w, h } = rc;
    g.fillStyle = o.bg; g.fillRect(x, y, w, h);
    for (let i = 0; i < 5; i++) blotch(g, x + R(0, w), y + R(0, h), R(20, 60), '255,255,255', R(0.08, 0.2)); // uneven paint
    g.strokeStyle = o.fg; g.lineWidth = 5; g.beginPath();
    g.moveTo(x + 9 + R(-2, 2), y + 9); g.lineTo(x + w - 9, y + 9 + R(-2, 2)); g.lineTo(x + w - 9 + R(-2, 2), y + h - 9); g.lineTo(x + 9, y + h - 9 + R(-2, 2)); g.closePath(); g.stroke();
    const lines = text.split('\n'); const fs = lines.length > 1 ? 40 : 56;
    g.font = `900 ${fs}px "Arial Black", Impact, Arial, sans-serif`; g.textBaseline = 'middle'; g.textAlign = 'left';
    lines.forEach((ln, li) => {
      const cy = y + h / 2 + (li - (lines.length - 1) / 2) * (fs + 3) - (o.phone ? 6 : 0);
      const tw = g.measureText(ln).width; const sx = Math.min(1, (w - 40) / tw);
      let cx = x + w / 2 - tw * sx / 2;
      for (const ch of ln) { // each letter painted by hand: its own size, tilt and baseline
        const cw = g.measureText(ch).width * sx;
        g.save(); g.translate(cx + cw / 2, cy + R(-2.5, 2.5)); g.rotate(R(-0.06, 0.06)); g.scale(sx * R(0.94, 1.06), R(0.94, 1.08));
        if (o.shadow) { g.fillStyle = 'rgba(0,0,0,0.5)'; g.fillText(ch, -g.measureText(ch).width / 2 + 3, 3); }
        g.fillStyle = o.fg; g.fillText(ch, -g.measureText(ch).width / 2, 0); g.restore();
        cx += cw;
      }
    });
    if (o.phone) { g.font = '700 17px Arial, sans-serif'; g.textAlign = 'center'; g.fillStyle = o.fg; g.fillText(o.phone, x + w / 2 + R(-6, 6), y + h - 16); }
    speckle(g, x, y, w, h, 900, 0.22, '255,255,255', '40,30,20', 2);
    for (let i = 0; i < 5; i++) blotch(g, x + R(0, w), y + R(0, h), R(12, 40), '90,60,35', R(0.15, 0.35));
    g.fillStyle = 'rgba(110,55,20,0.35)'; for (let i = 0; i < 6; i++) g.fillRect(x + R(0, w), y + h - R(2, 30), R(2, 4), R(10, 30)); // rust runs from the nails
  }
  function cleanSticker(g, rc, text, bg, fg) {
    const { x, y, w, h } = rc; g.fillStyle = bg; g.fillRect(x, y, w, h);
    const lines = text.split('\n'); const fs = lines.length > 1 ? 44 : 58;
    g.font = `italic 800 ${fs}px "Avenir Next", Arial, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = fg;
    lines.forEach((ln, i) => fitText(g, ln, x + w / 2, y + h / 2 + (i - (lines.length - 1) / 2) * (fs + 2), w - 30));
  }
  function gritSticker(g, rc, text, bg, fg, sh) {
    const { x, y, w, h } = rc; g.fillStyle = bg; g.fillRect(x, y, w, h);
    const lines = text.split('\n'); const fs = lines.length > 1 ? 46 : 60;
    g.font = `italic 900 ${fs}px "Arial Black", Impact, Arial, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle';
    lines.forEach((ln, i) => {
      const cy = y + h / 2 + (i - (lines.length - 1) / 2) * (fs + 2);
      g.fillStyle = sh; for (let k = 5; k > 0; k--) fitText(g, ln, x + w / 2 + k, cy + k, w - 30);
      g.fillStyle = fg; fitText(g, ln, x + w / 2, cy, w - 30);
    });
    speckle(g, x, y, w, h, 700, 0.3, '255,255,255', '0,0,0', 2);
    g.clearRect(x + R(0, w - 40), y + R(0, h - 30), R(10, 40), R(8, 26)); // peeled
  }
  // wall writing: transparent background (B only)
  function wallPaint(g, rc, text, col) {
    const { x, y, w, h } = rc;
    g.clearRect(x, y, w, h);
    g.font = '900 42px Arial, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
    const lines = text.split('\n');
    lines.forEach((ln, i) => {
      const cy = y + h / 2 + (i - (lines.length - 1) / 2) * 44;
      g.save(); g.translate(x + w / 2, cy); g.rotate(R(-0.035, 0.035)); g.fillStyle = col;
      const tw = g.measureText(ln).width; const sx = Math.min(1, (w - 20) / tw); g.scale(sx, 1); g.fillText(ln, 0, 0); g.restore();
    });
    g.fillStyle = col; for (let i = 0; i < 12; i++) g.fillRect(x + R(30, w - 30), y + R(h / 2, h / 2 + 18), 2, R(6, 30)); // drips
  }
  function posters(g, rc, list) {
    list.forEach(([title, sub, bg, fg], i) => {
      const x = rc.x + i * 128, y = rc.y, W = 128, H = 128;
      g.fillStyle = bg; g.fillRect(x, y, W, H);
      g.fillStyle = 'rgba(40,30,20,0.85)'; g.beginPath(); g.arc(x + W / 2, y + 52, 20, 0, Math.PI * 2); g.fill(); g.fillRect(x + W / 2 - 28, y + 70, 56, 22);
      g.fillStyle = fg; g.font = '900 18px Arial, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
      g.fillText(title, x + W / 2, y + 22, W - 10); g.font = '700 11px Arial, sans-serif'; g.fillText(sub, x + W / 2, y + 112, W - 10);
      speckle(g, x, y, W, H, 300, 0.3, '255,255,255', '0,0,0', 2);
      g.clearRect(x + R(0, W - 20), y + R(0, H - 20), R(8, 22), R(8, 22)); // torn
    });
  }
  function billboard(g, gritty) {
    const { x, y, w, h } = BB;
    g.fillStyle = '#14365e'; g.fillRect(x, y, w, h);
    g.fillStyle = '#f2b705'; g.fillRect(x, y + h - 70, w, 70);
    g.fillStyle = '#f2b705'; g.beginPath(); g.arc(x + w - 110, y + 130, 70, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#14365e'; g.font = '900 80px Arial, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('S', x + w - 110, y + 134);
    g.textAlign = 'left'; g.textBaseline = 'alphabetic'; g.fillStyle = '#ffffff';
    g.font = '900 86px "Arial Black", Arial, sans-serif'; g.fillText('STEADY TRUST BANK', x + 40, y + 130, w - 260);
    g.font = '700 50px Arial, sans-serif'; g.fillText('Your money no go waka.', x + 40, y + 210, w - 260);
    g.fillStyle = '#14365e'; g.font = '700 32px Arial, sans-serif'; g.fillText('EVERY BRANCH NA MASTERPIECE', x + 40, y + h - 24, w - 80);
    if (gritty) {
      speckle(g, x, y, w, h, 3000, 0.14, '255,255,255', '0,0,0', 3);
      for (let i = 0; i < 7; i++) { g.fillStyle = 'rgba(80,55,30,0.3)'; g.fillRect(x + R(0, w), y + R(0, 40), R(3, 9), R(60, 240)); }
      g.fillStyle = 'rgba(225,215,195,0.9)'; g.fillRect(x + R(500, 800), y + R(0, 80), R(80, 160), R(40, 90)); // a torn strip
    }
  }

  // Builds both atlases from one list of entries; returns { a, b, uv(id) }.
  function atlases(entries) {
    const ids = {}; const out = {};
    ['a', 'b'].forEach(style => {
      setSeed(style === 'a' ? 101 : 202);
      const c = canvas(AW, AW), g = c.getContext('2d');
      g.fillStyle = style === 'a' ? '#ffffff' : '#ddd5c4'; g.fillRect(0, 0, AW, AW);
      entries.forEach((e, i) => {
        const rc = cellRect(i); ids[e.id] = uvOf(rc);
        if (e.kind === 'sign') (style === 'a' ? cleanSign : paintedSign)(g, rc, e.text, e);
        else if (e.kind === 'sticker') style === 'a' ? cleanSticker(g, rc, e.text, e.bg, e.fg) : gritSticker(g, rc, e.text, e.bg, e.fg, e.sh);
        else if (e.kind === 'paint') { if (style === 'b') wallPaint(g, rc, e.text, e.col); }
        else if (e.kind === 'posters') { if (style === 'b') posters(g, rc, e.list); }
      });
      billboard(g, style === 'b');
      out[style] = toTex(c, false);
    });
    ids.billboard = uvOf(BB);
    return { a: out.a, b: out.b, uv: (id) => ids[id] };
  }

  // Ground occlusion: building footprints blurred onto a canvas (white = open sky). Read by every material near the ground.
  function aoMap(size, half, shapes) {
    const c = canvas(size, size), g = c.getContext('2d');
    g.fillStyle = '#fff'; g.fillRect(0, 0, size, size);
    const k = size / (half * 2), tx = (x) => (x + half) * k;
    shapes.forEach(({ poly, strength, spread }) => {
      const steps = 6;
      for (let s = steps; s >= 0; s--) {
        const d = spread * s / steps; const cx = poly.reduce((a, p) => a + p[0], 0) / poly.length, cz = poly.reduce((a, p) => a + p[1], 0) / poly.length;
        g.fillStyle = `rgba(0,0,0,${strength / (steps + 1)})`; g.beginPath();
        poly.forEach((p, i) => { const dx = p[0] - cx, dz = p[1] - cz, l = Math.hypot(dx, dz) || 1; const X = tx(p[0] + dx / l * d), Z = tx(p[1] + dz / l * d); i ? g.lineTo(X, Z) : g.moveTo(X, Z); });
        g.closePath(); g.fill();
      }
    });
    const t = toTex(c, false, false); t.anisotropy = 1; t.flipY = false; // row 0 = north edge (z = -half)
    return t;
  }

  return { rnd, R, pick, setSeed, ridges, ankara, glow, atlases, aoMap };
})();
