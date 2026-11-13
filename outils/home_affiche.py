"""Home : section « À l'affiche » sur fond blanc. Photo pleine largeur de la pièce, synopsis centré, puis les 5 lampes de la pièce.
Au survol d'un nom : la photo produit à gauche et la photo dans la scène à droite. Au scroll, le nom au centre de l'écran passe à l'orange.
À lancer après generer_lampes.py, generer_sections.py et textes.py :  python3 outils/home_affiche.py
"""
import os, re, importlib.util, html
here=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location('gl',os.path.join(here,'generer_lampes.py')); G=importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
os.chdir(G.DOCS)
pc=G.THEATRE[0]; par={c['slug']:c for c in G.LAMPES}
arrow=G.arrow
lis=''
for sl,role in pc['roles']:
    c=par[sl]; prod=G.L(c['imgs'][0][0],520); scene=G.L('local/midiminuit-focus-'+sl,520)
    lis+=(f'<li><a href="lampe-{sl}.html" data-img="{prod}" data-scene="{scene}"><span class="t">{c["prenom"]}</span><span class="n">{c["nom"]}</span><span class="h">{role}</span>'
          f'<span class="th"><img src="{prod}" alt="" loading="lazy"></span></a></li>')
sec=f'''<section class="sec aff-home" id="programme">
  <figure class="ah__img"><img src="{pc['image']}" alt="{html.escape(pc['image_alt'],quote=True)}" loading="lazy"></figure>
  <div class="wrap ah__body">
    <p class="ah__sup" data-r>À l'affiche</p>
    <h2 class="ah__t" data-r>{pc['titre']}</h2>
    <p class="ah__s" data-r>{pc['sous']}</p>
    <p class="ah__x" data-r>{pc['texte']}</p>
    <p class="ah__dist" data-r><b>({len(pc['roles'])})</b> Les lampes à l'affiche</p>
    <div class="noms__stage" data-r>
      <div class="noms__pic noms__pic--l" aria-hidden="true"><img src="" alt=""></div>
      <div class="noms__pic noms__pic--r" aria-hidden="true"><img src="" alt=""></div>
      <ul class="noms__list">{lis}</ul>
    </div>
    <p class="noms__pied" data-r><a class="lien" href="piece-il-est-12h-miss-flower.html">Découvrir la pièce</a> <span class="ah__sep">·</span> <a class="lien" href="lampes.html">Toutes les lampes</a></p>
  </div>
</section>'''
h=open('index.html').read()
h,n=re.subn(r'<section class="sec (?:noms|aff-home)" id="programme">.*?</section>(?=<section class="sec carnet")',lambda m:sec,h,count=1,flags=re.S)
assert n==1
open('index.html','w').write(h); print('home affiche ok')
