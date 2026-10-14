// Gidi's world for the Mock: the city data (web/gidi-data.js) in the sim's frame (metres, x east,
// z south, centred on the map), building footprints for collisions, estate walls as barriers,
// the lane network baked by tools/roadnet, the lagoon and ocean, and a far-field massing of every
// building so the skyline is there before the detailed tiles stream in (tiles.ts).
// Same interface the Real-world modules expect from their World (drive.ts, traffic.ts).
import * as THREE from "three/webgpu";
import { RoadNet } from "./roadnet";

export interface Road {
  cls: number;
  w: number;
  speed: number;
  name: number;
  pts: Float32Array;
}

export interface GidiData {
  size: number[];
  water: number[][][];
  ocean: number[][][];
  buildings: Record<string, (string | number[])[][]>;
  storeys: Record<string, number[]>;
  walls?: Record<string, number[][][]>;
  pois: { name: string; type: string; d: string; x: number; y: number; note?: string }[];
  districts: { id: string; name: string; poly: number[][][] }[];
}

export const CENTRE = { x: 4400, y: 3360 };
export const toSim = (x: number, y: number) => ({ x: x - CENTRE.x, z: y - CENTRE.y });

export function pointInPoly(p: Float32Array, x: number, z: number): boolean {
  let inside = false;
  const n = p.length / 2;
  for (let i = 0, j = n - 1; i < n; j = i++) {
    const xi = p[i * 2], zi = p[i * 2 + 1], xj = p[j * 2], zj = p[j * 2 + 1];
    if (zi > z !== zj > z && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) inside = !inside;
  }
  return inside;
}

export class World {
  group = new THREE.Group();
  data!: GidiData;
  meta = { half: { x: CENTRE.x, z: CENTRE.y }, names: [] as string[] };
  footprintList: Float32Array[] = [];
  storeys: number[] = [];
  net: RoadNet | null = null;
  city = { drive: "right" as const, lagosLife: true };
  roads: Road[] = [];
  private walls: number[] = [];
  massingByTile = new Map<string, THREE.Object3D>();

  async load(base: string) {
    const src = await fetch(`${base}web/gidi-data.js`).then((r) => r.text());
    this.data = JSON.parse(src.slice(src.indexOf("{"), src.lastIndexOf("}") + 1));
    for (const [d, list] of Object.entries(this.data.buildings)) {
      const st = this.data.storeys[d] ?? [];
      list.forEach((b, i) => {
        const pts = b.slice(1) as number[][];
        const f = new Float32Array(pts.length * 2);
        pts.forEach((p, k) => {
          const s = toSim(p[0], p[1]);
          f[k * 2] = s.x;
          f[k * 2 + 1] = s.z;
        });
        this.footprintList.push(f);
        this.storeys.push(st[i] ?? 1);
      });
    }
    for (const segs of Object.values(this.data.walls ?? {})) {
      for (const w of segs) {
        for (let k = 0; k + 1 < w.length; k++) {
          const a = toSim(w[k][0], w[k][1]), b = toSim(w[k + 1][0], w[k + 1][1]);
          this.walls.push(a.x, a.z, b.x, b.z, 2.8, 0.25);
        }
      }
    }
    this.net = await RoadNet.load("gidi", `${base}web/city/net/`);
    this.buildWater();
    this.buildMassing();
  }

  /** No garden walls of its own: compound walls are part of each building's tile model. */
  gardenColliders(_i: number): number[] {
    return [];
  }

  /** Estate walls as colliders: flat [ax, az, bx, bz, height, thickness, ...]. */
  barrierColliders(): number[] {
    return this.walls;
  }

  private buildWater() {
    const mat = new THREE.MeshStandardNodeMaterial({ color: 0x2f4a50, roughness: 0.08, metalness: 0.1 });
    for (const poly of [...this.data.water, ...this.data.ocean]) {
      const shape = new THREE.Shape(poly.map((p) => { const s = toSim(p[0], p[1]); return new THREE.Vector2(s.x, -s.z); }));
      const g = new THREE.ShapeGeometry(shape).rotateX(-Math.PI / 2);
      const m = new THREE.Mesh(g, mat);
      m.position.y = 0.02;
      m.receiveShadow = true;
      this.group.add(m);
    }
    // the land under everything, red earth
    const land = new THREE.Mesh(new THREE.PlaneGeometry(this.meta.half.x * 2 + 4000, this.meta.half.z * 2 + 4000).rotateX(-Math.PI / 2), new THREE.MeshStandardNodeMaterial({ color: 0x9a6a48, roughness: 1 }));
    land.position.y = -0.05;
    land.receiveShadow = true;
    this.group.add(land);
  }

  /** Every building as a coloured extruded block, one mesh per 400 m tile: what you see beyond the
   *  streamed tiles (tiles.ts hides a tile's blocks once its real model has loaded). */
  private buildMassing(size = 400) {
    const buckets = new Map<string, { pos: number[]; col: number[] }>();
    const c = new THREE.Color();
    const pal = [0xefe2c4, 0xf3c9a0, 0xbcd9e6, 0xc8e3c0, 0xf0d27a, 0xf4f1ea, 0xe9b3ad];
    this.footprintList.forEach((f, i) => {
      const h = this.storeys[i] * 3.1;
      const n = f.length / 2;
      let cx = 0, cz = 0;
      for (let k = 0; k < n; k++) { cx += f[k * 2]; cz += f[k * 2 + 1]; }
      const key = `${Math.floor((cx / n + CENTRE.x) / size)}_${Math.floor((cz / n + CENTRE.y) / size)}`;
      if (!buckets.has(key)) buckets.set(key, { pos: [], col: [] });
      const { pos, col } = buckets.get(key)!;
      c.setHex(pal[i % pal.length]);
      const push = (x: number, y: number, z: number, k = 1) => { pos.push(x, y, z); col.push(c.r * k, c.g * k, c.b * k); };
      for (let k = 0; k < n; k++) {
        const ax = f[k * 2], az = f[k * 2 + 1], bx = f[((k + 1) % n) * 2], bz = f[((k + 1) % n) * 2 + 1];
        push(ax, 0, az, 0.8); push(bx, 0, bz, 0.8); push(bx, h, bz);
        push(ax, 0, az, 0.8); push(bx, h, bz); push(ax, h, az);
      }
      for (let k = 1; k + 1 < n; k++) {
        push(f[0], h, f[1], 0.7); push(f[(k + 1) * 2], h, f[(k + 1) * 2 + 1], 0.7); push(f[k * 2], h, f[k * 2 + 1], 0.7);
      }
    });
    const mat = new THREE.MeshStandardNodeMaterial({ vertexColors: true, roughness: 0.9, side: THREE.DoubleSide });
    for (const [key, { pos, col }] of buckets) {
      const g = new THREE.BufferGeometry();
      g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
      g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
      g.computeVertexNormals();
      const m = new THREE.Mesh(g, mat);
      this.massingByTile.set(key, m);
      this.group.add(m);
    }
  }

  /** Where the player starts: a named place (POI), else the middle of the Maze. */
  spawn(name?: string | null): { x: number; z: number; yaw: number } {
    const poi = this.data.pois.find((p) => name && p.name.toLowerCase().includes(name.toLowerCase())) ?? this.data.pois.find((p) => p.name === "Ladi Lane Parts Market");
    return poi ? this.spawnAt(poi.x, poi.y) : this.spawnAt(CENTRE.x, CENTRE.y);
  }

  /** Start on the car lane nearest a point given in map metres (x east, y south). */
  spawnAt(gx: number, gy: number): { x: number; z: number; yaw: number } {
    const s = toSim(gx, gy);
    // stand on the nearest car lane, facing along it
    let best: { x: number; z: number; yaw: number; d: number } | null = null;
    for (const l of this.net?.lanes ?? []) {
      if (!(l.allow & 1) || l.kind !== 0) continue;
      for (let k = 0; k + 1 < l.cum.length; k++) {
        const ax = l.pts[k * 2], az = l.pts[k * 2 + 1], bx = l.pts[k * 2 + 2], bz = l.pts[k * 2 + 3];
        const d = Math.hypot((ax + bx) / 2 - s.x, (az + bz) / 2 - s.z);
        if (!best || d < best.d) best = { x: (ax + bx) / 2, z: (az + bz) / 2, yaw: Math.atan2(bx - ax, bz - az), d };
      }
    }
    return best ? { x: best.x, z: best.z, yaw: best.yaw } : { x: s.x, z: s.z, yaw: 0 };
  }

  districtAt(x: number, z: number): string | null {
    const gx = x + CENTRE.x, gy = z + CENTRE.y;
    for (const d of this.data.districts) {
      const poly = d.poly[0];
      let ins = false;
      for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
        const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
        if (yi > gy !== yj > gy && gx < ((xj - xi) * (gy - yi)) / (yj - yi) + xi) ins = !ins;
      }
      if (ins) return d.name;
    }
    return null;
  }
}
