# Código Python

Es la parte **ejecutable** del repositorio. Existe por una razón concreta: las reglas de
aprobación están descritas en documentos y especificadas en Power Fx, pero un documento no
se puede probar. Aquí las mismas reglas están implementadas en Python y cubiertas por
pruebas, de modo que se pueden verificar sin desplegar nada en un tenant de Microsoft 365.

---

## Los tres scripts

| Orden | Script | Entrada | Salida |
|---|---|---|---|
| 1 | [`generate_seed_data.py`](generate_seed_data.py) | — (datos ficticios en el código) | `data/FacturasEmitidas.xlsx`, `data/AjustesPostFacturacion.xlsx` |
| 2 | [`automation_engine.py`](automation_engine.py) | Los dos `.xlsx` anteriores | `data/BitacoraDecisiones.csv` |
| 3 | [`excel_report_styler.py`](excel_report_styler.py) | Los `.xlsx` y la bitácora | `data/Reporte_Gerencial_Facturacion.xlsx` |

```bash
python src/generate_seed_data.py
python src/automation_engine.py
python src/excel_report_styler.py
pytest tests/ -q
```

El orden importa: cada script consume lo que produjo el anterior.

---

## `automation_engine.py` — el motor de reglas

Es el archivo que vale la pena leer. Tiene dos funciones y un `dataclass`:

| Elemento | Responsabilidad |
|---|---|
| `evaluar_solicitud(...)` | **Función pura.** Recibe una solicitud y el monto de su factura, y devuelve un `Decision`. No lee archivos ni escribe nada. Es la que prueban los tests |
| `procesar_bandeja(...)` | Lee los `.xlsx`, aplica `evaluar_solicitud` a cada fila y escribe la bitácora |
| `Decision` | `dataclass` inmutable con el dictamen: estado, aprobador responsable y motivo legible |

La separación entre las dos funciones es deliberada: **la lógica de negocio no toca disco**.
Por eso las reglas se pueden probar con una llamada, sin archivos de por medio ni datos de
ejemplo que mantener:

```python
>>> from automation_engine import evaluar_solicitud
>>> evaluar_solicitud("AJU-TEST", "F001-00000001", 120.00, 1000.00).estado
'PENDIENTE_JEFATURA'
```

### Los topes viven en dos constantes

```python
TOPE_AUTOAPROBACION = 50.00   # regla R2
TOPE_JEFATURA       = 500.00  # reglas R3 y R4
```

Están en la cabecera del módulo, no repartidas por el código, para que cambiar una regla
sea cambiar una línea. Los mismos valores aparecen en la Canvas App y en el flujo de
aprobación: cámbialos en los tres lugares y en
[`docs/01-business-rules.md`](../docs/01-business-rules.md).

---

## `generate_seed_data.py` — datos de prueba

Construye los dos datasets ficticios desde listas literales. No usa datos aleatorios a
propósito: los mismos 10 recibos y las mismas 4 solicitudes en cada corrida, para que el
resultado del motor sea reproducible y las pruebas no dependan del azar.

Todos los datos son inventados. Empresas, personas, documentos de identidad y montos no
corresponden a ningún cliente real.

---

## `excel_report_styler.py` — reporte para jefatura

Toma la bitácora y los datasets, calcula los indicadores del ciclo y los escribe en un
Excel con formato corporativo (encabezados, semáforo de cumplimiento, anchos de columna).
Es el archivo que el flujo 02 distribuiría por correo cada mañana.

Las cifras que muestra **se derivan de los datos del repositorio**, no están escritas a
mano: si cambias los datasets, el reporte cambia.

---

## Por qué no hay conexión con Power Platform

El motor no consume las APIs de Dataverse ni dispara los flujos. Reproduce las reglas
localmente, y esa es exactamente su utilidad: permite verificar que la implementación en
Power Fx respeta las mismas reglas, comparando el estado que asigna la app contra el que
escribe la bitácora. El procedimiento está en
[`docs/03-deployment-guide.md`](../docs/03-deployment-guide.md#b4--verificar-contra-el-motor-de-python).

---

## Pruebas

Las pruebas están en [`../tests/test_reglas_aprobacion.py`](../tests/test_reglas_aprobacion.py)
y cubren cada regla más los bordes exactos de los topes (S/ 50.00 y S/ 500.00), que es
donde una implementación se desvía sin que nadie lo note.

```bash
pytest tests/ -q
```
