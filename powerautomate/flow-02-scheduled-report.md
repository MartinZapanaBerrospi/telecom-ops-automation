# Flujo 02 — Reporte operacional programado

**Nombre:** `Flow_Distribucion_Diaria_Reporte_Operacional`
**Disparador:** Recurrencia, lunes a viernes a las 08:00 (hora de Lima, UTC-5)
**Definición:** [`definitions/report-distribution-flow.json`](definitions/report-distribution-flow.json)

No implementa reglas de negocio: es distribución. Toma el reporte del día y lo pone
delante de quien debe leerlo, sin que nadie tenga que pedirlo.

---

## Pasos

1. **Disparador de recurrencia.** Lunes a viernes, 08:00, zona horaria
   `SA Pacific Standard Time`. Los fines de semana no hay ciclo que reportar.
2. **Obtener el reporte.** Recupera `Reporte_Gerencial_Facturacion.xlsx`, el archivo que
   genera [`src/excel_report_styler.py`](../src/excel_report_styler.py) con los
   indicadores del día anterior.
3. **Leer los KPIs de cabecera** para el cuerpo del correo:
   - Facturación emitida
   - Efectividad de cobranza
   - Monto en ajustes y notas de crédito
   - Casos pendientes de aprobación
4. **Enviar correo HTML** a la jefatura, con la tabla resumen en el cuerpo y el Excel
   adjunto. El resumen en el cuerpo importa: se lee desde el celular, sin abrir el adjunto.
5. **Publicar en Teams**, en el canal `#Soporte-Operaciones-Facturacion`.

---

## Detalles que importan al construirlo

- **La zona horaria se declara en el disparador, no se asume.** `SA Pacific Standard
  Time` es Lima. Un flujo sin zona horaria corre en UTC y llega a las 03:00.
- **El Excel tiene que existir antes de las 08:00.** El flujo no lo genera: lo lee. Quien
  lo produce es el paso previo del pipeline; si falla, el flujo envía un adjunto viejo sin
  avisar. Una comprobación de la fecha de modificación del archivo sería lo correcto y hoy
  no está modelada.
- **Los destinatarios son de ejemplo.** Ver la tabla de
  [cuentas y canales](README.md#cuentas-y-canales-de-ejemplo).
