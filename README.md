# jesareko_landing

Landing corporativa estática de Jesareko, empresa de servicios tecnológicos en Paraguay con foco en infraestructura IT, redes y WiFi, CCTV, automatización, páginas web, monitoreo y soporte técnico.

El proyecto esta preparado para publicarse como sitio estatico en GitHub y Cloudflare Pages sin build command y con directorio de salida `/public`.

Solo `public/` se publica. La documentacion y las configuraciones alternativas de servidor permanecen fuera del sitio accesible. CSS y JavaScript se mantienen en una unica version legible; Cloudflare aplica compresion en la entrega.

Nota de seguridad: el código frontend no puede ocultarse totalmente, porque HTML, CSS y JavaScript se entregan al navegador. Este proyecto usa minificación y configuraciones de headers/CDN para reducir exposición casual y endurecer el despliegue, pero no debe contener secretos, tokens ni credenciales.
