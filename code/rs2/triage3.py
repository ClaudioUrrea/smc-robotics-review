# Cribado de cadenas genericas SR07 (Scopus) y W01 (WoS): top-N por citas de cada cadena, exista o no en otras exportaciones; excluye lo ya cribado.
import json,re,csv,sys,collections
sys.path.insert(0,'./scripts')
from parse import *
B='./work/'
N=int(sys.argv[1]) if len(sys.argv)>1 else 300
screened=set()
for f in ('CRIBADO_WOS_RS2.csv','CRIBADO_SCOPUS_RS2.csv'):
    for r in csv.DictReader(open(B+f,encoding='utf-8')):
        if set(r['cadenas'].split('|')) <= {'SR07','W01','SR08','W12'}: continue   # se recalculan
        if r['doi'] and r['doi']!='por verificar': screened.add(doi_n(r['doi']))
        screened.add(norm(r['titulo']))
def load(path,wos):
    out=[]
    for r in recs(path):
        c=field(r,'Times-Cited') if wos else (re.search(r'Cited by:\s*(\d+)',field(r,'note')) or [0,'0'])[1]
        out.append(dict(cites=int(re.sub(r'\D','',c) or 0),doi=doi_n(field(r,'DOI' if wos else 'doi')),title=field(r,'Title' if wos else 'title'),year=field(r,'Year' if wos else 'year'),
          journal=field(r,'Journal' if wos else 'journal'),abstract=field(r,'Abstract' if wos else 'abstract'),
          akw=field(r,'Keywords' if wos else 'author_keywords'),kw=field(r,'Keywords-Plus' if wos else 'keywords'),dt=field(r,'Type' if wos else 'type')))
    out.sort(key=lambda e:-e['cites']); return out
import glob
sr=load(B+'respaldos_scopus/SR07_scopus_completo.bib',False)[:N]
f8=B+'respaldos_scopus/SR08_scopus_completo_3305.bib'
s8=load(f8,False)[:N] if glob.glob(f8) else []
w1=[]
for f in (sorted(glob.glob(B+'respaldos_wos/W12_*.bib')) or [B+'respaldos_wos/W01_generica_top1000.bib']): w1+=load(f,True)
w1.sort(key=lambda e:-e['cites']); w1=w1[:N]
pool={}
for tag,lst in (('SR07',sr),('SR08',s8),('W12',w1)):
    for rank,e in enumerate(lst,1):
        k=e['doi'] or norm(e['title'])
        if k in pool or norm(e['title']) in {norm(x['title']) for x in ()}: pool[k]['cad'].add(tag); pool[k]['cites_'+tag]=e['cites']; continue
        e['cad']={tag}; e['cites_'+tag]=e['cites']; pool[k]=e
# fusion por titulo
bt={}
for k,e in list(pool.items()):
    t=norm(e['title'])
    if t in bt: bt[t]['cad']|=e['cad']; bt[t].update({x:e[x] for x in e if x.startswith('cites_')}); bt[t]['doi']=bt[t]['doi'] or e['doi']
    else: bt[t]=e
pool=list(bt.values())
smc=re.compile(r'sliding[\s-]*mode|sliding[\s-]*surface|super[\s-]*twisting|terminal sliding|variable structure|\bSMC\b|twisting algorithm|sliding[\s-]*manifold',re.I)
five=re.compile(r'robot|manipulator|quadrotor|quadcopter|QUAVs?|multirotor|\bUAVs?\b|unmanned aerial|\bAUVs?\b|\bROVs?\b|\bUUVs?\b|underwater|exoskeleton|rehabilitation|wearable|drone|legged|wheeled|nonholonomic|aerial vehicle|haptic|prosthe',re.I)
other=re.compile(r'Euler[\s-]*Lagrange|mechanical system|soft|continuum|gripper|crane|ship|vessel|\bUSVs?\b|surface vehicle|marine|pendulum|underactuated|servo|(autonomous|unmanned|underwater|aerial|surface|ground|guided|intelligent|mobile)[\s-]*vehicle',re.I)
nonrob=re.compile(r'suspension|brak|anti[\s-]*lock|electric vehicle|\bEVs?\b|\bHEVs?\b|hybrid electric|car[\s-]*trailer|steering|in[\s-]*wheel|traction|powertrain|engine|microgrid|PMSM|permanent magnet|converter|inverter|power grid|battery|wind turbine|photovoltaic|vehicle dynamics|lateral stability|yaw (moment|stability)|lane[\s-]*keeping|platoon',re.I)
rows=[];nsk=0
for e in pool:
    k=e['doi'] or norm(e['title'])
    if (e['doi'] and e['doi'] in screened) or norm(e['title']) in screened: nsk+=1; continue
    t=e['title'];a=e['abstract'];akw=e['akw'] or '';kw=akw+' '+(e['kw'] or '')
    n=len(smc.findall(a)); main=bool(smc.search(t) or smc.search(akw)); p5=bool(five.search(t+' '+kw)); po=bool(other.search(t+' '+kw))
    dt=e['dt']
    revt=bool(re.search(r'review|survey|tutorial|overview|state[\s-]*of[\s-]*the[\s-]*art|perspective',t,re.I))
    if dt in ('Erratum','Book chapter','Conference paper','Proceedings Paper','Editorial Material','Correction'): dec,cod='EXCLUIR','I3 ('+dt+')'
    elif not a or len(a)<40: dec,cod='EXCLUIR','X3 sin resumen'
    elif revt and (p5 or po) and not main: dec,cod='CONTEXTO','revisión de control de plataforma (posicionamiento/brecha)'
    elif not (main or n>=2): dec,cod='EXCLUIR','X1/I1 SMC no principal'
    elif nonrob.search(t) and not five.search(t): dec,cod='EXCLUIR','X2 dominio no robótico (automoción/energía)'
    elif p5: dec,cod=('INCLUIR','I1+I2 provisional') if main else ('INCLUIR','DUDA I1: SMC solo en resumen; verificar RS3')
    elif po: dec,cod='INCLUIR','DUDA I2: plataforma fuera de las 5 clases; decidir en RS3'
    elif main and five.search(a): dec,cod='INCLUIR','DUDA I2: plataforma solo en resumen; verificar en RS3'
    else: dec,cod='EXCLUIR','X2/I2 sin plataforma robótica'
    cs=max(e.get('cites_SR07',0),e.get('cites_SR08',0)) if ({'SR07','SR08'}&e['cad']) else ''
    rows.append(dict(cadenas='|'.join(sorted(e['cad'])),anio=e['year'],citas_scopus=cs,tipo=dt,titulo=t,revista=e['journal'],doi=e['doi'],en_WoS='sí' if 'W12' in e['cad'] else '',decision=dec,codigo=cod+' (genérica)',rev_cercana='',citas_wos=e.get('cites_W12','')))
# CSV maestro de genericas
rows.sort(key=lambda r:-max(int(r['citas_scopus'] or 0),int(r['citas_wos'] or 0)))
for i,r in enumerate(rows,1): r['orden']=i
flds=['orden','cadenas','anio','citas_scopus','citas_wos','tipo','titulo','revista','doi','en_WoS','decision','codigo','rev_cercana']
w=csv.DictWriter(open(B+'CRIBADO_GENERICAS_RS2.csv','w',newline='',encoding='utf-8'),fieldnames=flds); w.writeheader(); w.writerows(rows)
print('N por cadena',N,'| pool fusionado',len(pool),'| ya cribados antes',nsk,'| a cribar',len(rows))
print(collections.Counter(r['decision'] for r in rows)); print(collections.Counter(r['cadenas'] for r in rows))
print(collections.Counter(r['codigo'][:26] for r in rows))
