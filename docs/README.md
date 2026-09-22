# Documentación

Tres documentos, en orden de lectura. Si sólo vas a leer uno, lee el primero.

| # | Documento | Qué responde |
|---|---|---|
| 01 | [Proceso y reglas de negocio](01-business-rules.md) | Qué problema se resuelve, cuáles son las reglas R1–R5 y en qué estado queda cada solicitud. **Es la fuente de verdad del proyecto.** |
| 02 | [Modelo de datos](02-data-model.md) | Qué tablas hay, qué columnas tienen y cómo se relacionan |
| 03 | [Guía de despliegue](03-deployment-guide.md) | Cómo mostrarlo sin desplegar nada, cómo construirlo en un tenant gratuito y cómo dejar el repositorio importable (`.zip` de solución y fórmulas legibles en GitHub) |

## `assets/`

Maquetas en SVG de las pantallas de la app y de la tarjeta adaptable en Teams. Existen
porque una Canvas App no se puede leer desde GitHub: el `.msapp` es un archivo comprimido
y el flujo vive en la nube. Las maquetas cubren ese hueco mientras el proyecto no esté
desplegado.

| Archivo | Qué muestra |
|---|---|
| [`app-dashboard.svg`](assets/app-dashboard.svg) | `DashboardScreen`: KPIs del ciclo y galería de solicitudes con sus estados |
| [`app-new-adjustment.svg`](assets/app-new-adjustment.svg) | `NewAdjustmentScreen`: la regla R1 bloqueando un ajuste mayor que la factura |
| [`teams-adaptive-card.svg`](assets/teams-adaptive-card.svg) | La tarjeta adaptable que recibe la jefatura para aprobar o rechazar |

Si algún día construyes la app en un tenant, reemplaza estos SVG por capturas reales
—instrucciones en [`03-deployment-guide.md`](03-deployment-guide.md#b5--capturar-la-evidencia)—
y actualiza el README raíz.
