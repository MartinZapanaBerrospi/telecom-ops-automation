# -*- coding: utf-8 -*-
"""Motor de reglas de aprobación de ajustes de post-facturación.

Implementa en Python las mismas reglas que la Canvas App valida con Power Fx y
que el flujo de Power Automate ejecuta en la nube, de modo que puedan probarse
y auditarse sin desplegar nada en un tenant de Microsoft 365.

Reglas (fuente de verdad: docs/01-business-rules.md):
  R1. El ajuste no puede superar el monto de la factura original.
  R2. Monto <= S/ 50.00            -> aprobación automática.
  R3. S/ 50.00 < monto <= S/ 500   -> aprobación de jefatura vía Teams.
  R4. Monto > S/ 500.00            -> escala a gerencia.
  R5. La factura referida debe existir en el maestro de facturas emitidas.

Uso:
    python src/automation_engine.py

Salida:
    data/BitacoraDecisiones.csv con el dictamen de cada solicitud.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

TOPE_AUTOAPROBACION = 50.00
TOPE_JEFATURA = 500.00


@dataclass(frozen=True)
class Decision:
    """Resultado de evaluar una solicitud de ajuste."""

    id_ajuste: str
    numero_recibo: str
    monto_solicitado: float
    estado: str
    aprobador: str
    motivo: str

    @property
    def requiere_aprobacion_humana(self) -> bool:
        return self.estado.startswith("PENDIENTE")


def evaluar_solicitud(id_ajuste: str, numero_recibo: str, monto_solicitado: float,
                      monto_factura: float | None) -> Decision:
    """Aplica las reglas R1-R5 a una solicitud y devuelve su dictamen."""
    if monto_factura is None:
        return Decision(id_ajuste, numero_recibo, monto_solicitado, "RECHAZADO",
                        "SISTEMA", "R5: el recibo no existe en el maestro de facturas emitidas")

    if monto_solicitado <= 0:
        return Decision(id_ajuste, numero_recibo, monto_solicitado, "RECHAZADO",
                        "SISTEMA", "El monto solicitado debe ser mayor que cero")

    if monto_solicitado > monto_factura:
        return Decision(id_ajuste, numero_recibo, monto_solicitado, "RECHAZADO", "SISTEMA",
                        f"R1: el ajuste supera el monto facturado (S/ {monto_factura:,.2f})")

    if monto_solicitado <= TOPE_AUTOAPROBACION:
        return Decision(id_ajuste, numero_recibo, monto_solicitado, "APROBADO_AUTO", "SISTEMA",
                        f"R2: monto dentro del tope de autoaprobación (S/ {TOPE_AUTOAPROBACION:,.2f})")

    if monto_solicitado <= TOPE_JEFATURA:
        return Decision(id_ajuste, numero_recibo, monto_solicitado, "PENDIENTE_JEFATURA", "JEFATURA",
                        "R3: requiere aprobación de jefatura por tarjeta adaptable en Teams")

    return Decision(id_ajuste, numero_recibo, monto_solicitado, "PENDIENTE_GERENCIA", "GERENCIA",
                    f"R4: monto mayor a S/ {TOPE_JEFATURA:,.2f}; escala a gerencia")


def procesar_bandeja(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Evalúa todas las solicitudes pendientes y registra la bitácora de decisiones."""
    facturas = pd.read_excel(data_dir / "FacturasEmitidas.xlsx")
    ajustes = pd.read_excel(data_dir / "AjustesPostFacturacion.xlsx")

    montos_por_recibo = dict(zip(facturas["NumeroRecibo"], facturas["MontoTotal"]))

    decisiones = [
        evaluar_solicitud(
            fila["IdAjuste"],
            fila["NumeroRecibo"],
            float(fila["MontoReclamado"]),
            montos_por_recibo.get(fila["NumeroRecibo"]),
        )
        for _, fila in ajustes.iterrows()
    ]

    bitacora = pd.DataFrame([asdict(d) for d in decisiones])
    bitacora["fecha_evaluacion"] = datetime.now().isoformat(timespec="seconds")
    salida = data_dir / "BitacoraDecisiones.csv"
    bitacora.to_csv(salida, index=False, encoding="utf-8")

    print(f"Solicitudes evaluadas: {len(bitacora)}")
    for estado, cantidad in bitacora["estado"].value_counts().items():
        print(f"  {estado:<20} {cantidad}")
    print(f"Bitácora escrita en: {salida}")
    return bitacora


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    procesar_bandeja()
