# RS3: resolución de DUDA I1/I2, decisión del canon, formulario de extracción (desde título + resumen + palabras clave del autor),
# selección del corpus de síntesis y tablas suplementarias. Reglas explícitas y reproducibles; no hay lectura de texto completo.
import csv,json,re,collections,math
B='./work/'; R=B+'RS3/'
import sys; sys.path.insert(0,'./scripts'); from rs3_clean import clean
rows=list(csv.DictReader(open(B+'CORPUS_RS2_UNIFICADO.csv',encoding='utf-8-sig')))
for _r in rows: _r['titulo']=clean(_r['titulo']); _r['revista']=clean(_r['revista'])
AB=json.load(open(R+'abstracts_cache.json'))
FIVE={'Manipulador','Móvil terrestre/patas','Aéreo','Submarino/marino','Exoesqueleto/rehabilitación/médico'}
SMC=re.compile(r'sliding[\s-]*mode|sliding[\s-]*surface|sliding[\s-]*manifold|sliding[\s-]*variable|super[\s-]*twisting|terminal sliding|variable[\s-]*structure|\b\w*TSMC?\b|\b\w*SMC\b|\bSMO\b|twisting algorithm|\bHOSM\b|\bSOSM',re.I)
CMP=re.compile(r'compar|outperform|superior to|better than|than (the )?(conventional|traditional|classical|standard|existing|ordinary)',re.I)
METH=re.compile(r'(propos|design|develop|present|introduc|novel|employ|adopt|utili[sz]|investigat|construct|establish|devise|synthes|integrat|combin)[^.]{0,180}(sliding|super[\s-]*twisting|terminal sliding|\bSMC\b|variable[\s-]*structure|\bSMO\b)|(sliding|super[\s-]*twisting|\bSMC\b)[^.]{0,60}(is|are) (proposed|designed|developed|presented|adopted|employed|used|applied)|(based on|using|via|with)[^.]{0,30}(sliding[\s-]*mode|super[\s-]*twisting|terminal sliding|\bSMC\b)',re.I)
ROBOT=re.compile(r'\brobot\w*|manipulator|mechatronic|haptic|humanoid|gripper|end[\s-]*effector|exoskeleton|\bAUVs?\b|\bROVs?\b|quadrotor|quadcopter|\bUAVs?\b|unmanned|underwater|legged|wheeled|nonholonomic|mobile (platform|vehicle)',re.I)
def i1_ok(r,a):
    t=r['titulo']
    if re.search(r'grating[\s-]*sliding|triboelectric|nanogenerator',t,re.I): return False,'X1 «sliding» no es SMC (dispositivo deslizante)'
    if SMC.search(t): return True,'SMC en título'
    n=len(SMC.findall(a)); kw=AB.get(r['id'],{}).get('k','')
    sents=[x for x in re.split(r'(?<=[.;])\s+',a) if SMC.search(x)]
    if sents and all(CMP.search(x) for x in sents) and not SMC.search(kw): return False,'SMC solo en frases de comparación (línea base)'
    if SMC.search(kw) and n>=1: return True,'SMC en palabras clave del autor + resumen'
    if METH.search(a): return True,'SMC como método (resumen)'
    if n>=3: return True,'SMC ≥3 menciones'
    if n>=2 and not CMP.search(a): return True,'SMC ≥2 menciones sin comparación'
    return False,'SMC solo mención/línea base'
ROBOT2=re.compile(ROBOT.pattern+r'|\bUSVs?\b|\bASVs?\b|surface vehicle|autonomous (vehicle|vessel|ship|surface|underwater|aerial|ground)|drone|helicopter|multi[\s-]*rotor|hexacopter|octocopter|rehabilitation (robot|exoskeleton|device|system|glove|orthosis)|prosthe|multi[\\s-]*robot|\\bAGVs?\\b|automated guided|cobot|collaborative robot|Stewart|hexapod|parallel (platform|mechanism|manipulator|robot)|soft robot|micro[\\s-]*hand|parallel kinematic|kinematic machine|rotorcraft|\\bVTOL\\b|remotely[\\s-]*operated vehicle|micro[\\s-]*manipulat|agricultural (vehicle|robot)|field robot|bionic|orthosis|\bbiped|quadruped|\btracked|tractor|omnidirectional|self[\s-]*balancing|two[\s-]*wheeled|parallel (mechanism|robot)|cable[\s-]*driven|\bSCARA|flexible[\s-]*joint|mechanical arm|\brobotic|\w+[\s-]*link (robot|manipulator|arm)|(\d|two|three|four|six)[\s-]*(DOF|degrees?[\s-]*of[\s-]*freedom) (robot|manipulator|arm)|soft actuator|continuum|space robot',re.I)
REV=re.compile(r'review|survey|tutorial|overview|state[\s-]*of[\s-]*the[\s-]*art|perspective|roadmap|advances|trends',re.I)
PT=[]
PT=[('Exoesqueleto/rehabilitación/médico',r'exoskeleton|rehabilitation|prosthe|wearable|surgical|medical|upper[\s-]*limb|lower[\s-]*limb|orthos|ankle|knee|gait|hand rehabilitation|lower extremity'),
('Submarino/marino',r'underwater|\bAUVs?\b|\bROVs?\b|\bUUVs?\b|marine|vessel|\bships?\b|\bUSVs?\b|surface vehicle|hovercraft|underactuated surface'),
('Aéreo',r'quadrotor|quadcopter|multi[\s-]*rotor|\bUAVs?\b|\bQUAVs?\b|unmanned aerial|drone|helicopter|hexacopter|octocopter|tilt[\s-]*rotor|aerial'),
('Espacial',r'space robot|spacecraft|on[\s-]*orbit|free[\s-]*floating|space manipulator|tethered'),
('Móvil terrestre/patas',r'mobile robot|wheeled|nonholonomic|differential[\s-]*drive|car[\s-]*like|tracked|omnidirectional|mecanum|legged|quadruped|biped|humanoid|self[\s-]*balancing|two[\s-]*wheeled|tractor|autonomous vehicle|ground vehicle|walking'),
('Manipulador',r'manipulator|robot(ic)? arm|\b\w+[\s-]*link|SCARA|parallel robot|delta robot|flexible[\s-]*joint|end[\s-]*effector|\bDOF\b|degree[s]?[\s-]*of[\s-]*freedom|PUMA|industrial robot|cable[\s-]*driven|teleoperat'),
('Blando/continuo/pinza',r'soft robot|continuum|gripper|pneumatic artificial muscle|\bPAM\b')]

PT=[(n,(r'exoskeleton|prosthe|orthos|rehabilitation (robot|exoskeleton|device|glove)|(surgical|medical|wearable|assistive) robot|upper[\s-]*limb (robot|exoskeleton)|lower[\s-]*limb (robot|exoskeleton)|gait (robot|exoskeleton|assist)' if n.startswith('Exoesqueleto') else p).replace(r'\b\w+[\s-]*link|',r'\b\w+[\s-]*link (robot|manipulator|arm)|').replace(r'|\bDOF\b|degree[s]?[\s-]*of[\s-]*freedom',r'|(DOF|degrees?[\s-]*of[\s-]*freedom) (robot|manipulator|arm|exoskeleton)').replace(r'|marine|',r'|marine (vehicle|vessel|craft|robot|surface)|')) for n,p in PT]
IEEE_T={x.lower() for x in ['Legged locomotion','Marine vehicles','Manipulator dynamics','Manipulators','Robots','Mobile robots','Autonomous aerial vehicles','Space vehicles','Underwater vehicles','Autonomous underwater vehicles','Robot kinematics','Robot sensing systems','Service robots','Humanoid robots','Exoskeletons','Unmanned aerial vehicles','Aircraft','Vehicle dynamics','Wheels','Robot control','Grippers','Aerospace electronics','Aerospace and electronic systems','Rotors','Propellers','Collaborative robots','Robot motion','Robot arms','End effectors','Joints','Drones','Quadrotors','Helicopters','Sea surface','Oceans','Medical robotics','Wearable robots','Robotics and automation','Kinematics','Legged robots','Wheeled robots','Multi-robot systems','Space robotics','Underwater robots','Aerial robots','Surgical robots','Rehabilitation robotics','Mobile robot','Robot']}
def plat_title(r):
    t=r['titulo']; kw=AB.get(r['id'],{}).get('k',''); ab=AB.get(r['id'],{}).get('a','')
    for n,p in PT:
        if re.search(p,t,re.I): return n
    # palabras clave: los términos del tesauro IEEE (que aparecen incluso como «palabras clave de autor») solo cuentan si el resumen confirma un robot
    terms=[x.strip() for x in kw.split(';') if x.strip()]
    own=' ; '.join(x for x in terms if x.lower() not in IEEE_T); ieee=' ; '.join(x for x in terms if x.lower() in IEEE_T)
    for n,p in PT:
        if re.search(p,own,re.I): return n
        if re.search(p,ieee,re.I) and ROBOT2.search(ab): return n
    return ''
def i2_ok(r,a):
    t=r['titulo']+' '+a; p=r['plataforma_auto']
    if p=='Espacial' and not re.search(r'\brobot\w*|manipulator',t,re.I): return False,'X2 plataforma espacial sin robot (satélite/nave)'
    NONROB=re.compile(r'\bcranes?\b|launch vehicle|rectifier|converter|inverter|\bPMSM|permanent magnet|battery|fuel cell|power grid|microgrid|photoelectric|wind turbine|maglev|vehicle suspension|brak',re.I)
    if NONROB.search(r['titulo']): return False,'X2 dominio no robótico en título'
    pt=plat_title(r)
    if pt and pt!='Espacial': return True,'plataforma en título/palabras clave ('+pt+')'
    if ROBOT2.search(r['titulo']): return True,'término robótico en título'
    hits={m.group(0).lower() for m in ROBOT2.finditer(a)}
    VAL=re.compile(r'(simulat|experiment|validat|verif|demonstrat|illustrat|applied to|application to|implemented on|tested on|test[\s-]*bed|example)[^.]{0,90}('+ROBOT2.pattern+r')|('+ROBOT2.pattern+r')[^.]{0,60}(simulat|experiment|validat|demonstrat|illustrat|example)',re.I)
    if VAL.search(a): return True,'robot como ejemplo de validación en resumen'
    if len(ROBOT2.findall(a))>=3: return True,'plataforma robótica ≥3 veces en resumen'
    first=re.split(r'(?<=\.)\s+',a)[0] if a else ''
    if re.search(r'\brobot\w*|manipulator|quadrotor|\bUAVs?\b|\bAUVs?\b|exoskeleton',first,re.I) and not re.search(r'such as|e\.g\.|including|applications? in|fields? of|used to model|models? of|modell?ing of',first,re.I) and SMC.search(r['titulo']+' '+AB.get(r['id'],{}).get('k','')): return True,'plataforma robótica en la frase inicial del resumen'
    return False,'X2 sin plataforma robótica en título/resumen (péndulo/grúa/servo/multiagente/EL genérico)'
dud={}
out=[]
for r in rows:
    r=dict(r); r['dec_rs3']=r['decision']; r['regla_rs3']=''; r['plat_rs3']=r['plataforma_auto']
    a=AB.get(r['id'],{}).get('a','')
    c=r['codigo']
    if r['decision']=='INCLUIR' and r['anio']>='2016':
        flagged=('DUDA' in c) or ('verificar' in c)
        lang=AB.get(r['id'],{}).get('lang','')
        if lang:
            r['dec_rs3']='EXCLUIR'; r['regla_rs3']='I3 idioma no inglés según Scopus ('+lang+')'
        elif not a:
            tt=r['titulo']
            if SMC.search(tt) and ROBOT2.search(tt): r['regla_rs3']='sin resumen; aceptado por título (SMC + plataforma)'
            else:
                r['dec_rs3']='EXCLUIR'; r['regla_rs3']='X3 sin resumen y título insuficiente'
        else:
            ok1,w1=i1_ok(r,a); ok2,w2=i2_ok(r,a)
            r['regla_rs3']='I1: '+w1+' | I2: '+w2
            if not(ok1 and ok2):
                if ((r['tipo'] and 'review' in r['tipo'].lower()) or REV.search(r['titulo'])) and ok1 and not ok2:
                    r['dec_rs3']='CONTEXTO'; r['regla_rs3']+=' | revisión de SMC sin plataforma → CONTEXTO'
                else: r['dec_rs3']='EXCLUIR'
            elif r['plataforma_auto'] not in FIVE|{'Blando/continuo/pinza','Espacial'}: r['plat_rs3']='Robot genérico (EL/subactuado)'
        r['plataforma_nivel']=('ejemplo de validación' if 'ejemplo de validación' in r['regla_rs3'] or '≥3 veces' in r['regla_rs3'] else 'principal') if r['dec_rs3']=='INCLUIR' else ''
        if flagged or r['dec_rs3']!='INCLUIR': dud[r['id']]=(c,r['dec_rs3'],r['regla_rs3'])
    elif r['decision']=='CANDIDATO CANÓNICO':
        spacecraft=r['id'] in('R2-07284','R2-07316','R2-07317')
        r['dec_rs3']='CONTEXTO' if spacecraft else 'INCLUIR (E-F)'
        r['regla_rs3']='canon: nave espacial sin robot → solo contexto' if spacecraft else 'canon: referencia histórica/teórica de SMC con plataforma mecánica (decisión RS3)'
    out.append(r)
# ---------- corrección de plataforma (RS4): «Exoesqueleto/médico» sin ningún término de la clase se reasigna
EXO_STRICT=re.compile(r'exoskeleton|exosuit|prosthe|orthos|rehabilitat|surgical|medical robot|wearable robot|assistive robot|upper[\s-]*limb|lower[\s-]*limb|gait|ankle|knee|wrist|elbow|hand rehabilitation|finger|catheter|needle|endoscop|ultrasound robot|patient|human[\s-]*robot',re.I)
for _r in out:
    if _r.get('plat_rs3','').startswith('Exo'):
        d=AB.get(_r['id'],{}); t=_r['titulo']+' '+d.get('k','')+' '+d.get('a','')
        if not EXO_STRICT.search(t):
            _r['plat_rs3']=next((n for n,p in PT if not n.startswith('Exo') and re.search(p,t,re.I)),'Robot genérico (EL/subactuado)')
# ---------- recodificación de variantes (RS3 v2.3): título + palabras clave + resumen (frases que no son comparación)
VR=[('STA/HOSM',r'super[\s-]*twisting|high(er)?[\s-]*order sliding|second[\s-]*order sliding|\bSOSM|twisting algorithm|\bHOSM\b|arbitrary[\s-]*order sliding|continuous sliding|\bSTA\b|\bSTSMC?\b'),
('Terminal (TSM/NTSM/FTSM)',r'terminal sliding|\bN?F?TSM[C]?\b|nonsingular terminal|non-singular terminal|terminal attractor'),
('Tiempo finito/fijo/predefinido',r'finite[\s-]*time|fixed[\s-]*time|predefined[\s-]*time|prescribed[\s-]*time|appointed[\s-]*time|practical[\s-]*fixed|arbitrary[\s-]*time'),
('Integral (ISM)',r'integral[\w\s-]{0,25}sliding|\bI(T)?SMC?\b|integral[\s-]*(type|terminal)'),
('Adaptativo',r'adaptive|adaptation law|self[\s-]*tuning|gain[\s-]*adaptation'),
('Inteligente (neuronal/difuso/aprendizaje)',r'neural|fuzzy|\bRBF|reinforcement learning|deep learning|learning[\s-]*based|online learning|actor[\s-]*critic|adaptive dynamic programming|\bADP\b|ANFIS|data[\s-]*driven'),
('Optimización metaheurística',r'genetic algorithm|particle swarm|\bPSO\b|grey[\s-]*wolf|metaheuristic|optimi[sz]ation algorithm|whale|evolutionary|swarm algorithm'),
('Fraccionario',r'fractional'),
('Basado en observador',r'observer|\bESO\b|disturbance estimat|time[\s-]*delay estimat|\bTDE\b|estimator'),
('Disparo por eventos/discreto',r'event[\s-]*trigger|self[\s-]*trigger|discrete[\s-]*time|sampled[\s-]*data|digital implementation|implicit'),
('Tolerante a fallas',r'fault[\s-]*tolerant|actuator fault|fault[\s-]*estimat'),
('Backstepping híbrido',r'backstepping'),
('MPC híbrido',r'predictive control|\bMPC\b'),
('Multiagente/formación',r'\bformation|\bconsensus|containment|multi[\s-]*agent|cooperative|swarm(?! algorithm)')]
def recode_var(r):
    d=AB.get(r['id'],{}); a=d.get('a','')
    sents=[x for x in re.split(r'(?<=[.;])\s+',a) if not CMP.search(x)]
    t=r['titulo']+' . '+d.get('k','')+' . '+' '.join(sents)
    v=[n for n,p in VR if re.search(p,t,re.I)]
    return '; '.join(v) or 'Convencional/primer orden'
for _r in out:
    if _r['dec_rs3'] in ('INCLUIR','INCLUIR (E-F)','CONTEXTO') and AB.get(_r['id'],{}).get('a'):
        _r['variante_rs2']=_r['variante_auto']; _r['variante_auto']=recode_var(_r)
# ---------- extracción de campos
def has(p,s): return bool(re.search(p,s,re.I))
def ext(r):
    d=AB.get(r['id'],{}); a=d.get('a',''); k=d.get('k','')
    s=r['titulo']+' . '+a+' . '+k
    if not a: return dict(garantia_con_inferencia='sin resumen',objetivo='sin resumen',chattering='sin resumen',incertidumbre='sin resumen',observador='sin resumen',convergencia='sin resumen',validacion='sin resumen',gdl='sin resumen',impl_discreta='sin resumen',codigo_disponible='no detectado')
    o=('formación' if has(r'\bformation|\bconsensus|containment control|multi[\s-]*agent|multi[\s-]*(robot|UAV|AUV|vehicle|vessel|quadrotor)s?|cooperative (control|tracking|transport)[^.]{0,40}(robots|UAVs|vehicles|agents|vessels)|leader[\s-]*follower|swarm',s) else 'fuerza/contacto' if has(r'force control|force tracking|impedance|admittance|contact force|contact (task|motion)|interaction force',s) else 'estabilización/regulación' if has(r'stabili[sz]ation|regulation|set[\s-]*point|balanc|point[\s-]*to[\s-]*point',s) and not has(r'tracking|trajectory',s) else 'seguimiento' if has(r'tracking|trajectory|path[\s-]*follow|reference|attitude control|altitude|depth control|heading control|position control|motion control|landing|hover|docking|berthing|gait|assist',s) else 'no especificado')
    ch=[]
    if has(r'boundary[\s-]*layer|saturation function|\bsat\(|sigmoid|hyperbolic tangent|\btanh|continuous approximation|smooth(ed)? (sign|control)|quasi[\s-]*sliding',s): ch.append('capa límite/aprox. continua')
    if has(r'super[\s-]*twisting|high(er)?[\s-]*order sliding|second[\s-]*order sliding|\bHOSM|\bSOSM|twisting algorithm',s): ch.append('orden superior (STA/HOSM)')
    if has(r'adaptive (gain|switching|law|reaching)|gain[\s-]*adapt|time[\s-]*varying gain|dynamic gain',s): ch.append('ganancia adaptativa')
    if has(r'disturbance observer|\bDOB\b|extended state observer|\bESO\b|\bTDE\b|time[\s-]*delay estimation|uncertainty estimat|disturbance estimat',s) and has(r'chatter|switching gain|reduc',s): ch.append('compensación por observador')
    if has(r'chatter',s) and not ch: ch.append('chattering mencionado sin técnica explícita')
    chat='; '.join(ch) if ch else 'no reportado en resumen'
    inc=[]
    if has(r'disturbance',s): inc.append('perturbación externa')
    if has(r'uncertain|unmodel|unknown dynamics|parametric|model(ing)? error',s): inc.append('incertidumbre paramétrica/dinámica')
    if has(r'fault',s): inc.append('fallas')
    if has(r'saturat',s): inc.append('saturación')
    if has(r'time[\s-]*delay|delayed',s): inc.append('retardo')
    if has(r'noise|measurement error',s): inc.append('ruido')
    ob='sí' if has(r'observer|\bESO\b|estimator|\bTDE\b|differentiator|\bSMO\b',s) else 'no'
    cv=('prescrita/predefinida' if has(r'prescribed[\s-]*time|predefined[\s-]*time',s) else 'tiempo fijo' if has(r'fixed[\s-]*time',s) else 'tiempo finito' if has(r'finite[\s-]*time',s) else 'asintótica/exponencial' if has(r'asymptotic|exponential(ly)? (stab|converg)|uniformly ultimately|\bUUB\b|ultimate(ly)? bound',s) else 'no especificada')
    hil=has(r'hardware[\s-]*in[\s-]*the[\s-]*loop|\bHIL\b|processor[\s-]*in[\s-]*the[\s-]*loop|software[\s-]*in[\s-]*the[\s-]*loop',s)
    exp=has(r'experiment|real[\s-]*time implementation|hardware|test[\s-]*bed|prototype|laborator|validated on|physical platform|real robot|on a real|testing platform|flight test|sea trial|field test',s)
    sim=has(r'simulat|numerical|matlab|simulink|gazebo|coppelia|v-rep',s)
    v=('HIL' if hil else '')+('; ' if hil and (exp or sim) else '')
    v+=('experimento' if exp else '')+('; ' if exp and sim else '')+('simulación' if sim else '')
    v=v or 'no indicada en resumen'
    g=re.search(r'\b(\d+|two|three|four|five|six|seven)[\s-]*(DOF|DoF|degrees?[\s-]*of[\s-]*freedom|link)',s,re.I)
    gd=g.group(0).lower().replace('-',' ') if g else 'no indicado'
    di='sí' if has(r'discrete[\s-]*time|sampled[\s-]*data|digital|implicit|event[\s-]*trigger|discretiz|discretis',s) else 'no'
    cd='sí (mención)' if has(r'github|open[\s-]*source|code (is|are) (available|publicly)|source code',s) else 'no detectado (solo resumen)'
    vv=r.get('variante_auto','')
    gi=cv if cv!='no especificada' else ('tiempo finito (implícita: TSM)' if 'Terminal' in vv else 'tiempo finito (implícita: STA/HOSM)' if 'STA' in vv else 'no especificada')
    return dict(garantia_con_inferencia=gi,objetivo=o,chattering=chat,incertidumbre='; '.join(inc) or 'no especificada',observador=ob,convergencia=cv,validacion=v,gdl=gd,impl_discreta=di,codigo_disponible=cd)
map_rows=[]
for r in out:
    if r['dec_rs3'] in('INCLUIR','INCLUIR (E-F)') or r['dec_rs3']=='CONTEXTO':
        r.update(ext(r)); map_rows.append(r)
inc=[r for r in out if r['dec_rs3']=='INCLUIR' and r['anio']>='2016']
C=collections.Counter
print('DUDA/verificación resueltas:',len(dud),C(v[1] for v in dud.values()))
print('INCLUIR 2016+ tras RS3:',len(inc),'| previos 7226 | excluidos RS3:',C(r['regla_rs3'].split(':')[0][:2] if r['dec_rs3']=='EXCLUIR' and r['decision']!='EXCLUIR' else '' for r in out if r['dec_rs3']=='EXCLUIR' and r['decision']=='INCLUIR'))
print('motivos:',C(r['regla_rs3'][:60] for r in out if r['dec_rs3']=='EXCLUIR' and r['decision']=='INCLUIR').most_common(12))
print('plataforma',C(r['plat_rs3'] for r in inc))
print('validacion',C(r['validacion'] for r in inc).most_common(8))
json.dump(out,open(R+'_out_tmp.json','w'),ensure_ascii=False)
