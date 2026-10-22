# Draw units: road- and council-penalised nearest-seed growth over 250 m land cells.
import numpy as np, pickle, heapq, json
from scipy import ndimage as nd
from pyproj import Transformer
import seeds
L='../lagos/'
T=Transformer.from_crs(4326,32631,always_xy=True)
F=dict(np.load(L+'feat.npz')); K=dict(np.load(L+'class.npz'))
x0,y0=float(F['x0']),float(F['y0']); ny,nx=F['n'].shape; C=250
lga=F['lga']
inlga=nd.binary_fill_holes(nd.binary_closing(lga>=0,iterations=3))|(lga>=0)
water=(K['cl']==0)|((lga<0)&(F['water']>0.5))
area=inlga&~water           # study area: every land cell of the 20 LGAs (gaps between rough polygons filled)
# fill lga id for gap cells from nearest lga cell
idx=nd.distance_transform_edt(lga<0,return_distances=False,return_indices=True)
lgaf=lga[idx[0],idx[1]]
# big-road raster: motorway / trunk / primary (no links, no planned roads)
PL=('Fourth Mainland Bridge','Fourth Mainland Road','4MB Link Road','Lagoon Highway','7th Axial Road','Third Axial Road','Lagos-Calabar Coastal Highway','Omu Creek Road','Lekki Regional Road')
road=np.zeros((ny,nx),bool); rail=np.zeros((ny,nx),bool)
for st,cl,nm,fl,cs in pickle.load(open(L+'major.pkl','rb')):
    if len(cs)<2 or nm in PL: continue
    big = st=='road' and cl in ('motorway','trunk','primary')
    if not (big or st=='rail'): continue
    a=np.array(cs)[:,:2]
    for p,q in zip(a[:-1],a[1:]):
        k=max(int(np.hypot(*(q-p))/60),1)
        for t in np.linspace(0,1,k+1):
            x,y=p+(q-p)*t; i=int((y-y0)//C); j=int((x-x0)//C)
            if 0<=i<ny and 0<=j<nx:
                (road if big else rail)[i,j]=True
U=seeds.load()
cost=np.ones((ny,nx)); cost[road]+=2.0; cost[rail]+=1.0; cost[~area]=8.0   # water / outside: costly but passable
INF=1e18; dist=np.full((ny,nx),INF); lab=np.full((ny,nx),-1)
h=[]
for u,(nm,pts) in enumerate(U):
    for la,lo in pts:
        x,y=T.transform(lo,la); i=int((y-y0)//C); j=int((x-x0)//C)
        dist[i,j]=0; lab[i,j]=u; heapq.heappush(h,(0.0,i,j,u))
while h:
    d,i,j,u=heapq.heappop(h)
    if d>dist[i,j] or lab[i,j]!=u: continue
    for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
        a,b=i+di,j+dj
        if 0<=a<ny and 0<=b<nx and (area[a,b] or dist[a,b]<INF or True):
            if not (inlga[a,b] or water[a,b]): continue
            c=cost[a,b]+(4.0 if lgaf[a,b]!=lgaf[i,j] else 0.0)
            nd_=d+c
            if nd_<dist[a,b]:
                dist[a,b]=nd_; lab[a,b]=u; heapq.heappush(h,(nd_,a,b,u))
unit=np.where(area,lab,-1)
print('unassigned area cells',int((area&(unit<0)).sum()))
# tidy: cells whose unit piece is a small detached fragment (<4 cells) join the unit they touch most
for it in range(3):
    ch=0
    for u in range(len(U)):
        lb,n=nd.label(unit==u)
        if n<=1: continue
        sz=nd.sum(np.ones_like(lb),lb,range(1,n+1)); keep=np.argmax(sz)+1
        for k in range(1,n+1):
            if k==keep or sz[k-1]>=16: continue
            m=lb==k; ring=nd.binary_dilation(m)&~m&(unit>=0)&(unit!=u)
            if ring.any():
                unit[m]=np.bincount(unit[ring]).argmax(); ch+=1
    if not ch: break
np.savez_compressed('units.npz',unit=unit,area=area,road=road,rail=rail,lgaf=lgaf)
json.dump([nm for nm,_ in U],open('unit_names.json','w'))
for u,(nm,_) in enumerate(U):
    m=unit==u; print('%-45s %7.1f km2  built %6.1f  lga %s'%(nm,m.sum()/16,(m&(F['cover']>=0.10)).sum()/16,
       F['names'][np.bincount(lgaf[m]).argmax()] if m.any() else '-'))
