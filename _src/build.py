#!/usr/bin/env python3
"""Genera la propuesta de opticalmeria.com (v3) como HTML estático.
Uso: python3 _src/build.py            -> rutas para GitHub Pages (/opticalmeria-propuesta/)
     BASE=/ python3 _src/build.py     -> rutas para el dominio propio
Todas las páginas comparten cabecera, pie, site.css y site.js."""
import json, os, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = os.environ.get("BASE", "/opticalmeria-propuesta/")
LIVE = "https://www.opticalmeria.com/"
NOINDEX = os.environ.get("NOINDEX", "1") == "1"
VER = "4"

def u(p=""):
    return BASE + p

STORES = [
    dict(slug="albox", town="Albox", name="Óptica Almería Albox", street="Avenida Puente, 9",
         cp="04800", tel="950 43 00 12", tel_e164="+34950430012", wpimg="wp-content/uploads/2024/08/ALBOX.jpg", img="tienda-albox", imgw=[640, 1200],
         maps="https://www.google.com/maps/search/?api=1&query=%C3%93ptica+Almer%C3%ADa+Avenida+Puente+9+Albox",
         embed="https://www.google.com/maps?q=%C3%93ptica+Almer%C3%ADa,+Avenida+Puente+9,+04800+Albox&output=embed",
         geo=(37.3889, -2.1486)),
    dict(slug="huercal-overa", town="Huércal-Overa", name="Óptica Almería Huércal-Overa", street="Avenida Guillermo Reyna, 16",
         cp="04600", tel="950 13 41 99", tel_e164="+34950134199", wpimg="wp-content/uploads/2024/08/huercal-overa-1.jpg", img="tienda-huercal", imgw=[532],
         maps="https://www.google.com/maps/search/?api=1&query=%C3%93ptica+Almer%C3%ADa+Guillermo+Reyna+16+Hu%C3%A9rcal-Overa",
         embed="https://www.google.com/maps?q=%C3%93ptica+Almer%C3%ADa,+Avenida+Guillermo+Reyna+16,+04600+Hu%C3%A9rcal-Overa&output=embed",
         geo=(37.3889, -1.9417)),
]

POSTS = [
    ("cansado-ordenador", "¿Cansado del ordenador?", "2024-08-08"),
    ("palmeras-los-ojos", "Palmeras en los ojos", "2017-03-09"),
    ("me-enamore-paris", "Me enamoré en París", "2016-12-13"),
    ("lentes-protectoras", "Lentes protectoras", "2016-12-12"),
    ("adicta-las-gafas", "Adicta a las gafas", "2016-10-27"),
    ("7-consejos-cuidar-tus-lentes-contacto", "7 consejos para cuidar tus lentes de contacto", "2016-10-27"),
]
MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()
def fecha(iso):
    y, m, d = iso.split("-"); return f"{int(d)} {MESES[int(m)-1]} {y}"

NAV = [("tu-salud-visual/", "Salud visual"), ("salud-auditiva/", "Audífonos"), ("nuestras-marcas/", "Gafas y marcas"),
       ("nosotros/", "Nosotros"), ("contacto/", "Tiendas")]

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'  # Lucide: phone
PIN_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'  # Lucide: map-pin
LOGO = ('<svg viewBox="0 0 66 28" aria-hidden="true"><defs><linearGradient id="lg{n}" x1="0" x2="1">'
        '<stop offset="0" stop-color="#2a82be"/><stop offset="1" stop-color="#47b475"/></linearGradient></defs>'
        '<circle cx="13" cy="14" r="11.6" fill="none" stroke="currentColor" stroke-width="1.7"/>'
        '<circle cx="40" cy="14" r="11.6" fill="none" stroke="url(#lg{n})" stroke-width="1.7"/>'
        '<path d="M63 2.4v23.2" stroke="url(#lg{n})" stroke-width="1.7"/></svg>')

def pic(name, widths, alt, sizes="100vw", cls="", eager=False, w=None, h=None):
    av = ", ".join(f"{u('img/')}{name}-{x}.avif {x}w" for x in widths)
    wb = ", ".join(f"{u('img/')}{name}-{x}.webp {x}w" for x in widths)
    big = widths[-1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    dims = f' width="{w}" height="{h}"' if w else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{av}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{wb}" sizes="{sizes}">'
            f'<img src="{u("img/")}{name}-{big}.webp"{c} alt="{html.escape(alt)}"{dims} {load}></picture>')

# ---------- datos estructurados ----------
ORG = {"@type": "Organization", "@id": LIVE + "#org", "name": "Óptica Almería", "url": LIVE,
       "logo": LIVE + "wp-content/uploads/2024/08/cropped-icono.png", "email": "info@opticalmeria.com",
       "foundingDate": "1980", "award": "Centro Varilux especialista desde 2000",
       "department": [{"@id": LIVE + f"opticas/{s['slug']}/#tienda"} for s in STORES]}
def store_ld(s):
    return {"@type": "Optician", "@id": LIVE + f"opticas/{s['slug']}/#tienda", "name": s["name"],
            "url": LIVE + f"opticas/{s['slug']}/", "telephone": s["tel_e164"], "image": LIVE + s["wpimg"],
            "parentOrganization": {"@id": LIVE + "#org"}, "priceRange": "€€",
            "address": {"@type": "PostalAddress", "streetAddress": s["street"], "postalCode": s["cp"],
                        "addressLocality": s["town"], "addressRegion": "Almería", "addressCountry": "ES"},
            "hasMap": s["maps"],
            "areaServed": ["Albox", "Huércal-Overa", "Valle del Almanzora", "Levante almeriense"],
            "knowsAbout": ["Optometría", "Lentes progresivas Varilux", "Lentes de contacto", "Audífonos", "Audiometría"]}
def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": LIVE + p} for i, (p, n) in enumerate(items)]}
def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": html.unescape(__import__('re').sub('<[^>]+>', '', a))}} for q, a in faqs]}

# ---------- piezas comunes ----------
def head(title, desc, path, ld, preload=""):
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ""
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.className="js"</script>
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}
<link rel="canonical" href="{LIVE}{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Óptica Almería">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{LIVE}wp-content/uploads/2024/06/optica-almeria.jpg">
<meta name="theme-color" content="#f5f0e8">
<link rel="icon" href="{LIVE}wp-content/uploads/2024/08/cropped-icono.png">
<link rel="preload" href="{u('fonts/jost.woff2')}" as="font" type="font/woff2" crossorigin>
{preload}
<link rel="stylesheet" href="{u('site.css')}?v={VER}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
'''

def header(cur):
    links = "".join(f'<a href="{u(p)}"{" aria-current=page" if p == cur else ""}>{t}</a>' for p, t in NAV)
    opto = "".join(f'<li><a href="{u(p)}"{" aria-current=page" if p == cur else ""}>{t}</a><small>{d}</small></li>' for (p, t), d in zip([("", "Inicio")] + NAV, ["0,1", "0,2", "0,4", "0,6", "0,8", "1,0"]))
    tels = "".join(f'<a class="btn{" ghost" if i else ""}" href="tel:{s["tel_e164"]}">{PHONE_SVG}Llamar a {s["town"]}</a>' for i, s in enumerate(STORES))
    return f'''<header class="top" id="top">
 <div class="wrap nav">
  <a class="logo" href="{u()}" aria-label="Óptica Almería, inicio">{LOGO.format(n=1)}<span>Óptica Almería</span></a>
  <nav class="menu" aria-label="Principal">{links}</nav>
  <a class="btn" href="{u('contacto/')}#cita">Pedir cita</a>
  <details class="mmenu"><summary><i aria-hidden="true"></i><span class="mo">Menú</span><span class="mc">Cerrar</span></summary><nav class="optonav" aria-label="Principal en el móvil"><ol>{opto}</ol><div class="tels">{tels}</div></nav></details>
 </div>
</header>
<main id="main">
'''

def cita_block():
    phones = "".join(f'<a href="tel:{s["tel_e164"]}"><span>{s["town"]}</span><b>{s["tel"]}</b></a>' for s in STORES)
    return f'''<section class="night cita" id="cita" aria-labelledby="cita-t">
 <div class="wrap">
  <h2 class="h2 rv" id="cita-t">Llama a la tienda que te pille más cerca</h2>
  <p class="lead rv">Te damos hora para la revisión de la vista o del oído. Si no sabes qué necesitas, cuéntanoslo por teléfono y te orientamos.</p>
  <div class="phones rv">{phones}</div>
  <p class="mail">O escríbenos a <a href="mailto:info@opticalmeria.com">info@opticalmeria.com</a></p>
 </div>
</section>
'''

def footer():
    stores = "".join(f'<li><a href="{u("opticas/" + s["slug"] + "/")}">{s["town"]}</a> · <a href="tel:{s["tel_e164"]}">{s["tel"]}</a></li>' for s in STORES)
    nav = "".join(f'<li><a href="{u(p)}">{t}</a></li>' for p, t in NAV)
    calls = "".join(f'<a class="btn{" ghost" if i else ""}" href="tel:{s["tel_e164"]}">{PHONE_SVG}{s["town"]}</a>' for i, s in enumerate(STORES))
    return f'''</main>
<footer class="foot">
 <div class="wrap">
  <p class="big" aria-hidden="true">Óptica Almería</p>
  <div>
   <a class="logo" href="{u()}" aria-label="Óptica Almería, inicio">{LOGO.format(n=2)}<span>Óptica Almería</span></a>
   <p>Ópticos y audioprotesistas en Albox y Huércal-Overa desde 1980. Centro Varilux especialista desde 2000.</p>
  </div>
  <div><h2>Tiendas</h2><ul>{stores}</ul></div>
  <div><h2>La web</h2><ul>{nav}<li><a href="{LIVE}blog/">Blog de Carmen</a></li></ul></div>
  <div><h2>Escríbenos</h2><ul><li><a href="mailto:info@opticalmeria.com">info@opticalmeria.com</a></li></ul></div>
  <p class="legal"><span>© Óptica Almería · Óptica Berruezo, S. L.</span><a href="{LIVE}aviso-legal/">Aviso legal</a><a href="{LIVE}politica-de-privacidad/">Privacidad</a><span>Propuesta de rediseño, noviembre de 2026</span></p>
 </div>
</footer>
<nav class="callbar" aria-label="Llamar a una tienda">{calls}</nav>
<script src="{u('site.js')}?v={VER}" defer></script>
</body>
</html>
'''

def page(path, title, desc, ld, body, cur="", preload=""):
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(title, desc, path, ld, preload) + header(cur) + body + footer(), encoding="utf-8")
    print("ok", out.relative_to(ROOT))

def phead(crumb, lbl, h1, lead, img=None, imgw=None, alt=""):
    fig = f'<figure>{pic(img, imgw, alt, "(max-width:1020px) 100vw, 45vw", eager=True)}</figure>' if img else ""
    return f'''<header class="phead">
 <div class="wrap">
  <div>
   <p class="crumbs"><a href="{u()}">Inicio</a> / {crumb}</p>
   <h1 class="h1">{h1}</h1>
   <p class="lead">{lead}</p>
  </div>
  {fig}
 </div>
</header>
'''

# ---------- PORTADA ----------
FAQ_HOME = [
    ("¿Cada cuánto tengo que revisarme la vista?",
     "La Organización Mundial de la Salud recomienda una revisión al año, también si no llevas gafas. Sirve para ajustar la graduación y para detectar a tiempo problemas como las cataratas."),
    ("¿Hacéis revisiones del oído y audífonos?",
     "Sí. Hacemos videotoscopia, audiometría tonal en cabina insonorizada y logoaudiometría, y adaptamos audífonos digitales, tanto los que van dentro del oído como los de detrás de la oreja. Pide cita por teléfono en tu tienda."),
    ("¿Qué quiere decir que seáis centro Varilux especialista?",
     "Es un título que da Essilor, el fabricante de las lentes Varilux, a las ópticas con aparatos de medida precisos y personal formado para adaptar progresivos. Lo tenemos desde el año 2000."),
    ("¿Tengo que pedir cita para graduarme?",
     "Es mejor. Así te atendemos sin prisas y con el gabinete libre. Llama a Albox al 950 43 00 12 o a Huércal-Overa al 950 13 41 99."),
    ("¿Adaptáis lentillas?",
     "Sí. Adaptamos lentes de contacto y también Orto-K, unas lentes que se ponen para dormir y corrigen la miopía durante el día."),
]

def home():
    lens_img = lambda cls: (f'<div class="lens {cls}"><picture><source type="image/avif" srcset="{u("img/gafas-sol-desierto-1170.avif")}">'
                            f'<img src="{u("img/gafas-sol-desierto-1170.webp")}" alt="" width="1170" height="666" fetchpriority="high"></picture></div>')
    proof = '''<div class="proof"><ul class="wrap">
  <li><b>4,9</b><span>de nota media en Google</span></li>
  <li><b>2000</b><span>centro Varilux especialista desde ese año</span></li>
  <li><b>1980</b><span>abrimos la primera tienda en Albox</span></li>
  <li><b>2</b><span>tiendas, en Albox y Huércal-Overa</span></li>
 </ul></div>'''
    svcs = [
        ("Graduación de la vista", "Medimos tu agudeza visual de lejos y de cerca y comprobamos cómo trabajan los dos ojos juntos."),
        ("Retinografía", "Una foto del fondo del ojo que sirve para vigilar la retina de una revisión a la siguiente."),
        ("Lentes de contacto", "Te adaptamos las lentillas y te enseñamos a ponértelas y a cuidarlas."),
        ("Orto-K", "Lentes que se llevan mientras duermes y corrigen la miopía durante el día, sin gafas."),
        ("Baja visión", "Ayudas ópticas para quien ya no ve bien ni con sus gafas: lupas, filtros y telescopios."),
    ]
    svc_html = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in svcs)
    tests = [
        ("Videotoscopia", "Miramos el conducto y el tímpano con una cámara conectada a una pantalla, y tú lo ves con nosotros."),
        ("Audiometría tonal", "En cabina insonorizada escuchas tonos a distintas intensidades para saber cuál es tu umbral de audición."),
        ("Logoaudiometría", "La misma prueba, pero con palabras: así sabemos cuánto entiendes de lo que oyes."),
        ("Umbral de molestia", "Buscamos a qué volumen te empiezan a molestar los sonidos para que el audífono nunca llegue ahí."),
    ]
    quiz = ["Subes la tele más que los demás", "Pides a menudo que te repitan las cosas", "En un bar o en una comida familiar te cuesta seguir la conversación", "Te parece que la gente habla entre dientes", "Oyes un pitido o un zumbido cuando hay silencio"]
    quiz_html = "".join(f'<li><label><input type="checkbox"><span>{q}</span></label></li>' for q in quiz)
    tests_html = "".join(f"<li class='rv'><h3>{a}</h3><p>{b}</p></li>" for a, b in tests)
    stores_html = "".join(store_card(s) for s in STORES)
    posts_html = "".join(f'<li><a href="{LIVE}{s}/"><time datetime="{d}">{fecha(d)}</time><h3>{t}</h3><span class="arrow" aria-hidden="true">→</span></a></li>' for s, t, d in POSTS[:4])
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ_HOME)
    body = f'''
<section class="hero" aria-labelledby="h1">
 <div class="wrap">
  <div>
   <p class="lbl">Óptica y audífonos · Albox y Huércal-Overa</p>
   <h1 class="h1" id="h1">Gafas hechas a la medida de tus ojos</h1>
   <p class="lead">Graduamos tu vista con los aparatos de un centro Varilux especialista, revisamos tu oído en cabina insonorizada y te ayudamos a elegir montura entre primeras marcas. Desde 1980, en el Almanzora.</p>
   <div class="ctas"><a class="btn" href="#cita">Pedir cita</a><a class="btn ghost" href="#tiendas">Ver las tiendas</a></div>
  </div>
  <figure>
   <div class="lenses">{lens_img("l1")}<span class="bridge" aria-hidden="true"></span>{lens_img("l2")}</div>
   <figcaption class="lens-cap">¿Mejor con la primera… o con la segunda?</figcaption>
  </figure>
 </div>
</section>
{proof}

<section aria-labelledby="rev-t">
 <div class="wrap exam">
  <figure class="chart rv" aria-label="Optotipo de agudeza visual">
   <div class="rows"><p>Ó<small>0,1</small></p><p>P T<small>0,2</small></p><p>I C A<small>0,4</small></p><p>A L M E R<small>0,6</small></p><p>Í A · A L B O X<small>0,8</small></p><p><span>HUÉRCAL-OVERA</span><small>1,0</small></p></div>
   <div class="tune"><label for="dio">Mueve el dial hasta leerlo bien</label><div class="tune-row"><input type="range" id="dio" min="-3" max="0" step="0.25" value="-1.75"><output id="dio-out" for="dio">−1,75</output></div><p class="tune-ok" aria-live="polite"></p></div>
   <figcaption>Este optotipo es de broma. El de verdad te espera en el gabinete.</figcaption>
  </figure>
  <div>
      <h2 class="h2 rv" id="rev-t">Una vez al año, aunque veas bien</h2>
   <p class="lead rv">Somos establecimiento sanitario. En el gabinete medimos tu graduación y miramos la salud del ojo, que es lo que permite detectar a tiempo cosas que todavía no notas.</p>
   <ul class="svc-list rv">{svc_html}</ul>
   <p style="margin-top:28px" class="rv"><a class="tlink" href="{u('tu-salud-visual/')}">Miopía, astigmatismo, cataratas: qué es cada cosa <span class="arrow">→</span></a></p>
  </div>
 </div>
</section>

<section class="band" aria-labelledby="prog-t">
 <div class="wrap prog">
  <figure class="rv">{pic("progresivos", [640, 1230], "Clienta de Óptica Almería ajustándose unas gafas de pasta de carey", "(max-width:1020px) 100vw, 55vw")}</figure>
  <div>
   <p class="lbl rv">Progresivos</p>
   <h2 class="h2 rv" id="prog-t">Ver de lejos, de media distancia y de cerca con las mismas gafas</h2>
   <p class="lead rv">Unos progresivos solo funcionan si se miden bien: la altura de cada pupila, la distancia entre los ojos, cómo te queda la montura en la cara. Por eso Essilor nos nombró centro Varilux especialista, y por eso tomamos esas medidas con aparatos de precisión.</p>
   <figure class="zones rv">
    <svg viewBox="0 0 200 170" aria-hidden="true"><path d="M22 14H178Q192 14 192 30V104Q192 156 128 158H72Q8 156 8 104V30Q8 14 22 14Z" fill="var(--card)" stroke="currentColor" stroke-width="1.5"/><path d="M8 66Q100 84 192 66" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 5"/><path d="M20 118Q100 104 180 118" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 5"/><path d="M100 70V114" stroke="var(--accent)" stroke-width="10" stroke-linecap="round" opacity=".18"/></svg>
    <figcaption><ol><li><b>Lejos</b><span>la carretera, la tele</span></li><li><b>Intermedia</b><span>el ordenador, el salpicadero</span></li><li><b>Cerca</b><span>el libro, el móvil</span></li></ol></figcaption>
   </figure>
   <dl class="rv"><dt>2000</dt><dd>el año en que Essilor nos nombró centro Varilux especialista.</dd></dl>
  </div>
 </div>
</section>

<section id="audifonos" aria-labelledby="ear-t">
 <div class="wrap">
  <p class="como rv" aria-hidden="true">¿Cómo?</p>
  <div class="ear-grid">
   <div><h2 class="h2 rv" id="ear-t">Cuando oyes, pero no entiendes</h2></div>
   <p class="lead rv">La pérdida de oído llega poco a poco y casi siempre en los dos oídos, por eso solemos darnos cuenta tarde. El estudio completo de tu audición se hace en cuatro pruebas, sin molestias.</p>
  </div>
  <svg class="wave rv" viewBox="0 0 1200 80" preserveAspectRatio="none" aria-hidden="true"><path class="lit" d="M0 40 C 40 4, 80 76, 120 40 S 200 8, 240 40 S 320 68, 360 40 S 440 16, 480 40 S 560 60, 600 40 S 680 26, 720 40 S 800 52, 840 40 S 920 34, 960 40 S 1040 46, 1080 40 S 1160 40, 1200 40"/></svg>
  <div class="quiz rv">
   <h3 class="h3">¿Te pasa alguna de estas?</h3>
   <ul>{quiz_html}</ul>
   <p class="quiz-out" aria-live="polite">Marca las que te suenen.</p>
  </div>
  <ol class="tests">{tests_html}</ol>
  <p class="ear-more rv">Con el resultado te explicamos qué audífono te conviene, de los que van dentro del oído o de los de detrás de la oreja, y te lo adaptamos a tu audición. <a class="tlink" href="{u('salud-auditiva/')}">Cómo funciona un audífono <span class="arrow">→</span></a></p>
 </div>
</section>

<section class="band" aria-labelledby="mar-t">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2 rv" id="mar-t">Monturas que se eligen con calma, y con espejo</h2></div>
  <p class="lead rv">Trabajamos solo con primeras marcas, de las más clásicas a las más atrevidas. Ven a probártelas: te decimos con sinceridad cuál te favorece y cuál no.</p></div>
  <div class="frames">
   <figure class="f1 rv">{pic("gafas-sol-desierto", [640, 1170], "Dos chicas con gafas de sol entre rocas del desierto de Almería", "(max-width:700px) 100vw, 56vw")}</figure>
   <figure class="rv">{pic("etnia", [640, 1200], "Montura de pasta de carey con varillas de colores de Etnia Barcelona", "(max-width:700px) 100vw, 42vw")}</figure>
   <figure class="rv">{pic("monturas-redondas", [640, 1126], "Cuatro gafas de sol redondas de acetato en distintos colores", "(max-width:700px) 100vw, 42vw")}</figure>
  </div>
  <ul class="brands rv" aria-label="Algunas de nuestras marcas"><li>Varilux</li><li>Etnia Barcelona</li><li>Persol</li><li>Ray-Ban</li></ul>
  <p style="margin-top:22px" class="rv"><a class="tlink" href="{u('nuestras-marcas/')}">Todas las marcas <span class="arrow">→</span></a></p>
 </div>
</section>

<section id="tiendas" aria-labelledby="tie-t">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2 rv" id="tie-t">En Albox y en Huércal-Overa</h2></div>
  <p class="lead rv">Las dos tiendas tienen gabinete de optometría. Llama antes y te damos hora.</p></div>
  <div class="stores">{stores_html}</div>
 </div>
</section>

<section class="band" aria-labelledby="his-t">
 <div class="wrap story">
  <figure class="rv">{pic("pita", [600, 1057], "Una pita florecida en el desierto de Almería bajo un cielo de atardecer", "(max-width:1020px) 100vw, 38vw")}</figure>
  <div>
   <p class="lbl rv">Nosotros</p>
   <p class="year rv" aria-hidden="true">1980</p>
   <h2 class="h2 rv" id="his-t">Un viaje que empezó en Albox</h2>
   <p class="lead rv">Hemos cambiado de siglo, hemos visto pasar la revolución tecnológica y tantísimas modas, y hemos cambiado de imagen más de una vez. Lo que no ha cambiado es la forma de trabajar: cuidar tu mirada con calidad, con los últimos avances y con trato de amigo.</p>
   <p class="rv" style="margin-top:28px"><a class="tlink" href="{u('nosotros/')}">Quiénes somos <span class="arrow">→</span></a></p>
  </div>
 </div>
</section>

<section aria-labelledby="blog-t">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2 rv" id="blog-t">Adicta a las gafas, el blog de Carmen</h2></div>
  <p class="lead rv">Consejos para cuidar tus lentillas, cómo descansar la vista del ordenador y alguna que otra montura de la que nos enamoramos.</p></div>
  <ul class="posts rv">{posts_html}</ul>
 </div>
</section>

<section class="band" aria-labelledby="faq-t">
 <div class="wrap faq">
  <div><h2 class="h2 rv" id="faq-t">Lo que más nos preguntáis en el mostrador</h2></div>
  <div class="rv">{faq_html}</div>
 </div>
</section>
{cita_block()}'''
    ld = [ORG] + [store_ld(s) for s in STORES] + [faq_ld(FAQ_HOME), {"@type": "WebSite", "@id": LIVE + "#web", "url": LIVE, "name": "Óptica Almería", "inLanguage": "es"}]
    pre = f'<link rel="preload" as="image" href="{u("img/gafas-sol-desierto-1170.avif")}" type="image/avif" fetchpriority="high">'
    page("", "Óptica en Albox y Huércal-Overa · Gafas, progresivos y audífonos | Óptica Almería",
         "Ópticos y audioprotesistas en Albox y Huércal-Overa desde 1980. Revisión de la vista, progresivos Varilux, lentillas y audífonos con audiometría en cabina. Pide cita.",
         ld, body, preload=pre)

def store_card(s, h="h3"):
    return f'''<article class="store rv">
 <figure>{pic(s["img"], s["imgw"], "Fachada de Óptica Almería en " + s["town"], "(max-width:700px) 100vw, 50vw")}</figure>
 <div class="in">
  <{h} class="h3"><a href="{u("opticas/" + s["slug"] + "/")}" style="text-decoration:none">{s["town"]}</a></{h}>
  <address>{s["street"]}, {s["cp"]} {s["town"]} (Almería)</address>
  <a class="tel" href="tel:{s["tel_e164"]}">{s["tel"]}</a>
  <p class="hours">Horario: <a href="{s["maps"]}" rel="noopener">míralo en Google Maps</a></p>
  <div class="acts"><a class="btn" href="tel:{s["tel_e164"]}">{PHONE_SVG}Llamar</a><a class="btn ghost" href="{s["maps"]}" rel="noopener">{PIN_SVG}Cómo llegar</a></div>
 </div>
</article>'''

# ---------- SALUD VISUAL ----------
def salud_visual():
    defs = [
        ("Miopía", "La imagen se enfoca por delante de la retina, así que lo lejano se ve borroso. Es típico guiñar los ojos para ver mejor, y si no está bien corregida da fatiga y dolor de cabeza.",
         "Se corrige con lentes cóncavas, más finas en el centro que en los bordes. A través de ellas las cosas parecen algo más pequeñas."),
        ("Hipermetropía", "La imagen se enfoca por detrás de la retina y cuesta ver de cerca. Con poca graduación y en gente joven el ojo lo compensa haciendo fuerza, pero a cambio llegan el dolor de cabeza, el lagrimeo y los ojos rojos después de leer.",
         "Se corrige con lentes convexas, más gruesas en el centro."),
        ("Astigmatismo", "La córnea está un poco más curvada en un eje que en otro, y la imagen sale distorsionada de lejos y de cerca. Da síntomas parecidos a la hipermetropía: dolor de cabeza, fatiga e irritación.",
         "Casi nunca va solo: suele acompañar a la miopía o a la hipermetropía."),
        ("Cataratas", "No son un defecto de graduación, pero la cambian: bajan la agudeza visual y dan deslumbramiento. Aparecen en cerca del 65 % de las personas de más de 70 años, antes si hay mucho sol o antecedentes en la familia.",
         "Al principio se compensan cambiando la graduación de la gafa. Más adelante hace falta operar."),
    ]
    d = "".join(f'<div><h3>{a}</h3><p>{b}</p><p>{c}</p></div>' for a, b, c in defs)
    body = phead("Salud visual", "Salud visual", "Tu revisión de la vista en Albox y Huércal-Overa",
                 "Llevar gafas solo quiere decir que el ojo enfoca un poco fuera de sitio, y eso tiene arreglo. Lo importante es revisarlo a tiempo.",
                 "lentillas", [640, 1400], "Un chico a punto de ponerse una lentilla") + f'''
<section style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap split">
  <nav class="toc" aria-label="En esta página"><ul><li><a href="#revision">La revisión</a></li><li><a href="#defectos">Defectos de la vista</a></li><li><a href="#servicios">Qué hacemos</a></li></ul></nav>
  <div class="prose">
   <h2 id="revision">Una revisión al año</h2>
   <p>La Organización Mundial de la Salud recomienda revisarse la vista al menos una vez al año, para corregir la graduación y para detectar enfermedades del ojo cuando todavía tienen fácil arreglo. Si en tu familia hay antecedentes, todavía más.</p>
   <p>La revisión la hace un óptico optometrista y no duele: lees letras, miras luces y te hacemos alguna foto del ojo.</p>
   <h2 id="defectos">Los defectos de la vista, explicados</h2>
   <div class="defs">{d}</div>
   <h2 id="servicios">Qué hacemos en el gabinete</h2>
   <ul>
    <li><strong>Graduación</strong> de lejos y de cerca, y visión con los dos ojos a la vez.</li>
    <li><strong>Retinografía</strong>: foto del fondo del ojo para comparar de un año a otro.</li>
    <li><strong>Progresivos Varilux</strong>, con medidas tomadas con aparato. Somos centro Varilux especialista desde 2000.</li>
    <li><strong>Lentes de contacto</strong> y <strong>Orto-K</strong>, que corrigen la miopía mientras duermes.</li>
    <li><strong>Baja visión</strong>: lupas, filtros y otras ayudas para quien ya no ve bien con gafas.</li>
   </ul>
   <p class="note">Si tienes dudas sobre tu vista, llama a tu tienda y te damos hora: Albox, <a href="tel:+34950430012">950 43 00 12</a>; Huércal-Overa, <a href="tel:+34950134199">950 13 41 99</a>.</p>
  </div>
 </div>
</section>
{cita_block()}'''
    page("tu-salud-visual", "Revisión de la vista en Albox y Huércal-Overa | Óptica Almería",
         "Miopía, hipermetropía, astigmatismo y cataratas, explicados. Revisión anual, retinografía, progresivos Varilux, lentillas y Orto-K en Albox y Huércal-Overa.",
         [ORG, crumbs_ld([("", "Inicio"), ("tu-salud-visual/", "Salud visual")])], body, cur="tu-salud-visual/")

# ---------- AUDÍFONOS ----------
def salud_auditiva():
    body = phead("Audífonos", "Salud auditiva", "Audífonos y revisión del oído en Albox y Huércal-Overa",
                 "La pérdida de audición llega despacio y casi siempre en los dos oídos. Cuanto antes se detecta, más sonidos se recuperan.",
                 "audifono", [768], "Audífono retroauricular sobre una huella dactilar") + f'''
<section style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap split">
  <nav class="toc" aria-label="En esta página"><ul><li><a href="#causas">Por qué se pierde oído</a></li><li><a href="#tipos">Tipos de pérdida</a></li><li><a href="#pruebas">Las pruebas</a></li><li><a href="#audifonos">Tipos de audífono</a></li></ul></nav>
  <div class="prose">
   <h2 id="causas">Por qué se pierde oído</h2>
   <p>La pérdida de audición, o hipoacusia, es la dificultad para oír ciertos sonidos. Como avanza poco a poco, muchas veces nos damos cuenta cuando ya es importante. Las causas más frecuentes son:</p>
   <ul><li>La edad.</li><li>La herencia familiar.</li><li>Pasar mucho tiempo con ruidos fuertes.</li><li>Infecciones y algunos medicamentos.</li><li>Golpes y accidentes.</li></ul>
   <h2 id="tipos">Tipos de pérdida</h2>
   <p>Según cuánto se pierde, la pérdida es leve, moderada, severa o profunda. Según dónde está el problema:</p>
   <div class="defs">
    <div><h3>De transmisión</h3><p>El sonido no llega bien hasta los receptores del oído interno. Afecta a todos los tonos por igual y suele recuperarse buena parte de la audición.</p></div>
    <div><h3>Neurosensorial</h3><p>Los receptores están dañados. No afecta igual a todos los tonos y la queja típica es «oigo, pero no entiendo».</p></div>
    <div><h3>Mixta</h3><p>Se juntan las dos: falla la transmisión y fallan los receptores.</p></div>
   </div>
   <h2 id="pruebas">Las pruebas que te hacemos</h2>
   <ul>
    <li><strong>Videotoscopia.</strong> Vemos el conducto y el tímpano con un otoscopio conectado a una pantalla.</li>
    <li><strong>Audiometría tonal.</strong> En cabina insonorizada, con tonos a distintas intensidades, por vía aérea y ósea.</li>
    <li><strong>Logoaudiometría.</strong> Igual, pero con palabras, para saber cuánto entiendes.</li>
    <li><strong>Umbral de molestia.</strong> A qué volumen te empiezan a molestar los sonidos.</li>
   </ul>
   <h2 id="audifonos">Tipos de audífono</h2>
   <p>Todos los audífonos que adaptamos son digitales: más pequeños, más potentes y ajustables a tu audición. El tipo depende del estudio previo.</p>
   <div class="defs">
    <div><h3>Dentro del oído</h3><p>Van en el conducto y en la parte visible de la oreja, hechos a medida con una impresión que tomamos en el gabinete. Los más pequeños, los CIC, quedan escondidos del todo.</p></div>
    <div><h3>Detrás de la oreja</h3><p>Una cajita detrás de la oreja unida por un tubo fino a un auricular dentro del oído, con molde a medida o estándar. Suelen tener más potencia.</p></div>
   </div>
   <p class="note">Pide cita para el estudio de audición: Albox, <a href="tel:+34950430012">950 43 00 12</a>; Huércal-Overa, <a href="tel:+34950134199">950 13 41 99</a>.</p>
  </div>
 </div>
</section>
{cita_block()}'''
    page("salud-auditiva", "Audífonos y audiometría en Albox y Huércal-Overa | Óptica Almería",
         "Estudio completo de audición con videotoscopia y audiometría en cabina insonorizada. Audífonos digitales dentro del oído y detrás de la oreja en Albox y Huércal-Overa.",
         [ORG, crumbs_ld([("", "Inicio"), ("salud-auditiva/", "Audífonos")])], body, cur="salud-auditiva/")

# ---------- MARCAS ----------
def marcas():
    body = phead("Gafas y marcas", "Gafas y marcas", "Monturas de primeras marcas",
                 "De las más clásicas a las más atrevidas. Sea cual sea tu estilo, encontramos la gafa que te favorece.",
                 "etnia", [640, 1200], "Montura de carey con varillas de colores de Etnia Barcelona") + f'''
<section style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap">
  <div class="frames">
   <figure class="f1 rv">{pic("gafas-sol-desierto", [640, 1170], "Dos chicas con gafas de sol entre rocas del desierto de Almería", "(max-width:700px) 100vw, 56vw")}</figure>
   <figure class="rv">{pic("persol", [640, 945], "Campaña Reflex Edition de Persol en blanco y negro", "(max-width:700px) 100vw, 42vw")}</figure>
   <figure class="rv">{pic("monturas-redondas", [640, 1126], "Cuatro gafas de sol redondas de acetato", "(max-width:700px) 100vw, 42vw")}</figure>
  </div>
  <div class="prose" style="margin-top:56px">
   <h2>Solo primeras marcas</h2>
   <p>Así podemos garantizar que cada montura y cada lente son de la máxima calidad y cumplen todas las normas sanitarias. En la tienda tenemos muchas más de las que caben aquí: ven a probártelas sin compromiso.</p>
   <ul class="brands" style="margin-top:12px"><li>Varilux</li><li>Etnia Barcelona</li><li>Persol</li><li>Ray-Ban</li></ul>
  </div>
 </div>
</section>
{cita_block()}'''
    page("nuestras-marcas", "Gafas graduadas y de sol de primeras marcas en Albox | Óptica Almería",
         "Monturas graduadas y gafas de sol de primeras marcas como Etnia Barcelona, Persol y Ray-Ban, y lentes Varilux, en Albox y Huércal-Overa.",
         [ORG, crumbs_ld([("", "Inicio"), ("nuestras-marcas/", "Gafas y marcas")])], body, cur="nuestras-marcas/")

# ---------- NOSOTROS ----------
def nosotros():
    body = phead("Nosotros", "Nosotros", "Ópticos en el Almanzora desde 1980",
                 "Óptica Almería es un viaje que empezó en Albox y ha recorrido la provincia entera, siempre de la mano de nuestros pacientes y amigos.",
                 "pita", [600, 1057], "Pita florecida en el desierto de Almería") + f'''
<section style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap split">
  <nav class="toc" aria-label="En esta página"><ul><li><a href="#historia">Historia</a></li><li><a href="#varilux">Varilux especialista</a></li><li><a href="#sanitario">Establecimiento sanitario</a></li></ul></nav>
  <div class="prose">
   <h2 id="historia">Un viaje en el tiempo, y en la amistad</h2>
   <p>Hemos cambiado de siglo, hemos vivido la revolución tecnológica y la globalización, hemos visto pasar tantísimas modas, y todo ello junto a vosotros. En estos años hemos cambiado de imagen, pero seguimos valorando lo que de verdad importa: cuidar tu mirada con la mayor calidad y con los últimos avances técnicos.</p>
   <p>La filosofía de la casa ha sido siempre la misma: darte la mejor solución al mejor precio, con una selección de marcas exclusivas y modelos nuevos de lentes y monturas para cualquier necesidad, sea de diseño o de moda.</p>
   <h2 id="varilux">Centro Varilux especialista desde 2000</h2>
   <p>Es un título que otorga Essilor a las ópticas que dan mejor servicio y atención y trabajan con los últimos avances. Para tenerlo, nuestras tiendas cuentan con los instrumentos de medida más precisos del mercado y con personal muy cualificado.</p>
   <h2 id="sanitario">Somos establecimiento sanitario</h2>
   <p>Nuestro trabajo tiene que ver con tu salud, la visual y la auditiva. Por eso cada revisión la hace un profesional titulado y con el tiempo que haga falta.</p>
  </div>
 </div>
</section>
{cita_block()}'''
    page("nosotros", "Quiénes somos · Ópticos desde 1980 en Albox | Óptica Almería",
         "Óptica Almería: ópticos en Albox y Huércal-Overa desde 1980 y centro Varilux especialista desde 2000. Establecimiento sanitario de salud visual y auditiva.",
         [ORG, crumbs_ld([("", "Inicio"), ("nosotros/", "Nosotros")])], body, cur="nosotros/")

# ---------- CONTACTO ----------
def contacto():
    cards = "".join(store_card(s, "h2") for s in STORES)
    body = phead("Tiendas", "Tiendas y contacto", "Dos tiendas, en Albox y Huércal-Overa",
                 "Las dos tienen gabinete de optometría. Llama antes de venir y te damos hora para que no tengas que esperar.") + f'''
<section style="padding-top:0">
 <div class="wrap"><div class="stores">{cards}</div>
 <p class="note" style="margin-top:36px">¿Dudas? Escríbenos a <a href="mailto:info@opticalmeria.com">info@opticalmeria.com</a> y te contestamos.</p></div>
</section>
{cita_block()}'''
    page("contacto", "Tiendas y contacto en Albox y Huércal-Overa | Óptica Almería",
         "Óptica Almería en Avenida Puente 9 de Albox (950 43 00 12) y Avenida Guillermo Reyna 16 de Huércal-Overa (950 13 41 99). Cómo llegar y pedir cita.",
         [ORG] + [store_ld(s) for s in STORES] + [crumbs_ld([("", "Inicio"), ("contacto/", "Tiendas")])], body, cur="contacto/")

# ---------- UNA PÁGINA POR TIENDA ----------
def tienda(s):
    other = [x for x in STORES if x is not s][0]
    body = phead(f'<a href="{u("contacto/")}">Tiendas</a> / {s["town"]}', s["town"], f"Óptica Almería en {s['town']}",
                 f"{s['street']}. Revisión de la vista, progresivos Varilux, lentillas y audífonos. Llama al {s['tel']} y te damos hora.",
                 s["img"], s["imgw"], f"Fachada de Óptica Almería en {s['town']}") + f'''
<section style="padding-top:clamp(24px,3vw,40px)">
 <div class="wrap">
  <dl class="info">
   <div><dt>Dirección</dt><dd>{s["street"]}<br>{s["cp"]} {s["town"]} (Almería)</dd></div>
   <div><dt>Teléfono</dt><dd><a href="tel:{s["tel_e164"]}">{s["tel"]}</a></dd></div>
   <div><dt>Horario</dt><dd><a href="{s["maps"]}" rel="noopener">Míralo en Google Maps</a></dd></div>
  </dl>
  <div class="ctas" style="margin:32px 0 56px"><a class="btn" href="tel:{s["tel_e164"]}">{PHONE_SVG}Llamar a {s["town"]}</a><a class="btn ghost" href="{s["maps"]}" rel="noopener">{PIN_SVG}Cómo llegar</a></div>
  <div class="map"><iframe src="{s["embed"]}" title="Mapa de Óptica Almería en {s["town"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  <div class="prose" style="margin-top:56px">
   <h2>Qué hacemos en esta tienda</h2>
   <ul>
    <li>Revisión de la vista y retinografía.</li>
    <li>Progresivos Varilux, con medidas tomadas con aparato.</li>
    <li>Lentes de contacto y Orto-K.</li>
    <li>Gafas graduadas y de sol de primeras marcas.</li>
    <li>Estudio de audición y audífonos.</li>
   </ul>
   <p>¿Te pilla mejor la otra? Estamos también en <a href="{u("opticas/" + other["slug"] + "/")}">{other["town"]}, {other["street"]}</a>.</p>
  </div>
 </div>
</section>
{cita_block()}'''
    page(f"opticas/{s['slug']}", f"Óptica en {s['town']}, {s['street']} | Óptica Almería",
         f"Óptica Almería en {s['street']}, {s['town']}. Revisión de la vista, progresivos Varilux, lentillas y audífonos. Teléfono {s['tel']}.",
         [ORG, store_ld(s), crumbs_ld([("", "Inicio"), ("contacto/", "Tiendas"), (f"opticas/{s['slug']}/", s["town"])])], body, cur="contacto/")

if __name__ == "__main__":
    home(); salud_visual(); salud_auditiva(); marcas(); nosotros(); contacto()
    for s in STORES: tienda(s)
    (ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if NOINDEX else f"User-agent: *\nAllow: /\nSitemap: {LIVE}sitemap.xml\n")
    (ROOT / ".nojekyll").write_text("")
