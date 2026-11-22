# Estimación de recall de la búsqueda en bases de datos usando la bola de nieve como muestra independiente.
import json,csv,re,sys,collections
sys.path.insert(0,'./scripts'); from parse import norm,doi_n
S='analisis/snowball/'
cand=json.load(open(S+'candidatos.json')); meta=json.load(open(S+'meta.json'))
f=json.load(open(S+'s2_citantes_clasicos.json'))['citantes'];b=json.load(open(S+'s2_referencias_revisiones.json'))['referencias'];x=json.load(open(S+'backward_extra.json'))
keys=set(cand)|set(f)|set(b)|set(x)
db=set();dbt=set()
for fn in ('CRIBADO_WOS_RS2.csv','CRIBADO_SCOPUS_RS2.csv','CRIBADO_GENERICAS_RS2.csv'):
    for r in csv.DictReader(open(fn,encoding='utf-8')):
        if r['doi']: db.add(doi_n(r['doi']))
        db.add(norm(r['titulo']))
smc=re.compile(r'sliding[\s-]*mode|super[\s-]*twisting|terminal sliding',re.I)
core=re.compile(r'robot|manipulator|quadrotor|quadcopter|multi[\s-]*rotor|\bUAVs?\b|unmanned aerial|\bAUVs?\b|\bROVs?\b|\bUUVs?\b|underwater|exoskeleton|rehabilitation|wearable|drone|legged|wheeled|nonholonomic|aerial vehicle|vessel|surface vehicle|gripper|continuum|flexible[\s-]*joint',re.I)
res=collections.Counter(); faltan=[]
for d in keys:
    m=meta.get(d) or {}
    if not m:
        v=f.get(d) or b.get(d)
        if not v: continue
        m=dict(title=v['title'],year=v['year'],type='journal-article' if 'JournalArticle' in (v.get('types') or []) else 'x')
    t=m.get('title') or ''; y=m.get('year') or 0
    if not (smc.search(t) and core.search(t) and y and 2016<=y<=2026 and m.get('type')=='journal-article'): continue
    j=(m.get('journal') or '')
    if re.search(r'PapersOnLine|Conference Series|Procedia|E3S Web|MATEC Web|Proceedings|Conference',j,re.I) or re.match(r'(erratum|correction)',t,re.I): res['excl_serie_congreso_o_errata']+=1; continue
    hit=(d in db) or (norm(t) in db)
    res['en_bd' if hit else 'fuera_bd']+=1
    if not hit: faltan.append((y,t))
n=res['en_bd']+res['fuera_bd']; p=res['en_bd']/n
import math; se=math.sqrt(p*(1-p)/n)
out=dict(excluidos_I3=res['excl_serie_congreso_o_errata'],muestra_relevante=n,ya_en_busqueda=res['en_bd'],solo_bola_nieve=res['fuera_bd'],recall_estimado=round(p,4),ic95=[round(p-1.96*se,4),round(p+1.96*se,4)],criterio='título con SMC/STA/TSM y plataforma robótica explícita; artículo de revista 2016–2026')
json.dump(out,open('analisis/recall_estimado.json','w'),ensure_ascii=False,indent=1); print(out)
for y,t in sorted(faltan)[-12:]: print(' fuera:',y,t[:95])
