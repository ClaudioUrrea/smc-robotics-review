import csv,json,re,collections,math,random,glob,os
B='./work/'; R=B+'RS3/'
o=json.load(open(R+'_out_tmp.json')); AB=json.load(open(R+'abstracts_cache.json'))
C=collections.Counter
for r in o: r['cit']=int(r['citas_max'] or 0)
FIELDS=['garantia_con_inferencia','objetivo','chattering','incertidumbre','observador','convergencia','validacion','gdl','impl_discreta','codigo_disponible']
# extracción (misma función que rs3_extract; se reimporta para no duplicar)
import importlib.util,sys,io,contextlib
spec=importlib.util.spec_from_file_location('rs3e','./scripts/rs3_extract.py'); m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
out=m.out
for r in out:
    r['cit']=int(r['citas_max'] or 0); r.setdefault('plataforma_nivel','')
    if r['plat_rs3']=='Otro/genérico (EL, subactuado)': r['plat_rs3']='Robot genérico (EL/subactuado)'
inc=[r for r in out if r['dec_rs3']=='INCLUIR' and r['anio']>='2016']
for r in out:
    if r['dec_rs3'] in('INCLUIR','INCLUIR (E-F)','CONTEXTO'): r.update(m.ext(r))
# ---- corpus de mapeo final
cols=['id','estrato','anio','titulo','revista','doi','tipo','cit','dec_rs3','regla_rs3','variante_auto','plat_rs3','plataforma_nivel','plat_en_titulo']+FIELDS
def wcsv(name,rows,cols):
    w=csv.DictWriter(open(R+name,'w',newline='',encoding='utf-8-sig'),fieldnames=cols,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
for r in out: r['plat_en_titulo']='sí' if m.ROBOT2.search(r['titulo']) else 'no'
mp=[r for r in out if r['dec_rs3'] in('INCLUIR','INCLUIR (E-F)')]
wcsv('CORPUS_MAPEO_RS3.csv',mp,cols)
# ---- matriz variante x plataforma (corpus de mapeo 2016+)
VAR=[l for l in sorted({v for r in inc for v in r['variante_auto'].split('; ')})]
PLT=sorted({r['plat_rs3'] for r in inc})
mat=collections.defaultdict(int)
for r in inc:
    for v in r['variante_auto'].split('; '): mat[(v,r['plat_rs3'])]+=1
with open(R+'MATRIZ_variante_plataforma_RS3.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['variante']+PLT+['total'])
    for v in VAR: w.writerow([v]+[mat[(v,p)] for p in PLT]+[sum(mat[(v,p)] for p in PLT)])
# ---- corpus de síntesis
def cpy(r): return r['cit']/max(1,2027-int(r['anio']))
def expr(r): return ('experimento' in r['validacion']) or ('HIL' in r['validacion'])
cells=collections.defaultdict(list)
for r in inc:
    if r['regla_rs3'].startswith('sin resumen') or r.get('plataforma_nivel')!='principal': continue
    if not m.SMC.search(r['titulo']) or re.search(r'review|survey|overview|tutorial|state[\s-]*of[\s-]*the[\s-]*art',r['titulo'],re.I): continue   # RS4: representante de celda con SMC en el título y no revisión
    if r['tipo'] and 'review' in r['tipo'].lower(): continue
    for v in r['variante_auto'].split('; '): cells[(v,r['plat_rs3'])].append(r)
def pick(coef):
    chosen={}
    for (v,p),lst in sorted(cells.items(),key=lambda kv:len(kv[1])):
        k=min(len(lst),max(1,round(coef*math.sqrt(len(lst)))))
        have=sum(1 for r in lst if r['id'] in chosen)
        srt=sorted(lst,key=lambda r:-(cpy(r)*(1.5 if expr(r) else 1.0)*(1.3 if int(r['anio'])>=2024 else 1.0)))
        for r in srt:
            if have>=k: break
            if r['id'] not in chosen: chosen[r['id']]=(v,p); have+=1
    return chosen
coef=0.2
while True:
    ch=pick(coef)
    if len(ch)>=190 or coef>3: break
    coef+=0.02
print('coef',round(coef,2),'sintesis mapeo',len(ch),'celdas',len(cells))
syn=[]
byid={r['id']:r for r in out}
for i,(v,p) in ch.items():
    r=dict(byid[i]); r['rol_sintesis']='celda: %s × %s'%(v,p); syn.append(r)
# revisiones (INCLUIR tipo review, CONTEXTO, cercanas)
RT=re.compile(r'review|survey|tutorial|overview|state[\s-]*of[\s-]*the[\s-]*art',re.I)
BAD=re.compile(r'PMSM|PMLSM|motor|converter|filter|weld|power|grid|battery',re.I)
revs=[r for r in out if r['dec_rs3'] in('INCLUIR','CONTEXTO') and r['anio']>='2016' and RT.search(r['titulo']) and not BAD.search(r['titulo']) and 'dominio no robótico' not in r['codigo'] and r['id'] not in ch]
smc_rev=sorted([r for r in revs if m.SMC.search(r['titulo'])],key=lambda r:-(cpy(r)+(5 if r['rev_cercana']=='sí' else 0)))
plat_rev=sorted([r for r in revs if not m.SMC.search(r['titulo']) and m.ROBOT2.search(r['titulo'])],key=lambda r:-(cpy(r)+(5 if r['rev_cercana']=='sí' else 0)))
revs=smc_rev[:16]+plat_rev[:14]
for r in revs: r=dict(r); r['rol_sintesis']='revisión/tutorial '+('de SMC' if m.SMC.search(r['titulo']) else 'de control de plataforma')+' (posicionamiento, brecha)'; syn.append(r)
rec=[r for r in inc if r['anio'] in('2025','2026','2027') and r.get('plataforma_nivel')=='principal' and r['id'] not in ch and not r['regla_rs3'].startswith('sin resumen') and not(r['tipo'] and 'review' in r['tipo'].lower()) and m.SMC.search(r['titulo']) and not re.search(r'review|survey|overview',r['titulo'],re.I)]
recsel=[]
for yrs,cap in ((('2026','2027'),13),(('2025',),12)):
    pc=C();k=0
    for r in sorted([x for x in rec if x['anio'] in yrs],key=lambda r:-(r['cit']*(1.5 if expr(r) else 1.0))):
        if pc[r['plat_rs3']]>=2: continue
        recsel.append(r); pc[r['plat_rs3']]+=1; k+=1
        if k>=cap: break
for r in recsel: r=dict(r); r['rol_sintesis']='reciente 2025–2026 (frontera actual)'; syn.append(r)
# canon
canon=[r for r in out if r['estrato'].startswith('E-F')]
for r in canon: r=dict(r); r['rol_sintesis']='canon fundacional (E-F, experto)'; syn.append(r)
cand=sorted([r for r in out if r['dec_rs3']=='INCLUIR (E-F)'],key=lambda r:-r['cit'])
for r in cand[:16]: r=dict(r); r['rol_sintesis']='clásico de SMC robótico pre-2016 (candidato aceptado)'; syn.append(r)
import os
if os.path.exists('./work/RS4/SINTESIS_RS4.md'):   # RS4: todo trabajo citado en la síntesis pertenece al corpus de síntesis
    cit=set(re.findall(r'R2-\d{5}',open('./work/RS4/SINTESIS_RS4.md',encoding='utf-8').read()))
    have={r['id'] for r in syn}
    for i in sorted(cit-have):
        if i in byid: r=dict(byid[i]); r['rol_sintesis']='citado en la síntesis RS4'; syn.append(r)
REVF=[r for r in syn if 'revisión' in r['rol_sintesis']]
for r in REVF:
    for f in FIELDS: r[f]='n/a (revisión)'
for r in syn:
    if r['plat_rs3']=='Otro/genérico (EL, subactuado)': r['plat_rs3']='Robot genérico (EL/subactuado)'
seen=set(); S=[]
for r in syn:
    if r['id'] in seen: continue
    seen.add(r['id']); S.append(r)
S.sort(key=lambda r:(r['rol_sintesis'][:6],-r['cit']))
wcsv('CORPUS_SINTESIS_RS3.csv',S,cols+['rol_sintesis'])
wcsv('TABLA_S1_datos_por_estudio.csv',S,['id','doi','anio','titulo','revista','cit','rol_sintesis','plat_rs3','variante_auto']+FIELDS)
print('SINTESIS total',len(S),C(r['rol_sintesis'][:14] for r in S))
# ---- excluidos con motivo
ex=[]
for r in out:
    if r['decision']=='EXCLUIR': ex.append(dict(id=r['id'],doi=r['doi'],anio=r['anio'],titulo=r['titulo'],revista=r['revista'],etapa='RS2 (título/resumen)',motivo=r['codigo']))
    elif r['dec_rs3']=='EXCLUIR': ex.append(dict(id=r['id'],doi=r['doi'],anio=r['anio'],titulo=r['titulo'],revista=r['revista'],etapa='RS3 (verificación resumen)',motivo=r['regla_rs3']))
wcsv('TABLA_S3_excluidos_con_motivo.csv',ex,['id','doi','anio','titulo','revista','etapa','motivo'])
# decisiones DUDA
dd=[dict(id=i,codigo_previo=v[0],decision_rs3=v[1],regla=v[2],titulo=byid[i]['titulo']) for i,v in m.dud.items()]
wcsv('RS3_DUDAS_resueltas.csv',dd,['id','codigo_previo','decision_rs3','regla','titulo'])
wcsv('CANON_candidatos_decision.csv',[dict(id=r['id'],anio=r['anio'],cit=r['cit'],titulo=r['titulo'],decision=r['dec_rs3'],regla=r['regla_rs3']) for r in out if r['decision']=='CANDIDATO CANÓNICO'],['id','anio','cit','titulo','decision','regla'])
# ---- PRISMA
def n(f,wos=False):
    return sum(1 for l in open(f,encoding='utf-8',errors='ignore') if l.startswith('@'))
wos_raw=sum(n(f) for f in glob.glob(B+'respaldos_wos/W12_*.bib'))
sc=[f for f in glob.glob(B+'respaldos_scopus/*.bib') if not re.search(r'SENS_|^S01_integral',os.path.basename(f)) and 'S01_integral' not in f]
sc_raw=sum(n(f) for f in sc)
cnt=C(r['decision'] for r in out)
rs3_inc=len(inc); rs3_ctx=sum(1 for r in out if r['dec_rs3']=='CONTEXTO'); 
pr=[('IDENTIFICACIÓN','Registros exportados de WoS (cadena genérica W12, 11 lotes; las cadenas específicas X01–X15 y las revisiones Q05–Q09b aportan 662 filas adicionales, ya contenidas en el recuento único)',wos_raw),
('IDENTIFICACIÓN','Registros exportados de Scopus (S01–S15, SR05–SR08; excluye sensibilidad)',sc_raw),
('IDENTIFICACIÓN','Registros de bola de nieve (citas hacia atrás y adelante, tras filtro de título/año/tipo)',919),
('IDENTIFICACIÓN','Canon fundacional (selección experta)',42),
('CRIBADO','Registros únicos tras eliminar duplicados (DOI y título normalizado)',len(out)),
('CRIBADO RS2','Excluidos en título/resumen (X1–X4, I3, I4)',cnt['EXCLUIR']),
('CRIBADO RS2','Conservados para RS3 (INCLUIR + CONTEXTO + CANDIDATO CANÓNICO)',len(out)-cnt['EXCLUIR']),
('ELEGIBILIDAD RS3','Corpus de mapeo 2016+ evaluado con I1/I2 sobre título + resumen + palabras clave',cnt['INCLUIR']-sum(1 for r in out if r['decision']=='INCLUIR' and r['anio']<'2016')),
('ELEGIBILIDAD RS3','Excluidos en RS3 (X1 SMC no principal; X2 sin plataforma robótica; X3 sin resumen)',sum(1 for r in out if r['dec_rs3']=='EXCLUIR' and r['decision']=='INCLUIR')),
('ELEGIBILIDAD RS3','Reclasificados a CONTEXTO en RS3 (revisión de SMC sin plataforma)',sum(1 for r in out if r['dec_rs3']=='CONTEXTO' and r['decision']=='INCLUIR')),
('INCLUIDOS','Corpus de mapeo 2016–2026 (matriz, series temporales, tasa de validación)',rs3_inc),
('INCLUIDOS','Canon histórico: E-F + candidatos aceptados pre-2016',sum(1 for r in out if r['dec_rs3']=='INCLUIR (E-F)')+sum(1 for r in out if r['decision']=='INCLUIR' and r['anio']<'2016')),
('INCLUIDOS','Registros CONTEXTO (no evidencia primaria)',rs3_ctx),
('INCLUIDOS','Corpus de síntesis citado (curado por celda variante × plataforma + revisiones + canon)',len(S))]
with open(R+'TABLA_S2_PRISMA_flujo.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['fase','paso','n']); w.writerows(pr)
for p in pr: print(p[0],'|',p[1][:70],'|',p[2])
exp=C(); 
for r in inc: exp[('exp' if ('experimento' in r['validacion'] or 'HIL' in r['validacion']) else r['validacion'])]+=1
print(exp)
json.dump(dict(total_mapeo=rs3_inc,exp=exp,matriz_tot={v:sum(mat[(v,p)] for p in PLT) for v in VAR}),open(R+'resumen_rs3.json','w'),ensure_ascii=False,indent=1)

# ---- sensibilidad: núcleo estricto (plataforma en el título) vs corpus ampliado
strict=[r for r in inc if r.get('plataforma_nivel')=='principal']
def dist(rs,key):
    c=C(); 
    for r in rs:
        for v in (r[key].split('; ') if key=='variante_auto' else [r[key]]): c[v]+=1
    t=sum(c.values()); return {k:c[k]/t for k in c}
res={}
for key in('plat_rs3','variante_auto'):
    a=dist(inc,key); b=dist(strict,key); ks=set(a)|set(b)
    res[key]=dict(max_dif_pp=round(100*max(abs(a.get(k,0)-b.get(k,0)) for k in ks),1))
    res[key]['orden_igual']=[k for k,_ in sorted(a.items(),key=lambda x:-x[1])[:4]]==[k for k,_ in sorted(b.items(),key=lambda x:-x[1])[:4]]
ex_s=sum(1 for r in strict if 'experimento' in r['validacion'] or 'HIL' in r['validacion'])
res['n_estricto']=len(strict); res['n_ampliado']=len(inc); res['exp_estricto']=round(ex_s/len(strict),3); res['exp_ampliado']=round(sum(1 for r in inc if 'experimento' in r['validacion'] or 'HIL' in r['validacion'])/len(inc),3)
json.dump(res,open(R+'sensibilidad_nucleo_estricto.json','w'),indent=1)
print(res)
print('por año',sorted(C(r['anio'] for r in inc).items())[-4:])
