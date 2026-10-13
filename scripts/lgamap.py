# Map of Lagos State's 20 LGAs (OSM admin_level=6, ODbL), coloured by zone, with lagoon/sea and main roads.
import json, pickle, matplotlib, osmium, shapely.wkb as wl
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from shapely.geometry import shape
NAMES={"Agege":"Agege","Ajeromi/Ifelodun":"Ajeromi-\nIfelodun","Alimosho":"Alimosho","Amuwo Odofin":"Amuwo-Odofin","Apapa":"Apapa","Badagry":"Badagry","Epe":"Epe","Eti Osa":"Eti-Osa","Ibeju Lekki":"Ibeju-Lekki","Ifako/Ijaye":"Ifako-\nIjaiye","Ikeja":"Ikeja","Kosofe":"Kosofe","Lagos Island":"Lagos\nIsland","Lagos Mainland":"Lagos\nMainland","Mushin":"Mushin","Ojo":"Ojo","Oshodi/Isolo":"Oshodi-\nIsolo","Shomolu":"Shomolu","Surulere":"Surulere","Ìkòròdú":"Ikorodu"}
ZONE={"Lagos Island":0,"Eti Osa":0,"Ibeju Lekki":0,"Epe":0,"Lagos Mainland":1,"Surulere":1,"Mushin":1,"Shomolu":1,"Oshodi/Isolo":1,"Apapa":1,"Ajeromi/Ifelodun":1}
ZC=["#c9a227","#d9653b","#5b8fb9"]; ZN=["Island side","Inner mainland","Outer mainland"]
d=json.load(open("adm6.geojson")); lg={}
for ft in d["features"]:
    n=ft["properties"].get("name")
    if ft["properties"].get("admin_level")=="6" and n in NAMES:
        g=shape(ft["geometry"]); c=g.representative_point()
        if 2.6<c.x<4.4 and 6.3<c.y<6.75: lg[n]=g  # skip same-named LGAs elsewhere in Nigeria
water=[pickle.load(open("lagoon.pkl","rb"))]
roads=[]; fct=osmium.geom.WKBFactory()
class H(osmium.SimpleHandler):
    def way(s,w):
        if w.tags.get("highway") in ("motorway","trunk","primary"):
            try: roads.append((w.tags["highway"],wl.loads(fct.create_linestring(w),hex=True)))
            except Exception: pass
H().apply_file("lagos.osm.pbf",locations=True)
def draw(bbox,fname,small=False,sp=0.035):
    fig,ax=plt.subplots(figsize=(26,26*(bbox[3]-bbox[1])/(bbox[2]-bbox[0])),dpi=100)
    fig.patch.set_facecolor("#16181b"); ax.add_patch(plt.Rectangle((bbox[0],bbox[1]),bbox[2]-bbox[0],bbox[3]-bbox[1],fc="#1f4459",zorder=0))
    for n,g in lg.items():
        z=ZONE.get(n,2)
        for p in getattr(g,"geoms",[g]):
            ax.fill(*p.exterior.xy,fc=ZC[z],alpha=0.30,ec=ZC[z],lw=1.6,zorder=1)
    for g in water:
        for p in getattr(g,"geoms",[g]): ax.fill(*p.exterior.xy,fc="#1f4459",lw=0,zorder=2)
    for h,g in roads:
        ax.plot(*g.xy,color="#f2e3c0",lw=1.6 if h!="primary" else 0.8,alpha=0.75,zorder=3)
    for n,g in lg.items():
        land=g.difference(water[0]); c=(land if not land.is_empty else g).representative_point()
        if bbox[0]<c.x<bbox[2] and bbox[1]<c.y<bbox[3]:
            ax.text(c.x,c.y,NAMES[n],color="#ffffff",fontsize=15 if not small else 13,ha="center",va="center",weight="bold",zorder=5,
                    bbox=dict(boxstyle="round,pad=0.2",fc="#16181b",ec="none",alpha=0.6))
    for i in range(3):
        ax.add_patch(plt.Rectangle((bbox[0]+0.01*(bbox[2]-bbox[0]),bbox[3]-(0.05+sp*i)*(bbox[3]-bbox[1])),0.015*(bbox[2]-bbox[0]),(0.06 if sp>0.05 else 0.022)*(bbox[3]-bbox[1]),fc=ZC[i],alpha=0.8,zorder=6))
        ax.text(bbox[0]+0.03*(bbox[2]-bbox[0]),bbox[3]-(0.04+sp*i)*(bbox[3]-bbox[1]),ZN[i],color="white",fontsize=15,va="center",zorder=6)
    ax.text(bbox[0]+0.01*(bbox[2]-bbox[0]),bbox[1]+0.015*(bbox[3]-bbox[1]),"Lagos State's 20 local government areas. Boundaries and roads © OpenStreetMap contributors (ODbL).",color="#bbb",fontsize=12,zorder=6)
    ax.set_xlim(bbox[0],bbox[2]); ax.set_ylim(bbox[1],bbox[3]); ax.set_aspect(1/0.9935); ax.axis("off")
    plt.savefig(fname,bbox_inches="tight",pad_inches=0.05,facecolor=fig.get_facecolor()); plt.close()
xs=[g.bounds for g in lg.values()]
full=[min(b[0] for b in xs)-0.02,min(b[1] for b in xs)-0.02,max(b[2] for b in xs)+0.02,max(b[3] for b in xs)+0.02]
print(full)
draw(full,"lagos-lgas-state.png",sp=0.1)
draw([3.22,6.40,3.62,6.70],"lagos-lgas-core.png",True)
