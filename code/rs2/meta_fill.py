import json,urllib.request,urllib.parse,time
S='./work/analisis/snowball/'
c=json.load(open(S+'candidatos.json'));m=json.load(open(S+'meta.json'))
f=json.load(open(S+'s2_citantes_clasicos.json'))['citantes'];b=json.load(open(S+'s2_referencias_revisiones.json'))['referencias'];x=json.load(open(S+'backward_extra.json'))
todo=[d for d in set(c)|set(f)|set(b)|set(x) if d not in m and not d.lower().startswith('s2:')]
print('faltan',len(todo),flush=True); fails=0
for i in range(0,len(todo),25):
    lot=todo[i:i+25]
    u='https://api.crossref.org/works?'+urllib.parse.urlencode({'filter':','.join('doi:'+d for d in lot),'rows':25,'select':'DOI,title,issued,type,container-title,is-referenced-by-count,author'})
    js=None
    for t in range(8):
        try: js=json.load(urllib.request.urlopen(u,timeout=90)); break
        except Exception: time.sleep(3*(t+1))
    if not js: fails+=1; continue
    for it in js['message']['items']:
        m[it['DOI'].lower()]=dict(title=(it.get('title') or [''])[0],year=(it.get('issued',{}).get('date-parts') or [[None]])[0][0],type=it.get('type'),journal=(it.get('container-title') or [''])[0],cites=it.get('is-referenced-by-count',0),au=(it.get('author') or [{}])[0].get('family',''))
    if i%500==0: json.dump(m,open(S+'meta.json','w')); print(i,len(m),'fallos',fails,flush=True)
    time.sleep(0.5)
json.dump(m,open(S+'meta.json','w')); print('fin',len(m),'fallos lote',fails,'aún faltan',sum(1 for d in todo if d not in m))
