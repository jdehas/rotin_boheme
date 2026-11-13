"""Génère les sections Meubles, Objets et Kids (collection + une fiche par pièce), avec la même mise en page que les lampes.
Les photos sont lues sur Cloudinary par leur nom : <base>, <base>-studio, <base>-detail-*, etc.
Noms, descriptions et textes viennent de Ginette : les modifier dans SECTIONS ci-dessous, puis relancer :
    python3 outils/generer_lampes.py && python3 outils/generer_sections.py
"""
import os, re, glob, html, importlib.util, sys
here=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location('gl',os.path.join(here,'generer_lampes.py')); G=importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
os.chdir(G.DOCS)
B='https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_%d/rotin-boheme/'
def U(sec,n,w=720): return (B%w)+sec+'/'+n+'.jpg'
SUFFIXES=[('-studio','studio'),('-detail-pieds','détail des pieds'),('-detail-coussin','détail du coussin'),('-detail-pied','détail du pied'),('-detail-assise','détail de l’assise'),('-detail-dossier','détail du dossier'),('-detail-matiere','détail de la matière'),('-detail','détail'),('-detail-1','détail'),('-detail-2','second détail'),('-plateau','sur un plateau'),('-salon-jour','en situation, dans un salon'),('-chambre-jour','en situation, dans une chambre'),('-chambre-enfant-jour','dans une chambre d’enfant'),('-salle-a-manger-jour','dans une salle à manger'),('-entree-jour','dans une entrée'),('-cuisine-jour','dans une cuisine'),('-bureau-jour','sur un bureau')]
# (section, fichier de sortie, titre, nom du menu, base Cloudinary, prénom, nom, étiquette, description courte)
SECTIONS={
 'meubles':('Les meubles','Meubles',[
  ('meuble-01-chevet-corail','À nommer','Chevet corail','table de chevet, laque corail','Une table de chevet couleur corail, sur de petits pieds.'),
  ('meuble-02-fauteuil-rotin-naturel','Honoré','Naturel','fauteuil, rotin et coussin fleuri','Un fauteuil en rotin naturel, son coussin fleuri d’origine conservé.'),
  ('meuble-03-fauteuil-rotin-noir','Doña','Frida K','fauteuil, rotin noir','Un fauteuil de caractère, venu de loin, qui a gardé ses coussins fleuris et son allure de diva.')]),
 'objets':('Les objets','Objets',[
  ('objet-01-pichet-bleu-roses','À nommer','Pichet bleu aux roses','pichet en céramique bleu','Un pichet en céramique bleu, décoré de roses.'),
  ('objet-02-pichet-barbotine-raisins','Mireille','Barbotine','pichet, raisins en relief','Un pichet en barbotine, orné de grappes de raisins en relief.'),
  ('objet-03-miroir-soleil','Ludovic','Soleil','miroir, métal doré','Un miroir soleil en métal doré.'),
  ('objet-04-presentoir-asperges','À nommer','Présentoir aux asperges','présentoir en céramique','Un présentoir décoré d’asperges.'),
  ('objet-05-egouttoir-asperges','À nommer','Égouttoir aux asperges','égouttoir en céramique','Un égouttoir décoré d’asperges.')]),
 'kids':('Enfants','Enfants',[
  ('kids-01-poupee-princesse','À nommer','Poupée princesse','poupée','Une poupée princesse.'),
  ('kids-02-nain','À nommer','Nain','nain de jardin','Un nain coiffé de son bonnet.'),
  ('kids-03-cabane','À nommer','Cabane','cabane pour enfant','Une cabane pour enfant.'),
  ('kids-04-chaise-renard','À nommer','Chaise renard','chaise pour enfant','Une chaise pour enfant, ornée d’un renard.'),
  ('kids-05-table-ronde-osb','À nommer','Table ronde','table ronde pour enfant','Une table ronde pour enfant.'),
  ('kids-06-ours-beige','À nommer','Ours beige','ours en peluche','Un ours beige.'),
  ('kids-07-ours-orange','À nommer','Ours orange','ours en peluche','Un ours orange.'),
  ('kids-08-chaise-menthe','À nommer','Chaise menthe','chaise pour enfant','Une chaise pour enfant, couleur menthe.'),
  ('kids-09-tabouret-pliant','À nommer','Tabouret pliant','tabouret pour enfant','Un tabouret pliant pour enfant.'),
  ('kids-10-locomotive','À nommer','Locomotive','locomotive jouet','Une locomotive jouet.')]),
}
def slugify(t): 
    import unicodedata
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower(); return re.sub(r'[^a-z0-9]+','-',t).strip('-')
# Photos livrées dans le dépôt (docs/assets/photos/), en attendant le dépôt Cloudinary. Ordre : studio d'abord.
# Écartées : les chambres qui contiennent un tableau parodie (marque déposée), voir docs/assets/photos/LISEZMOI.md
LOCAL={
 'kids-08-chaise-menthe':[('kids-08-chaise-menthe-studio','sur fond rose poudré'),('kids-08-chaise-menthe-chambre-matin-v3','dans une chambre d’enfant rose, avec la lampe 13'),('kids-chambre-matin-ours-chaise','dans une chambre d’enfant, avec l’ourson orange et la lampe 13'),('kids-08-chaise-menthe-podium','sur un podium rose'),('kids-08-chaise-menthe-detail-dossier','détail du dossier vissé'),('kids-08-chaise-menthe-detail-pieds','détail des pieds aux bouts blancs')],
 'kids-10-locomotive':[('kids-10-locomotive-studio','sur fond lilas gris'),('kids-10-locomotive-socle','sur un socle lilas'),('kids-10-locomotive-detail-avant','détail de l’avant'),('kids-10-locomotive-detail-panneau','détail du panneau')],
 'kids-07-ours-orange':[('kids-07-ours-orange-studio','sur fond bleu ciel fané'),('kids-chambre-matin-ours-chaise','dans une chambre d’enfant, avec la chaise menthe et la lampe 13'),('kids-07-ours-orange-socle','sur un socle bleu'),('kids-07-ours-orange-detail-visage','détail du visage'),('kids-07-ours-orange-detail-pattes','détail des pattes')],
 'kids-03-cabane':[('kids-03-cabane-studio','sur fond vert amande'),('kids-03-cabane-chambre-matin-v2','dans une chambre d’enfant, le matin'),('kids-03-cabane-detail-interieur','détail de l’intérieur'),('kids-03-cabane-detail-toit','détail du toit')],
 'objet-03-miroir-soleil':[('objet-03-miroir-soleil-studio','sur un mur bleu ciel'),('objet-03-miroir-soleil-detail-miroir','détail du miroir bombé'),('objet-03-miroir-soleil-detail-rayons','détail des rayons en feuilles')],
}
items=[]
for sec,(titre,menu,lst) in SECTIONS.items():
    for base,prenom,nom,tag,desc in lst:
        n=f'{prenom} {nom}'
        imgs=[]
        if G.existe(sec+'/'+base+'-studio') if False else False: pass
        def ex(nm):
            import urllib.request
            try: return urllib.request.urlopen(urllib.request.Request(U(sec,nm,200),method='HEAD'),timeout=10).status==200
            except Exception: return False
        loc=next((v for k,v in LOCAL.items() if base.startswith(k)),None)
        if loc:
            imgs=[('local/'+f,f'{n}, {lab}',None) for f,lab in loc]
            imgs.insert(1,(sec+'/'+base,f'{n}, photo sur fond blanc',None))
            seen={base}
            main=None
        else:
            main=base+'-studio' if ex(base+'-studio') else base
            imgs.append((sec+'/'+main,f'{n}, {tag}',None))
            if main!=base: imgs.append((sec+'/'+base,f'{n}, photo sur fond blanc',None))
            seen={main,base}
        for suf,lab in ([] if loc else SUFFIXES[1:]):
            nm=base+suf
            if nm in seen: continue
            if ex(nm): imgs.append((sec+'/'+nm,f'{n}, {lab}',None)); seen.add(nm)
        slug=f'{sec}-{slugify(n)}' if prenom!='À nommer' else f'{sec}-{slugify(nom)}'
        items.append(dict(sec=sec,slug=slug,file=f'{sec[:-1] if sec.endswith("s") else sec}-{slugify(n if prenom!="À nommer" else nom)}.html',prenom=prenom,nom=nom,tag=tag,desc=desc,meta=f'{n} : {tag}, Rotin Bohème.',imgs=imgs,key=None))
# l'image se construit avec G.L qui préfixe lampes/ : on la contourne en fournissant des chemins relatifs à rotin-boheme/
G.B='https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_%d/rotin-boheme/'
def L2(n,w=900):
    if n.startswith('local/'): return 'assets/photos/'+n[6:]+'.jpg'
    return (G.B%w)+n+'.jpg'
G.L=L2
for it in items: G.LAMPES.append(it)
out={}
for sec,(titre,menu,lst) in SECTIONS.items():
    mine=[x for x in items if x['sec']==sec]
    for i,c in enumerate(mine):
        autres=[mine[(i+j)%len(mine)]['slug'] for j in range(1,min(5,len(mine)))]
        c['pieces']=[('suggestions',autres)]
        c['prix']='Prix à renseigner'
        open(c['file'],'w').write(G.affiche(c))
    cards=''.join(f'<a class="coll__c" href="{c["file"]}"><div class="coll__ph"><img src="{L2(c["imgs"][0][0],640)}" alt="{c["prenom"]} {c["nom"]}, {c["tag"]}" width="640" height="800" loading="lazy"></div><p class="coll__p">{c["prenom"]}</p><h2 class="coll__n">{c["nom"]}</h2></a>' for c in mine)
    secn=f"""<section class="sec coll" id="{sec}"><div class="wrap">
  <p class="fiche__crumb" data-r><a href="index.html">Accueil</a> <span>/</span> {menu}</p>
  <div class="coll__tete" data-r><h1 class="coll__t">{titre}</h1><p class="coll__nb"><b>({len(mine)})</b> pièces uniques</p></div>
  <div class="coll__g" data-r>{cards}</div>
</div></section>"""
    open(f'{sec}.html','w').write(G.page(secn,f'Rotin Bohème · {titre}',f'{titre} de Rotin Bohème : pièces uniques chinées et habillées à la main.'))
    print(sec,len(mine),'pièces',sum(len(c['imgs']) for c in mine),'photos')
# menu : les liens Meubles, Objets, Kids mènent aux collections
for f in glob.glob('*.html'):
    t=open(f).read(); t2=t
    for sec,(titre,menu,_) in SECTIONS.items():
        t2=re.sub(r'<a href="[^"]*">'+menu+'</a>',f'<a href="{sec}.html">{menu}</a>',t2)
    if t2!=t: open(f,'w').write(t2)
print('ok')
