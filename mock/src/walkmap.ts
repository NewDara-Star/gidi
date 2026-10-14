// The walk map (tools/walkmap/bake_walk.py): what each square metre of Gidi is, streamed in 400 m
// tiles round the player. The player stops where it's blocked or water (and slides along walls);
// the minimap (M) shows it. Classes match the baker.
import { CENTRE } from "./world";

export const enum Walk { Block = 0, Ground = 1, Foot = 2, Road = 3, Deck = 4, FootDeck = 5, Water = 6 }

const SIZE = 400;
const COLOURS = ["#262626", "#b07850", "#e6dcbe", "#5a5a5f", "#ffc800", "#ff78c8", "#285a8c"];

export class WalkMap {
  private tiles = new Map<string, Uint8Array | "loading" | null>();

  constructor(private base: string) {}

  /** The class at a sim point; Ground while its tile is still loading (never trap anyone). */
  at(x: number, z: number): Walk {
    const gx = Math.floor(x + CENTRE.x), gy = Math.floor(z + CENTRE.y);
    const tx = Math.floor(gx / SIZE), ty = Math.floor(gy / SIZE);
    const t = this.tile(tx, ty);
    if (t === null) return Walk.Block; // off the map
    if (t === "loading") return Walk.Ground;
    return t[(gy - ty * SIZE) * SIZE + (gx - tx * SIZE)] as Walk;
  }

  /** Can someone on foot stand here? Roads too: people do walk in the road. */
  walkable(x: number, z: number) {
    const c = this.at(x, z);
    return c !== Walk.Block && c !== Walk.Water;
  }

  private tile(tx: number, ty: number) {
    const k = `${tx}_${ty}`;
    const have = this.tiles.get(k);
    if (have !== undefined) return have;
    if (tx < 0 || ty < 0) {
      this.tiles.set(k, null);
      return null;
    }
    this.tiles.set(k, "loading");
    fetch(`${this.base}web/city/walk/${k}.png`)
      .then((r) => (r.ok ? r.blob() : Promise.reject()))
      .then((b) => createImageBitmap(b, { colorSpaceConversion: "none", premultiplyAlpha: "none" }))
      .then((bmp) => {
        const c = new OffscreenCanvas(SIZE, SIZE);
        const g = c.getContext("2d", { willReadFrequently: true })!;
        g.drawImage(bmp, 0, 0);
        const rgba = g.getImageData(0, 0, SIZE, SIZE).data;
        const a = new Uint8Array(SIZE * SIZE);
        for (let i = 0; i < a.length; i++) a[i] = rgba[i * 4];
        this.tiles.set(k, a);
      })
      .catch(() => this.tiles.set(k, null)); // no walk map baked: off the map or not built
    return "loading" as const;
  }

  /** Draw the map round (x, z) into a canvas, north up, the player in the middle facing yaw. */
  draw(cv: HTMLCanvasElement, x: number, z: number, yaw: number, metres = 240) {
    const g = cv.getContext("2d")!;
    const n = cv.width, step = metres / n;
    const img = g.createImageData(n, n);
    const rgb = COLOURS.map((h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]);
    for (let j = 0; j < n; j++) {
      for (let i = 0; i < n; i++) {
        const c = rgb[this.at(x + (i - n / 2) * step, z + (j - n / 2) * step)] ?? rgb[0];
        const o = (j * n + i) * 4;
        img.data[o] = c[0]; img.data[o + 1] = c[1]; img.data[o + 2] = c[2]; img.data[o + 3] = 255;
      }
    }
    g.putImageData(img, 0, 0);
    g.save();
    g.translate(n / 2, n / 2);
    g.rotate(-yaw);
    g.fillStyle = "#ff3030";
    g.beginPath();
    g.moveTo(0, 7); g.lineTo(-4, -4); g.lineTo(4, -4);
    g.closePath();
    g.fill();
    g.restore();
  }
}
