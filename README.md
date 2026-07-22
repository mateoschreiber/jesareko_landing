# Jesareko

Landing estática para Jesareko, servicios de redes WiFi, CCTV, alarmas, control de acceso, detección de incendio y soporte técnico en Encarnación, Itapúa, Paraguay.

Sitio: <https://jesareko.com/>

## Características

- HTML, CSS y JavaScript sin proceso de compilación.
- Diseño responsive, navegación accesible y menú móvil.
- Formulario que prepara consultas para WhatsApp o correo sin almacenar datos.
- SEO local: metadatos, canonical, Open Graph, JSON-LD, `robots.txt` y sitemap.
- Fuentes e imágenes servidas localmente.
- Cabeceras de seguridad para Cloudflare Pages en `public/_headers`.

## Estructura

```text
public/                 Sitio publicado
  assets/               CSS, JavaScript, fuentes e imágenes
docs/                   Referencias y procedencia de activos
deploy/                 Configuraciones de servidor alternativas
docs/image-sources.json Registro de imágenes de referencia
README_SEGURIDAD.md     Controles y checklist de seguridad
wrangler.jsonc          Configuración de Cloudflare Pages
```

Solo el contenido de `public/` se publica.

## Desarrollo local

No se requieren dependencias. Desde la raíz:

```powershell
python -m http.server 4173 --directory public
```

Abrir <http://localhost:4173/>.

## Verificación

```powershell
node --check public/assets/js/main.js
curl.exe -sSI https://jesareko.com/
```

Antes de publicar, comprobar navegación, formulario, enlaces de WhatsApp/correo, vista móvil y consola del navegador.

## Despliegue

### Cloudflare Pages

- Build command: vacío.
- Output directory: `public`.
- Configurar el dominio `jesareko.com` y HTTPS.
- Activar `Always Use HTTPS` y SSL/TLS `Full (strict)`.

Las cabeceras se aplican desde `public/_headers`. Las recomendaciones de Cloudflare, Nginx y Apache están en [deploy](deploy/).

## Configuración de contenido

Antes de una publicación comercial, revisar:

- Número de WhatsApp y correo en `public/assets/js/main.js`.
- Dominio, canonical, sitemap y metadatos sociales.
- Imagen Open Graph rasterizada.
- Derechos y procedencia de imágenes en `docs/image-sources.json`.

## Seguridad y privacidad

El frontend no contiene secretos y no procesa formularios en un servidor. Las consultas se abren en WhatsApp o en el cliente de correo del visitante. Consultar [README_SEGURIDAD.md](README_SEGURIDAD.md) antes de modificar cabeceras, formularios o el despliegue.

## Licencia

Todos los derechos reservados. No se autoriza la redistribución ni el uso comercial del contenido, marca o activos sin permiso expreso de Jesareko.
