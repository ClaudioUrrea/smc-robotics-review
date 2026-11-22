# Genera la hoja de codificación ciega (60 registros fijos) y su clave a partir del estado actual de RS3.
import json,csv,re,os,io,sys,contextlib,importlib.util
from openpyxl import Workbook,load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Alignment,Font,PatternFill
R='./work/RS3/'
spec=importlib.util.spec_from_file_location('m','./scripts/rs3_extract.py'); m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
by={r['id']:r for r in m.out}
IDS=[row[1] for row in load_workbook(sys.argv[1])['Codificar'].iter_rows(min_row=2,values_only=True)]   # misma muestra (semilla 5150)
PL=['Manipulador','Aéreo','Submarino/marino','Móvil terrestre/patas','Exoesqueleto/rehabilitación/médico','Espacial','Blando/continuo/pinza','Robot genérico (EL/subactuado)','Sin plataforma robótica']
VAR=['TSM (terminal)','STA/HOSM','Adaptativo','Inteligente (NN/difuso/aprendizaje)','Observador','Tiempo finito/fijo/predefinido','ISM (integral)']
wb=Workbook(); ins=wb.active; ins.title='Instrucciones'
for line in ['Codificación ciega para el κ humano (Paper R2, RS3). Tiempo estimado: 40–50 min.',
'Lea solo el título y el resumen de cada fila. No consulte otros archivos del proyecto: la hoja no muestra códigos automáticos, para que la codificación sea ciega.',
'pertinente_I1_I2: «sí» si el modo deslizante (cualquier variante, incluido el observador por modo deslizante) es el método principal Y se aplica a una plataforma robótica, aunque sea como ejemplo de validación. «no» si el SMC es solo línea base o mención, o si no hay robot (péndulo, grúa, motor, satélite, multiagente abstracto).',
'plataforma: elija de la lista; «Robot genérico» = sistema Euler-Lagrange/subactuado presentado como robot.',
'Columnas de variante: «sí» si el resumen la usa como parte del método propuesto; deje vacío o «no» en otro caso. Varias pueden ser «sí».',
'validacion_experimental: «sí» si el resumen reporta experimentos en hardware real o HIL; «no» si solo hay simulación o no lo dice.',
'Al terminar, guarde el archivo con el mismo nombre en la carpeta 07 y escriba «κ listo». El cálculo es automático (scripts/kappa_autor.py).']:
    ins.append([line])
ins.column_dimensions['A'].width=150
for row in ins.iter_rows():
    for c in row: c.alignment=Alignment(wrap_text=True)
ws=wb.create_sheet('Codificar')
hdr=['n','id','titulo','resumen','pertinente_I1_I2','plataforma']+VAR+['validacion_experimental','nota']; ws.append(hdr)
for c in ws[1]: c.font=Font(bold=True); c.fill=PatternFill('solid',fgColor='DDEBF7'); c.alignment=Alignment(wrap_text=True,vertical='top')
for k,i in enumerate(IDS,1): ws.append([k,i,by[i]['titulo'],m.AB[i]['a']]+['']*(len(hdr)-4))
N=len(IDS)+1
li=wb.create_sheet('Listas'); li.append(['plataforma']); [li.append([p]) for p in PL]
dv1=DataValidation(type='list',formula1='"sí,no"',allow_blank=True); dvp=DataValidation(type='list',formula1='Listas!$A$2:$A$10',allow_blank=True)
ws.add_data_validation(dv1); ws.add_data_validation(dvp); dv1.add(f'E2:E{N}'); dvp.add(f'F2:F{N}')
for col in range(7,7+len(VAR)+1): L=ws.cell(1,col).column_letter; dv1.add(f'{L}2:{L}{N}')
for L,wd in zip('ABCDEF',[4,10,45,90,12,26]): ws.column_dimensions[L].width=wd
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
ws.freeze_panes='E2'
wb.save(R+'CODIFICACION_CIEGA_AUTOR_60.xlsx')
key=[]
for k,i in enumerate(IDS,1):
    r=by[i]; v=r['variante_auto']; inc=r['dec_rs3']=='INCLUIR'; x=m.ext(r)['validacion']
    key.append(dict(n=k,id=i,pertinente='sí' if inc else 'no',plataforma=r['plat_rs3'] if inc else 'Sin plataforma robótica',
      **{'TSM (terminal)':'sí' if 'Terminal' in v else 'no','STA/HOSM':'sí' if 'STA' in v else 'no','Adaptativo':'sí' if 'Adaptativo' in v else 'no','Inteligente (NN/difuso/aprendizaje)':'sí' if 'Inteligente' in v else 'no','Observador':'sí' if 'observador' in v else 'no','Tiempo finito/fijo/predefinido':'sí' if 'Tiempo' in v else 'no','ISM (integral)':'sí' if 'Integral' in v else 'no'},
      validacion_experimental='sí' if ('experimento' in x or 'HIL' in x) else 'no'))
os.makedirs(R+'_clave_no_abrir',exist_ok=True)
w=csv.DictWriter(open(R+'_clave_no_abrir/CLAVE_codificacion_ciega.csv','w',newline='',encoding='utf-8-sig'),fieldnames=list(key[0])); w.writeheader(); w.writerows(key)
print(len(IDS),sum(1 for x in key if x['pertinente']=='sí'))
