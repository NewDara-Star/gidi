# SIMILAR.md's ladder: how many districts at each similarity threshold, from analysis.json.
import json, numpy as np
A=json.load(open('analysis.json')); R=A['rows']; N=len(R); S=np.array(A['S'])
flag=lambda r: r['distinct_pct']>=35 or r['richness']>=70
TH=['90','85','80','75','70','65','60','55','50']
out=[]; summ=[]
for t in TH:
    lab=np.array(A['lab'][t]); nd_=lab.max()+1
    alone=[R[u]['name'] for u in range(N) if flag(R[u]) and (lab==lab[u]).sum()==1]
    fold=0
    for d in range(nd_):
        mem=[u for u in range(N) if lab[u]==d]
        if sum(R[u]['built_km2'] for u in mem)<3 and max(R[u]['richness'] for u in mem)<70: fold+=1
    summ.append((t,int(nd_),int(nd_-fold),len(alone)))
    if t=='50': continue
    out.append('\n### At %s%%: %d districts (%d after folding tiny plain units)\n'%(t,nd_,nd_-fold))
    out.append('Rich or distinct units still alone (%d): %s.\n'%(len(alone),', '.join(alone) if alone else 'none'))
    out.append('| D | Members (units) | Land km² | Built km² | Built at 1:3, km² | Inner similarity % |')
    out.append('|---|---|---|---|---|---|')
    for d in range(nd_):
        mem=[u for u in range(N) if lab[u]==d]
        land=sum(R[u]['land_km2'] for u in mem); bu=sum(R[u]['built_km2'] for u in mem)
        if len(mem)>1:
            iu=[S[a][b] for i,a in enumerate(mem) for b in mem[i+1:]]; ins='%.0f'%np.mean(iu)
        else: ins='-'
        out.append('| %d | %s | %.0f | %.1f | %.1f | %s |'%(d+1,', '.join(R[u]['name'] for u in mem),land,bu,bu/9,ins))
open('districts.md','w').write('\n'.join(out))
print(summ); json.dump(summ,open('summary.json','w'))
tb=sum(r['built_km2'] for r in R); tl=sum(r['land_km2'] for r in R); print('total land',tl,'built',tb, tb/9)
fl=[r['name'] for r in R if flag(r)]; print(len(fl),fl)
