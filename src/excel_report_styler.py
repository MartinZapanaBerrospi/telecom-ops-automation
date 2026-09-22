# -*- coding: utf-8 -*-
"""Reporte operacional de post-facturación con formato corporativo.

Consolida los datos del repositorio en el Excel que el flujo 02 de Power Automate
distribuye cada mañana a la jefatura (ver powerautomate/flow-02-scheduled-report.md).

Las cifras se calculan a partir de los datos, no están escritas a mano: si cambian
los datasets, cambia el reporte.

Entradas:
    data/FacturasEmitidas.xlsx
    data/AjustesPostFacturacion.xlsx
    data/BitacoraDecisiones.csv      (opcional; la produce automation_engine.py)

Salida:
    data/Reporte_Gerencial_Facturacion.xlsx con tres hojas:
      - Resumen_KPIs      indicadores del periodo contra su meta
      - Detalle_Ciclos    apertura por ciclo de facturación
      - Bitacora          dictamen de cada solicitud, si la bitácora existe

Uso:
    python src/excel_report_styler.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SALIDA = DATA_DIR / "Reporte_Gerencial_Facturacion.xlsx"

# Metas operacionales del área. En un sistema real vendrían de una tabla de
# parámetros editable por el negocio, no de constantes en el código.
META_TASA_DISPUTA_PCT = 2.0   # el monto reclamado no debería superar el 2% de lo facturado
META_PENDIENTES = 3           # solicitudes esperando decisión humana al cierre del día

# Paleta corporativa, la misma de la Canvas App (powerapps/app-architecture.md).
AZUL_CORPORATIVO = "005A9E"
AZUL_PROFUNDO = "0F172A"
VERDE_OK = "DCFCE7"
VERDE_TEXTO = "166534"
AMBAR_ALERTA = "FEF3C7"
AMBAR_TEXTO = "92400E"
GRIS_BORDE = "CBD5E1"

ESTADO_OK = "CUMPLIDO"
ESTADO_ALERTA = "EN OBSERVACION"


def _soles(monto: float) -> str:
    return f"S/ {monto:,.2f}"


def calcular_kpis(facturas: pd.DataFrame, ajustes: pd.DataFrame) -> pd.DataFrame:
    """Indicadores del periodo, cada uno contra su meta."""
    facturado = float(facturas["MontoTotal"].sum())
    reclamado = float(ajustes["MontoReclamado"].sum())
    reconocido = float(ajustes["MontoReconocido"].sum())
    tasa_disputa = (reclamado / facturado * 100) if facturado else 0.0
    pendientes = int(ajustes["EstadoReclamo"].str.startswith("PENDIENTE").sum())
    resueltas = len(ajustes) - pendientes
    tasa_resolucion = (resueltas / len(ajustes) * 100) if len(ajustes) else 0.0

    filas = [
        ("Facturacion total emitida (S/)", "-", _soles(facturado), ESTADO_OK),
        ("Recibos emitidos en el periodo", "-", f"{len(facturas):,}", ESTADO_OK),
        ("Solicitudes de ajuste registradas", "-", f"{len(ajustes):,}", ESTADO_OK),
        ("Monto reclamado por clientes (S/)", "-", _soles(reclamado), ESTADO_OK),
        ("Monto reconocido y aprobado (S/)", "-", _soles(reconocido), ESTADO_OK),
        (
            "Tasa de disputa sobre facturacion (%)",
            f"< {META_TASA_DISPUTA_PCT:.1f} %",
            f"{tasa_disputa:.2f} %",
            ESTADO_OK if tasa_disputa < META_TASA_DISPUTA_PCT else ESTADO_ALERTA,
        ),
        (
            "Solicitudes pendientes de decision",
            f"<= {META_PENDIENTES}",
            str(pendientes),
            ESTADO_OK if pendientes <= META_PENDIENTES else ESTADO_ALERTA,
        ),
        ("Tasa de resolucion de solicitudes (%)", "-", f"{tasa_resolucion:.1f} %", ESTADO_OK),
    ]
    return pd.DataFrame(
        filas, columns=["Indicador Operacional", "Meta", "Resultado Actual", "Estado"]
    )


def calcular_detalle_ciclos(facturas: pd.DataFrame, ajustes: pd.DataFrame) -> pd.DataFrame:
    """Apertura por ciclo de facturación (C01, C15, C28)."""
    ciclo_por_recibo = dict(zip(facturas["NumeroRecibo"], facturas["Ciclo"]))
    ajustes = ajustes.assign(Ciclo=ajustes["NumeroRecibo"].map(ciclo_por_recibo))

    por_ciclo = facturas.groupby("Ciclo").agg(
        recibos=("IdFactura", "count"), facturado=("MontoTotal", "sum")
    )
    ajustes_por_ciclo = ajustes.groupby("Ciclo").agg(
        solicitudes=("IdAjuste", "count"), reclamado=("MontoReclamado", "sum")
    )
    detalle = por_ciclo.join(ajustes_por_ciclo).fillna(0).reset_index()

    detalle["Recibos Emitidos"] = detalle["recibos"].astype(int)
    detalle["Solicitudes"] = detalle["solicitudes"].astype(int)
    detalle["Monto Facturado (S/)"] = detalle["facturado"].map(_soles)
    detalle["Monto Reclamado (S/)"] = detalle["reclamado"].map(_soles)
    detalle["Tasa de Disputa (%)"] = (
        detalle["reclamado"] / detalle["facturado"] * 100
    ).map(lambda valor: f"{valor:.2f} %")

    return detalle[
        [
            "Ciclo",
            "Recibos Emitidos",
            "Monto Facturado (S/)",
            "Solicitudes",
            "Monto Reclamado (S/)",
            "Tasa de Disputa (%)",
        ]
    ]


def cargar_bitacora() -> pd.DataFrame | None:
    """Lee la bitácora de decisiones si automation_engine.py ya se ejecutó."""
    ruta = DATA_DIR / "BitacoraDecisiones.csv"
    if not ruta.exists():
        return None
    return pd.read_csv(ruta).rename(
        columns={
            "id_ajuste": "ID Ajuste",
            "numero_recibo": "Recibo",
            "monto_solicitado": "Monto (S/)",
            "estado": "Dictamen",
            "aprobador": "Aprobador",
            "motivo": "Regla Aplicada",
            "fecha_evaluacion": "Evaluado",
        }
    )


def aplicar_formato(ruta: Path) -> None:
    """Formato corporativo: título, encabezados, bordes y semáforo de estado."""
    wb = openpyxl.load_workbook(ruta)
    linea = Side(style="thin", color=GRIS_BORDE)
    borde = Border(left=linea, right=linea, top=linea, bottom=linea)

    for nombre in wb.sheetnames:
        ws = wb[nombre]
        ultima_col = get_column_letter(ws.max_column)

        ws.merge_cells(f"A1:{ultima_col}1")
        titulo = ws["A1"]
        titulo.value = (
            "TELECOM - REPORTE OPERACIONAL DE POST FACTURACION "
            f"({nombre.replace('_', ' ')})"
        )
        titulo.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
        titulo.fill = PatternFill("solid", start_color=AZUL_CORPORATIVO)
        titulo.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 30

        ws.merge_cells(f"A2:{ultima_col}2")
        subtitulo = ws["A2"]
        subtitulo.value = (
            "Generado por src/excel_report_styler.py a partir de los datos "
            "del repositorio - datos ficticios"
        )
        subtitulo.font = Font(name="Calibri", size=10, italic=True, color="475569")
        subtitulo.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[2].height = 18

        for col in range(1, ws.max_column + 1):
            celda = ws.cell(row=4, column=col)
            celda.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            celda.fill = PatternFill("solid", start_color=AZUL_PROFUNDO)
            celda.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[4].height = 24

        for fila in range(5, ws.max_row + 1):
            ws.row_dimensions[fila].height = 20
            for col in range(1, ws.max_column + 1):
                celda = ws.cell(row=fila, column=col)
                celda.border = borde
                celda.font = Font(name="Calibri", size=10)
                celda.alignment = Alignment(
                    horizontal="left" if col == 1 else "center", vertical="center"
                )
                if celda.value == ESTADO_OK:
                    celda.fill = PatternFill("solid", start_color=VERDE_OK)
                    celda.font = Font(name="Calibri", size=10, bold=True, color=VERDE_TEXTO)
                elif celda.value == ESTADO_ALERTA:
                    celda.fill = PatternFill("solid", start_color=AMBAR_ALERTA)
                    celda.font = Font(name="Calibri", size=10, bold=True, color=AMBAR_TEXTO)

        for columna in ws.columns:
            ancho = max(len(str(celda.value or "")) for celda in columna)
            letra = get_column_letter(columna[0].column)
            ws.column_dimensions[letra].width = max(ancho + 4, 15)

    wb.save(ruta)


def generar_reporte() -> Path:
    """Arma el Excel con formato a partir de los datos del repositorio."""
    facturas = pd.read_excel(DATA_DIR / "FacturasEmitidas.xlsx")
    ajustes = pd.read_excel(DATA_DIR / "AjustesPostFacturacion.xlsx")

    hojas = {
        "Resumen_KPIs": calcular_kpis(facturas, ajustes),
        "Detalle_Ciclos": calcular_detalle_ciclos(facturas, ajustes),
    }

    bitacora = cargar_bitacora()
    if bitacora is not None:
        hojas["Bitacora"] = bitacora
    else:
        print(
            "Aviso: no existe data/BitacoraDecisiones.csv. Ejecuta "
            "'python src/automation_engine.py' para incluir la hoja Bitacora."
        )

    with pd.ExcelWriter(SALIDA, engine="openpyxl") as writer:
        for nombre, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre, index=False, startrow=3)

    aplicar_formato(SALIDA)

    print(f"Hojas generadas: {', '.join(hojas)}")
    print(f"Reporte escrito en: {SALIDA}")
    return SALIDA


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    generar_reporte()
