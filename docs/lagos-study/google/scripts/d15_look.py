"""Re-runs the scripted figures of docs/lagos-study/google/d15.md (the Google look for Mùṣá, 28 Oct).

The agent that wrote the note used scratch scripts; this one, written by the main session, re-computes from the map
files every view's Gidi x,y, whether it is inside the d15 outline, and the "Ours (r30)" column: our buildings whose
footprint centroid lies within 30 m (Gidi) of the view's point, their kinds, median footprint, and cover (footprint
area clipped to the circle, over the circle's area).

    ~/.venvs/gidi/bin/python -I docs/lagos-study/google/scripts/d15_look.py
"""
import json
import re
import statistics
from collections import Counter
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import Point, Polygon

ROOT = Path(__file__).resolve().parents[4]
NOTE = ROOT / "docs/lagos-study/google/d15.md"
plan = json.loads((ROOT / "map/d15/plan.json").read_text())
district = json.loads((ROOT / "map/d15/district.json").read_text())
outline = Polygon(district["records"][0]["outline"][0])
to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32631", always_xy=True)


def gidi(lat, lon):
    e, n = to_utm.transform(lon, lat)
    return (e - 500525) / 3, 10500 - (n - 707825) / 3


houses = []
for r in plan["records"]:
    if r.get("type") == "building" and r.get("footprint"):
        p = Polygon(r["footprint"])
        if p.is_valid and p.area > 0:
            houses.append((p, r))

print(f"outline area {outline.area:,.0f} m2, bounds {[round(v) for v in outline.bounds]}")
rows = re.findall(r"^\| (S\d+\w?) \| ([^|]+) \| ([\d.]+),([\d.]+) \| (\d+),(\d+) \|", NOTE.read_text(), re.M)
for sid, name, lat, lon, nx, ny in rows:
    x, y = gidi(float(lat), float(lon))
    c = Point(x, y).buffer(30, 64)
    near = [(p, r) for p, r in houses if c.contains(p.centroid)]
    cover = sum(p.intersection(c).area for p, _ in houses if p.intersects(c)) / c.area
    kinds = Counter(r["kind"] for _, r in near)
    med = statistics.median(p.area for p, _ in near) if near else 0
    storeys = Counter(r.get("storeys") for _, r in near)
    print(f"{sid:5} {name.strip()[:28]:28} note {nx},{ny} ours {x:.0f},{y:.0f} d={((x-int(nx))**2+(y-int(ny))**2)**.5:.0f} "
          f"inside={outline.contains(Point(x, y))} n={len(near)} cover={cover:.0%} median={med:.0f} "
          f"storeys={dict(storeys)} kinds={dict(kinds)}")

# The Matori estate stream, which the note says lies 76-83 m outside the outline.
for lat, lon in [(6.5415, 3.3500), (6.5406, 3.3505)]:
    x, y = gidi(lat, lon)
    print(f"Matori stream {lat},{lon}: {x:.0f},{y:.0f} inside={outline.contains(Point(x, y))} "
          f"distance to outline {outline.exterior.distance(Point(x, y)):.0f} m (Gidi)")
