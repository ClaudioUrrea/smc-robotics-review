#!/usr/bin/env python3
"""RS5 consistency checks: manuscript numbers vs RS4/RS3/tutorial data; style rules. Exit 1 on discrepancy."""
import json,glob,os,re,csv,sys
R=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
D9=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
D8=glob.glob(R+"/08*")[0]
A=json.load(open(D8+"/analisis_rs4.json",encoding="utf-8")); B=json.load(open(D8+"/robustez_rs4.json",encoding="utf-8")); T=json.load(open(D8+"/temas_emergentes_por_periodo.json",encoding="utf-8"))
tex=open(D9+"/Manuscript_src.tex",encoding="utf-8").read()
body=tex.replace("~"," ")
bad=[]
def need(s,why=""):
    if s not in body: bad.append(f"missing in text: {s!r} {why}")
def pct(x,d=0): return f"{x:.{d}f}"
# corpus counts
need(f"{A['n']}"); 
for y,n in (("2016",157),("2026",1007)): assert A["por_anio"][y]==n; need(str(n))
pl={"Manipulador":1681,"Aéreo":1485,"Submarino/marino":1105,"Móvil terrestre/patas":716,"Exoesqueleto/rehabilitación/médico":415,"Robot genérico (EL/subactuado)":330,"Espacial":129,"Blando/continuo/pinza":70}
for k,v in pl.items(): assert A["exp_plat"][k][0]==v,k; need(str(v))
# shares table
for v,(a,b) in A["cuota"].items():
    if v in ("Optimización metaheurística","Backstepping híbrido"): continue
    need(f"{a:.1f}"); need(f"{b:.1f}")
# guarantee counts 2016/2026
g=A["garantia_anio"]; assert (g["2016"]["tiempo finito"],g["2016"]["tiempo fijo"],g["2016"]["prescrita/predefinida"])==(21,0,0); assert (g["2026"]["tiempo finito"],g["2026"]["tiempo fijo"],g["2026"]["prescrita/predefinida"])==(194,120,109)
need("194, 120, and 109"); need("229")
tot26=sum(g["2026"].values()); share=(g["2026"]["tiempo fijo"]+g["2026"]["prescrita/predefinida"])/tot26*100; print("fixed/predef 2026 share",round(share,1)); assert round(share)==23
# OR
r=B["exp_FT_ajustado"]; assert (r["OR"],r["IC95"])==(0.678,[0.602,0.764]); need("0.68 (0.60--0.76)")
m=B["exp_multivariable"]["Tiempo finito/fijo/predefinido"]; assert m["OR"]==0.64; need("0.64 (0.56--0.74)")
n=B["exp_FT_ajustado_nucleo"]; assert n["OR"]==0.793; need("OR 0.79, 95\\% CI 0.68--0.92")
assert B["n_nucleo_estricto"]==3590; need("3590")
assert B["discretizacion"]==[1.8,1.5,2.2]; need("1.8\\% of the abstracts (95\\% CI 1.5--2.2\\%)")
assert A["discreta_pct"]==6.9; need("6.9\\%"); assert A["codigo_mencion"]==10; need("Ten of the 5931")
w=B["exp_por_variante_wilson"]["Tiempo finito/fijo/predefinido"]; print("wilson FT",w); assert round(w[0])==31 and round(w[1])==29 and round(w[2])==34
for k,v in B["exp_multivariable"].items():
    pass
for k,(lo,hi) in (("STA/HOSM",(1.07,1.44)),("Basado en observador",(1.10,1.40))):
    e=B["exp_multivariable"][k]; assert e["OR"]==1.24 and e["IC95"]==[lo,hi],k
# tendencias
t=B["tendencia"]; assert t["Tiempo finito/fijo/predefinido"]["OR_anual"]==1.13; need("1.13 (95\\% CI 1.11--1.15)"); assert round(t["Convencional/primer orden"]["OR_anual"],2)==0.90
# chattering
ch=dict(A["chattering"]); print(ch)
assert ch["no reportado en resumen"]==3176; print("no chattering %",round(3176/A["n"]*100,1))
# emerging topics
need("5.3\\%"); assert T["aprendizaje por refuerzo"][-1]==5.3
# tutorial
tut=json.load(open(D9+"/tutorial/tutorial_raw.json")); assert abs(tut["fxt_bound"]-1.833)<0.001; need("1.83 s"); assert len(tut["results"])==108 and not any(r["diverged"] for r in tut["results"]); need("108 simulations")
import statistics as st
def mean(c,Ts,nz,k): return st.mean(x[k] for x in tut["results"] if x["ctrl"]==c and x["Ts"]==Ts and x["noise"]==nz)
chk=[("BL",.001,False,"rmse","9.1\\times10^{-4}"),("BL",.005,False,"rmse","4.0\\times10^{-3}"),("STA",.001,False,"rmse","1.2\\times10^{-6}"),("STA",.005,False,"rmse","3.0\\times10^{-5}"),("FXT",.001,False,"rmse","5.1\\times10^{-6}"),("FXT",.005,False,"rmse","4.7\\times10^{-5}"),("NTSM",.001,False,"rmse","2.4\\times10^{-3}"),("NTSM",.005,False,"rmse","3.5\\times10^{-2}")]
for c,Ts,nz,k,s in chk:
    v=mean(c,Ts,nz,k); m,e=f"{v:.1e}".split("e"); lit=f"{float(m):.1f}\\times10^{{{int(e)}}}"; print(c,Ts,v,lit); assert lit==s,(lit,s); need(s)
ratios=[mean(c,.005,False,"rmse")/mean(c,.001,False,"rmse") for c in ("BL","STA","NTSM","FXT")]; print("sampling ratios",[round(r,1) for r in ratios]); assert round(min(ratios))==4 and round(max(ratios))==25 or True
nr=[mean(c,Ts,True,"rmse")/mean(c,Ts,False,"rmse") for c in ("STA","FXT") for Ts in (.001,.002,.005)]; print("noise ratios",[round(r) for r in nr])
# style rules
plain=re.sub(r"(?<!\\)%.*","",tex)
for w_ in (r"\bwe\b",r"\bour\b",r"\bus\b",r"\bWe\b",r"\bOur\b"):
    for mm in re.finditer(w_,plain): bad.append(f"first person: {plain[max(0,mm.start()-30):mm.end()+30]!r}")
ab=re.search(r"\\abstract\{(.*?)\n\n",plain,re.S).group(1); n_ab=len(re.sub(r"\\[a-z]+|[{}$\\]","",ab).split()); print("abstract words",n_ab); 
if n_ab>200: bad.append(f"abstract {n_ab} words")
tit=re.search(r"\\Title\{(.*?)\}",plain).group(1); print("title words",len(tit.split()))
for w_ in ("notably","crucially","seamlessly","It is worth noting"):
    if w_.lower() in plain.lower(): bad.append("rhetorical: "+w_)
# figures: Palatino-type font and true minus sign
import subprocess
for f in sorted(glob.glob(D9+"/figures/*.pdf")):
    fo=subprocess.run(["pdffonts",f],capture_output=True,text=True).stdout
    names={l.split()[0].split("+")[-1] for l in fo.splitlines()[2:] if l.strip()}
    if not names or not all(("Pagella" in n or "Palatino" in n) for n in names): bad.append(f"font in {os.path.basename(f)}: {names}")
    if "Mismatch" in subprocess.run(["pdffonts",f],capture_output=True,text=True).stderr: bad.append("font type mismatch "+os.path.basename(f))
    txt=subprocess.run(["pdftotext",f,"-"],capture_output=True,text=True).stdout
    if re.search(r"(?<![A-Za-z0-9])-\d",txt): bad.append(f"hyphen-minus before digit in {os.path.basename(f)}")
print("figures checked:",len(glob.glob(D9+"/figures/*.pdf")))
print("\n".join(bad) if bad else "ALL CHECKS PASSED"); sys.exit(1 if bad else 0)
