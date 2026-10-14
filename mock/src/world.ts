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

/** Districts not built out yet: walled off with hoarding until they are (README, district status). */
export const UNBUILT = new Set(["border", "oldshore", "frontier"]);

/** How busy the streets are, 0..1, from each district's people per km² (docs/lagos-lgas-research.md):
 * the ~80,000/km² markets and ghettos are 1, the GRAs and Ikoyi-like estates a handful of walkers. */
export const DENSITY: Record<string, number> = {
  jungle: 1.0, maze: 0.95, hub: 1.0, oldisland: 1.0, bazaar: 0.9, watertown: 0.85, foodgate: 0.85,
  railside: 0.6, capital: 0.55, port: 0.45, heights: 0.2, estate: 0.15,
  border: 0, oldshore: 0, frontier: 0,
};
/** Places that pull a crowd round them, metres of reach and the boost. */
const CROWD_POIS: Record<string, [number, number]> = {
  market: [220, 0.6], transit: [180, 0.6], church: [60, 0.25], mosque: [60, 0.25], school: [70, 0.3],
  sport: [150, 0.4], night: [80, 0.3], hospital: [90, 0.3], betting: [40, 0.15], landmark: [100, 0.2],
};

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
    this.buildHoarding();
    await this.monumentColliders(base);
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

  /** Corrugated hoarding round each unbuilt district, the kind that fences off a Lagos building site,
   * and a solid wall behind it for the car's physics. */
  private buildHoarding() {
    const segs: number[] = [];
    for (const d of this.data.districts) {
      if (!UNBUILT.has(d.id)) continue;
      const poly = d.poly[0];
      for (let k = 0; k + 1 < poly.length; k++) {
        const a = toSim(poly[k][0], poly[k][1]), b = toSim(poly[k + 1][0], poly[k + 1][1]);
        const len = Math.hypot(b.x - a.x, b.z - a.z);
        const n = Math.max(1, Math.ceil(len / 40)); // keep each panel straight on long edges
        for (let i = 0; i < n; i++) {
          const t0 = i / n, t1 = (i + 1) / n;
          segs.push(a.x + (b.x - a.x) * t0, a.z + (b.z - a.z) * t0, a.x + (b.x - a.x) * t1, a.z + (b.z - a.z) * t1);
        }
      }
    }
    const n = segs.length / 4;
    if (!n) return;
    const H = 3.2;
    const mesh = new THREE.InstancedMesh(new THREE.BoxGeometry(1, H, 0.12).translate(0, H / 2, 0), new THREE.MeshStandardNodeMaterial({ color: 0xb2b8b8, roughness: 0.45, metalness: 0.5 }), n);
    const band = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.5, 0.16).translate(0, H - 0.6, 0), new THREE.MeshStandardNodeMaterial({ color: 0x1f5fa8, roughness: 0.6 }), n);
    const m = new THREE.Matrix4(), q = new THREE.Quaternion(), up = new THREE.Vector3(0, 1, 0);
    for (let i = 0; i < n; i++) {
      const [ax, az, bx, bz] = segs.slice(i * 4, i * 4 + 4);
      const len = Math.hypot(bx - ax, bz - az);
      q.setFromAxisAngle(up, Math.atan2(-(bz - az), bx - ax));
      m.compose(new THREE.Vector3((ax + bx) / 2, 0, (az + bz) / 2), q, new THREE.Vector3(len, 1, 1));
      mesh.setMatrixAt(i, m);
      band.setMatrixAt(i, m);
      this.walls.push(ax, az, bx, bz, H, 0.4);
    }
    mesh.castShadow = mesh.receiveShadow = true;
    this.group.add(mesh, band);
  }

  /** Statues, clock towers, screens, arch pylons and the lighthouse (web/city/monuments.json,
   * blender/city.py monument_sites) as solid posts for the car and for walking. */
  private async monumentColliders(base: string) {
    let sites: { kind: string; x: number; y: number; ang: number; r?: number; span?: number }[] = [];
    try {
      sites = await fetch(`${base}web/city/monuments.json`).then((r) => r.json());
    } catch {
      return;
    }
    const square = (cx: number, cz: number, r: number) => {
      const f = new Float32Array([cx - r, cz - r, cx + r, cz - r, cx + r, cz + r, cx - r, cz + r]);
      this.footprintList.push(f);
      this.storeys.push(1);
    };
    for (const m of sites) {
      const s = toSim(m.x, m.y);
      if (m.kind === "arch") {
        const h = (m.span ?? 16) / 2 + 1.2, nx = -Math.sin(m.ang), nz = -Math.cos(m.ang); // ang is in Blender's frame (y north)
        for (const sg of [-1, 1]) square(s.x + nx * h * sg, s.z + nz * h * sg, 1.0);
      } else square(s.x, s.z, m.r ?? 2);
    }
  }

  /** The district's id at a point, or null outside them all. */
  districtIdAt(x: number, z: number): string | null {
    return this.districtWhere(x, z)?.id ?? null;
  }

  /** True where the player may not go yet (an unbuilt district). */
  blocked(x: number, z: number) {
    const id = this.districtIdAt(x, z);
    return id !== null && UNBUILT.has(id);
  }

  /** Street crowd at a point, 0..1+: the district's density, lifted near markets, parks, stations,
   * churches and mosques. */
  crowdAt(x: number, z: number) {
    const gx = Math.round(x / 40), gz = Math.round(z / 40), key = gx * 100000 + gz;
    let v = this.crowdCache.get(key);
    if (v === undefined) this.crowdCache.set(key, (v = this.crowdAtRaw(gx * 40, gz * 40)));
    return v;
  }
  private crowdCache = new Map<number, number>();

  private crowdAtRaw(x: number, z: number) {
    const id = this.districtIdAt(x, z);
    let d = id === null ? 0.1 : DENSITY[id] ?? 0.5;
    if (d === 0) return 0;
    const gx = x + CENTRE.x, gy = z + CENTRE.y;
    for (const p of this.data.pois) {
      const c = CROWD_POIS[p.type];
      if (!c) continue;
      const r = Math.hypot(p.x - gx, p.y - gy);
      if (r < c[0]) d += c[1] * (1 - r / c[0]);
    }
    return d;
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
    return this.districtWhere(x, z)?.name ?? null;
  }

  private districtWhere(x: number, z: number) {
    const gx = x + CENTRE.x, gy = z + CENTRE.y;
    for (const d of this.data.districts) {
      const poly = d.poly[0];
      let ins = false;
      for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
        const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
        if (yi > gy !== yj > gy && gx < ((xj - xi) * (gy - yi)) / (yj - yi) + xi) ins = !ins;
      }
      if (ins) return d;
    }
    return null;
  }
}
