# Security Remediation Plan

## 1. Estado inicial

Fuente principal: `SECURITY-AUDIT.md`, verificado de forma dirigida sobre HEAD local el 2026-09-12.

| Hallazgo | Estado actual | Evidencia verificada |
| --- | --- | --- |
| SEC-002 | Confirmado | `docs/image-sources.json` mantiene `publication_gate.status = blocked` y `redistribution_authorization = unverified`; `public/index.html` y `public/tecnologias.html` referencian `assets/img/brands/*`. |
| SEC-001 | Confirmado | `public/assets/js/main.js` construye URLs `wa.me` y `mailto:` con nombre, empresa, ciudad, servicio y mensaje. |
| SEC-003 | Confirmado parcialmente | `wrangler.jsonc` tiene `observability.enabled = false`; la verificacion de Security Events, alertas, metricas y retencion depende de Cloudflare Dashboard. |
| SEC-004 | Informativo | `public/_headers`, Nginx y Apache usan `Strict-Transport-Security: max-age=31536000` sin `includeSubDomains` ni `preload`; no hay inventario de subdominios en el repo. |

## 2. Alcance

Se modificaran solo archivos directamente relacionados con SEC-001 a SEC-004. No se hara auditoria nueva, crawling, navegador, despliegue, push ni commit. No se cambiara ninguna licencia a verificada sin evidencia documental.

## 3. Orden de ejecucion

1. SEC-002: alinear el contenido publicable con el gate de activos.
2. SEC-001: reducir datos prellenados en WhatsApp y correo.
3. SEC-003: aplicar configuracion de observabilidad solo donde la documentacion oficial la respalda y documentar controles externos.
4. SEC-004: no endurecer HSTS sin precondiciones verificadas; documentar checklist futura.
5. Revision de diffs y validacion dirigida/completa.

## 4. SEC-002 - Procedencia de activos

- Estado actual: Confirmado.
- Evidencia: `docs/image-sources.json` bloquea publicacion y mantiene autorizacion no verificada; HTML publico referencia cinco assets bajo `assets/img/brands/*`; el test existente solo comprueba que el bloqueo este documentado, no que impida publicacion.
- Cambio propuesto: retirar referencias publicas a los assets bloqueados y reemplazarlas por recursos visuales propios, sin tocar los archivos de imagen restringidos ni marcar autorizaciones como verificadas. Reforzar `tests/test_content_contract.py` para fallar si un asset bloqueado/no verificado queda referenciado desde HTML publicable.
- Archivos afectados: `public/index.html`, `public/tecnologias.html`, `public/assets/css/styles.css`, `tests/test_content_contract.py`.
- Riesgo del cambio: bajo a medio; cambia piezas visuales en hero/catalogo, pero mantiene la arquitectura estatica y copy tecnico.
- Pruebas: content contract, validacion de referencias de assets, suite completa.
- Criterio de aceptacion: ningun `assets/img/brands/*` bloqueado aparece en HTML publicable; `docs/image-sources.json` sigue reflejando no verificado; el test detecta regresion.
- Rollback: restaurar los `img` solo cuando exista autorizacion documentada o sustituir por activos propios registrados.
- Resultado esperado: MITIGADO.

## 5. SEC-001 - Privacidad del contacto

- Estado actual: Confirmado.
- Evidencia: `message(data)` concatena todos los campos y se usa en `wa.me` y `mailto:`; la UI afirma que los datos se envian por WhatsApp o correo.
- Cambio aplicado: retirar la captura de datos y mantener solo canales con mensajes prellenados minimos. El sitio no pide nombre, empresa, ciudad, servicio ni mensaje libre, y la politica de privacidad describe el flujo de contacto externo.
- Archivos afectados: `public/assets/js/main.js`, `public/contacto.html`, `public/privacidad.html`, tests relacionados.
- Riesgo del cambio: bajo; conserva el flujo de contacto y reduce exposicion de datos en URLs.
- Pruebas: tests de contacto, busquedas dirigidas de URL/body, suite completa.
- Criterio de aceptacion: las URLs generadas no incorporan datos personales ni detalles sensibles; no aparecen nuevos sinks DOM inseguros; la UI describe correctamente el flujo.
- Rollback: restaurar el armado anterior solo si se reemplaza por un canal con controles de privacidad adecuados.
- Resultado esperado: RESUELTO.

## 6. SEC-003 - Observabilidad

- Estado actual: Confirmado parcialmente.
- Evidencia: `wrangler.jsonc` deshabilita `observability`; documentacion oficial de Cloudflare Workers indica que esa opcion persiste logs del Worker, que los Workers nuevos la tienen habilitada por defecto, y que `head_sampling_rate` controla el porcentaje de requests registrados. Workers Logs tiene limites/retencion/costos segun plan. El estado de Security Events, alertas y retencion operacional no es verificable desde el repo.
- Cambio propuesto: habilitar observabilidad en `wrangler.jsonc` con muestreo conservador y documentar que aplica al deployment via Workers Static Assets/Wrangler. Agregar checklist externa para Cloudflare Dashboard: Security Events, alertas, metricas, retencion, responsable y revision periodica.
- Archivos afectados: `wrangler.jsonc`, `deploy/cloudflare-rules.md`, `README_SEGURIDAD.md`.
- Riesgo del cambio: bajo a medio; aumenta observabilidad pero puede generar volumen de logs segun trafico y plan.
- Pruebas: validacion sintactica JSONC si existe herramienta disponible, revision de diff, suite existente.
- Criterio de aceptacion: configuracion respaldada por docs oficiales y documentacion clara de elementos no verificables.
- Rollback: volver `observability.enabled` a `false` si el plan/costo operativo no lo permite.
- Resultado esperado: MITIGADO + REQUIERE ACCION EXTERNA para controles de dashboard.

## 7. SEC-004 - HSTS

- Estado actual: Informativo.
- Evidencia: HSTS existe con un ano de `max-age`, pero no hay inventario de subdominios ni evidencia de HTTPS valido para todos.
- Cambio propuesto: no modificar headers HSTS. Documentar estado `NO MODIFICAR / PRECONDICION NO VERIFICADA` y checklist futura.
- Archivos afectados: documentacion solamente.
- Riesgo del cambio: bajo; evita bloquear subdominios desconocidos.
- Pruebas: verificar que `includeSubDomains` y `preload` no se agreguen.
- Criterio de aceptacion: no se endurece HSTS sin evidencia; existe checklist futura.
- Rollback: no aplica mientras no cambien headers.
- Resultado esperado: NO MODIFICAR / PRECONDICION NO VERIFICADA.

## 8. Archivos previstos

- `SECURITY-REMEDIATION-PLAN.md`
- `SECURITY-REMEDIATION-REPORT.md`
- `public/index.html`
- `public/tecnologias.html`
- `public/assets/css/styles.css`
- `tests/test_content_contract.py`
- `public/contacto.html`
- `public/assets/js/main.js`
- `public/privacidad.html`
- `wrangler.jsonc`
- `deploy/cloudflare-rules.md`
- `README_SEGURIDAD.md`

## 9. Riesgos de regresion

- Perdida visual por retirar imagenes de fabricantes.
- Tests existentes que asumian imagenes especificas en posiciones primarias.
- Contacto menos detallado al abrir WhatsApp/correo.
- Volumen/costo de Workers Logs si el muestreo no se revisa despues del despliegue.
- Confundir documentacion de acciones externas con evidencia ya verificada.

## 10. Validacion

- Tests dirigidos de `tests/test_content_contract.py`.
- Tests relacionados con contacto, incluido `tests/contact-query-runtime.mjs`.
- Validacion de referencias de assets bloqueados/no verificados.
- Validacion de archivos estaticos existente.
- Suite completa existente una sola vez al final.
- `git diff --check`.

## 11. Rollback

- SEC-002: revertir placeholders o reemplazarlos por activos propios/autorizados registrados.
- SEC-001: revertir funciones de mensaje minimo si se implementa un canal con privacidad controlada.
- SEC-003: revertir `observability.enabled` o ajustar `head_sampling_rate` segun decision operativa.
- SEC-004: sin cambio de headers; retirar solo documentacion si se obtiene evidencia suficiente y se decide endurecer.

## 12. Elementos que requieren accion humana/externa

- Obtener autorizacion escrita de redistribucion o proveer activos propios para `assets/img/brands/*`.
- Confirmar en Cloudflare Dashboard: Security Events, alertas, metricas, retencion, responsable y revision periodica.
- Verificar post-deploy que Workers Logs/observabilidad producen datos utiles para el deployment real.
- Inventariar subdominios, validar HTTPS en todos, confirmar que ninguno requiere HTTP y evaluar impacto antes de `includeSubDomains`/`preload`.
