# RS5 figures F1-F7 + PRISMA, generated from RS4/RS3 data. Run: python3 rs5_figuras.py
import json, csv, os, glob
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from estilo_figuras import aplicar
FONT=aplicar(10.5)
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
D8=glob.glob(os.path.join(ROOT,"08*"))[0]; D7=glob.glob(os.path.join(ROOT,"07*"))[0]
OUT=os.path.join(os.path.dirname(__file__),"..","figures"); os.makedirs(OUT,exist_ok=True)
A=json.load(open(os.path.join(D8,"analisis_rs4.json"),encoding="utf-8"))
R=json.load(open(os.path.join(D8,"robustez_rs4.json"),encoding="utf-8"))
T=json.load(open(os.path.join(D8,"temas_emergentes_por_periodo.json"),encoding="utf-8"))
EN={"Adaptativo":"Adaptive","Backstepping híbrido":"Backstepping hybrid","Basado en observador":"Observer-based",
"Convencional/primer orden":"Conventional (1st order)","Disparo por eventos/discreto":"Event-triggered/discrete","Fraccionario":"Fractional-order",
"Integral (ISM)":"Integral (ISM)","Inteligente (neuronal/difuso/aprendizaje)":"Intelligent (NN/fuzzy/RL)","MPC híbrido":"MPC hybrid",
"Multiagente/formación":"Multi-agent/formation","Optimización metaheurística":"Metaheuristic tuning","STA/HOSM":"STA/HOSM",
"Terminal (TSM/NTSM/FTSM)":"Terminal (TSM/NTSM/FTSM)","Tiempo finito/fijo/predefinido":"Finite/fixed/predefined time","Tolerante a fallas":"Fault-tolerant"}
ENP={"Manipulador":"Manipulator","Aéreo":"Aerial","Submarino/marino":"Marine/underwater","Móvil terrestre/patas":"Ground/legged",
"Exoesqueleto/rehabilitación/médico":"Exo/medical","Robot genérico (EL/subactuado)":"Generic Euler–Lagrange","Espacial":"Space","Blando/continuo/pinza":"Soft/continuum"}
C={"b":"#1f4e79","o":"#c55a11","g":"#548235","r":"#9e2a2b","k":"#404040","l":"#8faadc"}
def save(fig,name): fig.savefig(os.path.join(OUT,name+".pdf"),bbox_inches="tight"); fig.savefig(os.path.join(OUT,name+".png"),dpi=300,bbox_inches="tight"); plt.close(fig)

# F1 timeline
ev=[(1967,"Variable-structure\nsystems (Emel'yanov)"),(1977,"Utkin: sliding modes\nin control (foundational)"),(1983,"Slotine–Sastry:\nrobot sliding surfaces"),
(1992,"Terminal SMC\nin manipulators"),(1993,"Higher-order SMC\n(Levant)"),(1996,"Integral SM\n(Utkin–Shi)"),(2003,"Super-twisting\noutput feedback"),
(2012,"Fixed-time\nstability (Polyakov)"),(2016,"Mapping corpus\nbegins (n = 5931)"),(2026,"2024–26: 39%\ndeclare finite/\nfixed/predefined\ntime guarantees")]
fig,ax=plt.subplots(figsize=(7.2,2.9)); ax.axhline(0,color=C["k"],lw=1)
HT=[1.25,-0.5,0.5,-1.35,1.2,-0.5,0.5,-1.35,1.95,0.5]
HA={5:"left"}
for i,(y,t) in enumerate(ev):
    h=HT[i]; s=1 if h>0 else -1
    ax.plot([y,y],[0,h],color=C["b"],lw=0.8); ax.plot(y,0,"o",color=C["o"],ms=4)
    ax.text(y+(0.8 if HA.get(i)=="left" else 0),h+0.08*s,(t if t[0].isdigit() else f"{y}\n{t}"),ha=HA.get(i,"center"),va="bottom" if s>0 else "top",fontsize=8.5)
ax.set_ylim(-2.4,2.9); ax.set_xlim(1950,2034); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_xlabel("Year"); save(fig,"F1_timeline")

# F2 yearly output + share by variant
yrs=[str(y) for y in range(2016,2027)]; n=[A["por_anio"][y] for y in yrs]
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.2,2.8),gridspec_kw={"width_ratios":[1,1.25]})
a1.bar(yrs,n,color=C["l"]); a1.set_ylabel("Works per year"); a1.set_xticks(range(len(yrs))); a1.set_xticklabels([y if int(y)%2==0 else "" for y in yrs],rotation=90)
a1.bar(yrs[-1],n[-1],color=C["l"],hatch="///",edgecolor=C["b"]); a1.set_title("(a) Volume (2026 to 11 Nov)",fontsize=10.4)
sel=["Tiempo finito/fijo/predefinido","Basado en observador","Terminal (TSM/NTSM/FTSM)","Adaptativo","Inteligente (neuronal/difuso/aprendizaje)","STA/HOSM","Convencional/primer orden"]
cols=[C["r"],C["o"],C["g"],C["b"],"#7f6000",C["k"],"#7030a0"]
rows=list(csv.reader(open(os.path.join(D8,"serie_anual_variante.csv"),encoding="utf-8-sig")))
tot=np.array(n,float); ser={r[0]:np.array([float(x) for x in r[1:12]]) for r in rows[1:]}
for v,c in zip(sel,cols): a2.plot(range(2016,2027),100*ser[v]/tot,color=c,label=EN[v])
a2.set_ylabel("Share of works (%)"); a2.set_title("(b) Share by variant",fontsize=10.4); a2.legend(fontsize=7.2,frameon=False,loc="center left",bbox_to_anchor=(1.0,0.5))
fig.tight_layout(); save(fig,"F2_trends")

# F3 heatmap variant x platform
rows=list(csv.reader(open(os.path.join(D8,"matriz_variante_plataforma_exp.csv"),encoding="utf-8-sig"))); hdr=rows[0]
plats=[h[:-4] for h in hdr[1:9]]; var=[r[0] for r in rows[1:]]
N=np.array([[float(x) for x in r[1:9]] for r in rows[1:]]); E=np.array([[float(x) for x in r[9:17]] for r in rows[1:]])
fig,ax=plt.subplots(figsize=(7.2,4.6)); M=np.ma.masked_where(N<20,E)
im=ax.imshow(M,cmap="YlGnBu",vmin=0,vmax=100,aspect="auto")
for i in range(N.shape[0]):
    for j in range(N.shape[1]):
        if N[i,j]>=20: ax.text(j,i,f"{E[i,j]:.0f}",ha="center",va="center",fontsize=8.5,color="white" if E[i,j]>60 else "black")
        else: ax.text(j,i,"·",ha="center",va="center",color="#999999")
ax.set_xticks(range(8)); ax.set_xticklabels([f"{ENP[p]}\n(n={int(N[:,k].max())}max)".replace("max)",")") if False else ENP[p] for k,p in enumerate(plats)],rotation=30,ha="right")
ax.set_yticks(range(len(var))); ax.set_yticklabels([EN[v] for v in var]); ax.spines[:].set_visible(False)
cb=fig.colorbar(im,ax=ax,fraction=0.03); cb.set_label("Experimental/HIL validation (% of works, observed)")
fig.tight_layout(); save(fig,"F3_heatmap")

# F4 guarantee by year (stacked, share)
cats=["tiempo finito","tiempo fijo","prescrita/predefinida","asintótica/exponencial","no especificada"]
lab=["Finite time","Fixed time","Predefined/prescribed","Asymptotic/exponential","Not specified"]
colr=[C["r"],C["o"],"#ffc000",C["l"],"#d9d9d9"]
G=np.array([[A["garantia_anio"][y][c] for c in cats] for y in yrs],float); G=100*G/G.sum(1,keepdims=True)
fig,ax=plt.subplots(figsize=(5.2,2.8)); b=np.zeros(len(yrs))
for k in range(5): ax.bar(yrs,G[:,k],bottom=b,color=colr[k],label=lab[k],width=0.8); b+=G[:,k]
ax.set_ylabel("Works (%)"); ax.tick_params(axis="x",rotation=60); ax.legend(fontsize=7.8,frameon=False,loc="center left",bbox_to_anchor=(1,0.5))
save(fig,"F4_guarantees")

# F5 emerging topics
per=["2016–18","2019–21","2022–24","2025–26"]
sel5=["aprendizaje por refuerzo","aprendizaje profundo/datos","desempeño prescrito (PPC)","barrera/restricciones","saturación de entrada","disparo por eventos","implementación discreta/digital"]
l5=["Reinforcement learning","Deep/data-driven","Prescribed performance","Barrier/constraints","Input saturation","Event-triggered","Discrete/digital implementation"]

fig,ax=plt.subplots(figsize=(5.2,2.9))
for k,(s,l) in enumerate(zip(sel5,l5)):
    ax.plot(per,T[s],marker="o",ms=3,label=l,ls="--" if "Discrete" in l else "-",color=["#c00000","#ed7d31","#548235","#1f4e79","#7f6000","#7030a0","#404040"][k])
ax.set_ylabel("Works mentioning topic (%)"); ax.legend(fontsize=7.8,frameon=False,loc="center left",bbox_to_anchor=(1,0.5)); save(fig,"F5_emerging")

# F6 SLIDE schema
fig,ax=plt.subplots(figsize=(7.2,3.6)); ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(0,50)
cols6=[("S","Surface",["Conventional","Integral (ISM)","Terminal\n(TSM/NTSM)","Higher-order/STA"],C["b"]),
("L","Layers",["Observer/\nestimator","Adaptation","Learning\n(NN/RL)","Fractional, hybrid,\nfault-tolerant,\nmulti-agent"],C["o"]),
("I","Implementation",["Continuous time","Discrete/sampled","Implicit","Event-triggered"],C["g"]),
("D","Deadline",["Asymptotic","Finite time","Fixed time","Predefined"],C["r"]),
("E","Embodiment",["Manipulator,\naerial","Marine,\nground","Exo/medical,\nspace","Soft,\ngeneric"],"#7030a0")]
for i,(k,name,items,c) in enumerate(cols6):
    x=1+i*19.6; ax.add_patch(FancyBboxPatch((x,40),18,8,boxstyle="round,pad=0.3",fc=c,ec="none"))
    ax.text(x+9,44,f"{k}\n{name}",ha="center",va="center",color="white",fontsize=8.8,weight="bold",linespacing=1.1)
    for j,it in enumerate(items):
        ax.add_patch(FancyBboxPatch((x,29.5-j*7.2),18,5.6,boxstyle="round,pad=0.2",fc="white",ec=c,lw=0.9))
        ax.text(x+9,32.3-j*7.2,it,ha="center",va="center",fontsize=7.3,linespacing=1.0)
ax.text(50,-1.8,"Typical design: extended-state observer + adaptive NTSM, fixed time, event-triggered, underwater vehicle  →  S: terminal · L: {observer, adaptation} · I: event · D: fixed · E: marine",
        ha="center",fontsize=7.6,style="italic"); save(fig,"F6_SLIDE")

# F7 forest plot
ex=R["exp_multivariable"]; keys=sorted(ex,key=lambda k:ex[k]["OR"])
fig,ax=plt.subplots(figsize=(5.0,3.2))
for i,k in enumerate(keys):
    o=ex[k]["OR"]; lo,hi=ex[k]["IC95"]; sig=(lo>1) or (hi<1)
    ax.plot([lo,hi],[i,i],color=C["r"] if hi<1 else (C["g"] if lo>1 else "#7f7f7f"),lw=1.6); ax.plot(o,i,"s",color=C["k"],ms=3.5)
ax.axvline(1,color="k",lw=0.7,ls="--"); ax.set_yticks(range(len(keys))); ax.set_yticklabels([EN[k] for k in keys])
ax.set_xlabel("Adjusted odds ratio for experimental/HIL validation (95% CI)"); ax.set_xlim(0.4,1.6); save(fig,"F7_forest")

# PRISMA
fl=list(csv.DictReader(open(glob.glob(os.path.join(D7,"TABLA_S2*"))[0],encoding="utf-8-sig"))); g=lambda s:[int(r["n"]) for r in fl if r["paso"].startswith(s)][0]
wos,sco,snow,canon=g("Registros exportados de WoS"),g("Registros exportados de Scopus"),g("Registros de bola"),g("Canon fundacional")
uniq,ex2,keep=g("Registros únicos"),g("Excluidos en título"),g("Conservados"); ev3,ex3,ctx32=g("Corpus de mapeo 2016+"),g("Excluidos en RS3"),g("Reclasificados")
mapc,canonin,ctx,syn=g("Corpus de mapeo 2016–2026"),g("Canon histórico"),g("Registros CONTEXTO"),g("Corpus de síntesis")
extra_wos=662; ident=wos+extra_wos+sco+snow+canon; dup=ident-uniq
fig,ax=plt.subplots(figsize=(7.2,7.4)); ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(0,100)
def box(x,y,w,h,t,fc="#eaf1f8"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.25",fc=fc,ec=C["b"],lw=0.9)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=9.1)
def arr(x1,y1,x2,y2): ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color=C["k"],lw=0.9))
f=lambda v:f"{v:,}"
ax.text(-1,93,"Identification",rotation=90,va="center",fontsize=9.8,weight="bold"); ax.text(-1,58,"Screening",rotation=90,va="center",fontsize=9.8,weight="bold"); ax.text(-1,14,"Included",rotation=90,va="center",fontsize=9.8,weight="bold")
box(3,87,22,11,f"Web of Science\n(n = {f(wos+extra_wos)})"); box(27,87,20,11,f"Scopus\n(n = {f(sco)})"); box(49,87,22,11,f"Citation chasing\n(n = {f(snow)})"); box(73,87,24,11,f"Expert canon\n(n = {canon})")
for x in (14,37,60,85): arr(x,87,x,83.5)
box(3,73,57,9,f"Records identified (n = {f(ident)})"); box(66,73,31,9,f"Duplicates removed\n(n = {f(dup)})","#fbe5d6"); arr(60,77.5,66,77.5); arr(31.5,73,31.5,68.5)
box(3,58,57,9,f"Records screened on title and abstract\n(n = {f(uniq)})"); box(66,58,31,9,f"Records excluded\n(n = {f(ex2)})","#fbe5d6"); arr(60,62.5,66,62.5); arr(31.5,58,31.5,53.5)
box(3,42,57,10.5,f"Records assessed for eligibility\n(n = {f(keep)})"); box(66,39,31,16,f"Excluded at eligibility\n(n = {f(ex3)}): SMC not\nthe main method, no\nrobotic platform, or\nno abstract","#fbe5d6"); arr(60,47,66,47); arr(31.5,42,31.5,37.5)
box(3,22,57,14.5,f"Mapping corpus 2016–2026 (n = {f(mapc)})\nPre-2016 historical canon (n = {canonin})\nContext records, not primary evidence (n = {ctx};\nincludes {ctx32} reclassified at eligibility)"); arr(31.5,22,31.5,17.5)
box(3,4,57,12.5,f"Citable synthesis corpus (n = {syn})\n(curated by variant × platform\ncell, reviews and canon)","#e2efda")
assert ident-dup==uniq and keep-ex3==mapc+canonin+ctx and uniq-ex2==keep
save(fig,"F0_PRISMA")
print("ok",ident,dup,wos,sco,snow,canon,uniq,ex2,keep,ev3,ex3,ctx32,mapc,canonin,ctx,syn)
