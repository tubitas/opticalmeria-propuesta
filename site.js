// Cabecera con línea al bajar y aparición suave de bloques. Nada más.
(function(){
  var top=document.getElementById('top');
  var onScroll=function(){top.classList.toggle('scrolled',window.scrollY>8)};
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  var m=document.querySelector('.mmenu');
  if(m){m.addEventListener('toggle',function(){document.documentElement.style.overflow=m.open?'hidden':''});m.addEventListener('click',function(e){if(e.target.closest('a'))m.removeAttribute('open')});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')m.removeAttribute('open')});}

  // optotipo: dial que enfoca
  var dio=document.getElementById('dio');
  if(dio){var rows=document.querySelector('.chart .rows'),out=document.getElementById('dio-out'),ok=document.querySelector('.tune-ok');
    var upd=function(){var v=parseFloat(dio.value);rows.style.setProperty('--b',(Math.abs(v)*3.2).toFixed(2)+'px');
      out.textContent=(v<0?'−':'')+Math.abs(v).toFixed(2).replace('.',',');ok.textContent=v===0?'Así, nítido. En el gabinete lo afinamos lente a lente.':''};
    dio.addEventListener('input',upd);upd();}
  // audífonos: ¿te pasa alguna?
  var q=document.querySelector('.quiz');
  if(q){var qo=q.querySelector('.quiz-out'),tels='<a href="tel:+34950430012">Albox, 950 43 00 12</a> o <a href="tel:+34950134199">Huércal-Overa, 950 13 41 99</a>';
    q.addEventListener('change',function(){var n=q.querySelectorAll('input:checked').length;
      qo.innerHTML=n===0?'Marca las que te suenen.':n===1?'Una sola puede ser cosa de un mal día. Si se repite, ven a vernos.':
        'Con '+n+', merece la pena estudiar tu audición. Llama y te damos hora: '+tels+'.';});}
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){
    document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
})();
