# Pruebas

```bash
pytest tests/ -q
```

Una sola suite, [`test_reglas_aprobacion.py`](test_reglas_aprobacion.py), sobre la función
`evaluar_solicitud()` de [`src/automation_engine.py`](../src/automation_engine.py).

## Qué se prueba y por qué

Las reglas de aprobación son lo único de este proyecto que puede estar mal de una forma
que nadie note. Un color equivocado en la app se ve; un tope mal comparado (`<` en lugar
de `<=`) aprueba automáticamente un ajuste que debía ir a jefatura, y no se ve nunca.

Por eso las pruebas se concentran en **los bordes exactos**, no en casos cómodos:

| Prueba | Qué fija |
|---|---|
| `test_monto_pequeno_se_autoaprueba` | Caso base de R2 |
| `test_el_tope_de_autoaprobacion_es_inclusivo` | Exactamente S/ 50.00 se autoaprueba, no escala |
| `test_monto_intermedio_escala_a_jefatura` | S/ 50.01 y S/ 500.00 son jefatura (R3), ambos extremos del rango |
| `test_monto_alto_escala_a_gerencia` | S/ 500.01 ya es gerencia (R4) |
| `test_ajuste_mayor_que_la_factura_se_rechaza` | R1 |
| `test_recibo_inexistente_se_rechaza` | R5 |
| `test_montos_no_positivos_se_rechazan` | Cero y negativos, parametrizado |
| `test_las_decisiones_pendientes_se_marcan_para_revision_humana` | Que un estado `PENDIENTE_*` traiga el aprobador responsable correcto |

Las pruebas usan las constantes `TOPE_AUTOAPROBACION` y `TOPE_JEFATURA` en lugar de
escribir `50.00` y `500.00`. Así, si mañana el negocio sube un tope, las pruebas siguen
verificando el comportamiento en el borde nuevo y no hay que reescribirlas.

## No hay pruebas de lectura de archivos

`evaluar_solicitud()` es una función pura y no toca disco: por eso se puede probar sin
`.xlsx` de por medio. `procesar_bandeja()`, que sí lee y escribe, no tiene pruebas —es
principalmente orquestación de pandas— y es la deuda conocida de esta suite.
