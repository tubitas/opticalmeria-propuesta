# Propuesta opticalmeria.com · v3 (noviembre 2026)

Web estática de 8 páginas generada con `python3 _src/build.py` (cabecera, pie, textos y datos estructurados en ese archivo).
Estilos en `site.css`, 20 líneas de JS en `site.js`, fuente Jost servida desde `fonts/`, fotos de su propia web en `img/` (AVIF + WebP).
Lleva `noindex` y robots `Disallow` a propósito, para no competir con opticalmeria.com.

Para el dominio real: `BASE=/ NOINDEX=0 python3 _src/build.py`.
La v2 (Fraunces + fotos de Unsplash) sigue en el historial de git.
