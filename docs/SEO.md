# Plan SEO de Jesareko

## Implementado

- URLs canónicas limpias sin extensión: `/servicios`, `/casos`, `/tecnologias`, `/contacto` y `/privacidad`.
- Redirecciones permanentes desde las URLs `.html` y manejo uniforme sin barra final.
- Sitemap, enlaces internos, Open Graph y JSON-LD alineados con las URLs públicas finales.
- Títulos y descripciones orientados a WiFi, CCTV, alarmas, soporte técnico, Encarnación e Itapúa.
- Imagen social raster de 1200 × 630 px y tarjetas sociales grandes.
- Entidad `Organization` y `WebSite` con áreas de servicio y atención personalizada.
- Sin dirección física, coordenadas, horarios, perfil de Google Business ni reseñas inventadas.
- Cobertura declarada: Encarnación, Carmen del Paraná, Cambyretá, Capitán Miranda, Hohenau, Obligado, Bella Vista y zonas cercanas de Itapúa.

## Acciones externas después del despliegue

1. Crear en Cloudflare un Bulk Redirect `301` de `www.jesareko.com` a `https://jesareko.com`, preservando ruta y parámetros.
2. Verificar que HTTP, HTTPS y `www` converjan en una sola URL sin cadenas de redirección.
3. Registrar el dominio en Google Search Console y enviar `https://jesareko.com/sitemap.xml`.
4. Inspeccionar `/`, `/servicios`, `/casos`, `/tecnologias` y `/contacto` después de publicar.
5. Medir impresiones, consultas, CTR y clics a WhatsApp/correo antes de ampliar contenido.

## Próximas fases, solo con información real

- Crear páginas individuales por servicio cuando exista contenido suficiente y diferenciado.
- Publicar casos reales anonimizados con problema, alcance y resultado verificable.
- Agregar dirección, coordenadas y horarios al schema solo cuando exista un local o una política pública definida.
- Vincular Google Business mediante `sameAs` solo después de crear y verificar el perfil.
- Incorporar reseñas únicamente con autorización y evidencia auténtica; no generar valoraciones ficticias.
