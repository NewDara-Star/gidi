# Shared by the similarity study's plot scripts: the grids, the units, the LGA lines. Needs the grids in ../lagos/ (feat.npz, class.npz), which were never committed and are lost (decisions/CODEBASE.md).
import numpy as np, json, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import shape
from pyproj import Transformer
L='../lagos/'
T=Transformer.from_crs(4326,32631,always_xy=True)
F=dict(np.load(L+'feat.npz')); K=dict(np.load(L+'class.npz')); Un=dict(np.load('units.npz'))
x0,y0=float(F['x0']),float(F['y0']); ny,nx=F['n'].shape
ext=[x0/1000,(x0+nx*250)/1000,y0/1000,(y0+ny*250)/1000]
NAMES=json.load(open('unit_names.json'))
lg=json.load(open('/Users/Star/gidi-data/research/data/lagos_lgas_utm31.geojson'))['features']
def draw_lga(ax,lw=0.5,c='#555'):
    for f in lg:
        g=shape(f['geometry']); gs=g.geoms if g.geom_type=='MultiPolygon' else [g]
        for p in gs:
            x,y=p.exterior.xy; ax.plot(np.array(x)/1000,np.array(y)/1000,color=c,lw=lw,ls=':')
def boundaries(ax,lab,color='k',lw=0.6):
    # draw cell edges where label changes
    segs=[]
    a=lab
    d=(a[:,1:]!=a[:,:-1])&((a[:,1:]>=0)|(a[:,:-1]>=0))
    ii,jj=np.nonzero(d)
    for i,j in zip(ii,jj):
        x=(x0+(j+1)*250)/1000; segs.append([(x,(y0+i*250)/1000),(x,(y0+(i+1)*250)/1000)])
    d=(a[1:,:]!=a[:-1,:])&((a[1:,:]>=0)|(a[:-1,:]>=0))
    ii,jj=np.nonzero(d)
    for i,j in zip(ii,jj):
        y=(y0+(i+1)*250)/1000; segs.append([((x0+j*250)/1000,y),((x0+(j+1)*250)/1000,y)])
    from matplotlib.collections import LineCollection
    ax.add_collection(LineCollection(segs,colors=color,lw=lw))
def centroid(m):
    if (m&(F['cover']>=0.10)).sum()>=4: m=m&(F['cover']>=0.10)   # place label on the built part
    ii,jj=np.nonzero(m)
    # pick the member cell nearest the mean (keeps label inside the unit)
    ci,cj=ii.mean(),jj.mean(); k=np.argmin((ii-ci)**2+(jj-cj)**2)
    return (x0+(jj[k]+.5)*250)/1000,(y0+(ii[k]+.5)*250)/1000
STATE=(ext[0]+1,ext[1]-1,ext[2]+1,ext[3]-1)
_a=T.transform(3.08,6.39); _b=T.transform(3.66,6.70)
CORE=(_a[0]/1000,_b[0]/1000,_a[1]/1000,_b[1]/1000)
_a=T.transform(3.27,6.42); _b=T.transform(3.47,6.66)
INNER=(_a[0]/1000,_b[0]/1000,_a[1]/1000,_b[1]/1000)
