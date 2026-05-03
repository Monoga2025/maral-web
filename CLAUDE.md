# Industrias Maral — Contexto del Proyecto

## Empresa
- **Nombre:** Industrias Maral S.A.S
- **Ubicación:** Curití, Santander, Colombia
- **Marcas:** MAXANT (antenas móviles), ALMOTCOM (estaciones base/Yagi)
- **Modelo de negocio:** B2B mayorista — los clientes son distribuidores, no usuarios finales. Compran grandes volúmenes. La tienda debe optimizarse para seleccionar muchos productos rápido.
- **Contacto:** ventas@industriasmaral.com · (+57) 316 776 0692 · WhatsApp: 573167760692

---

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `index.html` | Landing page principal |
| `tienda.html` | Tienda / catálogo de productos |
| `img/` | Imágenes locales de productos (26 PNG descargadas de WordPress) |
| `enhance_images.py` | Script para mejorar fotos con Gemini API (requiere billing activo) |
| `Componentes/` | Componentes React de referencia (shadcn/Tailwind) — solo para inspiración visual |

---

## Stack técnico
- **Vanilla HTML/CSS/JS** — sin frameworks, archivos únicos autocontenidos
- **Sin build tools** — abrir directo en browser
- **Imágenes:** `./img/` (local) con fallback a `https://industriasmaral.com/wp-content/uploads/2023/03/`

---

## Sistema tipográfico (NO cambiar)
```css
--font: 'Barlow', sans-serif;           /* body, UI */
--display: 'Barlow Condensed', sans-serif; /* títulos, headings */
--mono: 'DM Mono', monospace;           /* SKUs, precios, datos técnicos */
```
- **PROHIBIDO:** Syne, Outfit, Inter, Space Grotesk — el usuario los rechazó explícitamente
- Barlow Condensed: weights 600/700/800 para display
- Barlow: 400/500/600/700 para body

---

## Paleta de colores (CSS variables)
```css
--navy:  #04122A   /* fondo oscuro principal */
--navy2: #082040
--blue:  #1255A8
--org:   #0EA5E9   /* sky blue — acento primario (antes era naranja) */
--org2:  #38BDF8   /* sky light */
--bg:    #EFF5FC   /* fondo página */
--bg2:   #FFFFFF
--txt:   #080F1E
--txt2:  #364B66
--txt3:  #7A90A8
--bdr:   #C8D8EC
--green: #059669
```
- El logo circle del nav es `fill="#0EA5E9"` (azul sky) — antes era naranja `#E85D00`

---

## Decisiones de diseño

### index.html
- Grain texture en `body::after` con SVG `feTurbulence`, `mix-blend-mode: multiply`
- Nav glassmorphism: `backdrop-filter: blur(24px) saturate(180%)`
- Ambient orbs: pseudo-elementos `::before/::after` con radial gradients en secciones
- Cards con `::after` barra top que `scaleX` 0→1 en hover
- Marquee de clientes: `animation: marquee-scroll 22s linear infinite` + `mask-image` fade edges
- Stats con `text-shadow: 0 0 40px rgba(56,189,248,.35)` en los números

### tienda.html
- **Layout full-width** — eliminado sidebar fijo de 256px; `max-width: var(--max); margin: 0 auto`
- **Filter drawer** slide-in: `position:fixed; transform:translateX(-100%)` — el sidebar se convirtió en drawer
- **Catalog header** oscuro navy arriba del grid con stats y botón de filtros
- **Grid de productos:** `gap:1px; background:var(--bdr); border:1px solid var(--bdr)` — separadores ultra-finos
- **Cards hover:** `box-shadow: 0 0 0 2px var(--org), 0 16px 48px rgba(14,165,233,.18); transform: scale(1.01)` — doble ring premium
- **Imágenes:** `background: #fff` en `.pcard-img` + `mix-blend-mode: multiply` en img → elimina fondo blanco sobre gris
- **Qty en card:** controles +/− directamente en la tarjeta, sin abrir modal
- **Sticky cart bar:** `position:fixed; bottom:0` sube cuando el carrito tiene items

### Variables JS importantes (tienda.html)
- `searchQ` — variable del buscador (NO `searchTerm`)
- `IMG` — `'./img/'` (antes era `'../Maral/wp-content/uploads/2023/03/'`)
- `IMG_FALLBACK` — `'https://industriasmaral.com/wp-content/uploads/2023/03/'`
- `render()` — función principal de renderizado del catálogo
- `updateBadge()` — llama a `updateStickyCart()` al final
- `addFromCard(id)` — agrega producto desde la tarjeta con qty del input

---

## Imágenes de productos

### Estado actual
- **26 imágenes reales** en `./img/` (descargadas de WordPress)
- **9 placeholders SVG** en `./img/` para productos ALMOTCOM y Yagi (mr801, mr801b, mr802, mr803, mr805, mr415, mr416, mr430-2, mr430) que no tienen fotos en el servidor

### Fallback chain en el HTML
```
./img/archivo.png → (onerror) → industriasmaral.com/.../archivo.png → (onerror) → SVG placeholder 📡
```

### Mejora de imágenes con IA
El usuario validó que Gemini (web) produce fotos premium a partir de las originales con fondo blanco.

**Proceso manual:** gemini.google.com → subir imagen original + prompt → guardar resultado en `./img/` con mismo nombre

**Proceso automático:** `python enhance_images.py` — requiere billing activo en aistudio.google.com (~$1 USD para las 35 fotos con Imagen 4 Fast)

**Prompt de mejora adaptado para antenas:**
```
Professional commercial studio product photo of a radio antenna (MAXANT / MARAL brand).

Keep the EXACT same antenna model, geometry, proportions and brand markings.
Do NOT change the antenna shape, connector, or any identifying feature.
Do NOT add or remove parts.

Background: dark charcoal gradient (#1a1a1a center, #0a0a0a edges).
Subtle radial highlight beneath the antenna (floor reflection).

Lighting: directional from upper-left, warm 5600K highlights on metallic parts.
Fill light: soft cool-toned from right, ratio 3:1. Rim backlight to separate from bg.

Sony A1, 85mm f/1.4 at f/2.0, ISO 100, 1/200s equivalent.
Deep dynamic range, micro-contrast, real metallic texture, subtle film grain.
4K, sharp focus, cinematic contrast curve.

NEGATIVE: no new background, no color shift, no cartoon, no distortion of shape.
```

---

## Google AI API
- **Key:** `AIzaSyALkv-vxbmjH7tcze0y9M-WTEA6OIBBZqI`
- **Plan:** Free tier — `limit: 0` para todos los modelos de imagen (Imagen 4, gemini-2.5-flash-image, gemini-3.1-flash-image-preview)
- Para activar: aistudio.google.com/apikey → Billing

---

## Componentes de referencia (Componentes/*.txt)
Contienen código React/shadcn de inspiración — NO se usan directamente. Se adaptan a vanilla JS/CSS.

| Archivo | Componente |
|---|---|
| `2.txt` | Barra de búsqueda con autocomplete (ya implementada en tienda.html) |
| `4.txt` | Radar effect con framer-motion |
| `5.txt` | Wireframe dotted globe (d3.js) |
| `6.txt` | GLSL Hills background (Three.js) |

---

## Pendientes
- [ ] Mejorar las 26 fotos con Gemini cuando se active billing
- [ ] Conseguir fotos reales para los 9 productos ALMOTCOM/Yagi (mr*)
- [ ] index.html: revisar sección de clientes (logos reales)
