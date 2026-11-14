<?php
/*
Plugin Name: Óptica Almería · diseño nuevo (v5)
Description: Sirve la portada y las páginas de servicios y tiendas con el diseño nuevo. El blog, las entradas y el escritorio siguen en WordPress. Para volver a la web anterior basta con desactivar este plugin.
Version: 5.7
Author: Antonio Martínez Rosado
*/
if (!defined('ABSPATH')) exit;

function ov5_trozos($html) {
    $out = '';
    if (preg_match_all('#<(script|style)\b[^>]*>.*?</\1>#s', $html, $m)) {
        foreach ($m[0] as $t) {
            if (preg_match('#cookie-law-info|cky|googletagmanager|gtag\(|metricool#i', $t)) $out .= $t . "\n";
        }
    }
    return $out;
}

// Google Analytics y Metricool solo cuando el visitante acepta «Analítica» en el aviso de CookieYes.
// Antes iba en el plugin WP Headers and Footers (desactivado el 10/11/2026: Wordfence bloquea guardar ese formulario).
// La meta de verificación de Search Console también sale de aquí.
add_action('wp_head', function () {
  if (is_admin()) return;
  echo "<meta name=\"google-site-verification\" content=\"0YPlPvpoRA9SeORL0uxpqpZ5tDNcMUuYufSjYXVFE6w\" />\n";
  echo "<script id=\"ov5-consent\">/* googletagmanager + metricool tras consentimiento */\n(function(){var cargado=false;function cargar(){if(cargado)return;cargado=true;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-JX418GQGP7';document.head.appendChild(s);window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};gtag('js',new Date());gtag('config','G-JX418GQGP7');var m=document.createElement('script');m.src='https://tracker.metricool.com/resources/be.js';m.onload=function(){beTracker.t({hash:'d28a629050eeb5d96ad3c05f9355aec4'})};document.head.appendChild(m);}\nfunction mirar(){try{var c=window.getCkyConsent&&getCkyConsent();if(c&&c.categories&&c.categories.analytics)cargar();}catch(e){}}\ndocument.addEventListener('cookieyes_consent_update',function(e){if(e.detail&&e.detail.accepted&&e.detail.accepted.indexOf('analytics')>-1)cargar();});\nif(document.readyState!=='loading')mirar();else document.addEventListener('DOMContentLoaded',mirar);window.addEventListener('load',mirar);})();</script>\n";
}, 1);
// ---------- Versión inglesa del blog y de los legales (5.7) ----------
// Traducciones: site/en/traducciones.json (entradas existentes) + campo «ov5_en» de cada entrada o página
// (JSON con path, title, seo_title, desc, html y, opcional, image). El blog automático escribe ese campo.
add_action('init', function () {
    foreach (array('post', 'page') as $t) {
        register_post_meta($t, 'ov5_en', array('type' => 'string', 'single' => true, 'show_in_rest' => true,
            'auth_callback' => function () { return current_user_can('edit_posts'); }));
    }
});

function ov5_en_entradas() {
    static $c = null;
    if ($c !== null) return $c;
    $c = array();
    $f = __DIR__ . '/site/en/traducciones.json';
    if (is_file($f)) {
        foreach ((array) json_decode(file_get_contents($f), true) as $e) {
            if (!empty($e['wp_id']) && get_post_status($e['wp_id']) !== 'publish') continue;
            $c[$e['path']] = $e;
        }
    }
    $ids = get_posts(array('post_type' => array('post', 'page'), 'post_status' => 'publish', 'numberposts' => 300,
                           'meta_key' => 'ov5_en', 'fields' => 'ids'));
    foreach ($ids as $id) {
        $e = json_decode((string) get_post_meta($id, 'ov5_en', true), true);
        if (!is_array($e) || empty($e['path']) || empty($e['title']) || empty($e['html'])) continue;
        $e['path'] = trim(preg_replace('#[^a-z0-9/-]#', '', strtolower($e['path'])), '/');
        $e['wp_id'] = $id;
        $e['type'] = get_post_type($id);
        $e['es_url'] = get_permalink($id);
        if (empty($e['date'])) $e['date'] = get_the_date('Y-m-d', $id);
        if (empty($e['image']) && has_post_thumbnail($id)) {
            $im = wp_get_attachment_image_src(get_post_thumbnail_id($id), 'large');
            if ($im) $e['image'] = array('src' => $im[0], 'w' => $im[1], 'h' => $im[2], 'alt' => isset($e['image_alt']) ? $e['image_alt'] : '');
        }
        $c[$e['path']] = $e;
    }
    return $c;
}

function ov5_en_por_id($id) {
    foreach (ov5_en_entradas() as $e) if (!empty($e['wp_id']) && (int) $e['wp_id'] === (int) $id) return $e;
    return null;
}

function ov5_fecha_en($iso) {
    $t = strtotime($iso);
    return $t ? date('j F Y', $t) : '';
}

function ov5_en_pagina($titulo, $desc, $canon, $es, $body, $ld, $ogtype = 'website', $ogimg = '') {
    $f = __DIR__ . '/site/en/_plantilla.html';
    if (!is_file($f)) return false;
    $alt = '<link rel="alternate" hreflang="es" href="' . esc_url($es) . '">' . "\n"
         . '<link rel="alternate" hreflang="en" href="' . esc_url($canon) . '">' . "\n"
         . '<link rel="alternate" hreflang="x-default" href="' . esc_url($es) . '">';
    $html = strtr(file_get_contents($f), array(
        '%%TITLE%%' => esc_html($titulo), '%%DESC%%' => esc_attr($desc), '%%CANONICAL%%' => esc_url($canon),
        '%%ALTERNATES%%' => $alt, '%%OGTYPE%%' => $ogtype,
        '%%OGIMAGE%%' => esc_url($ogimg ? $ogimg : home_url('/wp-content/uploads/2024/06/optica-almeria.jpg')),
        '%%LD%%' => wp_json_encode(array('@context' => 'https://schema.org', '@graph' => $ld), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        '%%ES%%' => esc_url($es), '%%BODY%%' => $body));
    return $html;
}

function ov5_en_render($sub) {
    $home = home_url('/');
    $miga = function ($items) use ($home) {
        $l = array(); $i = 1;
        foreach ($items as $p => $n) $l[] = array('@type' => 'ListItem', 'position' => $i++, 'name' => $n, 'item' => $home . $p);
        return array('@type' => 'BreadcrumbList', 'itemListElement' => $l);
    };
    $org = array('@id' => $home . '#org');
    if ($sub === 'blog') {
        $posts = array_filter(ov5_en_entradas(), function ($e) { return $e['type'] === 'post'; });
        usort($posts, function ($a, $b) { return strcmp($b['date'], $a['date']); });
        $li = '';
        foreach ($posts as $e) {
            $li .= '<li><a href="' . esc_url($home . 'en/' . $e['path'] . '/') . '"><time datetime="' . esc_attr($e['date']) . '">'
                 . esc_html(ov5_fecha_en($e['date'])) . '</time><h3>' . esc_html($e['title']) . '</h3><span class="arrow" aria-hidden="true">→</span></a></li>';
        }
        $body = '<header class="phead"><div class="wrap"><div><p class="crumbs"><a href="' . esc_url($home . 'en/') . '">Home</a> / Blog</p>'
              . '<h1 class="h1">Addicted to glasses, Carmen’s blog</h1><p class="lead">Advice on eyes, ears and glasses from our opticians in Albox and Huércal-Overa. Carmen writes in Spanish; these are our English translations.</p></div></div></header>'
              . '<section style="padding-top:0"><div class="wrap"><ul class="posts">' . $li . '</ul></div></section>';
        $ld = array($miga(array('en/' => 'Home', 'en/blog/' => 'Blog')),
                    array('@type' => 'Blog', '@id' => $home . 'en/blog/#blog', 'url' => $home . 'en/blog/', 'name' => 'Carmen’s blog', 'inLanguage' => 'en', 'publisher' => $org));
        $blog_es = get_option('page_for_posts') ? get_permalink(get_option('page_for_posts')) : $home . 'blog/';
        return ov5_en_pagina('Carmen’s Blog: Eyes, Ears and Glasses | Óptica Almería',
            'Advice on eye health, contact lenses, varifocals, sunglasses and hearing from Óptica Almería, opticians in Albox and Huércal-Overa.',
            $home . 'en/blog/', $blog_es, $body, $ld);
    }
    $todas = ov5_en_entradas();
    if (!isset($todas[$sub])) return false;
    $e = $todas[$sub];
    $canon = $home . 'en/' . $e['path'] . '/';
    $es_a = '<a href="' . esc_url($e['es_url']) . '" hreflang="es" lang="es">Versión en español</a>';
    $fig = '';
    if (!empty($e['image']['src'])) {
        $im = $e['image'];
        $fig = '<figure><img src="' . esc_url($im['src']) . '" alt="' . esc_attr(isset($im['alt']) ? $im['alt'] : '') . '"'
             . (!empty($im['w']) ? ' width="' . (int) $im['w'] . '" height="' . (int) $im['h'] . '"' : '') . ' fetchpriority="high"></figure>';
    }
    if ($e['type'] === 'post') {
        $crumb = '<a href="' . esc_url($home . 'en/') . '">Home</a> / <a href="' . esc_url($home . 'en/blog/') . '">Blog</a>';
        $lead = '<time datetime="' . esc_attr($e['date']) . '">' . esc_html(ov5_fecha_en($e['date'])) . '</time>. Carmen wrote this post in Spanish; this is our English translation. ' . $es_a;
        $ld = array($miga(array('en/' => 'Home', 'en/blog/' => 'Blog', 'en/' . $e['path'] . '/' => $e['title'])),
            array('@type' => 'BlogPosting', '@id' => $canon . '#post', 'url' => $canon, 'headline' => $e['title'], 'description' => $e['desc'],
                  'datePublished' => $e['date'], 'inLanguage' => 'en', 'author' => $org, 'publisher' => $org,
                  'isPartOf' => array('@id' => $home . 'en/blog/#blog'), 'translationOfWork' => array('@id' => $e['es_url']),
                  'image' => !empty($e['image']['src']) ? $e['image']['src'] : null));
        $ogtype = 'article';
    } else {
        $crumb = '<a href="' . esc_url($home . 'en/') . '">Home</a> / Legal';
        $lead = 'English translation for information only. In case of any discrepancy, the Spanish version prevails. ' . $es_a;
        $ld = array($miga(array('en/' => 'Home', 'en/' . $e['path'] . '/' => $e['title'])));
        $ogtype = 'website';
    }
    $body = '<header class="phead"><div class="wrap"><div><p class="crumbs">' . $crumb . '</p><h1 class="h1">' . esc_html($e['title']) . '</h1>'
          . '<p class="lead">' . $lead . '</p></div>' . $fig . '</div></header>'
          . '<section style="padding-top:clamp(40px,5vw,72px)"><div class="wrap"><div class="prose ov5-art">' . wp_kses_post($e['html']) . '</div></div></section>';
    $tit = !empty($e['seo_title']) ? $e['seo_title'] : $e['title'];
    if (strpos($tit, 'Óptica Almería') === false) $tit .= ' | Óptica Almería';
    return ov5_en_pagina($tit, $e['desc'], $canon, $e['es_url'], $body, $ld, $ogtype, !empty($e['image']['src']) ? $e['image']['src'] : '');
}

function ov5_en_sitemap() {
    $home = home_url('/');
    $u = array('en/', 'en/eye-care/', 'en/hearing-aids/', 'en/brands/', 'en/about-us/', 'en/stores/',
               'en/opticians/albox/', 'en/opticians/huercal-overa/', 'en/blog/');
    foreach (ov5_en_entradas() as $e) $u[] = 'en/' . $e['path'] . '/';
    $x = '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach ($u as $p) $x .= '<url><loc>' . esc_url($home . $p) . '</loc></url>' . "\n";
    return $x . '</urlset>';
}
add_filter('wpseo_sitemap_index', function ($s) {
    return $s . '<sitemap><loc>' . esc_url(home_url('/en/sitemap.xml')) . '</loc><lastmod>' . gmdate('c') . '</lastmod></sitemap>' . "\n";
});

// hreflang en las entradas y páginas españolas que tienen versión inglesa
add_action('wp_head', function () {
    if (is_admin()) return;
    $en = null; $es = null;
    if (is_home() || (get_option('page_for_posts') && is_page(get_option('page_for_posts'))) || is_page('blog')) {
        $en = home_url('/en/blog/'); $es = home_url('/blog/');
    } elseif (is_singular()) {
        $e = ov5_en_por_id(get_queried_object_id());
        if ($e) { $en = home_url('/en/' . $e['path'] . '/'); $es = get_permalink(get_queried_object_id()); }
    }
    if (!$en) return;
    echo '<link rel="alternate" hreflang="es" href="' . esc_url($es) . '">' . "\n"
       . '<link rel="alternate" hreflang="en" href="' . esc_url($en) . '">' . "\n"
       . '<link rel="alternate" hreflang="x-default" href="' . esc_url($es) . '">' . "\n";
}, 2);

add_action('template_redirect', function () {
    if (is_admin() || is_preview()) return;
    foreach (array('s', 'p', 'page_id', 'preview', 'et_fb', 'customize_changeset_uuid') as $q) {
        if (isset($_GET[$q])) return;
    }
    $ruta = trim((string) parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');
    $mapa = array(
        ''                     => 'index.html',
        'tu-salud-visual'      => 'tu-salud-visual/index.html',
        'salud-auditiva'       => 'salud-auditiva/index.html',
        'nuestras-marcas'      => 'nuestras-marcas/index.html',
        'nosotros'             => 'nosotros/index.html',
        'contacto'             => 'contacto/index.html',
        'opticas/albox'        => 'opticas/albox/index.html',
        'opticas/huercal-overa'=> 'opticas/huercal-overa/index.html',
        // versión en inglés (desde 5.6)
        'en'                          => 'en/index.html',
        'en/eye-care'                 => 'en/eye-care/index.html',
        'en/hearing-aids'             => 'en/hearing-aids/index.html',
        'en/brands'                   => 'en/brands/index.html',
        'en/about-us'                 => 'en/about-us/index.html',
        'en/stores'                   => 'en/stores/index.html',
        'en/opticians/albox'          => 'en/opticians/albox/index.html',
        'en/opticians/huercal-overa'  => 'en/opticians/huercal-overa/index.html',
    );
    if ($ruta === 'en/sitemap.xml') {
        status_header(200); header('Content-Type: application/xml; charset=utf-8'); echo ov5_en_sitemap(); exit;
    }
    if (isset($mapa[$ruta])) {
        $f = __DIR__ . '/site/' . $mapa[$ruta];
        if (!is_file($f)) return;
        $html = file_get_contents($f);
    } elseif (strpos($ruta, 'en/') === 0) {
        $html = ov5_en_render(substr($ruta, 3));
        if ($html === false) return;
    } else {
        return;
    }
    // aviso de cookies y analítica: los mismos que ya tiene la web, sacados de WordPress
    ob_start(); wp_head(); $cab = ov5_trozos(ob_get_clean());
    ob_start(); wp_footer(); $pie = ov5_trozos(ob_get_clean());
    $cab = '<meta name="google-site-verification" content="0YPlPvpoRA9SeORL0uxpqpZ5tDNcMUuYufSjYXVFE6w" />' . "\n" . $cab;
    $html = str_replace('</head>', $cab . '</head>', $html);
    $html = str_replace('</body>', $pie . '</body>', $html);
    status_header(200);
    header('Content-Type: text/html; charset=utf-8');
    echo $html;
    exit;
}, 0);
