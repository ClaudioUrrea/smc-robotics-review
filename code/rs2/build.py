import sys,glob,re,json,csv,os
sys.path.insert(0,'./scripts')
from parse import *
base='./work/'
# Scopus
sc={}
for f in sorted(glob.glob(base+'respaldos_scopus/S*_completo*.bib')):
    b=os.path.basename(f)
    if 'integral' in b: continue
    code=re.match(r'(S\d+|SR\d+)',b).group(1)
    allr=recs(f)
    # rank within string by citations
    rows=[]
    for r in allr:
        note=field(r,'note'); m=re.search(r'Cited by:\s*(\d+)',note)
        c=int(m.group(1)) if m else 0
        rows.append((c,r))
    rows.sort(key=lambda x:-x[0])
    for rank,(c,r) in enumerate(rows,1):
        doi=doi_n(field(r,'doi')); title=field(r,'title'); k=doi or norm(title)
        e=sc.setdefault(k,dict(doi=doi,title=title,year=field(r,'year'),journal=field(r,'journal'),
            cites=c,abstract=field(r,'abstract'),akw=field(r,'author_keywords'),dt=field(r,'type'),kw=field(r,'keywords'),strata={}))
        e['strata'][code]=rank
# WoS universe
wos_doi=set(); wos_title=set(); n=0
for f in glob.glob('./work/*.bib'):
    b=os.path.basename(f)
    if not re.search(r'(X\d\d|Q0\d)',b): continue
    for r in recs(f):
        n+=1
        d=doi_n(field(r,'doi')); t=norm(field(r,'title'))
        if d: wos_doi.add(d)
        if t: wos_title.add(t)
print('WoS registros leidos',n,'DOIs',len(wos_doi),'titulos',len(wos_title))
# screened WoS
scr={}
for row in csv.DictReader(open(base+'CRIBADO_WOS_RS2.csv',encoding='utf-8')):
    scr[doi_n(row['doi'])]=row; scr[norm(row['titulo'])]=row
for k,e in sc.items():
    e['in_wos']= (e['doi'] in wos_doi) or (norm(e['title']) in wos_title)
    e['wos_screened']=scr.get(e['doi']) or scr.get(norm(e['title']))
json.dump(sc,open(base+'analisis/scopus_unicos.json','w'))
tot=len(sc); inw=sum(e['in_wos'] for e in sc.values()); ins=sum(1 for e in sc.values() if e['wos_screened'])
print('Scopus unicos',tot,'en WoS (cualquier export)',inw,'solo Scopus',tot-inw,'ya cribados en WoS',ins)
