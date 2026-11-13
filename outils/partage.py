"""Image de partage sur les réseaux sociaux (Open Graph et carte Twitter) : Lulu Guinguette, sur toutes les pages.
À lancer en dernier, après les autres scripts :  python3 outils/partage.py
L'image (1200 x 630) est docs/assets/partage.jpg, tirée de la photo studio de Lulu Guinguette allumée.
"""
import os, re, glob, html
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(os.path.join(root,'docs'))
BASE='https://jdehas.github.io/rotin_boheme/'
ALT="Lulu Guinguette, lampe à pied de céramique écrue et abat-jour bleu ciel à franges moutarde, allumée"
n=0
for f in sorted(glob.glob('*.html')):
    h=open(f).read()
    h=re.sub(r'<meta (?:property="og:|name="twitter:)[^>]*>','',h)
    t=re.search(r'<title>(.*?)</title>',h,re.S); d=re.search(r'<meta name="description" content="([^"]*)"',h)
    if not t: continue
    tags=(f'<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="Rotin Bohème">'
          f'<meta property="og:title" content="{t.group(1)}">'+(f'<meta property="og:description" content="{d.group(1)}">' if d else '')+
          f'<meta property="og:url" content="{BASE}{"" if f=="index.html" else f}">'
          f'<meta property="og:image" content="{BASE}assets/partage.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{html.escape(ALT)}">'
          f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}assets/partage.jpg"><meta name="twitter:image:alt" content="{html.escape(ALT)}">')
    h=h.replace('</head>',tags+'</head>',1); open(f,'w').write(h); n+=1
print('pages',n)
