# Fundación Maisha · sitio web (prototipo)

Prototipo estático del rediseño de maishafoundation.com. Más adelante se migra a Next.js + Sanity (y Shopify para The Maisha Market).

## Estructura
- `_build/build.py`: genera todas las páginas desde una plantilla compartida. Los programas se definen en la lista `PROGRAMS`.
- `assets/`: estilos (`site.css`) y scripts (`site.js`) compartidos.
- `img/`: fotos, logos y productos.
- `site/`: versión publicada en Vercel (se genera, no se edita a mano).

## Actualizar
```bash
python3 _build/build.py --deploy
```
Haz commit y push: Vercel publica `site/` automáticamente.
