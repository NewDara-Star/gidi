// Gidi desktop shell (adapted from the owner's Real-world desktop/main.cjs): opens the Gidi map
// (web/gidi-maps.html: 2D, 3D and Mock tabs) as a native app.
// - Serves the whole repo over a private app:// scheme, so the map, the Mock (mock/dist) and the
//   streamed city (web/city) load with fetch() and WebGPU exactly as on the web.
// - Grants WebHID access to Logitech wheels without a picker, so the G29 (force feedback, rev
//   lights) just works.
// - Screenshot mode, for checking the Mock without anyone at the controls:
//     GIDI_SHOT=out.png GIDI_AT="Ladi Lane" GIDI_WAIT=40 npx electron .
const { app, BrowserWindow, protocol, net, session, Menu } = require("electron");
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const ROOT = path.join(__dirname, "..", "..");
const LOGITECH = 0x046d;

protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true } },
]);
app.commandLine.appendSwitch("ignore-gpu-blocklist");
app.commandLine.appendSwitch("enable-unsafe-webgpu");

let mainWin = null;
const NOTES = path.join(ROOT, "mock", "notes");

// The Mock's N key: a play-tester's note, with where they were and a screenshot, appended to
// mock/notes/NOTES.md (screenshots beside it).
async function saveNote(req) {
  const n = await req.json();
  fs.mkdirSync(NOTES, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  let shot = "";
  if (mainWin) {
    const img = await mainWin.webContents.capturePage();
    shot = `${stamp}.jpg`;
    fs.writeFileSync(path.join(NOTES, shot), img.toJPEG(80));
  }
  const file = path.join(NOTES, "NOTES.md");
  if (!fs.existsSync(file)) fs.writeFileSync(file, "# Mock play-test notes\n\nWritten in the Mock with **N**. Each note has where you were (map metres, the Mock's `?xy=` link) and a screenshot.\n");
  const where = `${n.district ?? "outside the districts"}, xy ${Math.round(n.x)},${Math.round(n.y)}${n.driving ? `, driving a ${n.driving}` : ", on foot"}, ${n.hour}`;
  fs.appendFileSync(file, `\n- **${new Date().toLocaleString("en-GB")}**: ${String(n.text).replace(/\n/g, " ")}\n  - ${where}${shot ? ` · ![](${shot})` : ""}\n`);
  return new Response(JSON.stringify({ ok: true, file: "mock/notes/NOTES.md" }), { headers: { "content-type": "application/json" } });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1600, height: 950, backgroundColor: "#0d0f12", title: "Gidi", autoHideMenuBar: true,
    webPreferences: { preload: path.join(__dirname, "preload.cjs"), contextIsolation: true, sandbox: true, backgroundThrottling: false },
  });
  mainWin = win;
  const env = process.env;
  if (env.GIDI_SHOT) {
    const q = new URLSearchParams({ base: "app://gidi/" });
    if (env.GIDI_AT) q.set("at", env.GIDI_AT);
    if (env.GIDI_XY) q.set("xy", env.GIDI_XY);
    if (env.GIDI_LOOK) q.set("look", env.GIDI_LOOK);
    if (env.GIDI_EXACT) q.set("exact", "1");
    if (env.GIDI_TIME) q.set("time", env.GIDI_TIME);
    if (env.GIDI_DRIVE) q.set("drive", env.GIDI_DRIVE);
    win.loadURL(`app://gidi/mock/dist/index.html?${q}`);
    win.webContents.on("console-message", (_e, level, msg) => { if (level >= 2) console.log("page:", msg); });
    win.webContents.once("did-finish-load", async () => {
      await new Promise((r) => setTimeout(r, (Number(env.GIDI_WAIT) || 40) * 1000));
      const img = await win.webContents.capturePage();
      fs.writeFileSync(path.resolve(env.GIDI_SHOT), img.toPNG());
      const info = await win.webContents.executeJavaScript("JSON.stringify(window.__gidiState ? window.__gidiState() : {})").catch(() => "{}");
      console.log("SHOT", env.GIDI_SHOT, info);
      app.quit();
    });
    return;
  }
  win.loadURL("app://gidi/web/gidi-maps.html");
  if (env.GIDI_MAPSHOT) {  // open the map, click a view tab (GIDI_TAB: dim2d, dim3d, dimmock), capture
    win.webContents.once("did-finish-load", async () => {
      await new Promise((r) => setTimeout(r, 4000));
      await win.webContents.executeJavaScript(`document.getElementById(${JSON.stringify(env.GIDI_TAB || "dimmock")})?.click()`);
      await new Promise((r) => setTimeout(r, (Number(env.GIDI_WAIT) || 40) * 1000));
      fs.writeFileSync(path.resolve(env.GIDI_MAPSHOT), (await win.webContents.capturePage()).toPNG());
      console.log("MAPSHOT", env.GIDI_MAPSHOT);
      app.quit();
    });
  }
  win.webContents.on("before-input-event", (event, input) => {
    if (input.type === "keyDown" && (input.key === "F11" || (input.meta && input.control && input.key.toLowerCase() === "f"))) {
      win.setFullScreen(!win.isFullScreen());
      event.preventDefault();
    }
  });
}

app.whenReady().then(() => {
  // app://gidi/<path> -> <repo>/<path>
  protocol.handle("app", (req) => {
    const { pathname } = new URL(req.url);
    if (pathname === "/__note" && req.method === "POST") return saveNote(req);
    const file = path.normalize(path.join(ROOT, decodeURIComponent(pathname)));
    if (!file.startsWith(ROOT)) return new Response("forbidden", { status: 403 });
    // HTML and JS as UTF-8 (the map's labels use ² and ·); everything else as it comes
    const type = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8" }[path.extname(file)];
    if (type) return net.fetch(pathToFileURL(file).toString()).then(async (r) => new Response(await r.arrayBuffer(), { status: r.status, headers: { "content-type": type } }));
    return net.fetch(pathToFileURL(file).toString());
  });
  const ses = session.defaultSession;
  ses.setPermissionCheckHandler((_wc, permission) => permission === "hid" || permission === "media");
  ses.setDevicePermissionHandler((details) => details.deviceType === "hid" && details.device.vendorId === LOGITECH);
  ses.on("select-hid-device", (event, details, callback) => {
    event.preventDefault();
    const wheel = details.deviceList.find((d) => d.vendorId === LOGITECH);
    callback(wheel ? wheel.deviceId : undefined);
  });
  Menu.setApplicationMenu(null);
  createWindow();
  app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});
app.on("window-all-closed", () => { if (process.platform !== "darwin") app.quit(); });
