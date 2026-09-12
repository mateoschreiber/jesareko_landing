# Security Remediation Report

## 1. Resumen ejecutivo

Se convirtio `SECURITY-AUDIT.md` en un plan de accion y se aplicaron mitigaciones controladas para SEC-001 a SEC-004 sin despliegue, commit ni push. La arquitectura sigue siendo estatica y no se agregaron dependencias.

## 2. Estado antes/despues

| Hallazgo | Antes | Despues | Evidencia |
| --- | --- | --- | --- |
| SEC-001 | Datos del formulario se incorporaban a URLs de WhatsApp y `mailto:` | RESUELTO | `public/contacto.html` no solicita datos personales ni detalles de infraestructura; `public/assets/js/main.js` usa un mensaje general y `tests/contact-query-runtime.mjs` valida las URLs. |
| SEC-002 | Assets con `publication_gate = blocked` estaban dentro de `public/` y referenciados desde HTML publicable | RESUELTO | Los binarios bloqueados se movieron a `docs/restricted-assets/`; tests comprueban que no existan dentro del directorio publicable ni en HTML. |
| SEC-003 | Observabilidad/security logging no verificable desde repo; `observability.enabled = false` | REQUIERE ACCION EXTERNA | No hay Worker script/`main`; `wrangler.jsonc` conserva `observability.enabled = false` y la documentacion lista verificaciones de Cloudflare Dashboard. |
| SEC-004 | HSTS sin `includeSubDomains`/`preload` | NO MODIFICAR / PRECONDICION NO VERIFICADA | Headers no se cambiaron; `README_SEGURIDAD.md` documenta checklist futura. |

## 3. SEC-001

- Cambio: WhatsApp y correo preparan solo `Hola Jesareko, quisiera solicitar informacion tecnica.` con subject generico para correo.
- UI: se retiro la captura de nombre, empresa, ciudad, servicio y mensaje; el panel explica que los canales se abren con un mensaje general.
- Privacidad: `public/privacidad.html` documenta que el sitio no almacena datos personales ni los transfiere desde sus botones.
- Resultado: RESUELTO.

## 4. SEC-002

- Cambio: se retiraron de HTML publico las cinco referencias a `assets/img/brands/*` y los cinco binarios bloqueados salieron de `public/`.
- Sustitucion: se agregaron visuales propios con CSS/HTML, sin reproducir activos de fabricantes.
- Registro: `docs/image-sources.json` conserva `blocked` y `unverified`, y ahora apunta a `docs/restricted-assets/*`; no se invento autorizacion.
- Tests: el gate ahora falla si cualquier asset registrado queda referenciado desde HTML publicable o existe fisicamente dentro del directorio publicado.
- Resultado: RESUELTO.

## 5. SEC-003

- Cambio versionado: se revirtio el cambio anterior; `wrangler.jsonc` conserva `observability.enabled = false`.
- Base documental: Cloudflare documenta que `assets.directory` define los Static Assets y que Workers Logs/observability se orienta a logs del Worker. Este proyecto no declara Worker script/`main` ni logging propio, por lo que `head_sampling_rate = 1` no se mantiene solo por hardening aparente.
- Limite: Security Events, WAF/managed rules, Bot protections, alertas, analytics, HTTPS/TLS, headers efectivos, retencion, costo real y responsable requieren Cloudflare Dashboard/deployment real.
- Resultado: REQUIERE ACCION EXTERNA.

## 6. SEC-004

- Cambio de headers: ninguno.
- Motivo: el repositorio no contiene inventario de subdominios ni evidencia de HTTPS valido en todos.
- Documentacion: se agrego checklist antes de evaluar `includeSubDomains` o `preload`.
- Resultado: NO MODIFICAR / PRECONDICION NO VERIFICADA.

## 7. Archivos modificados

- `SECURITY-REMEDIATION-PLAN.md`
- `SECURITY-REMEDIATION-REPORT.md`
- `README_SEGURIDAD.md`
- `deploy/cloudflare-rules.md`
- `docs/image-sources.json`
- `docs/restricted-assets/*`
- `wrangler.jsonc`
- `public/index.html`
- `public/tecnologias.html`
- `public/assets/css/styles.css`
- `public/assets/js/main.js`
- `public/contacto.html`
- `public/privacidad.html`
- `tests/contact-query-runtime.mjs`
- `tests/test_content_contract.py`
- `tests/test_site_contract.py`

## 8. Tests ejecutados

- `node tests/contact-query-runtime.mjs` -> OK.
- `C:/Users/MaSch/AppData/Local/Programs/Python/Python312/python.exe -m unittest tests.test_content_contract.ContentContractTests.test_blocked_brand_assets_are_replaced_by_owned_visuals tests.test_content_contract.ContentContractTests.test_image_source_registry_blocks_publication_without_redistribution_authorization tests.test_content_contract.ContentContractTests.test_contact_query_initialization_runtime_contract tests.test_site_contract.SiteContractTests.test_blocked_technology_catalog_assets_are_not_published` -> OK.
- `C:/Users/MaSch/AppData/Local/Programs/Python/Python312/python.exe -m unittest tests.test_content_contract.ContentContractTests.test_technologies_is_an_editorial_application_catalog` -> OK.
- `C:/Users/MaSch/AppData/Local/Programs/Python/Python312/python.exe -m unittest discover -s tests` -> OK, 44 tests.
- `rtk git diff --check` -> OK.
- Static check `assets/img/brands` under `public/` -> OK, no blocked/unverified files inside the public directory.
- Static check HSTS `includeSubDomains`/`preload` in deployed header templates -> OK, not added.

## 9. Resultados

- No quedan referencias publicas ni archivos fisicos publicables de assets bloqueados/no verificados.
- Las URLs generadas por los botones de contacto no incluyen datos personales, servicio ni mensaje libre.
- No se agregaron sinks DOM inseguros.
- HSTS no se endurecio sin precondiciones.
- Observabilidad por `wrangler` queda deshabilitada para este sitio static-assets-only; la deteccion operacional pasa a Cloudflare Dashboard.

## 10. Riesgos residuales

- Los assets de fabricantes se conservan fuera de `public/` como evidencia restringida en `docs/restricted-assets/*`.
- El estado real de Cloudflare Security Events, WAF/Bot protections, alertas, analytics, HTTPS/TLS, headers efectivos y retencion no puede verificarse sin dashboard/deploy.
- HSTS `includeSubDomains`/`preload` queda pendiente hasta inventariar subdominios.

## 11. Acciones externas requeridas

- Obtener autorizacion escrita o proveer activos propios si se quieren restaurar imagenes de fabricantes.
- Confirmar en Cloudflare Dashboard: Security Events, WAF/managed rules cuando corresponda, Bot protections, alertas, analytics, HTTPS/TLS, headers efectivos, retencion, responsable y revision periodica.
- Inventariar subdominios y validar HTTPS antes de cambiar HSTS.

## 12. Verificacion post-deploy

POST-DEPLOY VERIFICATION REQUIRED:

- Confirmar que headers reales se sirven como espera `public/_headers`.
- Confirmar que Security Events, WAF/Bot protections, alertas y analytics estan activos en Cloudflare Dashboard.
- Confirmar que no hay URLs publicas cacheadas para los antiguos `assets/img/brands/*`.

## 13. Rollback

- SEC-001: restaurar el armado de mensajes anterior solo si se reemplaza por un canal con controles claros de privacidad.
- SEC-002: restaurar assets de fabricantes dentro de `public/` solo con autorizacion documentada o reemplazarlos por activos propios registrados.
- SEC-003: habilitar `observability` solo si se agrega Worker script/telemetria util y se define un muestreo respaldado por necesidad operativa.
- SEC-004: no hay rollback de headers porque no se modificaron.

## 14. Fuentes oficiales consultadas

- Cloudflare Workers Wrangler configuration: https://developers.cloudflare.com/workers/wrangler/configuration/
- Cloudflare Workers Static Assets: https://developers.cloudflare.com/workers/static-assets/
- Cloudflare Workers Logs: https://developers.cloudflare.com/workers/observability/logs/workers-logs/
