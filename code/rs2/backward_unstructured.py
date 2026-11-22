import json,urllib.request,urllib.parse,re,time,difflib
def J(u):
    for t in range(8):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'PaperR2/1.0'}),timeout=60))
        except Exception as e: time.sleep(4*(t+1))
    return None
S='./work/analisis/snowball/'
s2=json.load(open(S+'s2_referencias_revisiones.json')); oc=json.load(open(S+'candidatos.json'))
known=set(oc)|{k for k in s2['referencias'] if not k.startswith('s2:')}
smc=re.compile(r'sliding[\s-]*mode|sliding[\s-]*surface|super[\s-]*twisting|terminal sliding|variable structure|twisting',re.I)
plat=re.compile(r'robot|manipulator|quadrotor|quadcopter|multi[\s-]*rotor|UAV|unmanned aerial|AUV|ROV|UUV|underwater|exoskeleton|rehabilitation|wearable|drone|legged|wheeled|nonholonomic|aerial|haptic|prosthe|vessel|surface vehicle|gripper|continuum|link|flexible[\s-]*joint|mechanical system|Euler|underactuated|spacecraft',re.I)
out={};stats=dict(sin_doi=0,smc_plat=0,resueltos=0,doi_nuevo=0)
for doi in s2['conteos']:
    m=(J('https://api.crossref.org/works/'+urllib.parse.quote(doi)) or {'message':{}})['message']
    for r in m.get('reference',[]):
        d=(r.get('DOI') or '').lower()
        if d:
            if d not in known: out.setdefault(d,dict(src='crossref-ref-doi',seeds=[]))['seeds'].append(doi); stats['doi_nuevo']+=1
            continue
        stats['sin_doi']+=1
        txt=' '.join(str(r.get(k,'')) for k in ('article-title','unstructured','volume-title','journal-title'))
        if not (smc.search(txt) and plat.search(txt)): continue
        stats['smc_plat']+=1
        q=r.get('article-title') or r.get('unstructured') or txt
        u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':q[:300],'rows':2,'select':'DOI,title'})
        it=(J(u) or {'message':{'items':[]}})['message']['items']
        for x in it[:1]:
            t=(x.get('title') or [''])[0]
            if t and (t.lower()[:40] in q.lower() or difflib.SequenceMatcher(None,t.lower(),q.lower()[:len(t)+40]).ratio()>0.6):
                dd=x['DOI'].lower(); stats['resueltos']+=1
                if dd not in known: out.setdefault(dd,dict(src='crossref-ref-texto',seeds=[]))['seeds'].append(doi)
        time.sleep(0.6)
    print(doi,stats,flush=True)
json.dump(out,open(S+'backward_extra.json','w')); print('DOI extra',len(out),stats)
