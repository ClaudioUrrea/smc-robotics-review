import json,statistics as st,csv,os,math
import matplotlib; matplotlib.use("Agg"); from matplotlib.ticker import NullFormatter; import matplotlib.pyplot as plt
import sys; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","scripts"))
from estilo_figuras import aplicar
aplicar(10.5)
here=os.path.dirname(os.path.abspath(__file__)); D=json.load(open(os.path.join(here,"tutorial_raw.json"))); R=D['results']
names={'BL':'SMC + boundary layer','STA':'Super-twisting','NTSM':'NTSM','FXT':'Fixed-time STA'}
rows=[]
def ms(v): return (st.mean(v), st.stdev(v) if len(v)>1 else 0.0)
for c in names:
  for Ts in (0.001,0.002,0.005):
    for nz in (False,True):
      r=[x for x in R if x['ctrl']==c and x['Ts']==Ts and x['noise']==nz]
      rows.append(dict(controller=names[c],Ts_ms=Ts*1e3,noise='yes' if nz else 'no',n=len(r),
        **{k+"_mean":ms([x[k] for x in r])[0] for k in ('rmse','settle','tv','hf')},**{k+"_sd":ms([x[k] for x in r])[1] for k in ('rmse','settle','tv','hf')}))
with open(os.path.join(here,"TABLA_T3_tutorial.csv"),"w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
cols={'SMC + boundary layer':'#1f4e79','Super-twisting':'#548235','NTSM':'#c55a11','Fixed-time STA':'#9e2a2b'}
fig,ax=plt.subplots(1,3,figsize=(7.2,2.9))
for k,(key,lab,log) in enumerate([("rmse","Tracking RMSE (rad)",True),("tv","Torque total variation (N·m/s)",True),("hf","Torque HF RMS (N·m)",True)]):
  for nm,c in cols.items():
    for nz,ls in (("no","-"),("yes","--")):
      y=[r[key+"_mean"] for r in rows if r['controller']==nm and r['noise']==nz]
      ax[k].plot([1,2,5],y,ls=ls,marker="o",ms=3,color=c,label=nm if (k==0 and nz=="no") else None)
  ax[k].set_xscale("log"); ax[k].xaxis.set_minor_formatter(NullFormatter()); ax[k].set_yscale("log"); ax[k].set_xticks([1,2,5]); ax[k].set_xticklabels(["1","2","5"]); ax[k].set_xlabel("Sampling period $T_s$ (ms)"); ax[k].set_ylabel(lab,fontsize=9.1)
from matplotlib.lines import Line2D
h=[Line2D([],[],color=c,lw=1.4,marker="o",ms=3) for c in cols.values()]+[Line2D([],[],color="k",ls="-"),Line2D([],[],color="k",ls="--")]
fig.legend(h,list(cols)+["no noise","with noise"],ncol=6,fontsize=7.8,frameon=False,loc="lower center",bbox_to_anchor=(0.5,-0.06))
fig.tight_layout(); fig.savefig(os.path.join(here,"..","figures","F8_tutorial.pdf"),bbox_inches="tight"); fig.savefig(os.path.join(here,"..","figures","F8_tutorial.png"),dpi=300,bbox_inches="tight")
# trajectory figure for 1 case (clean, 2 ms)
import importlib.util,sys
spec=importlib.util.spec_from_file_location("t",os.path.join(here,"smc_tutorial.py")); t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
for r in rows: print(r['controller'],r['Ts_ms'],r['noise'],f"{r['rmse_mean']:.2e}±{r['rmse_sd']:.1e} st={r['settle_mean']:.2f} tv={r['tv_mean']:.0f} hf={r['hf_mean']:.2f}")
