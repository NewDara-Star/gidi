import numpy as np, json, csv
from scipy import ndimage as nd
Rw=json.load(open('finger.json')); N=len(Rw)
Un=dict(np.load('units.npz')); unit=Un['unit']; area=Un['area']
K=dict(np.load('../lagos/class.npz')); CLS=list(K['names'])
# ---- fingerprint vectors
MET=[('bldg_per_km2','log'),('median_foot_m2','log'),('big_share','lin'),('height_m','lin'),('share4','sqrt'),('grid','lin'),
     ('pop_per_built_km2','log'),('street_km_per_km2','lin'),('major_share','lin'),('built_share','lin'),('roof_cover','lin'),('poi_per_km2','log')]
def tr(v,t): return np.log1p(v) if t=='log' else (np.sqrt(v) if t=='sqrt' else v)
M=np.array([[tr(float(r[k]),t) for k,t in MET] for r in Rw])
Z=np.clip((M-M.mean(0))/M.std(0),-3,3)
Pc=np.array([[r['c%02d'%q] for q in range(17)] for r in Rw]); Pc=Pc/Pc.sum(1,keepdims=True)
Sq=np.sqrt(Pc)
Hd=np.sqrt(((Sq[:,None,:]-Sq[None,:,:])**2).sum(-1)/2)          # Hellinger, 0..1
Md=np.sqrt(((Z[:,None,:]-Z[None,:,:])**2).mean(-1))              # RMS z difference
iu=np.triu_indices(N,1)
H95=Hd[iu].max(); M95=Md[iu].max()   # normalise by the most unlike pair of units in Lagos
import os; WC=float(os.environ.get('WCLASS','0.5'))
D=WC*np.minimum(Hd/H95,1)+(1-WC)*np.minimum(Md/M95,1)
S=100*(1-D)
print('H95 %.3f M95 %.3f'%(H95,M95))
# ---- neighbours: shared land edge, or across <=750 m of water
F=dict(np.load('../lagos/feat.npz')); water=(~area)&((K['cl']==0)|(F['water']>0.5))   # real water only
adj={}
for a,b in [(unit[:,1:],unit[:,:-1]),(unit[1:,:],unit[:-1,:])]:
    m=(a>=0)&(b>=0)&(a!=b)
    for p,q in zip(a[m],b[m]):
        k=(min(p,q),max(p,q)); adj[k]=adj.get(k,0)+1
wl=set()
for u in range(N):
    mu=unit==u
    g=nd.binary_dilation(mu,iterations=3,mask=mu|water)
    ring=nd.binary_dilation(g)&~mu&(unit>=0)
    for v in np.unique(unit[ring]):
        k=(min(u,v),max(u,v))
        if k not in adj: wl.add(k)
pairs=[]
for k,e in adj.items(): pairs.append((int(k[0]),int(k[1]),'land',float(e*0.25)))
for k in wl: pairs.append((int(k[0]),int(k[1]),'water',0.0))
nb={u:set() for u in range(N)}
for a,b,_,_ in pairs: nb[a].add(b); nb[b].add(a)
# ---- distinctiveness, richness
for u,r in enumerate(Rw):
    s=[S[u,v] for v in nb[u]]
    r['nbrs']=len(s); r['most_alike_nbr']=Rw[max(nb[u],key=lambda v:S[u,v])]['name'] if s else ''
    r['max_nbr_sim']=round(max(s),1) if s else 0; r['distinct_pct']=round(100-max(s),1) if s else 100
    r['mean_unlike_pct']=round(100-np.mean(s),1) if s else 100
    p=np.array([r['c%02d'%q] for q in range(17)]); p[[0,6,7]]=0; p=p/max(p.sum(),1e-9); p=p[p>0]
    r['eff_classes']=round(float(np.exp(-(p*np.log(p)).sum())),2)
kf=np.log1p(np.array([r['k_markets']+r['k_hubs']+r['k_landmarks'] for r in Rw]))
of=np.log1p(np.array([r['ov_markets']+r['ov_transit']+r['ov_campus'] for r in Rw]))
dv=np.array([r['eff_classes'] for r in Rw])
rich=100*(0.4*dv/dv.max()+0.4*kf/kf.max()+0.2*of/of.max())
for u,r in enumerate(Rw): r['richness']=round(float(rich[u]),1)
# ---- contiguity-constrained average-linkage merging
cl={u:[u] for u in range(N)}; cn={u:set(nb[u]) for u in range(N)}
def csim(a,b): return float(np.mean(S[np.ix_(cl[a],cl[b])]))
steps=[]; snaps={N:{k:list(v) for k,v in cl.items()}}
nxt=N
while len(cl)>1:
    best=None
    for a in cl:
        for b in cn[a]:
            if a<b:
                s=csim(a,b)
                if best is None or s>best[0]: best=(s,a,b)
    if best is None: break
    s,a,b=best
    steps.append(dict(step=len(steps)+1,sim=round(s,1),a=' + '.join(Rw[x]['name'] for x in cl[a]),b=' + '.join(Rw[x]['name'] for x in cl[b]),count_after=len(cl)-1))
    cl[nxt]=cl.pop(a)+cl.pop(b); cn[nxt]=(cn.pop(a)|cn.pop(b))-{a,b}
    for c in cn[nxt]: cn[c]=(cn[c]-{a,b})|{nxt}
    nxt+=1; snaps[len(cl)]={k:list(v) for k,v in cl.items()}
# count at threshold: stop at the first merge whose similarity is below t
TH=[90,85,80,75,70,65,60,55,50]
cut={}
for t in TH:
    k=next((i for i,s in enumerate(steps) if s['sim']<t),len(steps))
    cut[t]=N-k
lab_at={}
for t in TH:
    sn=snaps[cut[t]]; lab=np.full(N,-1)
    for i,(k,mem) in enumerate(sorted(sn.items(),key=lambda kv:-sum(Rw[m]['built_km2'] for m in kv[1]))):
        lab[mem]=i
    lab_at[t]=lab
json.dump(dict(S=S.round(2).tolist(),pairs=pairs,steps=steps,cut=cut,lab={t:lab_at[t].tolist() for t in TH},rows=Rw,H95=float(H95),M95=float(M95),MET=MET),open('analysis.json','w'))
# ---- tables
cols=['id','name','lga','land_km2','built_km2','built_share','bldg','bldg_per_km2','roof_cover','median_foot_m2','big_share','height_m','share4','grid','pop','pop_per_built_km2','street_km_per_km2','major_share','poi_per_km2','ov_markets','ov_transit','ov_campus','ov_industry','k_markets','k_hubs','k_landmarks','eff_classes','richness','nbrs','max_nbr_sim','most_alike_nbr','distinct_pct','mean_unlike_pct']+['c%02d'%q for q in range(17)]+['k_list']
with open('units.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(cols[:-18]+['%% %s'%c for c in CLS]+['k_list (knowledge)'])
    for r in Rw: w.writerow([r[c] for c in cols])
with open('pairs.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['unit_a','unit_b','link','shared_edge_km','similarity_pct','class_part_hellinger','metric_part_rms_z'])
    for a,b,ty,e in sorted(pairs,key=lambda p:-S[p[0],p[1]]):
        w.writerow([Rw[a]['name'],Rw[b]['name'],ty,e,round(S[a,b],1),round(Hd[a,b],3),round(Md[a,b],2)])
with open('ladder.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['step','similarity_pct','group_a','group_b','districts_after'])
    for s in steps: w.writerow([s['step'],s['sim'],s['a'],s['b'],s['count_after']])
ps=np.array([S[a,b] for a,b,_,_ in pairs])
print('pairs',len(pairs),'land',len(adj),'water',len(wl)); print('neighbour sim pct: min %.0f p10 %.0f p25 %.0f med %.0f p75 %.0f p90 %.0f max %.0f'%tuple([ps.min()]+list(np.percentile(ps,[10,25,50,75,90]))+[ps.max()]))
print(cut)
