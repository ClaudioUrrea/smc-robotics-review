import json,urllib.parse,urllib.request,difflib,re,csv,time,sys
canon=[
("Utkin 1977","Variable structure systems with sliding modes","Utkin",1977),
("Utkin 1993","Sliding mode control design principles and applications to electric drives","Utkin",1993),
("Utkin 1973","Sliding modes in multidimensional systems with variable structure","Utkin",1973),
("Slotine & Sastry 1983","Tracking control of non-linear systems using sliding surfaces, with application to robot manipulators","Slotine",1983),
("Slotine 1984","Sliding controller design for non-linear systems","Slotine",1984),
("Slotine 1985","The robust control of robot manipulators","Slotine",1985),
("Young 1978","Controller design for a manipulator using theory of variable structure systems","Young",1978),
("Young Utkin Ozguner 1999","A control engineer's guide to sliding mode control","Young",1999),
("Hung Gao Hung 1993","Variable structure control: a survey","Hung",1993),
("DeCarlo Zak Matthews 1988","Variable structure control of nonlinear multivariable systems: a tutorial","DeCarlo",1988),
("Drakunov Utkin 1992","Sliding mode control in dynamic systems","Drakunov",1992),
("Levant 1993","Sliding order and sliding accuracy in sliding mode control","Levant",1993),
("Levant 1998","Robust exact differentiation via sliding mode technique","Levant",1998),
("Levant 2003","Higher-order sliding modes, differentiation and output-feedback control","Levant",2003),
("Bartolini 1998","Chattering avoidance by second-order sliding mode control","Bartolini",1998),
("Man Paplinski Wu 1994","A robust MIMO terminal sliding mode control scheme for rigid robotic manipulators","Man",1994),
("Venkataraman Gulati 1993","Control of nonlinear systems using terminal sliding modes","Venkataraman",1993),
("Feng Yu Man 2002","Non-singular terminal sliding mode control of rigid manipulators","Feng",2002),
("Moreno Osorio 2008","A Lyapunov approach to second-order sliding mode controllers and observers","Moreno",2008),
("Moreno Osorio 2012","Strict Lyapunov functions for the super-twisting algorithm","Moreno",2012),
("Polyakov Fridman 2014","Stability notions and Lyapunov functions for sliding mode control systems","Polyakov",2014),
("Lee Utkin 2007","Chattering suppression methods in sliding mode control systems","Lee",2007),
("Plestan 2010","New methodologies for adaptive sliding mode control","Plestan",2010),
("Utkin Poznyak 2013","Adaptive sliding mode control with application to super-twist algorithm: Equivalent control method","Utkin",2013),
("Utkin 2013 STA","On convergence time and disturbance rejection of super-twisting control","Utkin",2013),
("Furuta 1990","Sliding mode control of a discrete system","Furuta",1990),
("Burton Zinober 1986","Continuous approximation of variable structure control","Burton",1986),
("Spurgeon 2014","Sliding mode control: a tutorial","Spurgeon",2014),
("Yu Yu Wang Xu 2021","Terminal sliding mode control - an overview","Yu",2021),
("Boiko Fridman 2005","Analysis of chattering in systems with second-order sliding modes","Boiko",2005),
("Shtessel Fridman Plestan 2016","Higher order sliding modes: Backgrounds and some recent contributions","Shtessel",2016),
("Utkin 2016","Discussion aspects of high-order sliding mode control","Utkin",2016),
("Edwards Spurgeon 1998 libro","Sliding Mode Control: Theory and Applications","Edwards",1998),
("Utkin 1992 libro","Sliding Modes in Control and Optimization","Utkin",1992),
("Utkin Guldner Shi 1999 libro","Sliding Mode Control in Electromechanical Systems","Utkin",1999),
("Shtessel et al 2014 libro","Sliding Mode Control and Observation","Shtessel",2014),
("Perruquetti Barbot 2002 libro","Sliding Mode Control in Engineering","Perruquetti",2002),
("Slotine Li 1991 libro","Applied Nonlinear Control","Slotine",1991),
("Filippov 1988 libro","Differential Equations with Discontinuous Righthand Sides","Filippov",1988),
("Emelyanov 1967","Variable structure control systems","Emelyanov",1967),
("Itkis 1976","Control systems of variable structure","Itkis",1976),
("Fridman Moreno Iriarte 2011 libro","Sliding Modes after the First Decade of the 21st Century","Fridman",2011),
]
def q(title,au):
    u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':title+' '+au,'rows':5,'select':'DOI,title,author,issued,container-title,is-referenced-by-count,type'})
    return json.load(urllib.request.urlopen(u,timeout=30))['message']['items']
rows=[]
for lab,t,au,y in canon:
    best=None;bs=0
    try:
        for it in q(t,au):
            tt=(it.get('title') or [''])[0]; s=difflib.SequenceMatcher(None,re.sub(r'\W+',' ',t.lower()),re.sub(r'\W+',' ',tt.lower())).ratio()
            fams=' '.join(a.get('family','') for a in it.get('author',[]) or []).lower()
            yr=(it.get('issued',{}).get('date-parts') or [[0]])[0][0]
            sc=s+(0.15 if au.lower() in fams else 0)-(0.1 if abs((yr or 0)-y)>2 else 0)
            if sc>bs: bs=sc;best=(it,tt,yr,s)
    except Exception as e: best=None
    time.sleep(0.3)
    if best and bs>=0.9:
        it,tt,yr,s=best; rows.append(dict(etiqueta=lab,estado='VERIFICADO (Crossref)',doi=it['DOI'],titulo=tt,anio=yr,revista=(it.get('container-title') or [''])[0],tipo=it.get('type'),citas_crossref=it.get('is-referenced-by-count'),similitud=round(s,2)))
    else:
        rows.append(dict(etiqueta=lab,estado='NO ENCONTRADO — verificar a mano (libro/preDOI)',doi='',titulo=t,anio=y,revista='',tipo='',citas_crossref='',similitud=round(best[3],2) if best else ''))
w=csv.DictWriter(open('./work/CANON_FUNDACIONAL.csv','w',newline='',encoding='utf-8'),fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r['estado'][:10],'|',r['etiqueta'],'|',r['doi'],'|',r['citas_crossref'],'|',r['revista'][:35])
print(sum(r['estado'].startswith('VERIF') for r in rows),'/',len(rows))
