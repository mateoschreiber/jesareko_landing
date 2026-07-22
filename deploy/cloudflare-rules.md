# Cloudflare: reglas recomendadas para despliegue estatico

## DNS y TLS
- Activar el proxy naranja para el registro del dominio que sirve la landing.
- Usar SSL/TLS en `Full` o `Full (strict)`. Preferir `Full (strict)` si el hosting de origen tiene certificado valido.
- Activar `Always Use HTTPS`.
- Activar `Automatic HTTPS Rewrites`.
- No exponer la IP de origen si se usa hosting propio. Si hay servidor propio, permitir trafico HTTP/HTTPS solo desde rangos IP oficiales de Cloudflare a nivel firewall.
- Consolidar el host principal con un Bulk Redirect permanente:
  - Origen: `www.jesareko.com`
  - Destino: `https://jesareko.com`
  - Estado: `301`
  - Activar `Preserve query string`, `Subpath matching` y `Preserve path suffix`.
- Verificar que `http://www.jesareko.com/*` también termine en `https://jesareko.com/*` sin cadenas de redirección.

## Rendimiento seguro
- Activar `Brotli`.
- Activar `Auto Minify` para HTML, CSS y JS si esta disponible en el plan.
- Crear Cache Rules:
  - `/assets/*`: cache publico de 1 dia mientras los archivos mantengan nombres estables.
  - `/`, `/servicios`, `/casos`, `/tecnologias`, `/contacto`, `/privacidad`, `/robots.txt`, `/sitemap.xml`: cache corto, por ejemplo 5 a 60 minutos.
- Purgar cache despues de cambiar HTML, CSS, JS, `robots.txt` o `sitemap.xml`.

## SEO tecnico
- Mantener `assets.html_handling` en `drop-trailing-slash` para que las rutas canonicas sean `/servicios`, `/casos`, `/tecnologias`, `/contacto` y `/privacidad`.
- No publicar canónicas, enlaces internos ni URLs del sitemap con extensión `.html`.
- Después de desplegar, comprobar que las rutas `.html` respondan con redirección permanente y que el host `www` no entregue contenido con estado `200`.

## WAF y antiabuso
- Activar WAF Managed Rules si el plan lo permite.
- Activar Bot Fight Mode o una proteccion equivalente si esta disponible.
- Usar Security Level `Medium` como base. Subir a `High` si hay trafico sospechoso persistente.
- Usar `Under Attack Mode` solo durante ataques o picos claramente maliciosos, porque agrega friccion a usuarios reales.
- No bloquear paises por defecto. Hacerlo solo si hay evidencia operativa de abuso concentrado y no afecta clientes reales.

## Rate limiting y challenges
- Si la landing no tiene backend, no hay rutas sensibles reales. Si en el futuro se agregan endpoints como `/api`, `/login`, `/admin` o formularios server-side, aplicar rate limiting especifico.
- Regla sugerida de challenge para abuso de la home:
  - Condicion: `http.request.uri.path eq "/"` y volumen alto desde la misma IP o AS.
  - Accion: Managed Challenge.
  - Usar umbrales conservadores para no afectar visitantes reales.
- Regla sugerida para abuso de assets:
  - Condicion: `starts_with(http.request.uri.path, "/assets/")` y tasa anormalmente alta.
  - Accion: JS Challenge o Managed Challenge solo si hay scraping/abuso claro.
- Crear reglas separadas para bloquear user agents vacios o evidentemente automatizados solo si aparecen en logs.

## Observabilidad
- Revisar Security Events despues de publicar.
- Monitorear picos por pais, ASN, user agent y path.
- Mantener una regla temporal documentada para modo ataque y retirarla cuando el trafico vuelva a la normalidad.
