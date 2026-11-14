// Cabecera con línea al bajar y aparición suave de bloques. Nada más.
(function(){
  var EN=document.documentElement.lang==='en';
  var top=document.getElementById('top');
  var onScroll=function(){top.classList.toggle('scrolled',window.scrollY>8)};
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  var m=document.querySelector('.mmenu');
  if(m){m.addEventListener('toggle',function(){document.documentElement.style.overflow=m.open?'hidden':''});m.addEventListener('click',function(e){if(e.target.closest('a'))m.removeAttribute('open')});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')m.removeAttribute('open')});}


  var calm=matchMedia('(prefers-reduced-motion: reduce)').matches;

  // titulares que se enfocan palabra a palabra
  if(!calm){document.querySelectorAll('.h1,.h2').forEach(function(h){
    if(h.children.length||!h.textContent.trim())return;
    var words=h.textContent.trim().split(/\s+/);h.setAttribute('aria-label',h.textContent.trim());
    h.innerHTML=words.map(function(w,i){return '<span class="w" aria-hidden="true" style="--i:'+i+'">'+w+'</span>'}).join(' ');
    h.classList.add('fx');h.classList.remove('rv');});
    var hs=document.querySelectorAll('.fx');
    if('IntersectionObserver' in window){var io3=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io3.unobserve(e.target)}})},{rootMargin:'0px 0px -10% 0px'});hs.forEach(function(h){io3.observe(h)});}
    else hs.forEach(function(h){h.classList.add('on')});}

  // portada v5: las piezas se mueven un poco con el ratón, cada una a su profundidad
  var art=document.querySelector('.h5-art');
  if(art&&!calm){var h5=document.querySelector('.hero5');
    h5.addEventListener('pointermove',function(e){var r=h5.getBoundingClientRect();art.style.setProperty('--mx',((e.clientX-r.left)/r.width-.5).toFixed(3));art.style.setProperty('--my',((e.clientY-r.top)/r.height-.5).toFixed(3))});
    h5.addEventListener('pointerleave',function(){art.style.setProperty('--mx',0);art.style.setProperty('--my',0)});}
  // héroe: las lentes se turnan, como en el gabinete, y siguen un poco al ratón
  var L=document.querySelector('.lenses'),cap=document.querySelector('.lens-cap');
  if(L&&!calm){var st=1;setTimeout(function(){L.classList.add('loop');var sw=function(){L.dataset.s=st;cap.className='lens-cap s'+st;st=st===1?2:1};sw();setInterval(sw,2600)},3200);
    var hero=document.querySelector('.hero');
    hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;L.style.transform='translate('+(x*18).toFixed(1)+'px,'+(y*14).toFixed(1)+'px)'});
    hero.addEventListener('pointerleave',function(){L.style.transform=''});}
  // cifras que cuentan al aparecer
  var nums=document.querySelectorAll('.proof b');
  if(nums.length&&!calm&&'IntersectionObserver' in window){
    var run=function(b){var t=b.textContent,sep=t.indexOf(',')>-1?',':(t.indexOf('.')>-1?'.':''),dec=!!sep,v=parseFloat(t.replace(',','.')),from=v>1900?v-40:0,t0=performance.now();
      var f=function(now){var k=Math.min(1,(now-t0)/1400);k=1-Math.pow(1-k,3);var x=from+(v-from)*k;b.textContent=dec?x.toFixed(1).replace('.',sep):Math.round(x);if(k<1)requestAnimationFrame(f)};requestAnimationFrame(f)};
    var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){run(e.target);io2.unobserve(e.target)}})},{threshold:.6});
    nums.forEach(function(b){io2.observe(b)});}
  // optotipo: dial que enfoca
  var dio=document.getElementById('dio');
  if(dio){var rows=document.querySelector('.chart .rows'),out=document.getElementById('dio-out'),ok=document.querySelector('.tune-ok');
    var upd=function(){var v=parseFloat(dio.value);rows.style.setProperty('--b',(Math.abs(v)*3.2).toFixed(2)+'px');
      out.textContent=(v<0?'−':'')+Math.abs(v).toFixed(2).replace('.',EN?'.':',');ok.textContent=v===0?(EN?'That’s it, sharp. In the consulting room we fine-tune it lens by lens.':'Así, nítido. En el gabinete lo afinamos lente a lente.'):''};
    dio.addEventListener('input',upd);upd();}
  // audífonos: ¿te pasa alguna?
  var q=document.querySelector('.quiz');
  if(q){var qo=q.querySelector('.quiz-out'),tels=EN?'<a href="tel:+34950430012">Albox, +34 950 43 00 12</a> or <a href="tel:+34950134199">Huércal-Overa, +34 950 13 41 99</a>':'<a href="tel:+34950430012">Albox, 950 43 00 12</a> o <a href="tel:+34950134199">Huércal-Overa, 950 13 41 99</a>';
    q.addEventListener('change',function(){var n=q.querySelectorAll('input:checked').length;
      qo.innerHTML=EN?(n===0?'Tick the ones that ring a bell.':n===1?'Just one could be an off day. If it keeps happening, come and see us.':
        'With '+n+', it’s worth having your hearing checked. Call and we’ll give you a time: '+tels+'.'):
        (n===0?'Marca las que te suenen.':n===1?'Una sola puede ser cosa de un mal día. Si se repite, ven a vernos.':
        'Con '+n+', merece la pena estudiar tu audición. Llama y te damos hora: '+tels+'.');});}
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){
    document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
})();

/* Mapa: solo se carga Google Maps cuando la persona lo pide */
document.querySelectorAll('.map[data-src]').forEach(function(m){
  var b=m.querySelector('.map-on'); if(!b)return;
  b.addEventListener('click',function(){
    var f=document.createElement('iframe');f.src=m.dataset.src;f.title=m.dataset.title;f.setAttribute('referrerpolicy','no-referrer-when-downgrade');f.setAttribute('allowfullscreen','');
    m.innerHTML='';m.appendChild(f);f.focus();
  });
});
