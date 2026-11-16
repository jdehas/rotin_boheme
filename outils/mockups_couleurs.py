"""Deux mockups de la home avec deux autres systèmes de couleurs (le système actuel, « Nuit de midi », reste la référence).
Génère : docs/assets/immersive-b.css, immersive-c.css, docs/mockup-couleurs-b.html, mockup-couleurs-c.html et la page de comparaison docs/mockup-couleurs.html.
    python3 outils/mockups_couleurs.py
Chaque feuille est la feuille actuelle dont les couleurs sont remplacées une à une (même mise en page, mêmes photos, seul le système de couleurs change).
"""
import os, re, html
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(root, 'docs')

# Système actuel (A) : couleurs à remplacer
A = dict(BG='#15213A', BG2='#1E2D4A', FG='#EFE8DA', FG2='#F2E9DA', ACC_D='#D6A65A', ACC_L='#E2621B',
         DK='#141414', LBG='#FFFFFF', LT='#F1EDE4', TILE='#E9E0CE', HFG='#F5F1E7')

PALETTES = {
 'b': dict(nom='Velours', slogan='Le rideau se lève',
    desc="Un rideau de théâtre en velours bordeaux, des roses poudrés de coulisses, un or de lampe allumée. Chaleureux, dramatique, très « scène ».",
    BG='#4A1626', BG2='#5F2237', FG='#F6E6DA', FG2='#F6E6DA', ACC_D='#EDB872', ACC_L='#B8322A',
    DK='#2B1119', LBG='#F8EAE0', LT='#EFD6C9', TILE='#EBCFC2', HFG='#FBEFE4'),
 'c': dict(nom='Rotin et sauge', slogan='La roulotte dans la jungle',
    desc="Le vert profond des plantes de Miss Flower et du bois de la roulotte, le lin du rotin, un ocre de paille. Naturel, solaire, bohème.",
    BG='#23392E', BG2='#31503F', FG='#F1EBDA', FG2='#F1EBDA', ACC_D='#E3B547', ACC_L='#A85F18',
    DK='#1F2A22', LBG='#F5EFE0', LT='#E8DFC9', TILE='#E4DCC6', HFG='#F7F1E2'),
}

def rgb(h): h = h.lstrip('#'); return ','.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))

def recolorer(css, P):
    out = []
    for ln in css.split('\n'):
        carnet = '.carnet .lien' in ln
        def rep(old, new): return re.sub(re.escape(old), new, ln, flags=re.I)
        ln = rep(A['ACC_L'], P['ACC_D'] if carnet else P['ACC_L'])
        ln = rep(A['BG'], P['BG']); ln = rep(A['BG2'], P['BG2'])
        ln = rep(A['FG'], P['FG']); ln = rep(A['FG2'], P['FG2'])
        ln = rep(A['ACC_D'], P['ACC_D']); ln = rep(A['DK'], P['DK'])
        ln = rep(A['LT'], P['LT']); ln = rep(A['TILE'], P['TILE']); ln = rep(A['HFG'], P['HFG'])
        if 'background:#fff' in ln or '--bg:#fff' in ln: ln = ln.replace('#fff', P['LBG'])
        ln = ln.replace('rgba(239,232,218,', f"rgba({rgb(P['FG'])},")
        ln = ln.replace('rgba(21,33,58,', f"rgba({rgb(P['BG'])},")
        ln = ln.replace('rgba(30,45,74,', f"rgba({rgb(P['BG2'])},")
        ln = ln.replace('rgba(20,20,20,', f"rgba({rgb(P['DK'])},")
        out.append(ln)
    return '\n'.join(out)

css = open(os.path.join(D, 'assets/immersive.css')).read()
home = open(os.path.join(D, 'index.html')).read()
for k, P in PALETTES.items():
    open(os.path.join(D, f'assets/immersive-{k}.css'), 'w').write(recolorer(css, P))
    h = home.replace('assets/immersive.css', f'assets/immersive-{k}.css')
    h = re.sub(r'<title>.*?</title>', f'<title>Mockup couleurs · {P["nom"]} · Rotin Bohème</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta (?:property="og:|name="twitter:)[^>]*>', '', h)
    open(os.path.join(D, f'mockup-couleurs-{k}.html'), 'w').write(h)

# Page de comparaison
def sw(c, n, claire=False): return f'<li style="background:{c};color:{"#141414" if claire else "#fff"}"><b>{n}</b><span>{c}</span></li>'
def bloc(nom, slogan, desc, P, lien, tag):
    cl = lambda x: sum(int(x.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) > 420
    sws = ''.join(sw(P[c], n, cl(P[c])) for c, n in (('BG', 'Fond profond'), ('BG2', 'Fond secondaire'), ('FG', 'Texte sur fond profond'), ('ACC_D', 'Accent sur fond profond'), ('LBG', 'Sections claires'), ('DK', 'Texte sur clair'), ('ACC_L', 'Accent sur clair'), ('LT', 'Fonds de vignettes')))
    return f'<section><p class="t">{tag}</p><h2>{nom}</h2><p class="s">{slogan}</p><p class="d">{desc}</p><ul>{sws}</ul><a href="{lien}">Voir la home avec ce système</a></section>'
A_P = dict(BG=A['BG'], BG2=A['BG2'], FG=A['FG'], ACC_D=A['ACC_D'], LBG=A['LBG'], DK=A['DK'], ACC_L=A['ACC_L'], LT=A['LT'])
corps = (bloc('Nuit de midi', 'Le soleil s’est couché à midi', "Le bleu nuit de la pièce « Il est 12 h, Miss Flower », le crème des lampes éteintes, l’orange des abat-jour allumés. Théâtral et nocturne : c’est le système en ligne aujourd’hui.", A_P, 'index.html', 'Système A, actuel')
         + ''.join(bloc(P['nom'], P['slogan'], P['desc'], P, f'mockup-couleurs-{k}.html', 'Système ' + k.upper()) for k, P in PALETTES.items()))
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Trois systèmes de couleurs · Rotin Bohème</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FAF7F2;--fg:#1E1A16}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:"Instrument Sans",system-ui,sans-serif;line-height:1.5}}
header{{max-width:78rem;margin:0 auto;padding:3.5rem 1.25rem 1rem}}
h1{{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:clamp(2.4rem,6vw,4.4rem);line-height:1;margin:0 0 .8rem}}
header p{{max-width:44rem;color:rgba(30,26,22,.7);margin:0}}
main{{max-width:78rem;margin:0 auto;padding:1.5rem 1.25rem 4rem;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.5rem}}
section{{background:#fff;border-radius:1.2rem;padding:1.6rem;box-shadow:0 1px 0 rgba(0,0,0,.06)}}
.t{{font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;color:rgba(30,26,22,.55);margin:0 0 .5rem}}
h2{{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:2.2rem;line-height:1.05;margin:0}}
.s{{font-style:italic;color:rgba(30,26,22,.6);margin:.3rem 0 .8rem}} .d{{font-size:.95rem;margin:0 0 1.1rem}}
ul{{list-style:none;margin:0 0 1.2rem;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:.5rem}}
li{{border-radius:.7rem;padding:.7rem .8rem;display:flex;flex-direction:column;gap:.1rem;min-height:4.4rem;justify-content:flex-end;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}}
li b{{font-weight:500;font-size:.8rem}} li span{{font-size:.75rem;opacity:.8;font-variant-numeric:tabular-nums}}
a{{color:inherit;text-underline-offset:.25em}}
@media (max-width:980px){{main{{grid-template-columns:1fr}}}}
</style></head><body>
<header><h1>Trois systèmes de couleurs</h1><p>Même plateforme de marque, mêmes photos, même mise en page. Seul le système de couleurs change : un bleu nuit (actuel), un velours bordeaux et un vert sauge naturel. Chacun mène à la home complète.</p></header>
<main>{corps}</main></body></html>'''
open(os.path.join(D, 'mockup-couleurs.html'), 'w').write(page)
print('mockups ok')
