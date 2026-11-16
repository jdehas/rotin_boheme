"""Deux mockups de home avec une mise en page nouvelle (couleurs actuelles, mêmes photos et textes).
  mockup-home-1.html : « Affiche », avec les polices Gloock et Figtree (jeu 5)
  mockup-home-2.html : « Courrier », avec les polices Xanh Mono et Hanken Grotesk (jeu 22)
    python3 outils/mockups_home.py
"""
import os, re, html
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(root, 'docs')
index = open(os.path.join(D, 'index.html')).read()
base_css = open(os.path.join(D, 'assets/immersive.css')).read()
# Début de page (en-tête, menu) et pied de page repris de la home actuelle
HEAD = index[:index.index('<main>')]
FOOT = index[index.index('</main>'):]
HEAD = re.sub(r'<meta (?:property="og:|name="twitter:)[^>]*>', '', HEAD)
cdn = 'https://res.cloudinary.com/ducsqgqbj/image/upload/f_auto,q_auto,w_%d/rotin-boheme/'
def L(path, w=700): return (cdn % w) + path + '.jpg'
ARW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

# Distribution dans l'ordre du synopsis
PIECE = [('lulu-guinguette', 'La danseuse', 'Lulu', 'Guinguette', 'lampe-12-frange-fleurs-studio-eteinte'),
         ('dori-morse', 'La télégraphiste', 'Dori', 'Morse', 'lampe-05-blanche-pointilles-studio-eteinte'),
         ('bob-longcou', 'Le guetteur', 'Bob', 'Longcou', 'lampe-06-bureau-noire-studio-eteinte'),
         ('elsa-mandarine', 'Le Soleil', 'Elsa', 'Mandarine', 'lampe-04-canton-orange-studio-eteinte'),
         ('miss-flower', 'La jardinière', 'Miss', 'Flower', 'lampe-13-bois-tourne-studio-eteinte')]
RUB = [('lampes.html', 'Lampes', 14, L('lampes/lampe-04-canton-orange-studio-eteinte', 500)),
       ('meubles.html', 'Meubles', 3, L('meubles/meuble-01-chevet-corail-studio', 500)),
       ('objets.html', 'Objets', 5, L('objets/objet-01-pichet-bleu-roses-studio', 500)),
       ('kids.html', 'Enfants', 10, 'assets/photos/kids-07-ours-orange-studio.jpg')]
MOT = 'Je chine des pieds de lampe, des fauteuils et des miroirs qui ont déjà beaucoup servi. Je les habille. Je les maquille parfois. Je leur cherche ensuite le décor où ils brilleront le mieux. Chez <span class="or">Rotin Bohème</span>, chaque pièce reçoit un nom et un rôle : c’est ma façon de leur offrir une nouvelle scène.'
CARNET = 'Quand j’étais petite, je voulais habiller le monde. Je dessinais des robes pour les chaises et je cousais des histoires aux ourlets des rideaux. Je croyais que tout pouvait devenir autre chose, pour peu qu’on lui en laisse l’occasion.'
SYNOPSIS = 'Un mardi de mai, le soleil a décidé de se coucher à 12 h. À Midiminuit, personne ou presque ne s’en est inquiété : on a sorti les lampes et la fête a commencé.'

# ---------------------------------------------------------------- Mise en page 1 : « Affiche »
CSS1 = r'''
/* Mise en page 1 : Affiche */
:root{--navy:#15213A;--navy2:#1E2D4A;--cream:#EFE8DA;--gold:#D6A65A;--or:#E2621B;--ink:#141414}
.or{color:var(--or)}
.l1-hero{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);min-height:100svh;background:var(--navy);color:var(--cream)}
.l1-hero__t{display:flex;flex-direction:column;justify-content:flex-end;padding:8rem var(--gutter) 3.5rem;gap:1.6rem;text-align:left}
.l1-hero__eb{letter-spacing:.2em;text-transform:uppercase;font-size:.8rem;color:var(--gold);margin:0}
.l1-hero h1{font-family:var(--serif);font-weight:400;font-size:clamp(3rem,6.4vw,6.6rem);line-height:.95;margin:0}
.l1-hero h1 em{font-style:normal;color:var(--or)}
.l1-hero__cta{display:flex;flex-wrap:wrap;gap:.8rem}
.l1-hero__ph{position:relative;overflow:hidden;min-height:60svh}
.l1-hero__ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:78% 50%}
.l1-marq{background:var(--or);color:var(--ink);overflow:hidden;white-space:nowrap;border-block:1px solid rgba(0,0,0,.2)}
.l1-marq span{display:inline-block;padding:.8rem 0;font-family:var(--serif);font-size:clamp(1.3rem,2.2vw,2rem);text-transform:uppercase;letter-spacing:.04em;animation:l1m 34s linear infinite}
@keyframes l1m{to{transform:translateX(-50%)}}
.l1-mot{background:var(--cream);color:var(--ink);padding:var(--section) var(--gutter)}
.l1-mot__g{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:1.5rem;align-items:end}
.l1-mot__t{grid-column:1/10;font-family:var(--serif);font-size:clamp(1.9rem,3.8vw,3.5rem);line-height:1.12;margin:0;text-align:left;text-wrap:balance}
.l1-mot__sig{grid-column:10/13;justify-self:end;text-align:right;border-top:2px solid var(--or);padding-top:1rem;font-size:.9rem;letter-spacing:.18em;text-transform:uppercase;margin:0;align-self:end}
.l1-rub{background:#fff;color:var(--ink);padding:var(--section) var(--gutter)}
.l1-rub__in{max-width:var(--max);margin:0 auto}
.l1-rub__tt{font-size:.8rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(20,20,20,.55);margin:0 0 1.2rem}
.l1-rub a{display:grid;grid-template-columns:4rem minmax(0,1fr) auto 7.5rem 3rem;align-items:center;gap:1.5rem;padding:1.3rem 0;border-top:1px solid rgba(20,20,20,.18);transition:padding .3s}
.l1-rub a:last-child{border-bottom:1px solid rgba(20,20,20,.18)}
.l1-rub__n{font-size:.9rem;color:rgba(20,20,20,.5)}
.l1-rub__nm{font-family:var(--serif);font-size:clamp(2.6rem,7vw,6.4rem);line-height:.95;text-transform:uppercase;transition:color .3s}
.l1-rub__c{font-size:.9rem;color:rgba(20,20,20,.6);white-space:nowrap}
.l1-rub__ph{width:7.5rem;height:5.6rem;border-radius:.8rem;overflow:hidden;background:#F1EDE4}
.l1-rub__ph img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply}
.l1-rub__ar{width:2.6rem;height:2.6rem;border-radius:50%;border:1px solid rgba(20,20,20,.3);display:grid;place-items:center;transition:background .3s}
.l1-rub__ar svg{width:1rem;height:1rem;stroke:currentColor;fill:none;stroke-width:1.6}
.l1-rub a:hover{padding-left:1.2rem}.l1-rub a:hover .l1-rub__nm{color:var(--or)}.l1-rub a:hover .l1-rub__ar{background:var(--ink);color:#fff}
.l1-aff{background:var(--navy);color:var(--cream);padding:var(--section) 0}
.l1-aff__top{max-width:var(--max);margin:0 auto;padding:0 var(--gutter);display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:1.5rem;align-items:end;margin-bottom:2.5rem}
.l1-aff__eb{grid-column:1/-1;font-size:.8rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin:0}
.l1-aff__t{grid-column:1/8;font-family:var(--serif);font-weight:400;font-size:clamp(2.6rem,6vw,5.6rem);line-height:.95;margin:0}
.l1-aff__s{grid-column:9/13;margin:0;line-height:1.6;color:rgba(239,232,218,.8)}
.l1-aff__row{display:flex;gap:1rem;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-left:var(--gutter);padding:0 var(--gutter) 1.5rem;scrollbar-width:thin}
.l1-aff__c{flex:0 0 clamp(15rem,24vw,21rem);scroll-snap-align:start;position:relative;border-radius:1.2rem;overflow:hidden;aspect-ratio:4/5;background:var(--navy2)}
.l1-aff__c img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .8s}
.l1-aff__c:hover img{transform:scale(1.04)}
.l1-aff__c::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(21,33,58,.9),transparent 55%)}
.l1-aff__cap{position:absolute;left:1.1rem;right:1.1rem;bottom:1rem;z-index:1}
.l1-aff__cap small{display:block;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.l1-aff__cap b{display:block;font-family:var(--serif);font-weight:400;font-size:clamp(1.8rem,2.6vw,2.4rem);line-height:1;text-transform:uppercase}
.l1-aff__foot{max-width:var(--max);margin:1rem auto 0;padding:0 var(--gutter)}
.l1-aff__foot a{color:var(--or);border-bottom:1px solid var(--or);padding-bottom:2px}
.l1-car{background:#fff;color:var(--ink);padding:var(--section) var(--gutter)}
.l1-car__g{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:1.5rem;align-items:center}
.l1-car__tx{grid-column:1/7}
.l1-car__tx h2{font-family:var(--serif);font-weight:400;font-size:clamp(2.4rem,5vw,4.6rem);line-height:.98;margin:0 0 1.5rem}
.l1-car__tx h2 em{font-style:normal;color:var(--or)}
.l1-car__tx p{font-size:1.15rem;line-height:1.65;margin:0 0 1.2rem;max-width:34rem}
.l1-car__tx a{color:var(--or);border-bottom:1px solid var(--or);padding-bottom:2px}
.l1-car__ph{grid-column:8/13;border-radius:1.4rem;overflow:hidden;aspect-ratio:4/5;transform:translateY(2.5rem)}
.l1-car__ph img{width:100%;height:100%;object-fit:cover}
.l1-let{background:var(--cream);color:var(--ink);padding:var(--section) var(--gutter)}
.l1-let__g{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:1.5rem;align-items:center}
.l1-let h2{grid-column:1/7;font-family:var(--serif);font-weight:400;font-size:clamp(2.6rem,5.4vw,5rem);line-height:.95;margin:0;text-align:left}
.l1-let__f{grid-column:8/13}
.l1-let__f p{margin:0 0 1rem;color:rgba(20,20,20,.7)}
.l1-let form{display:flex;border:1px solid rgba(20,20,20,.35);border-radius:62.4rem;padding:.3rem .3rem .3rem 1.4rem}
.l1-let input{flex:1;min-width:0;background:transparent;border:0;font:inherit;color:var(--ink)}.l1-let input:focus{outline:none}
.l1-let button{border:0;border-radius:62.4rem;background:var(--ink);color:#fff;padding:.75rem 1.5rem;font:inherit}
@media (max-width:900px){
 .l1-hero{grid-template-columns:1fr}.l1-hero__ph{order:-1;min-height:62svh}.l1-hero__t{padding:2.2rem var(--gutter) 3rem}
 .l1-hero__ph img{object-position:66% 50%}
 .l1-mot__g,.l1-aff__top,.l1-car__g,.l1-let__g{grid-template-columns:1fr;gap:1.2rem}
 .l1-mot__t,.l1-mot__sig,.l1-aff__t,.l1-aff__s,.l1-car__tx,.l1-car__ph,.l1-let h2,.l1-let__f{grid-column:1/-1}
 .l1-mot__sig{justify-self:start;text-align:left;margin-top:1rem}.l1-car__ph{transform:none;margin-top:1.5rem}
 .l1-rub a{grid-template-columns:2.4rem minmax(0,1fr) 5rem;gap:.9rem}.l1-rub__c,.l1-rub__ar{display:none}.l1-rub__ph{width:5rem;height:4rem}
}
'''

def home1():
    marq = ''.join('Lampes · Meubles · Objets · Enfants · Il est 12 h, Miss Flower · ' for _ in range(6))
    rub = ''.join(f'<a href="{u}"><span class="l1-rub__n">0{i}</span><span class="l1-rub__nm">{n}</span><span class="l1-rub__c">{c} pièces</span><span class="l1-rub__ph"><img src="{im}" alt="" loading="lazy"></span><span class="l1-rub__ar">{ARW}</span></a>' for i, (u, n, c, im) in enumerate(RUB, 1))
    cards = ''.join(f'<a class="l1-aff__c" href="lampe-{sl}.html"><img src="assets/photos/midiminuit-focus-{sl}.jpg" alt="{pr} {nm}, {role}, dans la pièce" loading="lazy"><span class="l1-aff__cap"><small>{role}</small><b>{pr} {nm}</b></span></a>' for sl, role, pr, nm, _ in PIECE)
    body = f'''<main>
<section class="l1-hero"><div class="l1-hero__t"><p class="l1-hero__eb">Rotin Bohème</p><h1>Seconde main pour <em>premiers rôles.</em></h1><div class="l1-hero__cta"><a class="btn btn--plein" href="lampes.html">Découvrir les lampes<span class="ar">{ARW}</span></a><a class="btn" href="#affiche">Voir l’affiche<span class="ar">{ARW}</span></a></div></div><div class="l1-hero__ph"><img src="assets/heros/hero-1.jpg" alt="Une roulotte de bois ouverte, éclairée par une guirlande d’ampoules, avec des rideaux rayés, deux fauteuils en rotin et des lampes"></div></section>
<div class="l1-marq" aria-hidden="true"><span>{marq}</span></div>
<section class="l1-mot"><div class="l1-mot__g"><p class="l1-mot__t">{MOT}</p><p class="l1-mot__sig">Bernadette</p></div></section>
<section class="l1-rub"><div class="l1-rub__in"><p class="l1-rub__tt">Entrer par</p>{rub}</div></section>
<section class="l1-aff" id="affiche"><div class="l1-aff__top"><p class="l1-aff__eb">À l’affiche</p><h2 class="l1-aff__t">Il est 12 h, Miss Flower</h2><p class="l1-aff__s">{SYNOPSIS}</p></div><div class="l1-aff__row">{cards}</div><p class="l1-aff__foot"><a href="piece-il-est-12h-miss-flower.html">Découvrir la pièce</a></p></section>
<section class="l1-car" id="atelier"><div class="l1-car__g"><div class="l1-car__tx"><h2>La troupe des <em>objets retrouvés</em></h2><p>{CARNET}</p><p>Ce matin, la troupe a repris la route.</p><a href="a-propos.html">Lire la suite du carnet</a></div><div class="l1-car__ph"><img src="assets/heros/carnet-3.jpg" alt="Dans la roulotte de la troupe : un miroir soleil et une lampe allumée sur sa caisse en bois" loading="lazy"></div></div></section>
<section class="l1-let" id="lettre"><div class="l1-let__g"><h2>Demandez le programme !</h2><div class="l1-let__f"><p>Les pièces qui arrivent à l’atelier et les coulisses de leur seconde vie, dans votre boîte aux lettres.</p><form action="#" onsubmit="return false" aria-label="Inscription au programme"><label class="vh" for="email">Adresse e-mail</label><input id="email" type="email" placeholder="Votre adresse e-mail" autocomplete="email"><button type="submit">Je m’inscris</button></form></div></div></section>
'''
    return body

# ---------------------------------------------------------------- Mise en page 2 : « Courrier »
CSS2 = r'''
/* Mise en page 2 : Courrier */
:root{--navy:#15213A;--navy2:#1E2D4A;--cream:#EFE8DA;--paper:#FBF8F1;--gold:#D6A65A;--or:#E2621B;--ink:#15213A}
.or{color:var(--or)}
.l2{background:var(--cream);color:var(--ink);overflow-x:clip}
.l2 .w{max-width:var(--max);margin:0 auto;padding:0 var(--gutter)}
.l2-hero{padding:8rem 0 4rem}
.l2-hero__top{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:1.5rem;align-items:end;margin-bottom:2rem}
.l2-hero__no{grid-column:1/4;font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(21,33,58,.6);margin:0;align-self:start}
.l2-hero h1{grid-column:1/11;font-family:var(--serif);font-weight:400;font-size:clamp(2.3rem,5.4vw,5rem);line-height:1.05;margin:0;text-align:left}
.l2-hero h1 em{color:var(--or)}
.l2-hero__nav{grid-column:1/-1;display:flex;gap:1.5rem;flex-wrap:wrap;font-size:.95rem}
.l2-hero__nav a{border-bottom:1px solid var(--ink);padding-bottom:2px}
.l2-frame{background:#fff;padding:.7rem;border:1px solid rgba(21,33,58,.25);box-shadow:0 1.5rem 3rem -1.5rem rgba(21,33,58,.35)}
.l2-frame img{display:block;width:100%;height:clamp(22rem,52vw,40rem);object-fit:cover;object-position:78% 50%}
.l2-cap{font-size:.8rem;color:rgba(21,33,58,.65);text-align:right;margin:.8rem 0 0;font-style:italic}
.l2-duo{padding:3rem 0 var(--section);display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:2rem;align-items:start}
.l2-letter{grid-column:1/8;background:var(--paper);padding:clamp(1.8rem,4vw,3.4rem);box-shadow:0 1.2rem 2.6rem -1rem rgba(21,33,58,.3);transform:rotate(-.9deg)}
.l2-letter small{display:block;font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:rgba(21,33,58,.55);margin-bottom:1.4rem}
.l2-letter p{font-family:var(--serif);font-size:clamp(1.15rem,1.9vw,1.55rem);line-height:1.55;margin:0 0 1.5rem}
.l2-letter .sig{font-style:italic;font-size:1.5rem;margin:0}
.l2-som{grid-column:9/13;padding-top:1rem}
.l2-som h2{font-family:var(--serif);font-weight:400;font-size:1.1rem;letter-spacing:.14em;text-transform:uppercase;margin:0 0 1.2rem;color:rgba(21,33,58,.6)}
.l2-som a{display:flex;align-items:baseline;gap:.6rem;padding:.7rem 0;font-family:var(--serif);font-size:clamp(1.4rem,2.4vw,2.1rem)}
.l2-som a i{flex:1;border-bottom:2px dotted rgba(21,33,58,.4);transform:translateY(-.3em)}
.l2-som a span{font-size:1rem}
.l2-som a:hover{color:var(--or)}
.l2-prog{background:var(--navy);color:#EFE8DA;padding:var(--section) 0}
.l2-prog__g{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:2.5rem;align-items:start}
.l2-prog__ph{grid-column:1/7;margin:0}
.l2-prog__ph img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;border:.6rem solid #fff}
.l2-prog__ph figcaption{font-size:.8rem;color:rgba(239,232,218,.7);margin-top:.7rem;font-style:italic}
.l2-prog__tx{grid-column:8/13}
.l2-prog__tx small{font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.l2-prog__tx h2{font-family:var(--serif);font-weight:400;font-size:clamp(2rem,3.6vw,3.2rem);line-height:1.05;margin:.6rem 0 1rem;text-align:left}
.l2-prog__tx p{line-height:1.65;color:rgba(239,232,218,.85)}
.l2-dist{margin:1.8rem 0}
.l2-dist a{display:flex;align-items:center;gap:.9rem;padding:.55rem 0}
.l2-dist img{width:3rem;height:3rem;border-radius:50%;object-fit:cover;flex:none}
.l2-dist b{font-family:var(--serif);font-weight:400;font-size:1.15rem}
.l2-dist i{flex:1;border-bottom:2px dotted rgba(239,232,218,.4);transform:translateY(.2em)}
.l2-dist span{font-size:.85rem;color:var(--gold);text-align:right}
.l2-dist a:hover b{color:var(--or)}
.l2-prog__tx .go{color:var(--or);border-bottom:1px solid var(--or);padding-bottom:2px}
.l2-col{padding:var(--section) 0}
.l2-col h2{font-family:var(--serif);font-weight:400;font-size:clamp(1.8rem,3vw,2.6rem);margin:0 0 2rem;text-align:left}
.l2-col__g{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:1.2rem;align-items:start}
.l2-col__c:nth-child(even){margin-top:3.2rem}
.l2-col__c .im{display:block;aspect-ratio:4/5;background:#E9E0CE;border-radius:.3rem;overflow:hidden}
.l2-col__c img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply;transition:transform .8s}
.l2-col__c:hover img{transform:scale(1.05)}
.l2-col__c small{display:block;margin-top:.7rem;font-size:.75rem;letter-spacing:.14em;color:rgba(21,33,58,.55)}
.l2-col__c b{display:block;font-family:var(--serif);font-weight:400;font-size:1.25rem;line-height:1.1}
.l2-car{padding:0 0 var(--section)}
.l2-car__g{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:2rem;align-items:center}
.l2-car__tx{grid-column:1/7}
.l2-car__tx h2{font-family:var(--serif);font-weight:400;font-size:clamp(2rem,4vw,3.6rem);line-height:1.05;margin:0 0 1.2rem;text-align:left}
.l2-car__tx p{font-size:1.1rem;line-height:1.7;margin:0 0 1rem;max-width:34rem}
.l2-car__tx a{color:var(--or);border-bottom:1px solid var(--or);padding-bottom:2px}
.l2-polaroid{grid-column:8/12;background:#fff;padding:.9rem .9rem 3.2rem;box-shadow:0 1.4rem 2.6rem -1rem rgba(21,33,58,.4);transform:rotate(2.2deg);margin:0}
.l2-polaroid img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.l2-polaroid figcaption{position:absolute}
.l2-polaroid{position:relative}.l2-polaroid figcaption{left:0;right:0;bottom:.9rem;text-align:center;font-style:italic;font-size:.95rem}
.l2-let{background:var(--navy);color:#EFE8DA;padding:var(--section) 0}
.l2-let__in{max-width:44rem}
.l2-let h2{font-family:var(--serif);font-weight:400;font-size:clamp(2rem,4vw,3.4rem);line-height:1.1;margin:0 0 1rem;text-align:left}
.l2-let p{line-height:1.7;color:rgba(239,232,218,.85);margin:0 0 1.4rem}
.l2-let form{display:flex;border-bottom:2px solid #EFE8DA;max-width:30rem;padding-bottom:.4rem}
.l2-let input{flex:1;min-width:0;background:transparent;border:0;font:inherit;color:#EFE8DA}.l2-let input::placeholder{color:rgba(239,232,218,.6)}.l2-let input:focus{outline:none}
.l2-let button{background:none;border:0;color:var(--gold);font:inherit;cursor:pointer;border-bottom:0}
@media (max-width:900px){
 .l2-hero{padding-top:6.5rem}.l2-hero__no,.l2-hero h1{grid-column:1/-1}
 .l2-hero__top,.l2-duo,.l2-prog__g,.l2-car__g{grid-template-columns:1fr;gap:1.4rem}
 .l2-letter,.l2-som,.l2-prog__ph,.l2-prog__tx,.l2-car__tx,.l2-polaroid{grid-column:1/-1}
 .l2-polaroid{max-width:18rem;margin:1.5rem auto 0}
 .l2-col__g{grid-template-columns:repeat(2,minmax(0,1fr))}.l2-col__c:nth-child(even){margin-top:1.6rem}
}
'''

def home2():
    som = ''.join(f'<a href="{u}">{n}<i></i><span>{c}</span></a>' for u, n, c, _ in RUB)
    dist = ''.join(f'<a href="lampe-{sl}.html"><img src="assets/photos/midiminuit-focus-{sl}.jpg" alt=""><b>{pr} {nm}</b><i></i><span>{role}</span></a>' for sl, role, pr, nm, _ in PIECE)
    col = ''.join(f'<a class="l2-col__c" href="lampe-{sl}.html"><span class="im"><img src="{L("lampes/" + im, 600)}" alt="{pr} {nm}" loading="lazy"></span><small>N° 0{i}</small><b>{pr} {nm}</b></a>' for i, (sl, role, pr, nm, im) in enumerate(PIECE, 1))
    body = f'''<main class="l2">
<section class="l2-hero"><div class="w"><div class="l2-hero__top"><p class="l2-hero__no">N° 12 · Rotin Bohème</p><h1>Seconde main pour <em>premiers rôles.</em></h1><div class="l2-hero__nav"><a href="lampes.html">Lampes</a><a href="meubles.html">Meubles</a><a href="objets.html">Objets</a><a href="kids.html">Enfants</a></div></div>
<div class="l2-frame"><img src="assets/heros/hero-1.jpg" alt="Une roulotte de bois ouverte, éclairée par une guirlande d’ampoules, avec des rideaux rayés, deux fauteuils en rotin et des lampes"></div><p class="l2-cap">Fig. 1 : la roulotte de la troupe, à la tombée de la nuit.</p></div></section>
<div class="w"><section class="l2-duo"><article class="l2-letter"><small>Midiminuit, un mardi de mai</small><p>{MOT}</p><p class="sig">Bernadette</p></article><nav class="l2-som" aria-label="Sommaire"><h2>Sommaire</h2>{som}</nav></section></div>
<section class="l2-prog" id="affiche"><div class="w l2-prog__g"><figure class="l2-prog__ph"><img src="assets/heros/midiminuit.jpg" alt="Un appartement à midi, le ciel déjà étoilé, avec les cinq lampes de la pièce" loading="lazy"><figcaption>Fig. 2 : l’appartement de Midiminuit, à midi.</figcaption></figure><div class="l2-prog__tx"><small>À l’affiche</small><h2>Il est 12 h, Miss Flower</h2><p>{SYNOPSIS}</p><div class="l2-dist">{dist}</div><a class="go" href="piece-il-est-12h-miss-flower.html">Découvrir la pièce</a></div></div></section>
<section class="l2-col"><div class="w"><h2>Les premiers rôles</h2><div class="l2-col__g">{col}</div></div></section>
<section class="l2-car" id="atelier"><div class="w l2-car__g"><div class="l2-car__tx"><h2>La troupe des objets retrouvés</h2><p>{CARNET}</p><p>Ce matin, la troupe a repris la route.</p><a href="a-propos.html">Lire la suite du carnet</a></div><figure class="l2-polaroid"><img src="assets/heros/carnet-3.jpg" alt="Dans la roulotte de la troupe : un miroir soleil et une lampe allumée sur sa caisse en bois" loading="lazy"><figcaption>Dans la roulotte.</figcaption></figure></div></section>
<section class="l2-let" id="lettre"><div class="w"><div class="l2-let__in"><h2>Cher lecteur, demandez le programme.</h2><p>Les pièces qui arrivent à l’atelier et les coulisses de leur seconde vie, dans votre boîte aux lettres.</p><form action="#" onsubmit="return false" aria-label="Inscription au programme"><label class="vh" for="email">Adresse e-mail</label><input id="email" type="email" placeholder="Votre adresse e-mail" autocomplete="email"><button type="submit">Je m’inscris →</button></form></div></div></section>
'''
    return body

SETS = [
 (1, 'Gloock', 'Figtree', 'Gloock', 'Figtree:wght@400;500;600', False, CSS1, home1, 'Affiche'),
 (2, 'Xanh Mono', 'Hanken Grotesk', 'Xanh+Mono:ital@0;1', 'Hanken+Grotesk:wght@400;500;600', True, CSS2, home2, 'Courrier'),
]
for n, ser, sans, hs, hx, ital, css, fn, nom in SETS:
    c = base_css.replace('Instrument Serif', ser).replace('Instrument Sans', sans).replace('Bricolage Grotesque', sans)
    if not ital: c += '\n*{font-synthesis:none}em,i{font-style:normal}\n'
    open(os.path.join(D, f'assets/home-{n}.css'), 'w').write(c + css)
    h = HEAD.replace('assets/immersive.css', f'assets/home-{n}.css')
    h = re.sub(r'(https://fonts\.googleapis\.com/css2\?family=)[^"]*', lambda m: m.group(1) + hs + '&family=' + hx + '&display=swap', h, count=1)
    h = re.sub(r'<title>.*?</title>', f'<title>Mockup home {n} · {nom} · Rotin Bohème</title>', h, count=1, flags=re.S)
    open(os.path.join(D, f'mockup-home-{n}.html'), 'w').write(h + fn() + FOOT)
print('home ok')
