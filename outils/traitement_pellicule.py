"""Traitement « pellicule » des images d'ambiance de la home : noirs légèrement relevés, grain, vignettage,
cadre à bords arrondis, bords un peu brûlés (chauds et assombris).
Usage : python3 outils/traitement_pellicule.py source.jpg sortie.jpg [largeur]"""
import sys, numpy as np
from PIL import Image, ImageFilter
def traiter(src,dst,largeur=2000,seed=5):
    im=Image.open(src).convert('RGB')
    if largeur and im.width>largeur: im=im.resize((largeur,round(im.height*largeur/im.width)),Image.LANCZOS)
    a=np.asarray(im).astype('float32'); H,W,_=a.shape
    # 1) noirs relevés et contraste doux
    a=a*0.93+13.0
    # 2) vignettage elliptique
    yy,xx=np.mgrid[0:H,0:W].astype('float32'); nx=(xx-W/2)/(W/2); ny=(yy-H/2)/(H/2)
    v=1.0-0.30*np.clip(nx**2*0.8+ny**2*0.9-0.25,0,1.4)
    a*=v[...,None]
    # 3) cadre à coins arrondis : distance signée à un rectangle arrondi
    m=0.010*W; r=0.028*W
    cx,cy=W/2,H/2; hw,hh=W/2-m-r,H/2-m-r
    dx=np.abs(xx-cx)-hw; dy=np.abs(yy-cy)-hh
    d=np.sqrt(np.maximum(dx,0)**2+np.maximum(dy,0)**2)+np.minimum(np.maximum(dx,dy),0)-r   # <0 dedans
    dehors=np.clip(d/(0.0035*W)+0.5,0,1)                       # 1 = hors cadre (bord net, légèrement adouci)
    brule=np.clip(1.0-(-d)/(0.032*W),0,1)**2*(d<0)            # 1 au bord intérieur, 0 à 3,2 % de la largeur
    # bords brûlés : plus chauds (rouge+, bleu-) et plus sombres
    a[...,0]*=1+0.10*brule; a[...,1]*=1-0.07*brule; a[...,2]*=1-0.38*brule
    a*=(1-0.22*brule)[...,None]
    cadre=np.array([20,16,18],'float32')
    a=a*(1-dehors[...,None])+cadre*dehors[...,None]
    # 4) grain argentique : luminance + un peu de chroma, légèrement adouci
    g=np.random.default_rng(seed)
    n=g.normal(0,1,(H,W,1))*6.0+g.normal(0,1,(H,W,3))*1.6
    n=np.asarray(Image.fromarray(np.clip(n*8+128,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))).astype('float32')
    n=(n-128)/8.0*1.15
    a=a+n*(0.55+0.45*(a.mean(axis=2,keepdims=True)<110))    # un peu plus visible dans les ombres
    Image.fromarray(np.clip(a,0,255).astype('uint8')).save(dst,'JPEG',quality=88,subsampling=0,optimize=True,progressive=True)
if __name__=='__main__':
    traiter(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 2000)
