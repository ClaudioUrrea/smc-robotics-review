# Normalización de texto (RS3): títulos paralelos en otro idioma, entidades HTML, puntuación de ancho completo, CJK residual y aviso de copyright final.
import re,unicodedata,html
CJK=re.compile(r'[぀-ヿ㐀-䶿一-鿿가-힯　-〿]')
def clean(s,abstract=False):
    if not s: return s or ''
    s=html.unescape(html.unescape(s))
    s=re.sub(r'<sub>([^<]*)</sub>',r'_\1',s); s=re.sub(r'<sup>([^<]*)</sup>',r'^\1',s); s=re.sub(r'</?(inf|i|b|em|strong|sc|mml:[a-z]+)[^>]*>','',s)
    if not abstract: s=re.sub(r';\s*\[[^\]]{8,}\]?\s*,?\s*$','',s)   # título paralelo en otro idioma: «…; [traducción]»
    s=s.replace('\uffe3','').replace('\u203e','')
    s=unicodedata.normalize('NFKC',s).replace('\u0304','')
    s=re.sub(r';\s*\[[^\]]*'+CJK.pattern+r'[^\]]*\]?','',s)          # «; [título en chino]»
    s=re.sub(r'\[[^\]]*'+CJK.pattern+r'[^\]]*\]','',s)
    s=re.sub(r'(\S*'+CJK.pattern+r'+\S*\s*)+','',s)                     # CJK residual
    if abstract:
        s=re.split(r'\},\s*[a-z_]+\s*=\s*\{',s)[0]                      # campo .bib arrastrado
        cut=re.compile(r'((Crown\s+)?Copyright\b|©|\(C\)\s*\d{4}|\(c\)\s*\d{4}|All rights reserved|This (article|work|paper) is (an open access article |)(distributed|licensed|published) under|This is an open access article|licensed under a Creative Commons|under the terms of the Creative Commons|Esta obra está bajo una licencia|Published by (Wiley|Elsevier)|Authors retain the copyright|Published under licen[cs]e|Licensee [A-Z]|licensee [A-Z]|\S?\s?\b(19|20)\d{2},? (by )?the authors?\b)',re.I)
        mm=[x for x in cut.finditer(s) if len(s)-x.start()<700]
        if mm: s=s[:mm[0].start()]                                       # aviso de copyright/licencia final, desde su primera aparición
        s=re.sub(r'\[(Objective|Methods?|Results?|Conclusions?)\]\s*',r'\1: ',s)
    s=re.sub(r'\s*,\s*',', ',s); s=re.sub(r'\(\s+','(',s); s=re.sub(r'\s+\)',')',s)
    if abstract: s=re.sub(r'(\w)\((?=[A-Z])',r'\1 (',s); s=re.sub(r'\)(?=[A-Za-z]{2})',') ',s)
    return re.sub(r'\s+',' ',s).strip(' ;')
