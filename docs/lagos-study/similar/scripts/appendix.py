# Appendix A and B of SIMILAR.md (unit fingerprints, neighbour pairs) from analysis.json.
import json, csv, numpy as np
A=json.load(open('analysis.json')); R=A['rows']; S=np.array(A['S'])
CLS=list(np.load('../lagos/class.npz')['names'])
short={'dense inner core (1-3 storeys)':'dense core','dense outer sprawl (bungalows)':'dense sprawl','suburban bungalow belt':'bungalow belt','planned or surveyed grid':'grid','low-density villa & new estate':'villa/estate','industry & warehouses':'industry','port & tank farm':'port','open land (bush/farm)':'open','swamp & mangrove':'swamp','scattered new build':'scattered','waterfront & stilts':'stilts','towers & mid-rise':'towers','dense grid tenement':'grid tenement','military & barracks':'military'}
o=['## Appendix A. Unit fingerprints\n','Full numbers, all 17 class shares and the knowledge lists: `units.csv`. Here: the main columns. Densities are per km² of built cells (roof cover >= 10%). Classes: the three biggest shares of the unit\'s land.\n',
'| # | Unit | LGA | Land km² | Built km² | Bldg/km² | Median roof m² | Big-roof % | Height m | 4+ % | Grid | People/km² | Street km/km² | Major % | Top classes | Markets K/OV | Hubs K/OV | Landmarks K | Rich | Distinct % |','|'+'---|'*20]
for r in R:
    sh=sorted(((r['c%02d'%q],q) for q in range(17)),reverse=True)[:3]
    tc=', '.join('%s %d'%(short.get(CLS[q],CLS[q]),round(100*v)) for v,q in sh if v>=0.05)
    o.append('| %d | %s | %s | %.0f | %.1f | %d | %d | %d | %.1f | %.0f | %.2f | %d | %.1f | %d | %s | %d/%d | %d/%d | %d | %.0f | %.0f |'%(r['id'],r['name'],r['lga'],r['land_km2'],r['built_km2'],r['bldg_per_km2'],r['median_foot_m2'],round(100*r['big_share']),r['height_m'],100*r['share4'],r['grid'],r['pop_per_built_km2'],r['street_km_per_km2'],round(100*r['major_share']),tc,r['k_markets'],r['ov_markets'],r['k_hubs'],r['ov_transit'],r['k_landmarks'],r['richness'],r['distinct_pct']))
o.append('\n## Appendix B. All neighbour pairs, most alike first\n')
o.append('Land = the units touch. Water = across 750 m of water or less. Also in `pairs.csv` (with the two parts of the distance).\n')
o.append('| Unit A | Unit B | Link | Similarity % |'); o.append('|---|---|---|---|')
for a,b,ty,e in sorted(A['pairs'],key=lambda p:-S[p[0]][p[1]]):
    o.append('| %s | %s | %s | %.0f |'%(R[a]['name'],R[b]['name'],ty,S[a][b]))
o.append('\n## Appendix C. The merge ladder, step by step\n')
o.append('Each step joins the two touching groups that are most alike on average. Also in `ladder.csv`. A step can score a little higher than the one before it (average linkage does that); the threshold counts stop at the first step below the line.\n')
o.append('| Step | Similarity % | Joins | With | Districts after |'); o.append('|---|---|---|---|---|')
for s in A['steps']:
    f=lambda x: x if len(x)<90 else x.split(' + ')[0]+' + %d more'%(len(x.split(' + '))-1)
    o.append('| %d | %.1f | %s | %s | %d |'%(s['step'],s['sim'],f(s['a']),f(s['b']),s['count_after']))
o.append('\n## Appendix D. Districts at each threshold\n')
o.append(open('districts.md').read())
open('appendix.md','w').write('\n'.join(o))
print('ok')
