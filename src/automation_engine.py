# -*- coding: utf-8 -*-
"""
Motor de Integración y Simulación de Webhooks de Power Automate
Autor: Martín Zapana Berrospi
"""
import json
import time
import datetime
from pathlib import Path

def simular_envio_solicitud_ajuste():
    print("[*] Simulando registro de solicitud desde Power Apps...")
    solicitud = {
        "idSolicitud": "SOL-2026-00418",
        "numeroRecibo": "F001-00045218",
        "cliente": "Corporación Minera del Sur S.A.C.",
        "montoSolicitado": 145.50,
        "tipoIncidencia": "SOBREFACTURACION_DATOS",
        "analista": "martin.zapana.b@uni.pe",
        "fechaRegistro": datetime.datetime.now().isoformat()
    }
    
    print(f"    -> Solicitud creada: {solicitud['idSolicitud']} por S/ {solicitud['montoSolicitado']:.2f}")
    
    # Evaluar regla de negocio
    if solicitud["montoSolicitado"] > 30.0:
        print("    [!] Monto > S/ 30.00: Disparando Flow_Aprobacion_Ajuste a Jefatura por Teams...")
        time.sleep(0.5)
        print("    [+] Tarjeta Adaptable (Adaptive Card) entregada con éxito a Jefatura.")
        decision = "APROBADO"
        print(f"    [OK] Jefatura respondió: {decision}. Actualizando estado en Base de Datos Oracle...")
    else:
        print("    [+] Monto <= S/ 30.00: Auto-aprobado por regla operacional.")
        decision = "AUTO_APROBADO"
        
    return {"status": "SUCCESS", "decision": decision, "id": solicitud["idSolicitud"]}

if __name__ == "__main__":
    resultado = simular_envio_solicitud_ajuste()
    print(f"[COMPLETE] Resultado del flujo: {resultado}")
