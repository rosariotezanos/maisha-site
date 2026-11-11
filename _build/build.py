#!/usr/bin/env python3
"""Genera las páginas estáticas del prototipo de Fundación Maisha.

Cada página comparte header, footer y estilos. Los programas usan una sola plantilla
alimentada por datos (PROGRAMS), igual que será un documento "programa" en Sanity.
Uso:  python3 _build/build.py   (desde la carpeta maisha-rediseno)
"""
import html, json, os, re, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import icon

_DIMS = {}
def _dims(m):
    p = m.group(1)
    if p not in _DIMS:
        with Image.open(os.path.join(SRC, p)) as im: _DIMS[p] = im.size
    w, h = _DIMS[p]
    return f'<img src="{p}" width="{w}" height="{h}"'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = ROOT
# --deploy: escribe documentos HTML completos en site/ (para Vercel)
DEPLOY = '--deploy' in sys.argv
if DEPLOY:
    ROOT = os.path.join(SRC, 'site')
e = html.escape

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700'
         '&family=Wix+Madefor+Text:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Caveat:wght@600&display=swap">')

PROGRAMS = [
  dict(slug="acogida", name="Acogida", stage="Al llegar", img="acogida-hero",
       short="Acompañamiento integral a embarazadas en crisis durante el embarazo y el postparto.",
       title="Nadie debería vivir su embarazo sola",
       intro="Mediante nuestro programa de acogida brindamos acompañamiento integral a embarazadas en crisis durante el embarazo y el postparto.",
       hand="Karibu, mamá",
       does=[("Acompañamiento 24/7","Apoyo telefónico permanente, visitas domiciliarias y un hogar temporal para madres que no cuentan con una red de apoyo."),
             ("Necesidades básicas","Entregamos insumos, alimentación y cuidado a cada mujer y a su recién nacido."),
             ("Comunidad","Organizamos encuentros de madres con la comunidad local y con la red de voluntarios Maisha en terreno.")],
       stats=[("435","Mujeres","han recibido acompañamiento durante su embarazo y postparto.","embarazada"),
              ("232","Con apoyo telefónico","han recibido asistencia de nuestro equipo local en Kenia.","telefono"),
              ("133","Madres indoor","han vivido temporalmente en el centro de acogida Maisha.","casa"),
              ("48","Madres outdoor","acompañadas y visitadas regularmente en su casa.","visita"),
              ("136","Toto Care Box","donadas, con un ajuar completo para los primeros meses.","regalo"),
              ("100%","Continuó su embarazo","de las madres acompañadas por el programa.","corazon")],
       gallery=["acogida-1","acogida-2","acogida-3","acogida-totocarebox","acogida-4"],
       quote=('Ver cómo confiaban en mí, cómo me contaban de ellas y de sus vidas, y cómo compartíamos tristezas y alegrías fue, lejos, lo más significativo para mí. Creo que eso es lo que hace tan especial ser voluntaria de acogida: te permite una cercanía con todas las mamás de la casa en lo cotidiano.',
              'Jacinta Fernández','Voluntaria de Acogida · Memoria 2025','testimonios/jacinta-fernandez')),
  dict(slug="salud", name="Salud", stage="Embarazo y parto", img="salud-hero",
       short="Controles prenatales, atención del parto y consejería en lactancia materna.",
       title="Atención digna antes, durante y después del parto",
       intro="A través de nuestro programa de salud velamos por que las madres y sus hijos reciban atención sanitaria antes, durante y después del parto.",
       hand="Partos dignos",
       does=[("Control y parto","Ofrecemos controles prenatales, atención del parto y consejería en lactancia materna."),
             ("Seguimiento en casa","Acompañamos a madres y recién nacidos con visitas domiciliarias continuas."),
             ("Capacidades locales","Educamos y capacitamos al personal de salud local para potenciar habilidades en la propia comunidad.")],
       stats=[("100%","Lactancia materna","exclusiva durante los primeros meses.","gota"),
              ("895","Controles prenatales","a Madres Maisha, y 5.244 a madres de otras comunidades.","estetoscopio"),
              ("463","Partos atendidos","120 de Madres Maisha y 343 de madres de otras comunidades.","bebe"),
              ("276","Ecografías","obstétricas realizadas a Madres Maisha.","ecografia"),
              ("123","Madres capacitadas","en prevención y cuidado de ellas y sus recién nacidos.","birrete"),
              ("327","Personal de salud","local capacitado.","grupo")],
       gallery=["salud-equipo","salud-1","salud-2","salud-3","salud-4"],
       quote=('Gracias por encargarse de mis gastos del hospital. Tuve una cesárea y agradecí mucho que me ayudaran con todos los gastos. ¡Gracias a Dios estoy viva! Disfruté de todos los talleres. Todo lo que hicimos fue beneficioso.',
              'Mitchel Auma','Madre Maisha, mamá de Velt · Memoria 2025','testimonios/mitchel-auma')),
  dict(slug="educacion", name="Educación Sexual", stage="Crianza", img="educacion-hero",
       short="Educación afectiva y sexual, y la iniciativa Menstruación Sin Reglas.",
       title="Decidir con libertad y responsabilidad",
       intro="Acompañamos a niños, niñas, adolescentes y jóvenes en las diferentes etapas de su desarrollo bajo una mirada personalista de su afectividad y sexualidad.",
       hand="Menstruación sin reglas",
       does=[("Junto a Teen STAR","El programa internacional capacita a nuestros voluntarios en cambios corporales, ciclo menstrual, cerebro adolescente, planificación familiar, autoestima, emociones y relaciones."),
             ("Toma de decisiones","Desarrollamos habilidades para decidir desde la libertad y la responsabilidad."),
             ("Monitores locales","Capacitamos a monitores de la comunidad de Kibera para que el programa se replique de forma continua en Kenia.")],
       extra=("Menstruación Sin Reglas","Informada · Ecológica · Accesible",
              "En Kenia la menstruación es uno de los principales motivos de ausentismo escolar, y en Chile es un problema para mujeres en situación de calle, privadas de libertad o en campamentos. Por eso recaudamos fondos para entregar toallas higiénicas reutilizables a niñas y jóvenes en Kenia y Chile. Cada entrega va acompañada de un taller sobre el ciclo menstrual y la higiene femenina.","educacion-toallas"),
       stats=[("3.640","Beneficiarios","directos del programa educativo en colegios y comunidades.","grupo"),
              ("108","Madres Maisha","se han beneficiado del programa en sexualidad y afectividad.","embarazada"),
              ("74","Comunidades y escuelas","donde se ha implementado el programa en Kenia.","escuela"),
              ("63","Voluntarios y monitores","capacitados para aplicar el programa.","birrete"),
              ("14.899","Toallas reutilizables","entregadas a niñas y adolescentes por Menstruación Sin Reglas.","toalla"),
              ("3.916","Beneficiarias","de la campaña educativa: 3.841 en Kenia y 75 en Chile.","grupo")],
       gallery=["educacion-1","educacion-2","educacion-3","educacion-4","educacion-5"],
       quote=('Gracias Maisha por pagar mis gastos del hospital y ayudarme a criar a mi hija. Me encantó TeenSTAR y estoy usando lo que he aprendido para enseñarles a mis hermanas pequeñas en casa.',
              'Florence Joan','Madre Maisha, mamá de Killan · Memoria 2025','testimonios/florence-joan')),
  dict(slug="sustentabilidad", name="Sustentabilidad", stage="Autonomía", img="sustentabilidad-hero",
       short="Oficios, ahorro y emprendimiento para sostener a la familia de forma autónoma.",
       title="Herramientas para salir adelante",
       intro="Empoderamos a las madres con herramientas que les permiten mantener a sus familias de manera autónoma y segura.",
       hand="Hecho por mamás Maisha",
       does=[("Oficios","Capacitaciones en costura, computación, y finanzas y emprendimiento."),
             ("Ingresos propios","Estrategias de ahorro y actividades generadoras de ingresos, como la confección para The Maisha Market."),
             ("Desarrollo personal","Instancias recreativas y de aprendizaje que amplían horizontes y fortalecen la confianza.")],
       stats=[("144","Beneficiarias directas","han participado de nuestros programas de sustentabilidad.","grupo"),
              ("803","Sesiones","impartidas para fortalecer el aprendizaje.","sesiones"),
              ("50","Mujeres","capacitadas en costura y finanzas con el Fondo Chile en 2025.","hilo")],
       gallery=["sustentabilidad-1","sustentabilidad-2","sustentabilidad-3","sustentabilidad-4","market-feria"],
       quote=('Aprendí muchísimas habilidades: computación, costura y cocina. Conseguí un trabajo temporal gracias a mis conocimientos de computación. Actualmente, estoy produciendo toallas higiénicas reutilizables para Maisha y estoy ganando dinero con ello.',
              'Seline Atieno','Madre Maisha, mamá de Kyle · Memoria 2025','testimonios/seline-atieno')),
  dict(slug="derechos", name="Derechos Humanos", stage="En todo el camino", img="derechos-hero",
       short="Educación cívica para que madres y jóvenes conozcan y defiendan sus derechos.",
       title="Conocer y defender los propios derechos",
       intro="Nuestro quinto y más nuevo programa empodera a madres y jóvenes de los slums de Nairobi promoviendo sus derechos fundamentales y la educación cívica.",
       hand="Dignidad",
       does=[("Derechos Humanos y Ciudadanía","En 2025, con el fondo PAEE de la Cancillería de Chile, ejecutamos el primer proyecto del programa."),
             ("Junto a Strathmore","Formamos a jóvenes en Derechos Humanos y Educación Cívica con la Escuela de Derecho de la Universidad de Strathmore."),
             ("Graduación","El ciclo cerró con una ceremonia de graduación en la Strathmore Law Clinic.")],
       stats=[("278","Jóvenes","de slums de Nairobi capacitados en Derechos Humanos y Educación Cívica.","birrete"),
              ("2025","Primer proyecto","del nuevo y quinto programa Maisha.","bandera")],
       gallery=["derechos-grupo","derechos-manos","comunidad","historia-equipo","historia-2021"],
       quote=None),
]
PROG = {p["slug"]: p for p in PROGRAMS}

ICON_CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 7h14l-1.2 10.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8z"/><path d="M9 10V6a3 3 0 0 1 6 0v4"/></svg>'
WA = '<a class="wa" href="#contacto" aria-label="Escríbenos por WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3z"/></svg></a>'


def header(active):
    def cur(k): return ' aria-current="page"' if k == active else ''
    prog_items = ''.join(f'<li><a href="programa-{p["slug"]}.html"><img src="img/{p["img"]}.jpg" alt="">'
                         f'<span style="color:inherit;font-size:.95rem">{e(p["name"])}<span>{e(p["stage"])}</span></span></a></li>' for p in PROGRAMS)
    prog_mobile = ''.join(f'<a href="programa-{p["slug"]}.html">{e(p["name"])}</a>' for p in PROGRAMS)
    return f'''<header class="site">
  <div class="wrap">
    <div class="pill">
      <a class="logo" href="index.html" aria-label="Fundación Maisha, inicio"><span class="mark" aria-hidden="true"></span></a>
      <nav aria-label="Principal">
        <ul class="menu">
          <li class="has-drop"><a href="nosotros.html"{cur("nosotros")}>Nosotros</a>
            <ul class="drop">
              <li><a href="nosotros.html#somos">Quiénes somos</a></li>
              <li><a href="nosotros.html#historia">Nuestra historia</a></li>
              <li><a href="nosotros.html#kibera">Kenia y Kibera</a></li>
              <li><a href="nosotros.html#equipo">Equipo</a></li>
              <li><a href="nosotros.html#medios">En los medios</a></li>
              <li><a href="nosotros.html#memorias">Memorias</a></li>
            </ul>
          </li>
          <li class="has-drop"><a href="index.html#programas"{cur("programas")}>Programas</a>
            <ul class="drop">{prog_items}</ul>
          </li>
          <li><a href="voluntariado.html"{cur("voluntariado")}>Voluntariado</a></li>
          <li><a href="market.html"{cur("market")}>Maisha Market</a></li>
        </ul>
      </nav>
      <div class="nav-actions">
        <span class="lang"><strong>ES</strong> / EN</span>
        <a class="cart-btn" href="market.html#carrito" aria-label="Carrito">{ICON_CART}<b data-cart-count hidden>0</b></a>
        <a class="btn btn-donate btn-sm" href="dona.html">Donar</a>
        <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Abrir menú">
          <svg width="26" height="26" viewBox="0 0 26 26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 8h18M4 13h18M4 18h12"/></svg>
        </button>
      </div>
    </div>
    <div class="mobile" id="mobile-menu" hidden>
      <details><summary>Nosotros</summary><div><a href="nosotros.html#somos">Quiénes somos</a><a href="nosotros.html#historia">Nuestra historia</a><a href="nosotros.html#kibera">Kenia y Kibera</a><a href="nosotros.html#equipo">Equipo</a><a href="nosotros.html#medios">En los medios</a><a href="nosotros.html#memorias">Memorias</a></div></details>
      <details><summary>Programas</summary><div>{prog_mobile}</div></details>
      <a href="voluntariado.html">Voluntariado</a>
      <a href="market.html">Maisha Market</a>
      <a href="#contacto">Contacto · ES / EN</a>
    </div>
  </div>
</header>'''


FOOTER = '''<footer class="site" id="contacto">
  <div class="kanga" aria-hidden="true"></div>
  <div class="foot">
    <div class="wrap foot-top">
      <div>
        <a class="logo" href="index.html" aria-label="Fundación Maisha"><span class="mark" aria-hidden="true"></span></a>
        <div class="contact">
          <p><b>Contacto</b>contacto@fundacionmaisha.com<br>+56 9 8901 2205</p>
          <p><b>Chile · Kenia</b>Santiago y Kibera, Nairobi</p>
        </div>
      </div>
      <div>
        <h4>Fundación</h4>
        <ul><li><a href="nosotros.html#somos">Quiénes somos</a></li><li><a href="nosotros.html#historia">Historia</a></li><li><a href="nosotros.html#kibera">Kenia y Kibera</a></li><li><a href="nosotros.html#memorias">Memorias</a></li></ul>
      </div>
      <div>
        <h4>Participa</h4>
        <ul><li><a href="dona.html">Dona</a></li><li><a href="dona.html#socio">Hazte socio</a></li><li><a href="voluntariado.html">Voluntariado</a></li><li><a href="market.html">The Maisha Market</a></li></ul>
      </div>
      <div>
        <h4>Newsletter</h4>
        <p style="color:var(--on-navy-muted);font-size:.94rem;margin-bottom:14px">Recibe noticias de Chile y Kenia.</p>
        <form class="news-form" id="nl-form">
          <input id="nl-email" type="email" placeholder="tu@correo.cl" aria-label="Correo electrónico" required>
          <button type="submit">Suscribirme</button>
        </form>
        <p class="form-msg" id="nl-msg" aria-live="polite"></p>
      </div>
    </div>
    <div class="wrap foot-bottom">
      <span>© 2026 Fundación Maisha · Built by Studio X Design Lab</span>
      <nav aria-label="Redes"><a href="#">Instagram</a><a href="#">LinkedIn</a><a href="#">Facebook</a><a href="#">YouTube</a></nav>
    </div>
  </div>
</footer>'''


def page(filename, title, active, body, css='', js=''):
    doc = f'''<title>{e(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<link rel="stylesheet" href="assets/site.css">
{('<style>' + css + '</style>') if css else ''}
{header(active)}
<main>
{body}
</main>
{FOOTER}
{WA}
<script src="assets/site.js"></script>
{('<script>' + js + '</script>') if js else ''}
'''
    if DEPLOY or filename != 'index.html':  # en claude.ai el index lo envuelve el visor; en Vercel todas necesitan documento completo
        doc = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
               '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
               '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}'
               'body{margin:0}[hidden]{display:none!important}</style></head><body>\n' + doc + '</body></html>')
    doc = re.sub(r'<img src="(img/[^"]+)"', _dims, doc)
    with open(os.path.join(ROOT, filename), 'w', encoding='utf-8') as f:
        f.write(doc)


def stats_html(stats, note=None):
    s = ''.join(f'<div class="stat">{icon(st[3], "ico stat-ico") if len(st) > 3 else ""}<b>{e(st[0])}</b><strong>{e(st[1])}</strong><p>{e(st[2])}</p></div>' for st in stats)
    return s, (f'<p class="note" style="margin-top:22px">{e(note)}</p>' if note else '')


def quote_html(q):
    if not q: return ''
    text, who, role, img = q
    return f'''<section class="sec"><div class="wrap quote">
  <img src="img/{img}.jpg" alt="{e(who)}" loading="lazy">
  <blockquote><p>{e(text)}</p><cite><strong>{e(who)}</strong>{e(role)}</cite></blockquote>
</div></section>'''


def quote_html_reveal(q):
    return quote_html(q).replace('<img ','<img data-reveal="left" ',1).replace('<blockquote>','<blockquote data-reveal data-delay="2">',1)


VIDEOS = [
  ("Xfwcl9_sG_Q", "El inicio de Maisha, hasta hoy", "Fernanda junto a un grupo de chilenos viajaron a Kenia en 2015 y se comprometieron con una iniciativa local. Así nació Fundación Maisha.", "Fundación Maisha"),
  ("n8yXzrLkWOE", "La campeona Provida", "La historia de Domtila Ayot, el corazón y motor de Maisha.", "BARN Short Docs"),
  ("Gam48_L3OrU", "Mi lugar en el mundo", "Fernanda es enfermera y vive en Nairobi. Desde hace 7 años acompaña a mujeres embarazadas con partos dignos y sin violencia obstétrica.", "Capítulo 2"),
  ("baW57_EZH1M", "Siempre hay un chileno", "Sinopsis de nuestra historia en el capítulo de Siempre hay un Chileno en Nairobi.", "Sinopsis"),
  ("DWMm_LqEFuI", "Una chilena en Nairobi", "Capítulo completo de Siempre hay un Chileno en Nairobi. Maisha aparece en el minuto 19:00.", "Capítulo completo"),
  ("KAhoDj_Bq88", "Desconocidos TV", "Sebastián y Wenceslao, médicos y cofundadores de Maisha, cuentan su experiencia.", "Capítulo 87"),
]
PLAY = '<span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.4-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg></span>'


def video_link(vid, title, cls, inner):
    return (f'<a class="{cls}" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" data-video="{vid}" '
            f'aria-label="Ver video: {e(title)}">{inner}</a>')


def prog_cards():
    cards = ''.join(f'''<li data-reveal data-delay="{i+1}"><a class="prog" href="programa-{p["slug"]}.html">
      <img src="img/{p["img"]}.jpg" alt="" loading="lazy">
      <span class="badge">{icon(p["slug"])}</span>
      <div class="body"><span class="stage">{e(p["stage"])}</span><h3>{e(p["name"])}</h3><p>{e(p["short"])}</p><span class="go">Conocer →</span></div>
    </a></li>''' for i, p in enumerate(PROGRAMS))
    thread = ('<svg class="thread" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true">'
              '<path d="M0 40 C 150 0, 250 60, 360 30 S 600 0, 720 34 S 960 60, 1080 24 S 1180 20, 1200 30" '
              'fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/></svg>')
    return f'<ol class="prog-grid">{thread}{cards}</ol>'


# ---------------------------------------------------------------- INICIO
def build_home():
    css = '''
.hero{padding-top:0;position:relative}
.hero > .wrap{max-width:none;padding-left:0;padding-right:0}
:root{--edge:max(24px,calc((100vw - 1480px) / 2 + 24px))}
.hero-box{position:relative;border-radius:0;overflow:hidden;min-height:clamp(600px,52vw,780px);display:grid;align-items:end;color:#fff;background:var(--navy)}
.hero-box > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:72% 30%}
.hero-box::before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(6,16,34,.86) 0%,rgba(6,16,34,.7) 28%,rgba(6,16,34,.32) 46%,rgba(6,16,34,0) 60%)}
.hero-in{position:relative;z-index:2;padding:170px var(--edge) 64px;display:grid;gap:22px}
.hero h1{font-size:var(--step-4);font-weight:700;line-height:1.08}
.hero h1 span{display:block}
@keyframes heroUp{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
@keyframes heroFade{from{opacity:0}to{opacity:1}}
@keyframes heroZoom{from{transform:scale(1.08)}to{transform:scale(1)}}
@keyframes helpIn{from{opacity:0;transform:translateX(40px)}to{opacity:1;transform:none}}
.hero-box > img{animation:heroZoom 2.4s cubic-bezier(.2,.7,.2,1) both}
.hero h1 span{animation:heroUp .9s cubic-bezier(.2,.7,.2,1) both}
.hero h1 span + span{animation-delay:.15s}
.hero .sub{animation:heroFade 1s .45s ease both}
.hero .row{animation:heroUp .8s .6s cubic-bezier(.2,.7,.2,1) both}
.help{animation:helpIn .8s .9s cubic-bezier(.2,.7,.2,1) both}
@media (prefers-reduced-motion: reduce){.hero-box > img,.hero h1 span,.hero .sub,.hero .row,.help{animation:none}}
.hero h1 em{font-style:normal;color:var(--orange)}
.hero-in > p{font:400 var(--step-1)/1.4 var(--display);color:rgba(255,255,255,.9)}
.hero .sub span{display:block}
.hero .row{display:flex;flex-wrap:wrap;gap:12px;margin-top:8px}
.hero .btn-line{color:#fff}
.help{position:absolute;right:var(--edge);bottom:32px;z-index:2;display:flex;align-items:center;gap:14px;background:var(--card);color:var(--ink);border-radius:18px;padding:14px 14px 14px 18px;box-shadow:0 16px 34px rgba(0,0,0,.22);max-width:360px}
.help p{font:600 .9rem/1.3 var(--display)}
.help p span{display:block;font:500 .8rem var(--body);color:var(--muted)}
@media (max-width:900px){.help{position:relative;right:auto;bottom:auto;margin:16px 16px 0;max-width:none;box-shadow:0 8px 24px rgba(8,19,38,.12);border:1px solid var(--line)}}
@media (max-width:760px){.hero-box{min-height:660px;display:flex;flex-direction:column;justify-content:flex-end}.hero-box > img{object-position:79% 0%}.hero-box::before{background:linear-gradient(0deg,rgba(6,16,34,.95) 0%,rgba(6,16,34,.85) 34%,rgba(6,16,34,.4) 52%,rgba(6,16,34,0) 64%)}.hero-in{padding:0 20px 28px;gap:14px}.hero h1{font-size:2.3rem}.hero-in > p{font-size:1rem;text-wrap:pretty}.hero .sub span{display:inline}.hero h1 span{display:inline}.hero .row .btn{padding:.9em 1.3em}}

.intro{display:grid;grid-template-columns:1fr 1fr;gap:72px;align-items:center}
.intro > *{min-width:0}
.statement{font:600 var(--step-3)/1.18 var(--display);letter-spacing:-.015em;text-wrap:balance}
.statement span{color:var(--orange-ink)}
.collage{position:relative;padding:0 0 70px 50px}
.collage .a{width:100%;height:auto;border-radius:var(--r)}
.collage .b{position:absolute;left:0;bottom:0;width:44%;aspect-ratio:1;object-fit:cover;border-radius:50%;border:8px solid var(--paper)}
.collage .hand{position:absolute;right:8px;bottom:18px;transform:rotate(-5deg)}
@media (max-width:860px){.intro{grid-template-columns:1fr;gap:36px}.collage{padding:0 0 60px 30px}}

.impact{padding:56px}
.impact-grid{display:grid;grid-template-columns:1.5fr .7fr;gap:56px;align-items:center}
.impact .map{position:absolute;right:-140px;top:-120px;width:560px;aspect-ratio:1;color:var(--orange);opacity:.14;-webkit-mask-image:url(img/mapa-nairobi.png);mask-image:url(img/mapa-nairobi.png);pointer-events:none}
.impact .stats{margin-top:40px;grid-template-columns:repeat(2,1fr)}
.memo{position:relative;display:grid;gap:14px;justify-items:start}
.memo img{width:100%;max-width:240px;border-radius:6px;transform:rotate(3deg);box-shadow:0 24px 40px -18px rgba(0,0,0,.6)}
.memo p{color:var(--on-navy-muted);font-size:.95rem}
@media (max-width:900px){.impact{padding:32px 22px}.impact-grid{grid-template-columns:1fr;gap:40px}}
@media (max-width:440px){.impact .stats{grid-template-columns:1fr}}

.ways{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.way{position:relative;display:flex;flex-direction:column;border-radius:var(--r);overflow:hidden;text-decoration:none;color:var(--on-navy);background:var(--navy)}
.way img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;object-position:50% 20%;transition:transform .4s ease}
.way:hover img{transform:scale(1.04)}
.way > div{padding:22px 26px 26px;display:grid;gap:8px;flex:1;align-content:start}
.way h3{font-size:var(--step-2);font-weight:700}
.way p{color:rgba(255,255,255,.85);font-size:.96rem}
.way .go{font-weight:600;color:var(--orange)}
@media (max-width:900px){.ways{grid-template-columns:1fr}}

.allies{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:28px 40px;color:var(--logo-ink)}
.allies .mark{height:52px;width:120px;opacity:.75}
.allies .amref{font:700 1rem/1.05 var(--display);opacity:.75}
.allies .amref small{display:block;font-weight:600;font-size:.75rem}
'''
    body = f'''
<section class="hero"><div class="wrap">
  <div class="hero-box">
    <img src="img/madre-bebe.jpg" alt="Madre sonriendo mientras sostiene a su bebé recién nacido">
    <div class="hero-in">
      <h1><span>Porque todo embarazo</span> <span>merece <em>compañía</em>.</span></h1>
      <p class="sub"><span>Maisha es una fundación chilena que acompaña</span> <span>a mujeres embarazadas, madres y jóvenes</span> <span>en contextos vulnerables en Kenia.</span></p>
      <div class="row"><a class="btn btn-donate" href="dona.html">Quiero donar</a><a class="btn btn-line" href="nosotros.html">Conócenos</a></div>
    </div>
  </div>
  <div class="help" aria-label="Línea de apoyo">
    <p>Pregnant and need support?<span>We're here to help, 24/7.</span></p>
    <a class="btn btn-donate btn-sm" href="#contacto">Call now</a>
  </div>
</div></section>

<section class="sec"><div class="wrap intro">
  <div>
    <p class="eyebrow" style="margin-bottom:18px" data-reveal>Maisha significa vida</p>
    <p class="statement" data-reveal data-delay="1">Nacimos en el corazón de Kibera para <span>acompañar a cada madre</span> desde el embarazo hasta su autonomía.</p>
    <p class="lead" style="margin-top:22px" data-reveal data-delay="2">Desde 2016, junto a Mama Domitila y el Centro de Esperanza Edel Quinn, somos una red de apoyo entre Chile y Kenia para que toda madre reciba a su hijo en condiciones dignas.</p>
    <a class="btn btn-navy" href="nosotros.html#historia" style="margin-top:28px" data-reveal data-delay="3">Nuestra historia</a>
  </div>
  <figure class="collage" data-reveal="right" data-delay="1">
    <img class="a" src="img/equipo.jpg" alt="Madres con sus bebés y voluntarias de Maisha en Kibera">
    <img class="b" src="img/domitila.jpg" alt="Mujer de la comunidad de Kibera">
    <span class="hand">Karibu, bienvenida</span>
  </figure>
</div></section>

<section class="sec" id="programas" style="padding-top:20px"><div class="wrap">
  <div class="head">
    <p class="eyebrow" data-reveal>Nuestros programas</p>
    <h2 class="h2" data-reveal data-delay="1">Cinco programas que siguen <em>el camino de cada madre</em></h2>
    <p class="lead" data-reveal data-delay="2">Detrás de cada mujer hay una historia que merece ser acompañada.</p>
  </div>
  <div style="padding-top:30px">{prog_cards()}</div>
</div></section>

<section class="sec" style="padding-top:20px"><div class="wrap">
  <div class="navy-panel impact" data-reveal="fade">
    <span class="mark map" aria-hidden="true"></span>
    <div class="impact-grid">
      <div>
        <p class="eyebrow">#ImpactoMaisha</p>
        <h2 class="h2" style="margin-top:12px" data-reveal data-delay="1">Lo que hemos logrado juntos en Kibera</h2>
        <div class="stats">
          <div class="stat" data-reveal data-delay="2">{icon("embarazada", "ico stat-ico")}<b data-count="435" data-suffix="">435</b><strong>Mujeres</strong><p>acompañadas durante su embarazo y postparto.</p></div>
          <div class="stat" data-reveal data-delay="3">{icon("casa", "ico stat-ico")}<b data-count="133" data-suffix="">133</b><strong>Madres</strong><p>han vivido en el centro de acogida.</p></div>
          <div class="stat" data-reveal data-delay="4">{icon("grupo", "ico stat-ico")}<b data-count="482" data-suffix="">482</b><strong>Talleres</strong><p>y convivencias realizadas.</p></div>
          <div class="stat" data-reveal data-delay="5">{icon("corazon", "ico stat-ico")}<b data-count="100" data-suffix="%">100%</b><strong>De las madres</strong><p>continuaron con su embarazo.</p></div>
        </div>
      </div>
      <div class="memo" data-reveal="right" data-delay="2">
        <img src="img/memoria-2025.jpg" alt="Portada de la Memoria 2025">
        <p>Testimonios y resultados en nuestra memoria anual.</p>
        <a class="btn btn-donate btn-sm" href="memorias/memoria-2025-es.pdf" target="_blank" rel="noopener">Leer Memoria 2025</a>
      </div>
    </div>
  </div>
</div></section>

<section class="sec" style="padding-top:20px"><div class="wrap">
  <div data-reveal="fade">{video_link("Xfwcl9_sG_Q", "El inicio de Maisha, hasta hoy", "vfeature", '<img src="img/videos/Xfwcl9_sG_Q.jpg" alt="" loading="lazy">' + PLAY + '<span class="vtext"><span class="eyebrow">Conoce nuestra historia</span><b>El inicio de Maisha, hasta hoy</b><span>Fernanda junto a un grupo de chilenos viajaron a Kenia en 2015 y se comprometieron con una iniciativa local. Así nació Fundación Maisha.</span></span>')}</div>
  <p class="vmore" data-reveal="fade"><a class="link" href="nosotros.html#medios">Ver más videos de Maisha en los medios →</a></p>
</div></section>

{quote_html_reveal(("Disfruté mucho de mi experiencia en la casa Maisha. Me sentí muy apoyada durante mi embarazo. Disfruté de la costura y de las charlas de salud. ¡Muchas gracias por tenerme en Maisha!", "Vivian Emali", "Madre Maisha, mamá de CJay · Memoria 2025", "testimonios/vivian-emali"))}

<section class="sec" style="padding-top:20px"><div class="wrap">
  <div class="head"><p class="eyebrow" data-reveal>¡Involúcrate!</p><h2 class="h2" data-reveal data-delay="1">Sé parte de la familia Maisha</h2></div>
  <div class="ways">
    <a class="way" href="voluntariado.html" data-reveal data-delay="1"><img src="img/voluntaria.jpg" alt="" loading="lazy"><div><p class="eyebrow" style="color:var(--orange)">Voluntariado</p><h3>Viaja a Kenia y sé un puente de esperanza</h3><span class="go">Postular →</span></div></a>
    <a class="way" href="dona.html#socio" data-reveal data-delay="2"><img src="img/acogida-5.jpg" alt="" loading="lazy"><div><p class="eyebrow" style="color:var(--orange)">Socios</p><h3>Aporta cada mes</h3><span class="go">Hazte socio →</span></div></a>
    <a class="way" href="market.html" data-reveal data-delay="3"><img src="img/market-feria.jpg" alt="" loading="lazy"><div><p class="eyebrow" style="color:var(--orange)">Tienda</p><h3>The Maisha Market</h3><span class="go">Ir a la tienda →</span></div></a>
  </div>
</div></section>

<section class="sec tight"><div class="wrap">
  <p class="eyebrow" style="margin-bottom:26px">Alianzas por el mundo</p>
  <div class="allies" data-reveal="fade">
    <span class="mark" style="-webkit-mask-image:url(img/logo-aiep.png);mask-image:url(img/logo-aiep.png)" role="img" aria-label="AIEP"></span>
    <span class="mark" style="-webkit-mask-image:url(img/logo-totocarebox.png);mask-image:url(img/logo-totocarebox.png)" role="img" aria-label="TotoCareBox"></span>
    <span class="mark" style="-webkit-mask-image:url(img/logo-teenstar.png);mask-image:url(img/logo-teenstar.png)" role="img" aria-label="Teen STAR"></span>
    <span class="mark" style="-webkit-mask-image:url(img/logo-reamedica.png);mask-image:url(img/logo-reamedica.png)" role="img" aria-label="ReaMedica Health"></span>
    <span class="amref">amref<small>health africa</small></span>
  </div>
</div></section>
'''
    page('index.html', 'Fundación Maisha', 'inicio', body, css)


# ---------------------------------------------------------------- NOSOTROS
def build_nosotros():
    css = '''
.sec[id]{scroll-margin-top:170px}
/* Grilla de 4 columnas compartida por Quiénes somos, Valores e Historia */
.g4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}
.span2{grid-column:span 2}
.about{align-items:stretch}
.about-intro{grid-column:span 2;display:grid;gap:16px;align-content:center;padding-right:clamp(0px,4vw,56px)}
.about-intro .h2 em{font-style:normal;color:var(--orange-ink)}
.mv{position:relative;overflow:hidden;border-radius:var(--r);padding:32px 30px 34px;display:grid;gap:12px;align-content:start;box-shadow:0 18px 40px -18px rgba(8,19,38,.35);transition:transform .25s ease}
.mv:hover{transform:translateY(-4px)}
.mv h3{font-size:var(--step-2);font-weight:600;line-height:1.15}
.mv p:last-child{line-height:1.5}
.mv-navy{background:var(--navy);color:var(--on-navy)}
.mv-navy .eyebrow{color:var(--orange)}
.mv-navy p:last-child{color:var(--on-navy-muted)}
.mv-orange{background:var(--orange);color:#081326}
.mv-orange .eyebrow{color:#081326;opacity:.7}
.mv::after{content:"";position:absolute;right:-40px;bottom:-40px;width:150px;height:150px;border-radius:50%;border:22px solid currentColor;opacity:.07}
.values-wrap{margin-top:64px}
.values-wrap > .eyebrow{margin-bottom:20px}
.value{display:grid;gap:10px;align-content:start;background:var(--sand);border-radius:var(--r);padding:28px 26px 30px;transition:transform .25s ease}
.value:hover{transform:translateY(-4px)}
.val-ico{width:42px;height:42px;padding:11px;box-sizing:content-box;border-radius:50%;background:#FFFFFF;color:#3E4659;box-shadow:0 8px 20px rgba(8,19,38,.08);margin-bottom:6px}
.value:hover .val-ico{transform:translateY(-4px) scale(1.05)}
.value:hover .ico .f,.value:hover .ico .fs{transform:scale(1.18)}
.value h3{font-size:1.15rem;font-weight:600}
.value p{color:var(--muted);font-size:.95rem;line-height:1.45}
.hist-head{align-items:end;margin-bottom:72px}
@media (max-width:980px){.g4{grid-template-columns:repeat(2,minmax(0,1fr))}.about-intro{grid-column:1/-1;padding-right:0}.hist-head .span2{grid-column:1/-1}}
@media (max-width:560px){.g4{grid-template-columns:1fr}.span2,.about-intro{grid-column:auto}.value{padding:24px 22px 26px}}
@media (max-width:480px){.values{grid-template-columns:1fr}}

.timeline{position:relative;list-style:none;margin:0;padding:0;display:grid;gap:36px}
.timeline::before{content:"";position:absolute;left:calc(50% - 1px);top:10px;bottom:10px;border-left:2px dashed var(--orange);opacity:.6}
.tl{display:grid;grid-template-columns:1fr 1fr;gap:72px;align-items:center;position:relative}
.tl::after{content:"";position:absolute;left:calc(50% - 9px);top:50%;width:18px;height:18px;border-radius:50%;background:var(--orange);box-shadow:0 0 0 6px var(--paper)}
.tl .yr{font:700 clamp(2.2rem,4vw,3.2rem)/1 var(--display);color:var(--orange-ink);letter-spacing:-.02em}
.tl .txt{display:grid;gap:10px}
.tl .txt p{color:var(--muted)}
.tl img{width:100%;height:auto;border-radius:var(--r)}
.tl:nth-child(even) .txt{order:2}
.tl.solo{grid-template-columns:1fr 1fr}
.tl.solo .txt{grid-column:1}
.tl.solo:nth-child(even) .txt{grid-column:2}
@media (max-width:860px){
  .timeline::before{left:8px}
  .tl,.tl.solo{grid-template-columns:1fr;gap:18px;padding-left:40px}
  .tl::after{left:0;top:6px}
  .tl:nth-child(even) .txt{order:0}
  .tl.solo .txt,.tl.solo:nth-child(even) .txt{grid-column:auto}
}

.kib{padding:56px}
.kib-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(56px,8vw,128px)}
.kib-head{display:flex;align-items:center;gap:18px}
.kib-head .eyebrow{margin-bottom:4px}
.kib-ico{width:58px;height:58px;padding:9px;box-sizing:content-box;border-radius:50%;background:#FFFFFF;color:#3E4659;box-shadow:0 8px 20px rgba(8,19,38,.10);flex:none}
.kib-mean{margin-top:18px;padding:14px 18px;border-radius:14px;background:var(--card);border-left:3px solid var(--orange);font-size:1rem;color:var(--muted)}
.kib-mean b{color:var(--ink);font-weight:600}
.kib-grid > *{min-width:0}
.facts{list-style:none;padding:0;margin:22px 0 0;display:grid;gap:0}
.facts li{display:flex;justify-content:space-between;gap:20px;padding:12px 0;border-bottom:1px solid var(--line);font-size:.97rem}
.facts li span{color:var(--muted)}
.facts li b{text-align:right;font-weight:600}
.kib-photos{display:grid;grid-template-columns:1fr 1fr;gap:clamp(56px,8vw,128px);margin-top:56px;align-items:start}
.kib-photos img{width:72%;height:auto;border-radius:20px;justify-self:center}
@media (max-width:860px){.kib{padding:30px 20px}.kib-grid{grid-template-columns:1fr;gap:48px}.kib-photos{gap:16px}.kib-photos img{width:100%}}

.team{display:grid;grid-template-columns:repeat(5,1fr);gap:22px 18px}
.member{margin:0;display:grid;gap:12px;align-content:start}
.member .ph{border-radius:20px;overflow:hidden;background:var(--sand);aspect-ratio:1}
.member img{width:100%;height:100%;object-fit:cover;object-position:50% 20%;filter:grayscale(1);transition:transform .4s ease,filter .4s ease}
.member:hover img{transform:scale(1.05);filter:grayscale(0)}
.member b{display:block;font:600 1.02rem/1.25 var(--display)}
.member span{display:block;margin-top:2px;font-size:.88rem;line-height:1.35;color:var(--muted)}
@media (max-width:1100px){.team{grid-template-columns:repeat(4,1fr)}}
@media (max-width:800px){.team{grid-template-columns:repeat(3,1fr)}}
@media (max-width:520px){.team{grid-template-columns:1fr 1fr;gap:18px 12px}}
.team-h{font:700 .8rem var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:36px 0 14px}

.ods{display:grid;grid-template-columns:repeat(8,1fr);gap:8px;list-style:none;padding:0;margin:22px 0 0;max-width:520px}
.ods li{position:relative;aspect-ratio:1;border-radius:8px;color:#fff;display:grid;place-items:center;font:700 1.05rem var(--display);cursor:help;transition:transform .2s ease}
.ods li:hover,.ods li:focus-visible{transform:translateY(-3px);outline:none}
.ods .tip{position:absolute;bottom:calc(100% + 12px);left:50%;transform:translate(-50%,6px);width:280px;max-width:calc(100vw - 40px);background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 18px 40px rgba(8,19,38,.2);font:400 .88rem/1.45 var(--body);text-align:left;opacity:0;visibility:hidden;transition:opacity .18s ease,transform .18s ease;z-index:30;pointer-events:none}
.ods .tip b{display:block;font:600 .95rem/1.25 var(--display);margin-bottom:6px}
.ods .tip em{display:block;font-style:normal;margin-top:8px;padding-top:8px;border-top:1px solid var(--line);color:var(--muted)}
.ods .tip::after{content:"";position:absolute;top:100%;left:50%;margin-left:-7px;border:7px solid transparent;border-top-color:var(--card)}
.ods li:hover .tip,.ods li:focus .tip{opacity:1;visibility:visible;transform:translate(-50%,0)}
.ods li:nth-child(-n+2) .tip{left:0;transform:translate(0,6px)}.ods li:nth-child(-n+2):hover .tip,.ods li:nth-child(-n+2):focus .tip{transform:none}.ods li:nth-child(-n+2) .tip::after{left:22px}
.ods li:nth-last-child(-n+2) .tip{left:auto;right:0;transform:translate(0,6px)}.ods li:nth-last-child(-n+2):hover .tip,.ods li:nth-last-child(-n+2):focus .tip{transform:none}.ods li:nth-last-child(-n+2) .tip::after{left:auto;right:15px}
@media (max-width:560px){.ods{position:relative;grid-template-columns:repeat(4,1fr);gap:10px;max-width:none}.ods li{position:static;font-size:1.2rem}
.ods li:hover,.ods li:focus-visible{transform:none;box-shadow:0 0 0 3px var(--orange)}
.ods .tip,.ods li:nth-child(n) .tip{left:0;right:0;width:auto;max-width:none;transform:translateY(6px)}
.ods li:nth-child(n):hover .tip,.ods li:nth-child(n):focus .tip{transform:none}
.ods .tip::after{display:none}}
.memos{display:grid;grid-template-columns:auto 1fr;gap:48px;align-items:center}
.memos img{width:220px;border-radius:6px;transform:rotate(-2deg);box-shadow:0 24px 40px -18px rgba(16,35,63,.5)}
@media (max-width:700px){.memos{grid-template-columns:1fr}.memos img{width:180px}}
'''
    team = [
      ("Directorio", [("Domtila Ayot","Cofundadora y Directora"),("Mª Antonia Villablanca","Cofundadora y Directora"),("Fernanda Almarza","Cofundadora y Directora"),("Wenceslao Zegers","Cofundador y Director"),("Sebastián Frías","Cofundador"),("Julián Álvarez","Cofundador"),("Christine Chassin-Trubert","Directora")]),
      ("Equipo", [("Rocío Rivero","Directora Ejecutiva"),("Verónica Córdova","Coordinación de Operaciones en Kenia"),("Montana Njaaga","Coordinadora de Operaciones en Kenia"),("Bernardita Sanhueza","Coordinación de Voluntariado"),("Rosario Mozó","Socios"),("Consuelo Gutiérrez","The Maisha Market"),("Florencia Torrejón","Ventas The Maisha Market")]),
      ("Asesores", [("Cristina Alonso","Programa de Salud"),("Rosario Larraín","Programa de Acogida"),("Manuela Kawas","Programa de Sustentabilidad"),("Nicole Espinoza","Programa de Educación Sexual"),("Francisco Cáceres","Psicólogo, Voluntariado")]),
    ]
    def _slug(n):
        import unicodedata
        key = {'Domtila Ayot':'domtila','Montana Njaaga':'montana','Christine Chassin-Trubert':'chassin'}.get(n)
        if key: return key
        last = n.split()[-1]
        return unicodedata.normalize('NFKD', last).encode('ascii','ignore').decode().lower()
    def ini(n):
        p = [w for w in n.replace('Mª','M').split() if w[0].isupper()]
        return (p[0][0] + p[-1][0]).upper()
    team_html = ''.join(f'<p class="team-h">{g}</p><div class="team">' + ''.join(
        f'<figure class="member"><div class="ph"><img src="img/equipo/{_slug(n)}.jpg" alt="{e(n)}" loading="lazy"></div><figcaption><b>{e(n)}</b><span>{e(r)}</span></figcaption></figure>' for n, r in ms) + '</div>' for g, ms in team)

    tl = [
      ("2009","El Centro de Esperanza Edel Quinn","Mama Domitila recortó papeles con su número de teléfono y los pegó por Kibera, esperando que quien buscara un hombro donde apoyarse pudiera recurrir a ella. Así nació el Centro de Esperanza Edel Quinn, dedicado a embarazos en crisis.","historia-2009"),
      ("2015","Cinco chilenos en Kenia","Un grupo de voluntarios chilenos en un hospital de bajos recursos se cruzó con esta pequeña gran iniciativa local y decidió convertirse en una verdadera red de apoyo.","historia-fundadores"),
      ("2016","Nace Maisha","En alianza con Edel Quinn Centre se forma Maisha, que en suajili significa vida.","historia-chile"),
      ("2017","Fundación en Chile","Maisha se constituye legalmente en Chile como fundación sin fines de lucro operativa en el extranjero.",None),
      ("2019","Nuevo centro de acogida","Se adopta la figura de CBO en Kenia y se inaugura el nuevo centro de acogida para madres junto a la organización África Digna.","historia-2019"),
      ("2020","Cuatro programas","Se consolidan los programas de acogida, salud, educación sexual y sustentabilidad.",None),
      ("2022","Profesionalización","El equipo en Chile y Kenia se profesionaliza, y The Maisha Market se constituye legalmente como tienda solidaria.","historia-equipo"),
      ("2026","Nuevas caras e ideas","Comenzamos el año con nuevo directorio. El sueño de un Maisha Chile y la casa propia se va haciendo realidad.","comunidad"),
    ]
    tl_html = ''.join(
        f'<li class="tl{"" if img else " solo"}"><div class="txt"><span class="yr">{y}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        + (f'<img src="img/{img}.jpg" alt="" loading="lazy">' if img else '') + '</li>' for y, t, d, img in tl)

    body = f'''
<section class="phero"><div class="wrap">
  <div class="phero-grid">
    <div>
      <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><span>Nosotros</span></nav>
      <h1 class="h1">Maisha significa <em>vida</em></h1>
      <p class="lead">Somos una fundación que nace de la colaboración entre Chile y Kenia, comprometida con la dignidad de la persona, para acompañar a mujeres, madres y jóvenes.</p>
    </div>
    <figure class="phero-photo"><img src="img/historia-equipo.jpg" alt="Equipo Maisha junto a madres de Kibera"><span class="hand">Chile ♥ Kenia</span></figure>
  </div>
  <nav class="subnav" aria-label="En esta página"><ul>
    <li><a href="#somos">Quiénes somos</a></li><li><a href="#historia">Historia</a></li><li><a href="#kibera">Kenia y Kibera</a></li><li><a href="#equipo">Equipo</a></li><li><a href="#medios">En los medios</a></li><li><a href="#memorias">Memorias</a></li>
  </ul></nav>
</div></section>

<section class="sec" id="somos"><div class="wrap">
  <div class="g4 about">
    <div class="about-intro">
      <p class="eyebrow">Quiénes somos</p>
      <h2 class="h2">Una red entre <em>Chile</em> y <em>Kenia</em></h2>
      <p class="lead">Somos una fundación comprometida con la dignidad de la persona, que trabaja por acompañar a mujeres, madres y jóvenes.</p>
    </div>
    <div class="mv mv-navy"><p class="eyebrow">Misión</p><h3>Acompañar y ofrecer oportunidades</h3><p>Acompañar y ofrecer oportunidades de crecimiento a embarazadas, madres y jóvenes en contextos vulnerables.</p></div>
    <div class="mv mv-orange"><p class="eyebrow">Visión</p><h3>Toda madre, en condiciones dignas</h3><p>Ser la principal red de acompañamiento para mujeres, logrando que toda madre reciba a su hijo en las condiciones dignas que ambos merecen.</p></div>
  </div>
  <div class="values-wrap">
    <p class="eyebrow">Nuestros valores</p>
    <div class="g4 values">
      <div class="value">{icon("corazon", "ico val-ico")}<h3>Respeto a la vida</h3><p>Estamos comprometidos con el respeto a la vida y la dignidad de la persona humana.</p></div>
      <div class="value">{icon("mano", "ico val-ico")}<h3>Responsabilidad</h3><p>Un acompañamiento concreto a embarazadas, madres y adolescentes que requieren una red de apoyo.</p></div>
      <div class="value">{icon("grupo", "ico val-ico")}<h3>Cooperación</h3><p>Trabajamos en equipo, de forma horizontal y apoyándonos en actores locales.</p></div>
      <div class="value">{icon("balanza", "ico val-ico")}<h3>Equidad</h3><p>Igualdad de oportunidades y no discriminación.</p></div>
    </div>
  </div>
</div></section>

<section class="sec" id="historia" style="padding-top:20px"><div class="wrap">
  <div class="g4 hist-head">
    <div class="span2"><p class="eyebrow">Nuestra historia</p><h2 class="h2" style="margin-top:12px">Maisha nació en el corazón de <em>Kibera</em></h2></div>
    <p class="lead span2">Mama Domitila Ayot veía cómo muchas mujeres y adolescentes de su población quedaban embarazadas con escaso o nada de apoyo, en condiciones de pobreza extrema. Decidió aportar con lo poco que podía entregar.</p>
  </div>
  <ol class="timeline">{tl_html}</ol>
</div></section>

<section class="sec" id="medios" style="padding-top:20px"><div class="wrap">
  <div class="g4 hist-head" style="margin-bottom:40px">
    <div class="span2"><p class="eyebrow">Maisha en los medios</p><h2 class="h2" style="margin-top:12px">Nuestra historia, <em>en video</em></h2></div>
    <p class="lead span2">Reportajes, documentales y entrevistas que cuentan cómo nació Maisha y quiénes la hacen posible.</p>
  </div>
  <div class="vgrid">{''.join(video_link(v, t, "vcard", f'<span class="vthumb"><img src="img/videos/{v}.jpg" alt="" loading="lazy">{PLAY}</span><span class="vbody"><span class="vtag">{e(tag)}</span><b>{e(t)}</b><span>{e(d)}</span></span>') for v, t, d, tag in VIDEOS)}</div>
</div></section>

<section class="sec" id="kibera"><div class="wrap">
  <div class="panel kib">
    <div class="kib-grid">
      <div>
        <div class="kib-head">{icon("montana", "ico kib-ico")}<div><p class="eyebrow">Sobre Kenia</p><h2 class="h2">Kenia</h2></div></div>
        <p class="kib-mean">Su nombre viene del Monte Kenia. En algunas lenguas locales significa <b>“montaña luminosa”</b>.</p>
        <p class="lead" style="margin-top:14px;font-size:1.05rem">Un país del este de África conocido por su variedad de paisajes, animales y personas de 44 etnias.</p>
        <ul class="facts">
          <li><span>Capital</span><b>Nairobi</b></li><li><span>Población</span><b>56,2 millones</b></li>
          <li><span>Superficie</span><b>580.367 km²</b></li><li><span>Idiomas oficiales</span><b>Inglés y suajili</b></li><li><span>Esperanza de vida</span><b>67 años</b></li>
        </ul>
      </div>
      <div>
        <div class="kib-head">{icon("bosque", "ico kib-ico")}<div><p class="eyebrow">Sobre Kibera</p><h2 class="h2">Kibera</h2></div></div>
        <p class="kib-mean">Su nombre significa <b>“bosque”</b> o <b>“jungla”</b>.</p>
        <p class="lead" style="margin-top:14px;font-size:1.05rem">El slum más grande de Kenia y el segundo de África: una población informal en los suburbios de Nairobi con escaso acceso a servicios básicos.</p>
        <ul class="facts">
          <li><span>Densidad</span><b>+2.000 personas por hectárea</b></li><li><span>Ubicación</span><b>Suburbios de Nairobi</b></li><li><span>Donde trabajamos</span><b>Centro de acogida Maisha</b></li>
        </ul>
      </div>
    </div>
    <div class="kib-photos"><img src="img/kibera-techos.jpg" alt="Techos de zinc de Kibera" loading="lazy"><img src="img/kibera.jpg" alt="Calle comercial en Kibera" loading="lazy"></div>
  </div>
</div></section>

<section class="sec" id="equipo" style="padding-top:20px"><div class="wrap">
  <div class="head" style="margin-bottom:10px"><p class="eyebrow">Equipo</p><h2 class="h2">Las personas detrás de Maisha</h2></div>
  {team_html}
  
</div></section>

<section class="sec" id="memorias"><div class="wrap">
  <div class="panel" style="padding:48px">
    <div class="memos">
      <img src="img/memoria-2025.jpg" alt="Portada de la Memoria 2025">
      <div>
        <p class="eyebrow">Memorias</p>
        <h2 class="h2" style="margin-top:12px">#ImpactoMaisha</h2>
        <p class="lead" style="margin-top:14px">Nuestra memoria anual 2025 reúne el impacto de la fundación, testimonios y el trabajo de estos años.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px"><a class="btn btn-navy" href="memorias/memoria-2025-es.pdf" target="_blank" rel="noopener">Leer en español</a><a class="btn btn-line" href="memorias/memoria-2025-en.pdf" target="_blank" rel="noopener">Read in English</a></div>
        <p style="margin-top:36px;font-weight:600">Agenda 2030</p>
        <p style="color:var(--muted);font-size:.95rem">Con nuestras acciones contribuimos a estos Objetivos de Desarrollo Sostenible de la ONU.</p>
        <ul class="ods"><li tabindex="0" style="background:#E5243B" aria-describedby="ods-1">1<span class="tip" role="tooltip" id="ods-1"><b>ODS 1 · Fin de la pobreza</b>Poner fin a la pobreza en todas sus formas en todo el mundo.<em>En Maisha: Acompañamos a madres de Kibera, uno de los asentamientos informales más grandes de África.</em></span></li><li tabindex="0" style="background:#4C9F38" aria-describedby="ods-3">3<span class="tip" role="tooltip" id="ods-3"><b>ODS 3 · Salud y bienestar</b>Garantizar una vida sana y promover el bienestar para todos en todas las edades.<em>En Maisha: Controles prenatales, atención del parto y salud mental para madres y recién nacidos.</em></span></li><li tabindex="0" style="background:#FF3A21" aria-describedby="ods-5">5<span class="tip" role="tooltip" id="ods-5"><b>ODS 5 · Igualdad de género</b>Lograr la igualdad entre los géneros y empoderar a todas las mujeres y las niñas.<em>En Maisha: Educación y herramientas para que mujeres y niñas decidan sobre su vida.</em></span></li><li tabindex="0" style="background:#A21942" aria-describedby="ods-8">8<span class="tip" role="tooltip" id="ods-8"><b>ODS 8 · Trabajo decente y crecimiento económico</b>Promover el crecimiento económico inclusivo, el empleo pleno y productivo y el trabajo decente para todos.<em>En Maisha: Capacitación en oficios, finanzas y emprendimiento en el programa de Sustentabilidad.</em></span></li><li tabindex="0" style="background:#DD1367" aria-describedby="ods-10">10<span class="tip" role="tooltip" id="ods-10"><b>ODS 10 · Reducción de las desigualdades</b>Reducir la desigualdad en los países y entre ellos.<em>En Maisha: Acceso a salud, educación y oportunidades para quienes viven en los slums de Nairobi.</em></span></li><li tabindex="0" style="background:#3F7E44" aria-describedby="ods-13">13<span class="tip" role="tooltip" id="ods-13"><b>ODS 13 · Acción por el clima</b>Adoptar medidas urgentes para combatir el cambio climático y sus efectos.<em>En Maisha: Toallas higiénicas reutilizables con Menstruación Sin Reglas: informada, ecológica y accesible.</em></span></li><li tabindex="0" style="background:#00689D" aria-describedby="ods-16">16<span class="tip" role="tooltip" id="ods-16"><b>ODS 16 · Paz, justicia e instituciones sólidas</b>Promover sociedades pacíficas e inclusivas y facilitar el acceso a la justicia para todos.<em>En Maisha: Formación en Derechos Humanos y Educación Cívica junto a la Universidad de Strathmore.</em></span></li><li tabindex="0" style="background:#19486A" aria-describedby="ods-17">17<span class="tip" role="tooltip" id="ods-17"><b>ODS 17 · Alianzas para lograr los objetivos</b>Fortalecer las alianzas mundiales para el desarrollo sostenible.<em>En Maisha: Trabajamos con AIEP, Teen STAR, TotoCareBox, ReaMedica, Amref y Fundación Kianda.</em></span></li></ul>
      </div>
    </div>
  </div>
</div></section>
'''
    page('nosotros.html', 'Nosotros · Fundación Maisha', 'nosotros', body, css)


# ---------------------------------------------------------------- PROGRAMA (plantilla)
PROG_CSS = '''
.does{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.does .card{padding:28px;display:grid;gap:10px;align-content:start}
.does .card i{width:38px;height:38px;border-radius:12px;background:var(--orange-soft);color:var(--orange-ink);display:grid;place-items:center;font:700 1rem var(--display);font-style:normal}
.does h3{font-size:1.15rem}
.does p{color:var(--muted);font-size:.97rem}
@media (max-width:900px){.does{grid-template-columns:1fr}}
.pimpact{padding:52px}
.pimpact .stats{margin-top:34px}
@media (max-width:760px){.pimpact{padding:32px 22px}}
.extra{display:grid;grid-template-columns:.8fr 1.2fr;gap:48px;align-items:center;padding:44px}
.extra img{width:100%;height:auto;max-width:340px;margin-inline:auto;border-radius:20px}
@media (max-width:860px){.extra{grid-template-columns:1fr;padding:28px 22px}}
.others{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.other{display:flex;gap:14px;align-items:center;padding:12px;border:1px solid var(--line);border-radius:18px;text-decoration:none;background:var(--card);transition:border-color .15s}
.other:hover{border-color:var(--orange)}
.oico{width:56px;height:56px;border-radius:16px;background:var(--sand);display:grid;place-items:center;flex:none}.oico .ico{width:40px;height:40px}
.other b{display:block;font:600 1rem var(--display)}
.other span{font-size:.82rem;color:var(--muted)}
@media (max-width:1000px){.others{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.others{grid-template-columns:1fr}}
'''


def build_program(p):
    does = ''.join(f'<div class="card"><i aria-hidden="true">{i+1}</i><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(p["does"]))
    st, note = stats_html(p.get("stats", []), p.get("stats_note"))
    impact = ''
    if p.get("stats"):
        impact = f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="navy-panel pimpact">
  <p class="eyebrow">Impacto</p><h2 class="h2" style="margin-top:12px">{e(p["name"])} en cifras</h2>
  <div class="stats">{st}</div>{note}
</div></div></section>'''
    elif note:
        impact = f'<section class="sec tight"><div class="wrap">{note}</div></section>'
    extra = ''
    if p.get("extra"):
        t, sub, d, img = p["extra"]
        extra = f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="panel extra">
  <img src="img/{img}.jpg" alt="Toallas higiénicas reutilizables de tela" loading="lazy">
  <div><p class="eyebrow">Iniciativa</p><h2 class="h2" style="margin-top:12px">{e(t)}</h2><p class="hand" style="margin-top:10px">{e(sub)}</p><p class="lead" style="margin-top:16px;font-size:1.05rem">{e(d)}</p></div>
</div></div></section>'''
    gallery = ''.join(f'<img src="img/{g}.jpg" alt="" loading="lazy">' for g in p["gallery"])
    others = ''.join(f'<a class="other" href="programa-{o["slug"]}.html"><span class="oico">{icon(o["slug"])}</span><div><b>{e(o["name"])}</b><span>{e(o["stage"])}</span></div></a>'
                     for o in PROGRAMS if o["slug"] != p["slug"])
    body = f'''
<section class="phero"><div class="wrap phero-grid">
  <div>
    <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><a href="index.html#programas">Programas</a><span aria-hidden="true">/</span><span>{e(p["name"])}</span></nav>
    <p class="prog-tag">{icon(p["slug"])}<span>Programa {e(p["name"])} · {e(p["stage"])}</span></p>
    <h1 class="h1">{e(p["title"])}</h1>
    <p class="lead">{e(p["intro"])}</p>
    <div class="phero-cta"><a class="btn btn-donate" href="dona.html">Apoyar este programa</a><a class="btn btn-line" href="voluntariado.html">Ser voluntario</a></div>
  </div>
  <figure class="phero-photo"><img src="img/{p["img"]}.jpg" alt="Programa {e(p["name"])} de Fundación Maisha"><span class="hand">{e(p["hand"])}</span></figure>
</div></section>

<section class="sec"><div class="wrap">
  <div class="head"><p class="eyebrow">Qué hacemos</p><h2 class="h2">Cómo acompañamos</h2></div>
  <div class="does">{does}</div>
</div></section>
{impact}
{extra}
{quote_html(p.get("quote"))}
<section class="sec" style="padding-top:20px"><div class="wrap">
  <div class="head" style="margin-bottom:28px"><p class="eyebrow">Galería</p><h2 class="h2">En terreno</h2></div>
  <div class="gallery">{gallery}</div>
</div></section>

<section class="sec" style="padding-top:20px"><div class="wrap">
  <div class="panel cta-card">
    <div><h2 class="h2">Ayúdanos a que más madres lleguen a {e(p["name"].lower()) if p["slug"]!="derechos" else "este programa"}</h2><p>Con un aporte mensual sostienes el trabajo en Kibera durante todo el año.</p></div>
    <div class="row"><a class="btn btn-donate" href="dona.html#socio">Hazte socio</a><a class="btn btn-line" href="dona.html">Aporte único</a></div>
  </div>
  <p class="eyebrow" style="margin:56px 0 18px">Otros programas</p>
  <div class="others">{others}</div>
</div></section>
'''
    page(f'programa-{p["slug"]}.html', f'{p["name"]} · Fundación Maisha', 'programas', body, PROG_CSS)


# ---------------------------------------------------------------- VOLUNTARIADO
def build_voluntariado():
    css = '''
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;list-style:none;padding:0;margin:0;counter-reset:s}
.steps li{position:relative;padding:28px;border:1px solid var(--line);border-radius:var(--r);background:var(--card);display:grid;gap:10px;align-content:start}
.steps li::before{counter-increment:s;content:counter(s);width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--orange);color:#10233F;font:700 1.05rem var(--display)}
.steps h3{font-size:1.15rem}
.steps p{color:var(--muted);font-size:.97rem}
@media (max-width:860px){.steps{grid-template-columns:1fr}}
.vform{padding:44px;display:grid;grid-template-columns:.9fr 1.1fr;gap:48px}
.vform > *{min-width:0}
.vform img{width:100%;height:auto;border-radius:var(--r);align-self:start}
@media (max-width:860px){.vform{grid-template-columns:1fr;padding:26px 20px}}
'''
    areas = ''.join(f'<option>{e(p["name"])}</option>' for p in PROGRAMS)
    body = f'''
<section class="phero"><div class="wrap phero-grid">
  <div>
    <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><span>Voluntariado</span></nav>
    <h1 class="h1">Involúcrate y sé <em>voluntario</em></h1>
    <p class="lead">En Maisha trabajamos por el bienestar de mujeres embarazadas en contextos vulnerables en Kenia. Junto a voluntarios y socios entregamos herramientas, cuidado y espacios seguros para proteger la dignidad de cada mujer.</p>
    <div class="phero-cta"><a class="btn btn-donate" href="#postular">Postular</a><a class="btn btn-line" href="#boletin">Boletín voluntarios</a></div>
  </div>
  <figure class="phero-photo"><img src="img/voluntaria.jpg" alt="Voluntaria de Maisha junto a madres del taller de costura"><span class="hand">Voluntaria 2025</span></figure>
</div></section>

<section class="sec"><div class="wrap">
  <div class="grid-2">
    <div><p class="eyebrow">Por qué sumarte</p><h2 class="h2" style="margin-top:12px">Un puente de esperanza</h2></div>
    <p class="lead">Al unirte, tu dedicación ayuda a estas mujeres a descubrir su potencial, empoderarse y construir un futuro mejor para ellas y sus familias. Puedes aportar desde la salud, la educación, la psicología, el diseño o cualquier otra área.</p>
  </div>
</div></section>

<section class="sec" id="boletin" style="padding-top:20px"><div class="wrap">
  <div class="head"><p class="eyebrow">Cómo postular</p><h2 class="h2">Tres pasos para llegar a Kibera</h2></div>
  <ol class="steps">
    <li><h3>Lee el boletín</h3><p>Ahí está la información de cada programa y los requisitos para viajar a Kenia.</p><a class="link" href="#boletin">Descargar boletín →</a></li>
    <li><h3>Completa el formulario</h3><p>Cuéntanos quién eres y en qué programa te gustaría participar.</p><a class="link" href="#postular">Ir al formulario →</a></li>
    <li><h3>Conversemos</h3><p>Nuestra coordinación de voluntariado te contactará para los siguientes pasos.</p></li>
  </ol>
</div></section>

<section class="sec" style="padding-top:20px"><div class="wrap"><div class="gallery">
  <img src="img/voluntariado-1.jpg" alt="" loading="lazy"><img src="img/voluntariado-2.jpg" alt="" loading="lazy"><img src="img/acogida-testimonio.jpg" alt="" loading="lazy"><img src="img/salud-2.jpg" alt="" loading="lazy"><img src="img/voluntariado-4.jpg" alt="" loading="lazy">
</div></div></section>

{quote_html(("Maisha no solo acompaña embarazos; acompaña vidas. Ser parte de este proceso, aunque sea por unos meses, es algo que llevaré siempre conmigo. Asante sana, Maisha, por enseñarme tanto durante este tiempo.", "Dominga Acosta", "Voluntaria de Sustentabilidad · Memoria 2025", "testimonios/dominga-acosta"))}
<section class="sec" id="postular" style="padding-top:20px"><div class="wrap">
  <div class="panel vform">
    <img src="img/voluntariado-3.jpg" alt="Grupo de voluntarios Maisha con la bandera de la fundación">
    <form data-demo>
      <h2 class="h2">Quiero ser voluntario</h2>
      <p class="lead" style="margin:10px 0 26px;font-size:1.05rem">Introduce tus datos y nos pondremos en contacto contigo. ¡Estamos muy felices de que quieras ser parte de la familia Maisha!</p>
      <div class="form-grid">
        <div class="field"><label for="v-nombre">Nombre</label><input id="v-nombre" required></div>
        <div class="field"><label for="v-apellido">Apellidos</label><input id="v-apellido"></div>
        <div class="field full"><label for="v-email">Email</label><input id="v-email" type="email" required></div>
        <div class="field full"><label for="v-area">Interesado en</label><select id="v-area">{areas}<option>Otro</option></select></div>
        <div class="field full"><label for="v-msg">Mensaje</label><textarea id="v-msg" required></textarea></div>
        <div class="full"><button class="btn btn-donate" type="submit">Enviar postulación</button></div>
        <p class="ok-msg full" hidden>¡Gracias! Te escribiremos a la brevedad.</p>
      </div>
    </form>
  </div>
</div></section>
'''
    page('voluntariado.html', 'Voluntariado · Fundación Maisha', 'voluntariado', body, css)


# ---------------------------------------------------------------- DONA
def build_dona():
    css = '''
.dona-top{padding-top:120px}
.dona-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.dona-grid > *{min-width:0}
.tabs{display:grid;grid-template-columns:1fr 1fr;background:var(--sand);border-radius:999px;padding:5px;margin-bottom:22px}
.tabs button{font:600 .98rem var(--display);border:0;border-radius:999px;padding:.8em;background:transparent;color:var(--muted);cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--navy);color:var(--on-navy)}
.dcard{padding:30px;display:grid;gap:18px}
.amounts{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.amounts button{font:700 1.02rem var(--display);padding:.95em .3em;border-radius:12px;border:1.5px solid var(--line);background:transparent;color:var(--ink);cursor:pointer;font-variant-numeric:tabular-nums}
.amounts button[aria-pressed="true"]{border-color:var(--orange);background:var(--orange-soft)}
.equiv{display:block;padding:14px 16px;border-radius:14px;background:var(--sand);font-size:.95rem;color:var(--muted)}
.equiv b{color:var(--ink)}
.methods{display:grid;gap:12px}
.method{display:grid;gap:6px;padding:18px;border:1px solid var(--line);border-radius:16px}
.method h3{font-size:1.02rem}
.method p{font-size:.93rem;color:var(--muted)}
.bank{display:grid;grid-template-columns:auto 1fr auto;gap:6px 14px;align-items:center;font-size:.93rem;margin-top:6px}
.bank span{color:var(--muted)}
.bank b{font-weight:600;font-variant-numeric:tabular-nums}
.copy{font:600 .78rem var(--body);border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:.35em .8em;cursor:pointer}
.small{font-size:.82rem;color:var(--muted);text-align:center}
.what{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.what .card{overflow:hidden}
.what img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;object-position:50% 25%}
.what div{padding:18px 20px 22px}
.what b{display:block;font:700 1.6rem var(--display);color:var(--orange-ink)}
.what p{color:var(--muted);font-size:.95rem;margin-top:4px}
@media (max-width:960px){.dona-grid{grid-template-columns:1fr}.what{grid-template-columns:1fr 1fr}}
@media (max-width:480px){.amounts{grid-template-columns:1fr 1fr}.what{grid-template-columns:1fr}.dcard{padding:22px}}
'''
    js = r'''
(function(){
  var tabs=[].slice.call(document.querySelectorAll('.tabs button'));
  function show(id){tabs.forEach(function(t){var on=t.dataset.tab===id;t.setAttribute('aria-selected',String(on));document.getElementById(t.dataset.tab).hidden=!on;});}
  tabs.forEach(function(t){t.onclick=function(){show(t.dataset.tab);};});
  if(location.hash==='#unico') show('unico');
  var eq={10000:'una ecografía para ver al bebé por primera vez',25000:'un control prenatal para un embarazo acompañado',100000:'insumos y alimentación para una madre en acogida'};
  var amt=25000, btns=[].slice.call(document.querySelectorAll('.amounts button')), other=document.getElementById('d-other'), go=document.getElementById('d-go'), eqt=document.getElementById('d-eq');
  var fmt=function(n){return '$'+n.toLocaleString('es-CL');};
  function render(){
    btns.forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.amt==='other'?!other.hidden:(other.hidden&&+b.dataset.amt===amt)));});
    go.textContent='Hacerme socio con '+fmt(amt)+' al mes';
    eqt.innerHTML=eq[amt]?('<b>'+fmt(amt)+'</b> al mes equivale a '+eq[amt]+'.'):('Gracias por tu aporte de <b>'+fmt(amt)+'</b> al mes.');
  }
  btns.forEach(function(b){b.onclick=function(){if(b.dataset.amt==='other'){other.hidden=false;other.focus();}else{other.hidden=true;other.value='';amt=+b.dataset.amt;}render();};});
  other.addEventListener('input',function(){var d=other.value.replace(/\D/g,'');other.value=d?(+d).toLocaleString('es-CL'):'';amt=d?+d:25000;render();});
  document.getElementById('mensual').addEventListener('submit',function(e){e.preventDefault();document.getElementById('d-ok').hidden=false;});
  render();
})();'''
    body = '''
<section class="dona-top"><div class="wrap dona-grid">
  <div>
    <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><span>Dona</span></nav>
    <h1 class="h1">Ayúdanos a acompañar a <em>más madres</em></h1>
    <p class="lead" style="margin-top:20px">Tu aporte sostiene el centro de acogida, los controles de salud y los talleres en Kibera. Puedes hacerte socio con un aporte mensual o hacer una donación única.</p>
    <figure style="margin-top:34px"><img src="img/campana-2027.jpg" alt="Campaña 10 mujeres, 10 historias, 10 vidas para el 2027" style="width:100%;border-radius:var(--r)"></figure>
  </div>
  <div id="socio">
    <div class="tabs" role="tablist" aria-label="Tipo de aporte">
      <button role="tab" type="button" data-tab="mensual" aria-selected="true">Hazte socio</button>
      <button role="tab" type="button" data-tab="unico" aria-selected="false">Aporte único</button>
    </div>
    <form class="card dcard" id="mensual" role="tabpanel">
      <h2 style="font-size:var(--step-2)">Aporte mensual</h2>
      <div class="amounts" role="group" aria-label="Monto mensual">
        <button type="button" data-amt="10000">$10.000</button><button type="button" data-amt="25000">$25.000</button><button type="button" data-amt="100000">$100.000</button><button type="button" data-amt="other">Otro</button>
      </div>
      <input id="d-other" class="field" hidden inputmode="numeric" placeholder="Escribe un monto en pesos" aria-label="Otro monto" style="font:inherit;padding:.85em 1em;border:1.5px solid var(--orange);border-radius:12px;background:var(--card);color:var(--ink)">
      <p class="equiv" id="d-eq"></p>
      <div class="form-grid">
        <div class="field"><label for="d-name">Nombre</label><input id="d-name" required></div>
        <div class="field"><label for="d-mail">Email</label><input id="d-mail" type="email" required></div>
      </div>
      <button class="btn btn-donate" id="d-go" type="submit">Hacerme socio</button>
      <p class="ok-msg" id="d-ok" hidden>Prototipo: aquí se abre el pago mensual (Webpay / Flow).</p>
      <p class="small">¿Vives fuera de Chile? Suscríbete como socio en moneda internacional a través de <b>PayPal</b>.</p>
    </form>
    <div class="card dcard" id="unico" role="tabpanel" hidden>
      <h2 style="font-size:var(--step-2)">Donación única</h2>
      <div class="methods">
        <div class="method"><h3>Transferencia electrónica</h3>
          <div class="bank">
            <span>Nombre</span><b>Fundación Maisha</b><button class="copy" type="button" data-copy="Fundación Maisha">Copiar</button>
            <span>Banco</span><b>BCI · Cuenta corriente</b><span></span>
            <span>N° cuenta</span><b>28988957</b><button class="copy" type="button" data-copy="28988957">Copiar</button>
            <span>RUT</span><b>65.142.454-2</b><button class="copy" type="button" data-copy="65.142.454-2">Copiar</button>
            <span>Email</span><b>donaciones@fundacionmaisha.com</b><button class="copy" type="button" data-copy="donaciones@fundacionmaisha.com">Copiar</button>
          </div>
        </div>
        <div class="method"><h3>Tarjeta de crédito o débito</h3><p>Visa, Mastercard y Redcompra a través de Webpay.</p><a class="btn btn-navy btn-sm" href="#unico" style="justify-self:start;margin-top:6px">Pagar con tarjeta</a></div>
        <div class="method"><h3>Desde Kenia · M-Pesa</h3><p>Lipa na M-Pesa · Till Number <b style="color:var(--ink)">9560405</b></p></div>
        <div class="method"><h3>Desde otros países · PayPal</h3><p>Donaciones en moneda internacional.</p></div>
      </div>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="head"><p class="eyebrow">Tu aporte en Kibera</p><h2 class="h2">¿Qué podemos hacer con tus aportes?</h2></div>
  <div class="what">
    <div class="card"><img src="img/salud-3.jpg" alt="" loading="lazy"><div><b>$10.000</b><p>Una ecografía: ver al bebé por primera vez.</p></div></div>
    <div class="card"><img src="img/salud-4.jpg" alt="" loading="lazy"><div><b>$25.000</b><p>Un control prenatal: un embarazo acompañado, mes a mes.</p></div></div>
    <div class="card"><img src="img/salud-2.jpg" alt="" loading="lazy"><div><b>$250.000</b><p>Una atención de parto segura, acompañada y digna.</p></div></div>
    <div class="card"><img src="img/acogida-2.jpg" alt="" loading="lazy"><div><b>$1.000.000</b><p>La acogida completa de una Madre Maisha, del embarazo al postparto.</p></div></div>
  </div>
</div></section>
'''
    page('dona.html', 'Dona · Fundación Maisha', 'dona', body, css, js)


# ---------------------------------------------------------------- MARKET
PRODUCTS = [("Necessaire","Accesorios",12000),("Joyero","Accesorios",14000),("Simio","Deco",15000),("Estrellita Nyota","Deco",5500),
            ("Lanyard Masai Mara","Accesorios",8000),("Kesi Big","Accesorios",8000),("Tote Bag Nairobi","Accesorios",8500),("Tote Bag Wambui","Accesorios",12000),
            ("Corazón Sagrado Big","Corazón Sagrado",8000),("Porta chupetes Baby","Infantil",9500),("Babero Baby","Infantil",8500),("Jirafa L","Deco",12000),("Elefante M","Deco",8000)]


def build_market():
    css = '''
.mk-hero{padding-top:120px}
.mk-head{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:end}
.mk-head > *{min-width:0}
.mk-banner{position:relative;border-radius:var(--r);overflow:hidden}
.mk-banner img{width:100%;height:auto}
.mk-banner .hand{position:absolute;left:16px;bottom:14px;background:var(--card);padding:10px 16px;border-radius:12px;transform:rotate(-3deg)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:44px 0 26px}
.chips button{font:500 .93rem var(--display);padding:.6em 1.1em;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.chips button[aria-pressed="true"]{background:var(--navy);color:var(--on-navy);border-color:var(--navy)}
.products{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
.product{display:grid;gap:10px}
.product .ph{position:relative;border-radius:20px;overflow:hidden;background:var(--sand)}
.product img{width:100%;aspect-ratio:1;object-fit:cover;transition:transform .35s ease}
.product:hover img{transform:scale(1.04)}
.product .add{position:absolute;right:10px;bottom:10px;font:600 .88rem var(--display);border:0;border-radius:999px;padding:.7em 1.1em;background:var(--orange);color:#081326;cursor:pointer;box-shadow:0 6px 16px rgba(0,0,0,.15)}
.product h3{font-size:1.02rem;font-weight:600}
.product p{display:flex;justify-content:space-between;color:var(--muted);font-size:.93rem}
.product p b{color:var(--ink);font-variant-numeric:tabular-nums}
@media (max-width:1000px){.products{grid-template-columns:repeat(3,1fr)}}
@media (max-width:700px){.mk-head{grid-template-columns:1fr}.products{grid-template-columns:1fr 1fr;gap:14px}.product .add{padding:.6em .9em;font-size:.8rem}}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.why .card{padding:26px}
.why h3{font-size:1.1rem;margin-bottom:6px}
.why p{color:var(--muted);font-size:.96rem}
@media (max-width:800px){.why{grid-template-columns:1fr}}
.drawer{position:fixed;inset:0;z-index:70;display:flex;justify-content:flex-end;background:rgba(11,24,48,.45)}
.drawer[hidden]{display:none}
.drawer aside{width:min(420px,100%);height:100%;background:var(--paper);display:flex;flex-direction:column;padding:calc(22px + env(safe-area-inset-top,0px)) max(22px,env(safe-area-inset-right,0px)) calc(22px + env(safe-area-inset-bottom,0px)) 22px;box-shadow:-20px 0 40px rgba(0,0,0,.2)}
.drawer header{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}
.drawer h2{font-size:var(--step-2)}
.drawer .x{border:0;background:var(--sand);color:var(--ink);width:40px;height:40px;border-radius:50%;cursor:pointer;font-size:1.2rem}
.lines{flex:1;overflow:auto;display:grid;gap:14px;align-content:start}
.line{display:grid;grid-template-columns:64px 1fr auto;gap:12px;align-items:center}
.line img{width:64px;height:64px;border-radius:12px;object-fit:cover}
.line b{display:block;font:600 .95rem var(--display)}
.line span{font-size:.85rem;color:var(--muted)}
.qty{display:flex;align-items:center;gap:8px}
.qty button{width:28px;height:28px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.total{display:flex;justify-content:space-between;font:700 1.1rem var(--display);padding:18px 0;border-top:1px solid var(--line);margin-top:12px}
.empty{color:var(--muted);text-align:center;padding:40px 0}
'''
    prods = ''.join(f'''<article class="product" data-cat="{e(c)}">
  <div class="ph"><img src="img/market/p{i:02d}.jpg" alt="{e(n)}" loading="lazy"><button class="add" type="button" data-i="{i}">Agregar</button></div>
  <h3>{e(n)}</h3><p><span>{e(c)}</span><b>${p:,.0f}</b></p>
</article>'''.replace(',', '.') for i, (n, c, p) in enumerate(PRODUCTS))
    cats = sorted(set(c for _, c, _ in PRODUCTS))
    chips = '<button type="button" aria-pressed="true" data-cat="">Todos</button>' + ''.join(f'<button type="button" aria-pressed="false" data-cat="{e(c)}">{e(c)}</button>' for c in cats)
    js = 'var PRODUCTS=' + json.dumps([dict(n=n, c=c, p=p, img=f'img/market/p{i:02d}.jpg') for i, (n, c, p) in enumerate(PRODUCTS)], ensure_ascii=False) + ';' + r'''
(function(){
  var C=window.maishaCart, cart=C.read(), dr=document.getElementById('drawer'), lines=document.getElementById('lines'), tot=document.getElementById('total'), msg=document.getElementById('co-msg');
  var fmt=function(n){return '$'+n.toLocaleString('es-CL');};
  function render(){
    C.write(cart);
    if(!cart.length){lines.innerHTML='<p class="empty">Tu carrito está vacío.</p>';tot.textContent=fmt(0);return;}
    lines.innerHTML=cart.map(function(l,k){var p=PRODUCTS[l.i];return '<div class="line"><img src="'+p.img+'" alt=""><div><b>'+p.n+'</b><span>'+fmt(p.p)+'</span></div><div class="qty"><button type="button" data-k="'+k+'" data-d="-1" aria-label="Quitar uno">−</button>'+l.q+'<button type="button" data-k="'+k+'" data-d="1" aria-label="Agregar uno">+</button></div></div>';}).join('');
    tot.textContent=fmt(cart.reduce(function(a,l){return a+PRODUCTS[l.i].p*l.q;},0));
  }
  function open(){dr.hidden=false;msg.hidden=true;}
  document.querySelectorAll('.add').forEach(function(b){b.onclick=function(){var i=+b.dataset.i,f=cart.filter(function(l){return l.i===i;})[0];if(f)f.q++;else cart.push({i:i,q:1});render();open();};});
  lines.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var k=+b.dataset.k;cart[k].q+=+b.dataset.d;if(cart[k].q<1)cart.splice(k,1);render();});
  document.getElementById('x').onclick=function(){dr.hidden=true;};
  dr.addEventListener('click',function(e){if(e.target===dr)dr.hidden=true;});
  document.querySelectorAll('.cart-btn').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();open();});});
  document.getElementById('checkout').onclick=function(){msg.hidden=false;};
  var chips=[].slice.call(document.querySelectorAll('.chips button'));
  chips.forEach(function(c){c.onclick=function(){chips.forEach(function(x){x.setAttribute('aria-pressed',String(x===c));});document.querySelectorAll('.product').forEach(function(p){p.hidden=!!c.dataset.cat&&p.dataset.cat!==c.dataset.cat;});};});
  if(location.hash==='#carrito') open();
  render();
})();'''
    body = f'''
<section class="mk-hero"><div class="wrap">
  <div class="mk-head">
    <div>
      <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><span>The Maisha Market</span></nav>
      <h1 class="h1">The Maisha <em>Market</em></h1>
      <p class="lead" style="margin-top:18px">Productos 100% solidarios, hechos a mano con telas africanas. Todo lo recaudado nos ayuda a acoger a más Madres Maisha en nuestra casa de acogida en Kenia.</p>
    </div>
    <figure class="mk-banner"><img src="img/sustentabilidad-hero.jpg" alt="Madre Maisha cosiendo en el taller"><span class="hand">Hecho en Kenia</span></figure>
  </div>
  <div class="chips" role="group" aria-label="Categorías">{chips}</div>
  <div class="products">{prods}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="why">
    <div class="card"><h3>Hecho a mano</h3><p>Cuidadosamente confeccionado para ti, con mucho amor.</p></div>
    <div class="card"><h3>Productos con sentido</h3><p>Cada compra ayuda a mantener la casa de acogida para Madres Maisha.</p></div>
    <div class="card"><h3>Hecho en Kenia</h3><p>Gran parte de nuestros productos los confeccionan Madres Maisha.</p></div>
  </div>
  <div class="panel cta-card" style="margin-top:28px">
    <div><h2 class="h2">Regalos corporativos</h2><p>Regalos con propósito para tu empresa o evento. Pide nuestro catálogo.</p></div>
    <div class="row"><a class="btn btn-navy" href="#contacto">Pedir catálogo</a></div>
  </div>
</div></section>

<div class="drawer" id="drawer" hidden role="dialog" aria-modal="true" aria-labelledby="cart-h">
  <aside>
    <header><h2 id="cart-h">Tu carrito</h2><button class="x" id="x" type="button" aria-label="Cerrar carrito">×</button></header>
    <div class="lines" id="lines"></div>
    <div class="total"><span>Total</span><span id="total">$0</span></div>
    <button class="btn btn-donate" id="checkout" type="button">Ir a pagar</button>
    <p class="ok-msg" id="co-msg" hidden style="margin-top:12px">Prototipo: aquí se abre el checkout de Shopify.</p>
  </aside>
</div>
'''
    page('market.html', 'The Maisha Market', 'market', body, css, js)


if __name__ == '__main__':
    if DEPLOY:
        shutil.rmtree(ROOT, ignore_errors=True); os.makedirs(ROOT)
        for d in ('assets','img','memorias'): shutil.copytree(os.path.join(SRC,d), os.path.join(ROOT,d))
    build_home(); build_nosotros(); build_voluntariado(); build_dona(); build_market()
    for p in PROGRAMS: build_program(p)
    print('ok')
