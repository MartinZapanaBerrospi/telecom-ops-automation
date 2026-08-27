# 🔄 Flujo 1: Sistema de Aprobación Automatizado con Adaptive Cards
### Power Automate Cloud Flow: `Flow_Aprobacion_Ajuste_PostFacturacion`

---

## 🎯 Descripción
Cuando un analista registra una solicitud de ajuste o nota de crédito desde **Power Apps**, este flujo:
1. Evalúa el monto solicitado.
2. Si es **menor o igual a S/ 30.00**, se auto-aprueba y genera la nota de crédito automáticamente.
3. Si es **mayor a S/ 30.00**, genera una **Tarjeta Adaptable interactiva (Adaptive Card)** enviada a Microsoft Teams y un correo a la Jefatura con botones de *Aprobar* y *Rechazar*.
4. Al recibir la respuesta, actualiza el estado en la base de datos Oracle y notifica al analista.

---

## 📐 Payload de la Tarjeta Adaptable (Adaptive Card JSON)

```json
{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "🚨 Solicitud de Ajuste de Post Facturación",
      "weight": "Bolder",
      "size": "Medium",
      "color": "Attention"
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Recibo:", "value": "@{triggerBody()?['NumeroRecibo']}" },
        { "title": "Cliente:", "value": "@{triggerBody()?['ClienteNombre']}" },
        { "title": "Monto Solicitado:", "value": "S/ @{triggerBody()?['MontoSolicitado']}" },
        { "title": "Incidencia:", "value": "@{triggerBody()?['TipoIncidencia']}" },
        { "title": "Analista Solicitante:", "value": "@{triggerBody()?['Analista']}" }
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
      "title": "✅ Aprobar Ajuste",
      "style": "positive",
      "data": { "decision": "APROBADO" }
    },
    {
      "type": "Action.Submit",
      "title": "❌ Rechazar",
      "style": "destructive",
      "data": { "decision": "RECHAZADO" }
    }
  ]
}
```
