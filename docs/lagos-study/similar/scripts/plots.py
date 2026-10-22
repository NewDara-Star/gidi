from common import *
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
A=json.load(open('analysis.json')); S=np.array(A['S']); R=A['rows']; N=len(R)
unit=Un['unit']
cen=[centroid(unit==u) for u in range(N)]
def base(ax,box,img_alpha=0.35):
    img=np.ones((ny,nx,4)); img[...,:3]=[0.80,0.88,0.95]
    m=unit>=0; img[m,:3]=0.93; img[m&(F['cover']>=0.10),:3]=0.80
    ax.imshow(img,origin='lower',extent=ext,interpolation='nearest')
    boundaries(ax,unit,'#666',0.5)
    ax.set_xlim(box[:2]); ax.set_ylim(box[2:]); ax.set_xticks([]); ax.set_yticks([])
# ---- similarity.png
cm=plt.cm.RdYlGn; nrm=Normalize(30,90)
def simpanel(ax,box,fs,lab):
    base(ax,box)
    for a,b,ty,e in A['pairs']:
        s=S[a][b]; (xa,ya),(xb,yb)=cen[a],cen[b]
        ax.plot([xa,xb],[ya,yb],color=cm(nrm(s)),lw=1+4*max(s-30,0)/60,ls='-' if ty=='land' else '--',zorder=3)
        if lab:
            mx,my=(xa+xb)/2,(ya+yb)/2
            if box[0]<mx<box[1] and box[2]<my<box[3]:
                ax.text(mx,my,'%d'%round(s),fontsize=fs,ha='center',va='center',zorder=5,bbox=dict(boxstyle='round,pad=0.08',fc='white',alpha=0.8,lw=0))
    for u in range(N):
        x,y=cen[u]
        if box[0]<x<box[1] and box[2]<y<box[3]:
            ax.plot(x,y,'o',ms=4,color='k',zorder=4); ax.text(x,y+0.35,R[u]['name'],fontsize=fs-1,ha='center',zorder=5,color='#222')
fig=plt.figure(figsize=(22,26))
a=fig.add_axes([0.01,0.78,0.98,0.20]); simpanel(a,STATE,5,False); a.set_title('Neighbour links coloured by similarity % (red 30 or less, green 90). Dashed = across water (<= 750 m)',fontsize=12)
a=fig.add_axes([0.01,0.40,0.98,0.37]); simpanel(a,CORE,7,True); a.set_title('Metro',fontsize=12)
a=fig.add_axes([0.01,0.01,0.98,0.38]); simpanel(a,INNER,9,True); a.set_title('Inner metro',fontsize=12)
sm=plt.cm.ScalarMappable(norm=nrm,cmap=cm); cb=fig.colorbar(sm,cax=fig.add_axes([0.93,0.42,0.012,0.3])); cb.set_label('similarity %')
fig.savefig('similarity.png',dpi=80); plt.close(fig)
# ---- ladder pictures
pal=list(plt.cm.tab20.colors)+list(plt.cm.tab20b.colors)+list(plt.cm.Set3.colors)
for t in ('85','75','65'):
    lab=np.array(A['lab'][t]); nd_=lab.max()+1
    dmap=np.where(unit>=0,lab[np.maximum(unit,0)],-1)
    def dpanel(ax,box,fs):
        img=np.ones((ny,nx,4)); img[...,:3]=[0.80,0.88,0.95]
        m=dmap>=0
        cols=np.array([pal[(k*5)%len(pal)] for k in range(nd_)])
        img[m,:3]=cols[dmap[m]]*0.75+0.25; bl=m&(F['cover']>=0.10); img[bl,:3]=cols[dmap[bl]]
        ax.imshow(img,origin='lower',extent=ext,interpolation='nearest')
        boundaries(ax,unit,'#777',0.3); boundaries(ax,dmap,'k',1.4)
        for d in range(nd_):
            mem=[u for u in range(N) if lab[u]==d]
            big=max(mem,key=lambda u:R[u]['built_km2']); x,y=cen[big]
            if box[0]<x<box[1] and box[2]<y<box[3]:
                txt='D%d %s'%(d+1,R[big]['name'])+(' +%d'%(len(mem)-1) if len(mem)>1 else '')
                ax.text(x,y,txt,fontsize=fs,ha='center',va='center',bbox=dict(boxstyle='round,pad=0.1',fc='white',alpha=0.8,lw=0))
        ax.set_xlim(box[:2]); ax.set_ylim(box[2:]); ax.set_xticks([]); ax.set_yticks([])
    fig=plt.figure(figsize=(22,26))
    a=fig.add_axes([0.01,0.78,0.98,0.20]); dpanel(a,STATE,6); a.set_title('Districts at similarity >= %s%%: %d districts (thick lines; thin = units; label = biggest unit +n others; full lists in SIMILAR.md)'%(t,nd_),fontsize=12)
    a=fig.add_axes([0.01,0.40,0.98,0.37]); dpanel(a,CORE,8); a.set_title('Metro',fontsize=12)
    a=fig.add_axes([0.01,0.01,0.98,0.38]); dpanel(a,INNER,10); a.set_title('Inner metro',fontsize=12)
    fig.savefig('ladder_%s.png'%t,dpi=80); plt.close(fig)
print('ok')
