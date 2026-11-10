<?php
/*
Plugin Name: Óptica Almería · diseño nuevo (v5)
Description: Sirve la portada y las páginas de servicios y tiendas con el diseño nuevo. El blog, las entradas y el escritorio siguen en WordPress. Para volver a la web anterior basta con desactivar este plugin.
Version: 5.4.2
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
// Va aquí y no en WP Headers and Footers porque Wordfence bloquea guardar este código desde ese plugin.
add_action('wp_head', function () {
  if (is_admin()) return;
  echo "<script id=\"ov5-consent\">/* googletagmanager + metricool tras consentimiento */\n(function(){var cargado=false;function cargar(){if(cargado)return;cargado=true;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-JX418GQGP7';document.head.appendChild(s);window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};gtag('js',new Date());gtag('config','G-JX418GQGP7');var m=document.createElement('script');m.src='https://tracker.metricool.com/resources/be.js';m.onload=function(){beTracker.t({hash:'d28a629050eeb5d96ad3c05f9355aec4'})};document.head.appendChild(m);}\nfunction mirar(){try{var c=window.getCkyConsent&&getCkyConsent();if(c&&c.categories&&c.categories.analytics)cargar();}catch(e){}}\ndocument.addEventListener('cookieyes_consent_update',function(e){if(e.detail&&e.detail.accepted&&e.detail.accepted.indexOf('analytics')>-1)cargar();});\nif(document.readyState!=='loading')mirar();else document.addEventListener('DOMContentLoaded',mirar);window.addEventListener('load',mirar);})();</script>\n";
}, 1);
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
    );
    if (!isset($mapa[$ruta])) return;
    $f = __DIR__ . '/site/' . $mapa[$ruta];
    if (!is_file($f)) return;
    $html = file_get_contents($f);
    // aviso de cookies y analítica: los mismos que ya tiene la web, sacados de WordPress
    ob_start(); wp_head(); $cab = ov5_trozos(ob_get_clean());
    ob_start(); wp_footer(); $pie = ov5_trozos(ob_get_clean());
    $html = str_replace('</head>', $cab . '</head>', $html);
    $html = str_replace('</body>', $pie . '</body>', $html);
    status_header(200);
    header('Content-Type: text/html; charset=utf-8');
    echo $html;
    exit;
}, 0);
