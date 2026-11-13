"""Génère la collection Lampes et les fiches lampes du site (dossier docs/).
Les noms, histoires et textes viennent de Ginette : les modifier dans LAMPES ci-dessous, puis relancer :
    python3 outils/generer_lampes.py

Champs facultatifs d'une lampe, tous fournis par Ginette :
    histoire    texte de l'onglet « Le rôle » (paragraphes séparés par une ligne vide)
    matiere     texte de l'onglet « Matière et état »
    dimensions  texte de l'onglet « Dimensions »
    prix        prix affiché sous le nom
    valide      True quand les textes sont validés par John (retire la mention « Texte provisoire »)
Sans valeur, la fiche garde les mentions provisoires.
"""
import re, os, glob, html
DOCS=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs')
os.chdir(DOCS)
B='https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_%d/rotin-boheme/lampes/'
def L(n,w=900): return (B%w)+n+'.jpg'
def paras(t): return ''.join('<p>'+html.escape(p.strip(),quote=False)+'</p>' for p in t.strip().split('\n\n') if p.strip())

# Lampes mises en scène : noms validés dans la base Notion « Rotin Bohème, passations de Ginette »
def jeu(prefixe,studio,plateau,ambiance,alts):
    return [
     (prefixe+'-studio-eteinte',alts['studio_off'],prefixe+'-studio-allumee'),
     (prefixe+'-studio-allumee',alts['studio_on'],None),
     (prefixe+'-plateau-eteinte',alts['plateau_off'],prefixe+'-plateau-allumee'),
     (prefixe+'-plateau-allumee',alts['plateau_on'],None),
     (prefixe+'-'+ambiance[0],ambiance[1],None),
     (prefixe+'-detail-abat-jour',alts['abat'],None),
     (prefixe+'-detail-pied',alts['pied'],None)]
LAMPES=[
 dict(slug='alizee-canopee',prenom='Alizée',nom='Canopée',fiche=False,card=('assets/heros/alizee-1.jpg',None)),  # fiche écrite à la main
 dict(slug='lulu-guinguette',prenom='Lulu',nom='Guinguette',tag='lampe, pied blanc et abat-jour fleuri à franges',
  desc='Un pied blanc tout en rondeurs, un abat-jour fleuri bleu ciel et une cascade de franges dorées.',
  meta="Lulu Guinguette : lampe au pied blanc sculpté et abat-jour fleuri à franges dorées.",key='lampe-12-frange-fleurs',
  imgs=[('lampe-12-frange-fleurs-studio-eteinte','Lampe au pied blanc sculpté en rondeurs empilées et abat-jour fleuri bleu ciel à franges dorées, éteinte','lampe-12-frange-fleurs-studio-allumee'),
        ('lampe-12-frange-fleurs-studio-allumee',"La même lampe allumée : l'abat-jour s'illumine et la lumière chaude s'étale sur le sol",None),
        ('lampe-12-frange-fleurs-chambre-jour',"La lampe sur une malle ancienne à côté d'un lit, dans une chambre aux murs rosés",None),
        ('lampe-12-frange-fleurs-detail-abat-jour',"Détail de l'abat-jour : fleurs roses et feuillages sur fond bleu ciel, franges dorées",None),
        ('lampe-12-frange-fleurs-detail-pied','Détail du pied blanc, des rondeurs empilées',None)]),
 dict(slug='dori-morse',prenom='Dori',nom='Morse',tag='lampe, pied blanc et abat-jour à pointillés',
  desc="Un pied blanc en forme d'amphore et un haut abat-jour blanc rythmé de lignes et de pointillés noirs.",
  meta='Dori Morse : lampe au pied blanc en amphore et haut abat-jour blanc à lignes et pointillés noirs.',key='lampe-05-blanche-pointilles',
  imgs=jeu('lampe-05-blanche-pointilles',0,0,('salon-jour',"La lampe sur une table de bois dans un salon aux murs verts, près d'un fauteuil en rotin"),
   dict(studio_off='Lampe blanche : pied en amphore et haut abat-jour à lignes et pointillés noirs, éteinte, sur fond bleu nuit',studio_on="La même lampe allumée : l'abat-jour s'éclaire d'une lumière chaude",
        plateau_off='La lampe posée sur un plateau de travertin, éteinte',plateau_on='La lampe sur le plateau de travertin, allumée',
        abat="Détail de l'abat-jour : lignes et pointillés noirs sur fond blanc",pied='Détail du pied blanc en amphore'))),
 dict(slug='elsa-mandarine',prenom='Elsa',nom='Mandarine',tag="lampe, porcelaine de Canton et abat-jour orange",
  desc="Un pied en porcelaine de Canton peint de scènes et un abat-jour orange mandarine.",
  meta="Elsa Mandarine : lampe en porcelaine de Canton avec abat-jour orange.",key='lampe-04-canton-orange',
  imgs=jeu('lampe-04-canton-orange',0,0,('bureau-jour','La lampe posée sur un bureau, à la lumière du jour'),
   dict(studio_off='Lampe en porcelaine de Canton et abat-jour orange, éteinte, sur fond crème',studio_on='La même lampe allumée : l\'abat-jour orange rayonne',
        plateau_off='La lampe sur un plateau de pierre, éteinte',plateau_on='La lampe sur le plateau de pierre, allumée',
        abat="Détail de l'abat-jour orange",pied='Détail du pied en porcelaine de Canton'))),
 dict(slug='melville-black',prenom='Melville',nom='Black',tag='lampe, pied bleu nuit et abat-jour en toile jungle',
  desc="Un pied bleu nuit à long col et un abat-jour en toile jungle blanche et marine.",
  meta="Melville Black : lampe au pied bleu nuit et abat-jour en toile jungle.",key='lampe-07-toile-jungle',
  imgs=jeu('lampe-07-toile-jungle',0,0,('entree-jour','La lampe sur une console dans une entrée crème, entre tentures blanc cassé et bleu nuit'),
   dict(studio_off='Lampe au pied bleu nuit et abat-jour en toile jungle, éteinte, sur fond lin',studio_on='La même lampe allumée',
        plateau_off='La lampe sur un plateau de pierre, éteinte',plateau_on='La lampe sur le plateau de pierre, allumée',
        abat="Détail de l'abat-jour en toile jungle",pied='Détail du pied bleu nuit'))),
 # lampes sans noms ni mises en scène pour l'instant (noms provisoires)
 dict(slug='lea-raphia',prenom='Léa',nom='Raphia',fiche=False,key='lampe-09-raphia-haute',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061942/rotin-boheme/lampes/lampe-09-raphia-haute.jpg',None)),
 dict(slug='jelly-bell',prenom='Jelly',nom='Bell',fiche=False,key='lampe-01-orphiste-haute',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061932/rotin-boheme/lampes/lampe-01-orphiste-haute.jpg',None)),
 dict(slug='marcel-trapp',prenom='Marcel',nom='Trapp',fiche=False,key='lampe-08-abstraite-gres',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061940/rotin-boheme/lampes/lampe-08-abstraite-gres.jpg',None)),
 dict(slug='carol-jouy',prenom='Carol',nom='Jouy',fiche=False,key='applique-11-toile-bleue',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/rotin-boheme/lampes/applique-11-toile-bleue.jpg',None)),  # applique murale en toile de Jouy bleue
 dict(slug='miss-flower',prenom='Miss',nom='Flower',fiche=False,key='lampe-13-bois-tourne',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/rotin-boheme/lampes/lampe-13-bois-tourne.jpg',None)),
 dict(slug='daisy-bell',prenom='Daisy',nom='Bell',fiche=False,key='lampe-02-orphiste-large',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/rotin-boheme/lampes/lampe-02-orphiste-large.jpg',None)),
 dict(slug='amin-boubacar',prenom='Amin',nom='Boubacar',fiche=False,key='lampe-10-bois-sculpte',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/rotin-boheme/lampes/lampe-10-bois-sculpte.jpg',None)),
]
shell=open('lampe-alizee-canopee.html').read()
arrow=re.search(r'class="btn btn--plein" href="#">Ajouter au panier<span class="ar">(.*?)</span></a>',shell,re.S).group(1)
a0=shell.index('<section class="sec fiche fiche--page"'); b0=shell.index('</section>',a0)+len('</section>')
def page(sec,title,meta):
    o=shell[:a0]+sec+shell[b0:]
    o=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',o,1)
    return re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{meta}">',o,1)
def fiche(c):
    th=''.join(f'<button class="fiche__t" type="button" data-full="{L(p)}" data-alt="{a}"'+(f' data-lit="{L(l)}"' if l else '')+f' aria-label="Voir la photo {i+1}"'+(' aria-current="true"' if i==0 else '')+f'><img src="{L(p,200)}" alt="" loading="lazy" width="200" height="250"></button>' for i,(p,a,l) in enumerate(c['imgs']))
    p0,a0_,l0=c['imgs'][0]
    prov='' if c.get('valide') else '<span class="vh"> Texte provisoire.</span>'
    prix=html.escape(c.get('prix') or 'Prix à renseigner',quote=False)
    role=paras(c.get('histoire') or 'Histoire à écrire par Ginette avec Bernadette.')
    mat=paras(c.get('matiere') or 'À renseigner.')
    dim=paras(c.get('dimensions') or 'À renseigner.')
    sec=f'''<section class="sec fiche fiche--page" id="fiche"><div class="wrap">
  <p class="fiche__crumb" data-r><a href="index.html">Accueil</a> <span>/</span> <a href="lampes.html">Lampes</a> <span>/</span> {c['prenom']} {c['nom']}</p>
  <div class="fiche__g">
  <div class="fiche__img" data-r>
    <div class="fiche__main fiche__main--ph" id="fbox" data-base="0"><img id="fmain" src="{L(p0)}" alt="{a0_}" width="928" height="1152"><img class="fiche__hover" id="fhover" src="{L(l0)}" alt="" aria-hidden="true" width="928" height="1152"></div>
    <div class="fiche__thumbs" style="--n:{len(c['imgs'])}">{th}</div>
  </div>
  <div class="fiche__txt" data-r>
    <p class="eyebrow">Il est 20h, Miss Flower · rôle de la troupe</p>
    <p class="fiche__prenom">{c['prenom']}</p>
    <h2 class="fiche__nom">{c['nom']}</h2>
    <p class="fiche__tag">{c['tag']}</p>
    <p class="fiche__prix"><b>{prix}</b> · pièce unique</p>
    <p class="fiche__desc">{c['desc']}{prov}</p>
    <div class="fiche__cta"><a class="btn btn--plein" href="#">Ajouter au panier<span class="ar">{arrow}</span></a><a class="btn" href="index.html#programme">Voir toute la troupe<span class="ar">{arrow}</span></a></div>
    <div class="fiche__acc">
      <details open><summary>Le rôle</summary>{role}</details>
      <details><summary>Matière et état</summary>{mat}</details>
      <details><summary>Dimensions</summary>{dim}</details>
    </div>
  </div></div></div>
  <script>(function(){{var box=document.getElementById('fbox'),m=document.getElementById('fmain'),h=document.getElementById('fhover'),ts=document.querySelectorAll('.fiche__t');ts.forEach(function(b){{b.addEventListener('click',function(){{m.src=b.dataset.full;m.alt=b.dataset.alt;if(b.dataset.lit){{h.src=b.dataset.lit;box.dataset.base='0'}}else{{box.dataset.base='1'}}box.classList.remove('is-on');ts.forEach(function(x){{x.removeAttribute('aria-current')}});b.setAttribute('aria-current','true')}})}});if(window.matchMedia('(hover:none)').matches){{box.addEventListener('click',function(){{if(box.dataset.base==='0')box.classList.toggle('is-on')}})}}}})();</script></section>'''
    return page(sec,f"Rotin Bohème · {c['prenom']} {c['nom']}, lampe",c['meta'])
# fiches
for f in glob.glob('lampe-*.html'):
    if f!='lampe-alizee-canopee.html': os.remove(f)
for c in LAMPES:
    if c.get('imgs'): open(f"lampe-{c['slug']}.html",'w').write(fiche(c))
# collection
cards=''
for c in LAMPES:
    href=f"lampe-{c['slug']}.html" if (c.get('imgs') or c['slug']=='alizee-canopee') else '#'
    if c.get('imgs'):
        off,alt,lit=c['imgs'][0]
        ph=f'<img src="{L(off,640)}" alt="{c["prenom"]} {c["nom"]}, {c["tag"]}" width="640" height="800" loading="lazy"><img class="coll__lit" src="{L(lit,640)}" alt="" aria-hidden="true" width="640" height="800" loading="lazy">'; cl='coll__c coll__c--lit'
    else:
        ph=f'<img src="{c["card"][0]}" alt="{c["prenom"]} {c["nom"]}" width="640" height="800" loading="lazy">'; cl='coll__c'
    cards+=f'<a class="{cl}" href="{href}"><div class="coll__ph">{ph}</div><p class="coll__p">{c["prenom"]}</p><h2 class="coll__n">{c["nom"]}</h2></a>'
js='''<script>(function(){var c=document.querySelectorAll('.coll__c--lit');if(!('IntersectionObserver' in window)||!window.matchMedia('(hover:none)').matches){return}var io=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('is-lit',e.isIntersecting)})},{rootMargin:'-38% 0px -38% 0px'});c.forEach(function(x){io.observe(x)})})();</script>'''
sec=f'''<section class="sec coll" id="lampes"><div class="wrap">
  <p class="fiche__crumb" data-r><a href="index.html">Accueil</a> <span>/</span> Lampes</p>
  <div class="coll__tete" data-r><h1 class="coll__t">Les lampes</h1><p class="coll__nb"><b>({len(LAMPES)})</b> pièces uniques</p></div>
  <div class="coll__g" data-r>{cards}</div>
</div>{js}</section>'''
open('lampes.html','w').write(page(sec,'Rotin Bohème · Les lampes','Les lampes de Rotin Bohème : pièces uniques chinées et habillées à la main.'))
# affiche de la home : noms et liens des lampes à fiche
h=open('index.html').read()
for c in LAMPES:
    if not c.get('key'): continue
    pat=re.compile(r'<li><a href="([^"]*)"( data-img="[^"]*'+re.escape(c['key'])+r'\.jpg"[^>]*>)<span class="t">[^<]*</span><span class="n">[^<]*</span>')
    if not pat.search(h):
        assert not c.get('imgs'),c['key']  # une lampe sans entrée dans l'affiche de la home reste dans la collection seulement
        continue
    href=f'lampe-{c["slug"]}.html' if c.get('imgs') else '\\1'
    h=pat.sub(f'<li><a href="{href}"\\2<span class="t">{c["prenom"]}</span><span class="n">{c["nom"]}</span>',h,1)
open('index.html','w').write(h)
for f in glob.glob('*.html'):
    pass
print('ok',len(LAMPES),'lampes')
