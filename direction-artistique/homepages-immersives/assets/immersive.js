/* Comportements discrets : en-tête, révélations, parallaxe, rail, repères, programme, menu. Aucune dépendance. */
(function(){
  var d=document,w=window;d.documentElement.classList.add('js');
  var hdr=d.querySelector('.hdr'),hero=d.querySelector('.hero'),img=d.querySelector('.hero__img');
  var reduit=w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function onScroll(){
    var y=w.scrollY||0,h=hero?hero.offsetHeight:0;
    if(hdr)hdr.classList.toggle('solid',y>h-90);
    if(img&&!reduit&&y<h*1.2)img.style.translate='0 '+(y*0.12).toFixed(1)+'px';
  }
  onScroll();w.addEventListener('scroll',onScroll,{passive:true});

  var els=[].slice.call(d.querySelectorAll('[data-r]'));
  if('IntersectionObserver' in w){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(e){io.observe(e);});
  } else els.forEach(function(e){e.classList.add('in');});

  d.querySelectorAll('.rail-wrap').forEach(function(rw){
    var rail=rw.querySelector('.rail');if(!rail)return;
    rw.querySelectorAll('[data-dir]').forEach(function(b){b.addEventListener('click',function(){rail.scrollBy({left:(+b.dataset.dir)*Math.min(rail.clientWidth*.8,360),behavior:'smooth'});});});
  });

  d.querySelectorAll('.pin').forEach(function(p){p.addEventListener('click',function(e){e.preventDefault();var on=p.classList.contains('on');d.querySelectorAll('.pin.on').forEach(function(x){x.classList.remove('on');});if(!on)p.classList.add('on');});});

  var ap=d.querySelector('.apercu');
  if(ap&&w.matchMedia('(hover:hover)').matches){
    var im=ap.querySelector('img');
    d.querySelectorAll('.prog a').forEach(function(a){
      a.addEventListener('mouseenter',function(){im.src=a.dataset.img;ap.classList.add('on');});
      a.addEventListener('mouseleave',function(){ap.classList.remove('on');});
      a.addEventListener('mousemove',function(e){ap.style.left=(e.clientX+150)+'px';ap.style.top=e.clientY+'px';});
    });
  }

  /* Liste de noms : l'objet et son détail suivent le nom survolé */
  var st=d.querySelector('.noms__stage');
  if(st&&w.matchMedia('(hover:hover)').matches){
    var list=st.querySelector('.noms__list'),L=st.querySelector('.noms__pic--l'),R=st.querySelector('.noms__pic--r');
    var li=L.querySelector('img'),ri=R.querySelector('img');
    function show(a){
      list.classList.add('hov');list.querySelectorAll('a.cur').forEach(function(x){x.classList.remove('cur');});a.classList.add('cur');
      var sr=st.getBoundingClientRect(),ar=a.getBoundingClientRect(),y=(ar.top-sr.top+ar.height/2)+'px';
      var soon=a.dataset.soon;
      L.classList.toggle('is-soon',!!soon);R.classList.toggle('is-soon',!!soon);
      if(!soon){li.src=a.dataset.img;ri.src=a.dataset.img;R.style.setProperty('--o',a.dataset.o);R.style.setProperty('--s',a.dataset.s);}
      L.style.top=y;R.style.top=y;st.classList.add('on');
    }
    function hide(){st.classList.remove('on');list.classList.remove('hov');list.querySelectorAll('a.cur').forEach(function(x){x.classList.remove('cur');});}
    list.querySelectorAll('a').forEach(function(a){
      a.addEventListener('mouseenter',function(){show(a);});
      a.addEventListener('focus',function(){show(a);});
      a.addEventListener('blur',hide);
    });
    list.addEventListener('mouseleave',hide);
  }

  var menu=d.querySelector('.menu'),mb=d.querySelector('.menu-btn'),mc=d.querySelector('.menu-close');
  if(menu&&mb){mb.addEventListener('click',function(){menu.classList.add('open');});if(mc)mc.addEventListener('click',function(){menu.classList.remove('open');});menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){menu.classList.remove('open');});});}
})();
