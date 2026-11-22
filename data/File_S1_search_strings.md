# File S1. Search strategies

Paper: *Sliding Mode Control in Robotics: A Fifty-Year Review and Tutorial Since Utkin*.

Databases: Web of Science Core Collection (Advanced Search, field TS = title, abstract, author keywords and Keywords Plus) and Scopus (Advanced document search, field TITLE-ABS-KEY). Exports were made on 10–11 November 2026 in BibTeX with full records and abstracts. Common filters: article or review; 2016–2026 (except the review and canon strings); English (Scopus language filter; WoS records in other languages were removed at eligibility, rule I3).

Export rule: specific strings (variant and platform) were sorted by citations and the top N records exported; generic strings were exported in full. The generic strings are the basis of the mapping corpus; the specific strings and the citation chasing were added to increase recall (estimated recall 96.0%, 95% CI 94.2–97.8%).

## Web of Science

**X01_integral.bib  (N = 30)**

```
TS=("integral sliding mode*" OR "integral sliding-mode*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X02_terminal.bib  (N = 30)**

```
TS=("terminal sliding" OR "nonsingular terminal" OR "fast terminal") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X03_higher_order.bib  (N = 30)**

```
TS=("higher-order sliding" OR "high-order sliding" OR "second-order sliding" OR "super-twisting") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X04_adaptive.bib  (N = 30)**

```
TS=("adaptive sliding mode*" OR "adaptive sliding-mode*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X05_intelligent.bib  (N = 30)**

```
TS=("sliding mode*" OR "sliding-mode*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND TS=(fuzzy OR "neural network*" OR "reinforcement learning") AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X06_fractional.bib  (N = 30)**

```
TS=("fractional-order" OR "fractional order") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND TS=("sliding mode*" OR "sliding-mode*") AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X07_observers.bib  (N = 30)**

```
TS=("sliding mode observer*" OR "sliding-mode observer*" OR "sliding mode differentiator*" OR "robust exact differentiator*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X08_time.bib  (N = 30)**

```
TS=("sliding mode*" OR "sliding-mode*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND TS=("fixed-time" OR "prescribed-time" OR "predefined-time" OR "event-triggered") AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X09_implementation.bib  (N = 30)**

```
TS=("sliding mode*" OR "sliding-mode*") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND TS=(chattering) AND TS=("discrete-time" OR discretization OR discretisation OR "sampled-data" OR implicit) AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X10_manipulators.bib  (N = 30)**

```
TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(manipulator* OR "robot arm*" OR "robotic arm*") AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X11_mobile.bib  (N = 30)**

```
TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=("mobile robot*" OR "wheeled robot*" OR nonholonomic OR "legged robot*") AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X12_aerial.bib  (N = 30)**

```
TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(quadrotor* OR quadcopter* OR multirotor* OR UAV* OR "unmanned aerial") AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X13_underwater.bib  (N = 30)**

```
TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=("underwater vehicle*" OR AUV* OR ROV* OR "underwater robot*") AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X14_exoskeletons.bib  (N = 30)**

```
TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(exoskeleton* OR "rehabilitation robot*" OR "wearable robot*") AND DT=(Article OR Review) AND PY=(2016-2026)
```

**X15_recent.bib  (N = 60)**

```
TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DT=(Article OR Review) AND PY=(2025-2026)
```

**W01 (generic, parallel to SR07 de Scopus) — 11-Nov-2026**

```
TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(robot* OR robotic* OR "mechanical system*" OR "Euler-Lagrange" OR "Euler Lagrange" OR underactuated OR "multi-link" OR "n-link") AND DT=(Article OR Review) AND PY=(2016-2026) AND LA=(English)
```

Results: 5.932; exported los 1.000 most cited (respaldos_wos/W01_generica_top1000.bib). Cribado top 300 junto con SR07 -> CRIBADO_GENERICAS_RS2.csv.

**W12 = W01 ∪ W02 (generic completa, parallel to SR07 ∪ SR08) — 11-Nov-2026**

```
TS=("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TS=(robot* OR robotic* OR "mechanical system*" OR "Euler-Lagrange" OR "Euler Lagrange" OR underactuated OR "multi-link" OR "n-link" OR manipulator* OR quadrotor* OR quadcopter* OR multirotor* OR "multi-rotor" OR UAV OR UAVs OR "unmanned aerial" OR drone* OR VTOL OR helicopter* OR AUV OR AUVs OR ROV OR ROVs OR UUV OR UUVs OR underwater OR "surface vehicle*" OR USV OR USVs OR vessel* OR exoskeleton* OR rehabilitation OR prosthe* OR orthos* OR wheeled OR nonholonomic OR legged OR biped* OR quadruped* OR humanoid* OR gripper* OR continuum) AND DT=(Article OR Review) AND PY=(2016-2026) AND LA=(English)
```

Results: 10.730 (W01 = 5.932; W02 = 4.798, platform-only complement). Exported all, sorted by date, en 11 batches: respaldos_wos/W12_0001-1000.bib … W12_10001-10730.bib (10.730 UT unique records verified).

## Scopus

**S01_integral.bib  (N = 30)**

```
TITLE-ABS-KEY("integral sliding mode*" OR "integral sliding-mode*") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S02_terminal.bib  (N = 30)**

```
TITLE-ABS-KEY("terminal sliding" OR "nonsingular terminal" OR "fast terminal") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S03_higher_order.bib  (N = 30)**

```
TITLE-ABS-KEY("higher-order sliding" OR "high-order sliding" OR "second-order sliding" OR "super-twisting") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S04_adaptive.bib  (N = 30)**

```
TITLE-ABS-KEY("adaptive sliding mode*" OR "adaptive sliding-mode*") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S05_intelligent.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND TITLE-ABS-KEY(fuzzy OR "neural network*" OR "reinforcement learning") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S06_fractional.bib  (N = 30)**

```
TITLE-ABS-KEY("fractional-order" OR "fractional order") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S07_observers.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode observer*" OR "sliding-mode observer*" OR "sliding mode differentiator*" OR "robust exact differentiator*") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S08_time.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND TITLE-ABS-KEY("fixed-time" OR "prescribed-time" OR "predefined-time" OR "event-triggered") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S09_implementation.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND TITLE-ABS-KEY(chattering) AND TITLE-ABS-KEY("discrete-time" OR discretization OR discretisation OR "sampled-data" OR implicit) AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S10_manipulators.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY(manipulator* OR "robot arm*" OR "robotic arm*") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S11_mobile.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY("mobile robot*" OR "wheeled robot*" OR nonholonomic OR "legged robot*") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S12_aerial.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY(quadrotor* OR quadcopter* OR multirotor* OR UAV* OR "unmanned aerial") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S13_underwater.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY("underwater vehicle*" OR AUV* OR ROV* OR "underwater robot*") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S14_exoskeletons.bib  (N = 30)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY(exoskeleton* OR "rehabilitation robot*" OR "wearable robot*") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**S15_recent.bib  (N = 60)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR UAV* OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2024 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**SR05_reviews.bib  (N = all; mirror of Q05)**

```
TITLE-ABS-KEY("sliding mode*" OR "variable structure control*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY(robot* OR manipulator* OR quadrotor* OR multirotor* OR UAV* OR "unmanned aerial" OR "underwater vehicle*" OR AUV* OR exoskeleton*) AND DOCTYPE(re) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**SR07_generica.bib  (N = all = 4839; mejora de recall, 11-Nov-2026)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY(robot* OR robotic* OR "mechanical system*" OR "Euler-Lagrange" OR "Euler Lagrange" OR underactuated OR "multi-link" OR "n-link") AND (DOCTYPE(ar) OR DOCTYPE(re)) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND LANGUAGE(english)
```

**SR08_scopus_completo_3305.bib  (N = all = 3305; complemento de plataforma, 11-Nov-2026)**

```
TITLE-ABS-KEY("sliding mode*" OR "sliding-mode*" OR "super-twisting" OR "terminal sliding") AND TITLE-ABS-KEY(manipulator* OR quadrotor* OR quadcopter* OR multirotor* OR "multi-rotor" OR UAV OR UAVs OR "unmanned aerial" OR drone* OR VTOL OR helicopter* OR AUV OR AUVs OR ROV OR ROVs OR UUV OR UUVs OR underwater OR "surface vehicle*" OR USV OR USVs OR vessel* OR exoskeleton* OR rehabilitation OR prosthe* OR orthos* OR wheeled OR nonholonomic OR legged OR biped* OR quadruped* OR humanoid* OR gripper* OR continuum) AND (DOCTYPE(ar) OR DOCTYPE(re)) AND LANGUAGE(english) AND PUBYEAR > 2015 AND PUBYEAR < 2027 AND NOT TITLE-ABS-KEY(robot* OR robotic* OR "mechanical system*" OR "Euler-Lagrange" OR "Euler Lagrange" OR underactuated OR "multi-link" OR "n-link")
```

## Citation chasing

Backward: references of 19 seed reviews (OpenCitations Index v2, Semantic Scholar and Crossref reference lists). Forward: citing works of 6 classic robot-SMC papers (Semantic Scholar, full pagination). Candidates were filtered by title (SMC and platform terms), years 2016–2026 and journal article type; pre-2016 works with at least 150 citations were assessed as canon candidates. Run on 11 November 2026.

