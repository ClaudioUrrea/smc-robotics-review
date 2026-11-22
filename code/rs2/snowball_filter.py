import json,urllib.request,urllib.parse,time,re,csv,sys,glob,collections
sys.path.insert(0,'./scripts'); from parse import norm,doi_n
B='./work/'; S=B+'analisis/snowball/'
cand={k:set(v) for k,v in json.load(open(S+'candidatos.json')).items()}
F='./work/analisis/snowball/feng2002_citantes_parcial.txt'
import shutil; shutil.copy(F,S+'feng2002_citantes_parcial.txt')
for d in open(F).read().split(): cand.setdefault(d.lower(),set()).add('cit:10.1016/s0005-1098(02)00147-4')
s2f=json.load(open(S+'s2_citantes_clasicos.json'))['citantes']; s2b=json.load(open(S+'s2_referencias_revisiones.json'))['referencias']; bx=json.load(open(S+'backward_extra.json'))
s2meta={}
for k,v in s2f.items():
    for sd in v['seeds']: cand.setdefault(k,set()).add('cit:'+sd)
    s2meta[k]=v
for k,v in s2b.items():
    for sd in v['seeds']: cand.setdefault(k,set()).add('ref:'+sd)
    s2meta[k]=v
for k,v in bx.items():
    for sd in v['seeds']: cand.setdefault(k,set()).add('ref:'+sd)
meta=json.load(open(S+'meta.json'))
todo=[]
for i in range(0,len(todo),40):
    lot=todo[i:i+40]
    u='https://api.crossref.org/works?'+urllib.parse.urlencode({'filter':','.join('doi:'+d for d in lot),'rows':40,'select':'DOI,title,issued,type,container-title,is-referenced-by-count,author'})
    for t in range(3):
        try: js=json.load(urllib.request.urlopen(u,timeout=120)); break
        except Exception: js=None; time.sleep(4)
    for it in (js or {'message':{'items':[]}})['message']['items']:
        meta[it['DOI'].lower()]=dict(title=(it.get('title') or [''])[0],year=(it.get('issued',{}).get('date-parts') or [[None]])[0][0],type=it.get('type'),journal=(it.get('container-title') or [''])[0],cites=it.get('is-referenced-by-count',0),au=(it.get('author') or [{}])[0].get('family',''))
json.dump(meta,open(S+'meta.json','w')); json.dump({k:sorted(v) for k,v in cand.items()},open(S+'candidatos.json','w'))
# ya en corpus
seen=set()
for f in ('CRIBADO_WOS_RS2.csv','CRIBADO_SCOPUS_RS2.csv','CRIBADO_GENERICAS_RS2.csv','CANON_FUNDACIONAL.csv'):
    for r in csv.DictReader(open(B+f,encoding='utf-8')):
        if r.get('doi'): seen.add(doi_n(r['doi']))
        seen.add(norm(r['titulo']))
smc=re.compile(r'sliding[\s-]*mode|sliding[\s-]*surface|super[\s-]*twisting|terminal sliding|variable structure|twisting algorithm|sliding[\s-]*manifold|\bSMC\b',re.I)
plat=re.compile(r'robot|manipulator|quadrotor|quadcopter|multi[\s-]*rotor|\bUAVs?\b|unmanned aerial|\bAUVs?\b|\bROVs?\b|\bUUVs?\b|underwater|exoskeleton|rehabilitation|wearable|drone|legged|wheeled|nonholonomic|aerial vehicle|haptic|prosthe|Euler[\s-]*Lagrange|mechanical system|underactuated|vessel|surface vehicle|spacecraft|gripper|continuum|n[\s-]*link|two[\s-]*link|flexible[\s-]*joint',re.I)
revt=re.compile(r'review|survey|tutorial|overview|state[\s-]*of[\s-]*the[\s-]*art',re.I)
rows=[];C=collections.Counter()
for d,orig in cand.items():
    m=meta.get(d)
    if not m and d in s2meta:
        v=s2meta[d]; ty='journal-article' if (v.get('types') or []) and 'JournalArticle' in v['types'] else ('proceedings-article' if 'Conference' in (v.get('types') or []) else 'otro/S2')
        m=dict(title=v['title'],year=v['year'],type=ty,journal=v.get('venue') or '',cites=0,au='')
    if not m: C['sin metadatos']+=1; continue
    t=m['title'] or ''
    if d in seen or norm(t) in seen: C['ya en corpus']+=1; continue
    if not (smc.search(t) and plat.search(t)): C['título sin SMC+plataforma']+=1; continue
    y=m['year'] or 0; ty=m['type']
    core=re.search(r'robot|manipulator|quadrotor|quadcopter|multi[\s-]*rotor|\bUAVs?\b|unmanned aerial|\bAUVs?\b|\bROVs?\b|\bUUVs?\b|underwater|exoskeleton|rehabilitation|wearable|drone|legged|wheeled|nonholonomic|aerial vehicle|haptic|prosthe|vessel|surface vehicle|gripper|continuum|link|flexible[\s-]*joint',t,re.I)
    if y>=2016 and ty=='journal-article': dec,cod=('INCLUIR','I1+I2 por título (bola de nieve); verificar resumen en RS3') if core else ('INCLUIR','DUDA I2: espacial/mecánico genérico sin robot (bola de nieve); decidir en RS3')
    elif y>=2016 and ty in ('otro/S2',None): dec,cod='INCLUIR','DUDA I3: tipo de documento no determinado (solo metadatos S2); verificar en RS3'
    elif y>=2016 and revt.search(t): dec,cod='CONTEXTO','revisión/tutorial no artículo de revista (bola de nieve)'
    elif y>=2016: dec,cod='EXCLUIR','I3 ('+str(ty)+')'
    elif m['cites']>=150 and ty=='journal-article': dec,cod='CANDIDATO CANÓNICO',('pre-2016 muy citado, recomendado para E-F' if core else 'pre-2016 muy citado sin robot (espacial/teoría): decisión experta')
    else: dec,cod='EXCLUIR','I4 año<2016'
    C[dec]+=1
    o='|'.join(sorted({('atrás' if x.startswith('ref:') else 'adelante') for x in orig}))
    rows.append(dict(origen='SB-'+o,semillas='|'.join(sorted(orig))[:200],anio=y,titulo=t,revista=m['journal'],doi=d,tipo=ty,citas_crossref=m['cites'],decision=dec,codigo=cod))
rows.sort(key=lambda r:({'INCLUIR':0,'CANDIDATO CANÓNICO':1,'CONTEXTO':2}.get(r['decision'],3),-r['citas_crossref']))
w=csv.DictWriter(open(B+'CRIBADO_SNOWBALL_RS2.csv','w',newline='',encoding='utf-8'),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('candidatos',len(cand),'con meta',sum(1 for d in cand if d in meta)); print(C)
for r in rows:
    if r['decision']=='CANDIDATO CANÓNICO': print('CAN',r['anio'],r['citas_crossref'],r['doi'],'|',r['titulo'][:90])
for r in rows[:25]: print(r['decision'][:3],r['anio'],r['citas_crossref'],r['origen'],'|',r['titulo'][:85])
