import json,urllib.parse,urllib.request,csv,time
miss=[("Man Paplinski Wu 1994","A robust MIMO terminal sliding mode control scheme for rigid robotic manipulators",1994),
("Shtessel Fridman Plestan 2016","Higher order sliding modes: backgrounds and some recent contributions",2016),
("Utkin 2016","Discussion aspects of high-order sliding mode control",2016),
("Edwards Spurgeon 1998 libro","Sliding Mode Control: Theory and Applications",1998),
("Shtessel et al 2014 libro","Sliding Mode Control and Observation",2014),
("Perruquetti Barbot 2002 libro","Sliding Mode Control in Engineering",2002),
("Slotine Li 1991 libro","Applied Nonlinear Control",1991),
("Emelyanov 1967","Variable structure control systems",1967),
("Itkis 1976","Control Systems of Variable Structure",1976)]
H={'User-Agent':'mailto:research@example.org'}
for lab,t,y in miss:
    u='https://api.openalex.org/works?'+urllib.parse.urlencode({'search':t,'per-page':5,'select':'id,doi,display_name,publication_year,cited_by_count,type,primary_location,authorships'})
    try: res=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30))['results']
    except Exception as e: print(lab,'ERR',e); continue
    print('==',lab)
    for it in res[:4]:
        src=((it.get('primary_location') or {}).get('source') or {}).get('display_name')
        au=', '.join(a['author']['display_name'] for a in it['authorships'][:3])
        print('  ',it['publication_year'],it['cited_by_count'],it['type'],it['doi'],'|',it['display_name'][:70],'|',au[:50],'|',src)
    time.sleep(0.2)
