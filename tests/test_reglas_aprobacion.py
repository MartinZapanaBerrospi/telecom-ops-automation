# -*- coding: utf-8 -*-
"""Pruebas de las reglas de aprobación de ajustes."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from automation_engine import (  # noqa: E402
    TOPE_AUTOAPROBACION,
    TOPE_JEFATURA,
    evaluar_solicitud,
)

FACTURA = 1000.00


def dictamen(monto, monto_factura=FACTURA):
    return evaluar_solicitud("AJU-TEST", "F001-00000001", monto, monto_factura).estado


def test_monto_pequeno_se_autoaprueba():
    assert dictamen(25.00) == "APROBADO_AUTO"


def test_el_tope_de_autoaprobacion_es_inclusivo():
    assert dictamen(TOPE_AUTOAPROBACION) == "APROBADO_AUTO"


def test_monto_intermedio_escala_a_jefatura():
    assert dictamen(TOPE_AUTOAPROBACION + 0.01) == "PENDIENTE_JEFATURA"
    assert dictamen(TOPE_JEFATURA) == "PENDIENTE_JEFATURA"


def test_monto_alto_escala_a_gerencia():
    assert dictamen(TOPE_JEFATURA + 0.01) == "PENDIENTE_GERENCIA"


def test_ajuste_mayor_que_la_factura_se_rechaza():
    assert dictamen(1200.00) == "RECHAZADO"


def test_recibo_inexistente_se_rechaza():
    assert dictamen(10.00, monto_factura=None) == "RECHAZADO"


@pytest.mark.parametrize("monto", [0, -15.5])
def test_montos_no_positivos_se_rechazan(monto):
    assert dictamen(monto) == "RECHAZADO"


def test_las_decisiones_pendientes_se_marcan_para_revision_humana():
    decision = evaluar_solicitud("AJU-TEST", "F001-00000001", 120.00, FACTURA)
    assert decision.requiere_aprobacion_humana is True
    assert decision.aprobador == "JEFATURA"
