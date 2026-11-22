import json,urllib.parse,urllib.request,time
miss=[("Man Paplinski Wu 1994","robust MIMO terminal sliding mode control scheme rigid robotic manipulators"),
("Shtessel Fridman Plestan 2016","Higher order sliding modes backgrounds and some recent contributions"),
("Utkin 2016","Discussion aspects of high-order sliding mode control"),
("Edwards Spurgeon 1998 libro","Sliding Mode Control Theory and Applications Edwards Spurgeon"),
("Shtessel et al 2014 libro","Sliding Mode Control and Observation Shtessel"),
("Perruquetti Barbot 2002 libro","Sliding Mode Control in Engineering Perruquetti"),
("Slotine Li 1991 libro","Applied Nonlinear Control Slotine Li"),
("Emelyanov 1967","Variable structure control systems Emelyanov"),
("Itkis 1976","Control systems of variable structure Itkis")]
for lab,q in miss:
    u='https://api.semanticscholar.org/graph/v1/paper/search?'+urllib.parse.urlencode({'query':q,'limit':3,'fields':'title,year,externalIds,citationCount,venue,authors'})
    for tr in range(4):
        try: res=json.load(urllib.request.urlopen(u,timeout=30)).get('data',[]); break
        except Exception as e: res=None; time.sleep(4)
    print('==',lab, '' if res is not None else 'ERR')
    for it in (res or []):
        print('  ',it['year'],it['citationCount'],(it.get('externalIds') or {}).get('DOI'),'|',it['title'][:70],'|',', '.join(a['name'] for a in it['authors'][:3])[:45],'|',it['venue'][:30])
    time.sleep(1.5)
