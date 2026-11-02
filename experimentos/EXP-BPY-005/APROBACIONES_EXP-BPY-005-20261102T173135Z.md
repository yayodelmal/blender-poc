# Aprobaciones previas a la impresión — EXP-BPY-005

**Run de impresión:** `EXP-BPY-005-20261102T173135Z`. **Fecha de registro:** 2026-11-02T17:31Z. **Estado del experimento:** `NOT RUN` (no se ha impreso nada). Archivo nuevo; no modifica los documentos de preparación (`EXP-BPY-005-20261102T153524Z`), cuyos hashes están en su manifiesto.

## Aprobaciones recibidas del responsable (2026-11-02)

El responsable respondió que aprueba, de forma explícita, estos cuatro puntos:

| Punto | Alcance aprobado | Lo que el responsable NO indicó |
|---|---|---|
| Ficha de laminado | La ficha de `reports/RESULTADO.md` (sección "Estado posterior a la aclaración de Preview"): K1C, 0,4 mm (`0.4-Standard`), Hyper PLA, `Smooth PEI Plate / High Temp`, preset `0.20mm Standard @Creality K1C 0.4 nozzle`, 220/50 °C, capa 0,20 mm, 2 paredes, grid 15 %, sin soportes, brim automático 5 mm. Estimación del laminador: 30 min 36 s, 14,45 g, 4,84 m | — |
| Decisión sobre el adhesivo (`please apply glue before print`) | Aprobó este punto, pero **no indicó qué decidió**: si se aplica adhesivo o no, ni qué superficie física está montada ni su limpieza | Decisión concreta; cara de la PEI montada; estado de limpieza |
| Consolidación documental | La estructura `docs/`, `archivo/`, los índices, las erratas y `herramientas/sellar_artefacto.py` | — |
| Registro de EXP-BPY-005 | Preparar el registro con la ficha aprobada, sin inventar datos físicos | — |

La tolerancia física ±0,5 mm por eje, la confirmación de Hyper PLA, de cama original K1C y de K1C con boquilla de 0,4 mm ya constaban en `reports/RESULTADO.md` y no cambian.

## Entradas selladas para este run

Registro: `registro_artefactos.jsonl` (generado por `herramientas/sellar_artefacto.py`).

| artifact_id | Ruta | Tamaño | SHA-256 | Nota |
|---|---|---:|---|---|
| `stl_approved` | `../EXP-BPY-003/artifacts/EXP-BPY-003-20261102T144300Z_relief_plate.stl` | 23.984 | `c6342d689ef70742ae0f9b3d6bbbf32b4f0f542ef7a5b6be2645f3205755b3d3` | Entrada aprobada |
| `source_3mf_exp004` | `../EXP-BPY-004/artifacts/EXP-BPY-004-20261102T155417Z_slice_project.3mf` | 24.252 | `e0eaedbab02e51429a6bfe2dd254196d1cdd4d576584dcdefb3ce5bfe7c018bd` | Original: no abrir en Creality Print |
| `print_project_copy` | `artifacts/EXP-BPY-005-20261102T173135Z-print_project.3mf` | 24.252 | `e0eaedbab02e51429a6bfe2dd254196d1cdd4d576584dcdefb3ce5bfe7c018bd` | **Abrir solo esta copia.** Marcada `mutable`: la aplicación puede guardarla |

El 3MF no incluye G-code; Creality Print volverá a laminar al abrirlo, y las estimaciones pueden variar de las de la ficha.

## Antes de imprimir (lo hace la persona responsable)

1. Registrar la decisión sobre el adhesivo y la superficie: cara de la PEI montada, limpieza, y si se aplica adhesivo. Sin ese dato, el campo del registro queda `NO MEDIDO`.
2. Abrir `print_project_copy` en Creality Print, comprobar que el preset sea `0.20mm Standard @Creality K1C 0.4 nozzle` y guardar una **captura persistente** (ver `docs/04_procedimientos/CREALITY.md`).
3. Iniciar y supervisar la impresión en la K1C. Este experimento no controla la impresora.
4. Tras la impresión, recoger fotos, pie de metro (instrumento, resolución, tres medidas por eje) y completar `REGISTRO_IMPRESION.md`, `MEDICIONES_FISICAS.md` y `EVALUACION_CALIDAD.md`.
5. Verificar de nuevo con `python3 -I herramientas/sellar_artefacto.py verify --registro experimentos/EXP-BPY-005/registro_artefactos.jsonl`. El estado de `print_project_copy` podrá aparecer `CAMBIADO (mutable)` si Creality Print la guardó; es esperado y debe anotarse.

Nada de lo anterior cambia el estado: `NOT RUN` hasta que existan fotos y mediciones reales.
