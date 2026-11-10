// Óptica Almería v4: cabecera, menú, lente del héroe, dial de graduación, tira de monturas y apariciones.
(function(){
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // cabecera
  var top = document.getElementById('top');
  var onScroll = function(){ top.classList.toggle('scrolled', window.scrollY > 24); };
  onScroll(); addEventListener('scroll', onScroll, {passive:true});

  // menú optotipo
  var menu = document.querySelector('.chartmenu');
  if (menu) {
    menu.addEventListener('toggle', function(){ document.documentElement.style.overflow = menu.open ? 'hidden' : ''; });
    menu.addEventListener('click', function(e){ if (e.target.closest('.panel a')) menu.open = false; });
    addEventListener('keydown', function(e){ if (e.key === 'Escape' && menu.open) menu.open = false; });
  }

  // la lente: nítido dentro, borroso fuera
  var stage = document.querySelector('.lens-hero .stage');
  if (stage) {
    var img = stage.querySelector('.sharp img');
    var NW = 1170, NH = 666, faces = [[0.17, 0.33], [0.516, 0.33]];
    var x = 0, y = 0, tx = 0, ty = 0, auto = true, t0 = performance.now(), raf = 0;
    var map = function(f){ // fracción de la foto -> px dentro del escenario (object-fit: cover)
      var w = stage.clientWidth, h = stage.clientHeight, s = Math.max(w / NW, h / NH);
      var iw = NW * s, ih = NH * s, pos = getComputedStyle(img).objectPosition.split(' ');
      var px = parseFloat(pos[0]) / 100, py = parseFloat(pos[1]) / 100;
      return [f[0] * iw - (iw - w) * px, f[1] * ih - (ih - h) * py];
    };
    var vis = function(){ // solo las caras que caen dentro de la foto (en el móvil se recorta una)
      var w = stage.clientWidth, ps = faces.map(map).filter(function(p){ return p[0] > 30 && p[0] < w - 30; });
      return ps.length ? ps : [map(faces[1])];
    };
    var place = function(){ stage.style.setProperty('--x', x.toFixed(1) + 'px'); stage.style.setProperty('--y', y.toFixed(1) + 'px'); };
    var start = vis()[0]; x = tx = start[0]; y = ty = start[1]; place();
    var tick = function(now){
      if (auto) { // va de una cara a la otra y se para en cada una, como al graduar
        var v = vis(), a = v[0], b = v[v.length - 1];
        var p = ((now - t0) / 4200) % 2, k = p < 1 ? p : 2 - p;
        k = Math.min(1, Math.max(0, (k - 0.25) / 0.5)); k = k * k * (3 - 2 * k);
        tx = a[0] + (b[0] - a[0]) * k; ty = a[1] + (b[1] - a[1]) * k + Math.sin(now / 900) * 6;
      }
      x += (tx - x) * 0.14; y += (ty - y) * 0.14; place();
      raf = requestAnimationFrame(tick);
    };
    var follow = function(e){
      var r = stage.getBoundingClientRect(); auto = false;
      tx = e.clientX - r.left; ty = e.clientY - r.top;
    };
    stage.addEventListener('pointermove', follow);
    stage.addEventListener('pointerdown', follow);
    if (!reduce) {
      var io0 = new IntersectionObserver(function(es){ es.forEach(function(e){
        if (e.isIntersecting) { if (!raf) raf = requestAnimationFrame(tick); }
        else { cancelAnimationFrame(raf); raf = 0; }
      }); });
      io0.observe(stage);
    } else {
      stage.addEventListener('pointermove', function(){ x = tx; y = ty; place(); });
    }
    addEventListener('resize', function(){ if (auto || reduce) { var s = vis()[0]; x = tx = s[0]; y = ty = s[1]; place(); } });
  }

  // dial: gradúate tú
  var dial = document.getElementById('dioptrias');
  if (dial) {
    var st = document.querySelector('.statement'), out = document.getElementById('dio-out'), done = document.querySelector('.grad .done');
    var fmt = function(v){ return (v < 0 ? '−' : '') + Math.abs(v).toFixed(2).replace('.', ','); };
    var upd = function(){
      var v = parseFloat(dial.value); st.style.setProperty('--blur', (Math.abs(v) * 3.2).toFixed(2) + 'px');
      out.textContent = fmt(v);
      done.textContent = v === 0 ? 'Así. En el gabinete lo hacemos con aparatos y lente a lente.' : '';
    };
    dial.addEventListener('input', upd); upd();
    document.getElementById('enfocar').addEventListener('click', function(){
      var v = parseFloat(dial.value);
      if (reduce) { dial.value = 0; upd(); return; }
      var step = function(){ v = Math.min(0, v + 0.25); dial.value = v; upd(); if (v < 0) setTimeout(step, 70); };
      step();
    });
  }

  // tira de monturas
  var reel = document.querySelector('.reel');
  document.querySelectorAll('.reel-nav button').forEach(function(b){
    b.addEventListener('click', function(){
      var f = reel.querySelector('figure'); var d = (f ? f.offsetWidth + 18 : 400) * (b.dataset.dir === 'prev' ? -1 : 1);
      reel.scrollBy({left: d, behavior: reduce ? 'auto' : 'smooth'});
    });
  });

  // apariciones
  var els = document.querySelectorAll('.rv, .wave');
  if (!('IntersectionObserver' in window) || reduce) { els.forEach(function(el){ el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, {rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(el){ io.observe(el); });
})();
