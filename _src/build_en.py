#!/usr/bin/env python3
"""Versión en inglés de opticalmeria.com, en /en/. Mismo diseño, CSS, JS y fotos que build.py.
Uso: igual que build.py (mismas variables BASE, ASSETS, NOINDEX, OUT). Ejecutar DESPUÉS de build.py.
Pensada para los residentes británicos e irlandeses del Almanzora y el Levante: inglés británico
(«varifocals», «eye test», «centre»). Los textos legales y el blog siguen en español."""
import json, html, re
import build as B
from build import LIVE, STORES, LOGO, PHONE_SVG, PIN_SVG, pic, a, u, crumbs_ld, slash

ES_OF = {v: k for k, v in B.EN_PATHS.items()}

NAV = [("en/eye-care/", "Eye care"), ("en/hearing-aids/", "Hearing aids"), ("en/brands/", "Brands"),
       ("en/about-us/", "About us"), ("en/stores/", "Shops")]

INTL = {"albox": "+34 950 43 00 12", "huercal-overa": "+34 950 13 41 99"}
ALT = {"albox": "Round acetate sunglasses at Óptica Almería",
       "huercal-overa": "Óptica Almería shop front in Huércal-Overa"}
HOURS = "Monday to Friday, 9:30am–2pm and 5:40–8:30pm (summer afternoons 5–8pm). Saturdays, 10am–2pm."
MONTHS = "January February March April May June July August September October November December".split()
def date_en(iso):
    y, m, d = iso.split("-"); return f"{int(d)} {MONTHS[int(m)-1]} {y}"

def store_ld_en(s):
    d = B.store_ld(s)
    d["knowsAbout"] = ["Optometry", "Varilux varifocal lenses", "Contact lenses", "Hearing aids", "Audiometry"]
    return d
ORG = B.ORG
def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', x))}} for q, x in faqs]}

# ---------- piezas comunes ----------
def head(title, desc, path, ld, preload=""):
    es = ES_OF[path]
    robots = '<meta name="robots" content="noindex,nofollow">' if B.NOINDEX else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.className="js"</script>
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}
<link rel="canonical" href="{LIVE}{path}/">
{B.alternates(es)}
<meta property="og:type" content="website">
<meta property="og:locale" content="en_GB">
<meta property="og:locale:alternate" content="es_ES">
<meta property="og:site_name" content="Óptica Almería">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{LIVE}wp-content/uploads/2024/06/optica-almeria.jpg">
<meta name="theme-color" content="#f5f0e8">
<link rel="icon" href="{LIVE}wp-content/uploads/2024/08/cropped-icono.png">
<link rel="preload" href="{a('fonts/jost.woff2')}" as="font" type="font/woff2" crossorigin>
{preload}
<link rel="stylesheet" href="{a('site.css')}?v={B.VER}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(cur, path):
    es = ES_OF[path]
    links = "".join(f'<a href="{u(p)}"{" aria-current=page" if p == cur else ""}>{t}</a>' for p, t in NAV)
    opto = "".join(f'<li><a href="{u(p)}"{" aria-current=page" if p == cur else ""}>{t}</a><small>{d}</small></li>' for (p, t), d in zip([("en/", "Home")] + NAV, ["0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]))
    tels = "".join(f'<a class="btn{" ghost" if i else ""}" href="tel:{s["tel_e164"]}">{PHONE_SVG}Call {s["town"]}</a>' for i, s in enumerate(STORES))
    return f'''<header class="top" id="top">
 <div class="wrap nav">
  <a class="logo" href="{u('en/')}" aria-label="Óptica Almería, home">{LOGO.format(n=1)}<span>Óptica Almería</span></a>
  <nav class="menu" aria-label="Main">{links}</nav>
  <a class="btn" href="{u('en/stores/')}#cita">Book now</a>
  <a class="lang" href="{u(slash(es))}" hreflang="es" lang="es" title="Versión en español" aria-label="Versión en español">ES</a>
  <details class="mmenu"><summary><i aria-hidden="true"></i><span class="mo">Menu</span><span class="mc">Close</span></summary><nav class="optonav" aria-label="Main, on mobile"><ol>{opto}</ol><div class="tels">{tels}</div><a class="lang2" href="{u(slash(es))}" hreflang="es" lang="es">Versión en español</a></nav></details>
 </div>
</header>
<main id="main">
'''

def cita_block():
    phones = "".join(f'<a href="tel:{s["tel_e164"]}"><span>{s["town"]}</span><b>{INTL[s["slug"]]}</b></a>' for s in STORES)
    return f'''<section class="night cita" id="cita" aria-labelledby="cita-t">
 <div class="wrap">
  <h2 class="h2 rv" id="cita-t">Call whichever shop is closer to you</h2>
  <p class="lead rv">We’ll give you a time for your eye test or hearing test. If you’re not sure what you need, tell us on the phone and we’ll point you in the right direction.</p>
  <div class="phones rv">{phones}</div>
  <p class="mail">Or email us at <a href="mailto:info@opticalmeria.com">info@opticalmeria.com</a></p>
 </div>
</section>
'''

def footer(path):
    es = ES_OF[path]
    stores = "".join(f'<li><a href="{u("en/opticians/" + s["slug"] + "/")}">{s["town"]}</a> · <a href="tel:{s["tel_e164"]}">{INTL[s["slug"]]}</a></li>' for s in STORES)
    nav = "".join(f'<li><a href="{u(p)}">{t}</a></li>' for p, t in NAV)
    calls = "".join(f'<a class="btn{" ghost" if i else ""}" href="tel:{s["tel_e164"]}">{PHONE_SVG}{s["town"]}</a>' for i, s in enumerate(STORES))
    return f'''</main>
<footer class="foot">
 <div class="wrap">
  <p class="big" aria-hidden="true">Óptica Almería</p>
  <div>
   <a class="logo" href="{u('en/')}" aria-label="Óptica Almería, home">{LOGO.format(n=2)}<span>Óptica Almería</span></a>
   <p>Opticians and hearing care specialists in Albox and Huércal-Overa since 1980. Varilux specialist centre since 2000.</p>
  </div>
  <div><h2>Our stores</h2><ul>{stores}</ul></div>
  <div><h2>This site</h2><ul>{nav}<li><a href="{LIVE}blog/" hreflang="es">Carmen’s blog (in Spanish)</a></li><li><a class="lang2" href="{u(slash(es))}" hreflang="es" lang="es">Versión en español</a></li></ul></div>
  <div><h2>Write to us</h2><ul><li><a href="mailto:info@opticalmeria.com">info@opticalmeria.com</a></li></ul></div>
  <p class="legal"><span>© Óptica Almería · Óptica Berruezo, S. L.</span><a href="{LIVE}aviso-legal/" hreflang="es">Legal notice</a><a href="{LIVE}politica-de-privacidad/" hreflang="es">Privacy</a><a href="{LIVE}politica-de-cookies/" hreflang="es">Cookies</a><span>(in Spanish)</span><button type="button" class="cky-banner-element linkbtn">Cookie settings</button><a class="credit" href="https://geovisibilidad.com/">Web: geovisibilidad</a></p>
 </div>
</footer>
<nav class="callbar" aria-label="Call a shop">{calls}</nav>
<script src="{a('site.js')}?v={B.VER}" defer></script>
</body>
</html>
'''

def page(path, title, desc, ld, body, cur="", preload=""):
    out = B.OUT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(title, desc, path, ld, preload) + header(cur, path) + body + footer(path), encoding="utf-8")
    print("ok", out.relative_to(B.OUT))

def phead(crumb, h1, lead, img=None, imgw=None, alt=""):
    fig = f'<figure>{pic(img, imgw, alt, "(max-width:1020px) 100vw, 45vw", eager=True)}</figure>' if img else ""
    return f'''<header class="phead">
 <div class="wrap">
  <div>
   <p class="crumbs"><a href="{u('en/')}">Home</a> / {crumb}</p>
   <h1 class="h1">{h1}</h1>
   <p class="lead">{lead}</p>
  </div>
  {fig}
 </div>
</header>
'''

def store_card(s, h="h3"):
    return f'''<article class="store rv">
 <figure>{pic(s["img"], s["imgw"], ALT[s["slug"]], "(max-width:700px) 100vw, 50vw")}</figure>
 <div class="in">
  <{h} class="h3"><a href="{u("en/opticians/" + s["slug"] + "/")}" style="text-decoration:none">{s["town"]}</a></{h}>
  <address>{s["street"]}, {s["cp"]} {s["town"]} (Almería)</address>
  <a class="tel" href="tel:{s["tel_e164"]}">{INTL[s["slug"]]}</a>
  <p class="hours">{HOURS}</p>
  <div class="acts"><a class="btn" href="tel:{s["tel_e164"]}">{PHONE_SVG}Call</a><a class="btn ghost" href="{s["maps"]}" rel="noopener">{PIN_SVG}Directions</a></div>
 </div>
</article>'''

PHONES_LINE = 'Albox, <a href="tel:+34950430012">+34 950 43 00 12</a>; Huércal-Overa, <a href="tel:+34950134199">+34 950 13 41 99</a>'

# ---------- HOME ----------
FAQ_HOME = [
    ("How often should I have my eyes tested?",
     "The World Health Organization recommends an eye test once a year, even if you don’t wear glasses. It keeps your prescription up to date and helps catch problems such as cataracts early."),
    ("Do you do hearing tests and hearing aids?",
     "Yes. We do video otoscopy, pure-tone audiometry in a soundproof booth and speech audiometry, and we fit digital hearing aids, both in-the-ear and behind-the-ear. Call your nearest shop to book."),
    ("What does being a Varilux specialist centre mean?",
     "It’s a title Essilor, the maker of Varilux lenses, gives to opticians with precise measuring equipment and staff trained to fit varifocals. We have held it since 2000."),
    ("Do I need an appointment for an eye test?",
     "It’s better. That way we can see you without rushing and with the consulting room free. Call Albox on +34 950 43 00 12 or Huércal-Overa on +34 950 13 41 99."),
    ("Do you fit contact lenses?",
     "Yes. We fit contact lenses and also Ortho-K, lenses you wear overnight that correct short-sightedness during the day."),
]

def home():
    proof = '''<div class="proof"><ul class="wrap">
  <li><svg class="pi" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 4.5l3.4 7 7.6 1.1-5.5 5.4 1.3 7.6L16 22l-6.8 3.6 1.3-7.6L5 12.6l7.6-1.1z"/></svg><b>4.9</b><span>Google rating, from 38 reviews (Albox)</span></li>
  <li><svg class="pi" viewBox="0 0 32 32" aria-hidden="true"><circle cx="10" cy="17" r="6"/><circle cx="22" cy="17" r="6"/><path d="M4 17l-1.5-5M28 17l1.5-5"/></svg><b>2000</b><span>Varilux specialist centre since that year</span></li>
  <li><svg class="pi" viewBox="0 0 32 32" aria-hidden="true"><path d="M5 13v14h22V13M3.5 8.5L6 4h20l2.5 4.5v1.8a3.6 3.6 0 0 1-6.25 2.4 3.6 3.6 0 0 1-6.25 0 3.6 3.6 0 0 1-6.25 0A3.6 3.6 0 0 1 3.5 10.3z"/><path d="M13 27v-7h6v7"/></svg><b>1980</b><span>we opened our first shop in Albox</span></li>
  <li><svg class="pi" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 28s9-8.2 9-15a9 9 0 0 0-18 0c0 6.8 9 15 9 15z"/><circle cx="16" cy="13" r="3.2"/></svg><b>2</b><span>shops, in Albox and Huércal-Overa</span></li>
 </ul></div>'''
    svcs = [
        ("Eye test", "We measure how well you see far and near, and check how both eyes work together."),
        ("Retinal photography", "A photo of the back of the eye, so we can keep an eye on your retina from one test to the next."),
        ("Contact lenses", "We fit your lenses and show you how to put them in and look after them."),
        ("Ortho-K", "Lenses you wear while you sleep that correct short-sightedness during the day, with no glasses."),
        ("Low vision", "Optical aids for people who no longer see well even with glasses: magnifiers, filters and telescopes."),
    ]
    svc_html = "".join(f"<li><h3>{x}</h3><p>{y}</p></li>" for x, y in svcs)
    tests = [
        ("Video otoscopy", "We look at the ear canal and eardrum with a camera linked to a screen, and you see it with us."),
        ("Pure-tone audiometry", "In a soundproof booth you listen to tones at different volumes, so we find your hearing threshold."),
        ("Speech audiometry", "The same test with words, so we know how much of what you hear you actually understand."),
        ("Discomfort level", "We find the volume at which sounds start to bother you, so your hearing aid never goes that far."),
    ]
    quiz = ["You turn the TV up louder than everyone else", "You often ask people to repeat themselves",
            "In a bar or at a family meal you struggle to follow the conversation", "People seem to mumble",
            "You hear ringing or buzzing when it’s quiet"]
    quiz_html = "".join(f'<li><label><input type="checkbox"><span>{q}</span></label></li>' for q in quiz)
    tests_html = "".join(f"<li class='rv'><h3>{x}</h3><p>{y}</p></li>" for x, y in tests)
    stores_html = "".join(store_card(s) for s in STORES)
    posts_html = "".join(f'<li><a href="{LIVE}{s}/" hreflang="es" lang="es"><time datetime="{d}">{date_en(d)}</time><h3>{t}</h3><span class="arrow" aria-hidden="true">→</span></a></li>' for s, t, d in B.POSTS[:4])
    faq_html = "".join(f"<details><summary>{q}</summary><p>{x}</p></details>" for q, x in FAQ_HOME)
    body = f'''
<section class="hero6" aria-labelledby="h1">
 <div class="h6-copy">
  <p class="lbl">Albox and Huércal-Overa · since 1980</p>
  <h1 class="h1" id="h1">Glasses made to measure for your eyes</h1>
  <div class="ctas"><a class="btn" href="#cita">Book an appointment</a><a class="btn ghost" href="#tiendas">See our shops</a></div>
 </div>
 <figure class="h6-photo"><picture><source type="image/avif" srcset="{a("img/tabernas-800.avif")} 800w, {a("img/tabernas-1200.avif")} 1200w, {a("img/tabernas-1600.avif")} 1600w" sizes="(max-width:1020px) 100vw, 50vw"><img src="{a("img/tabernas-1200.webp")}" srcset="{a("img/tabernas-800.webp")} 800w, {a("img/tabernas-1200.webp")} 1200w, {a("img/tabernas-1600.webp")} 1600w" sizes="(max-width:1020px) 100vw, 50vw" alt="Woman wearing tortoiseshell glasses in the Tabernas desert at sunset" width="1600" height="1986" fetchpriority="high"></picture></figure>
 <div class="seal" aria-hidden="true"><svg viewBox="0 0 200 200"><defs><path id="sealp" d="M100,100 m-76,0 a76,76 0 1,1 152,0 a76,76 0 1,1 -152,0"/></defs><text><textPath href="#sealp" textLength="474" lengthAdjust="spacing">VARILUX SPECIALIST CENTRE · SINCE 2000 · ALBOX · HUÉRCAL-OVERA ·</textPath></text></svg>{LOGO.format(n=9)}</div>
</section>
{proof}

<section aria-labelledby="rev-t">
 <div class="wrap exam">
  <figure class="chart rv" aria-label="Visual acuity chart">
   <div class="rows"><p>Ó<small>0.1</small></p><p>P T<small>0.2</small></p><p>I C A<small>0.4</small></p><p>A L M E R<small>0.6</small></p><p>Í A · A L B O X<small>0.8</small></p><p><span>HUÉRCAL-OVERA</span><small>1.0</small></p></div>
   <div class="tune"><label for="dio">Turn the dial until it reads clearly</label><div class="tune-row"><input type="range" id="dio" min="-3" max="0" step="0.25" value="-1.75"><output id="dio-out" for="dio">−1.75</output></div><p class="tune-ok" aria-live="polite"></p></div>
   <figcaption>This chart is just for fun. The real one is waiting for you in our consulting room.</figcaption>
  </figure>
  <div>
   <h2 class="h2 rv" id="rev-t">Once a year, even if you see well</h2>
   <p class="lead rv">We are a registered healthcare establishment. In the consulting room we measure your prescription and check the health of your eyes, which is how we catch things early, before you notice them.</p>
   <ul class="svc-list rv">{svc_html}</ul>
   <p style="margin-top:28px" class="rv"><a class="tlink" href="{u('en/eye-care/')}">Short-sightedness, astigmatism, cataracts: what each one means <span class="arrow">→</span></a></p>
  </div>
 </div>
</section>

<section class="band" aria-labelledby="prog-t">
 <div class="wrap prog">
  <figure class="rv">{pic("pareja", [640, 1230], "Couple in their fifties wearing acetate glasses in the afternoon light", "(max-width:1020px) 100vw, 55vw")}</figure>
  <div>
   <p class="lbl rv">Varifocals</p>
   <h2 class="h2 rv" id="prog-t">See far, in between and close up with the same pair of glasses</h2>
   <p class="lead rv">Varifocals only work if they’re measured properly: the height of each pupil, the distance between your eyes, how the frame sits on your face. That’s why Essilor made us a Varilux specialist centre, and why we take those measurements with precision instruments.</p>
   <figure class="zones rv">
    <svg viewBox="0 0 200 170" aria-hidden="true"><path d="M22 14H178Q192 14 192 30V104Q192 156 128 158H72Q8 156 8 104V30Q8 14 22 14Z" fill="var(--card)" stroke="currentColor" stroke-width="1.5"/><path d="M8 66Q100 84 192 66" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 5"/><path d="M20 118Q100 104 180 118" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 5"/><path d="M100 70V114" stroke="var(--accent)" stroke-width="10" stroke-linecap="round" opacity=".18"/></svg>
    <figcaption><ol><li><b>Distance</b><span>the road, the TV</span></li><li><b>Intermediate</b><span>the computer, the dashboard</span></li><li><b>Near</b><span>a book, your phone</span></li></ol></figcaption>
   </figure>
   <dl class="rv"><dt>2000</dt><dd>the year Essilor made us a Varilux specialist centre.</dd></dl>
  </div>
 </div>
</section>

<section id="audifonos" aria-labelledby="ear-t">
 <div class="wrap">
  <p class="como rv" aria-hidden="true">Pardon?</p>
  <div class="ear-grid">
   <div><h2 class="h2 rv" id="ear-t">When you can hear, but can’t make out the words</h2></div>
   <p class="lead rv">Hearing loss comes on little by little and nearly always in both ears, which is why we tend to notice it late. A full hearing assessment takes four painless tests.</p>
  </div>
  <svg class="wave rv" viewBox="0 0 1200 80" preserveAspectRatio="none" aria-hidden="true"><path class="lit" d="M0 40 C 40 4, 80 76, 120 40 S 200 8, 240 40 S 320 68, 360 40 S 440 16, 480 40 S 560 60, 600 40 S 680 26, 720 40 S 800 52, 840 40 S 920 34, 960 40 S 1040 46, 1080 40 S 1160 40, 1200 40"/></svg>
  <div class="quiz rv">
   <h3 class="h3">Does any of this sound familiar?</h3>
   <ul>{quiz_html}</ul>
   <p class="quiz-out" aria-live="polite">Tick the ones that ring a bell.</p>
  </div>
  <ol class="tests">{tests_html}</ol>
  <p class="ear-more rv">With the results we explain which hearing aid suits you, in-the-ear or behind-the-ear, and fit it to your hearing. <a class="tlink" href="{u('en/hearing-aids/')}">How a hearing aid works <span class="arrow">→</span></a></p>
 </div>
</section>

<section class="band" aria-labelledby="mar-t">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2 rv" id="mar-t">Frames chosen calmly, in front of a mirror</h2></div>
  <p class="lead rv">We only work with leading brands, from the classic to the daring. Come and try them on: we’ll tell you honestly which ones suit you and which don’t.</p></div>
  <div class="frames">
   <figure class="f1 rv">{pic("gafas-sol-desierto", [640, 1170], "Two women wearing sunglasses among desert rocks in Almería", "(max-width:700px) 100vw, 56vw")}</figure>
   <figure class="rv">{pic("etnia", [640, 1200], "Tortoiseshell acetate frame with coloured temples", "(max-width:700px) 100vw, 42vw")}</figure>
   <figure class="rv">{pic("monturas-redondas", [640, 1126], "Four round acetate sunglasses in different colours", "(max-width:700px) 100vw, 42vw")}</figure>
  </div>
  <div class="marquee rv"><ul class="brands" aria-label="Some of our brands"><li>Varilux</li><li>Ray-Ban</li><li>Persol</li><li>LOEWE</li><li>Silhouette</li><li>Gigi Studios</li><li>Emporio Armani</li><li>Oakley</li></ul><ul class="brands" aria-hidden="true"><li>Varilux</li><li>Ray-Ban</li><li>Persol</li><li>LOEWE</li><li>Silhouette</li><li>Gigi Studios</li><li>Emporio Armani</li><li>Oakley</li></ul></div>
  <p style="margin-top:22px" class="rv"><a class="tlink" href="{u('en/brands/')}">All our brands <span class="arrow">→</span></a></p>
 </div>
</section>

<section id="tiendas" aria-labelledby="tie-t">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2 rv" id="tie-t">In Albox and Huércal-Overa</h2></div>
  <p class="lead rv">Both shops have an optometry consulting room. Call ahead and we’ll give you a time.</p></div>
  <div class="stores">{stores_html}</div>
 </div>
</section>

<section class="band" aria-labelledby="his-t">
 <div class="wrap story">
  <figure class="rv">{pic("pita", [600, 1057], "A flowering agave in the Almería desert under a sunset sky", "(max-width:1020px) 100vw, 38vw")}</figure>
  <div>
   <p class="lbl rv">About us</p>
   <p class="year rv" aria-hidden="true">1980</p>
   <h2 class="h2 rv" id="his-t">A journey that began in Albox</h2>
   <p class="lead rv">We’ve seen in a new century, the technology revolution and more fashions than we can count, and we’ve changed our look more than once. What hasn’t changed is how we work: looking after your eyes with quality, the latest advances and the warmth of a friend.</p>
   <p class="rv" style="margin-top:28px"><a class="tlink" href="{u('en/about-us/')}">Who we are <span class="arrow">→</span></a></p>
  </div>
 </div>
</section>

<section aria-labelledby="blog-t">
 <div class="wrap">
  <div class="sec-head"><div><h2 class="h2 rv" id="blog-t">Carmen’s blog, in Spanish</h2></div>
  <p class="lead rv">Tips on caring for your contact lenses, resting your eyes from the computer, and the odd frame we’ve fallen in love with. Carmen writes it in Spanish.</p></div>
  <ul class="posts rv">{posts_html}</ul>
 </div>
</section>

<section class="band" aria-labelledby="faq-t">
 <div class="wrap faq">
  <div><h2 class="h2 rv" id="faq-t">What people ask us most at the counter</h2></div>
  <div class="rv">{faq_html}</div>
 </div>
</section>
{cita_block()}'''
    ld = [ORG] + [store_ld_en(s) for s in STORES] + [faq_ld(FAQ_HOME), {"@type": "WebPage", "@id": LIVE + "en/#webpage", "url": LIVE + "en/", "name": "Óptica Almería", "inLanguage": "en", "isPartOf": {"@id": LIVE + "#web"}}]
    pre = f'<link rel="preload" as="image" href="{a("img/tabernas-1200.avif")}" imagesrcset="{a("img/tabernas-800.avif")} 800w, {a("img/tabernas-1200.avif")} 1200w, {a("img/tabernas-1600.avif")} 1600w" imagesizes="(max-width:1020px) 100vw, 50vw" type="image/avif" fetchpriority="high">'
    page("en", "Optician in Albox & Huércal-Overa | Óptica Almería",
         "Opticians and hearing care in Albox and Huércal-Overa since 1980. Eye tests, Varilux varifocals, contact lenses and hearing aids. Book an appointment.",
         ld, body, preload=pre)

# ---------- EYE CARE ----------
def eye_care():
    defs = [
        ("Short-sightedness (myopia)", "The image focuses in front of the retina, so distant things look blurred. People often squint to see better, and if it isn’t properly corrected it causes eye strain and headaches.",
         "It’s corrected with concave lenses, thinner in the middle than at the edges. Through them things look slightly smaller."),
        ("Long-sightedness (hyperopia)", "The image focuses behind the retina and close work is hard. With a low prescription, young eyes compensate by working harder, but the price is headaches, watery eyes and red eyes after reading.",
         "It’s corrected with convex lenses, thicker in the middle."),
        ("Astigmatism", "The cornea is slightly more curved in one direction than the other, so the image is distorted both far and near. The symptoms are similar to long-sightedness: headaches, tiredness and irritation.",
         "It rarely comes alone: it usually goes with short- or long-sightedness."),
        ("Cataracts", "They aren’t a focusing problem, but they change your prescription: they reduce sharpness and cause glare. They appear in about 65% of people over 70, earlier with a lot of sun or a family history.",
         "At first a change of prescription makes up for them. Later on, surgery is needed."),
    ]
    d = "".join(f'<div><h3>{x}</h3><p>{y}</p><p>{z}</p></div>' for x, y, z in defs)
    body = phead("Eye care", "Your eye test in Albox and Huércal-Overa",
                 "Wearing glasses just means your eye focuses slightly off target, and that can be put right. What matters is checking it in time.",
                 "lentillas", [640, 1400], "A young man about to put in a contact lens") + f'''
<section style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap split">
  <nav class="toc" aria-label="On this page"><ul><li><a href="#revision">The eye test</a></li><li><a href="#defectos">Common eye conditions</a></li><li><a href="#servicios">What we do</a></li></ul></nav>
  <div class="prose">
   <h2 id="revision">An eye test once a year</h2>
   <p>The World Health Organization recommends having your eyes tested at least once a year, to keep your prescription right and to catch eye conditions while they are still easy to treat. Even more so if they run in your family.</p>
   <p>The test is done by a qualified optometrist and it doesn’t hurt: you read letters, look at lights and we take a photo or two of your eye.</p>
   <h2 id="defectos">Common eye conditions, explained</h2>
   <div class="defs">{d}</div>
   <h2 id="servicios">What we do in the consulting room</h2>
   <ul>
    <li><strong>Eye tests</strong> for distance and near, and how both eyes work together.</li>
    <li><strong>Retinal photography</strong>: a photo of the back of the eye to compare from year to year.</li>
    <li><strong>Varilux varifocals</strong>, measured with precision instruments. We have been a Varilux specialist centre since 2000.</li>
    <li><strong>Contact lenses</strong> and <strong>Ortho-K</strong>, which corrects short-sightedness while you sleep.</li>
    <li><strong>Low vision</strong>: magnifiers, filters and other aids for people who no longer see well with glasses.</li>
   </ul>
   <p class="note">If you have any questions about your eyes, call your nearest shop and we’ll give you a time: {PHONES_LINE}.</p>
  </div>
 </div>
</section>
{cita_block()}'''
    page("en/eye-care", "Eye Tests in Albox & Huércal-Overa | Óptica Almería",
         "Short-sightedness, long-sightedness, astigmatism and cataracts explained. Yearly eye tests, Varilux varifocals, contact lenses and Ortho-K in Albox.",
         [ORG, crumbs_ld([("en/", "Home"), ("en/eye-care/", "Eye care")])], body, cur="en/eye-care/")

# ---------- HEARING AIDS ----------
def hearing():
    body = phead("Hearing aids", "Hearing tests and hearing aids in Albox and Huércal-Overa",
                 "Hearing loss comes on slowly and nearly always in both ears. The sooner it’s picked up, the more sounds you get back.",
                 "audifono", [768], "Behind-the-ear hearing aid on a fingerprint") + f'''
<section style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap split">
  <nav class="toc" aria-label="On this page"><ul><li><a href="#causas">Why hearing goes</a></li><li><a href="#tipos">Types of hearing loss</a></li><li><a href="#pruebas">The tests</a></li><li><a href="#audifonos">Types of hearing aid</a></li></ul></nav>
  <div class="prose">
   <h2 id="causas">Why hearing goes</h2>
   <p>Hearing loss is difficulty hearing certain sounds. Because it creeps up gradually, we often only notice it once it’s significant. The most common causes are:</p>
   <ul><li>Age.</li><li>Family history.</li><li>Spending a lot of time around loud noise.</li><li>Infections and some medicines.</li><li>Knocks and accidents.</li></ul>
   <h2 id="tipos">Types of hearing loss</h2>
   <p>Depending on how much is lost, hearing loss is mild, moderate, severe or profound. Depending on where the problem lies:</p>
   <div class="defs">
    <div><h3>Conductive</h3><p>Sound doesn’t reach the receptors of the inner ear properly. It affects all pitches equally and a good part of the hearing can usually be recovered.</p></div>
    <div><h3>Sensorineural</h3><p>The receptors are damaged. It doesn’t affect all pitches equally, and the typical complaint is “I can hear, but I can’t understand”.</p></div>
    <div><h3>Mixed</h3><p>Both together: sound isn’t conducted properly and the receptors are damaged too.</p></div>
   </div>
   <h2 id="pruebas">The tests we do</h2>
   <ul>
    <li><strong>Video otoscopy.</strong> We look at the ear canal and eardrum with an otoscope linked to a screen.</li>
    <li><strong>Pure-tone audiometry.</strong> In a soundproof booth, with tones at different volumes, by air and bone conduction.</li>
    <li><strong>Speech audiometry.</strong> The same, but with words, to find out how much you understand.</li>
    <li><strong>Discomfort level.</strong> The volume at which sounds start to bother you.</li>
   </ul>
   <h2 id="audifonos">Types of hearing aid</h2>
   <p>All the hearing aids we fit are digital: smaller, more powerful and adjustable to your hearing. The type depends on your hearing assessment.</p>
   <div class="defs">
    <div><h3>In the ear</h3><p>They sit in the ear canal and the visible part of the ear, custom-made from an impression we take in the consulting room. The smallest, CIC, are completely hidden.</p></div>
    <div><h3>Behind the ear</h3><p>A small case behind the ear connected by a thin tube to an earpiece inside the ear, with a custom or standard mould. They are usually more powerful.</p></div>
   </div>
   <p class="note">Book your hearing assessment: {PHONES_LINE}.</p>
  </div>
 </div>
</section>
{cita_block()}'''
    page("en/hearing-aids", "Hearing Tests & Hearing Aids in Albox | Óptica Almería",
         "Full hearing assessment with video otoscopy and audiometry in a soundproof booth. Digital in-the-ear and behind-the-ear hearing aids in Albox and Huércal-Overa.",
         [ORG, crumbs_ld([("en/", "Home"), ("en/hearing-aids/", "Hearing aids")])], body, cur="en/hearing-aids/")

# ---------- BRANDS ----------
GROUPS = {"Españolas": "Spanish", "Del resto de Europa": "From the rest of Europe", "De fuera de Europa": "From outside Europe"}
def brands():
    groups = "".join(f'<div class="bgroup"><h3>{GROUPS[t]}</h3><ul class="blist">' + "".join(f"<li>{m}</li>" for m in ms) + "</ul></div>" for t, ms in B.MARCAS)
    body = phead("Glasses & brands", "Frames from leading brands",
                 "From the classic to the daring. Whatever your style, we’ll find the glasses that suit you.",
                 "etnia", [640, 1200], "Tortoiseshell frame with coloured temples") + f'''
<section style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap">
  <div class="frames">
   <figure class="f1 rv">{pic("gafas-sol-desierto", [640, 1170], "Two women wearing sunglasses among desert rocks in Almería", "(max-width:700px) 100vw, 56vw")}</figure>
   <figure class="rv">{pic("persol", [640, 945], "Persol Reflex Edition campaign in black and white", "(max-width:700px) 100vw, 42vw")}</figure>
   <figure class="rv">{pic("monturas-redondas", [640, 1126], "Four round acetate sunglasses", "(max-width:700px) 100vw, 42vw")}</figure>
  </div>
  <div class="prose" style="margin-top:56px">
   <h2>Leading brands only</h2>
   <p>That way we can guarantee every frame and every lens is top quality and meets all health regulations. These are the {B.N_MARCAS} frame and sunglasses brands we stock right now, grouped by where they come from. For prescription lenses we work with Varilux, by Essilor. Come and try them on, no obligation.</p>
  </div>
  <div class="brandgroups">{groups}</div>
 </div>
</section>
{cita_block()}'''
    page("en/brands", "Designer Glasses & Sunglasses in Albox | Óptica Almería",
         f"{B.N_MARCAS} frame and sunglasses brands, from Ray-Ban, Persol and LOEWE to Gigi Studios and Silhouette, plus Varilux lenses, in Albox and Huércal-Overa.",
         [ORG, crumbs_ld([("en/", "Home"), ("en/brands/", "Glasses & brands")])], body, cur="en/brands/")

# ---------- ABOUT US ----------
def about():
    body = phead("About us", "Opticians in the Almanzora valley since 1980",
                 "Óptica Almería is a journey that began in Albox and has travelled the whole province, always alongside our patients and friends.",
                 "pita", [600, 1057], "Flowering agave in the Almería desert") + f'''
<section style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap split">
  <nav class="toc" aria-label="On this page"><ul><li><a href="#historia">Our story</a></li><li><a href="#varilux">Varilux specialist</a></li><li><a href="#sanitario">Healthcare establishment</a></li></ul></nav>
  <div class="prose">
   <h2 id="historia">A journey through time, and friendship</h2>
   <p>We’ve seen in a new century, lived through the technology revolution and globalisation, watched more fashions come and go than we can count, and all of it alongside you. Over the years we’ve changed our look, but we still value what really matters: looking after your eyes with the highest quality and the latest technical advances.</p>
   <p>Our philosophy has always been the same: give you the best solution at the best price, with a selection of exclusive brands and new lens and frame designs for every need, whether it’s about design or fashion.</p>
   <h2 id="varilux">Varilux specialist centre since 2000</h2>
   <p>It’s a title Essilor awards to opticians who give the best service and care and work with the latest advances. To hold it, our shops have the most precise measuring instruments on the market and highly qualified staff.</p>
   <h2 id="sanitario">We are a healthcare establishment</h2>
   <p>Our work is about your health, both your sight and your hearing. That’s why every test is done by a qualified professional, taking all the time it needs.</p>
  </div>
 </div>
</section>
{cita_block()}'''
    page("en/about-us", "About Us · Opticians in Albox since 1980 | Óptica Almería",
         "Óptica Almería: opticians in Albox and Huércal-Overa since 1980 and a Varilux specialist centre since 2000. A healthcare establishment for eyes and ears.",
         [ORG, crumbs_ld([("en/", "Home"), ("en/about-us/", "About us")])], body, cur="en/about-us/")

# ---------- STORES ----------
def stores():
    cards = "".join(store_card(s, "h2") for s in STORES)
    body = phead("Our stores", "Two shops, in Albox and Huércal-Overa",
                 "Both have an optometry consulting room. Call before you come and we’ll give you a time, so you don’t have to wait.") + f'''
<section style="padding-top:0">
 <div class="wrap"><div class="stores">{cards}</div>
 <p class="note" style="margin-top:36px">Any questions? Email us at <a href="mailto:info@opticalmeria.com">info@opticalmeria.com</a> and we’ll get back to you.</p></div>
</section>
{cita_block()}'''
    page("en/stores", "Our Opticians in Albox & Huércal-Overa | Óptica Almería",
         "Óptica Almería at Avenida Puente 9, Albox (+34 950 43 00 12) and Avenida Guillermo Reyna 16, Huércal-Overa (+34 950 13 41 99). Directions and appointments.",
         [ORG] + [store_ld_en(s) for s in STORES] + [crumbs_ld([("en/", "Home"), ("en/stores/", "Our stores")])], body, cur="en/stores/")

# ---------- ONE PAGE PER SHOP ----------
def shop(s):
    other = [x for x in STORES if x is not s][0]
    tel = INTL[s["slug"]]
    body = phead(f'<a href="{u("en/stores/")}">Our stores</a> / {s["town"]}', f"Óptica Almería in {s['town']}",
                 f"{s['street']}. Eye tests, Varilux varifocals, contact lenses and hearing aids. Call {tel} and we’ll give you a time.",
                 s["img"], s["imgw"], ALT[s["slug"]]) + f'''
<section style="padding-top:clamp(24px,3vw,40px)">
 <div class="wrap">
  <dl class="info">
   <div><dt>Address</dt><dd>{s["street"]}<br>{s["cp"]} {s["town"]} (Almería), Spain</dd></div>
   <div><dt>Phone</dt><dd><a href="tel:{s["tel_e164"]}">{tel}</a></dd></div>
   <div><dt>Opening hours</dt><dd>Monday to Friday, 9:30am to 2pm and 5:40pm to 8:30pm<br>In summer, afternoons 5pm to 8pm<br>Saturdays, 10am to 2pm</dd></div>
  </dl>
  <div class="ctas" style="margin:32px 0 56px"><a class="btn" href="tel:{s["tel_e164"]}">{PHONE_SVG}Call {s["town"]}</a><a class="btn ghost" href="{s["maps"]}" rel="noopener">{PIN_SVG}Directions</a></div>
  <div class="map" data-src="{s["embed"]}" data-title="Map of Óptica Almería in {s["town"]}"><button type="button" class="map-on"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg><span>Show the map</span><small>Clicking loads Google Maps, which uses its own cookies.</small></button></div>
  <div class="prose" style="margin-top:56px">
   <h2>What we do at this shop</h2>
   <ul>
    <li>Eye tests and retinal photography.</li>
    <li>Varilux varifocals, measured with precision instruments.</li>
    <li>Contact lenses and Ortho-K.</li>
    <li>Prescription glasses and sunglasses from leading brands.</li>
    <li>Hearing assessments and hearing aids.</li>
   </ul>
   <p>Is the other shop handier for you? We’re also in <a href="{u("en/opticians/" + other["slug"] + "/")}">{other["town"]}, {other["street"]}</a>.</p>
  </div>
 </div>
</section>
{cita_block()}'''
    page(f"en/opticians/{s['slug']}", f"Optician in {s['town']} · Hearing Aids | Óptica Almería",
         f"Óptica Almería at {s['street']}, {s['town']}. Eye tests, Varilux varifocals, contact lenses and hearing aids. Phone {tel}.",
         [ORG, store_ld_en(s), crumbs_ld([("en/", "Home"), ("en/stores/", "Our stores"), (f"en/opticians/{s['slug']}/", s["town"])])], body, cur="en/stores/")

if __name__ == "__main__":
    home(); eye_care(); hearing(); brands(); about(); stores()
    for s in STORES: shop(s)
