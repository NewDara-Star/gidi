// Gidi Mock: walk and drive through the generated city.
// The behaviour is the owner's Real-world sim (car physics with Pacejka tyres, G29 force feedback,
// keyboard/pad/wheel input, SUMO-network traffic with signals and give-way, pedestrians); the world
// and every model are Gidi's own kit (blender/: city tiles, fleet, people).
import * as THREE from "three/webgpu";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { Graphics, type Quality } from "./graphics";
import { World, CENTRE } from "./world";
import { TileStreamer } from "./tiles";
import { NetTraffic, VEHICLE_MODELS, WALKER_MODELS } from "./trafficnet";
import { loadVehicleModels } from "./models";
import { PlayerVehicle, type VehicleKind } from "./drive";
import { DriveControls } from "./wheel";
import { G29 } from "./g29";
import { Input } from "./input";
import { initPhysics, physicsReady, wheelRangeDeg } from "./carphysics";
import { ALLOW_CAR, ALLOW_SERVICE, LaneKind } from "./roadnet";
import { Signals } from "./signals";

const params = new URLSearchParams(location.search);
// The repo root: the Mock lives at mock/dist/ (or mock/ in dev); the city data at web/.
const BASE = params.get("base") ?? new URL("../../", location.href).href;
const MODELS = new URL("models/", location.href).href;
const $ = (id: string) => document.getElementById(id)!;
const toast = (t: string) => {
  const el = $("toast");
  el.textContent = t;
  el.classList.add("on");
  clearTimeout((toast as any).t);
  (toast as any).t = setTimeout(() => el.classList.remove("on"), 4500);
};

const canvas = $("c") as HTMLCanvasElement;
const gfx = new Graphics(canvas);
await gfx.init((params.get("q") as Quality) ?? "high");
gfx.setPlace(6.5, 3.4, "Africa/Lagos");
let hours = Number(params.get("time") ?? 16.5);
gfx.setTime(hours);
const scene = gfx.scene, camera = gfx.camera;

$("load").textContent = "Loading Gidi…";
const world = new World();
await world.load(BASE);
scene.add(world.group);
const tiles = new TileStreamer(BASE);
await tiles.init(world.massingByTile);
scene.add(tiles.group);

// traffic and pedestrians on the city's lane network
let traffic: NetTraffic | null = null;
if (world.net) {
  traffic = new NetTraffic(world.net, { honk: () => {} }, { vehicles: 130, walkers: 280 }, "right");
  traffic.busy = (x: number, z: number) => world.crowdAt(x, z);
  traffic.blocked = (x: number, z: number) => world.blocked(x, z);
  scene.add(traffic.group);
  loadVehicleModels(VEHICLE_MODELS, MODELS).then((m) => traffic!.setVehicleModels(m));
  const loader = new GLTFLoader();
  Promise.all(WALKER_MODELS.map((k) => Promise.all([0, 1].map((s) => loader.loadAsync(`${MODELS}gidi_person_${k}_${s}.glb`).then((g) => g.scene, () => null)))))
    .then((m) => traffic!.setWalkerModels(m));
}

// visible traffic lights at the signalised junctions, on the traffic's own clock
const signals = world.net ? new Signals(world.net) : null;
if (signals) scene.add(signals.group);

// the player: on foot, or in a danfo or a car
const me = { x: 0, z: 0, yaw: 0, camYaw: 0, speed: 0 };
const xy = params.get("xy")?.split(",").map(Number);
const spawn = xy ? world.spawnAt(xy[0], xy[1]) : world.spawn(params.get("at"));
Object.assign(me, { x: spawn.x, z: spawn.z, yaw: spawn.yaw, camYaw: spawn.yaw + Math.PI });
if (params.get("look")) { me.yaw = (Number(params.get("look")) * Math.PI) / 180; me.camYaw = me.yaw + Math.PI; } // degrees, 0 = south, 90 = east
const avatar = new THREE.Group();
new GLTFLoader().loadAsync(`${MODELS}gidi_person_ankara_0.glb`).then((g) => avatar.add(g.scene), () => {});
scene.add(avatar);

const drive = new DriveControls();
const g29 = new G29();
drive.g29 = g29;
const input = new Input(canvas);
let car: PlayerVehicle | null = null;
let cockpit = false;
let ffbJolt = 0;
void initPhysics();
const bodyModels: Record<VehicleKind, Promise<THREE.Object3D | null>> = {
  danfo: new GLTFLoader().loadAsync(`${MODELS}gidi_danfo_0.glb`).then((g) => g.scene, () => null),
  car: new GLTFLoader().loadAsync(`${MODELS}gidi_car_saloon.glb`).then((g) => g.scene, () => null),
};

function laneSpot(x: number, z: number) {
  const net = world.net;
  if (!net) return null;
  let best: { x: number; z: number; yaw: number } | null = null, bd = 120;
  for (const l of net.lanes) {
    if (l.kind !== LaneKind.Road || !(l.allow & ALLOW_CAR) || l.allow & ALLOW_SERVICE || l.length < 30) continue;
    for (let k = 0; k + 3 < l.pts.length; k += 2) {
      const ax = l.pts[k], az = l.pts[k + 1], bx = l.pts[k + 2], bz = l.pts[k + 3];
      const dx = bx - ax, dz = bz - az, len2 = dx * dx + dz * dz || 1;
      const t = Math.max(0.1, Math.min(0.9, ((x - ax) * dx + (z - az) * dz) / len2));
      const px = ax + dx * t, pz = az + dz * t;
      const d = Math.hypot(x - px, z - pz);
      if (d < bd) { bd = d; best = { x: px, z: pz, yaw: Math.atan2(dx, dz) }; }
    }
  }
  return best;
}

async function enterVehicle(kind: VehicleKind) {
  if (car) return;
  if (!physicsReady()) return toast("Still loading the car physics, try again in a second");
  const spot = laneSpot(me.x, me.z);
  if (!spot) return toast("No road near here. Walk to a street first");
  car = new PlayerVehicle(kind, spot.x, spot.z, spot.yaw, world as any, "right");
  carKind = kind;
  const model = await bodyModels[kind];
  if (model) car.setBodyModel(model.clone(true));
  scene.add(car.root);
  void g29.setRange(wheelRangeDeg(car.spec.physics));
  avatar.visible = false;
  me.camYaw = spot.yaw + Math.PI;
  setCockpit(false);
  drive.read(0);
  $("speedo").hidden = false;
  toast(g29.connected || drive.wheelPad() ? "In P with the parking brake on. Brake, right paddle to D, then gas." : "Brake (S) then X for Drive · Z back toward R and P · B parking brake · C camera · F get out");
}

function exitVehicle() {
  if (!car) return;
  me.x = car.x + Math.cos(car.yaw) * 2.2;
  me.z = car.z - Math.sin(car.yaw) * 2.2;
  me.yaw = car.yaw;
  scene.remove(car.root);
  car.dispose();
  car = null;
  avatar.visible = true;
  void g29.release();
  $("speedo").hidden = true;
}

function setCockpit(on: boolean) {
  cockpit = on;
  car?.setCockpit(on);
  camera.fov = on ? 72 : 60;
  camera.updateProjectionMatrix();
}

// N: write a note for the fix list (desktop app: saved to mock/notes/NOTES.md with a screenshot)
const noteBox = $("note") as HTMLFormElement, noteText = $("notetext") as HTMLTextAreaElement;
let carKind = "";
for (const t of ["keydown", "keyup"]) noteText.addEventListener(t, (e) => e.stopPropagation()); // typing doesn't walk or drive
noteText.addEventListener("keydown", async (e) => {
  if (e.key === "Escape") { noteBox.hidden = true; return; }
  if (e.key !== "Enter" || e.shiftKey) return;
  e.preventDefault();
  const text = noteText.value.trim();
  noteBox.hidden = true;
  noteText.blur();
  if (!text) return;
  const gx = me.x + CENTRE.x, gy = me.z + CENTRE.y;
  const body = { text, x: gx, y: gy, district: world.districtAt(me.x, me.z), driving: car ? carKind : "", hour: `${Math.floor(hours)}:00` };
  await new Promise((r) => setTimeout(r, 120)); // let the box close before the screenshot
  try {
    const r = await fetch(`${BASE}__note`, { method: "POST", body: JSON.stringify(body) });
    if (!r.ok) throw new Error();
    toast("Saved to mock/notes/NOTES.md");
  } catch {
    const list = JSON.parse(localStorage.getItem("gidiNotes") || "[]");
    list.push(body);
    try { localStorage.setItem("gidiNotes", JSON.stringify(list)); } catch {}
    toast("Saved in this browser (the desktop app writes them to mock/notes)");
  }
});

addEventListener("keydown", (e) => {
  const k = e.key.toLowerCase();
  if (k === "n" && noteBox.hidden) { e.preventDefault(); noteBox.hidden = false; noteText.value = ""; noteText.focus(); return; }
  if (k === "f" && !car) void enterVehicle("danfo");
  else if (k === "g" && !car) void enterVehicle("car");
  else if (k === "t") { hours = (hours + 1) % 24; gfx.setTime(hours); toast(`${Math.floor(hours)}:00`); }
});
$("connect").addEventListener("click", async () => {
  const ok = await g29.connect();
  toast(ok ? "Wheel connected: force feedback on" : "Couldn't open the wheel (Chrome/Electron, PC mode)");
});
addEventListener("pagehide", () => void g29.release());

// ------------------------------------------------------------- loop
let last = performance.now();
let lookOffset = 0;
let lastWallToast = 0;
const tmp = new THREE.Vector3();
function frame(now: number) {
  requestAnimationFrame(frame);
  const dt = Math.min(0.05, (now - last) / 1000);
  last = now;
  if (car) driveStep(dt);
  else walkStep(dt);
  tiles.update(me.x, me.z);
  if (traffic) traffic.update(dt, me.x, me.z, car ? { x: car.x, z: car.z, yaw: car.yaw, speed: Math.abs(car.vf), driving: true } : { x: me.x, z: me.z, yaw: me.yaw, speed: me.speed, driving: false });
  if (signals && traffic) signals.update(traffic.time, me.x, me.z);
  placeCamera(dt);
  gfx.follow(me.x, me.z);
  gfx.render();
  const d = world.districtAt(me.x, me.z);
  $("where").textContent = d ?? "Outside the districts";
  if (world.blocked(me.x + Math.sin(me.yaw) * 6, me.z + Math.cos(me.yaw) * 6) && now - lastWallToast > 8000) {
    lastWallToast = now;
    toast("Not built yet: this district opens when it's built out");
  }
}

function walkStep(dt: number) {
  input.update();
  drive.read(dt);
  me.camYaw += input.takeYawDelta();
  const sp = input.run ? 5.5 : 1.6;
  const mx = input.move.x, my = input.move.y;
  if (mx || my) {
    // camera space -> world: forward is away from the camera
    const fwd = me.camYaw + Math.PI;
    const vx = Math.sin(fwd) * my - Math.cos(fwd) * mx, vz = Math.cos(fwd) * my + Math.sin(fwd) * mx;
    const l = Math.hypot(vx, vz) || 1;
    const nx = me.x + (vx / l) * sp * dt, nz = me.z + (vz / l) * sp * dt;
    if (!world.blocked(nx, nz) && !world.footprintList.some((f, i) => i % 1 === 0 && Math.abs(f[0] - nx) < 60 && Math.abs(f[1] - nz) < 60 && inside(f, nx, nz))) {
      me.x = nx;
      me.z = nz;
    }
    me.yaw = Math.atan2(vx, vz);
    me.speed = sp;
  } else me.speed = 0;
  avatar.position.set(me.x, 0.05, me.z);
  avatar.rotation.y = me.yaw;
}

function inside(p: Float32Array, x: number, z: number) {
  let ins = false;
  const n = p.length / 2;
  for (let i = 0, j = n - 1; i < n; j = i++) {
    const xi = p[i * 2], zi = p[i * 2 + 1], xj = p[j * 2], zj = p[j * 2 + 1];
    if (zi > z !== zj > z && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) ins = !ins;
  }
  return ins;
}

/** G29's gears swallow small forces: lift anything above a hair past the dead band (Real-world main.ts). */
function minForce(x: number) {
  const m = 0.06, eps = 0.02;
  const a = Math.min(1, Math.abs(x));
  return Math.sign(x) * (a < eps ? (a / eps) * (m + (1 - m) * eps) : m + (1 - m) * a);
}

function driveStep(dt: number) {
  const c = car!;
  const inp = drive.read(dt);
  if (inp.shift) {
    const why = c.shift(inp.shift, inp.brake);
    if (why) toast(why);
  }
  c.controls(inp, dt);
  c.update(dt, inp, world as any, traffic ?? undefined);
  if (traffic) {
    const fx = Math.sin(c.yaw), fz = Math.cos(c.yaw), r = c.spec.width / 2;
    for (const o of [c.spec.length / 2 - r, -(c.spec.length / 2 - r)]) {
      const hit = traffic.collide(c.x + fx * o, c.z + fz * o, r);
      if (hit && hit.kind === "person") c.hitPerson();
    }
  }
  if (c.impact > 1.5) ffbJolt = (c.vr >= 0 ? 1 : -1) * Math.min(1, c.impact / 10);
  if (g29.connected) {  // force feedback: the front tyres' aligning torque at the rack (Real-world main.ts)
    ffbJolt *= Math.pow(0.002, dt);
    if (c.kerbJolt) ffbJolt = c.kerbJolt;
    void g29.setSpring(0);
    void g29.setDamper(0.13 + 0.2 * Math.max(0, 1 - c.speed / 8));
    void g29.setForce(inp.keyboardSteering ? 0 : minForce(c.phys.steerTorque * 0.045 + ffbJolt));
    void g29.setRevLights(c.rpm > 0.35 ? (c.rpm - 0.35) / 0.6 : 0);
  }
  if (inp.camera) setCockpit(!cockpit);
  if (inp.exit) return exitVehicle();
  lookOffset += input.takeYawDelta();
  lookOffset *= Math.pow(0.08, dt);
  me.x = c.x;
  me.z = c.z;
  me.yaw = c.yaw;
  me.speed = c.speed;
  $("kmh").textContent = String(Math.round(Math.abs(c.vf) * 3.6));
  $("gear").textContent = c.selector + (c.selector === "D" ? c.gear : "");
}

function placeCamera(dt: number) {
  if (car) {
    if (cockpit) {
      car.placeCamera(camera, car.spec.cockpit.x, car.spec.cockpit.y, car.spec.cockpit.z, lookOffset, dt);
      return;
    }
    const want = car.yaw + Math.PI + lookOffset;
    me.camYaw += Math.atan2(Math.sin(want - me.camYaw), Math.cos(want - me.camYaw)) * Math.min(1, dt * 3.5);
    const dist = 10.5 + Math.min(6, car.speed * 0.15);
    camera.position.set(car.x + Math.sin(me.camYaw) * dist, 4.4, car.z + Math.cos(me.camYaw) * dist);
    camera.lookAt(tmp.set(car.x, 1.4, car.z));
    return;
  }
  const dist = 5.5;
  camera.position.set(me.x + Math.sin(me.camYaw) * dist, 2.6, me.z + Math.cos(me.camYaw) * dist);
  camera.lookAt(tmp.set(me.x, 1.5, me.z));
}

addEventListener("resize", () => gfx.resize());
$("load").remove();
if (params.get("drive")) setTimeout(() => void enterVehicle(params.get("drive") as VehicleKind), 2500);
(window as any).__gidiState = () => ({ x: me.x, z: me.z, driving: !!car, tiles: (tiles as any).loaded?.size, cars: traffic?.cars.filter((c: any) => c.active).length });
toast("WASD to walk (Shift runs), drag to look · F: drive a danfo · G: drive a car · T: time of day · N: write a note · 🎮 Connect wheel for the G29");
requestAnimationFrame(frame);
(window as any).__gidi = { world, tiles, traffic, me, CENTRE };
