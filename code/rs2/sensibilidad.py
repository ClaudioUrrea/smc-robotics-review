# Sensibilidad: ¿cambia la distribución variante×plataforma si se incluyeran ponencias/capítulos o artículos no ingleses?
import csv,re,sys,collections,json,math
sys.path.insert(0,'./scripts'); from parse import recs,field,norm
src=open('./scripts/unify.py').read()
exec(src[src.index('V=[('):src.index('EXP=re.compile')])   # mismas reglas V y P que el corpus
smc=re.compile(r'sliding[\s-]*mode|super[\s-]*twisting|terminal sliding|variable structure|\bSMC\b',re.I)
nonrob=re.compile(r'suspension|brak|anti[\s-]*lock|electric vehicle|\bEVs?\b|hybrid electric|steering|in[\s-]*wheel|traction|powertrain|engine|microgrid|PMSM|permanent magnet|converter|inverter|power grid|battery|wind turbine|photovoltaic|vehicle dynamics',re.I)
def code(t,a,k):
    tk=t+' '+k
    var=[n for n,p in V if re.search(p,tk,re.I)] or [n for n,p in V if len(re.findall(p,a,re.I))>=2] or ['Convencional/primer orden']
    pl=[n for n,p in P if re.search(p,tk,re.I)] or [n for n,p in P if re.search(p,a,re.I)]
    return var,(pl[0] if pl else None)
def load(f):
    out=[];L=collections.Counter()
    for r in recs(f):
        t=field(r,'title');a=field(r,'abstract');k=field(r,'author_keywords')
        L[field(r,'language')]+=1
        if not (smc.search(t) or smc.search(field(r,'author_keywords')) or len(smc.findall(a))>=2): continue
        if nonrob.search(t): continue
        v,p=code(t,a,k)
        if p is None: continue
        out.append((v,p,field(r,'type')))
    return out,L
corp=[x for x in csv.DictReader(open('./work/CORPUS_RS2_UNIFICADO.csv',encoding='utf-8-sig')) if x['decision']=='INCLUIR' and x['anio'].isdigit() and int(x['anio'])>=2016 and x['plataforma_auto']!='Otro/genérico (EL, subactuado)']
C=[(x['variante_auto'].split('; '),x['plataforma_auto']) for x in corp]
res={}
for tag,f in (('ponencias_capitulos','respaldos_scopus/SENS_ponencias_capitulos_5075.bib'),('no_ingles','respaldos_scopus/SENS_no_ingles_767.bib')):
    X,L=load('./work/'+f)
    def dist(D,i):
        c=collections.Counter()
        for d in D:
            if i==1: c[d[1]]+=1
            else: c.update(d[0])
        return c
    out={}
    for i,nm in ((1,'plataforma'),(0,'variante')):
        a=dist(C,i);b=dist(X,i);ks=sorted(set(a)|set(b))
        na=sum(a.values());nb=sum(b.values())
        # chi2 y V de Cramér (tabla 2×k)
        chi=0
        for k in ks:
            tot=a[k]+b[k]
            for obs,n in ((a[k],na),(b[k],nb)):
                e=tot*n/(na+nb); chi+=(obs-e)**2/e if e else 0
        Vc=math.sqrt(chi/((na+nb)*(min(2,len(ks))-1)))
        out[nm]=dict(cramer_V=round(Vc,3),dif_max_pp=round(max(abs(100*a[k]/na-100*b[k]/nb) for k in ks),1),
                    tabla={k:[round(100*a[k]/na,1),round(100*b[k]/nb,1)] for k in ks})
    res[tag]=dict(registros=sum(L.values()),elegibles_aprox=len(X),idiomas=dict(L.most_common(6)),**out)
json.dump(res,open('./work/analisis/sensibilidad_idioma_tipo.json','w'),ensure_ascii=False,indent=1)
for t,r in res.items():
    print('==',t,'registros',r['registros'],'elegibles',r['elegibles_aprox'],r['idiomas'])
    for nm in ('plataforma','variante'): print('  ',nm,'V=',r[nm]['cramer_V'],'difmax pp=',r[nm]['dif_max_pp']); [print('     ',k,v) for k,v in r[nm]['tabla'].items()]
