# Cómo llevarlo a Power Platform (y cómo mostrarlo)

Este repositorio contiene **especificaciones**, no una solución exportada. Esta guía
explica las dos cosas que un lector puede querer hacer con ellas: construir la solución en
un tenant real, y —el caso más común— entender o demostrar el proyecto sin construir nada.

---

## Parte A — El problema de mostrar un proyecto de Power Platform

Power Apps y Power Automate no se leen como código. Una app de lienzo vive dentro de un
archivo `.msapp` comprimido y un flujo vive en la nube: subir esos archivos a GitHub no le
muestra nada a quien los mire. Por eso este repositorio se apoya en cuatro capas, de menos
a más esfuerzo:

| Capa | Qué comunica | Estado |
|---|---|---|
| **1. Diagramas en Mermaid** | El proceso, las reglas, el modelo de datos | Listo — GitHub los renderiza solo |
| **2. Maquetas SVG** de las pantallas | Cómo se ve y se usa la app | Listo — [`assets/`](assets/) |
| **3. Código Power Fx y definiciones JSON** | Que el diseño es concreto y no una idea vaga | Listo — `powerapps/`, `powerautomate/` |
| **4. Motor de reglas en Python + pruebas** | Que las reglas **funcionan**, no solo están descritas | Listo — `src/`, `tests/` |
| **5. Capturas de la app real** | Prueba de que se construyó | Pendiente — requiere la Parte B |

Las capas 1 a 4 ya están en el repositorio y son lo que hace legible el proyecto sin
tenant. La capa 5 es la única que exige desplegar, y la Parte B explica cómo hacerlo gratis.

> **Recomendación.** Si el objetivo es un portafolio, lo que más pesa es la capa 5: dos o
> tres capturas de la app funcionando, más un GIF corto de la tarjeta adaptable llegando a
> Teams. Un **Developer Plan** de Power Platform es gratuito y alcanza de sobra para esto.

---

## Parte B — Construirlo en un tenant

### B.0 · Requisitos

- Una cuenta de Microsoft 365. Con el
  [Power Apps Developer Plan](https://powerapps.microsoft.com/developerplan/) obtienes un
  entorno propio con Dataverse, sin costo y sin necesidad de licencia corporativa.
- Acceso a [make.powerapps.com](https://make.powerapps.com) y
  [make.powerautomate.com](https://make.powerautomate.com).

### B.1 · Cargar los datos

1. Ejecuta `python src/generate_seed_data.py` para tener los dos `.xlsx` al día.
2. En [make.powerapps.com](https://make.powerapps.com) → **Tablas** → **Importar** →
   **Importar datos desde Excel**, y carga cada archivo.
3. Crea las tablas `FacturasEmitidas` y `AjustesPostFacturacion` respetando los nombres de
   columna de [`02-data-model.md`](02-data-model.md). Los nombres importan: las fórmulas
   Power Fx del repositorio los usan literalmente.
4. Marca `NumeroRecibo` como columna de búsqueda alternativa en `FacturasEmitidas`.

> Si prefieres evitar Dataverse, una lista de SharePoint funciona igual para este alcance.
> Cambian los conectores, no las fórmulas.

### B.2 · Construir la Canvas App

1. Crea una app de lienzo en blanco, formato tableta.
2. Arma las cuatro pantallas descritas en
   [`powerapps/app-architecture.md`](../powerapps/app-architecture.md):
   `DashboardScreen`, `NewAdjustmentScreen`, `ApprovalQueueScreen` y `DetailAuditScreen`.
   Las maquetas de [`assets/`](assets/) muestran la disposición esperada.
3. Copia las fórmulas de
   [`powerapps/power-fx-formulas.md`](../powerapps/power-fx-formulas.md) en las propiedades
   que indica cada bloque (`App.OnStart`, `btnEnviarSolicitud.OnSelect`, etc.).
4. Aplica la paleta documentada en la arquitectura de la app.

### B.3 · Crear los flujos

Los archivos de [`powerautomate/definitions/`](../powerautomate/definitions/) son extractos
de definición en el esquema de Logic Apps: sirven como referencia de la lógica, **no se
importan directamente**. Para un flujo importable se necesita exportar una solución
`.zip` desde el propio entorno, lo cual sólo es posible después de construirlo.

1. En [make.powerautomate.com](https://make.powerautomate.com), crea los tres flujos
   siguiendo [`powerautomate/README.md`](../powerautomate/README.md).
2. El flujo 01 se dispara desde la app; conéctalo en Power Apps y ajusta el nombre que
   usan las fórmulas (`FlowNotificarAprobacionAjuste`).
3. Reemplaza los correos y canales de ejemplo (`jefatura.postfacturacion@telecom.com`,
   `#Soporte-Operaciones-Facturacion`) por los tuyos, o la tarjeta no llegará a ningún lado.

### B.4 · Verificar contra el motor de Python

Es la ventaja de tener las reglas implementadas dos veces. Registra en la app las mismas
cuatro solicitudes de `data/AjustesPostFacturacion.xlsx` y compara el estado que asigna la
app con el de `data/BitacoraDecisiones.csv`:

```bash
python src/automation_engine.py
```

Si difieren, la implementación en Power Fx se apartó de las reglas de
[`01-business-rules.md`](01-business-rules.md). Presta atención especial a los bordes
exactos (S/ 50.00 y S/ 500.00), que es donde suelen aparecer las diferencias.

### B.5 · Capturar la evidencia

Una vez funcionando, guarda en `docs/assets/`:

- Captura del `DashboardScreen` con la galería poblada.
- Captura del `NewAdjustmentScreen` mostrando el banner de validación cuando el monto
  supera la factura (regla R1 en acción: es la captura más elocuente del proyecto).
- Captura o GIF de la tarjeta adaptable recibida en Teams.
- Captura del historial de ejecuciones del flujo, con corridas exitosas.

Después sustituye las maquetas SVG del README por esas capturas y actualiza la sección
"Qué está implementado" del README raíz: el proyecto habrá dejado de ser una
especificación.

---

## Diferencias conocidas entre la especificación y un despliegue real

Cosas que esta guía no resuelve y que aparecerán al construirlo:

- **Los límites de delegación.** `Filter()` y `LookUp()` sobre miles de filas en Dataverse
  se delegan sólo con ciertos operadores. Con 10 facturas no se nota; con 20 000 sí.
- **El control de roles.** `ApprovalQueueScreen` asume un grupo de seguridad
  (`M365_Jefatura_PostFacturacion`) que hay que crear en Entra ID.
- **La respuesta de la tarjeta adaptable.** El patrón correcto es la acción
  *Post adaptive card and wait for a response*; el flujo queda en espera y consume tiempo
  de ejecución.
- **Los topes están fijos en el código.** En producción deberían venir de una tabla de
  parámetros editable por el negocio, no de constantes.
