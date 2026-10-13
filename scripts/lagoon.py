# Assemble Lagos Lagoon (OSM relation 2116203) leniently with shapely, since osmium refuses its geometry.
import osmium, shapely.wkb as wkblib, pickle, sys
from shapely.ops import linemerge, polygonize, unary_union
wkbf=osmium.geom.WKBFactory(); roles={}; geoms={}
class R(osmium.SimpleHandler):
    def relation(s,r):
        if r.id==2116203:
            for m in r.members:
                if m.type=="w": roles[m.ref]=m.role
R().apply_file(sys.argv[1])
class W(osmium.SimpleHandler):
    def way(s,w):
        if w.id in roles:
            try: geoms[w.id]=wkblib.loads(wkbf.create_linestring(w),hex=True)
            except Exception as e: print("bad",w.id,e)
W().apply_file(sys.argv[1],locations=True)
outer=[g for i,g in geoms.items() if roles[i]!="inner"]; inner=[g for i,g in geoms.items() if roles[i]=="inner"]
m=linemerge(outer); po=list(polygonize(unary_union(outer)))
pi=list(polygonize(unary_union(inner)))
print("outer",len(outer),"inner",len(inner),"outer polys",len(po),"area",sum(p.area for p in po),"inner polys",len(pi))
ends=[]
for g in getattr(m,"geoms",[m]):
    if not g.is_ring: ends.append((g.coords[0],g.coords[-1]))
print("open chains",len(ends), ends[:4])
lag=unary_union(po).difference(unary_union(pi)) if po else None
pickle.dump(lag,open(sys.argv[2],"wb"))
