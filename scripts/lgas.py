# Lagos's 20 LGAs from OSM admin_level=6 boundaries (ODbL), assembled leniently, drawn over the study map's water and main roads.
import osmium, shapely.wkb as wl, pickle, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from shapely.ops import polygonize, unary_union
LAGOS={"Agege","Ajeromi/Ifelodun","Alimosho","Amuwo Odofin","Apapa","Badagry","Epe","Eti Osa","Ibeju Lekki","Ifako/Ijaiye","Ikeja","Kosofe","Lagos Island","Lagos Mainland","Mushin","Ojo","Oshodi/Isolo","Shomolu","Surulere","Ìkòròdú"}
GROUP={"Lagos Island":"Island","Eti Osa":"Island","Ibeju Lekki":"Island","Epe":"Island",
 "Lagos Mainland":"Inner","Surulere":"Inner","Mushin":"Inner","Shomolu":"Inner","Oshodi/Isolo":"Inner","Apapa":"Inner","Ajeromi/Ifelodun":"Inner"}
COL={"Island":"#c9a227","Inner":"#d9653b","Outer":"#5b8fb9"}
rel={}; f=osmium.geom.WKBFactory(); ways={}
class R(osmium.SimpleHandler):
    def relation(s,r):
        t=r.tags
        if t.get("boundary")=="administrative" and t.get("admin_level")=="6" and t.get("name") in LAGOS:
            rel[t["name"]]=[(m.ref,m.role) for m in r.members if m.type=="w"]
R().apply_file("../raw/nigeria.osm.pbf")
need={w for v in rel.values() for w,_ in v}
class W(osmium.SimpleHandler):
    def way(s,w):
        if w.id in need:
            try: ways[w.id]=wl.loads(f.create_linestring(w),hex=True)
            except Exception: pass
W().apply_file("../raw/nigeria.osm.pbf",locations=True)
polys={}
for n,ms in rel.items():
    ls=[ways[w] for w,r in ms if w in ways and r!="inner"]
    p=unary_union(list(polygonize(unary_union(ls))))
    polys[n]=p; print(n, round(p.area*12321,1),"km2 approx")
pickle.dump(polys,open("lgas.pkl","wb"))
