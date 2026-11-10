// Cabecera con línea al bajar y aparición suave de bloques. Nada más.
(function(){
  var top=document.getElementById('top');
  var onScroll=function(){top.classList.toggle('scrolled',window.scrollY>8)};
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  var m=document.querySelector('.mmenu');
  if(m){m.addEventListener('click',function(e){if(e.target.tagName==='A')m.removeAttribute('open')});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')m.removeAttribute('open')});}
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){
    document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
})();
