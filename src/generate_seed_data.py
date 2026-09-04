# -*- coding: utf-8 -*-
"""
Generador de Datasets de Prueba (Seed Data) para Power Apps / Dataverse / SharePoint
Crea:
1. data/FacturasEmitidas.xlsx
2. data/AjustesPostFacturacion.xlsx
Autor: Martín Zapana Berrospi
"""
import pandas as pd
from pathlib import Path
import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def generar_datasets():
    # 1. Facturas Emitidas (Sector Telecomunicaciones)
    facturas = [
        {"IdFactura": "FAC-1001", "NumeroRecibo": "F001-00045210", "IdCliente": "CLI-801", "ClienteNombre": "Minera Las Bambas S.A.", "TipoDocumento": "RUC", "NumeroDocumento": "20554896321", "PlanNombre": "Plan Corporativo Móvil Ilimitado 120", "MontoTotal": 450.00, "Ciclo": "C01", "FechaEmision": "2026-08-01", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1002", "NumeroRecibo": "F001-00045211", "IdCliente": "CLI-802", "ClienteNombre": "Juan Carlos Pérez Gómez", "TipoDocumento": "DNI", "NumeroDocumento": "45896321", "PlanNombre": "Plan Móvil Postpago 69.90", "MontoTotal": 89.90, "Ciclo": "C01", "FechaEmision": "2026-08-01", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1003", "NumeroRecibo": "F001-00045212", "IdCliente": "CLI-803", "ClienteNombre": "Distribuidora Lima Norte S.A.C.", "TipoDocumento": "RUC", "NumeroDocumento": "20601245897", "PlanNombre": "Plan Negocios Fibra Óptica 200MB", "MontoTotal": 280.00, "Ciclo": "C01", "FechaEmision": "2026-08-01", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1004", "NumeroRecibo": "F001-00045213", "IdCliente": "CLI-804", "ClienteNombre": "María Elena Rodríguez Prado", "TipoDocumento": "DNI", "NumeroDocumento": "71254896", "PlanNombre": "Plan Móvil Conectado 49.90", "MontoTotal": 49.90, "Ciclo": "C15", "FechaEmision": "2026-08-15", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1005", "NumeroRecibo": "F001-00045214", "IdCliente": "CLI-805", "ClienteNombre": "Constructora Graña & Asociados", "TipoDocumento": "RUC", "NumeroDocumento": "20100458963", "PlanNombre": "Troncal SIP Flota Móvil 50 Líneas", "MontoTotal": 3250.00, "Ciclo": "C15", "FechaEmision": "2026-08-15", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1006", "NumeroRecibo": "F001-00045215", "IdCliente": "CLI-806", "ClienteNombre": "Carlos Alberto Mendoza Solís", "TipoDocumento": "DNI", "NumeroDocumento": "10458963", "PlanNombre": "Plan Móvil Premium Roaming Plus", "MontoTotal": 175.40, "Ciclo": "C15", "FechaEmision": "2026-08-15", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1007", "NumeroRecibo": "F001-00045216", "IdCliente": "CLI-807", "ClienteNombre": "Textil San Pedro E.I.R.L.", "TipoDocumento": "RUC", "NumeroDocumento": "20489632145", "PlanNombre": "Plan Empresarial Enlace Dedicado", "MontoTotal": 540.00, "Ciclo": "C28", "FechaEmision": "2026-08-28", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1008", "NumeroRecibo": "F001-00045217", "IdCliente": "CLI-808", "ClienteNombre": "Lucía Valeria Quispe Huamán", "TipoDocumento": "DNI", "NumeroDocumento": "48963251", "PlanNombre": "Plan Residencial Dúo Voz & Internet", "MontoTotal": 55.90, "Ciclo": "C28", "FechaEmision": "2026-08-28", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1009", "NumeroRecibo": "F001-00045218", "IdCliente": "CLI-809", "ClienteNombre": "Corporación Minera del Sur S.A.C.", "TipoDocumento": "RUC", "NumeroDocumento": "20334455667", "PlanNombre": "Plan Telecom Enterprise Voz & Datos Ilimitado", "MontoTotal": 1820.00, "Ciclo": "C28", "FechaEmision": "2026-08-28", "EstadoPago": "EMITIDO"},
        {"IdFactura": "FAC-1010", "NumeroRecibo": "F001-00045219", "IdCliente": "CLI-810", "ClienteNombre": "Roberto Alonso Chávez Ramos", "TipoDocumento": "DNI", "NumeroDocumento": "46985214", "PlanNombre": "Plan Móvil Ultra 79.90", "MontoTotal": 124.50, "Ciclo": "C28", "FechaEmision": "2026-08-28", "EstadoPago": "EMITIDO"}
    ]
    df_facturas = pd.DataFrame(facturas)
    facturas_path = DATA_DIR / "FacturasEmitidas.xlsx"
    df_facturas.to_excel(facturas_path, index=False, sheet_name="Facturas")
    print(f"[OK] Facturas generadas en: {facturas_path}")

    # 2. Ajustes Post Facturacion
    ajustes = [
        {"IdAjuste": "AJU-2026-001", "IdFactura": "FAC-1002", "NumeroRecibo": "F001-00045211", "IdCliente": "CLI-802", "ClienteNombre": "Juan Carlos Pérez Gómez", "TipoIncidencia": "SOBREFACTURACION_DATOS", "MontoReclamado": 20.00, "MontoReconocido": 20.00, "EstadoReclamo": "APROBADO_AUTO", "UsuarioAnalista": "analista.ops@telecom.com", "FechaRegistro": "2026-08-05 10:15:00", "Justificacion": "Cargo indebido por paquete adicional no solicitado por el cliente."},
        {"IdAjuste": "AJU-2026-002", "IdFactura": "FAC-1006", "NumeroRecibo": "F001-00045215", "IdCliente": "CLI-806", "ClienteNombre": "Carlos Alberto Mendoza Solís", "TipoIncidencia": "DESFASE_ROAMING", "MontoReclamado": 85.50, "MontoReconocido": 85.50, "EstadoReclamo": "APROBADO_JEFATURA", "UsuarioAnalista": "analista.ops@telecom.com", "FechaRegistro": "2026-08-18 14:30:00", "Justificacion": "Tarificación errónea de datos en zona fronteriza con corte no advertido."},
        {"IdAjuste": "AJU-2026-003", "IdFactura": "FAC-1009", "NumeroRecibo": "F001-00045218", "IdCliente": "CLI-809", "ClienteNombre": "Corporación Minera del Sur S.A.C.", "TipoIncidencia": "DESCUENTO_NO_APLICADO", "MontoReclamado": 145.50, "MontoReconocido": 0.00, "EstadoReclamo": "PENDIENTE_JEFATURA", "UsuarioAnalista": "martin.zapana.b@uni.pe", "FechaRegistro": "2026-09-01 09:20:00", "Justificacion": "Convenio corporativo anual con descuento del 8% no imputado en el ciclo."},
        {"IdAjuste": "AJU-2026-004", "IdFactura": "FAC-1010", "NumeroRecibo": "F001-00045219", "IdCliente": "CLI-810", "ClienteNombre": "Roberto Alonso Chávez Ramos", "TipoIncidencia": "CARGO_DUPLICADO", "MontoReclamado": 44.60, "MontoReconocido": 0.00, "EstadoReclamo": "PENDIENTE_JEFATURA", "UsuarioAnalista": "martin.zapana.b@uni.pe", "FechaRegistro": "2026-09-02 11:45:00", "Justificacion": "Doble cobro de servicio de valor agregado (SVA) digital no activado."}
    ]
    df_ajustes = pd.DataFrame(ajustes)
    ajustes_path = DATA_DIR / "AjustesPostFacturacion.xlsx"
    df_ajustes.to_excel(ajustes_path, index=False, sheet_name="Ajustes")
    print(f"[OK] Ajustes generados en: {ajustes_path}")

if __name__ == "__main__":
    generar_datasets()
