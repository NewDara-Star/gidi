# Per-LGA building height stats from Google Open Buildings 2.5D (2023), read at ~4 m (the data's effective resolution).
import rasterio, numpy as np, json, os, sys
from rasterio.features import rasterize
from shapely.geometry import shape, box
D=os.path.expanduser('~/mnt/gidi-data/research/data/')
L=json.load(open(D+'lagos_lgas_utm31.geojson'))['features']
lg=[(f['properties']['name'],shape(f['geometry'])) for f in L]
OUT=os.path.expanduser('~/gidi-work/tiles/'); os.makedirs(OUT,exist_ok=True)
BINS=[0,4.5,7.5,10.5,13.5,20,40,200]
tiles=sorted(f for f in os.listdir(D+'open-buildings-2023') if f.endswith('.tif'))
budget=float(sys.argv[1]) if len(sys.argv)>1 else 35
import time; t0=time.time()
for t in tiles:
    o=OUT+t+'.json'
    if os.path.exists(o): continue
    if time.time()-t0>budget: break
    r=rasterio.open(D+'open-buildings-2023/'+t); n=3125
    tb=box(*r.bounds); res={}
    hits=[(nm,g) for nm,g in lg if g.intersects(tb)]
    if hits:
        cnt,H,P=r.read(out_shape=(3,n,n),resampling=rasterio.enums.Resampling.nearest)
        tf=r.transform*r.transform.scale(r.width/n,r.height/n)
        for nm,g in hits:
            m=rasterize([(g,1)],out_shape=(n,n),transform=tf,dtype='uint8').astype(bool)
            px=m.sum()
            if px==0: continue
            b=m&(P>=0.5)&(H>0)
            h=H[b]
            res[nm]={'px':int(px),'built':int(b.sum()),'hist':np.histogram(h,BINS)[0].tolist(),
                     'hsum':float(h.sum()),'count':float(cnt[m&(cnt>0)].sum()*(r.width/n)**2)}
    json.dump(res,open(o,'w')); print('done',t,len(res),round(time.time()-t0,1))
print('remaining',len([t for t in tiles if not os.path.exists(OUT+t+'.json')]))
