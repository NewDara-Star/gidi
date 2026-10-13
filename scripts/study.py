# Lagos study map from OpenStreetMap (ODbL). Draws roads by class, rail, water, markets, bridges, place names.
import sys, json, osmium, shapely.wkb as wkblib, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import LineString
wkbf = osmium.geom.WKBFactory()
ROADS = {"motorway":(2.4,"#e8a23a"),"trunk":(2.0,"#e8a23a"),"primary":(1.4,"#f2c76e"),
         "secondary":(0.9,"#d9d2c2"),"tertiary":(0.6,"#b9b2a4"),"residential":(0.2,"#8f897d"),
         "unclassified":(0.2,"#8f897d")}
class H(osmium.SimpleHandler):
    def __init__(s):
        super().__init__(); s.roads={k:[] for k in ROADS}; s.rail=[]; s.water=[]; s.coast=[]
        s.places=[]; s.markets=[]; s.bridges=[]
    def node(s,n):
        t=n.tags
        if t.get("place") in ("suburb","town","city","neighbourhood","quarter","island") and "name" in t:
            s.places.append((n.location.lon,n.location.lat,t["name"],t["place"]))
        if t.get("amenity")=="marketplace" and "name" in t:
            s.markets.append((n.location.lon,n.location.lat,t["name"]))
    def way(s,w):
        t=w.tags; h=t.get("highway")
        try:
            if h in ROADS or (h and h.endswith("_link") and h[:-5] in ROADS):
                g=wkblib.loads(wkbf.create_linestring(w),hex=True); s.roads[h.replace("_link","")].append(g)
                if t.get("bridge")=="yes" and h in ("motorway","trunk","primary") and g.length>0.004:
                    s.bridges.append((g,t.get("name","")))
            elif t.get("railway") in ("rail","light_rail"):
                s.rail.append(wkblib.loads(wkbf.create_linestring(w),hex=True))
            elif t.get("natural")=="coastline":
                s.coast.append(wkblib.loads(wkbf.create_linestring(w),hex=True))
        except Exception: pass
    def area(s,a):
        t=a.tags
        try:
            if t.get("natural") in ("water","bay","strait") or t.get("water") or t.get("natural")=="wetland" and t.get("wetland")=="mangrove":
                s.water.append(wkblib.loads(wkbf.create_multipolygon(a),hex=True))
            if t.get("amenity")=="marketplace" and "name" in t:
                c=wkblib.loads(wkbf.create_multipolygon(a),hex=True).centroid; s.markets.append((c.x,c.y,t["name"]))
        except Exception: pass
h=H(); h.apply_file(sys.argv[1],locations=True)
bbox=[float(x) for x in sys.argv[3].split(",")]; minor=sys.argv[4]=="1"
fig,ax=plt.subplots(figsize=(30,30*(bbox[3]-bbox[1])/(bbox[2]-bbox[0])),dpi=110)
ax.set_facecolor("#1d1f22"); fig.patch.set_facecolor("#1d1f22")
for g in h.water:
    for p in getattr(g,"geoms",[g]):
        ax.fill(*p.exterior.xy,color="#23465c",lw=0)
import pickle,os
for f in ("lagoon.pkl","sea.pkl"):
    if os.path.exists(f):
        o=pickle.load(open(f,"rb")); o=o if isinstance(o,list) else [o]
        for g in o:
            for p in getattr(g,"geoms",[g]): ax.fill(*p.exterior.xy,color="#23465c",lw=0)
for g in h.coast: ax.plot(*g.xy,color="#3b7da3",lw=0.8)
for k,(lw,c) in reversed(list(ROADS.items())):
    if not minor and k in ("residential","unclassified"): continue
    for g in h.roads[k]: ax.plot(*g.xy,color=c,lw=lw,solid_capstyle="round")
for g in h.rail: ax.plot(*g.xy,color="#c75b5b",lw=1.2,ls=(0,(4,2)))
for g,n in h.bridges: ax.plot(*g.xy,color="#ffffff",lw=3.2,alpha=0.9)
for x,y,n in h.markets:
    if bbox[0]<x<bbox[2] and bbox[1]<y<bbox[3]:
        ax.plot(x,y,"o",color="#5fd38d",ms=4); ax.text(x,y,"  "+n,color="#5fd38d",fontsize=7)
for x,y,n,p in h.places:
    if bbox[0]<x<bbox[2] and bbox[1]<y<bbox[3] and (minor or p in ("suburb","town","city","island")):
        ax.text(x,y,n,color="#ffffff",fontsize=11 if p!="neighbourhood" else 8,ha="center",weight="bold" if p in("town","city","suburb") else None)
ax.set_xlim(bbox[0],bbox[2]); ax.set_ylim(bbox[1],bbox[3]); ax.set_aspect(1/0.9935); ax.axis("off")
ax.text(bbox[0]+0.005,bbox[1]+0.005,"Lagos study map. Data © OpenStreetMap contributors (ODbL). White = big bridges, red dashes = rail, green = markets.",color="#aaa",fontsize=10)
plt.savefig(sys.argv[2],bbox_inches="tight",pad_inches=0.1,facecolor=fig.get_facecolor())
print("roads",{k:len(v) for k,v in h.roads.items()},"water",len(h.water),"markets",len(h.markets),"places",len(h.places),"bridges",len(h.bridges))
