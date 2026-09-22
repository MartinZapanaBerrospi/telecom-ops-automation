# Flujo 01 — Aprobación de ajustes

**Nombre:** `Flow_Aprobacion_Ajuste_PostFacturacion`
**Disparador:** Power Apps (`PowerApps.Run()` desde `btnEnviarSolicitud`)
**Definición:** [`definitions/approval-flow.json`](definitions/approval-flow.json)

Es el flujo que convierte una solicitud de ajuste en una decisión trazable. Implementa las
reglas **R2, R3 y R4** de [`docs/01-business-rules.md`](../docs/01-business-rules.md);
las reglas R1 y R5 ya las validó la app antes de llamarlo.

---

## Parámetros de entrada

Los envía la Canvas App en el orden en que aparecen en
[`powerapps/power-fx-formulas.md`](../powerapps/power-fx-formulas.md):

| Parámetro | Tipo | Ejemplo |
|---|---|---|
| `IdAjuste` | Texto | `AJU-2026-003` |
| `NumeroRecibo` | Texto | `F001-00045218` |
| `ClienteNombre` | Texto | `Corporación Minera Pampa Azul S.A.C.` |
| `MontoSolicitado` | Decimal | `145.50` |
| `TipoIncidencia` | Texto | `DESCUENTO_NO_APLICADO` |
| `Analista` | Texto | `Martín Zapana Berrospi` |

---

## Pasos

1. **Disparador.** Recibe los seis parámetros desde la app.
2. **Condición de monto** (`Check_Amount_Threshold`):
   - **≤ S/ 50.00** → aprobación automática. Escribe `APROBADO_AUTO`, iguala
     `MontoReconocido` a `MontoReclamado` y salta al paso 5. *(regla R2)*
   - **S/ 50.01 – S/ 500.00** → tarjeta adaptable a la jefatura. *(regla R3)*
   - **> S/ 500.00** → tarjeta adaptable a gerencia. *(regla R4)*
3. **Tarjeta adaptable.** Acción *Post adaptive card and wait for a response* sobre
   Microsoft Teams, con el payload de más abajo. El flujo queda en espera.
4. **Respuesta humana.** Según el botón pulsado, escribe `APROBADO_JEFATURA` /
   `APROBADO_GERENCIA` o `RECHAZADO`, junto con el comentario del aprobador. El comentario
   es obligatorio al rechazar.
5. **Bitácora.** Registra el dictamen con `IdAjuste`, estado, aprobador, motivo y fecha.
6. **Notificación al analista.** Correo con el resultado y el comentario del aprobador.

> Los topes de S/ 50.00 y S/ 500.00 son los mismos que valida la Canvas App y que prueba
> `tests/test_reglas_aprobacion.py`. Están definidos en un solo lugar:
> [`docs/01-business-rules.md`](../docs/01-business-rules.md).

---

## Payload de la tarjeta adaptable

Se muestra maquetada en
[`docs/assets/teams-adaptive-card.svg`](../docs/assets/teams-adaptive-card.svg).

```json
{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "Solicitud de ajuste de post facturación",
      "weight": "Bolder",
      "size": "Medium",
      "color": "Attention"
    },
    {
      "type": "TextBlock",
      "text": "Supera el tope de autoaprobación de S/ 50.00 (regla R3).",
      "wrap": true,
      "isSubtle": true
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Recibo:", "value": "@{triggerBody()?['NumeroRecibo']}" },
        { "title": "Cliente:", "value": "@{triggerBody()?['ClienteNombre']}" },
        { "title": "Monto solicitado:", "value": "S/ @{triggerBody()?['MontoSolicitado']}" },
        { "title": "Incidencia:", "value": "@{triggerBody()?['TipoIncidencia']}" },
        { "title": "Analista:", "value": "@{triggerBody()?['Analista']}" }
      ]
    },
    {
      "type": "Input.Text",
      "id": "txtComentarioJefatura",
      "placeholder": "Ingrese observaciones de aprobación o motivo de rechazo...",
      "isMultiline": true
    }
  ],
  "actions": [
    {
      "type": "Action.Submit",
      "title": "Aprobar ajuste",
      "style": "positive",
      "data": { "decision": "APROBADO" }
    },
    {
      "type": "Action.Submit",
      "title": "Rechazar",
      "style": "destructive",
      "data": { "decision": "RECHAZADO" }
    }
  ]
}
```

---

## Detalles que importan al construirlo

- **Usa *Post adaptive card and wait for a response*, no *Post card*.** La segunda envía la
  tarjeta y sigue de largo; el flujo necesita esperar la decisión.
- **El rechazo exige comentario.** `Input.Text` no lo puede forzar: hay que validarlo en el
  flujo después del `Submit` y reenviar la tarjeta si viene vacío.
- **La tarjeta caduca.** Si nadie responde, el flujo queda en espera indefinidamente.
  Un escalamiento por tiempo sería la extensión natural, y hoy no está modelado
  ([supuestos del modelo](../docs/01-business-rules.md#6-supuestos-del-modelo)).
- **`MontoReconocido` puede diferir de `MontoReclamado`.** El modelo de datos lo permite
  (aprobación parcial), pero este flujo no lo implementa: aprueba el monto completo o
  rechaza.
