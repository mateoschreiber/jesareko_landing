# Final fix report — 2026-07-26

## Correcciones

- La navegación móvil conserva enlaces visibles sin JavaScript. JavaScript añade `.js` y solo entonces habilita el botón y el estado colapsado; el menú abierto queda en el flujo normal del header.
- El formulario tiene `action="mailto:"` y una alternativa explícita de correo/WhatsApp que sigue disponible sin JavaScript. WhatsApp conserva la prioridad con JavaScript.
- El foco usa un contorno sólido `--color-brand-dark`; el botón «Volver arriba» inicia fuera del árbol de foco/accesibilidad y respeta `prefers-reduced-motion` al desplazarse.
- Tecnologías añade secciones ligeras y honestas de Redes y WiFi y Soporte técnico. Sus metadatos y JSON-LD ya no prometen detección de incendio ni monitoreo.
- Todos los CTA globales de WhatsApp llevan mensaje prellenado. La política conserva el número directo de contacto sin alterarlo.
- Se retiraron los componentes CSS heredados sin uso (dashboard, métricas, grids/tarjetas antiguas); el análisis contra las seis páginas dejó `unused_static_css_classes: none` y `legacy_selector_hits: 0`.
- `scripts/serve-static.py` sirve rutas limpias locales; README documenta su uso.
- `docs/image-sources.json` bloquea la publicación hasta contar con autorización escrita de redistribución; no se modificaron activos.

## TDD y contratos

Antes de implementar se añadieron contratos focalizados para navegación sin JS, foco/volver arriba, rutas limpias, fallback de contacto, CTA prellenados, catálogo ampliado y gate de publicación. La primera ejecución falló en los siete contratos por las ausencias esperadas; tras los cambios, los siete pasaron. Se ajustó un contrato de Casos para evaluar solo el contenido editorial, no el porcentaje codificado de una URL de WhatsApp.

## Verificación fresca

```text
python -m unittest discover -s tests -v  -> OK (38 tests)
python -m compileall tests scripts       -> exit 0
node --check public/assets/js/main.js    -> exit 0
git diff --check                         -> exit 0
```

El contrato de servidor levantó un servidor temporal y comprobó `200` para `/`, `/servicios`, `/casos`, `/tecnologias`, `/contacto` y `/privacidad`.

## Residual

- No se ejecutó una matriz visual de overflow en navegador en esta ola; no se inventó esa verificación. Permanecen los contratos estáticos de layout y los artefactos QA previos sin versionar.
- La publicación sigue bloqueada mientras la autorización de redistribución de los activos de fabricantes sea no verificada.
