import sys,glob,re,json,os
sys.path.insert(0,'./scripts')
from parse import *
canon=[
("Utkin 1977 Variable structure systems with sliding modes (IEEE TAC)",r"variable structure systems with sliding modes"),
("Utkin 1978 Sliding Modes and Their Application in VSS (libro)",r"sliding modes and their application"),
("Utkin 1992 Sliding Modes in Control and Optimization (libro)",r"sliding modes in control and optimization"),
("Utkin, Guldner, Shi 1999 Sliding Mode Control in Electromechanical Systems",r"sliding mode control in electro-?mechanical"),
("Edwards & Spurgeon 1998 Sliding Mode Control: Theory and Applications",r"sliding mode control: theory and applications"),
("Slotine & Sastry 1983 Tracking control ... sliding surfaces ... robot manipulators",r"tracking control of non-?linear systems using sliding surfaces"),
("Slotine 1984 Sliding controller design for non-linear systems",r"sliding controller design for non-?linear"),
("Slotine 1985 The robust control of robot manipulators",r"robust control of robot manipulators"),
("Young 1978 Controller design for a manipulator using VSS theory",r"controller design for a manipulator using theory of variable structure"),
("Young, Utkin, Ozguner 1999 A control engineer's guide to SMC",r"control engineer.s guide to sliding mode"),
("Hung, Gao, Hung 1993 Variable structure control: a survey",r"variable structure control: a survey"),
("DeCarlo, Zak, Matthews 1988 VSC of nonlinear multivariable systems: a tutorial",r"variable structure control of nonlinear multivariable systems: a tutorial"),
("Drakunov & Utkin 1992 Sliding mode control in dynamic systems",r"sliding mode control in dynamic systems"),
("Levant 1993 Sliding order and sliding accuracy",r"sliding order and sliding accuracy"),
("Levant 1998 Robust exact differentiation via sliding mode technique",r"robust exact differentiation via sliding mode"),
("Levant 2003 Higher-order sliding modes, differentiation and output-feedback control",r"higher-order sliding modes, differentiation"),
("Bartolini et al 1998 Chattering avoidance by second-order SMC",r"chattering avoidance by second-order sliding"),
("Man, Paplinski, Wu 1994 Robust MIMO terminal sliding mode ... rigid robotic manipulators",r"robust mimo terminal sliding mode control scheme"),
("Venkataraman & Gulati 1993 Control of nonlinear systems using terminal sliding modes",r"control of nonlinear systems using terminal sliding modes"),
("Feng, Yu, Man 2002 Non-singular terminal SMC of rigid manipulators",r"non-?singular terminal sliding mode control of rigid manipulators"),
("Moreno & Osorio Strict Lyapunov functions for the super-twisting algorithm",r"strict lyapunov functions for the super-twisting"),
("Shtessel et al 2014 Sliding Mode Control and Observation (libro)",r"sliding mode control and observation"),
("Polyakov & Fridman 2014 Stability notions and Lyapunov functions for SM systems",r"stability notions and lyapunov functions for sliding mode"),
("Lee & Utkin 2007 Chattering suppression methods in SMC systems",r"chattering suppression methods in sliding mode"),
("Plestan et al 2010 New methodologies for adaptive SMC",r"new methodologies for adaptive sliding mode"),
("Utkin & Poznyak 2013 Adaptive SMC with application to super-twist algorithm",r"adaptive sliding mode control with application to super-?twist"),
("Utkin 2013 On convergence time and disturbance rejection of super-twisting control",r"convergence time and disturbance rejection of super-twisting"),
("Spurgeon 2014 Sliding mode control: a tutorial",r"sliding mode control ?: a tutorial"),
("Furuta 1990 Sliding mode control of a discrete system",r"sliding mode control of a discrete system"),
("Perruquetti & Barbot 2002 Sliding Mode Control in Engineering (libro)",r"sliding mode control in engineering"),
("Fridman 2011 / Fridman-Moreno-Iriarte Sliding Modes after the first decade / Modes glissants",r"sliding modes after the first decade|sliding mode control and observation"),
("Yu, Yu, Wang, Xu 2021 Terminal Sliding Mode Control - An Overview",r"terminal sliding mode control - an overview"),
("Wang et al 2022? Boiko & Fridman Analysis of chattering",r"analysis of chattering in systems with second-order sliding"),
("Utkin 2016 Discussion aspects of high-order sliding mode control",r"discussion aspects of high-order sliding mode"),
]
txt={}
def add(src,t,y):
    txt.setdefault(norm(t),[]).append((src,y))
for f in glob.glob('./work/respaldos_scopus/*.bib')+glob.glob('./work/respaldos_wos/*.bib')+glob.glob('./work/*.bib')+glob.glob('./work/Downloads/*.bib'):
    if 'integral_cited' in f: continue
    wos='X' in os.path.basename(f)[:1] or 'Q0' in os.path.basename(f) or 'W01' in f
    for r in recs(f):
        t=field(r,'Title' if re.search(r'(?m)^Title',r) else 'title'); y=field(r,'Year' if re.search(r'(?m)^Year',r) else 'year')
        add(os.path.basename(f)[:3],t,y)
found=0;miss=[]
for name,rx in canon:
    hit=[(k,v) for k,v in txt.items() if re.search(rx,k.replace('  ',' '),re.I)]
    if hit: found+=1; print('EN CORPUS ',name,'|',hit[0][0][:60],hit[0][1][0][1])
    else: miss.append(name); print('FALTA     ',name)
print(found,'/',len(canon))
json.dump(miss,open('./work/analisis/canon_faltante.json','w'),ensure_ascii=False)
