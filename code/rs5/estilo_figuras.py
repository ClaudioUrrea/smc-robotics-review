"""Common figure style for Paper R2: Palatino-type font and true minus sign (U+2212).
- Windows: uses Palatino Linotype (TrueType, installed with Windows).
- Linux/macOS: converts TeX Gyre Pagella (Palatino clone shipped with TeX Live) from OTF/CFF to TrueType once
  (cache in ~/.cache/r2_fonts) so that PDFs embed a consistent TrueType font (no CFF/Type42 mismatch)."""
import os, glob, matplotlib
from matplotlib import font_manager as fm
CACHE=os.path.join(os.path.expanduser("~"),".cache","r2_fonts")
def _otf2ttf(src,dst):
    from fontTools.ttLib import TTFont,newTable
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    f=TTFont(src); go=f.getGlyphOrder(); gs=f.getGlyphSet(); glyf={}
    for n in go:
        pen=TTGlyphPen(gs); gs[n].draw(Cu2QuPen(pen,1.0,reverse_direction=True)); glyf[n]=pen.glyph()
    f["loca"]=newTable("loca"); f["glyf"]=g=newTable("glyf"); g.glyphOrder=go; g.glyphs=glyf; del f["CFF "]
    f["maxp"]=m=newTable("maxp"); m.tableVersion=0x00010000; m.maxZones=1
    for k in ("maxTwilightPoints","maxStorage","maxFunctionDefs","maxInstructionDefs","maxStackElements","maxSizeOfInstructions","maxComponentElements"): setattr(m,k,0)
    f["head"].glyphDataFormat=0; f["post"].formatType=2.0; f["post"].extraNames=[]; f["post"].mapping={}; f["post"].glyphOrder=go
    f.sfntVersion="\x00\x01\x00\x00"; f.save(dst)
def _pagella_ttf():
    os.makedirs(CACHE,exist_ok=True); out=[]
    for src in sorted(set(glob.glob("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-*.otf")+glob.glob("/usr/share/texlive/texmf-dist/fonts/opentype/public/tex-gyre/texgyrepagella-*.otf"))):
        dst=os.path.join(CACHE,os.path.basename(src)[:-4]+".ttf")
        if not os.path.exists(dst): _otf2ttf(src,dst)
        out.append(dst)
    return out
def aplicar(base=8):
    win=[p for p in glob.glob(r"C:\Windows\Fonts\pala*.ttf")]
    paths=win or _pagella_ttf()
    if not paths: raise SystemExit("No Palatino-type font found (Palatino Linotype or TeX Gyre Pagella)")
    for p in paths: fm.fontManager.addfont(p)
    fam="Palatino Linotype" if win else "TeX Gyre Pagella"
    # keep only TrueType entries of the chosen family
    fm.fontManager.ttflist=[f for f in fm.fontManager.ttflist if not (f.name==fam and not f.fname.lower().endswith(".ttf"))]
    matplotlib.rcParams.update({"font.family":"serif","font.serif":[fam],"font.size":base,
        "mathtext.fontset":"custom","mathtext.rm":fam,"mathtext.it":fam+":italic","mathtext.bf":fam+":bold","mathtext.sf":fam,"mathtext.cal":fam,
        "axes.unicode_minus":True,"axes.spines.top":False,"axes.spines.right":False,"axes.linewidth":0.7,
        "lines.linewidth":1.4,"pdf.fonttype":42,"ps.fonttype":42})
    return fam
