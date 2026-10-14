// Visible traffic lights for Gidi's signalised junctions: a galvanised pole and a three-aspect head
// at the end of every signalled approach lane, lit from the same signal program and clock the AI
// traffic obeys (RoadNet.signalState). Lagos-style: plain grey pole, black head, often a solar panel
// on top (docs/look/research-street.md 2.4). Only heads near the player are updated.
import * as THREE from "three/webgpu";
import type { RoadNet } from "./roadnet";

interface Head { x: number; z: number; tl: number; li: number; lamps: THREE.Mesh[] }

export class Signals {
  group = new THREE.Group();
  private heads: Head[] = [];
  private on = [new THREE.Color(3, 0.15, 0.1), new THREE.Color(3, 2.0, 0.1), new THREE.Color(0.2, 3, 0.6)];
  private off = new THREE.Color(0.08, 0.08, 0.08);

  constructor(private net: RoadNet) {
    const pole = new THREE.MeshStandardNodeMaterial({ color: 0x8a8f92, roughness: 0.5, metalness: 0.6 });
    const black = new THREE.MeshStandardNodeMaterial({ color: 0x151515, roughness: 0.6 });
    const panel = new THREE.MeshStandardNodeMaterial({ color: 0x1e2a44, roughness: 0.3, metalness: 0.4 });
    const poleG = new THREE.CylinderGeometry(0.07, 0.09, 4.2, 8).translate(0, 2.1, 0);
    const headG = new THREE.BoxGeometry(0.34, 1.0, 0.3).translate(0, 3.5, 0.12);
    const lampG = new THREE.CircleGeometry(0.1, 12);
    const panelG = new THREE.BoxGeometry(0.6, 0.03, 0.9).rotateX(-0.4).translate(0, 4.35, 0);
    const seen = new Set<string>();
    for (const k of net.links) {
      if (k.tl < 0) continue;
      const lane = net.lanes[k.from];
      if (!lane || lane.pts.length < 4) continue;
      const n = lane.pts.length;
      const ex = lane.pts[n - 2], ez = lane.pts[n - 1], px = lane.pts[n - 4], pz = lane.pts[n - 3];
      const dx = ex - px, dz = ez - pz, l = Math.hypot(dx, dz) || 1;
      // stand on the kerb side (right of travel), a little before the stop line
      const rx = -dz / l, rz = dx / l;
      const x = ex - (dx / l) * 1.0 - rx * (lane.width / 2 + 0.8), z = ez - (dz / l) * 1.0 - rz * (lane.width / 2 + 0.8);
      const key = `${Math.round(x / 3)}_${Math.round(z / 3)}`;
      if (seen.has(key)) continue;
      seen.add(key);
      const g = new THREE.Group();
      g.position.set(x, 0, z);
      g.rotation.y = Math.atan2(-dx, -dz); // the head faces the oncoming traffic
      g.add(new THREE.Mesh(poleG, pole), new THREE.Mesh(headG, black));
      if (Math.random() < 0.6) g.add(new THREE.Mesh(panelG, panel));
      const lamps: THREE.Mesh[] = [];
      for (let i = 0; i < 3; i++) {
        const m = new THREE.Mesh(lampG, new THREE.MeshBasicNodeMaterial({ color: this.off }));
        m.position.set(0, 3.82 - i * 0.31, 0.275);
        g.add(m);
        lamps.push(m);
      }
      this.group.add(g);
      this.heads.push({ x, z, tl: k.tl, li: k.li, lamps });
    }
  }

  update(time: number, px: number, pz: number) {
    for (const h of this.heads) {
      if (Math.abs(h.x - px) > 250 || Math.abs(h.z - pz) > 250) continue;
      const st = this.net.signalState(h.tl, h.li, time);
      // SUMO states: r/R red, y/Y amber, g/G/s green
      const i = st === "r" || st === "R" ? 0 : st === "y" || st === "Y" || st === "u" ? 1 : 2;
      h.lamps.forEach((m, k) => ((m.material as THREE.MeshBasicNodeMaterial).color = k === i ? this.on[i] : this.off));
    }
  }
}
