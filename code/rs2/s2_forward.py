import json,urllib.request,time
allc={};cnt={}
for doi in ['10.1016/s0005-1098(02)00147-4','10.1109/9.362847','10.1080/00207178408933284','10.1109/tsmc.1978.4309907','10.1177/027836498500400205','10.23919/acc.1983.4788090']:
    n=0;off=0
    while True:
        u=f'https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}/citations?fields=externalIds,title,year,publicationTypes,venue&limit=1000&offset={off}'
        js=None
        for t in range(6):
            try: js=json.load(urllib.request.urlopen(u,timeout=90)); break
            except Exception as e: err=e; time.sleep(5*(t+1))
        if js is None: print('FAIL',doi,off,err); break
        d=js.get('data',[]); n+=len(d)
        for x in d:
            p=x.get('citingPaper') or {}
            k=((p.get('externalIds') or {}).get('DOI') or '').lower() or 'S2:'+str(p.get('paperId'))
            allc.setdefault(k,dict(title=p.get('title') or '',year=p.get('year'),types=p.get('publicationTypes'),venue=p.get('venue'),seeds=[]))['seeds'].append(doi)
        if 'next' not in js or not d: break
        off=js['next']; time.sleep(3)
    cnt[doi]=n; print(doi,'citantes S2',n,flush=True); time.sleep(3)
json.dump(dict(conteos=cnt,citantes=allc),open('./work/analisis/snowball/s2_citantes_clasicos.json','w')); print('total únicos',len(allc))
