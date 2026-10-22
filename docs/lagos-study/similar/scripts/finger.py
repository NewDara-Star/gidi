# Per-unit fingerprint from the 250 m grids + Overture places + knowledge lists.
import numpy as np, json, csv, re, pyarrow.parquet as pq, shapely
from scipy import ndimage as nd
from pyproj import Transformer
from know import KNOW, items
L='../lagos/'
T=Transformer.from_crs(4326,32631,always_xy=True)
F=dict(np.load(L+'feat.npz')); K=dict(np.load(L+'class.npz')); B=dict(np.load(L+'bgrid65.npz')); H=dict(np.load(L+'hgrid.npz')); R=dict(np.load(L+'rgrid.npz'))
Un=dict(np.load('units.npz')); unit=Un['unit']; NAMES=json.load(open('unit_names.json')); N=len(NAMES)
x0,y0=float(F['x0']),float(F['y0']); ny,nx=unit.shape
CLS=list(K["names"]); cl=K["cl"].copy(); _i=nd.distance_transform_edt(cl<0,return_distances=False,return_indices=True); cl=np.where(cl<0,cl[_i[0],_i[1]],cl)  # gap cells between rough LGA polygons take the nearest class
built=F['cover']>=0.10
# Overture places (confidence >= 0.5)
P={k:np.zeros(N) for k in ('poi','market','transit','campus','industry','worship','hotel')}
t=pq.read_table('/Users/Star/Real-world/research/data/overture-lagos/lagos_overture_place.parquet',columns=['geometry','confidence','basic_category','names']).to_pylist()
for r in t:
    if (r['confidence'] or 0)<0.5: continue
    g=shapely.from_wkb(r['geometry']); x,y=T.transform(g.x,g.y); i=int((y-y0)//250); j=int((x-x0)//250)
    if not(0<=i<ny and 0<=j<nx) or unit[i,j]<0: continue
    u=unit[i,j]; c=r['basic_category'] or ''; nm=((r['names'] or {}).get('primary') or '').lower()
    P['poi'][u]+=1
    if c in('market','farmers_market') or re.search(r'\bmarket\b',nm): P['market'][u]+=1
    if c in('public_transit_facility_or_service','train_station') or re.search(r'motor park|bus terminal|bus station|\bbrt\b|jetty|ferry terminal',nm): P['transit'][u]+=1
    if c in('college_university',): P['campus'][u]+=1
    if c in('manufacturer',): P['industry'][u]+=1
rows=[]
for u in range(N):
    m=unit==u; mb=m&built; land=m.sum()/16; bk=max(mb.sum()/16,1/16)
    sh=np.bincount(cl[m],minlength=17)/m.sum()
    hist=B['hist'][:,mb].sum(1); c=np.cumsum(hist); k=int(np.argmax(c>=c[-1]/2)) if c[-1] else 0
    prev=c[k-1] if k else 0; frac=(c[-1]/2-prev)/max(hist[k],1); medfoot=2**(k+3+frac)
    a=B['a'][m].sum(); bp=H['bp'][m].sum()
    g=K['grid'][mb]; w=F['n'][mb]
    kn=KNOW.get(NAMES[u],('','',''))
    r=dict(id=u+1,name=NAMES[u],
      lga=str(F['names'][np.bincount(Un['lgaf'][m]).argmax()]),
      land_km2=round(land,1),built_km2=round(bk,1),built_share=round(mb.sum()/m.sum(),3),
      bldg=int(F['n'][m].sum()),bldg_per_km2=int(F['n'][mb].sum()/bk),roof_cover=round(B['a'][mb].sum()/(bk*1e6),3),
      median_foot_m2=round(medfoot,0),big_share=round(B['bigA'][m].sum()/max(a,1),3),
      height_m=round(H['hs'][m].sum()/max(bp,1),2),share4=round(H['h4'][m].sum()/max(bp,1),3),
      grid=round(float((g*w).sum()/max(w.sum(),1)),3),
      pop=int(F['pop'][m].sum()),pop_per_built_km2=int(F['pop'][mb].sum()/bk),
      street_km_per_km2=round(R['L'][mb].sum()/1000/bk,1),major_share=round(R['Lmaj'][m].sum()/max(R['L'][m].sum(),1),3),
      poi_per_km2=round(P['poi'][u]/bk,1),
      ov_markets=int(P['market'][u]),ov_transit=int(P['transit'][u]),ov_campus=int(P['campus'][u]),ov_industry=int(P['industry'][u]),
      k_markets=len(items(kn[0])),k_hubs=len(items(kn[1])),k_landmarks=len(items(kn[2])),
      k_list='; '.join(x for x in (kn[0],kn[1],kn[2]) if x))
    for q,nm in enumerate(CLS): r['c%02d'%q]=round(float(sh[q]),4)
    rows.append(r)
json.dump(rows,open('finger.json','w'),indent=0)
print(len(rows)); print(rows[0])
