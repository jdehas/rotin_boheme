"""Détoure une lampe photographiée sur fond uni (studio) : le fond est repéré en partant des bords de l'image,
en suivant les dégradés doux et en s'arrêtant au contour de l'objet. Sortie : WebP transparent, recadré.
    python3 outils/detourer.py <image.jpg> <sortie.webp> [seuil]
"""
import sys, collections
import numpy as np
from PIL import Image, ImageFilter

def detourer(src, dst, seuil=7.0):
    im = Image.open(src).convert('RGB')
    a = np.asarray(im).astype(np.int32)
    h, w, _ = a.shape
    bg = np.zeros((h, w), bool)
    q = collections.deque()
    for x in range(w):
        for y in (0, h - 1):
            bg[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if not bg[y, x]: bg[y, x] = True; q.append((y, x))
    s2 = seuil * seuil
    while q:
        y, x = q.popleft()
        c = a[y, x]
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not bg[ny, nx]:
                d = a[ny, nx] - c
                if int(d[0] * d[0] + d[1] * d[1] + d[2] * d[2]) <= s2:
                    bg[ny, nx] = True; q.append((ny, nx))
    fg = ~bg
    m = Image.fromarray((fg * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MedianFilter(5))              # retire les poussières
    m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))  # contour doux, sans liseré de fond
    arr = np.asarray(m)
    # ne garde que la plus grande forme : l'objet, sans reflets ni miettes
    lab = (arr > 127)
    seen = np.zeros_like(lab); best = []
    ys, xs = np.nonzero(lab)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]: continue
        comp = []; seen[y0, x0] = True; qq = collections.deque([(y0, x0)])
        while qq:
            y, x = qq.popleft(); comp.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and lab[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; qq.append((ny, nx))
        if len(comp) > len(best): best = comp
    keep = np.zeros_like(lab)
    for y, x in best: keep[y, x] = True
    keepm = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    alpha = np.minimum(arr, np.asarray(keepm)).astype(np.uint8)
    out = im.convert('RGBA'); out.putalpha(Image.fromarray(alpha))
    out = out.crop(out.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
    out.save(dst, 'WEBP', quality=88, method=6)
    return out.size

if __name__ == '__main__':
    print(detourer(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 7.0))
