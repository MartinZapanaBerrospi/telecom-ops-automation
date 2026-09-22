# Canvas App — `Telecom Post-Billing Adjustment Manager`

La aplicación que usa el analista de post-facturación para registrar un ajuste y mandarlo
a aprobación.

> **Estado: especificación.** La app no está desplegada en ningún tenant. Lo que hay aquí
> es su arquitectura, sus fórmulas Power Fx y su metadato de definición, en detalle
> suficiente para reconstruirla. Ver [cómo construirla](../docs/03-deployment-guide.md#b2--construir-la-canvas-app).

![Pantalla de nueva solicitud](../docs/assets/app-new-adjustment.svg)

---

## Archivos

| Archivo | Contenido |
|---|---|
| [`app-architecture.md`](app-architecture.md) | Las cuatro pantallas, sus controles, el modelo de estado y la paleta de colores |
| [`power-fx-formulas.md`](power-fx-formulas.md) | Las fórmulas Power Fx de cada propiedad: `App.OnStart`, búsqueda de recibo, envío de solicitud y filtrado de galería |
| [`app-definition.json`](app-definition.json) | Metadato de la app: orígenes de datos y componentes reutilizables |

---

## Las cuatro pantallas

| Pantalla | Quién la usa | Qué hace |
|---|---|---|
| `DashboardScreen` | Analista | KPIs del ciclo y galería filtrable de solicitudes |
| `NewAdjustmentScreen` | Analista | Formulario de registro con validación en tiempo real y disparo del flujo |
| `ApprovalQueueScreen` | Jefatura | Bandeja de pendientes, con aprobación y rechazo (motivo obligatorio) |
| `DetailAuditScreen` | Ambos | Trazabilidad de una solicitud: quién, cuándo, con qué justificación |

---

## Lo que la app valida antes de guardar

Éste es el punto del diseño que más importa: la app **no** deja que una solicitud inválida
llegue a la bandeja de la jefatura. Antes del `Patch()` comprueba, en este orden:

1. Que el número de recibo exista en `FacturasEmitidas` (regla **R5**).
2. Que el monto solicitado sea mayor que cero.
3. Que el monto no supere el `MontoTotal` de la factura original (regla **R1**).
4. Que la justificación tenga al menos 15 caracteres.

Si algo falla, muestra el banner y bloquea el botón de envío. Si todo pasa, guarda la
solicitud y dispara el flujo de aprobación.

> Las reglas completas están en [`docs/01-business-rules.md`](../docs/01-business-rules.md).
> Si cambias un tope aquí, cámbialo también en ese documento, en
> `powerautomate/definitions/approval-flow.json` y en `src/automation_engine.py`.

---

## Convenciones de nombres

Los controles siguen el prefijo estándar de Power Apps, y las fórmulas del repositorio los
usan literalmente. Si al construir la app les pones otros nombres, tendrás que ajustar las
fórmulas.

| Prefijo | Tipo de control | Ejemplo |
|---|---|---|
| `txt` | Entrada de texto | `txtNumeroRecibo`, `txtMontoSolicitado` |
| `drp` | Desplegable | `drpTipoIncidencia`, `drpFiltroEstado` |
| `btn` | Botón | `btnEnviarSolicitud` |
| `gal` | Galería | `galAjustes` |
| `col` | Colección | `colAjustes`, `colCiclos` |
| `var` | Variable global o de contexto | `varMontoOriginal`, `varIsJefatura` |
