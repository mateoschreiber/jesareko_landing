# Security Remediation Report

## 1. Resumen ejecutivo

Se convirtio `SECURITY-AUDIT.md` en un plan de accion y se aplicaron mitigaciones controladas para SEC-001 a SEC-004 sin despliegue, commit ni push. La arquitectura sigue siendo estatica y no se agregaron dependencias.

## 2. Estado antes/despues

| Hallazgo | Antes | Despues | Evidencia |
| --- | --- | --- | --- |
| SEC-001 | Datos del formulario se incorporaban a URLs de WhatsApp y `mailto:` | RESUELTO | `public/assets/js/main.js` usa `contactPrompt()` minimo; `tests/contact-query-runtime.mjs` valida que campos sensibles no aparezcan en URLs. |
| SEC-002 | Assets con `publication_gate = blocked` estaban referenciados desde HTML publicable | MITIGADO | `public/index.html` y `public/tecnologias.html` usan visuales propios CSS/HTML; tests bloquean referencias a `docs/image-sources.json`. |
| SEC-003 | `observability.enabled = false` y dashboard no verificable | MITIGADO + REQUIERE ACCION EXTERNA | `wrangler.jsonc` habilita observabilidad; docs agregan checklist de Security Events, alertas, metricas, retencion y responsable. |
| SEC-004 | HSTS sin `includeSubDomains`/`preload` | NO MODIFICAR / PRECONDICION NO VERIFICADA | Headers no se cambiaron; `README_SEGURIDAD.md` documenta checklist futura. |

## 3. SEC-001

- Cambio: WhatsApp y correo preparan solo `Hola Jesareko, quisiera solicitar informacion tecnica.` con subject generico para correo.
- UI: el formulario aclara que los detalles quedan en el formulario y agrega aviso sobre WhatsApp/correo como servicios externos.
- Privacidad: se documento que esos detalles no se envian automaticamente en el texto prellenado.
- Resultado: RESUELTO.

## 4. SEC-002

- Cambio: se retiraron de HTML publico las cinco referencias a `assets/img/brands/*`.
- Sustitucion: se agregaron visuales propios con CSS/HTML, sin reproducir activos de fabricantes.
- Registro: `docs/image-sources.json` conserva `blocked` y `unverified`; no se invento autorizacion.
- Tests: el gate ahora falla si cualquier asset registrado queda referenciado desde HTML publicable.
- Resultado: MITIGADO.

## 5. SEC-003

- Cambio versionado: `wrangler.jsonc` ahora usa `observability.enabled = true` y `head_sampling_rate = 1`.
- Base documental: Cloudflare Workers Logs documenta que `observability` persiste logs del Worker y que `head_sampling_rate` controla el porcentaje de requests registrados.
- Limite: Security Events, alertas, metricas, retencion, costo real y utilidad post-deploy requieren Cloudflare Dashboard/deployment real.
- Resultado: MITIGADO + REQUIERE ACCION EXTERNA.

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
- Static check `assets/img/brands` under `public/` -> OK, no public references.
- Static check HSTS `includeSubDomains`/`preload` in deployed header templates -> OK, not added.

## 9. Resultados

- No quedan referencias publicas a assets bloqueados/no verificados.
- Las URLs generadas por el formulario no incluyen nombre, empresa, ciudad, servicio ni mensaje libre.
- No se agregaron sinks DOM inseguros.
- HSTS no se endurecio sin precondiciones.
- Observabilidad versionada quedo habilitada para el flujo `wrangler`, con verificacion post-deploy pendiente.

## 10. Riesgos residuales

- Los assets de fabricantes siguen presentes en `public/assets/img/brands/*`, pero no referenciados desde HTML publicable.
- El estado real de Cloudflare Security Events/alertas/logs no puede verificarse sin dashboard/deploy.
- `head_sampling_rate = 1` puede requerir ajuste operativo si el volumen/costo de Workers Logs lo demanda.
- HSTS `includeSubDomains`/`preload` queda pendiente hasta inventariar subdominios.

## 11. Acciones externas requeridas

- Obtener autorizacion escrita o proveer activos propios si se quieren restaurar imagenes de fabricantes.
- Confirmar en Cloudflare Dashboard: Security Events, alertas, metricas, retencion, responsable y revision periodica.
- Revisar costo/volumen de Workers Logs despues del despliegue.
- Inventariar subdominios y validar HTTPS antes de cambiar HSTS.

## 12. Verificacion post-deploy

POST-DEPLOY VERIFICATION REQUIRED:

- Confirmar que headers reales se sirven como espera `public/_headers`.
- Confirmar que Workers Logs recibe datos utiles para el deployment real si se usa `wrangler`.
- Confirmar que Security Events y alertas estan activos en Cloudflare Dashboard.
- Confirmar que no hay referencias publicas cacheadas a `assets/img/brands/*`.

## 13. Rollback

- SEC-001: restaurar el armado de mensajes anterior solo si se reemplaza por un canal con controles claros de privacidad.
- SEC-002: restaurar assets de fabricantes solo con autorizacion documentada o reemplazarlos por activos propios registrados.
- SEC-003: volver `observability.enabled` a `false` o bajar `head_sampling_rate` si el costo/retencion no es aceptable.
- SEC-004: no hay rollback de headers porque no se modificaron.

## 14. Fuentes oficiales consultadas

- Cloudflare Workers Wrangler configuration: https://developers.cloudflare.com/workers/wrangler/configuration/
- Cloudflare Workers Logs: https://developers.cloudflare.com/workers/observability/logs/workers-logs/
