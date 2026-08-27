# 📋 Blueprint Operacional: Automatización de Post Facturación

```
  +-----------------------+
  |  Analista de Soporte  |
  +-----------+-----------+
              | (1) Ingresa Solicitud y Reclamo
              v
  +-----------------------+
  |   Canvas Power App    | ---> Valida Formato de Recibo y Topes
  +-----------+-----------+
              | (2) Dispara Flujo Cloud
              v
  +-----------------------+
  |    Power Automate     |
  +-----------+-----------+
              |
              +----> Si Monto <= S/ 30.00: Auto-aprueba
              |
              +----> Si Monto > S/ 30.00:
                     Envia Adaptive Card a MS Teams / Correo
                     a la Jefatura de Post Facturación
              |
              v
  +-----------------------+
  |   Decisión Jefatura   | ---> [ ✅ APROBADO ] / [ ❌ RECHAZADO ]
  +-----------+-----------+
              |
              v
  +-----------------------+
  |  Oracle DB / SAP ERP  | ---> Aplica Nota de Crédito & Notifica al Analista
  +-----------------------+
```
