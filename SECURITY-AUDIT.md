# Security Audit

Fecha: 2026-09-12

## 1. Resumen ejecutivo

Riesgo global: **MEDIO**

Hallazgos:

| Severidad | Cantidad |
| --- | ---: |
| Critica | 0 |
| Alta | 0 |
| Media | 2 |
| Baja | 0 |
| Informativa | 2 |

El proyecto es una landing estatica sin backend propio, sin dependencias de aplicacion, sin lockfile, sin formularios server-side, sin autenticacion y sin APIs privadas visibles en el repositorio. La postura de frontend es buena: CSP restrictiva, recursos locales, `target="_blank"` con `rel="noopener noreferrer"`, validacion/normalizacion cliente y ausencia de sinks DOM peligrosos como `innerHTML`, `eval` o `document.write` en el codigo productivo.

Los riesgos principales no son de explotacion remota clasica, sino de privacidad/proteccion de datos, procedencia de activos publicados y verificabilidad operativa del despliegue.

## 2. Alcance

Incluido:

- Codigo y configuracion bajo `C:\Users\MaSch\Documents\jesareko_landing\jesareko_landing`.
- `public/`, `deploy/`, `docs/`, `scripts/`, `tests/`, `README.md`, `README_SEGURIDAD.md`, `wrangler.jsonc`, `.gitignore`, `.gitattributes`.
- Analisis estatico de HTML, CSS, JavaScript, configuracion Cloudflare/servidores alternativos y datos de procedencia.
- Busqueda dirigida de secretos, credenciales, archivos sensibles, endpoints, dependencias y CI/CD.

Excluido por instruccion:

- Modificacion de codigo.
- Pruebas destructivas.
- Ataques a servicios externos.
- Navegador, Chromium, DevTools, Playwright, screenshots y Lighthouse.
- Validacion runtime de headers sobre `https://jesareko.com/`.

## 3. Metodologia

- Reconocimiento de estructura con busquedas dirigidas.
- Modelo de amenazas ligero antes de clasificar hallazgos.
- Revision OWASP Top 10:2025 solo para categorias aplicables.
- Mapeo razonable contra OWASP ASVS 5.0.0 sin tratar esto como certificacion ASVS.
- Revision de secretos y archivos sensibles por patrones.
- Revision de frontend security, deployment, Cloudflare, supply chain, privacidad y Git.
- Evidencia por archivo y linea.

Fuentes oficiales usadas:

- OWASP Top 10:2025: https://top10.owasp.org/2025/
- OWASP Top 10:2025 A01 Broken Access Control: https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/
- OWASP ASVS 5.0.0: https://github.com/OWASP/ASVS/tree/v5.0.0
- Cloudflare Pages custom headers: https://developers.cloudflare.com/pages/configuration/headers/
- Cloudflare Workers Static Assets headers: https://developers.cloudflare.com/workers/static-assets/headers/

## 4. Arquitectura y superficie de ataque

Tipo de aplicacion: landing estatica.

Stack observado:

- HTML/CSS/JavaScript sin proceso de compilacion (`README.md:9`).
- Sin `package.json`, lockfile, `requirements.txt`, `pyproject.toml` ni manifiestos equivalentes.
- Deploy previsto en Cloudflare Pages/Workers Static Assets con `wrangler.jsonc`.
- Directorio publicado: `public/` (`README.md:28`, `wrangler.jsonc:8-10`).
- Unico JS productivo: `public/assets/js/main.js`.
- Formulario cliente en `public/contacto.html:93-143`.

Superficie publica:

- Rutas HTML: `/`, `/servicios`, `/casos`, `/tecnologias`, `/contacto`, `/privacidad`.
- Assets estaticos bajo `/assets/`.
- Contacto por WhatsApp y correo.
- No se detectaron directorios `functions/`, `_worker.js`, `.github/workflows`, `/api`, `/admin`, login, sesiones ni cookies propias.

Controles positivos observados:

- CSP restrictiva sin `unsafe-inline` ni `unsafe-eval` (`public/_headers:3`).
- HSTS, `nosniff`, anti-clickjacking, `Referrer-Policy`, `Permissions-Policy`, COOP/CORP (`public/_headers:4-13`).
- Redirecciones canonicas simples sin destino controlado por usuario (`public/_redirects:1-6`).
- Recursos externos limitados a navegacion voluntaria hacia WhatsApp y `mailto`.
- `.gitignore` excluye `.env`, `.dev.vars`, `.wrangler`, `node_modules`, logs, temporales y estado local de Codex (`.gitignore:1-34`).

## 5. Modelo de amenazas resumido

Activos:

- Datos personales y de contexto tecnico ingresados en contacto: nombre, empresa, ciudad, servicio y mensaje.
- Informacion potencialmente sensible sobre infraestructura fisica: CCTV, alarmas, accesos, incendio, redes y soporte.
- Reputacion/marca y continuidad de publicacion.
- Configuracion de seguridad de despliegue.

Entradas controladas por usuario:

- Campos del formulario (`public/contacto.html:101-132`).
- Query parameter `servicio` en `/contacto` (`public/assets/js/main.js:215-217`).
- Navegacion a rutas publicas.

Trust boundaries:

- Navegador del visitante -> JavaScript local.
- Sitio -> WhatsApp/Meta mediante `https://wa.me/...?...`.
- Sitio -> cliente de correo mediante `mailto:`.
- Repositorio -> Cloudflare/static hosting.
- Repositorio -> activos de terceros incluidos localmente.

No aplican en el codigo actual:

- Autenticacion.
- Autorizacion server-side.
- Base de datos.
- APIs.
- Cookies/sesiones.
- SSRF.
- File uploads.
- Ejecucion de comandos.

## 6. Hallazgos criticos y altos

No se identificaron hallazgos criticos ni altos con la evidencia disponible.

## 7. Todos los hallazgos

| ID | Hallazgo | Severidad | Confianza | OWASP/CWE | Archivo | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| SEC-001 | Datos de contacto potencialmente sensibles se incorporan en URLs de WhatsApp y `mailto:` | Media | Alta | OWASP A01:2025, CWE-201, ASVS v5.0.0-14.2.1 | `public/assets/js/main.js`, `public/contacto.html` | Confirmado |
| SEC-002 | Activos de fabricantes publicados pese a autorizacion de redistribucion no verificada | Media | Alta | OWASP A08:2025, supply chain/provenance | `docs/image-sources.json`, `public/*.html` | Confirmado |
| SEC-003 | Observabilidad/security logging del despliegue no verificable y deshabilitada en config local | Informativa | Media | OWASP A09:2025, ASVS v5.0.0-16.1.1 | `wrangler.jsonc`, `deploy/cloudflare-rules.md` | Requiere verificacion |
| SEC-004 | HSTS sin `includeSubDomains`/preload; aceptable para L1, hardening pendiente para niveles mayores | Informativa | Alta | OWASP A02:2025, ASVS v5.0.0-3.4.1 / 3.7.4 | `public/_headers`, `deploy/*` | Informativo |

### SEC-001 - Datos de contacto potencialmente sensibles se incorporan en URLs de WhatsApp y `mailto:`

Estado: Confirmado

Severidad: Media

Confianza: Alta

Categoria: OWASP A01:2025 Broken Access Control / CWE-201 Exposure of Sensitive Information Through Sent Data / ASVS v5.0.0-14.2.1

Ubicacion:

- `public/contacto.html:93-143`
- `public/assets/js/main.js:188-204`
- `public/privacidad.html:71-86`

Evidencia:

- El formulario solicita nombre, empresa, ciudad, servicio y mensaje (`public/contacto.html:101-132`).
- El sitio ofrece servicios de CCTV, alarmas, accesos, incendio, redes y soporte; el mensaje puede contener detalles de infraestructura fisica.
- `message(data)` concatena todos los campos (`public/assets/js/main.js:188-189`).
- El boton de WhatsApp abre `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message(data))}` (`public/assets/js/main.js:196`).
- El envio por correo construye un URI `mailto:` con `subject` y `body` codificados (`public/assets/js/main.js:204`).
- La politica de privacidad reconoce que se recolectan esos datos y que comunicaciones por WhatsApp/correo se rigen por esas plataformas (`public/privacidad.html:71-86`).

Escenario de riesgo:

Un usuario describe en el formulario detalles sobre fallas de camaras, alarmas, accesos, ubicacion o red. Al elegir WhatsApp, esos datos pasan como query string del URL `wa.me`; al elegir correo, pasan dentro de un URI `mailto:`. Aunque el envio es voluntario y esta codificado, la informacion puede quedar en historial local, logs o telemetria del navegador/aplicacion externa, y se entrega a una plataforma de terceros antes de que exista una conversacion ya iniciada dentro de la app.

Impacto:

- Exposicion indirecta de datos personales y detalles de seguridad fisica.
- Riesgo de incumplimiento de minimizacion si el mensaje contiene informacion sensible.
- Mayor dependencia de plataformas externas para el tratamiento de datos.

Probabilidad: Media. El flujo esta en la ruta principal de contacto y es el CTA recomendado.

Recomendacion:

- Para WhatsApp, prellenar solo un mensaje minimo no sensible, por ejemplo una solicitud generica, y pedir que los detalles se escriban dentro de la conversacion ya abierta.
- Mantener el formulario detallado solo si se envia por un canal con controles claros de privacidad, retencion y logging.
- Agregar aviso junto al formulario indicando que los detalles se abriran en WhatsApp/correo y pueden ser tratados por esas plataformas.
- Evitar incluir datos sensibles en URLs cuando exista alternativa.

Esfuerzo estimado: Bajo a medio.

### SEC-002 - Activos de fabricantes publicados pese a autorizacion de redistribucion no verificada

Estado: Confirmado

Severidad: Media

Confianza: Alta

Categoria: OWASP A08:2025 Software or Data Integrity Failures / supply chain provenance

Ubicacion:

- `docs/image-sources.json:2-6`
- `docs/image-sources.json:9-61`
- `public/index.html:121`
- `public/tecnologias.html:92-128`
- `tests/test_content_contract.py:456-459`

Evidencia:

- El registro declara `publication_gate.status: blocked` y exige no publicar hasta autorizacion escrita (`docs/image-sources.json:2-4`).
- `redistribution_authorization` figura como `unverified` (`docs/image-sources.json:6`).
- Cinco imagenes locales bajo `assets/img/brands/...` estan registradas con derechos no verificados o sin licencia de redistribucion expresa (`docs/image-sources.json:9-61`).
- Esas imagenes se referencian desde paginas publicas (`public/index.html:121`, `public/tecnologias.html:92-128`).
- Existe un test que documenta el bloqueo de publicacion por autorizacion no verificada (`tests/test_content_contract.py:456-459`).

Escenario de riesgo:

El sitio puede desplegar activos de fabricantes sin prueba de autorizacion de redistribucion. Esto no permite ejecucion de codigo ni acceso no autorizado, pero si introduce riesgo de integridad/procedencia del contenido publicado, reclamaciones, takedown, sustitucion apresurada de assets y perdida de confianza operativa.

Impacto:

- Riesgo legal/reputacional y de interrupcion de publicacion.
- El propio repositorio declara que la publicacion debe estar bloqueada.
- Debilita el control de procedencia de activos en el supply chain de contenido.

Probabilidad: Alta si el sitio se despliega con el `public/` actual.

Recomendacion:

- Sustituir imagenes por activos propios o con licencia explicita.
- Guardar evidencia de autorizacion en `docs/image-sources.json`.
- Convertir el gate en control de CI/CD antes del deploy si se agrega pipeline.
- No publicar `public/assets/img/brands/*` hasta resolver autorizaciones.

Esfuerzo estimado: Medio.

### SEC-003 - Observabilidad/security logging del despliegue no verificable y deshabilitada en config local

Estado: Requiere verificacion

Severidad: Informativa

Confianza: Media

Categoria: OWASP A09:2025 Security Logging and Alerting Failures / ASVS v5.0.0-16.1.1

Ubicacion:

- `wrangler.jsonc:5-6`
- `deploy/cloudflare-rules.md:47-50`
- `README_SEGURIDAD.md:33-35`

Evidencia:

- `wrangler.jsonc` declara `"observability": { "enabled": false }`.
- La documentacion recomienda revisar Security Events y logs despues de publicar, pero esa configuracion operacional no es verificable estaticamente (`deploy/cloudflare-rules.md:47-50`, `README_SEGURIDAD.md:33-35`).

Escenario de riesgo:

En una landing estatica el impacto es limitado, pero abuso de scraping, picos DDoS, errores de headers, ataques automatizados o intentos de publicar rutas no esperadas podrian quedar sin deteccion o sin evidencia util si Cloudflare Security Events/logging/alerting no esta habilitado fuera del repo.

Impacto:

- Menor capacidad de respuesta ante abuso.
- Menor evidencia durante incidentes.
- No afecta confidencialidad directamente en el codigo actual.

Probabilidad: No verificable con analisis estatico.

Recomendacion:

- Confirmar en Cloudflare Dashboard que Security Events, alertas y metricas relevantes estan habilitadas.
- Documentar responsable, retencion y revision de eventos.
- Si se agregan APIs/formularios server-side, elevar este control a requisito bloqueante.

Esfuerzo estimado: Bajo.

### SEC-004 - HSTS sin `includeSubDomains`/preload; aceptable para L1, hardening pendiente para niveles mayores

Estado: Informativo

Severidad: Informativa

Confianza: Alta

Categoria: OWASP A02:2025 Security Misconfiguration / ASVS v5.0.0-3.4.1 / ASVS v5.0.0-3.7.4

Ubicacion:

- `public/_headers:4`
- `deploy/nginx-static-secure.conf:49`
- `deploy/apache-htaccess-secure.txt:24`

Evidencia:

- HSTS usa `max-age=31536000`, lo cual cumple el minimo de un ano.
- No incluye `includeSubDomains` ni `preload`.

Escenario de riesgo:

Si existen subdominios bajo el mismo dominio y no fuerzan HTTPS, usuarios podrian quedar expuestos a downgrade/MITM en esos subdominios. No se probo el dominio ni los subdominios por restriccion de alcance, por lo que esto queda como hardening, no vulnerabilidad confirmada.

Impacto:

- Limitado al posture de transporte y solo si hay subdominios aplicables.

Probabilidad: Baja/no verificada.

Recomendacion:

- Confirmar inventario de subdominios antes de habilitar `includeSubDomains`.
- Si todos los subdominios sirven HTTPS correctamente, considerar `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload` y evaluar inclusion en preload list.

Esfuerzo estimado: Bajo a medio.

## 8. OWASP Top 10:2025

| Categoria | Estado | Evidencia |
| --- | --- | --- |
| A01 Broken Access Control | Aplicable parcialmente | No hay auth/autorizacion. Se usa para SEC-001 por CWE-201/sent data, categoria listada por OWASP A01:2025. |
| A02 Security Misconfiguration | Aplicable | Headers fuertes en `public/_headers:1-13`; hardening HSTS en SEC-004. |
| A03 Software Supply Chain Failures | Aplicable parcialmente | No hay dependencias de codigo ni lockfile; supply chain de contenido revisado en SEC-002. |
| A04 Cryptographic Failures | No aplicable en codigo | No hay criptografia, passwords, tokens ni backend; TLS runtime no verificable. |
| A05 Injection | Aplicable parcialmente | Form inputs se normalizan y se usan con `textContent`/`encodeURIComponent`; no hay SQL/NoSQL/shell/template sinks. |
| A06 Insecure Design | Aplicable parcialmente | Flujo de contacto via URL a terceros genera SEC-001. |
| A07 Authentication Failures | No aplicable | No hay login, usuarios, sesiones ni recuperacion de contrasena. |
| A08 Software or Data Integrity Failures | Aplicable | SEC-002 por procedencia/autorizacion de activos publicados. |
| A09 Security Logging and Alerting Failures | Requiere verificacion | SEC-003; no hay backend, pero Cloudflare runtime no se pudo verificar. |
| A10 Mishandling of Exceptional Conditions | No verificable/no aplicable | Sitio estatico sin backend; errores runtime de plataforma no verificables sin navegador/red. |

## 9. Supply Chain

Dependencias de codigo:

- No se encontro `package.json`, lockfile npm/pnpm/yarn/bun, `requirements.txt`, `pyproject.toml` ni CI que instale dependencias.
- No se detectaron `curl | shell`, `npx`, `postinstall`, acciones GitHub ni descarga de ejecutables en rutas de despliegue.

Activos:

- Recursos CSS, JS, fuentes e imagenes se sirven localmente.
- Riesgo confirmado de procedencia/autorizacion de imagenes en SEC-002.

Limitacion:

- No se ejecuto auditoria de paquetes porque no existe manifiesto/lockfile de paquetes que auditar.

## 10. Configuracion HTTP / headers

Configuracion principal en `public/_headers`:

- CSP restrictiva: `default-src 'self'`, `script-src 'self'`, `style-src 'self'`, `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'none'`, `form-action 'self'`.
- HSTS `max-age=31536000`.
- `X-Content-Type-Options: nosniff`.
- `X-Frame-Options: DENY`.
- `Referrer-Policy: strict-origin-when-cross-origin`.
- `Permissions-Policy` restrictiva.
- COOP/CORP definidos.
- `X-XSS-Protection: 0`, decision moderna razonable.

Observaciones:

- Cloudflare documenta que `_headers` en el directorio de assets estaticos aplica a respuestas de assets estaticos tanto para Pages como para Workers Static Assets. No aplica a respuestas generadas por Functions/Worker code. No se detectaron Pages Functions, `_worker.js`, `main` de Worker ni `assets.run_worker_first`.
- Los headers reales de produccion no fueron verificados por restriccion de alcance.

## 11. Frontend Security

Entradas:

- `name`, `company`, `city`, `service`, `message`.
- Query parameter `servicio`.

Controles:

- Longitudes HTML (`public/contacto.html:101-132`) y limites JS (`public/assets/js/main.js:3`).
- Normalizacion y eliminacion de caracteres de control (`public/assets/js/main.js:128-132`).
- `service` se valida contra allowlist (`public/assets/js/main.js:4-11`, `public/assets/js/main.js:183`).
- Mensajes de error se asignan con `textContent`, no HTML (`public/assets/js/main.js:167`).
- WhatsApp y correo usan `encodeURIComponent` (`public/assets/js/main.js:196`, `public/assets/js/main.js:204`).
- `servicio` desde query solo se aplica si coincide con allowlist (`public/assets/js/main.js:215-217`).

No se detecto:

- `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `Function`, `postMessage`, `fetch`, XHR, cookies, localStorage ni sessionStorage en codigo productivo.
- `target="_blank"` sin `rel="noopener noreferrer"` en enlaces externos revisados.
- Recursos externos ejecutables.

## 12. Backend/API

No aplicable. No se detecto backend, API, serverless functions, Workers custom code, Pages Functions, endpoints administrativos ni almacenamiento server-side.

## 13. Autenticacion/autorizacion

No aplicable. No hay login, usuarios, roles, sesiones, JWT, cookies de autenticacion ni panel administrativo.

## 14. Datos y privacidad

Datos personales identificados:

- Nombre.
- Empresa u organizacion.
- Ciudad.
- Servicio de interes.
- Mensaje libre.

Datos potencialmente sensibles por contexto:

- Detalles de CCTV, alarmas, control de acceso, incendio, red y soporte tecnico.

Controles positivos:

- La politica declara no usar cookies de terceros ni almacenar en bases permanentes del sitio (`public/privacidad.html:71-86`).
- El sitio no procesa formularios en servidor propio segun README (`README.md:82`).

Riesgo:

- SEC-001: datos de contacto y posibles detalles de infraestructura se incorporan en URLs de terceros o `mailto:`.

## 15. CI/CD

No se detecto `.github/workflows` ni otra configuracion CI/CD.

Riesgo:

- No hay pipeline verificable que bloquee el gate de imagenes de SEC-002.
- Si se agrega CI/CD, deberia ejecutar tests, validar `docs/image-sources.json`, comprobar secretos y validar headers.

## 16. Cloudflare/deployment

Configuracion observada:

- `wrangler.jsonc` define `name`, `compatibility_date`, `observability.enabled=false` y `assets.directory="./public"` con `html_handling="drop-trailing-slash"` (`wrangler.jsonc:1-12`).
- `README.md` indica Cloudflare Pages, build command vacio, output `public`, dominio y HTTPS (`README.md:60-67`).
- `public/_headers` y `public/_redirects` estan en el directorio publicado.

No verificable:

- Dominio real.
- SSL/TLS `Full (strict)`.
- Always Use HTTPS.
- WAF/Bot Fight/managed rules.
- Security Events.
- Aplicacion efectiva de headers en produccion.

## 17. Hardening recomendado

P0 - inmediato:

- Resolver SEC-002 antes de publicar: retirar/sustituir imagenes no autorizadas o documentar autorizacion escrita.

P1 - corto plazo:

- Reducir datos prellenados en WhatsApp/`mailto:` segun SEC-001.
- Agregar aviso de tratamiento por plataformas externas junto al formulario.
- Confirmar en Cloudflare la aplicacion efectiva de headers, HTTPS, WAF basico y Security Events.

P2 - recomendado:

- Convertir el gate de `docs/image-sources.json` en chequeo automatico si se agrega CI/CD.
- Documentar retencion y revision de eventos de seguridad.
- Mantener recursos ejecutables exclusivamente locales; si se agregan CDN, exigir SRI y version fija.

P3 - hardening futuro:

- Evaluar HSTS `includeSubDomains; preload` cuando exista inventario de subdominios.
- Si se agrega backend/formulario server-side: validacion server-side, anti-spam, rate limiting, logging seguro, retencion definida, CSRF si hay cookies/sesiones, y gestion de secretos fuera del codigo.

## 18. Elementos no verificables

- Headers reales servidos por `https://jesareko.com/`.
- Estado real de Cloudflare: TLS mode, Always Use HTTPS, WAF, Bot Fight, cache rules, redirects de `www`, Security Events.
- Logs/alertas y retencion operacional.
- Historial Git completo de secretos; se reviso el arbol actual y archivos sensibles versionados, sin recorrer historia completa porque no hubo evidencia que lo justificara.
- Derechos reales de imagenes ante fabricantes; el repositorio declara no verificados.
- Comportamiento runtime en navegadores por restriccion explicita de no usar navegador/DevTools/Playwright/Lighthouse.

## 19. Fuentes oficiales consultadas

- OWASP Top 10:2025: https://top10.owasp.org/2025/
- OWASP A01:2025 Broken Access Control: https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/
- OWASP ASVS 5.0.0 repository: https://github.com/OWASP/ASVS/tree/v5.0.0
- OWASP ASVS 5.0.0 CSV: https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/docs_en/OWASP_Application_Security_Verification_Standard_5.0.0_en.csv
- Cloudflare Pages custom headers: https://developers.cloudflare.com/pages/configuration/headers/
- Cloudflare Workers Static Assets headers: https://developers.cloudflare.com/workers/static-assets/headers/
