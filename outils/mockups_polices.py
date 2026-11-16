"""Dix mockups de la home, un par jeu de polices (couleurs actuelles, mêmes photos, même mise en page).
Génère docs/assets/immersive-p1.css à p10.css, docs/mockup-polices-1.html à 10 et la page de comparaison docs/mockup-polices.html.
    python3 outils/mockups_polices.py
"""
import os, re, html
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(root, 'docs')

# (titres, texte, href Google Fonts titres, href texte, a une italique, ambiance)
JEUX = [
 ('Playfair Display', 'Source Sans 3', 'Playfair+Display:ital,wght@0,400..700;1,400..700', 'Source+Sans+3:wght@400;500;600', True, 'Théâtre classique : romantique, italiques très expressifs.'),
 ('Cormorant Garamond', 'Work Sans', 'Cormorant+Garamond:ital,wght@0,400..700;1,400..700', 'Work+Sans:wght@400;500;600', True, 'Raffiné et aérien : très fin, presque papeterie de luxe.'),
 ('DM Serif Display', 'DM Sans', 'DM+Serif+Display:ital@0;1', 'DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600', True, 'Chaleureux et affirmé : gros pleins, accessible, solide.'),
 ('Young Serif', 'Karla', 'Young+Serif', 'Karla:wght@400;500;600', False, 'Rétro et artisanal : un serif trapu, comme une étiquette de brocante.'),
 ('Gloock', 'Figtree', 'Gloock', 'Figtree:wght@400;500;600', False, 'Affiche : contrasté et puissant, très « devant de scène ».'),
 ('Abril Fatface', 'Lato', 'Abril+Fatface', 'Lato:wght@400;700', False, 'Cirque et troupe : une ancienne affiche de saltimbanques, très marquée.'),
 ('Libre Caslon Display', 'Libre Franklin', 'Libre+Caslon+Display', 'Libre+Franklin:wght@400;500;600', False, 'Magazine : sobre, éditorial, comme un programme de théâtre imprimé.'),
 ('Marcellus', 'Mulish', 'Marcellus', 'Mulish:wght@400;500;600', False, 'Gravé et doux : capitales inspirées des inscriptions romaines, très lisibles.'),
 ('Caprasimo', 'Outfit', 'Caprasimo', 'Outfit:wght@400;500;600', False, 'Bohème années 70 : arrondi, joyeux, un peu hippie chic.'),
 ('Prata', 'Hanken Grotesk', 'Prata', 'Hanken+Grotesk:wght@400;500;600', False, 'Élégant et posé : un serif classique avec une sans moderne.'),
]

css = open(os.path.join(D, 'assets/immersive.css')).read()
home = open(os.path.join(D, 'index.html')).read()
liens = []
for i, (ser, sans, hs, hx, ital, amb) in enumerate(JEUX, 1):
    c = css.replace('Instrument Serif', ser).replace('Instrument Sans', sans).replace('Bricolage Grotesque', sans)
    if not ital:  # pas d'italique dessinée : on évite l'italique simulée, plus laide
        c += '\n*{font-synthesis:none}em,i,.pp__exergue,.piece__s,.carnet__sig,.ah__s{font-style:normal}\n'
    open(os.path.join(D, f'assets/immersive-p{i}.css'), 'w').write(c)
    h = home.replace('assets/immersive.css', f'assets/immersive-p{i}.css')
    h = re.sub(r'(https://fonts\.googleapis\.com/css2\?family=)[^"]*', lambda m: m.group(1) + hs + '&family=' + hx + '&display=swap', h, count=1)
    h = re.sub(r'<title>.*?</title>', f'<title>Mockup polices {i} · {ser} et {sans} · Rotin Bohème</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta (?:property="og:|name="twitter:)[^>]*>', '', h)
    open(os.path.join(D, f'mockup-polices-{i}.html'), 'w').write(h)

cartes = ''
for i, (ser, sans, hs, hx, ital, amb) in enumerate(JEUX, 1):
    it = 'italic' if ital else 'normal'
    cartes += (f'<section><p class="n">{i}</p><h2 style="font-family:&quot;{ser}&quot;,serif">Il est 12 h, Miss Flower</h2>'
               f'<p class="nm" style="font-family:&quot;{ser}&quot;,serif;text-transform:uppercase">Guinguette · Mandarine</p>'
               f'<p class="it" style="font-family:&quot;{ser}&quot;,serif;font-style:{it}">objets retrouvés, Bernadette</p>'
               f'<p class="tx" style="font-family:&quot;{sans}&quot;,sans-serif">Je chine des pieds de lampe, des fauteuils et des miroirs qui ont déjà beaucoup servi. Je leur cherche ensuite le décor où ils brilleront le mieux.</p>'
               f'<p class="fn"><b>{ser}</b> et <b>{sans}</b><br>{amb}</p><a href="mockup-polices-{i}.html">Voir la home avec ce jeu</a></section>')
fam = '&family='.join(hs + '&family=' + hx for (_, _, hs, hx, _, _) in JEUX)
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Dix jeux de polices · Rotin Bohème</title>
<link href="https://fonts.googleapis.com/css2?family={fam}&display=swap" rel="stylesheet">
<style>
body{{margin:0;background:#FAF7F2;color:#1E1A16;font-family:system-ui,sans-serif;line-height:1.5}}
header{{max-width:80rem;margin:0 auto;padding:3.5rem 1.25rem 1rem}}
h1{{font-weight:400;font-size:clamp(2.2rem,5vw,3.6rem);line-height:1;margin:0 0 .8rem;font-family:Georgia,serif}}
header p{{max-width:46rem;color:rgba(30,26,22,.7);margin:0}}
main{{max-width:80rem;margin:0 auto;padding:1.5rem 1.25rem 4rem;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.2rem}}
section{{background:#fff;border-radius:1.1rem;padding:1.5rem}}
.n{{font-size:.75rem;letter-spacing:.14em;color:rgba(30,26,22,.5);margin:0 0 .4rem}}
h2{{font-weight:400;font-size:2.3rem;line-height:1.05;margin:0 0 .6rem}}
.nm{{font-size:1.5rem;margin:0 0 .3rem}} .it{{font-size:1.2rem;margin:0 0 .8rem;color:#A85F18}}
.tx{{margin:0 0 1rem;font-size:1rem}} .fn{{font-size:.8rem;color:rgba(30,26,22,.62);margin:0 0 .8rem}}
a{{color:inherit;text-underline-offset:.25em;font-size:.9rem}}
@media (max-width:820px){{main{{grid-template-columns:1fr}}}}
</style></head><body>
<header><h1>Dix jeux de polices</h1><p>Même home, mêmes couleurs, mêmes photos : seules les polices changent. Chaque carte montre le titre, les noms en capitales, un mot en italique et le texte courant. Chaque lien ouvre la home complète avec ce jeu.</p></header>
<main>{cartes}</main></body></html>'''
open(os.path.join(D, 'mockup-polices.html'), 'w').write(page)
print('polices ok')
