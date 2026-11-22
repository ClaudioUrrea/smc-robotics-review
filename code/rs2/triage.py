import json,re,csv,sys
sys.path.insert(0,'./scripts')
pool=json.load(open('./work/analisis/pool_scopus.json'))
smc=re.compile(r'sliding[\s-]*mode|sliding[\s-]*surface|super[\s-]*twisting|terminal sliding|variable structure|\bSMC\b|\bSTA\b|twisting algorithm|sliding[\s-]*manifold',re.I)
plat=re.compile(r'robot|manipulator|quadrotor|quadcopter|QUAVs?|multirotor|\bUAVs?\b|unmanned aerial|\bAUVs?\b|\bROVs?\b|\bUUVs?\b|underwater|exoskeleton|rehabilitation|wearable|drone|legged|wheeled|mobile vehicle|nonholonomic|aerial vehicle|unmanned surface|\bUSV\b|marine vehicle|vessel|gripper|haptic|prosthe',re.I)
revw=re.compile(r'review|survey|tutorial|overview|state[\s-]*of[\s-]*the[\s-]*art|perspective|retrospective|histor|roadmap|advances|trends',re.I)
off=re.compile(r'PMSM|permanent magnet|motor|inverter|converter|rectifier|power|wind|battery|photovoltaic|solar|inventor|grid|induction|drive|lithium|frequency|networked|hydraulic|periodic|filter|estimation',re.I)
rows=[]
for k,e in pool.items():
    t=e['title']; a=e['abstract']; kw=(e.get('akw') or '')+' '+(e.get('kw') or '')
    text=' '.join([t,a,kw])
    ws=e.get('wos_screened')
    n_smc_abs=len(smc.findall(a))
    smc_main = bool(smc.search(t) or smc.search(e.get('akw') or ''))
    p = bool(plat.search(t+' '+kw))
    isrev = bool(revw.search(t)) and bool(smc.search(t)) and (n_smc_abs>=1 or bool(re.search('sliding',t,re.I)))
    y=int(e['year'] or 0)
    dec,cod='INCLUIR',''
    if ws:
        dec,cod=ws['decision'],'heredado de WoS ('+ws['codigo'][:40]+')'
    elif e['dt'] in ('Book chapter','Conference paper') and isrev and smc_main:
        dec,cod='CONTEXTO','I3 ('+e['dt']+') pero revisión/tutorial SMC: solo para introducción y comprobación de brecha'
    elif e['dt'] in ('Erratum','Book chapter','Conference paper'):
        dec,cod='EXCLUIR','I3 ('+e['dt']+')'
    elif not a or len(a)<40:
        dec,cod='EXCLUIR','X3 sin resumen'
    elif y<2016 and not ('SR06' in e['pool'] or isrev):
        dec,cod='EXCLUIR','I4 año<2016'
    elif not (smc_main or n_smc_abs>=2):
        dec,cod='EXCLUIR','X1/I1 SMC no principal'
    elif not smc_main:
        dec,cod='INCLUIR','DUDA I1: SMC solo en resumen; verificar RS3'
    elif not p and isrev and off.search(t):
        dec,cod='CONTEXTO','X2 revisión SMC en dominio no robótico: solo comprobación de brecha'
    elif not p and not isrev and smc_main and plat.search(a):
        dec,cod='INCLUIR','DUDA I2: plataforma solo en resumen; verificar en RS3'
    elif not p and not isrev:
        dec,cod='EXCLUIR','X2/I2 sin plataforma robótica'
    else:
        cod='I1+I2'+(' revisión/tutorial' if isrev else '')+' provisional'
    rows.append(dict(cadenas='|'.join(sorted(e['pool'])),anio=e['year'],citas_scopus=e['cites'],tipo=e['dt'],titulo=e['title'],revista=e['journal'],doi=e['doi'],en_WoS='sí' if e['in_wos'] else 'no',decision=dec,codigo=cod,rev_cercana='sí' if isrev else ''))
rows.sort(key=lambda r:-int(r['citas_scopus']))
for i,r in enumerate(rows,1): r['orden']=i
w=csv.DictWriter(open('./work/CRIBADO_SCOPUS_RS2.csv','w',newline='',encoding='utf-8'),fieldnames=['orden']+[k for k in rows[0] if k!='orden'])
w.writeheader(); w.writerows(rows)
import collections
print(collections.Counter(r['decision'] for r in rows)); print(collections.Counter(r['codigo'].split(' (')[0].split(';')[0][:30] for r in rows))
