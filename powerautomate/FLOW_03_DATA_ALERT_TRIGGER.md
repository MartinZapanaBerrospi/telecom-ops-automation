# ⚡ Flujo 3: Alerta en Tiempo Real por Descuadre de Facturación
### Power Automate Cloud Flow: `Flow_Alerta_Descuadre_Ciclo`

---

## 🎯 Descripción
Disparador HTTP Webhook (`When an HTTP request is received`). Cuando el pipeline de Python o el procedimiento almacenado en Oracle detecta más de **5% de descuadres en un ciclo**, envía un POST con el lote afectado.

### Payload recibido:
```json
{
  "codigoCiclo": "C15",
  "periodo": "2026-08",
  "facturasAfectadas": 142,
  "montoDiscrepancia": 8450.20,
  "motivo": "Desfase en tasación de paquete Roaming Internacional"
}
```

### Acción Automática:
* Crea una tarjeta urgente en Teams etiquetando al analista de guardia.
* Bloquea preventivamente la emisión del ciclo en el sistema comercial.
