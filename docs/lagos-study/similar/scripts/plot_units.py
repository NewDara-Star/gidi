# Map of the study units (SIMILAR.md's unit pictures), drawn with common.py.
from common import *
from matplotlib.colors import ListedColormap
unit=Un['unit']; n=len(NAMES)
pal=plt.cm.tab20(np.linspace(0,1,20)); cols=np.array([pal[(k*7)%20] for k in range(n)])
def panel(ax,box,fs,title):
    img=np.ones((ny,nx,4)); img[...,:3]=[0.80,0.88,0.95]
    m=unit>=0; img[m]=cols[unit[m]]; img[m,3]=0.55
    bl=F['cover']>=0.10; img[m&bl,3]=0.85
    ax.imshow(img,origin='lower',extent=ext,interpolation='nearest')
    boundaries(ax,unit,'k',0.7); draw_lga(ax)
    for u in range(n):
        mm=unit==u
        if not mm.any(): continue
        x,y=centroid(mm)
        if box[0]<x<box[1] and box[2]<y<box[3]:
            ax.text(x,y,'%d %s'%(u+1,NAMES[u]),fontsize=fs,ha='center',va='center',bbox=dict(boxstyle='round,pad=0.1',fc='white',alpha=0.75,lw=0))
    ax.set_xlim(box[:2]); ax.set_ylim(box[2:]); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(title,fontsize=12)
fig=plt.figure(figsize=(22,26))
panel(fig.add_axes([0.01,0.78,0.98,0.20]),STATE,6,'81 units over all Lagos land (darker = built cells, roof cover >= 10%). Dotted: LGA polygons. Numbers match units.csv')
panel(fig.add_axes([0.01,0.40,0.98,0.37]),CORE,8,'Metro')
panel(fig.add_axes([0.01,0.01,0.98,0.38]),INNER,10,'Inner metro (Oshodi to the Island)')
fig.savefig('units.png',dpi=80)
