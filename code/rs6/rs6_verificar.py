#!/usr/bin/env python3
"""RS6 checks: numbers introduced or corrected in the claim-by-claim audit, recomputed from the RS2-RS4 data.
Run from any folder; locates the Paper_R2 root by relative path. Exit 1 on discrepancy."""
import csv, glob, json, os, re, subprocess, sys
from math import sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
D = lambda p: glob.glob(os.path.join(ROOT, p))[0]
D9, D8, D7, D6 = D("09*"), D("08*"), D("07*"), D("06*")
csv.field_size_limit(10**9)
tex = open(os.path.join(D9, "Manuscript_src.tex"), encoding="utf-8").read()
A = json.load(open(os.path.join(D8, "analisis_rs4.json"), encoding="utf-8"))
T = json.load(open(os.path.join(D8, "temas_emergentes_por_periodo.json"), encoding="utf-8"))
CAL = json.load(open(os.path.join(D6, "analisis", "calibracion_experimental.json"), encoding="utf-8"))
AUD = json.load(open(os.path.join(D7, "auditoria_metricas.json"), encoding="utf-8"))
bad = []

def need(s, why=""):
    if s not in tex:
        bad.append(f"missing in text: {s!r} {why}")

def absent(s, why=""):
    if s in tex:
        bad.append(f"should not appear: {s!r} {why}")

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d

# mapping corpus (same filter as RS4: 2016+ and not the expert canon)
M = [r for r in csv.DictReader(open(os.path.join(D7, "CORPUS_MAPEO_RS3.csv"), encoding="utf-8-sig"))
     if r["estrato"] != "E-F" and int(r["anio"] or 0) >= 2016]
assert len(M) == A["n"] == 5931, len(M)
ex = lambda r: ("experimento" in r["validacion"] or "HIL" in r["validacion"])
FT = "Tiempo finito/fijo/predefinido"

# 1. Guarantee-validation gap within platforms: works with vs without a time guarantee
diffs = {}
for p in sorted({r["plat_rs3"] for r in M}):
    P = [r for r in M if r["plat_rs3"] == p]
    a = [r for r in P if FT in r["variante_auto"]]; b = [r for r in P if FT not in r["variante_auto"]]
    pa, pb = 100 * sum(map(ex, a)) / len(a), 100 * sum(map(ex, b)) / len(b)
    diffs[p] = (round(pa), round(pb), len(a))
print("FT vs no FT by platform:", diffs)
assert all(v[0] < v[1] for v in diffs.values()), "gap not lower in every platform"
gaps = [v[1] - v[0] for v in diffs.values()]
assert (min(gaps), max(gaps)) == (1, 17), (min(gaps), max(gaps))
assert diffs["Manipulador"][:2] == (34, 43) and diffs["Submarino/marino"][:2] == (19, 31)
assert diffs["Blando/continuo/pinza"][2] == 6
need("by 1 to 17 percentage points"); need("34\\% versus 43\\% for manipulators and 19\\% versus 31\\% for marine robots")
need("only six works with a guarantee")

# 2. Calibration of the experimental indicator
assert round(CAL["VPP"], 2) == 0.87 and [round(x, 2) for x in CAL["VPP_IC95"]] == [0.62, 0.96]
assert len([m for m in CAL["muestra"] if m["estrato"] == "sí"]) == 15 and len(CAL["muestra"]) == 30
need("calibrated against 30 full texts read by the author (15 coded positive and 15 coded negative)")
need("0.87 (95\\% CI 0.62--0.96)")
obs = 100 * sum(map(ex, M)) / len(M)
print("observed exp %", round(obs, 1), "calibrated", round(obs * CAL["VPP"], 1))
assert round(obs) == 38 and round(obs * CAL["VPP"]) == 33
need("observed in 38\\% of works (about 33\\% after calibration)")
assert round(100 / CAL["VPP"] - 100) == 15

# 3. Platform precision audit: 40/40
lo, hi = wilson(40, 40); assert AUD["precision_principal"] == [100.0, 91.2, 100] and round(100 * lo) == 91
need("all 40 included works coded at that level (100\\%; 95\\% CI 91--100\\%)")

# 4. Emerging topics and labels (event-triggered, HIL)
assert T["disparo por eventos"][0] == 0.4 and T["disparo por eventos"][-1] == 6.3
assert A["cuota"]["Disparo por eventos/discreto"] == [3.5, 8.3]
need("event-triggered/discrete label grew from 3.5\\% to 8.3\\%"); need("0.4\\% to 6.3\\% as a topic")
assert T["HIL"][0] == 0.4 and T["HIL"][-1] == 2.3
need("0.4\\% (2016--2018) to 2.5\\% (2025--2026) of the works")  # E8-c: value of the coded HIL field in Table S4 (verified in 11/scripts/e8c_verificar.py)

# 5. Decision matrix: share 2024-26, declared guarantee, experimental validation
FAM = {"Integral (ISM)": ("13", "33", "35"), "Terminal (TSM/NTSM/FTSM)": ("27", "65", "36"), "STA/HOSM": ("16", "39", "43"),
       FT: ("39", "100", "31"), "Adaptativo": ("49", "34", "37"), "Basado en observador": ("39", "44", "40"),
       "Inteligente (neuronal/difuso/aprendizaje)": ("30", "27", "34"), "Fraccionario": ("7", "45", "30")}
for f, (sh, de, xp) in FAM.items():
    g = A["garantia_por_variante"][f]; decl = g["tiempo finito"] + g["tiempo fijo"] + g["prescrita/predefinida"]
    got = (f"{A['cuota'][f][1]:.0f}", f"{decl:.0f}", f"{A['exp_var'][f]:.0f}")
    if got != (sh, de, xp): bad.append(f"matrix {f}: data {got} vs text {(sh, de, xp)}")
need("Finite/fixed/ predefined time & Nominal and bound")
need("(47\\% and 43\\%)")

# 6. Layer frequencies and multi-label counts
lay = lambda v: round(100 * sum(v in r["variante_auto"] for r in M) / len(M))
assert lay("Adaptativo") == 45 and lay("Basado en observador") == 35
nv = A["n_variantes_por_trabajo"]; ge2 = sum(v for k, v in nv.items() if int(k) >= 2); ge3 = sum(v for k, v in nv.items() if int(k) >= 3)
assert round(100 * ge2 / A["n"]) == 72 and round(100 * ge3 / A["n"]) == 46
need("72\\% of the 5931 works carry two or more variant labels and 46\\% carry three or more")

# 7. Manipulator DOF statement: DOF unreported in most experimental abstracts -> "where the abstract reports it"
man = [r for r in M if r["plat_rs3"] == "Manipulador" and ex(r)]
unrep = sum(r["gdl"].startswith("no indicado") for r in man) / len(man)
print("manipulator exp works without DOF in abstract:", round(100 * unrep))
need("where the abstract reports it, the arms have 2 to 7 DOF")

# 8. Wording removed in RS6
for s in ("checked in the audit stage", "supports all citations", "Fixed/predefined time designs",
          "in the 2010s, fixed-time stability \\cite{BHAT00", "to predefined time \\cite{R2-00070",
          "well studied in theory \\cite{R2-00019,R2-07268}", "gave way to"):
    absent(s)
need("predefined time \\cite{SANCHEZ18}")

# 9. Timeline figure date matches the cited Emel'yanov source (1967)
txt = subprocess.run(["pdftotext", os.path.join(D9, "figures", "F1_timeline.pdf"), "-"], capture_output=True, text=True).stdout
if "1957" in txt or "1967" not in txt:
    bad.append("F1 timeline: Emel'yanov entry should read 1967")

# 9b. Language and document-type sensitivity (RS2)
S = json.load(open(os.path.join(D6, "analisis", "sensibilidad_idioma_tipo.json"), encoding="utf-8"))
ne, pc = S["no_ingles"], S["ponencias_capitulos"]
assert (ne["registros"], ne["elegibles_aprox"], pc["registros"], pc["elegibles_aprox"]) == (767, 558, 5075, 3696)
assert round(100 * ne["idiomas"]["Chinese"] / ne["registros"]) == 92
vs = [ne["plataforma"]["cramer_V"], ne["variante"]["cramer_V"], pc["plataforma"]["cramer_V"], pc["variante"]["cramer_V"]]
assert (round(min(vs), 2), round(max(vs), 2)) == (0.05, 0.14), vs
dv = lambda t, k: round(t["tabla"][k][1] - t["tabla"][k][0])
assert dv(pc["variante"], "Convencional/primer orden") == 8 and dv(ne["plataforma"], "Espacial") == 7 and dv(ne["plataforma"], "Manipulador") == -9
need("767 non-English articles (92\\% in Chinese; about 558 potentially eligible)"); need("5075 English conference papers and book chapters (about 3696")
need("$V$ = 0.05--0.14")

# 10. Every cited key has a bibliography entry
keys = json.load(open(os.path.join(D9, "cited_keys.json")))
mt = open(os.path.join(D9, "Manuscript.tex"), encoding="utf-8").read()
miss = [k for k in keys if "\\bibitem{" + k + "}" not in mt]
if miss: bad.append(f"no bibitem for {miss}")
print("references:", len(keys))

print("\n".join(bad) if bad else "ALL RS6 CHECKS PASSED"); sys.exit(1 if bad else 0)
