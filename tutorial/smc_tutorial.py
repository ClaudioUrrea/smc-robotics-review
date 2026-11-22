#!/usr/bin/env python3
"""Illustrative 2-DOF SMC tutorial (RS5). Pure Python (math, random, multiprocessing). Reproduces Table T3 and Fig. F8.
Usage: python3 smc_tutorial.py [--quick]. Deterministic: seeds fixed. NOT new research: didactic comparison only."""
import math, random, json, sys, csv, os
from multiprocessing import Pool
sgn=lambda x:(x>0)-(x<0)
sig=lambda x,p:sgn(x)*abs(x)**p
# --- plant (planar 2R, vertical plane). Nominal parameters; TRUE plant has +20% masses, viscous friction and disturbance
NOM=dict(m1=1.0,m2=1.0,l1=1.0,l2=1.0,lc1=0.5,lc2=0.5,I1=1/12,I2=1/12)
TRU=dict(NOM,m1=1.2,m2=1.2,I1=1.2/12,I2=1.2/12)
G=9.81
def MCg(p,q,qd):
    c2=math.cos(q[1]); s2=math.sin(q[1])
    M11=p['m1']*p['lc1']**2+p['m2']*(p['l1']**2+p['lc2']**2+2*p['l1']*p['lc2']*c2)+p['I1']+p['I2']
    M12=p['m2']*(p['lc2']**2+p['l1']*p['lc2']*c2)+p['I2']; M22=p['m2']*p['lc2']**2+p['I2']
    h=-p['m2']*p['l1']*p['lc2']*s2
    C=[[h*qd[1],h*(qd[0]+qd[1])],[-h*qd[0],0.0]]
    c1=math.cos(q[0]); c12=math.cos(q[0]+q[1])
    g=[(p['m1']*p['lc1']+p['m2']*p['l1'])*G*c1+p['m2']*p['lc2']*G*c12, p['m2']*p['lc2']*G*c12]
    return [[M11,M12],[M12,M22]],C,g
def f_true(t,x,tau):
    q=x[:2]; qd=x[2:]; M,C,g=MCg(TRU,q,qd)
    d=[1.0*math.sin(3*t),0.5*math.cos(2*t)]
    r=[tau[i]+d[i]-0.1*qd[i]-C[i][0]*qd[0]-C[i][1]*qd[1]-g[i] for i in range(2)]
    det=M[0][0]*M[1][1]-M[0][1]**2
    a0=(M[1][1]*r[0]-M[0][1]*r[1])/det; a1=(-M[0][1]*r[0]+M[0][0]*r[1])/det
    return [qd[0],qd[1],a0,a1]
def rk4(t,x,tau,h):
    k1=f_true(t,x,tau); k2=f_true(t+h/2,[x[i]+h/2*k1[i] for i in range(4)],tau)
    k3=f_true(t+h/2,[x[i]+h/2*k2[i] for i in range(4)],tau); k4=f_true(t+h,[x[i]+h*k3[i] for i in range(4)],tau)
    return [x[i]+h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(4)]
def ref(t):
    q=[0.6*math.sin(t)+0.3, 0.5*math.sin(1.5*t)-0.3]; d=[0.6*math.cos(t),0.75*math.cos(1.5*t)]; a=[-0.6*math.sin(t),-1.125*math.sin(1.5*t)]
    return q,d,a
# --- controller parameters (fixed a priori, identical for all scenarios)
P=dict(lam=8.0, bl_K=25.0, bl_phi=0.05, sta_k1=8.0, sta_k2=30.0, nt_beta=3.0, nt_pq=5/3, nt_K=25.0,
       fx_k1=3.0, fx_k2=3.0, fx_a=0.5, fx_b=1.5, fx_c1=8.0, fx_c2=8.0, fx_k3=30.0, eps=1e-3)
def bound_fixed_time(P):
    return 2/P['fx_c1']+2/P['fx_c2']+1/(P['fx_k1']*(1-P['fx_a']))+1/(P['fx_k2']*(P['fx_b']-1))
def run(args):
    ctrl,Ts,noise,seed,T=args
    rnd=random.Random(1000*seed+7); h=Ts/4; nsub=4; N=int(T/Ts)
    q0,d0,_=ref(0.0); x=[q0[0]+0.2,q0[1]-0.2,d0[0],d0[1]]; z=[0.0,0.0]; t=0.0
    sq,sv=(1e-3,1e-2) if noise else (0.0,0.0)
    E=[];TAU=[];TS=[]
    for k in range(N):
        qm=[x[0]+rnd.gauss(0,sq),x[1]+rnd.gauss(0,sq)]; vm=[x[2]+rnd.gauss(0,sv),x[3]+rnd.gauss(0,sv)]
        qr,dr,ar=ref(t); e=[qm[i]-qr[i] for i in range(2)]; ed=[vm[i]-dr[i] for i in range(2)]
        v=[0.0,0.0]
        for i in range(2):
            if ctrl=='BL':
                s=ed[i]+P['lam']*e[i]; w=-P['bl_K']*max(-1,min(1,s/P['bl_phi'])); v[i]=ar[i]-P['lam']*ed[i]+w
            elif ctrl=='STA':
                s=ed[i]+P['lam']*e[i]; z[i]+=-P['sta_k2']*sgn(s)*Ts; v[i]=ar[i]-P['lam']*ed[i]-P['sta_k1']*sig(s,0.5)+z[i]
            elif ctrl=='NTSM':
                pq=P['nt_pq']; s=e[i]+sig(ed[i],pq)/P['nt_beta']
                v[i]=ar[i]-P['nt_beta']/pq*sig(ed[i],2-pq)-P['nt_K']*sgn(s)
            else: # fixed-time
                a_,b_,k1,k2=P['fx_a'],P['fx_b'],P['fx_k1'],P['fx_k2']; eps=P['eps']
                s=ed[i]+k1*sig(e[i],a_)+k2*sig(e[i],b_)
                dsd=k1*a_*max(abs(e[i]),eps)**(a_-1)*ed[i]+k2*b_*abs(e[i])**(b_-1)*ed[i]
                z[i]+=-P['fx_k3']*sgn(s)*Ts; v[i]=ar[i]-dsd-P['fx_c1']*sig(s,0.5)-P['fx_c2']*sig(s,1.5)+z[i]
        M,C,g=MCg(NOM,qm,vm)
        tau=[M[i][0]*v[0]+M[i][1]*v[1]+C[i][0]*vm[0]+C[i][1]*vm[1]+g[i] for i in range(2)]
        tau=[max(-60,min(60,u)) for u in tau]
        for _ in range(nsub): x=rk4(t,x,tau,h); t+=h
        if any(abs(c)>1e3 for c in x): return dict(ctrl=ctrl,Ts=Ts,noise=noise,seed=seed,diverged=True)
        qt,_,_=ref(t); E.append((x[0]-qt[0],x[1]-qt[1])); TAU.append(tau); TS.append(t)
    i0=int(2.0/Ts); n=len(E)
    rmse=math.sqrt(sum(a*a+b*b for a,b in E[i0:])/(n-i0)/2)
    # settling: last time |e|>0.01 rad (either joint), after start
    last=0.0
    for k,(a,b) in enumerate(E):
        if max(abs(a),abs(b))>0.01: last=TS[k]
    tv=sum(abs(TAU[k][j]-TAU[k-1][j]) for k in range(i0+1,n) for j in range(2))/(2*(T-2.0))
    w=max(1,int(0.02/Ts)); hf=0.0
    for k in range(i0+w,n):
        for j in range(2):
            ma=sum(TAU[m][j] for m in range(k-w,k))/w; hf+=(TAU[k][j]-ma)**2
    hf=math.sqrt(hf/((n-i0-w)*2))
    return dict(ctrl=ctrl,Ts=Ts,noise=noise,seed=seed,diverged=False,rmse=rmse,settle=last,tv=tv,hf=hf)
if __name__=="__main__":
    quick='--quick' in sys.argv; T=2.5 if quick else 5.0; seeds=3 if quick else 8
    jobs=[]
    for c in ['BL','STA','NTSM','FXT']:
        for Ts in (0.001,0.002,0.005):
            jobs.append((c,Ts,False,0,T))
            for s in range(1,seeds+1): jobs.append((c,Ts,True,s,T))
    with Pool(max(1,os.cpu_count() or 1)) as pool: res=pool.map(run,jobs)
    out=os.path.dirname(os.path.abspath(__file__)); json.dump(dict(P=P,fxt_bound=bound_fixed_time(P),T=T,results=res),open(os.path.join(out,"tutorial_raw.json"),"w"),indent=1)
    print("done",len(res),"diverged",sum(r['diverged'] for r in res),"fxt bound",round(bound_fixed_time(P),3))
