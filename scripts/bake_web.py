# Bake Gidi map v0.3 into JSON for the web map: districts, water, arterials, generated local streets, POIs.
# Units: metres, origin top-left, y down. Map units from map02.py are 0.8 km.
import json, math, random, re, os
from shapely.geometry import Polygon, LineString, Point, MultiLineString
from shapely.ops import unary_union, nearest_points
src=open("scripts/map02.py").read()
D=eval("["+src.split("D=[",1)[1].split("\n]\n",1)[0]+"\n]")
lagoon=eval(src.split("lagoon=",1)[1].split("\n",1)[0])
S=800.0; YT=8.0
def m(p): return (round(p[0]*S,1), round((YT-p[1])*S,1))
def mp(pts): return [m(p) for p in pts]
W,H=11*S,(8+0.4)*S
water=Polygon(mp(lagoon)).union(Polygon(mp([(5.0,0.05),(5.5,0.05),(5.5,2.0),(5.0,2.1)])))
ocean=Polygon(mp([(0,-0.4),(11,-0.4),(11,0.6),(5.0,0.6),(5.0,0.05),(2.95,0.05),(2.85,0.6),(0,0.6)]))

# Storeys for any district file generated before the generator wrote them (v1): bigger footprints go taller,
# matched to the real height bands of the district's inspiration (data/results/lga_table.json, built-area shares).
BANDS={"maze":[22,57,13,7]}
def derive_storeys(blds,id_):
    from shapely.geometry import Polygon as _P
    fixed={"shed":1,"kiosk":1,"stalls":1,"canopy":1,"warehouse":2,"school":2}
    st=[fixed.get(b[0]) for b in blds]
    free=sorted([i for i,b in enumerate(blds) if st[i] is None],key=lambda i:-_P(blds[i][1:]).area)
    b1,b2,b3,b4=BANDS.get(id_,[25,55,13,7]); n=len(free); cut4=n*b4/100; cut3=cut4+n*b3/100; cut2=cut3+n*b2/100
    for r,i in enumerate(free):
        st[i]=(4 if r<cut4*0.7 else 5) if r<cut4 else 3 if r<cut3 else 2 if r<cut2 else 1
    return st
GEN={}
IDS=["border","bazaar","jungle","port","maze","hub","railside","capital","estate","foodgate","watertown","oldshore","oldisland","heights","frontier"]
INFO=json.load(open("web/districts_info.json"))
from shapely.ops import polygonize
GENZONE=None
for _id in IDS:  # generated districts own the land inside their edge roads; neighbours' sketch streets stay out of it
    if os.path.exists(f"web/gen-{_id}.json"):
        _F=json.load(open(f"web/gen-{_id}.json"))
        _ring=max(polygonize(unary_union([LineString(m["pts"]) for m in _F["mains"] if "edge_with" in m])),key=lambda p:p.area).buffer(8)
        GENZONE=_ring if GENZONE is None else GENZONE.union(_ring)
PAT={"border":("sprawl",170,30,.45,8),"bazaar":("grid",95,10,.15,-4),"jungle":("organic",62,16,.18,12),"port":("grid",150,0,.25,0),
"maze":("organic",55,18,.2,-20),"hub":("grid",90,14,.15,25),"railside":("sprawl",150,30,.4,-12),"capital":("grid",120,4,.12,0),
"estate":("estate",140,22,.35,10),"foodgate":("sprawl",120,22,.3,30),"watertown":("organic",60,18,.22,-35),"oldshore":("sprawl",140,28,.4,5),
"oldisland":("organic",52,16,.15,-10),"heights":("estate",120,14,.25,-8),"frontier":("sprawl",190,30,.5,2)}
FIRST=["Adeyemi","Okafor","Bello","Ayinde","Ogundipe","Balogun","Lawal","Adebayo","Eze","Musa","Akande","Oladipo","Afolabi","Ibrahim","Adeleke","Oyelaran","Kalejaiye","Bankole","Odusanya","Mama Ronke","Iya Oloja","Ajasa","Fadipe","Oshinowo","Salami","Olatunji","Abeni","Taiwo","Kehinde","Idowu","Alaba","Ireti","Ayo","Folake"]
SUF=["Street","Road","Close","Lane","Crescent","Avenue","Way","Street","Street","Road"]
rnd=random.Random(1977)
def grid_lines(poly,sp,jit,drop,ang,pat):
    minx,miny,maxx,maxy=poly.bounds; cx,cy=(minx+maxx)/2,(miny+maxy)/2; R=max(maxx-minx,maxy-miny)
    a=math.radians(ang); ca,sa=math.cos(a),math.sin(a)
    def rot(x,y): return (cx+x*ca-y*sa, cy+x*sa+y*ca)
    n=int(R/sp)+2; pts={}
    for i in range(-n,n+1):
        for j in range(-n,n+1):
            x,y=i*sp,j*sp
            if pat=="estate": x+=math.sin(j*0.9)*sp*0.35; y+=math.sin(i*0.8)*sp*0.25
            pts[(i,j)]=rot(x+rnd.uniform(-jit,jit),y+rnd.uniform(-jit,jit))
    segs=[]
    for (i,j),p in pts.items():
        for di,dj in ((1,0),(0,1)):
            q=pts.get((i+di,j+dj))
            if q is None: continue
            if rnd.random()<drop: continue
            segs.append((p,q))
    mains=[]
    for k in (0,):
        mains.append(LineString([rot(-R,0),rot(R,0)])); mains.append(LineString([rot(0,-R),rot(0,R)]))
    return segs,mains
out={"size":[W,H],"districts":[],"water":[list(water.exterior.coords)],"ocean":[list(ocean.exterior.coords)],"streets":{},"mains":[],"pois":[]}
land_all=[]
for (name,ins,act,pts),id_ in zip(D,IDS):
    poly=Polygon(mp(pts)).buffer(0)
    land=poly.difference(water).difference(ocean)
    info=INFO[id_]
    out["districts"].append({"id":id_,"name":name.title().replace("The ","The "),"act":act,"area":round(poly.area*1e-6,2),"poly":[list(map(list,poly.exterior.coords))],**info})
    pat,sp,jit,drop,ang=PAT[id_]
    segs,mains=grid_lines(land,sp,jit,drop,ang,pat)
    inner=land.buffer(-6)
    if GENZONE is not None and not os.path.exists(f"web/gen-{id_}.json"): inner=inner.difference(GENZONE)
    lines=[]
    for p,q in segs:
        g=LineString([p,q]).intersection(inner)
        for s in getattr(g,"geoms",[g]):
            if s.geom_type=="LineString" and s.length>8: lines.append([[round(c[0]),round(c[1])] for c in s.coords])
    out["streets"][id_]=lines
    gen=f"web/gen-{id_}.json"
    if os.path.exists(gen):  # original street + building generator, calibrated on a pattern study (scripts/gen_fabric.py)
        F=json.load(open(gen))
        out["streets"][id_]=F["streets"]; mains=[]
        for mm in F["mains"]: out["mains"].append({"d":id_,"name":mm["name"],"pts":mm["pts"]})
        out.setdefault("buildings",{})[id_]=F["buildings"]
        out.setdefault("parcels",{})[id_]=F["parcels"]
        out.setdefault("lanes",{})[id_]=F.get("lanes",[])
        if F.get("paths"): out.setdefault("paths",{})[id_]=[p["pts"] for p in F["paths"]]   # footpaths: rail side, canal banks, worn crossings
        if F.get("canal"): out.setdefault("canals",[]).append({"d":id_,"pts":F["canal"]})
        for st in F.get("structures",[]):  # flyovers, rail bridges and skywalks drawn above the roads (slip roads are already in mains)
            if st["kind"]!="ramp": out.setdefault("structures",[]).append({"d":id_,**st})
        out.setdefault("storeys",{})[id_]=F.get("storeys") or derive_storeys(F["buildings"],id_)
        GEN[id_]=F
        core=json.load(open(f"study-{id_}-core.json")); M=F["metrics"]
        NETJ=json.load(open("web/network.json")) if os.path.exists("web/network.json") else {"gateways":[]}
        row=lambda lab,key,fmt: [lab,fmt(core["median"][key]),fmt(core["dense"][key]),fmt(M[key])]
        out.setdefault("study",{})[id_]={"rows":[
            ["Streets, km per km²",str(core["median"]["drive_km_per_km2"]),str(core["dense"]["drive_km_per_km2"]),str(M["drive_km_per_km2_edges_half"])],
            row("Junctions per km²","junctions_per_km2",str), row("T-junctions","T_share",lambda v:f"{round(v*100)}%"),
            ["Typical block",f'{core["median"]["block_m2"]["p50"]/1e4:.1f} ha',f'{core["dense"]["block_m2"]["p50"]/1e4:.1f} ha',f'{M["block_m2"]["p50"]/1e4:.1f} ha'],
            row("Buildings per km²","buildings_per_km2",lambda v:f"{v:,}"), row("Ground built on","coverage",lambda v:f"{round(v*100)}%"),
            ["Typical house",f'{round(core["median"]["footprint_m2"]["p50"])} m²',f'{round(core["dense"]["footprint_m2"]["p50"])} m²',f'{round(M["footprint_m2"]["p50"])} m²'],
            ["Gap between houses",f'{core["median"]["gap_m"]["p50"]} m',f'{core["dense"]["gap_m"]["p50"]} m',f'{M["gap_m"]["p50"]} m']],
            "links":[g for g in NETJ["gateways"] if g["from"]==id_]}
    for k,ml in enumerate(mains):
        g=ml.intersection(inner)
        for s in getattr(g,"geoms",[g]):
            if s.geom_type=="LineString" and s.length>150:
                nm=f"{rnd.choice(FIRST)} {rnd.choice(SUF)}"
                out["mains"].append({"d":id_,"name":nm,"pts":[[round(c[0]),round(c[1])] for c in s.coords]})
    # boardwalks for Water Town on the lagoon
    if id_=="watertown":
        bw=[]
        for i in range(26):
            x=rnd.uniform(m((5.05,0))[0],m((5.45,0))[0]); y=rnd.uniform(m((0,3.6))[1],m((0,2.6))[1])
            pt=Point(x,y)
            if water.contains(pt):
                L=rnd.uniform(25,60); a=rnd.choice([0,math.pi/2])+rnd.uniform(-.2,.2)
                bw.append([[round(x),round(y)],[round(x+L*math.cos(a)),round(y+L*math.sin(a))]])
        out["boardwalks"]=bw
    # POIs
    for p in info["pois"]:
        minx,miny,maxx,maxy=land.bounds
        pt=Point(minx+(maxx-minx)*p["u"], miny+(maxy-miny)*(1-p["v"]))
        core=land.buffer(-40) if not land.buffer(-40).is_empty else land
        if not core.contains(pt): pt=nearest_points(core,pt)[0]
        if id_ in GEN:  # generated district: landmarks sit on their parcels, street things on a street, the canal on the canal
            F=GEN[id_]
            if p["name"] in F["poi_pos"]: pt=Point(F["poi_pos"][p["name"]])
            elif "Canal" in p["name"] and F.get("canal"): pt=nearest_points(LineString(F["canal"]),pt)[0]
            else: pt=nearest_points(MultiLineString(F["streets"]+[m["pts"] for m in F["mains"]]),pt)[0]
        q={k:v for k,v in p.items() if k not in("u","v")}; q["d"]=id_; q["x"]=round(pt.x); q["y"]=round(pt.y)
        out["pois"].append(q)
    land_all.append(land)
# arterials (named), from map02 road calls, in map units
ART=[("Coastal Expressway","exp",[(0,1.35),(1.5,1.35),(2.9,1.3),(4.0,1.35),(5.0,1.45)]),
("Ring Road","art",[(1.0,4.7),(1.3,3.4),(1.7,2.6),(2.4,2.5),(3.4,2.4),(4.2,2.3),(4.6,1.6)]),
("Ayinde Avenue","art",[(2.5,5.75),(2.45,4.6),(2.35,3.3),(2.3,2.5),(2.4,1.3)]),
("Northern Road","art",[(2.4,2.5),(2.96,3.22),(3.6,3.3),(4.4,4.2),(5.0,5.0),(6.4,6.2),(7.8,6.9),(9.2,7.0)]),
("The Long Bridge","bridge",[(4.85,3.75),(5.4,3.3),(5.8,2.8),(6.1,2.2)]),
("Wharf Bridge","bridge",[(5.0,1.45),(5.5,1.45)]),
("Waterfront Drive","art",[(5.5,1.3),(6.0,1.3),(6.7,1.3),(8.0,1.35)]),
("Peninsula Expressway","exp",[(8.0,1.35),(9.2,1.4),(10.4,1.45)]),
("Shore Road","art",[(6.4,6.5),(7.8,6.9),(9.2,7.0),(9.3,7.2)])]
out["rail"]={"name":"Gidi Rail","pts":[list(m(p)) for p in [(0.9,4.7),(1.3,3.9),(1.75,3.1),(2.2,2.6),(2.7,2.3),(3.3,2.15),(3.9,2.0),(4.5,1.9)]]}
out["arterials"]=[{"name":n,"cls":c,"pts":[list(m(p)) for p in pts]} for n,c,pts in ART]
out["ferries"]=[{"name":"Old Shore – Heights ferry","pts":[list(m((8.2,6.45))),list(m((7.4,2.4)))]},{"name":"Old Shore – Water Town ferry","pts":[list(m((8.2,6.45))),list(m((5.35,3.6)))]}]
out["labels"]=[{"t":"The Lagoon","x":m((7.9,4.6))[0],"y":m((7.9,4.6))[1],"k":"water"},{"t":"The Ocean","x":m((6.8,-0.1))[0],"y":m((6.8,-0.1))[1],"k":"water"},{"t":"Farms and bush","x":m((5.6,6.9))[0],"y":m((5.6,6.9))[1],"k":"bush"},{"t":"Farms and bush","x":m((0.7,6.4))[0],"y":m((0.7,6.4))[1],"k":"bush"}]

# ---- civic layer: churches, mosques, schools, health, order, daily life (invented names) ----
CIV=json.load(open("web/civic.json")); ORDER=CIV["_counts_order"]
crnd=random.Random(2026)
CH_A=["Grace","Glory","Covenant","Victory","Mercy","Favour","Shiloh","Zion","Bethel","Rehoboth","Canaan","Goshen","Ebenezer","Living Spring","Mountain of Fire and Peace","Overcomers","Divine Light","Open Heaven","Latter Rain","Ark of Refuge"]
CH_B=["Assembly","Chapel","Ministries","Gospel Church","Tabernacle","Parish","Bible Church","Prayer House","Revival Centre","Baptist Church","Methodist Church","Anglican Church"]
CH_K=[("Church in a converted warehouse. Banners outside; loud vigils on Friday nights.",3),("Shopfront church. Plastic chairs, a keyboard, Sunday crowds on the road.",3),("Church in a half-built building. Services under bare concrete.",2),("Old mission church with a bell tower.",1)]
MQ=["Nurul Huda","Al-Furqan","Taqwa","Rahma","Salam","Hidaya","Al-Ikhlas","Ar-Rasheed","Darussalam","Nurudeen","Al-Mumin","Baitul Hamd"]
MQ_K=[("Neighbourhood mosque. Call to prayer five times a day; Friday prayers fill the street.",4),("Small prayer spot by the market. Traders pray between sales.",2),("Mosque with a loudspeaker minaret and a Quranic school in the yard.",2)]
SC_PUB=["Community Primary School","Model Secondary School","Community Grammar School","Junior High School","Primary School No. {n}"]
SC_PRI=["Bright Stars Nursery & Primary","Royal Kiddies School","Golden Gate College","Excellence Academy","Little Angels School","Wisdom Gate Schools","Destiny Child College"]
CL=["Mercy Clinic","Hope Medical Centre","Life Line Hospital","Ayo Maternity Home","Good Shepherd Clinic","Divine Health Hospital","Sunrise Medical Centre"]
CHEM=["Good Health Chemist","Iya Bisi Patent Medicine","Cure Pharmacy","Life Pharmacy","Mama Ronke Chemist","Alafia Pharmacy","Daily Care Chemist","Remedy Stores","Oko Medicine Store","Fresh Life Pharmacy"]
FUEL=["Gidi Oil","Sunline Fuel","Crestline","Tinapet","Lagoon Petroleum","Kekemax"]
BANK=["Gidi Trust Bank","Harbour Bank","Lagoon Bank","Eagle Bank","Crest Bank","Union Crest Bank"]
SPORT=[("Community Football Pitch","Sandy pitch. Evening matches, betting on the side."),("Viewing Centre","Football viewing centre. Match nights are loud and packed."),("Odds Corner","Betting shop and viewing centre.")]
NOTE={"clinic":"Private clinic in a converted house. Legal medicine deliveries.","chemist":"Patent medicine store. There's one on almost every street.",
"fuel":"Petrol station. In fuel scarcity the queue stretches onto the road.","bank":"Bank with an ATM. Long queues; cash runs."}
def wpick(lst): 
    t=sum(w for _,w in lst); r=crnd.random()*t
    for v,w in lst:
        r-=w
        if r<=0: return v
    return lst[0][0]
ART_LINES=[LineString([m(p) for p in pts]) for _,_,pts in ART]
allp=[Point(p["x"],p["y"]) for p in out["pois"]]
# Everyday places in the built districts are placed by coverage (owner, Oct 2026): every house gets a school, a place of worship
# and a chemist or clinic within 10 minutes' walk (833 m at 5 km/h); a house that can't be reached in 10 gets 15 (1250 m).
# Same walking network as the living test (scripts/walknet.py). Names are still dealt at random.
import sys as _sys; _sys.path.insert(0,"scripts"); import walknet
EVERYDAY={"school":("school",),"worship":("church","mosque"),"health":("chemist","clinic")}
if GEN:
    REACH=walknet.Reach(walknet.graph(walknet.ways_of(out,list(GEN)),"walk"))
def coverage_plan(id_):
    """{type: [points]} for this district's schools, places of worship, chemists and clinics, chosen greedily by coverage."""
    houses=[Polygon(b[1:]).centroid for b in out["buildings"][id_] if b[0] in ("front","back","stilt")]   # homes, on land and on stilts
    HA=[REACH.attach(h) for h in houses]
    cands=[Point(q["x"],q["y"]) for q in SL]
    def covered(dist,limit): return {i for i,(u,du,v,dv,off) in enumerate(HA) if min(dist.get(u,1e18)+du,dist.get(v,1e18)+dv)+off<=limit}
    CC={}   # candidate -> houses within 10 and 15 min
    for j,c in enumerate(cands):
        d=REACH.from_points([c],1250); CC[j]=(covered(d,833),covered(d,1250))
    plan={}; taken=set(); report={}
    for cat,types in EVERYDAY.items():
        want={t:max(0,cnt[t]-keyed.get(t,0)) for t in types}; need=sum(want.values())
        have=[Point(p["x"],p["y"]) for p in out["pois"] if p["d"]==id_ and p["type"] in types]
        d0=REACH.from_points(have,1250) if have else {}
        c10,c15=covered(d0,833),covered(d0,1250); picks=[]
        for limit in (833,1250):   # 10 minutes first; whoever is still out of reach gets 15
            while True:
                gain=lambda j: len((CC[j][0] if limit==833 else CC[j][1])-(c10 if limit==833 else c15|c10))
                free_=[j for j in CC if j not in taken and all(cands[j].distance(cands[k])>60 for k in picks)]
                if not free_: break
                j=max(free_,key=lambda j:(gain(j),-j)); g=gain(j)
                if g==0 and (limit==1250 or len(picks)>=need): break
                if g==0:   # every house is covered but the district still has places to fill: spread them out
                    j=max(free_,key=lambda j:min([cands[j].distance(cands[k]) for k in picks]+[cands[j].distance(h) for h in have]+[1e9]))
                picks.append(j); taken.add(j); c10|=CC[j][0]; c15|=CC[j][1]
        seq=[]   # share the picks between the types in proportion (churches and mosques; chemists and clinics)
        for k in range(len(picks)):
            t=max(types,key=lambda t:(want[t]+0.5)/(1+sum(1 for x in seq if x==t))); seq.append(t)
        for j,t in zip(picks,seq): plan.setdefault(t,[]).append(cands[j])
        report[cat]=(round(100*len(c10)/max(1,len(houses))),round(100*len(c15|c10)/max(1,len(houses))),len(picks),need)
    print(id_,"everyday places within 10 / 15 min (%), placed / planned:",report)
    return plan
LEFT={}   # each district's unused civic slots, for the late places
for (name,ins,act,pts),id_ in zip(D,IDS):
    poly=Polygon(mp(pts)).buffer(0); land=poly.difference(water).difference(ocean); core=land.buffer(-35)
    if core.is_empty: core=land
    roads=[LineString(mm["pts"]) for mm in out["mains"] if mm["d"]==id_]+[a for a in ART_LINES if a.intersects(poly)]
    minx,miny,maxx,maxy=core.bounds
    SL=list(GEN[id_]["slots"]) if id_ in GEN else None
    def spot(near_road=False, spacing=70):
        if SL:  # generated district: civic places take over a real plot (a building), near a main road when they need passing trade
            for sp in (spacing, spacing*0.6, spacing*0.35):
                c=[q for q in SL if (q["main"] or not near_road) and all(Point(q["x"],q["y"]).distance(o)>sp for o in allp)]
                if c:
                    q=crnd.choice(c); SL.remove(q); pt=Point(q["x"],q["y"]); allp.append(pt); return pt
        for _ in range(400):
            if near_road and roads:
                r=crnd.choice(roads); pt=r.interpolate(crnd.random(),normalized=True)
                pt=Point(pt.x+crnd.uniform(-30,30),pt.y+crnd.uniform(-30,30))
            else:
                pt=Point(crnd.uniform(minx,maxx),crnd.uniform(miny,maxy))
            if core.contains(pt) and all(pt.distance(q)>spacing for q in allp):
                allp.append(pt); return pt
        for _ in range(400):
            pt=Point(crnd.uniform(minx,maxx),crnd.uniform(miny,maxy))
            if core.contains(pt): allp.append(pt); return pt
    def add(t,nm,note,pt): out["pois"].append({"name":nm,"type":t,"note":note,"d":id_,"x":round(pt.x),"y":round(pt.y),"civic":True})
    for k in CIV["key"].get(id_,[]):
        b=core.bounds; pt=Point(b[0]+(b[2]-b[0])*k["u"], b[1]+(b[3]-b[1])*(1-k["v"]))
        if not core.contains(pt): pt=nearest_points(core,pt)[0]
        if SL:
            q=min([q for q in SL if q["main"]] or SL,key=lambda q:Point(q["x"],q["y"]).distance(pt)); SL.remove(q); pt=Point(q["x"],q["y"])
        allp.append(pt); add(k["type"],k["name"],k["note"],pt)
    cnt=dict(zip(ORDER,CIV["counts"][id_]))
    keyed={}
    for k in CIV["key"].get(id_,[]): keyed[k["type"]]=keyed.get(k["type"],0)+1
    dn=name.title()
    PLAN=coverage_plan(id_) if SL else {}
    for q in [q for pts_ in PLAN.values() for q in pts_]:   # the planned plots are taken
        SL[:]=[r for r in SL if (r["x"],r["y"])!=(q.x,q.y)]
    def spot_or_plan(t, **kw):
        if PLAN.get(t): pt=PLAN[t].pop(0); allp.append(pt); return pt
        return spot(**kw)
    for t in ORDER:
        n=max(0,cnt[t]-keyed.get(t,0),len(PLAN.get(t,[])))
        for i in range(n):
            if t=="church": nm=f"{crnd.choice(CH_A)} {crnd.choice(CH_B)}"; note=wpick(CH_K); pt=spot_or_plan(t)
            elif t=="mosque": nm=f"{crnd.choice(MQ)} Mosque"; note=wpick(MQ_K); pt=spot_or_plan(t)
            elif t=="school":
                if crnd.random()<0.55: nm=crnd.choice(SC_PRI); note="Private school in a converted house, name painted on the wall. School-run jams at 7 a.m. and 2 p.m."
                else: nm=dn.replace("The ","")+" "+crnd.choice(SC_PUB).format(n=crnd.randint(1,9)); note="Public school with a sandy yard. Kids in uniform fill the lanes at 7 a.m. and 2 p.m."
                pt=spot_or_plan(t,spacing=90)
            elif t=="clinic": nm=crnd.choice(CL); note=NOTE["clinic"]; pt=spot_or_plan(t)
            elif t=="chemist": nm=crnd.choice(CHEM); note=NOTE["chemist"]; pt=spot_or_plan(t,near_road=True,spacing=45)
            elif t=="fuel": nm=crnd.choice(FUEL); note=NOTE["fuel"]; pt=spot(near_road=True,spacing=120)
            elif t=="bank": nm=crnd.choice(BANK); note=NOTE["bank"]; pt=spot(near_road=True,spacing=50)
            elif t=="sport":
                nm,note=crnd.choice(SPORT); pt=spot(); t2="betting" if "Odds" in nm or "Viewing" in nm else "sport"; add(t2,nm,note,pt); continue
            add(t,nm,note,pt)
    LEFT[id_]=SL

# places added after review ("key_late"): placed after every district's random ones, on the nearest free real plot, so no other civic pin moves
for id_,ks in CIV.get("key_late",{}).items():
    SL=LEFT.get(id_)
    for k in ks:
        pt=Point(k["x"],k["y"])
        if SL:
            q=min(SL,key=lambda q:Point(q["x"],q["y"]).distance(pt)); SL.remove(q); pt=Point(q["x"],q["y"])
        out["pois"].append({"name":k["name"],"type":k["type"],"note":k["note"],"d":id_,"x":round(pt.x),"y":round(pt.y),"civic":True})

def rd(o):
    if isinstance(o,float): return round(o,1)
    if isinstance(o,list): return [rd(x) for x in o]
    if isinstance(o,tuple): return [rd(x) for x in o]
    if isinstance(o,dict): return {k:rd(v) for k,v in o.items()}
    return o
for mm in out["mains"]:  # labels read left to right
    if mm["pts"][0][0] > mm["pts"][-1][0]: mm["pts"] = mm["pts"][::-1]
s=json.dumps(rd(out),separators=(",",":"),ensure_ascii=False)
open("web/gidi-data.js","w").write("window.GIDI="+s+";")
print(len(s)//1024,"KB", sum(len(v) for v in out["streets"].values()),"street segs",len(out["pois"]),"pois",len(out["mains"]),"mains")
