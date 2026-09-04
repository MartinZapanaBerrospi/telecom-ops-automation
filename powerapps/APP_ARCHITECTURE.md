# 📱 Telecom Post-Billing Adjustment Manager
### Arquitectura Técnica & Diseño de la Aplicación en Microsoft Power Apps (Canvas App)

---

## 🎯 Objetivo de la Aplicación
Permitir a los analistas de **Soporte Operacional de Post Facturación** registrar, auditar y someter a aprobación solicitudes de ajustes (notas de crédito, cobros duplicados, devoluciones por interrupción de servicio y reclamos de datos móviles), integrando validaciones en tiempo real y conexión con Microsoft Power Automate.

---

## 🏛️ Estructura de Pantallas (Screens)

```
+-----------------------------------------------------------------------------+
|                           POST-BILLING APP FLOW                             |
+-----------------------------------------------------------------------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
         [DashboardScreen]                       [ApprovalQueueScreen]
         - Métricas del Ciclo                    - Bandeja de Jefatura
         - Lista de Solicitudes                  - Aprobación / Rechazo
         - Filtros por Estado                    - Historial de Auditoría
                   |                                       |
                   v                                       |
         [NewAdjustmentScreen]                             |
         - Búsqueda de Recibo / Cliente                    |
         - Validación de Consumos                          |
         - Carga de Sustentos (PDF/Img)                    |
         - Envío a Power Automate                          |
                   |                                       |
                   +-------------------+-------------------+
                                       |
                                       v
                             [DetailAuditScreen]
                             - Trazabilidad Completa
                             - Logs de Aprobación
```

---

## 🧩 Detalle de Componentes por Pantalla

### 1. `DashboardScreen` (Pantalla Principal)
* **Header Corporativo:** Logo corporativo del operador / Operaciones, foto de usuario activo y selector de ciclo (`C01`, `C15`, `C28`).
* **KPI Cards (Indicadores en tiempo real):**
  * *Total Solicitudes del Ciclo* (`CountRows(colAjustes)`)
  * *Monto Total en Disputa (S/)* (`Sum(colAjustes, MontoReclamado)`)
  * *Tasa de Aprobación %*
  * *Casos Pendientes de Jefatura*
* **Data Gallery (`galAjustes`):** Lista filtrable por Estado (*Pendiente*, *Aprobado*, *Rechazado*) y buscador por DNI/RUC o Número de Recibo.
* **Bóton Flotante CTA:** `+ Nueva Solicitud` (Navega a `NewAdjustmentScreen`).

### 2. `NewAdjustmentScreen` (Formulario de Registro)
* **Buscador de Factura:** Entrada de texto con validación de formato `F001-XXXXXXXX`. Al escribir, auto-rellena mediante `LookUp()` los datos del cliente, plan contratado y monto emitido.
* **Campos del Formulario:**
  * Tipo de Incidencia (Dropdown: *Sobrefacturación de Datos*, *Cargo Duplicado*, *Descuento no Aplicado*, *Falla Técnica*).
  * Monto Solicitado (S/).
  * Justificación Técnica (Texto multilínea, min. 20 caracteres).
  * Adjunto de Evidencia (Attachment control).
* **Validación Dinámica:** Si el monto solicitado supera el valor de la factura original, el botón "Enviar" se bloquea y muestra un banner de advertencia en rojo.

### 3. `ApprovalQueueScreen` (Bandeja Exclusiva de Jefatura)
* **Control de Roles:** Visible únicamente si el usuario pertenece al grupo de seguridad `M365_Jefatura_PostFacturacion`.
* **Acciones de Decisión:** Botón "Aprobar" (dispara flujo a SAP/Oracle) y "Rechazar" (requiere motivo obligatorio).

---

## 🎨 Paleta de Colores & Diseño UI (Estándar Telecom)
* **Primario:** Telecom Deep Blue (`#005A9E` / `RGBA(0, 90, 158, 1)`) o Crimson Corporate (`#DA291C`)
* **Secundario:** Deep Navy (`#0F172A`)
* **Background:** Clean White / Slate Light (`#F8FAFC`)
* **Success / Warning / Danger:** `#10B981` / `#F59E0B` / `#EF4444`
