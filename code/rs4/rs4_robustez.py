# RS4: robustez estadística de los hallazgos principales
import csv,json,collections,math,re
import numpy as np, pandas as pd, statsmodels.formula.api as smf
from statsmodels.stats.proportion import proportion_confint
R='./work/'
ab=json.load(open(R+'RS3/abstracts_cache.json'))
M=[r for r in csv.DictReader(open(R+'RS3/CORPUS_MAPEO_RS3.csv',encoding='utf-8-sig')) if r['dec_rs3']=='INCLUIR' and r['anio']>='2016']
V=['Tiempo finito/fijo/predefinido','Terminal (TSM/NTSM/FTSM)','STA/HOSM','Integral (ISM)','Adaptativo','Basado en observador','Inteligente (neuronal/difuso/aprendizaje)','Convencional/primer orden','Fraccionario','Multiagente/formación','Tolerante a fallas','Disparo por eventos/discreto']
rows=[]
for r in M:
    d=dict(y=min(int(r['anio']),2026),plat=r['plat_rs3'],exp=int('experimento' in r['validacion'] or 'HIL' in r['validacion']),nivel=r['plataforma_nivel'],smc_tit=int(bool(re.search(r'sliding|super[\s-]*twisting|\bSMC\b|variable structure',r['titulo'],re.I))))
    for i,v in enumerate(V): d['v%d'%i]=int(v in r['variante_auto'].split('; '))
    rows.append(d)
D=pd.DataFrame(rows); D['yc']=D['y']-2021
out={}
def wilson(k,n): lo,hi=proportion_confint(k,n,method='wilson'); return [round(100*k/n,1),round(100*lo,1),round(100*hi,1)]
# 1. tendencia de cuota: logit(variante) ~ año; OR por año
tr={}
for i,v in enumerate(V):
    m=smf.logit(f'v{i} ~ yc',D).fit(disp=0); tr[v]=dict(OR_anual=round(math.exp(m.params['yc']),3),IC95=[round(math.exp(x),3) for x in m.conf_int().loc['yc']],p=float(f"{m.pvalues['yc']:.2g}"))
    a=D[D.y<=2018]; b=D[D.y>=2024]; tr[v]['2016-18']=wilson(a[f'v{i}'].sum(),len(a)); tr[v]['2024-26']=wilson(b[f'v{i}'].sum(),len(b))
out['tendencia']=tr
# 2. validación experimental ~ garantía temporal, ajustado por plataforma y año (y por variantes núcleo)
m=smf.logit('exp ~ v0 + C(plat) + yc',D).fit(disp=0)
out['exp_FT_ajustado']=dict(OR=round(math.exp(m.params['v0']),3),IC95=[round(math.exp(x),3) for x in m.conf_int().loc['v0']],p=float(f"{m.pvalues['v0']:.2g}"))
m2=smf.logit('exp ~ v0 + v1 + v2 + v3 + v4 + v5 + v6 + v8 + v9 + v10 + v11 + C(plat) + yc',D).fit(disp=0)
out['exp_multivariable']={V[int(k[1:])]:dict(OR=round(math.exp(m2.params[k]),2),IC95=[round(math.exp(x),2) for x in m2.conf_int().loc[k]],p=float(f"{m2.pvalues[k]:.2g}")) for k in m2.params.index if re.fullmatch(r'v\d+',k)}
out['exp_por_variante_wilson']={v:wilson(D[D[f'v{i}']==1].exp.sum(),(D[f'v{i}']==1).sum()) for i,v in enumerate(V)}
# 3. robustez: núcleo estricto (plataforma principal y SMC en el título)
S=D[(D.nivel=='principal')&(D.smc_tit==1)]
out['n_nucleo_estricto']=len(S)
out['nucleo_estricto']={v:dict(cuota_16_18=round(100*S[S.y<=2018][f'v{i}'].mean(),1),cuota_24_26=round(100*S[S.y>=2024][f'v{i}'].mean(),1),exp=round(100*S[S[f'v{i}']==1].exp.mean(),1)) for i,v in enumerate(V)}
ms=smf.logit('exp ~ v0 + C(plat) + yc',S).fit(disp=0); out['exp_FT_ajustado_nucleo']=dict(OR=round(math.exp(ms.params['v0']),3),IC95=[round(math.exp(x),3) for x in ms.conf_int().loc['v0']])
# 4. sensibilidad a la corrección del indicador experimental (VPP 0,87; sin falsos negativos): la razón entre grupos no cambia si el error es no diferencial
out['nota_correccion']='Si el VPP del indicador es igual en todos los grupos, la corrección multiplica cada tasa por ≈0,87 y conserva las razones; el OR ajustado no cambia en primer orden.'
# 5. discretización en el resumen: IC
k=sum(1 for r in M if re.search(r'discrete[\s-]*time|sampled[\s-]*data|digital implementation|implicit discreti|discretization',r['titulo']+' '+ab[r['id']]['a'],re.I))
out['discretizacion']=wilson(k,len(M))
json.dump(out,open(R+'RS4/robustez_rs4.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(out,ensure_ascii=False,indent=0)[:6000])
