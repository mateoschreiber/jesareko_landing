# Jesareko Editorial Technical Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rediseñar las seis páginas públicas de Jesareko con una interfaz editorial técnica mobile-first, contenido más breve, imágenes oficiales de calidad y una conversión principal hacia WhatsApp.

**Architecture:** Mantener el sitio estático actual y sus URLs, consolidar el sistema visual en una única hoja CSS y conservar un único script progresivo para navegación, acordeones y contacto. Las páginas compartirán el mismo encabezado, footer, tokens y contratos de accesibilidad, mientras cada página tendrá una secuencia de contenido específica y verificable.

**Tech Stack:** HTML5 estático, CSS moderno sin framework, JavaScript ES2020 sin dependencias, Python `unittest` para contratos estructurales, Cloudflare Pages/Wrangler para publicación.

## Global Constraints

- Prioridad mobile desde 320 px; validar 320, 360, 390, 430, 768, 1024, 1280 y 1440 px.
- Conservar el logo y el verde de Jesareko con un uso más sobrio.
- Usar Inter para cuerpo y navegación, Merriweather para titulares editoriales.
- Radios: 10 px en controles pequeños, 14 px en botones/tarjetas compactas y 20 px en paneles/imágenes.
- Área táctil mínima: 48 × 48 px.
- WhatsApp es el CTA principal y debe usar un SVG oficial con texto visible.
- No usar estadísticas, certificaciones, testimonios ni resultados inventados.
- No depender de hover, carruseles o elementos superpuestos para comprender o usar el sitio.
- Registrar origen y licencia de cada imagen externa en `docs/image-sources.json`.
- No introducir dependencias de frontend, CMS ni proceso de compilación.
- Ninguna página puede tener desbordamiento horizontal, logos deformados o saltos de layout evitables.

---

## File Map

- `public/assets/css/styles.css`: tokens, reset, layout, componentes y responsive; se reemplaza por una versión consolidada sin bloques duplicados.
- `public/assets/js/main.js`: navegación mobile, acordeones, botón volver arriba y flujo accesible del formulario.
- `public/index.html`: portada y recorrido de conversión.
- `public/servicios.html`: identificación de necesidades y alcance de servicios.
- `public/casos.html`: situaciones frecuentes y casos verificables.
- `public/tecnologias.html`: catálogo editorial de tecnologías y marcas.
- `public/contacto.html`: WhatsApp principal y formulario secundario.
- `public/privacidad.html`: contenido legal dentro del nuevo shell visual.
- `public/assets/img/brands/`: imágenes oficiales optimizadas de Hikvision y Dahua.
- `docs/image-sources.json`: procedencia, licencia, producto y archivo local de imágenes.
- `tests/test_site_contract.py`: estructura, accesibilidad estática, navegación y activos.
- `tests/test_content_contract.py`: arquitectura y contenido mínimo por página.
- `README.md`: comandos de verificación y procedimiento de revisión local.

---

### Task 1: Add the static-site contract test harness

**Files:**
- Create: `tests/test_site_contract.py`
- Create: `tests/test_content_contract.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: archivos HTML de `public/` y activos referenciados mediante rutas relativas.
- Produces: comando estable `python -m unittest discover -s tests -v` para todos los trabajos posteriores.

- [ ] **Step 1: Write the failing shared-shell tests**

Crear `tests/test_site_contract.py` con este contenido inicial:

```python
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PAGES = ["index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html", "privacidad.html"]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.h1_count = 0
        self.images = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            self.images.append(attrs)
        if tag == "a":
            self.links.append(attrs)


def parse_page(name):
    parser = PageParser()
    parser.feed((PUBLIC / name).read_text(encoding="utf-8"))
    return parser


class SiteContractTests(unittest.TestCase):
    def test_every_page_has_one_h1_and_unique_ids(self):
        for page in PAGES:
            with self.subTest(page=page):
                parsed = parse_page(page)
                self.assertEqual(parsed.h1_count, 1)
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))

    def test_images_have_alt_and_dimensions(self):
        for page in PAGES:
            for image in parse_page(page).images:
                with self.subTest(page=page, src=image.get("src")):
                    self.assertIn("alt", image)
                    self.assertIn("width", image)
                    self.assertIn("height", image)

    def test_blank_targets_are_safe(self):
        for page in PAGES:
            for link in parse_page(page).links:
                if link.get("target") == "_blank":
                    rel = set(link.get("rel", "").split())
                    self.assertTrue({"noopener", "noreferrer"}.issubset(rel))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the baseline failure**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: FAIL en imágenes existentes que no reservan `width` y `height`; el fallo demuestra que el contrato detecta saltos de layout potenciales.

- [ ] **Step 3: Add the content-test skeleton**

Crear `tests/test_content_contract.py`:

```python
from pathlib import Path
import unittest

PUBLIC = Path(__file__).resolve().parents[1] / "public"


def html(name):
    return (PUBLIC / name).read_text(encoding="utf-8")


class ContentContractTests(unittest.TestCase):
    def test_public_pages_exist(self):
        for page in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html", "privacidad.html"):
            with self.subTest(page=page):
                self.assertTrue((PUBLIC / page).is_file())

    def test_primary_conversion_is_whatsapp(self):
        for page in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html"):
            with self.subTest(page=page):
                self.assertIn("https://wa.me/595971141032", html(page))
```

- [ ] **Step 4: Document the verification command**

Agregar a `README.md`:

````markdown
## Verificación

```powershell
python -m unittest discover -s tests -v
python -m http.server 4173 --directory public
```

La revisión responsive se realiza en 320, 360, 390, 430, 768, 1024, 1280 y 1440 px.
````

- [ ] **Step 5: Commit the test harness**

```powershell
git add tests README.md
git commit -m "test: add static site contract checks"
```

---

### Task 2: Consolidate the visual foundation and shared shell

**Files:**
- Modify: `public/assets/css/styles.css`
- Modify: `public/assets/js/main.js`
- Modify: `public/index.html`
- Modify: `public/servicios.html`
- Modify: `public/casos.html`
- Modify: `public/tecnologias.html`
- Modify: `public/contacto.html`
- Modify: `public/privacidad.html`
- Modify: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: fuentes locales existentes y `assets/img/jesareko-logo.svg`.
- Produces: `.site-header`, `.site-nav`, `.nav-menu`, `.nav-toggle`, `.site-footer`, `.btn`, `.btn--primary`, `.brand-lockup` y tokens CSS compartidos.

- [ ] **Step 1: Add failing shared-shell assertions**

Agregar a `SiteContractTests`:

```python
    def test_every_page_uses_new_shared_shell(self):
        for page in PAGES:
            source = (PUBLIC / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertIn('class="site-nav"', source)
                self.assertIn('class="brand-lockup"', source)
                self.assertIn('class="site-footer"', source)
                self.assertIn('aria-controls="primaryMenu"', source)

    def test_whatsapp_uses_symbol_not_emoji(self):
        for page in PAGES:
            source = (PUBLIC / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertNotIn("📱", source)
                self.assertNotIn("☎", source)
                if "wa.me/" in source:
                    self.assertIn('href="#icon-whatsapp"', source)
```

- [ ] **Step 2: Run the shell tests and verify failure**

Run:

```powershell
python -m unittest tests.test_site_contract.SiteContractTests.test_every_page_uses_new_shared_shell tests.test_site_contract.SiteContractTests.test_whatsapp_uses_symbol_not_emoji -v
```

Expected: FAIL porque las páginas aún usan el shell anterior.

- [ ] **Step 3: Replace the CSS foundation**

Reemplazar `styles.css` completo. Comenzar con estos tokens exactos y construir componentes una sola vez, sin bloques de sobrescritura al final:

```css
:root {
  --color-ink: #0e1f16;
  --color-ink-soft: #415148;
  --color-brand: #0f6b3f;
  --color-brand-dark: #0a4529;
  --color-brand-soft: #e3f0e8;
  --color-paper: #ffffff;
  --color-canvas: #f3f5f2;
  --color-line: #d7ded8;
  --color-whatsapp: #25d366;
  --radius-sm: 10px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --space-1: .5rem;
  --space-2: 1rem;
  --space-3: 1.5rem;
  --space-4: 2rem;
  --space-5: clamp(3rem, 8vw, 7rem);
  --container: 74rem;
}

img, svg { display: block; max-width: 100%; }
.container { width: min(calc(100% - 2rem), var(--container)); margin-inline: auto; }
.btn { min-height: 48px; border-radius: var(--radius-md); }
.editorial-grid { display: grid; grid-template-columns: minmax(0, 1.08fr) minmax(0, .92fr); }
@media (max-width: 52rem) { .editorial-grid { grid-template-columns: minmax(0, 1fr); } }
```

Prohibir en el nuevo archivo correcciones con margen negativo, `overflow-x: hidden` usado para ocultar errores y alturas fijas para contenido textual.

- [ ] **Step 4: Replace the shared header and footer markup**

Usar en las seis páginas el mismo encabezado base:

```html
<header class="site-header" id="siteHeader">
  <nav class="site-nav container" aria-label="Navegación principal">
    <a class="brand-lockup" href="/" aria-label="Jesareko, inicio">
      <img src="assets/img/jesareko-logo.svg" alt="" width="32" height="32">
      <span>Jesareko</span>
    </a>
    <button class="nav-toggle" id="navToggle" type="button" aria-label="Abrir menú" aria-controls="primaryMenu" aria-expanded="false">
      <span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>
    </button>
    <div class="nav-menu" id="primaryMenu">
      <a href="/servicios">Servicios</a><a href="/casos">Casos</a><a href="/tecnologias">Tecnologías</a><a href="/contacto">Contacto</a>
      <a class="btn btn--primary" href="https://wa.me/595971141032" target="_blank" rel="noopener noreferrer">
        <svg class="icon" aria-hidden="true"><use href="#icon-whatsapp"></use></svg><span>Solicitar diagnóstico</span>
      </a>
    </div>
  </nav>
</header>
```

Conservar en cada página el `symbol#icon-whatsapp` actual y ajustar el footer a cuatro grupos: marca, navegación, servicios y contacto/legal.

- [ ] **Step 5: Make mobile navigation deterministic**

En `main.js`, mantener una única fuente de verdad:

```javascript
function setMenuOpen(open) {
  navToggle?.classList.toggle("is-open", open);
  primaryMenu?.classList.toggle("is-open", open);
  navToggle?.setAttribute("aria-expanded", String(open));
  navToggle?.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
}

navToggle?.addEventListener("click", () => {
  setMenuOpen(navToggle.getAttribute("aria-expanded") !== "true");
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setMenuOpen(false);
});
```

El CSS mobile debe insertar `.nav-menu.is-open` en el flujo del header; no debe superponer el hero.

- [ ] **Step 6: Run the shared-shell tests**

```powershell
python -m unittest tests.test_site_contract -v
```

Expected: PASS.

- [ ] **Step 7: Commit the foundation**

```powershell
git add public/assets/css/styles.css public/assets/js/main.js public/*.html tests/test_site_contract.py
git commit -m "feat: establish editorial responsive shell"
```

---

### Task 3: Rebuild the homepage conversion flow

**Files:**
- Modify: `public/index.html`
- Modify: `tests/test_content_contract.py`

**Interfaces:**
- Consumes: shell y componentes de Task 2.
- Produces: secciones `#hero`, `#areas`, `#evidence`, `#process`, `#cases` y `#diagnostic`.

- [ ] **Step 1: Add the failing homepage contract**

Agregar a `ContentContractTests`:

```python
    def test_homepage_follows_approved_narrative(self):
        source = html("index.html")
        positions = [source.index(f'id="{section}"') for section in ("hero", "areas", "evidence", "process", "cases", "diagnostic")]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(source.count('class="service-row__item"'), 3)
        self.assertIn("Infraestructura clara. Sistemas que funcionan.", source)
        self.assertIn("Encarnación", source)
```

- [ ] **Step 2: Run the homepage test and verify failure**

```powershell
python -m unittest tests.test_content_contract.ContentContractTests.test_homepage_follows_approved_narrative -v
```

Expected: FAIL porque las nuevas secciones todavía no existen.

- [ ] **Step 3: Replace the homepage main content**

Reescribir `<main>` con esta jerarquía exacta:

```html
<main id="mainContent">
  <section class="hero editorial-grid" id="hero">
    <div class="hero__copy"><p class="eyebrow">Encarnación · Itapúa</p><h1>Infraestructura clara. Sistemas que funcionan.</h1><p>Redes, videovigilancia y soporte técnico con diagnóstico previo y entrega documentada.</p><a class="btn btn--primary" href="https://wa.me/595971141032" target="_blank" rel="noopener noreferrer"><svg class="icon" aria-hidden="true"><use href="#icon-whatsapp"></use></svg><span>Solicitar diagnóstico</span></a></div>
    <figure class="hero__media"><img src="assets/img/brands/dahua-video-surveillance.webp" alt="Sistema de videovigilancia Dahua" width="1200" height="900"></figure>
  </section>
  <section class="service-row" id="areas">
    <a class="service-row__item" href="/servicios#redes"><span>01</span><h2>Redes y WiFi</h2></a>
    <a class="service-row__item" href="/servicios#seguridad"><span>02</span><h2>Seguridad física</h2></a>
    <a class="service-row__item" href="/servicios#soporte"><span>03</span><h2>Soporte técnico</h2></a>
  </section>
  <section class="technology-proof" id="evidence"><div><p class="eyebrow">Tecnología aplicada</p><h2>Equipos adecuados para cada entorno.</h2><p>Seleccionamos por cobertura, uso y mantenimiento.</p></div><div class="brand-list"><span>Hikvision</span><span>Dahua</span></div></section>
  <section class="process-section" id="process"><p class="eyebrow">Proceso</p><h2>Del diagnóstico a una entrega que se puede mantener.</h2><ol class="process-list"><li>Diagnóstico</li><li>Propuesta</li><li>Instalación</li><li>Entrega documentada</li></ol></section>
  <section class="case-preview" id="cases"><p class="eyebrow">Aplicaciones frecuentes</p><h2>Problemas técnicos reconocibles.</h2><div class="case-preview__grid"><article><h3>Comercio con puntos ciegos</h3></article><article><h3>Vivienda con WiFi inestable</h3></article><article><h3>Oficina sin documentación técnica</h3></article></div><a href="/casos">Ver aplicaciones</a></section>
  <section class="diagnostic-cta" id="diagnostic"><h2>Empecemos por revisar el lugar.</h2><p>Contanos qué está fallando o qué necesitás instalar.</p><a class="btn btn--primary" href="https://wa.me/595971141032" target="_blank" rel="noopener noreferrer"><svg class="icon" aria-hidden="true"><use href="#icon-whatsapp"></use></svg><span>Hablar por WhatsApp</span></a></section>
</main>
```

Usar el titular aprobado, un único párrafo de hasta 32 palabras y un CTA primario. Convertir las seis tarjetas de problemas en tres situaciones concretas dentro de Casos. Eliminar chips, dashboard, métricas decorativas e iconos vacíos.

- [ ] **Step 4: Run homepage and full contract tests**

```powershell
python -m unittest tests.test_content_contract.ContentContractTests.test_homepage_follows_approved_narrative -v
python -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 5: Commit the homepage**

```powershell
git add public/index.html tests/test_content_contract.py
git commit -m "feat: rebuild homepage editorial journey"
```

---

### Task 4: Rebuild Services around customer needs

**Files:**
- Modify: `public/servicios.html`
- Modify: `tests/test_content_contract.py`

**Interfaces:**
- Consumes: `.editorial-grid`, `.section-heading`, `.service-detail` y `.diagnostic-cta`.
- Produces: `#redes`, `#seguridad`, `#soporte` y enlaces contextuales a Contacto.

- [ ] **Step 1: Add the failing services contract**

```python
    def test_services_has_three_decision_paths(self):
        source = html("servicios.html")
        for section in ("redes", "seguridad", "soporte"):
            self.assertIn(f'id="{section}"', source)
        self.assertNotIn("Incluye:</strong>", source)
        self.assertNotIn("Conviene cuando:</strong>", source)
        self.assertNotIn("Resultado:</strong>", source)
```

- [ ] **Step 2: Run and verify failure**

```powershell
python -m unittest tests.test_content_contract.ContentContractTests.test_services_has_three_decision_paths -v
```

Expected: FAIL por la estructura y fórmula de contenido existentes.

- [ ] **Step 3: Recompose the services page**

Crear un índice inicial de tres rutas. Cada sección debe contener: titular orientado a problema, resumen de 20–35 palabras, máximo cuatro capacidades, una nota de criterio técnico y un enlace «Consultar este servicio». Mover web/automatización a una nota secundaria dentro de Soporte; no mostrarla como cuarto pilar equivalente.

Usar esta anatomía repetible:

```html
<section class="service-detail editorial-grid" id="redes">
  <div class="service-detail__intro"><span class="section-index">01</span><h2>Redes y WiFi</h2><p>Revisamos cobertura, cableado y capacidad para que la red responda al uso real del lugar.</p></div>
  <div class="service-detail__scope"><h3>Qué revisamos</h3><ul><li>Cobertura y zonas muertas</li><li>Saturación y estabilidad</li><li>Puntos de acceso y cableado</li><li>Red de invitados</li></ul><a href="/contacto?servicio=redes">Consultar este servicio</a></div>
</section>
```

- [ ] **Step 4: Run services and full tests**

```powershell
python -m unittest tests.test_content_contract.ContentContractTests.test_services_has_three_decision_paths -v
python -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 5: Commit Services**

```powershell
git add public/servicios.html tests/test_content_contract.py
git commit -m "feat: simplify service decision paths"
```

---

### Task 5: Reframe Cases without invented proof

**Files:**
- Modify: `public/casos.html`
- Modify: `tests/test_content_contract.py`

**Interfaces:**
- Consumes: `.case-study`, `.case-study__media`, `.case-study__body`.
- Produces: tres aplicaciones frecuentes con situación, criterio e intervención, etiquetadas sin fingir proyectos ejecutados.

- [ ] **Step 1: Add the failing cases contract**

```python
    def test_cases_are_honestly_labeled(self):
        source = html("casos.html")
        self.assertIn("Aplicaciones frecuentes", source)
        self.assertGreaterEqual(source.count('class="case-study"'), 3)
        for label in ("Situación", "Criterio", "Intervención"):
            self.assertIn(label, source)
```

- [ ] **Step 2: Run and verify failure**

```powershell
python -m unittest tests.test_content_contract.ContentContractTests.test_cases_are_honestly_labeled -v
```

Expected: FAIL por ausencia de la nueva anatomía.

- [ ] **Step 3: Rebuild Cases**

Crear tres aplicaciones frecuentes: comercio con puntos ciegos, vivienda con WiFi inestable y oficina con accesos/documentación dispersos. Etiquetarlas como escenarios de trabajo hasta contar con evidencia propia. No incluir porcentajes, clientes, fechas o resultados cuantificados no verificables.

- [ ] **Step 4: Run tests**

```powershell
python -m unittest tests.test_content_contract.ContentContractTests.test_cases_are_honestly_labeled -v
python -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 5: Commit Cases**

```powershell
git add public/casos.html tests/test_content_contract.py
git commit -m "feat: present honest technical scenarios"
```

---

### Task 6: Source and integrate official technology imagery

**Files:**
- Modify: `public/tecnologias.html`
- Modify: `public/assets/img/brands/*`
- Modify: `docs/image-sources.json`
- Modify: `tests/test_site_contract.py`
- Modify: `tests/test_content_contract.py`

**Interfaces:**
- Consumes: páginas oficiales de Hikvision y Dahua y archivos existentes en `public/assets/img/brands/`.
- Produces: `.product-editorial`, imágenes WebP/PNG optimizadas y registro de fuentes completo.

- [ ] **Step 1: Add failing asset-source tests**

Agregar a `tests/test_site_contract.py`:

```python
import json

    def test_every_brand_image_has_a_source_record(self):
        registry = json.loads((ROOT / "docs" / "image-sources.json").read_text(encoding="utf-8"))
        registered = {item["local_file"] for item in registry["images"]}
        used = set()
        for page in PAGES:
            for image in parse_page(page).images:
                src = image.get("src", "")
                if "assets/img/brands/" in src:
                    used.add(src)
        self.assertTrue(used.issubset(registered))
```

Normalizar `docs/image-sources.json` a esta interfaz:

```json
{
  "images": [
    {
      "local_file": "assets/img/brands/dahua-video-surveillance.webp",
      "brand": "Dahua",
      "product": "Video surveillance product",
      "source_url": "https://www.dahuasecurity.com/",
      "usage_basis": "Official manufacturer product media",
      "retrieved_on": "2026-07-26"
    }
  ]
}
```

- [ ] **Step 2: Run and verify failure**

```powershell
python -m unittest tests.test_site_contract.SiteContractTests.test_every_brand_image_has_a_source_record -v
```

Expected: FAIL hasta normalizar el registro y referencias.

- [ ] **Step 3: Select assets from official sources**

Buscar únicamente en dominios oficiales de Hikvision y Dahua. Elegir entre 4 y 6 imágenes con fondo limpio, mínimo 1200 px en su lado mayor y correspondencia directa con cámaras, acceso o alarmas mostradas. Registrar la URL exacta, no la página principal cuando exista una ficha específica.

- [ ] **Step 4: Optimize and store assets**

Conservar transparencia cuando el fabricante la ofrezca. Para fotografías, convertir a WebP con calidad visual 82–88; para logos, preferir SVG oficial. No ampliar imágenes pequeñas. Mantener nombres descriptivos en minúsculas y con guiones.

- [ ] **Step 5: Rebuild Technologies**

Agrupar la página por aplicación, no por una cuadrícula uniforme de productos. Usar cada imagen dentro de:

```html
<article class="product-editorial editorial-grid">
  <figure class="product-editorial__media"><img src="assets/img/brands/hikvision-cctv-cameras.webp" alt="Cámaras de videovigilancia Hikvision" width="1200" height="900"></figure>
  <div class="product-editorial__copy"><span class="brand-wordmark">Hikvision</span><h2>Videovigilancia para cobertura útil.</h2><p>Seleccionamos cámaras, grabación y acceso remoto según los puntos que realmente necesitan control.</p></div>
</article>
```

- [ ] **Step 6: Run asset and full tests**

```powershell
python -m unittest tests.test_site_contract.SiteContractTests.test_every_brand_image_has_a_source_record -v
python -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 7: Commit technology assets**

```powershell
git add public/tecnologias.html public/assets/img/brands docs/image-sources.json tests
git commit -m "feat: add sourced technology showcase"
```

---

### Task 7: Rebuild Contact and harden interactive states

**Files:**
- Modify: `public/contacto.html`
- Modify: `public/assets/js/main.js`
- Modify: `tests/test_content_contract.py`

**Interfaces:**
- Consumes: `WHATSAPP_NUMBER`, `FIELD_LIMITS`, `ALLOWED_SERVICES` y shell de navegación.
- Produces: formulario `#contactForm`, acciones `#sendWhatsApp` y `#sendEmail`, mensajes en `#formStatus` y soporte de `?servicio=`.

- [ ] **Step 1: Add the failing contact contract**

```python
    def test_contact_prioritizes_whatsapp_and_has_accessible_errors(self):
        source = html("contacto.html")
        self.assertLess(source.index('id="sendWhatsApp"'), source.index('id="sendEmail"'))
        for field in ("name", "city", "service", "message"):
            self.assertIn(f'data-error-for="{field}"', source)
        self.assertIn('role="status"', source)
        self.assertIn('aria-live="polite"', source)
```

- [ ] **Step 2: Run and verify failure**

```powershell
python -m unittest tests.test_content_contract.ContentContractTests.test_contact_prioritizes_whatsapp_and_has_accessible_errors -v
```

Expected: FAIL si el nuevo orden o estado accesible no existe.

- [ ] **Step 3: Recompose Contact**

Colocar primero un panel breve con número visible y CTA de WhatsApp. Mantener el formulario como alternativa y reducirlo a nombre, empresa opcional, ciudad, servicio y mensaje. Usar etiquetas persistentes y conservar el selector nativo como fallback.

- [ ] **Step 4: Harden the script**

Mantener validación y normalización existentes. Añadir selección inicial segura desde query string:

```javascript
const requestedService = new URLSearchParams(window.location.search).get("servicio");
if (requestedService && ALLOWED_SERVICES.has(requestedService)) {
  serviceSelect.value = requestedService;
  updateServicePicker(requestedService);
}
```

Al validar, usar `aria-invalid="true"` y `aria-describedby` sobre el control real; retirar ambos atributos cuando el campo se corrija. No borrar valores después de abrir WhatsApp o correo.

- [ ] **Step 5: Run contact and full tests**

```powershell
python -m unittest tests.test_content_contract.ContentContractTests.test_contact_prioritizes_whatsapp_and_has_accessible_errors -v
python -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 6: Commit Contact**

```powershell
git add public/contacto.html public/assets/js/main.js tests/test_content_contract.py
git commit -m "feat: prioritize accessible whatsapp contact"
```

---

### Task 8: Apply the shell to Privacy and finish responsive/accessibility QA

**Files:**
- Modify: `public/privacidad.html`
- Modify: `public/assets/css/styles.css`
- Modify: `public/assets/js/main.js`
- Modify: `README.md`
- Modify: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: sitio completo de Tasks 2–7.
- Produces: entrega validada sin overflow, recursos fallidos ni regresiones de teclado.

- [ ] **Step 1: Add final CSS-regression assertions**

Agregar a `SiteContractTests`:

```python
    def test_css_does_not_mask_layout_failures(self):
        css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        self.assertNotIn("overflow-x: hidden", css)
        self.assertNotIn("margin-left: -", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        for token in ("--radius-sm: 10px", "--radius-md: 14px", "--radius-lg: 20px"):
            self.assertIn(token, css)

    def test_local_asset_references_exist(self):
        for page in PAGES:
            for image in parse_page(page).images:
                src = image.get("src", "")
                if src and not src.startswith(("http://", "https://", "data:")):
                    self.assertTrue((PUBLIC / src).is_file(), f"{page}: missing {src}")
```

- [ ] **Step 2: Run full tests before final fixes**

```powershell
python -m unittest discover -s tests -v
```

Expected: FAIL si queda una regla antigua, dimensión ausente o activo roto.

- [ ] **Step 3: Finish Privacy and CSS cleanup**

Aplicar encabezado/footer compartidos a Privacidad. Corregir únicamente los fallos reportados. Confirmar que `styles.css` contiene una sola definición canónica por componente y que todos los media queries están agrupados por comportamiento.

- [ ] **Step 4: Run the complete automated suite**

```powershell
python -m unittest discover -s tests -v
python -m compileall tests
git diff --check
```

Expected: todos los tests PASS, compilación Python correcta y `git diff --check` sin salida.

- [ ] **Step 5: Start the local site for browser QA**

```powershell
python -m http.server 4173 --directory public
```

Abrir `http://127.0.0.1:4173/` y revisar las seis páginas.

- [ ] **Step 6: Verify each viewport and page**

Para cada ancho 320, 360, 390, 430, 768, 1024, 1280 y 1440 px, comprobar en Inicio, Servicios, Casos, Tecnologías, Contacto y Privacidad:

```javascript
({
  viewport: window.innerWidth,
  overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  imagesIncomplete: [...document.images].filter((image) => !image.complete || image.naturalWidth === 0).map((image) => image.src),
  duplicateIds: [...document.querySelectorAll("[id]")].map((node) => node.id).filter((id, index, ids) => ids.indexOf(id) !== index)
})
```

Expected: `overflow` igual a `0`, `imagesIncomplete` vacío y `duplicateIds` vacío.

- [ ] **Step 7: Verify interactions and accessibility**

En 320 y 1440 px: abrir/cerrar menú, cerrar con Escape, recorrer la página con Tab, activar WhatsApp sin enviar datos, probar formulario vacío y válido, confirmar foco visible, activar reducción de movimiento y revisar consola.

Expected: sin superposición, pérdida de foco, controles inaccesibles, errores de consola ni recursos 404.

- [ ] **Step 8: Capture final comparison screenshots**

Guardar capturas completas de Inicio, Tecnologías y Contacto en 390 y 1440 px dentro de `work/qa/` para revisión; no versionar esas capturas.

- [ ] **Step 9: Commit the validated redesign**

```powershell
git add public README.md tests docs/image-sources.json
git commit -m "feat: complete responsive editorial redesign"
```

---

## Deployment Gate

La implementación termina con el sitio validado localmente. Publicar en Cloudflare Pages es una acción separada: antes de ejecutar `wrangler pages deploy public`, confirmar con el usuario el proyecto y el entorno de destino. Tras publicar, repetir en `https://jesareko.com/` la comprobación de overflow, recursos, navegación, formulario y WhatsApp.
