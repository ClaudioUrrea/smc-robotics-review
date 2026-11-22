# RS4: análisis cuantitativo del corpus de mapeo 2016–2026 (RS3 v2.3)
import csv,json,collections,math,itertools,re
R3='./work/RS3/'; R4='./work/RS4/'
M=[r for r in csv.DictReader(open(R3+'CORPUS_MAPEO_RS3.csv',encoding='utf-8-sig')) if r['dec_rs3']=='INCLUIR' and r['anio']>='2016']
for r in M:
    r['y']=min(int(r['anio']),2026); r['V']=r['variante_auto'].split('; '); r['exp']=('experimento' in r['validacion'] or 'HIL' in r['validacion'])
C=collections.Counter; n=len(M); out={'n':n}
VAR=sorted({v for r in M for v in r['V']}); PLT=[p for p,_ in C(r['plat_rs3'] for r in M).most_common()]
Y=list(range(2016,2027)); ny=C(r['y'] for r in M)
# 1. serie anual por variante (conteo y % del año)
with open(R4+'serie_anual_variante.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['variante']+Y+['crec_2016_18_vs_2024_26_pp'])
    for v in VAR:
        c=[sum(1 for r in M if r['y']==y and v in r['V']) for y in Y]
        p0=100*sum(c[:3])/sum(ny[y] for y in Y[:3]); p1=100*sum(c[-3:])/sum(ny[y] for y in Y[-3:])
        w.writerow([v]+c+[round(p1-p0,1)]); out.setdefault('cuota',{})[v]=(round(p0,1),round(p1,1))
out['por_anio']={y:ny[y] for y in Y}
# 2. matriz variante×plataforma con % experimental
with open(R4+'matriz_variante_plataforma_exp.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['variante']+[p+' (n)' for p in PLT]+[p+' (%exp)' for p in PLT])
    for v in VAR:
        ns=[sum(1 for r in M if v in r['V'] and r['plat_rs3']==p) for p in PLT]
        es=[round(100*sum(1 for r in M if v in r['V'] and r['plat_rs3']==p and r['exp'])/k) if k else '' for k,p in zip(ns,PLT)]
        w.writerow([v]+ns+es)
# 3. % experimental por plataforma y por variante; tendencia temporal
out['exp_plat']={p:(sum(1 for r in M if r['plat_rs3']==p),round(100*sum(r['exp'] for r in M if r['plat_rs3']==p)/sum(1 for r in M if r['plat_rs3']==p),1)) for p in PLT}
out['exp_var']={v:round(100*sum(r['exp'] for r in M if v in r['V'])/sum(1 for r in M if v in r['V']),1) for v in VAR}
out['exp_anio']={y:round(100*sum(r['exp'] for r in M if r['y']==y)/ny[y],1) for y in Y}
# 4. co-ocurrencias (lift)
pc=C(); vc=C(r_ for r in M for r_ in r['V'])
for r in M:
    for a,b in itertools.combinations(sorted(set(r['V'])),2): pc[(a,b)]+=1
lift=sorted([(a,b,k,round(k*n/(vc[a]*vc[b]),2)) for (a,b),k in pc.items() if k>=30],key=lambda x:-x[2])
out['coocurrencia_top']=lift[:12]; out['coocurrencia_bajo']=sorted(lift,key=lambda x:x[3])[:8]
out['n_variantes_por_trabajo']=dict(sorted(C(len([v for v in r['V'] if v!='Convencional/primer orden']) for r in M).items()))
# 5. garantía declarada por variante
G=['tiempo finito','tiempo fijo','prescrita/predefinida','asintótica/exponencial','no especificada']
out['garantia_por_variante']={v:{g:round(100*sum(1 for r in M if v in r['V'] and r['convergencia']==g)/vc[v],1) for g in G} for v in VAR}
out['garantia_anio']={y:{g:sum(1 for r in M if r['y']==y and r['convergencia']==g) for g in G} for y in Y}
# 6. chattering, implementación discreta, observador por plataforma
out['chattering']=C(t for r in M for t in r['chattering'].split('; ')).most_common()
out['discreta_pct']=round(100*sum(r['impl_discreta']=='sí' for r in M)/n,1)
out['discreta_exp_pct']=round(100*sum(r['impl_discreta']=='sí' for r in M if r['exp'])/max(1,sum(r['exp'] for r in M)),1)
out['codigo_mencion']=sum(1 for r in M if r['codigo_disponible'].startswith('sí'))
out['objetivo']=C(r['objetivo'] for r in M).most_common()
out['objetivo_plat']={p:C(r['objetivo'] for r in M if r['plat_rs3']==p).most_common(3) for p in PLT}
# 7. huecos: celdas con n<15 o %exp<25
gaps=[]
for v in VAR:
    for p in PLT:
        k=sum(1 for r in M if v in r['V'] and r['plat_rs3']==p); e=sum(1 for r in M if v in r['V'] and r['plat_rs3']==p and r['exp'])
        gaps.append((v,p,k,round(100*e/k) if k else None))
out['celdas_vacias_o_raras']=[g for g in gaps if g[2]<10 and g[1] not in('Robot genérico (EL/subactuado)',)]
out['celdas_grandes_poco_experimentales']=sorted([g for g in gaps if g[2]>=60 and g[3] is not None and g[3]<30],key=lambda g:g[3])
# 8. revistas principales
out['revistas']=C(r['revista'] for r in M).most_common(12)
json.dump(out,open(R4+'analisis_rs4.json','w'),ensure_ascii=False,indent=1,default=str)
print(json.dumps({k:out[k] for k in ['n','por_anio','cuota','exp_plat','exp_var','exp_anio','coocurrencia_top','coocurrencia_bajo','n_variantes_por_trabajo','discreta_pct','discreta_exp_pct','codigo_mencion','chattering','objetivo','celdas_grandes_poco_experimentales','revistas']},ensure_ascii=False,default=str))
print('GARANTIA',json.dumps(out['garantia_por_variante'],ensure_ascii=False))
print('VACIAS',out['celdas_vacias_o_raras'])
