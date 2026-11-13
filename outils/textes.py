"""Textes de Ginette appliqués à toutes les pages de docs/ (menu, pied de page, lettre d'information, découpage de la home).
Idempotent : on peut le relancer sans risque. À lancer après generer_lampes.py et generer_sections.py :
    python3 outils/generer_lampes.py && python3 outils/generer_sections.py && python3 outils/textes.py"""
import os, re, glob
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs'); os.chdir(D)
REMPL=[
 # menu : Kids devient Enfants
 ('>Kids</a>','>Enfants</a>'),
 # lettre d'information : « Demandez le programme ! », vouvoiement
 ('<section class="lettre">','<section class="lettre" id="lettre">'),
 ('<h2>Le programme dans ta boîte aux lettres</h2>','<h2>Demandez le programme !</h2>'),
 ("<p>Les nouvelles recrues de la troupe et leurs histoires. Une lettre à la fois.</p>","<p>Les pièces qui arrivent à l'atelier et les coulisses de leur seconde vie, dans votre boîte aux lettres.</p>"),
 ('aria-label="Inscription à la lettre"','aria-label="Inscription au programme"'),
 ('placeholder="Ton adresse e-mail"','placeholder="Votre adresse e-mail"'),
 ('<button type="submit">Recevoir</button>',"<button type=\"submit\">Je m'inscris</button>"),
]
# pied de page : La troupe, Les coulisses, Le guichet
def pied(t):
    t=re.sub(r'<div><h3>Boutique</h3><ul>.*?</ul></div>','<div><h3>La troupe</h3><ul><li><a href="lampes.html">Lampes</a></li><li><a href="meubles.html">Meubles</a></li><li><a href="objets.html">Objets</a></li><li><a href="kids.html">Enfants</a></li></ul></div>',t,flags=re.S)
    t=re.sub(r'<div><h3>La maison</h3><ul>.*?</ul></div>','<div><h3>Les coulisses</h3><ul><li><a href="#">L\'atelier</a></li><li><a href="a-propos.html">Le carnet de route</a></li><li><a href="#lettre">Le programme</a></li></ul></div>',t,flags=re.S)
    t=t.replace('<div><h3>Aide</h3>','<div><h3>Le guichet</h3>')
    return t
# menu mobile : ajouter « Le programme » s'il manque
def menu_mobile(t):
    return re.sub(r'(<div class="menu"[^>]*>.*?<nav>)(.*?)(</nav>)',lambda m: m.group(1)+m.group(2)+('' if 'Le programme' in m.group(2) else '<a href="#lettre">Le programme</a>')+m.group(3),t,count=1,flags=re.S)
# home : découpage de l'affiche (Aussi à l'affiche, Le petit théâtre)
def home(t):
    if 'aff-home' in t: return t
    t=re.sub(r'<li class="noms__sep"[^>]*>.*?</li>','',t)
    liens={'Doña Frida K':'meuble-dona-frida-k.html','Honoré Naturel':'meuble-honore-naturel.html','Ludovic Soleil':'objet-ludovic-soleil.html','Mireille Barbotine':'objet-mireille-barbotine.html'}
    def cible(m):
        nom=m.group(3)+' '+m.group(4)
        return m.group(0) if nom not in liens else m.group(0).replace('href="#"','href="%s"'%liens[nom],1)
    t=re.sub(r'<li><a href="#"([^>]*)><span class="t">([^<]*)</span><span class="n">([^<]*)</span>',lambda m:m.group(0),t)  # placeholder
    items=list(re.finditer(r'<li><a href="([^"]*)"[^>]*><span class="t">([^<]*)</span><span class="n">([^<]*)</span>',t))
    out=t; 
    for m in reversed(items):
        nom=m.group(2)+' '+m.group(3)
        if m.group(1)=='#' and nom in liens:
            seg=m.group(0).replace('href="#"','href="%s"'%liens[nom],1); out=out[:m.start()]+seg+out[m.end():]
    t=out
    items=list(re.finditer(r'<li><a href="([^"]*)"[^>]*><span class="t">([^<]*)</span><span class="n">([^<]*)</span>',t))
    noms=[m.group(2)+' '+m.group(3) for m in items]
    lampes=[m for m in items if m.group(1).startswith('lampe-')]
    cabanons=[m for m in items if m.group(2)=='Les' and m.group(3)=='Cabanons']
    autres=[m for m in items if m not in lampes and m not in cabanons]
    if autres and cabanons:
        deb=autres[0].start(); t=t[:deb]+'<li class="noms__sep" id="aussi-a-l-affiche"><b>(%d)</b> Aussi à l\'affiche</li>'%len(autres)+t[deb:]
        items=list(re.finditer(r'<li><a href="([^"]*)"[^>]*><span class="t">Les</span><span class="n">Cabanons</span>',t))
        deb=items[0].start(); t=t[:deb]+'<li class="noms__sep" id="petit-theatre"><b>(1)</b> Le petit théâtre</li>'+t[deb:]
    t=re.sub(r'(<p class="noms__tete"[^>]*><b>)\(\d+\)(</b> À l\'affiche</p>)',lambda m:m.group(1)+'(%d)'%len(lampes)+m.group(2),t)
    return t
for f in sorted(glob.glob('*.html')):
    t=open(f).read(); t0=t
    for a,b in REMPL: t=t.replace(a,b)
    t=pied(t); t=menu_mobile(t)
    if f=='index.html': t=home(t)
    # titres des pages de section : Kids → Enfants
    if f=='kids.html': t=t.replace('<h1 class="coll__t">Kids</h1>','<h1 class="coll__t">Enfants</h1>').replace('Accueil</a> <span>/</span> Kids','Accueil</a> <span>/</span> Enfants').replace('Rotin Bohème · Kids','Rotin Bohème · Enfants')
    if t!=t0: open(f,'w').write(t)
print('textes appliqués')
