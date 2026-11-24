# Cómo poner el sitio de Maisha en Wix Studio

El diseño completo ya está hecho. En Wix solo hay que crear las páginas y pegar en cada una un **Elemento personalizado** con el link que corresponde. No hay que diseñar nada.

> **Requisito de Wix:** los elementos personalizados solo funcionan en sitios con **plan Premium y dominio conectado**. El plan que pagó Maisha cumple con esto.

---

## 1. Preparar el sitio en Wix Studio

1. Abre el sitio en el editor de Wix Studio.
2. **Borra el contenido del encabezado (header) y del pie de página (footer)** de Wix, o desactívalos. El diseño ya trae su propio menú, footer y botón de WhatsApp. Si no los borras, saldrán duplicados.
3. Deja el fondo de las páginas en **blanco**.

## 2. Crear las 10 páginas

Crea estas páginas con **exactamente estas direcciones (URL)**. Así funcionan todos los links del menú. La dirección se cambia en *Configuración de la página → SEO → URL de la página*.

| Página | Dirección (URL) | Link del elemento (Server URL) | Nombre de la etiqueta (Tag name) |
|---|---|---|---|
| Inicio | `/` (página de inicio) | `https://maisha-site.vercel.app/wix/index.js` | `maisha-inicio` |
| Nosotros | `/nosotros` | `https://maisha-site.vercel.app/wix/nosotros.js` | `maisha-nosotros` |
| Voluntariado | `/voluntariado` | `https://maisha-site.vercel.app/wix/voluntariado.js` | `maisha-voluntariado` |
| Dona | `/dona` | `https://maisha-site.vercel.app/wix/dona.js` | `maisha-dona` |
| Maisha Market | `/market` | `https://maisha-site.vercel.app/wix/market.js` | `maisha-market` |
| Acogida | `/programa-acogida` | `https://maisha-site.vercel.app/wix/programa-acogida.js` | `maisha-programa-acogida` |
| Salud | `/programa-salud` | `https://maisha-site.vercel.app/wix/programa-salud.js` | `maisha-programa-salud` |
| Educación Sexual | `/programa-educacion` | `https://maisha-site.vercel.app/wix/programa-educacion.js` | `maisha-programa-educacion` |
| Sustentabilidad | `/programa-sustentabilidad` | `https://maisha-site.vercel.app/wix/programa-sustentabilidad.js` | `maisha-programa-sustentabilidad` |
| Derechos Humanos | `/programa-derechos` | `https://maisha-site.vercel.app/wix/programa-derechos.js` | `maisha-programa-derechos` |

Las páginas de programas no necesitan aparecer en el menú de Wix. El menú del diseño ya las incluye.

## 3. Poner el elemento en cada página

En cada página:

1. Haz clic en **Agregar elementos (+) → Código incrustado (Embed code) → Elemento personalizado (Custom element)**.
2. Arrástralo a la página y haz clic en **Elegir origen (Choose source)**.
3. Elige **Server URL** y pega el **link del elemento** de la tabla.
4. En **Tag name** escribe el **nombre de la etiqueta** de la tabla (por ejemplo `maisha-inicio`).
5. Estira el elemento al **ancho completo de la página** (en Wix Studio: *Estirar / Stretch*) y ubícalo **arriba de todo**, sin márgenes.
6. Dale una altura grande (por ejemplo 3000 px). El elemento ajusta su altura solo al contenido al publicar, pero en el editor puede verse cortado. Eso es normal.

> En el editor, a veces el elemento personalizado se ve vacío o cortado. **Revisa siempre en *Vista previa* o en el sitio publicado.**

## 4. Títulos para Google (SEO)

En *Configuración de la página → SEO* de cada página, pon el título y la descripción. Sugerencias:

- **Inicio:** "Fundación Maisha · Porque todo embarazo merece compañía"
- **Nosotros:** "Nosotros · Fundación Maisha"
- **Programas:** "Acogida · Fundación Maisha" (y así con cada uno)

## 5. Publicar

Publica el sitio y revisa cada página en computador y celular.

---

## Cómo se actualiza el diseño

Los elementos se cargan desde `maisha-site.vercel.app`. Cuando se haga un cambio de diseño o texto, se actualiza en Vercel y **Wix lo muestra solo, sin tocar nada en Wix** (puede tardar unos minutos por el caché).

## Cosas que conviene saber

- **Las fotos, PDFs y videos** también se cargan desde Vercel, así que el proyecto de Vercel tiene que seguir activo. El plan gratuito de Vercel alcanza.
- **Los formularios** (newsletter, voluntariado, donación) todavía son de prueba: muestran un mensaje, pero no envían datos. Hay que conectarlos a su destino real (correo, Mailchimp, pasarela de pago).
- **La tienda** se conecta a Shopify en un segundo paso.
- **Google** lee este contenido porque se genera con JavaScript. Google procesa JavaScript, pero es un poco más lento que con texto normal.
