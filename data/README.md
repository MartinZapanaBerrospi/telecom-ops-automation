# Datos

Todos los datos de esta carpeta son **ficticios**. Empresas, personas, documentos de
identidad, planes y montos fueron inventados para el ejercicio y no corresponden a ningún
cliente real ni a ningún operador de telecomunicaciones.

La descripción completa de columnas, tipos y relaciones está en
[`docs/02-data-model.md`](../docs/02-data-model.md).

---

## Qué hay aquí

| Archivo | Rol | ¿Versionado? |
|---|---|---|
| `FacturasEmitidas.xlsx` | **Entrada.** Maestro de facturas: 10 recibos con su cliente, plan y monto | Sí |
| `AjustesPostFacturacion.xlsx` | **Entrada.** Bandeja de solicitudes: 4 reclamos esperando dictamen | Sí |
| `BitacoraDecisiones.csv` | **Salida** de `src/automation_engine.py`: el dictamen de cada solicitud | No |
| `Reporte_Gerencial_Facturacion.xlsx` | **Salida** de `src/excel_report_styler.py`: el reporte con formato para jefatura | No |

Los dos archivos de entrada están versionados a propósito: permiten abrir el proyecto y
entender los datos sin instalar nada ni ejecutar Python. Las salidas están en
[`.gitignore`](../.gitignore) porque se regeneran en cada corrida.

---

## Regenerar todo

```bash
python src/generate_seed_data.py     # reconstruye los dos .xlsx de entrada
python src/automation_engine.py      # produce BitacoraDecisiones.csv
python src/excel_report_styler.py    # produce el reporte con formato
```

Los datos de entrada son fijos, no aleatorios: cada corrida produce exactamente los mismos
10 recibos y las mismas 4 solicitudes, para que el resultado del motor de reglas sea
reproducible.

---

## Estos archivos son el origen de las tablas en Power Platform

En un despliegue real, `FacturasEmitidas.xlsx` y `AjustesPostFacturacion.xlsx` se importan
como tablas de Dataverse (o como listas de SharePoint) conservando los nombres de columna
tal cual, porque las fórmulas Power Fx del repositorio los usan literalmente. El
procedimiento está en
[`docs/03-deployment-guide.md`](../docs/03-deployment-guide.md#b1--cargar-los-datos).
