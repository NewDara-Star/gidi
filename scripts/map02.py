# Gidi map v0.2 (drawn in units of 0.8 km; 1.25 units = 1 km): 15 districts merged from Lagos's 20 LGAs (see lagos-lgas-research.md). Schematic, km grid.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as P
from shapely.geometry import Polygon
BG="#15171a"; BUSH="#24282b"; WATER="#1f4459"; SEA="#183849"
ACT={1:"#5fd38d",2:"#f2c76e",3:"#e0675c"}
D=[ # name, inspired by, act, polygon (km)
("THE BORDER","Badagry: smuggling, checkpoints, beach",2,[(0,0.6),(1.5,0.6),(1.5,2.2),(0.2,2.3)]),
("THE BAZAAR","Ojo + Trade Fair: market with its own court",2,[(1.5,0.6),(2.85,0.6),(2.9,1.9),(1.55,2.0),(1.5,2.2)]),
("JUNGLE CITY","Ajegunle + Festac: ghetto, music, scam cafés",1,[(2.85,0.6),(2.95,0.05),(3.95,0.05),(4.0,1.85),(2.9,1.9)]),
("THE PORT","Apapa + Mile 2: containers, tankers, prison",2,[(3.95,0.05),(5.0,0.05),(5.0,2.1),(4.0,1.85)]),
("THE MAZE","Mushin + Shomolu: parts lanes, print shops",1,[(2.9,1.9),(4.0,1.85),(4.3,3.05),(3.0,3.15)]),
("THE HUB","Oshodi + Ojuelegba: interchange, motor parks",1,[(1.55,2.0),(2.9,1.9),(3.0,3.15),(1.75,3.35)]),
("RAILSIDE","Agege + Ifako + Alimosho: bread, cattle, sprawl",1,[(0.2,2.3),(1.5,2.2),(1.55,2.0),(1.75,3.35),(1.85,4.6),(0.3,4.7)]),
("THE CAPITAL","Ikeja: phone market, government, night strip",2,[(1.75,3.35),(3.0,3.15),(3.2,4.55),(1.85,4.6)]),
("THE ESTATE","Magodo, Omole, Ikeja GRA: big men, gates",2,[(1.85,4.6),(3.2,4.55),(3.35,5.7),(2.0,5.75)]),
("FOOD GATE","Kosofe: Mile 12 food trucks, Ojota park",1,[(3.0,3.15),(4.3,3.05),(4.35,3.6),(4.85,3.85),(5.05,4.7),(3.9,5.1),(3.2,4.55)]),
("WATER TOWN","Makoko + Bariga + Agboyi: stilts, canoes, sawmill",3,[(4.0,1.85),(5.0,2.1),(5.05,2.8),(4.85,3.85),(4.35,3.6),(4.3,3.05)]),
("OLD SHORE","Ikorodu + Epe: royal town, ferries, fish, curfews",2,[(6.4,5.75),(7.6,6.35),(9.2,6.6),(9.3,7.5),(6.3,7.5)]),
("OLD ISLAND","Lagos Island: palace, cloth market, porters",2,[(5.5,0.7),(6.6,0.7),(6.75,1.9),(6.0,2.2),(5.5,2.0)]),
("THE HEIGHTS","Ikoyi, VI, Banana Island: towers, money",3,[(6.6,0.7),(8.0,0.7),(8.0,2.3),(6.75,1.9)]),
("THE FRONTIER","Lekki + Ibeju-Lekki: land war, refinery",3,[(8.0,0.7),(10.4,0.7),(10.4,2.45),(8.0,2.3)]),
]
lagoon=[(5.0,2.1),(5.5,2.0),(6.0,2.2),(6.75,1.9),(8.0,2.3),(10.4,2.45),(10.9,2.5),(10.9,6.3),(9.2,6.6),(7.6,6.35),(6.4,5.75),(5.05,4.7),(4.85,3.85),(5.05,2.8)]
fig,ax=plt.subplots(figsize=(19,14),dpi=110); fig.patch.set_facecolor(BG)
ax.add_patch(P([(0,-0.4),(11,-0.4),(11,8),(0,8)],fc=BUSH,ec="none"))           # undeveloped land / farms
ax.add_patch(P([(0,-0.4),(11,-0.4),(11,0.6),(5.0,0.6),(5.0,0.05),(2.95,0.05),(2.85,0.6),(0,0.6)],fc=SEA,ec="none"))  # ocean; reclaimed land bulges under Jungle City and the Port       # ocean
ax.add_patch(P(lagoon,fc=WATER,ec="#3b7da3",lw=1.2))
ax.add_patch(P([(5.0,0.05),(5.5,0.05),(5.5,2.0),(5.0,2.1)],fc=WATER,ec="none"))  # harbour channel
ax.add_patch(P([(10.4,0.6),(11,0.6),(11,2.5),(10.4,2.45)],fc=BUSH,ec="none"))
ax.plot([5.5,10.4],[0.66,0.66],color="#d8c38a",lw=3,zorder=4)          # beach
tot=0; rows=[]
LAB={"THE HUB":(2.3,3.0),"THE MAZE":(3.6,2.7),"THE PORT":(4.5,1.2),"JUNGLE CITY":(3.4,1.2),"THE BAZAAR":(2.2,1.0),"THE BORDER":(0.75,1.9),"OLD ISLAND":(6.1,1.05),"THE HEIGHTS":(7.35,1.0),"THE FRONTIER":(9.3,1.95),"WATER TOWN":(4.55,2.45),"FOOD GATE":(3.85,4.0),"THE CAPITAL":(2.45,3.95),"THE ESTATE":(2.6,5.2),"RAILSIDE":(0.9,3.5),"OLD SHORE":(7.8,7.0)}
BAN={"OLD ISLAND","THE HEIGHTS","THE CAPITAL","THE PORT"}; SWEEP={"THE HUB","THE MAZE","FOOD GATE"}
for n,ins,a,pts in D:
    poly=Polygon(pts); ar=poly.area*0.64; tot+=ar; rows.append((n,ins,a,round(ar,1)))
    ax.add_patch(P(pts,fc=ACT[a],alpha=0.16,ec=ACT[a],lw=2,zorder=2))
    if n in BAN: ax.add_patch(P(pts,fc="none",ec="#ff8a7a",lw=0,hatch="///",alpha=0.35,zorder=2))
    c=poly.representative_point(); x,y=LAB.get(n,(c.x,c.y))
    ax.text(x,y,f"{n}\n{ar:.1f} km²",color="white",fontsize=11,weight="bold",ha="center",va="center",zorder=7,linespacing=1.3,
            bbox=dict(boxstyle="round,pad=0.25",fc=BG,ec=ACT[a],lw=1.2,alpha=0.85))
# stilts
for x,y in [(5.12,3.0),(5.2,3.2),(5.1,3.4),(5.28,3.05),(5.18,2.85),(5.3,3.35)]:
    ax.add_patch(plt.Rectangle((x,y),0.06,0.06,fc="#8a7f6c",ec="none",zorder=5))
def road(pts,lw=2.6,c="#e8a23a",ls="-",z=4): ax.plot(*zip(*pts),color=c,lw=lw,ls=ls,solid_capstyle="round",zorder=z)
road([(0,1.35),(1.5,1.35),(2.9,1.3),(4.0,1.35),(5.0,1.45)])                  # coast expressway (Badagry-style)
road([(1.0,4.7),(1.3,3.4),(1.7,2.6),(2.4,2.5),(3.4,2.4),(4.2,2.3),(4.6,1.6)])  # ring road
road([(2.5,5.75),(2.45,4.6),(2.35,3.3),(2.3,2.5),(2.4,1.3)],lw=2.2)        # north-south artery
road([(2.4,2.5),(2.96,3.22),(3.6,3.3),(4.4,4.2),(5.0,5.0),(6.4,6.2),(7.8,6.9),(9.2,7.0)],lw=2.4)  # food-gate road to Old Shore
road([(4.85,3.75),(5.4,3.3),(5.8,2.8),(6.1,2.2)],lw=5,c="#ffffff")         # THE LONG BRIDGE
road([(5.0,1.45),(5.5,1.45)],lw=4,c="#ffffff")                            # port bridge
road([(6.0,1.3),(6.7,1.3),(8.0,1.35),(9.2,1.4),(10.4,1.45)],lw=2.6)       # island + peninsula road
road([(7.2,1.95),(7.4,2.6),(7.6,2.3)],lw=0)
ax.plot([0.9,1.3,1.75,2.2,2.7,3.3,3.9,4.5],[4.7,3.9,3.1,2.6,2.3,2.15,2.0,1.9],color="#c75b5b",lw=2,ls=(0,(5,3)),zorder=4)  # rail
for (x1,y1),(x2,y2) in [((8.2,6.45),(7.4,2.4)),((8.2,6.45),(5.35,3.6))]:
    ax.plot([x1,x2],[y1,y2],color="#8fc1dc",lw=1.2,ls=(0,(2,3)),zorder=3)   # ferries
def pin(x,y,t,c="#ffffff",dx=0.08,dy=0,fs=8.5):
    ax.add_patch(plt.Circle((x,y),0.06,fc=c,ec=BG,lw=1.2,zorder=8)); ax.text(x+dx,y+dy,t,color=c,fontsize=fs,zorder=8,va="center")
pin(3.1,0.45,"1 Tunde's room")
pin(3.3,2.2,"2 The steal, 'Ole!'",dy=-0.13)
pin(2.85,2.05,"3 The gate",dx=-0.62,dy=-0.12)
pin(1.85,2.5,"4 Boss's motor park",dx=-0.05,dy=-0.15)
pin(4.9,3.78,"Bridge checkpoint",c="#ff9a8a",dx=0.1,dy=0.18)
pin(8.35,1.4,"Toll plaza",c="#ff9a8a",dy=0.16)
pin(0.6,1.35,"Checkpoints",c="#ff9a8a",dy=-0.15)
pin(0.15,1.0,"Border post",c="#ff9a8a")
pin(4.5,0.35,"Container yard",c="#f2c76e",dx=-0.4,dy=-0.15)
pin(8.2,6.45,"Ferry jetty",c="#8fc1dc",dy=0.14)
ax.text(7.6,4.4,"THE LAGOON",color="#8fc1dc",fontsize=22,weight="bold",alpha=0.65)
ax.text(5.85,3.0,"THE LONG BRIDGE\nokada banned",color="white",fontsize=9)
ax.text(6.5,-0.15,"THE OCEAN",color="#8fc1dc",fontsize=14,alpha=0.7)
ax.text(0.15,7.75,"GIDI — map v0.3",color="white",fontsize=24,weight="bold",va="top")
ax.text(0.15,7.3,f"15 districts merged from Lagos's 20 local governments · {tot:.1f} km² of district land · frame 8.8 × 6.7 km",color="#cfcfcf",fontsize=11,va="top")
for i,(a,t) in enumerate([(1,"Act 1  Survive"),(2,"Act 2  Hustle"),(3,"Act 3  Empire")]):
    ax.add_patch(P([(0.15,6.85-i*0.3),(0.4,6.85-i*0.3),(0.4,7.0-i*0.3),(0.15,7.0-i*0.3)],fc=ACT[a],alpha=0.5,ec=ACT[a]))
    ax.text(0.5,6.92-i*0.3,t,color="white",fontsize=10.5,va="center")
ax.add_patch(P([(0.15,5.95),(0.4,5.95),(0.4,6.1),(0.15,6.1)],fc="none",ec="#ff8a7a",hatch="///"))
ax.text(0.5,6.02,"Okada banned (taskforce seizes bikes)",color="white",fontsize=10.5,va="center")
ax.plot([0.15,0.4],[5.75,5.75],color="#c75b5b",lw=2,ls=(0,(5,3))); ax.text(0.5,5.75,"Rail",color="white",fontsize=10.5,va="center")
ax.plot([0.15,0.4],[5.5,5.5],color="#8fc1dc",lw=1.2,ls=(0,(2,3))); ax.text(0.5,5.5,"Ferry",color="white",fontsize=10.5,va="center")
ax.text(0.5,5.25,"Dark land = farms and bush (not built)",color="#9a9a9a",fontsize=9.5,va="center")
ax.plot([9.35,10.6],[7.7,7.7],color="white",lw=2); ax.text(9.98,7.55,"1 km",color="white",fontsize=10,ha="center")
ax.text(10.9,-0.35,"Schematic; all names are working titles. Inspired by Lagos, not a map of it.",color="#8a8a8a",fontsize=8,ha="right")
ax.set_xlim(0,11); ax.set_ylim(-0.4,8); ax.set_aspect("equal"); ax.axis("off")
plt.savefig("gidi-map-v0.3.png",bbox_inches="tight",pad_inches=0.05,facecolor=BG)
print("total",round(tot,1)); [print(r) for r in rows]
