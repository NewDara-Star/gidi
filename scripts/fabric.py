# Side-by-side 1 km tiles: densest real squares in the inspiration LGAs vs the Gidi district. Block sizes from the noded network.
import pickle, json, sys, math, statistics
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from shapely.geometry import box, LineString, Polygon, Point
from shapely.ops import unary_union, polygonize
from shapely.strtree import STRtree
DID=sys.argv[1]; R=pickle.load(open(f"real-{DID}.pkl","rb"))
DRIVE={"primary","secondary","tertiary","unclassified","residential","living_street","primary_link","secondary_link","tertiary_link","trunk","motorway"}
lines=[]; cls=[]
for h,g in R["roads"]:
    for p in getattr(g,"geoms",[g]):
        if p.geom_type=="LineString": lines.append(p); cls.append(h)
tree=STRtree(lines)
minx,miny,maxx,maxy=R["area"].bounds
def density(b):
    return sum(lines[i].intersection(b).length for i in tree.query(b) if cls[i] in DRIVE)
best=[]
for x in range(int(minx),int(maxx)-1000,250):
    for y in range(int(miny),int(maxy)-1000,250):
        b=box(x,y,x+1000,y+1000)
        if R["area"].contains(b): best.append((density(b),b))
best.sort(key=lambda t:-t[0])
picks=[best[0][1]]
for dval,b in best[1:]:
    if all(b.centroid.distance(p.centroid)>2500 for p in picks): picks.append(b)
    if len(picks)==2: break
def stats(segs,b):
    net=unary_union([s for s in segs]).intersection(b)
    blocks=[p for p in polygonize(unary_union([net,b.exterior])) if p.area>200]
    inner=[p.area for p in blocks if not p.touches(b.exterior) and p.within(b.buffer(-1))]
    nodes={}
    for part in getattr(net,"geoms",[net]):
        if part.geom_type!="LineString": continue
        for c in (part.coords[0],part.coords[-1]):
            k=(round(c[0],1),round(c[1],1)); nodes[k]=nodes.get(k,0)+1
    return dict(km=round(net.length/1000,1), intersections=sum(1 for v in nodes.values() if v>=3),
                deadends=sum(1 for v in nodes.values() if v==1), median_block_m2=round(statistics.median(inner)) if inner else None, blocks=len(inner))
tiles=[]
for i,b in enumerate(picks):
    segs=[lines[j].intersection(b) for j in tree.query(b) if cls[j] in DRIVE]
    segs=[s for s in segs if not s.is_empty]
    tiles.append(("Real "+["Mushin/Shomolu densest square","second densest square"][i],b,[(cls[j],lines[j].intersection(b)) for j in tree.query(b) if cls[j] in DRIVE],stats(segs,b)))
s=open("web/gidi-data.js").read(); G=json.loads(s[len("window.GIDI="):-1])
d={x["id"]:x for x in G["districts"]}[DID]; poly=Polygon(d["poly"][0]); c=poly.centroid
gb=box(c.x-500,c.y-500,c.x+500,c.y+500)
gsegs=[("residential",LineString(l).intersection(gb)) for l in G["streets"][DID]]+[("secondary",LineString(m["pts"]).intersection(gb)) for m in G["mains"] if m["d"]==DID]
gsegs=[(h,g) for h,g in gsegs if not g.is_empty]
tiles.append(("Gidi: the Maze (current)",gb,gsegs,stats([g for _,g in gsegs],gb)))
W={"primary":3.2,"trunk":3.2,"secondary":2.4,"tertiary":1.8,"residential":0.9,"unclassified":0.9,"living_street":0.8}
fig,axs=plt.subplots(1,len(tiles),figsize=(6.2*len(tiles),7.2),dpi=110); fig.patch.set_facecolor("#f4f2ed")
for ax,(title,b,segs,st) in zip(axs,tiles):
    ax.set_facecolor("#ebe7df")
    for h,g in segs:
        for p in getattr(g,"geoms",[g]):
            if p.geom_type=="LineString": ax.plot(*p.xy,color="#e8a23a" if W.get(h,0.9)>1.5 else "#55524c",lw=W.get(h.replace("_link",""),0.9),solid_capstyle="round")
    x0,y0,x1,y1=b.bounds; ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#c9c3b6")
    ax.set_title(title,fontsize=13,weight="bold",color="#222",loc="left")
    ax.text(0,-0.075,f"{st['km']} km of road · {st['intersections']} junctions · {st['deadends']} dead ends\nmedian block {st['median_block_m2']:,} m² ({st['blocks']} whole blocks)",transform=ax.transAxes,fontsize=10.5,color="#333",va="top")
fig.suptitle("Street fabric, 1 km × 1 km at the same scale. Real data © OpenStreetMap contributors (ODbL).",fontsize=12,color="#555",y=0.995)
plt.tight_layout(); plt.savefig(f"fabric-{DID}.png",facecolor=fig.get_facecolor(),bbox_inches="tight")
print([ (t[0],t[3]) for t in tiles]); print([p.centroid.coords[0] for p in picks])
