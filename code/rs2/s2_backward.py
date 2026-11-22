import json,urllib.request,time
seeds=['10.1109/ojies.2020.3040412','10.1109/tii.2011.2123907','10.1007/s40435-020-00638-7','10.1016/j.neucom.2023.126896','10.1016/j.jai.2025.06.001','10.3390/act14030108','10.1016/j.arcontrol.2022.07.001','10.3390/robotics14080101','10.1016/j.arcontrol.2022.07.003','10.1109/jestie.2021.3087938','10.1007/s00521-017-3144-z','10.3390/act12080332','10.3934/mbe.2022120','10.1017/s0263574720000223','10.1016/j.arcontrol.2018.10.009','10.1016/j.arcontrol.2019.08.004','10.1177/1729881419862164','10.3390/fractalfract7010077','10.1002/rnc.5121']
oc=json.load(open('./work/analisis/snowball/candidatos.json'))
allr={};cnt={}
for doi in seeds:
    u=f'https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}/references?fields=externalIds,title,year,publicationTypes,venue&limit=1000'
    js=None
    for t in range(6):
        try: js=json.load(urllib.request.urlopen(u,timeout=90)); break
        except Exception as e: err=e; time.sleep(5*(t+1))
    if js is None: print('FAIL',doi,err); continue
    d=js.get('data') or []
    for x in d:
        p=x.get('citedPaper') or {}
        k=((p.get('externalIds') or {}).get('DOI') or '').lower() or 'S2:'+str(p.get('paperId'))
        allr.setdefault(k,dict(title=p.get('title') or '',year=p.get('year'),types=p.get('publicationTypes'),venue=p.get('venue'),seeds=[]))['seeds'].append(doi)
    nOC=sum(1 for v in oc.values() if 'ref:'+doi in v)
    cnt[doi]=dict(s2=len(d),opencitations=nOC); print(doi,'S2',len(d),'| OpenCitations',nOC,flush=True); time.sleep(3)
json.dump(dict(conteos=cnt,referencias=allr),open('./work/analisis/snowball/s2_referencias_revisiones.json','w')); print('únicos',len(allr))
