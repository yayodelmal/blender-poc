# CU-01 REV-003 — Medición de cavidad (evidencia complementaria)

**Resultado: PASS.** Complementa la validación de `REV-003-20261103T033342Z`, cuyo informe señala que no medía la cavidad. Este run es **nuevo**: no modifica el informe, el registro ni el modelo de aquel.

## Qué se midió

Sobre `REV-003-20261103T033342Z/artifacts/CU01_REV003_planter_20261103T033342Z.blend` (entrada del run), con `herramientas/validar_malla.py --cavidad`: rayos desde el centro del hueco contra las cuatro paredes interiores (12 rayos), el piso (9 rayos) y la tapa.

- Cavidad medida 138,0 × 138,0 × 56,0 mm; esperada 138 × 138 × 56 mm (tolerancia 0,01 mm). Equivale a pared de 5 mm por lado sobre el cuerpo liso de 148 mm.
- Piso a z = 4,0 mm, plano y cerrado en los 9 rayos. Planos interiores planos. Tapa abierta.
- Se repitió también el control del volumen y la envolvente: PASS (ver `evidencias/validation_cavidad.json`).

## Control negativo

Declarar una cavidad de 128 × 128 × 56 mm sobre el mismo archivo debe fallar: el validador terminó con código 2 y marcó `cavidad_x_mm` y `cavidad_y_mm` (`evidencias/control_negativo.json`). Ese código 2 es lo esperado, por eso el registro de este run lleva `exit_code 0` para el conjunto y el detalle está en `logs/control_negativo.meta.json`.

## Calibración del método

El mismo método sobre REV-001 (esperado 108) y REV-002 (esperado 128) midió 108,0 y 128,0 mm con piso en 4,0 mm. Esas pruebas se hicieron fuera del repo y no están selladas aquí.

## Alcance

Sigue siendo un modelo digital en Blender 5.4.0 Alpha. No se exportó STL ni se imprimió; 5 mm de pared con boquilla de 0,4 mm no se ha evaluado para impresión.
