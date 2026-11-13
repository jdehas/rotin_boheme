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
 dict(slug='alizee-canopee',prenom='Alizée',nom='Canopée',fiche=False,auto='lampe-14-alizee-canopee',tag='lampe, pied en cuivre et abat-jour en velours Thévenon',
  desc='Une jungle de singe, de paon et de serpent qui s\'éclaire le soir venu. Seconde vie de premier rôle.',
  meta='Alizée Canopée : pied en cuivre style Hollywood Regency, abat-jour en velours Thévenon Animalia.',
  histoire="""Elle a fait ses débuts dans les années 60, sur un pied de cuivre en éventail de palmes, du genre qu'on ne trouvait que dans les salons où l'on savait recevoir. Puis la mode a changé et on l'a oubliée dans un coin.

Je lui ai offert un nouveau costume : un velours de la maison parisienne Thévenon, motif Animalia. Un singe guette depuis sa branche, un paon fait la roue et un serpent se faufile entre les feuillages. Toute une jungle en noir et blanc, qui s'illumine dès que le soir tombe.

Elle sait tenir la scène. Sur une console, un chevet ou un coin de bibliothèque, elle prend toute la place sans jamais couvrir les autres.""",
  matiere="Pied en cuivre style Hollywood Regency, années 60. Abat-jour en velours de la maison Thévenon, motif « Animalia ».",
  dimensions="Largeur 36 cm\n\nHauteur de l'abat-jour 18 cm\n\nHauteur totale 45 cm",
  card=('assets/heros/alizee-1.jpg',None)),  # repli : photo recadrée tant que le jeu Cloudinary n'existe pas
 dict(slug='lulu-guinguette',prenom='Lulu',nom='Guinguette',tag='lampe, pied blanc et abat-jour fleuri à franges',
  desc='Un pied blanc tout en rondeurs, un abat-jour fleuri bleu ciel et une cascade de franges dorées.',
  meta="Lulu Guinguette : lampe au pied blanc sculpté et abat-jour fleuri à franges dorées.",key='lampe-12-frange-fleurs',
  imgs=[('lampe-12-frange-fleurs-studio-eteinte','Lampe au pied blanc sculpté en rondeurs empilées et abat-jour fleuri bleu ciel à franges dorées, éteinte','lampe-12-frange-fleurs-studio-allumee'),
        ('lampe-12-frange-fleurs-studio-allumee',"La même lampe allumée : l'abat-jour s'illumine et la lumière chaude s'étale sur le sol",None),
        ('lampe-12-frange-fleurs-plateau-eteinte','La lampe sur un plateau patiné, éteinte','lampe-12-frange-fleurs-plateau-allumee'),
        ('lampe-12-frange-fleurs-plateau-allumee','La lampe sur le plateau patiné, allumée',None),
        ('lampe-12-frange-fleurs-chambre-jour-v2',"La lampe sur une malle ancienne à côté d'un lit, dans une chambre aux tentures sauge",None),
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
 dict(slug='miss-flower',auto='lampe-13-bois-tourne',prenom='Miss',nom='Flower',fiche=False,tag='lampe, pied en bois tourné et abat-jour jungle',desc='Un pied en bois tourné patiné, à renflements successifs, et un abat-jour imprimé jungle : feuillages vert émeraude, brique et crème.',meta='Miss Flower : lampe au pied en bois tourné et abat-jour imprimé jungle.',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794062832/rotin-boheme/lampes/lampe-13-bois-tourne.jpg',None)),
 dict(slug='geraldine-pistache',auto='lampe-03-canton-verte',prenom='Géraldine',nom='Pistache',fiche=False,tag='lampe, porcelaine de Canton et abat-jour vert pistache',desc='Un abat-jour vert pistache aux reflets soyeux, une porcelaine peinte de personnages et une monture dorée à trois pieds en griffes.',meta='Géraldine Pistache : lampe en porcelaine de Canton et abat-jour vert pistache.',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061934/rotin-boheme/lampes/lampe-03-canton-verte.jpg',None)),
 dict(slug='lea-raphia',auto='lampe-09-raphia-haute',prenom='Léa',nom='Raphia',fiche=False,tag='lampe, abat-jour en raphia et pied noir',desc='Un très haut abat-jour en raphia tissé naturel sur un pied noir bas, orné d\'une bande en relief doré et vert.',meta='Léa Raphia : lampe à très haut abat-jour en raphia et pied noir.',key='lampe-09-raphia-haute',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061942/rotin-boheme/lampes/lampe-09-raphia-haute.jpg',None)),
 dict(slug='bob-longcou',auto='lampe-06-bureau-noire',prenom='Bob',nom='Longcou',fiche=False,tag='lampe de bureau, réflecteur noir et bras en laiton',desc='Un réflecteur noir mat évasé en cornet, un bras en laiton courbé et une base ronde basse.',meta='Bob Longcou : lampe de bureau au réflecteur noir et bras en laiton.',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061938/rotin-boheme/lampes/lampe-06-bureau-noire.jpg',None)),
 dict(slug='daisy-bell',auto='lampe-02-orphiste-large',prenom='Daisy',nom='Bell',fiche=False,tag='lampe, pied noir sculpté et abat-jour graphique',desc='Un large pied noir sculpté et un abat-jour graphique.',meta='Daisy Bell : lampe au large pied noir sculpté.',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061933/rotin-boheme/lampes/lampe-02-orphiste-large.jpg',None)),
 dict(slug='amin-boubacar',auto='lampe-10-bois-sculpte',prenom='Amin',nom='Boubacar',fiche=False,tag='lampe, pied en bois sculpté',desc='Un pied en bois sculpté foncé, coiffé de son abat-jour.',meta='Amin Boubacar : lampe au pied en bois sculpté.',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061943/rotin-boheme/lampes/lampe-10-bois-sculpte.jpg',None)),
 dict(slug='jelly-bell',prenom='Jelly',nom='Bell',fiche=False,auto='lampe-01-orphiste-haute',key='lampe-01-orphiste-haute',tag='lampe, pied noir sculpté et abat-jour en tapisserie graphique',desc='Un pied noir sculpté en lobes superposés et un abat-jour en tapisserie aux cercles rouges, noirs, bleus et crème.',meta='Lampe au pied noir sculpté et abat-jour en tapisserie graphique aux cercles colorés.',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061932/rotin-boheme/lampes/lampe-01-orphiste-haute.jpg',None)),
 dict(slug='marcel-trapp',auto='lampe-08-abstraite-gres',key='lampe-08-abstraite-gres',prenom='Marcel',nom='Trapp',fiche=False,tag='lampe, pied en grès et abat-jour en tissus assemblés',desc='Un pied de grès brun et un abat-jour en tissus assemblés, aux grands aplats gris, crème et marine.',meta='Marcel Trapp : lampe au pied de grès brun et abat-jour en tissus assemblés.',card=('https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_640/v1794061940/rotin-boheme/lampes/lampe-08-abstraite-gres.jpg',None)),
]
# --- Détection automatique des photos mises en scène -------------------------------------------
# Une lampe sans fiche qui a une clé « auto » est promue dès que Cloudinary contient son jeu :
#   <auto>-studio-eteinte et <auto>-studio-allumee (obligatoires), puis -plateau-eteinte/-allumee,
#   une photo d'ambiance (-chambre-jour, -salon-jour, -entree-jour, -bureau-jour...), -detail-abat-jour, -detail-pied.
# La carte de la collection montre alors la photo studio éteinte, et l'allumée au survol.
import urllib.request
AMBIANCES=['chambre-jour','chambre-nuit','salon-jour','entree-jour','bureau-jour','salle-a-manger-jour','cuisine-doree','cuisine-jour','bibliotheque-jour']
PAIRES=[('arche','sous une arche'),('plateau','sur un plateau'),('socle','sur son socle'),('formica','sur un bureau en formica')]
def existe(nom):
    try: return urllib.request.urlopen(urllib.request.Request(L(nom,200),method='HEAD'),timeout=10).status==200
    except Exception: return False
for c in LAMPES:
    pre=c.get('auto')
    if c.get('imgs') or not pre or not (existe(pre+'-studio-eteinte') and existe(pre+'-studio-allumee')): continue
    n=f"{c['prenom']} {c['nom']}"
    imgs=[(pre+'-studio-eteinte',n+', studio éteinte',pre+'-studio-allumee'),(pre+'-studio-allumee',n+', studio allumée',None)]
    for k,lab in PAIRES:
        if existe(pre+'-'+k+'-eteinte') and existe(pre+'-'+k+'-allumee'):
            imgs+=[(pre+'-'+k+'-eteinte',n+', '+lab+', éteinte',pre+'-'+k+'-allumee'),(pre+'-'+k+'-allumee',n+', '+lab+', allumée',None)]
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
# --- Mise en page « affiche » (essai) : grand écran sans texte, infos dessous -------------------------
# Ordre : nom, courte description, prix, ajouter au panier, matière et état, dimensions, autres photos, rôle, collections.
PIECES={'il-est-12h':'Il est 12h, Miss Flower'}
def carte_piece(slug):
    c=next(x for x in LAMPES if x['slug']==slug)
    if c.get('imgs'): img=L(c['imgs'][0][0],640); href=f"lampe-{slug}.html"
    else: img=c['card'][0]; href='#'
    return f'<a class="coll__c" href="{href}"><div class="coll__ph"><img src="{img}" alt="{c["prenom"]} {c["nom"]}" loading="lazy"></div><p class="coll__p">{c["prenom"]}</p><h3 class="coll__n">{c["nom"]}</h3></a>'
def affiche(c):
    p0,a0_,l0=c['imgs'][0]
    role=paras(c.get('histoire') or 'Histoire à écrire par Ginette avec Bernadette.')
    mat=paras(c.get('matiere') or 'À renseigner.')
    dim=paras(c.get('dimensions') or 'À renseigner.')
    prix=html.escape(c.get('prix') or 'Prix à renseigner',quote=False)
    reste=list(c['imgs'])  # toutes les photos : éteintes et allumées comprises
    gal=''
    for i,(p,a,l) in enumerate(reste):
        gal+=f'<button class="afi__ph" type="button" data-full="{L(p,1800)}" data-alt="{a}" aria-label="Agrandir la photo {i+1}"><img src="{L(p,720)}" alt="{a}" loading="lazy"></button>'
    colls=''
    for cle,membres in c.get('pieces',[]):
        colls+=f'<div class="afi__piece"><h3>{PIECES[cle]}</h3><div class="coll__g afi__cg">'+''.join(carte_piece(m) for m in membres)+'</div></div>'
    sec=f"""<section class="aff" id="fiche">
  <div class="aff__hero" id="hero" role="button" tabindex="0" aria-pressed="false" aria-label="Allumer ou éteindre la lampe"><div class="aff__bg" aria-hidden="true"><i class="l" style="--off:url({L(p0,300)});--on:url({L(l0,300)})"><b></b></i><i class="r" style="--off:url({L(p0,300)});--on:url({L(l0,300)})"><b></b></i></div><div class="aff__fg pair"><img src="{L(p0,1600)}" alt="{a0_}"><img class="pair__on" src="{L(l0,1600)}" alt="" aria-hidden="true"></div></div>
  <div class="afi wrap">
    <div class="afi__main">
      <p class="afi__pre" style="margin-top:0">{c['prenom']}</p>
      <h1 class="afi__nom">{c['nom']}</h1>
      <p class="afi__desc">{c['desc']}</p>
    </div>
    <div class="afi__cols"><div><h2>Matière et état</h2>{mat}</div><div><h2>Dimensions</h2>{dim}</div><div><h2>Prix</h2><p class="afi__prix"><b>{prix}</b></p><p class="afi__uniq">pièce unique</p><div class="fiche__cta" style="margin:0"><a class="btn btn--plein" href="#">Ajouter au panier<span class="ar">{arrow}</span></a></div></div></div>
  </div>
  <div class="afi__gal wrap" style="--n:4">{gal}</div>
  <div class="afi__role wrap"><h2 class="vh">Le rôle</h2>{role}</div>
  <div class="afi__coll wrap"><h2>Collections</h2><p class="afi__sub">Les pièces dans lesquelles {c['prenom']} a joué : les autres lampes avec lesquelles elle s'accorde.</p>{colls}</div>
  <div class="lb" id="lb" hidden><button class="lb__x" type="button" aria-label="Fermer">×</button><button class="lb__p" type="button" aria-label="Photo précédente">‹</button><img id="lbimg" alt=""><button class="lb__n" type="button" aria-label="Photo suivante">›</button></div>
  <script>(function(){{var h=document.getElementById('hero');function tog(){{var on=h.classList.toggle('is-on');h.setAttribute('aria-pressed',on)}}
  if(window.matchMedia('(hover:none)').matches){{h.addEventListener('click',tog)}}h.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();tog()}}}});
  var ph=[].slice.call(document.querySelectorAll('.afi__ph')),lb=document.getElementById('lb'),im=document.getElementById('lbimg'),cur=0;
  function show(i){{cur=(i+ph.length)%ph.length;im.src=ph[cur].dataset.full;im.alt=ph[cur].dataset.alt;lb.hidden=false;document.body.style.overflow='hidden'}}
  function close(){{lb.hidden=true;document.body.style.overflow=''}}
  ph.forEach(function(b,i){{b.addEventListener('click',function(){{show(i)}})}});
  lb.querySelector('.lb__x').onclick=close;lb.querySelector('.lb__p').onclick=function(e){{e.stopPropagation();show(cur-1)}};lb.querySelector('.lb__n').onclick=function(e){{e.stopPropagation();show(cur+1)}};
  lb.addEventListener('click',function(e){{if(e.target===lb||e.target===im)close()}});
  document.addEventListener('keydown',function(e){{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)}});}})();</script>
</section>"""
    return page(sec,f"Rotin Bohème · {c['prenom']} {c['nom']}, essai affiche",c['meta'])
for c in LAMPES:
    if c.get('imgs') and c['slug'] in ('lulu-guinguette',):
        c.setdefault('matiere',"Pied en céramique écrue mate, tournée à la main, avec quelques mouchetures naturelles.\n\nAbat-jour en coton imprimé botanique, frange en viscose moutarde.\n\nCâble textile neuf, douille E14, mise aux normes. Très bon état : une petite trace d'usage sous le pied, conservée.")
        c.setdefault('dimensions',"Hauteur totale : 52 cm\n\nAbat-jour : diamètre 24 cm, hauteur 22 cm\n\nPied : hauteur 30 cm\n\nPoids : 2,4 kg")
        c.setdefault('prix','185 €')
        c.setdefault('pieces',[('il-est-12h',['dori-morse','elsa-mandarine','melville-black','jelly-bell'])])
        open(f"essai-affiche-{c['slug']}.html",'w').write(affiche(c))
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
for c in LAMPES:
    if c.get('imgs') and not c.get('key'):
        pat=re.compile(r'(<li><a href="lampe-'+re.escape(c['slug'])+r'\.html" data-img=")[^"]*(")(.*?<span class="th"><img src=")[^"]*(")',re.S)
        if pat.search(h):
            h=pat.sub(lambda m: m.group(1)+L(c['imgs'][0][0],520)+m.group(2)+m.group(3)+L(c['imgs'][0][0],200)+m.group(4),h,1)
open('index.html','w').write(h)
for f in glob.glob('*.html'):
    pass
print('ok',len(LAMPES),'lampes')
