# Bola de nieve por citas (OpenCitations COCI v2 + metadatos Crossref). Hacia atrás: referencias de revisiones semilla. Hacia adelante: citas de clásicos de robótica SMC.
import json,urllib.request,urllib.parse,time,re,csv,sys,os
sys.path.insert(0,'./scripts'); from parse import norm,doi_n
B='./work/'; S=B+'analisis/snowball/'
back=['10.1109/ojies.2020.3040412','10.1109/tii.2011.2123907','10.1007/s40435-020-00638-7','10.1016/j.neucom.2023.126896','10.1016/j.jai.2025.06.001','10.3390/act14030108','10.1016/j.arcontrol.2022.07.001','10.3390/robotics14080101','10.1016/j.arcontrol.2022.07.003','10.1109/jestie.2021.3087938','10.1007/s00521-017-3144-z','10.3390/act12080332','10.3934/mbe.2022120','10.1017/s0263574720000223','10.1016/j.arcontrol.2018.10.009','10.1016/j.arcontrol.2019.08.004','10.1177/1729881419862164','10.3390/fractalfract7010077','10.1002/rnc.5121']
fwd=['10.1177/027836498500400205','10.1109/tsmc.1978.4309907','10.1109/9.362847','10.1016/s0005-1098(02)00147-4','10.23919/acc.1983.4788090','10.1080/00207178408933284']
def get(u,tries=4):
    for t in range(tries):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'PaperR2-review/1.0'}),timeout=120))
        except Exception as e: err=e; time.sleep(3*(t+1))
    print('FAIL',u[:90],err); return None
cand={}  # doi -> set(origen)
for d in back:
    js=get('https://api.opencitations.net/index/v2/references/doi:'+d) or []
    for x in js:
        for tok in x['cited'].split():
            if tok.startswith('doi:'): cand.setdefault(tok[4:].lower(),set()).add('ref:'+d)
    print('back',d,len(js),flush=True)
for d in fwd:
    js=get('https://api.opencitations.net/index/v2/citations/doi:'+d) or []
    for x in js:
        for tok in x['citing'].split():
            if tok.startswith('doi:'): cand.setdefault(tok[4:].lower(),set()).add('cit:'+d)
    print('fwd',d,len(js),flush=True)
json.dump({k:sorted(v) for k,v in cand.items()},open(S+'candidatos.json','w'))
print('candidatos DOI',len(cand),flush=True)
# metadatos Crossref en lotes
meta={}
if os.path.exists(S+'meta.json'): meta=json.load(open(S+'meta.json'))
todo=[d for d in cand if d not in meta]; 
for i in range(0,len(todo),40):
    lot=todo[i:i+40]
    u='https://api.crossref.org/works?'+urllib.parse.urlencode({'filter':','.join('doi:'+d for d in lot),'rows':40,'select':'DOI,title,issued,type,container-title,is-referenced-by-count,author'})
    js=get(u)
    if js:
        for it in js['message']['items']:
            meta[it['DOI'].lower()]=dict(title=(it.get('title') or [''])[0],year=(it.get('issued',{}).get('date-parts') or [[None]])[0][0],type=it.get('type'),journal=(it.get('container-title') or [''])[0],cites=it.get('is-referenced-by-count',0),au=(it.get('author') or [{}])[0].get('family',''))
    if i%800==0: json.dump(meta,open(S+'meta.json','w')); print('meta',i,len(meta),flush=True)
json.dump(meta,open(S+'meta.json','w')); print('meta total',len(meta))
