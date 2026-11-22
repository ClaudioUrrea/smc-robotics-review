import json,csv,collections
# Lectura de auditoría de reglas asistida por IA generativa (título+resumen, sin ver los códigos automáticos)
H={1:('EXO',''),2:('MAR','FT OBS'),3:('AER','OBS'),4:('AER','ADA'),5:('MAN','INT'),6:('MAR','TSM FT'),7:('MAN','FT OBS ADA'),8:('AER',''),9:('OTR','OBS'),10:('MAN',''),
11:('BLA',''),12:('OTR','ISM INT'),13:('AER','ADA ISM INT FT'),14:('MOV','INT'),15:('MAN','ISM STA ADA OBS FT'),16:('MAN',''),17:('MAN',''),18:('MAN','OBS FT ISM'),19:('MAN','ADA'),20:('MAR','STA ADA'),
21:('EXO',''),22:('MOV','ISM'),23:('AER','ADA'),24:('EXO','OBS TSM FT'),25:('MAN',''),26:('MAN','ADA INT'),27:('OTR','ISM'),28:('AER','OBS'),29:('MAR','STA ADA'),30:('MAR','TSM OBS'),
31:('MAN','TSM INT'),32:('AER','ADA FT'),33:('AER',''),34:('AER',''),35:('OTR','OBS INT'),36:('EXO',''),37:('MOV',''),38:('MAR','STA FT'),39:('MAN',''),40:('MAR','FT OBS'),
41:('OTR',''),42:('MAR','STA ADA OBS'),43:('MOV','OBS'),44:('AER','INT'),45:('AER','TSM FT'),46:('MAR','ADA INT'),47:('AER','TSM FT OBS'),48:('MAR','OBS'),49:('MOV','INT ADA'),50:('MOV','ADA'),
51:('AER','ADA'),52:('MAN','ADA INT'),53:('MAR','ADA OBS'),54:('OTR','ADA TSM FT'),55:('AER','STA OBS ADA'),56:('OTR',''),57:('MAN',''),58:('MAN','OBS'),59:('ESP','INT ADA'),60:('MAN','FT'),
61:('AER','ADA'),62:('AER',''),63:('MOV','ADA OBS'),64:('MOV','ADA OBS'),65:('OTR','INT STA'),66:('MAN','TSM FT'),67:('MAN','STA'),68:('MAR','TSM FT'),69:('OTR','ADA INT'),70:('AER','FT OBS'),
71:('MAR',''),72:('AER',''),73:('EXO','INT'),74:('NOROB',''),75:('MOV',''),76:('MOV','ADA'),77:('OTR','OBS ADA'),78:('MAN','TSM FT OBS'),79:('MAN','FT ADA INT'),80:('EXO','ADA'),
81:('MAN',''),82:('ESP','INT'),83:('OTR','INT ADA'),84:('AER','INT ADA'),85:('MOV','OBS'),86:('AER',''),87:('OTR',''),88:('MAN','TSM OBS'),89:('ESP','TSM FT'),90:('MAR','OBS FT'),
91:('OTR','INT'),92:('MAN','INT'),93:('AER','FT OBS'),94:('MAR',''),95:('OTR','ADA'),96:('AER','TSM FT'),97:('MAN','INT FT TSM'),98:('AER',''),99:('MOV',''),100:('MOV','ADA TSM')}
PM={'Manipulador':'MAN','Aéreo':'AER','Submarino/marino':'MAR','Móvil terrestre/patas':'MOV','Exoesqueleto/rehabilitación/médico':'EXO','Espacial':'ESP','Blando/continuo/pinza':'BLA','Otro/genérico (EL, subactuado)':'OTR'}
VM={'TSM':'Terminal (TSM/NTSM/FTSM)','STA':'STA/HOSM','ADA':'Adaptativo','INT':'Inteligente (neuronal/difuso/aprendizaje)','OBS':'Basado en observador','FT':'Tiempo finito/fijo/predefinido','ISM':'Integral (ISM)'}
S=json.load(open('./work/analisis/validacion_muestra100.json'))
C={x['id']:x for x in csv.DictReader(open('./work/CORPUS_RS2_UNIFICADO.csv',encoding='utf-8-sig'))}
def kappa(a,b):
    n=len(a); po=sum(x==y for x,y in zip(a,b))/n
    ca=collections.Counter(a); cb=collections.Counter(b); pe=sum(ca[k]*cb[k] for k in set(a)|set(b))/n/n
    return round(po,3),round((po-pe)/(1-pe),3) if pe<1 else 1.0
A=[];Hh=[];rows=[]
vflags={k:([],[]) for k in VM}
for s in S:
    c=C[s['id']]; ap=PM[c['plataforma_auto']]; hp,hv=H[s['n']]
    A.append(ap); Hh.append(hp)
    av=set(c['variante_auto'].split('; ')); hvs=set(hv.split())
    for k,lab in VM.items(): vflags[k][0].append(lab in av); vflags[k][1].append(k in hvs)
    rows.append(dict(n=s['n'],id=s['id'],titulo=s['titulo'],plataforma_auto=ap,plataforma_ia=hp,variante_auto=c['variante_auto'],variante_ia=hv,coincide_plataforma='sí' if ap==hp else 'no'))
res={'plataforma':dict(zip(('acuerdo','kappa'),kappa(A,Hh)))}
for k in VM: res[VM[k]]=dict(zip(('acuerdo','kappa'),kappa(*vflags[k])))
res['confusiones_plataforma']=collections.Counter(f'{a}->{h}' for a,h in zip(A,Hh) if a!=h).most_common()
json.dump(res,open('./work/analisis/kappa_codificacion.json','w'),ensure_ascii=False,indent=1)
w=csv.DictWriter(open('./work/VALIDACION_CODIFICACION_100.csv','w',newline='',encoding='utf-8-sig'),fieldnames=list(rows[0])+['plataforma_autor','variante_autor','nota_autor']); w.writeheader(); w.writerows(rows)
print(json.dumps(res,ensure_ascii=False,indent=0))
