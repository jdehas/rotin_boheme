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
    <p class="ah__x" data-r>{pc['home']}</p>
    <p class="ah__dist" data-r><b>({len(pc['roles'])})</b> Les lampes à l'affiche</p>
    <div class="noms__stage" data-r>
      <div class="noms__pic noms__pic--l" aria-hidden="true"><img src="" alt=""></div>
      <div class="noms__pic noms__pic--r" aria-hidden="true"><img src="" alt=""></div>
      <ul class="noms__list">{lis}</ul>
    </div>
    <p class="noms__pied" data-r><a class="lien" href="piece-il-est-12h-miss-flower.html">Découvrir la pièce</a> <span class="ah__sep">·</span> <a class="lien" href="lampes.html">Toutes les lampes</a></p>
  </div>
</section>'''
# Section des 4 rubriques, sur fond marine : elle s'intercale entre le héros et l'affiche blanche
arr='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
elsa=par['elsa-mandarine']
RUB=[('lampes.html','Lampes',G.L(elsa['imgs'][0][0],640),'Lampes, Elsa Mandarine'),
     ('meubles.html','Meubles','https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/rotin-boheme/meubles/meuble-01-chevet-corail-studio.jpg','Meubles, chevet corail'),
     ('objets.html','Objets','https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/rotin-boheme/objets/objet-01-pichet-bleu-roses.jpg','Objets, pichet bleu aux roses'),
     ('kids.html','Enfants',G.L('local/kids-07-ours-orange-studio',640),'Enfants, ourson orange')]
cards=''.join(f'<a class="rub__c" href="{u}"><span class="rub__ph"><img src="{i}" alt="{a}" loading="lazy"></span><span class="rub__n">{n}</span></a>' for u,n,i,a in RUB)
MOT=("Je chine des pieds de lampe, des fauteuils et des miroirs qui ont déjà beaucoup servi. Je les habille. Je les maquille parfois. Je leur cherche ensuite le décor où ils brilleront le mieux. Chez Rotin Bohème, chaque pièce reçoit un nom et un rôle\u00a0: c'est ma façon de leur offrir une nouvelle scène.","Bernadette")  # texte de Ginette, version A choisie par John (à faire approuver par Bernadette avant mise en ligne)
mot=f'<section class="sec mdb" id="mot"><div class="wrap"><p class="mdb__t" data-r>{MOT[0]}</p><p class="mdb__sig" data-r>{MOT[1]}</p></div></section>'
rub=f'<section class="sec rub" id="rubriques"><div class="wrap"><div class="rub__g" data-r>{cards}</div></div></section>'
h=open('index.html').read()
h=re.sub(r'<section class="sec rub" id="rubriques">.*?</section>','',h,count=1,flags=re.S)
h=re.sub(r'<section class="sec mdb" id="mot">.*?</section>','',h,count=1,flags=re.S)
h,n=re.subn(r'<section class="sec (?:noms|aff-home)" id="programme">.*?</section>(?=<section class="sec carnet")',lambda m:mot+rub+sec,h,count=1,flags=re.S)
assert n==1
open('index.html','w').write(h); print('home affiche ok')
