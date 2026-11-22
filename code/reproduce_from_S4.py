#!/usr/bin/env python3
"""Regenerates the corpus statistics reported in the article from Table S4 alone (released data).

Usage:  python reproduce_from_S4.py Table_S4.csv [Manuscript.tex]
With the manuscript, every printed value is also searched for in the text and the script fails on a mismatch.

Indicators that come from keyword searches of abstracts (Figure 6, the 1.8% discretization indicator, the 45 chattering
measures, the computational-cost, overestimation and noise mentions) need the abstracts, which cannot be redistributed;
the records can be retrieved with the identifiers and DOIs of Table S4.
Dependencies: numpy, pandas (logistic regression implemented by iteratively reweighted least squares)."""
import sys, re, numpy as np, pandas as pd

d = pd.read_csv(sys.argv[1]); tex = open(sys.argv[2], encoding="utf-8").read() if len(sys.argv) > 2 else None
m = d[d["set"] != "historical canon (pre-2016)"].copy()
m["yr"] = m.year.clip(upper=2026)                     # 16 early-access records dated 2027 are counted in 2026
L = m.variant_labels.fillna("").str.split("; ")
has = lambda lab: L.apply(lambda x: lab in x).values
FT, CONV = has("Finite/fixed/predefined time"), has("Conventional/first order")
EXP = m.validation.fillna("").str.contains("experiment|HIL").values
HIL = m.validation.fillna("").str.contains("HIL").values
yr = m.yr.values; n = len(m); fails = []

def wilson(k, N, z=1.959964):
    p = k / N; c = (p + z*z/(2*N)) / (1 + z*z/N); h = z*np.sqrt(p*(1-p)/N + z*z/(4*N*N)) / (1 + z*z/N)
    return 100*p, 100*(c-h), 100*(c+h)
def logit(X, y):
    b = np.zeros(X.shape[1])
    for _ in range(60):
        p = 1/(1+np.exp(-X@b)); H = X.T@(X*(p*(1-p))[:, None]); s = np.linalg.solve(H, X.T@(y-p)); b += s
        if np.abs(s).max() < 1e-10: break
    return b, np.sqrt(np.diag(np.linalg.inv(H)))
plats = [p for p in sorted(m.platform.unique()) if p != "Manipulator"]
P = np.column_stack([(m.platform == p).values.astype(float) for p in plats])
base = np.column_stack([np.ones(n), P, yr - 2021.0])
def OR(g, extra=None, mask=None):
    X = np.column_stack([g.astype(float)] + ([extra] if extra is not None else []) + [base])
    y = EXP.astype(float)
    if mask is not None: X, y = X[mask], y[mask]
    b, se = logit(X, y); return np.exp(b[0]), np.exp(b[0]-1.96*se[0]), np.exp(b[0]+1.96*se[0])
def show(name, value, needle=None):
    print(f"{name:62s} {value}")
    if tex is not None and needle is not None and needle not in tex:
        fails.append(f"{name}: '{needle}' not found in the manuscript")

pct = lambda x: f"{x:.0f}"
show("Mapping corpus size", n, "5931")
show("Works in 2016 / 2026 (incl. 16 early access 2027)", (int((yr==2016).sum()), int((yr==2026).sum())), "from 157 works in 2016 to 1007 in 2026")
P1, P2 = (yr >= 2016) & (yr <= 2018), yr >= 2024
show("Time-guarantee share 2016-18 / 2024-26 (%)", (round(100*FT[P1].mean(), 1), round(100*FT[P2].mean(), 1)), "Finite/fixed/predefined time & 18.9 & 38.7")
nl = L.apply(len).values
show("Works with >=2 / >=3 variant labels (%)", (pct(100*(nl>=2).mean()), pct(100*(nl>=3).mean())), "72\\% of the 5931 works carry two or more variant labels and 46\\%")
e, lo, hi = wilson(EXP.sum(), n); show("Experimental or HIL validation (%)", f"{e:.1f} ({lo:.1f}-{hi:.1f})", "observed in 38\\% of works")
e, lo, hi = wilson(EXP[FT].sum(), FT.sum()); show("  time-guarantee works (%)", f"{e:.1f} ({lo:.1f}-{hi:.1f})", "31\\% of cases (95\\% CI 29--33\\%)")
show("  remaining works (%)", f"{100*EXP[~FT].mean():.1f}", "compared with 41\\% for the remaining works")
e, lo, hi = wilson(EXP[CONV].sum(), CONV.sum()); show("  conventional first-order (%)", f"{e:.1f} ({lo:.0f}-{hi:.0f})", "47\\% for conventional first-order SMC")
o = OR(FT); show("Adjusted OR, time guarantee (platform + year)", "%.2f (%.2f-%.2f)" % o, "0.68 (0.60--0.76)")
expl = m.convergence_stated.isin(["finite time", "fixed time", "prescribed/predefined"]).values
show("  same, explicit claims only", "%.2f (%.2f-%.2f)" % OR(expl), "gives 0.68 when the group is defined by explicit claims only")
fx = m.convergence_stated.isin(["fixed time", "prescribed/predefined"]).values
show("  same, fixed or predefined only", "%.2f (%.2f-%.2f)" % OR(fx), "0.64 (0.53--0.77)")
strict = ((m.platform_level == "main") & m.title.str.contains(r"sliding|super[\s-]*twisting|\bSMC\b|variable structure", case=False, regex=True)).values
show("Strict core size", int(strict.sum()), "3590 works")
show("  adjusted OR in the strict core", "%.2f (%.2f-%.2f)" % OR(FT, mask=strict), "OR 0.79, 95\\% CI 0.68--0.92")
diffs = {p: round(100*(EXP[(m.platform==p).values & ~FT].mean() - EXP[(m.platform==p).values & FT].mean())) for p in m.platform.unique()}
show("Validation gap within platforms (pp, min-max)", (min(diffs.values()), max(diffs.values())), "by 1 to 17 percentage points")
for lab, needle in [("Manipulator", "1681 manipulator works"), ("Aerial", "1485 aerial"), ("Underwater/marine", "1105 marine"), ("Space", "129 space")]:
    show(f"Platform count: {lab}", int((m.platform == lab).sum()), needle)
show("Tracking / formation / force (%)", (pct(100*(m.control_task=="tracking").mean()), pct(100*(m.control_task=="formation").mean()), round(100*(m.control_task=="force/contact").mean(), 1)), "Tracking is the declared control task in 67\\% of works, formation in 11\\%, force or contact in 4.5\\%")
show("Abstracts without chattering mention (%)", pct(100*(m.chattering_treatment=="not reported in abstract").mean()), "Fifty-four percent")
ct = m.chattering_treatment.fillna("")
show("Chattering techniques (HOSM, observer, adaptive, boundary layer)", tuple(int(ct.str.contains(k).sum()) for k in ["higher order", "observer compensation", "adaptive gain", "boundary layer"]), "higher-order sliding modes (922 works), observer compensation (660), adaptive gain (544), and boundary layer (362)")
show("Works mentioning code", int((m.code_availability == "yes (mentioned)").sum()), "Ten of the 5931")
show("HIL 2016-18 / 2025-26 (%)", (round(100*HIL[P1].mean(), 1), round(100*HIL[(yr >= 2025)].mean(), 1)), "0.4\\% (2016--2018) to 2.5\\% (2025--2026) of the works")
A, B = has("Terminal (TSM/NTSM/FTSM)"), FT
show("Lift terminal x time guarantee", (int((A & B).sum()), round((A & B).sum()*n/(A.sum()*B.sum()), 2)), "966 works; lift 2.00")
keep = ~(m.document_type.fillna("").str.contains("Retract") | (m.validation == "no abstract")).values
show("Records without abstract / retracted", (int((m.validation == "no abstract").sum()), int(m.document_type.fillna("").str.contains("Retract").sum())), "retains 27 records from citation chasing")
show("  validation, all / time guarantee / rest without them (%)", (round(100*EXP[keep].mean(), 1), round(100*EXP[keep & FT].mean(), 1), round(100*EXP[keep & ~FT].mean(), 1)))
show("  adjusted OR without them", "%.2f (%.2f-%.2f)" % OR(FT, mask=keep))
if tex is not None:
    print("\n" + ("ALL VALUES FOUND IN THE MANUSCRIPT" if not fails else "MISMATCHES:\n" + "\n".join(fails)))
    sys.exit(1 if fails else 0)
