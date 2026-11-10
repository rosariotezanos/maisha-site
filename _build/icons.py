"""Íconos Maisha: rediseño de los íconos del sitio actual.
Mismo lenguaje que los originales (línea gris + acento naranjo), con trazos parejos y redondeados.
.l = línea (toma el color del texto), .f = relleno naranjo."""

def _hand(x, y, s, cls):
    # Mano levantada: palma + cuatro dedos + pulgar
    t = f'transform="translate({x} {y}) scale({s})"'
    if cls == 'f':
        return (f'<g {t}><rect class="f" x="-7" y="0" width="14" height="13" rx="5"/>'
                '<path class="fs" d="M-5 1v-9M-1.7 0v-12M1.7 0v-11M5 1v-8M-7 7l-4-5"/></g>')
    return (f'<g {t}><rect class="l" x="-7" y="0" width="14" height="13" rx="5"/>'
            '<path class="l" d="M-5 1v-9M-1.7 0v-12M1.7 0v-11M5 1v-8M-7 7l-4-5"/></g>')

ICONS = {
  # ---- programas (rediseño de los 5 íconos del sitio actual)
  'acogida': '<path class="l" d="M7 22 24 8l17 14v17a3 3 0 0 1-3 3H10a3 3 0 0 1-3-3z"/>'
             '<path class="f" d="M24 36c-5.6-3.7-8.6-6.6-8.6-10a4.3 4.3 0 0 1 8.6-1.4 4.3 4.3 0 0 1 8.6 1.4c0 3.4-3 6.3-8.6 10z"/>',
  'salud': '<path class="l" d="M11 5v11a8 8 0 0 0 16 0V5M8 5h6M24 5h6M19 24v5a10 10 0 0 0 20 0v-4"/>'
           '<circle class="f" cx="39" cy="21" r="5"/><circle class="l" cx="39" cy="21" r="5"/>',
  'educacion': '<path class="f" d="M24 9a11.5 11.5 0 0 0-6.8 20.8c1.1.9 1.8 2.1 1.8 3.5V34h10v-.7c0-1.4.7-2.6 1.8-3.5A11.5 11.5 0 0 0 24 9z"/>'
               '<path class="l" d="M19 38.5h10M20.5 43h7M24 2.5V5M7 20.5H4.5M43.5 20.5H41M11.5 8l1.8 1.8M36.5 8l-1.8 1.8"/>',
  'sustentabilidad': '<rect class="f" x="7" y="31" width="8" height="11" rx="1.5"/><rect class="f" x="20" y="24" width="8" height="18" rx="1.5"/>'
                     '<rect class="f" x="33" y="16" width="8" height="26" rx="1.5"/>'
                     '<path class="l" d="M6 22 31 7M23.5 6.5H31V14"/>',
  'derechos': _hand(12, 22, .9, 'l') + _hand(36, 22, .9, 'l') + _hand(24, 20, 1.15, 'f'),

  # ---- cifras
  'embarazada': '<circle class="l" cx="21.5" cy="7.5" r="4.3"/>'
                '<path class="f" d="M25 19.6c6.3 1.5 10 5.3 10 9.6 0 4.4-3.6 7.5-8.8 7.8.9-5.6.6-11.6-1.2-17.4z"/>'
                '<path class="l" d="M19.3 13.6c-2.6 2.4-3.9 6.5-3.9 11 0 3.9 1.2 7.2 3.4 9.7V44M23.8 13.6c1.6 1.6 1.7 3.7 1.2 6 1.8 5.8 2.1 11.8 1.2 17.4V44"/>'
                '<path class="l" d="M19.6 18.2c.3 4.2 2.4 7.6 6.2 9.4"/>',
  'telefono': '<path class="l" d="M15 7h-4a3 3 0 0 0-3 3.3C9.4 27 21 38.6 37.7 40a3 3 0 0 0 3.3-3v-4l-8-3.2-3.6 3.6A24 24 0 0 1 18.6 22.6l3.6-3.6L19 11z"/>'
              '<path class="fs" d="M29 6.5A12.5 12.5 0 0 1 41.5 19M29 13a6 6 0 0 1 6 6"/>',
  'casa': '<path class="l" d="M7 22 24 8l17 14v17a3 3 0 0 1-3 3H10a3 3 0 0 1-3-3z"/><rect class="f" x="19" y="28" width="10" height="14" rx="2"/>',
  'visita': '<path class="l" d="M5 27 16 18l11 9v13a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"/>'
            '<path class="f" d="M35 5a7 7 0 0 0-7 7c0 5.3 7 12 7 12s7-6.7 7-12a7 7 0 0 0-7-7z"/><circle cx="35" cy="12" r="2.6" fill="#fff"/>',
  'regalo': '<path class="l" d="M7 19h34v7H7zM10 26h28v16H10zM24 19v23"/>'
            '<path class="f" d="M24 19c-2.7-6.3-11.5-8-11-2.3.3 3 6 2.3 11 2.3zM24 19c2.7-6.3 11.5-8 11-2.3-.3 3-6 2.3-11 2.3z"/>',
  'corazon': '<path class="f" d="M24 41C12 33.4 6 27.3 6 19.6A9.6 9.6 0 0 1 24 15a9.6 9.6 0 0 1 18 4.6C42 27.3 36 33.4 24 41z"/>'
             '<path class="fs-w" d="M11 24h7l3-5 4 9 3-4h9"/>',
  'grupo': '<circle class="l" cx="11" cy="17" r="4.5"/><circle class="l" cx="37" cy="17" r="4.5"/>'
           '<path class="l" d="M3 38v-3a8 8 0 0 1 13-6.2M45 38v-3a8 8 0 0 0-13-6.2"/>'
           '<circle class="f" cx="24" cy="15" r="6"/><path class="f" d="M13 42v-4a11 11 0 0 1 22 0v4z"/>',
  'estetoscopio': '<path class="l" d="M11 5v11a8 8 0 0 0 16 0V5M8 5h6M24 5h6M19 24v5a10 10 0 0 0 20 0v-4"/><circle class="f" cx="39" cy="21" r="5"/>',
  'bebe': '<circle class="l" cx="24" cy="14" r="7"/><path class="f" d="M14 30a10 10 0 0 1 20 0v6a7 7 0 0 1-7 7h-6a7 7 0 0 1-7-7z"/>'
          '<path class="l" d="M21 13.5h.01M27 13.5h.01M22 17.5c1.2.8 2.8.8 4 0"/>',
  'ecografia': '<rect class="l" x="5" y="6" width="38" height="27" rx="3"/><path class="l" d="M18 42h12M24 33v9"/>'
               '<path class="f" d="M20 14a6 6 0 1 1 1.5 11.8c-2.8.6-5-1.4-5-4 0-1.7 1-2.6 1-4.3 0-1.6.9-3 2.5-3.5z"/>',
  'gota': '<path class="f" d="M24 5s-12 13.5-12 22a12 12 0 0 0 24 0C36 18.5 24 5 24 5z"/><path class="fs-w" d="M18.5 28a5.5 5.5 0 0 0 5.5 5.5"/>',
  'birrete': '<path class="l" d="M3 17 24 8l21 9-21 9z"/><path class="l" d="M11 21.5V31c0 3.3 5.8 6.5 13 6.5s13-3.2 13-6.5v-9.5"/>'
             '<path class="fs" d="M43 18v12"/><circle class="f" cx="43" cy="32" r="2.6"/>',
  'escuela': '<path class="l" d="M6 42V22l18-10 18 10v20M6 42h36M20 42v-9h8v9"/><path class="l" d="M24 12V4"/><path class="f" d="M24 4h9l-2.5 3 2.5 3h-9z"/>',
  'toalla': '<path class="f" d="M18 6h12a6 6 0 0 1 6 6v3.5l5 2.5v12l-5 2.5V36a6 6 0 0 1-6 6H18a6 6 0 0 1-6-6v-3.5L7 30V18l5-2.5V12a6 6 0 0 1 6-6z"/>'
            '<path class="fs-w" d="M20 16h.01M28 16h.01M24 22h.01M20 28h.01M28 28h.01M24 34h.01"/>',
  'sesiones': '<rect class="l" x="6" y="9" width="36" height="33" rx="3"/><path class="l" d="M6 18h36M15 5v8M33 5v8"/>'
              '<path class="fs" d="M14 29l3 3 5-6M27 29l3 3 5-6"/>',
  'hilo': '<path class="l" d="M14 6h20M14 42h20"/><rect class="f" x="17" y="9" width="14" height="30" rx="3"/>'
          '<path class="fs-w" d="M17 15l14 5M17 22l14 5M17 29l14 5"/><path class="l" d="M31 13c6 0 10 3 10 8s-5 7-5 12"/>',
  'bandera': '<path class="l" d="M10 44V5"/><path class="f" d="M10 6h26l-5 7 5 7H10z"/>',
}


def icon(name, cls='ico'):
    return f'<svg class="{cls}" viewBox="0 0 48 48" aria-hidden="true">{ICONS[name]}</svg>'
