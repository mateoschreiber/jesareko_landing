# jesareko_landing

Landing estática de Jesareko, negocio de servicios tecnológicos en Paraguay con foco en diagnóstico, instalación, integración y soporte de redes WiFi, CCTV, alarmas, control de acceso, detección de incendio, monitoreo y presencia web.

El proyecto esta preparado para publicarse como sitio estatico en GitHub y Cloudflare Pages sin build command y con directorio de salida `/public`.

Solo `public/` se publica. La documentacion y las configuraciones alternativas de servidor permanecen fuera del sitio accesible. CSS y JavaScript se mantienen en una unica version legible; Cloudflare aplica compresion en la entrega.

Nota de seguridad: el código frontend no puede ocultarse totalmente, porque HTML, CSS y JavaScript se entregan al navegador. La compresión se delega al CDN y las cabeceras endurecen el despliegue, pero el proyecto no debe contener secretos, tokens ni credenciales.
