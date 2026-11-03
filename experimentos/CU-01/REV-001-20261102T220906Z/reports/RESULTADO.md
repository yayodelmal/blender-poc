# CU-01 — REV-001 — Resultado digital

**Resultado: PASS para validación geométrica digital.** Esta revisión crea el macetero CU-01 solicitado y valida el archivo `.blend` en un proceso de Blender independiente del proceso de construcción.

## Especificación aprobada

- Envolvente total: 150 × 150 × 60 mm, incluido el relieve.
- Cuerpo cuadrado abierto arriba; paredes de 20 mm.
- Base cerrada de 4 mm, sin perforaciones de drenaje.
- Cavidad derivada: 108 × 108 × 56 mm.
- Relieve de ladrillo real en cuatro caras: nominal 15 × 7 mm, 1 mm de relieve, juntas de 1,2 mm y aparejo alternado con continuidad en las esquinas.

## Validación observada

- Envolvente medida: 150,000021 × 150,000021 × 60,000002 mm; dentro de ±0,01 mm.
- Una sola componente cerrada, manifold, orientación coherente y volumen positivo.
- Sin aristas ni caras degeneradas.
- Cavidad 108 × 108 × 56 mm; apertura superior comprobada y piso cerrado a z≈4 mm. Siete rayos de muestra confirmaron el piso; no se encontraron perforaciones en esas muestras.
- 264 parches de ladrillo en total: 66 por cara y siete hiladas por cara. Juntas medidas aproximadamente 1,2 mm.
- Volumen firmado medido: 688.081,907 mm³; esperado: 688.081,6 mm³; diferencia dentro de la tolerancia configurada de 1 mm³.
- Blender 5.4.0 Alpha, build `745ab9a3e3c5`; ejecutable SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`.

## Ajuste del patrón

Para cubrir cada cara de 148 mm conservando juntas de 1,2 mm y el aparejo alternado, las piezas de extremo se ajustan: 16,7 mm en hiladas pares y 8,6 mm en impares. Las piezas interiores permanecen nominalmente en 15 mm. Por lo tanto, el patrón respeta la dimensión nominal, pero **no todas las piezas son exactamente de 15 mm**.

## Historial de construcción

- `REV-001-20261102T220143Z`: fallo del script durante la limpieza de un objeto borrado; no se guardó un `.blend`.
- `REV-001-20261102T220547Z`: el validador observó 209 componentes, geometría no manifold y altura de 56,2 mm. Se conserva como intento fallido.
- `DIAG-BOOLEAN-20261102T220718Z`: ensayos en memoria mostraron que un lado y lados opuestos se podían unir; incluir caras adyacentes en el mismo operando falló en las ramas observadas. Esto no prueba una causa general de Blender.
- `REV-001-20261102T220906Z`: se construyó y unió cada cara secuencialmente. La validación independiente pasó.

## Alcance

Este resultado cubre el modelo digital y sus mediciones en Blender Alpha. No valida una versión estable de Blender, tolerancias de impresión física, fabricación ni resistencia de uso. No se exportó STL, no se usó Creality Print y no se imprimió el modelo. El maestro EXP-BPY-003 y los experimentos históricos no se modificaron.

## Archivos

- `artifacts/CU01_REV001_planter_20261102T220906Z.blend` — modelo validado.
- `evidencias/validation.json` — mediciones y controles detallados.
- `registro_artefactos.jsonl` — hashes del modelo y evidencias.
