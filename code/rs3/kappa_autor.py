# κ de Cohen autor (codificación ciega) vs reglas automáticas RS3. Uso: python kappa_autor.py <carpeta 07>
import sys,csv,json,os
from openpyxl import load_workbook
D=sys.argv[1] if len(sys.argv)>1 else '.'
ws=load_workbook(os.path.join(D,'CODIFICACION_CIEGA_AUTOR_60.xlsx'))['Codificar']
H=[c.value for c in ws[1]]; A={}
for row in ws.iter_rows(min_row=2,values_only=True):
    d=dict(zip(H,row)); A[d['id']]=d
K={r['id']:r for r in csv.DictReader(open(os.path.join(D,'_clave_no_abrir','CLAVE_codificacion_ciega.csv'),encoding='utf-8-sig'))}
def norm(x): x=(x or '').strip().lower(); return 'sí' if x in('sí','si','s','yes','1','x') else ('no' if x in('','no','n','0') else x)
def kappa(pairs):
    n=len(pairs); 
    if not n: return None
    cats=sorted({a for a,b in pairs}|{b for a,b in pairs}); po=sum(a==b for a,b in pairs)/n
    pe=sum((sum(a==c for a,b in pairs)/n)*(sum(b==c for a,b in pairs)/n) for c in cats)
    return dict(n=n,acuerdo=round(po,3),kappa=round((po-pe)/(1-pe),3) if pe<1 else 1.0)
done=[i for i in K if A.get(i) and (A[i].get('pertinente_I1_I2') or '').strip()]
out={'pertinencia_I1_I2':kappa([(norm(A[i]['pertinente_I1_I2']),K[i]['pertinente']) for i in done])}
both=[i for i in done if norm(A[i]['pertinente_I1_I2'])=='sí' and K[i]['pertinente']=='sí']
out['plataforma']=kappa([((A[i]['plataforma'] or '').strip(),K[i]['plataforma']) for i in both])
for v in ['TSM (terminal)','STA/HOSM','Adaptativo','Inteligente (NN/difuso/aprendizaje)','Observador','Tiempo finito/fijo/predefinido','ISM (integral)','validacion_experimental']:
    out[v]=kappa([(norm(A[i][v]),K[i][v]) for i in both])
json.dump(out,open(os.path.join(D,'kappa_autor_resultado.json'),'w'),ensure_ascii=False,indent=1); print(json.dumps(out,ensure_ascii=False,indent=1))
