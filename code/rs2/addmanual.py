import csv
f='./work/CRIBADO_SCOPUS_RS2.csv'
rows=list(csv.DictReader(open(f,encoding='utf-8')))
flds=list(rows[0].keys())
rows.append(dict(orden=len(rows)+1,cadenas='MANUAL(AU-ID)',anio='2022',citas_scopus='12',tipo='Article',titulo='Design of a generalized dynamic model and a trajectory control and position strategy for n-link underactuated revolute planar robots',revista='Control Engineering Practice',doi='por verificar',en_WoS='no verificado',decision='INCLUIR',codigo='Añadido por control AU-ID 24078008600; autoría propia; verificar I1 (SMC principal) y DOI en RS3',rev_cercana=''))
w=csv.DictWriter(open(f,'w',newline='',encoding='utf-8'),fieldnames=flds); w.writeheader(); w.writerows(rows)
import collections; print(collections.Counter(r['decision'] for r in rows),len(rows))
