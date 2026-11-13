"""Home : lampes détourées autour de « Demandez le programme ! » (section newsletter sur fond blanc).
Détoure les photos de studio de cinq lampes de la pièce, les enregistre dans docs/assets/cutout/ et les place dans la section.
    python3 outils/lampes_lettre.py
"""
import os, re, urllib.request, importlib.util
here=os.path.dirname(os.path.abspath(__file__)); root=os.path.dirname(here)
spec=importlib.util.spec_from_file_location('dt',os.path.join(here,'detourer.py')); D=importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
B='https://res.cloudinary.com/ducsqgqbj/image/upload/f_jpg,q_92,w_800/rotin-boheme/lampes/%s-studio-eteinte.jpg'
# (fichier, lampe Cloudinary, seuil de détourage, côté, position %, décalage vers le haut en px (les lampes ont toutes la même taille, à des niveaux différents), texte alternatif)
L=[('elsa-mandarine','lampe-04-canton-orange',7,'l',4,0,'Elsa Mandarine, lampe à pied de porcelaine et abat-jour orange, détourée'),
   ('dori-morse','lampe-05-blanche-pointilles',7,'l',17,110,'Dori Morse, lampe blanche à abat-jour rayé de pointillés, détourée'),
   ('bob-longcou','lampe-06-bureau-noire',7,'r',4,60,'Bob Longcou, lampe de bureau noire et laiton, détourée'),
   ('lulu-guinguette','lampe-12-frange-fleurs',2.5,'r',16,0,'Lulu Guinguette, lampe à abat-jour fleuri et franges, détourée'),
   ('miss-flower','lampe-13-bois-tourne',7,'r',29,120,'Miss Flower, lampe au pied en bois tourné et abat-jour jungle, détourée')]
out=os.path.join(root,'docs/assets/cutout'); os.makedirs(out,exist_ok=True)
tmp=os.path.join(out,'_tmp.jpg')
for f,src,t,_,_,_,_ in L:
    dst=os.path.join(out,f+'.webp')
    if os.path.exists(dst): continue
    urllib.request.urlretrieve(B%src,tmp); D.detourer(tmp,dst,t)
    from PIL import Image
    im=Image.open(dst)
    if im.height>640: im.resize((round(im.width*640/im.height),640),Image.LANCZOS).save(dst,'WEBP',quality=88,method=6)
if os.path.exists(tmp): os.remove(tmp)
from PIL import Image
imgs=''
for f,_,_,side,pos,b,alt in L:
    w,hh=Image.open(os.path.join(out,f+'.webp')).size
    imgs+=f'<img class="lettre__l lettre__l--{side}" style="--p:{pos}%;--b:{b}px" src="assets/cutout/{f}.webp" alt="" width="{w}" height="{hh}" loading="lazy">'
html=f'<div class="lettre__lampes" aria-hidden="true">{imgs}</div>'
p=os.path.join(root,'docs/index.html'); h=open(p).read()
h=re.sub(r'<div class="lettre__lampes".*?</div>','',h,count=1,flags=re.S)
h,n=re.subn(r'(<section class="lettre" id="lettre">)',lambda m:m.group(1)+html,h,count=1); assert n==1
open(p,'w').write(h); print('lampes ok')
