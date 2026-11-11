(function(){
  var burger=document.getElementById('burger'), mm=document.getElementById('mobile-menu');
  if(burger&&mm){
    burger.addEventListener('click',function(){var o=mm.hidden;mm.hidden=!o;burger.setAttribute('aria-expanded',String(o));});
    mm.addEventListener('click',function(e){if(e.target.tagName==='A'){mm.hidden=true;burger.setAttribute('aria-expanded','false');}});
  }
  var nl=document.getElementById('nl-form');
  if(nl) nl.addEventListener('submit',function(e){e.preventDefault();document.getElementById('nl-msg').textContent='¡Gracias! Te escribiremos con novedades desde Chile y Kenia.';nl.reset();});
  document.querySelectorAll('form[data-demo]').forEach(function(f){
    f.addEventListener('submit',function(e){e.preventDefault();var m=f.querySelector('.ok-msg');if(m)m.hidden=false;});
  });
  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click',function(){
      var t=b.getAttribute('data-copy'), lbl=b.textContent;
      var done=function(){b.textContent='Copiado';setTimeout(function(){b.textContent=lbl;},1400);};
      try{navigator.clipboard.writeText(t).then(done,function(){done();});}catch(err){done();}
    });
  });
  // Cart badge (shared with the Market page)
  window.maishaCart={
    read:function(){try{return JSON.parse(localStorage.getItem('maisha-cart')||'[]');}catch(e){return [];}},
    write:function(c){try{localStorage.setItem('maisha-cart',JSON.stringify(c));}catch(e){} window.maishaCart.badge(c);},
    badge:function(c){var n=(c||window.maishaCart.read()).reduce(function(a,i){return a+i.q;},0);document.querySelectorAll('[data-cart-count]').forEach(function(el){el.textContent=n;el.hidden=!n;});}
  };
  window.maishaCart.badge();
})();

// Aparición suave de textos y tarjetas al hacer scroll + conteo de cifras
(function(){
  var els=[].slice.call(document.querySelectorAll('[data-reveal]'));
  if(!els.length||!('IntersectionObserver' in window)) return;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function count(b){
    var to=+b.getAttribute('data-count'), suf=b.getAttribute('data-suffix')||'', t0=null, dur=1400;
    if(reduce||!to){return;}
    function step(t){ if(!t0)t0=t; var k=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-k,3);
      b.textContent=Math.round(to*e).toLocaleString('es-CL')+suf; if(k<1) requestAnimationFrame(step); }
    b.textContent='0'+suf; requestAnimationFrame(step);
  }
  function show(el){ if(el.classList.contains('is-in')) return; el.classList.add('is-in');
    el.querySelectorAll('[data-count]').forEach(count); }
  // Lo que ya está en pantalla al cargar se queda visible; solo se anima lo que está más abajo
  var vh=window.innerHeight;
  els.forEach(function(el){ if(el.getBoundingClientRect().top<vh*0.92) el.classList.add('is-in'); });
  document.documentElement.classList.add('reveal-on');
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){ if(en.isIntersecting){ show(en.target); io.unobserve(en.target); } });
  },{rootMargin:'0px 0px -8% 0px',threshold:0.12});
  els.forEach(function(el){ if(!el.classList.contains('is-in')) io.observe(el); });
})();

// Videos: se reproducen dentro de la página en el sitio publicado; si la página está embebida (vista previa), se abren en YouTube
(function(){
  var embedded; try{ embedded = window.self !== window.top; }catch(e){ embedded = true; }
  if(embedded) return;
  document.querySelectorAll('[data-video]').forEach(function(a){
    a.addEventListener('click',function(ev){
      ev.preventDefault();
      var box=a.classList.contains('vcard')?a.querySelector('.vthumb'):a;
      if(box.querySelector('iframe')) return;
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+a.getAttribute('data-video')+'?autoplay=1&rel=0';
      f.title=a.getAttribute('aria-label')||'Video';
      f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen=true;
      box.appendChild(f);
    });
  });
})();
