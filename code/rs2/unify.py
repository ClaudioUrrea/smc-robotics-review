# Fusión del corpus RS2 (WoS + Scopus + genéricas + bola de nieve + canon) con dedupe DOI/título y codificación automática provisional.
import csv,json,re,glob,sys,collections
sys.path.insert(0,'./scripts'); from parse import norm,doi_n,recs,field
B='./work/'
# --- resúmenes y palabras clave desde todos los .bib
AB={}
def addab(doi,t,a,k):
    for key in (doi_n(doi) if doi else None, norm(t)):
        if key and (key not in AB or len(a)>len(AB[key][0])): AB[key]=(a or '',k or '')
for f in glob.glob('./work/*.bib')+glob.glob(B+'respaldos_wos/*.bib'):
    for r in recs(f): addab(field(r,'DOI'),field(r,'Title'),field(r,'Abstract'),field(r,'Keywords'))
for f in glob.glob(B+'respaldos_scopus/*.bib'):
    for r in recs(f): addab(field(r,'doi'),field(r,'title'),field(r,'abstract'),field(r,'author_keywords'))
# --- fuentes
U={}; T={}
def key(doi,t):
    d=doi_n(doi) if doi and doi!='por verificar' else ''
    nt=norm(t)
    if d and d in U: return d
    if nt in T: return T[nt]
    return d or nt
RANK={'INCLUIR':3,'CONTEXTO':2,'CANDIDATO CANÓNICO':2,'EXCLUIR':1}
def add(estrato,fuente,r,cites):
    k=key(r.get('doi',''),r['titulo'])
    e=U.get(k)
    if not e:
        e=U[k]=dict(doi=doi_n(r['doi']) if r.get('doi') and r['doi']!='por verificar' else '',titulo=r['titulo'],anio=r.get('anio',''),revista=r.get('revista',''),tipo=r.get('tipo',''),citas_max=0,estratos=set(),fuentes=set(),decisiones=[],codigo='',rev_cercana='')
        T[norm(r['titulo'])]=k
    e['estratos'].add(estrato); e['fuentes'].update(x for x in fuente.split('|') if x)
    try: e['citas_max']=max(e['citas_max'],int(cites or 0))
    except: pass
    e['decisiones'].append(r['decision'])
    if RANK.get(r['decision'],0)>=max([RANK.get(x,0) for x in e['decisiones'][:-1]]+[0]): e['codigo']=r.get('codigo','')
    if r.get('rev_cercana')=='sí': e['rev_cercana']='sí'
    if not e['doi'] and r.get('doi') and r['doi']!='por verificar': e['doi']=doi_n(r['doi'])
    if not e['tipo']: e['tipo']=r.get('tipo','')
for r in csv.DictReader(open(B+'CRIBADO_WOS_RS2.csv',encoding='utf-8')): add('E-WoS',r['cadenas'],r,r['citas'])
for r in csv.DictReader(open(B+'CRIBADO_SCOPUS_RS2.csv',encoding='utf-8')): add('E-Scopus',r['cadenas'],r,r['citas_scopus'])
for r in csv.DictReader(open(B+'CRIBADO_GENERICAS_RS2.csv',encoding='utf-8')): add('E-Gen',r['cadenas'],r,max(int(r['citas_scopus'] or 0),int(r['citas_wos'] or 0)))
for r in csv.DictReader(open(B+'CRIBADO_SNOWBALL_RS2.csv',encoding='utf-8')): add('E-SB',r['origen'],r,r['citas_crossref'])
for r in csv.DictReader(open(B+'CANON_FUNDACIONAL.csv',encoding='utf-8')):
    r=dict(r,decision='INCLUIR',codigo='E-F canon fundacional (selección experta): '+r['estado'][:60])
    add('E-F','canon',r,r['citas_crossref'])
# --- codificación automática provisional
V=[('STA/HOSM',r'super[\s-]*twisting|high(er)?[\s-]*order sliding|second[\s-]*order sliding|\bSOSM|twisting algorithm|\bHOSM\b|arbitrary[\s-]*order sliding|continuous sliding'),
('Terminal (TSM/NTSM/FTSM)',r'terminal sliding|\bN?F?TSM[C]?\b|nonsingular terminal|non-singular terminal'),
('Tiempo finito/fijo/predefinido',r'finite[\s-]*time|fixed[\s-]*time|predefined[\s-]*time|prescribed[\s-]*time|practical[\s-]*fixed'),
('Integral (ISM)',r'integral sliding|\bI?SMC?\b.{0,3}integral|integral[\s-]*(type|terminal)'),
('Adaptativo',r'adaptive|adaptation law|self[\s-]*tuning|gain[\s-]*adaptation'),
('Inteligente (neuronal/difuso/aprendizaje)',r'neural|fuzzy|\bRBF|reinforcement learning|deep learning|learning[\s-]*based|ANFIS|data[\s-]*driven|model[\s-]*free'),
('Optimización metaheurística',r'genetic algorithm|particle swarm|\bPSO\b|grey[\s-]*wolf|metaheuristic|optimi[sz]ation algorithm|whale|evolutionary'),
('Fraccionario',r'fractional'),
('Basado en observador',r'observer|\bESO\b|disturbance estimat|time[\s-]*delay estimat|\bTDE\b|estimator'),
('Disparo por eventos/discreto',r'event[\s-]*trigger|self[\s-]*trigger|discrete[\s-]*time|sampled[\s-]*data|digital implementation|implicit'),
('Tolerante a fallas',r'fault[\s-]*tolerant|actuator fault|fault[\s-]*estimat'),
('Backstepping híbrido',r'backstepping'),
('MPC híbrido',r'predictive control|\bMPC\b'),
('Multiagente/formación',r'formation|consensus|multi[\s-]*agent|cooperative|swarm|containment')]
P=[('Exoesqueleto/rehabilitación/médico',r'exoskeleton|rehabilitation|prosthe|wearable|surgical|medical|upper[\s-]*limb|lower[\s-]*limb|orthos|ankle|knee|gait|hand rehabilitation|lower extremity'),
('Submarino/marino',r'underwater|\bAUVs?\b|\bROVs?\b|\bUUVs?\b|marine|vessel|\bships?\b|\bUSVs?\b|surface vehicle|hovercraft|underactuated surface'),
('Aéreo',r'quadrotor|quadcopter|multi[\s-]*rotor|\bUAVs?\b|\bQUAVs?\b|unmanned aerial|drone|helicopter|hexacopter|octocopter|tilt[\s-]*rotor|aerial'),
('Espacial',r'space robot|spacecraft|on[\s-]*orbit|free[\s-]*floating|space manipulator|tethered'),
('Móvil terrestre/patas',r'mobile robot|wheeled|nonholonomic|differential[\s-]*drive|car[\s-]*like|tracked|omnidirectional|mecanum|legged|quadruped|biped|humanoid|self[\s-]*balancing|two[\s-]*wheeled|tractor|autonomous vehicle|ground vehicle|walking'),
('Manipulador',r'manipulator|robot(ic)? arm|\b\w+[\s-]*link|SCARA|parallel robot|delta robot|flexible[\s-]*joint|end[\s-]*effector|\bDOF\b|degree[s]?[\s-]*of[\s-]*freedom|PUMA|industrial robot|cable[\s-]*driven|teleoperat'),
('Blando/continuo/pinza',r'soft robot|continuum|gripper|pneumatic artificial muscle|\bPAM\b')]
EXP=re.compile(r'experiment|real[\s-]*time implementation|hardware|test[\s-]*bed|prototype|laboratory|validated on|physical platform|real robot|on a real|testing platform',re.I)
def code(e):
    ab,kw=AB.get(e['doi'],AB.get(norm(e['titulo']),('','')))
    tk=e['titulo']+' '+kw; full=tk+' '+ab
    var=[n for n,p in V if re.search(p,tk,re.I)] or [n for n,p in V if len(re.findall(p,ab,re.I))>=2]
    pl=[n for n,p in P if re.search(p,tk,re.I)] or [n for n,p in P if re.search(p,ab,re.I)]
    return '; '.join(var) or 'Convencional/primer orden', (pl[0] if pl else 'Otro/genérico (EL, subactuado)'), ('sí' if EXP.search(ab) else ('no' if ab else 'sin resumen')), bool(ab)
rows=[]
for k,e in U.items():
    dec=max(e['decisiones'],key=lambda x:RANK.get(x,0))
    conf='sí' if len({RANK.get(x,0) for x in e['decisiones']})>1 else ''
    v,p,x,hab=code(e)
    if isinstance(e['anio'],str) and not e['anio'].isdigit(): e['anio']=re.sub(r'\D','',e['anio'])[:4]
    rows.append(dict(id='',estrato='|'.join(sorted(e['estratos'])),fuentes='|'.join(sorted(e['fuentes'])),anio=e['anio'],titulo=e['titulo'],revista=e['revista'],doi=e['doi'],tipo=e['tipo'],citas_max=e['citas_max'],decision=dec,conflicto_fuentes=conf,codigo=e['codigo'],rev_cercana=e['rev_cercana'],variante_auto=v,plataforma_auto=p,experimental_auto=x))
rows.sort(key=lambda r:({'INCLUIR':0,'CONTEXTO':1,'CANDIDATO CANÓNICO':1,'EXCLUIR':2}.get(r['decision'],3),-int(r['citas_max'] or 0)))
for i,r in enumerate(rows,1): r['id']='R2-%05d'%i
w=csv.DictWriter(open(B+'CORPUS_RS2_UNIFICADO.csv','w',newline='',encoding='utf-8-sig'),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
C=collections.Counter
inc=[r for r in rows if r['decision']=='INCLUIR']
print('total',len(rows),C(r['decision'] for r in rows)); print('conflictos',sum(1 for r in rows if r['conflicto_fuentes']))
print('estratos INCLUIR',C(r['estrato'] for r in inc).most_common(12))
print('plataforma',C(r['plataforma_auto'] for r in inc)); print('experimental',C(r['experimental_auto'] for r in inc))
vc=C(); [vc.update(r['variante_auto'].split('; ')) for r in inc]; print('variantes',vc.most_common())
json.dump(dict(total=len(rows),dec=C(r['decision'] for r in rows),plat=C(r['plataforma_auto'] for r in inc),var=vc,exp=C(r['experimental_auto'] for r in inc),anio=C(r['anio'] for r in inc)),open(B+'analisis/resumen_corpus.json','w'),ensure_ascii=False,indent=1)
