# ⏰ Flujo 2: Distribución Programada de Reportes de Facturación
### Power Automate Cloud Flow: `Flow_Distribucion_Diaria_Reporte_Operacional`

---

## 🎯 Descripción
Flujo con **Disparador Recurrente (Recurrence Trigger)** programado de Lunes a Viernes a las **08:00 AM (Hora de Lima - PET)**.

### Pasos del Flujo:
1. **Trigger:** Recurrencia `Lunes a Viernes a las 08:00`.
2. **Ejecución / Extracción:** Llama al script Python / API que genera el archivo `Reporte_Operacional_PostFacturacion.xlsx`.
3. **Lectura de KPIs:** Obtiene los valores de:
   * Facturación Emitida del Día.
   * Tasa de Cobranza %.
   * Casos en Disputa.
4. **Envío de Correo HTML:** Envía correo corporativo a `jefatura.postfacturacion@telecom.com` con el reporte adjunto y tabla resumen en HTML.
5. **Mensaje a Microsoft Teams:** Publica mensaje informativo en el canal *#Soporte-Operaciones-Facturacion*.
