"""Étend une photo 4:5 en image large (2400 x 1000) d'un seul tenant : pas de superposition ni de cadre.
- 12 % de décor sous la lampe (dernières lignes de la photo prolongées et lissées)
- côtés : les bords de la photo prolongés ligne par ligne, lissés, avec un léger grain
Une seule image par état (éteinte, allumée), à poser en fond pleine largeur (object-fit: cover)."""
import io, urllib.request, numpy as np
from PIL import Image, ImageFilter
W,H=2400,1000
def _blur_axis(a,sigma,axis):
    from PIL import ImageFilter
    # flou gaussien séparable via PIL sur chaque canal
    im=Image.fromarray(np.clip(a,0,255).astype('uint8'))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(sigma))).astype('float32')
def etendre(src_bytes,out_path):
    im=Image.open(io.BytesIO(src_bytes)).convert('RGB')
    ph=int(H*0.88); pw=int(round(ph*im.width/im.height))
    im=im.resize((pw,ph),Image.LANCZOS); a=np.asarray(im).astype('float32')
    # 1) bas : prolonger les 6 dernières lignes, lissées horizontalement
    last=a[-6:].mean(axis=0,keepdims=True)                       # 1 x pw x 3
    last=np.asarray(Image.fromarray(np.clip(np.repeat(last,8,0),0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(14))).astype('float32')[4:5]
    bot=np.repeat(last,H-ph,axis=0)
    # léger assombrissement progressif vers le bas pour que le sol se fonde dans le bas de page
    k=np.linspace(1.0,0.93,H-ph)[:,None,None]
    col=np.concatenate([a,bot*k],axis=0)                          # H x pw x 3
    # 2) côtés : couleur du bord, ligne par ligne, lissée
    def edge(side):
        e=col[:,:8].mean(axis=1) if side=='l' else col[:,-8:].mean(axis=1)   # H x 3
        e=np.asarray(Image.fromarray(np.clip(np.repeat(e[None],8,0),0,255).astype('uint8').transpose(1,0,2)).filter(ImageFilter.GaussianBlur(10))).astype('float32')
        return e[:,4:5] if False else None
    def edge_col(side):
        e=col[:,:8].mean(axis=1) if side=='l' else col[:,-8:].mean(axis=1)   # H x 3
        img=Image.fromarray(np.clip(np.repeat(e[:,None,:],8,1),0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(24))
        return np.asarray(img).astype('float32')[:,4,:]             # H x 3
    el,er=edge_col('l'),edge_col('r')
    side=(W-pw)//2
    canvas=np.zeros((H,W,3),'float32')
    canvas[:,:side]=el[:,None,:]; canvas[:,side+pw:]=er[:,None,:]
    canvas[:,side:side+pw]=col
    # 3) fondu de raccord sur 60 px de chaque côté de la jonction (la photo se fond dans le prolongement)
    f=60
    for i in range(f):
        t=i/f
        # à gauche : de la photo vers la couleur de bord
        canvas[:,side+i]=col[:,i]*t+ (el*(1-t)+col[:,i]*t)*0+ col[:,i]*0 + (el*(1-t))
        canvas[:,side+pw-1-i]=col[:,pw-1-i]*t+er*(1-t)
    # 4) grain très léger pour éviter les bandes, puis léger flou horizontal des seules zones prolongées
    ext=Image.fromarray(np.clip(canvas,0,255).astype('uint8'))
    blur=ext.filter(ImageFilter.GaussianBlur(6))
    mask=Image.new('L',(W,H),0)
    m=np.zeros((H,W),'uint8'); m[:,:side+f//2]=255; m[:,side+pw-f//2:]=255; m[ph:,:]=255
    mask=Image.fromarray(m).filter(ImageFilter.GaussianBlur(20))
    out=Image.composite(blur,ext,mask)
    # grain (tramage) sur toute l'image : casse les marches des dégradés sombres, d'où les stries à 8 bits
    arr=np.asarray(out).astype('float32')
    g=np.random.default_rng(7)
    n=g.normal(0,2.0,(H,W,1))+g.normal(0,0.6,(H,W,3))
    Image.fromarray(np.clip(arr+n,0,255).astype('uint8')).save(out_path,'JPEG',quality=90,subsampling=0,optimize=True,progressive=True)
def depuis_url(url,out_path):
    for t in range(3):
        try:
            data=urllib.request.urlopen(url,timeout=40).read(); break
        except Exception: 
            if t==2: raise
    etendre(data,out_path)
