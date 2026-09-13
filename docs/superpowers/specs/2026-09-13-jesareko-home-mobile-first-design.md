# Mejora visual mobile-first de la Home de Jesareko

## Objetivo y alcance

Elevar únicamente `/` para que comunique infraestructura técnica instalada con mayor impacto, ritmo y confianza. Se conservan la marca, los textos esenciales, las rutas, los CTA de WhatsApp, el sistema tipográfico Inter/Merriweather y la paleta verde de Jesareko. No se alterará visualmente ninguna ruta fuera de la Home.

La experiencia parte desde pantallas de 320 px y amplía la composición para tablet y escritorio. No habrá una versión de escritorio encogida para móvil ni interacciones esenciales dependientes de hover.

## Estructura y componentes

`public/index.html` conservará la secuencia semántica de hero, servicios, tecnología, proceso, aplicaciones y CTA. Se ampliarán únicamente los bloques de la Home con clases locales y CSS en `public/assets/css/styles.css`; `main.js` solo añadirá comportamiento de animación no esencial si resulta necesario. Los enlaces y anclas existentes permanecen sin cambios.

### Hero

El hero mantiene ubicación, H1, explicación y CTA. En móvil presenta ese contenido primero y una foto local a continuación, con relación de aspecto reservada, sin texto sobre la imagen. A partir de tablet usa dos columnas: copy de lectura rápida y una imagen que ocupa aproximadamente 45–55% sin comprometer el tamaño del CTA ni la legibilidad.

La imagen será el LCP: local, declarada con dimensiones, `fetchpriority="high"`, sin carga diferida y con variantes responsive si su formato final lo justifica. El tratamiento visual reutiliza el encuadre, radio y sobriedad de Tecnologías.

### Servicios

Los tres enlaces existentes pasan a tarjetas grandes y completas: identificador, foto, título, conceptos técnicos y señal direccional. En móvil se apilan a ancho casi total y mantienen foto y CTA claramente visibles. Desde el ancho que permita títulos y metadatos cómodos, se convierten en tres columnas editoriales equivalentes. Cada tarjeta sigue siendo un único enlace accesible a su ancla de Servicios.

No se introducen carruseles, JavaScript adicional ni contenido inventado.

### Tecnología aplicada: pieza de identidad

`Tecnología aplicada` se convierte en una pieza de identidad de fondo verde oscuro, no solo una superficie recoloreada. Combinará: titular y explicación en alto contraste; tres capacidades —redes, seguridad e infraestructura documentada—; indicadores de estado descriptivos; y un pequeño diagrama de topología formado con CSS/SVG semánticamente decorativo. Su composición debe sugerir orden, conexión y mantenimiento sin parecer dashboard, hacker o interfaz de operaciones.

El bloque conserva lectura lineal en móvil. En escritorio, copy y la topología/capacidades se disponen en retícula. Los indicadores no comunican estado real ni datos operativos: son refuerzos visuales de conceptos ya expresados en texto.

## Dirección fotográfica

Se generarán cuatro fotografías originales y locales: hero, Redes y WiFi, Seguridad física/CCTV y Soporte/documentación. Pertenecerán a una única serie: fotografía documental comercial realista, instalaciones ordenadas, luz diurna natural suavizada, interiores empresariales sobrios, verde y gris de baja saturación, profundidad de campo moderada y ausencia de personas protagonistas.

Cada imagen excluirá texto, logotipos, marcas falsas, visuales futuristas, estética hacker/cyberpunk y stock genérico. Las composiciones dejarán área limpia donde el recorte responsive pueda cambiar sin ocultar el equipo principal. Las imágenes de servicios se cargarán de forma diferida y tendrán ancho, alto y `object-fit` declarados para evitar CLS. Se almacenarán como nuevos assets con nombre específico sin sustituir imágenes existentes; la procedencia y procesamiento se documentarán.

## Movimiento e interacción

Se separan dos niveles de movimiento:

1. Interacción rápida, 160–220 ms: borde, elevación de hasta 3 px, flecha y escala de foto máxima de 1.04 en tarjetas; se activa solo con hover capaz o foco visible.
2. Movimiento ambiental lento, entre 1.8 y 3.5 s y sin bucle distractor: un pulso muy tenue de nodo o trazo de topología únicamente dentro de Tecnología aplicada. Nunca desplaza contenido ni representa actividad real.

Las revelaciones de scroll deben conservar el contenido visible por defecto. `prefers-reduced-motion: reduce` suprime las transiciones no esenciales, escalados y movimiento ambiental.

## Sistema visual, accesibilidad y rendimiento

Se reutilizan tokens de color, tipo, radios y espacio actuales. Solo se añadirán tokens de Home necesarios para superficies oscuras y nodos, con contraste WCAG AA, foco visible y tamaño mínimo de control de 48 px. Las fotos tendrán texto alternativo útil; los elementos de topología puramente ornamentales usarán `aria-hidden`.

No se añadirán dependencias. La carga local de fuentes e imágenes se mantendrá; las fotos se optimizarán a formato web moderno cuando sea posible sin introducir una herramienta de producción. El hero tendrá prioridad y las tarjetas carga diferida. Las relaciones de aspecto declaradas reservan espacio antes de la descarga.

## Error handling

Si una foto no carga, su contenedor conserva proporción y presenta una superficie neutra; ningún texto crítico depende de ella. Con JavaScript desactivado, los enlaces, CTA y todo el contenido continúan disponibles. Las animaciones son opcionales.

## Validación

Se validarán la Home y sus enlaces en 320, 375, 390, 430, 768, 1024, 1280, 1440 y una vista grande. Además, se incluirán puntos intermedios adyacentes a cada cambio de composición y una barrida continua de anchos para detectar overflow, cortes, cambios bruscos de jerarquía o tarjetas comprimidas.

La validación cubrirá capturas antes/después, navegador real, consola y recursos, DOM, árbol de accesibilidad, foco y teclado, menú móvil, CTA y enlaces, hover cuando corresponda, `prefers-reduced-motion`, `scrollWidth`, dimensiones y carga de imágenes. Se ejecutarán las pruebas contractuales existentes y revisión final de CSS para confirmar que no hay cambios visuales en otras rutas.

## Criterios de aceptación

- La Home logra una jerarquía inequívoca desde 320 px y conserva una composición editorial en escritorio.
- Hero y tres servicios emplean las cuatro fotos nuevas de la misma serie visual.
- Tecnología aplicada funciona como una firma visual oscura, legible y técnica.
- Las microinteracciones diferencian respuesta rápida y ambiente lento, y respetan movimiento reducido.
- No se rompe navegación, CTA, anclas, responsividad, accesibilidad ni rendimiento de forma significativa.
