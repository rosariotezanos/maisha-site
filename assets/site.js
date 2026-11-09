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
