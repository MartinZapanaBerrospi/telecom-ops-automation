# Flujo 03 — Alerta por descuadre de ciclo

**Nombre:** `Flow_Alerta_Descuadre_Ciclo`
**Disparador:** Webhook HTTP (*When an HTTP request is received*)
**Definición:** no tiene JSON aparte; su lógica cabe entera en este documento.

Es el único flujo que no parte de una acción de una persona. Lo dispara el pipeline de
datos cuando detecta que un ciclo de facturación cerró con más de **5% de descuadres**
entre lo tasado y lo facturado.

---

## Payload que recibe

```json
{
  "codigoCiclo": "C15",
  "periodo": "2026-08",
  "facturasAfectadas": 142,
  "montoDiscrepancia": 8450.20,
  "motivo": "Desfase en tasación de paquete Roaming Internacional"
}
```

---

## Pasos

1. **Disparador HTTP.** Recibe el POST del pipeline con el lote afectado.
2. **Evaluar severidad.** Compara `montoDiscrepancia` contra el umbral de escalamiento.
3. **Publicar tarjeta urgente en Teams**, etiquetando al analista de guardia del ciclo.
4. **Notificar por correo** a la jefatura, con el detalle del lote.
5. **Marcar el ciclo para revisión** en la tabla de control, de modo que la app lo muestre
   señalado antes de que alguien registre ajustes sobre recibos de ese lote.

---

## Detalles que importan al construirlo

- **El webhook es una URL con secreto en el query string.** Cualquiera que la tenga puede
  disparar el flujo. En producción debe ir detrás de autenticación, no expuesta.
- **Un lote puede disparar la alerta varias veces.** Sin deduplicación por
  `codigoCiclo` + `periodo`, un pipeline que reintenta genera una tarjeta por reintento.
- **Bloquear la emisión del ciclo no está modelado.** Sería la acción realmente valiosa,
  pero exige escribir en el sistema comercial, que queda fuera del alcance de este
  proyecto.
