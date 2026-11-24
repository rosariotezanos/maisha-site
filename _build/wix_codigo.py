#!/usr/bin/env python3
"""Genera el código HTML completo de cada página para pegarlo en Wix
(Elemento HTML → "Código"), y una página con botones para copiarlo.

Salida: site/wix-codigo/index.html   (abrir en el navegador y usar "Copiar")
Uso (después de build.py --deploy):  python3 _build/wix_codigo.py
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
OUT = os.path.join(SITE, 'wix-codigo')
BASE = 'https://maisha-site.vercel.app/'

PAGES = [  # (archivo, nombre, url en wix)
    ('index', 'Inicio', '(página de inicio)'),
    ('nosotros', 'Nosotros', 'nosotros'),
    ('voluntariado', 'Voluntariado', 'voluntariado'),
    ('dona', 'Dona', 'dona'),
    ('market', 'Maisha Market', 'market'),
    ('programa-acogida', 'Acogida', 'programa-acogida'),
    ('programa-salud', 'Salud', 'programa-salud'),
    ('programa-educacion', 'Educación Sexual', 'programa-educacion'),
    ('programa-sustentabilidad', 'Sustentabilidad', 'programa-sustentabilidad'),
    ('programa-derechos', 'Derechos Humanos', 'programa-derechos'),
]

CSS = open(os.path.join(SITE, 'assets', 'site.css'), encoding='utf-8').read()
JS = open(os.path.join(SITE, 'assets', 'site.js'), encoding='utf-8').read()
CSS = re.sub(r'url\((?:\.\./)?(img/[^)]+)\)', lambda m: f'url({BASE}{m.group(1)})', CSS)


def page_code(name):
    doc = open(os.path.join(SITE, name + '.html'), encoding='utf-8').read()
    doc = doc.replace('<link rel="stylesheet" href="assets/site.css">', '<style>' + CSS + '</style>')
    doc = doc.replace('<script src="assets/site.js"></script>', '<script>' + JS + '</script>')
    doc = doc.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    doc = re.sub(r'src="((?:img|memorias)/[^"]+)"', lambda m: f'src="{BASE}{m.group(1)}"', doc)
    doc = re.sub(r'url\((img/[^)]+)\)', lambda m: f'url({BASE}{m.group(1)})', doc)
    return doc


def build():
    os.makedirs(OUT, exist_ok=True)
    items = []
    for name, label, url in PAGES:
        code = page_code(name)
        items.append(f'''<section class="it">
  <div class="top"><div><h2>{html.escape(label)}</h2><p>URL de la página en Wix: <code>{html.escape(url)}</code> · {len(code)//1024} KB</p></div>
  <button type="button" data-i="{name}">Copiar código</button></div>
  <textarea id="c-{name}" readonly spellcheck="false">{html.escape(code)}</textarea>
</section>''')
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Maisha · Código para Wix</title>
<style>
body{{margin:0;font:16px/1.5 system-ui,sans-serif;background:#F3F5F9;color:#17213A}}
main{{max-width:900px;margin:0 auto;padding:32px 16px 80px}}
h1{{margin:0 0 6px}} .lead{{color:#5D6578;margin:0 0 28px}}
ol{{background:#fff;border-radius:16px;padding:20px 20px 20px 40px;margin:0 0 28px}}
.it{{background:#fff;border-radius:16px;padding:18px 20px;margin-bottom:14px}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}}
h2{{margin:0;font-size:1.15rem}} .top p{{margin:2px 0 0;color:#5D6578;font-size:.9rem}}
button{{font:600 .95rem system-ui;border:0;border-radius:999px;padding:.75em 1.3em;background:#F59B1B;color:#081326;cursor:pointer}}
button.ok{{background:#2E9E5B;color:#fff}}
textarea{{width:100%;height:70px;margin-top:12px;border:1px solid #E3E7EE;border-radius:10px;font:12px monospace;color:#5D6578;box-sizing:border-box}}
</style></head><body><main>
<h1>Código del sitio para Wix</h1>
<p class="lead">Una página de Wix por cada bloque. Copia el código y pégalo en el Elemento HTML.</p>
<ol>
<li>En Wix, crea la página y ponle la <b>URL</b> indicada (Configuración de la página → SEO).</li>
<li>Agrega <b>Incrusta código</b> (Elemento HTML). En <b>Elige qué incrustar</b> deja <b>Código</b>.</li>
<li>Aquí haz clic en <b>Copiar código</b>, pégalo en el cuadro de Wix y haz clic en <b>Aplicar</b>.</li>
<li>Estira el elemento al ancho completo y dale la altura de la pantalla (unos 900 px).</li>
</ol>
{''.join(items)}
</main><script>
document.querySelectorAll('button[data-i]').forEach(function(b){{
  b.onclick=function(){{
    var t=document.getElementById('c-'+b.dataset.i), done=function(){{b.textContent='¡Copiado!';b.classList.add('ok');setTimeout(function(){{b.textContent='Copiar código';b.classList.remove('ok')}},1800)}};
    if(navigator.clipboard) navigator.clipboard.writeText(t.value).then(done,function(){{t.select();document.execCommand('copy');done()}});
    else {{t.select();document.execCommand('copy');done()}}
  }};
}});
</script></body></html>'''
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
    return [(n, len(page_code(n))) for n, _, _ in PAGES]


if __name__ == '__main__':
    for n, s in build():
        print(n, s // 1024, 'KB')
