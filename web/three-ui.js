/* Panel, district switcher and controls for Gidi 3D. */
(function () {
  const D = window.DISTRICT, G3 = window.GIDI3D;
  const ORDER = [["jungle", "Jungle City"], ["maze", "The Maze"], ["hub", "The Hub"], ["railside", "Railside"], ["foodgate", "Food Gate"],
    ["port", "The Port"], ["bazaar", "The Bazaar"], ["capital", "The Capital"], ["estate", "The Estate"], ["oldisland", "Old Island"],
    ["oldshore", "Old Shore"], ["border", "The Border"], ["watertown", "Water Town"], ["heights", "The Heights"], ["frontier", "The Frontier"]];
  const GLYPH = { story: "★", market: "M", transit: "T", danger: "!", check: "✕", night: "☾", landmark: "◆", industry: "▲", water: "≈", gov: "▣", park: "≡" };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  document.getElementById("districts").innerHTML = ORDER.map(([id, n]) =>
    id === D.id ? `<button class="dchip on" aria-current="true">${n}</button>` : `<span class="dchip" title="Not modelled yet">${n}<small>soon</small></span>`).join("");

  const okada = { ban: ["ban", "Okada banned"], sweep: ["sweep", "Okada sweeps"], free: ["", "Okada country"] }[D.okada];
  let done = {}; try { done = JSON.parse(localStorage.getItem("gidi3d-done-" + D.id) || "{}"); } catch (e) {}
  document.getElementById("eyebrow").textContent = "District 1 of 15 · inspired by " + D.inspired;
  document.getElementById("pbody").innerHTML = `
    <h1>${esc(D.name)}</h1>
    <div class="chips"><span class="chip a1">Act ${D.act} · Survive</span><span class="chip ${okada[0]}">${okada[1]}</span><span class="chip">Oja: ${esc(D.oja)}</span></div>
    <p class="lead">${esc(D.blurb)}</p>
    <div class="stats">${D.lots.length.toLocaleString()} buildings · ${D.trees.length} trees · ${D.area.toFixed(1)} km²</div>
    <h2>Landmarks</h2>
    <ul class="places">${D.pois.map((p, i) => p.civic ? "" : `<li><button data-i="${i}" class="t-${p.type}"><span class="pin">${GLYPH[p.type]}</span><span><span class="pn">${esc(p.name)}</span><span class="ps">${esc(p.note)}</span></span></button></li>`).join("")}</ul>
    <h2>What to model</h2>
    <ul class="model">${D.model.map((m, i) => `<li><input type="checkbox" id="m${i}" ${done[i] ? "checked" : ""}><label for="m${i}">${esc(m)}</label></li>`).join("")}</ul>
    <h2>Between missions</h2>
    <ul class="model">${D.activities.map((a) => `<li>· ${esc(a)}</li>`).join("")}</ul>
    <h2>Key</h2>
    <div class="legend">
      <span class="sw" style="background:#8a4f36"></span><span>Rusted tin gable roof: bungalows and back-row compounds</span>
      <span class="sw" style="background:#a9a49b"></span><span>Flat concrete roof, often with a water tank</span>
      <span class="sw" style="background:#c8c5bf"></span><span>Uncompleted building, rebar showing</span>
      <span class="sw" style="background:#7a7f86"></span><span>Main street · lanes are lighter</span>
      <span class="sw" style="background:#6aa39b"></span><span>The canal (gang line)</span>
      <span class="sw" style="background:#6b7077"></span><span>Ring Road flyover, buka and touts underneath</span>
    </div>`;
  document.querySelectorAll(".places button").forEach((b) => b.addEventListener("click", () => G3.focusPoi(+b.dataset.i)));
  document.querySelectorAll(".model input").forEach((c) => c.addEventListener("change", () => {
    done[c.id.slice(1)] = c.checked; try { localStorage.setItem("gidi3d-done-" + D.id, JSON.stringify(done)); } catch (e) {}
  }));
  window.addEventListener("poi", (e) => document.querySelectorAll(".places button").forEach((b) => b.classList.toggle("on", +b.dataset.i === e.detail)));

  const panel = document.getElementById("panel"), tg = document.getElementById("toggle");
  tg.addEventListener("click", () => { const shut = panel.classList.toggle("shut"); document.getElementById("pbody").hidden = shut; tg.textContent = shut ? "Show" : "Hide"; });
  let flat = false; const dim = document.getElementById("dim");
  dim.addEventListener("click", () => { flat = !flat; G3.topDown(flat); dim.textContent = flat ? "3D" : "2D"; });
  document.getElementById("home").addEventListener("click", () => { flat = false; dim.textContent = "2D"; G3.home(); });
  document.getElementById("compass").addEventListener("click", G3.north);
  document.getElementById("zin").addEventListener("click", () => G3.zoom(0.6));
  document.getElementById("zout").addEventListener("click", () => G3.zoom(1.6));
})();
