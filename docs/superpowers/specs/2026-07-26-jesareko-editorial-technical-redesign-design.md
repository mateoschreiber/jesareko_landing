# Rediseño editorial técnico de Jesareko

## Objetivo

Rediseñar todo `jesareko.com` para que deje de percibirse como una plantilla genérica o generada por IA y adopte una identidad editorial técnica inspirada en la referencia de Selux. El resultado debe equilibrar fotografía de producto, jerarquía tipográfica, contenido comercial claro y credibilidad técnica local.

La experiencia prioriza mobile, sirve por igual a hogares y empresas, conserva el logo y el verde de Jesareko y orienta la conversión hacia la solicitud de un diagnóstico por WhatsApp.

## Alcance

El rediseño cubre:

- Inicio.
- Servicios.
- Casos.
- Tecnologías.
- Contacto.
- Navegación global, footer y componentes compartidos.
- Revisión y reducción del contenido existente sin cambiar su significado esencial.
- Responsive, accesibilidad, estados de interacción y validación visual.

No incluye renovación del logo, cambio de identidad corporativa, creación de certificaciones, testimonios, métricas o casos no verificables, ni incorporación de un CMS.

## Dirección aprobada

La dirección elegida es **Editorial técnica**. Combina:

- Retícula asimétrica y espacios amplios inspirados en Selux.
- Fotografías de equipos e instalaciones como elementos compositivos principales.
- Titulares editoriales breves.
- Servicios agrupados por función, no por tarjetas equivalentes.
- Prueba técnica, proceso y contexto local.
- Conversión visible sin repetir CTA en cada bloque.

La interfaz no debe copiar la identidad de Selux. La referencia se limita a principios de composición, jerarquía y disciplina visual.

## Arquitectura de información

### Navegación global

La navegación tendrá cinco destinos: Inicio, Servicios, Casos, Tecnologías y Contacto. En escritorio será horizontal. En mobile se abrirá mediante un control claramente etiquetado y se desplegará sin cubrir contenido crítico ni generar desplazamiento horizontal.

El CTA global será «Solicitar diagnóstico» y abrirá WhatsApp con texto predefinido. El icono de WhatsApp será el SVG oficial, acompañado siempre por una etiqueta textual.

### Inicio

1. **Hero editorial:** ubicación, promesa breve, explicación concisa, CTA principal e imagen técnica.
2. **Tres áreas principales:** Redes y WiFi, Seguridad física y Soporte técnico.
3. **Evidencia tecnológica:** uso de Hikvision y Dahua según cobertura, entorno y mantenimiento, sin sugerir certificaciones inexistentes.
4. **Proceso:** diagnóstico, propuesta, instalación y entrega documentada.
5. **Casos o situaciones frecuentes:** problema, intervención y resultado verificable.
6. **Cierre:** un único llamado claro al diagnóstico por WhatsApp.

### Servicios

La página ayudará al visitante a reconocer su necesidad. Cada área tendrá una introducción breve, situaciones que resuelve, alcance y siguiente acción. Se elimina la fórmula repetida «Incluye / Conviene cuando / Resultado» y el exceso de listas redundantes.

### Casos

Cada caso seguirá una estructura estable:

1. Situación inicial.
2. Criterio aplicado.
3. Intervención.
4. Resultado verificable.

Si aún no existen fotografías o resultados propios suficientes, se mostrarán escenarios de trabajo claramente identificados como aplicaciones frecuentes, no como proyectos ejecutados.

### Tecnologías

La página funcionará como catálogo editorial de aplicaciones y equipos. Las marcas y productos se organizarán por propósito: videovigilancia, alarmas, acceso, redes y soporte. Las imágenes deberán proceder de sitios oficiales o recursos con licencia adecuada y registrar URL, marca y condiciones de uso.

### Contacto

WhatsApp será la vía principal. El formulario será secundario y pedirá únicamente los datos necesarios para orientar el diagnóstico. Los mensajes de error se mostrarán junto al campo y el estado final será explícito.

### Footer

El footer retomará la densidad informativa de Selux, pero con una jerarquía más simple: navegación, áreas de servicio, ubicación, contacto y enlaces legales. En mobile se convertirá en grupos apilados legibles.

## Sistema visual

### Color

Se conserva el verde actual como color de marca y acción. La mayor parte de la interfaz usará blanco, grises cálidos y verde oscuro. El verde brillante de WhatsApp se reservará para el icono o la acción correspondiente y no reemplazará el color de marca.

### Tipografía

- Inter: navegación, cuerpo, etiquetas y controles.
- Merriweather: titulares editoriales y cifras destacadas.

Los titulares serán cortos y tendrán cortes de línea controlados. El contenido mantendrá longitudes cómodas y no se justificará.

### Radios

La escala aprobada es:

- 10 px: inputs, iconos y controles pequeños.
- 14 px: botones principales y tarjetas compactas.
- 20 px: imágenes, paneles y superficies destacadas.
- Radio de cápsula: solo etiquetas breves cuando aporte semántica.

No se aplicará el mismo radio a todos los componentes.

### Espaciado

El sistema partirá de una unidad de 8 px. Las separaciones principales usarán valores de la escala y `clamp()` cuando deban variar con el viewport. Cada componente tendrá espaciado interno propio; no se corregirán solapamientos mediante márgenes negativos.

### Imágenes y logos

- El logo de Jesareko conservará su proporción y zona de seguridad.
- Hikvision y Dahua usarán wordmarks oficiales en SVG o PNG de alta resolución.
- Todos los logos usarán dimensiones reservadas y `object-fit: contain`.
- Las fotografías de equipos usarán relaciones de aspecto declaradas para evitar saltos de layout.
- No se deformarán, recortarán de forma destructiva ni mezclarán imágenes de distinta calidad sin tratamiento común.
- Cada imagen tendrá texto alternativo útil o `alt=""` cuando sea decorativa.

## Componentes

### Botones

Los botones tendrán altura táctil mínima de 48 px. El CTA de WhatsApp combinará icono oficial, texto y contraste suficiente. El icono no se dibujará mediante caracteres, emojis ni formas aproximadas.

### Servicios

En escritorio se presentarán como filas o módulos editoriales. En mobile se apilarán en flujo normal. Cada módulo tendrá un destino completo y un indicador direccional consistente.

### Casos

Los casos combinarán imagen, contexto y resultado. No se repetirán decoraciones, badges o sombras si no ayudan a interpretar el contenido.

### Formularios

Los campos mostrarán etiqueta persistente, ayuda cuando sea necesaria, foco visible, error específico y confirmación final. El selector de servicio debe funcionar con teclado, lectores de pantalla y pantallas táctiles.

### Logos e iconos

Los iconos compartirán tamaño visual, trazo y alineación. Se evitarán bloques decorativos vacíos. Los logos de terceros no se alterarán ni se usarán como iconos de interfaz.

## Interacción y estados

- Transiciones entre 160 y 220 ms.
- Sin dependencia de hover para descubrir contenido.
- Soporte para `prefers-reduced-motion`.
- Foco visible en enlaces, botones, menú y formulario.
- Menú mobile con control de apertura, cierre, tecla Escape y estado `aria-expanded`.
- Estado de carga reservado para el envío del formulario.
- Errores legibles sin cambiar bruscamente el layout.
- Enlaces externos y WhatsApp identificables antes de activarlos.

## Estrategia responsive

La implementación será mobile-first y partirá de 320 px. Los breakpoints responderán al contenido, no a modelos de dispositivo.

Reglas obligatorias:

- `min-width: 0` en hijos de flex y grid.
- Columnas flexibles con `minmax(0, 1fr)`.
- Imágenes con ancho máximo del 100 % y proporción reservada.
- Tipografía y espaciado fluidos con límites explícitos.
- Conversión a flujo vertical antes de que el contenido quede comprimido.
- Menú, CTA, logos y texto sin posicionamiento que pueda superponerse.
- Ningún desplazamiento horizontal accidental.
- Compatibilidad con zoom del navegador y tamaños de fuente aumentados.

## Manejo de errores

- Si una imagen no carga, el contenedor conservará su proporción y mostrará un fondo neutro; el contenido seguirá siendo comprensible.
- Si JavaScript no está disponible, navegación, enlaces y formulario conservarán una alternativa funcional.
- Si WhatsApp no puede abrirse, el número permanecerá visible y copiable en Contacto.
- La validación del formulario no borrará valores ni dependerá únicamente del color.
- Los textos largos y nombres de equipos podrán envolver sin romper la retícula.

## Validación y pruebas

Se verificará el sitio completo en 320, 360, 390, 430, 768, 1024, 1280 y 1440 px.

La validación incluirá:

- Comprobación automática de que `scrollWidth` no supera el ancho visible.
- Capturas comparativas de todas las páginas en mobile y escritorio.
- Menú mobile, cierre por Escape y navegación por teclado.
- Estados de foco, error, carga y éxito.
- Formulario con datos válidos e inválidos.
- Enlaces internos, externos y WhatsApp.
- Proporción, nitidez, texto alternativo y carga de imágenes y logos.
- Contraste y orden semántico de encabezados.
- `prefers-reduced-motion`.
- Revisión de consola y recursos fallidos.

## Criterios de aceptación

El rediseño se considera aceptado cuando:

- Las cinco páginas comparten el mismo sistema visual y de navegación.
- La portada comunica servicio, ubicación y siguiente acción sin saturación.
- Mobile mantiene jerarquía y CTA accesible desde 320 px.
- No existen solapamientos, recortes indebidos, desbordamiento horizontal ni saltos de layout evitables.
- Los logos se ven nítidos, proporcionados y con zona de seguridad.
- El icono de WhatsApp es oficial, claro y accesible.
- Las imágenes tienen calidad suficiente y origen registrado.
- El contenido no contiene afirmaciones inventadas ni patrones repetitivos propios de una plantilla genérica.
- Las pruebas responsive, funcionales y de accesibilidad definidas pasan.

## Secuencia de implementación

1. Inventariar contenido, componentes e imágenes existentes.
2. Consolidar tokens, tipografía, espaciado, radios, contenedores y breakpoints.
3. Construir navegación, footer, botones, iconos e imágenes compartidas.
4. Rediseñar Inicio y validar el sistema en mobile antes de extenderlo.
5. Aplicar el sistema a Servicios, Casos, Tecnologías y Contacto.
6. Reducir y revisar el contenido página por página.
7. Integrar imágenes oficiales y registrar sus fuentes.
8. Ejecutar pruebas responsive, funcionales, de accesibilidad y rendimiento.
9. Corregir regresiones y realizar revisión visual final.
