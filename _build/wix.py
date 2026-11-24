#!/usr/bin/env python3
"""Genera un "Elemento personalizado" de Wix Studio por cada página del sitio.

Cada archivo site/wix/<pagina>.js define una etiqueta HTML (por ejemplo <maisha-inicio>)
que dibuja la página completa con el mismo diseño. Wix lo carga desde Vercel.
Las fotos, PDFs y videos también se cargan desde Vercel (BASE).

Uso (después de `python3 _build/build.py --deploy`):
    python3 _build/wix.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
OUT = os.path.join(SITE, 'wix')
BASE = 'https://maisha-site.vercel.app/'

PAGES = {  # archivo -> (etiqueta, url de la página en Wix)
    'index': ('maisha-inicio', '/'),
    'nosotros': ('maisha-nosotros', '/nosotros'),
    'voluntariado': ('maisha-voluntariado', '/voluntariado'),
    'dona': ('maisha-dona', '/dona'),
    'market': ('maisha-market', '/market'),
    'programa-acogida': ('maisha-programa-acogida', '/programa-acogida'),
    'programa-salud': ('maisha-programa-salud', '/programa-salud'),
    'programa-educacion': ('maisha-programa-educacion', '/programa-educacion'),
    'programa-sustentabilidad': ('maisha-programa-sustentabilidad', '/programa-sustentabilidad'),
    'programa-derechos': ('maisha-programa-derechos', '/programa-derechos'),
}
FONTS = ('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700'
         '&family=Wix+Madefor+Text:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Caveat:wght@600&display=swap')


# ---------------------------------------------------------------- CSS scoping
def split_blocks(css):
    """Divide CSS de nivel superior en (prelude, body) respetando llaves anidadas."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0:
            break
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        out.append((prelude, css[j + 1:k - 1]))
        i = k
    return out


def scope_selector(sel):
    sel = sel.strip()
    if not sel:
        return None
    if '[data-theme' in sel or sel.startswith('body::before'):
        return None
    if sel.startswith('.reveal-on'):
        return '.mw.reveal-on' + sel[len('.reveal-on'):]
    for root in (':root', 'html', 'body'):
        if sel == root:
            return '.mw'
        if sel.startswith(root + ' ') or sel.startswith(root + ':'):
            return None if sel.startswith(root + ':not') else '.mw' + sel[len(root):]
    return '.mw ' + sel


def scope_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    res = []
    for prelude, body in split_blocks(css):
        if prelude.startswith('@media'):
            if 'prefers-color-scheme' in prelude:
                continue
            inner = scope_css(body)
            if inner.strip():
                res.append(f'{prelude}{{{inner}}}')
        elif prelude.startswith('@keyframes') or prelude.startswith('@font-face'):
            res.append(f'{prelude}{{{body}}}')
        elif prelude.startswith('@'):
            continue
        else:
            sels = [s for s in (scope_selector(x) for x in prelude.split(',')) if s]
            if sels:
                res.append(f'{",".join(sels)}{{{body}}}')
    return '\n'.join(res)


# ---------------------------------------------------------------- URL rewriting
def page_url(name, anchor=''):
    url = PAGES.get(name, (None, '/' + name))[1]
    return url + anchor


def rewrite_html(html):
    def href(m):
        target = m.group(1)
        if re.match(r'^(https?:|mailto:|tel:|#)', target):
            return m.group(0)
        if target.endswith('.pdf'):
            return f'href="{BASE}{target}"'
        mm = re.match(r'^([\w-]+)\.html(#[\w-]*)?$', target)
        if mm:
            return f'href="{page_url(mm.group(1), mm.group(2) or "")}"'
        return m.group(0)
    html = re.sub(r'href="([^"]+)"', href, html)
    html = re.sub(r'src="((?:img|memorias)/[^"]+)"', lambda m: f'src="{BASE}{m.group(1)}"', html)
    html = re.sub(r'url\((?:\.\./)?(img/[^)]+)\)', lambda m: f'url({BASE}{m.group(1)})', html)
    return html


def rewrite_css_urls(css):
    return re.sub(r'url\((?:\.\./)?(img/[^)]+)\)', lambda m: f'url({BASE}{m.group(1)})', css)


# ---------------------------------------------------------------- build
SITE_CSS = open(os.path.join(SITE, 'assets', 'site.css'), encoding='utf-8').read()
SITE_JS = open(os.path.join(SITE, 'assets', 'site.js'), encoding='utf-8').read()
# En Wix la clase de animación va en el contenedor de la página, no en <html>
SITE_JS = SITE_JS.replace("document.documentElement.classList.add('reveal-on')",
                          "(document.querySelector('.mw')||document.documentElement).classList.add('reveal-on')")

EXTRA_CSS = '''
.mw{display:block;position:relative;width:100%;overflow-x:clip;text-align:left}
.mw [hidden]{display:none!important}
.mw h1,.mw h2,.mw h3,.mw h4,.mw h5,.mw p,.mw li,.mw blockquote,.mw cite,.mw figcaption,.mw label{color:inherit;font-size:inherit}
.mw h1,.mw h2,.mw h3,.mw h4,.mw h5,.mw p,.mw ul,.mw ol,.mw figure,.mw blockquote{margin:0}
.mw img,.mw svg,.mw iframe{border:0;outline:0;box-shadow:none}
.mw button,.mw input,.mw select,.mw textarea{font:inherit;letter-spacing:normal}
.mw header.site{position:fixed;left:0;right:0;top:0;z-index:999}
.mw .wa{z-index:998}
'''

TEMPLATE = r'''/* Fundación Maisha · página "__NAME__" para Wix Studio (Elemento personalizado).
   Etiqueta: <__TAG__>   Generado desde el sitio maisha-site. No editar a mano. */
(function(){
  var TAG = "__TAG__";
  if (customElements.get(TAG)) return;
  var CSS = __CSS__;
  var HTML = __HTML__;
  function fonts(){
    if (document.getElementById('maisha-fonts')) return;
    var l = document.createElement('link'); l.id = 'maisha-fonts'; l.rel = 'stylesheet';
    l.href = "__FONTS__"; document.head.appendChild(l);
  }
  function run(){
__JS__
  }
  class MaishaPage extends HTMLElement {
    connectedCallback(){
      if (this._ok) return; this._ok = true;
      fonts();
      this.style.display = 'block';
      this.style.width = '100%';
      this.innerHTML = '<style>' + CSS + '</style><div class="mw">' + HTML + '</div>';
      try { run(); } catch (e) { console.error('Maisha', e); }
      // Ajusta la altura del elemento al contenido (Wix le da una altura fija)
      var self = this, mw = this.querySelector('.mw');
      function fit(){
        var h = Math.ceil(mw.getBoundingClientRect().height);
        self.style.height = h + 'px';
        var p = self.parentElement;
        for (var i = 0; p && i < 3; i++, p = p.parentElement) { p.style.minHeight = h + 'px'; p.style.height = 'auto'; }
      }
      fit();
      if (window.ResizeObserver) new ResizeObserver(fit).observe(mw);
      window.addEventListener('load', fit);
      // Si se llega con un ancla (/nosotros#equipo), bajar a esa sección
      if (location.hash) setTimeout(function(){ var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }, 400);
    }
  }
  customElements.define(TAG, MaishaPage);
})();
'''


def build():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, (tag, url) in PAGES.items():
        doc = open(os.path.join(SITE, name + '.html'), encoding='utf-8').read()
        inline_css = ''.join(re.findall(r'<style>(.*?)</style>', doc.split('</head>', 1)[1], flags=re.S))
        scripts = re.findall(r'<script>(.*?)</script>', doc, flags=re.S)
        body = doc.split('</head><body>', 1)[1]
        start = body.index('<header class="site">')
        end = body.index('<script src="assets/site.js">')
        html = rewrite_html(body[start:end].strip())
        css = scope_css(rewrite_css_urls(SITE_CSS + '\n' + inline_css)) + EXTRA_CSS
        js = SITE_JS + '\n' + '\n'.join(scripts)
        js = '\n'.join('    ' + l for l in js.splitlines())
        out = (TEMPLATE.replace('__NAME__', name).replace('__TAG__', tag).replace('__FONTS__', FONTS)
               .replace('__CSS__', json.dumps(css, ensure_ascii=False))
               .replace('__HTML__', json.dumps(html, ensure_ascii=False))
               .replace('__JS__', js))
        with open(os.path.join(OUT, name + '.js'), 'w', encoding='utf-8') as f:
            f.write(out)
        rows.append((name, tag, url, f'{BASE}wix/{name}.js'))
    # página de prueba local que monta un elemento
    with open(os.path.join(OUT, 'prueba.html'), 'w', encoding='utf-8') as f:
        f.write('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                '<body style="margin:0"><div id="slot"></div><script>var p=(location.hash||"#index").slice(1);'
                'var s=document.createElement("script");s.src=p+".js";s.onload=function(){'
                'var tags=' + json.dumps({n: t for n, (t, _) in PAGES.items()}) + ';'
                'document.getElementById("slot").appendChild(document.createElement(tags[p]));};document.body.appendChild(s);</script>')
    return rows


if __name__ == '__main__':
    for r in build():
        print(*r, sep=' | ')
