# Gidi concept map v0.1 — a schematic remix of Lagos's shape, sized for the game. Owner redraws it.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch, Circle
import numpy as np
BG="#17191c"; LAND="#2a2d31"; WATER="#1f4459"; ROAD="#e8a23a"; MINOR="#6b665d"; TXT="#f2f2f2"
ACT={1:"#5fd38d",2:"#f2c76e",3:"#e0675c"}
fig,ax=plt.subplots(figsize=(18,13.5),dpi=110); fig.patch.set_facecolor(BG); ax.set_facecolor(WATER)
ax.add_patch(plt.Rectangle((0,0),8,6,fc=WATER,ec="none",zorder=0))
# land: mainland (west/north), island chain (south-east), peninsula (east)
main=[(0,0.9),(0,6),(8,6),(8,4.9),(6.2,4.7),(5.4,4.2),(4.9,3.4),(4.6,2.6),(4.2,2.15),(3.7,1.9),(3.3,1.4),(2.9,1.15),(2.2,1.0),(1.2,0.85)]
ax.add_patch(Polygon(main,closed=True,fc=LAND,ec="#3b7da3",lw=1.2))
isl=[(3.9,1.15),(4.4,1.55),(5.0,1.75),(5.6,1.7),(6.2,1.9),(8,2.05),(8,0.95),(6.4,0.9),(5.4,0.75),(4.6,0.7),(4.1,0.8)]
ax.add_patch(Polygon(isl,closed=True,fc=LAND,ec="#3b7da3",lw=1.2))
# ocean strip + beach
ax.add_patch(Polygon([(0,0),(8,0),(8,0.55),(4.4,0.5),(0,0.62)],closed=True,fc="#183849",ec="none"))
ax.plot([4.1,8],[0.62,0.6],color="#d8c38a",lw=3)  # beach
# stilt village on water
for x,y in [(4.55,2.9),(4.7,3.05),(4.62,2.75),(4.8,2.88),(4.5,3.1),(4.72,2.62)]:
    ax.add_patch(plt.Rectangle((x,y),0.07,0.07,fc="#8a7f6c",ec="none"))
# roads
def road(pts,lw=3,c=ROAD,ls="-"): ax.plot(*zip(*pts),color=c,lw=lw,solid_capstyle="round",ls=ls,zorder=3)
road([(0,4.6),(1.6,4.4),(2.6,4.0),(3.4,3.5),(4.1,3.0),(4.35,2.4),(4.2,2.0)])            # ring expressway
road([(1.2,6),(1.5,4.4),(1.7,3.2),(2.2,2.2),(2.6,1.3)])                                  # north-south artery
road([(0,2.6),(1.7,3.2),(2.9,3.6),(3.5,4.6),(4.2,6)])                                    # cross artery
road([(0.3,1.3),(1.4,1.25),(2.6,1.3),(3.3,1.45)],lw=2.5)                                 # port road
road([(4.35,2.6),(5.0,2.4),(5.6,2.1),(5.9,1.75)],lw=5,c="#ffffff")                     # THE BRIDGE
road([(3.3,1.45),(3.75,1.2),(4.2,1.05)],lw=4,c="#ffffff")                                # short old bridge
road([(4.2,1.05),(5.0,1.15),(5.9,1.4),(6.5,1.55),(8,1.6)],lw=3)                          # island + peninsula road
road([(5.9,1.75),(5.9,1.4)],lw=2.5)
road([(5.2,6),(5.6,5.2),(6.4,4.9),(8,5.1)],lw=2.5)                                       # north road to estate
ax.plot([1.0,1.4,1.75,2.1,2.4],[6,4.8,3.6,2.4,1.5],color="#c75b5b",lw=2,ls=(0,(5,3)),zorder=3)  # rail
# minor street texture
rng=np.random.default_rng(7)
for cx,cy,r,n in [(1.6,2.4,0.75,70),(2.6,3.0,0.6,45),(0.8,3.6,0.7,40),(4.6,1.1,0.35,45),(6.3,1.3,0.45,25)]:
    for _ in range(n):
        x,y=cx+rng.uniform(-r,r),cy+rng.uniform(-r,r); a=rng.choice([0,np.pi/2])+rng.normal(0,0.25); l=rng.uniform(0.08,0.25)
        ax.plot([x,x+l*np.cos(a)],[y,y+l*np.sin(a)],color=MINOR,lw=0.6,zorder=2)
# districts
def district(x,y,name,inspired,act,w=1.5,h=0.48):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.03",fc=BG,ec=ACT[act],lw=2,alpha=0.92,zorder=5))
    ax.text(x,y+0.07,name,color=TXT,fontsize=12.5,ha="center",va="center",weight="bold",zorder=6)
    ax.text(x,y-0.12,inspired,color="#a9a9a9",fontsize=8.5,ha="center",va="center",zorder=6)
district(1.55,2.35,"MARKET QUARTER","feel of Mushin, Idumota, Oshodi markets",1,1.75)
district(2.75,3.05,"THE MOTOR PARK","feel of Oshodi: buses, touts, the boss's park",1,1.7)
district(0.85,3.75,"THE STREETS BEHIND","feel of Ajegunle, Agege: Tunde's room",1,1.65)
district(0.95,1.05,"THE PORT","feel of Apapa: containers, tanker jams",2,1.4)
district(4.62,3.4,"WATER TOWN","feel of Makoko: stilts, canoes",3,1.2)
district(6.4,5.35,"THE ESTATE","feel of Omole, Magodo: gates, big men",2,1.6)
district(4.75,1.3,"OLD ISLAND","feel of Lagos Island: old markets",2,1.25)
district(6.45,1.0,"THE RICH SIDE","feel of Ikoyi, VI: towers, clubs, power",3,1.45)
district(7.15,2.4,"THE PENINSULA","feel of Lekki: one road, new estates",3,1.25)
# story pins
def pin(x,y,label,dx=0.12,dy=0.0,c="#ffffff"):
    ax.add_patch(Circle((x,y),0.05,fc=c,ec=BG,lw=1.5,zorder=8)); ax.text(x+dx,y+dy,label,color=c,fontsize=9.5,zorder=8,va="center")
pin(0.55,3.45,"1  Tunde's room")
pin(1.0,1.95,"2  The steal → 'Ole!' chase",dy=-0.13)
pin(2.45,1.75,"3  The gate: boss pulls him in",dx=-0.05,dy=-0.14)
pin(3.3,2.75,"4  Boss's motor park (the bike)")
pin(4.38,2.48,"Bridge-head checkpoint",dx=-1.5,dy=-0.02,c="#ff9a8a")
pin(6.95,1.6,"Toll plaza",dx=0.1,dy=-0.16,c="#ff9a8a")
pin(1.75,1.27,"Where the oja comes in",dy=0.12,c="#f2c76e")
# legend & notes
ax.text(0.08,5.82,"GIDI — concept map v0.1",color=TXT,fontsize=22,weight="bold",va="top")
ax.text(0.08,5.5,"Lagos's shape, compressed for a game: about 8 km × 6 km (Claude's proposal; owner redraws).",color="#cfcfcf",fontsize=11,va="top")
for i,(a,t) in enumerate([(1,"Act 1  Survive: mainland, open from the start"),(2,"Act 2  Hustle: port, old island, the estate"),(3,"Act 3  Empire: rich side, peninsula, water town")]):
    ax.add_patch(FancyBboxPatch((0.1,5.1-i*0.27),0.18,0.14,boxstyle="round,pad=0.01",fc=BG,ec=ACT[a],lw=2))
    ax.text(0.38,5.17-i*0.27,t,color=TXT,fontsize=10.5,va="center")
ax.text(5.15,3.9,"THE LAGOON",color="#8fc1dc",fontsize=20,weight="bold",alpha=0.7)
ax.text(5.4,3.1,"THE BRIDGE\nOkada are banned here (as on real Lagos bridges).\nRide it anyway and the taskforce can seize your bike\n— the bike you still owe the boss for.",color="#ffffff",fontsize=9.5,va="center")
ax.text(4.5,0.25,"THE OCEAN",color="#8fc1dc",fontsize=14,alpha=0.7)
ax.plot([6.8,7.8],[5.85,5.85],color=TXT,lw=2); ax.text(7.3,5.72,"1 km",color=TXT,fontsize=10,ha="center")
ax.text(7.95,0.06,"Schematic. All names are working titles. Inspired by Lagos; not a map of it.",color="#888",fontsize=8,ha="right")
ax.set_xlim(0,8); ax.set_ylim(0,6); ax.set_aspect("equal"); ax.axis("off")
plt.savefig("gidi-concept-v0.1.png",bbox_inches="tight",pad_inches=0.05,facecolor=BG)
