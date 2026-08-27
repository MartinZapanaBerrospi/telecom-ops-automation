# ⚡ Telecom Operations & Power Platform Automation Pipeline

[![Power Apps](https://img.shields.io/badge/Power_Apps-Canvas_App_UI-742774?style=for-the-badge&logo=powerapps&logoColor=white)](https://powerapps.microsoft.com/)
[![Power Automate](https://img.shields.io/badge/Power_Automate-Cloud_Workflows-0066FF?style=for-the-badge&logo=powerautomate&logoColor=white)](https://powerautomate.microsoft.com/)
[![Microsoft 365](https://img.shields.io/badge/Microsoft_365-Teams_%26_Outlook-D83B01?style=for-the-badge&logo=microsoft&logoColor=white)](https://www.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-Automation_Engine-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Excel](https://img.shields.io/badge/MS_Excel-Executive_Styling-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/excel)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> Solución integral de **Automatización Operacional y Power Platform (Power Apps + Power Automate)** diseñada para optimizar los procesos de **Post Facturación, Auditoría de Ajustes y Distribución de Reportes** en empresas de Telecomunicaciones.

---

## 🎯 Caso de Uso Operacional

En el área de **Soporte Operacional de Post Facturación (Claro / Telcos)**, cientos de solicitudes de notas de crédito, reprocesamiento de recibos y reclamos de clientes se gestionan mensualmente. Realizar este proceso de forma manual o por cadenas de correo genera:
* Tiempos de respuesta lentos en la aprobación de ajustes.
* Falta de trazabilidad y riesgo de doble compensación económica.
* Retrasos diarios en el envío de reportes a la jefatura.

Esta solución implementa una **Canvas App en Power Apps** conectada a flujos en **Power Automate**, con **Adaptive Cards en Teams** y un motor de reportes en **Python & Excel**.

---

## 🏗️ Arquitectura de la Solución

```
+------------------------------------+        +------------------------------------+
|       Microsoft Power Apps         |  --->  |      Microsoft Power Automate      |
|  - Registro de Ajustes de Recibo   |        |  - Flujo 1: Aprobaciones Multinivel|
|  - Validación de Topes en Tiempo Real|      |  - Flujo 2: Reporte Diario 8:00 AM |
|  - Bandeja de Auditoría & KPIs     |        |  - Flujo 3: Alerta Webhook Descuadre|
+------------------------------------+        +-----------------+------------------+
                                                                |
                                        +-----------------------+-------------------+
                                        |                                           |
                                        v                                           v
                        +-------------------------------+           +-------------------------------+
                        |        Microsoft Teams        |           |      Motor Python & Excel     |
                        |   - Adaptive Cards con Botones|           |   - Generación Automatizada   |
                        |     de Aprobación Interactiva |           |   - Estilizado Corporativo    |
                        +-------------------------------+           +-------------------------------+
```

---

## 📂 Contenido del Repositorio

```
telecom-ops-automation/
├── powerapps/
│   ├── APP_ARCHITECTURE.md        # Especificación técnica y diseño de pantallas de la app
│   ├── POWER_FX_FORMULAS.md       # Catálogo de fórmulas Power Fx (Patch, LookUp, Filter, User)
│   └── msapp_definition.json      # Esquema de datos y variables de contexto
├── powerautomate/
│   ├── FLOW_01_APPROVAL_SYSTEM.md # Flujo de aprobaciones con Adaptive Cards para Teams/Outlook
│   ├── FLOW_02_SCHEDULED_REPORT.md# Flujo programado (Recurrent Trigger) de reportes diarios
│   ├── FLOW_03_DATA_ALERT_TRIGGER.md # Flujo de alertas inmediatas por anomalías en ciclo
│   └── flows_definitions/         # Definiciones exportables JSON para importar en Power Automate
│       ├── approval_flow.json
│       └── report_distribution.json
├── src/
│   ├── automation_engine.py       # Motor de simulación de solicitudes y webhooks
│   └── excel_report_styler.py     # Generador de reportes Excel estilizados con formato Claro
├── docs/
│   └── PROCESS_BLUEPRINT.md       # Diagrama de flujo del proceso de inicio a fin
├── requirements.txt
└── README.md
```

---

## ⚡ Aspectos Técnicos Destacados

### 1. Fórmulas Power Fx (Validación y Envío Seguro)
```powerfx
If(
    Value(txtMontoSolicitado.Text) > varMontoOriginal,
    Notify("El monto solicitado no puede superar el total de la factura.", NotificationType.Error, 4000),
    
    // Registro mediante Patch
    Patch(
        AjustesPostFacturacion,
        Defaults(AjustesPostFacturacion),
        {
            NumeroRecibo: txtNumeroRecibo.Text,
            MontoReclamado: Value(txtMontoSolicitado.Text),
            EstadoReclamo: "PENDIENTE_APROBACION",
            UsuarioAnalista: User().Email,
            FechaRegistro: Now()
        }
    );
    // Disparo inmediato a Power Automate
    FlowNotificarAprobacionAjuste.Run(txtNumeroRecibo.Text, Value(txtMontoSolicitado.Text))
);
```

### 2. Tarjetas Adaptables Interactivas (MS Teams & Outlook)
Los supervisores y jefaturas reciben en Teams una tarjeta con el desglose del reclamo y botones de un solo clic para **Aprobar** o **Rechazar**, sin necesidad de ingresar a sistemas externos.

---

## 🚀 Cómo Ejecutar los Scripts de Simulación

```bash
# 1. Clonar el repositorio
git clone https://github.com/MartinZapanaBerrospi/telecom-ops-automation.git
cd telecom-ops-automation

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Probar el motor de simulación de flujos
python src/automation_engine.py

# 4. Generar el reporte ejecutivo estilizado en Excel
python src/excel_report_styler.py
```

---

## 👨‍💻 Autor

**Martín Zapana Berrospi**
* 🎓 Bachiller en Ciencias (Matemática) & Estudiante de Ingeniería de Sistemas (8vo Ciclo) — **Universidad Nacional de Ingeniería (UNI)**
* 💼 LinkedIn: [martin-eduardo-zapana-berrospi](https://www.linkedin.com/in/martin-eduardo-zapana-berrospi/)
* 🌐 Portafolio: [martinzapana.com](https://martinzapana.com)
