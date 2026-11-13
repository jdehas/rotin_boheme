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
 dict(slug='carol-jouy',prenom='Carol',nom='Jouy',tag='applique murale en toile de Jouy bleue',
  desc="Une applique en demi-cylindre habillée d'une toile de Jouy bleue et crème, aux scènes de chasse et de danse sous les arbres.",
  meta="Carol Jouy : applique murale en toile de Jouy bleue et crème, scènes de chasse sous les arbres.",
  imgs=[('applique-11-toile-bleue-studio-eteinte',"Applique murale en toile de Jouy bleue sur un mur rose poudré, éteinte",'applique-11-toile-bleue-studio-allumee'),
        ('applique-11-toile-bleue-studio-allumee',"La même applique allumée : une lumière chaude déborde en haut et en bas",None),
        ('applique-11-toile-bleue-detail-toile',"Détail de la toile de Jouy : deux chasseurs, des chiens et un grand arbre",None),
        ('applique-11-toile-bleue-detail-passepoil',"Détail du bas de l'applique : toile de Jouy et passepoil bleu",None)]),
 # lampes sans noms ni mises en scène pour l'instant (noms provisoires)
 dict(slug='bois-tourne',auto='lampe-13-bois-tourne',prenom='À nommer',nom='Bois tourné',fiche=False,card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794062832/rotin-boheme/lampes/lampe-13-bois-tourne.jpg',None)),
 dict(slug='geraldine-pistache',auto='lampe-03-canton-verte',prenom='Géraldine',nom='Pistache',fiche=False,card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061934/rotin-boheme/lampes/lampe-03-canton-verte.jpg',None)),
 dict(slug='lea-raphia',auto='lampe-09-raphia-haute',prenom='Léa',nom='Raphia',fiche=False,key='lampe-09-raphia-haute',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061942/rotin-boheme/lampes/lampe-09-raphia-haute.jpg',None)),
 dict(slug='bob-longcou',auto='lampe-06-bureau-noire',prenom='Bob',nom='Longcou',fiche=False,card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061938/rotin-boheme/lampes/lampe-06-bureau-noire.jpg',None)),
 dict(slug='octave-orphiste',prenom='Octave',nom='Orphiste',fiche=False,auto='lampe-01-orphiste-haute',key='lampe-01-orphiste-haute',tag='lampe, pied noir sculpté et abat-jour en tapisserie graphique',desc='Un pied noir sculpté en lobes superposés et un abat-jour en tapisserie aux cercles rouges, noirs, bleus et crème.',meta='Lampe au pied noir sculpté et abat-jour en tapisserie graphique aux cercles colorés.',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061932/rotin-boheme/lampes/lampe-01-orphiste-haute.jpg',None)),
 dict(slug='gaston-patchwork',auto='lampe-08-abstraite-gres',prenom='Gaston',nom='Patchwork',fiche=False,card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061940/rotin-boheme/lampes/lampe-08-abstraite-gres.jpg',None)),
]
# --- Détection automatique des photos mises en scène -------------------------------------------
# Une lampe sans fiche qui a une clé « auto » est promue dès que Cloudinary contient son jeu :
#   <auto>-studio-eteinte et <auto>-studio-allumee (obligatoires), puis -plateau-eteinte/-allumee,
#   une photo d'ambiance (-chambre-jour, -salon-jour, -entree-jour, -bureau-jour...), -detail-abat-jour, -detail-pied.
# La carte de la collection montre alors la photo studio éteinte, et l'allumée au survol.
import urllib.request
AMBIANCES=['chambre-jour','salon-jour','entree-jour','bureau-jour','salle-a-manger-jour','cuisine-jour','bibliotheque-jour']
def existe(nom):
    try: return urllib.request.urlopen(urllib.request.Request(L(nom,200),method='HEAD'),timeout=10).status==200
    except Exception: return False
for c in LAMPES:
    pre=c.get('auto')
    if c.get('imgs') or not pre or not (existe(pre+'-studio-eteinte') and existe(pre+'-studio-allumee')): continue
    n=f"{c['prenom']} {c['nom']}"
    imgs=[(pre+'-studio-eteinte',n+', studio éteinte',pre+'-studio-allumee'),(pre+'-studio-allumee',n+', studio allumée',None)]
    if existe(pre+'-plateau-eteinte') and existe(pre+'-plateau-allumee'):
        imgs+=[(pre+'-plateau-eteinte',n+', sur un plateau, éteinte',pre+'-plateau-allumee'),(pre+'-plateau-allumee',n+', sur un plateau, allumée',None)]
    for a in AMBIANCES:
        if existe(pre+'-'+a): imgs.append((pre+'-'+a,n+', en situation',None)); break
    for suf,lab in (('detail-abat-jour',"détail de l'abat-jour"),('detail-pied','détail du pied')):
        if existe(pre+'-'+suf): imgs.append((pre+'-'+suf,n+', '+lab,None))
    c['imgs']=imgs
    c.setdefault('tag','lampe'); c.setdefault('desc','Description à écrire par Ginette.'); c.setdefault('meta',n+' : lampe de Rotin Bohème.')
    print('photos studio détectées :',n)
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
    assert pat.search(h),c['key']
    href=f'lampe-{c["slug"]}.html' if c.get('imgs') else '\\1'
    h=pat.sub(f'<li><a href="{href}"\\2<span class="t">{c["prenom"]}</span><span class="n">{c["nom"]}</span>',h,1)
open('index.html','w').write(h)
for f in glob.glob('*.html'):
    pass
print('ok',len(LAMPES),'lampes')
