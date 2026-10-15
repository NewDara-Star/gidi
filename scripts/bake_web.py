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
# ---- Gidi v2 frame (owner, 15 Oct 2026: one even scale 1:4, docs/LAYOUT-V2.md): size, water, districts, arterials and rail come from
# web/layout-v2.json (scripts/layout_v2.py). map02.py still gives the districts' names, inspirations and acts.
LAYOUT=json.load(open("web/layout-v2.json"))
W,H=LAYOUT["size"]
water=unary_union([Polygon(w).buffer(0) for w in LAYOUT["water"]])   # the lagoon, the harbour, the channel round Old Island, the creeks, the bay
ocean=Polygon(LAYOUT["ocean"]).buffer(0)
IDS_V1=["border","bazaar","jungle","port","maze","hub","railside","capital","estate","foodgate","watertown","oldshore","oldisland","heights","frontier"]
NEW_D={"airport":("THE AIRPORT","Murtala Muhammed International Airport (Ikeja)",2),"yaba":("THE CAMPUS","Yaba + Akoka (the university, Sabo, Ojuelegba)",2)}   # names to be settled with the owner
IDS=IDS_V1+list(NEW_D)
_NM={i:(n,ins,act) for (n,ins,act,pts),i in zip(D,IDS_V1)}; _NM.update(NEW_D)
D=[(_NM[i][0],_NM[i][1],_NM[i][2],i) for i in IDS]   # the last slot is now the district id: its outline is DPOLY[id]
DPOLY={k:Polygon(v).buffer(0) for k,v in LAYOUT["districts"].items()}
def gen_ok(i):
    """A district's generated file counts only once it is built in the v2 frame (older files sit at the v1 positions)."""
    f=f"web/gen-{i}.json"
    return os.path.exists(f) and json.load(open(f)).get("layout")=="v2"

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
INFO=json.load(open("web/districts_info.json"))
from shapely.ops import polygonize
GENZONE=None
for _id in IDS:  # generated districts own the land inside their edge roads; neighbours' sketch streets stay out of it
    if gen_ok(_id):
        _F=json.load(open(f"web/gen-{_id}.json"))
        _ring=max(polygonize(unary_union([LineString(m["pts"]) for m in _F["mains"] if "edge_with" in m])),key=lambda p:p.area).buffer(8)
        GENZONE=_ring if GENZONE is None else GENZONE.union(_ring)
PAT={"border":("sprawl",170,30,.45,8),"bazaar":("grid",95,10,.15,-4),"jungle":("organic",62,16,.18,12),"port":("grid",150,0,.25,0),
"maze":("organic",55,18,.2,-20),"hub":("grid",90,14,.15,25),"railside":("sprawl",150,30,.4,-12),"capital":("grid",120,4,.12,0),
"estate":("estate",140,22,.35,10),"foodgate":("sprawl",120,22,.3,30),"watertown":("organic",60,18,.22,-35),"oldshore":("sprawl",140,28,.4,5),
"oldisland":("organic",52,16,.15,-10),"heights":("estate",120,14,.25,-8),"frontier":("sprawl",190,30,.5,2),
"airport":("grid",220,0,.55,0),"yaba":("grid",85,10,.15,-15)}
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
out={"size":[W,H],"districts":[],"water":[list(map(tuple,w)) for w in LAYOUT["water"]],"ocean":[list(map(tuple,LAYOUT["ocean"]))],"streets":{},"mains":[],"pois":[],"buildings":{},"parcels":{},"lanes":{},"storeys":{}}   # empty until a district is built
land_all=[]
for (name,ins,act,pts),id_ in zip(D,IDS):
    poly=DPOLY[id_]
    land=poly.difference(water).difference(ocean)
    info=INFO[id_]
    out["districts"].append({"id":id_,"name":name.title().replace("The ","The "),"act":act,"area":round(poly.area*1e-6,2),"poly":[list(map(list,poly.exterior.coords))],**info})
    pat,sp,jit,drop,ang=PAT[id_]
    segs,mains=grid_lines(land,sp,jit,drop,ang,pat)
    inner=land.buffer(-6)
    if GENZONE is not None and not gen_ok(id_): inner=inner.difference(GENZONE)
    lines=[]
    for p,q in segs:
        g=LineString([p,q]).intersection(inner)
        for s in getattr(g,"geoms",[g]):
            if s.geom_type=="LineString" and s.length>8: lines.append([[round(c[0]),round(c[1])] for c in s.coords])
    out["streets"][id_]=lines
    gen=f"web/gen-{id_}.json"
    if gen_ok(id_):  # original street + building generator, calibrated on a pattern study (scripts/gen_fabric.py)
        F=json.load(open(gen))
        out["streets"][id_]=F["streets"]; mains=[]
        for mm in F["mains"]: out["mains"].append({"d":id_,"name":mm["name"],"pts":mm["pts"]})
        out.setdefault("buildings",{})[id_]=F["buildings"]
        if F.get("encroach"): out.setdefault("encroach",[]).extend(dict(z,d=id_) for z in F["encroach"])   # declared zones (market spill), see scripts/cross_sections.py
        out.setdefault("parcels",{})[id_]=F["parcels"]
        out.setdefault("lanes",{})[id_]=F.get("lanes",[])
        if F.get("paths"): out.setdefault("paths",{})[id_]=[p["pts"] for p in F["paths"]]   # footpaths: rail side, canal banks, worn crossings
        if F.get("canal"): out.setdefault("canals",[]).append({"d":id_,"pts":F["canal"],"width":4.0})   # the water: gen_fabric keeps 2 m a side, bank paths at 3 m, houses at 4 m
        if F.get("walls"): out.setdefault("walls",{})[id_]=F["walls"]   # compound walls (the Estate)
        for q in F.get("gates",[]): out.setdefault("gates",[]).append({"d":id_,**q})   # estate gates: a barrier across the street
        for st in F.get("structures",[]):  # flyovers, rail bridges and skywalks drawn above the roads (slip roads are already in mains)
            if st["kind"]!="ramp": out.setdefault("structures",[]).append({"d":id_,**st})
        out.setdefault("storeys",{})[id_]=F.get("storeys") or derive_storeys(F["buildings"],id_)
        if F.get("styles"): out.setdefault("styles",{})[id_]=F["styles"]   # house styles (the Heights)
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
        _bx=poly.buffer(160).bounds
        for i in range(26):
            x=rnd.uniform(_bx[0],_bx[2]); y=rnd.uniform(_bx[1],_bx[3])
            pt=Point(x,y)
            if water.contains(pt) and pt.distance(poly)<160:
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
        if id_ in GEN and p["name"] in GEN[id_].get("poi_from",{}): q["_from"]=GEN[id_]["poi_from"][p["name"]]   # a pin moved to its gate
        out["pois"].append(q)
    land_all.append(land)
# arterials (named), from map02 road calls, in map units
ART=[(a["name"],a["cls"],[tuple(p) for p in a["pts"]]) for a in LAYOUT["arterials"]]   # in metres (layout v2)
out["rail"]={"name":LAYOUT["rail"]["name"],"pts":LAYOUT["rail"]["pts"]}
out["arterials"]=[{"name":n,"cls":c,"pts":[list(p) for p in pts]} for n,c,pts in ART]
_LAG0=Point(12500,4000)   # open lagoon: each ferry pier is the point of its district's shore nearest to it, so the crossing stays on the water
def _ferry(a,b):
    p,q=(nearest_points(DPOLY[k].exterior,_LAG0)[0] for k in (a,b)); return [[round(p.x),round(p.y)],[round(q.x),round(q.y)]]
out["ferries"]=[{"name":"Old Shore – Heights ferry","pts":_ferry("oldshore","heights")},{"name":"Old Shore – Water Town ferry","pts":_ferry("oldshore","watertown")}]
_lag=max(getattr(water,"geoms",[water]),key=lambda g:g.area).representative_point()
out["labels"]=[{"t":"The Lagoon","x":round(_lag.x),"y":round(_lag.y),"k":"water"},{"t":"The Ocean","x":round(W*0.45),"y":round(H-600),"k":"water"},
               {"t":"Farms and bush","x":round(W*0.2),"y":900,"k":"bush"},{"t":"Farms and bush","x":round(W*0.85),"y":700,"k":"bush"}]

# ---- clean the roads (rule-based pass, scripts/roadclean.py) before anything reads them
import roadclean
_st,_skip=roadclean.clean(out,water.union(ocean))
print("road clean:",dict(_st),"skipped",len(_skip))
for _s in _skip: print("  skipped:",_s)

# ---- junctions (scripts/junctions.py): roundabouts where main roads cross, traffic lights, give-way Ts
import junctions
_jr=junctions.junctions(out)
print("junctions:",dict(_jr))
for _j in out["junctions"]:
    if _j["kind"]=="roundabout" and "roads" in _j: print("  new roundabout:",_j["name"],f"r {_j['r']} m at ({_j['x']:.0f}, {_j['y']:.0f}),","/".join(_j["roads"]))

# ---- market streets (scripts/market_streets.py): traders on the walkways and the road round each market, a lane kept clear
import market_streets, hand
_frozen=hand.districts_frozen()   # districts frozen into their hand files: placed by hand from now on (scripts/hand.py)
_lagos_m=[d for d in IDS if gen_ok(d) and json.load(open(f"web/gen-{d}.json")).get("fabric")=="lagos" and d not in _frozen]
print("market streets:",market_streets.market_streets(out,_lagos_m),"| frozen tables:",hand.apply_frozen(out,"tables"))

# ---- road heights (scripts/roadz.py): decks and bridges get height profiles from the terrain, waterfront roads a sea wall
import roadz
water,ocean,_hr=roadz.heights(out,water,ocean,json.load(open("web/terrain.json")))
print("road heights:",_hr["decks"],"decks,",_hr["culverts"],"culverts,",_hr.get("boardwalks",0),"paths made boardwalks,",_hr["quays"],"sea walls on",round(_hr["quay_m"]),"m of road")
for _s in _hr["extended"]: print("  lengthened:",_s)
for _s in _hr["low"]: print("  LOW:",_s)
for _s in _hr["cleared"]: print("  cleared from a bridge landing:",_s)

# ---- street furniture as data (scripts/furniture.py): on walkways only, for districts built to the cross-sections
import furniture
import cross_sections
out["cross_sections"]=cross_sections.SECTIONS   # one table of road widths for the generator, the checks and the kit
_lagos=[d for d in IDS if gen_ok(d) and json.load(open(f"web/gen-{d}.json")).get("fabric")=="lagos"]
print("street furniture:",_lagos,furniture.furniture(out,[d for d in _lagos if d not in _frozen]),"| frozen:",hand.apply_frozen(out,"furniture"))

for _d in out["districts"]:
    if _d["id"] in _lagos: _d["fabric"]="lagos"   # built to the cross-sections: the 2D ground plan draws its roads at true width

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
ART_LINES=[LineString(pts) for _,_,pts in ART]
allp=[Point(p.pop("_from",None) or (p["x"],p["y"])) for p in out["pois"]]   # spaced from where gate pins stood before, so no civic place moves
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
    poly=DPOLY[id_]; land=poly.difference(water).difference(ocean); core=land.buffer(-35)
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
    cnt=dict(zip(ORDER,CIV["counts"].get(id_,[0]*len(ORDER))))   # a new district has no civic counts until it is built
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
    if not gen_ok(id_): continue   # placed at v1 positions: they come back when the district is rebuilt in the v2 frame
    SL=LEFT.get(id_)
    for k in ks:
        pt=Point(k["x"],k["y"])
        if SL:
            q=min(SL,key=lambda q:Point(q["x"],q["y"]).distance(pt)); SL.remove(q); pt=Point(q["x"],q["y"])
        out["pois"].append({"name":k["name"],"type":k["type"],"note":k["note"],"d":id_,"x":round(pt.x),"y":round(pt.y),"civic":True})

# Safe ground (README, the sacred list): churches, mosques, schools, hospitals and clinics, and any place the district model flags "safe"
# (the Palace). Each is marked on its pin, and its plot (its parcel, or else the building its pin stands on) is listed for the game:
# no crime is set there and no chase is routed through it.
SAFE_TYPES={"church","mosque","school","hospital","clinic"}
out["safe_ground"]=[]
for p in out["pois"]:
    if p["type"] in SAFE_TYPES or p.get("safe"): p["safe"]=True
    else: continue
    F=GEN.get(p["d"]); pts=None
    if F and p["name"] in F.get("poi_plot",{}) and not p.get("civic"): pts=F["parcels"][F["poi_plot"][p["name"]]]["pts"]
    elif F:
        pt=Point(p["x"],p["y"]); b=next((b for b in F["buildings"] if Polygon(b[1:]).buffer(0.5).contains(pt)),None)
        if b: pts=b[1:]+[b[1]]
    if pts: out["safe_ground"].append({"name":p["name"],"d":p["d"],"type":p["type"],"pts":pts})
print("safe ground:",sum(1 for p in out["pois"] if p.get("safe")),"places,",len(out["safe_ground"]),"plots")

# Okada ban zones (district model: the Capital, the Port, Old Island, the Heights). The zone is the district less an 8 m band, so its
# edge roads stay rideable: that is where the task force stands. For a built district, every point where a road an okada can use
# enters the zone is a checkpoint site for the game.
BAN_EDGE_M=8
out["okada_ban"]=[]
_ride=[(k,n,g) for k,n,g in walknet.ways_of(out,list(GEN)) if k in ("street","main","arterial")]
for d in out["districts"]:
    if d.get("okada")!="ban": continue
    z=Polygon(d["poly"][0]).buffer(-BAN_EDGE_M); entry={"district":d["id"],"name":d["name"],"edge_m":BAN_EDGE_M,"poly":[list(c) for c in z.exterior.coords],"built":d["id"] in GEN,"checkpoints":[]}
    if d["id"] in GEN:
        cps=[]
        for k,n,g in _ride:
            x=g.intersection(z.exterior)
            for q in getattr(x,"geoms",[x]):
                if q.geom_type!="Point" or any(q.distance(Point(c["x"],c["y"]))<15 for c in cps): continue
                cps.append({"x":round(q.x,1),"y":round(q.y,1),"road":n or k,"kind":k})
        entry["checkpoints"]=sorted(cps,key=lambda c:(c["kind"]!="arterial",c["kind"]!="main",c["x"]))
    out["okada_ban"].append(entry)
print("okada ban zones:",[(e["district"],e["built"],len(e["checkpoints"])) for e in out["okada_ban"]])

# ---- Lagos-isms (scripts/isms.py, hand edits in web/isms-edits.json): placed by rule, after the roads are final and the safe ground is listed
import isms
_ir,_iw=isms.run(out)
print("isms:",{k:{"km":round(sum(s["open_m"]+s["covered_m"] for s in v.values())/1000)} for k,v in _ir.items()},len(out["gutters"]),"gutter runs,",len(out["gutter_crossings"]),"crossings")
for _s in _iw: print("  isms-edits warning:",_s)

def rd(o):
    if isinstance(o,float): return round(o,1)
    if isinstance(o,list): return [rd(x) for x in o]
    if isinstance(o,tuple): return [rd(x) for x in o]
    if isinstance(o,dict): return {k:rd(v) for k,v in o.items()}
    return o
# ---- frozen districts (web/hand/<id>.json): replaced by their snapshot, then their hand edits, last of all (scripts/hand.py)
print("frozen districts:",hand.apply_snapshots(out),"| hand edits:",hand.apply_edits(out))
for mm in out["mains"]:  # labels read left to right
    if mm["pts"][0][0] > mm["pts"][-1][0]: mm["pts"] = mm["pts"][::-1]
s=json.dumps(rd(out),separators=(",",":"),ensure_ascii=False)
open("web/gidi-data.js","w").write("window.GIDI="+s+";")
print(len(s)//1024,"KB", sum(len(v) for v in out["streets"].values()),"street segs",len(out["pois"]),"pois",len(out["mains"]),"mains")
