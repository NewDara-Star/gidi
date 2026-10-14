// Streams the Blender-generated city (web/city/<detail>/tiles/<tx>_<ty>.glb, see blender/city.py)
// round the player: full detail within one tile, the lighter web build out to three, the data's
// massing beyond. Materials come back by name and are rebuilt here in TSL; each vertex colour's
// alpha carries the kit's wear value, so the weathering (stains, rain streaks, red mud splash,
// chalky paint, rust on zinc and steel) is the same as in the Blender renders.
import * as THREE from "three/webgpu";
import { abs, attribute, float, mix, mx_noise_float, normalWorld, positionWorld, smoothstep, vec3 } from "three/tsl";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { DRACOLoader } from "three/examples/jsm/loaders/DRACOLoader.js";
import { CENTRE } from "./world";

interface Manifest {
  size: number;
  details: string[];
  tiles: Record<string, Record<string, { faces: number; bytes: number }>>;
}

const n01 = (p: any, s: number) => mx_noise_float(p.mul(s)).mul(0.5).add(0.5);

/** Kit material -> node material. `kind` is the Blender master material's name. */
function makeMaterial(kind: string): THREE.Material {
  const c = attribute("color", "vec4");
  const base = c.xyz;
  const wear = c.w;
  const p = positionWorld;
  const wall = float(1).sub(abs(normalWorld.y));
  const big = n01(p, 0.35);
  const fine = n01(p, 6.0);
  if (kind === "emit") {
    const m = new THREE.MeshBasicNodeMaterial();
    m.colorNode = base.mul(1.6);
    return m;
  }
  if (kind === "water") {
    // muddy water: mostly its own colour, soft reflections
    const m = new THREE.MeshStandardNodeMaterial({ roughness: 0.3, metalness: 0.0 });
    m.colorNode = base.mul(0.8);
    return m;
  }
  if (kind === "glass" || kind === "glass_lit") {
    const m = new THREE.MeshStandardNodeMaterial({ roughness: 0.06, metalness: 0.45 });
    m.colorNode = base;
    return m;
  }
  if (kind === "zinc" || kind === "steel") {
    const m = new THREE.MeshStandardNodeMaterial();
    const patina = mix(base, vec3(0.36, 0.27, 0.2), wear.mul(0.55));
    const streak = n01(vec3(p.x.mul(6), p.y.mul(0.6), p.z.mul(6)), 2.5);
    const r = smoothstep(float(0.85).sub(wear.mul(0.3)), 0.95, streak.mul(0.6).add(big.mul(0.4)));
    const rust = r.mul(wear.mul(1.2)).clamp(0, 1);
    m.colorNode = mix(patina, mix(vec3(0.22, 0.09, 0.03), vec3(0.4, 0.17, 0.06), fine), rust);
    m.roughnessNode = float(kind === "zinc" ? 0.4 : 0.5).add(rust.add(wear).mul(0.3));
    m.metalnessNode = float(kind === "zinc" ? 0.55 : 0.3).sub(rust.add(wear).mul(0.3));
    return m;
  }
  // painted render, concrete, block, earth, asphalt, wood...: stains and streaks by wear,
  // red earth splashed up the foot of walls, sun-chalked paint, fine unevenness always
  const m = new THREE.MeshStandardNodeMaterial({ roughness: kind === "asphalt" ? 0.92 : 0.86 });
  const streak = n01(vec3(p.x.add(p.z).mul(2.6), p.y.mul(0.16), float(3.7)), 1.0);
  const stain = smoothstep(0.45, 0.75, big).mul(0.75).add(wall.mul(smoothstep(0.5, 0.8, streak)).mul(0.7));
  let col = mix(base, base.mul(vec3(0.5, 0.42, 0.33)), stain.mul(wear).mul(0.75).clamp(0, 0.85));
  if (kind === "paint") col = mix(col, vec3(0.86, 0.84, 0.8), smoothstep(0.55, 0.8, n01(p, 0.9)).mul(wear).mul(0.6));
  const foot = float(1).sub(smoothstep(0.05, float(0.5).add(big.mul(0.9)), p.y)).mul(wall);
  col = mix(col, vec3(0.42, 0.19, 0.09), foot.mul(wear).mul(0.8).clamp(0, 1));
  m.colorNode = col.mul(fine.mul(0.12).oneMinus().add(0.06));
  return m;
}

export class TileStreamer {
  group = new THREE.Group();
  private manifest: Manifest | null = null;
  private loader = new GLTFLoader();
  private loaded = new Map<string, { detail: string; obj: THREE.Object3D } | "loading">();
  private materials = new Map<string, THREE.Material>();
  private massing = new Map<string, THREE.Object3D>();
  private size = 400;
  private last = "";

  constructor(private base: string) {
    const draco = new DRACOLoader();
    draco.setDecoderPath(`${location.href.replace(/[^/]*$/, "")}draco/`);
    this.loader.setDRACOLoader(draco);
  }

  async init(massingByTile: Map<string, THREE.Object3D>) {
    this.massing = massingByTile;
    try {
      this.manifest = await fetch(`${this.base}web/city/manifest.json`).then((r) => r.json());
      this.size = this.manifest!.size;
    } catch {
      this.manifest = null;
    }
  }

  tileOf(x: number, z: number) {
    return { tx: Math.floor((x + CENTRE.x) / this.size), ty: Math.floor((z + CENTRE.y) / this.size) };
  }

  /** Call every frame or so with the player's position; loads and drops tiles as they move. */
  update(x: number, z: number) {
    if (!this.manifest) return;
    const { tx, ty } = this.tileOf(x, z);
    const key = `${tx}_${ty}`;
    if (key === this.last) return;
    this.last = key;
    const want = new Map<string, string>();
    for (let dx = -3; dx <= 3; dx++) {
      for (let dy = -3; dy <= 3; dy++) {
        const k = `${tx + dx}_${ty + dy}`;
        const have = this.manifest.tiles[k];
        if (!have) continue;
        const ring = Math.max(Math.abs(dx), Math.abs(dy));
        const det = ring <= 1 && have.full ? "full" : have.web ? "web" : have.full ? "full" : "";
        if (det) want.set(k, det);
      }
    }
    for (const [k, v] of this.loaded) {  // drop what's out of range or at the wrong detail
      if (v === "loading") continue;
      if (want.get(k) !== v.detail) {
        this.group.remove(v.obj);
        v.obj.traverse((o) => (o as THREE.Mesh).geometry?.dispose());
        this.loaded.delete(k);
        const ms = this.massing.get(k);
        if (ms) ms.visible = true;
      }
    }
    // nearest first
    const order = [...want.entries()].sort((a, b) => this.ring(a[0], tx, ty) - this.ring(b[0], tx, ty));
    for (const [k, det] of order) {
      if (this.loaded.has(k)) continue;
      this.loaded.set(k, "loading");
      const [ax, ay] = k.split("_").map(Number);
      this.loader.load(`${this.base}web/city/${det}/tiles/${k}.glb`, (gltf) => {
        const cur = this.loaded.get(k);
        if (cur !== "loading") return;
        const obj = gltf.scene;
        obj.position.set(ax * this.size - CENTRE.x, 0, (ay + 1) * this.size - CENTRE.y);
        obj.traverse((o) => {
          const mesh = o as THREE.Mesh;
          if (!mesh.isMesh) return;
          const name = ((mesh.material as THREE.Material).name || "paint").split(".")[0];
          if (!this.materials.has(name)) this.materials.set(name, makeMaterial(name));
          mesh.material = this.materials.get(name)!;
          mesh.castShadow = det === "full";
          mesh.receiveShadow = true;
        });
        this.group.add(obj);
        this.loaded.set(k, { detail: det, obj });
        const ms = this.massing.get(k);
        if (ms) ms.visible = false;
      }, undefined, () => this.loaded.delete(k));
    }
  }

  private ring(k: string, tx: number, ty: number) {
    const [a, b] = k.split("_").map(Number);
    return Math.max(Math.abs(a - tx), Math.abs(b - ty));
  }
}
