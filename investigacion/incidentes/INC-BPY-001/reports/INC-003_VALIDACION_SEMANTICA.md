# INC-003 — Validación semántica de la copia actual

Estado: **PASS para invariantes semánticas inspeccionadas**. Esta conclusión no implica identidad binaria con el hash incorrectamente listado ni aprueba una línea base.

## Seguridad y procedimiento

- Se verificó que la build local expone `--disable-autoexec`; la opción deshabilita scripts automáticos, incluidos Python drivers y startup scripts.
- El archivo abierto fue una copia en `evidencias/maestro_actual_copia_20261102T110754-0300.blend`, no el maestro.
- Blender: `/Applications/Blender.app/Contents/MacOS/Blender`, Blender 5.4.0 Alpha, hash de build `745ab9a3e3c5`, Python 3.13.13; el ejecutable es arm64.
- Perfil, HOME y temporales quedaron bajo `evidencias/runtime_20261102T110754-0300/` y `logs/tmp_20261102T110754-0300/`.
- Comando: Blender background, factory startup, disable-autoexec, `--python-exit-code 1`, copia .blend y el script propio de inspección.
- Inicio/fin: 2026-11-02 14:08:47–14:08:48 UTC (11:08:47–48 -0300); código de salida 0.
- El script solo lee `bpy.data`, evalúa vértices base y topología, emite JSON a stdout y no invoca operadores ni APIs de guardado.
- Hash de maestro antes y después: `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`. Hash de copia antes/después: igual.

## Resultados

| Comprobación | Esperado | Observado | Estado |
|---|---|---|---|
| Objeto en escena | Exactamente `EXP-BPY-001_Cube_20261102T105936` | Un objeto, mismo nombre, tipo MESH | PASS |
| Identidad declarada | ID `EXP-BPY-001-20261102T105936-0300`; mesh `…_Mesh` | Coinciden nombre, mesh e ID | PASS |
| Dimensiones | 50 × 50 × 50 mm ±0,01 | 50,00000074505806 mm por eje; desviación +0,00000074505806 mm | PASS |
| Centro geométrico | (0,0,0) mm ±0,01 | (0,0,0) mm | PASS |
| Transformación | loc/rot (0,0,0), escala (1,1,1) | Coincide | PASS |
| Unidades | METRIC, scale_length 1, display MILLIMETERS | Coincide | PASS |
| Propiedades | parameters_mm 50/50/50, units mm, ID original | Coinciden | PASS |
| Topología | 8 vértices, 12 aristas, 6 caras, 1 componente, manifold | Coincide | PASS |
| Procesadores inesperados | Sin modificadores, sin shape keys | 0 y ninguno | PASS |
| Scripts/drivers embebidos detectables | Ningún Text datablock/driver | Lista vacía de ambos | PASS |

Las propiedades `parameters_mm` son metadatos, no un parámetro reactivo vinculado a la malla. El mecanismo funcional de construcción sigue siendo el script generador que calcula vértices desde sus constantes; esta inspección no afirma parametricidad reactiva.

## Evidencia y límites

Log JSON completo: `../logs/semantic_readonly_20261102T110754-0300.log`. Metadatos de ejecución: `../logs/semantic_readonly_20261102T110754-0300.meta`. Script propio revisado: `../evidencias/inspect_copy_readonly_20261102T110754.py`.

La inspección verifica la geometría de la malla base. No se encontraron modificadores ni shape keys que requirieran evaluación adicional. Una coincidencia geométrica no demuestra equivalencia binaria ni permite reconstruir el hash contemporáneo faltante.
