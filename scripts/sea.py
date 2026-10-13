# Build sea/lagoon polygons from OSM coastline (land on the left, water on the right, per OSM coastline convention).
import sys, osmium, shapely.wkb as wkblib, pickle
from shapely.geometry import box, LineString, Point
from shapely.ops import polygonize, unary_union, linemerge
wkbf=osmium.geom.WKBFactory(); bb=box(*[float(x) for x in sys.argv[2].split(",")])
lines=[]
class H(osmium.SimpleHandler):
    def way(s,w):
        if w.tags.get("natural")=="coastline":
            try: lines.append(wkblib.loads(wkbf.create_linestring(w),hex=True))
            except Exception: pass
H().apply_file(sys.argv[1],locations=True)
clipped=[l.intersection(bb) for l in lines]
segs=[]
for c in clipped:
    for g in getattr(c,"geoms",[c]):
        if g.geom_type=="LineString" and g.length>0: segs.append(g)
noded=unary_union(segs+[bb.exterior])
polys=list(polygonize(noded))
water=[]
for p in polys:
    votes=0
    for s in segs:
        if s.distance(p)>1e-9: continue
        cs=list(s.coords)
        for (x1,y1),(x2,y2) in zip(cs,cs[1:]):
            mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; L=(dx*dx+dy*dy)**.5
            if L==0: continue
            q=Point(mx+dy/L*1e-5, my-dx/L*1e-5)   # right-hand side
            r=Point(mx-dy/L*1e-5, my+dx/L*1e-5)
            if p.contains(q): votes+=1
            elif p.contains(r): votes-=1
    if votes>0: water.append(p)
print(len(lines),"coast ways",len(polys),"pieces",len(water),"water pieces")
pickle.dump(water,open(sys.argv[3],"wb"))
