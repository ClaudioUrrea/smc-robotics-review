import re,glob,json,sys,os,unicodedata
def norm(t):
    t=unicodedata.normalize('NFKD',t.lower()); t=re.sub(r'[^a-z0-9]+',' ',t); return re.sub(r'\s+',' ',t).strip()
def field(r,name):
    m=re.search(r'(?im)^\s*'+name+r'\s*=\s*\{',r)
    if not m: return ''
    i=m.end(); d=1; j=i
    while j<len(r) and d>0:
        c=r[j]
        if c=='{': d+=1
        elif c=='}': d-=1
        j+=1
    return re.sub(r'\s+',' ',r[i:j-1]).strip()
def recs(path):
    t=open(path,encoding='utf-8-sig',errors='ignore').read()
    return [r for r in re.split(r'\n(?=@[A-Za-z]+\s*\{)',t) if re.match(r'\s*@',r)]
def doi_n(d): 
    d=d.lower().strip(); d=re.sub(r'^https?://(dx\.)?doi\.org/','',d); return d
