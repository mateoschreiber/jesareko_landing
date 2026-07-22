# README de seguridad

## Que se endurecio
- Se preparó una Content Security Policy restrictiva para producción, compatible con los recursos locales y Cloudflare Web Analytics.
- Se agregaron headers recomendados: CSP, HSTS, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `Cross-Origin-Opener-Policy: same-origin` y `Cross-Origin-Resource-Policy`.
- Se eliminaron estilos inline para evitar `unsafe-inline` en estilos y se retiró `navigate-to`, directiva no soportada por navegadores actuales.
- El formulario sigue siendo estatico, pero ahora normaliza texto, elimina caracteres de control, limita longitudes y construye WhatsApp/mailto con `encodeURIComponent`.
- CSS y JavaScript tienen una sola fuente de verdad; la compresion se delega al CDN.
- Las configuraciones alternativas de Nginx y Apache fuerzan HTTPS, limitan TLS a 1.2/1.3 y devuelven `404` para rutas inexistentes.
- Se agregaron archivos de despliegue para Cloudflare Pages/Netlify, Nginx y Apache.
- Se agregaron `robots.txt`, `sitemap.xml` y `.gitignore`.

## Que no es posible en una web estatica
- El codigo HTML, CSS y JavaScript no puede ocultarse al 100%. Todo frontend enviado al navegador puede inspeccionarse.
- La minificacion reduce exposicion casual y peso, pero no impide que alguien lea o copie el codigo.
- Sin backend no se pueden guardar formularios, aplicar validaciones server-side ni proteger secretos.
- No se deben poner tokens, claves API, credenciales, datos privados ni endpoints sensibles en HTML o JS.

## Despliegue con Cloudflare Pages
1. Subir el repositorio a GitHub.
2. Crear un proyecto en Cloudflare Pages conectado al repo.
3. Configurar sin build command y con directorio de salida `/public`.
4. Las cabeceras se leen directamente desde `public/_headers`.
5. Configurar el dominio propio.
6. Activar HTTPS y revisar que la landing cargue sin errores CSP en DevTools.
7. Verificar `https://jesareko.com/`, WhatsApp, email, GitHub y la imagen Open Graph antes de publicar.

## Despliegue detras de Cloudflare con hosting propio
1. Servir el sitio con Nginx o Apache usando los ejemplos de `/deploy`.
2. Activar proxy naranja en Cloudflare.
3. Usar SSL/TLS `Full (strict)` con certificado valido en origen.
4. En el firewall del servidor, permitir trafico 80/443 solo desde rangos IP oficiales de Cloudflare.
5. Desactivar directory listing y bloquear archivos ocultos o extensiones sensibles.
6. Revisar logs del servidor y Security Events de Cloudflare despues de publicar.

## Checklist anti-DDoS
- Proxy naranja activo.
- SSL/TLS en `Full` o `Full (strict)`.
- `Always Use HTTPS` activo.
- `Brotli` activo.
- Cache Rules para `/assets/*`.
- WAF Managed Rules activo si el plan lo permite.
- Bot Fight Mode o equivalente activo si esta disponible.
- Security Level en `Medium`; subir a `High` ante abuso.
- Under Attack Mode solo durante ataques.
- Rate limiting preparado para futuras rutas sensibles.
- Reglas de challenge para exceso de requests a `/` o `/assets/*` solo si los logs lo justifican.

## Checklist antes de publicar
- Confirmar `https://jesareko.com/` o el dominio definitivo de Jesareko como dominio activo.
- Confirmar `595971141032` como numero de WhatsApp.
- Confirmar `alemateo07@gmail.com` como correo de contacto.
- Cambiar `https://github.com/tuusuario`.
- Agregar `assets/img/og-image.jpg` o ajustar `og:image`.
- Verificar que no haya `.env`, logs, backups o archivos internos publicados.
- Probar formulario por WhatsApp y correo.
- Probar headers con una herramienta de analisis de seguridad.
- Revisar consola del navegador por errores CSP.

## Formularios y datos reales
Si en el futuro se procesan datos reales, usar un backend propio o un proveedor externo seguro con HTTPS, validacion server-side, rate limiting, proteccion anti-spam, politicas de privacidad y manejo adecuado de datos privados.

## Fuentes oficiales
- Cloudflare DDoS Protection docs: https://developers.cloudflare.com/ddos-protection/
- OWASP HTTP Security Response Headers Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
- MDN Content Security Policy: https://developer.mozilla.org/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
