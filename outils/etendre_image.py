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
    a=a[:,3:-3]; pw=a.shape[1]            # on écarte 3 px de chaque côté : le bord d'une photo exportée est souvent légèrement faussé
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
    # Le décor d'une photo de studio s'assombrit vers les bords (vignettage). Un prolongement plat créerait une cassure de pente,
    # visible comme une ligne verticale. On prolonge donc la pente du bord, en l'estompant, avec une dérive totale bornée.
    tau=170.0; dmax=14.0
    def derive(cols):
        a_=col[:,cols[0]:cols[1]].mean(axis=1); b_=col[:,cols[2]:cols[3]].mean(axis=1)
        sl=(b_-a_)/abs((cols[2]+cols[3]-cols[0]-cols[1])/2.0)            # variation par pixel, vers l'intérieur
        img=Image.fromarray(np.clip(np.repeat((sl*tau*4+128)[:,None,:],8,1),0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(60))
        d=(np.asarray(img).astype('float32')[:,4,:]-128)/4.0
        return -np.clip(d,-dmax,dmax)                                  # dérive vers l'extérieur
    Dl=derive((0,10,60,130)); Dr=derive((pw-10,pw,pw-130,pw-60)); Dr=Dr
    # côté droit : « vers l'intérieur » = vers la gauche, on inverse la pente mesurée
    sgn=-1.0
    canvas=np.zeros((H,W,3),'float32')
    xl=np.arange(side)[::-1].astype('float32')+1.0
    canvas[:,:side]=el[:,None,:]+Dl[:,None,:]*(1-np.exp(-xl/tau))[None,:,None]
    xr=np.arange(W-side-pw).astype('float32')+1.0
    canvas[:,side+pw:]=er[:,None,:]+Dr[:,None,:]*(1-np.exp(-xr/tau))[None,:,None]
    canvas[:,side:side+pw]=col
    # 3) texture : la photo a son propre bruit (compression, grain) ; le prolongement lisse en est dépourvu, ce qui dessinerait
    #    une césure verticale à la jonction. On lui ajoute donc le même niveau de bruit, mesuré près du bord de la photo.
    ph_gray=col[:ph,:80].mean(axis=2)
    base=np.asarray(Image.fromarray(np.clip(ph_gray,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(2))).astype('float32')
    sigma=float(np.std(ph_gray-base)); sigma=min(max(sigma,0.6),4.0)
    g0=np.random.default_rng(11)
    nz=g0.normal(0,sigma,(H,W,1))*0.9+g0.normal(0,sigma*0.35,(H,W,3))
    nz=np.asarray(Image.fromarray(np.clip(nz*10+128,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))).astype('float32')
    nz=(nz-128)/10.0
    ext_mask=np.zeros((H,W,1),'float32'); ext_mask[:,:side]=1; ext_mask[:,side+pw:]=1; ext_mask[ph:,:]=1
    canvas=canvas+nz*ext_mask
    out=Image.fromarray(np.clip(canvas,0,255).astype('uint8'))
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

def depuis_fichier(chemin,out_path):
    etendre(open(chemin,'rb').read(),out_path)
