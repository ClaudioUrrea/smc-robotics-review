# RS3 paso 0: caché de resúmenes/palabras clave del autor por registro del corpus unificado
import csv,json,glob,sys
sys.path.insert(0,'./scripts'); from parse import norm,doi_n,recs,field
from rs3_clean import clean
B='./work/'
AB={}; KW={}
def addab(doi,t,a,k,wos=False):
    # resumen: el más largo tras limpiar; palabras clave: las de autor de WoS si existen (Scopus mezcla términos del tesauro IEEE)
    a=clean(a or '',True); k=clean(k or '')
    for key in (doi_n(doi) if doi else None, norm(t)):
        if not key: continue
        if key not in AB or len(a)>len(AB[key][0]): AB[key]=(a,AB.get(key,('',''))[1])
        if k and (wos or key not in KW): KW.setdefault(key,k) if not wos else KW.__setitem__(key,k) if key not in KW or not KW.get(key+'#w') else None
        if k and wos: KW[key+'#w']=1
for f in glob.glob(B+'respaldos_wos/*.bib'):
    for r in recs(f): addab(field(r,'DOI'),field(r,'Title'),field(r,'Abstract'),field(r,'Keywords'),True)
for f in glob.glob(B+'respaldos_scopus/*.bib'):
    for r in recs(f): addab(field(r,'doi'),field(r,'title'),field(r,'abstract'),field(r,'author_keywords'))
rows=list(csv.DictReader(open(B+'CORPUS_RS2_UNIFICADO.csv',encoding='utf-8-sig')))
out={};miss=0
for r in rows:
    if r['decision']=='EXCLUIR': continue
    a=AB.get(doi_n(r['doi']) if r['doi'] else '',None) or AB.get(norm(r['titulo']),('',''))
    kk=[x for x in (doi_n(r['doi']) if r['doi'] else '',norm(r['titulo'])) if x]
    out[r['id']]=dict(a=a[0],k=next((KW[x] for x in kk if x in KW),''),ks='wos' if any(KW.get(x+'#w') for x in kk) else 'scopus')
    if not a[0]: miss+=1
LANG={}
for r in recs(B+'respaldos_scopus/SENS_no_ingles_767.bib'):
    for kk in (doi_n(field(r,'doi')) if field(r,'doi') else None, norm(field(r,'title'))):
        if kk: LANG[kk]=field(r,'language')
for r in rows:
    if r['id'] in out:
        lg=LANG.get(doi_n(r['doi']) if r['doi'] else '') or LANG.get(norm(r['titulo']))
        if lg: out[r['id']]['lang']=lg
json.dump(out,open(B+'RS3/abstracts_cache.json','w'),ensure_ascii=False)
print(len(out),'registros; sin resumen:',miss)
