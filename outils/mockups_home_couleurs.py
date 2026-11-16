"""Les deux mises en page de home avec les palettes B (Velours) et C (Rotin et sauge) :
  mockup-home-1b.html : « Affiche » (polices 5) en Velours
  mockup-home-2c.html : « Courrier » (polices 22) en Rotin et sauge
Les mockups mockup-home-1.html et mockup-home-2.html restent tels quels.
    python3 outils/mockups_home_couleurs.py   (à lancer après mockups_home.py)
"""
import os, re, importlib.util
here = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(os.path.dirname(here), 'docs')
spec = importlib.util.spec_from_file_location('mc', os.path.join(here, 'mockups_couleurs.py')); MC = importlib.util.module_from_spec(spec); spec.loader.exec_module(MC)
for n, k, suf, nom in ((1, 'b', '1b', 'Affiche en Velours'), (2, 'c', '2c', 'Courrier en Rotin et sauge')):
    css = open(os.path.join(D, f'assets/home-{n}.css')).read()
    css = '\n'.join(l.replace('#fff', '#FFFDF9') if ('l2-frame{' in l or 'l2-polaroid{' in l) else l for l in css.split('\n'))
    open(os.path.join(D, f'assets/home-{suf}.css'), 'w').write(MC.recolorer(css, MC.PALETTES[k]))
    h = open(os.path.join(D, f'mockup-home-{n}.html')).read()
    h = h.replace(f'assets/home-{n}.css', f'assets/home-{suf}.css')
    h = re.sub(r'<title>.*?</title>', f'<title>Mockup home {suf} · {nom} · Rotin Bohème</title>', h, count=1, flags=re.S)
    open(os.path.join(D, f'mockup-home-{suf}.html'), 'w').write(h)
print('home couleurs ok')
