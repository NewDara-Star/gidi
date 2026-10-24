# Per-LGA land cover (ESA WorldCover 2021), surface height (Copernicus DSM), population (WorldPop 2020).
import rasterio, numpy as np, json, os, glob
from rasterio.mask import mask
from rasterio.merge import merge
from shapely.geometry import shape, mapping
from shapely.ops import transform
from pyproj import Transformer
D=os.path.expanduser('~/mnt/gidi-data/research/data/')
inv=Transformer.from_crs(32631,4326,always_xy=True).transform
L=[(f['properties']['name'],transform(inv,shape(f['geometry']))) for f in json.load(open(D+'lagos_lgas_utm31.geojson'))['features']]
WC={10:'trees',20:'shrub',30:'grass',40:'crops',50:'built',60:'bare',80:'water',90:'wetland',95:'mangrove'}
wc=[rasterio.open(f) for f in sorted(glob.glob(D+'worldcover/*.tif'))]
dem=[rasterio.open(f) for f in sorted(glob.glob(D+'dem/*.tif'))]
pop=rasterio.open(D+'worldpop/nga_ppp_2020_UNadj_constrained.tif')
def clip(srcs,g):
    out=[]
    for s in srcs:
        try: a,_=mask(s,[mapping(g)],crop=True,filled=True,nodata=s.nodata if s.nodata is not None else 0); out.append(a[0])
        except ValueError: pass
    return out
res={}
for nm,g in L:
    r={}
    cnt={}
    for a in clip(wc,g):
        v,c=np.unique(a,return_counts=True)
        for vv,cc in zip(v,c):
            if vv in WC: cnt[WC[vv]]=cnt.get(WC[vv],0)+int(cc)
    tot=sum(cnt.values()); land=tot-cnt.get('water',0)
    r['cover_pct_of_land']={k:round(v/land*100,1) for k,v in cnt.items() if k!='water'} if land else {}
    r['water_pct_of_area']=round(cnt.get('water',0)/tot*100,1) if tot else None
    r['land_km2']=round(land*100/1e6,1)  # 10 m pixels
    hs=[a[(a>-50)&(a<500)] for a in clip(dem,g)]
    h=np.concatenate(hs) if hs else np.array([])
    if h.size: r['surface_m']={'p10':round(float(np.percentile(h,10)),1),'p50':round(float(np.percentile(h,50)),1),'p90':round(float(np.percentile(h,90)),1),'share_below_3m':round(float((h<3).mean()*100),1),'share_below_5m':round(float((h<5).mean()*100),1)}
    pa=clip([pop],g)
    if pa:
        p=pa[0]; p=p[p>0]; r['population_2020']=int(p.sum())
        if r['land_km2']: r['people_per_land_km2']=int(p.sum()/r['land_km2'])
        r['busiest_100m_cell']=int(p.max()) if p.size else 0
    res[nm]=r; print(nm, r.get('people_per_land_km2'), r['cover_pct_of_land'].get('trees'), r.get('surface_m',{}).get('share_below_5m'), flush=True)
json.dump(res,open(os.path.expanduser('~/gidi-work/landpop_by_lga.json'),'w'),indent=1)
